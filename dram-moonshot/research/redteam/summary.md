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
