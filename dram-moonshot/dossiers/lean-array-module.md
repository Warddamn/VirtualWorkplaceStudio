# LEAN ARRAY MODULE: helium-free, PFAS-light, EUV-free process modules for periodic memory arrays

NEW DRAM Stage 3 dossier. Author: agent `dosw-lean-array-module`, 2026-11-02.

Inputs:
- Model `models/lean-array-module.py`, re-run today with exit 0. Its output is identical to `research/stage3/lean-array-module_model_output.md`.
- Notes `research/stage3/lean-array-module_notes.md`.
- Assumptions `research/assumptions/dos-lean-array-module.md`.

Tags:
- [REPORTED]: from a logged source, usually seen only as a search snippet.
- [ESTIMATE]: model arithmetic.
- [UNVERIFIED-PK]: prior knowledge, no URL.
- [SPECULATIVE]: not yet shown by anyone.

---

## 0. Header

**Name:** LEAN ARRAY MODULE.

**Thesis:** Replace helium backside cooling with low-pressure hydrogen, delete the fluorocarbon capacitor etch, and pattern periodic layers without EUV, so an array line keeps running when Qatar, 3M or ASML stop.

**Rank:** 8 of 10, EV 40 (S2xP4xD5).

**Category:** materials/resources (device-lens concept plus the system-lens Merchant Cell Wafer's chokepoint recipe).

| Id | Idea | Creativity technique | Verdict | Role |
|---|---|---|---|---|
| I-10762 | Low-pressure H2 backside cooling | Wishful thinking / ideal final result | ADVANCE (67.1) | Core module |
| I-07130 | Interference gratings + coarse cuts | Reverse brainstorming | ADVANCE (62.1) | EUV-free layers (deferred) |
| I-11235 | Fiber-drawn capacitor arrays | Scarcity and constraint as engine | HOLD (60.9; innovation DROP) | Back-up no-etch mold |
| I-00257 | Local gain FETs from the VCT step | SCAMPER-Substitute | ADVANCE (62.6) | Why stub cells need no HAR etch |
| N-21 | AAO capacitor mold (B2-01) | Phase-B lens: new materials, low-resource fab | ALIVE, NEW | PFAS-free mold, Si-access cells |
| N-29 | Fluorine-free carbon mold (B2-10) | Same lens | ALIVE, TWIST | Alternate PFAS-free mold |
| N-26 | Ga-free, In-lean oxide channels (B2-07) | Same lens | ALIVE, KNOWN+TWIST | Gallium out of oxide cells |

**Verdicts**

- **PHYSICALLY POSSIBLE? Yes.** H2 is the only helium-like backside gas (1.17x conductivity, Paschen minimum 1.8-2.3x); the one unknown, a_H2, is measurable and its ~0.27 prior clears the 0.17 GO line.
- **STEP CHANGE IF IT WORKS? Yes on supply-chain exposure, no on $/bit.** Backside He, capacitor fluorocarbon and F~40 nm-array EUV (5-7 layers) all go to 0, but that He is ~3% (1-11%) of DRAM's and $/bit stays ~1.0x.
- **PROVABLE WITH $1M IN 24 MONTHS? Yes for the core H2 module, partly for the line.** A ~$100k rig decides at month 8 and a partner 300 mm swap closes by month 20; AAO gets a first look, IL waits for the raise.

---

## 1. How it works

Plasma etch and deposition tools hold the wafer on an electrostatic chuck, a ceramic plate that grips it by static charge. The plasma pours kilowatts into the wafer, and the chuck below is water-cooled. The two touch only on tiny bumps, so the heat must cross a ~10 micrometre gap. That gap is filled with gas at 10-40 Torr, which is 1-5% of an atmosphere. Today that gas is helium.

At these pressures, gas molecules cross the gap without hitting one another. Each one carries heat from the hot wafer to the cold chuck. Light molecules move faster, so they carry more heat.

A gas that bounces off a surface without fully taking on its temperature has a low accommodation coefficient. Such a gas acts as if the gap were tens of micrometres wider than it really is. That sounds bad, but it makes cooling insensitive to the few micrometres of gap variation caused by wafer bow. Helium is light and accommodates poorly, so it cools evenly. Nitrogen and argon accommodate well, so their cooling follows every micrometre of gap.

Hydrogen is lighter still. It conducts heat 1.17x better than helium, arcs less, and can be made on site from water. The unknown is how well H2 "shakes hands" with real backsides coated in oxide, nitride, polysilicon or etch residue. If the handshake is too weak (below 0.10), no pressure the chuck can hold makes up for it.

```
          PLASMA (~2.4 kW ends up as heat in the wafer)
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 ===================  300 mm WAFER (hot)  ====================
    ^ ^ ^   gas in a ~10 um gap, 15-40 Torr: He today -> H2   ^ ^ ^
 ##======##======##======##======##======##   ESC ceramic (cold),
       mesas carry the clamp; gas carries the heat   water-cooled
      |                                     |
 seal leak 1-2.5 sccm H2 -> plasma     dump ~40 sccm -> foreline
 (H/F ratio +0.5-1.2%)                 (~2% of the 4% LFL)
```

The concept has four modules:

```
 TODAY                                  LEAN ARRAY LINE
 He backside gas (Qatar ~30%)     ->    H2 from an on-site electrolyser       [CORE]
 AR-60 C4F6/C4F8 capacitor etch   ->    oxide stub/gain cell (no HAR), AAO
   (PFAS-class gas)                       mold, or carbon mold               [SECONDARY]
 EUV on periodic layers (ASML)    ->    IL/NIL + coarse DUV cuts, F~40 nm only [DEFERRED]
 IGZO channel (Ga ~98% Chinese)   ->    ZTO / In-lean oxide                   [MATERIALS]
```

AAO grows capacitor holes electrochemically in aluminium, and the carbon mold is etched with oxygen, so neither needs fluorocarbon plasma. IL and NIL print repetitive layers with interfering beams or a stamp, not a $290M scanner. None of this makes memory cheaper; it makes the line harder to stop.

---

## 2. The physics and the numbers

### 2.1 Gas-gap conductance

**Heat load.** 3.0 kW bias x 0.80 heat fraction / 0.0707 m2 = **34.0 kW/m2** [ESTIMATE].

**Model.** h = k/(d + g_w + g_c) + 50 W/m2K, with a gap d of 10 um. The Smoluchowski jump distance is g = (2-a)/a x 2gamma/(gamma+1) x lambda/Pr.

**Helium baseline.** At 15 Torr and a = 0.45 (Sandia [REPORTED]):
- g = 3.44 x 1.25 x 9.8 um / 0.667 = **63.6 um per surface**. The gap therefore acts like ~137 um.
- h = 0.155/137e-6 + 50 = **1,180 W/m2K**.
- The wafer sits 34,000/1,180 = **28.8 K** above the chuck.

**Free-molecular ratio.** Per unit accommodation, conductance scales as (gamma+1)/(gamma-1)/sqrt(M). That gives 2.0 for He and 4.18 for H2, a ratio of **2.09x**. The jump model matches Corruccini within 0.0%.

| Gas (a) | p (Torr) | h (W/m2K) | dT (K) | dT spread, gap 5-15 um (K) |
|---|---|---|---|---|
| He (0.45) | 15 | 1,180 | 28.8 | 2.0 |
| H2 (0.20) | 15 | 976 | 34.8 | 1.7 |
| H2 (0.20) | 22.5 | 1,405 | 24.2 | 1.7 |
| N2 (0.85) | 15 | 1,098 | 30.9 | **11.9** |
| Ar (0.95) | 15 | 766 | 44.3 | **16.8** |

N2 matches helium's average, but a +/-5 um gap error spreads its wafer temperature 6x wider. Only H2 keeps helium's uniformity.

### 2.2 The key unknown and the break-even

**Prior.** Baule hard-cube scaling (surface mass 20 amu) gives a_H2/a_He = 0.200/0.333 = 0.60. Times helium's measured 0.45, that is **a_H2 ~ 0.27**. The planning value is 0.20 [ESTIMATE].

**Break-even a_H2** to match helium at 15 Torr:

| Condition | a_H2 needed |
|---|---|
| Drop-in, same 15 Torr | **0.241** |
| Parity at 1.5x pressure (22.5 Torr) | **0.168 (GO line)** |
| Parity at the 40 Torr clamp limit | **0.098 (NO-GO line)** |

The 1.5x-pressure break-even is 0.168, 0.166 and 0.163 at gaps of 5, 20 and 40 um. It barely moves.

**Correction to the card.** The card says a low a_H2 means "pressure must rise or the gap must shrink". The jump distance (60-90 um) dominates the 5-40 um gap, so shrinking the gap does almost nothing. The real levers are pressure, a chuck coating or a blend.

**Asymmetric rescue.** A poorly accommodating wafer (0.10) against a well-accommodating chuck face (0.45) reaches parity at **23 Torr**.

**Sensitivity** (3 kW, 10 um gap, +/-2 K window):

| a_H2 | dT shift at He pressure | Parity pressure | Seal leak | Verdict |
|---|---|---|---|---|
| 0.05 | +95.8 K | >40 Torr | - | NO-GO |
| 0.10 | +39.0 K | 39.1 Torr | 1.84 sccm | CONDITIONAL |
| 0.16 | +14.6 K | 23.7 Torr | 1.11 sccm | CONDITIONAL |
| 0.20 | +6.0 K | 18.5 Torr | 0.87 sccm | GO |
| 0.25 | -1.0 K | 14.4 Torr | 0.68 sccm | GO (drop-in) |

**Bias power.** At a_H2 = 0.20 and 1.5x pressure, H2 runs cooler than helium at every bias: 16.1 vs 19.2 K at 2 kW, 40.3 vs 48.0 K at 5 kW, and 80.6 vs 95.9 K at 10 kW.

### 2.3 Arcing, leak-in, flammability

**Arcing.** From textbook constants, the Paschen minimum is 142 V for He and **326 V for H2 (2.3x)**. The Stage-2 critics quoted measured values of ~270 vs ~150 V, a ratio of ~1.8x. **I carry 1.8x.**

**Leak into the plasma.** Start from the 0.5 sccm helium seal leak [REPORTED, US 9,753,463], taken at 15 Torr [ESTIMATE]. Scaled to H2 at 22.5 Torr, it is 0.5 x 1.5 x sqrt(4.00/2.02) = 1.06 sccm in the molecular regime, and 0.5 x 1.5^2 x 2.22 = 2.50 sccm in the viscous regime. That adds **0.5-1.2% H atoms against 420 sccm of F atoms**. This is the size of a recipe trim.

**Flammability.** Dump plus leak (42 sccm) in a 50.5 slm foreline is **2.1% of the LFL**. A single fault, limited by the restricting orifice (RFO) to 200 sccm, is **10% of the LFL**. The usual alarm point is 25%.

### 2.4 The honest size of the helium lever

**Volume.** 150 chucked steps x 2.5 min x 20 sccm = **7.5 L of helium per DRAM wafer** [ESTIMATE; range 3-30 L]. Samsung's HeRS first line, ~4.7 t/yr on ~1.2M wafers, is ~22 L/wafer recovered. That is the same order [REPORTED, weak attribution].

**Share.** The fleet uses 166k m3/yr. That is **~3% (1-11%) of DRAM's pro-rata helium**, taken as 160M m3 x 22.5% semiconductors x 17% DRAM.

**Cost.** **$0.32/wafer**, or 104 u$/GB against $1.48/GB. H2 costs $0.007/wafer.

**Insurance value.** A 100k-wpm fab books ~$32M a day. Retrofitting 1,500 chambers at $50k costs $75M, which pays back after **2.4 days** of avoided stoppage [ESTIMATE].

**Critic correction carried.** I-10762 claimed H2 removes "~60-80% of fab helium demand". It is nearer 3%. Under a partial cut, a fab keeps backside cooling and sheds other uses first (leak check → H2/N2 tracer, PECVD diluent → Ar). H2 matters in a near-total cutoff, or as the last step to a fully helium-free line. **It is a tail-risk hedge, not a cost lever.** The backside share is unverified.

### 2.5 Secondary modules (corrected numbers)

**AAO (N-21).** The 1-beta cell is 1,070 nm2, so the hexagonal pitch is 35.2 nm, anodized at ~14 V. The pore is 0.65 x pitch, and the mid-plane diameter after the liner is 11.9 nm. With C = 3.9 eps0 pi d h/EOT at EOT 0.55 nm, a 2.5 um pore gives **5.84 fF** (parity with 1-beta's 5.4 fF; 76 mV signal; 67 ms retention at a 13 fA tail). A 3.0 um pore gives **7.01 fF** (+30%; 88 mV; 81 ms). **B2-01's +37-64% holds only at 40 nm pitch.** At the 1-beta pitch, AAO buys parity to +30%. Its real value is the deleted fluorocarbon etch and the deleted support lattice. Anodization uses 34 Wh/wafer, 0.0026% of fab energy (B2-01's 8 Wh counted the array area only).

**IL/NIL (I-07130).** A single full-wafer grating fails, because 0.1 K moves the wafer edge by 150 mm x 2.6 ppm/K x 0.1 K = **39 nm**. Per-field phase lock at 0.3 ppm gives **6.3 nm**. That meets the 10 nm budget of an F = 40 nm oxide cell, **never 1-beta's 2.5 nm**. Such a cell gives 0.109 Gb/mm2 per tier, 0.24x 1-beta, so it needs at least 5 tiers. EUV at 1c costs $825-1,155 per wafer (19-27%).

### 2.6 Against 1-beta DDR5

| Metric | 1-beta DDR5 | LEAN | Change |
|---|---|---|---|
| $/GB | $1.48 | ~$1.48 | ~1.0x |
| Backside He | ~7.5 L/wafer | 0 | removed |
| Capacitor etch | AR ~60 fluorocarbon | none | removed |
| Cs, Si-access | 5.4 fF | 5.8-7.0 fF | 1.08-1.30x |
| EUV layers | 0 (1-beta); 5-7 (1c) | 0 | vs 1c only |
| Gb/mm2 | 0.447 | 0.109 per F40 tier | needs ≥5 tiers |

### 2.7 GO / NO-GO

- **GO:** symmetric a_H2 ≥0.17 (+/-0.02) on SiO2, SiN, poly and CFx backsides against Al2O3/AlN at 20-60 C. Proceed to Step 2.
- **CONDITIONAL:** 0.10-0.17. Try a coating or a blend.
- **NO-GO:** <0.10 everywhere. Stop pure H2.

Step 2 must then show all of the following:
- +/-2 K of helium across the wafer;
- etch-rate drift ≤2%;
- selectivity drift ≤5% at 2x the predicted leak;
- ≤10% of the LFL in single fault;
- zero backside arcs.

---

## 3. What is new versus prior art

Patent issue years are inferred from patent numbers [UNVERIFIED-PK]. Patent contents come from search snippets [REPORTED].

| Prior art | Date | Shows | Gap left |
|---|---|---|---|
| US 5,810,933; US 6,170,496 | ~1998-2001 | He is standard and N2 an alternative; gas-gap transfer falls below prediction (accommodation) | No H2 |
| US 9,753,463 | ~2017 | ~0.5 sccm seal leak, ~19.5 sccm dump; some makers use N2/Ar for cost | Our leak anchor |
| US 10,395,963 | ~2019 | **Lists H2 as a backside gas** (carrier patent within the result set not pinned) | No broad H2 claim possible; no production use |
| US 8,970,818 | ~2015 | Surfaces raising H2 accommodation (target ≥0.4), lithography | Fallback and IP constraint |
| ASML-related clamps US 12,174,552; 12,189,309; 12,461,452; 12,717,249 | 2024-26 | ESC in **low-pressure H2-rich** EUV tools, in production; backfill gas at the burls aids cooling (whether that gas is H2 is not confirmed) | No RF bias, no fluorocarbon, low flux |
| Sandia, Trott et al. | 2010 | TAC rig: ~0.95 Ar, 0.85 N2, 0.45 He on Si, SiN, poly and metals; contamination matters most | **No H2**; no CFx-residue backsides |
| Banerjee et al., *Nat. Nanotech.* | 2009 | ALD MIM in AAO, ~10 uF/cm2 | Not a DRAM cell |
| Masuda, imprint-ordered AAO | 2004 | 40-500 nm interval | 35 nm below range |
| Micron US 7,829,410; 7,126,181 | ~2006-10 | Template storage nodes | No AAO-DRAM patent found (one search) |
| NRL nanochannel glass (Tonucci, *Science*); microchannel plates; photonic-crystal-fibre stack-and-draw | 1992 | ~33 nm draw-redraw channels [UNVERIFIED-PK] | Basis of I-11235; draw-redraw is not new |
| IBM SOI eDRAM micro sense amp (Barth, ISSCC 2007-08) | 2007-08 | 3T local gain per ~32-cell local bitline [UNVERIFIED-PK] | Basis of I-00257; stub/gain cells are not new |
| US 8,685,628 (193i IL); MIT SBIL; Eulitha [UNVERIFIED-PK] | 2000s-14 | ~33.5 nm half-pitch IL | No DRAM overlay |
| Intel/Borodovsky complementary lithography (gridded lines + e-beam cuts); Phase B N-32, the same IL-array idea [UNVERIFIED-PK] | 2010s; 2026 | Periodic gratings plus coarse cuts | IL-plus-cuts is not new; the delta is only the oxide-cell overlay budget |
| Canon NIL, SPIE 12956/13177 | 2024 | <10 nm; SK hynix and Kioxia trials; DNP 10 nm template (Dec 2025) | Overlay and defects |
| UMich ZTO 2T0C; Cornell CNF PFAS-etch project | undated; 2026 | Ga-free cell, >1,500 s retention; PFAS gas substitution | Long channels; no mold substitution |

**The genuine delta**

1. **No production H2 backside use** in a plasma chamber turned up in searches across Stage 2 and Stage 3.
2. **No measured H2 accommodation** on SiO2, SiN, poly or CFx-coated Si was found (Stage 2, Stage 3 and a verifier search). The Step-1 dataset would be new science.
3. **Narrow claimable inventions:**
   - a leak-compensated recipe;
   - gas composition as a per-zone actuator;
   - accommodation-mapped pressure control;
   - an RFO-limited safety architecture.
4. **The bundle.** Oxide cells relax the limits that kill each piece alone. IL can meet 10 nm overlay but not 2.5 nm, and stub or gain cells delete the HAR etch outright.

---

## 4. Show-stoppers and how persistence could get around them

| # | Show-stopper | Number | Workaround |
|---|---|---|---|
| 1 | Low a_H2 on coated backsides | NO-GO <0.10. An in-situ Ar-plasma clean cut He's value by up to 0.10 at Sandia; H2 on tungsten fell from 0.54 bare to 0.14 under an adsorbed-H film (Phys. Rev. 40, 78) [REPORTED] | Chuck-face coating (0.10 wafer vs 0.45 chuck → 23 Torr), avoiding US 8,970,818; 50/50 H2/He blend halves He; J-R chuck raises the 40 Torr ceiling; start on lower-flux chambers |
| 2 | H2 leak into HAR fluorocarbon etch | 1.06-2.50 sccm = 0.5-1.2% H/F; limits ER ≤2%, selectivity ≤5% | Feed-forward CH2F2/H2 trim; differentially pumped seal band; lower outer-zone pressure; fall back to CVD/PVD and non-HAR chambers |
| 3 | Flammability, EHS | 2.1% LFL normal, 10% single fault | RFO, N2-purged plenum, sensors, interlock to ≤25% LFL under SEMI S2 / NFPA 55 / NFPA 2; fabs already pipe H2 [UNVERIFIED-PK] |
| 4 | Materials under H2 + plasma | Y2O3/AlN faces, bonds, elastomer permeation, Ti embrittlement; backside-film reduction at 400-650 C | Etch chambers first (<~100 C); 500 h coupon soaks; keep N2/Ar on hot, low-flux CVD |
| 5 | Small helium lever; incumbent 80-90% recapture (not physics) | ~3% (1-11%) of DRAM He; $0.32/wafer | Sell as the He-free closing step and outage insurance (2.4-day payback), complementary to recapture; get the use split by month 6 |
| 6 | AAO pitch and registration | 35.2 nm vs 40 nm floor; 3-4 nm imprint-to-pad overlay; barrier removal; anion-laden walls | 4F2 at 40 nm pitch; Ti/Nb stop layer; ramp-down barrier thinning; ALD Al2O3 liner; self-aligned pads; ECC |
| 7 | IL overlay | 39 nm per 0.1 K full-wafer; 6.3 nm per-field vs 2.5 nm needed at 1-beta | Only for F~40 nm oxide cells; SBIL-type per-field phase lock; Canon NIL alternate |
| 8 | Carbon-mold bow (N-29) | Kill at >2 nm uncorrectable at AR 50-100 | Boron-doped carbon, support decks, shorter capacitors, H2-plasma strip |
| 9 | Fiber-drawn glass (I-11235) | Rayleigh-Plateau core breakup; 1% draw disorder misregisters within ~100 cells | Etchable-core nanochannel glass with pads wider than the pitch; last in line |
| 10 | ZTO threshold control (N-26) | Ioff ≤1 aA at Lg <30 nm unshown | Al/Si-doped ZTO, 3-5 nm channels, double gate; In-lean ITZO fallback |
| 11 | Gain-FET mismatch (I-00257) | Vt sigma 30-50 mV vs ~250 mV gives ~5-6 sigma over 1e10 cells | CDS and ECC; measured on the shared MARGIN STACK MPW |

---

## 5. The decisive experiment

**Question.** Does H2 cool like helium on real films, without upsetting the etch or creating a fire hazard?

**Step 1. Accommodation matrix (months 1-8, ~$100k, binary gate).**
- **Where:** a university gas-surface lab, using Sandia's Trott TAC assembly as the template. Sandia is the preferred CRADA partner.
- **Rig:** a parallel-plate cell with a 50 mm guarded hot plate carrying a wafer coupon and a cold plate carrying a chuck-ceramic coupon. Gaps of 5-50 um are read capacitively. Pressure runs 0.05-50 Torr on capacitance manometers.
- **Gases:** He (calibrate to 0.45 +/- 0.03), H2, N2, Ar, and 25/50/75% H2-He blends.
- **Wafer faces:** native-oxide Si, SiO2, SiN, poly, CFx-exposed and post-clean backsides.
- **Chuck faces:** Al2O3, AlN, Y2O3. Temperatures 20/40/60 C.
- **Analysis:** fit a_wafer and a_chuck with the model's `h_gas()`, to +/-0.02.
- **Pass/fail (symmetric a_H2):** ≥0.17 GO; 0.10-0.17 CONDITIONAL; <0.10 NO-GO.

**Step 1b. Small-tool plasma test (months 4-10, ~$120k).**
- **Where:** a university ICP etcher with a 150/200 mm ESC (Cornell CNF, UMD or UIUC class).
- **Install:** an H2 line with RFO, sensor and purged plenum.
- **Thermal run:** thermocouple wafer, He vs H2, 5-30 Torr, 1-3 kW.
- **Bleed run:** 0-4 sccm H2 into a C4F6/C4F8/O2/Ar oxide etch on AR 10-20 coupons. Measure etch rate, selectivity and profile, with OES of H-alpha and CF2.
- **Pass:** wafer temperature within +/-2 K of He, etch-rate drift ≤2% and selectivity drift ≤5% at 2.5 sccm.

**Step 2. 300 mm chamber swap (months 10-20, ~$300k cash plus partner in-kind).**
- **Where:** NY CREATES Albany NanoTech, or an OEM demo lab (Lam, Applied's META Center, TEL).
- **Sequence:**
  - SEMI S2 / NFPA 55 / NFPA 2 hazard analysis with a third-party assessor;
  - centre and edge thermocouple-wafer maps at 2-5 kW;
  - AR ≥40 HAR oxide etch on patterned wafers, with etch rate, selectivity, bow and CD against He;
  - ≥100 wafer-hours of foreline logging.
- **Pass:** +/-2 K, etch-rate drift ≤2%, selectivity drift ≤5%, zero arcs and ≤10% LFL in single fault.

| Decisive-experiment budget | $k |
|---|---|
| Step 1 rig hardware (manometers, guarded heater, vacuum, DAQ) | 55 |
| Step 1 coupons and films | 15 |
| Step 1 lab fees and student (or Sandia SPP) | 30 |
| Step 1b tool time, thermocouple wafers, H2 install, SEM | 120 |
| Step 2 300 mm campaign (cash share) | 300 |
| Third-party safety review | 30 |
| H2-bleed plasma simulation (1 student-year) | 40 |
| **Total** | **590** |

The portfolio seed books Step 1 at $80k, sharing the student and some hardware.

**Gates:** month 8, month 10 and month 20. The IL moire overlay test (~$500k) is deferred until a periodic oxide cell wafer exists.

---

## 6. The $1M, 24-month plan

Month 0 is January 2027.

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 2027 | Rig build; Sandia CRADA; coupons; host-fab H2 safety plan; provisional #1; helium use-split requests to 2 fabs and 2 gas suppliers | — |
| Q2 2027 | He calibration; H2 matrix; Step 1b line installed; plasma simulation | He = 0.45 +/- 0.03 |
| Q3 2027 | Matrix done; 1b thermal runs | **M8: a_H2 ≥0.17** |
| Q4 2027 | 1b bleed etch; Step 2 host agreement; hazard analysis; provisionals #2-3; PCT on #1 | **M10: +/-2 K, ER ≤2%, selectivity ≤5%** |
| Q1 2028 | 300 mm H2 install; thermocouple maps; AAO coupon starts | Assessor sign-off |
| Q2 2028 | Patterned HAR etch; 100 wafer-hours; AAO anodization | — |
| Q3 2028 | Step 2 complete; AAO measured; a_H2 dataset published after filing | **M20: 300 mm pass; AAO ≥5.5 fF/pore at ≤40 nm** |
| Q4 2028 | Data package, SEMI S2 report, OEM term sheets, raise | Raise |

| Budget allocation | $k |
|---|---|
| Decisive experiment (section 5) | 590 |
| AAO coupon (Al sputter, pretexture, anodization, ALD, metrology) | 80 |
| IP: 3 provisionals + 1 PCT | 45 |
| Two lean founder stipends | 230 |
| Contingency | 50 |
| **Total** | **995** |

**Team**
- **Founder 1, gas-surface and plasma physicist.** Recruit from Sandia Engineering Sciences (the Trott group; DSMC modellers such as Torczynski and Gallis [UNVERIFIED-PK]), or from alumni of the Kushner (Michigan), Oehrlein (UMD) or Ruzic (UIUC CPMI) groups [UNVERIFIED-PK].
- **Founder 2, the recruited process expert.** An ESC or etch-process engineer with backside-gas and chuck-qualification experience, from Lam Research, Applied Materials or TEL. This person carries Step 2 and the OEM license.
- **Collaborators** [UNVERIFIED-PK except Trott and UMD]:
  - Sandia (rig, DSMC);
  - UMD Rubloff/Lee (AAO MIM);
  - Argonne Elam (ALD in pores);
  - Masuda (TMU);
  - Schattenburg (MIT) and Brueck (UNM) for the deferred IL work;
  - Chang (UCLA) for fluorocarbon surfaces.
- **Part-time:** a hydrogen-code EHS consultant, such as a Linde or Air Products alumnus or a TUV/UL-class assessor.
- **Pipelines:** NNCI staff, SRC alumni, DOE SCGSR, Activate.

**IP strategy**

- **Month 2:** a leak-compensated recipe (seal-leak feed-forward to the H-additive flows) and per-zone gas composition as a heat-transfer actuator. Both hold value whatever a_H2 is, and also for blends.
- **After the M8 gate:** accommodation-mapped control, and a chuck-face treatment drafted outside US 8,970,818.
- **Month 14:** the RFO-limited H2 safety architecture.
- **Later:** the AAO mold registered to pads, only after a KR/JP freedom-to-operate (FTO) search.

Publish the a_H2 dataset after filing, so it becomes the reference and pre-empts broad claims. Keep the recipe-trim tables as trade secrets.

FTO risks:
- US 10,395,963 names H2. That rules out a broad claim but probably blocks no use, and older He/N2 ESC patents are likely expired [ESTIMATE].
- US 8,970,818.
- The ASML-related H2 clamp filings.
- OEM multi-zone backside-gas portfolios [UNVERIFIED-PK].
- Micron's template capacitors.
- The SBIL patents and US 8,685,628.
- Canon's NIL portfolio.

---

## 7. After the demo

**Licensees and partners**

- **First licensees:** Lam, Applied Materials and TEL. The H2 option is a chuck-and-gas-stick retrofit plus a qualification package. ESC ceramic makers supply coated chuck faces [UNVERIFIED-PK which].
- **Gas suppliers:** Linde and Air Products sell both helium and on-site H2, and hold Korean long-term helium contracts [REPORTED, A2].
- **Memory makers:**
  - SK hynix and Samsung are the most exposed: Korea took 64.7% of its helium from Qatar.
  - Micron, for a helium-free line in Boise or Clay.
  - Kioxia, which uses the same HAR etch chambers for NAND.
- **Foundries:** TSMC, Intel, GlobalFoundries and Samsung Foundry use the same chucks.
- **Display makers:** Samsung Display, LG Display and BOE, mainly for the IL/NIL module and large-area chucks [UNVERIFIED-PK].

**What the round buys**

- **$10-15M:**
  - 2-3 dedicated 300 mm chambers (HAR etch and CVD);
  - a 10,000-wafer-pass marathon;
  - a full SEMI S2 assessment;
  - a beta-site retrofit of 5-10 chambers;
  - a blend product for CONDITIONAL chambers;
  - the deferred IL overlay test (~$500k).
- **$25-50M:** a helium-free, fluorocarbon-free capacitor module for one portfolio oxide cell (MARGIN STACK or AND-STACK). It covers the other helium uses (leak check, diluent, purge, anneal), adds AAO or carbon molds on a 1T1C test array, and launches a retrofit-kit business.

**Standards:**
- SEMI S2 (equipment EHS) and SEMI S6 (exhaust).
- NFPA 55 and NFPA 2.
- A proposed SEMI guideline for H2 backside gas [SPECULATIVE].
- JEDEC is not involved, because the memory cells are unchanged.

---

## 8. Resources and America

| Input | Today [REPORTED unless marked] | With this concept |
|---|---|---|
| Helium | Qatar ~30%, offline since March 2026, no restart date as of June; Korea 64.7% Qatar-sourced; ~6 weeks storage; spot $1,000-1,200/Mcf vs ~$500 | Backside use → 0; other uses still need substitutes |
| PFAS | 3M exit end-2025; EU restriction ~2028+; "no fully equivalent substitutes" | Capacitor HAR etch deleted; NF3 cleans remain |
| EUV | ASML sole source, ~65 tools in 2026; ~$290M and ~10 GWh/yr each; 5% of DRAM wafer kWh but 19-27% of 1c cost | 0 for F~40 nm oxide tiers; 1-beta already uses none |
| Gallium | ~98% Chinese; U.S. ban suspension ends 2026-11-27 | ZTO removes Ga (and In) |
| New dependencies | — | Iridium in PEM electrolysers (alkaline avoids it) [UNVERIFIED-PK]; Canon/DNP NIL; Y2O3 coatings unchanged |

**Energy and water** [ESTIMATE; conversion factors are prior knowledge]:
- **Hydrogen.** A 100k-wpm fab uses 1.43 g x 1.2M wafers = ~1.7 t of H2 a year. At ~55 kWh/kg that takes ~95 MWh, **0.006%** of the fab's ~1.56 TWh. Water is ~17 m3/yr.
- **Anodization.** 0.0026% of fab energy. Both are negligible, as A2 found.

**U.S. manufacturability:**
- The chambers come mostly from U.S. OEMs, and hydrogen is domestic.
- U.S. fabs are relatively buffered on helium: TrendForce notes Intel's "relative buffer" [REPORTED].
- **So the helium hedge mainly protects allied Korean and Taiwanese supply. For U.S. fabs the value is PFAS, EUV and resilience.**
- The demo is fully U.S.-buildable:
  - Sandia or a university for the rig;
  - Cornell CNF, UMD or UIUC for the small-tool test;
  - NY CREATES Albany (300 mm access for startups [REPORTED]) or Applied's META Center for Step 2;
  - UMD, Argonne CNM or NIST CNST for AAO.
- The weak link is lithography: NIL tools are Japanese, and no production IL vendor exists [UNVERIFIED-PK].

---

## 9. Kill criteria

Physics kills only; business findings re-scope instead. Start: January 2027.

| # | Kill (deadline) | Measurable condition | Revival condition |
|---|---|---|---|
| 1 | Pure H2 cooling (2027-08-31, M8) | a_H2 <0.10 (+/-0.02) on every film (SiO2, SiN, poly, CFx) against every chuck face (Al2O3, AlN, Y2O3) at 20-60 C | A chuck treatment reaches ≥0.20, or a 50/50 H2/He blend holds He-level h within 5% |
| 2 | Drop-in claim (2027-12-31, M12) | CONDITIONAL band, and no coating or blend reaches an effective ≥0.17 | A J-R chuck qualified at ≥60 Torr backside |
| 3 | H2 in HAR etch chambers (2027-10-31, M10) | A 2.5 sccm bleed shifts etch rate >2% or selectivity >5%, and the additive trim cannot restore both | A pumped seal band holds the leak ≤0.3 sccm |
| 4 | That host site (2028-02-29, M14) | Single-fault foreline above 25% LFL with RFO and purge | Diluted-exhaust design at another host |
| 5 | The OEM package (2028-08-31, M20) | At 300 mm and 2-5 kW: temperature outside +/-2 K anywhere on the wafer, any arc in ≥100 wafer-hours, or etch-rate drift >2% | A blend passes all three |
| 6 | AAO (2028-08-31, M20) | At ≤40 nm pitch: <2 um depth, or ≥1e-4 branched/missing pores, or pad attack, or <5.5 fF/pore | Ti/Nb stop layer; the carbon mold and stub cells cover meanwhile |
| 7 | IL (post-raise, 2029-12-31) | Per-field overlay >10 nm (3 sigma) at 300 mm | NIL ≤10 nm at ≤0.1 defects/cm2 |
| 8 | Carbon mold (post-raise, 2029-12-31) | AR ≥40, 20 nm holes, >2 nm bow/wiggle that boron doping and decks cannot fix | — |

**Re-scope, not kill (2027-06-30, M6).** If backside cooling is <1% of fab helium, sell H2 only as the helium-free closing step and as outage insurance. If it is >10%, the hedge value rises.

---

## 10. Sources

All URLs below are logged in `research/sources/*.jsonl`.

**Accommodation and gap physics**
- https://www.sandia.gov/research/publications/details/an-experimental-assembly-for-precise-measurement-of-thermal-accommodation-c-2010-11-01/
- https://sandia.gov/research/publications/details/determination-of-thermal-accommodation-coefficients-from-heat-transfer-meas-2010-10-01
- https://meetings-archive.aps.org/dfd/2006/ho/3/
- https://arxiv.org/pdf/2402.11977
- https://deepblue.lib.umich.edu/bitstream/handle/2027.42/70040/JCPSA6-58-10-4080-1.pdf;sequence=2
- https://uwaterloo.ca/microelectronics-heat-transfer-laboratory/publications/contributors/ssong
- https://doi.org/10.1103%2FPhysRev.40.78

**ESC patents and EUV clamps**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5810933
- https://patents.justia.com/patent/6170496
- https://patents.justia.com/patent/7017652
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9753463
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10395963
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8970818
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12174552
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12461452
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12717249
- https://patents.google.com/patent/US12189309

**Helium**
- https://wtop.com/news/2026/03/iran-war-halts-qatar-helium-output-threatening-global-tech-supply-chains/
- https://tomshardware.com/tech-industry/semiconductors/the-global-helium-shortage-is-a-direct-threat-to-chipmaking
- https://tomshardware.com/tech-industry/qatar-helium-shutdown-puts-chip-supply-chain-on-a-two-week-clock
- https://www.caixinglobal.com/2026-03-16/qatar-helium-shutdown-adds-new-risk-to-chip-supply-chain-102423361.html
- https://www.trendforce.com/news/2026/03/27/news-iran-conflict-reportedly-drives-50-helium-spot-price-surge-samsung-sk-hynix-on-high-alert/
- https://www.trendforce.com/news/2026/03/23/news-under-qatars-shadow-helium-crunch-hits-south-korea-harder-putting-samsung-sk-hynix-tsmc-in-spotlight/
- https://www.trendforce.com/news/2026/04/08/news-decoding-impact-asia-chipmakers-move-to-tackle-helium-strain-as-intel-gains-relative-buffer/
- https://iumi.com/newsletter-june-2026/qatari-helium-shortages/
- https://kr.linkedin.com/in/haneul-yu-49296072
- https://www.nasdaq.com/articles/war-or-peace-artificial-intelligence-ai-chip-industry-just-learned-depending-one-route-30

**PFAS**
- https://www.3m.com/3M/en_US/pfas-stewardship/uses-applications/
- https://www.sgs.com/news/2026/04/safeguards-05026-echa-consults-over-seacs-draft-opinion-on-pfas-restrictions-under-reach
- https://www.chemradar.com/en/service/detail/fop1tsgjw45c
- https://atkinson.cornell.edu/research/dashboard/optimizing-semiconductor-manufacturing-processes-to-eliminate-emissions-of-pfass-and-high-global-warming-potential-gases/

**Capacitor molds and channels**
- https://dx.doi.org/10.1038/nnano.2009.37
- https://www.mrs-j.org/pub/tmrsj/vol29_no3/vol29_no3_0855.pdf
- https://patents.google.com/patent/US7829410
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7126181
- https://deepblue.lib.umich.edu/items/e6ac2d99-46aa-444a-bc41-2851e63c965c

**Lithography and EUV**
- https://spiedigitallibrary.org/conference-proceedings-of-spie/12956/3012070/Nanoimprint-lithography-performance-advances-for-new-application-spaces/10.1117/12.3012070.full
- https://proceedings.spiedigitallibrary.org/conference-proceedings-of-spie/13177/1317708/Nanoimprint-performance-improvements-for-high-volume-semiconductor-device-manufacturing/10.1117/12.3034104.full
- https://bits-chips.com/magazine/bc202308/?pagenr=7
- https://www.trendforce.com/news/category/Semiconductors/page/5
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8685628
- https://www.marketbeat.com/instant-alerts/asml-q2-earnings-call-highlights-2026-07-15/
- https://siliconanalysts.com/analysis/chip-manufacturing-energy-cost

**Facilities**
- https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york
- https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale

**Without URLs:** textbook gas, Paschen, Baule and Corruccini relations; Tonucci 1992; MIT SBIL; IBM eDRAM micro sense amp (Barth, ISSCC 2007-08); names marked [UNVERIFIED-PK].
