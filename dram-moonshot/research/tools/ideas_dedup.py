#!/usr/bin/env python3
"""Merge, validate and deduplicate the 10,000-idea pool.

Inputs : research/ideas10k/raw/*.jsonl  (one idea per line; schema in research/ideas10k/BRIEF.md)
         research/phaseB/B*-*.json       (Phase B seed ideas, if present; mapped into the same schema)
Outputs: research/ideas10k/ideas_10k.jsonl   unique ideas with global ids I-00001...
         research/ideas10k/ideas_10k.csv
         research/ideas10k/duplicates.jsonl  removed near-duplicates with the id they duplicate
         research/ideas10k/stats.json        counts by cell / technique / facet / kind; under-filled cells
Method : normalize text -> exact-title dedup -> MinHash LSH (word 2-shingles of title+idea, 128 perms,
         32 bands x 4 rows) -> verify candidates by true Jaccard >= THRESH -> keep the first occurrence.
Usage  : python3 research/tools/ideas_dedup.py [--thresh 0.5] [--target 10000]
"""
import csv
import glob
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

DM = Path(__file__).resolve().parents[2]
RAW = DM / "research" / "ideas10k" / "raw"
OUT = DM / "research" / "ideas10k"
CFG = json.loads((OUT / "config.json").read_text())
THRESH = float(sys.argv[sys.argv.index("--thresh") + 1]) if "--thresh" in sys.argv else 0.5
TARGET = int(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else 10000
PERMS, BANDS = 128, 32
ROWS = PERMS // BANDS
STOP = set("a an the of to and or in on for with by is are be as at from that this it its into via using use uses can than then".split())
TECH = {t["id"]: t["name"] for t in CFG["techniques"]}
_TC = DM / "research" / "ideas10k" / "topup" / "config.json"
if _TC.exists():
    TECH.update({t["id"]: t["name"] for t in json.loads(_TC.read_text())["techniques"]})
FACET = {f["id"]: f["name"] for f in CFG["facets"]}


def norm(s):
    s = re.sub(r"[^a-z0-9 ]+", " ", str(s).lower())
    return [w for w in s.split() if w not in STOP]


def shingles(words):
    return {" ".join(words[i:i + 2]) for i in range(max(1, len(words) - 1))}


def h64(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), "little")


rng = np.random.default_rng(12345)
P = (1 << 31) - 1  # Mersenne prime: (a*x+b) < 2^62 fits in uint64, so hashing stays vectorized
A = rng.integers(1, P, size=PERMS, dtype=np.uint64)
B = rng.integers(0, P, size=PERMS, dtype=np.uint64)


def minhash(sh):
    hs = np.array([h64(x) % P for x in sh], dtype=np.uint64)
    if hs.size == 0:
        return np.zeros(PERMS, dtype=np.uint64)
    v = (np.outer(hs, A) + B) % np.uint64(P)
    return v.min(axis=0)


def load():
    ideas, bad = [], []
    for f in sorted(RAW.glob("*.jsonl")):
        for i, ln in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            ln = ln.strip()
            if not ln:
                continue
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                bad.append(f"{f.name}:{i}")
                continue
            if not str(d.get("title", "")).strip() or not str(d.get("idea", "")).strip():
                bad.append(f"{f.name}:{i} (empty)")
                continue
            d["cell"] = d.get("cell") or f.stem
            d["source"] = "ideas10k"
            ideas.append(d)
    for f in sorted(glob.glob(str(DM / "research" / "phaseB" / "B*-*.json"))):
        try:
            data = json.loads(Path(f).read_text())
        except Exception:
            continue
        for d in data.get("ideas", []):
            ideas.append({"cell": "PHASE-B:" + Path(f).stem, "n": d.get("id"), "title": d.get("name", ""),
                          "idea": d.get("mechanism", d.get("one_liner", "")),
                          "why": d.get("step_change_claim", ""), "kind": "technology", "constrained": False,
                          "novelty": {"KNOWN": 1, "TWIST": 3, "NEW": 4}.get(str(d.get("novelty", "")).split()[0].upper().strip("[]"), 3),
                          "physics_risk": "medium", "source": "phaseB"})
    # Novelty top-up round (loaded LAST so existing ids I-00001..I-11597 stay stable)
    TOPRAW = DM / "research" / "ideas10k" / "topup" / "raw"
    for f in sorted(TOPRAW.glob("*.jsonl")) if TOPRAW.exists() else []:
        for i, ln in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            ln = ln.strip()
            if not ln:
                continue
            try:
                d = json.loads(ln)
            except json.JSONDecodeError:
                bad.append(f"topup/{f.name}:{i}")
                continue
            if not str(d.get("title", "")).strip() or not str(d.get("idea", "")).strip():
                continue
            d["cell"] = d.get("cell") or f.stem
            d["source"] = "topup"
            ideas.append(d)
    return ideas, bad


def main():
    ideas, bad = load()
    seen_title, keep, dups = {}, [], []
    for d in ideas:
        k = " ".join(norm(d["title"]))
        if k in seen_title:
            dups.append({**d, "dup_of_index": seen_title[k], "reason": "exact title"})
            continue
        seen_title[k] = len(keep)
        keep.append(d)
    sh = [shingles(norm(d["title"]) + norm(d["idea"])) for d in keep]
    sigs = np.stack([minhash(s) for s in sh]) if keep else np.zeros((0, PERMS), dtype=np.uint64)
    buckets = defaultdict(list)
    for i in range(len(keep)):
        for b in range(BANDS):
            buckets[(b, sigs[i, b * ROWS:(b + 1) * ROWS].tobytes())].append(i)
    removed = {}
    for idxs in buckets.values():
        if len(idxs) < 2:
            continue
        for x in range(len(idxs)):
            i = idxs[x]
            if i in removed:
                continue
            for y in range(x + 1, len(idxs)):
                j = idxs[y]
                if j in removed:
                    continue
                inter = len(sh[i] & sh[j])
                jac = inter / max(1, len(sh[i] | sh[j]))
                if jac >= THRESH:
                    removed[j] = (i, round(jac, 3))
    final = [d for i, d in enumerate(keep) if i not in removed]
    for j, (i, jac) in removed.items():
        dups.append({**keep[j], "dup_of_title": keep[i]["title"], "jaccard": jac, "reason": "near-duplicate"})
    for n, d in enumerate(final, 1):
        d["id"] = f"I-{n:05d}"
        c = str(d["cell"])
        d["technique"] = TECH.get(c[:3], "Phase B lens" if c.startswith("PHASE-B") else "")
        d["facet"] = FACET.get(c[4:7], "")
    with (OUT / "ideas_10k.jsonl").open("w", encoding="utf-8") as fh:
        for d in final:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    with (OUT / "duplicates.jsonl").open("w", encoding="utf-8") as fh:
        for d in dups:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    cols = ["id", "cell", "technique", "facet", "kind", "constrained", "novelty", "physics_risk", "title", "idea", "why", "source"]
    with (OUT / "ideas_10k.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(final)
    per_cell = Counter(d["cell"] for d in final)
    need = CFG["ideas_per_cell"]
    under = {c["cell"]: per_cell.get(c["cell"], 0) for c in CFG["cells"] if per_cell.get(c["cell"], 0) < int(need * 0.85)}
    stats = {"raw": len(ideas), "malformed": len(bad), "exact_dups": sum(1 for d in dups if d["reason"] == "exact title"),
             "near_dups": len(removed), "unique": len(final), "target": TARGET, "short_of_target": max(0, TARGET - len(final)),
             "by_technique": Counter(d["technique"] for d in final), "by_facet": Counter(d["facet"] for d in final),
             "by_kind": Counter(str(d.get("kind", "")) for d in final), "by_risk": Counter(str(d.get("physics_risk", "")) for d in final),
             "novelty_mean": round(sum(float(d.get("novelty") or 0) for d in final) / max(1, len(final)), 2),
             "cells_present": len(per_cell), "underfilled_cells": under, "malformed_lines": bad[:50]}
    (OUT / "stats.json").write_text(json.dumps(stats, indent=1, default=dict))
    print(f"raw {len(ideas)} | malformed {len(bad)} | exact dups {stats['exact_dups']} | near dups {len(removed)} | "
          f"UNIQUE {len(final)} (target {TARGET}) | cells {len(per_cell)}/250 | underfilled {len(under)}")


if __name__ == "__main__":
    main()
