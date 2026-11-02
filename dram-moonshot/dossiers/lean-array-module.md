# LEAN ARRAY MODULE: helium-free, PFAS-light, EUV-free process modules for periodic memory arrays

NEW DRAM Stage 3 dossier. Author: agent `dosw-lean-array-module`, 2026-11-02.

Inputs:
- Model `models/lean-array-module.py`, re-run today with exit 0. Its output is identical to `research/stage3/lean-array-module_model_output.md`. Re-run again after the red team, with a RED-TEAM REVISIONS block and a new section I.
- Red-team objections `research/redteam/rt_*.json`, answered in `research/redteam/responses_lean-array-module.json` (section 11).
- Notes `research/stage3/lean-array-module_notes.md`.
- Assumptions `research/assumptions/dos-lean-array-module.md`.

Tags:
- [REPORTED]: from a logged source, usually seen only as a search snippet.
- [ESTIMATE]: model arithmetic.
- [UNVERIFIED-PK]: prior knowledge, no URL.
- [SPECULATIVE]: not yet shown by anyone.

---

## 0. Header (revised after red team)

**Name:** LEAN ARRAY MODULE.

**Thesis:** Replace helium backside cooling with low-pressure hydrogen, delete the fluorocarbon capacitor etch, and pattern periodic layers without EUV, so an array line keeps running when Qatar, 3M or ASML stop.

**Thesis (revised after red team):** Replace helium backside cooling with low-pressure hydrogen. That is the one lever this concept owns. Delete the AR-60 capacitor-mold etch only where a planar or 80 nm-pitch oxide cell allows it, and pattern F~40 nm periodic layers without EUV only if a portfolio oxide cell wins.

**Rank:** 8 of 10, EV 40 (S2xP4xD5).

**Rank inputs (revised after red team):** P4 → P3 gives EV 30 (S2xP3xD5). The S2 now rests on the helium lever alone.

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

**Role changes (revised after red team):**
- **N-21 AAO** is retargeted to an 80-86 nm pitch for F~40 nm oxide 1T1C tiers. The 1-beta-pitch AAO leg is **KILLED** (RT-CIRC-02).
- **N-26 ZTO** is dropped from the seed. Gallium (~60 kg/yr per fab) is stockpiled instead.
- **I-07130 IL** stays deferred, and now depends on a portfolio cell winning.
- **The red-team top-ups I-12302 and I-12627** were considered and not adopted (section 11).

**Verdicts (revised after red team)**

- **PHYSICALLY POSSIBLE? Yes, with lower odds.** No physics forbids H2 backside cooling. But the Baule 0.27 is a translational prior, and with rotational accommodation the effective a_H2 is **0.19-0.21**, against a GO line of 0.17. On the worst of four films, P(GO) is ~35-55% (P3, was P4). Fallbacks are D2, H2/He blends and an asymmetric chuck face. AAO works only at a pitch of 80 nm or more.
- **STEP CHANGE IF IT WORKS? Narrowed to one owned lever.** Backside helium goes from 7.5 L/wafer to 0 in Si-access lines (75-90% of it in oxide-cell lines). That is ~3% (1-11%) of DRAM's helium and the closing step to a helium-free line, at ~1.0x $/bit. Fluorocarbon etch gas falls ~25-30%, and only for planar or 80 nm-pitch oxide cells (it was "capacitor fluorocarbon -> 0"). EUV goes to 0 only if a portfolio F~40 nm oxide cell wins.
- **PROVABLE WITH $1M IN 24 MONTHS? Partly.**
  - The H2 physics: **yes**, through a $630k three-step experiment by month 20. It now adds plasma-pretreated, cryogenic, edge-zone and IGZO-monitor tests.
  - The 80 nm AAO cup: a first look only.
  - IL: no.
  - An investable IP position: **no** from data alone. It needs a paid JDA by month 10.
- **FINAL STATUS: DOWNGRADED** (section 11).

**Original Stage-3 verdicts (superseded by the red team; kept for the record)**

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

## 2. The physics and the numbers (revised after red team)

### 2.1 Gas-gap conductance

**Heat load.** 3.0 kW bias x 0.80 heat fraction / 0.0707 m2 = **34.0 kW/m2** [ESTIMATE].

**Model.** h = k/(d + g_w + g_c) + 50 W/m2K, with a gap d of 10 um. The Smoluchowski jump distance is g = (2-a)/a x 2gamma/(gamma+1) x lambda/Pr.

**Helium baseline.** At 15 Torr and a = 0.45 (Sandia [REPORTED]):
- g = 3.44 x 1.25 x 9.8 um / 0.667 = **63.6 um per surface**. The gap therefore acts like ~137 um.
- h = 0.155/137e-6 + 50 = **1,180 W/m2K**.
- The wafer sits 34,000/1,180 = **28.8 K** above the chuck.

**Free-molecular ratio.** Per unit accommodation, conductance scales as (gamma+1)/(gamma-1)/sqrt(M). That gives 2.0 for He and 4.18 for H2, a ratio of **2.09x**. The jump model matches Corruccini within 0.0%.

**(Revised after red team, RT-DEV-01.)** The 2.09x assumes that H2 fully exchanges its rotational energy with the surface. Translation carries 2kT per molecule and H2 rotation carries kT. So when the rotational accommodation is r times the translational one, the ratio per unit *translational* accommodation is 2.09 x (4+2r)/6. At r = 0.1-0.3 that is **1.46-1.60x** (model I1). The fitted coefficient in `h_gas()` is an effective one that already folds this in, so the table below stays valid at a given effective a_H2.

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

**Prior (revised after red team, RT-DEV-01).** The 0.27 is translational. ORNL measured the rotational accommodation of H2 and D2 on graphite at ~0.05-0.2 [REPORTED]. That gives an effective a = 0.27 x (4+2r)/6 = **0.19-0.21** at r = 0.1-0.3, so the 0.20 planning value is the central estimate, not a pessimistic one.
- **Parity pressure:** 17.9-19.8 Torr, which is inside the 22.5 Torr GO pressure. The margin over the 0.168 break-even is only +0.02-0.04.
- **Odds:** a lognormal prior (1-sigma factor 1.5) puts P(a >= 0.168) at 88% for the old median and **66%** for the effective one. The GO needs the *worst* of four films to pass, which gives **43-66%**. I add an adsorbate tail (H on W fell from 0.54 to 0.14) and carry **P3 (~35-55%)**.
- **Cryogenic chucks** (RT-PROC-04): with gas at 220 K, normal H2 has gamma 1.43, and the free-molecular ratio falls to 1.99x. The GO line moves to **0.175** (drop-in 0.251, clamp limit 0.102; model I4).
- **D2 diagnostic** (new): D2 has helium's mass, so Baule gives it a translational coefficient of ~0.45, and its rotational quanta are half of H2's. That gives a_eff ~0.35-0.39 and **1.06-1.21x helium's h** at 15 Torr. Running H2 against D2 on the same coupon separates the rotational term from the mass term. D2 is also a fallback for CONDITIONAL chambers, if it is recaptured; its cost is [SPECULATIVE].

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

**Where the leak sits on the wafer (revised after red team, RT-PROC-01).** I modelled the gas above the wafer as one-dimensional radial advection and diffusion (model I2). The H2 diffusivity is 7,900-21,000 cm2/s at 30-80 mTorr, and the Peclet number over 1 cm is 0.04-0.12.
- **Edge:** the leak enters at r = R, so the wafer edge sees the fully mixed value above: H/F of 0.5-1.2% at 500 sccm, or 0.17-0.40% at 1,500 sccm.
- **Centre:** 0.42-0.75x of the edge value.
- **Bevel gap:** close to pure H2.
- **So:** the H fraction is not above the chamber average, but a 1.3-2.4x radial gradient lands on the outer die, and global etch-rate criteria could miss it.
- **Edge-He guard zone:** He or Ar in the outer zone (r > 130 mm) and H2 inside. H2 entering the plasma then drops to ~0, and H2 still replaces **73%** of that chamber's backside helium.

**Oxide channels (revised after red team, RT-DEV-02, RT-CIRC-01).** At the viscous bound the leak carries 5 sccm of H atoms. Against recipes that already carry H, that is small: 0.3% of PECVD SiN (~1,600 sccm-equivalent) and 0.2% of TEOS (~2,100). In O2-plasma ALD or Ar PVD over an exposed oxide channel it becomes the dominant H source.
- **Rule:** use H2 only in chambers whose wafers have no exposed oxide channel, or whose recipe already carries at least 100x the leak's H. All other chambers keep He or Ar.
- **Helium still replaced** (model I3):

| Line | H2 share, no edge guard | With an edge guard in HAR chambers |
|---|---|---|
| Si-access DRAM (today) | 100% | 92% |
| Oxide-cell line, 10-25% of chucked steps exposed | 75-90% | 69-83% |

**Flammability.** Dump plus leak (42 sccm) in a 50.5 slm foreline is **2.1% of the LFL**. A single fault, limited by the restricting orifice (RFO) to 200 sccm, is **10% of the LFL**. The usual alarm point is 25%.

### 2.4 The honest size of the helium lever

**Volume.** 150 chucked steps x 2.5 min x 20 sccm = **7.5 L of helium per DRAM wafer** [ESTIMATE; range 3-30 L]. Samsung's HeRS first line, ~4.7 t/yr on ~1.2M wafers, is ~22 L/wafer recovered. That is the same order [REPORTED, weak attribution].

**Share.** The fleet uses 166k m3/yr. That is **~3% (1-11%) of DRAM's pro-rata helium**, taken as 160M m3 x 22.5% semiconductors x 17% DRAM.

**Cost.** **$0.32/wafer**, or 104 u$/GB against $1.48/GB. H2 costs $0.007/wafer.

**Insurance value.** A 100k-wpm fab books ~$32M a day. Retrofitting 1,500 chambers at $50k costs $75M, which pays back after **2.4 days** of avoided stoppage [ESTIMATE].

**Insurance value (revised after red team, RT-PROC-05, RT-IND-04).** The $50k per chamber was hardware only. Model I5 adds requalification of 30-80 chamber families at $0.5-3M each [ESTIMATE].

| Case | Cost | Payback in days of full stoppage |
|---|---|---|
| Brownfield, low-high | $90-315M | 2.8-9.9 |
| Brownfield, mid | $150M | **4.7** (was 2.4) |
| Greenfield, H2 qualified during the ramp | ~$82M | 2.6 |

- **Lead time:** requalification takes 6-12 months, so it cannot be done in a crisis.
- **When it pays:** backside cooling becomes the binding helium use only when a fab's cut exceeds 89-99% (97% at a 3% share), after ~6 weeks of storage.
- **Expected value** [SPECULATIVE]: at a 0.5-3% annual chance of a binding 30-day cutoff, it is $5-29M/yr per fab. That recovers a brownfield retrofit in 5-32 years, and a greenfield one in 3-17 years.
- **Qatar:** it has restarted part of Helium 2. Output is estimated at below ~30% of normal, and two damaged LNG trains need 3-5 years of repair [REPORTED, gasworld 2026]. So the tightness persists, but a full stoppage is not the base case.
- **The pitch** is therefore dual qualification on greenfield lines, not a brownfield retrofit.

**Critic correction carried.** I-10762 claimed H2 removes "~60-80% of fab helium demand". It is nearer 3%. Under a partial cut, a fab keeps backside cooling and sheds other uses first (leak check → H2/N2 tracer, PECVD diluent → Ar). H2 matters in a near-total cutoff, or as the last step to a fully helium-free line. **It is a tail-risk hedge, not a cost lever.** The backside share is unverified.

### 2.5 Secondary modules (corrected numbers)

**AAO (N-21).** The 1-beta cell is 1,070 nm2, so the hexagonal pitch is 35.2 nm, anodized at ~14 V. The pore is 0.65 x pitch, and the mid-plane diameter after the liner is 11.9 nm. With C = 3.9 eps0 pi d h/EOT at EOT 0.55 nm, a 2.5 um pore gives **5.84 fF** (parity with 1-beta's 5.4 fF; 76 mV signal; 67 ms retention at a 13 fA tail). A 3.0 um pore gives **7.01 fF** (+30%; 88 mV; 81 ms). **B2-01's +37-64% holds only at 40 nm pitch.** At the 1-beta pitch, AAO buys parity to +30%. Its real value is the deleted fluorocarbon etch and the deleted support lattice. Anodization uses 34 Wh/wafer, 0.0026% of fab energy (B2-01's 8 Wh counted the array area only).

**AAO (revised after red team, RT-CIRC-02, RT-DEV-03, RT-PROC-03, RT-CIRC-03).**

*Why the 1-beta pitch fails.* The pore is 22.8 nm. ZrO2 at EOT 0.55 nm and k 40 is 5.64 nm thick, and the outer TiN is 3 nm. That leaves a **5.6 nm inner-electrode core at AR ~450** (539 at 3.0 um). The mold itself is AR 109-131, which takes 3.1-4.5x the AR-squared ALD dose of today's AR-62 pillar. Resistance is not the problem: the core's distributed RC is ~0.9 ns. The fill is. **The 1-beta-pitch AAO leg is killed.**

*The retarget.* F = 40 nm oxide 1T1C tiers at an 80 nm square pitch (DUV- or imprint-pretextured) or an 86 nm hexagonal pitch:
- **Geometry:** pore 52-56 nm, 5 nm TiN electrodes.
- **Capacitance:** **7.2-7.9 fF/um**, so 5.4 fF needs only **0.68-0.75 um, a cup AR of 12-14**. A 20.7 nm hole remains inside the top electrode.
- **Barrier:** at ~32 V it is ~35 nm. Wet etching alone would widen the pore by ~70 nm, which is more than the pitch. So a current-limited voltage ramp-down first thins it to ~3-5 nm, and a short H3PO4 dip then opens it, widening the pore ~8-10 nm [UNVERIFIED-PK]. No fluorocarbon or chlorine plasma is used.
- **Overlay:** the budget at this pitch is ~10 nm, which an ordinary 193i pretexture layer meets.

*Missing-pore budget* (16 Gb die with on-die SEC):

| Missing or branched pores | Dead cells per die | 136-bit words with 2 or more dead cells |
|---|---|---|
| 1e-4 | 1.7M | 12,321 |
| 1e-6 | 17k | ~1 |

The kill line moves to **<=1e-6**. Proving it takes ≥3e6 counted pores, which is 0.019 mm2 at an 80 nm pitch.

*Retention on A1's convention* (50 mV end-of-retention signal, model I7):

| Capacitor | Fresh signal | Retention |
|---|---|---|
| 1-beta pillar | 71 mV | 64 ms |
| 35 nm AAO cup | 76-88 mV | 80-123 ms (1.25-1.9x) |
| 80 nm AAO cup, 7.2 fF on a 1 aA IGZO tail | 90 mV | ~1,670 s |

So the 35 nm cup gives no refresh relief once a 2x VRT guard is held. At 80 nm, the retention comes from the oxide access device, not from the cup.

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

**Table rows revised after red team:**

| Metric | 1-beta DDR5 | LEAN (revised) | Change |
|---|---|---|---|
| Backside He replaced | — | 100% (Si line); 75-90% (oxide line) | oxide-exposed steps keep He/Ar |
| Cs, Si-access AAO | 5.4 fF | killed (5.6 nm core, AR ~450) | — |
| Cs, oxide 1T1C AAO at 80 nm | — | 5.4 fF at 0.75 um (AR 14) | no AR-60 etch |
| Fluorocarbon etch gas | 3,200 scc/wafer [ESTIMATE] | 2,300-2,340 (planar or oxide cell); 6,000 (3D cell) | -27-28%, or +88% |
| Retrofit payback | — | 4.7 days brownfield; 2.6 greenfield | was 2.4 |

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

**GO / NO-GO additions (revised after red team):**
- The GO must hold on the **worst plasma-pretreated** film (RT-DEV-04).
- Cryogenic chambers need a_H2 ≥0.175 at -70 to 0 C, judged as a separate GO (RT-PROC-04).
- The Step 1b thermocouple-wafer a_H2 must match the rig within **±0.03**.
- Step 2 adds edge-zone pass criteria at r = 140-148 mm (RT-PROC-01): tilt ≤0.1°, bottom CD within 1 nm, bow in spec.
- IGZO monitor wafers at 2x the leak must show **ΔVt ≤5 mV and no Ioff-tail shift** (RT-DEV-02, RT-CIRC-01).

### 2.8 Fluorocarbon inventory and gallium (revised after red team)

**Fluorocarbon inventory** (model I8 [ESTIMATE], scc of C4F6/C4F8/CF4/CHF3 per wafer, NF3 cleans excluded). The capacitor mold is ~38% of a 1-beta wafer's fluorocarbon etch gas: 1,200 of 3,200 scc.

| Flow | Fluorocarbon etch gas vs 1-beta |
|---|---|
| MARGIN STACK-class planar oxide 4F2 with stub | **-27%** (stub, VCT-pillar and buried-bitline etches remain) |
| F40 oxide 1T1C with an 80 nm AAO cup | -28% |
| AND-STACK-class 3D cell | **+88%** |
| 3D cell with TEL's HF/PF3 cryo etch [REPORTED: "greatly reduces" CF partial pressure] | ~-12%, but that is the industry's lever, not LEAN's |

**LEAN deletes the AR-60 step, not PFAS-class etch** (RT-PROC-02, RT-CIRC-04).

**Gallium** (model I9). A fab of oxide cells needs 10 nm of IGZO at 3x the wafer area, over 5 tiers at 30% utilisation. That is **~60 kg/yr** per 100k-wpm fab. A 10-year stockpile costs ~$0.4M, under an hour of fab revenue. Gallium exposure is therefore a stockpile item, so ZTO's leakage risk (RT-DEV-05) is not worth taking.

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

## 5. The decisive experiment (revised after red team)

**Question.** Does H2 cool like helium on real, plasma-modified films, including on cryogenic chucks, without upsetting the etch at the wafer edge, degrading oxide channels or creating a fire hazard?

Changes from the Stage-3 version are tagged with the objection ids they answer.

**Step 1. Accommodation matrix (months 1-8, ~$145k, was $100k; binary gate).**
- **Where:** a university gas-surface lab, using Sandia's Trott TAC assembly as the template. Sandia is the preferred CRADA partner.
- **Rig:** a parallel-plate cell with a 50 mm guarded hot plate carrying a wafer coupon and a cold plate carrying a chuck-ceramic coupon. Gaps of 5-50 um are read capacitively. Pressure runs 0.05-50 Torr on capacitance manometers.
- **New in the rig:**
  - An LN2-cooled cold plate reaching **-70 C** (RT-PROC-04).
  - A load-locked side chamber that **plasma-pretreats** coupons (Ar, O2, C4F8 polymer, H2) and transfers them without an air break (RT-DEV-04).
- **Gases:** He (calibrate to 0.45 +/- 0.03), H2, **D2** (separates the rotational term; RT-DEV-01), N2, Ar, and 25/50/75% H2-He blends.
- **Wafer faces:** native-oxide Si, SiO2, SiN, poly, CFx-exposed and post-clean backsides, plus production backsides pulled from a partner's HAR flow and measured as received.
- **Chuck faces:** Al2O3, AlN, Y2O3. Temperatures -70/-20/20/40/60 C.
- **Analysis:** fit a_wafer and a_chuck with the model's `h_gas()`, to +/-0.02.
- **Pass/fail (effective symmetric a_H2, worst pretreated film):** ≥0.17 GO; 0.10-0.17 CONDITIONAL; <0.10 NO-GO. The cryogenic set is a separate GO at ≥0.175.
- **Data policy** (RT-IND-02): the data stays confidential until the provisionals are filed and a JDA is signed.

**Step 1b. Small-tool plasma test (months 4-10, ~$145k, was $120k).**
- **Where:** a university ICP etcher with a 150/200 mm ESC (Cornell CNF, UMD or UIUC class).
- **Install:** an H2 line with RFO, sensor and purged plenum.
- **Thermal run:** thermocouple wafer, He vs H2, 5-30 Torr, 1-3 kW. **Gate:** the in-plasma a_H2 matches the rig within ±0.03 (RT-DEV-04).
- **Bleed run:** 0-5 sccm H2 into a C4F6/C4F8/O2/Ar oxide etch on AR 10-20 coupons. Measure etch rate, selectivity and profile, with OES of H-alpha and CF2. Also make a first look at tilt and CD in the outer 10 mm (RT-PROC-01).
- **Oxide-channel monitor** (new; RT-DEV-02, RT-CIRC-01): IGZO TFTs from a university TFT line (W/L ≥0.1/0.05 um), run through the H2-cooled chamber at 2x the predicted leak, against He controls. Measure:
  - ΔVt;
  - the Ioff tail at 85 C;
  - the PBTI shift;
  - RTN capture and emission spectra from 10 us to 10 s, the timescales of sensing and retention, because H-induced traps show up there first.
- **Pass:**
  - wafer temperature within +/-2 K of He;
  - etch-rate drift ≤2% and selectivity drift ≤5% at 2.5 sccm;
  - **ΔVt ≤5 mV, with no Ioff-tail shift** at 2x the leak.

**Gate at month 10 (new; RT-IND-01, RT-IND-02):** a signed JDA with paid NRE, or a royalty on H2-capable chucks and gas sticks, from an OEM or a gas supplier. Without one, Step 2 runs at NY CREATES Albany as thermal and edge maps only, and the program seeks grant co-funding.

**Step 2. 300 mm chamber swap (months 10-20, ~$300k cash plus partner in-kind).**
- **Where:** NY CREATES Albany NanoTech, or an OEM demo lab (Lam, Applied's META Center, TEL), but the OEM lab only under the JDA.
- **Sequence:**
  - SEMI S2 / NFPA 55 / NFPA 2 hazard analysis with a third-party assessor;
  - centre and edge thermocouple-wafer maps at 2-5 kW;
  - AR ≥40 HAR oxide etch on patterned wafers, with etch rate, selectivity, bow and CD against He;
  - **edge-zone metrology at r = 140-148 mm at 2x the leak** (RT-PROC-01);
  - an **edge-He guard-zone split** (outer zone on He, H2 inside);
  - **300 mm IGZO monitor wafers**;
  - ≥100 wafer-hours of foreline logging;
  - the partner's **estimate of per-chamber requalification cost and time** (RT-PROC-05).
- **Pass:**
  - +/-2 K across the wafer;
  - etch-rate drift ≤2% and selectivity drift ≤5%;
  - **at the edge: tilt ≤0.1°, bottom CD within 1 nm and bow in spec, versus He**;
  - ΔVt ≤5 mV;
  - zero arcs and ≤10% LFL in single fault.

| Decisive-experiment budget (revised after red team) | $k |
|---|---|
| Step 1 rig hardware (manometers, guarded heater, vacuum, DAQ; +cryo plate, +plasma pretreat and vacuum transfer) | 95 |
| Step 1 coupons, films, D2 | 20 |
| Step 1 lab fees and student (or Sandia SPP) | 30 |
| Step 1b tool time, thermocouple wafers, H2 install, SEM; +IGZO monitor TFTs and electrical test | 145 |
| Step 2 300 mm campaign (cash share; edge metrology and monitors included) | 300 |
| Third-party safety review | 30 |
| Edge-transport simulation (was a $40k H2-bleed simulation; the radial model is now in `models/`) | 10 |
| **Total** | **630** |

The portfolio seed books Step 1 at $80k, sharing the student and some hardware.

**Gates:** month 8 (accommodation), month 10 (plasma, oxide monitor and JDA) and month 20 (300 mm). The IL moire overlay test (~$500k) is deferred until a periodic oxide-cell wafer exists.

**AAO coupon** (re-specified; $70k, in the section-6 budget; RT-DEV-03, RT-PROC-03, RT-CIRC-02):
- **Structure:** an 80 nm-pitch, 1 mm2 e-beam pad array, with a pretexture aligned to the pads.
- **Barrier:** opened by ramp-down plus H3PO4, proven by pad contact resistance.
- **Fill:** TEM of a conformal TiN/ZrO2/TiN to the pore bottom.
- **Electrical:** ≥5.4 fF per pore at ≤1 um depth, and ≤1e-7 A/cm2.
- **Defects:** ≤1e-6 missing or branched pores over ≥3e6 counted pores.
- **Shorts and outgassing:** comb structures for Al-residue shorts, and TDS to 450 C for sulfate and oxalate outgassing.

---

## 6. The $1M, 24-month plan

Month 0 is January 2027. Rows and tables marked "(revised after red team)" follow section 5.

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 2027 | Rig build; Sandia CRADA; coupons; host-fab H2 safety plan; provisional #1; helium use-split requests to 2 fabs and 2 gas suppliers | — |
| Q2 2027 | He calibration; H2 matrix; Step 1b line installed; plasma simulation | He = 0.45 +/- 0.03 |
| Q3 2027 | Matrix done; 1b thermal runs | **M8: a_H2 ≥0.17** |
| Q4 2027 | 1b bleed etch; IGZO monitor run; Step 2 host agreement; hazard analysis; provisionals #2-3; PCT on #1 | **M10: +/-2 K, ER ≤2%, selectivity ≤5%, rig-vs-plasma a_H2 within ±0.03, ΔVt ≤5 mV; paid JDA or Albany-only Step 2 (revised after red team)** |
| Q1 2028 | 300 mm H2 install; thermocouple maps; AAO coupon starts | Assessor sign-off |
| Q2 2028 | Patterned HAR etch; 100 wafer-hours; AAO anodization | — |
| Q3 2028 | Step 2 complete; AAO measured; a_H2 dataset published after filing **and after the JDA (revised after red team)** | **M20: 300 mm pass incl. edge zone; AAO ≥5.4 fF/pore at ≤1 um, 80 nm pitch, ≤1e-6 missing pores (revised after red team)** |
| Q4 2028 | Data package, SEMI S2 report, OEM term sheets, raise | Raise |

| Budget allocation (revised after red team) | $k |
|---|---|
| Decisive experiment (section 5; was 590) | 630 |
| AAO coupon at 80 nm pitch (Al sputter, e-beam pads and pretexture, anodization, ALD, TEM, pore count, TDS; was 80) | 70 |
| IP: 3 provisionals + 1 PCT | 45 |
| JDA legal (new, RT-IND-02) | 15 |
| Two lean founder stipends | 230 |
| Contingency (was 50) | 10 |
| **Total** | **1,000** |

The contingency is thin. If the month-10 JDA brings partner NRE, it replaces the Step 2 cash share. If not, Step 2 shrinks to thermal and edge maps at Albany (~$150k), which frees ~$150k.

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

**IP strategy (revised after red team, RT-IND-01, RT-IND-02).**
- **Filing order:** the asymmetric-accommodation chuck face (wafer 0.10 against chuck 0.45 reaches parity at 23 Torr) and the edge-He guard / per-zone composition move ahead of any OEM meeting.
- **Publication:** the dataset is published only after a JDA or after month 20.
- **Second counterparty:** a gas supplier (Linde or Air Products, which sell both helium and on-site H2).
- **The honest IP position is narrow.** The program is pitched as a co-funded resilience program (JDA/NRE plus CHIPS R&D, Natcast or DOE grants), not as a royalty company.

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

## 9. Kill criteria (revised after red team)

Physics kills only; business findings re-scope instead. Start: January 2027. Rows marked RT are new or changed after the red team.

| # | Kill (deadline) | Measurable condition | Revival condition |
|---|---|---|---|
| 1 | Pure H2 cooling (2027-08-31, M8) | Effective a_H2 <0.10 (+/-0.02) on every film (SiO2, SiN, poly, CFx), **after plasma pretreatment (RT)**, against every chuck face (Al2O3, AlN, Y2O3) at 20-60 C | A chuck treatment reaches ≥0.20; a 50/50 H2/He blend holds He-level h within 5%; or **D2 with recapture passes (RT)** |
| 1c | **H2 on cryogenic chucks (RT; 2027-08-31, M8)** | Effective a_H2 <0.102 at -70 to 0 C on every film | Blend or D2 at -70 C; keep He on cryo chambers only |
| 2 | Drop-in claim (2027-12-31, M12) | CONDITIONAL band, and no coating or blend reaches an effective ≥0.17 | A J-R chuck qualified at ≥60 Torr backside |
| 3 | H2 in HAR etch chambers (2027-10-31, M10) | A 2.5 sccm bleed shifts etch rate >2% or selectivity >5%, and the additive trim cannot restore both | A pumped seal band holds the leak ≤0.3 sccm, **or the edge-He guard zone (H2 into the plasma ~0, 73% of He still replaced) (RT)** |
| 3b | **H2 near oxide channels (RT; 2027-10-31, M10). Re-scope, not kill** | IGZO monitor ΔVt >5 mV or an Ioff-tail shift at 85 C, at 2x the leak | Those chamber classes keep He/Ar; H2 covers 75-90% of backside He in an oxide line, 100% in a Si line |
| 3c | **Rig vs plasma (RT; M10)** | In-plasma a_H2 differs from the rig by >0.03 **and** the in-plasma value is <0.10 | The rig is recalibrated on pretreated surfaces; kill #1 is re-judged on in-plasma data |
| 4 | That host site (2028-02-29, M14) | Single-fault foreline above 25% LFL with RFO and purge | Diluted-exhaust design at another host |
| 5 | The OEM package (2028-08-31, M20) | At 300 mm and 2-5 kW: temperature outside +/-2 K anywhere on the wafer, any arc in ≥100 wafer-hours, etch-rate drift >2%, **or edge tilt >0.1°, bottom CD >1 nm or bow out of spec at r = 140-148 mm (RT)** | A blend or the edge-He guard passes all of them |
| 6 | AAO **at 80-86 nm pitch for oxide 1T1C (RT; was ≤40 nm)** (2028-08-31, M20) | Barrier not opened without fluorocarbon or Cl plasma; <5.4 fF/pore at ≤1 um; >1e-7 A/cm2; **>1e-6 missing or branched pores (RT; was 1e-4)**; Al-residue shorts; or outgassing at 400 C | Ti/Nb/W stop layer; the carbon mold and stub cells cover meanwhile |
| 6x | **AAO at the 1-beta 35 nm pitch: KILLED by the red team (RT-CIRC-02)** | 5.6 nm inner core at AR ~450 under 3 nm TiN; parity Cs at best; no retention gain | TEM-verified TiN/ZrO2/TiN fill of ≥2 um pores at ≤36 nm pitch, ≥5 fF/pore, ≤1e-7 A/cm2 |
| 7 | IL (post-raise, 2029-12-31) | Per-field overlay >10 nm (3 sigma) at 300 mm | NIL ≤10 nm at ≤0.1 defects/cm2 |
| 8 | Carbon mold (post-raise, 2029-12-31) | AR ≥40, 20 nm holes, >2 nm bow/wiggle that boron doping and decks cannot fix | — |
| 9 | **ZTO (RT): dropped from the seed, not tested** | — | Anyone reports Lg ≤40 nm ZTO made at ≤400 C with SS ≤90 mV/dec and Ioff ≤10 aA at 85 C |

**Re-scope, not kill (2027-06-30, M6).** If backside cooling is <1% of fab helium, sell H2 only as the helium-free closing step and as outage insurance. If it is >10%, the hedge value rises.

**Re-scope, not kill (RT; 2027-10-31, M10).** With no paid JDA or NRE, Step 2 runs at Albany as thermal and edge maps only, and the program seeks grant or OEM-internal funding (RT-IND-01, RT-IND-02).

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

**Added after the red team** (logged in `research/sources/resp-lean-array-module.jsonl`):
- https://ornl.gov/publication/measurement-and-modeling-hydrogen-molecule-ro-vibrational-accommodation-e-204
- https://lac913.epfl.ch/epsppd3/2008/pdf/P2_004.pdf
- https://www.gasworld.com/story/air-liquide-expects-qatar-restart-to-ease-helium-supply-pressures/2255652.article/
- https://www.gasworld.com/story/qatar-to-resume-lng-production-within-weeks-says-pm/2252968.article/
- https://www.agbi.com/industry/2026/03/qatari-lng-shutdown-puts-11-of-global-helium-supply-at-risk/
- https://semiengineering.com/cryogenic-etch-a-key-enabler-of-3d-nand/
- https://eetimes.itmedia.co.jp/ee/articles/2604/09/news030_6.html
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11075084

---

## 11. Red-team outcome

Four adversarial reviewers raised **18 objections** against this dossier: DEV (device physicist), PROC (DRAM/3D-NAND process veteran), CIRC (DRAM circuit designer) and IND (industry strategist and investor). Their files are `research/redteam/rt_*.json`.
- **None is deleted.** Every one is answered in `research/redteam/responses_lean-array-module.json`.
- **The model was re-run with exit 0.** Its new section I holds the variants, and a "RED-TEAM REVISIONS" block in the inputs lists every changed input.
- **Searches:** 3 of the 3 WebSearch queries were used.

**Dispositions:** REFUTED 0 | ACCEPTED-MITIGATED 8 | ACCEPTED-DOWNGRADE 9 | ACCEPTED-KILL 1 (a named leg: AAO at the 1-beta pitch).

| Id | Severity | Disposition | One-line action |
|---|---|---|---|
| RT-DEV-lean-array-module-01 | MAJOR | ACCEPTED-DOWNGRADE | Effective a_H2 prior 0.27 → 0.19-0.21 (rotational accommodation); P4 → P3; D2 added to the rig |
| RT-DEV-lean-array-module-02 | MAJOR | ACCEPTED-MITIGATED | Chamber exclusion rule (no exposed oxide channel, or recipe H ≥100x the leak) plus IGZO monitors at 2x leak |
| RT-DEV-lean-array-module-03 | MAJOR | ACCEPTED-DOWNGRADE | AAO retargeted to 80-86 nm pitch oxide 1T1C (cup AR 12-14, barrier by ramp-down + H3PO4); Si-access cells lose the PFAS-free capacitor |
| RT-DEV-lean-array-module-04 | MINOR | ACCEPTED-MITIGATED | Plasma-pretreated, vacuum-transferred coupons; a ±0.03 rig-vs-plasma gate at M10 |
| RT-DEV-lean-array-module-05 | MINOR | ACCEPTED-DOWNGRADE | ZTO dropped from claims and seed; gallium (~60 kg/yr per fab) stockpiled |
| RT-PROC-lean-array-module-01 | MAJOR | ACCEPTED-MITIGATED | Edge metrics at r = 140-148 mm (tilt ≤0.1°, CD ±1 nm, bow); edge-He guard zone as fallback |
| RT-PROC-lean-array-module-02 | MAJOR | ACCEPTED-DOWNGRADE | PFAS claim cut to -25-30% of fluorocarbon etch gas, for planar or 80 nm-pitch oxide cells only |
| RT-PROC-lean-array-module-03 | MAJOR | ACCEPTED-MITIGATED | 80 nm pitch with a 193i/imprint pretexture (10 nm budget); kill line 1e-4 → 1e-6 over ≥3e6 pores; comb and TDS tests |
| RT-PROC-lean-array-module-04 | MINOR | ACCEPTED-MITIGATED | Matrix extended to -70 C (cryo GO line 0.175, a separate GO) |
| RT-PROC-lean-array-module-05 | MINOR | ACCEPTED-MITIGATED | Requalification added (payback 4.7 days brownfield, 2.6 greenfield); greenfield dual-qualification; partner cost estimate |
| RT-CIRC-lean-array-module-01 | MAJOR | ACCEPTED-MITIGATED | H2-vs-He IGZO/ZTO FET split after channel formation; ΔVt <5 mV; He kept in 10-25% of steps of an oxide line |
| RT-CIRC-lean-array-module-02 | MAJOR | ACCEPTED-KILL | AAO capacitor at the 1-beta 35 nm pitch killed (5.6 nm core, AR ~450); revival = CIRC's TEM-fill test |
| RT-CIRC-lean-array-module-03 | MINOR | ACCEPTED-DOWNGRADE | Restated on A1's convention (80-123 ms, no relief with a 2x VRT guard); refresh credit goes to oxide access only |
| RT-CIRC-lean-array-module-04 | MINOR | ACCEPTED-DOWNGRADE | Fluorocarbon inventory per cell added; thesis says "deletes the AR-60 step", not "deletes PFAS etch" |
| RT-IND-lean-array-module-01 | FATAL (venture) | ACCEPTED-DOWNGRADE | Not a physics kill (mission rule); venture re-scoped to a JDA/NRE- and grant-co-funded resilience program; narrow IP |
| RT-IND-lean-array-module-02 | MAJOR | ACCEPTED-MITIGATED | Paid-JDA gate before Step 2; data confidential until the JDA; chuck-face and edge-guard claims filed first |
| RT-IND-lean-array-module-03 | MAJOR | ACCEPTED-DOWNGRADE | Step change narrowed to backside He; PFAS and EUV relabelled as conditional options for portfolio cells |
| RT-IND-lean-array-module-04 | MINOR | ACCEPTED-DOWNGRADE | Insurance restated: binds only above an 89-99% cut; EV $5-29M/yr per fab; Qatar partly restarted (<30% of normal) |

**Redesigns adopted**

1. **Edge-He guard zone.** He or Ar runs in the outer backside zone (r > 130 mm) and H2 inside. H2 entering the plasma drops to ~0, and 73% of that chamber's backside helium is still replaced (RT-PROC-01).
2. **Oxide-channel exclusion rule.** H2 is used only where no oxide channel is exposed, or where the recipe already carries ≥100x the leak's H. H2 replaces 100% of backside He in Si lines and 75-90% in oxide lines (RT-DEV-02, RT-CIRC-01).
3. **D2 as a diagnostic and fallback.** It separates rotational from mass effects, and gives a_eff ~0.35-0.39 and 1.06-1.21x helium's h (RT-DEV-01).
4. **A rig that measures the surfaces that matter.** It adds plasma pretreatment, vacuum transfer and -70 C operation (RT-DEV-04, RT-PROC-04).
5. **AAO retargeted.** It moves from the 35 nm Si pitch to an 80-86 nm oxide-1T1C pitch, using a DUV/imprint pretexture, a barrier opened without plasma, and a 1e-6 defect line (RT-DEV-03, RT-PROC-03, RT-CIRC-02).
6. **ZTO swapped for a stockpile.** ZTO is dropped, and gallium is stockpiled (RT-DEV-05).
7. **A new go-to-market.** Greenfield dual-gas qualification replaces brownfield retrofits (RT-PROC-05, RT-IND-04).
8. **A JDA before Step 2,** with a confidential dataset and the narrow claims filed first (RT-IND-01, RT-IND-02).

**Top-up ideas considered**
- **I-12302 (plate-strip sensing; ~135 mV against ~14 mV; planar Micron prior art).** It is a 3D-array sensing circuit. It does not touch a process module and does not rescue Si-access AAO retention, so it is not adopted.
- **I-12627 (two series write transistors; tail p → p² if defects are independent).** It does not stack the storage-node junction/GIDL leakage that dominates Si-access tails. In oxide cells it belongs to the cell dossiers, not to LEAN, so it is not adopted.

**Revised step-change claim.** The axis is still supply-chain exposure, not $/bit (~1.0x).
- **The owned lever:** backside helium goes from **7.5 L/wafer to 0** in Si-access lines, and ~75-90% of the way in oxide-cell lines. That is **~3% (1-11%) of DRAM's helium**, and it is the closing step to a fully helium-free line. Its value is option value for tail risk: ~$82M per greenfield fab, or $150M (90-315) brownfield.
- **Conditional options, not LEAN's own claims:**
  - Fluorocarbon etch gas **-25-30%** (was "capacitor fluorocarbon → 0"), only for planar or 80 nm-pitch oxide cells. 3D cells come out +88% unless the industry's cryo HF/PF3 etch is adopted.
  - EUV → 0, only on F~40 nm oxide tiers if a portfolio cell wins.
- **Size of the downgrade:** three chokepoints to zero becomes one owned lever plus two conditional options. The probability of the core GO falls from P4 (~50-75%) to P3 (~35-55%).

**Revised decisive experiment** (section 5): $630k by month 20, inside a $1.0M, 24-month plan.
- **Step 1, the rig (M1-8, $145k):** plasma-pretreated and production-backside coupons, -70 to 60 C, He/H2/D2/blends. GO is ≥0.17 on the worst film (≥0.175 on the cryo set).
- **Step 1b, the small tool (M4-10, $145k):**
  - in-plasma a_H2 within ±0.03 of the rig;
  - H2 bleed with ER ≤2% and selectivity ≤5%;
  - IGZO TFT monitors at 2x the leak: ΔVt ≤5 mV, no Ioff-tail shift at 85 C, and RTN spectra from 10 us to 10 s.
- **Gate at M10:** a paid JDA, or an Albany-only Step 2.
- **Step 2, 300 mm (M10-20, $300k):**
  - ±2 K maps;
  - AR ≥40 etch with edge tilt ≤0.1°, bottom CD ±1 nm and bow in spec at r = 140-148 mm;
  - an edge-guard split and IGZO monitors;
  - ≥100 wafer-hours, zero arcs and ≤10% LFL in single fault;
  - the partner's requalification estimate.
- **AAO coupon ($70k):** 80 nm pitch, no fluorocarbon barrier opening, TEM fill, ≥5.4 fF at ≤1 um, ≤1e-6 missing pores.

**Revised verdicts**
- **PHYSICALLY POSSIBLE? Yes, with lower odds.** The effective a_H2 prior is 0.19-0.21 against a 0.17 GO line, so P(GO) is ~35-55%. AAO is possible only at a pitch of 80 nm or more, and the 1-beta-pitch leg is killed.
- **STEP CHANGE IF IT WORKS? Narrowed.** On supply-chain exposure: backside helium → 0, which is ~3% of DRAM's helium and the closing step to a helium-free line, at 1.0x $/bit. PFAS etch gas falls -25-30% and EUV goes to 0, both only conditionally.
- **PROVABLE WITH $1M? Partly.** Yes for the H2 module ($630k, month 20). A first look only for the 80 nm AAO cup. No for IL. No for an investable IP position without a paid JDA.

**FINAL STATUS: DOWNGRADED.** The core H2 physics stands, with lower odds and four tests it was missing. The step change narrows to the backside-helium hedge, for four reasons:
- the PFAS and EUV claims depend on borrowed portfolio cells;
- AAO at the 1-beta pitch is killed;
- ZTO is dropped;
- the venture IP is thin, so the program is re-scoped as an OEM- or gas-supplier-co-funded resilience effort.

**Revival to STANDS:**
- the rig shows an effective a_H2 ≥0.20 on SiO2, SiN and CFx after plasma pretreatment, which is DEV's test;
- **and** M6 data shows backside cooling is >10% of fab helium;
- **and** a partner pays NRE before Step 2.
