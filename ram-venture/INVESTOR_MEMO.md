# INVESTOR MEMO: Memory Lifecycle & Cost Intelligence (DD2)

> **PRIMARY:** DD2 `lifecycle-intel` (C-80, C-29, C-61). Memory lifecycle & cost intelligence SaaS for small U.S. hardware OEMs, run as a gated side business, not a venture.
> **FALLBACK:** DD5 `open-memory-ip` (C-33). OpenRAM macro service for U.S. open-PDK tapeouts (sky130/GF180). Wedge only; run after DD2, never alongside it.
> **MOONSHOT:** NONE honestly qualifies. Best available: the C-86 contract-reference Memory Cost Escalation Index (killed as designed by the red team), held as a ~$0-marginal option inside DD2's kill test.

*Phase 6, 2026-11-01. Source keys: **DEC** `research/phase6/decision.json`; **LI** `04_DEEPDIVES/lifecycle-intel.md`; **LI.py** `models/lifecycle-intel.py` output; **LAND** `01_LANDSCAPE.md`; **RT** `05_REDTEAM.md`; **ST** `SUMMARY_TABLE.md`; **J-** `research/phase6/judge_*.json`.*

**Bottom line.** We screened 98 concepts for making RAM, or something better, in the U.S. and killed 83 (ST); seven deep dives drew 186 red-team objections, none refuted (RT). Nothing venture-scale survived for a founder with under $50k (DEC). What remains is a capped, gated side business that **pays no $10k/month founder salary within 36 months** in any modelled scenario (LI.py §6). Web evidence is search-snippet grade (LAND). We are not asking for money.

## Problem

Small U.S. hardware makers (industrial PCs, rugged servers, medtech) put DDR4, eMMC, NOR and EEPROM on boards that live 5–20 years; nobody tracks memory full-time (LI §1, §3). In 2026 prices spiked 80–90%, DDR4 lead times reached 25–45+ weeks, and EOL notices hit live BOMs (LI §1); 75% of AdvaMed members report memory constraints and 63% allocation problems (LI §3). Missing the ~6-month last-time-buy window forces a board redesign (LI §1).

## Insight

The shortage is a price spike, not a cost opening. Incumbents make DDR5 at $1.48/GB and earn ~82% gross margin even at the $8.15/GB glut price, and memory earns no Made-in-USA premium (LAND §0). No alternative memory a small entrant could make comes within 10× on $/GB (cheaper rows need a T4 fab, are DRAM itself, or are salvaged Optane: `models/device_cost_compare.py` §4). The opening is selling to memory buyers, not making memory (DEC reaim).

## Product

- **Alerts:** upload a BOM; get memory EOL and die-revision PCN alerts with last-time-buy deadlines and alternates, F-RAM/MRAM *candidates* for dying NVSRAM and high-write EEPROM, and a brand-level §5949 screen.
- **LTB sizer** and $3,500 last-time-buy studies; $249 or $649/month, blended net $340 at 80% contribution margin (LI.py §3).

## Why now

- §5949 bars federal purchases of products with CXMT, YMTC or SMIC chips from 2027-12-23 (LAND §0).
- **Short window:** prices should turn in 2028 (LAND §0); price-alert revenue then falls 57% (GLUT) or 83% (SEVERE); only the lifecycle module ($5,774/month) holds (LI.py §6).

## Why us

Thin. The founder ships software fast and works in product development and operations at a design/manufacturing company: they know the buyer, but the employer is in the target industry (Risk 1; LI §6). Not a chip engineer; ~15 h/week caps them at ~20 trials a month. Support: two advisors, contractors (LI §0, §9). No buyer has paid or signed anything (DEC).

## Market

- ~3,000 U.S. SMB hardware OEMs ([ESTIMATE], cut from 6,000 by the red team; LI §2.4).
- $1M ARR by m36 needs ~238 accounts (7.9%) and 3.3× the modelled trial inflow (LI.py §8); the red team's ceiling is $0.1–0.3M ARR (RT-VC-DD2-04).
- Octopart flags EOL parts free; SiliconExpert starts at $250/month; Arrow, Siemens or Renesas could bundle it free and are the realistic exit (LI §5).

## Model

| LI.py §6 | BASE | GLUT (DDR5 −60%) | SEVERE (−90%) |
|---|---|---|---|
| ARR m18 / m36 | $69,915 / $149,629 | $66,411 / $104,077 | $63,862 / $83,031 |
| Plan cash low (from $40k; LI.py §10) | $9,150 @ m16 | $9,784 @ m16 | $10,112 @ m16 |
| Pays $10k/mo salary | never | never | never |

- First revenue m6 (2027-05); breakeven m17, founder unpaid (LI.py §4, §6).
- **Plan cash** ($1,950 test charged; $5k antitrust opinion, $1k consult deferred): max draw **$30,850** (cap $34k), low **$9,150** (floor $5k). If K3+K4 pass and that $6k is spent: **$36,850** and **$3,150**, breaching both unless results beat BASE (LI.py §10 PLAN rows). **Funding rule:** that $6k is spent only if index prepayments or a ≤$10k note cover it, else the index stays closed (DEC).
- **Downside:** 30% lower price or conversion puts the BASE cash low at −$11,109 or −$4,943 (LI.py §7).
- **Salary path:** trial conversion ≥14.7%; at 15%, BASE reaches $318,279 ARR at m36 and the founder goes full-time at m33; never in GLUT (LI.py §10; J-EV).
- **Index option:** K3 (≥2 of 10 signed LOIs naming a live contract) + K4 (≥10 legal-signed price-contribution agreements) open C-86, the only path above $2M ($2–10M; `03_SCORING.md` §6), at ~3% odds (J-CEIL), ≤1% to venture scale (J-INT).

## Ask

**No outside capital now.** Self-funded kill test: ≤$500 before K0, ~$1,950 planned (~$2,950 if the $1,000 consult is not deferred), $5,000 hard cap, ≤$34k ever, $5k cash floor (DEC; LI §10). Gates:

- **K0:** written employer carve-out by 2026-11-09.
- **K6, K1:** 25 qualified cold calls in 21 days; ≥5 refundable $500 deposits or paid LOIs at ≥$200/month by 2026-12-01.
- **K5:** data terms ≤$1,000/month by 2026-12-15.

**Later:** strategics (Lytica, Z2Data, Accuris, Supplyframe, Luminovo) after K1, as partners or acquirers (LI §11); angels only if the index has ≥10 licences or one enterprise redistribution deal by 2028-05, then **$0.5–1M** for a full-time founder and a seller for ~2 years (LI §7, [ESTIMATE]).

## Risks

Kill triggers: LI §10–11.

1. **Employer refuses a carve-out.** Attorney review; no code before signature. *Kill:* K0 fails.
2. **Nobody pays versus free or cheap incumbents.** Memory-only depth; ≥3 of 5 deposits in cash (J-INT). *Kill:* K1 fails; <2 paying accounts at m9; <5 accounts or MRR <$1,700 at m12.
3. **Part-time funnel too thin.** Outreach beyond the employer's network. *Kill:* K6 fails.
4. **Data rights:** Octopart terms restrict pricing use; Nexar fees unquoted. Written quote; public price prints. *Kill:* K5 and a K1 re-run fail (no-price plan: $69,289 ARR, $3,997 cash low; LI.py §10).
5. **2028 glut removes urgency.** Lifecycle features, LTB studies. *Kill:* ARR <$78k at m24 → sell or wind down.
6. **Cash runs out, or incumbents bundle.** $34k cap; sell to an incumbent. *Kill:* cash <$5k; <13 accounts at m18 → exit talks.
