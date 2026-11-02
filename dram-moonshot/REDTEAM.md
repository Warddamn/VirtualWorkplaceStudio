# NEW DRAM — PHYSICS RED TEAM

## Red-team narrative

### What the red team was asked to do

Ten concepts reached the red team, distilled from 12,857 generated ideas (10,525 distinct) through 30 ADVANCE ideas. Each arrived with a dossier and a runnable model. Four reviewers attacked every dossier independently, one lens each:

| Lens | Reviewer (from `rt_*.json`) | What it attacked |
|---|---|---|
| DEV | Device physicist | Oxide semiconductors, Schottky contacts, leakage, RTN (random telegraph noise: a transistor's threshold jumping between levels as single traps fill and empty), BTI and hydrogen reliability, charge transfer |
| PROC | 30-year DRAM and 3D-NAND process-integration veteran | Deep etch, ALD, staircases, hybrid bonding, overlay, thermal budget, contamination, yield per layer, fab cost per wafer |
| CIRC | DRAM circuit and sense-amp designer | Signal margin, offset and RTN, coupling, timing, periphery pitch, refresh, ECC (error-correcting code) hardware, row hammer |
| IND | Memory-industry strategist and deep-tech investor | Prior art and patent estates, licensing economics, competitive response, seed and Series-A fundability |

The rule came from `MISSION.md`: kill only for physics. An idea dies only if it breaks a law of physics or hits a known show-stopper with no plausible way around it. Business, timing and founder fit are not grounds. Three lenses attacked physics and engineering. IND tested whether the step change and an ownable position were real; its findings could downgrade or re-scope, never kill (the owners say so in RT-IND-lean-array-module-01 and RT-IND-pixel-stack-03).

Every objection got a written answer and a disposition: REFUTED (wrong), ACCEPTED-MITIGATED (right; a priced redesign answers it), ACCEPTED-DOWNGRADE (right; the claim shrinks) or ACCEPTED-KILL (right; a named sub-claim, a "leg", dies, not the whole concept). Reviewers set severity as FATAL, MAJOR or MINOR.

*Sources.* Counts come from `research/redteam/rt_*.json` and `responses_*.json`. Outcomes come from each dossier's section 11, which matches the response file's `final_status` in all ten cases. Revised figures are the owners' model re-runs (`models/<slug>.py`, RED-TEAM REVISIONS block); they carry no evidence tag in the source unless one is shown.

### The counts

**By lens.** 181 objections, all 181 answered, 0 unanswered.

| Lens | Objections | FATAL | MAJOR | MINOR | REFUTED | MITIGATED | DOWNGRADE | KILL |
|---|---|---|---|---|---|---|---|---|
| DEV | 45 | 0 | 27 | 18 | 1 | 30 | 14 | 0 |
| PROC | 44 | 2 | 32 | 10 | 0 | 24 | 18 | 2 |
| CIRC | 46 | 0 | 30 | 16 | 1 | 25 | 16 | 4 |
| IND | 46 | 1 | 34 | 11 | 0 | 22 | 24 | 0 |
| **Total** | **181** | **3** | **123** | **55** | **2** | **101** | **72** | **6** |

**By concept.** Every concept ended DOWNGRADED.

| Concept | DEV | PROC | CIRC | IND | Total | FATAL / MAJOR / MINOR | REF / MIT / DOWN / KILL | Final status |
|---|---|---|---|---|---|---|---|---|
| hot-side-memory | 4 | 5 | 5 | 5 | 19 | 1 / 14 / 4 | 0 / 13 / 6 / 0 | DOWNGRADED |
| raw-ber-contract | 5 | 4 | 5 | 5 | 19 | 0 / 14 / 5 | 0 / 10 / 7 / 2 | DOWNGRADED |
| and-stack | 5 | 5 | 5 | 5 | 20 | 1 / 14 / 5 | 1 / 12 / 6 / 1 | DOWNGRADED |
| margin-stack | 5 | 4 | 6 | 4 | 19 | 0 / 15 / 4 | 0 / 8 / 11 / 0 | DOWNGRADED |
| pixel-stack | 4 | 4 | 5 | 5 | 18 | 0 / 10 / 8 | 0 / 8 / 10 / 0 | DOWNGRADED |
| diode-tower | 4 | 4 | 4 | 4 | 16 | 0 / 13 / 3 | 1 / 10 / 5 / 0 | DOWNGRADED |
| charge-river | 5 | 6 | 4 | 4 | 19 | 0 / 13 / 6 | 0 / 12 / 6 / 1 | DOWNGRADED |
| cell-wafer-foundry | 4 | 4 | 4 | 5 | 17 | 0 / 10 / 7 | 0 / 12 / 5 / 0 | DOWNGRADED |
| lean-array-module | 5 | 5 | 4 | 4 | 18 | 1 / 10 / 7 | 0 / 8 / 9 / 1 | DOWNGRADED |
| ai-memory-diet | 4 | 3 | 4 | 5 | 16 | 0 / 10 / 6 | 0 / 8 / 7 / 1 | DOWNGRADED |

**Severity versus disposition.** The 3 FATAL objections ended as 1 KILL, 1 MITIGATED and 1 DOWNGRADE. The 123 MAJOR objections ended as 2 REFUTED, 59 MITIGATED, 57 DOWNGRADE and 5 KILL. The 55 MINOR objections ended as 41 MITIGATED and 14 DOWNGRADE.

**The three FATAL objections:**
- RT-PROC-and-stack-01: the single-film write path cannot be built. The owner showed it is topologically impossible; that leg was killed.
- RT-PROC-hot-side-memory-01: a carrier bonded before backside lithography leaves ~3-10 nm of intrafield distortion against a <10 nm overlay budget. Mitigated by a carrier-last flow.
- RT-IND-lean-array-module-01: nothing a venture could own, "FATAL to the venture path, not to the physics". Downgraded and re-scoped.

**The six kills hit five legs:** the single-film AND-STACK closure; the AI-MEMORY-DIET all-layer latent; the CHARGE-RIVER cost-per-bit leg; LEAN ARRAY's AAO capacitor at the 35 nm pitch; and the RAW-BER sense-amp flag, which took two kills. **The two refutations:** RT-DEV-and-stack-02 (its tail arithmetic was 1000x high) and RT-CIRC-diode-tower-02 (refresh re-writes each level at the current temperature, so the write-to-read gap is bounded by slew times interval).

### Recurring objections, and how they were answered

**1. Oxide-transistor tail statistics after the ≤400 °C thermal, hydrogen and bonding budget.** This attack hit all seven oxide-transistor concepts, reached RAW-BER and LEAN ARRAY too, and moved most of the numbers.
- Dossiers sized cells from median devices; the pass lines sit in the tails.
- MARGIN STACK's 1e-10 leakage tail was never derived from its own inputs (RT-DEV-margin-stack-01).
- HOT-SIDE's 1e-4 tail cell was assumed to leak 3x the median. On the dossier's own sigma it is 15x, 91x or 8,217x at a write-FET sigma_Vt of 30, 50 or 100 mV (RT-DEV-hot-side-memory-01).
- RTN was budgeted as a small Gaussian; in 0.01 µm²-class devices it has a heavy exponential tail (MARGIN STACK, PIXEL-STACK, CHARGE-RIVER, HOT-SIDE).
- Hydrogen came from cumulative tier processing (PIXEL-STACK), bond-plane water at ~2-5e14 H2O/cm² (CELL-WAFER FOUNDRY, HOT-SIDE) and an H2 backside-gas leak (LEAN ARRAY).

The answers share a shape. Assumed tails became measured-quantile GO lines. Error models now carry heavy-tail RTN, with screening and sparing. Owners added negative hold biases, ALD Al2O3 hydrogen barriers and D2O-labelled real-bond splits that SIMS can tell apart. Series write transistors (top-up idea I-12627) get credit only where defects can be independent; bond-plane hydrogen is a correlated sheet source, so it gets none. The cost was real: HOT-SIDE now plans at 1 bit per cell, not 2; PIXEL-STACK's design capacitor rose from 0.45 to 0.60 fF; MARGIN STACK withdrew its 17-40x stretch and 28x refresh claim.

**2. Prior art.** IND raised an ownership objection against every concept. imec owns the oxide-CCD direction (CHARGE-RIVER). NEO and Macronix surround AND-STACK. SEL's DOSRAM patents say a short bitline allows a smaller capacitor (MARGIN STACK). Kepler's 1T-nC stack plus US 2007/0183191 make an obviousness case (DIODE-TOWER). US 10,395,963 lists H2 as a backside gas (LEAN ARRAY). The array/periphery split is anticipated (CELL-WAFER FOUNDRY). Per-layer latents are MHA2MLA/TransMLA (AI MEMORY DIET). No concept died on this. Claims narrowed to implementation details, claim reading and an FTO (freedom-to-operate) opinion now precede filing, and IP lines rose (for example $45k to $55k).

**3. Refresh and ECC assumptions.** RAW-BER's 15x refresh headline gave up chipkill (ECC that survives a whole dead chip); with chipkill kept it is ~9x on DDR5. MARGIN STACK and CELL-WAFER FOUNDRY counted the margin ECC buys but not its parity: +6.2% die for MARGIN STACK, 15.6% parity behind CELL-WAFER FOUNDRY's 26 mV threshold. HOT-SIDE's RS(36,32) code could not also cover random errors at raw BER (bit error rate) 1e-4, so an inner row BCH was added (combined overhead 1.149). Parity is now in every affected model, and RAW-BER's measurement sets the shared error budget.

**4. Heat on the hot side of a GPU.** a-IGZO threshold moves ~-17 mV/K, so a 20-40 K swing between write and read eats a 2-bit window (RT-CIRC-hot-side-memory-02). All logic heat crosses the tiers: up to +22.9 K over 10 W/mm² hotspots without copper via fill (RT-IND-hot-side-memory-05). The answers: in-row reference cells; a rewrite when |T − T_write| > 10 K (8.5 mV residual); 1 bit per cell in hotspots; 10% copper fill over hotspots (0.93 K). Planning capacity at 16 tiers halved, 157 to 78 GB/GPU. AND-STACK got the same treatment (in-page references, refresh when ΔT > 5 K).

**5. Bonding, overlay, voids and per-layer cost.** HOT-SIDE's FATAL overlay objection produced a carrier-last flow (+$400/wafer, 1% logic scrap). Saddle warp leaves ±2.20 µm of wafer-to-wafer residual against a 0.375 µm budget at 1.5 µm pitch, so CELL-WAFER FOUNDRY made D2W (die-to-wafer) bonding primary at 2.0 µm (0.14 µm error against 0.50 µm). Void, contamination (In/Ga/Zn ≤1e10 at/cm²) and royalty terms entered the models. PROC repriced stacked layers at NAND's own economics (CHARGE-RIVER $10 to $25 per plate; AND-STACK $50 per tier), and PIXEL-STACK's 0.998 tier yield was flagged as a requirement, not a measurement. These changes cut most bits-per-dollar claims.

### Concept by concept

**HOT-SIDE MEMORY: DOWNGRADED.** No leg was killed, but "refresh-free" became "refresh-light" and bond-first gave way to carrier-last. What survived is ~10x lower energy per bit than HBM (high-bandwidth memory): 0.37 vs 3.95 pJ/b delivered, 5.5-15x by placement. The saving fell from ~190 to ~90 W/GPU in the 16-tier, 1-bit planning case (~170 W if 2 bits work), and cost rose to $4.6-12/GB. Revival of 2 bits per cell needs a measured 1e-4 RTN quantile ≤30 mV, a cross-temperature residual ≤10 mV, tail leakage ≤7.5 aA (attoamps) at 105 °C and drift ≤20 mV in a ≥600 mV window.

**RAW-BER CONTRACT: DOWNGRADED.** The per-read sense-amp flag was killed: a delayed strobe sees 50-150 ps of skew against a 14-35 ps window, and even ideal flags net −2.2% to −0.2% of die. Relaxed refresh behind a side-band code survived with chipkill kept: ~9x on DDR5 RDIMMs at 85 °C (6.1-20x), ~13x on retired DDR4 behind CXL, 2.9x in degraded mode, worth ~$3.9 per module over 5 years. The flag revives only with silicon showing a flag-window sigma ≤1.5 mV across ≥1k sense amps at 85 °C without trim, plus a positive area ledger.

**AND-STACK: DOWNGRADED.** The single-film, single-etch closure was killed: a ring contact on one wall-lining film always touches its own read channel. A two-film "notched write pocket" cell survives [SPECULATIVE], with P(closure) ~20% [ESTIMATE]. Density is 5.9x 1-beta (the 2026 incumbent node; was 8.1x). Bits/$ is 2.3x against 2026 1-beta (was 3.8x) but ~1.1-1.4x against a projected 2032 incumbent, and refresh power is ~25x lower. The gate is a 2-tier vertical closure coupon at month 14; if it has not closed by month 18, single-etch is killed.

**MARGIN STACK: DOWNGRADED.** No leg was killed, but the 17-40x stretch, the 28x refresh claim, "$/bit flat" and "no EUV added" were withdrawn. The sensing-limited cell is 0.13/0.29/0.74 fF (optimistic/central/pessimistic), so the 0.5 fF planning cell closes in the central case and the 1.0 fF fallback in all three; the capacitor is 10.8x shorter. The price is +9% to +25% $/bit and −11% density against plain 4F2, and EV fell from 75 to 24. Revival is the M17 GO: projected BER ≤9e-5 at 0.5 fF, RTN ≤44 mV and an aged 2e-5 leakage quantile ≤586 aA. IND adds that a memory maker must say capacitor deletion is worth paying for.

**PIXEL-STACK: DOWNGRADED.** No leg was killed, and the read closes at a 0.60 fF design capacitor. Density fell from 6.2x to 4.6x 1-beta at 64 tiers, bits/$ from 2.5x to ~parity, and the edge over incumbent-style 3D from 2.5x to ~1.5x. It returns to STANDS at ~5.2-5.9x only if the M9 time-domain RTN residual comes in at ≤20 mV.

**DIODE-TOWER: DOWNGRADED.** No leg was killed and one objection was refuted. But AgOx, the only contact class that met the barrier bar, decomposes inside the thermal budget and is now diagnostic only. Density stays ~3.9x 1-beta at 64 tiers; $/bit moved from 0.35x to 0.55x; P(pass) is ~5-10% [ESTIMATE] and EV fell from 45 to ~16. Revival is Gate A (2027-07-30): a process-integrable bottom-anode contact with 99.99th-percentile ring leakage ≤928 aA at 85 °C and an RTN tail ≤25 mV.

**CHARGE-RIVER: DOWNGRADED.** The cost-per-bit leg was killed: at $25/plate the part costs $1.74/GB, 0.85x DDR5. Density of ~2.5x 1-beta (was 3.6x), ~158x lower standby power and ~2.4-3x lower energy per useful bit than HBM3 including I/O survive, though the regeneration fix needs a deck-joint tier [SPECULATIVE]. The cost leg revives at ≤$12 per plate pair plus staircase-free contacts.

**CELL-WAFER FOUNDRY: DOWNGRADED.** No leg was killed; the merchant, open-interface leg was demoted to optional. Capex per GB/month is 3.6x lower (was 7.6x), $/GB is 0.62x DDR5 (was 0.36x), with zero EUV layers. The split itself supplies only ~1.5x of the capex factor; the rest is tier density. The full claim revives with a ≤2-deck 64-tier flow on a ≤$3k cell wafer, a measured ≥$15/tier NAND-line advantage over logic BEOL, and an LOI pair trading under the spec.

**LEAN ARRAY MODULE: DOWNGRADED.** The AAO (anodic aluminium oxide) capacitor at the 35 nm pitch was killed: it needs a 5.6 nm core filled at aspect ratio ~450. The venture was re-scoped to a program co-funded by a JDA (joint development agreement) and grants. H2 backside cooling survives: the effective accommodation prior is 0.19-0.21 against a 0.17 GO line, P(GO) ~35-55% (EV 40 to 30), for ~3% of DRAM helium at 1.0x $/bit. It returns to STANDS if a_H2 ≥0.20 after plasma pretreatment, backside cooling is >10% of fab helium, and a partner pays NRE.

**AI MEMORY DIET: DOWNGRADED.** The single all-layer latent was killed: it needs 26.7x more decode reads. Host-lite tiering survives at 1.40x fewer DRAM GB per human-chat conversation (1.17x in wafer terms) and ~1.17x fleet-wide at 50% agent traffic [ESTIMATE, model section 11]; S fell from 2 to 1 and EV from 30 to 15. Deleting host DRAM alone caps at 1.28x. A step change needs chat GPUs with ~2/3 of today's HBM, about 1.7x [SPECULATIVE], and would be scored as a new concept.

### The one experiment that resolves the most objections

The judge physicist named it the Oxide Tail Statistics (OTS) lot (`judge_physicist.json`). `decision.json` makes it the portfolio thesis.

One shared planar reticle carries 65k small-area (0.01-0.02 µm²) source followers with an on-coupon 15 ns dual sample-and-hold, ≥1e5-1e6 floating-node leakage cells with single and series write gates, planar AND-STACK CR and disturb cells, integrable-anode Schottky diodes and minimal 3-phase CCDs. It would run as two lots at Purdue Birck, with GT IEN as second source, in IGZO, In-poor IGZO, IGO and Ga-free ZTO/In2O3. Splits cover 1x/2x/4x cumulative hydrogen and thermal dose plus a D2O-labelled 350-400 °C bond. The physicist's budget is $220k for the lots, plus $100k of add-ons and a $60k bench.

| Concept | Pass line the lot measures (judge files; CWF from its dossier §5) | Objections it bears on |
|---|---|---|
| HOT-SIDE | tail ≤22.5 aA at 125 °C; RTN ≤100 mV (1 b) / ≤30 mV (2 b) | DEV-01, DEV-02, DEV-03, CIRC-02 |
| AND-STACK | write-FET tail ≤17 aA at −3 V hold | CIRC-01, DEV-02, DEV-03 |
| MARGIN STACK | aged 2e-5 quantile ≤586 aA; RTN ≤44 mV | DEV-01, DEV-03, DEV-05, CIRC-04, PROC-03 |
| PIXEL-STACK | SF residual ≤40 mV; tail ≤45-90 aA | DEV-01, DEV-02, DEV-03, CIRC-02, CIRC-05, PROC-02 |
| DIODE-TOWER | RTN tail ≤25 mV; integrable-anode leakage | CIRC-01, DEV-01, DEV-02, DEV-03, PROC-01 |
| CHARGE-RIVER | FD-SF 1e-9 step ≤30 e- | DEV-01, DEV-02, CIRC-04 |
| CELL-WAFER FOUNDRY | top-tier ΔVt ≤20 mV after a real bond (D2O split) | DEV-01, DEV-02 |

That is 28 objections across seven concepts. The physicist wrote that "one measurement campaign sets the size of the step for 7 of the 10 concepts". The lot also tests whether neighbouring tails are independent, which decides whether series write gates help. The operator judge framed the stakes: "With near-Gaussian tails, 3-4 cells live. With heavy tails, the portfolio collapses to RAW-BER plus a 1 b HOT-SIDE tier." The judge panel was unanimous. BEST BET is HOT-SIDE MEMORY, FASTEST PROOF is RAW-BER CONTRACT, and MOONSHOT is AND-STACK.

### What "DOWNGRADED, none killed" means, and what it does not

**What it means.** Under the mission's rule, no reviewer found a broken law or a show-stopper with no plausible way around it. All 181 objections have a written answer and a disposition; the compiler that builds this file exits with an error if any is missing. The FATAL overlay objection on HOT-SIDE became a priced redesign and a new gate rather than a kill.

**What it does not mean:**
- **The claims did not stand.** `decision.json` sums it up as "~2x on headline claims". Five legs died.
- **Cheap bits did not survive.** No concept still claims more than ~1.6x bits/$ against a projected 2032 incumbent.
- **Some survivals are bets.** Several rest on numbers nobody has measured yet (oxide tails, RTN at ns timescales, bond hydrogen) or on process steps nobody has built ([SPECULATIVE] modules; P(closure) ~20% [ESTIMATE]; DIODE-TOWER P(pass) ~5-10% [ESTIMATE]).
- **Surviving physics is not a business.** LEAN ARRAY's IND objection was FATAL to the venture path.
- **The red team did not see the answers.** The owners wrote them, and no second round was run: the compiler accepts round-2 files (`rt2_*.json`), but none exist.

"Not killed" means the concept is still worth measuring. It does not mean the concept is proven.

## Method

Four adversarial reviewers attacked every deep dive independently, in two rounds (round 1: DD1–DD5, `rt_*.json`; round 2: DD6–DD7, `rt2_*.json`): **CIRC** — DRAM circuit and sense-amplifier designer (signal margin, offset/RTN, coupling, timing, periphery pitch, refresh, ECC hardware, hammer), **DEV** — Device physicist (oxide semiconductors, ferroelectrics, Schottky contacts, leakage/RTN/BTI/hydrogen reliability, charge transfer); IEDM/VLSI/Nature Electronics reviewer, **IND** — Memory-industry strategist and deep-tech investor (prior art and patent estates of the memory majors, licensing economics, competitive response, seed and Series-A fundability), **PROC** — 30-year DRAM and 3D-NAND process-integration veteran (deep etch, ALD, staircase, hybrid bonding, overlay, CMP, thermal budget, contamination, yield per layer, tool sets, fab cost per wafer). Every objection is reproduced **verbatim** below with the deep-dive owner's response, a disposition (REFUTED / ACCEPTED-MITIGATED / ACCEPTED-DOWNGRADE / ACCEPTED-KILL) and the action taken. Objections are answered, never deleted. This file is generated by `research/tools/compile_redteam.py` from `research/phase5/rt_*.json` and `research/phase5/responses_*.json`.

## Scoreboard

| Deep dive | Final status | Objections | FATAL | MAJOR | MINOR | REFUTED | ACCEPTED-MITIGATED | ACCEPTED-DOWNGRADE | ACCEPTED-KILL |
|---|---|---|---|---|---|---|---|---|---|
| ai-memory-diet AI MEMORY DIET | **DOWNGRADED** | 16 | 0 | 10 | 6 | 0 | 8 | 7 | 1 |
| and-stack AND-STACK: single-etch 3D oxide gain-cell DRAM (revised: two-film notched-write-pocket cell) | **DOWNGRADED** | 20 | 1 | 14 | 5 | 1 | 12 | 6 | 1 |
| cell-wafer-foundry CELL-WAFER FOUNDRY: litho-light periodic oxide cell wafers bonded to U.S. foundry periphery under an open bitline-group bond spec | **DOWNGRADED** | 17 | 0 | 10 | 7 | 0 | 12 | 5 | 0 |
| charge-river CHARGE-RIVER: buried-channel oxide CCD strings, scheduled like a drum for LLM weight and KV streaming | **DOWNGRADED** | 19 | 0 | 13 | 6 | 0 | 12 | 6 | 1 |
| diode-tower DIODE-TOWER: two stacked transistors and 16-64 wrapped linear-capacitor tiers per pillar, steered by per-tier oxide Schottky diodes and read by a double-sampled in-hole gain FET | **DOWNGRADED** | 16 | 0 | 13 | 3 | 1 | 10 | 5 | 0 |
| hot-side-memory HOT-SIDE MEMORY: oxide gain-cell tiers in the backside-power carrier wafer (carrier-last), plus at most 4 tiers in the logic BEOL | **DOWNGRADED** | 19 | 1 | 14 | 4 | 0 | 13 | 6 | 0 |
| lean-array-module LEAN ARRAY MODULE: helium-free, PFAS-light, EUV-free process modules for periodic memory arrays | **DOWNGRADED** | 18 | 1 | 10 | 7 | 0 | 8 | 9 | 1 |
| margin-stack MARGIN STACK: segment-gain, double-sampled, ECC-budgeted sensing that cuts the cell capacitor ~10x on oxide-access DRAM | **DOWNGRADED** | 19 | 0 | 15 | 4 | 0 | 8 | 11 | 0 |
| pixel-stack PIXEL-STACK: image-sensor-style group-sensed 3D 1T1C DRAM with an all-oxide source-follower + CDS amp tier every 16 cell tiers | **DOWNGRADED** | 18 | 0 | 10 | 8 | 0 | 8 | 10 | 0 |
| raw-ber-contract RAW-BER CONTRACT | **DOWNGRADED** | 19 | 0 | 14 | 5 | 0 | 10 | 7 | 2 |

## Reviewers' one-line verdicts

| Reviewer | ai-memory-diet | and-stack | cell-wafer-foundry | charge-river | diode-tower | hot-side-memory | lean-array-module | margin-stack | pixel-stack | raw-ber-contract |
|---|---|---|---|---|---|---|---|---|---|---|
| CIRC | Host-lite for human chat is plausible at ~1.4-1.5x, but agent/API traffic needs the host tier, a single shared latent multiplies decode HBM reads ~27x, and only 2 local drives fit per GPU. | Biggest density prize; at realistic IGZO swing (120-160 mV/dec) the -1.5 V write-plate hold leaks 5-40x the 21 aA budget during reads, 2-bit MLC needs a cross-temperature reference scheme, and the bonded current-mode SA forces 8-16:1 muxing. | Bond physics is a fair first experiment, but wordlines through n-only oxide predecode with a negative hold are an analog problem, and the 26 mV threshold is booked without its 15.6% parity or global-line coupling. | CTE is the right binary test, but the design hides an amp tier at every hole end and has no regeneration return path in a straight hole; a buffer plus reverse lap doubles latency and plate wear. | Diode barrier aside, the 7 mV gain-FET residual is half the portfolio's own oxide-SF estimate (which caps the back-wall tower below parity), V_f cancels only isothermally, and plate drivers vs plate RC are unpriced. | Energy win survives any reasonable correction, but 64-cell subarrays imply impossible driver/SA density in the carrier, 2-bit MLC ignores ~17 mV/K cross-temperature shift, and the 190 W needs the 16-tier x 2-bit capacity case. | A sound hedge on helium, but H2 leak-in into oxide-channel chambers conflicts with the portfolio's tight hydrogen budgets, and the AAO 'parity' capacitor assumes an AR-400 three-layer fill. | Circuit idea sound and 0.5 fF plausible, but the global CDS comparator does not fit a 29 nm column, the BCH parity turns 'flat' $/bit into +6-13%, and the 22FDX emulation cannot measure alpha or oxide RTN, the two terms that decide Cs. | CDS-in-oxide argument holds in principle, but one auto-zeroed comparator per 0.7-5.6 um2 does not fit the base wafer, and the RTN input (3x instead of ~9x q/CoxWL) hides a residual near the NO-GO line. | Error-physics study is cheap and decisive, but the flag circuit cannot resolve a 3.6 mV window under SA strobe skew, flags have no pins or check bits to ride on, and the 15x headline gives up chipkill and ignores self-refresh. |
| DEV | No device physics blocks it; flash write amplification and end-of-life throughput are the physical risks, and the energy claim is overstated for LPDDR5X hosts. | Biggest prize, least-closed device physics: write half-select on shared write plates, Vt-tail cutoff and IPD read disturb each force redesign-scale changes, and the planar 64-cell emulation tests none of them. | The bond physics is credible engineering; the device risk is bond-interface hydrogen reaching the top tier and the selector/predecode TFTs, and the rest inherits the cells' risk. | The decisive test is cheap, but the buried-channel lever cannot work at 4.5e12 cm^-2 in a few-nm film and oxide-SF RTN at a 5e-10 BER eats the eye; P ~10-20% unless imec's 98% turns out to be end-to-end. | Least likely cell: the only >=1.0 eV contact class (AgOx) decomposes inside the thermal budget, and the bottom-anode geometry plus trap-assisted leakage widen a gap already 0.15-0.2 eV; P ~10-15%, cheap to kill, keep it as a coupon side-bet. | The energy case is robust at 1 b; the 2-b capacity claim fails on the dossier's own arithmetic if write-FET sigma_Vt >30 mV or read-FET RTN is uncontrolled, and bond-interface hydrogen must move into Gate A. | A real hedge with overstated plausibility: rotational accommodation pulls the H2 prior to the GO line, the H2 leak-in conflicts with an oxide-cell portfolio, and AAO trades an AR-60 etch for AR-110-130 ALD plus an unsolved barrier opening. | Sound physics and the right keystone, but the 10x cut rests on an underived IGZO 1e-10 leakage tail, an unsupported 25 uS oxide gain FET and a Gaussian RTN budget; plan for ~1-1.5 fF (3-5x) until oxide-native ns-CDS and >=1e6-cell tail data exist. | A credible CDS argument, but RTN tails in 0.01 um^2 oxide followers and a sigma-30-mV retention assumption put 0.45 fF in the conditional band; the <=1 fF fallback (~4-5x) is the honest planning case. | Coding arithmetic is solid; the device measurement is not, because the reduced-tRCD flag proxy samples the wrong error population and DDR4 raw data cannot set a DDR5 refresh interval. |
| IND | A useful systems paper, not a company or a step change: 1.19x in wafer terms without the prior-art latent, IP that needs a client and a server the startup does not control, and NVIDIA's platform moving toward more host memory. | Biggest prize, but ~3 years behind NEO's NAND-process DRAM (PoC April 2026, no licensee yet), inside Macronix's 3D AND pillar estate, and its 3.8x bits/$ is measured against 2026 1-beta; the planar seed proves select coupling, not manufacturability. | The split is anticipated and already done in-house, the open spec earns nothing, the merchant market has neither buyer nor seller, and the seed funds no bond physics; it lives only as the scale path of a cell that wins. | Boldest and cheapest to kill, but imec owns the direction and its partners own the route to market, and a 2x-cheaper, streaming-only tier is squeezed between HBF and DRAM, the Optane trap. | A materials search with a 0.15-0.3 eV gap, exposed to obviousness (Kepler 1T-nC plus diode-access 1D1C, US 2007/0183191), and the smallest density step of the three oxide 3D cells; lowest priority for capital. | Cleanest energy story in the set, but TSMC/Intel own the slot, the ~190 W/GPU is ~2x high on traffic share and quoted against a front-side-power product, and the seed tests none of the foundry-only risks; it needs a named backside-power partner before a raise. | A real tail-risk hedge with nothing to own: H2 backside gas is already in the patent record, the lever is ~3% of DRAM helium ($0.32/wafer), and the OEMs would capture any value; a grant-funded or OEM-internal project, not a venture. | Best physics-to-risk ratio and the portfolio's reader chip, but no $/bit or density step and a thin patent position (IBM micro-SA + OCSA + Hi-ECC); fund it as a portfolio tool, not a licensing company, until a memory maker says capacitor-module deletion is worth paying for. | Credible read physics, but its bits/$ is the 0.998 tier-yield input restated, the Smart-Cut baseline is a strawman against incumbents' bonded-periphery 3D DRAM, and the patent estate around it is crowded. | Sound engineering, weak business: $2.60 of value per module, replicable in firmware by CXL controller incumbents, with the only novel claim on its least valuable feature (flags, ~8% of parity). |
| PROC | A software lever with a real but small effect of its own (~1.2x wafer-eq). Once the NAND it buys is counted against a DGX-class baseline, it may raise fab wafer starts and resources per rack. | Biggest prize, least-closed integration. No process sequence yet gives ring-to-film write contact plus read isolation in one hole, the stack is ~320 mixed sublayers, and the 22 nm twin pillars are unbuildable. The realistic case is the coaxial fallback at ~1.5-2.5x bits/$. | Bond physics is testable, but anisotropic warp, AR-110 isolation at 80 nm pitch and cross-fab contamination make the merchant split costlier than modelled. It lives or dies with a passing cell and a neutral bond fab. | The planar CTE test is cheap and worth running, but the vertical product as drawn does not close: gate-first 5 um of W, AR-80 holes, AR-130 per-row slits, no staircase and two-ended sensing. Realistic density is ~2x 1-beta at near-DDR5 cost. | An elegant cell whose best-barrier anodes (AgOx/PtOx) cannot survive 400 C or be etched back in a hole, and whose top-of-pillar 3T+2BL wiring is unpriced. The coupons must use etched, integrable anodes. | The best energy idea in the set, but logic-fab realities gate it: carrier-induced backside overlay distortion, bond voids and In/Ga/Zn contamination must be shown harmless to $30k wafers, and honest carrier cost is ~$2.3-4/GB, not $1.36. | H2 backside cooling is a sound, testable hedge if edge-local H effects are measured. The PFAS and AAO claims are weaker than stated: the portfolio's 3D cells bring deep etches back, and AAO cannot register to pads. | Sound physics and cheapest to test, but the 'same-step 3T amp, +1 DUV mask' needs 3-4 critical (EUV-class) levels, and the MPW cannot measure the coupling that sets Cs. Expect a capex/PFAS win with a ~10% $/bit loss. | Credible read physics, but four sequential decks plus amp tiers price at Smart-Cut parity (~0.67x), and the SiNx-capped SF works against the hydrogen retention budget. | The coding math is sound, but manufacturability depends on vendor screens and sort/repair flows the plan never touches, and the DDR4 experiment measures cells 2-3 generations old. |

## ai-memory-diet — AI MEMORY DIET (ai-memory-diet)

**Final status after red team: DOWNGRADED.** No physics kill. Host-lite survives: for human-chat traffic it holds p99 <=0.30 s at 3.5 Gen5 drive-eq/GPU (5.0 at end of life with throttling) and stays at 1.50x on MLA/hybrid re-runs. But the gains shrink. Full-KV-path accounting gives 1.40x DRAM GB per human-chat conversation (1.17x wafer-eq). Agent/API traffic genuinely needs host DRAM, so the fleet gain is ~1.17x at 50% agent capacity. The single all-layer latent is killed (26.7x decode reads), the per-layer latent is prior art and compute-bound, the client signal saves flash not DRAM, and the diet is ~neutral on total wafer starts. S 2 -> 1, EV 30 -> 15.

*Revised verdicts* — Possible: Yes for host-lite (gap-aware tiering): no device physics; flash bandwidth, NAND endurance (WAF ~1.1 with FDP) and p99 restore fit 3.5 Gen5 drive-eq/GPU fresh and 5.0 at end of life for 70B GQA human chat, <=2 local drives for MLA models. No for the single all-layer latent (26.7x more decode KV reads than GQA). · Profitable: STEP CHANGE IF IT WORKS: No. Axis: DRAM bits per served AI chat user. Factor 1.40x fewer DRAM GB per human-chat conversation (1.17x wafer-eq) with full KV-path DRAM, 1.24x at a 120 GB host floor, ~1.17x fleet-wide at 50% agent/API capacity; S = 1 (was 4.5x headline with the latent). · Doable by this founder: PROVABLE WITH $1M: partly. Yes for the technical claim: ~$205k external, an 8-GPU replay of measured human + agent traces with FDP and pre-cycled drives, a 35 °C soak and one MLA-class model settle host-lite by M12. No for 'bits not bought', which needs NVIDIA or a hyperscaler to ship host-lite pool SKUs.

### RT-CIRC-ai-memory-diet-01 — MAJOR — CIRC — §2.2 scenarios (human-chat gap model) / §4 #7 agents 'not modeled'

> Agent and API traffic is exactly where the host tier earns its keep. The model's ~240 GB/GPU host tier holds a conversation for ~9 s. Agentic and API turns wait 1-10 s on tool calls, have no typing signal, and in 2026 carry a large and growing share of served tokens. For that traffic the host tier's hit rate would be high, not 5%. Host-lite forces those turns to flash or recompute, and the p99 TTFT gate on human chat traces never sees them.

*What would change the reviewer's mind:* The replay testbed includes an agent and API trace mix at a realistic share, and host-lite still meets p99 TTFT <=0.30 s.

**Response — ACCEPTED-DOWNGRADE:** Valid, and the biggest correction. The model now includes an agent/API class (model 11.6, all ESTIMATE): tool-wait gaps log-normal with a 3 s median (sigma 1.2), 4 s steps, a 24k median context (5.3 GB at 70B GQA FP8) and no client signal. Today's 240 GB host tier catches 84-90% of agent returns but only ~5% of human-chat returns. Two fixes were tested. (a) Host-lite with agents restored from flash on arrival keeps the 1.50x figure, but agent p99 is 0.66-1.02 s at 3-5 drive-eq. Holding agent p99 <=0.30 s needs 5.8-7.3 drive-eq/GPU, beyond 2 local bays plus a shelf drive (today's mixed node: 0.22 s). (b) Gap-aware tiering: human-chat KV bypasses the host, and a host tier is kept just large enough that agents keep today's hold time. It needs 103/143/187/240 GB/GPU at 25/50/75/100% agent share, and holds agent p99 0.13-0.26 s and human p99 0.18-0.32 s. The DRAM gain falls with agent share: 1.35x/1.22x/1.11x/1.00x on HBM + host, and fleet-wide 1.28x/1.17x/1.08x at 25/50/75% agent capacity with full-path DRAM. OpenRouter agentic tokens grew ~14x in Feb-Aug 2026 against 2.8x for human use (secondary source), so the agent share is large and rising.

*Action taken:* Adopt gap-aware tiering. The concept becomes a human-chat-pool design. G2 replays measured human + agent mixes and gates agent p99 as well as human p99. The step-change claim is restated as a function of human-chat share. Server-side tool-latency deadlines are added as an untested workaround.

### RT-CIRC-ai-memory-diet-02 — MAJOR — CIRC — §2.2 scenario D / §5 step 4 latent gate (RULER only) / §4 #2

> A single latent shared by all layers multiplies decode HBM traffic. GQA FP8 reads 2 KiB per token per layer. A latent shared across all 80 layers at 3x compression is ~53 KiB per token, and each layer must read all of it, even with MLA-style weight absorption. Per decode step that is ~80/3 = ~27x more KV read bandwidth: for a 32k context, ~139 GB per step versus 5.2 GB, unless it is held on-chip, which 1.75 GB per sequence cannot be. Decode is HBM-bandwidth-bound, so D's 'equal tokens/s' cannot hold. The latent gate measures only RULER accuracy.

*What would change the reviewer's mind:* A latent design (for example layer-group latents) whose per-step HBM read bytes are <= GQA FP8, and a latent gate that adds decode tokens/s at batch on the 8-GPU node.

**Response — ACCEPTED-KILL:** Correct physics. With a latent shared by g layers at 3x capacity compression, each layer reads its group's whole latent, so per-step reads are GQA x g/3. Model 11.1 gives: g=80 reads 140 GB per step for one 32k session versus 5.2 GB for GQA FP8; HBM bandwidth allows ~3 active sessions/GPU versus 89; DRAM per conversation is 0.06x of today. MLA-style weight absorption does not help, because every layer still reads the full shared latent. So the single all-layer latent leg (I-04878 as written) is killed. Only g <= 3 avoids raising reads, and g = 1 (per-layer) is MHA2MLA/TransMLA prior art. The owner also found a second correction: with a compute bound added (5 PF FP8 x 0.4 MFU, decode plus prompt prefill), a 70B dense model caps at ~143 active sessions/GPU. Even a per-layer 3x latent therefore buys 1.62x active sessions, not 3x. D0 falls from 4.50x/3.57x to 2.43x/1.93x, and the latent is not the diet's own lever.

*Action taken:* Kill the single all-layer latent and the I-04878 IP claim. latent_group_layers 80 -> 1 and a compute bound go into the model. G3 is replaced by G3': a decode-tokens/s-at-batch plus RULER check of prior-art per-layer retrofits, $15k, adopt or drop.

### RT-CIRC-ai-memory-diet-03 — MAJOR — CIRC — §2.4 drives (3 x 15.36 TB per GPU) / §4 #4 'local bays ~2 per GPU [UNVERIFIED-PK]'

> The flash slots and the DRAM in the storage path do not add up. GB300 NVL72 compute trays expose 8 E1.S bays per 4-GPU tray (Cudo, Gigabyte, HPE specs; logged in rt-CIRC), with 15 TB the largest listed E1.S. That is <=2 local drives per GPU, so the 3rd drive-equivalent (~7 GB/s per GPU) must come over the scale-out NIC from pod shelves that carry their own server and BlueField DRAM. Enterprise TLC SSDs also carry ~1 GB of FTL DRAM per TB, ~46 GB across 3 x 15.36 TB per GPU, against the 176 GB/GPU freed. The 'DRAM GB per conversation' metric counts none of this. Including SSD DRAM alone moves 1.50x to ~1.44x, and shelf-server DRAM lowers it further.

*What would change the reviewer's mind:* A bill of DRAM across the full KV path (host, SSD controllers, storage servers and DPUs) for A and B0, with B0 still >=1.4x.

**Response — ACCEPTED-MITIGATED:** Valid accounting gap; the conclusion survives. Model 11.2 bills DRAM across the whole KV path: 2 local E1.S per GPU (8 per 4-GPU tray), the third and later drive-eq on a pod shelf at ~10 GB of head/DPU DRAM per drive [UNVERIFIED-PK], and SSD FTL DRAM at 1 GB/TB. B0 vs A moves from 1.50x to 1.44x with FTL, 1.43x with the shelf, and 1.40x with flash sized for p99 (A 3.3, B0 3.5 drive-eq). In wafer terms it is 1.17x. KV chunks are ~40 MB sequential appends that expire in bulk, so large-indirection-unit (64 KiB) or ZNS drives cut FTL DRAM 16x and give 1.47x. MLA-class models need <=1 drive-eq (model 11.7), which fits the local bays with no shelf: 1.50x. At the critic's 120 GB host floor the ratio is 1.24x.

*Action taken:* Report full-KV-path DRAM as the headline metric and specify large-IU or ZNS FDP drives. G0/G2 measure host RSS + SSD controller DRAM + shelf heads. Kill 7R fires if the full-path ratio is <1.25x.

### RT-DEV-ai-memory-diet-01 — MAJOR — DEV — §2.4 endurance (2.33 DWPD on 3-DWPD drives; model INPUT spill_frac 1.0, no write-amplification term); GO 2

> Endurance is sized on host writes with an implicit write amplification of 1. KV chunks expire on mixed timelines (12% never return, 1 h retention, per-session TTLs), so without FDP or ZNS placement the flash translation layer garbage-collects partly valid blocks, and typical WAF is ~1.3-2.0. That puts NAND wear at ~3.0-4.7 DWPD-equivalent against a 3 DWPD rating, and endurance, not bandwidth, becomes the binding drive count. GO 2 ('<=3 DWPD by SMART') passes if it reads host writes and fails if it reads NAND writes.

*What would change the reviewer's mind:* Rig data reporting NAND-side writes (vendor log page) with measured WAF <=1.25 under replayed expiry patterns, or FDP-enabled drives in the bill of materials with their WAF measured.

**Response — ACCEPTED-MITIGATED:** Valid. The model now applies WAF to NAND-side writes and DWPD (model 11.3). B0 on 3 x 15.36 TB is 2.71 NAND DWPD at WAF 1.0, 2.98 at 1.1, 3.52 at 1.3, 4.06 at 1.5 and 5.41 at 2.0, so without placement control endurance sets the drive count at 3.5-5.4 drive-eq. KV is close to the ideal FDP workload: chunks are appended, never overwritten, and expire on known TTL buckets. Placing chunks into reclaim units by expiry class lets whole units die together. Samsung/Meta's CacheLib+FDP work reached device WAF ~1 on production Meta and Twitter traces (arXiv 2503.11665, logged). The base case is WAF 1.1, giving 2.98 DWPD on 3 drives, or 2.55 at the p99-sized 3.5 drives. The 12% of chunks that never return can be gated out of spill.

*Action taken:* waf 1.0 -> 1.1 in the model. The BOM specifies FDP-capable drives. GO 2 now reads NAND-side writes (vendor/OCP log page) and requires WAF <=1.25 under replayed expiry patterns.

### RT-IND-ai-memory-diet-01 — MAJOR — IND — §3 Genuine delta #1 (client-deadline restore); §6 IP ('No search has been run'); §7 NVIDIA 'likeliest partner or acquirer'

> The strongest IP, client-deadline restore, needs both the client and the server. Chat operators (OpenAI, Anthropic, Google, Meta) own both and could ship a typing/send hint in weeks. NVIDIA owns the server-side KV stack (Dynamo/KVBM, NIXL, ICMS on BlueField-4). Prior art for prefetch on user intent (speculation rules, hover prefetch, LiveMind 2024, CachedAttention 2024) makes a broad claim obvious, and no FTO search has been run. The startup controls no deployment surface.

*What would change the reviewer's mind:* An inference provider or chat operator agreeing to run the hint and queue in production under licence. Or an FTO opinion showing the deadline-queue claim survives LiveMind and CachedAttention.

**Response — ACCEPTED-DOWNGRADE:** Valid on defensibility. The mission does not kill for business reasons, but it does lower what the leg is worth. The model already showed the client signal saves flash, not DRAM: 1.2 drive-eq/GPU at the base mix (2.3 vs 3.5) and up to 4.7 at 128k FP8. Model 11.7 adds that for MLA-class models restores take tens of ms (B0 p99 0.05 s on 2 local drives), so the signal is moot there. Operators who own client and server can build it, and LiveMind, CachedAttention and speculation rules narrow any claim. The 'strongest IP' becomes an optional efficiency feature, best offered as an open API field.

*Action taken:* Demote the client-deadline restore to optional (G1 optional; the lead-time study is cut from $45k to $15k). Run the FTO search ($20k) at M0-M1, before any filing. File only if the deadline-queue claim survives LiveMind and CachedAttention; otherwise publish defensively and propose a 'prefetch hint' field to the OpenAI-compatible API. Pursue a production pilot through an inference provider.

### RT-IND-ai-memory-diet-02 — MAJOR — IND — §0 Step change; §2.2 Scenario table (B0 1.50x DRAM / 1.19x wafer); §2.3 Rack and fleet

> The diet's own contribution is 1.50x less DRAM per conversation, or 1.19x in wafer terms. The 3x latent that lifts this to 4.5x is mostly prior art (MLA, MHA2MLA, xKV). Freed DRAM is worth $18.8k per rack at cost, against a GB300 NVL72 rack priced in the millions [training knowledge]. 10,000 racks avoid 0.13-0.19% of world DDR5-equivalent output. On the mission's axes that is S = 2 at best, and it is not a step change in DRAM bits per user unless the unshown retrofit latent works.

*What would change the reviewer's mind:* G3 showing a retrofit all-layer latent at >=3x with <=1 point RULER loss on a 70B model, plus a production measurement of host-DRAM working set <=64 GB/GPU.

**Response — ACCEPTED-DOWNGRADE:** Accepted, and the re-runs lower it further. The diet's own lever is 1.40x DRAM GB per human-chat conversation with full-path DRAM and p99-sized flash, or 1.17x in wafer terms (model 11.2/11.9). It is 1.24x/1.11x at a 120 GB host floor and ~1.17x fleet-wide at 50% agent capacity. The latent no longer lifts this: the all-layer version is killed, and a per-layer latent is prior art and compute-bound at 1.62x active sessions, so D0 is 2.43x, not 4.5x. Freed DRAM at cost is still ~$19k per rack, and 10,000 racks avoid 0.13-0.19% of world DDR5-equivalent output. On the mission axis this is S = 1, not a step change.

*Action taken:* Revised step-change claim: ~1.4x DRAM GB (1.17x wafer-eq) per human-chat conversation, scaling with chat share; S 2 -> 1, EV 30 -> 15. The latent is no longer counted. G2 measures the full-path ratio directly.

### RT-IND-ai-memory-diet-03 — MAJOR — IND — §4 #5 (soldered or busy host DRAM; Vera ~1.5 TB/CPU); §7 OEMs/ODMs

> GB300's host DRAM is Grace's soldered LPDDR5X (480 GB per Grace), and the next platform goes the other way: Vera with ~1.5 TB per CPU, per the dossier. NVIDIA's ICMS already puts KV on pod-level flash. Depopulation is a decision in NVIDIA's reference design, not an OEM SKU choice, and NVIDIA's roadmap is adding host memory for context. Without NVIDIA, 'publish the node spec' has no adopter.

*What would change the reviewer's mind:* NVIDIA, or a hyperscaler custom-ASIC team (TPU, Trainium, MTIA), committing to a host-lite SKU. Or measured evidence that Vera's extra memory sits idle in serving.

**Response — ACCEPTED-DOWNGRADE:** Valid on adoption, and the owner's own agent run partly supports NVIDIA's direction. Agent-heavy pools do use host DRAM (84-90% of agent returns hit it), and an agent-only node keeps ~240 GB/GPU under gap-aware tiering. Extra host memory on Vera is a poor use of bits only for human-chat traffic. There the model gives a 750 GB/GPU tier serving 25% of returns and 2 TB serving 55% at 4.4x the DRAM per conversation; MLA-class models serve 23% from a 240 GB host tier. Vera's LPDDR5X is reported to sit on SOCAMM modules [UNVERIFIED-PK], which would make depopulation a module-population choice rather than a board respin. But the reference design is NVIDIA's call. The $1M can produce the measurement IND asks for: host-tier utilisation versus size on mixed traces, at 240/750/1,500 GB. It cannot produce adoption.

*Action taken:* Add a host-size sweep on mixed traces to G2 as the 'is Vera's memory idle in serving?' measurement. Target hyperscaler custom-ASIC teams (TPU, Trainium, MTIA), who own their host configs, and inference providers who can segregate chat pools. The 'bits not bought' claim stays unprovable with $1M.

### RT-IND-ai-memory-diet-04 — MAJOR — IND — §2.1 KV geometry (70B GQA, 160 KiB/token FP8); §3 Latent KV row

> The baseline is a 70B GQA model with 160 KiB/token of FP8 KV. Frontier serving is moving to MLA models (DeepSeek-V3/R1, Kimi K2) and hybrid linear-attention models (Qwen3-Next, Kimi Linear, MiniMax), whose KV per token is several-fold smaller from pretraining [training knowledge]. That shrinks scenario A's host and flash load, removes the need for a retrofit latent, and eases the restore-time problem the client signal exists to solve. G2 and G3 may be moot by 2028.

*What would change the reviewer's mind:* The model re-run on an MLA/hybrid-attention traffic mix and still showing >=1.5x DRAM per conversation from host-lite, plus a material p99 benefit from the signal.

**Response — ACCEPTED-MITIGATED:** Partly valid; the core claim survives the re-run. Model 11.7 re-runs the model on a DeepSeek-V3-class MLA model (34.3 KiB/token, 37B active, 84 GB/GPU weights) and a Qwen3-Next-class hybrid (12 KiB/token plus ~40 MB recurrent state per session). Host-lite's DRAM ratio is set by how long a host tier can hold a session against human gaps, not by bytes per token, so B0 vs A stays 1.50x on HBM + host for both. MLA is compute-bound at ~84 active sessions/GPU and leaves ~136 GB of HBM idle to hold idle KV. Host-lite then needs ~0.6 drive-eq/GPU, fitting 2 local bays with no shelf, with B0 p99 0.05 s, so the client signal and the latent are moot. The hybrid is HBM-bound, with flash reads of 16 GB/s per GPU and B0 p99 0.14 s on 2 drives. Rewriting its state every turn drives 402 TB/day, ~9.6 drive-eq at 3 DWPD, for today's flash tier as much as for host-lite. So IND is right that G3 and the signal are likely moot by 2028; host-lite is not.

*Action taken:* Re-baseline the plan on an MLA-class model plus GQA and add G2b: MLA host-lite with <=2 local drives. Drop the retrofit-latent research. Flag hybrid-state endurance as kill 9: test FP8 state, selective spill and high-endurance flash.

### RT-PROC-ai-memory-diet-01 — MAJOR — PROC — §2.4 'The diet adds ~0 flash against 2026 practice'; model INPUT ssd_per_gpu=3 for both baseline and diet; §8 resources

> The endurance constraint alone (107 TB/day per GPU at 3 DWPD) forces >=36 TB of TLC per GPU, and the plan buys 3 x 15.36 TB = 46 TB. NVIDIA's own DGX B200 ships 8 x 3.84 TB NVMe per 8 GPUs: ~3.84 TB per GPU, ~0.25 drive-equivalents in capacity and ~0.5-1 in bandwidth. Against that baseline, the diet adds ~32-42 TB of NAND per GPU, ~2.3-3.0 PB per NVL72 rack, or ~16-30 NAND wafers at ~100-140 TB per wafer. That buys 12.7 TB of freed DRAM, ~4 DRAM wafers. Fab wafer starts, kWh and water per rack therefore go up, not down, in a year when the dossier itself reports enterprise SSD prices up 2.3-2.8x.

*What would change the reviewer's mind:* Fleet data showing that 2026 inference racks already carry >=3 Gen5 drive-equivalents per GPU of >=3 DWPD flash for KV tiering (ICMS/LMCache deployments), so the diet's flash is truly not incremental.

**Response — ACCEPTED-DOWNGRADE:** Valid per rack; wrong per served conversation; and the diet's own resource benefit turns out to be ~neutral. Model 11.8 adds the DGX-class baseline: 240 GB host, 3.84 TB/GPU NVMe not used for KV, misses recomputed. Recompute FLOPs cap it at ~18 active and ~378 conversations per GPU, against 1,820 with a flash tier, and a miss costs ~1.0 s mean and ~10 s p99 TTFT. Per rack, 3 drive-eq/GPU add ~25 NAND wafers against ~4.1 DRAM wafer-eq freed, as PROC says. Per 1,000 conversations, total wafer starts are 1.037 (DGX-class) vs 0.427 (A, p99-sized) vs 0.411 (B0), and fab kWh 1,337 vs 552 vs 533. That 2.5x credit belongs to the flash tier (ICMS/LMCache, prior art), not to the diet. The diet's own increment over A is ~1.04x in total DRAM + NAND wafer starts. No fleet data was found showing 2026 racks already carry >=3 drive-eq/GPU of KV flash; NVIDIA's ICMS has no per-GPU figure in the snippets.

*Action taken:* Withdraw the resource-intensity claim; the diet is ~neutral on DRAM+NAND wafer starts versus A. Report three baselines (DGX no-flash, A flash tier, B0) with total wafer starts per 1,000 conversations. Claim only DRAM bits, and state that the 2026 baseline's flash is assumed, not shown.

### RT-PROC-ai-memory-diet-02 — MAJOR — PROC — §0 STEP CHANGE (1.50x DRAM, 1.19x wafer-eq); FINAL_CONCEPTS S=2

> On FINAL_CONCEPTS' own scale, S=2 means ~1.3-2x and S=1 means <=1.3x. The diet's own lever is 1.19x in wafer terms (1.29x DRAM at the critic's 22%), and the client-signal variant B gives 1.02x. The 3x comes from a latent that is model research in a crowded prior-art field, not a memory change. Scored on what the diet itself does, S is 1 and EV is 15, not 30.

*What would change the reviewer's mind:* Measured traces in which host-lite alone gives >=1.3x fewer wafer-equivalent DRAM GB per served conversation at equal p99.

**Response — ACCEPTED-DOWNGRADE:** Accepted. On FINAL_CONCEPTS' scale, the diet's own lever in wafer terms is 1.17x after full-path accounting (1.19x before), 1.11x at a 120 GB floor, and ~1.1x fleet-wide at 50% agent capacity. The client-signal variant B is 1.02x. The latent is no longer counted (all-layer killed; per-layer prior art and compute-bound). So S = 1 and EV = 15. The would-change-my-mind test (host-lite alone >=1.3x wafer-eq on measured traces) cannot be met. Deleting host DRAM entirely caps the wafer-eq gain at (288x3+240)/(288x3) = 1.28x, so S = 1 is structural. S = 2 would need a lever on HBM per conversation, such as chat-pool SKUs with less HBM on compute-bound MLA nodes, where ~136 GB/GPU of HBM sits idle (model 11.7) [SPECULATIVE].

*Action taken:* Rescore S 2 -> 1, EV 30 -> 15 in sections 0 and 11; FINAL STATUS DOWNGRADED. G2 still measures the wafer-eq ratio.

### RT-CIRC-ai-memory-diet-04 — MINOR — CIRC — §2.5 p99 model (M/M/1 at rho<=0.6, reads only) / §4 #8

> The p99 restore model queues reads only. Each GPU writes ~1.2-1.45 GB/s continuously at 2.33 DWPD. NAND program and erase operations (ms-scale) block reads on the same die, and garbage collection under mixed load adds write amplification above 1. That threatens both the p99 and the 3 DWPD gate unless FDP/ZNS placement keeps write amplification ~1.

*What would change the reviewer's mind:* Rig measurements of p99 restore latency and write amplification under the full read-plus-write mix.

**Response — ACCEPTED-MITIGATED:** Valid. The flash queue now adds NAND program/erase die-time: host writes x WAF / (10 GB/s sustained write per drive), with no program-suspend credit (write_interf 1.0, conservative). At 3 drive-eq this adds ~0.05 to flash utilisation. B0 p99 goes from 0.33 to 0.38 s and B from 0.11 to 0.13 s; drive-eq for p99 <=0.30 s goes from 3.2 to 3.5 (B0) and 2.2 to 2.3 (B). At WAF 2.0 the figures are 3.6 and 2.4 (model 11.4). Write amplification is handled by FDP placement (RT-DEV-01).

*Action taken:* Interference is in the model. Specify drives with program/erase suspend and FDP. G2 records p99 and NAND-side WAF under the full replayed read-plus-write mix.

### RT-DEV-ai-memory-diet-02 — MINOR — DEV — §2.4 bandwidth sizing (14 GB/s per drive at rho <=0.6) over drive life

> As NAND nears its P/E rating, raw BER rises and controllers fall back to read-retry and soft LDPC decoding, which cuts sustained read throughput. Fresh KV data (<=1 h) limits retention-driven retries, but wear-driven program noise still grows. The p99 gate is tested on new drives, while the design runs at rho ~0.5-0.6 with no end-of-life margin.

*What would change the reviewer's mind:* Restore throughput and p99 measured on drives pre-cycled to >=80% of rated endurance.

**Response — ACCEPTED-MITIGATED:** Valid. KV data lives <=1 h, so retention errors are negligible, but wear-driven raw BER and read-retry do rise. With a 0.85 end-of-life read derate [ESTIMATE], B0 p99 at 3 drive-eq goes from 0.39 to 0.53 s and needs 4.2 drive-eq (B: 2.7). Combined with one throttled drive it needs 5.0 (B: 3.3) (model 11.4). That is ~1.5 extra drive-eq of flash, not DRAM. Pre-cycling a new 15.36 TB drive to 80% of 3 DWPD x 5 years takes ~67 PB of writes, or months. Used enterprise drives at a known SMART 'percentage used' of 70-90% are cheap and immediate.

*Action taken:* Add a pre-cycled arm (4 used drives at >=80% rated wear, ~$3k) to the wear rig. The G2 PASS line includes p99 on pre-cycled drives at <=5 drive-eq.

### RT-DEV-ai-memory-diet-03 — MINOR — DEV — §8 energy in use ('~1.9 kW per rack at 0.15 W/GB')

> 0.15 W/GB is a DDR5-RDIMM-class figure, but this rack's host memory is LPDDR5X on Grace, whose background power per GB is several times lower [training knowledge]. Freed host DRAM probably saves ~0.3-0.6 kW per rack, not 1.9 kW. At ~15-25 W per Gen5 drive under mixed load, 216 drive-equivalents draw ~3.2-5.4 kW. The diet costs energy against a no-flash design, and saves little against the 2026 flash-tier baseline.

*What would change the reviewer's mind:* Measured per-GB LPDDR5X power on a GB300 tray under serving load.

**Response — ACCEPTED-DOWNGRADE:** Valid. GB300 host memory is LPDDR5X; at ~0.04 W/GB (0.03-0.05, UNVERIFIED-PK) the freed 12.7 TB per rack saves 0.38-0.63 kW, not 1.9 kW. 216 drives at 15-25 W draw 3.2-5.4 kW. Against a flash-tier baseline with the same drives, the net saving is ~0.4-0.6 kW per rack, well under 1% of a ~130 kW rack. Against a DGX-class rack with one drive per GPU, the diet adds ~1.5-3.2 kW, though that rack serves ~4.8x fewer conversations per GPU (model 11.5, 11.8). Energy was never the step-change axis, but the dossier overstated it ~4x.

*Action taken:* dram_w_per_gb 0.15 -> 0.04 in the model; the section 8 energy claim is restated. Measure LPDDR5X W/GB under serving load during the GB200/GB300 tray week, with TACC Vista GH200 as a cross-check.

### RT-DEV-ai-memory-diet-04 — MINOR — DEV — §4 #4 flash slots and pod shelves; M/M/1 queue in §2.5

> Gen5 E1.S and U.2 drives throttle at roughly 70-80 C composite temperature, and dense flash shelves beside liquid-cooled GPU racks are often air-cooled. A throttled drive can lose about half its bandwidth, which at rho 0.5-0.6 sets the p99 directly. Throttling and read/write interference (program/erase busy time on shared dies) are both outside the M/M/1 model.

*What would change the reviewer's mind:* A 24 h soak on the replay node at rack-representative inlet temperature, with drive temperatures logged and p99 held.

**Response — ACCEPTED-MITIGATED:** Valid. With one of three drives throttled to 50% (bandwidth x 5/6), B0 p99 at 3 drive-eq is 0.56 s and needs 4.2 drive-eq; with signal it is 0.19 s at 2.7. With end of life added it needs 5.0, or 3.3 with signal (model 11.4). The deadline queue gives the most tolerance. Throttling is a flash-provisioning and airflow problem, not a DRAM one. The scheduler can also steer urgent restores away from hot drives. MLA-class models use <=1 drive-eq and leave large thermal margin.

*Action taken:* Add a 24 h soak on the replay node at 35 °C inlet with drive temperatures logged. G2 PASS requires p99 held at <=5 drive-eq on pre-cycled drives. Steering by drive temperature goes into the restore queue.

### RT-IND-ai-memory-diet-05 — MINOR — IND — §5 Lead-time study (300-500 users, forked Open WebUI) and replay node (8-GPU H200/B200)

> 300-500 consenting users on a forked UI for 6 weeks will not reproduce production gap and context distributions, or the agent and API traffic that §4 #7 leaves unmodeled. The replay node (one 8-GPU H200/B200) is not the GB300/Vera platform whose host memory is at stake. An operator will treat the result as a hypothesis, not as grounds to change a node spec.

*What would change the reviewer's mind:* Traces from a production partner (LMArena or an inference provider) that cover chat, agent and API traffic.

**Response — ACCEPTED-MITIGATED:** Valid. A 300-500-user forked UI cannot reproduce production gap, context or agent distributions, and one H200/B200 node is not the GB300/Vera platform. The trace problem matters most because agent share is the decisive unknown (RT-CIRC-01), so the revised plan leads with traces. Sources: a production partner under NDA (LMArena or an inference provider), public chat traces (Mooncake, BurstGPT, Qwen-Bailian), and agent trajectories with real tool latencies generated on rented GPUs. A GB200/GB300 tray week ($10k) checks the Grace LPDDR5X path, LPDDR5X W/GB and E1.S thermals. The result is framed as evidence for a pool-level node-spec change, not proof of fleet adoption.

*Action taken:* Traces line $20k, reduced user study $15k (optional), and a GB200/GB300 tray week $10k go into the revised core. G2 runs at measured agent shares.

### RT-PROC-ai-memory-diet-03 — MINOR — PROC — §2.3 rack/fleet 'freed DRAM'; §7 'freed host bits move to HBM'

> The freed host bits are LPDDR5X/SOCAMM. They relieve the HBM shortage only if HBM output is limited by front-end wafers. In 2026 it is gated by TSV, stacking and test: TC bonders, MR-MUF, and base-die and stack yield. LPDDR wafer starts can move to HBM core dies on the same node only as fast as back-end capacity grows. For HBM, 'bits not bought' does not equal 'shortage relieved'.

*What would change the reviewer's mind:* A supply analysis (TrendForce, Yole) showing that front-end wafer starts, not back-end stacking, bind HBM output in 2027-28.

**Response — ACCEPTED-MITIGATED:** Valid. The freed bits are LPDDR5X front-end bits. HBM output in 2026-28 is gated mainly by TSV, stacking, MR-MUF/TC bonding and stack test, so 'bits not bought' does not translate into HBM relief. The 2026 shortage also hit conventional server DRAM and LPDDR, which is where the freed bits land. The bit count per conversation is unchanged; only the shortage narrative moves. No supply analysis was searched (quota).

*Action taken:* Section 7's 'freed host bits move to HBM' is withdrawn and restated as relief for conventional DRAM/LPDDR demand. HBM-per-conversation effects are attributed only to compute-bound or latent effects outside the diet's claim.

## and-stack — AND-STACK: single-etch 3D oxide gain-cell DRAM (revised: two-film notched-write-pocket cell) (and-stack)

**Final status after red team: DOWNGRADED.** The single-film single-etch closure is topologically impossible (RT-PROC-and-stack-01; that leg is killed). The concept survives only as a two-film notched-write-pocket cell whose key modules are unproven (P(closure) ~20%). Revised geometry and cost inputs cut 64 x 2 b from 8.1x density / 3.8x bits/$ to 5.9x / 2.3x vs 2026 1-beta, and ~1.1-1.4x vs projected 2032 incumbents. The cell-physics objections (hold leakage, cutoff, disturb, cross-temperature, half-select) all have numerical fixes, so there is no physics kill. Provability with $1M shrinks to a 2-tier closure coupon at relaxed pitch.

*Revised verdicts* — Possible: YES, conditionally, and only as a two-film cell. The cell physics (oxide 2T0C, floating ring, AND read) breaks no law, but the single-film BL = SL closure is topologically impossible: a ring contact on one wall-lining film always abuts the ring's own read channel. The notched write pocket closes electrically, with ~10 nm of isolation wrapped by the write plate; at a -3.0 V hold the write-FET tail leaks <= 5 aA even at 160 mV/dec, against a 17 aA budget. It still needs unproven modules: a selective IPD opening in the notch, write-film confinement by recess-fill-etch-back, IGZO-safe slit replacement, and twin W-core pillars. · Profitable: Axis: density first. 64 x 2 b = 2.62 Gb/mm2, 5.9x 1-beta (was 8.1x). Bits/$ is 2.3x vs 2026 1-beta at component level (2.2-2.6x across cost cases; was 3.8x), but only ~1.1-1.4x vs a projected 2032 incumbent at first product, or 1.2-1.6x at 96 tiers in two decks. Refresh power is ~25x lower at 1 s, and the array needs no EUV. That is a step change on density and a modest one on cost. · Doable by this founder: PARTLY. About $0.4M by month 14 decides the new crux: a 2-tier vertical closure coupon plus planar statistics (write-FET tails on 1e4 devices, cross-temperature BER, VRT/RTN). The $970k plan adds a 4-tier stack by month 23 and a 32-tier dummy-stack etch coupon. Not provable within $1M: 64-tier manufacturability at 170 nm pitch (twin 28 nm pillars, a 256-layer mixed etch), tier yield and cost. Those need the raise or a NAND partner.

### RT-PROC-and-stack-01 — FATAL — PROC — §4 #2 'Topology closure'; §3 delta 'BL = SL = data writing' (own proposal, unverified); kill #1 (TCAD, month 3)

> The integration sequence does not close as described. Where the ring gates the BL-SL read path, it must be insulated from the IGZO film by the read-gate dielectric (EOT 3 nm). Where the write plate gates the write path, the same ring must contact the same film ohmically. In a single hole the film and the gate dielectric are both conformal ALD liners deposited after the ring etch-back. Opening the dielectric only at each ring's write edge, on all 64 tiers at once, at AR 60, would need a self-aligned, tier-selective removal that no 3D-NAND flow has. The fallback, segmented write and read films, adds two lateral recess/fill modules per tier, each with its own selectivity. Month-3 TCAD can show a short-free electrostatic geometry but not a process that builds it. Without such a flow, the single-etch concept and its 3.8x bits/$ reduce to the coaxial fallback's ~1.56x.

*What would change the reviewer's mind:* A step-by-step flow (every dep/etch/recess with materials and selectivities) that gives ring-to-film write contact and ring-to-film read isolation in one hole. Demonstrate it on a 2-4-tier vertical coupon with FIB/TEM and an electrical write-then-read on >=2 tiers.

**Response — ACCEPTED-KILL:** Accepted, and stronger than stated: the single-film closure is not just unbuildable but topologically impossible. In one axisymmetric hole every plate is a sheet perforated only by holes. The ring, inside its select layer, can therefore reach the film only inside or at the edge of its own band. Any contact there sits directly against the ring's own read channel, with no gated segment between. A read with the ring high then shorts the ring to BL/SL. BL = SL writing removes only the BL-SL current during writes. The single-film BL = SL leg is therefore killed. The concept can revive as a two-film cell, the notched write pocket, built only from lateral recesses, which are self-aligned per tier and local to each hole: (1) stack SiO2 / doped poly-SiGe select plate / SiO2 / SiN write-plate sacrificial layer; (2) etch the holes; (3) recess the SiGe 18 nm, deposit the IPD (1 nm SiO2 + 5 nm HfO2) and a TiN ring, etch the ring back 8 nm behind the wall, then pinch off an Al2O3 plug in front of each ring as a self-aligned read-gate dielectric; (4) notch the SiN 15 nm above each ring with hot H3PO4; (5) open the IPD membrane on the ring top inside the notch, by thermal ALE of HfO2/Al2O3 selective to SiO2; (6) deposit a Ga-rich IGZO write film (4 nm), add a sacrificial pinch-off fill and etch back, leaving the write film only in each notch on the ring top; (7) deposit the In-rich read film on the wall, gated by the ring through the plug and contacting the write-film lips at each notch mouth; (8) form the core and the twin pillars; (9) cut slits, remove the SiN and the notch fill from the back, then deposit an 8 nm write-gate dielectric and an O2-ALD Ru write plate wrapping the notch. Isolation is ~10 nm of write film wrapped by the write plate. Steps 5, 6 and 9 (an IGZO-safe back-side removal) have no precedent [SPECULATIVE]. IMECAS shows a shared-node dual-gate 2T0C over 4 tiers in one integration step, but in a vertical-word-line topology. P(closure) ~20% [ESTIMATE]. If it fails, only the per-tier patterned fallback remains, at ~1.0-1.6x bits/$, and the bits/$ step change dies.

*Action taken:* Kill the named leg: the single-film BL = SL single-etch closure. Re-centre the decisive experiment on a month-14 2-tier vertical closure coupon. GO #1B requires write-then-read on >= 2 tiers, ring hold <= 100 aA and FIB/TEM of the notch contact. Kill single-etch if the coupon has not closed by month 18. Model: wrap 1 -> 0, IPD EOT 2.5 -> 2.0 nm, tier pitch 80 -> 90 nm.

### RT-CIRC-and-stack-01 — MAJOR — CIRC — §2.2 select margin / model 'lowest ring potential -1.09 V', ss_mv_dec_85c 90, v_wp_hold -1.5

> The write-FET hold margin during reads is thin. During any read in a block, the 63 unselected rings are pulled to -1.09 V while the write plates sit at -1.5 V. That leaves each write FET only 0.91 V below Vt. The claimed 10.1 decades (~3 aA from I(Vt) = 39 nA) assumes SS = 90 mV/dec at 85 C, which is an estimate. A published IGZO 2T0C shows 161 mV/dec at 300 K (Frontiers of Physics 2025; logged in rt-CIRC). At 120-160 mV/dec the margin is 5.7-7.6 decades, or ~0.1-0.8 fA. A -3.7 sigma Vt tail (sigma Vt 30-40 mV) costs another 1-1.7 decades. Against a 21 aA budget, any block with more than ~3-20% read duty fails 2-bit retention, a workload-dependent 'read hammer'. The fix is a hold of <=-2.5 V (a >=5 V write-plate swing, with IPD and gate-oxide stress) or a write-plate pull-down synchronised to the select plates.

*What would change the reviewer's mind:* Phase 1 measures write-FET leakage with the ring at -1.1 V and the plate at -1.5 V, at 85 C on >=1e4 devices, with a 1e-4 tail <=5 aA. Alternatively, a bias scheme that keeps the write FET's Vgs <=-1.5 V relative to the ring during reads, with its plate-driver cost.

**Response — ACCEPTED-MITIGATED:** Valid, and worse than stated. The write FET is wide and short: in the redesign it is the write film on the notch floor, W = 2 pi x 60 nm and L ~10 nm, so W/L ~38 and I(Vt) ~3.8 uA, not 39 nA. Model section 11a checks the old -1.5 V hold with the ring parked at -1.30 V and a 1e-4-tail cell (Vt - 3.72 sigma at sigma 40 mV, plus a 0.15 V DIBL penalty). That cell leaks ~1.8 nA at 120 mV/dec, ~1e8 times the 17 aA budget. Three changes fix it. (1) Select plates idle LOW: every ring sits permanently 1.30 V below its stored value, and only the selected tier's plate moves. (2) The write-plate hold goes to -3.0 V, a 5.5 V swing on thick-oxide drivers. (3) A separate 8 nm SiO2/Al2O3 write-gate dielectric carries 3.9 MV/cm in hold and 3.1 MV/cm when writing. The tail cell then leaks 0.0006 aA at 120 mV/dec and 5.1 aA at 160 mV/dec, inside 17 aA. A -2.5 V hold would fail at 160 mV/dec (6.8 fA). I-12627 (two series write gates) was considered and not adopted. It squares the tail probability only if the two devices' defects are independent, which a shared hole film does not give, and it costs a third plate per tier (~40% more stack height). It is kept as an option for 1 b.

*Action taken:* Model: v_wp_hold -1.5 -> -3.0 V and ss 90 -> 120 mV/dec; new section 11a for the write-FET tail. GO #1A adds a write-FET hold-leakage test: 1e-4 tail <= 17 aA at the idle-low bias, on >= 1e4 devices at 85 C. Kill the DRAM-class claim if the tail exceeds 1 fA.

### RT-CIRC-and-stack-02 — MAJOR — CIRC — §2.4 multilevel / §3 'single-bias current-mode MLC read with write-verify at read bias' / §2.10 GO (isothermal)

> MLC reads across temperature are not addressed. Write-verify at the read bias cancels per-cell CR, Vt and kickback only at the write temperature. The ring-gated film's Vt moves ~-17 mV/K (a-IGZO; Chen, IEEE TED 2009). A level written at 85 C and read at 35 C shifts ~0.85 V, most of the 1 V four-level window, and the mobility tempco changes the 298 nA level step as well. Per-page reference cells track only the common mode. A 5% tempco spread is ~40 mV at 50 K, against a 30 mV coupling budget and an 86 mV drift budget. Every GO test is isothermal.

*What would change the reviewer's mind:* Cross-temperature BER (write and read delta T +/-50 K) with in-page references in the Phase 1 emulation, with 2-bit raw BER <=1e-4.

**Response — ACCEPTED-MITIGATED:** Valid: every GO test was isothermal. At -17 mV/K (a-IGZO; Chen, TED 2009) a 50 K gap between write and read shifts Vt by 850 mV. Three fixes. (1) In-page reference cells are written with every page. They remove the common-mode shift and cost 2% parity (model ecc_parity 0.10 -> 0.12). (2) The selected plate's read level tracks temperature through an on-die replica cell (dVt/CR), so cold reads keep their overdrive. (3) The controller forces a refresh of any region whose |T - T_write| exceeds 5 K. Model section 11f puts the residual tempco spread (5% of the shift) at 4.2 mV at the 5 K trigger, 8.5 mV at 10 K and 42.5 mV at 50 K. The trigger is therefore what makes 2 b work; 1 b tolerates the full 50 K with references alone. The extra rewrites cost little, because refresh already runs every ~1 s.

*Action taken:* GO #1A adds a cross-temperature test: 2-b raw BER <= 1e-4 with in-page references at dT +/-10 K, characterised out to +/-50 K. It also adds read-FET Vt(T) from 25 to 110 C. Drop 2 b if the residual exceeds 30 mV at 10 K.

### RT-CIRC-and-stack-03 — MAJOR — CIRC — §2.3 read / model l_local_bl_um 20, SADP top BL 75 nm, 'flash comparators'

> The sense amp does not pitch-match, which costs page bandwidth. The local bitline is 20 um long and runs to a bonded SA on a 75 nm SADP pitch, so each bitline has 1.5 um2 of footprint. The read is a clamped current-mode 2-bit flash (a clamp amplifier, 3 comparators and 3 reference currents), plus BL = SL data-write and verify drivers: ~10-20 um2 at 28 nm. That forces 8-16:1 column muxing. Page read width and the already slow 100 ns, 4-pulse write bandwidth then fall 8-16x. The '~15 ns non-destructive read' holds per bitline, not per page.

*What would change the reviewer's mind:* A bonded-SA floorplan at <=1.5 um2 per bitline, or read and write bandwidth per mm2 with the mux included, compared against DDR5.

**Response — ACCEPTED-MITIGATED:** Valid on page width, not on bandwidth. At the revised 85 nm top-BL pitch, a 20 um local BL has 1.70 um2 of footprint. A ~12 um2 clamped 2-b sense amp plus write driver therefore forces 8:1 muxing (model section 11d). Even so, the array holds ~73,500 SAs per mm2, each delivering 2 b per ~20 ns: ~920 GB/s per mm2 internally. DDR5-class bandwidth per GB at 64 x 2 b density needs only ~1.05 GB/s per mm2, so the headroom is ~880x. Read latency per access stays ~16 ns plus ~2 ns of mux settling. Writes are the slow path: a 2.8 KiB tier-page takes ~7.8 us at 8:1 (0.36 GB/s per block). Write bandwidth must therefore come from many blocks running in parallel behind the controller buffer. Serial (SAR-style) 2-b sensing with one comparator is the fallback if area is short.

*Action taken:* Model section 11d added. The dossier now quotes latency per access, and bandwidth per mm2 with the mux included. Phase 0 includes a bonded-SA floorplan: one SA per 8 BLs of 1.7 um2 each.

### RT-DEV-and-stack-01 — MAJOR — DEV — §1 and §2.3 write (BL = SL = data, one write plate per tier shared by the block); model INPUTS rows_per_select_group=2, n_sel_on_bl=16

> Writes are selected only by plate and pillar driver, and a single-etch write plate is shared by every hole between slits. When write plate k pulses to 2.5 V, every ring on tier k connects through its write FET to its own BL/SL pillars, and an ohmic channel write has no inhibit (unselected rings at 0-1 V see Vgs >=1.5 V). Holes in the 15 unselected select groups on a 16:1 local BL have floating pillars (1.28 fF each, 2.56 fF for BL+SL) that charge-share with a 0.246 fF ring and pull it ~90% of the way to the pillar voltage. Each plate pulse therefore corrupts every non-driven hole on that tier. The planar 64-cell emulation, with its own write electrode per cell, cannot reveal this.

*What would change the reviewer's mind:* A specified write scheme with extracted pillar-to-pillar coupling, e.g. read, precharge and float all 16 groups, then >=3 charge-share pulses to <10 mV error, with the page-write time and energy put in the model; or full-depth slits every select group (2 rows, ~300 nm), with the ~20-33% area penalty carried into §2.1 instead of 15%.

**Response — ACCEPTED-MITIGATED:** Valid, and fatal to the original write scheme. The floating pillars of the 15 unselected groups (2.58 fF) pull a 0.214 fF ring 92% of the way to their voltage (model section 11c). The fix adopted has no area penalty; the page becomes one tier of one block. (1) Read the whole tier-page into the buffer. (2) Raise write plate k and hold it on. (3) Drive the 16 groups in turn through the hole-top selects. Each group's BL, pillars and ring are actively driven, then left floating at their target while the next group is driven. (4) SL pillars float through a new bottom-select plate, so no BL-SL current flows. (5) Drop write plate k and verify. A page is 706 BLs x 16 groups = 11,294 cells (2.8 KiB at 2 b). Four pulse cycles take 1.0 us unmuxed and 7.8 us at 8:1 mux. Writes thus become flash-like page operations behind an SRAM buffer, while reads stay ~16 ns. The alternative of a full-depth slit per group (20-33% area) is rejected.

*Action taken:* Add the sequential-group write scheme and the bottom-select plate. Phase 0 runs SPICE of the 16-group sequence with extracted pillar coupling; error on floated groups must be < 10 mV. The 4-tier stack tests one shared write plate across >= 2 groups. Page-write time is now in the model (section 11c).

### RT-DEV-and-stack-02 — MAJOR — DEV — §2.2 select margin ('142 fA per unselected cell'; model INPUTS guard_v 0.1 V, vt_read 0.5 V)

> The cutoff arithmetic uses nominal Vt with a 0.1 V guard and ignores Vt variation in a 5 nm ALD oxide film lining a 60:1 recessed hole, where thickness and In/Ga/Zn composition drift with depth and the Vt of In-rich films moves of order 0.1 V per nm. At an assumed sigma_Vt of 50 mV over ~8e9 unselected cells per 16Gb die, the 1e-10 low-Vt cell (-318 mV) leaks ~3.5 decades over 142 fA, ~0.48 uA, i.e. 1.6 level steps of the 298 nA 2-b read. Even a 1e-4 cell (-186 mV) leaks ~17 nA, 6% of a level, and that leakage depends on the neighbour's stored level, which write-verify at read bias cannot cancel. The guard must be ~0.3-0.35 V, which raises the swing to ~2.1-2.2 V at CR_min 0.61 and the CR bar from 0.53 to ~0.61-0.63.

*What would change the reviewer's mind:* Measured per-tier sigma_Vt <=30 mV along a >=32-tier hole, or a summed 63-cell off-current distribution on >=1e4 holes with the 1e-4 hole below 1% of a level step at 85 C.

**Response — REFUTED:** The tail arithmetic is off by 1000x. 142 fA x 10^3.5 is ~0.45 nA, not 0.48 uA, and the 1e-4 cell (-186 mV) leaks ~17 pA, not 17 nA. Model section 11b, at sigma_Vt 50 mV: at 90 mV/dec the 1e-10 cell leaks 380 pA, 0.16% of the 234 nA 2-b level step; at 120 mV/dec it leaks 50 pA (0.02%). Even all 63 unselected cells at the full cutoff budget sum to only 7 nA, 3% of a step. The dependence on the neighbours' stored levels, which write-verify cannot cancel, is therefore small. No 0.3-0.35 V guard is needed for Vt tails. What did move the cutoff is the subthreshold slope (RT-CIRC-and-stack-01). At 120 mV/dec the unselected ring must sit at or below -0.15 V. The pull-down therefore rises from 1.09 to 1.30 V (guard 0.10 -> 0.15 V, covering Vt tail and temperature), and the CR bar rises to >= 0.57 at a 3.0 V swing.

*Action taken:* Keep the measurement anyway, since it is cheap: per-cell off-current and Vt distribution on >= 1e4 cells at 85 C in Phase 1A. Model: guard 0.15 V, v_plate_max 3.0 V.

### RT-DEV-and-stack-03 — MAJOR — DEV — §2.2 IPD (6 nm Al2O3/HfO2 laminate, 0.69 V across it on every neighbour read); §2.10 GO disturb test (1e9 neighbour writes only)

> Every read of any tier in a hole swings the 63 other select plates by ~1.8 V, so each unselected ring moves 1.09 V and its IPD sees a 0.7 V excursion on every neighbour read. Al2O3/HfO2 laminates show dielectric relaxation and charge trapping (Curie-von Schweidler). At 0.1-1% of the IPD and gate displacement charge (~760 + 400 e-), that is ~1-12 e-, or 0.7-8 mV on a 0.246 fF ring per excursion, with history-dependent recovery. A hot hole read at MHz rates accumulates this against an 86 mV 2-b drift budget. The GO disturb test counts 1e9 neighbour writes but no neighbour reads.

*What would change the reviewer's mind:* A read-disturb test on the planar emulation: ring shift <=30 mV after 1e12 neighbour select-plate excursions at 85 C.

**Response — ACCEPTED-MITIGATED:** Valid for the original bias, where every read swung the 63 other rings. Each excursion moves ~1,660 electrons of displacement charge, so trapping 0.1-1% of it shifts the ring 1.2-12 mV (model section 11h). The fix is to idle the select plates LOW. Rings are then parked below cutoff at all times, and a ring moves only when its own tier is read. Neighbour reads cause no excursion, a 64x cut when reads are spread evenly. Idling low puts a permanent DC bias on the IPD. Offsetting the selected-plate level to V_ref ~ +1.27 V centres that bias at <= 1.27 V (2.1 MV/cm) for the -3 sigma CR cell. A single-cell read hammer can still cause up to 1e7 excursions per second. But refresh rewrites the level with write-verify every ~1 s, so the shift that matters is the one inside one refresh interval.

*Action taken:* GO #1A adds a read-disturb test at 85 C: <= 30 mV ring shift after 1e8 own-tier excursions inside one refresh interval, and after 1e12 cumulative, with IPD relaxation and recovery logged.

### RT-DEV-and-stack-04 — MAJOR — DEV — §4 #2 topology closure; write FET L = one plate (~40 nm); 'write-plate hold -1.5 V gives 10.1 decades'

> The ring must contact the film ohmically under its write plate yet act as an insulated gate on the same continuous film at the select level. Isolation rests on a ~40 nm write-plate-gated segment of 5 nm film, fringed by the adjacent select plate swinging ~1.8 V, and the vertical film path from the ring contact to the read channel is gated only by fringe. The '10 decades of suppression' assumes an ideal 90 mV/dec, but a 40 nm, side-gated, curved thin-film segment will show DIBL and a degraded slope. At an effective 120-150 mV/dec, suppression falls to 6-7.5 decades, which puts hold leakage near the 21 aA budget before any trap-assisted term.

*What would change the reviewer's mind:* 3D TCAD of the real write-level segment, with fringe and curvature, showing >=9 decades; then a measured planar 'ring contact + gated segment + read channel' structure holding <=21 aA at 85 C.

**Response — ACCEPTED-MITIGATED:** Valid on the original geometry, and that geometry's single-film closure does not exist anyway (RT-PROC-and-stack-01). In the two-film redesign the isolating segment is the write film on the notch floor, ~10 nm long. The write plate wraps it from above through its own 8 nm dielectric. Its slope and DIBL are the risk, so the model is deliberately pessimistic: 120 mV/dec central and 160 worst, a 0.15 V DIBL penalty and a -3.72 sigma Vt tail. At -3.0 V hold the tail segment is >= 1.9 V below Vt and leaks 0.0006 aA (120 mV/dec) to 5 aA (160 mV/dec), against a 17 aA budget. The write film can also be a separate composition: Ga-rich and higher-Vt, decoupled from the high-mobility read film.

*Action taken:* Phase 0 3D TCAD of the notch segment, with fringe and curvature, must show >= 9 decades at -3.0 V hold (kill gate G0). Phase 1B measures ring hold <= 100 aA through the real segment at 85 C. Phase 1A measures write-FET tails on >= 1e4 devices.

### RT-IND-and-stack-01 — MAJOR — IND — §3 Prior art (NEO 3D X-DRAM row); §7 Partners

> NEO Semiconductor already occupies 'DRAM on a NAND process'. It launched 3D X-DRAM in 2023-25, with IGZO 1T1C and 3T0C variants announced in 2025. In April 2026 it reported a PoC at NIAR-TSRI with <10 ns read/write, >1 s retention at 85 C and >1e14 endurance, in a round led by Stan Shih (rt-IND log). AND-STACK would arrive ~3 years later, with a ~100 ns 2-b write-verify page write and a 1e12-cycle endurance anchor. Telling for the licensing model: this review found no named NEO licensee or signed partner ~3 years after launch, despite a working PoC.

*What would change the reviewer's mind:* A claim-by-claim comparison against NEO's 3D X-DRAM patents showing the dual-plate floating ring is outside them. Plus one measured AND-STACK advantage NEO does not have, such as 2 b/cell holding >=1 s at 85 C with select-plate CR >= 0.53. Or evidence that any memory maker has licensed a NAND-process DRAM cell.

**Response — ACCEPTED-MITIGATED:** Accepted as a positioning fact. It is not a physics objection, and NEO's progress shows the category has demand. NEO's 3D X-DRAM proof of concept (April 2026; company-reported <10 ns, >1 s at 85 C, >1e14 cycles) is a 1-b cell. AND-STACK's case is 2 b per tier with a non-destructive read: on the revised model, 5.9x 1-beta density at 64 tiers. It has no write-speed case, because its writes are now microsecond-class page operations. The plan has three parts. (1) A Phase 0 claim chart against NEO's 3D X-DRAM patent families, alongside Macronix. (2) The differentiator NEO has not shown goes into GO #1A and #1B: 2 b/cell holding >= 1 s at 85 C, with select CR >= 0.57, on a vertical cell. (3) NEO's lack of a licensee weakens a licensing-only route, so the scale path now leads with a joint development agreement (JDA) with a NAND maker, not a licence.

*Action taken:* Add the NEO claim chart to the IP budget ($60k), add the differentiator measurement to the GO lists, and re-order the scale path to JDA first.

### RT-IND-and-stack-02 — MAJOR — IND — §3 'The delta'; §6 FTO (Macronix 'natural licensor')

> The pillar topology is Macronix 3D AND (US 12,245,428 / 12,156,402 / 12,200,935), and Macronix also holds 3D 2T0C. The select plate wrapping the ring is the coupling capacitor of the familiar capacitively coupled 2T1C gain cell, where a read wordline boosts the storage node through a capacitor. Examples include SEL's NOSRAM-family oxide gain cells [training knowledge] and the per-cell capacitor tied to a wordline in series oxide gain-cell NAND (US 8,421,071). What stays new is geometry: a floating TiN ring in a recess, and BL = SL writing. The 'natural licensor' is also the party best placed to build the cell on its own 3D AND line, which leaves the startup little bargaining power.

*What would change the reviewer's mind:* Claims read on the three Macronix families, SEL NOSRAM and US 8,421,071, showing the dual-plate + floating-ring + BL=SL-write combination is non-obvious and claimable. Ideally backed by a Macronix option or JDA.

**Response — ACCEPTED-DOWNGRADE:** Accepted. The select plate that couples the ring is the read-wordline boost capacitor of 2T1C gain cells (the SEL NOSRAM family; US 8,421,071). The twin S/D pillars are Macronix's: two N+ poly plugs split by a SiN column, shown at 8 layers with 34 'viable' (IEDM 2020 coverage). A broad 'dual-plate AND gain cell' claim is unlikely to survive. Claimable novelty narrows to four items: (1) the two-film notched write pocket, where a per-hole write film in a write-plate notch contacts the ring's top face; (2) the idle-low / deep-hold bias scheme with the V_ref offset; (3) the sequential group write with a floating-SL bottom select; (4) temperature-triggered MLC rewrites. This lowers the licensing value, since Macronix could build around or alongside, but not the size of the step.

*Action taken:* Rewrite Provisional #1 around the notch-write module and the bias scheme. In Phase 0, read the claims of the three Macronix families, SEL NOSRAM, US 8,421,071 and US11631453. Approach Macronix for an option or JDA after filing.

### RT-IND-and-stack-03 — MAJOR — IND — §2.6 Cost and §2.8 Sensitivity; models/and-stack.py comp_1b_usd_gb=1.48, $/tier=30 ('unanchored')

> The 3.8x bits/$ compares a hypothetical 64-tier 2-b product against 2026 1-beta at $1.48/GB. On the dossier's own path (planar M11, 4-tier M23, 16-tier JDA, 32-64-tier short loops, licensee qualification), first volume is ~2032-33. Incumbent cost per bit falls ~8-12%/yr, which puts the comparison point at ~$0.69-0.90/GB, and 3.8x shrinks to ~1.8-2.3x. That sits inside the model's own 1.8-4.4x range, which an unanchored $30/tier and 1% tier defects set. Incumbent 3D DRAM (Samsung VS-DRAM, SK hynix) will be shipping into the same window.

*What would change the reviewer's mind:* The cost model re-based to the incumbents' ~2032 roadmap (1d, 4F2, 3D) and still showing >=3x, with $/tier anchored to a NAND maker's cost per layer pair.

**Response — ACCEPTED-DOWNGRADE:** Accepted and quantified (model section 11i). With all red-team inputs, 64 x 2 b costs $0.65/GB at component level: 2.3x bits/$ against 2026 1-beta ($1.48), down from 3.8x. An incumbent riding an 8-12%/yr decline reaches ~$0.69-0.90/GB by ~2032, so the first product is only 1.1-1.4x cheaper per bit. A two-deck 96 x 2 b part reaches $0.57/GB: 2.6x against 2026 and 1.2-1.6x against 2032. The comparison ignores AND-STACK's own learning curve and incumbent 3D DRAM, either of which could move it either way. Bits/$ is no longer the headline claim; density (5.9x) and EUV-free capital are.

*Action taken:* Rewrite the step-change claim: density first, then bits/$ of 2.3x vs 2026 and ~1.1-1.6x vs 2032. Anchor $/tier to a NAND maker's cost per layer pair during the JDA approach.

### RT-IND-and-stack-04 — MAJOR — IND — §5 Decisive experiment (Phase 1 planar, Phase 2 200-300 nm e-beam holes); §4 #6-7

> The seed deliverable is a ~$150k planar 64-cell emulation with e-beam floating TiN islands. Phase 2 uses 200-300 nm e-beam holes in a 0.8 um, 4-tier stack. A memory maker's first questions are show-stoppers #6-7: etching 128 alternating metal/dielectric plates at 60:1 (NAND etches oxide/nitride and replaces the nitride later); 18 nm recess ALD; two 22 nm pillars in a 68 nm core at a 24 nm plate web. None of these is touched before the raise. The investor sees a coupling-ratio number, not evidence the structure can be made at 150 nm pitch.

*What would change the reviewer's mind:* A partner short loop (NAND pilot line or Albany) showing a >=32-plate replacement-gate stack etched at <=100 nm CD, with per-tier recess uniformity <=2 nm, even without working cells.

**Response — ACCEPTED-DOWNGRADE:** Accepted. The seed proves the cell physics and, now, the closure on a 2-tier vertical coupon at a relaxed 250 nm pitch. It does not prove a 64-tier, 170 nm-pitch structure, twin 28 nm pillars or a 256-layer mixed etch. A partial fix fits the budget: an $80k 32-tier dummy-stack coupon (SiO2 / poly-SiGe / SiN, no cells) etched at 110 nm, through a tool-vendor demo lab or a NY CREATES short loop. It measures CD taper, bow and SiGe recess uniformity by TEM, with targets of <= 5% CD variation and recess sigma <= 2 nm. If no vendor slot is available, the coupon becomes the first milestone of the raise. Provability falls from 'partly: physics by month 11' to 'partly: closure at relaxed pitch by month 14'.

*Action taken:* Add the dummy-stack etch coupon ($80k, months 8-16) and state manufacturability as a milestone for the raise.

### RT-PROC-and-stack-02 — MAJOR — PROC — §1 'deposit a tall stack of metal plates, etch one field of holes'; §4 #7; model INPUTS tier_pitch_nm=80, ring_h_nm ('6 nm W caps + 6 nm IPD top/bottom')

> As modelled, the 'sandwich' select level is W 6 nm / IPD / 18 nm ring / IPD / W 6 nm. That can only be made by recessing a different middle material X between two W caps. With the write plate and inter-plate oxide, each tier is ~5 sublayers of 3-4 materials, so 64 tiers is a ~320-layer single etch at AR 60, not '128 plates'. A gate-first build puts ~2.8 um of W/Mo in the stack; at ~1 GPa that bows a 775 um wafer by ~1.7 mm (Stoney), against the ~0.1-0.2 mm litho and bond chucks tolerate, and no HAR etch through such a stack has a precedent. A gate-last build (NAND-style replacement) runs a WF6/H2 or Mo-chloride/H2 fill at 300-500 C after the IGZO is in the hole. That floods the channel with the hydrogen the H-lean mold and the <=86 mV 2-b drift budget exist to exclude.

*What would change the reviewer's mind:* A demonstrated >=32-tier stack of the actual materials, etched at AR >=30 with <=5% CD variation and bow <=150 um. Alternatively, a replacement-metal flow after which coupon IGZO Vt shift is <=20 mV and 2-b drift <=86 mV.

**Response — ACCEPTED-DOWNGRADE:** Accepted in part. The sandwich select level is dropped, because the ring's top face is now the write contact. A tier is therefore 4 layers, SiO2 / poly-SiGe / SiO2 / SiN (90 nm), giving 256 layers at 64 tiers (6.06 um, AR 55), not ~320. On bow, Stoney confirms 1.75 mm for 2.8 um of W at 1 GPa (model section 11j), so gate-first metal is dropped. The etched stack is stress-tunable dielectric and poly, as in NAND, and the write-plate metal arrives later from the slits, like NAND's replacement W. On hydrogen, the replacement fill uses O2-based ALD Ru (no WF6 or H2) plus a final H+O anneal, and the poly-SiGe select plates are annealed at >= 800 C before the films go in. Two things remain unprecedented: a 3-4-material, 256-layer etch at AR 55 (Micron etched oxide/poly at up to 96 tiers; Samsung etches oxide/nitride), and Ru replacement after IGZO. Two 32-tier decks are the etch hedge, adding ~$400/wafer at 96 tiers.

*Action taken:* Dummy-stack etch coupon: 32 tiers, CD variation <= 5%, bow <= 150 um. Coupon 1B measures IGZO dVt <= 20 mV and 2-b drift <= 78 mV after the Ru fill. Model: tier_pitch 80 -> 90 nm, array_base +$1,200.

### RT-PROC-and-stack-03 — MAJOR — PROC — §1 top view; §4 #6; model INPUT pillar_w_nm=22 ('BL and SL metal pillars inside the 68 nm core')

> Two separate 22 nm metal pillars in a 68 nm core down a 5.42 um stack can be made only two ways. One is two ~22 nm sub-holes at AR ~245, aligned inside the channel hole; the other is one fill split by a <=20 nm slot etched 5.4 um deep. Neither exists in production: NAND channel holes are ~100 nm at AR <=70 per deck. Doped-poly pillars (Macronix 3D AND's choice) can be filled, but at ~1 mOhm-cm a 22 nm x 5.4 um pillar is ~140 kOhm and drops up to 0.13 V at the 0.89 uA read current, more than the 0.1 V Vds. Pillar shorts are also hole-level (all 64 tiers), so tier-orthogonal codes do not fix them.

*What would change the reviewer's mind:* A coupon >=2.8 um deep (16-32-tier depth) with two isolated metal pillars per <=100 nm hole, <=1e-4 pillar-to-pillar shorts over >=1e5 holes, and <=10 kOhm per pillar.

**Response — ACCEPTED-DOWNGRADE:** Accepted. Two 22 nm pillars in a 68 nm core at AR ~245 are not credible. There is evidence for the class: Macronix's vertical AND/NOR cell puts two N+ poly S/D plugs, split by a SiN column, in each hole, shown at 8 layers with 34 'viable' (IEDM 2020 coverage). Doped poly is excluded here, though: 98 kOhm, costing 69% of Vds even with split contacting (model section 11e). The redesign moves to a 110 nm hole at 170 nm pitch, which keeps the 24 nm web and gives an 88 nm core for two 28 nm W-core pillars (~5.6 kOhm). It is built in two 32-tier decks joined by an inter-deck plug, so the pillar sub-holes reach AR ~110 per deck. y_hole drops from 0.97 to 0.93, because pillar shorts are hole-level and only column repair helps. The cost is density: the pitch alone gives (170/150)^2 = 1.28x less per tier, and with the other changes 64 x 2 b falls from 8.1x to 5.9x 1-beta. The >= 2.8 um twin-pillar coupon (<= 1e-4 shorts over 1e5 holes, <= 10 kOhm) needs a partner line and is a milestone for the raise.

*Action taken:* Model: pitch 150 -> 170 nm, hole 90 -> 110 nm, pillar 22 -> 28 nm, y_hole 0.97 -> 0.93. List the twin-pillar coupon for the raise. Phase 2 keeps 200-300 nm holes, where twin pillars are easy.

### RT-PROC-and-stack-04 — MAJOR — PROC — §2.6 cost; §4 #11; model INPUTS tier_usd=30, array_base_usd=1000

> $30 per tier (two metal plates plus a tri-layer) and $1,000 for the whole cell module sit below NAND's own economics. TechInsights' Choe put the 64-to-96-layer cost gain at only 10-15%. That implies 55-70% of a NAND wafer's cost scales with layer count, ~$20-38 per ONON pair at a $2.5-3.5k wafer [rt-PROC estimate]. An AND-STACK tier is two pairs built with metal depositions, which are slower and costlier than PECVD SiN. Its cell module adds >=5 HAR recess, ALD and etch-back steps. At $60/tier and a $2,000 base, the 64 x 2 b wafer is ~$8,840 and component cost ~$0.61/GB: 2.4x bits/$, not 3.8x.

*What would change the reviewer's mind:* A NAND partner's cost model (Kioxia, Micron, SK hynix) or Yole/TechInsights reverse-costing showing <=$35 per metal-plate tier and <=$1,200 for the AR-60 cell module.

**Response — ACCEPTED-DOWNGRADE:** Accepted. A tier is ~1.5-2 ONON-pair equivalents. On top of that, the cell module, the notch-write module, slit Ru replacement, twin sub-hole pillars, a bottom select and a second SADP level all add per-wafer steps. With revised inputs of $50/tier and a $2,200 base (wafer $8,400 at 64 tiers), 64 x 2 b costs $0.65/GB at component level: 2.3x bits/$ (model). The reviewer's $60/$2,000 case on the revised geometry gives $0.68/GB (2.2x); an optimistic $35/$1,600 gives 2.6x. Break-even rises to 18 tiers at 2 b and 44 tiers at 1 b.

*Action taken:* Model: tier_usd 30 -> 50, array_base 1000 -> 2200, with sensitivity rows in section 11i. Anchor these to a NAND partner's cost model before the raise.

### RT-CIRC-and-stack-04 — MINOR — CIRC — §2.3 read current / model pillar_w_nm 22 (metal pillars, 5.4 um)

> Pillar resistance is not modelled. Two 22 nm metal pillars 5.4 um tall (AR ~245) in TiN or W, at 30-150 uOhm*cm thin-film resistivity, are ~4-21 kOhm each. At 0.89 uA and a 0.1 V clamped Vds, bottom tiers lose ~8-38 mV of Vds, up to ~38% of current, so the 298 nA level step falls to ~185 nA. Write-verify cancels the static offset, but bottom-tier margin and the 1.5 ns resolve time degrade.

*What would change the reviewer's mind:* Pillar resistance and tier-position read current measured on the 4-tier stack.

**Response — ACCEPTED-MITIGATED:** Valid; it was not modelled. Model section 11e: a 28 nm pillar with a 3 nm TiN liner and a W core (35 uOhm.cm) over 6.06 um is ~5.6 kOhm. The fix is to contact BL at the top and SL at the bottom. That is needed anyway, because SL floats through a bottom select during writes. Every tier then sees one pillar length of series resistance. The loss becomes a uniform ~4 mV (4% of Vds) that write-verify cancels; contacting both pillars from the top would cost 8 mV (8%) at the worst tier. The level step falls from 234 to ~225 nA, and resolve time rises from 1.9 to ~2.0 ns. Doped-poly pillars (98 kOhm, 69-138% of Vds) are excluded.

*Action taken:* Adopt top-BL / bottom-SL contacting and specify W-core pillars. Phase 2 measures read current versus tier, and pillar resistance.

### RT-CIRC-and-stack-05 — MINOR — CIRC — §5 Phase 1 planar emulation / GO 'CR sigma <=0.03 over >=50 cells'

> The planar emulation uses e-beam TiN islands, so it measures planar island-to-island CR spread. It cannot measure the tier-to-tier CR sigma that sets plate swing. That comes from hole taper and bow over a 5.4 um, 60:1 etch, which change ring arc, recess depth and C_IPD/C_gate from top to bottom. The GO number is therefore not the 64-tier number.

*What would change the reviewer's mind:* Report CR versus tier on the 4-tier vertical stack and extrapolate taper to 64 tiers from a NAND-class hole profile.

**Response — ACCEPTED-MITIGATED:** Valid: e-beam islands measure island-to-island spread, not taper. Two answers. (1) CR is the ratio of two coaxial capacitors, so to first order it does not depend on CD. Model section 11g gives CR 0.594 at 110 nm and 0.593 at 88 nm (a 20% taper); a +/-3 nm change in ring thickness moves it +/-0.011. (2) Tier-to-tier offsets are trimmed per plate, with 64 select-plate trims per block as in NAND's per-WL biasing. The swing is then set by within-tier sigma. The model now uses sigma 0.045 instead of 0.03, and the GO bar becomes CR >= 0.57 at a 3.0 V swing. The vertical coupon (month 14) and the 4-tier stack (month 23) report CR per tier. A 32-tier dummy-stack etch coupon gives the taper and recess profile needed to extrapolate to 64 tiers.

*Action taken:* Change cr_sigma 0.03 -> 0.045 and put per-tier trims in the controller. Report CR versus tier on coupon 1B and in Phase 2. Take the taper profile from the dummy-stack coupon.

### RT-DEV-and-stack-05 — MINOR — DEV — §4 #7 plate stack (W/Mo plates, 6 nm IPD to the film)

> 128 plates of CVD W (WF6 with H2/B2H6/SiH4 nucleation) carry fluorine and hydrogen, both shallow donors in IGZO, within 6-10 nm of the channel. Out-diffusion during later <=400 C steps shifts Vt negative and raises off-current exponentially. The H-lean mold addresses the oxide layers, not the metal plates.

*What would change the reviewer's mind:* PVD Mo plates, or SIMS showing F and H <=1e19 cm^-3 in the film after the full thermal budget, with delta-Vt <=30 mV.

**Response — ACCEPTED-MITIGATED:** Valid for CVD W plates. The redesign puts no CVD W in the stack. Select plates are gate-first doped poly-SiGe; Micron's floating-gate 3D NAND used gate-first poly word lines at 32-96 tiers [UNVERIFIED-PK]. Because the periphery is on a separate bonded wafer, the array stack can take an >= 800 C activation and H/F drive-out anneal before any oxide film goes in. Write plates are replaced from the slits after the films, with an O2-based ALD Ru fill (no WF6, no H2 reducer), followed by a final H+O anneal. The cost is resistance. Poly select plates (~300 ohm/sq) need ~60 um segments to hold ~4.3 ns RC, which raises the staircase share (array efficiency 0.70 -> 0.66 in the model).

*Action taken:* SIMS on coupon 1B: F and H <= 1e19 cm^-3 in the films after the full thermal budget, with dVt <= 30 mV. Split Ru against Mo for the fill. Model: plate_rs 15 -> 300 ohm/sq, plate_len 200 -> 60 um, array_eff 0.70 -> 0.66.

### RT-IND-and-stack-05 — MINOR — IND — §7 Standards ('Launch as a CXL Type-3 expander'); §2.3 Write ~100 ns, page-buffered

> A CXL Type-3 launch with ~100 ns page writes behind an SRAM buffer makes AND-STACK a non-drop-in tier at ~2.5-4x lower $/GB than DRAM. Intel Optane held the same position: roughly half DRAM's $/GB and dependent on software tiering. Intel exited in 2022 with a ~$0.5B write-down [training knowledge]. Z-RAM shows that a capacitorless DRAM cell can win licences and still never ship: Innovative Silicon licensed it to AMD and Hynix and shut down in 2010 [training knowledge].

*What would change the reviewer's mind:* A plan for a DDR/HBM-compatible interface (write latency hidden inside JEDEC timings), or a hyperscaler LOI for a CXL capacity tier at the modelled price.

**Response — ACCEPTED-MITIGATED:** Accepted as a product risk, not a physics one. AND-STACK differs from Optane on reads: ~16 ns, DRAM-class, against Optane's several hundred ns. But after RT-DEV-and-stack-01 its writes are microsecond-class tier-page operations, so it is not drop-in DDR. The plan has three parts. (1) A die-level write-back architecture: writes land in per-bank SRAM page buffers at DDR timing, and the cell write-back runs in the background across many blocks. Internal write bandwidth is limited by energy, not by the array: ~0.4 mW per GB/s of cell writes. (2) Launch as a CXL Type-3 capacity tier only where >= 2x on $/GB matters, and seek a hyperscaler LOI before the Series A. (3) Accept that a non-drop-in tier at 1.1-1.6x cheaper than 2032 incumbents is a thin value case. That is a market risk, which the founder framing does not treat as a kill.

*Action taken:* Phase 0 architecture study: the buffer depth needed to hide write-back under JEDEC tWR at the measured page-write times. Add the LOI target to the raise plan.

### RT-PROC-and-stack-05 — MINOR — PROC — §2.2 CR spread; model INPUT cr_sigma=0.03

> Sigma_CR of 0.03 implies ~+/-1.5 nm control of recess depth and IPD thickness across 64 tiers and the wafer. Yet AR-60 NAND holes typically taper 15-25% in CD from top to bottom, and lateral recess rates track local CD and etchant transport. CR sets plate swing, not cutoff, so sigma 0.06 still gives CR_min 0.52 and a ~2.1 V swing, which is survivable. But read W/L (current per level) and C_SN also follow hole CD, so placing the 2-b levels needs per-tier verify trims, like NAND's per-WL biasing.

*What would change the reviewer's mind:* TEM recess-depth data on a >=32-tier coupon with sigma <=1.5 nm top to bottom, or a per-tier trim scheme shown to hold 4 levels despite tier-dependent CD.

**Response — ACCEPTED-MITIGATED:** Accepted for W/L and C_SN; overstated for CR. CR is a capacitance ratio and barely moves with CD: from 0.594 to 0.593 for a 20% taper, and +/-0.011 for +/-3 nm of ring thickness (model section 11g). C_SN (0.214 -> 0.178 fF) and read W/L do follow CD. Per-cell write-verify at the read bias already places each level in current space. Per-tier reference trims (64 per block, like NAND's per-WL biasing) absorb the tier-dependent level step. The planning value for sigma_CR rises to 0.045 (within-tier, after trims), and at a 3.0 V swing the bar is CR >= 0.57.

*Action taken:* Model: cr_sigma 0.045. Put per-tier trims in the controller spec. Require TEM recess sigma <= 2 nm on the dummy-stack coupon.

## cell-wafer-foundry — CELL-WAFER FOUNDRY: litho-light periodic oxide cell wafers bonded to U.S. foundry periphery under an open bitline-group bond spec (cell-wafer-foundry)

**Final status after red team: DOWNGRADED.** No physics kill: bond physics remains testable and the 0-EUV path stands. After parity, global-line coupling, SA area, deck cost, D2W, contamination and royalty corrections, the step-change factors roughly halve: capex 7.6x -> 3.6x and $/GB 0.36x -> 0.62x DDR5 (1T1C-64), and the 1T1C break-even moves from 16 to 28 tiers. Most of what remains is tier density that any in-house 3D DRAM gets; the split's own share is ~1.5x capex and only while existing logic capacity absorbs the periphery. The merchant/open-interface leg has no buyer, seller or royalty and is demoted to optional. Two new must-pass device gates were added: bond-plane hydrogen and the oxide sub-WL driver. The concept lives as the bond and integration scale path of whichever portfolio cell passes.

*Revised verdicts* — Possible: YES (unchanged). No physics is violated. New measured risks: bond-plane hydrogen into top-tier oxide channels and TFTs (needs ~1,400-3,500x barrier attenuation; one ALD Al2O3 layer has shown ~18x) and a bootstrapped n-only oxide sub-WL driver holding levels under Vt drift. Anisotropic warp is solved by D2W (0.14 um vs a 0.50 um budget at 2.0 um pitch). · Profitable: STEP CHANGE IF IT WORKS: capital intensity and EUV. 3.6x less new memory-fab capex per GB/month ($61 -> $17.1; was 7.6x) and 0 EUV layers vs 5-7. $/GB 0.62x DDR5 ($0.92; was 0.36x); density 3.6x 1b (was 4.5x); bitline energy 1.4x. Gain-cell variant: 5.9x capex, 0.38x $/GB, 5.8x density. All conditional on a 64-tier portfolio cell. The split itself contributes only ~1.5x capex (with existing logic capacity), so most of the factor is inherited from the cell's tiers. · Doable by this founder: PROVABLE WITH $1M: PARTLY. Standalone, $795k of experiments ($995k with founder pay) settles bond opens/bridges/overlay/voids, bond-plane hydrogen, the oxide sub-WL driver and group select, adhesion and contamination on 4- and 8-tier coupons bonded D2W at a fab-grade partner by M22. It cannot settle a 64-tier cell, the deck-driven cell-wafer cost or merchant economics. Within the portfolio seed (~$60k funded): NO unless a bonding partner contributes in kind.

### RT-CIRC-cell-wafer-foundry-01 — MAJOR — CIRC — §2 bond grid ('1:8 oxide-TFT WL predecode') / §4 #7 'the predecode is digital and offset-tolerant'

> The wordline drive through n-only oxide predecode is analog, not digital. IGZO cells need a negative wordline hold (~-0.5 to -0.7 V across the portfolio, for zA leakage) and a ~2.3-3 V high. An n-only pass TFT passes the high level only up to V_gate - Vt, so its gate needs ~3.5-4 V or 1970s-style bootstrapping. Its 50-100 mV Vt drift (the I-02936 critics' figure) lands directly on the wordline high level and therefore on the restore level. Unselected wordlines behind an off predecode TFT float instead of being clamped at the negative hold, so neighbour coupling lifts them and erodes retention. The predecode switches the wordline voltage itself.

*What would change the reviewer's mind:* A predecode/driver circuit with simulated wordline high and hold accuracy of +/-50 mV over oxide Vt drift, active clamping of unselected wordlines at <=-0.5 V, and its area in the 8% edge budget.

**Response — ACCEPTED-MITIGATED:** Valid. Calling the predecode 'digital and offset-tolerant' was wrong: the n-only oxide TFT is an analog switch in the WL path, and an off pass gate leaves the WL floating. Redesign: a 1980s-style self-bootstrapped n-only sub-WL driver. The pass-TFT gate is precharged and then coupled up by the FX edge to ~3.0 + 0.7 x 3.0 = 5.1 V. That leaves 1.3 V of overdrive at VPP with an end-of-life Vt of 0.8 V. The WL high is therefore the silicon FX-rail level, and a 0.1 V PBTI drift changes R_on by ~8% (edge time), not the restore level. Each WL gets an active n-TFT clamp to the silicon VNWL rail (<=-0.5 V), so unselected WLs are held, not floating. VPP keeps >=150 mV of overdrive above the cell Vt, so the restore level is set by the bitline. Load per tier WL is 5,000 cells x 0.04 fF + wire = 260 fF. A 5 ns edge needs 156 uA, i.e. W ~0.8 um of short-channel ALD In2O3. Area is 7.4e6 WL segments x 0.45 um2 = 3.3 mm2 = 19% of the array. It does NOT fit the 8% edge budget the critic asked about, so it moves to a dedicated TFT driver plane over the array (+$60 per cell wafer). This is not demonstrated: it becomes a measured gate.

*Action taken:* Adopt the bootstrapped sub-WL driver with VNWL clamp on a dedicated TFT plane (+$60/cell wafer in cell_common_adders). Put it on coupon lot 1 driving a 260 fF dummy WL. Add kill K3b: <=50 mV level loss, <=10 ns edges and a <=-0.5 V clamp after 1,000 h at 125 C, else the TFT-predecode leg dies (revival: a layer-transferred thin-Si driver plane).

### RT-CIRC-cell-wafer-foundry-02 — MAJOR — CIRC — §2 bitline and cell (Cs 1.16 fF at 26 mV) / model ecc 1.0625, dv_min_margin_mV 26

> The sense threshold and ECC parity are inconsistent. Cs = 1.16 fF uses MARGIN STACK's 26 mV threshold, which exists only at raw BER 1e-4 with BCH t=8 (15.6% parity). The model uses ecc = 1.0625 (DDR5 on-die), which overstates density by ~8.8% (2.01 -> ~1.85 Gb/mm2). The 26 mV also assumes 1-beta-like coupling. A 47 um global line at 80 nm pitch behind a 146:1 oxide group select has data-dependent BL-BL coupling alpha ~0.1-0.2 per side, which the model omits. That requires S >= 26/(1-2*alpha) = 33-43 mV, i.e. Cs 1.5-2.0 fF. Together, density lands at ~1.5-1.75 Gb/mm2 (3.4-3.9x), and $/GB rises ~10-25%.

*What would change the reviewer's mind:* Field-solver alpha for the 47 um global line and a model re-run with ecc 1.156 (or the RAW-BER t=9 value), showing density >=4x.

**Response — ACCEPTED-DOWNGRADE:** Valid on both counts. (1) Parity: the 26 mV threshold requires BCH t=8 parity (15.6%). The model now uses ecc 1.156 for 1T1C, which alone takes density 2.01 -> 1.85 Gb/mm2 (-8%). (2) Coupling: modelled from geometry as 0.05 fF/um per side of the global line (~2/3 of 0.15 fF/um), giving alpha = 0.145 unshielded on the revised 73 um line, inside CIRC's 0.1-0.2. That needs S = 36.6 mV, Cs 2.05 fF and 1.43 Gb/mm2 (3.2x). Redesign: route global lines on two metal levels with a grounded shield between neighbours (+~$120/cell wafer). Residual alpha is 0.035, S 28.0 mV. Net CIRC-02 effect at the original SA size: 2.01 -> 1.81 Gb/mm2 (4.5x -> 4.0x, -10%) and $/GB 0.54 -> 0.60 (+11%). This meets the critic's '>=4x' condition only at a 2.5 um2 SA; with CIRC-03 the total is 3.6x. For comparison, the conventional 50 mV / 6.25% option with shielding gives 1.27 Gb/mm2 (2.8x). I-12302 plate-strip sensing (~135 mV vs ~14 mV) was considered. In this bond-group architecture it needs a local gain FET per 8-64-cell strip, which turns the 1T1C into the non-destructive spec class (equal to the gain-cell route: 2.60 Gb/mm2). It also faces Micron's planar prior art (US 5,991,216; 8,009,460), so it is kept as the 1T1C revival path, not the base.

*Action taken:* Model: ecc 1.0625 -> 1.156; c_cpl 0 -> 0.05 fF/um; shield_factor 0.25 with two shielded metal levels (+$120/cell wafer). This lowers the 1T1C density claim by ~10% (4.5x -> 4.0x before CIRC-03). Add field-solver alpha extraction to the experiment and a K5' re-scope trigger if shielded alpha >0.05.

### RT-DEV-cell-wafer-foundry-01 — MAJOR — DEV — §2 GO ('after a <=250 C anneal, delta-Vt <=20 mV'); §4 #4 workarounds

> Oxide-oxide (SiO2/SiCN) hybrid bonding releases water and hydrogen at the bond plane. Activated surfaces carry ~4-5 OH/nm^2, and condensation releases ~2-5e14 H2O/cm^2 within ~1 um of the top tier and of the oxide-TFT group selectors and WL predecode that sit on the bond side. An IGZO donor sheet of 1e12 cm^-2 shifts Vt by ~0.14 V at EOT 3 nm, so if ~0.03-0.07% of that inventory acts as donors in a channel, the 20 mV spec is broken. A 180-250 C bond slows diffusion but leaves the inventory in place for the life of the part. The Arrhenius-dose argument does not cover this.

*What would change the reviewer's mind:* ToF-SIMS on bonded 4-tier coupons showing no H rise in the top-tier channel, plus delta-Vt <=20 mV on top-tier cells and selector TFTs after bond, anneal and a 1,000 h 125 C bake, with or without an ALD Al2O3/SiN barrier under the bond layer.

**Response — ACCEPTED-MITIGATED:** Valid and not refutable by arithmetic. 20 mV at EOT 3 nm allows 1.44e11 donors/cm2, i.e. 0.03-0.07% of the 2-5e14 H2O/cm2 bond-plane inventory. Molecular H2 diffuses ~137 um in SiO2 during a 250 C / 2 h anneal and ~2.9 mm over 10 yr at 85 C [UNVERIFIED-training D], so an oxide standoff does not help; only barriers do. If all of the inventory were mobile, the barrier stack must attenuate ~1,400-3,500x. A single O3-ALD Al2O3 barrier cut an IGZO TFT's hydrogen-exposure shift from ~-12 V to ~-0.66 V (~18x; Ajou, logged). A 3-layer Al2O3 / low-H SiN / Al2O3 stack is ~300-5,800x only if the layers act independently [SPECULATIVE]. Note that the split's 'hydrogen freedom' argument is now neutral: monolithic CuA has the periphery-BEOL hydrogen problem instead. I-12627 (series write devices square the leakage tail) does not rescue this, because bond-plane hydrogen is a correlated sheet source. Mitigation: barrier stack plus SiCN (lower OH than SiO2) bond dielectric, plus a measured gate. The gate uses D-labelled bond surfaces (D2O rinse or D-plasma), so ToF-SIMS separates bond-origin hydrogen from background. ΔVt is measured on top-tier cells AND selector/driver TFTs after the bond, 3 x 260 C reflow and 1,000 h at 125 C, across the barrier splits.

*Action taken:* Add an Al2O3/low-H SiN/Al2O3 barrier under the bond layer (+$20/cell wafer). Add the D-labelled ToF-SIMS + 1,000 h 125 C + reflow gate and the barrier split to lot 1 (FA line F +$35k). Extend K3' to cover selector/driver TFTs and the best barrier. Revival if it fails: Cu-only room-temperature SAB, or TFTs on the substrate side.

### RT-IND-cell-wafer-foundry-01 — MAJOR — IND — §3 Genuine delta and 'Not new'; §6 IP ('publish under an open licence with a royalty-free or FRAND pledge')

> The generic array/periphery split is anticipated (US 10,340,261; 11,430,766; 11,114,453; 11,094,653). Proprietary versions already run in-house: Samsung VCT/PUC and VS-DRAM peri-on-cell, SK hynix VG, Kioxia CBA and YMTC Xtacking. The spec itself is to be published royalty-free. Revenue therefore comes only from narrow implementation patents (domain-switched supply adjacency, bond-link BIST and remap, a grid matched to sense-amp area), which incumbents with large bonding estates can design around. The UCIe/OCP model the dossier cites has made money for no spec originator.

*What would change the reviewer's mind:* One incumbent or foundry agreeing to adopt the spec and license the implementation patents. Or a claim on the supply-adjacency rule shown to be unavoidable at <=1.5 um pitch.

**Response — ACCEPTED-MITIGATED:** Valid as a value-capture objection. The generic split is anticipated and already runs in-house, and a royalty-free spec earns nothing. The supply-adjacency claim is also avoidable: a designer can cluster supply pads instead of domain-switching them. The mission does not kill on business grounds, and this changes no physics or step-change number. It does change the plan. The spec is published as a defensive, reciprocal-licence standard, not a revenue engine. Value is captured through: (a) implementation claims on the bond-ready oxide cell wafer (stress-compensated, hydrogen-barriered, co-specified with a measured anneal/reflow budget); (b) the bootstrapped oxide sub-WL driver plane with VNWL clamps; (c) D-labelled bond-hydrogen qualification and bond-link BIST/remap methods; (d) bundling with whichever portfolio cell passes. Standards spending is cut from $20k to $5k until an adopter appears.

*Action taken:* Re-base the IP strategy: defensive open spec with reciprocal licence; provisionals on the bond-ready oxide stack, the oxide SWD plane and the D-labelled qualification method. Drop the claim that the adjacency rule is unavoidable. Budget line I $20k -> $5k.

### RT-IND-cell-wafer-foundry-02 — MAJOR — IND — §2 Capex ($61 -> $8 per GB/month) and Null hypothesis (+$800 per pair; >=$12.5/tier); §9 D1

> About 4.2x of the 7.6x capex claim is tier density, 'which any in-house 3D DRAM would also get'. That leaves ~1.8x for the split itself. The split costs +$800 per wafer pair and pays only if a NAND-class line processes each tier >=$12.5 cheaper than logic BEOL at 64 tiers (42% of the $30 assumed). No data supports that per-tier advantage. If it fails, the dossier's own D1 demotes the concept to 'an option inside someone else's 3D DRAM'.

*What would change the reviewer's mind:* A fab-cost model from a NAND maker or a cost-analysis house showing per-tier cost on a NAND line >=$12.5 below logic BEOL. Or a thermal or hydrogen reason the cell steps cannot run on the periphery wafer.

**Response — ACCEPTED-DOWNGRADE:** Valid, and worse after the red-team corrections. The revised capex factor is 3.6x (1T1C-64), of which 3.3x is good GB per wafer (tier density) that any in-house 3D DRAM also gets. A monolithic in-house 3D DRAM that must process its own periphery needs ~$26.4 per GB/month against $17.1 for the split, so the split's own share is ~1.5x, and only while existing 28 nm logic capacity absorbs the periphery (1.0x if it must be built). The null-hypothesis bar rises: the W2W premium is $977/pair, needing >=$15.3/tier at 64 tiers (51% of a $30 tier). D2W costs $1,369 net of a $208 KGD saving, needing >=$21.4/tier, because a cell-only wafer cannot be fully KGD-tested (owner correction: 50% screen capture). Partial counter-evidence: Samsung chose W2W peri-under-cell bonding for its IGZO 4F2 VCT, and Kioxia/YMTC bond NAND. Incumbents with both options pick the bond, but that supports the in-house split, not the merchant one. No data shows a $15/tier NAND-line advantage.

*Action taken:* Restate the step-change claim as inherited: 3.6x capex / 0.62x $/GB comes mostly from the cell's tiers, and the split adds ~1.5x conditional. D1' threshold raised to $15.3 (W2W) / $21.4 (D2W) per tier. Commission a per-tier fab-cost comparison (NAND line vs logic BEOL) as a raise-stage item.

### RT-IND-cell-wafer-foundry-03 — MAJOR — IND — §7 Who partners and why; §8 U.S. manufacturability ('no U.S. NAND-class volume line')

> There is no merchant buyer or seller. Samsung and SK hynix 'would license implementation patents, not buy merchant wafers'. The only plausible cell-wafer makers (Kioxia, Samsung, SK hynix/Solidigm, Micron, YMTC) are vertically integrated and would arm competitors by selling cell wafers to third-party periphery. No U.S. NAND-class line exists, and an owned 300 mm cell line costs more than the $10-50M round. Memory has no precedent for a merchant array wafer.

*What would change the reviewer's mind:* An LOI from a cell-wafer maker (e.g., a NAND maker with idle decks) and a periphery foundry agreeing to trade wafers under the spec.

**Response — ACCEPTED-DOWNGRADE:** Valid. No merchant cell-wafer seller or buyer exists. Every plausible cell-wafer maker is vertically integrated, no U.S. NAND-class line exists, and an owned line exceeds a $10-50M round. Per the mission this is not a kill, since a market structure is not physics, and logic had no merchant foundry before 1987. But the 'merchant' adjective and the U.S.-supply-independence step change cannot be claimed today. The first realistic adopter is in-house: a U.S. memory maker (Micron) bonding its own oxide cell wafers to U.S. logic periphery, or a NAND maker with idle decks using the spec internally. The U.S.-manufacturability claim is downgraded from 'step change' to 'enabler'. The periphery is U.S.-sourceable on existing logic capacity, and the cell line needs a partner.

*Action taken:* Demote the merchant leg to optional. Retarget scale-path partners to in-house adopters (Micron + U.S. logic periphery; a NAND maker with idle decks). Revival of the merchant leg: an LOI from a cell-wafer maker plus a periphery foundry agreeing to trade wafers under the spec.

### RT-IND-cell-wafer-foundry-04 — MAJOR — IND — §6 Portfolio caveat (only A, H, I ~$75k seed-funded); §2 Sensitivity (particles: 0.5/cm2 -> W2W yield 0.70); §9 K4

> Inside the portfolio seed, only ~$75k (spec, IP, standards) is funded. The bond vehicles (~$625k) become partner, grant or raise items, so the seed tests no bond physics at all. Run standalone, the GO bar needs <=0.05 particles/cm2: the model gives W2W yield 0.70 at 0.5/cm2 and 0.24 at 2/cm2. Bonding Purdue coupons at a SkyWater facility could therefore trip K4 because of university-cleanroom particle density, not the concept. Bonding houses (imec, EVG, Adeia) already generate this class of data routinely.

*What would change the reviewer's mind:* A fab-grade bonding partner (imec, NY CREATES, Intel or TSMC packaging) committing in kind to the 8-tier W2W lot within the seed, with particle density documented.

**Response — ACCEPTED-MITIGATED:** Valid. Inside the portfolio seed only ~$60k (spec, IP, standards) is funded, so the seed alone tests no bond physics. Standalone, university-cleanroom particles could trip K4: W2W void yield is 0.67 at 0.5/cm2 and 0.20 at 2/cm2 in the revised model. Fixes: (1) all bond-layer CMP, clean, inspection and bonding at a fab-grade partner, with particle maps logged per wafer; (2) opens/bridges counted only on CSAM-void-free fields, so particle density cannot masquerade as bond physics; (3) D2W primary, which confines voids to one die (void yield 0.905 even at 0.5/cm2, $1.00/GB vs $1.30 W2W); (4) pursue in-kind bonding through a NY CREATES/NSTC startup programme or a bonder-vendor demo lab. Honest verdict: provable within the portfolio seed = No unless that in-kind partner commits; standalone = Partly at $795k of experiments.

*Action taken:* Make the fab-grade partner a Q1 gate (quote <=$275k or in-kind commitment, else switch partner). Adopt void-free-field accounting in GO/K2'/K4'. State the portfolio-seed provability as No in §0/§11.

### RT-PROC-cell-wafer-foundry-01 — MAJOR — PROC — §2 sensitivity 'Residual run-out after compensation 10% / 25%'; §4 #1; model runout_um (delta = b*t/r)

> The overlay model treats run-out as isotropic, so magnification compensation removes 75-90% of it. Multi-tier memory stacks warp anisotropically; the cited 3D NAND +300/-550 um is a saddle. Using the model's own delta = b*t/r, that saddle gives ~+1.5 um along one axis and ~-2.8 um along the other at r = 150 mm. Isotropic correction removes only the ~-0.65 um mean, leaving ~+/-2.2 um against a 0.375 um budget at 1.5 um pitch. The bow <=200 um gate is necessary but not sufficient.

*What would change the reviewer's mind:* Bonded overlay maps on 8-tier coupons (IR verniers at centre, mid-radius and edge, both axes) showing <=0.30 um after compensation. Alternatively, an anisotropic warp component <=~40 um after backside compensation.

**Response — ACCEPTED-MITIGATED:** Valid. Using the model's own Delta = b*t/r, a +300/-550 um saddle gives +1.55 / -2.84 um run-out. Isotropic correction removes only the -0.65 um mean, leaving +/-2.20 um, 5.9x the 0.375 um budget at 1.5 um. W2W needs an anisotropic half-difference <=73 um with perfect isotropic correction (PROC's ~40 um gate adopted). Redesign: D2W becomes the primary bond mode. Each ~4 mm die is flattened alone, so the worst wafer curvature (0.049/m) gives only 0.038 um of die-level run-out. Adding 0.10 um (3 sigma) placement (Besi CHAMEO ultra plus AC, logged) gives 0.14 um, a 2.7x margin at 1.5 um. The spec pitch also moves to 2.0 um at no density cost (the SA-limited group), giving a 0.50 um budget, 3.6x margin and a 97 um W2W saddle allowance. D2W is priced by throughput at +$600/pair with partial cell-die screening, so $/GB is $0.92 D2W vs $0.91 W2W: cost-neutral. Stress-balanced 0/90 deg die orientation is kept as a W2W revival lever.

*Action taken:* D2W primary; spec pitch 2.0 um (1.5 alternate, 1.0 dropped). Both-axis shape maps and IR verniers. K1' drops W2W (not the concept) if the anisotropic half-difference stays >40 um. Model: d2w_extra_cost 300 -> 600, cell_kgd_capture 1.0 -> 0.5, plus an anisotropic warp section.

### RT-PROC-cell-wafer-foundry-02 — MAJOR — PROC — §2 base case 1T1C, 64 tiers, footprint 80 x 323 nm; model INPUTS cell_base_cost=700, tier_cost=30

> An 80 nm BL pitch with a lateral 1T1C cell in every tier needs per-cell isolation along the WL direction. In Si/SiGe (Samsung, SK hynix) and replacement-channel schemes, that is a line or slot etch of ~40 nm CD through the whole ~4.5 um, 64-tier stack (AR ~110), beyond the ~50-70 production limit. That forces 2-4 decks, each repeating the HAR modules, alignment and staircase. A $700 cell base plus $30/tier, cheaper than a 200-layer NAND wafer for a far more complex cell, is not credible. At ~2x that cell-wafer cost, the pair is ~$8,400, cost ~$0.78/GB, and cost break-even moves from 16 to ~20 tiers.

*What would change the reviewer's mind:* A 3D-DRAM integrator flow for 64 tiers at 80 nm pitch in <=2 decks, with the cell wafer priced at <=$3k.

**Response — ACCEPTED-DOWNGRADE:** Valid. Per-cell isolation at 40 nm CD through ~4.5 um is AR ~112, beyond the ~50-70 production limit. The original $700 + $30/tier contained no HAR-module or staircase cost at all. Revised model: decks limited to AR 60 (2.4 um, ~34 tiers), so 64 tiers need 2 decks (128 need 4), at $800 per deck for the HAR modules, staircase and inter-deck plug. With +$200 of adders the 64-tier cell wafer rises $2,620 -> $4,420 (1.7x) and the pair $5,820 -> $7,797. 1T1C $/GB goes 0.68 -> 0.87 at this step (0.91 W2W / 0.92 D2W all-in), and cost break-even moves 16 -> 28 tiers. PROC's 2x case ($1,300/deck, ~$5.4k cell wafer) gives $1.03/GB. 128 tiers no longer beats 64 for 1T1C (the minimum is ~$0.87 at ~96 tiers), because decks scale with tiers. A self-isolating channel-last flow (ALD channel only in lateral recesses around each VBL) could avoid the slit, but it is unproven and not credited.

*Action taken:* Model: deck_cost 0 -> $800 with n_decks = ceil(tiers x 70 nm / (40 nm x 60)). This lowers the $/GB step from 0.36x to 0.62x DDR5 (together with the other corrections; decks alone add +$0.19/GB) and raises the 1T1C break-even to 28 tiers. Ask a 3D-DRAM integrator for a <=2-deck 64-tier flow as a raise-stage diligence item.

### RT-PROC-cell-wafer-foundry-03 — MAJOR — PROC — §0/§1 open merchant split (cell wafer from one maker, periphery from a logic foundry); §5 bonding partner

> The merchant model ships In/Ga/Zn-bearing, Cu-padded cell wafers into a bonding, CMP and thinning line that must also take logic periphery wafers. In and Ga are acceptors in Si and Zn is a deep-level contaminant, and logic foundries keep them off shared tools. So either the foundry builds a dedicated hybrid-bond line for a merchant customer, or a neutral third-party bond fab must exist with fab-grade <=0.05/cm2 cleanliness (the model's own input). Neither is costed. The null hypothesis, in-house CuA as Samsung and SK hynix already do, avoids the problem entirely.

*What would change the reviewer's mind:* A named bonding partner that accepts oxide-semiconductor wafers, with a contamination qualification (VPD-ICPMS <=1e10 at/cm2) and a bond price of <=$400 per pair.

**Response — ACCEPTED-MITIGATED:** Valid for the merchant model: In and Ga are acceptors in Si and Zn is a deep level, so logic foundries keep them off shared CMP/bond tools. Mitigation: (1) the cell wafer presents only Cu/SiCN at its bond face, because the oxide semiconductors are buried under the redistribution BEOL and the Al2O3/SiN barrier. Bevel and backside are encapsulated, and an edge-trim/bevel clean is done before shipping. (2) The open spec gains a contamination clause: VPD-ICPMS <=1e10 at/cm2 In/Ga/Zn on front, bevel and backside before entering a bond line, the same route foundries already use to admit eMRAM/FeRAM materials into BEOL. (3) D2W bonding runs in a packaging-class line used to non-Si materials. Bond cost is raised $400 -> $500/pair for a segregated or qualified line (+$0.01/GB). Partial rebuttal: 'CuA avoids the problem entirely' holds only for in-house memory fabs. Monolithic CuA at a logic foundry puts In/Ga/Zn into the foundry's own BEOL tools, which is worse than receiving an encapsulated wafer.

*Action taken:* Model: bond_cost_pair 400 -> 500. Add a VPD-ICPMS qualification of coupon wafers before bonding (line F). Add the contamination clause and encapsulation requirement to spec v0.1. The bonding-partner gate requires acceptance of oxide-semiconductor wafers.

### RT-CIRC-cell-wafer-foundry-03 — MINOR — CIRC — §2 bond grid (SA ~2.5 um2 in 28 nm logic) / sensitivity

> A 2.5 um2 SA in 28 nm logic is optimistic. It must deliver ECC-grade ~7 mV sigma with offset cancellation and restore through a 19.9 fF line and an oxide group-select switch (~50-100 kOhm at 40 nm IGZO, tau 1-2 ns). DRAM SAs are built on tailored periphery devices. The sensitivity row (1-5 um2 -> 3.8-4.8x) shows this matters, and the base case sits at the optimistic end.

*What would change the reviewer's mind:* A 28 nm SA layout with offset cancellation and write driver at <=2.5 um2, Monte Carlo offset <=7 mV.

**Response — ACCEPTED-DOWNGRADE:** Valid: the base sat at the optimistic end. A 28 nm offset-cancelled SA with ECC-grade ~7 mV sigma, a write driver and restore through an oxide group select is taken as 4.0 um2 (was 2.5). M rises 146 -> 196, Cbl 19.9 -> 25.8 fF and Cs 1.22 -> 1.62 fF. Density goes 1.81 -> 1.60 Gb/mm2 (-12%) and $/GB +13% (0.60 -> 0.68 W2W). At 5 um2 it is 1.50 Gb/mm2 (3.4x). Restore through a 100 kOhm oxide select: tau = 100 kOhm x 25.8 fF = 2.6 ns, so 5 tau = 13 ns against a ~32 ns tRAS. Feasible, but it sets tRAS; a 2x-wide selector halves it. Side benefit: with the larger SA the group is SA-limited up to 2.0 um, so the spec pitch relaxes to 2.0 um at no density cost (overlay budget 0.375 -> 0.50 um). Gain cells absorb the larger SA with a bigger cluster (M 205 -> 328) and keep 2.60 Gb/mm2.

*Action taken:* Model: a_sa_um2 2.5 -> 4.0 (1T1C density -12%, to 3.6x 1b). Lay out the 28 nm SA with offset cancellation and write driver, with Monte Carlo, on the MARGIN STACK MPW share (target <=4 um2, sigma <=7 mV). Spec pitch 1.5 -> 2.0 um.

### RT-CIRC-cell-wafer-foundry-04 — MINOR — CIRC — §5 step 11 sense-margin emulation (programmable Cbl + 0-2 fF bond emulator)

> The sense emulation on the MARGIN STACK MPW uses a lumped Cbl and a bond emulator. It leaves out the oxide 146:1 group-select switch (kickback, Vt spread, R_on) and the oxide wordline predecode, which are the electrical novelties of this split. Everything electrical that makes the split pay is therefore still unmeasured at the raise.

*What would change the reviewer's mind:* Oxide group-select and predecode TFTs on the coupon lot, read by the MPW, before the raise.

**Response — ACCEPTED-MITIGATED:** Valid. The lumped-Cbl emulator measured only what the model had already shown to be negligible (bond parasitics are 2% of Cbl). It left out the oxide group select (kickback, Vt spread, R_on) and the oxide WL driver, which are the electrical novelties of the split. Fix: build a 196:1 oxide group-select mux and the bootstrapped 1:8 sub-WL driver on coupon lots 1 and 2. Characterise them pre-bond by probe. In lot 2, read them through the bonds with the MPW SA board: charge injection, R_on distribution, Vt spread, signal versus programmed Cbl. Incremental cost ~$10k in masks and test (lines B and E). This gives the raise a measured electrical chain from cell to oxide select to bond to SA.

*Action taken:* Add oxide group-select and sub-WL-driver test structures to both coupon lots, read through the bonds by the MPW board before the raise. K5' now counts oxide-select effects in the 5% sense-margin trigger.

### RT-DEV-cell-wafer-foundry-02 — MINOR — DEV — §2/§5 model 'bond-anneal thermal dose as equivalent time at 85 C (Ea 0.58-0.72 eV)'

> Expressing a 250-350 C anneal as 0.09-37 years at 85 C assumes a single thermally activated process with the same activation energy at both temperatures. At bond temperatures, hydrogen release from SiCN/SiN, H transport through barriers and oxygen exchange in IGZO switch on, and none of these runs at 85 C at any rate. The Arrhenius map can understate bond-induced shifts and is no basis for the <=250 C spec.

*What would change the reviewer's mind:* Measured delta-Vt versus anneal temperature (150-300 C) on coupons, showing one activation energy that matches 85 C aging.

**Response — ACCEPTED-MITIGATED:** Valid. The single-Ea map (250 C x 2 h = 0.09-0.36 yr at 85 C) assumes one process. At bond temperatures, hydrogen release from SiCN/SiN, transport through barriers and oxygen exchange in IGZO switch on, and none of them runs at 85 C. The map is therefore at best a lower bound and is withdrawn as the basis for the <=250 C spec. The model now prints that caveat. The anneal temperature is set empirically: ΔVt versus anneal at 150/200/250/300 C, plus a 3 x 260 C reflow profile, on coupons. Only if one activation energy fits both the anneal series and 85 C aging is the Arrhenius extrapolation used for lifetime.

*Action taken:* Model s5 carries a RED-TEAM CAVEAT that the Arrhenius map is a lower bound. Add a 150 C point to the anneal split (was 200/250/300) and a reflow profile. The spec temperature becomes provisional until GATE 1.

### RT-DEV-cell-wafer-foundry-03 — MINOR — DEV — §4 #7 oxide-TFT WL predecode ('digital and offset-tolerant')

> An n-only oxide predecode passing ~3 V word-line pulses loses a threshold voltage per pass gate unless bootstrapped, and display-style bootstrapped IGZO gate drivers run at microsecond rates, not nanosecond. PBTI under 3 V at 85-125 C drifts the pass Vt by tens to hundreds of mV over life (the I-02936 critics' 50-100 mV), and that drift comes straight off the WL high level, and so off the write-'1' level and retention. Without the 1:8 predecode, WL bonds exceed the site budget at 1.5 um.

*What would change the reviewer's mind:* A 1:8 IGZO predecode delivering a 3.0 V WL with <=10 ns edges and <=50 mV level loss after 1,000 h at 125 C.

**Response — ACCEPTED-MITIGATED:** Valid on the premises: an un-bootstrapped n-only pass gate loses a Vt, and PBTI drift would come off the WL high. The micro-second speed of display gate drivers comes from pF panel loads and um-long channels, not from bootstrapping. Here the load is ~260 fF, so W ~0.8 um of short-channel ALD In2O3 at ~200 uA/um [UNVERIFIED-training drive] gives a 5 ns edge. With a bootstrapped gate (~5.1 V) and a silicon-defined FX level, the 50-100 mV drift appears as an ~8% R_on change, not a level loss. Without >=1:8 predecode, WL bonds exceed sites at 1.5-2.0 um, so this leg is necessary. The critic's would-change-my-mind test (1:8 IGZO predecode, 3.0 V WL, <=10 ns edges, <=50 mV loss after 1,000 h at 125 C) is adopted verbatim as a gate.

*Action taken:* Same redesign as CIRC-01 (bootstrapped SWD + VNWL clamp, dedicated TFT plane). Adopt DEV's test as K3b at M14, with stress running in parallel with the lot 1 bake.

### RT-DEV-cell-wafer-foundry-04 — MINOR — DEV — §5 thermal cycling (-40/125 C, 500 cycles) on a ~5 um multi-tier oxide stack

> The bonded interface is not the only weak plane. ALD laminates in the tier stack (Al2O3/HfO2/TiN/IGZO) often have adhesion energies of only a few J/m^2, comparable to an annealed bond. Post-bond thinning, Cu pad expansion (17 vs ~0.5 ppm/K for SiO2) and thermal cycling load the weakest interface. Delamination inside the stack would read as daisy-chain 'opens' and be blamed on the bond.

*What would change the reviewer's mind:* Four-point-bend adhesion >=5 J/m^2 on the tier stack, and FIB on every failed chain to locate the failing plane.

**Response — ACCEPTED-MITIGATED:** Valid. ALD laminates (Al2O3/HfO2/TiN/IGZO) can have Gc of a few J/m2. Thinning, the 17 vs ~0.5 ppm/K Cu/SiO2 CTE mismatch and thermal cycling load the weakest plane, and delamination inside the stack would read as bond opens. Fix: four-point-bend Gc on the tier-stack laminates (target >=5 J/m2). Add unbonded control daisy chains through the tiers that see the same thinning and cycling, so stack failures are separated from bond failures. FIB every failed chain (~25 lamellae, was 15). A delamination inside the stack is a cell-stack problem; it would also hit monolithic CuA. It is routed to the cell's owner and not counted against the bond.

*Action taken:* Add four-point bend (~$12k), unbonded control chains and FIB-every-failure to line F. Add GO item tier-stack Gc >=5 J/m2. The failure-attribution rule is in revised §9.

### RT-IND-cell-wafer-foundry-05 — MINOR — IND — §3 Adeia/Xperi DBI row; §6 FTO; §4 #9

> A product needs an Adeia DBI licence: Micron licensed in 2022, and AMD settled in March 2026 after litigation. That stacks a hybrid-bonding royalty onto an interface that earns no royalty of its own.

*What would change the reviewer's mind:* The Adeia licence cost quantified per wafer pair and shown to be <1% of the $5,820 pair cost.

**Response — ACCEPTED-MITIGATED:** Valid; now quantified, with honest uncertainty. Adeia terms are confidential, so the model books 1% of pair cost: $77/pair on the revised $7.7k pair, +~$0.01/GB (~1%). That is at the critic's <1% threshold but cannot be verified. The royalty also widens the split's premium over monolithic CuA by ~$1.2/tier at 64 tiers. The original Ziptronix DBI families were filed around 2000-2005 and expire before a ~2030 product [UNVERIFIED-training], so the exposure is to later improvement patents. R&D bonding at a licensed partner remains low-risk.

*Action taken:* Model: dbi_royalty_frac 0 -> 0.01 (included in the pair cost and the null-hypothesis premium). FTO: claims review of the post-2010 Adeia families before the raise. Bond via a licensed partner.

### RT-PROC-cell-wafer-foundry-04 — MINOR — PROC — §4 #4 anneal dVt; §2 GO '<=250 C anneal, dVt <=20 mV'

> Low-temperature (<=200-250 C) Cu/SiCN or oxide hybrid bonding gives up Cu interdiffusion and pad reliability unless a special Cu microstructure is used. Dielectric bonding also releases water and hydrogen at the interface (Si-OH condensation), directly above the top tiers' IGZO. The GO counts only anneal temperature, not interface water, and packaging reflows (~260 C, several times) add dose after the test.

*What would change the reviewer's mind:* A ToF-SIMS H profile of the top tier after bonding plus 3 x 260 C reflow, with dVt <=20 mV and Cu-Cu Kelvin resistance stable after 1,000 thermal cycles.

**Response — ACCEPTED-MITIGATED:** Valid. Low-temperature Cu/SiCN bonding gives up Cu interdiffusion and pad reliability unless the Cu microstructure is engineered. Interface water sits directly above the top tiers, and 3 x ~260 C reflows add thermal dose after the test. Fixes: (1) a nanotwinned (111) Cu split for <=200-250 C bonding; (2) Kelvin-resistance stability after 1,000 thermal cycles (was 500); (3) 3 x 260 C reflow is added before the post-bond ΔVt/retention and ToF-SIMS measurements; (4) the interface-water term is handled by the DEV-01 barrier and D-labelled hydrogen gate. A 260 C reflow drives H2 ~29 um in SiO2 [UNVERIFIED-training D], so it is a hydrogen-transport event, not just added dose.

*Action taken:* Add the nanotwinned-Cu split, 1,000-cycle Kelvin stability and 3 x 260 C reflow to the GO list and to K3'. The PROC test (ToF-SIMS after bond + 3 x reflow, dVt <=20 mV, Kelvin stable after 1,000 cycles) is adopted as written.

## charge-river — CHARGE-RIVER: buried-channel oxide CCD strings, scheduled like a drum for LLM weight and KV streaming (charge-river)

**Final status after red team: DOWNGRADED.** No physics kill, but the step-change claim shrinks. (1) The original two-ended regeneration had no return path; the fix needs a speculative deck-joint regenerator tier, or a 2x tighter CTE (0.9987 vs 0.9973) in a one-way 64-stage string. (2) Staircases cost ~29% of array area. (3) Realistic $25/plate plus the new tiers erase the cost advantage: $1.74/GB, 0.85x DDR5. Density falls from 3.6x to ~2.5x 1-beta and the cost leg is killed. The buried-channel factor weakens (0.18 -> 0.28) and RTN must be screened. P(pass) is lower and still hinges on imec's unread CTE definition.

*Revised verdicts* — Possible: YES (revised after red team): no law is violated and no physics kill was found, but three specs tightened. The buried heterochannel needs dEc >=0.5 eV at 4.5e12 cm-2 (0.3 eV leaves ~1.4 kT). Oxide-SF RTN must be screened at the 2-5 ns CDS timescale. Each segment must be injected at one end and sensed at the other. · Profitable: STEP CHANGE IF IT WORKS: DENSITY ~2.5x 1-beta (1.14 Gb/mm2; 2.2-2.7x over strip lengths; ~3.5x only with speculative staircase-free contacts), plus ~158x lower refresh/standby power and ~2.4-3x lower energy per useful bit than HBM3 including I/O, for a scheduled LLM streaming tier. Cost per bit is ~parity ($1.74/GB, 0.85x; 0.7-1.5x range), no longer a step change. Was 3.6x density and 2.1x cost. · Doable by this founder: PARTLY: $994k over 24 months can prove or kill the device physics: CTE >=0.9973 at 150 MT/s on an overlapping-gate reference, buried >=3x vs surface, RTN tails on >=1e4 nodes at real CDS timing, a regenerated 98-transfer loop at BER <=5e-10 and a 12-plate vertical coupon. It cannot prove AR-40 conformal heterostack decks, the deck-joint regenerator tier, the staircase or cost; those are $10-50M partner milestones.

### RT-CIRC-charge-river-01 — MAJOR — CIRC — §1 diagram / model holes_per_row 1 ('each hole on its own column line'), 512 SAs per 262,144-hole subarray, periph_eff 0.75

> The per-hole output and injection devices are not priced. Each hole has its own column line, so it needs its own floating diffusion, reset, source follower and select at the top end, plus a fill-and-spill injection structure at each end for regeneration: ~5-7 oxide TFTs per hole end in a 0.02 um2 footprint. PIXEL-STACK's area model needs 0.034 um2 for one SF/RST/SEL set even when shared by 2 bitlines, and still requires two sub-layers. 'No transistor per bit' holds, at ~10-14 TFTs per 64 bits. But the hole ends need amp tiers that periph_eff 0.75 and the $1,200 array base do not price, and the noise of those scaled SFs is what sets the 8 e- read noise.

*What would change the reviewer's mind:* A layout of the per-hole output and injection set at <=0.02 um2, or a sharing scheme with its timing and noise, added to the cost and density model.

**Response — ACCEPTED-MITIGATED:** Valid for the original two-ended design, which needed FD+RST+SF+SEL plus a fill-and-spill injector at each end (~10-14 TFTs per hole), none of it priced. Redesign: (1) Injection needs no per-hole TFT. It uses fill-and-spill (potential equilibration) from a per-column injection line, and the hole is selected by its strip's input-gate plate. The packet is set by the input-gate barrier and the well capacitance, not by the line. (2) Sensing happens only at segment tops. The FD is shared by 2 holes on one column line from adjacent strips, which are never read together. That gives one RST/SF/SEL set per 2 holes, i.e. 1.5 TFT per hole per sensing level, in a 0.054 um2 footprint (2 holes including slit share) against PIXEL-STACK's 0.034 um2 per set: one sub-layer with 1.6x margin. (3) This is the I-12302 principle: clamp the long column line and sense a short local strip with a gain FET. Dumping 313 e- onto a ~51 fF column would give ~1 mV, against 125 mV on a 0.40 fF strip (Micron planar plate-sensing patents narrow any claim). Priced in the model: array base $1,200 -> $1,500 for the top tier and bottom lines, +$500 for the joint tier (CIRC-02), C_FD 0.30 -> 0.40 fF, read noise 8 -> 10 e-. The floor moves 0.9970 -> 0.9973. The TFTs fit the footprint, so density is not reduced; their cost is inside the revised $1.74/GB.

*Action taken:* Model inputs revised (array_base_usd, c_fd_fF, sigma_read_e, joint_tier_usd). Add a shared-FD layout and a >=1e4-node FD-SF array to runs 1-2. State 1.5 TFT per hole per sensing level, and 0 at injection ends, in the dossier.

### RT-CIRC-charge-river-02 — MAJOR — CIRC — §1 'a sense node reads each puddle ... and re-injects' / §2.6 latency and endurance / model n_t = 3 x stages + 2

> A straight hole has no return path for regeneration. Readout is destructive at the segment end. Re-injection must happen either at the far end of the segment, which is mid-hole where no circuitry exists, or at the same end after the lap. The second option needs 32 bits of buffer per sense node: 1e6 nodes x 32 b = 32 Mb of latches, ~5-8 mm2 of 28-40 nm CMOS under a 9.9 mm2 die. It also needs a reverse lap, which doubles lap time (0.64 -> 1.28 us, so s must rise from 92% to ~96% for 40 ns) and plate cycles (1.5e11 -> 3e11, 30x beyond imec's >1e10). The model's 98-transfer read counts one input injection as if the input sat at the read end.

*What would change the reviewer's mind:* A U-shaped, pipe-connected string (Toshiba P-BiCS-style) or an explicit bidirectional scheme, with its buffer area, endurance and latency carried into the model.

**Response — ACCEPTED-DOWNGRADE:** Correct, and the most consequential circuit objection: the original 'sense and re-inject at each end' scheme has no physical return path. Modeled options (model section 4c): (a) LIFO bidirectional at each end: the worst bit sees 194 transfers; it needs a bottom sense node and a 32-bit buffer per node (~32 Mb, 5-8 mm2) and doubles plate cycles to 3e11. Rejected. (b) One-way 64-stage string, injected at the bottom and sensed at the top, decisions returned through the CMOS: 64 b/hole with no new tier, but 194 transfers raise the CTE floor 0.9973 -> 0.9987 (2x less deferral allowed). The lap becomes 1.28 us (s >= 96.1%; MoE + sparse attention averages 58 ns) and cycles 3e11; 1.18 Gb/mm2, $1.58/GB. (c) 'Joint': two 100-plate decks with an oxide-TFT regenerator tier at the deck joint. The lower deck is sensed at the joint and the upper deck injected there. It keeps 2 x 32 stages, 98 transfers, the ~0.997 floor, a 0.64 us lap and 1.5e11 cycles, at +$500/wafer and 4% TAV area. Bonus: ALD at AR 40 per deck and no CCD transfer across the deck joint. But no one has built a TFT tier between stack decks [SPECULATIVE]. A P-BiCS U-string doubles the loop per regenerator (128 stages at 200 plates), so it is worse. Base = (c), fallback = (b).

*Action taken:* Downgrade: 64 b/hole at ~0.997 now depends on a speculative deck-joint tier, and without it the GO line is CTE >= 0.9987 (the old STRONG-GO). The seed loop demo implements inject-at-one-end / sense-at-other with an FPGA/sky130 return path, and also runs a 194-transfer one-way loop to price the fallback. The joint tier is a $10-50M partner milestone.

### RT-DEV-charge-river-01 — MAJOR — DEV — §2.4 buried-channel factor 0.18x (f_it 0.6, eta_buried 0.9, eta_fz 0.4) at a 4.5e12 cm^-2 packet

> A buried channel protects the packet from interface traps only while the charge stays away from the interfaces. Silicon BCCDs limit full well to ~1e12 cm^-2 with the potential maximum ~0.1-1 um deep for exactly this reason. Here a 4.5e12 cm^-2 packet in a few-nm heterochannel raises the 2D Fermi level ~36 meV (m* 0.3) and drops ~0.14-0.2 V across a 2-3 nm cap (E = qn/eps ~6.8e5 V/cm), consuming most of a 0.3 eV offset, so the top of every '1' packet reaches the cap interface. A 90% removal of interface loss is not credible at the design point. Buried operation needs <=~1e12 cm^-2 (~70 e- at 25 nm plates), where the model's own partition-noise floor is above 0.999.

*What would change the reviewer's mind:* A planar heterochannel CCD at a matched 4.5e12 cm^-2 showing >=3x lower deferral than surface IGZO at 50 MHz and 25 C, plus a Poisson-Schrodinger solve placing the packet's charge >=2 nm from any interface at full fill.

**Response — ACCEPTED-MITIGATED:** Largely right at the dossier's stated spec. Electrostatics (model section 5a) at 4.5e12 cm-2: E_F sits 36 meV above the subband, 170 mV drops across a 2.5 nm cap (eps 12) and E0 is ~50 meV. That leaves a margin of 44 meV, i.e. 1.4 kT at 85 C (0.3 kT with a 3 nm cap), so the top of each '1' packet reaches the cap/dielectric interface, and +-0.05 eV composition swings move the estimated interface-loss removal between ~0.3 and ~0.9. Not fatal, because heterostructures hold far more sheet charge than doping-defined Si BCCDs once the offset is larger. At dEc 0.5 eV with a <=2.5 nm cap the margin is ~7.9 kT; at 0.4 eV it is 4.7 kT. Reported offsets: IGZO/beta-Ga2O3 0.71+-0.1 eV (XPS), high-In IGZO/IGZO ~0.4 eV, but In2O3/Ga2O3 only 0.09 eV. They are method- and composition-dependent, and Ga-rich caps conflict with the Ga-free aim. Model: eta_buried 0.9 -> 0.5, so the buried + fat-zero deferral factor goes 0.18 -> 0.28 until measured. The per-transfer reading of imec stays NO-GO (buried, 25 C: 0.88-0.99); the end-to-end reading stays GO (~75x margin).

*Action taken:* Raise the offset spec from >=0.3 to >=0.5 eV with a <=2.5 nm cap. Solve Poisson-Schrodinger at full fill by M2, with DEV's criterion that the charge sits >=2 nm from any interface. Measure XPS band offsets at Argonne on every stack before run 1. GATE 1 keeps 'buried >=3x lower deferral than surface at matched 4.5e12 cm-2, 50 MHz, 25 C', now scored on the overlapping-gate reference. Fallback: 2.5e12 cm-2 (173 e- packets) holds >=4 kT even at 0.3 eV but needs CTE ~0.999.

### RT-DEV-charge-river-02 — MAJOR — DEV — §2.1 and §2.3 (read noise 8 e-, Gaussian; raw-BER target 4.9e-10, Q = 6.11)

> The BER target is 5e-10 per decision, so read-chain tails matter at ~6 sigma, not 3.7. At end B the floating-diffusion source follower is an oxide FET whose RTN amplitudes are exponentially distributed. For a ~0.01 um^2 gate (eta ~1.4-4.2 mV, i.e. 2.6-7.9 e- at 534 uV/e-) with ~20% of devices carrying a fast trap, the 5e-10 quantile is ~19 eta, i.e. ~50-150 e-, against an eye half-width of ~100 e- at 65% survival. A Gaussian 8 e- term hides this. Silicon sensing at both ends would halve the bits per hole (density ~1.8x 1-beta).

*What would change the reviewer's mind:* A measured 1e-9 quantile of between-sample jumps <=30 e- on oxide FD-SF devices, or a design with silicon sensing at both ends and the density carried at 32 stages per hole.

**Response — ACCEPTED-MITIGATED:** Same physics as CIRC-04; accepted. With the revised 0.40 fF FD, eta 1.4-4.2 mV is 3.5-10.5 e-. With p_fast 0.2 and p_switch 0.25, the unscreened 1e-9 per-read step quantile is 62/124/186 e- against a ~95 e- eye half-width. So 2.8 mV moves the floor to 0.9993 and 4.2 mV fails at any CTE: a Gaussian 8 e- term does hide this. Mitigation without halving density: (1) screen and spare at 25 e- (<=1.8% of nodes at 4.2 mV; floor back to 0.9976); (2) a larger SF gate (eta scales as 1/WL, so a 100 x 200 nm gate halves it, fits the 2-hole footprint and, being bootstrapped, barely raises C_FD); (3) in-field re-screen during scrub; (4) the I-12627 dual-SF option. Silicon sensing at both ends is no longer needed, because the bottom and joint ends are injection-only in the new topology.

*Action taken:* Adopt DEV's test as a GO criterion: measured 1e-9 per-read between-sample step quantile <=30 e- on >=1e4 oxide FD-SF nodes at the 2-5 ns CDS interval, after sparing <=2%. New kill: >5% of nodes must be spared to reach 30 e-. Revival: bonded Si SF at >=1 um pitch with 8-hole FD sharing, or >=600 e- packets.

### RT-DEV-charge-river-03 — MAJOR — DEV — §4 #6 vertical integration (AR-80 hole, conformal ALD heterochannel); §5 'why planar first'

> The 3.6x density needs a buried core/barrier/cap heterostructure, each layer a few nm thick, conformal down an 8 um x 100 nm hole, holding a >=0.3 eV offset from top to bottom. No ALD multilayer oxide heterostructure has been shown at AR 80. Composition gradients with depth (ALD supercycle growth per cycle depends on precursor depletion) shift the offset and the local channel potential along the string, and a step at the two-deck joint acts as a barrier or pocket. At 313 e-, a 30 mV local potential error (~1 kT at 85 C) is enough to strand charge at 150 MT/s.

*What would change the reviewer's mind:* A >=16-plate vertical coupon with TEM/EDS showing <=5% composition variation over the hole depth, and per-stage CTE within 2x of planar.

**Response — ACCEPTED-DOWNGRADE:** Valid, and planar coupons cannot prove it. What changes: (1) The joint topology splits the stack into two 100-plate decks, each with its own ALD channel at AR 40, and removes any CCD transfer across the deck joint, because the joint is a sense/inject interface. That eliminates the joint step or pocket. (2) Robustness: at dEc >=0.5 eV a +-0.05 eV swing leaves >=6 kT of margin. Smooth top-to-bottom grading (50 mV over 100 plates = 0.5 meV per plate) is common to all strings and absorbed by per-depth DFE kernels and clock trims. Fat zero neutralises static pockets below 47 e-. An abrupt 30 mV (~1 kT) step is inside the ~2.5-3 kT barrier tolerance at a 6.7 ns dwell (model section 5b). (3) In-seed evidence: multi-cation ALD composition versus depth in AR 40-80 conformality test structures with TEM/EDX; planar composition-corner CCDs (+-10% In/Ga) to measure dCTE/dcomposition; and a 12-plate vertical coupon at low AR. CTE of a full AR-40 deck remains a partner milestone.

*Action taken:* Provability downgrade: the vertical leg can be bounded but not proven in the seed, so 'PROVABLE WITH $1M' falls to PARTLY. Add LHAR TEM/EDX, composition corners and the 12-plate coupon (~$80k). New kill: a top-to-bottom composition spread >10% that the corners show moves CTE by >5e-4.

### RT-IND-charge-river-01 — MAJOR — IND — §3 Honest position ('imec owns vertical oxide CCD memory'); §6 FTO; §7 imec program partners

> imec owns this direction: a planar 142-bit IGZO CCD (IEDM 2024), the first vertical IGZO CCD (IMW 2026), and a CXL-buffer framing with a '~5x 2D DRAM by 2030' claim. imec's core memory partners [training knowledge] reach that IP through its partner program, so the likely buyers already have a route around the startup. The startup's claims are narrowed on every side: buried heterochannel: oxide heterochannel TFT art from 2017-24; DFE sensing: LSST deferred-charge correction and RE43,639; placement: IBM 650 SOAP and ShiftsReduce. 'A cross-licence, not a fight' presumes the startup holds something imec's partners need.

*What would change the reviewer's mind:* A professional search of imec's 2022-24 oxide-CCD filings showing the buried heterochannel and the partition-noise DFE are unclaimed, plus a measured buried-vs-surface deferral improvement >=3x that imec's devices do not show.

**Response — ACCEPTED-DOWNGRADE:** Accepted as a defensibility downgrade, not a physics one. imec has planar (2024) and vertical (2026) oxide CCDs, and our original claims are narrowed on every side. Changes: (1) a professional FTO/patentability search of imec and SEL oxide-CCD filings 2022-26, budgeted at $20k (was $3-5k) and done before any provisional; (2) claims refocused on what the red team forced and imec has not published: the channel-last replacement-gate oxide CCD flow, inject-bottom/sense-top regeneration with a deck-joint regenerator tier, RTN-screened shared-FD readout with per-string deferral screening and sparing, a >=0.5 eV buried heterochannel at >=4e12 cm-2, and the lead-time placement controller; (3) a cross-licence needs a measured advantage imec lacks, i.e. buried deferral >=3x below surface at 150 MT/s. MISSION excludes business kills, so this lowers defensibility, not physical possibility.

*Action taken:* FTO by M2. GATE 1's buried >=3x result is the IP-bearing measurement. If FTO shows imec claims the buried heterochannel, drop claim #1 and file on the readout, regeneration and integration claims.

### RT-IND-charge-river-02 — MAJOR — IND — §2.2 Density and cost; §4 #7 Cost ceiling; models/charge-river.py yield_rel=0.8

> The cost ceiling is ~2.1x ($0.71/GB; range $0.42-1.47), because a CCD hole stores 64 bits against ~600 for TLC NAND. yield_rel = 0.8 for a never-built bonded 200-plate stack is a guess. On read-mostly weights, CHARGE-RIVER loses to High Bandwidth Flash (SanDisk/SK hynix, OCP spec Aug 2026, 512 GB per stack) at NAND-class $/GB. On random and KV traffic, it needs a scheduler and a front buffer that DRAM does not. A 2x-cheaper, non-drop-in, software-dependent tier is the Optane position, which failed commercially [training knowledge].

*What would change the reviewer's mind:* A buyer (accelerator vendor or hyperscaler) stating a price and latency spec for a write-endurant streaming tier between HBF and HBM that $0.71/GB at >=92% schedulability meets.

**Response — ACCEPTED-DOWNGRADE:** Accepted, and worse than stated. With all red-team corrections ($25/plate, 29% staircase, spares, joint tier, 100 nm slits) cost is $1.74/GB for the joint base (0.85x DDR5) and $1.58/GB one-way (0.93x); even at yield 0.95 it is $1.46/GB. The cost leg is withdrawn (PROC-04). What remains: density ~2.5x 1-beta per mm2 (capacity per die and stack), ~158x lower refresh/standby power and ~2.4-3x lower energy per useful bit than HBM3, at scheduled DRAM-class latency and high endurance. Against HBF it is positioned as the write-endurant KV-cache tier: NAND tolerates ~1e3-1e5 writes per cell [training knowledge], while KV cache is rewritten every token. yield_rel 0.8 stays as a mature-stage guess with 0.5-0.95 carried, and the parity conclusion holds across that range. The Optane analogy is a business risk, which MISSION excludes from kills.

*Action taken:* Restate the step change as density plus standby/refresh energy, not cost. In Q4, hold buyer-discovery talks (accelerator vendor, hyperscaler) for a write-endurant streaming-tier price/latency spec (no budget). Getting that spec is a raise-stage gate.

### RT-IND-charge-river-04 — MAJOR — IND — §5 Decisive experiment (planar e-beam CCDs at Penn/SNF/CNF); §4 #6 vertical integration deferred

> The seed builds planar e-beam CCDs in university nanofabs, while imec already has a vertical oxide CCD (3 word lines, >4 MHz). A planar result at 150 MT/s would be new physics. To a memory maker it would still read as behind imec on integration and ahead only on clock rate, with the hard part, a buried heterochannel deposited by ALD in a hole (show-stopper #6), deferred to a partner. Investors will ask why this should be a company rather than an imec partner asking imec to run the faster clock.

*What would change the reviewer's mind:* An 8-16-plate vertical coupon with the buried heterochannel inside the seed (via MIT LL or Albany), or a signed imec collaboration that leaves the startup clear ownership of its channel IP.

**Response — ACCEPTED-MITIGATED:** Partly accepted. Planar CCDs at 150 MT/s and matched sheet charge are necessary, because they measure the channel physics, but they are not enough to look ahead of imec. Change: the seed now also builds a 12-plate vertical CCD coupon: 4 three-phase stages; a W or Mo/SiO2 stack of ~0.5-0.7 um; ~250 nm holes at AR ~3; e-beam multi-depth contacts instead of a staircase; the buried heterochannel and a bottom injection contact. It targets >=50 MHz. A vertical, buried-channel result at ~10x imec's >4 MHz would lead on clock and channel. AR-40/80 decks remain partner work (MIT LL, Albany NY CREATES, imec). 'Why a company' is a business question that MISSION does not kill on. The honest answer is that the company's asset is channel, readout and integration know-how plus IP, most likely monetised through memory-maker partners.

*Action taken:* Vertical coupon at M14-20 ($50k plus shared fab hours, funded by merging run 2 and cutting contingency). Partner outreach after FTO and provisionals.

### RT-PROC-charge-river-01 — MAJOR — PROC — §1/§2.1 200 W/SiO2 plates; model INPUTS plate_thk_nm=25, slit_nm=60 ('plates are not replaced through it'), holes_per_row=1

> The plates are gate-first W: 200 x 25 nm = 5 um of W. At CVD-W stress (~1 GPa) that bows a 300 mm wafer by ~3 mm (Stoney), and even 200 MPa gives ~0.6 mm, against ~0.1-0.2 mm chuckable. The hole is 8 um deep at AR 80 through alternating metal and oxide. The per-row isolation slits are 60 nm wide through the same 8 um, AR ~130 in metal, while NAND slits are >100 nm wide and cut ONON. Switching to replacement metal only moves the problem: a WF6/H2 fill after the IGZO channel is deposited injects H and F into the traps that set CTE.

*What would change the reviewer's mind:* An 8 um metal/oxide stack (or two 4 um decks) with bow <=150 um and a <=60-80 nm slit etched through it. Alternatively, a replacement-metal flow with CTE unchanged (delta <5e-4) on planar coupons exposed to the fill chemistry.

**Response — ACCEPTED-MITIGATED:** Accepted for the gate-first spec. 5 um of blanket W at ~1 GPa bows a 300 mm wafer ~3 mm (Stoney: 3 x 1e9 x 5e-6 x 0.15^2 / (180e9 x 775e-6^2)), and a 60 nm slit through 8 um of metal is AR ~130. Redesign: adopt NAND's ONON stack with replacement W and slits >=100 nm, inheriting NAND's bow management (slit-segmented W, low-stress W, backside compensation, decks). Use a channel-LAST order: gate/blocking dielectric liner in the hole, sacrificial core, W replacement through the slits, an outgas anneal, then core removal and the ALD oxide channel at <=400 C. WF6/H2 then never touches the channel. Slit efficiency stays at 0.74 by moving to 2-row strips with half-pitch column lines (was 0.70 with 1-row strips and 60 nm slits). Two 100-plate decks halve each etch to AR 40.

*Action taken:* In run 1, expose planar coupons to the W-fill chemistry and thermal cycle, and split channel-last against channel-first (pass: dCTE <5e-4, PROC's criterion). Bow and slit etch on a real stack are partner milestones on a NAND tool set.

### RT-PROC-charge-river-02 — MAJOR — PROC — §8 'no staircase, 3-6 clock contacts'; §2.6 plate RC 'strap every ~100 um'; model INPUT holes_per_row=1

> Each plate is a separate buried W layer, so tying plates 1, 4, 7 ... into one clock phase means contacting every one of them. That requires a ~200-step staircase, or a 3-metal stack with selective recess, which is an even harder etch. With per-row slits, each one-hole-wide strip needs its own staircase: ~200 steps x 0.3 um, about 60 um at the strip end. RC (145 Ohm/um, 0.73 fF/um) limits a strip to ~100-200 um at 50 MHz, and a buried plate cannot be 'strapped' without yet another staircase. Overhead is therefore 60/(L+60), or ~23-38% of array area, cutting density from 1.62 to ~1.0-1.25 Gb/mm2 (2.2-2.8x 1-beta). The per-row slits cannot simply be dropped: sharing plates across 16 rows multiplies park-and-shift cycles 16x (1.5e11 to 2.4e12).

*What would change the reviewer's mind:* A plate-contact scheme with <=10% area overhead that keeps per-row (or <=4-row) clock groups, shown in layout with plate RC <=2 ns at 50 MHz.

**Response — ACCEPTED-DOWNGRADE:** Accepted; the dossier's 'no staircase, 3-6 clock contacts' was wrong. Every buried plate needs a contact step at each driven strip end. Strip length is RC-limited to ~100-200 um at 50 MHz, and RC per um2 does not depend on strip width, so wider strips do not help. At 0.3 um per step and 150 um strips, the 200-plate staircase costs 29% of array area (efficiency 0.71; 0.62-0.77 over 100-200 um), inside PROC's 23-38% band. With the other corrections, density falls 1.62 -> 1.14 Gb/mm2 (3.6x -> 2.5x; 2.2-2.7x over strip lengths). Per-row clocking is kept: 2-row strips with half-pitch column lines read both rows at once, so cycles are not multiplied. A [SPECULATIVE] staircase-free scheme, with three sacrificial plate materials and each phase contacted through its own trench after selectively recessing the other two (~3 um per end), would restore 0.98 efficiency (1.56 Gb/mm2, 3.5x). No such process exists.

*Action taken:* Downgrade: density -29% from the staircase alone. Staircase now in the model. The staircase-free phase contact is listed as a $10-50M-stage process development and IP candidate. A plate-contact layout with RC <=2 ns is a partner milestone.

### RT-PROC-charge-river-03 — MAJOR — PROC — §1 'end A: bonded CMOS wafer (sense amps, DFE)'; model INPUTS segments=2, c_fd_fF=0.30

> Two-ended strings need a sense node at the hole bottom. A hybrid-bond pad plus via is ~1-2 fF (the HOT-SIDE model uses 10 fF for bond plus BEOL via stack), and bonds cannot sit at the 141 nm hole pitch, so the bottom node must be multiplexed. A node shared by N holes carries N x junction/overlap capacitance plus wire. At even 8-16 holes, C_FD is ~1-2 fF: conversion gain falls 3-6x and read noise rises to ~25-50 e-, and the model itself says a 313 e- packet fails at 30 e-. That leaves two options. One is per-hole in-array FD/RST/SF/SEL oxide devices under the stack, contacted by an AR-80 bottom punch-through (NAND's hardest step). The other is one-ended strings at half the bits (~1.8x 1-beta).

*What would change the reviewer's mind:* A bottom-end readout with C_FD <=0.5 fF per <=8 holes, shown in layout, and measured read noise <=8 e- on a vertical coupon.

**Response — ACCEPTED-MITIGATED:** Accepted for the original two-ended design: a bottom node shared by 8-16 holes has C_FD 1-2 fF and 25-50 e- of noise. The redesign removes the bottom sense node. In both new topologies the hole bottom only injects, by fill-and-spill (potential equilibration) from a per-column line, and the packet does not depend on the line's capacitance. Low-noise FDs exist only at segment tops (the hole top, plus the deck joint in the joint topology), where a TFT tier can be patterned. There the FD is shared by 2 holes at ~0.40 fF, giving 10 e- of read noise. The hole bottom still needs a NAND-like bottom punch or backside exposure, plus per-column bottom lines at 70 nm pitch. Landing a deep hole on a line is an overlay risk, eased by AR-40 decks. CMOS goes under the array, or bonds only at subarray edges, never at hole pitch.

*Action taken:* Model: C_FD 0.30 -> 0.40 fF, read noise 8 -> 10 e-. The vertical coupon includes a bottom injection contact. GATE 2 item: measured read noise <=10 e- on the coupon's top FD.

### RT-PROC-charge-river-04 — MAJOR — PROC — §2.2 wafer cost; model INPUT per_plate_usd=10

> $10 per W/SiO2 plate pair is 2-4x below NAND's own per-layer economics. Choe/TechInsights' 10-15% cost gain from 64 to 96 layers implies 55-70% of NAND wafer cost scales with layer count, ~$20-38 per ONON pair at a $2.5-3.5k wafer [rt-PROC estimate], and CVD/PVD W layers cost more than PECVD SiN. At $25/plate the wafer is ~$8,250 and cost ~$1.11/GB, only 1.3x below DDR5. With objection 02's area overhead added, the cost advantage disappears.

*What would change the reviewer's mind:* A NAND-maker or reverse-costing estimate of <=$12 per metal/oxide plate pair, including deposition, etch share and metrology.

**Response — ACCEPTED-KILL:** Accepted. Searches this session found TechInsights' view that going from 64 to 96 layers cut cost only ~10-15%, and that 3D NAND bit cost follows ~0.7x per node and levels out at 300-400 layers. Neither gives a direct 200-layer per-layer cost. A metal/oxide pair (or ONON plus replacement W) carrying its share of HAR hole etch, slit etch, staircase litho-trim cycles and W fill plausibly costs what a NAND layer costs: base $25 (range $12-35). Model: the wafer goes $5,280 -> $9,050. That gives $1.74/GB (0.85x DDR5) for the joint base and $1.58 (0.93x) one-way. At $15/plate it is 1.09-1.22x. >=1.5x needs <=~$15/plate AND staircase-free contacts ($12: $0.91/GB, 1.63x). The cost-per-bit step change does not survive.

*Action taken:* Kills the cost-per-bit leg; the concept survives on density and standby energy. Revival condition: a NAND-maker or reverse-costing figure <=$12 per plate pair AND staircase-free phase contacts (>=1.6x). A $5k reverse-costing check is in the budget.

### RT-PROC-charge-river-05 — MAJOR — PROC — §5 step 3 (single-level W/Mo gates, 12-20 nm e-beam gaps, 16-256 stages, university fabs)

> Single-level CCDs with 12-20 nm e-beam gaps are notoriously defect-limited. A wide gap leaves a potential pocket or barrier that defers charge; a narrow one shorts phases. E-beam stitching and gap-CD variation over 256 stages will stack fab-defect deferral on top of oxide-trap deferral. GATE 1's NO-GO (<0.9934) could then reflect a university gap process rather than IGZO physics, and a pass on wide channels may not transfer. Production CCDs use overlapping multi-level gates for exactly this reason.

*What would change the reviewer's mind:* Overlapping two-level gates with an ALD inter-gate dielectric on run 1, or CTE measured on imec- or MIT LL-built planar structures as the reference for scoring the university variants.

**Response — ACCEPTED-MITIGATED:** Accepted. Run 1 adds overlapping two-level gates (W / ALD Al2O3 inter-gate dielectric / W, a standard university-fab build) as the process-clean physics reference. GATE 1 PASS/FAIL, including buried versus surface at matched charge, is scored on those structures. The single-level 12-20 nm e-beam-gap structures are scored separately as the vertical-geometry proxy (CTE versus gap width), so a NO-GO now requires failure on the overlapping-gate reference. Precedent: MIT LL's fast single-poly CCDs show single-level gates work when gaps are narrow and controlled. The vertical gap is a deposited film, more uniform than an e-beam gap.

*Action taken:* +1 mask and ALD level in run 1 (inside the revised $50k materials and $35k e-beam lines). GATE 1 rule rewritten. Ask MIT LL or imec for reference structures to cross-calibrate.

### RT-CIRC-charge-river-03 — MINOR — CIRC — §2.2 table 'core read energy 0.072 pJ/bit vs HBM 3.44 pJ' / model eta_rec 0.5

> The energy comparison is not like for like. The 0.072 pJ/bit core read excludes I/O, while HBM's 3.44 pJ includes it. The 45 fJ/bit shift energy also assumes every bit of a 32-stage lap is consumed. A random single-bit access pays the whole lap, ~1.4 pJ per useful bit. 50% clock-energy recovery (eta_rec) at 50 MHz across per-row clock groups is unsourced: on-chip LC resonance would need uH-class inductors, so stepwise charging is the realistic route.

*What would change the reviewer's mind:* Energy per useful bit for measured trace mixes, with I/O and a specified clock-recovery circuit included.

**Response — ACCEPTED-DOWNGRADE:** Accepted. The like-for-like model adds an HBM-class 1.0 pJ/bit I/O term and cuts clock recovery from 50% to 33%: 3-phase charge sharing or 3-step stepwise charging, since on-chip LC would need uH inductors. Streaming then costs 1.09 pJ/bit including I/O. A random 64 B access laps a whole clock strip (150 um x 2 rows = 2,121 holes) for 512 useful bits: 15.9 pJ per useful bit plus I/O, worse than a DRAM row activation. CIRC's per-hole ~1.4 pJ is if anything optimistic. Weighted by the 0.5-2% random floor this gives 1.17-1.40 pJ per useful bit, ~2.4-2.9x below HBM3's 3.44 pJ, not the ~48x a core-versus-total comparison implied. The scrub-versus-refresh saving falls from 191x to ~158x with the lower recovery.

*Action taken:* Energy claim restated as ~2.4-3x per useful bit including I/O, with the refresh/standby step at ~158x. The simulator reports energy per useful bit on measured trace mixes. The sky130 chip carries a 3-step stepwise clock-driver test.

### RT-CIRC-charge-river-04 — MINOR — CIRC — §2.3 CTE floor / model sigma_read_e 8 (Gaussian)

> The 4.9e-10 per segment-read target is a ~6.1 sigma decision, made on ~1e6 oxide source followers. With exponential RTN amplitudes, the worst SFs (q/(Cox*W*L) ~1.4 mV at 100 x 100 nm and 3 nm EOT; 1e-6 quantile ~14x the mean, ~19 mV, ~48 e- on 0.4 fF) lose about half the eye. The dossier's own sensitivity says 30 e- fails at any CTE. Sense-node screening and sparing, each spare costing ~512 holes x 64 bits, belong in the GO and the density figure.

*What would change the reviewer's mind:* A measured SF noise distribution over >=1e4 nodes and a sparing overhead added to the density figure.

**Response — ACCEPTED-MITIGATED:** Accepted and modeled (model section 4b). The eye at the floor is 191 e- wide (half-width ~95 e-). RTN model: exponential steps with eta 1.4/2.8/4.2 mV (3.5/7.0/10.5 e- at 401 uV/e-); 20% of nodes have a fast trap, which switches between CDS samples with probability 0.25. Unscreened floors are 0.9975 / 0.9993 / fails at any CTE. Screening out nodes with a measured step >25 e- spares 0% / 0.56% / 1.8% of nodes and returns the floor to 0.9975-0.9976. With 2-hole FD sharing a spare costs 2 holes x 32 b, not 512 holes x 64 b, and the overhead is carried in spare_frac 0.03 (2% strings + 1% nodes), which costs 3% of density. Insurance against traps activating after the screen, from the I-12627 principle: two independent SFs per FD, averaged, with a disagreement flag that re-samples the still-held FD. The per-read event probability falls 5e-2 -> ~3e-3 and the amplitude tail enters squared, if trap sites are independent.

*Action taken:* Add an RTN node array: >=1e4 oxide FD-SF cells with on-die oxide sample-and-hold at the real 2-5 ns CDS interval, >=1e7 samples per node ($15k). New GO line: 1e-9 per-read step quantile <=30 e- after sparing <=2% of nodes. In-field re-screen during scrub. Sparing included in density.

### RT-DEV-charge-river-04 — MINOR — DEV — §2.2 plate stack (25 nm W plates, 15 nm SiO2 inter-plate gaps, EOT 5 nm); CTE model

> Single-level gates separated by 15 nm gaps (gap/gate 0.6, gap/EOT 3) leave the channel under each gap controlled only by fringing. That forms potential barriers or pockets that strand charge at high clock rates and low signal, which is why silicon CCDs use overlapping gates. The CTE model has no gap term. The planar run's 12-20 nm e-beam gaps will see it, but the vertical geometry (curved channel, deposited gap oxide) differs.

*What would change the reviewer's mind:* 2D/3D electrostatics of the vertical gap showing a barrier or pocket <0.5 kT at full and fat-zero fill, confirmed by planar CTE versus gap width.

**Response — ACCEPTED-MITIGATED:** Accepted that the model lacked a gap term; it now has one (model section 5b). Barrier: escape time tau_b = tau_diff(40 nm) x exp(dV/kT). Charge stranded after a 6.67 ns dwell stays below 20% of the deferral budget (3.6e-4) up to ~2.5-3 kT (65-90 mV), so DEV's <0.5 kT criterion is stricter than the transport needs. Pocket: a static pocket smaller than the fat zero (47 e-) stays permanently filled and causes no data-dependent loss. With ~0.014 fF of gap coupling that covers pockets several hundred mV deep. The residual risk is signal-dependent pockets. Evidence: MIT LL's fast single-poly Si CCDs work with narrow gaps, and the vertical gap is a deposited oxide film, more uniform than an e-beam gap.

*Action taken:* By M2, 2D/3D electrostatics of the curved vertical gap at full and fat-zero fill (pass: barrier <=2 kT, signal-dependent pocket <=5 e-). Planar CTE against gap width 12-20 nm. The 12-plate vertical coupon measures the real deposited gap.

### RT-DEV-charge-river-05 — MINOR — DEV — §2.3 worst-string factor k_ws = 1.5 over ~1e8 strings

> With ~1e8-1e9 strings per die, the worst-string factor is set by rare 'bright' defects (a pinhole, an In-rich cluster, a gap pocket), as with trap-dominated columns in CCD imagers. Poisson spread of ~1e2-1e3 traps per string alone gives only ~1.1-1.2. The 1e-8 quantile cannot come from a few hundred narrow planar channels, and the model shows that k_ws 3 alone moves the floor to ~0.9985.

*What would change the reviewer's mind:* A string-screening and spare-mapping scheme sized from a measured 1e-4 tail and extrapolated with a defect model, with the spare cost carried into density.

**Response — ACCEPTED-MITIGATED:** Accepted. k_ws is redefined from a natural tail to a screen threshold. Every string's deferral is measured at test and re-measured each scrub (per-string DFE kernels are extracted anyway), and strings above 1.5x median are mapped out, as NAND bad blocks are. Spare cost = P(bulk lognormal > 1.5x) + rare-defect share. For bulk sigma_ln 0.10 / 0.15 / 0.20 (Poisson spread of 1e2-1e3 traps plus CD spread) that is 0.003% / 0.34% / 2.1%, plus ~0.1-1% rare defects. It is carried as 2% strings inside spare_frac 0.03. If sigma_ln reaches 0.3, spares at 1.5x would be 8.8%; then run k_ws 2 (1.0% spared, floor 0.9973 -> 0.9980). The 1e-8 tail is a yield/sparing number measurable only on Gb-class arrays.

*Action taken:* String-screen and spare-map architecture added; spare overhead included in density. The seed measures the bulk distribution to the 1e-3-1e-4 quantile on narrow channels and the vertical coupon. A defect-model extrapolation to 1e-8 is a raise-stage deliverable.

### RT-IND-charge-river-03 — MINOR — IND — §2.4 'Step 0 is a $35 paper'; FINAL_CONCEPTS EV 40 (P=2), tie with LEAN broken on step size

> The rank-7 EV (P = 2) and the dossier's P(pass) of 15-25% vs >=50% both hinge on whether imec's 'CTE >98%' is per transfer or end-to-end. That $35 paper has not been read. Until it is, the EV ranking against LEAN ARRAY MODULE (tied at 40 and broken on step size) is unsupported in either direction.

*What would change the reviewer's mind:* Read imec's IEDM 2024 and IMW 2026 papers and restate P using the CTE definition they give.

**Response — ACCEPTED-MITIGATED:** Accepted. A search this session confirmed the record: IEDM 2024 paper 37-6, R. Kishore et al., DOI 10.1109/iedm50854.2024.10873539. The public abstract still says only 'CTE >98%' (plus 'multilevel capability'), so the definition is still unknown. P is therefore restated conditionally, not as a point: P(GATE 1 pass) ~10-20% if imec's 98% is per transfer (lower than the earlier 15-25%, because the buried factor is now 0.28 and the floor rose to 0.9973), and ~40-50% if end-to-end (~75x CTE margin on the trap-kinetics carry-over, but the buried >=3x condition is now harder). Until the paper is read, this dossier's P should not break the EV tie with LEAN ARRAY MODULE in either direction.

*Action taken:* Buy and read the IEDM 2024 and IMW 2026 papers in week 1 (M0), before any spending, and restate P. If the 98% is per transfer and imec shows <2x from a buried channel or fat zero, apply kill criterion 1.

### RT-PROC-charge-river-06 — MINOR — PROC — §2.3 k_ws=1.5; §4 #6 'conformal ALD heterochannel' in an AR-80 hole

> A buried heterochannel (IGO/IGZO core, barrier and cap) grown by multi-cation ALD supercycles in an 8 um, AR-80 hole will grade in composition from top to bottom, because the In, Ga and Zn precursors stick and deplete differently. The >=0.3 eV band offset and the trap DOS then vary along the string. That variation sets the worst-string factor k_ws (<=1.5 to PASS; k_ws 3 alone moves the floor to ~0.9985), and planar coupons cannot measure it.

*What would change the reviewer's mind:* TEM-EDX composition plus CTE (or TFT trap DOS) at the top, middle and bottom of an AR >=40 hole, within +/-10% composition and k_ws <=1.5.

**Response — ACCEPTED-MITIGATED:** Accepted that planar coupons cannot measure it. Two distinctions reduce its bite. First, smooth top-to-bottom grading is common to every string at a given depth: it shifts the median, which per-depth DFE kernels and clock trims absorb, rather than adding to k_ws, which is string-to-string. Second, at dEc >=0.5 eV a +-10% composition swing (~+-0.05 eV) still leaves >=6 kT of buried margin. Abrupt local variation does feed k_ws, and that is screened and spared (DEV-05). In-seed measurements: TEM-EDX composition at the top, middle and bottom of AR 40-80 conformality test structures coated with our multi-cation ALD supercycle (PROC's +-10% criterion), plus planar composition-corner CCDs (+-10% In/Ga) to measure CTE and offset sensitivity. Together they turn the measured grading into a predicted vertical k_ws contribution. The joint topology halves the per-deck AR to 40.

*Action taken:* ~$30k for LHAR test chips, TEM/EDX and corner splits. GATE 2 adds: composition within +-10% top-to-bottom at AR >=40, and predicted k_ws <=1.5.

## diode-tower — DIODE-TOWER: two stacked transistors and 16-64 wrapped linear-capacitor tiers per pillar, steered by per-tier oxide Schottky diodes and read by a double-sampled in-hole gain FET (diode-tower)

**Final status after red team: DOWNGRADED.** No objection is fatal, and the engineering objections (plate RC, top of pillar, stack process, readout noise, coupling) all have priced redesigns: wrapped tier on Mo replacement plates, replacement-first flow, stacked 2T top, 300 um centre-driven segments, 0.3 V guard. The downgrade comes from three things. (1) The only contact class that met the barrier bar, AgOx, cannot survive the process, and no process-integrable anode (RuO2, MoOx, WOx) has an IGZO datum. (2) The bottom-anode interface (0.1-0.3 eV) and Poole-Frenkel/TAT leakage (+0.12-0.22 eV) could widen the barrier gap from 0.15-0.2 eV to 0.24-0.71 eV. (3) Once yield, per-tier and top-of-pillar costs are priced, $/bit at 64 tiers rises from 0.35x to 0.55x (about parity with a 2032 incumbent), the smallest step in the portfolio. EV falls from 45 to ~16 (S2 x P2 x D4). The concept stays alive as the two-terminal per-tier-device hedge, funded through the shared oxide coupon run until Gate A.

*Revised verdicts* — Possible: Yes, conditionally, with lower confidence. No law is violated. It needs a process-integrable (RuO2/MoOx/WOx), bottom-anode, etch-back-formed contact at >=1.06-1.11 eV thick-film-equivalent, or 1.18-1.33 eV if Poole-Frenkel-limited, with sigma <= 0.05 eV in a 15 nm shell (budget 928 aA per ring at 85 C). No integrable anode has an IGZO datum; RuO2/IrO2 on GaN (1.43-1.48 eV) and Pd on a-HIZO (1.40 eV mean, but sigma 0.14 eV) show high barriers exist on wide-gap and amorphous oxides. · Profitable: Density: ~3.9x 1-beta at 64 tiers (2.0x at 32; parity at 17). Bits/$: ~1.8x at 64 tiers ($/bit 0.55x at tier yield 0.995; 0.45x at 0.998, 0.76x at 0.99; 0.73x at 32 tiers). 2 transistors per 30-61 bits. Roughly parity vs a 2032 incumbent unless >=96 tiers at >=0.998. No energy step unless 1 s retention. · Doable by this founder: Partly (less than before). A ~$260k Stage A ($170k without the bench) settles the diode on vertical-recess, ring-sized, bottom-anode coupons, plus RTN and drift, by M7. A 4-tier wrapped replacement-first stack fits a $960k / 24-month plan. Not provable inside $1M: >=32-tier yield, the AR >=30 replacement hole etch and the full-pitch stacked 2T top. P(pass) ~5-10% [ESTIMATE].

### RT-CIRC-diode-tower-01 — MAJOR — CIRC — §2.1 signal (sigma_cds_mV 7) / §4 #6 / §2.5 'CDS residual vs maximum tiers'

> The gain-FET residual is inconsistent with the portfolio's own model. sigma_cds_mV = 7 is the 'midpoint of the concept's 5-10 mV'. PIXEL-STACK's model computes a 14.7 mV readout residual for a 100 x 100 nm oxide SF (0.01 um2), which is close to an in-hole FET in a 60 nm hole (pi x 60 nm x 60-100 nm = 0.011-0.019 um2). The RTN correction in RT-CIRC-pixel-stack-02 pushes that to ~24-35 mV. Per §2.5, 15 mV caps the back-wall tower at 14 tiers, below the 18-tier parity. The 1.9-3.9x density claim survives only on the wrapped capacitor (0.725 fF, +1 deposition per tier) or a bonded Si gain FET, so the base case should move there with its cost.

*What would change the reviewer's mind:* A measured post-CDS residual <=7 mV on an in-hole-sized oxide gain FET at 85 C, or §2.2 restated on the wrapped-Cs cell with its density and $/bit.

**Response — ACCEPTED-MITIGATED:** Partly a units mismatch, but the substance holds. The dossier's 7 mV was an rms sigma, used as signal/2 >= 3.72 x 7.33 mV, i.e. ~26 mV of budget. PIXEL-STACK's 14.7 mV (24-35 mV after the RTN correction) is already a 3.72-sigma + RTN + coupling quantity, so '15 mV caps the tower at 14 tiers' maps one onto the other wrongly. Re-run in PIXEL-STACK units (sigma_SF 2.5 mV rms + deterministic 1e-4 RTN tail + 1.2 mV coupling): the back-wall cell reaches 79/52/39/22 max tiers at RTN 13/20/25/35 mV. 32 tiers survives a 20 mV tail; 64 tiers fails above ~13 mV, so the critic's conclusion holds for the 64-tier claim. The base cell is moved to the wrapped capacitor, made physical as Mo/poly/Mo with a 5 nm plate pull-back: Cs 0.594 fF (not 0.725), 65 nm tier, priced at $38/tier. It reaches 156/110/89/60 max tiers at the same RTN values; at 20 mV, z = 14.1 at 32 tiers and 8.3 at 64, and the allowed residual is 58/40 mV at 32/64 tiers. A longer in-hole gain FET is a further lever (RTN ~1/L, gate C ~L): 206 tiers at L = 100 nm. A bonded Si gain FET is not a real fallback at a 121 nm per-pillar pitch; it is replaced by a sequential Smart-Cut c-Si layer.

*Action taken:* Base = wrapped cell (model cell_wrap True, density/cost restated). G5 rewritten in PIXEL-STACK units: <=40 mV for 64 tiers, <=58 mV for 32. Add the 1e-4 RTN distribution on >=65k oxide FETs of <=0.01 um2 at 85 C with a ~15 ns CDS gap (L 50/100 nm splits) on the shared PIXEL-STACK/MARGIN STACK lot. New kill 6 at M9 (>50 mV at both lengths). Kill 11 rewritten (>58 mV kills; 40-58 mV caps at 32-48 tiers).

### RT-CIRC-diode-tower-02 — MAJOR — CIRC — §2.4 write / §3 delta 2 'V_f offsets largely cancel' / §4 #3 'V_f moves ~0.1 V from 0 to 85 C'

> Cross-temperature V_f does not cancel. A level is stored as V_pillar,write + V_f - swing and read by dumping to V_pillar + V_f, so V_f cancels only when write and read happen at the same temperature. The dossier itself says V_f moves ~0.1 V between 0 and 85 C. A write at 85 C read at 25 C shifts the dumped charge by Cs*dV_f: 0.27 fF x ~70 mV / 1.27 fF = ~15 mV of pillar signal. That is ~35% of the 42 mV half-margin at 32 tiers (z 5.8 -> ~3.7) and more at 64 tiers (half-margin ~30 mV). The reference tier is written at a different time, so it does not cancel this either.

*What would change the reviewer's mind:* Coupon floating-node read error versus write and read temperature difference (+/-60 K), or a temperature-tracked reference scheme with its scrub rate.

**Response — REFUTED:** The objection assumes data written at 85 C and read at 25 C. In this cell every read is destructive, and every refresh is a dump read plus a clamp write-back, so each level is re-written with V_f at the current temperature at least once per refresh interval. The write/read temperature difference is therefore bounded by die slew x interval, not by the +/-60 K range. Model: clamp V_f tempco 1.33 mV/K (1.10 eV contact, I_end). At 64 ms and 10 K/s (the LPDDR MR4-polling example rate [UNVERIFIED]), dT = 0.64 K and dV_f = 0.8 mV, giving a pillar offset of 0.28 / 0.19 mV at 32 / 64 tiers (0.4% of the half-margin). Even at 100 K/s the offset is 2.8 / 1.9 mV (4%). In 1 s refresh mode at 10 K/s it is 4.4 / 3.0 mV (6.6%). The critic's 60 K case (26 / 18 mV in the wrapped cell) needs data left unrefreshed while the die cools 60 K, which a DRAM never does. The reference tier is refreshed in the same interval, so it tracks too.

*Action taken:* Model now carries dV_f = slew x interval x tempco x Cs/(Cs+Cp) as a deterministic readout term. The coupon still writes and reads floating nodes at temperatures up to +/-60 K apart, to confirm the clamp tempco and the model. In 1 s (G2) mode the controller keeps the reference tier refreshed within the same interval.

### RT-CIRC-diode-tower-03 — MAJOR — CIRC — §2.4 'page = plate segment, slits every 4 rows' / §1 'CMOS under array: ~1.8-2 V plate drivers'

> Plate drivers trade off against plate RC, and neither is in the model. A 25 nm TiN plate perforated by ~101 nm hole-plus-ring openings at 121 nm pitch (20 nm webs) has an effective R_sq of ~120-240 Ohm/sq. Each plate carries ~33 nodes/um x 0.27 fF plus fringe, ~12 fF/um. A 4-row (0.48 um) segment 50 um long then has an Elmore delay of ~3-6 ns, but at 200 um it is ~45-90 ns. Keeping 50 um segments at 32 tiers needs ~1.2M plate drivers/mm2, or 0.85 um2 each, for ~2 V thick-oxide drivers that need >=2-4 um2 with level shifting, plus a 32-step staircase at every segment. array_eff 0.55 is borrowed from A1 and prices none of this.

*What would change the reviewer's mind:* A plate-driver and staircase floorplan whose segment length meets <=10 ns RC at 32 tiers, or a demonstration of the I-11544 Vt-coded tier decoder.

**Response — ACCEPTED-MITIGATED:** Reproduced. TiN 25 nm at ~150 uOhm.cm is 60 Ohm/sq; perforated by 101 nm openings at 121 nm pitch it is ~205 Ohm/sq (Maxwell-Garnett mesh). With ~0.23 fF of load per node, a 4-row segment has an Elmore delay of 4.0 ns at 50 um but 65 ns at 200 um. Keeping 50 um segments at 32 tiers needs 1.18M drivers/mm2 (0.85 um2 each) and 22% / 45% staircase overhead at 32 / 64 tiers: unworkable, as the critic said. Redesign: Mo replacement plates (25 uOhm.cm at 10 nm) in the wrapped tier. The two Mo layers are perforated only by the 60 nm hole (+5 nm pull-back), so the mesh is 21 Ohm/sq. With 8-row, 300 um segments driven from the centre, RC is 7.2 ns at the wrapped load (0.44 fF/node). That needs 0.10M drivers/mm2 at 9.6 um2 each, enough for a ~2 V thick-oxide driver or a NAND-style pass gate fed by global plate drivers. The page is ~19.8k pillars (2.4 KB). The staircase is now priced in density: 0.35 um/step per segment adds 3.7% / 7.5% at 32 / 64 tiers. Net density is 1.98x / 3.88x (was 1.94x / 3.94x), because 8-row slits halve the slit overhead.

*Action taken:* Model: rows_per_plate 4->8; seg_len_um 300 centre-driven; stair_step_um 0.35 in the footprint; new section 12b. A plate-driver/pass-gate floorplan is part of the M0-6 design work. Binary-chop multi-depth contacts are listed as the staircase-area reducer; the I-11544 Vt-coded decoder stays optional.

### RT-DEV-diode-tower-01 — MAJOR — DEV — §4 #1 paths (AgOx-class anodes, 1.0-1.2 eV on ZnO) and #8 anode stability; §5 anode matrix

> AgOx on crystalline ZnO is the only contact class in the dossier that reaches the 1.07-1.12 eV low-field bar, but silver oxide is thermally unstable. Reported decomposition of Ag2O to Ag + O2 starts near 170-200 C in gas ambients and is essentially complete by ~400 C (logged in rt-DEV.jsonl). In the tower the anode goes down first and then sees IGZO ALD, every later tier and <=400 C anneals, so its barrier reverts toward a Ag/IGZO contact, and Ag diffuses fast through thin oxides (risking shorts through 5.5 nm ZrO2 and 15 nm IGZO). That leaves PtOx, IrOx, RuOx and MoOx, none shown at >=1.0 eV on amorphous IGZO.

*What would change the reviewer's mind:* Any anode on IGZO that keeps >=1.07 eV with sigma <=0.05 eV after the cumulative thermal budget of a 32-tier build (not one 400 C anneal), with no Ag detected in the ZrO2 by ToF-SIMS.

**Response — ACCEPTED-DOWNGRADE:** Agreed on the main point. Ag2O partly dissociates by 300 C and fully decomposes by ~400 C (PCCP 2001; RSC Adv 2012: stable in gas only below ~170 C), and Ag diffuses through thin oxides. AgOx was the only contact class at >= the 1.07 eV low-field bar, so its loss matters. AgOx moves to planar diagnostics only. One correction: in the hole flow all tiers are built in one sequence, so the anode sees IGZO ALD + core + top 2T + BEOL, one <=400 C budget rather than 32 tier anneals. The coupon will reproduce that cumulative schedule (IGZO ALD <=300 C, 2 x 350 C, 400 C 1 h), not one anneal. Consequence: the barrier gap is no longer '0.15-0.2 eV with a known contact class just above it'. It is 0.14-0.41 eV from the best IGZO datum of any kind (Pt, itself non-integrable), and no integrable anode has been measured on IGZO.

*Action taken:* Anode matrix restricted to RuO2 (Ru node ring, in-situ O3 re-oxidation), MoOx, WOx and an area-selective IrO2 liner, on IGZO / Ga-rich / a-Ga2O3 shells. ToF-SIMS on every G1-passing split. Cumulative thermal schedule. Downgrade: P 3 -> 2 (pass chance ~5-10% [ESTIMATE]), lowering provability, not the step-change if it works.

### RT-DEV-diode-tower-02 — MAJOR — DEV — §2.3 leakage model (thermionic + image force + TFE + Gaussian patches); Q2 2027 gate '>=1.0 eV low-field'

> Reverse leakage in wide-gap oxide and nitride Schottky diodes is usually not thermionic-limited. ZnO and GaN diodes commonly leak orders of magnitude above thermionic theory through trap-assisted tunnelling and Poole-Frenkel emission via deep states, and a-IGZO carries ~1e16-1e18 cm^-3 eV^-1 of V_O-related deep states. At the 0.87 MV/cm anode field of a depleted 15 nm shell, Poole-Frenkel lowering is ~2x the image-force term, ~0.2-0.35 eV. A barrier extracted by I-V-T and Werner-Guttler on thick diodes therefore does not predict ring leakage, and anodes may be down-selected on the wrong metric.

*What would change the reviewer's mind:* Ring-sized thin-shell diodes whose reverse current at 0.7 V tracks the thermionic prediction within 10x over 25-125 C (an activation energy equal to the barrier), on coupon structures (b) and (c).

**Response — ACCEPTED-DOWNGRADE:** Valid and supported: a JAP 2006 study of single-crystal ZnO Schottky diodes found reverse current dominated by Poole-Frenkel, with ~5x local field enhancement, and GaN reviews report PF + TFE. Deep V_O states in a-IGZO make the same likely. Model sensitivity (PF lowering = 2x the image-force term at the hold field): the G1 thick-film bar rises from 1.06-1.11 eV (thermionic) to 1.18-1.33 eV. A hypothetical 1.20 eV RuO2/IGZO contact goes from 0.56-2.6 s to 1-82 ms tail retention. A thick-film I-V-T / Werner-Guttler barrier therefore cannot down-select anodes. Field levers reduce PF too: the 20 nm shell bar is 0.99-1.02 eV thermionic, and the 80 nm escape geometry 0.97-0.98 eV.

*Action taken:* Gate A and the Q2 down-select are judged on measured ring-sized thin-shell leakage (structures b, c, and the new vertical coupons e) at 85 C / 0.8 V, plus its activation energy over 25-125 C. The critic's test (Ea = barrier, within 10x of thermionic) is reported as a diagnostic. The model adds the PF case (section 12f-g). Downgrade: worst-case bar +0.12-0.22 eV, folded into the P 3 -> 2 downgrade.

### RT-DEV-diode-tower-03 — MAJOR — DEV — §5 step 2 ('anode below the IGZO, as in the tier')

> The literature's 0.9-1.2 eV barriers on IGZO and ZnO come from top contacts sputtered in O2 onto the semiconductor, which oxidises the interface and removes V_O donors. In the tower the anode is underneath, and IGZO is grown on it by ALD with O3/H2O and metal-organic precursors at 150-300 C. That reduces noble-metal oxides (PtOx, AgOx, RuOx) and leaves a V_O- and H-rich interfacial layer that pins the Fermi level. Inverted, bottom-anode oxide Schottky diodes typically lose ~0.1-0.3 eV, which on its own widens the 0.15-0.2 eV gap to ~0.25-0.5 eV.

*What would change the reviewer's mind:* Bottom-anode diodes with ALD IGZO on top reaching the barrier and ideality (n <=1.3) of top-anode controls from the same run.

**Response — ACCEPTED-DOWNGRADE:** Valid. Literature barriers come from O2-sputtered top contacts. Here IGZO ALD (metal-organics, H2O/O3, 150-300 C) grows on the anode and can strip interface oxygen; the a-RuOx/InAlN analogue falls from 0.75 to 0.55 eV after a vacuum anneal. The flip was evaluated: a pillar-core anode deposited last onto IGZO is a top contact and needs no anode etch-back, but it sits at the inner coaxial radius. Its hold field is 1.83 vs 0.91 MV/cm, costing +0.29-0.32 eV of image-force/TFE lowering at 60/15 nm (0.12-0.14 eV even at 100/20). That is as much as the 0.1-0.3 eV it avoids, so the flip is rejected. Process mitigations: in-situ O3 or O2-plasma re-oxidation of the Ru/RuO2 node face just before IGZO, O3-first low-temperature IGZO nucleation, and a 1-2 nm O3-ALD GaOx interlayer (DRAM's O3-ALD high-k on Ru electrodes is the analogue [UNVERIFIED]). If the 0.1-0.3 eV loss is real, the top-contact-equivalent bar is 1.16-1.41 eV (thermionic).

*Action taken:* Every anode is run as a pair on the same wafer: bottom-anode as integrated vs a top-anode control. This measures the penalty directly (gate G6), with a GaOx-interlayer split. The flipped variant is kept only as a planar diagnostic and disclosed in the IP (model 12h). Downgrade is part of the P 3 -> 2.

### RT-IND-diode-tower-01 — MAJOR — IND — §3 Prior art and genuine delta #1; §6 FTO (Kepler US 12096638)

> Delta #1, a per-tier rectifier between each floating node and the shared pillar in place of coercivity, falls between two estates: Kepler's 1T-nC stack: US 11,423,967 and 11,527,277, plus US 12,096,638, 'one transistor and N memory element', which is not limited to ferroelectrics by title (claims unread); also Intel EP4016625; diode-accessed capacitor memory with a plate line: US 2007/0183191, found in this review, uses a diode instead of a MOSFET as the access device, with the capacitor's other electrode on a plate line (rt-IND log). Kepler's 1T-nC plus diode-access 1D1C is a two-reference obviousness argument against the core cell. Pre-1990 diode-capacitor art remains unsearched.

*What would change the reviewer's mind:* Claims of US 12,096,638 and US 2007/0183191 read, with an FTO opinion showing that the single-pulse dump-read/clamp-write operation and the plate-swing rule are claimable on their own.

**Response — ACCEPTED-MITIGATED:** Agreed. Kepler's 1T-nC stack (US 11423967/11527277/12096638) plus US 2007/0183191 (diode-accessed capacitor, other electrode on a plate line) is a credible two-reference obviousness case against delta #1 as a broad cell claim. Delta #1 is downgraded from 'looks new' to 'probably obvious'. The claim set moves to elements a combination does not teach and that are detectable: (a) single-pulse dump-read / clamp write-back through the steering diode plus the plate-swing rule (swing >= Vdata + V_f + guard), visible in plate/pillar waveforms; (b) the depleted-shell, outer-anode coaxial diode sized to an anode-field limit, with the flip shown inferior by +0.29-0.32 eV; (c) the wrapped Mo/poly/Mo recess tier with plate pull-back; (d) in-hole anode formation with interface-oxygen control. A moat issue, not physics.

*Action taken:* Read the claims of US 12096638 and US 2007/0183191 at M0-1 (+$10k counsel; IP line 45 -> 55k) before filing. Pre-1990 diode-capacitor search. FTO opinion moved ahead of stack 1. Dossier section 3 notes the downgrade of delta #1.

### RT-IND-diode-tower-02 — MAJOR — IND — §2.3 Net bar (>=1.07-1.12 eV vs best IGZO 0.92 eV); §5 Coupon gate; header note 'P should be 2'

> The decisive experiment is a materials search, not a device proof. The best IGZO contact is 0.92 eV low-field against a 1.07-1.12 eV bar (1.17-1.22 eV for 1 s retention), and the dossier's own notes argue P = 2. If an anode passes, what the company owns is a known oxidized-metal-on-oxide Schottky (AgOx on ZnO, 2008; US 8,508,015) in a particular geometry. Composition results get published, and Kioxia, Micron and Samsung, all running in-hole oxide ALD, can reproduce them in one lot. A PASS creates more value for the field than for the company.

*What would change the reviewer's mind:* A process claim detectable in a competitor's product (e.g., in-hole outer-anode formation with interface-oxygen control that sets sigma <= 0.05 eV), filed alongside the coupon PASS.

**Response — ACCEPTED-MITIGATED:** Valid: a composition PASS is publishable and reproducible by anyone with in-hole oxide ALD, and the oxidised-metal-on-oxide Schottky is old art (US 8508015, AgOx 2008). What the company can own is the integrated cell, the operating method, and process steps detectable in a product (TEM/SIMS): an outer anode ring formed by etch-back + in-situ re-oxidation + O3-first oxide nucleation giving sigma <= 0.05 eV, the wrapped recess with plate pull-back, and the 2T in-line top. It also holds a 12-18 month data lead (4-tier stack, RTN, drift). The moat stays thin, but the mission rules out killing on business grounds.

*Action taken:* Anode and interface recipes are trade secrets until process claims are filed, and those claims are filed alongside the coupon PASS (second-wave filing moved to M7-8). No composition publications before the PCT; only the aA test structure is published.

### RT-IND-diode-tower-03 — MAJOR — IND — §2.2 Versus 1-beta; §2.5 Tier yield; models/diode-tower.py tier_yield=0.998, base_wafer_usd=3000

> The recess ring forces a 121 nm pitch, so parity needs 18 tiers and 3x needs 50. The 0.35x $/bit at 64 tiers assumes tier_yield 0.998 and $25/tier. At 0.99 per tier, the dossier's own table gives 0.58x at 64 tiers and 0.71x at 32. Re-based to an incumbent cost curve in the ~2032 window (-8-12%/yr), a 32-tier tower is near parity. The portfolio already funds AND-STACK and PIXEL-STACK, which claim more density, so an investor has no reason to fund a third oxide 3D cell with the smallest step.

*What would change the reviewer's mind:* Evidence that the tower's per-tier cost is <=50% of AND-STACK's or PIXEL-STACK's (deposition only, no per-tier litho), plus a multi-tier yield data point >=0.995.

**Response — ACCEPTED-DOWNGRADE:** Re-run with red-team costs ($3,450 base wafer, $38/tier, staircase in the footprint, tier yield 0.995). $/bit is 0.73x 1-beta at 32 tiers and 0.55x at 64 (0.45x at 0.998, 0.76x at 0.99), vs the claimed 0.55x / 0.35x. Against a 2032 incumbent falling 8-12%/yr, the 64-tier tower is 0.91-1.18x (roughly parity) and the 32-tier tower 1.2-1.6x. The critic's condition fails: $38/tier is not <= 50% of AND-STACK's $30 or PIXEL-STACK's $25 + $250/deck. Density, 3.9x at 64 tiers, is the smallest step in the portfolio (AND-STACK 8.1x, PIXEL-STACK 6.2x). The tower's distinct value is a two-terminal per-tier device with no per-tier transistor, which diversifies per-tier device risk; it is not cost per tier.

*Action taken:* Step-change claim lowered: S 3 -> 2. Density ~3.9x at 64 tiers, bits/$ ~1.8x vs today's 1-beta (was ~2.9x), parity-ish vs the 2032 curve unless >=96 tiers at >=0.998. Model tier_yield 0.995 with 0.998/0.99 shown; section 12l. Portfolio role is the two-terminal-device hedge, funded only through the shared oxide coupon run until Gate A. A multi-tier yield >= 0.995 data point is a raise milestone.

### RT-PROC-diode-tower-01 — MAJOR — PROC — §2.3 contact table (AgOx 1.10 eV best); §4 #8 'PtOx and AgOx may decompose [UNVERIFIED]'; §5 anode matrix

> The only contacts near the bar are ones the process cannot build. Ag2O partly dissociates at 300 C and is fully decomposed by ~400 C (Waterhouse, PCCP 2001); in gas it is stable only below ~170 C. An AgOx anode therefore will not survive the <=400 C IGZO, ALD and anneal steps intact, and PtOx also reduces at these temperatures. Pt, Ag and Ir have no volatile dry-etch products, so the per-tier etch-back that isolates anode rings inside a 60 nm, AR 27-53 hole is not available for them. Ag and Pt are also fast-diffusing contaminants excluded from most DRAM and CMOS-under-array tool sets. RuOx (volatile RuO4) and MoOx can be integrated, but no logged data puts either at >=1.07 eV on IGZO.

*What would change the reviewer's mind:* A dry-etchable anode (RuOx, MoOx or similar) on a <=20 nm IGZO or Ga2O3 shell with low-field phi >=1.07 eV and sigma <=0.05 eV after 400 C, plus a demonstrated HAR etch-back of that anode.

**Response — ACCEPTED-DOWNGRADE:** Agreed. Ag2O dissociates at 300 C and is gone by 400 C; PtOx reduces. Pt, Ag and Ir have no practical volatile dry-etch products for a HAR etch-back, and Ag, Pt and Pd are fab contaminants. These are excluded from the integrated list. Integrable anodes: Ru/RuO2 (volatile RuO4 via O2 plasma or O3, an isotropic etch-back), Mo/MoOx (MoF6, or wet), W/WOx (WF6), plus an area-selective IrO2 liner that needs no etch-back [SPECULATIVE]. Evidence such oxides make high barriers on wide-gap semiconductors: O2-annealed RuO2/IrO2 on GaN 1.43/1.48 eV; IrO2/RuO2 on 4H-SiC > 1.9 eV; oxidised Ir/Ru/Pd on beta-Ga2O3 above the 1.2-1.4 eV of the metals. Counter-evidence: amorphous RuOx on InAlN only 0.75 eV, falling to 0.55 eV after a vacuum anneal. No datum puts an integrable anode at >= 1.07 eV on IGZO. That is the critic's point, and it lowers the pass probability.

*Action taken:* Matrix restricted to dry- or wet-etchable anodes, with Ga-rich and a-Ga2O3 shells (lower electron affinity raises every barrier; keep a Ga-free shell for supply). RuO2/IGZO vs RuO2/Ga2O3 run planar first. A HAR etch-back of the chosen anode is a Stage B pass item. AgOx/PtOx/Pt are planar diagnostics only. Downgrade folded into P 3 -> 2.

### RT-PROC-diode-tower-02 — MAJOR — PROC — §2.6 GO measured on planar coupons with 'anode below the IGZO, as in the tier'; §2.3 inhomogeneity tail

> In the tower the Schottky interface is the ring's inner face, which is created by the etch-back that separates tiers. IGZO is then deposited onto a plasma-etched, partly reduced noble-metal-oxide surface. Oxidised-metal barriers are set by surface oxygen stoichiometry and defects (the dossier's own IrOx citation). Sigma costs 0.14 eV at 0.05 eV and 0.21 eV at 0.07 eV, against a barrier gap of already 0.15-0.3 eV. Planar, as-deposited anodes will understate sigma and overstate phi, so Gate A can pass on coupons and fail in the hole.

*What would change the reviewer's mind:* Barrier height and sigma measured on anodes given the real etch-back chemistry, or on vertical recess coupons, within 0.03 eV of the planar values.

**Response — ACCEPTED-MITIGATED:** Valid: in the tower the Schottky face is created by the etch-back. Oxidised-metal barriers are set by surface stoichiometry, and sigma costs 0.14 eV at 0.05 and 0.21 eV at 0.07 against a gap that is already large. Planar as-deposited anodes would overstate phi and understate sigma, so Gate A could pass on coupons and fail in the hole.

*Action taken:* New Stage A structure (e), +$30k: 2-tier vertical recess coupons (SiO2/Mo/poly/Mo mold, 100-150 nm e-beam holes, poly recess, ZrO2, Ru node, the real O2-plasma etch-back, in-situ re-oxidation, IGZO, core). Gate A uses (e) plus the ring arrays and floating nodes; planar coupons become diagnostics. The vertical-vs-planar phi/sigma difference is reported (G6). Kill 5 judged on vertical coupons.

### RT-PROC-diode-tower-03 — MAJOR — PROC — §1 diagram (access FET, gain FET, read select, write BL, read BL per pillar); §2.1 footprint 0.0165 um2; model INPUT base_wafer_usd=3000

> Each 121 nm-pitch pillar needs three transistors and two bitlines at its top. Three vertical oxide FETs will not fit side by side in 0.0165 um2: one 4F2 VCT at F~60 nm already takes ~0.014 um2. They must either stack as 2-3 device levels, or the footprint grows ~2-3x and 32-tier density falls from 1.94x to below parity. Two bitlines per pillar column put metal at ~60 nm pitch, under the ArFi single-exposure limit (~76-80 nm), so SADP is required. None of these ~10-15 masks is in the $3,000 base or the footprint.

*What would change the reviewer's mind:* A top-of-pillar layout and flow fitting the access, gain and select FETs plus both bitlines in <=0.02 um2 per pillar, with the added masks priced.

**Response — ACCEPTED-MITIGATED:** Valid: three side-by-side FETs plus two bitlines do not fit a 0.0165 um2 pillar, and two bitlines would need ~60 nm metal pitch (SADP). Redesign: (1) remove the read-select device, using the gain FET's source as a read word line as in imec 2T0C; (2) merge the write and read bitlines into one bitline per column at the 121 nm pillar pitch (single ArFi exposure, >= ~80 nm; no SADP), with the access FET off during the floating-pillar CDS read; (3) stack the access and gain FETs in-line as vertical channel-all-around IGZO devices in the pillar's own footprint. IMECAS showed vertical CAA IGZO 2T0C beyond 4F2 by monolithic stacking (IEDM 2021), and Huawei reports a 50 x 50 nm2 CAA FET. Footprint stays 0.0155 um2 before staircase. Transistors per user bit fall to 2/30 = 0.067 (32 tiers) and 2/61 = 0.033 (64). The ~7 added masks (two device levels, word line / read word line, contacts, bitline) are priced: base wafer $3,000 -> $3,450.

*Action taken:* Model base_wafer_usd 3000->3450; section 12m. Stage B builds the in-line 2T top on the 4-tier stack in 100-150 nm holes. The full 121 nm-pitch top is a raise milestone. Dossier header and diagram description updated to 2T.

### RT-PROC-diode-tower-04 — MAJOR — PROC — §1 'etches one hole through a stack of metal plate floors'; §5 Stage B 'TiN/SiO2 x 4'; model INPUT plate_nm=25

> At 64 tiers the stack holds 1.6 um of TiN; at ~1 GPa that bows a 775 um wafer by ~1 mm (Stoney). Alternating TiN/SiO2 stacks have no production HAR etch at AR 53. The NAND-style replacement route (SiN out through slits, metal in) would expose the ZrO2 and IGZO already in the hole to hot H3PO4 and to WF6/H2 or TiCl4/NH3 fills at 300-500 C. That brings in exactly the hydrogen and fluorine the barrier and drift budgets cannot take. A 4-tier Stage B stack will reveal neither problem.

*What would change the reviewer's mind:* A >=32-pair TiN (or Mo)/oxide stack with bow <=150 um etched at AR >=30, or a replacement flow shown to shift the coupon barrier by <=30 meV.

**Response — ACCEPTED-MITIGATED:** Valid as stated for TiN/SiO2. Stoney: 64 x 25 nm TiN at 1 GPa bows a 775 um wafer by ~1.0 mm. A TiN/SiO2 HAR etch does not exist in production, and NAND-style replacement after the in-hole stack would expose ZrO2 and IGZO to hot H3PO4 and WF6 / TiCl4 hydrogen and fluorine. Redesign: replacement-first. (1) Build an oxide/SiN/poly/SiN mold (NAND-like) and etch holes in dielectric only: AR 35 at 32 tiers, 69 at 64 as two 32-tier decks. (2) Fill holes with sacrificial carbon. (3) Etch slits, remove SiN with H3PO4 and fill with CVD/ALD Mo while nothing sensitive is in the hole. (4) Do an H out-gas bake, then strip the carbon. (5) Recess poly, ZrO2, node, etch-back, re-oxidise, IGZO, core. Stress: the wrapped tier has 20 nm Mo per tier (1.28 um at 64 tiers): 0.80 mm at 1 GPa, 0.24 mm at 0.3 GPa, 0.12 mm at 0.15 GPa. Meeting <= 150 um needs stress-tuned Mo + compressive oxide + a backside film, as NAND does. Cost is included in $38/tier and the $3,450 base.

*Action taken:* Stage B 4-tier stack uses the replacement-first Mo flow, not a TiN/SiO2 shortcut. Add a 32-pair mold bow coupon and a barrier-shift test (coupon diodes with/without the replacement thermal/H budget, <=30 meV). New kill 8 at M14. A hole etch at AR >= 30 and 60-80 nm is honestly a partner / raise milestone, not provable inside $1M. Model section 12k.

### RT-CIRC-diode-tower-04 — MINOR — CIRC — §2.4 plate-swing rule (0.2 V guard) / model c_fringe_tier_fF (pillar-to-plate only)

> The 0.2 V guard that keeps unselected nodes reverse-biased is eroded by plate k's 1.8 V swing coupling into nodes k+/-1. The plate-to-adjacent-node fringe is ~0.01-0.02 fF against a ~0.29 fF node (~4-7%), which gives ~70-120 mV and eats most of the guard. The model includes only pillar-to-plate fringe.

*What would change the reviewer's mind:* Extracted plate-to-adjacent-node coupling for the recessed-ring geometry, and a guard re-derived with it.

**Response — ACCEPTED-MITIGATED:** Valid. Estimate for the back-wall cell: node k+1 sits directly above node k across 25 nm SiO2 + 2 x 5.5 nm ZrO2. Node-node coupling is 0.0045 fF (it follows plate k+1 at Cs/(Cs+Cj) = 0.95), and plate fringe adds up to ~0.01 fF. On a 0.284 fF node at a 1.9 V swing that is a 29-92 mV step, which eats up to half of the old 0.2 V guard on top of the 100 mV droop. Fixes: (1) guard 0.2 -> 0.3 V, which costs +0.1 V of plate swing (~1.9 V) and ~11% plate energy (plate term 2.3 fJ in a 31 fJ access); (2) in the wrapped tier plate k's own Mo layers lie above and below node k, shielding k +/- 1 to <= ~0.0005 fF (~2 mV) [ESTIMATE]. Guard left after droop: 108-171 mV back-wall, ~198 mV wrapped.

*Action taken:* m_rev 0.2->0.3 V in the model (hold bias 0.8 V propagated to all barrier bars). 3D TCAD extraction of plate/node-to-neighbour coupling at M0-1. An adjacent-plate hammer pattern is added to the M18 zero-flip test (kill 9).

### RT-DEV-diode-tower-04 — MINOR — DEV — §2.4 endurance; G4 (delta-phi <=30 meV after 1e12 pulses at 515 A/cm^2)

> Noble-metal/IGZO interfaces are the active element of interface-type resistive switches, where oxygen-vacancy migration under repeated bias modulates the barrier. 1e12 forward pulses at ~515 A/cm^2, with ~1.1 V forward and reverse fields near 1 MV/cm, is a switching-like stress. Barrier drift is therefore a known mechanism, not just an unknown.

*What would change the reviewer's mind:* G4 passed on the G1-passing anode at 85 C with reverse-hold leakage re-measured every decade of pulses, delta-phi <=30 meV.

**Response — ACCEPTED-MITIGATED:** Valid: noble-metal/IGZO interfaces switch through O-vacancy migration, so drift is a known mechanism. The wrapped cell makes the stress harsher: 29.7 nA average write, ~1,125 A/cm2, 1.1e-5 C/cm2 per pulse. Ten years of 64 ms refresh is 9.9e9 pulses, so a 1e12 test still covers it ~100x. The drift budget is unchanged: 30 meV = 2.6x leakage.

*Action taken:* G4 exactly as the critic asked: on the G1-passing anode at 85 C, with reverse-hold leakage re-measured every decade, using a bipolar waveform (forward pulses + 0.8 V reverse hold). Options: a 20 ns write (halves current density; V_f lower by kT ln2), Ga-rich shells and passivation against V_O migration, hot-row remap. Kill 3 unchanged (>60 meV within 1e10).

### RT-IND-diode-tower-04 — MINOR — IND — §7 Partners ('cross-license our diode delta against their 1T-nC estate'); FE persistent variant

> The ferroelectric fallback walks into the best-funded programs in the space: Micron's 32 Gb NVDRAM (IEDM 2023), Kepler's 1T-nC program, the 2T-64C consortium (IEDM 2025: Notre Dame, Penn State, IBM, Fraunhofer, NUS) and FMC's HfO2 FeRAM effort [training knowledge]. The cross-licence plan assumes the diode delta is worth something to Kepler or Intel. For the FE variant it is not.

*What would change the reviewer's mind:* A stated interest from Kepler or Micron in a fatigue-free linear variant, or a measured endurance or retention advantage over FE 1T-nC that they lack.

**Response — ACCEPTED-MITIGATED:** Agreed. The FE persistent variant walks into Micron NVDRAM, Kepler 1T-nC, the 2T-64C consortium and FMC, and the diode delta adds nothing to an FE cell. It is no longer the NO-GO fallback, and no longer the premise of a Kepler/Intel cross-licence. It is parked, not killed for physics, with a revival condition: a measured endurance or retention advantage over FE 1T-nC, or stated partner interest in a fatigue-free linear variant.

*Action taken:* On a NO-GO, <=$60k goes to the Ga2O3 / heterojunction retry and the rest to AND-STACK / PIXEL-STACK coupons (section 6 revised). Section 7's cross-licence plan is restated for the linear diode-steered variant only. Kill 2 no longer says 'keep the FE variant'.

## hot-side-memory — HOT-SIDE MEMORY: oxide gain-cell tiers in the backside-power carrier wafer (carrier-last), plus at most 4 tiers in the logic BEOL (hot-side-memory)

**Final status after red team: DOWNGRADED.** The energy-per-bit step survives every correction (~11x vs HBM delivered at SM-local placement, 5.5x worst case). The system claim halves, from ~190 to ~90 W/GPU, because traffic share tracks capacity and the planning case drops to 1 b/cell: RTN, cross-temperature and 1e-4 tail-leakage terms are unmeasured, and the tail alone makes it refresh-light rather than refresh-free. Cost rises from $1.36-3.55 to $4.6-12/GB. Bond-first is replaced by a carrier-last flow to sidestep the FATAL backside-overlay objection and In/Ga/Zn exposure, which only a BSPDN foundry can finally prove. No objection kills the physics.

*Revised verdicts* — Possible: Yes at 1 b/cell: refresh-light, with the 1e-4-tail refresh at ~3.6 s (105 C) and ~1.4 s (125 C), ~225x rarer than Si. 2 b/cell is conditional on a 1e-4 RTN quantile <=30 mV, cross-temperature residual <=10 mV, tail leakage <=7.5 aA at 105 C and drift <=20 mV in a >=600 mV window, none of which is measured yet. No law is violated. Backside overlay and contamination are engineering risks, sidestepped by the carrier-last flow. · Profitable: STEP CHANGE IF IT WORKS: energy per bit moved, ~10x lower than HBM (0.37 vs 3.95 pJ/b delivered; 5.5-15x depending on placement), down from ~12x. ~90 W saved per 2028-30 backside-power GPU at the 16 x 1 b planning case (48 W at 8 x 1 b, ~170 W if 2 b works), down from ~190 W. Not a cost step: $4.6-12/GB, 3-8x DDR5 cost, 1-3x below the HBM4 price. · Doable by this founder: PROVABLE WITH $1M: partly. The cell question (drift, RTN, cross-temperature, 1e-4 tail, real-bond hydrogen) is answered for ~$240k by M11. Logic shift on 22FDX plus carrier proxies (IPD, CSAM voids, VPD-ICPMS) fit in $1.00M by M22. Production backside overlay, killer-defect density, foundry materials acceptance and a named BSPDN partner need the raise.

### RT-PROC-hot-side-memory-01 — FATAL — PROC — §4 #7 'Carrier bow vs backside-litho overlay: Unknown'; §5 Gate C pass 'bow increase <=10% [ASSUMPTION]'

> In a BSPDN flow the carrier is bonded before the logic wafer is thinned to <1 um and its backside nano-TSV/contact level is patterned. That level needs <10 nm overlay to the buried frontside today and <<5 nm at the next node (CEA-Leti, SPIE 12496; Chip Scale Review 2024), and bonding to a blank carrier already leaves ~15 nm (mean+3sigma) after scanner correction. The thinned logic layer takes on the carrier's surface strain. With 3.2 um of tier films at ~100 MPa that strain is ~2-7e-6 (membrane to bending), ~0.3-1 um at the wafer edge, which is mostly correctable. But a 10% die-scale stress non-uniformity (16 patterned tiers vs scribe and periphery) leaves ~3-10 nm of intrafield distortion over a 28 mm field, the entire budget. Gate C measures bow, which is the wrong metric. No foundry will bond a ~$30k 18A/A16 wafer to a carrier that adds even 2-3 nm of uncorrectable distortion.

*What would change the reviewer's mind:* High-order and intrafield backside-overlay residuals on logic-emulation wafers bonded to an 8-16-tier carrier within ~1-2 nm (3sigma) of the blank-carrier reference after standard scanner correction. Measure them with backside overlay marks at a BSPDN-capable partner (imec, CEA-Leti or Intel).

**Response — ACCEPTED-MITIGATED:** Valid against the bond-first flow (today's BSPDN order: carrier bonded before thinning and backside litho). With ~100 MPa net tier stress and 10% die-scale non-uniformity, 3-10 nm of intrafield distortion uses up the <10 nm backside-overlay budget. Bow was the wrong Gate C metric. Two answers. (1) Baseline becomes a CARRIER-LAST flow. The logic wafer goes through thinning and backside litho on an inorganic IR-release temporary Si carrier (EVG IR LayerRelease class: inorganic release layer, front-end and fusion/hybrid-bond compatible, vendor claim, logged). The backside is then moved to a second temporary carrier, the front is released, and the memory wafer is hybrid-bonded at 1.5 um pitch, which tolerates ~100-300 nm of alignment error. The memory wafer never sees backside litho, so carrier-induced overlay goes to zero. Cost in the model: +$400/wafer and 1% logic scrap from the two temporary bond/debond cycles. (2) Bond-first stays only as a conditional option: stress-neutral tier films (|net| <=10-20 MPa gives ~0.3-2 nm by the reviewer's own scaling) plus dummy-filled scribe and periphery. The field-repeating part of the fingerprint is correctable by intrafield high-order correction, so only the non-repeating residual counts.

*Action taken:* Carrier-last is the baseline flow (model: carrier_last_usd $400, p_kill_temp_bond 1%). Gate C metric changes from bow to in-plane distortion: film-stress maps of patterned vs blanket tiers, FEM, and wafer-geometry IPD of SOI bonded to a tier coupon vs a blank-carrier reference. Bond-first is kept only if the residual is <=1-2 nm (3 sigma) at a BSPDN partner (imec, CEA-Leti or Intel); that is a raise milestone, and kill criterion 6 is rewritten.

### RT-CIRC-hot-side-memory-01 — MAJOR — CIRC — §2 density (array_eff_carrier 0.5) / §6 subarray 64x256 / §2 energy (8.1 fF RBL)

> Periphery does not fit under the array as modelled. The energy number uses a 64-cell local read bitline in 64 x 256-cell subarrays. Across 16 tiers x ~2.5e10 cells per tier per die, that implies ~6.3e9 bitline segments and ~3.1e9 wordline drivers (a write and a read wordline per 256-cell row). Under 800 mm2 of carrier that is 0.13 um2 per SA and 0.26 um2 per driver. A level-shifting driver for the 2.2 V write-wordline swing (-0.5 to 1.7 V) in 28-65 nm CMOS is ~2-5 um2. Array efficiency 0.5 cannot hold with these subarrays. Real designs need 2-4k-cell rows and tier-shared SAs reached through oxide tier-select switches. Those put an extra oxide device (sigma Vt 30-100 mV, with its own PBTI) and 16-tier via capacitance into the 2-bit read path, which the 8 mV sense residual ignores.

*What would change the reviewer's mind:* A carrier floorplan for 16 tiers giving SA and wordline-driver counts per mm2 that fit 28-65 nm CMOS, with the energy and window budget re-run on the resulting bitline hierarchy.

**Response — ACCEPTED-MITIGATED:** Correct. 16 tiers x 2.5e10 cells with 64 x 256 subarrays needs 6.3e9 SAs and 3.1e9 WL drivers: 0.13 um2 and 0.26 um2 each, or ~24x the carrier area. Redesigned floorplan, re-run in model section 11(a): 8,192-cell rows, a 64-cell local RBL behind an oxide segment switch, and a 4,096-cell in-tier global RBL with one via per tier to a Si 16:1 tier mux and a shared 2-b SA in the carrier. That gives 9.1 um2 per WL driver and 146 um2 per SA, or 50% of the carrier area in 28 nm-class CMOS (3 um2 drivers, 25 um2 SA+mux). The tier-select device is now Si in the carrier, not oxide. The remaining oxide segment switch runs in deep triode at >=1.5 V overdrive: a 50 mV Vt sigma moves Ron ~3%, and with Ron <=10% of the read-FET resistance that is <1 mV equivalent. Per-segment reference rows cancel the common mode. Costs: tier efficiency 0.50 to 0.45; global RBL/WBL of 126 fF; read 0.087 to 0.121 pJ/b; 2-b write 0.134 to 0.54 pJ/b; mix 0.21 pJ/b at the port; sense residual 8 to 10 mV; carrier CMOS $1,800 to $2,800 (28 nm-class). A 65 nm carrier fits only ~4-5 tiers.

*Action taken:* Model: array_eff_carrier 0.45, cells_per_row 8192, c_gbl_fF 126, sigma_read 10 mV, carrier_cmos_usd 2800, E_oxide_refresh_fJ 200. Capacity at 16 x 2 b drops from 89 to 78 GB/die. M0-3 design work delivers a carrier floorplan with SA and driver counts per mm2 and SPICE of the hierarchical RBL with an extracted 16-tier via. The 2-b row page is 2 KB with read-modify-write.

### RT-CIRC-hot-side-memory-02 — MAJOR — CIRC — §2 multi-level margin (24 mV drift budget) / §5 Gate A (isothermal)

> Cross-temperature reads are not budgeted. a-IGZO TFT threshold falls ~17 mV/K (Chen et al., IEEE TED 2009; logged in rt-CIRC). A GPU's local temperature swings 20-40 K between idle and load on ms-to-s scales, and hotspots move with the kernel. Data written at 80 C and read at 105 C therefore sees up to ~0.4 V of read-FET shift if uncompensated, against a 2-bit half-spacing of 100 mV and a 24 mV drift budget. Per-level references cancel only the common mode, and a 5% cell-to-cell tempco spread is ~20 mV at 25 K, which is the whole budget. Gate A measures drift isothermally at 85, 105 and 125 C, so it cannot see this.

*What would change the reviewer's mind:* Gate A adds write-at-T1, read-at-T2 maps (delta T +/-30 K) on >=1e5 cells with in-array references, showing residual sigma <=10 mV. Otherwise the plan should default to 1 bit per cell.

**Response — ACCEPTED-DOWNGRADE:** Valid. a-IGZO Vt moves ~-17 mV/K (long-channel display TFT; unmeasured for 40 nm ALD channels). A 25-30 K swing between write and read is 0.4-0.5 V of common mode, and a 5% cell-to-cell tempco spread leaves 21-26 mV, the whole 2-b budget. Mitigation: (a) each 2 KB row carries its own three per-level reference cells, written in the same burst (0.04% overhead), so temperature history, drift and tempco are common to data and references; (b) a write-temperature tag per region, plus a rewrite when |T - T_write| > 10 K, holds the residual to 5% x 17 x 10 = 8.5 mV. Rewrite is an internal row cycle. Steady serving rarely trips the rule, but kernel-scale hotspot motion of 20-40 K on ms scales could trip it often over the ~15% hotspot area, which is why 1 b is assigned there (thermal-map bits per cell, delta #4). The residual is modelled as a 10 mV term, which with the RTN reserve takes the 2-b drift allowance to 20 mV. 2 b is not proven until cross-temperature maps exist, so the planning case follows the reviewer's default: 1 b.

*Action taken:* Model: sigma_xT_mV 10, plan_bits 1. The planning capacity at 16 tiers halves from 157 to 78 GB/GPU, and 2 b becomes an upside. Gate A adds write-at-T1/read-at-T2 maps (dT +/-30 K) on >=1e5 cells with in-row references; 2 b passes only if the residual sigma is <=10 mV. The tempco is measured on 40 nm ALD devices at 25-125 C.

### RT-CIRC-hot-side-memory-03 — MAJOR — CIRC — §2 watts saved (traffic_frac 0.5 -> 193 W)

> Traffic share is coupled to capacity, and the 193 W assumes the best capacity case. LLM decode reads every resident weight and KV byte each step, so the near tier's traffic share is roughly its share of resident bytes. A share of 0.5 needs ~144 of 288 GB, which only the 16-tier x 2-bit case gives (178 GB/GPU). At Gate A's 1-bit fallback, 16 tiers give 89 GB/GPU (31%) and ~119 W. The 8 x 1-bit first product gives 44 GB (15%) and ~58 W at the same 3.65 pJ/bit delta. The planning headline should be indexed to bits per cell and tier count.

*What would change the reviewer's mind:* A trace-driven study showing that a hot subset (<30% of resident bytes) carries >=50% of HBM traffic in real serving, or a tier plan that actually delivers 2 bits per cell at 16 tiers.

**Response — ACCEPTED-DOWNGRADE:** Accepted. In decode every resident byte is read each step, so the near tier's traffic share is about its share of resident bytes. The model now indexes share to capacity: additive = C/(C+288), HBM-shrink = C/288, planning = their mean, capped at 0.5. Revised density and delivered energy (0.37 pJ/b): 8 x 1 b (39 GB/GPU) is 13% and 48 W; 16 x 1 b (78 GB, planning) is 24% and 92 W; 16 x 2 b (157 GB) is 45% and 169 W. The 190 W headline belonged to the 16 x 2 b best case. A hot subset, such as skewed MoE expert popularity, shared experts or prefix KV, could raise share above byte share, but that is unproven until traces show it.

*Action taken:* W/GPU headline downgraded from ~190 W to ~90 W (planning 16 x 1 b; range 48-169 W); model traffic_share() added. The M0-3 trace study must report the bytes-moved share vs resident share on production decode traces (dense and MoE). Kill criterion 8 is re-indexed.

### RT-DEV-hot-side-memory-01 — MAJOR — DEV — §2 retention and refresh; model INPUT tail_leak_mult=3; Gate A 'tail retention >=1 s at 125 C (<=7.5 aA)'

> The 1e-4 tail cell is assumed to leak only 3x the reported imec cell, yet the dossier itself quotes 30-100 mV Vt sigma for BEOL oxide devices (§4 row 9). At 3.72 sigma and ~95 mV/dec at 105 C (ideal 75), sigma 30/50/100 mV gives ~15x/90x/8,000x, not 3x. From the implied 75 zA at 95 C, the 105 C tail is ~2-13 aA (sigma 30-50 mV) against the 7.5 aA 2-b budget at 1 s, and the 125 C tail is ~7.5-45 aA against the Gate-A line of <=7.5 aA. Unless write-FET sigma_Vt <=30 mV is shown in arrays, both 2-b capacity and the 125 C GO fail on the dossier's own arithmetic.

*What would change the reviewer's mind:* A write-FET Vt distribution on >=1e5 BEOL cells with sigma <=30 mV and SS <=90 mV/dec at 105 C, or a measured 1e-4-quantile retention >=1 s at 125 C after the full emulation sequence.

**Response — ACCEPTED-DOWNGRADE:** Correct on the dossier's own numbers. At the 1e-4 quantile (3.72 sigma) with SS 95 mV/dec, write-FET sigma_Vt of 30/50/100 mV gives 15x/91x/8,217x, not 3x. That is a 105 C tail of 13 aA and a 125 C tail of 46 aA at 50 mV, against ceilings of 7.5 aA (2 b, 1 s) and 22.5 aA (1 b, 1 s). Three answers. (1) Series or double-length write gate (top-up I-12627). In a vertical cell it costs no footprint, only a 0.20 to 0.24 um taller tier. A cell then leaks only if both segments are outliers, so the 1e-4 pair quantile sits at z = 2.33 (independent) to 2.96 (rho 0.5): 17-36x at 50 mV before any stack-effect credit. (2) Hold bias -0.5 to -0.7 V buys ~127x for subthreshold-limited cells, which makes the single FET 0.7x. If leakage is not subthreshold-limited, the Vt-sigma mapping does not apply in the first place. (3) The planning value is now 25x. That gives a 1-b refresh of 3.6 s at 105 C and 1.4 s at 125 C (1 b passes 125 C at 12.5 aA), and a 2-b refresh of 0.64 s and 0.25 s. Unmitigated 91x gives 0.24 s (2 b, 105 C) and 0.49 s (1 b, 125 C).

*Action taken:* tail_leak_mult raised from 3 to 25, with the 91x unmitigated case shown in model section 11. Refresh claim downgraded from 'refresh-free, ~6,400x fewer refreshes' (typical cell) to 'refresh-light': ~225x fewer than Si at 105 C for 1 b (1e-4 tail) and ~40x for 2 b. Refresh power for 78 GB is ~0.2-0.5 W vs 1.8-7.2 W for Si. Gate A adds write-FET Vt/SS distributions on >=1e5 cells, a directly measured 1e-4 retention quantile at 105/125 C, single vs series write-gate splits and -0.5 vs -0.7 V hold splits.

### RT-DEV-hot-side-memory-02 — MAJOR — DEV — §2 multi-level margin (sigma_read 8 mV, sigma_place 10 mV) and show-stopper #2

> The 2-b budget has no term for random telegraph noise in the read transistor, which in a gain cell is the sensor itself. RTN is cancelled neither by per-level references nor by write-verify, because the trap state at verify and at read (1-4 s later) are independent. For a read-FET gate of 0.0016-0.01 um^2 (40 nm planar to vertical channel-all-around) at EOT ~4 nm, one trap shifts Vt by 1.9-11.6 mV on average, or 4-35 mV with amorphous-channel percolation, and nearly every trap with tau between microseconds and seconds toggles between verify and read. With ~1 such trap per device and a ~60 mV excursion allowance, the per-read error probability spans ~3e-7 (small eta) to >1e-2 (large eta). This is the mechanism that capped MLC in sub-20 nm NAND, and it decides whether 2 b (89 GB) or 1 b (44 GB) is real.

*What would change the reviewer's mind:* Gate A reports repeated-read Vt-equivalent distributions (>=100 reads spaced ~1 s) on >=1e5 cells at 105 C, with the 1e-4 RTN quantile <=30 mV.

**Response — ACCEPTED-MITIGATED:** Accepted: RTN in the read FET is a missing term that neither references nor write-verify cancel. Single-trap dVt = q/(Cox A) at EOT 4 nm. For the planar 40 nm gate (0.0016 um2), eta = 11.6 mV and P(err) ~3e-3, or 9e-2 with 3x percolation: 2 b is dead in planar cells. For the vertical channel-all-around read FET (0.01-0.015 um2), eta = 1.2-1.9 mV, giving P(err) 4e-22 to 5e-15, or 5e-8 to 1e-5 with 3x percolation. So 2 b is plausible only in vertical cells and only if percolation stays at <=3x. Search found no IGZO-specific RTN amplitude data (logged), so this is unmeasured. Budget change: half the raw-BER budget (5e-5) is reserved for RTN, and the Gaussian terms get the rest. Cells that show inconsistent verify reads are flagged and remapped (1% capacity budget). 1 b, with a 300 mV half-spacing, is insensitive to RTN.

*Action taken:* Model: rtn_ber_share 0.5, which moves the 2-b allowed drift from 24 to 20 mV. Vertical channel-all-around read FETs with >=0.01 um2 gate area become a design rule. Gate A adds >=100 repeated reads ~1 s apart, plus fast reads at 1 us-1 ms spacing, on >=1e5 cells at 105 C. 2 b needs the 1e-4 RTN quantile <=30 mV (eta <=3.3 mV, P(>60 mV) = 1e-8); 1 b needs <=100 mV.

### RT-DEV-hot-side-memory-03 — MAJOR — DEV — §5 Step 2 emulation (350 C/2 h + 400 C forming gas on unbonded coupons); show-stopper #1

> A backside-power carrier must survive grinding of the logic wafer to sub-micron thickness plus backside CMP, so its oxide-oxide bond is annealed hot (typically 300-400 C) and acts as a water/hydrogen source. Activated surfaces carry ~4-5 OH/nm^2, and condensation releases ~2-5e14 H2O/cm^2 at the bond plane, within ~1 um of the top tier. An IGZO donor sheet of 1e12 cm^-2 shifts Vt by ~0.14 V at EOT 3 nm, so if ~0.1% of that inventory acts as donors in a channel it exceeds the 24 mV drift and 10 mV Vt budgets. Gate A anneals unbonded coupons and never sees bond-interface water, and Gate C (carrier emulation) arrives at M22, after the capacity decision.

*What would change the reviewer's mind:* SIMS hydrogen profiles plus top-tier delta-Vt <=10 mV after a real fusion or hybrid bond with a 350-400 C anneal on a tier coupon, moved into Gate A.

**Response — ACCEPTED-MITIGATED:** Valid: Gate A annealed unbonded coupons, so it never saw the ~2-5e14 H2O/cm2 that a 350-400 C oxide-oxide bond releases within ~1 um of the top tier. 0.1% of that acting as channel donors would shift Vt by 30-70 mV, far over the 10 mV budget. Fix: a real bond moves into Gate A. Small Si cap chips with 0.5-1 um of product-like bonding oxide are plasma-activated, hydrated with D2O and fusion-bonded over the array area of tier coupons, leaving the pads exposed, then annealed at 350-400 C for 2 h. The deuterium label separates bond-plane hydrogen from bulk hydrogen in SIMS (DOE nanocenter). The split also runs with and without a 10-20 nm ALD Al2O3 barrier and a SiCN bond dielectric.

*Action taken:* Gate A gains a bonded split (+$25k, M6-11); the Gate A date moves from M10 to M11 (2027-11-30). Pass: top-tier dVt <=10 mV and drift within the unbonded split's class. Fail: kill criterion 1 is evaluated on the bonded split, not the unbonded one.

### RT-IND-hot-side-memory-01 — MAJOR — IND — §2 Watts saved per GPU; models/hot-side-memory.py traffic_frac=0.50, hbm_util=0.60

> The ~190 W/GPU planning saving assumes traffic_frac 0.50. In decode-dominated serving, almost every resident byte (weights, KV) is read once per step, so the near tier's share of traffic tracks its share of resident bytes. The dossier's own table puts the near tier at 44-178 GB per GPU beside 288 GB of HBM. If that capacity is additive, the share is 13-38%, which gives ~50-145 W, not 190 W (the model's own sweep gives 77 W at 20%). At Blackwell's 8 TB/s and 50% share it is already only 70 W. The 12x per-bit energy gain survives. The per-GPU dollar case ($2,313 of datacenter capacity over 5 years) roughly halves.

*What would change the reviewer's mind:* The planned M0-3 traffic-share study, run on production decode traces, showing >=50% of HBM bytes moved come from <=30% of resident capacity (hot KV, activation reuse). Or a placement in which the near tier holds the entire tensor-parallel weight slice while HBM shrinks.

**Response — ACCEPTED-DOWNGRADE:** Accepted; this is the same coupling as CIRC-03. Additive capacity gives 12-35% share, so 45-133 W across 8 x 1 b to 16 x 2 b. The HBM-shrink placement gives 14-50%, so 51-189 W. The planning case (16 x 1 b, mid) is 24% and ~92 W, roughly half of 190 W. Per bit, the gain survives at ~11x. The 5-year value per GPU at ~$16.4/W goes from ~$3,100 to ~$1,500 for 16 x 1 b. That still covers the revised near-tier cost (~$650/GPU) about 2x. HBM-shrink also removes ~2 HBM4 stacks (~$1,150), which would on its own cover the near-tier cost.

*Action taken:* Same downgrade as CIRC-03: ~190 W becomes ~90 W planning. The decisive trace study runs in M0-3 on production decode traces. It passes the 'hot subset' case only if >=50% of bytes moved come from <=30% of resident bytes; otherwise the capacity-indexed number stands.

### RT-IND-hot-side-memory-02 — MAJOR — IND — §1 'Two recent changes'; §2 'saving ~190 W per Rubin-class GPU'; §7 Intel Foundry as first partner

> The premise that backside power 'already forces a bonded carrier onto every leading-edge logic die' does not hold for the product the saving is quoted against. A 22 TB/s Rubin-class GPU is built on a front-side-power node (TSMC N3P [training knowledge]). Backside-power accelerators arrive only with TSMC A16/A14 or Intel 18A/14A, ~2028+. Intel 18A, the only U.S. backside-power line, has few external logic customers. So the addressable slot in 2028-30 is a handful of tape-outs. Each one requires a foundry to insert a third party's memory wafer into its own wafer-to-wafer flow, with no known-good-die screen.

*What would change the reviewer's mind:* A named backside-power accelerator program (A16, 14A or 18A) with a dated tape-out whose owner wants an active carrier. Or a foundry statement that the carrier slot is open to third-party wafers.

**Response — ACCEPTED-MITIGATED:** Valid as worded: Rubin is a front-side-power product, and 'every leading-edge die' is false before ~2028. Corrected premise: backside power puts a bonded carrier on every A16, 18A and 14A-class die. Reported programs exist. Nvidia is reported as TSMC's first A16 customer for Feynman (2028, samples possibly 2027), and OpenAI was earlier reported to have booked A16 capacity (logged; reports, not TSMC confirmations). That window, ~2029-31, is when a carrier product could ship after an 18-24 month demo and a $10-50M development round anyway. The 22 TB/s Rubin-class GPU is kept only as a bandwidth proxy, and HBM bandwidth per GPU rises in later generations. For front-side-power hosts there is a fallback: an SoIC/V-Cache-style face-to-back bond with TSVs through the logic. It works, but it pays for a full extra wafer, so the 'free slot' advantage is lost there. No named program has asked for an active carrier.

*Action taken:* Section 0 premise reworded, and the watts are quoted against a '2028-30 backside-power accelerator at >=20 TB/s'. Raise gate: a named BSPDN accelerator or foundry contact (A16, 14A or 18A) willing to evaluate a third-party carrier before the Series A. The front-side-power SoIC fallback is added to the scale path.

### RT-IND-hot-side-memory-03 — MAJOR — IND — §3 Prior art and genuine delta; §6 IP strategy; §7 'Logic foundries own the slot'

> The dossier concedes that the broad claim is barred (Chip Scale Review 2022; imec CMOS 2.0, arXiv 2510.04535) and that the foundries own the slot. What the startup keeps is narrow: thermal-map-aware bits per cell, an analogue of NAND SLC/MLC mode switching; fail-soft binning, i.e. RAIN, Chipkill and bad-block practice, which the Stage-2 critic rated DROP on I-00729. TSMC (BEOL memory over logic, VLSI 2025), imec and Samsung (IGZO VCT plus wafer-to-wafer periphery) each own more of this stack than the startup does. A foundry would build the 'memory carrier option' in-house or through imec's partner program and has no need for a licence.

*What would change the reviewer's mind:* Claims read for US 12,666,958 and US 2025/0167193, plus an FTO opinion, showing a carrier-stack claim a foundry cannot design around (e.g., a backside-proof hydrogen barrier combined with power-map-sized via fill). Or a foundry JDA that names the startup as IP owner.

**Response — ACCEPTED-MITIGATED:** Accepted. The broad claim is barred (Chip Scale Review 2022; imec CMOS 2.0). Binning and SLC/MLC switching are established practice, and TSMC, imec and Samsung each hold more of the stack. A foundry could build the option itself. The red team created narrower but real reductions to practice that a foundry would need and does not yet have published. (1) Carrier-last oxide-memory flow with the bevel/encapsulation contamination package. (2) Bond-interface hydrogen control: a D2O-labelled qualification method plus a barrier and SiCN bond stack with data. (3) Cross-temperature MLC: in-row references, write-temperature tags and a delta-T rewrite rule. (4) RTN screening and remap for gain cells. (5) A Si tier-mux carrier floorplan under oxide tiers. The business case is therefore data, know-how and team toward a JDA or acquisition, not a royalty stream. The founder framing does not kill on business grounds, but the licensing upside is lowered.

*Action taken:* Claims of US 12,666,958 and US 2025/0167193 are read in M0-3 (within the $40k IP line), before filing. Provisionals are re-ordered to (2), (3), (1), (4), (5). An FTO opinion comes before the raise. Exit thesis: a foundry or memory-maker JDA naming the startup as data and IP owner of the qualification method.

### RT-IND-hot-side-memory-04 — MAJOR — IND — §5 Honesty note; §6 'Inside the portfolio seed, only Gate A runs (~$150k)'

> The portfolio seed funds only Gate A, a 1-4 kb coupon drift study; Gates B and C become raise milestones. The risks a foundry and an accelerator buyer will actually price stay untouched until after the raise: killer-defect density <=1.25e-4/cm2 (university fabs run 'far above' it, per §5); carrier bow against backside-litho overlay; Cu hybrid bonding on production backside-power logic. The $10-50M investor is asked to fund the part that decides adoption on the strength of one coupon's drift sigma.

*What would change the reviewer's mind:* An in-kind commitment from a foundry, MIT LL or NY CREATES to run Gate C on 300 mm backside-power-like wafers within the seed. Or a Gate-B logic-shift result on real 22FDX dies inside the seed budget.

**Response — ACCEPTED-MITIGATED:** Partly refuted, partly accepted. The standalone $1M plan already funds Gate B on real 22FDX dies (logic RO/Vt shift under 2 tiers, 1,000 h bake), which is the reviewer's own second 'change my mind' condition. Only the portfolio-seed variant was Gate-A-only. Accepted: production-scale killer density (<=1.25e-4/cm2), backside overlay on real BSPDN logic and Cu bonding on production wafers cannot be shown in $1M. Seed proxies are added for each foundry risk the reviewers named. Overlay: patterned-vs-blanket tier film-stress maps, FEM and wafer-geometry IPD vs a blank-carrier reference ($20k, folded into carrier emulation, now $130k). Voids: CSAM plus Surfscan on 20 bonded 200 mm pairs ($45k). Contamination: VPD-ICPMS/TXRF ($15k). The budget is rebalanced to $1.00M: sky130 dropped, BEOL post-processing reduced to 2 tiers, contingency 4.3%.

*Action taken:* Revised plan is $1,000k: salaries 240 + experiments 677 + IP 40 + contingency 43. Gate B on 22FDX stays inside the seed. The data room states plainly which numbers are proxies (IPD, CSAM, VPD) and which are foundry-only (overlay residual, defect density, materials acceptance). PROVABLE stays 'partly'.

### RT-PROC-hot-side-memory-02 — MAJOR — PROC — §2 'Yield and cost' $1.36/GB; model INPUT logic_die_usd ('~38 good 800 mm2 dies') vs §9 GB/wafer computed on 64 gross sites

> The model prices the logic die at ~38 good dies per wafer but spreads the carrier cost over all 64 gross 800 mm2 sites (GB/wafer = 64 x 80 GB = 5,120). W2W bonding allows no known-good-die selection, so every carrier site under a dead logic die is scrapped with it. $/GB therefore rises by 64/38 = 1.68x: from $1.36 to ~$2.29/GB for 16 x 2 b, and from $3.55 to ~$5.98/GB for 8 x 1 b. The 'near-tier bits at DDR5-like dollars' line becomes 1.5-4x DDR5 cost.

*What would change the reviewer's mind:* §9 re-run with GB/wafer = good logic dies x GB/die. Alternatively, a known-good-die (D2W) route with its own cost and pitch.

**Response — ACCEPTED-DOWNGRADE:** Correct. W2W bonding has no known-good-die screen, so only carrier sites under the ~38 good logic dies ship, not all 64 gross sites. That alone is x1.68. Model re-run with GB/wafer = 38 x GB/die x 0.9, together with PROC-03, the 28 nm carrier, ECC and the carrier-last adder. 16 x 2 b goes from $1.36 to $4.61/GB, 16 x 1 b (planning) from $2.71 to $9.22/GB, and 8 x 1 b from $3.55 to $11.87/GB. That is 3-8x DDR5 cost and 1-3x below the HBM4 price. Per GPU the near tier costs ~$420-650 against ~$790-1,500 of 5-year value at ~$16.4 per W saved, so it remains net positive. The 'DDR5-like dollars' line is withdrawn. A D2W known-good-die route is the revival, at the cost of losing the free carrier slot.

*Action taken:* Cost claim downgraded from $1.36-3.55/GB to $4.6-12/GB: a premium near tier, not cheap bits. Section 9 of the model now uses good_logic_dies = 38. The step-change axis (energy) is unaffected.

### RT-PROC-hot-side-memory-03 — MAJOR — PROC — §2 'Incremental cost ... 16 x $300 tiers'; model INPUT tier_usd=300 ('~3 ArFi single-exposure passes')

> A sequentially built 2T0C tier is not three litho passes. Write-WL, read gate, channel/via, write-BL, read-BL/SL and storage-node contact make >=5-6 patterned levels, even in IMECAS-style single-step dual-gate cells, and each level must register to the tier below. Sixteen tiers then carry ~80-100 masks, more than an entire DRAM flow, plus 16 chained overlay registrations whose yield loss binning can absorb but whose cost it cannot. At ~$100 per patterned level all-in, a tier costs ~$500-600 and the carrier adder ~$10-12k. Combined with objection 02, 16 x 2 b lands at ~$3.5-4/GB.

*What would change the reviewer's mind:* A mask-level flow for one carrier tier with <=3 patterned levels (e.g. NAND-style self-aligned patterning of >=4 tiers per litho), or a foundry quote of <=$5k/wafer for a 16-tier BEOL oxide stack.

**Response — ACCEPTED-DOWNGRADE:** Accepted. A sequential vertical 2T0C tier needs >=5-6 patterned, registered levels: write WL, read gate, channel/via, write BL, read BL/SL and SN contact. That is ~88 masks for 16 tiers. At ~$100 per level all-in, a tier costs ~$550 rather than $300, and the 16-tier adder becomes $12,350/wafer with the 28 nm carrier and the carrier-last steps. The 16 chained registrations cost yield, which binning absorbs, and money, which it does not. No EUV is added (ArFi single exposure), but mask count is no longer a selling point.

*Action taken:* tier_usd raised from 300 to 550; the 16 x 2 b cost moves to $4.61/GB, already included in PROC-02. Revival condition logged: self-aligned multi-tier patterning with <=3 litho levels per tier (NAND-style), or a foundry quote of <=$5k/wafer for a 16-tier stack. Mask count is listed as a cost, not a benefit, in sections 2 and 8.

### RT-PROC-hot-side-memory-04 — MAJOR — PROC — §2 'Yield and cost' logic scrap 0.6% at p=0.1% per tier/bond; §4 #5 (counts shorts only)

> The logic-scrap estimate counts shorts but not bond voids. A single >=0.5 um particle unbonds a 2-3 mm radius (CELL-WAFER FOUNDRY's own input), and the void delaminates when the logic wafer is thinned to <1 um, killing the 8 cm2 die above it. A blank prime carrier is the cleanest surface in the fab; a carrier after 16 tiers of dep/etch/CMP is not. At CELL-WAFER FOUNDRY's 'fab-grade' 0.05 particles/cm2, voids scrap 1-exp(-0.05 x 8) = 33% of $800 logic dies. Holding scrap <=1% needs <=0.0013/cm2, about one particle per 300 mm wafer, on a heavily processed surface.

*What would change the reviewer's mind:* CSAM void maps on >=25 W2W pairs (8-16-tier processed carrier on dummy logic) showing void-induced die loss <=1% at 800 mm2 die size.

**Response — ACCEPTED-MITIGATED:** Valid that voids were not counted, but 33% overstates the problem. With a 2.5 mm void radius each particle kills ~11 cm2 of 800 mm2 dies, so <=1% loss needs <=0.0009/cm2, about one particle per wafer pair. The 0.05/cm2 is CELL-WAFER FOUNDRY's merchant pre-bond figure. Production BSPDN already fusion-bonds a heavily processed logic BEOL surface (15+ CMP'd levels) at a yield the foundries accept. A processed carrier adds a second processed surface, not the first. The carrier is also the cheap side: it can be Surfscan-inspected and then re-cleaned, re-CMP'd or scrapped ($8-12k) before it meets a $30k logic wafer. A thick CMP-last bond oxide removes tier topography. Planning incremental density is 0.001/cm2, giving 1.1% void loss. Total logic scrap is 2.7% ($21/die) with 4 BEOL tiers and the carrier-last steps, or 2.3% carrier-only.

*Action taken:* Void term added to model section 8 (void_D_cm2 0.001, R 2.5 mm). The flow gets pre-bond carrier inspection with re-clean or reject. The seed adds CSAM plus Surfscan on 20 fusion-bonded 200 mm pairs with tier-emulating topography ($45k) to calibrate void size vs particle count. A university cannot reach the fab-grade rate, so the production rate is a foundry/raise milestone.

### RT-PROC-hot-side-memory-05 — MAJOR — PROC — §7-8 U.S. manufacturability (Intel 18A / TSMC A16 bonding and backside line); §4 #10

> The carrier enters the leading-edge logic fab at bonding. It then stays attached through grind, CMP, backside litho, nano-TSV etch, metallization and forming gas, all on tools shared with every 18A/A16 wafer. In, Ga and Zn are not approved materials in leading-edge FEOL-adjacent lines: In and Ga are acceptors in Si, and Zn is a deep-level contaminant. Films at the carrier bevel and edge exclusion, slurry and brush carry-over, and chamber walls all become cross-contamination paths; the typical limit is <=1e10 atoms/cm2 by VPD-ICPMS on backside and bevel. Before any foundry accepts the carrier, the concept needs either dedicated backside tool sets, which it never prices, or a qualified encapsulation and bevel-clean flow.

*What would change the reviewer's mind:* VPD-ICPMS/TXRF data on encapsulated, bevel-cleaned IGZO carriers after a full backside-sequence emulation, showing In/Ga/Zn <=1e10 at/cm2 on all exposed surfaces, plus acceptance by a foundry materials review.

**Response — ACCEPTED-MITIGATED:** Valid for bond-first: the carrier would ride through grind, CMP, nano-TSV etch, metal and forming gas on shared 18A/A16 backside tools while the logic silicon is exposed from the back. Ga and In are acceptors in Si and Zn is a deep-level killer. The carrier-last flow adopted for PROC-01 also removes most of this exposure. The memory wafer arrives only after all backside litho, etch and metallization, and sees only the hybrid-bond, anneal, debond and bump steps, which run on advanced-packaging lines that already handle more materials than FEOL. Added on top: full SiN/Al2O3 encapsulation of the tiers, 2-3 mm edge exclusion with no oxide semiconductor near the bevel, and a bevel etch and clean before the carrier leaves the memory line.

*Action taken:* Seed adds VPD-ICPMS/TXRF ($15k, commercial lab) on encapsulated, bevel-cleaned coupons after backside-sequence emulation. Target: In/Ga/Zn <=1e10 at/cm2 on all exposed surfaces. New kill line: if this fails, bond-first is dead and the carrier host rests on carrier-last. A foundry materials-review sign-off is a raise milestone.

### RT-CIRC-hot-side-memory-04 — MINOR — CIRC — §2 density (ecc_overhead 1.125, RS(36,32)) vs raw_ber_target 1e-4

> Capacity counts only the tier-orthogonal RS(36,32) at 12.5%. The window budget targets raw BER 1e-4, which RAW-BER CONTRACT says needs BCH t=9 (17.6%) against random bit errors. RS(36,32) with 8-bit symbols at 1e-4 has a symbol error rate ~8e-4 and fails ~4e-6 per codeword (P of >=3 symbol errors in 36). Adding an inner BCH cuts the capacity from 89 to ~76 GB per die, and the traffic share with it.

*What would change the reviewer's mind:* A combined random-plus-erasure code that meets 2e-19 per read within the 12.5% budget.

**Response — ACCEPTED-MITIGATED:** Correct: RS(36,32) with 8-bit symbols at raw BER 1e-4 fails 3.6e-6 per codeword (recomputed). The 12.5% cannot also cover random errors. Fix: rows are 2 KB (CIRC-01) and are activated whole, so an inner binary BCH over each 16,384-bit row (m=15) at t=23 uses 345 parity bits (2.1%) and fails at 4.7e-20, below the 2e-19 target. The outer tier-orthogonal RS keeps handling a whole failed tier. Combined overhead is 1.125 x 1.021 = 1.149, against CIRC's 1.32 with a 512-bit BCH. Capacity falls ~2% (not 89 to 76 GB), and reads gain ~20-40 ns of decode latency (~50-80 ns total, still below HBM's ~100+ ns).

*Action taken:* Model: ecc_overhead 1.149, recomputed in section 11(d). Latency quoted as ~50-80 ns. The controller RTL budget includes a row-BCH decoder. The code choice is revisited once Gate A gives the error-cluster spectrum (per RAW-BER CONTRACT).

### RT-CIRC-hot-side-memory-05 — MINOR — CIRC — §2 energy (L_deliver_near_mm 1 vs L_deliver_hbm_mm 8)

> The 1 mm delivery distance assumes every byte sits above its consumer. Tensor-parallel weight slices and KV are read by all SMs, and on an 800 mm2 die the mean distance from an SM to an arbitrary location is ~8-10 mm unless data is strictly partitioned per SM cluster (~0.6 GB per SM). At 56 fJ/mm, delivered energy is ~0.5-0.6 pJ/bit. That makes the ratio to HBM ~6.5x rather than 12x, although watts fall only ~10% (~176 W).

*What would change the reviewer's mind:* A placement and addressing scheme showing that >=80% of near-tier reads are served within 1-2 mm of the consuming SM.

**Response — ACCEPTED-MITIGATED:** Valid: 1 mm assumed every byte sits above its consumer. With random placement the mean SM distance on 800 mm2 is ~9 mm, delivered energy 0.71 pJ/b and the ratio 5.5x. Mitigation: SM-local placement is natural for decode. Each GEMV weight tile is read by exactly one SM every step under a fixed tiling, and FlashDecoding-style KV splits give each sequence chunk to one SM. Both can be pinned to the near-tier region above that SM cluster (~0.4-0.9 GB per SM at 39-78 GB/die) with a NUMA-style address map, as spatial accelerators already do for SRAM. The planning case puts 80% of reads at ~1.5 mm and 20% at ~9 mm, a 3 mm mean: 0.37 pJ/b delivered vs 3.95 pJ/b for HBM, ~11x (15x at 1 mm, 5.5x at 9 mm).

*Action taken:* Model: L_deliver_near_mm 3, with the 1/3/9 mm sweep in section 11(e). The per-bit claim becomes ~10x (5.5-15x). The trace study adds a placement simulation that must show >=80% of near-tier reads within 1-2 mm. Placement or addressing claims go into the IP list as defensive publication.

### RT-DEV-hot-side-memory-04 — MINOR — DEV — §2 write-verify (sigma_place 10 mV, 3 iterations, t_cycle 20 ns)

> On a 0.15 fF node, kT/C at 105-125 C is 5.9-6.1 mV rms and is re-sampled on every write iteration. A 10 mV placement sigma therefore leaves ~8 mV for verify-read noise, write-wordline kickback spread (~5% of a 0.2-0.35 V kick, i.e. 10-17 mV unless the verify captures it) and RTN. Three program/verify loops with an 8-15 ns sense each also make the 2-b write ~50-80 ns, not the 20 ns array cycle used for bandwidth and latency.

*What would change the reviewer's mind:* Measured placement sigma <=10 mV at 105 C with <=3 iterations in <=40 ns on a 64 kb array.

**Response — ACCEPTED-MITIGATED:** Mostly accepted. kT/C on 0.15 fF is 5.9-6.1 mV rms at 105-125 C and is re-sampled on every write. Because verify reads after WWL falls, it captures both kT/C and the kickback spread, so the final placement is a verify-truncated distribution rather than a kT/C draw. A +/-10 mV acceptance window (5.8 mV rms) plus 8 mV verify noise gives 9.9 mV, so the 10 mV placement sigma holds. One try lands within window 90% of the time, and three tries 99.9%. The timing point is right: 3 loops x (5 ns write + 10-15 ns sense) is ~45-80 ns, not 20 ns. Writes are 20% of traffic and posted through logic-side SRAM, and only ~0.13% of one tier's subarrays are active at peak bandwidth, so read latency and bandwidth are unaffected. 1 b needs no verify loop.

*Action taken:* Model: t_write_ns 60. The 2-b write is quoted as ~60 ns posted, and the write energy is 0.54 pJ/b at the port including the global WBL. Gate B (22FDX readout with tiers) measures placement sigma <=10 mV within <=3 iterations in <=60 ns at 105 C. Probe-card coupons cannot time ns loops.

### RT-IND-hot-side-memory-05 — MINOR — IND — §2 Thermal red flag; §4 #4

> All logic heat crosses the tier stack: +2.3 K at 1 W/mm2 average and up to +22.9 K over 10 W/mm2 hotspots without Cu via fill. On a thermally capped ~1-1.4 kW accelerator, even the 2.4 K left after 3% via fill is a clock tax that the energy saving must buy back. The memory itself runs at ~100-114 C, exactly where the 2-b drift spec (<=24 mV) is hardest. So 89 GB per die plausibly becomes 44 GB.

*What would change the reviewer's mind:* Gate C heater data showing <=1 K added at 10 W/mm2 with vias, plus a vendor-side model in which perf/W stays net positive after the thermal tax.

**Response — ACCEPTED-MITIGATED:** Valid as a tax, smaller than feared once the vias are sized to the power map. The tier stack is now 3.84 um because of the series-gate cells. Unvia'd it adds 27 K at 10 W/mm2; 3% Cu fill gives 2.9 K and 10% gives 0.93 K. Revised rule: 10% fill over the ~15% hotspot area and 3% elsewhere, giving 0.93 K over hotspots and 0.29 K at the 1 W/mm2 average, for ~1.5% capacity cost. That meets the reviewer's <=1 K line. The 1-D model ignores lateral spreading, so it is an upper bound. The tax is offset: a share of the ~3.5 pJ/b HBM path (PHY and NoC) is dissipated on the GPU die, and the near tier removes most of it from the hottest die. The '89 becomes 44 GB' point is accepted and already covered by the 1-b planning case.

*Action taken:* Model: via_fill_hot 0.10 and tier_thick 0.24 um. Gate C heater pass tightened to <=1 K at 10 W/mm2 with 10% fill (was <=5 K with 3%). Hotspot regions run 1 b. A perf/W net check (logic clock vs memory-path watts) goes into the M22 data room.

## lean-array-module — LEAN ARRAY MODULE: helium-free, PFAS-light, EUV-free process modules for periodic memory arrays (lean-array-module)

**Final status after red team: DOWNGRADED.** The core H2 physics stands, but with lower odds (effective a_H2 prior 0.19-0.21 against a 0.17 GO line; P4 -> P3) and four tests it was missing (plasma-pretreated surfaces, -70 C chucks, edge-zone etch, IGZO monitors). The step change narrows to the backside-helium hedge: ~3% of DRAM helium, 1.0x $/bit. The PFAS and EUV claims depend on borrowed portfolio cells, AAO at the 1-beta pitch is killed, ZTO is dropped, and the venture IP is thin, so the program is re-scoped as a JDA- and grant-co-funded resilience program.

*Revised verdicts* — Possible: Yes, with lower odds. H2 backside cooling violates no physics, but rotational accommodation puts the effective a_H2 prior at 0.19-0.21 against a 0.17 GO line. P(GO on the worst film) is ~35-55% (P3, was P4). Fallbacks are D2, H2/He blends and asymmetric chuck faces; the cryo GO line is 0.175. AAO is possible only at >= 80 nm pitch (cup AR 12-14); the 1-beta-pitch leg is killed. · Profitable: Axis: supply-chain exposure, narrowed. Backside helium goes from 7.5 L/wafer to 0 in Si-access lines (75-90% of it in oxide-cell lines): ~3% (1-11%) of DRAM helium, the closing step to a helium-free line, at $/bit 1.0x. Fluorocarbon etch gas falls only -25-30%, and only for planar or 80 nm-pitch oxide cells (was 'capacitor fluorocarbon -> 0'). EUV goes to 0 only if a portfolio F~40 nm oxide cell wins. Downgraded from three chokepoints to zero, to one owned lever plus two conditional options. · Doable by this founder: Partly. Yes for the H2 module physics: a $630k three-step experiment (rig M8, small tool M10, 300 mm M20), now with plasma-pretreated, cryo, edge-zone and IGZO-monitor tests, inside a $1.0M/24-month plan. A first look only for the 80 nm AAO cup ($70k coupon). No for IL. No for an investable IP position from data alone; it needs a paid JDA by M10.

### RT-IND-lean-array-module-01 — FATAL — IND — §2.4 Honest size of the helium lever; §3 Prior art (US 10,395,963); §6 IP strategy

> Nothing a $10-50M investor could own survives: H2 as an ESC backside gas is already listed in US 10,395,963 (confirmed by this review's search); the OEMs' live backside-gas-efficiency family (US 9,753,463 and the same-title US 12,493,303, ~2025 by number; family link inferred from title) shows they already engineer helium substitution; the core accommodation dataset is to be published; the residual claims (leak-compensated recipe, per-zone composition, RFO safety) are recipe-level and easy to design around. The economic lever is ~3% of DRAM's helium, $0.32/wafer (104 u$/GB), in fabs that already recapture 80-90%. The value goes to tool OEMs and gas suppliers, and the startup has neither a product nor a royalty base. FATAL to the venture path, not to the physics.

*What would change the reviewer's mind:* An OEM (Lam, AMAT, TEL) or memory maker paying for exclusive access or a licence before the data exists. Or a claim the OEMs must license, e.g., accommodation-mapped pressure control shown to be required for +/-2 K uniformity.

**Response — ACCEPTED-DOWNGRADE:** Accepted as a venture finding, not a physics kill: the mission re-scopes business findings rather than killing on them. The facts stand:
- H2 is named as a backside gas in US 10,395,963.
- The OEMs' gas-efficiency family (US 9,753,463 / 12,493,303) is active.
- The lever is ~3% (1-11%) of DRAM helium, $0.32/wafer.
- The insurance binds only above an 89-99% cut (model I5).
What survives to own is narrow:
(a) the first H2 accommodation dataset on process films, kept confidential until a JDA;
(b) an asymmetric-accommodation chuck face (wafer 0.10 against chuck 0.45 reaches parity at 23 Torr), drafted outside US 8,970,818;
(c) the edge-He guard / per-zone composition and the leak-compensated recipe;
(d) the oxide-channel exclusion rule and monitor protocol, as a qualification package.
None of these is a royalty base a $10-50M investor would underwrite alone. Re-scope: an OEM- or gas-supplier-co-funded program (paid JDA or NRE), grant support for helium resilience (CHIPS R&D/Natcast, DOE), or a module inside the portfolio's lean-line package.

*Action taken:* Venture claim downgraded from 'licensing company' to 'co-funded resilience program'. M10 paid-JDA gate added (RT-IND-02). Dataset publication deferred until after a JDA or M20. The 'provable with $1M' verdict for an investable IP position is now 'no' without a paying partner. The physics verdicts are unchanged by this objection.

### RT-CIRC-lean-array-module-01 — MAJOR — CIRC — §2.3 leak into the plasma (fluorocarbon only) / §0 bundle with oxide cells

> The leak-in analysis covers only fluorocarbon etch chemistry (0.5-1.2% H/F). The same ~1-2.5 sccm of H2 reaches the wafer in every chucked ALD, PECVD and etch step on the oxide-channel tiers this module is bundled with. H is a shallow donor in IGZO, and the portfolio's own budgets are tight. PIXEL-STACK tolerates <=3-20 mV of H-induced delta Vt. HOT-SIDE puts its 24 mV drift budget at ~3 ppm of H in one SiN tier. AND-STACK requires an H-lean mold. A continuous H2 backside source in oxide-tier chambers works against all three, and the GO tests only etch rate and selectivity.

*What would change the reviewer's mind:* An IGZO/ZTO FET split processed with H2 versus He backside gas in every chucked step after channel formation, showing delta Vt <5 mV and no Ioff tail shift. Alternatively, restrict H2 to chambers that never see an exposed oxide channel, and state the share of helium that leaves.

**Response — ACCEPTED-MITIGATED:** Same physics as RT-DEV-02, judged against the portfolio's tightest budgets: PIXEL-STACK 3-20 mV, HOT-SIDE 24 mV at ~3 ppm H, AND-STACK's H-lean mold. I adopt CIRC's stricter test and the restriction. Share of helium that leaves the H2 scope:
- Today's Si-access DRAM: none.
- An oxide-cell line: 10-25% of chucked steps see an exposed or near-surface channel, so H2 replaces 75-90% of backside He, or 69-83% with edge guards in HAR chambers (model I3).
Post-channel chambers that run H-rich chemistry anyway (PECVD SiN, TEOS) stay allowed, because the leak adds 0.2-0.3% to their H. The leak's effect on molecular H2 is also tiny: ~0.15 mTorr partial pressure against ~30 Torr in a forming-gas anneal. The risk is atomic H in plasma steps, which the split measures directly.

*Action taken:* An IGZO/ZTO FET split, H2 vs He backside in every chucked step after channel formation: on a university TFT line in Step 1b and at 300 mm in Step 2. Pass: delta Vt < 5 mV and no Ioff-tail shift at 85 C. The restriction rule and the 10-25% excluded share go into the OEM package.

### RT-CIRC-lean-array-module-02 — MAJOR — CIRC — §2.5 AAO (5.84 fF at 35.2 nm pitch, 11.9 nm mid-plane, EOT 0.55 nm)

> The AAO capacitor geometry does not close. The pore is 0.65 x 35.2 = 22.9 nm, and Cs is computed at an 11.9 nm dielectric mid-plane with 0.55 nm EOT (~5.6 nm of k~40 ZrO2). That leaves ~2.7 nm for the outer electrode and a ~6 nm core for the inner electrode, down a 2.5 um pore: an ALD fill at aspect ratio ~400, against ~60 for today's capacitor, with 2.7 nm TiN walls of very high resistivity. A 1-beta pillar uses convex outer area, while an AAO pore has only concave inner area. The 'parity' 5.84 fF therefore assumes a three-layer conformal fill that has not been shown at this pitch.

*What would change the reviewer's mind:* TEM-verified TiN/ZrO2/TiN fill of >=2 um AAO pores at <=36 nm pitch, with >=5 fF measured per pore and leakage <=1e-7 A/cm2.

**Response — ACCEPTED-KILL:** Valid, and fatal to the 1-beta-pitch AAO leg. Model I6: the pore is 22.8 nm. ZrO2 at EOT 0.55 nm and k 40 is 5.64 nm, and the outer TiN is 3 nm. That leaves a 5.6 nm inner core at AR ~450 for 2.5 um (539 for 3.0 um). The cup offers only concave area, so parity Cs needs this three-layer conformal fill at ~7x today's AR. Resistance is not the blocker (distributed RC ~0.9 ns); the fill is. No plausible variant beats the AR-60 pillar it replaces, and the leg gives no retention gain either (RT-CIRC-03). The module is retargeted to an 80 nm-pitch oxide 1T1C: cup AR 14, with a 20.7 nm hole left inside the top TiN.

*Action taken:* Leg 'AAO capacitor at the 1-beta 35 nm pitch for Si-access cells' killed (kill #6x). Revival condition is CIRC's test: TEM-verified TiN/ZrO2/TiN fill of >= 2 um AAO pores at <= 36 nm pitch, >= 5 fF per pore, <= 1e-7 A/cm2. The rest of the concept is unaffected.

### RT-DEV-lean-array-module-01 — MAJOR — DEV — §2.2 prior a_H2 ~0.27 'before the rotational-mode penalty'; §2.1 free-molecular ratio 2.09x

> The 2.09x H2/He conductance per unit accommodation uses (gamma+1)/(gamma-1) = 6 for H2, which assumes full exchange of rotational energy. H2 has unusually large rotational quanta (J=0->2 at 44 meV, J=1->3 at 74 meV, against kT ~26-30 meV), and its rotational accommodation on surfaces is generally well below its translational accommodation [training knowledge]. At a rotational/translational ratio of 0.1-0.3, the factor is 4.2-4.6, not 6, and the H2/He ratio is ~1.5-1.6x, not 2.09x. In the model's own terms, the 0.27 prior becomes ~0.19-0.21 effective, just above the 0.17 GO line, and the dossier's own logged datum (H2 on W: 0.54 bare vs 0.14 under adsorbed H) points lower. P4 (50-75%) is not supported; ~P3 is.

*What would change the reviewer's mind:* Rig data on SiO2, SiN and CFx coupons giving an effective a_H2 >=0.20, fitted with the same h_gas() formula (which folds rotational exchange into the fitted coefficient).

**Response — ACCEPTED-DOWNGRADE:** Valid. Baule's 0.27 is a translational prior. The 2.09x H2/He free-molecular ratio uses (gamma+1)/(gamma-1) = 6, which assumes full rotational exchange. ORNL measured H2/D2 rotational accommodation on graphite at ~0.05-0.2 (logged). Model I1: effective a = 0.27 x (4+2r)/6 = 0.189-0.207 at r = 0.1-0.3. The free-molecular ratio per unit translational accommodation is then 1.46-1.60x, not 2.09x. Parity pressure is 17.9-19.8 Torr, still inside the 22.5 Torr GO pressure, but the margin over the 0.168 break-even is only +0.02-0.04. The planning value 0.20 was already effective, but the verdict text '0.27 clears 0.17' overstated plausibility. A lognormal prior (1-sigma factor 1.5) gives P(a >= 0.168) of 88% at the old median and 66% at the effective one. The GO needs the worst of four films, which gives 43-66%. With the adsorbate tail (H on W 0.54 -> 0.14), I carry P3 (~35-55%), not P4. D2 has helium's mass and half H2's rotational quanta (model a_eff 0.35-0.39, 1.06-1.21x He's h at 15 Torr). It is added to separate the rotational term from the mass term, and as a recapture-only fallback.

*Action taken:* Prior restated as 0.19-0.21 effective. Plausibility P4 -> P3: P(GO) ~50-75% -> ~35-55%, EV 40 -> 30. D2 added to the Step 1 rig. DEV's test (effective a_H2 >= 0.20 on SiO2/SiN/CFx) is adopted as the marker for a likely drop-in. The GO line stays at 0.17.

### RT-DEV-lean-array-module-02 — MAJOR — DEV — §2.3 leak into the plasma (1.06-2.5 sccm H2); §3 delta 4 (the bundle with oxide cells)

> The concept is bundled with oxide-channel arrays, yet it feeds 1-2.5 sccm of H2 into every chucked plasma step. There it dissociates into atomic H, which diffuses into exposed or near-surface films. IGZO is the most hydrogen-sensitive channel in the portfolio: other dossiers equate ~20 mV of Vt drift with ~3 ppm of the H in one PECVD SiN tier. Steps 1b and 2 test etch-rate and selectivity drift but include no oxide-device Vt or leakage monitor.

*What would change the reviewer's mind:* IGZO TFT monitor wafers run through the H2-cooled chamber at 2x the predicted leak with delta-Vt <=10 mV and unchanged Ioff; otherwise, a rule restricting H2 cooling to chambers that never see exposed oxide channels.

**Response — ACCEPTED-MITIGATED:** Valid: Steps 1b and 2 tested only etch. At the viscous bound the leak carries 5 sccm of H atoms (model I3). That is 0.2-0.3% of the H in recipes that already carry it (PECVD SiN ~1,600 sccm-eq., TEOS ~2,100). In O2-plasma ALD or Ar PVD over an exposed oxide channel it is the dominant H source. Rule adopted: H2 cooling only in chambers whose wafers have no exposed or near-surface oxide channel, or whose recipe carries >= 100x the leak's H. Other chambers keep He or Ar; PVD chucks commonly use Ar already. Share of backside He still replaced: 100% for today's Si-access DRAM, which has no oxide channels, and 75-90% for an oxide-cell line where 10-25% of chucked steps are excluded.

*Action taken:* Step 1b and Step 2 add IGZO (and ZTO if available) TFT monitor wafers through each H2-cooled chamber class at 2x the predicted leak. Pass: delta Vt <= 5 mV (stricter than DEV's 10 mV), an unchanged Ioff tail at 85 C, a PBTI shift no worse than He, and RTN spectra from 10 us to 10 s. Failing chamber classes keep He/Ar (kill #3b, a re-scope).

### RT-DEV-lean-array-module-03 — MAJOR — DEV — §2.5 AAO mold at the 1-beta pitch (35.2 nm pitch, ~23 nm pores, 2.5-3.0 um deep)

> Deleting the AR-60 fluorocarbon etch with AAO creates two harder problems. First, a TiN/ZrO2/TiN MIM must be deposited conformally in ~23 nm pores 2.5-3.0 um deep (AR ~110-130), roughly 3.1-4.5x the AR-squared ALD dose and time of today's AR-62 pillar. Second, the anodic barrier layer at each pore bottom (~1.0-1.4 nm/V x 14 V = 14-20 nm of alumina) must be opened to reach the landing pad. Wet widening cannot be afforded at a 35 nm pitch, and dry barrier etches are typically fluorocarbon or chlorine chemistry. The PFAS-free claim and the 5.8-7.0 fF parity both rest on these unshown steps.

*What would change the reviewer's mind:* A 35 nm-pitch AAO coupon with the barrier opened by a non-fluorocarbon process, a conformal MIM down to the pore bottom (TEM), and >=5.5 fF per pore at <=1e-7 A/cm^2.

**Response — ACCEPTED-DOWNGRADE:** Valid at 35.2 nm. Model I6: mold AR 109-131 means 3.1-4.5x the AR-squared ALD dose of today's AR-62 pillar, and the barrier at ~14 V (~15 nm) must be opened. The PFAS-free and parity claims at the 1-beta pitch rested on unshown steps, and that leg is killed under RT-CIRC-02. Retarget: the portfolio's F = 40 nm oxide 1T1C tiers at an 80 nm square (DUV/imprint-pretextured) or 86 nm hexagonal pitch. Pores are 52-56 nm with 5 nm TiN electrodes, giving 7.2-7.9 fF/um, so 5.4 fF needs 0.68-0.75 um at a cup AR of 12-14. The barrier (~35 nm at ~32 V) cannot be opened by wet etch alone, which would widen the pore ~70 nm, more than the pitch. It is opened by a current-limited voltage ramp-down to ~3-5 nm, then a short H3PO4 dip (~8-10 nm widening) [UNVERIFIED-PK]. No fluorocarbon or chlorine plasma is used. Si-access cells lose the PFAS-free capacitor.

*Action taken:* AAO scoped to >= 80 nm pitch oxide 1T1C only. The $70k seed coupon is re-specified: barrier opening without fluorocarbon, proven by pad contact resistance; TEM of a conformal TiN/ZrO2/TiN down to the pore bottom; >= 5.4 fF per pore at <= 1 um; <= 1e-7 A/cm2.

### RT-IND-lean-array-module-02 — MAJOR — IND — §5 Step 2 (300 mm swap at an OEM demo lab); §7 'First licensees: Lam, Applied Materials and TEL'

> The decisive 300 mm step runs in an OEM demo lab (Lam, Applied's META Center, TEL) or at Albany, and the first licensees are those same OEMs. Once a public coupon rig shows a_H2 >= 0.17, an OEM can qualify H2 in its own chamber within a quarter, using its own ESC, gas-stick and safety IP. The startup's experiment de-risks the OEM's product for free.

*What would change the reviewer's mind:* A development agreement signed before Step 2 that gives the startup paid NRE or a royalty on H2-capable chucks. Or a chuck-face coating patent, drafted outside US 8,970,818, that the OEM cannot route around.

**Response — ACCEPTED-MITIGATED:** Valid: a public coupon result plus an OEM-hosted Step 2 hands the OEM the product. Plan changes:
1. Step 1 data stays confidential until the provisionals are filed and a JDA is signed.
2. A gate before Step 2 (M10): a signed JDA with paid NRE, or a royalty on H2-capable chucks and gas sticks. Without one, Step 2 runs at NY CREATES Albany, a neutral site, as thermal and edge maps only (~$150k), funded from the seed.
3. The asymmetric chuck-face and edge-guard claims are filed before any OEM disclosure.
4. A gas supplier (Linde or Air Products, which sell both He and on-site H2) is approached as a second counterparty, so the startup does not depend on one OEM.

*Action taken:* M10 JDA gate added to sections 5, 6 and 9. Publication policy changed. Provisional #2 (chuck-face asymmetry, edge-He guard) moved before any OEM meeting. $15k JDA legal budgeted.

### RT-IND-lean-array-module-03 — MAJOR — IND — §0 Step change ('EUV ... go to 0'); §2.5 IL/NIL and AAO; §2.6

> The 'EUV out of array modules' claim holds only for F ~40 nm oxide cells, because IL's per-field overlay (6.3 nm) cannot meet 1-beta's 2.5 nm. Those cells give 0.109 Gb/mm2 per tier (0.24x 1-beta) and need >=5 tiers, so the claim depends on a portfolio 3D cell winning. The PFAS claim also leans on borrowed levers: stub or gain cells from other concepts, or an AAO mold at 35.2 nm pitch, below Masuda's ~40 nm floor. Canon NIL is already in trials at SK hynix and Kioxia. Without the borrowed levers, LEAN is a helium hedge worth ~3%.

*What would change the reviewer's mind:* AAO at <=35 nm pitch with <=1e-4 defective pores, or an IL/NIL overlay result on a real cell layer, inside the seed.

**Response — ACCEPTED-DOWNGRADE:** Valid: without borrowed levers, LEAN is the helium hedge.
- EUV-free IL serves only F~40 nm oxide tiers (0.109 Gb/mm2 per tier, >= 5 tiers for 1-beta parity), and Canon NIL trials at SK hynix and Kioxia already occupy that space.
- The PFAS cut (-25-30%) needs a planar oxide cell (MARGIN STACK) or the 80 nm AAO cup on an oxide 1T1C.
- AAO at 35 nm pitch is killed (RT-CIRC-02).
Neither an IL/NIL overlay result on a real cell layer nor sub-35 nm AAO fits inside the seed, so IND's test cannot be met there.

*Action taken:* Step-change claim narrowed to backside He -> 0, the concept's own lever. PFAS (-25-30%, conditional) and EUV (conditional on a portfolio oxide cell) are relabelled 'enabling options for portfolio cells', not LEAN's claim. The FINAL_CONCEPTS line should drop 'PFAS HAR etch and EUV out of array modules'.

### RT-PROC-lean-array-module-01 — MAJOR — PROC — §2.3 leak into plasma '0.5-1.2% H atoms against 420 sccm of F'; §5 Step 1b/2 pass criteria

> The H2 leak enters at the outer seal band, i.e. at the wafer bevel, and flows outward to the pump. The H fraction is therefore not the 0.5-1.2% chamber average. It is concentrated in the outer few mm, where HAR etch already fights edge tilt, CD and polymer balance through edge-ring tuning. The pass criteria are global etch-rate (<=2%) and selectivity (<=5%) drifts. Both can be met while edge-die hole tilt and bottom CD shift enough to lose the outer ring of die, ~5-10% of DRAM die per wafer.

*What would change the reviewer's mind:* Step 2 data at r = 140-148 mm on patterned AR >=40 wafers at 2x the predicted leak: hole tilt <=0.1 deg, bottom CD within 1 nm, and bow within spec versus helium.

**Response — ACCEPTED-MITIGATED:** Valid in substance, overstated in magnitude. Model I2 treats the gas above the wafer as radial advection and diffusion. The H2 diffusivity is 7,900-21,000 cm2/s at 30-80 mTorr, and the Peclet number over 1 cm is 0.04-0.12. The leak enters at r = R, so the edge sees the fully mixed value the dossier quoted: H/F 0.5-1.2% at 500 sccm, 0.17-0.40% at 1,500 sccm. The centre sees 0.42-0.75x of that. The H is therefore not concentrated above the chamber average. But a 1.3-2.4x radial gradient peaks on the outer die, where tilt and CD are already tuned, and the bevel gap sees near-pure H2. Global etch-rate and selectivity criteria could miss that. Redesign: an edge-He guard zone, with He or Ar in the outer backside zone (r > 130 mm) and H2 inside. H2 entering the plasma drops to ~0, and H2 still replaces 73% of that chamber's backside He. In a Si line with guards in HAR chambers, that is 92% overall.

*Action taken:* Step 2 pass criteria add PROC's test: r = 140-148 mm on AR >= 40 patterned wafers at 2x leak, tilt <= 0.1 deg, bottom CD within 1 nm, bow in spec vs He. The edge-guard split runs as the fallback. Step 1b adds a first look at the edge on 200 mm. Kill #5 revised.

### RT-PROC-lean-array-module-02 — MAJOR — PROC — §0 STEP CHANGE 'capacitor fluorocarbon ... go to 0'; FINAL_CONCEPTS 'PFAS HAR etch and EUV out of array modules'

> The PFAS claim holds only for planar oxide 4F2 with a stub (MARGIN STACK). Every 3D cell in the same portfolio brings back a deep fluorocarbon etch (oxide) and Cl/F etch (metal): AND-STACK at AR 60 through ~320 metal/oxide sublayers, DIODE-TOWER at AR 27-53, CHARGE-RIVER at AR 80 plus 60 nm slits, PIXEL-STACK with four AR-24 group etches, and CELL-WAFER FOUNDRY's 64-tier stacks. The module moves the PFAS-heavy etch from the capacitor to the cell stack rather than deleting it.

*What would change the reviewer's mind:* A flow for whichever portfolio cell passes whose deep etches run on non-PFAS chemistry (e.g. cryogenic HF-based etch or a carbon mold with O2 etch), with the profile demonstrated at the AR it needs.

**Response — ACCEPTED-DOWNGRADE:** Valid. The PFAS claim belonged to the capacitor, not the line. Model I8 inventory [ESTIMATE, scc of fluorocarbon etch gas per wafer, NF3 cleans excluded]:
- The capacitor mold is ~38% of a 1-beta wafer's 3,200 scc.
- A planar oxide 4F2 with a stub (MARGIN STACK class), or an F40 oxide 1T1C with an 80 nm AAO cup, gives -27-28%.
- A 3D oxide cell (AND-STACK class) adds ~4,000 scc of deep etch: +88%.
- TEL's HF/PF3 cryo etch ('greatly reduces' CF partial pressure, logged) would bring a 3D cell to about -12%. That is the industry's lever, not LEAN's; patent alternatives such as US 11,075,084 are still hydrofluorocarbons.
So LEAN removes the AR-60 capacitor etch, not PFAS-class etch.

*Action taken:* PFAS claim lowered from 'capacitor fluorocarbon -> 0' (read as PFAS out) to '-25-30% of fluorocarbon etch gas, only for planar or 80 nm-pitch oxide cells'. The deep etches of 3D cells are listed as needing cryo HF/PF3 or the carbon mold (N-29), and are tracked as revival, not claimed.

### RT-PROC-lean-array-module-03 — MAJOR — PROC — §2.5 AAO; §4 #6; kill #6 ('>=1e-4 branched/missing pores')

> Self-ordered AAO forms um-scale domains with random orientation. Pores cannot land on an existing 35.2 nm-pitch storage-node pad array without an imprint pre-texture aligned to the pads at ~3-4 nm overlay, which brings nm-class lithography back in. The Al film must also anodise completely down to a stop layer across 300 mm, where voltage drop in a thin film makes depth non-uniform. Any unanodised Al island shorts neighbouring nodes, and sulfate or oxalate incorporated in the oxide outgasses in later 400 C steps. The kill line of 1e-4 missing pores is 1.7M dead cells per 16 Gb die, beyond redundancy and the entire raw-BER budget.

*What would change the reviewer's mind:* AAO on pad arrays at <=40 nm pitch with >=99.9999% pore-to-pad registration across a 300 mm wafer, no Al-residue shorts, and <=1e-6 missing or branched pores.

**Response — ACCEPTED-MITIGATED:** Valid for the 35.2 nm pitch. Imprint-to-pad registration at 3-4 nm brings nm-class lithography back. At 1e-4 missing pores, 1.7M cells per 16 Gb die are dead, and 12,321 SEC words have two or more failures (model I6), beyond repair and the raw-BER budget. Changes:
1. AAO moves to an 80-86 nm pitch. The overlay budget there is ~F/4 = 10 nm, so the pretexture is an ordinary 193i (or imprint) layer aligned to the pads, with no EUV or nm-class tool.
2. The kill line tightens to <= 1e-6 missing or branched pores: 17k cells per die and ~1 SEC word needing repair. It is shown by counting >= 3e6 pores (0.019 mm2 at 80 nm pitch) with zero defects.
3. Al-residue shorts are tested with interdigitated combs over the pad array.
4. Sulfate and oxalate outgassing is measured by TDS to 450 C, with an ALD Al2O3 seal liner.
Anodization uniformity across 300 mm is post-raise.

*Action taken:* AAO coupon re-specified: 80 nm pitch, 1 mm2 e-beam pad array, automated pore count, combs, TDS. Kill #6 revised to <= 1e-6 at 80-86 nm pitch. 300 mm registration of >= 99.9999% moves to the $10-15M round.

### RT-CIRC-lean-array-module-03 — MINOR — CIRC — §2.5 AAO retention (67 ms at a 13 fA tail)

> AAO's 67 ms at a 13 fA tail is only 5% above 64 ms, and DDR5 refreshes at 32 ms above 85 C. AAO therefore buys no refresh relief and no VRT guard band, and its silicon-access route keeps every circuit-side cost of today's DRAM. The 76 mV signal also uses a different droop convention from A1's 50 mV at 5.42 fF, which flatters the comparison.

*What would change the reviewer's mind:* Signal and retention restated on A1's droop convention with a >=2x VRT guard.

**Response — ACCEPTED-DOWNGRADE:** Valid on substance. The convention point cuts the other way. On A1's convention (50 mV end-of-retention signal, Cbl 34.7 fF; model I7):
- The 1-beta pillar gives 71 mV fresh and 64 ms.
- The 35 nm AAO cup gives 76-88 mV fresh and 80-123 ms (1.25-1.9x). The original 67 ms, on a fixed 0.15 V droop, understated it rather than flattering it.
- With a >= 2x VRT guard, none clears 128 ms with margin, so there is no refresh relief, and the leg is killed anyway (RT-CIRC-02).
- Refresh relief can only come from oxide access: the 80 nm cup (7.2 fF) on a 1 aA IGZO tail holds ~1,670 s.
Top-ups: I-12302 plate-strip sensing (~135 vs ~14 mV) is a 3D-array sensing circuit with planar Micron prior art, outside a process module. I-12627's series write transistors do not stack the Si storage-node junction/GIDL leakage. Neither rescues Si-access AAO.

*Action taken:* AAO claims no retention or refresh benefit. Signal and retention are restated on A1's convention in section 2.5 and model I7. Refresh credit goes to the oxide access device only. I-12302 and I-12627 are not adopted.

### RT-CIRC-lean-array-module-04 — MINOR — CIRC — §0 thesis 'delete the fluorocarbon capacitor etch' / §1 module table

> The PFAS step depends on the circuits working elsewhere. 'Stub or gain cells delete the HAR etch outright' holds only if MARGIN STACK's circuits, or a capacitorless cell, pass their GO. MARGIN STACK's 120 nm stub, the VCT pillar etch and the buried-bitline etch still use fluorocarbon chemistry. The module deletes the AR-60 step, not PFAS-class etch.

*What would change the reviewer's mind:* A fluorocarbon gas inventory per wafer, before and after, for the specific cell the module ships with.

**Response — ACCEPTED-DOWNGRADE:** Valid. Inventory per model I8 [ESTIMATE, scc of C4F6/C4F8/CF4/CHF3 per wafer]:
- 1-beta: 3,200, of which the capacitor mold is 1,200.
- MARGIN STACK + LEAN: 2,340 (-27%). The 120 nm stub, VCT pillar and buried-bitline etches stay fluorocarbon.
- F40 oxide 1T1C + 80 nm AAO: 2,300 (-28%).
- AND-STACK class: 6,000 (+88%).
The module deletes the AR-60 step, not PFAS-class etch. The circuit dependence CIRC names (MARGIN STACK's GO) holds: without a planar or oxide cell, LEAN's fluorocarbon lever is zero.

*Action taken:* Thesis reworded to 'delete the AR-60 capacitor-mold etch (~25-30% of fluorocarbon etch gas) where a planar or 80 nm-pitch oxide cell allows it'. Inventory table added (section 2.8), to be refined with partner gas-use data in Step 2.

### RT-DEV-lean-array-module-04 — MINOR — DEV — §5 Step 1 rig (static gas, coupons at 20-60 C)

> The rig measures accommodation on coupons in static gas. Production backsides under bias are plasma-heated, H-terminated, polymer- or fluoride-contaminated and ion-bombarded at the edge, and accommodation is set by the outermost monolayer. Sandia's Ar-plasma clean shifted He by up to 0.10, so a static-gas coupon can misstate a_H2 by more than the 0.17-0.24 band that separates GO from drop-in.

*What would change the reviewer's mind:* Step 1b thermocouple-wafer data under plasma agreeing with the rig-fitted a_H2 within +/-0.03.

**Response — ACCEPTED-MITIGATED:** Valid. Accommodation is set by the outermost monolayer, and Sandia's Ar-plasma clean moved He by up to 0.10, which is more than the 0.17-0.24 GO-to-drop-in band. The rig changes:
- Coupons are pretreated in situ in a load-locked side chamber (Ar, O2, C4F8 polymer, H2 plasmas) and measured without an air break.
- Production backsides pulled from a partner's HAR flow are measured as received.
- The GO is judged on the worst pretreated surface.
DEV's test becomes a formal gate: the Step 1b thermocouple-wafer a_H2 under plasma must agree with the rig within +/-0.03 at M10. If it does not, kill #1 is re-judged on in-plasma data (kill #3c).

*Action taken:* +$20k for plasma pretreatment and vacuum transfer in Step 1; production-backside coupons added; M10 rig-vs-plasma gate (+/-0.03) added to sections 5 and 9.

### RT-DEV-lean-array-module-05 — MINOR — DEV — §4 #10 Ga-free ZTO / In-lean channels (N-26)

> Ga-free ZTO usually needs >=400-500 C anneals to reach low trap density. ZTO made at BEOL temperature shows larger hysteresis, more PBTI and Sn2+-related subgap states, and its ~1,500 s 2T0C result is on a long channel. Ioff <=1 aA at Lg <30 nm is unshown, so the materials module may trade a gallium risk for a leakage risk.

*What would change the reviewer's mind:* Short-channel (Lg <=40 nm) ZTO FETs made at <=400 C with SS <=90 mV/dec and extracted Ioff <=10 aA at 85 C.

**Response — ACCEPTED-DOWNGRADE:** Valid. Short-channel ZTO made at <= 400 C with aA-class Ioff is unshown, and its Sn2+ subgap states, hysteresis and PBTI make it a leakage risk. Model I9 shows the gallium it was meant to remove is small. A fab of oxide cells uses 10 nm of IGZO at 3x the wafer area, over 5 tiers at 30% utilisation. That is ~60 kg of Ga a year per 100k-wpm fab, and a 10-year stockpile costs ~$0.4M, under an hour of fab revenue. Gallium exposure is a stockpile item, so ZTO's leakage risk is not worth taking.

*Action taken:* N-26 ZTO is dropped from LEAN's claims and seed budget. The materials claim changes from 'Ga out' to 'Ga stockpiled (~60 kg/yr per fab)'. Revival (kill #9) is DEV's test: anyone reports Lg <= 40 nm ZTO at <= 400 C with SS <= 90 mV/dec and Ioff <= 10 aA at 85 C.

### RT-IND-lean-array-module-04 — MINOR — IND — §2.4 Insurance value (2.4-day payback); §8 Resources (helium storage, U.S. buffer)

> The 2.4-day payback assumes a stoppage that the dossier's own logic says fabs avoid. Under a partial cut they shed leak check, diluent and purge first and keep backside cooling. The dossier also notes ~6 weeks of storage and that U.S. fabs are 'relatively buffered'. The hedge pays only in a near-total, prolonged cutoff. If Qatar's output resumes (not checked here), the urgency that motivates customers disappears.

*What would change the reviewer's mind:* Fab helium use-split data (the planned M6 requests) showing backside cooling >10% of fab helium, plus a credible scenario in which it is the binding use.

**Response — ACCEPTED-DOWNGRADE:** Valid. Backside cooling binds only when a fab's cut exceeds 97% (89-99%) after ~6 weeks of storage. A logged search (gasworld, AGBI 2026) shows Qatar has partly restarted Helium 2:
- output is estimated at below ~30% of normal;
- two damaged LNG trains need 3-5 years of repair.
So 2026-27 tightness persists, but a full fab stoppage is not the base case. Model I5 [SPECULATIVE probabilities]: at a 0.5-3% annual chance of a binding 30-day cutoff, the expected value is $5-29M/yr per fab. That recovers $150M brownfield in 5-32 years, or $82M greenfield in 3-17 years. The value is option value for tail risk, plus the closing step to a fully helium-free line.

*Action taken:* '2.4-day payback' replaced by the binding-threshold and expected-value table (section 2.4). The M6 use-split re-scope gate is kept (if backside is > 10% of fab He, the hedge value rises). The pitch moves to greenfield dual qualification.

### RT-PROC-lean-array-module-04 — MINOR — PROC — §2.7 GO matrix at 20/40/60 C; §4 #4 'Etch chambers first (<~100 C)'

> The newest HAR etchers (TEL's cryogenic channel-hole etch, Lam Cryo 3.0) run their chucks at roughly -60 to -70 C. That is where high-bias heat removal is hardest and where the helium stake is highest. Light-gas accommodation shifts with surface temperature and adsorbate films (the dossier's own H-on-W 0.54 -> 0.14), and the test matrix stops at 20 C.

*What would change the reviewer's mind:* a_H2 measured at -70 to 0 C on the same film and chuck faces, staying >=0.17.

**Response — ACCEPTED-MITIGATED:** Valid. Cryogenic HAR etchers run their chucks at about -60 to -70 C (TEL's HF/PF3 cryo etch is logged at about -60 C), and that is where high-bias heat removal is hardest. Model I4 uses 220 K gas. Normal H2 has gamma 1.43 there (rotation partly frozen), which lowers the free-molecular ratio per unit a from 2.09x to 1.99x. The break-even moves from 0.168 to 0.175 (drop-in 0.251, clamp limit 0.102). The gas physics barely moves. The risk is the surface: condensed by-products and adsorbed H, which shifted H on W from 0.54 to 0.14. The matrix therefore extends to -70 C.

*Action taken:* An LN2-cooled cold plate (-70 to 60 C) is added to the rig. The cryo GO is a_H2 >= 0.175, judged separately from the 20-60 C set. Kill #1c added. If cryo fails, cryo chambers alone keep He.

### RT-PROC-lean-array-module-05 — MINOR — PROC — §2.4 'Retrofitting 1,500 chambers at $50k ... pays back after 2.4 days'

> Changing the backside gas on an HVM HAR etch chamber is a process change. It requires requalifying every product route through the chamber, customer PCNs for automotive and server DRAM, and re-baselining the backside-flow and leak fault-detection limits that use He flow as a clamp-health signal. $50k per chamber and a 2.4-day payback ignore months of qualification wafers. The insurance value is real, but the payback is misstated.

*What would change the reviewer's mind:* An OEM or fab estimate of per-chamber requalification cost and time for a backside-gas change.

**Response — ACCEPTED-MITIGATED:** Valid: the $50k per chamber was hardware only. Model I5 adds per-family requalification at 30-80 families x $0.5-3M. That gives $90-315M per 100k-wpm brownfield fab and a payback of 2.8-9.9 days of full stoppage (mid case 4.7, was 2.4). It also takes 6-12 months of lead time, so it cannot be done during a crisis. Qualifying H2 during a greenfield ramp costs ~10% incremental, ~$82M, with a 2.6-day payback. The workaround is dual-gas qualification at new fabs (Micron Idaho/New York, new Korean lines), not brownfield retrofits.

*Action taken:* Payback restated in sections 2.4 and 2.6. Go-to-market moved to greenfield dual qualification. PROC's test (an OEM or fab estimate of requalification cost and time) is requested from the Step 2 partner by M14.

## margin-stack — MARGIN STACK: segment-gain, double-sampled, ECC-budgeted sensing that cuts the cell capacitor ~10x on oxide-access DRAM (margin-stack)

**Final status after red team: DOWNGRADED.** The physics stands: with a 2-pillar gain FET, 64-cell segments and 4:1-muxed signal-first double sampling, the sensing-limited cell is 0.13/0.29/0.74 fF (optimistic/central/pessimistic), so the 0.5 fF planning cell closes in the central case, and the 1.0 fF fallback closes in all three. But the promise shrinks. (1) RTN heavy tails and a weaker gain FET kill the 17-40x stretch. (2) A leakage tail derived from the model's own inputs kills the 28x refresh claim; the retention requirement becomes an ECC-budgeted 2e-5 quantile. (3) 2-4 added EUV-class layers plus BCH parity turn $/bit into a +9% to +25% penalty and density into -11% vs plain 4F2. (4) The $1M experiment still cannot measure VCT coupling, the VCT sidewall leakage tail or the real mask count. (5) SEL prior art narrows novelty.

*Revised verdicts* — Possible: Yes (revised after red team). No new physics. Sensing-limited Cs is 0.13/0.29/0.74 fF; 0.5 fF closes in the central case (P(err) 8e-7 vs a 9e-5 target) but not the pessimistic one, and the 1.0 fF fallback closes in all cases. Retention needs the aged 2e-5 IGZO leakage quantile <= 586 aA (model estimate ~100-260 aA); the 1e-10 tail derived from the inputs is 1.5-5.5 fA fresh. · Profitable: Narrowed. Axis: capacitor-module resource intensity plus 3D readiness. The capacitor goes 5.42 -> 0.5 fF: 10.8x shorter, AR 62 -> 5.7 (5.4x at the 1.0 fF fallback), i.e. ~10x less HAR capacitor etch, ~100x less ZrO2/TiN ALD exposure, and no Ru/k>50 push. A 3D-tier lateral capacitor shrinks to 63-127 nm from ~450 nm (per-tier density 2.2-2.8x, break-even ~10-13 tiers vs ~26), conditional on a 3D host. It is NOT a step on $/bit (+9% to +25% penalty, central +17%), density (-11% vs plain 4F2), latency or array energy (1.3x). Refresh gains of 2-12x are conditional and belong mostly to oxide access. · Doable by this founder: Partly. A $563k decisive experiment ($999k plan, 17 months) measures four things: the circuit residual and muxed double sampling on a 22FDX emulator with ratio-matched coupling, error pairs (DRAM Bender), IGZO gain-FET RTN at a 1-3 ns gap on an oxide-on-CMOS carrier, and the 2e-5 leakage quantile directly on >=1e6 planar and etched-sidewall IGZO cells after a 1,000 h stress. VCT coupling alpha, the VCT sidewall tail and the added mask count stay projections (field solver, process emulation) until partner silicon.

### RT-CIRC-margin-stack-01 — MAJOR — CIRC — §2.6 area / model §7 density; §5 MPW global CDS

> The global CDS comparator does not pitch-match. There is one global line per buried bitline at 2F = 29.4 nm pitch, serving 16 segments x 32 cells = 512 cells (c_gbl_fF 6 fF = 15 um line), so each comparator gets 15 um x 29.4 nm = 0.44 um2 of under-array area. Each one needs an auto-zeroed comparator, two 10 fF sampling caps (c_sample_fF), a delayed-compare flag latch and a write-back driver. A plain 8-10-device DRAM latch SA already uses ~0.4-0.9 um2. The +8.8% die figure counts only the 4 in-array sites per segment and prices none of this. The fixes cost elsewhere. Lengthening the global line to 32-64 segments raises C_GBL to 12-24 fF, cuts local gain from 3 to ~0.75-1.5 and multiplies the comparator term 2-4x. Muxing comparators serialises restore of a destructively read row.

*What would change the reviewer's mind:* A layout of the full CDS comparator + sampling + restore + flag cell at <=0.44 um2 per 29.4 nm column, or a re-run of §2.3 and §7 at the global-line length that does fit, showing sigma_res and die area.

**Response — ACCEPTED-MITIGATED:** Valid: per-column CDS needs ~1.15 um2 against 0.443 um2 (260%; model R7). Redesign: 64-cell segments, 16 per 1,024-cell global line, which gives 0.885 um2 under the array per column. One auto-zeroed comparator (two 5 fF caps) serves 4 columns using signal-first double sampling: sample the signal with the WL open, reset the segment, sample the reset level, compare. Each column keeps only a precharge, a mux switch, a 4T restore latch and a write driver: ~0.55 um2 (62%), leaving room for sub-WL and line drivers. The comparator holds the signal sample, so muxing never loses the destructively read segment; all columns restore in parallel from their latches (3.1 ns). Consequences, re-run: C_GBL 12 fF, so G 0.9 and a 4.3 mV comparator term; segment-reset kTC (1.22 mV) and 1 mV of reset injection are no longer cancelled; decisions at 11.4 ns (13.4 ns with WL rise vs 14 ns tRCD); array energy 15.2 fJ (1.3x below 1-beta, was 2.3x). Net: central Cs 0.29 fF, and 0.5 fF closes.

*Action taken:* Model R7 and the new inputs (n_seg 64, c_gbl 12 fF, comp_mux 4, c_sample 5 fF). The MPW includes the full column cell. Gate at M7: layout <= 0.885 um2 per column including 1/4 comparator, else 2,048-cell columns at G ~0.45. Energy claim revised to 1.3x.

### RT-CIRC-margin-stack-02 — MAJOR — CIRC — §2.6 cost / §2.7 table (density 0.701 Gb/mm2, $/bit flat)

> ECC parity is missing from the density and $/bit numbers. The model gets 0.701 Gb/mm2 as 0.762/1.087, which counts only the segment overhead. The design needs BCH t=8, 80 check bits per 512 (15.6%), against the 6.25% on-die ECC already in A1's '16Gb + ECC' baseline (cells_16gb 1.7e10). That is a further x1.088 of die area, so density falls to ~0.644 Gb/mm2. At a capacitor-module share of 10/15/20%, $/bit becomes +12.7/+9.3/+5.8%, not +3.6/+0.4/-2.8%. RAW-BER CONTRACT's own corrected target (2e-19 per read) needs t=9 (17.6%), which is worse again. MARGIN STACK is a ~6-13% $/bit penalty on 4F2, not 'flat'.

*What would change the reviewer's mind:* An architecture that carries the t=8 code in bits that already exist (for example the RDIMM side band) without extra array bits, or a sourced capacitor-module cost share of >=30% from a teardown cost model.

**Response — ACCEPTED-DOWNGRADE:** Valid in substance. BCH t=8 adds 80 check bits per 512 against the baseline's 6.25% on-die ECC: x1.088 array bits. Scaling only the array (70% of a PUC die) gives die x1.062 plus 0.5% for decoders, not x1.088 on the whole die. After segments and parity, density is 0.677 Gb/mm2 (-11% vs plain 4F2, 1.51x 1-beta). Combined with PROC-01's layers, $/bit is +9% to +25%: the reviewer's 'penalty, not flat' holds. A server variant carries the code in the existing RDIMM side band (512 + 128 bits, BCH-12, as in RAW-BER CONTRACT) with no on-die code and no extra array bits, at the cost of chipkill.

*Action taken:* Parity and decoder area added to model R9. Density and $/bit revised in sections 0 and 2.7. The side-band variant is noted for x4 server parts.

### RT-CIRC-margin-stack-03 — MAJOR — CIRC — §5 decisive experiment (22FDX MPW, M16-17 GO by projection)

> The experiment cannot measure the two terms that set Cs. The GO statistic is sigma_res with coupling folded in, and §2.8 shows that alpha alone moves the 0.5 fF threshold from 23.5 mV (alpha 0.05) to 14.5 mV (alpha 0.20). The MPW is Si FD-SOI with MOM stubs and BEOL-metal segments. Its gain FETs have AVT ~1-2 mV*um and no IGZO trap noise, and its coupling geometry has nothing to do with a buried bitline at 29 nm pitch under vertical-gate wordlines. Oxide 1/f comes from coupons and is 'combined by projection' (§5 step 7). Neither alpha nor the oxide gain-FET residual is measured in situ, so D=5 ('decisive binary for <=$300k') is overstated.

*What would change the reviewer's mind:* Partner TCAD or field-solver alpha for a VCT 4F2 buried bitline, calibrated to published Samsung or SK hynix 4F2 coupling data, plus a measured IGZO gain-FET + CDS population (>=1,000 devices) at the real ~15 x 60 nm pillar footprint.

**Response — ACCEPTED-DOWNGRADE:** Valid: neither alpha nor the oxide gain-FET residual is measured in situ. Mitigations: ratio-matched programmable coupling plus field-solver alpha (PROC-02); oxide-native double sampling on >=1e4 IGZO gain FETs at the pillar gate area (2,827 and 5,655 nm2) at 1-3 ns on the BEOL-IGZO carrier (DEV-04); 22FDX gain FETs used only for circuit statistics (comparator, kTC, kick, muxing). Remaining gap: real VCT geometry and pillar-sidewall IGZO. The decisive binary becomes 'circuit plus oxide device statistics', not 'VCT array'.

*Action taken:* D lowered from 5 to 3 in section 0. The GO/NO-GO reports a projected BER with a measured-vs-projected column and an uncertainty band. Partner VCT/OCTRAM silicon is the first raise milestone.

### RT-CIRC-margin-stack-04 — MAJOR — CIRC — §2.3 post-CDS residual (sigma_1f_rtn_mV 4.0, Gaussian) / §2.9 GO metric

> RTN is treated as a 4 mV Gaussian, but it has a heavy per-device tail. A 15 nm x 60 nm GAA pillar at 2 nm EOT has Cox*W*L ~ 17.3 fF/um2 x 0.0028 um2 = 0.049 fF. One trap therefore gives q/(Cox*W*L) ~ 3.3 mV, and percolation in oxide channels typically multiplies that 2-5x. RTN amplitudes are exponentially distributed across devices, as PIXEL-STACK's own rtn_mult note says, so the 1e-4 device quantile is ~7-9x the mean: ~25-45 mV, not 3.72 x 4 = 15 mV. A gain FET whose trap toggles between the two samples errs on all 32 cells it serves. The 0.5 fF planning cell survives with ~78 mV of post-coupling signal. The 0.09-0.32 fF row-I stretch (17-40x) does not, and a sigma-based GO threshold is the wrong statistic.

*What would change the reviewer's mind:* A measured per-device RTN amplitude distribution on >=10k scaled IGZO FETs at 85 C with a 5-15 ns sample gap, with a 1e-4 quantile <=15 mV, and a GO restated as a measured BER tail rather than sigma_res.

**Response — ACCEPTED-DOWNGRADE:** Valid; confirmed in model R3. For one pillar the 1e-4 between-sample jump quantile is 40 mV central and 65 mV pessimistic, against 15 mV for a Gaussian 4 mV. A toggling gain FET can err on any of the 64 cells it serves, but only one cell per segment is read per activation, and row codewords put each of those cells in a different codeword, so its errors stay iid across codewords. With two pillars and the heavy-tail statistic, the central quantile is 22.6 mV and 0.5 fF survives with P(err) 8e-7, as the reviewer predicted; the 17-40x stretch does not. GO is restated as a projected BER tail, not sigma_res.

*Action taken:* Stretch withdrawn. GO = projected BER <= 9e-5 at 0.5 fF from the measured Gaussian residual plus a measured per-device RTN distribution (>=1e4 IGZO FETs, 1-3 ns gap, 85 C). K9 added.

### RT-CIRC-margin-stack-05 — MAJOR — CIRC — §2.4 ECC / §1 read timing (3.6 ns vs 14 ns tRCD)

> On-die ECC latency and write granularity are not costed. A 592-bit codeword per device is 9x a DDR5 x4 burst (64 bits), so every access must fetch and decode 592 bits, and any write narrower than 512 data bits per device becomes a read-modify-write. That is the DDR5 on-die-ECC write penalty on a 4x larger codeword. At raw BER 1e-4, 1-(1-1e-4)^592 = 5.8% of reads take the BCH slow path: >=8 Berlekamp-Massey iterations plus a Chien search over 592 positions, ~10-20 ns at DRAM-periphery speed [ESTIMATE]. That lands in p95 read latency. Neither the 3.6 ns sense chain nor the tRCD comparison includes it.

*What would change the reviewer's mind:* A synthesis estimate of t=8 BCH decode latency and area per bank in a DRAM-periphery-class process, plus a column path that delivers 592 bits per access at DDR5 rates, folded into tCL, tCCD_WR and die area.

**Response — ACCEPTED-MITIGATED:** Valid. At raw BER 1e-4, 5.75% of 592-bit codeword reads take the BCH slow path (+~15 ns); the mean penalty is +0.86 ns. At 1e-5 it is 0.59% and at 1e-6 0.06% (model R8). 1e-4 is the 85 C worst-pattern design corner, so the slow path is a p95 tail only near that corner. Granularity: a 592-bit on-die codeword suits wide-IO parts (HBM pseudo-channel, LPDDR x16 BL32 = 512 bits per access). For DDR5 x4 RDIMMs the code moves to the module side band (BCH-12 over 512 + 128 bits, decoded in the controller), giving up chipkill. Narrow on-die writes are read-modify-write, as in DDR5 on-die ECC. Decoder area (0.5% of die) is in the cost.

*Action taken:* Contractor scope M2-7: synthesis estimate of the t=8 BCH decoder (latency, area per bank) in a 22-28 nm-class library. Model R8. The latency penalty and the wide-IO / side-band split are stated in section 2.10.

### RT-DEV-margin-stack-01 — MAJOR — DEV — §2.5 retention / §2.9 GO 3; model INPUTS ioff_igzo_median_aA=1, sigma_vt_access_mV=50

> The 0.5 fF planning cell is set by the IGZO 1-in-1e10 leakage tail, yet the dossier never derives that tail from its own inputs. With the model's sigma_vt_access_mV = 50 and a realistic 85-100 mV/dec slope at 85 C (ideal 71), the 6.36-sigma low-Vt cell sits 318 mV lower and leaks 3.2-3.7 decades (1,500-5,000x) above the median: 1.5-5 fA if OCTRAM's '<1 aA' is an 85 C median (its test temperature and statistic are unpublished; rt-DEV.jsonl). That is 2.6-8.5x over the 586 aA GO line; even with the droop-optimised 370 mV allowance, 0.5 fF holds only 37-123 ms, so the 917 ms refresh and 28x refresh-power claims collapse. The coupon plan (>=1,000-cell 2T droop arrays plus a lognormal fit) observes only to ~3.1 sigma and extrapolates 3 more sigma on an assumed shape.

*What would change the reviewer's mind:* A negative WL hold that puts the -6.4-sigma cell >=1.2 V below threshold, shown on >=1e6 IGZO VCT cells at 85 C with a measured 1e-6 quantile <=60 aA and sigma_Vt <=25 mV, so that the 1e-10 extrapolation is short.

**Response — ACCEPTED-DOWNGRADE:** Valid. The model now derives the tail from its own inputs (model R5): Tail(q) = Ioff_med x 10^((Q^-1(q) x sigma_Vt + drift - V_NWL)/SS). Reading OCTRAM's '<1 aA' as the 85 C median, sigma_Vt,access 50 mV and SS 85/90/100 mV/dec, the fresh 1e-10 tail is 5,520/3,420/1,516 aA (2.6-9.4x over the 586 aA line for 0.5 fF at 64 ms and 75 mV droop), and 8.5-42 fA after 75 mV of drift. The pre-red-team 917 ms refresh and 28x refresh-power claims, and a 1e-10 GO line, do not survive. Redesign 1, an ECC-budgeted retention quantile: 1e-5 of the 1e-4 raw-BER budget goes to retention-weak cells (Hi-ECC precedent). A leaky cell errs only while it holds the vulnerable value, so the allowed leaky-cell fraction is 2e-5 (4.11 sigma, not 6.36). Averaged codeword failure is unchanged because Poisson counts add (592 x (9e-5 + 1e-5) gives 2.33e-17). The 501 codewords per die with >=2 weak cells are handled by sort-time repair and patrol scrub. At 2e-5 the tail is 113-261 aA fresh and 101 aA aged with a -0.1 V negative-WL reserve (SS 90). That passes 586 aA with 5.8x margin, and >=1e6 cells see it directly (~20 tail cells), so no 3-sigma extrapolation is needed. Redesign 2, negative WL hold: wide-gap IGZO has no GIDL/BTBT penalty, so each ~90 mV of hold buys a decade of channel leakage. -0.3 V brings even the aged 1e-10 tail to ~11 aA, but only for the subthreshold-channel component, not for trap-assisted or dielectric paths. Refresh: with the revised noise, 0.5 fF tolerates 241 mV of droop, giving a 591 ms (central tail) to 94 ms (SS 100, no reserve) refresh, i.e. 11.8x to 1.9x less refresh power. That gain belongs mostly to oxide access; a plain oxide 4F2 cell gets more of it.

*Action taken:* Refresh-power claim withdrawn (28x becomes a conditional 2-12x, not credited to MARGIN STACK). The 1e-10 requirement is replaced by an aged 2e-5 quantile <= 586 aA (conditional <= 1,881 aA at 241 mV droop), measured directly on >=1e6 cells on the BEOL-IGZO-on-CMOS carrier and on coupons, with a 0 to -0.5 V negative-WL-hold sweep. Model R5/R6 added; GO 3, K2 and K3 rewritten; 0.5 fF planning cell kept with a 1.0 fF fallback.

### RT-DEV-margin-stack-02 — MAJOR — DEV — §2.3 residual budget and §9 sense timing (model of the dossier); model INPUTS i_gain_uA=5, gain_local=3, vov_gain_V=0.4

> The 1.89 mV comparator term and the 0.72 ns sample time both rest on 5 uA (gm 25 uS) from a same-step, high-Vt IGZO gain FET at 0.4 V overdrive, and no source supports that. Scaling OCTRAM's >15 uA (at an undisclosed, typically 1.5-2.5 V overdrive) down to 0.4 V gives 0.4-4 uA and gm ~2-10 uS, so the local gain G = gm*t/C_GBL is 0.23-1.2 at 0.7 ns on 6 fF, not 3. The comparator then refers to ~5-25 mV at the input (with the -4-sigma 0.53 gm factor), central sigma_res rises from 5 to ~7-25 mV and Cs from 0.14 to ~0.15-0.64 fF (§2.8 table at alpha 0.1), and the stretch case disappears. Restoring G = 3 needs 1.8-9 ns per sample, which makes sense-plus-restore 6-20 ns against a ~14 ns tRCD and widens the 1/f+RTN window.

*What would change the reviewer's mind:* Measured Id-Vg at 85 C on a VCT-geometry IGZO FET (15 nm pillar, 60 nm Lg, the same high-Vt step) giving >=4 uA at Vov 0.4 V; or a multi-pillar/back-gated gain stage whose area is carried in the +8.8% die figure.

**Response — ACCEPTED-MITIGATED:** Valid; reproduced in model R2. A square law through OCTRAM's 15 uA at an assumed 2.0 V (1.5 V) overdrive gives 0.60 (1.07) uA and gm 3.0 (5.3) uS at 0.4 V, so G = 0.36 (0.64) in 0.72 ns on 6 fF, not 3. Redesign: two parallel same-step gain pillars (+1 site per segment, carried in the area: 5 sites per 64 cells, +5.5% die), a deeper pulsed read source to Vov 0.6 V (about -1.1 V for a ~1 V Vt; Vds <= ~2 V suits wide-gap IGZO), and 1.2 ns samples. That gives gm 9 uS, I 2.7 uA and G 0.90 on the 12 fF global line CIRC-01 forces (pessimistic 0.48, optimistic 1.87). The input-referred comparator term is 4.3 mV central (12.8 pessimistic), not 1.9 mV. With all terms and the RTN tail, the sensing-limited Cs is 0.13 / 0.29 / 0.74 fF (optimistic / central / pessimistic). 0.5 fF closes in the central case (P(err) 8e-7 vs 9e-5) but not the pessimistic one, so weak drive moves the planning cell to 1.0 fF. Timing: 4:1-muxed signal-first double-sampling decisions at 11.4 ns (13.4 ns with WL rise, vs a 14 ns tRCD), plus a 3.1 ns parallel restore. The 3.6 ns read-chain claim is withdrawn.

*Action taken:* Model inputs changed: n_gain_pillars 1 -> 2, vov_gain_V 0.4 -> 0.6, t_sample 1.2 ns, and i_gain and G now computed from k = 3.75 uA/V2. The MPW emulates 1/2/4-pillar gain stages. The BEOL carrier measures Id-Vg and gm of IGZO FETs at gate areas matched to 1 and 2 pillars, at 0.3-0.8 V overdrive and 85 C. Pass: >= 2.7 uA at 0.6 V for the 2-pillar area. Below G 0.5, the planning cell moves to 1.0 fF.

### RT-DEV-margin-stack-03 — MAJOR — DEV — §2.3 'oxide 1/f + RTN between samples 4.0 mV [SPECULATIVE]' folded into a Gaussian 3.72-sigma RSS

> RTN is budgeted as a 4 mV Gaussian term, but in a 15 x 60 nm IGZO pillar FET (gate area ~2,800 nm^2, EOT 2 nm) one trap shifts Vt by q/(Cox*W*L) ~3.3 mV on average. Amplitudes are exponentially distributed and enhanced 2-3x by percolation in amorphous channels (eta ~7-10 mV). If 1-30% of the ~5.3e8 gain FETs on a 16Gb die carry a trap whose time constant lies within 10x of the 0.7-5 ns sample gap, the 1e-4 per-read quantile is eta*ln(50-1,500) = 4-7 eta, i.e. ~13-70 mV, against the 15 mV a Gaussian 4 mV implies. CDS cancels only traps that do not switch between samples. This erases the 0.14-0.25 fF stretch and consumes 17-90% of the ~78 mV left at 0.5 fF after coupling and kick.

*What would change the reviewer's mind:* Per-device, time-domain RTN statistics on >=1e4 scaled IGZO FETs at 85 C with 1-10 ns resolution, showing the 1e-4 quantile of between-sample Vt jumps <=15 mV.

**Response — ACCEPTED-DOWNGRADE:** Valid. RTN is now an explicit exponential heavy tail (model R3), not a 4 mV Gaussian. The mean jump of an active trap is eta = m x q/(Cox W L), where q/(Cox W L) = 3.28 mV for one 15 x 60 nm pillar at 2 nm EOT and 1.64 mV for two, and m = 2-3 for percolation (a logged TU Wien source gives heavy tails in percolative channels). The active-trap fraction is 1-30% per pillar and the toggle probability 0.25-0.5. Error probability is P = Q(m/sigma) + w exp(-m/eta + sigma^2/2eta^2) Phi(m/sigma - sigma/eta), replacing the RSS. For the pre-red-team 1-pillar FET, the 1e-4 between-sample quantile is 40 mV central and 65 mV pessimistic, confirming the reviewer's 13-70 mV and killing the 0.09-0.32 fF stretch. Two pillars halve the per-trap step: the 1e-4 quantile becomes 22.6 mV central and 36 mV pessimistic. Against the 47 mV margin at 0.5 fF, central P(err) is 8e-7. The required Cs spans 0.23-0.68 fF across m = 2-5 and f = 1-100%. Sort-time screening of ns-RTN gain FETs plus segment repair is extra margin and is not counted.

*Action taken:* Stretch claim (17-40x, 0.09-0.32 fF) withdrawn. Central sensing limit is 0.29 fF (18.8x); the 0.5 fF planning cell is kept. The GO line becomes a projected BER built from the measured RTN jump distribution of >=1e4 IGZO gain FETs at matched gate area, a 1-3 ns gap and 85 C on the BEOL carrier. Pass: 1e-4 quantile <= 44 mV at 0.5 fF (<= 82 mV for 1.0 fF). New kill criterion K9.

### RT-DEV-margin-stack-04 — MAJOR — DEV — §5 decisive experiment, steps 3, 5 and 7 (silicon sigma_res plus coupon oxide 1/f, combined by projection)

> The decisive number, the oxide post-CDS residual at a 0.7 ns sample gap, is never measured on an oxide device. The 22FDX MPW measures silicon FD-SOI gain FETs. The coupon 'discrete CDS on IGZO gain FETs' runs through ~1-10 pF of probe and board parasitics, which caps sampling bandwidth at tens of MHz. The GO/NO-GO therefore extrapolates IGZO noise from Hz-MHz PSDs to GHz and assumes Gaussian statistics, exactly where small oxide FETs are non-Gaussian. A pass could be an artefact of silicon's lower trap density.

*What would change the reviewer's mind:* An oxide-native ns-CDS measurement: IGZO gain FETs post-processed in the BEOL of the 22FDX die (or an on-coupon IGZO sample-and-hold), so an oxide FET drives an on-chip fF-scale node sampled at <=1 ns.

**Response — ACCEPTED-MITIGATED:** Valid: probe-coupled coupons cannot sample at ns, and silicon FD-SOI has the wrong trap physics. Added an oxide-native vehicle: a SKY130 readout carrier (two U.S.-fabbed runs, ~$30k, ~100 dies each) with an on-chip fF sample-and-hold under each top-metal landing site. IGZO gain FETs, and hybrid 2T leakage cells (IGZO write FET over a Si read FET), are post-processed on the dies at <=350 C in a university fab (Purdue Birck, Georgia Tech IEN or Stanford SNF). An oxide FET then drives an on-chip fF node sampled at 1-3 ns, which is the measurement the reviewer asked for. Cost +$90k, offset by halving the standalone coupon line to $60k. Risks: die-level process yield and passivation-via alignment. Mitigations: cheap dies, a second run at M9, and a fallback to coupon PSDs flagged as projection. The 22FDX emulator stays for density, coupling and comparator statistics.

*Action taken:* Plan step 5b added (SKY130 tape-out M4, post-processing M8-13, test M12-16) with a $90k budget line. The GO uses measured carrier RTN and residual, not Hz-MHz PSD extrapolation.

### RT-IND-margin-stack-01 — MAJOR — IND — §0 Verdicts, §2.6 Cost; models/margin-stack.py cap_module_share=0.15 ('concept says 10-20% [unsourced]')

> By the dossier's own model, $/bit moves +3.6% / +0.4% / -2.8% ($1.44-1.53/GB vs $1.48). Density is 0.701 Gb/mm2 against 0.762 for plain oxide 4F2 VCT (-8%). The capacitor module's share of wafer cost (0.10-0.20) is unsourced. A licensee therefore pays +8.8% die area and one strap mask to delete a capacitor module whose capex value is never stated in dollars. 'AR 62 to 5.7' is an engineering metric that no memory maker pays royalties for. The EV-75 rank-1 score rests on S=3 for a sub-metric (capacitor height), not on a mission axis that has a buyer.

*What would change the reviewer's mind:* A sourced capacitor-module cost (tool count, $/wafer, HAR-etch plus ALD tool-hours) from a teardown or cost house, showing the stub saves >=8-10% of wafer cost net of the +8.8% area. Or a memory maker stating it would pay for capacitor-module deletion on its 4F2 or 3D roadmap.

**Response — ACCEPTED-DOWNGRADE:** Valid. No sourced module cost exists (red-team search logged, none found). With PROC-01 and CIRC-02, $/bit is a +9% to +25% penalty and density -11% against plain oxide 4F2. MARGIN STACK is re-scoped to two claims. (a) Capacitor-module resource intensity: a 10.8x shorter capacitor (5.4x at the 1 fF fallback), ~100x less ZrO2/TiN ALD exposure, no AR-60 fluorocarbon etch, no Ru/k>50 push. That is a mission axis, but its scope is one module, and the fab-level share is unknown. (b) A 3D-tier enabler: lateral capacitor 450 -> 63-127 nm, per-tier density 2.2-2.8x, break-even ~10-13 tiers vs ~26. That is where a buyer would plausibly pay.

*Action taken:* $15k cost-split study. Before the raise, ask Nanya, Kioxia and Samsung contacts whether they would pay for capacitor-module deletion on 4F2 or 3D. Suggested EV re-score: S 3 -> 2 (EV 75 -> 24 with P4, D3).

### RT-IND-margin-stack-02 — MAJOR — IND — §3 Prior art and genuine delta; §6 IP and FTO

> Every claimable element maps to a reference the dossier itself lists: local 3T gain per ~32-cell segment: IBM Barth, ISSCC 2007; offset sampling and cancellation in a shipping DRAM sense amp: the OCSA family, US 11,763,878; ECC spent to relax margin or refresh: Hi-ECC (ISCA 2010) and Micron US 7,447,974; oxide 1T1C stacked over Si sense amps on short bitlines: SEL DOSRAM, US 12,230,314 / 11,694,594 / 11,488,528 (claims unread; the Cs values in SEL's DOSRAM papers are unchecked). IBM plus OCSA plus Hi-ECC is a ready obviousness combination against claim 1 (gain FET + CDS + Cs <= 0.5 Cseg). What remains, kick compensation and high-Vt biasing, are circuit details that incumbent sense-amp teams can design around. SEL is the likeliest blocker, not a licensee.

*What would change the reviewer's mind:* A professional patentability/FTO opinion on the three SEL families and the OCSA family showing claim 1 survives. Plus the Cs and bitline length from SEL's DOSRAM papers, showing no prior sub-1 fF short-segment design.

**Response — ACCEPTED-DOWNGRADE:** Valid, and sharpened by our own search. SEL DOSRAM patents (US 12,051,726 / US 12,230,314) stack the cell array over local SAs, with ~8-WL local arrays, and state that a shorter bit line 'allows the storage capacitance of the memory cell to be reduced'. So 'short bitline -> smaller Cs' is SEL prior art, and IBM micro-SA + OCSA + Hi-ECC is a ready obviousness combination against a broad claim 1. Remaining candidates: (i) a same-step in-array oxide gain FET whose Vt cancels by double sampling through that FET, including muxed signal-first DS; (ii) kick compensation for short segments; (iii) high-Vt same-step biasing by a pulsed read source; (iv) a lateral stub sized to a 3D sense tier. These are narrow and can be designed around. The ECC-budgeted retention quantile is Hi-ECC prior art and is not claimed.

*Action taken:* Patentability/FTO opinion on the SEL DOSRAM and OCSA families before the first provisional (IP line raised to $55k). Claims narrowed to (i)-(iv); section 3 delta revised. MARGIN STACK is funded as a portfolio instrument, not as a licensing company, until the opinion and a host say otherwise.

### RT-IND-margin-stack-03 — MAJOR — IND — §5 Decisive experiment; §4 #9 emulation gap; models/margin-stack.py avt_oxide_mVum=2.5 ('no IGZO AVT found')

> The M16-17 GO/NO-GO is a GF 22FDX silicon emulator plus planar IGZO coupons, combined 'by projection'. No oxide VCT array is ever built. The only parties with real oxide 4F2 arrays, Samsung (10a VCT) and Kioxia/Nanya (OCTRAM, 275 Mb), can rerun the 'shrink Cs, add local gain and CDS' experiment on silicon that matters within one design cycle of a pitch or paper. So the demo hands over the insight without handing over leverage. A $10-50M investor will diligence the projection step: Si 1/f and mismatch mapped onto an oxide AVT that is itself an estimate. They will discount the result.

*What would change the reviewer's mind:* A signed JDA or MTA giving access to partner oxide VCT or OCTRAM test arrays before tape-out, so the M16 number is measured on oxide. Or a pre-negotiated option or licence with Nanya or Kioxia that triggers on the §2.9 GO numbers.

**Response — ACCEPTED-DOWNGRADE:** Valid. Mitigation: the BEOL-IGZO-on-CMOS carrier puts the oxide device terms on measured oxide (RTN at ns on >=1e4 FETs; leakage to the 2e-5 quantile on >=1e6 cells, before and after stress). The projection then covers only geometry: alpha, the sidewall tail and the mask count. We will seek an MTA or JDA with Kioxia/Nanya or imec for test-array access but do not assume one. Incumbents could rerun the experiment after a paper, so provisionals go in before any disclosure. The investor discount stands.

*Action taken:* MTA outreach M0-6 (Nanya, Kioxia, imec). Provisional before any partner disclosure. GO report carries a measured-vs-projected column. Provability verdict lowered to 'partly'.

### RT-PROC-margin-stack-01 — MAJOR — PROC — §2.6-2.7 'Added masks +1 DUV; no EUV'; model INPUTS added_mask_frac=0.012, sites_strap=1, sites_extra_per_seg=3

> A 'same-step' VCT gain FET does not come with the terminals a segment amp needs. A 4F2 VCT device's natural nodes are the buried BL (bottom), the WL (gate, mid-pillar) and the top pad. The amp needs its GATE on the buried BL segment, its source on a separate read-source line and its drain on a new global line. Building that takes at least four levels: a WL-layer cut to make gate islands, the island-to-BL strap, a buried-BL cut every 32 cells with a separate buried read-source/write-back line, and a global-BL metal at the 2F~29 nm pitch, one line per column because the 3T amp has no column select. ArFi single exposure stops at ~76-80 nm pitch (the AND-STACK model's own note), so these are EUV or SAQP+cut layers. At the portfolio's $165 per EUV layer, three added layers cost ~$495, or ~13% of a $3,800 wafer. That turns the claimed -3% to +4% $/bit into roughly +10% to +17%, and voids 'no EUV added'.

*What would change the reviewer's mind:* A VCT-integrator process flow, or a process-emulation flow (e.g. Coventor), that builds the gain, reset and write-back FETs, the gate-to-BL strap and the global line with <=1 added critical layer, or with every added layer at >=80 nm pitch.

**Response — ACCEPTED-DOWNGRADE:** Valid. A same-step 3T segment amp needs four new things: a WL-island cut in the gain row, a gate-to-buried-BL strap, a buried-BL cut with separate read-source wiring, and a 2F-pitch global line. That is 2-4 EUV-class levels, not 1 DUV. At $165 per layer they cost 8.7 / 13.0 / 17.4% of a $3,800 wafer (model R9). With BCH parity and segment area the die is x1.125. $/bit is then a +9% to +25% penalty (central +17%) against plain oxide 4F2 at a 10-20% capacitor-module share; even a 30% share gives +2% to +12%. 'No EUV added' is withdrawn. Mitigations to test: (a) merge the BL and WL-island cuts into the existing SAQP cut masks (the 2-layer low case); (b) the I-12302 plate-strip variant. It keeps the buried BL continuous and clamped, senses a top plate strip (85 mV at 0.5 fF on a 2 fF strip vs 64 mV on the 64-cell segment), and builds the gain FET as a separate BEOL oxide FET with its own Vt. That removes the buried cut and the bias conflict but adds plate patterning, so it is probably still ~3 layers. (c) The 120 nm stub makes the array thinner, which shortens through-array contacts.

*Action taken:* The $/bit claim moves from -3..+4% to a +9..+25% penalty; MARGIN STACK is no longer scored on $/bit or fab $ per bit. added_crit_layers (2/3/4) and euv_usd_per_layer are in the model. A process-emulation flow (SEMulator3D-class, academic or partner) of the same-step and plate-strip variants runs in M0-5 inside the $55k simulation line. Gate: <=3 added critical layers, target <=2.

### RT-PROC-margin-stack-02 — MAJOR — PROC — §5 decisive experiment steps 1, 3, 6; key unknown alpha (data-dependent BL coupling); K4/K6

> The quantity that decides Cs is data-dependent BL-BL/WL coupling alpha in an oxide 4F2 array: buried bitlines at ~29 nm pitch under a wrap-around WL. The MPW is 22FDX with MOM stubs and planar wires at >=80-100 nm pitch, so its silicon measures the emulator layout's coupling, not a VCT array's. Per §2.8, alpha alone moves the required Cs from 0.26 to 0.44 fF at 13 mV (alpha 0.05 to 0.20). K4 and K6 will therefore rest on partner TCAD, a simulation of the one term the concept admits CDS cannot cancel. The terms the MPW measures well (comparator 1.9 mV, sampling kTC 0.3 mV) are not the ones in doubt.

*What would change the reviewer's mind:* Alpha measured on real VCT/IGZO array silicon under worst-case neighbour data (a Samsung, Kioxia/Nanya or imec 4F2 IGZO test vehicle). Alternatively, a 22FDX structure whose Cbl-bl/Cseg and Cwl-bl/Cseg ratios match extracted VCT values within 20%.

**Response — ACCEPTED-MITIGATED:** Valid: 22FDX metal at >=80 nm pitch cannot reproduce VCT buried-BL/WL coupling. Two mitigations. (1) alpha becomes an extraction problem. A 3D field solver runs on published 4F2 VCT geometry (Samsung ISSCC 2026 VCT, SK hynix VLSI 2026 shielded vertical gate), sweeping dimensions +-30%: static capacitance ratios of a stated geometry are reliable even when the geometry is uncertain. (2) The MPW gets ratio-matched, programmable coupling structures: explicit MOM caps between neighbour segment nodes and from a WL-emulation line. These set Cbl-bl/Cseg and Cwl-bl/Cseg to the extracted values within 20% and step alpha from 0.05 to 0.30, which is the reviewer's alternative criterion. The silicon then measures how double sampling, kick compensation and the muxed comparator respond to alpha. Model R4 margins: with central noise, 0.5 fF tolerates alpha <= 0.25 per side (1.0 fF: 0.34); with pessimistic noise only 0.02 (1.0 fF: 0.22). The real VCT alpha stays a projection until partner silicon exists.

*Action taken:* Programmable coupling block added to the MPW; field-solver extraction in M0-5. K6 restated: extracted alpha > 0.25 moves the planning cell to 1.0 fF; > 0.34 ends any cut beyond 5.4x. The GO is evaluated at the extracted alpha, with a sensitivity case at 1.5x it.

### RT-PROC-margin-stack-03 — MAJOR — PROC — §5 step 5 (IGZO coupons, >=1,000-cell droop arrays, lognormal fit to 1e-10); §2.9 GO #3; K2/K3

> G4, K2 and K3 hinge on the 1-in-1e10 IGZO leakage tail at 85 C (<=586 aA). A >=1,000-cell coupon observes only about the 1e-3 quantile, so reaching 1e-10 means extrapolating ~3.3 sigma along an assumed lognormal. DRAM retention tails are defect-driven (VRT, trap-assisted leakage, sidewall and contact damage) and not lognormal. The tail of a planar university-fab IGZO FET is also not the tail of a plasma-etched vertical IGZO sidewall in a VCT. The kill decision would rest on a number the experiment misses by about seven orders of magnitude in sample size.

*What would change the reviewer's mind:* Tail data at 85 C on >=1e7 oxide cells from a partner array (an OCTRAM-class 275 Mb device or a Samsung 4F2 IGZO test array). Alternatively, a mechanism-resolved tail model validated on >=1e6 vertical cells and predicting <=586 aA at 1e-10.

**Response — ACCEPTED-DOWNGRADE:** Valid: 1,000 cells see only ~1e-3, DRAM tails are defect-driven, and a planar university IGZO FET is not an etched VCT sidewall. Two changes. (1) The requirement moves from a 1e-10 tail to an ECC-budgeted 2e-5 leaky-cell fraction (see DEV-01), which >=1e6 cells observe directly (~20 tail cells), so no 3.3-sigma lognormal extrapolation is needed. (2) Those >=1e6 cells come from hybrid 2T leakage cells on the SKY130 carrier (>=2.5e5 per die over >=4 dies) plus coupons, with planar AND plasma-etched-sidewall IGZO splits to probe the sidewall-damage and hydrogen mechanisms. It is still not a VCT array: the VCT-specific tail remains a projection until partner data on >=1e7 cells.

*Action taken:* GO 3 rewritten to the measured aged 2e-5 quantile. The leakage carrier and sidewall split are budgeted. Partner-array tail data becomes the first milestone of the raise. K2/K3 move to 2028-04-30. Provability lowered (D 5 -> 3, with CIRC-03 and IND-03).

### RT-CIRC-margin-stack-06 — MINOR — CIRC — §2.3 / model i_gain_uA 5, gain_local 3, vov_gain_V 0.4

> The gain-FET drive is unsourced. 5 uA at 0.4 V overdrive (gm 25 uS, G=3 in 0.72 ns) is an estimate, while OCTRAM's '>15 uA' Ion is at full boosted overdrive (~2 V). Square-law scaling from that point gives ~0.6 uA and gm ~3 uS at 0.4 V, or G ~0.36 in 0.72 ns. Even linear scaling gives ~3 uA. Holding G=3 then takes ~1.2-6 ns per sample, which stretches the 3.6 ns read chain to ~6-14 ns. Holding the sample time instead raises the input-referred comparator term 2-8x.

*What would change the reviewer's mind:* Measured Id-Vg and gm of a same-step IGZO VCT pillar at 0.3-0.5 V overdrive with a pulsed negative read source.

**Response — ACCEPTED-MITIGATED:** Valid (same finding as DEV-02). The square law gives ~0.6 uA, gm ~3 uS and G ~0.36 at 0.4 V and 0.72 ns (model R2). Fix: 2 pillars, Vov 0.6 V via a deeper pulsed read source, 1.2 ns samples. That gives gm 9 uS and G 0.9 on 12 fF, a 4.3 mV comparator term, and decisions at 11.4 ns, so the read chain is ~14 ns with restore, not 3.6 ns. 0.5 fF still closes centrally.

*Action taken:* Same as DEV-02. The BEOL carrier measures Id-Vg and gm of matched-area IGZO FETs at 0.3-0.5 V overdrive with a pulsed negative source.

### RT-DEV-margin-stack-05 — MINOR — DEV — §2.9 GO 3 and §9 K2 (tail measured on fresh, as-built coupons)

> The tail spec is checked on fresh coupons, but IGZO access FETs drift negative over life from hydrogen redistribution and hold-bias stress. Every 30 mV of negative drift at 90 mV/dec multiplies the subthreshold tail by ~2.2x, so a 10-year, 85-105 C drift of 50-100 mV (common for unbarriered IGZO) multiplies it by 3.6-13x after qualification.

*What would change the reviewer's mind:* Tail leakage re-measured after a 1,000 h, 105 C hold-bias stress, with <=2x growth.

**Response — ACCEPTED-MITIGATED:** Valid. 75 mV of negative drift (central of 50-100 mV) multiplies the tail 6.8x at 90 mV/dec (model R5). Mitigations: a -0.1 V negative-WL reserve more than cancels it (aged 2e-5 tail 101 aA vs 191 aA fresh); hydrogen-barrier encapsulation splits on the coupons; and ECC corrected-error telemetry to shorten refresh adaptively over life. Measurement: a 1,000 h, 105 C hold-bias stress with tail re-measurement; <=2x growth passes.

*Action taken:* Stress line budgeted ($10k, M12-15). GO 3 is evaluated on post-stress data. vt_drift_mV and v_nwl_hold_V added to the model.

### RT-IND-margin-stack-04 — MINOR — IND — §7 After the demo; §8 U.S. build

> MARGIN STACK has no host until oxide-access 4F2 ships in volume. Samsung's VCT targets 2028 production (TrendForce 2026-04). Micron is reportedly skipping 4F2. OCTRAM has no product date. Add 2-3 years of qualification and first royalty-bearing wafers arrive ~2030+, a 6-8-year seed-to-revenue path for a technique with no $/bit lever. Its role as the portfolio's reader chip makes it a shared instrument, not a standalone company.

*What would change the reviewer's mind:* A named first host with a dated oxide-4F2 or 3D-tier product that has capacitor shrink on its roadmap (e.g., a Nanya differentiation program). Or evidence that the margin-test chip has paying users of its own.

**Response — ACCEPTED-MITIGATED:** Factually right on timing: Samsung VCT targets ~2028, so first royalties come ~2030+. But time to revenue is excluded as a kill criterion by the mission. Hosts, in order: Samsung and SK hynix 4F2 (2028+); Kioxia/Nanya OCTRAM; 3D-tier DRAM with PIXEL-STACK sense tiers; BEOL oxide eDRAM on logic through foundries. Until one commits, the margin-test chip and BEOL carrier serve the portfolio as its reader instruments (RAW-BER CONTRACT, PIXEL-STACK, DIODE-TOWER).

*Action taken:* Named-host search and a licensee question before the raise. MARGIN STACK is treated as the portfolio's reader instrument until a host commits. No change to the physics verdicts.

### RT-PROC-margin-stack-04 — MINOR — PROC — §2.6 cost; model INPUTS cap_module_share=0.15 [unsourced], cap_height_scaled_frac=0.65

> The concept's only economic win is the capacitor module, and both inputs that size it are unsourced estimates. A 120 nm stub still needs a bottom electrode, ZrO2/Al2O3 ALD, the top electrode and plate, and the contact, so only the height-scaled share shrinks. At a 10% module share the model already gives +3.6% $/bit; add objection 01's masks and MARGIN STACK costs more on every axis except capacitor capital and PFAS. That is a fair PFAS/capex claim, but the concept should not be scored on $/bit.

*What would change the reviewer's mind:* A teardown-based cost split (TechInsights or IC Knowledge) showing the 1-beta/1c capacitor module at >=15% of wafer cost with >=65% of it height-scaled, or a licensee's internal figure.

**Response — ACCEPTED-DOWNGRADE:** Valid. A red-team WebSearch for a teardown capacitor-module cost split (TechInsights / IC Knowledge) found none (logged in resp-margin-stack.jsonl), so cap_module_share and cap_height_scaled_frac remain unsourced. Model R9 shows $/bit loses at every plausible share: +9% to +25% at 10-20%, and +2% to +12% even at 30%. The fair claim is the reviewer's: capacitor capital and PFAS only.

*Action taken:* $/bit removed from the step-change claim. $15k budgeted for a teardown cost report or cost-model licence to size the module, its ALD/HAR-etch tool-hours and its PFAS share.

## pixel-stack — PIXEL-STACK: image-sensor-style group-sensed 3D 1T1C DRAM with an all-oxide source-follower + CDS amp tier every 16 cell tiers (pixel-stack)

**Final status after red team: DOWNGRADED.** No objection is fatal and the physics still closes, but the step change shrinks. Planning density falls from 6.2x to 4.6x 1-beta at 64 tiers (2.05 Gb/mm2). Three changes drive this: the design Cs moves 0.45->0.60 fF to absorb realistic RTN at a per-sense error budget; the capacitor EOT moves 0.50->0.60 nm; array efficiency moves 0.55->0.50. Bits/$ falls from 2.5x to ~parity at realistic deck prices and repaired tier yield. The planning refresh gain is ~15x (was 17x), and access energy is ~parity at ~50 fJ (was 2x worse). The edge over incumbent-style 3D at equal tiers is ~1.5x (1.1-2.1x), not 2.5x. The decisive experiment still fits $1M/24 months, with fixes for the RTN timescale, cumulative hydrogen dose and fab-grade calibration.

*Revised verdicts* — Possible: YES (revised after red team). At the 0.60 fF planning Cs (88 nm capacitor at EOT 0.6 nm) the read closes: modelled residual 15.8 mV vs 39.6 mV allowed. Random terms are held to 2e-7 per sense with a sense-count-triggered scrub, so the worst reviewer RTN corner (36.7 mV without screening or DFB) still passes. Retention plans at 0.52 s (sigma_Vt 35 mV, dVt 20 mV), range 0.05-2.4 s. No physics violated; the RTN tail, cumulative-H sigma broadening and lateral-cavity capacitor remain unmeasured. · Profitable: STEP CHANGE IF IT WORKS: density. ~4.6x 1-beta at 64 tiers (2.05 Gb/mm2), 5.2x if the 0.45 fF RTN gate passes. ~1.5x (1.1-2.1x) vs incumbent-style 3D at equal tiers, only above ~32-48 tiers. Secondary: refresh power ~15x lower (planning, low confidence). Bits/$ ~parity (0.6-1.25x); access energy ~parity (50 vs 46 fJ); tRC ~62 ns; zero EUV, <=400 C. · Doable by this founder: PROVABLE WITH $1M: partly. A ~$390k planar lot settles the decisive read and retention physics by M9: on-coupon 15 ns sample-and-hold for per-device time-domain RTN on 65k SFs, 1x/2x/4x cumulative H/thermal dose, a fab-grade reference split, and lateral-cavity capacitors. A 2-lot 4-tier stack with one amp tier by M21 needs partner labs. Tier yield, bits/$ and the 64-tier hydrogen accumulation cannot be proven at this budget.

### RT-CIRC-pixel-stack-01 — MAJOR — CIRC — §1 diagram 'CDS comparator in logic periphery' / model c_col_fF 15 ('shared by 16-32 SELs'), share 2, array_eff 0.55

> There are too many comparators for the base wafer. Each vertical bitline has 0.022 um2 of footprint (2 mirrored cells per tier), there is one SF per 2 bitlines, and the 15 fF column line serves 16-32 SELs. That makes one auto-zeroed CDS comparator per 0.7-1.4 um2 of array footprint per 16-tier group, or 2.8-5.6 um2 even if all 4 groups share one base comparator. That area must also hold the sampling cap, the restore driver and the base wafer's share of 64 tiers of wordline drivers. An auto-zeroed comparator with a sampling cap at 22-28 nm is ~5-10 um2. Going to 64-128 SELs per column instead raises c_col to ~40-70 fF. With gm 10 uS, SF settling (tau = C/gm) grows from 1.5 to 4-7 ns per sample, and tRC from 55 ns toward ~75-90 ns.

*What would change the reviewer's mind:* A base-wafer floorplan per mm2 that lists comparators, wordline drivers and restore drivers and fits array_eff 0.55, with tRC and the noise budget recomputed at the resulting c_col.

**Response — ACCEPTED-MITIGATED:** Valid for the original column plan. One auto-zeroed comparator per 32-SEL column per group cannot fit 0.7-1.4 um2 (2.8-5.6 um2 if 4 groups share). CIRC's alternative is worse when run in the model: 64 SELs directly on a 40 fF column give tRC 111 ns and 208 fJ/bit; 128 SELs on 70 fF give 166 ns and 347 fJ. Redesign: (1) Only one group is active per activation, so the 4 groups share one base comparator through an oxide group-select switch and a vertical column via. (2) A 2:1 base-wafer mux joins two 32-SEL local columns from different WL segments, which are never active together. Inactive SEL junctions stay isolated, so the column grows only 15->19 fF (+~2.5 fF mux wire, +~1.5 fF via/switch). At the revised cell (0.027 um2 per BL) that leaves 13.8 um2 of base wafer per comparator (72k/mm2 of array). Needed: ~3-4 um2 of FEOL [ESTIMATE]: inverter auto-zero comparator + latch 1.5-2.5, restore driver 0.3, DFB DAC 0.5, mux 0.2; the 10 fF CDS cap is MOM in upper metal above. At the 19 fF column: tRC 62 ns, 50 fJ/bit, residual 15.8 mV. This is a budget, not yet a drawn floorplan.

*Action taken:* c_col 15->19 fF in the model. New Q1 gate G0b: a drawn sky130/22FDX layout of comparator + restore + DFB DAC + mux in <=13.8 um2 at <=20 fF. If it fails, use a 4:1 mux (~24 fF, tRC ~70 ns) or the 32-tier-group variant.

### RT-CIRC-pixel-stack-02 — MAJOR — CIRC — §2.2 read noise / model rtn_mult 3.0 ('1e-4-tail RTN = 3 x q/CoxWL')

> The RTN tail input contradicts its own basis. The note says Si RTN amplitudes are exponential with a mean of 1-2 x q/(Cox*W*L). An exponential's 1e-4 quantile is ln(1e4) = 9.2x the mean, i.e. 9-18 x q/(Cox*W*L) = 13-25 mV, not 4.2 mV. Even discounting for trap occupancy and toggling probability (~7x the mean), it is ~10-20 mV. Substituted in, the readout residual moves from 14.7 mV to ~24-35 mV. That shifts the verdict from GO to CONDITIONAL or NO-GO at 0.45 fF and pushes Cs toward 0.6-0.75 fF: ~5-6x 1-beta rather than 6.2x.

*What would change the reviewer's mind:* The planar lot's RTN amplitude distribution on >=65k SFs at 85 C with a 15 ns gap, with a 1e-4 quantile <=6 mV at 0.01 um2.

**Response — ACCEPTED-DOWNGRADE:** Valid: the 3x input contradicts its own exponential basis. There are two corrections, one in each direction. (a) Adding a 1e-4 RTN quantile linearly to a 3.72 sigma Gaussian spends the 1e-4 budget twice. The joint quantile on the original 100x100 nm SF is 10.5-26.7 mV at 1e-4, across steps of 1-3x q/CoxWL and 1-30% of SFs with a fast trap; CIRC's linear add gives 23-36 mV. (b) Owner-found, and worse: CDS decisions are restored raw, so random per-sense errors accumulate between ECC corrections. Random terms must therefore be held to ~2e-7 per sense, with a sense-count-triggered row scrub every <=128 senses. At 2e-7 the original SF gives 15.6-52.7 mV. Redesign: SF 200x100 nm halves the step and still fits the two amp sub-layers (0.0432 um2 needed vs >=0.044 available); Vov 0.25 V; a BIST screen remaps SFs with fast-trap steps >8 mV (0.03-0.65% of SFs). Revised residual: 15.8 mV modelled. Worst corner (3x, 30%, no screen): 28.0 mV with DFB and 36.7 mV without, vs 39.6 allowed at 0.60 fF and 29.0 at 0.45 fF. Planning Cs moves 0.45->0.60 fF (88 nm capacitor at EOT 0.6), taking density from 5.2x to 4.6x 1-beta at the revised geometry (-12%). 0.45 fF returns only if the measured time-domain RTN passes.

*Action taken:* Model: RTN as exponential steps convolved with the Gaussian terms at p_sense 2e-7; SF 200x100; scrub every 128 senses; cs_design 0.60 fF. Experiment: on-coupon oxide dual S/H with a 15 ns gap, 65k SFs x >=1e4 reads at 85 C. CIRC threshold adopted as a sub-gate: 1e-4 step quantile <=6 mV at 0.01 um2 (<=4 mV at 0.02 um2); <=1% of SFs above 8 mV.

### RT-DEV-pixel-stack-01 — MAJOR — DEV — §2.2 'RTN 1e-4 tail (3 x q/Cox·W·L) 4.2 mV'; model RTN constant

> The RTN tail is set at 3x the single-trap mean step (1.39 mV for a 100 x 100 nm SF at EOT 3 nm). Trap amplitudes in small devices are exponentially distributed and enhanced 2-3x by percolation in amorphous channels (eta ~2.8-4.2 mV). If 1-30% of the ~5e8 SFs per die carry a trap whose time constant lies within 10x of the 15 ns CDS gap, the per-read 1e-4 quantile is eta*ln(50-1,500) = 4-7 eta, i.e. ~11-31 mV, not 4.2. That moves the 14.7 mV residual to ~21-42 mV, from GO into the 15-30 mV CONDITIONAL band or past the 30 mV NO-GO line. In a 0.01 um^2 device, Hooge 1/f and RTN also double-count, since the 1/f there is the sum of a few Lorentzians.

*What would change the reviewer's mind:* Time-domain RTN on >=1e4 SFs of <=0.01 um^2 at 85 C, giving a 1e-4 quantile of jumps within a 15 ns gap <=10 mV. The planar run can deliver this if analysed per device rather than by PSD.

**Response — ACCEPTED-DOWNGRADE:** Accepted; same redesign as RT-CIRC-pixel-stack-02. The percolation-enhanced step (2-3x q/CoxWL) and a 1-30% fraction of SFs with a trap near the 15 ns gap are now explicit model inputs (planning 2x, 10%, toggle probability 0.25). Convolving the RTN steps with the Gaussian terms is gentler than adding eta*ln(f/1e-4) linearly: on the original 100x100 nm SF, DEV's 21-41 mV becomes 11-27 mV at 1e-4. But an owner-found constraint makes it harsher. Each CDS decision is written back raw, so random per-sense errors accumulate between ECC corrections, and the random terms must be budgeted at ~2e-7 per sense. At 2e-7 the original SF gives 26.7-52.7 mV at 2-3x steps: NO-GO at the pessimistic corner. Revised design: the SF goes to 200x100 nm, which still fits the two amp sub-layers; Vov 0.25 V; a BIST screen remaps SFs with fast-trap steps above 8 mV. The modelled residual is then 15.8 mV, and 23.2/28.0 mV at the 3x/30% corner (screened with 10% escape / unscreened), inside the 39.6 mV allowed at the 0.60 fF planning Cs. The double-counting point is conceded but not taken as credit: both 1/f and RTN stay in the model (conservative), and the measurement will separate them. DEV's test (per-device time-domain RTN, >=1e4 SFs, 15 ns gap) is adopted verbatim. An on-coupon sample-and-hold lets slow external readout see the 15 ns gap.

*Action taken:* Model: explicit RTN step model at 2e-7 per sense, SF 200x100 nm, design Cs 0.45->0.60 fF. DEV threshold becomes an M9 sub-gate: 1e-4 per-read quantile of 15 ns-gap jumps <=10 mV at <=0.02 um2. Joint-residual gates: GO <=20 mV, PLAN <=40 mV, NO-GO >55 mV.

### RT-DEV-pixel-stack-02 — MAJOR — DEV — §2.3 retention (Ioff median 1 aA, sigma_Vt 30 mV, SS 80 mV/dec); §2.5 retention table

> Retention closes (31 vs 34 aA) only at the optimistic end of every input. The dossier's own text gives 30-100 mV oxide offsets; at sigma_Vt 50 mV its table gives 0.15 s, and with a 50 mV hydrogen shift 0.04 s, about the same as DDR5's 32 ms hot interval. The 1 aA median is imported from a vertical OCTRAM device, whose test temperature and statistic are unpublished (rt-DEV.jsonl), into a lateral TFT deposited in a <=400 C multi-tier stack. 80 mV/dec at 85 C is near-ideal (ideal is 71). The 17x refresh-power claim is therefore unsupported.

*What would change the reviewer's mind:* Measured on the planar lot after the H/400 C splits: sigma_Vt <=30 mV, SS <=85 mV/dec at 85 C, and a 1e-4-quantile node leakage <=34 aA on >=1e4 nodes.

**Response — ACCEPTED-DOWNGRADE:** Valid. The 1 aA median comes from a vertical OCTRAM device whose test temperature is not stated, and sigma_Vt 30 mV is the optimistic end. Planning inputs are now sigma_Vt 35 mV and dVt 20 mV, giving 0.52 s at the 0.60 fF planning Cs (0.41 s at 0.45 fF). Across sigma_Vt 20-50 mV and dVt 0-50 mV the range is 0.05-2.4 s (model sec.10). SS stays at 80 mV/dec: in this model SS acts only through the median, which the planar lot measures directly. The refresh claim is therefore unproven rather than unsupported: ~15x lower refresh power at planning inputs, only ~1.4x at sigma 50/dVt 50 mV. Levers if the tail is worse: (1) per-group WL hold trim, worth 0.52->0.85 s; (2) a larger Cs; (3) the I-12627 series access pair. If the two devices are independent, a 1e-4 pair tail needs each at 1e-2: 29 aA and 1.55 s (2.7 s with a ~3x stack effect, 0.93 s if fully correlated), at -19% density per tier.

*Action taken:* vt_sigma_mV 30->35 and h_vt_shift 0->20 in the model. Planar lot measures sigma_Vt, SS at 85 C and 1e-4-quantile node leakage on >=1e4 nodes after the cumulative dose (DEV's thresholds, rescaled to 45 aA at 0.60 fF). Adds an I-12627 series-gate split to test tail correlation.

### RT-DEV-pixel-stack-03 — MAJOR — DEV — §4 #4 hydrogen/thermal accumulation; GO 'bottom-tier delta-Vt <20 mV after the amp tier'

> Group-1 cells absorb the thermal and hydrogen budget of 48 further cell tiers and 6-8 amp sub-layers, each with ALD channels and capacitor dielectrics from H-bearing precursors and 250-400 C steps: plausibly tens of hours at 300-400 C. The planar run tests one 400 C/H2 sequence and the 4-tier milestone tests one amp tier; neither bounds the 64-tier accumulation, where unbarriered IGZO commonly shifts by hundreds of mV. Retention falls ~2x per 20 mV of negative shift at sigma 30 mV (§2.5 table), so the bottom group sets the whole die's refresh.

*What would change the reviewer's mind:* A cumulative-dose anneal equal to the 64-tier budget on planar coupons with Al2O3/SiNx barriers, giving delta-Vt <=20 mV and an unchanged Ioff tail.

**Response — ACCEPTED-MITIGATED:** Valid: one 400 C/H2 step does not bound group 1's dose. Plan changes: (1) Planar coupons get 1x, 2x and 4x cumulative group sequences, each being cell-module ALD and anneals plus two amp sub-layers' depositions and 400 C anneals. The 64-tier dVt is then read from a measured dose-response, not one point. (2) ALD Al2O3 barriers go above and below every amp tier, plus liners on the BL vias. The amp tier itself tolerates hydrogen: CDS cancels SF Vt shifts up to 100 mV, and RST/SEL/TG only switch. So the issue is containment, not materials. (3) Each group has its own WL drivers, so the bottom group's hold voltage can be trimmed to cancel the uniform shift: 0.52->0.85 s at 0.60 fF. Only the sigma broadening cannot be corrected. (4) A Purdue-style In2O3 channel split (survives 600 C). Planning retention already assumes dVt 20 mV and sigma_Vt 35 mV.

*Action taken:* Add 1x/2x/4x cumulative-dose splits with SIMS (H line $25k->$40k). GO at 4x: uniform dVt <=50 mV and trimmable, sigma_Vt <=35 mV, Ioff tail unchanged. Kill #6 revised.

### RT-IND-pixel-stack-01 — MAJOR — IND — §2.4 Wafer cost/yield/$/GB; models/pixel-stack.py tier_yield=0.998, amp_tier_yield=0.995

> The 0.40x $/bit ($0.58/GB) takes tier_yield = 0.998 as an input, and 0.998 is A1's requirement, not a measurement. The only public data point, SK hynix's 5-tier array at 56.1%, implies ~0.89 per tier raw. At 0.99 per tier, 64-tier stack yield falls from 0.862 to ~0.52 and $/bit rises ~1.7x, to ~0.67x. At 0.98 per tier, yield is ~0.27 and $/bit is ~1.3x, worse than 1-beta. The bits/$ claim, which the dossier already rates low confidence, is the yield assumption restated.

*What would change the reviewer's mind:* A repaired-tier-yield model built from measured per-tier defect densities on a multi-tier oxide stack (Kioxia 3D OCTRAM data or a partner short loop), showing >=0.995 per tier after 16-tier group repair.

**Response — ACCEPTED-DOWNGRADE:** Valid: 0.998 is A1's requirement, not a measurement. The model now uses a raw per-tier killer-defect probability d with mat-level spare-tier repair: 1 spare per 16 tiers per mat, 64 mats, 50% of defects crossing tiers, 80% of those column-repairable. Unrepaired, IND's arithmetic holds: d 0.01 gives yield 0.52 and 0.66x $/bit at the original prices. Repaired, at the revised $13,500 wafer, d 0.002/0.01/0.03/0.11 gives yields 0.97/0.92/0.81/0.47 and $/bit 0.80/0.84/0.96/1.64x. Planning d is 0.03 (3.7x better than SK hynix's 5-tier R&D 0.11), giving 0.807 and 0.96x. Bits/$ is therefore ~parity: 1.04x at planning, ~1.2x at d <=0.01, 0.6x at SK hynix-level defectivity. It also rests on defects being random and tier-local, which nobody has measured on a multi-tier oxide stack. The $1M plan cannot measure it.

*Action taken:* Repaired-yield model and spare-tier cost in the model. Bits/$ dropped from the step-change claim ('parity, low confidence'). The 4-tier lots report per-tier defect counts, and the raise milestone asks a partner (Kioxia OCTRAM) for short-loop per-tier defect densities.

### RT-IND-pixel-stack-02 — MAJOR — IND — §3 Honest caveats ('Against A1's optimistic 3D case there is no density gain'); §2.5 Cost (Smart-Cut comparison)

> The headline advance is removing a bonded or Smart-Cut c-Si sense layer from every 16-tier group. Incumbents are not planning in-stack Smart-Cut sense layers. Samsung's VS-DRAM uses peri-on-cell bonding with a long vertical bitline, and the mainstream 3D route is a Si/SiGe epitaxial superlattice (imec, 120 bilayers) with sense amps on a bonded base wafer. Against A1's optimistic 3D case (6.7x at 64 tiers), the dossier itself finds no density gain. The licensable delta is therefore 'reach that density at a 70 nm pitch with a 52 nm capacitor'. It is worth what capacitor length costs an incumbent, not ~2.5x.

*What would change the reviewer's mind:* A comparison against incumbent roadmaps (VS-DRAM, SK hynix 3D, Kioxia OCTRAM), using their planned per-tier cell area and capacitor length, that shows PIXEL-STACK >=2x better at equal tier count.

**Response — ACCEPTED-DOWNGRADE:** Valid. Removing a Smart-Cut layer beats a design no incumbent plans, and at PROC's deck prices the cost edge over Smart-Cut is 1.24x, not 1.7x. The right comparison is incumbent-style 3D at equal tier count. Incumbent per-tier cell areas are not public: searches found none, and one academic horizontal cell is 0.122 um2. Modelled with the same pitch, TFT and EOT: (1) A 64-tier long vertical BL read by an ideal bonded OCSA needs 0.71-0.98 fF (0.0147-0.0177 um2), so PIXEL-STACK's edge at 0.60 fF is 1.09-1.31x. (2) A switched hierarchical BL without gain (+10-20 fF global) needs 1.3-1.9 fF, an edge of 1.56-2.08x. (3) Against A1 optimistic (40 nm pitch, 300 nm capacitor) it is 0.89x; against A1 base, 2.22x. An ideal OCSA per vertical BL needs ~0.3-1 um2 of base wafer per 0.027 um2 BL footprint, so the realistic no-gain incumbent is the switched case. At 16 tiers (VS-DRAM) the ideal-OCSA cell beats PIXEL-STACK (0.72x), so the concept pays only above ~32-48 tiers. Licensable delta: ~1.5x density (1.1-2.1x) at >=64 tiers, with an 88 nm capacitor vs ~200-300 nm.

*Action taken:* Drop 'removes Smart-Cut' as the headline. Restate the claim against incumbent-style 3D at equal tiers (~1.5x, 1.1-2.1x, >=64 tiers). Equal-tier table added to model sec.10.

### RT-IND-pixel-stack-03 — MAJOR — IND — §3 Prior art; §6 FTO risks

> Every element sits in someone else's estate: hierarchical 3D bitlines with local/global switches: US 12,207,458, US 12,603,114, EP 4567797-799, and US 12,010,831 (probably Micron); oxide RST/SF/SEL readout with CDS: US 11,477,398 and De Roose (IISW 2015); oxide pixels on an H-barrier: US 12,615,863; oxide memory over sense amps: SEL DOSRAM, US 10,622,059. The dossier concedes that an examiner can combine the hierarchical-bitline and oxide-APS families against the system claim. In the U.S. home, Micron's vertical-digit-line patents force a cross-licence. What is defensible (pillar-gated SF, decision-feedback CDS, per-group H barrier) is narrow.

*What would change the reviewer's mind:* An FTO opinion clearing claim 1 against the hierarchical-3D-bitline and oxide-APS families, or a cross-licence term sheet with Micron or Kioxia.

**Response — ACCEPTED-MITIGATED:** Valid as an IP/business risk. It does not touch the physics, and the mission does not kill for business reasons. The broad system claim is likely obvious over hierarchical 3D bitlines plus oxide-APS CDS, so the plan files narrower implementation claims, several of them new in this response: (1) a per-sense error budget with sense-count-triggered row scrub for CDS-read DRAM; (2) a BIST RTN screen and remap for in-stack followers; (3) a two-pass neighbour-decision CDS compare; (4) a group-shared base comparator via group-select plus a 2:1 segment mux; (5) a per-group WL hold trim set by the in-stack SF leakage meter; (6) a per-group Al2O3 H barrier with an H-tolerant amp tier; (7) the pillar-gated SF [SPECULATIVE]; (8) as dependents, the series-gate access option (I-12627) and an SF on a plate strip (I-12302). An FTO opinion on claim 1 against the hierarchical-3D-bitline and oxide-APS families comes before the raise. The scale path assumes a cross-licence with Micron or Kioxia.

*Action taken:* IP line $45k->$55k, including an FTO opinion by M18. Replace the sec.6 claims list. Describe the licensing value as narrow implementation claims plus know-how.

### RT-PROC-pixel-stack-01 — MAJOR — PROC — §2.5 cost; model INPUTS usd_per_deck=250, usd_per_amp_sublayer=300

> An amp tier every 16 tiers turns the stack into four sequential modules. Each needs its own BL-hole HAR etch, cell-isolation trench, lateral channel and capacitor recesses, ALD fills, WL staircase and CMP, then two amp sub-layers of ~4 DUV masks each, then realignment for the next group. $250 per deck for all of that is implausible by NAND standards (a staircase alone is several litho/trim cycles), and $300 per sub-layer prices four critical levels at ~$60 each. At $1,000/deck and $600/sub-layer the wafer is ~$13,400 and $/bit ~0.67x 1-beta. That equals the Smart-Cut c-Si case (0.67x) the oxide amp tier was supposed to beat.

*What would change the reviewer's mind:* A bottom-up step list (steps, tool-hours) for one 16-tier group plus its amp tier, from a 3D-DRAM or NAND integrator, pricing it at <=$650 per group-plus-amp.

**Response — ACCEPTED-DOWNGRADE:** Valid; PROC's numbers are adopted. Rough bottom-up per 16-tier group: BL-hole and slit litho/HAR etch ~$160, recess ~$30, capacitor ALD ~$100, channel ~$80, WL replacement ~$60, 16-tier staircase ~$400, CMP/clean/metrology ~$170, total ~$1,000. Per amp sub-layer: 4 DUV levels x ~$100 + channel/gate/anneal ~$100 + vias ~$100 = ~$600 [ESTIMATE, not an integrator's step list]. The wafer goes from $8,000 to $13,400 (PROC's 0.66x), and to $13,500 with spare tiers. With the revised 0.60 fF cell and the repaired-yield planning case, $/bit is 0.96x 1-beta. Re-priced at the same deck cost, Smart-Cut is $16,700 and 1.19x, so the oxide amp tier keeps a 1.24x edge, not 1.7x. If the measured residual comes in near the modelled 16 mV, 32-tier groups halve the amp-tier count and reach 0.56x $/bit.

*Action taken:* usd_per_deck 250->1000 and usd_per_amp_sublayer 300->600 in the model. Bits/$ dropped from the step-change claim. Get an integrator step list (Kioxia/TEL/Lam contact) before the raise.

### RT-PROC-pixel-stack-02 — MAJOR — PROC — §2.5 'SF must keep >=~0.01 um2 of gate area and a SiNx-capped gate'; §2.3 retention; §4 #4

> The noise fix and the retention fix pull in opposite directions. The SF 1/f budget relies on a SiNx-capped gate, since Al2O3-only gates are 100-1000x noisier (Cho, EDL 2009). But PECVD SiNx is the classic hydrogen source that dopes IGZO, and at sigma_Vt 30 mV retention tolerates only ~3 mV of H-induced dVt (31.3 vs 33.8 aA). Each of the 4 groups adds an amp tier with that SiNx plus another cell module's ALD and anneals. Group 1 therefore takes ~4x the H/thermal dose of the single 400 C/H2 planar test.

*What would change the reviewer's mind:* Planar coupons that combine the low-noise SF gate stack with access cells and survive a 4x cumulative group thermal/H sequence with tail leakage <=34 aA and dVt <20 mV. Alternatively, a low-H gate stack (e.g. ALD SiN) meeting alpha_H <=1e-2 at 0.01 um2.

**Response — ACCEPTED-MITIGATED:** Valid as a test gap, and partly answerable by design. (1) Low 1/f does not need PECVD SiNx. Fung's alpha 1.5e-3 device used a SiO2 gate. Cho's SiNx gain came from an interlayer that suppresses Al2O3 remote-phonon scattering. So the split is a low-H PEALD SiO2 or ALD SiN interlayer under HfO2/Al2O3; KAIST shows gate-insulator H content itself changes IGZO LFN. (2) The H-bearing film sits in the amp tier, whose devices tolerate Vt shift (CDS cancels SF offset within 100 mV; RST/SEL/TG only switch). The conflict is therefore H containment: ALD Al2O3 barriers above and below each amp tier, plus BL-via liners. (3) Coupons now put the low-noise SF gate stack and access cells on one die, run 1x/2x/4x cumulative group sequences, and measure alpha_H, tail leakage and dVt together.

*Action taken:* Planar splits: PEALD SiO2/HfO2 vs ALD SiN/HfO2 vs PECVD SiNx/Al2O3 SF gates, each beside access cells, each at 1x/2x/4x dose. Gate: alpha_H <=1e-2 at <=0.02 um2, with tail <=45 aA and dVt <20 mV after 4x.

### RT-CIRC-pixel-stack-03 — MINOR — CIRC — §2.4 timing/energy (89 fJ, tRC 55 ns) / §4 #5 amp-tier area

> Density, mask count and tRC cannot all hold at once. At share 2 the amp tier needs two sub-layers per 16-tier group (~8 extra masks per group, 32 per 64 tiers). Share 4 or 8 removes a sub-layer but gives a tRC of 106 or 210 ns, outside DRAM class. The SF static bias (2 uA x 1.2 V x 16 ns) makes reads 89 fJ/bit, 2x DDR5, and ~4 mA of static current per activated 4096-bitline row. The step-change claim should state which corner it is.

*What would change the reviewer's mind:* A single design point that meets tRC <=60 ns, energy <=46 fJ/bit and <=1 amp sub-layer per group, or a statement of which axis is conceded.

**Response — ACCEPTED-DOWNGRADE:** Valid; one corner is now stated. Share 2, two amp sub-layers per group: this concedes ~8 DUV masks per group, 32 per 64-tier stack, still with zero EUV, priced at $600 each. tRC 62 ns, including a 5 ns DFB pass (52 ns without). Energy 50 fJ/bit instead of 89. Energy fell because SF settling energy scales as settle_tau x C_col x Vov x V_amp. The changes: V_amp 1.2->0.8 V; Vov 0.4->0.25 V; settling 4.6->4 tau; Id 1.5 uA (gm 12 uS at W/L 2). Share 1 gives tRC 33 ns at 3 sub-layers (+$2,400/wafer). Share 4 or 8 is outside DRAM class (122-240 ns). Conceded: the mask count, and a tRC ~1.35x DDR5. Energy reaches ~1.1x DDR5, not <=46 fJ.

*Action taken:* Revise v_amp, sf_vov, sf_id, settle_tau and t_dfb in the model. Restate the claim as density-only, with tRC ~62 ns, ~50 fJ/bit and +32 DUV masks. SF drift headroom 150->100 mV (kill #7 revised).

### RT-CIRC-pixel-stack-04 — MINOR — CIRC — §2.2 coupling 'after decision feedback 1.2 mV' / model dfb_residual 0.15

> Decision feedback is not free in a page that is sensed all at once. It needs the neighbours' decisions before the victim's, but every bitline on the open wordline is sensed simultaneously. That takes a two-pass compare with a per-comparator threshold DAC, ~+5 ns and extra area, none of it modelled. Without decision feedback the residual is 21.5 mV, and it fails at Cc/C_BL 0.2 (33.6 mV).

*What would change the reviewer's mind:* A comparator design with two-pass decision feedback and its area and time added to §2.4.

**Response — ACCEPTED-MITIGATED:** Valid. A two-pass compare is now in the model. Pass 1 decides every bit on the row. Pass 2 re-fires each latch with its threshold shifted by its two neighbours' pass-1 decisions, through a 2-level charge-injection DAC (~0.5 um2 per comparator, ~1 fJ/bit) [ESTIMATE]. This adds 5 ns per sensed bitline, so tRC goes 52->62 ns. A pass-1 error (<=~1e-3) mis-corrects only one neighbour's ~1.5 mV share. The planning Cs of 0.60 fF passes without DFB even at the worst RTN corner (36.7 vs 39.6 mV), so DFB is margin, not a load-bearing assumption. Without DFB the modelled residual is 24.5 mV.

*Action taken:* Add t_dfb_ns 5 and e_cmp 1 fJ to the model. Include the DAC in the G0b layout. Planar coupons measure coupling raw and after software two-pass DFB. Kill #3 unchanged (>15 mV after DFB).

### RT-CIRC-pixel-stack-05 — MINOR — CIRC — §2.3 retention / model h_vt_shift_mV 0.0

> The planning retention (1.08 s) assumes zero hydrogen-induced Vt shift after the full <=400 C stack, while the gate only requires <20 mV. At 20 mV the model gives 0.67 s, so the '~17x lower refresh' headline rests on an input set to the best case.

*What would change the reviewer's mind:* Planning retention computed at the gate value (20 mV), or measured delta Vt <=3 mV after 400 C/H2 in the planar lot.

**Response — ACCEPTED-DOWNGRADE:** Valid. Planning retention now uses the gate value, dVt 20 mV, together with sigma_Vt 35 mV from RT-DEV-pixel-stack-02. That gives 0.52 s at 0.60 fF (0.82 s at sigma 30 mV), not 1.08 s. The refresh-power claim falls only from 17x to 15x, because access energy also fell (89->50 fJ). Refresh busy time is 2.96% including scrub, vs DDR5's 7.6%. A per-group WL hold trim, set from the in-stack SF leakage meter, could cancel the uniform part of the shift (0.85 s); this is not credited in planning.

*Action taken:* h_vt_shift 0->20 mV in the model. Restate the refresh claim as ~15x lower at planning inputs, range ~1.4-70x over sigma_Vt 20-50 mV and dVt 0-50 mV.

### RT-DEV-pixel-stack-04 — MINOR — DEV — §5 step 5 ('pixel amp as the meter: 1 mV in 1,000 s on 3 fF = 3e-21 A')

> Over 1,000 s the SF itself drifts by more than 1 mV: from 1/f noise integrated down to 1 mHz, from PBTI under continuous bias, and from a Vt temperature coefficient of order -1 to -3 mV/K (0.5 K of chuck drift is ~1 mV). The RST device's own aA-level leakage adds to the signal. Sub-zA metrology needs a reference node and chopped readout.

*What would change the reviewer's mind:* A differential meter with a matched dummy node showing a baseline drift <0.3 mV per 1,000 s at 85 C.

**Response — ACCEPTED-MITIGATED:** Valid for the zeptoamp claim, which is withdrawn. The GO metric never needed it. The retention gate is a 1e-4-tail leakage of 45-90 aA, which droops a 0.6 fF node by 75 mV in 0.5-1 s. Leakage is now mapped by write-wait-read: each point is a fresh CDS read after a wait of 10 ms-100 s, so SF 1/f, PBTI and tempco cancel in every sample. A 1 aA cell droops 0.17 V in 100 s, ~25 mV at the node. Median sub-aA leakage, if wanted, uses a differential meter against a matched dummy node (no cell) with power-gated, chopped sampling. DEV's <0.3 mV per 1,000 s baseline criterion applies.

*Action taken:* Rewrite sec.5 step 5 as write-wait-CDS-read retention maps. Remove the 3e-21 A claim; the dummy-node differential meter is secondary only.

### RT-IND-pixel-stack-04 — MINOR — IND — §2.4 Energy per accessed bit (89 fJ vs ~46 fJ); tRC 55 ns

> Energy per accessed bit is 89 fJ against ~46 fJ (~2x worse), driven by a 2 uA x 16 ns source-follower bias per read, and tRC is 55 ns against ~46 ns. The demand pull for new DRAM is AI memory, where pJ/bit and bandwidth decide purchases (HBM). A density-only cell that is 2x worse on access energy meets resistance in exactly the segment with pricing power.

*What would change the reviewer's mind:* A design point (pulsed SF bias or wider SF sharing) at <=46 fJ/bit that keeps the 14.7 mV residual.

**Response — ACCEPTED-MITIGATED:** Mitigated to near parity with a pulsed, low-voltage SF: V_amp 0.8 V, Vov 0.25 V (gm/Id 8/V), Id 1.5 uA, 4 tau settling on a 19 fF column. SF bias energy falls 38->17.6 fJ core, and the total 89->50 fJ/bit (DDR5 46 fJ). The residual holds at 15.8 mV, because the 1/f term falls with Vov (1.34->0.74 mV). Wider SF sharing does not save energy, since settling energy is per sample, and it costs tRC (share 4: 122 ns). Energy is not claimed as an advantage: AI buyers get density and ~15x lower refresh power at ~1.1x access energy. If 46 fJ is a hard requirement, settling to 3 tau gives ~42 fJ for ~+1% gain spread [ESTIMATE].

*Action taken:* Revised inputs in the model. Planar lot measures oxide SF gm/Id at Vov 0.25 V and 85 C (>=8/V needed).

### RT-IND-pixel-stack-05 — MINOR — IND — §5 Decisive experiment (planar SF lots at Purdue/GT); §2.5 Hooge-alpha table

> GO hinges on the Hooge alpha, which spans 1e-3 to 1e-1 with gate stack and process (Fung 2010; Cho 2009). A university ALD IGZO SF could land at 1e-2 to 1e-1 (20-47 mV residual at 100 x 100 nm) for reasons unrelated to Kioxia's or Samsung's fab-grade IGZO, giving a false NO-GO. Or it could land at 1e-3 and fail to transfer, giving a false GO. Neither result binds a memory maker.

*What would change the reviewer's mind:* Coupons run on a partner's fab-grade IGZO (Kioxia, a display-maker line or Albany) alongside the university splits.

**Response — ACCEPTED-MITIGATED:** Valid. Three mitigations. (1) Every coupon carries large-area (1-10 um2) SFs, whose alpha_H is compared with published fab-grade values: 1.5e-3 SiO2-gated, 6e-3 Al2O3/SiNx. If the university alpha exceeds 6e-3, a scaled-device failure is logged as 'process-limited', not NO-GO. (2) A $50k fab-grade split runs the SF/RTN ladder on a partner IGZO line (Kioxia/Nanya, a display-maker R&D line or Albany), negotiated in Q1. GO counts only if the fab-grade split agrees within 2x on residual. (3) An In-ratio split, because scaled ALD IGZO noise rises with In content (Purdue TED 2025); this is a caution for the In-rich depletion SF.

*Action taken:* New budget line 'fab-grade reference coupons' $50k, funded by cutting the 4-tier stack from 3 lots to 2. Calibration rule written into the M9 gate.

### RT-PROC-pixel-stack-03 — MINOR — PROC — §2.1 cell footprint (20 BL + 70 TFT + 52 cap + 15 plate nm); model INPUT array_eff=0.55

> The footprint leaves no room to bring each amp tier's column output, RST supply and SEL/RST/TG controls down to the base-wafer CDS columns through 1-3 lower groups. Either a vertical column via per SF passes through every lower cell tier (~+6-10% cell area), or each group needs an edge via farm and its own control staircase (~+3-8% die area). Neither appears in the 0.55 efficiency or in the 15 ns CDS timing, and column capacitance grows with length.

*What would change the reviewer's mind:* A floorplan of a 4-group mat showing column and control routing with array efficiency >=0.5 and column capacitance <=15 fF.

**Response — ACCEPTED-DOWNGRADE:** Valid. Each group's column output, RST supply and SEL/RST/TG controls reach the base through an edge via farm plus a per-group control staircase (~5% die area). Vias through the lower cell tiers would instead cost 6-10% cell area. Spare SF columns for the RTN screen add ~3%. array_eff therefore goes 0.55->0.50 (-9% density). The vertical via and group-select switch add ~1.5 fF to the column (now 19 fF, including the 2:1 mux). That is already in the 62 ns tRC and the 15.8 mV residual.

*Action taken:* array_eff 0.50 in the model. A 4-group mat floorplan with column/control routing joins the Q1 layout gate G0b (array eff >=0.50, column <=20 fF).

### RT-PROC-pixel-stack-04 — MINOR — PROC — §2.1 capacitor 69.1 fF/um2 at EOT 0.50 nm; §4 #6; kill #4

> Production ZrO2/Al2O3/ZrO2 reaches 0.5 nm EOT through tetragonal crystallisation with TiN electrodes on vertical pillars. In a ~60 nm lateral cavity the TiN/ZrO2/TiN shell takes >=27-32 nm of tier height, the recess must be filled by ALD from a 24:1 hole into a 52 nm-deep, ~30 nm-tall slot, and the cell then sees up to three more group thermal cycles that raise leakage. The 8% retention margin cannot absorb EOT 0.7 nm (a 75 nm capacitor) without losing density, and the dossier does not carry that into the GO line.

*What would change the reviewer's mind:* M12 lateral-cavity coupons at 60 nm tier pitch reaching >=60 fF/um2 with J <=1e-7 A/cm2 after 4x cumulative 400 C exposure.

**Response — ACCEPTED-DOWNGRADE:** Valid. Planning EOT goes 0.50->0.60 nm (57.6 fF/um2). At the 0.60 fF planning Cs the capacitor is 88 nm (72 nm at 0.50 nm), costing ~8% density. At EOT 0.7 nm it is 104 nm, or ~4.2x 1-beta. The tier stack (26 nm SN + 2 x (6 nm dielectric + 5 nm plate) + ~12 nm isolation = 60 nm) agrees with PROC's >=27-32 nm shell but leaves no slack. The open question is a conformal ALD fill of an 88 nm slot from a 24:1 hole. The GO line now carries the capacitor: M12 coupons at 60 nm tier pitch must reach >=57.6 fF/um2 with J <=1e-7 A/cm2 after 4x cumulative 400 C. The density claim is quoted at the measured EOT.

*Action taken:* eot_nm 0.50->0.60 in the model. M12 gate and kill #4 revised to 4x cumulative exposure. Capacitor coupon line $20k->$25k.

## raw-ber-contract — RAW-BER CONTRACT (raw-ber-contract)

**Final status after red team: DOWNGRADED.** All 19 objections were accepted (0 refuted); none kills the relaxed-refresh core. The sense-amp flag leg is killed: a delayed strobe sees 50-150 ps skew against a 14-35 ps window, and even ideal flags net -2.2% to -0.2% of die. Keeping chipkill and moving to DDR5's real 32 ms window and post-on-die-SEC error structure cuts the commodity headline from 15x to ~9x at 85 C (6-20x; ~13x on retired DDR4; 2.9-4x in degraded mode). 64Gb refresh-busy recovery falls from ~38 to ~6-16 points, and the value is ~$3.9 per module over 5 yr. Provability falls from 'yes' to 'partly': raw 1b/1c maps need a vendor test mode, 2e-19 is bounded by census plus model, and the new-die sort flow stays on paper.

*Revised verdicts* — Possible: Yes for relaxed refresh behind a side-band code: coding theory on measured retention tails, no new physics. No for the delayed-strobe sense-amp flag as specified (killed). Revival only with silicon flag-window sigma <=1.5 mV and a positive ledger. · Profitable: Refresh energy and refresh-busy time, with chipkill kept: ~9x on DDR5 RDIMMs at 85 C (6.1x pessimistic, 20x optimistic, 17.8x without the DDR5 retention derate, ~35x at 65 C, 2.9x in degraded mode) and ~13x on retired DDR4 behind CXL (7.8x pessimistic, 4x degraded). Was 15x without chipkill. Module level: 0.98 -> 0.11 W per 64 GB, ~$3.9 per module over 5 yr. 64Gb refresh-busy 18% -> 2% (~6-16 points after same-bank refresh). Margin for new cells 1.88x (Cs 5.4 -> 2.7 fF), no flag bonus. · Doable by this founder: Partly. Yes: DDR4 raw physics, DDR5 post-on-die-ECC statistics (JEDEC ECS counts + open Antmicro DDR5 RDIMM testers), VRT coincidence and dwell-time (RTN) spectrum, failure-mode census, 1 h-grade vs 1,000 h-hold servo test, and DDR5 + retired-DDR4 CXL soaks. Phase 1 decisive ~$124k at M6; $946k all-in over 24 months. No: raw ECC-off 1b/1c maps (vendor test mode), 2e-19 per read directly (census + coincidence model bound it), and the sort/repair flow for dies built to contract (paper study).

### RT-CIRC-raw-ber-contract-01 — MAJOR — CIRC — §2.3 erasure flags / §6 IP 'file first: the DRAM sense-amp reliability flag'

> The flag circuit cannot resolve its own window. The window is delta = 0.5 sigma = 3.6 mV. A latch's resolution time scales as tau*ln(V/dV), so signals of 3.6 and 7.2 mV differ by only tau*ln2 ~ 15-35 ps (tau ~20-50 ps). SAN/SAP enable skew along a 1k-SA strip, plus supply droop when ~8k SAs latch at once, is tens to ~150 ps, so a delayed-strobe flag sees skew rather than signal unless every SA is calibrated. The DRAM Bender reduced-tRCD proxy measures column-path timing marginality, not latch metastability. Phase 1 therefore cannot validate the flag the IP strategy files first.

*What would change the reviewer's mind:* sky130 or 22FDX silicon showing a per-SA flag-window sigma <=1.5 mV across a >=1k-SA strip at 85 C without per-SA trim.

**Response — ACCEPTED-KILL:** Valid, and fatal to the delayed-strobe flag as specified. Model 10.5(a): the 3.6 mV window equals tau*ln2 = 14-35 ps of resolution time. A strobe-timing error s shifts the effective threshold by exp(s/tau). 50 ps of skew is 6-40 mV of equivalent amplitude noise, and 150 ps is 68 mV to >1 V. Only a locally referenced strobe pair with <=15 ps skew and tau >= 50 ps reaches ~1.2 mV, inside the critic's 1.5 mV line. An amplitude-domain alternative (an offset-cancelled dual-reference comparator) at 1.5 mV noise still flags 82% of errors at 7.2 false flags per error. It saves only 10 of 90 check bits (Chase t=8 vs hard t=9), and RT-CIRC-02 shows even ideal flags are net negative. Phase 1's reduced-tRCD proxy cannot validate the circuit (RT-DEV-01).

*Action taken:* Kill the per-read SA flag leg (named leg: delayed-sample flag latch). Revival needs silicon with flag-window sigma <=1.5 mV across >=1k SAs at 85 C without trim, plus a positive ledger. One amplitude-flag test structure rides the single remaining sky130 slot as revival data. The controller keeps a generic erasure input (chip marks, XED-style hints) at no cost.

### RT-CIRC-raw-ber-contract-02 — MAJOR — CIRC — §1 controller diagram ('data + unsure flags') / §2.3

> Flag storage and transport are not costed. The flag is born at row activation but read at the column access 15-50 ns later. Each bitline SA therefore needs a second latch and comparator: ~+20-40% SA-strip area, or ~+2-4% die [ESTIMATE]. DDR5 has no per-bit flag pins. At the modelled false-flag rate (~6e-4 per bit), a 512-bit line averages ~0.3 flags and needs ~10-20 bits of position code. BCH-12 already uses 120 of the 128 side-band bits, leaving 8. Flags must cost either burst beats (bandwidth) or check bits (code strength).

*What would change the reviewer's mind:* A protocol plus on-die encoder that carries flags within existing DDR5 RDIMM beats without weakening the code below the 2e-19 per read target, with the SA-strip area added.

**Response — ACCEPTED-KILL:** Valid; the ledger kills the per-bit flag as a product feature. Model 10.5(c-e) at raw BER 1e-4 with ideal flags: 0.40 flags per 640-bit line. One position plus an overflow bit costs 11 bits and overflows on 6.3% of lines; two positions cost 22 bits. Flags save 20 of 90 check bits (3.9% of die bits). The cost is >=11 transport bits (2.1%), or one extra beat in 16 (6.25% bandwidth), plus a second SA latch (+2-4% die). Net -2.2% to -0.2% of die. Inside the fixed 128-bit RDIMM side band, BCH t=10 + 2 flag positions (122 bits) reaches 3.62e-4 vs 3.32e-4 for plain BCH-12. That is +9% at best with ideal, all-soft flags, and -7% with 1.5 mV comparator noise. Refresh-latched (confident) errors erase the rest. No protocol carries flags for free.

*Action taken:* Same leg as RT-CIRC-01: the flag interface is removed from the contract and the headline. Revival only if a measured new-cell ledger is positive (e.g. >=25% parity saving, per RT-IND-02).

### RT-CIRC-raw-ber-contract-03 — MAJOR — CIRC — §2.5 / §2.4 (BCH-12 1.5 s vs RS-8 0.84 s; 'RS with one chip dead' 8.3e-7)

> The 15x refresh headline gives up chipkill. It is the BCH-12 path (1-1.5 s), which cannot correct a dead x4 chip (64 bits per line), and hyperscale RAS requires SDDC/chipkill. The RS-8 path keeps chipkill but gives 0.84 s central and 0.50 s pessimistic, i.e. 13x and 7.7x. With one chip already dead, the maximum raw BER is 8.3e-7, so refresh must fall back toward 64-128 ms in degraded mode until the DIMM is serviced. The honest server number is ~8-13x, with a degraded-mode fallback.

*What would change the reviewer's mind:* A code that gives both BCH-12-class random-bit correction and SDDC within 128 check bits, with a measured safe interval >=1 s at 85 C.

**Response — ACCEPTED-DOWNGRADE:** Valid: the 15x headline was the no-chipkill BCH-12 path. The headline now uses RS(80,64) byte symbols, which keep SDDC. Model 10.1: retired DDR4 at 85 C gives 837 ms = 13.1x central and 500 ms = 7.8x pessimistic. Degraded mode, with one chip marked dead (erasure decoding, limit 8.3e-7), gives 258 ms = 4.0x. DDR5 RDIMMs behind on-die SEC are worse, because SEC turns doublets into 3-symbol events (limit 1.5e-5). They give 285 ms = 8.9x central, 194 ms = 6.1x pessimistic, and 92 ms = 2.9x degraded (366 ms at 65 C). No code is known to us that gives BCH-12 random-bit capacity and SDDC within 128 bits. The Hamming bound does not forbid one (~2^83 random-12 patterns + ~2^67 chip patterns < 2^128 syndromes), so it is listed as an open coding question for the advisor. Degraded-mode rule: on chip marking, that rank drops to its degraded interval until service.

*Action taken:* Server headline restated as ~9x (DDR5) / ~13x (retired DDR4) at 85 C with chipkill, plus a degraded-mode fallback of 2.9-4x. BCH-12 kept only for non-chipkill tiers. Code question (SDDC + t~12 in 128 bits) assigned to the coding advisor.

### RT-CIRC-raw-ber-contract-04 — MAJOR — CIRC — §2.5 idle-power saving 14-16% / §4 #5 self-refresh

> Self-refresh may erase the idle saving. Idle is where refresh dominates module power, and DDR5 self-refresh runs off the on-die timer at a fixed tREFI, with temperature scaling only. Keeping DIMMs in power-down with controller-issued REF keeps the clock, the CA bus, the RCD and the controller PHY awake: ~0.3-1 W per RDIMM [ESTIMATE, training knowledge] against 0.456 W saved. Idle savings can go negative. The model treats this background cost as zero ('unmodelled').

*What would change the reviewer's mind:* Measured RDIMM plus PHY power on the Phase 2 platform, self-refresh versus power-down with 1 s controller REF, or a vendor test mode or JEDEC MR for a programmable self-refresh interval.

**Response — ACCEPTED-MITIGATED:** Valid for an always-on controller-REF policy. Model 10.3: the refresh saving while the controller issues REF is 0.865 W per 64 GB at the DDR5 central interval (32 ms baseline 0.98 W). With the critic's 0.3-1 W power-down background, always-on controller REF loses only if self-refresh residency exceeds ~87% at 1 W. That is a small loss, but a real one for deep-idle servers. The fix is a hybrid policy: idle ranks enter the die's own self-refresh (no saving, no loss), and the controller issues relaxed REF only in active/power-down states. Saving = 0.865 W x (1 - residency): 0.69 W and $3.94 per module over 5 yr at 20% residency; 0.43 W and $2.46 at 50%. A programmable self-refresh interval would recover the rest. LPDDR-style temperature-compensated self-refresh is a precedent [UNVERIFIED-PK]; that is a JEDEC ask. Phase 2 measures RDIMM + PHY power in self-refresh vs power-down with 1 s controller REF, as the critic asked.

*Action taken:* Hybrid self-refresh policy in the controller. Idle-saving claim restated to exclude self-refresh residency. Phase 2 power measurement added. Programmable self-refresh added to the JEDEC grade proposal.

### RT-CIRC-raw-ber-contract-05 — MAJOR — CIRC — §1 'ordinary loads and stores ~100-200 ns' / §2.1 decoder

> The read chain falls outside DRAM-class latency. The contract lives in a CXL Type-3 controller, which adds ~70-150 ns load-to-use over local DDR5 [training knowledge]. At the contract BER, BCH-12 takes the slow path on 1-(1-1e-4)^576 = 5.6% of lines (Berlekamp-Massey plus Chien, ~15-30 ns at 28 nm), and Chase decoding of flagged lines adds more, so p95 sits on the slow path. For the commodity path this is a capacity-tier product. For new cells 'built to contract' to stay in the 10-100 ns class, the decoder must move on-die or into the host memory controller, which the plan does not cost.

*What would change the reviewer's mind:* A measured p50/p99 load-to-use latency distribution at injected raw BER 1e-4 on the Phase 2 FPGA controller, with an ASIC projection for an on-die or host-side decoder.

**Response — ACCEPTED-MITIGATED:** Partly valid. The 5.6-6.2% slow path is real for raw DDR4 at 1e-4, but nearly all of it is single-symbol errors that a syndrome lookup fixes in ~4 ns. Model 10.4: at 1e-4, 6.2% of lines hold an error but only 0.20% need Berlekamp-Massey. At the servoed RS-8 operating BER (1.8e-5), 1.2% hold an error and 0.007% need BM; the mean adder is 0.05 ns and p99 is on the 4 ns lookup. Behind DDR5's on-die SEC, ~0% of lines need any fix. So decoding does not push p95 onto a 15-30 ns path. The CXL hop itself (+70-150 ns) is real: the commodity product is a capacity tier, as section 1 already stated ('~100-200 ns'). DRAM-class latency for cells built to contract needs the decoder in the host memory controller, where chipkill decoders already sit, or on-die.

*Action taken:* Single-symbol fast path specified in the controller. Phase 2 measures p50/p99 load-to-use at injected 1e-4 plus an ASIC projection for a host-IMC decoder (pass line: p99 decode adder <=5 ns). Commodity product labelled a capacity tier; host-IMC integration named as the DRAM-class path.

### RT-DEV-raw-ber-contract-01 — MAJOR — DEV — §5 steps 3 and 6 (reduced-tRCD double read as the flag proxy); GO-B (>=50% flaggable at 0.5 sigma)

> Reduced-tRCD failures are dominated by slow charge sharing (high access-transistor or contact resistance, slow SA enable) and cluster by subarray and column, as Solar-DRAM itself showed. The flag proposed for new silicon targets small |dV| from charge loss or small Cs. These are different populations: a full-charge cell with a slow access path fails early sampling with a large |dV|, while a leaky but fast cell fails late with a small |dV|. GO-B and the 20-check-bit saving can therefore pass or fail for the wrong physical reason.

*What would change the reviewer's mind:* A validation on the DRAM Bender rigs in which truncated-tRAS cells, whose |dV| is known by construction, are shown to be the cells flagged at reduced tRCD, with the column/subarray correlation of flags within 2x of random.

**Response — ACCEPTED-MITIGATED:** Valid. Reduced-tRCD failures track access-path timing: slow charge sharing, high access/contact resistance, subarray/column clustering (Solar-DRAM). The flag targets small |dV|, and these are different populations. The flag leg is now killed on circuit and bit-economics grounds: RT-CIRC-01, and RT-CIRC-02 (ideal flags net -2.2% to -0.2% of die; model 10.5). So GO-B is removed from the decisive gate and no decision rests on the proxy. As zero-hardware revival data, Phase 1 step 8 runs the critic's validation. Truncated-tRAS cells, whose |dV| is known by construction, are compared with reduced-tRCD flags: overlap, and column/subarray correlation of flags against random. An amplitude-domain proxy is added: two reads with opposite residual bitline offsets from a deliberately shortened tRP, whose disagreement set is |dV| < delta by construction [UNVERIFIED-PK method, FracDRAM/ComputeDRAM-style timing violation].

*Action taken:* GO-B (>=50% flaggable) deleted from the M6 gate. Proxy validation and a biased-precharge proxy kept in Phase 1 step 8 as revival data for the killed flag leg.

### RT-DEV-raw-ber-contract-02 — MAJOR — DEV — §5 population (60 DDR4 modules for raw physics; DDR5 only after on-die SEC) vs the commodity DDR5 RDIMM claim (§2.5, §2.7)

> The product claim is relaxed refresh on DDR5 RDIMMs, but the decisive raw retention, VRT and cluster data come from DDR4, because DDR5 hides raw errors behind on-die SEC. Retention tails at 85 C are set by GIDL and trap-assisted junction leakage and by the WL-off bias, all of which change with each buried-channel cell generation, and a 1-beta cell at ~5.4 fF stores less charge than typical DDR4 cells, so the same leakage fails it sooner. A lognormal fitted on DDR4 (median 82 s, sigma_ln 1.24) cannot set the DDR5 interval; the 0.84-1.5 s result is a DDR4 result.

*What would change the reviewer's mind:* Raw (ECC-off) retention and cluster maps on >=20 1-alpha/1-beta DDR5 dies, via a vendor test mode or a DDR5 PHY, showing a safe interval >=0.5 s at 85 C.

**Response — ACCEPTED-DOWNGRADE:** Valid, and the model was worse than the critic said. DDR5's own JEDEC window is 32 ms (tREFI 3.9 us x 8192 REF), half of DDR4's 64 ms [REPORTED, resp log]. That is direct evidence the tail moved left. The original model also paired DDR5's tREFI with a 64 ms window. The model now applies ret_time_scale_ddr5 = 0.5 (1.0 as sensitivity) and places the controller code behind DDR5 on-die SEC. That hurts RS-8: doublets become 3-symbol events, so the internal limit falls from 5.4e-5 to 1.5e-5. DDR5 RDIMM with chipkill at 85 C: central 285 ms = 8.9x the 32 ms spec; pessimistic 194 ms = 6.1x; optimistic 643 ms; 569 ms without the derate; 1.14 s at 65 C. The DDR4 lognormal no longer sets the DDR5 interval. Phase 1 adds a DDR5 leg (+$28k): >=24 1a/1b DDR5 RDIMMs from 2-3 vendors on two open Antmicro DDR5 RDIMM testers (Artix US+; Google-funded; used for the Phoenix DDR5 study). It reads per-die singleton counts through JEDEC ECS codeword-count mode; the 256/Gb threshold masks only BER < ~2.4e-7 on a 16Gb die. It adds post-SEC 2-3-bit event maps and inverts them with BEER-style H-matrix recovery. The critic's raw ECC-off maps still need a vendor test mode.

*Action taken:* Commodity DDR5 headline cut from 15x (DDR4-derived, no chipkill) to ~9x central (6-20x) at 85 C. DDR5 leg on open testers added to Phase 1. New kill #9 on the DDR5 inference. Vendor NDA test mode pursued in parallel.

### RT-IND-raw-ber-contract-01 — MAJOR — IND — §2.7 Energy value ($2.60 per 64 GB over 5 yr); §3 'Not new'; §7 Licensees

> The dossier values the commodity product at $2.60 per 64 GB module over 5 years (2.7% of module cost) and 14-16% of idle module power. The parties who could ship it can implement every piece in firmware: CXL controller vendors (Marvell Structera, Astera, Montage, Microchip); hyperscalers already running Vistara-style DDR4 reuse. The pieces are re-coding the 25% side band as BCH-12 or RS-8, temperature-tracked refresh and RFM substitution, all of which §3 says not to claim. A royalty on a $2.60 saving does not support a $10-50M company.

*What would change the reviewer's mind:* A controller vendor or hyperscaler quantifying a larger value (e.g., retention-reject DRAM sold as product at a stated $/GB, or measured 64Gb throughput recovered) and agreeing to license. Or a defensible claim on the relaxed-refresh + VRT-sized scrub + RFM combination.

**Response — ACCEPTED-DOWNGRADE:** Valid on value. A model fix partly offsets it: DDR5's real 32 ms window doubles the refresh baseline to 0.98 W per 64 GB. The saving at the revised central interval is 0.87 W; with 20% self-refresh residency (hybrid) it is 0.69 W = $3.94 per module over 5 yr ($0.062/GB, ~4% of module cost), not $2.60. That is still a feature, and section 3 already concedes no piece is claimable alone. Under the founder frame, business size is not a kill. But the step-change claim is restated: the commodity leg is ~9x on refresh energy, ~23-29% of a 3 W idle module, worth ~4% of module cost. The larger values are conditional and partly outside the $1M proof: 64Gb refresh-busy ~6-16 points, and new cells at half Cs. Strategy: lead with the open grade, the measured error atlas and a servoed reference controller (contributed to OCP/JEDEC), license the firmware to CXL controller vendors and hyperscalers, and treat venture scale as contingent on a new-cell partner qualifying to the grade.

*Action taken:* Commodity value restated at ~$3.9 per module over 5 yr. The company thesis moves from 'controller royalty' to 'grade + atlas + reference controller, venture value via new-cell partners'. Licensee asks become raise-stage milestones.

### RT-IND-raw-ber-contract-02 — MAJOR — IND — §3 Genuine delta #1; §2.3 'flags add ~8%'; §6 Provisional #1

> The strongest patent, the per-read sense-amp reliability flag, covers the least valuable feature: flags save at most 20 of 90 check bits (~8%); they are worth ~0 for resident data, because refresh latches retention errors to confident values; they need DRAM-vendor silicon and an interface change that JEDEC members (Samsung, SK hynix, Micron) control. The obviousness exposure is real: Razor's delayed-sample latch (MICRO 2003), NAND's soft-bit second sense (US 11,907,545) and time-dependent sense-amp sensitivity (US 4,545,036, 1985). This review's search found no direct anticipation (rt-IND), but the commercial lever stays in the vendors' hands.

*What would change the reviewer's mind:* A DRAM vendor engineering sample or test mode that exports a per-read flag. Or a measured flag value worth >=25% of parity on new-cell (MARGIN STACK) silicon.

**Response — ACCEPTED-DOWNGRADE:** Valid. The flag leg is now killed (RT-CIRC-01, RT-CIRC-02): ideal flags net -2.2% to -0.2% of die, and a delayed-strobe flag sees skew, not signal. Leading the IP with it would put the strongest-looking claim on a negative-value feature that DRAM vendors control. The IP order changes. Provisional #1 covers the raw-BER grade and test method (BER + cluster spectrum + VRT growth + chip-fault coincidence, code chosen from the grade). Provisional #2 covers servoed latching-aware relaxed refresh with first-read chip marking and a degraded-mode interval. A flag filing is optional and defensive only. For new-cell margin, idea I-12302 (plate-strip sensing, ~135 mV vs ~14 mV) is a far bigger lever than flags. Model 10.10: Cs 0.30 fF for 50 mV and 0.15 fF at the contract's 26.6 mV, vs 5.42 to 2.68 fF on bitline sensing. But it has planar Micron prior art (US 5,991,216; US 8,009,460) and its own disturb questions. It is a portfolio margin route, not replacement IP for this dossier. Net: the IP is thinner and the defensibility claim drops.

*Action taken:* IP strategy reordered: grade/test method and servoed refresh first, flag filing optional and defensive. IP budget $45k -> $35k. I-12302 recorded as the new-cell margin route.

### RT-IND-raw-ber-contract-03 — MAJOR — IND — §2.5 Refresh-blocked time; §2.7 'strategic: defuses the 64Gb tRFC crisis'

> The large 'strategic' value rests on an extrapolated 64Gb tRFC of ~1.6 us, i.e. 41% refresh-blocked time. JEDEC and the vendors already attack this inside the device with same-bank refresh (REFsb), finer-granularity refresh, PRAC/RFM and new bank organisations [training knowledge]. If 64Gb parts hide tRFC on-die, the controller's benefit falls back to the $2.60-per-module energy case. Memory makers also have little reason to bless relaxed-retention bins that cannibalise full-spec parts.

*What would change the reviewer's mind:* A vendor or JEDEC projection showing 64Gb refresh overhead >15% even with REFsb and FGR, plus one vendor willing to sell a relaxed-retention grade.

**Response — ACCEPTED-DOWNGRADE:** Valid. With tRFC at 700 ns (RT-PROC-04), 64Gb refresh-busy time is 17.9% on an all-bank basis. Same-bank refresh and finer granularity hide an estimated 1/2-2/3 of it (5.9-9.0% equivalent) [ESTIMATE]. Relaxed refresh divides whatever remains by ~9x (DDR5 central), so ~6-16 points are recovered rather than ~38. The 64Gb crisis case shrinks to 'meaningful, not decisive'. Vendor reluctance to bless relaxed-retention bins is a business risk, not physics, and under the founder frame it is not a kill. The servoed controller (RT-PROC-02) works on standard parts without a vendor bin. It does run REF outside the JEDEC average-rate rule, so it is a hyperscaler-validated mode, like Meta's DDR4 reuse, until a grade exists. A vendor willing to sell a relaxed-retention grade is a raise-stage milestone.

*Action taken:* Strategic 64Gb claim restated as ~6-16 points recovered. Out-of-spec REF named as an adoption risk. Vendor relaxed-grade commitment moved to the raise milestones.

### RT-IND-raw-ber-contract-04 — MAJOR — IND — §5 Decisive experiment (60 DDR4 modules + post-SEC DDR5); §4 #6

> The month-6 GO/NO-GO is measured on 60 DDR4 modules (no on-die ECC) from older nodes, plus post-SEC DDR5 statistics. Error geometry, VRT growth and cluster spectra will differ on 1b/1c DDR5 and on the oxide and 3D cells the contract exists to enable. DDR5's on-die SEC turns a 2-bit error into a 3-bit burst ~53% of the time (dossier), which is exactly the cluster regime that breaks BCH-12. A memory maker will call the atlas a description of legacy parts. An investor gets a characterization paper of a kind SAFARI has published for a decade (RAIDR, REAPER, PaCRAM).

*What would change the reviewer's mind:* Vendor test-mode access (under NDA) to raw pre-ECC errors on 1b/1c DDR5, or the same atlas measured on oxide coupons, with <=0.4% of error bits in >=3-bit clusters.

**Response — ACCEPTED-MITIGATED:** Valid as an investor read of the original plan. First, the DDR5 leg measures the governed product's post-SEC error stream, which is what the controller decodes, on 1a/1b RDIMMs via ECS counts and open DDR5 testers. Raw ECC-off maps remain a vendor-NDA item. Second, the investor-grade deliverable becomes a running system, not an atlas. That means 1,000 h soaks at the servoed interval on DDR5 RDIMMs (controller RTL on the open tester) and on retired DDR4 behind the CXL FPGA, with 0 UE and corrected errors within 2x of model. Retired DDR4 behind CXL is the Meta/Marvell landing zone and gives 13x central with chipkill. Third, the delta versus SAFARI's decade of characterization is stated narrowly. It is a grade (BER + cluster spectrum + VRT growth + chip-fault coincidence) scored against side-band codes at 2e-19, plus a servo that holds the grade in-system. The oxide-coupon atlas is deferred to the AND-STACK/PIXEL-STACK partners.

*Action taken:* Demo redefined around DDR5 + retired-DDR4 system soaks. DDR5 leg added. Novelty claim narrowed to grade + servo. Vendor test mode and oxide coupons listed as raise-stage evidence.

### RT-PROC-raw-ber-contract-01 — MAJOR — PROC — §5 Phase 1 population (60 DDR4 modules); §4 #6; DRAM Bender has no DDR5 support

> The GO/NO-GO is measured on DDR4 because DDR4 has no on-die ECC, but 2026 DDR4 is mostly 1y/1z/1a silicon. 1b/1c cells (smaller Cs, newer high-k stacks, buried-WL GIDL, tighter-pitch hammer coupling) ship only as DDR5/LPDDR5. There, 128+8 SEC hides raw singletons and miscorrects doublets (~53% per §2.4). The decisive cluster spectrum, VRT growth and flaggable share are therefore measured on cells 2-3 generations older than any product the contract would govern. The 'DDR5 cross-check' sees only post-SEC statistics.

*What would change the reviewer's mind:* Raw (ECC-bypassed) error maps from current 1b/1c DDR5 or LPDDR5X dies through a vendor test mode under NDA, matching the DDR4 cluster spectrum and VRT growth within 2x.

**Response — ACCEPTED-MITIGATED:** Valid: same core as RT-DEV-02, from the process side. The DDR4 population is kept for raw spatial physics and adds a node-trend axis: 1x/1y/1z/1a date codes, fitted to extrapolate retention tail, cluster spectrum and VRT one generation. The new DDR5 leg measures the governed product on 1a/1b DDR5 RDIMMs. It reads per-die singleton counts from JEDEC ECS codeword mode and maps post-SEC 2-3-bit events. Their spatial geometry is visible because SEC events are chip-confined, and BEER/HARP-style H-matrix recovery inverts them to raw rates. The red-team model run shows the post-SEC structure is what matters for the commodity product: the controller never sees singletons, and RS-8 behind SEC tolerates 1.5e-5 internal BER vs 5.4e-5 on raw DDR4. So the DDR5 GO is computed on the post-SEC stream, which the leg measures directly. Raw 1b/1c singleton spatial maps, the critic's exact ask, need a vendor test mode under NDA. They matter mainly for the new-cell leg and are pursued as a business-development item.

*Action taken:* DDR5 leg (ECS + post-SEC maps + H-matrix inversion) and a DDR4 node-trend axis added. DDR5 gate set on post-SEC data (kill #9). Vendor test mode sought for raw maps.

### RT-PROC-raw-ber-contract-02 — MAJOR — PROC — §2.5 safe interval; §8 'zero wafer starts'; §5 population (3 vendors x 2-3 date codes)

> Commodity parts are screened at sort to 64 ms (32 ms hot) plus guard band. Beyond that screen the retention distribution is uncontrolled: it shifts with die revision (vendors ship A/B/M-die and node shrinks under one part number) and with test-program changes. 60 modules from 3 vendors x 2-3 date codes cover a handful of wafer lots per vendor, yet a contract interval must hold for the worst lot in a fab's lot-to-lot distribution. The 'zero wafer starts' relaxed-refresh product therefore needs a vendor-run screen (a new bin), not just a controller.

*What would change the reviewer's mind:* Safe-interval data across >=30 lots per vendor, including two die revisions, showing the worst-lot 85 C safe interval >=0.5 s. Alternatively, a vendor commitment to a 1 s retention screen.

**Response — ACCEPTED-MITIGATED:** Valid for a fixed fleet interval, but the controller need not use one. It servos each rank's interval on its own corrected-error telemetry, keeping measured BER at 1/3 of the code limit. That is NAND-style adaptive trim, and it costs 0.73x in interval at the DDR5 tail slope (BER ~ t^3.4). Model 10.8 with lot retention scale lognormal: at sigma_ln 0.35, a fixed interval covering the 1-in-1000 lot is 97 ms (3.0x), while adaptive per-module gives a 6.1x fleet-mean cut. At sigma 0.7 it is 33 ms (1.0x) vs 5.1x. Proving a 1-in-100 worst lot directly needs ~298 lots, which $1M cannot sample. So the demo proves the servo instead: each module is graded from <=1 h of test, and the grade must hold over 1,000 h for >=95% of modules. The DDR4 quick screen is widened to 150 modules over >=30 lots per vendor (+$6k), to measure sigma_lot. 'Zero wafer starts' stays true. A vendor 1 s retention screen becomes an optional bin, not a requirement.

*Action taken:* Per-module servoed interval added to the controller; population widened to >=30 lots/vendor; servo pass line (1 h grade holds 1,000 h for >=95%) in the M6 gate. The fleet claim is restated as a distribution: ~6x fleet-mean vs 8.9x nominal.

### RT-PROC-raw-ber-contract-03 — MAJOR — PROC — §2.6-2.7 'New 1-beta-class die built to contract'; §4 #7

> At raw BER 1e-4 a 16 Gb die ships ~1.7M weak bits. Wafer sort must therefore change from 'repair every fail' to 'repair clusters, leave singletons', and it must certify a cluster spectrum and a VRT growth rate per die. VRT growth needs hours to days of soak and cannot be screened at sort, so it becomes a lot statistic. Per-die DUE (2e-19 per read) is then guaranteed only statistically, and outlier dies escape. Redundancy, fuse budgets and test time (multi-second pauses x temperatures x patterns) all need redesign, and none of it is costed or planned.

*What would change the reviewer's mind:* A sort/repair flow, with a test-time estimate, that bounds per-die cluster and VRT parameters from <=1 h of test, validated by post-sort dies staying within the grade after 1,000 h.

**Response — ACCEPTED-MITIGATED:** Valid: the new-die leg needs a sort/repair flow, and none was planned. Model 10.9 sketches one: pauses of 0.5/1/2 s x 4 patterns x 2 temperatures = 28 s, plus ~12 s of write/read passes. That is ~40 s per batch, ~0.08 s per die at 512 parallel sites [ESTIMATE]. The same maps give each die's cluster spectrum. 'Repair clusters, leave singletons' consumes fewer fuses than 'repair every fail'. VRT growth cannot be screened at sort; it becomes a lot statistic from sampled 24-48 h soaks. Per-die escapes are caught in the field by the controller's servo, first-read chip marking and PPR, as NAND controllers handle bad blocks. Per-die guarantees are therefore statistical plus field-adaptive, as in NAND. Validation within $1M follows the critic's criterion scaled to modules: grade from <=1 h of test, hold over the 1,000 h soak. Redundancy/fuse redesign and tester cost stay unquantified: a partner-stage task.

*Action taken:* Sort-flow test-time estimate added (model 10.9). 1 h-grade vs 1,000 h-hold test in Phase 1 step 6. Fuse/redundancy design deferred to the first DRAM partner and listed as unproven in the PROVABLE verdict.

### RT-DEV-raw-ber-contract-03 — MINOR — DEV — §2.5 VRT growth input (1x static BER per day); §9 kill #4

> VRT comes from metastable defects in the storage-node depletion region whose switching is thermally activated (activation energies near 1 eV are typical). At 85 C cells toggle between leaky and normal states on minute-to-hour scales, so the population that is marginal at 1 s is far larger than at 64 ms. The 1x/day growth input has no source. The 4-week, 20-module soak measures a mean growth rate but not the joint probability of 2-3 VRT cells landing in one 64 B codeword within one scrub period.

*What would change the reviewer's mind:* Measured per-codeword VRT coincidence statistics at 1 s/85 C over >=4 weeks, folded into the 2e-19 calculation.

**Response — ACCEPTED-MITIGATED:** Valid. The 1x/day VRT growth is an unsourced ESTIMATE (swept 0.1-100x/day), and the plan measured mean growth, not same-codeword coincidence. Model 10.7: if 10% of VRT error bits arrive as same-codeword pairs, the BCH-12 limit falls from 3.32e-4 to 1.02e-4, and to 4.6e-5 at 30%. RS-8 counts a pair as at most two symbols, so the chipkill path, now the headline, is insensitive. The kill #4 threshold is unchanged: ~700x/day still holds >=0.5 s with a 10-minute scrub on RS-8 (DDR4 basis). Phase 1 adds per-codeword VRT arrival counts per scrub period at 1 s/85 C over 1,000 h on 20 modules (overdispersion vs Poisson, folded into the 2e-19 calculation). It also adds a VRT dwell-time spectrum, the RTN-at-the-right-timescale measurement: row subsets re-mapped every 20 s-20 min at 85 C (<= 1/3 of the shortest dwell), plus hourly whole-module maps.

*Action taken:* Phase 1 step 4: VRT coincidence counts and a dwell-time (RTN) spectrum. The VRT pass line requires per-codeword pairs within 2x of Poisson.

### RT-DEV-raw-ber-contract-04 — MINOR — DEV — §2.1 target 2e-19 per read; §5 pass line 'overdispersion within 2x of Poisson to 6 errors'

> BCH-12 fails at >=13 errors per codeword, so the 2e-19 target is set by rare correlated mechanisms: a weak sub-wordline driver under-restoring a whole chip's contribution, or a MAT-edge defect, at 1e-12 to 1e-18 per codeword. A 6-month study of ~80 modules yields ~1e12-1e13 codeword observations, which bounds nothing below ~1e-12, and a Poisson check to 6 errors says nothing about 13.

*What would change the reviewer's mind:* A physical failure-mode census (sub-WL driver, MAT, column) with each mechanism's rate bounded independently, or fleet telemetry at >=1e15 codewords, before the JEDEC grade is fixed.

**Response — ACCEPTED-MITIGATED:** Valid: counting cannot reach 2e-19, and correlated mechanisms set the tail. First, RS-8 with chipkill is now the headline code. Any mechanism confined to one chip is corrected, such as a weak sub-wordline driver or a MAT-edge defect inside one die. The residual is coincidence: a chip-confined fault plus one random symbol error in another chip on the same read. Model 10.6 uses 30 FIT/die of multi-bit faults [UNVERIFIED-PK field studies], i.e. 0.0105 per module-year. UE = faults x reads-before-marking x q. q rises from 1e-6 at 64 ms to 1.0e-2 on raw DDR4 at a servoed 1.8e-5 BER. That gives 1.1e-4 UE/module-yr if the controller marks a chip on its first chip-confined correction, but 1.1e-3 (the whole budget) after 10 reads. Behind DDR5 on-die SEC, q = 1.7e-6, giving 1.8e-8. Second, the 'Poisson to 6 errors' check is replaced by a failure-mode census. Every multi-bit event is classified by chip, DQ, beat, row, column and MAT, and each mechanism's event rate is measured at 1 s vs 32/64 ms. 1.8e5 module-hours bound an unseen mechanism at <=0.15 per module-year, i.e. a UE share <=2.5e-7 on DDR5. On DDR4 that bound is 1.5e-3, so DDR4 needs a ~10x BER guard or more census. Multi-chip common-mode events (VPP droop, thermal slew faster than the scheduler) remain for fleet telemetry. The JEDEC grade is fixed only after >=1e15-codeword fleet data, at the raise stage.

*Action taken:* Failure-mode census replaces the overdispersion-to-6 pass line. First-read chip marking becomes a contract rule (new kill #10). Chip-fault coincidence term added to the model. Grade frozen only after fleet data.

### RT-DEV-raw-ber-contract-05 — MINOR — DEV — §9 kill #1 revival ('oxide/IGZO cells, whose retention tail sits 1e3-1e4x to the right')

> No IGZO DRAM array retention distribution at the 1e-4 to 1e-9 quantiles has been published: OCTRAM and 3D OCTRAM report a typical Ioff and no tail, and the rt-DEV search found no test temperature. Oxide cells also bring their own error physics: PBTI and hydrogen Vt drift that is systematic and correlated with temperature history, and RTN-driven off-current switching that behaves like VRT. The revival condition is unsupported as written.

*What would change the reviewer's mind:* A published IGZO 1T1C or 2T0C array retention CDF down to <=1e-6 at 85 C.

**Response — ACCEPTED-MITIGATED:** Valid. No published IGZO array retention CDF reaches 1e-6 at 85 C. rt-DEV and this response found only typical Ioff; Kioxia OCTRAM quotes <1 aA with no temperature or statistic. The '1e3-1e4x to the right' figure was a typical-Ioff ratio and is withdrawn as a tail claim. Oxide PBTI and hydrogen Vt drift (systematic, history-correlated) and RTN-like Ioff switching are additional error terms the grade must carry. The revival condition is restated as a measurement: an oxide or gain-cell array retention CDF to <=1e-6 at 85 C, >=10x right of Si at equal Cs, with drift and RTN terms characterised. Idea I-12627 adds a design lever: two series write devices square the tail only if defects are independent. Model 10.10, DDR4-anchor tail at the RS-8 limit: interval 0.84 s goes to 5.6 s at rho = 0, but only 1.8 s at rho = 0.1 and 1.3 s at rho = 0.3. The tail-correlation test is therefore the decisive measurement, and the lever does not apply to Si storage-node junction/GIDL leakage.

*Action taken:* Kill #1 revival rewritten as a measurable condition (CDF to 1e-6 at 85 C plus drift and RTN terms). I-12627 stacked-write route recorded, with its rho <= 0.1 requirement. The 1e3-1e4x claim is removed.

### RT-IND-raw-ber-contract-05 — MINOR — IND — §7 Licensees (CXL controller vendors); §7 '$10-15M: 22/28 nm CXL Type-3 controller ASIC'

> The landing zone is CXL memory expansion, yet the dossier's own examples (Meta Vistara, Marvell Structera X/XA) use retired DDR4 for capacity, where refresh power is noise at server level. A $10-15M controller ASIC (~25 people for ~2 years) would compete with incumbents that already ship CXL controllers with ECC and compression. The differentiation is a firmware feature set.

*What would change the reviewer's mind:* Two module makers or hyperscalers committing to a design-in on the strength of the 1,000 h soak.

**Response — ACCEPTED-DOWNGRADE:** Valid in part. Retired DDR4 behind CXL is where the physics is best: no on-die SEC, and RS-8 with chipkill gives 837 ms = 13x central, 7.8x pessimistic and 4x degraded. But at server level the saving is ~0.45 W per 64 GB DDR4 module (64 ms basis), and the CXL hop adds 70-150 ns. It is a capacity tier, and the feature is firmware-sized. The plan no longer presents a $10-15M controller ASIC as the value path. The first commercial vehicle is licensing the servoed refresh + grade firmware into existing CXL controllers (Marvell, Microchip, Astera, Montage). An ASIC is built only if a new-cell partner needs one. Two design-in commitments cannot be bought with $1M; they are a raise-stage milestone that follows the soak.

*Action taken:* Section 7's '$10-15M ASIC' is demoted to contingent. Firmware licensing into incumbent CXL controllers is the first vehicle. Two design-in letters become a raise milestone.

### RT-PROC-raw-ber-contract-04 — MINOR — PROC — §2.5 refresh-blocked time 41% -> 2.6% at 64Gb; model INPUT trfc_ns 64Gb = 1600

> The 1.6 us tRFC for 64Gb is an extrapolation. Yet JEDEC kept DDR5 tRFC1 at 410 ns from 24Gb to 32Gb (the model's own input), because vendors add internal parallel refresh rather than lengthen tRFC. At a plausible 0.6-0.8 us, the blocked fraction is ~15-20%, not 41%. That shrinks the 'strategic 64Gb tRFC crisis' argument, which carries most of the commodity value; energy alone is worth $2.60 per module over 5 years.

*What would change the reviewer's mind:* A published JEDEC or vendor 64Gb tRFC >=1.2 us, or vendor evidence that same-bank/fine-granularity refresh cannot hold tRFC under 1 us.

**Response — ACCEPTED-DOWNGRADE:** Valid. 64Gb tRFC input revised from 1600 to 700 ns central (600-800 range; 1600 kept as an upper sensitivity). This response's search did not confirm any 64Gb or even the 32Gb 410 ns value. Model 10.2: blocked time at 3.9 us tREFI is 15.4/17.9/20.5% at 600/700/800 ns, not 41%. At the revised DDR5 central interval (285 ms) it falls to 1.7-2.3%, so ~13-18 points are recovered on an all-bank basis, not ~38. The same fix to the refresh window also changes 16Gb at 1 s: 0.24% blocked, not 0.48% (model section 5).

*Action taken:* trfc_ns[64Gb] 1600 -> 700 ns in the RED-TEAM REVISIONS block. The 'defuses the 64Gb tRFC crisis' claim is restated as ~6-16 points of refresh-busy time recovered (after same-bank refresh).
