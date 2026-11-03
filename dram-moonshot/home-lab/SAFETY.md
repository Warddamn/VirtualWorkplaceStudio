# Home-lab safety

*All eight experiments in one place. As of 2026-11-03. Every rule below comes from a guide or from [FIRST_PRINCIPLES.md §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment), and links to it. Where the guides disagreed, the safer rule won and the guide was changed (section 14).*

**Evidence tags.** [REPORTED] = a supplier safety data sheet (SDS) or other source, as cited in the guide. [UNVERIFIED] = the guide could not confirm it. [ESTIMATE] = arithmetic.

---

## 1. How to use this file

1. Read section 2 (hard rules) before you buy anything.
2. Read the section for each hazard your experiment has (the table below).
3. Then read the guide's own Safety box. It has the details for that build, and it wins for that build.

| Guide | Its Safety box | Hazards beyond the basics (sections here) |
|---|---|---|
| E1 A bit on the bench | [E1 §4](E1_bit_on_the_bench.md#4-safety) | 9 V battery; optional 12 V warm box (3); fridge runs (10); IPA (5) |
| E2 A gain cell without a capacitor | [E2 §4](E2_gain_cell_no_capacitor.md#4-safety) | ±9 V batteries (7); glass reed relay (6); E1's warm box (3) |
| E3 The price of distance | [E3 §4](E3_price_of_distance.md#4-safety) | USB fast-charge meter (7); coax on the floor (12) |
| E4 Femtoamp leakage bench | [E4 §6](E4_femtoamp_leakage_bench.md#6-safety) | 12 V heater block to 85 °C (3); drilling a tin (11); silica gel (5) |
| E5 Charge river (BBD) | [E5 §6](E5_charge_river_bbd.md#6-safety) | Optional E4 block at ≤60 °C (3); 15 V fallback chip (7) |
| E6 Retention tail of a real DRAM | [E6 §6](E6_retention_tail_real_dram.md#6-safety) | 12 V heater in a foam box (3); your PC's data on the PC route (9) |
| E7 Make your own oxide transistor | [E7 §3](E7_make_your_own_oxide_transistor.md#3-safety) | Ammonia and metal nitrates (5); hot plate to 350 °C (4); silicon shards (6); 27-30 V (7) |
| E8 Your own oxide gain-cell memory | [E8 §3](E8_your_own_oxide_gain_cell_memory.md#3-safety) | 14.4 W heater block (3); 27 V on the chip (7); E7's chemistry (5) |

**Safety level** used in the [README ladder](README.md#the-ladder): **Low** = low-voltage electronics and soldering only (E3; E1, E2 and E5 without a heater). **Medium** = adds a home-built heater or your computer's data (E4, E6, E8; E1, E2 and E5 with the heater). **High** = corrosive and toxic chemicals plus a 350 °C hot plate (E7).

---

## 2. Hard rules

These apply to every experiment ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment) unless another link is given).

**Electricity**
- **No mains-voltage builds.** Never build anything that plugs into the wall. Never open or modify a mains device. Bought, unmodified tools are fine: bench supply, soldering station, hot plate, laptop charger, a certified 12 V adapter ([E4 §6](E4_femtoamp_leakage_bench.md#6-safety), [E6 §6](E6_retention_tail_real_dram.md#6-safety)).
- **30 V is the ceiling.** USB, AA/AAA/9 V cells, certified 12 V adapters, or a 0-30 V bench supply. Set the supply's voltage and current limit (50-100 mA; E7 uses 30 V and 50 mA) *before* you connect a circuit ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)). No vacuum-tube high voltage.
- **Protect your computer** with a powered USB hub or a USB isolator ([E1 §4](E1_bit_on_the_bench.md#4-safety), [E2 §4](E2_gain_cell_no_capacitor.md#4-safety)).

**Banned at home**
- Hydrofluoric acid (HF) and anything containing it, including some rust removers ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)).
- Cyanide, mercury (including mercury UV lamps, so no UV-ozone cleaning), liquid nitrogen, lasers above class 2, pressurized toxic gases.
- Inverted canned air as a freeze spray (flammable; frostbite), and dry ice in any closed container ([E6 §6](E6_retention_tail_real_dram.md#6-safety) also bans cold sprays and liquid nitrogen).
- 2-methoxyethanol, the solvent in most published oxide inks: reproductive toxin, H360FD, and flammable, H226 [REPORTED].
- Metal-nitrate "combustion" inks with organic fuels (2-methoxyethanol, acetylacetone); heating a dried nitrate-plus-fuel residue.
- Concentrated acids, piranha and RCA cleans; any acid stronger than household vinegar ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)).
- Spray pyrolysis: it makes a breathable mist of metal salts. Inhaled indium compounds have caused fatal lung disease in workers; NIOSH's limit is 0.1 mg/m³ [REPORTED, E7 S34].
- Sputtering and any vacuum deposition.
- Ceramic wool (refractory ceramic fibre, Carc. 1B, H350i) ([E4 §6](E4_femtoamp_leakage_bench.md#6-safety)).
- Blue indicating silica gel (cobalt(II) chloride, Carc. 1B and Repr. 1B) ([E4 §6](E4_femtoamp_leakage_bench.md#6-safety)).

**Heat**
- Never leave a hot plate or a hot soldering iron unattended. Heaters follow the rule for their design (section 3.1): E1's and E6's foam boxes are always attended; E4's and E8's metal blocks are attended until you have watched one full heated run.
- **Never bridge a fuse or a thermal cut-out.** An opened fuse means something went wrong: find out why ([E6 §6](E6_retention_tail_real_dram.md#6-safety)).

**Your own computer**
- Do every DRAM experiment on a separate chip or board. Do not change refresh or memory timing in the BIOS of a PC you need. Do not chill or pull memory from a running PC ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment), [E6 §6](E6_retention_tail_real_dram.md#6-safety)).

---

## 3. Heaters and thermal runaway

Four heater designs exist. E2 reuses E1's; E5 reuses E4's at 60 °C. Each one stacks **independent layers**: a power limit, software, and hardware cut-outs that work even if the software or the sensor fails.

### 3.1 The heaters side by side

| | E1 warm box (also E2) | E4 block (also E5) | E6 thermostat box | E8 block |
|---|---|---|---|---|
| Section | [E1 §6.5](E1_bit_on_the_bench.md#65-warm-box-heater-optional) | [E4 §5.3](E4_femtoamp_leakage_bench.md#53-mini-hot-chuck-and-thermostat-only-for-runs-above-room-temperature) | [E6 §7 step 8](E6_retention_tail_real_dram.md#7-build) | [E8 §3](E8_your_own_oxide_gain_cell_memory.md#3-safety) |
| Heater | 2 × 10 Ω 10 W resistors **in series** on an aluminium plate, on metal spacers ≥20 mm, in a 2-3 L foam box | 2 × 10 Ω 25 W aluminium-housed resistors **in series**, bolted to a ~30 × 30 × 15 mm aluminium block in the tin, under a foil tent | 12 V, ~15 W polyimide or silicone heater rated ≥150 °C, on a ceramic tile lifted off the floor of an EPS foam box | One 10 Ω 25 W aluminium-clad resistor bolted to a ≥60 × 40 × 6 mm aluminium block on a ceramic tile |
| Supply | Certified 12 V DC adapter, ≥1 A | 12 V adapter with safety marks, 1 A inline fuse | Certified 12 V adapter, 2 A inline fuse, optional buck converter | Bought 12 V, 2 A adapter |
| Power if stuck on | 7.2 W | 7.2 W | Whatever the stuck-on test allows (≤15 W) | 14.4 W (software caps duty at 30%, ~4.3 W) |
| Highest setpoint | 45 °C (board ≤55 °C) | 85 °C; E5 sets 60 °C | 65 °C (W1209 setpoint capped at 70 °C) | 65 °C |
| Software guard | Cut-off at 55 °C; off on sensor failure; watchdog; 100 kΩ gate pull-down | Cut-off at 90 °C; sensor fault; runaway check; watchdog; 100 kΩ pull-down | W1209 in heating mode (P0 = H), over-temperature cut 72 °C | Off above 70 °C or if the NTC reads below 5 °C; watchdog; 100 kΩ pull-down |
| Hardware cut-out 1 | 72 °C thermal fuse clamped to the plate | Bimetal thermostat, ~95 °C, self-resetting, clamped to the block | 80 °C bimetal switch in the box air, 2-3 cm from the SDRAM | 80 °C bimetal thermostat (KSD301 type) pressed to the block |
| Hardware cut-out 2 | (the power limit and first test) | One-shot thermal fuse ~110 °C on the block | One-shot thermal fuse on the heater, ≥110 °C, ~25 °C above its stuck-on temperature | One-shot thermal fuse ~91 °C |
| Proof before use | 60 min fully on with only the sensor inside: box air must stay ≤55 °C, else use a 9 V adapter (4 W) | Watched heat-up to 85 °C from cold; must settle below ~87 °C | **Stuck-on test:** fully on, no thermostat; box air must settle ≤75 °C and the heater ≤ its rating − 25 °C | Check NTC against a thermocouple at 45 and 65 °C |
| Supervision | Always attended | Attended until you have watched one full run end to end; smoke alarm | Heated blocks always attended by an awake adult; look every 30-60 min; never overnight | Same rule as E4 |

The cut-out temperatures differ because the setpoints differ. Each hardware cut-out sits about 10-30 °C above its own setpoint, so it does not trip in normal use. One-shot fuses are rated to hold only well below their opening temperature, so a fuse rated near the working temperature would open during normal runs ([E6 §6](E6_retention_tail_real_dram.md#6-safety), [E8 §3](E8_your_own_oxide_gain_cell_memory.md#3-safety)).

### 3.2 Rules for every heater

- **Series, never parallel.** Two 10 Ω resistors in parallel draw 28.8 W, four times the series power. In E1 that overloads each 10 W resistor ([E1 §6.5](E1_bit_on_the_bench.md#65-warm-box-heater-optional)). E4 used to allow it as a fallback; it no longer does (section 14).
- **Heater current never runs through a breadboard or jumper wires.** Use 20-22 AWG stranded wire, screw terminals or crimp splices ([E4 §5.3](E4_femtoamp_leakage_bench.md#53-mini-hot-chuck-and-thermostat-only-for-runs-above-room-temperature), [E6 §7](E6_retention_tail_real_dram.md#7-build)).
- **A pull-down keeps the heater off** whenever the microcontroller is unplugged, resetting or hung: 100 kΩ from gate to source, plus the hardware watchdog (E1, E4, E8).
- **12 V never touches a microcontroller pin.** Only the gate resistor and one common ground join the circuits. Check with the meter before you plug in USB ([E1 §6.5](E1_bit_on_the_bench.md#65-warm-box-heater-optional)).
- **Solder a thermal fuse with care.** Crimp it, or solder ≥10 mm from its body with pliers on the lead as a heat sink: soldering heat can open or weaken it. Check it reads ~0 Ω afterwards ([E4 §5.3](E4_femtoamp_leakage_bench.md#53-mini-hot-chuck-and-thermostat-only-for-runs-above-room-temperature)).
- **Foam.** Polystyrene foam (EPS or XPS) is rated only to about 74-75 °C and burns with styrene smoke [REPORTED, E4 S23]. Keep anything that can pass 60 °C (heater, resistors, plate) **at least 20 mm from foam** ([E4 §6](E4_femtoamp_leakage_bench.md#6-safety)). Foam boxes hold only air at ≤75 °C: E6 proves that with its stuck-on test, and E1's box stays ≤55 °C.
- **Placement.** Stand every heater on a hard, non-flammable surface (tile, stone or metal tray), away from curtains and paper. Keep a smoke alarm in the room and the 12 V plug within reach ([E6 §6](E6_retention_tail_real_dram.md#6-safety)).
- **Stopping a heated run.** Unplug the 12 V heater adapter first. Then stop the script with Thonny's Stop button or by unplugging the Pico. Ctrl-C in an `mpremote` terminal stops only the computer side; the Pico and its heater keep running ([E1 §4](E1_bit_on_the_bench.md#4-safety), [E2 §4](E2_gain_cell_no_capacitor.md#4-safety)).
- **Burns.** Metal at about 65 °C can burn skin within seconds [REPORTED, E6 S40]. Let a block cool below 45 °C before you touch it or swap devices ([E4 §6](E4_femtoamp_leakage_bench.md#6-safety)).
- **Hair dryer** (E1, E2): short demos only, ≤15 min, on its lowest setting, ≥30 cm away, attended ([E1 §4](E1_bit_on_the_bench.md#4-safety)).
- **Never improvise** a heat mat, a kitchen appliance or a hot plate under a powered board in place of these designs ([FIRST_PRINCIPLES §2.7](FIRST_PRINCIPLES.md#27-temperature-i--expeakt-calcs-7)).

---

## 4. Hot plates and fire

Only E7 (and E8's devices, made in E7) use a hot plate ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety), [FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment)).

- **The right plate.** A bought lab hot plate with a ceramic or aluminium top. Never a kitchen pan, griddle or toaster oven, anything with a non-stick (PTFE) coating, or anything that will touch food again.
- **Temperature caps.** ≤70 °C for anything with a breadboard, jumper wires or a powered board on it. ≤350 °C for bare film samples. Anything hotter, and any furnace anneal, goes to a makerspace or lab. Check the surface with a thermocouple: the dial is not accurate. E7 uses an aluminium block and the block reading.
- **Outdoors (or at an open window with a fan blowing out, E7's ventilation rule), and the only mains item.** Plug it into a GFCI/RCD-protected outlet (ground-fault circuit interrupter / residual-current device) or a portable GFCI adapter. Use an outdoor-rated cord, fully unrolled, plug joint off the ground. Never in rain or dew, on wet ground, or with wet gloves. If it gets wet, unplug it at the wall first.
- **Fire.** Ceramic tile on a non-combustible surface. No solvent bottle within 1 m. Never heat or evaporate a flammable solvent on the plate. Keep an ABC dry-powder or CO2 extinguisher (never water) and a fire blanket within reach. Put up a "HOT" sign, and let the plate cool 30 minutes; it stays hot after the light goes off. Never leave it on unattended.
- **Wet samples.** A sample wet with an organic solvent (IPA, ethanol, acetone) never goes on a plate hotter than ~100 °C: dry it at room temperature first. Chips must have no solvent smell before they go on the plate. E7's water-based ammine ink has no organic solvent and is baked at 120-150 °C outdoors ([E7 §8](E7_make_your_own_oxide_transistor.md#8-procedure) step 13).
- **Nitrate-soaked paper** can burn fiercely once dry: rinse wipes with water and bag them wet.
- **Ultrasonic cleaner.** Solvent only in a capped glass jar standing in the water-filled tank, heater off; never pour solvent into the tank.
- **Hot chips.** Steel tweezers, never plastic-tipped. Cool chips on a second, room-temperature block; never lift the hot block off the plate. Let a chip cool before the next coat, or the ink boils and spatters ammonia.

---

## 5. Chemicals

Only E7 uses real chemistry. E8 adds none. The other guides use isopropyl alcohol, flux and silica gel only.

### 5.1 How to handle them

- **Before you buy:** read the SDS for the exact bottle you will buy; hazards differ between suppliers ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)). Many lab suppliers sell only to institutions; order through a makerspace, community lab or school, and ask them to store the bottle ([E7 §5](E7_make_your_own_oxide_transistor.md#5-parts)).
- **PPE (personal protective equipment):** indirect-vent chemical splash goggles (glasses do not seal against splashes); nitrile gloves, changed after any splash; a lab coat or long cotton sleeves (not polyester); closed shoes; glasses, not contact lenses, near ammonia.
- **First aid, set up before you open the ammonia:** rinse water within 10 seconds (a garden hose on gentle flow, or a 1 L eyewash bottle). Eyes: flush ≥15 minutes, eyelids open, then get medical help and take the SDS. Skin: remove contaminated clothing, rinse 15 minutes. Breathed in: fresh air; medical help if coughing continues. US Poison Control: 1-800-222-1222. Have a second person nearby the first time you make ink.
- **Quantities:** ≤20 mL of solution at a time ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment)).
- **Storage:** a locked box or cabinet, original labelled containers in a secondary tray, out of reach of children and pets. Oxidizers (nitrates) apart from flammables, ammonia, acids and bleach. Never a food fridge: chill inks in a dedicated, labelled cooler.

### 5.2 SDS table: every chemical named in any guide

| Chemical | Used in | Hazards (GHS codes as the guide cites them) | PPE | Ventilation | Storage | Disposal |
|---|---|---|---|---|---|---|
| Isopropyl alcohol (IPA), 99% | Cleaning flux and nodes: E1, E2, E4, E6, E7, E8 | H225 highly flammable (flash point ~12 °C), H319 eye irritation, H336 drowsiness [REPORTED, E1 S19] | Nitrile gloves, safety glasses | Ventilated room; away from the iron, flames and any heater, which must be off and cold ([E1 §4](E1_bit_on_the_bench.md#4-safety), [E6 §6](E6_retention_tail_real_dram.md#6-safety)) | Capped, away from heat; apart from oxidizers | Let small amounts evaporate outdoors away from ignition, or take to household hazardous waste (HHW); never down a drain ([E1 §4](E1_bit_on_the_bench.md#4-safety), [E4 §6](E4_femtoamp_leakage_bench.md#6-safety)) |
| Ethanol | Cleaning: E7 | H225, H319 [UNVERIFIED, standard SDS content, E7] | As IPA | Small volumes; never near the hot plate | Capped | Not stated in the guides: follow your SDS; never a drain |
| Acetone | Cleaning: E7 | H225, H319, H336 [UNVERIFIED, E7] | As IPA | Never near the hot plate ([E7 §8](E7_make_your_own_oxide_transistor.md#8-procedure) step 5) | Capped | Not stated: follow your SDS |
| Ammonium hydroxide, 28-30% NH3 | Dissolving ZnO: E7 | H314 severe burns and eye damage, H335, H400; some add H302, H318, H411 [REPORTED, E7 S28] | Splash goggles, nitrile gloves, coat, closed shoes | Outdoors upwind, or a ducted fume hood only (a range hood is not one) | Below 25 °C; vials ≤2/3 full; open chilled, slowly, pointing away; **never with bleach, acids or silver** | AMMONIA waste bottle (HDPE, ≤ half full, cool) to HHW; never a drain ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)) |
| Zinc oxide powder | Ink: E7 | Low acute toxicity; aquatic H410 on typical SDSs [UNVERIFIED] | Gloves, goggles | Weigh gently; make no dust | Locked chemical box | Zinc waste jar to HHW ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment)) |
| Zinc acetate dihydrate (optional) | Zinc source: E7 | H302, H318 serious eye damage, H411 [REPORTED, E7 S32] | Goggles | No dust | Locked box | Zinc waste jar to HHW |
| Zinc nitrate hexahydrate (upgrade) | IZO/IGZO inks: E7 | H272 oxidizer, H302, H315, H319 or H318, H335, aquatic H400/H410/H411 [REPORTED, E7 S29] | Goggles, gloves | Anneals release nitrogen oxides: outdoors, or an open window with a fan blowing out; stand upwind | Away from paper, solvents, heat and ammonia | NITRATE / METAL-SALT bottle to HHW |
| Indium(III) nitrate hydrate (upgrade) | In2O3, IZO, IGZO: E7 | H272, H315, H319; some add H335, H351 suspected carcinogen [REPORTED, E7 S30]; indium REL 0.1 mg/m³ | Gloves; never make dust or mist; wash hands | As zinc nitrate; never sprayed | As zinc nitrate | NITRATE / METAL-SALT bottle to HHW |
| Gallium(III) nitrate hydrate (upgrade) | IGZO: E7 | H272, H315, H319; some add H335 [REPORTED, E7 S31] | As indium nitrate | As zinc nitrate | As zinc nitrate | NITRATE / METAL-SALT bottle to HHW |
| Silver conductive paint (and silver epoxy) | Contacts: E7 | Flammable solvent carrier [UNVERIFIED: read your paint's SDS] | Gloves | Ventilate; no flame or hot plate nearby | **Away from ammonia and ammonia waste** | Wipes and brushes kept away from ammonia; otherwise not stated: follow your SDS |
| Household vinegar (5% acetic acid) | Etching ZnO: E7 step 17 | No hazard given in the guide | Goggles | - | - | Etch rinses go in the NITRATE / METAL-SALT bottle |
| Silica gel, orange or plain (cobalt-free) | Drying: E1, E2, E4, E7, E8 | Choking hazard for children and pets | - | - | Sealed sachets, out of reach | Household waste. Replace when spent, or regenerate at 100-120 °C for 2 h on a foil tray in an oven that never holds food ([E4 §6](E4_femtoamp_leakage_bench.md#6-safety)) |
| Solder and rosin flux | All builds | Flux fumes irritate the airways; leaded solder needs hand washing ([E1 §4](E1_bit_on_the_bench.md#4-safety)) | Safety glasses | Open window or fume fan | - | Not stated |
| Thermal paste | E8 heater block | None given in the guide | Gloves if your SDS asks | - | - | Not stated: follow your SDS |
| **Banned:** 2-methoxyethanol | (published inks) | H360FD, H226 [REPORTED, FIRST_PRINCIPLES S27] | Not at home | | | |
| **Banned:** blue silica gel (cobalt(II) chloride) | - | Carc. 1B (H350i), Repr. 1B (H360F) [REPORTED, E4 S24] | Not at home | | | |
| **Banned:** ceramic wool | - | Carc. 1B (H350i) when inhaled [REPORTED, E4 S22] | Not at home | | | |
| **Not used:** nitric acid; HF; bleach | - | Oxidizer, corrosive [UNVERIFIED, E7]; HF banned; bleach + ammonia gives toxic chloramine | Not at home | | | |

### 5.3 Waste and incompatible pairs

- **Two waste bottles, never combined.** AMMONIA (zinc-ammine ink and rinses) and NITRATE / METAL-SALT (nitrate inks, vinegar etch rinses). Together they make ammonium nitrate, an energetic oxidizer once dry ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)). Both go to HHW drop-off; neither goes down a drain.
- **Ammonia and silver.** Ammonia with silver compounds can form explosive "fulminating silver" on standing [REPORTED, standard laboratory hazard; UNVERIFIED this session]. Paint silver only on fully annealed chips, on a different table from the ink.
- **Ammonia and bleach or acids:** never mix.
- **Nitrates and paper or solvents:** keep apart; nitrate-soaked paper burns fiercely once dry.

---

## 6. Silicon, glass and other sharps

- **Cleaving wafers** (E7): inside a zip bag or on paper, wearing safety glasses. Handle chips with tweezers. Shards go in a labelled rigid container ("sharp silicon"); vacuum the floor afterwards ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)). Wear cut-resistant gloves and work over a tray; pick shards up with tape or a brush, never fingers ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment)).
- **Reed relays** (E2, E7, E8) have contacts in a thin glass tube. Bend leads only with pliers held between the glass and the bend ([E2 §4](E2_gain_cell_no_capacitor.md#4-safety)).
- **Clipped leads fly.** Safety glasses, and cover the lead with your hand as you cut ([E1 §4](E1_bit_on_the_bench.md#4-safety)).
- **Cut tin and swarf** (E4): see section 11.

---

## 7. Batteries, power supplies and pins

- **9 V batteries** (E1, E2, E4, E7, E8). A shorted 9 V battery gets hot and can start a fire. Tape or cap the terminals of spares; take batteries out of the circuit when you finish ([E1 §4](E1_bit_on_the_bench.md#4-safety)).
- **±9 V rails** (E2). One battery makes +9 V (minus to ground); one makes −9 V (its **plus** to ground: the red wire goes to ground, the black wire is the −9 V rail). Check −9 V with the meter before you connect anything. Connect each battery's ground terminal first and remove it last ([E2 §4](E2_gain_cell_no_capacitor.md#4-safety)).
- **27 V battery stacks** (three 9 V in series: E7's battery test, and E8 when it uses the E4 bench). All the 9 V rules apply to every battery in the stack. The stack stays under the 30 V ceiling. In E7 it feeds the gate only through a 1 MΩ resistor, which limits a short to ~27 µA [ESTIMATE] ([E7 §8](E7_make_your_own_oxide_transistor.md#8-procedure) step 14; [E8 §6](E8_your_own_oxide_gain_cell_memory.md#6-the-circuit)). Up to 27 V sits on the chip's substrate in E8: do not touch the chips while powered ([E8 §3](E8_your_own_oxide_gain_cell_memory.md#3-safety)).
- **Bench supply** (E7, E8, E5 fallback). Set the voltage your build needs and a 50 mA current limit *before* you connect: cheap supplies can overshoot at switch-on. E7's and E8's rig takes 30 V; the LM358 op-amp's absolute maximum is 32 V ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)). E5's MN3007 fallback takes ~15 V on its own fused rail, never 30 V ([E5 §6](E5_charge_river_bbd.md#6-safety)). Never connect a bench supply to a board's 5 V pin while that board is also on USB: it can back-feed the computer ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment)).
- **Voltage ratings of parts.** The ALD1106 is rated 10.6 V, so its wordline stays ≤10 V from a 9 V battery; never use the 12 V heater adapter for it ([E1 §4](E1_bit_on_the_bench.md#4-safety), [E2 §4](E2_gain_cell_no_capacitor.md#4-safety)). The 2N7000 gate is rated ±20 V: E8 caps its word line at 10 V in code and fits a 15 V Zener as a backstop ([E8 §3](E8_your_own_oxide_gain_cell_memory.md#3-safety)). 3.3 V parts such as the SDRAM die at 5 V ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment)).
- **Microcontroller pins take ≤3.3 V.** Check every divider with the meter before you connect an ADC pin. E5's 15 V MN3007 fallback needs its own fused rail and a ≥5:1 divider; the normal divider would put ~8.9 V on the pin ([E5 §6](E5_charge_river_bbd.md#6-safety)). A push-pull comparator must run from 3.3 V.
- **ADS1115 supply differs on purpose.** E4 powers it from 3.3 V, because the breakout's pull-ups would otherwise put 5 V on the Pico's pins ([E4 §5.1](E4_femtoamp_leakage_bench.md#51-circuit)). E7 and E8 power it from 5 V *behind a BSS138 level shifter*, because their amplifier swings to 5 V ([E7 §7](E7_make_your_own_oxide_transistor.md#7-build-the-t4-mini-smu-measurement-rig)). Never mix the two: a 5 V ADS1115 without the level shifter puts 5 V on the Pico.
- **Coils.** Fit the flyback diode across every relay coil ([E2 §4](E2_gain_cell_no_capacitor.md#4-safety)). Drive coils through a transistor or the ULN2003A, never straight from a GPIO pin ([E7 §7](E7_make_your_own_oxide_transistor.md#7-build-the-t4-mini-smu-measurement-rig)).
- **USB fast-charge meter** (E3's FNIRSI FNB58). Its trigger menu can raise USB to 9-20 V, and the Pico's input is rated 5.5 V. Never open that menu with the Pico attached; plug the meter into a computer port, not a fast charger ([E3 §4](E3_price_of_distance.md#4-safety)).
- **Other cells and stored energy.** Alkaline or NiMH cells, or a USB power bank; no loose lithium cells (18650, LiPo) without a protection board. Avoid large electrolytic banks; fit polarized capacitors the right way round, rated ≥1.5x the supply ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment)).

---

## 8. Static (ESD)

Electrostatic discharge (ESD) kills the parts, not you. The ADA4530-1 and LMC6001 electrometer inputs, the ALD1106, 2N7000s, JFETs, BBDs, the DRAM board and E7's TFT chips can all die from a spark too small to feel. Touch grounded metal (E4, E7 and E8: the grounded tin) before you handle them. Keep chips in antistatic bags until you fit them; hold boards by the edges. A wrist strap with its built-in 1 MΩ resistor is best ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment); every guide's Safety box).

---

## 9. Your computer and your data

- **Hardware.** A misplaced jumper can push 9-18 V back into your USB port, which can damage it or crash the computer and lose open work. Use a powered USB hub you can afford to lose, or a USB isolator (ADuM3160 type, about $15-30 [ESTIMATE]). Keep USB 5 V on its own labelled rail. Check every rail with the meter before you plug in USB, and save your work first ([E1 §4](E1_bit_on_the_bench.md#4-safety), [E2 §4](E2_gain_cell_no_capacitor.md#4-safety)).
- **Long runs.** Turn off sleep, hibernation and overnight update restarts (macOS: `caffeinate -i`; Linux: `systemd-inhibit`). Use a new file name for every run and `tee`, never `>`, which silently overwrites. Copy logs to a second drive daily ([E4 §7](E4_femtoamp_leakage_bench.md#7-procedure), [E5 §7](E5_charge_river_bbd.md#7-procedure), [E8 §7](E8_your_own_oxide_gain_cell_memory.md#7-procedure)). Delete old files from the Pico: its flash is small ([E1 §8](E1_bit_on_the_bench.md#8-data-sheet--log-template)).
- **E6's PC route (E6 §14 item 4, platform rank 5: raising tREFI on an ECC PC).** Relaxed refresh can corrupt memory, crash the operating system and damage files. Boot a live USB stick; disconnect or do not mount internal drives; save nothing important. If Windows uses BitLocker or Device Encryption, save the recovery key off the PC first (a BIOS change or CMOS reset can trigger recovery, and a live USB does not prevent it). To clear BIOS settings, unplug the PC at the wall, wait a minute, then use the board's clear-CMOS button or jumper; never open the power supply. After a memory change the first boot can stay black for minutes: wait 5 minutes before resetting. Do not add heaters inside a PC case ([E6 §14](E6_retention_tail_real_dram.md#14-other-platforms-notes)).

---

## 10. Cold runs

From [E1 §4](E1_bit_on_the_bench.md#4-safety) and [FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment):
- Seal the board in a zip bag with silica gel, closed around the USB cable with tape; keep it away from food and wipe the shelf afterwards. Never put an unbagged board in a freezer that holds food.
- In the family fridge, ≤3 h. Longer runs belong in a spare fridge with no food, or a picnic cooler with gel packs that do not touch the bag. Check the door still closes fully.
- No power bank inside: most switch off at the Pico's small current.
- Leave the bag closed for 30 minutes after you take it out, and let it reach room temperature before you open or power it. Never power a wet board.
- No freeze sprays, no liquid nitrogen, no dry ice in a closed container.

---

## 11. Soldering, drilling and cutting

- **Soldering** (all builds). The tip is ~350 °C: use a stand, keep the cord clear, never leave it hot and unattended, unplug it when done. Ventilate flux smoke (open window or fume fan). Prefer lead-free solder; wash your hands after leaded solder; no food or drink at the bench. Safety glasses ([E1 §4](E1_bit_on_the_bench.md#4-safety)).
- **Drilling** (E4's tin and block; E8's block, 2.5 mm drill and M3 tap). Clamp the work in a vise or with two clamps; never hold it by hand. Safety glasses. Sharp bit at low speed, a drop of oil on aluminium. Deburr every hole. Handle cut tin in work gloves and vacuum swarf rather than brushing it by hand ([E4 §6](E4_femtoamp_leakage_bench.md#6-safety)).

---

## 12. Children, pets and the household

- Keep children and pets out of the room while the iron, a heater, the hot plate or chemicals are out, and away from a long or heated run ([E1 §4](E1_bit_on_the_bench.md#4-safety), [E6 §6](E6_retention_tail_real_dram.md#6-safety), [E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)).
- Store small parts (SOT-23 parts are tiny), silica-gel packets, 9 V batteries and IPA out of reach: small parts and gel packets are choking hazards ([E1 §4](E1_bit_on_the_bench.md#4-safety), [E2 §4](E2_gain_cell_no_capacitor.md#4-safety), [E3 §4](E3_price_of_distance.md#4-safety)).
- Lock coin cells away: a swallowed coin cell can burn through tissue in hours; get emergency help at once if one goes missing [UNVERIFIED] ([FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment)).
- Keep pet birds in another part of the house during any heating step; they are very sensitive to fumes [UNVERIFIED].
- Chemicals live in a locked box, never in a food fridge ([E7 §3](E7_make_your_own_oxide_transistor.md#3-safety)).
- Tape long coax down or keep it on the bench: it is a trip hazard ([E3 §4](E3_price_of_distance.md#4-safety)).

---

## 13. Move this to a makerspace or a lab

| Step | Why | Source |
|---|---|---|
| Spray pyrolysis; UV-ozone or oxygen-plasma cleaning; sputtering or evaporation | Breathable metal-salt mist; mercury lamps; vacuum and high voltage | [E7 §3](E7_make_your_own_oxide_transistor.md#3-safety) |
| Anneals above your hot plate's rating, above 350 °C, in a furnace or in forming gas | Fire and gas hazards beyond a home plate | [E7 §3](E7_make_your_own_oxide_transistor.md#3-safety), [FIRST_PRINCIPLES §7](FIRST_PRINCIPLES.md#7-safety-for-every-experiment) |
| Any 2-methoxyethanol recipe; any acid stronger than vinegar; combustion inks | Reproductive toxin; corrosives; energetic reactions | [E7 §3](E7_make_your_own_oxide_transistor.md#3-safety) |
| E7 and E8 as a whole, ideally | They need the most care | [FIRST_PRINCIPLES §5](FIRST_PRINCIPLES.md#5-experiment-map) |
| Buying and storing ammonia and nitrates | Suppliers sell corrosives only to accounts | [E7 §5](E7_make_your_own_oxide_transistor.md#5-parts) |
| E4 option A: soldering the SOIC-8 ADA4530-1 | Fine pitch; best with a mentor, magnifier and flux | [E4 §4.1](E4_femtoamp_leakage_bench.md#41-bench-choose-one-electrometer-option) |
| Drilling E4's block without a vise | Use a makerspace drill press | [E4 §6](E4_femtoamp_leakage_bench.md#6-safety) |
| Your first surface-mount part (E2's SOT-23 JFET) | A makerspace can help | [E2 §6.1](E2_gain_cell_no_capacitor.md#61-one-cell-three-are-built-side-by-side-a-b-c) |
| E6 on a bare SDRAM chip (54-pin TSOP adapter) | Fine-pitch soldering | [FIRST_PRINCIPLES §5](FIRST_PRINCIPLES.md#5-experiment-map) |
| A commercial source-measure unit (it can output 200 V) | Set its limit to ≤30 V, or better, use one at a makerspace or university | [E7 §5](E7_make_your_own_oxide_transistor.md#5-parts) |
| DRAM Bender and DDR4 module studies | University lab equipment | [E6 §3](E6_retention_tail_real_dram.md#3-honest-scope) |

---

## 14. Where the guides disagreed, and what changed

**Fixed (the safer rule won):**
1. **Parallel heater wiring.** E1 said "series, never parallel"; E4 allowed parallel wiring (28.8 W) as a fallback. E4 now allows series only ([E4 §5.3](E4_femtoamp_leakage_bench.md#53-mini-hot-chuck-and-thermostat-only-for-runs-above-room-temperature)); its firmware comment says the same.
2. **Clearance from foam.** E1 put its heater plate on metal spacers ≥10 mm; E4's rule is ≥20 mm from foam for anything that can pass 60 °C; E6 gave no wall clearance. All three now use 20 mm ([E1 §6.5](E1_bit_on_the_bench.md#65-warm-box-heater-optional), [E6 §7 step 8b](E6_retention_tail_real_dram.md#7-build)).
3. **Improvised heaters.** FIRST_PRINCIPLES §2.7 suggested a hot plate with a PID controller or a reptile heat mat, with no hardware cut-outs. It now points to E4's and E6's heaters.
4. **Unattended heating.** E8 said only "stay nearby for the first heat-up". It now uses E4's rule: watch one full heated run first, with a smoke alarm in the room.
5. **Soldering a thermal fuse.** E8 allowed soldering 5 mm from the fuse body; E1, E4 and E6 say 10 mm. E8 now says 10 mm ([E8 §3](E8_your_own_oxide_gain_cell_memory.md#3-safety)).
6. **Regenerating silica gel.** E4 said "in an oven"; FIRST_PRINCIPLES §7 bans heating in anything that will touch food again. E4 now says an oven that never holds food, or replace the gel.
7. **Heater wiring.** Only E4 and E6 said to keep heater current off breadboards and jumper wires. E1 and E8 now say it too.
8. **Wet samples on the plate.** FIRST_PRINCIPLES §7 said no solvent-wet sample above ~100 °C, while E7 bakes fresh ink at 120-150 °C. The rule now says *organic* solvent; E7's ink is water-based.
9. **Bench-supply voltage.** An earlier draft of this file told every bench-supply user to set 30 V, including E5's ~15 V MN3007 fallback. Section 7 now gives each build its own voltage ([E5 §6](E5_charge_river_bbd.md#6-safety)).

**Different on purpose (kept):**
- Cut-out temperatures (55, 72, 80, 90, 91, 95, 110 °C) differ because the setpoints differ (45-85 °C); see section 3.1.
- E6's air cut-out opens at 80 °C, above the foam's ~75 °C rating. It is a backup: the stuck-on test already proves the air cannot pass 75 °C, and the switch resets itself.
- ADS1115 at 3.3 V (E4) vs 5 V behind a level shifter (E7, E8): section 7.
