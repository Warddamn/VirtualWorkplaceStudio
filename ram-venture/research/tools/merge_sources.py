#!/usr/bin/env python3
"""Merge per-agent source logs (research/sources/*.jsonl) into SOURCES.md.

- Deduplicates by normalized URL; aggregates the facts each source supports.
- Reports (does not fabricate) URLs cited in deliverable markdown that are
  missing from every agent log, so the verification gate can chase them.

Usage: python3 research/tools/merge_sources.py [--check]
  --check  exit 1 if any deliverable cites a URL not in the logs.
"""
import json
import re
import sys
from pathlib import Path

RV = Path(__file__).resolve().parents[2]
SRC_DIR = RV / "research" / "sources"
OUT = RV / "SOURCES.md"
DELIVERABLE_GLOBS = ["*.md", "04_DEEPDIVES/*.md"]
URL_RE = re.compile(r"https?://[^\s\)\]>\"'`|]+")


def norm(url: str) -> str:
    u = url.strip().rstrip(".,;:")
    u = re.sub(r"#.*$", "", u)
    u = u.replace("http://", "https://")
    u = re.sub(r"^https://www\.", "https://", u)
    return u.rstrip("/").lower()


internal = []


def load_logs():
    records, bad = {}, []
    for f in sorted(SRC_DIR.glob("*.jsonl")):
        agent = f.stem
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                bad.append(f"{f.name}:{i}")
                continue
            url = str(r.get("url", "")).strip()
            if not url.startswith("http"):
                internal.append(f"{agent}: {url or '(none)'} — {str(r.get('title', ''))[:120]} — {str(r.get('supports', ''))[:160]}")
                continue
            k = norm(url)
            rec = records.setdefault(k, {
                "url": url, "title": r.get("title", ""), "publisher": r.get("publisher", ""),
                "published": r.get("published", "unknown"), "accessed": r.get("accessed", "2026-11-01"),
                "type": r.get("type", "other"), "supports": [], "agents": set(),
            })
            s = str(r.get("supports", "")).strip()
            if s and s not in rec["supports"]:
                rec["supports"].append(s)
            rec["agents"].add(agent)
            if not rec["title"] and r.get("title"):
                rec["title"] = r["title"]
    return records, bad


def cited_urls():
    cited = {}
    for g in DELIVERABLE_GLOBS:
        for f in RV.glob(g):
            if f.name == "SOURCES.md":
                continue
            for m in URL_RE.findall(f.read_text(encoding="utf-8", errors="replace")):
                cited.setdefault(norm(m), (m, set()))[1].add(str(f.relative_to(RV)))
    return cited


def esc(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def main():
    check = "--check" in sys.argv
    records, bad = load_logs()
    cited = cited_urls()
    missing = {k: v for k, v in cited.items() if k not in records}

    by_type = {}
    for k, r in records.items():
        by_type.setdefault(r["type"] or "other", []).append((k, r))
    order = ["primary-filing", "company-IR", "government", "peer-reviewed", "conference", "patent",
             "market-research", "news", "blog", "other"]
    types = order + sorted(t for t in by_type if t not in order)

    lines = [
        "# SOURCES",
        "",
        "Every source used by any agent in this engagement, merged from `research/sources/*.jsonl` by "
        "`research/tools/merge_sources.py`, deduplicated by URL. Accessed dates are 2026-10/11 unless stated. "
        "Types: primary-filing / company-IR / government / peer-reviewed / conference / patent are primary; "
        "market-research is usually a free press release about a paywalled report; news/blog are secondary.",
        "",
        f"**Total unique sources: {len(records)}**",
        "",
    ]
    n = 0
    for t in types:
        items = by_type.get(t)
        if not items:
            continue
        items.sort(key=lambda kr: (kr[1]["publisher"].lower(), kr[1]["title"].lower()))
        lines += [f"## {t} ({len(items)})", "", "| # | Source | Published | Accessed | Supports | Logged by |",
                  "|---|---|---|---|---|---|"]
        for k, r in items:
            n += 1
            title = esc(r["title"] or r["url"])[:160]
            pub = esc(r["publisher"])
            sup = esc("; ".join(r["supports"]))[:600]
            lines.append(f"| S{n:03d} | [{title}]({r['url']}) — {pub} | {esc(r['published'])} | "
                         f"{esc(r['accessed'])} | {sup} | {', '.join(sorted(r['agents']))} |")
        lines.append("")
    if missing:
        lines += ["## Cited in deliverables but not in any agent log (verification gate must resolve)", ""]
        for k, (u, files) in sorted(missing.items()):
            lines.append(f"- {u} — cited in {', '.join(sorted(files))}")
        lines.append("")
    if internal:
        lines += ["## Non-web references (local files, training-knowledge notes) — not counted as sources", ""] + [f"- {b}" for b in internal] + [""]
    if bad:
        lines += ["## Malformed log lines skipped", ""] + [f"- {b}" for b in bad] + [""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"SOURCES.md: {len(records)} unique sources; {len(missing)} cited-but-unlogged; {len(bad)} malformed lines")
    if check and missing:
        for k, (u, files) in sorted(missing.items()):
            print(f"  MISSING: {u}  <- {', '.join(sorted(files))}")
        sys.exit(1)


if __name__ == "__main__":
    main()
