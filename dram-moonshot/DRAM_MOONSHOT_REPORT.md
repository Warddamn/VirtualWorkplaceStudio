# DRAM Moonshot: what a $1M team could prove about new ways to make working memory

*Final report of the invention study set out in [MISSION.md](MISSION.md). As of 2026-11-02.*

**How to read this report.**
- **Sources.** Every number comes from a file in this folder, linked in the text. The final decision is [research/stage3/decision.json](research/stage3/decision.json). It rests on three judge files ([physicist](research/stage3/judge_physicist.json), [investor](research/stage3/judge_investor.json), [operator](research/stage3/judge_operator.json)) and ten red-teamed dossiers in [dossiers/](dossiers/).
- **Conflicts.** Where files disagree, the later stage wins: red-team responses and dossier section 11, then the dossier body, then Stage 3 notes, then Stage 2, then screening. [FINAL_CONCEPTS.md](research/stage3/FINAL_CONCEPTS.md) predates the red team, so its headline numbers appear only when labelled "pre-red-team".
- **Evidence tags**, as the sources use them:
  - [REPORTED]: from a logged source, almost always a web search snippet;
  - [MODEL]: output of a Python model in `models/` or `research/models/`;
  - [ESTIMATE]: arithmetic or judgment the source tags as an estimate;
  - [SPECULATIVE]: untested physics or process;
  - [UNVERIFIED]: not confirmed. [UNVERIFIED-PK] means prior knowledge with no logged URL.
- **Untagged numbers.** Counts of ideas, objections and verdicts come from data files and carry no tag. Judge confidences are judgments.

---

## 1. The answer in one page

**Headline** ([decision.json](research/stage3/decision.json)):

> "No free lunch and no physics kill: 10,525 distinct ideas funneled to 10 concepts; all 10 survived 181 red-team objections but were downgraded (~2x on headline claims). The durable step changes are energy per bit moved next to compute (~10x), refresh bought with coding (~9x), and density from tier count without EUV (4.6-5.9x) — not cheap bits (<=1.6x bits/$ vs a projected 2032 incumbent)."

Three judges read the red-teamed dossiers without seeing each other: a physicist-founder, a deep-tech investor and a Thiel-fellow operator. All three made the same three picks.

**BEST BET: [HOT-SIDE MEMORY](dossiers/hot-side-memory.md).**
- **What.** Oxide-semiconductor gain cells: two thin-film transistors, no capacitor. 16 tiers of them sit in the carrier wafer that backside-power chips already need, bonded face to face onto the GPU.
- **Step change.**
  - ~10x lower energy per bit delivered than HBM (high-bandwidth memory): 0.37 vs 3.95 pJ/bit [MODEL].
  - ~90 W saved per GPU at the 16-tier, 1-bit-per-cell planning case; range 48-169 W [MODEL].
- **Decisive experiment.** "Gate A+" by month 11 (2027-11-30), ~$240k standalone [ESTIMATE]. Test chips in four oxide channels, after a real 350-400 °C bond, with ≥1e5 cells per split.
- **Kill line.** Kill the capacity claim if every split fails one of three tests: weakest-cell (1e-4 tail) retention ≥1 s at 105 °C, drift σ ≤75 mV, or noise (RTN) 1e-4 quantile ≤100 mV.
- **Judge confidence:** 0.45-0.55.

**FASTEST PROOF: [RAW-BER CONTRACT](dossiers/raw-ber-contract.md).**
- **What.** Error-correcting codes (ECC) carry the rare weak bits, as a flash controller does for NAND, so DRAM refresh can run far less often.
- **Step change.**
  - ~9x less refresh energy on DDR5 server modules at 85 °C, keeping chipkill [MODEL]. Chipkill is the code that survives a dead chip.
  - ~13x on retired DDR4 behind a CXL (memory-expansion link) controller [MODEL].
- **Decisive experiment.** Phase 1 runs on DRAM Bender test stations and open DDR5 testers. No fab, no new physics. ~$124k [ESTIMATE], yes/no at month 6 (2027-06-30).
- **Kill line.** NO-GO if any of these holds:
  - the chipkill-safe interval, including variable retention time (VRT), is <4x the JEDEC standard refresh window at 65 °C;
  - multi-chip events are >10%;
  - a 1-hour grade holds on <95% of modules over 1,000 h.
- **Judge confidence:** 0.6-0.7.

**MOONSHOT: [AND-STACK](dossiers/and-stack.md).**
- **What.** It builds DRAM the way 3D NAND is built: many deposited layers, one hole etch, a capacitorless 2-bit oxide cell at each tier.
- **Step change.**
  - Density: 64 tiers × 2 bits = 2.62 Gb/mm², 5.9x 1-beta, today's leading DRAM node [MODEL].
  - Cost: ~2.3x bits per dollar vs 2026, but 1.1-1.4x vs a projected 2032 incumbent [MODEL].
  - ~25x lower refresh power, and no EUV lithography [MODEL].
- **Decisive experiment.** Planar GO #1A at month 9 on the shared oxide lot. Then a 2-tier vertical "closure coupon" (GO #1B) at months 14-16, ~$0.4M standalone to that gate [ESTIMATE]. P(closure) ~20% [ESTIMATE].
- **Kill line.** At month 18, if the coupon has not closed, kill single-etch and fall back to a per-tier patterned cell.
- **Judge confidence:** 0.12-0.6. The judges differ: physicist 0.12, operator 0.35, investor 0.6.

**The biggest unknown.** The statistical tails of small amorphous-oxide transistors (IGZO, IGO, ZTO; ≤0.01-0.02 µm²), after the full ≤400 °C hydrogen, thermal and bonding budget, at 85-125 °C. Two numbers decide it:
- the 1e-4 to 2e-5 quantile of attoamp-level off-state leakage (1 aA = 1e-18 A);
- the 1e-4 quantile of random telegraph noise (RTN), from nanoseconds to seconds.

Published data describe median cells, while every pass line sits in the tail. One measurement campaign sets the size of the step for 7 of the 10 concepts.

**The Monday action.** In ≤2 hours, write a one-page "Oxide Tail Spec":
- rows: device structures;
- columns: channel splits, device area, timescale, temperature, hydrogen/thermal dose, bond split, and each concept's pass/kill line, copied from the dossiers' section 5 and 11 thresholds.

Send it to an oxide-transistor university group with external-user access; the judges name Purdue's Birck Nanotechnology Center. Ask whether they can run it and at what cost.

**The $1M** funds one shared "Oxide Tail Statistics" wafer lot that answers the question seven concepts share. A fab-free DRAM error study sets the ECC budget every cell model uses. Larger spends release only after cheaper gates pass (section 8).

---

## 2. The question we asked

**DRAM-class memory** means byte-addressable working memory with ~10-100 ns access and effectively unlimited endurance, natively or through architecture ([MISSION.md](MISSION.md)). A concept had to promise a step change on at least one axis:
- cost per bit;
- density;
- energy per bit, including refresh;
- capital intensity: fab dollars, mask count, EUV dependence;
- resource intensity: scarce or concentrated inputs, energy, water, PFAS;
- U.S. manufacturability.

**The founder's framing.** "Anything is possible if executed correctly, and persistence is how breakthroughs happen."
- **No business kills.** No idea was killed for business reasons, time to revenue or founder fit.
- **Kill only for physics.** An idea dies only if it violates physics, or hits a known show-stopper with no plausible way around it.
- **Every kill names its revival condition:** what would have to be true for the idea to live.

**The $1M frame.** A Thiel-Fellow-style team:
- **Money and team:** a $1M seed and two full-time founders, one a recruited device or circuit expert.
- **Demo:** a convincing one in 18-24 months, using multi-project-wafer (MPW) shuttles, university nanofabs and national-lab user facilities.
- **Next:** a $10-50M raise, then licensing, partnering or fab-lite.

The sister study `../ram-venture/` judged memory ideas as small businesses. This one judges them as inventions.

---

## 3. Is "we don't have the natural resources" true?

**Verdict: PARTLY TRUE, but not in the way the premise states it** ([A2](research/phaseA/A2_materials_resources.md)). Geology is not the limit. Chokepoints, capital, time and local power are.

**Geology: not supported.**
- **Per GB.** A GB of DRAM holds ~42 mg of silicon. It takes ~0.42 kWh of fab electricity and ~2.6 L of gross water [ESTIMATE].
- **Fleet-wide** (~22M wafers/yr) [ESTIMATE]:
  - tungsten ~150 t, ~0.17% of world supply;
  - copper ~44 t, <0.001%;
  - zirconium ~19 t, <0.01%;
  - electricity ~29 TWh, ~0.1% of world use.
- **Cost.** All listed metals together cost under $25 per $3,800 wafer, even at 2026 record prices [ESTIMATE].
- **History.** A2 found no DRAM output lost to a raw-material shortage in 2022-2026. That covers the neon spike, the tungsten and hafnium spikes and the 2026 Qatar helium shock.

**Chokepoints: true, and live** [REPORTED]:

| Chokepoint | Concentration and signal |
|---|---|
| Helium | Qatar ~30% of supply, offline since March 2026; Korea took 64.7% of its helium from Qatar in 2025; spot ~2x |
| High-purity quartz (crucibles) | Spruce Pine, NC: >80% |
| Tungsten | China ~80%; APT +350% YTD in 2026 |
| Hafnium | Chinese export controls; ~$5k → ~$13k/kg |
| Ga, Ge, Sb, rare earths | Chinese controls; suspensions expire November 2026 |
| EUV scanners | ASML only, ~65 per year |
| Photoresist, PFAS | Japan ~90% of resist; 3M exited PFAS end-2025; EU restriction from ~2028 |

**What binds supply in 2026-2028: capital, cleanroom time and tools.**
- Micron sees DRAM bit growth only in the low-20s % in 2027-28. It expects no meaningful output from new cleanrooms until late 2028 or later [REPORTED].
- Industry DRAM capex is $61.3B in 2026 [REPORTED], and new capacity costs ~$145-170k per wafer-start-per-month.
- HBM uses ~2.5-3x the wafer area per GB of DDR5 [ESTIMATE].
- Megafab sites hit local limits: Yongin needs ~15 GW against <2 GW of local supply [REPORTED].

**Use phase.** A server GB burns ~6.6 kWh over 5 years, ~16x its fab electricity [ESTIMATE].

**A warning.** Some "new DRAM" chemistries would create limits today's DRAM does not have [ESTIMATE]:
- ruthenium electrodes: 26-176% of world Ru;
- HZO ferroelectrics: 14-41% of separated Hf;
- 3D Si/SiGe superlattices: 6-38% of refined Ge.

IGZO is fine on quantity (In and Ga under 0.4%), but gallium is ~98% Chinese [UNVERIFIED-PK]. So every oxide concept carries Ga-free channel splits.

**Consequence for the search.** The final portfolio targets the binding inputs:
- use-phase energy: HOT-SIDE, RAW-BER;
- EUV and capital: AND-STACK, CELL-WAFER FOUNDRY;
- helium: LEAN ARRAY MODULE.

---

## 4. Why DRAM is stuck

[A1](research/phaseA/A1_scaling_limits.md) ranks ten bottlenecks. A1 tags model numbers [ESTIMATE] and web facts [REPORTED via snippet]. The last column maps them to this study's final concepts.

| # | Bottleneck | Today (A1) | What a fix must do | Wall type | Concepts attacking it |
|---|---|---|---|---|---|
| 1 | Capacitor charge wall | Cs 5.4 fF (1-beta) → 4.5 fF (1c); aspect ratio 60-75; 7 fF at 1c needs AR ~115 or k ~70 | Sense charge from a ≤300 nm capacitor, or in-cell gain, or ≥5x less bitline capacitance | Materials + engineering | MARGIN, PIXEL, HOT-SIDE, AND, DIODE, CHARGE-RIVER |
| 2 | No manufacturable 3D cell | Break-even ~26 tiers (7-156); SK hynix 5 tiers at 56.1% yield | ≤0.012-0.02 µm² per tier, one hole etch, ≤0.2% killer defects per tier | Engineering | AND, PIXEL, DIODE, CHARGE-RIVER; CELL-WAFER as scale path |
| 3 | Leakage tail forces refresh | Tail ≤13 fA (64 ms); ~46 fJ per bit-refresh; 16-33% of idle power | Worst-case off-current ≤0.1 fA at 85-125 °C | Materials (oxides are close) | HOT-SIDE, AND, oxide cells; RAW-BER via coding |
| 4 | Litho-bound scaling, capital | 6F² at F ≈ 12-13 nm; 5-7 EUV layers ($825-1,155/wafer); depreciation ~55% of wafer cost | Density from structure, not wavelength | Engineering | AND, CELL-WAFER, LEAN |
| 5 | Data-movement energy | HBM 3-4 pJ/bit; 134-448 W per accelerator | Bits ≤100 µm from compute, ≤0.4 pJ/bit, cells that hold data at 85-125 °C | Engineering + thermal | HOT-SIDE, CHARGE-RIVER |
| 6 | HBM TSV tax | ~3x wafer per bit vs DDR5 | Vertical bandwidth without per-die TSVs | Engineering | HOT-SIDE |
| 7 | Periphery overhead | ~49% of the die | Periphery under the array at no area cost | Engineering | CELL-WAFER, HOT-SIDE carrier |
| 8 | Destructive read, overfetch | 128x overfetch; ~5.9 pJ per useful bit | Non-destructive or sub-page reads | Architecture + cell | Gain cells: HOT-SIDE, AND |
| 9 | Row hammer | Flips after ~0.5-1k activations [extrapolated] | No charge path from a toggling neighbour | Device physics | RAW-BER (controller RFM) |
| 10 | Voltage floor | Bitline ~1 V, wordline ~3 V | ≥50 mV signal at ≤0.4 V | Engineering | MARGIN, PIXEL (local gain) |

**A1's verdict.** "None of the ten bottlenecks is a physics wall." Bitline thermal noise (kT/C) is 0.38 mV against a 50 mV budget, and a bit is ~17,800 electrons [ESTIMATE]. Most bottlenecks trace to two causes:
- a passive capacitor read through a long bitline behind a leaky silicon switch;
- bits far from compute, read destructively in large pages.

---

## 5. How we searched

**Expert lenses first.** Five expert lenses wrote 101 seed cards: cell physics, materials, 3D process, architecture and first principles. A physics triage ([TRIAGE.md](research/phaseB/TRIAGE.md)) found 0 ideas dead on physics and 8 failed sub-claims. The seeds entered the pool as "Phase B lens".

**The creativity grid** ([config.json](research/ideas10k/config.json), [BRIEF.md](research/ideas10k/BRIEF.md)):
- **Grid:** 25 techniques × 10 facets = **250 cells**, 46 ideas each. The first half was free; the second half obeyed one forced constraint. That yielded 11,496 lexically unique ideas.
- **Top-up** ([topup/config.json](research/ideas10k/topup/config.json)): 6 new techniques in **30 cells** of 42 ideas. Each cell carried a list of mechanism families to avoid, taken from screener theme tags. That yielded 1,260 ideas.
- **Total:** 11,496 + 1,260 + 101 = **12,857** ideas under **32 technique labels**.

**The techniques:**
- SCAMPER-Substitute, -Combine, -Adapt, -Magnify/Minify, -Eliminate, -Reverse/Rearrange;
- TRIZ inventive principles; Biomimicry; Cross-domain analogy; Forgotten-technology revival; Assumption inversion; First principles;
- Random stimulus / forced connection; Morphological box (Zwicky); Provocation (de Bono "Po"); Reverse brainstorming; Perspective shift / personas;
- Extreme users and edge cases; Scale and time shifting; Failure mining; Physical-effects walk; Periodic-table walk; Manufacturing analogies;
- Wishful thinking / ideal final result; Scarcity and constraint as engine;
- top-up: Constraint stacking; Distant-field transplant; Extremophiles, minerals and Earth systems; Time travel; Paradox as feature; Measurement-first invention;
- plus "Phase B lens".

**The facets:** bit storage element; access device, leakage and refresh; sensing and periphery; array architecture and 3D integration; materials and resource intensity; manufacturing, lithography and capital intensity; system architecture (need less DRAM); interface, packaging and data movement; reliability, ECC and error tolerance; supply, industry and strategy.

**The 25 constraints** included: no EUV; no storage capacitor; ≤400 °C; no helium; Earth-abundant elements only; university-nanofab buildable; zero refresh power; 125 °C for 10 years; no PFAS; 1990s tools; roll-to-roll; U.S.-only; tolerate 1% raw bit errors; 100x cheaper per GB.

**Removing duplicates, in two passes.**
1. **Lexical** ([ideas_dedup.py](research/tools/ideas_dedup.py)). Exact titles, then MinHash LSH on word 2-shingles (128 permutations, 32 bands × 4 rows), verified at Jaccard ≥0.5. It removed 4 exact duplicates and 0 near-duplicates from 12,861 raw ideas.
2. **Same mechanism** ([screen_tools.py](research/tools/screen_tools.py)). Screening batches were grouped by facet and sorted by a MinHash key so similar ideas sat together. Screeners flagged **2,332** ideas that shared a core mechanism with an earlier one, leaving **10,525 distinct ideas**.

**The rubric** ([SCREEN_RUBRIC.md](research/ideas10k/SCREEN_RUBRIC.md)). Every idea was scored 1-5 on four scales, in 137 batches of ~100:
- **P**, physics plausibility: 1 = violates physics; 5 = engineering only.
- **S**, step change if it works: 1 = <10% or a niche; 5 = ≥10x on a mission axis.
- **N**, novelty: 1 = widely pursued; 5 = not seen before.
- **D**, demo-ability with $1M in 24 months: 1 = needs a fab or a decade; 5 = a convincing demo fits.

**From scores to the Stage 2 pool.**
- **Composite** = S×1.0 + P×0.8 + N×0.6 + D×0.6, scaled to 0-100.
- **Shortlist:** the top ~300 by composite, with ≥20 per facet: 301.
- **Breakthrough ranking:** (1.2·S + 1.0·N + 0.5·P + 0.3·D)/15 added 107 ideas not on the shortlist, giving a 408-idea pool.
- **Top-up:** the 24 best top-up ideas joined, for **432** in total.

**Stage 2** ([STAGE2_REPORT.md](research/ideas10k/stage2/STAGE2_REPORT.md)). A physics critic and an innovation critic each re-scored every idea and gave a verdict.
- **Consensus** = the mean over both lenses of (1.2·S2 + 1.0·N2 + 0.7·P2 + 0.5·D2)/17.
- **ADVANCE** needed both critics to say ADVANCE, or one ADVANCE and one HOLD with consensus ≥70.
- **DROP** if both said DROP, or the physics critic said DROP with P2 ≤2.

**Stage 3 and after.**
- **Inventor teams.** Two teams combined the 30 ADVANCE ideas independently: a device team (10 concepts) and a system team (11). A chief-scientist reconciliation made 6 merges and 1 absorption and cut 4, leaving 10 concepts. They use 24 of the 30 ADVANCE ideas ([IDEAS_INDEX.md](IDEAS_INDEX.md)).
- **Models and dossiers.** Each concept got a model (`models/<slug>.py`) and a dossier (`dossiers/<slug>.md`).
- **Red team.** Four attacker lenses raised 181 objections: device physicist 45, process veteran 44, circuit designer 46, industry strategist 46. Of these, 3 were FATAL, 123 MAJOR and 55 MINOR. All were answered:
  - 101 mitigated;
  - 72 downgraded;
  - 6 kills of 5 named sub-claims;
  - 2 refuted.
- **Judges.** Three independent judges made the picks.

**The funnel.**

| Step | Count | Source |
|---|---|---|
| Ideas generated (grid 11,496 + top-up 1,260 + Phase B 101) | 12,857 | [ideas_10k.jsonl](research/ideas10k/ideas_10k.jsonl) |
| Screened on P, S, N, D | 12,857 | [scored_ideas.jsonl](research/ideas10k/screen/scored_ideas.jsonl) |
| Same-mechanism duplicates → distinct ideas | 2,332 → 10,525 | same |
| Shortlist → Stage 2 pool | 301 → 408 | [SCREEN_REPORT.md](research/ideas10k/screen/SCREEN_REPORT.md), [stage2_pool.jsonl](research/ideas10k/screen/stage2_pool.jsonl) |
| + best top-up ideas → critiqued | +24 → 432 | [best24.json](research/ideas10k/topup/best24.json), [stage2_results.jsonl](research/ideas10k/stage2/stage2_results.jsonl) |
| ADVANCE / HOLD / DROP | 30 / 132 / 270 | same |
| Inventor concepts → final concepts | 21 → 10 | [FINAL_CONCEPTS.json](research/stage3/FINAL_CONCEPTS.json) |
| Red-team objections answered | 181 of 181 | [research/redteam/](research/redteam/), [REDTEAM.md](REDTEAM.md) |
| Concepts killed / downgraded | 0 / 10 | `responses_<slug>.json` |
| Unanimous picks | 3 | [decision.json](research/stage3/decision.json) |

---

## 6. The 10 concepts that came out

The rank and EV (S × P × D) are pre-red-team values from [FINAL_CONCEPTS.md](research/stage3/FINAL_CONCEPTS.md). The rest comes from each dossier's section 11: claims are [MODEL] and costs [ESTIMATE]. **Every final status is DOWNGRADED.**

| Rank (EV) | Concept | Mechanism | Headline after red team | Killed or withdrawn inside it | Decisive experiment |
|---|---|---|---|---|---|
| 1 (75) | [MARGIN STACK](dossiers/margin-stack.md) | A gain transistor per 64 cells plus double sampling and an ECC budget, so oxide-access cells need far less capacitor | Capacitor 5.42 → 0.5 fF (10.8x shorter): ~10x less deep capacitor etch. But +9-25% $/bit and −11% density. Owner re-score EV 24 | Withdrawn: the 17-40x stretch, the 28x refresh claim | $563k; month 17 |
| 2 (64) | [HOT-SIDE MEMORY](dossiers/hot-side-memory.md) | Oxide gain-cell tiers in the backside-power carrier wafer | ~10x energy/bit vs HBM; ~90 W per GPU; refresh ~225x rarer than Si; $4.6-12/GB | No kill. "Refresh-free" became "refresh-light" | ~$240k; month 11 |
| 3 (60) | [AND-STACK](dossiers/and-stack.md) | One hole etch, 3D-NAND style; a 2-bit capacitorless oxide cell per tier | 5.9x 1-beta at 64 tiers; 2.3x bits/$ vs 2026, 1.1-1.4x vs 2032 | **Killed:** single-film closure (topologically impossible) | ~$0.4M; month 14 |
| 4 (60) | [RAW-BER CONTRACT](dossiers/raw-ber-contract.md) | An error contract and controller, so weak bits and slow refresh can ship | ~9x refresh energy on DDR5 (6.1-20x); ~13x on retired DDR4; ~$3.9 per module over 5 yr | **Killed:** the per-read sense-amp "unsure" flag | $124k; month 6 |
| 5 (48) | [PIXEL-STACK](dossiers/pixel-stack.md) | Read a 3D 1T1C stack like an image sensor, with an oxide amp tier every 16 tiers | ~4.6x 1-beta at 64 tiers; ~1.5x vs incumbent 3D at equal tiers; bits/$ ~parity | Dropped: 2.5x bits/$; "removes Smart-Cut" | ~$390k; month 9 |
| 6 (45) | [DIODE-TOWER](dossiers/diode-tower.md) | Per-tier oxide Schottky diodes steer 16-64 capacitor tiers onto one pillar | 3.9x 1-beta at 64 tiers; ~1.8x bits/$; EV ~16; P(pass) ~5-10% | AgOx anode demoted (not integrable); ferroelectric fallback dropped | ~$260k; month 7 |
| 7 (40) | [CHARGE-RIVER](dossiers/charge-river.md) | Charge packets march through vertical oxide CCD strings, scheduled for LLM streaming | ~2.5x density; ~158x lower standby power; cost ~parity ($1.74/GB) | **Killed:** the cost-per-bit leg | Gate 1, month 10 |
| 8 (40) | [LEAN ARRAY MODULE](dossiers/lean-array-module.md) | Hydrogen instead of helium for wafer backside cooling | Backside helium 7.5 L/wafer → 0: ~3% (1-11%) of DRAM's helium at ~1.0x $/bit; EV 30 | **Killed:** AAO capacitor mold at the 35 nm pitch | $145k rig, month 8 |
| 9 (36) | [CELL-WAFER FOUNDRY](dossiers/cell-wafer-foundry.md) | Litho-light oxide cell wafers bonded to U.S. foundry periphery | 3.6x less new-fab capex per GB/month, 0.62x DDR5 $/GB, 0 EUV; the split itself adds ~1.5x | Merchant leg demoted to optional | $795k; months 14 and 22 |
| 10 (30) | [AI MEMORY DIET](dossiers/ai-memory-diet.md) | Stream chat KV caches (an AI model's per-conversation working memory) between HBM and flash; drop the host-DRAM tier for human chat (agent traffic keeps one) | 1.40x fewer DRAM GB per human-chat conversation (1.17x wafer terms); EV 15 | **Killed:** one shared KV latent for all layers | ~$205k; month 12 |

**After the red team the order changed.** The operator re-scored S × P × D:

| Concept | Re-score |
|---|---|
| HOT-SIDE | 48 |
| RAW-BER | 48 |
| PIXEL | 36 |
| CHARGE-RIVER | 30 |
| LEAN | 30 |
| MARGIN | 24 |
| AND | 24 |
| DIODE | 16 |
| DIET | 15 |
| CELL-WAFER | ~12 |

The pre-red-team rank 1, MARGIN STACK, fell furthest.

---

## 7. The three picks in depth

### 7.1 BEST BET: HOT-SIDE MEMORY

**Mechanism.**
- **Today.** An accelerator's HBM sits beside the processor. Each bit crosses a high-speed port, millimetres of interposer and vertical vias (TSVs), at ~3.5 pJ/bit. Memory cannot sit on top, because silicon DRAM at 105 °C must refresh about every 16 ms.
- **Two recent changes.**
  - Backside power (BSPDN; Intel 18A, TSMC A16) bonds each backside-power logic wafer to a blank carrier wafer.
  - Oxide gain cells hold charge behind an IGZO (indium-gallium-zinc oxide) transistor that leaks zeptoamps.
- **The idea.** Make the carrier a 28 nm-class CMOS wafer with 8-16 oxide tiers built below 400 °C. Bond it face to face to the processor, so data moves about a micrometre. Defects cost capacity, not a scrapped GPU.
- **What it is not.** It is a near tier for the hottest data, not an HBM replacement.

**Numbers** ([models/hot-side-memory.py](models/hot-side-memory.py), revised; [MODEL] unless tagged):

| Quantity | Value |
|---|---|
| Planning case, 16 tiers × 1 b | 0.392 Gb/mm² (0.88x 1-beta); 78 GB per GPU (157 GB if 2 b works) |
| Typical retention | ~103 s at 105 °C, extrapolated from imec's >200 s at 95 °C [REPORTED] |
| Weakest-cell (1e-4) refresh | 1 b: every 3.6 s at 105 °C, 1.4 s at 125 °C, ~225x rarer than Si |
| Leakage ceilings at the tail | 22.5 aA (1 b), 7.5 aA (2 b); planning tail 12.5 aA at 125 °C |
| Energy delivered at 3 mm | 0.374 vs 3.95 pJ/bit for HBM: ~11x (5.5x at random placement, 15x at 1 mm) |
| Watts saved per GPU | 48 W (8 × 1 b), ~92 W (16 × 1 b), 169 W (16 × 2 b) |
| Cost | $4.6-12/GB incremental; ~$1,500 of 5-year value per GPU [ESTIMATE] |

**Why the judges picked it.**
- **Physicist:** "Its step change comes from geometry, not from heroic cell physics, so it is the one that survived every red-team correction." It pays at 1 bit per cell and needs no ≥32-tier yield.
- **Investor:** P(Gate A+ at 1 b) ~0.5-0.6 and P(fundable Series A) ~0.15, the best in the set [ESTIMATE].
- **Operator:** it ties RAW-BER at 48 and wins, because RAW-BER is worth ~$3.9 per module and can be copied in firmware.
- **Agreed weaknesses:**
  - it is not a cost step;
  - the 2-bit capacity is unmeasured;
  - foundries own the carrier slot, so the raise needs a named backside-power partner.

**Decisive experiment: Gate A+, month 11 (2027-11-30).**
- **Arrays.** Vertical 2T0C arrays, read gate ≥0.01 µm², built at Purdue Birck or Georgia Tech IEN.
- **Splits:**
  - channel: IGZO, In-poor IGZO, IGO, Ga-free ZTO;
  - write gate: single vs series;
  - hold bias: −0.5 vs −0.7 V;
  - encapsulation: hydrogen-lean vs PECVD.
- **Process.** Each split sees the post-bond heat sequence and a real fusion bond, labelled with heavy water (D₂O) so SIMS can trace the bond's hydrogen.
- **Measurements on ≥1e5 cells per split:**
  - drift at 85/105/125 °C;
  - write at one temperature, read at another (±30 K);
  - RTN at 1 µs to 1 s;
  - the measured 1e-4 retention quantile;
  - threshold shift (ΔVt) of the top tier after bonding.
- **Pass, 1 b:** drift ≤75 mV, RTN ≤100 mV, tail ≤22.5 aA at 125 °C, bonded ΔVt ≤10 mV.
- **Pass, 2 b:** drift ≤20 mV in a ≥600 mV window, cross-temperature ≤10 mV, RTN ≤30 mV, tail ≤7.5 aA at 105 °C.

**Cost and timeline** [ESTIMATE].
- Gate A+ costs ~$240k: coupons $130k, real-bond split $25k, bench $85k.
- The standalone plan is $1.00M over 24 months, with month 0 = January 2027:
  - Gate B (2028-06-30): 2 tiers on finished logic, ring-oscillator (RO) speed shift ≤1% and transistor threshold (Vt) shift ≤10 mV after 1,000 h at 105 °C.
  - Gate C (2028-10-31): carrier emulation plus void and contamination checks.
- In the portfolio, Gate A+ rides the shared lot (~$150-175k by the judges' counts), and Gate B moves to a sky130 carrier.

**Kills and revivals** (dossier §9):

| Month | Kill if… | Revival |
|---|---|---|
| M11 | Every split, incl. the real bond, has drift >75 mV at 1 s/105 °C, still >75 mV at a 100 ms hold (kills capacity) | Hydrogen barrier plus In-poor or ZTO split at ≤25 mV |
| M11 | Every split has 1e-4 retention <1 s at 105 °C (tail >22.5 aA), incl. series gate and −0.7 V hold (kills the concept) | Write-FET σVt ≤30 mV, or a measured tail ≤22.5 aA |
| M11 | The RTN 1e-4 quantile is >100 mV in every split (kills capacity) | Larger read gate or lower-trap gate stack |
| M11 | Window <600 mV, cross-T >10 mV, RTN >30 mV or tail >7.5 aA (drop 2 b) | Continue at 1 b, the planning case |
| M18 | RO shift >1% or Vt >10 mV, unrecoverable | Carrier-only from then on |
| M22 | Drift worsens >50% after carrier emulation (kills the carrier host); >2 nm predicted distortion or In/Ga/Zn >1e10 at/cm² (kills bond-first) | None stated for the carrier host; bond-first revives with stress-neutral tiers at a partner |

**Red team.** 19 objections: 13 mitigated, 6 downgraded, 0 kills ([responses](research/redteam/responses_hot-side-memory.json)).
- **PROC-01 (FATAL): carrier bow wrecks backside lithography overlay.** Mitigated with "carrier-last": the memory wafer bonds after backside processing.
- **DEV-01: the leakage tail is 91x the typical cell, not 3x.** Downgraded. A series write gate (top-up idea I-12627) and a −0.7 V hold give a 25x planning value, and "refresh-free" becomes "refresh-light".
- **DEV-02 (RTN) and DEV-03 (bond-interface hydrogen).** Mitigated: half the error budget is reserved for RTN, and a real D₂O bond moved into Gate A.
- **CIRC-02: cross-temperature reads.** Downgraded: the planning case moves to 1 b.
- **CIRC-03 / IND-01: traffic share tracks capacity.** Downgraded: ~190 W became ~90 W per GPU.
- **PROC-02/03: cost per GB.** Downgraded: $1.36-3.55 became $4.6-12/GB.

### 7.2 FASTEST PROOF: RAW-BER CONTRACT

**Mechanism.**
- **Today's rule.** Every DRAM bit must read right on its own. So all bits refresh every 64 ms (32 ms on DDR5) because a few in a billion leak fast, and each holds charge ~7 noise widths (σ) above the sense amp's error.
- **What flash did.** NAND solved the same problem with a controller and a strong code.
- **The contract.** Publish a raw bit-error-rate (BER) contract: ≤1 wrong bit in 10,000, in a stated error pattern. A mature-node CXL controller keeps it, by decoding, scrubbing, scheduling refresh by temperature and guarding against row hammer.
- **Now and later.** On today's DDR5 it stretches refresh. Later, new cells are designed to the contract instead of to 7σ.

**Numbers** ([models/raw-ber-contract.py](models/raw-ber-contract.py), revised; [MODEL] unless tagged):

| Quantity | Value |
|---|---|
| Margin at raw BER 1e-4 | 3.72σ instead of 7σ: 50 → 26.6 mV (1.88x); capacitor 5.42 → 2.68 fF |
| DDR5, chipkill, 85 °C | Safe interval 285 ms = 8.9x the 32 ms spec; 194 ms pessimistic (~6x); 2.9x with a chip dead; 35x at 65 °C |
| Retired DDR4, chipkill, 85 °C | 837 ms = 13.1x of 64 ms (7.8x pessimistic) |
| Module refresh power, DDR5 64 GB | 0.98 → 0.11 W; ~$3.94 per module over 5 years [ESTIMATE] |

**Why the judges picked it.** It is the only decisive experiment with no fabrication and no new physics, and it starts in week 1. Its census of error clustering and VRT tells whether the 1.88x margin holds on real silicon. MARGIN STACK, PIXEL-STACK, HOT-SIDE and AND-STACK's 2-bit mode all bank on that margin. The judges agree the stand-alone prize is small: "the proof and the instrument, not the company" (physicist).

**Decisive experiment: Phase 1, months 0-6.**
- **Retired DDR4:** 150 modules screened over ≥30 lots per vendor; 60 deep-mapped at 0.128-4 s × 45/65/85 °C.
- **DDR5:** ≥24 RDIMMs on 2 open Antmicro testers, inverting on-die-ECC event maps to raw BER.
- **VRT and RTN:** VRT coincidence over 1,000 h on 20 modules, plus a dwell-time (RTN) spectrum.
- **Census, servo, hammer:** a census of every multi-bit event; a 1-hour grade checked against 1,000 h; row-hammer tests at relaxed refresh with controller refresh management (RFM).
- **GO** needs all three:
  - interval ≥6x the window at 85 °C (DDR5 ≥0.19 s, DDR4 ≥0.38 s) and ≥24x at 65 °C;
  - multi-chip events ≤10%;
  - the grade holds on ≥95% of modules.

**Cost and timeline** [ESTIMATE]. ~$124k: 4 Bender stations $56k, DDR5 testers $20k, modules $24k, thermal $14k, server $10k. The judges budget $90-120k. The full 24-month plan ($946k, with CXL soaks) waits for the raise.

**Kills and revivals** (dossier §9).
- **M6, commodity product.** Kill if the chipkill interval incl. VRT is <4x the JEDEC window at 65 °C. *Revival:* an oxide or gain-cell array with a retention distribution measured to ≤1e-6 at 85 °C, ≥10x right of silicon. Or stacked write devices with tail correlation ρ ≤0.1, which takes the interval from 0.84 to 1.8 s [MODEL].
- **M6, codes.** Kill the binary BCH code if >0.4% of error bits arrive in ≥3-bit clusters, and both line codes if >10% of events span more than a byte. *Revival:* chip-symbol codes in a wider side band [UNVERIFIED-PK].
- **M6, DDR5.** Kill the DDR5 claim (keep retired DDR4) if its interval is <128 ms at 65 °C. *Revival:* vendor ECC-off maps under NDA.
- **On NO-GO.** Every cell model reverts from the 3.72σ budget toward 7σ.

**Red team.** 19 objections: 10 mitigated, 7 downgraded, 2 kills ([responses](research/redteam/responses_raw-ber-contract.json)).
- **CIRC-01/02: the "unsure" flag sees 50-150 ps of strobe skew against a 14-35 ps window, and even ideal flags cost more die than they save.** The flag leg is killed.
- **DEV-02 and CIRC-03: the 15x headline came from DDR4 data without chipkill.** Downgraded to ~9x on DDR5, with chipkill as the default.
- **PROC-01/02: DDR5 must be measured, and one fleet interval fails across lots.** Mitigated with a DDR5 leg and a per-module servo.
- **IND-01/03: value and 64Gb claims are small.** Downgraded to ~$3.9 per module, and 64Gb refresh-busy time 18% → 2% (~6-16 points after same-bank refresh).

### 7.3 MOONSHOT: AND-STACK

**Mechanism.**
- **3D NAND's trick.** NAND got cheap by depositing 100+ layers and drilling one field of holes; each layer costs a deposition, not a lithography step. But NAND cells sit in series (slow) and write through an insulator (wear).
- **AND-STACK keeps the trick.** At each floor, a tiny metal ring in the hole wall stores a few hundred electrons. It gates a 5 nm oxide film whose current, between two metal pillars, reads the bit without erasing it.
- **Two plates per floor.** A write plate charges the ring and seals it. A select plate turns the ring up for reading and silences the other 63 floors.
- **Parallel, 2 bits.** Cells are wired in parallel ("AND"), each holding one of four voltages.

**What the red team changed.** The original single-film cell cannot be wired: wherever the ring touches the film, it touches its own read channel. The redesign, a two-film "notched write pocket", needs three never-built process modules [SPECULATIVE]:
1. selective etch of the insulator inside a notch;
2. recess-fill-etch-back of an oxide semiconductor;
3. IGZO-safe replacement of the write plates.

**Numbers** ([models/and-stack.py](models/and-stack.py), revised; [MODEL] unless tagged):

| Quantity | Value |
|---|---|
| Geometry | 110 nm holes at 170 nm pitch; 64 tiers = 6.06 µm, aspect ratio 55 |
| Density | 64 × 2 b: 2.62 Gb/mm², 5.9x 1-beta (was 8.1x); 8.8x as a two-deck 96 × 2 b part |
| Cost | $0.65/GB: 2.3x bits/$ vs 2026 (2.2-2.6x); 1.1-1.4x vs 2032; break-even at 18 tiers (2 b) |
| Write-FET leakage tail at −3.0 V hold | ≤5 aA at 160 mV/decade, against a 17 aA budget |
| Refresh power at 1 s | ~25x lower than DDR5 |
| Odds | P(closure) ~20% [ESTIMATE]; investor: P(GO #1B) ~0.1-0.15, P(64-tier product) ~0.03-0.05 [ESTIMATE] |

**Why the judges picked it.**
- **Highest ceiling.** It is the only concept whose density comes from tier count, not lithography, on NAND tool sets with no EUV.
- **Persistence fits.** The physicist calls the risk "a process-integration problem with many knobs, which is exactly where persistence works".
- **Cheap to carry.** Its cell physics is the same oxide 2T0C the HOT-SIDE lot measures. Planar riders cost ~$15k in the operator's budget and $30-35k in the others.
- **Honest discounts.** Bits per dollar is only 1.1-1.4x vs 2032; NEO's NAND-process DRAM is ~3 years ahead; Macronix's 3D AND patents surround it.

**Decisive experiment.**
- **G0 TCAD device simulation (months 0-3, ~$35k).** A notch geometry with ≥9 decades of write-segment suppression at a −3.0 V hold, and coupling ratio (CR) ≥0.55.
- **GO #1A planar (month 9):**
  - CR ≥0.57 at σ ≤0.045 over ≥50 cells;
  - write-FET 1e-4 tail ≤17 aA on ≥1e4 devices at 85 °C;
  - 4 levels holding ≥1 s with ≤78 mV drift;
  - cross-temperature 2-bit BER ≤1e-4 at ±10 K;
  - ≤30 mV disturb.
- **GO #1B (month 14 in the dossier; 14-16 in the decision).** A 2-tier vertical coupon with 250 nm e-beam holes must show write-then-read with no ring-to-channel short, ring hold ≤100 aA at 85 °C, per-tier CR ≥0.57, and the notch contact imaged in TEM.

**Cost and timeline** [ESTIMATE]. ~$0.4M direct to GO #1B; the full plan is $970k, adding a 32-tier dummy etch coupon and a 4-tier stack by month 23. In the portfolio, the closure coupon ($100-120k) is released only if the month-9 tails pass.

**Kills and revivals** (dossier §9).
- **M3.** No notch geometry with ≥9 decades or CR ≥0.55 in TCAD: move to the per-tier fallback. *Revival:* a bottom select cap with no short path, or a 190 nm pitch.
- **M9.** CR <0.40 or σ >0.07: kill single-etch. A ring or write-FET tail >1 fA kills the DRAM-class claim; >100 aA drops 2 bits. *Revival:* a split at ≤17 aA, or a −3.5 V hold with a thicker write-gate dielectric.
- **M18 (2028-06-30).** No write-then-read closure on ≥2 tiers: kill single-etch. The per-tier fallback survives at ~1.0-1.6x bits/$, and the bits/$ claim dies. *Revival:* area-selective or self-aligned write-film confinement on a 2-tier coupon.
- **Pivots, not kills.** A blocking Macronix or NEO patent, or a failed dummy etch, leads to a JDA (joint development agreement) or a licence.

**Red team.** 20 objections: 1 refuted, 12 mitigated, 6 downgraded, 1 kill ([responses](research/redteam/responses_and-stack.json)).
- **PROC-01 (FATAL): no process gives write contact and read isolation in one hole.** The single-film leg is killed, the cell revived as the two-film pocket, and the closure coupon becomes the decisive gate.
- **CIRC-01: hold leakage.** Mitigated: idle-low select plates and a −3.0 V write-plate hold give a tail ≤5 aA.
- **DEV-02: refuted.** The objection's tail arithmetic was 1000x high.
- **PROC-02/03/04 and IND-03: stack, pitch and cost.** Downgraded: density 8.1x → 5.9x, bits/$ 3.8x → 2.3x (1.1-1.4x vs 2032).
- **IND-01/02/04: NEO and Macronix prior art; 64-tier manufacturability.** Claims narrowed to the notch module, bias scheme and group write. A 32-tier etch coupon was added, and 64 tiers became a raise milestone.

---

## 8. The $1M portfolio and gates

**Thesis** (decision.json): "One shared Oxide Tail Statistics lot answers the question seven concepts share, so the $1M funds evidence for most of the portfolio at once; the DRAM-error study sets the ECC budget every cell model uses; conditional spends (AND-stack closure coupon, Hot-Side Gate B) release only after gates pass."

**Facilities.**
- **First:** Purdue Birck Nanotechnology Center, as an external user: ≤400 °C oxide deposition and the Peide Ye group's oxide-transistor know-how.
- **Second source:** Georgia Tech IEN.
- **Carrier die:** SkyWater sky130 CMOS for the oxide-on-CMOS carrier.
- **Later:** MIT Lincoln Laboratory or NY CREATES for bonding.

**Hires.**
- **First recruit (co-founder): an oxide-semiconductor device-reliability physicist.** The skills are oxide-transistor drift (PBTI), hydrogen effects and RTN, attoamp leakage-tail metrology on ≥1e4-device arrays, and 2T0C experience. The judges name imec's IGZO 2T0C alumni, Purdue, Georgia Tech, Stanford, Intel Components Research and Micron as pools; they flag these as unverified training knowledge.
- **Recruiting reality** (operator). About $65k/yr will not buy a senior industry person. Target a senior PhD or postdoc. Pay in equity plus first authorship on the first ≥1e5-device oxide tails dataset.
- **Advisors and contractors.** An image-sensor readout designer as advisor. A DRAM Bender-experienced student as contractor; the non-device founder runs RAW-BER.

**Budget, three judges** (k$; decision.json `judge_budgets_k$`; each totals 1,000):

| Line | Physicist | Investor | Operator |
|---|---|---|---|
| Two founders, 24 months | 240 | 240 | 260 |
| IP: provisionals, freedom-to-operate (FTO), claim reading | 45 | 50 | 40 |
| Shared oxide lot, Purdue/GT | 220 | 280 (incl. bench 80, D₂O bond 35, sky130 25) | 210 |
| Bench, metrology, user facilities | 60 | (in the line above) | 60 |
| Lot riders: AND planar, diode anodes, CCDs, pixel caps | 100 | 70 | 80 |
| RAW-BER Phase 1 | 120 | 110 | 90 |
| sky130 carrier / HOT-SIDE Gate B | 85 | 70 (gated M11) | 80 |
| AND closure coupon (conditional) | 100 | 120 (gated M9) | 110 (incl. TCAD) |
| Overhead, legal, travel, contingency | 30 | 30 + 30 reserve | 30 + 40 |

**The shared lot carries:**
- 65k small source followers, with an on-coupon 15 ns sample-and-hold;
- ≥1e5-1e6 2T0C leakage cells, single vs series write gate;
- drift and cross-temperature structures;
- 1x/2x/4x hydrogen dose;
- a D₂O bond split;
- channels IGZO, In-poor IGZO, IGO and Ga-free ZTO/In₂O₃;
- riders for AND, DIODE, CHARGE-RIVER (only if imec's paper passes) and PIXEL.

**Gate schedule.** decision.json has no gate list, so this table uses the physicist judge's gates (the most detailed set), with the others' additions marked. Month 0 = January 2027.

| Month | Gate | Pass / kill line | What passing buys |
|---|---|---|---|
| M3 | Desk | imec CCD efficiency definition read; patent claims read; lot reticle taped. Investor: benches reproduce published DDR4 and IGZO retention within 2x. Operator: AND TCAD ≥9 decades | Lot spend released; CCD rider kept or dropped |
| M6 | RAW-BER | GO ≥6x window at 85 °C, ≥24x at 65 °C, multi-chip ≤10%, grade holds ≥95%. NO-GO <4x at 65 °C: all cells re-planned at 7σ | The measured ECC budget for every cell; a publishable error atlas |
| M7 | DIODE-TOWER | Kill if every integrable anode leaks >928 aA at the 99.99th percentile at 85 °C | Keeps the two-terminal hedge |
| M9 | Portfolio gate (shared lot) | RTN at 15 ns: ≤20 mV GO for PIXEL 0.45 fF; ≤40-44 mV PIXEL 0.60 fF plan and MARGIN GO; >55 mV NO-GO for all source-follower reads. Leakage: ≤22.5 aA at 125 °C (HOT-SIDE); write-FET ≤17 aA (AND); aged 2e-5 quantile ≤586 aA (MARGIN) | The remaining ~$270k goes to the cells that pass; the AND coupon releases only if the write-FET tail is ≤100 aA |
| M10 | CHARGE-RIVER | Transfer efficiency ≥0.9973 with decision feedback at ≥150 MT/s, 25 and 85 °C; buried channel ≥3x better | Else parked as paper or grant work |
| M11 | HOT-SIDE Gate A+ | Section 7.1 pass lines | Gate B released; backside-power partner talks open (the investor files the bond-hydrogen and cross-temperature provisionals here; the dossier and operator file them in Q1 2027) |
| M12 | Lead selection (operator) | ≥70% of remaining cash to the lead: HOT-SIDE if A+ passes, PIXEL if only it passes | Focus |
| M14-16 | AND GO #1B | Section 7.3; hard stop for single-etch at M18 | JDA talks with NAND makers |
| M18 | Demo, raise trigger | Oxide tiers on finished CMOS: RO ≤1%, Vt ≤10 mV after 1,000 h at 105 °C; ≤0.9 pJ/bit at the port; a named backside-power contact | Raise $10-15M (physicist); the operator's raise gate is M22-24 at $10-50M |

**If nothing passes** (investor): "Neither means no raise: sell or license the atlas data and IP and return capital." DIODE-TOWER, CHARGE-RIVER, LEAN, CELL-WAFER and AI MEMORY DIET get no seed cash beyond the shared splits. They run as grant, JDA or partner legs.

---

## 9. First 90 days for the BEST BET

**Dates.** The dossiers assume money at month 0 = January 2027. The Monday action is today, Monday 2026-11-02.
- Weeks 1-8 run on ~$0, following the investor's pre-M0 list.
- Weeks 9-13 are month 0.
- If the seed closes earlier, slide the funded weeks left.

The plan comes from the [HOT-SIDE dossier](dossiers/hot-side-memory.md) §5-6 and the judges' sequences.

**One rule.** File the provisionals before any disclosure (operator). So the Tail Spec lists test structures and pass lines only, not the carrier architecture or the cross-temperature scheme.

| When | Actions |
|---|---|
| **Day 1 (Monday action)** | Write the one-page Oxide Tail Spec (≤2 h). Email it to Purdue Birck (Ye group) and Georgia Tech IEN (Datta, Khan, Yu groups). Ask whether they hold per-device leakage/RTN data on ≥1e4 devices they would share under NDA, and for a quote on two planar lots. Submit the Birck external-user application the same morning |
| Weeks 1-2 | Read the claims of US 12,666,958 and US 2025/0167193 before filing anything. Read imec IEDM 2024 paper 37-6 (it sets CHARGE-RIVER's odds for free). Start the co-founder search; send the spec to the top 3 candidates |
| Weeks 3-4 | Confirm Ga-free channels in the spec (China's Ga export-ban suspension ends 2026-11-27). Line up SIMS (secondary-ion mass spectrometry) time at a DOE nanoscience center and an Argonne user proposal |
| Weeks 5-6 | Draft provisional 1, bond-interface hydrogen control with D₂O qualification, and provisional 2, cross-temperature multi-level cells |
| Weeks 7-8 | Design the trace study: bytes moved vs bytes resident on dense and mixture-of-experts (MoE) decode traces. Pass: ≥80% of reads within 1-2 mm of the GPU core cluster (SM) that uses them. Start the carrier floorplan (sense amps and drivers per mm²) |
| Weeks 9-10 (M0) | Incorporate; file both provisionals; sign the Birck and IEN agreements; order the bench (analyzers, dual-zone hot chuck, FPGA fast-read RTN capture). The systems founder orders DRAM Bender rigs and starts RAW-BER |
| Weeks 11-12 | Lay out the shared reticle (section 8 list). Book a SkyWater sky130 shuttle for the oxide-on-CMOS carrier |
| Week 13 | Check toward the M3 gate: the bench reproduces published IGZO 2T0C retention within 2x; the reticle is on track to tape by M3; the trace study shows whether ≥50% of bytes come from ≤30% of resident bytes (if not, plan on the capacity-indexed ~90 W) |

After that, per the dossier: coupon lots in months 2-11 and Gate A+ on 2027-11-30.

---

## 10. What the creativity techniques taught us

From [TECHNIQUE_PERFORMANCE.md](research/stage3/TECHNIQUE_PERFORMANCE.md), cross-checked against [IDEAS_INDEX.md](IDEAS_INDEX.md). Grid techniques had ~460 ideas each, top-up techniques 210, and Phase B 101. TECHNIQUE_PERFORMANCE counts only ideas a concept cites by direct id. IDEAS_INDEX also maps Phase B triage ids (N-xx) back to their seed cards, which changes only the Phase B count (8 direct, 22 mapped).

| Technique | S≥4 | N≥4 | Reached Stage 2 | ADVANCE | Ideas in final concepts |
|---|---|---|---|---|---|
| Wishful thinking / ideal final result | 8.5% | 9.4% | 22 | 6 | 7 |
| Phase B lens (expert seeds) | 9.9% | 21.8% | 22 | 5 | 8 direct; 22 mapped |
| Failure mining | 8.7% | 19.1% | 30 | 3 | 3 |
| Assumption inversion | 6.3% | 9.6% | 25 | 2 | 5 |
| Scarcity and constraint as engine | 3.0% | 10.0% | 13 | 1 | 4 |
| First principles | 6.7% | 11.3% | 21 | 0 | 2 |
| Physical-effects walk | 4.1% | 24.1% | 6 | 0 | 0 |
| Time travel (top-up) | 2.9% | 25.2% | 7 | 0 | 0 |
| Paradox as feature (top-up) | 0.0% | 21.0% | 9 | 0 | 0 |

**Lessons.**
1. **"Imagine the ideal result" and "mine past failures" won.** Wishful thinking had the most ADVANCEs (6). Failure mining had the best S≥4 rate of any grid technique (8.7%) and the most Stage 2 entries (30).
2. **Expert seeds punched far above their weight.** The Phase B seeds were under 1% of the pool but produced 5 ADVANCEs and 22 of the 68 ideas the final concepts cite (8 by direct id, 14 more through Phase B triage ids).
3. **Novelty alone did not survive.** The four highest-novelty grid and top-up techniques (21-25% N≥4) gave one ADVANCE between them. 15 of 32 techniques gave none, including all six top-up techniques.
4. **The top-up still mattered later.**
   - I-12627 (Paradox as feature: two series write transistors) became HOT-SIDE's fix for the leakage tail.
   - I-12302 (Time travel: plate-strip sensing) became CELL-WAFER FOUNDRY's 1T1C revival path.
   - The exclusion lists cut duplication: 5.7% of top-up ideas were flagged as duplicates (72 of 1,260), against 19.6% of grid ideas (2,257 of 11,496), computed from scored_ideas.jsonl.
5. **Constraints raised claimed step size, not survival.** Re-checked from the data:

| Group | Ideas | S≥4 | Reached Stage 2 | ADVANCE (rate among reviewed) |
|---|---|---|---|---|
| Constrained half | 6,378 | 274 (4.3%) | 240 | 12 (5.0%) |
| Free half, incl. 101 Phase B seeds (as in TECHNIQUE_PERFORMANCE) | 6,479 | 173 (2.7%) | 192 | 18 (9.4%) |
| Free half, grid and top-up only | 6,378 | 163 (2.6%) | 170 | 13 (7.6%) |

   The "12 vs 18" gap depends on counting the expert Phase B seeds as "free". Without them it is 12 vs 13, a near tie. The robust finding is the rate: constraints push screeners toward bold step claims that critics then cut.

6. **What fed the final 10.**
   - Phase B lens 22 (8 by direct id); Wishful thinking 7; Assumption inversion 5; Scarcity 4.
   - 3 each: Failure mining, SCAMPER-Combine, Perspective shift, Forgotten-technology revival.
   - 2 each: SCAMPER-Magnify/Minify, -Adapt, -Substitute, First principles, Random stimulus.
   - 1 each: Provocation, Scale and time shifting, Reverse brainstorming, TRIZ, Biomimicry, SCAMPER-Reverse, Manufacturing analogies, Extreme users.
   - None: Cross-domain analogy, Physical-effects walk, SCAMPER-Eliminate, Morphological box, Periodic-table walk, and all six top-up techniques.

---

## 11. What died, and what would revive it

No concept died on physics. Five named sub-claims died (six kill dispositions; two hit the same RAW-BER leg).

| Concept | Killed sub-claim | Physics reason | Revival condition |
|---|---|---|---|
| AND-STACK | Single-film write/read closure | Topologically impossible: in one round hole the ring can touch the film only beside its own read channel, so a read shorts it | The two-film notched pocket ([SPECULATIVE], P ~20%); for single-etch, self-aligned write-film confinement on a 2-tier coupon |
| RAW-BER | Per-read "unsure" sense-amp flag | 14-35 ps of latch time vs 50-150 ps of strobe skew; even ideal flags net −2.2% to −0.2% of die | Flag-window σ ≤1.5 mV over ≥1k sense amps at 85 °C without trim, plus a positive measured ledger |
| CHARGE-RIVER | Cost per bit | ~$25 per plate pair gives $1.74/GB (DDR5 $1.48/GB), i.e. 0.85x DDR5's bits per dollar | ≤$12 per plate pair and staircase-free contacts (≥1.6x) |
| LEAN ARRAY | AAO capacitor mold at 35 nm pitch | A 5.6 nm core at aspect ratio ~450 after the dielectric and electrode; no plausible fill | TEM-verified fill of ≥2 µm pores at ≤36 nm pitch, ≥5 fF per pore |
| AI MEMORY DIET | One KV latent shared by all layers | Every layer re-reads the whole latent: 26.7x more reads per decode step, ~3 active sessions per GPU instead of 89 | None in that form; per-layer latents avoid it but are prior art |

**Claims withdrawn through downgrades:**
- HOT-SIDE "refresh-free";
- MARGIN STACK's 17-40x stretch and 28x refresh;
- PIXEL-STACK's 2.5x bits/$;
- DIODE-TOWER's AgOx anodes and ferroelectric fallback;
- LEAN's ZTO leg;
- CELL-WAFER's merchant leg;
- AI MEMORY DIET's 4.5x headline.

**Strong concepts cut before the dossiers** ([FINAL_CONCEPTS.md](research/stage3/FINAL_CONCEPTS.md); not physics kills):

| Concept | Promote if |
|---|---|
| Panel memory ("memory by the square metre") | ≤0.1 killer defects/cm² per tier at ≤0.3 µm imprint on ≥200 mm glass, at ≤$50/m² per tier-pass |
| Second-Life Bits | Recertified cost ≤$3/GB at ≥70% yield, with the retention fingerprint stable over 3 months |
| Racetrack in the capacitor hole | Shift-error rate ≤1e-9 per step in ≤30 nm wires |
| Click-RAM (nanoribbon switch) | ≥1e12 snap cycles without stiction, ≤10% switching-voltage spread |

**What persistence can and cannot beat** (the judges).
- **It can beat** integration and process problems: notch modules, bond warp, hydrogen budgets, layout, yield. They have many knobs. Every one of the 181 objections got a priced design-around.
- **It cannot beat** an oxide trap's emission time, the shape of an RTN tail, a topological impossibility, or the absence of an integrable ≥1.0 eV oxide Schottky barrier. Those must be measured, or a different material found.

So: measure the oxide tails first, then build the cell they allow.

---

## 12. Honest limits

1. **Snippet-grade evidence.**
   - Phase A agents had 25-30 web searches each and no page fetches.
   - A3 found IEEE Xplore, arXiv and TrendForce unreachable. The sister study's log (`../ram-venture/ASSUMPTIONS.md`) records 403s for trendforce.com, sec.gov and investors.micron.com, and proxy 403 or DNS failures for en.wikipedia.org (entries A-A3-1 and A-p1-ip-1).
   - Most papers were seen only via snippets or press releases, and patent claims were not read.
   - This report made no web searches.
2. **First-order models.** The models are stdlib arithmetic. HOT-SIDE's thermal figure is a 1-D upper bound. Its hot retention extrapolates imec's 95 °C data, because no 125 °C oxide 2T0C data was found. Costs are [ESTIMATE].
3. **No lab data.** Every pass line sits in a 1e-4 to 2e-5 tail that no file on disk measures. With heavy tails, the operator expects the portfolio to shrink to RAW-BER plus a 1-bit HOT-SIDE tier.
4. **Leftover duplicates.**
   - MinHash caught only lexical repeats.
   - Screeners compared ideas only within ~100-idea facet batches, so cross-facet cousins survive. The screening report lists "dimm reuse market" (21), "dimm reuse cxl" (14) and "dimm reuse via cxl" (7) as separate themes.
   - So "10,525 distinct" overstates mechanism diversity.
5. **LLM throughout.** Ideas, scores, critiques, objections and verdicts all came from language-model agents. The judges were independent of each other but read the same dossiers, so unanimity is not independent evidence.
6. **Late prior art.**
   - imec's planar IGZO CCD (>98% transfer efficiency at ~4-6 MHz, definition unread) caps CHARGE-RIVER.
   - UniIC/XMC SeDRAM (wafer-on-wafer DRAM on logic, 0.88 pJ/bit, in production) and a 2022 Chip Scale Review article on memory as the carrier bar broad HOT-SIDE claims.
   - Taalas's mask-ROM weights (AMD acquiring) compete for static-weight traffic.
   - NEO and Macronix narrow AND-STACK; SEL narrows MARGIN STACK.
7. **Stale ranks; assumed dates.** The FINAL_CONCEPTS ranks predate the red team. Plans assume month 0 = January 2027. Recruiting names are unverified training knowledge.

---

## 13. How to reproduce

The language-model steps cannot be re-run by script. The scripts merge, check and aggregate their outputs, and run the models. **Most overwrite their outputs, so work on a copy.** Run from `dram-moonshot/`:

```bash
python3 research/tools/ideas_dedup.py --thresh 0.5 --target 10000   # merge raw cells, exact + MinHash dedup -> ideas_10k.jsonl, stats.json
python3 research/tools/screen_tools.py batch                        # facet-grouped, MinHash-ordered screening batches
python3 research/tools/screen_tools.py aggregate                    # scores -> scored_ideas, shortlist, SCREEN_REPORT.md
python3 research/tools/topup_prep.py                                # top-up cells and exclusion lists
python3 research/tools/stage2_aggregate.py                          # two-lens reviews -> stage2_results, STAGE2_REPORT.md
python3 research/tools/compile_redteam.py                           # REDTEAM.md; exits 1 if any objection lacks a response
python3 research/tools/build_ideas_index.py                         # IDEAS_INDEX.md
for s in margin-stack hot-side-memory and-stack raw-ber-contract pixel-stack diode-tower \
         charge-river lean-array-module cell-wafer-foundry ai-memory-diet; do python3 models/$s.py; done
python3 models/dram_cell_physics.py; for f in research/models/*.py; do python3 "$f"; done
```

All ten concept models, `dram_cell_physics.py` and the eight Phase A-C models exited 0 when run for this report.

**File map.**

| What | Where |
|---|---|
| Mission and rules | [MISSION.md](MISSION.md) |
| Decision, judges | [decision.json](research/stage3/decision.json); [physicist](research/stage3/judge_physicist.json), [investor](research/stage3/judge_investor.json), [operator](research/stage3/judge_operator.json) |
| Dossiers (section 11 = red-team outcome) | [dossiers/](dossiers/) |
| Models and outputs | [models/](models/); `research/stage3/<slug>_model_output.md` |
| Final concepts (pre-red-team), lineage | [FINAL_CONCEPTS.md](research/stage3/FINAL_CONCEPTS.md), [.json](research/stage3/FINAL_CONCEPTS.json) |
| Red team | [research/redteam/](research/redteam/), [REDTEAM.md](REDTEAM.md) |
| Phase A | [A1](research/phaseA/A1_scaling_limits.md), [A2](research/phaseA/A2_materials_resources.md), [A3](research/phaseA/A3_research_frontier.md) |
| Phase B and triage | [research/phaseB/](research/phaseB/) |
| Idea pool, screening, Stage 2 | [research/ideas10k/](research/ideas10k/); [SCREEN_REPORT.md](research/ideas10k/screen/SCREEN_REPORT.md); [STAGE2_REPORT.md](research/ideas10k/stage2/STAGE2_REPORT.md) |
| Technique performance; idea index | [TECHNIQUE_PERFORMANCE.md](research/stage3/TECHNIQUE_PERFORMANCE.md); [IDEAS_INDEX.md](IDEAS_INDEX.md) |
| Sources, assumptions, tools | [research/sources/](research/sources/), [research/assumptions/](research/assumptions/), [research/tools/](research/tools/) |
