#!/usr/bin/env python3
"""Screening tools for the 10k idea pool.

  python3 research/tools/screen_tools.py batch       # write research/ideas10k/screen/batches/S###.jsonl (~100 ideas each)
  python3 research/tools/screen_tools.py aggregate   # merge scores -> scored_ideas.jsonl/csv, shortlist.jsonl, SCREEN_REPORT.md

Batching: ideas grouped by facet (Phase B seeds in their own group), ordered by a MinHash key so lexically
similar ideas sit together (helps screeners spot same-mechanism duplicates), then cut into ~100-idea batches.
Composite: S*1.0 + P*0.8 + N*0.6 + D*0.6 (max 15) -> 0-100. Flags: BREAKTHROUGH (S=5,P>=3), MOONSHOT (S=5,N>=4,P>=2),
QUICKWIN (D>=4,P>=4,S>=3). Within-batch percentile is kept to expose screener leniency.
Shortlist: top ~300 by composite with a per-facet floor (>=20 per facet) for diversity; duplicates excluded.
"""
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

DM = Path(__file__).resolve().parents[2]
IDEAS = DM / "research" / "ideas10k" / "ideas_10k.jsonl"
SDIR = DM / "research" / "ideas10k" / "screen"
BATCH_SIZE = 100
W = {"S": 1.0, "P": 0.8, "N": 0.6, "D": 0.6}


def mh_key(text):
    words = [w for w in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split() if len(w) > 3]
    sh = {" ".join(words[i:i + 2]) for i in range(max(1, len(words) - 1))}
    return min((int(hashlib.md5(s.encode()).hexdigest()[:12], 16) for s in sh), default=0)


def batch():
    ideas = [json.loads(x) for x in IDEAS.read_text().splitlines() if x.strip()]
    groups = defaultdict(list)
    for d in ideas:
        groups[d.get("facet") or "Phase B seeds"].append(d)
    (SDIR / "batches").mkdir(parents=True, exist_ok=True)
    n = 0
    manifest = []
    for g in sorted(groups):
        items = sorted(groups[g], key=lambda d: mh_key(d["title"] + " " + d["idea"]))
        k = max(1, round(len(items) / BATCH_SIZE))
        size = -(-len(items) // k)
        for i in range(0, len(items), size):
            n += 1
            bid = f"S{n:03d}"
            chunk = items[i:i + size]
            with (SDIR / "batches" / f"{bid}.jsonl").open("w") as fh:
                for d in chunk:
                    fh.write(json.dumps({k2: d.get(k2) for k2 in ("id", "title", "idea", "why", "kind", "physics_risk")},
                                        ensure_ascii=False) + "\n")
            manifest.append({"batch": bid, "facet": g, "n": len(chunk)})
    (SDIR / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"{n} batches, {sum(m['n'] for m in manifest)} ideas")


def aggregate():
    ideas = {json.loads(x)["id"]: json.loads(x) for x in IDEAS.read_text().splitlines() if x.strip()}
    manifest = json.loads((SDIR / "manifest.json").read_text())
    scored, missing, bad = {}, [], []
    for m in manifest:
        f = SDIR / "scores" / f"{m['batch']}.jsonl"
        if not f.exists():
            missing.append(m["batch"])
            continue
        rows = []
        for ln in f.read_text().splitlines():
            try:
                rows.append(json.loads(ln))
            except json.JSONDecodeError:
                bad.append(m["batch"])
        comps = []
        for r in rows:
            if r.get("id") not in ideas:
                continue
            try:
                vals = {k: max(1, min(5, int(r[k]))) for k in "PSND"}
            except Exception:
                bad.append(f"{m['batch']}:{r.get('id')}")
                continue
            c = round(sum(W[k] * vals[k] for k in W) / (5 * sum(W.values())) * 100, 1)
            comps.append(c)
            scored[r["id"]] = {**ideas[r["id"]], **vals, "composite": c, "dup_of": r.get("dup_of", "") or "",
                               "theme": r.get("theme", ""), "note": r.get("note", ""), "batch": m["batch"]}
        srt = sorted(comps)
        for r in rows:
            if r.get("id") in scored and scored[r["id"]]["batch"] == m["batch"]:
                c = scored[r["id"]]["composite"]
                scored[r["id"]]["batch_pct"] = round(100 * sum(1 for x in srt if x <= c) / max(1, len(srt)), 1)
    for d in scored.values():
        flags = []
        if d["S"] == 5 and d["P"] >= 3:
            flags.append("BREAKTHROUGH")
        if d["S"] == 5 and d["N"] >= 4 and d["P"] >= 2:
            flags.append("MOONSHOT")
        if d["D"] >= 4 and d["P"] >= 4 and d["S"] >= 3:
            flags.append("QUICKWIN")
        d["flags"] = ",".join(flags)
    allrows = sorted(scored.values(), key=lambda d: (-d["composite"], -d["S"], -d["N"], d["id"]))
    for i, d in enumerate(allrows, 1):
        d["rank"] = i
    with (SDIR / "scored_ideas.jsonl").open("w") as fh:
        for d in allrows:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    cols = ["rank", "id", "composite", "batch_pct", "S", "P", "N", "D", "flags", "theme", "facet", "technique", "kind",
            "title", "idea", "note", "dup_of", "cell"]
    with (SDIR / "scored_ideas.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(allrows)
    nondup = [d for d in allrows if not d["dup_of"]]
    facets = Counter(d.get("facet") or "Phase B seeds" for d in nondup)
    short, seen = [], set()
    for fct in facets:  # per-facet floor
        for d in [x for x in nondup if (x.get("facet") or "Phase B seeds") == fct][:20]:
            short.append(d)
            seen.add(d["id"])
    for d in nondup:  # fill to ~300 by composite, always including every BREAKTHROUGH/MOONSHOT
        if len(short) >= 300 and not ({"BREAKTHROUGH", "MOONSHOT"} & set(d["flags"].split(","))):
            continue
        if d["id"] not in seen:
            short.append(d)
            seen.add(d["id"])
    short.sort(key=lambda d: -d["composite"])
    with (SDIR / "shortlist.jsonl").open("w") as fh:
        for d in short:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    themes = Counter(d["theme"].strip().lower() for d in nondup if d["theme"])
    lines = ["# Screening report", "",
             f"Scored {len(scored)} of {len(ideas)} ideas ({len(missing)} batches missing: {missing or 'none'}; malformed: {len(bad)}). "
             f"Screener-flagged same-mechanism duplicates: {sum(1 for d in allrows if d['dup_of'])}. Shortlist: {len(short)}.", "",
             f"Flags: BREAKTHROUGH {sum('BREAKTHROUGH' in d['flags'] for d in allrows)}, MOONSHOT {sum('MOONSHOT' in d['flags'] for d in allrows)}, "
             f"QUICKWIN {sum('QUICKWIN' in d['flags'] for d in allrows)}.", "",
             "## Top 50 by composite", "", "| # | id | score | S | P | N | D | flags | theme | title |", "|---|---|---|---|---|---|---|---|---|---|"]
    for d in nondup[:50]:
        lines.append(f"| {d['rank']} | {d['id']} | {d['composite']} | {d['S']} | {d['P']} | {d['N']} | {d['D']} | {d['flags']} | "
                     f"{d['theme']} | {d['title']} |")
    lines += ["", "## Most common themes (non-duplicates)", ""] + [f"- {t}: {c}" for t, c in themes.most_common(60)]
    (SDIR / "SCREEN_REPORT.md").write_text("\n".join(lines) + "\n")
    print(f"scored {len(scored)}/{len(ideas)}; missing batches {len(missing)}; dups flagged {sum(1 for d in allrows if d['dup_of'])}; shortlist {len(short)}")


if __name__ == "__main__":
    {"batch": batch, "aggregate": aggregate}[sys.argv[1]]()
