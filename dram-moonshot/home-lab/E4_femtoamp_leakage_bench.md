# E4: The DRAM cell is an electrometer. A femtoamp leakage bench at home

*Home-lab track T2. Written 2026-11-03. Part of the [dram-moonshot](../README.md) study.*

| | |
|---|---|
| **Goal** | Measure transistor off-leakage down to about 1 fA (1e-15 A) with the charge-decay method used in oxide 2T0C research. Then measure 30-120 identical transistors to get a leakage *distribution*, its quantiles with confidence intervals, and an activation energy. |
| **Why** | It rehearses the study's "Oxide Tail Spec", the measurement that decides 7 of its 10 concepts. Same method and same statistics; cheaper devices. |
| **Difficulty** | 3 of 5. The electronics are simple. The craft (shielding, insulation, patience) is the hard part. |
| **Time** | Build: 1-2 weekends. Calibration: 1 day. Data: 2-4 weeks of mostly unattended overnight logging. |
| **Cost tier** | About $150-250 for the full bench with heater and 100 test transistors (prices approximate as of Nov 2026). About $80 for a room-temperature-only first build. |
| **Code** | [code/T2_analysis/leakage_tail.py](code/T2_analysis/leakage_tail.py) (analysis; run `--selftest` and `--expected`), [code/T2_analysis/e4_pico_leakage_bench.py](code/T2_analysis/e4_pico_leakage_bench.py) (MicroPython for the Pico, untested on hardware) |

**Evidence tags used below.** [DATASHEET] = manufacturer spec, read from a search snippet when the maker's site was not reachable. [REPORTED] = paper, press, distributor or forum page. [ESTIMATE] = our arithmetic, mostly printed by `leakage_tail.py --expected`. [UNVERIFIED] = could not confirm this session. Every tagged number has a numbered source in section 14.

---

## 0. The idea in one paragraph

A DRAM bit is charge on a tiny, isolated node. It dies because a switched-off transistor leaks. The leak is far too small for any meter to see directly. But you do not need to see the current. You watch the *voltage* of the isolated node fall, and use charge conservation: **I = C · dV/dt**. Oxide-transistor researchers measure attoamp leakage this way. Their storage node is the read transistor's own gate, so the memory cell is its own electrometer [REPORTED, 17]. You will build the same thing, bigger: a cheap MOSFET as the "write transistor", a film capacitor as the storage node, and an electrometer op-amp as the "read transistor". Then you will measure many transistors and do the statistics the study's biggest unknown needs.

---

## 1. How this connects to the study

The study's biggest unknown ([report, section 1](../DRAM_MOONSHOT_REPORT.md); [decision.json](../research/stage3/decision.json)):

> "The statistical tails of scaled amorphous-oxide transistors (IGZO/IGO/ZTO, <=0.01-0.02 um2) after the full <=400 C hydrogen, thermal and bonding budget at 85-125 C: the 1e-4 to 2e-5 quantile of aA-level off-state leakage..."

The numbers that matter, from the [HOT-SIDE MEMORY dossier](../dossiers/hot-side-memory.md) [MODEL, from the study]:

| Quantity | Value |
|---|---|
| Typical oxide gain cell leakage (imec >200 s at 95 °C, 0.15 fF node) | 75 zA (7.5e-20 A) |
| 1e-4 tail cell, after the series-gate fix (25x typical) | 3.7 aA at 105 °C; 12.5 aA at 125 °C |
| Ceiling for 1 bit/cell with a 1 s refresh | 22.5 aA |
| Gate A+ kill line | 1e-4-tail retention ≥ 1 s at 105 °C, with ≥ 1e5 cells per split |

The published imec cells reached >400 s retention from an extracted off-current of 3e-19 A/µm (2020), and >1,000 s in 2021 [REPORTED, 17].

**What E4 gives you.** You cannot reach zeptoamps at home, and you cannot make 0.01 µm² oxide transistors. You *can* run the whole method end to end: build the bench, calibrate the current scale, measure a population, compute tail quantiles with honest confidence intervals, fit an activation energy, and see why 100 devices cannot tell you a 1e-4 quantile. That turns the "Oxide Tail Spec" Monday action from words into a method you have run.

---

## 2. First principles

All numbers in this section come from `python3 code/T2_analysis/leakage_tail.py --expected` [ESTIMATE] unless tagged otherwise.

### 2.1 Law 1: charge conservation on an isolated node

An isolated conductor holds charge Q = C·V. If a current I leaks off it:

**I = −C · dV/dt**

Small C turns a tiny current into a big voltage slope. That is the whole trick:

| Case | C | I | dV/dt | Time for a 10 mV drop |
|---|---|---|---|---|
| imec-class 2T0C cell, typical | 0.15 fF | 75 zA | 500 µV/s | 20 s |
| Hot-side 1e-4 tail ceiling (1 b, 1 s) | 0.15 fF | 22.5 aA | 0.15 V/s | 0.07 s |
| Your bench, low-leakage device | 100 pF | 1 fA | 10 µV/s | 1,000 s |
| Your bench, typical device | 470 pF | 1 pA | 2.1 mV/s | 4.7 s |
| Your bench, hot device | 10 nF | 100 pA | 10 mV/s | 1 s |

A 0.15 fF cell turns 75 zA into 0.5 mV/s. Your 100 pF node is ~670,000 times bigger, so the same slope needs ~670,000 times more current. **The cell is the electrometer. Shrinking the node is what makes attoamps measurable.**

### 2.2 Your bench is a giant 2T0C cell

| 2T0C gain cell (study) | Your bench |
|---|---|
| Write transistor (oxide TFT), off during hold | Device under test (DUT): a 2N7000 MOSFET, off during hold |
| Write word line (WWL), write bit line (WBL) | DUT gate (driven 0 / 9 V), DUT source (driven 1.0 V / 0 V) |
| Storage node = read-transistor gate + parasitics | Storage node = DUT drain + film capacitor + op-amp input |
| Read transistor senses the node without touching it | Electrometer op-amp: its input transistor's gate senses the node |
| Word-line kickback shifts the node when the write gate turns off [REPORTED, 18] | Same effect: ΔV = −Cgd·ΔVgate/(C_node + Cgd) |

One difference matters: a silicon MOSFET has a body diode, and an oxide TFT does not. With the source (and body) at 0 V and the node at +1 V, the drain-body junction is reverse-biased. Its generation current is most of what you will measure. In an oxide TFT there is no junction; leakage is channel and trap physics. Section 3 deals with that honestly.

### 2.3 Law 2: how small a slope can you resolve?

For a straight-line fit to N evenly spaced points over T seconds, each with voltage noise σ_v:

**σ_slope = σ_v · √(12/N) / T**, so **σ_I = C · σ_slope**

With an ADS1115 16-bit converter at ±2.048 V (62.5 µV per step) and one averaged sample per second:

| C node | 300 s window | 600 s | 1,800 s |
|---|---|---|---|
| 100 pF | 4.2 aA | 1.5 aA | 0.28 aA |
| 470 pF | 20 aA | 6.9 aA | 1.3 aA |
| 1,000 pF | 42 aA | 15 aA | 2.8 aA |

**Noise is not your limit.** The limit is everything else that moves the node: op-amp bias current, insulator leakage, dielectric absorption, temperature drift. Plan on a practical floor of **about 1-10 fA after subtracting a blank run**.

kT/C noise (the charge frozen in when the switch opens) is √(kT/C): 6.4 µV at 100 pF, 5.3 mV on a 0.15 fF cell. It is a one-time offset, not a slope, so it does not limit a leakage measurement.

### 2.4 The enemies of femtoamps, with numbers

| Enemy | Physics | Size | Defence |
|---|---|---|---|
| Op-amp input bias current | The amplifier's own input leaks onto the node | ADA4530-1: ±20 fA max, −40 to 85 °C; ±250 fA max to 125 °C [DATASHEET, 1]. LMP7721: 3 fA typical, ±20 fA max at 25 °C, ±900 fA at 85 °C [DATASHEET, 4]. LMC6001: 25 fA max, 2 pA over temperature [DATASHEET, 5]. | Pick the part for your temperature. Measure it in a blank run and subtract. |
| Insulator surface leakage | Water films and salts on insulators conduct. FR4 and nylon are poor; PTFE, polyethylene and sapphire are good [REPORTED, 11] | 1e13 Ω at 1 V passes 100 fA | Air-wire the node. Touch it only with PTFE. Clean with isopropyl alcohol. Keep relative humidity (RH) below 40% with silica gel. Guard. |
| Guarding | Leakage needs a voltage difference. A guard conductor driven to the node's own voltage leaves none across the insulator | Removes most surface leakage | Surround the node with a guard at the buffer-output voltage. |
| Dielectric absorption (DA) | The capacitor's dielectric "remembers" its past voltage and slowly gives charge back | DA: polypropylene 0.05-0.10%, C0G/NP0 ~0.6%, X7R ~2.5% [REPORTED, 12]. Crude model I_DA ≈ C·DA·ΔV/(ln(1000)·t). At 100 pF: polypropylene 0.12 fA without soak, 2.4 aA with soak; X7R 6 fA without soak. | Use polypropylene or PTFE. *Soak* the node at its start voltage for 10 min first. |
| Gate kickback | The gate-drain capacitance Cgd couples the gate step onto the node | Cgd ≈ 5 pF [UNVERIFIED], 9 V gate step: −429 mV on 100 pF, −95 mV on 470 pF, −45 mV on 1 nF | Use ≥ 470 pF, or a 5 V gate swing. Skip the first 60 s of data. |
| Triboelectric and piezo charge | Moving or flexing cables and insulators make charge [REPORTED, 11] | Can be pA for seconds | Immobilise every wire. Do not touch the tin while logging. |
| Temperature | Leakage rises steeply with temperature: dlnI/dT = Ea/(kT²) | 7.8% per K at 0.6 eV | Hold the block within ±0.2 K. Log its temperature. |
| Light | Photons make junction current | Room light on an open junction can exceed pA | The closed cookie tin is dark. Keep it closed. |
| Capacitor leakage | Film-capacitor insulation resistance is huge but finite [UNVERIFIED] | Unknown for your part | The blank run includes it. If the blank is high, change the capacitor or build an air capacitor (two 75 × 75 mm plates 0.5 mm apart on PTFE spacers ≈ 100 pF). |

### 2.5 Law 3: Arrhenius, and what Ea tells you

Thermally generated leakage follows **I = I0 · exp(−Ea / kT)**, with k = 8.617e-5 eV/K.

| Ea | ×I per +10 K near 25 °C | ×I from 25 to 85 °C | What it suggests |
|---|---|---|---|
| ≈ 0.56 eV | 2.0 | 39 | Silicon generation current in the junction depletion region (Ea ≈ Eg/2) |
| 0.8 eV | 2.8 | 184 | The study's planning value for IGZO |
| ≈ 1.12 eV | 4.1 | 1,485 | Silicon diffusion current (Ea ≈ Eg), usually only when hot |
| < 0.4 eV | small | small | Tunnelling, surface or fixture leakage: suspect your bench |

Measuring Ea is cheap physics: four temperatures and one fit tell you which mechanism dominates. The oxide campaign needs Ea for the same reason: the study had to extrapolate imec's 95 °C data to 105-125 °C using Ea = 0.5-1.1 eV.

### 2.6 Law 4: statistics of the tail

A quantile q_p is the leakage that a fraction p of devices exceeds. Three facts you will meet:

1. **Order-statistic confidence intervals need no distribution model.** For the median of 100 devices, the 95% interval runs from the 40th to the 61st sorted value (the self-test checks this).
2. **To even see the 1e-4 tail you need ~30,000 devices.** P(at least one of n beyond q) = 1 − (1 − p)^n ≥ 0.95 gives n ≥ ln(0.05)/ln(1 − p).
3. **Anything rarer than your sample is a model, not data.** With 100 devices you can bound up to about the 96th percentile from data. A 1e-4 value from 100 devices is a lognormal extrapolation. It is only as good as the lognormal assumption, and tails are exactly where that assumption fails.

| Tail p | n to see ≥ 1 device beyond it (95%) | n for a data-only upper confidence bound | n for ~10 devices beyond it |
|---|---|---|---|
| 1e-1 | 29 | 36 | 100 |
| 1e-2 | 299 | 368 | 1,000 |
| 1e-3 | 2,995 | 3,688 | 10,000 |
| **1e-4** | **29,956** | **36,887** | **100,000** |
| 2e-5 | 149,786 | ~184,000 | 500,000 |

This is why the study's Gate A+ asks for **≥ 1e5 cells per split**: 1e5 is about 10 devices beyond the 1e-4 quantile.

### 2.7 Your predictions, written down before you build

| Quantity | Prediction | Basis |
|---|---|---|
| Bench floor (blank run), ADA4530-1, 25 °C | \|I\| ≤ 20 fA; probably a few fA | [DATASHEET, 1] |
| Noise-limited resolution | 1-20 aA (100-1,000 pF, 600-1,800 s) | [ESTIMATE] |
| Time constant, 10 GΩ × 470 pF | 4.7 s (±10%, the resistor's tolerance) | [ESTIMATE] |
| Kickback, 470 pF node, 9 V gate | ≈ −95 mV | [ESTIMATE], Cgd [UNVERIFIED] |
| 2N7000 off-leakage, 25 °C, 1 V | Median somewhere in 0.1-10 pA, lognormal spread σ_ln ≈ 0.5-1.5 | [ESTIMATE]. Datasheet guarantees only ≤ 1 µA at 48 V [DATASHEET, 8]; a forum post claims "a few pA" [UNVERIFIED, 8] |
| Activation energy, 25-85 °C | 0.55-0.8 eV (generation-dominated) | [ESTIMATE] from silicon physics |
| Leakage at 85 °C vs 25 °C | 39× (0.56 eV) to 184× (0.8 eV) | [ESTIMATE] |
| Highest quantile you can bound from 100 devices | ~q0.96 | [ESTIMATE] |

If your measurement disagrees, that is data. Write down which row and by how much.

---

## 3. What this proves, and what it does NOT prove

| This experiment PROVES (at home) | It does NOT prove |
|---|---|
| The charge-decay method works and you can run it: I = C·dV/dt resolves currents from pA down to ~1-10 fA. | Anything about oxide (IGZO, IGO, ZTO) transistors. Your devices are silicon MOSFETs with a body diode. Oxide TFTs have no junction, and their leakage is channel and trap physics. |
| You can calibrate a current scale (time-constant method) and measure a bench floor (blank). | Attoamp or zeptoamp metrology. The study's cells leak 1e-20 to 1e-17 A. Your floor is ~1e-15 A, 100-100,000x higher. |
| You can turn many measurements into quantiles with honest confidence intervals, and spot a non-lognormal tail. | The 1e-4 or 2e-5 quantile of anything. That needs ≥ 3e4-1e5 devices (section 2.6). |
| You can extract an activation energy and name the leakage mechanism. | Behaviour after the ≤ 400 °C hydrogen, thermal and bonding budget, at 0.01 µm² device size, at 105-125 °C. |
| You can write a better Oxide Tail Spec, because you know what each column costs in time and devices. | Random telegraph noise (RTN) on ns-to-s timescales. That needs fast sampling on small devices. |

**How it scales.** The same method, at 1/670,000 the node capacitance and with on-chip arrays, is how the real campaign works. Section 13 lists the steps: makerspace, then university nanofab external-user access, then a shared wafer lot.

---

## 4. Parts and tools

Prices are approximate snapshots, as of Nov 2026, from the pages in section 14. Check stock before ordering. Electrometer op-amps are often short.

### 4.1 Bench (choose ONE electrometer option)

| Part | Spec that matters | Example part number | ~USD | Where to buy | Tag |
|---|---|---|---|---|---|
| **Electrometer op-amp, option A (best, hot runs)** | Bias ±20 fA max from −40 to 85 °C; built-in guard buffer; SOIC-8 | ADA4530-1ARZ | 18-38 | DigiKey, Mouser, LCSC | [DATASHEET 1, REPORTED 3] |
| SOIC-8 to DIP adapter (for option A) | Lets you bend the input pin up into air | Any SOIC-8 breakout | 1-3 | Adafruit, Amazon | [UNVERIFIED] |
| **Electrometer op-amp, option B (easiest soldering, room temp only)** | 25 fA max at 25 °C (2 pA over temperature); DIP-8 | LMC6001AIN/NOPB | 16-23 | Newark, Farnell; stock is spotty | [DATASHEET 5, REPORTED 5] |
| Electrometer op-amp, alternatives | 3 fA typical / ±20 fA max at 25 °C, ±900 fA at 85 °C (LMP7721); 20 fA max −40 to 85 °C with guard buffer (OPA928) | LMP7721MA/NOPB; OPA928DR | not confirmed | DigiKey, Mouser, TI | [DATASHEET 4, 6]; price [UNVERIFIED] |
| No-solder option (expensive) | Ready-made ADA4530-1 buffer board | ADA4530-1R-EBZ-BUF | 660-700 | DigiKey, Arrow | [REPORTED, 2] |
| Microcontroller | Runs the sequence, logs over USB | Raspberry Pi Pico 2 | 5 | Raspberry Pi resellers | [REPORTED, 9] |
| Analog-to-digital converter | 16-bit, programmable gain, I²C | Adafruit ADS1115 breakout #1085 | 15 | Adafruit, Mouser, DigiKey | [REPORTED, 10] |
| Storage capacitor(s) | Polypropylene film/foil, low DA; 470 pF and 1,000 pF, plus 10-100 nF for hot runs | WIMA FKP2D011001D00 (1,000 pF, 100 V); FKP2D001001D00 (100 pF) | 0.20-0.60 each | Anglia, Rapid, Future, Cytech | [REPORTED, 14] |
| Calibration resistor | 10 GΩ ±10%, 1206 chip | Ohmite HVC1206Z1008KET | 6.75 | DigiKey | [REPORTED, 7] |
| Devices under test | Small N-channel MOSFET, TO-92 legs are easy to air-wire | onsemi 2N7000 (×100); a second brand such as Diotec 2N7000 for a "split" | 0.25 each at 100 (0.62 single) | DigiKey | [REPORTED, 8] |
| Gate driver | NPN level shifter to a 9 V battery | 2N3904 + 10 kΩ + 100 kΩ, 9 V battery | 4 | any | [UNVERIFIED] |
| Bit-line divider | 22 kΩ + 10 kΩ metal film → ~1.03 V | any 1% resistors | 1 | any | [UNVERIFIED] |
| Shield (Faraday cage) | Closed metal box, lid touching all round | Metal cookie or tea tin, ~20 cm | 0-10 | kitchen | |
| Insulation | Solid PTFE rod or sheet for standoffs; PTFE-insulated wire | PTFE rod 10-12 mm; silver-plated PTFE hook-up wire | 10-15 | hardware or hobby stores, Amazon | [UNVERIFIED] |
| Humidity control | Indicating silica gel; a cheap hygrometer | any | 15 | any | [UNVERIFIED] |
| Low-noise cable | Short coax from buffer output to ADC | RG-174 or similar | 5 | any | [UNVERIFIED] |
| Cleaning and handling | 99% isopropyl alcohol, nitrile gloves, plastic tweezers | any | 10 | any | [UNVERIFIED] |

### 4.2 Heater block (for the temperature series)

| Part | Spec that matters | Example | ~USD | Where | Tag |
|---|---|---|---|---|---|
| Heater resistors (2) | 10 Ω, 25 W, aluminium housed | Dale/Arcol HS25 10R | 2.25 each | Surplus Sales, RS | [REPORTED, 16] |
| Power supply | 12 V DC, ≥ 3 A, wall adapter with its own approvals (no mains wiring by you) | any | 10-15 | any | [UNVERIFIED] |
| Heater switch | Logic-level N-MOSFET, ≥ 5 A at 3.3 V gate drive, plus a 100 kΩ gate pull-down | e.g. IRLB8721 | 1-2 | Adafruit, DigiKey | [UNVERIFIED] |
| Thermal fuse | One-shot cut-off at ~100-110 °C, in series with the heater, clamped to the block | any 10 A axial thermal fuse | 1-3 | DigiKey, Amazon | [UNVERIFIED] |
| Temperature sensor | DS18B20 (±0.5 °C absolute; 0.0625 °C steps), stainless probe | Adafruit #381 or equivalent | 4-10 | Adafruit, Pi Hut, Core Electronics | [REPORTED, 15] |
| Aluminium block | ~30 × 30 × 15 mm, drilled for the DUT body and the sensor | scrap 6061 | 5 | makerspace, hardware store | [UNVERIFIED] |
| Insulation | Small foam box *outside* the hot zone, or ceramic-wool pad around the block | XPS foam offcut | 5-10 | hardware store | [UNVERIFIED] |

### 4.3 Tools

Soldering iron (temperature controlled), digital multimeter, flush cutters, plastic tweezers, a hand drill, a PC with Python 3 + numpy and `mpremote` (the MicroPython file tool). No oscilloscope needed.

---

## 5. Build

### 5.1 Circuit

```
                         +9 V battery
                             |
                           100k
  Pico GP16 --10k--+         +----------------------- DUT gate (G)        [write word line]
                   |  2N3904 |
                   +--->|----+  (emitter to GND)      GP16 low  = DUT ON
                                                      GP16 high = DUT OFF

  Pico GP17 --22k--+------------------------------- DUT source (S)        [write bit line]
                  10k                                 GP17 high = ~1.03 V, low = 0 V
                   |
                  GND

          ======= inside the cookie tin, nothing here touches the PCB =======
          DUT drain (D) ===== air wire =====+===== op-amp IN+ (pin bent up, air-wired)
                                             |
                                    C_s 470 pF polypropylene ---- GND
                                             |
                                (optional, for calibration only)
                                    10 GOhm -------- calibration source (GP18 divider)

  op-amp: unity-gain buffer, OUT tied to IN-. Supply 5 V (Pico VBUS) + 100 nF.
  op-amp OUT --1k--> ADS1115 AIN0          (node copy, low impedance)
  op-amp OUT ------> GUARD: copper foil / brass tube around the node wire and the PTFE post
                     (ADA4530-1: use its own guard pins instead)
  ADS1115 SDA/SCL -> Pico GP4/GP5.   DS18B20 -> GP22 (4.7k pull-up).   Heater MOSFET gate -> GP15.
```

Keep the node at 0.5-2 V, inside the op-amp's input range on a single 5 V supply. Check your op-amp's common-mode range in its datasheet [UNVERIFIED for each part].

### 5.2 Mechanical: the craft that decides femtoamps

1. **The tin is the shield.** Drill one hole for a short cable bundle. Ground the tin to the circuit ground at one point.
2. **Mount a PTFE post** (a 15 mm piece of PTFE rod) on the tin floor. The storage node lives on top of it: the capacitor lead, the DUT drain lead and the op-amp input pin meet there.
3. **Air-wire the node.** Bend the op-amp's +IN pin up so it does not touch the socket or board. Solder the node wires to it in free air. FR4 board is a leaky insulator; air is not.
4. **Guard.** Wrap the PTFE post in copper tape connected to the buffer output, so the insulator has no voltage across it.
5. **Clean** every part near the node with 99% isopropyl alcohol and let it dry. Wear gloves: skin salts conduct.
6. **Dry.** Put fresh indicating silica gel and a hygrometer in the tin. Aim for RH < 40%.
7. **Immobilise.** Tape every cable down. Moving cables make charge.
8. **DUT socket.** Clamp the DUT body in a hole in the aluminium block. Its drain lead goes up to the PTFE post in air. The gate and source leads are low-impedance, so ordinary wiring is fine for them.

### 5.3 Mini hot chuck and thermostat (only for runs above room temperature)

Bolt the two 10 Ω heater resistors to the aluminium block. The block sits on PTFE or ceramic standoffs inside the tin, with a small insulating cover over it. The op-amp stays at the far side of the tin, near room temperature. Wire the heaters in parallel to 12 V through the MOSFET and the thermal fuse. That is 2 × 14.4 W = 28.8 W full power, and the firmware caps the duty at 80%. Twist the heater wires together and route them away from the node.

The firmware switches the heater slowly (2 s windows), so there are few switching edges near the femtoamp node. The robust slope fit ignores the occasional spike. The PI gains are a starting point: tune them on your block.

---

## 6. Safety

> **SAFETY: E4**
> - **Voltages.** Everything is USB 5 V, a 9 V battery and a 12 V wall adapter. Never open or modify a mains device. No mains wiring in this build.
> - **Heat and fire.** The block runs at ≤ 85 °C, and the firmware refuses higher setpoints. The heater resistor surfaces can get hotter than the block. Three independent cut-outs: (1) a thermal fuse (~100-110 °C) clamped to the block, in series with the heater; (2) firmware cut-off at 90 °C, and on any sensor fault; (3) the watchdog resets the Pico if the code hangs, and the heater pin then defaults off (100 kΩ pull-down). Keep foam and plastics away from the resistors: polystyrene foam softens near 100 °C. Never leave a heated run unattended until you have watched one complete run end to end. Put the tin on a non-flammable surface with a smoke alarm in the room.
> - **Burns.** Let the block cool below 45 °C before touching it or swapping devices.
> - **Isopropyl alcohol** is flammable (SDS: highly flammable liquid and vapour; eye irritant). Use it with the heater off and cold, in a ventilated room, away from flames. Store it capped. Let small amounts evaporate outdoors or discard as household hazardous waste.
> - **Silica gel** (indicating type) may contain a colour indicator. Read its SDS and don't eat it or let children handle it. Dispose of it in household waste.
> - **Soldering:** use ventilation or a fume extractor, eye protection, and wash your hands (lead solder).
> - **Static:** the electrometer input is easily destroyed by a static discharge. Touch the grounded tin before touching the node.
> - No chemicals beyond these, no vacuum, no cryogens, no lasers.

---

## 7. Procedure

### Phase A: bring-up and the bench floor (day 1-2)

1. Build the circuit in section 5.1, *without* a DUT. Check every supply with the multimeter before inserting the op-amp.
2. Flash MicroPython on the Pico. Copy `e4_pico_leakage_bench.py` and set `MODE = "BLANK"`, `HEATER_ENABLED = False`, `RECORD_S = 3600`, `CAP_PF = 470`.
3. Close the tin. Log: `mpremote run e4_pico_leakage_bench.py > blank_25C_1.csv`. The node floats; you are measuring the bench itself (op-amp bias plus insulation leakage plus capacitor).
4. Repeat 3 times on different days. Analyse: `python3 leakage_tail.py --csv blank_25C_1.csv --cap-pf 470`.
5. **Floor check.** You want |I_blank| ≤ 20 fA, with the runs agreeing within ±5 fA. If not, see section 11.

### Phase B: calibrate the current scale (day 2)

6. Solder the 10 GΩ resistor from the node to the calibration source (GP18 through a divider to ~0.5 V; read it on ADS1115 AIN2). Set `MODE = "TAU_CAL"`.
7. Run it. The node relaxes toward the new source voltage with **τ = R·C_node**. The firmware prints a 63% time-constant estimate; fit the logged curve properly if you like.
8. Compute C_node = τ / 10 GΩ. Expect ~4.7 s for 470 pF. The difference from the capacitor's nominal value is the op-amp input, DUT and wiring capacitance (tens of pF). **Use this measured C_node in all later analysis.** Its ±10% uncertainty (the resistor's tolerance) scales every current equally. It does not change quantile *ratios* or Ea.
9. Remove the resistor (it would swamp any femtoamp measurement). Re-run one blank to confirm the floor is back.
10. *Optional, advanced: femtoamp injection.* Connect a 10 pF capacitor from the node to a slowly ramped voltage, made with a Pico PWM output, a two-stage RC filter and a 100:1 divider. A ramp of 0.1 mV/s injects 10 pF × 0.1 mV/s = 1 fA. Check that the bench reports the expected slope. This tests linearity at the floor.

### Phase C: one device, repeatability (day 3)

11. Insert DUT #1. Set `MODE = "DUT"`, `DEVICE_ID = "Q001"`, `SOAK_S = 600`, `RECORD_S = 1800`.
12. Close the tin and **wait 15 minutes** for handling charge and heat to settle, then start. The firmware soaks the node at ~1.03 V with the gate on, turns the gate off, sets the source to 0 V, and logs.
13. Look at the first minute: you should see the kickback step (≈ −0.1 V), then a straight decline. Run `leakage_tail.py --plan <current>` with your rough current, and change C_s if the droop in 1,800 s is outside ~5-300 mV.
14. Measure the same device 3 times (remove and reinsert it between runs). Repeatability target: within ±20%.

### Phase D: the distribution at room temperature (weeks 1-2)

15. Number 30-120 devices with a marker. If you bought two brands, mix them in random order: a "split".
16. Measure each one as in steps 11-12. Each takes ~55 minutes, so let the Pico run overnight sessions and swap devices morning and evening. Run a BLANK every ~10 devices.
17. Concatenate all CSV files into one (same columns) and analyse:
    `python3 leakage_tail.py --csv all_25C.csv --cap-pf <your C_node> --json results_25C.json`

### Phase E: temperature series and activation energy (weeks 2-4)

18. Pick 10-20 devices spanning the 25 °C distribution: low, median and high leakers, including your top 2.
19. Measure each at 25, 45, 65 and 85 °C (`HEATER_ENABLED = True`, `SETPOINT_C`). Leakage rises ~40-180x by 85 °C, so shorten `RECORD_S` (300-600 s) and use larger C_s (section 2 table) so the droop stays below ~0.3 V. Record each run's capacitance in the `cap_pf` column.
20. Run a BLANK at each temperature. The script subtracts the blank at the matching temperature.
21. Optional "process split": bake half of a fresh batch, unpowered, at 85 °C for 24 h in the block, then remeasure all at 25 °C. That is the home cousin of the study's hydrogen/thermal-dose split.

### Phase F: analysis and your home tail spec (1 evening)

22. Run the analysis on everything:
    `python3 leakage_tail.py --csv all.csv --cap-pf 470 --json all.json`
    It prints per temperature: median, quantiles 0.1/0.5/0.9/0.99, each with order-statistic and bootstrap 95% CIs; the lognormal spread; a lognormality check (probability-plot correlation, PPCC); a *labelled* lognormal extrapolation to the 1e-4 quantile; and Ea per device with its spread.
23. Fill in the home tail spec (section 12), including a pass/kill line you wrote **before** step 15.

---

## 8. Data sheet and log template

**Per-run CSV** (what the firmware prints, what the script reads):

```
device,temperature,time,voltage,cap_pf,temp_meas_C
Q001,25.0,0.00,0.9312345,470.0,25.031
Q001,25.0,1.00,0.9312290,470.0,25.029
...
```

**Lab notebook, one line per run:**

| Date | Run file | Device | Brand/lot | Setpoint °C | Block °C mean ± sd | RH % | C_node pF | V after kickback | Window s | Notes (touched tin? door slam? glitches?) |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

**Calibration record:**

| Date | R (nominal) | τ measured (s) | C_node = τ/R (pF) | Blank I (fA) ×3 | RH % | Op-amp part |
|---|---|---|---|---|---|---|
| | | | | | | |

**Results summary** (copy from the script output):

| T (°C) | n | Below floor | Median | q0.9 [95% CI] | q0.99 [95% CI] | σ_ln | PPCC vs 5% critical | 1e-4 extrapolated (MODEL) |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

| Ea median [95% CI] | Ea IQR | Ea range | Pooled Ea (medians) | Mechanism reading |
|---|---|---|---|---|
| | | | | |

---

## 9. Pass/fail criteria

| Check | Pass | Fail means |
|---|---|---|
| Bench floor | \|I_blank\| ≤ 20 fA (ADA4530-1) or ≤ 50 fA (LMC6001) at 25 °C; 3 blanks agree within ±5 fA | Leakage path or humidity problem: section 11 |
| Calibration | τ within 15% of 10 GΩ × (nominal C_s + ~30 pF); repeatable within 3% | Wrong resistor, leaky node, or a wiring error |
| Linearity (optional ramp test) | Injected 1-10 fA recovered within ±30% | Floor is unstable at that level: quote a higher floor |
| Single-device repeatability | 3 reinsertions agree within ±20% | Handling charge, settling time too short, or a thermal problem |
| Distribution | ≥ 30 devices above the floor; quantile table with CIs produced | Too many devices below the floor: use smaller C, longer windows, or a hotter temperature |
| Arrhenius | ≥ 10 devices with 4 temperatures, per-device R² ≥ 0.95, Ea between 0.4 and 1.3 eV | Temperature not stable, fixture leakage dominating, or a mechanism change (still interesting!) |
| Self-test | `leakage_tail.py --selftest` prints PASS | Python/numpy install problem |

The **experiment succeeds** if you produce the results table with confidence intervals, an Ea with a confidence interval, and a written statement of which quantiles are data and which are model.

---

## 10. What would surprise you (results that would mean something new)

- **Two populations.** A few devices leaking 10-1,000x more than the rest, so the lognormality check fails (the self-test plants exactly this). This is the tail problem in miniature. It shows why the study refuses to extrapolate medians.
- **Leakage that jumps between levels** during a run, as steps in the slope that come and go. That is the transistor version of variable retention time (VRT), the effect the [RAW-BER CONTRACT](../dossiers/raw-ber-contract.md) kill line must include. Seeing it in discrete silicon parts would be a nice result: save those files.
- **Ea below 0.4 eV** with your fixture verified clean. Something other than thermal generation is leaking: tunnelling, or surface leakage on the package.
- **Ea near 1.1 eV at 25-45 °C.** Diffusion current already dominates at room temperature, which is unusual for a small junction.
- **Different distributions for the two brands** at equal median. The tail is a process property, not a device-type property. That is the whole reason the Oxide Tail Spec has channel splits.
- **Leakage that drifts down for hours** after insertion, beyond the dielectric-absorption estimate. That suggests slow surface or trap relaxation, the cousin of oxide-transistor bias-temperature drift.

---

## 11. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Blank current is hundreds of fA or more | Node touches FR4, flux residue, humidity, or a leaky capacitor | Air-wire the node, clean it with IPA, add fresh desiccant, try another capacitor or the air capacitor |
| Blank current changes sign or wanders day to day | Humidity changes, temperature drift, triboelectric charge from moved cables | Log RH, tape the cables down, wait 30 min after closing the tin |
| Node rails (0 V or 5 V) immediately | Op-amp damaged by static, or input outside its common-mode range | Replace it, ground yourself first, keep the node at 0.5-2 V |
| Big step, then a curve that flattens for minutes | Dielectric absorption (no soak) or thermal settling | Use the 10-minute soak; skip 60-120 s; use polypropylene, not ceramic |
| Spikes every few seconds | Heater switching, mains pickup, a phone nearby | Twist the heater leads, close the lid fully, move phones away. Theil-Sen ignores isolated spikes |
| Slope wobbles with a ~minutes period | Heater PI loop oscillating | Lower kp and ki; add thermal mass |
| Node does not reach ~1 V during soak | Gate not fully on (VGS too low) | Check the 9 V level shifter; check 2N7000 pinout (S-G-D, flat side facing you) |
| Huge kickback (> 0.3 V) | Node capacitance too small for the gate swing | Use ≥ 470 pF, or drive the gate from 5 V instead of 9 V |
| Many devices "below floor" | Devices leak less than your floor at 25 °C | Good devices! Measure them hotter, or use smaller C and 1,800 s windows |
| Calibration τ far from expected | Wrong resistor value, or the resistor's own surface leakage | Mount the resistor on PTFE in air; clean it; check its value code |

---

## 12. Rehearsing the Oxide Tail Spec

The study's Monday action is a one-page spec with rows of device structures and columns of splits and conditions ([decision.json](../research/stage3/decision.json)). Fill in the home version first. Then you will know what each column costs.

| Spec column | Real campaign (study) | Your home rehearsal |
|---|---|---|
| Device structures | 2T0C gain-cell arrays; ≥ 1e5 cells per split (Gate A+) | 2N7000 MOSFETs; 30-120 devices |
| Channel splits | IGZO, In-poor IGZO, IGO, Ga-free ZTO | Two brands (onsemi vs Diotec or DComponents), or two lots |
| Device area | ≤ 0.01-0.02 µm² | Not controlled (discrete die) |
| Timescale | ns RTN up to ≥ 1e4 s retention | 300-1,800 s windows |
| Temperature | 85-125 °C; pass lines at 105 and 125 °C | 25, 45, 65, 85 °C |
| Hydrogen / thermal dose | 1x / 2x / 4x H; ≤ 400 °C | Optional: 24 h unpowered bake at 85 °C on half a batch |
| Bond split | Real 350-400 °C fusion bond | Not applicable |
| Pass / kill line | 1e-4-tail retention ≥ 1 s at 105 °C; drift σ ≤ 75 mV; RTN 1e-4 quantile ≤ 100 mV | Write your own before measuring, e.g. "q0.9 at 85 °C ≤ 50 pA, with the upper CI below 100 pA" |
| Statistics | Directly measured 1e-4 quantile | q0.5 and q0.9 with CIs measured; 1e-4 shown only as a labelled extrapolation |

**Sample-size reality** (section 2.6): to *see* the 1e-4 tail at 95% confidence you need 29,956 devices; to put ~10 devices beyond it, 100,000. At 55 minutes per device, your bench would need ~11 years per split. That is the honest reason the real campaign uses on-chip arrays where every cell is its own electrometer and thousands are read in parallel.

---

## 13. Scaling up: what it would take next

| Step | What changes | Who and where | Rough cost | Tag |
|---|---|---|---|---|
| 1. Home, more channels | 4 electrometers (4 × ADA4530-1) on all four ADS1115 inputs: 4x throughput; 100 devices at 65 °C in a week | You | +$100-150 | [ESTIMATE] |
| 2. Makerspace | A real guarded printed circuit board (guard rings, routed slots, solder-mask-free node area), reflow-soldered SOIC parts, a 16-channel reed-relay or source-follower multiplexer for the low-impedance sides | Makerspace with reflow oven and PCB ordering | $200-500 | [ESTIMATE] |
| 3. University lab (external user) | A semiconductor parameter analyser (e.g. Keysight B1500A class, sub-fA resolution) on a probe station with a hot chuck to 125 °C; wafer test structures instead of packaged parts | Nanofab or characterisation facility with external-user access; the judges name Purdue Birck, with Georgia Tech IEN second | Hourly user fees [UNVERIFIED]; the study's physicist budget puts a shared aA floating-node bench with ns sampling and hot chuck at ~$60k | [REPORTED, decision.json] |
| 4. The real thing | On-chip 2T0C arrays, ≥ 1e5 cells per split, read in parallel by their own read transistors: the Oxide Tail Statistics lot | Shared wafer lot at a university fab | ~$210-280k in the judges' budgets | [REPORTED, decision.json] |

**What your home result is worth there.** You will arrive with a working analysis pipeline (`leakage_tail.py` reads any array's decay logs). You will have rehearsed the calibration and blank discipline, and you will have a spec whose sample-size column you have computed yourself. That makes the conversation with a facility shorter and cheaper.

---

## 14. Sources

Prices are snapshots of distributor pages with no guaranteed date; treat them as approximate as of Nov 2026. Several manufacturer sites (analog.com, electricdruid.net) and some reference hosts were blocked from this session, so some specs come from search-engine snippets of the official pages. They are tagged [DATASHEET] when the snippet quotes the maker's datasheet.

1. ADA4530-1 data sheet, Analog Devices: ±20 fA max input bias −40 to +85 °C, ±250 fA max to +125 °C, integrated guard buffer, SOIC-8. https://www.analog.com/media/en/technical-documentation/data-sheets/ADA4530-1.pdf [DATASHEET, via search snippet]
2. ADA4530-1 evaluation boards: ADA4530-1R-EBZ-BUF and -TIA, $699.14 (DigiKey), $659 (Findchips/Arrow). https://www.digikey.com/en/products/detail/analog-devices-inc/ADA4530-1R-EBZ-TIA/ADA4530-1R-EBZ-TIA-ND/5726244 ; https://www.findchips.com/search/ADA4530 [REPORTED]
3. ADA4530-1ARZ chip price ~$31-38 (Mouser/DigiKey snapshots), ~$18-22 (LCSC). https://www.digikey.com/en/products/detail/analog-devices-inc/ADA4530-1ARZ-R7/7404339 ; https://www.lcsc.com/product-detail/C77380.html [REPORTED]
4. LMP7721 data sheet, TI: 3 fA typical, ±20 fA at 25 °C, ±900 fA at 85 °C; guard recommendations. https://www.ti.com/document-viewer/LMP7721/datasheet/specifications [DATASHEET]
5. LMC6001, TI: 25 fA max tested, 2 pA over temperature; ACTIVE, OPA928 suggested as newer. Farnell UK £17.32; Newark $19.28 at 10; BIN grade no longer manufactured per Farnell Japan. https://www.ti.com/product/LMC6001 ; https://uk.farnell.com/texas-instruments/lmc6001ain-nopb/ic-op-amp-single/dp/3117127 ; https://origin-www.findchips.com/detail/LMC6001AIN%2FNOPB/Texas-Instruments ; https://jp.farnell.com/en-JP/texas-instruments/lmc6001bin-nopb/op-amp-single-1-3mhz-1-5v-us-dip/dp/3004668 [DATASHEET / REPORTED]
6. OPA928, TI: 20 fA max −40 to +85 °C, internal guard buffer, SOIC-8; OPA928EVM. https://www.ti.com/product/OPA928 ; https://www.ti.com/tool/OPA928EVM [DATASHEET]; chip price inconsistent across listings [UNVERIFIED]
7. Ohmite HVC1206Z1008KET 10 GΩ ±10% 1206, $6.75 at 1. https://www.digikey.com.br/en/products/detail/ohmite/HVC1206Z1008KET/2709632 ; Ohmite MOX200001007JE 1 GΩ $5.03: https://www.digikey.com/es/products/detail/ohmite/MOX200001007JE/705445 [REPORTED]
8. 2N7000 (onsemi) DigiKey: $0.62 at 1, $0.2466 at 100. https://www.digikey.com/en/products/detail/onsemi/2N7000/244278 [REPORTED]. Datasheet: drain-source leakage ≤ 1 µA at 48 V. https://www2.ensc.sfu.ca/reference/data-sheets/2N7000.PDF [DATASHEET]. "A few pA" off-leakage claim, conditions not given: https://www.electronics-related.com/showthread/sci.electronics.design/671070-1.php [UNVERIFIED]
9. Raspberry Pi Pico 2 (RP2350), $5; 12-bit ADC. https://www.guru3d.com/story/raspberry-pi-pico-2-release-specifications-and-pricing-just ; https://www.cnx-software.com/2024/08/08/raspberry-pi-pico-2-raspberry-pi-rp2350-dual-core-risc-v-or-arm-cortex-m33-microcontroller/ [REPORTED]
10. Adafruit ADS1115 breakout #1085, $14.95. https://www.adafruit.com/product/1085 [REPORTED]
11. Keithley Low Level Measurements Handbook (7th ed.) and Low Current/High Resistance e-handbook: leakage, triboelectric effects, guarding, humidity, insulator choice (PTFE, polyethylene, sapphire; avoid phenolics, nylon). https://xdevs.com/doc/Keithley/LowLevelHandbook_7Ed.pdf ; https://xdevs.com/doc/Keithley/LowCurrentHiResistance_EHandbook.pdf [REPORTED]
12. Dielectric absorption: WIMA table (polypropylene ~0.05-0.10%, NP0 0.6%, X7R 2.5%); Analog Devices on polystyrene/polypropylene/PTFE for sample-and-hold; Silicon Chip overview. https://wima.de/en/?p=7135 ; https://wcm-cce.cldnet.analog.com/media/en/training-seminars/design-handbooks/Op-Amp-Applications/Section7.pdf ; https://siliconchip.com.au/Issue/PE/2021/November/Circuit+Surgery [REPORTED]
13. Community practice, "Measuring nanoamps and below like a Ninja" (EEVblog forum). https://eevblog.com/forum/metrology/measuring-nanoamps-and-below-like-a-ninja/175 [REPORTED]
14. WIMA FKP2 polypropylene prices: 1,000 pF FKP2D011001D00 £0.16 (Anglia), €0.50 (Ormix); 100 pF FKP2D001001D00 ~$0.26 (Cytech, reference price). https://www.anglia-live.com/product/130137001/FKP2D011001D00KSSD/WIMA ; https://www.cytechsystems.com.cn/de/product/fkp2d001001d00jssd [REPORTED]
15. DS18B20 waterproof sensor (Adafruit #381 and compatibles), £3.50-£8.33 / AU$21.51 listings. https://core-electronics.com.au/catalog/product/view/sku/ADA381 ; https://thepihut.com/products/waterproof-ds18b20-digital-temperature-sensor-extras [REPORTED]
16. 10 Ω 25 W aluminium-housed resistor, $2.25 each (Surplus Sales); Arcol HS25 10R (RS). https://www.surplussales.com/items/136509/10-ohm-5-25w-wire-wound-resistor/ ; https://uk.rs-online.com/web/p/chassis-mount-resistors/1623396 [REPORTED]
17. imec capacitor-less IGZO 2T0C DRAM: >400 s retention from an extracted off-current of 3e-19 A/µm, with the read transistor's parasitic capacitance as the storage element (IEDM 2020); >1e3 s and >1e11 cycles (IEDM 2021, Belmonte et al.). https://imec-int.com/en/articles/capacitor-less-igzo-based-dram-cell-excellent-retention-endurance-and-gate-length-scaling ; https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html ; https://dev.eejournal.com/?p=87736 [REPORTED]
18. Word-line capacitive coupling into the 2T0C storage node (SJTU, IEEE EDL 2023). https://sigroup.sjtu.edu.cn/files/EDL_CC_2023.pdf [REPORTED]
19. Study files: [DRAM_MOONSHOT_REPORT.md](../DRAM_MOONSHOT_REPORT.md) section 1; [research/stage3/decision.json](../research/stage3/decision.json) (biggest unknown, Monday action, judge budgets); [dossiers/hot-side-memory.md](../dossiers/hot-side-memory.md) section 2 (75 zA typical, 3.7/12.5 aA tail, 7.5/22.5 aA ceilings, Ea 0.5-1.1 eV range); [dossiers/raw-ber-contract.md](../dossiers/raw-ber-contract.md) (VRT). [MODEL / REPORTED as tagged there]
20. Silicon junction leakage physics (generation current ∝ n_i, Ea ≈ Eg/2; diffusion current ∝ n_i², Ea ≈ Eg; Eg(Si) ≈ 1.12 eV): standard device-physics textbook result (e.g. Sze, *Physics of Semiconductor Devices*). [UNVERIFIED this session; textbook knowledge]
