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

*(Revised after red team.)* The cell is now a two-film cell, the "notched write pocket". A per-hole write film, confined in a notch of the write-plate level, contacts the top face of the ring. The single-film BL = SL closure turned out to be topologically impossible (§11).

**One-line thesis.** Build DRAM-class memory the way 3D NAND is built: deposit a tall stack of metal plates, etch one field of holes and line the holes with oxide-semiconductor films. Unlike NAND, every tier-hole crossing becomes a capacitorless, transistor-written gain cell that drives its own read current. Density then comes from tier count, not from lithography.

**Rank, category, score.**
- Rank 3 of 10, category cell/array.
- EV 60 = step size 5 × plausibility 3 × $1M-provability 4.
- Ranks 2-4 are within scoring noise. AND-STACK carries the portfolio's largest bits-per-dollar prize.
- *(Revised after red team.)* Plausibility falls from 3 to ~2 (P(closure) ~20%), and the bits/$ prize roughly halves (§11). The EV is not re-scored here.

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

**PHYSICALLY POSSIBLE? YES, conditionally, and only as a two-film cell (revised after red team).**
- The cell physics breaks no law. Oxide 2T0C cells, per-tier recessed rings and in-hole source/drain pillars have each been shown separately.
- The pre-red-team closure is topologically impossible: BL = SL writing on a single film lining the hole wall. In that layout the ring can only contact the film right next to its own read channel (RT-PROC-and-stack-01). That leg is killed.
- The revised two-film cell still needs three things:
  - select-plate CR ≥ 0.57 (σ ≤ 0.045) at a plate swing of ≤ 3.0 V;
  - a write-FET leakage tail of ≤ 17 aA at a −3.0 V write-plate hold, at 85 °C;
  - three process modules that have no precedent (§11.2).
- *Pre-red-team bars: CR ≥ 0.53 and a 21 aA tail.*

**STEP CHANGE IF IT WORKS? YES on density, modest on cost (revised after red team).**
- **64 tiers × 2 b:** 5.9× 1-beta density (was 8.1×). Bits/$ at component level is ~2.3× 2026 1-beta (2.2-2.6× across cost cases; was 3.8×), at 1% per-tier defects.
- **Against a ~2032 incumbent** ($0.69-0.90/GB): ~1.1-1.4× at first product, and 1.2-1.6× for a two-deck 96 × 2 b part.
- **32 × 2 b:** 2.9× density and 1.5× bits/$ (was 4.1× and 2.7×).
- **Refresh:** power is ~25× lower at 1 s retention (was 31×). The array needs no EUV.

**PROVABLE WITH $1M IN 24 MONTHS? PARTLY (revised after red team).**
- About $0.4M of direct spend decides the new crux by month 14. That buys a 2-tier vertical closure coupon plus planar statistics.
- A 4-tier stack and a 32-tier dummy-stack etch coupon complete a $970k plan by month 23.
- 64-tier manufacturability at 170 nm pitch, tier yield and cost need the $10-50M round or a NAND partner.

**FINAL STATUS: DOWNGRADED** (§11).

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

*(Revised after red team.)* The single-film arrangement drawn above cannot be wired. Wherever the ring touches the film, it touches the edge of its own read channel. In the redesign the select plate wraps only the ring's back face. The ring's top face is contacted by a separate write film in a notch of the write-plate level, and an Al₂O₃ plug in front of the ring serves as the read-gate dielectric. Select plates idle low and write plates hold at −3.0 V. See §11.2.

---

## 2. The physics and the numbers

All values come from `models/and-stack.py` unless tagged.

### 2.0 Red-team revisions to this section (revised after red team)

The model now carries a RED-TEAM REVISIONS block (old → new, with objection ids). Setting `APPLY_RT_REVISIONS = False` reproduces the pre-red-team numbers kept in §2.1-2.10 below. The revised values are:

| Quantity | Pre-red-team | Revised | Driver |
|---|---|---|---|
| Hole pitch / diameter / pillar width | 150 / 90 / 22 nm | 170 / 110 / 28 nm | PROC-03 (twin pillars) |
| Tier pitch, stack at 64 tiers | 80 nm, 5.42 µm, AR 60 | 90 nm, 6.06 µm, AR 55 | PROC-02 |
| Bit-tiers for 1-beta parity | 15.7 | 21.8 | pitch, array eff 0.66, parity 12% |
| 64 × 2 b density | 3.63 Gb/mm² (8.1×) | 2.62 Gb/mm² (5.9×) | PROC-02/03, CIRC-02 |
| Select wrap, IPD EOT → CR, C_SN | 1, 2.5 nm → 0.70, 0.246 fF | 0, 2.0 nm → 0.59, 0.214 fF | PROC-01 (top face is the write contact) |
| Read-FET slope at 85 °C | 90 mV/dec | 120 mV/dec (160 worst) | CIRC-01, DEV-04 |
| Unselected ring cutoff, pull-down | ≤ +0.01 V, 1.09 V | ≤ −0.15 V, 1.30 V | slope; guard 0.15 V (DEV-02) |
| CR bar, swing at base CR | ≥ 0.53 (σ 0.03, 2.5 V), 1.79 V | ≥ 0.57 (σ 0.045, 3.0 V), 2.83 V | DEV-02, PROC-05 |
| Write-plate hold, select idle | −1.5 V, idle at read level | −3.0 V, idle LOW | CIRC-01, DEV-03 |
| Read current, 2-b step, resolve | 0.89 µA, 298 nA, 1.5 ns | 0.70 µA, 234 nA, 1.9 ns | geometry |
| 2-b max drift, 1 s leak budget | 86 mV, 21 aA | 78 mV, 17 aA | kickback 206 mV, C_SN |
| Refresh power vs DDR5 at 1 s | 31× lower | 25× lower | write-plate swing 5.5 V |
| Write | 4 pulses, ~100 ns per cell | 2.8 KiB tier-page, 1.0 µs (no mux) to 7.8 µs (8:1 mux) | DEV-01, CIRC-03 |
| Wafer, 64 × 2 b component $/GB | $5,920, $0.39 (3.8×) | $8,400, $0.65 (2.3×; ~1.1-1.4× vs 2032) | PROC-04, IND-03 |
| Break-even tiers (2 b / 1 b) | 9 / 19 | 18 / 44 | PROC-04 |

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

*(Revised after red team.)* Hole area is 0.0288 µm² and density is 0.0205 Gb/mm² per bit-tier, so 1-beta parity needs 21.8 bit-tiers. That gives 32 × 2 b = 1.31 Gb/mm² (2.9×), 64 × 2 b = 2.62 Gb/mm² (5.9×), and 96 × 2 b in two decks = 3.93 Gb/mm² (8.8×). The web stays at 170 − 110 − 2×18 = 24 nm. The select plates are poly-SiGe at ~300 Ω/sq, which forces 60 µm segments (RC 4.3 ns) and a 14% staircase, and the array efficiency input falls to 0.66.

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

*(Revised after red team.)* The two-film cell has no top wrap: the ring's top face is the write contact. IPD EOT 2.0 nm then gives C_IPD 0.127, C_gate 0.072 and C_par 0.015 fF, so C_SN is 0.214 fF and CR is 0.59. At 120 mV/dec the unselected ring must sit at or below −0.15 V, so the pull-down is 1.30 V (guard 0.15 V). With σ 0.045 (CR_min 0.46), the plate swing is 2.83 V and the IPD carries 2.55 MV/cm. Offsetting the selected-plate level to V_ref ≈ +1.27 V centres the IPD bias at ≤ 1.27 V (2.1 MV/cm). The bar for a ≤ 3.0 V swing is **CR ≥ 0.57**. A 20% hole taper moves CR by only 0.001, because CR is a ratio of coaxial capacitors (model §11g). Kickback is now 206 mV (deterministic) and neighbour coupling 9 mV per volt.

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

*(Revised after red team.)*
- **Read.** 0.70 µA top-level current, a 234 nA level step, 1.9 ns to resolve, and ~16 ns array read including 4.3 ns of select-plate RC. About 5.7 fJ per cell, because the selected plate now swings 2.83 V from idle-low.
- **Write.** A shared write plate half-selects every hole on its tier (RT-DEV-and-stack-01). Writes are therefore tier-pages: 706 BLs × 16 groups = 11,294 cells, 2.8 KiB at 2 b. The sequence is:
  1. read the page into the buffer;
  2. hold write plate k on;
  3. drive the 16 groups in turn, each left floating at its target;
  4. float SL through a bottom select;
  5. verify.
- **Write time and energy.** 1.0 µs per page unmuxed and 7.8 µs at the 8:1 sense-amp mux the bonded periphery forces. About 108 fJ per 2-bit cell.
- **Bandwidth.** Internal read bandwidth is ~920 GB/s per mm² of array, ~880× the DDR5-class need per GB (model §11c-d).

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

*(Revised after red team.)*
- **Budget.** Random σ is 16 mV, so 2 b tolerates 78 mV of drift at raw BER 1e-4. The 1 s budget is 17 aA (8.6e-8 A/cm² over the IPD).
- **Refresh.** 0.45 mW/GB at 1 s, **25× lower** than DDR5.
- **Write-FET tail.** The write FET is wide and short (W/L ~38, I(Vt) ~3.8 µA). Its 1e-4 tail (−3.72σ at σ 40 mV, plus a 0.15 V DIBL penalty) leaks ~1.8 nA at the old −1.5 V hold. At −3.0 V it leaks 0.0006 aA at 120 mV/dec and 5 aA at 160 mV/dec.
- **Cross-temperature.** At −17 mV/K, write-to-read gaps of 5, 10 and 50 K leave residuals after references of 4.2, 8.5 and 42.5 mV. Regions are therefore refreshed when |T − T_write| > 5 K (model §11a, §11f).

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

*(Revised after red team; model §9 and §11i.)* Inputs are now $50/tier and a $2,200 array base. The base covers the notched write pocket, slit Ru replacement, twin sub-hole pillars, a bottom select and a second SADP level. Hole yield is 0.93, because pillar shorts are hole-level.

| Case | Density | Component $/GB | vs 2026 1-beta | vs ~2032 incumbent ($0.69-0.90) |
|---|---|---|---|---|
| 64 × 2 b revised | 5.9× | 0.65 | 2.3× | 1.1-1.4× |
| 64 × 2 b, rt-PROC case ($60/tier, $2,000 base) | 5.9× | 0.68 | 2.2× | 1.0-1.3× |
| 64 × 2 b, optimistic ($35, $1,600) | 5.9× | 0.56 | 2.6× | 1.2-1.6× |
| 96 × 2 b, two decks | 8.8× | 0.57 | 2.6× | 1.2-1.6× |
| 32 × 2 b | 2.9× | 0.97 | 1.5× | 0.7-0.9× |
| 64 × 1 b | 2.9× | 1.19 | 1.2× | 0.6-0.8× |

Break-even is now 18 tiers at 2 b and 44 at 1 b.

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

*(Revised after red team.)* These criteria are superseded by GO #1A (planar, month 9) and GO #1B (vertical closure coupon, month 14) in §5 and §11.5. GO #1B is the decisive gate. GO #1A adds five measurements:
- write-FET tails on ≥ 1e4 devices;
- Vt(T) and cross-temperature BER;
- own-tier read disturb;
- variable retention time (VRT), from retention re-measured ≥ 100 times on ≥ 1e4 cells;
- read-FET RTN over windows from 10 ns to 1 s.

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
| 2 | Topology closure: the ring must touch the film where the write plate gates it, yet be insulated where it gates the read | Any ring-to-read-path short (TCAD, month 3) | BL = SL writing (own proposal, unverified); else segmented write and read films, at +2 recesses. *(Revised after red team: one film cannot close, so BL = SL is killed. The answer is the two-film notched write pocket, §11.2.)* |
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

## 5. The decisive experiment (revised after red team)

**Question.** Does the two-film notched write pocket close: can a ring be written through a per-hole write film yet stay isolated from its own read channel? Then three physics questions follow:
- can one select plate, idling low, mute 63 neighbours at the real 120-160 mV/dec slope;
- does the write FET hold ≤ 17 aA at its 1e-4 tail;
- do 4 levels survive 1 s at 85 °C and a 10 K write-to-read temperature step?

*The pre-red-team question asked only for select-plate muting and 1 s retention on a planar emulation. That emulation cannot test closure, half-select, tier taper or cross-temperature reads.*

**Phase 0 (months 1-3, ~$35k).**
1. Run 3D TCAD of the notch write segment, including fringe, curvature and DIBL. It must show ≥ 9 decades at a −3.0 V hold.
2. Run CR versus geometry (wrap 0, IPD EOT 2.0-2.5 nm, hole CD ±20%).
3. Run SPICE of the 16-group sequential write, with extracted pillar coupling. Floated groups must stay within < 10 mV.
4. Draw a bonded-SA floorplan: one SA per 8 BLs.
5. Run an architecture study of the write-back buffer.
6. Complete the freedom-to-operate claim charts (Macronix 3D AND ×3, SEL NOSRAM, US 8,421,071, US11631453, NEO 3D X-DRAM) and file Provisional #1 on the notch-write module and the bias scheme.

**Phase 1A (months 2-9, ~$90k fab + $20k analysis). Planar physics.**
- **Facilities and structure.** Same as before: Purdue Birck or GT IEN, with ALD at NUFAB or Argonne CNM. The 64-cell AND emulation has e-beam TiN islands. To it add arrays of ≥ 1e4 single write FETs and read FETs, at the real channel lengths, measured on a semi-automatic hot-chuck prober.
- **Measurements:**
  - CR across ≥ 50 cells;
  - per-cell off-current and Vt distribution on ≥ 1e4 cells at 85 °C;
  - write-FET hold leakage at the idle-low bias, 1e-4 tail;
  - read-FET slope and Vt(T) from 25 to 110 °C;
  - 2-b retention to 1e4 s;
  - cross-temperature 2-b BER with in-page references (ΔT ±10 K, characterised to ±50 K);
  - disturb after 1e8 own-tier select excursions and 1e9 neighbour writes;
  - VRT, with retention re-measured ≥ 100 times on ≥ 1e4 cells;
  - read-FET RTN over windows from 10 ns to 1 s;
  - endurance to 1e12 cycles;
  - SIMS.

**Phase 1B (months 4-14, ~$150k fab + $25k FIB/TEM). The 2-tier vertical closure coupon: the decisive gate.**
- **Stack.** 2 × (SiO₂ / doped poly-SiGe select / SiO₂ / SiN write-plate sacrificial layer), with 250 nm e-beam holes (Birck or NIST CNST).
- **Module sequence:**
  1. SiGe recess;
  2. IPD (SiO₂ + HfO₂);
  3. TiN ring and etch-back;
  4. Al₂O₃ read-gate plug;
  5. SiN notch;
  6. selective ALE opening of the IPD membrane on the ring top;
  7. Ga-rich IGZO write film, sacrificial fill and etch-back;
  8. In-rich read film;
  9. pillars;
  10. trench "slit", back-side removal of the SiN and the fill, 8 nm write-gate dielectric and an O₂-ALD Ru fill.
- **Measurements:**
  - FIB/TEM of the notch contact;
  - electrical write-then-read on both tiers;
  - ring hold at 85 °C;
  - CR per tier;
  - IGZO ΔVt and drift after the Ru fill;
  - SIMS for F and H.

**Dummy-stack etch coupon (months 8-16, ~$80k).** A 32-tier SiO₂ / poly-SiGe / SiN stack with no cells, run through a tool-vendor demo lab or a NY CREATES short loop. Etch 110 nm holes, then measure CD taper, bow and SiGe recess uniformity by TEM. If no slot is available, it moves to the raise.

**Phase 2 (months 14-23, ~$140k fab + $30k FA). A 4-tier vertical stack, one lot.** It re-uses the 1B flow and adds:
- a shared write plate across ≥ 2 hole-top select groups, to test the sequential group write;
- a bottom select;
- read current versus tier;
- tier-to-tier CR;
- a defect-confinement map.

**Readout.** Bench B1500A + WGFMU, or the shared MARGIN STACK MPW chip.

| Budget line (standalone) | $k |
|---|---|
| Two founders, lean, 24 months | 190 |
| IP: freedom-to-operate claim charts (now including NEO), 3 provisionals, PCT | 60 |
| Phase 0 TCAD, SPICE and architecture | 35 |
| Bench: used B1500A/WGFMU, semi-automatic hot-chuck prober, switch matrix | 85 |
| Phase 1A planar fab | 90 |
| Phase 1A SIMS, XPS, TEM | 20 |
| Phase 1B 2-tier closure coupon fab | 150 |
| Phase 1B FIB/TEM | 25 |
| 32-tier dummy-stack etch coupon (vendor demo or NY CREATES) | 80 |
| Phase 2 4-tier stack fab (one lot) | 140 |
| Phase 2 FIB/TEM | 30 |
| Travel, legal, company | 40 |
| Contingency | 25 |
| **Total** | **970** |

**Rate anchors and allocation.** All budget lines are [ESTIMATE]. Rates are anchored to Notre Dame ($124/h), UNM ($88-250/h) and NUFAB. Direct spend to GO #1B is ~$0.4M: Phase 0, Phase 1A, Phase 1B and the bench. Under the portfolio's ~$150k allocation, Phase 0 plus the planar write-FET and cutoff statistics are the seed deliverable. The closure coupon then becomes the first funded milestone.

**Pass/fail.**
- **#1A (month 9):** CR ≥ 0.57 with within-tier σ ≤ 0.045; ≤ 111 fA per unselected cell; write-FET 1e-4 tail ≤ 17 aA; 4 levels for ≥ 1 s at 85 °C with ≤ 78 mV tail drift; cross-temperature 2-b BER ≤ 1e-4 at ±10 K; ≤ 30 mV disturb.
- **#1B (month 14, decisive):** write-then-read on ≥ 2 tiers with no ring-to-read-channel short; ring hold ≤ 100 aA at 85 °C with the write plate at −3.0 V; per-tier CR ≥ 0.57; FIB/TEM of the notch contact.
- **#2 (month 22-23):** every tier meets #1A; the sequential group write leaves ≤ 10 mV on floated groups; tier-to-tier CR offset is trimmable; leakage tails are within 2× of planar.

## 6. The $1M, 24-month plan

Month 1 = January 2027.

| Quarter | Milestones | Gate |
|---|---|---|
| Q1 2027 | TCAD (notch segment ≥ 9 decades), SPICE (group write), claim charts; Provisional #1; bench; nanofab onboarding | **G0:** notch segment ≥ 9 decades at −3.0 V; nominal CR ≥ 0.57 |
| Q2 2027 | Phase 1A run; write-FET and Vt statistics on ≥ 1e4 devices; 1B short loops (SiGe recess, plug, notch) | Write-FET tail trending ≤ 100 aA |
| Q3 2027 | **GO/NO-GO #1A (month 9)**; 1B first coupon lot; Provisional #2 | **G1A:** §5 #1A |
| Q4 2027 | 1B second lot (ALE open, write-film confinement, Ru fill); dummy-stack etch slot; PCT (month 12) | Notch contact seen in TEM |
| Q1 2028 | **GO/NO-GO #1B (month 14, decisive)**; Phase 2 lot starts | **G1B:** write-then-read on 2 tiers |
| Q2 2028 | 4-tier lot; dummy-stack TEM results; **kill single-etch if 1B has not closed by month 18** | Recess σ ≤ 2 nm; CD ≤ 5% |
| Q3 2028 | Group-write test; reliability; FA | Floated groups ≤ 10 mV |
| Q4 2028 | **GO/NO-GO #2**; demo; data room; raise | **G2:** §5 #2 |

**Allocation** *(revised after red team)*. ~48% fab and etch coupon, 20% founders, 9% bench, 8% analysis, 6% IP, 4% design and 7% overhead plus contingency, on a $970k total.

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

## 9. Kill criteria (revised after red team)

Physics only. Month 1 = January 2027. The pre-red-team criteria assumed the single-film cell. That leg is now killed (RT-PROC-and-stack-01), so these criteria apply to the two-film notched write pocket.

1. **2027-03-31 (G0).** Kill single-etch and move to the coaxial or per-tier fallback if TCAD shows either of two things:
   - no notch geometry reaches ≥ 9 decades of write-segment suppression at a −3.0 V hold, with a 120 mV/dec slope and DIBL;
   - nominal CR is < 0.55 for every geometry with IPD EOT ≥ 2.0 nm and web ≥ 20 nm.
   *Revival:* wrap 0.5 (bottom select cap) without a short path, or a 190 nm pitch.
2. **2027-09-30 (#1A).** If measured CR mean is < 0.40, or within-tier σ is > 0.07 over ≥ 50 cells: kill single-etch. *Revival:* > 3.5 V drivers with IPD stress shown to 1e12 excursions.
3. **2027-09-30.** Ring tail leakage at 85 °C:
   - > 1 fA means 1 b holds < 53 ms: kill the DRAM-class claim;
   - > 100 aA: drop to 1 b;
   - *Revival:* a split at ≤ 17 aA.
4. **2027-09-30.** Write-FET hold leakage 1e-4 tail at a −3.0 V hold on ≥ 1e4 devices:
   - > 100 aA: drop 2 b;
   - > 1 fA: kill;
   - *Revival:* a −3.5 V hold with an 8-10 nm write-gate dielectric, or a higher-Vt write film.
5. **2027-09-30.** If 63-cell on/off is < 1e4 at 85 °C with a swing ≤ 3.5 V: kill.
6. **2027-09-30.** Disturb > 1 LSB after 1e8 own-tier excursions or 1e9 neighbour writes: drop 2 b. Disturb > 250 mV at 1 b: kill.
7. **2027-09-30.** Drift > 78 mV in 1 s at 85 °C on both molds, or a cross-temperature residual > 30 mV at ΔT 10 K with references: drop 2 b. A 1-b drift > 250 mV in 1 s: kill.
8. **2028-06-30.** If coupon 1B has shown no write-then-read closure on ≥ 2 tiers, or the ring hold through the notch segment exceeds 1 fA: **kill the single-etch leg**. Only the per-tier patterned fallback survives, at ~1.0-1.6× bits/$, and the bits/$ step-change claim dies. *Revival:* an area-selective or self-aligned write-film confinement shown on a 2-tier coupon.
9. **2028-10-31.** If any 4-tier stack tier is worse than 2× planar in CR or leakage tail, or untrimmed tier σ_CR is > 0.07: kill single-etch and move to the fallback.
10. **2028-10-31.** If the non-confined defect share is > 30% **and** the per-tier killer rate is > 3%, 64 × 2 b falls below ~1.5× bits/$ vs 2026 1-beta: kill the bits/$ claim and keep only the density and energy niche.
11. **2028-10-31.** If endurance at 85 °C is < 1e10 cycles (~8× the 1-s refresh need): kill.

**Pivot, not a kill.** Two triggers lead to a partner, JDA or licensing route rather than a kill: a blocking patent (Macronix, NEO), or a failed dummy-stack etch (CD variation > 5% or recess σ > 2 nm at 32 tiers). An etch failure also moves the stack to two decks or a wider pitch.

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
