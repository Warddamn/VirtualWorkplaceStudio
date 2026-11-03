# E1: A bit on the bench

*Track T1, bench electronics. Written 2026-11-03. Prices are approximate as of November 2026.*

**Goal.** Build one bit of DRAM (dynamic random-access memory) from a transistor and a capacitor, then grow it into a 16-bit array. Use them to measure the three facts that shape every DRAM chip:
1. Reading a bit shares its charge with the bitline and destroys it.
2. The stored charge leaks away, and faster when warm.
3. Refresh and error correction keep the data anyway.

| | |
|---|---|
| **Difficulty** | Part A (one cell): 3 of 5. Part B (4 x 4 array): 4 of 5 |
| **Time** | Part A: one day (build 4-6 h, or 8-10 h if this is your first build of this kind; measuring 2-4 h). Part B: a second weekend, plus long runs at room temperature or in a spare fridge, which may run overnight (heater runs never do: they are always attended). Each temperature point: 1-5 h |
| **Cost tier** | $$ (about $25-40 for Part A, $30-45 more for Part B), plus the shared core kit (section 5) |
| **Board** | Raspberry Pi Pico (RP2040) running MicroPython. An early Pico 2 is risky here (section 11) |
| **Code** | [`code/T1_pico/e1_single_cell.py`](code/T1_pico/e1_single_cell.py), [`e1_array_4x4.py`](code/T1_pico/e1_array_4x4.py), [`hamming16.py`](code/T1_pico/hamming16.py), [`analyze_t1.py`](code/T1_pico/analyze_t1.py), [`bench_calcs.py`](code/T1_pico/bench_calcs.py) |

**Acronyms used here.**
- **1T1C:** one transistor, one capacitor, today's DRAM cell.
- **MOSFET:** metal-oxide-semiconductor field-effect transistor.
- **GPIO:** general-purpose input/output pin.
- **ADC:** analog-to-digital converter.
- **ECC:** error-correcting code.
- **C0G:** the most stable ceramic capacitor dielectric, also called NP0.
- **CSV:** comma-separated values.
- **VPP:** the boosted wordline voltage.
- **VRT:** variable retention time.
- **ESD:** electrostatic discharge.
- **SDS:** safety data sheet.
- **PPE:** personal protective equipment.

---

## 1. Why this experiment matters to the study

The study ([DRAM_MOONSHOT_REPORT.md](../DRAM_MOONSHOT_REPORT.md), section 1) picked three ideas. E1 touches two of them directly.

- **FASTEST PROOF: [raw-ber-contract](../dossiers/raw-ber-contract.md).**
  - **The idea.** Let error correction catch the rare weak cells, so DRAM can refresh about 9x less often.
  - **What it rests on.** The *distribution* of retention times across cells, and especially its weak tail.
  - **What E1 adds.** You measure that distribution on 16 cells with the same write-wait-read method the study's Phase 1 uses on real chips. A 16-cell Hamming code then shows the refresh interval stretching.
- **BEST BET: [hot-side-memory](../dossiers/hot-side-memory.md).**
  - **The idea.** Remove the capacitor entirely.
  - **What E1 adds.** You cannot judge a capacitorless cell until you have felt why the capacitor is a problem: the read is destructive, the restore costs energy, and refresh follows from leakage. E1 is the baseline. [E2](E2_gain_cell_no_capacitor.md) is the alternative.

---

## 2. First principles and the numbers to expect

All numbers below come from `python3 code/T1_pico/bench_calcs.py --section e1`. Planning assumptions:
- **Supply.** The Pico's 3.3 V.
- **Precharge.** The bitline (BL) is precharged to V/2 = 1.65 V.
- **Strays.** About 30 pF of stray capacitance on the bitline [ESTIMATE].

### 2.1 Law 1: charge sharing (conservation of charge)

**The setup.** The cell holds charge Q = Cs·Vcell on its storage capacitor Cs. The bitline holds Cbl·Vpre. Opening the access transistor joins them. The total charge stays the same and spreads over Cs + Cbl:

```
Cs·Vcell + Cbl·Vpre = (Cs + Cbl)·Vfinal
dV = Vfinal - Vpre = (Vcell - Vpre) · Cs / (Cs + Cbl)
```

**Worked example.** Cs = 1 nF, Cbl = 4.7 nF + 30 pF stray, stored '1' = 3.3 V:

dV = (3.3 - 1.65) × 1 / (1 + 4.73) = 1.65 × 0.1745 = **+288 mV**

| Cs | Cbl (plug-in) | Cbl/Cs | Expected dV for '1' | for '0' | '1' range with ±5% capacitors |
|---|---|---|---|---|---|
| 1 nF | 1 nF | 1.03 | +813 mV | -813 mV | 772-854 mV |
| 1 nF | 2.2 nF | 2.23 | +511 mV | -511 mV | 476-547 mV |
| 1 nF | 4.7 nF | 4.73 | +288 mV | -288 mV | 265-313 mV |
| 1 nF | 10 nF | 10.0 | +150 mV | -150 mV | 137-164 mV |
| 1 nF | 22 nF | 22.0 | +72 mV | -72 mV | 65-79 mV |

**Compared with a real chip.** A real 1-beta DRAM cell has Cs ≈ 5.4 fF on a 34.7 fF bitline, a ratio of about 6.4. Its fresh signal is about 71 mV at a 1.05 V array [MODEL, `models/dram_cell_physics.py`]. Your 4.7 nF and 10 nF rows bracket that ratio. Same law, one million times more charge.

### 2.2 Law 2: the read destroys the bit

**Why.** After sharing, the cell sits at Vfinal, not at 3.3 V. Read it again without restoring and the signal shrinks by Cs/(Cs+Cbl) each time.

**Expected** (Cs 1 nF, Cbl 4.7 nF): **+288 → about +49 mV** (ratio 0.175 per read). After that, the ~9 mV wordline kickback (section 2.4) that hits the cell each time the wordline falls is as large as the signal. Reads 3 and 4 therefore come out near **+7 and ~0 mV** (even slightly negative), not the +8.8 and +1.5 mV of the pure law [ESTIMATE, `bench_calcs.py` E1.2]. Judge the law on read 2 ÷ read 1 (0.175).

That is why every DRAM read ends with a restore: the sense amplifier drives the bitline back to full rail while the wordline is still open.

### 2.3 Threshold-voltage loss: why DRAM boosts its wordline

**The physics.** An n-channel MOSFET passes a high voltage only up to about V_gate − Vth. Vth (threshold voltage) also rises as the source rises (the body effect).

**Expected** with an ALD1106 (Vth 0.4 min / 0.7 typ / 1.0 max V at 1 µA [DATASHEET, via snippet], body effect γ ≈ 0.5 √V [ESTIMATE]):

| Wordline high | Highest '1' you can store | Vth at that point |
|---|---|---|
| 3.3 V (no boost) | **2.17 V** | 1.13 V |
| 9 V (boosted, from a 9 V battery) | **3.30 V** (full) | 1.28 V |

**Effect on the signal.** The unboosted '1' gives only **+91 mV** instead of +288 mV. Across the datasheet Vth range, the unboosted '1' is 1.91-2.43 V, a signal of +45 to +137 mV [ESTIMATE].

**On real chips.** Real DRAM pumps its wordline to ~2.9 V for a ~1.05 V array (VPP), for the same reason [MODEL inputs, A1].

**With a 2N7000.** Vth is about 2.1 V typical (0.8-3.0 V) [DATASHEET], so a 3.3 V gate passes only about 1.2 V.

### 2.4 Wordline kickback

**The effect.** When the gate falls from 9 V to 0 V, its overlap capacitance pulls the storage node down:

```
dV = 9 V × C_overlap / (Cs + C_overlap)
```

| Switch | Cs = 1 nF | Cs = 10 nF |
|---|---|---|
| ALD1106 (~1 pF overlap [ESTIMATE]) | 9 mV | 0.9 mV |
| 2N7000 (~5 pF gate-to-drain, Crss 4 typ / 5 max [DATASHEET]; in step 9 its drain is on the node) | 45 mV | 4.5 mV |

**Why it matters.** On a chip, Cs is only ~5 fF, so kickback is a real design limit. On the bench it is small, but you can see it.

### 2.5 Law 3: retention = charge budget ÷ leakage

**The law.** Leakage current I drains the node at dV/dt = I/C, so

```
t_retention = Cs × dV_allowed / I_leak
```

**What dV_allowed is.** A '1' still reads correctly while its signal beats the sense amplifier's offset and noise. Budget about 20 mV [ESTIMATE]. With Cs = 1 nF and Cbl = 4.7 nF, the lowest readable '1' is

1.65 + 0.020 × 5.73 = **1.76 V**

So the allowed droop is 3.30 - 1.76 = **1.54 V**.

**Check your own offset.** With 1% resistors, VREF and the GPIO precharge level can each be off by up to ±16.5 mV, so they can differ by ~33 mV, more than the whole 20 mV budget [ESTIMATE]. Use 0.1% resistors for the VREF divider and the precharge pairs (section 5.2), or calibrate: the firmware logs `v_pre` and `v_ref`. If |v_pre − v_ref| plus the comparator offset exceeds ~10 mV, redo the 1.76 V limit above with your measured offset.

| Cs | Leakage | Expected retention |
|---|---|---|
| 1 nF | 1 pA | 1,540 s (26 min) |
| 1 nF | 10 pA | 154 s |
| 1 nF | 33 pA | 46 s |
| 1 nF | 100 pA | 15 s |
| 1 nF | 1 nA | 1.5 s |
| 10 nF | 10 pA | 1,540 s |

**What will leak, at 22 °C:**

| Path | Size | Basis |
|---|---|---|
| ALD1106 transistor, off | ~5 pA | 10 pA typical, 400 pA max at 12 V [DATASHEET]; scaled by √(3.3/12) for the smaller junction voltage [ESTIMATE] |
| 1 nF C0G capacitor at its *worst-case* spec | ≤ 33 pA | Insulation resistance ≥ 100 GΩ at this size [DATASHEET, KEMET]; typical parts are much better |
| Peek op-amp input (LMC6482) | 20 fA typical, 4 pA max | [DATASHEET] |
| Breadboard plastic, flux residue, humidity | unknown, can be 10-1000 pA | Section 6.3 shows how to keep it off the node |

**Planning retention for Cs = 1 nF.** About 300 s if the transistor dominates, down to ~46 s if the capacitor sits at its worst-case spec. That is minutes: easy to measure with a Pico.

### 2.6 Leakage vs temperature

**The physics.** Silicon junction leakage comes from thermally generated carriers:
- In the depletion region, generation current scales with the intrinsic carrier density, n_i ∝ T^1.5·exp(-Eg/2kT).
- Diffusion current scales with n_i².
- Here Eg is the bandgap (1.12 eV for silicon) and k is Boltzmann's constant.

| Temperature | Generation model (n_i) | Diffusion model (n_i²) | ALD1106 datasheet trend (10 pA → 1 nA from 25 to 125 °C) |
|---|---|---|---|
| 4 °C (fridge) | 0.20x leakage → **5x longer retention** | 0.04x | 0.44x → 2.3x longer |
| 22 °C (room) | 1x | 1x | 1x |
| 35 °C | 2.9x | 8.3x | 1.8x |
| 45 °C (warm box) | 6.2x → **6x shorter retention** | 38x | 2.9x → 2.9x shorter |
| 55 °C | 12.6x | 160x | 4.6x |

**Rates.**
- Generation leakage doubles every **8.8 °C**.
- Diffusion leakage doubles every 4.4 °C.
- The datasheet trend doubles every 15 °C.
- The study's DRAM model uses "retention halves every ~10 °C" ([`models/dram_cell_physics.py`](../models/dram_cell_physics.py)).

**What to expect.** Retention between 4 °C and 45 °C should change by roughly 7x to 30x. If it changes by less than ~2x, your leakage is not the transistor. It is the board, the humidity or the capacitor.

### 2.7 Sixteen cells: the first taste of "tails"

**The model.** Retention across cells is roughly lognormal: ln(t) is normally distributed with spread σ. The weakest of N cells sits near the 1/N quantile. The 1e-4 quantile (the study's kill-line level) is median × exp(-3.719·σ).

| σ (spread of ln t) | Weakest of 16 (× median) | 2nd weakest | 2nd ÷ 1st (median of many arrays) | True 1e-4 quantile (× median) | Estimate of it from 16 cells, 90% band |
|---|---|---|---|---|---|
| 0.3 | 0.60 | 0.68 | 1.11x | 0.33 | 0.71-1.44x of true |
| 0.5 | 0.42 | 0.53 | 1.20x | 0.16 | 0.56-1.83x of true |
| 1.0 | 0.18 | 0.28 | 1.44x | 0.024 | 0.31-3.35x of true |

(Monte Carlo in `bench_calcs.py`, 20,000 virtual arrays [ESTIMATE].)

**Two lessons.**
1. **Sixteen cells pin down the median, not the tail.** Even if the shape really is lognormal, the extrapolation to 1e-4 is off by up to ~3x. Real tails often are not lognormal. The study's biggest unknown is exactly this, for oxide transistors, which is why it wants ≥1e5 cells measured directly.
2. **ECC in miniature.** A code that fixes one error per 16-bit word lets you refresh at the *second*-weakest cell's retention. Expect a gain of 1.1-1.4x on 16 cells. The study's ~9x for real modules comes from the same idea applied to billions of cells with long tails ([raw-ber-contract](../dossiers/raw-ber-contract.md)).
3. **Wait steps must be finer than the effect.** A coarse schedule of 4 waits per decade steps by 1.78x. It cannot see a 1.1-1.4x gap: in simulation the measured gain is exactly 1.00 in most arrays. So `retmap` and `ecc` follow the coarse pass with a fine pass in 5% steps. With it, the simulated median gain is 1.10 against a true 1.13 at σ = 0.3, and 1.21 against 1.19 at σ = 0.5 [ESTIMATE, `analyze_t1.py --selftest`].

### 2.8 Refresh energy: bench vs chip

**Bench.** Restoring one '1' costs E ≈ (Cbl + Cs) × V × (V - V_shared) ≈ **26 nJ**. The precharge divider's static current for 5 ms adds 2.7 µJ.

**Chip.** A chip refreshes a bit for about **46 fJ** [MODEL]. That is 5-6 orders of magnitude less, because its capacitors are ~1e5-1e6x smaller and it runs at about a third of the voltage.

**The point.** Same physics, different scale: energy follows C·V².

---

## 3. Honest scope

| What E1 proves | What E1 does NOT prove |
|---|---|
| The charge-sharing law and the Cbl/Cs trade-off that sets DRAM's sense margin | Anything about real DRAM cell numbers (5 fF, fA leakage, 64 ms refresh) |
| That a DRAM read is destructive and needs restore | That the study's ~9x refresh saving holds (that needs billions of cells, real ECC and real modules) |
| Retention = C·dV/I, measured with your own data | Anything about oxide transistors or the 1e-4 to 2e-5 tail statistics (your parts are ~1e6x larger than a chip cell) |
| How retention depends on temperature, and whether your leakage is junction physics or surface leakage | Long-term effects in real DRAM: VRT at the 1e-6 level, row hammer, wear-out |
| The retention-profiling method the study's Phase 1 uses (write, wait, read, log per cell) | Cost, density or manufacturability of any new memory |
| The ECC refresh-extension principle, on a 16-bit codeword | |

**How it scales up.**

| Step | Where | What it adds | Rough cost |
|---|---|---|---|
| 1. This bench | Home | Laws and method; your analysis code | $25-90 |
| 2. Retention profiling of real DRAM | University or company lab: DRAM Bender (an open FPGA-based DRAM tester; FPGA = field-programmable gate array) on Xilinx/BittWare DDR4 boards. It supports DDR3, DDR4 and HBM2, not DDR5 [REPORTED, in the dossier]. A cheaper hobby route (a DDR3 FPGA dev board with an open memory controller and refresh disabled) may exist [UNVERIFIED] | Real cells, real tails, real VRT, millions of cells | ~$14k per station in the study's budget [MODEL, [raw-ber-contract](../dossiers/raw-ber-contract.md)]; ~$90-124k for the study's full Phase 1 |
| 3. Temperature-controlled module study | University lab with a thermal chamber | 65-85 °C points and the 1,000 h statistics the kill line needs | Study Phase 1 |
| 4. Your own cell on silicon | Multi-project-wafer shuttle runs on open process kits (SKY130-class) | A real 1T1C or gain-cell test array | Varies by provider [UNVERIFIED current availability and price] |

---

## 4. Safety

> **SAFETY: E1**
> - **Voltages.** Only USB 5 V, the Pico's 3.3 V and one 9 V battery. No mains-powered builds. The optional heater runs from an unmodified, commercially made 12 V DC adapter (≤30 V).
> - **VPP stays at or below 10 V.** The ALD1106 is rated 10.6 V. Use a 9 V battery only, and measure it first (a fresh one reads ~9.5 V). Never use the 12 V heater adapter for the wordline.
> - **Protect your computer.** The 9 V battery and the 12 V heater adapter share ground with your computer's USB port. One misplaced jumper can push 9-12 V back into the computer, which can damage the port or crash it and lose open work. Connect the Pico through a powered USB hub you can afford to lose, or a USB isolator (ADuM3160-type; full speed is enough for the Pico; about $15-30 [ESTIMATE]). Keep USB 5 V (VBUS) on its own labelled rail, away from the 9 V rail. Check every rail with the multimeter before plugging in USB. Save open work first.
> - **Children and pets.** Keep them away from the bench while the iron is hot and while a heated or long run is going. Store small parts, silica-gel packets, 9 V batteries and IPA out of their reach: small parts and gel packets are choking hazards.
> - **9 V battery.** Never let its terminals touch metal: a shorted 9 V battery gets hot and can start a fire. Store it in its cap or in tape. Take it out of the circuit when you finish.
> - **Soldering.**
>   - The iron tip is about 350 °C. Use a stand, keep the cord clear and never leave a hot iron unattended.
>   - Rosin flux fumes irritate the airways, so work by an open window or with a fume fan.
>   - Lead-free solder is preferred. If you use leaded solder, wash your hands afterwards and keep food away from the bench.
>   - Wear safety glasses: clipped leads fly.
> - **Isopropyl alcohol (IPA, 99%) for cleaning.**
>   - SDS hazards (GHS): H225 highly flammable liquid and vapour; H319 causes serious eye irritation; H336 may cause drowsiness or dizziness [REPORTED, supplier SDS]. Flash point about 12 °C: the vapour can ignite at room temperature.
>   - Use 99% IPA (hardware or electronics shop), not 70% rubbing alcohol, which leaves water behind.
>   - Use small amounts, away from the hot iron and any flame. Ventilate. Wear nitrile gloves and safety glasses.
>   - Never put a board that is still damp into a bag, the fridge or the warm box.
>   - Store it capped, away from heat.
>   - Let small used amounts evaporate outdoors, away from ignition sources, or follow local disposal rules. Never pour IPA down a drain.
> - **Desiccant.** Use non-indicating silica gel, or a cobalt-free orange or green type. Avoid blue-to-pink "cobalt chloride" gel [UNVERIFIED].
> - **Cold run.**
>   - Put the electronics in a zip bag with silica gel, and close the bag around the USB cable with tape. Keep it away from food, and wipe the shelf afterwards.
>   - Use a thin, flat USB cable and check that the door still closes fully. In the family fridge, keep runs to ≤3 h. Longer runs belong in a spare fridge with no food in it, or a picnic cooler with frozen gel packs that do not touch the bag.
>   - Do not use a power bank inside: most switch off at the Pico's small current [ESTIMATE].
>   - When you take the bag out, leave it closed for 30 minutes so water does not condense on the cold board.
> - **Warm run.** Keep the board at **≤55 °C**.
>   - **Heater option 1, the resistor heater (section 6.5):** 12 V, 7.2 W, two 10 Ω resistors **in series**.
>     - Bolt the resistors and the 72 °C thermal fuse to an aluminium plate on metal spacers. Never let them touch foam.
>     - The firmware holds the set point, cuts off at 55 °C and turns the heater off if the sensor fails. A 100 kΩ gate pull-down keeps the heater off whenever the Pico is unplugged or resetting.
>     - Never power the heater unless the script is running its thermostat. Never leave it running unattended.
>   - **Heater option 2, a hair dryer:** only for a short demo (≤15 min, for example watching one cell's `peek` decay speed up). Not for the retention maps: a hair dryer is not made to run for hours and cannot hold 45 °C. Use it as sold, on its lowest setting, at least 30 cm away. Never cover it, never leave it, and stop if any plastic softens.
> - **Stopping a heated run.** Unplug the 12 V heater adapter first. Then stop the script with Thonny's Stop button, or unplug the Pico. Ctrl-C in an `mpremote` terminal stops only the computer side: the Pico keeps running, heater included.
> - **ESD.** The ALD1106 and the CMOS chips are damaged by static. Touch grounded metal before handling them. This protects the parts, not you.

---

## 5. Parts and tools

### 5.1 Shared core kit (also used by E2 and E3)

| Part | Spec that matters | Example part number | Approx. USD | Where to buy |
|---|---|---|---|---|
| Microcontroller board | RP2040; 12-bit ADC, ENOB 8.7 [REPORTED]; MicroPython | Raspberry Pi Pico (SC0915) or Pico H | ~4-5 [UNVERIFIED] | Raspberry Pi approved resellers (Adafruit, PiShop, DigiKey) |
| Solderless breadboards ×2 | Full size | any 830-point | 10-15 [ESTIMATE] | Any electronics shop |
| Jumper wire kit | Solid core, 22 AWG | any | 8 [ESTIMATE] | |
| Digital multimeter | 600 mV range with 0.1 mV resolution; µA range; capacitance range helps | any 6000-count meter | 25-40 [ESTIMATE] | |
| Temperature sensor | ±0.5 °C from -10 to +85 °C [DATASHEET] | DS18B20: bare TO-92 part, or the waterproof probe Adafruit 381 (~$10 [REPORTED]) | 3-10 [ESTIMATE] | Adafruit, DigiKey |
| Resistor and capacitor assortment | 1% metal film resistors | any | 15 [ESTIMATE] | |
| USB data cable | Data, not charge-only | | 5 | |

### 5.2 E1 parts

| Part | Spec that matters | Example part number | Approx. USD | Where to buy |
|---|---|---|---|---|
| Access transistors | 4-terminal n-MOSFET with a separate substrate pin; IDS(OFF) 10 pA typ / 400 pA max at 12 V; IGSS 0.1 pA typ [DATASHEET]; 10.6 V rating [REPORTED] | ALD1106PBL (quad, DIP-14): 1 for Part A, 4 for Part B | 3-8 each (one broker lists $2.90 [REPORTED]) | DigiKey, Mouser, ALD direct |
| Wordline level shifter | 4 channels, low-side 3 V up, high-side to 18 V; no power-up order needed [REPORTED] | CD40109BE (PDIP-16) | 1-2 [ESTIMATE] | DigiKey, Mouser |
| Sense amplifiers (comparators) | Bias ~1 pA, 1.6-5.5 V supply, push-pull output [REPORTED] | MCP6541-I/P (1 ch, Part A), MCP6544-I/P (4 ch, PDIP-14, Part B) | 1-2 each [ESTIMATE] | DigiKey, Mouser |
| Buffer op-amp for the ADC | Input current 20 fA typ / 4 pA max; specified at 3 V; rail-to-rail [DATASHEET] | LMC6482AIN/NOPB (dual, PDIP-8) | 3-5 [ESTIMATE] | DigiKey, Mouser, TI |
| Storage capacitors Cs | C0G (NP0), 5%, 50 V or more. **Not X7R/Y5V**: they leak and drift | 1 nF C0G radial ×20, 10 nF C0G or polypropylene film ×2 | 0.2-0.5 each [ESTIMATE] | |
| Bitline capacitors Cbl | C0G or film, so the value is known; X7R loses capacitance under DC bias | 1, 2.2, 4.7, 10, 22 nF (×4 of 4.7 nF for Part B) | 0.2-0.5 each [ESTIMATE] | |
| Precharge resistors | Matched pair per bitline; 0.1% (or calibrate, section 2.5) | 10 kΩ 0.1% ×10 | ~0.5-1 each [ESTIMATE] | DigiKey, Mouser |
| Reference divider | 1.65 V; 0.1% (or calibrate) | 100 kΩ 0.1% ×2, 1 µF film | ~0.5-1 each [ESTIMATE] | DigiKey, Mouser |
| 9 V battery and clip | VPP for the wordline | | 3-5 | |
| Cleaning | IPA 99%, small brush | | 8 | Pharmacy, hardware store |
| Desiccant and zip bags | For the cold run | | 5 | |
| *Optional warm box* (section 6.5) | 12 V DC adapter rated ≥1 A; 2× 10 Ω 10 W resistors (wired in series); logic-level MOSFET, VGS(th) 1.0-2.0 V, RDS(on) ≤ 35 mΩ at VGS 4 V [DATASHEET]; 220 Ω and 100 kΩ resistors; 72 °C thermal fuse rated ≥2 A; aluminium plate, metal spacers ≥10 mm; 2-3 L foam box | IRLZ44N (TO-220) | 15-25 [ESTIMATE] | DigiKey, Mouser |
| *Optional* hygrometer | Humidity explains many leakage surprises | any | 10 [ESTIMATE] | |
| *Recommended* USB protection | Powered USB hub, or a USB isolator (ADuM3160-type, full speed) | any | 15-30 [ESTIMATE] | |

**Tools.**
- Soldering iron (temperature-controlled), solder, flush cutters, tweezers, safety glasses.
- Optional: a USB oscilloscope (≥10 MHz, 2 channels) to watch the bitline during a read.

---

## 6. Circuits

### 6.1 Circuit A: one cell with a sense amp, restore and probes

```
                 +9 V (battery +; battery - to GND) = VPP          Pico 3V3
                        |                                             |
                  CD40109B VDD                                  CD40109B VCC
   GP2 ---------> CD40109B ch A in        ch A out ---- WL ----------+
                                                                       | gate
                                                         drain  +------+
   GP3 --[10k 1%]--+                                   +--------|  ALD1106 #1
                   +------------ BL --------------------+        |  substrate (V-) -> GND
   GP4 --[10k 1%]--+   |     |       |                          +------ source = SN (air-wired)
                       |     |       |                                     |
                    [Cbl]  MCP6541   LMC6482-A follower -> GP26 (ADC0)   [Cs 1 nF C0G] -> GND
                     GND   (+)=BL                                          |
                           (-)=VREF -> out -> GP5               LMC6482-B follower (+in = SN) -> GP27 (ADC1)
                                                                (optional "peek" probe)

   VREF: 3V3 --[100k 1%]--+--[100k 1%]-- GND,  1 uF film VREF->GND,  VREF -> GP28 (ADC2)
   DS18B20: data -> GP22 (4.7k pull-up to 3V3), taped next to Cs
   LMC6482 and MCP6541 powered from 3V3/GND, 100 nF decoupling on each chip
   CD40109B: all four ENABLE pins -> VDD (high = enabled); unused data inputs B, C, D -> GND
```

**How it works.**
- **Bitline drive.** GP3 and GP4 drive the bitline through equal 10 kΩ resistors:
  - both high = write 1;
  - both low = write 0;
  - one high and one low = precharge to V/2;
  - both set as inputs = bitline floating, ready to sense.
- **Sensing.** The comparator decides 1 or 0 against VREF. The firmware then drives the bitline to that value while the wordline is still open. That is the restore.

### 6.2 Circuit B: the 4 x 4 array (16 bits)

```
                  BL0          BL1          BL2          BL3
   WL0 (CD40109B A) ── cell00 ─── cell01 ─── cell02 ─── cell03    <- ALD1106 package #1 (4 gates tied to WL0)
   WL1 (CD40109B B) ── cell10 ─── cell11 ─── cell12 ─── cell13    <- package #2
   WL2 (CD40109B C) ── cell20 ─── cell21 ─── cell22 ─── cell23    <- package #3
   WL3 (CD40109B D) ── cell30 ─── cell31 ─── cell32 ─── cell33    <- package #4
                        |            |            |            |
                     [4.7 nF]     [4.7 nF]     [4.7 nF]     [4.7 nF]   Cbl to GND
                     2x10k        2x10k        2x10k        2x10k      precharge/write (GP6/7, 8/9, 10/11, 12/13)
                     SA0          SA1          SA2          SA3        MCP6544 (+in = BLn, -in = VREF) -> GP14..17
   each cell = one ALD1106 transistor: drain -> BLn, gate -> WLr, source -> its own 1 nF C0G -> GND
   all four substrate (V-) pins -> GND;  CD40109B: VCC = 3V3, VDD = 9 V, all four ENABLE pins -> VDD
```

**CD40109B enables.** Tie all four ENABLE pins HIGH, to VDD (the wordline supply). Enable is active-high: a low on an enable puts that output in high impedance [REPORTED, TI product page]. A floating output would leave an ALD1106 gate floating and corrupt the data. VDD is a valid logic 1 whichever rail the enables are referenced to. In Part A, also tie the unused data inputs B, C and D to GND: floating CMOS inputs draw current and can oscillate.

**Pin numbers.** Take them for the ALD1106 (G, D, S of each transistor and the V− substrate pin) and the CD40109B (inputs, outputs and enables) from the pin diagram on page 1 of each datasheet. They are deliberately not reproduced here, because this guide could not verify them.

### 6.3 Build rules for low leakage (the part that decides whether it works)

At picoamps, the breadboard is part of your circuit. Follow these rules for every storage node (SN).

1. **Air-wire the storage node.** Bend the ALD1106 source pins outward so they do not enter the breadboard. Solder Cs directly to the bent pin, and put the other leg of Cs into the ground rail. Nothing on the storage node may touch the breadboard plastic.
2. **Clean.** After soldering, scrub flux off the node with 99% IPA and a brush, rinse with fresh IPA (scrubbing alone spreads dissolved flux), blot with a lint-free wipe, and let it dry for at least 1 hour (overnight is better). IPA and water hide under DIP bodies and in breadboard clips. Flux and fingerprints are leakage paths.
3. **Do not touch the node.** Skin oil leaks more than your transistor.
4. **Power the op-amp before the node is charged.** An unpowered chip's input protection diodes conduct and drain the node.
5. **Keep it dry.** Note the humidity in the log. On a humid day, put the board in a box with silica gel.
6. **Choose the right capacitor types.** Use C0G or polypropylene film for Cs. Avoid ceramic X7R and Y5V (they leak and creep, called dielectric absorption) and polyester film.
7. **Guard (advanced).** An electrometer trick: surround the node with a copper wire driven by the peek follower's output. The node and its surroundings then sit at the same voltage, and almost no current flows across the gap.

### 6.4 Pico-specific pitfalls

| Pitfall | What happens | Fix |
|---|---|---|
| ADC input is not an electrometer | The ADC samples by connecting a small capacitor to the pin. It also has a digital input buffer and optional pulls; one forum user read ~30% low through 47 kΩ because a pull was left on [REPORTED] | Never put the ADC on the storage node. Buffer with the LMC6482 (20 fA). The ADC only sees low-impedance follower outputs |
| ADC resolution and noise | 12-bit LSB = 0.806 mV, but ENOB 8.7 [REPORTED] means ~8 mV effective steps. The reference is the 3.3 V rail | Average 64-256 samples (→ ~0.5 mV). GP23 high puts the Pico's regulator in low-ripple mode (non-W boards) |
| ADC DNL spikes (RP2040 erratum E11) | Codes 512, 1536, 2560 and 3584 are wider than the others [REPORTED] | Average many samples; never trust a single LSB step near those codes |
| GPIO leakage | The bitline sits on two GPIO pins, the comparator input and the follower input. The GPIO input leakage is not in this guide's sources [UNVERIFIED]. A 1 µA-class worst case over a ~3 ms float would shift the bitline by ~0.5 V | Measure it: the float test (step 3b) gives the leakage of everything on the bitline. 1 nA would shift it by only ~1 mV. Never connect a GPIO to the storage node |
| Pico 2 (RP2350 A2 stepping) erratum E9 | A pad with its input buffer on, sitting between logic levels, leaks enough to pull toward ~2.2 V [REPORTED]. A floating bitline at 1.65 V is exactly that case | Use an RP2040 Pico, or a Pico 2 confirmed as A4 stepping (reported fixed) [REPORTED] |
| Protection-diode leakage | Every chip input on a node adds its ESD diodes (pA at room temperature, more when warm) | Count inputs: the storage node has only the transistor, Cs and (optionally) one LMC6482 input |

### 6.5 Warm-box heater (optional)

```
   12 V DC adapter (+) --[72 °C thermal fuse, >=2 A]--[10 Ω 10 W]--[10 Ω 10 W]-- IRLZ44N drain
   IRLZ44N source ------ 12 V adapter (-) ------ Pico GND    (one common ground, joined at ONE point, away from the bitlines)
   GP18 --[220 Ω]-- IRLZ44N gate;   100 kΩ from gate to source   (heater OFF whenever the Pico is unplugged or resetting)
   DS18B20 taped to the board under test, not to the heater plate
```

- **Series, never parallel.** In series the resistors make 20 Ω: 12²/20 = 7.2 W at 0.6 A, 3.6 W in each 10 W resistor. In parallel (5 Ω) they would draw 2.4 A and 28.8 W, 14.4 W in each 10 W resistor, overloading both and most adapters [ESTIMATE].
- **Adapter.** 12 V DC, rated ≥1 A, unmodified and commercially made.
- **12 V never touches a Pico pin.** Only the gate resistor and the one common ground join the two circuits. Check with the multimeter before you plug in USB.
- **Mounting.** Bolt both resistors to the aluminium plate. Stand the plate on metal spacers ≥10 mm high, so nothing hot touches foam.
- **Fuse.** Clamp the fuse body to the plate beside the resistors with a metal clip or thermal tape, so it feels their temperature. Join its leads with crimp or screw terminals. Or solder quickly, ≥10 mm from the body, gripping the lead with pliers as a heat sink: soldering heat can open or weaken a thermal fuse.
- **MOSFET.** The IRLZ44N has VGS(th) 1.0-2.0 V and RDS(on) ≤ 35 mΩ at VGS = 4 V [DATASHEET]. At 0.6 A a 3.3 V gate drive turns it fully on in practice [ESTIMATE]: it should stay cool. If it gets warm, use a MOSFET whose datasheet specifies RDS(on) at VGS ≤ 3.3 V.
- **First test, attended, before any board goes in.** Connect the 220 Ω gate resistor to the Pico's 3V3 pin instead of GP18, so the heater is fully on. Close the 2-3 L box with only the DS18B20 inside and watch the temperature for 60 min (`e1_single_cell.py` in `peek` mode logs `temp_c` about every 30 s). If the air passes 55 °C, use a 9 V adapter instead (4 W). Move the gate resistor back to GP18 afterwards.
- **In use.** The firmware preheats, holds the set point for 30 min, and only then measures (section 7, step 15). It starts the Pico's hardware watchdog: if the script hangs, the Pico resets and the gate pull-down turns the heater off. Stay nearby the whole time.

---

## 7. Procedure

### Part A: one cell

1. **Bench-check the parts.**
   - Measure each Cs and Cbl with the multimeter's capacitance range, if it has one, and write the values on a strip of tape.
   - Measure VREF (it should be ~1.65 V) and the 9 V battery.
2. **Measure your floor first, before any transistor.**
   - Air-wire one 1 nF C0G to an LMC6482 follower input.
   - Touch the node briefly to 3.3 V with a jumper, then remove the jumper.
   - Log the follower for 30-60 minutes. Run `e1_single_cell.py` in `peek` mode with the wordline disconnected.
   - Run `python3 analyze_t1.py decay e1_floor.csv --c-pf 1000`. The result is the leakage of the capacitor, the op-amp and your wiring together.
   - **Pass:** under ~1 pA, 5x below the transistor's expected ~5 pA, so the transistor dominates. 1-5 pA works but blurs the temperature test. If it is higher, clean and dry the board before going on.
3. **Build Circuit A.**
   - Start with the CD40109B VDD on **3.3 V**, not 9 V.
   - Install the ALD1106, VREF, the comparator, the followers and the DS18B20.
   - Copy `t1_common.py` and `e1_single_cell.py` to the Pico.
   - **3b. Float test.** With the wordline closed, set `MODE = "float"` and `CBL_NF` to the fitted Cbl, and run `mpremote run e1_single_cell.py > e1_float.csv`. It precharges the bitline, floats it, and reads the BL follower twice 5 ms apart. Run `python3 analyze_t1.py float e1_float.csv`: drift × Cbl ÷ time is the leakage of the GPIOs, the comparator and the follower. **Pass:** drift < 0.5 mV.
4. **See the threshold-voltage loss.**
   - Set `MODE = "peek"` and `PEEK_S = 60`, and run.
   - The peek follower shows the stored '1' settling near **~1.9-2.4 V** (2.2 V at the typical Vth), not 3.3 V (section 2.3).
   - Move the CD40109B VDD to the **9 V battery** and repeat. The '1' should now reach **~3.3 V**.
   - You have just rediscovered why DRAM needs a boosted wordline.
5. **Charge sharing sweep.**
   - Set `MODE = "share"` and `LOGFILE = "e1_share.csv"`, and run from Thonny.
   - Fit Cbl = 1 nF. Type `1` when asked. The script writes and reads '1' and '0' ten times each, with restore.
   - Repeat for 2.2, 4.7, 10 and 22 nF.
   - Copy the file to the PC and run `python3 analyze_t1.py share e1_share.csv`.
   - Compare with the table in 2.1. The script fits one stray capacitance for the whole sweep.
6. **Destructive read.**
   - Set `MODE = "destructive"`, `N_AVG = 1024` (the later reads are only a few mV) and `LOGFILE = "e1_destr.csv"`, with Cbl = 4.7 nF. Run from Thonny and type `4.7` when asked.
   - Expect about +288 and +49 mV, then reads near +7 and ~0 mV (section 2.2), then a full signal again after the restore.
   - Copy the file to the PC and run `python3 analyze_t1.py destructive e1_destr.csv`. Judge read 2 ÷ read 1.
   - Set `N_AVG` back to 64 afterwards.
7. **Retention at room temperature.**
   - Set `CBL_NF` to the bitline capacitor you fitted (4.7) and `MODE = "retention"` (log-spaced waits from 1 s to 30 min, about 2 h in all). This mode asks no questions.
   - Capture with `mpremote run e1_single_cell.py > e1_ret_room.csv`. Also set `LOGFILE` as a backup, and turn off computer sleep.
   - Note the wait at which a stored '1' first reads as 0. Also watch the stored '0's.
8. **Optional: how parking the bitline changes retention.** Repeat step 7 with `PARK = "zero"`.
   - A stored '1' then sees 3.3 V across the transistor instead of 1.65 V.
   - It also loses the −1.65 V gate-to-source bias that held the transistor hard off (gate at 0 V, bitline-side terminal at 1.65 V). Subthreshold channel current can then flow on top of junction leakage. It is negligible for a part at the typical 0.7 V Vth, but can reach tens of pA for a part near the 0.4 V minimum [ESTIMATE, assuming ~90 mV per decade below the 1 µA threshold point]. So retention can drop by much more than 2x, and how much tells you about your part. This is why real DRAM holds unselected wordlines slightly negative.
   - A stored '0' sees no voltage at all.
   - Compare.
9. **Optional: the body-diode trap.**
   - Swap the ALD1106 for a 2N7000, with its source on the bitline side and its drain on the storage node.
   - Store a '0', then run one `share` cycle.
   - The 2N7000's built-in body diode conducts whenever the bitline is above the node, so the "0" charges to ~1.1-1.3 V during precharge.
   - Expect the '0' signal to shrink to about a quarter (roughly -70 mV instead of -288 mV) [ESTIMATE].
   - This is why chip transistors have a separate body terminal held at the lowest voltage. The ALD1106 gives you one.

### Part B: the 16-bit array

10. **Build Circuit B** with the same rules. Air-wire all 16 storage nodes.
11. **Pattern test.** Run `MODE = "pattern"`. Checkerboard, inverse, all-1 and all-0 should read back with **0 errors**.
12. **Retention map at room temperature.**
    - Run `MODE = "retmap"`. It writes all 1s, waits, and reads all 16 cells with no restore. A coarse pass (1 s to 1 h, 1.78x steps) finds where cells fail. A fine pass in 5% steps then resolves each cell (section 2.7).
    - Time: about 2.5-4.5 h at room temperature with the default `FINE_STOP_CELLS = 16`. Set it to 2 to stop once the two weakest cells have failed: ~1 h, still enough for the ECC gain [ESTIMATE, simulated for a 300 s median].
    - Capture with `mpremote run e1_array_4x4.py > e1_retmap_room.csv`, set `LOGFILE` as a backup, and turn off computer sleep.
    - Run `python3 analyze_t1.py retmap e1_retmap_room.csv`. It prints:
      - a 4 x 4 map of retention times;
      - the median, weakest and second-weakest cells;
      - a lognormal σ;
      - the extrapolated 1e-4 quantile with its 90% band;
      - the ECC gain (second ÷ first).
13. **Refresh beats leakage.**
    - Set `T_REF_S` to half the weakest retention from step 12. Run `MODE = "refresh"` (about 2 h: 1 h with refresh, then 1 h without).
    - Expect **0 errors** with refresh, then errors in the no-refresh copy that runs afterwards.
14. **ECC in miniature.**
    - Run `MODE = "ecc"`. It stores the 11-bit word 0x7FF as a 16-bit Hamming codeword (all 16 bits are 1s, the leaky state). Like `retmap`, it runs a coarse pass and then a 5% fine pass, about 1 h at room temperature [ESTIMATE].
    - Run `python3 analyze_t1.py ecc e1_ecc.csv`. It finds the first raw error and the point where the decoder can no longer fix the word (status 2, or `data_ok = 0`).
    - The ratio is your ECC refresh extension. Compare it with 1.1-1.4x (section 2.7).
15. **Temperature.** Repeat step 12 at three temperatures:
    - **Cold (~4 °C).** Read the cold-run rules in section 4 first. Bag the board with silica gel, close the bag around the cable, and wait 1 h to equilibrate. Retention is ~5x longer, so set `FINE_STOP_CELLS = 2`. If no cell has failed by the last wait, set `RET_MAX_S = 14400` and repeat. That takes ~5-7 h, so use a spare fridge with no food in it. It is fine unattended, because no heater is used. A picnic cooler with gel packs (~5-10 °C for a few hours) also works: the analysis uses the temperature you measured.
    - **Room temperature.**
    - **Warm box (45 °C).** Build section 6.5 and do its first test. Set `HEATER_SETPOINT_C = 45.0`. The script preheats, holds 45 °C for 30 min before the first write, and prints `# preheat` lines meanwhile. Then the map takes under 1 h [ESTIMATE]. Stay nearby the whole time. To stop early, unplug the 12 V adapter first.
    - Analyze with `python3 analyze_t1.py temp e1_retmap_cold.csv e1_retmap_room.csv e1_retmap_warm.csv`. It fits an activation energy Ea and the "halves every X °C" figure.
16. **Repeat one run** at room temperature on another day. Cells whose retention moved by more than 2x are candidates for variable retention time (section 10).

---

## 8. Data sheet / log template

Keep a paper or spreadsheet log. Each run also produces a CSV file.

**Data safety.**
- Give every run a new file name with the date, for example `e1_retmap_room_2026-11-08.csv`. A shell `>` overwrites an older file of the same name, while `LOGFILE` appends, so two runs could end up mixed in one file and break the fits.
- For runs over 10 min, also set `LOGFILE` and turn off computer sleep. If the computer sleeps, the PC side stops while the Pico carries on.
- After copying, delete old files from the Pico (`mpremote rm :name.csv`). Its flash is small (~1.4 MB [ESTIMATE]); when it is full, the firmware stops writing the file and continues on USB only.

**Run header (one line per run):**

| Date/time | Board (Pico/Pico 2, stepping) | Part (A/B) | Mode | Cs measured | Cbl measured | WL driver VDD | Bitline park | Temp °C | Humidity % | File name | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

**Charge sharing results (Part A):**

| Cbl (nF) | Cbl/Cs | Predicted dV (mV) | Measured dV '1' (mV) | Measured dV '0' (mV) | Measured ÷ predicted | Sense amp correct (%) |
|---|---|---|---|---|---|---|
| 1 | | +813 | | | | |
| 2.2 | | +511 | | | | |
| 4.7 | | +288 | | | | |
| 10 | | +150 | | | | |
| 22 | | +72 | | | | |

**Retention map (Part B), seconds:**

| | BL0 | BL1 | BL2 | BL3 |
|---|---|---|---|---|
| WL0 | | | | |
| WL1 | | | | |
| WL2 | | | | |
| WL3 | | | | |

**Temperature summary:**

| Temp °C | Median retention (s) | Weakest (s) | 2nd weakest (s) | ECC gain | σ (ln) |
|---|---|---|---|---|---|
| 4 | | | | | |
| 22 | | | | | |
| 45 | | | | | |

**CSV columns written by the Pico:**
- **Part A:** `exp, mode, t_s, temp_c, cs_nF, cbl_nF, wait_s, read_idx, stored_bit, v_pre, v_after, dv, sa_bit, adc_bit, v_ref`
- **Part B retention map:** `exp, mode, t_s, temp_c, wait_s, row, col, stored_bit, read_bit`

---

## 9. Pass / fail criteria

| # | Test | Pass | If it fails |
|---|---|---|---|
| 1 | Floor (step 2) | Leakage of capacitor + op-amp + wiring < 1 pA (1-5 pA works but blurs the temperature test) | Clean, rinse, dry for ≥1 h and air-wire; then retry |
| 2 | Charge-sharing law | Measured dV within ±15% of prediction (with measured capacitors and a fitted stray ≤ 100 pF) for Cbl/Cs from 1 to 22 | Check that the bitline really floats and that VREF is correct |
| 3 | Destructive read | Second-read ÷ first-read signal = Cs/(Cs+Cbl) within ±25% | |
| 4 | Boost | The '1' rises from 1.9-2.4 V to ~3.3 V when VDD goes from 3.3 V to 9 V | Check that VDD really moved to the battery |
| 5 | Refresh | Zero errors for 1 h with T_ref ≤ ½ × the weakest retention; errors without refresh | |
| 6 | Temperature | Retention at 45 °C ≥ 2x shorter than at 22 °C, and at 4 °C ≥ 1.5x longer | An informative "fail": your leakage is surface or dielectric, not junction. Find it |
| 7 | ECC | `analyze_t1.py ecc` reports an extension > 1.0 (the decoder still fixes the word at a longer wait than the first raw error) | Make sure the fine pass ran (a `# fine pass` line in the log) |

---

## 10. What would surprise you (and why it would matter)

- **Retention barely depends on temperature.** The leakage path is then not silicon at all: it is surface water, flux or the capacitor. On a chip, that kind of non-thermal, defect-driven leakage tail is exactly what the study fears for oxide transistors.
- **A cell's retention jumps between runs by 2x or more, with nothing else changed.** That is variable retention time (VRT). Real DRAM has it, and the raw-ber-contract kill line explicitly includes it. Log which cell, how often, and by how much.
- **The weakest of 16 cells is 10x or more below the median.** A heavy tail. Lognormal statistics would make that rare (σ ≈ 1 gives ~5.6x). A part with a defect behaves like a real "tail cell".
- **Stored '0's fail too.** With the bitline parked at 1.65 V, subthreshold current leaks into a '0'. Real DRAM sees this too. In real chips about half the cells are also "anti-cells": a logical 1 is stored as a discharged capacitor, because the cell sits on the complementary bitline of its sense amplifier. So retention tests must use both data patterns.
- **The measured dV is larger than predicted.** Your Cbl is smaller than its label. X7R capacitors lose much of their capacitance under DC bias. Measure, don't trust.

---

## 11. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| dV ≈ 0 for every Cbl | Wordline never opens: CD40109B VDD missing, enables in the wrong state, or the gate on the wrong pin | Measure the wordline with the multimeter while the firmware holds it on |
| dV ≈ 0, and the bitline reads 1.65 V during sensing | The bitline is not floating: a pull resistor is on, or the second GPIO is still driven | Check `tristate()`; measure the bitline with the GPIOs set as inputs |
| Comparator says 1 for everything | VREF is wrong, or the comparator's inputs are swapped | VREF should be ~1.65 V; + input = BL |
| A '1' holds less than 1 s on every cell | Leakage path: flux, fingers, breadboard contact, an unpowered op-amp, or a GPIO on the node | Section 6.3. Re-run the floor test |
| Retention differs run to run with no pattern | Humidity, temperature drift, or dielectric absorption of the capacitor | Log humidity; use C0G or film; let the board settle 10 min after power-up |
| Readings are noisy | ADC noise | Turn on GP23 low-ripple mode, raise `N_AVG`, keep the ADC wires short |
| Pico 2: the floating bitline drifts toward ~2.2 V | RP2350 erratum E9 (A2 stepping) | Use an RP2040 Pico or an A4-stepping Pico 2 |
| The bitline drifts in the float test (step 3b) | A GPIO pull left on, a leaky comparator or follower input, or flux on the bitline | Check `tristate()`, clean, re-run `float` |
| The script stops with "set point not reached" | Heater not powered, fuse open, MOSFET wired wrong, sensor off the board, or gaps in the box | Check the adapter, the fuse and the gate drive with the multimeter. Use a 2-3 L box and tape the gaps. Do not use a smaller or thicker-walled box: if control fails, it gets hotter. Never raise the voltage above 12 V |

---

## 12. Sources

Evidence tags:
- [DATASHEET] = manufacturer data;
- [REPORTED] = paper, press, distributor or search snippet;
- [ESTIMATE] = calculation in `bench_calcs.py`;
- [MODEL] = the study's model;
- [UNVERIFIED] = could not confirm.

Web pages were read through search snippets on 2026-11-03; some hosts were blocked, so a few datasheets could not be opened in full. Prices are approximate as of November 2026.

1. ALD1106 IDS(OFF) 10 pA typ / 400 pA max at VDS 12 V, 1 nA / 4 nA at 125 °C; IGSS 0.1 pA / 10 pA; "consists of junction leakage currents"; gate threshold 0.4 / 0.7 / 1.0 V at IDS = 1 µA [DATASHEET, via snippet]: https://www.electronicsdatasheets.com/download/120482.pdf?format=pdf, https://web.ece.ucsb.edu/Faculty/rodwell/Classes/ECE137B/datasheets/ALD1106.pdf (also https://www.aldinc.com/pdf/ALD1106.pdf)
2. ALD1106 distributor attributes: RDS(on) 500 Ω at 5 V, threshold listed as 1 V [REPORTED]: https://www.lcsc.com/product-detail/C3289693.html
3. ALD1106PBL "MOSFET 4N-CH 10.6V 14DIP", $2.90 at quantity 1 (broker) [REPORTED]: https://www.smbom.com/product/ald1106pbl-16467559
4. 2N7000 VGS(th) 0.8 / 2.1 / 3.0 V; Ciss 20 pF typ / 50 pF max (older sheet 60 pF max); Crss 4 pF typ / 5 pF max; IDSS 1 µA max at 48 V [DATASHEET]: https://www.onsemi.com/download/data-sheet/pdf/2n7000-d.pdf
5. LMC6482 input current 0.02 pA typ / 4 pA max; specified at 3 V, 5 V and 15 V; rail-to-rail; PDIP-8 [DATASHEET]: https://www.ti.com/product/LMC6482
6. MCP6541 / MCP6544 bias current 1 pA, 1.6-5.5 V, push-pull, 600 nA per comparator, PDIP [REPORTED, distributor listings]: https://futureelectronics.com/fr/p/semiconductors--analog--comparators/mcp6544-i-p-microchip-1851997 and https://au.rs-online.com/web/p/comparators/0598251
7. CD40109B quad low-to-high level shifter, VCC 3-18 V, no VDD-first sequencing needed; a low on an ENABLE input puts that output in high impedance [REPORTED]: https://www.ti.com/product/CD40109B, https://www.ti.com/product/es-mx/CD40109B-MIL and https://www.radiolocman.com/datasheet/data.html?di=285989
8. KEMET C0G insulation resistance at 25 °C: 1,000 MΩ·µF or 100 GΩ, whichever is lower [DATASHEET]: https://mfgdatasheets.nlight.net/Kemet%20C0G.pdf
9. DS18B20 ±0.5 °C from -10 to +85 °C, 750 ms 12-bit conversion [DATASHEET]: https://www.analog.com/products/DS18B20 and https://wcm-cce.cldnet.analog.com/media/cn/technical-documentation/data-sheets/2812.pdf. Adafruit 381 is the waterproof DS18B20 probe, $9.95 [REPORTED]: https://www.adafruit.com/product/381
10. RP2040 ADC ENOB 8.7 [REPORTED]: https://pigweed.googlesource.com/third_party/github/raspberrypi/pico-sdk/+/d0c7642369b91c934b014134c862000eee1dbca4%5E%21
11. RP2040 ADC input pull-up pitfall (reading ~30% low through 47 kΩ) [REPORTED, forum]: https://forum.micropython.org/viewtopic.php?p=55650
12. RP2040 ADC DNL spikes at codes 512/1536/2560/3584 [REPORTED]: https://hackster.io/news/raspberry-pi-confirms-it-is-investigating-a-flaw-in-the-raspberry-pi-pico-rp2040-adc-95c393b55dfb and https://github.com/kitanokitsune/rp2040adc_correction
13. RP2350-E9 redefined as input-mode leakage when the pad sits between logic levels [REPORTED]: https://hackaday.com/2024/09/04/the-worsening-raspberry-pi-rp2350-e9-erratum-situation/ and https://hackster.io/news/a-surprise-hardware-bug-in-raspberry-pi-s-rp2350-leads-to-unexpected-pull-down-behavior-76b51ec22ede
14. RP2350 A4 stepping fixes E9; mixed stock [REPORTED]: https://support.thepihut.com/hc/en-us/articles/29618349405469-When-will-you-stock-the-A3-A4-stepping-RP2350-Raspberry-Pi-Pico-2 and https://www.cnx-software.com/?p=154587
15. Real-DRAM cell numbers (5.42 fF cell, 34.7 fF bitline, 71 mV signal, 46 fJ refresh per bit, retention halves per ~10 °C) [MODEL]: [`models/dram_cell_physics.py`](../models/dram_cell_physics.py)
16. raw-ber-contract ~9x refresh saving, kill line incl. VRT [MODEL]: [`dossiers/raw-ber-contract.md`](../dossiers/raw-ber-contract.md), [`DRAM_MOONSHOT_REPORT.md`](../DRAM_MOONSHOT_REPORT.md) section 1
17. All [ESTIMATE] numbers: [`code/T1_pico/bench_calcs.py`](code/T1_pico/bench_calcs.py) (run `--selftest` to check the formulas). The ECC-gain resolution of the coarse and fine schedules: [`code/T1_pico/analyze_t1.py`](code/T1_pico/analyze_t1.py) `--selftest`.
18. IRLZ44N VGS(th) 1.0-2.0 V at 250 µA, RDS(on) ≤ 0.035 Ω at VGS = 4.0 V [DATASHEET, via snippet]: https://www.infineon.com/assets/row/public/documents/non-assigned/49/infineon-irliz44n-ds-en.pdf and https://www.thierry-lequeu.fr/data/IRLZ44N.pdf
19. Isopropanol SDS hazard statements H225, H319, H336 [REPORTED, supplier SDS]: https://www.vanderbilt.edu/vinse/facilities/safety_data_sheets/Isopropanol.pdf
20. DRAM Bender on Xilinx/BittWare DDR4 boards, DDR3/DDR4/HBM2 support, ~$14k per station in the study's budget [MODEL / REPORTED, via the dossier]: [`dossiers/raw-ber-contract.md`](../dossiers/raw-ber-contract.md) (DRAM Bender facts and budget table)
21. `mpremote run` follows the board's output and does not forward keyboard input; exiting sends Ctrl-B, not Ctrl-C (mpremote 1.29.0 source, `commands.py` and `transport_serial.py`) [REPORTED, read during this guide's review]: https://pypi.org/project/mpremote/
22. [UNVERIFIED]: Pico price; ALD1106 and CD40109B pin numbers; RP2040 GPIO input-leakage spec (measure it with the float test); silica-gel indicator chemistry; a hobby-priced DDR3 FPGA retention tester; current shuttle availability; 0.1% resistor and USB isolator prices.
