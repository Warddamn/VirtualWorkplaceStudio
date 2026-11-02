# AND-STACK: technical dossier

*Dossier agent `dosw-and-stack`, 2026-11-02.*

*Inputs:*
- *`research/stage3/FINAL_CONCEPTS.json` (slug `and-stack`) and `FINAL_CONCEPTS.md`;*
- *`research/stage3/and-stack_notes.md`;*
- *`models/and-stack.py`, re-run with exit 0; its output is in `research/stage3/and-stack_model_output.md`;*
- *`MISSION.md`.*

*Tags: [ESTIMATE] is my own arithmetic or judgment; [SPECULATIVE] is untested physics or process; [UNVERIFIED-PK] is prior knowledge with no logged source. No web searches were made for this dossier.*

---

## 0. Header

**Name.** AND-STACK: single-etch 3D oxide gain-cell DRAM. It is AND-wired, has a select plate per tier and stores 2 bits per cell. The fallback is a coaxial per-tier cell.

**One-line thesis.** Build DRAM-class memory the way 3D NAND is built: deposit a tall stack of metal plates, etch one field of holes and line the holes with oxide-semiconductor films. Unlike NAND, every tier-hole crossing becomes a capacitorless, transistor-written gain cell that drives its own read current. Density then comes from tier count, not from lithography.

**Rank, category, score.**
- Rank 3 of 10, category cell/array.
- EV 60 = step size 5 × plausibility 3 × $1M-provability 4.
- Ranks 2-4 are within scoring noise. AND-STACK carries the portfolio's largest bits-per-dollar prize.

**Lineage.**
- The primary is device/AND-STACK: the single-etch dual-plate AND topology, the arithmetic and the two-step experiment.
- System/Depreciated-Fab DRAM is merged in as the coaxial fallback, with CMOS-under-array, the H-lean-mold drift test and the depreciated-line path.
- Its 4F² density claim was corrected to A3's ~15 bit-tier parity.

**Constituent ideas by creativity technique.** Grid cell in brackets; Stage-2 critic verdicts given where they exist.
- **Biomimicry:** I-03474, "tree-ring shells": a per-tier recessed storage ring in one hole [T08-F06; HOLD/HOLD].
- **Wishful thinking / ideal final result:**
  - I-10833, concentric write/read devices on 3D-NAND tools [T24-F06; ADVANCE physics / DROP innovation];
  - I-10664, the ring as a floating gate on a shared read channel [T24-F02; ADVANCE/ADVANCE].
- **SCAMPER-Combine:**
  - I-00729, tier-orthogonal codewords [T02-F06; ADVANCE physics / DROP innovation, on Chipkill and NAND RAIN prior art];
  - I-00869, shuttle CMOS plus university post-processing [T02-F09; ADVANCE/HOLD].
- **SCAMPER-Adapt:** I-01312, the SSD-controller playbook [T03-F09; ADVANCE/ADVANCE].
- **SCAMPER-Magnify/Minify:** I-01822, idle 3D-NAND tool sets [T04-F10; HOLD/HOLD].
- **TRIZ #33 Homogeneity:** I-02936, n-only oxide periphery [T07-F04; ADVANCE/ADVANCE].
- **Phase B lenses:**
  - B1 cell physics: N-05 (2 b/cell on oxide leakage).
  - B2 materials: N-37 (trailing-node CMOS-under-array reuse) and I-11532 (oxide tiers on logic BEOL).
  - B3 3D process: N-43 (the coaxial 4F² fallback), N-56 (the H-lean batch mold) and I-11544 (a Vt-coded tier decoder that removes the staircase; HOLD/HOLD, Macronix LSM prior art).
  - B4 architecture: I-11559 (ECC-paid margin; ADVANCE/ADVANCE).

**PHYSICALLY POSSIBLE? YES, conditionally.**
- No law is broken.
- Each part has been shown separately: oxide 2T0C cells, per-tier recessed rings and in-hole source/drain pillars.
- The combination is unbuilt. It needs a select-plate coupling ratio of at least 0.53, and tail leakage through the ring's dielectrics of at most 21 aA at 85 °C.

**STEP CHANGE IF IT WORKS? YES. Axis: density and bits per dollar.**
- **64 tiers × 2 b:** 8.1× 1-beta density and ~3.8× bits/$ at component level, assuming 1% per-tier defects (range 1.8-4.4×).
- **32 × 2 b:** 4.1× density and 2.7× bits/$.
- **Refresh:** power is 31× lower at 1 s retention.
- These replace the card's 4.5-8.9× density and 3-12× bits/$.

**PROVABLE WITH $1M IN 24 MONTHS? PARTLY.**
- A ~$150k planar emulation gives a decisive physics binary by month 11.
- A 4-tier vertical stack fits a standalone $985k plan by month 23.
- Tier yield at 32-64 tiers, and therefore cost, needs the $10-50M round.

---

## 1. How it works (for a smart non-engineer)

**DRAM today** keeps each bit in a microscopic capacitor ~60 times taller than wide, printed in one flat layer with the world's costliest lithography.

**3D NAND.** 3D NAND flash got cheap by depositing 100+ layers and drilling one field of holes through all of them. Each extra layer costs a deposition, not a lithography step. But NAND has two problems for DRAM use:
- Its cells sit in series, like beads on a string, so reads take microseconds.
- It writes by forcing charge through an insulator, which wears out.

**AND-STACK** keeps NAND's "deposit layers, drill once" manufacturing and changes what sits at each floor of the hole:

- **The bit is a tiny metal ring** buried in the hole wall at each floor. A few hundred electrons set its voltage.
- **The ring is a gate.** A 5 nm film of oxide semiconductor lines the hole: IGZO or indium oxide, the family that drives display pixels. The ring's voltage sets how much current that film passes between two metal wires in the middle of the hole, a bitline (BL) and a source line (SL). Measuring that current reads the bit without erasing it.
- **Each floor has two metal plates.**
  - The *write plate* is a door. It opens to charge the ring to the data voltage, then seals it. Oxide semiconductors leak so little that the charge lasts seconds or more, not DRAM's 32-64 ms.
  - The *select plate* is a volume knob that wraps the ring. To read floor 7, its knob turns up. The other 63 knobs turn *down*, which silences their rings, so only floor 7 speaks.
- **Parallel, not series.** Every cell connects straight to both wires. This "AND" layout is borrowed from Macronix 3D AND flash.
- **Two bits per cell.** Each cell holds one of four voltages within 1 V, set by write-verify. Error correction absorbs rare misreads.

```
SIDE VIEW (2 of 64 tiers)                 TOP VIEW at a SELECT level
 local BL -[hole-top select]-+             select plate (W), wraps ring
 WRITE k   | film | BL | ins | SL | film     | IPD 6 nm (Al2O3)
 SELECT k  [RING]=film  (ring gates film)    |  | RING, TiN, 0.25 fF = bit
 WRITE k+1 | film |    |     |    | film     |  |  | gate oxide, EOT 3 nm
 SELECT k+1[RING]=film                       |  |  |  | IGZO/In2O3 film 5 nm
  ... 128 plates, 5.4 um, one hole etch      v  v  v  v
 SL grounded during read               (((( ([BL] |ins| [SL]) ))))
                                       90 nm hole, 150 nm hex pitch
```

**Fallback.** If single-etch select margin fails, each tier is patterned with ArF lithography instead. Each cell is then a coaxial 4F² gain cell (N-43) on the same AND pillars.

---

## 2. The physics and the numbers

All values come from `models/and-stack.py` unless tagged.

### 2.1 Density

**Area per hole.** √3/2 × 150² nm² = 19,486 nm², plus 15% for slits, gives **0.0224 µm² per hole**. That is one cell per tier.

**Density per bit-tier.**
- Raw: 1/0.0224 µm² = 0.0446 Gb/mm².
- With array efficiency 0.7 and 10% ECC parity: 0.0446 × 0.7/1.1 = **0.0284 Gb/mm²**.

**Parity with 1-beta.** 1-beta is 0.447 Gb/mm², so parity needs **15.7 bit-tiers**.

| Tiers × bits | Gb/mm² | vs 1-beta | Stack, aspect ratio |
|---|---|---|---|
| 32 × 2 | 1.82 | **4.1×** | 2.86 µm, 32:1 |
| 64 × 2 | 3.63 | **8.1×** | 5.42 µm, 60:1 |
| 64 × 3 (does not close) | 5.45 | 12.2× | 5.42 µm, 60:1 |

**Overheads.** Staircase 4.7% of area (inside the 0.7). Plate web 150 − 90 − 2×18 = **24 nm**, thin (§4).

### 2.2 The storage ring and the key unknown

**Ring capacitance.** The sandwich select plate gives C_IPD 0.173 fF, C_gate 0.059 fF and C_parasitic 0.015 fF.
- **C_SN = 0.246 fF**, so **CR = 0.173/0.246 = 0.70**.
- A back-face-only ring, as in Micron floating-gate NAND, gives CR 0.54.

**Why AND relaxes the card's CR ≥ 0.6.**
1. On/off ≥ 1e5 against 63 cells allows each unselected cell 0.89 µA/1e5/63 = **142 fA**.
2. With I(Vt) = 39 nA and 90 mV/dec at 85 °C, that is 5.4 decades, or 0.49 V below Vt. So an unselected ring must sit at or below +0.01 V.
3. The top level is 1.0 V plus a 0.1 V guard. The plates must therefore pull rings down **1.09 V, whatever the CR**.
4. CR only sets the swing, 1.09 V/CR_min. At CR 0.70 (σ 0.03, min 0.61) that is **1.79 V**, with 1.15 MV/cm across the IPD.
5. For a swing of at most 2.5 V, the bar is **CR ≥ 0.53**.

The 0.6 figure came from I-10664's series pass-boost.

| CR mean | Plate swing | IPD field |
|---|---|---|
| 0.40 | 3.51 V | 4.0 MV/cm (too much) |
| 0.55 | 2.37 V | 2.1 MV/cm |
| 0.70 | 1.79 V | 1.2 MV/cm (base) |

**Other terms.**
- Neighbour-ring coupling is **8 mV** per volt, against a 30 mV budget.
- Write kickback is 130 mV. It is deterministic and pre-compensated.
- kTC noise is 4.5 mV.
- One 2-bit level step is 333 mV, or **512 electrons**.

### 2.3 Read, write, energy

**Read.**
- Read current: µC_ox(W/L)V_ov·V_ds = 20 cm²/Vs × 1.15 µF/cm² × 0.39 × 1 V × 0.1 V = **0.89 µA**.
- The local bitline is 8.9 fF. A 298 nA level step resolves 50 mV in 8.9 fF × 50 mV/298 nA = **1.5 ns**.
- Array read is ~15 ns, at ~1.5 fJ per cell. Reads are non-destructive.

**Write.**
- A 2-bit write is 4 program/verify pulses: **~90 fJ and ~100 ns**.
- Writes are therefore page writes behind an SRAM buffer.

### 2.4 Multilevel, retention, refresh

**Raw BER.** With 13.8 mV random σ, 60 mV drift and 30 mV coupling, 2 b in 1 V gives raw BER **1e-8**. Up to **86 mV** of drift fits the 1e-4 target.

**3 b does not close.** The margin is −19 mV. Closing it needs a 1.5 V window, ≤ 10 mV coupling and ≤ 48 mV drift.

**Leakage budget.**
- For 2 b at 1 s refresh: 86 mV × 0.246 fF/1 s = **21 aA** at the 1e-4 tail.
- At 64 s: 0.33 aA.
- Spread over the ring's IPD area, that is ≤ 1.2e-7 A/cm² at 1 s, or ≤ 1.8e-9 A/cm² at 64 s.

**Refresh power per GB at 85 °C.**
- DDR5 at 32 ms: 11.5 mW.
- AND-STACK at 1 s: 0.37 mW (**31× lower**).
- AND-STACK at 64 s: 0.006 mW (~2,000× lower).

**Headroom.** imec's >200 s at 95 °C implies ≤ ~250 zA per typical cell, ~two decades of headroom [ESTIMATE]; the risk is the tail.

### 2.5 Endurance and yield

**Endurance.**
- 1 s refresh for 10 years needs 1.3e9 pulses, **780× inside** imec's 1e12.
- A pathological hot row needs 2.8e14, about 280× short. It needs controller remap, or a measured ≥1e14.

**Die yield at 64 tiers with 1% per-tier killer defects.**
- No erasure code: 0.99⁶⁴ × 0.95 × 0.97 × 0.97 = **0.47**.
- Tier-orthogonal RS with 2 spares: **0.84** if 10% of defects are non-confined, 0.74 if 30% are.

### 2.6 Cost

**Wafer.** $2,500 periphery + $500 bond + $1,000 array base + 64 × $30 = **$5,920**. That is 1.56× a 1-beta wafer, for 7.7× the GB (23,708 vs 3,069).

| Case | Component $/GB | Bits/$ vs $1.48 |
|---|---|---|
| 32 × 1 b (the card's pessimistic case) | 0.99 | 1.5× |
| 32 × 2 b | 0.56 | 2.7× |
| 64 × 1 b | 0.65 | 2.3× |
| 64 × 2 b | **0.39** (wafer level $0.25) | **3.8×** (5.0×) |

**Break-even.** 19 tiers at 1 b, 9 tiers at 2 b.

### 2.7 Against 1-beta DDR5

| | 1-beta DDR5 | AND-STACK 64 × 2 b |
|---|---|---|
| Density | 0.447 Gb/mm² | 3.63 Gb/mm² |
| Component $/GB | $1.48 | ~$0.39 [ESTIMATE; $/tier unanchored] |
| Storage | 1T1C, ~5-10 fF capacitor, AR 60-90:1 | Floating ring, 0.25 fF |
| Read | Destructive | Non-destructive, ~15 ns |
| Write | ~10 ns class | ~100 ns, page-buffered |
| Refresh | 32 ms above 85 °C (tRFC 295 ns) | 1-64 s target |
| EUV | Micron 1-gamma: 1 layer; Samsung 1c: 6-7 | None |

### 2.8 Sensitivity

**64 × 2 b component $/GB** (bits/$ vs 1-beta in brackets):

| $/tier | Tier defects 0.2% | 2% | 10% |
|---|---|---|---|
| $15 | 0.33 (4.4×) | 0.36 (4.1×) | 0.51 (2.9×) |
| $30 | 0.37 (4.0×) | 0.40 (3.7×) | 0.58 (2.5×) |
| $80 | 0.50 (3.0×) | 0.55 (2.7×) | 0.82 (1.8×) |

**Other levers.**
- **Pitch** [ESTIMATE]. At 160 nm the web is 34 nm, giving 7.1× density and ~3.5× bits/$. At 170 nm the web is 44 nm, giving 6.3× and ~3.2×.
- **Leakage.** At the 100 aA NO-GO bar, 2 b holds 0.21 s (6.6× DDR5's 32 ms interval) and 1 b holds 0.62 s (19×).

### 2.9 Critics' corrections carried here

| Item | Original | Corrected (source) |
|---|---|---|
| Topology | Series: 20-100 nA, 0.5-5 µs reads; ~100 tiers disturbed per write | AND pillars + per-tier write plate (Stage-2 critics) |
| Density, 32/64 × 2 b | 4.5× / 8.9× | 4.1× / 8.1× (model, parity included) |
| Bits/$ | 3-12× before yield | 3.8× (1.8-4.4×); 12× needs 3 b (model) |
| Coupling bar | CR ≥ 0.6 | CR ≥ 0.53 (model) |
| Read | ~3.8 µA, 0.3 ns | 0.89 µA, 1.5 ns (model) |
| Coaxial fallback | Parity at 4 bit-tiers | ~15 bit-tiers; ~1.56× bits/$ at 3 b × 8 (chief, A3) |
| Tier yield | — | 0.998³⁰⁰ = 55% without repair, so erasure coding is mandatory (I-01822 critic, A1) |

### 2.10 GO/NO-GO (planar, month 11)

**GO** needs all of:
- CR ≥ 0.53 with σ ≤ 0.03 over ≥ 50 cells;
- ≤ 142 fA per unselected cell at 85 °C with the top level stored;
- ≤ 30 mV of disturb after 1e9 neighbour writes;
- 4 levels in ≤ 1 V held ≥ 1 s at 85 °C, with the 1e-4 tail drifting ≤ 86 mV.

**NO-GO** on any of:
- CR < 0.40;
- tail leakage > 100 aA;
- disturb > 1 LSB.

**Revival:** 1 b/cell with 2× the tiers, or the coaxial fallback.

---

## 3. What is new versus prior art

| Prior art (who, when) | What it shows | Relation to AND-STACK |
|---|---|---|
| Macronix 3D AND flash, US12245428 / US12156402 / US12200935 (granted; dates unverified) | Two S/D pillars inside the channel hole | The borrowed pillar layout; top freedom-to-operate risk |
| Macronix 3D NOR, US10910393 | Vertical S/D lines with top BL-select | Hole-top select precedent |
| Macronix 3D 2T0C, gate- and channel-all-around IGZO (per imec article) | Macronix holds both halves | Most likely prior filer |
| imec 2T0C (IEDM 2020/21; EDL 2025): >200 s at 95 °C, >1e12 cycles, <10 ns | Retention and endurance anchors | The cell physics relied on |
| SJTU IGO 2T0C (AFM 2026): >30,000 s, 4 b | MLC headroom | MLC anchor |
| IMECAS + Beijing Super String (VLSI 2026): 4-tier single-step dual-gate 2T0C, 3 b, 400 s | Closest silicon | Topology known from a news snippet only |
| Kioxia 3D OCTRAM (IEDM 2025): SiN→IGZO in 8 layers, Ioff < 1 aA | Oxide channels in all tiers at once | Process proof |
| NEO 3D X-DRAM (TCAD 2025-05; single-cell PoC 2026-05, >1e14) | "DRAM on a NAND process" | Competitor |
| CXMT BEOL IGZO 3D DRAM (IEDM 2025); NUS stacked 2T0C1R (IEDM 2024); U. Michigan Ga-free ZTO 2T0C | Other oxide 3D cells | Adjacent |
| SEL series oxide gain-cell NAND, US8421071 / US8750023 / US12082391 (2013-2024) | Series strings | What AND-STACK avoids |
| US11631453 (Micron per one snippet): vertical gain cell, shared R/W bitline | Resembles BL = SL writing | Claims must be read |
| Micron/Intel floating-gate 3D NAND, ~2015 [UNVERIFIED-PK] | Per-tier recess and IPD at 32-64+ tiers | Ring-module know-how |
| Huawei vertical channel-all-around IGZO 2T0C (ULSIC vs TFT 8 invited talk) | Vertical CAA oxide 2T0C for 3D DRAM | Named by the I-03474 and I-10833 critics; adjacent vertical cell |
| Micron vertical Si gain cell, US6246083 | Read FET gated by the storage node, vertical | Old gain-cell claims around "ring gates film" |
| Toshiba NAND-structured DRAM, 1990s [UNVERIFIED-PK; I-10664 critic] | Series-string DRAM cells | What AND-STACK avoids |
| Chipkill (IBM, 1997); Micron RAIN / SSD die-RAID parity across NAND planes [UNVERIFIED-PK; I-00729 critics] | Erasure/symbol codes across failure domains | The I-00729 innovation critic rated tier-orthogonal codes DROP on this prior art |
| Macronix VG-NAND layer select by multilevel operation (LSM, ~2011) [UNVERIFIED-PK; I-11544 critics] | Vt-coded layer decode | Prior art for the staircase-free decoder in §4 #7 |

**The delta.** No public reference was found that combines all four of:
1. a gain cell at every tier-hole crossing;
2. in-hole BL/SL pillars;
3. a per-tier floating ring on a dedicated select plate;
4. a per-tier write plate.

Four claimable pieces sit on top of that combination:
- **BL = SL = data writing**, which closes the single-film topology;
- the **sandwich select plate** (CR 0.54 → 0.70, with neighbour shielding);
- **single-bias current-mode MLC read with write-verify at the read bias**, which cancels per-cell CR, Vt and kickback;
- **tier-orthogonal erasure** behind a raw-BER contract. This is the weakest: Chipkill and NAND RAIN already code across failure domains, so only the tier mapping and the raw-BER contract are candidates.

This rests on three snippet-level searches, not a freedom-to-operate opinion.

---

## 4. Show-stoppers and how persistence could get around them

| # | Show-stopper | Killing number | Workaround |
|---|---|---|---|
| 1 | Ring dielectric leakage at 85 °C | Tail > 21 aA fails 2 b at 1 s; > 100 aA is NO-GO; > 1 fA leaves 1 b at 62 ms, no better than DDR5 | Low-field Al₂O₃/SiO₂ IPD; HfO₂ passivation (SJTU: 100×); H-lean mold; 1 b (62 aA at 1 s); 0.25 s refresh (85 aA budget at 2 b), still ~8× rarer than DDR5 |
| 2 | Topology closure: the ring must touch the film where the write plate gates it, yet be insulated where it gates the read | Any ring-to-read-path short (TCAD, month 3) | BL = SL writing (own proposal, unverified); else segmented write and read films, at +2 recesses |
| 3 | Coupling ratio and spread | CR < 0.53 needs > 2.5 V plates; < 0.40 puts > 3 MV/cm on the IPD | Sandwich wrap (0.70); IPD EOT 2.0 nm (0.75); 3-3.5 V NAND-class drivers |
| 4 | PBTI and hydrogen drift | > 86 mV per interval kills 2 b; > ~250 mV kills 1 b | H-lean mold (4-8× less H, N-56); imec H+O anneal (~30×); In-poor IGZO; In₂O₃/ZTO |
| 5 | Neighbour-write disturb | > 30 mV after 1e9 writes; > 1 LSB is NO-GO | Sandwich shielding (8 mV modelled); −1.5 V write-plate hold (10 decades of suppression); erasure coding |
| 6 | Geometry: 24 nm web; two 22 nm pillars in a 68 nm core; ALD into 60:1 recesses | Web < 20 nm | 160-170 nm pitch (still 6.3-7.1×); a shared-pillar variant |
| 7 | Etching metal/oxide at 60:1, where NAND etches oxide/nitride and replaces it later [UNVERIFIED-PK] | CD or profile loss over 128 plates | Replacement gate (SiN/X/SiN select level; recess X for the ring; W replaces SiN from slits) [SPECULATIVE]; or doped-poly plates, 50 µm long, with the I-11544 decoder (RC ~4 ns) [ESTIMATE] |
| 8 | Tier yield | > 30% non-confined defects gives yield ≤ 0.74; 10%/tier gives ≤ 2.5× | RS with 2 spares; plate-short isolation; measure confinement in Phase 2 |
| 9 | Hot-row endurance | 2.8e14 needed vs 1e12 shown | Controller remap and typed pages; measure ≥ 1e14 |
| 10 | 2 b write latency | ~100 ns | Page-parallel writes, SRAM buffer, CXL attach |
| 11 | Unanchored cost inputs | > ~$105/tier gives < 2.5× at 1% defects ($80 gives 2.9×; 1.8× at 10%) | Use a NAND partner's cost model; stop at 48 tiers |

None breaks a physical law. Show-stoppers 1-3 could force the fallback.

---

## 5. The decisive experiment

**Question.** On a ~0.25 fF ring, can one select plate mute 63 neighbours by 5.4 decades, without disturbing them, while 4 levels survive 1 s at 85 °C?

**Phase 0 (months 0-3, ~$30k).**
1. Run 3D electrostatics over wrap 0, 0.5 and 1, IPD EOT 2-5 nm and recess ±3 nm. Target nominal CR ≥ 0.6.
2. Run SPICE of a 64-tier hole in BL = SL write mode.
3. Choose single or segmented films.
4. Complete the freedom-to-operate search and Provisional #1.

**Phase 1 (months 2-11, ~$150k fab + $25k analysis). A planar 64-cell AND emulation.**
- **Facilities.** Purdue Birck (Peide Ye's ALD In₂O₃) or Georgia Tech IEN. ALD splits at Northwestern NUFAB ($37-77/h academic, ×2 industry) or Argonne CNM.
- **Structure.** 64 cells on one shared BL and one shared SL. Each cell has its own write and select electrodes and an e-beam floating TiN island at the true ring area (~0.012 µm²) and at 10× area. An optional top cap emulates wrap.
- **Splits.** Wrap × IPD EOT (2.5/3.5 nm) × channel (IGZO/In₂O₃/ZTO) × mold (H-lean LPCVD vs PECVD). Two runs of ~5 wafers each.
- **Measurements at 25/85/110 °C.**
  - CR across ≥ 50 cells;
  - summed 63-cell off current;
  - 2 b level maps;
  - retention to 1e4 s, with the 1e-4 tail extracted;
  - disturb after 1e9 neighbour writes;
  - endurance to 1e12 (~28 h at 10 MHz);
  - SIMS hydrogen.

**Phase 2 (months 10-22, ~$330k fab + $50k FA). A 4-tier vertical stack.**
- **Stack.** 4 × (write plate + W/TiN/W select) plus a hole-top select, ~0.8 µm thick.
- **Holes and cell module.** 200-300 nm e-beam holes (Birck or NIST CNST), ICP etched. Then: TiN recess, IPD, ring, etch-back, gate dielectric, film, split pillars.
- **Measurements.** As Phase 1, per tier, plus tier-to-tier spread, FIB/TEM and a defect-confinement map.

**Readout.** Bench B1500A + WGFMU, or the shared MARGIN STACK MPW chip.

| Budget line (standalone) | $k |
|---|---|
| Two founders, lean, 24 months | 190 |
| IP: freedom-to-operate search, 3 provisionals, PCT | 50 |
| Phase 0 TCAD and SPICE | 30 |
| Bench: used B1500A/WGFMU, hot-chuck prober | 85 |
| Phase 1 fab (~650 tool-h + 150 staff-h at ~$150/h) | 150 |
| Phase 1 SIMS, XPS, TEM | 25 |
| Phase 2 fab (~1,400 tool-h at ~$175/h + staff, e-beam) | 330 |
| Phase 2 FIB/TEM (~20 cross-sections) | 50 |
| Travel, legal, company | 40 |
| Contingency | 35 |
| **Total** | **985** |

**Rate anchors and allocation.** All budget lines are [ESTIMATE]. Rates are anchored to Notre Dame ($124/h), UNM ($88-250/h) and NUFAB. The portfolio seed allocates only ~$150k to AND-STACK. Under that allocation, Phases 0-1 (~$230k) are the seed deliverable and Phase 2 is the raise milestone.

**Pass/fail.**
- **#1 (month 11):** §2.10.
- **#2 (month 22-23):** every tier meets #1, tier-to-tier σ_CR ≤ 0.03, and leakage tails are within 2× of planar.

---

## 6. The $1M, 24-month plan

Month 1 = January 2027.

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 2027 | TCAD/SPICE; freedom-to-operate search; Provisional #1; bench; nanofab onboarding | **G0:** nominal CR ≥ 0.60, no ring short |
| Q2 2027 | Phase 1 run 1; first CR and cutoff data; Provisional #2 | CR ≥ 0.45 or redesign |
| Q3 2027 | Phase 1 run 2 (molds, 64-cell, disturb); SIMS | Tail trending ≤ 100 aA |
| Q4 2027 | **GO/NO-GO #1 (month 11)**; Provisional #3; PCT (month 12) | **G1:** §2.10 |
| Q1 2028 | Phase 2 short loops: stack, holes, sandwich recess | Recess σ ≤ 2 nm (TEM) |
| Q2 2028 | Rings, split pillars, first 4-tier lot | Per-tier write/read |
| Q3 2028 | Second lot; reliability; FA | Tier spread in limits |
| Q4 2028 | **GO/NO-GO #2**; demo; data room; raise | **G2:** §5 #2 |

**Allocation.** ~49% fab, 19% founders, 9% bench, 8% analysis, 5% IP, 3% design and 8% overhead plus contingency.

**Team.**
- **Founder A, device and process.** A floating-gate 3D-NAND integrator with recess and IPD experience. Recruit from ex-Micron Boise R&D, where FG 3D NAND was developed, or ex-Intel/Solidigm Folsom NAND R&D [UNVERIFIED-PK].
- **Founder B, circuits, test and controller.** MLC write-verify sensing and erasure-coded controllers. Recruit from Georgia Tech (the Shimeng Yu group) or Purdue ECE [UNVERIFIED-PK].
- **First collaborator.** Peide Ye (Purdue): vertical ALD In₂O₃ TFTs, 600 °C survival, and a 3-layer monolithic platform on 200 mm.
- **Advisors.**
  - An oxide PBTI/hydrogen expert from imec, Purdue or display IGZO teams.
  - Suman Datta (Georgia Tech) [UNVERIFIED-PK].
  - H.-S. Philip Wong (Stanford) [UNVERIFIED-PK].
- **Programs.**
  - DOE user facilities (Argonne CNM, CINT, ORNL CNMS, Molecular Foundry) for publishable H-lean-mold and ALD studies. Non-proprietary use is free [UNVERIFIED-PK].
  - NSF SBIR/STTR for runway.

**IP strategy.**
- **File first, before any talk:** Provisional #1, the dual-plate AND gain-cell array and its operation. That means a per-tier write plate plus select plate, a floating ring gating a channel between in-hole BL/SL pillars, reads with the other plates at cutoff, BL = SL writes and the hole-top select.
- **Then:**
  - #2, the sandwich select plate;
  - #3, single-bias MLC read with write-verify at the read bias;
  - #4, tier-orthogonal erasure (with RAW-BER CONTRACT);
  - #5, the H-lean mold (with the portfolio).
- **Freedom-to-operate risks, highest first:** Macronix 3D AND/NOR, then US11631453, SEL families, Micron/Intel recess patents, and NEO, Kioxia, imec and IMECAS. Read the claims in Q1 2027; Macronix is the natural licensor.

---

## 7. After the demo: scale path

**What $10-50M buys** [ESTIMATE]:
- **~$10-15M:** a 16-tier 300 mm lot through a JDA at NY CREATES Albany, which already runs a memory JDA with Fraunhofer IPMS. Also a 1-4 Mb array with bonded 28-65 nm periphery, wafer-bonded at the SkyWater-operated Center for NeoVation (W2W and D2W tools).
- **~$30-50M:** 32- and 64-tier short loops, a Gb-density test chip, 1,000 h reliability, an FPGA CXL controller, and 15-25 people.

| Partner | Why |
|---|---|
| Macronix | Holds 3D AND plus 3D 2T0C: licensor, partner or blocker |
| Kioxia / SanDisk | NAND decks; 3D OCTRAM puts IGZO in all tiers; OCTRAM work with Nanya |
| SK hynix / Solidigm | NAND tools; broke ground on a ~$4B HBM-packaging plant at Purdue on 2026-08-27 |
| Micron | Floating-gate recess heritage, CMOS-under-array; Manassas runs 1-alpha DRAM from 2026-05-22; second Idaho fab output late 2028 |
| Samsung | 16-tier VS-DRAM and IGZO 4F² VCT with bonded periphery |
| Foundries (GlobalFoundries, SkyWater, TIE); display makers [UNVERIFIED-PK] | Periphery, bonding, coaxial fallback; oxide-channel reliability |

**Route.** Fab-lite on a partner's depreciated NAND decks, or licensing; cell wafers can feed CELL-WAFER FOUNDRY.

**Standards.**
- Launch as a **CXL Type-3 expander**. The controller hides page writes and owns refresh and ECC.
- Push a JEDEC "raw-BER-1e-4 / ECC-native" grade via RAW-BER CONTRACT [UNVERIFIED-PK on venue].

---

## 8. Resources and America

**Scarce inputs.**
- **Gallium.** A2 records Ga as ~98% Chinese [UNVERIFIED-PK]. China's suspension of its U.S. Ga/Ge export ban ends **2026-11-27**. Ga-free In₂O₃ and ZTO (>1,500 s in a 2T0C) are therefore qualified from day 1.
- **Indium.** Quantity is small; A2 counts IGZO as minor even at 40 tiers.
- **Tungsten.** W is China-concentrated [UNVERIFIED-PK]; molybdenum plates are the hedge.
- **Germanium.** No Si/SiGe superlattice is used. A2 estimates 3D silicon DRAM would need 6-38% of refined Ge.
- **Hafnium.** The dielectrics can be Al₂O₃/SiO₂, which avoids a hafnium price that went from ~$5,000 to ~$13,000/kg.

**EUV.** None. The array needs one ArF hole layer plus an SADP top bitline at 75 nm pitch; periphery is at 28-65 nm. For comparison, an EUV tool uses up to ~10-12 GWh a year, and EUV is ~10% of fab electricity.

**Energy, water, helium and PFAS.**
- The flow is deposition-heavy: ~132 depositions and one deep etch.
- A 1.56× wafer cost buys 7.7× the GB, so process energy and water per GB plausibly fall ~3-5× [SPECULATIVE: cost as proxy].
- The hole etch still needs helium cooling and fluorocarbon chemistry. The Qatar helium halt of March 2026 argues for the LEAN ARRAY MODULE hedge.
- In use, refresh power falls 31-2,000×.

**U.S. manufacturability.**
- The whole demo runs in U.S. facilities.
- Volume needs a NAND-class line, and there is **no U.S. 3D-NAND fab** [UNVERIFIED: ram-venture p1]. That gap is the U.S. opportunity.
- Routes: an Albany JDA, a partner's U.S. greenfield, or the coaxial fallback on depreciated U.S. lines (SkyWater Bloomington, GlobalFoundries Burlington, Texas Institute for Electronics).
- China's rare-earth review covers "≥256-layer memory": 64 tiers is ~132 layers, 128 tiers would cross it.

---

## 9. Kill criteria

Physics only. Month 1 = January 2027.

1. **2027-03-31.** If TCAD gives nominal CR < 0.55 for every geometry with IPD EOT ≥ 2.0 nm and web ≥ 20 nm, **or** no write topology avoids a ring short: kill single-etch and move to the coaxial fallback. *Revival:* CR ≥ 0.6 at a 160-170 nm pitch.
2. **2027-11-30.** If measured CR mean < 0.40 or σ > 0.06 over ≥ 50 cells: kill single-etch. *Revival:* > 3.5 V drivers with IPD stress shown to 1e12 reads.
3. **2027-11-30.**
   - Tail leakage > 1 fA at 85 °C means 1 b holds < 62 ms: kill the DRAM-class claim.
   - Tail > 100 aA: drop to 1 b.
   - *Revival:* a split at ≤ 21 aA.
4. **2027-11-30.** If 63-cell on/off < 1e4 at 85 °C with a swing ≤ 3.5 V: kill.
5. **2027-11-30.** Disturb > 1 LSB after 1e9 writes: drop 2 b. Disturb > 250 mV at 1 b: kill.
6. **2027-11-30.** Drift > 86 mV in 1 s at 85 °C on both molds: drop 2 b. 1-b drift > 250 mV in 1 s: kill.
7. **2028-10-31.** If any 4-tier stack tier is worse than 2× planar in CR or leakage tail, or tier σ_CR > 0.05: kill single-etch and move to the fallback.
8. **2028-10-31.** If the non-confined defect share is > 30% **and** the per-tier killer rate is > 3.5%: kill the bits-per-dollar claim (64 × 2 b < 2.5×) and keep only an energy niche.
9. **2028-10-31.** If endurance at 85 °C is < 1e10 cycles (~8× the 1-s refresh need): kill.

**Pivot, not a kill.** A blocking patent triggers a partner or licensing route.

---

## 10. Sources

All logged in `research/sources/*.jsonl` (mostly `dos-and-stack`, `A1`-`A3`; ram-venture cross-references in `dosw-and-stack`). Mostly snippet-level.

**Patents**
- https://patents.google.com/patent/US12245428
- https://patents.google.com/patent/US12156402
- https://patents.google.com/patent/US12200935
- https://patents.google.com/patent/US10910393
- https://patents.google.com/patent/US11631453
- https://patents.google.com/patent/US6246083
- https://patents.google.com/patent/US8421071
- https://patents.justia.com/patent/12082391
- https://patents.justia.com/patent/20220238532

**Oxide cells**
- https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology
- https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234
- https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html
- https://www.eenewseurope.com/news/imec-shows-capacitor-free-dram
- https://imec-publications.be/handle/20.500.12860/59908
- https://dc.engconfintl.org/ulsic_vs_tft_8/33
- https://sigroup.sjtu.edu.cn/files/AdvFunctMater_UltrathinOxide_DRAM_2026.pdf
- https://www.ithome.com/0/966/543.htm
- https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html
- https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology
- https://www.storagenewsletter.com/2025/05/08/neo-semiconductor-unveils-1t1c-and-3t0c-igzo-based-3d-x-dram-technology/
- https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/
- https://pc.watch.impress.co.jp/docs/column/semicon/2061772.html
- https://shine.nus.edu.sg/2025/02/18/1t1r-and-2toc1r-igzo-mos%e2%82%82-all-beol-3d-memory-cells/
- https://deepblue.lib.umich.edu/items/e6ac2d99-46aa-444a-bc41-2851e63c965c
- https://engineering.purdue.edu/~yep/Papers/VLSI2024%20T4-1_Zehao%20Lin.pdf
- https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf
- https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing

**DRAM baseline and 3D**
- https://www.techinsights.com/ja/node/37840
- https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7134/SQR-RD5N16G5K6HZZG.pdf
- https://www.trendforce.com/news/2025/03/11/news-micron-pioneers-1%CE%B3-ddr5-samples-with-reduced-euv-use-but-future-risks-loom/
- https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development
- https://semiengineering.com/baby-steps-towards-3d-dram/
- https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx
- https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/
- https://www.imec-publications.be/entities/publication/6228fcc8-685e-4e72-83ba-3cb478415500/full
- https://memlab.ece.gatech.edu/papers/ISCA_2013_1.pdf

**Facilities and partners**
- https://nanofabrication.nd.edu/facility-access/fees/
- https://www.nuance.northwestern.edu/documents/rates/2025-rates/2025-nufab.pdf
- https://unmnanofab.unm.edu/user-rates/2026-04-24.pdf
- https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale
- https://www.suss.com/de/news/technical-publications/suss-microtec-xbc300-gen2-neovation-microelectronics
- https://www.wlfi.com/2026/08/27/sk-hynix-partners-with-purdue-university-ceremonially-breaks-ground-4b-memory-chip-facility/
- https://evertiq.com/news/2026-08-28-sk-hynix-breaks-ground-on-4-billion-packaging-facility-in-indiana
- https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia
- https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm

**Resources**
- https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us
- https://www.engineeringnews.co.za/article/china-halts-ban-on-gallium-germanium-antimony-exports-to-us-but-controls-remain-2025-11-10
- https://www.trendforce.com/news/2025/10/09/news-china-expands-rare-earth-curbs-subjects-14nm-logic-and-256-layer-memory-chips-to-case-by-case-review/
- https://bits-chips.com/article/shining-brighter-a-10x-source-power-efficiency-boost-for-euv-lithography
- https://www.caixinglobal.com/2026-03-16/qatar-helium-shutdown-adds-new-risk-to-chip-supply-chain-102423361.html
- https://news.metal.com/newscontent/103938701-from-stability-to-surge-the-overseas-hafnium-market-caught-between-ai-demand-and-supply-controls
