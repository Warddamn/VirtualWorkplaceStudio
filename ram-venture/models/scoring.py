#!/usr/bin/env python3
"""Phase 3 scoring model for the American Memory venture study.

Inputs
  research/phase3/scores_raw/*.json   independent scorer outputs, each:
      {"scorer": "<key>", "scores": [{"id": "C-01", "criteria": {"tech": {"score": 1-5, "why": "..."}, ...}}]}
  research/phase2/concepts_master.json  concept metadata (name, tier, status)

Outputs
  scores.csv                          one row per scored concept: consensus (median) criterion scores,
                                      justification, and weighted totals under three weightings + ranks
  research/phase3/rankings.md         ranking tables and rank-shift analysis (embedded into 03_SCORING.md)

Method
  * Each criterion is scored 1-5 (5 = best for the venture; capital, competitive density and
    regulatory risk are scored inversely, so 5 = least capital / least crowded / least risk).
  * Consensus score per criterion = median of independent scorers (ties -> lower median, i.e.
    conservative). Justification = text from a scorer whose score equals the consensus.
  * Weighted total = sum(weight * score) / (5 * sum(weights)) * 100  -> 0..100 scale.
  * Three weightings per mission Phase 3: default, capital-constrained (x2 capital & founder-fit),
    moonshot (x2 moat & gross margin).
  * Disagreement (max-min across scorers >= 3 on any criterion) is flagged for review.

Run: python3 models/scoring.py   (exits 0; prints the top 15 under each weighting)
"""
import csv
import json
import statistics
import sys
from pathlib import Path

RV = Path(__file__).resolve().parents[1]
RAW_DIR = RV / "research" / "phase3" / "scores_raw"
MASTER = RV / "research" / "phase2" / "concepts_master.json"
OUT_CSV = RV / "scores.csv"
OUT_MD = RV / "research" / "phase3" / "rankings.md"

# Criterion key -> (label, default weight). Mission Phase 3 rubric; edit weights here.
CRITERIA = {
    "tech":        ("Technical feasibility", 20),
    "capital":     ("Capital required (inverse)", 15),
    "ttr":         ("Time to revenue", 15),
    "usmfg":       ("U.S. manufacturability", 10),
    "margin":      ("Gross margin", 10),
    "moat":        ("Moat", 10),
    "competition": ("Competitive density (inverse)", 5),
    "regulatory":  ("Regulatory/export risk (inverse)", 5),
    "cycle":       ("Cycle-proofing", 5),
    "founder":     ("Founder-fit", 5),
}

DEFAULT = {k: w for k, (_, w) in CRITERIA.items()}
CAPITAL_CONSTRAINED = dict(DEFAULT, capital=DEFAULT["capital"] * 2, founder=DEFAULT["founder"] * 2)
MOONSHOT = dict(DEFAULT, moat=DEFAULT["moat"] * 2, margin=DEFAULT["margin"] * 2)
WEIGHTINGS = {"default": DEFAULT, "capital_constrained": CAPITAL_CONSTRAINED, "moonshot": MOONSHOT}


def weighted(scores: dict, weights: dict) -> float:
    total_w = sum(weights.values())
    return round(sum(weights[k] * scores[k] for k in weights) / (5 * total_w) * 100, 1)


def low_median(vals):
    s = sorted(vals)
    return s[(len(s) - 1) // 2]


def load_raw():
    per_concept = {}
    scorers = []
    if not RAW_DIR.exists():
        return per_concept, scorers
    for f in sorted(RAW_DIR.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        scorer = data.get("scorer", f.stem)
        scorers.append(scorer)
        for row in data.get("scores", []):
            cid = row["id"]
            for crit, v in row["criteria"].items():
                if crit not in CRITERIA:
                    continue
                sc = int(v["score"])
                if not 1 <= sc <= 5:
                    raise ValueError(f"{f.name}: {cid}.{crit} score {sc} out of range")
                per_concept.setdefault(cid, {}).setdefault(crit, []).append((sc, v.get("why", ""), scorer))
    return per_concept, scorers


def main():
    meta = {}
    if MASTER.exists():
        for c in json.loads(MASTER.read_text(encoding="utf-8"))["cards"]:
            meta[c["id"]] = c
    raw, scorers = load_raw()
    if not raw:
        print("scoring.py: no raw scores yet (research/phase3/scores_raw/ empty) — nothing to do.")
        print("Weightings:", json.dumps(WEIGHTINGS, indent=1))
        return 0

    rows = []
    flags = []
    for cid, crits in raw.items():
        missing = [k for k in CRITERIA if k not in crits]
        if missing:
            flags.append(f"{cid}: missing criteria {missing} — skipped")
            continue
        cons, why = {}, {}
        for k, lst in crits.items():
            vals = [s for s, _, _ in lst]
            m = low_median(vals)
            cons[k] = m
            why[k] = next((w for s, w, _ in lst if s == m), lst[0][1])
            if max(vals) - min(vals) >= 3:
                flags.append(f"{cid}.{k}: scorer spread {vals} (consensus {m})")
        row = {"id": cid, "name": meta.get(cid, {}).get("name", ""),
               "capital_tier": meta.get(cid, {}).get("capital_tier", ""),
               "branch": meta.get(cid, {}).get("branch", ""),
               "n_scorers": min(len(v) for v in crits.values())}
        for k in CRITERIA:
            row[k] = cons[k]
            row[f"{k}_why"] = why[k]
            row[f"{k}_mean"] = round(statistics.mean(s for s, _, _ in crits[k]), 2)
        for wname, w in WEIGHTINGS.items():
            row[f"total_{wname}"] = weighted(cons, w)
        rows.append(row)

    for wname in WEIGHTINGS:
        ranked = sorted(rows, key=lambda r: (-r[f"total_{wname}"], -r["tech"], r["id"]))
        for i, r in enumerate(ranked, 1):
            r[f"rank_{wname}"] = i

    rows.sort(key=lambda r: r["rank_default"])
    fields = (["rank_default", "rank_capital_constrained", "rank_moonshot", "id", "name", "branch", "capital_tier",
               "total_default", "total_capital_constrained", "total_moonshot", "n_scorers"]
              + list(CRITERIA) + [f"{k}_why" for k in CRITERIA] + [f"{k}_mean" for k in CRITERIA])
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    md = ["## Rankings under three weightings", "",
          f"Scorers: {', '.join(scorers)} (consensus = lower median per criterion). Totals on a 0–100 scale.", "",
          "| Weighting | " + " | ".join(f"{CRITERIA[k][0]}" for k in CRITERIA) + " |",
          "|---|" + "---|" * len(CRITERIA)]
    for wname, wts in WEIGHTINGS.items():
        md.append(f"| {wname} | " + " | ".join(str(wts[k]) for k in CRITERIA) + " |")
    md += ["", "| Concept | Tier | Default (rank) | Capital-constrained (rank) | Moonshot (rank) | Max rank shift |",
           "|---|---|---|---|---|---|"]
    for r in rows:
        ranks = [r["rank_default"], r["rank_capital_constrained"], r["rank_moonshot"]]
        md.append(f"| {r['id']} {r['name']} | {r['capital_tier']} | {r['total_default']} ({r['rank_default']}) | "
                  f"{r['total_capital_constrained']} ({r['rank_capital_constrained']}) | "
                  f"{r['total_moonshot']} ({r['rank_moonshot']}) | {max(ranks) - min(ranks)} |")
    md += ["", "### Biggest movers between weightings", ""]
    movers = sorted(rows, key=lambda r: -(max(r["rank_default"], r["rank_capital_constrained"], r["rank_moonshot"])
                                          - min(r["rank_default"], r["rank_capital_constrained"], r["rank_moonshot"])))[:10]
    for r in movers:
        md.append(f"- {r['id']} {r['name']}: default #{r['rank_default']} → capital-constrained "
                  f"#{r['rank_capital_constrained']} → moonshot #{r['rank_moonshot']}")
    if flags:
        md += ["", "### Scorer-disagreement flags (spread ≥ 3 points)", ""] + [f"- {f}" for f in flags]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    for wname in WEIGHTINGS:
        print(f"\nTop 15 — {wname}")
        for r in sorted(rows, key=lambda r: r[f"rank_{wname}"])[:15]:
            print(f"  {r[f'rank_{wname}']:>2}. {r['id']:<6} {r[f'total_{wname}']:>5}  {r['capital_tier']:<3} {r['name'][:60]}")
    print(f"\nscored {len(rows)} concepts from {len(scorers)} scorers; {len(flags)} flags -> scores.csv, research/phase3/rankings.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
