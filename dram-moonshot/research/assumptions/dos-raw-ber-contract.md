# Assumptions: dos-raw-ber-contract (Stage 3 dossier, RAW-BER CONTRACT)

Agent key `dos-raw-ber-contract`, written 2026-11-02. Every numeric input below appears in `models/raw-ber-contract.py`. Search quota was 6 WebSearch calls, all used. Sources are in `research/sources/dos-raw-ber-contract.jsonl`.

- [dos-raw-ber-contract] Module UE budget from random raw errors is <=1e-3 per 64 GB module-year. Basis: field DIMM UE rates of ~0.2-1%/yr, dominated by hard faults [UNVERIFIED: training knowledge]. This gives 2e-19 per 64 B read at 10 GB/s average.
- [dos-raw-ber-contract] Average module bandwidth is 10 GB/s. Basis: ~25% of a DDR5-4800 channel peak.
- [dos-raw-ber-contract] A DDR5 RDIMM line carries 512 data + 128 check bits (32+8 per subchannel, BL16, x4) [UNVERIFIED: JESD79-5 organisation from training knowledge].
- [dos-raw-ber-contract] DDR5 on-die SEC(136,128) miscorrects a 2-bit error into 3 bits ~53% of the time. Basis: 136 of 255 nonzero syndromes map to a column.
- [dos-raw-ber-contract] Sigma_eff = 50 mV / 7 = 7.14 mV. Basis: concept text and A1 dv_min_mV.
- [dos-raw-ber-contract] The flag window is 0.5 sigma (~3.6 mV), with a reduced-tRCD second read as the proxy. Basis: Solar-DRAM shows reduced-tRCD weak cells are stable.
- [dos-raw-ber-contract] Margin errors are Gaussian (static SA offset + noise, iid along a row-wise codeword).
- [dos-raw-ber-contract] Chase decoding is capped at 8 flagged positions. It ignores miscorrection among candidates, so it is an upper bound.
- [dos-raw-ber-contract] Retention tail at 85 C uses three models: B4's pow3 (3.6e-9 x (t/64 ms)^3); a lognormal through RAIDR-era anchors (30 cells/32 GB at 128 ms and 1,000 at 256 ms, shifted 4x to 85 C; sigma_ln 1.24); and a pow5 bound. A data-pattern factor of 0.5 applies to random data.
- [dos-raw-ber-contract] Retention scales x4 per 20 C (65 C) and x16 per 40 C (45 C). Basis: A1's halving per ~10 C.
- [dos-raw-ber-contract] VRT latches new errors at 1x the static BER per day without scrub (swept 0.1-100). Basis: REAPER (VRT exists) and B4 (x3 accumulation). No measured rate was found.
- [dos-raw-ber-contract] Scrub energy is 3 pJ/bit (IO-dominated sequential read inside the CXL device); scrub runs every 1 h.
- [dos-raw-ber-contract] Bursts are modelled as exactly-b-bit clusters inside one codeword (b=3 or 8). RS bursts are assumed byte-confined, which is optimistic.
- [dos-raw-ber-contract] Hammer: tRC 46 ns, RAAIMT 40, tRFMsb 150 ns, typical 1e6 ACT/s/bank [ESTIMATE / UNVERIFIED].
- [dos-raw-ber-contract] Page-code decode is 1 pJ/bit and the line syndrome fast path 0.05 pJ/bit. Basis: Stage-2 critic estimate; no measured 28 nm figure was found.
- [dos-raw-ber-contract] Value uses $0.10/kWh, PUE 1.3 and a 5-yr life.
- [dos-raw-ber-contract] Budget items are all estimates except the Agilex kit (~EUR 9k), the CXL Type-3 IP list price (~EUR 192k; KIT page, Jan 2025, via snippet) and ChipFoundry sky130 ($15k per 100 chips, via snippet). DRAM Bender station cost ($14k each) is an estimate.
- [dos-raw-ber-contract] The 2e-19/read reliability cannot be demonstrated directly in a 1,000 h soak (~5.6e14 reads per board). It is extrapolated from measured raw-error statistics, so the soak tests for surprises (zero UE, corrected counts within 2x of model).
