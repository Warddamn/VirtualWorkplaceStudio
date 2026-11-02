# DIODE-TOWER: technical dossier

*Agent `dosw-diode-tower`, 2026-11-02. Model: `models/diode-tower.py` (re-run 2026-11-02, exit 0; output `research/stage3/diode-tower_model_output.md`). Notes: `research/stage3/diode-tower_notes.md`. Assumptions: `research/assumptions/dos-diode-tower.md`. Sources: `research/sources/dos-diode-tower.jsonl`, plus A2/A3 cross-references. Numbers come from the model unless a source is named. Tags: [ESTIMATE] is a modelled judgement, [SPECULATIVE] is plausible but unshown physics, and [UNVERIFIED] is unchecked training knowledge.*

---

## 0. Header

**Name.** DIODE-TOWER: one transistor and 16-64 linear-capacitor bits per pillar. Per-tier oxide Schottky diodes steer the bits, and a double-sampled gain FET reads them.

**One-line thesis.** A one-way oxide diode in every tier replaces ferroelectric coercivity as the selector in a 1T-nC stack. A plate pulse then dumps only the selected tier onto a shared pillar. Bits come from deposition and one hole etch, with no EUV, and charge crosses a semiconductor junction, never an insulator.

**Rank and category.** Rank 6 of 10 (EV = S 3 × P 3 × D 5 = 45). Category: cell/array. The model-backed notes argue P should be 2 (10-25%) for the linear version as specified.

**Constituent ideas and technique lineage.**

| Id | Contribution | Technique |
|---|---|---|
| I-10647 | Core cell: diode-steered capacitor tiers on one pillar | Wishful thinking / ideal final result |
| I-05218 | CDS cancels gain-FET offset and reset noise | First principles |
| I-00257 | Local gain FET per 16-cell segment, made in the same vertical step | SCAMPER-Substitute |
| I-11559 | ECC-paid margin: raw BER 1e-4 needs z ≥ 3.72 | Phase B lens (B4 architecture) |
| I-11148 | Erasure-flagging sense | Scarcity and constraint as engine |
| I-02355 | Antiferroelectric plateau dielectric (optional upgrade) | SCAMPER-Reverse/Rearrange |
| I-10664 | "Many bits, one read transistor" | Wishful thinking / ideal final result |
| I-03474 | Coaxial per-tier rings cut by a selective recess | Biomimicry (tree rings) |
| I-10833 | Reuse depreciated 3D-NAND hole/recess/ALD tools | Wishful thinking / ideal final result |
| I-00729 | Tier-orthogonal codewords absorb tier defects | SCAMPER-Combine |
| I-11544 | Vt-coded in-stack tier decoder | Phase B lens (B3 3D process) |

The merge took the FE persistent variant, the AFE upgrade path and the Ru caution from the device-lens DIODE-TOWER. It took the in-hole gain FET with CDS, the stricter image-force and forward-current spec, the Ru-free MoOx contact and the coupon-first gate from the system-lens Pillar DRAM.

**Verdicts.**
- **PHYSICALLY POSSIBLE? Yes, conditionally.** No law is violated. The tier diode needs a thick-film barrier of **≥1.07-1.12 eV with patch σ ≤ 0.05 eV in a 15 nm IGZO shell**. The best IGZO contact found is 0.92 eV; AgOx on crystal ZnO reaches 1.0-1.2 eV.
- **STEP CHANGE IF IT WORKS? Yes, on density and transistor count, at 32-64 tiers only.** Density is 1.9× 1-beta at 32 tiers, 3× at 50 and 3.9× at 64 (parity at 18). Transistors per bit fall 10-20×. Cost is 0.55-0.35× $/bit at tier yield 0.998. There is no energy step unless retention reaches 1 s.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.** Coupons costing ~$135k (plus a $90k reusable bench) settle the deciding diode numbers by month 7. A 4-8-tier stack fits in a $980k plan. Yield at 32-64 tiers and the in-hole gain FET's residual do not.

---

## 1. How it works (for a smart non-engineer)

A DRAM bit is a bucket of charge (a capacitor) behind a tap (a transistor). Today every bucket has its own tap. Each bucket is also a 60:1 capacitor skyscraper, because it must nudge a reading wire shared by ~500 others (A1 §2).

DIODE-TOWER etches one hole through a stack of metal "plate" floors. On each floor a small ring-shaped bucket wraps the hole. All the floors share one vertical metal core, the pillar, and only the pillar has a tap. Between each bucket and the pillar sits a **one-way valve**, an oxide Schottky diode.

- **Read floor k.** Set the pillar to a known level and let it float. Pulse floor k's plate up. That bucket rises above the pillar, its valve opens and its charge pours in. An amplifier at the top of the hole samples the pillar before and after, and the subtraction cancels the amplifier's own error.
- **Write floor k** (same pulse). Drive the pillar to the data level. The bucket drains to one valve-drop above it. When the plate drops, the bucket falls **below** any level the pillar can reach, so its valve stays shut (the plate-swing rule, §2.4).
- **The other floors.** Their plates don't move, so their valves stay reverse-biased. They lose only the diode's reverse leakage, and that leakage is the whole bet.

```
     write bitline                     read bitline (to CDS comparator)
          |                                   |
     [ACCESS FET]                      [GAIN FET]--[READ SELECT]
          |_____________  _______________|  (gate = pillar)
                        ||
   plate 32  ===|ZrO2|[node]>|IGZO|| <- metal pillar core: 1.0 fF at 32 tiers
     ...                        ||     [node] = 15 nm recessed ring, Cs 0.27 fF
   plate k   ===|ZrO2|[node]>|IGZO||     >|    = Schottky: node = anode, IGZO = cathode
     ...                        ||     ring diode area 2,639 nm2
   plate 1   ===|ZrO2|[node]>|IGZO||
   -------------------------------------------------------------
   CMOS under array: ~1.8-2 V plate drivers, tier decoder, CDS, ECC
```

Three transistors serve 30 user bits at 32 tiers, or 61 at 64.

---

## 2. The physics and the numbers

### 2.1 Cell and signal (60 nm hole, 15 nm shell, 85 °C)

- **Storage capacitor.** Cs = 2π·ε₀·40·14 nm / ln(50.5/45) = **0.270 fF** (coaxial ZrO₂, 5.5 nm, k = 40). That holds 843 e⁻ at 0.5 V, against ~17,700 e⁻ in a 1-beta cell.
- **Diode.** Ring area 2π·30·14 = **2,639 nm²**. The fully depleted shell loads the pillar by only 0.018 fF per unselected tier.
- **Pillar.** 0.72 / 1.00 / 1.57 fF at 16 / 32 / 64 tiers. The card assumed 1.5 fF.
- **Footprint.** Pitch is 60 + 2(15 + 5.5) + 20 = 121 nm. With a slit every 4 rows (+12.4%) the footprint is **0.0165 µm²**, 1.5× the card's 0.011.

Signal at 32 tiers = 0.27 × 0.5/(0.27 + 1.00) = **106 mV** fresh, or 85 mV after the 100 mV droop budget. kT/C is 1.97 mV, and the assumed post-CDS residual is 7 mV. Then z = (85/2)/7.33 = **5.8**. At 64 tiers the signal is 73/59 mV and z = 4.1. At 96 tiers z = 3.1, which fails.

**Corrections carried.** The card compared signal/σ (7-15) with BCH t = 8's 3.72, but 3.72 is a half-margin, so the right test is signal/(2σ). The lighter pillar wins some margin back: 106 mV, not 76 mV.

### 2.2 Versus 1-beta DDR5

User Gb/mm² = (1e6/0.0165) × (tiers − reference − spares) × 0.55 array efficiency / 1.156 ECC. Cost = ($3,000 + $25/tier) / (density × 0.998^tiers), relative to $3,800 / 0.447.

| Metric | 1-beta DDR5 | 32 tiers | 64 tiers |
|---|---|---|---|
| Density | 0.447 Gb/mm² | 0.867 (**1.94×**) | 1.763 (**3.94×**) |
| Transistors per user bit | 1 | 0.10 | 0.05 |
| Capacitor | ~60:1 pillar | 15 nm lateral ring (hole AR 27) | hole AR 53 |
| EUV layers | 0 (Micron 1β) | 0 | 0 |
| $/bit | 1.0 ($1.48/GB) | 0.55× ($0.81) | 0.35× ($0.52) |
| Energy per access | ~46 fJ | 28 fJ | — |
| Refresh power at 64 ms | 6.1 mW/GB | 4.1 mW/GB | — |
| Endurance | unlimited | 1e12 pulses needed, unmeasured | — |

Parity comes at **18 tiers** and 3× at **50**. That is harsher than the critics' "2-4× at 16-32 tiers" at the low end: the recess ring forces a 121 nm pitch. It matches their "≥48 tiers for 3×". **The step change is a 32-64-tier claim.** Energy per access improves 1.6×, which is no step, because bitline wiring dominates. Refresh energy falls 16× only if 1 s retention (G2) holds.

### 2.3 The diode

**Budget.** I ≤ Cs·ΔV/t = 0.27 fF × 0.1 V / 64 ms = **422 aA** per tier, or **27 aA** for 1 s.

**Thermionic leakage.** I = Aj·A*·T²·exp(−φ/kT), with A* = 40.9 A/cm²K². The prefactor is 2.64e-11 cm² × 40.9 × 358² = 1.38e-4 A, and kT = 30.9 meV. 422 aA needs φ_eff ≥ 0.0309 × ln(1.38e-4/4.22e-16) = **0.818 eV**; 27 aA needs 0.903 eV. At 1.00 eV the current is 1.2 aA (23 s).

**Inhomogeneity tail.** A 40,000-diode Monte Carlo models each ring as ~12 Gaussian barrier patches (Werner–Güttler/Tung). At σ = 0.05 eV the 1e-4 tail tier leaks **94×** the mean, a penalty of kT·ln 94 = **0.14 eV**. The tail tier then needs a mean φ_eff ≥ **0.96 eV** for 64 ms, or 1.04 eV for 1 s.

**Thin-shell lowering (new flag).** The shell is fully depleted, so the anode field is ~(V_bi + V_rev)/15 nm ≈ **0.87 MV/cm**. Thick literature diodes see ~0.2 MV/cm. Image-force lowering, √(qE/4πε₀ε), is 0.177 eV at ε = 4 and 0.102 eV at ε = 12. Thermionic-field emission adds ~0.07 eV (±50%), for **0.18-0.25 eV** of total lowering. At a 10 nm shell it is 0.35-0.45 eV.

**Net bar.** A thick-film barrier must be **≥1.07-1.12 eV** for 64 ms and ≥1.17-1.22 eV for 1 s. Demonstrated contacts, mapped into a 15 nm shell with the σ 0.05 tail:

| Contact | Low-field φ | Tier φ_eff | Tail retention |
|---|---|---|---|
| Passivated a-IGZO (PKU) | 0.82 eV | 0.70-0.73 eV | 13-41 µs |
| Best Pt-IGZO (KIT, secondary) | 0.92 eV | 0.78-0.82 eV | 0.2-0.8 ms |
| AgOx on crystal ZnO (AVS 2008) | 1.10 eV | 0.94-0.98 eV | 35-140 ms (marginal) |

The best IGZO result is **0.15-0.2 eV short** of the 64 ms bar, and 0.25-0.3 eV short of the 1 s bar.

### 2.4 Write, disturb, endurance

- **Write current.** Charging 0.27 fF by 0.5 V in 10 ns takes **~13.6 nA** on average, or **~515 A/cm²**, far above where oxide rectifiers are characterised. Forward bias flattens the shell, so the full low-field barrier applies. A 1.12 eV contact therefore needs V_f ≈ **1.10 V at 0 °C**, not the card's 0.7-0.9 V.
- **Plate-swing rule.** ΔV_PL ≥ Vdata + V_f + 0.2 V ≈ **1.8 V** keeps every stored level below the pillar minimum.
  - Without it, a victim forward-biased by 0.5 V loses 100 mV in 350 (0.9 eV) to 2.3e5 (1.1 eV) pillar accesses. At ~2e7 accesses/s, a 1.0 eV victim fails in **0.45 ms**. With the rule there are zero events.
  - ZrO₂ sees ≤0.7 V, because the floating node follows the plate.
  - A page is a plate segment, with slits every 4 rows (12% area). Inhibit biasing, as in the Sogang 1T-nC thesis, is the alternative.
- **Endurance.** Each access is 2 forward pulses of 5.1e-6 C/cm². Ten years of 64 ms refresh is 9.9e9 pulses, so a 1e12 test covers it ~100×. A hot row needs 1.4e14, so it needs remapping. Drift of 30 meV multiplies leakage 2.6×; 60 meV multiplies it 7×.

### 2.5 Sensitivity

**1e-4-tail retention, 85 °C** (P = ≥64 ms; R = ≥1 s):

| φ_eff | σ 0 | σ 0.03 | σ 0.05 | σ 0.07 |
|---|---|---|---|---|
| 0.90 eV | 902 ms P | 140 ms P | 10 ms | 1 ms |
| 0.95 eV | 4.6 s R | 707 ms P | 49 ms | 5 ms |
| 1.00 eV | 23 s R | 3.6 s R | 246 ms P | 25 ms |
| 1.05 eV | 116 s R | 18 s R | 1.2 s R | 125 ms P |

- **CDS residual vs maximum tiers (z ≥ 3.72).** 5 mV → 117 tiers; 7 → 73; 10 → 40; 15 → 14 (below parity). With the wrapped capacitor, 10 mV allows 148.
- **Escape geometry.** An 80 nm hole with a 30 nm shell and a wrapped Cs (0.90 fF) lowers the 64 ms bar to **0.96-0.97 eV** low-field, at 3.0× (not 3.9×) density at 64 tiers. A 100 nm hole: 0.96 eV at 2.3×.
- **Tier yield.** At 32 / 64 tiers, relative $/bit is 0.53 / 0.33× at a yield of 0.999, 0.61 / 0.42× at 0.995 and 0.71 / 0.58× at 0.99 [ESTIMATE].

### 2.6 GO/NO-GO threshold

Measure on **thin-shell vertical coupons at design thickness**, at 85 °C and 0.7 V reverse.

| Gate | Pass |
|---|---|
| **G1** parity retention | 99.99th-percentile ring leakage ≤ **422 aA** (mean φ_eff ≥ 0.96 eV at σ 0.05) |
| G2 1 s (stretch) | ≤ 27 aA (φ_eff ≥ 1.04 eV) |
| **G3** write | ≥ 0.8 nA at ≤ 1.2 V and 0 °C; n ≤ 1.3 |
| **G4** endurance | Δφ ≤ 30 meV after 1e12 pulses at ~515 A/cm² |
| G5 signal (stack) | post-CDS residual ≤ 7 mV at ≥ 32 tiers |

**GO** if any anode on a ≥15 nm shell, after ≤400 °C, passes G1 + G3 + G4. **NO-GO** if the best tail is > 422 aA, or if Δφ is > 60 meV within 1e10 pulses. **Revival:** the 80 nm escape bar.

---

## 3. What is new versus prior art

| Prior art | Who, when | Covers |
|---|---|---|
| 1TnC FeRAM (n FE capacitors on one node, one plate line each) | Kepler Computing: US 11423967, 11527277, 11521667, 12041785, 11978762; app filed 2021-06-04 | Shared-node, plate-selected stacks, selected by coercivity |
| "One transistor and N memory element" | US 12096638 (Kepler) | Not limited to FE by title. **Read its claims** |
| FE gain bit-cell with stacked capacitors | US 11910618 (Kepler presumed [UNVERIFIED]) | Gain read of a stacked node |
| 3D FeRAM plate lines | Intel, EP4016625 | 1T-nC plate lines |
| 2T-64C FeRAM | Notre Dame / Penn State / IBM / Fraunhofer / NUS, IEDM 2025 | A 64-capacitor shared node can be built |
| 1T-nC disturb and VDD/3 inhibit | Sogang thesis, 2026 | Shared-node disturb |
| 32 Gb NVDRAM | Micron, IEDM 2023 | Competes with the FE variant |
| 3T micro sense amp | IBM (Barth), ISSCC 2007 / JSSC 2008 | Local gain read |
| Oxide NAND-string gain cells | US 8421071, US 8750023 | Series gain strings |
| Oxidized-metal Schottky contacts to ZnO | US 8508015; AVS 2008 (AgOx); Look, APL 2017 (IrOx) | The anode process |
| Diode-selected cross-point memory | US 8134194 family | Diodes selecting *resistive* elements |
| Cross-point DRAM | US 5281837 | A vertical 1T1C, not diode-capacitor |
| Floating-gate 3D-NAND recess | Micron/Intel [prior knowledge] | The tier process |
| Vertical IGZO devices | Kioxia OCTRAM (2024-12, Ioff < 1 aA); imec 2T0C (2025, > 1e12 cycles); IMECAS 4-tier (VLSI 2026) | Access and gain FETs |
| Supporting-block prior art named by Stage 2 critics | Samsung/SK hynix offset-cancellation sense amps, image-sensor CDS (I-05218); Hi-ECC (ISCA 2010), DDR5 on-die ECC, NAND LDPC soft sensing (I-11559); XED (ISCA 2016), Razor (MICRO 2003), weak-cell erasure maps US 8,898,544, chipkill marking (I-11148); Chipkill, SSD RAIN (I-00729); NEO 3D X-DRAM, Huawei vertical CAA IGZO (I-03474, I-10833); Toshiba NAND-structured DRAM, US 12082391 (I-10664); NaMLab biased-AFE ZrO₂, MPB-HZO capacitors (I-02355); Macronix VG-NAND layer select, coded ROM decoders (I-11544) | CDS read, ECC-paid margin, erasure flags, tier codes, in-hole oxide cells, AFE option and tier decoder. None of these is claimed as new |

**Negative result.** Two searches and both stage-2 critics found **no diode-steered linear-capacitor 1T-nC or 1D1C DRAM**. That is not an FTO opinion, and pre-1990 diode-capacitor literature was not searched.

**The genuine delta.**
1. **A per-tier rectifier between each floating node and the shared pillar** replaces coercivity, so the dielectric can be linear ZrO₂. That means no fatigue, wake-up or imprint, and no HZO demand (A2: 14-41% of separated Hf).
2. **Dump read plus clamp write-back in one plate pulse through the same diode.** V_f offsets largely cancel.
3. **The plate-swing rule.** Without it, pillar hammer kills the cell in milliseconds.
4. **A depleted-shell, outer-anode coaxial diode sized to an anode-field limit**, with an optional low-electron-affinity shell.
5. **An in-hole gain FET with CDS** reading the pillar as a local bitline under a raw-BER-1e-4 contract.

Items 1-4 look new. Item 5 combines known parts.

---

## 4. Show-stoppers and how persistence could get around them

1. **Barrier gap: 0.15-0.2 eV (64 ms), 0.25-0.3 eV (1 s).** The design needs ≥1.07-1.12 eV (≥1.17-1.22 eV for 1 s), and the best on IGZO is 0.92 eV. *Paths:*
   - AgOx-class anodes (1.0-1.2 eV on ZnO);
   - Ga-rich IGZO or a-Ga₂O₃ shells, whose lower electron affinity raises every barrier (higher Ga also stabilises Pt/IGZO, Sci Rep 2019);
   - a 20 nm shell (0.11-0.17 eV of lowering);
   - the 80 nm escape geometry (0.96-0.97 eV);
   - [SPECULATIVE] p-NiO/n-IGZO heterojunctions, with generation-limited leakage and no image force.
   All five fit in the coupon matrix for <$10k.
2. **Inhomogeneity: σ 0.05 costs 0.14 eV; σ 0.07 costs 0.21 eV.** *Paths:* interface oxygen control (IrOx barriers are defect-set, Wright State 2017); retention-profiled tier repair (1 spare per 32); tier-orthogonal erasure codes (I-00729).
3. **Write vs retention: V_f ≈ 1.1 V cold, plate swing ~1.8 V.** *Paths:* a temperature-compensated plate driver (V_f moves ~0.1 V from 0 to 85 °C); a 20 ns write (V_f lower by kT·ln2); a thick-oxide ~2 V driver (routine next to NAND's ~20 V). Plate energy is only 0.94 fJ/bit.
4. **Forward-pulse drift: unmeasured; budget ≤30 meV at 1e12.** Unpassivated IGZO diodes are air-unstable (PKU), and a-Si Schottky leakage rises under stress (MRS 1997). *Paths:* SiO₂/Al₂O₃ passivation, Ga-rich shells, hot-row remapping, and a 32 ms refresh guard (budget 844 aA).
5. **Pillar hammer: fails in 1e2-1e5 accesses without the rule.** *Paths:* the plate-swing rule, page = plate segment, or inhibit biasing.
6. **Gain-FET residual: ≤7 mV needed for 32 tiers.** 10 mV caps the tower at 40 tiers (~2.4×); 15 mV caps it at 14. *Paths:* the wrapped capacitor (148 tiers at 10 mV); measure on the shared MARGIN STACK chip; fall back to a bonded silicon gain FET (CELL-WAFER FOUNDRY).
7. **Process: a uniform 15 nm recess along 1.6-3.2 µm holes, and ≥0.998 tier yield.** At 0.99, $/bit at 64 tiers rises from 0.35× to 0.58×. *Paths:* floating-gate NAND ships recess rings at 100+ tiers; spare tiers; the I-11544 decoder.
8. **Anode stability at ≤400 °C.** PtOx and AgOx may decompose [UNVERIFIED]. *Paths:* IrOx, RuOx and MoOx splits, and capping layers.

---

## 5. The decisive experiment

**Question:** does any oxide anode on a thin IGZO, Ga-rich or Ga₂O₃ shell pass G1 + G3 + G4 after ≤400 °C?

**Facilities.**
- **Purdue Birck (first choice):** oxide ALD, and it ran 3 stacked In₂O₃ tiers on 200 mm in 2026. Georgia Tech IEN is the alternate.
- **Argonne CNM:** XPS/UPS and interface TEM, free for non-proprietary work.
- **NIST CNST:** optional internal-photoemission cross-check.

**Steps.**
1. **M0-1.** Fix shells and anodes with the model plus DEVSIM TCAD. **File provisionals first.**
2. **M1-4, fabricate ~30+ variants on ~12 wafers.**
   - Base matrix: 5 anodes (RuOx, IrOx, PtOx, AgOx, MoOx) × 3 IGZO shells (10/15/20 nm) × 2 compositions (standard, Ga-rich).
   - Extra splits: a-Ga₂O₃, a 30 nm escape shell, NiO/IGZO and a Ga-free shell.
   - Process: anode **below** the IGZO, as in the tier; ohmic Mo/ITO cathode; anneals at 300, 350 and 400 °C.
3. **Four structures per die.**
   - (a) 20-200 µm diodes: I-V-T from −40 to 150 °C, C-V, Werner–Güttler mean φ and σ.
   - (b) 1e4-1e6 parallel ring-sized (2,600 nm², e-beam) diodes, for field and size effects.
   - (c) ≥1,000 diode-isolated floating nodes (target 16k, multiplexed). Each has a ring diode, a 1-2 fF MIM and an IGZO source follower, and resolves ~1e-19 A at 85-125 °C.
   - (d) Pulsed-forward arrays: 1e10-1e12 pulses at ~500 A/cm², with I-V-T every decade.
4. **M3-7, measure.** In-house bench plus Argonne. With fewer than 1e4 nodes, extrapolate the 99.99th percentile from the measured 99.9th using the fitted σ, and say so.
5. **M7, gate.**

**Pass/fail, frozen before data.**
- **PASS:** tail ≤ 422 aA at 85 °C and 0.7 V; ≥ 0.8 nA at ≤ 1.2 V and 0 °C with n ≤ 1.3; Δφ ≤ 30 meV at 1e12 pulses. Stretch: ≤ 27 aA.
- **FAIL:** any one of:
  - tail > 422 aA in every split, including the escape split;
  - Δφ > 60 meV within 1e10 pulses;
  - σ > 0.07 eV on every anode.

| Stage A line | $k | Basis |
|---|---|---|
| Design, TCAD | 10 | open TCAD |
| Coupon fab | 100 | ~450 tool-h × $150 + 60 e-beam h × $250 + $15k materials [ESTIMATE] |
| Outside IPE/TEM | 25 | Argonne free if non-proprietary |
| Test bench (reused to M24) | 90 | 4200A + PMU, hot/cold chuck, AWG, CDS board [ESTIMATE] |
| **Total** | **225** | **$135k without the bench**; ~$80-120k marginal inside the portfolio's shared oxide coupon run |

**Stage B (raise milestone, M7-20, $335k).**
- **Build:** a 4-tier stack in 100-200 nm holes (TiN/SiO₂ × 4, recess, ZrO₂, anode, etch-back, IGZO, core), with a wrapped-capacitor split and a discrete gain FET read by a CDS board or the MARGIN STACK chip.
- **Pass:**
  - ≥ 80 mV-equivalent signal at emulated 32-tier load;
  - tail retention ≥ 64 ms at 85 °C;
  - zero flips in 1e9 accesses;
  - 1e12 cycles.

| Months | 0-1 | 1-4 | 3-7 | 7 | 7-14 | 12-18 | 14-20 | 18-24 |
|---|---|---|---|---|---|---|---|---|
| Work | Design, file | Coupon fab | Coupon test | **GO/NO-GO** | Stack 1 | Stack 2, 8-tier | Disturb, retention | Data, raise |

---

## 6. The $1M, 24-month plan

**Quarterly gates** (M0 = 2027-01-04).

| Quarter | Milestone | Gate |
|---|---|---|
| Q1 2027 | 3 provisionals; masks; coupon fab; bench | Filed before user-facility work |
| Q2 2027 | I-V-T and σ on all anodes; ring arrays | ≥ 1.0 eV low-field with σ ≤ 0.07 on a thin shell, else re-spin Ga₂O₃/NiO |
| Q3 2027 | Floating-node retention; 1e12 cycling | **Gate A (2027-07-30): G1 + G3 + G4** |
| Q4 2027 | Stack 1 fab; **PCT conversion of the Q1 filings (12-month deadline)** | Recess ±2 nm by TEM |
| Q1 2028 | Stack 1 measured | Read charge ≥ 50% of Cs·Vdata; shorts ≤ 1% |
| Q2 2028 | Stack 2; 8-tier coupons; disturb | Zero flips in 1e9 |
| Q3 2028 | In-stack retention, endurance, CDS | **Raise gate (2028-08-31)**: Stage B pass |
| Q4 2028 | Data room; second-wave filings; FTO opinion | Raise |

**Allocation ($k).** Stage A 225. Two stack iterations 255 (~1,400 tool-h × $150 + $45k masks and materials). Readout silicon and boards 30. FIB/TEM 25. Reliability 25. IP (3 provisionals, 1 PCT, Kepler FTO read) 45. Two lean founders 300. Travel 15. Contingency 60. **Total 980.** On a NO-GO, the remaining ~$650-700k moves to the FE persistent variant (Notre Dame, Sandia MESA) or to AND-STACK / PIXEL-STACK coupons.

**Team.**
- **Founder A, device (the recruited expert).** An oxide contact and reliability physicist: Schottky I-V-T, IPE, ALD, aA floating-node metrology. Recruit from:
  - Purdue (Ye group [UNVERIFIED]);
  - Notre Dame (Kai Ni) and the 2T-64C team;
  - Georgia Tech (Yu/Khan [UNVERIFIED]);
  - imec/IMECAS 2T0C alumni and the Kioxia OCTRAM team;
  - display IGZO reliability engineers (Sharp, LG Display).
- **Founder B, circuits.** CDS, plate drivers, ECC. Recruit from ex-IBM eDRAM designers (Barth lineage), image-sensor CDS teams (OmniVision, onsemi, Sony) and SSD-controller ECC teams.
- **Advisors.**
  - Process: an ex-Micron Boise floating-gate recess engineer.
  - Oxide-Schottky physics: Wright State (Look), ASU (Nemanich), Liverpool/Durham, KIT/Offenburg, PKU (Zhang Dawei).
- **Programs** [UNVERIFIED fit]: Argonne Chain Reaction Innovations / Activate, NSF SBIR, DOE NSRC proposals.

**IP.**
- **File first (M0-1):**
  1. The diode-steered linear-capacitor 1T-nC cell with single-pulse dump and clamp write-back.
  2. The plate-swing rule plus the page = plate-segment / inhibit scheme.
  3. The depleted-shell outer-anode geometry with a low-electron-affinity shell.
- **Second wave (M14-20):** reference-tier/self-referenced read, retention-profiled tier repair, the wrapped recess capacitor.
- **Publish:** the aA test structure.
- **FTO risks, highest first:**
  - Kepler US 12096638, then 11910618;
  - Intel EP4016625;
  - US 8421071/8750023;
  - US 8508015 (check expiry before commercial AgOx/PtOx/IrOx);
  - Micron/Intel recess patents;
  - IBM micro-SA patents (expiring ~2027-28 [ESTIMATE]).

---

## 7. After the demo: scale path

**Partners and licensees.**
- **Micron.** The U.S. home: floating-gate recess heritage (the tier process), the NVDRAM team (DIODE-TOWER is its volatile, fatigue-free sibling), and U.S. DRAM fabs.
- **Kioxia.** OCTRAM vertical IGZO plus BiCS hole processing: the most experienced oxide-in-hole partner.
- **SK hynix.** Intel's floating-gate NAND line via Solidigm [UNVERIFIED], and 5-tier 3D DRAM yield work.
- **Samsung.** 4F² IGZO VCT and 3D DRAM programs.
- **Intel and Kepler.** Cross-license our diode delta against their 1T-nC estate. The FE variant fits their roadmap.
- **Foundries.** GlobalFoundries and SkyWater for CMOS-under-array or embedded BEOL memory (the ≤400 °C flow is logic-compatible), or fab-lite through CELL-WAFER FOUNDRY.
- **Display makers.** Sharp/SEL, LG Display, Samsung Display and BOE as IGZO-contact materials partners and IP counterparties, not volume makers.
- **Tool makers.** Lam, Applied Materials, TEL and ASM: recess etch and anode ALD co-development.

**What a raise buys.**
- **$10-15M:**
  - an 8-16-tier stack on 200/300 mm via NY CREATES Albany, Sandia MESA or a Micron/Kioxia JDA;
  - a 28 nm CMOS-under-array chip with ~2 V plate drivers;
  - a 64 kb-1 Mb array behind RAW-BER CONTRACT ECC;
  - 1,000 h at 85-95 °C, 1e14 pulses, and tier yield ≥ 0.995 at 16 tiers.
- **$30-50M:** 32 tiers in 60-80 nm holes on 300 mm, spare-tier repair learning, a Mb-Gb CXL Type-3 demonstrator, and license negotiations.

**Standards.** A destructive dump read, page = plate segment and a raw BER of 1e-4 point to CXL attach under RAW-BER CONTRACT's "ECC-native" grade, then JEDEC. DDR/HBM compatibility could come later via logic base dies.

---

## 8. Resources and America

- **EUV: none.** The 121 nm-pitch hole array is one ArF-immersion exposure, and bits come from deposition. Micron 1β already uses zero EUV (A2), so the gain is avoiding 1c-class EUV.
- **Hafnium: not needed.** TiN/ZrO₂ tiers avoid HZO's 14-41% of separated Hf. The AFE upgrade would bring it back.
- **Ruthenium: fine only as a thin anode** [ESTIMATE, this dossier].
  - A solid RuOx ring (49,480 nm³ per tier, 64 tiers) is ~0.0075 cm³ per wafer: 0.04 g Ru, or 0.003 mg/GB.
  - A2's Ru-electrode case deposits ~0.14 mg/GB (0.42 g per 3,068-GB wafer; 26-176% of world Ru, depending on utilization). The ring is ~40× less: **~0.6-4% of world Ru**, just under A2's 5% flag.
  - A 2 nm liner on a TiN ring cuts that ~10×. Ru tripled to $56/g in a year (A2).
  - **Prefer AgOx or MoOx.** Keep Ir to thin liners.
- **Indium and gallium.** The 64-tier IGZO shell is ~0.1 g per wafer (In 0.036 g, Ga 0.022 g), negligible on quantity. But Ga is ~98% Chinese, and the suspension of the U.S. ban lapses **2026-11-27** (A2). Ga-rich and Ga₂O₃ shells raise that exposure, **so keep a Ga-free shell in the matrix.**
- **Energy and water** [ESTIMATE].
  - 1-beta: ~1,300 kWh and 8 m³ per wafer (0.42 kWh/GB, A2).
  - Tower: a 3D-NAND-like 1,300-2,000 kWh wafer yielding ~3.5× the GB gives ~0.12-0.2 kWh/GB.
  - Use phase dominates (~16× fab energy). Refresh is 4.1 vs 6.1 mW/GB, or 0.26 mW/GB at 1 s.
- **PFAS.** The deep-hole etch still uses C₄F₆/C₄F₈, and chamber clean uses NF₃. LEAN ARRAY MODULE's carbon mold is the hedge.
- **U.S. manufacturability.**
  - The demo is all-U.S.: Purdue, Georgia Tech, Notre Dame, Argonne, Sandia, NIST, SkyWater.
  - Recess and ALD tools are largely U.S. (Lam, Applied).
  - **Gap:** there is no U.S. volume 3D-NAND fab, so "depreciated NAND tools" sit mostly in Asia.
  - The U.S. route is Micron's DRAM fabs, NY CREATES Albany, or a fab-lite line whose smaller tool set (no EUV, no 60:1 capacitor module) needs less capital.

---

## 9. Kill criteria (M0 = 2027-01-04)

Physics only; each has a revival condition.

1. **2027-07-30 (M7):** no split after ≤400 °C has a 99.99th-percentile ring leakage ≤ **422 aA** at 85 °C and 0.7 V. → Kill the 60 nm, 3.9× configuration. *Revival:* a contact at the 80 nm escape bar (0.96-0.97 eV low-field, σ ≤ 0.05; 3.0×).
2. **2027-07-30:** the escape split (≥25-30 nm shell, wrapped Cs) also fails G1. → Kill the linear tower and keep the FE variant. *Revival:* a Ga₂O₃ shell or p/n oxide heterojunction ≤ 422 aA per ring.
3. **2027-07-30:** Δφ > **60 meV** within 1e10 pulses at ~500 A/cm² and 85 °C on every G1-passing split. → Kill. *Revival:* passivation or a Ga-rich shell holding ≤ 30 meV to 1e12.
4. **2027-07-30:** the best G1-passing contact gives < **0.8 nA** at 1.2 V and 0 °C. → Kill the 10 ns write. *Revival:* n ≤ 1.3 at the same barrier.
5. **2027-07-30:** σ > **0.07 eV** on every anode. → Kill. *Revival:* σ ≤ 0.05 eV after interface treatment.
6. **2028-03-03 (M14):** 4-tier read charge < **50%** of Cs·Vdata, or ring shorts > **1%**. → Kill the recess process as built. *Revival:* ±2 nm recess and an alternative etch-back.
7. **2028-06-30 (M18):** **any** flip in 1e9 accesses under the plate-swing rule. → Kill the biasing scheme. *Revival:* inhibit biasing with zero flips at ≤ 2× pillar energy.
8. **2028-08-31 (M20):** in-stack tail retention < **64 ms** at 85 °C, or < **60 mV** at emulated 32-tier load. → Kill the raise case. *Revival:* the wrapped split meeting both.
9. **2028-12-29 (M24):** oxide gain-FET residual > **15 mV** (14 tiers, below parity). → Kill the in-hole read and move to a bonded silicon gain FET. Between 10 and 15 mV, cap the claim at ≤ 40 tiers (~2.4×).

---

## 10. Sources

All URLs are logged in `research/sources/*.jsonl` (mainly `dos-diode-tower.jsonl`, plus A2/A3). Most were read through search snippets only.

- Pt-IGZO 0.92 eV (KIT, secondary): https://publikationen.bibliothek.kit.edu/1000121423/82897741
- Pt/a-IGZO, IEEE Access 2020: https://doaj.org/article/155d5567667543779c9bef95b9e29878
- PE-ALD PtOx/ZnO: https://livrepository.liverpool.ac.uk/3015044/
- Empa Pt/IGZO: https://carboquant.empa.ch/web/s405/-/fabrication-characterization-and-simulation-of-sputtered-pt-in-ga-zn-o-schottky-diodes-for-low-frequency-half-wave-rectifi
- Ga-content stability, Sci Rep 2019: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6536494/
- Passivated a-IGZO SBD (PKU): https://ylpgw2023.hkust.edu.hk/ylpgw2021/Abstracts/ZHANG Dawei_Reliable High-Performance Amorphous In-Ga-Zn-O Schottky Diodes With Passivation Layer(1).pdf
- a-Si Schottky drift, MRS 1997: https://www.cambridge.org/core/journals/mrs-online-proceedings-library-archive/article/abs/time-dependence-of-the-reverse-current-in-amorphous-silicon-schottky-diodes/D877540B37303FF67609B6CBC620774A
- AgOx/ZnO, AVS 2008: https://www2.avs.org/symposium2008/Papers/Paper_EM-TuM3.html
- IrOx/ZnO, APL 2017: https://corescholar.libraries.wright.edu/physics/1493
- Au/ZnO (ASU): https://nemanich.physics.asu.edu/node/445
- US 8508015: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8508015
- US 11423967: https://patents.justia.com/patent/11423967
- US 11527277: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11527277
- US 11910618: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11910618
- US 12041785: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12041785
- US 12096638: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12096638
- US 11521667: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11521667
- US 11978762: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11978762
- EP4016625: https://data.epo.org/publication-server/rest/v1.2/patents/EP4016625NWA1/document.html
- US 8134194: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8134194
- US 5281837: https://patents.google.com/patent/US5281837
- US 8421071: https://patents.google.com/patent/US8421071
- Sogang 1T-nC thesis: https://dcollection.sogang.ac.kr/dcollection/srch/srchDetail/000000082483
- 2T-64C, IEDM 2025: https://research.ibm.com/publications/towards-scalable-3d-integration-of-2t-nc-feram-with-hundreds-of-layer-stacking
- IBM micro sense amp: https://researcher.ibm.com/publications/a-500-mhz-random-cycle-15-ns-latency-soi-embedded-dram-macro-featuring-a-three-transistor-micro-sense-amplifier
- imec 2T0C: https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234
- Kioxia OCTRAM: https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology
- IMECAS 4-tier: https://www.ithome.com/0/966/543.htm
- Purdue 3D oxide: https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing
- Sandia MESA: https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/
- sky130 pricing: https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/
- wafer.space GF180: https://www.crowdsupply.com/wafer-space/gf180mcu-run-2
- Micron NVDRAM: https://www.eenewseurope.com/en/iedm-micron-to-present-dram-like-non-volatile-memory-for-ai/
- Ruthenium prices: https://www.kitco.com/news/off-the-wire/2026-03-16/ruthenium-prices-hit-record-high-ai-boom-squeezes-supply
- Ga/Ge suspension: https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us
- SK hynix 5-tier: https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development
- NSTC Albany: https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york

Internal: `research/phaseA/A1_scaling_limits.md`, `research/phaseA/A2_materials_resources.md`, `research/ideas10k/stage2/stage2_results.jsonl`, `research/stage3/FINAL_CONCEPTS.md`.
