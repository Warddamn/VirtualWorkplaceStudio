# E4: The DRAM cell is an electrometer. A femtoamp leakage bench at home

*Home-lab track T2. Written 2026-11-03. Part of the [dram-moonshot](../README.md) study.*

| | |
|---|---|
| **Goal** | Measure transistor off-leakage down to about 1 fA (1e-15 A) with the charge-decay method used in oxide 2T0C research. Then measure 30-120 identical transistors to get a leakage *distribution*, its quantiles with confidence intervals, and an activation energy. |
| **Why** | It rehearses the study's "Oxide Tail Spec", the measurement that decides 7 of its 10 concepts. Same method and same statistics; cheaper devices. |
| **Difficulty** | 3 of 5 for the first build (op-amp option B, room temperature). 4 of 5 with op-amp option A (fine-pitch soldering, best done at a makerspace) and the heater. The electronics are simple. The craft (shielding, insulation, patience) is the hard part. |
| **Time** | Build: 1-2 weekends (2-3 with the heater). Calibration: 1 day. Data: one device per run (~35 min with a 600 s record), swapped by hand, so about 8 devices on a day you are home. 30 devices ≈ 4 home days; 120 ≈ 15 home days (3-5 weeks part-time). Temperature series: 3-4 h per device for 25-85 °C including cool-down (one unattended `SERIES` run each), so 10 devices ≈ 1-2 weeks. Nights are for blanks and long single runs. Full plan: 6-10 weeks part-time; the 30-device room-temperature version: 2-3 weeks. |
| **Cost tier** | About $105-150 for a room-temperature first build (option B, 30 transistors). About $165-235 for the full bench with heater, option A and 100 transistors. Before shipping and tools; prices approximate as of Nov 2026 [ESTIMATE, sum of the section 4 rows]. |
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

| Case | C | I | dV/dt | Time for a 10 mV drop | Time to drain 0.9 V → 0.45 V |
|---|---|---|---|---|---|
| imec-class 2T0C cell, typical | 0.15 fF | 75 zA | 500 µV/s | 20 s | 900 s |
| Hot-side 1e-4 tail ceiling (1 b, 1 s) | 0.15 fF | 22.5 aA | 0.15 V/s | 0.07 s | 3 s |
| Your bench, blank or low-leakage device | 100 pF | 1 fA | 10 µV/s | 1,000 s | 12.5 h |
| Your bench, typical 2N7000 (default C_s) | 10 nF | 1 pA | 100 µV/s | 100 s | 75 min |
| Your bench, typical 2N7000 on too small a C_s | 470 pF | 1 pA | 2.1 mV/s | 4.7 s | 3.5 min: **drained** |
| Your bench, hot device | 100 nF | 100 pA | 1 mV/s | 10 s | 7.5 min |

A 0.15 fF cell turns 75 zA into 0.5 mV/s. Your 100 pF node is ~670,000 times bigger, so the same slope needs ~670,000 times more current. **The cell is the electrometer. Shrinking the node is what makes attoamps measurable.**

**But the node must also hold the current.** A small C makes a loud slope, and it also empties fast. The buffer is only linear between about 0.45 V and 2.04 V (section 5.1), so a node written to ~0.9 V has ~0.45 V of room. Size the storage capacitor for the current you expect: **C_s ≥ I × T / 0.3 V**, with T the record window. For a 2N7000 at 25 °C (0.1-10 pA expected, 600 s window) that is 0.2-20 nF. For a whole population, size it so the *median* device droops only ~30 mV; then a device 10x leakier still fits. **10 nF polypropylene is the default for 2N7000s.** Keep 470 pF for blanks and for devices already measured below ~50 fA. `leakage_tail.py --plan` does this arithmetic. A node that drains is not "quiet": the firmware stops the run, and the script reports a *lower bound* on the current (sections 7 and 11).

### 2.2 Your bench is a giant 2T0C cell

| 2T0C gain cell (study) | Your bench |
|---|---|
| Write transistor (oxide TFT), off during hold | Device under test (DUT): a 2N7000 MOSFET, off during hold |
| Write word line (WWL), write bit line (WBL) | DUT gate (driven 0 / 9 V), DUT source (driven 1.0 V / 0 V) |
| Storage node = read-transistor gate + parasitics | Storage node = DUT drain + film capacitor + op-amp input |
| Read transistor senses the node without touching it | Electrometer op-amp: its input transistor's gate senses the node |
| Word-line kickback shifts the node when the write gate turns off [REPORTED, 18] | Same effect: ΔV ≈ −[Cgd·(V_node + Vth) + Cds·V_WBL]/C_node. Only the part of the gate swing below V_node + Vth couples; above it the channel still ties the node to the bit line. The bit-line step 1.03 → 0 V couples through the drain-source capacitance Cds. |

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
| 10 nF | 420 aA | 150 aA | 28 aA |

**Noise is not your limit.** The limit is everything else that moves the node: op-amp bias current, capacitor and insulator leakage, dielectric absorption, temperature drift. Plan on **about 1-10 fA after blank subtraction with an air or PTFE capacitor, and expect 10-100 fA [ESTIMATE] with a boxed film capacitor until your blank shows otherwise.**

A big C_s has its own enemy: temperature. Polypropylene's capacitance changes by roughly −200 ppm/K [UNVERIFIED this session], which moves a ~1 V node by ~200 µV per kelvin. On 10 nF a 20 fA blank moves only 3.6 µV in 1,800 s, so **measure the femtoamp floor on 470 pF**, and on 10 nF only check that the blank is far below your devices.

kT/C noise (the charge frozen in when the switch opens) is √(kT/C): 6.4 µV at 100 pF, 5.3 mV on a 0.15 fF cell. It is a one-time offset, not a slope, so it does not limit a leakage measurement.

### 2.4 The enemies of femtoamps, with numbers

| Enemy | Physics | Size | Defence |
|---|---|---|---|
| Op-amp input bias current | The amplifier's own input leaks onto the node | ADA4530-1: ±20 fA max, −40 to 85 °C; ±250 fA max to 125 °C [DATASHEET, 1]. LMP7721: 3 fA typical, ±20 fA max at 25 °C, ±900 fA at 85 °C [DATASHEET, 4]. LMC6001: 25 fA max, 2 pA over temperature [DATASHEET, 5]. | Pick the part for your temperature. Measure it in a blank run and subtract. |
| Insulator surface leakage | Water films and salts on insulators conduct. FR4 and nylon are poor; PTFE, polyethylene and sapphire are good [REPORTED, 11] | 1e13 Ω at 1 V passes 100 fA | Air-wire the node. Touch it only with PTFE. Clean with isopropyl alcohol. Keep relative humidity (RH) below 40% with silica gel. Guard. |
| Guarding | Leakage needs a voltage difference. A guard conductor driven to the node's own voltage leaves none across the insulator | Removes most surface leakage | Surround the node with a guard at the buffer-output voltage. |
| Dielectric absorption (DA) | The capacitor's dielectric "remembers" its past voltage and slowly gives charge back | DA: polypropylene 0.05-0.10%, C0G/NP0 ~0.6%, X7R ~2.5% [REPORTED, 12]. Crude model I_DA ≈ C·DA·ΔV/(ln(1000)·t). At 100 pF: polypropylene 0.12 fA without soak, 2.4 aA with soak; X7R 6 fA without soak. | Use polypropylene or PTFE. *Soak* the node at its start voltage for 10 min first. |
| Kickback at switch-off | Cgd couples the part of the gate swing below V_node + Vth (~2-4 V); Cds couples the bit-line step 1.03 → 0 V | Cgd ≈ 5 pF (2N7000 Crss 4 pF typical, 5 pF max at 25 V [DATASHEET, 26]; larger near 1 V) × 2-4 V: −20 to −40 mV at 470 pF. Plus Cds (10-50 pF near 1 V [ESTIMATE, from Coss 11 pF typical / 25 pF max at 25 V [DATASHEET, 26]]) × 1.03 V: −20 to −110 mV. Total ≈ −0.05 to −0.15 V at 470 pF; −2 to −7 mV at 10 nF. | Use a larger C_s; the gate voltage matters little. Skip the first 60 s of data. |
| Triboelectric and piezo charge | Moving or flexing cables and insulators make charge [REPORTED, 11] | Can be pA for seconds | Immobilise every wire. Do not touch the tin while logging. |
| Temperature | Leakage rises steeply with temperature: dlnI/dT = Ea/(kT²) | 7.8% per K at 0.6 eV | Hold the block within ±0.2 K. Log its temperature. |
| Light | Photons make junction current | Room light on an open junction can exceed pA | The closed cookie tin is dark. Keep it closed. |
| Capacitor leakage | Film-capacitor insulation resistance is huge but finite. The epoxy end seal and the plastic box are extra surface-leakage paths. | WIMA FKP 2: insulation resistance ≥ 5×10^5 MΩ at 20 °C [REPORTED, 21: retailer copies of the WIMA data], i.e. ≤ 1.8 pA guaranteed at 0.9 V. Usually far lower, but not guaranteed at fA. Your blank measures it. | The blank run includes it. If the blank is high, change the capacitor or build an air capacitor (two 75 × 75 mm plates 0.5 mm apart on PTFE spacers ≈ 100 pF). |

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
| Bench floor (blank), ADA4530-1, 25 °C, 470 pF | ≤ 20 fA with a PTFE-spaced air capacitor. With a boxed film capacitor, anywhere from a few fA to a few hundred fA, so the blank decides | [DATASHEET 1] + capacitor insulation [REPORTED, 21] |
| Noise-limited resolution | 0.3-15 aA on 100-1,000 pF (600-1,800 s); 28-150 aA on 10 nF | [ESTIMATE] |
| Time constant, 10 GΩ × 470 pF | 4.7 s (±10%, the resistor's tolerance). At 10 nF it is 100 s: measure that capacitor with a multimeter instead | [ESTIMATE] |
| Kickback | ≈ −0.05 to −0.15 V at 470 pF; −2 to −7 mV at 10 nF (gate and bit-line steps) | [ESTIMATE], capacitances [DATASHEET, 26] |
| 2N7000 off-leakage, 25 °C, 1 V | Median somewhere in 0.1-10 pA, lognormal spread σ_ln ≈ 0.5-1.5. So C_s = 10 nF by default; on 470 pF a 1 pA device drains in ~3.5 min | [ESTIMATE]. Datasheet guarantees only ≤ 1 µA at 48 V [DATASHEET, 8]; a forum post claims "a few pA" [UNVERIFIED, 8] |
| Activation energy, 25-85 °C | 0.55-0.8 eV (generation-dominated) | [ESTIMATE] from silicon physics |
| Leakage at 85 °C vs 25 °C | 39× (0.56 eV) to 184× (0.8 eV) | [ESTIMATE] |
| Highest quantile you can bound from 100 devices | q0.964 = 0.025^(1/100) (two-sided 95%) | [ESTIMATE] |

The 2N7000 row differs on purpose from the planning values in [E2](E2_gain_cell_no_capacitor.md#22-law-1-retention-is-set-by-the-write-switchs-off-leakage) (10 pA-10 nA at ~3 V) and [E8](E8_your_own_oxide_gain_cell_memory.md#14-temperature-arrhenius) (10 pA). All three rest on the same thin evidence: the datasheet gives only ≤ 1 µA at 48 V. E4 sizes its capacitor for the lower, 1 V case; E2 and E8 plan for a leakier part. Your measurement replaces all three.

If your measurement disagrees, that is data. Write down which row and by how much.

---

## 3. What this proves, and what it does NOT prove

| This experiment PROVES (at home) | It does NOT prove |
|---|---|
| The charge-decay method works and you can run it: I = C·dV/dt resolves currents from pA down to ~1-10 fA with an air or PTFE capacitor (10-100 fA with a boxed film capacitor, until your blank shows better). | Anything about oxide (IGZO, IGO, ZTO) transistors. Your devices are silicon MOSFETs with a body diode. Oxide TFTs have no junction, and their leakage is channel and trap physics. |
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
| **Electrometer op-amp, option B (your first build: easiest soldering, room temperature only)** | 25 fA max at 25 °C (2 pA over temperature); DIP-8. Before pushing it into a turned-pin socket, bend the +IN pin straight out sideways with flat pliers so it never touches the socket. Check the datasheet for the pin number; +IN is pin 3 on most single op-amps. | LMC6001AIN/NOPB | 16-23 | Newark, Farnell; stock is spotty | [DATASHEET 5, REPORTED 5] |
| Electrometer op-amp, option A (best, hot runs; a makerspace job) | ±20 fA max from −40 to 85 °C; built-in guard buffer; SOIC-8 at 1.27 mm pitch. Do this at a makerspace with a mentor, a magnifier and flux. Either solder every pin except +IN to the breakout, or mount the chip dead-bug (upside down, glued to the PTFE post) and wire each pin with 30 AWG wire. Do not bend a soldered SOIC pin: it snaps. | ADA4530-1ARZ | 18-38 | DigiKey, Mouser, LCSC | [DATASHEET 1, REPORTED 3] |
| SOIC-8 breakout (option A only) | Carries the chip; +IN stays unsoldered | Any SOIC-8 breakout | 1-3 | Adafruit, Amazon | [UNVERIFIED] |
| Electrometer op-amp, alternatives | 3 fA typical / ±20 fA max at 25 °C, ±900 fA at 85 °C (LMP7721); 20 fA max −40 to 85 °C with guard buffer (OPA928) | LMP7721MA/NOPB; OPA928DR | not confirmed | DigiKey, Mouser, TI | [DATASHEET 4, 6]; price [UNVERIFIED] |
| No-solder option (expensive) | Ready-made ADA4530-1 buffer board | ADA4530-1R-EBZ-BUF | 660-700 | DigiKey, Arrow | [REPORTED, 2] |
| Microcontroller | Runs the sequence, logs over USB. The firmware is written for both the Pico and the Pico 2; if the same board will later do E1 or E2, buy the RP2040 Pico (early Pico 2 pins leak, E1 §6.4) | Raspberry Pi Pico 2 or Pico | 5 | Raspberry Pi resellers | [REPORTED, 9] |
| Analog-to-digital converter | 16-bit, programmable gain, I²C. Power it from the Pico's 3.3 V, not 5 V (section 5.1) | Adafruit ADS1115 breakout #1085 | 15 | Adafruit, Mouser, DigiKey | [REPORTED, 10] |
| Temperature sensor | DS18B20 (±0.5 °C absolute; 0.0625 °C steps), stainless probe. **Needed even at room temperature: you log the temperature of every run** (leakage changes ~8% per K) | Adafruit #381 or equivalent | 4-10 | Adafruit, Pi Hut, Core Electronics | [REPORTED, 15] |
| Storage capacitors | Polypropylene film/foil, low DA. **10 nF is the default for 2N7000s.** 470 pF for blanks, the floor check and low-leakage devices; 47 nF and 100 nF for hot runs | WIMA FKP2D011001D00 (1,000 pF, 100 V) and FKP2D001001D00 (100 pF) for small values; 10-100 nF from the WIMA FKP 2 / MKP 2 or KEMET R76 series (check the datasheet says polypropylene) | 0.20-0.60 small; ~0.30-1 for 10-100 nF | Anglia, Rapid, Future, Cytech, DigiKey | [REPORTED, 14]; 10-100 nF price [UNVERIFIED] |
| Write and calibration resistor | 10 GΩ ±10%, 1206 chip. It stays soldered to the node for good | Ohmite HVC1206Z1008KET | 6.75 | DigiKey | [REPORTED, 7] |
| Write and calibration switch | One section of a triple SPDT analog switch whose select input accepts 3.3 V logic on a 5 V supply (TTL-level "HCT" type); DIP-16. Plus a 100 kΩ pull-down on the select line | 74HCT4053 (e.g. CD74HCT4053E) | ~1 | DigiKey, Mouser | [UNVERIFIED, 27] |
| SRC divider and ADC resistor | 2 × 47 kΩ + 10 kΩ (1%) for the 0.49 V / 0.99 V source; 10 kΩ from the buffer output to AIN0 | any metal film | 1 | any | [ESTIMATE] |
| Devices under test | Small N-channel MOSFET, TO-92 legs are easy to air-wire | onsemi 2N7000 (×100); a second brand such as Diotec 2N7000 for a "split" | 0.25 each at 100 (0.62 single) | DigiKey | [REPORTED, 8] |
| Gate driver | NPN level shifter to a 9 V battery | 2N3904 + 10 kΩ + 100 kΩ, 9 V battery | 4 | any | [UNVERIFIED] |
| Bit-line divider | 22 kΩ + 10 kΩ metal film → ~1.03 V | any 1% resistors | 1 | any | [UNVERIFIED] |
| Shield (Faraday cage) | Closed metal box, lid touching all round | Metal cookie or tea tin, ~20 cm | 0-10 | kitchen | |
| Insulation | Solid PTFE rod or sheet for standoffs; PTFE-insulated wire | PTFE rod 10-12 mm; silver-plated PTFE hook-up wire | 10-15 | hardware or hobby stores, Amazon | [UNVERIFIED] |
| Humidity control | **Cobalt-free** indicating silica gel (orange when dry, green or colourless when wet), in a sealed mesh sachet or a small jar with a perforated lid; a cheap hygrometer | any | 15-25 | any | [UNVERIFIED] |
| Low-noise cable | Short coax from buffer output to ADC | RG-174 or similar | 5 | any | [UNVERIFIED] |
| Cleaning and handling | 99% isopropyl alcohol, nitrile gloves, plastic and PTFE tweezers | any | 10 | any | [UNVERIFIED] |

### 4.2 Heater block (for the temperature series)

| Part | Spec that matters | Example | ~USD | Where | Tag |
|---|---|---|---|---|---|
| Heater resistors (2) | 10 Ω, 25 W, aluminium housed. Wired in **series**: 20 Ω on 12 V = 0.6 A, 7.2 W | Dale/Arcol HS25 10R | 2.25 each | Surplus Sales, RS | [REPORTED, 16] |
| Power supply | 12 V DC, ≥ 1 A, a wall adapter with safety marks (UL/ETL/CE/UKCA) and a barrel plug; you add a barrel-jack socket. No mains wiring by you | any | 10-15 | any | [UNVERIFIED] |
| Inline fuse | 1 A (blade or glass) in a holder, at the adapter output | any | 2-4 | any | [UNVERIFIED] |
| Heater switch | Logic-level N-MOSFET, ≥ 5 A at 3.3 V gate drive, plus a 100 kΩ gate pull-down | e.g. IRLB8721 | 1-2 | Adafruit, DigiKey | [UNVERIFIED] |
| Thermostat (hardware cut-out 1) | Normally-closed bimetal disc, opens at ~95 °C, resets itself; clamped to the block | KSD301 / KSD9700 type | 1-2 | Amazon, DigiKey | [UNVERIFIED] |
| Thermal fuse (hardware cut-out 2) | One-shot cut-off rated ~110 °C, clamped to the block; fitted with crimp butt-splices | any 10 A axial thermal fuse | 1-3 | DigiKey, Amazon | [UNVERIFIED] |
| Aluminium block | ~30 × 30 × 15 mm, drilled for the DUT body and the sensor | scrap 6061 | 5 | makerspace, hardware store | [UNVERIFIED] |
| Insulation and cover | Air gap plus an aluminium-foil radiation shield, or a silicone sponge sheet rated ≥ 200 °C. The cover is a folded foil tent or a small steel can. **No ceramic wool, no fibreglass, no polystyrene foam near the block** | kitchen foil; silicone sponge sheet | 0-10 | hardware store, Amazon | [UNVERIFIED] |
| Heater wiring | 20-22 AWG stranded wire, screw terminals, crimp butt-splices | any | 5 | any | [UNVERIFIED] |

The DS18B20 now sits in the core bench list (4.1). For the heater runs it goes into a hole in the block.

### 4.3 Tools

Soldering iron (temperature controlled); digital multimeter with a capacitance range (to measure the 10 nF capacitor); flush cutters; plastic and PTFE tweezers; a hand drill; a small bench vise or two clamps (~$15-25); safety glasses; a deburring tool or file; work gloves; a crimp tool for the butt-splices (heater only); a PC with Python 3 + numpy and `mpremote` (the MicroPython file tool). No oscilloscope needed.

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

  Write/calibration source "SRC":
  3.3 V --47k--+--10k-- GND            GP18 low = SRC ~0.49 V; GP18 high = SRC ~0.99 V
  GP18  --47k--+--> SRC --> 74HCT4053 section "a", input 1 ("A")  and  ADS1115 AIN2
  op-amp OUT -------------> 74HCT4053 section "a", input 0 ("B" = bootstrap)
  GP19 --+----------------> 74HCT4053 select of section "a"   (low = B, high = A)
        100k to GND         4053: VCC = 5 V; VEE, GND and inhibit to GND;
                            unused selects and unused switch pins to GND

          ======= inside the cookie tin, nothing here touches the PCB =======
          DUT drain (D) ===== air wire =====+===== op-amp IN+ (pin bent out, air-wired)
                                             |
                                    C_s 10 nF (or 470 pF) polypropylene ---- GND
                                             |
                                    10 GOhm, stays soldered ---- 4053 section "a" common

  op-amp: unity-gain buffer, OUT tied to IN-. Supply 5 V (Pico VBUS) + 100 nF.
  op-amp OUT --10k--> ADS1115 AIN0          (node copy; the 10k limits current if OUT rails)
  op-amp OUT ------> GUARD: copper foil / brass tube around the node wire and the PTFE post
                     (ADA4530-1: use its own guard pins instead)
  ADS1115 VDD -> Pico 3V3(OUT) (pin 36), GND -> GND.
  ADS1115 SDA/SCL -> Pico GP4/GP5.   DS18B20 -> GP22 (4.7k pull-up to 3.3 V).   Heater MOSFET gate -> GP15.
```

Keep the node at 0.5-2 V, inside the op-amp's input range on a single 5 V supply. Check your op-amp's common-mode range in its datasheet [UNVERIFIED for each part]. The firmware treats 0.45-2.04 V as the valid window: below it the buffer output is near its rail, above it the ADS1115 (±2.048 V range) clips.

**Power the ADS1115 from the Pico's 3.3 V, never from VBUS.** The breakout's I²C pull-ups go to its own supply pin [UNVERIFIED this session], so 5 V there would put 5 V on GP4/GP5, and the Pico's pins must never see 5 V. The 10 kΩ in series with AIN0 limits the current if the 5 V buffer output ever goes above 3.3 V. Its gain error is about 0.2%, constant, because the ADS1115's input impedance is several MΩ on this range [DATASHEET from memory, UNVERIFIED this session, 28]. It scales every current equally, like the C uncertainty.

**The 10 GΩ resistor is the node's write and calibration path.** In position A (GP19 high) its far end sits on SRC: that writes the node in BLANK runs (no device can) and steps it in TAU_CAL. In position B (GP19 low, the default through the pull-down, also after a reset) its far end follows the node through the buffer. It then carries only the buffer's offset voltage divided by 10 GΩ: an offset of 40 µV gives 4 fA [ESTIMATE]. That current is constant and present in every run, including the blanks, so blank subtraction removes it. Its Johnson noise adds a random walk of only ~20 aA over 1,800 s [ESTIMATE]. Check your op-amp's offset in its datasheet: a 1 mV offset would give a constant 100 fA, still subtracted, but then judge the floor by how well the blanks *agree*. You never desolder anything from the cleaned node.

### 5.2 Mechanical: the craft that decides femtoamps

1. **The tin is the shield.** Drill one hole for a short cable bundle, with the tin clamped (Safety box). Ground the tin to the circuit ground at one point.
2. **Mount a PTFE post** (a 15 mm piece of PTFE rod) on the tin floor. The storage node lives on top of it: the capacitor lead, the DUT drain lead, the 10 GΩ resistor's near end and the op-amp input pin meet there.
3. **Air-wire the node.** Option B: bend the op-amp's +IN pin straight out sideways before it goes into the socket, so it touches neither socket nor board. Solder the node wires to it in free air. FR4 board is a leaky insulator; air is not.
4. **Guard.** Wrap the PTFE post in copper tape connected to the buffer output, so the insulator has no voltage across it.
5. **Clean** every part near the node with 99% isopropyl alcohol and let it dry. Wear gloves: skin salts conduct.
6. **Dry.** Put a sealed sachet of fresh cobalt-free (orange) indicating silica gel and a hygrometer in the tin. Aim for RH < 40%.
7. **Immobilise.** Tape every cable down. Moving cables make charge.
8. **DUT socket.** Clamp the DUT body in a hole in the aluminium block. Its drain lead goes up to the PTFE post in air. The gate and source leads are low-impedance, so ordinary wiring is fine for them.
9. **Change the storage capacitor only between phases, never between devices.** It is soldered on the femtoamp node. You fit 470 pF for Phases A-B and 10 nF (or the value `--plan` picks) from Phase C on. After each change: clean with IPA, dry, close the tin, wait an hour, and run one blank.

### 5.3 Mini hot chuck and thermostat (only for runs above room temperature)

Bolt the two 10 Ω heater resistors to the aluminium block and wire them in **series**. 12 V across 20 Ω is 0.6 A and 7.2 W. That is plenty for a ~36 g block (a few W hold 85 °C [ESTIMATE]), and it limits what any fault can do. **Never wire the resistors in parallel:** that makes 28.8 W, four times the stuck-on power, and the home lab allows series heaters only ([SAFETY.md](SAFETY.md#3-heaters-and-thermal-runaway)). If series wiring cannot reach 85 °C, close the foil tent and the gaps, or end the temperature series at 65 °C. The block sits on PTFE or ceramic standoffs inside the tin. The cover over it is a folded aluminium-foil tent or a small steel can, never foam. The op-amp stays at the far side of the tin. Expect the tin's air to warm a few K at an 85 °C setpoint: that is why you run a blank at every setpoint.

**Heater wiring.** Use 20-22 AWG stranded wire, soldered or in screw terminals. Never run heater current through a solderless breadboard or jumper wires: their contacts are rated about 1 A and can overheat [UNVERIFIED]. The chain is: 12 V adapter → barrel-jack socket → 1 A inline fuse → thermal fuse → bimetal thermostat → resistor → resistor → MOSFET drain; MOSFET source → GND. Fit the thermal fuse with crimp butt-splices. If you must solder it, keep at least 10 mm of lead, clamp pliers on the lead between the joint and the body as a heat sink, and touch the iron for under 3 s. Then check that the fuse reads ~0 Ω on the multimeter. Clamp the fuse and the thermostat to the block. Twist the heater wires together and route them away from the node.

**First heat-up, watched.** With the tin closed and you watching, heat to 85 °C once from cold. Note how fast the block rises (expect ~0.1-0.2 K/s [ESTIMATE]) and that it settles without passing ~87 °C. If it cannot reach 85 °C, the firmware's runaway check stops it after 3 min. Then improve the foil tent, or make 65 °C the top point of `SERIES`. Do not switch to parallel wiring.

The firmware switches the heater slowly (2 s windows), so there are few switching edges near the femtoamp node. The robust slope fit ignores the occasional spike. The PI gains are a starting point: tune them on your block.

---

## 6. Safety

> **SAFETY: E4**
> - **Voltages.** USB 5 V, a 9 V battery and a 12 V wall adapter with safety marks. Never open or modify a mains device. No mains wiring in this build.
> - **Heat and fire.** The block runs at ≤ 85 °C, and the firmware refuses higher setpoints. The heater resistor surfaces can get hotter than the block. Protection is **two independent hardware cut-outs**, the bimetal thermostat (~95 °C, resets itself) and the one-shot thermal fuse (~110 °C), both clamped to the block in series with the heater. On top of them sit **firmware checks** (90 °C cut-off, sensor fault, a runaway check) that use the same sensor as the controller. They do not cover a sensor that has slipped out of the block, and a MOSFET that fails short bypasses all firmware. The watchdog only resets a hung Pico (the heater pin then defaults off through its 100 kΩ pull-down). The series wiring limits even a stuck-on heater to 7.2 W.
> - **Heater wiring.** 1 A inline fuse at the adapter output. Never run heater current through a breadboard or jumper wires.
> - **Foam and fibre.** Keep polystyrene (XPS/EPS) foam at least 20 mm from anything that can exceed 60 °C: its maximum service temperature is about 74-75 °C [REPORTED, 23], and it burns with styrene smoke. Do not use ceramic wool: refractory ceramic fibre is classified as a carcinogen when inhaled (EU CLP Carc. 1B, H350i) [REPORTED, 22].
> - **Supervision.** Never leave a heated run unattended until you have watched one complete run end to end. Put the tin on a non-flammable surface with a smoke alarm in the room.
> - **Burns.** Let the block cool below 45 °C before touching it or swapping devices.
> - **Drilling and cutting.** Clamp the tin and the block in a vise, or to the bench with two clamps; never hold them by hand. Wear safety glasses. Use a sharp bit at low speed, with a drop of oil on aluminium. Deburr every hole by twisting a larger bit by hand, or with a file. Handle the cut tin in work gloves, and vacuum up swarf rather than brushing it with your hand. No vise? Drill the block on a makerspace drill press.
> - **Isopropyl alcohol** is flammable (SDS: highly flammable liquid and vapour; eye irritant). Use it with the heater off and cold, in a ventilated room, away from flames. Store it capped. Let small amounts evaporate outdoors or discard as household hazardous waste.
> - **Silica gel.** Buy only the cobalt-free orange type. Do not use blue indicating gel: it contains cobalt(II) chloride, classified as a carcinogen (Carc. 1B) and reproductive toxicant (Repr. 1B) in EU safety data sheets [REPORTED, 24]. Keep sachets closed and out of reach of children and pets (choking hazard). Replace spent gel, or regenerate orange gel on a foil tray at 100-120 °C for 2 h in an oven that never holds food ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment): no equipment that will touch food again). Orange gel can go in household waste.
> - **Soldering:** use ventilation or a fume extractor, eye protection, and wash your hands (lead solder).
> - **Static:** the electrometer input is easily destroyed by a static discharge. Touch the grounded tin before touching the node.
> - No chemicals beyond these, no vacuum, no cryogens, no lasers.

---

## 7. Procedure

> **Protect your data (read before Phase A).**
> 1. Turn off sleep, hibernation and overnight update restarts on the PC while logging. Windows: Settings > System > Power, "never sleep when plugged in", and pause updates. macOS: run the logger as `caffeinate -i mpremote run ...`. Linux: `systemd-inhibit mpremote run ...`.
> 2. Never reuse a file name: put date, device, temperature and run number in it, and use `tee` (it also shows the data live): `mpremote run e4_pico_leakage_bench.py | tee 2026-11-03_Q001_25C_r1.csv`. A plain `>` silently overwrites an old file.
> 3. Copy the CSV folder to a second drive or a cloud folder every day.
> 4. Write each run's file name in the lab notebook before you start it.

### Phase A: bring-up and the bench floor (day 1-2)

1. Build the circuit in section 5.1 *without* a DUT, with C_s = 470 pF. Check every supply with the multimeter before inserting the op-amp. Check SRC with GP18 low and high (~0.49 V and ~0.99 V).
2. Flash MicroPython on the Pico. Copy `e4_pico_leakage_bench.py` and set `MODE = "BLANK"`, `HEATER_ENABLED = False`, `CAP_PF = 470`, `RECORD_S = 3600`.
3. Close the tin, wait 15 minutes, then log: `mpremote run e4_pico_leakage_bench.py | tee 2026-11-03_BLANK_470pF_25C_r1.csv`. With no device, nothing else can set the node, so the firmware writes it to ~0.99 V through the 10 GΩ resistor (switch on A; τ ≈ 4.7 s), soaks, moves the switch to B (bootstrap) and logs. You are measuring the bench itself: op-amp bias, insulation and capacitor leakage, and the constant offset current through the resistor. **The first logged voltage must be 0.5-2.0 V.** The firmware refuses to log outside 0.45-2.04 V, because a railed buffer (near 0 V) or a clipped ADC (2.047 V) looks like a perfect floor.
4. Repeat 3 times on different days. Analyse: `python3 leakage_tail.py --csv 2026-11-03_BLANK_470pF_25C_r1.csv`.
5. **Floor check.** You want |I_blank| ≤ 20 fA, with the runs agreeing within ±5 fA. If not, see section 11.

### Phase B: calibrate the current scale (day 2)

6. Set `MODE = "TAU_CAL"`, `CAL_SETTLE_S = 120`, `CAL_WINDOW_S = 100` (both ≥ 10 τ; τ = 4.7 s at 470 pF). The firmware puts the switch on A, holds SRC low (~0.49 V), steps it to ~0.99 V and logs. Both levels keep the node inside the buffer's linear range.
7. Run it. The node relaxes toward the new source voltage with **τ = R·C_node**. The firmware prints a 63% time-constant estimate. Check it in a spreadsheet: plot ln(V_final − V) against t; the slope is −1/τ.
8. Compute C_node = τ / 10 GΩ. Expect ~4.7 s for 470 pF. The difference from the capacitor's nominal value is the op-amp input and wiring. The DUT is not in yet: its drain adds roughly 30-60 pF near 1 V [ESTIMATE], 6-13% of 470 pF. Either repeat TAU_CAL once with a DUT inserted, gate off and WBL at 0 V (its pA leak is < 2% of the ~50 pA calibration current), or work on C_s ≥ 4.7 nF, where the DUT's share is about 1% or less. **Set `CAP_PF` to your measured value; the firmware writes it into every row, and the analysis uses it.** Its ±10% uncertainty (the resistor's tolerance) scales every current equally. It does not change quantile *ratios* or Ea.
9. **For C_s of 2.2 nF or more** (the 10 nF default), skip TAU_CAL: measure the capacitor on the multimeter's capacitance range before soldering it in. The ~30 pF of wiring plus the DUT's ~30-60 pF is under 1% of 10 nF (about 4% of 2.2 nF). (TAU_CAL would need CAL_SETTLE_S and CAL_WINDOW_S ≥ 1,000 s at 10 nF.) The resistor stays in place either way; re-run one blank to confirm the floor.
10. *Optional, advanced: femtoamp injection.* Connect a 10 pF capacitor from the node to a slowly ramped voltage, made with a Pico PWM output, a two-stage RC filter and a 100:1 divider. A ramp of 0.1 mV/s injects 10 pF × 0.1 mV/s = 1 fA. Check that the bench reports the expected slope. This tests linearity at the floor.

### Phase C: pilot, capacitor choice and repeatability (day 3)

11. Swap C_s to **10 nF** polypropylene (section 5.2, step 9: clean, dry, wait, blank). Measure it with the multimeter first. Insert DUT #1. Set `MODE = "DUT"`, `DEVICE_ID = "Q001"`, `CAP_PF = <measured>`, `SOAK_S = 600`, `RECORD_S = 600`.
12. Close the tin and **wait 15 minutes** for handling charge and heat to settle, then start. The firmware soaks the node at ~1.03 V with the gate on, turns the gate off, sets the source to 0 V, and logs. It **stops by itself** if the node leaves 0.45-2.04 V or falls more than 0.5 V, and says so: that device leaked more than the node can hold.
13. **Pilot.** Measure 3-5 devices this way. In the first minute you should see the kickback step (−2 to −7 mV at 10 nF), then a straight decline. Run `python3 leakage_tail.py --plan <their median current> --window-s 600`. It prints the C_s for a population (median droop ~30 mV, so a device 10x leakier stays under 0.3 V). Expect 2.2-100 nF for medians of 0.1-10 pA [ESTIMATE, from `--plan`]. If it differs from 10 nF by more than ~3x, swap the capacitor **once, now**. Then keep it for the whole population; do not change it between devices.
14. Measure the same device 3 times (remove and reinsert it between runs). Repeatability target: within ±20%.

### Phase D: the distribution at room temperature (weeks 1-2)

15. Number 30-120 devices with a marker. If you bought two brands, mix them in random order: a "split".
16. Measure each one as in steps 11-12. Each takes ~35 minutes (15 min settle, 10 min soak, 10 min record). Swap a device about every 40-60 minutes while you are home; run blanks overnight. Run a BLANK every ~10 devices, on the same capacitor.
17. Concatenate all CSV files into one (same columns; on macOS or Linux, `cat 2026-*_25C_*.csv > all_25C.csv`; the script skips repeated header lines and `#` lines) and analyse:
    `python3 leakage_tail.py --csv all_25C.csv --json results_25C.json`
    The `cap_pf` column already holds your measured C_s. Use `--cap-pf` only to override a whole file (the script warns if the override differs from the column by > 1%).

### Phase E: temperature series and activation energy (weeks 2-4)

18. Pick 10-20 devices spanning the 25 °C distribution: low, median and high leakers, including your top 2.
19. **Without removing the device, measure it at 25, 45, 65 and 85 °C in that order, on one fixed capacitor.** Leakage rises ~40-180x by 85 °C, so choose C_s for the hottest point: run `--plan <I at 85 °C> --window-s 120` and read its "minimum C" line (a device of 1 pA at 25 °C gives I85 ≈ 100 pA and ~40 nF: fit 47 nF). Then `--plan <I at each temperature> --cap-pf <C_s>` prints the longest `RECORD_S` that keeps the droop under 0.3 V. Use `--skip-s 10` for records shorter than 120 s. Set `HEATER_ENABLED = True` and `SERIES = ((25, 1800), (45, 900), (65, 300), (85, 120))` (your numbers): the firmware runs all four in one go and writes the setpoint into the `temperature` column. Afterwards let the block cool below 45 °C before the next swap. Allow 3-4 h per device including cool-down.
20. Run a BLANK at each temperature, on the same capacitor (the tin's air warms a few K at 85 °C). The script subtracts the blank at the matching temperature.
21. Optional "process split": bake half of a fresh batch, unpowered, at 85 °C for 24 h in the block, then remeasure all at 25 °C. That is the home cousin of the study's hydrogen/thermal-dose split.

### Phase F: analysis and your home tail spec (1 evening)

22. Run the analysis on everything:
    `python3 leakage_tail.py --csv all.csv --json all.json`
    It prints per temperature: median, quantiles 0.1/0.5/0.9/0.99, each with order-statistic and bootstrap 95% CIs (the bootstrap is suppressed where it cannot be valid); the lognormal spread; a lognormality check (probability-plot correlation, PPCC); a *labelled* lognormal extrapolation to the 1e-4 quantile; Ea per device with its spread; and how many runs were truncated or drained. Drained runs are *lower bounds*, so with any of them present every upper quantile is a lower bound too.
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

| Date | Run file | Device | Brand/lot | Setpoint °C | Block °C mean ± sd | RH % | C_node pF | V after kickback | Window s | Status (ok / stopped: drained) | Notes (touched tin? door slam? glitches?) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

**Calibration record:**

| Date | R (nominal) | τ measured (s) | C_node = τ/R (pF) | Blank I (fA) ×3 | RH % | Op-amp part |
|---|---|---|---|---|---|---|
| | | | | | | |

**Results summary** (copy from the script output):

| T (°C) | n | Below floor | Truncated / drained | Median | q0.9 [95% CI] | q0.99 [95% CI] | σ_ln | PPCC vs 5% critical | 1e-4 extrapolated (MODEL) |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

| Ea median [95% CI] | Ea IQR | Ea range | Pooled Ea (medians) | Mechanism reading |
|---|---|---|---|---|
| | | | | |

---

## 9. Pass/fail criteria

| Check | Pass | Fail means |
|---|---|---|
| Valid run | First logged voltage 0.5-2.0 V; node never left 0.45-2.04 V. A device may be called "below floor" only if its node drooped < 0.3 V and never left the window | Node never written (BLANK), railed, or drained: re-write it, or use a ~10x larger C_s |
| Bench floor | \|I_blank\| ≤ 20 fA (ADA4530-1) or ≤ 50 fA (LMC6001) at 25 °C on 470 pF; 3 blanks agree within ±5 fA. A constant offset current through the bootstrapped resistor is allowed: agreement matters most | Leakage path or humidity problem: section 11 |
| Calibration | τ within 15% of 10 GΩ × (nominal C_s + ~30 pF), repeatable within 3%; or, for C_s ≥ 2.2 nF, the multimeter reading within the capacitor's tolerance | Wrong resistor, leaky node, or a wiring error |
| Linearity (optional ramp test) | Injected 1-10 fA recovered within ±30% | Floor is unstable at that level: quote a higher floor |
| Single-device repeatability | 3 reinsertions agree within ±20% | Handling charge, settling time too short, or a thermal problem |
| Distribution | ≥ 30 devices measured (not drained) above the floor, all on one fixed C_s; quantile table with CIs produced | Many drained: larger C_s. Many below the floor (and quiet): longer windows or a hotter temperature |
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
| Node reads ~0 V or 2.047 V from the start (firmware says INVALID), or rails during a run | First: a BLANK node never written (check the 4053 select on GP19 and SRC), or a DUT node that drained. Then: input outside the common-mode range. Last: op-amp damaged by static | Re-write the node to ~1 V; use a larger C_s for leaky devices; keep the node at 0.5-2 V. Replace the op-amp only after the rest is ruled out, and ground yourself first |
| Run stops early: "node drained" | The device leaks more than C_s can hold over the window | Re-measure with ~10x larger C_s or a shorter window. Meanwhile the script reports the run as a lower bound |
| No temperature in the CSV | DS18B20 missing or miswired | Fit it (GP22, 4.7 kΩ pull-up): you need the temperature of every run. The firmware keeps running without it |
| Big step, then a curve that flattens for minutes | Dielectric absorption (no soak) or thermal settling | Use the 10-minute soak; skip 60-120 s; use polypropylene, not ceramic |
| Spikes every few seconds | Heater switching, mains pickup, a phone nearby | Twist the heater leads, close the lid fully, move phones away. Theil-Sen ignores isolated spikes |
| Slope wobbles with a ~minutes period | Heater PI loop oscillating | Lower kp and ki; add thermal mass |
| Node does not reach ~1 V during soak | Gate not fully on (VGS too low) | Check the 9 V level shifter; check 2N7000 pinout (S-G-D, flat side facing you) |
| Huge kickback (> 0.3 V) | Node capacitance too small for the gate and bit-line steps | Use a larger C_s (the gate-voltage change matters little) |
| Many devices "below floor" | First rule out a DRAINED node: if v_end < 0.3 V or the node fell more than 0.5 V, the device leaked MORE than the node could hold | Re-measure with 10x larger C_s or a shorter window. Only a run with v_end > 0.5 V and droop < 0.3 V may be called below floor. Then: measure them hotter, or use a smaller C and 1,800 s windows |
| Calibration τ far from expected | Wrong resistor value, the resistor's own surface leakage, or a window shorter than 10 τ | Mount the resistor on PTFE in air; clean it; check its value code. At ≥ 2.2 nF use the multimeter instead |

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

**Sample-size reality** (section 2.6): to *see* the 1e-4 tail at 95% confidence you need 29,956 devices; to put ~10 devices beyond it, 100,000. At ~8 hand-swapped devices a day, your bench would need ~10 years per split. That is the honest reason the real campaign uses on-chip arrays where every cell is its own electrometer and thousands are read in parallel.

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
21. WIMA FKP 2 polypropylene capacitors: insulation resistance ≥ 5×10^5 MΩ at +20 °C (minimum), as quoted on retailer copies of the WIMA data; WIMA's own datasheet was not reached this session. https://www.audiophonics.fr/en/wima-polyester-capacitors/wima-fkp-2-polypropylene-capacitor-5mm-1000v-15nf-p-6043.html ; https://www.audiophonics.fr/en/wima-polyester-capacitors/wima-fkp-2-polypropylene-capacitor-5mm-63v-33nf-p-6045.html ; https://beta.rapidonline.com/wima-fkp2-series-radial-polypropylene-capacitors-62505 (supplied in review, not re-checked) [REPORTED]
22. Refractory ceramic fibre (ceramic wool): EU CLP Carc. 1B (H350i), IARC Group 2B, per manufacturer safety data sheet (Morgan Thermal Ceramics). https://www.morganadvancedmaterials.com/media/12069/203-eu-english.pdf [REPORTED, not re-fetched this session]
23. Extruded polystyrene (XPS) maximum service temperature 165 °F (74 °C) in manufacturer data sheets (Owens Corning FOAMULAR, Sika Sarnatherm); EN 14307 covers XPS up to +75 °C. https://usa.sika.com/dms/getdocument.get/ee9046c9-1165-44a4-8c2d-7d706d6b3c53/sarnatherm_xps.pdf ; https://owenscorning.com/insulation/products/foamular-xps-pipe-insulation-fabrication-billets ; https://www.intertek.com/building/standards/en-14307/ [REPORTED]
24. Blue indicating silica gel (cobalt(II) chloride, ~0.5-1%): safety data sheets classify it Carc. 1B (H350i) and Repr. 1B (H360F). https://static.cymitquimica.com/products/02/pdf/sds-036737.pdf ; https://www.glentham.com/en/products/product/GK0520/datasheet/ [REPORTED]
25. MicroPython driver behaviour: `ds18x20.convert_temp()` calls `ow.reset(True)`, and `OneWire.reset(required=True)` raises `OneWireError` when no device answers. https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/sensor/ds18x20/ds18x20.py ; https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/bus/onewire/onewire.py [REPORTED, source read this session]
26. 2N7000 capacitances (onsemi 2N7000/2N7002/NDS7002A data sheet, VDS = 25 V, VGS = 0, 1 MHz): Ciss 20 pF typ / 50 max; Coss 11 pF typ / 25 max; Crss 4 pF typ / 5 max. https://www.onsemi.com/download/data-sheet/pdf/2n7000-d.pdf ; https://www.onsemi.com/pdf/datasheet/nds7002a-d.pdf [DATASHEET, via search snippet]
27. Logic thresholds: HCT-family parts (74HCT4053) accept TTL levels (high ≥ 2.0 V) on a 5 V supply, so a 3.3 V GPIO drives them; 4000-series CMOS (CD4053B, CD4066B) on 5 V needs ≥ 3.5 V for a high. Standard datasheet values. [UNVERIFIED this session]
28. ADS1115 (TI): input impedance several MΩ on the ±2.048 V range; analog inputs must stay within the supply rails (abs max VDD + 0.3 V). https://www.ti.com/product/ADS1115 [DATASHEET from memory, UNVERIFIED this session]

