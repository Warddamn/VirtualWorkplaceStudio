#!/usr/bin/env python3
"""Verification gate for the dram-moonshot study.

Run from anywhere:

    python3 research/tools/gate_check.py

Prints PASS or FAIL for each check and exits 1 if any check fails. Stdlib only.

  G1  every models/*.py exits 0 within 120 s. The models write
      research/stage3/<slug>_model_output.md, so they run in a scratch mirror of the
      folder; tracked outputs are not touched. The gate also notes whether each
      fresh output is byte-identical to the copy on disk (information only).
  G2  research/tools/compile_redteam.py exits 0 and reports 0 unanswered objections
      (it rewrites REDTEAM.md in place; the gate notes whether REDTEAM.md changed).
  G3  every dossiers/*.md has "## N." sections 0 through 11, in order, and
      section 11 is "Red-team outcome".
  G4  no gendered pronouns (he, she, his, her, him, hers; any case) in the report,
      README, ideas index, dossiers, red-team summary and decision.json.
      Not counted as pronouns: tokens inside a URL, and the exact-case chemical
      symbol "He" (helium) in a file that spells out "helium", unless the next word
      is a verb from PRONOUN_VERBS, and mixed-case acronyms such as "HeRS" (a pronoun
      is written lower, Capitalised or UPPER). ALLOWLIST is for quoted literature
      titles only.
  G5  the funnel counts in IDEAS_INDEX.md (and the funnel line in README.md) equal
      the counts recomputed from the jsonl data.
  G6  the BEST BET, FASTEST PROOF and MOONSHOT named in README.md and
      DRAM_MOONSHOT_REPORT.md match research/stage3/decision.json.
  G7  every relative markdown link in README.md, DRAM_MOONSHOT_REPORT.md and
      IDEAS_INDEX.md resolves to an existing file or folder.
  G8  IDEAS_INDEX.md regenerates byte-identically from build_ideas_index.py.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable or "python3"
MODEL_TIMEOUT_S = 120
TOOL_TIMEOUT_S = 600

DOSSIER_DIR = "dossiers"
REPORT = "DRAM_MOONSHOT_REPORT.md"
README = "README.md"
INDEX = "IDEAS_INDEX.md"
DECISION = "research/stage3/decision.json"
FINAL = "research/stage3/FINAL_CONCEPTS.json"
P_IDEAS = "research/ideas10k/ideas_10k.jsonl"
P_SCORED = "research/ideas10k/screen/scored_ideas.jsonl"
P_S2 = "research/ideas10k/stage2/stage2_results.jsonl"

PRONOUN_RE = re.compile(r"\b(he|she|his|her|him|hers)\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>()\[\]`]+")
# A capitalised "He" followed by one of these is read as a pronoun even in a helium file.
PRONOUN_VERBS = {
    "said", "says", "say", "told", "tells", "thinks", "thought", "believes", "believed", "wants",
    "wanted", "joined", "joins", "led", "leads", "founded", "wrote", "writes", "argued", "argues",
    "noted", "notes", "will", "would", "was", "has", "had", "did", "does", "can", "could", "should",
    "might", "must", "may", "recruited", "works", "worked", "plans", "planned", "knows", "knew",
    "himself", "herself", "agreed", "agrees", "decided", "decides", "asked", "asks",
}
# (relative path, exact substring of the line) pairs for quoted literature titles only.
ALLOWLIST = []

ROLES = (("BEST BET", "BEST_BET"), ("FASTEST PROOF", "FASTEST_PROOF"), ("MOONSHOT", "MOONSHOT"))


def rel(path):
    return os.path.relpath(path, ROOT)


def read(relpath):
    with open(os.path.join(ROOT, relpath), encoding="utf-8") as fh:
        return fh.read()


def jsonl(relpath):
    rows = []
    with open(os.path.join(ROOT, relpath), encoding="utf-8") as fh:
        for ln in fh:
            if ln.strip():
                rows.append(json.loads(ln))
    return rows


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def prose_lines(text):
    """Yield (line_no, line) for lines outside fenced code blocks."""
    fence = None
    for i, ln in enumerate(text.splitlines(), 1):
        m = re.match(r"^\s*(`{3,}|~{3,})", ln)
        if m:
            mark = m.group(1)[0] * 3
            if fence is None:
                fence = mark
            elif mark == fence:
                fence = None
            continue
        if fence is None:
            yield i, ln


# ---------------------------------------------------------------- G1
def build_mirror(tmp):
    """Mirror ROOT into tmp with symlinks, but real copies of models/ and an empty
    slot for every research/stage3/*_model_output.md so model writes land in tmp."""
    for name in os.listdir(ROOT):
        if name in ("models", "research") or name.startswith("."):
            continue
        os.symlink(os.path.join(ROOT, name), os.path.join(tmp, name))
    os.makedirs(os.path.join(tmp, "research", "stage3"))
    for name in os.listdir(os.path.join(ROOT, "research")):
        if name == "stage3":
            continue
        os.symlink(os.path.join(ROOT, "research", name), os.path.join(tmp, "research", name))
    for name in os.listdir(os.path.join(ROOT, "research", "stage3")):
        if name.endswith("_model_output.md"):
            continue
        os.symlink(os.path.join(ROOT, "research", "stage3", name),
                   os.path.join(tmp, "research", "stage3", name))
    os.makedirs(os.path.join(tmp, "models"))
    for name in sorted(os.listdir(os.path.join(ROOT, "models"))):
        if name.endswith(".py"):
            with open(os.path.join(ROOT, "models", name), "rb") as src, \
                    open(os.path.join(tmp, "models", name), "wb") as dst:
                dst.write(src.read())


def g1():
    models = sorted(f for f in os.listdir(os.path.join(ROOT, "models")) if f.endswith(".py"))
    details, bad, same, compared = [], [], 0, 0
    with tempfile.TemporaryDirectory(prefix="gate_g1_") as tmp:
        build_mirror(tmp)
        for f in models:
            t0 = time.time()
            try:
                p = subprocess.run([PY, os.path.join("models", f)], cwd=tmp, capture_output=True,
                                   text=True, timeout=MODEL_TIMEOUT_S)
                rc, dt = p.returncode, time.time() - t0
                tail = (p.stderr.strip().splitlines() or [""])[-1]
            except subprocess.TimeoutExpired:
                rc, dt, tail = "timeout", time.time() - t0, f"killed after {MODEL_TIMEOUT_S} s"
            note = ""
            out = os.path.join("research", "stage3", f[:-3] + "_model_output.md")
            if os.path.exists(os.path.join(tmp, out)) and not os.path.islink(os.path.join(tmp, out)):
                compared += 1
                if os.path.exists(os.path.join(ROOT, out)) and \
                        sha(os.path.join(tmp, out)) == sha(os.path.join(ROOT, out)):
                    same += 1
                    note = "; output identical to disk"
                else:
                    note = f"; output DIFFERS from {out} on disk (info)"
            ok = rc == 0
            if not ok:
                bad.append(f)
            details.append(f"models/{f}: exit {rc}, {dt:.1f} s{note}" + ("" if ok else f" | {tail}"))
    details.append(f"info: {same}/{compared} fresh model outputs byte-identical to research/stage3 copies")
    summary = f"{len(models) - len(bad)}/{len(models)} models/*.py exit 0 within {MODEL_TIMEOUT_S} s"
    return not bad, summary, details


# ---------------------------------------------------------------- G2
def g2():
    path = os.path.join(ROOT, "REDTEAM.md")
    before = sha(path) if os.path.exists(path) else None
    try:
        p = subprocess.run([PY, os.path.join(ROOT, "research", "tools", "compile_redteam.py")],
                           cwd=ROOT, capture_output=True, text=True, timeout=TOOL_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return False, "compile_redteam.py timed out", []
    msg = (p.stdout.strip() + " " + p.stderr.strip()).strip()
    m = re.search(r"(\d+) objections, (\d+) responses, (\d+) unanswered", msg)
    after = sha(path) if os.path.exists(path) else None
    unanswered_in_file = "UNANSWERED:" in read("REDTEAM.md") if after else True
    ok = p.returncode == 0 and m is not None and m.group(3) == "0" and not unanswered_in_file
    details = [msg or "(no output)",
               "REDTEAM.md unchanged by recompile" if before == after else "REDTEAM.md was rewritten (it was stale)"]
    summary = f"compile_redteam.py exit {p.returncode}; " + (
        f"{m.group(1)} objections, {m.group(3)} unanswered" if m else "could not parse its summary line")
    return ok, summary, details


# ---------------------------------------------------------------- G3
def g3():
    files = sorted(f for f in os.listdir(os.path.join(ROOT, DOSSIER_DIR)) if f.endswith(".md"))
    details, bad = [], []
    for f in files:
        heads = []
        for _, ln in prose_lines(read(os.path.join(DOSSIER_DIR, f))):
            m = re.match(r"^##\s+(\d+)\.\s+(.*?)\s*$", ln)
            if m:
                heads.append((int(m.group(1)), m.group(2)))
        nums = [n for n, _ in heads]
        first = {}
        for n, t in heads:
            first.setdefault(n, t)
        missing = [n for n in range(12) if n not in first]
        in_order = [n for n in nums if n in range(12)] == sorted(n for n in nums if n in range(12)) \
            and len(nums) == len(set(nums))
        s11 = first.get(11, "")
        s11_ok = s11.lower().startswith("red-team outcome")
        problems = []
        if missing:
            problems.append(f"missing sections {missing}")
        if not in_order:
            problems.append(f"sections out of order or repeated: {nums}")
        if not s11_ok:
            problems.append(f"section 11 is '{s11}' not 'Red-team outcome'")
        if problems:
            bad.append(f)
            details.append(f"dossiers/{f}: " + "; ".join(problems))
    summary = f"{len(files) - len(bad)}/{len(files)} dossiers have sections 0-11 in order with 11 = Red-team outcome"
    return not bad and bool(files), summary, details


# ---------------------------------------------------------------- G4
def g4():
    targets = [REPORT, README, INDEX, "research/redteam/summary.md", DECISION]
    targets += [os.path.join(DOSSIER_DIR, f) for f in sorted(os.listdir(os.path.join(ROOT, DOSSIER_DIR)))
                if f.endswith(".md")]
    hits, n_url, n_helium, n_mixed, n_allow, missing = [], 0, 0, 0, 0, []
    for t in targets:
        if not os.path.exists(os.path.join(ROOT, t)):
            missing.append(t)
            continue
        text = read(t)
        helium_file = "helium" in text.lower()
        for i, ln in enumerate(text.splitlines(), 1):
            urls = [m.span() for m in URL_RE.finditer(ln)]
            for m in PRONOUN_RE.finditer(ln):
                if any(a <= m.start() < b for a, b in urls):
                    n_url += 1
                    continue
                tok = m.group(0)
                if tok not in (tok.lower(), tok.capitalize(), tok.upper()):
                    n_mixed += 1  # mixed-case acronym such as "HeRS", not a pronoun form
                    continue
                if tok == "He" and helium_file:
                    nxt = re.match(r"\W*([A-Za-z]+)", ln[m.end():])
                    if not (nxt and nxt.group(1).lower() in PRONOUN_VERBS):
                        n_helium += 1
                        continue
                if any(t == f and s in ln for f, s in ALLOWLIST):
                    n_allow += 1
                    continue
                snippet = ln[max(0, m.start() - 40):m.end() + 40].strip()
                hits.append(f"{t}:{i}: '{m.group(0)}' in \"{snippet}\"")
    details = hits[:]
    details.append(f"info: not counted: {n_url} inside URLs, {n_helium} helium symbol 'He', "
                   f"{n_mixed} mixed-case acronyms (e.g. HeRS), "
                   f"{n_allow} allowlisted titles (allowlist size {len(ALLOWLIST)})")
    if missing:
        details.append("missing files: " + ", ".join(missing))
    summary = f"{len(hits)} gendered-pronoun hits in {len(targets) - len(missing)} files"
    return not hits and not missing, summary, details


# ---------------------------------------------------------------- G5
def fmt(n):
    return f"{n:,}"


def g5():
    ideas = jsonl(P_IDEAS)
    scored = jsonl(P_SCORED)
    s2 = jsonl(P_S2)
    total = len({r["id"] for r in ideas})
    dups = sum(1 for r in scored if r.get("dup_of"))
    verdict = {v: sum(1 for r in s2 if r.get("final") == v) for v in ("ADVANCE", "HOLD", "DROP")}
    data = {
        "Lexically unique ideas generated": total,
        "Screened": len({r["id"] for r in scored}),
        "Screener-flagged duplicates": dups,
        "Distinct ideas": len(scored) - dups,
        "Critiqued in Stage 2": len({r["id"] for r in s2}),
        "Stage 2 ADVANCE": verdict["ADVANCE"],
        "Stage 2 HOLD": verdict["HOLD"],
        "Stage 2 DROP": verdict["DROP"],
    }
    details, bad = [], []
    if len(ideas) != total:
        bad.append("ids")
        details.append(f"{P_IDEAS}: {len(ideas)} rows but {total} unique ids")
    if {r["id"] for r in ideas} != {r["id"] for r in scored}:
        bad.append("idsets")
        details.append("ideas_10k.jsonl and scored_ideas.jsonl hold different id sets")
    table = {}
    in_funnel = False
    for _, ln in prose_lines(read(INDEX)):
        if ln.startswith("## "):
            in_funnel = ln.strip().lower().startswith("## 2. funnel counts")
            continue
        if in_funnel and ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 2 and re.fullmatch(r"[\d,]+", cells[1]):
                table[cells[0]] = int(cells[1].replace(",", ""))
    for label, val in data.items():
        got = table.get(label)
        ok = got == val
        if not ok:
            bad.append(label)
        details.append(f"IDEAS_INDEX '{label}': {fmt(got) if got is not None else 'MISSING'} "
                       f"vs data {fmt(val)}" + ("" if ok else "  <-- MISMATCH"))
    # README funnel line: the same numbers must appear on it.
    line = next((ln for _, ln in prose_lines(read(README)) if "→" in ln and fmt(total) in ln), None)
    want = [fmt(total), fmt(data["Distinct ideas"]), fmt(dups), fmt(data["Critiqued in Stage 2"]),
            f"{verdict['ADVANCE']} ADVANCE"]
    if line is None:
        bad.append("readme")
        details.append(f"README.md: no funnel line containing {fmt(total)}")
    else:
        miss = [w for w in want if w not in line]
        if miss:
            bad.append("readme")
        details.append("README.md funnel line: " + ("all of " + ", ".join(want) + " present" if not miss
                                                    else "missing " + ", ".join(miss)))
    summary = (f"data: {fmt(total)} ideas / {fmt(dups)} duplicates / {fmt(data['Distinct ideas'])} distinct / "
               f"{fmt(data['Critiqued in Stage 2'])} critiqued / {verdict['ADVANCE']} ADVANCE")
    return not bad, summary, details


# ---------------------------------------------------------------- G6
def g6():
    dec = json.loads(read(DECISION))
    want = {label: dec[key]["slug"] for label, key in ROLES}
    names = {}
    for c in json.loads(read(FINAL))["concepts"]:
        names[c["name"].split(":")[0].strip().upper()] = c["slug"]
    role_re = re.compile(r"\b(BEST BET|FASTEST PROOF|MOONSHOT)\b[*_]*\s*:\s*[*_]*\s*"
                         r"(?:\[([^\]]+)\]\(([^)\s]+)\)|([A-Z][A-Z0-9' -]*[A-Z0-9]))")
    details, bad = [], []
    for doc in (README, REPORT):
        found = {label: [] for label, _ in ROLES}
        for i, ln in prose_lines(read(doc)):
            for m in role_re.finditer(ln):
                label, ltext, target, bare = m.groups()
                slugs = set()
                if target:
                    mt = re.search(r"(?:^|/)dossiers/([A-Za-z0-9_-]+)\.md$", target.split("#")[0])
                    if mt:
                        slugs.add(mt.group(1))
                    if ltext.strip().upper() in names:
                        slugs.add(names[ltext.strip().upper()])
                elif bare and bare.strip().upper() in names:
                    slugs.add(names[bare.strip().upper()])
                if slugs:
                    found[label].append((i, slugs))
        for label, _ in ROLES:
            hits = found[label]
            wrong = [(i, s) for i, s in hits if s != {want[label]}]
            if not hits:
                bad.append(doc)
                details.append(f"{doc}: {label} not named (expected {want[label]})")
            elif wrong:
                bad.append(doc)
                details.append(f"{doc}: {label} names " + "; ".join(
                    f"line {i}: {sorted(s)}" for i, s in wrong) + f" but decision.json says {want[label]}")
            else:
                details.append(f"{doc}: {label} = {want[label]} ({len(hits)} mention(s))")
    for label, _ in ROLES:
        if not os.path.exists(os.path.join(ROOT, DOSSIER_DIR, want[label] + ".md")):
            bad.append("dossier")
            details.append(f"dossiers/{want[label]}.md missing")
    summary = "decision.json: " + ", ".join(f"{label} {want[label]}" for label, _ in ROLES)
    return not bad, summary, details


# ---------------------------------------------------------------- G7
LINK_RE = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
REFDEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$")


def g7():
    details, n, broken = [], 0, []
    for doc in (README, REPORT, INDEX):
        base = os.path.dirname(os.path.join(ROOT, doc))
        for i, ln in prose_lines(read(doc)):
            text = re.sub(r"`[^`]*`", "", ln)
            targets = [m.group(1) for m in LINK_RE.finditer(text)]
            m = REFDEF_RE.match(text)
            if m:
                targets.append(m.group(1))
            for t in targets:
                if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", t) or t.startswith("#") or t.startswith("//"):
                    continue
                path = urllib.parse.unquote(t.split("#")[0].split("?")[0])
                if not path:
                    continue
                n += 1
                if not os.path.exists(os.path.normpath(os.path.join(base, path))):
                    broken.append(f"{doc}:{i}: ({t}) does not resolve")
    details = broken[:] or [f"all {n} relative links resolve"]
    return not broken, f"{n - len(broken)}/{n} relative links resolve", details


# ---------------------------------------------------------------- G8
def g8():
    with tempfile.TemporaryDirectory(prefix="gate_g8_") as tmp:
        out = os.path.join(tmp, "IDEAS_INDEX.md")
        try:
            p = subprocess.run([PY, os.path.join(ROOT, "research", "tools", "build_ideas_index.py"), out],
                               cwd=ROOT, capture_output=True, text=True, timeout=TOOL_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            return False, "build_ideas_index.py timed out", []
        if p.returncode != 0 or not os.path.exists(out):
            return False, f"build_ideas_index.py exit {p.returncode}", [p.stderr.strip()[-500:]]
        with open(out, "rb") as fh:
            fresh = fh.read()
    with open(os.path.join(ROOT, INDEX), "rb") as fh:
        disk = fh.read()
    if fresh == disk:
        return True, f"IDEAS_INDEX.md byte-identical to a fresh build ({len(disk):,} bytes)", []
    a, b = disk.decode("utf-8", "replace").splitlines(), fresh.decode("utf-8", "replace").splitlines()
    first = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
    return False, f"IDEAS_INDEX.md differs from a fresh build ({len(disk):,} vs {len(fresh):,} bytes)", \
        [f"first difference at line {first + 1}"]


CHECKS = [
    ("G1", "models run", g1),
    ("G2", "red team compiled", g2),
    ("G3", "dossier sections", g3),
    ("G4", "no gendered pronouns", g4),
    ("G5", "funnel numbers", g5),
    ("G6", "picks match decision", g6),
    ("G7", "relative links", g7),
    ("G8", "ideas index reproducible", g8),
]


def main():
    print(f"dram-moonshot gate check  (root: {ROOT})")
    failed = []
    for code, name, fn in CHECKS:
        try:
            ok, summary, details = fn()
        except Exception as exc:  # a crashing check is a failing check
            ok, summary, details = False, f"check crashed: {type(exc).__name__}: {exc}", []
        print(f"{code} {'PASS' if ok else 'FAIL'}  {name}: {summary}")
        for d in details:
            print(f"     {d}")
        if not ok:
            failed.append(code)
    print(f"GATE: {'PASS' if not failed else 'FAIL'} ({len(CHECKS) - len(failed)}/{len(CHECKS)} checks passed"
          + (f"; failed: {', '.join(failed)})" if failed else ")"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
