# Assumptions: dos-ai-memory-diet (stage 3 dossier, AI MEMORY DIET)

Agent key `dos-ai-memory-diet`. Written 2026-11-02. These assumptions feed `models/ai-memory-diet.py`, `research/stage3/ai-memory-diet_model_output.md` and `research/stage3/ai-memory-diet_notes.md`.

## Network and evidence
- [dos-ai-memory-diet] Search budget: all 6 WebSearch calls used; no WebFetch. Every web fact is snippet-only and tagged "(via search snippet)" in `research/sources/dos-ai-memory-diet.jsonl`. Basis: the task's network quota.
- [dos-ai-memory-diet] Cross-references: 7 log entries are marked CROSS-REF (CachedAttention, xKV, DroidSpeak, Cake, Lamina, GMI/TensorMesh, thaw-vllm, Micron HBM 3x). They were copied from earlier dram-moonshot logs and not re-searched. Basis: MISSION rule 4.
- [dos-ai-memory-diet] Training-knowledge facts carry no URL and are tagged [training knowledge]: Llama-3.1-70B shape; Dynamo KVBM tier names; LMCache disk backends; Mooncake (FAST'25); InferCept (ICML'24); NVLink-C2C ~900 GB/s; Gen5 NVMe ~14 GB/s; GB200/GB300 tray E1.S bays; TACC Vista GH200; WildChat timestamps; prefetch-on-hover prior art; group affiliations in notes section 5.
- [dos-ai-memory-diet] Price attribution is unconfirmed: the $35.70/GB and $31.75/GB retail DDR5 medians and the 2.3-2.8x enterprise-SSD price change came from a search summary spanning several pages.

## Model inputs ([ESTIMATE] unless cited in the INPUTS block)
- [dos-ai-memory-diet] Host DRAM per GPU on GB300 = 240 GB (480 GB per Grace, 1 Grace : 2 GPUs). Basis: Red Hat catalog snippet.
- [dos-ai-memory-diet] Host-lite floor = 64 GB/GPU for OS, runtime, GDS/NIXL buffers and the serving process; critic case = 120 GB/GPU. Basis: Stage 2 I-10877 critiques.
- [dos-ai-memory-diet] Serving model = 70B GQA, FP8 weights (70 GB) and FP8 KV (160 KiB/token), one replica per 288 GB GPU, vLLM utilisation 0.9. Basis: the common open-model serving point.
- [dos-ai-memory-diet] Decode floor 30 tok/s per user; HBM 8 TB/s per GPU. The bandwidth bound and the capacity bound are both computed, and the smaller wins. Basis: NVIDIA's 576 TB/s per rack / 72.
- [dos-ai-memory-diet] T_gen = 10 s per turn; 1,000 new tokens per turn (prompt plus response). Basis: concept card 5-10 s; ~500-token answers.
- [dos-ai-memory-diet] Context per session is log-normal, median 8k, sigma 1.0, capped at 128k (mean 13.0k). Basis: no data found; this is the swing input (notes section 8).
- [dos-ai-memory-diet] Human inter-turn gap is log-normal fitted to median 110 s and P80 372 s. The fitted P99 is ~3,190 s vs 2,207 s reported, conservative for capacity. Basis: arXiv 2605.18825 snippet (Qwen-Bailian trace).
- [dos-ai-memory-diet] TTL 600 s for returns counted as warm; flash retention 1 h. Basis: judgment.
- [dos-ai-memory-diet] A today-style LRU host tier holds a session for host_kv_GB / (turn rate x KV) seconds, and its hit share is P(gap < that hold time). Basis: Little's law with LRU approximated as a FIFO hold.
- [dos-ai-memory-diet] The flash restore queue is M/M/1. The diet uses two-class preemptive priority (urgent = lead shorter than the mean low-priority response) and today's design uses FIFO. Write interference is ignored. Basis: tractable and pessimistic on service-time variance, optimistic on writes.
- [dos-ai-memory-diet] Flash = 3 Gen5 drive-equivalents per GPU (local plus pod shelves over the ~100 GB/s NIC), each 15.36 TB, ~14 GB/s, 3 DWPD; rho_max 0.6. Basis: section 4 sizing.
- [dos-ai-memory-diet] Client lead mix: typed 60% (median 8 s, sigma 0.8), paste 20% (2 s), one-click 10% (0.4 s), voice 5% (4 s), no signal 5% (0 s). Basis: judgment; measuring this is Phase 1.
- [dos-ai-memory-diet] Send predictor: restore starts when predicted remaining lead = 3 x expected restore, with multiplicative error sigma 0.7. False-positive prefetches: 0.5 per turn held 2 s in HBM. Basis: judgment; Phase 1 measures it.
- [dos-ai-memory-diet] Uncovered turns use parallel load+recompute, which halves the residual (f_fb = 0.5). Basis: the Cake mechanism; the factor is a guess.
- [dos-ai-memory-diet] p99 added-TTFT budget = 0.30 s (~15% of a 2 s interactive SLO). Basis: judgment.
- [dos-ai-memory-diet] Latent planning case: 3x capacity and 3x per-step read reduction. Basis: MHA2MLA ~3.2x beyond GQA-8, TransMLA, X-EcoMLA 6.4x and xKV 8x training-free. A single all-layer latent re-read per layer would cut reads less.
- [dos-ai-memory-diet] Prices: DRAM $20/GB contract (2026 shortage); HBM priced at 3x DRAM (wafer-proportional); flash $0.20/GB. Basis: snippets plus the Micron HBM wafer ratio. The cost floor is $1.48/GB (ram-venture).
- [dos-ai-memory-diet] Resources: 0.42 kWh and 2.6 L per DRAM GB; world output ~68 EB/yr DDR5-equivalent (upper bound). Basis: A2.
- [dos-ai-memory-diet] GPU rental $3/GPU-h for the budget; drives ~$3k each. Basis: judgment, not verified this session.
- [dos-ai-memory-diet] Founder cost: $9k/month each, loaded. Basis: lean seed norm.

## Judgment calls
- [dos-ai-memory-diet] Baseline = the 2026 state of the art: an HBM + host-DRAM LRU tier + flash (LMCache disk/ICMS), not a no-flash design. The diet's incremental flash is therefore ~0.
- [dos-ai-memory-diet] Demoted the client signal from "the key unknown" to an efficiency lever. The model shows host-lite passes at short contexts without it, and the signal's HBM hold can cancel its benefit in wafer terms.
- [dos-ai-memory-diet] Cross-finetune exact KV sharing kept as a platform rule only. The Stage 2 innovation lens dropped it, and the duplicated cross-variant prefix KV is small.
- [dos-ai-memory-diet] PIM top-k, retired-GPU KV servers and recompute-as-correction are left out of the seed budget (chief note).
- [dos-ai-memory-diet] Facilities: no nanofab or MPW is needed; GPU clusters replace them.
