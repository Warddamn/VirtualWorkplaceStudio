# Agent conventions — ram-venture research engagement

Every research agent reads this file first. It is short on purpose.

- **Root:** `/home/user/VirtualWorkplaceStudio/ram-venture` (written `$RV` below).
- **Today:** 2026-11-01. Your training data stops around mid-2026, so search the web hard and prefer sources dated 2025–2026. Put a date on every fact.
- **Full mission:** `$RV/research/MISSION_PROMPT.md`. Read §2 (rules), §3 (search space) and §5 (quality bar) before you start.
- **Founder:** builds software and web apps fast; not a chip engineer. Keeps a day job (product development and operations at a design/manufacturing company). Personal capital under $50k. Wants first revenue within 18 months; 36 months is the hard ceiling for the primary pick. US East Coast. Wants recurring revenue, not a science project or grant farm.

## Hard rules (mission §2, condensed)
1. **Physics.** Every device or material concept cites at least one peer-reviewed paper, conference paper (IEDM/ISSCC/VLSI/IMW), patent, or credible industry source showing the mechanism works at some scale. Give it a TRL from 1 to 9. With no evidence it is `UNSUPPORTED` and dies.
2. **Three separate scores:** POSSIBLE? PROFITABLE? DOABLE BY THIS FOUNDER? Never blur them.
3. **Capital tiers:** T0 < $50k · T1 $50k–$2M · T2 $2M–$50M · T3 $50M–$1B · T4 > $1B. **Never propose building a leading-edge DRAM fab.**
4. **"Better than RAM"** must name the axis ($/GB, $/GB-month, W/GB, non-volatility, density, bandwidth, latency tolerance, supply security, lifecycle length) AND the workload or buyer where that trade wins.
5. **"Cheaper materials" means three different things.** (a) material systems, (b) processes, (c) capital. Keep them apart.
6. **Cycle-proofing:** say what happens to the concept in a 2028–29 glut where DDR5 falls 60%. If it dies, say so.
7. **Don't ask questions.** Make the call and log the assumption.
8. **Compute numbers, don't guess them.** Cost stacks, unit economics and scores live in Python under `$RV/models/` and must run with `python3`.
9. **Be brutally honest.** More kills than survivors is the expected result. Name concrete materials, fabs, partners, buyers and sources. "Use graphene", "leverage AI" and "partner with Micron" are not concepts.

## Source logging (MANDATORY)
Log every source you rely on in `$RV/research/sources/<your-agent-key>.jsonl`, one JSON object per line:

```json
{"url": "https://...", "title": "...", "publisher": "...", "published": "YYYY-MM-DD|YYYY-MM|YYYY|unknown", "accessed": "2026-11-01", "type": "primary-filing|company-IR|peer-reviewed|conference|patent|market-research|government|news|blog|other", "supports": "the specific fact or number this source backs"}
```

- Append with Python (`json.dumps`) so every line is valid JSON. One object per line.
- Log only URLs you actually opened or saw in search results. **Never invent a URL.** If a fact came only from a search-result summary, write "(via search snippet)" in `supports`.
- When a source sits behind a paywall (TrendForce, Yole, TechInsights), cite the free press release or news coverage of it. Don't claim to have read the report itself.

## Citation style in markdown
- Inline citation: `claim ([Publisher, 2026-09](https://url))`.
- Every number gets a citation, a pointer to a model (`models/x.py`), or a tag `[ESTIMATE: basis]`.
- Confidence tags on key facts:
  - `[VERIFIED]`: primary source opened.
  - `[REPORTED]`: secondary source or news.
  - `[ESTIMATE]`: your own computation or assumption.
  - `[UNVERIFIED]`: could not confirm.

## Assumptions
Log every number you assume and every judgment call you make in `$RV/research/assumptions/<your-agent-key>.md`, one bullet each:

`- [<agent-key>] <assumption> — basis: <why / source>`

## Files and git
- Write only the files your task says you own, plus your own sources and assumptions files.
- Don't edit other agents' files.
- Don't run `git commit` or `git push`; the orchestrator does that.
- When you write Python, run it and make sure it exits 0.
