#!/usr/bin/env python3
"""Consistency and health check for the dram-moonshot home lab.

Run from anywhere:

    python3 home-lab/tools/check_home_lab.py          # from dram-moonshot/
    python3 tools/check_home_lab.py --quick           # skip the slow self-tests

Prints PASS or FAIL for each check and exits 1 if any check fails. Python standard
library only (the scripts it runs need numpy; they are run, not imported).

  H1  every Python script's self-test and smoke run exits 0 within its timeout, with no
      traceback. Every script that offers --selftest must be listed here (discovered
      automatically), so a new self-test cannot be forgotten.
  H2  every .py file compiles (py_compile), MicroPython firmware included.
  H3  the E6 C firmware passes `make syntax` (gcc -fsyntax-only -Wall -Wextra, with and
      without -DENABLE_METHOD_Z) with no warnings, if gcc is installed. Without make, the
      same gcc commands run directly. Without gcc, the check is SKIPPED (not failed).
  H4  every relative markdown link in home-lab/**/*.md resolves, including #anchors
      (GitHub-style heading slugs, or an explicit <a id="...">).
  H5  every E*.md has the required sections: first principles; a "proves / does NOT
      prove" table; Safety; a parts table; procedure; data sheet or log template;
      pass/fail criteria; what would surprise you; failure modes; Sources. Each also
      declares Difficulty, Time and Cost in its header table.
  H6  the effort numbers agree: each guide's "N of 5" difficulty appears in the README
      ladder row and in the FIRST_PRINCIPLES.md experiment-map row for that guide.
  H7  no gendered pronouns (he, she, his, her, him, hers; lower-case or Capitalised) in
      any .md, .py, .c, .h, .ld or Makefile. Not counted: tokens inside a URL, and "He"
      (helium) in a file that spells out "helium" unless the next word is a verb, as
      research/tools/gate_check.py does.
  H8  no shell-garbled dollar amounts (a "$1..." eaten by a double-quoted heredoc leaves
      "~0k", "WITH M?", " M?" beside "PROVABLE", or a bare "0k"), and every guide, the
      backbone and the README still carry "$<digit>" amounts.
  H9  every firmware or MicroPython file says "untested on hardware".
  H10 the front door and safety file link every guide, and SAFETY.md links each
      guide's own safety section.

Exemptions (genuine false positives, documented here):
  - H5: E6 has no heading called "Procedure"; its step-by-step section is "8. Measurement
    protocol", so "protocol" also counts as the procedure heading.
  - H7: this checker file is not scanned, because it must spell out the words it looks
    for. URLs and the helium symbol are excluded by design, as in gate_check.py.
  - H9: files under tools/ are PC-side checkers, not firmware, even when their text
    mentions MicroPython.
  - H9: code/T3_dram/stm32_retention/host_test_patterns.c is a PC-side test program,
    not firmware, so it is not required to carry the marker.
"""
import argparse
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.dirname(HERE)
PY = sys.executable or "python3"

# --------------------------------------------------------------------------- H1 list
# (label, script relative to LAB, args, timeout s, slow). "{tmp}" is replaced by a scratch dir.
RUNS = [
    ("calcs selftest", "models/home_lab_calcs.py", ["--selftest"], 300, False),
    ("calcs all sections", "models/home_lab_calcs.py", [], 300, False),
    ("bench_calcs selftest", "code/T1_pico/bench_calcs.py", ["--selftest"], 120, False),
    ("bench_calcs all sections", "code/T1_pico/bench_calcs.py", [], 120, False),
    ("analyze_t1 selftest", "code/T1_pico/analyze_t1.py", ["--selftest"], 300, False),
    ("hamming16 self-check", "code/T1_pico/hamming16.py", [], 60, False),
    ("leakage_tail selftest", "code/T2_analysis/leakage_tail.py", ["--selftest", "--workdir", "{tmp}"], 300, False),
    ("leakage_tail expected", "code/T2_analysis/leakage_tail.py", ["--expected"], 120, False),
    ("ccd_cte selftest", "code/T2_analysis/ccd_cte.py", ["--selftest", "--workdir", "{tmp}"], 300, False),
    ("ccd_cte expected", "code/T2_analysis/ccd_cte.py", ["--expected"], 120, False),
    ("retention_map selftest", "code/T3_dram/retention_map.py", ["--selftest"], 300, True),
    ("retention_map predict", "code/T3_dram/retention_map.py", ["predict"], 120, False),
    ("capture_retention selftest", "code/T3_dram/capture_retention.py", ["--selftest"], 300, False),
    ("capture_retention simulate", "code/T3_dram/capture_retention.py",
     ["--simulate", "--temp-c", "45", "--out", "{tmp}/sim.log"], 300, True),
    ("retention_map analyze (simulated log)", "code/T3_dram/retention_map.py",
     ["analyze", "{tmp}/sim.log", "--report", "{tmp}/sim_report.md"], 300, True),
    ("expected_numbers", "code/T4_oxide/expected_numbers.py", [], 120, False),
    ("iv_analysis selftest", "code/T4_oxide/iv_analysis.py", ["--selftest"], 120, False),
    ("retention_analysis selftest", "code/T4_oxide/retention_analysis.py", ["--selftest"], 120, False),
    ("pico_smu sim transfer", "code/T4_oxide/pico_smu.py",
     ["--sim", "--mode", "transfer", "--out", "{tmp}/sim_transfer.csv"], 120, False),
    ("pico_gaincell sim calibrate", "code/T4_oxide/pico_gaincell.py",
     ["--sim", "--test", "calibrate", "--switch", "relay", "--out", "{tmp}/sim_cal.csv"], 120, False),
]

PRONOUN_RE = re.compile(r"\b(he|she|his|her|him|hers|He|She|His|Her|Him|Hers)\b")
URL_RE = re.compile(r"https?://[^\s<>()\[\]`]+")
PRONOUN_VERBS = {
    "said", "says", "say", "told", "tells", "thinks", "thought", "believes", "believed", "wants",
    "wanted", "joined", "joins", "led", "leads", "founded", "wrote", "writes", "argued", "argues",
    "noted", "notes", "will", "would", "was", "has", "had", "did", "does", "can", "could", "should",
    "might", "must", "may", "recruited", "works", "worked", "plans", "planned", "knows", "knew",
    "himself", "herself", "agreed", "agrees", "decided", "decides", "asked", "asks", "is",
}
GARBLE = [
    (re.compile(r"~0\d*k\b"), "'~0..k' (a '$1' eaten by the shell)"),
    (re.compile(r"\bWITH M\?"), "'WITH M?' (a '$1M' eaten by the shell)"),
    (re.compile(r"PROVABLE.{0,40}\sM\?|\sM\?.{0,40}PROVABLE"), "' M?' beside 'PROVABLE'"),
    (re.compile(r"(?<![\w.,$~/-])0\d*[kK]\b"), "bare '0..k' amount"),
]
LINK_RE = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
REFDEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$")
ANCHOR_RE = re.compile(r"<a\s+(?:id|name)=\"([^\"]+)\"", re.IGNORECASE)


def rel(p):
    return os.path.relpath(p, LAB)


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def files(exts=None, names=()):
    out = []
    for root, dirs, fs in os.walk(LAB):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__" and not d.startswith("."))
        for f in sorted(fs):
            if (exts and f.endswith(exts)) or f in names:
                out.append(os.path.join(root, f))
    return out


def prose_lines(text):
    """(line_no, line) for lines outside fenced code blocks."""
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


def headings(text):
    return [(i, len(m.group(1)), m.group(2).strip()) for i, ln in prose_lines(text)
            for m in [re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", ln)] if m]


def slug(title):
    """GitHub-style heading anchor: lower-case, drop punctuation and symbols, spaces to '-'."""
    t = re.sub(r"`([^`]*)`", r"\1", title)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = t.replace("**", "").replace("__", "")
    t = t.lower()
    keep = "".join(ch for ch in t if ch.isalpha() or ch in "0123456789 -_")
    return keep.replace(" ", "-")


def anchors(text):
    seen, out = {}, set()
    for _, _, h in headings(text):
        s = slug(h)
        n = seen.get(s, 0)
        out.add(s if n == 0 else f"{s}-{n}")
        seen[s] = n + 1
    out.update(m.group(1) for m in ANCHOR_RE.finditer(text))
    return out


# --------------------------------------------------------------------------- checks
def h1(quick):
    details, bad = [], []
    listed = {(s, "--selftest" in a) for _, s, a, _, _ in RUNS}
    for p in files((".py",)):
        if "/tools/" in p.replace(os.sep, "/"):
            continue
        if '"--selftest"' in read(p) and (rel(p), True) not in listed:
            bad.append(rel(p))
            details.append(f"{rel(p)} offers --selftest but is not in this checker's RUNS list")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", MPLBACKEND="Agg")
    with tempfile.TemporaryDirectory(prefix="home_lab_check_") as tmp:
        for label, script, args, tmo, slow in RUNS:
            if quick and slow:
                details.append(f"SKIP (--quick) {label}")
                continue
            path = os.path.join(LAB, script)
            argv = [a.replace("{tmp}", tmp) for a in args]
            t0 = time.time()
            try:
                p = subprocess.run([PY, path] + argv, cwd=tmp, capture_output=True, text=True,
                                   timeout=tmo, env=env)
                rc, out = p.returncode, p.stdout + p.stderr
            except subprocess.TimeoutExpired:
                rc, out = f"timeout after {tmo} s", ""
            dt = time.time() - t0
            ok = rc == 0 and "Traceback (most recent call last)" not in out
            last = (out.strip().splitlines() or [""])[-1][:90]
            details.append(f"{'ok  ' if ok else 'FAIL'} {label}: exit {rc}, {dt:.1f} s | {last}")
            if not ok:
                bad.append(label)
    n = len(RUNS)
    return not bad, f"{n - len(bad)}/{n} script runs exit 0" + (" (slow runs skipped)" if quick else ""), details


def h2(_quick):
    bad, details = [], []
    pys = files((".py",))
    with tempfile.TemporaryDirectory(prefix="home_lab_pyc_") as tmp:
        for k, p in enumerate(pys):
            try:
                py_compile.compile(p, cfile=os.path.join(tmp, f"{k}.pyc"), doraise=True)
            except py_compile.PyCompileError as exc:
                bad.append(rel(p))
                details.append(f"{rel(p)}: {exc.msg.strip().splitlines()[-1]}")
    return not bad, f"{len(pys) - len(bad)}/{len(pys)} .py files compile", details


def h3(_quick):
    d = os.path.join(LAB, "code", "T3_dram", "stm32_retention")
    if not os.path.isdir(d):
        return False, "code/T3_dram/stm32_retention missing", []
    if not shutil.which("gcc"):
        return True, "SKIPPED: gcc not installed (not a failure)", []
    srcs = re.search(r"^SRCS\s*=\s*(.+)$", read(os.path.join(d, "Makefile")), re.M).group(1).split()
    if shutil.which("make"):
        cmds = [["make", "-s", "syntax"]]
    else:
        base = ["gcc", "-fsyntax-only", "-std=c11", "-Wall", "-Wextra"]
        cmds = [base + srcs, base + ["-DENABLE_METHOD_Z"] + srcs]
    details, ok = [], True
    for c in cmds:
        p = subprocess.run(c, cwd=d, capture_output=True, text=True, timeout=300)
        out = (p.stdout + p.stderr).strip()
        warn = [ln for ln in out.splitlines() if "warning:" in ln or "error:" in ln]
        good = p.returncode == 0 and not warn
        ok &= good
        details.append(f"{' '.join(c[:3])}...: exit {p.returncode}, {len(warn)} warnings/errors")
        details += warn[:10]
    return ok, f"C firmware syntax ({len(srcs)} files, default and -DENABLE_METHOD_Z): " + \
        ("clean" if ok else "problems"), details


def h4(_quick):
    mds = files((".md",))
    cache, broken, n = {}, [], 0
    for md in mds:
        base = os.path.dirname(md)
        for i, ln in prose_lines(read(md)):
            text = re.sub(r"`[^`]*`", "", ln)
            targets = [m.group(1) for m in LINK_RE.finditer(text)]
            m = REFDEF_RE.match(text)
            if m:
                targets.append(m.group(1))
            for t in targets:
                if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", t) or t.startswith("//"):
                    continue
                n += 1
                path, _, frag = t.partition("#")
                path = urllib.parse.unquote(path.split("?")[0])
                dest = os.path.normpath(os.path.join(base, path)) if path else md
                if not os.path.exists(dest):
                    broken.append(f"{rel(md)}:{i}: ({t}) file does not exist")
                    continue
                if frag and dest.endswith(".md"):
                    if dest not in cache:
                        cache[dest] = anchors(read(dest))
                    if urllib.parse.unquote(frag).lower() not in cache[dest]:
                        broken.append(f"{rel(md)}:{i}: ({t}) anchor #{frag} not found in {rel(dest)}")
    return not broken, f"{n - len(broken)}/{n} relative links resolve in {len(mds)} markdown files", broken


REQUIRED = [
    ("first principles", "heading", r"first principles"),
    ("proves / does NOT prove table", "table", r"prove.*\|.*not prove"),
    ("Safety section", "heading", r"\bsafety\b"),
    ("parts section", "heading", r"\bparts\b"),
    ("parts table", "line", r"^\|\s*Part\s*\|"),
    ("procedure (E6 calls it \"Measurement protocol\")", "heading", r"\bprocedure\b|\bprotocol\b"),
    ("data sheet / log template", "heading", r"data sheet|log template"),
    ("pass/fail criteria", "heading", r"pass\s*/\s*fail"),
    ("what would surprise you", "heading", r"surprise"),
    ("failure modes and fixes", "heading", r"failure modes"),
    ("Sources", "heading", r"\bsources\b"),
    ("Difficulty declared", "line", r"^\|\s*\**Difficulty\**\s*\|"),
    ("Time declared", "line", r"^\|\s*\**Time\**\s*\|"),
    ("Cost declared", "line", r"^\|\s*\**Cost( tier)?\**\s*\|"),
]


def guides():
    return sorted(p for p in files((".md",)) if re.match(r"E\d_", os.path.basename(p))
                  and os.path.dirname(p) == LAB)


def h5(_quick):
    details, bad = [], 0
    for g in guides():
        text = read(g)
        heads = [h for _, _, h in headings(text)]
        lines = [ln for _, ln in prose_lines(text)]
        miss = []
        for name, kind, pat in REQUIRED:
            rx = re.compile(pat, re.IGNORECASE)
            if kind == "heading":
                hit = any(rx.search(h) for h in heads)
            elif kind == "table":
                hit = any(ln.lstrip().startswith("|") and rx.search(ln) for ln in lines)
            else:
                hit = any(rx.search(ln) for ln in lines)
            if not hit:
                miss.append(name)
        if miss:
            bad += 1
            details.append(f"{rel(g)}: missing " + "; ".join(miss))
        else:
            details.append(f"{rel(g)}: all {len(REQUIRED)} present")
    n = len(guides())
    return bad == 0 and n == 8, f"{n - bad}/{n} guides have every required section (8 expected)", details


def difficulty_digits(text):
    for _, ln in prose_lines(text):
        if re.match(r"^\|\s*\**Difficulty\**\s*\|", ln):
            return sorted(set(re.findall(r"(\d)\s*of\s*5", ln)))
    return []


def table_rows(text, header_pat):
    """Yield (header_cells, row_cells) for the first table whose header matches header_pat."""
    lines = [ln for _, ln in prose_lines(text)]
    for k, ln in enumerate(lines):
        if ln.lstrip().startswith("|") and re.search(header_pat, ln, re.IGNORECASE):
            head = [c.strip() for c in ln.strip().strip("|").split("|")]
            for row in lines[k + 2:]:
                if not row.lstrip().startswith("|"):
                    return
                yield head, [c.strip() for c in row.strip().strip("|").split("|")]
            return


def h6(_quick):
    details, bad = [], []
    readme = os.path.join(LAB, "README.md")
    fp = os.path.join(LAB, "FIRST_PRINCIPLES.md")
    rtext = read(readme) if os.path.exists(readme) else ""
    ftext = read(fp)
    for g in guides():
        gid = os.path.basename(g)[:2]
        want = difficulty_digits(read(g))
        # README ladder: the table whose header has "Difficulty"; row that links this guide.
        r_cell = None
        for head, row in table_rows(rtext, r"\|\s*Difficulty"):
            if any(os.path.basename(g) in c for c in row):
                idx = next(i for i, h in enumerate(head) if "difficulty" in h.lower())
                r_cell = row[idx] if idx < len(row) else ""
        f_cell = None
        for head, row in table_rows(ftext, r"Effort: difficulty"):
            if row and row[0] == gid:
                idx = next(i for i, h in enumerate(head) if "effort" in h.lower())
                f_cell = row[idx].split("·")[0]
        probs = []
        if not want:
            probs.append("guide declares no 'N of 5'")
        if r_cell is None:
            probs.append("no README ladder row")
        elif not all(d in r_cell for d in want):
            probs.append(f"README ladder says '{r_cell}'")
        if f_cell is None:
            probs.append("no FIRST_PRINCIPLES experiment-map row")
        elif not all(d in f_cell for d in want):
            probs.append(f"FIRST_PRINCIPLES map says '{f_cell.strip()}'")
        line = f"{gid}: guide difficulty {'/'.join(want) or '?'}"
        if probs:
            bad.append(gid)
            line += " | MISMATCH: " + "; ".join(probs)
        details.append(line)
    return not bad, f"{len(guides()) - len(bad)}/{len(guides())} guides' difficulty agrees with README and " \
                    f"FIRST_PRINCIPLES", details


def h7(_quick):
    targets = files((".md", ".py", ".c", ".h", ".ld"), names=("Makefile",))
    hits, n_url, n_he = [], 0, 0
    for p in targets:
        if os.path.abspath(p) == os.path.abspath(__file__):
            continue  # this file lists the pronouns it looks for
        text = read(p)
        helium = "helium" in text.lower()
        for i, ln in enumerate(text.splitlines(), 1):
            urls = [m.span() for m in URL_RE.finditer(ln)]
            for m in PRONOUN_RE.finditer(ln):
                if any(a <= m.start() < b for a, b in urls):
                    n_url += 1
                    continue
                if m.group(0) == "He" and helium:
                    nxt = re.match(r"\W*([A-Za-z]+)", ln[m.end():])
                    if not (nxt and nxt.group(1).lower() in PRONOUN_VERBS):
                        n_he += 1
                        continue
                hits.append(f"{rel(p)}:{i}: '{m.group(0)}' in \"{ln[max(0, m.start() - 40):m.end() + 40].strip()}\"")
    details = hits + [f"info: not counted: {n_url} inside URLs, {n_he} helium symbol 'He'"]
    return not hits, f"{len(hits)} gendered-pronoun hits in {len(targets) - 1} files", details


def h8(_quick):
    hits, details = [], []
    mds = files((".md",))
    for p in mds:
        for i, ln in prose_lines(read(p)):
            scrub = URL_RE.sub("", ln)
            for rx, why in GARBLE:
                m = rx.search(scrub)
                if m:
                    hits.append(f"{rel(p)}:{i}: {why}: \"{scrub[max(0, m.start() - 30):m.end() + 30].strip()}\"")
    need = guides() + [os.path.join(LAB, "FIRST_PRINCIPLES.md"), os.path.join(LAB, "README.md")]
    for p in need:
        if not os.path.exists(p):
            hits.append(f"{rel(p)}: missing")
            continue
        k = len(re.findall(r"\$\d", read(p)))
        details.append(f"{rel(p)}: {k} '$<digit>' amounts")
        if k == 0:
            hits.append(f"{rel(p)}: no '$<digit>' amounts left (were they eaten by the shell?)")
    return not hits, f"{len(hits)} garbled or missing dollar amounts in {len(mds)} markdown files", hits + details


def is_firmware(p):
    r = rel(p).replace(os.sep, "/")
    if r.startswith("tools/"):
        return False
    if "/stm32_retention/" in r:
        return not os.path.basename(p).startswith("host_test")
    if not p.endswith(".py"):
        return False
    text = read(p)
    head = "\n".join(text.splitlines()[:30])
    return bool(re.search(r"^\s*(import|from)\s+(machine|rp2)\b", text, re.M)
                or os.path.basename(p).startswith("pico_") or "_pico_" in os.path.basename(p)
                or re.search(r"micropython", head, re.IGNORECASE))


def h9(_quick):
    fw = [p for p in files((".py", ".c", ".h", ".ld"), names=("Makefile",)) if is_firmware(p)]
    bad = [rel(p) for p in fw if "untested on hardware" not in read(p).lower()]
    details = [f"missing marker: {b}" for b in bad] + [f"firmware files: {', '.join(rel(p) for p in fw)}"]
    return not bad and bool(fw), f"{len(fw) - len(bad)}/{len(fw)} firmware files say 'untested on hardware'", details


def h10(_quick):
    details, bad = [], []
    names = [os.path.basename(g) for g in guides()]
    for doc in ("README.md", "SAFETY.md"):
        p = os.path.join(LAB, doc)
        if not os.path.exists(p):
            bad.append(doc)
            details.append(f"{doc} missing")
            continue
        text = read(p)
        miss = [n for n in names if f"({n}" not in text]
        if doc == "README.md":
            miss += [x for x in ("SAFETY.md", "FIRST_PRINCIPLES.md") if f"({x}" not in text]
        if doc == "SAFETY.md":
            for g in guides():
                gtext = read(g)
                safe = [slug(h) for _, _, h in headings(gtext) if re.search(r"\bsafety\b", h, re.I)]
                if not any(f"({os.path.basename(g)}#{s})" in text for s in safe):
                    miss.append(f"{os.path.basename(g)}#<safety section>")
        if miss:
            bad.append(doc)
            details.append(f"{doc}: does not link " + ", ".join(miss))
        else:
            details.append(f"{doc}: links every guide" + (" and its safety section" if doc == "SAFETY.md" else ""))
    return not bad, "front door and SAFETY.md link every guide", details


CHECKS = [
    ("H1", "script self-tests and smoke runs", h1),
    ("H2", "py_compile", h2),
    ("H3", "C firmware syntax", h3),
    ("H4", "relative links and anchors", h4),
    ("H5", "required guide sections", h5),
    ("H6", "difficulty agrees across docs", h6),
    ("H7", "no gendered pronouns", h7),
    ("H8", "dollar amounts intact", h8),
    ("H9", "firmware marked untested", h9),
    ("H10", "front door and safety links", h10),
]


def main():
    ap = argparse.ArgumentParser(description="Check the dram-moonshot home lab.")
    ap.add_argument("--quick", action="store_true", help="skip the slow script runs")
    ap.add_argument("--verbose", "-v", action="store_true", help="print details for passing checks too")
    a = ap.parse_args()
    print(f"home-lab check  (root: {LAB})")
    failed = []
    for code, name, fn in CHECKS:
        try:
            ok, summary, details = fn(a.quick)
        except Exception as exc:  # a crashing check is a failing check
            ok, summary, details = False, f"check crashed: {type(exc).__name__}: {exc}", []
        print(f"{code} {'PASS' if ok else 'FAIL'}  {name}: {summary}")
        if a.verbose or not ok:
            for d in details:
                print(f"     {d}")
        if not ok:
            failed.append(code)
    print(f"HOME-LAB CHECK: {'PASS' if not failed else 'FAIL'} ({len(CHECKS) - len(failed)}/{len(CHECKS)} "
          f"checks passed" + (f"; failed: {', '.join(failed)})" if failed else ")"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
