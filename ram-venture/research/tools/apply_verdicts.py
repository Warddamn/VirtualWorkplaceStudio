#!/usr/bin/env python3
"""Apply Phase 3 kill/verify verdicts (research/phase3/verify/*.json) to concepts_master.json, then re-render.

Verify file format: {"batch": "01", "verdicts": [{"id": "C-07", "verdict": "KEEP|KEEP_WITH_CORRECTIONS|KILL",
   "kill_rule": "...", "reason": "...", "corrections": [{"field": "trl", "new_value": 4, "why": "..."}],
   "new_evidence": [{"title":..., "url":..., "type":..., "date":..., "shows":...}], "evidence_check": [...]}]}
"""
import json
import subprocess
import sys
from pathlib import Path

RV = Path(__file__).resolve().parents[2]
MASTER = RV / "research" / "phase2" / "concepts_master.json"
VDIR = RV / "research" / "phase3" / "verify"
EDITABLE = {"trl", "capital_tier", "time_to_first_revenue_months", "time_to_first_revenue_text",
            "gross_margin_estimate", "gross_margin_mid_pct", "survives_glut", "glut_reason",
            "who_is_already_doing_this", "us_manufacturability", "fatal_flaw", "rule1_status", "wins_axis",
            "buyer", "what_it_is", "why_it_could_work", "possible", "profitable", "doable_by_founder",
            "materials_sense", "name"}


def main():
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    cards = {c["id"]: c for c in master["cards"]}
    n_kill = n_corr = 0
    unknown = []
    for f in sorted(VDIR.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        for v in data.get("verdicts", []):
            c = cards.get(v.get("id"))
            if c is None:
                unknown.append(f"{f.name}:{v.get('id')}")
                continue
            for corr in v.get("corrections", []) or []:
                fld = corr.get("field")
                if fld in EDITABLE:
                    c[fld] = corr.get("new_value")
                    c.setdefault("verify_corrections", []).append(f"{fld}: {corr.get('why', '')}")
                    n_corr += 1
            urls = {e.get("url") for e in c.get("evidence", []) or []}
            for e in v.get("new_evidence", []) or []:
                if e.get("url") and e["url"] not in urls:
                    c.setdefault("evidence", []).append(e)
                    urls.add(e["url"])
            c["verify_verdict"] = v.get("verdict")
            c["verify_reason"] = v.get("reason", "")
            if v.get("verdict") == "KILL":
                c["status"] = "KILLED"
                c["kill_rule"] = v.get("kill_rule", "")
                c["kill_reason"] = v.get("reason", "")
                n_kill += 1
            else:
                c["status"] = "ALIVE"
    MASTER.write_text(json.dumps(master, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"applied verdicts: {n_kill} killed, {n_corr} field corrections; unknown ids: {unknown or 'none'}")
    r = subprocess.run([sys.executable, str(RV / "research" / "tools" / "render_concepts.py")])
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
