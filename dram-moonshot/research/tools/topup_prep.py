#!/usr/bin/env python3
"""Prepare the novelty top-up round: 6 new creativity techniques x 10 facets (3 per facet = 30 cells),
plus per-facet exclusion lists of mechanism families already covered (from screener theme tags and titles)."""
import json
from collections import Counter, defaultdict
from pathlib import Path

DM = Path(__file__).resolve().parents[2]
TOP = DM / "research" / "ideas10k" / "topup"
cfg = json.loads((DM / "research" / "ideas10k" / "config.json").read_text())
NEW_T = [
 ("T26", "Constraint stacking", "Apply TWO forced constraints at once; the collision forces genuinely different mechanisms."),
 ("T27", "Distant-field transplant", "Transplant a working mechanism from a far field: music, linguistics, markets/finance, sports, medicine, astronomy, agriculture, military logistics, theatre."),
 ("T28", "Extremophiles, minerals and Earth systems", "Learn from tardigrades, deep-sea vents, minerals that record magnetic history, ice cores, tree rings, geodes, weather and ocean memory."),
 ("T29", "Time travel", "How a 1955 engineer would solve it with 2026 materials; how a 2100 engineer would; what the 1970s would have built if DRAM had never been invented."),
 ("T30", "Paradox as feature", "Embrace a contradiction (volatile AND permanent, dense AND sparse, analog AND digital, forgetful AND exact) and make it the mechanism."),
 ("T31", "Measurement-first invention", "Invent the instrument, metrology or test method that would unlock a new memory, then design the memory that the new measurement makes possible."),
]
scored = [json.loads(x) for x in (DM / "research/ideas10k/screen/scored_ideas.jsonl").read_text().splitlines() if x.strip()]
themes = defaultdict(Counter)
for d in scored:
    if d.get("theme"):
        themes[d.get("facet") or "Phase B seeds"][d["theme"].strip().lower()] += 1
cells = []
for fi, f in enumerate(cfg["facets"]):
    excl = [t for t, _ in themes[f["name"]].most_common(140)]
    (TOP / f"exclude_{f['id']}.txt").write_text(
        f"Mechanism families ALREADY covered in facet '{f['name']}' (from screener theme tags, most common first). "
        "Your ideas must NOT belong to any of these families:\n" + "\n".join(f"- {t}" for t in excl) + "\n")
    for k in range(3):
        t = NEW_T[(fi + 2 * k) % len(NEW_T)]
        c1 = cfg["constraints"][(fi * 5 + k * 11) % len(cfg["constraints"])]
        c2 = cfg["constraints"][(fi * 5 + k * 11 + 7) % len(cfg["constraints"])]
        cells.append({"cell": f"{t[0]}-{f['id']}", "technique": t[1], "technique_def": t[2], "facet": f["name"],
                      "facet_def": f["def"], "constraint": c1 + (" AND " + c2 if t[0] == "T26" else ""),
                      "exclude_file": f"research/ideas10k/topup/exclude_{f['id']}.txt"})
json.dump({"techniques": [{"id": a, "name": b, "def": c} for a, b, c in NEW_T], "ideas_per_cell": 42, "cells": cells},
          open(TOP / "config.json", "w"), indent=1)
print(len(cells), "top-up cells;", sum(len(v) for v in themes.values()), "theme tags across", len(themes), "facets")
