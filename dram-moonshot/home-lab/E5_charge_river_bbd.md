# E5: A charge river in a chip. Bucket-brigade delay lines as charge-transfer memory

*Home-lab track T2. Written 2026-11-03. Part of the [dram-moonshot](../README.md) study.*

| | |
|---|---|
| **Goal** | Use a bucket-brigade device (BBD) audio delay chip, which is literally a river of charge packets, to (a) measure how much charge each transfer leaves behind (charge transfer efficiency, CTE), and (b) build a working circulating delay-line memory, like the mercury delay lines of the 1940s, and measure how long data survives with and without regeneration, its bit-error rate (BER) against clock speed, and its energy per stored bit. |
| **Why** | The study's [CHARGE-RIVER](../dossiers/charge-river.md) concept stores bits as electron packets marching through an oxide channel. It lives or dies on one number, CTE, and on a regenerated loop. You can measure both kinds of thing on a $5 chip. |
| **Difficulty** | 2 of 5 for the delay-line memory; 3 of 5 for clean CTE numbers. |
| **Time** | Build: 1 weekend. Measurements: 1-2 weekends (the overnight BER runs are unattended). |
| **Cost tier** | About $40-60 without an oscilloscope (prices approximate as of Nov 2026). An oscilloscope with CSV export helps but is optional. |
| **Code** | [code/T2_analysis/ccd_cte.py](code/T2_analysis/ccd_cte.py) (analysis; run `--selftest` and `--expected`), [code/T2_analysis/e5_pico_bbd_memory.py](code/T2_analysis/e5_pico_bbd_memory.py) (MicroPython PIO firmware, untested on hardware) |

**Evidence tags used below.** [DATASHEET] = manufacturer spec, read from a search snippet when the maker's site was not reachable. [REPORTED] = paper, press, distributor or forum page. [ESTIMATE] = our arithmetic, mostly printed by `ccd_cte.py --expected`. [UNVERIFIED] = could not confirm this session. [MODEL] = from the study's own models. Numbered sources are in section 14.

---

## 0. The idea in one paragraph

A BBD is a chain of 1,024 (or 4,096) tiny capacitors joined by transistor switches. A two-phase clock passes a charge packet from each bucket to the next, like a bucket brigade passing water. Guitar pedals use them to delay sound by tens of milliseconds. Feed it bits instead of music, read each bit at the far end, decide 1 or 0, and push a fresh, full-size packet back in at the start. Now you have a memory where the bit is a packet that keeps moving. That is how EDSAC's mercury delay lines stored 576 bits per tank in 1949 [REPORTED, 12]. It is also the CHARGE-RIVER idea, minus the oxide, the 3D hole and the 313-electron packets.

---

## 1. How this connects to the study

From the [CHARGE-RIVER dossier](../dossiers/charge-river.md) [MODEL / REPORTED as tagged there]:

| Study quantity | Value |
|---|---|
| Transfers per read (32-stage segment, 3 phases) | 98 |
| Packet size | ~313 electrons (imec's vertical IGZO CCD holds "a few thousand") |
| Minimum per-transfer CTE (GO floor, with decision-feedback equalisation, DFE) | 0.9970 |
| STRONG GO | CTE ≥ 0.999 |
| One-way 64-stage fallback | CTE ≥ 0.9987 |
| imec IEDM 2024 planar 142-bit IGZO CCD | "CTE >98%", undefined: per transfer or end to end? (>200 s, >1e10 cycles, >6.25 MHz) |
| Demo gate | A regenerated 98-transfer loop logs raw BER ≤ 5e-10 for ≥ 1e12 decisions at 50 MHz |
| Energy target | 45 fJ recycled shift per bit read; DRAM refresh is 46 fJ/bit per 64 ms |

**What E5 gives you.** The *measurement methods* for both gates: CTE extraction from trailing charge (the "extended pixel edge response", EPER, method used on astronomy CCDs [REPORTED, 10]), and a regenerated-loop BER test with honest zero-error statistics. It also gives you a physical feel for why regeneration is non-negotiable, and why energy scales with C·V².

---

## 2. First principles

All numbers below come from `python3 code/T2_analysis/ccd_cte.py --expected` [ESTIMATE] unless tagged.

### 2.1 Law 1: charge is conserved, but transfer is incomplete

Each transfer moves a fraction (1 − ε) of a packet forward and leaves ε behind. The left-behind charge joins the *next* packet. CTE = 1 − ε. After N transfers, one injected packet is spread over output samples k = 0, 1, 2, … as a negative-binomial distribution:

**h_k = C(N+k−1, k) · (1−ε)^N · ε^k**

Three things you can measure follow from it:

| Observable | Formula | Meaning |
|---|---|---|
| Packet survival | h_0 / Σh = (1−ε)^N ≈ e^(−Nε) | How much of the packet arrives on time |
| First trailing ratio | h_1 / h_0 = N·ε | The "smear": the next sample gets Nε of the packet |
| Frequency response | \|H(f)\| = exp(−Nε(1 − cos 2πf/f_clk)) | Treble loss: −2Nε nepers at the Nyquist frequency |

Your readout (output buffer, ADC, scope) adds its own smear r, which does not grow with N: **h_1/h_0 = N·ε + r**. Measure two or more lengths N and the slope is ε.

| ε (per transfer) | CTE | N = 1024: survival, h1/h0, Nyquist dB | N = 2048 | N = 4096 |
|---|---|---|---|---|
| 3e-5 | 0.99997 | 0.970, 0.031, −0.5 | 0.940, 0.061, −1.1 | 0.884, 0.123, −2.1 |
| 1e-4 | 0.99990 | 0.903, 0.102, −1.8 | 0.815, 0.205, −3.6 | 0.664, 0.410, −7.1 |
| 3e-4 | 0.99970 | 0.735, 0.307, −5.3 | 0.541, 0.614, −10.7 | 0.293, 1.229, −21.4 |
| 1e-3 | 0.99900 | 0.359, 1.024, −17.8 | 0.129, 2.048, −35.6 | 0.017, 4.096, −71.2 |

Audio BBDs pass usable treble at 1024-4096 stages, which suggests ε of order 1e-4 or less. That is our guess [ESTIMATE]: no per-stage figure was verified this session. **Your measurement replaces it.**

### 2.2 Where the loss comes from: predict a U-shaped curve

- **Too fast: incomplete transfer.** In a BBD, a MOSFET passes the charge as a source follower. In strong inversion, the residue falls roughly as 1/t during the half-period t = 1/(2f), so ε rises roughly in proportion to clock frequency f [ESTIMATE, textbook BBD behaviour]. BBD patents also name threshold-voltage modulation by drain voltage, parasitic capacitance, and surface-state trapping [REPORTED, 9].
- **Too slow: leakage.** Junction leakage adds "dark" charge to every bucket in proportion to the time per stage, so level shifts and noise grow as f falls. This is why datasheets give a minimum clock (10 kHz for the V3207 [DATASHEET, 2]).
- **Prediction:** ε is lowest somewhere in the middle of the 10-200 kHz range, and rises at both ends. Oxide CCDs have the same two walls, plus much worse trapping. The dossier's first risk is "oxide traps cap CTE at speed".

### 2.3 How big is a bucket?

The MN3007 reissue's clock input capacitance is ≤ 700 pF [REPORTED, 5]. Spread over 512 buckets per phase, that is ~1.4 pF per bucket [ESTIMATE].

| Quantity | BBD (home) | CHARGE-RIVER (study) |
|---|---|---|
| Packet | 0.3 V on 1.4 pF ≈ 2.6 million electrons | ~313 electrons |
| kT/C noise of one bucket at 300 K | 55 µV ≈ 470 electrons rms | must stay ≤ ~8 electrons of read noise |
| Channel | crystalline silicon MOS | deposited amorphous oxide (IGZO, IGO, ZTO) |
| Clock | 10-200 kHz (datasheet), ~500 kHz practical [REPORTED, 4] | 50 MHz stage clock (150 MT/s) |
| Transfers between regenerations | 1,024-4,096 | 98 |
| CTE needed | (you measure it) | ≥ 0.9970 |

The BBD's own thermal noise is larger than the whole CHARGE-RIVER packet. That one line explains why a BBD cannot test few-electron physics.

### 2.4 Law 2: a stopped bucket is a DRAM cell

Stop the clock and each bucket is a capacitor behind an off switch: a DRAM cell. It loses its margin ΔV in **t_ret = C_b · ΔV / I_leak**.

We do not know the bucket leakage. Bound it from the datasheet: at the 10 kHz minimum clock, the full 1,024-stage delay is 51.2 ms [DATASHEET, 2]. If the designers allowed ≤ 10 mV of leakage drift over that time, then I_leak ≤ 1.4 pF × 10 mV / 51.2 ms ≈ 270 fA [ESTIMATE].

| Bucket leakage | Retention at 25 °C (150 mV margin) | At 60 °C (Ea = 0.6 eV, ~12x faster) |
|---|---|---|
| 270 fA (upper bound) | 0.77 s | 0.07 s |
| 30 fA | 6.8 s | 0.6 s |
| 3 fA | 68 s | 5.9 s |

**Prediction: retention of order 0.1-100 s at room temperature**, the same "seconds" scale as silicon DRAM cells. There will be a spread across buckets, with a weak-bucket tail, exactly the statistics of E4.

### 2.5 Law 3: moving charge costs C·V² per clock cycle

Each clock phase charges and discharges its line capacitance once per cycle. From the supply: **P = 2 · C_clk · V² · f**.

| Case | Clock power | Per stored bit (512 bits) | Per packet-transfer |
|---|---|---|---|
| V3207-class at 5 V, 10 kHz (C_clk assumed = 700 pF) | 0.35 mW (70 µA from 5 V) | 0.68 µW | 34 pJ |
| MN3007 at 15 V, 10 kHz | 3.15 mW | 6.2 µW | 308 pJ |
| DRAM refresh (study: 46 fJ/bit per 64 ms) | | 0.72 pW | |
| CHARGE-RIVER design (45 fJ per 98-transfer read) | | | 0.46 fJ |

A BBD loop uses about a million times DRAM's standby power per bit. Per transfer it costs ~70,000 times the CHARGE-RIVER target. The physics is the same, so the lesson is direct: **energy goes as C·V²**. The study's concept only works with femtofarad plates at about a volt, and with shifting only when data is needed ("park-and-shift"). It is not a free-running clock.

### 2.6 Law 4: regeneration beats decay

**Without regeneration** (output amplified and fed straight back, analog), the impulse spreads further on every lap. The worst-case eye, a lone 0 after many 1s, is 2·(1−ε)^(N·laps) − 1. It closes after **laps = ln 2 / (N·ε)**:

| N, ε | Laps to eye closure | Time at 10 kHz |
|---|---|---|
| 1024, 1e-4 | 6.8 | 0.35 s |
| 4096, 1e-4 | 1.7 | 0.35 s |
| 1024, 1e-3 | 0.7 | 0.03 s |

Any loop-gain error makes it worse, as gain^laps. So **analog recirculation forgets in under a second.**

**With regeneration** (decide 1/0 every lap and re-inject a full packet), the loss is reset every lap. With a one-pass eye of ~240 mV and ~1 mV of noise, the Gaussian error probability is effectively zero. Errors will come from glitches, timing slips, threshold drift and weak buckets, not from thermal noise. **Prediction: zero errors in ≥ 1e9 decisions at 10-100 kHz.**

**Zero-error statistics.** If you see 0 errors in n decisions, the 95% upper limit on BER is about **3/n**. At 10 kHz you make 3.6e7 decisions per hour; overnight at 100 kHz, ~4e9 (BER < ~1e-9). The study's demo needs 1e12 decisions, which at 50 MHz is 5.6 hours.

### 2.7 Your predictions, written down before you build

| Quantity | Prediction | Basis |
|---|---|---|
| Loop length L (V3207) | N/2 = 512 clock periods, plus 0-2 for pipeline | [DATASHEET, 2]: delay = N/(2·f) |
| Delay at 10 kHz | 51.2 ms | [DATASHEET, 2] |
| Per-transfer ε at 10-50 kHz | 1e-5 to 3e-4 (best guess 1e-4): CTE 0.9997-0.99999 | [ESTIMATE] |
| h1/h0 for N = 1024 at ε = 1e-4 | 0.10 plus readout smear | [ESTIMATE] |
| ε against clock | U-shaped; minimum mid-range | [ESTIMATE] |
| Stopped-clock retention, 25 °C | 0.1-100 s, median ~1-10 s; ~12x shorter at 60 °C | [ESTIMATE] |
| Analog loop, no regeneration | Eye closes in ~7 laps (~0.35 s) for N = 1024, sooner with any gain error | [ESTIMATE] |
| Regenerated loop at 10-100 kHz | 0 errors in ≥ 1e9 decisions | [ESTIMATE] |
| Error onset with clock speed | Somewhere between 200 kHz (datasheet max) and ~500 kHz (practical max) | [DATASHEET 2, REPORTED 4] |
| Extra clock-driver current | ~70 µA at 10 kHz, ~0.7 mA at 100 kHz, from 5 V (if C_clk ≈ 700 pF) | [ESTIMATE] |

---

## 3. What this proves, and what it does NOT prove

| This experiment PROVES | It does NOT prove |
|---|---|
| Charge packets can be moved through 1,000-4,000 transfers with measurable, modelable loss. You learn to extract per-transfer CTE with the astronomers' trailing-charge method, and to separate it from readout smear. | Anything about oxide (IGZO) CCD CTE. A BBD is a chain of silicon MOS capacitors and switches, not a CCD, and not an amorphous oxide with band-tail traps. |
| A circulating delay-line memory works: regeneration keeps data indefinitely, and analog recirculation forgets in a few laps. | Few-electron physics. Home packets are ~2.6 million electrons; the study's are ~313. Partition noise and single-trap effects are invisible here. |
| How to state a BER honestly from zero errors (3/n). | Speed. 10-500 kHz here, against 50 MHz needed. Trap emission at 6.7 ns gate dwell is the dossier's open question. |
| A "stopped" charge store is a DRAM cell with a retention-time spread across buckets. | Density, vertical 3D integration, cost, or the LLM-aware scheduler. |
| Energy per transfer scales with C·V², with numbers. | That CHARGE-RIVER's 0.46 fJ per transfer is achievable. |

**How it scales.** The methods carry over unchanged: the same `ccd_cte.py` reads a planar IGZO CCD's output, and the same zero-error BER rule scores the 98-transfer demo. The devices do not. Section 13 has the ladder.

---

## 4. Parts and tools

Prices are approximate snapshots, as of Nov 2026, from section 14. **BBD stock has been tight**: a forum user reported trouble finding V3207D in May 2026 [REPORTED, 4]. Buy 3 chips if you can.

| Part | Spec that matters | Example part number | ~USD | Where to buy | Tag |
|---|---|---|---|---|---|
| BBD, 1,024 stages (×3) | 4-10 V supply; 10-200 kHz clock; up to 51.2 ms delay | Coolaudio V3207D | 2.50-5.50 each (dated listings) | Small Bear, Tayda, Aion, Electric Druid: check stock | [DATASHEET 2]; price [REPORTED 4, historical] |
| BBD, 4,096 stages (optional, for the two-length method) | VDD 5 V typ (4-8 V); VGG = 14/15 VDD; −20 to +60 °C | Coolaudio V3205SD | not found | same shops | [DATASHEET 3]; price [UNVERIFIED] |
| Fallback BBD | 1,024 stages, MN3007-compatible; clock input ≤ 700 pF; needs a higher supply (~15 V class) | Xvive MN3007 | 14.95, in stock at listing time | Amplified Parts | [REPORTED 5]; supply voltage [UNVERIFIED] |
| Microcontroller | PIO state machines make the clock and the regeneration | Raspberry Pi Pico 2 | 5 | Raspberry Pi resellers | [REPORTED, 7] |
| Clock buffer | 5 V outputs, accepts 3.3 V inputs, drives hundreds of pF | 74AHCT125 (DIP-14 or on a breakout) | ~1 | DigiKey, Adafruit | [UNVERIFIED] |
| Comparator | Open-collector output, 5 V supply | LM393 (DIP-8) | ~0.5 | any | [UNVERIFIED] |
| Analog switch + op-amp (for the "no regeneration" analog loop) | 5 V single supply, rail-to-rail op-amp | CD4066B + MCP6002 | ~2 | any | [UNVERIFIED] |
| Passives | Resistors 10k, 22k, 100k; 10k and 20k trimmers; 100 nF, 10 µF, 100 µF caps; ferrite bead | kit | ~10 | any | [UNVERIFIED] |
| Breadboard + jumpers | | | ~10 | any | [UNVERIFIED] |
| Optional: oscilloscope | 2 channels, ≥ 10 MHz, CSV export | any | 60-400 | any | [UNVERIFIED] |
| Optional: warm box | The E4 heater block, held ≤ 60 °C (the BBD's operating limit) | from E4 | 0 | | [DATASHEET, 3] |

**Tools:** soldering iron (for headers), digital multimeter with a µA/mA range, PC with Python 3 + numpy and `mpremote`.

---

## 5. Build

### 5.1 Circuit

Wire the BBD's supply, VGG (if it has one), clock and output pins **exactly as the datasheet's application circuit shows**. These parts are PMOS designs, and pin names and supply polarity conventions differ between families. We could not verify every pinout this session [UNVERIFIED], so the datasheet is the authority.

```
 USB 5 V (Pico VBUS) --ferrite--+--100uF--100nF-- GND
                                +--> BBD supply (per datasheet), 74AHCT125 VCC, LM393 VCC
                                +--> VGG divider/trimmer (V3205SD: VGG = 14/15 of VDD)

 Pico GP2 --> 74AHCT125 buffer --> BBD CP1        (buffer OE pins to GND)
 Pico GP3 --> 74AHCT125 buffer --> BBD CP2

 BBD input node:  5 V --22k--+--22k-- GND          bias ~2.5 V, source resistance 11 kOhm
                             +--100k-- Pico GP4 (DATA): a '1' adds ~ +0.33 V
                             +--[CD4066]-- feedback op-amp output   (analog-loop mode only;
                             |                CD4066 control = Pico GP6)
                             +--> BBD IN

 BBD OUT1 + OUT2 --> datasheet output resistors --> summed node "OUT"
 OUT --10k--> LM393 IN+      threshold trimmer wiper --100k--> LM393 IN-
              LM393 output --10k pull-up to 3.3 V--> Pico GP5 (COMP)
 OUT --10k--+--> Pico GP26 (ADC0)
           22k               divider keeps the ADC input below 3.3 V
            |
           GND
```

Input level check: 2.5 V × 100/111 = 2.25 V for a '0'; plus 3.3 × 11/111 = 0.33 V gives 2.58 V for a '1'. Adjust the bias divider until a slow triangle wave (from the Pico's PWM output through an RC filter) comes out undistorted. That shows you are in the BBD's linear range.

### 5.2 Firmware in one picture

The PIO state machine runs 32 cycles per BBD clock period:

```
 phase A (CLK1 high) 16 cycles: [8 wait][sample COMP][present next DATA bit, 7 wait]
 phase B (CLK2 high) 16 cycles: [16 wait]
```

- **Write mode** shifts bits from the CPU into DATA and shifts COMP samples back.
- **Regen mode** replaces "present next bit" with "copy COMP to DATA" (`mov pins, pins`). The loop then refreshes itself with no CPU involvement, at any clock up to ~500 kHz.
- **Retention mode** stops the state machine. Both clock lines freeze, every bucket holds its charge, and the clock later resumes from the same place.

All programs start and rest in phase A, so switching programs never adds a spurious clock cycle.

---

## 6. Safety

> **SAFETY: E5**
> - **Voltages.** USB 5 V only, or ≤ 15-18 V from a bench supply or battery if you use the MN3007 fallback. Never ≥ 30 V, and no mains wiring.
> - **Heat.** The BBD's operating range ends at +60 °C [DATASHEET, 3]. If you warm it with the E4 block, set ≤ 60 °C and keep all of E4's heater safety measures (thermal fuse, firmware cut-off, supervision).
> - **ADC pin.** Never feed more than 3.3 V into a Pico pin. Check the OUT divider with a multimeter before connecting GP26.
> - **Soldering:** ventilation, eye protection, wash hands after (lead solder).
> - **Static:** BBDs are MOS parts. Touch ground before handling them.
> - No chemicals, no lasers, no high voltage, no vacuum.

---

## 7. Procedure

### Phase A: bring-up (day 1)

1. Build section 5.1 on a breadboard. Check 5 V, VGG and the input bias (~2.25 V) with the multimeter before inserting the BBD.
2. Flash MicroPython on the Pico. Set `MODE = "cte"`, `N_STAGES = 1024`, `F_REF_HZ = 10000`, and run `mpremote run e5_pico_bbd_memory.py > cte_1024_10k.csv`.
3. Plot the `value` column (any spreadsheet). You should see a flat baseline with a pulse every 32 samples. No pulses means no clock, a wrong pinout, or bias outside range. Check them in that order.
4. Read the '0' and '1' output levels from the ADC data, or with a multimeter in `clock` mode. Set the comparator threshold trimmer to their midpoint.

### Phase B: loop length (day 1)

5. Set `MODE = "delay"`. It writes a pseudo-random sequence and finds the loop length L by correlation. Expect L ≈ 512-514 with agreement ≥ 0.99. Put that L into `LOOP_LEN`.

### Phase C: charge transfer efficiency (day 2)

6. **Single chip, sampling-phase check.** Capture `cte` at 10 kHz. Analyse:
   `python3 ccd_cte.py --samples cte_1024_10k.csv --fold-period 32 --skip 0`
   Note h1/h0 and ε. If you have a scope, capture the output with the clock on channel 2 and analyse it at two sampling phases:
   `python3 ccd_cte.py --scope cap.csv --nstages 1024 --phase 0.25 --fold-period 32` (then `--phase 0.4`).
   If h1/h0 does not change with phase, and lead/main ≈ 0, readout smear is small at this clock.
7. **Two lengths.** Repeat with two V3207s in series (2,048 stages; chip 1's output feeds chip 2's input through the same bias network as section 5.1; both chips share the clock) and, if you have one, a V3205SD (4,096 stages). Put all runs in one CSV with their `n_stages`. The script fits h1/h0 against N: **the slope is ε, the intercept is the readout smear.** Caveat: the series chain adds one chip-to-chip interface, and the V3205SD is a different design. Report the single-chip result too, and compare.
8. **Clock sweep.** Repeat step 6 at 5, 10, 20, 50, 100 and 200 kHz. Plot ε against f and look for the U-shape.
9. **Compare** with the study bar: GO ≥ 0.9970, STRONG GO ≥ 0.999 per transfer. Record how far above (or below) the silicon BBD sits.

### Phase D: the delay-line memory with regeneration (days 3-4, overnight)

10. Set `MODE = "loop"`, `F_RUN_HZ = 10000`, `STORE_S = 60`. It writes a 512-bit pattern, regenerates it for 60 s, reads it back and prints errors and BER per bit per lap.
11. Repeat with `STORE_S = 600`, then an overnight `STORE_S = 36000` at `F_RUN_HZ = 100000` (~3.6e9 decisions).
12. **BER against clock speed:** `STORE_S = 300` at F_RUN_HZ = 10k, 50k, 100k, 200k, 300k, 400k, 500k. Find where errors start.

### Phase E: without regeneration (day 4)

13. **Analog loop.** Add the CD4066 and an MCP6002 gain stage: BBD OUT, AC-coupled, gain set by a trimmer, back into the input node. Set `MODE = "analog"`. Plot `value` lap by lap: the square pattern smears and drifts. Count the laps until a threshold can no longer separate 1s from 0s. Compare with ln 2/(Nε) using your measured ε.
14. **Stopped clock (retention).** Set `MODE = "retention"` and run `HOLD_S` = 0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100 s. The firmware prints the error count, the direction of each error (1→0 or 0→1) and *which positions* failed. Each position is one bucket.
15. Repeat step 14 three times per hold time, and on all three chips. For each bucket, its retention time is the shortest hold at which it failed. Build the retention-time distribution: median, 10th percentile, weakest bucket.
16. *Optional, warm:* repeat steps 14-15 at 40, 50 and 60 °C in the E4 block (≤ 60 °C). Fit an Arrhenius Ea to the median retention time. Leakage-limited retention gives Ea ≈ 0.5-0.8 eV.

### Phase F: energy per bit (day 5)

17. Put the multimeter (µA/mA range) in series with the 74AHCT125's 5 V supply. Set `MODE = "clock"` at F_RUN_HZ = 10k, 50k and 100k, and read the current with the clock running and stopped.
18. The clock-driver current rises linearly with f: I = 2·C_clk·V·f. The slope gives C_clk, which you compare with the 700 pF assumption. Then energy per stored bit per second = P / 512. Repeat in series with the BBD supply to get its static current.

---

## 8. Data sheet and log templates

**CTE runs** (one file per run, or concatenated; the firmware prints this format):

```
run,n_stages,f_clk_hz,index,value
N1024_10000Hz,1024,10000,0,2.413205
...
```

**CTE summary:**

| Run | N | f_clk (kHz) | Sampling phase | Reps | Amplitude (mV) | lead/main | h1/h0 | ε (h1/h0) | ε (fit) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

| f_clk | Multi-length ε (slope) | Readout intercept | CTE | vs GO 0.9970 |
|---|---|---|---|---|
| | | | | |

**Loop / BER:**

| Date | Chip | f_run (kHz) | Stored (s) | Laps | Decisions = bits × laps | Errors | BER (or < 3/n) | Temp °C |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

**Retention (stopped clock):**

| Chip | Temp °C | Hold (s) | Run | Errors | 1→0 | 0→1 | Failed positions |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

**Energy:**

| f_run (kHz) | I_clock-driver on (µA) | off (µA) | I_BBD on (µA) | off (µA) | C_clk = ΔI/(2·V·f) (pF) | Power per stored bit (µW) |
|---|---|---|---|---|---|---|
| | | | | | | |

---

## 9. Pass/fail criteria

| Check | Pass | Fail means |
|---|---|---|
| Self-test | `ccd_cte.py --selftest` prints PASS | Python/numpy problem |
| Delay-line works | `delay` mode agreement ≥ 0.99, L within N/2 ± 4 | Wiring, threshold or clock problem: section 11 |
| CTE extracted | lead/main within ±0.01; h1/h0 repeatable within ±10% over 3 captures; ε reported with readout smear separated (multi-length) or shown small (phase check) | Sampling at the wrong phase, or too few repeats |
| Regenerated memory | 0 errors in ≥ 1e8 decisions at 10 kHz (BER < 3e-8); overnight ≥ 1e9 | Glitches, threshold drift or a weak bucket. Positions tell you which |
| Without regeneration | Analog loop loses the pattern in < 20 laps; stopped clock shows a hold time with ≥ 50% errors | If the stopped clock holds > 1,000 s, report it: that is a surprise (section 10) |
| Energy | C_clk from the current slope within 2x of 700 pF | The chip's clock load differs from the MN3007 figure: report your value |

The **experiment succeeds** when you have one CTE number with uncertainty and readout separated, a BER upper limit for the regenerated loop, a retention-time distribution for the stopped clock, and an energy-per-bit figure.

---

## 10. What would surprise you (results that would mean something new)

- **No growth of the trail with N** (slope ≈ 0). The silicon BBD is better than ~1e-5 per transfer and all the smear is readout. Then the BBD is a very clean reference line.
- **A pattern-dependent first-sample deficit**: the first 1 after a long run of 0s comes out smaller than later 1s. That is the "first pixel response" of trapping [REPORTED, 10]. In a silicon BBD it would be surprising. In oxide CCDs it is *the* expected failure mode.
- **Regenerated-loop errors that always hit the same positions.** Weak buckets, the BBD equivalent of DRAM weak cells: the tail problem again.
- **Retention failures that move between buckets from run to run.** That would be variable retention time (VRT), the effect the [RAW-BER CONTRACT](../dossiers/raw-ber-contract.md) has to budget for.
- **Retention much longer than 100 s** at 25 °C. BBD buckets leak less than our upper bound. Re-derive the leakage from your data: I = C_b·ΔV/t.
- **A sharp error cliff with clock speed** rather than a gradual rise. A cliff points to a timing limit (clock edges, comparator delay); a gradual rise points to transfer physics.

---

## 11. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Output is flat; no pulses | No clock, wrong supply polarity or pinout, VGG missing | Re-check against the datasheet; measure the clock pins in `clock` mode (DC average should be ~2.5 V on each) |
| Output pulses distorted or clipped | Input bias outside the linear range | Adjust the bias divider; test with a slow triangle |
| `delay` agreement ~0.5 | Comparator threshold wrong or output inverted | Re-set the threshold to the midpoint; try `INVERT = True` |
| lead/main clearly non-zero | Sampling during an output transition | Use a scope capture with the `--phase` option; try 0.2-0.4 |
| h1/h0 changes with sampling phase | Readout bandwidth smear | Lower the clock, reduce series resistance into the ADC, or use the multi-length slope |
| Errors in `loop` mode at a low clock | Threshold drift with temperature; comparator chatter | Add ~10 mV of hysteresis to the LM393 (a 1 MΩ positive-feedback resistor); re-set the threshold warm |
| Firmware stalls at high clock in write mode | MicroPython cannot keep the FIFOs fed above ~50 kHz | Write and read at `F_REF_HZ` ≤ 20 kHz; only regeneration runs fast (it needs no CPU) |
| Pico resets or USB drops | Clock-driver current spikes on USB 5 V | Add the ferrite and 100 µF; keep the BBD wiring short |

---

## 12. Mapping to the study's CHARGE-RIVER gates

| Dossier gate (charge-river.md) | Home analogue | What carries over |
|---|---|---|
| Median per-transfer CTE ≥ 0.9970 with DFE at ≥ 150 MT/s, 25 and 85 °C | ε from the trailing-charge slope at 5-200 kHz, 25-60 °C | The extraction method and readout separation; the clock-sweep and temperature-sweep design |
| Regenerated 98-transfer loop, raw BER ≤ 5e-10 for ≥ 1e12 decisions | Regenerated 512-bit loop, zero-error BER bound | The 3/n zero-error rule, positional error logging, and the soak-overnight discipline |
| Trap kinetics at short gate dwell | ε rising at high clock | Reading a rise in ε against clock as a time-constant problem |
| Retention: a 20 s scrub needs ≤ 0.25 aA per well | Stopped-clock retention distribution of ~1.4 pF buckets | Retention = C·ΔV/I_leak, and weak-cell tail statistics (E4's `leakage_tail.py` statistics apply) |
| Energy: 45 fJ shift per bit | 34 pJ per packet-transfer measured from C_clk | Energy ∝ C·V²: the case for fF plates and park-and-shift |

---

## 13. Scaling up: what it would take next

| Step | What | Where | Rough cost | Tag |
|---|---|---|---|---|
| 0. Read the papers | Buy imec's IEDM 2024 (planar IGZO CCD) and IMW 2026 (vertical) papers and find out whether ">98%" is per transfer or end to end. The dossier calls this "Step 0 is a $35 paper": it judges P(pass) at ~15-25% if the 98% is per transfer, and ≥ 50% if it is end to end | Home | ~$35 | [REPORTED, study] |
| 1. A real CCD at home | Hobbyist linear CCD image sensors (for example the Toshiba TCD1304, used in DIY spectrometers) have true CCD shift registers. Flash an LED and measure EPER-style CTE on a buried-channel silicon CCD with the same script | Home or makerspace | ~$20-50 | [UNVERIFIED] |
| 2. Oxide trap spectroscopy | 1 ns-1 ms transient measurements on IGZO thin-film transistor coupons at 0-125 °C give trap densities that predict CTE before any CCD exists (dossier months 1-4) | University lab with a pulsed parameter analyser | lab fees [UNVERIFIED] | [REPORTED, study] |
| 3. Planar oxide CCDs on a shared lot | Overlapping-gate IGZO CCDs as a rider on the shared oxide lot, only if step 0 passes | University fab (Purdue Birck, Georgia Tech IEN) | ~$15-40k rider across the three judges' budgets | [REPORTED, decision.json] |
| 4. Regenerator silicon | A sense, decide and re-inject chip at 50 MHz on an open-source-PDK shuttle (e.g. SKY130) or an FPGA front end, for the 98-transfer demo loop | Shuttle program (availability changes: check current providers) | ~$25-85k sky130 lines in the judges' budgets, shared with other concepts | [REPORTED, decision.json]; shuttle availability [UNVERIFIED] |

---

## 14. Sources

Prices are distributor snapshots of uncertain date; treat them as approximate as of Nov 2026. Some hosts (electricdruid.net, analog.com, arxiv.org) could not be fetched from this session, so several specs come from search-engine snippets.

1. Coolaudio BBD family list (V3207 = MN3207 1024-stage; V3205SD = MN3205 4096-stage; V3102 two-phase clock generator). https://sdiy.info/wiki/Coolaudio_International_Ltd. [REPORTED]
2. Coolaudio V3207 data sheet (copy): 1024-stage low-noise BBD, delays up to 51.2 ms, clock 10-200 kHz, supply 4-10 V. https://studylib.net/doc/18495714/v3207-1024-stage-low-noise-bbd-analog-delay-line [DATASHEET, via search snippet]
3. Coolaudio V3205SD data sheet: 4096-stage, VDD 4 / 5 / 8 V (min / typ / max), VGG = 14/15 VDD, operating −20 to +60 °C. https://cdn.mediavalet.com/aunsw/musictribe/cKeOXD_mmkCpntp-nTE6rQ/SFKj7__jTEupvoxPvlB55A/Original/COOLAUDIO_V3205SD_DATASHEET.pdf [DATASHEET, via search snippet]; V3102 data sheet: https://cdn.mediavalet.com/aunsw/musictribe/sqqx9zK0GkyHkAXphmCw0A/jrIhIpN7R0m5p9AUoziLmQ/Original/COOLAUDIO_V3102_DATASHEET.pdf
4. Availability and practice: PedalPCB "V3207D sources" thread (V3207 historical €2.50 at 1-9; Aion $5.35; a user reporting trouble finding V3207D in May 2026). https://forum.pedalpcb.com/threads/v3207d-sources.29316/ ; Electric Druid MN3207 page (200 kHz datasheet maximum; ~500 kHz practical in their lab). https://electricdruid.net/product/mn3207-1024-stage-delay-line/ [REPORTED]
5. Xvive MN3007 reissue, $14.95, in stock at listing time: https://www.amplifiedparts.com/products/integrated-circuit-xvive-mn3007-bbd-1024-stage ; clock input capacitance 700 pF max (MN3005: 2,800 pF): https://www.cedist.com/node/45647 [REPORTED]
6. MN3207 die photo ("1024 stage analog delay line CCD"). https://zeptobars.com/en/read/MN3207-1024-stage-analog-delay-line-CCD [REPORTED]
7. Raspberry Pi Pico 2, $5. https://www.guru3d.com/story/raspberry-pi-pico-2-release-specifications-and-pricing-just [REPORTED]
8. Adafruit ADS1115 #1085 (if you add a 16-bit ADC), $14.95. https://www.adafruit.com/product/1085 [REPORTED]
9. BBD loss mechanisms in patents: surface-state trapping, Vt modulation by VDS, drain-substrate capacitance (US 4,171,229); tetrode BBD (US 4,250,517); inefficiency terms (US 4,709,380). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4171229 ; https://patents.justia.com/patent/4250517 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4709380 [REPORTED]
10. EPER / FPR charge-transfer-inefficiency methods (CTI = deferred charge / (signal × transfers); first-pixel deficit from traps; electronic contamination of the first trail pixels): Euclid Q1 VIS (arXiv 2503.15303); LSST ITL sensors (arXiv 2001.03223); PyAutoCTI docs. https://arxiv.org/pdf/2503.15303 ; https://web3.arxiv.org/pdf/2001.03223 ; https://pyautocti.readthedocs.io/en/latest/overview/overview_3_cti_features.html [REPORTED, via search snippets]
11. LSST serial deferred-charge correction (Snyder et al. 2021), as cited in the study. https://spiedigitallibrary.org/journals/Journal-of-Astronomical-Telescopes-Instruments-and-Systems/volume-7/issue-04/048002/Characterization-and-correction-of-serial-deferred-charge-in-LSST-camera/10.1117/1.JATIS.7.4.048002.full [REPORTED]
12. EDSAC mercury delay lines: 32 tanks of 576 bits, 512 35-bit words (May 1949). https://www.computerhistory.org/storageengine/edsac-computer-employs-delay-line-storage/ ; https://www.cl.cam.ac.uk/events/EDSAC99/simulators/india/arch.html [REPORTED]
13. imec IGZO CCD: IEDM 2024 planar 142-bit 4-phase, "CTE >98%" (undefined): https://imec-publications.be/handle/20.500.12860/59420 ; IMW 2026 vertical IGZO CCD, "a few thousand" electrons: https://www.eejournal.com/industry_news/imec-demonstrates-the-first-3d-implementation-of-a-charge-coupled-device-for-ai-memory-applications/ [REPORTED, as logged in the study dossier]
14. Study files: [dossiers/charge-river.md](../dossiers/charge-river.md) sections 2.3-2.5 and 5 (CTE floor 0.9970, STRONG GO 0.999, 98 transfers, 313 e-, 45 fJ shift, DRAM 46 fJ/bit per 64 ms, BER ≤ 5e-10 demo, $35 paper step); [research/stage3/decision.json](../research/stage3/decision.json) (CCD rider and sky130 budget lines); [dossiers/raw-ber-contract.md](../dossiers/raw-ber-contract.md) (VRT). [MODEL / REPORTED as tagged there]
15. Zero-error confidence bound (the "rule of three": 0 events in n trials gives a 95% upper limit ≈ 3/n): standard statistics. [ESTIMATE]
