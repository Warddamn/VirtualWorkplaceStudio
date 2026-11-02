# B5: First principles and wild cards. Notes, reasoning and rejected ideas

**Agent:** `B5-firstprinciples` · **Phase:** B (divergent ideation), lens 5 · **Written:** 2026-11-01

**Files**
- Cards: `research/phaseB/B5-firstprinciples.json` (18 cards).
- Model: `research/models/B5_firstprinciples_estimates.py` (stdlib only; imports the A1 model; `python3` exits 0). Every number below is printed there.
- Sources: `research/sources/B5-firstprinciples.jsonl` (60 entries).
- Assumptions: `research/assumptions/B5-firstprinciples.md`.

**Evidence grade**
- All 15 of my WebSearch calls were used, with no WebFetch. Every web fact comes from a search snippet.
- Claims with no URL found are tagged `[UNVERIFIED-PK]`.
- My arithmetic is `[ESTIMATE]`.
- Framing per MISSION.md: physics only, no business kills, and every kill names a revival condition.

**Inputs read first**
- Phase A maps A1, A2 and A3.
- Phase B cards B1, B2 and B4, so as not to duplicate them.
- ram-venture device cards A1-A3.

---

## 1. The first-principles ledger: what it takes to hold a bit for ~1 s (model B5-00)

| Requirement | Number | Consequence |
|---|---|---|
| Barrier for one bit, 1 s | 21 kT (attempt time 1 ns) to 30 kT (0.1 ps) = 0.77 eV at 300 K | Any two-state system with a ~0.8 eV barrier holds one bit for a second |
| Barrier for a 16Gb die, 1 s, at most one flip | 44-54 kT = 1.38 eV (300 K), 1.65 eV (85 C) | Array size multiplies the requirement by ln(1.7e10) = 23.6 kT |
| Same, with ECC cleaning a raw BER of 1e-6 | 35-44 kT = 1.13 / 1.35 eV | ECC is worth ~10 kT of barrier |
| Non-volatile (10 years, whole die) | 64-73 kT = 1.9 / 2.25 eV | DRAM needs ~20-30 kT less barrier than flash or MRAM, and that slack can buy speed, voltage and endurance |
| Energy stored on today's 1-beta bit | 3.0e-15 J = 7.2e5 kT | DRAM holds charge **kinetically** (slow leakage), not thermodynamically. It spends ~10^4x more energy per bit than the barrier needs |
| Refresh energy against Landauer | 45.9 fJ against 2.9e-21 J: **1.6e7x** | Refresh energy is engineering, not physics |
| Holding power | 0.72 pW/bit at 64 ms; 46 fW/bit at 1 s retention | Retention >= 1 s makes refresh power negligible |
| Charge needed to sense | Image-sensor jots read **0.22 electrons rms** at room temperature | ~17,700 electrons per bit is not a noise floor; it exists to beat bitline capacitance and leakage |
| Area floor | 4F2 per wired layer (718 nm2 at F = 13.4 nm) | Below 4F2 per layer, density can only come from **shift addressing** (racetrack, CCD), **multi-level** or **tiers**. Wires, not storage elements, set density |

**Reading.** Physics leaves room for roughly 10^4x less stored energy, roughly 10^3x less charge and roughly 10^7x less refresh energy. The ledger also says *what kind* of storage can use that room:
- something with a ~1-1.5 eV (or ~45-65 kT mechanical or magnetic) barrier, and
- a write path that switches that barrier off **without wearing anything out**.

That second requirement turned out to be the selective one (section 2).

---

## 2. Five cross-cutting rules this lens produced (for Phase C triage)

1. **Crystalline-barrier rule (charge fluence).** A capacitor-type cell whose write current crosses an insulator passes Cs·V per write through ~F2. For 0.93 fC through (20 nm)^2 that is 2.3e-4 C/cm2 per write.
   - Amorphous dielectrics break down at Q_BD ~1-100 C/cm2, which allows only **4e3-4e5 writes**.
   - DRAM-class endurance (1e15) needs Q_BD >= 2.3e11 C/cm2.
   - Only crystalline barriers can plausibly meet that. Epitaxial resonant-tunnel-diode-class barriers carry ~1e5 A/cm2 for years [UNVERIFIED-PK: the premise most worth checking].
   - So every tunnel-write DRAM idea (crested barriers, ULTRARAM, QD-Flash, 2D floating gates) must use epitaxial or van der Waals barriers, or route the write current through a semiconductor channel (transistors, CCD/jot transfer gates) or a mechanical contact. (B5-05, B5-06, B5-03.)
2. **Wire rule.** Density beyond 4F2 per layer cannot come from a better storage element, because addressing wires set the area. The only levers are shift registers (B5-02, B5-12, B1-08), levels per cell (B5-03, B5-04) and tiers or decks (B5-01, B5-05, B5-07). This is why the racetrack-in-a-hole card is the only one here claiming >5x density.
3. **Arrhenius-gating rule.** Heat cannot be the write gate for a single thermally activated barrier.
   - Holding 1 s needs 0.77 eV, and writing over that barrier in 1 ns needs **~975 K**.
   - Holding 1e6 s needs 1.13 eV and **~1,425 K** for the write.
   - The gate must change the barrier itself: by field (transistor, resonant tunnelling), mechanics (a relay or snap-through) or magnetic torque. PCM's endurance problem is this rule in action.
4. **Cryogenic memory gap.** The best superconducting memory array is **2.6 Mb/cm2 = 2.6e-5 Gb/mm2, 1/17,000 of DDR5**. At 77 K, cooling costs 9.7-19.3 W per W, so cold memory loses for warm compute: 7.6-15 pJ/bit at the wall against 5.9 pJ warm. Cold memory wins only when compute is already cold. Then the right designs are:
   - oxide multi-level gain cells at 77 K (B5-14);
   - quantum-dot charge cells at 4 K (B5-17, ~2,000-4,000x denser than superconducting arrays);
   - superconducting and CDW cells only as fast caches (B5-15, B5-16).
5. **Charge-free storage is the only cure for row hammer and refresh at the same time.** Mechanical bits (B5-01, B5-07 hold) and magnetic bits (B5-02, B5-12, B5-13) have no charge for a toggling neighbour to disturb and no leakage tail. They trade leakage for an **unmeasured 1e15-cycle reliability question at nm scale**: ribbon fatigue and stiction, domain-wall shift errors under current densities 10-100x beyond electromigration rules. That is the lens's biggest open physics question.

---

## 3. Card summary

| ID | Card | Axis and claimed factor | Novelty | Biggest physics doubt |
|---|---|---|---|---|
| B5-01 | Click-RAM: snap-through 2D ribbon as a mechanical floating gate | Refresh 0, ~2-4 aJ writes, sub-ns; density parity at 2 tiers | NEW combination | Pull-in/stiction; strain uniformity; fatigue at 1e15 |
| B5-02 | Capacitor-hole racetrack (electroplated domain-wall wires) | **~10-25x bits per footprint**, no refresh | TWIST, close to NEW | Shift J 1e11-1e12 A/m2 against EM; shift errors |
| B5-03 | Deep-level charge bit (QD-Flash to single defect) | [SPEC] 2.7-5x density, ~3.5 aJ | TWIST / [SPECULATIVE] | Slow erase; trap variability |
| B5-04 | Jot-RAM: pinned well + CDS, 4 b/cell | 4 b/cell, capacitor-free, refresh relief when cool | NEW combination | Dark current at 85 C; vertical pinned-well scaling |
| B5-05 | Crystalline crested-barrier 1S1C crosspoint | 1.3-2.7x density, no transistor | TWIST | Charge-fluence wear unless crystalline; 5-10 V writes |
| B5-06 | Seconds-ULTRARAM | Refresh ÷1e3-1e6, ~1e-17 J writes | TWIST | III-V on Si; endurance past 1e7 unmeasured |
| B5-07 | Self-timed NEMS-selector crosspoint | 6-58 s retention, 1.3-2.7x density | TWIST | Contact endurance; threshold spread |
| B5-08 | Adiabatic refresh with stepwise or piezo-MEMS recovery | 2.4-3.2x lower refresh energy | TWIST | Sense-amp regeneration not recoverable |
| B5-09 | Negative-capacitance bitline | Capacitor 1.3 um to ~0.26 um | TWIST | Stability and noise gain 3.3x |
| B5-10 | Myelinated bitline (vacuum sheath + 2T nodes) | Cs to 0.6-0.8 fF | TWIST (bio framing) | Node offset against segment signal |
| B5-11 | DNA-brick nanotrench patterning | Replaces 5-7 EUV layers ($825-1,155/wafer) | TWIST | 95% yield against 99.99+% needed; salts |
| B5-12 | Voltage-clocked skyrmion shift register | Refresh 0, ~47 aJ/gate; density 1.34x worse | TWIST / [SPEC] | VCMA gives only 5 kT per step |
| B5-13 | Altermagnetic tunnel-junction RAM | 2.8x denser than FM-MTJ crosspoint, ~1.2x 1-beta | [SPECULATIVE] | TMR tiny; RuO2 contested |
| B5-14 | 77 K oxide multi-level gain-cell stage | x0.13 array energy, refresh ÷1e5 | TWIST | Needs cold compute to exist |
| B5-15 | Superconducting kinetic-inductance memory + FDM readout | ~1e-20-1e-17 J/op; density 1/90-1/17,000 | KNOWN + twist | Density |
| B5-16 | 1T-TaS2 CDW cryomemory | ~24 aJ, ~2 ps | KNOWN | Mechanism disputed; cryo only |
| B5-17 | Quantum-dot charge RAM at 4 K | 0.05-0.1 Gb/mm2 cold (2,000-4,000x superconducting) | NEW combination | Gate variability; read speed |
| B5-18 | TSV-free inductive stacking | No TSV, -26% area (4-high only) | KNOWN | Coupling reach: fails for 16-high |

**Most exciting three**, by physics headroom times the cheapness of a decisive demo:
1. **B5-02, capacitor-hole racetrack.** It turns DRAM's own worst process step (the 60:1 capacitor hole) into a z-axis shift register. A 1.3 um hole holds ~10 data bits and a 3 um hole ~25. It is the only idea in this lens that claims an order-of-magnitude density gain without lithography.
2. **B5-01, Click-RAM.** An 80 kT elastic barrier, a 5-15 GHz mechanical response, ~2-4 aJ writes, zero refresh and immunity to row hammer. The physics is clean, and the risk is pure engineering (stiction, uniformity).
3. **B5-09, negative-capacitance bitline.** It cuts the capacitor ~5x (1.3 um to ~260 nm) without changing the array, provable on a ~$200k MPW. It attacks A1's master bottleneck most directly of any card here.

Wild card worth a Phase C look: **B5-17.** If superconducting AI happens, the 4 K memory gap is 17,000x, and spin-qubit fabs already build the right structure.

---

## 4. Rejected ideas: why each died, and what would revive it

| # | Idea | Kill (physics, with numbers) | Revival condition |
|---|---|---|---|
| R1 | Acoustic delay-line RAM (GHz SAW/BAW recirculating loop) | Bit length = v/rate = 0.5 um at 10 Gb/s, so a 1 um-wide line holds 2 Mb/mm2 = **1/224 of DDR5**; 200 ns loop latency; per-pass amplification energy | Low-loss THz phonons with ~nm wavelength (not available). *Revived instead as B5-08: the piezo resonator as an energy-recovery inductor* |
| R2 | Optical bistable nanocavity RAM (photonic-crystal cavities) | Diffraction-limited cavity ~0.05 um2, so 20 Mb/mm2 (**1/22 of DDR5** before waveguides); holding power ~30 nW/bit, i.e. **~30 W per Gb** [holding power UNVERIFIED-PK] | Plasmonic or 2D-material cavities under 0.005 um2 with under 10 pW holding power |
| R3 | Frequency-multiplexed NEMS resonator bits (parametric oscillators) | Static drive power E·w/Q = **6.3 pW/bit** at Q = 1e4, against DRAM refresh at 0.72 pW/bit; um-scale footprint | Q >= 1e6 at GHz in ~100 nm resonators |
| R4 | Thermally gated write ('heat as the gate') | A single Arrhenius barrier needs **975-1,425 K** for ns writes over a 1 s to 1e6 s barrier; PCM-class damage | A barrier gated by field or mechanics, not temperature |
| R5 | Quantum-paraelectric SrTiO3 planar capacitor (cryo, k ~2e4) | Looks great unbiased (14 fF planar at 20 nm), but 1 V across 20 nm is 500 kV/cm and STO's k collapses at tens of kV/cm; at 100 nm and k ~2,000 it is only 0.28 fF | Thin films that keep k > 5,000 above 100 kV/cm (not seen) |
| R6 | Via-threaded nanoring '3D core memory' | Oersted field at r = 25 nm is **8 Oe per 100 uA** (80 Oe at 1 mA), so writes need mA; induction read is **0.13 uV** | Spin-orbit-efficient ring writes plus sidewall MTJs by ALD (2040 tools) |
| R7 | Nanofluidic 'ion-channel' memristor | An aqueous ion drifts 10 nm in 2 ns but diffuses back in **77 ns** without a binding barrier; with one, it hits the voltage-time dilemma; liquids in a chip | A solid-state analogue, which is ECRAM/protonics (B1-16, B2-05) |
| R8 | 'Ballistic' or superconducting bitlines to cut Cbl | Bitline capacitance (~0.15-0.2 fF/um) is geometric; conductivity cannot lower it | None: use vacuum (B5-10) or active cancellation (B5-09) |
| R9 | Rotaxane molecular crossbar (Caltech/UCLA 2007 class, ~1e11 bits/cm2) | Endurance and retention far below DRAM-class (organic redox switches, ~tens to ~1e6 cycles [UNVERIFIED-PK]) | Molecular switches with >= 1e12 cycles |
| R10 | DNA as the storage medium | Writes by synthesis take minutes to hours; archival only | None for working memory. *DNA survives as a fab tool (B5-11)* |
| R11 | ECRAM / electrochemical cells as DRAM | Faradaic insertion at 1e15 cycles is implausible (battery-class chemistry); covered by B1-16 and B2-05 | Non-faradaic (double-layer) ion positioning (B2-05) |
| R12 | Wide-bandgap SiC/GaN junction DRAM (1990s SiC lineage [UNVERIFIED-PK]) | Retention is excellent but density and process are poor; IGZO already reaches aA at BEOL temperatures | None needed: oxide channels dominate |
| R13 | Wavelength-addressed 3D tiers (light pipes as wordlines) | A light pipe needs >= lambda/2n ~150-250 nm diameter, so it cannot fit DRAM pitches; IGZO persistent photoconductivity is slow | Sub-wavelength plasmonic delivery with low loss (not available) |
| R14 | Photon-sustained latch (photodiode-loaded SRAM) | 4T + 2 photodiode area; stray light; beaten by IGZO gain cells on every axis | None |
| R15 | 'Thermal-ratchet' self-refresh from ambient heat | Violates the second law: each refresh erases information, costing at least kT ln2 from a powered source | None (physics) |
| R16 | Magnetic bubble memory with an on-chip rotating field | Field energy B^2/2mu0 over the chip at ~100 MHz gives watts per chip | Voltage clocks instead, which became B5-12 |
| R17 | Backside deep-trench eDRAM in backside-power-delivery logic wafers | Si is thinned below 1 um, leaving no room for deep trenches | Trenches in the bonded carrier wafer |
| R18 | Spin-crossover, photochromic or azobenzene molecular switches | ms-s switching; limited cycles | None for DRAM-class |
| R19 | Mild-cold (0-10 C) capacitor-less DRAM | ~170x retention gain over 85 C, but DFM claims >10 s at 85 C already (A3); covered by B4-13 thermal arbitrage | If floating-body tails stay short at 85 C |
| R20 | 2D magnets (CrI3) and Li@C60 'ion in a cage' switches | Cryogenic Tc / barrier too low at room temperature; air-sensitive | Room-temperature 2D magnets with electrical switching |
| R21 | Bio ion-channel steep-slope gating (cooperative gating charge) | The physics maps onto negative-capacitance FETs and NEMS, already covered by B1-02 and B1-18 | No separate card |
| R22 | SNAP superlattice edge patterning | Patterned region limited to ~um stripes; covered by B2's patterning family | Stitching at wafer scale |

---

## 5. Overlaps and hand-offs

- **B1 (cell physics)**
  - B5-07 extends B1-18 (NEMS access switch) to a two-terminal self-timed selector.
  - B5-12 differs from B1-08 (oxide CCD) by shifting magnetic, non-volatile bits.
  - B5-06's relaxed retention parallels B1-14's relaxed-retention VCMA logic.
  - B5-09 attacks the same Cs/Cbl ratio as B1-04, with active cancellation instead of charge transfer.
- **B2 (materials)**
  - B5-11 sits next to B2-11 (DSA) and B2-15 (defect budget).
  - B5-10's node idea pairs with B2-08 (complementary-oxide sense amps).
- **B4 (architecture)**
  - B5-08 complements B4-02 and B4-03 (refresh policy): B4 refreshes less often, B5-08 makes each refresh cheaper.
  - B5-18 complements B4-15 (interconnect).
- **Phase C should test first:**
  - the crystalline-barrier premise (Q_BD of epitaxial and hBN barriers under pulsed fluence);
  - racetrack shift-error rate against current density in cylindrical wires;
  - ribbon pull-in and stiction margins under charge drive.

## 6. What I could not verify

- The original source of the 600 m/s cylindrical-wire domain-wall velocity (cited secondhand in Bran et al. 2023).
- Which paper holds QD-Flash's 4-day storage record.
- ULTRARAM endurance beyond 1e7 cycles, and any 2024-26 array data.
- Vaire's recovery figures (50% against 177x; unreconciled).
- The 1T-TaS2 switching mechanism (thermal or non-thermal: sources disagree).
- Electrophysiology capacitance-neutralisation practice, axon node spacing, CIS dark-current doubling per ~7 C and full-well density, the Cu EM limit, RTD current-density lifetimes, the 1990s single-electron-memory lineage, and DNA cost per gram. All are `[UNVERIFIED-PK]` in the assumptions file.
