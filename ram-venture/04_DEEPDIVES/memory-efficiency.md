# DD4 — Memory Efficiency for On-Prem & Self-Hosted Fleets

**Slug:** `memory-efficiency` · **Author:** `p4w-memory-efficiency` · **As of:** 2026-11-01
**Model:** `models/memory-efficiency.py` (re-run 2026-11-01 with the Phase 5 RED-TEAM REVISIONS block applied, exit 0; output in `research/phase4/memory-efficiency_model_output.md`). Section numbers written "model §N" refer to that output; model §0 compares Phase 4 and Phase 5 inputs.
**Red team (Phase 5):** `p5r-memory-efficiency`, 2026-11-01. 24 objections answered in §14 and `research/phase5/responses_memory-efficiency.json`. **FINAL STATUS: KILLED.**
**Research base:** `research/phase4/memory-efficiency_notes.md`, `research/sources/p4-memory-efficiency.jsonl`, `research/assumptions/p4-memory-efficiency.md`.
**Tags:** [REPORTED-P] = primary page seen only as a search snippet; other tags per `CONVENTIONS.md`. Model month 1 = 2026-11; month 36 = 2029-10.

---

## 0. Header

**Name:** Memory Efficiency for On-Prem & Self-Hosted Fleets.

> **Red-team outcome (revised after red team): KILLED.** With the 24 objections applied, the C-74 fee the value supports falls from $7.36 to $1.66 per node per month, while credible on-call and E&O cost ~$2,900–3,400 a month. The revised BASE never breaks even and runs out of the $40k in month 12 (2027-10). The ~$6k kill experiment is cancelled because no pass outcome changes that. Details in §14.

**Pitch (Phase 4, superseded):** A guarded Linux agent that frees about 10% of installed RAM on 20–200-node on-prem and colo fleets, so operators buying DDR5 servers at 2026 prices can put off DIMM purchases. The customer pays 30% of the DRAM they did not have to buy. A cloud memory audit and KV-cache integration work bring in cash along the way.

**Concepts.**

| Role | ID | Concept | Tier | Why it is in the bundle (scorers' exact words) |
|---|---|---|---|---|
| Anchor | C-73 | Memory FinOps Audit for Cloud SaaS | T0 | Ranked #1 under all three weightings. Veteran: "it is not a memory business at all, since the DRAM shortage never reached EC2 list prices." Founder: "A consulting side gig, not the venture." |
| Folded | C-74 | Fleet Memory-Reclaim Autopilot (on-prem) | T1 | Founder: "The best software economics in my chunk (80% GM, low T1)." VC: "one production incident from zero, and no moat." |
| Folded | C-75 | KV-Cache Tier Integration & Tuning | T0 | Veteran: "a consulting gig with a ~12-month half-life." VC: "a services gig with a closing window, not a venture." |

**Why these three were folded together:** they share one ledger, "GB of DRAM not bought", sold three ways (`03_SCORING.md` §7.4). C-74 answers the veteran's objection to C-73: on-prem buyers pay for DRAM directly, while cloud buyers saw no price change. C-75 is the services way into the KV-cache workload.

**What the research changed:** the anchor is upside down.
- **C-74 is the product:** the only line with a shortage-driven reason to buy.
- **C-73 is a cash bridge.** All 92 compared EC2 on-demand SKUs kept the same prices from Sep-2025 to Oct-2026 ([AWS Price List, 2026-10](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20261029175634/us-east-1/index.csv)) [VERIFIED by agent D].
- **C-75 is being commoditized now.** Red Hat AI 3.5 made CPU KV-cache offload GA on 2026-09-09 ([aicybr, 2026-09](https://aicybr.com/blog/red-hat-ai-3-5-enterprise-inference-agents)), and Tensormesh launched an on-prem KV platform on 2026-10-15 ([HPCwire, 2026-10-15](https://www.hpcwire.com/aiwire/2026/10/15/tensormesh-targets-redundant-llm-computation-with-enterprise-caching-platform/)) [REPORTED].

**Capital tier:**
- **Phase 4: T0.** The kernel contractor was scoped to a 100-hour MVP ($17.5k), and the cash low point was $10.4k out of $40k.
- **Revised after red team: does not fit T0.** With real on-call and the revised fee, cash falls below $0 in M12 (2027-10) and reaches −$95.7k by M36 (model §5). The founder would need T1 money, and nobody would fund this at $7k ARR.
- **As specified on the card, T1.** About 300 contractor hours cost $45–60k (`concepts_master.json` C-74).

**Scores** (`scores.csv`; 3 scorers; total, with rank of 40 survivors in parentheses):

| ID | Default | Capital-constrained | Moonshot | 5-yr ceiling band (`03_SCORING.md` §6) |
|---|---|---|---|---|
| C-73 | 82.0 (#1) | 85.0 (#1) | 76.7 (#1) | < $0.5M |
| C-75 | 76.0 (#7) | 78.3 (#8) | 71.7 (#9) | < $0.5M |
| C-74 | 74.0 (#10) | 74.2 (#13) | 73.3 (#8) | $0.5–2M |

The high totals reflect the rubric, not the business. C-73, the T0 software anchor, scores 5 on capital, time to revenue and founder fit. Moat (1–2) and competition (1–3) together carry only 15% of the weight (`03_SCORING.md` §6).

**Verdicts (revised after red team; Phase 4 verdicts in brackets):**
- **POSSIBLE? Yes technically, but smaller and lumpier than claimed.** Every mechanism is in upstream Linux, vLLM or LMCache and runs in production: Meta saves 20–32% of memory and Google ~5% of fleet RAM. On the beachhead, though, Proxmox already runs KSM by default. That leaves ~5–7% incremental reclaim from zswap and proactive reclaim (model: 6%, revised after red team). Reclaim is ~0 on hugepage-backed or SEV-SNP/TDX hosts. On Kubernetes and HPC, reclaim creates no capacity the scheduler can use (RT-HYP-DD4-02, RT-HYP-DD4-03, RT-PHY-DD4-03, RT-PHY-DD4-04). [Phase 4: "Yes", with 5–15%.]
- **PROFITABLE? No (revised after red team).**
  - **BASE:** ARR is $3.8k at M18 and $7.1k at M36. The model never breaks even, cash is below $0 from M12, and cash reaches −$95.7k at M36.
  - **GLUT:** ARR is $2.5k at M36.
  - **SEVERE:** ARR is $1.2k at M36.
  - **C-74 subscription:** it loses money at every customer count the part-time funnel reaches (loaded GM −473% at steady state; model §3, §5).
  - **Best case:** even the kill test's best outcome ends at −$85.4k (model §6).
  - [Phase 4: "No, not as a venture; marginal side business", with $37.7k / $68.7k ARR.]
- **DOABLE BY THIS FOUNDER? No (revised after red team).**
  - **On-call:** it needs a 24/7 kernel responder with a 1–2 h SLA ($2,500–3,000 a month). A part-time founder with a day job can neither be that person nor afford one.
  - **Channel:** the only route that changes the ceiling needs ~4,500–7,900 pure-DDR5 nodes, and an operator that size has its own kernel staff (model §7).
  - [Phase 4: "Marginal".]

**Recommendation (revised after red team): kill DD4.**
- **C-74:** killed now at $0. The §10 experiment is cancelled. A $0 reopen watch runs to 2027-03-31 (§10.2).
- **C-75:** dropped, as Phase 4 already recommended. It is now off in the headline model too.
- **C-73:** not a cash bridge. At most it is opportunistic consulting of ~2 audits a year, dropped entirely if 3 committed audits do not appear by 2026-11-30.

---

## 1. How it works

A server's memory (RAM) holds everything its programs are working on. Much of it has not been touched for minutes. Google measured that about 20% of allocated RAM sits "cold" by a 2-minute test ([LPC, 2019](https://lpc.events/event/4/contributions/561/attachments/363/596/Persistent_Memory_as_Memory.pdf)) [REPORTED-P].

Linux has free, built-in ways to use it better: **compression** (zswap/zram) packs idle pages at roughly 2:1 ([Linux zram docs](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/blockdev/zram.rst)) [REPORTED]; **deduplication** (KSM) merges identical pages across virtual machines; **proactive reclaim** (PSI-driven, as in Meta's Senpai, and Amazon's DAMON) quietly evicts memory nobody is using. Meta's version, TMO, saves 20–32% of memory across millions of servers ([Meta/ASPLOS 2022](https://par.nsf.gov/servlets/purl/10332477)) [REPORTED-P].

Small operators rarely turn these on, and the reason is fear. Set the knobs badly and the server starts swapping, latency explodes, or the out-of-memory killer ends the wrong process. In a ScaleOps vendor test with uncapped swap on a GPU node, p50 latency went from 14.2 s to 116.5 s ([ScaleOps](https://scaleops.com/blog/kubernetes-swap-gpu-workload-sizing/)) [REPORTED].

**The product (C-74)** has three parts: a free read-only **scan** that prices the cold memory in dollars; a **guarded agent** that turns the knobs per workload and backs off the moment memory pressure or p99 latency rises; and a **ledger** that converts "GB freed" into "DIMMs you did not buy this year," of which the customer pays a share.

```
 Customer node (512 GB RAM, 60% of node-GB DDR5)
 ┌──────────────────────────────────────────────────────────────┐
 │  hot pages ............................. stay in RAM        │
 │  cold pages (idle > ~2 min) ──► compress 2:1 (zswap)         │
 │  duplicate VM pages ──────────► merge (KSM)                  │
 │  unused cgroup memory ────────► proactive reclaim (PSI/DAMON)│
 └───────────────┬──────────────────────────────▲───────────────┘
                 │ metrics (PSI, faults, p99)   │ knob changes, with
                 ▼                              │ automatic back-off
 ┌──────────────────────────────────────────────┴───────────────┐
 │ Control plane: 1) free read-only scan  2) guarded agent      │
 │ 3) ledger: "51 GB freed on this node = $883 of DDR5 you did  │
 │    not buy" → invoice = 30% of that, spread over 36 months   │
 └──────────────────────────────────────────────────────────────┘
```

*(Revised after red team.)* The ledger example above uses Phase 4 inputs. With the accepted objections, a 512 GB node frees ~31 GB (6% incremental over stock Proxmox). Its realized value is ~$299 at the peak (40% DDR5; rental-equivalent 0.75), and the fee is $1.66 per node per month at a 20% share (§2.1). The free scan also now reports hugepage, SEV-SNP/TDX and KSM state per host. Under the swap policy the agent runs zswap without SSD writeback (memory.zswap.writeback=0) on boot-class media (RT-PHY-DD4-04, RT-PHY-DD4-05).

**C-75** applies the same idea to self-hosted AI models. While a language model reads a long prompt, it builds a "KV cache," its working notes, in scarce GPU memory. If the same long prefix comes back, such as a shared system prompt or a document being queried again, those notes can be fetched from cheaper server RAM instead of being recomputed. Vendor tests show the wait for the first token falling 50–80% on repeated long contexts ([LMCache docs](https://docs.lmcache.ai/getting_started/benchmarking.html); [LMSYS, 2025-09-10](https://lmsys.org/blog/2025-09-10-sglang-hicache)) [REPORTED]. Mixed workloads see only a 28% cut ([llm-d](https://llm-d.ai/docs/guide/Installation/tiered-prefix-cache/cpu)) [REPORTED-P]. We would install the tier and size it.

**C-73** is a one-off report right-sizing memory-heavy AWS instances.

---

## 2. Cost and unit-economics model

> **Revised after red team (Phase 5, 2026-11-01).** Thirteen inputs changed (model §0; the list is in §14.2). Phase 4 numbers stay in the tables as "was" values for audit. Every number marked *(revised after red team)* comes from the re-run `models/memory-efficiency.py`.

All numbers come from `models/memory-efficiency.py` unless a source is cited. The DDR5 value per GB is imported live from `models/dram_cost_stack.py`:
- **4Q26 contract:** $25.78 per user-GB of 64GB RDIMM.
- **A-05 glut:** $10.31 (`01_LANDSCAPE.md` §4.3).
- **Severe:** $2.58 [ESTIMATE: the landscape's $2.04/GB severe component price × the model's 1.266 RDIMM-to-component ratio].

### 2.1 What one node is worth (C-74 value driver, model §2) *(revised after red team)*

| Scenario / month | DDR5 RDIMM $/GB | Realized value per node: was → revised | Fee the value supports, $/node/mo: was → revised | MRR per 80-node customer: was → revised |
|---|---|---|---|---|
| Peak (2026-11) | 25.78 | $883 → **$299** | 7.36 → **1.66** | $589 → **$133** |
| BASE 2029-10 | 18.05 | $618 → **$209** | 5.15 → **1.16** | $412 → **$93** |
| GLUT 2029-10 | 10.31 | $362 → **$126** | 3.02 → **0.70** | $242 → **$56** |
| SEVERE 2029-10 | 2.58 | $106 → **$42** | 0.88 → **0.23** | $71 → **$19** |

**How the value is computed** *(revised after red team)*:
- **Reclaim.** 512 GB × **6%** incremental reclaim over a stock Proxmox baseline = 30.7 GB freed. Phase 4 used 10% = 51.2 GB. Proxmox runs KSM by default, so the dedup slice was never ours to sell (RT-HYP-DD4-02, RT-VC-DD4-03, RT-VET-DD4-02).
- **Price mix.** **40%** of the freed GB is valued at the DDR5 price, down from 60% (RT-HYP-DD4-06, RT-VET-DD4-05). The other 60% is valued at the used-DDR4 price of $4.45/GB ([amcompute, 2026-08](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm)) [REPORTED].
- **Realization: × 0.75** (new; RT-VC-DD4-02). Thirty-six months of freed capacity is worth its rental equivalent, not the full purchase price. The rental equivalent is P0 − PV(residual of 3-year-old DIMMs): 68% (flat prices) to 78% (BASE) [ESTIMATE: 8%/yr, 40% residual]. The reviewer's pure-deferral formula, P0 − PV(P36), gives 44% in BASE, but it ignores that DIMMs bought later have more life left.

**DIMM steps** (RT-PHY-DD4-01, RT-VET-DD4-01):
- **What a step does.** Servers buy DRAM in channel-balanced steps of 1.33–1.5×. At 6% reclaim, only ~12–18% of DIMM-configuration buyers drop a step on their next PO; the rest save $0.
- **On average across buyers it washes out.** Expected saving = P(cross) × step = r × S, so the step effect is modeled as lost conversion (pilot_to_sub 0.60 → 0.40, §2.2), not as lost value.
- **Memory-bound VM hosts are different.** They buy fewer whole nodes instead, which also saves CPU, chassis and licences. That saving is not modeled.

**How the fee is set** *(revised after red team)*:
- **Share.** The fee is **20%** (was 30%) of realized value, spread over 36 months and capped at a $10/node/month list price. On-prem "DIMMs not bought" is a counterfactual, not a line on a cloud invoice (RT-HYP-DD4-01).
- **Billing.** The ledger bills against a measurable event: a deferred PO, or a smaller DIMM SKU on new nodes.
- **Pure-node cases.** A pure-DDR5 node supports $3.30/node/month at 6% reclaim and $5.50 at 10%. So the kill test's $5 bar can be met only by all-DDR5 fleets with at least 10% incremental reclaim. A pure-DDR4 node is worth $103.

### 2.2 Unit economics by line (BASE, steady state, model §3) *(revised after red team)*

| Line | Price | COGS | Gross margin | CAC | Payback | LTV (gross profit) |
|---|---|---|---|---|---|---|
| C-74 subscription (80 nodes) | **$133/mo** (was $589) | $33 variable + **$728** on-call allocation (was $79 + $289) | 75% variable / **−473% loaded** (was 87% / 37%) | $1,917 + 124 founder h (was $1,000 + 66 h) | **never** (was 27.1 mo) | **−$41,905** (was $14,708) |
| C-74 paid pilot (60 days) | $2,000 | $2,100 | −5% | — | — | — |
| C-73 audit | $3,000 | $150 + 14 h | 95% cash / 60% labor-loaded | network; **~2/yr** (was ~4/yr) | — | $2,850 |
| C-73 monitoring | $250/mo | $25/mo | 90% | 10 audits per sub | — | $3,750 |
| C-75 engagement / retainer | $25,000 / $1,500/mo | unchanged | 60% / 70% | $6,000 benchmark | — | **Off in the revised headline.** The DD itself recommends dropping C-75 (RT-HYP-DD4-04, RT-PHY-DD4-07). It is shown only as a sensitivity |

**C-74 funnel** *(revised after red team)*:
- **Conversion chain.** Reply 8% × scan 35% × pilot **30%** (was 40%) × close **40%** (was 60%) = **0.34%** (was 0.67%). That is **298** outbound touches per customer (was 149) [ESTIMATE; no on-prem benchmark exists].
- **Why the cuts.** The pilot rate falls because the DIY admin is the competitor and HPC targets were dropped (RT-VC-DD4-05, RT-PHY-DD4-03, RT-VET-DD4-03). The close rate falls because only pilots that show a PO change convert.
- **Throughput.** Part-time capacity is ~0.30 new customers a month at peak pain. Over M8–M18 the model averages ~0.18 a month (was ~0.37).

**The loaded margin is the real one** *(revised after red team)*:
- **On-call.** A named 24/7 rotation with a 1–2 h response costs **$2,500/month** at 1–5 customers and **$3,000** at 6+ (was $750 / $2,000) (RT-HYP-DD4-04, RT-VC-DD4-04, RT-VET-DD4-04).
- **E&O insurance.** Tech E&O is **$400/month** (was $200). Small-tech E&O averages $67–110/month ([Insureon](https://www.insureon.com/small-business-insurance/errors-omissions/buy-for-less)) and the startup median is ~$308/month ([QuoteSweep](https://www.quotesweep.com/blog/tech-startup-insurance-cost)) [REPORTED-P]; the rest is uplift for higher limits.
- **What that means.** At ~$100 gross profit per 80-node customer, covering on-call and E&O alone takes **~29–34 customers**. The model reaches 5.4 by M36.

### 2.3 Headline results (from $40k, model §5) *(revised after red team)*

| | BASE | GLUT | SEVERE |
|---|---|---|---|
| ARR M12 / M18 / M24 / M36 | **$1.4k / $3.8k / $5.7k / $7.1k** (was $12.9k / $37.7k / $56.1k / $68.7k) | **$1.4k / $3.8k / $4.9k / $2.5k** (was … / $37.9k) | **$1.4k / $3.8k / $3.7k / $1.2k** (was … / $16.9k) |
| C-74 customers M12 / M18 / M24 / M36 | 0.7 / 2.0 / 3.4 / 5.4 (was 1.4 / 4.1 / 6.9 / 10.8) | 0.7 / 2.0 / 3.2 / 2.3 | 0.7 / 2.0 / 2.6 / 1.8 |
| Revenue, 36 months | $64.0k (was $229.7k) | $42.3k | $38.0k |
| Blended GM / C-74 sub GM | −80% / −702% (was 44% / 37%) | −124% / −1137% | −141% / −1564% |
| First revenue | M5 (2027-03), C-73 audit | same | same |
| Breakeven (trailing 3-mo net ≥ 0, founder unpaid) | **never** (was M10) | never | never |
| Cash below $0 from | **M12 (2027-10)** | M12 | M12 |
| Cash low / cash at M36 | **−$95.7k at M36** (was $10.4k low, $55.7k end) | −$90.8k | −$90.9k |
| New C-74 acquisition stopped (kill criterion 9, now in the model) | never (the BASE turn is only −30%) | M22 (2028-08) | M20 (2028-06) |
| Founder full-time | never | never | never |

**Caveats** [ESTIMATE: arithmetic on model §4a]:
- **The model does not stop spending.** It keeps spending after cash runs out, to show the size of the hole. In practice the §11 gates stop it earlier.
- **What the gates would have cost.** Following the Phase 4 gates, the founder would hit kill criterion 6 at 2027-07-31 (M9): the fee is below $5/node and there is no paying subscription. By then ~$31.3k of the $40k is gone (cash $8.7k).
- **SOC 2 comes earlier.** Buyers now ask for SOC 2 at the 2nd customer, so the $12k lands at M18 (RT-VC-DD4-05).

### 2.4 Sensitivity (BASE, model §6) *(revised after red team)*

| Case (BASE, revised inputs) | ARR M18 | ARR M36 | Cash at M36 (= cash low) |
|---|---|---|---|
| Revised base | $3.8k | $7.1k | −$95.7k |
| Price −30% | $2.7k | $5.0k | −$114.6k |
| Conversion −30% / +30% | $1.5k / $7.9k | $2.7k / $14.9k | −$93.2k / −$100.4k |
| Reclaim 5% (Google-like) | $3.2k | $6.0k | −$97.1k |
| Reclaim 10% incremental (the old PASS bar) | $6.0k | $11.3k | −$90.0k |
| Kill-test best case (reclaim 10%, DDR5 60%) | $7.8k | $14.8k | −$85.4k |
| Reclaim 20% (low end of TMO) | $11.5k | $21.9k | −$76.0k |
| C-75 back on (its gate passes) | $11.1k | $17.7k | −$62.6k |
| C-74 standalone (C-73 at zero) | $3.3k | $6.3k | −$112.3k |
| On-call and E&O back at Phase 4 levels | $3.8k | $7.1k | −$38.7k |
| Everything +30% | $10.5k | $21.1k | −$23.2k |

**One objection at a time** (Phase 4 inputs plus a single change, model §0):

| Single change | ARR M36 | Effect |
|---|---|---|
| Reclaim 6% | $46.0k | |
| Savings share 20% | $49.8k | |
| Realization 0.75 | $54.5k | |
| DDR5 share 40% | $54.7k | |
| Close rate 0.40 | $49.8k | |
| On-call $2,500 at 1–5 customers | | Cash low −$5.0k: breaches the $40k |
| C-75 off | | Cash low $5.2k |

Each objection alone leaves a weak side business. Together they leave none: no revised case breaks even or takes the founder full-time.

### 2.5 What must be true (model §7) *(revised after red team)*

**What it takes to pay one $10k/month salary from C-74:**

| Scenario | Fee the value supports | Customers needed (80 nodes each) |
|---|---|---|
| BASE, by M18 | $1.66/node (was $7.36) | **~150** (12,002 nodes); the model delivers 2.0, a ~74× shortfall (was 27 and ~7×) |
| GLUT, at M36 | $0.70/node (was $3.02) | ~357 (was ~66) |
| SEVERE, at M36 | $0.23/node (was $0.88) | ~1,075 (was ~225) |

**The only ceiling-changing route is a channel, and it contradicts the buyer** (RT-VC-DD4-01):
- **How big the partner must be.** A reseller or MSP partner must bring **~4,500** (10% reclaim) to **~7,900** (6% reclaim) pure-DDR5 VM-host nodes, at a 25% revenue share. That carries one salary plus fixed ops at BASE peak prices, and needs ~43% more at M36 BASE prices (model §7).
- **Why that fails.** An operator that large employs its own kernel engineers.

**Also required:**
- (a) At least 10% incremental reclaim over stock Proxmox, measured as in §10.3.
- (b) 2027 purchase orders that visibly shrink.
- (c) Credible on-call for under $1k a month.
- (d) Buyers pay rather than do it themselves.


---

## 3. Target customer and the first ten customers

> *(Revised after red team; superseded by the kill.)* Changes to this list:
> - **Kubernetes removed from the buyer definition.** kube-scheduler bin-packs on requests, so freed pages create no schedulable capacity (RT-HYP-DD4-03).
> - **Rows 4–7 (research computing) dropped.** Compute nodes run without swap, Slurm caps job memory by request, and freed pages are not resold (RT-PHY-DD4-03, RT-VET-DD4-03).
> - **Row 8 demoted.** Its channel is HPC.
> - **Rows 1–2 keep only the zswap and proactive-reclaim lever.** KSM is already on by default on Proxmox, and cross-tenant KSM stays off on multi-tenant hosts (RT-HYP-DD4-02, RT-VC-DD4-03, RT-VET-DD4-02).
>
> The list below is kept for audit.

**The buyer is defined by DRAM generation, not by industry** (Phase 4). They run a 20–200-node Proxmox/KVM ~~or on-prem Kubernetes~~ fleet, plan to buy DDR5 servers in 2026–27, and have no kernel team.

**The pain is documented** [REPORTED]: Dell raised prices 15–20% from mid-Dec-2025, led by PCs, with memory costs as the stated cause ([TrendForce News, 2025-12-05](https://www.trendforce.com/news/2025/12/05/exclusive-memory-crunch-hits-pcs-dell-hikes-prices-15-20-mid-december-lenovo-from-january-2026/)); a 64GB RDIMM went from ~$255 to more than $900 between Q3-25 and Q1-26 ([PC Server and Parts](https://pcserverandparts.com/news/server-price-increases-lead-times-2026/)); distributor 64GB DDR5-6400 is approaching ~$3,000 ([Fusion, 2026-06](https://info.fusionww.com/blog/rdimm-shortages-and-the-shift-in-server-shipments)).

**Buyers on DDR4 fleets are the wrong target.** They can top up with used 64GB DDR4 RDIMMs at $3.9–5.8/GB ([amcompute](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm)) [REPORTED], and resellers already push refurbished DDR4 servers as the workaround ([PC Server and Parts](https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/)) [REPORTED].

| # | Customer | Why they buy | How to reach them |
|---|---|---|---|
| 1 | **RichWeb** (Richmond, VA; HVENS Cloud) | An East Coast MSP moving customers from VMware to Proxmox in 2026, so it is rebuilding hosts at peak DRAM prices ([RichWeb](https://www.richweb.com/news/vmware-to-proxmox-in-2026/)) [REPORTED] | Reply to their migration content with a free scan offer on one Proxmox host, then an in-person visit |
| 2 | **Petronella Technology Group** (Raleigh, NC) | An MSP that migrated to Proxmox in 2026; KSM/zswap tuning is a direct fit ([Petronella](https://petronellatech.com/blog/proxmox-vs-vmware-2026-why-we-migrated-and-you-should-too)) [REPORTED] | Same approach: a scan offer tied to their blog post, then a visit |
| 3 | **Leaseweb USA** (Manassas, VA) | Writes publicly about 2026 server price rises ([Leaseweb, 2026-07-16](https://blog.leaseweb.com/2026/07/16/rising-server-cloud-prices-2026/)) [REPORTED]; likely DIY | Ask for a design-partner test bed and reference, not a sale |
| 4 | **Michigan State ICER** | Its next cluster is smaller because CPU node prices rose ~4–5× ([ICER](https://icer.msu.edu/news/important-information-about-icers-next-cluster-acquisition)) [REPORTED-P]. Reclaim stretches a fixed grant budget | Email the research-computing director. Offer a scan on login and shared nodes |
| 5 | **U. Arizona Research Computing** | New cluster in fall 2026; PIs buy in per node at rising prices ([UArizona](https://it.arizona.edu/news/hpc-buy-opportunity)) [REPORTED-P] | Same as #4. Frame it as "more PI jobs per purchased node" |
| 6 | **Rutgers OARC (NJ), UMBC HPCF (MD), UIC ACER** | Periodic node buy-ins ([Rutgers](https://oarc.rutgers.edu/?p=4762); [UMBC](https://hpcf.umbc.edu/sp-2024-purchase); [UIC](https://live.today.uic.edu/hpc-partnership-program-deadline-approaching-for-new-node-investments/)). Pain [UNVERIFIED] | Rutgers and UMBC are close enough to drive to. Approach them through their buy-in calendars |
| 7 | **UC Riverside** campus IT | Price rise from 2026-06-01; lead times 6–14 weeks ([UCR, 2026-06-02](https://bfs.ucr.edu/news/2026/06/02/computer-purchasing-reminder-ongoing-pricing-increases-lead-time-impacts)) [REPORTED-P] | Remote: email and video scan review |
| 8 | **Advanced Clustering Technologies** (HPC integrator; channel) | Flags memory pricing in its HPC pricing guide ([Advanced Clustering](https://www.advancedclustering.com/coming-soon-latest-edition-of-our-hpc-pricing-guide/)) [REPORTED]. Could quote "10–20% less RAM plus reclaim agent" to universities | A partner pitch at a 20–30% revenue share [ESTIMATE] |
| 9 | **Refurbished-server resellers**: PC Server and Parts, ServerMonkey (Comtek is UK, so second wave) | Already sell "dodge the memory shortage" to SMB and colo buyers ([PC Server and Parts](https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/); [Comtek](https://comtek.co.uk/?p=524116)) [REPORTED]. ServerMonkey's 2026-10 update relays TrendForce's call that server contract prices keep rising through 2H27 ([ServerMonkey, 2026-10](https://www.servermonkey.com/blog/october-2026-enterprise-it-market-update.html)) [REPORTED]. Reclaim lifts their attach rate | A referral or bundle agreement, same revenue share |
| 10 | **Mid-market regulated team self-hosting 70B-class models on 8–64 GPUs** [ESTIMATE: target definition] (legal-tech, health-tech, fintech; C-75) | Data residency plus KV-tier sizing. **No named firm found** | vLLM/LMCache community channels, NYC/Boston vLLM and Ray meetups, and job posts naming vLLM plus HIPAA/SOC 2 |

**Order of contact (Phase 4; superseded — rows 4, 5 and 8 dropped or demoted by the red team):** rows 1, 2, 4, 5 and 8 first: most likely to buy DDR5 hosts in 2027, least likely to have a kernel team. Series A–C SaaS firms with $20–200k/month AWS bills are C-73 audit prospects only.

---

## 4. Go-to-market

**Channel:**
- **Lead magnet.** An open-source, read-only "cold-memory / DRAM-deferral scan" (DAMON sysfs, PSI, idle-page tracking, Prometheus export) plays the role Robusta KRR plays in cloud right-sizing.
- **Primary channel.** Founder-led outbound to named East Coast MSPs and research-computing centers.
- **Secondary channel.** HPC integrators and refurbished-server resellers at a 20–30% revenue share [ESTIMATE].
- **Not a channel.** AWS Marketplace does not apply to on-prem buyers. C-73 is not a lead magnet either, because cloud SaaS buyers are different people from on-prem operators (`research/assumptions/p4-memory-efficiency.md`).

**Pricing:**

| Line | Price |
|---|---|
| Scan | Free, 14 days |
| C-74 pilot | $2,000 for 60 days |
| C-74 subscription | Phase 4: the lower of (30% × deferred DRAM value ÷ 36 months) and $10/node/month, i.e. $7.36/node at the peak ($589/month for 80 nodes). *Revised after red team:* 20% of realized value, billed against measured PO deltas on 12-month contracts, i.e. **$1.66/node** at the peak ($133/month for 80 nodes) |
| C-73 | $3,000 audit; $250/month monitoring |
| C-75 | $25,000 integration plus $1,500/month retainer |

The pitch to the customer was: "You keep 70% of the DRAM you didn't buy: a 3.3× return." *(Revised after red team:* at a 20% share it is a 5× return, but on only $299 of realized value per node.)

**What they already pay for.** On-prem operators already pay per server for support: Ubuntu Pro costs $500 per server per year, or $1,775 with 24/7 support ([Canonical](https://ubuntu.com/pricing/pro)) [REPORTED-P]. A memory add-on can draw on that budget line.

**Sales motion:** scan → readout call that turns cold GB into dollars → paid pilot with SLO guardrails written into the SOW → annual subscription.
- **Who sells:** the founder.
- **Who delivers:** the kernel contractor handles pilot calls and on-call.
- **Contract terms:** the MSA caps liability, and tech E&O insurance starts at the first pilot ($200/month in the model).

**First 90 days of selling** *(cancelled after red team: C-74 is killed and the §10 experiment will not run; kept for audit)* (assumed the §10 experiment passed on 2026-12-01):
- **Days 1–30 (Dec 2026):** turn the ≥2 pilot LOIs into signed SOWs. Send the 60 targets an anonymized readout of the test-host results. Publish the scanner on GitHub, with a Proxmox forum post and a write-up for research-computing staff.
- **Days 31–60 (Jan 2027):** run 2 pilots (contractor on guardrails, founder on the ledger UI). Send 40 new touches, weighted toward MSPs mid-migration from VMware; Broadcom ended its Cloud Service Provider program in Jan-2026 ([cloudmagazin, 2026-03-18](https://www.cloudmagazin.com/en/2026/03/18/vmware-broadcom-kostenfalle-2026-alternativen-proxmox-nutanix/)) [REPORTED]. Pitch Advanced Clustering and one reseller.
- **Days 61–90 (Feb 2027):** close at least 1 subscription at ≥$5/node/month. Publish a measured-reclaim case study (with consent). Send 40 more touches and ask each scan user for 2 referrals.

This is faster than the model (outreach at M5, first subscription at M8): meeting it is upside; missing it by 2027-07 is a kill trigger (§11).

---

## 5. Competitors and why you would win

| Competitor | Position | Price (2026) | Threat |
|---|---|---|---|
| **DIY: upstream Linux** plus Red Hat/Canonical `tuned` | Free features; support sold per server, e.g. RHEL ~$349–1,499 per socket pair per year ([Redress](https://redresscompliance.com/red-hat-subscription-pillar)) [REPORTED] | $0 | **The real C-74 competitor** |
| **Buy used DDR4 / refurbished servers** | The substitute ([Comtek](https://comtek.co.uk/?p=524116)) [REPORTED] | $3.9–5.8/GB | Wins every DDR4 fleet |
| **ScaleOps** | Kubernetes right-sizing; self-hosted, air-gapped, FIPS-compatible ([ScaleOps](https://scaleops.com/product/air-gapped/); [ScaleOps](https://scaleops.com/product/self-hosted/)) [REPORTED-P]. $130M Series C at >$800M ([raising.fi, 2026-03](https://raising.fi/news/scaleops-series-c-march-2026)); ~$210M total ([multiples.vc](https://multiples.vc/private-comps/scaleops)) [REPORTED] | Custom; $500–2,000+/month or % of savings ([Toolradar](https://toolradar.com/tools/scaleops/pricing)) | Closes C-74's Kubernetes segment the day it manages node swap; already publishes swap benchmarks |
| **CAST AI** | Cloud Kubernetes automation | ~$1,000/month + $5/vCPU/month ([CostBench](https://www.costbench.com/software/cloud-cost-management/cast-ai/)) [REPORTED] | C-73 |
| **IBM Kubecost / OpenCost; StormForge (CloudBolt)** | Cost visibility and ML right-sizing. IBM acquired Kubecost in Sep-2024 ([IBM](https://newsroom.ibm.com/blog-ibm-acquires-kubecost-to-broaden-hybrid-cloud-cost-management-capabilities)); CloudBolt acquired StormForge on 2025-03-31 ([CloudBolt](https://www.cloudbolt.io/company/news/cloudbolt-acquires-stormforge/)) | Kubecost ~$449/month per 100 nodes ([CostBench](https://costbench.com/software/cloud-cost-management/kubecost/)); StormForge ~$3/vCPU [UNVERIFIED: unsourced listing] | C-73; Kubernetes side of C-74 |
| **AWS Compute Optimizer, Robusta KRR, VPA, Goldilocks** | Free cloud right-sizing ([KRR](https://github.com/robusta-dev/krr)) | $0 | Free floor under C-73 |
| **Kove:SDM** | Software-defined remote memory ([StorageNewsletter, 2025-09-12](https://www.storagenewsletter.com/2025/09/12/software-defined-memory-kove-announces-benchmarks/)); Supermicro partner ([Supermicro](https://www.Supermicro.com/solutions/Solution_Brief_KoveSDM.pdf)) [REPORTED] | Not published | Adjacent: pooling, not reclaim |
| **MemVerge, Granulate** | MemVerge pivoted to AI memory ([Blocks & Files, 2025-09-24](https://www.blocksandfiles.com/ai-ml/2025/09/24/memverge-unveils-open-source-ai-memory-layer-for-llms/1603278)). Intel shut Granulate in Oct-2024 ([Globes](https://en.globes.co.il/en/article-intel-closes-granulate-lays-off-dozens-1001492599)) [REPORTED] | — | **Precedent:** the "make RAM go further" pioneers pivoted or died |
| **Tensormesh** (the LMCache company) | $24.5M raised ([Pulse 2.0, 2026-05-27](https://pulse2.com/tensormesh-20-million-raised-to-scale-kv-caching-infrastructure-for-enterprise-ai-inference/)). On-prem enterprise platform launched 2026-10-15 | Custom quote ([Toolradar](https://toolradar.com/tools/tensormesh/pricing)) | **Directly competes with C-75** |
| **NVIDIA Dynamo KVBM; Red Hat AI 3.5 / llm-d** | Free Apache-2.0 GPU→CPU→SSD KV tiering ([Dynamo](https://github.com/ai-dynamo/dynamo)). Red Hat's CPU offload is GA and supported | $0 / Red Hat subscription | C-75. Red Hat sells it to the same regulated buyers |
| WEKA, VAST, Pliops, Phison | Flash KV tiers | — | C-75 |

**Where we could win.** Only as the East Coast, hands-on DDR5-deferral specialist for 20–200-node Proxmox and on-prem Kubernetes fleets: too small for ScaleOps or Red Hat to chase, too unsophisticated to DIY. It would be held by an SLO guardrail dataset across customer workloads, a ledger in the buyer's language (DIMMs not bought), and local, in-person trust.

It is a services moat, not a software moat; scorers put moat at 2 (C-74) and 1 (C-73, C-75) (`scores.csv`).

*(Revised after red team.)* C-74 exits the Kubernetes segment now, not "the day ScaleOps manages node swap". On Kubernetes, reclaim without lower requests creates no schedulable capacity, and lowering requests is ScaleOps', VPA's and KRR's job (RT-HYP-DD4-03).

**Where we lose:** any operator with one competent Linux admin (free DIY); every DDR4 fleet (used DIMMs beat the fee); Kubernetes shops once ScaleOps adds swap management; all of C-75 (Red Hat, Tensormesh, NVIDIA); all of C-73 (free tools, no tailwind); and every segment after the 2028 turn, when "just buy RAM" wins.

---

## 6. IP position

**What we own:** the control plane and ledger code; the guardrail policy engine (per-workload rules for when to compress, reclaim or back off); and, over time, a measured reclaim-vs-latency dataset across customer workloads, the only asset that could become defensible. The scanner will be open source: a marketing asset, not IP.

**What we use under open-source licenses:**
- **Linux kernel features (GPLv2).** The agent stays in userspace and works only through sysfs, cgroup2 and procfs, so it carries no GPL obligation. Shipping a kernel module would make that module GPLv2.
- **Kubernetes LimitedSwap.** Stable in v1.34 ([KEP-2400](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/2400-node-swap/kep.yaml)); Apache-2.0.
- **LMCache, NVIDIA Dynamo and Mooncake.** Apache-2.0 per the C-75 card ([LMCache](https://github.com/LMCache/LMCache); [Mooncake](https://github.com/kvcache-ai/Mooncake)).
- **Senpai** ([GitHub](https://github.com/facebookincubator/senpai)). Its license was not checked [UNVERIFIED]. Re-implement the PSI-feedback idea rather than copy code until the license is confirmed.

**What we cannot own:** the mechanisms (TMO, Google far memory, DAMON are upstream and public), or the name "TMO", which is Meta's; keep it out of branding.

**Freedom-to-operate risks** (no patent search was run for this deep dive) [UNVERIFIED]:
- **Who might hold patents:** Meta, Google, Amazon and the hyperscale vendors may hold patents on PSI- or access-tracking-driven proactive reclaim and on KV-cache tiering.
- **Mitigation:** stay strictly on upstream kernel mechanisms and their documented knobs, and keep the novelty in the policy layer and the economics ledger.
- **Budget:** a lawyer's FTO read before the first subscription (budget ~$2–3k [ESTIMATE]). This is not in the model and would come from the cash cushion.

---

## 7. Regulatory and funding path

**Rules that matter:**
- **No export controls.** This is domestic software with no ITAR touchpoint. §5949 and FAR Case 2023-008 do not apply to the software itself (research notes §9).
- **Product liability.** The agent changes how production memory behaves, so:
  - the MSA must cap liability;
  - tech E&O and cyber insurance are mandatory from the first pilot (model $200/month in Phase 4; **$400/month revised after red team**, RT-HYP-DD4-04);
  - SOWs must name the SLO guardrails and the automatic-rollback behavior.
- **Swap safety and encryption.** Kubernetes guidance says to encrypt swap and use fast NVMe ([K8s swap docs](https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/cluster-administration/swap-memory-management.md)). zswap is outside the scope of KEP-2400 ([Kubernetes](https://www.kubernetes.dev/resources/keps/2400/)) [REPORTED-P], so on Kubernetes the agent has to stay on supported paths.
- **SOC 2 Type I.** Phase 4 expected it at about the 5th customer ($12k at M20). *Revised after red team:* buyers ask before an outside agent touches production memory, so it is due at the 2nd customer; the model books $12k at M18 (RT-VC-DD4-05).
- **Memory-error incidents.** zswap's pool is kernel memory, and a DRAM uncorrectable error there typically panics the node. The SOW must therefore define incidents to exclude hardware-UE panics logged by MCE/EDAC, with kdump on (RT-PHY-DD4-06; §11).
- **C-75 brings HIPAA.** KV tiers persist prompts to host DRAM and NVMe. Prompts at health-tech buyers may contain PHI, which means a BAA and encryption at rest.
- **University purchasing.** Quotes, POs and vendor registration can add 30–90 days to a sale [UNVERIFIED].

**Possible glut hedge** [UNVERIFIED]. NDAA FY2023 §5949 takes effect 2027-12-23; the FAR rule is only proposed ([GovInfo, 2026-02-17](https://www.govinfo.gov/content/pkg/FR-2026-02-17/html/2026-03065.htm)). If its grant-funds clause reaches federally funded university clusters, "clean" DDR5 could stay dearer for exactly the research-computing segment. Not modeled.

**Non-dilutive funding:**
- **SBIR/STTR is reauthorized through 2031-09-30** ([IEDC, 2026-04-15](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)) [REPORTED].
- **SBIR is closed to the founder for now.** The SBIR PI must spend more than half their time employed by the small business ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)) [REPORTED-P], so a founder who keeps their day job cannot be PI.
- **STTR with a university PI is the route** (e.g., an OS or memory-systems faculty member doing tiering research); topic fit with DOE ASCR or NSF systems programs is [UNVERIFIED]. Phase I money would not arrive before month 18, and grants are funding, not revenue (A-04). Pursue it only if a faculty partner appears during the university sales motion.

**Whether to raise:** don't.
No venture investor funds an on-prem tuning service at $1k–$21k ARR at M36 (revised after red team, model §5–6; Phase 4 range: $17k–$313k) against ScaleOps' $210M in the same category. Phase 4 said to bootstrap from the $40k and stop if the gates in §8 and §11 fail. *Revised after red team:* do not bootstrap it either, because C-74 is killed (§14).

---

## 8. 18-month roadmap with milestones

> *(Revised after red team.)* **Superseded.** C-74 was killed on 2026-11-01, and no part of this roadmap runs unless the §10.2 reopen condition is met. The gates below are Phase 4's and are kept for audit; the revised BASE would fail the 2027-07-31 gate (§2.3).

Model months are shown as M#. "Expected" figures are the Phase 4 model's BASE expected values.

| Quarter | Work | Measurable gate (pass to continue) |
|---|---|---|
| **Q1: M1–M3 (2026-11 → 2027-01)** | §10 kill experiment, days 1–29. Kernel-contractor MVP build starts in M2 (100 h, $17.5k across M2–M5). Scanner published. C-75 gate interviews | **2026-12-01:** every §10 pass threshold met. **2027-01-31:** 2 pilot SOWs signed; agent passes 14 days of soak on 3 test hosts with zero OOM kills |
| **Q2: M4–M6 (2027-02 → 2027-04)** | Guarded agent ready for pilots (model M6). First C-73 audit (model M5, $3k). C-75 public benchmark ($6k) **only if** the C-75 gate passed | **2027-04-30:** median measured reclaim ≥10% across pilot fleets at ≤5% p99 regression. ≥1 C-73 audit invoiced |
| **Q3: M7–M9 (2027-05 → 2027-07)** | Convert pilots. E&O insurance active. 40 touches/month plus a referral ask. First C-75 engagement possible (model M9) | **2027-07-31:** ≥1 paying C-74 subscription at ≥$5/node/month (model expected: 0.55 customers at M9). Cash ≥ $10k |
| **Q4: M10–M12 (2027-08 → 2027-10)** | Trailing-3-month breakeven, founder unpaid (model M10). Partner deal with one integrator or reseller | **2027-10-31:** ARR ≥ $12.9k (model M12). ≥2 C-74 subscriptions (model expected: 1.4, so this gate is stricter than BASE). Zero customer-impacting incidents. Loaded C-74 GM ≥ 30% |
| **Q5: M13–M15 (2027-11 → 2028-01)** | Inbound from the scanner ramps to ~4 conversations/month. Annual renewals reprice. **The DRAM turn begins in 2028-01 (M15)** | **2028-01-31:** ≥3 C-74 customers (model expected: 2.6). Renewal rate 100% |
| **Q6: M16–M18 (2028-02 → 2028-04)** | SOC 2 readiness (5th customer; model M20, $12k). Decide on the founder's role | **2028-04-30:** ARR ≥ $37.7k (model M18) to continue as a side business; ARR ≥ $75k **and** ≥8 C-74 customers to justify more investment. Full-time needs ~27 customers, which no modeled case reaches by M18 |

---

## 9. Team required

| Role | When | Where to find them | Cost (model) |
|---|---|---|---|
| **Founder:** product, scanner, control plane, ledger UI, all selling | From M1, part-time (~15 h/week, A-03). The model uses 38–86% of that | — | Unpaid through M36 in every scenario |
| **Kernel-savvy Linux memory contractor:** guardrails, pilots, on-call. The most important person | M1 (25 h kill test), M2–M5 build (100 h), then retainer | DAMON/zswap/MGLRU threads on LKML; Linux Plumbers Conference; ex-Red Hat, Canonical and SUSE kernel or support engineers; Proxmox forum power users [UNVERIFIED availability] | $175/h: $17.5k build; $2,100 per pilot; on-call $750/month (1–5 customers), $2,000 (6+) in Phase 4. **Revised after red team: $2,500 / $3,000 a month for a named 24/7 rotation with a 1–2 h SLA** (RT-VET-DD4-04) |
| **Kernel cofounder (alternative to the contractor)** | Before the first pilot, if one can be found | The same communities. Offer equity instead of retainer | Saves ~$36k/year of on-call at 6+ customers (revised after red team) [ESTIMATE: 12 × $3,000]. It would also lift the founder-fit score. This is the only way to remove the on-call cost, and it is a reopen condition (§10.2) |
| **Inference contractor** (C-75 only, and only if the gate passes) | M6 benchmark; per engagement after that | vLLM, LMCache and SGLang community channels; NYC/Boston vLLM and Ray meetups | $200/h; ~45 h per engagement; ~$3k for the benchmark |
| **SOC 2:** compliance tooling plus an auditor | At the 5th customer | Standard SOC 2 automation vendors and CPA firms | $12k (model) |
| **Insurance broker and lawyer** | M1 (LLC and MSA); first pilot (E&O) | Local East Coast tech-E&O brokers; a startup lawyer for the MSA liability cap | $1,500 setup; $200/month |

No sales hire: the model never affords one.

---

## 10. The cheapest experiment that could kill it *(revised after red team)*

### 10.1 Status: cancelled

The red team answered the question this experiment was built to answer (RT-VC-DD4-01, accepted). The re-run model shows that even the best outcome the test can produce leaves the ceiling where it is. With ≥10% reclaim and DDR5 at 60% of node-GB, BASE ARR is $7.8k at M18 and $14.8k at M36, and cash ends at −$85.4k (model §6). Spending ~$6k (capped at $10k), 15–25% of the founder's capital, to confirm a ceiling the model already shows is poor capital allocation.

**C-74 was killed at $0 on 2026-11-01.**

### 10.2 $0 reopen watch (until 2027-03-31)

C-74 reopens only if **both** of these happen without the founder spending cash:
1. **Channel.** A reseller or MSP partner commits in writing to resell to at least 4,500 majority-DDR5 VM-host nodes and accepts a savings-share invoice tied to measured PO reductions. This is the reviewer's own condition, scaled to the revised fee (model §7).
2. **On-call.** A named kernel engineer signs a retainer at no more than $1,000/month with a 24/7 response SLA of 2 hours or less, or joins as an equity cofounder (RT-VC-DD4-04, RT-VET-DD4-04, RT-HYP-DD4-04).

The founder's only job here is to answer inbound interest. If both conditions are met, re-run `models/memory-efficiency.py` with the partner's node count and the retainer price, then run §10.3 for no more than $6k.

### 10.3 Measurement protocol if reopened *(revised after red team)*

**Hypothesis:** an operator of majority-DDR5 Proxmox/KVM VM hosts will sign a 12-month contract that bills a share of a measured purchase-order reduction. They sign because guarded zswap and proactive reclaim free ≥10% of RAM beyond stock Proxmox at no SLO cost.

**Hosts.** The CI build runner and the Kubernetes node are dropped (RT-PHY-DD4-02, RT-HYP-DD4-03). Three hosts are used:
- **(a)** a Proxmox host with 20 mixed VMs on stock defaults (KSM on via ksmtuned, ballooning on);
- **(b)** a multi-tenant Proxmox host with KSM off, matching that security posture;
- **(c)** one production MSP Proxmox host under an LOI.

**Metric** (RT-PHY-DD4-02):
- **Reclaim measure.** For each host, find the lowest cgroup `memory.max` (or VM balloon target) that keeps p99 within 5% and PSI memory "some" avg60 under a fixed bound for 14 days. Compare it with the same measure on the stock baseline.
- **Split.** Report anonymous and file memory separately.
- **What counts.** The pass bar counts only anonymous memory plus the page cache the workload actually needs. Dropped page cache does not count.

**Policy:**
- **Boot-class media.** Run zswap with writeback disabled (`memory.zswap.writeback=0`, set per leaf cgroup, because older kernels do not apply it down the hierarchy; [LKML, 2023-11](https://lkml.iu.edu/hypermail/linux/kernel/2311.0/01961.html); [LKML, 2024-08](https://lkml.iu.edu/hypermail/linux/kernel/2408.2/00974.html)) [REPORTED-P].
- **Writeback.** Only to a dedicated swap device with a TBW budget. Log swap writes per day against the rated TBW (RT-PHY-DD4-05).
- **KSM.** Never enable cross-tenant KSM on multi-tenant hosts.
- **Excluded hosts.** The scanner reports hugepage/hugetlbfs backing, SEV-SNP/TDX status and KSM state for every host. Hosts with these configurations are excluded from billing and from the reclaim average (RT-PHY-DD4-04).

**PASS requires all of:**
- **Reclaim.** At least 10% incremental reclaim, by the metric above, on at least 5 MSP Proxmox hosts, with no more than 5% p99 regression and zero OOM kills (RT-HYP-DD4-02, RT-VET-DD4-02, RT-VC-DD4-03).
- **LOIs.** At least 2 paid-pilot LOIs at ≥$5/node/month, from signers who had no zswap or tuned reclaim enabled before the scan (RT-VC-DD4-05).
- **Changed purchase orders.** From those pilots, written 2027 server quotes or POs showing a smaller DIMM configuration or fewer nodes because of measured reclaim (RT-VET-DD4-01, RT-PHY-DD4-01, RT-HYP-DD4-01, RT-VC-DD4-02).
- **DDR5 census.** At least 10 responding fleets with ≥50% of node-GB on DDR5 and 2027 purchases planned. At least 15 of the 60 targets must confirm majority-DDR5 fleets (RT-VET-DD4-05, RT-HYP-DD4-06).

**Targets (60):**
- 40 Proxmox/KVM MSPs and regional hosts in VA/NC/MD/NJ/NY
- 10 on-prem VM-host operations teams
- 5 refurbished-server resellers
- 5 regional colo/hosting firms

No research-computing centers, HPC integrators or Kubernetes shops (RT-PHY-DD4-03, RT-VET-DD4-03, RT-HYP-DD4-03).

**Gates that run now, at $0:**
- **C-73.** If fewer than 3 committed $3k audits come from the founder's network by 2026-11-30, drop C-73 (RT-VC-DD4-06).
- **C-75.** No gate runs; C-75 is dropped.

### 10.4 Phase 4 design (cancelled; kept for audit)

**Hypothesis:** an East Coast operator buying DDR5 servers will pay at least $5 per node per month for guarded reclaim that frees at least 10% of RAM with no SLO regression.

**Budget:** ~$6.0k, run over 29 days (2026-11-02 → 2026-11-30); the go/no-go is recorded on 2026-12-01.

| Item | Cost |
|---|---|
| 3 rented bare-metal hosts × ~$200 | $600 |
| Kernel contractor, technical arm (15 h × $175) | $2,625 |
| Kernel contractor, scanner security review (10 h × $175) | $1,750 |
| Sales tooling | ~$300 |
| Travel to 2–3 targets in VA/NC/MD | ~$700 |
| **Total** | **~$5,975** |

**Overrun check:** if the contractor runs 50% over (~38 h instead of 25 h), the total is ~$8.2k, still under $10k [ESTIMATE: 37.5 h × $175 + $1,600 non-labor]. Spending stops at $10k whatever the state of the test.

**Steps:**
1. **Days 1–3.**
   - Rent 3 hosts and stand up three replayed workloads: (a) a Proxmox host with 20 mixed VMs; (b) a Kubernetes node running Java, Postgres and Redis; (c) a CI build runner.
   - The founder writes the read-only scanner (DAMON sysfs, PSI, idle-page tracking, Prometheus export).
2. **Days 4–7.**
   - Measure a 3-day baseline: p99 latency, major faults, OOM events.
   - Build the 60-target list: 25 Proxmox/KVM MSPs in VA/NC/MD/NJ/NY (incl. RichWeb, Petronella), 15 research-computing centers (§3 rows 4–7), 10 on-prem SaaS/fintech ops teams, 5 refurbished-server resellers, 5 HPC integrators.
3. **Days 8–21.**
   - The contractor runs zswap (zstd/zsmalloc), Senpai-style PSI reclaim and DAMON_RECLAIM, all with guardrails, for 14 days.
   - In parallel, contact all 60 targets with three asks: install the 14-day scan; share DDR5 vs DDR4 fleet mix and planned 2027 server/DIMM purchases; sign a paid-pilot LOI at a stated $/node.
   - Visit 2–3 targets in person.
4. **Days 15–28.** Interview 10 self-hosted LLM teams (the C-75 gate, $0).
5. **Day 29 (2026-11-30).** Score the results against the thresholds below, which are fixed now and may not be moved afterward.

**PASS requires all of:**
- ≥10% of installed RAM freed on average across the 3 hosts, at ≤5% p99 regression, with **zero** OOM kills on any host;
- ≥5 scan installs from the 60 targets;
- ≥2 signed paid-pilot LOIs at ≥$5/node/month, from fleets that are majority DDR5 and buying in 2027;
- fewer than half of the responding fleets are DDR4-dominant.

**FAIL on any one of those kills C-74.**

**Separate C-75 gate:** if fewer than 2 of the 10 LLM teams would pay ≥$15k for an integration now that Red Hat AI 3.5 ships CPU offload as GA, drop C-75 permanently.

**If it passes:** run 2 paid pilots and re-run `models/memory-efficiency.py` with measured reclaim and real DDR5 share before spending the rest of the build budget.

---

## 11. Explicit kill criteria *(revised after red team)*

**0. 2026-11-01 (red team): C-74 killed, C-75 dropped, C-73 demoted to opportunistic consulting. FIRED.** The reasons are in §14.

If C-74 is reopened under §10.2, the following criteria replace Phase 4's:

1. **2027-03-31:** the §10.2 channel and on-call conditions are not both met in writing → C-74 stays dead.
2. **Reopen + 29 days:** any §10.3 PASS condition missed → kill C-74.
3. **2026-11-30:** fewer than 3 committed C-73 audits → drop C-73 (RT-VC-DD4-06).
4. **Any date: incidents.** A reclaim-caused OOM kill or p99 SLO breach on a customer's production node → stop all pilots and find the root cause. **A second incident → kill C-74.** A node panic caused by a hardware uncorrectable memory error that MCE/EDAC/rasdaemon logged does not count as an agent incident; kdump is required on agent hosts so the cause can be proven. Every SOW states this definition (RT-PHY-DD4-06).
5. **Any date: drive wear.** Swap writes on a host above 0.1 drive-writes-per-day of the installed device → that host drops to zswap-only. A drive failure caused by agent writeback counts as an incident under criterion 4 (RT-PHY-DD4-05).
6. **Reopen + 5 months:** median incremental reclaim across pilot fleets below 8% by the §10.3 metric → kill C-74.
7. **2027-07-31:** no paying C-74 subscription, or a median contracted fee below $5/node/month → kill C-74.
8. **2027-12-31:** fewer than 5 signed C-74 subscriptions → kill C-74 (RT-HYP-DD4-05). The revised BASE has ~1.05 at that date.
9. **Any date before 8 C-74 customers: price stop.** TrendForce or Counterpoint report 64GB DDR5 RDIMM contract prices more than 40% below the 4Q26 peak (below ~$15.50/user-GB) → stop new C-74 acquisition and serve existing contracts until renewal. This rule is now in the model: it fires at M22 in GLUT and M20 in SEVERE, and never in BASE (RT-HYP-DD4-05).
10. **Any date:** Proxmox ships managed zswap or reclaim tuning → kill C-74. Kubernetes is already out of scope (RT-HYP-DD4-03).
11. **Any date:** cash below $8k → stop all spending except on-call.

**Phase 4 criteria (superseded; kept for audit).** How each maps to the revised list:

| Phase 4 criterion | What happened |
|---|---|
| #1 | Became revised #1–2: the reopen gate and the revised PASS |
| #2 | Dropped: C-75 is gone |
| #3 | Dropped: no pilots run without a reopen |
| #4 | Became #4, which adds the hardware-UE exclusion |
| #5 | Became #6, with the new metric |
| #6 | Became #7, unchanged |
| #7 | Became #11; the ARR gate is moot |
| #8 | Became #10; Kubernetes is exited now |
| #9 | Kept as #9; it is now in the model |
| #10 | Dropped as moot |

Revised #3 (C-73), #5 (drive wear) and #8 (5 subscriptions by 2027-12-31) are new.

1. **2026-12-01:** any §10 PASS condition missed → kill C-74.
2. **2026-12-01:** fewer than 2 of 10 LLM teams would pay ≥$15k → drop C-75.
3. **2027-01-31:** fewer than 2 pilot SOWs signed → kill C-74.
4. **Any date:** a reclaim-caused OOM kill or a p99 SLO breach on a customer's production node → stop all pilots and find the root cause. **A second incident → kill C-74.**
5. **2027-04-30:** median measured reclaim across pilot fleets below 8% → kill C-74. At 5% reclaim, M36 ARR is only $40.3k (model §6).
6. **2027-07-31:** no paying C-74 subscription, or the median contracted fee is below $5/node/month → kill C-74.
7. **2027-10-31:** ARR below $12.9k or cash below $8k → stop all spending beyond on-call, and keep only C-73 consulting.
8. **Any date:** ScaleOps, Red Hat or Canonical ships managed swap/zswap/reclaim tuning for self-hosted fleets → exit the Kubernetes segment within 30 days. If Proxmox ships the equivalent → kill C-74.
9. **Any date before 8 C-74 customers:** TrendForce or Counterpoint report 64GB DDR5 RDIMM contract prices more than 40% below the 4Q26 peak (below ~$15.50/user-GB) → stop new C-74 acquisition. Keep serving existing contracts until their renewals.
10. **2028-04-30:** ARR below $37.7k (model BASE M18) → wind down. ARR below $75k or fewer than 8 C-74 customers → no full-time move, no raise, and no further non-salary spending beyond on-call.

---

## 12. Cycle test *(revised after red team)*

**The glut arrives before the customers do, and since the red team it no longer matters: C-74 already loses money at peak prices.** The model starts the turn in 2028-01 (M15), when there are only ~1.3 C-74 customers (was ~2.6). That timing follows the 2028 downturn call (`01_LANDSCAPE.md` F2).

| | BASE (−30% over 2028) | GLUT (A-05, DDR5 −60%) | SEVERE (−90%) |
|---|---|---|---|
| DDR5 RDIMM $/user-GB at M36 | 18.05 | 10.31 | 2.58 |
| Realized value per 512 GB node | **$209** (was $618) | **$126** (was $362) | **$42** (was $106) |
| Fee the value supports, $/node/month | **1.16** (was 5.15) | **0.70** (was 3.02) | **0.23** (was 0.88) |
| C-74 customers at M36 | **5.4** (was 10.8) | **2.3** (was 8.9) | **1.8** (was 7.2) |
| New C-74 acquisition stopped (kill criterion 9) | never | M22 (2028-08) | M20 (2028-06) |
| ARR at M24 → M36 | **$5.7k → $7.1k** (was $56.1k → $68.7k) | **$4.9k → $2.5k** (was $48.0k → $37.9k) | **$3.7k → $1.2k** (was $41.5k → $16.9k) |
| C-74 subscription GM (36 months) | **−702%** (was 37%) | **−1137%** (was 21%) | **−1564%** (was −3%) |
| Monthly net at M36 | **−$3,275** (was +$2,862) | **−$3,083** (was +$591) | **−$3,167** (was −$839) |
| Cash at M36 | **−$95.7k** (was $55.7k) | **−$90.8k** (was $34.4k) | **−$90.9k** (was $22.0k) |
| Customers needed for one salary | ~150 by M18 (was 27) | ~357 (was ~66) | ~1,075 (was ~225) |

**What happens** *(revised after red team)*:
- **The vendor absorbs the whole price drop.** The fee is a fixed 20% share of realized value, so revenue per node falls 58% in GLUT and 86% in SEVERE by M36 (model §2).
- **Fixed costs do not move.** The $2,500–3,000/month on-call and $400 E&O stay the same in every scenario, and they exceed C-74 revenue in all three.
- **Even BASE is negative.** The glut only deepens a loss that already exists at peak prices.

**Verdict (mission rule 6)** *(revised after red team)*:
- **C-74:** dead in every scenario, including BASE.
- **C-75:** indifferent to DRAM prices.
  - A glut makes the host-DRAM tier cheaper. Holding a prefix in DDR5 beats recomputing it if the prefix is reused at least every ~3.4 h, against ~1.35 h at 4Q26 prices (`research/phase2/B_notes.md` §2.3).
  - Sizing by reuse interval alone misprices the tier. Concurrent fetches from 8 GPUs (~440 GB/s over PCIe Gen5) can saturate a 12-channel DDR5-4800 socket (460.8 GB/s theoretical), so per-socket bandwidth and NUMA must be sized too (RT-PHY-DD4-07).
  - Red Hat, Tensormesh and NVIDIA are commoditizing the line regardless, and it is dropped.
- **C-73:** indifferent to DRAM prices, with no tailwind in any scenario.
- **Bundle:** it does not survive as a venture or as a side business. Only ad-hoc C-73 consulting remains.

---

## 13. Sources

Every URL is logged in `research/sources/*.jsonl` (mostly `p4-memory-efficiency.jsonl`; also `D.jsonl`, `v1-policy.jsonl`, `p3-audit-*.jsonl`), and copied with a carried-over note to `p4w-memory-efficiency.jsonl`.

- **Memory-savings evidence:**
  - https://par.nsf.gov/servlets/purl/10332477
  - https://lpc.events/event/4/contributions/561/attachments/363/596/Persistent_Memory_as_Memory.pdf
  - https://github.com/facebookincubator/senpai
  - https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/blockdev/zram.rst
- **Swap safety and Kubernetes:**
  - https://scaleops.com/blog/kubernetes-swap-gpu-workload-sizing/
  - https://www.kubernetes.dev/resources/keps/2400/
  - https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/2400-node-swap/kep.yaml
  - https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/cluster-administration/swap-memory-management.md
- **KV-cache offload:**
  - https://docs.lmcache.ai/getting_started/benchmarking.html
  - https://lmsys.org/blog/2025-09-10-sglang-hicache
  - https://llm-d.ai/docs/guide/Installation/tiered-prefix-cache/cpu
  - https://github.com/LMCache/LMCache
  - https://github.com/kvcache-ai/Mooncake
  - https://github.com/ai-dynamo/dynamo
  - https://aicybr.com/blog/red-hat-ai-3-5-enterprise-inference-agents
  - https://www.hpcwire.com/aiwire/2026/10/15/tensormesh-targets-redundant-llm-computation-with-enterprise-caching-platform/
  - https://pulse2.com/tensormesh-20-million-raised-to-scale-kv-caching-infrastructure-for-enterprise-ai-inference/
  - https://toolradar.com/tools/tensormesh/pricing
- **DRAM and server prices:**
  - https://www.trendforce.com/news/2025/12/05/exclusive-memory-crunch-hits-pcs-dell-hikes-prices-15-20-mid-december-lenovo-from-january-2026/
  - https://pcserverandparts.com/news/server-price-increases-lead-times-2026/
  - https://info.fusionww.com/blog/rdimm-shortages-and-the-shift-in-server-shipments
  - https://www.amcompute.com/appraisals/ddr4-64gb-rdimm
  - https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/
  - https://comtek.co.uk/?p=524116
  - https://www.servermonkey.com/blog/october-2026-enterprise-it-market-update.html
- **Cloud price check:** https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20261029175634/us-east-1/index.csv
- **Buyers and channel:**
  - https://www.richweb.com/news/vmware-to-proxmox-in-2026/
  - https://petronellatech.com/blog/proxmox-vs-vmware-2026-why-we-migrated-and-you-should-too
  - https://blog.leaseweb.com/2026/07/16/rising-server-cloud-prices-2026/
  - https://icer.msu.edu/news/important-information-about-icers-next-cluster-acquisition
  - https://it.arizona.edu/news/hpc-buy-opportunity
  - https://oarc.rutgers.edu/?p=4762
  - https://hpcf.umbc.edu/sp-2024-purchase
  - https://live.today.uic.edu/hpc-partnership-program-deadline-approaching-for-new-node-investments/
  - https://bfs.ucr.edu/news/2026/06/02/computer-purchasing-reminder-ongoing-pricing-increases-lead-time-impacts
  - https://www.advancedclustering.com/coming-soon-latest-edition-of-our-hpc-pricing-guide/
  - https://www.cloudmagazin.com/en/2026/03/18/vmware-broadcom-kostenfalle-2026-alternativen-proxmox-nutanix/
- **Competitors and pricing:**
  - https://scaleops.com/product/air-gapped/
  - https://scaleops.com/product/self-hosted/
  - https://raising.fi/news/scaleops-series-c-march-2026
  - https://multiples.vc/private-comps/scaleops
  - https://toolradar.com/tools/scaleops/pricing
  - https://www.costbench.com/software/cloud-cost-management/cast-ai/
  - https://costbench.com/software/cloud-cost-management/kubecost/
  - https://newsroom.ibm.com/blog-ibm-acquires-kubecost-to-broaden-hybrid-cloud-cost-management-capabilities
  - https://www.cloudbolt.io/company/news/cloudbolt-acquires-stormforge/
  - https://github.com/robusta-dev/krr
  - https://www.storagenewsletter.com/2025/09/12/software-defined-memory-kove-announces-benchmarks/
  - https://www.Supermicro.com/solutions/Solution_Brief_KoveSDM.pdf
  - https://www.blocksandfiles.com/ai-ml/2025/09/24/memverge-unveils-open-source-ai-memory-layer-for-llms/1603278
  - https://en.globes.co.il/en/article-intel-closes-granulate-lays-off-dozens-1001492599
  - https://ubuntu.com/pricing/pro
  - https://redresscompliance.com/red-hat-subscription-pillar
  - https://www.usage.ai/blogs/finops/tools/prosperops-pricing/
  - https://www.usage.ai/?p=6180
- **Policy and funding:**
  - https://www.govinfo.gov/content/pkg/FR-2026-02-17/html/2026-03065.htm
  - https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/
  - https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and
- **Phase 5 red-team sources** (`research/sources/p5r-memory-efficiency.jsonl`):
  - https://forum.proxmox.com/goto/post?id=358973
  - https://forum.proxmox.com/goto/post?id=638846
  - https://lkml.iu.edu/hypermail/linux/kernel/2311.0/01961.html
  - https://lkml.iu.edu/hypermail/linux/kernel/2408.2/00974.html
  - https://docs.kernel.org/7.1/_sources/mm/hwpoison.rst.txt
  - https://lkml.iu.edu/hypermail/linux/kernel/2502.3/07004.html
  - https://www.insureon.com/small-business-insurance/errors-omissions/buy-for-less
  - https://www.quotesweep.com/blog/tech-startup-insurance-cost
  - https://www.mordorintelligence.com/industry-reports/server-dram-market
  - https://www.researchandmarkets.com/reports/6261263/registered-dimm-load-reduced-dimm-market-share
  - https://www.servermonkey.com/blog/may-2026-enterprise-it-hardware-market-update.html

---

## 14. Red-team outcome

**Reviewers:** VET (30-year DRAM process veteran), VC (semiconductor VC), HYP (hyperscaler procurement lead) and PHY (condensed-matter physicist), all in `research/phase5/rt_*.json`.
- **Objections:** 24 on DD4: 1 FATAL, 17 MAJOR, 6 MINOR.
- **Responses:** every response is recorded in full in `research/phase5/responses_memory-efficiency.json`, and each one was checked against the model. Where a reviewer gave a number, I re-ran it, and every quoted run reproduced. One run, HYP's −$4.5k cash low, turned out to be for the whole bundle; for C-74 alone the same costs give −$40.6k.

**Dispositions:**

| Disposition | Count |
|---|---|
| ACCEPTED-KILL | 4 |
| ACCEPTED-DOWNGRADE | 15 |
| ACCEPTED-MITIGATED | 5 |
| REFUTED | 0 |

Two objections were partly refuted on magnitude while their substance was accepted:
- **RT-VC-DD4-02:** the reviewer's own formula gives 44% in BASE, not "near zero".
- **RT-PHY-DD4-01 / RT-VET-DD4-01:** DIMM-step quantization averages out across buyers but splits them into winners and losers on each PO.

### 14.1 Objection table

| Objection | Severity | Disposition | Action |
|---|---|---|---|
| RT-VET-DD4-01 | MAJOR | ACCEPTED-DOWNGRADE | DIMM steps modeled as lost conversion (pilot_to_sub 0.60→0.40). Reopen PASS needs written POs showing fewer DIMMs or fewer nodes |
| RT-VET-DD4-02 | MAJOR | ACCEPTED-DOWNGRADE | reclaim_frac 0.10→0.06, counted only above stock Proxmox (KSM on). Never enable cross-tenant KSM |
| RT-VET-DD4-03 | MAJOR | ACCEPTED-DOWNGRADE | HPC rows 4–7 and the 15 RC targets dropped; row 8 demoted; scan_to_pilot 0.40→0.30 |
| RT-VET-DD4-04 | MAJOR | **ACCEPTED-KILL** | On-call $750/$2k → $2,500/$3,000 a month. C-74 loaded GM is now −473%. Reopen needs a ≤$1k retainer |
| RT-VET-DD4-05 | MAJOR | ACCEPTED-DOWNGRADE | ddr5_share 0.60→0.40. Reopen needs a census of ≥10 fleets with ≥50% of node-GB on DDR5 |
| RT-VC-DD4-01 | FATAL | **ACCEPTED-KILL** | ~$6k experiment cancelled and C-74 killed at $0. $0 reopen watch: a ≥4,500-node DDR5 channel plus ≤$1k on-call, by 2027-03-31 |
| RT-VC-DD4-02 | MAJOR | ACCEPTED-DOWNGRADE | value_realization 1.0→0.75 (rental equivalent); 12-month contracts tied to a named PO |
| RT-VC-DD4-03 | MAJOR | ACCEPTED-DOWNGRADE | Same reclaim cut. Reopen bar is ≥10% incremental on production MSP hosts with KSM left in its default state |
| RT-VC-DD4-04 | MAJOR | **ACCEPTED-KILL** | Same on-call revision. Reopen needs a signed retainer of ≤$1k/month with ≤1–2 h SLA |
| RT-VC-DD4-05 | MAJOR | ACCEPTED-DOWNGRADE | scan_to_pilot 0.30; SOC 2 trigger 5→2 customers. LOI signers must not have had zswap on before the scan |
| RT-VC-DD4-06 | MINOR | ACCEPTED-DOWNGRADE | c73_rate_pt 0.33→0.17. C-73 is no longer called a "cash bridge"; it needs 3 committed audits by 2026-11-30 or it is dropped |
| RT-HYP-DD4-01 | MAJOR | ACCEPTED-DOWNGRADE | savings_share 0.30→0.20; invoices tied to measured PO events |
| RT-HYP-DD4-02 | MAJOR | ACCEPTED-DOWNGRADE | reclaim_frac 0.06. The protocol's baseline is stock Proxmox (KSM, ksmtuned and ballooning at defaults) |
| RT-HYP-DD4-03 | MAJOR | ACCEPTED-DOWNGRADE | Kubernetes segment removed from C-74 now; the K8s node is removed from the test |
| RT-HYP-DD4-04 | MAJOR | **ACCEPTED-KILL** | On-call/E&O revised (E&O $200→$400, evidence-based, not $600). C-75 off in the headline. C-74 standalone ends at −$112.3k |
| RT-HYP-DD4-05 | MAJOR | ACCEPTED-DOWNGRADE | Kill-9 stop rule added to the model (fires at M22 GLUT, M20 SEVERE, never in BASE); new kill criterion: ≥5 subscriptions by 2027-12-31 |
| RT-HYP-DD4-06 | MINOR | ACCEPTED-DOWNGRADE | ddr5_share 0.40. Reopen needs ≥15 of 60 targets to confirm majority-DDR5 fleets |
| RT-PHY-DD4-01 | MAJOR | ACCEPTED-DOWNGRADE | Same as VET-01. Bill only at procurement events |
| RT-PHY-DD4-02 | MAJOR | ACCEPTED-MITIGATED | Reclaim redefined as the lowest memory.max or balloon target that holds p99 and PSI, split into anonymous and file memory. CI-runner host replaced |
| RT-PHY-DD4-03 | MAJOR | ACCEPTED-DOWNGRADE | Same as VET-03; scope is VM hosts only |
| RT-PHY-DD4-04 | MINOR | ACCEPTED-MITIGATED | Scanner reports hugepage, SEV-SNP/TDX and KSM state per host; those hosts are excluded from billing and from the average |
| RT-PHY-DD4-05 | MINOR | ACCEPTED-MITIGATED | zswap-only (memory.zswap.writeback=0) on boot media; writes/day tracked against TBW; fallback above 0.1 DWPD |
| RT-PHY-DD4-06 | MINOR | ACCEPTED-MITIGATED | SOW and kill criterion 4 exclude hardware-UE panics logged by MCE/EDAC; kdump required. Expected rate ~0.18/yr at the revised scale |
| RT-PHY-DD4-07 | MINOR | ACCEPTED-MITIGATED | C-75 off in the headline. Any consulting sizes for per-socket bandwidth and NUMA |

### 14.2 Changes made

**Model** (`models/memory-efficiency.py`, RED-TEAM REVISIONS (Phase 5) block; old → new):
- `reclaim_frac` 0.10 → 0.06
- `savings_share` 0.30 → 0.20
- `value_realization` (new) 1.0 → 0.75
- `ddr5_share` 0.60 → 0.40
- `oncall_small` $750 → $2,500
- `oncall_large` $2,000 → $3,000
- `insurance_pm` $200 → $400
- `scan_to_pilot` 0.40 → 0.30
- `pilot_to_sub` 0.60 → 0.40
- `soc2_trigger_customers` 5 → 2
- `acq_stop_price_frac` (new) 0 → 0.60, which wires kill criterion 9 into the simulation
- `c75_enabled` 1 → 0
- `c73_rate_pt` 0.33 → 0.17

**Other model changes:**
- **New model §0:** a Phase 4 vs Phase 5 comparison and a one-change-at-a-time table.
- **Sensitivity rows** for the revised case.
- **Channel threshold in §7.**
- **Phase 4 reproduction:** setting `APPLY_RED_TEAM = False` reproduces Phase 4 exactly.
- **Output:** the model re-ran (exit 0) and overwrote `research/phase4/memory-efficiency_model_output.md`.

**Document changes:**
- **§0:** status, capital tier, verdicts and recommendation revised.
- **§1:** ledger example annotated.
- **§2:** rewritten with revised numbers and the Phase 4 "was" values.
- **§3:** Kubernetes, the HPC rows and row 8 removed.
- **§4:** fee and pricing revised; the 90-day plan cancelled.
- **§5:** Kubernetes exited.
- **§7:** E&O, SOC 2 and the incident definition revised.
- **§8:** roadmap superseded.
- **§9:** on-call cost revised.
- **§10:** the experiment cancelled; a $0 reopen watch and a revised measurement protocol added.
- **§11:** kill criteria revised; kill 0 has fired.
- **§12:** cycle test revised.

**Logs:** sources are in `research/sources/p5r-memory-efficiency.jsonl` (5 searches) and assumptions in `research/assumptions/p5r-memory-efficiency.md`.

### 14.3 Revised headline economics (re-run model, from $40k)

| | BASE | GLUT | SEVERE |
|---|---|---|---|
| Fee supported at peak, $/node/month | $1.66 (was $7.36) | $1.66 | $1.66 |
| ARR M18 | **$3.8k** (was $37.7k) | $3.8k | $3.8k |
| ARR M36 | **$7.1k** (was $68.7k) | **$2.5k** (was $37.9k) | **$1.2k** (was $16.9k) |
| Breakeven (trailing 3-month net ≥ 0) | **never** (was M10) | never | never |
| Cash below $0 from | M12 (2027-10) | M12 | M12 |
| Cash at M36 | −$95.7k | −$90.8k | −$90.9k |
| Founder full-time | **never** | never | never |

**Best revised cases:**
- **Kill test passes at its bar** (10% reclaim, 60% DDR5): ARR $14.8k at M36, cash −$85.4k.
- **Everything +30%:** ARR $21.1k, cash −$23.2k.
- **C-75 back on:** ARR $17.7k, cash −$62.6k.

**If the founder had followed the Phase 4 plan:** the first gate (2027-07-31, M9) would have stopped them after spending ~$31.3k.

### 14.4 Revised verdicts

- **POSSIBLE? Yes technically, but smaller and lumpier than claimed.**
  - **Reclaim on the beachhead:** ~5–7% incremental over stock Proxmox, which already runs KSM.
  - **Some hosts free nothing:** reclaim is ~0 on hugepage-backed or SEV-SNP/TDX hosts.
  - **No usable capacity on Kubernetes or HPC.** Their schedulers allocate on requests, so freed pages are not resold.
- **PROFITABLE? No.**
  - **Revenue vs fixed cost:** $1.66 per node per month against $2,500–3,000 a month of on-call plus $400 of E&O.
  - **BASE:** ARR is $3.8k at M18 and $7.1k at M36, the model never breaks even, and the $40k is gone by M12.
  - **Kill test passed in full:** it still loses money.
- **DOABLE BY THIS FOUNDER? No.**
  - **On-call:** the business needs a 24/7 kernel responder that a part-time founder with a day job cannot be or afford.
  - **Channel:** the only route that raises the ceiling needs a ≥4,500-node DDR5 partner, and an operator that size has its own kernel staff.

### 14.5 FINAL STATUS: **KILLED**

**Reason.** After the accepted objections:
- **The fee collapses.** The value-supported C-74 fee falls 77%, from $7.36 to $1.66 per node per month. The causes compound: KSM is already on, the DDR5 share is smaller, the value is a rental equivalent rather than a purchase, and the take on a counterfactual saving is smaller.
- **Fixed costs rise.** Credible on-call plus E&O costs ~$2,900–3,400 a month, about three times the Phase 4 figure of $950 at 1–5 customers.
- **So the subscription loses money at every customer count the part-time funnel can reach,** and no pass outcome of the kill test changes that.

**What happens to each line:**
- **C-74:** killed at $0, and the ~$6k experiment is not run.
- **C-75:** dropped, as Phase 4 already recommended.
- **C-73:** survives only as ad-hoc consulting (~2 audits a year), and is dropped if 3 committed audits do not appear by 2026-11-30.

**Reopen watch:** C-74 reopens only if both §10.2 conditions arrive, at no cost, by 2027-03-31.
