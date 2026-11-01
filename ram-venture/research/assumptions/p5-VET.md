# Assumptions — p5-VET (red-team, DRAM process veteran persona), 2026-11-01

- [p5-VET] Stress variants for DD1 (fail_rate 0.08 / return_rate 0.05; mix_ddr5_64 0; buy_frac 0.70; b2b_price_factor 0.75; lab_cost $1,200) are plausible downside values, not point estimates — basis: decommissioned-DIMM CE-driven retirement, absence of ECC-corrected reporting in memtest86+ on Xeon Scalable, DDR5 platform age (2022-23 launch), B2B buyers' own lot+test cost.
- [p5-VET] Pre-i Fanuc share of the installed base ≈ 0.15 (vs DD3's 0.35 incl. i-series) — basis: i-series (16i/18i/21i/0i) accept CF-in-PCMCIA for boot-menu SRAM backup (IMD, snippet); rough split, not sourced.
- [p5-VET] Credible 24/7 kernel on-call with 1–2 h SLA ≈ $3k/month — basis: ~15 reserved hours at $175/h plus availability premium; judgment.
- [p5-VET] Outside-lab ESD/temperature/insertion qualification for a PC Card ≈ $5–10k — basis: typical small-lot qual-lab pricing; judgment, unsourced.
- [p5-VET] FM18W08 cycle time ≈ 130 ns vs 70 ns access, address latched on /CE falling — basis: recollection of Infineon/Cypress datasheet; flagged "verify" in the objection.
- [p5-VET] GF180MCU open-PDK wafers likely run in Singapore — basis: wafer.space Singapore-based (Crowd Supply snippet) and 01_LANDSCAPE §6 listing no GF180MCU at GF's U.S. fabs; UNVERIFIED.
- [p5-VET] Flip Feng Shui (Razavi et al., USENIX Security 2016) cited from training knowledge; URL not opened, so not logged as a source.
