# E8: Your own oxide gain-cell memory

*Home-lab experiment E8, track T4 of the [dram-moonshot](../README.md) study. Written 2026-11-03. Prices are approximate as of November 2026. All code in [code/T4_oxide/](code/T4_oxide/) is reference code, **untested on hardware**. Shared physics: [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md), sections 2.8-2.9.*

| | |
|---|---|
| **What you make** | A one-bit memory cell of the type the study's BEST BET uses: two transistors and no capacitor in the cell itself (2T0C). Your own oxide transistor from [E7](E7_make_your_own_oxide_transistor.md) is the write switch. Stretch goal: a 2×2 array (4 bits) of home-made cells driven by a Raspberry Pi Pico |
| **What you measure** | Retention at 25, 45 and 65 °C; leakage current and its activation energy; non-destructive reads; hold-bias dependence; kickback; and a side-by-side comparison with a silicon switch (the [E2](E2_gain_cell_no_capacitor.md) circuit) and an ideal switch (reed relay) |
| **Difficulty** | 4 of 5 for one cell; 5 of 5 for the 2×2 array |
| **Time** | 2-3 weekends after E7 for one cell (retention runs go overnight); 1-2 more for the array |
| **Cost tier** | $ on top of E7 and its rig: about $40, plus about $10 for the array ([parts](#4-parts)) |
| **Needs** | A "write-switch grade" TFT from E7 (Vth ≥ +3 V, Ioff ≤ 10 pA at Vgs = 0). Optional: the [E4 femtoamp bench](E4_femtoamp_leakage_bench.md) (track T2) to watch the storage node directly |

**Acronyms.** 2T0C = two transistors, zero capacitors. TFT = thin-film transistor. SN = storage node. WWL / WBL = write word line / write bit line. RBL = read bit line. TIA = transimpedance amplifier. C0G (also called NP0) = the most stable, lowest-leakage class of ceramic capacitor. NTC = negative-temperature-coefficient thermistor. PBTI = positive-bias temperature instability (threshold drift under positive gate stress). RTN = random telegraph noise. ESD = electrostatic discharge. HBM = high-bandwidth memory. Ea = activation energy.

---

## 0. What you are building, and why it matters

**A gain cell stores a bit on a transistor's gate.**
- The **write transistor** connects the bit line to the storage node (SN), then switches off. While it is off, its leakage is the only way the charge can leave.
- The SN is the gate of a second transistor, the **read transistor**. You read the bit by measuring the read transistor's current. Its gate draws no current, so the stored charge is untouched and the read is non-destructive. Ordinary DRAM destroys the bit on every read and must write it back.

**Why the study cares.** The BEST BET, [hot-side memory](../dossiers/hot-side-memory.md), stacks 2T0C oxide cells on a GPU. It works only because an oxide write switch leaks so little that a bit survives seconds at ~105 °C, where silicon DRAM must refresh every 16 ms [STUDY]. The cell's storage node there is ~0.15 fF [STUDY].

**Your version.**

```
          WBL c (0..5 V)                                RBL c (TIA virtual node, 2.5 V)
             |                                                  |
          [drain pad]                                        [drain]
 WWL r --->|  YOUR oxide TFT (E7 chip r)               SN --->|  2N7000 read transistor
 (the chip |  back gate = the chip's silicon                 [source]
  substrate)  [small source pad] ---------- SN ---+             |
                                                  |       row select r (N-MOSFET to ground)
                                          C_store 10 nF (C0G or polypropylene)
                                                  |
                                                 GND
```

Two differences from a real 2T0C cell are deliberate:
- The read transistor is a silicon 2N7000, so your measurement depends only on your home-made write switch.
- You add a 10 nF capacitor. Your TFT's source pad overlaps the back gate and couples the word line into the SN (section 1.2), and the big capacitor swamps that coupling.

Stretch B (section 8) removes the silicon read transistor too.

---

## 1. First principles and expected numbers

Every number is printed by [`code/T4_oxide/expected_numbers.py`](code/T4_oxide/expected_numbers.py), sections E8-1 to E8-4. Put your own pad area, threshold and capacitor into `PLAN` and run it again.

### 1.1 Charge, current and time

> Q = C_SN · V        I_leak = −C_SN · dV/dt        t_retention = C_SN · ΔV / I_leak

| Part of C_SN | Value |
|---|---|
| Added C_store | 10 nF |
| 2N7000 gate | ~50 pF [UNVERIFIED: distributors list 40-60 pF] |
| Air wiring | ~10 pF [ESTIMATE] |
| TFT source pad over the back gate (1 mm² on 300 nm SiO2) | 115 pF [ESTIMATE] |
| **Total** | **10.18 nF** |

At 1 pA of leakage, the cell loses 100 mV in **1,018 s** (about 17 minutes) [ESTIMATE].

### 1.2 Kickback: charge conservation

When the word line falls, the pad overlap capacitor pulls the SN down with it:

> ΔV_SN = −ΔV_WWL · C_ov / C_SN

| Case | Kick |
|---|---|
| Fast 27.5 V edge, C_store 10 nF | 311 mV |
| Your rig's slow, filtered edge: only the swing after the switch turns off counts, (V_SN + Vth) · C_ov / C_SN | 124 mV |
| Fast edge with only 1 nF C_store | 2.69 V: the bit is destroyed |
| Fast edge with 47 nF C_store | 0.07 V |

[ESTIMATE.] Real 2T0C cells fight the same effect; the study's plan includes "SPICE the MLC window and kickback" ([dossier §5](../dossiers/hot-side-memory.md)). Your fixes: a big C_store, a small storage-side pad, and a slow word-line edge.

### 1.3 Write time

The switch's on-resistance R_on = 1 / (µ · Cox · (W/L) · (Vgs − Vth)) charges C_SN:
- route A TFT: R_on ≈ 176 kΩ, so τ = R_on · C_SN ≈ 1.8 ms;
- route B TFT: R_on ≈ 585 kΩ, so τ ≈ 5.9 ms.

The code's 200 ms write pulse is more than 30τ [ESTIMATE].

### 1.4 Temperature: Arrhenius

> I(T) = I0 · exp(−Ea / kT)

| Switch | Leakage mechanism | Expected Ea |
|---|---|---|
| Silicon MOSFET (2N7000) | Drain-body p-n junction: thermal generation (∝ n_i) and diffusion (∝ n_i²) | 0.56-1.12 eV (Eg/2 to Eg) |
| Your oxide TFT | No junction; subthreshold tail, traps, surfaces, gate-oxide paths | Unknown, which is what you measure. Planning value 0.35 eV [ESTIMATE]. The study assumed 0.8 eV for imec's cells [STUDY] |

**Predicted retention, 100 mV lost from 10.18 nF** (planning leakage: oxide 1 pA, silicon 10 pA, both at 25 °C) [ESTIMATE]:

| T | Oxide switch | Silicon switch, Ea 0.56 eV | Silicon switch, Ea 1.12 eV | Oxide/silicon ratio |
|---|---|---|---|---|
| 25 °C | 1,018 s | 102 s | 102 s | 10 / 10 |
| 45 °C | 432 s | 26 s | 6.6 s | 17 / 66 |
| 65 °C | 203 s | 7.7 s | 0.6 s | 26 / 346 |

**The prediction to test.** The oxide cell's lead grows with temperature, by ×2.6 to ×35 from 25 to 65 °C, **if** its leakage has a lower Ea than the silicon junction. If both have Ea ≈ 0.8 eV, the ratio stays flat and the win is only the absolute level. Both outcomes are informative. A what-if: an oxide Ea of 1.3 eV against silicon's 0.56 eV would make the lines cross at 51 °C, so the oxide would lose when hot. That would be a real warning for hot-side memory, if it held at small scale.

The silicon value is a planning number. The E2 circuit measures it for real.

### 1.5 Hold bias: Boltzmann again

Below threshold the oxide channel's current falls 10x per SS volts of more negative gate. So lowering the word line during hold should keep cutting leakage, until a floor takes over:

| WWL hold (Vgs relative to the source pad) | Channel current predicted (Vth 8 V, SS 1 V/dec) | What you will see (1 pA floor) |
|---|---|---|
| +4 V | 6e-12 A | 6 pA |
| +2 V | 6e-14 A | ~1 pA (floor) |
| 0 V | 6e-16 A | ~1 pA (floor) |
| −2 V | 6e-18 A | ~1 pA (floor) |

[ESTIMATE.] The rig's word line cannot go below 0 V. To reach a negative effective Vgs, park the bit line above 0 V during hold (WBL 0.5 V gives Vgs = −0.5 V at WWL 0 V); that also shrinks Vds across the switch. Do this with the TFT only: with the 2N7000, a bit line above a stored "0" forward-biases its body diode and recharges the node (see E2).

A silicon switch behaves differently. Below about Vgs = 0.5 V its junction leakage dominates, so a more negative hold does not help and can hurt (gate-induced drain leakage). This is the home version of the study's −0.5 V vs −0.7 V hold split. In your cell the TFT's "source" is whichever side is lower, so the effective Vgs during hold is WWL − min(V_SN, V_WBL).

### 1.6 Non-destructive read

- The read transistor's gate is insulated. The 2N7000 datasheet guarantees gate leakage ≤10 nA [DATASHEET, R1]; real parts are usually far lower [ESTIMATE].
- Prediction: 1,000 reads change V_SN by no more than a quiet hold of the same length does.
- **Free voltmeter.** Near threshold the 2N7000's current changes ~10x per ~100 mV [ESTIMATE], so 1 mV on the SN changes the read current by ~2%. The calibration step turns read current back into SN voltage.

### 1.7 Why your retention time says little about a real chip

| | Your cell | imec-class 2T0C cell [STUDY] |
|---|---|---|
| Storage node | 10.18 nF | 0.15 fF (~7e7x smaller) |
| Leakage | ~1 pA | ~75 zA (~1e7x smaller) |
| Droop rate I/C | 9.8e-5 V/s | 5.0e-4 V/s |

[ESTIMATE.] The droop rates and retention times come out similar, but for opposite reasons. Only per-device physics transfers to a real chip: the mechanism, the Ea, the hold-bias dependence. The retention time does not.

### 1.8 What you cannot see

- **RTN.** One trapped electron shifts your TFT's threshold by 0.14 µV, versus 1.86 mV for a 0.01 µm² device (q/(Cox·A)) [ESTIMATE].
- **Tails.** To trust a quantile q you need about 10 devices beyond it, so N ≥ 10/q. Four cells give you the median at best. The study's pass lines sit at the 1e-4 to 2e-5 quantile, which needs ≥1e5-5e5 cells.

---

## 2. Honest scope

| What E8 proves | What E8 does NOT prove |
|---|---|
| A memory cell held by **your own** oxide transistor writes, holds and reads non-destructively | That a 0.15 fF oxide cell holds data for ≥1 s at 105-125 °C in its 1e-4 tail (the study's Gate A+ kill line) |
| Retention follows t = C·ΔV/I, measured with the same charge-decay method the study's Gate A+ and E4 use | Any absolute leakage at scale: your device is ~1e4 µm² of defect-rich film on 300 nm SiO2 |
| Whether your oxide switch's leakage is less temperature-sensitive than a silicon junction's (Ea), and whether a deeper hold bias lowers it: the two physics claims behind "refresh-light" hot-side memory | RTN (invisible at your size), Vt variation statistics, 1e-4 tails (4 cells) |
| Kickback and half-select disturb are real, measurable array effects (array stretch) | Speed (your writes take ms, not ns), endurance (you will do ~1e3-1e4 writes, not 1e12), density, cost, bonding, hydrogen budget |

**What a mm-scale home TFT can and cannot tell you about 0.01 µm² devices**

| Quantity | Transfers to 0.01 µm²? | Why |
|---|---|---|
| Leakage mechanism and its Ea | Partly | Same material class and physics; different defects and thickness |
| Hold-bias dependence (decades per volt) | Qualitatively | Subthreshold physics is scale-free; SS differs |
| Off-current per µm of width | No | Film quality and gate stack dominate |
| Retention time | No | C and I scale by 7e7 and 1e7 (section 1.7) |
| Vt spread, RTN, 1e-4 tail | No | They scale with 1/area and need ≥1e5 devices |
| The measurement method and analysis code | **Yes** | Same law, same code; that is your ticket (section 13) |

**How it scales up:** makerspace (better contacts, passivation) → university nanofab, external user (photolithographic arrays of hundreds of devices, heated probe station: first real distributions) → the study's Oxide Tail Statistics lot (≥1e5 cells of 0.01 µm² at 85-125 °C). Section 13 turns this demo into that request.

---

## 3. Safety

> **SAFETY BOX**
>
> - **Chemistry.** E8 uses devices you already made. Everything in [E7's Safety box](E7_make_your_own_oxide_transistor.md#3-safety) still applies to making them. E8 adds no chemicals.
> - **Voltage.** Everything stays ≤30 V: a USB-powered Pico, a 0-30 V bench supply with a 50 mA limit, and a bought 12 V adapter for the heater. No mains-voltage builds. Up to 28 V sits on the TFT chip's substrate (the word line). That is low energy, but do not touch the chips while powered.
> - **The 2N7000 gate is rated ±20 V.** The code limits the silicon-switch word line to 10 V (`wwl_on_si`). Never put the 27.5 V oxide word line on a 2N7000.
> - **Heater.**
>   - A 10 Ω 25 W aluminium-clad resistor on 12 V gives 14 W. **Bolt it to the aluminium block**: in free air it overheats.
>   - Wire a thermal cut-off fuse (~72-77 °C) in series with the heater, mounted on the block. The software also cuts the heater above 70 °C, but the fuse is the real guard.
>   - Maximum setpoint 65 °C. Put the block on a ceramic tile. Stay nearby for the first heat-up.
>   - A 65 °C block can burn skin with prolonged contact. Let it cool before handling.
> - **ESD.** Touch the grounded tin before handling 2N7000s or the TFT chips.
> - **Silica gel.** Use plain or orange (cobalt-free) silica gel. Blue indicating gel contains cobalt chloride [UNVERIFIED]. Keep it away from children and pets.
> - **Sharp chips.** Handle with tweezers (see E7).

---

## 4. Parts

All prices [ESTIMATE] unless tagged.

| Part | Spec that matters | Example part number | Approx USD | Where |
|---|---|---|---|---|
| Read transistors ×10 | N-MOSFET, Vth 0.8-3.0 V, gate leakage ≤10 nA spec, no gate Zener | onsemi 2N7000 [DATASHEET, R1] | 4 | Digi-Key, Mouser |
| Storage capacitors ×6 | 10 nF, C0G/NP0 50 V ceramic, or polypropylene film. Low leakage, low dielectric absorption | Any C0G 10 nF 50 V | 6 | Digi-Key, Mouser |
| Control-cell switch | Reed relay, 5 V coil (one is already on the rig board) | Any SIP reed relay | 3 | Any |
| Heater | 10 Ω, 25 W, aluminium-clad, bolt-down | Any | 4 | Any |
| Heater switch | Logic-level N-MOSFET, ≥2 A | Any logic-level TO-220 part [UNVERIFIED] | 2 | Any |
| Temperature sensor | 10 kΩ NTC, B ≈ 3950 | Any | 1 | Any |
| Thermal cut-off | ~72-77 °C, ≥2 A | Any | 2 | Any |
| Block | Aluminium, ~30×30×6 mm | Offcut | 5 | Metal supplier |
| Heater supply | 12 V, 2 A, bought adapter | Any | 10 | Any |
| Array add-on | 2nd LMC6482 (TIA1), 2nd LM358 (WWL1/WBL1), 2 more 2N7000 as row selects | As E7 | 10 | Any |
| Optional | E4 electrometer buffer to watch the SN directly | See E4 (track T2) | - | - |

**Total:** about $40 for one cell plus controls, and about $10 more for the 2×2 array [ESTIMATE]. You also need 1-2 write-switch-grade E7 chips, or 2 chips with 2 isolated TFTs each for the array.

---

## 5. Tools needed

Everything from E7 (soldering iron, multimeter, tweezers, the T4 mini-SMU rig, laptop with Python 3, numpy and `mpremote`), plus M3 screws and thermal paste for the heater, and a timer or overnight patience.

---

## 6. The circuit

**One storage node, swappable write switch.** Build a single SN with its C_store and 2N7000 read transistor. Connect the write switch through a 3-pin socket (WWL, WBL, SN) with short PTFE-insulated wires. Because the SN, C_store and read transistor never change, one calibration serves every switch, and any difference you measure comes from the switch alone:

| Switch | In the socket | Purpose |
|---|---|---|
| O | Your E7 oxide TFT | The experiment |
| S | 2N7000, **drain to SN, source to WBL**, gate to its own word line (≤10 V) | Silicon comparison: the [E2](E2_gain_cell_no_capacitor.md) circuit. This orientation keeps the body diode reverse-biased when WBL is parked at 0 V. Reversed, the diode drains the bit at once |
| R | Reed relay (GP14) | "Ideal switch": the floor set by C_store, the read gate, the board and the cables |
| D (optional) | An E7 device whose channel you scratched away: same pads, no channel | Floor from pad-to-gate oxide and surfaces |

Practical notes:
- **Heat only the switch.** The write switch sits on the heated aluminium block: the TFT chip lies on it, the 2N7000 or relay is clamped to it. C_store and the read transistor stay at room temperature in the tin. That way only the switch's leakage changes with temperature, and the calibration (read current ↔ SN voltage) stays valid.
- **Build the SN like [E4](E4_femtoamp_leakage_bench.md).** Solder it in the air or on PTFE standoffs. Clean off flux with isopropanol and let it dry. Never touch it.
- **Rig connections.** Gate amplifier → WWL; drain amplifier → WBL (the code caps the bit line at 5 V); TIA0 → RBL; GP12 → row-select MOSFET (or tie the read transistor's source to ground for a single cell); GP15 → heater MOSFET; GP28 → NTC divider.
- **Using the E4 bench instead.** E4's write driver is a 9 V battery level shifter. Your TFT needs Vgs ≈ Vth + 10 V to pass the write voltage, so use three 9 V batteries in series (27 V) as E4's word-line supply. That is still ≤30 V.

---

## 7. Procedure

1. **Pick the switch.** Choose a write-switch-grade TFT from E7. Note its source-pad area and Vth. Put them into `PLAN` (`sn_pad_area_mm2`, `vth_V`) in `expected_numbers.py` and rerun. Write down the predicted C_SN, kick and retention.
2. **Rehearse on the computer** (5 minutes):
   ```
   python3 code/T4_oxide/pico_gaincell.py --sim --test calibrate --out sim_cal.csv
   python3 code/T4_oxide/pico_gaincell.py --sim --test retention --switch tft --temp 45 --out sim_ox45.csv
   python3 code/T4_oxide/retention_analysis.py --selftest
   ```
3. **Build** the storage node and switch socket (section 6). With no switch in the socket, check with the multimeter that the SN is not shorted to anything (>100 MΩ, or the meter's limit).
4. **Load the code:** `mpremote cp code/T4_oxide/t4_hw.py code/T4_oxide/pico_gaincell.py :`
5. **Calibrate once.** The switch is held on while the bit line sweeps 0-3.6 V. With the reed relay in the socket, SN equals WBL exactly:
   `mpremote exec "import pico_gaincell as g; g.run('calibrate', switch='relay')" > cal.csv`
   The read current should rise smoothly over ~4-6 decades. The code picks "1" as the highest voltage whose read current stays ≤50 µA, and "0" with the read transistor off. Repeat the calibration with your TFT in the socket (`switch='tft'`) as a check: the two curves should match.
6. **Kickback check.** Start a 10-minute retention run (next step). The first samples show the kick. Compare with your prediction (~0.1-0.3 V). If the kick is over 0.5 V, raise C_store or shrink the source pad.
7. **Retention at room temperature, each switch in turn**, heater off:
   `mpremote exec "import pico_gaincell as g; g.run('retention', switch='tft', duration_s=3600, label='oxide')" > O_25.csv`
   Then swap in the 2N7000 (`switch='si'`, label `si`, file `S_25.csv`) and the relay (`switch='relay'`, label `relay`, file `R_25.csv`). Samples are log-spaced, 20 per decade of time, so fast and slow decays are both captured. If a switch has not lost 100 mV in an hour, run it overnight (`duration_s=43200`).
8. **Read disturb**, TFT in the socket: `g.run('read_disturb', switch='tft')` (1,000 reads). Compare its ΔV with the quiet-hold droop over the same time.
9. **Hold bias**, TFT in the socket: `g.run('hold_bias', switch='tft')` holds the word line at 4, 2 and 0 V for 10 minutes each. Expect leakage to fall with lower hold until the floor (section 1.5). Repeat with the 2N7000 at levels below its threshold, because 4 V would turn it on: `g.run('hold_bias', switch='si', levels=(1.0, 0.5, 0.0))`. Expect no change (junction-limited).
10. **Heat to 45 °C, then 65 °C.** Pass `temp=45` or `temp=65`; the code waits until the block is stable within ±0.5 °C for 5 minutes. Repeat step 7 for O, S and R at each temperature. At 65 °C the silicon cell may lose its bit in seconds: that is the point.
11. **Analyse:**
    ```
    python3 code/T4_oxide/retention_analysis.py compare --c-sn 10.18e-9 --calib cal.csv --floor-label relay \
      --run oxide:25:O_25.csv --run oxide:45:O_45.csv --run oxide:65:O_65.csv \
      --run si:25:S_25.csv    --run si:45:S_45.csv    --run si:65:S_65.csv \
      --run relay:25:R_25.csv --run relay:45:R_45.csv --run relay:65:R_65.csv --json e8_result.json
    ```
    Read every WARNING. "Cell leakage < 3x dummy floor" means you measured your setup, not your switch.
12. **Optional cross-check.** With the TFT in the socket, watch the SN directly with the E4 electrometer buffer on ADS AIN2. It should agree with the calibrated read-current estimate within ~10 mV.
13. **Fill in the data sheet** (section 9) and compare with the predictions in section 1.

---

## 8. Stretch goals

### 8a. A 2×2 array: 4 bits, organised like DRAM

| Line | Connects | Driven by |
|---|---|---|
| WWL0 | Substrate (back gate) of TFT chip 0 | Gate amplifier, GP0 |
| WWL1 | Substrate of TFT chip 1 | Second high-voltage amplifier, GP6 |
| WBL0 / WBL1 | TFT drains in column 0 / column 1, on both chips | Drain amplifier GP2 / filtered PWM GP8 (≤5 V) |
| SN(r,c) | Each TFT's small pad + its own 10 nF + its own 2N7000 gate | - |
| RBL0 / RBL1 | Read-transistor drains in column 0 / 1 | TIA0 / TIA1 (ADS AIN0 / AIN1) |
| Row select 0 / 1 | Read-transistor sources in row 0 / 1, through an N-MOSFET to ground | GP12 / GP13 |

A chip with a common back gate is a word line, and its separate TFTs are the bits on that row. That is a DRAM array in miniature. **Scribe moats between the two TFTs on each chip**, or the film leaks between bits.

Tests:
- **Patterns:** `g.run('pattern')` writes all 16 four-bit patterns, waits 60 s, reads back and prints pass/fail per pattern. Expected: 16/16. The droop in 60 s at 1 pA on 10 nF is ~6 mV, far inside the margin [ESTIMATE].
- **Half-select disturb:** `g.run('disturb')` stores 1,1 in row 1, then writes row 0 1,000 times while row 1's bit lines swing. Any loss beyond the quiet-hold droop is disturb. Real arrays have the same problem.

### 8b. All home-made cell (advanced)

Replace the 2N7000 with a second home TFT on its own chip, with its back gate wired to the SN.
- **Capacitance.** C_SN then includes that whole chip's back-gate capacitance: hundreds of pF for mm² pads [ESTIMATE].
- **Voltage.** The read TFT needs V_SN above its own Vth (~8 V), so "1" must be ~12-15 V. Raise `wbl_max` in `t4_hw.py` carefully, never above 20 V. Check that the write TFT can still pass that level: WWL 28 V − 15 V = 13 V > Vth.
- **What it shows.** A cell with no silicon transistor at all. Only the measurement electronics are silicon.

---

## 9. Data sheet / log template

```
Switch: O / S / R / D   Switch ID (E7 chip, device):        Date:
E7 data: Vth ___ V  SS ___ V/dec  Ioff(Vgs=0) ___ A  pad area (SN side) ___ mm2
C_store ___ nF (type ___)   read FET ___ (Vth measured ___ V)   C_SN (calc) ___ nF  (measured ___)
Calibration file ___   levels: "0" ___ V  "1" ___ V   read current at "1" ___ A
Kick on write: predicted ___ mV   measured ___ mV
Retention runs (100 mV criterion):
  T = 25 C: I_leak ___ A   t_100mV ___ s (extrapolated? Y/N)   file ___
  T = 45 C: I_leak ___ A   t_100mV ___ s                         file ___
  T = 65 C: I_leak ___ A   t_100mV ___ s                         file ___
  Ea ___ eV (R2 ___)       floor (relay) at same T: ___ / ___ / ___ A
Read disturb: 1000 reads, dV ___ mV vs quiet-hold dV ___ mV
Hold bias: WWL 4 V ___ A   2 V ___ A   0 V ___ A
Oxide/Si retention ratio: 25 C ___  45 C ___  65 C ___   growth ___   crossover ___ C
Array: patterns correct ___/16   half-select dV ___ mV after ___ writes
Room T ___ C, RH ___ %, dark tin Y/N     Notes:
```

---

## 10. Pass / fail criteria

| Test | Pass | Fail or warning |
|---|---|---|
| **It is a memory** | After 60 s at 25 °C, "1" and "0" read currents differ by ≥10x | <10x |
| **Non-destructive read** | 1,000 reads change V_SN by <10 mV beyond the quiet-hold droop | More: check read-transistor gate leakage and wiring |
| **Clean measurement** | Oxide-cell leakage ≥3x the relay cell at the same temperature | Otherwise report the oxide leakage as "≤ floor" and improve the setup (E4 methods) |
| **The physics claim** | At 65 °C, oxide-cell retention ≥10x silicon-cell retention on the same C_SN | Oxide worse than silicon at 65 °C: see section 12 |
| **Temperature slope** (informative either way) | Report Ea for both. Ea(Si) − Ea(oxide) ≥ 0.25 eV means the advantage grows ≥3x from 25 to 65 °C | Ea(oxide) ≥ Ea(Si): advantage flat or shrinking. Report the crossover temperature |
| **Hold bias** | Oxide leakage drops ≥10x from 4 V to 0 V hold, or reaches the floor | Flat above the floor: leakage is not through the channel (gate oxide, surface) |
| **Array (stretch)** | 16/16 patterns; half-select disturb <50 mV after 1,000 neighbour writes | Fewer patterns: isolation, kick or level choice |

---

## 11. What would surprise you (and would mean something new)

- **Oxide-cell leakage below the relay floor.** Impossible as measured: recheck your floor. If it holds up with the E4 method, publish the method.
- **Oxide leakage that does not rise from 25 to 65 °C** while silicon rises 15-150x. That is the hot-side thesis in miniature. If your device beats a silicon junction at 65 °C by 100x or more, that is a strong demo result.
- **Oxide Ea above silicon's.** It would mean a thermally activated defect path dominates. For the study, that is a warning sign about tails at 105-125 °C.
- **Retention that improves after a few hours at 65 °C.** That points to annealing of traps or desorption of water. Useful process knowledge: does a pre-bake fix it?
- **Step-like jumps in the decay.** At your size a single trap is invisible (section 1.8), so steps point to contamination, cracks or moving cables, not RTN.
- **"1" decaying faster than "0" rises, or the reverse.** That would show asymmetric leakage paths (to the word line vs the bit line).

---

## 12. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Stored "1" vanishes at the end of the write | Kickback too large | Bigger C_store; smaller SN pad; check the slow-edge setting (`wwl_fall_ms`) |
| Silicon cell loses its bit instantly at 25 °C | 2N7000 reversed: body diode forward-biased | Drain to SN, source to WBL |
| Every switch, including the relay, decays fast | Flux, fingerprints or humidity on the SN; leaky capacitor type | Clean with IPA and dry; air-wire the SN; C0G or polypropylene only; silica gel |
| Read current saturates or is pinned at the range limit | "1" level too high for the read transistor | Recalibrate; lower `i_one_max` |
| Calibration not monotonic | Write switch not fully on during calibration (Vgs too low) | Raise `wwl_on` (≤28 V) or lower the levels; check the TFT's Vth |
| Decay changes when the heater cycles | Heater PWM pickup on the SN | `heater_quiet_ms` already pauses it during reads; route heater wires away; twist the pair |
| Oxide leakage jumps after opening the tin | ZnO photoconductivity | Keep it dark; wait 30-60 minutes |
| Array bits copy each other | Film not isolated between the TFTs on one chip | Scribe moats |
| Leakage grows run after run | PBTI or drift from repeated 27.5 V writes; water uptake | Re-measure the TFT's transfer curve; shorter writes; bake at 150 °C between sessions |

---

## 13. From this demo to a nanofab: your ticket

**Why it works as a ticket.** University fabs are open to outside users, but they want people who know what they will measure and why. You will have:

1. E7 transfer and output curves with extracted parameters, plus the JSON and SVG files from `iv_analysis.py`;
2. E8 retention against temperature for oxide vs silicon vs ideal switches, with Ea, floors and hold-bias data;
3. open, tested analysis code (`code/T4_oxide/`);
4. the study's one-page **Oxide Tail Spec** (the Monday action in [decision.json](../research/stage3/decision.json)): device structures × channel splits, area, timescale, temperature, hydrogen and thermal dose, bond split, and the pass/kill lines from the dossiers.

**Where.**
- **Purdue's Birck Nanotechnology Center** is the judges' first choice. External users pay daily lab and cleanroom fees: $44 + $53/day for academic and non-profit users, $51 + $61/day for for-profit users, plus hourly tool rates (for example EBL $115-132/h) (2023 schedule, R2).
- **Georgia Tech IEN** is the second site. About 20% of its users are external, and academic and government users pay Georgia Tech rates (R3).
- Both are in the NNCI network of 16 sites open to external users (R3).

**A first ask that fits a demo budget** [ESTIMATE]:
- Training, then 10 cleanroom days and ~40 tool-hours (spin or sputter, photolithography for 10 µm devices, ALD Al2O3 passivation, a 400 °C forming-gas anneal, probe station with heated chuck).
- That is about $1.1k in day fees plus $2-5k in tool time at for-profit rates.
- It turns your 4 cells into a few hundred devices. That is enough for the first real distribution: the median and the 1-10% tail.

**Short email template**
```
Subject: External-user request: oxide TFT leakage statistics (Oxide Tail Spec attached)

Hello, I am an independent builder working on oxide-semiconductor gain-cell memory.
At home I made solution-processed ZnO TFTs (on/off ___, SS ___ V/dec, Ioff ___ A) and a
working 2T0C cell whose oxide write switch held data ___x longer than a silicon switch at 65 C
(Ea ___ vs ___ eV). Data and code are attached.
I would like to (1) train as an external user and fabricate ~200 photolithographic TFTs with
ALD passivation, and (2) ask whether your center could run the attached one-page Oxide Tail Spec
(1e5-cell arrays, 85-125 C, aA-level leakage tails) and at what cost.
Could we schedule a short call?
```

**The bigger step.** The Oxide Tail Statistics lot itself (≥1e5 cells of 0.01 µm², 85-125 °C, after the real bond budget) is what the study's $1M plan funds, at ~$220-280k [STUDY]. Your home data does not replace it. It shows you can specify it, measure it and analyse it.

---

## Sources

Tags: [REPORTED] = paper, press or vendor page, mostly via search snippets; [DATASHEET] = datasheet; [ESTIMATE] = our arithmetic; [UNVERIFIED] = not confirmed; [STUDY] = this repository's models and dossiers. Literature on solution oxide TFTs, chemicals and safety is listed in [E7's Sources](E7_make_your_own_oxide_transistor.md#sources).

- **R1** onsemi 2N7000 datasheet: VGS(th) 0.8-3.0 V at 1 mA; forward gate-body leakage limit 10 nA at VGS = 15 V. Input capacitance 40-60 pF per distributor listings [UNVERIFIED]. https://www.onsemi.com/download/data-sheet/pdf/2n7000-d.pdf ; https://www.farnell.com/datasheets/1840524.pdf ; https://ece-classes.usc.edu/ee459/library/datasheets/2N7000.pdf
- **R2** Purdue Birck recharge rates (2023 schedule, pending approval when posted; confirm current rates with Birck). https://engineering.purdue.edu/ECN/mailman/archives/bnc-all/2023-May/002727.html ; https://birck.research.purdue.edu/getting-started-at-birck/rates/ ; https://birck.research.purdue.edu/equipment/become-a-user/
- **R3** Georgia Tech IEN external users and NNCI. https://sites.gatech.edu/ien-prc/files/2021/07/IEN-Welcome-and-Overview-Vogel.pdf ; https://dev.research.gatech.edu/nano/become-core-user ; https://hg.gatech.edu/sites/default/files/attachments/IEN%20Seed%20Grant%20RFP%202016-17.pdf ; https://nnci.net/sites/default/files/inline-files/SENIC%20Overview%20Sept%202018_Final.pdf
- **R4** Oxide 2T0C retention: solution-processed IGZO 2T0C 3.69 s (250 °C anneal) → 66.0 s (450 °C), limited by trap-induced leakage (MRS Spring 2026 abstract) https://www.mrs.org/meetings-events/annual-meetings/archive/meeting/presentations/view/2026-mrs-spring-meeting/2026-mrs-spring-meeting-4433903 ; ITO vertical-channel 2T0C >160 s https://scholarworks.gnu.ac.kr/item/b7313d21-0cf1-4e73-99dc-d088f829f2b7 ; ITZO 2T0C >1,000 s (ETRI, press) https://ksp.etri.re.kr/ksp/article/file/72428.pdf ; Al:ITZO 2T0C https://pmc.ncbi.nlm.nih.gov/articles/PMC11739972
- **R5** Oxide TFT temperature behaviour: IGZO Ioff ~1e-12 to 1e-13 A nearly flat 300-370 K https://repositorio.ausjal.org/handle/20.500.12032/88707 ; IZO leakage rises above 340 K via a back-channel path https://cpl.iphy.ac.cn/fileCPL/journal/article/cpl/html/2018/0256-307X/0256-307X-2018-35-9-098502.html
- **R6** ZnO photoconductivity persistence and oxygen adsorption. https://rutchem.rutgers.edu/images/PDFs/faculty/garfunkel-pubs/2012/ApplPhysLett_101_031118.pdf ; https://koasas.kaist.ac.kr/handle/10203/240837
- **R7** Rig parts: LMC6482 https://www.lcsc.com/product-detail/C2878968.html ; ADS1115 (Adafruit 1085) https://www.adafruit.com/product/1085 ; Pico 2 https://www.electronicspecifier.com/boards-and-backplanes/raspberry-pi-unveils-the-pico-2-for-just-5
- **Study files** [STUDY]: [hot-side-memory dossier](../dossiers/hot-side-memory.md) (imec >200 s at 95 °C, implied 75 zA on 0.15 fF; 105 °C silicon refresh 16 ms; Gate A+ kill lines; Purdue Birck and Georgia Tech IEN); [decision.json](../research/stage3/decision.json) (Oxide Tail Spec, biggest unknown, $1M portfolio); [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md) §2.8-2.9 (band gap, gain cells).
- **Sibling experiments:** E2, the silicon gain cell ([E2_gain_cell_no_capacitor.md](E2_gain_cell_no_capacitor.md), code [`code/T1_pico/e2_gain_cell.py`](code/T1_pico/e2_gain_cell.py)); E4, the femtoamp leakage bench ([E4_femtoamp_leakage_bench.md](E4_femtoamp_leakage_bench.md), track T2, code [`code/T2_analysis/e4_pico_leakage_bench.py`](code/T2_analysis/e4_pico_leakage_bench.py)).
