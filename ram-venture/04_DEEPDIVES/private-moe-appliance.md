# DD6 — Private MoE Inference Appliance (DRAM instead of HBM) (`private-moe-appliance`)

Author: `p4w-private-moe-appliance` · As of 2026-11-01 · Model: `models/private-moe-appliance.py` (re-run 2026-11-01, exit 0; output in `research/phase4/private-moe-appliance_model_output.md`) · Notes: `research/phase4/private-moe-appliance_notes.md` · Evidence grade: the KTransformers repository was opened with git (HEAD c987331, 2026-10-28), so its benchmarks and licence are **[VERIFIED]**. Every other web fact is search-snippet grade, so the best it can carry is **[REPORTED]**. Model figures are **[ESTIMATE]**. Red-teamed in Phase 5 by `p5r-private-moe-appliance` (2026-11-01): **KILLED** (§14). The model now carries a RED-TEAM REVISIONS (Phase 5) block; `run_with(P_PHASE4)` reproduces the Phase 4 numbers.

---

## 0. Header (revised after red team)

**This is a ROUND-2 deep dive.** Round 1's red team (`05_REDTEAM.md`) killed DD1, DD3 and DD4 and downgraded DD2 and DD5, refuting 0 of 127 objections. That left no PRIMARY-grade venture and no MOONSHOT candidate. A second round was therefore run on the strongest scored survivors not chosen in round 1 (`research/phase3/selection.json` → `round2`). DD6 was round 2's **PRIMARY candidate**; DD7 (C-91 + C-65) was its MOONSHOT candidate.

**Red-team outcome (Phase 5, 2026-11-01): KILLED.** Four reviewers raised 32 objections: 1 FATAL, 19 MAJOR, 12 MINOR. Dispositions: **5 ACCEPTED-KILL, 17 ACCEPTED-DOWNGRADE, 10 ACCEPTED-MITIGATED, 0 REFUTED**. Every objection and response is in §14 and in `research/phase5/responses_private-moe-appliance.json`. The Phase 4 pitch and numbers are kept below, marked as superseded, so the record shows what was attacked.

**Pitch (Phase 4, superseded).** A quiet, U.S.-assembled server runs a 1-trillion-parameter open-weight AI model entirely inside a regulated firm's own network, for a team of 10–40 people. The model is held in ~$23k of ordinary server DDR5 instead of $112–144k of GPU memory (7–8 × 96 GB cards at $16–18k). It sells as a $31k or $63k box plus a $650 or $1,250-a-month support and model-update subscription.

**What survives the red team.** The physics holds for **one user at a time**, not a team. The L box serves 1–2 users at ≥10 tok/s (7–13 named users), not 4 (27). At authorized-channel RDIMM prices it quotes **$78,708**, not $62,525. A two-node Mac Studio cluster at **$44,598** matches its single-stream speed with ~2 s instead of ~22 s to the first token. What is left is the S box: a **$41,091** 200–300B-class server for ~20 named users, which never pays the founder a salary inside 36 months.

**Anchor and folded concepts**

| Role | ID | Concept | Why (scorer quotes, `research/phase3/scores_raw/*.json`) |
|---|---|---|---|
| Anchor | C-48 | On-prem MoE Box (DRAM-instead-of-HBM inference appliance) | Founder: "a 22%-margin workstation reseller with no moat, not a memory venture." VC: "a lifestyle business unless a support subscription attaches." Veteran: "no moat against Puget/Exxact/Dell and a ~20 tok/s single-stream ceiling." |
| Folded | none | — | No adjacent anchor exists (`03_SCORING.md` §7). C-75 (KV-cache tuning) was dropped inside DD4 in round 1 (RT-PHY-DD4-07). C-45 (KV Pool Node, #24, margin 1, moat 1) sells to multi-GPU operators, a different buyer |

**Capital tier: T1 (low), and a bridge is no longer optional (revised).** Demo rent, legal, insurance and the $8k ESP set-up land before the first order, which slips to **m10 (2027-08)**. Expected-value cash falls to **$3,450 at m9**, so BASE draws a **$25,000** tranche (model §5). Phase 4 had a $13,734 low and no draw.

**Scores and ranks** (`scores.csv`; median of three scorers; rank among 40 survivors; Phase 3, not re-scored)

| ID | Tier | Default | Capital-constrained | Moonshot | tech/capital/ttr/usmfg/margin/moat/competition/regulatory/cycle/founder |
|---|---|---|---|---|---|
| C-48 | T1 | 70.0 (15) | 71.7 (15) | 63.3 (19) | 5/4/4/3/2/1/2/4/4/4 |

**Three verdicts (revised after red team)**

- **POSSIBLE? Yes for one user; no for the team the pitch sells.** The software is TRL 8–9: open-source hybrid inference runs 1T-class MoE models with the experts in DDR5 [VERIFIED]. But four concurrent users touch 31 of 384 experts per layer, 3.88× one user's bytes. On one EPYC 9005 socket (576 GB/s platform peak, ~50% sustained) the model (§2.3) gives:
  - **L (Kimi-K2.5 INT4):** 16.3 tok/s single-stream; 9.8 / 7.1 / 5.5 tok/s per user at 2 / 3 / 4 concurrent. That is **1–2 users at ≥10 tok/s, 7–13 named users** (Phase 4: 4 and 27). Time to first token is ~22 s at 8k tokens, ~89 s at 32k and ~178 s at 64k.
  - **U.S.-origin 1T models on L** (Inkling, Nemotron 3 Ultra): 11–14 tok/s single, so one user.
  - **S (MiniMax-M2.x FP8, RTX PRO 5000 48GB):** 23.6 tok/s single, **3 users at ≥10 tok/s, ~20 named users** (Phase 4: 6 and 40).

  All of this is still unmeasured on the exact box.
- **PROFITABLE? No.**
  - BASE recurring ARR is **$63,873** at m36 (Phase 4: $253,693). Only $22,645 of it has survived a renewal decision.
  - The founder **never** goes full-time. The 36-month net is **−$29,411**, and the model draws $25k of external capital.
  - Breakeven comes at m28 with the founder unpaid, and **never** at a $10k salary.
  - GLUT gives $66,969 and SEVERE $68,675.
  - Even if the kill test passes (8% close rate, 6-month cycle, channel at 3 a month), m36 ARR is $86,763 and the 36-month net is +$6,446; the founder is still never full-time.
  - Full-time by m36 needs a **21% close rate** (3.5× the revised 6%, 2.6× Phase 4's own 8%).
- **DOABLE BY THIS FOUNDER? Build: yes. Sell and support on 15 h/week: no.** Phase 4's BASE used the founder's 65 hours exactly. Once delivery and support hours are counted, qualified conversations fall from 7 to ~4.8 a month by m36. A business-hours SLA needs a paid backup technician, and regulated buyers want supplier onboarding a single-member LLC struggles to pass.

**Recommendation (revised after red team): KILLED. It is not PRIMARY, FALLBACK or MOONSHOT.** Cancel the ~$7k kill test: even a pass leaves the founder unpaid for 36 months. Reopen only on the triggers in §14.4.


---

## 1. How it works

**The memory problem.** An AI model's "knowledge" is its weights. Kimi-K2.5 has ~1 trillion of them, which fill ~600 GB at 4-bit precision ([KTransformers Kimi-K2.5 doc](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/Kimi-K2.5.md)) [VERIFIED]. A normal AI server keeps all of that in GPU memory, the most expensive memory there is. That means 7–8 RTX PRO 6000 cards, now $16,000–17,987 each because of a GDDR7 shortage ([Tech Insider, 2026-09](https://tech-insider.org/nvidia-rtx-pro-6000-blackwell-price-2026/); [GPUPrix, 2026-10-22](https://gpuprix.com/us/gpus/rtx-pro-6000-blackwell)) [REPORTED].

**The trick.** Kimi-K2.5 is a *mixture of experts* (MoE). For each word, a router picks 8 of 384 experts per layer, so only ~32B of the 1T weights are read. Most of the model sits idle at any moment, which means it can live in cheaper, slower memory:

```
        768 GB server DDR5 (~$22.8k)                  1 GPU
   +--------------------------------------+     +----------------------+
   | 384 experts per layer (mostly cold)  | --> | attention, shared    |
   | CPU streams the 8 picked per token   | PCIe| experts, KV cache,   |
   | over 12 memory channels              | 5.0 | long-prompt prefill  |
   +--------------------------------------+     +----------------------+
        EPYC 9005, one socket                    RTX PRO 6000 (L) / RTX 5090 (S)
```

- **The CPU reads only the picked experts.** Twelve DDR5-6400 channels give ~614 GB/s in theory. At ~16 GB read per token that is a ceiling of ~38 tok/s [ESTIMATE: arithmetic]. The model assumes **17 tok/s**, about 45% of the ceiling, scaled from a measured 8.73 tok/s on an older 8-channel Xeon ([KTransformers R1/V3 tutorial](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/DeepseekR1_V3_tutorial.md)) [VERIFIED]. **(Revised after red team, RT-VET-DD6-01 / RT-PHY-DD6-01.)** The CPU actually streams ~11.9 GB of *routed* experts per token; attention and the shared expert sit on the GPU. The platform maximum is 12 × DDR5-6000 = 576 GB/s. And concurrent users barely share experts: four users touch 3.88× one user's bytes. The single-stream estimate survives (16–17 tok/s); the multi-user claim does not (§2.3).
- **The GPU does the compute-heavy parts.** For long prompts it streams weights over PCIe and processes the whole prompt at once. That is why the first word takes **~20 s** on the L box.
- **One socket, not two.** KTransformers keeps a weight copy per socket, and a second socket added only 29% (8.73 → 11.26 tok/s, same tutorial). **(Revised after red team, RT-PHY-DD6-02.)** That 1.29× came from a 2025 build that duplicated weights on each socket. Current kt-kernel/SGLang slices experts across NUMA nodes for up to +63% decode on dual-socket ([LMSYS, 2025-10-22](https://www.lmsys.org/blog/2025-10-22-KTransformers)) [REPORTED; baseline unstated]. A 2-socket L box would serve ~3 users (20 named) but quote ~$87k, which is DGX Station money.

**What the customer buys.**

| SKU | Hardware | Models it runs |
|---|---|---|
| **L "Team-1T"** | 768 GB DDR5, 48-core EPYC, RTX PRO 6000 (revised after red team: 832 GB bought, 12 installed + 1 on-site spare RDIMM, RT-PHY-DD6-05; L is out of BASE) | 1T-class at native INT4: Kimi-K2.5, or the U.S.-origin Inkling 975B and Nemotron 3 Ultra 550B |
| **S "Team-S"** | 384 GB DDR5, 32-core EPYC, RTX 5090 (revised after red team: RTX PRO 5000 Blackwell 48GB at $8,216, RT-VET-DD6-03) | 200–300B-class (MiniMax-M2.x, DeepSeek-V4-Flash); interactive, with ~5–7 s to first token (model §2: 5 s at 2k, 7 s at 8k) |

Both come with:

- a 48-hour soak (revised after red team: it is not a burn-in; it adds rasdaemon/EDAC correctable-error logging and DIMM-temperature checks, RT-VET-DD6-06);
- a FIPS-mode Linux image with the engine and model preloaded;
- RAG connectors and single sign-on;
- inserts for the customer's System Security Plan (SSP);
- a subscription covering patching, monitoring, quarterly model refreshes and signed offline updates (revised after red team, RT-VC-DD6-08: refreshes are limited to models that fit the installed memory, since the open-weight frontier has moved to 2.8T-class models such as Kimi K3).

**What it is bad at.** CPU decode barely batches. The vendor's 8-GPU reference serves 37 users at ~1.25 tok/s each, with a 41 s first-token wait at ~23 concurrent ([KTransformers Kimi-K2-Thinking doc](https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/Kimi-K2-Thinking.md)) [VERIFIED]. The L box suits "draft this memo from these 40 documents". It does not suit chat-speed Q&A or coding-agent fleets. **There is an irony here.** The work that most needs 1T-class quality (agentic coding, long legal reasoning) makes many long-context calls, and each one pays the ~20 s floor [ESTIMATE: judgment].

---

## 2. Cost and unit-economics model (revised after red team)

All figures are from `python3 models/private-moe-appliance.py` with the Phase 5 inputs (BASE unless stated; m1 = 2026-11, m36 = 2029-10). Model §0 lists all 25 input changes, old → new, each with its objection id. Model §0 also reproduces the Phase 4 numbers, which are quoted below in parentheses.

DRAM is `models/dram_cost_stack.py` `ddr5_reference()`: $25.78 per RDIMM user-GB at Q4-26 contract, times a small-buyer premium. That premium was **1.15** in Phase 4 and is now **1.65 before the 2028 turn**, unwinding to 1.15 across 2028. It gives **$42.5/GB, or $2,722 per 64 GB RDIMM** (Phase 4: $29.65/GB, $1,897; `dram_price()` × 64 GB at m1). Inputs are logged in `research/assumptions/p4-private-moe-appliance.md` and `p5r-private-moe-appliance.md`.

### 2.1 Bill of materials and box price (model §1; 22% GM target)

| SKU / scenario | DRAM | GPU | CPU | Platform | BOM | Box price | DRAM share |
|---|---|---|---|---|---|---|---|
| L, BASE Nov-2026 (832 GB incl. 1 on-site spare RDIMM) | $35,392 | $16,000 | $5,500 | $4,500 | **$61,392** | **$78,708** ($62,525) | 58% |
| L, GLUT Jan-2028 | $9,867 | $8,800 | $5,500 | $4,500 | $28,667 | $36,752 | 34% |
| L, SEVERE Jan-2028 | $2,467 | $8,000 | $5,500 | $4,500 | $20,467 | $26,240 | 12% |
| S, BASE Nov-2026 (RTX PRO 5000 48GB) | $16,335 | $8,216 | $3,700 | $3,800 | **$32,051** | **$41,091** ($30,622) | 51% |
| S, BASE Jan-2029 | $7,969 | $5,751 | $3,700 | $3,800 | $21,221 | $27,206 | 38% |
| S, GLUT Jan-2028 | $4,554 | $4,519 | $3,700 | $3,800 | $16,573 | $21,247 | 27% |

- **DRAM at authorized-channel prices** (RT-VET-DD6-02). SHI lists a 64 GB DDR5-6400 RDIMM at $7,862.50 MSRP ([SHI](https://www.publicsector.shidirect.com/product/49991475/64GB-DDR5-6400-RDIMM)) [REPORTED, undated list price]. Origin Storage's 64 GB-6400 module is £2,515.63 on special, ~$52/GB ([Avoira](https://shop.avoira.com/origin-storage-64gb-ddr5-6400mhz-rdimm-2rx4-ecc-1-1v-4x77a90966-os.html)) [REPORTED]. The doc's own $32/GB street price, plus the +35% the reviewer cites, gives $43. The $42.5 central is an [ESTIMATE]; the Fusion Worldwide $46–58/GB that VET cites is run as a sensitivity (premium 2.0) but could not be confirmed.
- **The S GPU is now an RTX PRO 5000 Blackwell 48GB** at $8,216 from SHI (MSRP $8,999) ([SHI](https://www.shidirect.com/product/50313204/NVIDIA-RTX-PRO-5000-Blackwell)) [REPORTED]. It replaces a GeForce RTX 5090 bought at Micro Center retail. The swap fixes the GeForce licence problem (RT-VET-DD6-03, RT-HYP-DD6-09) and the 32 GB KV ceiling (RT-PHY-DD6-03).
- **Win condition #1 fails.** "1T-class in one tower under $65k" is now $78,708. A 2-socket L box, the only way to restore user count, would quote ~$87,041. That is DGX Station GB300 money ($87–95k).

### 2.2 Unit economics per box (model §3)

| SKU, BASE | HW gross profit (realized GM) | Subscription $/mo (cost, GM) | 3-yr GP per customer | CAC |
|---|---|---|---|---|
| L | $13,500 (17%) | **$333** (capped at $50 × 6.7 named users; cost $400, **−20%**) | $12,357 | $7,667 |
| S | $6,857 (17%) ($5,724, 19%) | $650 ($302, 54%) | $16,606 ($18,238) | $7,667 ($5,188) |

- **Hardware GM** is now 17% after 3% quote-to-purchase drift, 2% warranty and $400 freight. Partner (15%) and VAR-paper (5% on half of direct deals) fees come off that.
- **CAC** is 1/0.06 × 4 h × $85 + $2,000 = $7,667. **LTV/CAC for S is 2.2** (Phase 4: 3.5).
- **The subscription is capped by what the box can serve** (RT-VET-DD6-01). An L box serving 6.7 named users cannot bill $1,250/month at the $50/user anchor.

### 2.3 Capacity and cost per named user (model §2 and §4; [ESTIMATE] until measured)

Capacity is now computed from memory bandwidth, not from a concurrency curve fitted on an ~845 GB/s Xeon 6 MRDIMM socket:

- **Step time** = fixed time + (distinct experts touched ÷ 8) × routed GB per token ÷ (576 GB/s × 0.50).
- **Bytes read.** Kimi reads 11.9 GB of routed experts per token, and MiniMax 7.0 GB (config arithmetic from RT-PHY-DD6-01).
- **Batching barely helps.** Four users touch 3.88× one user's experts. Sustaining 4 users at 10 tok/s therefore needs ~461 GB/s, 80% of the 576 GB/s platform peak: STREAM-class efficiency, which no engine syncing a GPU every layer reaches.

| Configuration | 1-stream | @2 | @4 | Max users ≥10 tok/s | Named users |
|---|---|---|---|---|---|
| L 1S, DDR5-6000, efficiency 0.50 | 16.3 | 9.8 | 5.5 | 1 | 6.7 (27) |
| L 1S, efficiency 0.55 or a 6400 board | 17.0–17.4 | 10.3–10.6 | 5.9–6.0 | 2 | 13.3 |
| L 2S, 24 × 32 GB, NUMA-aware (≈$87k quote) | 22.2 | 14.8 | 9.0 | 3 | 20 |
| L 1S, Inkling 975B / Nemotron 3 Ultra (U.S.-origin) | 13.7 / 11.0 | 8.0 / 6.2 | 4.4 / 3.4 | 1 | 6.7 |
| S 1S, MiniMax-M2.x FP8, PRO 5000 48GB | 23.6 | 15.2 | 9.0 | 3 | 20 (40) |
| S 1S, INT4 experts (unmeasured upside) | 31.6 | 22.3 | 14.2 | 6 | 40 |

| Option | $/named user/month (36 months) |
|---|---|
| This venture, L + subscription (6.7 / 13.3 users) | **$395 / $222** ($116) |
| This venture, S + subscription (20 users) | **$95** ($40) |
| Two Mac Studio M5 Ultra 512GB over RDMA, 1T at INT4 (~6.7 users), ~2 s TTFT | $185 |
| Mac Studio M5 Ultra 512GB, self-run (5 users) | $124 |
| NVIDIA DGX Station GB300, self-run (80 users) | $31 |
| M365 Copilot in GCC High | ~$35 [UNVERIFIED] |
| CoCounsel (legal cloud) | $104+ |

**The L box loses on every axis it competed on.** It costs more per user than CoCounsel, the Mac cluster and the DGX Station. It is slower to the first token than the Mac cluster by ~10×. Two M3 Ultras ran Kimi K2 Thinking at ~15 tok/s ([Hardware Corner](https://www.hardware-corner.net/mac-rdma-over-thunderbolt-llm/)), and four ran it at 28.3 tok/s ([Jeff Geerling](https://jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5); [Creative Strategies](https://creativestrategies.com/research/running-a-1t-parameter-model-on-a-40k-mac-studio-cluster/)) [REPORTED].

### 2.4 Scenario results (model §5; 36 months from $40k; L not quoted in BASE)

| Metric | BASE | GLUT | SEVERE |
|---|---|---|---|
| First order | m10 (2027-08) (m7) | m10 | m10 |
| Recurring ARR m12 / m18 / m24 | $3,880 / **$15,814** / $32,350 ($22,800 / $53,099 / $94,167) | $3,880 / $17,365 / $36,200 | $3,880 / $17,702 / $37,392 |
| **Recurring ARR m36** | **$63,873** ($253,693) | **$66,969** ($212,936) | **$68,675** ($197,747) |
| … of which renewal-tested (delivered ≤ m24) | $22,645 ($75,334) | $25,340 | $26,174 |
| 36-month revenue | $408,640 ($1,274,019) | $355,501 | $319,431 |
| Subscription share of 36-month revenue [ESTIMATE: Σ monthly sub revenue ÷ 36-mo revenue from the model's simulate() rows; not printed] | 17.0% | 21.1% | 24.2% |
| Breakeven as run, founder unpaid | m28 (2029-02) | m26 | m25 |
| Salary-inclusive breakeven / founder full-time | **never / never** (m20 / m23) | never / never | never / never |
| 36-month net after tax | **−$29,411** ($129,441) | −$24,164 | −$21,971 |
| External capital drawn | $25,000 ($0) | $25,000 | $25,000 |
| Boxes delivered / under subscription at m36 | 9.6 / 8.2 (24.3 / 22.3) | 10.1 / 8.6 | 10.4 / 8.8 |
| Cash m36; of which customers' prepaid money | $53,934; $35,709 | $62,457; $35,944 | $66,535; $35,925 |
| Founder economic profit (net − 2,340 unpaid h × $85) | **−$228,311** ($7,891) | −$223,064 | −$220,871 |

**The glut no longer matters** because the business is too small for it to matter. Cheaper boxes lift units slightly and the shortage premium unwinds, so GLUT and SEVERE are 5–8% *better* than BASE. All three lose money and never pay the founder.

### 2.5 Sensitivity (model §7; BASE with Phase 5 inputs)

| Lever | ARR m36 | 36-mo net | Full-time |
|---|---|---|---|
| BASE (Phase 5) | $63,873 | −$29,411 | never |
| **Kill-test pass: 8% close, 6-month cycle, channel 3/mo** | **$86,763** | **+$6,446** | **never** |
| Same, plus L re-admitted (25% of mix, 2 concurrent) | $88,607 | +$13,215 | never |
| Close rate 8% / 12% | $79,086 / $109,575 | +$441 / +$33,870 | never / never |
| Sales cycle 4 / 9 months | $65,656 / $62,686 | −$20,798 / −$46,954 | never |
| DRAM premium 1.15 / 2.0 | $65,025 / $62,952 | −$23,755 / −$36,496 | never |
| Price +30% (with demand response) / −30% | $80,831 / $45,594 | +$16,470 / −$70,288 | never |
| No MSP/RPO channel | $52,843 | −$42,858 | never |
| Founder 55 h / 45 h a month | $56,202 / $45,291 | −$42,909 / −$57,263 | never |
| No backup retainer / 24/7 retainer | $63,873 | −$14,800 / −$70,990 | never |
| Subscription price ×2 | $98,267 | +$6,202 | never |
| COGS +30% after quoting | $63,873 | −$95,730 | never |

- **No single lever reaches full-time.** Phase 4's m23 full-time switch sat on a knife-edge: adding only the $400/month insurance change moves it to m28 and cuts m36 ARR to $201,730 [ESTIMATE: model decomposition run].
- **Dropping the L box alone, on every other Phase 4 assumption, gives ARR $109,172 and never full-time** [ESTIMATE: model decomposition run, `run_with(P_PHASE4 + mix_L 0)`, BASE; not printed]. The Phase 4 path depended on L boxes' $12k of gross profit each, and that box fails the bandwidth arithmetic.
- **Component spikes are no longer upside** (RT-VC-DD6-01). Orders now fall 0.5% per 1% the box price sits above the Phase 4 card.

### 2.6 What must be true (model §8)

- **Full-time by m36** needs a **21.0%** close rate on qualified conversations, or prices ×1.97 with the demand response. Full-time by m30 needs 24.9%.
- **A non-negative 36-month net** needs an 8.0% close rate.
- **$1M ARR at m36** is not reachable at ≤6× the close rate.
- **The m60 ceiling** on the same funnel is ARR $86,599, still with no full-time switch.
- **The real recurring line is untested.** Two-thirds of m36 ARR is prepaid first-year support that has not faced a renewal.

---

## 3. Target customer and first ten customers

**The buyer** is the IT director, CISO or managing partner of a 20–500-person regulated organization that meets at least one of three tests:

1. **On-prem data.** CUI or ITAR data sits on an on-prem or air-gapped network where cloud AI is barred.
2. **Fine-tuning.** It wants open weights to tune on controlled code, CAD or privileged documents.
3. **Per-seat cost.** Its per-seat cloud AI bill exceeds the box. CoCounsel costs $104–639 per user per month ([Spellbook](https://spellbook.com/learn/legal-ai-tool-pricing)) [REPORTED].

**Not the buyer: a defense contractor whose CUI already sits in GCC High.**

- M365 Copilot reached GA there in Dec-2025 ([Daymark](https://www.daymarksi.com/blog/microsoft-365-copilot-in-gcc-high-what-dib-subcontractors-need-to-know-about-deploying-ai-without-breaking-cmmc)) [REPORTED].
- Claude on Bedrock GovCloud covers FedRAMP High and IL4/5, and ITAR data may be processed in Claude only via Bedrock ([Anthropic](https://anthropic.com/news/claude-in-amazon-bedrock-fedramp-high); [Claude support](https://support.claude.com/en/articles/13756069)) [REPORTED].
- CMMC Level 2 does **not** require on-prem AI ([Secureframe](https://secureframe.com/blog/cmmc-level-2-ai-governance)) [REPORTED].

Nobody knows what share of the ~80,000 Level 2 firms keep CUI on-prem. That share sizes the defense segment.

**No one below has been contacted. The model books zero named-customer revenue; every order comes from the funnel.**

| # | Customer | Why | How to reach |
|---|---|---|---|
| 1 | Founder's employer (design/manufacturing): engineering-document Q&A pilot | Warm; the founder's industry | **Only after a written carve-out (K0)**; then a paid, arm's-length pilot via an engineering manager |
| 2 | Petronella Technology Group (Raleigh, NC), as reseller | A CMMC RPO already selling on-prem AI, with an appliance waitlist ([Petronella](https://www.petronellatech.com/ai/on-premise-ai/); [ComplianceArmor](https://book.petronellatech.com/compliance/compliancearmor/)) | LinkedIn note to the CEO offering a 1T benchmark they lack. **(Revised after red team, RT-VC-DD6-06: treated as a rival, not a channel.)** |
| 3 | Virginia Tech ARC: PIs on the CUI/ITAR GPU cluster | CUI cluster with GPU nodes ([VT ARC](https://docs.arc.vt.edu/resources/compute/05cui.html)) | ARC staff, then PIs on DoD-funded awards. **(Revised after red team, RT-HYP-DD6-01: a benchmark partner, not a buyer. Purchases on federal awards must be competed under 2 CFR 200.320.)** |
| 4 | University of Delaware UDSecCom enclave users | Regulated-research enclave ([UD](https://services.udel.edu/TDClient/32/Portal/Requests/Service/516/University-of-Delaware-Secure-Computing-UDSecCom-Enclave)) | UD research-computing team; expect low subscription attach |
| 5 | ITAR machine shops and engineering subcontractors (20–200 staff) in PA/MD/VA/NC with on-prem CUI | (revised after red team) CMMC Phase 2, planned for 2026-11-10 ([Strike Graph](https://www.strikegraph.com/blog/cmmc-phase-2-deadline-november-2026)), was **suspended on 2026-07-13** pending a 60-day review; no resumption was found by 2026-11-01 ([Jenner](https://www.jenner.com/en/news-insights/client-alerts/department-of-war-suspends-cmmc-phase-iibut-compliance-obligations-remain-as-does-enforcement-risk); [McGuireWoods](https://blogs.mcguirewoods.com/2026/07/14/dow-suspends-cmmc-phase-ii-requirements-launches-60-day-review/)). DFARS CUI duties remain; the urgency does not | APEX Accelerator and NDIA chapter events [UNVERIFIED: names]; MSP referrals |
| 6 | DIB MSPs as resellers: Daymark (MA), CyberSheath (VA), Summit 7, Corsica | They advise on GCC High Copilot ([Summit 7](https://www.summit7.us/blog/copilot-for-gcc-high-faq)); none was seen offering an air-gapped option [ESTIMATE: judgment from search, not confirmed] | CMMC Con 2026, run by CyberSheath ([CyberSheath](https://cybersheath.com/company/news/cybersheath-opens-registration-for-cmmc-con-2026-as-phase-2-deadline-and-assessor-shortage-bear-down-on-defense-contractors/)) |
| 7 | Law firms of 50–300 attorneys on on-prem iManage (Philadelphia, Baltimore, Richmond) | Privilege; seat costs. BigLaw buys its own GPUs ([Latham/Bloomberg Law](https://www.lw.com/en/practices/admin/upload/SiteAttachments/Latham-Own-AI-Servers-Give-Firm-Best-Options-Leaders-Say.pdf)) | Legal-IT MSPs. No mid-size precedent was found; office power and noise bite ([Advantech](https://www.advantech.com/es-es/resources/case-study/enhancing-legal-consultation-services-with-genai-and-llms)). **(Revised after red team, RT-PHY-DD6-04:** the box is a sustained ~1.1–1.3 kW load, so it needs a server closet with a dedicated 20 A circuit or a colo cage. There is no quiet-tower option. For 1T-class work, a firm that accepts macOS is better served by a 2-node Mac cluster, RT-HYP-DD6-03.**)** |
| 8 | IP boutiques prosecuting export-controlled patents | Cannot paste ITAR data into commercial AI | USPTO practitioner directory, then email. Bedrock IL5 is their alternative |
| 9 | Credit unions, RIAs, community banks | Data residency | Weak; core-banking vendors bundle AI |
| 10 | Community hospitals and physician groups | Privacy | Lowest priority; EHR vendors ship AI with BAAs |

---

## 4. Go-to-market

**Positioning.** "The air-gapped, open-weight option *next to* GCC High." The MSP keeps the Microsoft relationship and adds a box for the enclave cloud AI cannot touch.

**Channels.**

1. **Founder-led direct sales (m3–m12),** at 5 qualified conversations a month.
2. **MSP/RPO co-sell from m13.** Partners take 10% of hardware and 15% of subscription and add 3 conversations a month. This channel is load-bearing: without it, ARR at m36 drops 44% and full-time slips to m30 (Phase 4 inputs [ESTIMATE: `run_with(P_PHASE4)` with no channel, $142,861]). **(Revised after red team, RT-VC-DD6-06:** partners take 15% of hardware and 20% of subscription and add 2 conversations a month. Without the channel, Phase 5 m36 ARR falls 17%, from $63,873 to $52,843, and the 36-month net to −$42,858; model §7.**)**
3. **Lead magnets.** A reproducible public benchmark on the actual box by m3, and a one-page "how an on-prem LLM box is scoped under CMMC" memo built from Track C (§10).

**Pricing** (model inputs):

- **Boxes:** S $30,622 and L $62,525, cost-plus, with quotes valid for 14 days. **(Revised after red team: S $41,091; L not quoted. Quotes are valid 30 days with a price-adjustment clause applied at PO, indexed to a published DRAM contract index and the distributor GPU price; the integrator absorbs ~3% drift. RT-HYP-DD6-07, RT-VET-DD6-02.)**
- **Setup:** $4,000.
- **Subscription:** $650 or $1,250 a month, billed annually in advance and mandatory in year 1. The anchors are Lemony at $499 a month for 5 users ([TechCrunch, 2025-06-11](https://techcrunch.com/2025/06/11/uptime-industries-wants-to-boost-localized-ai-usage-with-an-ai-in-a-box-called-lemony-ai)) and MSP AI add-ons at $25–75 per user per month ([First Focus](https://www.firstfocus.com.au/insights/mid-sized-business-budget-for-ai/)) [REPORTED].
- **Terms:** a 50% deposit, and a $2,500 60-day pilot credited to purchase. **(Revised after red team, RT-HYP-DD6-06:** next-business-day service on DIMMs, NVMe and PSUs from a depot spare pool; for a GPU failure, a 48 GB loaner installed within 2 business days while PNY handles the RMA. This is not equivalent to Dell ProSupport or HPE Foundation Care, and is not sold as such. A U.S.-person backup technician is on a $500/month business-hours retainer.**)**
- **Leasing** through a third-party lessor, like HPE's 36-month lease ([HPE](https://buy.hpe.com/us/en/enterprise-solutions/cloud-solutions/storage-cloud/hpe-private-cloud-ai-small-g2-bundle/p/s6m55a)). Not modelled.

**Sales motion.** Discovery ("Is your CUI in GCC High, and is Copilot approved for it?") → paid pilot on a rented host → security review (3–6 months) → PO and deposit → parts → 48-hour burn-in → on-site install → subscription.

**Supply rules.**

- Buy only from OCMs and authorized distributors, per DFARS 252.246-7008 ([DFARS](https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/252.246-7008.dita)). No gray-market GPUs. **(Revised after red team: no GeForce parts in any SKU; the S box uses an RTX PRO 5000 Blackwell 48GB, RT-VET-DD6-03, RT-HYP-DD6-09.)**
- Use only Samsung, SK hynix or Micron RDIMMs, with a provenance sheet, ahead of NDAA §5949 on 2027-12-23 ([Federal Register, 2026-02-17](https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services)). **(Revised after red team, RT-VET-DD6-05:** the sheet records the DRAM, RCD, PMIC and SPD-hub manufacturer IDs read from each module's SPD [UNVERIFIED-training: field layout], plus lot and date codes. Modules with a Montage RCD are rejected where it is visible. The sheet states that the fab site is not disclosed at small-buyer volume and makes no "non-PRC" claim. Each module also logs correctable errors via rasdaemon/EDAC against a replace threshold.**)**
- "Assembled in USA" is a modest differentiator, not a premium (`01_LANDSCAPE.md` §7.3).

**First 90 days**

| Days | Dates | Actions | Output |
|---|---|---|---|
| 1–29 | 2026-11-02 → 11-30 | K0 carve-out; kill test (§10) | Pass/fail on K0–K7 |
| 30–60 | 12-01 → 12-31 | Rented-host demo; benchmark harness; MSA and subscription terms ($3k legal); bench ($2.5k) | ≥1 paid pilot scheduled |
| 61–91 | 2027-01-01 → 01-31 | Publish benchmark; security packet (SSP inserts, FIPS image, SBOM, provenance sheet); first co-sell agreement | ≥10 qualified conversations logged |

---

## 5. Competitors and why you would win

All rows are [REPORTED] unless marked otherwise.

| Competitor | Offer and price | Threat |
|---|---|---|
| Mac Studio M5 Ultra 512GB | **$22,299**, shipping late Oct-2026 ([Macworld, 2026-10-28](https://macworld.com/article/3271691/the-mac-studio-with-512gb-of-ram-is-shipping-and-it-costs-new-car-money.html)) | Best for ≤700B models and 1–5 users. A 1T model at INT4 (~600 GB) does not fit in 512 GB [ESTIMATE: arithmetic]; 2.8T-class models do not serve well ([LLM Configurator](https://llmconfigurator.com/en/blog/mac-studio-m5-ultra-512gb-which-moe-models-fit)) |
| DGX Spark | $6,950 (128 GB); $4,999 (64 GB) ([Implicator](https://www.implicator.ai/nvidia-adds-64gb-dgx-spark-at-4-999-as-128gb-model-climbs-to-6-950/)) | Undercuts the S box for 1–3 users |
| DGX Station GB300 | $87–95k ([ServeTheHome](https://www.servethehome.com/nvidia-dgx-station-systems-available-at-last-gb300-gb200-workstations-for-your-desktop); [Tom's Hardware](https://www.tomshardware.com/desktops/nvidias-gb300-powered-dgx-station-desktop-tower-listed-for-nearly-usd100-000-online-enterprise-ai-powerhouse-now-available-to-buy-for-mere-mortals-with-lots-of-cash)); 748 GB coherent memory ([Wccftech](https://wccftech.com/nvidia-dgx-station-upgraded-gb300-blackwell-ultra-desktop-superchip/amp/)) | ~1.5× the L price for ~3× the users [ESTIMATE]; wins above ~50 users |
| Puget, AVADirect, HPE GPU servers | $43k (4-GPU) and $85k (8-GPU) ([Puget](https://pugetsystems.com/solutions/ai-and-hpc-workstations/ai-large-language-models)); $94,749 ([AVADirect](https://www.avadirect.com/4U-Eight-GPU-Large-Language-Model-Server/Configure/19085238)) | Any of them could add a 768 GB, one-GPU SKU within weeks |
| Petronella | Private LLM servers from "$8–12k" ([Petronella](https://book.petronellatech.com/blog/private-ai-deployment-guide-enterprise/)) | **Closest direct rival**; already owns the CMMC buyer |
| Lemony; Iternal | $499/month for 5 users; $697 per seat, perpetual ([Iternal](https://iternal.ai/local-llm.md)) | Prove the appliance model at the low end |
| Copilot GCC High; Claude on Bedrock GovCloud | ~$35/user/month [UNVERIFIED]; usage-priced | **The default answer for most defense contractors** |
| Small models on one GPU | Gemma 4 31B, which fits one 24 GB card at 4-bit ([Yotta Labs, 2026-10-05](https://www.yottalabs.ai/post/gemma-4-hardware-requirements-gpu-memory-2026)), and gpt-oss-120b ([Ertas](https://www.ertas.ai/blog/the-2026-open-source-ai-model-landscape)) | Erode the "you need 1T quality" premise |
| DIY on KTransformers | Free | Veteran scorer: "copyable by any integrator in a week" |
| (added after red team) Two Mac Studio M5 Ultra 512GB over RDMA-over-Thunderbolt-5 (macOS 26.2, exo) | ~$44,598; 2× M3 Ultra ran Kimi K2 Thinking at ~15 tok/s, 4× at 28.3 tok/s with ~2 s TTFT and <500 W ([Hardware Corner](https://www.hardware-corner.net/mac-rdma-over-thunderbolt-llm/); [Jeff Geerling](https://jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5); [Creative Strategies](https://creativestrategies.com/research/running-a-1t-parameter-model-on-a-40k-mac-studio-cluster/)) | **Beats the L box** on price (57% of $78.7k), TTFT (~10×) and power for any buyer who accepts macOS; no ECC/BMC, awkward in a CMMC boundary (RT-HYP-DD6-03, RT-VC-DD6-09) |
| (added after red team) Gemini on Google Distributed Cloud air-gapped | GA Aug-2025; Gemini 3.5 Flash GA there 2026-10-30, per RT-HYP-DD6-10 [REPORTED via red team; not verified by me] | Closed frontier model inside the customer's network; rack-scale footprint, so it hits only the top of the range (50–300-attorney firms, university enclaves) |

**Where you would win (honest conditions):**

1. **(Failed after red team: the L box quotes $78,708 and serves 1–2 users; §2.3.)** **Packaged 1T-class quality in one tower under $65k.** Today that otherwise takes 7–8 GPUs or a $90k DGX Station, and "few package DRAM-resident MoE specifically" (veteran scorer).
2. **CMMC-literate packaging.** A FIPS image, SSP inserts, escorted support, signed offline updates and a provenance sheet.
3. **(Failed for L after red team: Inkling and Nemotron 3 Ultra are one-user models on the L box, §2.3; defense moves to S with ≤400B U.S.-origin models.)** **U.S.-origin model curation.** The No Adversarial AI Act was introduced in Jun-2025, and agencies restrict DeepSeek ([The Record](https://therecord.media/bipartisan-bill-ban-deepseek-federal); [SCMP](https://www.scmp.com/news/china/science/article/3315838/china-tied-ai-tools-deepseek-face-us-federal-ban-over-threat-national-security)) [REPORTED]. Inkling 975B and Nemotron 3 Ultra are DRAM-sized ([OpenCurious](https://opencurious.com/open-source-ai-models)). **But KTransformers documents neither** (repo grep, 2026-10-28). Nemotron has llama.cpp GGUFs ([Unsloth](https://unsloth.ai/docs/models/nemotron-3-ultra)).
4. **Local service.** East Coast installs and a named human.

**Where you lose:**

- **On price per user** against Copilot, DGX Station and Mac Studio.
- **On moat** (score 1). Bigger integrators can copy the SKU.
- **If the market moves:** 30B-class models close the quality gap, or unified-memory desktops reach 768 GB.

---

## 6. IP position

**What it owns.** Nothing patentable:

- build recipes and tuning profiles;
- the benchmark harness;
- the FIPS image and SSP templates;
- the support tooling;
- a product trademark.

All of it is copyable.

**What it builds on:**

| Component | Licence | Status |
|---|---|---|
| KTransformers | **Apache 2.0**, with a contributor patent grant ([repo](https://github.com/kvcache-ai/ktransformers)) | [VERIFIED: LICENSE at HEAD c987331] |
| SGLang; llama.cpp | Apache 2.0; MIT | [UNVERIFIED-training] |
| Inkling 975B weights | Apache 2.0 ([OpenCurious](https://opencurious.com/open-source-ai-models)) | [REPORTED] |
| Kimi K2.x; DeepSeek; Nemotron 3 | Modified MIT with an attribution threshold; MIT; NVIDIA Open Model License | [UNVERIFIED-training]. Check preload and redistribution rights before shipping |

**Freedom-to-operate risks, ranked:**

1. **The founder's employment agreement.** The employer is customer candidate #1 and in an adjacent industry. A written carve-out comes first (K0), the same gate round 1 imposed on DD2 (RT-VC-DD2-05).
2. **Netlist DDR5 patents** (`01_LANDSCAPE.md` §10.3). Diluted by buying finished RDIMMs from licensed majors; Samsung reportedly signed a Netlist licence in 2026 ([Panabee, 2026-08](https://www.panabee.com/news/netlist-earnings-q2-2026-report)) [REPORTED].
3. **Hybrid CPU/GPU offload patents** held by the KTransformers authors ([Tsinghua MadSys, SOSP'25](https://madsys.cs.tsinghua.edu.cn/publication/ktransformers-unleashing-the-full-potential-of-cpu/gpu-hybrid-inference-for-moe-models/)) or others. Not searched [UNVERIFIED]. Apache 2.0's patent grant covers the contributed code.

---

## 7. Regulatory and funding path

**CMMC drives demand but does not mandate this product.**

- **Dates (revised after red team, RT-HYP-DD6-08).** Phase 2 was scheduled for 2026-11-10 and Phase 3 for 2027-11-10 ([A-LIGN](https://a-lign.com/articles/4-cmmc-myths-busted)). On 2026-07-13 the Department of War **suspended Phase 2** and paused later milestones pending a 60-day review due mid-September ([Jenner](https://www.jenner.com/en/news-insights/client-alerts/department-of-war-suspends-cmmc-phase-iibut-compliance-obligations-remain-as-does-enforcement-risk); [McGuireWoods, 2026-07-14](https://blogs.mcguirewoods.com/2026/07/14/dow-suspends-cmmc-phase-ii-requirements-launches-60-day-review/); [HSToday](https://www.hstoday.us/?p=223184)) [REPORTED]. No resumption was found on 2026-11-01. NIST 800-171/DFARS 7012 duties still apply ([Redspin](https://redspin.com/?p=79394)).
- **Backlog.** ~80,000 contractors need Level 2. 1,717 were certified by Jul-2026 ([CyberSheath](https://cybersheath.com/company/news/cybersheath-opens-registration-for-cmmc-con-2026-as-phase-2-deadline-and-assessor-shortage-bear-down-on-defense-contractors/)), served by ~80 C3PAOs ([Infonaligy](https://www.infonaligy.com/blog/cmmc-level-2-assessment-bottleneck)) [REPORTED].
- **Cloud is allowed.** Cloud AI handling CUI needs FedRAMP Moderate or equivalent, not on-prem ([Coalfire Federal](https://coalfirefederal.com/resource/ai-and-cui-what-cmmc-level-2-assessors-look-for/)) [REPORTED].
- **On-prem joins the boundary.** The box enters the assessment boundary and needs FIPS-validated crypto ([CybertronIT](https://cybertronit.com/blog/can-defense-contractors-use-chatgpt-under-cmmc)) [REPORTED].
- **Vendor scope.** Remote support can make the vendor an External Service Provider in the customer's scope. The design answer is escorted sessions plus signed offline bundles, budgeted at $8,000 (m9) plus $400 a month (model). Track C tests it.

**ITAR.** Anyone touching a customer's ITAR data during support must be a U.S. person [UNVERIFIED-training], as AWS GovCloud requires for ITAR inference ([AWS](https://aws.amazon.com/blogs/machine-learning/supercharge-regulated-workloads-with-claude-code-and-amazon-bedrock/)) [REPORTED]. Sell domestically only.

**Procurement.** DFARS 252.246-7008 and NDAA §5949 both favour authorized Samsung, SK hynix or Micron memory with a provenance sheet. The §5949 FAR rule was still only proposed on 2026-11-01 (`01_LANDSCAPE.md` §7.3). State-level bans on PRC-origin AI were not checked [gap].

**Funding.**

- **No grants.** SBIR/STTR runs to 2031-09-30 ([IEDC, 2026-04-15](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)), but an SBIR PI must be more than half employed by the company, which excludes a founder with a day job ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)). This is integration, not R&D, anyway. CHIPS money: $0.
- **Deposits fund parts.** The ~$25k bridge comes from distributor terms or a card line.
- **A ~$0.5M raise** for a seller and a field tech [ESTIMATE: model loaded costs × 2 years], only after ≥3 MSP/RPO partners each close about a box a month.

---

## 8. 18-month roadmap with measurable gates

**(Superseded after red team: the concept is KILLED, and these gates were set on the Phase 4 path. If reopened, use §11's revised criteria.)** m1 = 2026-11. Gates are ~75% of the model's BASE path, using whole-box floors.

| Period | Build | Sell | Gate (date: test) |
|---|---|---|---|
| m1 (Nov 2026) | Nothing until K0; then the Track B benchmark | Kill test (§10) | **2026-11-30:** K0–K7 pass, else §11 |
| m2–m3 (Dec–Jan) | Rented-host demo; FIPS image; harness | 5 qualified conversations a month | **2027-01-31:** benchmark published and meeting Track B thresholds; ≥10 conversations; ≥1 paid pilot |
| m4–m6 (Feb–Apr 2027) | Security packet; RAG and SSO connectors | Pilots into security review | **2027-04-30:** ≥2 prospects in formal review; ≥1 signed co-sell agreement |
| m7–m9 (May–Jul) | First build; ESP setup (m9) | First deposit (model m7) and delivery (m8) | **2027-07-31:** ≥1 deposit (model 1.2 orders); first box passes its acceptance benchmark |
| m10–m12 (Aug–Oct) | Monitoring and offline-update pipeline | 0.4 orders a month | **2027-10-31:** ≥2 orders (model 2.4); ARR ≥$17k (model $22.8k) |
| m13–m15 (Nov 2027–Jan 2028) | U.S.-origin model refresh; demo box bought (model m14) | Channel starts; CMMC Phase 3; §5949 | **2028-01-31:** ≥3 channel-sourced conversations; ARR ≥$27k (model $36.5k) |
| m16–m18 (Feb–Apr 2028) | Next-generation SKU priced for the 2028 turn | Founder still part-time | **2028-04-30:** ≥4 boxes delivered (model 4.7); ARR ≥$40k (model $53.1k). Full-time only on the model trigger: trailing 3-month GP − opex ≥ $10k and cash ≥ $30k (BASE m23) |

---

## 9. Team required

| Role | When | Cost | Where to find |
|---|---|---|---|
| **Founder** (product, builds, sales) | ~15 h/week; never full-time in Phase 5 BASE (Phase 4: m23) | Unpaid ($0 salary paid in 36 months, model §5); $10k/month loaded only after the full-time trigger (model) | — |
| Employment attorney | m0 | ~$500 [ESTIMATE] | Reviews the agreement before the K0 request |
| Commercial attorney | m1 | $3,000 (model): MSA, warranty, ITAR terms | East Coast tech-transactions boutique |
| CMMC RPO or C3PAO advisor | m1, then as needed | $500 consult; ESP review inside the $8k at m9 | The Cyber AB marketplace [UNVERIFIED]; Petronella, CyberSheath, Daymark |
| **Backup Linux/GPU technician** (U.S. person) | Named before m8 | (Revised after red team, RT-VC-DD6-03, RT-HYP-DD6-06) a $500/month business-hours retainer; Phase 5 BASE books 0 contractor hours (model §6a). Phase 4: $85/h, only ~25 h (24.5 h) in 36 months, but someone must answer during the founder's day job | Local MSP bench techs; U.S.-person KTransformers and SGLang contributors |
| Advisors: a DIB IT director and a legal-IT director | m1–m3 | 0.25–0.5% equity each [ESTIMATE] | Kill-test interviewees; CMMC Con |
| Insurance (GL, E&O, cyber) | m6 | $900/month (model; Phase 4 $500, RT-HYP-DD6-01) | Tech E&O broker |
| MSP/RPO partners | m13 | 15% of HW, 20% of subscription (Phase 4: 10% / 15%; RT-VC-DD6-06) | §3 #2, #6 |
| Field technician | ≥30 boxes under subscription and founder full-time | $7,500/month (model) | Ex-MSP field engineers. **Never triggered in BASE** (8.2 boxes under subscription at m36, model §5; Phase 4: 22.3) |
| Channel seller | Only with a T1 raise | ~$10k/month [ESTIMATE] | Ex-Exxact, Puget or MSP account managers |

---

## 10. Cheapest experiment that could kill it (revised after red team)

**The ~$7,000 November test is cancelled.** The Phase 4 test (K0–K7, 2026-11-02 → 11-30) was designed to confirm a business that passes. The red team showed the business fails even when the test passes:

- **The best case still loses.** With an 8% close rate, a 6-month cycle and the channel at 3 conversations a month, m36 ARR is $86,763, the 36-month net is +$6,446, and the founder is **never** full-time (model §7).
- **So the test has negative expected value for this founder.** It costs ~$7k and ~55–80 hours that DD2 or another pick could use.

The test was also under-budgeted and triple-booked (RT-VC-DD6-10). K7's 20 conversations at 3 h each is 60 h, more than the ~55 h budget, and it ran on the same dates as DD7's and DD2's tests.

**If a reopen trigger fires (§14.4), run this instead.** It runs on DD6's own calendar, alone, over 6 weeks and ~80 founder hours with a time log. The ~$7k budget (Phase 4 notes §13: ~$6.5k) and $9,500 hard cap [ESTIMATE: set under the <$10k kill-experiment ceiling, notes §13] are unchanged.

| Test | Pass | Fail → action | Changed because |
|---|---|---|---|
| **K0** carve-out | Signed before any call, and also covering daytime installs and meetings | Kill for this founder | RT-VC-DD6-03 |
| **K1** willingness to pay | **Cash:** ≥1 deposit, or ≥2 paid $2,500 pilots with written conversion terms, **and** ≥1 supplier-onboarding packet started at the price card below | Anything less → kill | RT-VC-DD6-02, RT-HYP-DD6-01: LOIs cost a buyer nothing |
| **K1b** price card | Buyers see S **$41k** / L **$79k**, a 30-day quote with a DRAM/GPU index clause, and $650 / ≤$667 a month | ≥50% reject the index clause → price in a ~10% hold premium and re-run | RT-VET-DD6-02, RT-HYP-DD6-07 |
| **K2** cloud substitution | ≥40% of DIB prospects have CUI/ITAR where cloud AI is barred | ≥60% covered → drop defense | unchanged; Phase 2 suspension noted (RT-HYP-DD6-08) |
| **K3** channel | ≥1 MSP/RPO co-sell **in writing** at ≤15% HW / ≤20% subscription, with a 12-month undertaking not to build its own DRAM-resident SKU. Petronella counts as a rival, not a channel | 0 → kill | RT-VC-DD6-06 |
| **K4-S** S performance (re-admits the S SKU) | Socket-pinned EPYC 9005 1S (`numactl --cpunodebind=0 --membind=0`; NPS mode, CCD count and STREAM triad logged), 12 × 32 GB at logged MT/s, RTX PRO 5000 48GB: **≥10 tok/s per user at 3 concurrent with 32k contexts**, TTFT(32k) ≤30 s while 2 other streams hold ≥8 tok/s, peak VRAM logged | Fails → kill | RT-PHY-DD6-01/02/03, RT-VET-DD6-04, RT-VC-DD6-11 |
| **K4-L** L performance (re-admits L) | Same pinning on the exact BOM CPU SKU, 12 × 64 GB: **≥10 tok/s per user at 4 concurrent**, TTFT(8k) ≤40 s with 4 prompts arriving together, a 64k prompt ≤90 s while 3 streams hold ≥8 tok/s, DIMMs <85 °C at ≤45 dBA or in a closet | Default expectation is **fail** (model: 5.5 tok/s at 4; 178 s at 64k) → L stays out | RT-VET-DD6-01, RT-HYP-DD6-05, RT-PHY-DD6-04 |
| **K4-M** Mac cluster | L beats a 2× M5 Ultra RDMA cluster on TTFT(8k) and on per-user tok/s at 4 concurrent, same model and quant | Fails → L is never re-admitted outside the DIB | RT-HYP-DD6-03, RT-VC-DD6-09 |
| **K5** U.S.-origin | A U.S.-origin 500B+ MoE at ≥10 tok/s per user at 2 concurrent on L | Defense is served only on S with ≤400B U.S.-origin models | RT-HYP-DD6-04, RT-VC-DD6-07 |
| **K6** CMMC scoping | Written path in which escorted support keeps the vendor out of scope | Offline-only; re-run the model | unchanged |
| **K7** funnel volume | ≥10 **unpaid** qualified conversations in 6 weeks, ≥3 with budget holders; time log ≤4 h each, including security-review work | Kill | RT-VC-DD6-10, RT-VC-DD6-03 |
| **K8** quality premium | Blind evaluation on the buyers' legal/engineering RAG set: the 200B–1T model is clearly preferred over Gemma 4 31B / gpt-oss-120b on one GPU | No clear preference → the DRAM thesis is moot; kill | RT-VC-DD6-08 |

**Even a full pass only reopens the concept.** To reach full-time by m36 the model needs a 21% close rate, so a pass must also show a close rate ≥12% after the first 30 qualified conversations (criterion 15).

---

## 11. Explicit kill criteria (revised after red team)

**Status: KILLED on 2026-11-01** (§14). The criteria below apply only if a §14.4 reopen trigger fires. Model figures are Phase 5 BASE.

1. **Before any call:** no written employer carve-out → **kill for this founder.**
2. **Within 6 weeks of reopening:** K1 fails (no deposit, no 2 paid pilots, no onboarding packet started), or K7 fails → **kill.**
3. **Within 6 weeks:** ≥60% of DIB prospects already covered by GCC High or Bedrock (K2) → drop defense. Re-test law and universities within 30 days; if they miss criterion 2's bar, **kill.** Universities buying on federal awards need a competitive quote (2 CFR 200.320), so count them as benchmark partners, not buyers (RT-HYP-DD6-01).
4. **Within 6 weeks:** no MSP/RPO co-sell on K3's terms → **kill.** (Phase 4 allowed a side line here; the model now gives −$42,858 with no channel.)
5. **L SKU: fired by default.** It is re-admitted only if K4-L **and** K4-M pass on the exact BOM (RT-VET-DD6-01, RT-HYP-DD6-03).
6. **U.S.-origin 1T on L: fired** (one user per box, §2.3). It is re-admitted only if K5 passes.
7. **C3PAO says remote support puts the vendor in scope with no escorted workaround** → offline-only support; re-run the model. If net turns more negative, **kill.**
8. **By m12 after reopening** (model: first order m10): no deposit banked → **kill.** Phase 4 had this at m9, which was calibrated on a 4-month cycle (RT-HYP-DD6-02).
9. **By m15:** fewer than 1 order, or recurring ARR under $7,000 (model: 1.5 orders, $9,700) → stop new orders; support the existing fleet only.
10. **Any month:** cash under $5,000 for two consecutive months without a committed $25k bridge → stagger or decline the order. If cash stays under $5,000 for a third month → stop.
11. **By m18:** fewer than 2 boxes delivered, or ARR under $12,000 (model: 2.0, $15,814) → never plan a full-time switch; offer the fleet to an MSP.
12. **First anniversaries:** the first three customers renew below 70%, or none takes a non-cancellable 3-year prepay → the recurring thesis fails; exit (RT-VC-DD6-04).
13. **Two consecutive quarters at quote:** authorized-channel lead time for the GPU **or the RDIMMs** exceeds 8 weeks, or no distributor gives a ≥14-day price hold → suspend quoting (RT-VET-DD6-02).
14. **Rewritten: any configuration at or below the L price** that runs a 1T-class model at INT4 at or above the L box's measured per-user rate, **or** a K8 blind evaluation that shows no clear preference for the 1T model → the L box has no reason to exist. **This fires today on the two-node Mac cluster evidence** (RT-HYP-DD6-03, RT-VC-DD6-09, RT-VC-DD6-08).
15. **New: after the first 30 qualified conversations,** a trailing close rate below 12% → exit. Full-time by m36 needs 21% (model §8).

---

## 12. Cycle test: the 2028–29 glut (DDR5 −60%) and the severe case

From 2028-Q1 (m15) the model takes three paths:

- **BASE:** DRAM and GPU prices drift −30% across 2028.
- **GLUT:** DDR5 −60% (the `ddr5_reference()` glut deck); GPUs fall to 55% of today's street price, about the RTX PRO 6000's $8,565 launch MSRP.
- **SEVERE:** DDR5 at $2.04/GB; GPUs at 50%.

Boxes are priced cost-plus, so a glut lowers the box price.

Phase 4 inputs, reproduced by `run_with(P_PHASE4)`. The ARR, full-time and net rows are printed in model §0; the price, GP and salary rows are model §1/§3/§5 on Phase 4 inputs [ESTIMATE: Phase 4 re-run at the Phase 7 gate, not printed in the current output].

| Metric (model §1, §3, §5; Phase 4 inputs) | BASE | GLUT | SEVERE |
|---|---|---|---|
| L box price (BASE: Nov-2026 quote; GLUT/SEVERE: Jan-2028 quote) | $62,525 | $35,779 (−43%) | $25,997 (−58%) |
| HW gross profit per L box | $12,105 | $6,756 | $4,799 |
| 3-yr GP per L customer | $40,366 | $35,016 | $33,060 |
| **Recurring ARR m36** | **$253,693** | **$212,936 (−16%)** | **$197,747 (−22%)** |
| Founder full-time / salary paid | m23 / $140,000 | m28 / $90,000 | m30 / $70,000 |
| 36-mo net after tax | $129,441 | $102,077 | $91,611 |
| GLUT at demand elasticity 1.0 (not 0.3) | — | $321,735 ARR | — |

**Mechanism.**

- Cheaper boxes lift unit demand slightly (elasticity 0.3), but each box carries 44–60% fewer gross-profit dollars.
- Hardware gross profit is what pays the founder, so the full-time switch slips 5–7 months.
- The per-box subscription does not deflate, so the subscription share of revenue rises to 23–28% [ESTIMATE: Σ sub revenue ÷ 36-mo revenue, Phase 4 run; not printed].
- Model §5's "breakeven as run" (BASE m26, GLUT and SEVERE m15) does not mean a glut helps. BASE's earlier full-time switch at m23 briefly pushes EBITDA negative.

**(Superseded by §14: with Phase 5 inputs GLUT and SEVERE are 5–8% above a BASE that never pays the founder; the glut is irrelevant to a business this small.)** Current model, Phase 5 inputs, BASE / GLUT / SEVERE: L box $78,708 (Nov-2026) / $36,752 / $26,240 (Jan-2028), HW gross profit per L box $13,500 / $6,090 / $4,234 (model §1, §3; L is out of BASE); recurring ARR m36 $63,873 / $66,969 / $68,675; founder full-time never, $0 salary paid; 36-month net −$29,411 / −$24,164 / −$21,971 (model §5). Phase 4 verdict: **it survives every glut case, shrinking 16–22%. It is the only concept in the study that still pays its founder through the glut.** The round-2 selection rationale ("the only concept that BENEFITS from a DRAM glut", `selection.json`) is **not supported** at the base elasticity. It holds only if a 43% price cut roughly doubles demand (elasticity 1.0 gives $322k).

**Caveats:**

1. **Substitutes get cheaper too.** DDR5 stays ~6.5× cheaper per GB than GPU memory ($25.78 vs ~$167) and ~9× in a glut ($10.31 vs ~$92) [ESTIMATE], but Macs and DGX boxes also fall in price, so elasticity is set low.
2. **GPUs may stay scarce** while DRAM falls. Then the box falls less, and demand gains less.
3. **Timing.** The glut lands at m15, as the channel starts and before the founder is full-time. Quitting at m23 means quitting into falling profit per box, which is why the trigger demands $30k of post-tax cash.
4. **The real threats are product-shaped, not DRAM-shaped:** unified-memory desktops, smaller models catching up, and the open-source stack getting easier. Kill criterion 14 watches for them.

---

## 13. Sources

Every URL below is logged in `research/sources/*.jsonl` (mostly `p4-private-moe-appliance.jsonl`; the licence fact in `p4w-private-moe-appliance.jsonl`; the Gemma 4 source in `p4v-private-moe-appliance.jsonl`). All are snippet grade unless the log says OPENED.

**Engine and performance (OPENED via git)**
- https://github.com/kvcache-ai/ktransformers
- https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/DeepseekR1_V3_tutorial.md
- https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/Kimi-K2.5.md
- https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/Kimi-K2-Thinking.md
- https://madsys.cs.tsinghua.edu.cn/publication/ktransformers-unleashing-the-full-potential-of-cpu/gpu-hybrid-inference-for-moe-models/

**Models and PRC-origin policy**
- https://opencurious.com/open-source-ai-models
- https://unsloth.ai/docs/models/nemotron-3-ultra
- https://www.ertas.ai/blog/the-2026-open-source-ai-model-landscape
- https://www.yottalabs.ai/post/gemma-4-hardware-requirements-gpu-memory-2026
- https://therecord.media/bipartisan-bill-ban-deepseek-federal
- https://www.scmp.com/news/china/science/article/3315838/china-tied-ai-tools-deepseek-face-us-federal-ban-over-threat-national-security

**Component prices and margins**
- https://tech-insider.org/nvidia-rtx-pro-6000-blackwell-price-2026/
- https://gpuprix.com/us/gpus/rtx-pro-6000-blackwell
- https://tech-insider.org/rtx-5090-shortage-price-surge-2026/
- https://store.supermicro.com/us_en/4u-gpu-superserver-amd-epyc-genoa-as-4125gs-tnrt.html
- https://www.sec.gov/Archives/edgar/data/0001375365/000137536526000022/smci-20260630.htm

**Substitutes and competitors**
- https://macworld.com/article/3271691/the-mac-studio-with-512gb-of-ram-is-shipping-and-it-costs-new-car-money.html
- https://llmconfigurator.com/en/blog/mac-studio-m5-ultra-512gb-which-moe-models-fit
- https://www.implicator.ai/nvidia-adds-64gb-dgx-spark-at-4-999-as-128gb-model-climbs-to-6-950/
- https://www.servethehome.com/nvidia-dgx-station-systems-available-at-last-gb300-gb200-workstations-for-your-desktop
- https://www.tomshardware.com/desktops/nvidias-gb300-powered-dgx-station-desktop-tower-listed-for-nearly-usd100-000-online-enterprise-ai-powerhouse-now-available-to-buy-for-mere-mortals-with-lots-of-cash
- https://wccftech.com/nvidia-dgx-station-upgraded-gb300-blackwell-ultra-desktop-superchip/amp/
- https://pugetsystems.com/solutions/ai-and-hpc-workstations/ai-large-language-models
- https://www.avadirect.com/4U-Eight-GPU-Large-Language-Model-Server/Configure/19085238
- https://buy.hpe.com/us/en/enterprise-solutions/cloud-solutions/storage-cloud/hpe-private-cloud-ai-small-g2-bundle/p/s6m55a
- https://www.petronellatech.com/ai/on-premise-ai/
- https://book.petronellatech.com/compliance/compliancearmor/
- https://book.petronellatech.com/blog/private-ai-deployment-guide-enterprise/
- https://techcrunch.com/2025/06/11/uptime-industries-wants-to-boost-localized-ai-usage-with-an-ai-in-a-box-called-lemony-ai
- https://iternal.ai/local-llm.md
- https://spellbook.com/learn/legal-ai-tool-pricing
- https://www.firstfocus.com.au/insights/mid-sized-business-budget-for-ai/

**Cloud alternatives and CMMC**
- https://www.daymarksi.com/blog/microsoft-365-copilot-in-gcc-high-what-dib-subcontractors-need-to-know-about-deploying-ai-without-breaking-cmmc
- https://www.summit7.us/blog/copilot-for-gcc-high-faq
- https://anthropic.com/news/claude-in-amazon-bedrock-fedramp-high
- https://support.claude.com/en/articles/13756069
- https://aws.amazon.com/blogs/machine-learning/supercharge-regulated-workloads-with-claude-code-and-amazon-bedrock/
- https://secureframe.com/blog/cmmc-level-2-ai-governance
- https://coalfirefederal.com/resource/ai-and-cui-what-cmmc-level-2-assessors-look-for/
- https://cybertronit.com/blog/can-defense-contractors-use-chatgpt-under-cmmc
- https://a-lign.com/articles/4-cmmc-myths-busted
- https://www.strikegraph.com/blog/cmmc-phase-2-deadline-november-2026
- https://www.infonaligy.com/blog/cmmc-level-2-assessment-bottleneck
- https://cybersheath.com/company/news/cybersheath-opens-registration-for-cmmc-con-2026-as-phase-2-deadline-and-assessor-shortage-bear-down-on-defense-contractors/

**Buyers**
- https://www.lw.com/en/practices/admin/upload/SiteAttachments/Latham-Own-AI-Servers-Give-Firm-Best-Options-Leaders-Say.pdf
- https://www.advantech.com/es-es/resources/case-study/enhancing-legal-consultation-services-with-genai-and-llms
- https://docs.arc.vt.edu/resources/compute/05cui.html
- https://services.udel.edu/TDClient/32/Portal/Requests/Service/516/University-of-Delaware-Secure-Computing-UDSecCom-Enclave

**Phase 5 red-team additions (logged in `research/sources/p5r-private-moe-appliance.jsonl`; all search-snippet grade)**
- https://www.publicsector.shidirect.com/product/49991475/64GB-DDR5-6400-RDIMM
- https://shop.avoira.com/origin-storage-64gb-ddr5-6400mhz-rdimm-2rx4-ecc-1-1v-4x77a90966-os.html
- https://www.amcompute.com/appraisals/ddr5-64gb-rdimm
- https://www.shidirect.com/product/50313204/NVIDIA-RTX-PRO-5000-Blackwell
- https://www.jenner.com/en/news-insights/client-alerts/department-of-war-suspends-cmmc-phase-iibut-compliance-obligations-remain-as-does-enforcement-risk
- https://blogs.mcguirewoods.com/2026/07/14/dow-suspends-cmmc-phase-ii-requirements-launches-60-day-review/
- https://www.hstoday.us/?p=223184
- https://redspin.com/?p=79394
- https://jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5
- https://creativestrategies.com/research/running-a-1t-parameter-model-on-a-40k-mac-studio-cluster/
- https://www.hardware-corner.net/mac-rdma-over-thunderbolt-llm/
- https://www.lmsys.org/blog/2025-10-22-KTransformers

**Procurement, IP and funding**
- https://github.com/GSA/GSA-Acquisition-DFARS/blob/master/dita/252.246-7008.dita
- https://www.federalregister.gov/documents/2026/02/17/2026-03065/federal-acquisition-regulation-prohibition-on-certain-semiconductor-products-and-services
- https://www.panabee.com/news/netlist-earnings-q2-2026-report
- https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/
- https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and

---

## 14. Red-team outcome

**Phase 5, agent `p5r-private-moe-appliance`, 2026-11-01.** Four adversarial reviewers raised **32 objections** against DD6: VET (DRAM veteran), VC (semiconductor VC), HYP (hyperscaler procurement lead) and PHY (physicist). There were **1 FATAL, 19 MAJOR and 12 MINOR**. Every objection, my full response and the action taken are in `research/phase5/responses_private-moe-appliance.json`; none is deleted. The model changes are in the RED-TEAM REVISIONS (Phase 5) block of `models/private-moe-appliance.py`, and the output is re-written to `research/phase4/private-moe-appliance_model_output.md`. WebSearch: 5 of 5 used; sources are in `research/sources/p5r-private-moe-appliance.jsonl` and assumptions in `research/assumptions/p5r-private-moe-appliance.md`.

**Dispositions:**
- **5 ACCEPTED-KILL**, killing two legs. The L "Team-1T" box (1-2 users, not 4; beaten by a $44.6k Mac cluster outside the DIB) dies, and so does the U.S.-origin 1T defense box (one user).
- **17 ACCEPTED-DOWNGRADE.**
- **10 ACCEPTED-MITIGATED.**
- **0 REFUTED.** I could not defeat any objection with evidence. There are two partial rebuttals, and neither changes a disposition:
  - The 1.29× dual-socket figure that VET used against L_single_tps reflects weight duplication, not a bandwidth limit.
  - The Llama 3 GPU failure rate behind HYP's field-service objection was measured under training load, so I modelled about a third of it.

| Objection | Severity | Disposition | Action (short) |
|---|---|---|---|
| RT-VET-DD6-01 | FATAL | ACCEPTED-KILL | L box serves 1-2 users, not 4; L SKU leaves BASE |
| RT-HYP-DD6-03 | MAJOR | ACCEPTED-KILL | 2-node Mac RDMA cluster beats L on price and TTFT outside the DIB |
| RT-HYP-DD6-04 | MAJOR | ACCEPTED-KILL | U.S.-origin 1T on L is a one-user box; defense-on-L leg dead |
| RT-VC-DD6-07 | MAJOR | ACCEPTED-KILL | Defense segment on L: 1 user per box; leg dead |
| RT-VC-DD6-09 | MAJOR | ACCEPTED-KILL | Cheaper, faster 1T substitute exists (2x Mac Studio); KC14 drawn to miss it |
| RT-HYP-DD6-01 | MAJOR | ACCEPTED-DOWNGRADE | New LLC can't PO direct easily: close 8->6%, VAR paper fee, insurance $900 |
| RT-HYP-DD6-02 | MAJOR | ACCEPTED-DOWNGRADE | Sales cycle 4 -> 7 months; KC8 moved to m12 |
| RT-HYP-DD6-05 | MAJOR | ACCEPTED-DOWNGRADE | Long-prompt prefill serializes: L 64k TTFT ~178 s; K4 extended |
| RT-HYP-DD6-06 | MAJOR | ACCEPTED-DOWNGRADE | Field service: $500/mo retainer, loaner GPU, 4% reserve |
| RT-HYP-DD6-07 | MAJOR | ACCEPTED-DOWNGRADE | 14-day quotes unworkable: 30-day quotes + index clause + 3% drift |
| RT-PHY-DD6-01 | MAJOR | ACCEPTED-DOWNGRADE | User counts were knife-edges on wrong bytes; recomputed from routed bytes |
| RT-PHY-DD6-02 | MAJOR | ACCEPTED-DOWNGRADE | 1.29x socket factor stale; 2S L tested (3 users, ~$87k); Track B pinned |
| RT-VC-DD6-01 | MAJOR | ACCEPTED-DOWNGRADE | Model rewarded price rises; demand now falls 0.5% per 1% above the card |
| RT-VC-DD6-02 | MAJOR | ACCEPTED-DOWNGRADE | 8% close rate unmeasured; cut to 6%; K1 demands cash; even 8% never pays founder |
| RT-VC-DD6-03 | MAJOR | ACCEPTED-DOWNGRADE | Founder hours were exactly consumed; retainer $500/mo, 4 h/conversation |
| RT-VC-DD6-04 | MAJOR | ACCEPTED-DOWNGRADE | Recurring line untested: only 30-35% of m36 ARR has faced a renewal; churn 30% |
| RT-VC-DD6-05 | MAJOR | ACCEPTED-DOWNGRADE | Founder economic profit ~$8k (P4) and -$228k (P5); m36 cash is mostly customers' money |
| RT-VC-DD6-06 | MAJOR | ACCEPTED-DOWNGRADE | Channel = competitors; partner 15%/20%, 2 conversations/mo; Petronella is a rival |
| RT-VC-DD6-08 | MAJOR | ACCEPTED-DOWNGRADE | Frontier moved to 2.8T (Kimi K3); 768 GB is last generation; quality eval added |
| RT-VET-DD6-02 | MAJOR | ACCEPTED-DOWNGRADE | RDIMMs at $42.5/GB; L quotes $78.7k; price now cuts demand |
| RT-HYP-DD6-08 | MINOR | ACCEPTED-DOWNGRADE | CMMC Phase 2 suspended 2026-07-13; dates corrected |
| RT-VC-DD6-11 | MINOR | ACCEPTED-DOWNGRADE | Named users were derived from chat-length prompts; 32k design context now |
| RT-HYP-DD6-09 | MINOR | ACCEPTED-MITIGATED | GeForce out; RTX PRO 5000 via authorized channel |
| RT-HYP-DD6-10 | MINOR | ACCEPTED-MITIGATED | GDC air-gapped Gemini added as a top-of-range competitor |
| RT-PHY-DD6-03 | MINOR | ACCEPTED-MITIGATED | S KV ceiling fixed by 48 GB card; capacity() has a VRAM term |
| RT-PHY-DD6-04 | MINOR | ACCEPTED-MITIGATED | Not a quiet office tower: closet/colo, 20 A circuit, DIMM temps; install 12 h |
| RT-PHY-DD6-05 | MINOR | ACCEPTED-MITIGATED | L ships a 13th RDIMM as on-site cold spare; S has a 10-DIMM degraded mode |
| RT-VC-DD6-10 | MINOR | ACCEPTED-MITIGATED | Kill test under-budgeted and triple-booked; cancelled, and if reopened run alone |
| RT-VET-DD6-03 | MINOR | ACCEPTED-MITIGATED | S re-specced on RTX PRO 5000 48GB ($8,216, SHI) |
| RT-VET-DD6-04 | MINOR | ACCEPTED-MITIGATED | K4 pinned to exact BOM, socket-pinned, >=10 tok/s line |
| RT-VET-DD6-05 | MINOR | ACCEPTED-MITIGATED | Provenance sheet limited to SPD-readable vendor IDs; no 'non-PRC' claim |
| RT-VET-DD6-06 | MINOR | ACCEPTED-MITIGATED | 48-h soak + CE telemetry + spare pool held as inventory |

### 14.1 Changes made

1. **Model** (`models/private-moe-appliance.py`). It now changes 25 inputs, old → new, each tagged with its objection id; model §0 prints the table. `run_with(P_PHASE4)` reproduces Phase 4 exactly ($253,693 / m23). The model exits 0. The new mechanics are:
   - **Bandwidth capacity model.** Step time is fixed time + distinct-expert bytes ÷ effective DRAM bandwidth, with a GPU KV-memory cap (VET-01, PHY-01/02/03).
   - **Capacity-capped subscription** at $50 per named user (VET-01).
   - **Demand response to price rises** against the fixed Phase 4 price card, at elasticity 0.5 (VC-01, VET-02).
   - **DRAM shortage premium** of 1.65× that unwinds across 2028 (VET-02).
   - **5% VAR-paper fee** on half of founder-sourced deals (HYP-01).
   - **3% drift between quote and purchase** (HYP-07).
   - **Spare-RDIMM pool and loaner GPU** held as inventory (VET-06, HYP-06, PHY-05).
   - **New honesty metrics:** renewal-tested ARR, customers' money in cash, founder economic profit, and subscription share of gross profit (VC-04, VC-05).
2. **Product.**
   - The L SKU is out of BASE and quoted to no one unless K4-L and K4-M pass. If it returns, it ships 13 RDIMMs (one an on-site cold spare).
   - The S SKU uses an RTX PRO 5000 Blackwell 48GB from an authorized channel; no GeForce parts anywhere.
   - Both are server-closet or colo devices, not quiet office towers.
   - The burn-in is renamed a 48-hour soak, with correctable-error telemetry added.
   - The provenance sheet lists the SPD-readable DRAM, RCD, PMIC and hub vendors and makes no "non-PRC" claim.
3. **Commercial terms.**
   - Quotes are now valid 30 days, with a DRAM/GPU index clause.
   - Service is next-business-day for DIMMs, NVMe and PSUs, and a 2-business-day loaner for GPUs.
   - A U.S.-person backup technician is on a $500/month retainer.
   - Petronella is reclassified as a rival, not a channel.
   - Universities become benchmark partners, not buyers.
4. **Facts corrected.**
   - CMMC Phase 2 was suspended on 2026-07-13 (§3, §7).
   - The 2-node Mac RDMA cluster and GDC air-gapped Gemini were added to §5.
   - The 1.29× socket factor and the 16 GB/token read were corrected in §1.
5. **Kill experiment (§10).** It is cancelled, because a pass does not produce a viable business. A reopen-only version is specified: run alone, cash-based K1, pinned K4, a Mac head-to-head, and a blind quality evaluation (K8).
6. **Kill criteria (§11).** All are revised. Criteria 5, 6 and 14 have fired, and 15 is new: exit if the close rate is below 12% after 30 conversations.

### 14.2 Revised headline economics (re-run model §0 and §5; Phase 4 in the last column)

| | BASE | GLUT | SEVERE | Phase 4 BASE |
|---|---|---|---|---|
| First order | m10 (2027-08) | m10 | m10 | m7 |
| ARR m18 | **$15,814** | $17,365 | $17,702 | $53,099 |
| ARR m36 | **$63,873** | **$66,969** | **$68,675** | $253,693 |
| … renewal-tested | $22,645 | $25,340 | $26,174 | $75,334 |
| Founder full-time | **never** | never | never | m23 |
| Breakeven as run (founder unpaid) / at $10k salary | m28 / **never** | m26 / never | m25 / never | m26 / m20 |
| 36-month net after tax | **−$29,411** | −$24,164 | −$21,971 | $129,441 |
| External capital drawn | $25,000 | $25,000 | $25,000 | $0 |
| Founder economic profit | −$228,311 | −$223,064 | −$220,871 | $7,891 |
| Kill-test-pass case (8% close, 6-month cycle, channel 3/mo) | $86,763 ARR; +$6,446; never full-time (model §7) | $93,260; +$14,411 [ESTIMATE: same overrides run on GLUT; not printed] | $96,299; +$15,095 [ESTIMATE: same, SEVERE; not printed] | — |

The economics do not depend on DRAM prices in either direction. A DRAM premium of 1.15 gives −$23,755 and 2.0 gives −$36,496, and the glut cases are 5–8% better than BASE. **What decides the business is the L box's physics and the close rate**, and neither moves with the DRAM cycle.

### 14.3 Revised verdicts

- **POSSIBLE? — Yes for one user; no for a team.** The software is TRL 8–9. The L box gives 16.3 tok/s single-stream but only 1–2 users at ≥10 tok/s (6.7–13.3 named), with ~22 s to the first token at 8k and ~178 s at 64k. U.S.-origin 1T models are one-user. The S box serves ~20 named users. All of this is still unmeasured.
- **PROFITABLE? — No.** BASE is $63,873 ARR at m36, −$29,411 net and $25k drawn. The founder is never full-time and the salary-inclusive breakeven never comes. The kill-test pass is +$6,446 over 36 months. Full-time needs a 21% close rate.
- **DOABLE BY THIS FOUNDER? — Build yes; sell and support part-time no.** Supplier onboarding for a part-time LLC, a ~7-month cycle and delivery hours together push selling down to ~4.8 conversations a month.

### 14.4 FINAL STATUS: **KILLED**

**Reason.**
- **The FATAL objection holds.** CPU decode cannot share expert reads across users: 4 users read 3.88× the bytes. So the L box is a 1–2-user machine. At authorized RDIMM prices it costs $78,708, and a $44.6k Mac cluster matches it with a ~10× faster first token.
- **The L box was the profit engine.** Without it, even on every other Phase 4 assumption, the founder never goes full-time (ARR $109,172; §2.5).
- **The accepted commercial corrections make it worse.** Close rate, cycle, channel terms, support cost, insurance and the price response together turn it into a money-losing S-box integrator that needs a bridge before its first order.
- **Passing the kill test would not change this.** The pass case still never pays a salary.

**Role.** Drop it as a PRIMARY, FALLBACK or MOONSHOT candidate, and cancel the November kill test. The only residue is inbound-only fee-for-service installs on customer-owned hardware.

**Reopen triggers** (unsolicited and costing $0; both (a) and (b) are needed):
- **(a) A channel commitment.** A VAR or MSP commits in writing to take ≥6 boxes a year on its own paper at ≤15%/20%.
- **(b) One of two proofs:**
  - a published or socket-pinned single-socket run showing ≥10 tok/s per user at 4 concurrent on a 1T-class MoE, in a box that quotes ≤$65k (e.g. a next-generation MRDIMM platform [UNVERIFIED-training]); or
  - a blind evaluation in which regulated buyers clearly prefer 200B–1T models over single-GPU 30–120B models.
