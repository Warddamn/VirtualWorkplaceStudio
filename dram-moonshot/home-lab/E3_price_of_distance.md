# E3: The price of distance

*Track T1, bench electronics. Written 2026-11-03. Prices are approximate as of November 2026.*

**Goal.** Measure, with a Pico and a multimeter, the law behind the BEST BET's ~10x energy claim. Every time a wire switches, the supply pays

**E = C·V² per charge-and-discharge cycle**

C is the wire's capacitance, and it grows with length. Then follow the same law from your 3 m cable down to a 1 µm chip bond. You will see where "0.37 vs 3.95 pJ/bit" comes from, and what part of it a bench can and cannot check.

| | |
|---|---|
| **Difficulty** | 2 of 5 |
| **Time** | Build: 2-3 h. Measuring: 1-2 h. Half a day |
| **Cost tier** | $ (about $15-30, plus the core kit from [E1](E1_bit_on_the_bench.md) section 5.1; +~$40 for an optional USB power meter) |
| **Board** | Raspberry Pi Pico or Pico 2 (both fine here) |
| **Code** | [`code/T1_pico/e3_energy.py`](code/T1_pico/e3_energy.py), [`analyze_t1.py`](code/T1_pico/analyze_t1.py) `energy`, [`bench_calcs.py`](code/T1_pico/bench_calcs.py) `--section e3` |

**Acronyms.**
- **HBM:** high-bandwidth memory, the DRAM stacks beside today's AI chips.
- **PHY:** the physical-layer input/output circuit at each end of a chip-to-chip link.
- **NoC:** network-on-chip, the wiring that carries data across a processor.
- **SM:** streaming multiprocessor, one compute block of a GPU.
- **TSV:** through-silicon via.
- **PWM:** pulse-width modulation.
- **SPI:** serial peripheral interface.
- **SRAM:** static random-access memory, the Pico's on-chip memory.
- **C0G:** stable ceramic capacitor dielectric.
- **ADC:** analog-to-digital converter.
- **DMM:** digital multimeter.

---

## 1. Why this experiment matters to the study

The BEST BET ([hot-side-memory](../dossiers/hot-side-memory.md)) claims ~10x lower energy per bit delivered than HBM: **0.37 vs 3.95 pJ/bit** [MODEL]. The dossier is clear that this comes "from geometry (no PHY/interposer/TSV path), not heroic cell physics" ([decision.json](../research/stage3/decision.json)).

- **HBM path.** Each bit leaves the DRAM, crosses a PHY, millimetres of interposer and a stack of vias, then 8 mm of on-chip wiring to the compute block.
- **Hot-side path.** Each bit crosses ~1 µm of bond and ~3 mm of on-chip wire.

**What E3 lets you do.** Measure the physics that makes distance expensive, on your own bench. Then check, line by line, how the study's model turns that physics into 0.37 and 3.95.

---

## 2. First principles and the numbers to expect

All numbers below come from `python3 code/T1_pico/bench_calcs.py --section e3`.

### 2.1 The law

**Charging.** Charging a capacitance C from 0 to V moves charge Q = C·V out of the supply, at voltage V. The supply therefore delivers

```
E_supply = Q·V = C·V²     (half ends up stored in C, half heats the resistance in the path)
```

**Discharging.** Discharging dumps the stored half as heat in the pull-down. So **one full cycle (0 → V → 0) costs C·V²**, whatever the resistance. A square wave at frequency f draws an average current of

```
I = C · V · f            → at 3.3 V and 1 MHz: 3.30 µA per pF
```

**Three predictions you will test.**
1. **Current rises linearly with frequency.** Energy is paid per transition, not per second.
2. **Energy per cycle scales as V².**
3. **Energy per cycle does not depend on the series resistance** (as long as each half-cycle settles). Numerical check: charging 100 pF to 3.3 V through 33 Ω, 330 Ω or 3,300 Ω draws the same 1.09 nJ from the supply every time, and the resistor always burns 0.545 nJ.

### 2.2 Expected readings

Setup: 3.3 V buffer, 100 Ω low-side shunt, 1 MHz.

| Load | C | E per cycle (C·V²) | Per random bit (~C·V²/4) | Extra current at 1 MHz | Extra shunt voltage | Highest f that still settles (33 Ω series) |
|---|---|---|---|---|---|---|
| Open buffer output (baseline) | ~0 extra | — | — | — | — | — |
| 10 cm hook-up wire | ~2 pF [ESTIMATE] | 22 pJ | 5 pJ | 6.6 µA | 0.66 mV | very high |
| 10 cm PCB trace, 50 Ω | ~12 pF [ESTIMATE] | 132 pJ | 33 pJ | 40 µA | 4.0 mV | ~80 MHz |
| **1 m RG-58 coax** | **101 pF** [DATASHEET] | **1.10 nJ** | 275 pJ | **333 µA** | **33.3 mV** | ~10 MHz |
| **3 m RG-58 coax** | **303 pF** | **3.30 nJ** | 825 pJ | **1.00 mA** | **100 mV** | ~3 MHz |
| 100 pF C0G (calibration) | 100 pF | 1.09 nJ | 272 pJ | 330 µA | 33.0 mV | ~10 MHz |
| 330 pF C0G (calibration) | 330 pF | 3.59 nJ | 898 pJ | 1.09 mA | 109 mV | ~3 MHz |
| 1 nF C0G (calibration) | 1 nF | 10.9 nJ | 2.7 nJ | 3.3 mA | 330 mV | ~1 MHz; **use ≤250 kHz** |

**Frequency sweep on 1 m of RG-58:**

| Frequency | Extra current | Shunt voltage |
|---|---|---|
| 100 kHz | 33 µA | 3.3 mV |
| 250 kHz | 83 µA | 8.3 mV |
| 500 kHz | 167 µA | 16.7 mV |
| 1 MHz | 333 µA | 33.3 mV |
| 2 MHz | 667 µA | 66.7 mV |

**Voltage sweep, 1 m of RG-58** (2.0 V is the lowest supply the SN74AHC125 is specified for [DATASHEET]):

| Supply | E per cycle | Relative to 3.3 V |
|---|---|---|
| 2.0 V | 404 pJ | **0.37x** |
| 2.5 V | 631 pJ | **0.57x** |
| 3.3 V | 1.10 nJ | 1.00x |

**Can you resolve it?**
- **DMM.** 0.1 mV on the 100 Ω shunt is 1 µA, or 0.3 pF at 1 MHz.
- **FNB58 USB power meter.** Its reported resolution is 10 µA, about 3 pF at 1 MHz on the 3.3 V side [REPORTED]. Resolution is not accuracy, and the last digits are noise.

### 2.3 From the bench to the chip: one law, eight orders of magnitude

The study's model charges each bit **0.5 × C × V²**. That is its "activity" convention. Strict accounting for random data gives 0.25 × C × V². Ratios between paths do not depend on the choice.

| Path | C | V | E per bit (0.5·C·V²) |
|---|---|---|---|
| 3 m RG-58 (your bench) | 303 pF | 3.3 V | 1.65 nJ |
| 1 m RG-58 (your bench) | 101 pF | 3.3 V | 550 pJ |
| 10 cm PCB trace | 12 pF | 3.3 V | 66 pJ |
| A microcontroller pin and pad | ~5 pF | 3.3 V | 27 pJ |
| **HBM path, "equivalent capacitance"** | 14 pF | 0.75 V | **3.95 pJ** |
| 8 mm on-chip wire (HBM PHY → SM) | 1.6 pF | 0.75 V | 0.45 pJ |
| **Hot-side path delivered, "equivalent capacitance"** | 1.33 pF | 0.75 V | **0.37 pJ** |
| 1 mm on-chip wire | 0.2 pF | 0.75 V | 56 fJ |
| Hybrid bond + via stack | 10 fF | 0.75 V | 2.8 fJ |
| Oxide storage node | 0.15 fF | 0.6 V | 0.027 fJ |

Top to bottom: 1.65 nJ ÷ 0.027 fJ = 6.1e7, which is 7.8 orders of magnitude [ESTIMATE].

**Two surprises hide in this table.**
1. **Capacitance per millimetre is not the difference.** An on-chip wire has *more* capacitance per millimetre (0.2 pF/mm [MODEL input]) than coax (0.1 pF/mm). Chips win by being **short** and running at **low voltage**. Coax at 3.3 V costs (3.3/0.75)² ≈ 19x more per pF than a 0.75 V chip wire.
2. **HBM's 3.95 pJ is not one long wire.** It is "equivalent" to driving ~14 pF at 0.75 V, but most of it is PHY circuitry: drivers, receivers, termination, clocking. E3 tests the law that makes distance and voltage expensive. It does not test the PHY's internal design.

### 2.4 Where 0.37 vs 3.95 comes from, line by line

`bench_calcs.py` re-implements `models/hot-side-memory.py` (post-red-team inputs). Its self-test confirms it reproduces the dossier's numbers.

**Near-tier read, at the memory port.**

| Item | Energy |
|---|---|
| Bitlines: (8.1 fF local + 126 fF global) × 0.9 V × 0.3 V swing | 36.2 fJ per cell read (2 bits) |
| Cell read per bit: (36.2 bitline + 9.0 sense + 0.2 wordline) ÷ 2 bits | 22.7 fJ |
| Decode | 2.0 fJ |
| Local data wire 0.1 mm | 8.1 fJ |
| Bond + via | 2.8 fJ |
| All of that ×2 for unmodelled periphery, plus 50 fJ controller/SRAM | **0.121 pJ/bit** |

Check: (22.7 + 2.0 + 8.1 + 2.8) × 2 + 50 = 121 fJ.

**Write, mix and delivery.**
- **Write-verify (2 bits, 3 loops):** 0.543 pJ/bit. A 20% write mix gives **0.206 pJ/bit** at the port.
- **Delivery wire:** 0.5 × 0.2 pF/mm × 0.75² = **56 fJ per bit per mm**.

**The totals.**

| Path | Port energy | Delivery | Delivered |
|---|---|---|---|
| Hot side | 0.206 pJ | + 3 mm × 0.056 = 0.169 | **0.374 pJ/bit** |
| HBM | 3.5 pJ at the PHY [REPORTED in the dossier] | + 8 mm × 0.056 = 0.45 | **3.95 pJ/bit** |

**Ratio: 10.6x.**

**Where the energy goes.**
- In HBM, 89% of the energy is the PHY, interposer and TSV path, and 11% is on-chip delivery.
- In the hot side, ~45% is the 3 mm of on-chip delivery wire and ~55% is the memory array and its controller.

**The lesson.** Once the off-chip hop is gone, *on-chip distance* becomes the biggest single cost. That is why the dossier says data placement next to its compute block matters: 5.5x if placement is random, 15x at 1 mm.

### 2.5 SPI to an external chip vs the Pico's own SRAM (qualitative)

**SPI pins.** Each SPI line is ~16 pF: pin and pad ~5 pF, the other chip's input ~7 pF, a short wire. The clock toggles every bit, and data rises on about a quarter of bits:

E ≈ (16 + 0.25 × 16) pF × 3.3² ≈ **218 pJ per bit** [ESTIMATE]

**What a meter sees.** At 8 Mbit/s that is ~1.7 mW: ~0.53 mA on the 3.3 V rail, or **~0.41 mA at the 5 V USB input** (assuming an ~85% efficient regulator [UNVERIFIED]). A 10 µA USB meter can see it.

**Internal SRAM.** About 1-10 pJ per 32-bit access in a 40 nm-class chip [ESTIMATE], or ~0.16 pJ per bit. That is **~1,000x less than the pins**. At the copy speed the script prints (for example 20 MB/s), the SRAM arrays themselves should add only ~12 µA at the USB input. The copy loop's CPU and bus work will probably add more (tens to hundreds of µA), and it can even shift the current by a few mA either way compared with the idle loop, because the processor runs different code [ESTIMATE]. That is logic energy, not memory-array energy. Per bit, the copy still comes out far below loaded SPI, because it moves roughly 30-100x more bits per second than 10 MHz SPI [ESTIMATE].

**The lesson.** Leaving the chip costs ~100-1,000x more per bit than staying on it. A microcontroller shows the same off-chip-vs-on-chip gap that HBM-vs-hot-side shows on a GPU.

---

## 3. Honest scope

| What E3 proves | What E3 does NOT prove |
|---|---|
| E = C·V² per cycle, linear in frequency, independent of series resistance | The 0.37 or 3.95 pJ/bit values (they come from a model with PHY, controller and periphery assumptions) |
| Energy scales with capacitance, and capacitance with length (1 m vs 3 m of coax) | On-chip wire capacitance values, or the energy of a real PHY (SerDes, termination, clocking) |
| Energy scales as V² (why chips push to 0.75 V and why the hot-side bitline swings only 0.3 V) | Anything about the memory cell, retention or density |
| Off-chip bits cost ~100-1,000x on-chip bits (SPI vs SRAM, qualitative) | That a real hot-side chip would reach 0.37 pJ/bit, or the ~90 W per GPU saving |

**How it scales up.**

| Step | Where | What it adds | Rough cost |
|---|---|---|---|
| 1. This bench | Home | The law, measured; your analysis code | $15-70 |
| 2. On-chip wires, measured | Home: an FPGA board (field-programmable gate array). Compare short vs long routed nets, and block RAM vs external memory, with a USB meter | Real on-chip capacitance per mm, at real core voltage | $30-150 for an FPGA board [ESTIMATE] |
| 3. Test structures on silicon | Multi-project-wafer shuttle: wire-length ladders and a toy bonded link | pF/mm and fJ/bit/mm on a real process | Varies [UNVERIFIED] |
| 4. Bitline and sense energy of oxide arrays | The study's Gate B (logic-side measurements on bonded coupons) | The dossier's downgrade line: "> 0.9 pJ/bit at the port" kills the 4x claim | Study budget |

---

## 4. Safety

> **SAFETY: E3**
> - **Voltages.** Only USB 5 V and the Pico's 3.3 V. The optional voltage sweep uses an adjustable low-voltage regulator module fed from USB, set between 2.0 and 3.3 V. Set the module's output with the multimeter, with nothing attached, before connecting the buffer. No mains-powered builds.
> - **USB power meter (FNB58).** It can "trigger" fast-charge modes (QC/PD) that raise the USB voltage to 9-20 V [REPORTED, it is sold as a fast-charge tester]. The Pico's VSYS input is rated 5.5 V maximum [DATASHEET, Raspberry Pi Pico]. Never open the meter's trigger or protocol menu with the Pico attached. Plug the meter into a computer USB port, not a fast charger. Check that it reads about 5.0 V with nothing attached, then plug in the Pico. Never use it on modified chargers or anything mains-side.
> - **Children and pets.** Keep them away from the bench while the iron is hot. Store small parts and capacitors out of their reach: they are choking hazards.
> - **Buffer limits.** Keep the buffer's supply at or below its rated maximum (check the datasheet). Use the 33-100 Ω series resistor, so that driving 1 nF does not overload the output.
> - **Cables.** Long coax on the floor is a trip hazard. Tape it down or keep it on the bench.
> - **Soldering.** Same rules as [E1](E1_bit_on_the_bench.md) section 4: iron ~350 °C, stand, ventilation, safety glasses.

---

## 5. Parts and tools

Shared core kit: [E1](E1_bit_on_the_bench.md) section 5.1 (Pico or Pico 2, breadboard, DMM with a 600 mV range).

| Part | Spec that matters | Example part number | Approx. USD | Where to buy |
|---|---|---|---|---|
| Line driver | CMOS buffer; VCC 2.0-5.5 V; inputs accept 0-5.5 V at any VCC, so the Pico's 3.3 V drive is fine when the buffer runs at 2.0 or 2.5 V [DATASHEET] | SN74AHC125N (PDIP-14), or 74HC125 at 3.3 V only | 0.5-1 [ESTIMATE] | DigiKey, Mouser |
| Shunt | 100 Ω 1% metal film, low side | | — | |
| Shunt filter | 10 kΩ + 10 µF (averages the pulses; τ = 0.1 s) | | — | |
| Supply monitor divider | 100 kΩ ×2 | | — | |
| Decoupling | 10 µF + 100 nF at the buffer | | — | |
| Series resistors | 33 Ω (default), 100 Ω and 330 Ω (series-R test) | | — | |
| Calibration loads | C0G, 5%: 100 pF, 330 pF, 1 nF | | 0.2 each | |
| Coax | RG-58, ~101 pF/m nominal (30.8 pF/ft) [DATASHEET]; 1 m and 3 m with BNC ends | any RG-58C/U patch cables | 5-10 each [ESTIMATE] | |
| BNC breakout | BNC-to-clip leads or a panel jack with wires | | 5 [ESTIMATE] | |
| *Optional* USB power meter | ~10 µA resolution [REPORTED]; logging helps. A fast-charge tester: never use its trigger menu with the Pico attached (section 4) | FNIRSI FNB58 | ~€40 / ~$40-45 [REPORTED] | Electronics retailers |
| *Optional* SPI device for Part C | Any SPI chip; e.g. a 1 Mbit SPI SRAM | 23LC1024 (DIP-8) [UNVERIFIED] | 2-4 [ESTIMATE] | DigiKey, Mouser |
| *Optional* voltage sweep | Adjustable regulator module, USB-powered, set to 2.0 / 2.5 / 3.3 V (for a 1.8 V point, use an SN74LVC125A instead: 1.65-3.6 V, 5 V-tolerant inputs [REPORTED]) | LM317- or buck-module class | 2-5 [ESTIMATE] | |

**Tools.**
- DMM, soldering iron, wire strippers.
- Optional: an oscilloscope, to see ringing on the 3 m cable.

---

## 6. Circuit

```
                     Pico 3V3 (or the adjustable module for the V-sweep)
                         |
                   74AHC125 VCC ---+--- 10 uF ---+--- 100 nF ---+
                                   |             |              |
   GP15 (PWM) ---> 1A  [74AHC125]  1Y ---[33 Ohm]---> LOAD centre (cable core / capacitor)
                   1OE -> GND (enabled)              LOAD return (cable shield) -> real GND
                   other 3 channels: inputs -> the buffer's own GND pin (G'), OE -> buffer VCC (disabled)
                   74AHC125 GND pin = node G'
                                   |
   (the decoupling caps return to G')
   G' ---[100 Ohm shunt]--- real GND          <- DMM (600 mV range) across this shunt
   G' ---[10k]---+---> GP26 (ADC0)            <- averaged shunt voltage
                 [10 uF] to real GND
   buffer VCC ---[100k]---+---[100k]--- real GND
                          +---> GP27 (ADC1)   <- V_eff = 2 x ADC1 - V_shunt
```

**Why it measures what we want.**
- **The discharge path.** Every coulomb that charges the load must come back through the buffer's ground pin, and so through the shunt.
- **The reading.** The average shunt current is therefore C·V·f plus the buffer's own switching and leakage current. The baseline load ("open") removes the buffer's own part.

**Simplest path, if you have no buffer chip.**
- Let the Pico's GPIO drive the load directly, with the 33 Ω resistor between the GPIO and the cable core (without it, reflections on the open cable ring past the supply rails).
- Read the whole-board current at the USB plug with the FNB58.
- At 1 MHz, 1 m of RG-58 adds ~0.26 mA at the 5 V input [ESTIMATE].
- This is coarser, but it is the same law.

---

## 7. Procedure

### Part A: the law

1. **Build the circuit.**
   - Measure the 100 Ω shunt with the DMM and write down its real value.
   - Measure each calibration capacitor if your DMM has a capacitance range.
2. **Load the firmware.** Copy `t1_common.py` and `e3_energy.py` to the Pico. Set `LOGFILE = "e3_sweep.csv"` and, if you will read the DMM, `MANUAL_DMM = True`. Run from Thonny.
3. **Baseline.**
   - Leave the output unloaded. Enter label `open`, C = `0`, and press Enter for all frequencies.
   - The script logs a static point (output held low) and then 100 kHz to 2 MHz.
4. **Calibration loads.**
   - Label `100pF`: all frequencies.
   - Label `330pF`: max 2 MHz.
   - Label `1nF`: max **250000** Hz.
5. **Cables.** Label `1m_RG58`, then `3m_RG58`. Clip the core to the series resistor and the shield to real ground. Leave the far end open.
6. **Short wires.** Label `10cm_wire`, and a PCB trace if you have one. These signals are tiny; average carefully or use the DMM.
7. **Analyze.**
   - Run `python3 analyze_t1.py energy e3_sweep.csv`, or add `--use-dmm` to use your typed readings.
   - For each load you get C_tot (from the slope of current vs frequency), C_load = C_tot − C_open, R² of the line, the ratio to nominal, and the energy per cycle.

### Part B: the three predictions

8. **Linearity in frequency.** Check that R² ≥ 0.995 for each load in step 7.
9. **Series resistance does not matter.**
   - With the 330 pF load, log label `330pF_R33` (33 Ω series) and then `330pF_R330` (330 Ω).
   - For BOTH, enter **500000** as the highest frequency. The 330 Ω run has τ = (330 + ~40) Ω × 330 pF ≈ 122 ns and settles (7τ per half-period) only below ~580 kHz. Swept to 2 MHz, its fitted C comes out ~24% low, and you would wrongly conclude that energy depends on R [ESTIMATE, `bench_calcs.py` E3.4].
   - Energy per cycle should agree within ±5%.
   - Then, as a separate demonstration, log `330pF_R3300` (3.3 kΩ) with highest frequency 1000000. It cannot settle (τ ≈ 1.1 µs against a 0.5 µs half-period at 1 MHz), so the current-vs-frequency curve bends over and the "energy" drops. Why? The swing never reaches full V.
10. **Energy ∝ V² (optional).**
    - Set the adjustable module to 2.0 V with the multimeter, nothing attached. Then power the buffer from it at 2.0 V and then 2.5 V (repeat 3.3 V from the Pico).
    - Run the 1 m RG-58 load at each voltage. The script records the effective voltage.
    - Fit log(E) vs log(V). The slope should be 2.

### Part C: off-chip vs on-chip (qualitative)

11. **Set up the meter.** Plug the USB power meter into a computer USB port (not a fast charger) and check it reads about 5.0 V with nothing attached. Do not open its trigger or protocol menu. Then plug in the Pico, and turn on the meter's logging or averaging.
12. **Run the phases.**
    - Set `MODE = "spi"` and run. The script runs three 20 s phases with 3 s gaps: `idle_busy`, `sram_copy` and `spi_write` (10 MHz).
    - It prints the bytes per second of each phase. Note the meter's average current for each phase.
13. **Repeat with a load.** Run again with 100 pF from the SPI clock pin (GP18) to ground, or with an SPI chip connected. The clock pin then switches ~100 pF more at 10 MHz: expect ~3.3 mA on the 3.3 V side (~2.6 mA at USB [ESTIMATE]).
14. **Compute.** Energy per byte = (I_phase − I_idle) × 5 V ÷ (bytes per second). Compare SPI (unloaded, loaded) with SRAM copy.
    - **Expected order, per bit:** loaded SPI ≫ unloaded SPI ≫ SRAM copy. The SRAM-copy phase may draw a few mA more or less than idle, because the processor runs different code. That current is the processor, not the memory. Per bit the copy is still far cheaper, because it moves roughly 30-100x more bits per second than 10 MHz SPI [ESTIMATE].

---

## 8. Data sheet / log template

**Run header:**

| Date/time | Board | Buffer part | Buffer supply (V) | Shunt measured (Ω) | Series R (Ω) | File | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Energy table:**

| Load label | Nominal C (pF) | Measured C_load (pF) | R² | Measured ÷ nominal | E per cycle (nJ) | E per cycle predicted (nJ) |
|---|---|---|---|---|---|---|
| open | 0 | (baseline) | | — | — | — |
| 100pF | 100 | | | | | 1.09 |
| 330pF | 330 | | | | | 3.59 |
| 1nF | 1000 | | | | | 10.9 |
| 1m_RG58 | 101 | | | | | 1.10 |
| 3m_RG58 | 303 | | | | | 3.30 |

**Part C:**

| Phase | Mean USB current (mA) | Δ vs idle (mA) | Bytes/s | Energy per byte (pJ) | Energy per bit (pJ) |
|---|---|---|---|---|---|
| idle_busy | | 0 | — | — | — |
| sram_copy | | | | | |
| spi_write (unloaded) | | | | | |
| spi_write (loaded) | | | | | |

**CSV columns written by the Pico (sweep):** `exp, mode, label, c_nom_pF, f_hz, v_shunt, i_a, v_eff, dmm_mV`

---

## 9. Pass / fail criteria

| # | Test | Pass |
|---|---|---|
| 1 | Linear in frequency | R² ≥ 0.995 for every load (within its settling limit) |
| 2 | Calibration capacitors | Measured C within ±10% of nominal for 100 pF, 330 pF and 1 nF |
| 3 | Cable length | 1 m and 3 m RG-58 within ±20% of 101 / 303 pF; 3 m ÷ 1 m = 3.0 ± 0.3 |
| 4 | Series R | E per cycle with 33 Ω and 330 Ω equal within ±5%, both swept only up to 500 kHz (step 9) |
| 5 | V² (optional) | Exponent 2.0 ± 0.15 |
| 6 | Off-chip vs on-chip (qualitative) | Loaded SPI costs clearly more per bit than the SRAM copy |

---

## 10. What would surprise you (and why it would matter)

- **The energy changes with series resistance at a frequency that should settle.** Then something besides C·V² is happening, such as shoot-through current in the buffer that depends on edge speed. Real I/O circuits fight this too.
- **The 3 m cable measures more than 3x the 1 m cable, or C rises with frequency.** Reflections and ringing add extra transitions. A long line is a transmission line, not a lumped capacitor, which is one reason real PHYs use termination and pay static power for it.
- **The static current (output held low) changes when a load is attached.** The load has a DC leak, such as a scope probe's 1 MΩ or a dirty connector.
- **SPI with nothing attached costs almost as much as with a chip attached.** The pad and I/O ring dominate, not the wire. That supports the picture that HBM's 3.5 pJ is mostly PHY, not distance.

---

## 11. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Current does not change with frequency | The buffer output is not switching (OE not enabled, wrong pin) | Check 1OE = GND; scope or DMM-AC the output |
| Readings jump around | The ADC filter is too short, or the USB supply is noisy | Wait longer (`SETTLE_MS`), average more, turn on low-ripple mode (GP23) |
| Measured C ≈ 2x nominal for every load | You are measuring both edges in a way that double-counts, or the shunt value is wrong | Measure the real shunt value; check `R_SHUNT` in the script |
| Negative C_load | The baseline was taken at a different supply voltage or temperature | Re-run "open" right before each load |
| The 1 nF load reads low at high frequency | It is not settling | Use ≤250 kHz, as the script prompt suggests |
| Buffer gets warm | The load is too large, or there is no series resistor | Use 100 Ω series for ≥1 nF |
| Unused 74AHC125 inputs make the baseline drift | Floating CMOS inputs draw current | Tie unused inputs to the buffer's own GND pin (G', which sits 0.1-0.3 V above real ground during the sweep) and their OE pins to the buffer's VCC |
| The 330 Ω run reads a lower C than the 33 Ω run | The sweep went above the 330 Ω settling limit | Re-run with highest frequency 500000 (step 9) |

---

## 12. Sources

Evidence tags:
- [DATASHEET] = manufacturer data;
- [REPORTED] = paper, press, distributor or search snippet;
- [ESTIMATE] = `bench_calcs.py`;
- [MODEL] = study model;
- [UNVERIFIED] = not confirmed.

Read through search snippets on 2026-11-03. Prices are approximate as of November 2026.

1. Hot-side vs HBM energy per bit, 0.37 vs 3.95 pJ/bit, port 0.121 / 0.543 / 0.206 pJ, 56 fJ/mm delivery, placement sensitivity [MODEL]: [`dossiers/hot-side-memory.md`](../dossiers/hot-side-memory.md) section 2; [`models/hot-side-memory.py`](../models/hot-side-memory.py); [`research/stage3/decision.json`](../research/stage3/decision.json)
2. HBM 3.5 pJ/bit at the PHY, as cited by the study model: arXiv 2602.18568 (HBM3E 3.44 pJ/b) and 36kr (HBM4 3-4 pJ/b) [REPORTED, via the model's input table; arxiv.org is blocked here and was not re-opened]: https://arxiv.org/pdf/2602.18568, https://eu.36kr.com/en/p/4002393085071497
3. RG-58C/U nominal 30.8 pF/ft (~101 pF/m); other variants 82-106 pF/m [DATASHEET / REPORTED]: https://www.fairviewmicrowave.com/content/dam/infinite-electronics/product-assets/fairview-microwave/product-datasheets/RG58CU-FT.pdf and https://www.webb.co.za/wp-content/uploads/2021/10/RG-58.pdf
4. FNIRSI FNB58 current resolution 0.00001 A; accuracy ±(0.5‰ + 2 digits) per retailers; "resolution is not accuracy" [REPORTED]: https://core-electronics.com.au/fnirsi-fnb58-usb-fast-charge-tester.html, https://www.elektormagazine.com/review/fnirsi-fnb58-review, price ~€40: https://eleshop.eu/fnirsi-fnb58-usb-tester-with-bluetooth.html
5. Pico 2 launched at $5 (August 2024) [REPORTED]: https://eetimes.itmedia.co.jp/ee/articles/2408/09/news079.html
6. RP2040 ADC ENOB 8.7 [REPORTED]: https://pigweed.googlesource.com/third_party/github/raspberrypi/pico-sdk/+/d0c7642369b91c934b014134c862000eee1dbca4%5E%21
7. All [ESTIMATE] numbers, including the numeric RC-energy check, the settling-limit table and the replay of the hot-side model: [`code/T1_pico/bench_calcs.py`](code/T1_pico/bench_calcs.py) `--section e3` and `--selftest`.
8. SN74AHC125: recommended VCC 2-5.5 V; inputs rated 0-5.5 V at any VCC [DATASHEET]: https://www.ti.com/lit/gpn/sn74ahc125. SN74LVC125A 1.65-3.6 V with 5 V-tolerant inputs [REPORTED]: https://www.ti.com/product/SN74LVC125A
9. Raspberry Pi Pico VSYS input 1.8-5.5 V [DATASHEET]: https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
10. [UNVERIFIED]: SN74AHC125N DIP availability; FNB58 trigger voltages (9-20 V is the usual QC/PD range); Pico regulator efficiency (85% assumed); SRAM energy per access in the RP2040 (1-10 pJ per 32-bit word assumed); CPU current difference between the copy and idle loops; hook-up-wire and PCB pF/m (calculated from geometry, not measured); 23LC1024 price; FPGA board and shuttle costs.
