# DD6 — Private MoE Inference Appliance (DRAM instead of HBM): research notes

**Agent:** `p4-private-moe-appliance` · **As of:** 2026-11-01 · **Anchor:** C-48 (PRIMARY candidate, round 2)
**Model:** `models/private-moe-appliance.py` (exit 0) → `research/phase4/private-moe-appliance_model_output.md`
**Sources:** `research/sources/p4-private-moe-appliance.jsonl` (95 entries) · **Assumptions:** `research/assumptions/p4-private-moe-appliance.md`

> **Evidence grade.** The KTransformers repository (HEAD c987331, 2026-10-28) was opened directly with a sparse git clone, so the benchmark tables quoted from it are **[VERIFIED]**. All 32 WebSearch calls in the quota were used. Every other fact comes from search-result snippets and is tagged **[REPORTED]** (or [REPORTED-P] when the snippet is from a primary filing or release). Both WebFetch attempts (techcrunch.com, pugetsystems.com) failed DNS, so I stopped fetching. CPU list prices are training-era recollections and are tagged **[UNVERIFIED]**.

---

## 0. Verdict (read this first)

**Conditional PRIMARY, at lifestyle scale only. Run the kill experiment (§13) before anything else.** This is the first concept in the study that clears every hard PRIMARY gate:

- first revenue lands inside 18 months (first deposit m7 = 2027-05);
- the recurring line is real (support plus model updates at 61–75% gross margin);
- the work is software, Linux and integration, which matches the founder's skills;
- the 2028 glut does not kill it.

It is **not a $1–2M ARR venture inside 36 months and not a MOONSHOT**:

- **BASE outcome:** $254k recurring ARR at m36. The founder goes full-time at m23 (2028-09). Net is $129k after tax over 36 months. If the same funnel runs on to m60, ARR reaches $559k.
- **What $1M ARR would take:** a 24.5% close rate on qualified conversations, which is 3.1× base.

| Question | Verdict |
|---|---|
| **POSSIBLE?** | **Yes, TRL 8–9.** Open-source hybrid inference runs 1T-parameter MoE models with the experts held in DDR5 [VERIFIED, KTransformers docs]. Two caveats. (1) A 1–2-GPU box serves a *small team*: about 27 named users on a 1T model at ≥10 tok/s each, with **~20 s time-to-first-token** on 2–8k-token RAG prompts. (2) Multi-user scaling is weak: the vendor's own 8×L20 reference runs 37 users at ~1.25 tok/s each. |
| **PROFITABLE?** | **Marginally, as a small integrator.** BASE is $254k recurring ARR at m36 and $1.27M revenue over 36 months. Salary-inclusive breakeven comes at m20, with no external capital in expected value; a ~$25k bridge covers lumpy double orders. Hardware earns 19% GM, the subscription 61–75%. **Two levers destroy it:** a 24/7 on-call SLA (full-time slips to m35), and losing the MSP/RPO channel (ARR −44%). |
| **DOABLE BY THIS FOUNDER?** | **Yes for build and support; unproven for the sale.** The sales motion is new for this founder: regulated-buyer security reviews and the CMMC scoping talk. A 3–6-month sales cycle squeezed into 15 h/week is the gating constraint. |
| **Glut (2028–29)** | **Survives, and shrinks a little.** GLUT ARR at m36 is $213k (−16%) and SEVERE $198k (−22%). Cheaper boxes lift demand, but each box carries fewer gross-profit dollars, and those dollars fund the founder's move to full-time. With demand elasticity 1.0 instead of 0.3, GLUT beats BASE ($322k). The C-48 card's claim that "a glut helps" is **unproven**. What does persist: DDR5 stays 6–9× cheaper per GB than GPU memory (§9). |
| **Biggest risk** | **The buyer has a cloud answer.** CMMC Level 2 does **not** require on-prem AI. M365 Copilot reached GA in GCC High in Dec 2025, and Claude on Bedrock GovCloud covers FedRAMP High, IL4/5 and ITAR. The defense segment shrinks to firms with on-prem or air-gapped CUI/ITAR networks, and those buyers also distrust the best open models because they are PRC-origin. |

---

## 1. How it works (for a smart non-engineer)

A mixture-of-experts (MoE) model such as Kimi-K2.5 has about 1 trillion parameters but uses only ~32B of them for each token. On a GPU server, all 1T parameters must sit in expensive GPU memory (HBM/GDDR). The hybrid trick works like this:

- The rarely-used "expert" weights live in cheap server DDR5 (768 GB).
- The CPU's 12 memory channels stream only the experts each token needs.
- One GPU handles attention, the shared experts and, for long prompts, "layerwise prefill": it streams the weights over PCIe and crunches the prompt.

KTransformers (Tsinghua MadSys + Approaching.AI, SOSP'25 [REPORTED]), SGLang and llama.cpp implement this. The result is a ~$62k box that holds a 1T model at native INT4. Holding it all in GPU memory would take 7–8 × 96 GB GPUs, at $16–18k each today.

---

## 2. Q1 — Performance (measured, then scaled)

### 2.1 Measured data points

| # | Model / hardware | Result | Source |
|---|---|---|---|
| P1 | DeepSeek-R1 Q4 · 1S / 2S Xeon Gold 6454S, 8ch DDR5-4800/socket, 1 GPU | Decode **8.73 (1S) → 11.26 (2S) → 13.69** tok/s. Prefill 54 → 74 → **255–286** tok/s with AMX. Needs 382 GB (1S) vs 1 TB (2S) because weights are duplicated per NUMA node | [KTransformers R1/V3 tutorial, 2025-02](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/DeepseekR1_V3_tutorial.md) [VERIFIED] |
| P2 | MiniMax-M2.1 (230B-A10B, FP8) · **2× EPYC 9355 + 1× RTX 5090, PCIe 5.0**, single concurrency | Prefill/decode **408/32.1** (2k), 1,196/31.4 (8k), 2,540/27.6 (32k) tok/s. With 2× 5090: 414/35.9, 1,847/35.5, 4,007/33.1. **>4.5× prefill and +30% decode vs llama.cpp** on the same hardware | [KT-Kernel MiniMax-M2.1, 2026](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/MiniMax-M2.1-Tutorial.md) [VERIFIED] |
| P3 | Qwen3-Coder-Next (80B-A3B FP8) · 1× RTX 5090 + 2× EPYC 9355 | 362/75.9 (64 tok) · 1,746/75.6 (2k) · 6,233/51.7 (32k) | [KT-Kernel Qwen3-Coder-Next](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/Qwen3-Coder-Next-Tutorial.md) [VERIFIED] |
| P4 | Kimi-K2-Thinking native INT4 · 2× Xeon 8488C, 2 TB DDR5-4800, 1–8× 48 GB GPUs | Single-concurrency **prefill** 53/184/290 tok/s at 2k/8k/30k tokens (1 GPU). 85/294/529 (2 GPUs). 130/435/1,055 (8 GPUs). Needs ≥650 GB RAM | [KT-Kernel Kimi-K2-Thinking-Native](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/Kimi-K2-Thinking-Native.md) [VERIFIED] |
| P5 | Kimi-K2-Thinking · **8× L20 + Xeon 6454S, 37 concurrent requests** | **45.9 tok/s aggregate output. Mean inter-token latency 800 ms (≈1.25 tok/s per user).** TTFT 3.6 s on decode bench. Prefill bench 578 tok/s aggregate, **mean TTFT 41 s** for 1k-token prompts at ~23 concurrent | [KTransformers Kimi-K2-Thinking](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/Kimi-K2-Thinking.md) [VERIFIED] |
| P6 | DeepSeek-class · Xeon 6 + MRDIMM-8800 + 4090D (Intel-supported test) | Aggregate output **17 → 40 tok/s** as concurrency rises; then GPU-bound. +130% throughput at 4-way concurrency | [KT balance_serve](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/balance-serve.md) [VERIFIED] |
| P7 | DeepSeek R1 671B Q4_K_M · Xeon 6 (China Telecom Tianyi Cloud) | ~9.7–10 tok/s per socket instance. 14.7 tok/s for two instances on one socket | [ctyun.cn](https://ctyun.cn/document/10026730/10959476) [REPORTED] |
| P8 | DeepSeek-V4-Flash · 1× RTX 5090, ≥200 GB RAM, AVX2 OK (AMX optional) | Decode **20+ tok/s**. Default `MAX_RUNNING_REQUESTS` = 2 | [KT DeepSeek-V4-Flash](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/DeepSeek-V4-Flash.md) [VERIFIED] |
| P9 | SGLang × KTransformers integration (Xeon 8452Y + A100/4080) | Up to **1.45×** decode throughput; accuracy variation <0.5% | [LMSYS, 2025-10-22](https://www.lmsys.org/blog/2025-10-22-KTransformers) [REPORTED] |
| P10 | Mac Studio M3 Ultra 512GB | Kimi-K2.5 **5–15 tok/s**; 4-Mac cluster ~28 tok/s on Kimi-K2-Thinking; DeepSeek R1 4-bit ~20.3 tok/s; V4-Flash ~35 tok/s | [Tenten](https://developer.tenten.co/how-to-run-kimi-k25-locally-on-mac-studio-m3-ultra-with-512gb); [Pinggy](https://pinggy.io/blog/self_hosting_llms_on_512gb_m5_ultra_mac_studio/) [REPORTED] |
| P11 | 8× RTX PRO 6000 · DeepSeek (SGLang) | 258 tok/s aggregate at 8 concurrent, 32.3 tok/s per request | [Helix.ml](https://helix.ml/blog/running-ds4-on-rtx-pro-6000) [REPORTED] |

### 2.2 What it means for a 1-socket, 1-GPU appliance

These rows are `models/private-moe-appliance.py` §2 [ESTIMATE], built from P1, P2 and P4–P6.

| SKU (model class) | 1-stream decode | Per-user @4 | @8 | Max concurrent at ≥10 tok/s | Named users (15% active at peak) | TTFT 2k / 8k prompt |
|---|---|---|---|---|---|---|
| **L**: Kimi-K2.5 1T INT4, 768 GB, RTX PRO 6000 | **17 tok/s** | 10.0 | 5.1 | **4** | **~27** | **~19 s / ~22 s** |
| **S**: MiniMax-M2.x 230B FP8, 384 GB, RTX 5090 | 25 tok/s | 14.8 | 7.5 | 6 | ~40 | ~5 s / ~7 s |

- **Corrections to the C-48 card.**
  - *AMX dependence is mostly gone.* KTransformers now prefills prompts above a token threshold on the GPU (layerwise), and its AVX2 path supports Kimi-K2.5 RAWINT4. So EPYC 9005 works: the MiniMax benchmark (P2) ran on EPYC. AMX helps only short prompts.
  - *Dual-socket is poor value.* It gains 29% at twice the DRAM, so one socket is the right design.
- **What doesn't change: per-user latency is the product's weak spot.** On the L box, every prompt above the threshold pays a ~20 s weight-streaming floor before the first token. That is fine for "draft this memo from these documents" and poor for chat-speed Q&A. The S box (200–300B class) feels interactive.
- **Concurrency is the hard ceiling.** CPU decode barely batches. With 384 experts and 8 active per token, four concurrent users share almost no expert reads. The measured gain is 2.3–2.35× aggregate (P6), and the 37-user reference (P5) drops to ~1.25 tok/s per user. **A 1-GPU DRAM box is a 10–40-person-team machine, not a department server.**
- **Quality vs smaller models.** The top open-weight models are 1T-class Chinese MoEs:
  - Kimi K3 (2.8T) scores ~57 on the AA index ([andrew.ooo](https://andrew.ooo/answers/best-open-weight-ai-model-august-2026-ranked-self-host/)) [REPORTED].
  - GLM-5.2 is the top-ranked open-weight model on BenchLM ([BenchLM](https://benchlm.ai/stats/open-source-llm)) [REPORTED].
  - Smaller models are close enough to threaten the premise. Gemma 4 31B (dense; one list ranks it #3 open model on Arena text) and gpt-oss-120b both run on **one GPU with no big DRAM** ([Ertas](https://www.ertas.ai/blog/the-2026-open-source-ai-model-landscape); [OpenCurious](https://opencurious.com/open-source-ai-models)) [REPORTED].
  - So the DRAM thesis holds only for buyers who need 500B–1T-class quality (agentic coding, long legal reasoning). The S tier, especially with U.S.-origin models, is close to a commodity GPU workstation.
- **The U.S.-origin model problem, and its partial fix.** Kimi, DeepSeek, GLM, Qwen and MiniMax are all PRC-origin. The No Adversarial AI Act was introduced in Jun-2025 to bar federal agencies from using PRC AI; no passage was found. Commerce and the Navy restrict DeepSeek on government devices ([The Record](https://therecord.media/bipartisan-bill-ban-deepseek-federal); [SCMP](https://www.scmp.com/news/china/science/article/3315838/china-tied-ai-tools-deepseek-face-us-federal-ban-over-threat-national-security)) [REPORTED]. Two U.S.-origin MoEs *are* DRAM-sized: **Inkling 975B-A41B** (Thinking Machines, Apache 2.0, Jul-2026) and **Nemotron 3 Ultra 550B-A55B** (NVIDIA, Jun-2026) ([OpenCurious](https://opencurious.com/open-source-ai-models)) [REPORTED]. By active-parameter scaling they would decode at ~13 and ~10 tok/s on the L box [ESTIMATE]. **KTransformers documents neither** (repo grep, 2026-10-28). Nemotron 3 Ultra has Unsloth GGUFs for llama.cpp ([Unsloth](https://unsloth.ai/docs/models/nemotron-3-ultra)) [REPORTED]. The defense segment therefore depends on engine support the founder does not control.

---

## 3. Q2 — BOM at 2026 prices and in a glut

From `models/private-moe-appliance.py` §1. DRAM is ddr5_reference() per RDIMM user-GB × 1.15 small-buyer premium.

| SKU / scenario | DRAM | GPU | CPU | Platform | **BOM** | **Box price (22% GM)** | DRAM share |
|---|---|---|---|---|---|---|---|
| L, BASE Nov-2026 | $22,770 | $16,000 | $5,500 | $4,500 | **$48,770** | **$62,525** | 47% |
| L, BASE Jan-2029 (−30% turn) | $15,939 | $11,200 | $5,500 | $4,500 | $37,139 | $47,614 | 43% |
| L, GLUT Jan-2028 | $9,108 | $8,800 | $5,500 | $4,500 | $27,908 | $35,779 | 33% |
| L, SEVERE Jan-2028 | $2,277 | $8,000 | $5,500 | $4,500 | $20,277 | $25,997 | 11% |
| S, BASE Nov-2026 | $11,385 | $5,000 | $3,700 | $3,800 | **$23,885** | **$30,622** | 48% |
| S, GLUT Jan-2028 | $4,554 | $2,750 | $3,700 | $3,800 | $14,804 | $18,979 | 31% |

Component evidence:

- **DDR5.** $25.78 per RDIMM user-GB at contract (`models/dram_cost_stack.py`). Street is ~$32/GB (ServNet tracker, Aug-2026, via the C-48 card). Glut $10.31; severe $2.58 per user-GB [ESTIMATE].
- **GPU: a second memory shortage.**
  - **RTX PRO 6000 96GB:** launch MSRP ~$8,565 (2025-03). April 2026 retail was $8,000–9,200. NVIDIA's US store raised it to **$16,000** in Sep-2026. GPUPrix's US low was **$17,987** on 2026-10-22 ([Tech Insider](https://tech-insider.org/nvidia-rtx-pro-6000-blackwell-price-2026/); [GPUPrix](https://gpuprix.com/us/gpus/rtx-pro-6000-blackwell); [Thunder Compute](https://www.thundercompute.com/blog/nvidia-rtx-pro-6000-pricing)) [REPORTED].
  - **RTX 5090:** $1,999 list. Micro Center charges $4,299–5,300 in store; online listings run $8.5–10k. GDDR7 supply is 30–40% below projections ([Tech Insider](https://tech-insider.org/rtx-5090-shortage-price-surge-2026/); [Noobfeed](https://noobfeed.com/hardware/geforce-rtx-5090-price-surge-gddr7)) [REPORTED].
- **CPU.**
  - EPYC 9455 (48C) ~$5.4k and EPYC 9355 (32C) ~$3.7k list [UNVERIFIED, training].
  - Xeon 6747P (48C, **8-channel**) MSRP $6,497; Newegg lists it at $8,731 ([Newegg](https://www.newegg.com/p/N82E16819118613)) [REPORTED].
  - Xeon 6767P launched at $9,595 and is 8-channel ([technical.city](https://technical.city/en/cpu/Xeon-6767P)) [REPORTED]. 12-channel Xeon 6 needs a pricier 6900P part [UNVERIFIED], which is why the design uses **EPYC 9005**.
- **Platform.** $3.8–4.5k [ESTIMATE]. No 2026 barebone price was found; the Supermicro AS-4125GS listing shows no price ([Supermicro eStore](https://store.supermicro.com/us_en/4u-gpu-superserver-amd-epyc-genoa-as-4125gs-tnrt.html)).
- **Takeaway.** At today's prices, memory is **~80% of the L-box BOM**: DRAM 47% plus a GPU priced up by GDDR7 at 33%. In a glut the BOM falls 43% (GLUT) to 58% (SEVERE).

---

## 4. Q3 — Substitutes and prices

| Substitute | Price (dated) | Memory | Fit vs this box | Source |
|---|---|---|---|---|
| **Apple Mac Studio M5 Ultra 512GB** | **$22,299** (shipping late Oct-2026). Apple dropped 512GB from M3 Ultra in Mar-2026 | 512 GB unified, ~1.2 TB/s | Cheapest way to run ≤700B at 4-bit for 1–5 users. **A 1T model at INT4 (~600 GB) does not fit**; it needs ~3-bit. Weak multi-user batching; no BMC/ECC server role | [iThinkDifferent](https://www.ithinkdiff.com/512gb-mac-studio-m5-ultra-price-22299/); [Macworld 2026-10-28](https://macworld.com/article/3271691/the-mac-studio-with-512gb-of-ram-is-shipping-and-it-costs-new-car-money.html); [LLM Configurator](https://llmconfigurator.com/en/blog/mac-studio-m5-ultra-512gb-which-moe-models-fit) [REPORTED] |
| **NVIDIA DGX Spark** | 128GB **$6,950** (from $3,999 at launch; $4,699 after 2026-02-23); new 64GB $4,999 (2026-10-23) | 128 GB LPDDR5X | 100–230B-class at low bit for 1–3 users; cannot hold 1T | [NVIDIA forum](https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713); [Implicator](https://www.implicator.ai/nvidia-adds-64gb-dgx-spark-at-4-999-as-128gb-model-climbs-to-6-950/) [REPORTED] |
| **NVIDIA DGX Station GB300** | **$85–100k**: MSI $85k; partners from $87,411.50; Exxact $94,930 | 748 GB coherent (288 GB HBM3e + 496 GB LPDDR5X) | Holds 1T at INT4 with far more throughput. ~1.5× the L-box price for ~3× the users [ESTIMATE]: **better per user above ~50 users** | [ServeTheHome](https://www.servethehome.com/nvidia-dgx-station-systems-available-at-last-gb300-gb200-workstations-for-your-desktop); [Tom's Hardware](https://www.tomshardware.com/desktops/nvidias-gb300-powered-dgx-station-desktop-tower-listed-for-nearly-usd100-000-online-enterprise-ai-powerhouse-now-available-to-buy-for-mere-mortals-with-lots-of-cash); [Wccftech](https://wccftech.com/nvidia-dgx-station-upgraded-gb300-blackwell-ultra-desktop-superchip/amp/) [REPORTED] |
| **Puget Systems LLM servers** | 4-GPU $43,357; 8-GPU $84,652 (as configured, date unclear) | Up to 752 GB VRAM | GPU-only route. With PRO 6000s now at $16k+, 8 cards alone cost >$128k | [Puget](https://pugetsystems.com/solutions/ai-and-hpc-workstations/ai-large-language-models) [REPORTED] |
| **AVADirect 4U 8-GPU LLM server** | $94,749 configured | 768 GB DDR5 + GPUs | Same class as Puget | [AVADirect](https://www.avadirect.com/4U-Eight-GPU-Large-Language-Model-Server/Configure/19085238) [REPORTED] |
| **HPE Private Cloud AI "Small"** | Reseller-quoted; 36-month FMV lease | RTX PRO 6000 Server Edition | Enterprise rack bundle, not SMB | [HPE](https://buy.hpe.com/us/en/enterprise-solutions/cloud-solutions/storage-cloud/hpe-private-cloud-ai-small-g2-bundle/p/s6m55a) [REPORTED] |
| **Petronella Technology Group** (Raleigh, NC) | Entry private LLM servers "$8–12k". ComplianceArmor on-prem CUI enclave appliance (waitlist) | n/a | **Closest direct competitor**: a CMMC RPO selling on-prem AI as "CMMC/HIPAA/ITAR compliant". Also a possible channel | [Petronella](https://www.petronellatech.com/ai/on-premise-ai/); [ComplianceArmor](https://book.petronellatech.com/compliance/compliancearmor/) [REPORTED] |
| **Lemony AI** (Uptime Industries) | **$499/month for up to 5 users** | small single node | Proves the hardware-plus-subscription model at the SMB low end | [TechCrunch 2025-06-11](https://techcrunch.com/2025/06/11/uptime-industries-wants-to-boost-localized-ai-usage-with-an-ai-in-a-box-called-lemony-ai) [REPORTED] |
| **Iternal** private AI appliance | $697 per seat, perpetual | n/a | One-time-license model | [Iternal](https://iternal.ai/local-llm.md) [REPORTED] |
| **M365 Copilot in GCC High** | GA Dec-2025; price not found (~$30–40/user/month [UNVERIFIED]) | cloud | **The default AI for DIB firms already on GCC High.** Covers FedRAMP High, DFARS 7012, ITAR and CMMC L2 environments. New OpenAI models arrive 4–12 weeks after commercial | [Daymark](https://www.daymarksi.com/blog/microsoft-365-copilot-in-gcc-high-what-dib-subcontractors-need-to-know-about-deploying-ai-without-breaking-cmmc); [Summit 7](https://www.summit7.us/blog/copilot-for-gcc-high-faq) [REPORTED] |
| **Claude on Amazon Bedrock GovCloud** | usage-priced | cloud | FedRAMP High + DoD IL4/5 (Jun-2025). Anthropic: ITAR data can be processed in Claude only via Bedrock (IL5) | [Anthropic](https://anthropic.com/news/claude-in-amazon-bedrock-fedramp-high); [AWS](https://aws.amazon.com/about-aws/whats-new/2025/05/amazon-bedrock-models-fedramp-high-dod-il-4-5-govcloud/); [Claude FAQ](https://support.claude.com/en/articles/13756069) [REPORTED-P] |
| **Legal per-seat cloud AI** | CoCounsel $104–639/user/month; Spellbook $100–300; Harvey from $50k/yr | cloud | WTP benchmark for law firms | [Spellbook](https://spellbook.com/learn/legal-ai-tool-pricing) [REPORTED] |

**Does CMMC Level 2 require on-prem? No.**

- **The rule.** Cloud services that handle CUI must meet FedRAMP Moderate *or equivalent* under DFARS 252.204-7012. They do not need FedRAMP High, and they need not be on-prem. Consumer ChatGPT with CUI is a violation ([Secureframe](https://secureframe.com/blog/cmmc-level-2-ai-governance); [Coalfire Federal](https://coalfirefederal.com/resource/ai-and-cui-what-cmmc-level-2-assessors-look-for/)) [REPORTED].
- **On-prem is not a shortcut.** It "buys you control, not automatic compliance". The GPU server joins the assessment boundary and needs FIPS-validated encryption ([CybertronIT](https://cybertronit.com/blog/can-defense-contractors-use-chatgpt-under-cmmc)) [REPORTED].
- **So GCC High is enough for most.** The on-prem buyer is one of three types: a firm whose CUI/ITAR data lives on on-prem or air-gapped networks; one that wants open weights it can fine-tune on controlled source or CAD data; or one whose per-seat cloud bill exceeds a box.

**Cost per named user per month over 36 months** (`models/private-moe-appliance.py` §4) [ESTIMATE capacities]:

| Option | $/user/month |
|---|---|
| This venture, L box + subscription (27 users) | $116 |
| This venture, S box + subscription (40 users) | $40 |
| Mac Studio M5 Ultra 512GB, self-run (5 users) | $124 |
| DGX Station GB300, self-run (80 users) | $31 |
| Copilot GCC High | ~$35 [UNVERIFIED] |
| Managed private AI | $16 |
| CoCounsel | $104+ |

**The L box is premium-priced per user.** Its pitch is not cost. It is "1T-class quality, INT4, multi-user, on your own network, supported", and it only works for small teams that need exactly that.

---

## 5. Q4 — Demand evidence

- **CMMC timing (strong, but it doesn't force on-prem).**
  - **Phase 2 starts 2026-11-10.** DoD intends to put Level 2 C3PAO requirements into applicable new contracts. Phase 3 follows on 2027-11-10 (32 CFR 170.3(e)) ([A-LIGN](https://a-lign.com/articles/4-cmmc-myths-busted); [Strike Graph](https://www.strikegraph.com/blog/cmmc-phase-2-deadline-november-2026)) [REPORTED].
  - **The backlog is large.** About **80,000** contractors need Level 2 C3PAO certification. **1,717** held one by Jul-2026, served by **~80–83 C3PAOs** ([Infonaligy](https://www.infonaligy.com/blog/cmmc-level-2-assessment-bottleneck); [CyberSheath](https://cybersheath.com/company/news/cybersheath-opens-registration-for-cmmc-con-2026-as-phase-2-deadline-and-assessor-shortage-bear-down-on-defense-contractors/); [Secureframe](https://secureframe.com/blog/federal-cybersecurity-report-2026)) [REPORTED].
  - **What it means here.** The same MSPs selling GCC High Copilot (Daymark, Summit 7, Corsica, CyberSheath) are the DIB's AI advisors.
- **Law.** BigLaw buys its own hardware. Latham & Watkins built its own Nvidia server infrastructure in a Latham-only secure data center, and Kirkland posted on-prem GPU jobs ([Latham/Bloomberg Law](https://www.lw.com/en/practices/admin/upload/SiteAttachments/Latham-Own-AI-Servers-Give-Firm-Best-Options-Leaders-Say.pdf); [Pulse 2.0](https://pulse2.com/latham-watkins-buys-nvidia-gpu-servers-to-build-in-house-ai-systems/amp/)) [REPORTED]. **No mid-size-firm on-prem case was found.** Firms "typically lack server racks", and power and noise are a problem in an office ([Advantech](https://www.advantech.com/es-es/resources/case-study/enhancing-legal-consultation-services-with-genai-and-llms)) [REPORTED]. The L box must therefore be a quiet tower or go in a colo cage.
- **Enterprise surveys (not SMB).**
  - Broadcom Private Cloud Outlook 2026 (1,000+ employees): public cloud as the primary production-inference environment fell from 56% to 41%, and 56% run or plan private-cloud inference ([LLM Configurator](https://llmconfigurator.com/en/enterprise/on-prem-ai-statistics)) [REPORTED].
  - Cloudian (vendor survey): 93% are repatriating AI workloads or evaluating it ([StorageNewsletter 2026-03-11](https://www.storagenewsletter.com/2026/03/11/enterprise-survey-finds-93-are-repatriating-ai-workloads-or-evaluating-a-move-away-from-public-cloud/)) [REPORTED].
  - **No credible SMB on-prem AI hardware purchase survey exists**; LLM Configurator says so itself.
- **Universities.** Many run CUI/ITAR enclaves, and some include GPUs:
  - Virginia Tech's CUI cluster has GPU nodes ([VT ARC](https://docs.arc.vt.edu/resources/compute/05cui.html)).
  - UIUC runs a Regulated Research Enclave ([UIUC](https://help.uillinois.edu/TDClient/42/UIUC/Requests/Service/1330)).
  - Northwestern offers CUI-compliant GPU HPC for LLM work ([Northwestern](https://www.it.northwestern.edu/departments/it-services-support/research/data-storage/available-options-for-regulated-research.html)).
  - The University of Delaware has the UDSecCom enclave ([UD](https://services.udel.edu/TDClient/32/Portal/Requests/Service/516/University-of-Delaware-Secure-Computing-UDSecCom-Enclave)).
  - Utah chose AWS instead ([Amazon, 2026-06](https://press.aboutamazon.com/aws/2026/6/university-of-utah-launches-secure-research-enclave-to-accelerate-competitive-research-with-amazon-web-services)) [REPORTED].
  - Universities have HPC staff, so subscription attach will be low.
- **Willingness to pay for subscriptions.**
  - Lemony: $499/month for 5 users.
  - MSP AI add-on: $25–75/user/month. MSP-led AI integration: $100–300/user/month ([First Focus](https://www.firstfocus.com.au/insights/mid-sized-business-budget-for-ai/)).
  - Managed private AI: $12–20/user/month at 100 users ([ibl.ai](https://ibl.ai/blog/private-ai-pricing.md)).
  - Basic managed IT: $100–150/user/month ([Petronella pricing guide](https://petronellatech.com/blog/managed-it-services-pricing-guide-2026-what-you-should-actually-pay)) [REPORTED].
  - **Model price:** $1,250/month for an L box (~$50/user at 27 users) and $650/month for S. Both sit inside the MSP AI add-on band.
- **Demand verdict.** The pain is real: CUI and privilege data cannot go to consumer AI. **But for most CMMC buyers the cheapest compliant answer is already in their Microsoft tenant.** Demand for an on-prem 1T-class box among 20–500-person regulated firms is **unproven**, and that is the main thing the kill experiment must test.

---

## 6. Q5 — Margin structure

- **Hardware.** Supermicro's FY26 GAAP gross margin was **10.8%**, with quarters swinging from 6.3% to 17.5% ([10-K](https://www.sec.gov/Archives/edgar/data/0001375365/000137536526000022/smci-20260630.htm); [IR](https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Financial-Results/default.aspx)) [REPORTED-P]. A boutique integrator that adds integration and model tuning can price ~22% (the C-48 card). After a 2% warranty reserve and freight, the model realizes **19%**: **$12.1k gross profit per L box and $5.7k per S box** in BASE.
- **Subscription.** L $1,250/month against $317/month cost: 2 h support at $85, $25 tooling, and a 3%/yr parts reserve on a $48.8k box. That is **75% GM** for L and **61%** for S [ESTIMATE].
- **Warranty and RMA.** OEM parts warranties (3 years) are passed through. The integrator carries labor, freight and loaners, reserved at 2% of hardware revenue [ESTIMATE; no source found].
- **Customer economics.** Three-year gross profit per customer is **$40.4k (L) and $18.2k (S)**, against a **CAC of $5.2k**. LTV/CAC is not the problem; lead flow and founder hours are.
- **Recurring share.** The subscription is 35% of a customer's three-year revenue in BASE, rising to 48–55% in GLUT/SEVERE as hardware deflates.

---

## 7. Q6 — Channel

1. **CMMC RPOs and DIB MSPs: the only scalable channel.** Candidates include Petronella (Raleigh NC, an RPO selling on-prem AI), Daymark Solutions (MA), Summit 7, CyberSheath (VA) and Corsica Technologies. All appear as GCC High Copilot advisors in 2026 search results ([Daymark](https://www.daymarksi.com/blog/microsoft-365-copilot-in-gcc-high-what-dib-subcontractors-need-to-know-about-deploying-ai-without-breaking-cmmc); [CyberSheath](https://cybersheath.com/company/news/cybersheath-opens-registration-for-cmmc-con-2026-as-phase-2-deadline-and-assessor-shortage-bear-down-on-defense-contractors/)) [REPORTED].
   - **Pitch:** "the air-gapped and open-weight option next to GCC High". The MSP keeps the customer relationship and takes 10% of hardware plus 15% of subscription [ESTIMATE].
   - **Model impact:** without this channel, BASE ARR at m36 falls from $254k to **$143k** and full-time slips to m30.
2. **Legal-tech VARs and legal IT MSPs** (iManage/NetDocuments partners). No named partner was found [gap].
3. **University procurement.** Universities buy through HPC/research-computing groups and existing reseller contracts. Sell to individual PIs with CUI or ITAR grants, not central IT.
4. **U.S. integration.**
   - **Where:** an East Coast bench with a 48-hour burn-in rack. Parts come only from OCMs and authorized distributors. DFARS 252.246-7008 / 246.870-2 prefer authorized sources for defense buyers, so no gray-market GPUs, even in the shortage.
   - **Which DRAM:** only Samsung, SK hynix or Micron RDIMMs. NDAA §5949 bars CXMT/YMTC/SMIC content from federal buys from 2027-12-23 (01_LANDSCAPE §0).
   - **What it buys:** "Assembled and tested in the USA", plus a component-provenance sheet, is a modest differentiator for federal-adjacent buyers. It is not a price premium (01_LANDSCAPE §7.3).

---

## 8. Q7 — First ten customer candidates

| # | Candidate (name or precise type) | Why them / evidence | Segment risk |
|---|---|---|---|
| 1 | **The founder's own employer** (design/manufacturing firm): a pilot for engineering-document Q&A on an internal network | Warm access; it is the founder's own industry | Conflict of interest; get written approval and keep it arm's-length |
| 2 | **Petronella Technology Group** (Raleigh, NC), as white-label hardware or reseller partner | Already sells "CMMC/HIPAA/ITAR compliant" on-prem AI and runs an appliance waitlist ([Petronella](https://www.petronellatech.com/ai/on-premise-ai/)) | Also a competitor; may build in-house |
| 3 | **Virginia Tech ARC**: PIs on the CUI/ITAR GPU cluster who need a 1T-class model inside the boundary | CUI cluster with GPU nodes ([VT ARC](https://docs.arc.vt.edu/resources/compute/05cui.html)) | Has HPC staff; may self-build |
| 4 | **University of Delaware UDSecCom** enclave users (East Coast) | Secure enclave for regulated research ([UD](https://services.udel.edu/TDClient/32/Portal/Requests/Service/516/University-of-Delaware-Secure-Computing-UDSecCom-Enclave)) | Low subscription attach |
| 5 | **ITAR machine shops and engineering subcontractors (20–200 staff)** in PA, MD, VA or NC whose CUI sits on on-prem file servers rather than GCC High | They have the CMMC Phase 2 deadline; the on-prem enclave is the qualifier | Many will choose GCC High Copilot |
| 6 | **DIB MSPs**: Daymark (MA), CyberSheath (VA), Summit 7, Corsica, as resellers | They advise on GCC High Copilot today and need an air-gapped option | They may see it as cannibalizing Microsoft margin |
| 7 | **Mid-size law firms (50–300 attorneys) on on-prem iManage** in Philadelphia, Baltimore or Richmond | Privilege concerns; per-seat AI costs $104–639/user/month | No mid-size on-prem precedent found; office power and noise |
| 8 | **IP boutiques prosecuting export-controlled patent applications** (ITAR technical data) | Cannot paste ITAR data into commercial cloud AI | Small firms; Bedrock IL5 is an alternative |
| 9 | **Credit unions, RIAs and community banks** (GLBA/SEC Reg S-P) | Data-residency stance | Weak evidence; core-banking vendors bundle AI |
| 10 | **Community hospitals and physician groups** (HIPAA) | Privacy-first buyers | EHR vendors (Epic) ship embedded cloud AI with BAAs; lowest priority |

None has been contacted. The model books **no revenue from named customers**; every order comes from the funnel. This is a deliberate fix for round-1 failure mode #1 (§11).

---

## 9. Q8 — Glut behavior and ceiling

**Glut behavior** (`models/private-moe-appliance.py` §5, §7):

| Metric | BASE | GLUT (−60% from 2028-Q1) | SEVERE ($2.04/GB) |
|---|---|---|---|
| L box price (Jan-2028 quote) | $62,525 | $35,779 | $25,997 |
| HW gross profit per L box | $12,105 | $6,756 | $4,799 |
| Founder full-time | m23 (2028-09) | m28 (2029-02) | m30 (2029-04) |
| Recurring ARR m36 | **$253,693** | **$212,936** | **$197,747** |
| 36-mo net after tax | $129,441 | $102,077 | $91,611 |
| GLUT with demand elasticity 1.0 | — | $321,735 ARR m36 | — |

- **Mechanism.** The glut cuts each box's gross-profit dollars by 44–60%, and hardware gross profit is what pays the founder to go full-time. Subscription revenue is priced per box, so it does not deflate. **The business survives every glut case**, which is unique in this study. Whether a glut *helps* depends on how much cheaper boxes lift demand, and that is not measured.
- **The relative advantage persists.** DDR5 is ~6.5× cheaper per GB than GPU memory today ($25.8/GB vs ~$167/GB for a $16k, 96 GB RTX PRO 6000) and ~9× cheaper in a glut ($10.3/GB vs ~$92/GB) [ESTIMATE].
- **Ceiling.**
  - BASE gives **$254k ARR at m36** and **$559k at m60** (49 boxes under subscription) on this funnel.
  - $1M ARR at m36 needs conversion of **24.5% (×3.06)** or subscription prices **×2.9** (L $3,639/month). Neither is plausible.
  - The real route past $1M is **channel volume**: ≥3 MSP/RPO partners each closing a box a month. That means a sales hire and a field tech, i.e., T1 capital in year 2–3.
  - The long-run threats to the ceiling are product-shaped, not DRAM-shaped:
    - unified-memory desktops (Mac M5/M6 Ultra, DGX Station successors);
    - smaller models catching up (Gemma 4 31B, gpt-oss);
    - the open-source stack getting easier, which commoditizes the integration.

---

## 10. Unit economics and P&L summary (BASE, from the model)

- **Path to first revenue.** Demo and published benchmark by m3; first qualified conversations m3; first order and deposit **m7 (2027-05)**; first delivery m8.
- **Early ARR.** $22.8k at m12, $53.1k at m18, $94.2k at m24 and $253.7k at m36.
- **Cash.**
  - The founder's $40k bottoms at **$13.7k in m7**. No external capital is needed in expected value.
  - **Lumpiness check:** one whole L order needs $17.5k of parts working capital beyond its 50% deposit. Two L orders in one month take cash to −$13.3k. Line up a **~$25k bridge** (vendor terms or a card line) or ask for a 70% deposit.
- **Founder.** Salary-inclusive breakeven at **m20**; full-time from **m23**. The founder is paid $140k of salary over 36 months, and 30% tax ($55k) is provisioned.
- **Sensitivity** (one lever at a time, ±30%):

| Lever | ARR m36 | Full-time |
|---|---|---|
| Price −30% | $112k | never |
| Conversion −30% | $118k | never |
| COGS +30% at fixed quotes | $160k (36-mo net only $20k) | never |
| Churn ±30% | $247–261k (little effect) | — |
| 24/7 on-call ($2.5k/month) | $160k | m35 |
| 30% deposit | cash low $10.0k | — |
| All-L mix | $375k | m20 |

---

## 11. Facing the round-1 red-team failure modes

| Round-1 failure mode (05_REDTEAM.md) | How DD6 handles it |
|---|---|
| Revenue booked from customers the research never found (DD3 LTSAs) | Zero named-customer revenue in BASE; funnel only, and the kill experiment measures conversion |
| Selling to the party that already has the answer (DD1 CleanBOM) | Named head-on: GCC High/Bedrock shops already have compliant AI. The target is narrowed to on-prem/air-gapped CUI, open-weight fine-tuning and per-seat-cost refugees, and the kill test asks the GCC-High question first |
| Free substitutes (DD2 vs Octopart; DD5 vs OpenRAM) | The software is free (KTransformers/SGLang/llama.cpp). Value is hardware plus integration, U.S.-origin model curation, FIPS/SSP documentation and support. Substitute prices are tabled (§4); the Mac Studio and DGX Station beat it on price per user in their bands |
| Counterfactual or "savings share" pricing (DD4) | None. A box plus a fixed-fee subscription |
| 24/7 on-call cost (DD4) | Business-hours, next-business-day SLA in BASE; the 24/7 retainer is shown (full-time m35) |
| Missing tax line (all DDs) | 30% provision with loss carry-forward; the full-time trigger tests post-tax cash |
| Cash cycle understated (DD1) | 50% deposit, parts paid at order, and an explicit whole-box lumpiness check |
| Founder cannot do the core work (DD5) | Builds, Linux, inference engines and RAG apps fit a software founder. The regulated sale is the gap, and the MSP/RPO channel is meant to carry it |
| Ceiling under $1M ARR (DD2, DD5) | Shown: $254k at m36, $559k at m60. Not hidden |
| PRC-origin inputs (new; veteran_2 scorer) | U.S.-origin Inkling/Nemotron 3 Ultra are sized into the L box; engine support is flagged as a dependency |

---

## 12. Regulatory and funding facts

- **CMMC.**
  - Phase 2 starts **2026-11-10**; Phase 3 **2027-11-10** (32 CFR 170.3(e)).
  - Cloud CUI must be FedRAMP Moderate or equivalent (DFARS 252.204-7012).
  - An on-prem box joins the assessment boundary and needs FIPS-validated crypto, so ship a FIPS-mode OS image.
  - Remote vendor support into a CUI enclave can put the vendor in the customer's scope as an External Service Provider. Design support as customer-escorted sessions plus signed offline update bundles. The model budgets $8k plus $400/month for this [ESTIMATE].
- **Procurement rules.** DFARS 252.246-7008 / 246.870-2 favor buying from OCMs and authorized suppliers. NDAA §5949 bars CXMT/YMTC/SMIC content in federal buys from 2027-12-23 (proposed FAR rule only). Both argue for authorized-channel Samsung, SK hynix or Micron RDIMMs and a provenance sheet.
- **PRC-origin AI.** The No Adversarial AI Act was introduced in Jun-2025 and covers federal agencies; no passage was found. Agency device bans on DeepSeek exist [REPORTED]. State-level bans were not checked [gap].
- **FTO.** 01_LANDSCAPE §10.3 flags a Netlist PMIC risk for DDR5 module and appliance makers. Buying finished RDIMMs from licensed majors (Samsung reportedly licensed in 2026) dilutes it.
- **Funding.** SBIR/STTR is reauthorized to **2031-09-30**, but an SBIR PI must be >50% employed by the company. A founder with a day job cannot be PI. In any case, this is an integration business, not an R&D one, so plan **no grant money**. CHIPS money is $0 for this concept. Fund with deposits; any T1 raise comes only after channel traction.

---

## 13. Kill experiment (<$10k, <30 days)

**Budget: ~$6.5k. Founder time: ~55 h over 4 weeks.**

- **Track A, demand (the real kill test; weeks 1–4, ~$2.5k).**
  - **Who:** 20 qualified conversations. Aim for 8 DIB subcontractors (20–200 staff, PA/MD/VA/NC), 5 law-firm IT directors (50–300 attorneys), 4 MSPs/RPOs (Petronella, Daymark, CyberSheath, Corsica or similar) and 3 university CUI-enclave PIs (VT, UD, USC).
  - **What they see:** a one-page offer and price card: S $31k / L $63k plus $650 / $1,250 a month; setup $4k; a 60-day paid pilot for $2,500, credited to purchase.
  - **First question to every DIB prospect:** "Is your CUI in GCC High today, and is Copilot GCC High approved for it?"
  - **Pass if:** ≥3 written LOIs at the card price **or** ≥1 paid pilot or deposit, **and** ≥1 MSP/RPO agrees in writing to co-sell, **and** ≥40% of DIB prospects confirm CUI or ITAR data on on-prem or air-gapped networks where cloud AI is barred.
- **Track B, performance (week 2–3, ~$3k).**
  - **Setup:** rent one week of a 768GB+/1-GPU EPYC 9005 or Xeon 6 host, or borrow an integrator demo unit.
  - **Runs:** Kimi-K2.5 INT4 (KTransformers+SGLang), Nemotron 3 Ultra Q4 (llama.cpp) and MiniMax-M2.x, on a legal/engineering RAG set.
  - **Measurements:** 1-stream decode, per-user decode at 2/4/8 concurrent, and TTFT at 2k/8k.
  - **Pass if:** L ≥12 tok/s single and ≥8 tok/s per user at 4 concurrent, TTFT(8k) ≤25 s, and a U.S.-origin 500B+ model at ≥8 tok/s single.
- **Track C, scoping (week 1, ~$500).** A one-hour paid consult with a C3PAO or RPO. Get, in writing, how an on-prem LLM box is scoped (CUI asset, FIPS, SSP) and whether escorted remote support keeps the vendor out of scope.
- **Remaining ~$500.** Outreach tooling and the LOI/pilot template (reuse a standard MSA).

---

## 14. Kill criteria (any one kills or reshapes)

| # | Trigger | Consequence |
|---|---|---|
| K1 | <2 LOIs **and** 0 paid pilots from 20 qualified conversations | **Kill DD6** |
| K2 | ≥60% of DIB prospects say GCC High Copilot or Bedrock already covers them | **Drop the defense segment.** Re-test law and university only; if those fail K1, kill |
| K3 | 0 of 4 MSPs/RPOs will co-sell | Downgrade to side-line. Without a channel, BASE ARR is $143k at m36 and full-time slips to m30 |
| K4 | L box measures TTFT(8k) >40 s or <6 tok/s per user at 4 concurrent | **Drop the L SKU.** The S box alone competes head-on with the $22k Mac Studio and the $7k DGX Spark: kill unless K1 passes strongly for S |
| K5 | No U.S.-origin 500B+ MoE runs on the hybrid engines at ≥8 tok/s | Defense buyers are unaddressable; law/university only |
| K6 | The C3PAO says vendor remote support puts us in CMMC scope with no escorted-session workaround | Offline-only support; re-price subscription and re-run the model |

---

## 15. Open gaps

1. **No measured Kimi-K2.5 run on 1S EPYC 9005/Xeon 6 with 12-channel DDR5 and one GPU.** Decode, concurrency and TTFT are scaled estimates (Track B closes this).
2. **No KTransformers support documented for Inkling 975B or Nemotron 3 Ultra.** U.S.-origin model performance on the box is unknown.
3. **No SMB on-prem AI purchase-rate data**, and no mid-size law-firm on-prem case. The 8% conversion and 5 conversations/month are judgments.
4. **Share of the ~80,000 CMMC L2 firms whose CUI lives on-prem or air-gapped rather than in GCC High** is unknown, and it sizes the defense segment.
5. **Copilot GCC High price** not found.
6. **CPU prices** (EPYC 9455/9355, Xeon 6900P) are training-era [UNVERIFIED]; platform and barebone prices are estimates.
7. **Warranty/RMA rates and subscription churn** are estimates; no appliance benchmark was found.
8. **Rental availability of 768GB+/GPU bare-metal hosts** for demos and Track B is not confirmed.
9. **GPU supply.** The RTX PRO 6000 shows as out of stock at NVIDIA's store, and authorized-channel lead times are unknown.
10. **No independent M5 Ultra Mac Studio LLM benchmarks yet** (it shipped late Oct-2026); the substitute's speed is projected.
11. **PRC-model policy.** The status of the No Adversarial AI Act and state-level bans was not verified beyond Jun-2025 snippets.
12. **Fetch failures.** WebFetch failed DNS for techcrunch.com and pugetsystems.com; the Lemony $499 and Puget prices are snippet-only.
