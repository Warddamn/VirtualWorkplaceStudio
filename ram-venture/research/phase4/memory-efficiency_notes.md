# DD4 — Memory Efficiency for On-Prem & Self-Hosted Fleets: research notes

**Agent:** `p4-memory-efficiency` · **As of:** 2026-11-01 · **Bundle:** anchor C-73 (cloud memory FinOps audit); folded in C-74 (on-prem reclaim autopilot) and C-75 (KV-cache tier integration)
**Model:** `models/memory-efficiency.py` (exit 0) → printed output in `research/phase4/memory-efficiency_model_output.md`
**Sources:** `research/sources/p4-memory-efficiency.jsonl` (90 entries) · **Assumptions:** `research/assumptions/p4-memory-efficiency.md`

> **Evidence grade.** I used all 28 of my WebSearch calls. My one WebFetch (kubernetes.io) failed DNS, so I stopped fetching, as instructed.
>
> - **Search snippets:** every new fact below rests on one, so nothing is **[VERIFIED]**. Primary pages seen only as snippets are tagged **[REPORTED-P]**; secondary or vendor pages are tagged **[REPORTED]**.
> - **Carried over:** some facts come from Phase 2/3 (agent D opened the AWS price list and the GitHub READMEs). They are marked "(carried over)".
> - **Network allowlist:** kubernetes.io has to be allowed in the session's network settings before the Kubernetes swap blog can be read in full.

---

## 0. Verdict (read this first)

**It is not a venture. It is, at best, a part-time services business, and its main line (C-74) loses most of its value in the 2028 turn.**

1. **The repositioning is correct but too small.** The shortage does hit on-prem and colo buyers:
   - **Server prices:** Dell, Lenovo and HPE raised server prices 10–20% [REPORTED].
   - **DIMM prices:** a 64GB RDIMM went from ~$255 to more than $900 between Q3-25 and Q1-26 [REPORTED].
   - **Hosting:** Hetzner and OVHcloud passed RAM costs through (OVH dedicated servers +16–100% in Aug-2026) [REPORTED].
   - **Universities:** they are buying smaller clusters [REPORTED].

   **The money per node is still tiny.** Reclaiming 10% of a 512 GB node frees 51 GB. On a DDR5-heavy fleet that defers **~$883 of DRAM, once**. At a 30% savings share, that supports a fee of **~$7.4/node/month at the peak**. A pure-DDR4 node is worth $228 once (`models/memory-efficiency.py` §2) [ESTIMATE].
2. **The glut arrives before the customers do.** The turn starts in 2028-01, which is month 15. The fee the value supports falls to **$3.0/node/month (GLUT)** and **$0.9/node/month (SEVERE)** by month 36. The model has only ~4 C-74 customers by month 18.
3. **C-75 is being commoditized now, not in 12 months:**
   - **Red Hat AI 3.5** (2026-09-09) ships vLLM CPU KV-cache offload as **GA** ([aicybr, 2026-09](https://aicybr.com/blog/red-hat-ai-3-5-enterprise-inference-agents)) [REPORTED].
   - **Tensormesh**, the LMCache company, launched an **on-prem enterprise KV-cache platform on 2026-10-15** ([HPCwire, 2026-10-15](https://www.hpcwire.com/aiwire/2026/10/15/tensormesh-targets-redundant-llm-computation-with-enterprise-caching-platform/)) [REPORTED].
   - **NVIDIA Dynamo KVBM** is free.
4. **C-73 has no tailwind and is no lead magnet for on-prem.**
   - **Prices did not move:** general EC2 list prices were unchanged from Sep-2025 to Oct-2026 (carried over, primary). I found no Azure or GCP memory-instance increase (§5).
   - **Wrong audience:** cloud SaaS buyers are not on-prem operators.
5. **Model headline** (from $40k; the founder never goes full-time in any scenario):

| | BASE | GLUT | SEVERE |
|---|---|---|---|
| Blended GM (36 mo) | 44% | 40% | 37% |
| C-74 subscription GM (36 mo, on-call loaded) | 37% | 21% | −3% |
| Breakeven (trailing-3-mo net ≥ 0, founder unpaid) | M10 (2027-08) | M10 | M10 (not sustained) |
| Cash low point | $10.4k at M8 | $10.4k at M8 | $10.4k at M8 |
| ARR M12 / M18 / M24 / M36 | $12.9k / $37.7k / $56.1k / $68.7k | $12.9k / $37.2k / $48.0k / $37.9k | $12.9k / $37.0k / $41.5k / $16.9k |
| C-74 customers at M18 / M36 | 4.1 / 10.8 | 4.1 / 8.9 | 4.0 / 7.2 |
| Customers needed to pay one $10k/mo salary | ~27 by M18 | ~66 at M36 prices | ~225 at M36 prices |

6. **The best case still fails the bar.** With every lever at +30% (price, conversion, churn −30%, COGS −30%), BASE reaches $104k ARR at M18 and $313k at M36. The founder goes full-time in M20. Even that misses "recurring revenue that becomes a venture."

**Recommendation for Phase 5/6:** demote DD4.
- **C-74:** keep only as a 30-day kill experiment (§11). Run it if, and only if, a DDR5-buying operator will sign a paid pilot before 2027-Q2.
- **C-75:** drop, apart from opportunistic consulting.
- **C-73:** drop as a venture line.

---

## 1. Q1 — Evidence of memory savings, and the failure modes

### 1.1 Host memory: compression, proactive reclaim, tiering

| Evidence | Result | Scale | Grade |
|---|---|---|---|
| **Meta TMO** (ASPLOS 2022) | Saves **20–32% of total memory** fleet-wide. PSI-based offload is upstream in Linux | Millions of Meta servers | [REPORTED-P] via p3-audit-11 ([NSF PAR](https://par.nsf.gov/servlets/purl/10332477)) |
| **Google software-defined far memory** (ASPLOS 2019) | zswap far memory deployed since 2016. The far-memory tier is ≥67% cheaper per GB. **About 20% of data is cold**, which gives a **4–5% DRAM TCO cut with no SLI change**. Cold share varies **1–52%** by machine | Google WSC fleet | [REPORTED-P] ([Google Research](https://research.google/pubs/software-defined-far-memory-in-warehouse-scale-computers/); [the morning paper, 2019-05-22](https://blog.acolyer.org/2019/05/22/sw-far-memory/)) |
| **Google LPC talk** | ~20% of RAM is allocated but cold (2-minute threshold). **Proactive zswap saves ~5% of total fleet RAM** | Fleet | [REPORTED-P] ([LPC](https://lpc.events/event/4/contributions/561/attachments/363/596/Persistent_Memory_as_Memory.pdf)) |
| **DAMON_RECLAIM** (Amazon, upstream since Linux 5.16) | **32% memory saving at 1.91% overhead** (RFC v2). **~40% at 3.38%** on zram (v3). **38.58% at 1.94%** (v5.15-rc5). The author calls these proof-of-concept results, not production | Lab benchmarks | [REPORTED-P] ([LKML v2](https://lkml.iu.edu/hypermail/linux/kernel/2106.1/00487.html); [LKML v3](https://lkml.iu.edu/hypermail/linux/kernel/2107.2/05374.html); [LKML](https://lkml.iu.edu/hypermail/linux/kernel/2110.2/03387.html); [Phoronix](https://www.phoronix.com/news/DAMON-Reclamation-Linux-5.16)) |
| **Senpai** (TMO userspace) | Kernel-build peak memory falls from 804 MB to 348 MB | Example | (carried over; D opened [GitHub](https://github.com/facebookincubator/senpai)) |
| **zram docs** | ~2:1 compression expected | Docs | (carried over) |
| **Kubernetes node swap** | GA in v1.34. In 2026 density tests, the latency rise at peak density came mainly from **CPU contention, not swap I/O**. GKE ships Node Memory Swap on Local SSD | Upstream | [REPORTED-P] ([Kubernetes blog, 2026-10-05](https://kubernetes.io/blog/2026/10/05/scaling-kubernetes-workloads-with-node-swap/)) |

**What a third party can realistically promise: 5–15% of installed RAM, not Meta's 20–32%.**
- **Why Meta gets more:** TMO's figure relies on in-house app tuning plus SSD offload, on workloads Meta controls.
- **Why a vendor gets less:** Google's zswap-only figure is ~5%, and DAMON's 32–40% is a lab result. A vendor on a stranger's fleet sits nearer Google's number until it earns trust.
- **Model:** base 10%; sensitivity at 5% and 20% (`models/memory-efficiency.py` §6) [ESTIMATE].

### 1.2 KV-cache offload (C-75)

| Evidence | Result | Grade |
|---|---|---|
| LMCache paper (arXiv 2510.09665) | **1.9–8.1× lower TTFT** at QPS 1; **2.3–14× throughput** at equal TTFT across five models | [REPORTED] preprint ([arXiv](https://arxiv.org/pdf/2510.09665)) |
| LMCache docs, Qwen3-8B | TTFT 0.757 s → 0.185 s (−75%); total time −41% | [REPORTED] vendor ([docs](https://docs.lmcache.ai/getting_started/benchmarking.html)) |
| LMCache blog, gpt-oss-120B | TTFT −67%; total query time −51% | [REPORTED] vendor ([blog](https://blog.lmcache.ai/2025-08-05-gpt-oss-support/)) |
| AWS SageMaker LMI | CPU offload: **2.65× faster TTFT**, 2.18× total latency. NVMe O_DIRECT: 1.57× | [REPORTED] ([repost](https://aihub.hkuspace.hku.hk/?p=5899)) |
| **llm-d, 16×H100 mixed workload** | **TTFT only −27.8%, throughput +21.7%**. **No benefit when KV fits in GPU** | [REPORTED-P] ([llm-d](https://llm-d.ai/docs/guide/Installation/tiered-prefix-cache/cpu)) |
| VAST/Backend.AI (2026-06-24), 8×H100, vLLM 0.20.0 | ~2× wall-clock and TTFT; warm turns 3.3× faster; **cold first turns ~4 s slower** | [REPORTED] ([VAST](https://www.vastdata.com/blog/vastdata-lablup-kvcache-offload-benchmark)) |
| SGLang HiCache (LMSYS, 2025-09-10) | Up to **6× throughput**, up to **80% lower TTFT**. Novita (3FS): TTFT −56%, hit rate 40% → 80% | [REPORTED] ([LMSYS](https://lmsys.org/blog/2025-09-10-sglang-hicache)) |
| Mooncake | Kimi serves 75% more requests within SLO | (carried over; vendor) |
| **NVIDIA Dynamo KVBM docs** | **No benefit if the CPU cache is smaller than the device cache.** Block churn can **degrade** performance, and too few prefix hits means no TTFT gain | [REPORTED-P] ([NVIDIA docs](https://docs.nvidia.com/dynamo/v1.0.0/components/kvbm/kvbm-guide)) |

**Takeaway.** The gains are real for long, repeated contexts: −50–80% TTFT in vendor tests. They are small for mixed workloads (−28% TTFT) and zero when KV fits in HBM. That spread is exactly why someone has to size and tune the DRAM tier per workload. The tuning is now a supported, GA feature in Red Hat AI 3.5 and in Tensormesh Platform. Branch B's math still holds: holding Llama-70B FP8 KV in DDR5 at 4Q26 prices beats recompute only if a prefix is reused at least once every ~1.35 h; in a glut that stretches to ~3.4 h (`research/phase2/B_notes.md` §2.3).

### 1.3 Failure modes (why one incident can end a small vendor)
- **Swap on a GPU inference node:** with `memory.swap.max` uncapped, p50 latency went from **14.2 s to 116.5 s** in a ScaleOps vendor benchmark ([ScaleOps](https://scaleops.com/blog/kubernetes-swap-gpu-workload-sizing/)) [REPORTED].
- **OOM ordering:** Kubernetes engineers saw the **OOM killer fire before eviction**, killing higher-priority pods that were not causing the pressure. They fixed it with `vm.min_free_kbytes` and `vm.watermark_scale_factor` ([Kubernetes blog, 2025-08-19](https://v1-34.docs.kubernetes.io/blog/2025/08/19/tuning-linux-swap-for-kubernetes-a-deep-dive)) [REPORTED-P].
- **zswap is outside KEP-2400** ([KEP](https://www.kubernetes.dev/resources/keps/2400/)). zswap also needs a physical backing swap device ([Proxmox forum](https://forum.proxmox.com/posts/848883/)) [REPORTED]. Swap degrades badly on throttled cloud disks, and the eviction manager does not account for swap (carried over, D).
- **KV tier:** cold first turns get slower (+4 s, VAST). A CPU tier that is too small causes block churn (NVIDIA).
- **DAMON/zram overhead** is 2–3.4% runtime in lab tests (LKML). Production overhead on mixed customer workloads is **unknown**.

---

## 2. Q2 — Who buys, how much the 2026 shortage hurts them, and whether they pay for savings software

### 2.1 On-prem and colo server buyers feel the shortage

| Signal | Detail | Grade |
|---|---|---|
| OEM price rises | Dell +15–20% from mid-Dec-2025. Lenovo quotes expired 2026-01-01 ([TrendForce News, 2025-12-05](https://www.trendforce.com/news/2025/12/05/exclusive-memory-crunch-hits-pcs-dell-hikes-prices-15-20-mid-december-lenovo-from-january-2026/)). Dell list +17% from 2026-03-30; HPE ProLiant +10–15% (reseller blog: [PC Server and Parts](https://pcserverandparts.com/news/how-much-does-a-server-cost-2026/)) | [REPORTED] |
| RDIMM prices | 64GB RDIMM ~$255 (Q3-25) → $450 (Q4-25) → >$900 (Q1-26), citing Counterpoint ([PC Server and Parts](https://pcserverandparts.com/news/server-price-increases-lead-times-2026/); [Network World](https://www.networkworld.com/article/4093752/server-memory-prices-could-double-by-2026-as-ai-demand-strains-supply.html)). Distributor 64GB DDR5-6400 approaching ~$3,000 (Jun-2026), and OEMs are short of DDR5 RDIMM ([Fusion](https://info.fusionww.com/blog/rdimm-shortages-and-the-shift-in-server-shipments)). Used 64GB DDR5 RDIMM $890–1,200 ([amcompute](https://www.amcompute.com/appraisals/ddr5-64gb-rdimm)). Canonical model deck: **$25.78 per user-GB contract** (`models/dram_cost_stack.py`) | [REPORTED]/[ESTIMATE] |
| Outlook | TrendForce expects server contract prices to rise through 2H27 ([ServerMonkey, 2026-10](https://www.servermonkey.com/blog/october-2026-enterprise-it-market-update.html)). "Buy servers now or cry later" ([The Register, 2026-01-14](https://www.theregister.com/2026/01/14/dram_infrastructure_costs/)) | [REPORTED] |
| Universities and HPC | **MSU ICER:** next cluster smaller than previous ones; CPU node prices ~4–5× and GPU ~2–3× in a year ([ICER](https://icer.msu.edu/news/important-information-about-icers-next-cluster-acquisition)). **UC Riverside:** price rise from 2026-06-01, lead times 6–14 weeks ([UCR](https://bfs.ucr.edu/news/2026/06/02/computer-purchasing-reminder-ongoing-pricing-increases-lead-time-impacts)). **U. Arizona:** node prices rising, buy early ([UArizona](https://it.arizona.edu/news/hpc-buy-opportunity)). **UBC Okanagan:** memory prioritization raises server prices ([UBCO](https://it.ok.ubc.ca/?p=21529)) | [REPORTED-P] |
| Hosting providers | **Hetzner:** rises from 2026-04-01 citing RAM/SSD ([heise](https://heise.de/-11185981)). **OVHcloud:** up to 87%; Aug-2026 dedicated +16–36% (Advance) to +74–100% (Game) ([ITdaily](https://itdaily.com/news/cloud/ovhcloud-price-increase-ram/); [OVHcloud](https://us.ovhcloud.com/resources/blog/dedicated-servers-price-change-for-the-second-half-of-2026/)). OVH memory options reportedly +68% to +652% for new orders ([Capital & Compute](https://capitalandcompute.net/hosting-price-hikes/), attribution [UNVERIFIED]). Leaseweb blogs about the 2026 price rises ([Leaseweb, 2026-07-16](https://blog.leaseweb.com/2026/07/16/rising-server-cloud-prices-2026/)) | [REPORTED] |
| Workarounds that compete with C-74 | Resellers push **refurbished DDR4 servers** as the shortage workaround ([Comtek](https://comtek.co.uk/?p=524116); [PC Server and Parts](https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/)) | [REPORTED] |

**Nuance that kills a lot of the TAM.**
- **Buy-used is the cheaper alternative.** Many named buyers (Proxmox MSPs, university HPC) run DDR4-era fleets and can top up with used 64GB DDR4 RDIMMs at $3.9–5.8/GB (p3-audit-11). For them, reclaim is worth about **one-sixth of the DDR5 figure per GB** ($4.45 vs $25.78).
- **Who the model targets:** operators who will **buy DDR5 servers in 2026–27**, with DDR5 assumed to be 60% of node-GB.

### 2.2 Self-hosted LLM teams (C-75)
- **Adoption is contested.** One Sep-2026 survey (n=200) puts open-weight models at **34% of enterprise token usage**, up from 23%, with 42% running them in production ([Techstrong.ai](https://techstrong.ai/articles/open-weight-ai-models-expected-to-capture-41-of-enterprise-token-usage/)). Menlo Ventures' survey (n=495) found enterprise open-source share **fell from 19% to 11%** ([IntuitionLabs summary](https://intuitionlabs.ai/articles/hosted-ai-api-vs-self-hosted-llm-cost)) [REPORTED].
- **No sector data.** I found no named health-system, law-firm or bank case study of a self-hosted vLLM cluster. One radar notes "growing" vLLM references in regulated case studies, with no names ([Rubinlake](https://rubinlake.com/pl/technology-radar/data-platforms-and-mlops/vllm)) [REPORTED].
- **Owned clusters need high utilization.** They break even only above ~50–83% sustained GPU utilization ([Iternal](https://iternal.ai/how-to-deploy-llm-on-premise)) [REPORTED]. So the buyer set is narrow.

### 2.3 Evidence that buyers pay for savings-based software
- **In cloud, yes, and at scale:**
  - **ScaleOps:** $130M Series C (2026-03-30) at a >$800M valuation, ~$210M raised in total ([raising.fi](https://raising.fi/news/scaleops-series-c-march-2026); [multiples.vc](https://multiples.vc/private-comps/scaleops)).
  - **CAST AI:** ~$1,000/month plus $5/vCPU/month ([CostBench](https://www.costbench.com/software/cloud-cost-management/cast-ai/)).
  - **Savings-share vendors:** ProsperOps takes ~30–35% of savings and Zesty 25% ([Usage.ai](https://www.usage.ai/blogs/finops/tools/prosperops-pricing/); [Usage.ai](https://www.usage.ai/?p=6180)) [REPORTED].
- **On-prem memory software specifically, thin evidence:**
  - **Kove:SDM:** claims customers but publishes no price ([StorageNewsletter, 2025-09-12](https://www.storagenewsletter.com/2025/09/12/software-defined-memory-kove-announces-benchmarks/)).
  - **MemVerge:** pivoted away from memory virtualization to AI memory (MemMachine) ([Blocks & Files, 2025-09-24](https://www.blocksandfiles.com/ai-ml/2025/09/24/memverge-unveils-open-source-ai-memory-layer-for-llms/1603278); [Yespress](https://yespress.io/memverge.md)).
  - **Granulate:** Intel shut it in Oct-2024 (carried over).
  - [REPORTED] — the pioneers of "software that makes RAM go further" either pivoted or died.

---

## 3. Q3 — Competitors and what they charge

| Competitor | What it does in this space | Price (2026) | Threat to |
|---|---|---|---|
| **ScaleOps** | K8s pod/node right-sizing. **Self-hosted and air-gapped, FIPS-compatible**, runs on OpenShift/Rancher ([ScaleOps](https://scaleops.com/product/air-gapped/)) | Custom. Aggregators say $500–2,000+/mo tiers, or a % of savings ([Toolradar](https://toolradar.com/tools/scaleops/pricing)) [REPORTED] | C-74 (on-prem K8s), C-73. $210M raised; publishes K8s swap benchmarks |
| **CAST AI** | Cloud K8s automation | Free monitoring tier; Growth ~$1,000/mo + $5/vCPU/mo ([CostBench](https://www.costbench.com/software/cloud-cost-management/cast-ai/)) [REPORTED] | C-73 |
| **StormForge (CloudBolt, acq. 2025-03-31)** | ML right-sizing | ~$3/vCPU/mo, single unverified listing ([TrustRadius](https://tr-web.dev.trustradius.com/compare-products/ibm-kubecost-vs-stormforge)); acquisition per [CloudBolt](https://www.cloudbolt.io/company/news/cloudbolt-acquires-stormforge/) | C-73, C-74 (K8s) |
| **IBM Kubecost (acq. Sep-2024)** / OpenCost | K8s cost visibility | Business ~$449/mo per 100 nodes ([CostBench](https://costbench.com/software/cloud-cost-management/kubecost/); [IBM](https://newsroom.ibm.com/blog-ibm-acquires-kubecost-to-broaden-hybrid-cloud-cost-management-capabilities)) [REPORTED] | C-73 |
| **AWS Compute Optimizer, Robusta KRR, VPA, Goldilocks** | Free right-sizing | $0 (carried over) | C-73 (free floor) |
| **Granulate (Intel)** | Runtime optimization | **Shut Oct-2024** (carried over) | Precedent |
| **MemVerge** | Pivoted to AI memory (MemMachine; Memory Machine AI/X/Batch) | n/a | No longer in on-prem DRAM reclaim |
| **Kove:SDM** | Software-defined remote memory; Supermicro partner ([Supermicro](https://www.Supermicro.com/solutions/Solution_Brief_KoveSDM.pdf)) | Not published | Adjacent (pooling, not reclaim) |
| **Linux upstream + Red Hat/Canonical** | zswap, zram, PSI, DAMON, KSM, `tuned` profiles, free. Support: Ubuntu Pro $500/server/yr, or $1,775 with 24/7 infra support ([Canonical](https://ubuntu.com/pricing/pro)). RHEL ~$349–1,499 per socket pair/yr ([Redress](https://redresscompliance.com/red-hat-subscription-pillar)) | Free features; support priced per server | **C-74's real competitor is DIY** |
| **Proxmox** | KSM built in; subscriptions ~€95–110/socket/yr (snippet) | — | C-74 |
| **Tensormesh** (LMCache) | $24.5M raised. Tensormesh Inference GA (May-2026). **Tensormesh Platform for on-prem enterprise (2026-10-15)**: tiered GPU/CPU/storage KV, security, observability, multi-tenancy ([HPCwire](https://www.hpcwire.com/aiwire/2026/10/15/tensormesh-targets-redundant-llm-computation-with-enterprise-caching-platform/); [TechIntelPro](https://techintelpro.com/news/ai/enterprise-ai/tensormesh-launches-platform-to-cut-llm-inference-costs-reusing-kv-cache)) | Custom quotes ([Toolradar](https://toolradar.com/tools/tensormesh/pricing)); serverless bills cached input tokens at $0 ([Pulse 2.0](https://pulse2.com/tensormesh-20-million-raised-to-scale-kv-caching-infrastructure-for-enterprise-ai-inference/)) | **C-75 (direct)** |
| **NVIDIA Dynamo KVBM** | Free Apache-2.0 GPU→CPU→SSD→remote KV tiering | $0 | C-75 |
| **Red Hat AI 3.5 / llm-d** | **CPU KV-cache offload GA** (2026-09-09), based on LMCache ([aicybr](https://aicybr.com/blog/red-hat-ai-3-5-enterprise-inference-agents); [Techzine](https://techzine.eu/blogs/infrastructure/131590/red-hat-lays-foundation-for-ai-inferencing-server-and-llm-d-project)) | Price not found | **C-75**: sells supported KV offload to the same regulated enterprises |
| WEKA, VAST, Pliops, Phison aiDAPTIV+ | Flash KV tiers (carried over) | — | C-75 |
| Percona-style OSS support | Not researched (quota) | — | Gap |

**Why we would win:** we probably would not. The only plausible edge is being the **East Coast, hands-on, DDR5-deferral specialist for 20–200-node Proxmox/K8s fleets**. That niche is too small for ScaleOps or Red Hat to chase, and too unsophisticated to DIY. It is a services moat, not a software moat.

---

## 4. Q4 — Evidence on pricing models

| Model | Evidence | Fit for C-74 |
|---|---|---|
| **% of savings** | ProsperOps ~30–35%, Zesty 25%, nOps savings share or flat fee ([nOps](https://www.nops.io/blog/prosperops-pricing/)). ScaleOps enterprise reportedly priced as a % of demonstrated savings (aggregator) | Natural fit for "DRAM not bought". **But the saving is a one-time capex deferral, not a monthly bill**, so it must be spread over a term. The model uses 30% of deferred value over 36 months |
| **Per node / per vCPU subscription** | Kubecost ~$4.5/node/mo; StormForge ~$3/vCPU/mo; CAST AI $5/vCPU/mo + base; Datadog infrastructure ~$15/host/mo ([CostBench](https://costbench.com/compare/datadog-vs-new-relic/)) | List cap set at $10/node/mo. **The value cap binds first**: $7.36/node/mo at the peak, $3.02 in the glut, $0.88 in severe |
| **Support contracts** | Ubuntu Pro $500–3,400/server/yr; RHEL $349–1,499 per socket pair/yr | Shows on-prem ops *do* pay per server for support. A "memory SLO support" add-on could ride this budget line |
| **One-time engagement + retainer** | C-75 card $15–40k plus retainer. Tensormesh and Red Hat now bundle the same capability | C-75 modeled at $25k plus $1.5k/mo |

**Implied economics** (`models/memory-efficiency.py` §2–3):
- **Value per node:** one-time value per 512 GB node at 10% reclaim is $883 (BASE peak), $362 (GLUT M36) and $106 (SEVERE M36).
- **Fee at $10/node/mo:** that would be **41% of peak value**, above the 25–35% take rates buyers accept.
- **Subscription margin:** variable gross margin is **87%**. Once the kernel on-call retainer is spread over ~7 customers, it is only **37%**.

---

## 5. Q5 — Did cloud memory-optimized prices change in 2026?

- **AWS: no change to general or memory-optimized EC2 list prices.**
  - **Primary diff:** agent D compared all 92 on-demand SKUs, including r7i, r8g, x2idn and u7i, between Sep-2025 and Oct-2026: identical (carried over, primary [AWS Price List](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20261029175634/us-east-1/index.csv)).
  - **Only GPUs moved:** EC2 Capacity Blocks for ML rose ~15% (2026-01-04) and ~20% (2026-07-01) ([The Register](https://www.theregister.com/2026/01/05/aws_price_increase/); [tech-insider](https://tech-insider.org/aws-ec2-capacity-blocks-price-hike-2026)) [REPORTED].
- **Azure and GCP: no published memory-optimized list increase found.** Commentary names AWS r-series, Azure E-series and GCP highmem as the most exposed, but offers projections only ([SoftwareSeni](https://www.softwareseni.com/how-memory-costs-are-reshaping-cloud-budgets-and-procurement-commitments/); [Readyset](https://readyset.io/blog/your-database-bill-is-climbing-faster-than-your-traffic): $386 → $415–500/mo *projected*) [REPORTED].
- **Tier-2 hosts did raise prices** (Hetzner, OVHcloud; §2.1). A C-73-style audit aimed at **renters of OVH/Hetzner bare metal** could find real new pain. That variant is untested and not modeled (assumption logged).
- **Conclusion: the scorers were right.** Hyperscaler customers feel no new memory pain, so C-73 is a 2024-vintage FinOps report.

---

## 6. Q6 — First ten customers (names or precise types, and where to find them)

| # | Candidate | Line | Why them | Where to find / evidence |
|---|---|---|---|---|
| 1 | **RichWeb** (Richmond, VA; HVENS Cloud) | C-74 | East Coast MSP/host moving customers from VMware to Proxmox in 2026, so it is buying or rebuilding hosts at 2026 DRAM prices | [richweb.com](https://www.richweb.com/news/vmware-to-proxmox-in-2026/) [REPORTED] |
| 2 | **Petronella Technology Group** (Raleigh, NC) | C-74 | MSP that migrated to Proxmox in 2026; KSM/zswap tuning on Proxmox hosts is a direct fit | [petronellatech.com](https://petronellatech.com/blog/proxmox-vs-vmware-2026-why-we-migrated-and-you-should-too) [REPORTED] |
| 3 | **Leaseweb USA** (Manassas, VA DC) | C-74 (design partner) | Publicly wrestling with 2026 server price rises. Likely to DIY; ask it to be a reference or test bed | [Leaseweb](https://blog.leaseweb.com/2026/07/16/rising-server-cloud-prices-2026/) [REPORTED] |
| 4 | **Michigan State ICER** | C-74 | Buying a smaller cluster because node prices jumped; memory reclaim stretches a fixed grant budget | [ICER](https://icer.msu.edu/news/important-information-about-icers-next-cluster-acquisition) [REPORTED-P] |
| 5 | **U. Arizona Research Computing** | C-74 | New cluster fall 2026, node prices rising; buy-in model means PIs pay per node | [UArizona](https://it.arizona.edu/news/hpc-buy-opportunity) [REPORTED-P] |
| 6 | **Rutgers OARC** (NJ) / **UMBC HPCF** (MD) / **UIC ACER** | C-74 | East Coast or nearby research-computing centers with periodic node buys. Pain not confirmed: these appeared in search results only ([Rutgers](https://oarc.rutgers.edu/?p=4762); [UMBC](https://hpcf.umbc.edu/sp-2024-purchase); [UIC](https://live.today.uic.edu/hpc-partnership-program-deadline-approaching-for-new-node-investments/)) | [UNVERIFIED] |
| 7 | **UC Riverside** campus IT | C-74 | Price rise from 2026-06-01, 6–14-week lead times | [UCR](https://bfs.ucr.edu/news/2026/06/02/computer-purchasing-reminder-ongoing-pricing-increases-lead-time-impacts) [REPORTED-P] |
| 8 | **Advanced Clustering Technologies** (HPC integrator) | Channel for C-74 | Publishes HPC pricing guides and flags memory pricing; could bundle "configure 10–20% less RAM plus reclaim agent" in quotes to universities | [Advanced Clustering](https://www.advancedclustering.com/coming-soon-latest-edition-of-our-hpc-pricing-guide/) [REPORTED] |
| 9 | **Refurbished-server resellers**: PC Server and Parts, ServerMonkey, Comtek | Channel for C-74 | Already sell "dodge the memory shortage" to SMB and colo buyers; a reclaim add-on raises their attach rate | [PC Server and Parts](https://pcserverandparts.com/news/refurbished-ddr4-server-memory-2026-server-ram-price-crisis/); [ServerMonkey](https://www.servermonkey.com/blog/october-2026-enterprise-it-market-update.html); [Comtek](https://comtek.co.uk/?p=524116) [REPORTED] |
| 10 | **Mid-market regulated teams self-hosting 70B-class models on 8–64 GPUs** (legal-tech, health-tech, fintech) | C-75 | Data residency; KV tier sizing. **No named firm found.** Find them via the vLLM/LMCache Slack, NYC/Boston vLLM and Ray meetups, Red Hat AI customer stories, and job posts naming vLLM plus HIPAA/SOC 2 | Type only [UNVERIFIED] |
| (+) | Series A–C SaaS with $20–200k/mo AWS bills, from the founder's network | C-73 | Cash bridge only | Type only |

**Kill-test ordering:** contact rows 1, 2, 4, 5 and 8 first. They are the most likely to be buying DDR5 hosts in 2027 and to lack a kernel team.

---

## 7. Q7 — Glut effect: does the business survive?

**Value per GB saved** (`models/dram_cost_stack.py` deck, per user-GB of 64GB DDR5 RDIMM): **$25.78 peak → $10.31 glut → $2.58 severe**. Component equivalents are $20.37, $8.15 and $2.04.

| | BASE M36 | GLUT M36 | SEVERE M36 |
|---|---|---|---|
| DDR5 RDIMM $/user-GB | 18.05 | 10.31 | 2.58 |
| Deferred value per 512 GB node (10% reclaim, 60% DDR5) | $618 | $362 | $106 |
| Value-capped fee $/node/mo | $5.15 | $3.02 | $0.88 |
| C-74 customers (model) | 10.8 | 8.9 | 7.2 |
| Total ARR | $68.7k | $37.9k | $16.9k |
| Cash at M36 (from $40k) | $55.7k | $34.4k | $22.0k |

- **GLUT:** the business survives as a hobby. ARR falls from a $48k peak (M24) to $38k, and C-74 subscription gross margin drops to 21%.
- **SEVERE:** C-74 subscriptions run at a negative gross margin (−3%), because the on-call cost exceeds the fees. Breakeven is never sustained. Only C-73 audits and C-75 services keep cash positive.
- **Cycle verdict (mission rule 6):** C-74 **partially dies** in GLUT and **dies** in SEVERE. C-75 is DRAM-indifferent but commoditizing. C-73 is DRAM-indifferent and tailwind-less.
- **One glut hedge [UNVERIFIED]:** if §5949's grant-funds clause applies, federally funded university clusters cannot buy CXMT-containing DIMMs from 2027-12-23. "Clean" DRAM could then stay dearer for exactly the university segment.

---

## 8. Channel evidence
- **VMware → Proxmox migration wave:**
  - Broadcom ended the VMware Cloud Service Provider program in Jan-2026 ([cloudmagazin, 2026-03-18](https://www.cloudmagazin.com/en/2026/03/18/vmware-broadcom-kostenfalle-2026-alternativen-proxmox-nutanix/)).
  - Smaller MSPs that cannot meet Broadcom commitments are moving customers to Proxmox ([cloudmagazin, 2026-04-13](https://www.cloudmagazin.com/en/2026/04/13/broadcomvmware-channel-provider-landscape-one-year-after/)) [REPORTED].
  - MSPs rebuilding clusters in 2026–27 are buying hosts at peak DRAM prices. This is the best-timed channel.
- **Refurbished-server resellers and HPC integrators** already market "shortage workarounds". They are a bundle or referral channel at ~20–30% rev share [ESTIMATE].
- **Open-source scanner as the lead magnet:** a free, read-only "cold-memory/DRAM-deferral scan" (DAMON sysfs, PSI, idle-page tracking, Prometheus export), modeled after Robusta KRR's role in cloud. C-73's cloud audit is not a lead magnet for this buyer.
- **Marketplaces:** AWS Marketplace does not apply to on-prem. The Proxmox partner directory and HPC-center procurement lists matter instead.

## 9. Regulatory and funding facts
- **SBIR/STTR (through 2031-09-30):** the founder cannot be SBIR PI while keeping a day job. STTR with a university PI works, for example a systems/OS faculty member doing memory-tiering research. Topics such as DOE ASCR HPC system software or NSF cloud/edge computing are plausible but **[UNVERIFIED]**. Phase I would not fund this before the 18-month mark.
- **Security and privacy:**
  - **Swap encryption:** swap on Kubernetes should be encrypted per the K8s docs (carried over).
  - **PHI in KV tiers:** KV tiers persist prompts, which may be PHI, to host DRAM/NVMe. That brings HIPAA BAAs and encryption at rest for C-75.
  - **SOC 2:** expect SOC 2 Type I requests at ~5 customers. The model assumes $12k.
- **Not relevant:** §5949 and FAR 2023-008 do not apply to the software itself; see §7 for the possible hedge. No export controls apply; this is domestic software.
- **Liability:** the C-74 agent changes production memory behavior. Tech E&O insurance is needed (model: $200/mo), and the MSA must cap liability.

## 10. Unit economics summary (BASE; from the model)

| Line | Price | COGS | GM | CAC | Payback |
|---|---|---|---|---|---|
| C-74 subscription (80 nodes) | $589/mo ($7.36/node) | $79 variable + $289 on-call allocation | 87% variable / 37% loaded | $1,000 cash + 66 founder hours | 27 months |
| C-74 paid pilot | $2,000 | $2,100 | −5% | — | — |
| C-73 audit | $3,000 | $150 + 14 h | 95% cash / 60% labor-loaded | network | — |
| C-75 engagement | $25,000 | $10,000 + 40 h | 60% / 48% | $6k benchmark once | — |
| C-75 retainer | $1,500/mo | 30% | 70% | from engagement | — |

**Funnel.** 149 outbound touches yield one C-74 customer (0.67%) at peak pain. Part-time capacity gives ~0.37 new customers/month on average over months 8–18. **Paying one salary at month 18 needs ~2.5/month.**

## 11. Kill experiment (<$10k, <30 days)

**Hypothesis:** an East Coast operator buying DDR5 servers will pay at least $5/node/month for guarded reclaim that frees at least 10% of RAM with no SLO regression.

**Two parallel arms, 30 days, ~$6k:**
1. **Technical arm (~$3.2k).**
   - **Setup:** rent 3 bare-metal hosts (~$200 each), then replay three workloads: (a) a Proxmox host with 20 mixed VMs, (b) a K8s node running Java, Postgres and Redis, (c) a CI build runner.
   - **Treatment:** zswap (zstd/zsmalloc), Senpai-style PSI reclaim and DAMON_RECLAIM, with guardrails, for 14 days.
   - **Labor:** 15 h of a kernel contractor at $175/h ($2,625).
   - **Measures:** % of installed RAM reclaimed, p99 latency, major faults, OOM kills.
2. **Demand arm (~$2.8k).**
   - **Scanner:** the founder builds a read-only scanner in week 1. The contractor reviews it for 10 h ($1,750).
   - **Outreach:** 60 named targets: 25 Proxmox/KVM MSPs in VA/NC/MD/NJ/NY (rows 1–2 plus the Proxmox partner list), 15 university research-computing centers (rows 4–7), 10 on-prem SaaS/fintech ops teams, 5 refurb resellers and 5 HPC integrators. Sales tooling ~$300; travel and incidentals ~$700.
   - **The ask:** (a) install the 14-day scan; (b) DDR5 vs DDR4 share of the fleet and planned 2027 DIMM/server purchases; (c) a signed paid-pilot LOI.
3. **C-75 gate ($0).** Interview 10 self-hosted LLM teams. If fewer than 2 would pay at least $15k for LMCache/KVBM integration now that Red Hat AI 3.5 offers CPU offload GA, drop C-75 permanently.

**Kill criteria (any one kills C-74):**
- Less than 10% of installed RAM reclaimable at ≤5% p99 regression with zero OOM kills on the 3 hosts.
- Fewer than 5 scan installs from 60 targets.
- Fewer than 2 signed paid-pilot LOIs at ≥$5/node/month from fleets that are majority DDR5 *and* buying in 2027.
- Most responders run DDR4 fleets, where value is ≤$1.3/node/month.

**Pass** means: run 2 paid pilots, re-run the model with measured reclaim and the real DDR5 share, and decide by 2027-Q2. That is before the 2028 turn erodes the value.

## 12. Open gaps
1. **Reclaim on mixed customer fleets** (5% or 20%?) is the biggest technical unknown. The kill experiment measures it. ARR at M36 ranges from $40k to $122k in BASE across 5–20% reclaim.
2. **Real DDR5 vs DDR4 share** in target fleets. No survey found.
3. **ScaleOps:** does it (or will it) manage node swap/zswap in its self-hosted product? Not found. If it does, C-74's K8s segment closes.
4. **Prices not found:** Kove:SDM, Red Hat AI Inference Server, and Percona-style support (no search budget left).
5. **No named regulated self-hosted LLM buyer** found for C-75.
6. **No Azure or GCP memory-instance price-list diff** was run; only the absence of announcements was confirmed.
7. **§5949 grant-funds coverage** for university clusters [UNVERIFIED].
8. The **Kubernetes 2026-10-05 swap density** numbers could not be read in full (kubernetes.io blocked).
9. **Proxmox adoption figures** (1.5M hosts, 16.1% share) come from an unsourced blog. Do not rely on them.
