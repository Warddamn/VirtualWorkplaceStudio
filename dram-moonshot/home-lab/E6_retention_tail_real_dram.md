# E6: Map the retention tail of a real DRAM chip on your desk

*Track T3 of the home-lab guides. As of 2026-11-03. Prices are approximate as of Nov 2026.*

This is the study's **FASTEST PROOF** ([raw-ber-contract](../dossiers/raw-ber-contract.md)) shrunk to a desk. You map how long every cell of a real memory chip holds its data. Then you compute how much less often it would need refreshing if an error-correcting code caught the few weak cells. It is mostly code, so it suits a software builder.

**In one paragraph.** DRAM (dynamic random-access memory) stores each bit as charge on a tiny capacitor that leaks. Every cell is rewritten ("refreshed") every 64 ms, because a rare few leak fast. Most cells hold their data for seconds or minutes. You will take refresh away from a 64-megabit chip for 64 ms to 65 s, at 25, 45 and 65 °C, and log the address of every bit that flips. That gives the chip's **retention tail**. A script then puts the measured failures into error-correcting codewords and finds the longest refresh interval that keeps uncorrectable errors under a target. That is your chip's **refresh relaxation factor**, the number the dossier puts at ~9x for DDR5 server memory.

**Files for this experiment**

| File | What it is |
|---|---|
| [code/T3_dram/retention_map.py](code/T3_dram/retention_map.py) | Expected results (`predict`), analysis (`analyze`), `--selftest`. Python + numpy only |
| [code/T3_dram/capture_retention.py](code/T3_dram/capture_retention.py) | Drives the board over USB serial, logs everything; `--simulate` and `--selftest` need no hardware |
| [code/T3_dram/stm32_retention/](code/T3_dram/stm32_retention/) | Reference firmware in C for the STM32F429I-DISC1. **Untested on hardware** |

---

## 0. At a glance

| Item | Value |
|---|---|
| Difficulty | **2 of 5.** Flash a board, run Python, solder 8 header pins (basic) |
| Time | One weekend to build and debug. About 10 h of unattended runs (3 temperatures). 10 minutes to analyse |
| Cost tier | **$$: about $100-170** (board $30-63, thermocouple kit ~$25, heater and thermostat ~$15, rest ~$30) |
| Skills | Install a toolchain, read a register table, run Python scripts |
| What you get | A retention map of 67,108,864 real DRAM cells, its tail quantiles, temperature activation energy, VRT share, error clustering, and an ECC-safe refresh interval |
| Main risk | Heat (65 °C box). Mitigated by a thermostat, an independent thermal fuse and a non-flammable base (Safety box, section 6) |

---

## 1. Why this experiment, and what it connects to

- **The thesis it tests.** The raw-ber-contract dossier claims that error-correcting codes (ECC) can carry the rare weak cells, so refresh can run far less often. It estimates ~9x less refresh energy on DDR5 server modules at 85 °C, and ~13x on retired DDR4 ([decision.json](../research/stage3/decision.json), [dossier](../dossiers/raw-ber-contract.md) section 2.5) [MODEL in the study].
- **The study's own gate.** NO-GO if the chipkill-safe interval is under 4x the standard refresh window at 65 °C. PASS at 24x or more at 65 °C (dossier section 5.R). You will compute the same two numbers for your chip.
- **The biggest unknown, in miniature.** The study's biggest unknown is a **tail statistic**: the 1e-4 to 2e-5 quantile of leakage in tiny oxide transistors. You cannot measure oxide transistors at home. You *can* build and debug the exact method on 67 million silicon cells: quantile estimation, temperature acceleration, telegraph-like switching (VRT), and the error budget. Section 15 spells out the link.

---

## 2. First principles: the laws, and the numbers to expect before you build

All numbers in this section come from `python3 code/T3_dram/retention_map.py predict` (exit 0). They are **[ESTIMATE]** unless tagged otherwise.

### 2.1 A DRAM cell is a leaky capacitor

**Law: charge conservation.** A cell with capacitance C_s stores charge Q = C_s · V. A leakage current I_leak drains it. The cell fails when it has lost enough voltage that the sense amplifier misreads it:

> t_ret = C_s · ΔV_allow / I_leak

**How much may it lose?** At read time the cell shares charge with its bitline (capacitance C_BL). The bitline moves by ΔV_BL = (V_cell − VDD/2) · C_s / (C_s + C_BL). The sense amplifier needs ΔV_BL above its offset V_off. So the cell may droop by

> ΔV_allow = VDD/2 − V_off · (C_s + C_BL) / C_s

**Worked example** (assumed values for an older chip [ESTIMATE]: C_s = 20 fF, C_BL = 100 fF, VDD = 2.0 V, V_off = 30 mV):
- (C_s + C_BL)/C_s = 120/20 = 6, so V_off · 6 = 0.18 V.
- ΔV_allow = 1.00 − 0.18 = 0.82 V.
- Allowed charge loss Q = 20 fF × 0.82 V = 16.4 fC, about 102,000 electrons.

| Retention time | Leakage that empties the cell (I = Q / t) |
|---|---|
| 64 ms | 256 fA |
| 1 s | 16.4 fA |
| 10 s | 1.64 fA |
| 100 s | 0.16 fA = 164 aA |

(1 fA = 1e-15 A; 1 aA = 1e-18 A.) **A 10 s retention time means a ~2 fA leak.** Your chip is a 67-million-channel femtoammeter. The hot-side and AND-STACK cells in this study need attoamp tails; this is the same equation one decade further on.

### 2.2 Temperature: leakage is thermally activated

**Law: Arrhenius.** Leakage grows as exp(−Ea / kT), so retention time scales as t_ret ∝ exp(Ea / kT). Here k = 8.617e-5 eV/K and T is in kelvin. The acceleration between two temperatures is

> AF = t_ret(T_cold) / t_ret(T_hot) = exp[(Ea/k) · (1/T_cold − 1/T_hot)]

Example for Ea = 0.6 eV, 25 → 65 °C: 1/298.15 − 1/338.15 = 3.97e-4 K⁻¹; (0.6 / 8.617e-5) × 3.97e-4 = 2.76; AF = e^2.76 = **15.8x**.

| Ea | Likely mechanism | 25→45 °C | 45→65 °C | 25→65 °C | Retention halves every |
|---|---|---|---|---|---|
| 0.35 eV | trap-assisted leakage, typical of **tail** cells [REPORTED in patents] | 2.35x | 2.13x | 5.0x | ~17 °C |
| 0.6 eV | thermal generation in the junction, ~half the silicon band gap | 4.34x | 3.65x | 15.8x | ~10 °C |
| 1.1 eV | diffusion current, ~the band gap | 14.8x | 10.7x | 158x | ~5.5 °C |

Patents report ~0.35 eV for tail bits and ~0.6-0.7 eV for normal bits [REPORTED, S29]. The study's cell model uses "retention halves every ~10 °C" ([dram_cell_physics.py](../models/dram_cell_physics.py), `RET_HALVING_C`). **Your fitted Ea tells you which mechanism rules your chip's tail.**

### 2.3 The tail, and why a code buys so much

**The retention tail.** Let F(t) be the fraction of cells that fail when refresh is withheld for time t. The study fits a lognormal tail through two published anchors at 85 °C: F(32 ms) = 1.1e-10 and F(64 ms) = 3.6e-9. These derive from RAIDR-era counts of "~30 cells below 128 ms and ~1,000 cells below 256 ms in 32 GB" [REPORTED, S25], moved to 85 °C ([raw-ber-contract.py](../models/raw-ber-contract.py) section 5). That fit has a median of ~82 s at 85 °C and a log-width sigma of 1.24. I apply "halves every 10 °C" to reach your temperatures.

**The code.** A code that corrects t errors per n-bit codeword fails only when more than t cells in one codeword are wrong. For independent errors with per-bit probability p:

> P_UE ≈ (n·p)^(t+1) / (t+1)!

The exponent t+1 is the whole story. Halve p and SEC-DED (t = 1) gets 4x safer; BCH t = 12 gets 8,192x safer. The tail is steep too: F grows roughly as t^3 to t^5 in the region of interest. So a modest code buys a large factor in refresh interval.

**Worked example: SEC-DED (72,64) at 45 °C, target 1** (target 1 = at most 1e-15 uncorrectable events per data bit-hour, with a scrub every hour):
- Per codeword per hour: 1e-15 × 64 bits × 1 h = 6.4e-14.
- C(72,2) · p² ≤ 6.4e-14 → 2,556 · p² ≤ 6.4e-14 → p ≤ 5.0e-9.
- Variable retention time adds new weak cells: multiply by (1 + 1/day × 1 h / 24 h) = 1.042, so the tail fraction allowed is F ≤ 4.8e-9.
- Invert the tail at 45 °C: median = 82 s × 2^4 = 1,310 s, so ln(median) = 7.18. Then z(4.8e-9) = −5.73, and ln t = 7.18 − 5.73 × 1.24 = 0.07, so **t = 1.08 s ≈ 17x the 64 ms window**.

**Target 2** is the study's tighter line: at most 2e-19 failures per 64-byte read (dossier section 2.1).

### 2.4 Expected results for a 64 Mbit SDR chip (67,108,864 cells)

**Expected failing cells** (central estimate, with the band from 0.5x retention (DDR5-like) to 4x (older, larger cells)) [ESTIMATE]:

| Refresh withheld for | 25 °C | 45 °C | 65 °C |
|---|---|---|---|
| 64 ms | 0 | 0 | 0 |
| 0.512 s | 0 | 0 | ~6 [0-103] |
| 1.024 s | 0 | 0 [0-6] | ~103 [0-1,358] |
| 4.096 s | 0 [0-6] | ~103 [0-1,358] | ~13,000 [103-96,000] |
| 16.4 s | ~103 [0-1,358] | ~13,000 [103-96,000] | ~516,000 (F 0.8%) |
| 65.5 s | ~13,000 [103-96,000] | ~516,000 | ~6.5 million (F ~10%) |

- **First failing cell expected:** 25 °C at ~5.5 s [2.8-22 s]; 45 °C at ~1.4 s; 65 °C at ~0.35 s.
- **q = 1e-4 reached** (the Oxide-Tail quantile): 25 °C at ~53 s; 45 °C at ~13 s; 65 °C at ~3.3 s.
- **Temperature sensitivity:** at a fixed wait, the failing fraction grows ~14x per +10 °C in this model. A study of 223 LPDDR4 chips reports ~10x per 10 °C [REPORTED, S27].
- **Cross-check:** a DDR3 survey found fewer than 0.001% of cells below 3 s at 45 °C, even in the worst module [REPORTED, S26]. The model gives 4.4e-7 (0.000044%), consistent.
- **Cold-boot evidence.** Halderman et al. (2008) showed that DRAM keeps its contents for several seconds after power is cut, even at room temperature. Near −50 °C, fewer than 1% of bits decayed after 10 minutes [REPORTED, S22]. That is the long-retention majority, seen from the outside. Do **not** reproduce their cooling (canned-air sprays cause frostbite and the propellant is flammable).

**Expected ECC-safe refresh interval** (independent errors, VRT growth 1/day, scrub 1 h) [ESTIMATE]:

| Code | 25 °C | 45 °C | 65 °C (target 1) | 65 °C, dossier target 2 |
|---|---|---|---|---|
| SEC-DED (72,64), plain server ECC | 4.3 s (68x) | 1.1 s (17x) | 0.27 s (4.2x) | 0.066 s (1.0x) |
| BCH-4 (552,512) | 31 s | 7.6 s | 1.9 s (30x) | 0.88 s (14x) |
| BCH-12 (640,512) | 115 s | 29 s | 7.2 s (113x) | 4.8 s (75x) |
| RS-8 (80,64) byte symbols, the dossier's chipkill code | 73 s | 18 s | 4.6 s (71x) | **2.7 s (42x; band 21-169x)** |

- **Prediction for the gate:** RS-8 at 65 °C, target 2 gives **~42x (21-169x)**. That is above the dossier's 24x PASS line in the central case. The pessimistic end (21x) sits just under it.
- **Consistency check:** the dossier gives 3.3 s for retired DDR4 / RS-8 at 65 °C. This model gives 2.7 s from the same anchor; it counts every cell in its charged state (worst case), where the dossier assumed random data.
- **These numbers assume independent errors.** Clustered errors shorten the interval a lot, above all for SEC-DED. Measuring clustering is one of the main things the experiment adds.
- **Refresh energy scales as 1/interval:** a 42x longer interval cuts array refresh energy 42x. Periphery and self-refresh costs are not modelled.

---

## 3. Honest scope

| This experiment proves | It does NOT prove |
|---|---|
| That a real commodity DRAM chip's retention distribution has a long majority and a thin tail, measured cell by cell | Anything about modern DDR4/DDR5 dies. This is a 64 Mbit SDR chip from an older, larger process; the dossier's ~9x is for DDR5 at 85 °C |
| The shape of *your* chip's tail between ~1e-7 and ~1e-1 failing fraction | The deep tail below ~1.5e-8 (one cell in 67 million). Code targets like SEC-DED's need p ~5e-9 or lower, so those safe intervals are **extrapolations** of the fitted tail (the script flags them EXTRAP) |
| Temperature activation energy over 25-65 °C | Behaviour at 85 °C or above (the part is likely rated 0-70 °C; section 6) |
| Data-pattern dependence, true/anti-cell layout, and VRT on one chip, over hours | Chip-to-chip and lot-to-lot spread (the dossier asks for ≥30 lots per vendor), or VRT growth over 1,000 hours |
| How error clustering in *real* adjacent addresses affects binary vs symbol codes | Chipkill. One x16 chip cannot lose "a chip"; RS-8 here uses byte symbols as a stand-in |
| A working measurement and analysis pipeline for tail statistics | Anything about oxide (IGZO) transistors. They are a different device; only the method transfers |
| A demo: "this chip would be fine refreshed every N seconds with code X" | That the 2e-19-per-read reliability target is met. One chip over a weekend sees ~1e-9 of the reads that would take |

**How the result scales up**

| Step | Where | Cost | What it adds |
|---|---|---|---|
| 1. This experiment | Home | $100-170 | Method, pipeline, one SDR chip |
| 2. Same on 2-3 boards | Home | +$30-63 per board | First look at chip-to-chip spread |
| 3. DDR3 with real DDR command control: Arty A7-100T + Antmicro rowhammer-tester | Home or makerspace (needs the Vivado toolchain) | ~$299 board [REPORTED] | A 256 MB DDR3L part, a modern-ish node, open Python control |
| 4. DRAM Bender on DDR4 DIMMs with temperature and VPP control | University lab (CMU, ETH, Rutgers and Georgia Tech lineages run it) | ~$14k per station [ESTIMATE in dossier] | Real modules, many lots; this is the dossier's Phase 1 |
| 5. Dossier Phase 1: 150 DDR4 + 24 DDR5 modules, 1,000 h soaks, open DDR5 testers | Funded lab | ~$124k [ESTIMATE in dossier] | The actual GO/NO-GO |

---

## 4. Platforms, ranked for a software builder

Every claim is tagged. **[UNVERIFIED]** means I could not confirm it in this session.

| Rank | Platform | Memory | How you take refresh away | Approx. cost | Skills | Verdict |
|---|---|---|---|---|---|---|
| **1** | **STM32F429I-DISC1** (also sold as 32F429IDISCOVERY) | ISSI IS42S16400J, 64 Mbit SDR SDRAM (4 banks × 4,096 rows × 256 columns × 16 bit) on FMC SDRAM bank 2 [REPORTED, S1-S2] | Relax: the controller's 13-bit refresh timer (COUNT ≥ 41) plus a slow clock gives up to a 4.19 s period. Pause: hold chip select high for any length [ESTIMATE from REPORTED register facts; below] | $30-63 [REPORTED, S10]; Digi-Key showed a 99-week lead time | C, flashing | **Start here.** All code, no FPGA |
| 1b | STM32F746G-DISCO | 128 Mbit Micron MT48LC4M32B2 class, only 64 Mbit wired (16-bit bus) [REPORTED, S11] | Same FMC methods; check pins and bank | ~$56 [UNVERIFIED] | C | Good substitute; the firmware needs a port |
| **2** | **Sipeed Tang Nano 20K** | GW2AR-18 FPGA with 64 Mbit, 32-bit SDR SDRAM in the package [REPORTED, S12] | You write the controller, so you issue (or skip) every refresh | $25-38 [REPORTED, S12] | Verilog; open tools (yosys, nextpnr-himbaechel, openFPGALoader) [REPORTED] | Best second step: full command control, same chip class |
| 3 | ULX3S (Lattice ECP5) | 32 MB SDR SDRAM [REPORTED, S14] | Same as Tang Nano; open toolchain | $145-235 [REPORTED, S14] | Verilog | 4x more cells; pricier |
| 4 | Digilent Arty A7-100T + Antmicro rowhammer-tester | 256 MB DDR3L, 16-bit [REPORTED, S16] | LiteDRAM "payload executor" sends raw DDR commands through the PHY; the playbook config has a `refresh` on/off key [REPORTED, S15] | $299 [REPORTED, S16] | Python + LiteX + Vivado | Real DDR3. Heavier toolchain; a makerspace-level step |
| 5 | A PC with ECC memory (AMD AM5 + ECC UDIMMs) | DDR5 ECC UDIMMs | Raise tREFI in the BIOS (max 65535 reported on AM5) and count corrected errors with Linux EDAC [REPORTED/UNVERIFIED, S19-S20] | $0 if you own one | Linux, BIOS | Real ECC, but small range and DDR5's on-die ECC hides raw errors. See 14.4 |
| 6 | DRAM Bender / SoftMC | DDR3/DDR4 DIMMs (DRAM Bender lists Alveo U200-class and BittWare XUPS3S boards; temperature and VPP control) [REPORTED, S17-S18] | Full command control | Thousands of dollars per board [ESTIMATE] | FPGA lab | University-lab route (step 4 above) |

### 4.1 How to take refresh away on the STM32F429I-DISC1

The STM32 has an FMC (flexible memory controller) that issues refresh automatically. Four options:

| Method | How | Range | Status |
|---|---|---|---|
| **A: relax** (primary for ≤4 s) | Program the refresh timer so each row is refreshed only every P. Hold for 3 periods, then restore. This *is* the product scenario (relaxed refresh) | 21.5 ms to 4.19 s at SDCLK 8 MHz; to 6.29 s at SDCLK 5.33 MHz | Uses only the documented COUNT range (13 bits, ≥41) [REPORTED, S3]. **Safest** |
| **B: pause** (primary for >4 s; fallback) | Issue precharge-all, then switch the chip-select pin (SDNE1, PB6) from FMC to a plain GPIO output held high. With chip select high the SDRAM ignores every command, including refresh. Give the pin back afterwards | Unlimited | The pin trick is not in ST's manual. The "chip select high = command inhibit" rule is standard SDR behaviour [UNVERIFIED-PK]. PB6 = SDNE1 on this board [UNVERIFIED-PK; check UM1670]. Timing is uncertain by up to one normal refresh window (~54 ms) |
| Z: COUNT = 0 | Write 0 to the timer | Unlimited | ST's STM32**H7** register text says "If the value programmed in the register is 0, no refresh is carried out" [REPORTED, S3]. **Not confirmed for the F4.** Off by default (`-DENABLE_METHOD_Z`); validate against method B |
| Not usable: self-refresh | The FMC can put the chip in self-refresh | - | In self-refresh **the chip refreshes itself** and may stay there indefinitely [REPORTED, S31] |
| Not usable: power-down | FMC command mode 110 | - | The chip does no refresh in power-down and must not stay longer than its refresh period [REPORTED, S31]. Whether the FMC wakes it to refresh is [UNVERIFIED] |

**The arithmetic for method A.** The full-array refresh period is rows × (COUNT + 1) / f_SDCLK. The board runs from its reset clock, the internal 16 MHz oscillator (HSI), so SDCLK = HCLK/2 = 8 MHz:
- Normal rate (ST's formula, with a 20-cycle margin): COUNT = (64 ms / 4,096) × 8 MHz − 20 = 125 − 20 = **105**, giving a 54 ms full window.
- To test 64 ms exactly: COUNT = 0.064 × 8e6 / 4,096 − 1 = **124**.
- Longest: 4,096 × 8,192 / 8e6 = **4.19 s**. With SDCLK = HCLK/3 (5.33 MHz): 6.29 s.
- The slow clock is deliberate. At ST's usual 90 MHz SDCLK the longest period would be only 4,096 × 8,192 / 90e6 = 0.37 s.

**Overlap check.** Run both A and B at 1, 2 and 4 s. They must agree within 2x (section 11).

---

## 5. Parts and tools

| Part | Spec that matters | Example part number | Approx. USD (Nov 2026) | Where |
|---|---|---|---|---|
| STM32F429I-DISC1 board | IS42S16400J SDRAM on FMC bank 2; ST-LINK with virtual COM port on USART1 (PA9/PA10) [REPORTED, S1, S6-S7] | STM32F429I-DISC1 (Digi-Key 497-16140-ND) | 30-63 (€26.23 ex-VAT Digi-Key IT; $45.61 TME; $62.99 Waveshare) [REPORTED, S10] | Digi-Key, TME, Waveshare, Mouser |
| USB cable | Fits the board's ST-LINK connector (mini-B on most units [UNVERIFIED]) | any | ~5 [ESTIMATE] | any |
| Thermocouple amplifier | MAX31855, K-type, 0.25 °C steps, SPI, 3.3 V | Adafruit 269 | 14.95 [REPORTED, S33] | Adafruit |
| K-type thermocouple | Glass-braid insulation (fine to 100 °C+), 1 m | Adafruit glass-braid K-type (product number [UNVERIFIED]) | ~10 [REPORTED, S36] | Adafruit |
| Heating pad | 5-12 V DC polyimide pad, 14 × 5 cm | Adafruit 4308 (or 1481, 5 V only) | ~7-8 (Adafruit 1481: $7.95) [REPORTED, S34] | Adafruit, Pi Hut |
| Thermostat | 12 V DC, NTC probe, -50 to 110 °C, relay | XH-W1209 | 4-7 [REPORTED, S35] | Many hobby stores |
| 12 V DC power adapter | Certified (UL/CE), ≥2 A, barrel plug | any | ~10 [ESTIMATE] | any |
| **Thermal cut-off fuse** | ~77 °C opening temperature, ≥2 A, in series with the heater | e.g. from an "assorted thermal fuse" kit [UNVERIFIED part] | ~1-5 [ESTIMATE] | Electronics stores |
| Insulated box | Small polystyrene foam box, ~20 × 15 × 10 cm | any | ~5-10 [ESTIMATE] | Craft or packaging store |
| Non-flammable base | Ceramic tile ≥15 × 15 cm | any | ~2 [ESTIMATE] | Hardware store |
| Kapton (polyimide) tape | Holds the thermocouple on the chip, heat-safe | any | ~6 [ESTIMATE] | any |
| Nylon standoffs, jumper wires | Female-female jumpers for the MAX31855 | any | ~6 [ESTIMATE] | any |
| Optional: USB-UART adapter | 3.3 V logic (CP2102 or FT232) | any | ~8 [ESTIMATE] | any |
| Optional: logic probe or 8-channel logic analyser | To confirm refresh really stops (method B) | any | ~10-15 [ESTIMATE] | any |

**Tools.** Soldering iron for 8 header pins. Computer with Python 3, numpy and pyserial. Arm GNU toolchain (`arm-none-eabi-gcc`). A flasher: open-source `stlink` (`st-flash`) or STM32CubeProgrammer. Multimeter.

---

## 6. Safety

> **SAFETY BOX: E6**
> - **Electrical.** Low voltage only. The board runs from USB 5 V. The heater runs from a certified 12 V DC adapter through the W1209 relay. **Never** build or open anything that touches mains voltage. Power the heater from its own adapter, never from the board's USB.
> - **Heat and fire.** Maximum box temperature 70 °C; aim for a chip surface of 25, 45 and 65 °C. Never exceed 85 °C. Put the heater on a ceramic tile, never on the foam. Wire a ~77 °C thermal cut-off fuse in series with the heater and tape it to the pad: it opens if the thermostat sticks. Set the W1209 high-temperature limit. Do not leave the box heating unattended until you have watched one full heat-up and one hold of at least 30 minutes. Keep a smoke alarm in the room. Unplug the heater when you are not running.
> - **Burns.** Surfaces at 65 °C can burn skin in seconds [UNVERIFIED-PK]. Let the box cool before handling the board.
> - **Component ratings.** The SDRAM part with the "-7TL" suffix is most likely commercial grade, 0-70 °C (a sister "-5TL" part lists 70 °C max; the "-7TLI" industrial part is rated -40 to 85 °C [REPORTED, S9]; one distributor claims 0-85 °C for -7TL [REPORTED, conflicting]). 65 °C stays inside the stricter reading.
> - **Static.** Touch a grounded metal object before handling the board. Hold it by the edges.
> - **Chemicals.** None needed. If you clean flux with isopropyl alcohol: it is flammable (see its SDS), so use it only with the heater unplugged and cold, in a ventilated room, and store it closed.
> - **Not at home.** Do not cool chips with sprays or liquid nitrogen to repeat the cold-boot result. Do not run method Z or modified firmware on a PC's memory. For the PC route (14.4), do not add heaters inside a PC case.

---

## 7. Build

1. **Buy the parts** in section 5. Read the SDRAM marking on your board with a magnifier and write it down.
2. **Install the tools.** Arm GNU toolchain, `stlink` or STM32CubeProgrammer, Python 3 with `pip install numpy pyserial`.
3. **Prove the board's SDRAM works with ST's own code first.** Run ST's STM32CubeF4 SDRAM example for this Discovery board (from ST's firmware package; exact path [UNVERIFIED]). If it fails, the board is faulty and nothing else here will work.
4. **Check the reference firmware against the manuals before flashing.** It is written from memory and **untested on hardware**. Open `stm32_retention/regs_f429.h` and `sdram_fmc.c` next to ST's RM0090 (FMC section) and UM1670 (board schematic). Check:
   - the FMC SDRAM register base (0xA0000140) and the bit positions of SDCR, SDTR, SDCMR, SDRTR and SDSR;
   - the 38 SDRAM pins and AF12;
   - that SDNE1 is on PB6 on your board;
   - the USART1 pins (PA9/PA10, AF7).
5. **Build and flash.** In `code/T3_dram/stm32_retention/`, run `make syntax` (works on any PC), then `make` and `make flash`.
6. **Talk to it.** Open a serial terminal at 115200 baud, 8N1 (eight data bits, no parity, one stop bit). Press reset: you should see `HELLO,e6-ret-0.1,IS42S16400J,4194304,16,8000000,A|B|C`. Type `PING`: expect `PONG`. If nothing arrives, see section 13.
7. **Fit the thermometer.** Solder the MAX31855 header. Wire VIN→3V3, GND→GND, CLK→PE2, CS→PE3, DO→PE4. One user reports PE2-PE5 free on this board [REPORTED, S32]; confirm in UM1670. Tape the thermocouple tip flat on top of the SDRAM package with Kapton tape. Type `TEMP`: expect room temperature.
8. **Build the thermal box.**
   - Put the tile in the foam box and stick the heater pad on the tile.
   - Mount the board on nylon standoffs about 1 cm above the pad.
   - Tape the W1209 probe next to the SDRAM.
   - Wire the heater through the W1209 relay and the thermal fuse to the 12 V adapter. Bring the USB cable out through a slot.
   - Set the W1209 to the target temperature with 0.5 °C hysteresis.
9. **Smoke test at room temperature:**
   `python3 capture_retention.py --port /dev/ttyACM0 --temp-c 25 --repeats 1 --waits 0.064 1.024 16.384 65.536 --out smoke.log`
   Expect a clean control run, zero failures at 64 ms and 1 s, and a few to a few thousand at 65 s (section 2.4).
10. **Dry run without hardware** at any time: `python3 capture_retention.py --simulate --temp-c 45 --out sim.log`, then `python3 retention_map.py analyze sim.log`.

---

## 8. Measurement protocol

1. **Data patterns: why they matter.**
   - A **true cell** stores 1 as charge; an **anti cell** stores 0 as charge [REPORTED, S30].
   - Leakage only runs from charged to discharged. So a true cell can fail only while it holds 1, and an anti cell only while it holds 0.
   - Some chips mix true and anti cells in blocks, often one block per subarray; one study saw blocks of 512 rows [REPORTED, S30].
   - **All-0 plus all-1 therefore test every cell exactly once in its charged state.** The script uses that pair as its main retention curve (F_solid).
   - Neighbours matter too. A cell's retention shifts with the data in nearby cells (data-pattern dependence) [REPORTED, S23]. For some newer devices a simple 0/1 pattern found only ~15% of failures [REPORTED, secondary, S23].
   - Default set: ALL0, ALL1, CHECKER, CHECKER inverted, ROWSTRIPE, RANDOM (fixed seed). Add COLSTRIPE and inverted stripes if time allows.
2. **Waits.** 64 ms to 65.5 s in factor-2 steps: 11 values. `capture_retention.py` uses method A up to 4.096 s and method B above.
3. **Temperatures.** 25, 45 and 65 °C on the chip surface, in that order. After each change, wait until the thermocouple has been steady within ±0.5 °C for 30 minutes.
4. **Repeats.** At least 5 full sweeps per temperature. Repeats catch **variable retention time (VRT)**: cells that jump between a long and a short retention time at random, like random telegraph noise (RTN) in transistors [REPORTED, S23-S24, S28]. The script shuffles pattern order in each repeat, so slow drift does not line up with one pattern.
5. **Controls.** Each temperature starts with a control run (method C: write, read, no pause). It must show **zero** failures.
6. **Early stop.** A sweep stops once a run fails more than 1% of all bits (`--stop-ber 1e-2`). Beyond that you are measuring the bulk, not the tail.
7. **Logging.** The firmware streams every failing word (address, expected and read value) for the first 20,000 failing words of a run, plus exact totals. The host adds a timestamp before each run. Do not edit the log by hand; annotate with lines starting with `#`.
8. **Run it:** `python3 capture_retention.py --port /dev/ttyACM0 --temp-c 45 --out e6_45C.log`. Time: at most ~2.1 h per temperature with 5 repeats and 6 patterns (`--plan` prints the estimate), plus heat soak and logging time. Disable sleep on the host PC.
9. **Optional, recommended:** repeat 25 °C at the end. Agreement with the first 25 °C run shows the chip did not change during the campaign.

---

## 9. Data sheet and log template

**Paper log, one line per temperature block:**

| Date/time | Board ID and SDRAM marking | Setpoint °C | TC reading start/end °C | Room °C | Log file | Repeats done | Control run clean? | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-__-__ __:__ | | 25 | / | | e6_25C.log | | yes / no | |

**What the log file looks like** (written by the firmware and `capture_retention.py`; full format in the header of `retention_map.py`):

```
HELLO,e6-ret-0.1,IS42S16400J,4194304,16,8000000,A|B|C
H,1793700000.0
RUN,17,B,1,0,1234,16384,2,45.0
TEMP,17,start,45.12
F,17,1a2b3c,ffff,fffb
TEMP,17,end,45.25
END,17,812,815,815,0,812,16391,OK
```

`END` fields: run id, failing words, failing bits, bits 1→0, bits 0→1, words logged, retention interval actually tested (ms), and OK or TRUNC (cap hit; the counts stay exact).

---

## 10. Analysis

```
python3 retention_map.py analyze e6_25C.log e6_45C.log e6_65C.log --report e6_report.md --csv e6_curve.csv
```

The report has eight parts:
1. **Retention CDF** per temperature: the failing fraction at each wait, mean of repeats, with failing-bit counts. Also a lognormal fit and the local tail slope k (F ∝ t^k).
2. **Tail quantiles** 1e-7 to 1e-2, including the Oxide-Tail quantiles 1e-4 and 2e-5. On 67 million cells those carry ±1.2% and ±2.7% statistical error.
3. **Temperature acceleration:** pairwise and a global Arrhenius fit (Ea in eV; "retention halves every X °C").
4. **Cell polarity:** true and anti rows, and the block size of the interleave.
5. **Pattern coverage:** what share of all failing cells each single pattern finds.
6. **VRT:** cells that fail in some repeats but not others; strict VRT (first-failure wait varies ≥4x between repeats); and how fast new failing cells appear across repeats.
7. **ECC.** Five codes:
   - SEC-DED (72,64);
   - BCH-4 (552,512);
   - BCH-12 (640,512), the dossier's binary code;
   - SSC-RS (18,16), byte symbols;
   - RS-8 (80,64), the dossier's code.

   Each runs with three mappings of cells to codewords: **adjacent** (real neighbouring addresses), **dq** (one symbol per data pin) and **random** (pseudo-random shuffle). Clustering is measured against chance coincidence. The output is the safe interval for target 1 and target 2, with EXTRAP flags.
8. **Verdict:** your 65 °C factor against the dossier's gate (PASS ≥24x, NO-GO <4x) and its ~9x / ~13x.

**`--selftest`** builds a synthetic 4 Mbit chip with a lognormal tail, VRT, coherent 2-bit clusters, 128-row anti-cell blocks and pattern dependence. It emulates the firmware's log line by line and checks that the pipeline recovers what was planted (27 checks, including a C-vs-Python check of the pattern generator). It passes, exit 0, in ~7 s.

---

## 11. Pass/fail criteria

**A. Is the setup valid? All must pass before you believe any number.**

| Check | Pass | Fail means |
|---|---|---|
| Control runs (no pause) | 0 failing bits at every temperature | Wiring, timing or firmware error |
| 64 ms at 25 °C | 0 failing bits (prediction: 0) | Setup error, or a damaged chip |
| Method A vs B at 1, 2, 4 s (≥20 failing bits) | Within 2x | One method is not doing what you think |
| Repeat-to-repeat scatter where ≥100 bits fail | Coefficient of variation under 30% | Temperature drift or VRT overload |
| Thermocouple start/end | Within ±1 °C of setpoint | Box not settled |

**B. The thesis at desk scale** (same lines as dossier section 5.R; RS-8 adjacent mapping, VRT multiplier, target 2):

| Result at 65 °C | Verdict | Prediction |
|---|---|---|
| ≥24x of 64 ms (≥1.54 s) | **PASS** | Central 42x (band 21-169x) |
| 4x-24x | PARTIAL | Only the pessimistic end |
| <4x (<256 ms) | **NO-GO** for this chip | Not expected |

Also record:
- the SEC-DED factor at 45 °C, target 1 (prediction ~17x, without clustering);
- the share of multi-byte error events (the dossier's NO-GO line is >10% multi-chip events; here, >10% of RS-8 events spanning more than one byte is the analogue).

---

## 12. What would surprise you (results that would mean something new)

- **Failures at 64-256 ms at 25 °C,** with clean controls. Weak cells far left of the published tail. That chip would defeat simple relaxed refresh.
- **A kink in the tail:** two straight segments on the probit plot, with different Ea. That would be two leakage mechanisms (tail ~0.35 eV vs main ~0.6 eV is the reported picture) that you can separate on a desk.
- **Ea well outside 0.3-1.1 eV,** or retention that *rises* with temperature for some cells. That points to telegraph-like trap physics (VRT), not plain leakage.
- **Strong clustering:** many multi-bit events in the adjacent mapping, well above chance. Clustered errors are the dossier's show-stopper number 1; they would favour symbol codes (RS) over binary BCH.
- **VRT that keeps growing:** new failing cells still appearing after many repeats, at a rate that does not flatten. That is the dossier's "unknown VRT growth" (show-stopper 3), on your desk.
- **Method A and B disagree** while both are working. That would mean relaxed refresh and paused refresh are not equivalent, which matters for how a controller should relax refresh.
- **A pass well above 169x or a fail below 21x.** Either is outside the band; recheck the setup, then believe it.

---

## 13. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| No HELLO on the serial port | Wrong port or baud; VCP solder bridges SB11/SB15 open [REPORTED, S6] | Check the port; use an external 3.3 V USB-UART on PA9/PA10 |
| Garbled characters | VCP issue reported on this board [REPORTED, S6] | Lower the baud rate or use an external adapter |
| `ERR,sdram init failed` | FMC registers or pins wrong (the firmware is untested) | Diff `sdram_fmc.c` against ST's BSP code; confirm step 3 passed |
| Control run fails | Timing, mode register or pin error; or code touching SDRAM | Recheck SDTR/SDCMR values; try CAS latency 2; make sure nothing runs from SDRAM |
| Every word fails at every wait | Wrong bank address (bank 1 is 0xC0000000; this board uses bank 2, 0xD0000000) or SDNE1 not handed back after method B | Check `SDRAM_BANK2_BASE`; check PB6 MODER after the pause |
| Nothing fails even at 65 s and 65 °C | Refresh never stopped (PB6 is not SDNE1 on your revision), or the chip is exceptional | Probe PB6 during a pause with a logic probe; compare with method A at 4 s and 65 °C (prediction ~1e-4 to 2e-4) |
| Temperature overshoots or drifts | Hysteresis too wide; box leaks | Set 0.5 °C hysteresis; close gaps; wait 30 min |
| Many TRUNC runs | Normal at high failing fractions | Counts stay exact. Lower `--stop-ber` to 1e-3 for full maps |
| Board resets when the heater switches | Shared supply or ground noise | Separate adapter for the heater; keep its wiring away from the board |
| Capture stops overnight | Host PC slept | Disable sleep; the log is flushed line by line, so restart where it stopped |
| LCD shows noise | The firmware does not drive the LCD | Ignore |

---

## 14. Other platforms: notes

1. **Tang Nano 20K.**
   - The SDRAM sits inside the FPGA package and is 32 bits wide [REPORTED, S12]. You write the SDRAM controller (or adapt one).
   - nand2mario's NESTang project targets this board [REPORTED, S13]; whether its SDRAM code is easy to reuse is [UNVERIFIED].
   - The upside: you choose exactly when each refresh happens, so method A's 4.19 s ceiling and method B's pin trick are not needed.
   - Port the protocol: the same RUN/F/END lines over the board's USB-UART, and the same analysis.
2. **ULX3S.** Same idea with 4x the cells and an open ECP5 toolchain [REPORTED, S14].
3. **Arty A7 + rowhammer-tester.**
   - The rowhammer-tester bypasses the LiteDRAM controller and sends command sequences through the PHY's DFI interface [REPORTED, S15]. The playbook config has a `refresh` key [REPORTED, S15].
   - A clean "disable refresh for T seconds" retention script was not found in the docs [UNVERIFIED]; you may need to write one.
   - Good for: real DDR3 timing and a more modern process. The DDR3L part number on current boards is [UNVERIFIED] (Digilent notes a memory change).
4. **A PC with ECC memory: real ECC, but read the warnings.**
   - **Setup.** An AM5 (Ryzen 7000/9000) board that supports ECC UDIMMs. Linux has EDAC reporting for Ryzen 7000 since kernel 6.5 [REPORTED, S20]. `rasdaemon` and `ras-mc-ctl --summary` log corrected errors per DIMM [REPORTED, S20]. DDR5 modules report their own temperature through the `spd5118` driver [REPORTED, S21].
   - **The knob.** Some AM5 BIOSes expose tREFI (the spacing between refresh commands) up to 65535; overclockers run it there [REPORTED/UNVERIFIED anecdotes, S19]. If the unit is memory-clock cycles at DDR5-6000 (3,000 MHz) [UNVERIFIED], 65535 cycles = 21.8 µs against the standard 3.9 µs. That is only **5.6x**: a 179 ms effective window. "Fine granularity refresh" mode halves it [REPORTED, S19].
   - **What you will probably see.** The central model gives ~0.1 weak cell in 32 GB at 45 °C and ~170 at 65 °C for a 179 ms window [ESTIMATE]. DDR5's on-die ECC fixes single errors inside each chip before EDAC sees them. **Expect zero corrected errors.** That is consistent with the thesis, but it is weak evidence.
   - **Risks.** Relaxed refresh can corrupt memory, crash the OS and damage files. Boot a live USB stick; disconnect or do not mount internal drives; save nothing important. Know how to clear the BIOS settings (CMOS reset) if the PC will not start. Do not add heaters; read the module temperature and accept what you get. Community tREFI claims are anecdotes [UNVERIFIED].
5. **DRAM Bender / SoftMC.** These are research-grade, with full command control, temperature and VPP control, and DDR3/DDR4 DIMMs [REPORTED, S17-S18]. They are the dossier's Phase 1 tool. Use them through a university collaboration.

---

## 15. How this connects to the Oxide Tail Spec (the study's Monday action)

| Oxide Tail Spec asks for | This experiment gives you |
|---|---|
| The 1e-4 to 2e-5 quantile of attoamp leakage over ≥1e5 cells | The same quantiles of a femtoamp leakage distribution over 6.7e7 cells, with error bars |
| Temperature dependence at 85-125 °C | An Arrhenius fit over 25-65 °C, and the code to fit it |
| The 1e-4 quantile of RTN | VRT statistics: the same "switching trap" physics in a retention test |
| Each concept's pass/kill line | A pipeline that turns a measured tail into an ECC-safe interval and a PASS/NO-GO |

What you would bring to a university oxide group: a working, tested analysis pipeline, and a one-page result from real silicon. Use them to sharpen the spec and its cost estimate.

---

## 16. Verification of the code in this folder (run 2026-11-03)

| Command | Result |
|---|---|
| `python3 retention_map.py --selftest` | 27/27 checks pass, exit 0 (~7 s) |
| `python3 retention_map.py predict` | exit 0; numbers in section 2 |
| `python3 capture_retention.py --selftest` | 8/8 checks pass, exit 0 (pyserial absent: simulate path) |
| `python3 capture_retention.py --simulate ...` then `retention_map.py analyze ...` | exit 0 end to end |
| `make syntax` (gcc -fsyntax-only -std=c11 -Wall -Wextra, default and with -DENABLE_METHOD_Z) | clean |
| `host_test_patterns.c` vs Python `pattern_words()` | 624/624 samples identical |
| Firmware on real hardware | **Not tested** |

---

## Sources

Tags: [DATASHEET] vendor document; [REPORTED] paper, press, forum or distributor page, usually read as a search snippet in this session; [ESTIMATE] my calculation; [UNVERIFIED] could not confirm; [UNVERIFIED-PK] from my prior knowledge, no URL confirmed. Several hosts were unreachable from this session (docs.rs, the ISSI datasheet mirror); those facts rest on search snippets. Prices are snapshots, approximate as of Nov 2026.

- **S1** ST board-support code for the STM32F429I-Discovery SDRAM (mbed mirror): IS42S16400J, FMC bank 2, 90 MHz timings. https://os.mbed.com/teams/ST/code/BSP_DISCO_F429ZI/docs/tip/stm32f429i__discovery__sdram_8c_source.html [REPORTED]
- **S2** 21ic forum SDRAM test: 4 banks × 4,096 rows × 256 columns × 16 bit, 12 row bits and 8 column bits. https://bbs.21ic.com/icview-2515182-1-1.html [REPORTED]
- **S3** FMC_SDRTR register text (STM32H7 device description, via docs.rs search snippets): 13-bit COUNT, at least 41 SDRAM clocks, COUNT = period/rows − 20, the timer starts on write, "if the value programmed is 0, no refresh is carried out". https://docs.rs/stm32h7/latest/stm32h7/stm32h743/fmc/sdrtr/struct.SDRTR_SPEC.html [REPORTED; F4 equivalence UNVERIFIED]
- **S4** FMC SDCMR/SDSR descriptions (command register, power-down status, auto-refresh precedence). https://docs.rs/stm32-hal2/1.8.2/stm32_hal2/pac/fmc/sdcmr/index.html ; https://docs.ros.org/en/api/picovoice_driver/html/group__FMC__SDRAM__Mode__Status.html [REPORTED]
- **S5** ST community: F7 SDRAM reports power-down and corrupted data after a re-init (anecdote). https://community.st.com/stm32cubemx-mcus-29/stm32f7-fmc-sdram-error-after-reinit-3256 [REPORTED]
- **S6** ST community: STM32F429I-DISC1 VCP on USART1 via SB11/SB15; a garbled-VCP report. https://community.st.com/s/question/0D50X00009XkeWa/stm32f429disco1-vcp-connection ; https://community.st.com/stm32-mcus-boards-and-hardware-tools-26/stm32f429-disco1-vcp-connection-92741 [REPORTED]
- **S7** Zephyr board page: console on USART1, PA9/PA10, 115200 8N1. https://docs.zephyrproject.org/latest/boards/st/stm32f429i_disc1/doc/index.html [REPORTED]
- **S8** ISSI 64Mb SDRAM datasheet: 4,096 refresh cycles per 64 ms (commercial, industrial, A1), 16 ms for A2. https://www.electronicsdatasheets.com/download/122066.pdf?format=pdf [DATASHEET, read via search snippet; host blocked]
- **S9** Temperature grades: Arrow IS42S16400J-5TL commercial, 70 °C max (listed obsolete) https://www.arrow.com/en/products/is42s16400j-5tl/integrated-silicon-solution-inc.html ; RS IS42S16400J-7TLI −40 to 85 °C, 143 MHz https://uk.rs-online.com/web/p/sdram/8115125 ; Findchips claims 0-85 °C for -7TL-TR https://origin-www.findchips.com/detail/is42s16400j-7tl-tr/Integrated-Silicon-Solution-Inc [REPORTED, conflicting; -7TL range UNVERIFIED]
- **S10** Board prices and stock: Digi-Key (497-16140-ND, 99-week lead time) https://www.digikey.com/en/products/detail/stmicroelectronics/STM32F429I-DISC1/5731713 ; Digi-Key IT €26.23 https://punchouttest.digikey.it/en/products/detail/stmicroelectronics/STM32F429I-DISC1/5731713 ; TME $45.61 https://www.tme.com/us/en-us/details/stm32f429i-disc1/stm-development-kits/stmicroelectronics/ ; Waveshare $62.99 https://www.waveshare.com/product/32F429IDISCOVERY.htm [REPORTED]
- **S11** STM32F746G-DISCO: 128-Mbit SDRAM with 64 Mbit accessible; MT48LC4M32B2 driver. https://estore.st.com/en/stm32f746g-disco-cpn.html ; https://developer.mbed.org/teams/ST/code/SDRAM_DISCO_F746NG//file/370f402a2219/SDRAM_DISCO_F746NG.h [REPORTED; price UNVERIFIED]
- **S12** Tang Nano 20K: Sipeed wiki https://wiki.sipeed.com/hardware/en/tang/tang-nano-20k/nano-20k.html ; launch at $25 https://www.cnx-software.com/?p=114273 ; datasheet "32Mbit QSPI NOR + 64Mbit SDRAM" https://aws.robu.in/wp-content/uploads/2024/03/Datasheet-236.pdf ; Hackaday, "8 Mbyte, 32-bit SDR SDRAM in the package" https://hackaday.com/2026/09/28/the-fpga-chronicles-exploring-the-tang-nano-20k/ ; prices $26.80-38 (Reach.dog, Spotpear, Walmart listings); open toolchain report https://www.elektroda.pl/rtvforum/topic3979636.html [REPORTED]
- **S13** nand2mario GitHub (NESTang; DDR3 controller for Tang Primer 20K). https://github.com/nand2mario [REPORTED; SDRAM-controller reuse UNVERIFIED]
- **S14** ULX3S: Crowd Supply $145-235, 32 MB SDRAM. https://crowdsupply.com/radiona/ulx3s ; https://radiona.org/ulx3s/ [REPORTED]
- **S15** Antmicro rowhammer-tester: https://github.com/antmicro/rowhammer-tester ; playbook `refresh` key https://rowhammer-tester.readthedocs.io/en/latest/playbook.html ; payload executor via DFI https://opensource.googleblog.com/2021/11/Open%20source%20DDR%20controller%20framework%20for%20mitigating%20Rowhammer.html ; Arty and ZCU104 targets https://antmicro.com/blog/2021/08/open-source-ddr-test-framework-for-rowhammer/ [REPORTED]
- **S16** Arty A7-100T: $299, 256 MB DDR3L, 16-bit. https://digilent.com/shop/arty-a7-100t-artix-7-fpga-development-board/ [REPORTED; DDR3L part number UNVERIFIED]
- **S17** DRAM Bender (IEEE TCAD; arXiv 2211.05838) https://arxiv.org/html/2211.05838v6 ; FMS 2024 talk: XCU200 (DDR4), BittWare XUPS3S, temperature and VPP control https://files.futurememorystorage.com/proceedings/2024/20240808_TEST-301-1_LUO.pdf [REPORTED]
- **S18** SoftMC (HPCA 2017). https://research.nvidia.com/publication/2017-02_softmc-flexible-and-practical-open-source-infrastructure-enabling-experimental.md ; https://arxiv.org/pdf/1805.03195v1.pdf [REPORTED; board model UNVERIFIED]
- **S19** AM5 tREFI ceiling 65535 and its temperature sensitivity: IgorsLab https://www.igorslab.de/en/no-brainer-questionable-communication-and-a-missed-opportunity-benchmark-preview-of-amd-expo-1-2-and-ultra-low-latency-mode/3/ ; forum post https://r.datuan.dev/r/overclocking/s/tfdLmODv5p ; FGR halves the interval https://www.noobfeed.com/hardware/ddr5-refresh-modes-am5-fgr [REPORTED/UNVERIFIED anecdotes]
- **S20** Linux EDAC for Ryzen 7000 (kernel 6.5) https://www.phoronix.com/news/Linux-6.5-EDAC ; rasdaemon how-to https://setphaserstostun.org/posts/monitoring-ecc-memory-on-linux-with-rasdaemon ; Level1Techs ECC thread https://forum.level1techs.com/t/how-do-i-know-if-ecc-is-working-enabled/236913 [REPORTED]
- **S21** Linux `spd5118` DDR5 temperature-sensor driver. https://docs.kernel.org/hwmon/spd5118.html [REPORTED]
- **S22** Halderman et al., "Lest We Remember: Cold Boot Attacks on Encryption Keys," USENIX Security 2008: several seconds of retention at room temperature; <1% decay after 10 min near −50 °C; 0.17% after 60 min in liquid nitrogen. https://jhalderm.com/pub/papers/coldboot-sec08.pdf [REPORTED]
- **S23** Liu et al., "An Experimental Study of Data Retention Behavior in Modern DRAM Devices," ISCA 2013 (248 DDR3 chips; data-pattern dependence; VRT). https://pdl.cmu.edu/PDL-FTP/NVM/dram-retention_isca13_abs.shtml ; retrospective https://arxiv.org/pdf/2306.16037 ; DATE 2015 "15% coverage" https://past.date-conference.com/proceedings-archive/2015/pdf/0258.pdf [REPORTED]
- **S24** Patel et al., "The Reach Profiler (REAPER)," ISCA 2017 (368 LPDDR4 chips). https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_paper.pdf [REPORTED]
- **S25** RAIDR, ISCA 2012 https://www.pdl.cmu.edu/ftp/NVM/raidr-isca12.pdf ; "~30 cells below 128 ms, ~1000 below 256 ms in 32 GB" (secondary) https://mdpi.com/530668 [REPORTED]
- **S26** "<0.001% of cells below 3 s at 45 °C, worst module." arXiv 1712.08304. https://arxiv.org/pdf/1712.08304 [REPORTED via snippet]
- **S27** 223 LPDDR4 chips: exponential BER growth with temperature, ~10x per 10 °C. arXiv 2109.14520. https://arxiv.org/pdf/2109.14520 [REPORTED via snippet; exact factor UNVERIFIED]
- **S28** Khan et al., SIGMETRICS 2014 (testing alone is insufficient against intermittent failures; ECC plus a few hours of testing works). https://www.pdl.cmu.edu/ftp/NVM/khan-efficacy-sigmetrics2014.pdf ; AVATAR, DSN 2015 https://fast.cc.gatech.edu/papers/DSN_2015_1.pdf [REPORTED]
- **S29** Activation energies: tail ~0.35 eV, normal ~0.6-0.7 eV. US patent 6,697,992 https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6697992 ; Weber et al. 2006, main and tail branches https://tore.tuhh.de/entities/publication/d416ddba-a69b-41a0-a42d-819c2c4c0338 [REPORTED]. Hamamoto, Sugiura and Sawada, "On the retention time distribution of dynamic random access memory (DRAM)," IEEE Trans. Electron Devices 45(6), 1998 [UNVERIFIED: not found by search; cited from prior knowledge]
- **S30** True and anti cells, and interleaving by subarray: BEER https://arxiv.org/pdf/2009.07985 ; DRAMScope https://arxiv.org/pdf/2405.02499 ; HARP https://arxiv.org/pdf/2204.10387 [REPORTED]
- **S31** Power-down does no refresh and must not exceed the refresh period; self-refresh can last indefinitely: Microchip DDR controller docs https://onlinedocs.microchip.com/oxy/GUID-2ACDA668-0A87-46A1-B7FC-9DC74A5461AD-en-US-2/GUID-A8858313-192F-4803-BA18-541AB0AA730F.html and https://onlinedocs.microchip.com/oxy/GUID-2ACDA668-0A87-46A1-B7FC-9DC74A5461AD-en-US-2/GUID-BAA22F95-84CE-41BD-96B5-C2BDD81147A7.html ; ProMOS V55C2256164VB datasheet wording (search snippet) [REPORTED]
- **S32** ST community: PE2-PE5 (and PF6, PG2, PG3, PG9) usable on the F429 Discovery, per one user citing UM1670 section 6.14. https://stcommunity.st.com/t5/stm32-mcus-products/which-pins-are-usable-on-the-f429-discovery-disc1-board/td-p/393213/page/2 [REPORTED, anecdote]
- **S33** Adafruit MAX31855 breakout, product 269, $14.95. https://www.adafruit.com/products/269 [REPORTED]
- **S34** Adafruit heating pads: 1481 (10 × 5 cm, 5 V, $7.95) https://www.adafruit.com/products/1481 ; 4308 (14 × 5 cm, 5-12 V, £5.80 at Pi Hut) https://thepihut.com/collections/new-products-maker/products/electric-heating-pad-14cm-x-5cm [REPORTED]
- **S35** W1209 thermostat: 12 V, -50 to 110 °C, NTC probe, relay; $4-7. https://shillehtek.com/blogs/shillehtek-product-manuals/w1209-12v-digital-temperature-controller-thermostat-switch-module-manual ; https://www.tinytronics.nl/shop/en/sensors/temperature/digital-thermostat-module-with-relay-xh-w1209 [REPORTED]
- **S36** Glass-braid K-type thermocouple, ~$10 at Adafruit (tutorial mention). https://www.adafruit.com/products/269 (linked tutorials) [REPORTED; product number UNVERIFIED]
- **S37** This study: [dossiers/raw-ber-contract.md](../dossiers/raw-ber-contract.md) (sections 2.1, 2.5, 5.R), [models/raw-ber-contract.py](../models/raw-ber-contract.py) (85 °C retention anchors, lognormal fit), [models/dram_cell_physics.py](../models/dram_cell_physics.py) (`RET_HALVING_C = 10`), [research/stage3/decision.json](../research/stage3/decision.json) [MODEL/ESTIMATE as tagged there]
- **[ESTIMATE]** Everything computed in section 2 and in the code: leakage arithmetic, Arrhenius factors, expected failing cells, safe intervals, refresh-timer limits (COUNT 105/124, 4.19 s, 6.29 s), the tREFI 5.6x arithmetic, and the run-time estimates.
