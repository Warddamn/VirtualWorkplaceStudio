# Oxide Tail Spec: one shared lot, measured for its worst devices

*v1.0, 2026-11-04. Request for a quote and for existing data. Print landscape, one page.*

**Purpose.** Seven memory concepts in our study stand or fall on the worst 1-in-10,000 to 1-in-50,000 devices (the 1e-4 to 2e-5 quantile), not the median. The two numbers are attoamp off-state leakage (1 aA = 1e-18 A) and random telegraph noise (RTN: one trapped charge switching a transistor's threshold), in amorphous-oxide transistors of ≤0.01-0.02 µm² at 85-125 °C, after the full ≤400 °C hydrogen, thermal and bonding budget [DJ]. Published data describe medians. **We ask** [JP, JI, JO]: (1) can you build and measure the structures below on one shared lot (two if needed) from January 2027, at what cost? (2) Do you hold per-device leakage or RTN distributions on ≥1e4 devices you could share under NDA? (3) Can you host, or name a partner for, the bond split?

| # | Structure (serves) | Channel splits | Device area | Timescale | Temp (°C) | H / thermal dose | Bond split | N per split | Pass / kill line [source] |
|-|-------|------|------|------|----|-----|--|-----|----------------|
| 1 | Floating-node leakage cells, single vs series write gate (MARGIN, AND, PIXEL) | C4; planar vs etched sidewall (MARGIN) | Design-size write FETs | Write-wait-read, 10 ms-1e5 s | 85; 1,000 h stress at 105 (MARGIN) | D3; hold 0 to −0.5 V (MARGIN), −3.0 V (AND) | No | ≥1e6 (MARGIN); ≥1e4 per gate type (AND, PIXEL) | MARGIN: aged 2e-5 quantile ≤586 aA GO, >1,172 aA kills cuts beyond 5.4x [MS §11.3, §9]. AND: write-FET tail ≤17 aA GO, >100 aA drops 2 bits/cell, >1 fA kills [AS §5, §9]. PIXEL: tail ≤45 aA GO, ≤90 aA plan, >225 aA kills the refresh claim, after 4x dose [PS §5, §9]. Report series-gate tail correlation [JP] |
| 2 | 2T0C gain-cell arrays, vertical channel-all-around (HOT) | C4; H-lean vs PECVD seal, ± ALD Al₂O₃ | Read gate ≥0.01 µm²; 25 arrays × 4 kb | Drift 1/10/100 s; RTN ≥100 reads ~1 s apart + 1 µs-1 ms reads | 85/105/125; write T1, read T2 (ΔT ±30 K) | Post-bond heat/H sequence; single vs series gate; −0.5 vs −0.7 V hold | Yes | ≥1e5 cells | 1 bit/cell GO if a split has drift σ ≤75 mV (1 s, 105 °C), RTN ≤100 mV, tail ≤22.5 aA at 125 °C, bonded ΔVt ≤10 mV. KILL if one line fails in every split (tail judged at 105 °C). 2 bits: drift ≤20 mV, RTN ≤30 mV, tail ≤7.5 aA at 105 °C [HS §5, §9, §11] |
| 3 | Small source followers (SF), on-coupon 15 ns dual sample-hold (PIXEL, DIODE) | C4; three SF gate stacks | 0.01-0.02 µm² (200 × 100 nm design; L 50 and 100 nm); ladder to 1 µm² | 15 ns CDS gap; ≥1e4 reads per node | 25/55/85 | D3 | No | 65,536 nodes (64 × 64, ≥16 dies) | PIXEL: per-sense 2e-7 residual ≤20 mV GO, ≤40 mV plan, >55 mV NO-GO; >3% of SFs with >8 mV steps kills the plan [PS §5, §9]. DIODE: RTN tail ≤25 mV; >50 mV at both L kills [DT §5R, §9] |
| 4 | fF-node ns sampler: IGZO FETs on sky130 CMOS die (MARGIN, CHARGE) | IGZO | 2,827 and 5,655 nm² (MARGIN); 0.40 fF node (CHARGE) | 1-3 ns gap (MARGIN); 2-5 ns, ≥1e7 samples/node (CHARGE) | 25-110 (MARGIN); 85 | ≤350 °C | No | ≥1e4 FETs or nodes | MARGIN: RTN tail ≤44 mV at 85 °C; >82 mV kills cuts beyond 5.4x [MS §9 K9]. CHARGE: 1e-9 step ≤30 e⁻ with ≤2% spared; >5% spared kills [CH §5, §9] |
| 5 | Planar coupling-ratio (CR) and disturb cells (AND) | C4 (lot) | 64-cell AND emulation; FETs at real lengths | Retention to 1e4 s; RTN 10 ns-1 s; ≥100 re-reads | 85; Vt(T) 25-110; ΔT ±10 K | Lot baseline | No | CR ≥50 cells; ≥1e4 FETs | CR ≥0.57 at σ ≤0.045 (CR <0.40 kills single-etch); ≤111 fA per unselected cell; 4 levels ≥1 s, ≤78 mV drift; disturb ≤30 mV after 1e9 neighbour writes [AS §5, §9] |
| 6 | Integrable-anode Schottky diodes (DIODE) | RuO₂, MoOx, WOx, IrO₂ on IGZO, Ga-rich IGZO, a-Ga₂O₃ | Ring 2,600 nm²; 1-2 fF floating nodes | Droop to ~1e-19 A; 1,000 h re-test; 1e12 pulses | 85 at 0.8 V; 25-125; 0 | ≤300 °C, 2 × 350, 400 °C 1 h | No | ≥1,000 nodes (target 16k) | PASS: 99.99th-percentile ring leakage ≤928 aA; ≥1.8 nA at ≤1.2 V, 0 °C; barrier shift ≤30 meV. KILL: every integrable split >928 aA [DT §5R, §9] |
| 7 | Minimal 3-phase CCDs, if the imec paper read passes (CHARGE) | Surface IGZO; buried IGO, In₂O₃; Ga-free ITZO, ZTO | Gates 25-250 nm; overlapping 2-level reference; 16/64/256 stages | Clock 4-200 MHz | 25 and 85 | ≤400 °C | No | Median per variant | Median CTE ≥0.9973 (with DFE) at ≥150 MT/s, buried ≥3x better: GO. <0.9951 at ≥50 MT/s in all variants: KILL [CH §5, §9] |
| 8 | Bond monitors: top- vs bottom-tier TFTs, SIMS (HOT, CELL-WAFER) | Best row-2 split; 3 barrier stacks | Cells, select and driver TFTs | ns-µs RTN; s-scale VRT; 1,000 h | 85; 125 for 1,000 h; 3 × 260 reflow | As row 2 | Yes | 1e4-1e5 devices | HOT: ΔVt ≤10 mV. CELL-WAFER: ΔVt ≤20 mV and retention within 2x after bond, reflow and 1,000 h, else kill [HS §5; CW §5R, §9] |
| 9 | Lateral-cavity capacitors, 60 nm tier pitch (PIXEL rider) | TiN/ZrO₂/TiN | 60-110 nm recesses | — | 25-85 | 4 × 400 °C | No | — | ≥57.6 fF/µm² at J ≤1e-7 A/cm²: pass; <40 fF/µm² or J ≥1e-6: fail [PS §5, §9] |

**Key.** C4 = IGZO (indium gallium zinc oxide), In-poor IGZO, IGO (indium gallium oxide), Ga-free ZTO (zinc tin oxide) or In₂O₃; ITZO = indium tin zinc oxide. D3 = 1x/2x/4x cumulative H and thermal dose, all ≤400 °C. Bond = Si cap chips fusion-bonded over the arrays, 350-400 °C (chemistry under NDA). Tail = 1e-4 quantile. 2T0C = 2 transistors, 0 capacitors; CDS = correlated double sampling; CCD = charge-coupled device; CTE = charge-transfer efficiency; DFE = decision feedback; ΔVt = threshold shift; VRT = variable retention time; SIMS = secondary-ion mass spectrometry. Names in capitals are study concepts. Row 2 is vertical; row 4 is on CMOS die; the rest are planar. Every number is [STUDY]: from the cited repo file, not yet measured. Full GO / KILL / REVIVE lines: spec page 4.

**Sources.** DJ = research/stage3/decision.json (biggest_unknown, PORTFOLIO); JP, JI, JO = research/stage3/judge_{physicist,investor,operator}.json (monday_action; JP gate M9 G3); HS, AS, MS, PS, DT, CH, CW = dossiers/hot-side-memory, and-stack, margin-stack, pixel-stack, diode-tower, charge-river, cell-wafer-foundry .md (§5 experiment, §9 kills, §11 red team). Facility: https://birck.research.purdue.edu/equipment/become-a-user/ [REPORTED].

<div style="page-break-after: always;"></div>

## Pages 2-4: the working notes behind the table

*For you, and for the lab under NDA. Page 1 alone is [OXIDE_TAIL_SPEC_onepage.md](OXIDE_TAIL_SPEC_onepage.md).* **Tags:** [STUDY] = copied from a repo file (model output, dossier line or judge decision), cited by file and section; not a measurement. [ESTIMATE] = arithmetic done for this spec. [REPORTED] = paper or official page; URLs come from the repo's source logs and were not re-fetched. [UNVERIFIED] = not confirmed. Dossier §11 (red-team outcome) overrides the dossier body ([README](../README.md)).

### Before you send page 1

- **Disclosure.** The study's rule: file the provisionals before any disclosure, so the spec shows test structures and pass lines only ([report §9](../DRAM_MOONSHOT_REPORT.md#9-first-90-days-for-the-best-bet)). The planned provisionals cover bond-interface hydrogen control with D₂O (heavy-water) qualification, and cross-temperature multi-level cells (report §9; JP sequence M0-1). So page 1 says "chemistry under NDA" for the bond and omits the cross-temperature reference scheme.
- **Timing conflict.** The Monday action sends on day 1; the provisionals are filed in weeks 9-10 (report §9). Choose: file early, send under NDA, or send page 1 as written.
- **Who.** Purdue Birck (Peide Ye group), Georgia Tech IEN (Datta, Khan, Yu groups; now listed as IMS, see [LAB_TARGETS.md](LAB_TARGETS.md)) and two imec IGZO-2T0C alumni; apply as a Birck external user the same morning (JP monday_action); copy your top 3 co-founder candidates (JO). Names are from training knowledge [UNVERIFIED].

### 2. Why one measurement decides seven concepts

Almost every oxide pass line sits in the 1e-4 to 2e-5 tail (two go to 2e-7 and 1e-9); published data are medians (DJ biggest_unknown) [STUDY]. imec's oxide 2T0C cell holds >200 s at 95 °C [REPORTED, Sources], which implies ~75 zA (1e-21 A) on the study's 0.15 fF node ([HS §2](../dossiers/hot-side-memory.md#2-the-physics-and-the-numbers-revised-after-red-team)). The red team moved HOT-SIDE's tail from 3x to 25x the median, 91x unmitigated ([HS §11](../dossiers/hot-side-memory.md#11-red-team-outcome)). "Whether the tail is ~3x or ~90x the median picks the winner" (JI). Near-Gaussian tails keep 3-4 cells alive; heavy tails leave RAW-BER plus a 1-bit HOT-SIDE tier (JO biggest_unknown) [STUDY].

| Concept | What it is | Tail it needs | Rows | Pass buys | Fail costs |
|---|---|---|---|---|---|
| [HOT-SIDE](../dossiers/hot-side-memory.md) (BEST BET) | Oxide 2T0C gain-cell tiers bonded next to a GPU | Retention tail ≤22.5 aA at 125 °C; RTN ≤100 mV; drift ≤75 mV | 2, 8 | ~10x lower energy per bit than HBM (0.37 vs 3.95 pJ/bit) | Capacity claim dies |
| [AND-STACK](../dossiers/and-stack.md) (MOONSHOT) | DRAM built like 3D NAND, a 2-bit oxide cell per tier | Write-FET tail ≤17 aA; coupling ratio ≥0.57 | 1, 5 | Closure coupon released; 5.9x 1-beta density | >100 aA: 1 bit, no coupon; >1 fA: kill |
| [MARGIN](../dossiers/margin-stack.md) | A gain FET per 64 cells allows a 0.5 fF capacitor | Aged 2e-5 leakage ≤586 aA; ns RTN ≤44 mV | 1, 4 | Capacitor 10.8x shorter | 1.0 fF fallback (5.4x) |
| [PIXEL](../dossiers/pixel-stack.md) | 3D 1T1C stack read like an image sensor | Residual ≤20/40 mV at 15 ns; tail ≤45/90 aA | 1, 3, 9 | ~4.6x 1-beta density | >55 mV: no oxide amp tier |
| [DIODE](../dossiers/diode-tower.md) | Oxide Schottky diodes steer 16-64 capacitor tiers | Ring leakage ≤928 aA; RTN ≤25 mV | 3, 6 | 3.9x 1-beta at 64 tiers | 3.9x configuration dies |
| [CHARGE-RIVER](../dossiers/charge-river.md) | Charge packets marched through oxide CCD strings | CTE ≥0.9973; RTN ≤30 e⁻ | 4, 7 | ~2.5x density, ~158x lower standby power | Device dies below 0.9951 |
| [CELL-WAFER](../dossiers/cell-wafer-foundry.md) | Oxide cell wafers bonded to U.S. logic | Bonded ΔVt ≤20 mV | 8 | Bond path for whichever cell passes | Oxide cells fail hybrid bonding |

All [STUDY], from each dossier's §5, §9 and §11 and [report §6](../DRAM_MOONSHOT_REPORT.md#6-the-10-concepts-that-came-out). The other three concepts need no oxide tail: RAW-BER (relaxed refresh on today's DRAM under error correction), LEAN ARRAY (hydrogen in place of helium for wafer cooling) and AI MEMORY DIET (AI cache streaming). RAW-BER's revival path does use one oxide number, the series-gate tail correlation ([raw-ber §9](../dossiers/raw-ber-contract.md#9-kill-criteria)).

### 3. Measurement methods

**3.1 Leakage by floating-node droop, I = C·dV/dt** ([FP §2.2](../home-lab/FIRST_PRINCIPLES.md#22-retention-t--cδv--i_leak-and-its-inverse-i--cdvdt-calcs-3)). Calibrate each node's C with a known charge step (the 2T0C node is ~0.15 fF, HS §2). Write, switch the write FET off at the set hold bias, wait, read through the read FET. Two products: (a) a write-wait-read ladder on every cell, pass/fail at a fixed droop, which gives the 1e-4 retention quantile directly; (b) full droop traces on a subsample, for current and activation energy. Run ≥2 blank (dummy) nodes per temperature. Current meters bottom out near 10 fA [REPORTED via FP §2.2, S10]; on a fF node each attoamp pass line becomes a 50-150 mV droop in 0.06-1 s [ESTIMATE]: 22.5 aA × 1 s ÷ 0.15 fF = 150 mV (HOT, 1 bit); 7.5 aA → 50 mV (2 bits); 586 aA × 64 ms ÷ 0.5 fF = 75 mV (MARGIN; MS §9 K2 states 75 mV); 45 aA × 1 s ÷ 0.60 fF = 75 mV (PIXEL); 928 aA × 64 ms ÷ 0.594 fF = 100 mV (DIODE). Serial probing of 1e5 devices takes 11.6 days per condition (FP §4), so cells must sit in multiplexed arrays. Label any lognormal extrapolation as a model.

**3.2 RTN capture.** Time domain, per device, at the gap the product uses: double sampling cancels noise slower than its gap, so the gap decides which traps count [ESTIMATE]. Benches cannot reach 1-3 ns, hence on-chip sample-and-hold (JO sequence M2-9). Keep raw sample pairs so any gap can be re-analysed.

| Concept | Gap | Statistic | Population [STUDY] |
|---|---|---|---|
| PIXEL | 15 ns | Joint per-sense 2e-7 residual; share of SFs with >8 mV steps | 65,536 nodes × ≥1e4 reads |
| DIODE | ~15 ns | 1e-4 amplitude, L = 50 and 100 nm | ≥65k FETs ≤0.01 µm² |
| MARGIN | 1-3 ns | 1e-4 between-sample jump | ≥1e4 FETs, 2,827 and 5,655 nm² |
| CHARGE-RIVER | 2-5 ns | 1e-9 per-read step | ≥1e4 nodes × ≥1e7 samples |
| HOT | ~1 s; 1 µs-1 ms | 1e-4 quantile | ≥1e5 cells |
| AND | 10 ns-1 s | Read-FET RTN | ≥1e4 read FETs |
| CELL-WAFER | ns-µs; seconds | Top- vs bottom-tier shift, VRT | 1e4-1e5 devices |

One trapped electron shifts the threshold by ~q/(C_ox·W·L): 8.7 mV for a 40 × 40 nm FET at 3 nm EOT (equivalent oxide thickness). Steps are roughly exponential, so the 1e-4 device sees ~9x the mean step, and a 100 mV line fails if the mean exceeds ~11 mV ([FP §2.13](../home-lab/FIRST_PRINCIPLES.md#213-random-telegraph-noise-why-tails-not-medians-set-refresh-calcs-13)) [STUDY].

**3.3 Arrhenius at 25/85/105/125 °C.** Pass lines sit at 85, 105 and 125 °C (HS §5); the 25 °C point is this spec's addition, to anchor each device's activation energy Ea [ESTIMATE]. Tail cells can have their own Ea: in silicon DRAM ~0.35 eV vs 0.6-0.7 eV for main cells [REPORTED via FP §2.7, S8]. No 125 °C oxide 2T0C data is published (FP §2.7). Log the device temperature itself: a 10 K error moves Ea ~21-23% over 25→65 °C (FP §2.7). Cross-temperature maps write at T1 and read at T2: ΔT ±30 K (HOT), ±10 K (AND, characterised to ±50 K), ±60 K (DIODE) [STUDY]. Expected leakage ratios [ESTIMATE] at Ea = 0.35 / 0.6 / 0.8 eV (0.8 eV is the study's oxide value, FP §2.7): 25→85 °C gives 10x / 50x / 184x; 85→105 °C gives 1.8x / 2.8x / 3.9x; 105→125 °C gives 1.7x / 2.5x / 3.4x.

**3.4 Dose and bond** [STUDY]. Lot-wide 1x/2x/4x cumulative ≤400 °C dose (JP, JO); PIXEL adds as-built, N₂, forming-gas and H-rich PECVD SiN splits, each ± ALD Al₂O₃ (PS §5). HOT post-bond sequence: 350 °C/2 h, 400 °C/30 min forming gas, PECVD SiN, 400 °C anneal. Real bond: D₂O-hydrated, plasma-activated Si cap chips with 0.5-1 µm bond oxide, fusion-bonded over the arrays at 350-400 °C, then SIMS H/D (HS §5). CELL-WAFER adds anneals at 150-300 °C (CW §5R); MARGIN passes if the tail grows ≤2x in the 1,000 h stress (MS §5.1).

### 4. Statistics: why ≥1e5 cells per split

The count beyond the true p-quantile is Binomial(N, p), so the tail level's relative error is ~1/√(Np). Estimating needs Np ≥10-30; a zero-failure pass at 95% needs N ≥ −ln(0.05)/p ≈ 3/p. Hence ≥1e5 cells per split ([FP §4](../home-lab/FIRST_PRINCIPLES.md#4-statistics-of-tails-how-many-samples-a-1e-4-quantile-needs-calcs-14)).

Zero-failure N is ~3.0e4 at 1e-4 and ~1.5e5 at 2e-5 (FP §4); a data-only 95% upper bound needs 36,887 and 184,450 (leakage_tail.py sample-size table); PIXEL's per-sense 2e-7 needs ~1.5e7 senses and CHARGE-RIVER's per-read 1e-9 ~3.0e9 reads [ESTIMATE]. **Each page-1 row against its quantile** [ESTIMATE; 95% distribution-free range of the true level]:

| Row | p | N asked | Np | 95% range | Verdict |
|---|---|---|---|---|---|
| 2 HOT | 1e-4 | 102,400 | 10 | 4e-5 to 1.8e-4 | OK |
| 1 MARGIN | 2e-5 | 1e6 | 20 | 1.2e-5 to 3e-5 | OK; one 2.5e5-cell die gives a bound only |
| 1, 5 AND | 1e-4 | 1e4 | 1 | 0 to 4e-4 | **Short**: ~3e4 to pass, 1e5 to estimate |
| 3 PIXEL | 2e-7/sense | 6.5e8 senses | 130 | 1.7e-7 to 2.4e-7 | OK per sense; per device (65,536) Np is only 6.6 |
| 3 DIODE RTN | 1e-4 | 65,536 | 6.6 | 3.1e-5 to 2e-4 | Marginal |
| 6 DIODE | 1e-4 | 1,000 (16k) | 0.1 (1.6) | 0 to 2e-3 (3.7e-4) | **Short**; DT §5 extrapolates from the 99.9th and says so |
| 4 CHARGE | 1e-9/read | 1e11 reads | 100 | 8e-10 to 1.2e-9 | OK per read |

**Independence.** A series write gate squares the tail only if the two devices' defects are independent (HS §11; PS §11). AND-STACK rejects it because one hole shares films and hydrogen (AS §11.2). Measure it: compare the series-gate tail with the square of the single-gate tail at the same current. In the RAW-BER model a correlation share of 0.1 lifts the safe interval from 0.84 to 1.8 s; 5.6 s needs zero (raw-ber §9) [STUDY]. **VRT** (variable retention time): re-measure ≥100 times on ≥1e4 cells (AS §5); re-test DIODE nodes after 1,000 h (DT §5R).

### 5. Deliverables and data format

Per split [ESTIMATE, proposed]: write-wait-read logs for every cell (A); droop traces for every cell beyond the 1e-3 quantile plus ≥1,000 random cells (B); raw RTN pairs (C); a metadata JSON per die (split, gate, hold bias, dose, bond, barrier, node-C calibration, chuck temperature log, wafer map); SIMS, CTE, I-V-T and C-V data as CSV in SI units.

**Format A** for [retention_map.py](../home-lab/code/T3_dram/retention_map.py) `analyze`:
```
HELLO,<tool_version>,<split_name>,<n_words>,<bits_per_word>,0,B|C
RUN,<id>,B,<pattern 0=all-0 | 1=all-1>,0,0,<wait_ms>,<repeat>,<temp_setpoint_C>
TEMP,<id>,start,<measured_C>
F,<id>,<word_index_hex>,<expected_hex>,<observed_hex>
END,<id>,<fail_words>,<fail_bits>,<bits_1to0>,<bits_0to1>,<logged_words>,<interval_ms>,OK
```
Method B = write-wait-read; method C = zero-wait control. Run all-0 and all-1 at each wait and repeat. interval_ms = the true wait. Waits are whole ms; ≤32 cells per word; pass `--words-per-row`.

**Format B** for [leakage_tail.py](../home-lab/code/T2_analysis/leakage_tail.py): CSV `device,temperature,time,voltage,run,cap_pf,temp_meas_C` (extra columns ignored). Device = unique cell ID, e.g. `IGZO-series/d03/r012/c117`; °C; seconds after switch-off; node volts; cap_pf in pF (0.15 fF = 0.00015). ≥30 in-range points per record; ≥2 BLANK records per temperature.

**Format C** (proposed; no parser yet): `device,temperature,gap_ns,read_index,v_first_V,v_second_V`.

**Checked 2026-11-04 on synthetic fab-style files** [ESTIMATE]: both scripts exit 0, and retention_map.py recovers a planted Ea of 0.80 eV. Caveats: leakage_tail.py hard-codes the home bench window, 0.45-2.04 V and ≤0.5 V droop (lines 83-86), so fab nodes outside it are dropped; add a window option before data arrives. retention_map.py flags any split named "SYNTH…" as synthetic; its sections 1-3 (CDF, quantiles, Arrhenius) apply, its DDR5 error-correction verdict does not. Neither script parses RTN yet.

### 6. Budget and schedule (from the judges)

**Budget, thousands of US dollars** [STUDY: DJ PORTFOLIO, judge budgets; totals ESTIMATE]:

| Line | Physicist | Investor | Operator |
|---|---|---|---|
| Shared lot | 220 (two lots) | 140 fab + 35 D₂O bond | 210 (one lot) |
| Riders | 100: diode 30, CCD 40, AND 30 | 70: AND 35, diode 20, CCD 15 | 80: AND 15, CCD 40, pixel caps 20, diode 5 |
| Bench, metrology | 60 | 80 | 60 |
| sky130 carrier | 85 | 25 | 80 |
| **Total** | **465** | **350** | **430** |
| After M9, if tails pass | AND coupon 100 | AND coupon 120 | AND TCAD + coupon 110 |

HOT-SIDE's standalone Gate A+ is ~$240k: $130k coupons (6 splits, 2 lots), $25k real bond, $85k bench (HS §5). The AND coupon releases only if the write-FET tail is ≤100 aA (JP; JI adds CR ≥0.40). The CCD rider runs only if the imec paper read passes, else $40k returns to contingency (JO G-M0). Birck 2023 for-profit rates: $51/day lab + $61/day cleanroom + tool hours, e-beam $115-132/h [REPORTED, Sources; E8 §13].

**Schedule** [STUDY]. Month 0 = January 2027 ([report §8](../DRAM_MOONSHOT_REPORT.md#8-the-1m-portfolio-and-gates)).

| When | What (source) |
|---|---|
| Day 1, 2026-11-02 | Spec, emails, Birck application (report §9) |
| Weeks 9-10 (M0) | Provisionals filed; Birck and IEN agreements; bench ordered (report §9) |
| M1-3 | One shared reticle taped, frozen by M3 (JP; JI G0) |
| M2-10 / M3-9 | One lot (JO) or two lots (JP); sky130 shuttle M2-9 (JO; MS §5.1 has M2-13) |
| 2027-07-30 (M7) | DIODE Gate A (DT §9) |
| 2027-09-30 (M9) | Portfolio read: PIXEL, AND #1A, leakage tails (JP G3; AS §9; PS §9) |
| 2027-10-31 to 2027-12-31 | CHARGE-RIVER Gate 1 (M10); HOT-SIDE Gate A+ 2027-11-30 (HS §9); CHARGE-RIVER RTN gate (CH §9; CH §11 says M12-16) |
| M12-16 | 1,000 h 105 °C stress (JO); CELL-WAFER hydrogen gate K3′ at M14 (CW §9); MARGIN K2 and K9 on 2028-04-30 (MS §9) |

### 7. What you bring

- **The spec and its decision rule, written before any data** (section 8). The study kills only for physics, and every kill names a revival ([MISSION.md](../MISSION.md)).
- **Analysis code**: [leakage_tail.py](../home-lab/code/T2_analysis/leakage_tail.py) (droop slopes, blanks, distribution-free and bootstrap intervals, lognormal check, per-device Ea) and [retention_map.py](../home-lab/code/T3_dram/retention_map.py) (write-wait-read CDFs, tail quantiles 1e-7 to 1e-2, Arrhenius, VRT). Check: `python3 home-lab/tools/check_home_lab.py`. Self-tested on synthetic data only ([home-lab README](../home-lab/README.md)).
- **Home-lab rehearsal data, when you have it**: E4 leakage distributions ([E4 §12](../home-lab/E4_femtoamp_leakage_bench.md#12-rehearsing-the-oxide-tail-spec)), an E6 DRAM retention map ([E6 §15](../home-lab/E6_retention_tail_real_dram.md#15-how-this-connects-to-the-oxide-tail-spec-the-studys-monday-action)), E7/E8 ZnO data ([E8 §13](../home-lab/E8_your_own_oxide_gain_cell_memory.md#13-from-this-demo-to-a-nanofab-your-ticket)). None exists yet (no data files in home-lab/ on 2026-11-04). Home floors are ~1-10 fA: it shows you can run the method, not the result (home-lab README).
- **People.** The lot is run by the study's first recruit, an oxide device-reliability physicist (DJ recruit_first); you run analysis and RAW-BER (report §8).

### 8. Decision rule per concept: GO / KILL / REVIVE

All [STUDY], from each dossier's §5, §9 (revised after the red team) and §11.

| Concept, gate | GO | KILL | REVIVE |
|---|---|---|---|
| HOT-SIDE, 2027-11-30 | 1 bit: one split has drift σ ≤75 mV (1 s, 105 °C), RTN ≤100 mV, tail ≤22.5 aA at 125 °C, bonded ΔVt ≤10 mV. 2 bits adds ≤20 mV drift in a ≥600 mV window, cross-T ≤10 mV, RTN ≤30 mV, ≤7.5 aA at 105 °C | Capacity claim, if every split (real-bond, series-gate, −0.7 V included) fails one line: drift >75 mV at 1 s and 100 ms; retention <1 s at 105 °C (>22.5 aA); RTN >100 mV | H barrier plus In-poor/ZTO split at ≤25 mV drift; write-FET σVt ≤30 mV; a larger read gate or lower-trap gate stack |
| AND-STACK, 2027-09-30 | Write-FET tail ≤17 aA at −3.0 V, 85 °C; CR ≥0.57, σ ≤0.045; ≤111 fA per unselected cell; 4 levels ≥1 s, ≤78 mV; cross-T BER ≤1e-4; disturb ≤30 mV | Tails >1 fA; CR <0.40 or σ >0.07 (single-etch); on/off <1e4 at ≤3.5 V. >100 aA drops 2 bits and the coupon | −3.5 V hold with 8-10 nm write-gate dielectric, or higher-Vt write film; >3.5 V drivers |
| MARGIN, 2028-04-30 | Aged 2e-5 ≤586 aA (≤1,881 aA conditional); RTN ≤44 mV at 1-3 ns | >1,172 aA on both splits or RTN >82 mV: no cut beyond 5.4x. >6,352 aA: oxide access dies | Negative-WL hold ≥−0.3 V, H+O anneal or In-lean channel; 4-pillar gain FETs or RTN screening |
| PIXEL, 2027-09-30 | Residual ≤20 mV (0.45 fF), ≤40 mV plan (0.60 fF); tail ≤45 aA (≤90 plan) after 4x dose; ≤1% SFs >8 mV | >55 mV: no oxide amp tier; >3% SFs >8 mV: no 0.60 fF plan; >225 aA or σVt >50 mV: no refresh claim | α_H ≤1e-2; 0.03 µm² SF or lower-trap stack; Ga-free/In-poor channel; independent series-gate tails |
| DIODE, 2027-07-30 (RTN M9) | ≤928 aA at 99.99th, 85 °C, 0.8 V; ≥1.8 nA at ≤1.2 V, 0 °C, n ≤1.3; Δφ ≤30 meV at 1e12; RTN ≤25 mV | Every integrable split >928 aA; Δφ >60 meV by 1e10; σ >0.07 eV; <1.8 nA (no 10 ns write); RTN >50 mV at both L | 80 nm escape contact (2.9x); profiled tier repair; Ga₂O₃ shell; Smart-Cut silicon sense layer |
| CHARGE-RIVER, 2027-10-31 (RTN 2027-12-31; M12-16 in CH §11) | CTE ≥0.9973 with DFE at ≥150 MT/s, 25/85 °C; buried ≥3x; 1e-9 step ≤30 e⁻ with ≤2% spared | CTE <0.9951 at ≥50 MT/s, all variants; >5% spared; 85 °C retention <2 s | ≥0.997 from any channel; dense-decode-only use at 4-6 MHz; bonded Si followers |
| CELL-WAFER, M14 | No D-traced H rise in the top-tier channel; ΔVt ≤20 mV on cells and TFTs | ΔVt >20 mV or retention down >2x at every anneal, best barrier | Room-temperature Cu-only bonding; thicker barrier with H getter; TFTs on the substrate side |

**Portfolio rule.** At M9 the remaining ~$270k goes to the cells that pass (JP G3). At M12, ≥70% of cash goes to the lead: HOT-SIDE if Gate A+ passes at 1 bit, else PIXEL if it passes; if both fail, publish the dataset and re-plan (JO). If nothing passes, sell or license the data and IP and return capital (JI G6).

### Appendix: where the source files disagree

1. **Seven or six concepts.** DJ, JP and README say seven (CELL-WAFER via bond hydrogen); JI and JO list six. This spec: seven, CELL-WAFER in row 8 only.
2. **HOT tail temperature.** Pass is ≤22.5 aA at 125 °C (HS §5, §11, model); kill is retention <1 s at 105 °C (HS §9, DJ). 105-125 °C is a grey zone.
3. **RTN gap.** JP scores MARGIN on the 15 ns coupon at M9; MS needs 1-3 ns on sky130 (K9, 2028-04-30) and CH needs 2-5 ns. This spec: row 4.
4. **PIXEL metric.** JP calls it a 1e-4 step quantile; PS §5 uses the joint per-sense 2e-7 residual, with 1e-4 step sub-gates of ≤6 and ≤10 mV.
5. **NO-GO level.** JP: >55 mV for all source-follower reads; MS K9 kills at >82 mV; DT at >50 mV. This spec: each dossier's line.
6. **AND M9.** JP drops 2 bits and single-etch at CR <0.57 or >100 aA; JI kills at CR <0.40 or >100 aA; AS §9 drops 2 bits at >100 aA and kills at >1 fA or CR <0.40. This spec: AS §9.
7. **Planar or vertical 2T0C.** JP: one planar reticle; HS §5 and JI: vertical channel-all-around arrays. Ask the lab.
8. **One lot or two.** JP and report §9: two; JO and JI: one. Ask for both quotes.
9. **Riders and carrier.** Rider sets differ (only JO has pixel capacitors). sky130 carrier: JP 85, JO 80, JI 25; HS §5 dropped sky130 for 22FDX.
10. **Sample sizes.** AND's ≥1e4 and DIODE's ≥1,000 nodes cannot resolve a 1e-4 quantile (FP §4).
11. **Disclosure timing**, and a rounding nit (29,956 in E4 §12 and leakage_tail.py, 29,957 in FP §4).

### Sources

**Repo files** (links relative to this file): [decision.json](../research/stage3/decision.json) (DJ: biggest_unknown, monday_action, PORTFOLIO, recruit_first); [judge_physicist.json](../research/stage3/judge_physicist.json) (JP), [judge_investor.json](../research/stage3/judge_investor.json) (JI), [judge_operator.json](../research/stage3/judge_operator.json) (JO); dossiers §2, §5, §9, §11: [hot-side-memory](../dossiers/hot-side-memory.md) (HS), [and-stack](../dossiers/and-stack.md) (AS), [margin-stack](../dossiers/margin-stack.md) (MS), [pixel-stack](../dossiers/pixel-stack.md) (PS), [diode-tower](../dossiers/diode-tower.md) (DT), [charge-river](../dossiers/charge-river.md) (CH), [cell-wafer-foundry](../dossiers/cell-wafer-foundry.md) (CW), [raw-ber-contract](../dossiers/raw-ber-contract.md) §9; [DRAM_MOONSHOT_REPORT.md](../DRAM_MOONSHOT_REPORT.md) §1, §6, §8, §9; [README.md](../README.md); [MISSION.md](../MISSION.md); home lab [README](../home-lab/README.md), [FIRST_PRINCIPLES.md](../home-lab/FIRST_PRINCIPLES.md) (FP) §2.2, §2.7, §2.13, §4, [E4](../home-lab/E4_femtoamp_leakage_bench.md) §12, [E6](../home-lab/E6_retention_tail_real_dram.md) §15, [E8](../home-lab/E8_your_own_oxide_gain_cell_memory.md) §13, [leakage_tail.py](../home-lab/code/T2_analysis/leakage_tail.py), [retention_map.py](../home-lab/code/T3_dram/retention_map.py).

**External** [REPORTED; from the repo's source logs, not re-fetched]:
- Purdue Birck external users and rates: https://birck.research.purdue.edu/equipment/become-a-user/ ; https://birck.research.purdue.edu/getting-started-at-birck/rates/ ; https://engineering.purdue.edu/ECN/mailman/archives/bnc-all/2023-May/002727.html (E8 R2).
- Georgia Tech IEN core users: https://dev.research.gatech.edu/nano/become-core-user (E8 R3).
- Purdue Ye group vertical all-oxide TFTs, VLSI 2024: https://engineering.purdue.edu/~yep/Papers/VLSI2024%20T4-1_Zehao%20Lin.pdf ; Georgia Tech oxide gain cells: https://shimeng.ece.gatech.edu/?p=916 (PS §5).
- imec IGZO 2T0C, >200 s at 95 °C (EDL 2025): https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234 (FP S16).
- Floating-node method, 135 yA/µm at 85 °C (JJAP 51, 021201): https://doi.org/10.1143/JJAP.51.021201 (FP S10).
- DRAM tail activation energy (Weber et al.): https://tore.tuhh.de/entities/publication/d044c2f2-f544-42c7-8293-2985814bdad2 (FP S8).
- imec IEDM 2024 paper 37-6, the oxide CCD CTE definition: https://doi.org/10.1109/iedm50854.2024.10873539 (JI monday_action).
