# B3 notes: 3D integration & process innovation

**Agent:** `B3-3dprocess` · **Written:** 2026-11-01 · **Phase:** B (divergent ideation), lens 3 of 5

**Files**
- Cards: `research/phaseB/B3-3dprocess.json`, 22 ideas, validated with python3.
- Model: `research/models/B3_3dprocess_estimates.py` (stdlib; `python3` exits 0). Every number in the cards comes from it, from a cited source, or from A1/A3.
- Sources: `research/sources/B3-3dprocess.jsonl`, 69 entries. 42 come from this session's searches (all via search snippet); 27 are cross-references to URLs that A1, A3 or B2 logged.
- Assumptions: `research/assumptions/B3-3dprocess.md`.

**Evidence grade.** I used 15 of 15 searches and no fetches. Web facts are snippet-level `[REPORTED]`, my arithmetic is `[ESTIMATE]`, and facts I knew without a URL are `[UNVERIFIED-PK]`. Novelty calls rest on ≤15 searches, so "not found" means only "not found".

---

## 1. How I aimed the lens

A1 says the walls are engineering, not physics. Three facts shape this lens:
- **The capacitor exists only to beat the bitline** (A1 #1, §4).
- **3D DRAM is a capacitor problem wearing a stacking costume** (A1 §6).
- **Every 2026 next-generation DRAM program already bonds a periphery wafer to the cell wafer** (A3 §2.9).

So the 3D/process question becomes: where can the third dimension or a process change **shorten the bitline, delete the capacitor, move the bits next to compute, or remove a yield/etch/strain blocker**? It must do so without new physics, and without the resource traps A2 flagged (Ge, H, Ru, Hf, EUV). That gave five families:

| Family | Cards | What it attacks |
|---|---|---|
| Short bitlines through the third dimension | B3-01 MSB (bonded, muxed), B3-09 sandwich (Smart-Cut sense layers), B3-22 sequential periphery-over-cell, B3-10 laser-grain sense layers | A1 #1, #7, #10 and the bond-pitch gap in A1 white space 1 |
| Memory where the compute already is | B3-02 carrier-is-memory, B3-03 coolant-backed memory, B3-11 memory interposer, B3-18 bonus tiers on a DRAM die | A1 #5, #6; A2 capital/cleanroom |
| Denser 3D cells from geometry | B3-04 coaxial 4F² 2T0C, B3-05 mirror-VCT | A1 #2, #4 |
| Process fixes for named 3D blockers | B3-06 Ge-free dopant superlattice, B3-07 graded tiers, B3-08 tier decoder, B3-16 spare tiers, B3-17 H-lean mold, B3-20 cold bonding, B3-21 grow-the-hole | A1 #2 (epi defects, recess, staircase, yield), A2 Ge/PFAS, the oxide-drift doubt |
| HBM without the TSV tax | B3-12 photonic periphery, B3-13 coil stack, B3-14 sidewall cube, B3-15 origami, B3-19 thin WoW + spares | A1 #6 |

**Cross-cutting insight 1: short bitlines.** A1 white space 1 wants one sense amp per 64–128-cell bitline, which needs 0.26–0.37 µm bond pitch. That pitch is beyond production. There are three routes around the bond-pitch wall:
- **Mux it.** B3-01 gangs 8 segments onto one bond: 0.74 µm pitch, Cbl ~9 fF.
- **Replace the bond with a litho via.** B3-22 builds sequential c-Si periphery on top: 100–200 nm vias.
- **Put the sense amps inside the stack.** B3-09 and B3-10 do this.

All three end in the same place: a **300–450 nm stub** instead of a 1.3 µm capacitor in 2D, and a **30–60 nm** in-tier capacitor in 3D.

**Cross-cutting insight 2: an empty slot.** Backside power delivery makes a bonded carrier wafer mandatory on every leading-edge logic wafer from 18A/A16 on. That carrier slot is a free face-to-face memory position (B3-02). Cooling the memory through that same wafer (B3-03) removes the thermal objection to DRAM-on-logic. In that configuration, refresh at 105 °C would cost only ~1.3 W per 52 GB layer anyway.

## 2. The three most exciting

1. **B3-02 Carrier-is-memory.**
   - *Mechanism.* Hybrid-bond a DRAM wafer where BSPDN logic puts its blank carrier.
   - *Claim.* **45–53 GB per 800 mm² accelerator at ~0.28 pJ/bit vs 3.5 pJ/bit for HBM (~12x).** That saves ~200–410 W at 8–16 TB/s and costs ~$1.7–2.3/GB at DRAM-wafer cost. A 300 mm memory wafer under a wafer-scale engine is ~3.9 TB.
   - *Risk.* Wafer-to-wafer compound yield. The fix is spare-heavy memory dies plus capacity binning.
2. **B3-04 Coaxial 4F² 2T0C.**
   - *Mechanism.* The storage node is the core gate of an IGZO read-channel shell, with the write FET stacked on top.
   - *Claim.* **1-beta parity at bits×tiers = 4.1 at F = 40 nm** (single-exposure ArF, no EUV), against 14 for A3's 10F² vertical 2T0C. 2 bits × 8 tiers gives **3.9x 1-beta density and ~2.5x bits/$** before yield.
   - *Risk.* A 0.16 fF node (~1,000 e⁻/V) suffers 75–211 mV write-wordline kickback and is sensitive to trap events.
   - *Prior art.* A twist on IME CAS's 4F² dual-gate 2T0C.
3. **B3-09 Sandwich stack (sibling: B3-22).**
   - *Mechanism.* A Smart-Cut single-crystal Si sense layer every 16 oxide tiers, using CEA-Leti 400 °C n&p CMOS, gives 16-cell vertical bitlines (~2–4 fF).
   - *Claim.* The in-tier capacitor shrinks **600 nm → 31–59 nm**, the footprint ~3x. 64 tiers gives **~4.5 Gb/mm² (10x 1-beta), ~5–7x bits/$** before yield.
   - *Risk.* Smart Cut implants ~5e16 H/cm² right above hydrogen-sensitive IGZO, so the barrier must block 99.9997%. B3-10's H-free laser-grain layer is the fallback.

**Runners-up.**
- **B3-03 coolant-backed memory:** memory 9–28 K above coolant gives **8–16x less refresh** for plain Si DRAM. It is the cheapest decisive demo (~$200k).
- **B3-18 bonus tiers:** oxide tiers over a finished DRAM die give 1.4–4.8x bits per die with no new front end.
- **B3-17 H-lean mold:** it de-risks every oxide 3D card at once.

## 3. Biggest physics doubts

- **Hydrogen and Vt stability in oxide stacks (the shared doubt).** Every oxide 3D/multi-level card (B3-04, 09, 11, 17, 18) assumes ≤20–50 mV drift.
  - *The budget.* My arithmetic (B3-17) says a 20 mV budget at EOT 3 nm is only **1.4e11 donors/cm²**. That is **3 ppm** of the hydrogen in one adjacent 30 nm PECVD SiN tier.
  - *Hydrogen sources.* Smart Cut (B3-09/22) implants ~5e16 H/cm². Recovery kinetics are slow (0.58 eV) and incomplete after repeated cycles (KAIST snippet).
  - *Bonding.* Repeated hybrid-bond anneals (8–16 h at 350 °C) equal ~5–37 years at 85 °C of activated kinetics (B3-20).
  - *Why it matters.* If drift cannot be held, oxide 3D falls back to 1 bit/cell and density claims halve or worse.
- **Tiny storage nodes in 4F² gain cells (B3-04).** 0.16 fF is ~1,000 electrons per volt. Kickback and single-trap noise could cap the cell at 1 bit.
- **Bond-pitch yield at 0.7–1 µm (B3-01, B3-02).** One bond per global bitline means ~30M bonds per die at ≥99.999%.
- **Selectivity in B3-06 (Si:B vs Si) and B3-21 (W/dielectric ASD).** Neither number was confirmed by search. Both cards could die on a single measured selectivity.

## 4. Rejected or folded ideas, each with a revival condition

| Idea | Why rejected | Revival condition |
|---|---|---|
| In-situ heater "anneal-reset" of oxide Vt drift (self-healing 3D oxide memory) | Recovery Ea 0.58 eV gives only 375x acceleration at 250 °C, and recovery is incomplete (KAIST). A 50 × 50 µm block on 2 µm SiO2 needs ~0.44 W for +250 K, i.e., kWh-scale energy per die-sweep, versus ~12 mW of refresh per die | Drift dominated by shallow traps that recover at ≤150 °C within hours (18x at 150 °C), allowing a package-level maintenance bake; or thermally suspended stacks |
| Storage capacitor formed in the hybrid-bond dielectric | 0.3 × 0.3 µm pad with 5 nm HfO2 = 3.2 fF, but cell area ≥ bond pitch² = 0.09 µm², **84x** a 1-beta cell | Bond pitch ≤40 nm; no known path |
| Per-cell bonding: a deep-trench capacitor wafer bonded to a transistor wafer | Needs a 30–40 nm bond pitch | Same as above |
| "Z-folded" bitline (reference bitline in the adjacent tier) | Vertical wordline pillars gate both tiers at once, so reference cells get activated; alternating tiers halves density | Tier-selective vertical gates (B3-08-style coding applied to wordlines) |
| Sense amps on the 3D staircase steps | A 1 µm step strip gives ~0.05 µm² per bitline per tier against ~1 µm² per SA | 20:1 mux on the step; superseded by B3-08 + B3-09 |
| Wireless mm-wave/THz chiplet memory links | ~1–10 pJ/bit [UNVERIFIED-PK]; no step on any axis versus optical (B3-12) or bonded (B3-02) | Sub-pJ/bit mm-wave transceivers at >100 Gb/s per channel |
| Free-space optical vertical links through stacked DRAM dies | Needs III-V emitters on every DRAM die | Si-compatible emitters (e.g., GeSn) at BEOL temperatures |
| Tier-specialized 2T0C (write FET in tier k, read FET in tier k+1, different oxides) | Single-etch flows make every pillar span all tiers, so a cell-specific two-tier storage-node link needs per-tier patterning. No density gain | Sequential tier-by-tier BEOL stacks, where mixed channels are trivial anyway |
| AAO-templated nanowire "anisotropic conductive" bond layer to relax overlay | It fixes planarity, not overlay; pad pitch stays overlay-limited | Folded into B3-20 (planarity) |
| Backside-array DRAM (cells on the backside of the periphery wafer via nano-TSVs) | For oxide cells, front-side monolithic over-CMOS already gives litho-aligned contacts; no step | When front BEOL is reserved for logic (memory-on-logic); but it then conflicts with backside power metal |
| SNAP superlattice-edge masters for line arrays | One-time master cost; no per-wafer step | Folded into B2-12 (NIL) |
| "Sea-of-cells" die-agnostic cell wafer | Real, but a logistics/mask-set idea | Folded into B2-12/B2-13 |
| Micro-transfer-printed memory dielets on logic | No density or energy step over die-to-wafer hybrid bonding; µm registration | ≤1 µm registration at >1e5 dielets/h with litho interconnect (then a known-good-die route for B3-02) |
| Smart-Cut stacking of full Si 1T1C layers, one transfer per tier | Each transfer + FEOL costs ~$300–700 against A1's $20–45/tier break-even | Transfer pre-built multi-tier groups (B3-16) |

## 5. Overlap with sibling lenses (deduplicated)

| B3 card | Nearest sibling | Why kept |
|---|---|---|
| B3-04 coax 2T0C | B1-06 (vertical semi-floating-gate 1T1D) | A different device (two FETs, coaxial storage node), and closer to measured IMECAS cells |
| B3-09/10/22 sense layers | B2-08 (complementary-oxide sense amps in-tier) | c-Si gives 8–17x the p-FET drive. These are alternatives if p-oxide is too weak |
| B3-18 bonus tiers | B2-16 (memory in logic BEOL), B2-18 (trailing-node CuA) | A different host (a finished DRAM die, including its periphery) |
| B3-11 memory interposer | B2-16 | A third host: the interposer silicon |
| B3-17 H-lean mold | B2-09 (Ge-free NAND-line oxide 3D), B2-10 (carbon mold) | The hydrogen-budget arithmetic is the part those cards lacked |
| B3-21 grow-the-hole | B2-20 (self-assembled tiers) | B2-20 forms the tiers; B3-21 forms the holes without etch |
| B3-08 decoder, B3-07 graded tiers | B2-09 | Process add-ons that make any NAND-like 3D DRAM stack better |

## 6. Novelty map (honest)

| Novelty | Cards |
|---|---|
| **KNOWN + twist** | B3-13 (Keio ThruChip), B3-14 (Irvine Sensors / 3D Plus heritage; 2025 edge-pad patent family), B3-19 (WOW Alliance), B3-20 (Suga SAB) |
| **TWIST on known** | B3-03, B3-04 (IMECAS 4F² 2T0C), B3-05, B3-06, B3-07, B3-08 (Macronix-style LSM), B3-10 (Delft µ-Cz), B3-16, B3-17 |
| **NEW combination** | B3-01, B3-02, B3-09, B3-11, B3-12, B3-18, B3-22 |
| **[SPECULATIVE]** | B3-15 origami, B3-21 grow-the-hole |

**Most patent-worthy and provable small:**
- **B3-02:** the BSPDN carrier as the memory wafer.
- **B3-04:** the coaxial storage-node-core 2T0C.
- **B3-01:** muxed global bitlines setting the bond count while 64-cell local bitlines set the capacitor.
- **B3-08:** a deposition-coded tier decoder for 3D DRAM.

## 7. Cheapest decisive experiments ($1M frame)

1. **B3-03 thermal demo (~$200k):** a commercial DRAM die with back-etched microchannels on a heater die. Retention-tail maps against heat flux give a fast, publishable number (8–16x refresh).
2. **H-budget study (~$150k, B3-17):** LPCVD vs PECVD molds, SiN→IGZO replacement, and PBTI/retention at 85–125 °C with SIMS/ERDA. This de-risks B3-04/09/11/18 and B2-09/16/18 at once.
3. **Coax cell single-tier (~$350k, B3-04):** C_SN, kickback and 85 °C retention. Go/no-go: ≥100 s at 85 °C with ≤50 mV residual kick.
4. **Muxed short-bitline D2W bond (~$600k, B3-01):** stub-capacitor coupon plus MPW sense-amp die. This is the most expensive of the four, but it validates the shared "short bitline" thesis behind B3-01/09/22.

## 8. Could not verify

- A measured lateral-recess non-uniformity number for 3D DRAM; B3-07 assumes 25% over 4 µm.
- HNA and anodization selectivity between 1–3e20 B-doped Si and intrinsic Si (B3-06).
- Whether CoWoS-S monolithic interposers still reach ~3.3 reticles (~2,700 mm²) in 2026.
- GlobalFoundries monolithic photonics process details and a 2025–26 Ayar Labs pJ/bit figure.
- A measured pJ/bit for TSV-free inductive DRAM stacks; the 10 fJ/bit figure is a company claim.
- Which result URL carried CEA-Leti's IEDM 2025 400 °C n&p result.
- Any public prior art for BSPDN-carrier-as-memory; my one search found none.
- Hydrogen content of production 3D-NAND mold films; the H percentages are [UNVERIFIED-PK].
