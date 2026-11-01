# INVESTOR MEMO: Memory Lifecycle & Cost Intelligence (DD2)

> **PRIMARY:** DD2 `lifecycle-intel` (C-80, C-29, C-61). Memory lifecycle & cost intelligence SaaS for small U.S. hardware OEMs, run as a gated side business, not a venture.
> **FALLBACK:** DD5 `open-memory-ip` (C-33). OpenRAM macro service for U.S. open-PDK tapeouts (sky130/GF180). Wedge only; run after DD2, never alongside it.
> **MOONSHOT:** NONE honestly qualifies. Best available: the C-86 contract-reference Memory Cost Escalation Index (killed as designed by the red team), held as a ~$0-marginal option inside DD2's kill test.

*Phase 6, 2026-11-01. Source keys: **DEC** `research/phase6/decision.json`; **LI** `04_DEEPDIVES/lifecycle-intel.md`; **LI.py** `models/lifecycle-intel.py` output; **LAND** `01_LANDSCAPE.md`; **RT** `05_REDTEAM.md`; **ST** `SUMMARY_TABLE.md`; **J-** `research/phase6/judge_*.json`.*

**Bottom line.** The study screened 98 concepts for making RAM, or something better, in the U.S., and killed 83 (ST). Seven deep dives drew 186 red-team objections, and none was refuted (RT). No venture-scale opportunity survived for a founder with under $50k (DEC). What is left is a capped, gated side business. BASE ARR is $69,915 at m18 and $149,629 at m36. It **never pays the founder a $10k/month salary within 36 months** in any scenario (LI.py §6). The web evidence is search-snippet grade (LAND). We are not asking for money.

## Problem

Small U.S. hardware makers (industrial PCs, rugged servers, medtech) put DDR4, eMMC, NOR and EEPROM on every board. Their products live 5–20 years, and nobody on staff tracks memory full-time (LI §1, §3). In 2026 prices spiked 80–90%, DDR4 lead times reached 25–45+ weeks, and EOL notices hit live BOMs (LI §1). Among AdvaMed members, 75% report memory constraints and 63% allocation problems (LI §3). After a discontinuance notice, a buyer has about 6 months for a last-time buy; missing it forces a board redesign (LI §1).

## Insight

This shortage is a price spike, not a cost opening. Incumbents make DDR5 at $1.48/GB, and at the $8.15/GB glut price they still earn ~82% gross margin. No alternative memory a small entrant could make comes within 10× on $/GB (the model's cheaper rows need a T4 fab, are DRAM itself, or are salvaged Optane: `models/device_cost_compare.py` §4), and memory carries no Made-in-USA premium (LAND §0). So the founder's opening is selling to people who buy memory, not making it (DEC reaim). The gap is price point and memory focus, not capability (LI §5).

## Product

- **Alerts:** upload a BOM to get memory EOL and die-revision PCN alerts with last-time-buy deadlines and alternates. Also: F-RAM/MRAM *candidates* for dying NVSRAM and high-write EEPROM, and a brand-level §5949 screen.
- **LTB sizer**, plus $3,500 last-time-buy studies (LI.py §3).
- **Pricing:** $249 or $649/month. Blended net is $340, at 80% contribution margin (LI.py §3).
- **Not in the base case:** the C-86 index; its panel reaches 14.2 of the 15 members needed by m36, so it is never published (LI.py §6; RT-VC-DD2-01).

## Why now

- §5949 bars federal purchases of products with CXMT, YMTC or SMIC chips from 2027-12-23 (LAND §0).
- **The window is short:** prices should turn in 2028 (LAND §0). The price-alert module then falls 57% in GLUT and 83% in SEVERE; only the lifecycle module ($5,774/month) holds flat (LI.py §6).

## Why us

This case is thin. The founder ships software fast and works in product development and operations at a design/manufacturing company, so they know the buyer. That is also Risk 1: the employer is in the target industry (LI §6). The founder is not a chip engineer. Working ~15 h/week caps them at ~20 trials a month (LI §0, §9). The team is the founder plus two advisors and contractors (LI §9). No buyer has paid or signed anything yet (DEC).

## Market

- ~3,000 U.S. SMB hardware OEMs, an [ESTIMATE] the red team cut from 6,000 (LI §2.4).
- $1M ARR by m36 needs ~238 accounts (7.9%) and 3.3× the modelled trial inflow (LI.py §8). The red team's ceiling is $0.1–0.3M ARR (RT-VC-DD2-04).
- Octopart flags EOL parts free; SiliconExpert starts at $250/month. Arrow, Siemens or Renesas could bundle the feature at no extra cost, and are the realistic exit (LI §5).

## Model

| LI.py §6 | BASE | GLUT (DDR5 −60%) | SEVERE (−90%) |
|---|---|---|---|
| ARR m18 / m36 | $69,915 / $149,629 | $66,411 / $104,077 | $63,862 / $83,031 |
| Accounts m36 | 37 | 25 | 20 |
| Cash low, plan (from $40k; LI.py §10) | $9,150 @ m16 | $9,784 @ m16 | $10,112 @ m16 |
| Covers $10k/mo salary | never | never | never |

- **Timing:** first revenue at m6 (2027-05); breakeven at m17, founder unpaid (LI.py §4, §6).
- **Cash on the plan** ($1,950 test charged; $5k antitrust opinion and $1k consult deferred): max draw **$30,850** (cap $34k), cash low **$9,150** at m16 (floor $5k). If K3+K4 pass and that $6k is spent: **$36,850** and **$3,150**, over the cap and under the floor unless results beat BASE (LI.py §10 PLAN rows).
- **Margin:** gross margin reaches 57% by m36 (LI.py §3).
- **Downside:** a 30% miss on price or conversion takes the BASE cash low to −$11,109 or −$4,943 (LI.py §7).

**What would change the picture:**

1. **K1 strong pass:** ≥8 of 25 deposits (J-EV).
2. **Measured trial conversion ≥14.7%.** At 15%, BASE reaches $318,279 ARR at m36 and the founder goes full-time at m33. Never in GLUT (LI.py §10; J-EV).
3. **LOIs to cite the index:** K3 (≥2 of 10 signed LOIs naming a live contract) plus K4 (≥10 legal-signed price-contribution agreements). Passing both opens C-86, the study's only path above $2M ($2–10M upside; `03_SCORING.md` §6). Odds are ~3% (J-CEIL), and ≤1% that it reaches venture scale (J-INT).

## Ask

**No outside capital now.** The founder self-funds the kill test: ≤$500 before K0, ~$1,950 planned (~$2,950 if the $1,000 consult is not deferred), a $5,000 hard cap, and ≤$34k ever, with a $5k cash floor (DEC; LI §10). Gates:

- **K0:** written employer carve-out by 2026-11-09.
- **K6 and K1:** 25 qualified cold calls in 21 days, and ≥5 of them giving a refundable $500 deposit or a paid LOI at ≥$200/month, by 2026-12-01.
- **K5:** data terms of ≤$1,000/month by 2026-12-15.

**When to talk.**

- **Strategic** (Lytica, Z2Data, Accuris, Supplyframe, Luminovo): after K1, as a data partner or acquirer. Exit talks start at m18 if accounts are <13 (LI §11).
- **Angel:** if, by 2028-05, the index has ≥10 licences or one enterprise redistribution deal, then raise **$0.5–1M** to fund a full-time founder plus a seller for ~2 years (LI §7, [ESTIMATE]).

## Risks

| # | Risk | Mitigation | Kill trigger (LI §10–11) |
|---|---|---|---|
| 1 | Employer refuses a carve-out: the day job is in the buyer's industry | Attorney review; no code before signature | K0 unsigned by 2026-11-09 |
| 2 | Nobody pays against free Octopart and $250 SiliconExpert | Memory-only depth; ≥3 of 5 deposits in cash (J-INT) | K1 <5/25; <2 paying accounts at m9; <5 accounts or MRR <$1,700 at m12 |
| 3 | A part-time funnel can't reach volume | Outreach outside the employer's network | K6 <25 calls in 21 days |
| 4 | Data rights: Octopart terms restrict pricing use; Nexar fees unquoted | Written quote; fall back to public price prints | K5 fails and the K1 re-run fails (no-price case on the plan: $69,289 ARR, $3,997 cash low; LI.py §10) |
| 5 | The 2028 glut removes urgency | Lean on lifecycle features and LTB studies | ARR <$78k at m24 → sell or wind down |
| 6 | Cash runs out, or incumbents bundle the feature | $34k cap; sell to an incumbent | Cash <$5k; <13 accounts at m18 → exit talks |
