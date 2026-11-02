# AI MEMORY DIET: dossier verification log

Verifier: `dosv-ai-memory-diet`, 2026-11-02. Target: `dossiers/ai-memory-diet.md`. WebSearch used: 1 of 2.

## Results by check

| Check | Result | Notes |
|---|---|---|
| (a) Model runs | PASS | `python3 models/ai-memory-diet.py` exits 0 and rewrites `research/stage3/ai-memory-diet_model_output.md` with no diff in git. |
| (b) Sections 0-10 | PASS | All 11 sections are present and substantive: header with verdicts and lineage, mechanism with diagram, physics with 7 subsections, prior art, 10 show-stoppers, decisive experiment, 24-month plan, post-demo, resources, 7 kill criteria, sources. |
| (c) Number tracing | PASS (0 model mismatches; 2 derived-arithmetic fixes) | 40+ numbers spot-checked (list below). All 40 URLs in the dossier appear in `research/sources/*.jsonl`, and their claims match the logged snippets. The Stage 2 verdicts, scores and techniques for all 10 idea ids match `stage2_results.jsonl`. Rank 10 and EV 30 (2 x 3 x 5) match `FINAL_CONCEPTS.md`. |
| (d) Decisive experiment | PASS | $206k external spend (45 + 75 + 36 + 50 = 206), gates at M6, M10 and M14, all pre-set: hold <=1.0 s/turn at <=0.5 FP/turn; p99 added TTFT <=0.30 s at <=3 drive-eq/GPU and <=3 DWPD; latent >=3x at <=1 point RULER loss at 32k. The 2-3x gray zone in G3 is now stated. The full plan totals $882k over 24 months. |
| (e) Prior art not overstated | PASS after fixes | The client-signal claim matches both I-08555 critics ("not found"), and the dossier names LiveMind, prefetch-on-hover and speculation rules as the closest prior art. The latent row omitted MiniCache, which the I-04878 physics critic named; it is now added, and "is open" is softened to "has not been shown". The I-10877 critics named GPUDirect Storage, nvCOMP/DALI and ZeRO-Infinity/FastPersist; a row for these was added. No other "none" claims were found. |
| (f) Founder pronouns | PASS | No gendered pronouns. |

## Numbers spot-checked against the model output (all match)

1. 160 KiB/token FP8; 53.3 KiB latent
2. 32k: 5.24 / 1.75 GB; 128k: 20.97 / 6.99 GB
3. One-drive restore: 0.37 / 1.50 s FP8; 0.12 / 0.50 s latent
4. Gap: median 110 s, P80 372 s, mean 314 s, fitted P99 3,192 s vs 2,207 s reported
5. 87.9% return within TTL; E[min(gap, TTL)] 195 s; 19.5x
6. Base mix: median 8k, mean 13.0k; 2.13 GB/session
7. HBM KV budget 288 x 0.9 - 70 = 189 GB; 89 active; 1,820 conversations/GPU
8. Scenario table A-D: conversations/GPU, p99, DRAM and wafer-eq GB/conversation (A 0.290/0.607 ... D 0.075/0.197)
9. Gains: B0 1.50x / 1.19x; B 1.28x / 1.02x; D0 4.50x / 3.57x; D 3.89x / 3.08x
10. B0 p99 0.33 s; 3.2 drive-eq closes it; hold 1.69 s, +17% HBM
11. Rack 38.0 TB; 12.7 / 8.6 / 5.8 TB freed; 33.3 / 22.7 / 15.2%
12. $18,755 / $253,440; $12,787 / $172,800; $8,525 / $115,200
13. Fab kWh 5,322 / 3,629 / 2,419; water 32,947 / 22,464 / 14,976 L
14. Fleet 0.086-0.127 EB; 0.13-0.19% of 68 EB
15. HBM per conversation 0.158 -> 0.061 GB (2.59x)
16. Flash reads 16.6 GB/s (supply law) and 21.3 GB/s with hold and FP
17. Flash per conversation 13.7 -> 4.6 MB/s
18. Writes 125.6 / 107.4 TB/day per GPU; 859 TB/day per node (diet)
19. Drives: 2.54 bandwidth, 2.33 endurance, 0.31 capacity drive-eq
20. Bill per 1,000 conversations: A $17,200; B0 $15,265 (-11%); D0 $5,088 (-70%)
21. Fixed-context table 16k-128k, FP8 and latent, with and without signal
22. Context limits ~38k / ~21k FP8; ~113k / ~63k latent
23. No-lead table: 3 drive-eq 0.10 / 0.17 s; 2.5: 0.16 / 0.28 s; 2: 0.37 / 0.63 s
24. Section 6b: base 2.2 / 3.2; 64k 3.9 / 6.1; 128k FP8 5.5 / 10.1; signal saves 1.1-4.7
25. First-keystroke hold 8.22 s, +82%, 0.936 wafer-eq GB per conversation
26. Send predictor m=3: 0.66-1.70 s, +7-17%, 0.548-0.601
27. Bigger host tier: 25.2% at 750 GB; 54.6% at 2 TB, 1.267 GB/conversation
28. Price: $18.8k at $1.48/GB; $452k at $35.70/GB
29. Section 2.6: $0.90 / $0.75 / $0.25 wafer-eq $ per conversation; 1.19x / 3.57x
30. 12% never return (1 - 0.879)
31. 24 drive-eq per node, 216 per rack; 21 GB/s ~1/5 of a 100 GB/s NIC
32. ~1.2 GB/s of writes per GPU (107.4 TB/day)
33. 1.9 kW per rack at 0.15 W/GB (12.67 TB)
34. Base p99 context ~82k (model input note)
35. Sources: MHA2MLA 92.19% / 0.5%; TransMLA 68.75%; X-EcoMLA 6.4x and ~70 MI300-h; xKV 8x at 87.8%; TensorMesh ~4x vs ~1.4x; HBM 35-45% / 20-30%; Micron Clay 16 billion kWh/yr and 48 MGD; HBF OCP spec Aug 2026; Samsung PIM mass production end-2026/early-2027
36. Budgets: core 206k; plan 882k (396 + 60 + 206 + 60 + 45 + 35 + 80); reserve $118k

## Fixes applied (surgical edits)

1. **Section 8 energy.** The dossier said "Net: a wash against a no-flash design". 216 drives x ~15 W = 3.2 kW against 1.9 kW of DRAM freed, so the net is ~1.3 kW more than a no-flash design. Changed to state that, keeping ~1.9 kW saved against the 2026 baseline.
2. **Section 2.4 writes.** "125.6 TB/day per GPU (107 with prefetch). That is ~860 TB/day per node" implied 125.6 x 8. 860 = 107.4 x 8. Now reads "With prefetch ... ~860 TB/day per 8-GPU node (~1,000 without)".
3. **Section 5 wear rig.** "12 x $3k plus a JBOF = $36,000" left the JBOF unpriced. It now says the ~$5-10k chassis comes from section 6 contingency, so the totals are unchanged.
4. **Section 5 G3.** The 2-3x gray zone between PASS (>=3x) and FAIL (<2x) is now stated as partial.
5. **Section 3 latent row.** Added MiniCache (named by the I-04878 critic) and xKV as cross-layer retrofits. "A retrofit single shared latent is open" became "A retrofit single latent shared by all layers has not been shown".
6. **Section 3 new row.** Added GPU-direct data paths (GDS, nvCOMP/DALI, ZeRO-Infinity/FastPersist), which the I-10877 critics named.
7. **Header search statement.** "No WebSearch ... was run for this dossier" hid that the research phase used 6 searches (notes). It now says this, and that no patent search has been run.

## WebSearch (1 of 2)

- The query on arXiv 2605.18825 confirmed that the paper exists (SAECache, semantic-aware prefix-cache eviction) and uses log-normal timing. It did **not** re-confirm the median ~110 s gap, which stays as a single-snippet [REPORTED] input. This is the decisive input behind 19.5x and the ~5% host-tier hit rate. The result is logged to `research/sources/dosv-ai-memory-diet.jsonl`.

## Residual risks (not fixed; not errors)

- The 110 s median comes from one snippet. If the median gap were ~30 s (the card's figure), host-tier hit rates would rise and the deletion argument would weaken. Kill criterion 2 tests this.
- "~160 kB per token" in section 1 is a lay rounding of 160 KiB (~164 kB).
- The ~11,000 GPU-h latent line at $50k implies ~$4.5/GPU-h including storage and evals. It is plausible but above the $3/GPU-h used elsewhere.
