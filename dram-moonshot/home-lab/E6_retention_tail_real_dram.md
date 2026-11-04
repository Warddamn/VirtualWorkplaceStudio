# E6: Map the retention tail of a real DRAM chip on your desk

*Track T3 of the home-lab guides. As of 2026-11-04: the firmware was checked against ST's own code, built with a real ARM compiler and run in two emulators on that date (section 16). Prices are search-result snapshots from 2026-11-04.*

This is the study's **FASTEST PROOF** ([raw-ber-contract](../dossiers/raw-ber-contract.md)) shrunk to a desk. You map how long every cell of a real memory chip holds its data. Then you compute how much less often it would need refreshing if an error-correcting code caught the few weak cells. It is mostly code, so it suits a software builder.

**In one paragraph.** DRAM (dynamic random-access memory) stores each bit as charge on a tiny capacitor that leaks. Every cell is rewritten ("refreshed") every 64 ms, because a rare few leak fast. Most cells hold their data for seconds or minutes. You will take refresh away from a 64-megabit SDR SDRAM chip (single-data-rate synchronous DRAM, an older and simpler cousin of the DDR (double-data-rate) memory in PCs) for 64 ms to 65 s, at 25, 45 and 65 °C, and log the address of every bit that flips. That gives the chip's **retention tail**. A script then puts the measured failures into error-correcting codewords and finds the longest refresh interval that keeps uncorrectable errors under a target. That is your chip's **refresh relaxation factor**, the number the dossier puts at ~9x for DDR5 server memory.

**Files for this experiment**

| File | What it is |
|---|---|
| [code/T3_dram/retention_map.py](code/T3_dram/retention_map.py) | Expected results (`predict`), analysis (`analyze`), `--selftest`. Python + numpy only |
| [code/T3_dram/capture_retention.py](code/T3_dram/capture_retention.py) | Drives the board over USB serial, logs everything; `--simulate` and `--selftest` need no hardware |
| [code/T3_dram/stm32_retention/](code/T3_dram/stm32_retention/) | Reference firmware in C for the STM32F429I-DISC1. Builds and links (5.8 KB of flash); every register value matches ST's code; runs end to end in emulation. **Untested on a real board** |
| [tools/e6_regcheck.py](tools/e6_regcheck.py) | Repeats the register, pin and SDRAM-setup comparison against ST's sources (section 7, step 4) |

---

## 0. At a glance

| Item | Value |
|---|---|
| Difficulty | **3 of 5.** The firmware is bare-metal code that has never run on a real board. It builds, matches ST's code register by register and runs end to end in emulation (section 16), but the first power-on is still a debugging session. You also flash a board, run Python, solder 8 header pins and wire a 12 V heater circuit |
| Time | 1-2 weekends to build and debug. About 10-12 h of runs plus 2-3 h of heat-up and soak (3 temperatures). The heated blocks are attended (check every 30-60 min); the 25 °C block can run overnight. 10 minutes to analyse |
| Cost tier | **$$: about $115-200** (board $32-66, thermocouple kit ~$25, heater, thermostat and two cut-outs ~$20-50, wiring and fuse ~$10, rest ~$30) [REPORTED prices of 2026-11-04 where section 5 shows them, else ESTIMATE] |
| Skills | Install a toolchain, read a register table, run Python scripts, follow a wiring list |
| What you get | A retention map of 67,108,864 real DRAM cells, its tail quantiles, temperature activation energy, VRT share (variable retention time: cells whose retention jumps between values), error clustering, and the longest refresh interval an error-correcting code (ECC) makes safe |
| Main risk | Heat and fire: a home-built heater in a foam box. Mitigated by a stuck-on test that proves the heater alone cannot push the box air above 75 °C, the thermostat's over-temperature cut, an 80 °C bimetal cut-out in the box air, a thermal fuse on the heater, attended heating only, and a non-flammable base (Safety box, section 6) |

---

## 1. Why this experiment, and what it connects to

- **The thesis it tests.** The raw-ber-contract dossier claims that error-correcting codes (ECC) can carry the rare weak cells, so refresh can run far less often. It estimates ~9x less refresh energy on DDR5 server modules at 85 °C. On retired DDR4 it estimates ~11x with two memory channels in lockstep and ~4x on a single channel ([decision.json](../research/stage3/decision.json), [dossier](../dossiers/raw-ber-contract.md) sections 2.5 and 12.1) [ESTIMATE] (study model). *Corrected 2026-11-04:* the earlier ~13x gave DDR4 the 128 check bits of a DDR5 line; a DDR4 line has 64.
- **The study's own gate.** NO-GO if the chipkill-safe interval is under 4x the standard refresh window at 65 °C. (Chipkill means a code that survives the loss of a whole memory chip.) PASS needs ≥24x at 65 °C **and** ≥6x at 85 °C (dossier section 5.R). Your chip is rated to about 70 °C, so you can test only the 65 °C half. You will compute the same numbers for your chip.
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

(1 fA = 1e-15 A; 1 aA = 1e-18 A.) **A 10 s retention time means a leak of about 1.6 fA.** Your chip is a 67-million-channel femtoammeter (the current scale rests on the assumed 20 fF and 0.82 V, so read it to within a factor of 2-3). The hot-side and AND-STACK cells in this study need attoamp tails; this is the same equation one decade further on.

### 2.2 Temperature: leakage is thermally activated

**Law: Arrhenius.** Leakage grows as exp(−Ea / kT), where Ea is the activation energy, so retention time scales as t_ret ∝ exp(Ea / kT). Here k = 8.617e-5 eV/K and T is in kelvin. The acceleration between two temperatures is

> AF = t_ret(T_cold) / t_ret(T_hot) = exp[(Ea/k) · (1/T_cold − 1/T_hot)]

Example for Ea = 0.6 eV, 25 → 65 °C: 1/298.15 − 1/338.15 = 3.97e-4 K⁻¹; (0.6 / 8.617e-5) × 3.97e-4 = 2.76; AF = e^2.76 = **15.8x**.

| Ea | Likely mechanism | 25→45 °C | 45→65 °C | 25→65 °C | Retention halves every |
|---|---|---|---|---|---|
| 0.35 eV | trap-assisted leakage, typical of **tail** cells [REPORTED in patents] | 2.35x | 2.13x | 5.0x | ~17 °C |
| 0.6 eV | thermal generation in the junction, ~half the silicon band gap | 4.34x | 3.65x | 15.8x | ~10 °C |
| 1.1 eV | diffusion current, ~the band gap | 14.8x | 10.7x | 158x | ~5.5 °C |

Patents report ~0.35 eV for tail bits and ~0.6-0.7 eV for normal bits [REPORTED, S29]. The study's cell model uses "retention halves every ~10 °C" ([dram_cell_physics.py](../models/dram_cell_physics.py), `RET_HALVING_C`). **Your fitted Ea tells you which mechanism rules your chip's tail.**

### 2.3 The tail, and why a code buys so much

**The retention tail.** Let F(t) be the fraction of cells that fail when refresh is withheld for time t. The study fits a lognormal tail (the logarithm of retention time follows a bell curve) through two published anchors at 85 °C: F(32 ms) = 1.1e-10 and F(64 ms) = 3.6e-9. These derive from RAIDR-era counts of "~30 cells below 128 ms and ~1,000 cells below 256 ms in 32 GB" [REPORTED, S25], moved to 85 °C ([raw-ber-contract.py](../models/raw-ber-contract.py) section 5). That fit has a median of ~82 s at 85 °C and a log-width sigma of 1.24. I apply "halves every 10 °C" to reach your temperatures.

**The code.** A code that corrects t errors per n-bit codeword fails only when more than t cells in one codeword are wrong. For independent errors with per-bit probability p:

> P_UE ≈ (n·p)^(t+1) / (t+1)!

The exponent t+1 is the whole story. Halve p and SEC-DED (single-error-correct, double-error-detect; t = 1) gets 4x safer; a BCH code (Bose-Chaudhuri-Hocquenghem) with t = 12 gets 8,192x safer. The tail is steep too: F grows roughly as t^3 to t^5 in the region of interest. So a modest code buys a large factor in refresh interval.

**Worked example: SEC-DED (72,64) at 45 °C, target 1** (target 1 = at most 1e-15 uncorrectable events per data bit-hour, with a scrub, a pass that reads and corrects all memory, every hour). Target 1 is my illustrative assumption [ESTIMATE], not an industry spec. 1e-15 per bit-hour is about 1,100 FIT per Gbit (FIT = failures per billion device-hours), roughly 5 uncorrectable events per year for a 64 GB server, which is lax. Target 2 (the dossier's, below) is the one that matters.
- Per codeword per hour: 1e-15 × 64 bits × 1 h = 6.4e-14.
- C(72,2) · p² ≤ 6.4e-14 → 2,556 · p² ≤ 6.4e-14 → p ≤ 5.0e-9.
- Variable retention time adds new weak cells: multiply by (1 + 1/day × 1 h / 24 h) = 1.042, so the tail fraction allowed is F ≤ 4.8e-9.
- Invert the tail at 45 °C: median = 82 s × 2^4 = 1,310 s, so ln(median) = 7.18. Then z(4.8e-9) = −5.73 (z = how many standard deviations below the median; `norm_ppf` in the script), and ln t = 7.18 − 5.73 × 1.24 = 0.07, so **t = 1.08 s ≈ 17x the 64 ms window**. Under target 2 the same code gives only 0.27 s (4.1x).

**Target 2** is the study's tighter line: at most 2e-19 failures per 64-byte read (dossier section 2.1).

### 2.4 Expected results for a 64 Mbit SDR chip (67,108,864 cells)

**Expected failing cells** (ALL0 + ALL1 together; central estimate, with the band from 0.5x retention (DDR5-like) to 4x (older, larger cells); the band does not include the activation-energy uncertainty, which the second table below covers) [ESTIMATE]:

| Refresh withheld for | 25 °C | 45 °C | 65 °C |
|---|---|---|---|
| 64 ms | 0 | 0 | 0 |
| 0.512 s | 0 | 0 | ~6 [0-103] |
| 1.024 s | 0 | 0 [0-6] | ~103 [0-1,358] |
| 4.096 s | 0 [0-6] | ~103 [0-1,358] | ~13,000 [103-96,000] |
| 16.4 s | ~103 [0-1,358] | ~13,000 [103-96,000] | ~516,000 (F 0.8%) |
| 65.5 s | ~13,000 [103-96,000] | ~516,000 | ~6.5 million (F ~10%) |

- **First failing cell expected:** 25 °C at ~5.5 s [2.8-22 s] (about 0.85 s at 25 °C if the tail Ea is 0.35 eV); 45 °C at ~1.4 s; 65 °C at ~0.35 s.
- **q = 1e-4 reached** (the Oxide-Tail quantile): 25 °C at ~53 s; 45 °C at ~13 s; 65 °C at ~3.3 s.
- **Temperature sensitivity:** at a fixed wait, the failing fraction grows ~14x per +10 °C in this model. A study of 223 LPDDR4 (low-power DDR4) chips reports ~10x per 10 °C [REPORTED, S27].
- **Cross-check:** a DDR3 survey found fewer than 0.001% of cells below 3 s at 45 °C, even in the worst module [REPORTED, S26]. The model gives 4.4e-7 (0.000044%), consistent.
- **Cold-boot evidence.** Halderman et al. (2008) showed that DRAM keeps its contents for several seconds after power is cut, even at room temperature. Near −50 °C, fewer than 1% of bits decayed after 10 minutes [REPORTED, S22]. That is the long-retention majority, seen from the outside. Their chips were unpowered, which is a different condition from this experiment (powered, refresh withheld), so treat it as qualitative evidence that most cells hold for seconds, not as a calibration point [UNVERIFIED on the size of the difference]. Do **not** reproduce their cooling (canned-air sprays cause frostbite and the propellant is flammable).

**Expected ECC-safe refresh interval** (independent errors, VRT growth 1/day, scrub 1 h) [ESTIMATE]:

| Code | 25 °C | 45 °C | 65 °C (target 1) | 65 °C, dossier target 2 |
|---|---|---|---|---|
| SEC-DED (72,64), plain server ECC (columns 2-4 use the lax target 1) | 4.3 s (68x) | 1.1 s (17x) | 0.27 s (4.2x) | 0.066 s (1.0x) |
| BCH-4 (552,512) | 31 s | 7.6 s | 1.9 s (30x) | 0.88 s (14x) |
| BCH-12 (640,512) | 115 s | 29 s | 7.2 s (113x) | 4.8 s (75x) |
| RS-8 (80,64), a Reed-Solomon (RS) code over byte symbols, the dossier's chipkill code | 73 s | 18 s | 4.6 s (71x) | **2.7 s (42x; 21-169x from the retention band alone, 10-169x with the Ea uncertainty below)** |

- **Prediction for the gate:** RS-8 at 65 °C, target 2: about 42x with the study's halves-every-10 °C rule; about 33x with a true Arrhenius law at Ea = 0.6 eV; about 21x if the tail has Ea ≈ 0.35 eV (section 2.2). With the 0.5x-4x retention band on top, the plausible range is about 10x to 169x. PASS (≥24x) is the central expectation, PARTIAL is a real possibility, and NO-GO (<4x) is not expected [ESTIMATE].

**The temperature law matters as much as the retention scale** (`predict`, section D2; every model shares the same 85 °C anchor, so a lower Ea means less retention gained by cooling) [ESTIMATE]:

| Temperature law | RS-8, 65 °C, target 2 | SEC-DED, 45 °C, target 1 / target 2 | First failing cell, 25 °C | Failing bits at 25 °C after 65.5 s (ALL0 + ALL1) |
|---|---|---|---|---|
| Halves every 10 °C (study rule) | 42x | 17x / 4.1x | 5.5 s | ~13,000 |
| Arrhenius, Ea 0.6 eV | 33x | 12x / 3.0x | 4.3 s | ~28,000 |
| Arrhenius, Ea 0.35 eV (reported for tail cells) | 21x | 4.4x / 1.1x | 0.85 s | ~1.4 million |
| Lowest corner: Ea 0.35 eV and 0.5x retention | 10x | 2.2x / 0.5x | 0.42 s | ~4.8 million |

- **Consistency check:** the dossier gives 3.3 s for RS-8 (80,64) at 65 °C on its 640-bit line. This model gives 2.7 s from the same anchor; it counts every cell in its charged state (worst case), where the dossier assumed random data. (Since the 2026-11-04 correction, that 640-bit line is retired DDR4 only if the controller gives up 11.1% of capacity for check bits. On real DDR4 lines the dossier gives 2.8 s with two channels in lockstep and 1.0 s on one channel; dossier section 12.1.)
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
| A working measurement and analysis pipeline for tail statistics | Anything about oxide (IGZO, indium-gallium-zinc oxide) transistors. They are a different device; only the method transfers |
| Retention of an idle chip, no access traffic | That the chip is fine *in use* at the long interval. Real traffic activates neighbouring rows. Disturbance flips (RowHammer, RowPress; S41) grow with the refresh interval, because an aggressor row gets about 42x more activations per window at a 42x interval [ESTIMATE]. This rig never hammers; test that on the Arty A7 rowhammer-tester or DRAM Bender (scale-up steps 3-4) |
| A demo: "this idle chip holds its data refreshed every N seconds with code X" | That the 2e-19-per-read reliability target is met. One chip over a weekend reads about 1.3e8 64-byte lines (3 × 331 runs × 131,072 lines), about 3e-11 of the 5e18 reads needed to see one 2e-19 event [ESTIMATE] |

**How the result scales up**

| Step | Where | Cost | What it adds |
|---|---|---|---|
| 1. This experiment | Home | $115-200 | Method, pipeline, one SDR chip |
| 2. Same on 2-3 boards | Home | +$32-66 per board | First look at chip-to-chip spread |
| 3. DDR3 with real DDR command control: Arty A7-100T + Antmicro rowhammer-tester | Home or makerspace (needs the Vivado toolchain) | ~$299 board [REPORTED] | A 256 MB DDR3L part, a modern-ish node, open Python control |
| 4. DRAM Bender on DDR4 DIMMs (memory modules) with temperature and VPP control (VPP: the DRAM's wordline supply voltage) | University lab (CMU, ETH, Rutgers and Georgia Tech lineages run it) | ~$14k per station [ESTIMATE in dossier] | Real modules, many lots; this is the dossier's Phase 1 |
| 5. Dossier Phase 1: 150 DDR4 + 24 DDR5 modules, 1,000 h soaks, open DDR5 testers | Funded lab | ~$124k [ESTIMATE in dossier] | The actual GO/NO-GO |

---

## 4. Platforms, ranked for a software builder

Every claim is tagged. **[UNVERIFIED]** means I could not confirm it in this session.

| Rank | Platform | Memory | How you take refresh away | Approx. cost | Skills | Verdict |
|---|---|---|---|---|---|---|
| **1** | **STM32F429I-DISC1.** The order code must end in DISC1; the older STM32F429I-DISCO, also boxed as 32F429IDISCOVERY, has no virtual COM port [REPORTED, S6] | ISSI IS42S16400J, 64 Mbit SDR SDRAM (4 banks × 4,096 rows × 256 columns × 16 bit) on SDRAM bank 2 of the FMC (flexible memory controller) [REPORTED, S1-S2; confirmed in ST's board code, S42] | Relax: the controller's 13-bit refresh timer (COUNT ≥ 41) plus a slow clock gives up to a 4.19 s period. Pause: hold chip select high for any length [ESTIMATE from REPORTED register facts; below] | $32-66, in stock at Mouser and Digi-Key [REPORTED, S10, 2026-11-04]; Digi-Key lists a 99-week factory lead time | C, flashing | **Start here.** All code, no FPGA |
| 1b | STM32F746G-DISCO | 128 Mbit Micron MT48LC4M32B2 class, only 64 Mbit wired (16-bit bus) [REPORTED, S11] | Same FMC methods; check pins and bank | ~$56 [UNVERIFIED] | C | Good substitute; the firmware needs a port |
| **2** | **Sipeed Tang Nano 20K** | GW2AR-18 FPGA (field-programmable gate array) with 64 Mbit, 32-bit SDR SDRAM in the package [REPORTED, S12] | You write the controller, so you issue (or skip) every refresh | $25-38 [REPORTED, S12] | Verilog; open tools (yosys, nextpnr-himbaechel, openFPGALoader) [REPORTED] | Best second step: full command control, same chip class |
| 3 | ULX3S (Lattice ECP5) | 32 MB SDR SDRAM [REPORTED, S14] | Same as Tang Nano; open toolchain | $145-235 [REPORTED, S14] | Verilog | 4x more cells; pricier |
| 4 | Digilent Arty A7-100T + Antmicro rowhammer-tester | 256 MB DDR3L, 16-bit [REPORTED, S16] | LiteDRAM "payload executor" sends raw DDR commands through the PHY (the physical-layer interface to the memory); the playbook config has a `refresh` on/off key [REPORTED, S15] | $299 [REPORTED, S16] | Python + LiteX + Vivado | Real DDR3. Heavier toolchain; a makerspace-level step |
| 5 | A PC with ECC memory (AMD AM5 + ECC UDIMMs, unbuffered memory modules) | DDR5 ECC UDIMMs | Raise tREFI (the spacing between refresh commands) in the BIOS (max 65535 reported on AM5) and count corrected errors with Linux EDAC (the kernel's error detection and correction driver) [REPORTED/UNVERIFIED, S19-S20] | $0 if you own one | Linux, BIOS | Real ECC, but small range and DDR5's on-die ECC hides raw errors. See 14.4 |
| 6 | DRAM Bender / SoftMC | DDR3/DDR4 DIMMs (DRAM Bender lists Alveo U200-class and BittWare XUPS3S boards; temperature and VPP control) [REPORTED, S17-S18] | Full command control | Thousands of dollars per board [ESTIMATE] | FPGA lab | University-lab route (step 4 above) |

### 4.1 How to take refresh away on the STM32F429I-DISC1

The STM32's FMC issues refresh automatically, timed by SDCLK (the SDRAM clock). Four options:

| Method | How | Range | Status |
|---|---|---|---|
| **A: relax** (primary for ≤4 s) | Precharge all banks, then program the refresh timer so each row is refreshed only every P. Hold for 3 periods, then restore. This *is* the product scenario (relaxed refresh) | 21.5 ms to 4.19 s at SDCLK 8 MHz; to 6.29 s at SDCLK 5.33 MHz | **Supported.** COUNT is a 13-bit field [ST CMSIS header, S43] and RM0090 asks for COUNT ≥ 41 [REPORTED, S3]. The firmware stays in 41-8191 and reads every value back (else `ERR,refresh count readback`). One caution: ST's STM32H7 manual says the register "must not be reprogrammed after the initialization procedure to avoid modifying the refresh rate" [REPORTED, S3; F4 wording UNVERIFIED]. Changing the rate is the point here; the A-vs-B overlap check below tests that it works. RM0090 also forbids COUNT = TWR + TRP + TRC + TRCD + 4 cycles [REPORTED, S52]; with the unused bank 1's reset timings that sum is 45 [ESTIMATE], so the firmware never writes 45 (a 24 ms wait runs at COUNT 46, 24.1 ms) |
| **B: pause** (primary for >4 s; fallback) | Issue precharge-all, then switch the chip-select pin (SDNE1, PB6) from FMC to a plain GPIO (general-purpose input/output) output held high. With chip select high the SDRAM ignores every command, including refresh. Give the pin back afterwards | Unlimited | **Supported, with one assumption.** PB6 = SDNE1 is confirmed in ST's board code and in Zephyr's board file [S42, S44]. "CS high = COMMAND INHIBIT: no new command is executed; operations in progress are not affected" is in ISSI's truth table for this chip family [REPORTED, S45]. Handing an FMC pin to a GPIO mid-run is not an ST-documented use [UNVERIFIED], so the firmware checks that PB6 really is a high GPIO during the pause and back on the FMC afterwards (else `ERR,sdne1 pin` and the run is dropped). The chip's row counter stops during the pause and resumes where it left off, so every row goes unrefreshed for the pause plus one normal window: a fixed +54 ms, not an uncertainty. The firmware reports that true interval [ESTIMATE] |
| Z: COUNT = 0 | Precharge all, then write 0 to the timer | Unlimited | **EXPERIMENTAL.** ST's STM32**H7** register text says "If the value programmed in the register is 0, no refresh is carried out" [REPORTED, S3]. RM0090 asks for COUNT ≥ 41, so 0 is outside the documented F4 range. Off by default (`-DENABLE_METHOD_Z`); validate against method B before you trust it |
| Not usable: self-refresh | The FMC can put the chip in self-refresh | - | In self-refresh **the chip refreshes itself** and may stay there indefinitely [REPORTED, S31] |
| Not usable: power-down | FMC command mode 110 | - | The chip does no refresh in power-down and must not stay longer than its refresh period [REPORTED, S31]. Whether the FMC wakes it to refresh is [UNVERIFIED] |

**The arithmetic for method A.** The full-array refresh period is rows × (COUNT + 1) / f_SDCLK. The firmware runs the core at 16 MHz from the board's 8 MHz crystal (HSE) through the PLL (the clock multiplier): ÷4, ×64, ÷8. If the crystal does not start it stays on the internal 16 MHz oscillator (HSI). Either way SDCLK (the SDRAM clock) = HCLK (the CPU bus clock) / 2 = 8 MHz:
- Normal rate (ST's formula, with a 20-cycle margin, "(15.62 us x Freq) - 20" in ST's board code, S42): COUNT = (64 ms / 4,096) × 8 MHz − 20 = 125 − 20 = **105**, giving a 54 ms full window.
- To test 64 ms exactly: COUNT = 0.064 × 8e6 / 4,096 − 1 = **124**.
- Longest: 4,096 × 8,192 / 8e6 = **4.19 s**. With SDCLK = HCLK/3 (5.33 MHz): 6.29 s.
- The slow clock is deliberate. At ST's usual 90 MHz SDCLK the longest period would be only 4,096 × 8,192 / 90e6 = 0.37 s.

**Overlap check.** Method B rests on the pin hand-over, which ST does not document, and it covers every wait above 4 s, which is nearly all of the 25 °C data. So check it against method A where both work and enough bits fail: 2.048 and 4.096 s at 65 °C (about 1,400 and 13,000 failing bits expected; at 1 s or at 25 °C too few cells fail to judge). Section 8 step 10 has the commands. The two must agree within 2x (section 11). They differ slightly by design: method A gives each cell three relaxed periods (so VRT cells get three chances to fail), and method B's interval is 54 ms longer.

---

## 5. Parts and tools

| Part | Spec that matters | Example part number | Approx. USD (Nov 2026) | Where |
|---|---|---|---|---|
| STM32F429I-DISC1 board | IS42S16400J SDRAM on FMC bank 2 [ST board code, S42]; ST-LINK/V2-B with a VCP (virtual COM port: a USB serial link through the on-board programmer) on USART1, pins PA9/PA10, through solder bridges SB11 and SB15, which are closed on a DISC1 as shipped [REPORTED, S6-S7, S44]. **Check the order code on the sticker before you buy, especially second-hand.** A board marked STM32F429I-DISCO has no VCP; then the USB-UART adapter below is REQUIRED | STM32F429I-DISC1 (Mouser 511-STM32F429I-DISC1; Digi-Key 497-16140-ND) | 32-66: Mouser $31.56 with 559 in stock (undated aggregator listing); Digi-Key $45.92 with 648 in stock (aggregator, 2026-06-21); TME $45.61 [REPORTED, S10, searched 2026-11-04] | Mouser, Digi-Key, TME, Newark |
| USB cable | USB Type-A to **Mini-B**: the ST-LINK connector is Mini-B [REPORTED, S47]. The board's second, micro-AB socket is the user USB port, not the programmer | any | ~5 [ESTIMATE] | any |
| Thermocouple amplifier | MAX31855, K-type, 0.25 °C steps, SPI (serial peripheral interface), 3.3 V; accuracy about ±2 °C [UNVERIFIED] (datasheet, from memory) | Adafruit 269 | 14.95 at Adafruit; Mouser showed 339 in stock; some resellers sold out [REPORTED, S33, searched 2026-11-04] | Adafruit, Mouser, Digi-Key |
| K-type thermocouple | Glass-braid insulation, rated to 500 °C, 1 m | Adafruit 270 | 9.95 at Adafruit (8.96 each for 10+) [REPORTED, S36, searched 2026-11-04] | Adafruit, Digi-Key, Mouser |
| **Heater** | 12 V DC heater, about 15 W, polyimide (Kapton) film or silicone rubber, rated ≥150 °C, with leads, no bigger than about 100 × 100 mm so it fits beside the board. The listing must state the maximum temperature | Thermo Technologies 3616108 (12 V, 15 W, 90 mm round, self-adhesive polyimide, IPX4; Rapid Online order code 07-7003) [REPORTED, S38], or a generic "12 V 15 W polyimide heater" listing. Conrad's 1594187 listing names 140 mm, too big for this box: check the size before you buy | £19.46 ex VAT at Rapid (UK), in stock [REPORTED, S38, searched 2026-11-04]; generic listings ~5-25 [ESTIMATE]. No US distributor listing of this exact part was found | Rapid (UK), RS, Omega (US, KHLVA series), marketplaces |
| Heater, alternative | Adafruit 4308: a 14 × 5 cm stainless-steel-fibre heating fabric, 5-12 V DC, no published temperature rating. About 8 Ω: about 0.6 A / 3 W at 5 V [REPORTED, S34] and about 1.4 A / 17 W at 12 V [ESTIMATE]. 3 W cannot heat the box (it loses about 8-11 W at 65 °C [ESTIMATE]), so it must run near 12 V. Measure its resistance R with the multimeter: power at 12 V = 144 / R watts. If that is above about 15 W, run it lower (buck converter). Never fold it; keep it flat on the tile under Kapton tape. **Do not buy Adafruit 1481: it is 5 V only** | Adafruit 4308 only | ~8 [REPORTED, S34] | Adafruit, Pi Hut, Core Electronics |
| Adjustable buck converter (recommended) | DC-DC step-down module, 12 V in, 3-12 V out, ≥2 A. Lets you turn the heater power down until the stuck-on test passes (power scales as V²) | LM2596-type module | 1.60-6: Addicore $2.48; eBay $1.59 plus shipping [REPORTED, S49, searched 2026-11-04] | Addicore, marketplaces |
| Thermostat | 12 V DC, NTC probe (negative-temperature-coefficient thermistor), -50 to 110 °C, relay. **Must be set to heating mode, P0 = H** (step 8a) | XH-W1209 | 4-9: eBay $6.83-8.92; Tinytronics €4.00 [REPORTED, S48, searched 2026-11-04] | Many hobby stores |
| 12 V DC power adapter | Certified (UL/CE), ≥2 A, 5.5 × 2.1 mm barrel plug | any | ~10 [ESTIMATE] | any |
| DC barrel jack to screw terminals | Female, 5.5 × 2.1 mm | any | ~2 [ESTIMATE] | any |
| Inline fuse holder + fuses | 2 A fast-blow, for the 12 V line | any | ~3 [ESTIMATE] | any |
| Hook-up wire and connectors | Stranded, 22 AWG (0.33 mm²) or thicker; crimp connectors or screw terminal blocks | any | ~3-5 [ESTIMATE] | any |
| **Bimetal thermal switch (air cut-out)** | Normally closed, opens at 80 °C, resets when cool, ≥2 A | KSD301 type, 80 °C N.C. | 3.50-8: Walmart (uxcell) $7.99 for one; Newegg Business $6.99 for two; LCSC $0.33 in bulk [REPORTED, S48, searched 2026-11-04] | Walmart, Newegg, LCSC, marketplaces |
| **Thermal fuse (heater fuse)** | One-shot, axial, ≥2 A (a 10 A / 250 V AC rating is fine at 12 V DC). Opening temperature Tf chosen in step 8d: about 25 °C above the heater's highest measured temperature, not below 110 °C, not above the heater's rating | assorted thermal-fuse kit (typical values 70-240 °C) [UNVERIFIED part], or one fuse of the right rating from a distributor | ~3-6 per marketplace kit [ESTIMATE]; single distributor parts about A$3.54 each (element14, a 240 °C example) [REPORTED, S49]. Distributor assortments cost far more (Bürklin 90-piece, €147) [REPORTED, S49] | electronics stores, marketplaces |
| Insulated box | Small expanded-polystyrene (EPS) foam box, ~20 × 15 × 10 cm, walls 1.5-2.5 cm | any | ~5-10 [ESTIMATE] | Craft or packaging store |
| Ceramic tiles | One ≥15 × 15 cm inside the box for the heater and board; a second tile or ceramic spacers to lift it off the foam floor | any | ~2-4 [ESTIMATE] | Hardware store |
| Kapton (polyimide) tape | Holds the probes and covers the heater; heat-safe | any | ~6 [ESTIMATE] | any |
| Nylon standoffs, jumper wires | M3 standoffs 25-30 mm tall; female-female jumpers for the MAX31855 | any | ~6 [ESTIMATE] | any |
| USB-UART adapter | 3.3 V logic (CP2102 or FT232). Optional on a DISC1; **required on an old DISCO**: adapter TX → PA10, adapter RX → PA9, GND → GND | any | ~8 [ESTIMATE] | any |
| Optional: logic analyser | 8-channel, 24 MS/s USB type (or a logic probe). Confirms that refresh really stops in method B (section 13) | any | ~10-15 [ESTIMATE] | any |

Prices in this table are search-result snapshots of 2026-11-04, without shipping or tax; check stock before you order.

**Tools.** Soldering iron for 8 header pins. Multimeter. Small screwdriver; crimp tool or pliers. Safety glasses. A cup of ice water (thermocouple check). Computer with Python 3, numpy and pyserial. Arm GNU toolchain (`arm-none-eabi-gcc`). A flasher: open-source `stlink` (`st-flash`) or STM32CubeProgrammer. STM32CubeIDE (free) for ST's example (step 3) and the fallback (step 5b).

---

## 6. Safety

> **SAFETY BOX: E6**
> - **Electrical.** Low voltage only. The board runs from USB 5 V. The heater runs from a certified 12 V DC adapter through an inline 2 A fuse and the W1209 relay. **Never** build or open anything that touches mains voltage. Power the heater from its own adapter, never from the board's USB. Use only a heater rated for 12 V. A 5 V-only pad (for example Adafruit 1481) on the 12 V adapter takes about 6x its rated power (12² / 5² = 5.8) and can overheat.
> - **Heat and fire. Hard limit: 75 °C box air.** Four independent layers, all required:
>   1. *Power limit (the stuck-on test, step 8d).* Before the first heated run, prove that the heater, left fully on with no thermostat, cannot push the box air above 75 °C. Then a stuck relay or a probe that falls off (it reads cold and keeps heating) cannot cause a fire.
>   2. *Thermostat in heating mode.* The W1209 must be set to P0 = H (heating: relay ON below the setpoint). Its factory default is C (cooling: relay ON *above* the setpoint), which runs a heater away [REPORTED, S35]. Set its over-temperature cut (P6, or P7 on some firmware) to 72 °C (step 8a).
>   3. *Air cut-out.* A normally-closed 80 °C bimetal switch (KSD301 type) in series with the heater, in the box air at board height, 2-3 cm from the SDRAM, never on the heater. It opens if the box air runs away and closes again when it cools.
>   4. *Heater fuse.* A one-shot thermal fuse taped to the heater, rated about 25 °C above the heater's highest temperature in the stuck-on test, and not below 110 °C. The heater runs about 40-60 °C hotter than the box air while heating [ESTIMATE: 10-15 W over a ~0.02 m² tile], so a fuse rated near the air temperature would open on every heat-up. Do not put a one-shot fuse in the 65 °C air either: such fuses are rated to hold for long periods only at their "holding temperature", well below their opening temperature, and may open anywhere in between [REPORTED, S39]. An opened fuse or a clicking cut-out means something went wrong: find out why, and replace a fuse only with the same rating. **Never bridge a fuse or a cut-out.**
> - **Attended heating only.** Run the heated blocks (45 and 65 °C) only while an adult is at home and awake. Look at the box and the W1209 display every 30-60 minutes. Never heat overnight or while you are out. The unheated 25 °C block may run overnight. Keep children and pets away from the box, the adapter and the cables. Stand the box on a hard, non-flammable surface (tile, stone or metal tray), away from curtains and paper. Keep a smoke alarm in the same room and the 12 V plug within reach. Unplug the heater when you are not running.
> - **Foam and placement.** EPS foam softens near 100 °C and is not meant for long use above about 75-80 °C [UNVERIFIED]. Inside the box, raise the heater tile off the foam floor on a second tile or ceramic spacers, so the hot spot does not sit on the foam. Keep the W1209 module, the buck converter, the inline fuse and the 12 V adapter OUTSIDE the box. Only the W1209 probe, the heater, the two cut-outs, the board and the thermocouple go inside.
> - **Burns.** Metal at about 65 °C can burn skin within seconds of contact, and the heater runs hotter than the box [REPORTED, S40; the ISO 13732-1 tables themselves were not read]. Let the box cool before handling the board.
> - **Component ratings.** The SDRAM part with the "-7TL" suffix is most likely commercial grade, 0-70 °C (a sister "-5TL" part lists 70 °C max; the "-7TLI" industrial part is rated -40 to 85 °C [REPORTED, S9]; one distributor claims 0-85 °C for -7TL [REPORTED, conflicting]). The board's LCD (liquid-crystal display) is likely rated to about 70 °C as well [UNVERIFIED]. Stay at 65 °C on the chip.
> - **Soldering.** The iron tip is about 350 °C: keep it in its stand, and unplug it when you are done. Work with a window open or a small fan pulling the flux smoke away from your face. Wear safety glasses when you clip leads. If your solder contains lead, wash your hands afterwards and do not eat at the bench.
> - **Static.** Touch a grounded metal object before handling the board. Hold it by the edges.
> - **Chemicals.** None needed. If you clean flux with isopropyl alcohol: it is flammable (see its SDS, the safety data sheet), so use it only with the heater unplugged and cold, in a ventilated room, and store it closed.
> - **Not at home.** Do not cool chips with sprays or liquid nitrogen to repeat the cold-boot result. Do not change refresh settings on a PC that holds data you need. For the PC route (14.4), do not add heaters inside a PC case.

---

## 7. Build

1. **Buy the parts** in section 5. Check that the board's order code ends in DISC1. Read the SDRAM marking on your board with a magnifier and write it down.
2. **Install the tools.**
   - Linux (Debian/Ubuntu): `sudo apt install gcc-arm-none-eabi binutils-arm-none-eabi make stlink-tools python3-numpy python3-serial`. Then `sudo usermod -aG dialout $USER`, and log out and back in (this lets you open the serial port). On Ubuntu 24.04 this installs arm-none-eabi-gcc 13.2.1 (package `15:13.2.rel1-2`), the exact compiler that built this firmware (section 16). The firmware uses no C library, so the C library package that apt suggests (`libnewlib-arm-none-eabi`) is optional.
   - macOS: `brew install --cask gcc-arm-embedded`, `brew install stlink`, then `python3 -m pip install numpy pyserial`.
   - Windows: install the Arm GNU Toolchain, STM32CubeProgrammer, and `make` through MSYS2; then `python -m pip install numpy pyserial`. You will flash with `STM32_Programmer_CLI -c port=SWD -w e6_retention.bin 0x08000000`.
   - All: install STM32CubeIDE (free) for ST's own SDRAM test (section 7.1, step B) and for the fallback in step 5b. Also install `git`.
3. **Prove the board's SDRAM works before you run any of this code.** Section 7.1 has the full first-power-on checklist. In short:
   - *Zero-tool check:* power the board as it came. The factory demo uses the SDRAM as the LCD frame buffer (ST's board-support package, BSP, sets `LCD_FRAME_BUFFER` = 0xD0000000 in stm32f429i_discovery_lcd.h:93 [S42]). Clean demo graphics mean the SDRAM is alive. Flashing anything erases the demo.
   - *ST's own test:* ST's example `Projects/STM32F429I-Discovery/Examples/FMC/FMC_SDRAM` in STM32CubeF4 (path confirmed, S42). Its readme says "If the data is read correctly from SDRAM, the LED3 is on, otherwise the LED4 is on" (readme.txt:50). If LED4 lights, the board is faulty and nothing else here will work.
4. **The register check is done. Repeat it only if you change the firmware.** On 2026-11-04 the firmware was compared with ST's own code from GitHub (commits in section 16): every address, bit field and value in `regs_f429.h`; the 38 SDRAM pins with alternate function 12 (AF12, which hands a pin to the FMC), PB6 = SDNE1 and PB5 = SDCKE1; the SDRAM timings, command sequence, mode register 0x0230 and refresh count in `sdram_fmc.c`; the USART1 pins (PA9/PA10, AF7) and baud divider in `uart.c`; the clock settings in `main.c`; and the memory sizes in the linker script. Result: 127 checks, all OK: 95 numbers compiled from both headers, 30 checks against ST's board code and HAL, and 2 memory-map checks. Each verified line in the code cites the ST file and line. Three values differ from ST's board code on purpose, each explained in `sdram_fmc.c`: write recovery TWR = 3 cycles (ST: 2), 8 power-up auto-refreshes (ST: 4) and a 100 ms power-up wait (ST's board code: 1 ms; ST's example: 100 ms). To repeat the check (needs git, Python 3 and the ARM compiler), from the `dram-moonshot` folder:

   ```
   mkdir st && cd st
   git clone --depth 1 --filter=blob:none --sparse https://github.com/STMicroelectronics/STM32CubeF4 cubef4
   git -C cubef4 sparse-checkout set Drivers/CMSIS/Include Projects/STM32F429I-Discovery/Examples/FMC Projects/STM32F429I-Discovery/Examples/UART/UART_TwoBoards_ComPolling
   git clone --depth 1 https://github.com/STMicroelectronics/cmsis-device-f4
   git clone --depth 1 https://github.com/STMicroelectronics/stm32f4xx_hal_driver hal
   git clone --depth 1 https://github.com/STMicroelectronics/32f429idiscovery-bsp bsp
   cd ..
   python3 home-lab/tools/e6_regcheck.py --cubef4 st/cubef4 --cmsis-device st/cmsis-device-f4 --hal st/hal --bsp st/bsp
   ```

   Expect `== RESULT: ALL OK (0 mismatches)`. Not checked against a document: ST's reference manual (RM0090) and board manual (UM1670) themselves, which could not be downloaded in this session; their key facts come from ST's code, Zephyr's board file and search snippets instead (section 16).
5. **Build and flash.** In `code/T3_dram/stm32_retention/`:
   - `make` builds `e6_retention.elf` and `e6_retention.bin` and prints their size. With arm-none-eabi-gcc 13.2.1 expect `text 5780, data 8, bss 12`: about 5.8 KB of the 2 MB flash and 20 bytes of static RAM, plus about 0.3 KB of stack [ESTIMATE from gcc's stack-usage report, section 16]. Other compiler versions give slightly different numbers. If the compiler is not on your PATH: `make CROSS=/path/to/bin/arm-none-eabi-`.
   - `make flash` writes it with `st-flash --reset write e6_retention.bin 0x08000000` and restarts the board (Windows: the `STM32_Programmer_CLI` command in step 2, then press the black reset button).
   - `make syntax` is a quick check with your PC's own gcc; it needs no ARM compiler.

   **5b. Fallback if init fails.** If you see `ERR,sdram init failed` and cannot find the cause in an evening: create an STM32CubeIDE project for this board. Keep the clock on HSI 16 MHz (no PLL). Call `BSP_SDRAM_Init()`, which runs SDCLK at HCLK/2 = 8 MHz (stm32f429i_discovery_sdram.h:81). Then, at once, write the refresh count yourself: `FMC_Bank5_6->SDRTR = 105 << 1;`. The BSP keeps its SDRAM handle private (`static`, stm32f429i_discovery_sdram.c:59), so `HAL_SDRAM_ProgramRefreshRate` cannot reach it. The BSP's own count, 1386 (stm32f429i_discovery_sdram.h:97), is meant for 90 MHz; at 8 MHz it would refresh the array only every 4,096 × 1,387 / 8 MHz = 0.71 s [ESTIMATE], far too slowly. Then paste in `run_test()` and the command parser from `main.c`, plus `patterns.c`, `uart.c`, `max31855.c`, and `sdram_fmc.c` without its `sdram_init()`.
6. **Talk to it.** The board talks over a UART (universal asynchronous receiver-transmitter; the STM32 calls its own a USART) at 115200 baud, 8N1 (eight data bits, no parity, one stop bit).
   - From here on, run every Python command from `code/T3_dram/`, where `capture_retention.py` and `retention_map.py` live (`cd ..` from the firmware folder).
   - Find the port: `python3 -m serial.tools.list_ports` (Linux /dev/ttyACM0, macOS /dev/cu.usbmodem…, Windows COMn).
   - Open it: `python3 -m serial.tools.miniterm <port> 115200` (Ctrl+] quits).
   - Press reset: you should see `SELFTEST,OK`, then `HELLO,e6-ret-0.5,IS42S16400J,4194304,16,8000000,A|B|C,HSE`. The last field says which clock runs: `HSE` is the board's crystal; `HSI` means the crystal did not start and the firmware fell back to the internal oscillator (it still works; see section 13 if text is garbled when hot). Type `PING`: expect `PONG`. Type `SELFTEST` at any time to repeat the SDRAM bus test (it overwrites the SDRAM, which is fine between runs).
   - Close the terminal before you run `capture_retention.py`. If nothing arrives, see section 13.
7. **Fit the thermometer.**
   - Solder the MAX31855 header (Soldering, section 6). Wire VIN→3V3, GND→GND, CLK→PE2, CS→PE3, DO→PE4. ST's board code uses port E only for the SDRAM (PE0, PE1, PE7-PE15) and one user reports PE2-PE5 free [S42; REPORTED, S32]; UM1670's free-pin table itself was not checked [UNVERIFIED].
   - Check it in a cup of ice water first: stir, wait a minute, type `TEMP`. It should read 0 ± 2 °C. Log the offset. Because the MAX31855 is only good to about ±2 °C, the ±1 °C checks in section 11 test stability, not absolute accuracy.
   - Check which side of your board the SDRAM chip is on (UM1670 board layout drawing). Tape the thermocouple tip flat on top of the SDRAM package with Kapton tape. Type `TEMP`: expect room temperature.
8. **Build the thermal box.** Do 8a to 8d in order, and stay with the box whenever the heater is powered.

   **8a. Program the W1209 BEFORE you connect the heater.** Power it from the 12 V adapter alone.
   - Hold SET for about 5 s to open the menu. Set P0 = H (heating: relay ON below the setpoint). The factory default is C (cooling), which would run a heater away.
   - P1 = 0.5 (hysteresis, °C). P2 = 70 (the highest setpoint the buttons can choose). P6 = 72 (over-temperature cut: relay forced OFF above 72 °C). On some firmware this is P7, so check the sheet that came with your module [REPORTED, S35].
   - Test it with NO heater connected: (1) set the setpoint 5 °C above room temperature; the relay must click ON and its LED light. (2) Warm the probe between your fingers past the setpoint; the relay must click OFF. (3) Set P6 to 30 for a moment and warm the probe; the display must show the alarm (`---` or `HHH`) with the relay OFF. Set P6 back to 72.

   **8b. Lay out the box.**
   - Stand the box on a hard, non-flammable surface. Inside, put the spacer tile (or ceramic spacers) on the floor and the main tile on top.
   - Put the heater on the main tile beside, not under, where the board's header rows will be. Cover it with a strip of Kapton tape.
   - Mount the board on 25-30 mm nylon standoffs on the tile. Keep every pin, jumper, probe and cable at least 2 cm from the heater.
   - Keep the heater at least 2 cm from every foam wall and from the lid. EPS foam is rated only to about 75 °C, and the heater runs 40-60 °C hotter than the box air (the same 20 mm rule as [E4](E4_femtoamp_leakage_bench.md#6-safety) and [SAFETY.md](SAFETY.md#3-heaters-and-thermal-runaway)).
   - Tape the W1209 probe on the SDRAM side of the board, next to the chip, with Kapton over the probe's metal tip so it cannot touch any pins.
   - Fix the KSD301 bimetal switch in the air at board height, 2-3 cm from the SDRAM, not touching the heater.
   - Bring the USB cable and the heater leads out through one small slot.

   **8c. Wire the heater circuit.** Use stranded 22 AWG wire or thicker, with screw terminals or crimp connectors.
   1. Plug the 12 V adapter into the female barrel jack with screw terminals.
   2. +12 V goes to the inline fuse holder with a 2 A fast fuse.
   3. After the fuse, split into two wires: one to the W1209 "+12V" terminal, one to the relay COM terminal (K0 on most boards; check yours [UNVERIFIED]).
   4. Relay NO terminal (K1) → bimetal switch → heater fuse → heater lead 1. Until 8d gives you the fuse rating, connect the bimetal switch straight to heater lead 1, and power the heater only while you watch it.
   5. Heater lead 2 → adapter −. W1209 GND → adapter −.
   6. Crimp the thermal fuse. If you must solder it, solder at least 10 mm from its body while you grip the lead with pliers as a heat sink: heat from the iron can open it.
   7. The W1209 module, the inline fuse, the buck converter (if used) and the adapter stay OUTSIDE the box.
   8. Before you plug in, check with the multimeter that +12 V and − are not shorted.
   - *If 8d tells you to lower the heater power:* put the buck converter between the inline fuse and the relay: fuse → buck IN+, buck OUT+ → relay COM, buck IN− and OUT− → adapter −. Set its output voltage with the multimeter BEFORE you connect the heater. The W1209's own "+12V" stays on the unregulated 12 V.

   **8d. Stuck-on test (attended, before any heated run).**
   - Bypass the thermostat: take the COM and NO wires out of the relay terminals and join them in a screw terminal block, so the heater is fully on through the bimetal switch. Leave the heater fuse out for now.
   - Tape the thermocouple to the heater, with a layer of Kapton under its tip. Close the box with the board inside and powered. Read the heater temperature by typing `TEMP` in the serial terminal, and the box air on the W1209 display.
   - Log both temperatures every 10 minutes (section 9) until both stop rising, about 1-2 h [ESTIMATE].
   - **Unplug at once** if the box air passes 75 °C, the heater passes its rating minus 25 °C (125 °C for a 150 °C heater), or the bimetal switch clicks open.
   - **PASS** if the air settles at or below 75 °C and the heater at or below its rating minus 25 °C. The equilibrium moves up one-for-one with room temperature: if your room will be warmer than during the test, add the difference.
   - **Too hot:** lower the heater power with the buck converter and repeat. Power scales as V²: 12 → 10 V gives 0.69x, 12 → 9 V gives 0.56x.
   - **Too weak:** if the air settles below about 68 °C, the heater cannot hold 65 °C with margin. Close gaps, use a thicker box, or use a stronger heater.
   - Then choose the heater fuse: Tf about 25 °C above the highest heater temperature you logged, not below 110 °C, not above the heater's rating. Fit it (wiring item 6). Put the COM and NO wires back on the relay. Move the thermocouple back onto the SDRAM.
   - Finally, set the W1209 to 65 °C and watch one full heat-up and a 30-minute hold. The relay should cycle and the reading should stay within about ±1 °C.
9. **Smoke test at room temperature,** with the heater unplugged and the lid ajar:
   `python3 capture_retention.py --port /dev/ttyACM0 --temp-c 25 --repeats 1 --waits 0.064 1.024 16.384 65.536 --out smoke.log`
   (use the chip temperature that `TEMP` reports for `--temp-c`.) Expect a clean control run and zero failures at 64 ms. At 1 s expect 0, though a handful is possible if your chip's tail has a low activation energy. At 65.5 s expect roughly 100 to 100,000 failing bits over ALL0 + ALL1 together (central about 13,000, so about 6,500 each, a BER of about 1e-4; BER = bit error rate, failing bits ÷ all bits). With a 0.35 eV tail it could be about 1.4 million [ESTIMATE, section 2.4]. One of ALL0/ALL1 may show almost none if your chip is mostly true cells or mostly anti cells (section 8). A closed box self-heats a few °C, and that alone can double the count. Any non-zero count at 65.5 s shows that refresh really stopped.
10. **Dry run without hardware** at any time: `python3 capture_retention.py --simulate --temp-c 45 --out sim.log`, then `python3 retention_map.py analyze sim.log`. The report says **SYNTHETIC DATA** at the top: its numbers come from a made-up chip and test only the pipeline. With one temperature, section 8 of the report prints NO VERDICT for the 65 °C gate; that is expected.

### 7.1 First power-on checklist

Do these in order, at room temperature, with the heater unplugged. Stop at the first step that fails and use its last column. Steps A-B use only ST's code; C-G use this firmware.

| Step | Do | Pass looks like | If it fails |
|---|---|---|---|
| A. Board alive | Plug a Mini-B data cable into the ST-LINK socket. Watch the factory demo | Demo graphics on the LCD. On Linux, `ls /dev/ttyACM*` shows a port | Try another cable and USB port: a charge-only cable has no data wires |
| B. ST's SDRAM example | Get STM32CubeF4 with its driver submodules: `git clone --recursive --depth 1 --shallow-submodules https://github.com/STMicroelectronics/STM32CubeF4` (several hundred MB with all submodules [ESTIMATE]; or ST's zip package). In STM32CubeIDE, import the existing project in `Projects/STM32F429I-Discovery/Examples/FMC/FMC_SDRAM/STM32CubeIDE` from inside that clone (File > Import > Existing Projects into Workspace [UNVERIFIED menu path]). Build it, then Run it (STM32CubeIDE flashes through the ST-LINK) | LED3 (PG13) on, LED4 (PG14) off. ST's readme: "If the data is read correctly from SDRAM, the LED3 is on, otherwise the LED4 is on" (readme.txt:50) | LED4 on: the SDRAM or its wiring is faulty; stop here. Nothing lit: the example did not run; read the build and debug console. The project links its drivers six folders up (`PARENT-6-PROJECT_LOC/Drivers/...` in its `.project`), so it builds only inside the full clone |
| C. Flash this firmware | `cd code/T3_dram/stm32_retention && make && make flash` | `make` prints the size table (text about 5,900 bytes); `st-flash` reports the flash written and verified | `st-flash` finds no board: end any STM32CubeIDE debug session, replug, run `st-info --probe` |
| D. First words | `python3 -m serial.tools.miniterm /dev/ttyACM0 115200`, then press the black reset button | `SELFTEST,OK`, then `HELLO,e6-ret-0.5,IS42S16400J,4194304,16,8000000,A\|B\|C,HSE` | Nothing at all: section 13, "No HELLO". `ERR,sdram init failed,step N` or `ERR,sdram selftest,...`: section 13. `HSI` at the end instead of `HSE`: it works; read the "garbled when hot" row of section 13 |
| E. Commands | Type `PING`, `TEMP`, `SELFTEST` | `PONG`; `TEMP,0,now,nan` with no thermocouple fitted (room temperature once fitted); `SELFTEST,OK` | `ERR,unknown command` for every line: the terminal sends something other than CR or LF line endings |
| F. One control run | Close miniterm. From `code/T3_dram/`: `python3 capture_retention.py --port /dev/ttyACM0 --temp-c 25 --repeats 1 --patterns ALL0 ALL1 --waits 0.064 --out first.log` | The control run gives BER 0 and prints the measured write+read time; both 64 ms runs give BER 0 | Section 13: "Control run fails", or "Board stops answering" for a TIMEOUT |
| G. Smoke test | Step 9 above (waits up to 65.5 s) | Failing bits at 65.5 s, none at 64 ms | Section 13: "Nothing fails even at 65 s" |

The same binary already passed steps D-F in emulation, against a perfect emulated SDRAM (section 16). So a failure at D-F on the real board most likely points to the board, the clock, the cable or the port, not to the command logic [ESTIMATE].

---

## 8. Measurement protocol

1. **Data patterns: why they matter.**
   - A **true cell** stores 1 as charge; an **anti cell** stores 0 as charge [REPORTED, S30].
   - Leakage runs almost entirely from charged to discharged. So a true cell fails almost only while it holds 1, and an anti cell almost only while it holds 0.
   - Some chips mix true and anti cells in blocks, often one block per subarray; one study saw blocks of 512 rows [REPORTED, S30].
   - **All-0 plus all-1 therefore test every cell exactly once in its charged state.** The script uses that pair as its main retention curve (F_solid).
   - Neighbours matter too. A cell's retention shifts with the data in nearby cells (data-pattern dependence) [REPORTED, S23]. For some newer devices a simple 0/1 pattern found only ~15% of failures [REPORTED, secondary, S23].
   - Default set: ALL0, ALL1, CHECKER, CHECKER inverted, ROWSTRIPE, RANDOM (fixed seed). Add COLSTRIPE and inverted stripes if time allows.
2. **Waits.** 64 ms to 65.5 s in factor-2 steps: 11 values. `capture_retention.py` uses method A up to 4.096 s and method B above. Method B's true interval is the pause plus 54 ms; the firmware reports it and the analysis uses it.
3. **Temperatures.** 25, 45 and 65 °C on the chip surface, in that order. After each change, wait until the thermocouple has been steady within ±0.5 °C for 30 minutes.
   - For the 25 °C block, leave the heater unplugged and the lid ajar: the board warms a closed box 2-5 °C above room temperature [ESTIMATE: 0.5-1 W into 0.2-0.35 W/K], and a heater-only thermostat cannot cool. Pass the measured chip temperature to `--temp-c` (for example `--temp-c 27`). The analysis uses the thermocouple readings anyway.
   - The 25 °C block may run overnight. The 45 and 65 °C blocks are attended (Safety box).
4. **Repeats.** At least 5 full sweeps per temperature. Repeats catch **variable retention time (VRT)**: cells that jump between a long and a short retention time at random, like random telegraph noise (RTN) in transistors [REPORTED, S23-S24, S28]. The script shuffles pattern order in each repeat, so slow drift does not line up with one pattern.
5. **Controls.** Each temperature starts with a control run (method C: write, read, no pause). It must show **zero** failures.
6. **Early stop.** A sweep stops once a run fails more than 1% of all bits (`--stop-ber 1e-2`). Beyond that you are measuring the bulk, not the tail.
7. **Logging.** The firmware streams every failing word (address, expected and read value) for the first 20,000 failing words of a run, plus exact totals. The host adds a timestamp before each run. Do not edit the log by hand; annotate with lines starting with `#`.
8. **Run it:** `python3 capture_retention.py --port /dev/ttyACM0 --temp-c 45 --out e6_45C.log`. Disable sleep on the host PC.
   - Time: about 2.5-4.5 h per temperature with 5 repeats and 6 patterns; 45 and 65 °C take longest, because more runs hit the 20,000-line logging cap [ESTIMATE]. Add 1-1.5 h of heat-up and soak for each heated block: 12-15 h in all.
   - The estimate assumes about 20 s to write and read 8 MB per run (two passes over 4,194,304 words at a 16 MHz core), plus the waits, plus serial time (a capped run sends 20,000 lines × 25 bytes, which takes 43 s at 115200 baud). `--plan` prints the estimate. The control run measures your board's real write+read time and prints a revised estimate.
   - Optional: 500000 baud would cut the logging time (16 MHz / 500000 = 32 exactly, so the baud-rate divider is exact). Whether the ST-LINK VCP accepts it is [UNVERIFIED]. To try it, change `BAUD` in `main.c` and pass `--baud 500000`.
9. **If a campaign stops part-way** (power cut, PC asleep): the log is flushed line by line, so nothing already logged is lost. Rerunning appends a fresh plan to the same file. To finish only what is missing, use `--first-repeat K --repeats M`. Example: repeats 1-3 finished, so run `--first-repeat 4 --repeats 2` with the same `--out`.
10. **A-vs-B overlap check** (at 65 °C, after the main 65 °C sweep, box still at 65 °C):
    - `python3 capture_retention.py --port /dev/ttyACM0 --temp-c 65 --method A --patterns ALL0 ALL1 --waits 2.048 4.096 --repeats 3 --out e6_65C_A.log`
    - then the same with `--method B --out e6_65C_B.log`.
    - Analyse the pair together: `python3 retention_map.py analyze e6_65C_A.log e6_65C_B.log --report e6_overlap.md`. Section 1b of that report lists F_solid for A and for B at each wait, their ratio, and whether they agree within 2x. (You can also analyse each file on its own and compare the F_solid columns.)
    - **Never mix these two logs with the campaign logs.** Pooled together, they would double-count repeats in the VRT and ECC sections. If you must, `--method A` or `--method B` keeps only one method.
11. **Optional, recommended:** repeat 25 °C at the end. Agreement with the first 25 °C run shows the chip did not change during the campaign.

---

## 9. Data sheet and log template

**Paper log, one line per temperature block:**

| Date/time | Board ID and SDRAM marking | --temp-c °C | Thermocouple (TC) reading start/end °C | Ice-water offset °C | Room °C | Log file | Repeats done | Control run clean? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-__-__ __:__ | | 25 | / | | | e6_25C.log | | yes / no | |

**Stuck-on test log (step 8d), one line every 10 minutes:**

| Time | Box air on W1209 °C | Heater (thermocouple) °C | Room °C | Heater voltage V | Notes (bimetal clicked? smell? foam OK?) |
|---|---|---|---|---|---|
| __:__ | | | | 12.0 | |

**What the log file looks like** (written by the firmware and `capture_retention.py`; full format in the header of `retention_map.py`):

```
HELLO,e6-ret-0.5,IS42S16400J,4194304,16,8000000,A|B|C,HSE
H,1793700000.0
RUN,17,B,1,0,1234,16384,2,45.0
TEMP,17,start,45.12
F,17,1a2b3c,ffff,fffb
TEMP,17,end,45.25
END,17,812,815,815,0,812,16438,OK
```

`END` fields: run id, failing words, failing bits, bits 1→0, bits 0→1, words logged, retention interval actually tested (ms; for method B the pause plus 54 ms), and OK, TRUNC (cap hit; the counts stay exact) or ERR (a precharge timed out, the refresh count did not read back, or PB6 was not where it should be; the pause was skipped or is not trusted, and the analysis drops the run). `HELLO` fields: firmware version, chip, words, bits per word, SDCLK in Hz, methods, and the clock source (HSE or HSI).

---

## 10. Analysis

```
python3 retention_map.py analyze e6_25C.log e6_45C.log e6_65C.log --report e6_report.md --csv e6_curve.csv
```

The report has these parts:
1. **Retention CDF** (cumulative distribution: the fraction failing by time t) per temperature: the failing fraction at each wait, mean of repeats, with failing-bit counts. Also a lognormal fit and the local tail slope k (F ∝ t^k). ALL0 and ALL1 are paired within the same repeat and method.
   - **1b. Method A vs B overlap:** printed only when one analysis holds both methods at the same wait (section 8 step 10). `--method A` or `--method B` analyses one method only.
2. **Tail quantiles** 1e-7 to 1e-2, including the Oxide-Tail quantiles 1e-4 and 2e-5. On 67 million cells those carry ±1.2% and ±2.7% statistical error.
3. **Temperature acceleration:** pairwise and a global Arrhenius fit (Ea in eV; "retention halves every X °C").
4. **Cell polarity:** true and anti rows, and the block size of the interleave.
5. **Pattern coverage:** what share of all failing cells each single pattern finds.
6. **VRT:** cells that fail in some repeats but not others; strict VRT (first-failure wait varies ≥4x between repeats); and how fast new failing cells appear across repeats. A per-day growth rate is printed only for campaigns of a day or more; over a few hours the new cells are mostly ones flickering near their threshold.
7. **ECC.** Five codes:
   - SEC-DED (72,64);
   - BCH-4 (552,512);
   - BCH-12 (640,512), the dossier's binary code;
   - SSC-RS (18,16), byte symbols;
   - RS-8 (80,64), the dossier's code.

   Each runs with three mappings of cells to codewords: **adjacent** (real neighbouring addresses), **dq** (one symbol per data pin) and **random** (pseudo-random shuffle). Clustering is measured against chance coincidence. The output is the safe interval for target 1 and target 2, with EXTRAP flags.
8. **Verdict:** your 65 °C factor against the dossier's gate (PASS ≥24x, printed as "PASS (65 °C half of the gate only)"; NO-GO <4x) and its ~9x (DDR5) / ~11x or ~4x (retired DDR4, lockstep or one channel). It needs a 65 °C bin, or at least two temperatures so the fitted Ea can move the hottest bin to 65 °C (marked EXTRAPOLATION). A single 25 °C or 45 °C campaign prints NO VERDICT.

**`--selftest`** builds a synthetic 4 Mbit chip with a lognormal tail, VRT, coherent 2-bit clusters, 128-row anti-cell blocks and pattern dependence. It emulates the firmware's log line by line and runs the whole pipeline. Its 32 checks are of different strength, so here is what they do and do not show:
- VRT is detected (strict share > 0), but its size is not checked.
- The per-temperature lognormal median is within 2x and sigma within 30% of the planted values (actual: median off by up to 1.55x at 25 °C, sigma 1.46 against 1.24). Those are loose.
- The tight checks are on the end product: the RS-8 (target 2) and SEC-DED (target 1, extrapolated) safe intervals at 65 °C must land within 2x of the planted truth, computed straight from the generating model. Actual: 0.97x and 1.34x.
- A mixed A/B log gives a correct overlap table, and `--method A` filters it.
- Also: true/anti layout, block size, clustering, parsing, truncation, and a C-vs-Python check of the pattern generator.

It passes, exit 0, in about 6 s.

---

## 11. Pass/fail criteria

**A. Is the setup valid? All must pass before you believe any number.**

| Check | Pass | Fail means |
|---|---|---|
| Control runs (no pause) | 0 failing bits at every temperature | Wiring, timing or firmware error |
| 64 ms at 25 °C | 0 failing bits (prediction: 0 in every model corner) | Setup error, or a damaged chip |
| Method A vs B at 2.048 and 4.096 s, 65 °C (section 8 step 10; report section 1b) | F_solid within 2x | One method is not doing what you think |
| Repeat-to-repeat scatter where ≥100 bits fail | Coefficient of variation under 30% | Temperature drift or VRT overload |
| Thermocouple in ice water | 0 ± 2 °C | Wrong wiring or a faulty amplifier |
| Thermocouple start/end | Within ±1 °C of the value given to `--temp-c` (a stability check: the MAX31855 itself is only good to about ±2 °C) | Box not settled |

**B. The thesis at desk scale** (same lines as dossier section 5.R; RS-8 adjacent mapping, VRT multiplier, target 2):

| Result at 65 °C | Verdict | Prediction |
|---|---|---|
| ≥24x of 64 ms (≥1.54 s) | **PASS** (65 °C half of the gate only) | Central 42x (33x at Ea 0.6 eV) |
| 4x-24x | PARTIAL | Plausible: a 0.35 eV tail gives about 21x; the DDR5-like derate gives 17-21x |
| <4x (<256 ms) | **NO-GO** for this chip | Not expected (lowest corner about 10x) |

The dossier's PASS also needs ≥6x the window at 85 °C. This chip cannot go there, so a desk PASS is half a PASS.

Also record:
- the SEC-DED factor at 45 °C, target 2 (prediction ~4x; ~17x under the looser target 1; both without clustering);
- the share of multi-byte error events (the dossier's NO-GO line is >10% multi-chip events; here, >10% of RS-8 events spanning more than one byte is the analogue).

---

## 12. What would surprise you (results that would mean something new)

- **Failures at 64-256 ms at 25 °C,** with clean controls. Weak cells far left of the published tail. That chip would defeat simple relaxed refresh.
- **A kink in the tail:** two straight segments on the probit plot (z of the failing fraction against log time, where a lognormal is a straight line), with different Ea. That would be two leakage mechanisms (tail ~0.35 eV vs main ~0.6 eV is the reported picture) that you can separate on a desk. A kink exactly at the A/B switch (between 4.096 and 8.192 s) is suspect until the overlap check passes.
- **Ea well outside 0.3-1.1 eV,** or retention that *rises* with temperature for some cells. That points to telegraph-like trap physics (VRT), not plain leakage.
- **Strong clustering:** many multi-bit events in the adjacent mapping, well above chance. Clustered errors are the dossier's show-stopper number 1; they would favour symbol codes (RS) over binary BCH.
- **VRT that keeps growing:** new failing cells still appearing after many repeats, at a rate that does not flatten. That is the dossier's "unknown VRT growth" (show-stopper 3), on your desk.
- **Method A and B disagree** while both are working. That would mean relaxed refresh and paused refresh are not equivalent, which matters for how a controller should relax refresh.
- **A pass well above 169x or a result below 10x.** Either is outside the band of section 2.4; recheck the setup, then believe it.

---

## 13. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| No HELLO on the serial port | Wrong port or baud. The board is the old DISCO (no VCP). The ST-LINK firmware was updated to a non-VCP image (V2J..S0) [REPORTED, S6]. VCP solder bridges SB11/SB15 open (they are closed as shipped) [REPORTED, S6, S44] | Check the order code and the port (`python3 -m serial.tools.list_ports`). Use a 3.3 V USB-UART adapter on PA9/PA10: adapter TX → PA10, RX → PA9. On an old DISCO, a 2013 ST forum thread reports a large capacitor on PA9 that spoils USART1 transmit [REPORTED, S53, snippet only; UNVERIFIED]: if the adapter receives garbage, check your board revision's schematic for PA9 |
| `capture_retention.py` prints `device: SELFTEST,OK` before `Device: HELLO...` | Boot lines still in the buffer | Normal; it skips them |
| Permission denied on /dev/ttyACM0 | Not in the dialout group (Linux) | `sudo usermod -aG dialout $USER`, then log in again |
| Port busy | A serial terminal is still open | Close it |
| Garbled characters, also when cold | VCP issue reported on this board [REPORTED, S6] | Lower the baud rate or use an external adapter |
| Garbled characters only when hot, and HELLO ends in `HSI` | The crystal did not start, so the firmware runs on the internal 16 MHz oscillator (HSI). The datasheet allows −8% to +4.5% over −40 to 105 °C and about ±1% at 25 °C [REPORTED, S46]. A UART receiver tolerates only a few % in total, and lowering the baud rate does not fix a percentage error | Find out why the crystal does not start (HELLO should end in `HSE`; ST's examples and Zephyr run this board from its 8 MHz HSE, S42, S44). Meanwhile keep the MCU cooler than the chip, or trim RCC_CR.HSITRIM |
| `ERR,sdram init failed,step N` | The FMC did not accept a command: N = 1 clock enable, 2 precharge-all, 3 auto-refresh, 4 mode register (each one a BUSY timeout), 5 the refresh count did not read back, 6 bank 2 is not in normal mode | Confirm step B of section 7.1 passed (then the SDRAM itself is fine). Re-run `tools/e6_regcheck.py` if you changed the firmware. Try the fallback in step 5b |
| `ERR,sdram selftest,<word>,<expected>,<read>` | The 1 ms bus test after init failed. Word 0 with a walking-bit pattern: a data line (D0-D15) or a byte-lane line (NBL0/1) is stuck or open. A power-of-two word (for example 100 = word 0x100): that address line is stuck or shorted (column A0-A7 = words 1-0x80, row A0-A11 = 0x100-0x80000, bank BA0/BA1 = 0x100000 and 0x200000; this split of the word address is from memory of RM0090 [UNVERIFIED]) | A pin is not reaching the chip: reflow or inspect the board around the SDRAM and the MCU, and compare with step B. The firmware refuses RUN until SELFTEST passes |
| `ERR,hardfault` | The processor crashed (for example an SDRAM access with the FMC not set up) | Reset. Report the command that caused it. The capture stops at once instead of waiting for END |
| `ERR,refresh count readback` | The FMC refresh register did not keep the value written | The run ends in ERR and is dropped. If it repeats, the FMC is not clocked or not set up: reset and check `HELLO` and step 4 |
| `ERR,sdne1 pin` | PB6 did not go to GPIO-high for a method-B pause, or did not return to the FMC after it | The run ends in ERR and is dropped. Reset. If it repeats, use method A only (`--method A`, waits up to 4.096 s) |
| `ERR,sdram not initialised` after RUN | Init failed at boot (see above) | As above. The firmware refuses RUN so it cannot crash |
| Board stops answering after RUN (TIMEOUT); PING gets no PONG | A crash (HardFault) from an SDRAM access, normally announced by `ERR,hardfault` (see that row); or a hang inside a wait, which prints nothing | Reset. `SDRAM_BANK2_BASE` is 0xD0000000 (ST's board code, S42) and the register values match ST's (section 16), so suspect the board: confirm ST's example (section 7.1, step B) works. The capture aborts after 3 runs without END |
| `ERR,precharge timeout`; END ends in ERR | The FMC stayed busy | The run is skipped and dropped from analysis. If it repeats, reset the board and recheck the FMC setup |
| Control run fails | Timing, mode register or pin error; or code touching SDRAM | Recheck SDTR/SDCMR values; try CAS latency 2; make sure nothing runs from SDRAM |
| Every word fails at every wait, with clean controls | SDNE1 not handed back after method B | The firmware now checks this and prints `ERR,sdne1 pin`; if it does not, check PB6 MODER after the pause with a debugger |
| Nothing fails even at 65 s and 65 °C | Refresh never stopped (PB6 is not SDNE1 on your revision), or the chip is exceptional | Probe PB6 (SDNE1). During normal refresh it pulses low about every 13.25 µs ((105 + 1) / 8 MHz). During a method-B pause it must stay high for the whole wait. A 24 MS/s logic analyser resolves the 125 ns pulse. Compare with method A at 4 s and 65 °C (prediction ~1e-4 to 2e-4) |
| Temperature falls when the box heats | Thermocouple wires swapped | Swap the yellow (+) and red (−) leads (US colour code) |
| `TEMP` shows nan; capture warns "thermocouple fault" | Thermocouple open, or its tip touching metal or ground. Also when the breakout is unpowered or its SO wire is shorted to ground (an all-zero frame) | Re-tape the tip with Kapton; check the screw terminal |
| Heater never turns on, or never turns off | W1209 still in cooling mode (P0 = C) | Unplug the heater at once; set P0 = H (step 8a) |
| Thermal fuse opened, or the bimetal switch clicks | Heater too hot, or fuse too close to it | Find out why. Redo the stuck-on test (step 8d); keep the bimetal switch in the air, away from the heater. Never bridge either |
| Temperature overshoots or drifts | Hysteresis too wide; box leaks | Set 0.5 °C hysteresis; close gaps; wait 30 min |
| 25 °C block reads 27-30 °C | The board self-heats the closed box | Lid ajar, heater unplugged; pass the measured value to `--temp-c` |
| Many TRUNC runs | Normal at high failing fractions | Counts stay exact. Lower `--stop-ber` to 1e-3 for full maps |
| Board resets when the heater switches | Shared supply or ground noise | Separate adapter for the heater; keep its wiring away from the board |
| Capture stopped (host PC slept) | Sleep or a power cut | Disable sleep. Nothing logged is lost; finish with `--first-repeat` (section 8 step 9) |
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
   - The rowhammer-tester bypasses the LiteDRAM controller and sends command sequences through the PHY's DFI interface (the standard link between a memory controller and the physical layer) [REPORTED, S15]. The playbook config has a `refresh` key [REPORTED, S15].
   - A clean "disable refresh for T seconds" retention script was not found in the docs [UNVERIFIED]; you may need to write one.
   - Good for: real DDR3 timing and a more modern process. The DDR3L part number on current boards is [UNVERIFIED] (Digilent notes a memory change).
4. **A PC with ECC memory: real ECC, but read the warnings.**
   - **Setup.** An AM5 (Ryzen 7000/9000) board that supports ECC UDIMMs. Linux has EDAC reporting for Ryzen 7000 since kernel 6.5 [REPORTED, S20]. `rasdaemon` and `ras-mc-ctl --summary` log corrected errors per DIMM [REPORTED, S20]. DDR5 modules report their own temperature through the `spd5118` driver [REPORTED, S21].
   - **The knob.** Some AM5 BIOSes expose tREFI (the spacing between refresh commands) up to 65535; overclockers run it there [REPORTED/UNVERIFIED anecdotes, S19]. If the unit is memory-clock cycles at DDR5-6000 (3,000 MHz) [UNVERIFIED], 65535 cycles = 21.8 µs against the standard 3.9 µs. That is only **5.6x**: a 179 ms effective window. "Fine granularity refresh" mode halves it [REPORTED, S19].
   - **What you will probably see.** The central model gives ~0.1 weak cell in 32 GB at 45 °C and ~170 at 65 °C for a 179 ms window [ESTIMATE]. DDR5's on-die ECC fixes single errors inside each chip before EDAC sees them. **Expect zero corrected errors.** That is consistent with the thesis, but it is weak evidence.
   - **Risks.** Relaxed refresh can corrupt memory, crash the OS and damage files. Boot a live USB stick; disconnect or do not mount internal drives; save nothing important. Do not add heaters; read the module temperature and accept what you get. Community tREFI claims are anecdotes [UNVERIFIED].
   - **Before touching the BIOS:** if Windows uses BitLocker or Device Encryption, save the recovery key somewhere off this PC (your Microsoft account or a printout), or suspend BitLocker first. A BIOS change or a CMOS reset can trigger recovery, and a live USB does not prevent that. Without the key, the data on the internal drive is lost. Back up anything you care about.
   - **To clear the BIOS settings (CMOS reset):** shut down, switch off and unplug the PC at the wall, wait 1 minute, then use the board's clear-CMOS button or jumper as its manual describes. Never open the power-supply unit.
   - **Memory training:** after any memory-setting change an AM5 board retrains memory, and the first boot can show a black screen for several minutes. Wait 5 minutes before you reset [UNVERIFIED].
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

## 16. Verification (run 2026-11-04)

**What the firmware was checked against.** ST's own code, cloned from GitHub (shallow and sparse clones). The three driver commits are the ones STM32CubeF4 at this commit pins as submodules.

| Source | Commit | Used for |
|---|---|---|
| STMicroelectronics/STM32CubeF4 (package FW.F4.1.28.3) | 60c8abe0ae88 | ST's FMC_SDRAM and UART examples for this board, `core_cm4.h` (S42, S43) |
| STMicroelectronics/32f429idiscovery-bsp | d77779a2a4e9 | The board's SDRAM driver: pins, timings, init sequence, mode register, refresh count (S42) |
| STMicroelectronics/stm32f4xx_hal_driver | 1f6451c3e077 | FMC low-level driver, GPIO alternate functions, UART baud formula, PLL limits (S42) |
| STMicroelectronics/cmsis-device-f4 | 9192c7b9df75 | `stm32f429xx.h` register map, startup vector order, memory map (S43) |
| zephyrproject-rtos/zephyr | decee24b4fbc | Independent board file: console on USART1 PA9/PA10, FMC pins, 8 MHz HSE (S44) |
| cmsis-svd/cmsis-svd-data | c65f8551e57c | ST's STM32F429 SVD v1.2: FMC register reset values and field layout (S43) |

**Results.**

| Command | Result |
|---|---|
| `python3 retention_map.py --selftest` | 32/32 checks pass, exit 0 (~7 s), including planted-truth checks of the 65 °C safe intervals and the A-vs-B overlap table |
| `python3 retention_map.py predict` | exit 0; numbers in section 2, including the temperature-law table (section D2) |
| `python3 capture_retention.py --selftest` | 17/17 checks pass, exit 0 (pyserial absent: simulate path), including injected faults: an ERR line mid-run, a failed control run, a hung board, truncated END lines, a broken thermocouple, `--first-repeat` and the `--seed` range |
| `python3 capture_retention.py --plan --temp-c 25 / 45 / 65` | about 3.2 / 3.9 / 3.6 h [ESTIMATE] |
| `python3 capture_retention.py --simulate ...` then `retention_map.py analyze ...` | exit 0 end to end |
| `make syntax` (host gcc -fsyntax-only -std=c11 -Wall -Wextra, default and with -DENABLE_METHOD_Z) | clean |
| `host_test_patterns.c` vs Python `pattern_words()` | 624/624 samples identical |
| `make` with arm-none-eabi-gcc 13.2.1 (Ubuntu 24.04 package 15:13.2.rel1-2, binutils 2.42) | Compiles and links with no warnings. Firmware e6-ret-0.5 (after the second review below): text 5,904 B, data 8 B, bss 12 B; `e6_retention.bin` is 5,912 bytes (sha256 5085b41b…5816a0). No floating-point instructions. Largest stack frame 216 B (`main`, from `-fstack-usage`), so about 0.3 KB of stack at the deepest call [ESTIMATE]. The `-DENABLE_METHOD_Z` build also links (text 5,996 B) |
| `python3 tools/e6_regcheck.py ...` (section 7, step 4) | 127/127 items OK: 95 numbers compiled from ST's header and from `regs_f429.h`, 30 checks of pins, timings, sequence and constants against ST's board code and HAL, 2 memory-map checks. Negative test: one deliberately wrong bit and one wrong pin were both reported (exit 1) |
| QEMU 8.2.2, board `netduinoplus2`, with `make emu` | QEMU's STM32F405 board has the same Cortex-M4 core and the same USART1 and GPIO addresses, but no FMC and 128 KB of RAM, so the emulator build skips the SDRAM. Result: the firmware boots, the crystal times out after 100 ms and it falls back to HSI, then prints `ERR,sdram init failed,step 100` (expected in this build), `HELLO,...,HSI`, and answers `PING` with `PONG`, `TEMP`, and errors for bad commands |
| Unicorn 2.1.4 CPU emulator, `tools/e6_emulate.py`, with the same `e6_retention.elf` that would be flashed | Boots on the crystal path (`HELLO,...,HSE`); `SELFTEST,OK`. The FMC receives SDCR1 0x2AD0, SDCR2 0x1D4, SDTR1 0x0F1F6FFF, SDTR2 0x01126361, then SDCMR 0x09 (clock enable), 0x0A (precharge-all), 0xEB (8 auto-refreshes), 0x4600C (mode register 0x230), then SDRTR 0xD2 (COUNT 105). Those are the values ST's HAL writes for these settings, apart from the deliberate TWR and auto-refresh count. PLLCFGR 0x28431004 (reserved bit 29 kept at its reset value 1); USART1 BRR 0x8B. RUN C, A (COUNT 124 for 64 ms, 7,999 for 4.096 s) and B complete with correct END lines. With one SDRAM address line stuck low the self-test names the right word (byte bit 1 → word 1; bit 9 → word 0x100; bit 21 → word 0x100000); a stuck data line fails at word 0 |
| `tools/e6_emulate.py --campaign`: the real `capture_retention.py` campaign code drives the emulated board, with 4 SDRAM words that flip one bit when read 1 s or more after writing | 13 runs (control, then ALL0 and ALL1 × 3 waits × 2 repeats), exit 0. Every 1.024 s and 8.192 s run reports exactly 4 failing bits, 1→0 under ALL1 and 0→1 under ALL0; 64 ms runs report none. `retention_map.py analyze` reads the log |
| Bug found by that loop, fixed | `retention_map.py analyze` crashed (`OverflowError` in the lognormal fit) when the failing fraction does not rise with the wait, as with a few defective cells that fail at every wait. The fit now reports "no lognormal fit" when sigma > 10 or the median is absurd; the self-test still passes |
| Firmware on a real board | **Not tested** |

**Second review (independent, 2026-11-04).** A second reviewer re-cloned ST's sources into fresh folders (the same six commits as above; all three driver submodule commits match what STM32CubeF4 pins), then re-read every firmware file against them without using the first review's comments. An independent compile-and-compare of 92 register numbers (CMSIS header vs `regs_f429.h`) matched 92 of 92; `tools/e6_regcheck.py` on the fresh clones also reported ALL OK. Pins, alternate functions, timings, init order, mode register, refresh formula, UART pins and divider, clock tree, vector table, stack and the `.data`/`.bss` start-up copy were all confirmed. It found no wrong register value. It made six small fixes:

| Finding | Risk before the fix | Fix |
|---|---|---|
| `RUN … Z …` was accepted on a normal build (Z compiled out) and ran as a control | A Z run silently became a no-pause run, labelled Z | Z is refused (`ERR,bad RUN command`) unless built with `-DENABLE_METHOD_Z` |
| The FMC buffers SDRAM writes in a 16-entry write FIFO [REPORTED, S52]; ST does not say whether a command or a pin hand-over waits for it | In method B, a write still queued when chip select goes high could be lost and counted as a retention failure [ESTIMATE] | One read of the last SDRAM word after the write loop, so every posted write has reached the chip before the precharge and the pause |
| The forbidden COUNT value (S52) was checked for bank 2 only (18) | With bank 1's reset timings the sum is 45, which a 24 ms method-A wait would program [ESTIMATE] | COUNT 45 is skipped |
| The self-test wrote its complement word to word 1 | With column address A0 stuck low, word 1 aliases word 0 and the fault was named as a data line (emulated: `ERR,sdram selftest,0,0001,fffe`) | The complement goes to the last word; A0 is now reported as word 1 |
| A thermocouple frame of all zeros (breakout unpowered, SO shorted low) read as 0.00 °C | A false but plausible-looking temperature | It reads as `nan` |
| GPIO set-up order differed from ST's HAL (mode before AF number) | None found: the SDRAM is not yet initialised, and AF0 is assumed unused on these pins [UNVERIFIED] | AF number first, mode last, as `HAL_GPIO_Init` |

Version bumped to e6-ret-0.5. Re-run after the fixes: `make` (no warnings), `make syntax`, `make hosttest`, the method-Z build, the QEMU emulator build (boots, `HELLO,e6-ret-0.5,…,HSI`, `PONG`), Unicorn boot and RUN A/B/C (a 24 ms method-A run programs COUNT 46; `RUN … Z …` refused on the normal build, run on the Z build), the stuck-address self-test for byte bits 1, 2, 9, 16, 17, 21 and 22 (each names its own word), and the `--campaign` loop (exit 0). Still never run on a real board.

**Safety of the three pause methods, re-checked.** No path leaves the SDRAM unrefreshed without a check firing, as far as registers and pins can show (they cannot prove the chip itself is refreshed; the clean control runs do that): if the normal refresh count does not read back after method A or Z, or PB6 does not return to the FMC after method B, the run ends in ERR and every later RUN and SELFTEST is refused until reset. During every pause the processor touches no SDRAM (code, stack and data are in internal flash and SRAM; only the SysTick interrupt runs). All banks are precharged first, so no row stays open past tRAS(max) (120 µs in ST's board code comment, S42). In method B the FMC keeps issuing refreshes that the chip ignores; because the processor issues no reads or writes in that window, the FMC never believes a row is open that the chip has not opened, so its state matches the chip's when the pin returns [ESTIMATE, from the command truth table, S45]. The firmware has no heater control and no watchdog: the heater is limited by the hardware interlocks of section 6 alone, so a firmware crash cannot leave it on.

**What is verified now, and what is not.**

| Item | Status | Evidence |
|---|---|---|
| Every register address, bit field and value the firmware uses (RCC, GPIO, USART1, SysTick, FMC) | Verified against ST's header | S43; `e6_regcheck.py` |
| The 38 SDRAM pins, AF12, PB6 = SDNE1, PB5 = SDCKE1 | Verified against ST's board code and Zephyr | S42, S44 |
| SDRAM geometry, CAS 3, SDCLK = HCLK/2, read pipe 1, timings, mode register 0x0230, refresh formula, init order, bank-2 register split | Verified against ST's board code and HAL. Three deliberate differences: TWR 3 (ST: 2), 8 auto-refreshes (ST: 4), 100 ms power-up wait (ST's board code: 1 ms) | S42 |
| USART1 on PA9/PA10, AF7, baud divider | Verified against ST's UART example and HAL | S42 |
| ST-LINK virtual COM port wired to PA9/PA10 through SB11/SB15, closed as shipped | Reported | S6, S44 |
| An 8 MHz crystal (HSE) on the board | Reported: ST's examples and Zephyr run the board from an 8 MHz HSE without bypass. If it is absent, the firmware falls back to HSI and says so | S42, S44 |
| Flash and RAM regions in the linker script | Verified against ST's memory map | S43 |
| Method A: COUNT 41-8191, changed at run time | COUNT range reported; changing it after init is outside ST's stated use (H7 text). The A-vs-B overlap check (section 8, step 10) is the hardware test | S3 |
| Method B: chip select high = command inhibit | Reported in ISSI's truth table for this chip family. Handing an FMC pin to a GPIO mid-run is not documented by ST [UNVERIFIED]; the firmware checks the pin each time | S45 |
| Method Z: COUNT = 0 | EXPERIMENTAL, off by default | S3 |
| TWR rules (TWR ≥ TRAS − TRCD and ≥ TRC − TRCD − TRP) | Reported for the STM32H5 FMC; 3 meets both | S50 |
| IS42S16400J timing table, power-up wait, auto-refresh count, no minimum clock at 8 MHz | [UNVERIFIED]: the datasheet could not be downloaded. ST's board code drives the same part with these settings at 90 MHz | S8, S42 |
| MAX31855 on PE2-PE4 | Partly: ST's board code uses port E only for the SDRAM; one user reports PE2-PE5 free | S42, S32 |
| Anything on a real board | Not tested | - |

**Remaining risks at first power-on**, most likely first [ESTIMATE of the order]:
1. The ST-LINK virtual COM port does not appear, or its firmware lost the VCP (section 13, first row).
2. The 8 MHz crystal does not start: HELLO ends in `HSI`. Everything works at room temperature; text may garble at 65 °C (section 13).
3. Method B's pin hand-over misbehaves on real silicon: `ERR,sdne1 pin`, or A and B disagree in the overlap check. Then use method A only (waits up to 4.096 s), or test method Z.
4. Method A's run-time change of COUNT does not take effect as expected. The overlap check catches it.
5. The SDRAM part on your board is not an IS42S16400J (read the marking; section 7, step 1).

**Exact build commands that worked in this session** (Ubuntu 24.04, x86-64):

```
# compiler: either  sudo apt install gcc-arm-none-eabi binutils-arm-none-eabi
# or, without root, unpack the same two packages into a folder (needs libisl23, libmpc3, libmpfr6):
apt-get download gcc-arm-none-eabi binutils-arm-none-eabi
dpkg -x gcc-arm-none-eabi_15%3a13.2.rel1-2_amd64.deb ~/armgcc
dpkg -x binutils-arm-none-eabi_2.42-1ubuntu1+23_amd64.deb ~/armgcc
cd home-lab/code/T3_dram/stm32_retention
make CROSS=~/armgcc/usr/bin/arm-none-eabi-          # plain `make` with the apt install
make CROSS=~/armgcc/usr/bin/arm-none-eabi- emu      # emulator build (never flash it)
qemu-system-arm -M netduinoplus2 -nographic -kernel e6_emu.elf -serial stdio -monitor none
python3 -m pip install unicorn                       # once
python3 ../../../tools/e6_emulate.py                 # boot, commands, RUN A/B/C
python3 ../../../tools/e6_emulate.py --campaign --out emu.log
```

In QEMU, type `PING` and press Enter. Ctrl+A then X should quit (QEMU's `-nographic` key) [UNVERIFIED with this exact command line]; closing the terminal also stops it. The GitHub release downloads of the xPack toolchain and of the Renode emulator were blocked in this session, so neither was tried.

---

## Sources

Tags: [DATASHEET] vendor document; [REPORTED] paper, press, forum or distributor page, usually read as a search snippet in this session; [ESTIMATE] my calculation, or the study's model where marked "(study model)"; [UNVERIFIED] could not confirm; "[UNVERIFIED] (from memory)" means it comes from prior knowledge, with no URL confirmed. Vendor source code that was read in full (ST's GitHub repositories, S42-S43) is tagged as a vendor document. Hosts that could not be reached from this session on 2026-11-04: st.com (RM0090, UM1670 and the datasheet PDFs), issi.com and three datasheet mirrors (datasheet.chipsmall.com, cdn.components.ru, static.chipdip.ru), manualslib.com, docs.rs, docs.embassy.dev, builds.renode.io, and GitHub's release downloads and API (so the xPack toolchain and Renode were not tried); facts from those places rest on search snippets. Prices are snapshots, approximate as of Nov 2026.

- **S1** ST board-support code for the STM32F429I-Discovery SDRAM (mbed mirror): IS42S16400J, FMC bank 2, 90 MHz timings. https://os.mbed.com/teams/ST/code/BSP_DISCO_F429ZI/docs/tip/stm32f429i__discovery__sdram_8c_source.html [REPORTED]
- **S2** 21ic forum SDRAM test: 4 banks × 4,096 rows × 256 columns × 16 bit, 12 row bits and 8 column bits. https://bbs.21ic.com/icview-2515182-1-1.html [REPORTED]
- **S3** FMC_SDRTR register text (STM32H7 device description, via docs.rs search snippets): 13-bit COUNT, at least 41 SDRAM clocks, COUNT = period/rows − 20, the timer starts on write, "if the value programmed is 0, no refresh is carried out". https://docs.rs/stm32h7/latest/stm32h7/stm32h743/fmc/sdrtr/struct.SDRTR_SPEC.html [REPORTED; F4 equivalence UNVERIFIED] The same text says the register "must not be reprogrammed after the initialization procedure to avoid modifying the refresh rate", and a search snippet of RM0090 Rev 18 (the F4 manual, via a manualslib.com page that was itself blocked) gives "COUNT = (SDRAM refresh rate x SDRAM clock frequency) - 20" and "COUNT must not equal TWR + TRP + TRC + TRCD + 4" [REPORTED, search snippets 2026-11-04; the F4 manual itself was not read]
- **S4** FMC SDCMR/SDSR descriptions (command register, power-down status, auto-refresh precedence). https://docs.rs/stm32-hal2/1.8.2/stm32_hal2/pac/fmc/sdcmr/index.html ; https://docs.ros.org/en/api/picovoice_driver/html/group__FMC__SDRAM__Mode__Status.html [REPORTED]
- **S5** ST community: F7 SDRAM reports power-down and corrupted data after a re-init (anecdote). https://community.st.com/stm32cubemx-mcus-29/stm32f7-fmc-sdram-error-after-reinit-3256 [REPORTED]
- **S6** ST community: STM32F429I-DISC1 VCP on USART1 via SB11/SB15; a garbled-VCP report. https://community.st.com/s/question/0D50X00009XkeWa/stm32f429disco1-vcp-connection ; https://community.st.com/stm32-mcus-boards-and-hardware-tools-26/stm32f429-disco1-vcp-connection-92741 [REPORTED]. Old STM32F429I-DISCO (ST-LINK/V2, no VCP) vs STM32F429I-DISC1 (ST-LINK/V2-B with VCP; "VCP available with the new order code only"): ST UM1670 https://www.st.com/resource/en/user_manual/dm00093903.pdf ; RT-Thread BSP note https://github.com/RT-Thread/rt-thread/blob/master/bsp/stm32/stm32f429-st-disco ; a DISC1 that lost its VCP after its ST-LINK was flashed with a plain V2 ("S0") image: ST community thread 20884 [REPORTED, cited by a reviewer; not re-fetched in this revision] A 2026-11-04 search snippet of an ST staff reply: the ST-LINK/V2-B VCP (U2 pins 12 and 13) reaches USART1 on PA9/PA10 through SB11 and SB15, which are ON by default on the DISC1; see UM1670 section 6.3.3. https://community.st.com/stm32-mcus-boards-and-hardware-tools-26/stm32f429-disco1-vcp-connection-92741 [REPORTED]
- **S7** Zephyr board page: console on USART1, PA9/PA10, 115200 8N1. https://docs.zephyrproject.org/latest/boards/st/stm32f429i_disc1/doc/index.html [REPORTED]
- **S8** ISSI 64Mb SDRAM datasheet: 4,096 refresh cycles per 64 ms (commercial, industrial, A1), 16 ms for A2. https://www.electronicsdatasheets.com/download/122066.pdf?format=pdf [DATASHEET, read via search snippet; host blocked]
- **S9** Temperature grades: Arrow IS42S16400J-5TL commercial, 70 °C max (listed obsolete) https://www.arrow.com/en/products/is42s16400j-5tl/integrated-silicon-solution-inc.html ; RS IS42S16400J-7TLI −40 to 85 °C, 143 MHz https://uk.rs-online.com/web/p/sdram/8115125 ; Findchips claims 0-85 °C for -7TL-TR https://origin-www.findchips.com/detail/is42s16400j-7tl-tr/Integrated-Silicon-Solution-Inc [REPORTED, conflicting; -7TL range UNVERIFIED]
- **S10** Board prices and stock: Digi-Key (497-16140-ND, 99-week lead time) https://www.digikey.com/en/products/detail/stmicroelectronics/STM32F429I-DISC1/5731713 ; Digi-Key IT €26.23 https://punchouttest.digikey.it/en/products/detail/stmicroelectronics/STM32F429I-DISC1/5731713 ; TME $45.61 https://www.tme.com/us/en-us/details/stm32f429i-disc1/stm-development-kits/stmicroelectronics/ ; Waveshare $62.99 https://www.waveshare.com/product/32F429IDISCOVERY.htm [REPORTED] Re-checked 2026-11-04 by search (aggregator and regional pages, no live US page read): Mouser 511-STM32F429I-DISC1, 559 in stock at $31.56 (undated); Digi-Key 648 in stock at $45.92 (listing dated 2026-06-21), 658 in stock on the Canada page, 461 on the Denmark page; Newark, element14 and TME in the $40-64 range. https://www.electronicsdatasheets.com/manufacturers/stmicroelectronics/parts/stm32f429i-disc1 ; https://www.digikey.ca/en/products/detail/stmicroelectronics/STM32F429I-DISC1/5731713 ; https://www.digikey.dk/en/products/detail/stmicroelectronics/STM32F429I-DISC1/5731713 [REPORTED]
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
- **S33** Adafruit MAX31855 breakout, product 269, $14.95. https://www.adafruit.com/products/269 [REPORTED] Re-checked 2026-11-04: $14.95 for 1-9 at Adafruit; Mouser 339 in stock; The Pi Hut £14.70 (5 left); Pi Supply sold out. https://octopart.com/part/adafruit-industries/269 ; https://thepihut.com/products/adafruit-thermocouple-amplifier-max31855-breakout-board-max6675-upgrade [REPORTED, search snippets]
- **S34** Adafruit heating pads: 1481 (10 × 5 cm, 5 V only, $7.95) https://www.adafruit.com/products/1481 ; 4308 (14 × 5 cm heating fabric with stainless-steel fibres, "apply 5-12 V DC", no published maximum temperature; £5.80 at Pi Hut) https://thepihut.com/collections/new-products-maker/products/electric-heating-pad-14cm-x-5cm ; https://core-electronics.com.au/electric-heating-pad-14cm-x-5cm.html ; Switch Science (5 V, max 1 A) https://www.switch-science.com/products/6460 ; about 0.6 A at 5 V (third-party listing) https://stgaws.robu.in/product/adafruit-accessories-electric-heating-pad-14cm-x-5cm [REPORTED, cited by reviewers; the 12 V figures are ESTIMATE]
- **S35** W1209 thermostat: 12 V, -50 to 110 °C, NTC probe, relay; $4-7. Menu: P0 = C (cooling, the factory default) or H (heating); P1 hysteresis; P2 upper setpoint limit; P6 high-temperature cut (relay OFF, display `---` or `HHH`), which is P7 on some firmware. https://shillehtek.com/blogs/shillehtek-product-manuals/w1209-12v-digital-temperature-controller-thermostat-switch-module-manual ; https://protosupplies.com/product/w1209-temperature-controller-module/ ; https://www.elektroda.com/rtvforum/topic3435508.html ; https://www.tinytronics.nl/shop/en/sensors/temperature/digital-thermostat-module-with-relay-xh-w1209 [REPORTED, search snippets, Nov 2026]
- **S36** Adafruit product 270, "Thermocouple Type-K Glass Braid Insulated", $9.95, good to 500 °C. https://www.adafruit.com/product/270 ; https://www.jameco.com/z/270-Adafruit-Industries-Thermocouple-Type-K-Glass-Braid-Insulated-K_2500751.html [REPORTED, cited by a reviewer; not re-fetched in this revision] Re-checked 2026-11-04: $9.95 for 1-9, $8.96 for 10-99 at Adafruit; The Pi Hut £9.60 in stock. https://www.adafruit.com/products/270 ; https://thepihut.com/collections/new-products-maker/products/thermocouple-type-k-glass-braid-insulated [REPORTED, search snippets]
- **S37** This study: [dossiers/raw-ber-contract.md](../dossiers/raw-ber-contract.md) (sections 2.1, 2.5, 5.R; the PASS line is ≥6x the window at 85 °C and ≥24x at 65 °C), [models/raw-ber-contract.py](../models/raw-ber-contract.py) (85 °C retention anchors, lognormal fit), [models/dram_cell_physics.py](../models/dram_cell_physics.py) (`RET_HALVING_C = 10`), [research/stage3/decision.json](../research/stage3/decision.json) [ESTIMATE] (study model, as tagged there)
- **S38** 12 V heater listings. Thermo Tech polyimide heating foil, self-adhesive, 12 V DC / AC, 15 W, 90 mm, IPX4 (Conrad 1594187) https://www.conrad.com/p/thermo-tech-polyimide-heating-foil-self-adhesive-12-v-dc-12-v-ac-15-w-ip-rating-ipx4-140-mm-1594187 ; RS PRO 50 × 100 mm polyimide mat, 5 W at 12 V (too weak for this box) https://ph.rs-online.com/web/p/heating-elements/7983769 ; RS PRO silicone mat 15 W, 100 × 150 mm, 12 V DC (too big to sit beside the board) https://za.rs-online.com/web/p/heater-pads/0731350 [REPORTED, search snippets, Nov 2026; prices and temperature ratings not shown in the snippets] Re-checked 2026-11-04: Thermo Technologies 3616108 TECH polyimide heating foil, 12 V, 15 W, 90 mm diameter, self-adhesive, IPX4, Rapid Online 07-7003, £19.46 ex VAT, 35-38 in stock https://www.rapidonline.com/thermo-technologies-3616108-tech-polyimide-heating-foil-12v-15w-ipx4-07-7003 . Note that the Conrad 1594187 URL above names 140 mm, so it is probably a different, larger foil. Omega KHLVA self-adhesive polyimide heaters (US) https://omega.com/en-us/p/KHRA-KHLVA-KHA-Series [REPORTED, search snippets; Omega price not shown]
- **S39** Thermal fuses: the holding temperature Th is the highest temperature at which the fuse will not open while carrying rated current for 168 h; fuses can open anywhere between Th and the rated functioning temperature Tf; under IEC 60691 Tf has a tolerance of +0/−10 °C. https://forum.digikey.com/t/thermal-fuse-holding-temperature-vs-rated-functioning-temperature/55 ; https://www.swe-check.com.au/editorials/thermal_fuses.php [REPORTED, search snippets]. "Th is typically 20-30 °C below Tf" is [UNVERIFIED] (from memory of typical datasheets)
- **S40** Contact burns: InCompliance, "Contact Burn Injuries" series (a 100 mm metal plate at 54 °C causes a burn in a 1-minute contact; thinner objects need more) https://incompliancemag.com/contact-burn-injuries-part-2/ ; https://incompliancemag.com/contact-burn-injuries-the-influence-of-object-thermal-mass/ [REPORTED]. ISO 13732-1 holds the official thresholds; its tables were not read [UNVERIFIED]
- **S41** Read-disturbance: RowHammer (Kim et al., ISCA 2014) and RowPress (Luo et al., ISCA 2023) flip bits in rows next to frequently or long-activated rows [UNVERIFIED] (from memory; not fetched). The tools that test it are in S15 and S17
- **S42** ST's board and driver code on GitHub, read in full in this session: STMicroelectronics/STM32CubeF4 @ 60c8abe0ae88 (package FW.F4.1.28.3) https://github.com/STMicroelectronics/STM32CubeF4 , files Projects/STM32F429I-Discovery/Examples/FMC/FMC_SDRAM/{readme.txt, Src/main.c, Src/stm32f4xx_hal_msp.c, Inc/main.h, Inc/stm32f4xx_hal_conf.h, STM32CubeIDE/.project, STM32CubeIDE/STM32F429ZITX_FLASH.ld} and Examples/UART/UART_TwoBoards_ComPolling/Inc/main.h; STMicroelectronics/32f429idiscovery-bsp @ d77779a2a4e9 https://github.com/STMicroelectronics/32f429idiscovery-bsp , files stm32f429i_discovery_sdram.c/.h, stm32f429i_discovery.h, stm32f429i_discovery_lcd.h; STMicroelectronics/stm32f4xx_hal_driver @ 1f6451c3e077 https://github.com/STMicroelectronics/stm32f4xx_hal_driver , files Inc/stm32f4xx_ll_fmc.h, Src/stm32f4xx_ll_fmc.c, Inc/stm32f4xx_hal_gpio.h, Inc/stm32f4xx_hal_gpio_ex.h, Inc/stm32f4xx_hal_uart.h, Inc/stm32f4xx_hal_rcc.h, Inc/stm32f4xx_hal_rcc_ex.h, Src/stm32f4xx_hal_rcc.c, Inc/Legacy/stm32_hal_legacy.h. The firmware comments cite file:line in these commits [DATASHEET: vendor code]
- **S43** ST's register map and startup files: STMicroelectronics/cmsis-device-f4 @ 9192c7b9df75 https://github.com/STMicroelectronics/cmsis-device-f4 , files Include/stm32f429xx.h, Source/Templates/gcc/startup_stm32f429xx.s, Source/Templates/system_stm32f4xx.c; STM32CubeF4 @ 60c8abe0ae88 Drivers/CMSIS/Include/core_cm4.h; ST's STM32F429 SVD v1.2 (register reset values and field layout) from cmsis-svd/cmsis-svd-data @ c65f8551e57c https://github.com/cmsis-svd/cmsis-svd-data [DATASHEET: vendor code]
- **S44** Zephyr's board support for this board: zephyrproject-rtos/zephyr @ decee24b4fbc, boards/st/stm32f429i_disc1/stm32f429i_disc1.dts (console = USART1, PA9/PA10; FMC pins; 8 MHz HSE without bypass) and doc/index.rst (UART_1_TX PA9, UART_1_RX PA10, 115200 8N1, ST-LINK/V2-B, /dev/ttyACM0). https://github.com/zephyrproject-rtos/zephyr/tree/main/boards/st/stm32f429i_disc1 [REPORTED: an independent project's board file, read in full]
- **S45** ISSI IS42S16400-family truth table and command descriptions: COMMAND INHIBIT = CS high, other inputs don't care; it "prevents new commands from being executed", operations in progress are not affected; AUTO REFRESH at least 4,096 times every 64 ms. https://html.alldatasheet.com/html-pdf/227645/ISSI/IS42S16400_08/534/5/IS42S16400_08.html ; https://zh.datasheetq.com/pdf-html/421820/ISSI/6page/IS42S16400E.html [REPORTED, search snippets of sibling revisions; the IS42S16400J datasheet itself was not reachable]
- **S46** STM32F427/F429 datasheet, HSI 16 MHz accuracy: about −8% to +4.5% over −40 to 105 °C (factory calibrated), about ±1% at 25 °C (that row is ambiguous in the mirror). https://www.alldatasheet.net/html-pdf/2185176/STMICROELECTRONICS/STM32F429NET7/273593/120/STM32F429NET7.html [REPORTED, mirror snippet 2026-11-04]
- **S47** The ST-LINK connector is USB Mini-B ("USB Type-A to Mini-B cable" in a copy of ST's data brief, https://static.chipdip.ru/lib/558/DOC014558516.pdf , seen only as a snippet; RS and Keil board pages). https://twen.rs-online.com/web/p/microcontroller-development-tools/9093660 ; https://www.keil.arm.com/boards/stmicroelectronics-stm32f429i-disc1-revc-06565c3/features/ [REPORTED, search snippets 2026-11-04]
- **S48** Thermostat and cut-out prices, 2026-11-04: XH-W1209 at US $6.83-8.92 on eBay listings and €4.00 at Tinytronics https://www.ebay.de/itm/335833500498 ; https://www.tinytronics.nl/shop/en/sensors/temperature/digital-thermostat-module-with-relay-xh-w1209 . KSD301 80 °C normally closed: Walmart (uxcell) $7.99 https://www.walmart.com/ip/206167273 ; Newegg Business $6.99 for two https://www.neweggbusiness.com/p/9B-30D-007Z-000W3 ; LCSC $0.33 each in quantity https://datasheet.lcsc.com/lcsc/XC-Elec-Shenzhen-KSD-301-80-103PAB_C156483.pdf [REPORTED, search snippets]
- **S49** Buck converter and thermal-fuse prices, 2026-11-04: LM2596 module, Addicore $2.48 https://reach.dog/shop/addicore/products/lm2596-step-down-adjustable-dc-dc-switching-buck-converter ; eBay $1.59 plus $6.89 shipping https://www.ebay.com/itm/225988103697 . Thermal fuses: element14 single axial parts about A$3.54 https://au.element14.com/c/circuit-protection/fuses-fuse-accessories/fuses/thermal-fuses ; Bürklin Thermodisc 90-piece assortment 72-240 °C, €147 https://www.buerklin.com/en/thermal-fuse-assortment/p/30g440 [REPORTED, search snippets]
- **S50** FMC write-recovery rules: TWR must match the SDRAM's tWR and satisfy TWR ≥ TRAS − TRCD and TWR ≥ TRC − TRCD − TRP (example: TRAS 4, TRCD 2 gives TWR ≥ 2, programmed as 0x1); with one SDRAM device the unused bank's TWR stays at its reset value 0xF. STM32H5 FMC register text via search snippets of https://docs.embassy.dev/stm32-metapac/git/stm32h563zi/fmc/regs/struct.Sdtr.html [REPORTED; F4 wording UNVERIFIED; that host was blocked for direct reading]
- **S51** Tools used for the build and the emulation, 2026-11-04: Ubuntu 24.04 packages gcc-arm-none-eabi 15:13.2.rel1-2 (sha256 519a5d0e5292…c5a91948), binutils-arm-none-eabi 2.42-1ubuntu1+23 (sha256 2aab2d6a7e4c…1e543472) and qemu-system-arm 1:8.2.2+ds-0ubuntu1.18 from http://archive.ubuntu.com/ubuntu ; Unicorn 2.1.4 from https://pypi.org/project/unicorn/ [REPORTED]
- **S52** RM0090 (STM32F405/415/407/417/427/437/429/439 reference manual) Rev 18, FMC SDRAM text, seen only as search snippets on 2026-11-04 (the mirror and ST's site were blocked): "The programmed COUNT value must not be equal to the sum of the following timings: TWR+TRP+TRC+TRCD+4 memory clock cycles"; COUNT "must be set at least to 41 SDRAM clock cycles"; "Write Data FIFO with 16 x33-bit depth, Write Address FIFO with 16x30-bit depth, Cacheable Read FIFO with 6 x32-bit depth". https://www.manualslib.com/manual/3287447/St-Stm32f405.html?page=1679 ; https://www.manualslib.com/manual/3287447/St-Stm32f405.html?page=1676 [REPORTED, snippets]
- **S53** ST community thread "Testing USART1 on STM32F429IDISCO board" (2013), which, per a search summary, says PA9 is hard to use for USART1 because of a large capacitor on it. Not read; it predates the DISC1, whose ST-LINK VCP uses PA9/PA10 (S44). https://community.st.com/s/question/0D50X00009Xki47SAB/testing-usart1-on-stm32f429idisco-board [REPORTED, snippet only; UNVERIFIED]
- **[ESTIMATE]** Everything computed in section 2 and in the code: leakage arithmetic, Arrhenius factors, expected failing cells, safe intervals and their temperature-law sensitivity, refresh-timer limits (COUNT 105/124, 4.19 s, 6.29 s), method B's +54 ms, the tREFI 5.6x arithmetic, the run-time estimates, the box heat balance (EPS walls 1.5-2.5 cm, k ≈ 0.035 W/m·K, ~0.13 m², ×1.3 for leaks → about 0.2-0.3 W/K, so 8-13 W to hold 65 °C in a 20-22 °C room), the heater-to-air temperature rise (h ≈ 10-20 W/m²K over the tile), and the read count of section 3.
