# E2: A gain cell without a capacitor

*Track T1, bench electronics. Written 2026-11-03. Prices are approximate as of November 2026.*

**Goal.** Build the BEST BET's memory cell from discrete parts. It is the two-transistor, zero-capacitor gain cell (2T0C):
- one transistor writes charge onto the gate of a second transistor;
- the second transistor's current reports the bit without disturbing it.

Then race four kinds of write switch against each other and see the core result: **retention is set almost entirely by the write switch's off-leakage.** That is the whole reason the study wants wide-bandgap oxide transistors.

| | |
|---|---|
| **Difficulty** | 3 of 5 (4 of 5 with the JFET and its negative rail) |
| **Time** | Build: 4-6 h (6-10 h if this is your first surface-mount or optocoupler build). Runs: 30 min each, more for temperature and 2-bit tests. One weekend |
| **Cost tier** | $$ (about $25-45, plus the shared core kit in [E1](E1_bit_on_the_bench.md) section 5.1; the ALD1106 can be shared with E1) |
| **Board** | Raspberry Pi Pico (RP2040) with MicroPython |
| **Code** | [`code/T1_pico/e2_gain_cell.py`](code/T1_pico/e2_gain_cell.py), [`analyze_t1.py`](code/T1_pico/analyze_t1.py), [`bench_calcs.py`](code/T1_pico/bench_calcs.py) `--section e2` |

**Acronyms.**
- **2T0C:** two transistors, zero capacitors.
- **SN:** storage node.
- **WBL / WWL:** write bitline / write wordline.
- **MOSFET:** metal-oxide-semiconductor field-effect transistor.
- **JFET:** junction field-effect transistor.
- **IGZO:** indium-gallium-zinc oxide, the oxide semiconductor in phone displays.
- **MLC:** multi-level cell, here 2 bits per cell.
- **RTN:** random telegraph noise.
- **GIDL:** gate-induced drain leakage.
- **ADC:** analog-to-digital converter.
- **C0G:** stable ceramic capacitor dielectric.
- **IPA:** isopropyl alcohol.
- **ESD:** electrostatic discharge.
- **SDS:** safety data sheet.

---

## 1. Why this experiment matters to the study

The BEST BET, [hot-side-memory](../dossiers/hot-side-memory.md), stacks oxide 2T0C cells on a GPU.
- **The bit lives on a gate.** A bit is charge on the read transistor's gate, about 0.15 fF.
- **The read is non-destructive.** Reading senses current, "like reading a gauge instead of opening the tap."
- **Retention needs zeptoamp switches.** At 0.15 fF the cell holds data only if the write transistor leaks zeptoamps (1 zA = 1e-21 A). The published oxide cell holds data for >200 s at 95 °C [REPORTED]. That implies ~75 zA [ESTIMATE].
- **Everything hinges on the tail.** The study's biggest unknown is the 1e-4 tail of that leakage ([report](../DRAM_MOONSHOT_REPORT.md), section 1).

**What you can do at home.** You cannot make an IGZO transistor at home. You can build the same circuit, with the same measurement method, and watch the same law decide everything:
- Retention = C × ΔV / I_leak.
- The capacitor is gone, so C is tiny.
- So I_leak must be tinier still.

**The method is the lab method.** The circuit below (a write switch onto a floating gate, read by a source follower) is the "floating-node" test that oxide-transistor developers use to measure zeptoamp leakage. Semiconductor Energy Laboratory patents describe:
- a device under test paired with a write transistor and a source-follower read circuit;
- retention defined as the time for a 0.2 V drop on the node;
- off-currents measured at 85-150 °C and extrapolated to room temperature, about 2 zA/µm [REPORTED, patent text].

---

## 2. First principles and the numbers to expect

Everything below comes from `python3 code/T1_pico/bench_calcs.py --section e2`.

### 2.1 What is the "capacitor" when there is no capacitor?

**The node.** The storage node is the read transistor's gate plus whatever touches it. The read transistor here is a source follower:
- drain at 3.3 V;
- source through 47 kΩ to ground;
- the source voltage goes to the ADC.

**Bootstrapping.** The source follows the gate with gain A ≈ 0.98, so the gate-source capacitance barely charges. It is "bootstrapped away":

```
C_SN(pure) = C_gd + C_gs × (1 - A) + strays ≈ 5 pF + 15 pF × 0.02 + 5 pF ≈ 10 pF   [ESTIMATE]
```

**The trimmed node.** With a known 220 pF C0G capacitor added ("trimmed node"), C_SN ≈ 230 pF.

**Cell A is bigger.** Its 2N7000 write switch has its drain on the node, so the node also carries that switch's Crss (4-5 pF) and its drain-source capacitance C_ds = Coss − Crss (Coss 11 pF typ / 25 pF max [DATASHEET]; C_ds ~6-20 pF at 3 V [ESTIMATE]). Cell A's node is therefore ~21-35 pF pure and ~241-255 pF trimmed. Use `--c-pf 250` for cell A and `--c-pf 230` for cells B and C.

**Why add a capacitor to a "capacitorless" cell?**
1. **Known size.** It makes the node size known, so leakage I = C·dV/dt comes out in absolute units.
2. **Kickback.** It tames kickback (2.4). The physics (t = C·ΔV/I) is identical with or without it. You will also run the pure node once.

### 2.2 Law 1: retention is set by the write switch's off-leakage

```
t_retention = C_SN × ΔV_allowed / I_leak          dV/dt = I_leak / C_SN   ("droop rate")
```

**Expected leakage of each switch, about 3 V across it, 22 °C:**

| Write switch | Low / typical | High / maximum | Basis |
|---|---|---|---|
| A: 2N7000 (ordinary MOSFET) | 10 pA | 10 nA | Datasheet gives only 1 µA max at 48 V [DATASHEET]; real low-voltage value unknown, so this is a planning range [ESTIMATE]. **You will measure it** |
| B: ALD1106 (low-leakage MOSFET) | ~5 pA | 400 pA | 10 pA typ / 400 pA max at 12 V [DATASHEET], scaled to 3.3 V [ESTIMATE] |
| C: 4117-class JFET, gate held at -9 V | ~0.2 pA | 10 pA | Gate leakage ≤ 1 pA (A suffix) or ≤ 10 pA (plain) at -20 V [REPORTED] |
| C': reed relay (the "near-perfect switch") | 0.33 pA | 3.3 pA | Insulation resistance 1e13 Ω typ / 1e12 Ω min [DATASHEET], at 3.3 V. The idle coil (+5 V) can push ~0.2-1.7 pA the other way, INTO the node [ESTIMATE]; step 8 measures it |

**Expected retention (time to lose 100 mV, the study's criterion; and 200 mV, the patent criterion):**

| Write switch | Node | 100 mV at high leakage | 100 mV at low leakage | 200 mV at low leakage |
|---|---|---|---|---|
| 2N7000 (cell A) | pure (~21-35 pF) | 0.2-0.35 ms | 0.2-0.35 s | 0.4-0.7 s |
| 2N7000 (cell A) | trimmed (~250 pF) | 2.5 ms | 2.5 s | 5 s |
| ALD1106 | trimmed | 58 ms | 4.4 s | 8.8 s |
| JFET | trimmed | 2.3 s | **115 s** | 230 s |
| reed relay | trimmed | 7 s | **70 s** | 140 s |
| reed relay | pure | 0.3 s | 3.1 s | 6.2 s |

**The floor.** The read transistor's gate, C_trim and the board. C0G parts are only guaranteed ≥100 GΩ (KEMET [DATASHEET]): up to 33 pA at 3.3 V, which would cap every trimmed cell near 0.7 s. Typical parts are 100-1,000x better, and the 0.01-1 pA planning floor [ESTIMATE] assumes that. Step 3 tells you which you have. If the floor stays above 1 pA after cleaning, try another C0G batch or a polystyrene or polypropylene 220 pF capacitor. The reed-relay cell measures the floor. If the JFET and reed cells come out identical, you have hit it.

**What to expect overall.** A spread of up to **~10,000x or more** in retention, set only by which switch you plug in. How big it is depends mostly on how leaky your 2N7000 really is at 3 V: the planning ranges overlap (2N7000 10 pA-10 nA, ALD1106 5-400 pA), so a quiet 2N7000 can even beat the ALD1106. The datasheet does not say, so that is the first new number you will learn. [E4](E4_femtoamp_leakage_bench.md#27-your-predictions-written-down-before-you-build) plans a lower 2N7000 median (0.1-10 pA at 1 V) from the same thin evidence; the two ranges overlap, and the difference is deliberate (E2 plans for a leaky part at ~3 V).

### 2.3 Law 2: the read does not destroy the bit

**Why.** A MOSFET gate draws femtoamps. Reading means letting current flow drain to source. No charge leaves the storage node.

**Proof.** You toggle the read on and off 10,000 times. The stored value must drift no faster than it does when left alone.

**The catch: capacitive coupling.** When the read transistor's drain jumps between 0 and 3.3 V, it kicks the gate through C_gd. The source also moves by ~1.1 V with it, so C_gs stops being bootstrapped and adds to the kick: ΔV = (C_gd × 3.3 V + C_gs × 1.1 V) / (C_SN + C_gs × A) [ESTIMATE]:
- pure node: ~1.3 V (transient);
- trimmed node: ~135 mV (transient).

The kick returns when the drain returns, because no charge is lost. Real 2T0C arrays have the same read-coupling problem.

### 2.4 Kickback: the write switch's own gate hits the node when it turns off

**The effect.** When the write wordline swings from ON to OFF, the switch's gate-to-node capacitance C_k moves the node:

```
dV = V_swing × C_k / (C_SN + C_k)
```

| Write switch (C_k [ESTIMATE]) | WWL swing | Kick on pure node | Kick on trimmed node |
|---|---|---|---|
| 2N7000 (~5 pF, Crss [DATASHEET]) | +9 → 0 V | **−2.9 V** (−1.3 to −2.1 V on cell A's bigger node) | −191 mV |
| 2N7000, negative hold | +9 → -9 V | −5.9 V | −382 mV |
| ALD1106 (~1 pF) | +9 → 0 V | −0.8 V | −39 mV |
| JFET (~1.5 pF) | +3 → -9 V | −1.5 V | −78 mV |
| reed relay (~1 pF coil-to-contact) | coil driver end 0 → +5 V at release (the other end stays at +5 V, so the coil's mean potential rises 2.5 V) | ≈ **+0.2 V (upward)** | ≈ +11 mV (upward) |

**A second step, ~5 ms later: the WBL park.** When WBL parks from 3.3 V to 0 V, it couples into the node through the off switch's drain-source capacitance: ΔV ≈ −3.3 V × C_ds / (C_SN + C_ds). It is separate from the gate kick and happens when WBL parks [ESTIMATE, `bench_calcs.py` E2.6b]:

| Write switch | WBL-park step, trimmed node |
|---|---|
| 2N7000 (C_ds ~6-20 pF, from Coss 11 pF typ / 25 pF max [DATASHEET]) | −80 to −260 mV |
| ALD1106, JFET, reed relay (C_ds ≤ ~1 pF [ESTIMATE]) | 0 to −15 mV |

The firmware measures the two steps separately (step 9).

**The lesson.** A −2.9 V kick takes a stored 3.3 V down to ~0.4 V, below the read transistor's threshold, so the '1' now reads as '0'. A lower stored level would be pushed below 0 V, where the switch's body diode clamps it and charge is lost. That is why the trimmed node is used with the MOSFET switches.

**On real chips.** The dossier requires a window of at least 600 mV after WWL kickback before it allows 2 bits per cell ([hot-side-memory](../dossiers/hot-side-memory.md), section 2). You will see why.

### 2.5 Reading the node: the source follower

**The equation.** Vout ≈ V_SN − Vth − √(I/K). For a 2N7000, Vth ≈ 2.1 V typical (0.8-3.0 V) [DATASHEET], and K ≈ 0.1 A/V² [ESTIMATE].

| V_SN | Expected Vout |
|---|---|
| 2.3 V | 0.19 V |
| 2.6 V | 0.49 V |
| 2.9 V | 0.79 V |
| 3.2 V | 1.09 V |

**The usable window.** A stored "1" written at 3.3 V gives ~1.1-1.2 V at the ADC. A node below Vth reads as ~0 V. The `transfer` calibration measures your exact curve.

### 2.6 Two bits per cell (stretch)

**The levels.** The firmware writes four levels with a write-verify loop (like flash memory), at follower outputs of 0.15, 0.45, 0.75 and 1.05 V. That gives a 0.30 V spacing and a 150 mV half-spacing. One bit per cell has a ~550 mV half-spacing: a '1' at Vout ≈ 1.1 V fails when it falls to the 0.55 V threshold. So the **1-bit hold time is t(−550 mV)**, which `analyze_t1.py decay ... --drop-mv 550` reports. Compare the 2-bit result with that, not with t(−100 mV).

| | Half-spacing | Time to lose it at 1 pA, trimmed node |
|---|---|---|
| 1 bit/cell | 550 mV | 127 s |
| 2 bits/cell | 150 mV | 35 s (**~3.7x shorter**) |

**What fails first.** The Pico's averaged read noise (~2 mV) is 75-275 standard deviations below these margins. On the bench, 2-bit storage fails by **drift (leakage), not noise**.

**The same trade in the study.** The dossier's 2-bit case refreshes every 0.64 s, against 3.6 s for 1 bit at 105 °C, about 5.6x [MODEL].

### 2.7 From your bench to the chip: one law, a million-fold scale

**The comparison.** The published oxide cell droops at

0.15 fF × 100 mV / 200 s = 75 zA → **0.50 mV/s** (at 95 °C)

Expected droop rates on your trimmed node:
- reed relay: 1.4-14 mV/s;
- JFET: 0.9-43 mV/s;
- ALD1106: 0.02-1.7 V/s;
- 2N7000: 0.04-43 V/s.

**The striking point.** Your best cell may droop about as slowly as the oxide cell, but with ~1.5 million times more capacitance (230 pF vs 0.15 fF). So the oxide switch leaks ~1.5 million times less than your best switch.

**Leakage a 0.15 fF chip node may have** (100 mV loss):

| Target retention | Maximum leakage |
|---|---|
| 64 ms (today's DRAM refresh window) | 234 aA |
| 1 s | 15 aA |
| 3.6 s (the dossier's 1-bit refresh at 105 °C) | 4.2 aA |
| 100 s | 150 zA |
| 1 h | 4.2 zA |

The study's 1-bit kill line allows ~22.5 aA for the 1e-4 tail cell at 1 s ([dossier](../dossiers/hot-side-memory.md)). That is more than the table's 15 aA because the dossier allows 150 mV of droop for 1 bit (0.15 fF × 0.15 V / 1 s), not the 100 mV used in this table.

### 2.8 Why a wide bandgap: the first-principles reason

**The physics.** Thermal generation of carriers scales as exp(−Eg/2kT). Going from silicon (Eg ≈ 1.12 eV) to IGZO (Eg ≈ 3.1-3.2 eV) multiplies it by exp(−(3.15 − 1.12)/(2kT)):

| Temperature | Suppression factor |
|---|---|
| 25 °C | 7e-18 |
| 95 °C | 1.3e-14 |
| 125 °C | 1.4e-13 |

**The caveat.** Real oxide leakage is set by defects, contacts and tunnelling, not by this intrinsic floor. That is why the study cares about tails, not medians. A Semiconductor Energy Laboratory patent reports, at 150 °C:
- a silicon FET (field-effect transistor) off-current of ~2.2e-6 A;
- a CAAC-IGZO FET off-current of ~3.9e-20 A [REPORTED, patent text].

---

## 3. Honest scope

| What E2 proves | What E2 does NOT prove |
|---|---|
| The gain-cell principle: storage on a gate, a non-destructive read, many reads per write | Anything about oxide (IGZO, IGO, ZTO) transistors: none are used here |
| Retention is set by the write switch's off-leakage (expected spread up to ~10,000x or more across the four switches) | The 1e-4 to 2e-5 leakage tail of 0.01 µm² oxide transistors (the study's biggest unknown) |
| You can measure sub-picoamp currents with a $5 board, using C·dV/dt: the floating-node method oxide labs use | RTN of nanometre devices (your transistors are ~1e6x larger in area; single-trap noise scales as 1/area) |
| Kickback and read coupling are real and scale as C_k/C_SN | Behaviour at 105-125 °C, after a 400 °C bond, or at 0.15 fF |
| 2 bits per cell trades margin for retention (~3.7x here) | Density, energy per bit or cost of the hot-side concept |

**How it scales up.**

| Step | Where | What it adds | Rough cost or source |
|---|---|---|---|
| 1. This bench | Home | Method, intuition, your own analysis code | $25-45 |
| 2. Same floating-node test on real IGZO thin-film transistors | University nanofab, external-user access (the study names Purdue Birck, with Georgia Tech IEN second) | First oxide numbers: sputtered IGZO, µm-size devices, a probe station and a source-measure unit | Hourly user fees [UNVERIFIED]. Send the "Oxide Tail Spec" first (the study's Monday action) |
| 3. Arrays of ≥1e5 small cells, measured at 85-125 °C | Shared "Oxide Tail Statistics" wafer lot | The 1e-4 tail: the decisive number | ~$210-280k in the judges' budgets ([decision.json](../research/stage3/decision.json)) |
| 4. Gate A+ coupons after a real 350-400 °C bond | Partner fab or national-lab user facility | The BEST BET's go/no-go | ~$240k standalone ([report](../DRAM_MOONSHOT_REPORT.md)) |

---

## 4. Safety

> **SAFETY: E2**
> - **Voltages.**
>   - USB 5 V, the Pico's 3.3 V, and two 9 V batteries:
>     - one makes +9 V (its minus terminal to circuit ground);
>     - one makes −9 V (its **plus** terminal to circuit ground).
>   - The biggest difference anywhere is 18 V. No mains-powered builds.
>   - Connect each battery's ground terminal first, and remove it last.
>   - Label the two clips "+9" and "−9". On the −9 V battery's snap clip, the **RED** wire goes to circuit ground and the **BLACK** wire is the −9 V rail. Check with the multimeter (black probe on ground): the −9 V rail must read about −9 V before you connect anything.
>   - V_ON stays at or below +10 V: the ALD1106 is rated 10.6 V, and a fresh 9 V battery reads ~9.5 V. Never use a 12 V adapter for V_ON.
> - **Protect your computer.** The 9 V batteries share ground with your computer's USB port, and the relay coil brings USB 5 V (VBUS) onto the breadboard. One misplaced jumper can push 9-18 V back into the computer, which can damage the port or crash it and lose open work. Connect the Pico through a powered USB hub you can afford to lose, or a USB isolator (ADuM3160-type; full speed is enough for the Pico; about $15-30 [ESTIMATE]). Keep VBUS on its own labelled rail, away from the 9 V rails. Check every rail with the multimeter before plugging in USB. Save open work first.
> - **Children and pets.** Keep them away from the bench while the iron is hot and while a long run is going. Store small parts (SOT-23 parts are tiny), silica-gel packets, 9 V batteries and IPA out of their reach: small parts and gel packets are choking hazards.
> - **9 V batteries.** Never let the terminals touch metal or each other: a shorted 9 V battery gets hot and can start a fire. Store each one capped.
> - **Reed relay.** The contacts sit in a thin glass tube. Bend the leads only with pliers held between the glass and the bend, never at the glass. Broken glass cuts.
> - **Relay coil.** Always fit the 1N4148 flyback diode across the coil. Without it, the coil's turn-off spike can destroy the driver transistor.
> - **Soldering and IPA cleaning.** Same rules as [E1](E1_bit_on_the_bench.md) section 4:
>   - iron ~350 °C, with a stand and ventilation;
>   - IPA SDS hazards (GHS): H225 highly flammable liquid and vapour; H319 causes serious eye irritation; H336 may cause drowsiness or dizziness [REPORTED, supplier SDS]. Use 99% IPA in small amounts, away from the iron, with nitrile gloves and safety glasses. Store it capped. Never pour it down a drain. Never put a damp board into a bag, the fridge or the warm box.
> - **Temperature runs.** Same limits as E1: ≤55 °C, never unattended. Warm runs use only the E1 section 6.5 heater (series resistors, 72 °C fuse, gate pull-down) controlled by `e2_gain_cell.py` with `HEATER_SETPOINT_C` set. Never power the heater unless this script is running its thermostat. To stop, unplug the 12 V adapter first, then press Thonny's Stop: Ctrl-C in an `mpremote` terminal does not stop the Pico. The hair dryer is for short demos only (≤15 min, attended).
> - **ESD.** MOSFETs and JFETs without gate protection die from static. Touch grounded metal first; this protects the parts.

---

## 5. Parts and tools

Shared core kit: [E1](E1_bit_on_the_bench.md) section 5.1 (Pico, breadboards, multimeter, DS18B20).

| Part | Spec that matters | Example part number | Approx. USD | Where to buy |
|---|---|---|---|---|
| Read transistors ×3, plus spares, plus write switch A, plus relay driver | VGS(th) 0.8 / 2.1 / 3.0 V; Ciss 20 pF typ; Coss 11 / 25 pF; Crss 4 / 5 pF [DATASHEET]. Pick parts with Vth ≤ 2.2 V. Pin order differs between makers (onsemi TO-92: source-gate-drain): check your datasheet | 2N7000 (TO-92) ×10 | 0.1-0.3 each [ESTIMATE] | DigiKey, Mouser, any shop |
| Write switch B (low-leakage MOSFET) | IDS(OFF) 10 pA typ / 400 pA max at 12 V; IGSS 0.1 pA typ [DATASHEET]; 10.6 V rating [REPORTED] | ALD1106PBL (one of its 4 transistors; share with E1) | 3-8 [REPORTED $2.90 at a broker] | DigiKey, Mouser |
| Write switch C (low-leakage JFET) | MMBF4117 is the non-A grade: IGSS ≤ 10 pA at -20 V (the ≤1 pA grade is 2N4117A/PN4117A); VGS(off) -0.6 to -1.8 V; IDSS ~30-90 µA [REPORTED] | MMBF4117 (SOT-23, in stock at DigiKey [REPORTED]) on a SOT-23-to-DIP adapter. Bend the adapter pin for the SN side up and air-wire it, then scrub the adapter with IPA: FR-4 and flux next to the node can leak more than the JFET. Or PN4117A if you find stock (through-hole, largely obsolete [REPORTED]) | 0.5-4 [ESTIMATE; one listing shows $3.63 for PN4117A, 0 in stock] | DigiKey, Mouser, Rochester |
| SOT-23 adapter board | 0.1" pins | any | 1-2 [ESTIMATE] | |
| Write switch C' (reed relay) | Insulation resistance 1e12 Ω min / 1e13 Ω typ [DATASHEET]; 5 V coil (~350 Ω [REPORTED]). The suffix selects options such as an internal coil diode and a coaxial shield [REPORTED] | Coto 9002-05-xx (9000 series, SIP): pick the suffix from the datasheet's part-number key. If it has the internal diode, connect coil + to VBUS as marked (wired backwards, the diode shorts VBUS through the driver). If it has a shield pin, tie the shield to WBL | 5-15 [UNVERIFIED] | DigiKey, Mouser, Newark |
| Optocouplers ×3 | Phototransistor output; collector-emitter rating ≥ 20 V (18 V across it here) | PC817 (VCEO 35 V [UNVERIFIED]) | 0.3 each [ESTIMATE] | |
| Trim capacitors ×4, plus spares from another batch | C0G, 5%, 220 pF (only ≥100 GΩ guaranteed [DATASHEET]; see section 2.2). Alternative: polystyrene or polypropylene film | any C0G radial | 0.2 each [ESTIMATE] | |
| Follower resistors | 47 kΩ ×3 | | — | |
| WWL pull-ups | 100 kΩ ×2 (MOSFET cells), 1 MΩ ×1 (JFET cell) | | — | |
| LED resistors | 330 Ω ×3 | | — | |
| PWM DAC filter | 10 kΩ + 1 µF film (polyester is fine here) | | — | |
| Relay driver | A 2N7000 that measured V_GS ≤ 2.2 V in step 1 (a part near the 3.0 V maximum may not sink the ~14 mA coil current from a 3.3 V GPIO), or a 2N3904 NPN with a 1 kΩ base resistor; plus 100 Ω gate resistor, 100 kΩ pull-down, 1N4148 | | 0.5 [ESTIMATE] | |
| Batteries | 9 V ×2 with snap clips (label them "+9" and "−9") | | 6-10 | |
| Cleaning | IPA 99%, brush, silica gel | | 8 [ESTIMATE] | |
| *Recommended* USB protection | Powered USB hub, or a USB isolator (ADuM3160-type, full speed) | | 15-30 [ESTIMATE] | |

**Tools.**
- Soldering iron, multimeter, flush cutters, pliers, safety glasses.
- Optional: an oscilloscope, to watch the kickback when a switch turns off.

---

## 6. Circuit

### 6.1 One cell (three are built side by side: A, B, C)

```
                         WWL_x (from its driver, 6.2)
                              |
   WBL (shared) ------[ write switch x ]------ SN_x  (air-wired: switch lead + gate lead + C_trim, nothing else)
                                                 |
                                      +----------+-----------+
                                      |                      |
                              [C_trim 220 pF C0G]     gate of Q_Rx (2N7000 read transistor)
                                      |                      drain  -> GP9  (READ_EN, 3.3 V while reading)
                                     GND                     source -> 47k -> GND
                                                             source -> ADC  (A: GP26, B: GP27, C: GP28)

   WBL: GP15 (PWM, 100 kHz) --[10k]--+-- WBL;  1 uF from WBL to GND   (a 0-3.3 V DAC, tau = 10 ms)
   DS18B20 -> GP22 (4.7k pull-up), taped beside the storage nodes
```

**Switch orientation and bodies.**
- **Switch A (2N7000).** Source to WBL, drain to SN. The built-in body diode then points from WBL to SN, and stays reverse-biased while WBL is parked at 0 V. Pin order differs between makers (onsemi's TO-92 is source-gate-drain): check your datasheet, because swapping source and drain flips the body diode.
- **Soldering the SOT-23 JFET.** Flux the adapter pads and tin one pad. Hold the part with tweezers and reflow that pad. Solder the other two pins, then reflow the first. Use a fine tip and a magnifier. A makerspace can help with your first surface-mount part.
- **Switch B (ALD1106).** Substrate (V−) pin to GND.
- **Switch C (JFET).** Symmetric; either end to SN.
- **Pin numbers.** Take them from each datasheet's pin diagram; they are not reproduced here.

### 6.2 Write-wordline drivers (one optocoupler per cell)

```
   V_ON ---[R_up]---+--- WWL_x  -> gate of write switch x
                    |
              opto collector
              opto emitter ---- V_OFF
   GPx --[330 Ohm]--> opto LED anode;  LED cathode -> GND

   LED on  (GPIO high) -> WWL pulled to V_OFF -> switch OFF  (HOLD)
   LED off (GPIO low)  -> WWL pulled to V_ON  -> switch ON   (WRITE)

   cell A, 2N7000 : V_ON = +9 V,  R_up = 100k, V_OFF = GND   (or -9 V for the "negative hold" run)
   cell B, ALD1106: V_ON = +9 V,  R_up = 100k, V_OFF = GND only (stay inside its 10.6 V rating)
   cell C, JFET   : V_ON = +3.3 V, R_up = 1 M, V_OFF = -9 V   (a JFET is ON at 0 V and needs a negative gate to turn off)
   GPIO: cell A -> GP10, cell B -> GP11, cell C -> GP12
```

**Reed relay (cell C', replacing the JFET in run 2):**
- **Connections.** GP13 → 100 Ω → gate of a low-Vth 2N7000 driver (V_GS ≤ 2.2 V in step 1), with 100 kΩ from that gate to GND. Or a 2N3904 NPN: GP13 → 1 kΩ → base, emitter to GND. Coil from USB 5 V (VBUS) to the driver's drain (or collector). A 1N4148 across the coil, cathode to 5 V. If the relay has an internal diode, coil + goes to VBUS as marked. Contacts between WBL and SN_C; a shield pin, if present, to WBL.
- **Why the idle coil matters.** With the driver off, both coil ends sit at +5 V. The coil-to-contact insulation (~1e12-1e13 Ω [ESTIMATE, same order as the contact insulation]) then drives ~0.2-1.7 pA INTO a 3.3 V node: the same size as, and opposite in sign to, the contact leakage you want to measure. Step 8 measures it.
- **Firmware.** Set `CELL_C_IS_RELAY = True`.

### 6.3 Low-leakage build rules (same as E1, and they matter more here)

**Why they matter more.** At 230 pF, a 1 pA leak moves the node 4.3 mV/s. A fingerprint can leak 100 pA.

1. **Air-wire each storage node.**
   - Bend the read transistor's gate lead up and solder it in the air to the switch's SN-side lead and one leg of C_trim.
   - The other leg of C_trim goes to the ground rail.
   - Nothing on the node touches the breadboard.
2. **Clean.** Scrub with 99% IPA, rinse with fresh IPA (scrubbing alone spreads dissolved flux), blot with a lint-free wipe, and let it dry at least 1 hour (overnight is better). Never touch the node again.
3. **Use C0G only for C_trim.** Not X7R: it leaks and creeps (dielectric absorption).
4. **Keep it dry.** Use a box with silica gel on humid days, and log the humidity.

---

## 7. Procedure

1. **Pick read transistors.**
   - For each 2N7000: tie gate to drain, feed 1 kΩ from 3.3 V into the drain, and ground the source.
   - Measure V_GS. That is Vth at ~1 mA.
   - Keep three with V_GS ≤ 2.2 V that lie within ±50 mV of each other.
2. **Build the read side.** For each of the three cells, build the read transistor, its 47 kΩ resistor, the ADC connection and C_trim, and air-wire the nodes. Add the PWM DAC and the DS18B20. Copy `t1_common.py` and `e2_gain_cell.py` to the Pico.
3. **Measure the floor, before any switch.**
   - Touch each storage node briefly to 3.3 V with a jumper, then pull the jumper away.
   - Run `MODE = "retention"`, `DURATION_S = 1800` (its "write" does nothing yet). Capture with `mpremote run e2_gain_cell.py > e2_floor.csv` (use a new name each run), set `LOGFILE` as a backup, and turn off computer sleep. The same applies to every run below.
   - Analyze with `python3 analyze_t1.py decay e2_floor.csv --c-pf 230 --col v_out`.
   - This is the leakage of read gate + C_trim + board. Target: **< 1 pA**. Up to 33 pA would still be within the C0G datasheet guarantee (section 2.2): if you are far above 1 pA after cleaning, swap C_trim or the read transistor (section 11).
4. **Install switches A (2N7000), B (ALD1106) and C (JFET) and their drivers.**
   - Check the rails first: +9 V rail ≈ +9 V, −9 V rail ≈ −9 V (black probe on ground), VBUS ≈ 5 V on its own rail.
   - Check with the multimeter: GPIO high → WWL at V_OFF; GPIO low → WWL at V_ON.
5. **Calibrate.**
   - Run `MODE = "transfer"`. It turns all switches on and sweeps WBL from 0 to 3.3 V.
   - Run `python3 analyze_t1.py transfer e2_transfer.csv`. It prints each cell's Vth and follower gain.
   - Use them to convert Vout into storage-node voltage.
6. **Fast run, for the leaky switch.**
   - Run `MODE = "fast"`. It samples a few ms with the switches on, 3 ms after switch-off with WBL still at the write level, then parks WBL with no settling delay and samples the decay for 2 s, fastest first (t = 0 at the park).
   - Cell A (2N7000) may lose 100 mV in milliseconds to seconds.
   - WBL falls with the 10 ms time constant of the PWM filter, so the first ~30 ms show the leak building up as the voltage across the switch grows. For millisecond cells, drive WBL from a plain GPIO for this run: wire GP14 → 100 Ω → WBL, remove the 10 kΩ / 1 µF filter, and set `WBL_GPIO = 14`.
   - Analyze with `decay e2_fast.csv --c-pf 250 --col v_out` for cell A (`--c-pf 230` for B and C). The analyzer warns if a cell decays faster than you sample, or if it was already empty at the first sample.
7. **Retention run.**
   - Run `MODE = "retention"`, `LOG_S = 1`, `DURATION_S = 1800`.
   - Expect cell C (JFET) to hold for minutes and cell B (ALD1106) for seconds.
   - Run `python3 analyze_t1.py decay e2_ret.csv --c-pf 230 --col v_out --drop-mv 550`. Record the leakage of each cell and the time to lose 100 mV and 200 mV. The extra t(−550 mV) is the **1-bit hold time** (Vout falling to the 0.55 V threshold), used in step 13. With 1800 s the run measures it for leakage ≥ 0.07 pA (230 pF × 0.55 V ÷ 1800 s) [ESTIMATE]; slower cells print `nan`.
8. **Swap in the reed relay.**
   - Replace switch C with the reed relay and set `CELL_C_IS_RELAY = True`.
   - Repeat step 7. Wait ~1 s after the relay opens before trusting the curve.
   - **Check the coil path.** Write 3.3 V, then set `PARK_V = 3.3` (zero volts across the contacts) and log for 10 min. Ignore cell A in this run: its body diode recharges it. Any drift of cell C' is coil leakage plus the floor; subtract it from the normal run.
9. **Kickback.**
   - Every `retention` run now logs three rows per cell at the write: `kick_before` (switch on), `kick_after` (2 ms after switch-off, WBL still at the write level) and `kick_park` (after WBL has parked). The `fast` run logs the first two at full speed.
   - Run `python3 analyze_t1.py kick e2_ret.csv`. The gate kick (after − before) compares with the first table in section 2.4; the WBL park step (park − after) compares with the second.
10. **Read many times.**
    - Run `MODE = "readmany"`. It toggles READ_EN 10,000 times and logs every 500th read.
    - Compare the drift with an idle hold of the same length (step 7).
11. **Negative hold (cell A only).**
    - Move cell A's V_OFF from GND to the −9 V rail and repeat steps 6-7.
    - Subthreshold leakage should drop, but kickback doubles (~0.38 V on the trimmed node). Gate-induced drain leakage (GIDL) may rise.
    - This is a miniature of the study's "−0.5 vs −0.7 V hold" split.
12. **Temperature.**
    - Repeat step 7 cold (~4 °C, bagged with silica gel, following E1's cold-run rules) and warm (45 °C).
    - Warm: build E1 section 6.5 and do its first test, then set `HEATER_SETPOINT_C = 45.0`. The script preheats, holds 45 °C for 30 min, then writes and logs. It prints `# preheat` lines meanwhile. Stay nearby. Never power the heater unless this script is running its thermostat.
    - Analyze with `python3 analyze_t1.py temp --decay --c-pf 230 --col v_out e2_cold.csv e2_room.csv e2_warm.csv`. It fits ln(I_leak) against 1/kT for each cell and prints Ea. By hand: Ea = ln(I_warm/I_cold) / (1/kT_cold − 1/kT_warm), with k = 8.617e-5 eV/K and T in kelvin. (`temp` without `--decay` is for E1 retention maps only.)
13. **Two bits per cell (stretch).**
    - On the best cell, run `MODE = "mlc"` (5 trials × 4 levels, 300 s hold each).
    - Run `python3 analyze_t1.py mlc e2_mlc.csv` and note when the first level errors appear.
    - Compare the first 2-bit error time with the 1-bit hold t(−550 mV) from step 7, not with t(−100 mV). Expect ~3.7x shorter (ratio ~0.27).
14. **The truly capacitorless node (optional).**
    - Remove C_trim from the reed-relay cell only and repeat step 8.
    - Expect ~20x shorter retention (230 pF → ~10 pF) and a kick of about +0.2 V (upward) at relay release.

---

## 8. Data sheet / log template

**Run header:**

| Date/time | Mode | Cell A switch | Cell B switch | Cell C switch | V_ON / V_OFF per cell | C_trim | WBL park V | Temp °C | Humidity % | File | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

**Results per cell:**

| Cell | Switch | Vth of read transistor (V) | Gate kick (mV), measured / predicted | WBL park step (mV), measured / predicted | Leakage (pA) | t(−100 mV) s | t(−200 mV) s | t(−550 mV) s (1-bit hold) | Droop rate (mV/s) |
|---|---|---|---|---|---|---|---|---|---|
| floor | none | | — | — | | | | | |
| A | 2N7000 | | / −191 | / −80 to −260 | | | | | |
| A | 2N7000, −9 V hold | | / −382 | / −80 to −260 | | | | | |
| B | ALD1106 | | / −39 | / 0 to −15 | | | | | |
| C | JFET | | / −78 | / 0 to −15 | | | | | |
| C' | reed relay | | / +11 | / 0 to −15 | | | | | |

**CSV columns written by the Pico:**
- **Retention and fast modes:** `exp, mode, t_s, temp_c, label, cell, v_out` (mode is `retention`, or `kick_before` / `kick_after` / `kick_park` for the write rows)
- **Transfer:** `exp, mode, label, v_wbl, cell, v_out`
- **2-bit (mlc):** `exp, mode, label, t_s, trial, level, target_v, v_out`

---

## 9. Pass / fail criteria

| # | Test | Pass |
|---|---|---|
| 1 | Floor | Read gate + C_trim + board < 1 pA (if higher, clean and dry before judging the switches) |
| 2 | Non-destructive read | 10,000 reads add ≤ 10% (or ≤ 5 mV, whichever is larger) to the drift of an idle hold of the same length |
| 3 | Switch decides retention | t(−100 mV) of the JFET and reed cells > both MOSFET cells, and best ÷ worst ≥ 10x. Less than 10x means either the floor dominates (check whether the best cell's leakage equals the step-3 floor) or your 2N7000 is unusually quiet (section 10). Either is a result |
| 4 | Floating-node method works | Best cell's extracted leakage ≤ 1 pA, with R² ≥ 0.95 on the decay fit |
| 5 | Kickback | Measured gate kicks within ±50% of the first table in section 2.4, and the 2N7000's WBL park step inside its −80 to −260 mV range (`analyze_t1.py kick`) |
| 6 | 2 bits per cell (stretch) | All 4 levels placed within ±15 mV after write-verify; first 2-bit error time ÷ 1-bit hold t(−550 mV) = 0.27 ± 0.15 |

---

## 10. What would surprise you (and why it would matter)

- **The 2N7000 holds as well as the JFET.** Its real off-leakage at 3 V is far below the datasheet maximum, and your floor dominates. Then measure each switch alone with a bigger C_trim (1 nF).
- **The negative hold makes retention worse.** That is GIDL, a real DRAM and oxide-cell trade-off: deeper "off" bias opens a tunnelling leak at the drain edge. Finding the best hold voltage is a real design question in the dossier.
- **Retention depends strongly on where WBL is parked.** The leak is driven by the voltage across the switch (subthreshold), not by junction area. Setting `PARK_V` near the stored level cuts the voltage across a JFET or reed switch to almost zero. **Never do this with the 2N7000 cell:** its body diode would recharge the node.
- **Vout jumps up or down in discrete steps during a hold.** That could be RTN-like trapping, a mechanical or contact event, or ESD. RTN is the study's second biggest unknown. Discrete transistors are huge, so true RTN should be tiny. Log the step size and how often steps occur.
- **The node creeps back up for a few seconds after a write.** That is dielectric absorption in C_trim (or in a switch package), not leakage. It is a known capacitor effect, and real oxide cells have their own fast relaxation ("drift").
- **Leakage barely changes between 4 °C and 45 °C for the best cells.** You are measuring surface or insulation leakage, not semiconductor physics.

---

## 11. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Vout stays at 0 V | The read transistor's Vth is above the stored level, READ_EN is low, or the switch never opens | Pick a lower-Vth 2N7000; check GP9; run `transfer` |
| `transfer` shows no response for one cell | WWL never reaches V_ON: LED backwards, missing pull-up, or JFET gate rail wrong | Measure WWL with the GPIO low and high |
| Every cell, even the reed, decays at the same rate | The floor dominates: flux, fingers, humidity, X7R C_trim | Section 6.3; re-run step 3 |
| Floor stays > 1 pA after cleaning and drying | A C0G C_trim near its 100 GΩ guarantee, or the read 2N7000's own gate leakage (onsemi guarantees only IGSS ≤ 10 nA at 15 V; typical parts are far lower) | Swap C_trim (another batch, or polystyrene/polypropylene), or swap the read transistor; or use a spare ALD1106 section (IGSS 0.1 pA typ [DATASHEET]) as the read device, then re-run `transfer` |
| A cell reads a flat line near 0 V from the first sample | It lost its charge before the first sample: the leakiest cell, not the best | `analyze_t1.py decay` flags it; re-run with `fast` mode |
| The node jumps negative when a switch opens and the data is lost | Kickback on the pure node | Use the trimmed node (220 pF) for MOSFET switches |
| Cell A loses everything instantly, even trimmed | 2N7000 orientation reversed (body diode forward), or WBL not parked at 0 V | Source to WBL, drain to SN; `PARK_V = 0.0` |
| Big glitch when the relay switches | Coil-to-contact coupling (upward at release) and contact bounce | Wait 1 s after release before trusting the curve; keep the flyback diode |
| The relay never clicks | Driver 2N7000 Vth too high for a 3.3 V gate, or an internal-diode relay wired backwards | Use a low-Vth 2N7000 or a 2N3904 with 1 kΩ; check the coil polarity marking |
| Noisy Vout | ADC noise, or 3.3 V rail ripple | GP23 high (low-ripple mode), more averaging, short ADC wires |
| JFET switch never turns off | The gate is not negative enough (VGS(off) up to −1.8 V) | Check the −9 V rail and the opto; the gate must sit below the node by more than 2 V |

---

## 12. Sources

Evidence tags:
- [DATASHEET] = manufacturer data;
- [REPORTED] = paper, patent, press, distributor or search snippet;
- [ESTIMATE] = `bench_calcs.py`;
- [MODEL] = study model;
- [UNVERIFIED] = not confirmed.

Read through search snippets on 2026-11-03; some hosts were blocked. Prices are approximate as of November 2026.

1. imec 2T0C IGZO cell, >200 s retention at 95 °C [REPORTED, via the study's dossier]: https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234, and [`dossiers/hot-side-memory.md`](../dossiers/hot-side-memory.md) section 2 (75 zA, 0.15 fF, 600 mV window, 22.5 aA tail ceiling, 3.6 s / 0.64 s refresh) [MODEL]
2. Semiconductor Energy Laboratory patents and paper on the floating-node method: device under test plus write transistor plus source-follower read; retention = time for a 0.2 V drop; Arrhenius extrapolation from 85-150 °C to ~2 zA/µm; Si FET ~2.2e-6 A vs CAAC-IGZO ~3.9e-20 A at 150 °C [REPORTED, patent text via search snippets; which statement comes from which patent was not confirmed]: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9196741, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9484467, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12082391
3. CAAC-IGZO embedded DRAM: ≤200 zA per FET at 85 °C needed for ~1 h refresh, using a −7 V back gate [REPORTED]: https://dc.engconfintl.org/ulsic_tft_vii/34
4. ALD1106 leakage and gate current [DATASHEET, via snippet]: https://www.electronicsdatasheets.com/download/120482.pdf?format=pdf; price $2.90 at quantity 1 (broker) [REPORTED]: https://www.smbom.com/product/ald1106pbl-16467559
5. 2N7000 VGS(th), Ciss 20 / 50 pF, Coss 11 / 25 pF, Crss 4 / 5 pF (typ / max at VDS 25 V), IDSS, IGSS [DATASHEET, via snippet]: https://www.onsemi.com/download/data-sheet/pdf/2n7000-d.pdf
6. 2N4117A-series JFET: IGSS < 1 pA (A) / 10 pA, VGS(off) −0.6 to −1.8 V [REPORTED]: https://linearsystems.com/_files/ugd/7e8069_12949627a6794d63a612d89b494fc997.pdf
7. PN4117A availability: obsolete at DigiKey; InterFET listing $3.63 with 0 in stock; MMBF4117 SOT-23 in stock [REPORTED]: https://www.digikey.my/en/products/detail/onsemi/PN4117A/1049077, https://findchips.com/search/PN4117%2FD28Z, https://www.digikey.sg/en/products/detail/onsemi/MMBF4117/1049290
8. Coto 9000 series reed relays: insulation resistance 1e12 Ω min, 1e13 Ω typical; 5 V coil types; part-number suffix selects options such as an internal diode and a coaxial shield; insulation resistance needs controlled handling [DATASHEET / REPORTED]: https://cototechnology.com/library/cotoclassic-9000-series-reed-relay-datasheet.pdf and https://canada.newark.com/coto-technology/9002-05-01/relay-reed-spst-no-200v-0-5a-tht/dp/62K1752
9. KEMET C0G insulation resistance [DATASHEET]: https://mfgdatasheets.nlight.net/Kemet%20C0G.pdf
10. RP2040 ADC ENOB 8.7 and Pico pitfalls: see [E1](E1_bit_on_the_bench.md) sources 10-14.
11. Study context (BEST BET, biggest unknown, Oxide Tail Spec, budgets) [MODEL]: [`DRAM_MOONSHOT_REPORT.md`](../DRAM_MOONSHOT_REPORT.md) section 1; [`research/stage3/decision.json`](../research/stage3/decision.json)
12. All [ESTIMATE] numbers: [`code/T1_pico/bench_calcs.py`](code/T1_pico/bench_calcs.py) `--section e2`.
13. Isopropanol SDS hazard statements H225, H319, H336 [REPORTED, supplier SDS]: https://www.vanderbilt.edu/vinse/facilities/safety_data_sheets/Isopropanol.pdf
14. Heater circuit, watchdog and stopping rules: [E1](E1_bit_on_the_bench.md) section 6.5 and sources 18 and 21.
15. [UNVERIFIED]: switch coupling capacitances C_k other than the 2N7000's Crss; 2N7000 C_ds at 3 V and low-voltage off-leakage; reed coil-to-contact insulation; PC817 VCEO; reed relay price and the exact suffix options; pin numbers; USB isolator price; university user fees.
