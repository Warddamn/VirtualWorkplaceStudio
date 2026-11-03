# First Principles: DRAM From Scratch, and a Home Experiment for Each Law

*Home-lab track T5, written 2026-11-03. This is the backbone the experiment guides (E1-E8) cite. Every number below is printed by [`models/home_lab_calcs.py`](models/home_lab_calcs.py). Section numbers match: "calcs §3" means `python3 models/home_lab_calcs.py --section 3`.*

**Evidence tags.**
- [DATASHEET]: a manufacturer datasheet value.
- [REPORTED]: a paper, patent, press release or study file. Most reached us as search snippets.
- [ESTIMATE]: our own arithmetic, or a bench value we chose.
- [UNVERIFIED]: a textbook or prior-knowledge value we did not re-check this session.
- [STUDY]: a number from the dram-moonshot models. It is a model output, not a measurement.

Prices are approximate as of November 2026.

---

## The short answer

- **DRAM (dynamic random-access memory) is very simple.** A bit is a small charge on a capacitor, kept there by a switch that leaks. Five laws set almost everything: Q = C·V, t = C·ΔV/I, the charge-sharing ratio, E = C·V², and Arrhenius leakage.
- **Each law can be tested at home.** Your parts will be about a million times larger than a chip's, but the law is the same. You can check it to about 5-10% with ±5% capacitors, or to 1-2% if you measure each capacitor with an LCR meter (a ~$15-30 component tester [ESTIMATE]) and cancel the switch's charge injection (§2.3).
- **The study's three picks reduce to three physical facts:**
  - **BEST BET** (hot-side memory) rests on two of them. Wide-bandgap oxides have almost no thermally made carriers (§2.8). And wire capacitance per metre is about the same at every scale, so energy per bit tracks distance (§2.10).
  - **FASTEST PROOF** (raw-BER contract; BER = bit error rate) rests on statistics. The weakest cell in 17 billion sets refresh today. A code moves that job to a much commoner cell (§4).
  - **MOONSHOT** (AND-stack) and **charge-river** rest on the same oxide leakage, plus gain cells and charge transfer (§2.9, §2.11).
- **What home cannot do.** You cannot reproduce 0.01 µm² oxide transistors, or measure their 1e-4 leakage tail. That still needs a university nanofab and about 1e5 devices (§6).
- **What home can do.** You can build the exact measurement method (the floating node, E4). You can also get real tail statistics from a ~$4 DRAM chip with 67 million cells, about $30-65 with the board that drives it (E6).

---

## 1. What a bit physically needs

A working-memory bit must meet six requirements. Each one is a physical requirement, not a design preference.

| Requirement | Physics | Number (calcs §1) |
|---|---|---|
| Two distinguishable states | The states must sit further apart than the noise. Thermal noise alone is sqrt(kT/C) (§2.6) | A DRAM bit is ~17,800 electrons of signal; an oxide gain-cell bit is ~560 electrons [ESTIMATE] |
| Holds long enough | Leakage, or a thermal hop over a barrier, must be slow. For barrier-type bits, Δ = E_b/kT ≥ ln(f0·t·N/P), with P the allowed expected number of failures (0.5 here) | One magnetic bit for 10 years: Δ ≈ 41. A 1 Gbit array with 0.5 expected failures in 10 years (about a 40% chance of any failure): Δ ≈ 62. That is the familiar "Δ ≥ 60" rule [ESTIMATE, f0 = 1 GHz] |
| Cheap to write | The energy is C·V² from the supply (§2.4). Speed comes from a switch that opens in nanoseconds | A 1-beta DRAM cell takes 6 fJ to write [ESTIMATE]. 1-beta is a current DRAM process generation, ~12 nm class [UNVERIFIED] |
| Readable without much energy | The signal must beat sense-amp offset (~50 mV budget) without large charge | 70.9 mV fresh signal in today's DRAM [STUDY] |
| Small | Charge per bit falls with area, so the bit must stay above the noise floor | ~0.1 fF is the kT/C floor for a 50 mV margin (§2.6) |
| Survives ≥1e15 writes | A hot line written every 10 ns for one year sees 3.2e15 writes. Refresh alone over 7 years is 3.5e9 | 1e15+ is the bar [ESTIMATE] |

**State carriers.** A bit can be stored in five physical things.

| Carrier | Examples | Write time | Endurance | What wears out |
|---|---|---|---|---|
| Charge | DRAM, SRAM (static RAM), gain cells, CCD (charge-coupled device) | ns | ~1e16, effectively unlimited [REPORTED, S13] | Nothing moves but electrons |
| Charge behind a thick barrier | NAND/NOR flash | µs-ms | 1e3-1e5 [UNVERIFIED] | Tunnelling damages the oxide |
| Polarization | FeRAM (ferroelectric RAM), FeFET (ferroelectric field-effect transistor) | ~10 ns [REPORTED, S13] | ~1e10-1e12 [UNVERIFIED] | Fatigue, imprint |
| Spin | STT-MRAM (spin-transfer-torque magnetic RAM) | ~10 ns | 1e12 to >1e15, sources differ [REPORTED, S13] | Tunnel-barrier breakdown |
| Resistance, via atom position | PCM (phase-change memory), RRAM (resistive RAM) | 10-50 ns | 1e8-1e9 (PCM), ~1e11 (RRAM) [REPORTED, S13] | Atoms migrate; filaments break |
| Mechanical position | NEMS (nano-electromechanical) relays, racetrack domains | ns-µs | Varies | Contacts wear |

**Why charge won working memory.**
- **Nothing wears out.** Writing moves only electrons. No atoms move, and no oxide is tunnelled through.
- **Writes are fast.** The array swings only ~1 V. The access transistor's gate (the wordline) is boosted above that (VPP; the VPP rail of DDR4, the previous PC memory standard, is 2.5 V [UNVERIFIED]), so a full "1" passes in nanoseconds despite the transistor's threshold voltage.
- **The price is leakage.** A transistor that opens easily also closes imperfectly. Charge leaks out, so the chip must rewrite every cell every 32-64 ms: that rewrite is the "refresh".

Every new DRAM idea in the study attacks this price. It lowers the leakage, makes the read gentler, or makes errors cheap.

---

## 2. The DRAM equations: one law, two scales

The chip numbers come from the study's 1-beta cell in [`models/dram_cell_physics.py`](../models/dram_cell_physics.py) (Cs = 5.42 fF, 512-cell bitline = 34.7 fF, 1.05 V). They are imported live, so they match the study exactly.

The bench reference cell is our choice [ESTIMATE]:
- a 1 nF C0G capacitor at 3.3 V, the USB and microcontroller rail. C0G (also called NP0) is a ceramic dielectric with almost no drift, leakage or memory effect;
- a 6.8 nF "bitline" capacitor, so Cbl/Cs = 6.8, close to the chip's 6.4. ([E1](E1_bit_on_the_bench.md#21-law-1-charge-sharing-conservation-of-charge) uses the commoner 4.7 nF and 10 nF values, which bracket it: about 288 and 150 mV with its 30 pF of stray);
- an access switch that passes the full 3.3 V. Use a CMOS (complementary metal-oxide-semiconductor) analog switch, which has N and P transistors together. Or drive an N-channel MOSFET's (metal-oxide-semiconductor field-effect transistor's) gate at least V_t (its threshold voltage) above 3.3 V: a bench "VPP" of 5-10 V from the ≤30 V supply. A plain N-MOSFET driven from a 3.3 V pin stores only 3.3 V − V_t. For a 2N7000 (V_t 0.8-3 V, ~2.1 V typical [DATASHEET range, UNVERIFIED this session]) that is about 1.2 V (calcs §4). The read signal is (V_cell − V/2)·Cs/(Cs + Cbl), so a "1" stored below 1.65 V reads as a "0", and the 212 mV prediction below fails.

### 2.1 Charge: Q = C·V (calcs §2)

| | C | V | Q | Electrons |
|---|---|---|---|---|
| Chip, 1-beta cell | 5.42 fF | 1.05 V | 5.69 fC | 35,500 (17,766 is signal) |
| Chip, oxide gain-cell node | 0.15 fF | 0.6 V window | 90 aC | 562 (1.07 mV per electron) |
| Bench cell | 1 nF | 3.3 V | 3.3 nC | 2.1e10 |

The bench bit holds ~580,000x more charge. That is why a bench cell is easy to read and hard to make leak.

**Home experiment:** E1 (a bit on the bench, a discrete 1T1C cell: one transistor, one capacitor).

### 2.2 Retention: t = C·ΔV / I_leak, and its inverse I = C·dV/dt (calcs §3)

A cell is good until its charge has drooped by the allowed ΔV.

**Chip.** The 1-beta cell may droop 155 mV and still give 50 mV of signal [STUDY]. So:
- 64 ms needs ≤13.1 fA of leakage in the weakest cell;
- 1 s needs ≤0.84 fA.

The oxide gain cell (2T0C: two transistors, zero capacitors; §2.9) is smaller still. With 0.15 fF and 100 mV of droop:
- 1 s needs ≤15 aA;
- 200 s (imec's reported 2T0C retention at 95 °C [REPORTED via study, S16]) implies ~75 zA for the study's 0.15 fF node with 100 mV of droop [ESTIMATE]. It is not a measured property of imec's device.

**Bench.** A 1 nF cell with 0.5 V of droop:

| Leakage | Retention | Typical source [ESTIMATE unless tagged] |
|---|---|---|
| 1 nA | 0.5 s | A cheap MOSFET switch, or a dirty board |
| 10 pA | 50 s | A clean board and a CMOS analog switch |
| 20 fA | 6.9 h | ADA4530-1 electrometer op-amp, worst-case input bias, -40 to 85 °C [DATASHEET, S7] |
| 1 fA | 139 h | The same op-amp, typical at 25 °C [DATASHEET, S7] |

**The inverse is the key measurement method.** Turn the equation around: I = C·dV/dt. Leave a node floating, then measure how fast it droops.
- A 100 pF node that droops 1 mV per hour carries 27.8 aA [ESTIMATE]. That is the arithmetic, not a home result. The ADA4530-1's own ~1 fA typical bias current moves the same node ~36 mV per hour. So at home this resolution exists only as a difference against a blank, and only if the bias current holds steady to a few percent. The datasheet maxima (20 fA at 85 °C, 250 fA at 125 °C) imply it doubles roughly every 11 °C, so ±1 °C of room drift alone moves it ~6-7% [ESTIMATE].
- This "floating-node" method is how attoamp and yoctoamp oxide leakage has been measured: JJAP 51, 021201 reports 135 yA/µm at 85 °C by tracking charge over a long time [REPORTED, S10].
- A Kato-family patent notes that direct current meters bottom out near 10 fA, which is why the slow-droop method is needed [REPORTED, S10].

At home, the real floor is not your voltmeter's resolution. It is everything else that leaks onto the node, or drifts:
- **the node capacitor's own insulation resistance.** C0G datasheet minimums are only ~10-100 GΩ [UNVERIFIED typical vendor spec], which allows 33-330 pA at 3.3 V. Real parts are usually far better, so measure yours in the blank, or use a PTFE, polystyrene or air-dielectric node;
- **the buffer amplifier's input bias current** (≤20 fA max, <1 fA typical at relative humidity (RH) below 50%, for the ADA4530-1 [DATASHEET, S7]);
- **current across the board surface.** Surround the node with a guard ring driven at the node voltage (the ADA4530-1 has a built-in guard buffer), keep humidity below 50% and clean off all flux. Mount the node in air or on PTFE (Teflon) standoffs, never on a solderless breadboard;
- **the switch or relay that charges the node,** which leaks, and the charge it injects when it opens;
- **electrostatic pickup.** Put the node and the device under test (DUT) in a closed, grounded metal box (a cookie tin works) with silica gel inside. Do not touch or walk near the setup during a run;
- **dielectric absorption.** Hold the node at its test voltage for ≥10x the planned observation time before you start, if you can;
- **the voltmeter's drift.** 1 mV per hour on a 3.3 V node needs a reference stable to 0.03% per hour. Use an external analog-to-digital converter (ADC) with its own reference, or a bench digital multimeter (DMM), not a microcontroller ADC referenced to its supply rail;
- **temperature drift.** Log it.

Calibrate C itself with a known charge step (a voltage step through a small, measured capacitor), because the buffer and wiring add several pF, a large share of a 10 pF node.

Run a "blank": the same node and capacitor with the DUT unplugged. Repeat it before and after each DUT run, and subtract it.

**Realistic home floors** [ESTIMATE]:

| Build | Leakage floor |
|---|---|
| Solderless breadboard | pA to nA |
| Clean hand-wired node, in air or on PTFE standoffs, ADA4530-1 guard in use | ~10-100 fA |
| ADA4530-1 evaluation board in a shielded box | ~1-20 fA |
| Best case: eval board, blank subtraction, temperature held to ±0.5 °C | ~0.1-1 fA |

Attoamps are out of reach at home. For scale, 10 fA on 100 pF droops 0.36 V per hour (calcs §3).

The ADA4530-1 needs a 4.5-16 V supply [DATASHEET, S7], so it will not run from the 3.3 V rail. Power it from USB 5 V (check it stays above 4.5 V under load) or a 9 V battery, and keep its output inside your ADC's 0-3.3 V range.

**Home experiments:** E1 (retention of the discrete cell); E4 (the femtoamp leakage bench). E7 and E8 reuse E4 to measure home-made oxide transistors.

### 2.3 Sense signal by charge sharing: ΔV = (V/2)·Cs/(Cs + Cbl) (calcs §4)

DRAM reads by connecting the cell to a bitline precharged to V/2. The cell's charge spreads over both capacitors.

| Case | Cbl/Cs | Signal |
|---|---|---|
| Chip, 512 cells per bitline | 6.4 | 70.9 mV [STUDY] |
| Chip, 128 cells per bitline | 2.2 | 166 mV [STUDY] |
| Chip, a 1 fF cell on the same bitline | 34.7 | 14.7 mV |
| Bench, 1 nF onto 6.8 nF | 6.8 | 212 mV |
| Bench, 1 nF onto 100 nF | 100 | 16.3 mV |

**The signal depends only on the ratio Cbl/Cs, and on V.** This is the "capacitor charge wall" from the study (bottleneck #1).
- Shrink the cell and the signal collapses, unless the bitline shrinks too.
- Or stop sharing charge at all. That is the gain cell (§2.9).

The read is also destructive: the cell's charge is spread out, so the chip must write it back.

**Home experiment:** E1. Sweep the "bitline" capacitor and plot the signal against Cbl/Cs. The points should fall on one curve.
- **Measured parts.** Use C0G (NP0) or film for both capacitors, and measure each one with an LCR meter or component tester. Unmeasured ±5% parts limit the check to ~±7%. An X7R "bitline" capacitor also loses capacitance under DC bias, so avoid X7R.
- **Charge injection.** When the switch turns off, some of its gate charge lands on the cell: about 20 pF of gate capacitance × a 5 V swing is ~100 pC; if 10-50% of it lands on the cell, that is ~10-50 mV on 1 nF [ESTIMATE, calcs §4]. Cancel it by reading a stored 1 and a stored 0 and taking half the difference.
- **No microcontroller pins on the node.** Never wire the cell or the bitline straight to a microcontroller pin, which can leak nA: 1 nA empties 0.5 V from 1 nF in 0.5 s. Buffer the node with a low-input-current CMOS op-amp.
- **No gate-protection Zeners.** Pick switch and read MOSFETs without built-in gate-protection Zener diodes (often marked "ESD protected", i.e. protected against electrostatic discharge; sometimes a "K" suffix such as 2N7002K [UNVERIFIED]). Those leak nA from the gate.

### 2.4 Energy: the supply pays C·V²; the capacitor keeps ½C·V² (calcs §5)

Charging any capacitor from a fixed supply draws C·V². Half is stored. The other half is lost as heat in the switch, whatever its resistance.

| | C·V² from supply | ½C·V² stored |
|---|---|---|
| Chip, 1-beta cell | 5.98 fJ | 2.99 fJ |
| Chip, 512-cell bitline | 38.3 fJ | 19.1 fJ |
| Chip, oxide gain-cell node | 54 aJ | 27 aJ |
| Bench, 1 nF cell | 10.9 nJ | 5.4 nJ |

The bitline costs 6x more than the cell. Moving charge costs more than storing it, at every scale.

**Home experiments:** E1 (charge energy); E3 (wire energy).

### 2.5 Refresh power: P = bits × E_refresh / t_ref (calcs §5)

**Chip.** The study's 46 fJ per refreshed bit (bitline plus wordline, ×2 for periphery) gives:
- 12.2 mW per 16 Gb die at 64 ms;
- 24.4 mW at the 32 ms used above 85 °C;
- 16-33% of an idle server module's power [STUDY].

A 9x longer interval cuts the 32 ms figure to 2.7 mW.

**Bench.** Eight cells refreshed every 10 s draw 68 nW. The microcontroller (~0.1 W) swamps it.

**Lesson:** on a bench the controller dominates, but on a chip the array is the cost. Do not try to show the refresh-power saving with a bench wattmeter. Show it by counting refreshes avoided (E6).

### 2.6 Thermal noise: σ_V = sqrt(kT/C), and a minimum capacitance (calcs §6)

Any capacitor at temperature T has a random voltage of rms sqrt(kT/C).

| Node | C | σ |
|---|---|---|
| Chip bitline, 85 °C | 34.7 fF | 0.38 mV [STUDY] |
| Chip 1-beta cell, 85 °C | 5.42 fF | 0.96 mV |
| Chip oxide gain-cell node, 105 °C | 0.15 fF | 5.9 mV |
| Bench 10 pF node, 25 °C | 10 pF | 20 µV |
| Bench 1 nF cell, 25 °C | 1 nF | 2.0 µV |

**Minimum C.** For an error probability P from kT/C alone, with margin M (half the gap between states): C_min = kT·(z/M)², where z is the normal-tail value for P.
- At 85 °C, a 50 mV margin and P = 1e-15 (z = 7.94): C_min = 0.125 fF.
- Accept P = 1e-4 behind error-correcting codes (ECC; z = 3.72): C_min = 27 aF, about 4.5x lower.
- At a 10 mV margin, C_min = 3.1 fF.

**What it means:**
- Today's 5 fF cell is ~40x above the thermodynamic floor. Its real limits are mismatch and coupling, as the study found.
- The gain cell's 0.15 fF node sits near the floor. Its margins must stay ≥50 mV.

**Home:** theory only. Bench kT/C is microvolts, below what most home setups resolve.

### 2.7 Temperature: I ∝ exp(−Ea/kT) (calcs §7)

Leakage rises with temperature by an activation energy Ea. Near temperature T it doubles every ΔT ≈ ln2·k·T²/Ea.

| Mechanism | Ea (eV) | Doubles every, near 25 °C | Near 85 °C | 25→65 °C (bench) |
|---|---|---|---|---|
| DRAM tail cells | ~0.35 [REPORTED, S8] | 16 K | 23 K | 5.0x |
| Si generation, ~Eg/2 | 0.56 | 9.8 K | 14 K | 13x |
| DRAM main cells | ~0.6-0.7 [REPORTED, S8] | 9.1 K | 13 K | 16x |
| Rule of thumb: retention halves per 10 °C (JEDEC, the memory-standards body, only doubles the refresh rate above 85 °C [UNVERIFIED]) | 0.79 (implied near 85 °C; near 25-65 °C the same rule implies ~0.6, which is how [E6](E6_retention_tail_real_dram.md#22-temperature-leakage-is-thermally-activated) reads it) | 6.9 K | 10 K | 38x |
| Oxide 2T0C extrapolation | 0.8 [STUDY] | 6.8 K | 9.8 K | 40x |
| Si diffusion, ~Eg | 1.12 | 4.8 K | 7.0 K | 174x |

**Worked numbers:**
- **Si DRAM.** A worst cell that just passes 64 ms at 85 °C should hold ≥0.63 s at 25 °C (Ea 0.35), ≥3.2 s (Ea 0.6), or ≥11 s (Ea 0.79).
- **Oxide 2T0C.** imec's 200 s at 95 °C becomes ~103 s at 105 °C and ~30 s at 125 °C (Ea 0.8), matching the hot-side dossier.
- **No 125 °C oxide 2T0C data is published** [STUDY].

**Two lessons:**
- Patents report a lower Ea for tail cells than for typical cells [REPORTED, S8]. Weber et al. tie the tail to gate-induced drain leakage (GIDL) [REPORTED, S8]. So the weakest cells degrade more slowly with heat and are harder to "cool away". **The tail has its own physics.**
- Ea is a fingerprint. Measure it and you learn the mechanism. For example, warm only the device under test (DUT) from 25 to 65 °C and fit Ea from its leakage (E4). Use the guide's own heater with its hardware cut-outs: E4's series-wired resistor block with a bimetal thermostat and a thermal fuse ([E4 §5.3](E4_femtoamp_leakage_bench.md#53-mini-hot-chuck-and-thermostat-only-for-runs-above-room-temperature)), or E6's thermostat box with its four safety layers ([E6 §6](E6_retention_tail_real_dram.md#6-safety)); [SAFETY.md](SAFETY.md#3-heaters-and-thermal-runaway) compares them. Do not improvise a heat mat or a hot plate under a powered board. A dial hot plate alone cycles and overshoots; a 10 K error in the DUT's true temperature changes the fitted Ea by ~21-23% over 25→65 °C [ESTIMATE, calcs §7]. Tape a thermometer probe (thermocouple or DS18B20) to the DUT itself, and after each step wait 15-20 minutes until it reads steady to ±0.5 °C. Keep the amplifier and breadboard outside the warm zone, joined by short PTFE-insulated leads: a warmed ADA4530-1 raises its own bias current and fakes an Arrhenius slope. Choose the node capacitance so the droop stays inside your ADC range at 65 °C, where leakage is 13-174x higher than at 25 °C (table above).

**Home experiments:** E4 (Ea of a junction's leakage); E6 (DRAM retention at two temperatures). For E6, warm the whole DRAM board in E6's own thermostat box and log the chip's case temperature, not the box setting.

### 2.8 Band gap: n_i = sqrt(Nc·Nv)·exp(−Eg/2kT) — the root of the BEST BET (calcs §8)

A semiconductor has free carriers even when undoped, made by heat across its band gap Eg. Their density is n_i. Below, IGZO is indium gallium zinc oxide (a-IGZO is its amorphous form), the oxide in the study's cells, and ZnO is zinc oxide.

Generation leakage scales as n_i, so the activation energy is about Eg/2. Diffusion leakage scales as n_i², so it is about Eg. The gap enters the exponent, divided by about 0.05 eV at room temperature.

| Material | Eg (eV) | n_i at 27 °C (cm⁻³) | n_i / n_i(Si) | One intrinsic carrier per |
|---|---|---|---|---|
| Si | 1.12 | 9.9e9 (textbook ~1e10) [UNVERIFIED, S3-S4] | 1 | 100 µm³ |
| a-IGZO | ~3.05 [REPORTED, S5] | 1e-7 to 2e-6 | ~4e-17 | ~2 m³ |
| IGZO | 3.2 | 6e-9 to 9e-8 | ~2e-18 | ~40 m³ |
| ZnO (E7's likely channel) | 3.37 [UNVERIFIED] | 2e-10 to 4e-9 | ~1e-19 | ~1,000 m³ |

Notes on the table:
- **Ranges.** The oxide ranges cover an electron mass of 0.20-0.34 m₀ [REPORTED, S6] and an unknown hole density of states (1e19-1e21 cm⁻³) [ESTIMATE].
- **Hot.** At 85 °C the oxide/Si ratio is still 1e-14 to 1e-17.

**The intrinsic floor is not the limit.** For a 40×40×10 nm depleted volume (generation current I = q·n_i·Vol/τ):
- silicon at 85 °C gives ~1.5 aA with a poor 1 µs generation lifetime;
- 3.05 eV IGZO gives ~2e-32 A [ESTIMATE].

The oxide floor sits ~8 orders of magnitude below even the yoctoamp-level measurements (135 yA/µm × 0.04 µm = 5.4 yA, vs 2e-32 A). Two consequences:
- **Wide-gap switches have essentially no holes.** So they have no inversion leakage and no GIDL, silicon's tail mechanism. That is why measured oxide leakage reaches <1 aA (Kioxia OCTRAM, S14), ≤200 zA (SEL DOSRAM, S15) and 135 yA/µm at 85 °C (S10) [REPORTED].
- **What is left is extrinsic.** Defects, hydrogen, the gate dielectric and the subthreshold tail set real leakage. **That is why the study's biggest unknown is the defect tail, not the median.**

**Subthreshold, and the hold voltage.**
- The ideal subthreshold swing (SS: the gate voltage per tenfold change in current) is SS = ln10·kT/q: 59.5 mV/decade at 27 °C and 71.1 at 85 °C.
- Off-current falls one decade per SS of gate voltage below the threshold voltage Vt. Hold 1.0 V below Vt and the off-current is ~10 aA at SS 100 mV/dec, or ~1 zA at 72 mV/dec [ESTIMATE, from 100 nA at Vt].
- Each extra 0.2 V of negative hold buys about 2 decades at SS 100. That is why the study's Gate A+ test (its first go/no-go test lot) splits −0.5 vs −0.7 V hold.

**Why leakage tails are lognormal.** Threshold voltage Vt is roughly Gaussian, and leakage is exponential in Vt. So log-leakage is Gaussian, with σ_log10(I) = σ_Vt/SS.
- With σ_Vt = 50 mV and SS = 100 mV/dec, σ = 0.5 decade.
- The 1e-4 cell then leaks 72x the median, and the worst of 1.7e10 cells leaks ~1,700x the median.

**Home experiments:**
- E7 (make your own oxide transistor). A home ZnO transistor will leak far above its n_i floor, at pA to nA, because home films are full of defects. Measuring that gap is the lesson.
- E8 (your own oxide gain-cell memory).
- E4 provides the measurement.

### 2.9 Gain cells: read through a transistor, not by sharing charge (calcs §9)

The oxide node holds 562 electrons. Share them with even the study's short 64-cell read bitline (8.1 fF) and the signal is only ~5 mV (11 mV even with the bitline precharged to one end of the window).

**So the gain cell does not share charge.** The stored charge sits on the gate of a read transistor, and the bitline senses that transistor's current:
- 1 µA for 10 ns moves 10 fC, which is 111x the stored charge;
- the stored charge is untouched, so the read is non-destructive and needs no write-back [ESTIMATE].

**That is why the capacitor can go:**
- signal comes from transistor gain, not from capacitor size;
- the cell becomes two transistors and no capacitor (2T0C);
- the price is a 15 aA leakage budget at the study's 1 s, 105 °C kill line (the pass/fail threshold that ends a concept).

**Bench analogue:** a 150 pF gate node at 3 V holds 450 pC. Read at 1 mA for 1 ms, it moves 1 µC, a ~2,200x charge gain. Charge gain grows with read time (it is I_read·t_read divided by the stored charge), so it is not a property of the cell: always quote it together with the read time.

**Home experiments:** E2 (a gain cell without a capacitor, discrete); E8 (an oxide version).

### 2.10 The price of distance: E_bit ≈ α·C_wire·V² — the root of hot-side memory's ~10x (calcs §10)

A wire is a capacitor. Its capacitance per length is C' = 2πε/ln(outer/inner). Only the **ratio** of sizes enters, and only through a logarithm. So a nanometre chip wire and a millimetre cable carry about the same capacitance per metre:

| Wire | pF per m | fF per µm |
|---|---|---|
| On-chip wire (study value) | 200 | 0.20 [STUDY; 0.1-0.25 reported, S11] |
| 50 Ω board microstrip | 121 | 0.12 [ESTIMATE] |
| RG-58-class coax | 97 | 0.10 [ESTIMATE; datasheets ~100, UNVERIFIED] |
| Two jumper wires 2.5 mm apart, in air | 14 | 0.014 [ESTIMATE] |

**So energy per bit is set by length × V².** Random data charges a wire on 1/4 of bits, so α = 0.25. The study's model uses a conservative α = 0.5; that does not change the ratios.

| Path | C | Wire energy per bit |
|---|---|---|
| Hybrid bond plus via stack, 0.75 V | 10 fF | 1.4 fJ |
| On-chip 1 mm, 0.75 V | 0.2 pF | 28 fJ |
| On-chip 8 mm (HBM port to compute; HBM = high-bandwidth memory, DRAM stacked beside a GPU), 0.75 V | 1.6 pF | 225 fJ |
| Board 10 cm plus pads, 1.1 V | 16 pF | 4.9 pJ |
| Bench: 1 m coax, 3.3 V | 97 pF | 264 pJ |

The study's full model, with drivers, ports and periphery, gives:
- 0.37 pJ/bit delivered for the near tier vs 3.95 pJ/bit for HBM (10.7x) [STUDY];
- ~15 pJ/bit for a DDR5 host link (DDR5: the current PC and server memory standard) [STUDY].

The ~10x does not need exotic physics. It comes from replacing millimetres of wire, ports and stacks with a 1 µm bond. The US Department of Energy (DOE) exascale study quoted 100-200 fJ/bit/mm for on-chip wires [REPORTED, S11]. That is C'·V² at ~0.7-1 V with every bit toggling: 4-7x the α = 0.25 figure above, but the same physics.

**Home experiment E3.** A square wave at frequency f into a wire draws extra supply current ΔI = f·C·V. Predictions:
- 1 m of coax at 1 MHz and 3.3 V: +320 µA;
- 10 m of coax at 100 kHz: +320 µA.

**Validity.** The formula assumes the wire fully charges every half period. So 5·R_source·C (or 3-5 round trips for long coax) must be well under 1/(2f). With a 100 Ω series resistor, 1 m at 1 MHz passes (48 ns against a 500 ns half period), but 10 m at 1 MHz does not (484 ns). Use 100 kHz for the 10 m length (calcs §10).

**How to measure it** [ESTIMATE]:
- Drive the cable from a separate buffer chip (for example a 74AC04, or the 74AHC125 used in E3) through a 33-100 Ω series resistor, not straight from a microcontroller pin. The peak current is ~20 mA, beyond many pin ratings (RP2040 drive settings are 2-12 mA [UNVERIFIED]).
- Measure only that chip's supply current: a multimeter on its mA or µA range, or the drop across a 10-100 Ω shunt (320 µA × 10 Ω = 3.2 mV). Put a 10 µF + 100 nF bypass on the chip side of the meter, so the meter reads the average. Most cheap USB power meters (~1 mA resolution) cannot see this.
- Leave the far end of the coax open. A 50 Ω terminator would draw ~33 mA and swamp the effect.
- Measure first with no cable and subtract that baseline (the buffer and probe have their own switching current).

The extra current should then rise linearly with length, with slope f·C'·V ≈ 320 µA per metre at 1 MHz and 3.3 V. That straight line proves energy tracks distance. [E3](E3_price_of_distance.md#22-expected-readings) uses the RG-58C/U datasheet value, 101 pF/m, and so predicts 333 µA per metre; the 4% gap is this section's geometry estimate against the datasheet, not a contradiction.

### 2.11 Charge transfer: an isolated packet keeps CTE^N (calcs §11)

A charge-coupled device (CCD), or a bucket-brigade device (BBD), stores bits as charge packets and moves them step by step. Each step moves a fraction CTE (charge-transfer efficiency) of the packet forward. The table shows how much of an **isolated** packet is still in its own bucket after N steps; the rest trails behind it.

| CTE | after 32 steps | 98 | 1,024 |
|---|---|---|---|
| 0.98 | 52% | 14% | ~0 |
| 0.997 | 91% | 75% | 4.6% |
| 0.999 | 97% | 91% | 36% |
| 0.9999 | 99.7% | 99% | 90% |

**Chip.**
- The charge-river dossier needs CTE ≥ 0.997 for 98-transfer segments [STUDY].
- imec's "CTE >98%" [REPORTED, S17] decides everything:
  - per transfer, only 14% survives 98 steps, which fails;
  - end to end over 568 transfers, it implies 0.99996 per transfer, which passes easily.

**Bench.** A bucket-brigade audio-delay chip (for example the 1,024-stage V3207D, clocked at 10-200 kHz [DATASHEET via snippet, S25]) passes every sample through N ≈ 1,000 transfers. Charge left behind is not lost: it joins the *next* sample. So inefficiency ε = 1 − CTE does not lower the gain at low frequency. It smears the signal and cuts high frequencies:

The response is |H(f)| = exp[−N·ε·(1 − cos(2πf/f_s))], with f_s the clock (sample) rate [UNVERIFIED textbook, S24].

The gain at DC is exactly 1. A 1 kHz tone at a 100 kHz clock with CTE 0.9999 over 1,024 transfers loses only ~0.002 dB. A BBD's low-frequency gain is set by its on-chip input and output followers and its bias, not by CTE. **So do not infer CTE from low-frequency insertion loss.** Two gain-independent methods:
1. **Isolated pulse (best).** Clock in one pulse, one clock period wide and synchronised to the clock, with empty samples around it. The first trailing sample's height divided by the main sample's height = N·ε. Over 1,024 transfers, a 10% trailing sample means CTE ≈ 0.9999, and a 1% trailing sample means CTE ≈ 0.99999. The chip's output stage adds its own smear; E5 separates it by comparing two chain lengths (the slope against N is ε).
2. **Frequency method.** Measure the gain at f ≤ f_s/100 and at f_s/4. Divide out the sample-and-hold sinc (−0.91 dB at f_s/4) and your output filter (measure the filter alone). Call the extra loss L dB; then ε = L/(8.69·N). Over 1,024 stages, 0.89 dB of extra loss at f_s/4 means CTE 0.9999, and 8.9 dB means CTE 0.999. Avoid a tone at exactly f_s/2: there the sampled amplitude depends on phase, and the sinc alone is −3.9 dB.

**Home experiment:** E5 (charge river, a bucket-brigade device). Measure CTE against clock frequency and temperature.

### 2.12 The physical floor: Landauer's kT·ln2 (calcs §12)

Erasing one bit must dissipate at least kT·ln2: 2.87 zJ (17.9 meV) at 27 °C [UNVERIFIED, S20].

| Operation | Energy | × Landauer |
|---|---|---|
| Oxide gain-cell node, ½CV² | 27 aJ | 9.4e3 |
| 1-beta cell, ½CV² | 3.0 fJ | 1.0e6 |
| DRAM refresh per bit [STUDY] | 46 fJ | 1.6e7 |
| Hot-side near tier, delivered [STUDY] | 0.37 pJ | 1.3e8 |
| HBM, delivered [STUDY] | 3.95 pJ | 1.4e9 |
| Bench 1 nF cell | 5.4 nJ | 1.9e12 |

There are 4-9 orders of magnitude of headroom. **Physics is not the wall. Wires, voltage swing and periphery are.** The headroom means a ~10x gain from geometry breaks no physical law. It does not show that the gain is easy.

### 2.13 Random telegraph noise: why tails, not medians, set refresh (calcs §13)

One electron caught in a defect near the channel shifts the threshold voltage by about q/(C_ox·W·L). EOT below is the equivalent oxide thickness.

| Device | Shift per trapped electron |
|---|---|
| Oxide read transistor, 40×40 nm, 3 nm EOT | 8.7 mV |
| Oxide transistor, 100×100 nm, 5 nm EOT | 2.3 mV |
| Discrete bench MOSFET, ~1 mm² gate | 0.2 nV |

The trap fills and empties at random, so the read current flips between two levels: random telegraph noise (RTN).

**Tails.** Step heights follow roughly an exponential distribution with mean η. The p-quantile is a_p = η·ln(N_t/p), with N_t the mean number of active traps per device.
- With η = 2.8 mV (charge-river dossier), the 1e-4 device sees ~26 mV.
- The study's kill line (1e-4 quantile ≤100 mV) fails if η exceeds ~11 mV [ESTIMATE].

**The general rule.** The median device sees about η. The 1e-4 device sees about 9η.
- Refresh, margins and yield are set by the tail.
- Published papers describe medians.

**Home:** E4 may show "popcorn" (burst) noise, the same RTN physics, in some small-signal parts. You cannot make RTN statistics of nanometre transistors at home.

---

## 3. The first-principles design space: five knobs

The laws above leave exactly five knobs for making DRAM a new way.

| Knob | Law it uses | Study concept | Home demo | What home can show |
|---|---|---|---|---|
| **1. Lower leakage** (wider gap, lower temperature, deeper hold voltage) | n_i ∝ exp(−Eg/2kT); Arrhenius; subthreshold slope | HOT-SIDE (BEST BET), AND-STACK, CHARGE-RIVER | E4, E7, E8; E6 for temperature | Measure fA-level leakage (~10 fA routinely, 0.1-1 fA at best) and its Ea; see a home oxide transistor leak far above its n_i floor |
| **2. Raise the signal without a big C** (gain) | ΔV ∝ Cs/(Cs+Cbl); transistor gain | HOT-SIDE and AND-STACK (capacitorless oxide cells) | E2, E8 | Non-destructive reads with ~100-2,000x charge gain at the chosen read time |
| **3. Shorten the wires** (stack memory on the logic) | E = α·C'·L·V² with C' ≈ constant | HOT-SIDE | E3 | Supply current linear in wire length |
| **4. Accept errors and correct them** | Order statistics; coding | RAW-BER (FASTEST PROOF); every cell's ECC budget | E6 (and E1 margins) | Measure a real retention tail and its spread σ_ln; show a code stretches the interval ~2-30x, set by σ_ln (§4) |
| **5. Move charge, not wires** | CTE^N | CHARGE-RIVER | E5 | Measure CTE of a real bucket-brigade chip with the isolated-pulse method |

**The knobs do not add up blindly.** The raw-BER dossier makes this point: margin and refresh relaxation spend the same error budget. Knob 1 helps every other knob, which is why one oxide tail measurement decides seven concepts.

---

## 4. Statistics of tails: how many samples a 1e-4 quantile needs (calcs §14)

**The problem.** Every pass line in the study sits at a 1e-4 to 2e-5 quantile. For example, "the weakest 1-in-10,000 cell must hold ≥1 s at 105 °C". Medians are easy. Tails need many samples.

**The math (order statistics).** Take N samples. The number K that fall below the true p-quantile is Binomial(N, p), which is close to Poisson(Np) when p is small.
- **Relative uncertainty** of the tail level is about 1/sqrt(Np).
- **A distribution-free 95% confidence interval** for the quantile is the pair of sorted samples [X_(r), X_(s)]. Pick r and s so that P(r ≤ K ≤ s−1) ≥ 0.95. The script computes them exactly. For large Np the normal approximation r, s ≈ Np ∓ 1.96·sqrt(Np) works.
- **Zero failures ("rule of three").** To show the quantile clears a pass line with 95% confidence and no failures, you need N ≥ −ln(0.05)/p ≈ 3/p.

| p | N | Expected tail count Np | True level lies in (95%) | Value uncertainty, lognormal σ = 0.5 decade |
|---|---|---|---|---|
| 1e-4 | 1e3 | 0.1 | cannot estimate | upper bound only |
| 1e-4 | 1e4 | 1 | 0 to 4e-4 | ×0.66 to unbounded |
| 1e-4 | **1e5** | **10** | 4e-5 to 1.8e-4 | **×0.84 to ×1.30** |
| 1e-4 | 1e6 | 100 | 8.1e-5 to 1.2e-4 | ×0.95 to ×1.06 |
| 2e-5 | 1e5 | 2 | 0 to 6e-5 | ×0.74 to unbounded |
| 2e-5 | 1e6 | 20 | 1.2e-5 to 3e-5 | ×0.90 to ×1.14 |
| 1e-4 | 6.7e7 (DRAM chip) | 6,711 | 9.8e-5 to 1.0e-4 | ×0.99 to ×1.01 |

**Rules of thumb:**
- **For an estimate,** aim for Np ≥ 10-30. That is N = 1e5-3e5 at 1e-4, and 5e5-1.5e6 at 2e-5.
- **For a zero-failure pass,** N ≥ 29,957 at 1e-4, and 149,787 at 2e-5.

This is why the study's Gate A+ asks for ≥1e5 cells per split.

A self-test checks the interval. Drawing 300 synthetic sets of 1e5 lognormal samples, the interval covered the true 1e-4 quantile 98% of the time; the theory says ≥97.5% (`--selftest`).

**How arrays and multiplexing get there.** One probe-station measurement per transistor at ~10 s each needs 11.6 days for 1e5 devices [ESTIMATE]. That is before temperature and time splits. The fix is to put the devices in an array and measure many in parallel:
- row and column multiplexers on the chip;
- one sense amplifier per column;
- a floating-node droop measurement on every cell at once (write, wait, read).

**A real DRAM chip already does all of this.** That makes it the cheapest tail-statistics machine you can buy:
- a 64 Mbit chip holds 67,108,864 cells, built-in multiplexers and sense amps;
- the chip costs ~$4-5 at quantity 1 (Alliance AS4C4M16SA-6TCN: DigiKey $3.95, Findchips $4.33, RS £4.97; approx. Nov 2026) [REPORTED, S9]. That is ~$6e-8 per cell. A board that drives it costs ~$30-65 (§5);
- one pass resolves the 1e-4 quantile from 6,711 cells, and the 1e-6 quantile from 67;
- reading all 8 MB takes 8.4 s at 1 MB/s, or 0.42 s at 20 MB/s.

**Timing trap.** Writing and reading take about as long as the wait, and every access to a row also refreshes that whole row. So rows read later have waited longer. A full pass at 1 MB/s (8.4 s) is longer than the expected first failure (below). Use one of these schemes:
- **Same order, same speed.** Write and read the rows in the same order at the same speed. Each row then waits exactly the same time from its write to its read: the set wait plus one pass. Waits cannot be shorter than one pass, so use a fast interface: the STM32 board's memory controller, an RP2040's PIO (programmable input/output) block, or an FPGA (field-programmable gate array) board, at ≥20 MB/s (0.42 s per pass).
- **Refresh burst, then log.** Keep normal refresh running while you write. Then restart every row at once with a burst of 4,096 AUTO REFRESH commands, which takes under 1 ms. Stop refreshing, wait t and read. Log each row's read time and fit with t_i = t + (time row i was read): `fit_retention_from_counts(..., t_offset=...)` in calcs §14 does this.
- **Slice.** Read only a slice of rows per trial, so the slice takes much less time than t.
- **Relax the controller's refresh timer,** so every row is refreshed exactly every P seconds (E6's method A).

In every scheme, make sure the controller sends no AUTO REFRESH commands and does not enter self-refresh during the wait. Close every row within the datasheet tRAS(max), the longest a row may stay open: ~100-120 µs for SDR SDRAM (single-data-rate synchronous DRAM; Micron's MT48LC4M16A2 lists 120 µs) [UNVERIFIED for your part, S28]. Bit-banging a 512-byte row at 1 MB/s keeps it open ~0.5 ms, which is too long. The self-test shows what the trap does: after a refresh burst and a slow 8.4 s read, the "1 s" rung logs 3 failures where a true 1 s wait expects 0.0006. Fitting with each row's real wait recovers σ to 0.1%.

**The honest limit.** The cells are silicon 1T1C, so this is silicon tail physics, not oxide. What E6 builds is the method and the analysis code: the write-wait-read ladder, both data patterns, temperature control and the probit fit (a lognormal fit on a normal-probability scale; calcs uses its binomial maximum-likelihood form, so zero-failure rungs count and a 3-failure rung does not weigh as much as a 144,000-failure rung). That pipeline is exactly what the oxide lot will need later. On 300 synthetic chips the fit recovers the tail's σ to within ~0.5% (5-95% range 0.996-1.004; `--selftest`). That is counting statistics only. On a real chip the error is set by how well a lognormal describes your tail, by VRT (below) and by temperature drift.

**A prior for E6** [ESTIMATE, order of magnitude only]. Fit a lognormal to the study's 85 °C retention anchors (σ_ln = 1.24, from server DIMMs). Shift it to 25 °C with Ea = 0.35-0.6 eV, and apply it to a 64 Mbit chip with each cell tested once in its charged state, every row waiting exactly the set time (see the timing trap above):
- **first failure:** ~0.85-4.3 s;
- **after 10 s unrefreshed:** ~40 to ~13,000 failing cells;
- **after 60 s:** ~2e4 to ~1e6 failing cells.

Halderman et al. found that DRAM keeps much of its data "for several seconds" at room temperature without power [REPORTED, S12], which is consistent. They cut power entirely, which changes the bias on every cell and likely raises leakage [ESTIMATE], so treat this as a loose check. They also chilled live PC memory: do not repeat that on your own machine (§7). E6 uses a stand-alone chip. Your chip will differ, and finding out by how much is the point.

**The raw-BER contract at home.** Assume independent errors, and require <0.01 expected uncorrectable words per full-chip pass. In the home analysis the check bits use chip cells too, so a SECDED word is 72 cells. The stretch factor equals exp(σ_ln·Δz), with Δz = 1.69 for SECDED and 3.28 for BCH-8. So it depends only on the spread σ_ln of your chip's retention distribution, not on temperature or Ea. With the server-anchor σ_ln = 1.24 the chip can go unrefreshed:
- **~8x longer** behind a single-error-correcting, double-error-detecting (SECDED) Hamming(72,64) code: 2.7 s instead of 0.33 s at Ea 0.35, or 13.8 s instead of 1.7 s at Ea 0.6. (0.33 s is where an uncoded chip has a 1% chance of any error; the first expected error is at ~0.85 s.)
- **~57x longer** behind a BCH code (Bose-Chaudhuri-Hocquenghem, a multi-error-correcting code) correcting 8 errors per 512 bits, like the study's line code.

| σ_ln | SECDED stretch | BCH-8 stretch |
|---|---|---|
| 0.5 | 2.3x | 5x |
| 1.0 | 5.4x | 26x |
| 1.24 (prior) | 8.1x | 57x |
| 2.0 | 30x | ~700x |

**Four relaxation factors, four baselines.** Compare factors only when their baselines match:
- [E1](E1_bit_on_the_bench.md#27-sixteen-cells-the-first-taste-of-tails)'s 1.1-1.4x is the second-weakest ÷ the weakest of 16 bench cells (one-error code on one 16-bit word).
- This section's 2.3-30x (8x at σ_ln = 1.24) is the coded chip's safe interval ÷ the uncoded chip's 1%-any-error interval, at the same temperature.
- [E6](E6_retention_tail_real_dram.md#24-expected-results-for-a-64-mbit-sdr-chip-67108864-cells)'s factors (for example SEC-DED 17x at 45 °C, RS-8 42x at 65 °C) are the safe interval ÷ the standard 64 ms window, under per-bit-hour or per-read targets. They are larger because 64 ms sits far below where even an uncoded chip first fails.
- The study's ~9x is for DDR5 server modules at 85 °C with chipkill kept, against standard refresh.

**Measuring σ_ln is the experiment's real result** (calcs §14). The study's own DDR5 figure is ~9x with chipkill (server error correction that survives a whole failed chip) kept. **This is the FASTEST PROOF's mechanism, demonstrated on a $4 chip (about $30-65 with the board that drives it).**

Watch for the known traps:
- **Anti-cells** store a 1 as "discharged", so test both all-0s and all-1s.
- **Variable retention time (VRT)** cells change over hours [REPORTED via study, S19].
- **Data-pattern dependence.**
- **Correlated failures** break the independent-error assumption. Measuring how often they occur is itself a result.

---

## 5. Experiment map

The expected numbers come from `home_lab_calcs.py`. Each guide has its own parts list, procedure and Safety box. The effort column copies each guide's own difficulty (1-5), time and cost; costs are approximate as of Nov 2026 [ESTIMATE].

| ID | Experiment | Effort: difficulty, time, cost | Laws tested | Key expected number (calcs §) | Supports | Proves at home | Cannot prove |
|---|---|---|---|---|---|---|---|
| E1 | A bit on the bench: discrete 1T1C cell | 3 for Part A, 4 for Part B · one day for Part A, a second weekend for Part B · ~$25-40 (A) + $30-45 (B), plus a shared core kit | Q=CV, t=CΔV/I, charge sharing, CV² | 212 mV signal (1 nF/6.8 nF, 3.3 V; E1's 4.7 nF bitline gives 288 mV); 50 s retention at 10 pA with 0.5 V droop (154 s with E1's 1.54 V budget) (§3-5) | Background for all | The laws at ~1e6x scale; the destructive read | Anything about nanoscale leakage |
| E2 | A gain cell without a capacitor | 3 (4 with the JFET and its negative rail) · one weekend · ~$25-45 plus core kit | Transistor gain; non-destructive read | ~2,000x charge gain at a 1 ms read (§9) | HOT-SIDE, AND-STACK | Read without write-back | Oxide behaviour; 0.15 fF nodes |
| E3 | The price of distance | 2 · half a day · ~$15-30 plus core kit | E = α·C'·L·V²; C' ≈ constant | +320 µA per metre of coax at 1 MHz, 3.3 V (§10) | HOT-SIDE | Energy linear in length | The 0.37 vs 3.95 pJ/bit system figure |
| E4 | Femtoamp leakage bench and tail statistics | 3 for the first build, 4 with op-amp option A and the heater (the craft is the hard part) · 1-2 weekends to build (2-3 with the heater), then 2-3 weeks for 30 devices at room temperature, or 6-10 weeks part-time for the full plan · ~$105-150 first build, ~$165-235 full | I = C·dV/dt; Arrhenius | Floor ~10-100 fA by hand, ~1-20 fA on the eval board, 0.1-1 fA at best; 10 fA on 100 pF droops 0.36 V/h. 27.8 aA is the arithmetic only (§3) | BEST BET's measurement method | The floating-node method; Ea of a junction | Attoamp tails of 1e5 oxide devices |
| E5 | Charge river: bucket-brigade device | 2-3 · one weekend, plus 1-2 weekends of runs · ~$40-60 | CTE^N; smear of incomplete transfer | One clock-wide pulse: trailing/main = N(1−CTE); 10% over 1,024 transfers → CTE 0.9999, or 0.89 dB extra loss at f_s/4 (§11) | CHARGE-RIVER | Measuring CTE; its clock and temperature dependence | Oxide buried-channel CTE at 150 MT/s |
| E6 | Retention tail of a real DRAM chip (raw-BER at home) | 3 on a dev board (a bare chip is harder: see step 3 below) · 1-2 weekends to build and debug, then ~12-15 h of runs including heat-up · ~$110-200 | Order statistics; Arrhenius; ECC | First failure ~1-4 s at 25 °C; SECDED stretches ~2-30x, 8x at the prior's σ_ln = 1.24 (§14) | RAW-BER (FASTEST PROOF) | A real 6.7e7-cell tail and its σ_ln; the code's leverage | DDR5 chipkill statistics; server VRT |
| E7 | Make your own oxide transistor | 4 · first proof (battery test) 1-2 weekends; full E7 3-4 weekends if you have built electronics, 6-10 if not · ~$410-550 plus a hot plate for the first proof, ~$1,200 with the measurement rig; makerspace advised | Band gap; subthreshold slope | Expect pA-nA off-current, far above the n_i floor (§8) | BEST BET, AND-STACK materials | That an oxide switches; its on/off ratio | IGZO quality; the aA regime |
| E8 | Your own oxide gain-cell memory | 4 (5 for the 2×2 array) · 2-3 weekends after E7, 1-2 more for the array · ~$49 on top of E7 and its rig, ~$10 more for the array | All of the above combined | Retention = C·ΔV/I of your own transistor (§3, §9) | HOT-SIDE cell concept | A working home-made 2T0C bit | Density, 105 °C tails, endurance at scale |

**Suggested order:**
1. Run `--selftest`.
2. **E1** (one day on a breadboard). Learn the laws and your tools. If you want a half-day warm-up first, do E3.
3. **E6, on a development board that already has the SDRAM soldered on** (for example the STM32F429I-DISC1, ~$30-65 [REPORTED, S26]), not a bare chip. Its memory controller refreshes automatically, so you must stop or relax that; E6 shows how, and ST's reference manual (RM0090) has the refresh and power-down options [UNVERIFIED]. The bare-chip route needs a 54-pin TSOP (thin small-outline package) adapter board, about 39 signal wires, 3.3 V-only logic and your own SDRAM controller code. On that route, budget for the adapter, flux, solder wick, a magnifier and two spare chips, and do the soldering at a makerspace.
4. **E4.** Follow the ESD, shielding and temperature rules (§2.2, §2.7, §7).
5. E2, E3 and E5 in any order.
6. **E7 and E8 last,** ideally at a makerspace. They need the most care.

The home-lab [README](README.md) lays out three paths. A software builder can start at step 3 (E6, at room temperature first) and come back to E1 later.

---

## 6. Honest scope

| What these experiments prove | What they do NOT prove |
|---|---|
| The five DRAM laws hold at bench scale, to ~1-10% depending on how well you measure your parts | That any study concept works at nanometre scale |
| Charge-sharing signal depends only on Cbl/Cs and V | That a 0.15 fF oxide node meets margins at 105 °C |
| Wire energy scales with length, with C' about scale-free | The study's 0.37 vs 3.95 pJ/bit; that is a system model |
| Floating-node droop can resolve currents of ~10 fA and up at home, and ~1-10 fA at best (E4's plan: air or PTFE capacitor, blank subtraction, steady temperature); ~0.1-1 fA only if the buffer's bias current holds steady to a few percent [ESTIMATE]. The floor is set by the buffer's bias current and its drift | aA-zA leakage. That needs the same method with no amplifier on the node during the wait, a guarded vacuum or dry fixture and tight temperature control (a university lab). Also: the 1e-4 leakage quantile of 0.01 µm² IGZO after a 400 °C bond |
| A real DRAM chip has a measurable retention tail, and ECC (error-correcting code) stretches refresh by a factor set by that tail's spread | DDR5 chipkill, multi-chip events, or 1,000 h module statistics |
| Home oxide films can switch | That home films say anything about sputtered IGZO tails |
| An isolated charge packet keeps CTE^N of its charge; the rest trails behind it as smear | Buried-channel oxide CTE at speed |

**The scale-up path** (what it would take next):
1. **Makerspace.** Ventilated hot plates and ovens, a spin coater, a better meter. This step improves E7 and E8 film quality and gives repeatable temperature steps. It is still not cleanroom data.
2. **University nanofab, external-user access.** The study names Purdue's Birck Nanotechnology Center [STUDY]. Rates and access rules vary; ask [UNVERIFIED]. Expect a user agreement, safety training, often a company or university affiliation plus liability insurance, and hourly tool fees [UNVERIFIED]. This step gives:
   - sputtered IGZO and atomic-layer-deposited (ALD) dielectrics;
   - lithography down to µm;
   - probe stations with heated chucks;
   - 1e3-1e4 devices by hand, or more with arrays.
   This is where the Monday action's "Oxide Tail Spec" goes.
3. **Shared wafer lot or shuttle run.** Oxide transistors on a CMOS carrier with on-chip multiplexers and sense amps: the study's Gate A+, ~$240k [STUDY]. Only this step measures ≥1e5 cells per split at 105 °C, which is the number that decides the BEST BET.

---

## 7. Safety, for every experiment

Each guide carries its own Safety box. These rules apply to all of them. The consolidated version, with every guide's rules, a heater comparison and an SDS table, is [SAFETY.md](SAFETY.md).

> **SAFETY — hard rules**
>
> **Electrical**
> - **Power.** Use USB, AA/AAA/9 V cells or a ≤30 V bench supply only. Commercial mains tools (bench supply, soldering station, hot plate, laptop charger) are fine if they are unmodified and undamaged. Never open them, and never build anything that plugs into the wall. No vacuum-tube high voltage. Set the bench supply's current limit (start at 50-100 mA) before you connect a circuit. Check every part's absolute-maximum voltage: 3.3 V parts such as the SDRAM are damaged by 5 V, so never wire them to a 5 V Arduino without level shifters.
> - **Protect your computer.** Plug experiments into a powered USB hub or a USB isolator, not straight into your laptop. Never connect a bench supply to a board's 5 V pin while that board is also on USB, because it can back-feed the computer.
> - **Your own computer's memory.** Do every DRAM experiment on a separate chip or development board. Do not change memory refresh or timing settings in your PC's BIOS/UEFI. Do not chill or pull memory modules from a running PC (the "cold boot" trick in S12). Do not run memory-stress tools on a machine with unsaved work. Back up before you install toolchains or drivers, and copy each run's log off the board when the run ends.
> - **Static (ESD, electrostatic discharge).** The ADA4530-1, small MOSFETs and the DRAM chip can be killed by a spark too small to feel. Wear a wrist strap (it has a built-in 1 MΩ resistor) clipped to a grounded point. Keep chips in their antistatic bags until you fit them, and hold boards by the edges.
> - **Batteries.** Use alkaline or NiMH cells, or a USB power bank. No loose lithium cells (18650, LiPo) without a protection board. Tape the terminals of spare 9 V batteries: a 9 V battery shorted by a jumper wire gets hot enough to burn.
> - **Stored energy.** The 1 nF reference cell at 3.3 V holds 5 nJ, which is harmless. Large electrolytic banks at 30 V can hold joules: avoid them, and discharge through a resistor. Fit electrolytic and tantalum capacitors the right way round, rated at ≥1.5x the supply voltage; reversed, they can burst or burn.
>
> **Heat and cold**
> - **Heat.** Use a dedicated lab-style hot plate with a ceramic or aluminium top. Never use a kitchen pan, griddle or toaster oven, anything with a non-stick (PTFE, "Teflon") coating, or any equipment that will touch food again. Caps: ≤70 °C for anything with a breadboard, jumper wires or a powered board on it; ≤350 °C for bare film samples on glass. Check the surface with a thermocouple, because the dial is not accurate. Anything hotter, and any furnace anneal, goes to a makerspace or university lab. Work on a non-flammable surface and keep paper and solvent bottles at least 1 m away. Keep a CO2 or ABC dry-powder extinguisher (never water) and a fire blanket in reach. Never leave the plate unattended, and unplug it when done: it stays hot after the light goes off.
> - **Solvents and heat.** Never heat or evaporate flammable solvents (isopropanol (IPA), ethanol, acetone) on an open hot plate. Let coatings dry at room temperature with ventilation first.
> - **Cold.** To cool a chip, seal the board in a zip bag with a silica-gel sachet and use a freezer or ice packs. Let it warm to room temperature inside the bag before you open or power it. Never power a wet board: condensation shorts boards and wrecks femtoamp readings. Never put an unbagged board in a freezer that holds food.
> - **Burns and solder.** Use eye protection. Use ventilation or a fume extractor for flux smoke. Prefer lead-free solder. Wash your hands after handling solder. No food or drink at the bench.
>
> **Banned items and chemicals**
> - **Banned.** Hydrofluoric acid, cyanide, mercury, liquid nitrogen, lasers above class 2, and pressurized toxic gases. Also banned: inverted canned air used as a freeze spray (flammable, causes frostbite) and dry ice in any closed container.
> - **Also banned at home:** 2-methoxyethanol, the solvent in most published sol-gel ZnO and IGZO recipes (for example S22). Its safety data sheets list it as a reproductive toxin (Globally Harmonized System code H360FD: may damage fertility and the unborn child) and a flammable liquid (H226) [REPORTED, SDS snippets, S27]. Use E7's water-based ammine route, or ethanol or isopropanol recipes, instead (a 2013 solvent comparison reportedly made ZnO films from all three [UNVERIFIED]). Also banned: metal-nitrate plus organic-solvent "combustion" precursors (indium, gallium or zinc nitrate in 2-methoxyethanol or acetylacetone), which react energetically when heated [REPORTED, S23]; concentrated acids for etching; and sputtering or any vacuum deposition. Do these at a university lab.
> - **Chemicals (E7, E8).** Read the safety data sheet (SDS) before you buy. Wear nitrile gloves, indirect-vent splash goggles and a cotton (not polyester) lab coat or apron. Work beside an open window with a fan blowing outward. Use ≤20 mL of solution at a time. After that room-temperature dry, bake films at ≤100 °C, with no solvent bottle nearby, before any anneal; never put a sample wet with an organic solvent on a plate hotter than ~100 °C. (E7's water-based ammine ink has no organic solvent; E7 bakes it at 120-150 °C outdoors, [E7 §8](E7_make_your_own_oxide_transistor.md#8-procedure) step 13.) Keep an eyewash bottle or a tap within reach, and rinse eyes for 15 minutes if splashed. Store chemicals closed and labelled, in a locked box away from food, children and pets. Collect all zinc- or indium-containing waste in a labelled jar for household-hazardous-waste drop-off; never pour it down the drain. If a step cannot be made safe at home, do it at a makerspace or university lab.
>
> **People and pets**
> - **Children and pets.** Keep them out of the room while the soldering iron, hot plate or chemicals are out. Store coin cells (CR2032 and similar) locked away: a swallowed coin cell can burn through tissue in hours, so get emergency help at once if one goes missing [UNVERIFIED]. Keep pet birds in another part of the house during any heating step; they are very sensitive to fumes [UNVERIFIED].
> - **Sharps.** Wear safety glasses and cut-resistant gloves when you score or snap glass slides, ITO (indium tin oxide) glass or silicon. Work over a tray. Pick up shards with tape or a brush, never fingers, and put them in a taped-shut, labelled cardboard sharps box. Cover clipped leads with your hand as you cut.

---

## 8. What could not be verified this session

- **Textbook values** (silicon Nc, Nv, n_i; the ZnO gap; Landauer; order statistics) were not re-checked [UNVERIFIED]. The self-test confirms the script reproduces them, e.g. n_i(Si) = 9.9e9 cm⁻³ against the textbook ~1e10.
- **Oxide band structure.** The Kamiya-Nomura-Hosono review was not found. IGZO's gap and electron mass come from other snippets. The hole density of states is a wide assumed bound.
- **DRAM retention activation energies** come from patent snippets, not from Hamamoto's IEDM paper.
- **Endurance figures** differ by up to 1,000x between sources, especially for STT-MRAM.
- **The E6 prior** extrapolates server-DIMM tail anchors to a small chip at 25 °C. It could be off by 10x or more.
- **Prices.** Only the 64 Mbit SDRAM price (S9) and the STM32F429I-DISC1 board price (S26) were checked, from search snippets, approx. November 2026. The DigiKey $3.95 SDRAM figure could not be reconfirmed; other listings show $4.33 and £4.97.
- **The charge-transfer formula** |H(f)| = exp[−Nε(1 − cos 2πf/f_s)] is textbook (S24), not re-fetched. It is checked against the simple transfer model (an isolated pulse's trailing/main ratio is exactly Nε) and agrees with the E5 analysis code.
- **tRAS(max)** for the AS4C4M16SA was not found; ~100-120 µs is typical for SDR SDRAM.
- **Board-level leakage floors** (breadboard pA-nA, hand-wired ~10-100 fA, eval board ~1-20 fA) are estimates, not measurements.
- **Safety facts** on coin cells, PTFE fumes and pet birds were not re-checked this session [UNVERIFIED].

---

## Sources

| # | Source | Used for | Tag |
|---|---|---|---|
| S1 | BIPM, *The International System of Units (SI Brochure)*, 9th ed., 2019. https://www.bipm.org/en/publications/si-brochure | Exact k_B, e, h, c | [REPORTED] (standard; not re-fetched) |
| S2 | CODATA 2018: Tiesinga et al., *Rev. Mod. Phys.* 93, 025010 (2021) | ε₀, m₀ | [UNVERIFIED] |
| S3 | S. M. Sze, K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed., Wiley 2007, App. G | Si Eg, Nc, Nv, Varshni fit | [UNVERIFIED] |
| S4 | P. P. Altermatt et al., *J. Appl. Phys.* 93, 1598 (2003) | n_i(Si) = 9.65e9 cm⁻³ | [UNVERIFIED] |
| S5 | U. Michigan OME lab, "Photosensitivity of amorphous IGZO TFTs for active-matrix flat-panel displays". https://web.eecs.umich.edu/omelab/downloads/Photosensitivity%20of%20Amorphous%20IGZO%20TFTs%20for%20Active-Matrix%20Flat-Panel%20Displays.pdf | a-IGZO optical gap ~3.05 eV | [REPORTED] (snippet) |
| S6 | arXiv 1812.11333 (ar5iv mirror https://ar5iv.labs.arxiv.org/html/1812.11333); arXiv 1811.08766 (https://arxiv.org/pdf/1811.08766) | 3.13 eV reference gap; electron mass ~0.20 m₀ computed, ~0.33 m₀ for c-IGZO | [REPORTED] (snippets; arxiv.org is blocked here) |
| S7 | Analog Devices, ADA4530-1 datasheet, Rev. C. https://www.analog.com/media/en/technical-documentation/data-sheets/ADA4530-1.pdf ; distributor summary https://www.digikey.com/en/product-highlight/a/analog-devices/ada4530-1-electrometer-grade-amplifier | Input bias ±20 fA max (−40 to 85 °C), <1 fA typ at 25 °C, ±250 fA max at 125 °C; supply 4.5-16 V (±2.25 to ±8 V); integrated guard buffer | [DATASHEET] (snippets) |
| S8 | US 6697992 (https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6697992); US 7051260 (https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7051260); Weber et al., TUHH (https://tore.tuhh.de/entities/publication/d044c2f2-f544-42c7-8293-2985814bdad2) | Tail Ea ~0.35 eV, normal ~0.6-0.7 eV ≈ Eg/2; GIDL as the tail mechanism | [REPORTED] (snippets) |
| S9 | DigiKey, Alliance Memory AS4C4M16SA-6TCN. https://www.digikey.com/en/products/detail/alliance-memory-inc/AS4C4M16SA-6TCN/5214135 ; RS https://twen.rs-online.com/web/p/sdram/0842641 ; Findchips listing (from a reviewer's search; URL not recorded) | 64 Mbit SDR SDRAM, 3.3 V, 54-TSOP II. DigiKey $3.95, Findchips $4.33 ($3.74 at qty 10), RS £4.97, all qty 1, approx. Nov 2026 | [REPORTED] (snippets; DigiKey figure not reconfirmed) |
| S10 | *Jpn. J. Appl. Phys.* 51, 021201 (2012). https://doi.org/10.1143/JJAP.51.021201; US 10559667 (https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10559667) | IGZO off-current 135 yA/µm at 85 °C via long-duration charge tracking; ~10 fA earlier detection limit | [REPORTED] (snippets; authorship not confirmed) |
| S11 | arXiv 1907.05748 (https://arxiv.org/pdf/1907.05748); arXiv 1512.00762 (https://arxiv.org/pdf/1512.00762); DOE ASCAC 2011 slides (https://sc.osti.gov/-/media/ascr/ascac/pdf/meetings/aug11/Chaing.pdf) | On-chip wire 0.1-0.25 fF/µm; 100-200 fJ/bit/mm | [REPORTED] (snippets) |
| S12 | J. A. Halderman et al., "Lest We Remember: Cold Boot Attacks on Encryption Keys", USENIX Security 2008. https://jhalderm.com/pub/papers/coldboot-sec08.pdf | DRAM keeps data for seconds at room temperature without refresh | [REPORTED] (snippet) |
| S13 | arXiv 1909.12221 (https://arxiv.org/pdf/1909.12221); *Nanoscale Res. Lett.* 9:526 table (https://nanoscalereslett.springeropen.com/articles/10.1186/1556-276X-9-526/tables/2) | Endurance and write-time ranges | [REPORTED] (snippets; they conflict) |
| S14 | Kioxia OCTRAM press release, 2024-12-10. https://www.kioxia.com/en-jp/about/news/2024/20241210-1.html | Ioff <1 aA per cell; temperature and statistic not stated | [REPORTED] (study log) |
| S15 | SEL DOSRAM, ECI ULSIC vs TFT VII. https://dc.engconfintl.org/ulsic_tft_vii/34 | Leakage ≤200 zA | [REPORTED] (study log) |
| S16 | imec, 40 nm IGZO 2T0C, EDL 2025. https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234 | >200 s at 95 °C, >1e12 cycles | [REPORTED] (study log) |
| S17 | imec, IGZO CCD buffer memory, IEDM 2024. https://imec-publications.be/handle/20.500.12860/59420 | "CTE >98%", >200 s, >1e10 cycles | [REPORTED] (study log) |
| S18 | dram-moonshot study: `models/dram_cell_physics.py`, `models/hot-side-memory.py`, `research/stage3/hot-side-memory_model_output.md`, `models/raw-ber-contract.py`, `dossiers/charge-river.md`, `research/stage3/decision.json` | Cs, Cbl, 46 fJ refresh, 0.37/3.95 pJ/bit, retention anchors, CTE floor, kill lines | [STUDY] |
| S19 | RAIDR, ISCA 2012 (https://www.pdl.cmu.edu/ftp/NVM/raidr-isca12.pdf); REAPER, ISCA 2017 (https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_paper.pdf) | Retention anchors; VRT | [REPORTED] (via study) |
| S20 | R. Landauer, *IBM J. Res. Dev.* 5, 183 (1961); A. Bérut et al., *Nature* 483, 187 (2012) | kT·ln2 bound and its measurement | [UNVERIFIED] |
| S21 | H. A. David, H. N. Nagaraja, *Order Statistics*, 3rd ed., Wiley 2003; J. A. Hanley, A. Lippman-Hand, *JAMA* 249, 1743 (1983) | Quantile confidence intervals; rule of three | [UNVERIFIED] (math checked by self-test) |
| S22 | KAIST, sol-gel ZnO thin-film transistor thesis/paper (0.3 M zinc acetate in 2-methoxyethanol with ethanolamine). https://dspace.kaist.ac.kr/bitstream/10203/25128/1/2010_695.pdf | The standard sol-gel ZnO recipe uses 2-methoxyethanol | [REPORTED] (snippet) |
| S23 | FCT-UNL, "Solution-based zinc tin oxide TFTs: the dual role of the organic solvent". https://docentes.fct.unl.pt/ritasba/publications/solution-based-zinc-tin-oxide-tfts-dual-role-organic-solvent-0 | 2-methoxyethanol acts as a fuel with metal nitrates in combustion precursors | [REPORTED] (snippet) |
| S24 | C. H. Séquin, M. F. Tompsett, *Charge Transfer Devices*, Academic Press, 1975 | Transfer-inefficiency frequency response exp[−Nε(1 − cos 2πf/f_s)]; trailing charge | [UNVERIFIED] (textbook, not re-fetched) |
| S25 | Coolaudio V3207 data sheet copy: 1,024-stage BBD, 10-200 kHz clock, 4-10 V supply. https://studylib.net/doc/18495714/v3207-1024-stage-low-noise-bbd-analog-delay-line ; PedalPCB "V3207D sources" thread (stock patchy; one dealer ~$5.35). https://forum.pedalpcb.com/threads/v3207d-sources.29316/ | E5 part example | [DATASHEET] / [REPORTED] (snippets) |
| S26 | STM32F429I-DISC1 (64 Mbit IS42S16400J SDRAM on board) prices: DigiKey https://www.digikey.com/en/products/detail/stmicroelectronics/STM32F429I-DISC1/5731713 (in stock, 99-week factory lead time); DigiKey Italy €26.23 ex-VAT https://punchouttest.digikey.it/en/products/detail/stmicroelectronics/STM32F429I-DISC1/5731713 ; Waveshare $62.99 https://www.waveshare.com/product/32F429IDISCOVERY.htm ; SDRAM part per https://bbs.21ic.com/icview-2515182-1-1.html | ~$30-65 board price, approx. Nov 2026 | [REPORTED] (snippets) |
| S27 | 2-methoxyethanol (CAS 109-86-4) SDS: TCI M0111 https://www.tcichemicals.com/IL/en/p/M0111 ; Sigma-Aldrich SDS copy https://portaleclns.iit.it/files/sds/11%20-%20service%20room/toxic-carcirogenic-corrosive%20cabinet/2-methoxyethanol_2024_eng.pdf | H360FD (reproductive toxicity 1B), H226 (flammable). A US OSHA-format SDS lists fewer codes | [REPORTED] (SDS snippets) |
| S28 | Micron MT48LC4M16A2 SDR SDRAM datasheet, tRAS(max) 120,000 ns (from a reviewer's note; not fetched) | Typical tRAS(max) | [UNVERIFIED] |
