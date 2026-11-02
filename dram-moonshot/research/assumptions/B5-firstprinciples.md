# Assumptions log: B5-firstprinciples (Phase B, lens 5: first principles and wild cards)

Written 2026-11-01. Numbers live in `research/models/B5_firstprinciples_estimates.py` (`python3` exits 0). One bullet per assumption or judgment call.

## Anchors reused (not re-derived)
- [B5-firstprinciples] 1-beta cell area is 1,070 nm2 (6F2 at F = 13.4 nm), array efficiency is 0.51, and density is 0.447 Gb/mm2. Basis: A1_scaling_limits.md section 1.
- [B5-firstprinciples] Cs = 5.4 fF, Cbl = 34.7 fF at 512 cells per bitline, 50 mV minimum sense signal, VARY 1.05 V, VWL 2.9 V. Basis: A1 `models/dram_cell_physics.py` INPUTS.
- [B5-firstprinciples] Refresh energy is 45.9 fJ per bit-refresh = 2 x (BL 20.1 + WL 2.8 fJ). Basis: A1 `refresh_energy_per_bit_fJ()`.
- [B5-firstprinciples] Random DDR5 activation costs 5.9 pJ per useful bit. Basis: A1 key findings.
- [B5-firstprinciples] The 77 K cooling penalty is 9.7-19.3 W at the wall per W removed. Basis: A3 model section 6.
- [B5-firstprinciples] EUV costs ~$165 per exposure, i.e. $825-1,155 per wafer for 5-7 layers. Basis: A1 key findings.
- [B5-firstprinciples] Usable area is 60,334 mm2 per 300 mm wafer; the DRAM fleet is 22.2M wafers/yr. Basis: ram-venture device model; A2.

## Thermodynamic floor (B5-00)
- [B5-firstprinciples] The barrier criterion is E/kT = ln(N*t/(tau0*p_fail)), with tau0 = 1 ns (magnetic and mechanical attempt rates) or 0.1 ps (atomic and phonon). Basis: Neel-Brown/Arrhenius; it matches B1-14's convention.
- [B5-firstprinciples] Landauer energy is kT ln2 at 300 K. Today's refresh is ~1.6e7x above it. Basis: arithmetic.

## B5-01 Click-RAM
- [B5-firstprinciples] Graphene E2D = 340 N/m and areal mass 7.6e-7 kg/m2; monolayer MoS2 E2D ~180 N/m and 3.1e-6 kg/m2; 2 nm ALD Al2O3 E ~170 GPa. Basis: textbook values [UNVERIFIED].
- [B5-firstprinciples] Buckled-ribbon barrier dU = E*A*pi^4*q^4/(32*L^3), derived for the first clamped-clamped mode (1 - cos) with uniform axial strain; effective mass is (3/8) of the ribbon mass; snap force is 1.54*dU/q (maximum slope of a quartic double well). Basis: my derivation [ESTIMATE].
- [B5-firstprinciples] Electrode overlap factor 0.5 (mode shape); the gap at the 'up' state is g0 + q. Basis: [ESTIMATE].
- [B5-firstprinciples] Read uses 1 nm EOT under the cavity and a 75 mV/decade oxide channel. Basis: [ESTIMATE] typical IGZO.
- [B5-firstprinciples] Cell footprints are 140x40, 90x40 and 90x25 nm (ribbon plus anchors at pitch). Basis: [ESTIMATE].
- [B5-firstprinciples] Fatigue reference: a 5 MHz MEMS oscillator runs 1.6e15 cycles in 10 years. Basis: arithmetic; that single-crystal MEMS resonators survive this is [UNVERIFIED-PK].

## B5-02 Capacitor-hole racetrack
- [B5-firstprinciples] Bit length = 3 wire diameters (domain + wall + dipolar guard); half the track is shift buffer. Basis: [ESTIMATE] from racetrack design practice.
- [B5-firstprinciples] Domain-wall velocity is 100 / 200 / 300 m/s at J = 1e11 / 3e11 / 1e12 A/m2. Basis: [ESTIMATE], discounted from the ~300 m/s current-driven simulation (APL Materials 2022, via snippet).
- [B5-firstprinciples] Nanowire resistivity is 2e-7 ohm.m; MTJ RA is 5 ohm.um2. Basis: [ESTIMATE].
- [B5-firstprinciples] The Cu electromigration DC design rule is ~1e10 A/m2 (1e6 A/cm2). Basis: [UNVERIFIED-PK].
- [B5-firstprinciples] World cobalt mine supply is ~2e5 t/yr. Basis: [UNVERIFIED-PK]; only used to show that the fleet's 2.3 t/yr is negligible.

## B5-03 Deep-level bit
- [B5-firstprinciples] Capture cross-section 1e-15 cm2, thermal velocity 1e7 cm/s, effective density of states 1e19 cm-3, so the emission prefactor is 1e-11 s. Basis: [ESTIMATE], typical deep-level values.
- [B5-firstprinciples] A dielectric constant of 11 is used for Poole-Frenkel lowering. Basis: [ESTIMATE], III-V/GaP class.
- [B5-firstprinciples] That 1990s room-temperature single-electron memories existed (Hitachi; Chou) is [UNVERIFIED-PK]; no URL was found this session.

## B5-04 Jot-RAM
- [B5-firstprinciples] Dark current doubles every ~7 C, and the 6-sigma tail is 100x the median (hot pixels). Basis: [ESTIMATE] from image-sensor practice [UNVERIFIED-PK].
- [B5-firstprinciples] Pinned-well full-well density is ~6,000 electrons/um2 of junction area. Basis: [UNVERIFIED-PK], CIS pinned-photodiode class.
- [B5-firstprinciples] Read noise scales as sqrt(bandwidth) from 0.22 electrons rms; DRAM bandwidth is taken as 50-500x the QIS readout bandwidth. Basis: [ESTIMATE].
- [B5-firstprinciples] Cell area is 4,000-5,000 nm2 plus 1/8 of a 2,000 nm2 shared readout. Basis: [ESTIMATE].
- [B5-firstprinciples] onsemi Nampa, Idaho is CIS-capable. Basis: [UNVERIFIED-PK].

## B5-05 / B5-06 Barrier-based cells
- [B5-firstprinciples] Q_BD is 1-100 C/cm2 for amorphous gate dielectrics. Basis: [UNVERIFIED-PK] (SiO2 charge-to-breakdown literature).
- [B5-firstprinciples] Crystalline resonant-tunnel-diode barriers carry ~1e5 A/cm2 for 10 years (~3e13 C/cm2) without wear-out. Basis: [UNVERIFIED-PK]; this is the key premise of the 'crystalline-barrier rule' and should be checked first in Phase C.
- [B5-firstprinciples] Floating-gate coupling Cox is 3.45e-2 F/m2 (EOT ~1 nm). Basis: [ESTIMATE].
- [B5-firstprinciples] Judgment: a DRAM-class cell needs ~1e15 write cycles over its life. Basis: MISSION 'effectively unlimited endurance'; A3 uses 1e15.

## B5-07 NEMS selector
- [B5-firstprinciples] Beam stiffness 1 N/m, gap 5 nm, area 2e-15 m2, coated contact gap 1 nm, no adhesion in the release estimate; effective mass 3e-21 kg. Basis: [ESTIMATE].
- [B5-firstprinciples] Hold leakage of 8.6-86 aA through the capacitor dielectric. Basis: B1-18 card numbers (cross-reference).

## B5-08 Adiabatic refresh
- [B5-firstprinciples] Refresh-only periphery multiplier is 1.3 (no column or I/O path), against A1's 2.0 for general access. Basis: [ESTIMATE].
- [B5-firstprinciples] Only the BL/WL CV^2 part is recoverable; the remaining 0.3 x core is treated as unrecoverable control energy. Basis: [ESTIMATE].
- [B5-firstprinciples] On-chip spiral inductor Q ~10 at 50-200 MHz; piezo-MEMS resonator Q ~1e3. Basis: [UNVERIFIED-PK].

## B5-09 / B5-10 Bitline capacitance
- [B5-firstprinciples] Cbl split: lateral bitline-bitline and bitline-contact 55%, bitline-wordline 25%, fixed 20%; today's effective lateral k is 2.5-4 (air spacers already partly in place). Basis: [ESTIMATE].
- [B5-firstprinciples] The neutralisation feedback capacitor is 24 fF at Cn/Cbl = 0.7; amplifier offset is 3-10 mV. Basis: [ESTIMATE].
- [B5-firstprinciples] Capacitance neutralisation is standard in electrophysiology amplifiers, and axon internodes are ~100x the fibre diameter. Basis: [UNVERIFIED-PK], no URL this session.

## B5-11 DNA patterning
- [B5-firstprinciples] The DNA layer is 20 nm thick at 1.7 g/cm3; cost is $200/g (bioreactor scaffold) to $1e4/g (synthetic oligos). Basis: [UNVERIFIED-PK].
- [B5-firstprinciples] Repair plus on-die ECC tolerates ~1e-4-1e-6 defects per feature. Basis: [ESTIMATE], consistent with B2-15's defect-budget framing.

## B5-12 / B5-13 Magnetic
- [B5-firstprinciples] VCMA coefficient 100 fJ/(V.m) (typical) and 1,000 (aspirational); 1 V across 1.5 nm MgO; skyrmion diameter 20 nm. Basis: [ESTIMATE].
- [B5-firstprinciples] A two-phase skyrmion track is 2F wide with a 4F bit length. Basis: [ESTIMATE], CCD analogy.
- [B5-firstprinciples] Ferromagnetic MTJ crosspoint pitch is ~2.5 d; altermagnet pitch is ~1.5 d. Basis: [ESTIMATE] (dipolar interaction versus no stray field).

## B5-14 to B5-17 Cryogenic
- [B5-firstprinciples] At 77 K, VARY is 0.4 V and VWL 1.0 V (Si subthreshold swing ~15-20 mV/decade). Basis: [ESTIMATE].
- [B5-firstprinciples] An oxide gain cell occupies 2.5x the 1T1C area. Basis: [ESTIMATE], consistent with A3 section 3.3.
- [B5-firstprinciples] NbN-class film: R_sq 500 ohm, Tc 10 K. Basis: [ESTIMATE].
- [B5-firstprinciples] The 4 K cooling penalty is 300-1,000 W/W, and ~500 W/W is used for point estimates. Basis: [ESTIMATE].
- [B5-firstprinciples] Quantum-dot cell is 70-100 nm with 0.5 array efficiency; gate capacitance 10 aF; SET sensing at 1 nA. Basis: [ESTIMATE].
- [B5-firstprinciples] That the 1T-TaS2 metastable state relaxes at elevated temperature is [UNVERIFIED-PK].

## B5-18 Inductive stacking
- [B5-firstprinciples] Coil diameter roughly equals the coupling distance (minimum 3x die thickness), at a coil pitch of 1.2 x diameter. Basis: [ESTIMATE], near-field coupling rule of thumb.

## Judgment calls
- [B5-firstprinciples] Kept cards whose density is worse than DRAM (B5-12, B5-15, B5-16) when they offer a step change on another MISSION axis (energy, volatility) or fill the cryogenic-memory gap, and labelled the density penalty in the step-change claim.
- [B5-firstprinciples] Did not duplicate B1 cards: the NEMS access switch (B1-18), protonic gain cell (B1-16), redox molecules (B1-17), oxide CCD (B1-08), relaxed-retention VCMA (B1-14) and nanogap floating node (B1-09). Cards that touch them (B5-07, B5-12) name the difference.
- [B5-firstprinciples] Electrochemical RAM (ECRAM) got no card: B1-16 and B2-05 cover it, and faradaic chemistry at 1e15 cycles is implausible (see notes).
- [B5-firstprinciples] The 15-search cap was fully used. Where a claim had no URL, it is tagged [UNVERIFIED-PK] rather than cited.
