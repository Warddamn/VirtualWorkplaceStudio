# E1: A bit on the bench

*Track T1, bench electronics. Written 2026-11-03. Prices are approximate as of November 2026.*

**Goal.** Build one bit of DRAM (dynamic random-access memory) from a transistor and a capacitor, then grow it into a 16-bit array. Use them to measure the three facts that shape every DRAM chip:
1. Reading a bit shares its charge with the bitline and destroys it.
2. The stored charge leaks away, and faster when warm.
3. Refresh and error correction keep the data anyway.

| | |
|---|---|
| **Difficulty** | Part A (one cell): 3 of 5. Part B (4 x 4 array): 4 of 5 |
| **Time** | Part A: one day (4-6 h build, 2-4 h measuring). Part B: a second weekend, plus overnight runs. Each temperature point: 1-3 h |
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

**Expected** (Cs 1 nF, Cbl 4.7 nF): **+288 → +50 → +8.8 → +1.5 mV** (ratio 0.175 per read).

That is why every DRAM read ends with a restore: the sense amplifier drives the bitline back to full rail while the wordline is still open.

### 2.3 Threshold-voltage loss: why DRAM boosts its wordline

**The physics.** An n-channel MOSFET passes a high voltage only up to about V_gate − Vth. Vth (threshold voltage) also rises as the source rises (the body effect).

**Expected** with an ALD1106 (Vth ≈ 0.7 V [UNVERIFIED typical], body effect γ ≈ 0.5 √V [ESTIMATE]):

| Wordline high | Highest '1' you can store | Vth at that point |
|---|---|---|
| 3.3 V (no boost) | **2.17 V** | 1.13 V |
| 9 V (boosted, from a 9 V battery) | **3.30 V** (full) | 1.28 V |

**Effect on the signal.** The unboosted '1' gives only **+91 mV** instead of +288 mV.

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
| 2N7000 (~10 pF, half of its 20 pF input capacitance [DATASHEET Ciss]) | 89 mV | 9 mV |

**Why it matters.** On a chip, Cs is only ~5 fF, so kickback is a real design limit. On the bench it is small, but you can see it.

### 2.5 Law 3: retention = charge budget ÷ leakage

**The law.** Leakage current I drains the node at dV/dt = I/C, so

```
t_retention = Cs × dV_allowed / I_leak
```

**What dV_allowed is.** A '1' still reads correctly while its signal beats the sense amplifier's offset and noise. Budget about 20 mV [ESTIMATE]. With Cs = 1 nF and Cbl = 4.7 nF, the lowest readable '1' is

1.65 + 0.020 × 5.73 = **1.76 V**

So the allowed droop is 3.30 - 1.76 = **1.54 V**.

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
| 2. Retention profiling of real DRAM | Home or makerspace: an FPGA (field-programmable gate array) board plus an open DRAM testing framework such as DRAM Bender (named in the study) | Real cells, real tails, real VRT, millions of cells | Board and setup [UNVERIFIED cost]; the study budgets ~$90-124k for the full Phase 1 with DDR5 testers |
| 3. Temperature-controlled module study | University lab with a thermal chamber | 65-85 °C points and the 1,000 h statistics the kill line needs | Study Phase 1 |
| 4. Your own cell on silicon | Multi-project-wafer shuttle runs on open process kits (SKY130-class) | A real 1T1C or gain-cell test array | Varies by provider [UNVERIFIED current availability and price] |

---

## 4. Safety

> **SAFETY: E1**
> - **Voltages.** Only USB 5 V, the Pico's 3.3 V and one 9 V battery. No mains-powered builds. The optional heater runs from an unmodified, commercially made 12 V DC adapter (≤30 V).
> - **9 V battery.** Never let its terminals touch metal: a shorted 9 V battery gets hot and can start a fire. Store it in its cap or in tape. Take it out of the circuit when you finish.
> - **Soldering.**
>   - The iron tip is about 350 °C. Use a stand, keep the cord clear and never leave a hot iron unattended.
>   - Rosin flux fumes irritate the airways, so work by an open window or with a fume fan.
>   - Lead-free solder is preferred. If you use leaded solder, wash your hands afterwards and keep food away from the bench.
>   - Wear safety glasses: clipped leads fly.
> - **Isopropyl alcohol (IPA, 99%) for cleaning.**
>   - SDS hazards: highly flammable liquid and vapour; causes serious eye irritation; vapour may cause drowsiness [UNVERIFIED: standard IPA SDS classification, not re-checked by search].
>   - Use small amounts, away from the hot iron and any flame. Ventilate. Wear nitrile gloves and safety glasses.
>   - Store it capped, away from heat.
>   - Let small used amounts evaporate outdoors, away from ignition sources, or follow local disposal rules.
> - **Desiccant.** Use non-indicating silica gel, or a cobalt-free orange or green type. Avoid blue-to-pink "cobalt chloride" gel [UNVERIFIED].
> - **Fridge run.**
>   - Seal the electronics in a zip bag with silica gel. Keep it away from food, and wipe the shelf afterwards.
>   - When you take the bag out, leave it sealed for 30 minutes so water does not condense on the cold board.
> - **Warm run.** Keep the board at **≤55 °C**.
>   - **Heater option 1, the resistor heater:** ≤12 V, ~7 W.
>     - Mount the resistors on an aluminium plate.
>     - Put a 72 °C thermal fuse in series.
>     - The firmware cut-off is 55 °C.
>     - Never let the resistors touch foam.
>     - Never leave it running unattended.
>   - **Heater option 2, a hair dryer:**
>     - Use it as sold, on its lowest setting, at least 30 cm away.
>     - Never cover it, and never leave it unattended.
>     - Stop if any plastic softens.
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
| Temperature sensor | ±0.5 °C from -10 to +85 °C [DATASHEET] | DS18B20 (TO-92, or Adafruit 374 waterproof probe) | 3-10 [ESTIMATE] | Adafruit, DigiKey |
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
| Precharge resistors | Matched pair per bitline | 10 kΩ 1% ×10 | — | |
| Reference divider | 1.65 V | 100 kΩ 1% ×2, 1 µF film | — | |
| 9 V battery and clip | VPP for the wordline | | 3-5 | |
| Cleaning | IPA 99%, small brush | | 8 | Pharmacy, hardware store |
| Desiccant and zip bags | For the fridge run | | 5 | |
| *Optional warm box* | ≤12 V adapter, 2× 10 Ω 10 W resistors, logic-level MOSFET (e.g. IRLZ44N [UNVERIFIED gate drive at 3.3 V]), 72 °C thermal fuse, aluminium plate, foam box | | 15-20 [ESTIMATE] | |
| *Optional* hygrometer | Humidity explains many leakage surprises | any | 10 [ESTIMATE] | |

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
   all four substrate (V-) pins -> GND;  CD40109B: VCC = 3V3, VDD = 9 V, enables tied "enabled"
```

**Pin numbers.** Take them for the ALD1106 (G, D, S of each transistor and the V− substrate pin) and the CD40109B (inputs, outputs, enables and their polarity) from the pin diagram and truth table on page 1 of each datasheet. They are deliberately not reproduced here, because this guide could not verify them.

### 6.3 Build rules for low leakage (the part that decides whether it works)

At picoamps, the breadboard is part of your circuit. Follow these rules for every storage node (SN).

1. **Air-wire the storage node.** Bend the ALD1106 source pins outward so they do not enter the breadboard. Solder Cs directly to the bent pin, and put the other leg of Cs into the ground rail. Nothing on the storage node may touch the breadboard plastic.
2. **Clean.** After soldering, scrub flux off the node with IPA and a brush. Let it dry for 10 minutes. Flux and fingerprints are leakage paths.
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
| GPIO leakage | The bitline sits on two GPIO pins. Their input leakage is not in this guide's sources [UNVERIFIED] | The bitline floats for only ~1 ms per read, so 1 nA would shift it by just 0.2 mV. Never connect a GPIO to the storage node |
| Pico 2 (RP2350 A2 stepping) erratum E9 | A pad with its input buffer on, sitting between logic levels, leaks enough to pull toward ~2.2 V [REPORTED]. A floating bitline at 1.65 V is exactly that case | Use an RP2040 Pico, or a Pico 2 confirmed as A4 stepping (reported fixed) [REPORTED] |
| Protection-diode leakage | Every chip input on a node adds its ESD diodes (pA at room temperature, more when warm) | Count inputs: the storage node has only the transistor, Cs and (optionally) one LMC6482 input |

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
   - **Pass:** under ~5 pA. If it is higher, clean and dry the board before going on.
3. **Build Circuit A.**
   - Start with the CD40109B VDD on **3.3 V**, not 9 V.
   - Install the ALD1106, VREF, the comparator, the followers and the DS18B20.
   - Copy `t1_common.py` and `e1_single_cell.py` to the Pico.
4. **See the threshold-voltage loss.**
   - Set `MODE = "peek"` and `PEEK_S = 60`, and run.
   - The peek follower shows the stored '1' settling near **~2.2 V**, not 3.3 V (section 2.3).
   - Move the CD40109B VDD to the **9 V battery** and repeat. The '1' should now reach **~3.3 V**.
   - You have just rediscovered why DRAM needs a boosted wordline.
5. **Charge sharing sweep.**
   - Set `MODE = "share"` and `LOGFILE = "e1_share.csv"`, and run from Thonny.
   - Fit Cbl = 1 nF. Type `1` when asked. The script writes and reads '1' and '0' ten times each, with restore.
   - Repeat for 2.2, 4.7, 10 and 22 nF.
   - Copy the file to the PC and run `python3 analyze_t1.py share e1_share.csv`.
   - Compare with the table in 2.1. The script fits one stray capacitance for the whole sweep.
6. **Destructive read.**
   - Set `MODE = "destructive"` with Cbl = 4.7 nF.
   - Expect +288, +50, +9 and +1.5 mV, then a full signal again after the restore.
   - Run `python3 analyze_t1.py destructive e1_destr.csv`.
7. **Retention at room temperature.**
   - Set `MODE = "retention"` (log-spaced waits from 1 s to 30 min, about 2 h in all).
   - Capture with `mpremote run e1_single_cell.py > e1_ret_room.csv`.
   - Note the wait at which a stored '1' first reads as 0. Also watch the stored '0's.
8. **Optional: how parking the bitline changes retention.** Repeat step 7 with `PARK = "zero"`.
   - A stored '1' then sees 3.3 V across the transistor instead of 1.65 V.
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
    - Run `MODE = "retmap"`. It writes all 1s, waits on a log-spaced schedule from 1 s to 1 h, and reads all 16 cells with no restore.
    - Capture to `e1_retmap_room.csv`.
    - Run `python3 analyze_t1.py retmap e1_retmap_room.csv`. It prints:
      - a 4 x 4 map of retention times;
      - the median, weakest and second-weakest cells;
      - a lognormal σ;
      - the extrapolated 1e-4 quantile with its 90% band;
      - the ECC gain (second ÷ first).
13. **Refresh beats leakage.**
    - Set `T_REF_S` to half the weakest retention from step 12. Run `MODE = "refresh"` for 1 h.
    - Expect **0 errors** with refresh, then errors in the no-refresh copy that runs afterwards.
14. **ECC in miniature.**
    - Run `MODE = "ecc"`. It stores the 11-bit word 0x7FF as a 16-bit Hamming codeword.
    - Find the first wait where `raw_errors ≥ 1` and the first wait where `data_ok = 0`.
    - The ratio is your ECC refresh extension. Compare it with 1.1-1.4x (section 2.7).
15. **Temperature.** Repeat step 12 at three temperatures:
    - **Fridge (~4 °C).** Put the whole board in a sealed bag with silica gel. Pass the USB cable through the door seal. Wait 1 h to equilibrate.
    - **Room temperature.**
    - **Warm box (45 °C).** Set `HEATER_SETPOINT_C = 45.0` and wait 30 min after the set point is reached.
    - Analyze with `python3 analyze_t1.py temp e1_retmap_cold.csv e1_retmap_room.csv e1_retmap_warm.csv`. It fits an activation energy Ea and the "halves every X °C" figure.
16. **Repeat one run** at room temperature on another day. Cells whose retention moved by more than 2x are candidates for variable retention time (section 10).

---

## 8. Data sheet / log template

Keep a paper or spreadsheet log. Each run also produces a CSV file.

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
| 1 | Floor (step 2) | Leakage of capacitor + op-amp + wiring < 5 pA | Clean, dry and air-wire; then retry |
| 2 | Charge-sharing law | Measured dV within ±15% of prediction (with measured capacitors and a fitted stray ≤ 100 pF) for Cbl/Cs from 1 to 22 | Check that the bitline really floats and that VREF is correct |
| 3 | Destructive read | Second-read ÷ first-read signal = Cs/(Cs+Cbl) within ±25% | |
| 4 | Boost | The '1' rises from ~2.2 V to ~3.3 V when VDD goes from 3.3 V to 9 V | |
| 5 | Refresh | Zero errors for 1 h with T_ref ≤ ½ × the weakest retention; errors without refresh | |
| 6 | Temperature | Retention at 45 °C ≥ 2x shorter than at 22 °C, and at 4 °C ≥ 1.5x longer | An informative "fail": your leakage is surface or dielectric, not junction. Find it |
| 7 | ECC | `data_ok = 1` holds at a longer wait than the first raw error | |

---

## 10. What would surprise you (and why it would matter)

- **Retention barely depends on temperature.** The leakage path is then not silicon at all: it is surface water, flux or the capacitor. On a chip, that kind of non-thermal, defect-driven leakage tail is exactly what the study fears for oxide transistors.
- **A cell's retention jumps between runs by 2x or more, with nothing else changed.** That is variable retention time (VRT). Real DRAM has it, and the raw-ber-contract kill line explicitly includes it. Log which cell, how often, and by how much.
- **The weakest of 16 cells is 10x or more below the median.** A heavy tail. Lognormal statistics would make that rare (σ ≈ 1 gives ~5.6x). A part with a defect behaves like a real "tail cell".
- **Stored '0's fail too.** With the bitline parked at 1.65 V, subthreshold current leaks into a '0'. Real DRAM sees this as well, which is why some cells store a '1' as "discharged" (anti-cells).
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
| The heater never reaches 45 °C | Too little power, or the box is not insulated | Use a smaller box; 7 W heats a 2-3 L foam box. Never raise the voltage above 12 V |

---

## 12. Sources

Evidence tags:
- [DATASHEET] = manufacturer data;
- [REPORTED] = paper, press, distributor or search snippet;
- [ESTIMATE] = calculation in `bench_calcs.py`;
- [MODEL] = the study's model;
- [UNVERIFIED] = could not confirm.

Web pages were read through search snippets on 2026-11-03; some hosts were blocked, so a few datasheets could not be opened in full. Prices are approximate as of November 2026.

1. ALD1106 IDS(OFF) 10 pA typ / 400 pA max at VDS 12 V, 1 nA / 4 nA at 125 °C; IGSS 0.1 pA / 10 pA; "consists of junction leakage currents" [DATASHEET, via snippet]: https://www.electronicsdatasheets.com/download/120482.pdf?format=pdf (also https://www.aldinc.com/pdf/ALD1106.pdf)
2. ALD1106 distributor attributes: RDS(on) 500 Ω at 5 V, threshold listed as 1 V [REPORTED]: https://www.lcsc.com/product-detail/C3289693.html
3. ALD1106PBL "MOSFET 4N-CH 10.6V 14DIP", $2.90 at quantity 1 (broker) [REPORTED]: https://www.smbom.com/product/ald1106pbl-16467559
4. 2N7000 VGS(th) 0.8 / 2.1 / 3.0 V; Ciss 20 pF typ / 50 pF max (older sheet 60 pF max); IDSS 1 µA max at 48 V [DATASHEET]: https://www.onsemi.com/download/data-sheet/pdf/2n7000-d.pdf
5. LMC6482 input current 0.02 pA typ / 4 pA max; specified at 3 V, 5 V and 15 V; rail-to-rail; PDIP-8 [DATASHEET]: https://www.ti.com/product/LMC6482
6. MCP6541 / MCP6544 bias current 1 pA, 1.6-5.5 V, push-pull, 600 nA per comparator, PDIP [REPORTED, distributor listings]: https://futureelectronics.com/fr/p/semiconductors--analog--comparators/mcp6544-i-p-microchip-1851997 and https://au.rs-online.com/web/p/comparators/0598251
7. CD40109B quad low-to-high level shifter, VCC 3-18 V, no VDD-first sequencing needed [REPORTED]: https://www.ti.com/product/es-mx/CD40109B-MIL and https://www.radiolocman.com/datasheet/data.html?di=285989
8. KEMET C0G insulation resistance at 25 °C: 1,000 MΩ·µF or 100 GΩ, whichever is lower [DATASHEET]: https://mfgdatasheets.nlight.net/Kemet%20C0G.pdf
9. DS18B20 ±0.5 °C from -10 to +85 °C, 750 ms 12-bit conversion [DATASHEET]: https://www.analog.com/products/DS18B20 and https://wcm-cce.cldnet.analog.com/media/cn/technical-documentation/data-sheets/2812.pdf
10. RP2040 ADC ENOB 8.7 [REPORTED]: https://pigweed.googlesource.com/third_party/github/raspberrypi/pico-sdk/+/d0c7642369b91c934b014134c862000eee1dbca4%5E%21
11. RP2040 ADC input pull-up pitfall (reading ~30% low through 47 kΩ) [REPORTED, forum]: https://forum.micropython.org/viewtopic.php?p=55650
12. RP2040 ADC DNL spikes at codes 512/1536/2560/3584 [REPORTED]: https://hackster.io/news/raspberry-pi-confirms-it-is-investigating-a-flaw-in-the-raspberry-pi-pico-rp2040-adc-95c393b55dfb and https://github.com/kitanokitsune/rp2040adc_correction
13. RP2350-E9 redefined as input-mode leakage when the pad sits between logic levels [REPORTED]: https://hackaday.com/2024/09/04/the-worsening-raspberry-pi-rp2350-e9-erratum-situation/ and https://hackster.io/news/a-surprise-hardware-bug-in-raspberry-pi-s-rp2350-leads-to-unexpected-pull-down-behavior-76b51ec22ede
14. RP2350 A4 stepping fixes E9; mixed stock [REPORTED]: https://support.thepihut.com/hc/en-us/articles/29618349405469-When-will-you-stock-the-A3-A4-stepping-RP2350-Raspberry-Pi-Pico-2 and https://www.cnx-software.com/?p=154587
15. Real-DRAM cell numbers (5.42 fF cell, 34.7 fF bitline, 71 mV signal, 46 fJ refresh per bit, retention halves per ~10 °C) [MODEL]: [`models/dram_cell_physics.py`](../models/dram_cell_physics.py)
16. raw-ber-contract ~9x refresh saving, kill line incl. VRT [MODEL]: [`dossiers/raw-ber-contract.md`](../dossiers/raw-ber-contract.md), [`DRAM_MOONSHOT_REPORT.md`](../DRAM_MOONSHOT_REPORT.md) section 1
17. All [ESTIMATE] numbers: [`code/T1_pico/bench_calcs.py`](code/T1_pico/bench_calcs.py) (run `--selftest` to check the formulas).
18. [UNVERIFIED]: Pico price; ALD1106 typical Vth of 0.7 V; ALD1106 and CD40109B pin numbers; RP2040 GPIO input-leakage spec; IPA SDS hazard statements (standard classification, not re-checked); IRLZ44N gate drive at 3.3 V; silica-gel indicator chemistry; DRAM Bender setup cost; current shuttle availability.
