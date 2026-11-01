# Phase 2, Branch D: Software & "virtual RAM" research notes

**Agent:** D · **As of:** 2026-11-01 · **Cards:** `research/phase2/D.json` (14 cards, D-01 to D-14) · **Sources:** `research/sources/D.jsonl` (65 entries) · **Assumptions:** `research/assumptions/D.md`

> **Method and limits, stated up front.** The shared WebSearch budget was already exhausted when this agent started, so **D ran zero web searches**. WebFetch reached only **github.com, raw.githubusercontent.com, pypi.org and the public AWS Price List API**. memverge.com, kove.net, arxiv.org and openjdk.org all failed DNS, and the Azure retail-price API returned 403. That shaped the evidence base:
> - **Primary data D opened itself:** ~40 GitHub/PyPI pages, and four AWS price-list files (the EC2 us-east-1 CSV, ~300 MB, streamed and filtered; ElastiCache JSON) at two dates. Each is tagged **[VERIFIED]**.
> - **Phase-1 and branch-B facts** are carried over and tagged `(via p1-market)` and so on. They count as **[REPORTED]** at best, because D did not open them.
> - **Company-status claims D could not open** (Kove, Granulate shutdown, Kubecost→IBM, PerfectScale→DoiT, ScaleMP→SAP, Hetzner/OVH 2026 pricing, analyst subscription prices, Amazon affiliate rates) are tagged **[UNVERIFIED-T]**, meaning training knowledge from before mid-2026. Phase 3 should treat them as open questions.
> - About 45 fetches and data pulls in total, under the 40–80 target in fetch count. The AWS diff alone covers 92 EC2 SKUs plus the ElastiCache tables.

---

## 0. The three findings that matter most for this branch

1. **The DRAM shortage never reached AWS list prices. [VERIFIED, primary]** D diffed the AWS Price List API for us-east-1: version `20250930212021` (effective Sep-2025, before the spike) against `20261029175634` (effective Oct-2026). **All 92 compared On-Demand Linux SKUs have identical prices:** c7i, m7i, m8g, r6i, r7g, r7i, r7iz, r8g, x2idn and u7i-6tb.112xlarge. ElastiCache node prices are also unchanged; cache.r7g.large is still Redis OSS $0.219/h and Valkey $0.1752/h. Meanwhile TrendForce conventional DRAM contract prices compounded about 4× from 4Q25 to 4Q26 (via p1-market).
   - **Implication:** customers who rent memory from AWS (the classic buyers of memory-efficiency SaaS) feel *no* shortage. Selling them memory savings has the same value it had in 2024, with no new "why now". The people who feel the pain buy DRAM themselves: on-prem and colo operators, hosting providers, OEMs and system builders, PC upgraders, and embedded device makers. Every card below is aimed with that in mind.
   - **Caveat:** D did not check Savings Plan or RI discount levels, Spot prices, or capacity availability. Hyperscalers may be rationing in ways that never show up in list prices. Azure and GCP were not checked.
   - **Corollary:** cloud RAM costs **$2.56–2.62/GiB-month at the margin** (computed). On-prem DDR5 costs **$0.23–0.54/GB-month** amortized over 5 years even at 2026 prices. Cloud RAM is therefore still **5–11× dearer than owned RAM at the peak of the shortage**, and roughly 12–28× dearer in a glut. That umbrella is the only reason D-08 (RAM rental) has a spread.

2. **The free DRAM-price data layer is saturated, and the East Coast marketplace slot is taken. [VERIFIED + REPORTED]**
   - GitHub search for "dram price" returns **37 repositories**, many updated within days, that scrape DRAMeXchange and TrendForce spot boards into dashboards. Examples are hw-codekim/dram_price (daily DRAMeXchange collection with a Telegram bot) and nwfella/memory-price-index (RamRadar retail plus TrendForce spot, with analysis dated 2026-11-01).
   - Free consumer and server trackers include rampricesusa, RamRadar, Servnet, capitalandcompute.net, siliconanalysts.com and Tom's Hardware's index (via p1-market).
   - **Mobius Materials** (Richmond VA, YC, $3M seed Dec-2025, ML-authentication patent filed) gives away a DRAM Market Report as lead-gen for its authenticated excess-semiconductor marketplace (via p1-market).
   - So a "DRAM price intelligence" product has no free-data moat, the paid contract data belongs to TrendForce and InSpectrum, and a funded regional competitor occupies the marketplace position.

3. **Software "virtual RAM" ideas are either free upstream or abandoned by their pioneers. [VERIFIED]**
   - zswap, zram, KSM, PSI-driven proactive reclaim (Meta Senpai) and CXL tiering (HMSDK's DAMON migration and weighted interleave) are all **in mainline Linux, free**.
   - Kubernetes container swap went **stable in v1.34**, and in-place pod resize went **stable in v1.35**.
   - **MemVerge's public GitHub now centers on LLM routing, LMCache/vLLM forks, a GPU cluster manager (MMAI) and cloud-HPC spot tooling.** That reads as a pivot away from memory virtualization.
   - Linux upstream still scores CXL Dynamic Capacity and multi-host sharing **[0]** (via B).
   - On the KV-cache side, NVIDIA Dynamo's KVBM (Apache-2.0) offloads GPU→CPU→SSD→remote. LMCache's company, **Tensormesh**, has shipped a hosted-inference/control-plane SDK on PyPI since 2026-04-02.

---

## 1. What D looked at, by sub-area, with key numbers

### 1.1 Cloud prices (AWS Price List API, opened)
| Item | Sep-2025 | Oct-2026 | Note |
|---|---|---|---|
| c7i.large (2 vCPU, 4 GiB) | $0.08925/h | $0.08925/h | same |
| r7i.large (2 vCPU, 16 GiB) | $0.1323/h | $0.1323/h | same |
| m8g.large / r8g.large (8 / 16 GiB) | $0.08976 / $0.11782 | same | same |
| x2idn.16xlarge (1,024 GiB) | $6.669/h | $6.669/h | $4,868/month on-demand |
| u7i-6tb.112xlarge (6,144 GiB) | $62.79/h | $62.79/h | $7.46/GiB-month all-in |
| ElastiCache cache.r7g.large Redis OSS / Valkey | $0.219 / $0.1752 | same | Valkey is 20% cheaper |
| ElastiCache Redis OSS Extended Support (cache.r7g.large) | — | $0.175/h (Yr1–2), $0.35/h (Yr3) | new SKUs; treated as additive [ESTIMATE] |

Derived (from `d_calcs.py`, §6): marginal RAM is $2.62/GiB-month (Intel) and $2.56 (Graviton). RAM makes up 28% of the m7i.large list price and 43% of r7i.large.

### 1.2 Memory-efficiency mechanisms (all opened on GitHub)
- **zswap** (zsmalloc pool, selectable compressor, per-cgroup writeback, shrinker). **zram** (lz4/zstd/deflate, writeback, recompression; its docs expect about 2:1). **KSM** (anonymous-page dedup built for KVM density; costs CPU and COW latency; a `general_profit` metric exists).
- **Senpai** (Meta): PSI plus cgroup2 `memory.high` proactive reclaim. In the README example a kernel build's peak drops from 804 MB to 348 MB. This is the userspace half of TMO. TMO's published fleet number (20–32% memory saved, ASPLOS'22) is **[UNVERIFIED-T]** because arxiv and ACM were unreachable.
- **Kubernetes:** KEP-2400 node swap is stable in **v1.34**, with LimitedSwap for Burstable pods only. zram/zswap are out of scope, and the eviction manager is not swap-aware. KEP-1287 in-place resize is stable in **v1.35**. The docs warn that swap degrades badly on throttled cloud disks, which is another reason the reclaim product (D-02) suits on-prem NVMe fleets better than cloud.
- **Right-sizing competition:** Robusta KRR (free, MIT) quotes Sysdig: **18% of memory unused** on average. OpenCost is Apache-2.0 and originally from Kubecost. CAST AI is active (114 repos, updates through 2026-10-31). StormForge's org links to CloudBolt, consistent with an acquisition. The Granulate gProfiler repo shows **no shutdown notice**, so the reported Intel shutdown stays [UNVERIFIED].
- **Caches:** Dragonfly's vendor test claims ~30% less idle memory than Redis and avoids Redis's ~3× snapshot peak. Its **BSL 1.1 forbids third-party managed services until 2030-11-01**. Valkey is active (security releases 2026-10-26), and 9.2.0-rc1 (2026-09-16) adds memory reductions. KeyDB has been part of Snap since 2022; latest release referenced is v6.3.0.
- **JVM:** compact object headers (JEP 450) were integrated into JDK mainline (PR #20677, 2024). The commonly cited 10–20% heap reduction, and JEP 519 making it a product feature in JDK 25, are **[UNVERIFIED-T]** (openjdk.org unreachable). Folded into D-01 as one lever.

### 1.3 KV-cache software (GitHub/PyPI opened)
- **LMCache:** 12.3k stars, 65 PyPI releases from 2025-05-28 to 2026-10-31. Backends include Redis/Valkey, Mooncake, S3, NIXL and GDS. NVIDIA Dynamo integrated it in Sep-2025. Development is "supported in part by Tensormesh".
- **Tensormesh:** a PyPI SDK since 2026-04-02 for "AI inference and control-plane management" with serverless chat completions and billing. In other words, the LMCache creators are monetizing hosted inference.
- **NVIDIA Dynamo:** stable 1.6.1 (nightly 1.7.0.dev20261101), Apache-2.0. KVBM offloads GPU→CPU→SSD→remote. It claims 2× TTFT from KV-aware routing (a Baseten benchmark) and 7× throughput per GPU on GB200 NVL72.
- **Mooncake:** Kimi serves 75% more requests within SLO. It is integrated with vLLM, SGLang, LMCache, Dynamo and TensorRT-LLM (connector merged 2026-10-10).
- **kvpress (NVIDIA):** KV-cache compression, free (0.5.5, 2026-09-17).
- KV footprint: Llama-3.1-70B is **320 KiB/token** at BF16 (config via B), so 1 TB of host DRAM holds about 3.1M tokens.

### 1.4 Tools for the shortage
- **Price data:** 37 GitHub scrapers. nwfella's index reports a DDR4 8Gb spot record of $47.04, DDR5 retail kits 2.6% below their 2026-10-23 record, 512Gb NAND wafer spot down 9.19% in the week to 2026-10-26, and client SSD contract prices up 285–303% YoY.
- **Paid analyst data:** TrendForce/DRAMeXchange, InSpectrum, Omdia, Gartner and Counterpoint subscription prices could **not** be verified; they are assumed to be $5k–50k+ per year [UNVERIFIED-T]. inSpectrum's monthly contract data is cited by the sell side (via p1-market).
- **Mobius Materials:** asked by the task to study its DRAM market reports. It is a **marketplace** (Richmond VA, YC, $3M seed Dec-2025 led by Spero Ventures, founder Margaret Upshur), and its DRAM reports are free or gated **lead-gen** for that marketplace, not a paid data product (via p1-market). Lesson: in this niche, price content is a customer-acquisition cost, not revenue.
- **Distributor APIs:** Nexar (Octopart supply data, Altium 365) offers a GraphQL API plus Excel and Power BI connectors (opened). DigiKey and Mouser APIs were not checked [UNVERIFIED-T].
- **Allocation:** TrendForce says supply is prioritized to strategic OEMs and module makers are limited (via p1-micron).
- **Provenance:** memtest86+'s JEP106 table, "Based on JEDEC JEP106BP – September 2026", lists **CXMT = 0x0A11 and YMTC = 0x091B**. Its SPD decoder reads the module manufacturer from DDR5 bytes 512–513 and DDR4 bytes 320–321. NDAA FY2023 §5949 starts Dec-2027 (via p1-backend). CXMT held a 9.5% revenue share in 2Q26 (via p1-market).
- **Consumer:** Micron ended Crucial (announced 2025-12-03, shipments through Feb-2026, via p1-micron). Retail DDR5 runs $13–18/GB and 32GB kits about $450, while TechRadar reports demand destruction (via p1-market).

---

## 2. Post-mortems and dead ends (why the tempting ideas die)

- **Optane / NVMe-as-RAM (D-06).** Intel wound down Optane with a $559M impairment in Q2-2022 (via A2), and Objective Analysis estimated the losses above $7B (via A2). Without byte-addressable persistent media, "SSD as RAM" hypervisors (IMDT, ScaleMP MemoryONE) only cover workloads that Linux swap plus zswap writeback already cover for free. The 2026 DRAM spike does not change the roughly 1000× latency gap. Branch B carded the hardware revival (B-09). D cards the software revival to kill it as well.
- **Software-defined memory, Kove/MemVerge (D-05).** MemVerge's public repos have moved to AI inference, GPU cluster management and cloud-HPC spot tooling (opened). Kove's 2026 status could not be opened. CXL pooling needs Dynamic Capacity Device support, which upstream scores [0]. Verdict: the category's pioneer pivoted, and a T0/T1 newcomer cannot fund the hardware ecosystem.
- **Granulate-style runtime optimization.** Intel reportedly shut Granulate down. The repo is still public with no notice, so this is [UNVERIFIED]. Either way, a big acquirer could not make standalone runtime optimization stick, which is a warning for D-01.
- **Consumer "download more RAM" (D-07).** Operating systems already compress memory. The 1995 SoftRAM case (FTC action, [UNVERIFIED-T]) is the precedent. Rule-1 status: **UNSUPPORTED**, because no evidence shows a third-party app beats the OS default.
- **Cloud memory-savings SaaS as a "shortage play".** This is refuted by the AWS price diff in §0.1. It is still a business (D-01), but not a shortage business.

---

## 3. Evidence behind each card (short form)

| Card | Core evidence (opened by D unless marked) | Key number | Honest verdict |
|---|---|---|---|
| D-01 Memory FinOps audit | AWS price list diff; KRR README (Sysdig 18%); KEP-1287 stable v1.35; CAST AI org; OpenCost | $2.6/GiB-mo marginal; ~$270/mo fee per $40k-bill customer; ~74 customers for $20k MRR | Fast revenue, crowded, no shortage tailwind; survives glut |
| D-02 Fleet reclaim autopilot | Senpai; zswap/zram/KSM docs; KEP-2400 stable v1.34; K8s swap docs; RDIMM prices (via p1) | 10 TB freed on 200×512GB fleet = $154k–328k deferred DRAM (2026), $61k (glut) | Best "real RAM saved" software play; DIY risk; needs kernel talent |
| D-03 KV-cache tier integration | LMCache, Dynamo, Mooncake READMEs; Tensormesh PyPI; Llama config (via B) | 320 KiB/token; 3.1M tokens per TB; 75% more requests (Mooncake) | Big market, being commoditized by NVIDIA/Tensormesh |
| D-04 Redis→Valkey/Dragonfly | ElastiCache price lists (2 versions); Dragonfly README + BSL; Valkey releases | −20% Valkey vs Redis; −56% vs Redis + extended support (50 nodes) | Real savings, one-shot, AWS-commoditized: a feature of D-01 |
| D-05 SDM pooling (dead) | MemVerge org + MMAI; CXL maturity map (via B); HMSDK (via B) | DCD [0] upstream | Kill: pioneer pivoted, T2+, no glut survival |
| D-06 NVMe-as-RAM (dead) | zswap docs; K8s swap docs; Intel 10-Q Optane (via A2) | ~1000× latency gap | Kill |
| D-07 Virtual-RAM app (dead) | zram docs; retail price/demand destruction (via p1) | 32GB kit ~$450 | Kill: UNSUPPORTED claim, ethics/regulatory risk |
| D-08 TB-RAM rental | AWS x2idn price; used DDR4 (via p1-backend/BuySellRAM); DDR4 +50% Q3-26 (via p1) | 1.5TB box $6.1–13.8k; payback 6–15 mo at $1.2k/mo vs AWS $4.9k/mo | Real spread vs AWS, thin vs Hetzner/OVH; ops-heavy |
| D-09 SMB OEM intelligence | TrendForce allocation (via p1); Nexar org; 37 GitHub scrapers; nwfella index; Mobius report (via p1) | 80 accts × $300 = $24k MRR ceiling-ish | Best founder-fit, weak moat, cyclical |
| D-10 Excess-DRAM marketplace | Mobius seed/report (via p1); nwfella; BuySellRAM (via p1) | 5–10% take | Kill for this founder: Mobius already does it in VA |
| D-11 DIMM provenance scanner | memtest86+ JEP106 table (CXMT 0x0A11) and SPD decoder; §5949 (via p1-backend); CXMT 9.5% share (via p1) | Law-driven from Dec-2027 | Most interesting: T0, survives glut, founder-doable; hinges on FAR rule |
| D-12 Consumer tracker + advisor | Crucial exit (via p1); rampricesusa (via p1); nwfella; GitHub search | ~$3–6 per affiliate sale [UNVERIFIED-T] | Kill as venture; weekend project |
| D-13 Newsletter (bridge) | Mobius/BuySellRAM lead-gen content (via p1); nwfella; TrendForce PR (via p1) | $2–6k MRR realistic | Bridge/funnel only; dies in glut |
| D-14 Embedded RAM diet | zram/zswap docs; LPDDR4X +70–75% QoQ, $21/GB LTAs (via p1); DDR4 +50% (via p1) | $160k–420k/yr BOM saving per 20k-unit line (2026); $50k (glut) | Re-qualification cost kills most cases; dies in glut |

---

## 4. Ranking inside branch D (D's view; Phase 3 rescoring governs)

1. **D-11 DIMM Provenance Scanner.** Demand comes from law, not price, so it is the only card that survives the glut *because* of the glut (CXMT-led oversupply puts more CXMT in the channel). It is T0, software-only, and a direct founder skill match. Kill experiment (<$2k, <30 days): (a) read SPD on 30–50 mixed DDR4/DDR5 modules, including at least 5 known CXMT-die modules bought on eBay or AliExpress. Measure how often the DRAM-manufacturer bytes are populated and truthful. (b) Interview 10 GSA/defense IT integrators on whether §5949 compliance will be evidenced by attestation or by inventory, and check the FAR rule status. If the fields are blank or spoofed in more than 30% of cases, or integrators say "attestation only", kill it.
2. **D-02 Fleet Memory-Reclaim Autopilot.** It saves real DRAM for the buyers who actually feel the shortage (on-prem and colo). The value is large at 2026 prices and halves in a glut. Founder-fit is marginal (needs a Linux-mm contractor). Kill experiment: run zswap plus Senpai-style reclaim on 3 volunteer Proxmox or K8s hosts for 2 weeks and measure GB reclaimed against p99 latency. If a fleet saves less than 10% of its RAM without SLO regressions, kill it.
3. **D-01 Memory FinOps Audit.** It is the fastest path to revenue (3–6 months, consulting-led) and survives the glut, but it is crowded and gets no shortage tailwind. Treat it as the bridge revenue line; D-04 and the JVM lever are features of it, not companies.

Honorable mention: **D-09** has the best founder-fit, but the moat is weak. It is worth building only as the free, lead-gen front end of D-11 or D-02, mirroring Mobius's playbook, not as the paid product.

---

## 5. Ideas considered but NOT carded (one-line reasons)

- **JVM compact-headers / heap audit as a standalone product.** Too narrow, and savings numbers are unverified; folded into D-01 as a lever.
- **BOM EOL and second-source substitution tool for memory parts.** It is SiliconExpert/Z2Data territory, and the feature is folded into D-09.
- **CXL tiering daemon product (TPP/MEMTIS/DAMON policy software).** It is upstream and free (HMSDK v6.9/v6.11), and the hardware side is branch B. Folded into the D-05 kill.
- **KV-cache compression SaaS.** NVIDIA kvpress is free (PyPI 0.5.5), and it would be the same buyer as D-03.
- **Prompt-cache hit-rate optimizer for hosted LLM API users.** It saves API dollars, not RAM, so it is out of scope.
- **DRAM price index or "hedging" product for contracts.** There is no exchange or futures market, TrendForce/InSpectrum own the benchmark, and redistribution is prohibited.
- **Used-RAM buy-back quoting engine for ITADs.** It overlaps branch C (recert/brokerage) and p1-backend S1. BuySellRAM and eBay already do it.
- **Memory-aware autoscaling for CPU/DRAM-resident MoE inference.** That is B-05 (hardware appliance) territory.
- **"Download more RAM" browser and Electron memory reducers.** OS and browser vendors already ship memory savers; no buyer.
- **RAM-heavy CI runner arbitrage (hosted runners with lots of RAM).** It is a sub-case of D-08 with worse competition (GitHub, Buildkite, depot).
- **Analyst-style paid DRAM forecast reports.** No proprietary channel data; TrendForce/Omdia/Gartner own it. Covered by the D-13 kill.

---

## 6. Calculation script (reproducible; run with python3)

The orchestrator owns `models/`, so D kept this in its scratchpad and copies it here verbatim. It exits 0.

```python
"""Branch D back-of-envelope calculations (agent D, 2026-11-01).
Inputs: AWS Price List API (us-east-1, versions 20250930212021 and 20261029175634, opened by agent D),
Phase-1 price facts (cross-referenced), and ESTIMATE assumptions logged in research/assumptions/D.md."""
H = 730  # hours per month

# --- 1. AWS marginal memory price (VERIFIED list prices, unchanged Sep-2025 -> Oct-2026) ---
c7i_large, r7i_large = 0.08925, 0.1323      # 4 GiB vs 16 GiB, 2 vCPU each
m8g_large, r8g_large = 0.08976, 0.11782     # 8 GiB vs 16 GiB, 2 vCPU each
x2idn_16xl, u7i_6tb = 6.669, 62.79          # 1024 GiB, 6144 GiB
marg_intel = (r7i_large - c7i_large) / 12 * H
marg_grav = (r8g_large - m8g_large) / 8 * H
print(f"AWS marginal memory $/GiB-month: Intel {marg_intel:.2f}, Graviton {marg_grav:.2f}")
print(f"AWS all-in $/GiB-month: x2idn.16xlarge {x2idn_16xl*H/1024:.2f}, u7i-6tb {u7i_6tb*H/6144:.2f}")
mem_share_m7i = (8 * (r7i_large - c7i_large) / 12) / 0.1008
mem_share_r7i = (16 * (r7i_large - c7i_large) / 12) / r7i_large
print(f"memory share of list price: m7i.large {mem_share_m7i:.0%}, r7i.large {mem_share_r7i:.0%}")

# --- 2. On-prem DRAM $/GB-month (Phase-1 cross-refs) ---
for label, usd_per_gb in [("RDIMM contract 1Q26 ($900/64GB)", 900/64), ("RDIMM contract ~$1000/64GB", 1000/64),
                          ("RDIMM street Aug-26 ($2064/64GB)", 2064/64)]:
    m = usd_per_gb / 60  # 5-yr straight-line
    print(f"{label}: ${usd_per_gb:.1f}/GB -> ${m:.3f}/GB-month; glut(-60%) ${m*0.4:.3f}; cloud/onprem ratio {marg_intel/m:.1f}x")

# --- 3. Cloud memory right-sizing SaaS unit economics (ESTIMATE) ---
bill = 40_000          # $/month EC2 for an SMB SaaS customer [ESTIMATE]
mem_share = 0.30       # share of bill attributable to RAM [ESTIMATE, cf. 28-43% above]
unused = 0.18          # Sysdig figure quoted in robusta-dev/krr README
realizable = 0.5       # fraction of unused RAM realizable given CPU/RAM coupling of instance sizes [ESTIMATE]
save = bill * mem_share * unused * realizable
fee = 0.25 * save
print(f"Right-sizing: savings ${save:,.0f}/mo; fee@25% ${fee:,.0f}/mo; customers for $20k MRR: {20000/fee:.0f}")

# --- 4. On-prem fleet reclaim (zswap/PSI) value (ESTIMATE) ---
servers, gb_per = 200, 512                 # mid-size on-prem/colo fleet [ESTIMATE]
cold_frac, ratio = 0.20, 2.0               # cold memory offloadable; zram doc expects ~2:1
saved_gb = servers * gb_per * cold_frac * (1 - 1/ratio)
for label, p in [("2026 contract $15/GB", 15.0), ("2026 street $32/GB", 32.0), ("glut $6/GB", 6.0)]:
    print(f"Reclaim: {saved_gb:,.0f} GB deferred purchase = ${saved_gb*p:,.0f} one-time at {label}")

# --- 5. Hosted TB-RAM bare metal from recovered DDR4 (ESTIMATE) ---
ram_gb = 1536; used_ddr4 = [3, 8]; chassis = 1500; colo = 250; rent = 1200
for p in used_ddr4:
    capex = ram_gb * p + chassis
    print(f"TB-RAM box @ ${p}/GB used DDR4: capex ${capex:,.0f}; payback {capex/(rent-colo):.1f} mo at ${rent}/mo rent; AWS x2idn.16xlarge (1 TiB) on-demand ${x2idn_16xl*H:,.0f}/mo")

# --- 6. ElastiCache Redis->Valkey arbitrage (VERIFIED SKUs; additive surcharge = ESTIMATE) ---
redis, valkey, es12, es3 = 0.219, 0.1752, 0.175, 0.35   # cache.r7g.large us-east-1
nodes = 50
base = redis * H * nodes; es = (redis + es12) * H * nodes; vk = valkey * H * nodes
print(f"50x cache.r7g.large: Redis ${base:,.0f}/mo; Redis+ExtSupport(Y1-2) ${es:,.0f}; Valkey ${vk:,.0f}; "
      f"Valkey saves {1-valkey/redis:.0%} vs Redis, {1-vk/es:.0%} vs extended support")

# --- 7. KV cache capacity (Llama-3.1-70B: 80 layers, 8 KV heads, head_dim 128, BF16) ---
kv_bytes = 80 * 8 * 128 * 2 * 2
print(f"KV per token {kv_bytes/1024:.0f} KiB; tokens per TB host DRAM {1e12/kv_bytes/1e6:.1f}M; "
      f"1 TB DRAM cost ${1000*15:,.0f} (2026 contract) vs ${1000*6:,.0f} (glut)")

# --- 8. Data-product / content bridge revenue (ESTIMATE) ---
for subs, price in [(30, 300), (80, 300), (150, 150)]:
    print(f"OEM intel SaaS: {subs} accounts x ${price}/mo = ${subs*price:,.0f} MRR")
for paid, price in [(200, 10), (500, 12)]:
    print(f"Newsletter: {paid} paid x ${price}/mo = ${paid*price:,.0f} MRR")

# --- 9. Embedded RAM diet (ESTIMATE) ---
units = 20_000; gb_saved = 1.0
for label, p in [("LPDDR4 2026 ~$8/GB", 8.0), ("glut ~$2.5/GB", 2.5)]:
    print(f"Embedded diet: {units} units x {gb_saved} GB x {label} = ${units*gb_saved*p:,.0f}/yr BOM saving")
```

Output (2026-11-01):
```
AWS marginal memory $/GiB-month: Intel 2.62, Graviton 2.56
AWS all-in $/GiB-month: x2idn.16xlarge 4.75, u7i-6tb 7.46
memory share of list price: m7i.large 28%, r7i.large 43%
RDIMM contract 1Q26 ($900/64GB): $14.1/GB -> $0.234/GB-month; glut(-60%) $0.094; cloud/onprem ratio 11.2x
RDIMM contract ~$1000/64GB: $15.6/GB -> $0.260/GB-month; glut(-60%) $0.104; cloud/onprem ratio 10.1x
RDIMM street Aug-26 ($2064/64GB): $32.2/GB -> $0.537/GB-month; glut(-60%) $0.215; cloud/onprem ratio 4.9x
Right-sizing: savings $1,080/mo; fee@25% $270/mo; customers for $20k MRR: 74
Reclaim: 10,240 GB deferred purchase = $153,600 one-time at 2026 contract $15/GB
Reclaim: 10,240 GB deferred purchase = $327,680 one-time at 2026 street $32/GB
Reclaim: 10,240 GB deferred purchase = $61,440 one-time at glut $6/GB
TB-RAM box @ $3/GB used DDR4: capex $6,108; payback 6.4 mo at $1200/mo rent; AWS x2idn.16xlarge (1 TiB) on-demand $4,868/mo
TB-RAM box @ $8/GB used DDR4: capex $13,788; payback 14.5 mo at $1200/mo rent; AWS x2idn.16xlarge (1 TiB) on-demand $4,868/mo
50x cache.r7g.large: Redis $7,994/mo; Redis+ExtSupport(Y1-2) $14,381; Valkey $6,395; Valkey saves 20% vs Redis, 56% vs extended support
KV per token 320 KiB; tokens per TB host DRAM 3.1M; 1 TB DRAM cost $15,000 (2026 contract) vs $6,000 (glut)
OEM intel SaaS: 30 accounts x $300/mo = $9,000 MRR
OEM intel SaaS: 80 accounts x $300/mo = $24,000 MRR
OEM intel SaaS: 150 accounts x $150/mo = $22,500 MRR
Newsletter: 200 paid x $10/mo = $2,000 MRR
Newsletter: 500 paid x $12/mo = $6,000 MRR
Embedded diet: 20000 units x 1.0 GB x LPDDR4 2026 ~$8/GB = $160,000/yr BOM saving
Embedded diet: 20000 units x 1.0 GB x glut ~$2.5/GB = $50,000/yr BOM saving
```

Notes on the embedded-diet line: the script uses $8/GB. Using the $21/GB mobile-LTA ceiling (Wccftech via p1) gives $420k/yr for the same 20k-unit line.

---

## 7. Open questions for Phase 3+

1. FAR implementing rule for NDAA §5949: effective date, and whether DIMMs inside servers count. This decides D-11.
2. Are SPD DRAM-manufacturer bytes reliably populated on CXMT-die modules (Kingston, ADATA, Lexar, Netac and others)? This needs a physical sample test.
3. Did hyperscalers tighten Savings Plan discounts, Spot or capacity for memory-optimized instances in 2026, even though list prices held? This would change the D-01 "why now".
4. Hetzner/OVH 2026 dedicated-server price changes (D-08 competitive spread).
5. TrendForce/DRAMeXchange and InSpectrum subscription pricing (D-09 price umbrella).
6. Kove 2026 status, and whether Intel shut down Granulate.
