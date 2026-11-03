# E7: Make your own oxide transistor

*Home-lab experiment E7, track T4 of the [dram-moonshot](../README.md) study. Written 2026-11-03. Prices are approximate as of November 2026; most are 2025-2026 listing snapshots. All code in [code/T4_oxide/](code/T4_oxide/) is reference code, **untested on hardware**. The physics backbone shared by all home experiments is [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md).*

| | |
|---|---|
| **What you make** | A thin-film transistor (TFT) whose channel is zinc oxide (ZnO) that you make from a water-based ink and a hot plate, below 400 °C |
| **What you measure** | Transfer and output curves. From them: threshold voltage (Vth), on/off ratio, subthreshold swing (SS), mobility (µ) and off-current (Ioff) |
| **Difficulty** | 4 of 5. The chemistry is simple; clean films and picoamp measurements take patience |
| **Time** | First proof (the battery test, section 8 step 14): 1-2 weekends. Full E7 if you are new to soldering: about 6-10 weekends for the picoamp rig, a spin coater, the chemistry and debugging (3-4 weekends if you have built electronics before). Later batches take an afternoon plus an overnight |
| **Cost tier** | $$$. First proof (battery test): about $410-550 plus a hot plate, or about $320 if you already own a multimeter and PPE. Full build: about $1,000 for materials and process tools, plus about $200 for the measurement rig ([BOM totals](#5-parts)). About $1,245 for E7, the rig and E8 together, or about $875 if a makerspace lends you a hot plate and spin coater |
| **Needs** | The [E4 femtoamp bench](E4_femtoamp_leakage_bench.md) (track T2) only for off-currents below about 1 pA |
| **Leads to** | [E8: your own oxide gain-cell memory](E8_your_own_oxide_gain_cell_memory.md) |

**Acronyms used here.** TFT = thin-film transistor. ESD = electrostatic discharge. GFCI/RCD = ground-fault circuit interrupter / residual-current device (a shock-protecting outlet). ALD = atomic layer deposition. MOSFET = metal-oxide-semiconductor field-effect transistor. IGZO = indium-gallium-zinc oxide. IZO = indium-zinc oxide. ZnO = zinc oxide. In2O3 = indium oxide. SiO2 = silicon dioxide. SMU = source-measure unit. TIA = transimpedance amplifier (a current-to-voltage converter). ADC/DAC = analog-to-digital / digital-to-analog converter. PWM = pulse-width modulation. SDS = safety data sheet. PPE = personal protective equipment. GHS H-codes are the standard hazard statements on an SDS (for example H314 = causes severe skin burns and eye damage). BEOL = back end of line, the wiring layers on top of a finished chip. RTN = random telegraph noise. 2T0C = two transistors, zero capacitors.

---

## 0. Why this experiment

Three of the study's strongest concepts rest on one device: an oxide-semiconductor transistor.

- **BEST BET, [hot-side memory](../dossiers/hot-side-memory.md):** 2T0C oxide gain cells stacked on a GPU, about 10x lower energy per bit moved than HBM (0.37 vs 3.95 pJ/bit) [STUDY].
- **MOONSHOT, [AND-stack](../dossiers/and-stack.md):** a 2-bit oxide cell in each tier of a 3D-NAND-style stack [STUDY].
- **[Charge-river](../dossiers/charge-river.md):** oxide charge-transfer devices [STUDY].

Why oxides could change how memory is made:
- **Low temperature.** They form at ≤400 °C, so they can be built on top of a finished chip (BEOL) [STUDY].
- **No crystal wafer as the channel.** The channel is a deposited film, not single-crystal silicon.
- **Very low leakage.** Their band gap is about 3x silicon's, so heat makes almost no free carriers (section 1.4).

**The claim you can test at home:** a working transistor *channel* can be made from a water-based metal-salt ink and a hot plate below 400 °C. The channel is the layer that must survive being built on top of a finished chip. Your gate and gate oxide are still a bought silicon wafer with ~1,000 °C thermal oxide, so E7 tests the low-temperature channel, not a fully low-temperature device.

**The claim you cannot test at home:** that a 0.01 µm² version leaks only attoamps (1 aA = 1e-18 A), and that the worst 1 in 10,000 devices does too. That is the study's biggest unknown ([decision.json](../research/stage3/decision.json)). Section 2 is honest about the gap and shows how this experiment gets you closer to the real test.

---

## 1. First principles

Every number here is printed by [`code/T4_oxide/expected_numbers.py`](code/T4_oxide/expected_numbers.py). Run it, change the `PLAN` values to match your device, and run it again.

### 1.1 The gate is a capacitor (Gauss's law)

Gate voltage above threshold puts charge into the channel:

> Q = Cox · (Vgs − Vth), with Cox = ε0 · εr / tox

| Gate oxide (SiO2, εr = 3.9) | Cox | Electrons per cm² at Vgs − Vth = 20 V |
|---|---|---|
| 100 nm | 34.5 nF/cm² | 4.3e12 |
| 230 nm | 15.0 nF/cm² | 1.9e12 |
| **300 nm (what you will use)** | **11.5 nF/cm²** | **1.4e12** |

[ESTIMATE: arithmetic.] A thinner oxide gives the same charge at a third of the voltage. You will use 300 nm because that is what you can buy cheaply, so you need 20-25 V on the gate.

### 1.2 Current is charge times velocity (the square law)

Electrons drift with velocity µ·E. Integrating along the channel gives the gradual-channel ("square law") equations:

> linear (small Vds): Id = (W/L) · µ · Cox · (Vgs − Vth − Vds/2) · Vds
> saturation (Vds ≥ Vgs − Vth): Id = (W/2L) · µ · Cox · (Vgs − Vth)²

Planning values: µ = 0.3 cm²/Vs, Vth = 8 V [ESTIMATE, from the literature in section 13].

| Route (section 4) | W/L | Id at Vgs = 15 V | Id at Vgs = 20 V | Id at Vgs = 24.5 V (rig maximum) |
|---|---|---|---|---|
| A: Pt test chip (W 1 mm, L 10 µm) | 100 | 8.5 µA | 24.9 µA | 47.0 µA |
| B: painted contacts (W 3 mm, L 100 µm) | 30 | 2.5 µA | 7.5 µA | 14.1 µA |

[ESTIMATE.] The rig's gate node tops out at 27 V, the LM358's guaranteed output on a 30 V supply [DATASHEET, S45], so Vgs max = 27 − 2.5 = 24.5 V.

**The battery test is different.** Section 8, step 14 uses wide painted stripes with a ~0.5 mm gap (W/L ≈ 6), the gate at 27 V and the drain at ~9 V. That is the linear regime: Id = µ·Cox·(W/L)·(Vov − Vds/2)·Vds = µ·(W/L)·1.50 µA. Expect about 2.6 µA at the planning µ, and 0.9-7 µA over µ = 0.1-0.9, which reads as 90-720 mV across a 100 kΩ shunt [ESTIMATE, `expected_numbers.py` E7-8]. Two paint blobs 1-2 mm apart (W/L ≈ 1-3) would give only 0.15-3.8 µA, which a meter with 1 µA resolution can miss.

### 1.3 Boltzmann statistics set the subthreshold swing

Below threshold, current rises by 10x for every SS volts:

> SS = ln(10) · (kT/q) · (1 + C_traps/Cox) ≥ 59.2 mV/decade at 25 °C (63.1 at 45 °C, 67.1 at 65 °C)

Home films on 300 nm SiO2 have many traps. Expect SS of 0.5-2 V/decade [ESTIMATE]. Turned around, SS tells you the trap density Dit = (SS/SS_ideal − 1)·Cox/q: 0.5 V/dec means ~5e11 and 1 V/dec means ~1.1e12 states/(cm²·eV) [ESTIMATE]. `iv_analysis.py` prints this.

### 1.4 The band gap removes the thermal leakage floor

Heat makes free carriers across the band gap:

> n_i = sqrt(Nc · Nv) · exp(−Eg / 2kT)

| Material | Eg | n_i at 27 °C | Thermal generation current, 1 µm depletion, 1 µs lifetime |
|---|---|---|---|
| Silicon | 1.12 eV | 8.9e9 cm⁻³ | 7e-8 A/cm² |
| ZnO | 3.37 eV | 3.2e-10 cm⁻³ | 3e-27 A/cm² |

[ESTIMATE; band gaps and masses are textbook values, UNVERIFIED this session; same physics as [FIRST_PRINCIPLES.md §2.8](FIRST_PRINCIPLES.md).] The ratio is about 3e19.

**What this means.** A silicon switch has a p-n junction, and the junction has a thermal-generation floor that doubles every ~8-10 °C. An oxide TFT has no p-n junction, and its intrinsic floor is about 1e19x lower. Its off-current is therefore set by three things: gate bias (subthreshold), defects, and stray paths. These are engineering problems, not physics limits. That is exactly why the study's biggest unknown is the defect tail, not the median.

**Your prediction.** With Vth = 8 V and SS = 1 V/dec, the channel current at Vgs = 0 should be about 6e-16 A [ESTIMATE]. That is far below your rig's ~1 pA floor. So the off-current you measure will be the floor of your setup (gate oxide, surfaces, cables), not the channel. Finding that floor, and pushing it down, is half the lesson.

### 1.5 Charge balance: can the gate empty the film?

To switch off, the gate must push every free electron out of the film:

> q · Nd · t = Cox · ΔV (Nd = donor density, t = film thickness)

| Nd (cm⁻³) | 5 nm film | 10 nm | 20 nm | 40 nm |
|---|---|---|---|---|
| 1e16 | 0.1 V | 0.1 V | 0.3 V | 0.6 V |
| 1e17 | 0.7 V | 1.4 V | 2.8 V | 5.6 V |
| 1e18 | 7.0 V | 13.9 V | 27.8 V | 55.7 V |
| 1e19 | 69.6 V | 139 V | 278 V | 557 V |

[ESTIMATE, 300 nm SiO2.] ZnO films are usually around 1e16-1e17, so they turn off easily. Undoped In2O3 can be around 1e18-1e19 [ESTIMATE], so it must be thinner than ~10 nm or alloyed with Ga or Zn. That is why industry uses IGZO rather than pure In2O3, and why this guide starts with ZnO. Because there are almost no holes (section 1.4), the film can sit fully depleted for as long as you like.

### 1.6 Chemistry and mass balance

- **Zinc-ammine ink.** ZnO dissolves in strong ammonia water as a zinc-ammine complex. Heating drives off ammonia and water and leaves ZnO. The film needs no organic solvent and leaves no carbon [REPORTED, S1-S3].
- **Indium nitrate ink (upgrade).** In(NO3)3 in water decomposes to In2O3, releasing nitrogen oxides (NOx). Hence the ventilation rule.
- **Film per coat.** Thickness ≈ wet film × concentration × molar volume. A 1-3 µm wet film of 0.1-0.2 M ink gives about 1.5-9 nm of dense oxide per coat [ESTIMATE]. Two to four coats give 10-20 nm.
- **Masses for 10 mL of 0.1 M ink:** 81.4 mg ZnO; 297.5 mg Zn(NO3)2·6H2O; 300.8 mg In(NO3)3 (anhydrous basis). For hydrated salts, use the molecular weight on your bottle. 28 wt% ammonia is ~14.8 M NH3, a large excess over 0.1 M zinc [ESTIMATE].

### 1.7 Expected results

| Quantity | Planning value [ESTIMATE] | Literature, solution oxides [REPORTED] |
|---|---|---|
| Mobility µ | 0.1-1 cm²/Vs (plan 0.3) | ZnO ammine 0.9 at 180 °C (S2); Al:ZnO ammine >5 at 180 °C, 3 at 120 °C (S1); Na:ZnO 1.84 at 300 °C (S4); aqueous In2O3 on SiO2-class 8.6 at 250 °C (S10); water-only IZO on SiO2 3.35 at 300 °C (S12) |
| Threshold Vth | +3 to +15 V (plan 8) | Depends on film; In-rich films go negative (depletion mode) |
| SS | 0.5-2 V/dec on 300 nm SiO2 | 90 mV/dec on thin high-k ZrOx (S8). Thin high-k gates are a lab step |
| On current Ion (Vgs 24.5 V, Vds 17.5 V) | Route A ~47 µA, route B ~14 µA | - |
| Off current Ioff | 1e-12 to 1e-10 A (rig floor ~1 pA) | pA-range is typical for solution oxide TFTs (S16, S18) |
| On/off ratio | 1e5-1e7 | 1e6-1e8 (S8, S10, S12, S15) |
| Hysteresis in air, no passivation | 0.5-5 V | "Scant" with Na doping (S4) |
| Bias-stress shift (PBTI) | Volts after 1,000 s at +20 V | 3.78 V for Y:ZnO (S15) |
| Off-current per µm of width | ~1e-15 A/µm (1 fA/µm) | Scaled vacuum IGZO: zA-aA levels (S44, [STUDY]) |

---

## 2. Honest scope

| What E7 proves | What E7 does NOT prove |
|---|---|
| A transistor-grade oxide channel can be made from a water-based ink at ≤350 °C, with no vacuum and no crystal wafer as the channel | That oxide cells reach attoamp leakage. Your device is ~1e4 µm² on 300 nm SiO2 and leaks pA, about a million times above aA |
| The physics in your own hands: square law, subthreshold swing, depletion, hysteresis, film carrier density (ZnO vs In2O3) | Anything about the 1e-4 tail. That needs ≥1e5 devices; you will have 5-20 (see `expected_numbers.py`, section E8-4) |
| A working measurement method (transfer/output curves and parameter extraction), the same one the study's Gate A+ uses | RTN. One trapped electron shifts your device's Vt by 0.14 µV, versus 1.9 mV for a 0.01 µm² device [ESTIMATE] |
| How In and Ga change a film, if you do the upgrade: In raises mobility, Ga lowers off-current | Stability under the study's hydrogen, thermal and bonding budget, or at 85-125 °C |
| A demo and a data package good enough to open doors (section 15) | That sputtered, industrial IGZO behaves like your solution film. It usually performs better |
| | A fully low-temperature device. Your gate stack is ~1,000 °C thermal SiO2 on a crystal wafer, bought. A stackable cell also needs a ≤400 °C deposited dielectric and gate (for example ALD Al2O3 or HfO2: a nanofab step, level 3) |

**How it scales up.**

| Level | Where | What it adds | What it costs |
|---|---|---|---|
| 1. Home (this guide) | Garage, kitchen table outdoors | First devices, curves, method | ~$410-550 plus a hot plate for the first proof; ~$1,245 for the full build |
| 2. Makerspace | Community lab with ventilation | Evaporated or sputtered Al contacts, oxygen plasma cleaning, better hot plates or a tube furnace, a microscope | Membership, typically tens to low hundreds of dollars a month [ESTIMATE] |
| 3. University nanofab, external user | NNCI sites such as Purdue Birck or Georgia Tech IEN | Photolithography (2-10 µm devices), ALD Al2O3 passivation and thin high-k gates, 400 °C forming-gas anneals, heated probe station, parameter analyzer. Hundreds of devices give the median and the 1-10% tail | Birck 2023 external for-profit: $51/day lab fee + $61/day cleanroom, plus tool hours (for example EBL $132/h) (S42) |
| 4. Sponsored run | The study's "Oxide Tail Statistics" lot | ≥1e5 cells of 0.01 µm², 85-125 °C, after the real bond budget: the 1e-4 tail | ~$220-280k in the judges' budgets [STUDY] |

---

## 3. Safety

> **SAFETY BOX: read all of it before you buy anything.**
>
> **Hard rules for this guide.**
> - No hydrofluoric acid (HF), ever, and nothing that contains it. Some rust removers contain HF. One famous home chip-maker used a store-bought rust remover as an acid source (S36). Do not.
> - No 2-methoxyethanol, the classic oxide-ink solvent. It is reprotoxic: H360FD, "may damage fertility; may damage the unborn child" (S33). If a recipe needs it, the recipe belongs in a university lab.
> - **No spray pyrolysis at home.** It turns metal salts into a hot mist you can breathe. NIOSH's recommended limit for indium compounds is only 0.1 mg/m³, and inhaled indium compounds have caused fatal lung disease in workers (S34). Spray only in a lab spray booth or fume hood.
> - No piranha, no RCA clean, no mercury UV lamps (so no UV-ozone at home), no combustion inks made with acetylacetone, and never heat a dried nitrate-plus-fuel residue.
> - Electricity: only USB, batteries, or a 0-30 V bench supply with its current limit set to 50 mA. No mains-voltage builds. The hot plate is a bought appliance; do not modify it.
> - Bench supply: set it to 30 V and 50 mA *before* you connect the rig. Cheap supplies can overshoot at switch-on, and the LM358's absolute maximum supply is 32 V [DATASHEET, S45].
> - **Hot plate outdoors** (the only mains item): plug it only into a GFCI-protected (RCD) outlet, or through a portable GFCI adapter. Use an outdoor-rated extension cord, fully unrolled, with the plug joint off the ground. Never use the plate in rain or dew, on wet ground, or with wet gloves. Keep the cord away from the ink table. If the plate gets wet, unplug it at the wall before touching it.
>
> **Chemicals: hazards from supplier SDSs, which differ between suppliers. Use the SDS for the bottle you actually buy.**
>
> | Chemical | Used for | GHS hazards (H-codes) | Main controls |
> |---|---|---|---|
> | Ammonium hydroxide, 28-30% NH3 | Dissolving ZnO | H314 severe burns and eye damage, H335 respiratory irritation, H400 aquatic toxicity; some add H302, H318, H411 (S28) | Outdoors or in a real ducted fume hood only. Splash goggles. Never mix with bleach (toxic chloramine gas) or acids. **Keep away from silver** (see Ammonia handling). Store below 25 °C |
> | Zinc oxide powder | Ink | Low acute toxicity; aquatic toxicity (H410 on typical SDSs) [UNVERIFIED] | Weigh gently; do not make dust |
> | Zinc acetate dihydrate (optional) | Alternative zinc source | H302, H318 serious eye damage, H411 (S32) | Goggles; no dust |
> | Zinc nitrate hexahydrate (upgrade) | IZO/IGZO inks | H272 oxidizer, H302, H315, H319 or H318, H335, aquatic H400/H410/H411 (S29) | Keep away from paper, solvents and heat |
> | Indium(III) nitrate hydrate (upgrade) | In2O3, IZO, IGZO | H272, H315, H319; some suppliers add H335 and H351 "suspected of causing cancer" (S30). Indium REL 0.1 mg/m³ (S34) | Never make dust or mist; gloves; wash hands |
> | Gallium(III) nitrate hydrate (upgrade) | IGZO | H272, H315, H319; some add H335 (S31) | As above |
> | Isopropanol, ethanol, acetone | Cleaning | Highly flammable (H225), eye irritation (H319), drowsiness (H336 for IPA and acetone) [UNVERIFIED, standard SDS content] | Small volumes. Never near the hot plate. Capped |
> | Silver conductive paint | Contacts | Flammable solvent carrier [UNVERIFIED, read your paint's SDS] | Ventilate; no flames or hot plate nearby. Never near ammonia ink or ammonia waste |
> | Nitric acid | **Not used in this guide** | Oxidizer, corrosive [UNVERIFIED] | If a recipe needs it, do that step in a lab |
>
> **PPE.** Indirect-vent chemical splash goggles (safety glasses do not seal against splashes); nitrile gloves, changed after any splash; a lab coat or long cotton sleeves; closed shoes. Wear glasses rather than contact lenses when you handle ammonia.
>
> **First aid. Set this up before you open the ammonia.**
> - Rinse water within 10 seconds: a garden hose on a gentle flow, or a 1 L eyewash bottle on the table.
> - Eye splash: flush for at least 15 minutes, holding the eyelids open, then get medical help and take the SDS with you.
> - Skin: take off contaminated clothing and rinse for 15 minutes.
> - Breathed in: move to fresh air. Get medical help if coughing or breathlessness continues.
> - US Poison Control: 1-800-222-1222. Have a second person nearby the first time you make ink.
>
> **Ammonia handling.**
> - Fill ink vials no more than 2/3 full. Open chilled vials while still cold, slowly, pointing away from you, outdoors. Warm, sealed ammonia vials can spray.
> - Store the stock bottle below 25 °C (not in a hot garage), and open it the same way.
> - **Never let ammonia meet silver.** Keep silver paint, silver-painted chips, paint brushes and wipes away from ammonia ink and ammonia waste. Ammonia plus silver compounds can form explosive silver nitride ("fulminating silver") on standing [REPORTED, standard laboratory hazard; UNVERIFIED this session]. Paint contacts only on fully annealed chips, on a different table from the ink.
>
> **Ventilation.**
> - Open, mix and spin the ammonia ink outdoors, upwind, on a stable table, or in a ducted fume hood. A kitchen range hood is not a fume hood.
> - Bakes and anneals release ammonia (zinc-ammine ink) or nitrogen oxides (nitrate inks). Run the hot plate outdoors under cover, or at an open window with a fan blowing out. Stand upwind.
>
> **Fire and heat.**
> - Hot plate on a ceramic tile on a non-combustible surface. No solvent bottles within 1 m while it is hot.
> - Never heat a solvent on the plate. Never leave the plate on unattended.
> - Keep an ABC extinguisher within reach. Put up a "HOT" sign and let the plate cool for 30 minutes.
> - Paper wipes soaked in nitrate solution can burn fiercely once dry. Rinse them with water and bag them wet.
> - **Ultrasonic cleaner:** put isopropanol only in a capped glass vial or jar standing in the water-filled tank, heater off. Never pour solvent into the tank.
> - Chips must be fully dry, with no solvent smell, before they go on the hot plate.
> - Hot chips: use steel tweezers, never plastic-tipped ones. Cool chips on a second, room-temperature block or tile; never lift the hot block off the plate. Let a chip cool to room temperature before the next coat, or the ink boils and spatters ammonia.
>
> **Sharp silicon.** Cleave wafers inside a zip bag or on paper, wearing safety glasses. Handle chips with tweezers. Put shards in a labelled rigid sharps container, such as a capped plastic bottle marked "sharp silicon". Vacuum the floor after cleaving.
>
> **ESD and the work area.** Touch the grounded tin before handling chips or the rig; the TIA's input is CMOS. Plug devices in with the rig at Vds = 0 (drain at VREF). Keep children and pets out of the work area while ink or the hot plate is in use.
>
> **Waste.**
> - Zinc-ammine ink leftovers and their rinses go in the **AMMONIA** bottle: labelled HDPE, no more than half full, kept cool.
> - Nitrate inks (In, Ga, Zn nitrate) and vinegar etch rinses go in the **NITRATE / METAL-SALT** bottle: "Zn/In/Ga salt waste: oxidizer, toxic to aquatic life".
> - Never combine the two bottles: together they make ammonium nitrate, an energetic oxidizer once dry. Never pour either down the drain (H400/H410/H411).
> - Keep ammonia and ammonia waste away from silver paint, silver-paint wipes and brushes, and any silver salt.
> - Take both bottles to your local household hazardous waste (HHW) drop-off.
>
> **Storage.**
> - Use a locked box or cabinet out of reach of children and pets. Keep the original labelled containers in a secondary tray.
> - Keep oxidizers (nitrates) apart from flammables (solvents, paint) and from ammonia, acids and bleach.
> - Never use a food fridge. Chill inks in a dedicated cooler with ice packs, labelled "chemicals, not food".
>
> **Move these steps to a makerspace or university lab:** spray pyrolysis; UV-ozone or oxygen-plasma cleaning; sputtering or evaporation; anneals above your hot plate's rating or in forming gas; any 2-methoxyethanol recipe; any acid stronger than household vinegar; combustion inks.

---

## 4. Choose your route

| | Route A: pre-patterned Pt test chips | Route B: bare wafer + painted contacts (**recommended first**) | Route C: B + makerspace metal contacts |
|---|---|---|---|
| Substrate and gate | Ossila S403A1: p-doped Si, 300 nm SiO2, 100 nm Pt on 5 nm Ti, 20 electrode pairs, W = 1 mm, L = 2-10 µm (S21) | p++ Si (0.001-0.005 Ω·cm), 300 nm thermal SiO2, 100 mm wafer cut into ~60 chips (S22) | As B |
| Contacts | Bottom contacts, already there | Top contacts after the anneal: silver paint over a thin wire used as a mask, so L = wire diameter (50-100 µm) | Evaporated or sputtered Al or Ti/Au through a shadow mask |
| Cost | $225, or £150 in the ordering table: the listing conflicts and the pack size is unconfirmed [UNVERIFIED] (S21) | $109.95 for the wafer (S22) | B plus makerspace fees |
| Pros | Micrometre channels; reusable; no contact painting | Cheapest; contacts never see the anneal; forgiving | Best contacts |
| Cons | Pt has a high work function, so it may form a contact barrier on ZnO (no direct data found) [UNVERIFIED]. Anneal tolerance not confirmed: Ossila says the contacts survive sonication and plasma, but gives no temperature (S21) [UNVERIFIED]. Exposed Ti edges can inject charge (S21). Needs a probe holder or a matching test board, not priced here [UNVERIFIED]. Route B is the recommended path | Silver can also form a contact barrier; `iv_analysis.py output` flags this. W and L are less exact | Needs makerspace access |

Ossila's older gold-electrode chips are discontinued, and their bare 300 nm oxide substrates (S146) cost $598 (S21). The MTI wafer above is the cheaper route.

---

## 5. Parts

Tags: [REPORTED] = vendor listing or search snippet; [ESTIMATE] = typical street price, not checked this session. Totals come from `expected_numbers.py`.

**Substrate, chemicals and consumables**

| Part | Spec that matters | Example part number | Approx USD | Where |
|---|---|---|---|---|
| Thermal-oxide wafer | p++ Si, 0.001-0.005 Ω·cm, 300 nm SiO2, 100 mm | MTI "thermal oxide wafer 300 nm SiO2 on Si(100), p-type, 0.001-0.005 Ω·cm" | 110 [REPORTED, S22] | mtixtl.com; UniversityWafer #1583 (quote) |
| or Pt test chips (route A) | 300 nm SiO2, Pt/Ti, L 2-10 µm | Ossila S403A1 | 150-225 [REPORTED, conflicting, S21] | ossila.com |
| Diamond scribe pen | Carbide or diamond tip | Any "diamond scribe" | 12 [ESTIMATE] | Hardware or lab suppliers |
| Zinc oxide | ≥99.9%, low metal impurities | Sigma-Aldrich 204951 (99.999%, 25 g) | 181 [REPORTED, S25]; 99.9% grades ~40 [ESTIMATE] | sigmaaldrich.com; Fisher |
| Ammonium hydroxide | 28-30% NH3, ACS reagent, 500 mL | Sigma AX1303; RICCA 72-976; Thermo 423305000 | 46-67 [REPORTED, S26] | Sigma, Genesee, Fisher |
| Syringe filters + syringes | Hydrophilic, 13 mm, 0.45 µm: PES, nylon or hydrophilic PTFE (plain PTFE is hydrophobic and will not pass a water ink); 3-5 mL Luer-lock syringes | Any | 25 [ESTIMATE] | Lab suppliers |
| Glass vials | 10-20 mL, PTFE-lined caps | Any | 15 [ESTIMATE] | Lab suppliers |
| Distilled or DI water | 1 gallon | Any | 2 [ESTIMATE] | Grocery store |
| Isopropanol | ≥99% | Any | 10 [ESTIMATE] | Hardware store |
| Silver conductive paint | Fast-drying, brushable | MG Chemicals 842AR (or similar) [UNVERIFIED part spec] | 25 [ESTIMATE] | Electronics distributors |
| Mask wire | 50-100 µm, straight (tungsten, nichrome or nylon monofilament) | Any | 10 [ESTIMATE] | Hobby or lab suppliers |
| Kapton tape | High-temperature polyimide | Any | 8 [ESTIMATE] | Electronics suppliers |
| Silica gel packs | For the dry, dark measurement tin | Any | 5 [ESTIMATE] | Hardware store |
| Eyewash bottle | 1 L, sterile eyewash or saline | Any | 12 [ESTIMATE] | Pharmacy, safety suppliers |
| Battery-test kit | 4× 9 V batteries with snap clips; 1 MΩ, 100 kΩ and 10 kΩ resistors; crocodile leads | Any | 20 [ESTIMATE] | Any |

**Buying the chemicals.** Most lab suppliers (Sigma-Aldrich/MilliporeSigma, Fisher, Thermo) sell only to verified business or institutional accounts and will not ship corrosives to a home address [REPORTED, S48]. 28-30% ammonia ships as UN2672, Class 8 (corrosive), usually with a hazmat fee [ESTIMATE]. Your options:
- order through a makerspace, community lab or school that has an account, and ask them to store the bottle;
- or use an education or hobby supplier that sells to individuals, after confirming that it ships to you.

Buy the smallest ammonia bottle offered: 100-250 mL is plenty. Zinc oxide (99.9%) is not hazmat and is easy to buy.

**Upgrade chemicals (In2O3, IZO, IGZO): about $350 more**

| Part | Spec | Example | Approx USD | Where |
|---|---|---|---|---|
| Indium(III) nitrate hydrate | 99.99%, 10 g | Thermo 225185-10G listing | 163 [REPORTED, undated listing, S27] | Thomas Scientific, Fisher, Sigma |
| Zinc nitrate hexahydrate | ≥98%, 100 g | Any reagent grade | 40 [ESTIMATE] | Lab suppliers |
| Gallium(III) nitrate hydrate | 99.9%, 5-10 g | Sigma 289892 | ~150 [ESTIMATE] | Sigma, Fisher |

**Process tools**

| Part | Spec | Example | Approx USD | Where |
|---|---|---|---|---|
| Hot plate | Digital, ceramic top, ≥350 °C | Benchmark H3770-H, 7×7 in, max 380-400 °C (listings disagree) | 274-302 [REPORTED, S23] | Genesee, Global Industrial |
| Thermocouple meter | K-type, with a bead probe | Any | 25 [ESTIMATE] | Electronics suppliers |
| Aluminum block | 50×50×6 mm, to even out plate temperature | Any offcut | 5 [ESTIMATE] | Metal supplier |
| Spin coater | 1,000-4,000 rpm, lid, timer | DIY: brushless motor + controller + Pico, or open designs such as Maasi (<€100 goal) or Hackaday 192036 | 50-100 parts [REPORTED goal, S24]; commercial from ~€500 (S24) | DIY; Ossila, Instras |
| Scale | 0.001 g resolution | "Jewelry milligram scale" | 30 [ESTIMATE] | Online |
| USB microscope | 50-200x, with a ruler to calibrate | Any | 40 [ESTIMATE] | Online |
| Ultrasonic cleaner (optional) | 0.5-2 L; water only in the tank (solvent stays in a capped jar) | Any | 40-80 [ESTIMATE] | Online |
| Portable GFCI adapter (if your outdoor outlet is not GFCI/RCD-protected) | 15 A, outdoor rated | Any | 15 [ESTIMATE] | Hardware store |
| PPE | Splash goggles, nitrile gloves, lab coat | Any | 55 [ESTIMATE] | Lab or hardware suppliers |

**T4 mini-SMU measurement rig (section 7): about $200**

| Part | Spec | Example part number | Approx USD | Where |
|---|---|---|---|---|
| Microcontroller | RP2350, MicroPython | Raspberry Pi Pico 2 | 5 [REPORTED, S40] | Raspberry Pi resellers |
| 16-bit ADC | 860 samples/s, programmable gain, I2C | Adafruit 1085 (ADS1115) | 14.95 [REPORTED, S39] | adafruit.com, Mouser |
| TIA op-amp ×2 | CMOS input, ~20 fA typical bias, ≤15.5 V supply, **A grade: Vos ≤0.75 mV** | TI LMC6482AIN (DIP-8). Do not use LMC6482IN (3 mV max) | 4 each [ESTIMATE]; specs [DATASHEET, S38] | Digi-Key, Mouser |
| High-voltage op-amp ×2 | Single supply, 32 V absolute maximum; output high 27 V min / 28 V typ at V+ = 30 V, RL 10 kΩ | LM358 [DATASHEET, S45] | 0.5 each [ESTIMATE] | Any |
| 2.5 V reference | Shunt reference | LM4040-2.5 [UNVERIFIED spec] | 1 [ESTIMATE] | Any |
| Reed relays ×3 | 5 V coil (~500 Ω), SIP, internal diode; insulation ≥1e12 Ω; an internal electrostatic shield pin if available | e.g. Coto 9007-05-00 (5 V, 500 Ω coil [REPORTED, S47]; shield not confirmed) | 3 each [ESTIMATE] | Digi-Key, Farnell |
| Relay driver | Darlington array, 3.3 V-logic inputs, built-in coil diodes | ULN2003A (DIP-16) [DATASHEET, S50] | 1 [ESTIMATE] | Any |
| I2C level shifter | 2-channel, BSS138-based, 3.3 V ↔ 5 V | Any "BSS138 bi-directional level shifter" board | 4 [ESTIMATE] | Any |
| Capacitors | 1 µF film ×6 (PWM filters), 100 nF ×8 (decoupling, monitor pins), 10 µF/50 V ×2, 10 pF C0G ×2 | Any | 6 [ESTIMATE] | Any |
| Resistors | 100 MΩ (glass or thick film), 1 MΩ, 10 kΩ 0.1% (TIA); 82 kΩ, 51 kΩ, 15 kΩ, 10 kΩ, 2.2 kΩ, 1 kΩ, 100 kΩ, 1 MΩ (section 7 table) | Any | 12 [ESTIMATE] | Digi-Key, Mouser |
| PTFE standoffs | For the TIA input node | Any | 5 [ESTIMATE] | Online |
| Bench supply | 0-30 V, current limit | Any | 65 [ESTIMATE] | Online |
| Metal tin | Cookie tin: dark box and shield | Any | 15 [ESTIMATE] | Kitchen |
| Multimeter | µA range | Any | 30 [ESTIMATE] | Any |
| Perfboard, shielded wire, BNC | - | Any | 20 [ESTIMATE] | Any |

A commercial SMU is an alternative. Used Keithley 2400 units were listed at about $3,000-3,950 in 2025, and a dealer listed one at $3,999 (S37). It can output 200 V, so set its source limit to ≤30 V, or better, use one at a makerspace or university.

**Totals [ESTIMATE].** Materials and process tools ~$997; rig ~$199; E8 add-on ~$49 (E8 guide). E7 + rig + E8: ~$1,245, or ~$875 if a makerspace lends the hot plate and spin coater. First proof (through the battery test): ~$406-547 plus a hot plate (~$321 if you already own a multimeter and PPE). All from `expected_numbers.py`.

---

## 6. Tools needed

Splash goggles, gloves and lab coat; tweezers (fine steel for hot chips; plastic-tipped for cold chips only); diamond scribe; soldering iron; wire strippers; multimeter; a laptop with Python 3 + numpy and `mpremote` (`pip install mpremote`); a small outdoor table; a timer; a marker and labels. For E8's heater block: a drill with a 2.5 mm bit and an M3 tap (or M3 nuts).

---

## 7. Build the T4 mini-SMU (measurement rig)

A source-measure unit sets a voltage and measures a current. You need two voltage sources (gate and drain) and one very sensitive ammeter (the TIA). The pin list is also in the header of [`t4_hw.py`](code/T4_oxide/t4_hw.py).

```
 Pico GP0 --PWM--> 15k/1uF/15k/1uF (2 poles, ~10 Hz) --> LM358 x9.2 (30 V supply) --+--> 100 kohm --> GATE  (0..27 V)
                                                                                     +--> 1 Mohm/100 kohm --> Pico ADC0 (gate monitor)
 Pico GP2 --PWM--> same filter --> LM358 x6.1 --> 10 kohm --> DRAIN (0..20 V) --> 1 Mohm/100 kohm --> Pico ADC1 (drain monitor)
                                                                  TFT channel
 SOURCE --------------------------> TIA (-) input  [LMC6482AIN on 5 V; (+) input at VREF = 2.5 V]
                                     feedback: 100 Mohm || 10 pF always; relay K1 adds 1 Mohm; relay K2 adds 10 kohm
 TIA output --1 kohm--> ADS1115 AIN0;  VREF --1 kohm--> AIN3;  current = -(AIN0 - AIN3 - offset) / Rf
 ADS1115 on +5 V  <--BSS138 I2C level shifter-->  Pico GP4/GP5
 Pico GP10 / GP11 / GP14 --> ULN2003A --> relay coils K1 / K2 / K3 (other coil end at +5 V)
```

**Component values** [ESTIMATE unless tagged]:

| Block | Parts and values | Why |
|---|---|---|
| PWM filters (GP0, GP2, GP6) | GP pin → 15 kΩ → 1 µF film to GND → 15 kΩ → 1 µF film to GND → LM358 (+) input | ~10.6 Hz per pole; cuts the 2 kHz PWM ripple by roughly 35,000x |
| Gate amplifier, gain 9.2 | LM358 non-inverting: Rf 82 kΩ (output to − input), Rg 10 kΩ (− input to GND) | 1 + 82/10 = 9.2. The output clips at 27-28 V on a 30 V supply [DATASHEET, S45] |
| Drain amplifier, gain 6.1 | Rf 51 kΩ, Rg 10 kΩ | 1 + 51/10 = 6.1, so 3.3 V of PWM gives ~20 V |
| LM358 power | V+ from the bench supply (30 V), V− to GND; 100 nF + 10 µF/50 V at the pins | Absolute maximum 32 V [DATASHEET, S45] |
| Series resistors | 100 kΩ to the gate; **10 kΩ** to the drain | Gate: limits current if the oxide breaks down. Drain: a drain-source short then feeds ≤1.4 mA into the TIA's input clamp, under the LMC6482's ±5 mA absolute maximum [DATASHEET, S38]; 1 kΩ would give 14 mA (`expected_numbers.py` E7-9) |
| Monitors | 1 MΩ/100 kΩ divider (÷11) and 100 nF from each Pico ADC pin to GND. Gate monitor at the LM358 **output**, before the 100 kΩ. Drain monitor at the DRAIN node, after the 10 kΩ | No DC current flows through the gate's 100 kΩ, so the gate node equals the monitored voltage. The drain monitor records the true Vds after the 10 kΩ's drop (0.5 V at 50 µA) |
| VREF | LM4040-2.5 fed from +5 V through 2.2 kΩ (~1.1 mA); 10 µF ‖ 100 nF across it | Feeds the TIA's (+) input and ADS AIN3 |
| TIA | LMC6482AIN on +5 V/GND, 100 nF at its pins. (+) = VREF. Feedback 100 MΩ ‖ 10 pF; K1 adds 1 MΩ, K2 adds 10 kΩ | Ranges in the table below |
| Relay drive | K1, K2 (and K3 for E8) coils between +5 V and ULN2003A outputs 1-3. ULN2003A inputs from GP10, GP11, GP14; pin 8 to GND; pin 9 (COM) to +5 V. Shield pins, if any, to VREF (K3: to the WBL) | A 5 V reed relay needs ~3.75 V to close; a 3.3 V GPIO pin cannot drive it reliably [ESTIMATE, S47]. **Never drive a coil straight from a GPIO** |
| ADC | ADS1115 board on +5 V (VBUS) and GND. I2C through a BSS138 level shifter (low side 3.3 V, high side 5 V). 1 kΩ in series with each AIN | The TIA output swings 0-5 V; the ADS inputs must stay within its supply + 0.3 V [DATASHEET, S49]. **Never run the ADS1115 at 3.3 V with this TIA.** The level shifter makes this safe on a Pico or a Pico 2 |
| Ground | One star point: bench-supply negative, Pico GND, ADS GND and the tin meet there | Avoids ground loops at the pA level |

**Build order: test each stage before the next.**
1. **Power and VREF.** Pico on USB, bench supply off. Measure +5 V (VBUS) and VREF: 2.50 V ± 0.5%. Type your measured VREF into `CFG["vref"]` in `t4_hw.py`.
2. **Amplifiers.** Set the bench supply to 30 V and 50 mA, *then* connect it. Copy the code (`mpremote cp code/T4_oxide/t4_hw.py code/T4_oxide/pico_smu.py :`). With **no device connected**, calibrate: `mpremote exec "import t4_hw as h; h.calibrate_dacs()"`. It writes `dac_cal.json` to the Pico, and every later run loads it. Then check the gate node with the multimeter: `mpremote exec "import t4_hw as h; r=h.make_rig(); r.set_gate(10); h.sleep_ms(30000)"` should hold 10 V for 30 s. Repeat at 0 and 20 V.
3. **TIA.** Floor test (section 8, step 3) with nothing connected. Then put a 100 MΩ test resistor from DRAIN to the TIA input and run `mpremote exec "import t4_hw as h; r=h.make_rig(); r.zero_offset(); r.set_drain(3.5); h.sleep_ms(3000); print(r.read_current())"`. That is Vds = 1 V across 100 MΩ, so expect 10 nA ± the resistor's tolerance.
4. **Relays.** Swap in a 1 MΩ test resistor. Drain at 3.5 V gives 1 µA: you should hear K1 click and see range `mid`. Drain at 12.5 V gives 10 µA: range `lo`.

Key ideas:
- **The source sits at 2.5 V, not 0 V.** That lets the TIA run from one 5 V supply and gives you −2.5 V of gate drive for free. So Vgs = V(gate) − 2.5 V, from −2.5 to about +24.5 V (the LM358's output tops out at 27-28 V on a 30 V supply [DATASHEET, S45]), and Vds = V(drain) − 2.5 V, up to 17.5 V.
- **Three current ranges.** These are the numbers you can expect:

| Range | Full scale | Step size (finest) | Thermal noise of Rf (10 Hz) |
|---|---|---|---|
| 10 kΩ | 200 µA | 6.2 nA (0.78 nA) | 4 pA |
| 1 MΩ | 2 µA | 63 pA (7.8 pA) | 0.4 pA |
| 100 MΩ | 20 nA | 0.63 pA (78 fA) | 41 fA |

[ESTIMATE; ADS1115 ±2.048 V and ±0.256 V ranges.] You need 8 decades, from ~1e-4 A on to ~1e-12 A off. Below about 1 pA, use the [E4 femtoamp bench](E4_femtoamp_leakage_bench.md) (track T2).
- **Zero the offset.** The op-amp's input offset voltage Vos shows up as a constant current Vos/Rf: about 1.1 pA typical and up to 7.5 pA for an LMC6482AI on the 100 MΩ range, and 30 pA for a non-A part [DATASHEET, S38; `expected_numbers.py` E7-9]. That is as big as the floor you want. So every sweep starts with `zero_offset()`: gate node 0 V and drain at VREF (Vds = 0), so no current can flow. The code averages 32 readings and subtracts the result from every later reading. Relay coil-to-contact leakage on the 100 MΩ range is constant, so the same step removes it.
- **Protect the gate.** The 100 kΩ series resistor limits the current if the oxide breaks down. The gate monitor sits before it, so no DC current flows through it.
- **Guard the TIA input.** Solder the TIA input node in the air or on a PTFE standoff, not on the perfboard. Keep it short, inside the grounded tin. Clean off flux with isopropanol.

---

## 8. Procedure

**A. Practice and rig check (one evening)**

1. Run the software checks on your computer:
   `python3 code/T4_oxide/expected_numbers.py`, `python3 code/T4_oxide/iv_analysis.py --selftest`, then the full pipeline on a simulated TFT: `python3 code/T4_oxide/pico_smu.py --sim --mode transfer --out sim.csv`, `python3 code/T4_oxide/pico_smu.py --sim --mode gleak --out sim_gleak.csv` and `python3 code/T4_oxide/iv_analysis.py transfer sim.csv --gleak sim_gleak.csv --svg sim.svg`. The simulated device should give µ ≈ 0.4, Vth ≈ 7 V, SS ≈ 0.9 V/dec. Add `--no-zero` to the first command once to see a 4.5 pA offset error appear in Ioff.
2. Build the rig (section 7) in the order given there, testing each stage. The bench supply is set to 30 V and 50 mA before it is connected.
3. **Floor test.** With nothing connected to the TIA input: `mpremote exec "import pico_smu; pico_smu.run('floor')" > floor.csv`. The first number it prints is your offset: mostly the op-amp offset voltage divided by 100 MΩ, about 1 pA typical and up to 7.5 pA for an LMC6482AI [DATASHEET, S38]. The code subtracts it. The scatter (standard deviation) of the corrected readings is your floor, and it should be ≤0.3-1 pA. Record both.

**B. Substrates (one afternoon)**

4. **Cleave.** Wearing safety glasses, scratch a 2 mm nick at the wafer edge on the polished side. Place the wafer nick-side up over a straight edge (a slide or ruler) inside a zip bag and press gently on both sides. Make strips, then ~10×10 mm chips. Label chips on the back with a scribe.
5. **Clean.** Wash with dish soap and warm water, rinse with distilled water, then rinse with isopropanol. Optional: put the chips and a few mL of isopropanol in a capped glass jar, and stand the jar in the water-filled ultrasonic tank (heater off) for 5 minutes, outdoors or at an open window, with no flame or hot plate within 3 m. Never pour solvent into the tank. Let the chips dry completely, standing on edge. Do not use acetone near the hot plate.
6. **Bake-clean.** The chips must be fully dry, with no solvent smell. Then 300 °C for 10 minutes on the hot plate, outdoors or at the window. This burns off organics so the water-based ink wets the oxide. Let the chips cool on a second, room-temperature aluminum block or tile; never lift the hot block off the plate.
7. **Check temperature.** Put the thermocouple bead on the aluminum block on the plate. Note the difference between setpoint and block reading at 150, 250 and 300 °C. Use the block reading from now on.

**C. ZnO ink: zinc-ammine route (outdoors, PPE on)**

8. Weigh 81 mg of ZnO into a clean vial (0.1 M in 10 mL). Halve or double everything as needed.
9. Outdoors, goggles on, rinse water ready, add 10 mL of 28-30% ammonium hydroxide with a plastic syringe. Use a vial big enough to stay no more than 2/3 full. Cap tightly and shake.
10. Chill the sealed vial in the labelled ice-pack cooler for several hours to overnight, shaking now and then. ZnO dissolves slowly, and cold helps (S5). The ink should become clear. Open the vial while it is still cold, slowly, pointing away from you.
11. Just before use, goggles on, filter it through a hydrophilic 0.45 µm (or 0.2 µm) syringe filter on a Luer-lock syringe into a fresh vial. Point the filter down into the vial and push slowly. If it will not flow, stop and use a new filter; never force it. Do not use cloudy ink. Use it within about a day, because ammonia escapes and zinc falls out of solution [ESTIMATE].

**D. Film**

12. **Coat.** Put the chip on the spin coater chuck (double-sided Kapton tape or a pocket). Close the lid. Drop on 40-60 µL of ink, enough to cover the chip, and spin at 3,000 rpm for 30 s [ESTIMATE; one paper used 3,500 rpm for 30 s, S5]. No spin coater? Drop-cast 5-10 µL and let it dry at 60 °C. The film will be thicker and less even, but it can work.
13. **Bake.** Immediately bake at 120-150 °C for 5 minutes, then anneal at 300 °C (block reading) for 30-60 minutes, outdoors or ventilated. Papers anneal ammine ZnO from 150-180 °C up to 400 °C, often at 300 °C for about an hour (S1, S2, S5). Repeat coat-and-anneal 2-4 times. Before each new coat, move the chip with steel tweezers to the cool block and let it reach room temperature (2-3 minutes): ink on a hot chip boils and spatters ammonia. Then do a final 60-minute anneal at 300-350 °C (stay under your plate's rating). Turn the plate off and let the chips cool on it.

   Make several chips at different final anneal temperatures (200, 250, 300 and 350 °C). The trend in Vth and mobility is the most informative result you will get.

**E. Contacts (route B) and isolation**

14. **Quick battery test: your first proof (about 1 hour).** Do it indoors, in dim light, with the chip under an opaque cup: daylight makes ZnO conduct even at 0 V gate. Use a fully annealed chip, and paint on a different table from any ammonia.
    - (a) **Moat first.** With the diamond scribe, scratch a closed square moat, about 6 × 6 mm, through the film in the middle of the chip. The film inside it must not reach any cleaved edge, because a cleaved edge is bare p++ silicon: the gate.
    - (b) **Two stripes.** Inside the moat, paint two silver stripes about 3 mm long, side by side, with a gap of about 0.5 mm (W/L ≈ 6). If you can, use the wire mask of step 15 instead (L = 50-100 µm gives 5-10x more current, so read the shunt on the 20 V range). Keep the paint at least 1 mm inside the moat. Let it dry for 30 minutes.
    - (c) **Gate.** Scratch through the oxide on the back of the chip and paint a silver spot there.
    - (d) **Wiring.** Three 9 V batteries in series (27 V) → 1 MΩ → gate. One 9 V battery (+) → 10 kΩ → drain stripe. Source stripe → 100 kΩ shunt → the joined battery negatives (0 V). Read the voltage across the 100 kΩ with the multimeter on its 2 V (or 200 mV) DC range: 1 mV = 10 nA. The drain must be positive (n-type channel).
    - (e) **Expected** [ESTIMATE, `expected_numbers.py` E7-8]: about 0.9-7 µA, i.e. 90-720 mV (planning value ~260 mV).
    - (f) **Three readings.** Wait 2 minutes after each change.

      | Reading | Gate lead | Drain battery | Should read |
      |---|---|---|---|
      | A | clipped to 0 V | connected | under ~1 mV |
      | B | 27 V | connected | ≥10 mV (0.1 µA) and ≥10x reading A; typically 90-720 mV |
      | C: control, required | 27 V | **unclipped** | falls back to the A level |

      Then reconnect the drain: reading B should come back.
    - (g) **Verdict.** Only low A, high B and low C means transistor action: a current that needs **both** the gate at 27 V **and** the drain battery. If C stays high, the current is gate current, not a transistor: film or paint touching a cleaved edge, a scratch through the gate oxide, or a pinhole. Without a moat that path alone can give 0.6-4.8 µA, exactly the size of a real signal [ESTIMATE, E7-8]. Re-scribe the moat, repaint and repeat. If the chip passes this control, you have very likely made a transistor. The rig's gate-leakage test (step 20) confirms it.
15. **Pads over a wire mask.** Tape a 50-100 µm wire tightly across the chip with Kapton tape at both ends, outside the chip. Paint silver on both sides, overlapping the wire by about 1 mm, keeping the paint ≥1 mm from every chip edge. A cleaved edge exposes bare silicon, which is the gate: paint touching it shorts your device. Make the source pad a thin stripe, about 0.5 mm wide (E8 needs a small source pad), and the drain pad large. Let it dry for 30 minutes, then lift the wire.
16. **Measure L and W** with the USB microscope, calibrated against a ruler. L is the gap and W is the length of the gap.
17. **Isolate.** Scribe a moat through the film around each device with the diamond scribe. Otherwise current flows around the ends of the channel and inflates mobility. For ZnO only, you can instead mask the device with Kapton tape and wipe the rest with household vinegar (5% acetic acid) on a swab, then rinse with water [UNVERIFIED: try on a scrap chip first]. Bake at 150 °C for 5 minutes to dry.
18. **Gate contact.** Scratch the back of the chip through its oxide (thermal oxide grows on both faces), paint silver there, and press the chip onto a copper-clad board that serves as the gate terminal. Put one layer of Kapton tape (≥50 µm) under that board, so the gate (up to 27 V) never touches the grounded tin.

18b. **Attach leads.** Glue a thin (0.1-0.2 mm) tinned-copper wire, or stripped 30 AWG wire-wrap wire, onto each pad with a drop of fresh silver paint (two-part silver epoxy is stronger), and let it cure for 1 hour. Tape the gate board to a small carrier board with Kapton, and tape each wire down so the pad never takes strain. Solder only the far end of each wire, at the carrier, never on or near the silver paint. Check each joint with the meter: pad to wire under 100 Ω. Alternative: spring-loaded pogo pins in a clamp.


**F. Measure (in the dark, dry tin)**

19. Before connecting the TIA, check pad-to-pad resistance with the multimeter, with the gate lead shorted to the source: it must read overrange (>20 MΩ). A low reading means silver bridged the gap. Then close the device in the grounded metal tin with silica gel. Wait 30-60 minutes after any light exposure, because ZnO photocurrent can take a long time to decay (S19). Do not touch or move cables during a sweep.
20. **Gate leakage.** Tie source and drain together to the TIA and unplug the drain amplifier:
    `mpremote exec "import pico_smu; pico_smu.run('gleak')" > gleak.csv`. The gate current should stay at your floor. Keep this file: step 24 needs it.
21. **Transfer, saturation, forward and reverse:**
    `mpremote exec "import pico_smu; pico_smu.run('transfer', vd=17.5)" > transfer_sat.csv`
22. **Transfer, linear:** `... pico_smu.run('transfer', vd=0.5) ...` → `transfer_lin.csv`.
23. **Output curves:** `... pico_smu.run('output') ...` → `output.csv`.
24. **Analyse:**
    `python3 code/T4_oxide/iv_analysis.py transfer transfer_sat.csv --gleak gleak.csv --W <W_um> --L <L_um> --tox-nm 300 --svg transfer.svg --json transfer.json`
    plus the same for `transfer_lin.csv` (it detects the linear regime) and `iv_analysis.py output output.csv`. Read every WARNING line. Without `--gleak` the gate-leakage check cannot run, and the script says so.
25. **Optional, harder:**
    - **Bias stress.** Hold Vgs = +20 V with Vds = 0 for 100 s and then 1,000 s, re-measuring transfer after each. ΔVth is the "drift" the study's kill lines are written in.
    - **Temperature.** Repeat at 45 and 65 °C on E8's heated block.
    - **Off-current.** Measure it with the E4 bench, which reaches fA.

---

## 9. Data sheet / log template

Copy one block per chip.

```
Chip ID:            Date:            Route: A / B / C          Wafer lot:
Ink: material ___  conc ___ M  made ___ (date/time)  filtered (Y/N)  appearance ___
Coats: n = ___   spin ___ rpm / ___ s   soft bake ___ C / ___ min
Anneal per coat: ___ C (block) / ___ min    final: ___ C / ___ min    plate setpoint ___ C
Contacts: material ___   L = ___ um   W = ___ um   isolated (scribe / vinegar / none)
Battery test (step 14): moat Y/N   A ___ mV   B ___ mV   C (drain unclipped) ___ mV   pass Y/N
Room: ___ C, RH ___ %, minutes in dark tin before measuring ___
Rig offset ___ A   floor (std, open circuit) ___ A   gate leakage max (gleak.csv) ___ A
Transfer sat (Vds = ___ V): Ion ___ A  Ioff ___ A  on/off ___  Von ___ V  SS ___ V/dec
                            Vth ___ V  mu_sat ___ cm2/Vs  hysteresis ___ V  Dit ___ /cm2 eV
Transfer lin (Vds = ___ V): Vth ___ V  mu_lin ___ cm2/Vs
Output: saturates (Y/N)   contact-barrier flag (Y/N)
Bias stress: dVth after 100 s ___ V, 1000 s ___ V
Verdict: PASS / GOOD / WRITE-SWITCH GRADE / FAIL      Notes:
Files: transfer_sat.csv  transfer_lin.csv  output.csv  gleak.csv  *.json  *.svg  photos
```

---

## 10. Pass / fail criteria

| Grade | Criteria (all must hold) |
|---|---|
| **FAIL** | On/off < 10; or gate current comparable to drain current; or the battery-test control (reading C) stays high |
| **PASS: it is a transistor** | Current rises with positive Vgs (n-type); on/off ≥ 1e3 in the dark; off-region gate current (from gleak.csv, passed with `--gleak`) < 0.3 × Ioff: `iv_analysis.py` prints neither a gate-leakage WARNING nor "Gate leakage NOT checked" |
| **GOOD** | On/off ≥ 1e5; SS ≤ 2 V/dec; µ ≥ 0.1 cm²/Vs; hysteresis ≤ 3 V; output curves saturate |
| **WRITE-SWITCH GRADE (needed for E8)** | Vth ≥ +3 V (enhancement mode); Ioff at Vgs = 0 ≤ 10 pA (≤1 pA preferred); on/off ≥ 1e6 |

---

## 11. What would surprise you (and would mean something new)

- **Off-current far below 1 fA per µm of width** (E4 bench) from a hot-plate film. Solution films are defect-rich, so that would point to an unusually clean film and is worth repeating carefully.
- **Off-current that falls when you heat the device.** That suggests desorbing water or oxygen dominates, not the channel.
- **Off-current with an activation energy ≥1 eV.** That looks like bulk generation, which the band-gap argument says should not happen in ZnO.
- **No hysteresis in humid air** without passivation.
- **Mobility >10 cm²/Vs from pure ZnO on SiO2 at ≤300 °C**, after you have isolated the device and measured W and L. That is beyond the literature in section 13. Check for fringe current first.
- **Better results at 200-250 °C than at 350 °C.** That would argue for an even lower thermal budget, which helps stacking.

---

## 12. Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| No current at any gate voltage | Film not converted (plate cooler than you think), film too thin, open contacts | Check the block temperature with the thermocouple; add coats; check pad continuity |
| Always on (on/off < 10) | Film too thick or too conductive; silver bridged the gap; film not isolated | Fewer coats; check pad-to-pad resistance at Vgs = 0; scribe moats |
| Large gate current | Scratched oxide under a probe or pad; silver touching a cleaved edge; pinhole | Keep paint ≥1 mm from edges; new chip; lighter probe pressure |
| Battery test: current stays when the drain is unclipped | Gate current: film or paint touching a cleaved edge, a scratch, a pinhole | Scribe a closed moat; repaint ≥1 mm inside it; new chip |
| Range never changes; currents pinned at a range limit (range column shows `!`) | Relay coils driven from GPIO pins, or ULN2003A COM/GND miswired | Drive the coils through the ULN2003A (section 7) |
| Wrong, too-small readings at high current | ADS1115 powered from 3.3 V: its input clamps the TIA output | Power the ADS1115 from 5 V, with the I2C level shifter |
| Off-current a few pA too high, or negative | TIA offset not removed; non-A op-amp | Let `zero_offset()` run (default); use an LMC6482**A**IN |
| Big hysteresis or drift | Water and oxygen adsorbed on the bare back channel | Bake at 150 °C right before measuring; dry tin; slower sweeps; ALD passivation at a makerspace or university |
| Off-current jumps with room light | Photoconductivity of ZnO; slow recovery (S19) | Dark tin; wait 30-60 minutes; do not open the lid mid-run |
| S-shaped start of output curves | Contact barrier (Ag or Pt on ZnO) | Al or In contacts (route C); try a short post-contact bake at 150 °C [ESTIMATE] |
| Mobility absurdly high | Fringe current from an unisolated film; wrong W or L | Isolate; measure W and L under the microscope |
| Noisy pA readings | Unshielded TIA input, moving cables (triboelectric charge), humidity | Short guarded input in the tin; PTFE; do not touch cables; silica gel |
| Film cracks or peels | Coat too thick, or ramped too fast | Lower concentration; more, thinner coats; put the chip on a warm plate, not a hot one |
| Comet streaks, spots | Dust; undissolved particles | Filter the ink; clean the chip; spin under a clean box lid |
| Cloudy ink | ZnO not dissolved; ammonia lost | Fresh ammonia; chill longer; filter |
| Depletion mode (on at Vgs = 0) with indium inks | Film too conductive (section 1.5) | Thinner film (lower concentration, one coat); add Zn or Ga; anneal in air longer |

---

## 13. Literature numbers to compare against

| Material and route | Anneal | µ (cm²/Vs) | On/off | Other | Source |
|---|---|---|---|---|---|
| ZnO, aqueous zinc-ammine | 180 °C | up to 0.9 | - | Polycrystalline film at 180 °C | S2 [REPORTED] |
| Al:ZnO, aqueous zinc-ammine | 180 °C / 120 °C | >5 / 3 | - | Same group as Lin, Faber, Anthopoulos | S1 [REPORTED] |
| ZnO from ZnO powder in ammonia | low T | - | - | "most efficient" precursor route | S3 [REPORTED] |
| Na:ZnO, ammonia route | 300 °C | 1.84 | - | "scant hysteresis", good stability | S4 [REPORTED] |
| Y:ZnO (sol-gel) | 350 °C | ~1.8 | ~1e7 | ΔVth 3.78 V under positive bias stress | S15 [REPORTED] |
| In2O3, aqueous, on ZrOx high-k | 250 °C | 23.6 | >1e7 | SS 90 mV/dec, Vth 0.13 V, 1.5 V operation | S8 [REPORTED] |
| In2O3, hexaaqua route, on Al2O3 | 250 °C | 36.3 | >1e7 | - | S9 [REPORTED] |
| Amorphous In2O3 (aqueous) | 250 °C | 8.6 | >1e6 | - | S10 [REPORTED; link attribution approximate] |
| Li:In2O3 (hydrated nitrate) | 250 °C | 60 | >1e8 | - | S11 [REPORTED] |
| IZO, water-only ink, on SiO2 | 300 °C, 2 h | 3.35 | ~1e8 | 230 °C for 4 h matches 300 °C | S12 [REPORTED] |
| IGZO, nitrates in water | 300 °C | 2.5 | >1e6.5 | Nitrogen incorporation noted | S13 [REPORTED; journal page not resolved] |
| Combustion In2O3, IZO, ZTO (Kim, Kanatzidis, Facchetti, Marks 2011) | 200-400 °C | - | - | Later work: combustion inks underperform at 200-250 °C | S7 [REPORTED; 2011 figures UNVERIFIED] |
| ZnO, aqueous inorganic inks (Meyers et al., JACS 2008, 130:17603) | - | [UNVERIFIED] | - | Citation confirmed, numbers not | S6 |
| Solution IGZO 2T0C memory | 250 °C → 450 °C | - | - | Retention 3.69 s → 66.0 s; limited by trap-induced leakage | S44 [REPORTED, conference abstract] |

---

## 14. Precedents: people who made semiconductors outside a fab

| Who | What | Notes | Source |
|---|---|---|---|
| Sam Zeloof | Z1 (simple), then Z2 in 2021: a home-made IC reported as 1,200 transistors, 10 µm polysilicon-gate process, in a family garage | Coverage differs: some say 100 transistors (a test array), most say 1,200 | S35 [REPORTED] |
| Jeri Ellsworth | "Home Chip Lab" shown at Maker Faire, May 2009; home-made point-contact transistors; a hand-made silicon inverter after about two years of process work | Used hydrofluoric acid and a rust remover as an acid source: **do not copy this** | S36 [REPORTED] |
| Hobbyist ZnO TFT write-ups | None verified this session. A 2009 blog post titled "homemade thin film transistor experiments" exists (brainwagon.org), but we could not read it | If you document yours, you may be among the first | S36 [UNVERIFIED] |
| University user facilities | NNCI sites open their fabs to external users from academia, industry and government | Your path to Level 3 | S43 [REPORTED] |

**What is new here.** Zeloof and Ellsworth made silicon devices, which need high-temperature diffusion and hazardous acids. An oxide TFT from an aqueous ink needs neither for its channel. It is the same device class the study's best concepts use. The high-temperature step (the gate oxide) is bought, not avoided.

---

## 15. Next steps

- Go to [E8](E8_your_own_oxide_gain_cell_memory.md): use your best write-switch-grade TFT as the write transistor of a memory cell.
- Package your results (curves, extraction JSON, photos, this log) with the study's one-page "Oxide Tail Spec". E8, section 13 shows how that package becomes a request for nanofab time.

---

## Sources

Evidence tags in the text: [REPORTED] = paper, press or vendor page, almost all reached through search snippets; [DATASHEET] = datasheet; [ESTIMATE] = our arithmetic; [UNVERIFIED] = not confirmed; [STUDY] = a number from this repository's models and dossiers. Two hosts (ossila.com and pubs.rsc.org) could not be fetched from this session, so their details come from search snippets only.

- **S1** Al-doped ZnO from an aqueous Zn-ammine complex (Lin, Thomas, Faber, Anthopoulos et al.): >5 cm²/Vs at 180 °C, 3 at 120 °C. https://livrepository.liverpool.ac.uk/id/eprint/3032961 ; https://researchportal.hkust.edu.hk/en/publications/al-doped-zno-transistors-processed-from-solution-at-120-c/
- **S2** Carbon-free aqueous Zn(OH)x(NH3)y ink, ZnO at 180 °C, µ up to 0.9 cm²/Vs (J. South China Univ. Tech. 2015). https://zrb.bjb.scut.edu.cn/CN/Y2015/V43/I3/98 ; https://zrb.bjb.scut.edu.cn/EN/abstract/article/1000-565X/11512
- **S3** Park et al., "Aqueous zinc ammine complex for solution-processed ZnO semiconductors in TFTs", RSC Adv. 2014, 4, 11295 (DOI 10.1039/C3RA47437B). https://pubs.rsc.org/en/Content/ArticleLanding/2014/RA/C3RA47437B ; https://research.knu.ac.kr/en/publications/aqueous-zinc-ammine-complex-for-solution-processed-zno-semiconduc/
- **S4** Na-doped ZnO by an ammonia-ZnO route, 1.84 cm²/Vs at 300 °C, scant hysteresis (J. Mater. Chem. 2012). https://pubs.rsc.org/es/content/articlelanding/2012/jm/c2jm33790h
- **S5** Recipe details from search snippets: ZnO powder in ammonium solution to 0.1 M, stirred overnight; a Li:ZnO paper chilling the ammonia ink for a day for solubility and annealing at 300 °C for 1 h; another paper using 14.5 M NH3, 12 h aging, 3,500 rpm for 30 s, 200-400 °C for 30 min. The mapping of each detail to each URL is approximate. https://rsc.org/suppdata/c5/ra/c5ra11480b/c5ra11480b1.pdf ; https://pubs.rsc.org/he/content/getauthorversionpdf/C3TC32311K
- **S6** Meyers, Anderson, Hung, Thompson, Wager, Keszler, "Aqueous inorganic inks for low-temperature fabrication of ZnO TFTs", J. Am. Chem. Soc. 130 (2008) 17603-17609 (DOI 10.1021/ja806935z). Citation confirmed via https://scholar.korea.ac.kr/handle/2021.sw.korea/107435 ; device numbers [UNVERIFIED].
- **S7** Kim, Kanatzidis, Facchetti, Marks, Nature Materials 10 (2011) 382-388, combustion processing at 200-400 °C. https://par.nsf.gov/search/author:%22Chen,%20Zhihua%22 ; later results at 200-250 °C: https://pubs.rsc.org/en/content/articlehtml/2020/ma/d0ma00072h ; https://electronicimaging.spiedigitallibrary.org/conference-proceedings-of-spie/11281/112811F/Structure-property-relationship-in-blade-coated-amorphous-In2O3-thin-film/10.1117/12.2545326.full
- **S8** Liu et al., aqueous In2O3 TFTs on ultrathin ZrOx, 250 °C, 23.6 cm²/Vs, >1e7, SS 90 mV/dec, ACS Appl. Mater. Interfaces 2014. https://www.ncbi.nlm.nih.gov/pubmed/25285983
- **S9** Hexaaqua indium(III) route, 36.31 cm²/Vs on Al2O3 at 250 °C. https://profiles.wustl.edu/en/publications/hexaaqua-metal-complexes-for-low-temperature-formation-of-fully-m/
- **S10** Amorphous In2O3, 250 °C, 8.6 cm²/Vs, >1e6 (Choi et al., JJAP 2013, per snippet). https://scholar.korea.ac.kr/handle/2021.sw.korea/103134
- **S11** Li-doped In2O3 from hydrated indium nitrate, 60 cm²/Vs, >1e8 at 250 °C, Sci. Rep. 2016. https://link.springer.com/10.1038/srep25079 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC4848541
- **S12** Liu et al., water-induced IZO on SiO2, 300 °C 2 h, 3.35 cm²/Vs, ~1e8, Adv. Funct. Mater. 2015. https://api.crossref.org/works/10.1002/adfm.201500056 ; https://novaresearch.unl.pt/en/publications/low-temperature-nontoxic-water-induced-metal-oxide-thin-films-and/
- **S13** IGZO from nitrates in DI water, 300 °C, 2.5 cm²/Vs, >1e6.5, Adv. Eng. Mater. (search snippet; article page not resolved) [REPORTED, incomplete citation].
- **S15** Y-doped ZnO, 350 °C, ~1.8 cm²/Vs, ~1e7, ΔVth 3.78 V under PBS, J. Mater. Chem. 2011. https://pubs.rsc.org/lt/content/articlelanding/2011/jm/c1jm11586c/unauth
- **S16** Bias stress in solution oxides: ZnO PBS mechanisms https://dspace.kaist.ac.kr/handle/10203/99311?mode=full ; negative bias stress https://research.knu.ac.kr/en/publications/effects-of-negative-gate-bias-stress-on-the-performance-of-soluti/ ; Zr:IZO on/off 2.6e6 https://pure.uos.ac.kr/en/publications/control-of-electrical-properties-and-gate-bias-stress-stability-i/
- **S18** Temperature behaviour: IGZO off-current ~1e-12 to 1e-13 A, nearly flat 300-370 K, on-state Ea ~0.35 eV (Estrada et al.) https://repositorio.ausjal.org/handle/20.500.12032/88707 ; mobility Ea ~26 meV (Chen and Kanicki, IEEE TED 2009) https://vhosts.eecs.umich.edu/omelab/downloads/CC%20IEEE%20TED%202009.pdf ; IZO leakage rises above 340 K https://cpl.iphy.ac.cn/fileCPL/journal/article/cpl/html/2018/0256-307X/0256-307X-2018-35-9-098502.html
- **S19** ZnO photoconductivity and oxygen adsorption: ZnO TFT UV detector, dark current ~5e-14 A, oxygen-plasma fix https://rutchem.rutgers.edu/images/PDFs/faculty/garfunkel-pubs/2012/ApplPhysLett_101_031118.pdf ; UV-ozone treatment reduces PPC https://koasas.kaist.ac.kr/handle/10203/240837 ; nanowire photocurrent persisting for hours https://arxiv.org/abs/1907.11393v1
- **S20** Contacts: Schottky junctions raise contact resistance in oxide TFTs https://link.springer.com/10.1038/s41598-024-61837-2 ; printed ITO interlayer cuts Ag/ZnO contact resistance 100x https://publica.fraunhofer.de/handle/publica/244560 . Pt on ZnO: no direct data found [UNVERIFIED].
- **S21** Ossila Pt OFET test chips S403A1 (Ti 5 nm / Pt 100 nm, 300 nm SiO2, p-doped Si, W 1 mm, L 2-10 µm, $225 vs £150 conflict); Au chips discontinued; S146 300 nm substrate $598. https://www.ossila.com/products/prefabricated-platinum-ofet-test-chips ; https://downloads.ossila.com/manuals/prefabricated-platinum-ofet-test-chips.pdf ; https://ossila.com/products/silicon-oxide-substrates
- **S22** MTI thermal-oxide wafer, 100 mm, p-type 0.001-0.005 Ω·cm, 300 nm SiO2, $109.95. https://mtixtl.com/products/thermal-oxide-wafer-300nm-sio2-layer-on-si-100100mm-diax0-5-mm-t-p-type-1sp-r-0-001-0-005-ohm-cm ; UniversityWafer item 1583: https://www.universitywafer.com/Wafers_Services/Silicon/ThermalOxide.html
- **S23** Benchmark H3770-H 7×7 in digital ceramic hot plate, max 380-400 °C, $274-302. https://www.globalindustrial.com/p/digital-hotplate-7x7 ; https://geneseesci.com/shop-online/category/8005/hot-plates
- **S24** Spin coaters: Maasi open design (<€100 goal) https://edoc.hu-berlin.de/18452/28886 ; Hackaday DIY spin coater https://hackaday.io/project/192036-diy-spin-coater ; commercial from ~€500, DIY cost warning https://instras.com/index.php/build-or-buy/ ; hard-drive build https://scielo.br/j/qn/a/qQgKLk65PbLTzpRhXsMZf4x/abstract/?lang=pt ; 500-10,000 rpm open build https://revistas.unal.edu.co/index.php/momento/article/view/50622 ; 2023 low-cost build https://pmc.ncbi.nlm.nih.gov/articles/PMC10172839/
- **S25** Sigma-Aldrich 204951 zinc oxide 99.999%, 25 g, $181. https://sigmaaldrich.com/product/aldrich/204951
- **S26** Ammonium hydroxide 28-30%, 500 mL, $45.70-95.50 (Sigma), $47 (Genesee/RICCA), ~$51.65 (Thermo). https://www.sigmaaldrich.com/US/en/product/mm/ax1303 ; https://www.geneseesci.com/product/72-976-ammonium-hydroxide-30-acs-reagent-grade-500-ml/ ; https://thermofisher.com/order/catalog/product/423305000
- **S27** Indium(III) nitrate hydrate 99.99%, 10 g, $163.10 (undated listing). https://www.thomassci.com/p/indiumiii-nitrate-hydrate-9999-trace-metals-basis
- **S28** Ammonium hydroxide SDS hazards (H314, H335, H400; variants H302, H318, H411). https://www.thomassci.com/p/sial-ammonium-hydroxide-solution ; https://portaleclns.iit.it/files/sds/22%20-%20bioprinting/ammonium%20hydroxide%20solution_2022_eng.pdf ; https://discovery.sdsmanager.com/safety-data-sheet/english/vwr-international-llc-ammonium-hydroxide-28-30-acs-reagent-acs-grade-en
- **S29** Zinc nitrate hexahydrate SDSs. https://www.sigmaaldrich.com/sds/sigald/228737 ; https://www.geneseo.edu/sites/default/files/documents/zinc%20nitrate%20sds%20-%202023.pdf ; https://labbox.es/wp-content/uploads/FDS/SDS_EN_10577.pdf
- **S30** Indium nitrate SDSs (Wako trihydrate: H272, H315, H319, H351). https://labchem-wako.fujifilm.com/sds/W01W0109-0457JGHEEN.pdf ; https://americanelements.com/indium-nitrate-hydrate-207398-97-8 ; https://www.sigmaaldrich.com/sds/aldrich/254215
- **S31** Gallium nitrate hydrate SDSs (H272, H315, H319). https://www.sigmaaldrich.com/sds/aldrich/289892 ; https://glentham.com/en/products/product/GX2811/datasheet ; https://www.americanelements.com/ganiy.html
- **S32** Zinc acetate dihydrate SDSs (H302, H318, H411). https://discovery.sdsmanager.com/safety-data-sheet/english/sigma-aldrich-inc-zinc-acetate-dihydrate-en ; https://www.himedialabs.com/media/TD/GRM3977.pdf
- **S33** 2-Methoxyethanol: Repr. 1B, H360FD. https://sdsmanager.com/safety-data-sheet/sigma-aldrich-chemie-gmbh-ethylene-glycol-monomethyl-ether-for-analysis-emsure-acs-reag-ph-eur-en/ ; https://lobachemie.com/lab-chemical-msds/MSDS-2METHOXYETHANOL-CASNO-109-86-00202-EN.aspx
- **S34** Indium: NIOSH REL 0.1 mg/m³ (8-h TWA); indium lung disease in ITO workers; Japan respirable limit 3e-4 mg/m³. https://archive.cdc.gov/www_cdc_gov/niosh/pel88/7440-74.html ; https://stacks.cdc.gov/view/cdc/31735 ; https://haz-map.com/Agents/521 ; https://www.jniosh.johas.go.jp/en/indu_hel/doc/IH_56_6_553.pdf
- **S35** Sam Zeloof, Z2. https://tomshardware.com/uk/news/man-builds-own-silicon-chip-at-home ; https://interestingengineering.com/a-new-homemade-z2-chip-came-from-the-mind-of-a-22-year-old-undergrad ; https://spectrum.ieee.org/the-high-school-student-whos-building-his-own-integrated-circuits ; https://hackaday.com/tag/sam-zeloof
- **S36** Jeri Ellsworth. https://hackaday.com/2010/03/page/15 ; https://hackaday.com/tag/transitor ; https://thenewstack.io/post-apocalyptic-computing-with-jeri-ellsworths-home-brewed-chips/ ; https://en.wikipedia.org/wiki/Jeri_Ellsworth (snippet only) ; brainwagon post (title only, not read) https://brainwagon.org/blog/homemade-thin-film-transistor-experiments
- **S37** Used Keithley 2400 asking prices. https://www.ebay.com/itm/356832854940 ; https://www.transcat.com/products/used-and-refurbished-equipment/used-keithley-2400-200v-1a-20w-digital-sourcemeter
- **S38** LMC6482: 20 fA typical input bias, 3-15.5 V supply, rail-to-rail. Input offset voltage: LMC6482AI 0.11 mV typical, 0.75 mV maximum at 25 °C in current TI listings (an older National revision lists 2.0 mV for the AI grade under other conditions); LMC6482I 3.0 mV maximum. Absolute maximum current at an input pin ±5 mA [DATASHEET, via distributor copies and search snippets; the TI PDF itself was not opened]. https://www.radiolocman.com/datasheet/data.html?di=215573 ; https://kyohritsu.com/eclib/OTHER/DATASHEET/lmc6482.pdf ; https://web.eecs.utk.edu/~dcostine/ECE482/Spring2022/components/parts/PartsKit/datasheets/LMC6482.pdf ; https://www.lcsc.com/product-detail/C2878968.html ; https://wiki.adom.inc/ray/lmc6482 ; https://www.radiolocman.com/datasheet/data.html?di=269843
- **S39** Adafruit ADS1115 breakout (product 1085), 16-bit, 860 SPS, $14.95. https://www.adafruit.com/product/1085
- **S40** Raspberry Pi Pico 2, $5 (August 2024). https://www.electronicspecifier.com/boards-and-backplanes/raspberry-pi-unveils-the-pico-2-for-just-5 ; https://www.cnx-software.com/2024/08/08/raspberry-pi-pico-2-raspberry-pi-rp2350-dual-core-risc-v-or-arm-cortex-m33-microcontroller/
- **S42** Purdue Birck rates (2023 schedule, pending approval when posted): daily lab fee $14/$44/$51 and cleanroom $28/$53/$61 (internal / external academic / external for-profit); tool rates hourly (for example EBL $115-132/h). https://engineering.purdue.edu/ECN/mailman/archives/bnc-all/2023-May/002727.html ; https://birck.research.purdue.edu/getting-started-at-birck/rates/ ; https://birck.research.purdue.edu/equipment/become-a-user/
- **S43** Georgia Tech IEN and NNCI: ~20% external users; academic and government users pay Georgia Tech rates. https://sites.gatech.edu/ien-prc/files/2021/07/IEN-Welcome-and-Overview-Vogel.pdf ; https://dev.research.gatech.edu/nano/become-core-user ; https://hg.gatech.edu/sites/default/files/attachments/IEN%20Seed%20Grant%20RFP%202016-17.pdf ; https://nnci.net/sites/default/files/inline-files/SENIC%20Overview%20Sept%202018_Final.pdf
- **S44** Oxide 2T0C retention: solution IGZO 2T0C 3.69 s (250 °C) → 66.0 s (450 °C), MRS Spring 2026 abstract https://www.mrs.org/meetings-events/annual-meetings/archive/meeting/presentations/view/2026-mrs-spring-meeting/2026-mrs-spring-meeting-4433903 ; vacuum ITO vertical 2T0C >160 s https://scholarworks.gnu.ac.kr/item/b7313d21-0cf1-4e73-99dc-d088f829f2b7 ; ITZO >1,000 s (ETRI, press) https://ksp.etri.re.kr/ksp/article/file/72428.pdf ; Al:ITZO 2T0C https://pmc.ncbi.nlm.nih.gov/articles/PMC11739972 ; study values (imec >200 s at 95 °C, implied 75 zA) from [../dossiers/hot-side-memory.md](../dossiers/hot-side-memory.md) [STUDY].
- **S45** LM358 output high voltage at V+ = 30 V: 27 V min, 28 V typ at RL = 10 kΩ; 26 V min at RL = 2 kΩ. Absolute maximum supply 32 V [DATASHEET, via search snippets of TI, ST and other LM358 datasheets]. https://static.rapidonline.com/pdf/82-0334.pdf ; https://ti.com/document-viewer/LM158-N/datasheet/GUID-6AC0155B-9988-4242-A0C1-9933FFF4CA47 ; https://cdn.sparkfun.com/assets/e/b/8/f/a/LM358.pdf
- **S47** Reed relays: Coto 9007-05-00, SPST-NO, 5 V coil, 500 Ω coil resistance, 0.5 A [REPORTED, distributor listings]. A must-operate voltage of ~75% of nominal (3.75 V for a 5 V coil) is typical for reed relays [ESTIMATE, not confirmed for this part]; shielding not confirmed. https://azcus.digikey.com/en/products/detail/coto-technology/9007-05-00/301696 ; https://au.element14.com/coto-technology/9007-05-00/relay-sip-reed-spst-5v/dp/108168201 ; https://digikey.cn/en/products/detail/comus-international/3570-1331-051/7497098
- **S48** Chemical suppliers selling only to institutions [REPORTED, search snippets supplied during review; not re-checked this session]. https://www.sciencebuddies.org/science-fair-projects/references/science-fair-materials-approved-supplier ; https://www.aladdinsci.com/eu_en/sales-policy/
- **S49** ADS1115: analog inputs must stay between GND − 0.3 V and VDD + 0.3 V [DATASHEET, TI ADS1115; not re-read this session]. https://www.ti.com/lit/ds/symlink/ads1115.pdf . RP2350 GPIO 5 V tolerance only while powered, ADC pins excluded [REPORTED, secondhand forum quotes of the RP2350 datasheet]: https://classiccmp.org/mailman3/hyperkitty/list/cctalk@classiccmp.org/message/KQSLPKCY7ZRZ2JKE26ZVVPDONBWQNQRM/ . The level shifter in section 7 avoids relying on it.
- **S50** ULN2003A seven-channel Darlington driver with input resistors for TTL/CMOS logic and built-in clamp diodes to COM [DATASHEET, TI ULN2003A; not re-read this session]. https://www.ti.com/lit/ds/symlink/uln2003a.pdf . Coil voltage through it ~4.1 V from 5 V [ESTIMATE].
