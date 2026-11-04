# DRAM Moonshot

*An invention study: new ways to make DRAM-class working memory. As of 2026-11-02.*

## What this is

DRAM (dynamic random-access memory) is the working memory in every computer. This study asked what new ways of making it could give a step change in cost per bit, density, energy per bit, fab capital, scarce materials or U.S. manufacturability. It judged ideas as inventions, not businesses. It killed an idea only for physics, and every kill names what would revive it. The frame is a Thiel-Fellow-style team: $1M seed, two founders, a convincing demo in 18-24 months using shared wafer runs and university labs ([MISSION.md](MISSION.md)). The earlier business study of the same market is [../ram-venture/](../ram-venture/README.md).

## The answer in five bullets

From [DRAM_MOONSHOT_REPORT.md](DRAM_MOONSHOT_REPORT.md) section 1 and [decision.json](research/stage3/decision.json). Three judges (physicist, investor, operator) chose the same three picks without seeing each other.

- **BEST BET: [HOT-SIDE MEMORY](dossiers/hot-side-memory.md).** Oxide gain cells (two transistors, no capacitor) stacked in the carrier wafer bonded onto a GPU. ~10x lower energy per bit delivered than HBM (high-bandwidth memory): 0.37 vs 3.95 pJ/bit [MODEL].
- **FASTEST PROOF: [RAW-BER CONTRACT](dossiers/raw-ber-contract.md).** Error-correcting codes carry the rare weak bits, so DRAM refreshes far less often. BER = bit error rate. ~9x less refresh energy on DDR5 server modules at 85 °C, keeping chipkill (the code that survives a dead chip) [MODEL]. No fab needed.
- **MOONSHOT: [AND-STACK](dossiers/and-stack.md).** DRAM built like 3D NAND: many deposited layers, one hole etch, a 2-bit oxide cell per tier. 64 tiers × 2 bits = 2.62 Gb/mm², 5.9x today's leading DRAM node (1-beta), with no EUV lithography [MODEL].
- **Biggest unknown.** The statistical tails of small amorphous-oxide transistors (IGZO, IGO, ZTO) after the full ≤400 °C hydrogen, thermal and bonding budget, at 85-125 °C. Two numbers decide it: the 1e-4 to 2e-5 quantile of attoamp-level off-state leakage (1 aA = 1e-18 A), and the 1e-4 quantile of random telegraph noise (RTN). This one measurement sets the size of the step for 7 of the 10 concepts.
- **Monday action.** In ≤2 hours, write a one-page "Oxide Tail Spec" (device structures × channel splits, device area, timescale, temperature, hydrogen/thermal dose, bond split, and each concept's pass/kill line from the dossiers' sections 5 and 11). Send it to an oxide-transistor university group with external-user access; the judges name Purdue's Birck Nanotechnology Center. Ask whether they can run it and at what cost.

## The funnel in one line

12,857 ideas → 10,525 distinct (2,332 same-mechanism duplicates removed) → 432 critiqued by two lenses → 30 ADVANCE → 10 concepts → 181 red-team objections, all answered (10 downgraded, 0 killed) → 3 unanimous picks. Details: [IDEAS_INDEX.md](IDEAS_INDEX.md) and report section 5.

## Start here

1. [DRAM_MOONSHOT_REPORT.md](DRAM_MOONSHOT_REPORT.md): the final report. Section 1 is the one-page answer.
2. The three pick dossiers: [hot-side-memory](dossiers/hot-side-memory.md), [raw-ber-contract](dossiers/raw-ber-contract.md), [and-stack](dossiers/and-stack.md). Section 11 of each is the red-team outcome and overrides the body.
3. [REDTEAM.md](REDTEAM.md): every objection and its answer, verbatim.
4. [IDEAS_INDEX.md](IDEAS_INDEX.md): the map of all 12,857 ideas.
5. [MISSION.md](MISSION.md): the question, the framing and the rules.

## Home lab

Can any of this be tested at home? At bench scale, yes. [home-lab/](home-lab/README.md) has eight experiments, from a one-transistor bit on a breadboard (E1) to a zinc-oxide transistor and gain cell made at home (E7, E8), with a first-principles backbone ([FIRST_PRINCIPLES.md](home-lab/FIRST_PRINCIPLES.md)) and one safety guide ([SAFETY.md](home-lab/SAFETY.md)).
The best first project for a software builder is E6: map the retention tail of a real 64 Mbit DRAM chip on a ~$32-66 development board, the FASTEST PROOF mechanism on a desk.
Home work cannot measure the oxide leakage tail itself. It builds the method, the analysis code and the data package for the Oxide Tail Spec.
Check it with `python3 home-lab/tools/check_home_lab.py`.

## Outreach

The Monday action, ready to send: [outreach/](outreach/README.md) holds the Oxide Tail Spec (one page plus working notes), a ranked list of nanofabs, faculty groups and DRAM test partners, five email drafts, and a reply tracker.
Start at [outreach/README.md](outreach/README.md). Every rate and name there rests on search snippets, so confirm by email before you budget.

## File map

| Path | What it holds |
|---|---|
| [DRAM_MOONSHOT_REPORT.md](DRAM_MOONSHOT_REPORT.md) | Final report: answer, picks, $1M plan, what died, honest limits |
| [REDTEAM.md](REDTEAM.md) | Compiled red team (generated; do not edit by hand) |
| [IDEAS_INDEX.md](IDEAS_INDEX.md) | Idea funnel index (generated; do not edit by hand) |
| [MISSION.md](MISSION.md) | Mission, framing, capital frame, rules |
| [home-lab/](home-lab/README.md) | Eight home experiments (E1-E8), first-principles backbone, safety guide and their code |
| [dossiers/](dossiers/) | One technical dossier per final concept (sections 0-11) |
| [models/](models/) | One Python model per concept, plus the shared `dram_cell_physics.py` |
| [research/phaseA/](research/phaseA/) | Bottleneck map: scaling limits, materials, research frontier |
| [research/phaseB/](research/phaseB/) | 101 expert-lens seed ideas and the physics triage |
| [research/ideas10k/](research/ideas10k/) | Idea pool, screening scores, Stage 2 critiques |
| [research/stage3/](research/stage3/) | Final concepts, notes, model outputs, judge files, `decision.json` |
| [research/redteam/](research/redteam/) | Attacker objections (`rt_*.json`), answers (`responses_*.json`), summary |
| [research/models/](research/models/) | Phase A-C estimate scripts |
| [research/sources/](research/sources/), [research/assumptions/](research/assumptions/) | Source and assumption logs |
| [research/tools/](research/tools/) | Merge, screening, aggregation, compile and gate scripts |

## How to re-run

The language-model steps cannot be re-run by script. The scripts below check, compile and model. Run them from this folder. Most overwrite their outputs, so work on a copy if in doubt.

```bash
python3 research/tools/gate_check.py          # verification gate: PASS/FAIL per check, exit 1 on any FAIL
python3 research/tools/compile_redteam.py     # rebuild REDTEAM.md; exit 1 if any objection lacks an answer
python3 research/tools/build_ideas_index.py   # rebuild IDEAS_INDEX.md
for f in models/*.py; do python3 "$f"; done   # concept models; write research/stage3/<slug>_model_output.md
for f in research/models/*.py; do python3 "$f"; done
```

The full pipeline, including dedup, screening and Stage 2 aggregation, is in report section 13.

## Honest limits

The evidence is mostly web-search snippets with patent claims unread, and the models are first-order arithmetic with no lab data: every pass line sits in a 1e-4 to 2e-5 tail that no file here measures. Ideas, scores, critiques and verdicts all came from language-model agents, and the judges read the same dossiers, so their unanimity is not independent evidence. "10,525 distinct" overstates mechanism diversity, because duplicates were caught only lexically or within ~100-idea batches.
