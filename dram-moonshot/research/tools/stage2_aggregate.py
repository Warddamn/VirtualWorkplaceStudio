#!/usr/bin/env python3
"""Merge Stage 2 two-lens critiques into a consensus ranking.

Inputs : research/ideas10k/stage2/reviews/{physics,innovation}_R##.jsonl, stage2 batches, scored_ideas.jsonl
Outputs: research/ideas10k/stage2/stage2_results.jsonl, STAGE2_REPORT.md, advance.jsonl
Consensus score (0-100, breakthrough-weighted, both lenses averaged): (1.2*S2 + 1.0*N2 + 0.7*P2 + 0.5*D2) / 17 * 100
Verdict: ADVANCE if both lenses ADVANCE, or one ADVANCE + one HOLD with consensus >= 70;
         DROP if both DROP, or the physics lens DROPs with P2 <= 2; otherwise HOLD.
"""
import json
from collections import Counter
from pathlib import Path

DM = Path(__file__).resolve().parents[2]
S2 = DM / "research" / "ideas10k" / "stage2"
ideas = {}
for ln in (DM / "research/ideas10k/screen/scored_ideas.jsonl").read_text().splitlines():
    if ln.strip():
        d = json.loads(ln)
        ideas[d["id"]] = d
batch_ids = {}
for f in sorted((S2 / "batches").glob("R*.jsonl")):
    for ln in f.read_text().splitlines():
        if ln.strip():
            batch_ids[json.loads(ln)["id"]] = f.stem
rev = {}
missing = []
for f in sorted((S2 / "batches").glob("R*.jsonl")):
    for lens in ("physics", "innovation"):
        rf = S2 / "reviews" / f"{lens}_{f.stem}.jsonl"
        if not rf.exists():
            missing.append(rf.name)
            continue
        for ln in rf.read_text().splitlines():
            try:
                r = json.loads(ln)
            except json.JSONDecodeError:
                continue
            rev.setdefault(r.get("id"), {})[lens] = r


def num(r, k, default=3):
    try:
        return max(1, min(5, int(r.get(k, default))))
    except Exception:
        return default


rows = []
for iid, b in batch_ids.items():
    lenses = rev.get(iid, {})
    scores, verdicts = [], {}
    for lens, r in lenses.items():
        s = (1.2 * num(r, "S2") + 1.0 * num(r, "N2") + 0.7 * num(r, "P2") + 0.5 * num(r, "D2")) / 17 * 100
        scores.append(s)
        verdicts[lens] = str(r.get("verdict", "HOLD")).upper()
    cons = round(sum(scores) / len(scores), 1) if scores else 0
    v = list(verdicts.values())
    pP2 = num(lenses.get("physics", {}), "P2")
    if len(v) == 2 and v.count("ADVANCE") == 2:
        final = "ADVANCE"
    elif "ADVANCE" in v and "HOLD" in v and cons >= 70:
        final = "ADVANCE"
    elif (len(v) == 2 and v.count("DROP") == 2) or (verdicts.get("physics") == "DROP" and pP2 <= 2):
        final = "DROP"
    else:
        final = "HOLD"
    base = ideas.get(iid, {})
    rows.append({"id": iid, "batch": b, "title": base.get("title", ""), "facet": base.get("facet", ""),
                 "technique": base.get("technique", ""), "idea": base.get("idea", ""), "consensus": cons, "final": final,
                 "verdicts": verdicts, "lenses_present": len(lenses),
                 "physics": lenses.get("physics", {}), "innovation": lenses.get("innovation", {})})
rows.sort(key=lambda r: ({"ADVANCE": 0, "HOLD": 1, "DROP": 2}[r["final"]], -r["consensus"]))
with (S2 / "stage2_results.jsonl").open("w") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
adv = [r for r in rows if r["final"] == "ADVANCE"]
with (S2 / "advance.jsonl").open("w") as fh:
    for r in adv:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
cnt = Counter(r["final"] for r in rows)
lines = ["# Stage 2 report: two-lens critique of the 408-idea pool", "",
         f"Reviewed {len(rows)} ideas; missing review files: {len(missing)} {missing[:6] if missing else ''}. "
         f"Final: ADVANCE {cnt['ADVANCE']}, HOLD {cnt['HOLD']}, DROP {cnt['DROP']}.", "",
         "Consensus = mean over the physics and innovation lenses of (1.2·S2 + 1.0·N2 + 0.7·P2 + 0.5·D2)/17, re-scored by the critics.", "",
         "## ADVANCE", "", "| id | score | facet | title | key insight | killer doubt | decisive experiment |", "|---|---|---|---|---|---|---|"]
for r in adv:
    p, i = r["physics"], r["innovation"]
    ki = (i.get("key_insight") or p.get("key_insight") or "").replace("|", "/")
    kd = (p.get("killer_doubt") or i.get("killer_doubt") or "").replace("|", "/")
    ex = (p.get("decisive_experiment") or i.get("decisive_experiment") or "").replace("|", "/")
    lines.append(f"| {r['id']} | {r['consensus']} | {r['facet'][:28]} | {r['title']} | {ki} | {kd} | {ex} |")
(S2 / "STAGE2_REPORT.md").write_text("\n".join(lines) + "\n")
print(f"stage2: {len(rows)} ideas; ADVANCE {cnt['ADVANCE']} HOLD {cnt['HOLD']} DROP {cnt['DROP']}; missing review files {len(missing)}")
