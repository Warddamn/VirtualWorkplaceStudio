# Assumptions: dos-charge-river (CHARGE-RIVER dossier), 2026-11-02

Every numeric ESTIMATE is listed with its basis in the INPUTS block of `models/charge-river.py`. The judgment calls are:

- [dos-charge-river] Each hole is read at BOTH ends (bonded CMOS below, top metal above), so 200 plates give 2 x 32-stage segments and 64 bits per hole. Basis: meets the chief's <=32-stage regeneration spec without a mid-stack amplifier.
- [dos-charge-river] Packets are parked between accesses and lapped on demand, with a scrub every 20 s, rather than circulated continuously. Basis: continuous circulation multiplies decisions ~5e4x and plate cycles to ~8e15 over 5 years (model sections 3 and 9).
- [dos-charge-river] Reliability target: 10 FIT per 16 Gb die, BCH t=2 over 512 bits, 30 reads per bit per second. Basis: DRAM-class reliability and LLM decode at 20-50 tok/s.
- [dos-charge-river] CTE -> BER uses a linear deferred-charge kernel with worst-case patterns, binomial partition noise and Poisson noise on the deferred charge. The DFE residual is kappa = 10% of the deferred charge, and worst-string deferral is k_ws = 1.5x the median. Basis: LSST shows deferred charge is largely modelable; Poisson trap counts plus spread across ~1e8 strings.
- [dos-charge-river] imec's ">98% CTE" is treated as ambiguous: both the per-transfer and the end-to-end (142 b x 4 phases) readings are modelled. Basis: snippets do not define it.
- [dos-charge-river] Trap emission follows SRH with nu0 = sigma v_th N_c ~1e11/s (sigma 1e-15 cm2, m* 0.3, N_c 5e18 cm^-3). Frequency and temperature transfer goes through the trap depth E_w = kT ln(nu0 t_dwell), and trap DOS = exponential tail (W 15-60 meV) + flat part. Basis: first principles; IGZO parameters from training knowledge.
- [dos-charge-river] Buried heterochannel + fat zero cut deferral to 0.18x of imec's surface channel (60% of the loss is interface traps, 90% of that removed, fat zero leaves 40%). Basis: [ESTIMATE]; no oxide buried-channel CCD has been measured.
- [dos-charge-river] Cost: the CHARGE-RIVER wafer is array $1.2k + $10/plate + CMOS $1.8k + bond $0.3k, at 0.8x mature yield, with good area calibrated to ram-venture's $3.8k -> $1.48/GB 1-beta. Basis: [ESTIMATE]; cross-checked against the NAND price x bits-per-hole ratio.
- [dos-charge-river] Planar wide-channel test CCDs measure the same trap-to-electron ratio as 40 nm vertical plates if the sheet charge matches (~4.5e12 cm^-2). Basis: the ratio is area-independent (model section 1); the narrow-channel variants measure granularity separately.
- [dos-charge-river] Startup users pay industry rates at university nanofabs. Basis: published 2025 fee schedules (Penn, KU, UD, Notre Dame, Texas A&M); the SNF, CNF and IEN amounts were not found.
