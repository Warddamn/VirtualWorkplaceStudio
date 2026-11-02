# Assumptions: B4-architecture (phase B, lens "ARCHITECTURE: DO DRAM'S JOB WITH LESS DRAM")

Agent key `B4-architecture`. Written 2026-11-01. These numbers feed three files: `research/models/B4_architecture_estimates.py` (python3 exits 0), `research/phaseB/B4-architecture.json` and `research/phaseB/B4-architecture_notes.md`.

## Network and evidence
- [B4-architecture] Search budget: I used all 15 of my WebSearch calls and no WebFetch. Basis: the task's network rules.
- [B4-architecture] Snippet-only evidence: every web fact comes from a search snippet and carries "(via search snippet)" in `research/sources/B4-architecture.jsonl`.
- [B4-architecture] Cross-references: 16 log entries marked CROSS-REF were copied from the A1/A3 logs and not re-searched. Basis: MISSION rule 4.
- [B4-architecture] Training-knowledge facts: these have no URL from this session, are tagged [UNVERIFIED] wherever they appear, and are never given a URL:
  - Smart Refresh (MICRO 2007); ESKIMO (MICRO 2009); Intel Hi-ECC (ISCA 2010); COP (ISCA 2015);
  - Quest (ICML 2024); SeedLM (Apple 2024); Matryoshka Quantization (Google 2025); Draft&Verify and LayerSkip self-speculative decoding;
  - DRISA and DrAcc; the ThruChip inductive-coupling interface (Keio);
  - NVIDIA L2 compute-data compression;
  - typical NAND read-disturb limits (1e5–1e6 reads per block) and P/E ratings (TLC ~3k, pSLC ~30–100k).
- [B4-architecture] Unpinned attributions:
  - The Celestial AI claim that disaggregation "cut DRAM requirements by up to 35%" appeared in a snippet without a pinned source, so I did not use it in any card.
  - The IBEX paper's attribution to arXiv 2603.26131 is not pinned.
  - The 1997 4-level 4 Gb DRAM is known only through a patent citation (Murotani et al., ISSCC 1997 TP4.6). NEC affiliation is unconfirmed.

## Shared anchors (imported from `models/dram_cell_physics.py`, A1)
- [B4-architecture] I imported A1's array values rather than re-deriving them:
  - VARY 1.05 V, precharge 0.525 V, droop budget 15% of VARY (155 mV), so V_sig at end of retention = 0.37 V.
  - Cbl = 0.06 fF/cell + 4 fF: 34.7 fF at 512 cells, 7.84 fF at 64.
  - 50 mV hard sense budget; 46 fJ per bit-refresh; 1β die 0.447 Gb/mm²; array efficiency 0.508.
  - Basis: sibling model.
- [B4-architecture] Refresh power per 64 GB RDIMM is 0.49 W at 64 ms. Basis: A1 §3.
- [B4-architecture] tRFC/tREFI values: 295/3,900 ns at 16 Gb; 1,600/7,800 ns at 64 Gb (A1 extrapolation, DDR4-style tREFI). Basis: A1 INPUTS.
- [B4-architecture] DDR5 1-beta costs ~$1.48/GB. Basis: ram-venture cost stack.

## Sense-error model (B4-01, B4-05)
- [B4-architecture] I read A1's 50 mV sense budget as z = 7.03, i.e. a 1e-12 per-bit error with Gaussian offset plus coupling noise, giving σ_eff = 7.1 mV. Basis: judgement. A1 calls the 50 mV "SA offset (after compensation) + coupling noise + guard", which makes this the most direct reading. Real tails may be heavier than Gaussian, which would weaken B4-01.
- [B4-architecture] SA offset is static per sense amp. Codewords are therefore laid along a row, where each bit passes through a different SA, and errors across a codeword are taken as independent. Basis: standard open-bitline array organisation. Pattern-dependent coupling breaks this assumption; it is flagged as a show-stopper in B4-01.
- [B4-architecture] BCH sizing uses binary BCH over GF(2^m), with m·t parity bits and Poisson error counts. The target is ≤1e-15 failure per codeword. Basis: standard approximation, slightly conservative for small t.
- [B4-architecture] Capacitor height scales linearly with required Cs; the pillar-bottom contribution is ignored. Basis: A1 pillar geometry. This slightly overstates the height saving at very short pillars.

## Retention-tail model (B4-01, B4-02, B4-04, B4-08)
- [B4-architecture] The tail is modelled as BER(t) = 3.6e-9 · (t / 0.256 s)^3 at the calibration temperature, then derated 4× in time for 85 °C. That gives 3.6e-9 at 64 ms, 1.4e-5 at 1 s and 1.1e-4 at 2 s.
  - Calibration: a recollection of RAIDR's "~1,000 cells in 32 GB need refresh below 256 ms" [UNVERIFIED].
  - Cross-check: recollections of Flikker-era data, ~1e-7 at 1 s and ~1e-3 at 20 s [UNVERIFIED].
  - This is the single most load-bearing assumption in the lens. B4-02's first experiment exists to measure it.
- [B4-architecture] Retention time scales as Cs/I_leak. A capacitor scaled by s therefore scales tail times by s. Basis: A1 (retention ∝ Cs/I_leak).
- [B4-architecture] VRT accumulation between scrubs is taken as 3× the static weak-cell count. Basis: judgement; VRT rates were not found this session.
- [B4-architecture] One syndrome XOR toggle costs 2 fJ in a DRAM-periphery process, and syndrome work is (m·t/2) XORs per bit. Basis: judgement for slow, high-Vt periphery transistors.

## Temperature (B4-13)
- [B4-architecture] I bracketed retention gain between two models: the A1 rule of thumb (retention halves per 10 °C) and Arrhenius with Ea = 0.25 eV (GIDL/trap-assisted tail) or 0.55 eV (SRH junction generation). Basis: textbook leakage mechanisms. The rule of thumb is likely optimistic below ~50 °C.

## AI-workload numbers (B4-03, B4-04, B4-06, B4-07, B4-09, B4-16, B4-18, B4-19, B4-21)
- [B4-architecture] KV cache per token for a 70B-class model is 328 KB: 8 KV heads × 128 dim × 80 layers × 2 (K, V) × 2 B. Basis: Llama-70B-style GQA geometry from training knowledge.
- [B4-architecture] BF16 exponents Huffman-code to 2.9 b including table overhead, against DFloat11's ~2.6 b entropy. The FP8 E4M3 exponent entropy is assumed to be 2.0 b, and FP4 E2M1 1.5 b. Basis: DFloat11 snippet plus judgement.
- [B4-architecture] The server ECC baseline is 12.5% (16+2 ECC-DIMM-style), so a BF16 value occupies 18 cells. Basis: x4/x8 ECC RDIMM convention.
- [B4-architecture] Mantissa planes tolerate BER 1e-5 and the KV mantissa tolerates 1e-4, per the RangeGuard and SHIELD snippets. I assume these transfer to 70B-class models and long generations. Basis: reported results on 1B–8B models. This is unverified at larger scale.
- [B4-architecture] HBM sweep configurations: 141 GB at 4.8 TB/s, 192 GB at 8 TB/s, 288 GB at 16 TB/s. Basis: H200/B200-class figures in A1; the 288 GB case is hypothetical.
- [B4-architecture] Recomputing a token's KV costs 2 × 70e9 FLOP at ~1 pJ/FLOP. Basis: judgement for a modern GPU at BF16.
- [B4-architecture] Top-k sparse attention scenario: 4 MSB planes of an INT8 K serve as the sketch, with k = 2,048 tokens out of 128k. Basis: typical settings in query-aware sparsity papers [UNVERIFIED].
- [B4-architecture] HBF capacity per dollar, two cases:
  - TLC: 8–16× HBM per $ (company claim).
  - pSLC: one third of that capacity, hence 3–5× HBM per $.
  - Basis: SanDisk PR (snippet) plus arithmetic.
- [B4-architecture] HBF read rate per page equals stack bandwidth divided by model size: every weight is read once per decode step. Basis: decode is weight-streaming.
- [B4-architecture] Self-speculative acceptance rates of 0.8–0.9 for a 4-bit draft and 0.85 for a 2-bit draft (with k = 6) are judgement calls. Basis: typical speculative-decoding acceptance; no source found for nested-quant drafts.
- [B4-architecture] In-bank PIM energy is 0.1–0.3 pJ/b, covering amortised activation plus the ADC. Basis: A1/RPU streaming activation of 0.05–0.18 pJ/b plus ADC overhead (judgement).
- [B4-architecture] Charge-sharing popcount uses a 5% Cs mismatch (1σ). Basis: judgement for DRAM capacitor variation.
- [B4-architecture] Broadcast weight bus scenarios: 140 GB at 30 steps/s and 810 GB at 20 steps/s. Optical excess loss is 3 dB on top of the ideal 1:N split. Basis: judgement.

## Interfaces and packaging (B4-11, B4-12, B4-14, B4-15)
- [B4-architecture] Per-die-in-stack yields of 0.98, 0.95 and 0.90 are scenarios, not data. 0.95 represents immature hybrid bonding at 16-high. Basis: A1 (bonding yield collapses across 16–20 bonds); no per-bond yield data was found.
- [B4-architecture] The HBM die area penalty is taken as 40% (the midpoint of TrendForce's 35–45%), giving HBM array efficiency ≈ 0.508/1.4 = 0.36. A streaming die is assumed to reach 0.45–0.55. Basis: judgement; floorplan study pending.
- [B4-architecture] Photonic link energy is ~1 pJ/b for modulator, driver and receiver, ~1 pJ/b for laser wall-plug and 0.1–1 pJ/b for ring tuning. Basis: typical silicon-photonics link budgets (training knowledge), checked against Celestial's reported 2.4–6.2 pJ/b.
- [B4-architecture] LPDDR HBM-lite energy terms, all judgement within published ranges: LPDDR core access ~1.5 pJ/b, short LPDDR I/O ~0.5 pJ/b, buffer logic ~0.2 pJ/b. Organic-substrate escape is ~50 lanes/mm per routing layer.
- [B4-architecture] Compaction before self-refresh costs ~10 pJ/b to read, compress and rewrite. Basis: judgement (DRAM read plus write plus LZ4 logic).

## Judgement calls
- [B4-architecture] I judged ideas on physics and demonstrability only, per MISSION.md; no idea was dropped for business reasons. Every rejected idea in the notes names its revival condition.
- [B4-architecture] Ideas that belong mainly to other lenses are referenced, not duplicated:
  - B1 (cell physics): charge-transfer sensing (B1-04), 2-bit 1T1C (B1-05).
  - B2 (materials and fabrication): defect-budget co-design (B2-15), BEOL main memory in logic (B2-16).
  - A3 white space 8: gain-cell PIM.
- [B4-architecture] Ranking weight is physics plausibility × size of step × provability on a $1M, 18–24-month budget.
