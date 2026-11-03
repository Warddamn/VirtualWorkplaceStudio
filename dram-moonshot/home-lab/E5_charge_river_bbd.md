# E5: A charge river in a chip. Bucket-brigade delay lines as charge-transfer memory

*Home-lab track T2. Written 2026-11-03. Part of the [dram-moonshot](../README.md) study.*

| | |
|---|---|
| **Goal** | Use a bucket-brigade device (BBD) audio delay chip, which is literally a river of charge packets, to (a) measure how much charge each transfer leaves behind (charge transfer efficiency, CTE), and (b) build a working circulating delay-line memory, like the mercury delay lines of the 1940s, and measure how long data survives with and without regeneration, its bit-error rate (BER) against clock speed, and its energy per stored bit. |
| **Why** | The study's [CHARGE-RIVER](../dossiers/charge-river.md) concept stores bits as electron packets marching through an oxide channel. It lives or dies on one number, CTE, and on a regenerated loop. You can measure both kinds of thing on a $5 chip. |
| **Difficulty** | 2 of 5 for the delay-line memory; 3 of 5 for clean CTE numbers. |
| **Time** | Build: 1 weekend. Measurements: 1-2 weekends (the overnight BER runs are unattended). |
| **Cost tier** | About $40-60 without an oscilloscope (prices approximate as of Nov 2026). An oscilloscope with CSV export helps but is optional. |
| **Code** | [code/T2_analysis/ccd_cte.py](code/T2_analysis/ccd_cte.py) (analysis; run `--selftest` and `--expected`; `--retention` for stopped-clock logs), [code/T2_analysis/e5_pico_bbd_memory.py](code/T2_analysis/e5_pico_bbd_memory.py) (MicroPython PIO firmware, untested on hardware) |

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

Your readout (output buffer, ADC, scope) adds its own smear r, which does not grow with N: **h_1/h_0 = N·ε + r**. If two lengths share an identical readout, the slope against N is ε. A series chain adds an interface smear r_if that a single chip lacks, so its slope is ε + r_if/1,024: an upper bound, not a clean separation. The cleanest honest number comes from one chip: **ε ≤ (h1/h0)/1,024**. Readout smear only adds to h1/h0, so this holds whenever lead/main ≈ 0 and no trailing sample is negative. At h1/h0 = 0.10 it already gives ε ≤ 1e-4, 30x inside the GO bar.

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

We could not find the V3207's clock input capacitance [UNVERIFIED]. The 15 V MN3007 is ≤ 700 pF [REPORTED, 5], giving ≤ 1.4 pF per bucket over 512 buckets per phase: treat that as an upper bound for the V3207. Step 18 measures C_clk; bucket ≈ C_clk/512 (an upper bound, since the clock line also drives gates).

| Quantity | BBD (home) | CHARGE-RIVER (study) |
|---|---|---|
| Bucket | ≤ 1.4 pF; 0.1 pF if C_clk is only ~50 pF | femtofarads |
| Packet | 0.3 V on 0.1-1.4 pF ≈ 190,000 to 2.6 million electrons | ~313 electrons |
| kT/C noise of one bucket at 300 K | 127-470 electrons rms (0.1-1.4 pF) | must stay ≤ ~8 electrons of read noise |
| Channel | crystalline silicon MOS | deposited amorphous oxide (IGZO, IGO, ZTO) |
| Clock | 10-200 kHz (datasheet), ~500 kHz practical [REPORTED, 4] | 50 MHz stage clock (150 MT/s) |
| Transfers between regenerations | 1,024-4,096 | 98 |
| CTE needed | (you measure it) | ≥ 0.9970 |

If the bucket is ≥ 0.61 pF, one bucket's kT/C noise (≥ 313 e-) is as large as the whole CHARGE-RIVER packet. At 0.1 pF it is still 127 e-, 40% of it. Either way the home packet is ≥ ~190,000 electrons, 600x bigger, so a BBD cannot test few-electron physics.

### 2.4 Law 2: a stopped bucket is a DRAM cell

Stop the clock and each bucket is a capacitor behind an off switch: a DRAM cell. It loses its margin ΔV in **t_ret = C_b · ΔV / I_leak**.

This formula holds for junction leakage. In a stopped BBD, half the transfer transistors stay at their source-follower cutoff and keep conducting slightly (subthreshold), so expect a **common-mode drift that grows with log(hold time)**, tens of mV per decade [ESTIMATE, textbook BBD subthreshold transfer], on top of it. Junction leakage also pulls every bucket the same way. With a fixed comparator threshold, the errors will then likely come as a near-simultaneous, one-direction cliff, set mostly by where the threshold sits, not as a per-bucket weak-cell tail. That is why step 15 logs analog levels and separates the two.

We do not know the bucket leakage. Bound it from the datasheet: at the 10 kHz minimum clock, the full 1,024-stage delay is 51.2 ms [DATASHEET, 2]. If the designers allowed ≤ 10 mV of leakage drift over that time, then I_leak ≤ 1.4 pF × 10 mV / 51.2 ms ≈ 270 fA [ESTIMATE].

| Bucket leakage | Retention at 25 °C (150 mV margin) | At 60 °C (Ea = 0.6 eV, ~12x faster) |
|---|---|---|
| 270 fA (upper bound) | 0.77 s | 0.07 s |
| 30 fA | 6.8 s | 0.6 s |
| 3 fA | 68 s | 5.9 s |

The 0.77 s row does not depend on the bucket size: C_b cancels between the bound and the retention time. The 30 fA and 3 fA rows assume 1.4 pF and scale with C_b.

**Prediction: retention of order 0.1-100 s at room temperature**, the same "seconds" scale as silicon DRAM cells. There will be a spread across buckets, with a weak-bucket tail, exactly the statistics of E4.

### 2.5 Law 3: moving charge costs C·V² per clock cycle

Each clock phase charges and discharges its line capacitance once per cycle. From the supply: **P = 2 · C_clk · V² · f**.

| Case | Clock power | Per stored bit (512 bits) | Per packet-transfer |
|---|---|---|---|
| V3207-class at 5 V, 10 kHz, if C_clk ≤ 700 pF | ≤ 0.35 mW (≤ 70 µA from 5 V) | ≤ 0.68 µW | ≤ 34 pJ |
| MN3007 at 15 V, 10 kHz (C_clk ≤ 700 pF) | ≤ 3.15 mW | ≤ 6.2 µW | ≤ 308 pJ |
| DRAM refresh (study: 46 fJ/bit per 64 ms) | | 0.72 pW | |
| CHARGE-RIVER design (45 fJ per 98-transfer read) | | | 0.46 fJ |

The BBD rows are upper bounds that scale linearly with your measured C_clk. At the bound, a BBD loop uses about a million times DRAM's standby power per bit, and per transfer it costs ~70,000 times the CHARGE-RIVER target. The physics is the same, so the lesson is direct: **energy goes as C·V²**. The study's concept only works with femtofarad plates at about a volt, and with shifting only when data is needed ("park-and-shift"). It is not a free-running clock.

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
| Error onset with clock speed | With an LM393: a timing cliff near 150-300 kHz from comparator delay (~0.3-1.3 µs plus the pull-up rise). The BBD's own limit lies between 200 kHz (datasheet max) and ~500 kHz (practical). To see BBD physics above ~150 kHz, set `REGEN_LATE = True` (decide at cycle 14 of 16) or use a faster comparator such as the TLV3201 (~40 ns, push-pull) [UNVERIFIED, 18] | [ESTIMATE]; [DATASHEET 2, REPORTED 4]; LM393 timing [DATASHEET from memory, 17] |
| Extra clock-driver current | ≤ ~70 µA at 10 kHz, ≤ ~0.7 mA at 100 kHz, from 5 V (if C_clk ≤ 700 pF); scales with your C_clk | [ESTIMATE] |
| Bucket size from C_clk | C_clk/512: ≤ 1.4 pF | [ESTIMATE], [REPORTED 5] |

---

## 3. What this proves, and what it does NOT prove

| This experiment PROVES | It does NOT prove |
|---|---|
| Charge packets can be moved through 1,000-4,000 transfers with measurable, modelable loss. You learn to extract per-transfer CTE with the astronomers' trailing-charge method, and to bound it honestly against readout smear. | Anything about oxide (IGZO) CCD CTE. A BBD is a chain of silicon MOS capacitors and switches, not a CCD, and not an amorphous oxide with band-tail traps. |
| A circulating delay-line memory works: regeneration keeps data indefinitely, and analog recirculation forgets in a few laps. | Few-electron physics. Home packets are ~190,000 to 2.6 million electrons; the study's are ~313. Partition noise and single-trap effects are invisible here. |

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
| BBD, 4,096 stages (optional, a separate chip: not a third "length") | VDD 5 V typ (4-8 V); VGG = 14/15 VDD; −20 to +60 °C | Coolaudio V3205SD | not found | same shops | [DATASHEET 3]; price [UNVERIFIED] |
| Fallback BBD (advanced) | **NOT compatible with the 5 V circuit in section 5.1.** It needs a ~15 V supply on its own fused rail; a 15 V clock swing (an MN3101-class clock driver, or a CD40109B level shifter powered at 15 V); its own input bias divider from 15 V; a re-biased comparator input; and an ADC divider of at least 5:1, e.g. 47 kΩ over 10 kΩ (2.6 V at 15 V). With the section 5.1 divider a 15 V output would put ~8.9 V on GP26 and can destroy the pin. Try it only after the V3207 version works | Xvive MN3007 | 14.95, in stock at listing time | Amplified Parts | [REPORTED 5]; supply and driver details [UNVERIFIED] |
| Microcontroller | PIO state machines make the clock and the regeneration | Raspberry Pi Pico 2 | 5 | Raspberry Pi resellers | [REPORTED, 7] |
| Clock and logic buffer | 5 V outputs, accepts 3.3 V inputs, drives hundreds of pF. Channels: CLK1, CLK2, and the CD4066 control | 74AHCT125 (DIP-14 or on a breakout) | ~1 | DigiKey, Adafruit | [UNVERIFIED] |
| Comparator | Open-collector output, 5 V supply. Inputs must stay below Vcc − 1.5 V = 3.5 V | LM393 (DIP-8) | ~0.5 | any | [DATASHEET from memory, 17] |
| Analog switch + op-amp (optional analog loop, step 13) | 5 V single supply, rail-to-rail op-amp. The CD4066B on 5 V needs ≥ 3.5 V on its control pin, so drive it from the 74AHCT125, or use a 74HCT4066, whose control accepts 3.3 V | CD4066B (or 74HCT4066) + MCP6002 | ~2 | any | [UNVERIFIED, 16] |
| Passives | Resistors 10k, 15k, 22k, 100k; a 10 kΩ 25-turn trimmer (3296 style) for the threshold; a 20 kΩ trimmer; 1 µF film cap; 100 nF, 10 µF, 100 µF caps; ferrite bead; a 10 Ω resistor as a current shunt | kit | ~12 | any | [UNVERIFIED] |
| Breadboard + jumpers | | | ~10 | any | [UNVERIFIED] |
| Optional: oscilloscope | 2 channels, ≥ 10 MHz, CSV export. Needed for the 50-200 kHz CTE points | any | 60-400 | any | [UNVERIFIED] |
| Optional: warm box | A second Raspberry Pi Pico 2 (~$5) running the E4 firmware in `HEAT_ONLY` mode with `SETPOINT_C` ≤ 60 and `MAX_SETPOINT_C = 60`, plus the E4 heater parts and all its safety cut-outs | from E4 + a Pico 2 | ~5 plus E4 heater parts | | [DATASHEET 3] for the V3205SD's 60 °C limit |

**Tools:** soldering iron (for headers), digital multimeter with mV and mA ranges, PC with Python 3 + numpy and `mpremote`.

---

## 5. Build

### 5.1 Circuit

Wire the BBD's supply, VGG (if it has one), clock and output pins **exactly as the datasheet's application circuit shows**. These parts are PMOS designs, and pin names and supply polarity conventions differ between families. We could not verify every pinout this session [UNVERIFIED], so the datasheet is the authority.

```
 USB 5 V (Pico VBUS) --ferrite--+--100uF--100nF-- GND
                                +--> BBD supply (per datasheet), 74AHCT125 VCC, LM393 VCC, CD4066 VDD
                                +--> VGG divider/trimmer (V3205SD: VGG = 14/15 of VDD)

 Pico GP2 --> 74AHCT125 buffer 1 --> BBD CP1        (all four buffer OE pins to GND)
 Pico GP3 --> 74AHCT125 buffer 2 --> BBD CP2
 Pico GP6 --> 74AHCT125 buffer 3 --> CD4066 control (5 V logic; analog-loop mode only)
              74AHCT125 buffer 4 input --> GND (unused)

 BBD input node:  5 V --22k--+--22k-- GND          bias ~2.5 V, source resistance 11 kOhm
                             +--100k-- Pico GP4 (DATA): a '1' adds ~ +0.33 V
                             +--[CD4066 switch A]-- feedback op-amp output (analog-loop mode only)
                             +--> BBD IN
              CD4066: the three unused control pins and their switch pins to GND

 BBD OUT1 + OUT2 --> datasheet output resistors --> summed node "OUT"
 OUT --10k--> LM393 IN+      threshold trimmer wiper --100k--> LM393 IN-
              LM393 output --10k pull-up to 3.3 V--> Pico GP5 (COMP)
 OUT --15k--+--> Pico GP26 (ADC0)
           22k               5 V at OUT gives 2.97 V at GP26; real OUT = ADC volts x 37/22
            |
           GND
```

Input level check: 2.5 V × 100/111 = 2.25 V for a '0'; plus 3.3 × 11/111 = 0.33 V gives 2.58 V for a '1'. Adjust the bias divider until a slow triangle wave (from the Pico's PWM output through an RC filter) comes out undistorted. That shows you are in the BBD's linear range.

**Comparator input range.** On a 5 V supply the LM393's inputs must stay below about 3.5 V (Vcc − 1.5 V) [DATASHEET from memory, 17]. Measure OUT's DC level. If it sits higher, feed IN+ through a 2:1 divider (10k/10k) and take the threshold from the same divided range (halve V_th in step 4).

**Why the 74AHCT125 drives the CD4066.** A CD4066B on 5 V needs at least 3.5 V on its control pin for a solid "on" [UNVERIFIED, 16]. The Pico gives 3.3 V, which may leave the switch half-on with a high resistance. The spare buffer turns GP6 into a 5 V logic level.

### 5.2 Firmware in one picture

The PIO state machine runs 32 cycles per BBD clock period:

```
 phase A (CLK1 high) 16 cycles: [8 wait][sample COMP][present next DATA bit, 7 wait]
 phase B (CLK2 high) 16 cycles: [16 wait]
```

- **Write mode** shifts bits from the CPU into DATA and shifts COMP samples back.
- **Regen mode** replaces "present next bit" with "copy COMP to DATA" (`mov pins, pins`). The loop then refreshes itself with no CPU involvement. With an LM393 it works up to roughly 150-300 kHz [ESTIMATE]: above that, the comparator's decision arrives after the sample point and the loop slips one bit. `REGEN_LATE = True` moves the decision to cycle 14 of 16, which buys the comparator more time.
- **Retention mode** stops the state machine. Both clock lines freeze, every bucket holds its charge, and the clock later resumes from the same place.
- **CTE capture** reads the Pico's ADC in a hard interrupt once per clock. That is valid only up to ~10-20 kHz: hard-interrupt entry plus the handler take of order 10-20 µs [ESTIMATE], so at faster clocks the sample point moves and interrupts merge. The firmware counts the interrupts and prints a WARNING if any clock periods went unsampled.

All programs start and rest in phase A, so switching programs never adds a spurious clock cycle.

---

## 6. Safety

> **SAFETY: E5**
> - **Voltages.** USB 5 V only for the V3207 build. The MN3007 fallback needs ~15 V: keep it on its own fused rail from a bench supply or battery, never ≥ 30 V, and check every Pico pin with the multimeter before connecting it. No mains wiring.
> - **Heat.** The V3205SD's operating range ends at +60 °C [DATASHEET, 3]; the V3207's own limit was not verified [UNVERIFIED]: stay ≤ 60 °C. If you warm it with the E4 block, run the E4 firmware with `MAX_SETPOINT_C = 60`, and keep all of E4's heater safety measures (thermostat, thermal fuse, firmware cut-off, supervision).
> - **ADC pin.** Never feed more than 3.3 V into a Pico pin. Check the OUT divider with a multimeter before connecting GP26. With the MN3007 (15 V class) the divider must be at least 5:1, e.g. 47 kΩ over 10 kΩ: the section 5.1 divider would put ~8.9 V on GP26 and can destroy the pin.
> - **Push-pull comparators.** If you swap in a faster push-pull comparator, power it from 3.3 V so its output cannot put 5 V on GP5.
> - **Soldering:** ventilation, eye protection, wash hands after (lead solder).
> - **Static:** BBDs are MOS parts. Touch ground before handling them.
> - No chemicals, no lasers, no high voltage, no vacuum.

---

## 7. Procedure

> **Protect your data.** Turn off PC sleep and overnight update restarts while logging (macOS: `caffeinate -i mpremote run ...`; Linux: `systemd-inhibit mpremote run ...`; Windows: never sleep when plugged in, pause updates). Use a new file name for every run with `tee`, never `>`, which silently overwrites: `mpremote run e5_pico_bbd_memory.py | tee 2026-11-03_cte_1024_10k_r1.csv`. Copy the folder to a second drive daily.

### Phase A: bring-up (day 1)

1. Build section 5.1 on a breadboard. Check 5 V, VGG and the input bias (~2.25 V) with the multimeter before inserting the BBD.
2. Flash MicroPython on the Pico. Set `MODE = "cte"`, `N_STAGES = 1024`, `F_REF_HZ = 10000`, and run `mpremote run e5_pico_bbd_memory.py | tee 2026-11-03_cte_1024_10k_r1.csv`.
3. Plot the `value` column (any spreadsheet). You should see a flat baseline with a pulse every 32 samples. No pulses means no clock, a wrong pinout, or bias outside range. Check them in that order.
4. **Set the comparator threshold.** (a) From the cte CSV, baseline = the median value and pulse = peak minus baseline. Convert to real volts at OUT: real = value × 37/22 (× 1.682, for the 15k/22k divider; × 32/22 if you kept a 10k/22k one). (b) V_th = real baseline + real pulse / 2. (c) Put the multimeter between GND and LM393 pin 2 (IN− of comparator A) and turn the trimmer until it reads V_th ± 5 mV. Measure at the pin, not at the trimmer wiper: the LM393's input bias current (up to ~250 nA [UNVERIFIED, 17]) through the 100 kΩ shifts IN− by up to ~25 mV. Use a 10 kΩ 25-turn trimmer (3296 style).

### Phase B: loop length (day 1)

5. Set `MODE = "delay"`. It writes a pseudo-random sequence and finds the loop length L by correlation. Expect L ≈ 512-514 with agreement ≥ 0.99. Put that L into `LOOP_LEN`.

### Phase C: charge transfer efficiency (day 2)

6. **Single chip, sampling-phase check.** Capture `cte` at 10 kHz. Analyse:
   `python3 ccd_cte.py --samples 2026-11-03_cte_1024_10k_r1.csv --fold-period 32 --skip 0`
   Note h1/h0 and the one-chip bound **ε ≤ (h1/h0)/1,024** (the script marks it "bound OK" when lead/main ≈ 0 and no trailing sample is negative). If you have a scope, capture the output with the clock on channel 2 and analyse it at two sampling phases:
   `python3 ccd_cte.py --scope cap.csv --nstages 1024 --phase 0.25 --fold-period 32` (then `--phase 0.4`).
   If h1/h0 does not change with phase, and lead/main ≈ 0, readout smear is small at this clock.
7. **Two lengths (optional).** Repeat with two V3207s in series (2,048 stages; chip 1's output feeds chip 2's input through the same bias network as section 5.1; both chips share the clock). Put both runs in one CSV with their `n_stages`. The script fits h1/h0 against N: **the slope is ε plus the interface smear divided by 1,024 (an upper bound on ε)**; the intercept is the single-chip readout smear. Treat a V3205SD as a separate chip with its own one-chip bound, not as a third length. Report the single-chip bound as your main number.
8. **Clock sweep.** With the Pico ADC path, use 10 kHz, and 15 and 20 kHz only if lead/main stays within ±0.01 and the firmware prints no "not sampled" WARNING. For 50, 100 and 200 kHz use the oscilloscope path (`--scope`, step 6). 5 kHz is below the V3207's 10 kHz datasheet minimum: run it only as a deliberate probe of the leakage wall, and label it out of spec. Plot ε against f and look for the U-shape.
9. **Compare** with the study bar: GO ≥ 0.9970, STRONG GO ≥ 0.999 per transfer. Record how far above (or below) the silicon BBD sits.

### Phase D: the delay-line memory with regeneration (days 3-4, overnight)

10. Set `MODE = "loop"`, `F_RUN_HZ = 10000`, `STORE_S = 60`. It writes a 512-bit pattern, regenerates it for 60 s, reads it back and prints errors and BER per bit per lap.
11. Repeat with `STORE_S = 600`, then an overnight `STORE_S = 36000` at `F_RUN_HZ = 100000` (~3.6e9 decisions), logged with `tee` to a new file and with PC sleep off (box above).
12. **BER against clock speed:** `STORE_S = 300` at F_RUN_HZ = 10k, 50k, 100k, 200k, 300k, 400k, 500k. Find where errors start. If they start near 150-300 kHz, suspect the comparator first: repeat with `REGEN_LATE = True` and see whether the cliff moves.

### Phase E: without regeneration (day 4)

13. *Analog loop (advanced, optional).* The stopped-clock test (steps 14-15) is the required "without regeneration" result; this one needs a hand-trimmed gain. Build the gain stage below [ESTIMATE values], set `MODE = "analog"`, `ANALOG_LAPS = 3`, and adjust the trimmer until the lap-2 pulse height equals lap 1 within ±2%. Keep it slightly **below** 1 and below clipping: above 1.00 the pattern grows and clips, and a clipping loop is a crude regenerator, not an analog delay line. Then set `ANALOG_LAPS = 12` and plot `value` lap by lap: the square pattern smears and drifts. Count the laps until a threshold can no longer separate 1s from 0s. Compare with ln 2/(Nε) using your measured ε.
    ```
     OUT --1uF film--+--> MCP6002 IN+ (half A)       2.5 V ref: 5 V --10k--+--10k-- GND
                     |                                                     +--10uF-- GND
                    100k --> 2.5 V ref
     MCP6002 OUT --10k--20k trimmer--+--> MCP6002 IN-
                                     +--10k--10uF--> 2.5 V ref     (AC gain 2-4, DC gain 1)
     MCP6002 OUT --> CD4066 switch A --> BBD input node
     MCP6002 half B unused: IN+ to the 2.5 V ref, OUT tied to its IN-
    ```
14. **Stopped clock, bits (required).** Set `MODE = "retention"`. The firmware first does a 0.01 s reference hold, which fixes the rotation of the stored pattern **once**. Then it runs every hold in `HOLDS_S` (0.03, 0.1, 0.3, 1, 3, 10, 30, 100 s) and prints, per hold, the errors, the number of 1s written, the 1→0 and 0→1 counts, and *which positions* failed. Each position is one bucket.
15. **Stopped clock, analog levels (required).** Set `MODE = "retention_analog"`: same holds, but it logs the analog level of every bucket. Analyse with `python3 ccd_cte.py --retention ret.csv --cb-pf <C_clk/512 from step 18>`. It splits each change into a common-mode drift (all '1' buckets, all '0' buckets, fitted as a × log10(hold) + b × hold) and a per-bucket residual. The residual is the weak-bucket tail: excess leak ≈ C_b × residual / hold, within the output stage's gain (~2x). Repeat steps 14-15 three times per chip and on all three chips. Report the common-mode drift and the per-bucket tail separately; for each bucket, its retention time is the shortest hold at which it failed.
16. *Optional, warm:* repeat steps 14-15 at 40, 50 and 60 °C. Use a second Pico running the E4 firmware with `MODE = "HEAT_ONLY"`, `HEATER_ENABLED = True`, `SETPOINT_C` ≤ 60, `MAX_SETPOINT_C = 60` and `HOLD_HEAT_S` longer than your runs; it holds the block at the setpoint once it is stable. Mount the BBD on a small perfboard with 10 cm leads and press it against the block with a thermal pad. Keep the breadboard outside the warm zone. Fit an Arrhenius Ea to the median retention time and to the residual tail. Leakage-limited retention gives Ea ≈ 0.5-0.8 eV.

### Phase F: energy per bit (day 5)

17. Put a 10 Ω shunt resistor in the 74AHCT125's 5 V lead and read the voltage across it with the multimeter on mV (1 mV = 100 µA), or use the mA range. Do not use the µA range: its shunt (~100 Ω-1 kΩ) drops 0.1-2 V and starves the driver. Set `MODE = "clock"` at F_RUN_HZ = 10k, 50k and 100k, and read the current with the clock running and stopped.
18. The clock-driver current rises linearly with f: I = 2·C_clk·V·f. Fit the current against f at 10, 50 and 100 kHz and use **only the slope**: the static current that 3.3 V inputs draw in a 5 V AHCT part (up to ~1.35 mA per high input [UNVERIFIED, 19]) does not depend on f and cancels. C_clk = slope / (2·V). Then recompute the bucket size (C_clk/512), the electrons per packet, the kT/C noise and the energy per bit from your C_clk. Repeat in series with the BBD supply to get its static current.

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
