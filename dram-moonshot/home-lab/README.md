# Home lab: DRAM from first principles, on your desk

*The front door to eight home experiments for the [dram-moonshot](../README.md) study. As of 2026-11-03. Prices are approximate as of November 2026 and come from each guide [ESTIMATE unless tagged].*

**Evidence tags** (as in the guides): [DATASHEET] maker's spec; [REPORTED] paper, listing or snippet; [ESTIMATE] our arithmetic; [UNVERIFIED] not confirmed; [STUDY] a study model output.

**Acronyms.** 1T1C / 2T0C: one transistor and one capacitor / two transistors and none. BBD: bucket-brigade device. CTE: charge-transfer efficiency. Ea: activation energy. IGZO: indium gallium zinc oxide. JFET: junction field-effect transistor. SEC-DED / RS: single-error-correcting / Reed-Solomon codes. σ_ln: the spread of log retention time.

---

## The short answer

- **What you can do at home.** Test the main laws a DRAM (dynamic random-access memory) bit obeys (all but thermal noise, which stays theory), with parts about a million times bigger than a chip's. Map the retention tail of a real 67-million-cell DRAM chip. Measure femtoamp (1e-15 A) leakage. Even make a zinc-oxide transistor and store a bit on it.
- **What it proves.** The textbook laws the three picks rest on (stored charge, leakage-limited retention, charge sharing, Arrhenius heating, tail statistics) hold on your bench, and you can run the exact methods the study needs: floating-node droop, tail quantiles, Arrhenius fits, error-correction relaxation. It does not show that any pick works.
- **What it cannot prove.** That 0.01 µm² oxide transistors leak only attoamps (1e-18 A) in their worst 1-in-10,000. That is the study's biggest unknown, and it needs a university nanofab and about 1e5 devices.
- **Can home experiments revolutionize how DRAM is made?** Not on their own. The study's new ways to make DRAM (oxide gain cells built below 400 °C on top of logic, the AND-stack) stand or fall on fab-made 0.01 µm² devices, measured by the 1e5. No kitchen-table result can settle that. What home work can do is make the next step cheaper and sharper: real data, tested analysis code and a filled-in Oxide Tail Spec to send to a university fab ([From kitchen table to fab](#from-kitchen-table-to-fab)).
- **Best first project for a software builder: [E6](E6_retention_tail_real_dram.md), at room temperature first.** Its first steps ([E6 §7](E6_retention_tail_real_dram.md#7-build), steps 3-7, 9 and 10) are a ready-made board, a compiler, a `--simulate` dry run, 8 header pins for a thermometer and a room-temperature smoke test. No analog craft, no chemicals, no heater until you choose one. The 25 °C start costs about $70-105 (board, USB cable, thermocouple kit, standoffs, tape; [E6 §5](E6_retention_tail_real_dram.md#5-parts-and-tools)) [ESTIMATE]. You get real tail statistics from 67 million cells: the FASTEST PROOF's mechanism. [E2](E2_gain_cell_no_capacitor.md#7-procedure) starts by air-wiring sub-picoamp nodes on ±9 V rails, and [E4](E4_femtoamp_leakage_bench.md#phase-a-bring-up-and-the-bench-floor-day-1-2) by reaching a ≤20 fA floor in a shielded tin: craft first, code second. Caveat: E6's firmware has never run on a real board. It builds, matches ST's own code register by register, and runs end to end in emulation ([E6 §16](E6_retention_tail_real_dram.md#16-verification-run-2026-11-04)), but budget an evening for bring-up (first power-on checklist: [E6 §7.1](E6_retention_tail_real_dram.md#71-first-power-on-checklist); fallback: E6 §7 step 5b).

---

## First principles in one screen

A bit needs three things:
1. **A store:** a place to keep charge (a capacitor, or a transistor's gate).
2. **A switch that barely leaks:** so the charge stays.
3. **A sense:** a way to read the charge without losing it, or with a fast restore.

Six equations cover almost everything ([FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md) has the rest).

| # | Law | Part of the bit | What it says | Backbone | Tested in |
|---|---|---|---|---|---|
| 1 | Q = C·V | Store | A 1 nF bench cell holds ~580,000x a chip cell's charge | [§2.1](FIRST_PRINCIPLES.md#21-charge-q--cv-calcs-2) | E1 |
| 2 | t = C·ΔV / I, so I = C·dV/dt | Switch | Retention is charge budget ÷ leakage; a slow droop measures tiny currents | [§2.2](FIRST_PRINCIPLES.md#22-retention-t--cδv--i_leak-and-its-inverse-i--cdvdt-calcs-3) | E1, E2, E4, E8 |
| 3 | ΔV = (V/2)·Cs/(Cs + Cbl) | Sense | The signal depends only on the cell-to-bitline ratio, and the read destroys the bit. A gain cell senses current instead | [§2.3](FIRST_PRINCIPLES.md#23-sense-signal-by-charge-sharing-δv--v2cscs--cbl-calcs-4), [§2.9](FIRST_PRINCIPLES.md#29-gain-cells-read-through-a-transistor-not-by-sharing-charge-calcs-9) | E1; E2, E8 |
| 4 | E = C·V²; for a wire E ≈ α·C'·L·V² | Store and wires | Wire capacitance per metre is nearly scale-free, so energy tracks distance | [§2.4](FIRST_PRINCIPLES.md#24-energy-the-supply-pays-cv-the-capacitor-keeps-cv-calcs-5), [§2.10](FIRST_PRINCIPLES.md#210-the-price-of-distance-e_bit--αc_wirev--the-root-of-hot-side-memorys-10x-calcs-10) | E1, E3, E5 |
| 5 | I ∝ exp(−Ea/kT); n_i ∝ exp(−Eg/2kT) | Switch | Leakage is thermally activated; a wide band gap (oxides ~3-3.4 eV, silicon 1.12) removes the thermal floor | [§2.7](FIRST_PRINCIPLES.md#27-temperature-i--expeakt-calcs-7), [§2.8](FIRST_PRINCIPLES.md#28-band-gap-n_i--sqrtncnvexpeg2kt--the-root-of-the-best-bet-calcs-8) | E4, E6, E7, E8 |
| 6 | N ≳ 3/p to see a p-quantile; code stretch = exp(σ_ln·Δz) | All three | The weakest cells set refresh; a code's gain depends only on the tail's spread | [§4](FIRST_PRINCIPLES.md#4-statistics-of-tails-how-many-samples-a-1e-4-quantile-needs-calcs-14) | E6, E4 (E1 in miniature) |

Two more laws live in the backbone: charge transfer CTE^N ([§2.11](FIRST_PRINCIPLES.md#211-charge-transfer-an-isolated-packet-keeps-cten-calcs-11), tested in E5) and thermal noise kT/C ([§2.6](FIRST_PRINCIPLES.md#26-thermal-noise-σ_v--sqrtktc-and-a-minimum-capacitance-calcs-6), theory only).

---

## The ladder

Numbers come from each guide's header table; safety levels are defined in [SAFETY.md §1](SAFETY.md#1-how-to-use-this-file).

| # | Experiment | The question it answers | Study concept it supports | Cost | Time | Difficulty (1-5) | Safety | Needs |
|---|---|---|---|---|---|---|---|---|
| E1 | [A bit on the bench](E1_bit_on_the_bench.md) | Do charge sharing, the destructive read and t = C·ΔV/I hold on a bench cell, and does a code stretch refresh? | Baseline for all; FASTEST PROOF in miniature | $25-40 (Part A) + $30-45 (Part B), plus the core kit | 1 day (A); a second weekend (B) | 3 (A), 4 (B) | Low; Medium with the warm box | Pico (RP2040), breadboard, multimeter, soldering iron |
| E2 | [A gain cell without a capacitor](E2_gain_cell_no_capacitor.md) | If the capacitor goes, does the write switch's leakage alone set retention? | BEST BET cell; MOONSHOT cell | $25-45 plus the core kit | 1 weekend | 3 (4 with the JFET) | Low; Medium with the warm box | As E1, plus two 9 V batteries |
| E3 | [The price of distance](E3_price_of_distance.md) | Does wire energy grow with length and V²? | BEST BET's 0.37 vs 3.95 pJ/bit claim [STUDY] | $15-30 plus the core kit | Half a day | 2 | Low | Pico, multimeter, coax |
| E4 | [Femtoamp leakage bench](E4_femtoamp_leakage_bench.md) | Can you measure femtoamp leakage, and its tail statistics, at home? | The biggest unknown's method (Oxide Tail Spec) | $105-150 first build; $165-235 full | Build 1-2 weekends; 2-3 weeks for 30 devices; 6-10 weeks full | 3 (4 with option A and heater) | Medium | Soldering, meter with capacitance range, drill and vise, cookie tin, Python + numpy |
| E5 | [Charge river (BBD)](E5_charge_river_bbd.md) | How much charge does each transfer leave behind, and can moving charge hold data? | CHARGE-RIVER | $40-60 | Build 1 weekend; 1-2 weekends of runs | 2 (3 for clean CTE) | Low; Medium warm | Pico 2, multimeter; scope optional |
| E6 | [Retention tail of a real DRAM](E6_retention_tail_real_dram.md) | What does a real 67-million-cell retention tail look like, and how much refresh can a code save? | FASTEST PROOF (raw-BER contract) | $115-200 (board $32-66) | 1-2 weekends; ~12-15 h of runs | 3 | Medium | STM32F429I-DISC1, Arm toolchain, Python + numpy + pyserial, thermocouple |
| E7 | [Make your own oxide transistor](E7_make_your_own_oxide_transistor.md) | Can a water-based ink and a hot plate below 400 °C make a working oxide channel? | BEST BET, MOONSHOT and CHARGE-RIVER materials | $410-550 plus a hot plate (first proof); ~$1,200 with the rig | 1-2 weekends (first proof); 3-4 or 6-10 weekends (full) | 4 | High | Hot plate ≥350 °C, spin coater, milligram scale, splash goggles, 30 V bench supply |
| E8 | [Your own oxide gain-cell memory](E8_your_own_oxide_gain_cell_memory.md) | Can your own oxide transistor hold a bit, and does it beat silicon when hot? | BEST BET 2T0C cell | ~$49 on top of E7 (+$10 array) | 2-3 weekends after E7 (+1-2 array) | 4 (5 for the array) | Medium | E7's rig, heater block, drill and M3 tap |

**Core kit** ([E1 §5.1](E1_bit_on_the_bench.md#51-shared-core-kit-also-used-by-e2-and-e3)): Pico, breadboards, jumpers, multimeter, DS18B20 sensor, resistor and capacitor assortment, USB cable: about $70-100.

---

## Three paths

**(a) Software builder: E6 → E4 → E2** (E3 as an optional half-day warm-up).
- **E6** first, at 25 °C with the heater unplugged: board, cable, thermocouple (about $70-105). Add the heater box for 45 and 65 °C once the pipeline works. The study's 65 °C gate needs those heated runs: a 25 °C-only analysis prints NO VERDICT.
- **E4** next, as the room-temperature 30-device build (op-amp option B). Its `leakage_tail.py` is the Oxide Tail Spec rehearsal.
- **E2** last, as your first low-leakage build: the BEST BET's law in one weekend. Buy one RP2040 Pico (not an early Pico 2) and use it for both E4 and E2.
- **Budget:** about $310-580 with the core kit. **Calendar:** about 2-3 months part-time; 4 with E4's full temperature series.

**(b) Electronics: E1 → E2 → E3 → E4 → E5.**
- Each step reuses the last: E1's core kit serves E2 and E3, its warm box serves E2, and E4's heater block serves E5.
- **Budget:** about $310-560, plus ~$70-95 of options (warm box, USB isolator, USB power meter) and an optional oscilloscope ($60-400). **Calendar:** 3-5 months part-time.

**(c) Materials: E4 → E7 → E8.**
- E4 gives the femtoamp method; E7 makes the transistor (its battery test is the first proof); E8 stores a bit on it and races it against silicon.
- **Budget:** about $1,350-1,480; about $980-1,110 if a makerspace lends the hot plate and spin coater. **Calendar:** 4-8 months part-time. Do E7 at a makerspace if you can ([SAFETY.md §13](SAFETY.md#13-move-this-to-a-makerspace-or-a-lab)).

---

## What would count as a real discovery

These would be new, or rare in public, and worth publishing with data and code (the guides' searches found no prior public version, which is not proof that none exists [UNVERIFIED]):
- **E6: a full retention map of a named part** (the IS42S16400J on the DISC1) at 25, 45 and 65 °C: σ_ln, tail vs main activation energy, VRT (variable retention time) statistics, true/anti-cell layout, clustering, and the measured ECC (error-correcting code) relaxation factor against the dossier's gate.
- **E4: a 2N7000 off-leakage distribution at 1 V** for 30-120 devices, with quantile confidence intervals, per-device Ea and a two-brand split. The datasheet guarantees only ≤1 µA at 48 V [DATASHEET].
- **E7 + E8: the activation energy of a home-made ZnO transistor's subthreshold leakage at a fixed hold bias** (biased hold, 30-100x above the floor; [E8 §7](E8_your_own_oxide_gain_cell_memory.md#7-procedure) step 10b), against a silicon junction on the same storage node. No hobbyist ZnO-transistor write-up could be verified ([E7 §14](E7_make_your_own_oxide_transistor.md#14-precedents-people-who-made-semiconductors-outside-a-fab)).
- **E5: per-transfer CTE against clock** (the predicted U-curve) and the stopped-clock retention tail of a V3207 bucket-brigade chip. No per-stage figure was found ([E5 §2.1](E5_charge_river_bbd.md#21-law-1-charge-is-conserved-but-transfer-is-incomplete)).

**What would surprise, and matter** (from the guides' "surprise" sections):
- E6 cells failing at 64-256 ms at 25 °C, or strong error clustering: relaxed refresh would struggle.
- An oxide Ea *above* silicon's (E8): a warning for hot-side memory at 105-125 °C.
- Two populations of E4 devices: the tail problem in miniature.
- E8 oxide leakage flat from 25 to 65 °C while ≥3x above the floor: the temperature half of the hot-side thesis, in miniature (it says nothing about attoamp levels).

---

## From kitchen table to fab

| Step | Where | What it adds | Rough cost |
|---|---|---|---|
| 1. Home | E1-E8 | Laws, methods, tested analysis code | $300-1,500 by path |
| 2. Makerspace or community lab | Ventilation, spin coaters, metal contacts, reflow ovens | Better films and benches; not cleanroom data | Tens to low hundreds of dollars a month [ESTIMATE, E7 §2] |
| 3. University nanofab, external user | Purdue's Birck Nanotechnology Center (first choice), Georgia Tech IEN (second) | Sputtered IGZO, deposited gate dielectrics, lithography, heated probe stations: hundreds of devices, the median and 1-10% tail | Birck 2023 for-profit rates: $51/day lab + $61/day cleanroom, plus tool hours [REPORTED, E7 S42]. E8's first ask: ~$1.1k of day fees + $2-5k of tool time |
| 4. Shared wafer lot or MPW (multi-project wafer) shuttle | The study's Oxide Tail Statistics lot; open-source shuttles such as SKY130 | ≥1e5 cells at 85-125 °C: the 1e-4 tail that decides the BEST BET | ~$210-280k lot in the judges' budgets as read by E2 and E4 (E7 and E8 read $220-280k); Gate A+ ~$240k [STUDY]; shuttle prices vary [UNVERIFIED] |

**What each home experiment hands to the next step:**
- **E6 →** a university DRAM Bender station (~$14k in the study's budget): `retention_map.py`, your σ_ln, VRT and clustering ([E6 §3](E6_retention_tail_real_dram.md#3-honest-scope)).
- **E4 →** a probe-station campaign: `leakage_tail.py` and a home tail spec whose sample-size column you computed ([E4 §13](E4_femtoamp_leakage_bench.md#13-scaling-up-what-it-would-take-next)).
- **E7 + E8 →** a nanofab request: curves, extraction files and the email template in [E8 §13](E8_your_own_oxide_gain_cell_memory.md#13-from-this-demo-to-a-nanofab-your-ticket).
- **E5 →** the CCD (charge-coupled device) rider: `ccd_cte.py`, the 3/n zero-error rule, and the "$35 paper" step ([E5 §13](E5_charge_river_bbd.md#13-scaling-up-what-it-would-take-next)).
- **E1, E2, E3 →** test structures on a shuttle: a 1T1C or gain-cell array, wire-length ladders.

**The bridge is the Oxide Tail Spec,** the study's Monday action: one page of device structures × channel splits, device area, timescale, temperature, hydrogen and thermal dose, bond split, and each concept's pass/kill line. [E4 §12](E4_femtoamp_leakage_bench.md#12-rehearsing-the-oxide-tail-spec) rehearses every column. [E6 §15](E6_retention_tail_real_dram.md#15-how-this-connects-to-the-oxide-tail-spec-the-studys-monday-action) maps its quantiles. E8 §13 attaches it to the request you send to Purdue Birck.

---

## Honest limits

- **Scale.** Parts ~1e6x bigger than a chip's: the laws transfer, retention times do not.
- **Floors.** ~1-10 fA at best at home (E4, after blank subtraction, with an air or PTFE capacitor; 10-100 fA with a boxed film capacitor). The study needs attoamps to zeptoamps. A reading at your floor is your setup, not the device: every guide runs a floor or blank test for this reason.
- **Statistics.** 16 cells (E1), 30-120 devices (E4) and 4 cells (E8) cannot reach a 1e-4 quantile. E6 can, but it is silicon physics on an old SDR (single-data-rate) node at ≤65 °C: not oxide, not DDR5, not 85 °C.
- **E7's gate is bought.** Its ~1,000 °C thermal oxide means only the channel is low-temperature.
- **Code.** All firmware is reference code, **untested on hardware**; the analysis code is self-tested on synthetic data only. E6's firmware goes furthest: it is checked against ST's own code and runs end to end in emulation ([tools/e6_regcheck.py](tools/e6_regcheck.py), [tools/e6_emulate.py](tools/e6_emulate.py)).
- **Evidence.** Most specs and prices come from search snippets; check your part's datasheet.

---

## Before you start

1. **Read [SAFETY.md](SAFETY.md),** then the guide's own Safety box.
2. **Check the code:** `python3 tools/check_home_lab.py` runs every self-test and checks links and sections (needs numpy; `--quick` skips slow runs).
3. **Tools:** the core kit above; a temperature-controlled soldering iron; safety glasses; a computer with Python 3, numpy and `mpremote`. E6 adds pyserial and the Arm GNU toolchain. Code notes: [code/T1_pico/README.md](code/T1_pico/README.md).
4. **Buying tips:**
   - E6: the order code must end in DISC1 (the older DISCO has no virtual COM port).
   - Use an RP2040 Pico for E1 and E2: early Pico 2 boards (RP2350 A2) leak on floating pins (erratum E9).
   - Buy the LMC6482**A**IN, not the 3 mV LMC6482IN.
   - Storage nodes: C0G/NP0 or polypropylene capacitors, never X7R or Y5V. Buy spares from a second batch.
   - Bucket-brigade chips are scarce: buy three V3207D.
   - Lab suppliers sell ammonia and nitrates only to institutions; order through a makerspace, and buy the smallest bottle.
   - Silica gel: orange, cobalt-free only. 12 V adapters: certified and unmodified.

---

## Where the guides differ on purpose

Real contradictions were fixed in the guides ([SAFETY.md §14](SAFETY.md#14-where-the-guides-disagreed-and-what-changed) lists the safety ones). These differences are deliberate:
- **Bench cell.** The backbone uses 1 nF on 6.8 nF (212 mV). E1 uses the commoner 4.7 and 10 nF (288 and 150 mV), which bracket it.
- **Retention example.** 50 s at 10 pA with 0.5 V of droop (backbone) vs 154 s with E1's 1.54 V sense budget.
- **Coax.** 97 pF/m from geometry (backbone) vs 101 pF/m from the datasheet (E3).
- **Error-correction factors.** E1's 1.1-1.4x, the backbone's 2-30x, E6's 1-113x and the study's ~9x use four different baselines ([FIRST_PRINCIPLES §4](FIRST_PRINCIPLES.md#4-statistics-of-tails-how-many-samples-a-1e-4-quantile-needs-calcs-14)).
- **"Retention halves every 10 °C"** means Ea ≈ 0.79 eV near 85 °C, but ≈ 0.6 eV near 25-65 °C.
- **2N7000 off-leakage planning:** E4 0.1-10 pA at 1 V; E2 10 pA-10 nA at 3 V; E8 10 pA. You measure it.
- **Oxide Ea:** 0.8 eV for the study's IGZO; 0.35 eV planned for E8's home ZnO film.
- **Energy ratio:** 10.6x (E3), 10.7x (backbone) and ~11x (study) differ only by rounding.
- **Switch orientation agrees:** 2N7000 source to the bit line, drain to the storage node (E2, E4, E8). E1 step 9 adds a 1.65 V precharge on purpose, to show the body-diode trap.
