#!/usr/bin/env python3
"""Build IDEAS_INDEX.md: a browsable index of the 10k-idea funnel.

Deterministic, stdlib only. Run from anywhere:

    python3 research/tools/build_ideas_index.py [output_path]

Reads (paths relative to the dram-moonshot root):
    research/ideas10k/ideas_10k.jsonl              every generated idea
    research/ideas10k/screen/scored_ideas.jsonl    screener scores (P, S, N, D, composite, flags, theme, dup_of)
    research/ideas10k/stage2/stage2_results.jsonl  two-lens Stage 2 critique (final, consensus, verdicts)
    research/stage3/FINAL_CONCEPTS.json            the 10 final concepts and the idea ids each one cites
Optional (used if present):
    research/phaseB/ideas_master.json              maps Phase B triage ids (N-xx) back to the Phase B seed cards
    research/ideas10k/screen/shortlist.jsonl, stage2_pool.jsonl, research/ideas10k/topup/best24.json
    research/ideas10k/ideas_10k.csv, research/ideas10k/screen/scored_ideas.csv  (header row only)

Writes IDEAS_INDEX.md at the dram-moonshot root (or the given path). Every count in the
output is computed here; nothing is hard-coded except definitions copied from
research/tools/screen_tools.py and research/tools/stage2_aggregate.py, and one fixed
red-team caveat in section 3 (taken from dossiers/<slug>.md section 11 and
research/redteam/responses_<slug>.json; the script does not read those files).
"""
import collections
import csv
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P_IDEAS = "research/ideas10k/ideas_10k.jsonl"
P_SCORED = "research/ideas10k/screen/scored_ideas.jsonl"
P_S2 = "research/ideas10k/stage2/stage2_results.jsonl"
P_FINAL = "research/stage3/FINAL_CONCEPTS.json"
P_PHASEB = "research/phaseB/ideas_master.json"
P_SHORT = "research/ideas10k/screen/shortlist.jsonl"
P_POOL = "research/ideas10k/screen/stage2_pool.jsonl"
P_BEST24 = "research/ideas10k/topup/best24.json"
P_IDEAS_CSV = "research/ideas10k/ideas_10k.csv"
P_SCORED_CSV = "research/ideas10k/screen/scored_ideas.csv"

NO_FACET = "(none: Phase B seed)"
VERDICTS = ("ADVANCE", "HOLD", "DROP")

COLUMN_DOC = {
    "id": "Idea id (`I-` plus five digits). Same id in every file.",
    "cell": "Generation cell: `Txx-Fyy` = technique xx x facet yy; `PHASE-B:<deck>` for Phase B seeds.",
    "n": "Position of the idea inside its cell (Phase B seeds keep their card id, e.g. `B1-04`).",
    "technique": "Creativity technique used to generate the idea.",
    "facet": "Problem facet (part of the DRAM problem) the idea targets. Empty for Phase B seeds.",
    "kind": "Generator's label: technology, material, process, architecture, system, strategy, policy or business.",
    "constrained": "True if the idea came from the second half of its cell, which had to obey a forced constraint.",
    "novelty": "Generator's own 1-5 novelty guess (not the screener's N).",
    "physics_risk": "Generator's own risk label: low, medium, high or speculative.",
    "title": "Short title (the brief asked for 12 words or fewer; some Phase B seed titles are longer).",
    "idea": "The mechanism or strategy (the brief asked for 1-3 sentences).",
    "why": "Which bottleneck it attacks and the gain the generator claimed.",
    "source": "`ideas10k` (main grid), `topup` (novelty top-up) or `phaseB` (Phase B seed cards).",
    "rank": "Rank by composite score (1 = best).",
    "composite": "Screener composite, 0-100 (formula below).",
    "batch_pct": "Percentile of the idea inside its screening batch (exposes lenient screeners).",
    "S": "Screener: step change if it works, 1-5.",
    "P": "Screener: physics or feasibility plausibility, 1-5.",
    "N": "Screener: novelty against known art, 1-5.",
    "D": "Screener: demo-ability with $1M in 24 months, 1-5.",
    "flags": "Comma list of BREAKTHROUGH, MOONSHOT, QUICKWIN (rules below). Empty for most ideas.",
    "theme": "Screener's 2-4 word mechanism family, e.g. `cryogenic dram`.",
    "note": "Screener note, 25 words or fewer; required when S>=4 or N>=5.",
    "dup_of": "Id of the earlier idea with the same core mechanism, or `EXISTING:<theme>` for top-up ideas that repeat an existing theme. Empty = distinct.",
    "batch": "Screening batch id.",
}


def load_jsonl(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_json(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def exists(rel):
    return os.path.exists(os.path.join(ROOT, rel))


def csv_header(rel):
    if not exists(rel):
        return []
    with open(os.path.join(ROOT, rel), encoding="utf-8", newline="") as fh:
        return next(csv.reader(fh), [])


def md(text, limit=None):
    """Make text safe for a Markdown table cell."""
    s = " ".join(str(text if text is not None else "").split())
    if limit and len(s) > limit:
        s = s[: limit - 3].rstrip() + "..."
    return s.replace("|", "\\|")


def fmt_int(n):
    return f"{n:,}"


def pct(num, den):
    return f"{100.0 * num / den:.1f}%" if den else "-"


def norm_theme(t):
    return " ".join(str(t or "").lower().split())


def facet_label(f):
    return f if f else NO_FACET


def bscore(d):
    """Breakthrough-weighted score used for the Top 50 table."""
    return 1.2 * d["S"] + 1.0 * d["N"] + 0.5 * d["P"] + 0.3 * d["D"]


def flag_set(d):
    return {f.strip() for f in str(d.get("flags", "")).split(",") if f.strip()}


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "IDEAS_INDEX.md")
    for rel in (P_IDEAS, P_SCORED, P_S2, P_FINAL):
        if not exists(rel):
            sys.exit(f"missing input: {rel}")

    ideas = load_jsonl(P_IDEAS)
    scored_rows = load_jsonl(P_SCORED)
    s2_rows = load_jsonl(P_S2)
    final = load_json(P_FINAL)

    idea_ids = [d["id"] for d in ideas]
    sc = {d["id"]: d for d in scored_rows}
    if len(set(idea_ids)) != len(idea_ids):
        sys.exit("duplicate ids in ideas_10k.jsonl")
    if set(idea_ids) != set(sc):
        sys.exit(f"id mismatch: ideas {len(idea_ids)} vs scored {len(sc)}")
    # records in id order; ideas file is the base, scored adds the screener fields
    recs = []
    for d in sorted(ideas, key=lambda x: x["id"]):
        r = dict(d)
        r.update(sc[d["id"]])
        recs.append(r)
    by_id = {r["id"]: r for r in recs}

    s2 = {d["id"]: d for d in s2_rows}
    missing_s2 = sorted(i for i in s2 if i not in by_id)
    if missing_s2:
        sys.exit(f"stage2 ids not in ideas file: {missing_s2[:5]}")

    # ---- final concepts: which ideas each one cites -------------------------
    concepts = sorted(final.get("concepts", []), key=lambda c: (c.get("rank", 99), c.get("slug", "")))
    # Phase B triage ids (N-xx) -> Phase B card ids (B1-04) -> I- ids via the `n` field of phaseB seeds
    n_to_cards = collections.defaultdict(list)
    have_phaseb_map = exists(P_PHASEB)
    if have_phaseb_map:
        meta = load_json(P_PHASEB).get("meta", {})
        for card, nid in sorted(meta.get("id_map", {}).items()):
            if card not in n_to_cards[nid]:
                n_to_cards[nid].append(card)
    card_to_iid = {str(r["n"]): r["id"] for r in recs if r.get("source") == "phaseB"}

    cited_by = collections.defaultdict(list)      # I- id -> [slug, ...] (concept rank order)
    cited_via = collections.defaultdict(set)      # I- id -> {N-xx} when reached through a Phase B triage id
    concept_rows = []
    all_direct, all_n, unresolved = set(), set(), set()
    for c in concepts:
        slug = c.get("slug", "")
        direct, nids, mapped = [], [], []
        for raw in c.get("idea_ids", []):
            if raw in by_id:
                direct.append(raw)
                if slug not in cited_by[raw]:
                    cited_by[raw].append(slug)
            elif raw.startswith("N-"):
                nids.append(raw)
                iids = [card_to_iid[b] for b in n_to_cards.get(raw, []) if b in card_to_iid]
                if not iids:
                    unresolved.add(raw)
                for iid in iids:
                    mapped.append(iid)
                    cited_via[iid].add(raw)
                    if slug not in cited_by[iid]:
                        cited_by[iid].append(slug)
            else:
                unresolved.add(raw)
        all_direct.update(direct)
        all_n.update(nids)
        ids_here = sorted(set(direct) | set(mapped))
        vc = collections.Counter(s2[i]["final"] if i in s2 else "not in Stage 2" for i in ids_here)
        concept_rows.append((c, direct, nids, ids_here, vc))
    cited = set(cited_by)

    # ---- helpers for group tables ---------------------------------------------
    def stats(rows):
        n = len(rows)
        dist = sum(1 for r in rows if not r["dup_of"])
        s4 = sum(1 for r in rows if r["S"] >= 4)
        n4 = sum(1 for r in rows if r["N"] >= 4)
        st2 = sum(1 for r in rows if r["id"] in s2)
        adv = sum(1 for r in rows if r["id"] in s2 and s2[r["id"]]["final"] == "ADVANCE")
        cit = sum(1 for r in rows if r["id"] in cited)
        mean_c = sum(r["composite"] for r in rows) / n if n else 0.0
        return {"n": n, "dist": dist, "s4": s4, "n4": n4, "st2": st2, "adv": adv, "cit": cit, "mean": mean_c}

    def group_table(key_fn, label):
        groups = collections.defaultdict(list)
        for r in recs:
            groups[key_fn(r)].append(r)
        rows = [(k, stats(v)) for k, v in groups.items()]
        rows.sort(key=lambda kv: (-kv[1]["adv"], -(kv[1]["s4"] / kv[1]["n"]), kv[0]))
        out = [f"| {label} | Ideas | Distinct | Mean composite | S≥4 (n, %) | N≥4 % | Reached Stage 2 | ADVANCE | Cited by a final concept |",
               "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for k, s in rows:
            out.append(f"| {md(k)} | {fmt_int(s['n'])} | {fmt_int(s['dist'])} | {s['mean']:.1f} | {s['s4']} ({pct(s['s4'], s['n'])}) | "
                       f"{pct(s['n4'], s['n'])} | {s['st2']} | {s['adv']} | {s['cit']} |")
        tot = stats(recs)
        out.append(f"| **All** | {fmt_int(tot['n'])} | {fmt_int(tot['dist'])} | {tot['mean']:.1f} | {tot['s4']} ({pct(tot['s4'], tot['n'])}) | "
                   f"{pct(tot['n4'], tot['n'])} | {tot['st2']} | {tot['adv']} | {tot['cit']} |")
        return out, rows

    def s2_verdict(i):
        return s2[i]["final"] if i in s2 else "-"

    # ---- funnel numbers ---------------------------------------------------------
    total = len(recs)
    src = collections.Counter(r["source"] for r in recs)
    cells = {s: len({r["cell"] for r in recs if r["source"] == s}) for s in src}
    techniques = sorted({r["technique"] for r in recs})
    facets_real = sorted({r["facet"] for r in recs if r["facet"]})
    dups = [r for r in recs if r["dup_of"]]
    dups_existing = sum(1 for r in dups if str(r["dup_of"]).startswith("EXISTING:"))
    dups_dangling = sum(1 for r in dups if not str(r["dup_of"]).startswith("EXISTING:") and r["dup_of"] not in by_id)
    distinct = [r for r in recs if not r["dup_of"]]
    flags = collections.Counter()
    for r in recs:
        for f in flag_set(r):
            flags[f] += 1
    verdict_counts = collections.Counter(d["final"] for d in s2.values())
    s2_src = collections.Counter(by_id[i]["source"] for i in s2)
    lens_pairs = collections.Counter(
        tuple(d.get("verdicts", {}).get(k, "?") for k in ("physics", "innovation")) for d in s2.values())
    agree = sum(v for (a, b), v in lens_pairs.items() if a == b)
    pool_rows = load_jsonl(P_POOL) if exists(P_POOL) else None
    pool_ids = {d["id"] for d in pool_rows} if pool_rows is not None else None
    short_ids = {d["id"] for d in load_jsonl(P_SHORT)} if exists(P_SHORT) else None
    tracks = collections.Counter(str(d.get("track", "")) for d in pool_rows) if pool_rows is not None else collections.Counter()
    best24 = load_json(P_BEST24) if exists(P_BEST24) else None
    best24_ids = None
    if isinstance(best24, list):
        best24_ids = {(b["id"] if isinstance(b, dict) else str(b)) for b in best24}
    adv_ids = sorted((i for i in s2 if s2[i]["final"] == "ADVANCE"), key=lambda i: (-s2[i]["consensus"], i))
    adv_cited = sum(1 for i in adv_ids if i in cited)
    cited_vc = collections.Counter(s2_verdict(i) for i in cited)

    # ---- choose examples for the one-liners from the data -------------------------
    ex_id = adv_ids[0] if adv_ids else recs[0]["id"]
    def shell_safe(x):
        return "'" not in x and '"' not in x and "\\" not in x

    ex_facet = next((by_id[i]["facet"] for i in adv_ids if by_id[i]["facet"] and shell_safe(by_id[i]["facet"])),
                    next(f for f in facets_real if shell_safe(f)))
    tech_adv = collections.Counter(by_id[i]["technique"] for i in adv_ids if shell_safe(by_id[i]["technique"]))
    ex_tech = (sorted(tech_adv.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if tech_adv
               else next(t for t in techniques if shell_safe(t)))
    ex_slug = concepts[0]["slug"] if concepts else ""
    ex_theme_word = "igzo"
    n_ex_facet = sum(1 for r in distinct if r["facet"] == ex_facet and r["S"] >= 4)
    n_ex_tech = sum(1 for r in recs if r["technique"] == ex_tech)
    n_moon = flags.get("MOONSHOT", 0)
    n_theme = sum(1 for r in recs if ex_theme_word in norm_theme(r["theme"]))
    tag_re = re.compile(r"\[(REPORTED-P|REPORTED|ESTIMATE|MODEL|UNVERIFIED)[^\]]*\]")
    tagged = [r for r in recs if any(tag_re.search(str(r.get(f, ""))) for f in ("title", "idea", "why", "note", "theme"))]
    tagged_src = sorted({r["source"] for r in tagged})

    L = []
    w = L.append
    w("# Ideas index")
    w("")
    w(f"*Generated by `research/tools/build_ideas_index.py` from the files it names. Do not edit by hand: re-run "
      f"`python3 research/tools/build_ideas_index.py`. Every count below is computed by the script.*")
    w("")
    w("Numbers in this file are counts and averages over the data files. The scores are judgments by screener and critic "
      "agents on 1-5 scales, not measurements. The scores, verdicts and counts carry no evidence tags. Only "
      f"{len(tagged)} idea rows (source: {', '.join(tagged_src) or 'none'}) carry tags such as [ESTIMATE] inside their own "
      "text. Idea titles, themes and notes are raw generator or screener text, so treat any untagged number inside them as "
      "[UNVERIFIED].")
    w("")
    w("Where files overlap, this index uses the later stage: Stage 2 verdicts come from `stage2_results.jsonl`, and concept "
      "membership comes from `FINAL_CONCEPTS.json`. It does not read the red-team or judge files. For how each final concept "
      "fared under attack, see `dossiers/<slug>.md` (section 11), `research/redteam/responses_<slug>.json` and "
      "`research/stage3/decision.json`.")
    w("")
    w("## Contents")
    w("")
    for i, t in enumerate(["What this is and how to browse", "Funnel counts", "Final concepts and the ideas they cite",
                           "By technique", "By facet", "By kind, and constrained against free", "The ADVANCE ideas",
                           "Top 50 by breakthrough score", "The wildest ideas", "Top 40 themes"], 1):
        w(f"{i}. {t}")
    w("")

    # 1. browse --------------------------------------------------------------------
    w("## 1. What this is and how to browse")
    w("")
    w(f"The idea funnel generated {fmt_int(total)} lexically unique ideas, screened all of them, critiqued the best "
      f"{len(s2)} in Stage 2 and built {len(concepts)} final concepts from the ADVANCE ideas and related ideas (section 3). "
      "This file is the map. "
      "The data lives in the files below. All paths are relative to the `dram-moonshot` folder.")
    w("")
    w("| File | Rows | What it holds |")
    w("|---|---:|---|")
    w(f"| `{P_IDEAS}` (and `.csv`) | {fmt_int(len(ideas))} | Every idea as generated, before scoring. |")
    w(f"| `{P_SCORED}` (and `.csv`) | {fmt_int(len(scored_rows))} | Every idea plus screener scores, flags, theme and duplicate link. **Start here.** |")
    w(f"| `{P_S2}` | {len(s2_rows)} | Stage 2 critique: final verdict, consensus, and each lens's scores, key insight, killer doubt, decisive experiment, prior art. |")
    if pool_ids is not None:
        w(f"| `{P_POOL}` | {len(pool_ids)} | Ideas sent to Stage 2 from the main screen. |")
    w(f"| `{P_FINAL}` | {len(concepts)} concepts | The final concepts. `idea_ids` lists the ideas each one cites. |")
    w("")
    w("**Columns.** The CSV headers are read from disk. JSONL rows hold the same fields, plus the ones marked JSONL only.")
    w("")
    hdr_ideas = csv_header(P_IDEAS_CSV)
    hdr_scored = csv_header(P_SCORED_CSV)
    jsonl_only = sorted(set(sc[recs[0]["id"]].keys()) - set(hdr_scored)) if hdr_scored else []
    order = list(dict.fromkeys(hdr_ideas + hdr_scored + jsonl_only)) or sorted(COLUMN_DOC)
    w("| Column | In ideas_10k | In scored_ideas | Meaning |")
    w("|---|:---:|:---:|---|")
    jsonl_ideas_keys = set(ideas[0].keys())
    for col in order:
        in_i = "csv+jsonl" if col in hdr_ideas else ("jsonl" if col in jsonl_ideas_keys else "")
        in_s = "csv+jsonl" if col in hdr_scored else ("jsonl" if col in sc[recs[0]["id"]] else "")
        w(f"| `{col}` | {in_i} | {in_s} | {md(COLUMN_DOC.get(col, '(not documented)'))} |")
    w("")
    w("**Score definitions** (from `research/ideas10k/SCREEN_RUBRIC.md` and `research/tools/screen_tools.py`):")
    w("")
    w("- **P, S, N, D** are 1-5 screener scores: P = physics plausibility, S = step change if it works, N = novelty, "
      "D = demo-ability with $1M in 24 months. Most ideas score 2-3; 5s were meant to be rare.")
    w("- **composite** = (S + 0.8·P + 0.6·N + 0.6·D) / 15, scaled to 0-100.")
    w("- **Flags.** BREAKTHROUGH = S=5 and P≥3. MOONSHOT = S=5, N≥4 and P≥2. QUICKWIN = D≥4, P≥4 and S≥3.")
    w("- **Distinct** = an idea the screener did not mark as a same-mechanism duplicate (empty `dup_of`).")
    w("- **Stage 2** = two independent critic lenses, physics and innovation, each re-scored the idea (P2, S2, N2, D2) and "
      "voted ADVANCE, HOLD or DROP. **consensus** = mean over the two lenses of (1.2·S2 + 1.0·N2 + 0.7·P2 + 0.5·D2) / 17, "
      "scaled to 0-100. Final verdict (`research/tools/stage2_aggregate.py`): ADVANCE if both lenses say ADVANCE, or one "
      "ADVANCE plus one HOLD with consensus ≥70. DROP if both say DROP, or the physics lens says DROP with P2 ≤2. "
      "Otherwise HOLD.")
    w("- **Breakthrough score** (this index only) = 1.2·S + 1.0·N + 0.5·P + 0.3·D. It weights step size and novelty above "
      "feasibility.")
    w("")
    w("**Copy-paste one-liners.** Run them from the `dram-moonshot` folder. The row counts are today's.")
    w("")
    w(f"1. Distinct ideas with S≥4 in one facet ({n_ex_facet} rows for \"{ex_facet}\"):")
    w("")
    w("   ```sh")
    w(f"   python3 -c 'import json; [print(d[\"id\"], d[\"S\"], d[\"P\"], d[\"N\"], d[\"D\"], d[\"title\"]) for d in map(json.loads, open(\"{P_SCORED}\")) if d[\"facet\"]==\"{ex_facet}\" and d[\"S\"]>=4 and not d[\"dup_of\"]]'")
    w("   ```")
    w("")
    w(f"2. All ideas from one technique, best composite first ({n_ex_tech} rows for \"{ex_tech}\"):")
    w("")
    w("   ```sh")
    w(f"   python3 -c 'import json; r=[d for d in map(json.loads, open(\"{P_SCORED}\")) if d[\"technique\"]==\"{ex_tech}\"]; [print(d[\"id\"], d[\"composite\"], d[\"title\"]) for d in sorted(r, key=lambda d: (-d[\"composite\"], d[\"id\"]))]'")
    w("   ```")
    w("")
    w(f"3. Look up one id: its screen record, then its Stage 2 verdict and both killer doubts (example {ex_id}):")
    w("")
    w("   ```sh")
    w(f"   jq -c 'select(.id==\"{ex_id}\")' {P_SCORED}")
    w(f"   jq -r 'select(.id==\"{ex_id}\") | .final, .consensus, .physics.killer_doubt, .innovation.killer_doubt' {P_S2}")
    w("   ```")
    w("")
    w(f"4. Every MOONSHOT-flagged idea as tab-separated rows ({n_moon} rows):")
    w("")
    w("   ```sh")
    w(f"   jq -r 'select(.flags | test(\"MOONSHOT\")) | [.id, .S, .P, .N, .D, .title] | @tsv' {P_SCORED}")
    w("   ```")
    w("")
    w(f"5. The ideas one final concept cites (example `{ex_slug}`; `N-xx` ids are Phase B triage ids, see section 3):")
    w("")
    w("   ```sh")
    w(f"   jq -r '.concepts[] | select(.slug==\"{ex_slug}\") | .idea_ids[]' {P_FINAL}")
    w("   ```")
    w("")
    w(f"6. Search themes for a word ({n_theme} rows contain \"{ex_theme_word}\"):")
    w("")
    w("   ```sh")
    w(f"   python3 -c 'import json; [print(d[\"id\"], d[\"composite\"], d[\"theme\"], \"|\", d[\"title\"]) for d in map(json.loads, open(\"{P_SCORED}\")) if \"{ex_theme_word}\" in d[\"theme\"].lower()]'")
    w("   ```")
    w("")

    # 2. funnel ----------------------------------------------------------------------
    w("## 2. Funnel counts")
    w("")
    w("| Step | Count | Detail |")
    w("|---|---:|---|")
    src_detail = "; ".join(f"{s}: {fmt_int(src[s])} from {cells[s]} cells" for s in sorted(src, key=lambda s: -src[s]))
    w(f"| Lexically unique ideas generated | {fmt_int(total)} | {md(src_detail)}. {len(techniques)} technique labels, "
      f"{len(facets_real)} facets plus the facet-less Phase B seeds. |")
    w(f"| Screened | {fmt_int(len(scored_rows))} | Every idea scored on P, S, N, D. |")
    w(f"| Screener-flagged duplicates | {fmt_int(len(dups))} | Same core mechanism as an earlier idea. {dups_existing} of them "
      f"point at an existing theme (`EXISTING:`) rather than an id; {dups_dangling} point at an id not in the file. |")
    w(f"| Distinct ideas | {fmt_int(len(distinct))} | Total minus duplicates. |")
    for f in ("BREAKTHROUGH", "MOONSHOT", "QUICKWIN"):
        w(f"| Flag: {f} | {fmt_int(flags.get(f, 0))} | Rule in section 1. |")
    if short_ids is not None:
        w(f"| Shortlist | {len(short_ids)} | Top distinct ideas by composite with a per-facet floor (`shortlist.jsonl`). |")
    if pool_ids is not None:
        comp_n = tracks.get("composite", 0) + tracks.get("both", 0)
        brk_n = tracks.get("breakthrough", 0) + tracks.get("both", 0)
        w(f"| Stage 2 pool from the main screen | {len(pool_ids)} | `stage2_pool.jsonl`. Its `track` field: composite track "
          f"{comp_n}, breakthrough track {brk_n}, {tracks.get('both', 0)} on both. |")
    if best24_ids is not None:
        w(f"| Best top-up ideas added | {len(best24_ids)} | `topup/best24.json`. |")
    w(f"| Critiqued in Stage 2 | {len(s2)} | By source: " + ", ".join(f"{s} {s2_src[s]}" for s in sorted(s2_src, key=lambda s: -s2_src[s]))
      + f". The two lenses gave the same verdict on {agree} of {len(s2)}. |")
    for v in VERDICTS:
        w(f"| Stage 2 {v} | {verdict_counts.get(v, 0)} | {pct(verdict_counts.get(v, 0), len(s2))} of Stage 2. |")
    w(f"| Final concepts | {len(concepts)} | `FINAL_CONCEPTS.json`. |")
    w(f"| Ideas cited by final concepts | {len(cited)} | {len(all_direct)} cited directly by id, plus {len(cited) - len(all_direct)} "
      f"more reached through {len(all_n)} Phase B triage ids (`N-xx`). Their Stage 2 verdicts: "
      + ", ".join(f"{k} {cited_vc[k]}" for k in list(VERDICTS) + ["-"] if cited_vc.get(k))
      + " (`-` = never reached Stage 2). |")
    w(f"| ADVANCE ideas used by a final concept | {adv_cited} of {len(adv_ids)} | |")
    w("")
    w("Lens pairs in Stage 2 (physics verdict, innovation verdict):")
    w("")
    w("| Physics | Innovation | Ideas |")
    w("|---|---|---:|")
    for (a, b), v in sorted(lens_pairs.items(), key=lambda kv: (-kv[1], kv[0])):
        w(f"| {a} | {b} | {v} |")
    w("")
    if pool_ids is not None and best24_ids is not None:
        union = pool_ids | best24_ids
        w(f"Check: Stage 2 pool ({len(pool_ids)}) + top-up best ({len(best24_ids)}) = {len(union)} unique ids; "
          f"{len(union & set(s2))} of them appear in `stage2_results.jsonl`.")
        w("")
    if short_ids is not None and pool_rows is not None:
        comp_ids = {d["id"] for d in pool_rows if d.get("track") in ("composite", "both")}
        extra = short_ids - comp_ids
        extra_src = collections.Counter(by_id[i]["source"] for i in extra if i in by_id)
        if extra:
            src_txt = (f"all `{next(iter(extra_src))}` ideas" if len(extra_src) == 1
                       else "ideas from sources " + ", ".join(f"`{k}` ({v})" for k, v in sorted(extra_src.items())))
            w(f"Note: `shortlist.jsonl` as it is on disk shares {len(short_ids & comp_ids)} ids with the pool's composite track. "
              f"The other {len(extra)} shortlist ids are {src_txt}; {len(extra & set(s2))} of those reached Stage 2 through "
              "`topup/best24.json`. This index takes "
              "Stage 2 membership from `stage2_results.jsonl`, not from the shortlist.")
            w("")

    # 3. concepts --------------------------------------------------------------------
    w("## 3. Final concepts and the ideas they cite")
    w("")
    w("Each final concept lists source ids in `idea_ids`. `I-` ids are rows in the idea files. `N-` ids are Phase B triage "
      "ids from `research/phaseB/ideas_master.json`; the script maps each one back to its Phase B seed card (the `n` field, "
      "e.g. `B1-04`) and so to an `I-` id. Where triage merged two cards into one `N-` id, both cards count as cited.")
    w("")
    w("**Cited is not the same as survived.** `FINAL_CONCEPTS.json` was written before the physics red team. The red team "
      "then marked all 10 concepts DOWNGRADED (none killed) and killed some named legs that rest on cited ideas: the "
      "single all-layer latent (I-04878) in `ai-memory-diet` (RT-CIRC-ai-memory-diet-02), the per-read sense-amp flag "
      "interface (I-11148) in `raw-ber-contract` (RT-CIRC-raw-ber-contract-01 and -02), and the AAO capacitor at the 35 nm "
      "1-beta pitch (N-21) in `lean-array-module` (RT-CIRC-lean-array-module-02). For what each concept still claims, "
      "see `dossiers/<slug>.md` section 11.")
    w("")
    w("| Rank | Slug | Ids listed | I- ids | N- ids | Ideas cited (after mapping) | ADVANCE | HOLD | DROP | Not in Stage 2 |")
    w("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for c, direct, nids, ids_here, vc in concept_rows:
        w(f"| {c.get('rank', '')} | `{c.get('slug', '')}` | {len(c.get('idea_ids', []))} | {len(direct)} | {len(nids)} | {len(ids_here)} | "
          f"{vc.get('ADVANCE', 0)} | {vc.get('HOLD', 0)} | {vc.get('DROP', 0)} | {vc.get('not in Stage 2', 0)} |")
    w("")
    if unresolved:
        w(f"Ids the script could not map to an idea row: {', '.join(sorted(unresolved))}.")
        w("")
    if not have_phaseb_map:
        w("`research/phaseB/ideas_master.json` was missing, so `N-` ids were not mapped.")
        w("")

    # 4/5. technique and facet tables ------------------------------------------------
    w("## 4. By technique")
    w("")
    w("Sorted by ADVANCE count, then by S≥4 rate. S≥4, N≥4 and mean composite are over all ideas in the row, duplicates "
      "included. \"Cited by a final concept\" counts ideas cited directly or through an `N-` id.")
    w("")
    tbl, _ = group_table(lambda r: r["technique"], "Technique")
    L.extend(tbl)
    w("")
    pb_direct = sum(1 for i in all_direct if by_id[i]["source"] == "phaseB")
    pb_all = sum(1 for i in cited if by_id[i]["source"] == "phaseB")
    w(f"Counting only ids listed directly in `idea_ids` (no `N-` mapping), {len(all_direct)} ideas are cited, and Phase B lens "
      f"has {pb_direct} instead of {pb_all}. `research/stage3/TECHNIQUE_PERFORMANCE.md` reports the direct-only figure.")
    w("")
    w("## 5. By facet")
    w("")
    w("Same columns and sort as section 4.")
    w("")
    tbl, _ = group_table(lambda r: facet_label(r["facet"]), "Facet")
    L.extend(tbl)
    w("")

    # 6. kind and constrained -----------------------------------------------------------
    w("## 6. By kind, and constrained against free")
    w("")
    w("`kind` is the generator's own label. Same columns and sort as section 4.")
    w("")
    tbl, _ = group_table(lambda r: r["kind"], "Kind")
    L.extend(tbl)
    w("")
    w("In each generation cell, the first half of the ideas was free and the second half had to obey a forced constraint "
      "(`constrained` = true). Phase B seed cards were never split, and the file stores them as `constrained` = false, "
      "so the table shows the free half with and without them.")
    w("")
    groups = [
        ("Free, all (field = false)", [r for r in recs if not r["constrained"]]),
        ("Free, excluding Phase B seeds", [r for r in recs if not r["constrained"] and r["source"] != "phaseB"]),
        ("Phase B seeds (no split)", [r for r in recs if r["source"] == "phaseB"]),
        ("Constrained (field = true)", [r for r in recs if r["constrained"]]),
    ]
    w("| Half | Ideas | Distinct | Mean composite | S≥4 (n, %) | N≥4 % | Reached Stage 2 | ADVANCE | Cited by a final concept |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    cvf = {}
    for name, rows in groups:
        s = stats(rows)
        cvf[name] = s
        w(f"| {name} | {fmt_int(s['n'])} | {fmt_int(s['dist'])} | {s['mean']:.1f} | {s['s4']} ({pct(s['s4'], s['n'])}) | "
          f"{pct(s['n4'], s['n'])} | {s['st2']} | {s['adv']} | {s['cit']} |")
    w("")

    # 7. ADVANCE ------------------------------------------------------------------------
    w(f"## 7. The {len(adv_ids)} ADVANCE ideas")
    w("")
    w("Sorted by Stage 2 consensus. \"Used by\" lists the final concepts that cite the idea (rank order), as listed before "
      "the red team (see the caveat in section 3).")
    w("")
    w("| # | Id | Consensus | Title | Technique | Facet | Used by |")
    w("|---:|---|---:|---|---|---|---|")
    for k, i in enumerate(adv_ids, 1):
        r = by_id[i]
        used = ", ".join(f"`{s}`" for s in cited_by.get(i, [])) or "none"
        w(f"| {k} | {i} | {s2[i]['consensus']} | {md(r['title'])} | {md(r['technique'])} | {md(facet_label(r['facet']))} | {used} |")
    w("")

    # 8. Top 50 by breakthrough ------------------------------------------------------------
    top = sorted(distinct, key=lambda r: (-round(bscore(r), 6), -r["composite"], r["id"]))[:50]
    w("## 8. Top 50 by breakthrough score")
    w("")
    w("Distinct ideas only. Score = 1.2·S + 1.0·N + 0.5·P + 0.3·D (maximum 15). Ties go to the higher composite, then the "
      "lower id. \"Stage 2\" is the final Stage 2 verdict (`-` = not critiqued). This score is this index's own; it is not "
      "the `breakthrough` field stored in `stage2_pool.jsonl`.")
    w("")
    w("| # | Id | Score | S/P/N/D | Stage 2 | Title | Theme |")
    w("|---:|---|---:|---|---|---|---|")
    for k, r in enumerate(top, 1):
        w(f"| {k} | {r['id']} | {bscore(r):.1f} | {r['S']}/{r['P']}/{r['N']}/{r['D']} | {s2_verdict(r['id'])} | "
          f"{md(r['title'])} | {md(norm_theme(r['theme']))} |")
    w("")

    # 9. wildest -------------------------------------------------------------------------
    w("## 9. The wildest ideas")
    w("")
    wild = [r for r in distinct if r["S"] == 5 and r["N"] == 5]
    s5_all = sum(1 for r in recs if r["S"] == 5)
    n5_all = sum(1 for r in recs if r["N"] == 5)
    if wild:
        rule = "S=5 and N=5"
        w(f"Distinct ideas with S=5 and N=5: {len(wild)}.")
    else:
        top_sn = max(r["S"] + r["N"] for r in distinct)
        wild = [r for r in distinct if r["S"] + r["N"] >= top_sn]
        rule = f"S+N ≥ {top_sn}"
        w(f"No idea scored S=5 and N=5. Screeners gave S=5 to only {s5_all} ideas and N=5 to only {n5_all}, out of "
          f"{fmt_int(total)}. So this section shows the highest band that exists: distinct ideas with S+N ≥ {top_sn} "
          f"({len(wild)} ideas).")
    w("")
    wild.sort(key=lambda r: (-r["P"], -round(bscore(r), 6), -r["composite"], r["id"]))
    omitted = max(0, len(wild) - 60)
    if omitted:
        w(f"{omitted} more ideas meet the rule ({rule}) but are omitted here; the cap is 60, sorted by P.")
        w("")
    w(f"Rule: {rule}. Sorted by P (highest first), then breakthrough score.")
    w("")
    w("| # | Id | S/P/N/D | Stage 2 | Technique | Title | Screener note |")
    w("|---:|---|---|---|---|---|---|")
    for k, r in enumerate(wild[:60], 1):
        w(f"| {k} | {r['id']} | {r['S']}/{r['P']}/{r['N']}/{r['D']} | {s2_verdict(r['id'])} | {md(r['technique'])} | "
          f"{md(r['title'])} | {md(r.get('note', ''), 180)} |")
    w("")

    # 10. themes ---------------------------------------------------------------------------
    th_all = collections.Counter(norm_theme(r["theme"]) for r in recs if norm_theme(r["theme"]))
    th_dist = collections.Counter(norm_theme(r["theme"]) for r in distinct)
    th_s2 = collections.Counter(norm_theme(by_id[i]["theme"]) for i in s2)
    th_adv = collections.Counter(norm_theme(by_id[i]["theme"]) for i in adv_ids)
    th_best = {}
    for r in recs:
        t = norm_theme(r["theme"])
        th_best[t] = max(th_best.get(t, 0.0), r["composite"])
    w("## 10. Top 40 themes")
    w("")
    w(f"Themes are the screener's 2-4 word mechanism labels, lower-cased with spaces collapsed. There are {fmt_int(len(th_all))} "
      f"different themes, so near-synonyms (for example \"dimm reuse market\" and \"dimm reuse cxl\") stay separate. Counts include "
      "duplicates; \"Distinct\" excludes them.")
    w("")
    w("| # | Theme | Ideas | Distinct | Reached Stage 2 | ADVANCE | Best composite |")
    w("|---:|---|---:|---:|---:|---:|---:|")
    for k, (t, n) in enumerate(sorted(th_all.items(), key=lambda kv: (-kv[1], kv[0]))[:40], 1):
        w(f"| {k} | {md(t)} | {n} | {th_dist.get(t, 0)} | {th_s2.get(t, 0)} | {th_adv.get(t, 0)} | {th_best[t]:.1f} |")
    w("")

    text = "\n".join(L) + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    # console summary (for checking)
    print(f"wrote {os.path.relpath(out_path, ROOT)} ({len(text.encode('utf-8')):,} bytes)")
    print(f"total {total}; duplicates {len(dups)}; distinct {len(distinct)}; flags "
          + ", ".join(f"{f} {flags.get(f, 0)}" for f in ("BREAKTHROUGH", "MOONSHOT", "QUICKWIN")))
    print(f"stage2 {len(s2)}; " + ", ".join(f"{v} {verdict_counts.get(v, 0)}" for v in VERDICTS))
    print(f"cited by final concepts {len(cited)} (direct {len(all_direct)}, N-ids {len(all_n)}); ADVANCE used {adv_cited}/{len(adv_ids)}")
    for name, s in cvf.items():
        print(f"{name}: n {s['n']}, S>=4 {s['s4']} ({pct(s['s4'], s['n'])}), N>=4 {pct(s['n4'], s['n'])}, "
              f"stage2 {s['st2']}, ADVANCE {s['adv']}, cited {s['cit']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
