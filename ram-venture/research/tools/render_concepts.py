#!/usr/bin/env python3
"""Render research/phase2/concepts_master.json -> 02_CONCEPTS.md and concepts.csv.

The master file is {"cards": [...]} where each card follows research/CONCEPT_SCHEMA.md
plus: "id" (C-NN), optional "merged_from" (list of tmp_ids), optional "status"
(ALIVE|KILLED), optional "kill_reason", optional "kill_rule".
"""
import csv
import json
import sys
from pathlib import Path

RV = Path(__file__).resolve().parents[2]
MASTER = RV / "research" / "phase2" / "concepts_master.json"
MD = RV / "02_CONCEPTS.md"
CSV = RV / "concepts.csv"

BRANCH_NAMES = {
    "A": "A. Device & materials",
    "B": "B. Architecture & systems",
    "C": "C. Manufacturing & supply chain (U.S.)",
    "D": "D. Software & virtual RAM",
    "E": "E. Business-model-first concepts",
}

CSV_FIELDS = ["id", "name", "branch", "subbranch", "materials_sense", "trl", "capital_tier",
              "time_to_first_revenue_months", "gross_margin_mid_pct", "survives_glut", "rule1_status",
              "status", "kill_rule", "kill_reason", "wins_axis", "buyer", "us_manufacturability",
              "who_is_already_doing_this", "fatal_flaw", "possible", "profitable", "doable_by_founder",
              "evidence_urls", "merged_from"]


def ev_lines(card):
    out = []
    for e in card.get("evidence", []) or []:
        t = e.get("title", "source")
        u = e.get("url", "")
        typ = e.get("type", "")
        d = e.get("date", "")
        shows = e.get("shows", "")
        out.append(f"  - [{t}]({u}) — {typ}, {d}. {shows}".rstrip())
    return out or ["  - (none — UNSUPPORTED)"]


def main():
    data = json.loads(MASTER.read_text(encoding="utf-8"))
    cards = data["cards"]
    ids = [c["id"] for c in cards]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate ids in master")

    alive = sum(1 for c in cards if c.get("status", "ALIVE") != "KILLED")

    # Rule 5 coverage (materials sense), computed from the master so the legend never drifts from the data.
    def senses(c):
        ms = str(c.get("materials_sense", "")).strip().lower()
        if ms.startswith("mixed:"):
            return set(ms.split(":", 1)[1].split("+"))
        return {ms[0]} if ms[:1] in ("a", "b", "c") else set()

    def surv_list(s):
        ids = [c["id"] for c in cards if c.get("status", "ALIVE") != "KILLED" and s in senses(c)]
        if len(ids) == 1:
            ms = str(next(c for c in cards if c["id"] == ids[0]).get("materials_sense", ""))
            return f"{ids[0]} only" + (f" ({ms.split(':', 1)[1]})" if ms.startswith("mixed:") else "")
        return ", ".join(ids) or "none"

    n_sense = {s: sum(1 for c in cards if s in senses(c)) for s in ("a", "b", "c")}
    n_none = sum(1 for c in cards if not senses(c))
    rule5 = (" Rule 5 coverage (counted from `research/phase2/concepts_master.json`, mixed cards counted under each "
             f"sense they touch): **(a) {n_sense['a']} cards**, **(b) {n_sense['b']} cards**, **(c) {n_sense['c']} cards**, "
             f"{n_none} cards with no materials sense (pure software/service). Survivors: (a) {surv_list('a')}, "
             f"(b) {surv_list('b')}, (c) {surv_list('c')}.")
    lines = [
        "# 02 — CONCEPTS",
        "",
        f"**{len(cards)} concept cards** generated in Phase 2 by parallel ideation agents (one per branch A–E; branch A split "
        "three ways because it is the largest), then deduplicated. Merges are noted on each card. "
        f"Current status (after the Phase 3 kill pass and scoring, both Phase 5 red-team rounds, and the Phase 7 gate): **{alive} alive, {len(cards) - alive} killed**; each killed card shows its rule and reason. "
        "Scores are in `03_SCORING.md`. The machine-readable copy is `concepts.csv`. Device $/GB comparisons are in "
        "`models/device_cost_compare.py`.",
        "",
        "Legend: TRL = technology readiness level 1–9 · Tier T0 <$50k, T1 $50k–$2M, T2 $2M–$50M, T3 $50M–$1B, T4 >$1B · "
        "materials sense: (a) material system, (b) process, (c) capital (mission rule 5)." + rule5,
        "",
    ]
    if data.get("dedup_notes"):
        lines += ["## Deduplication log", ""] + [f"- {n}" for n in data["dedup_notes"]] + [""]

    for b in ["A", "B", "C", "D", "E"]:
        group = [c for c in cards if c.get("branch") == b]
        if not group:
            continue
        lines += [f"## {BRANCH_NAMES[b]} ({len(group)} cards)", ""]
        for c in group:
            status = c.get("status", "ALIVE")
            tag = f" — ☠ KILLED ({c.get('kill_rule', '')}: {c.get('kill_reason', '')})" if status == "KILLED" else ""
            lines += [f"### {c['id']} — {c['name']}{tag}", ""]
            lines.append(f"*Sub-branch:* {c.get('subbranch', '')} · *Materials sense:* {c.get('materials_sense', '')}"
                         + (f" · *Merged from:* {', '.join(c['merged_from'])}" if c.get("merged_from") else ""))
            lines.append("")
            lines.append(f"**What it is:** {c.get('what_it_is', '')}")
            lines.append("")
            lines.append(f"**Why it could work:** {c.get('why_it_could_work', '')}")
            lines.append("")
            lines.append(f"**Evidence:** TRL {c.get('trl', '?')} · Rule 1: {c.get('rule1_status', '?')}")
            lines += ev_lines(c)
            lines.append("")
            lines.append(f"**Capital tier:** {c.get('capital_tier', '?')} | **Time to first revenue:** "
                         f"{c.get('time_to_first_revenue_text', c.get('time_to_first_revenue_months', '?'))} | "
                         f"**Gross margin estimate:** {c.get('gross_margin_estimate', '?')}")
            lines.append("")
            lines.append(f"**US manufacturability:** {c.get('us_manufacturability', '')}")
            lines.append("")
            lines.append(f"**Who is already doing this:** {c.get('who_is_already_doing_this', '')}")
            lines.append("")
            lines.append(f"**Wins on which axis, for which buyer:** {c.get('wins_axis', '')} — for {c.get('buyer', '')}")
            lines.append("")
            lines.append(f"**Survives a 2029 glut?:** {c.get('survives_glut', '?')} — {c.get('glut_reason', '')}")
            lines.append("")
            lines.append(f"**Fatal-flaw candidate:** {c.get('fatal_flaw', '')}")
            lines.append("")
            lines.append(f"*Possible?* {c.get('possible', '')} · *Profitable?* {c.get('profitable', '')} · "
                         f"*Doable by this founder?* {c.get('doable_by_founder', '')}")
            if c.get("business_model_lenses"):
                lines.append("")
                lines.append(f"*Business-model lenses:* {c['business_model_lenses']}")
            lines.append("")
    MD.write_text("\n".join(lines), encoding="utf-8")

    with CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS, extrasaction="ignore")
        w.writeheader()
        for c in cards:
            row = {k: c.get(k, "") for k in CSV_FIELDS}
            row["status"] = c.get("status", "ALIVE")
            row["evidence_urls"] = " ".join(e.get("url", "") for e in c.get("evidence", []) or [])
            row["merged_from"] = " ".join(c.get("merged_from", []) or [])
            w.writerow(row)
    print(f"rendered {len(cards)} cards ({alive} alive) -> 02_CONCEPTS.md, concepts.csv")


if __name__ == "__main__":
    main()
