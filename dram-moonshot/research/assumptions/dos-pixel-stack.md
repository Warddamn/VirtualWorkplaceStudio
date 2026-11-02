# Assumptions: dos-pixel-stack (PIXEL-STACK dossier, 2026-11-02)

All values live in the INPUTS block of `models/pixel-stack.py`; this file lists the judgment calls.

- [dos-pixel-stack] Storage-node cross-section 30x25 nm (perimeter 110 nm) inside a 60 nm tier; capacitor C = Cox x (perimeter x length + end cap) — basis: tier thickness minus dielectric and plate liners; single-sided (pillar-like) is conservative vs a cup.
- [dos-pixel-stack] EOT 0.50 nm (69 fF/um2) for the ZrO2-based lateral capacitor, not the concept's 0.45 nm — basis: 1b production ~0.55 nm (A1); <=400 C crystallisation limits further scaling.
- [dos-pixel-stack] Cell footprint = 70 nm (y) x (20 BL half + 70 TFT + Lcap + 15 plate half) nm — basis: Kioxia 3D OCTRAM / OCTRAM pitches (54-63 nm) plus GAA wrap; gives 0.011 um2 at 0.45 fF, inside the concept's 0.010-0.012 um2.
- [dos-pixel-stack] Vertical bitline 0.15 fF per tier + 0.6 fF fixed (3.0 fF at 16 tiers) — basis: 2 mirrored cells per tier with ~0.03 fF drain overlap each plus pillar coupling; matches the concept's ~3 fF.
- [dos-pixel-stack] ECC overhead 592/512 (t=8 BCH at raw BER 1e-4) applied to density — basis: RAW-BER CONTRACT; the concept's density numbers used 1.0625.
- [dos-pixel-stack] Raw-BER target 1e-4 => 3.72 sigma; retention failures share that budget — basis: I-11559 / RAW-BER CONTRACT.
- [dos-pixel-stack] Droop budget 75 mV of the 0.5 V half-swing at end of refresh (the concept's 0.85 factor); leakage spec therefore 34 aA for 1 s at 0.45 fF (the concept's 68 aA assumed 150 mV droop) — basis: internal consistency with the 55 mV signal claim.
- [dos-pixel-stack] SF 100x100 nm, EOT 3 nm, Id 2 uA, Vov 0.4 V, gain 0.90 with 2% sigma — basis: amp-tier area per vertical BL (~0.022 um2) and CXMT 60.9 uA/um drive.
- [dos-pixel-stack] 1/f via Hooge mobility-fluctuation model with alpha 1.5e-3 (Fung JAP 2010) swept to 1e-1 — basis: scaled ALD devices are trap-dominated (Lee & Niu TED 2025) and Al2O3-only gates are 100-1000x noisier (Cho EDL 2009); N_sat = 2/3 Cox W L Vov / q.
- [dos-pixel-stack] RTN 1e-4 tail = 3 x q/(Cox W L) — basis: Si RTN amplitude distributions are roughly exponential with mean ~1-2x q/(Cox W L) [training knowledge, UNVERIFIED for IGZO].
- [dos-pixel-stack] Column comparator offset 1 mV after auto-zero; WL kickback 10% residual after dummy-WL cancellation — basis: standard auto-zero / dummy techniques in DRAM OCSA and CIS columns.
- [dos-pixel-stack] Neighbour coupling Cc/C_BL = 0.08 per aggressor, 2 aggressors; decision feedback leaves 15% — basis: BL shield (Samsung VS-DRAM); DFB residual limited by Cc variation (~10%) plus wrong neighbour decisions.
- [dos-pixel-stack] Cs sigma 6% (recess-length variation), C_BL sigma 3% — basis: Lam comment that recess varies along the stack (A1 sec.6); short recess should be tighter than the 600 nm case.
- [dos-pixel-stack] Guard band 8 mV for reference error, WL-WL disturb and temperature drift between samples — basis: judgment.
- [dos-pixel-stack] Oxide access TFT Ioff median 1 aA at 85 C; Vt sigma 30 mV; SS 80 mV/dec; capacitor J 1e-7 A/cm2 at 0.5 V — basis: Kioxia <1 aA (temperature unstated), CXMT SS, A1 dielectric target.
- [dos-pixel-stack] Costs: base wafer $3,000, $25 per cell tier, $250 per 16-tier deck, $300 per amp sub-layer, $2,000 per Smart-Cut layer; tier yield 0.998, amp tier 0.995 — basis: A1 sec.6 scenarios and Stage 2 critic ranges; low confidence.
- [dos-pixel-stack] Sharing factor 2 (two vertical BLs per SF via transfer gates) as the design point — basis: share 4 needs the same 2 amp sub-layers but doubles tRC to ~106 ns.
- [dos-pixel-stack] Depletion-mode (In-rich) oxide SF so the column sits above ground with the BL at VARY/2; amp supply 1.2 V; pulsed column bias — basis: oxide Vt is composition-tunable (imec In-poor vs standard IGZO drift study); design judgment.
- [dos-pixel-stack] DOE NSRC user facilities (Argonne CNM, ORNL CNMS, LBNL Molecular Foundry, Sandia CINT) charge no user fee for non-proprietary, publishable work and full cost recovery for proprietary work — basis: training knowledge [UNVERIFIED].
- [dos-pixel-stack] Stanford SNF, Purdue Birck and Georgia Tech IEN industrial rates not found; planning rate $110-150/h door + tool fees — basis: Notre Dame $124/h external, Penn $70/h industry door, TAMU $150/h industry (2025-26 schedules via search snippets).
