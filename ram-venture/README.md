# American Memory: venture study (as of 2026-11-01)

The question was whether there is a profitable way to make RAM, or something that does RAM's job better, in the United States from cheaper materials, processes or capital, for a software-builder founder with under $50k and a day job. The full brief is in `research/MISSION_PROMPT.md`.

## The answer

**No venture-scale opportunity survived.**
- 98 concepts were generated and **83 killed**, each for a stated rule. The kill rules are listed in `03_SCORING.md` §2 and on every card in `02_CONCEPTS.md`.
- Seven deep dives faced two red-team rounds: **186 objections, all 186 answered, 0 refuted**.
  - Five deep dives were killed.
  - Two were cut to capped side lines.
  - Nothing pays the founder a salary within 36 months in any DRAM price scenario.
- The literal mission, making cheaper memory bits in the U.S., is closed to an entrant on two counts:
  - The U.S. has no DRAM foundry, no display fab and no open die supply. The details are in `01_LANDSCAPE.md` §0 and §6.
  - Incumbents make DDR5 at about $1.48/GB and still earn about 82% gross margin at the $8.15/GB glut price. This comes from `models/dram_cost_stack.py`.
- **The paying needs sit beside the build-out, not inside it:** lifecycle, procurement and price intelligence sold to the people who buy memory.

| Pick | What | Status |
|---|---|---|
| **PRIMARY** | DD2: Memory Lifecycle & Cost Intelligence SaaS for small U.S. hardware OEMs (C-80, C-29, C-61) | A gated side business, not a venture. Kill test: ~$1,950 planned, 29 days, starting with a written employer carve-out |
| **FALLBACK** | DD5: OpenRAM macro service for U.S. open-PDK tapeouts (C-33) | Runs only after DD2 fails. Its $0 written questions go out in week 1 |
| **MOONSHOT** | None honestly qualifies. Best available: C-86, a contract-reference Memory Cost Escalation Index, held as a ~$0 option inside DD2's test | About 3% odds (ceiling judge) |

**Monday morning (≤2 h, $0):**
1. Lock DD2's pass/fail thresholds in a dated document sent to an outside advisor.
2. Ask the employer for a written carve-out.
3. Send DD5's no-release questions to UCSC VLSIDA and Open Circuit Design.

See `FIRST_90_DAYS.md` for the full plan.

## Read in this order
1. `INVESTOR_MEMO.md`: the two-page case for the PRIMARY, written honestly.
2. `FIRST_90_DAYS.md`: week by week from 2026-11-02, opening with the under-$10k kill experiment, with branches for pass and fail.
3. `SUMMARY_TABLE.md`: every surviving concept with scores under all three weightings, plus the §3E business-model lens matrix.
4. `05_REDTEAM.md`: every objection, word for word, with the response and disposition.
5. `04_DEEPDIVES/`: seven deep dives, each with a unit-economics model in `models/<slug>.py`.
   - Round 1: `provenance-recert`, `lifecycle-intel`, `nv-continuity-modules`, `memory-efficiency`, `open-memory-ip`.
   - Round 2: `private-moe-appliance`, `legacy-dram-diebank`.
6. `03_SCORING.md`: the kill register, rubric, three weightings, rank shifts and rubric blind spots. §9 explains why a second round was run.
7. `01_LANDSCAPE.md`: the premise checked bullet by bullet. It covers prices, margins, the cost stack, the U.S. capacity map, funding, export controls and IP.
8. `02_CONCEPTS.md` / `concepts.csv`: all 98 cards.
9. `OPEN_QUESTIONS.md`: what the study could not answer, and the 15 facts to re-check from primary sources.
10. `ASSUMPTIONS.md` and `SOURCES.md`: every assumption (A-xx) and every source, with access dates.

## Models (all exit 0 with `python3 models/<name>.py`)
- `dram_cost_stack.py`: DRAM $/GB from wafer to module, with cost against price against glut, and sensitivity. `ddr5_reference()` gives the canonical numbers.
- `device_cost_compare.py`: $/GB for every device concept against DDR5 today and in a glut.
- `scoring.py`: the Phase 3 rubric. Weights are editable, and all three weightings are computed.
- `<slug>.py` ×7: a 36-month P&L for each deep dive under BASE, GLUT and SEVERE, with sensitivity and the red-team revisions.

## How to re-run the checks
```
python3 research/tools/gate_check.py        # Phase 7 deterministic gate (must print GATE: PASS)
python3 research/tools/compile_redteam.py   # rebuilds 05_REDTEAM.md; fails if any objection is unanswered
python3 research/tools/merge_sources.py --check
```

## Evidence caveat
- **Search-snippet grade:** almost every external fact comes from search-result snippets. Web search was capped at 200 calls per turn, and the network policy blocked trendforce.com, sec.gov, investors.micron.com, nist.gov and other primary hosts, so few primary pages were opened.
- **Tags:** facts carry [REPORTED-P], [REPORTED], [ESTIMATE] or [UNVERIFIED].
- **Before any money moves:** re-check the 15 highest-weight facts listed in `OPEN_QUESTIONS.md` §6.2.

Working files from every phase are in `research/`, including agent notes, per-agent source and assumption logs, audits, scorer files, red-team JSON and the tools.
