# AND-STACK: technical dossier

*Dossier agent `dosw-and-stack`, 2026-11-02. Inputs: `research/stage3/FINAL_CONCEPTS.json` (slug `and-stack`), `research/stage3/and-stack_notes.md`, `models/and-stack.py` (re-run 2026-11-02, exit 0; output in `research/stage3/and-stack_model_output.md`), `research/stage3/FINAL_CONCEPTS.md`, `MISSION.md`. Tags: [ESTIMATE] = own arithmetic or judgment; [SPECULATIVE] = untested physics or process; [UNVERIFIED-PK] = prior knowledge not confirmed with a logged source. No web searches were made for this dossier.*

---

## 0. Header

**Name.** AND-STACK: single-etch 3D oxide gain-cell DRAM, AND-wired with a select plate per tier and 2 bits/cell. The fallback is a coaxial per-tier cell.

**One-line thesis.** Build DRAM-class memory the way 3D NAND is built: deposit a tall stack of metal plates, etch one field of holes, and line the holes with oxide-semiconductor films. Unlike NAND, every tier-hole crossing becomes a capacitorless, transistor-written gain cell that drives its own read current. Density then comes from tier count, not from lithography.

**Rank, category, score.** Rank 3 of 10. Category: cell/array. EV 60 = step size 5 × plausibility 3 × $1M-provability 4. Ranks 2-4 are within scoring noise. AND-STACK carries the portfolio's largest bits-per-dollar prize.

**Lineage.** The primary is device/AND-STACK: single-etch dual-plate AND topology, the density and cost arithmetic, and the two-step experiment. System/Depreciated-Fab DRAM is merged in as the coaxial per-tier fallback. It brings CMOS-under-array, the H-lean-mold drift test and the depreciated-line scale path. Its 4F² density claim was corrected to A3's ~15 bit-tier parity.

| ID | What it contributes | Creativity technique (grid cell) | Stage-2 critics |
|---|---|---|---|
| I-03474 "tree-ring shells" | Per-tier recessed storage ring in one hole | Biomimicry (T08-F06) | HOLD / HOLD |
| I-10833 | 3D-NAND toolset; concentric write and read devices | Wishful thinking / ideal final result (T24-F06) | ADVANCE (physics) / DROP (innovation) |
| I-10664 | Ring as a floating gate on a shared read channel | Wishful thinking / IFR (T24-F02) | ADVANCE / ADVANCE |
| I-00729 | Tier-orthogonal codewords | SCAMPER-Combine (T02-F06) | — |
| I-11559 | ECC-paid margin (raw BER 1e-4) | Phase B lens B4, architecture | — |
| I-01312 | SSD-controller playbook (LDPC, write buffer) | SCAMPER-Adapt (T03-F09) | — |
| I-02936 | Optional n-only oxide periphery | TRIZ #33 Homogeneity (T07-F04) | — |
| N-43 (B3-04) | Coaxial 4F² 2T0C, the fallback cell | Phase B lens B3, 3D process | — |
| N-37 (B2-18) | Trailing-node CMOS-under-array MLC fab reuse | Phase B lens B2, materials | — |
| N-05 (B1-05) | 2 bits/cell on oxide leakage | Phase B lens B1, cell physics | — |
| N-56 (B3-17) | Hydrogen-lean batch-furnace mold | Phase B lens B3, 3D process | — |
| I-11532 | Oxide gain-cell tiers on logic BEOL | Phase B lens B2, materials | — |
| I-11544 | Vt-coded in-stack tier decoder (no staircase) | Phase B lens B3, 3D process | — |
| I-01822 | Convert idle 3D-NAND tool sets | SCAMPER-Magnify/Minify (T04-F10) | HOLD / HOLD |
| I-00869 | Shuttle CMOS plus university post-processing | SCAMPER-Combine (T02-F09) | — |

**PHYSICALLY POSSIBLE? YES, conditionally.** It breaks no law, and each part has been shown on its own: oxide 2T0C cells, recessed per-tier rings and in-hole source/drain pillars. The combination has never been built. It passes or fails on two numbers: a select-plate coupling ratio of at least 0.53, and tail leakage through the ring's dielectrics of at most 21 aA at 85 °C.

**STEP CHANGE IF IT WORKS? YES. Axis: density and bits per dollar.**
- At 64 tiers × 2 b: **8.1× 1-beta density and ~3.8× bits/$** at the component level. This assumes 1% per-tier defects; the range is 1.8-4.4×.
- At 32 × 2 b: 4.1× density and 2.7× bits/$.
- Refresh power is 31× lower at 1 s retention.
- These figures replace the card's 4.5-8.9× density and 3-12× bits/$.

**PROVABLE WITH $1M IN 24 MONTHS? PARTLY.**
- The physics gate is a decisive binary by month 11, from a ~$150k planar emulation. It covers coupling, cutoff of 63 unselected cells, disturb and 2-bit retention.
- A 4-tier vertical stack fits a standalone $985k plan by month 23.
- Tier yield at 32-64 tiers, and therefore the cost claim, needs the $10-50M round.

---

## 1. How it works (for a smart non-engineer)

**DRAM today.** Today's DRAM stores each bit as charge in a microscopic capacitor, a ~60:1 deep pillar. One flat layer of these is printed with the most expensive lithography in the world.

**3D NAND.** 3D NAND flash got cheap another way. It deposits 100+ flat layers, then drills one field of holes through all of them at once, so each new layer costs a deposition, not a lithography step. NAND's trick does not carry straight over to DRAM. NAND cells are wired in series, like beads on a string, so reading takes microseconds. And NAND writes by forcing charge through an insulator, which wears it out after thousands of writes. DRAM has to be read in tens of nanoseconds and written trillions of times.

**AND-STACK's cell.** AND-STACK keeps NAND's "deposit layers, drill once" manufacturing but changes what sits at each floor of the hole:

- **The bit is a tiny metal ring** (a "storage ring") buried in the hole wall at each floor. Its charge, a few hundred electrons, sets its voltage.
- **The ring is a gate.** A 5 nm film of oxide semiconductor (IGZO or indium oxide, the same family that drives modern display pixels) lines the hole. The ring's voltage decides how much current that film lets flow between two vertical metal wires in the middle of the hole: a bitline (BL) and a source line (SL). Reading the current reads the bit, and reading does not erase it.
- **Each floor has two metal plates.**
  - The *write plate* is a door. When it opens, the film beside it conducts and the ring is charged to the data voltage. When it closes, the ring is sealed. Oxide semiconductors leak so little that the charge lasts seconds to hours, not DRAM's 32-64 milliseconds.
  - The *select plate* is a volume knob that wraps the ring. To read floor 7, floor 7's knob is turned up, and the other 63 knobs are turned *down* to push their rings below the point where the film conducts. Only floor 7 then "speaks" onto the bitline.
- **Parallel, not series.** Every cell connects straight to the two wires (an "AND" layout, borrowed from Macronix's 3D AND flash), so no read passes through a string of other cells.
- **Two bits per cell.** The ring is charged to one of four voltages within 1 V, checked by write-verify, and the controller's error correction absorbs rare misreads.

```
SIDE VIEW: one hole through two of 64 tiers (not to scale)

             local bitline  --[hole-top select gate]--+
                                                      |
 plate stack      hole wall                  hole core|            hole wall
 -----------+------------------+----------------------+--------------------
 WRITE  k   | film (door open  |  BL pillar  | ins |  SL pillar | film
            |  -> charges ring)|             |     |            |
 SELECT k   |[RING]=film  <- ring gates film between BL and SL in parallel
 WRITE  k+1 | film             |             |     |            |
 SELECT k+1 |[RING]=film       |             |     |            |
   ...        64 tiers = 128 plates, 5.4 um tall, one hole etch
 -----------+------------------+-------------+-----+------------+---------
                                       SL grounded during read

TOP VIEW at a SELECT level (90 nm hole on a 150 nm hexagonal grid)

  select-plate metal, wrapping the ring top/bottom/back ("sandwich")
   | 6 nm inter-plate dielectric (IPD, Al2O3-rich)
   |  | storage RING: TiN, 18 nm tall x 10 nm thick = the bit (0.25 fF)
   |  |  | read-gate dielectric (EOT 3 nm)
   |  |  |  | 5 nm IGZO / In2O3 film = read channel
   v  v  v  v
  (((( ( [BL 22 nm] |insulator| [SL 22 nm] ) ))))
```

**Fallback cell.** If the single-etch select margin fails, the fallback patterns each tier with ArF lithography. It is a coaxial 4F² gain cell whose storage node is the core gate of a read-channel shell (N-43), wired to the same AND pillars.

---

## 2. The physics and the numbers

Every number in this section is printed by `models/and-stack.py` unless marked otherwise.

### 2.1 Density

**Area per hole.**
- Hex-pitch area: √3/2 × 150² nm² = 19,486 nm².
- Adding 15% for block slits gives **0.0224 µm²** per hole, so one cell per tier.

**Density per bit-tier.**
- Raw: 1/0.0224 µm² = 0.0446 Gb/mm² per tier per bit.
- Applying array efficiency 0.7 (bonded periphery) and 10% ECC parity: 0.0446 × 0.7 / 1.1 = **0.0284 Gb/mm² per bit-tier**.

**Parity with 1-beta.** 1-beta is 0.447 Gb/mm² (Micron D1b 16 Gb / 35.83 mm²). Parity therefore needs 0.447 / 0.0284 = **15.7 bit-tiers**.

| Tiers × bits | Gb/mm² | vs 1-beta | Stack height | Hole aspect ratio |
|---|---|---|---|---|
| 16 × 2 | 0.91 | 2.0× | 1.58 µm | 18:1 |
| 32 × 2 | 1.82 | **4.1×** | 2.86 µm | 32:1 |
| 64 × 1 | 1.82 | 4.1× | 5.42 µm | 60:1 |
| 64 × 2 | 3.63 | **8.1×** | 5.42 µm | 60:1 |
| 64 × 3 (does not close, §2.4) | 5.45 | 12.2× | 5.42 µm | 60:1 |

**Overheads.**
- The staircase for 64 tiers (132 contacted layers, 0.3 µm steps, 4 lanes) takes 9.9 µm per 200 µm plate. That is 4.7% of area, and the 0.7 efficiency covers it.
- The plate web left between neighbouring rings is 150 − 90 − 2×18 = **24 nm**, which is thin (§4).

### 2.2 The storage ring and the key unknown

**Ring capacitance.** The sandwich select plate (wrap = 1) gives C_IPD 0.173 fF, C_gate 0.059 fF and C_parasitic 0.015 fF.
- **C_SN = 0.246 fF.**
- The coupling ratio is **CR = 0.173 / 0.246 = 0.70**.
- A ring coupled through its back face only, like Micron's floating-gate NAND recess, gives CR 0.54 and C_SN 0.159 fF.

**Why the AND topology relaxes the card's CR ≥ 0.6.**
1. On/off ≥ 1e5 against 63 unselected cells means each unselected cell may pass at most 0.89 µA / 1e5 / 63 = **142 fA**.
2. With I(Vt) = 100 nA × W/L 0.39 = 39 nA and a subthreshold slope of 90 mV/dec at 85 °C, that is log₁₀(39 nA / 142 fA) = 5.4 decades = 0.49 V below Vt.
3. So an unselected ring must sit at or below +0.01 V.
4. The highest stored level is 1.0 V, plus a 0.1 V guard. The unselected select plates must therefore pull every ring down by **1.09 V, whatever the CR**.
5. CR only sets the plate swing needed: ΔV = 1.09 V / CR_min. With CR = 0.70 and σ = 0.03, CR_min = 0.61 and the swing is **1.79 V**. The IPD then sees 0.69 V, or 1.15 MV/cm.
6. For a swing of at most 2.5 V, the bar is **CR_mean ≥ 0.53**.

The 0.6 figure came from the series-string pass-boost of I-10664 and does not apply here.

| CR mean | Plate swing | IPD field | Verdict |
|---|---|---|---|
| 0.40 | 3.51 V | 4.0 MV/cm | Swing too large (NAND-class drivers could still do it) |
| 0.50 | 2.66 V | 2.6 MV/cm | Marginal |
| 0.55 | 2.37 V | 2.1 MV/cm | OK |
| 0.70 | 1.79 V | 1.2 MV/cm | Base |

**Neighbour and noise terms.**
- Neighbour-ring coupling is **8 mV** per 1 V swing on the adjacent ring, against a 30 mV budget.
- Write-plate kickback is 130 mV. It is deterministic and pre-compensated by write-verify.
- kTC noise at 85 °C is 4.5 mV.
- One 2-bit level step is 333 mV, or **512 electrons**.

### 2.3 Read, write and energy

**Read current.**
- The read FET is two film arcs: W = 2 × 18 nm, L = 93 nm.
- At V_ds = 0.1 V and 1 V overdrive: I = µC_ox(W/L)V_ov·V_ds = 20 cm²/Vs × 1.15 µF/cm² × 0.39 × 1 × 0.1 = **0.89 µA**.

**Bitline and read time.**
- The hole-top select cuts unselected blocks off, so the local bitline is **8.9 fF**.
- A 2-bit current step of 298 nA resolves 50 mV in 8.9 fF × 50 mV / 298 nA = **1.5 ns**.
- Array read is ~15 ns: plate RC 3.1 ns + 1.5 ns + ~5 ns comparators + ~5 ns decode.
- Read energy is ~1.5 fJ per cell.
- Reads are non-destructive, so there is no restore.

**Write.**
- A write is ~23 fJ per pulse.
- A 2-bit write is 4 program/verify pulses: **~90 fJ and ~100 ns**.
- Because ~100 ns is slow, writes are page writes behind an SRAM buffer, as in DRAM row restore.

### 2.4 Multi-level budget, retention and refresh

**Raw BER.** The model combines random placement and read noise (σ = 13.8 mV) with 60 mV of drift and 30 mV of coupling. At 2 b in a 1 V window, raw BER is **1e-8**, and up to **86 mV** of drift is tolerated at the 1e-4 RAW-BER target. 3 b does not close in a 1 V window: its margin is −19 mV. It needs a 1.5 V window, coupling ≤ 10 mV and drift ≤ ~48 mV. The 3 b rows are upside only.

**Leakage budget.** For 2 b with a 1 s refresh, the allowed leakage is 86 mV × 0.246 fF / 1 s = **21 aA** per cell at the 1e-4 tail. At 64 s it is 0.33 aA. Spread over the ring's 1.25e-10 cm² of IPD, the dielectric must leak ≤ 1.2e-7 A/cm² at 1 s, or ≤ 1.8e-9 A/cm² at 64 s.

**Refresh power per GB at 85 °C.**

| Case | Refresh power per GB | vs DDR5 |
|---|---|---|
| DDR5, 32 ms refresh | 11.5 mW | — |
| AND-STACK, 1 s refresh | 0.37 mW | 31× lower |
| AND-STACK, 64 s refresh | 0.006 mW | ~2,000× lower |

**Headroom.** imec's >200 s at 95 °C implies a few hundred zA per cell [ESTIMATE: node capacitance not published]. The 1 s bar thus has about two decades of headroom per typical cell. The risk is the tail cell and the extra dielectrics around the ring.

### 2.5 Endurance and yield

**Endurance.**
- Refresh-only wear at 1 s for 10 years is 3.2e8 writes, or 1.3e9 pulses. That is **780× inside** imec's 1e12.
- A pathological hot row (1% write duty) needs 2.8e14 pulses, about 280× more than has been shown. The controller must remap hot rows, or ≥1e14 cycles must be measured.

**Die yield at 64 tiers with 1% per-tier killer defects per die.**
- With no erasure code: 0.99⁶⁴ × 0.95 × 0.97 × 0.97 = **0.47**.
- With tier-orthogonal RS codes and 2 spares: **0.84** if 10% of defects are not confined to one tier, or 0.74 if 30% are not.

### 2.6 Cost

**Wafer cost at 64 tiers.** $2,500 periphery + $500 bond + $1,000 array base + 64 × $30 = **$5,920**. That is 1.56× a $3,800 1-beta wafer.

**Bits per wafer.** The wafer yields 23,708 GB, which is 7.7× the 3,069 GB of a 1-beta wafer.

**$/GB vs 1-beta.** Wafer level: **$0.25/GB**, or 5.0×. Component level, including test and package: **$0.39/GB**, or **3.8×** better than $1.48.

| Case | Component $/GB | Bits/$ vs 1-beta |
|---|---|---|
| 16 × 2 b | 0.90 | 1.6× |
| 32 × 1 b (the card's pessimistic case) | 0.99 | 1.5× |
| 32 × 2 b | 0.56 | 2.7× |
| 64 × 1 b | 0.65 | 2.3× |
| 64 × 2 b | 0.39 | 3.8× |
| 96 × 2 b | 0.33 | 4.5× |

**Break-even.** At the component level, cost breaks even at 19 tiers for 1 b and 9 tiers for 2 b.

### 2.7 Against 1-beta DDR5

| | 1-beta DDR5 | AND-STACK 64 × 2 b |
|---|---|---|
| Density | 0.447 Gb/mm² | 3.63 Gb/mm² (8.1×) |
| Component $/GB | $1.48 | ~$0.39 (3.8×) [ESTIMATE, unanchored $/tier] |
| Storage | 1T1C, ~5-10 fF capacitor, AR 60-90:1 | 2T0C floating ring, 0.25 fF, no capacitor |
| Read | Destructive, then restore | Non-destructive current read, ~15 ns |
| Write | ~10 ns class | ~100 ns for 2 b (page-buffered) |
| Refresh | 32 ms above 85 °C (tREFI 3.9 µs, tRFC 295 ns) | 1-64 s target |
| Endurance | Effectively unlimited | 1e12 shown in single cells; hot rows need remap |
| EUV | Micron 1-gamma uses EUV on 1 layer; Samsung 1c 6-7 layers | None in the array; SADP top bitline only |
| Critical etch | Capacitor at AR 60-90:1 per bit layer | One 60:1 hole per 64 tiers |

Sources for the 1-beta column: `models/and-stack.py` INPUTS (from `ram-venture/models/dram_cost_stack.py`), the DDR5 datasheet, TechInsights, TrendForce and the capacitor aspect-ratio patents, all in §10.

### 2.8 Sensitivity

**Cost of 64 × 2 b vs $/tier and per-tier defect rate** (component $/GB, with bits/$ vs 1-beta in brackets):

| $/tier | p = 0.2% | p = 2% | p = 10% |
|---|---|---|---|
| $15 | 0.33 (4.4×) | 0.36 (4.1×) | 0.51 (2.9×) |
| $30 | 0.37 (4.0×) | 0.40 (3.7×) | 0.58 (2.5×) |
| $45 | 0.41 (3.6×) | 0.44 (3.3×) | 0.66 (2.3×) |
| $80 | 0.50 (3.0×) | 0.55 (2.7×) | 0.82 (1.8×) |

**Hole pitch.** If the 24 nm web forces a larger pitch [ESTIMATE, scaling the model]:
- 160 nm pitch: 34 nm web, 3.19 Gb/mm² (7.1×), ~3.4× bits/$.
- 170 nm pitch: 44 nm web, 2.83 Gb/mm² (6.3×), ~3.1× bits/$.

**Leakage.** At the NO-GO bar of 100 aA, 2 b holds 0.21 s and 1 b holds 0.62 s. Even then, refresh is still 19× rarer than DDR5's 32 ms.

### 2.9 Critics' corrections carried into this dossier

| Claim | Original | Corrected | By |
|---|---|---|---|
| Read topology | Series string: 20-100 nA, 0.5-5 µs; ~100 tiers disturbed per write | AND pillars + per-tier write plate | Stage-2 critics (I-03474, I-10833) |
| Density, 32/64 × 2 b | 4.5× / 8.9× | 4.1× / 8.1× (10% parity included) | dos-and-stack model |
| Bits/$, 64 tiers | 3-12× before yield | 3.8× (1.8-4.4×) after yield; 12× needs 3 b, which does not close | dos-and-stack model |
| Coupling bar | CR ≥ 0.6 | CR ≥ 0.53 (σ ≤ 0.03) | dos-and-stack model |
| Read current and time | ~3.8 µA, 0.3 ns | 0.89 µA at 0.1 V, 1.5 ns per 2-b step | dos-and-stack model |
| Stack height | 5.1 µm | 5.42 µm, 60:1 | dos-and-stack model |
| Fallback coaxial parity | 4 bit-tiers | ~15 bit-tiers; A3: 3 b × 8 gives ~1.56× bits/$ | Chief (A3 cross-check) |
| Tier yield | — | 0.998^300 = 55%; erasure coding mandatory | Stage-2 critic (I-01822); A1 |

### 2.10 GO/NO-GO threshold (Phase 1, month 11)

- **GO** requires all of:
  - CR ≥ 0.53 with σ ≤ 0.03 over ≥ 50 cells;
  - each unselected cell ≤ 142 fA at 85 °C with the top level stored (on/off ≥ 1e5 against 63);
  - ≤ 30 mV extra ring shift after 1e9 neighbour writes;
  - 4 levels in ≤ 1 V held ≥ 1 s at 85 °C, with the 1e-4-tail cell drifting ≤ 86 mV (≤ 21 aA).
- **NO-GO** on any of:
  - CR < 0.40;
  - tail leakage > 100 aA at 85 °C;
  - disturb > 1 LSB.
- **Revival:** 1 b/cell (leak budget 4× looser) with 2× the tiers, or the coaxial fallback.

---

## 3. What is new versus prior art

| Prior art | Who, when | What it shows | Relation |
|---|---|---|---|
| 3D AND flash: two S/D pillars inside the channel hole (US12245428, US12156402, US12200935) | Macronix; granted, dates unverified | In-hole BL/SL pillars, channel wrapping both | The pillar architecture AND-STACK borrows; the top freedom-to-operate risk |
| 3D NOR with vertical S/D lines and top BL-select (US10910393) | Macronix | Random-access vertical S/D | Hole-top select precedent |
| 3D 2T0C with gate-around and channel-all-around IGZO | Macronix, per imec article | Macronix holds both halves | Most likely prior filer: watch or partner |
| IGZO 2T0C: 400 s, 1e11 (IEDM 2020/21); >200 s at 95 °C, >1e12, <10 ns (EDL 2025) | imec, 2020-2025 | Retention and endurance anchors | Cell physics AND-STACK relies on |
| IGO 2T0C: >30,000 s, 4 b, 10 ns | SJTU, AFM 2026 | Multilevel retention headroom | MLC anchor |
| 4-tier dual-gate IGZO 2T0C in one step, 3 b, 400 s | IMECAS + Beijing Super String, VLSI 2026 | Closest silicon competitor | Topology known from a news snippet only; not AND pillars with floating rings |
| 3D OCTRAM: SiN→IGZO, 8 layers, Ion > 30 µA, Ioff < 1 aA | Kioxia, IEDM 2025 | Oxide channels in all tiers at once | Process proof for multi-tier oxide |
| BEOL IGZO 3D stacked DRAM | CXMT, IEDM 2025 | Competing oxide 3D DRAM | Different cell |
| 3D X-DRAM IGZO 1T1C/3T0C (TCAD); Si single-cell PoC > 1 s at 85 °C, > 1e14 | NEO Semiconductor, 2025-05 / 2026-05 | "DRAM on a NAND process" narrative | Competitor; endurance benchmark |
| Stacked 2T0C1R, dual-gated IGZO | NUS, IEDM 2024 | Stacked gain cell | Adjacent |
| Ga-free ZTO 2T0C, > 1,500 s | U. Michigan | Ga-free channel option | Materials route |
| Series oxide gain-cell NAND (US8421071, US8750023, US12082391) | SEL / Japanese OS camp, 2013-2024 | Series strings | The topology AND-STACK avoids |
| Vertical gain cell with shared R/W bitline (US11631453) | Micron per one snippet | Shared R/W bitline | Resembles BL = SL write; claims must be read |
| Vertical Si gain cell (US6246083); side- and top-gated read transistor (EP1938378B1) | Micron (likely expired); other | Read gate = storage node; multi-face gating | Limits over-broad claims |
| Floating-gate 3D NAND recessed rings | Micron/Intel, ~2015 [UNVERIFIED-PK] | Per-tier recess and IPD at 32-64+ tiers | The ring-module know-how |
| IGZO 3D CCD in vertical holes | imec, IMW 2026 | Rival "oxide in NAND holes" memory | Block-addressable, not random access |

**The genuine delta.** No single public reference was found that combines all four of:
1. a gain cell at every tier-hole crossing;
2. two in-hole S/D pillars (AND wiring);
3. a per-tier floating ring coupled to a dedicated select plate;
4. a per-tier write plate.

On top of that combination sit four claimable operating and process pieces:
- **writing with BL = SL = data**, which closes the single-film topology;
- the **sandwich select plate**, a recessed conductive interlayer that lets the plate wrap the ring (CR 0.54 → 0.70) and shields it from neighbours;
- a **single-bias current-mode MLC read with write-verify at the read bias**, which cancels per-cell CR, Vt and kickback;
- **tier-orthogonal erasure codewords** behind a raw-BER contract.

This rests on three snippet-level searches, not a freedom-to-operate opinion. Macronix is the party most likely to have filed something close.

---

## 4. Show-stoppers and how persistence could get around them

| # | Show-stopper | Number that kills it | Workaround path |
|---|---|---|---|
| 1 | **Ring dielectric leakage at 85 °C** (IPD, read gate, film interfaces) | Tail > 21 aA fails 2 b at 1 s; > 100 aA is NO-GO; > 1 fA means 1 b holds only 62 ms, no better than DDR5 | Low-field Al₂O₃/SiO₂ IPD instead of high-k (≤ 1.2e-7 A/cm² needed); HfO₂ passivation (SJTU: 100× retention); H-lean mold; 1 b at 250 mV loss (62 aA at 1 s); shorter refresh (0.25 s is still 128× rarer than DDR5) |
| 2 | **Topology closure**: the ring must touch the film where the write plate controls it, yet be insulated from it where it acts as the read gate | Any read-path short through the ring; TCAD at month 3 decides | BL = SL write mode (own proposal, unverified); else per-level segmented films (outer write film, inner read film), which costs 2 more selective recesses |
| 3 | **Coupling ratio and spread** | CR < 0.53 needs > 2.5 V plates; < 0.40 puts > 3 MV/cm on the IPD on every read; σ > 0.03 eats margin | Sandwich wrap (0.70); IPD EOT 2.0 nm (0.75); 3-3.5 V NAND-class plate drivers; lower top level at 1 b |
| 4 | **PBTI and hydrogen drift** | > 86 mV per refresh interval kills 2 b; > ~250 mV kills 1 b | H-lean LPCVD mold (H reservoir 4-8× smaller, N-56); imec H+O anneal (~30× less H-doping); In-poor IGZO; In₂O₃/ZTO |
| 5 | **Neighbour-write disturb** | > 30 mV extra after 1e9 writes; > 1 LSB is NO-GO | Sandwich plate shields (model: 8 mV); deeper write-plate hold (−1.5 V gives 10 decades of subthreshold suppression); tier-orthogonal erasure |
| 6 | **Geometry**: 24 nm plate web; two 22 nm pillars in a 68 nm core; ALD into recesses at 60:1 | Web < 20 nm risks plate opens and ring shorts | 160-170 nm pitch (−12% to −22% density, still 6.3-7.1×); one shared-pillar variant; ALD is the most conformal deposition there is (NAND runs it in deep holes [UNVERIFIED-PK]) |
| 7 | **Etching a metal/oxide stack** at 60:1, since NAND etches oxide/nitride and replaces the nitride with W later [UNVERIFIED-PK] | Hole profile or CD loss over 128 plates | Replacement-gate flow: an SiN/X/SiN select level, X recessed from the hole for the ring, then SiN replaced by W from the slits, which recreates the sandwich [SPECULATIVE]; or doped-poly plates (Micron FG-NAND precedent [UNVERIFIED-PK]) with 50 µm plates plus the I-11544 Vt-coded decoder to keep RC ~4 ns [ESTIMATE] |
| 8 | **Tier yield** | 1% per-tier defects with > 30% not confined → yield ≤ 0.74; 10% per-tier → 2.5× bits/$ at best | Tier-orthogonal RS with 2 spares; plate-short isolation at the drivers; measure the non-confined share in Phase 2 |
| 9 | **Hot-row endurance** | Needs 2.8e14 vs 1e12 shown | Controller write-combining and remap (RAW-BER CONTRACT typed pages); measure ≥ 1e14 (NEO claims it for Si) |
| 10 | **Write latency** | 2-b write ~100 ns | Page-parallel writes with an SRAM buffer; 1-b pages for write-hot data; CXL attach, which hides it |
| 11 | **Cost inputs unanchored** | $/tier > $80 or base > $2k cuts 64 × 2 b to < 2.5× | Use a NAND partner's cost model; drop to 48 tiers (3.4×) if decks are cheaper than tiers |

None of these breaks a physical law. Numbers 1, 2 and 3 are the ones that could force the fallback.

---

## 5. The decisive experiment

**Question.** On a ring of ~0.25 fF, can one select plate mute 63 neighbours by 5.4 decades without disturbing them, while 4 levels survive 1 s at 85 °C?

**Step by step.**

1. **Phase 0 (months 0-3, ~$30k). Electrostatics and design closure.**
   - Run a 3D electrostatic solver (open-source FEM or a collaborator's TCAD) over wrap 0 / 0.5 / 1, IPD EOT 2-5 nm and recess ±3 nm. Target nominal CR ≥ 0.6, so that a measured 0.53 is safe.
   - Simulate one 64-tier hole in SPICE with an oxide-TFT compact model, in BL = SL write mode. Confirm 142 fA per unselected cell and that no write path shorts the ring.
   - Choose the topology (single film or segmented films) and draw the masks.
   - Run the freedom-to-operate search and file Provisional #1.
2. **Phase 1 (months 2-11, ~$150k fab + $25k analysis). Planar 64-cell AND emulation.**
   - Facilities: Purdue Birck (primary; Peide Ye's ALD In₂O₃) or Georgia Tech IEN. ALD splits run at Northwestern NUFAB (ALD $37-77/h academic, ×2 for companies) or Argonne CNM.
   - Structure: 64 cells share one BL line and one SL line. Each cell has a bottom select electrode, ALD IPD, an e-beam-patterned floating TiN island at the true ring area (~0.012 µm²) and at 10× area, an optional top select cap to emulate wrap, the read-gate dielectric, the channel film, and its own write-TFT segment.
   - Splits: wrap (0/1) × IPD EOT (2.5/3.5 nm) × channel (IGZO / In₂O₃ / ZTO) × mold (H-lean LPCVD vs PECVD). That is two runs of ~5 wafers each.
   - Measure at 25, 85 and 110 °C:
     - CR = ΔVt_read / ΔV_select over ≥ 50 cells;
     - summed off current of 63 cells holding the top level;
     - 2-b write-verify level maps;
     - retention to 1e4 s, using the read FET as an electrometer, with the 1e-4 tail extracted;
     - disturb after 1e9 neighbour writes;
     - endurance to 1e12 (~28 h at 10 MHz);
     - hydrogen by SIMS.
3. **Phase 2 (months 10-22, ~$330k fab + $50k FA). 4-tier vertical stack.**
   - Stack: 4 × (write plate + W/TiN/W sandwich select level) + a hole-top select, ~14 layers and ~0.8 µm thick.
   - Holes: 200-300 nm, by e-beam at Birck or NIST CNST, etched by ICP.
   - Ring module: selective TiN recess, ALD IPD, ALD TiN ring, etch-back, read-gate dielectric, channel film.
   - Core: split pillars (insulating fill, e-beam cut, TiN/W fill).
   - Measure per-tier write/read, unselected-tier cutoff (cross-checked against the 64-cell planar result), tier-to-tier spread, 2-b retention at 85 °C, disturb, endurance, FIB/TEM, and a defect-localization map for the non-confined share.
4. **Readout.** Bench B1500A + WGFMU. Optionally use the portfolio's shared MARGIN STACK MPW sense/ADC chip, which is funded outside this budget.

**Budget (standalone seed).**

| Line | $k |
|---|---|
| Two founders, lean pay, 24 months | 190 |
| IP: freedom-to-operate search, 3 provisionals, 1 PCT | 50 |
| Phase 0 electrostatics, TCAD and SPICE | 30 |
| Test bench: used B1500A + WGFMU, hot-chuck prober, AWG, probe cards | 85 |
| Phase 1 fab: ~650 tool-h + ~150 staff-h at ~$150/h, e-beam, materials | 150 |
| Phase 1 SIMS, XPS and TEM | 25 |
| Phase 2 fab: ~1,400 tool-h at ~$175/h + ~300 staff-h, CNST e-beam | 330 |
| Phase 2 FIB/TEM, ~20 cross-sections | 50 |
| Travel, insurance, legal, company | 40 |
| Contingency (~4%) | 35 |
| **Total** | **985** |

All lines are [ESTIMATE]. The rates are anchored to Notre Dame ($124/h access), UNM ($88-250/h) and NUFAB. Birck and IEN rates were not found.

**Portfolio variant.** FINAL_CONCEPTS gives AND-STACK ~$150k of the shared seed. Under that allocation, Phases 0-1 (~$230k with bench and IP shares) are the seed deliverable, and Phase 2 becomes the raise milestone or partner-funded work.

**Timeline.** Month 3: design closure. Month 11: GO/NO-GO #1. Month 12: PCT filing. Months 16-20: two 4-tier lots. Months 22-23: GO/NO-GO #2.

**Pre-set pass/fail numbers.**
- **#1 (planar):** as §2.10.
- **#2 (4-tier):** every tier passes the #1 criteria, tier-to-tier σ_CR ≤ 0.03, and leakage tails are within 2× of planar.

---

## 6. The $1M, 24-month plan

Month 1 = January 2027.

| Quarter | Milestone | Gate |
|---|---|---|
| Q1 2027 | TCAD/SPICE closure; FTO search; Provisional #1 (dual-plate AND cell + BL = SL write); bench built; nanofab onboarding | **G0:** buildable geometry with nominal CR ≥ 0.60 and a write topology without ring shorts |
| Q2 2027 | Phase 1 run 1 (wrap × IPD × channel); first CR and 63-cell cutoff data; Provisional #2 (sandwich select plate) | CR ≥ 0.45 on the first wafers, or redesign |
| Q3 2027 | Phase 1 run 2 (H-lean vs PECVD mold; 64-cell and disturb structures); SIMS | Tail leakage trend ≤ 100 aA at 85 °C |
| Q4 2027 | Measurements; **GO/NO-GO #1 (month 11)**; Provisional #3 (single-bias MLC read); PCT (month 12) | **G1:** §2.10 criteria |
| Q1 2028 | Phase 2 short loops: stack deposition, 200-300 nm hole etch, sandwich recess | Recess depth σ ≤ 2 nm across 4 tiers (TEM) |
| Q2 2028 | Ring segmentation, split-pillar core, first full 4-tier lot | Per-tier write/read on ≥ 1 hole |
| Q3 2028 | Second lot; retention, disturb, endurance; FA | Tier spread within limits |
| Q4 2028 | **GO/NO-GO #2 (month 22-23)**; demo; data room; raise | **G2:** §5 criteria #2 |

**Budget allocation.** As in §5: ~39% fab, ~19% founders, ~9% bench, ~8% analysis and FA, ~5% IP, ~3% design, ~8% overhead and contingency.

**Team.**
- **Founder A, device and process.** A floating-gate 3D-NAND process-integration engineer with hands-on recess, IPD and FG-poly experience. Where to look: ex-Micron Boise R&D, which developed floating-gate 3D NAND before replacement gate, or ex-Intel/Solidigm NAND R&D in Folsom [UNVERIFIED-PK].
- **Founder B, circuits, test and controller.** Write-verify, current-mode MLC sensing and erasure-coded controllers, shared with the MARGIN STACK and RAW-BER CONTRACT work. Where to look: Georgia Tech (Shimeng Yu's memory co-design group) and Purdue ECE alumni [UNVERIFIED-PK].
- **First collaborator.** Peide Ye (Purdue ECE). His group has ALD In₂O₃ vertical all-oxide TFTs (VLSI 2024), 600 °C survival (EDL 2024) and a 3-layer monolithic In₂O₃ platform on 200 mm (2026).
- **Advisors.**
  - An oxide-TFT reliability (PBTI and hydrogen) expert from imec, Purdue or display-industry IGZO teams.
  - Georgia Tech: Suman Datta for oxide BEOL FETs, and the IEDM-2025 two-tier 3D FeRAM team [UNVERIFIED-PK on names].
  - Stanford: H.-S. Philip Wong for monolithic 3D [UNVERIFIED-PK].
- **Programs.** DOE user-facility proposals at Argonne CNM, CINT, ORNL CNMS and the LBNL Molecular Foundry. Non-proprietary work is free [UNVERIFIED-PK]. Use them for the publishable H-lean-mold and ALD studies. NSF SBIR/STTR can extend the runway [UNVERIFIED-PK on amounts].

**IP strategy.**
- **File first, before any talk or poster:**
  - *Provisional #1:* the dual-plate AND gain-cell array and its operation. It covers a per-tier write plate plus select plate, a floating ring coupled to the select plate gating a channel between in-hole BL and SL pillars, reads with the other select plates at cutoff, BL = SL writes and the hole-top select.
- **Then:**
  - *#2:* the sandwich select plate;
  - *#3:* single-bias current-mode MLC read with write-verify at the read bias, and a cutoff-bias schedule set from measured CR_min;
  - *#4:* tier-orthogonal erasure with exported flags, coordinated with RAW-BER CONTRACT;
  - *#5:* the H-lean batch mold for oxide 3D memory, coordinated with the portfolio.
- **Freedom-to-operate risks, highest first:**
  1. Macronix 3D AND split-pillar-in-hole patents (US12245428, US12156402, US12200935) and US10910393;
  2. US11631453 (shared R/W bitline vertical gain cell);
  3. SEL oxide-semiconductor gain-cell families;
  4. Micron/Intel floating-gate recess and IPD patents;
  5. NEO 3D X-DRAM, Kioxia OCTRAM, the imec 2T0C plug and IMECAS single-step 2T0C.
- **Mitigation:** read the claims in Q1 2027. Macronix is the natural licensor or partner if its claims read on the pillars. US6246083 and EP1938378B1 are useful prior art against over-broad claims.

---

## 7. After the demo: scale path

**What a $10-50M round buys.** All lines are [ESTIMATE].
- **~$10-15M:** a 16-tier, 300 mm short-loop lot through a JDA at NY CREATES Albany, which already runs a 300 mm memory JDA with Fraunhofer IPMS.
- **A 1-4 Mb test array** with bonded 28-65 nm CMOS periphery, from a GlobalFoundries or SkyWater shuttle. Wafer-to-wafer bonding could run at the SkyWater-operated Center for NeoVation in Florida (200/300 mm W2W and D2W tools).
- **~$30-50M:** 32- and 64-tier short loops, a Gb-density test chip, 1,000 h high-temperature reliability, an FPGA CXL controller with the RAW-BER contract, and a 15-25 person team.

**Who partners or licenses.**

| Partner | Why |
|---|---|
| **Macronix** | Holds 3D AND and a 3D 2T0C; the most likely licensor, partner or blocker |
| **Kioxia / SanDisk** | NAND decks, 3D OCTRAM (SiN→IGZO in all tiers), OCTRAM work with Nanya; the most natural line for the ring module |
| **SK hynix / Solidigm** | NAND tool sets; broke ground on a ~$4B HBM-packaging plant at Purdue, West Lafayette, on 2026-08-27, a channel through the Ye collaboration |
| **Micron** | Floating-gate recess heritage; CMOS-under-array; the only U.S. DRAM line (Manassas, 1-alpha since 2026-05-22); second Idaho fab output from late 2028 |
| **Samsung** | 16-tier VS-DRAM and IGZO 4F² VCT with bonded periphery; a licensee or competitor |
| **Foundries** (GlobalFoundries, SkyWater, Texas Institute for Electronics) | Periphery wafers and bonding; the coaxial fallback on depreciated ArF lines |
| **Display makers** (IGZO TFT fabs) [UNVERIFIED-PK] | Oxide-channel reliability and target or precursor supply chains; not hole etch |

**Business route.** Fab-lite on a partner's depreciated 3D-NAND decks, or licensing. The cell wafer can also feed CELL-WAFER FOUNDRY.

**Standards.**
- The first product is a **CXL Type-3 memory expander**. A controller hides page-write latency and owns refresh and ECC, so no DDR timing change is needed.
- In parallel, push a JEDEC "ECC-native / raw-BER-1e-4" device grade, the RAW-BER CONTRACT standards route [UNVERIFIED-PK on committee venue].
- A DDR or HBM attach would come later, once write latency is understood.

---

## 8. Resources and America

**Scarce inputs.**
- **Gallium.** IGZO needs Ga, which A2 records as ~98% Chinese [UNVERIFIED-PK]. China's suspension of its U.S. Ga/Ge export ban runs only to **2026-11-27**, and dual-use licensing remains. The plan therefore qualifies Ga-free channels from day 1: Purdue's ALD In₂O₃ and Michigan's ZTO 2T0C (>1,500 s).
- **Indium, tungsten and molybdenum.** Indium quantity is small: A2 puts IGZO at under 0.4% of world Ga even at 40 tiers. Tungsten is China-concentrated [UNVERIFIED-PK], so molybdenum plates are the hedge.
- **Germanium.** The design avoids the Si/SiGe superlattice of 3D silicon DRAM, which A2 estimates would need 6-38% of refined Ge.
- **Hafnium.** IPD and read gate can be Al₂O₃/SiO₂ rather than HfO₂, against a hafnium price that went from ~$5,000 to ~$13,000/kg.

**EUV.** None. The array is one ArF-defined hole layer plus an SADP top bitline at 75 nm pitch. Periphery is 28-65 nm. EUV scanners draw up to 10-12 GWh per tool per year and ~10% of fab electricity.

**Energy, water, helium and PFAS.**
- The flow is deposition-heavy and etch-light: ~132 depositions, one deep hole etch and slits, against DRAM's capacitor and contact etches.
- Per GB, AND-STACK uses a wafer costing 1.56× as much to make 7.7× the GB. If cost tracks energy and water, process energy and water per GB fall ~3-5× [SPECULATIVE: cost as proxy].
- Helium (etch-chuck cooling) and PFAS (fluorocarbon HAR etch) are still needed for the one hole etch. The Qatar helium halt of March 2026 argues for the LEAN ARRAY MODULE hedge.
- In use, refresh power falls 31-2,000× per GB.

**U.S. manufacturability.**
- Every step of the demo runs in U.S. university and national-lab facilities.
- Volume needs a NAND-class line. There is **no U.S. 3D-NAND fab** today [UNVERIFIED: ram-venture p1]. Micron Manassas is DRAM-only and takes no foundry customers.
- That gap is the concept's U.S. opportunity. Routes are a JDA at Albany, a NAND partner's U.S. greenfield, or the coaxial fallback on depreciated 200/300 mm U.S. lines (SkyWater Bloomington, GlobalFoundries Burlington, Texas Institute for Electronics).
- China's rare-earth review rule targets "≥256-layer memory". A 64-tier AND-STACK has ~132 layers, but a 128-tier stack would cross 256. That matters only for China-sourced inputs.

---

## 9. Kill criteria

Physics only. Month 1 = January 2027. Each criterion names its revival condition.

1. **2027-03-31 (month 3).** Kill single-etch, go to the coaxial fallback, if:
   - TCAD shows nominal CR < 0.55 for every geometry with IPD EOT ≥ 2.0 nm and a web ≥ 20 nm, **or**
   - neither BL = SL writing nor segmented films avoids a ring-to-read-path short.

   *Revival:* a geometry with CR ≥ 0.6, possibly at 160-170 nm pitch.
2. **2027-11-30 (month 11).** Kill single-etch if measured CR mean < 0.40 or σ > 0.06 over ≥ 50 cells.

   *Revival:* NAND-class drivers above 3.5 V, with IPD stress shown to hold for 1e12 reads.
3. **2027-11-30.** Kill the DRAM-class claim if the 1e-4-tail leakage of the best split is > 1 fA at 85 °C, because 1 b then holds < 62 ms.
   - Kill 2 b, keeping 1 b, if the tail is > 100 aA.

   *Revival:* an IPD or passivation split at ≤ 21 aA.
4. **2027-11-30.** Kill if the summed off current of 63 unselected cells keeps on/off below 1e4 at 85 °C with a plate swing ≤ 3.5 V.
5. **2027-11-30.** Drop 2 b if disturb is > 1 LSB (333 mV) after 1e9 neighbour writes. Kill if it is > 250 mV at 1 b.
6. **2027-11-30.** Drop 2 b if drift on both molds is > 86 mV in 1 s at 85 °C. Kill if 1-b drift is > 250 mV in 1 s.
7. **2028-10-31 (month 22).** Kill single-etch in favour of the coaxial fallback if, in the 4-tier stack:
   - any tier's CR or leakage tail is worse than 2× planar, **or**
   - tier-to-tier σ_CR is > 0.05.
8. **2028-10-31.** Kill the bits-per-dollar claim, keeping only an energy/refresh niche, if FA shows a non-confined defect share > 30% **and** an extrapolated per-tier killer rate > 2%. Together these push 64 × 2 b below 2.5×.
9. **2028-10-31.** Kill if endurance at 85 °C is < 1e10 cycles, about 8× the 1.3e9 that 1-s refresh needs over 10 years.

**Not a kill (pivot only).** A blocking Macronix or other claim found by the freedom-to-operate search triggers a partner or licence route, per the founder's rule.

---

## 10. Sources

All URLs below are logged in `research/sources/*.jsonl`. Most are in `dos-and-stack.jsonl`, `A1-scaling.jsonl`, `A2-resources.jsonl` and `A3-frontier.jsonl`. Cross-references from ram-venture are added in `dosw-and-stack.jsonl`. Most entries are search-snippet level.

**Prior art and patents**
- Macronix 3D AND: https://patents.google.com/patent/US12245428 · https://patents.google.com/patent/US12156402 · https://patents.google.com/patent/US12200935
- Macronix 3D NOR: https://patents.google.com/patent/US10910393
- Vertical gain cells: https://patents.google.com/patent/US11631453 · https://patents.google.com/patent/US6246083 · https://patents.google.com/patent/EP1938378B1/cg-RX-API-DMAC7.html
- SEL series gain cells: https://patents.google.com/patent/US8421071 · https://patents.justia.com/patent/12082391

**Oxide gain-cell physics**
- imec 2T0C: https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology · https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234 · https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html · https://www.eenewseurope.com/news/imec-shows-capacitor-free-dram
- imec IGZO hydrogen anneal (IEDM 2025): https://imec-publications.be/handle/20.500.12860/59908
- SJTU IGO 2T0C: https://sigroup.sjtu.edu.cn/files/AdvFunctMater_UltrathinOxide_DRAM_2026.pdf
- IMECAS + Beijing Super String: https://www.ithome.com/0/966/543.htm
- Kioxia 3D OCTRAM and OCTRAM: https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html · https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology
- NEO 3D X-DRAM: https://www.storagenewsletter.com/2025/05/08/neo-semiconductor-unveils-1t1c-and-3t0c-igzo-based-3d-x-dram-technology/ · https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/
- CXMT IEDM 2025 (PC Watch): https://pc.watch.impress.co.jp/docs/column/semicon/2061772.html
- NUS stacked 2T0C1R: https://shine.nus.edu.sg/2025/02/18/1t1r-and-2toc1r-igzo-mos%e2%82%82-all-beol-3d-memory-cells/
- U. Michigan ZTO 2T0C: https://deepblue.lib.umich.edu/items/e6ac2d99-46aa-444a-bc41-2851e63c965c
- Purdue ALD In₂O₃: https://engineering.purdue.edu/~yep/Papers/VLSI2024%20T4-1_Zehao%20Lin.pdf · https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf · https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing
- imec 3D CCD: https://siliconsemiconductor.net/article/124234/Imec_demonstrates_the_first_3D_implementation_of_a_charge_coupled_device_for_AI_memory_applications
- Georgia Tech 3D FeRAM (IEDM 2025, Mynavi): https://news.mynavi.jp/techplus/article/iedm2025-4/

**DRAM baseline, 3D DRAM and integration**
- Capacitor scaling (TechInsights): https://www.techinsights.com/ja/node/37840
- DDR5 timing datasheet: https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7134/SQR-RD5N16G5K6HZZG.pdf
- Capacitor aspect ratios: https://patents.justia.com/patent/20220238532
- EUV layer counts: https://www.trendforce.com/news/2025/03/11/news-micron-pioneers-1%CE%B3-ddr5-samples-with-reduced-euv-use-but-future-risks-loom/
- SK hynix 5-layer 3D DRAM yield: https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development
- Lam recess variation: https://semiengineering.com/baby-steps-towards-3d-dram/
- Samsung VS-DRAM (VLSI 2026 tipsheet): https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx
- Samsung 4F² VCT: https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/
- imec W2W hybrid bonding: https://www.imec-publications.be/entities/publication/6228fcc8-685e-4e72-83ba-3cb478415500/full
- ArchShield (raw-BER tolerance): https://memlab.ece.gatech.edu/papers/ISCA_2013_1.pdf

**Facilities, partners and U.S. capacity**
- Facility rates: https://nanofabrication.nd.edu/facility-access/fees/ · https://www.nuance.northwestern.edu/documents/rates/2025-rates/2025-nufab.pdf · https://unmnanofab.unm.edu/user-rates/2026-04-24.pdf
- NY CREATES + Fraunhofer IPMS JDA: https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale
- Center for NeoVation bonding tools: https://www.suss.com/de/news/technical-publications/suss-microtec-xbc300-gen2-neovation-microelectronics
- SK hynix West Lafayette: https://www.wlfi.com/2026/08/27/sk-hynix-partners-with-purdue-university-ceremonially-breaks-ground-4b-memory-chip-facility/ · https://evertiq.com/news/2026-08-28-sk-hynix-breaks-ground-on-4-billion-packaging-facility-in-indiana
- Micron Manassas: https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia
- Micron second Idaho fab (SEC): https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm
- MPW pricing: https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/

**Resources**
- Ga/Ge export ban suspension: https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us · https://www.engineeringnews.co.za/article/china-halts-ban-on-gallium-germanium-antimony-exports-to-us-but-controls-remain-2025-11-10
- Rare-earth review for ≥256-layer memory: https://www.trendforce.com/news/2025/10/09/news-china-expands-rare-earth-curbs-subjects-14nm-logic-and-256-layer-memory-chips-to-case-by-case-review/
- EUV energy: https://bits-chips.com/article/shining-brighter-a-10x-source-power-efficiency-boost-for-euv-lithography
- Qatar helium halt: https://www.caixinglobal.com/2026-03-16/qatar-helium-shutdown-adds-new-risk-to-chip-supply-chain-102423361.html
- Hafnium price: https://news.metal.com/newscontent/103938701-from-stability-to-surge-the-overseas-hafnium-market-caught-between-ai-demand-and-supply-controls
