#!/usr/bin/env python3
"""Phase 7 verification gate — deterministic checks. Exit 0 only if every check passes.

Checks
  G1  Every deliverable in the mission repo tree (§6) exists and is non-trivial.
  G2  Every script under models/ exits 0.
  G3  Every red-team objection has a response (compile_redteam.py exits 0).
  G4  Every URL cited in a deliverable is logged in research/sources/*.jsonl (merge_sources.py --check).
  G5  Every surviving concept satisfies Rules 1-6 as recorded data: rule1_status SUPPORTED with >=1 evidence URL
      and a TRL; capital tier recorded and not T4; a named winning axis AND buyer; materials sense recorded;
      a glut answer with a reason; possible/profitable/doable recorded separately.
  G6  No surviving concept or pick is "build a fab" (tier T3/T4 alive, or fab-building language in alive cards).
  G7  Every killed concept carries a kill rule and a reason.
  G8  The founder is never referred to with gendered pronouns in deliverables.
  G9  Picks in research/phase6/decision.json refer to alive concepts (MOONSHOT may be a documented option).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RV = Path(__file__).resolve().parents[2]
TREE = ["ASSUMPTIONS.md", "SOURCES.md", "01_LANDSCAPE.md", "02_CONCEPTS.md", "concepts.csv", "03_SCORING.md",
        "scores.csv", "05_REDTEAM.md", "INVESTOR_MEMO.md", "FIRST_90_DAYS.md", "OPEN_QUESTIONS.md",
        "SUMMARY_TABLE.md", "models/dram_cost_stack.py", "models/scoring.py"]
results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


# G1
missing = [f for f in TREE if not (RV / f).exists() or (RV / f).stat().st_size < 500]
dds = sorted((RV / "04_DEEPDIVES").glob("*.md"))
slug_models = [RV / "models" / f"{d.stem}.py" for d in dds]
missing += [str(p.relative_to(RV)) for p in slug_models if not p.exists()]
check("G1 repo tree complete (incl. 04_DEEPDIVES/<slug>.md + models/<slug>.py)",
      not missing and len(dds) >= 5, f"deep dives: {len(dds)}; missing/short: {missing or 'none'}")

# G2
fails = []
for m in sorted((RV / "models").glob("*.py")):
    r = subprocess.run([sys.executable, str(m)], cwd=RV, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        fails.append(f"{m.name} (exit {r.returncode}): {r.stderr.strip().splitlines()[-1:] }")
check("G2 every models/*.py exits 0", not fails, "; ".join(fails) or f"{len(list((RV / 'models').glob('*.py')))} scripts OK")

# G3
r = subprocess.run([sys.executable, str(RV / "research/tools/compile_redteam.py")], cwd=RV, capture_output=True, text=True)
check("G3 every red-team objection answered", r.returncode == 0, r.stdout.strip())

# G4
r = subprocess.run([sys.executable, str(RV / "research/tools/merge_sources.py"), "--check"], cwd=RV, capture_output=True, text=True)
check("G4 every cited URL is logged in SOURCES", r.returncode == 0, r.stdout.strip().splitlines()[0] if r.stdout else r.stderr[-300:])

# G5-G7
m = json.loads((RV / "research/phase2/concepts_master.json").read_text(encoding="utf-8"))
alive = [c for c in m["cards"] if c.get("status") != "KILLED"]
killed = [c for c in m["cards"] if c.get("status") == "KILLED"]
bad = []
for c in alive:
    probs = []
    if c.get("rule1_status") != "SUPPORTED":
        probs.append("rule1")
    if not any(str(e.get("url", "")).startswith("http") for e in c.get("evidence", []) or []):
        probs.append("no evidence URL")
    if not isinstance(c.get("trl"), (int, float)):
        probs.append("TRL")
    if c.get("capital_tier") not in ("T0", "T1", "T2", "T3"):
        probs.append(f"tier {c.get('capital_tier')}")
    if not str(c.get("wins_axis", "")).strip() or not str(c.get("buyer", "")).strip():
        probs.append("axis/buyer")
    if not str(c.get("materials_sense", "")).strip():
        probs.append("materials sense")
    if c.get("survives_glut") not in ("yes", "no", "partially") or not str(c.get("glut_reason", "")).strip():
        probs.append("glut")
    if not all(str(c.get(k, "")).strip() for k in ("possible", "profitable", "doable_by_founder")):
        probs.append("3 questions")
    if probs:
        bad.append(f"{c['id']}: {', '.join(probs)}")
check("G5 surviving concepts satisfy Rules 1-6 (recorded fields)", not bad, "; ".join(bad) or f"{len(alive)} alive concepts OK")

FAB_RE = re.compile(r"\b(build|building|construct|new)\s+(a\s+)?(leading-edge\s+)?(dram\s+)?fab\b", re.I)
fab = [c["id"] for c in alive if c.get("capital_tier") in ("T3", "T4")
       or FAB_RE.search(" ".join(str(c.get(k, "")) for k in ("name", "what_it_is")))]
check("G6 no surviving concept is 'build a fab' (and none alive at T3/T4)", not fab, ", ".join(fab) or "none")

nk = [c["id"] for c in killed if not str(c.get("kill_rule", "")).strip() or not str(c.get("kill_reason", "")).strip()]
check("G7 every killed concept has a rule and reason", not nk, ", ".join(nk) or f"{len(killed)} killed concepts OK")

# G8
PRON = re.compile(r"\b(founder|they)\b[^.\n]{0,80}\b(he|his|him|himself)\b|\b(he|his|him|himself)\b[^.\n]{0,40}\bday job\b", re.I)
hits = []
docs = [RV / f for f in TREE if f.endswith(".md") and f not in ("SOURCES.md",)] + dds
for f in docs:
    if not f.exists():
        continue
    for i, ln in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if PRON.search(ln) and not re.search(r"[\'\"]he[\'\"]|SanDisk founder", ln):
            hits.append(f"{f.relative_to(RV)}:{i}")
check("G8 no gendered pronouns for the founder", not hits, ", ".join(hits[:10]) or "clean")

# G9
dp = RV / "research/phase6/decision.json"
probs = []
if dp.exists():
    d = json.loads(dp.read_text(encoding="utf-8"))
    ids = {c["id"]: c for c in m["cards"]}
    for k in ("PRIMARY", "FALLBACK"):
        for cid in d.get(k, {}).get("concepts", []):
            if ids.get(cid, {}).get("status") == "KILLED":
                probs.append(f"{k} {cid} is KILLED")
    mo = d.get("MOONSHOT", {})
    if mo and any(ids.get(c, {}).get("status") == "KILLED" for c in mo.get("concepts", [])) and "option" not in mo.get("label", "").lower():
        probs.append("MOONSHOT is a killed concept without being labeled an option")
else:
    probs.append("decision.json missing")
check("G9 picks reference alive concepts (MOONSHOT option labeled)", not probs, "; ".join(probs) or "OK")

w = max(len(n) for n, _, _ in results)
for n, ok, det in results:
    print(f"{'PASS' if ok else 'FAIL'}  {n.ljust(w)}  {det[:300]}")
allok = all(ok for _, ok, _ in results)
print("\nGATE:", "PASS" if allok else "FAIL")
sys.exit(0 if allok else 1)
