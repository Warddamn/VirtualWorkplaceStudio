# DD4 — Memory Efficiency for On-Prem & Self-Hosted Fleets

**Slug:** `memory-efficiency` · **Author:** `p4w-memory-efficiency` · **As of:** 2026-11-01
**Model:** `models/memory-efficiency.py` (re-run 2026-11-01, exit 0; output in `research/phase4/memory-efficiency_model_output.md`). Section numbers written "model §N" refer to that output.
**Research base:** `research/phase4/memory-efficiency_notes.md`, `research/sources/p4-memory-efficiency.jsonl`, `research/assumptions/p4-memory-efficiency.md`.
**Tags:** [REPORTED-P] = primary page seen only as a search snippet; other tags per `CONVENTIONS.md`. Model month 1 = 2026-11; month 36 = 2029-10.

---

## 0. Header

**Name:** Memory Efficiency for On-Prem & Self-Hosted Fleets.

**Pitch:** A guarded Linux agent that frees about 10% of installed RAM on 20–200-node on-prem and colo fleets, so operators buying DDR5 servers at 2026 prices can put off DIMM purchases. The customer pays 30% of the DRAM they did not have to buy. A cloud memory audit and KV-cache integration work bring in cash along the way.

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
- **As modeled, T0.** The kernel contractor is scoped to a 100-hour MVP ($17.5k). The cash low point is $10.4k out of $40k (model §5).
- **As specified on the card, T1.** About 300 contractor hours cost $45–60k (`concepts_master.json` C-74).

**Scores** (`scores.csv`; 3 scorers; total, with rank of 40 survivors in parentheses):

| ID | Default | Capital-constrained | Moonshot | 5-yr ceiling band (`03_SCORING.md` §6) |
|---|---|---|---|---|
| C-73 | 82.0 (#1) | 85.0 (#1) | 76.7 (#1) | < $0.5M |
| C-75 | 76.0 (#7) | 78.3 (#8) | 71.7 (#9) | < $0.5M |
| C-74 | 74.0 (#10) | 74.2 (#13) | 73.3 (#8) | $0.5–2M |

The high totals reflect the rubric, not the business. C-73, the T0 software anchor, scores 5 on capital, time to revenue and founder fit. Moat (1–2) and competition (1–3) together carry only 15% of the weight (`03_SCORING.md` §6).

**Verdicts:**
- **POSSIBLE? Yes.** Every mechanism is in upstream Linux, vLLM or LMCache and runs in production: Meta saves 20–32% of memory and Google ~5% of fleet RAM. What is not known is how much a third party can safely free on a stranger's fleet. A realistic range is 5–15% [ESTIMATE: between Google's ~5% zswap figure and DAMON_RECLAIM's 32–40% lab results; research notes §1.1].
- **PROFITABLE? No, not as a venture. At best it is a marginal side business.**
  - **BASE:** ARR is $37.7k at month 18 and $68.7k at month 36, and the founder never goes full-time.
  - **GLUT:** ARR is $37.9k at month 36.
  - **SEVERE:** ARR is $16.9k, and the C-74 subscription runs at a −3% gross margin (model §5).
- **DOABLE BY THIS FOUNDER? Marginal.**
  - **In their skills:** the scanner, the control plane and the selling.
  - **Not in their skills:** SLO-safe kernel tuning needs a paid kernel engineer on call, and C-75 needs GPU-serving credibility the founder does not have.
  - **Too slow part-time:** the funnel yields ~0.37 customers a month against the ~2.5 needed to pay a salary (model §7).

**Recommendation:** demote DD4.
- **C-74:** run the 30-day kill experiment (§10); continue only if DDR5-buying operators sign paid pilots before 2027-Q2.
- **C-75:** drop it, apart from opportunistic consulting.
- **C-73:** keep it only as a cash bridge.

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

**C-75** applies the same idea to self-hosted AI models. While a language model reads a long prompt, it builds a "KV cache," its working notes, in scarce GPU memory. If the same long prefix comes back, such as a shared system prompt or a document being queried again, those notes can be fetched from cheaper server RAM instead of being recomputed. Vendor tests show the wait for the first token falling 50–80% on repeated long contexts ([LMCache docs](https://docs.lmcache.ai/getting_started/benchmarking.html); [LMSYS, 2025-09-10](https://lmsys.org/blog/2025-09-10-sglang-hicache)) [REPORTED]. Mixed workloads see only a 28% cut ([llm-d](https://llm-d.ai/docs/guide/Installation/tiered-prefix-cache/cpu)) [REPORTED-P]. We would install the tier and size it.

**C-73** is a one-off report right-sizing memory-heavy AWS instances.

---

## 2. Cost and unit-economics model

All numbers come from `models/memory-efficiency.py` unless a source is cited. The DDR5 value per GB is imported live from `models/dram_cost_stack.py`. It is $25.78 per user-GB of 64GB RDIMM at the 4Q26 contract price and $10.31 in the A-05 glut (`01_LANDSCAPE.md` §4.3). The severe case is $2.58 [ESTIMATE: the landscape's $2.04/GB severe component price × the model's 1.266 RDIMM-to-component ratio].

### 2.1 What one node is worth (C-74 value driver, model §2)

| Scenario / month | DDR5 RDIMM $/GB | One-time deferred value per node | Fee the value supports, $/node/mo | MRR per 80-node customer |
|---|---|---|---|---|
| Peak (2026-11) | 25.78 | $883 | 7.36 | $589 |
| BASE 2029-10 | 18.05 | $618 | 5.15 | $412 |
| GLUT 2029-10 | 10.31 | $362 | 3.02 | $242 |
| SEVERE 2029-10 | 2.58 | $106 | 0.88 | $71 |

**How the value is computed.** 512 GB × 10% reclaim = 51.2 GB freed. 60% of that is valued at the DDR5 price and 40% at the used-DDR4 price of $4.45/GB ([amcompute, 2026-08](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm)) [REPORTED].

**How the fee is set.** It is 30% of that value spread over 36 months. Savings-share vendors take about the same: ProsperOps ~30–35% and Zesty 25% ([Usage.ai](https://www.usage.ai/blogs/finops/tools/prosperops-pricing/); [Usage.ai](https://www.usage.ai/?p=6180)) [REPORTED]. The fee is capped at a $10/node/month list price.

A pure-DDR4 node is worth only $228, once, so DDR4 fleets cannot pay. The $10 list price would equal 41% of peak value, so the value cap binds first.

### 2.2 Unit economics by line (BASE, steady state, model §3)

| Line | Price | COGS | Gross margin | CAC | Payback | LTV (gross profit) |
|---|---|---|---|---|---|---|
| C-74 subscription (80 nodes) | $589/mo | $79 variable + $289 on-call allocation | 87% variable / **37% loaded** | $1,000 + 66 founder h | **27.1 mo** | $14,708 |
| C-74 paid pilot (60 days) | $2,000 | $2,100 | −5% | — | — | — |
| C-73 audit | $3,000 | $150 + 14 h | 95% cash / 60% labor-loaded | network | — | $2,850 |
| C-73 monitoring | $250/mo | $25/mo | 90% | 10 audits per sub | — | $3,750 |
| C-75 engagement | $25,000 | $10,000 + 40 h | 60% / 48% | $6,000 benchmark (once) | — | $15,000 |
| C-75 retainer | $1,500/mo | 30% | 70% | from engagement | — | $26,250 |

**C-74 funnel.** The conversion chain is reply 8% × scan 35% × pilot 40% × close 60% = 0.67%. That means 149 outbound touches per customer at peak pain [ESTIMATE; no on-prem benchmark exists]. Part-time capacity is 40 touches a month, plus inbound that ramps to 4 conversations a month by month 15.

**The loaded margin is the real one.** One incident can end the company, so a kernel-savvy on-call retainer ($750–2,000/month) is a cost of goods, not an option.

### 2.3 Headline results (from $40k, model §5)

| | BASE | GLUT | SEVERE |
|---|---|---|---|
| ARR M12 / M18 / M24 / M36 | $12.9k / $37.7k / $56.1k / $68.7k | $12.9k / $37.2k / $48.0k / $37.9k | $12.9k / $37.0k / $41.5k / $16.9k |
| C-74 customers M12 / M18 / M24 / M36 | 1.4 / 4.1 / 6.9 / 10.8 | 1.4 / 4.1 / 6.5 / 8.9 | 1.4 / 4.0 / 6.2 / 7.2 |
| Revenue, 36 months | $229.7k | $194.3k | $171.1k |
| Blended GM / C-74 sub GM | 44% / 37% | 40% / 21% | 37% / −3% |
| First revenue | M5 (2027-03), C-73 audit | same | same |
| Breakeven (trailing 3-mo net ≥ 0, founder unpaid) | M10 (2027-08) | M10 | M10 |
| Sustained breakeven | M23 (2028-09) | M23 | never |
| Cash low point | $10.4k at M8 | $10.4k at M8 | $10.4k at M8 |
| Cash at M36 | $55.7k | $34.4k | $22.0k |
| Founder full-time | never | never | never |

**Caveats** [ESTIMATE: arithmetic on the model's monthly tables]:
- Recurring revenue is only 18% of monthly revenue at M12 and 40% at M18; the rest is audits, pilots and engagements.
- Breakeven is founder-unpaid, and it breaks at M20 when the $12k SOC 2 Type I cost lands.
- If the kill experiment's ~$6k is fully additional to the build budget, the cash low point falls to about $4.4k.

### 2.4 Sensitivity (±30%, model §6)

| Case (BASE) | ARR M18 | ARR M36 | Cash low | Cash M36 |
|---|---|---|---|---|
| Base | $37.7k | $68.7k | $10.4k | $55.7k |
| Price −30% | $26.4k | $48.1k | **−$9.6k @M33** | −$9.1k |
| Conversion −30% | $14.4k | $25.6k | $10.3k | $29.4k |
| Reclaim 5% (Google-like) | $23.0k | $40.3k | $9.4k | $18.1k |
| Reclaim 20% (low end of TMO) | $48.3k | $122.1k | $10.5k | $104.6k |
| Drop C-75 | $30.5k | $58.2k | $5.2k | $22.6k |
| Everything +30% | $104.4k | $313.1k | $13.9k | $306.6k |

**The best case still misses the bar.** With every lever 30% better, the founder goes full-time in M20 (2028-06) and M36 ARR is $313k ($167.6k GLUT, $73.0k SEVERE). Conversion moves ARR most, then reclaim; the kill experiment measures both.

### 2.5 What must be true (model §7)

**What it takes to pay one $10k/month salary from C-74:**

| Scenario | Fee the value supports | Customers needed (80 nodes each) |
|---|---|---|
| BASE, by M18 | $7.36/node | **27** (2,157 nodes). The model delivers 4.1, a ~7× shortfall |
| GLUT, at M36 | $3.02/node | ~66 |
| SEVERE, at M36 | $0.88/node | ~225 |

**The part-time funnel cannot close the gap.** Hitting the BASE target means ~2.5 new customers a month from M8. The funnel makes ~0.37.

**Also required:**
- (a) ≥10% of installed RAM can be freed on a stranger's fleet without p99 or OOM regressions.
- (b) Target fleets are mostly DDR5 and still buying in 2027.
- (c) One swap incident does not end the company.
- (d) Buyers pay to have free upstream features tuned instead of doing it themselves.

---

## 3. Target customer and the first ten customers

**The buyer is defined by DRAM generation, not by industry.** They run a 20–200-node Proxmox/KVM or on-prem Kubernetes fleet, plan to buy DDR5 servers in 2026–27, and have no kernel team.

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

**Order of contact:** rows 1, 2, 4, 5 and 8 first: most likely to buy DDR5 hosts in 2027, least likely to have a kernel team. Series A–C SaaS firms with $20–200k/month AWS bills are C-73 audit prospects only.

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
| C-74 subscription | The lower of (30% × deferred DRAM value ÷ 36 months) and $10/node/month. That is $7.36/node at the peak, or $589/month for 80 nodes. Annual contracts reprice at renewal |
| C-73 | $3,000 audit; $250/month monitoring |
| C-75 | $25,000 integration plus $1,500/month retainer |

The pitch to the customer is: "You keep 70% of the DRAM you didn't buy: a 3.3× return" (model §2).

**What they already pay for.** On-prem operators already pay per server for support: Ubuntu Pro costs $500 per server per year, or $1,775 with 24/7 support ([Canonical](https://ubuntu.com/pricing/pro)) [REPORTED-P]. A memory add-on can draw on that budget line.

**Sales motion:** scan → readout call that turns cold GB into dollars → paid pilot with SLO guardrails written into the SOW → annual subscription.
- **Who sells:** the founder.
- **Who delivers:** the kernel contractor handles pilot calls and on-call.
- **Contract terms:** the MSA caps liability, and tech E&O insurance starts at the first pilot ($200/month in the model).

**First 90 days of selling** (assumes the §10 experiment passed on 2026-12-01):
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
  - tech E&O and cyber insurance are mandatory from the first pilot (model $200/month);
  - SOWs must name the SLO guardrails and the automatic-rollback behavior.
- **Swap safety and encryption.** Kubernetes guidance says to encrypt swap and use fast NVMe ([K8s swap docs](https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/cluster-administration/swap-memory-management.md)). zswap is outside the scope of KEP-2400 ([Kubernetes](https://www.kubernetes.dev/resources/keps/2400/)) [REPORTED-P], so on Kubernetes the agent has to stay on supported paths.
- **SOC 2 Type I.** Expected at about the 5th customer. The model books $12k at M20.
- **C-75 brings HIPAA.** KV tiers persist prompts to host DRAM and NVMe. Prompts at health-tech buyers may contain PHI, which means a BAA and encryption at rest.
- **University purchasing.** Quotes, POs and vendor registration can add 30–90 days to a sale [UNVERIFIED].

**Possible glut hedge** [UNVERIFIED]. NDAA FY2023 §5949 takes effect 2027-12-23; the FAR rule is only proposed ([GovInfo, 2026-02-17](https://www.govinfo.gov/content/pkg/FR-2026-02-17/html/2026-03065.htm)). If its grant-funds clause reaches federally funded university clusters, "clean" DDR5 could stay dearer for exactly the research-computing segment. Not modeled.

**Non-dilutive funding:**
- **SBIR/STTR is reauthorized through 2031-09-30** ([IEDC, 2026-04-15](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)) [REPORTED].
- **SBIR is closed to the founder for now.** The SBIR PI must spend more than half their time employed by the small business ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)) [REPORTED-P], so a founder who keeps their day job cannot be PI.
- **STTR with a university PI is the route** (e.g., an OS or memory-systems faculty member doing tiering research); topic fit with DOE ASCR or NSF systems programs is [UNVERIFIED]. Phase I money would not arrive before month 18, and grants are funding, not revenue (A-04). Pursue it only if a faculty partner appears during the university sales motion.

**Whether to raise:** don't.
No venture investor funds an on-prem tuning service at $17k–$313k ARR at M36 (model §5–6) against ScaleOps' $210M in the same category. Bootstrap from the $40k and stop if the gates in §8 and §11 fail.

---

## 8. 18-month roadmap with milestones

Model months are shown as M#. "Expected" figures are the model's BASE expected values.

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
| **Kernel-savvy Linux memory contractor:** guardrails, pilots, on-call. The most important person | M1 (25 h kill test), M2–M5 build (100 h), then retainer | DAMON/zswap/MGLRU threads on LKML; Linux Plumbers Conference; ex-Red Hat, Canonical and SUSE kernel or support engineers; Proxmox forum power users [UNVERIFIED availability] | $175/h: $17.5k build; $2,100 per pilot; on-call $750/month (1–5 customers), $2,000 (6+) |
| **Kernel cofounder (alternative to the contractor)** | Before the first pilot, if one can be found | The same communities. Offer equity instead of retainer | Saves ~$24k/year of on-call at 6+ customers [ESTIMATE: 12 × $2,000]. It would also lift the founder-fit score |
| **Inference contractor** (C-75 only, and only if the gate passes) | M6 benchmark; per engagement after that | vLLM, LMCache and SGLang community channels; NYC/Boston vLLM and Ray meetups | $200/h; ~45 h per engagement; ~$3k for the benchmark |
| **SOC 2:** compliance tooling plus an auditor | At the 5th customer | Standard SOC 2 automation vendors and CPA firms | $12k (model) |
| **Insurance broker and lawyer** | M1 (LLC and MSA); first pilot (E&O) | Local East Coast tech-E&O brokers; a startup lawyer for the MSA liability cap | $1,500 setup; $200/month |

No sales hire: the model never affords one.

---

## 10. The cheapest experiment that could kill it

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

## 11. Explicit kill criteria

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

## 12. Cycle test

**The glut arrives before the customers do.** The model starts the turn in 2028-01 (M15), when there are only ~2.6 C-74 customers. That timing follows the 2028 downturn call (`01_LANDSCAPE.md` F2).

| | BASE (−30% over 2028) | GLUT (A-05, DDR5 −60%) | SEVERE (−90%) |
|---|---|---|---|
| DDR5 RDIMM $/user-GB at M36 | 18.05 | 10.31 | 2.58 |
| Deferred value per 512 GB node | $618 | $362 | $106 |
| Fee the value supports, $/node/month | 5.15 | 3.02 | 0.88 |
| C-74 customers at M36 | 10.8 | 8.9 | 7.2 |
| ARR at M24 → M36 | $56.1k → $68.7k | $48.0k → $37.9k | $41.5k → $16.9k |
| C-74 subscription GM (36 months) | 37% | 21% | **−3%** |
| Monthly net at M36 | +$2,862 | +$591 | **−$839** (negative from M29) |
| Cash at M36 | $55.7k | $34.4k | $22.0k |
| Customers needed for one salary | 27 by M18 | ~66 | ~225 |

**What happens:** the fee is a fixed 30% share, so the customer keeps 3.3× and the vendor absorbs the whole price drop: revenue per node falls 59% in GLUT and 88% in SEVERE (model §2), while churn rises as "just buy RAM" gets cheaper. The $2,000/month on-call retainer does not shrink, which is why subscription GM goes negative in SEVERE. There, C-74 is only ~38% of M36 ARR; C-75 retainers and C-73 make up the rest [ESTIMATE: arithmetic on model §4c].

**Verdict (mission rule 6):**
- **C-74:** partly dies in GLUT (a hobby business at ~$38k ARR) and dies in SEVERE.
- **C-75:** indifferent to DRAM prices. A glut makes the host-DRAM tier cheaper: holding a prefix in DDR5 beats recomputing it if reused at least every ~3.4 h, against ~1.35 h at 4Q26 prices (`research/phase2/B_notes.md` §2.3). But the line is being commoditized by Red Hat, Tensormesh and NVIDIA regardless, and the model cuts deal flow 20% for the AI-capex slowdown a glut implies.
- **C-73:** indifferent to DRAM prices and has no tailwind in any scenario.
- **The bundle survives the glut only as a side business, never as a venture.**

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
