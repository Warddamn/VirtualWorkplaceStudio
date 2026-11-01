#!/usr/bin/env python3
"""Build research/phase2/concepts_master.json from per-branch ideation files.

  python3 research/tools/build_master.py --compact   # write compact_list.md for the dedup reviewer
  python3 research/tools/build_master.py             # apply dedup_map.json (if any), assign C-NN ids

dedup_map.json format:
  {"merges": [{"keep": "A1-03", "absorb": ["E-05"], "note": "same IGZO idea"}],
   "notes": ["free-text dedup notes"]}
Absorbed cards' evidence is appended to the kept card (deduplicated by URL); merged_from records lineage.
"""
import json
import re
import sys
from pathlib import Path

RV = Path(__file__).resolve().parents[2]
P2 = RV / "research" / "phase2"
BRANCH_FILE_RE = re.compile(r"^[A-E]\d?\.json$")
ORDER = ["A1", "A2", "A3", "B", "C", "D", "E"]


def load_cards():
    cards = []
    files = sorted((f for f in P2.glob("*.json") if BRANCH_FILE_RE.match(f.name)),
                   key=lambda f: ORDER.index(f.stem) if f.stem in ORDER else 99)
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        for c in data.get("cards", []):
            c = dict(c)
            c["branch"] = f.stem[0]
            c["_file"] = f.stem
            cards.append(c)
    return cards


def compact(cards):
    out = ["# Compact concept list for deduplication", "",
           f"{len(cards)} raw cards. Columns: tmp_id | name | sub-branch | tier | TRL | what it is | axis → buyer", ""]
    for c in cards:
        what = re.sub(r"\s+", " ", str(c.get("what_it_is", "")))[:320]
        out.append(f"- **{c.get('tmp_id')}** | {c.get('name')} | {c.get('subbranch', '')} | {c.get('capital_tier', '')} | "
                   f"TRL {c.get('trl', '?')} | {what} | {c.get('wins_axis', '')} → {c.get('buyer', '')}")
    (P2 / "compact_list.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"compact_list.md: {len(cards)} cards")


def build(cards):
    by_tmp = {c["tmp_id"]: c for c in cards}
    if len(by_tmp) != len(cards):
        dups = sorted({c["tmp_id"] for c in cards if sum(1 for d in cards if d["tmp_id"] == c["tmp_id"]) > 1})
        sys.exit(f"duplicate tmp_ids across files: {dups}")
    dmap_path = P2 / "dedup_map.json"
    dmap = json.loads(dmap_path.read_text(encoding="utf-8")) if dmap_path.exists() else {"merges": [], "notes": []}
    absorbed = set()
    notes = list(dmap.get("notes", []))
    for m in dmap.get("merges", []):
        keep = by_tmp.get(m["keep"])
        if keep is None:
            sys.exit(f"dedup_map keep id not found: {m['keep']}")
        lineage = [m["keep"]]
        seen_urls = {e.get("url") for e in keep.get("evidence", []) or []}
        for t in m.get("absorb", []):
            other = by_tmp.get(t)
            if other is None:
                sys.exit(f"dedup_map absorb id not found: {t}")
            if t in absorbed:
                sys.exit(f"{t} absorbed twice")
            absorbed.add(t)
            lineage.append(t)
            for e in other.get("evidence", []) or []:
                if e.get("url") not in seen_urls:
                    keep.setdefault("evidence", []).append(e)
                    seen_urls.add(e.get("url"))
        keep["merged_from"] = lineage
        notes.append(f"{' + '.join(lineage)} → kept {m['keep']} ({keep.get('name')}): {m.get('note', '')}")
    kept = [c for c in cards if c["tmp_id"] not in absorbed]
    width = 2 if len(kept) < 100 else 3
    tmp_to_id = {}
    for i, c in enumerate(kept, 1):
        c["id"] = f"C-{i:0{width}d}"
        tmp_to_id[c["tmp_id"]] = c["id"]
        c.setdefault("status", "ALIVE")
        c.pop("_file", None)
    for t in absorbed:
        # map absorbed ids to their keeper's final id
        for m in dmap.get("merges", []):
            if t in m.get("absorb", []):
                tmp_to_id[t] = tmp_to_id[m["keep"]]
    # Rewrite working-id cross-references (e.g. "Unlike C-04") inside card text to final ids, and show
    # lineage in dotted form (C.07) so it can't be confused with final ids (C-07).
    ref_re = re.compile(r"\b(A1|A2|A3|B|C|D|E)-(\d{2})\b")
    dot = lambda t: ref_re.sub(lambda m: f"{m.group(1)}.{m.group(2)}", t)
    for c in kept:
        for k, v in list(c.items()):
            if isinstance(v, str) and k not in ("tmp_id", "id"):
                c[k] = ref_re.sub(lambda m: tmp_to_id.get(f"{m.group(1)}-{m.group(2)}", m.group(0)), v)
        c["tmp_id"] = dot(c["tmp_id"])
        if c.get("merged_from"):
            c["merged_from"] = [dot(t) for t in c["merged_from"]]
    notes = [ref_re.sub(lambda m: f"{tmp_to_id.get(m.group(1) + '-' + m.group(2), '?')} (working id {m.group(1)}.{m.group(2)})", n)
             for n in notes]
    master = {"generated_by": "research/tools/build_master.py", "raw_cards": len(cards), "absorbed": len(absorbed),
              "dedup_notes": notes, "cards": kept}
    (P2 / "concepts_master.json").write_text(json.dumps(master, indent=1, ensure_ascii=False), encoding="utf-8")
    (P2 / "tmp_to_id.json").write_text(json.dumps(tmp_to_id, indent=1), encoding="utf-8")
    print(f"concepts_master.json: {len(cards)} raw → {len(kept)} cards ({len(absorbed)} absorbed by dedup)")


def main():
    cards = load_cards()
    if not cards:
        sys.exit("no branch files found in research/phase2/")
    if "--compact" in sys.argv:
        compact(cards)
    else:
        build(cards)


if __name__ == "__main__":
    main()
