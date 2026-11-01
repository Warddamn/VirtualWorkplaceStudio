#!/usr/bin/env python3
"""Fold per-agent assumption logs (research/assumptions/*.md) into ASSUMPTIONS.md.

Keeps the hand-written framing section (everything above the '## Agent-logged assumptions' marker)
and regenerates the agent-logged section, grouped by phase, with stable ids A-<agent>-<n>.
"""
import re
from pathlib import Path

RV = Path(__file__).resolve().parents[2]
OUT = RV / "ASSUMPTIONS.md"
ADIR = RV / "research" / "assumptions"
MARK = "## Agent-logged assumptions"
PHASES = [
    ("p1-", "Phase 1 — landscape"), ("v", "Phase 1b — verification"), ("p1b", "Phase 1b — verification"),
    ("A", "Phase 2 — ideation (devices)"), ("B", "Phase 2 — ideation (architecture)"),
    ("C", "Phase 2 — ideation (supply chain)"), ("D", "Phase 2 — ideation (software)"),
    ("E", "Phase 2 — ideation (business models)"), ("p3", "Phase 3 — kill pass, device model & scoring"),
    ("p4", "Phase 4 — deep dives"), ("p5", "Phase 5 — red team"), ("p6", "Phase 6 — decision"),
    ("p7", "Phase 7 — verification gate"),
]


def phase_of(stem: str) -> str:
    for pre, name in PHASES:
        if stem.startswith(pre) and (len(pre) > 1 or re.match(r"^[A-E]\d?$", stem)):
            return name
    return "Other"


def main():
    head = OUT.read_text(encoding="utf-8").split(MARK)[0].rstrip()
    groups = {}
    total = 0
    for f in sorted(ADIR.glob("*.md")):
        items = []
        for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
            s = ln.strip()
            if s.startswith(("- ", "* ")) and len(s) > 4:
                items.append(s[2:].strip())
        if not items:
            continue
        groups.setdefault(phase_of(f.stem), []).append((f.stem, items))
        total += len(items)
    order = [n for _, n in PHASES] + ["Other"]
    seen = []
    out = [head, "", MARK, "",
           f"{total} assumptions logged by {sum(len(v) for v in groups.values())} agents, merged from "
           "`research/assumptions/*.md` by `research/tools/merge_assumptions.py`. IDs are `A-<agent>-<n>`. "
           "Where a later phase revised an earlier assumption, the later entry notes it, and the canonical "
           "numbers live in the models (`models/dram_cost_stack.py` `ddr5_reference()`).", ""]
    for name in order:
        if name in seen or name not in groups:
            continue
        seen.append(name)
        out += [f"### {name}", ""]
        for stem, items in groups[name]:
            out += [f"<details><summary><b>{stem}</b> ({len(items)})</summary>", ""]
            for i, it in enumerate(items, 1):
                out.append(f"- **A-{stem}-{i}** {it}")
            out += ["", "</details>", ""]
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"ASSUMPTIONS.md: {total} agent assumptions from {sum(len(v) for v in groups.values())} files")


if __name__ == "__main__":
    main()
