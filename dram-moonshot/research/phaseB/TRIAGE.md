# C0: First physics triage of the Phase B idea set

**Agent:** `C0-triage` (lead device physicist) · **Written:** 2026-11-01 · **Inputs:** `B1`-`B5` idea cards and notes, Phase A maps · **Output data:** `research/phaseB/ideas_master.json` · **Arithmetic:** `research/models/C0_triage_checks.py` (python3 exits 0) · **Sources:** `research/sources/C0-triage.jsonl` (5 searches, snippets only) · **Assumptions:** `research/assumptions/C0-triage.md`

Judged on physics only. No idea was marked down for business, market, time-to-revenue or founder-fit reasons (MISSION.md).

## Summary

- **101 cards in, 97 ideas out.** Four cross-lens duplicates were merged (lineage below).
- **Verdicts:** **66 ALIVE**, **31 ALIVE-SPECULATIVE**, **0 DEAD-PHYSICS**.
- **Why no idea is dead:** before writing cards, the five lens agents had already rejected, folded or parked 78 ideas in their notes (B1 15, B2 13, B3 14, B4 14, B5 22), most of them on physics and each with a revival condition. I checked every surviving card against physical bounds. None breaks one.
- **What did fail:** 8 sub-claims or variants fail on physics. They are recorded in `dead_subclaims` so each idea can continue in its re-scoped form (list below).
- **Verdict rules.**
  - **ALIVE:** every required effect has been shown somewhere, within about 10x of what is needed. What remains is integration, yield or measurement. The `revival_condition` field holds the kill test.
  - **ALIVE-SPECULATIVE:** at least one required effect is contested, or not yet shown within about 100x of need. The effect is named in the reason, and the measurement that would promote the idea is given.
  - **DEAD-PHYSICS:** the core claim violates a bound, or hits a known show-stopper with no workaround.

### Verdicts by family

| Family | ALIVE | ALIVE-SPEC | DEAD |
|---|---|---|---|
| Less charge needed (sensing / bitline) | 10 | 2 | 0 |
| Data-aware memory | 10 | 2 | 0 |
| Stacking / interconnect | 8 | 0 | 0 |
| 3D cell / oxide gain cell | 7 | 0 | 0 |
| Patterning | 5 | 2 | 0 |
| More charge per area | 2 | 4 | 0 |
| Quasi-volatile tunnel-write | 0 | 6 | 0 |
| Refresh / retention policy | 6 | 0 | 0 |
| Spin | 1 | 3 | 0 |
| Memory where the compute is | 4 | 0 | 0 |
| 3D process add-on | 4 | 0 | 0 |
| Cryogenic | 3 | 1 | 0 |
| Ferroic | 1 | 2 | 0 |
| Mechanical | 0 | 3 | 0 |
| Capacitor process (no HAR etch) | 2 | 1 | 0 |
| Fab / capital model | 3 | 0 | 0 |
| Serial (shift) addressing | 0 | 2 | 0 |
| Ionic / molecular | 0 | 2 | 0 |
| Static latch | 0 | 1 | 0 |

## The cross-cutting physics insight

**Reading a bit is a circuit problem that is already solved in principle. Writing a bit is an endurance problem, and endurance decides almost every open verdict.**

1. **Read side.**
   - The ~17,700 electrons in today's bit exist to beat bitline capacitance and offset, not noise.
   - kTC noise on a 35 fF bitline is ~82 e⁻ rms (C0-11), and image sensors count 0.22 e⁻ rms.
   - So every idea that cuts the charge needed is ALIVE with no new physics. That covers short or segmented bitlines, charge transfer, active neutralisation, ECC margin and in-cell gain: N-04, N-40, N-48, N-61, N-27, N-62, N-89, N-90.
   - They deliver a 3-10x shorter capacitor, which then fits a 3D tier.
2. **Write side.**
   - A DRAM-class cell must survive 3.2e8 cycles (1 s refresh) to ~7e13 (hot row at 1% duty) in 10 years (C0-1).
   - **About half of the ALIVE-SPECULATIVE verdicts (15 of 31) hinge on one unmeasured number: cycling endurance.** These are N-01, N-10, N-12, N-13, N-14, N-16, N-17, N-18, N-20, N-81, N-83, N-85, N-86, N-87, N-96.
   - The charge-fluence rule sorts them. A write that pushes ~1 fC through an amorphous insulator a few nm² to a few hundred nm² in area survives only 1e2-1e5 cycles (C0-2).
   - Writes that can plausibly reach DRAM endurance go through one of four routes:
     - a **semiconductor channel** (transistor-written charge: gain cells, CCDs);
     - a **crystalline or vacuum barrier**;
     - **non-contact mechanics**;
     - **magnetic order**.
3. **The bridge between them.**
   - DRAM needs only ~44-54 kT of barrier for 1 s across a whole die, against 64-73 kT for 10-year non-volatility (B5-00).
   - The 20-30 kT of slack is what can buy speed and endurance. That is why the "quasi-volatile" retunings (N-10, N-14, N-20, N-86) are the right shape.
   - They live or die on the same endurance measurement.

**Shared materials doubt across 3D oxide ideas.**
- Hydrogen and PBTI Vt drift: a 20 mV budget is ~3 ppm of the hydrogen in one PECVD SiN tier (B3-17).
- It is not a physics wall, but it decides whether the multi-level density claims hold. Those claims belong to N-28, N-35, N-37, N-43, N-48, N-57, N-05.
- The cheapest experiment in the whole set is a joint test: multi-level retention and drift maps at 85-110 °C on an H-lean versus a PECVD mold (N-56).

## The 10 most exciting (physics headroom × size of step × novelty × cheap decisive test)

| Rank | ID | Idea | Step-change claim | Novelty | Verdict | Why it excites |
|---|---|---|---|---|---|---|
| 1 | N-04 | Charge-transfer pre-sense on an oxide 1T1C (B1-04) | Cs 5.4 -> 0.5 fF (pillar 1.3 -> ~0.12 um) on an unchanged 512-cell bitline | TWIST | ALIVE | Biggest capacitor cut with no new physics: 5.4 -> 0.5 fF (1.3 um -> ~0.12 um) on an unchanged 512-cell bitline, so array efficiency is kept. Noise is 19 sigma (C0-11). Stacks with N-62 (ECC) toward ~0.25 fF, still 9.5 sigma. One MPW proves it. |
| 2 | N-43 | Coaxial 4F2 2T0C (B3-04) | Coaxial 4F2 2T0C (storage node = core gate of the read channel): 1b parity at 4 bit-tiers with single-exposure ArF | TWIST | ALIVE | 1-beta density from 4 bit-tiers at single-exposure ArF (F = 40 nm, no EUV); 2 b x 8 tiers is 3.9x. Ordinary GAA device physics; the risk (0.16 fF node kickback) is circuit-addressable. Best EUV-independence and U.S.-manufacturability lever among the 3D cells. |
| 3 | N-08 | Vertical oxide CCD string (B1-08) | Transistor-less vertical oxide CCD string: 4.2-8.3x 1b density; serial 32-128 ns access | NEW | ALIVE-SPECULATIVE | The largest deposition-only density step (4-8x) with no transistor or capacitor per bit. It hinges on one number nobody has published, charge-transfer efficiency in an oxide channel, which a university fab can measure in months. Open territory. |
| 4 | N-82 | Racetrack in the capacitor hole (B5-02) | Racetrack in DRAM capacitor holes: electroplated domain-wall wires, 10-25 bits per cell footprint, no refresh | TWIST | ALIVE-SPECULATIVE | Turns DRAM's worst process step (the 60:1 hole) into a 10-25-bit vertical shift register with no refresh. Cylindrical-wire Bloch-point walls already move at >600 m/s. The bet is deterministic shifting at 20 nm, a clean physics question. |
| 5 | N-41 | Carrier-is-memory (B3-02) | The BSPDN carrier slot becomes a hybrid-bonded DRAM wafer: 45-53 GB per accelerator at ~0.28 pJ/bit | NEW | ALIVE | ~12x lower interface energy (3.5 -> 0.28 pJ/b, saving ~200-410 W per accelerator) by using a bonded-wafer slot that backside power makes mandatory anyway. Known physics in a new combination. |
| 6 | N-21 | AAO-Cap (B2-01) | Self-ordered anodic-alumina capacitor mold: Cs 7.4-8.9 fF from 2.5-3 um pores, no fluorocarbon HAR etch | NEW | ALIVE | Replaces the fluorocarbon 60:1 plasma etch and SiN support lattice with self-ordering electrochemistry (~8 Wh/wafer), giving +37-64% Cs. Directly answers the founder's resource question (PFAS, capital) with physics already shown in energy-storage AAO capacitors. |
| 7 | N-01 | AFE-reservoir ZrO2 stub (B1-01) | 3-6x signal charge/area; capacitor 1.3 um -> 0.21-0.42 um; Hf-free | TWIST | ALIVE-SPECULATIVE | 3-6x signal charge per wall area from the dielectric fabs already deposit, Hf-free. A one-number decision: full-transition endurance (best ~5e9 seen; ~1e12 needed), testable on MIM coupons in months. |
| 8 | N-48 | Sandwich stack (c-Si sense layer every 16 tiers) (B3-09) | Smart-Cut c-Si sense layer every 16 oxide tiers: in-tier capacitor 600 -> 31-59 nm; ~10x 1b at 64 tiers | NEW | ALIVE | Bounds bitline length in 3D, so the in-tier capacitor shrinks 10-20x (600 -> 31-59 nm) and 64 tiers give ~10x 1-beta density on known parts. Hydrogen blocking is the materials risk, with N-49 as the H-free fallback. |
| 9 | N-81 | Click-RAM (B5-01) | Click-RAM: bistable buckled 2D/ALD nanoribbon as a suspended gate; zero refresh, aJ writes, hammer-immune | NEW | ALIVE-SPECULATIVE | The cleanest charge-free bit: a 45-80 kT elastic barrier, aJ intrinsic writes, no refresh and no row hammer. Its risks (q^4 strain sensitivity, stiction, ring-down, fatigue) are quantified mechanics, not unknown physics. |
| 10 | N-62 | ECC-paid capacitor (B4-01) | Design the array for raw BER 1e-4 + BCH t=8: capacitor 2x shorter (1,300 -> 640 nm) | TWIST | ALIVE | Halves capacitor height by architecture alone (raw BER 1e-4 + BCH). Its FPGA error-tail study is the cheapest decisive experiment in the set, and it calibrates every margin- and refresh-relaxing idea (N-63, N-66, N-42). |

**Honourable mentions:**
- N-03 (IGZO gated-diode strip: a 3D tier with no capacitor module).
- N-35 (76-152 GB of oxide memory inside the logic BEOL).
- N-89 (negative-capacitance bitline).
- N-09 (vacuum-nanogap floating node).
- N-32 (maskless interference lithography).
- N-42 (cool-spec DRAM, the cheapest demo).

## Merges (lineage)

| Final ID | Primary | Absorbed | Why merged |
|---|---|---|---|
| N-51 | B3-12 photonic periphery wafer | B4-14 photonic periphery wafer | Identical mechanism and target. |
| N-52 | B3-13 coil-stacked HBM | B5-18 TSV-free inductive stacking | Same inductive-link stack. B5-18's reach arithmetic is kept as the constraint: direct links fail at 16-high, relayed links cost ~6 pJ/b average. |
| N-42 | B3-03 coolant-backed memory wafer | B4-13 thermal arbitrage (35 °C sled) | Same physics: retention bought by temperature. Two placements. |
| N-11 | B1-11 capacitive-NDRO FE gain cell | B2-06 flat AlBN FE capacitor | B2-06 reads its FE capacitor capacitively through a 2T gain cell, which is B1-11's cell in a different material. Its 5x Pr does not enter a non-switching read. |

The short-bitline family (N-04, N-19, N-27, N-40, N-48, N-49, N-61, N-62, N-89, N-90) and the "memory where the compute is" hosts (N-35, N-41, N-50, N-57) were **not** merged. They share a goal but use different mechanisms, which Phase C should compare head to head. They are tagged with a shared `family` instead.

## Cross-lens conflicts adjudicated

- **B1 vs B2-05 (N-25).** B1 killed a protonic stub as "thermodynamically contradictory". That argument holds for storing information in ion position. It does not hold for a double-layer capacitor, whose state is electronic charge and whose retention is set by electronic leakage. Verdict: ALIVE-SPECULATIVE. The pseudocapacitive variant is dead on faradaic endurance.
- **B1 vs B5-04 (N-84).** B1 killed a pinned-diode storage node on full-well grounds. B5's vertical well answers that objection. A new physics objection replaces it: about 2-3e18 cm⁻³ doping at 0.5-1 MV/cm. Verdict: ALIVE-SPECULATIVE.
- **B2 vs B5-11 (N-91).** B2 rejected DNA templates on defect rate. Proofreading assembly is not ruled out by physics. Verdict: ALIVE-SPECULATIVE, with a 500x defect gap stated.
- **B1 vs B5-02 (N-82).** B1 parked the vertical racetrack. Cylindrical-wire Bloch-point data from 2019-2023 (>600 m/s) justify a card. Verdict: ALIVE-SPECULATIVE.
- **B3-13 vs B5-18 (N-52).** Both are right. Direct links lose on coil area, and relayed links lose on energy above ~8-high.
- **B1 vs B5-09 (N-89).** B1 killed a passive parallel-FE canceller. B5-09 is an active negative-impedance amplifier, which is legitimate. Verdict: ALIVE.
- **A3/B4 cryogenic kill vs B5-14 to B5-17.** A3's kill was on system energy for warm data centres. These cards are judged inside their cold-compute scope.

## Sub-claims and variants that fail on physics (the idea survives re-scoped)

- **N-11** (B1-11/B2-06): B2-06: 1-4 fC of 2Pr*A is available only to a switching (destructive) read, not to the capacitive read the card specifies.
- **N-19** (B1-19): ~16x array-energy reduction: the thermal switching floor (>=2-17 fJ per decision) exceeds the bitline energy saved.
- **N-25** (B2-05): 100 uF/cm2 pseudocapacitive WO3/MnO2 skin: faradaic insertion at 1e12-1e15 cycles is battery-class chemistry (B5 R11).
- **N-52** (B3-13/B5-18): Direct (non-relayed) inductive links through 12-16-high stacks: 62-562 mm2 of coil per die.
- **N-76** (B4-17): 1.33x vs an optimal 4-bit scalar quantizer on i.i.d. weights exceeds the 1.22x rate-distortion bound.
- **N-81** (B5-01): Sub-ns write as stated: needs Q <=~10 or active ring-down control.
- **N-83** (B5-03): Si-compatible deep levels holding >=1 s at 85 C: impossible (<=0.56 eV in a 1.12 eV gap).
- **N-87** (B5-07): Amorphous 'soft-landing' tunnelling coating: 1e2-1e4 writes by charge fluence.

## Full table

Novelty labels: KNOWN, KNOWN+TWIST, TWIST and NEW follow each card's own novelty field; "speculative" marks cards whose authors flagged them `[SPECULATIVE]`. Each idea's full reasoning, numbers and promote/kill test are in `ideas_master.json` (`triage_reason`, `revival_condition`).

| ID | Name (source cards) | Lens | Novelty | Step-change claim | Triage | One-line physics reason |
|---|---|---|---|---|---|---|
| N-01 | AFE-reservoir stub capacitor (Hf-free antiferroelectric ZrO2) (B1-01) | B1 cell physics | TWIST | 3-6x signal charge/area; capacitor 1.3 um -> 0.21-0.42 um; Hf-free | **ALIVE-SPECULATIVE** | AFE charge is real; full-transition endurance (best ~5e9 seen) is 10-1e4x short. |
| N-02 | Temperature-hardened negative-capacitance stub (FE/DE superlattice) (B1-02) | B1 cell physics | KNOWN+TWIST | 2.5-4.7x capacitance/area via stabilized NC; pillar 1.3 -> 0.43-0.65 um | **ALIVE-SPECULATIVE** | Static NC at ns in multi-domain HZO is contested; 4.7x sits at the divergence point. |
| N-03 | IGZO gated-diode strip: a capacitor-module-free 3D DRAM tier ('two-gate NAND-like DRAM') (B1-03) | B1 cell physics | NEW | No 3D capacitor module; 3D break-even 26 -> 9-14 tiers; ~5 fJ/access | **ALIVE** | MOS-accumulation storage + one transfer: standard physics; 60-80 mV signal is thin. |
| N-04 | Charge-transfer pre-sense on a long bitline: sub-fF cells without shortening the bitline (B1-04) | B1 cell physics | TWIST | Cs 5.4 -> 0.5 fF (pillar 1.3 -> ~0.12 um) on an unchanged 512-cell bitline | **ALIVE** | Known circuit; bitline kTC 82 e- vs 1,560 e- signal (19 sigma). |
| N-05 | 2-bit/cell 1T1C on an oxide access device (B1-05) | B1 cell physics | TWIST | 2 bits per 1T1C cell on an oxide access device; 1.8-2.8x density | **ALIVE** | 4-level 1T1C died on Si leakage, which IGZO removes. |
| N-06 | Vertical oxide semi-floating-gate 1T1D gain cell (4F2, capacitor-less, stackable) (B1-06) | B1 cell physics | TWIST | 4F2 stackable semi-floating-gate gain cell; 2.5x per-tier density vs 10F2 2T0C | **ALIVE** | Needs >=0.95 eV oxide diode barrier (1.0 eV -> ~230 s at 85 C). |
| N-07 | 1T + 2 tunnel-diode latch: a refresh-free static cell at near-DRAM density (B1-07) | B1 cell physics | TWIST | Refresh -> 0 via a static two-tunnel-diode latch at near-DRAM density | **ALIVE-SPECULATIVE** | No NDR diode with PVCR>=3 at J_peak~1 A/cm2 known; not forbidden. |
| N-08 | Vertical oxide CCD string: transistor-less 3D charge-shift memory (B1-08) | B1 cell physics | NEW | Transistor-less vertical oxide CCD string: 4.2-8.3x 1b density; serial 32-128 ns access | **ALIVE-SPECULATIVE** | CTE>=0.9999 in amorphous oxide unmeasured (no published data found). |
| N-09 | Nanogap (vacuum/air) tunnel-barrier floating node: flash-like retention without oxide wear (B1-09) | B1 cell physics | NEW (speculative) | Non-volatile vacuum-gap floating node: ns writes at 6-8 V, trap-free barrier | **ALIVE-SPECULATIVE** | Vacuum barrier escapes wear; needs <=0.2 nm gap control and a <=3 eV stable emitter. |
| N-10 | Direct-tunnel charge-trap '3D AND' DRAM built with 3D-NAND tools (B1-10) | B1 cell physics | TWIST | Direct-tunnel charge-trap 3D AND on NAND tools: 2.7-7.2x density; refresh 16-1,562x less | **ALIVE-SPECULATIVE** | Amorphous tunnel layer at 1e10-1e12 writes vs charge-fluence limit. |
| N-11 | Capacitive-NDRO ferroelectric gain cell (HZO; AlBN flat-capacitor variant) (B1-11/B2-06) | B1 cell physics + B2 | TWIST | Capacitive non-destructive FE read: refresh/restore -> 0 for read-mostly data (read endurance >1e11) | **ALIVE** | Capacitive NDRO demonstrated (>1e11 reads); AlBN Pr is irrelevant to NDRO. |
| N-12 | Sliding-ferroelectric 2D gain channel (fatigue-free polarization) (B1-12) | B1 cell physics | TWIST | Sliding-ferroelectric 2D gain cell: ion-free switching, endurance path to 1e12-1e15 | **ALIVE-SPECULATIVE** | Ion-free switching, but domain stability <=50 nm and 85 C retention unshown. |
| N-13 | Lithium-niobate-on-insulator conductive-domain-wall memory (B1-13) | B1 cell physics | KNOWN+TWIST | LNOI conductive-domain-wall NDRO cell at 0.4-1 V (energy/endurance play, not density) | **ALIVE-SPECULATIVE** | LN DW physics fine (0.4 V at 20 nm); ns endurance at 1e12 unmeasured. |
| N-14 | VCMA crosspoint MRAM with deliberately relaxed (refreshed) retention (B1-14) | B1 cell physics | TWIST | VCMA crosspoint MRAM, 4 decks, 1 s retention: 2.9x 1b density, 6-20 fJ writes | **ALIVE-SPECULATIVE** | Needs VCMA >=300 fJ/Vm with high TMR (today ~30-100). |
| N-15 | Shared-rail SOT tier on hot logic (4 MTJs per write rail) (B1-15) | B1 cell physics | KNOWN+TWIST | Shared-rail SOT tier on logic: 2.2-2.6x SRAM density, >1e15 cycles, zero standby at 125 C | **ALIVE** | SOT >1e15 cycles demonstrated; SRAM-class density only. |
| N-16 | Protonic gain cell (H+ in WO3 behind a PSG electrolyte) (B1-16) | B1 cell physics | TWIST | Protonic WO3 gain cell: non-volatile 2-4 b/cell, 5 ns writes | **ALIVE-SPECULATIVE** | Faradaic proton insertion at 1e12 cycles unshown; H vs IGZO. |
| N-17 | Redox-molecule pseudocapacitor with natural multi-level plateaus (ZettaCore revival) (B1-17) | B1 cell physics | KNOWN+TWIST | Redox-molecule pseudocapacitor stub: 2.4-4.9x charge/area, 2 b/cell plateaus | **ALIVE-SPECULATIVE** | Solid electrolyte at >=1e8/s redox unshown (liquid-only data). |
| N-18 | NEMS relay access switch: zero-GIDL DRAM cell (B1-18) | B1 cell physics | KNOWN+TWIST | NEMS relay access switch: zero GIDL, 10-100 s retention with today's capacitor, hammer-immune | **ALIVE-SPECULATIVE** | Zero-leak gap sound; nm contact endurance 1e13-1e15 unshown. |
| N-19 | NbO2 Mott threshold switch as an in-stack local sense element (B1-19) | B1 cell physics | NEW (speculative) | NbO2 threshold switch as a one-device local sense amp per 64-cell bitline | **ALIVE-SPECULATIVE** | Comparator possible if sigma<=10 mV; energy claim dead (>=2-17 fJ thermal floor). |
| N-20 | 2D-barrier quasi-volatile 1T cell (seconds-to-minutes retention traded for endurance) (B1-20) | B1 cell physics | TWIST | 2D-barrier quasi-volatile 1T: 10-100 s retention traded for endurance; refresh 156-1,562x less | **ALIVE-SPECULATIVE** | Needs 1e12 cycles through hBN; gap 1.8e5-1.8e8x. |
| N-21 | AAO-Cap: self-ordered anodic-alumina capacitor mold (B2-01) | B2 materials | NEW | Self-ordered anodic-alumina capacitor mold: Cs 7.4-8.9 fF from 2.5-3 um pores, no fluorocarbon HAR etch | **ALIVE** | Anodization at ~16 V gives 40 nm interval; AAO MIM shown. |
| N-22 | Ru-free rutile: SnO2-templated TiO2 short-stub capacitor (B2-02) | B2 materials | KNOWN+TWIST | Ru-free rutile TiO2 on doped SnO2: EOT 0.34-0.40 nm, capacitor 27-38% shorter, zero Ru/Hf | **ALIVE** | Published templating; leakage window exists for 64 ms Si cells. |
| N-23 | Hf-free MPB zirconia with work-function-biased operating point (B2-03) | B2 materials | TWIST | Hf-free MPB zirconia, asymmetric electrodes: k 40 -> ~56; pillar 1.29 -> 0.97 um | **ALIVE-SPECULATIVE** | MPB small-signal k contested (2026 JMCC); step only 1.34x. |
| N-24 | Capacitor-first inverted flow with perovskite super-k (B2-04) | B2 materials | NEW | Capacitor-first perovskite (BST, k~150): 3-4x shorter capacitor, oxide transistors built on top | **ALIVE** | Cap-first order avoids thermal conflict; thin-film k collapse is the risk. |
| N-25 | Solid-state proton double-layer nano-capacitor [SPECULATIVE] (B2-05) | B2 materials | NEW (speculative) | Solid proton double-layer nano-capacitor: 2-3x (EDL) charge/area; 0.41 um stub | **ALIVE-SPECULATIVE** | EDL stores electronic charge, so B1's contradiction does not apply; ns EDL unshown. |
| N-26 | Gallium-free, indium-lean oxide channels (ZTO / SnO2 / ITZO) for gain cells and VCT (B2-07) | B2 materials | KNOWN+TWIST | Ga-free (ZTO/SnO2/ITZO) oxide channels; >=1,500 s retention already shown | **ALIVE** | ZTO 2T0C >1,500 s shown; materials engineering. |
| N-27 | In-tier complementary-oxide sense amplifiers (no-bond short bitlines) (B2-08) | B2 materials | NEW | In-tier complementary-oxide sense amps: Cs need 5.4 -> 1.2 fF, ~27x lower bitline energy, no bond | **ALIVE** | Ordinary circuit physics; auto-zero beats 20-50 mV TFT mismatch. |
| N-28 | Ge-free, NAND-line 3D oxide gain cell (oxide/nitride mold + channel replacement) (B2-09) | B2 materials | TWIST | NAND-line, Ge-free 3D oxide gain cell: 1.1-3.4x density at 16 tiers, no EUV or epitaxy | **ALIVE** | Pieces demonstrated (Kioxia, IMECAS); recess uniformity is process. |
| N-29 | Fluorine-free carbon mold for capacitor holes and sacrificial 3D tiers (B2-10) | B2 materials | TWIST | Fluorine-free amorphous-carbon HAR molds; PFAS-class gases out of capacitor/channel modules | **ALIVE** | a-C molds standard as hardmasks; bow/oxidation are engineering. |
| N-30 | DSA honeycomb: block-copolymer self-assembly for the capacitor/channel hole lattice (B2-11) | B2 materials | KNOWN+TWIST | Block-copolymer DSA honeycomb replaces 1-2 EUV/SAQP array layers | **ALIVE** | BCP hex lattice native; defectivity is kinetic. |
| N-31 | NIL-only periodic cell wafer (bonded periphery makes every layer imprintable) (B2-12) | B2 materials | KNOWN+TWIST | NIL-only periodic cell wafer: 2-3 imprints replace 4-6 EUV/SAQP layers | **ALIVE** | All-periodic cell wafer suits NIL; overlay/defects are tooling. |
| N-32 | Maskless interference lithography for an all-periodic cell wafer (B2-13) | B2 materials | NEW | Maskless 193i interference lithography for the cell wafer: 4F2 at F~17-18 nm, no masks, no EUV | **ALIVE** | 193i two-beam gives ~35 nm half-pitch; overlay is the bet. |
| N-33 | ASD self-aligned landing pads and top contacts (B2-14) | B2 materials | TWIST | Area-selective-deposition self-aligned landing pads: -1 to -2 critical litho layers | **ALIVE** | Nucleation-delay ASD; selectivity is a process window. |
| N-34 | Defect-budget co-design: 100x pattern-defect tolerance to unlock cheap patterning (B2-15) | B2 materials | KNOWN+TWIST | Design for a 1e-4 random-defect fraction with t=2 BCH: 100x pattern-defect tolerance for +6.25% bits | **ALIVE** | Coding theory; clusters need sparing. |
| N-35 | Main memory inside the logic die's own metal stack (monolithic BEOL oxide gain cells) (B2-16) | B2 materials | TWIST | 8-16 tiers of 3-bit oxide gain cells in the logic BEOL: 76-152 GB per 800 mm2 die, 3.5 -> 0.2 pJ/bit | **ALIVE** | BEOL oxide memory over logic exists; MLC drift at 105 C is materials. |
| N-36 | BEOL-only cell mini-line on reusable glass carriers, bonded to trailing-node periphery (B2-17) | B2 materials | NEW | BEOL-only cell line on reusable glass carriers, bonded to 28-65 nm periphery: 2.5-3.3x lower cell capex | **ALIVE** | Carriers and ~1 um bonding exist. |
| N-37 | Trailing-node fab reuse: CMOS-under-array deep-tier MLC oxide memory at F=65 nm (B2-18) | B2 materials | NEW | Depreciated 65 nm fab + CMOS-under-array 16-24 tiers of 3-4 b oxide cells: 1.8-2.7x 1b density | **ALIVE** | CuA proven in NAND; 3-4 b/cell drift budget ~20 mV is materials. |
| N-38 | Panel-level 3D oxide memory [SPECULATIVE] (B2-19) | B2 materials | NEW (speculative) | Panel-level (Gen 3.5) 64-128-tier oxide memory imprinted at F~100 nm: ~45 TB per panel | **ALIVE** | Density from tiers at F=100 nm; no new physics. |
| N-39 | Self-assembled tier stack: parallel block-copolymer lamellae + sequential infiltration synthesis [SPECULATIVE] (B2-20) | B2 materials | NEW (speculative) | Self-assembled tier stack: one BCP coat -> 25-80 parallel lamellae converted by SIS | **ALIVE-SPECULATIVE** | Defect-free 25-80-period lamellae never shown. |
| N-40 | MSB-DRAM: hierarchical 64-cell bitlines with sense amps bonded under the array (B3-01) | B3 3D/process | NEW | 64-cell local bitlines muxed 8:1 to bonded sense amps: capacitor 3-4x shorter; bond pitch 0.74-1.05 um | **ALIVE** | Charge-sharing arithmetic on known parts. |
| N-41 | Carrier-is-memory: the mandatory carrier wafer of backside-power logic becomes a DRAM wafer (B3-02) | B3 3D/process | NEW | The BSPDN carrier slot becomes a hybrid-bonded DRAM wafer: 45-53 GB per accelerator at ~0.28 pJ/bit | **ALIVE** | BSPDN carrier faces the signal BEOL; W2W yield is engineering. |
| N-42 | Cool-spec DRAM (coolant-backed memory wafer or 35 C memory sled) (B3-03/B4-13) | B3 3D/process + B4 | TWIST / NEW | Cool-spec DRAM: run memory 10-50 K cooler (in-wafer microchannels or a 35 C sled) for 4-18x retention | **ALIVE** | Arrhenius x3.7-18 (85->35 C); tail Ea may cap at 3-5x. |
| N-43 | Coaxial 4F2 2T0C: the storage node is the core gate of a read-channel shell (B3-04) | B3 3D/process | TWIST | Coaxial 4F2 2T0C (storage node = core gate of the read channel): 1b parity at 4 bit-tiers with single-exposure ArF | **ALIVE** | GAA oxide FET around a metal core; 0.16 fF kickback is circuit work. |
| N-44 | Mirror-VCT: 4F2 oxide cells above and below one shared bitline plane (2F2 effective) (B3-05) | B3 3D/process | TWIST | Mirror-VCT: 4F2 cells on both faces of one bitline plane, 2F2 effective (1.96x 1b) | **ALIVE** | Backside overlay/thermal budget only. |
| N-45 | Ge-free dopant-contrast superlattice (Si / Si:B) for 3D silicon DRAM (B3-06) | B3 3D/process | TWIST | Si / Si:B dopant-contrast superlattice replaces Si/SiGe for 3D Si DRAM: misfit 0.84% -> 0.05-0.16%, Ge-free | **ALIVE** | B contraction gives 0.05-0.16% strain; p+ selective etch known. |
| N-46 | Etch-compensated graded tier stack: uniform lateral recess by composition grading (B3-07) | B3 3D/process | TWIST | Composition-graded tier stack pre-cancels lateral-recess non-uniformity: ~2x taller decks | **ALIVE** | Deterministic recess can be pre-compensated. |
| N-47 | Vt-coded in-stack tier decoder: kill the staircase so 3D DRAM lines can be short (B3-08) | B3 3D/process | TWIST | Vt-coded binary tier decoder replaces the staircase: line-end area 12-21x smaller | **ALIVE** | Ordinary select transistors. |
| N-48 | Sandwich stack: Smart-Cut single-crystal sense layers every 16 oxide tiers (B3-09) | B3 3D/process | NEW | Smart-Cut c-Si sense layer every 16 oxide tiers: in-tier capacitor 600 -> 31-59 nm; ~10x 1b at 64 tiers | **ALIVE** | 16-cell vertical bitlines need 0.3-0.6 fF; H barrier is materials. |
| N-49 | H-free sputtered-Si laser grains as in-stack CMOS and floating-body tiers (B3-10) | B3 3D/process | TWIST | H-free sputtered-Si laser grains as in-stack CMOS and floating-body tiers: p-FET drive 8-17x p-oxide | **ALIVE** | Single-grain Si TFTs demonstrated (Delft). |
| N-50 | Memory interposer: oxide gain-cell tiers built into the silicon interposer (B3-11) | B3 3D/process | NEW | 8 oxide gain-cell tiers in the silicon interposer: +21-250 GB per package at ~0.3 pJ/bit | **ALIVE** | No new physics; interposer runs cool. |
| N-51 | Photonic periphery wafer bonded under the DRAM array (B3-12/B4-14) | B3 3D/process + B4 | NEW | Photonic periphery wafer bonded under the DRAM array: optical I/O per die, ~2-3.4 pJ/bit at metre reach | **ALIVE** | Ring drift ~0.1 nm/K; only global periphery can be photonic; HBM-parity energy. |
| N-52 | TSV-free inductive-coupling memory stacks (short direct, tall relayed) (B3-13/B5-18) | B3 3D/process + B5 | KNOWN+TWIST | TSV-free inductive-coupling stacks: no TSV keep-out/yield loss; direct for 2-4-high, relayed above | **ALIVE** | Direct reach fails at 16-high; relays work but cost ~6 pJ/b avg. |
| N-53 | Sidewall-wired DRAM cube with adaptive (die-position-corrected) side-face lithography (B3-14) | B3 3D/process | KNOWN+TWIST | TSV-free sidewall-wired DRAM cube with adaptive maskless side-face litho: 2,500-5,000 bus wires | **ALIVE** | Edge-stacking heritage; engineering. |
| N-54 | Origami memory stack: one thin membrane folded into N layers, wired through the folds [SPECULATIVE] (B3-15) | B3 3D/process | NEW (speculative) | Origami stack: one thin membrane folded N times, wired through the folds; stacking tax 3x -> 1.05-1.1x | **ALIVE** | 33 um polymer-hinge folds allow 67 um layer pitch; 8 K/W thermal limit. |
| N-55 | Yield firewall: spare tiers per block plus pre-tested tier groups (B3-16) | B3 3D/process | TWIST | Spare tiers per block + pre-tested tier groups: 64-tier stack yield 53% -> ~97% | **ALIVE** | Redundancy arithmetic. |
| N-56 | Hydrogen-lean batch-furnace mold for oxide 3D DRAM (B3-17) | B3 3D/process | TWIST | H-lean LPCVD batch mold, out-gassed before channel deposition: channel H reservoir 4-8x smaller | **ALIVE** | H budget 3 ppm of one PECVD tier: de-risking physics. |
| N-57 | BEOL bonus tiers: oxide gain-cell tiers stacked on a finished Si DRAM die (B3-18) | B3 3D/process | NEW | Oxide gain-cell tiers stacked on a finished Si DRAM die (periphery included): 1.4-4.8x bits per die | **ALIVE** | H sequencing solves the Si/IGZO conflict. |
| N-58 | Thin wafer-on-wafer DRAM with spare layers (64-high in today's package height) (B3-19) | B3 3D/process | KNOWN+TWIST | 4-10 um thin wafer-on-wafer DRAM with 12.5% spare layers: 64-high in 640 um | **ALIVE** | WOW thin stacking demonstrated. |
| N-59 | Cold-bond stack: room-temperature surface-activated hybrid bonding for oxide memory (B3-20) | B3 3D/process | KNOWN+TWIST | Room-temperature surface-activated hybrid bonding: removes 8-16 h at 350 C from oxide memory stacks | **ALIVE** | SAB demonstrated; RT fine-pitch hybrid is engineering. |
| N-60 | Grow-the-hole: bottom-up dual area-selective deposition replaces the high-aspect-ratio etch [SPECULATIVE] (B3-21) | B3 3D/process | NEW (speculative) | Grow-the-hole: dual area-selective deposition builds a 64-128-tier mold around pillars, no HAR etch | **ALIVE-SPECULATIVE** | Dual-ASD defectivity ~1e-10 per hole-tier is orders beyond shown. |
| N-61 | Sequential periphery-over-cell for Si DRAM: lithographic vias instead of hybrid bonds (B3-22) | B3 3D/process | NEW | Sequential c-Si periphery over a Si 1T1C array: per-segment sensing via 100-200 nm vias; capacitor 1.3 -> 0.23-0.38 um | **ALIVE** | Si DRAM tolerates 500 C sequential CMOS. |
| N-62 | ECC-paid capacitor: let the code, not the capacitor, carry the last 4 sigma (B4-01) | B4 architecture | TWIST | Design the array for raw BER 1e-4 + BCH t=8: capacitor 2x shorter (1,300 -> 640 nm) | **ALIVE** | Correct statistics; non-iid tails are the measurable risk. |
| N-63 | Scrub-as-refresh: 1-second refresh, page-level code, lazy scrub (B4-02) | B4 architecture | TWIST | 1 s refresh + page-level code + lazy scrub: ~15x less refresh energy on today's cells | **ALIVE** | Tail statistics + ECC; measurable on FPGA. |
| N-64 | Lifetime-leased refresh: streamed and dead data are never refreshed (B4-03) | B4 architecture | TWIST | Host-leased refresh: streamed or dead rows never refreshed; +5-18% decode throughput | **ALIVE** | Full-tRAS activation is a refresh. |
| N-65 | Significance-split memory: gold-grade sign/exponent, sand-grade mantissa (B4-04) | B4 architecture | NEW | Significance-split BF16: protected exponents, low-voltage mantissas; 1.58x capacity per bit, 3.7x less refresh | **ALIVE** | No physics change; ML tolerance premise. |
| N-66 | Approximate 4-level DRAM for low-order planes and 2-bit KV (B4-05) | B4 architecture | TWIST | Approximate 4-level 1T1C for error-tolerant data: 2x bits per cell without capacitor growth | **ALIVE** | 3.3 sigma half-gap (BER ~1e-3) fine for tolerant data. |
| N-67 | Graceful-forgetting KV memory: leakage as the eviction policy [SPECULATIVE] (B4-06) | B4 architecture | NEW (speculative) | Graceful-forgetting KV cache: charge decay as the eviction policy; KV refresh -> 0 outside a lease | **ALIVE-SPECULATIVE** | DRAM decay is lognormal dropout, not uniform fade; ML premise unproven. |
| N-68 | Tensor-aware codec in the memory controller (hardware DFloat11 + optional lossy KV) (B4-07) | B4 architecture | TWIST | Line-rate exponent entropy codec in the memory controller: lossless 1.47x capacity/bandwidth for BF16 | **ALIVE** | Exponent entropy ~2.6 b bounds the gain. |
| N-69 | Compression-funded ECC: compressible rows earn slow refresh for free (B4-08) | B4 architecture | TWIST | Compression-funded ECC: compressible rows refreshed every 0.5-1 s at zero capacity cost | **ALIVE** | Same physics as B4-02. |
| N-70 | Top-k KV from in-memory scoring of MSB-plane sketches (B4-09) | B4 architecture | NEW | Top-k KV via in-bank scoring of MSB-plane sketches: ~7x less KV traffic, ~8x less HBM for KV | **ALIVE** | PIM shipping-class; sketch quality is ML. |
| N-71 | Row-RAID: in-bank XOR parity rows built by triple-row activation (B4-10) | B4 architecture | NEW | In-subarray XOR parity rows via triple-row activation: hammer tolerance at ~3% capacity | **ALIVE** | Triple-row activation demonstrated. |
| N-72 | Erasure-coded memory stacks: 16+2 dies, any two may fail (B4-11) | B4 architecture | TWIST | 16+2 erasure-coded memory stacks: 16-high yield 44% -> 94% at 95% per-die yield | **ALIVE** | Coding arithmetic right; power shorts outside any code. |
| N-73 | Weight-streaming DRAM die: few banks, wide rows, no refresh (B4-12) | B4 architecture | TWIST | Weight-streaming DRAM die (few banks, wide rows, no refresh while serving): 1.3-1.5x less silicon per bit than HBM | **ALIVE** | Per-token reads refresh rows within 64 ms. |
| N-74 | GRS-linked LPDDR 'HBM-lite' on an organic substrate (B4-15) | B4 architecture | TWIST | LPDDR 'HBM-lite' over ground-referenced links on organic substrate: ~3x fewer wafers per bit than HBM at 2.7-3.4 pJ/b | **ALIVE** | Known links and dies; signal integrity. |
| N-75 | HBF weight tier with read-disturb-aware 'weight mode' (B4-16) | B4 architecture | KNOWN+TWIST | HBF weight tier in pSLC with disturb-scheduled relocation: ~3-5x HBM capacity per $ | **ALIVE** | NAND disturb arithmetic fits pSLC; us latency tier. |
| N-76 | Procedural weights: seeds plus coefficients, regenerated in the memory path (B4-17) | B4 architecture | TWIST | Procedural weights (seeds + coefficients) regenerated in the memory path: 4-5.3x vs BF16, 1.0-1.33x vs FP4 | **ALIVE-SPECULATIVE** | Rate-distortion caps gain at 1.07-1.22x for i.i.d. weights. |
| N-77 | Nested-precision bit-plane memory + self-speculative decoding (B4-18) | B4 architecture | NEW | Bit-plane-major weights serve a 2-4-bit draft for self-speculative decoding: 1.1-1.8x effective bandwidth | **ALIVE** | Layout + acceptance statistics. |
| N-78 | BitNet-native charge-sharing popcount PIM in commodity 1T1C (B4-19) | B4 architecture | TWIST | 8-row charge-sharing popcount PIM for ternary LLMs: 12-35x lower GEMV energy | **ALIVE** | ~76 mV per count, ~11 mV spread: 3-bit resolvable. |
| N-79 | Compact-then-sleep: compress, pack, partial-array self-refresh (B4-20) | B4 architecture | TWIST | Compress and pack before self-refresh, partial-array refresh for the rest: idle refresh power /32-48 | **ALIVE** | Known pieces; ~16 s break-even. |
| N-80 | Broadcast weight bus: one copy of the model feeds N lock-stepped replicas (B4-21) | B4 architecture | NEW | Optical broadcast weight bus: one model copy feeds N lock-stepped replicas; 22-72% of HBM freed for KV | **ALIVE** | Link-budget physics fine; lock-step is architecture. |
| N-81 | Click-RAM: a snap-through 2D-nanoribbon mechanical floating gate over an oxide channel (B5-01) | B5 first principles | NEW | Click-RAM: bistable buckled 2D/ALD nanoribbon as a suspended gate; zero refresh, aJ writes, hammer-immune | **ALIVE-SPECULATIVE** | Clean mechanics; strain uniformity (q^4), stiction, fatigue, ring-down unshown. |
| N-82 | Capacitor-hole racetrack: electroplated domain-wall nanowires in DRAM's high-aspect-ratio mold (B5-02) | B5 first principles | TWIST | Racetrack in DRAM capacitor holes: electroplated domain-wall wires, 10-25 bits per cell footprint, no refresh | **ALIVE-SPECULATIVE** | Bloch-point walls >600 m/s shown, but stochastic pinning; 20 nm shift error unshown. |
| N-83 | Deep-level charge bit: QD-Flash physics shrunk toward an atom-placed single-defect cell (B5-03) | B5 first principles | TWIST (speculative) | Deep-level charge bit (QD-Flash -> atom-placed single defect): 2.7-5x density, aJ writes, 1 s-1 day retention | **ALIVE-SPECULATIVE** | 1.0-1.3 eV levels give s-days; needs wide-gap host (Si capped at 0.56 eV). |
| N-84 | Jot-RAM: image-sensor pinned wells and correlated double sampling for few-electron multi-level memory (B5-04) | B5 first principles | NEW | Jot-RAM: pinned vertical well + correlated double sampling, 4 bits/cell as 0-320 electrons, capacitor-free | **ALIVE-SPECULATIVE** | 40 nm pinned well needs ~2-3e18 doping at 0.5-1 MV/cm (BTBT onset). |
| N-85 | Crystalline crested-barrier selector: transistor-less 1S1C crosspoint DRAM in stacked decks (B5-05) | B5 first principles | TWIST | Crystalline crested-barrier 1S1C crosspoint: 2-4 decks of stub capacitors, no access transistor | **ALIVE-SPECULATIVE** | V/3 nonlinearity arithmetic works; needs crystalline barrier at ~4e11 C/cm2. |
| N-86 | Seconds-ULTRARAM: a resonant-tunnelling floating gate retuned from 1,000-year retention to DRAM-class speed (B5-06) | B5 first principles | TWIST | Seconds-ULTRARAM: resonant-tunnelling floating gate retuned to 1 s-1 day retention for ns writes and 1e15 cycles | **ALIVE-SPECULATIVE** | ULTRARAM works; endurance beyond 1e7 unmeasured. |
| N-87 | Self-timed NEMS-selector crosspoint: a two-terminal hysteretic nanorelay that charges the capacitor and lets go by itself (B5-07) | B5 first principles | TWIST | Self-timed two-terminal NEMS selector crosspoint: 6-58 s retention at 1 fF, 1.3-2.7x 1b density | **ALIVE-SPECULATIVE** | Contact endurance unshown; amorphous soft-landing coating dies on fluence. |
| N-88 | Adiabatic refresh: recycle bitline and wordline charge with stepwise tanks or piezo-MEMS resonators (B5-08) | B5 first principles | TWIST | Adiabatic/stepwise refresh with tank capacitors or piezo-MEMS resonators: 2.4-3.2x lower refresh energy | **ALIVE** | Stepwise charging physics; SA regeneration not recoverable. |
| N-89 | Negative-capacitance bitline: electrophysiology's capacitance neutralisation applied to the DRAM sense path (B5-09) | B5 first principles | TWIST | Active capacitance neutralisation per bitline: a 1.1 fF (~260 nm) capacitor on an unchanged 512-cell bitline | **ALIVE** | Active NIC is an amplifier; noise rises only to ~1.1 mV. |
| N-90 | Myelinated bitline: vacuum-sheathed bitline segments with non-latching 2T 'nodes of Ranvier' (B5-10) | B5 first principles | TWIST | Vacuum-sheathed bitline segments with 2T oxide gain nodes every 32-64 cells: Cs need 0.6-0.8 fF | **ALIVE** | Air spacers in production; 2T node offset auto-zeroed. |
| N-91 | DNA-brick nanotrench templates for an EUV-free cell lattice (B5-11) | B5 first principles | TWIST | DNA-brick nanotrench templates replace 5-7 EUV exposures for periodic array layers | **ALIVE-SPECULATIVE** | 95% assembly yield vs <=1e-4 defects needed (>=500x). |
| N-92 | Voltage-clocked skyrmion shift register: magnetic bubble memory revived with gate clocks instead of currents (B5-12) | B5 first principles | TWIST | Voltage-clocked (VCMA) skyrmion shift register: refresh 0, ~47 aJ per gate toggle; density 1.34x worse than 1b | **ALIVE-SPECULATIVE** | 5 kT/step gives 6.7e-3 back-hop; needs ~28 kT. |
| N-93 | Altermagnetic tunnel-junction RAM: MRAM without stray fields (B5-13) | B5 first principles | NEW (speculative physics) | Altermagnetic tunnel-junction RAM: TMR readout without stray fields; ~1.2x 1b per deck | **ALIVE-SPECULATIVE** | Junction TMR small; RuO2 contested; switching unshown. |
| N-94 | 77 K oxide MLC gain-cell stage for cryogenic and superconducting computers (B5-14) | B5 first principles | TWIST | 77 K oxide MLC gain-cell stage for cryogenic compute: array energy x0.13, refresh ~1e5x less, 3-4 b/cell | **ALIVE** | IGZO works at 77 K; cold-compute scope only. |
| N-95 | Superconducting kinetic-inductance memory with frequency-multiplexed readout (4 K) (B5-15) | B5 first principles | KNOWN+TWIST | Superconducting kinetic-inductance memory with frequency-multiplexed readout at 4 K: ~1e-20-1e-17 J/op | **ALIVE** | Demonstrated; addressing limits density to 1/90-1/17,000 DDR5. |
| N-96 | 1T-TaS2 charge-configuration memory: picosecond, attojoule switching for the 4 K tier (B5-16) | B5 first principles | KNOWN | 1T-TaS2 charge-configuration memory at 4 K: ~2 ps, 24-94 aJ writes | **ALIVE-SPECULATIVE** | ps switching measured; mechanism and endurance unknown. |
| N-97 | Quantum-dot charge RAM at 4 K: spin-qubit process lines repurposed for dense cryogenic memory (B5-17) | B5 first principles | NEW | Gate-defined Si quantum-dot charge RAM at 4 K: 0.05-0.1 Gb/mm2, ~2,000-4,000x superconducting arrays | **ALIVE** | Many-electron dots widen windows; readout ~400x faster than qubits. |

## What I could not verify (5 searches, snippets only)

- **Crystalline barriers at ~1e11 C/cm².** No RTD or epitaxial-barrier lifetime-versus-charge-fluence data. The premise behind N-85, N-86, N-20 is still open.
- **Charge-transfer efficiency in any oxide-semiconductor CCD.** No data (N-08).
- **AFE ZrO2 endurance.** Nothing above ~5e9 field cycles was found. Wurtzite FE endurance >1e10 comes from a 2025 preprint.
- **Cylindrical-wire domain-wall data.** These experiments used wider wires than B5-02's 20 nm. Exact diameters are not confirmed.
- **Stated without a URL [UNVERIFIED-PK].** Porphyrin 1e12-cycle and 400 °C survival; ALD STO k ≥100; boron lattice-contraction coefficient; Si band-to-band onset field.
