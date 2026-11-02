# B1: New cell physics — reasoning notes, rankings and rejected ideas

**Agent:** `B1-cellphysics` · **Written:** 2026-11-01 · **Phase:** B (divergent ideation), lens "NEW CELL PHYSICS"

**Files**
- Cards: `research/phaseB/B1-cellphysics.json` (20 cards, validated with python3).
- Arithmetic: `research/models/B1_cellphysics_estimates.py`. It imports the helpers from A1's `models/dram_cell_physics.py` and `python3` exits 0.
- Sources: `research/sources/B1-cellphysics.jsonl` (62 entries). 43 come from my 15 searches and 19 are cross-references from the A1/A3 and ram-venture logs.
- Assumptions: `research/assumptions/B1-cellphysics.md`.

**Evidence grade.** I used 15 of 15 WebSearch calls and no WebFetch. Every web fact is from a search snippet. Physics numbers are my own arithmetic in the model and are tagged [ESTIMATE] in spirit. Ideas are judged on physics only (MISSION.md): nothing is killed for business reasons, and every kill names its revival condition.

---

## 1. How I aimed the lens

Phase A says the bit is "passive charge on a capacitor, read through a long bitline, behind a leaky Si switch" (A1 §10). That one cause gates bottlenecks #1, #3, #4 and #10. The design question for every card was which of three levers it pulls:

| Lever | What it changes | Cards |
|---|---|---|
| **More charge per µm² of wall** | Same sensing, shorter capacitor | B1-01 AFE reservoir, B1-02 NC stub, B1-17 redox molecules |
| **Less charge needed** | Better sensing or gain, so the capacitor shrinks or disappears | B1-03 gated-diode strip, B1-04 charge-transfer pre-sense, B1-05 MLC (uses the margin), B1-19 Mott local sense |
| **A different state variable** | No charge-sharing read at all | Gain-read charge: B1-06 SFG, B1-09 nanogap, B1-10 charge-trap, B1-20 2D barrier. Polarization: B1-11, B1-12, B1-13. Spin: B1-14, B1-15. Ions: B1-16. Latch: B1-07. Mechanics: B1-18. Shift register: B1-08 |

The unit I used throughout: today's capacitor wall delivers **3.3 µC/cm² of signal charge**, and the 1β cell holds 2.84 fC (≈17,700 e⁻) of signal [A1]. Any "more charge" idea is scored as a multiple of 3.3 µC/cm². Any "less charge" idea is scored by the minimum Cs it tolerates on a real bitline.

## 2. My ranking (physics plausibility × size of step × provability on $1M)

| Rank | Card | Step-change claim | Why here | Main physics doubt |
|---|---|---|---|---|
| 1 | **B1-04** Charge-transfer pre-sense + IGZO cell | Cs 5.4 → 0.5 fF (pillar 1,300 → 120 nm) on a 512-cell bitline; signal 155 mV vs 7.5 mV | Known circuit physics. The only new part is pairing it with oxide retention (75 s at 0.5 fF). Provable on one MPW chip | τ = Cbl/gm ≈ 14 ns transfer, plus cancellation of bias-current mismatch |
| 2 | **B1-03** IGZO gated-diode strip (3D tier without a capacitor module) | 3D break-even 26 → 9–14 tiers; ~5 fJ per access | Deletes the hardest 3D DRAM module (lateral TiN/high-k/TiN fill). Same IGZO strip and word-plane process as Kioxia's horizontal tiers | Only 60–80 mV fresh signal on a 64-cell local bitline; trap-limited charge transfer |
| 3 | **B1-01** AFE-reservoir ZrO2 stub | 3–6× charge per wall area, capacitor 210–420 nm, Hf-free | Uses the dielectric DRAM already deposits. The twist (low precharge, plateau reservoir) is testable on MIM capacitors in months | AFE endurance ~1e9–1e10 vs 1e12–1e15 needed |
| 4 | **B1-08** Vertical oxide CCD string | 4.2–8.3× 1β density, no per-bit device, one HAR etch | The largest density step of any card, built entirely by deposition | CTE ≥ 0.9999 in an oxide semiconductor; serial access of 32–128 ns |
| 5 | **B1-09** Nanogap floating node | Non-volatile gain cell: ns writes at 6–8 V, retention 1e4 to >1e8 s, no oxide wear | Most original. FN arithmetic works even with plain TiN | Ångström gap control and emission stability over 1e12 cycles |
| 6 | B1-10 Direct-tunnel charge-trap 3D AND | 2.7–7.2× density with NAND tools; refresh 16–1,562× lower | Process exists. Endurance is the whole bet | Thin-oxide wear-out at 1e10+ cycles |
| 7 | B1-06 Vertical oxide SFG 1T1D | b×N for parity 3.7 → 1.5 (F = 20 nm), 14.9 → 6 (F = 40 nm) | Halves tiers or levels needed vs 2T0C | Needs ≥1.0–1.1 eV diode barrier; half-select disturb |
| 8 | B1-05 2-bit 1T1C on IGZO | 1.8–2.8× density, no new litho | Simple, but needs B1-04 or short bitlines | 55 mV level steps vs Vt drift |
| 9 | B1-11 Capacitive-NDRO FE tier | Refresh and restore → 0 for read-mostly data | Real data (read >1e11) and a natural AI workload fit | Imprint drift; n ≤ 4 caps per node |
| 10 | B1-18 NEMS relay access | Retention 10–100 s with today's capacitor; WL energy ×0.06; hammer-immune | Clean physics | Contact endurance unmeasured |
| 11–20 | B1-02, B1-14, B1-12, B1-07, B1-20, B1-17, B1-15, B1-16, B1-13, B1-19 | See cards | Each has a single dominant unknown (detailed in its card) | — |

**Synergies worth testing together.** B1-04 multiplies B1-01, B1-03 and B1-05. Charge-transfer sensing on a gated-diode strip turns 60–80 mV into >150 mV. The same sensing on an AFE stub, or on a two-bit 1T1C, recovers the level margin. B1-03 and B1-08 share the physics question (complete charge transfer in IGZO), so one CTE test structure informs both.

## 3. Biggest physics doubts across the lens

1. **Charge-packet transfer in oxide semiconductors** (B1-03, B1-08, partly B1-04). At Dit 1e11–1e12 cm⁻²eV⁻¹ there are 6–57 trap states per eV under one gate, against packets of 1,000–8,000 electrons. A CCD needs CTE ≥ 0.9999 per transfer. No published CTE or trap-dynamics data for IGZO/IGO charge transfer turned up. This is a cheap measurement that unblocks three cards.
2. **Endurance of any switched order parameter** (AFE, FE, sliding FE, protons, trapped charge, DW). The reported range is 1e6–1e11, against 1e12–1e15 for DRAM duty. Only sliding ferroelectrics claim fatigue-free physics, and only SOT-MRAM has shown >1e15.
3. **Soft errors at 1,000–2,000 signal electrons** (B1-04, B1-03). BEOL oxide cells have no Si collection funnel. That should help, but no data exists.

## 4. Rejected or folded ideas, each with its revival condition

| Idea | Verdict | Physics reason | Revival condition |
|---|---|---|---|
| **Mott (VO2/NbO2) threshold selector as the storage-node isolator (1S1C crosspoint DRAM)** | Kill | Insulating-state conductivity (σ ~0.1–1 S/cm for VO2) gives ~20 nA through a 20 nm element at 1 V; the storage node needs ≤1e-14 A. OTS selectors leak ~nA at half-bias. Retention would be ~µs | A two-terminal selector with ≤1 fA at half-select and ≥10 µA on (≥10 decades) at ≤1 V, at 85 °C |
| **VO2 thermal-hysteresis bit** (array held inside the 5–15 K hysteresis loop) | Kill | Writing "1" by Joule heating works. Writing "0" needs local cooling below the lower transition, and there is no local refrigerator. Ambient must also stay inside a ~10 K window | A non-thermal reverse (metal → insulator) switch, e.g. field-, strain- or charge-driven, or ≥40 K hysteresis centred at 85–100 °C with an electrical erase |
| **S-type NDR (NbO2) self-latching storage** | Kill | Holding the metallic state needs ~µA per cell, so 1e10 cells draw ~kW | A holding current ≤1 pA per cell |
| **Protonic nano-supercapacitor stub** (2-terminal, ~18× charge per area) | Converted into B1-16 | Ion hopping depends exponentially on field. If ions stay put at hold fields, they also cannot leave at low read fields in ns; extraction needs ~1 V/nm, the same as writing | A mixed conductor with fast low-field ion transport and no self-discharge. This is thermodynamically contradictory, so the revival is the gain-cell form (B1-16) |
| **Perovskite membrane (STO/BTO, k ~300) planar capacitor** | Kill at DRAM pitch | A planar 2 fF capacitor at k 300 and 10 nm needs ~7,400 nm², 7× a 1β cell. Conformal 3D perovskites lose k to dead layers | Conformal ALD STO/BST with k ≥ 150 at ≤10 nm, ≤450 °C and ≤1e-7 A/cm² (A1's k ≥ 100 wall) |
| **Image-sensor (pinned-diode) storage node** | Kill as a cell; sensing principle kept in B1-03/B1-04 | Full-well capacity scales with area, so a 30 nm pinned node holds only a few electrons. Si dark current at 85 °C is also too high | Large-pitch eDRAM only. The CDS and complete-transfer ideas survive in B1-03/B1-04 |
| **Single-electron / Coulomb-blockade memory** (Hitachi PLEDM lineage) | Kill | Room-temperature blockade needs <2–3 nm islands; island-size variability and background-charge noise exceed kT margins | Atomically identical islands (dopant or molecular) placed deterministically |
| **Parallel ferroelectric NC element to cancel bitline capacitance** | Kill (physics) | NC is stabilised only in series, where charge is shared. A voltage-driven parallel FE simply switches. An active negative-impedance converter is possible, but it is just an amplifier | Folded into B1-04 (charge-transfer gain) |
| **Ferroelectric hysteretic access transistor** (steep slope to cut WL swing) | Fold | Switching the FE on every access hits the same endurance wall as FeFETs. Hysteresis-free NC-FETs show limited SS gains | An NC-FET with stable sub-60 mV/dec over ≥9 decades at 85 °C |
| **Piezoelectronic transistor (SmSe/PMN-PT) as access device** | Kill | The SmSe insulating state is far too conductive for storage isolation | A piezoresistive channel with ≥1e14 on/off |
| **Negative-compressibility 2DEG (LAO/STO) capacitance boost** | Fold into B1-02 | Enhancement appears at low carrier density and mostly at low temperature [UNVERIFIED] | >2× enhancement at room temperature and DRAM charge densities |
| **Magnetoelectric antiferromagnet memory (Cr2O3, BiFeO3)** | Park | Spin-orbit readout signals are µV–mV; BFO switching speed and endurance are unproven at ns. No evidence was retrieved this session | ME switching ≤1 ns, ≥1e12 cycles, ≥100 mV readout |
| **Magnetic racetrack (vertical)** | Park, superseded by B1-08 | Same serial-access trade as a CCD but needs 3D magnetic stacks; vertical racetracks are undemonstrated | ≥1 km/s domain-wall motion in a vertical 3D track with a single read/write head |
| **Wide-bandgap (Ga2O3) "hot" gain cell for 150 °C** | Fold into B1-03/B1-06 | Retention in oxide cells is interface-limited (A3 §3.1), so bandgap is not the lever. Ga is also a chokepoint (A2) | Only if interface-limited leakage is shown to scale with bandgap |
| **Electret-biased access transistor** | Not a step change | It is work-function engineering by another name: ~0.2–0.3 V of WL relief | — |

## 5. What I could not verify

- ns-pulse endurance numbers for AFE ZrO2 at DRAM duty, LiNbO3 domain walls, protonic WO3 cells and sliding FE at 10 ns (only ms-pulse 1e6 for 3R-MoS2 and an unattributed 1e11 for bilayer BN).
- Arimoto's 1997 charge-transfer pre-sensing paper: seen only as a citation inside a patent snippet. NEC four-level DRAM (1997): training knowledge only.
- Schottky and MIS barrier heights achievable on IGZO/In2O3 (B1-06 needs ≥1.0–1.1 eV).
- Any CTE, trap-capture or charge-transfer data in oxide semiconductors (B1-03, B1-08).
- Row-hammer and soft-error behaviour of any of these cells (A3 white space 5 still stands).
- NbO2 threshold-voltage variability and endurance: no URL retrieved; B1-19 rests on reasoning only.
