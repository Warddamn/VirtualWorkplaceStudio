# Assumptions: agent B (Phase 2, Branch B: architecture and systems)

Format: `- [B] <assumption> — basis: <why / source>`. The numbers are used in the computation embedded in `research/phase2/B_notes.md` §2.

## Research-environment limits (these matter for confidence)
- [B] Vendor-status facts that I could not re-open this session are tagged `[UNVERIFIED-T]` (training knowledge, roughly mid-2026) and carry no URL. This covers Astera Leo, Marvell Structera, Montage, Microchip SMC 2000, Samsung/Micron/SK hynix CMMs, Liqid, GigaIO, XConn, Panmnesia, Unifabrix, Enfabrica, ZeroPoint, Pliops, VAST, Hammerspace, NVIDIA ICMS, d-Matrix, Mythic, EnCharge, Sagence, GSI, UPMEM, Eliyan and SanDisk HBF — basis: the shared WebSearch budget (200 per turn) was already exhausted when B started, and WebFetch could not resolve arxiv.org, asteralabs.com or zeropoint-tech.com (network allowlist). Only public GitHub repos (git clone) were reachable.
- [B] A URL another agent logged from a search snippet is cited as CROSS-REFERENCE and was not opened by B — basis: CONVENTIONS.md source-logging rule.

## Prices ($/GB)
- [B] DDR5 server RDIMM costs about $20–32/GB in 4Q26 (midpoint $26) — basis: Counterpoint's 64GB RDIMM contract went from >$900 in 1Q26 (≈$14/GB), then rose with TrendForce's +58–63%, +13–18% and +10–15% QoQ in 2Q–4Q26; street price was about $2,064 per 64GB (≈$32/GB) in Aug 2026 (ServNet). It is an ESTIMATE.
- [B] In the 2028–29 glut, DDR5 RDIMM costs about $8–12.8/GB (midpoint $10.4) — basis: mission assumption A-05 (−60%) applied to the 4Q26 range.
- [B] Recovered DDR4 RDIMM resale value (the opportunity cost of reusing it) is about $25/GB in 4Q26, about $12/GB in the glut and about $1/GB at the 2023 trough — basis: DDR4 8Gb spot was $21 (TrendForce, 2026-08-03) to $44 (DRAMeXchange via BuySellRAM, 2026-08-31), and 8Gb = 1GB per chip, less a 20–40% discount for used modules. The glut case assumes DDR4 stays "sticky" because supply is EOL. Trough: DDR4 8Gb was $1.30 in Sep 2023 (KED).
- [B] GPU-attached HBM costs about $180–250 per GB of HBM when bought as an H200/B200-class GPU — basis: ESTIMATE of roughly $30k per 141GB GPU. This is not a verified list price. HBM3E at the die level is about $12/GB ($1.50/Gb, SammyFans 2026-10-02).
- [B] Enterprise TLC NVMe costs about $0.30–0.60/GB in 4Q26 — basis: ESTIMATE from about $0.15/GB in early 2025, compounded by the NAND contract increases of 1H26 (+55–60%, +70–75%). NAND turned flat in Oct 2026 and is forecast to reach surplus in 2H27.

## Performance inputs
- [B] H100 SXM dense BF16 peak is 989 TFLOPS at 45% MFU in prefill — basis: the NVIDIA datasheet figure from training knowledge [UNVERIFIED-T]; the MFU is an ESTIMATE.
- [B] An H100-hour costs $2.50 at a neocloud in 2026 — basis: ESTIMATE.
- [B] Production serving uses an FP8 KV cache, which halves the BF16 KV bytes — basis: ESTIMATE / common practice.
- [B] Reload bandwidth: 12 GB/s for one Gen5 x4 NVMe, about 50 GB/s for a CXL x16 Gen5 expander, about 45 GB/s for 400G RDMA, and about 55 GB/s for host DDR5 to GPU over PCIe Gen5 x16 — basis: interface line rates minus about 20% overhead (ESTIMATE).
- [B] Dense-model prefill costs 2×P FLOPs per token — basis: the standard transformer approximation.
- [B] An EPYC 9005 socket has 12 channels of DDR5-6400 (614 GB/s peak), with 60% achievable — basis: platform spec [UNVERIFIED-T] and an ESTIMATE for efficiency.
- [B] A Kimi-K2-class MoE has about 32B active parameters per token, with routed experts in INT4 (0.5 B/param) — basis: model card [UNVERIFIED-T]. KTransformers documents native INT4 for Kimi K2.5.
- [B] A CXL Type-3 expander adds about 70–100 ns over local DRAM (one hop) — basis: the Pond paper (ASPLOS '23) as I recall it [UNVERIFIED-T].

## Hardware cost inputs
- [B] A low-volume CXL add-in card without DRAM (controller, PCB, firmware and qualification amortized) costs about $1,200 per 512GB card (≈$2.34/GB). At hyperscaler volume an in-house board costs about $250 (≈$0.49/GB) — basis: ESTIMATE. Merchant controller prices are not public.
- [B] A hyperscaler dumping DDR4 into the market realizes about 50% of spot — basis: ESTIMATE. Selling millions of DIMMs would move the price.
- [B] The on-prem MoE appliance platform (2S EPYC board, CPUs, chassis, PSU, 2 workstation GPUs) costs about $36k excluding DRAM, and the hardware gross-margin target is 22% — basis: ESTIMATE.
- [B] Holding about 1TB of model weights entirely in HBM takes 8 H200-class GPUs at about $30k each (≈$240k) — basis: ESTIMATE.
- [B] An FPGA-based CXL compression card (Agilex 7 R-tile or Versal Premium class) has a BOM of about $3–8k before DRAM — basis: ESTIMATE from FPGA dev-kit pricing [UNVERIFIED-T].
- [B] Tape-out of an N6/12nm memory-controller chiplet, including masks, IP and packaging NRE, costs $20–60M — basis: ESTIMATE.

## Judgment calls
- [B] Branch B cards stay hardware/system/IP. Anything mostly software (KV-cache SaaS, memory-tiering daemons, RAM-as-a-service brokerage, price data) was left to Branch D and listed as "considered, not carded" in B_notes.md.
- [B] A vendor's CXL product counts as "shipping" only where B has a primary source. Otherwise it is "announced/[UNVERIFIED-T]".
- [B] The DDR4-in-CXL reuse economics are scored from the owner's point of view: reuse beats resale only if card $/GB + DDR4 resale $/GB < new DDR5 $/GB.
- [B] For the founder, "doable" means startable with <$50k, a day job, and no hardware engineering team in the first 12 months.
