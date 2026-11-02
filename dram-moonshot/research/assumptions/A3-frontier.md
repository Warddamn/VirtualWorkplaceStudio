# Assumptions: A3-frontier (phase A research frontier)

Agent key `A3-frontier`. Written 2026-11-01. The numbers below feed `research/models/A3_frontier_estimates.py` and `research/phaseA/A3_research_frontier.md`.

## Network and evidence
- [A3-frontier] I used 30 of the 30-call WebSearch quota and made no WebFetch calls. Every web fact comes from a search snippet and carries "(via search snippet)" in `research/sources/A3-frontier.jsonl`. Basis: the task's network rules.
- [A3-frontier] Venue papers from IEDM 2025, VLSI 2026 and IMW 2025 were seen only through press releases, trade previews (PC Watch, Mynavi, IT Home, cnyes) or repository abstracts. Numbers from them are tagged [REPORTED], never [VERIFIED]. Basis: no full text was reachable.
- [A3-frontier] Entries tagged `[CROSS-REF]` (OCTRAM, Samsung 4F² VCT, the 1 Mb HZO FeRAM, FMC, SK hynix 5-layer, Samsung eMRAM) are reused from ram-venture phase 2 cards and from dram-moonshot A1. I did not re-open them. Basis: MISSION rule 4, reuse rather than redo.
- [A3-frontier] Micron's NVDRAM 10¹⁵-cycle endurance comes from press coverage only. "10-year retention" comes from one Russian-language outlet and is tagged [UNVERIFIED]. Basis: the paper is not public.
- [A3-frontier] Samsung's IGO (zinc-free) result surviving >550 °C comes from a Korean blog and is tagged [UNVERIFIED]. Basis: single secondary source.
- [A3-frontier] NEO 3D X-DRAM numbers are company-reported for a single cell and tagged [CO-REPORTED]. Basis: no peer-reviewed array data.

## Model inputs (A3_frontier_estimates.py)
- [A3-frontier] The gain-cell storage-node capacitance C_SN is 1 fF, against a plausible range of 0.5–2 fF. Basis: read-transistor gate plus parasitic at 20–50 nm devices. Retention ceilings scale linearly with it.
- [A3-frontier] Tolerated storage-node droop is 200 mV for 1 bit. For 3 bits it is 62 mV: a 1 V window over 8 levels, halved. Basis: the usual half-level margin. Real margins after write-verify may be tighter.
- [A3-frontier] The imec 2020 cell is converted to per-cell leakage using a channel width of 50 nm. Basis: 45 nm-class device. imec's "extracted" Ioff is itself derived from retention, so the comparison is indicative only.
- [A3-frontier] Read-bitline capacitance is 0.1 fF per cell plus 5 fF fixed. Read current is 50% of the CXMT-reported 60.9 µA/µm on-current. Basis: a typical gain-cell read-bias derating.
- [A3-frontier] Three-bit sensing is taken to need ~8× the signal-development time of 1-bit sensing. Basis: 8× finer current resolution with the same integrator. SAR or time-domain schemes could do better.
- [A3-frontier] Footprint per cell is 10F² for a vertical-channel 2T0C and 24F² for a planar 2T0C. Basis: two transistors plus a storage-node contact. No published footprint was found for IMECAS or SJTU cells.
- [A3-frontier] Base wafer cost relative to a 1β DRAM wafer is 0.90 at F = 20 nm (SAQP-class litho, no EUV) and 0.55 at F = 40 nm (single-exposure ArF immersion, oxide BEOL plus logic periphery). Basis: judgement anchored to A2's statement that bits are added by deposition rather than lithography. This is the weakest input in §3.3.
- [A3-frontier] Each extra tier adds 12.5% of base wafer cost. Basis: the same convention as A2-resources (10–15%).
- [A3-frontier] The 1β reference is a 1,070 nm² cell with array efficiency 0.508. Basis: A1-scaling's calibration to teardowns. The same efficiency is applied to every design.
- [A3-frontier] The 2T-nC footprint assumes two 8F² transistors plus 50% routing at F = 20 nm. Basis: judgement. All n capacitors sit on a pillar over the transistor pair.
- [A3-frontier] HZO remanent polarisation P_r is 20 µC/cm², against a range of 15–25. Basis: typical HZO reports [UNVERIFIED-training]. The MFM capacitor is the 40 nm pillar wall area times a 20–40 nm layer height.
- [A3-frontier] The endurance duty cases (a hot row every 46 ns tRC, 1/µs, 1/ms, 1/s) run over 5 years. Basis: a server lifetime. tRC of ~46 ns is DDR5-class [UNVERIFIED-training].
- [A3-frontier] The VCMA MTJ is 50 nm in diameter, with MgO k = 9 and 1.2 nm thick. Line capacitance is 1–5 fF. Basis: typical pMTJ dimensions [UNVERIFIED-training].
- [A3-frontier] The cryogenic plant runs at 15–30% of Carnot COP at 77 K. A 12 W RDIMM falls to 30–50% of its warm power when cold. Basis: judgement; large-scale cryoplants are usually quoted at tens of percent of Carnot [UNVERIFIED-training]. Refresh share is ~0.75 W per RDIMM (A1).
- [A3-frontier] Bonding geometry is one bond per bitline segment of 64–256 cells, at bitline and cell pitches of 40/40, 64/64 and 80/120 nm. Basis: an open-bitline segment served from the periphery wafer.
- [A3-frontier] The PIM Amdahl check uses Samsung's 614/76.8 GB/s and 3.01× throughput. It treats the bandwidth ratio as the speed-up of the offloadable fraction. Basis: a first-order Amdahl model.

## Judgement calls
- [A3-frontier] Cryogenic DRAM is killed for data centres on system energy, not device physics. The revival condition is named in §6. Basis: the MISSION framing, physics only, with a named revival.
- [A3-frontier] Floating-body Si 1T is upgraded from ram-venture's "marginal" to alive at TRL 3–4, on the strength of the DFM IMW 2025 abstract (>10 s at 85 °C). Basis: a single abstract. Array tails are required.
- [A3-frontier] 2D materials are downgraded rather than killed. Basis: no physics violation, but no edge over oxide at DRAM-class speed and retention.
- [A3-frontier] The top-3 white spaces were chosen to complement A1's (short-bitline sensing, stackable 2T0C, memory-on-compute) and A2's (bits per capex dollar). White space 1 extends A1's white space 2, and white space 3 builds on A1's white space 1 and A2's white space 1. Basis: avoid duplicating sibling agents.
- [A3-frontier] "No data found" on row-hammer and SER in oxide cells is logged as a gap, not as evidence of immunity. Basis: absence of evidence.
- [A3-frontier] IGZO cannot host a floating-body (hole-storage) cell because it is n-type with no usable hole accumulation. Basis: device physics [ESTIMATE].
