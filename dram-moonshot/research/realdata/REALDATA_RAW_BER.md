# The FASTEST PROOF on real public data: raw-ber-contract

*Task C1. As of 2026-11-04. Scripts and derived numbers are in this folder. Raw data stays outside the repository; `fetch_data.py` re-downloads it. Reviewed and corrected by task C2 the same day; section 9 lists the changes. Corrected again the same day for the DDR4 line geometry (the model had given DDR4 the 128 check bits of a DDR5 line); section 10 lists those changes.*

**Evidence tags.** [DATASHEET] = a part's datasheet. [REPORTED] = a paper, press or official page, with its URL. [ESTIMATE] = arithmetic in this folder's scripts on real data, or the study's own model. [UNVERIFIED] = not checked.

**Acronyms.** DRAM: dynamic random-access memory. BER: bit error rate. ECC: error-correcting code. RS-8: the Reed-Solomon byte code the dossier uses, which keeps chipkill (it survives one dead chip). BCH-12: a binary code that does not keep chipkill. SEC: the single-error-correcting code inside each DDR5 chip (on-die ECC). VRT: variable retention time, when a cell's retention time jumps between values. Ea: activation energy, which sets how fast leakage grows with temperature. CE / UE: correctable / uncorrectable error. CI: 95% confidence interval. DIMM: memory module.

---

## 1. The answer in one page

**What could be tested.** Only one public raw dataset was both reachable and on topic: CMU SAFARI's retention measurements of 31 DDR3L modules from 2015-16, at 20 and 70 °C, with refresh paused for 64 ms to 2.048 s. No public field log with chip-level fields could be downloaded here. No public DDR4 or DDR5 retention data, and no public on-die-ECC chip data, were found.

**Main findings** [ESTIMATE unless tagged]:

1. **The model's retention tail is far too pessimistic for these parts.** At 70 °C the model expects 166x to 10,000x more failing bits than were measured between 0.5 and 2 s. At 256 ms it expects ~158 failing bits per module per test. All 28 modules measured at 70 °C showed 0.
2. **The tail's shape is close to the model's; its position is not.** The fitted lognormal width σ_ln (the spread of log retention time) is 1.05 (CI 0.97-1.12). The model uses 1.24. Per module it ranges 0.73-1.25. The tail widens with time: the local width grows from 0.78 (0.5-1 s) to 1.08 (1.5-2 s), which bends the safe way.
3. **The weakest cells barely speed up with heat, at the error rate measured.** Between 20 and 70 °C, the time to reach a fleet-mean BER of ~3e-9 shrinks only ~2x. That is Ea = 0.13 eV (CI 0.10-0.17), or 0.16 eV without module C4, which holds 76% of the 20 °C errors. The model assumes ~0.72 eV ("x4 per 20 °C"). Only 10 of 28 modules have errors at 20 °C; the other 18 give lower bounds (≥0.09-0.25 eV) that 0.72 eV also meets. The code limits sit near BER 1e-5, 3.7 decades deeper, where Ea is not measured and is likely higher. So cooling a module may buy much less than the model says: at the measured rate, 45 °C gives ~1.4x over 70 °C, not the model's ~5.7x.
4. **Re-running the model with the measured tail lengthens the safe interval about 3x.** DDR5 case, chipkill kept, 85 °C, with the model's own 0.5x DDR5 derate and its 0.72 eV above 70 °C: **0.96 s (CI 0.85-1.14 s), i.e. 30x the 32 ms window**. The model says 0.285 s (8.9x). Three pessimistic variants give 0.80-0.89 s (25-28x). The worst single module gives 0.59 s (18x). A bound that needs no extrapolation in BER gives at least 0.37 s (11.5x).
5. **Kill line at 65 °C: not triggered on these parts.** The data is taken at 70 °C, which is hotter than 65 °C, so it is a conservative check. At 2.048 s the fleet-mean BER sits 153x below the chipkill limit of a DDR4 line with two channels in lockstep, and the worst module 24x below. On a single DDR4 channel (RS(72,64), 64 check bits) the fleet margin is only 4.2x, and the worst module passes at 1.536 s but not at 2.048 s. (Corrected 2026-11-04: the first version gave 276x and 44x, against a 640-bit line with 128 check bits that a DDR4 module does not have.) For the DDR5 case (0.5x derate, so the same cells at 1.024 s) the margins are 77x and 12x. That is ≥32x the window for the fleet, and ≥24x for the worst module on one DDR4 channel, with no BER extrapolation, against a NO-GO line of <4x.
6. **Field data.** Public field studies show that 30-42% of DRAM faults are not single-bit, and ~23% of DDR4 faults hit several bits [REPORTED]. That supports keeping chipkill. In over 40% of DRAM-caused server failures, CEs first appear less than an hour before the failure [REPORTED]. Warnings are short. That supports the dossier's rule to mark a chip on its first chip-confined correction, not after many. The multi-chip kill line (>10% of events) cannot be tested with public data.
7. **A flaw found in the kill line.** If errors are independent, chance alone puts 0.5-1.6% of events on two chips with RS-8. At the BCH-12 limit it is 9.3%, close to the 10% NO-GO line. Counted by bytes, as kill #2 words it, chance alone gives 0.6-1.7% with RS-8 and 10.1% at the BCH-12 limit, already over the line. The census must compare against this chance level.

**Verdict on the ~9x claim.** Public data does not contradict it. For DDR3-class cells it looks conservative by about 3x (25-30x instead of 9x). It is **not testable for DDR5 with public data**. The DDR5 number rests on three untested inputs: the 0.5x retention derate, the on-die SEC error structure and VRT growth. Keep ~9x as the planning number. Treat ~25-30x as upside that only the Phase 1 DDR5 leg can confirm. That upside needs a per-module servo (fleet cut ~31x); one fixed interval for every module must suit the worst one and gives ~18x.

---

## 2. Datasets found

| # | Name | Source URL | License | Size | What it has | Used? |
|---|---|---|---|---|---|---|
| 1 | SAFARI DRAM-Voltage-Study, `retention_time_profile.csv` | https://github.com/CMU-SAFARI/DRAM-Voltage-Study | No license file in the repo, so all rights are reserved by default [REPORTED: repo tree, commit b2089c3] | 1,539,105 bytes, 28,657 rows | 31 DDR3L SO-DIMMs (10 vendor A, 12 B, 9 C); 2 GB each, 4 x 4Gb chips [REPORTED: https://arxiv.org/abs/1705.10292, via search snippet]; 20 and 70 °C ambient; 1.15/1.2/1.35 V; refresh paused 64-2048 ms; bit-error counts per bank per test. C2 check: the file's row-weighted means equal the paper's reported average weak-cell counts (section 3) | **Yes.** Raw file kept out of git; only fits and fleet means are committed |
| 2 | Same repo, `dimm_faulty_cachelines_out.csv` | same | same | 3,848 bytes | Voltage-induced errors, not retention | No (off topic) |
| 3 | Alibaba SRDS'22 DRAM error logs (`dramdata`) | https://github.com/alibaba-edu/dcbrain/tree/master/dramdata ; data at https://tianchi.aliyun.com/dataset/132973 | CC BY-SA 4.0 per C1's search snippet; a C2 search of the same page showed no licence text [UNVERIFIED] | 410.69 MB `dramdata.zip`, uploaded 2022-06-20 [REPORTED: Tianchi page via search snippet] | >70M CEs from >250K servers and 3M DIMMs over 8 months. Fields: server, DIMM, rank, bank, row, column, error type, time. Trouble tickets with UE/CE-driven failure type and time. **No chip (device) field** [REPORTED: readme, re-read by C2] | No. Tianchi was blocked from this session and needs a login; it is also above the 200 MB budget. `field_logs.py` reads it as is |
| 4 | Huawei SmartMem (WWW 2025 competition) | https://www.codabench.org/competitions/3586/ ; site source https://github.com/hwcloud-RAS/SmartMem.github.io | CC BY-NC 4.0 under competition rules that forbid redistribution [REPORTED: the site's terms page] | Not stated | Per-DIMM mcelog with 23 columns, **including deviceid (chip), bank group, bank, row, column and a DQ x beat error bitmap**; DIMM failure tickets [REPORTED: the site's dataset page] | No. Needs Codabench registration; cannot be shared; **non-commercial use only**, academic research included [REPORTED: terms page]. The per-DIMM files carry no serial-number column (the file name is the serial) [REPORTED: dataset page]. The best public source for the multi-chip question |
| 5 | Huawei M2-MFP repository | https://github.com/hwcloud-RAS/M2-MFP | CC BY-NC-SA 4.0 [REPORTED: README] | README and code only; data "will be provided in future updates" | Monthly counts: DIMMs with CEs, failed DIMMs, CE totals (Jan-Jul 2024, Intel Purley and Cascade) | Aggregates only (section 4.8) |
| 6 | Sandia Astra memory error and system monitoring data | https://doi.org/10.5281/zenodo.6515019 [REPORTED: cited in a later paper, via search snippet]; a C2 search found the paper's promise to publish the data but not the record itself [UNVERIFIED] | Not verified [UNVERIFIED] | Not verified | CE records plus power and temperature for a petascale Arm system [REPORTED: https://www.osti.gov/biblio/2003151] | No. zenodo.org was blocked |
| 7 | Khan et al. SIGMETRICS 2014 "full data sets" (retention, VRT) | http://www.ece.cmu.edu/~safari/tools/dram-sigmetrics2014-fulldata.html [REPORTED: search snippet] | Not verified | Not verified | Retention-failure data from the VRT study [UNVERIFIED: contents] | No. Host blocked. **The most valuable missing set for VRT** |
| 8 | EINSim (on-die ECC simulator) | https://github.com/CMU-SAFARI/EINSim | MIT [REPORTED: README] | Small | Simulator. The README at tag `full-size-dataset-v1.0` says the real-chip experimental data was **withheld for confidentiality**; only simulated "proxy" data ships [REPORTED, checked by C2] | No (no chip data) |
| 9 | BEER, HARP (on-die ECC tools) | https://github.com/CMU-SAFARI/BEER , https://github.com/CMU-SAFARI/HARP | MIT [REPORTED: READMEs] | Small | Tools that recover or work around on-die ECC; simulated errors | No (tools, not data). Useful for Phase 1 |
| 10 | SoftMC, DRAM Bender (test platforms) | https://github.com/CMU-SAFARI/SoftMC , https://github.com/CMU-SAFARI/DRAM-Bender | MIT [REPORTED: LICENSE files, checked by C2] | - | Retention-test programs, no result data | No. These are the Phase 1 tools |
| 11 | Liu et al. ISCA 2013 (248 DDR3 chips, VRT) | https://arxiv.org/pdf/2306.16037 (retrospective) | - | - | No public data link found [REPORTED: search] | No |
| 12 | Google 2009, Sridharan (Jaguar, Cielo, Hopper), Beigi 2023 (DDR4), Cheng 2022 (Alibaba) field studies | see Sources | - | - | Published aggregates only, used as parameters (section 4.8) | As parameters only |
| 13 | Decay-based DRAM PUF data (PUF: physically unclonable function) | https://par.nsf.gov/servlets/purl/10077358 | - | - | No public dataset found [REPORTED: search] | No |
| 14 | Computer Failure Data Repository | https://www.usenix.org/cfdr | - | - | Not checked: host blocked [UNVERIFIED] | No |

**Total downloaded:** ~1.5 MB of data (plus ~0.2 MB of READMEs and site pages). Well inside the 200 MB budget.

**Re-download:** `python3 -I research/realdata/fetch_data.py --dest ~/dram-realdata` fetches rows 1-2 from a pinned commit and checks their SHA-256. `--list` prints how to get rows 3-7 by hand.

---

## 3. Methods

All scripts are stdlib + numpy and have `--selftest` (synthetic data with known answers; all pass).

| Script | What it does |
|---|---|
| `fetch_data.py` | Downloads dataset 1 at commit b2089c3, checks SHA-256, lists the gated sets |
| `retention_fit.py` | Fits the retention data and re-runs the study model with the fits |
| `field_logs.py` | Field-log census (fault modes, clustering, multi-chip events, CE-before-failure); `--published` mode for the aggregates |

**Reading the retention file** [ESTIMATE: from the file itself].
- 28,657 rows. 1,596 rows have no module name and are dropped.
- 53% of non-zero rows are exact repeats: whole blocks of tests appear two or more times. Repeats do not move a mean, but they would fake precision. So every fit counts one test's worth of errors per condition, and every CI comes from resampling modules.
- At long intervals, exactly half the tests on a module show 0 errors and the other half show thousands. That is the classic signature of a data pattern and its inverse: only charged cells can leak. So the **mean over tests equals random data**, where half the cells are charged. This matches the model's `data_pattern_factor` = 0.5 (models/raw-ber-contract.py line 81).
- Bits per module = 2 GB × 8 = 1.718e10.
- Temperatures are ambient. The authors test at an ambient 20±1 °C unless stated, and call both 20 and 70 °C ambient [REPORTED: https://arxiv.org/pdf/1712.08304 and https://arxiv.org/pdf/1705.10292, via search snippets]. Chips may run a few °C warmer [UNVERIFIED]. That makes the 70 °C data a conservative stand-in for 65 °C. If the chips sat 10-20 °C above the 20 °C ambient and the 70 °C chips did not, Ea would be 0.17-0.23 eV instead of 0.13 eV [ESTIMATE].
- **Cross-check with the paper (C2).** The file's row-weighted mean at 70 °C and 2.048 s is 2,510 errors per test at 1.35 V and 2,641 at 1.15 V; at 20 °C it is 66 and 75. These equal the paper's reported average weak-cell counts [REPORTED: same two URLs, via search snippets]. So the file is the paper's data, and the authors average over all tests, zero tests included. This report weights each module equally instead. That gives a 35% higher BER at 70 °C, the safe direction [ESTIMATE].

**Fits** [ESTIMATE].
- **Tail.** Cell failure fraction F(t) = Φ((ln t − μ)/σ_ln), fitted by a Poisson likelihood over all seven intervals, including the zero counts. Done per module and on the fleet mean (each module weighted equally). 400 bootstrap resamples over modules.
- **Activation energy.** The time shift between 20 °C and 70 °C at equal BER. The 20 °C BER at 2.048 s is matched to the time at which the 70 °C curve reaches the same BER. Ea = k·ln(shift)/(1/T₂₀ − 1/T₇₀). A module with no errors at 20 °C gives only a lower bound.
- **Model re-run.** The script imports `models/raw-ber-contract.py` and swaps in the fitted tail. It replaces `lognormal_params` (lines 704-709) or `ber_ret` (lines 712-722). It then calls the model's own `p_max_interval` (lines 725-738) at the model's own code limits: `max_p_rs` (line 655), `max_p_rs_ondie` (line 963) and `max_p_hard` (line 335). It does this for the model's section 10.1 case table (lines 1057-1071) and for the three DDR4 layouts of its section 10.11 (`section_ddr4_geometry`, line 1383). That keeps the 2e-19 per-read target, VRT growth 1x/day, the 1 h scrub, the 0.5x DDR5 derate (line 140) and the energy arithmetic (`refresh_numbers`, line 741) unchanged.
- **Cases.**

| Case | Tail | 70 → 85 °C | Below 70 °C |
|---|---|---|---|
| A, optimistic | lognormal fit | fitted 0.13 eV | fitted 0.13 eV |
| **B, central** | lognormal fit | model 0.72 eV | fitted 0.13 eV |
| C, pessimistic | power law along the measured slope (k = 4.86), which bounds a lognormal from above | model 0.72 eV | fitted 0.13 eV |
| D | B, but the failing pattern is read as random data (2x BER) | model 0.72 eV | fitted 0.13 eV |
| E | B, but the single worst test is read as random data | model 0.72 eV | fitted 0.13 eV |
| Bound | the longest *measured* interval whose BER fits the code: no BER extrapolation | model 0.72 eV | none |

---

## 4. Results

### 4.1 Measured BER versus the model's tail (fleet mean, 1.35 V, random-data equivalent)

| Interval | 20 °C measured | 70 °C measured (CI) | 70 °C worst module | Model at 70 °C, lognormal | Model ÷ measured |
|---|---|---|---|---|---|
| 64-256 ms | 0 on 28 modules (<5.6e-12) | 0 on 28 modules (<6.2e-12) | 0 | 8.6e-12 to 9.2e-9 | at 256 ms: ~158 bits expected per test, 0 seen |
| 512 ms | 3.7e-13 | 1.9e-11 (5.5e-12 to 3.5e-11) | 1.6e-10 | 1.9e-7 | ~10,000x |
| 1.024 s | 1.1e-10 | 4.8e-9 (2.5e-9 to 7.4e-9) | 2.2e-8 | 2.9e-6 | 603x |
| 1.536 s | 8.6e-10 | 4.9e-8 (2.9e-8 to 7.6e-8) | 2.5e-7 | 1.2e-5 | 255x |
| 2.048 s | 2.9e-9 | 2.0e-7 (1.1e-7 to 3.2e-7) | 1.2e-6 | 3.3e-5 | 166x |

[ESTIMATE] Model values use its own temperature rule (x4 per 20 °C, so 85 → 70 °C is x2.83) and its anchors (BER 3.6e-9 at 64 ms and 1.1e-10 at 32 ms at 85 °C; lines 75-79). Even the model's *optimistic* "pow3" curve is 13x-68x above the data between 1 and 2 s.

### 4.2 Tail shape

| Quantity | Measured [ESTIMATE] | Model |
|---|---|---|
| σ_ln, fleet fit | **1.05** (CI 0.97-1.12) | 1.24 |
| σ_ln per module | median 1.00; 10th-90th percentile 0.78-1.19; range 0.73-1.25 | - |
| By vendor (median σ_ln) | A 1.18, B 0.82, C 1.10 | - |
| Local σ_ln between adjacent intervals | 0.78 (0.5-1 s), 0.98 (1-1.5 s), 1.08 (1.5-2 s) | - |
| Local slope d ln BER / d ln t at 2 s | 4.9 (lognormal); 4.86 (CI 4.51-5.27) between 1.5 and 2 s | ~5 at 64 ms, falling (model note, line 753) |
| Median retention at 70 °C (fit extrapolation, not a measured median) | 358 s | 232 s |

The fitted μ and median describe the tail's shape only. The data reaches at most F ≈ 2.5e-6 in one module, so the main body of the distribution is never seen.

C2 independent check [ESTIMATE]: a plain least-squares probit fit over the four non-zero intervals gives σ_ln 0.88. It weights the steep 0.5-1 s part. Re-run the same way, it gives 0.80 s (25x) for DDR5 at 85 °C, inside the range of cases C-E. The Poisson fit's 0.96 s comes out the same from separate code.

### 4.3 Temperature

| Quantity | Value [ESTIMATE] |
|---|---|
| Fleet Ea of the weakest cells (BER ~3e-9) | **0.13 eV** (CI 0.10-0.17); 0.11 eV matched at 1.536 s; 0.16 eV with the outlier-resistant estimator |
| Same, without module C4 (it holds 76% of the 20 °C errors) | 0.16 eV |
| Per-module point estimates (10 modules with errors at 20 °C) | 0.016-0.197 eV |
| Per-module lower bounds (18 modules with no errors at 20 °C) | ≥0.09 to ≥0.25 eV |
| Model's implied Ea | 0.72 eV (85-65 °C), 0.64 eV (65-45 °C) |

- **What it means.** For these weakest cells, 70 °C retention is only ~2x shorter than at 20 °C. This fits published device work: the extreme tail holds a low-Ea share, and that share shrinks toward the main distribution [REPORTED: Weber et al., https://tore.tuhh.de/entities/publication/d044c2f2-f544-42c7-8293-2985814bdad2 ; Hamamoto et al. 1998, https://next.sciencegate.app/document/10.1109/16.678551].
- **Which cells it describes (C2).** It is the Ea of the cells that fail first at 20 °C. Those are mostly low-Ea cells, because Ea is spread over cells [REPORTED: Hamamoto, same URL] and field-driven leakage (GIDL, gate-induced drain leakage) dominates the extreme tail [REPORTED: Weber, same URL]. The code limits sit near BER 1e-5, where higher-Ea cells take part. So the gain from cooling below 70 °C is unmeasured there, not shown to be small.
- **Main versus tail Ea.** The main distribution is never reached, so its Ea is NOT TESTABLE with this data.
- **Above 70 °C.** No data exists. Cases B-E use the model's 0.72 eV there, which is the more pessimistic choice.

### 4.4 VRT and test-to-test spread

- **No cell addresses and no timestamps** are in the file. So the VRT cell fraction and the VRT growth rate g cannot be measured.
- **Spread between repeated tests at one condition** (108 condition groups with ≥4 failing tests and median ≥50 errors) [ESTIMATE]:
  - median coefficient of variation 5%, 90th percentile 70%;
  - 18 groups (17%) differ by more than 3x between their highest and lowest test;
  - 6 of the 17 eligible modules have such a group (A1, A10, B1, B5, B8, C4); B1 and C4 reach 100-250x.
- **Cause.** The file does not record each test's data pattern, date or chip temperature. So this spread cannot be split into data-pattern dependence, VRT and setup changes. A 100x jump is most likely a pattern effect [ESTIMATE]. Treat it as a warning for the servo, not as a VRT measurement.

### 4.5 Spatial spread over banks (70 °C, 2.048 s)

- 28 modules. The busiest bank holds a median 13.9% of a module's errors (12.5% if even); the maximum is 18.7%.
- 11 of 28 modules fail a χ² evenness test at p < 0.001, counting one charged test. (C2 fix: the first version counted the mean over all tests, which halves every count because half the tests are zero, and reported 2 of 28.)
- **Reading.** Errors reach all 8 banks, with a modest but real imbalance between banks. Bank scale says nothing about clusters inside a codeword, which is what the codes care about. Those need bit addresses, which this file lacks.

### 4.6 Re-run of the model's safe interval

Chipkill kept (RS-8), 2e-19 per read, 1 h scrub, VRT 1x/day; "cut" = interval ÷ the part's own JEDEC window [ESTIMATE].

| Part / code | Model as published | A optimistic | **B central** (CI) | C pessimistic | D 2x pattern | E worst test | Bound, no BER extrapolation |
|---|---|---|---|---|---|---|---|
| DDR5, RS-8 behind SEC, 0.5x derate, 85 °C | 0.285 s (8.9x) | 2.23 s (70x) | **0.96 s (30x)**; CI 0.85-1.14 s | 0.89 s (28x) | 0.82 s (26x) | 0.80 s (25x) | ≥0.37 s (11.5x) |
| same, 70 °C | 0.81 s (25x) | 2.68 s (84x) | 2.68 s (84x); CI 2.37-3.16 s | 2.48 s (78x) | 2.28 s (71x) | 2.24 s (70x) | ≥1.02 s (32x) |
| same, 65 °C | 1.14 s (36x) | 2.85 s (89x) | 2.85 s (89x) | 2.65 s (83x) | 2.43 s (76x) | 2.39 s (75x) | ≥1.02 s (32x), from 70 °C data |
| same, 45 °C | 4.56 s | 3.77 s | 3.77 s | 3.50 s | 3.21 s | 3.16 s | - |
| DDR5, one chip dead, 85 °C | 0.092 s (2.9x) | 0.85 s (27x) | 0.37 s (11.5x) | 0.37 s | 0.32 s | 0.32 s | ≥0.18 s (5.7x) worst module |
| DDR4 (retired-DDR4 proxy), (b) two channels in lockstep, RS(144,128), 85 °C | 0.698 s (10.9x) | 5.29 s (83x) | **2.28 s (36x)**; CI 2.01-2.72 s | 2.05 s (32x) | 1.94 s (30x) | 1.90 s (30x) | ≥0.74 s (11.5x) |
| DDR4, (b) lockstep, 70 °C | 1.97 s (31x) | 6.36 s | 6.36 s (99x); CI 5.60-7.58 s | 5.72 s | 5.39 s | 5.30 s | ≥2.05 s (32x) |
| DDR4, (b) lockstep, one chip dead, 85 °C | 0.446 s (7.0x) | 3.62 s | 1.56 s (24x) | 1.49 s | 1.34 s | 1.31 s | ≥0.74 s (11.5x) |
| DDR4, (a) one channel, RS(72,64), 85 °C | 0.258 s (4.0x) | 2.28 s (36x) | **0.98 s (15x)**; CI 0.89-1.13 s | 0.98 s (15x) | 0.85 s (13x) | 0.84 s (13x) | ≥0.74 s (11.5x); worst module ≥0.55 s (8.6x) |
| DDR4, (a) one channel, 70 °C | 0.729 s (11x) | 2.74 s | 2.74 s (43x) | 2.73 s | 2.37 s | 2.34 s | ≥2.05 s (32x); worst module ≥1.54 s (24x) |
| DDR4, (a) one channel, one chip dead, 85 °C | 0.065 s (1.0x) | 0.71 s | 0.31 s (4.8x) | 0.28 s | 0.27 s | 0.27 s | ≥0.18 s (2.9x) |
| DDR4, (c) 640-bit line, −11.1% capacity, RS-8, 85 °C (the first version's "DDR4" row) | 0.837 s (13.1x) | 6.17 s (96x) | 2.66 s (42x); CI 2.32-3.20 s | 2.32 s (36x) | 2.25 s (35x) | 2.21 s (34x) | ≥0.74 s (11.5x) |
| DDR4, (c), 70 °C | 2.37 s (37x) | 7.41 s | 7.41 s (116x) | 6.45 s | 6.26 s | 6.15 s | ≥2.05 s (32x) |
| DDR4, (c), one chip dead, 85 °C | 0.258 s (4.0x) | 2.28 s | 0.98 s (15x) | 0.98 s | 0.85 s | 0.84 s | ≥0.55 s (8.6x) worst module |

DDR4 layouts (model section 10.11, corrected 2026-11-04): (a) one 72-bit channel, 512 data + 64 check bits per 64 B line, RS(72,64) over bytes; (b) two channels in lockstep, 1,024 + 128 bits per 128 B access, RS(144,128); (c) a 640-bit line with 128 check bits, which needs 64 more check bits per line stored in data space (−11.1% capacity). The first version of this table had only (c), labelled "DDR4".

**Refresh-energy cut, DDR5 at 85 °C against the 32 ms window** (refresh + scrub, the model's `refresh_numbers`) [ESTIMATE]:

| Case | Model | A | B | C | D | E |
|---|---|---|---|---|---|---|
| Cut | 8.9x | 67x | **29.5x** | 27x | 25x | 25x |

**Fleet view, case B** [ESTIMATE]: with a per-module servo, each module runs at its own interval and the fleet cut is 31x. One fixed interval for all 28 modules must suit the worst one (B7) and gives 18x.

**Per module, case B** (28 modules):

| Part, 85 °C | Worst module | 10th percentile | Median |
|---|---|---|---|
| DDR5 | 0.59 s (18x) | 0.81 s (25x) | 0.99 s (31x) |
| DDR4 (b) lockstep | 1.37 s (21x) | 1.91 s (30x) | 2.27 s (35x) |
| DDR4 (a) one channel | 0.68 s (11x) | 0.81 s (13x) | 1.13 s (18x) |
| DDR4 (c) 640-bit (first version's "DDR4") | 1.55 s (24x) | 2.20 s (34x) | 2.59 s (40x) |

The worst module is B7. Vendor B has the steepest tails (σ_ln 0.73-0.89) and the shortest intervals.

**How far the re-run extrapolates.**
- The highest fleet-mean BER measured is 2.0e-7; the highest single-module BER is 1.2e-6.
- The DDR5 code limit is 1.5e-5. The DDR4 limits are 3.0e-5 in lockstep (b), 8.3e-7 on one channel (a) and 5.4e-5 for the 640-bit layout (c).
- So cases A-E extrapolate 1.9 decades (DDR5), 2.2 decades (DDR4 lockstep), 0.6 decades (DDR4 one channel) and 2.4 decades (DDR4 layout c) in BER beyond the fleet mean.
- The tail bends the safe way over the measured range: its slope falls from 8.0 to 5.7 to 4.9. Case C holds the last slope fixed and still gives 0.89 s.
- A second, steeper population could appear beyond 2 s. Only the bound column is free of that risk.

### 4.7 VRT sensitivity (the growth rate g is not in the data), case B, 1 h scrub [ESTIMATE]

| VRT growth g | DDR5 85 °C | DDR5 70 °C | DDR4 85 °C, (b) lockstep / (a) one channel / (c) 640-bit |
|---|---|---|---|
| 1x/day (model default) | 0.96 s (30x) | 2.68 s | 2.28 / 0.98 / 2.66 s |
| 100x/day | 0.66 s (21x) | 1.83 s | 1.54 / 0.70 / 1.77 s |
| 700x/day (dossier kill line #4) | 0.45 s (14x) | 1.24 s | 1.03 / 0.50 / 1.18 s |

Even at the kill-line growth rate, the DDR5 case stays above the 6x GO line at 85 °C.

### 4.8 Field data: what public aggregates say

| Item | Value | Tag |
|---|---|---|
| Share of DDR4 field faults that hit several bits (corrected paper) | ~23% | [REPORTED] https://arxiv.org/pdf/2408.15302 |
| Same, original HPCA 2023 abstract (superseded by a decoding-bug corrigendum) | >45% | [REPORTED] https://ieeexplore.ieee.org/document/10071066 |
| Single-bit share of DRAM faults, Cielo/Hopper, vendors A/B/C | 64.6% / 69.5% / 58.4% | [REPORTED] https://sc.osti.gov/-/media/ascr/ascac/pdf/meetings/201512/ResilienceASCAC2015.pdf |
| Single-column share, same | 8.7% / 8.8% / 11.9% | [REPORTED] same |
| Jaguar: permanent faults; multi-bit (row, column, bank) faults | ≥70%; almost 50% of failures | [REPORTED] https://math.nist.gov/mcsd/Seminars/2015/2015-07-21-Diniz-presentation.pdf |
| Alibaba: in most DRAM-caused server failures, CEs appear only shortly before; for >40%, within 1 h | of 2,137 failures | [REPORTED] https://shujiehan.github.io/_pages/files/srds22.pdf (search snippet) |
| Huawei: UEs that CEs warn of first ("predictable") are the majority | qualitative | [REPORTED] https://arxiv.org/pdf/2406.05354 |
| Astra: faults even over socket, column and bank; uneven over node, rank and slot | qualitative | [REPORTED] https://www.osti.gov/biblio/2003151 |
| Google fleet: CE rate; DIMMs with errors per year | 25,000-70,000 FIT per Mbit; >8% of DIMMs | [REPORTED] https://research.google/pubs/dram-errors-in-the-wild-a-large-scale-field-study/ |
| M2-MFP (Huawei), Jan-May 2024, Purley: CE-logging DIMMs that failed in the month | 0.56% per month (CI 0.52-0.60%); ~3,600-4,100 CEs per CE-logging DIMM per month | [ESTIMATE] from [REPORTED] counts, https://github.com/hwcloud-RAS/M2-MFP |

FIT = failures per billion device-hours.

**Chance level of multi-chip events** [ESTIMATE]. Assume independent raw errors on a 10-chip x4 line, 64 bits per chip (`field_logs.py`, checked by Monte Carlo):

| Operating point | Errors on ≥2 chips (10 × 64 bits) | On ≥2 bytes of RS(80,64) (80 × 8 bits) | On ≥2 chips, DDR4 x4 line (18 × 32 bits) |
|---|---|---|---|
| 640-bit RS-8 at its limit (5.4e-5; DDR4 only in layout c) | 1.6% | 1.7% | 1.5% |
| 640-bit RS-8 servoed (limit ÷ 3) | 0.52% | 0.57% | 0.49% |
| 640-bit BCH-12 at its limit (3.3e-4; DDR4 only in layout c) | **9.3%** | **10.1%** | 8.8% |
| DDR5 behind on-die SEC, post-SEC events at the RS-8 limit | ~0.001% | - | - |

Real DDR4 layouts (corrected 2026-11-04; model section 10.11 limits):

| Operating point | Errors on ≥2 chips | Errors on ≥2 bytes |
|---|---|---|
| (a) one channel, RS(72,64) at its limit (8.3e-7), 18 × 32 bits | 0.022% | 0.023% |
| (a) one channel, servoed (limit ÷ 3) | 0.007% | - |
| (b) lockstep, RS(144,128) at its limit (3.0e-5), 36 × 32 bits | 1.7% | 1.7% |
| (b) lockstep, servoed (limit ÷ 3) | 0.56% | - |

The dossier's ">10% multi-chip events" line is almost reached by chance alone at the 640-bit BCH-12 operating point, and passed when counted by bytes. It should read ">10% *above the independent-error expectation*". On real DDR4 layouts with chipkill the chance level stays ≤1.7%.

---

## 5. Verdict per testable claim

| # | Claim (dossier / model) | Verdict | Evidence |
|---|---|---|---|
| 1 | Retention tail anchors: BER 3.6e-9 at 64 ms and 1.1e-10 at 32 ms (85 °C), lognormal (model lines 75-79, 704) | **CONTRADICTED** (too pessimistic, on DDR3L 2015-16) | 166-603x above measured at 1-2 s and 70 °C; ~158 bits per test expected at 256 ms, 0 seen on 28 modules |
| 2 | Tail width σ_ln ≈ 1.24 | **WEAKENED** (slightly) | 1.05 (CI 0.97-1.12); per module 0.73-1.25. A narrower tail rises faster, so this input alone errs on the optimistic side: holding the model's 64 ms anchor, σ_ln 1.05 cuts the DDR5 interval 0.25 → 0.18 s. The tail's position (row 1) more than offsets it |
| 3 | Retention x4 per 20 °C (Ea ≈ 0.64-0.72 eV) for the cooling bonus (65 °C, 45 °C) | **CONTRADICTED** at the measured BER (~3e-9, 20-70 °C); NOT TESTABLE at the code-limit BER (~1e-5) | Ea 0.13 eV (CI 0.10-0.17); 0.16 eV without C4; 18 of 28 modules give only lower bounds. 45 °C gives ~1.4x over 70 °C, not the model's ~5.7x. The model's 45 °C DDR5 interval (4.56 s) is above the data-based one (3.2-3.8 s) |
| 4 | Same rule from 70 to 85 °C | NOT TESTABLE WITH PUBLIC DATA | No data above 70 °C. The re-run uses the model's 0.72 eV there (pessimistic) |
| 5 | Tail versus main Ea | NOT TESTABLE WITH PUBLIC DATA | Main distribution not reached (max F ≈ 2.5e-6) |
| 6 | Kill #1: NO-GO if the RS-8 interval incl. VRT is <4x the window at 65 °C | **SUPPORTED** (not triggered) for DDR3-class cells; NOT TESTABLE for DDR5 | ≥32x measured at 70 °C with no BER extrapolation (≥24x for the worst module on one DDR4 channel); 84x DDR5 and 43-116x DDR4 by layout, modelled (case B, 70 °C) |
| 7 | GO: ≥6x at 85 °C and ≥24x at 65 °C | **SUPPORTED** for DDR3-class cells | 85 °C: ≥11.5x bound (≥8.6x worst module on one DDR4 channel), 25-30x cases B-E for DDR5, 30-36x DDR4 lockstep, 13-15x DDR4 one channel; 65 °C: ≥32x bound |
| 8 | **~9x refresh-energy cut on DDR5 RDIMMs at 85 °C** | **SUPPORTED as conservative for DDR3-class cells; NOT TESTABLE for DDR5** | Case B 29.5x (CI 0.85-1.14 s → 27-36x); fleet 31x with a per-module servo, 18x with one fixed interval; worst module 18x; bound 11.5x. The 0.5x DDR5 derate, the on-die SEC structure and VRT are untested |
| 9 | ~13x on retired DDR4 behind CXL | **CORRECTED** (2026-11-04): the ~13x gave DDR4 a 640-bit line with 128 check bits. The corrected model gives ~11x with two channels in lockstep and ~4x on one channel; 13x needs 11.1% of capacity spent on check bits. On retention, all three are **SUPPORTED** (conservative; DDR3L used as the proxy) | Case B: lockstep 2.28 s = 36x (30-32x pessimistic); one channel 0.98 s = 15x (13-15x pessimistic); 640-bit layout 2.66 s = 42x. Bound 11.5x for all three (one channel, worst module: 8.6x). Retired DDR4 is newer silicon than these DDR3L parts and, as in the model, gets no derate (section 10) |
| 10 | Degraded mode (one chip dead): 2.9x DDR5, 4.0x DDR4 at 85 °C | **SUPPORTED** (conservative) for DDR5. DDR4 corrected 2026-11-04: 7.0x in lockstep, none (1.0x) on one channel, 4.0x only in the 640-bit layout | DDR5 11.5x (case B), worst-module bound 5.7x. DDR4 case B: lockstep 24x (bound 11.5x), one channel 4.8x (bound 2.9x), 640-bit 15x (worst-module bound 8.6x) |
| 11 | VRT growth ≤700x/day (kill #4); VRT pairs within 2x of chance | NOT TESTABLE WITH PUBLIC DATA | No addresses or timestamps. Even at 700x/day, case B keeps DDR5 at 14x |
| 12 | Kill #2: BCH dies if >0.4% of error bits sit in ≥3-bit clusters; both codes die if >10% of events span >1 byte | NOT TESTABLE WITH PUBLIC DATA | No bit addresses. Banks show a modest imbalance (11 of 28 modules uneven at p < 0.001; busiest bank ≤18.7%). Bank scale says nothing about codeword clusters |
| 13 | Multi-chip events ≤10% (GO line) | NOT TESTABLE WITH PUBLIC DATA | Field logs run at normal refresh, and the only chip-level logs (SmartMem) are gated. Chance alone gives 0.5-1.6% with RS-8 and 9.3% at the BCH-12 limit (10.1% counted by bytes), so the line needs a chance-corrected definition |
| 14 | Chipkill must be the default (RT-CIRC-03) | **SUPPORTED** | 30-42% of field faults are not single-bit; ~23% of DDR4 faults are multi-bit; column faults are 9-12% |
| 15 | First-read chip marking works because faults show CEs before UEs (kill #10, model §10.6) | **SUPPORTED** (weakly) | Predictable UEs (CEs first) are the majority. Warnings are short: in >40% of DRAM-caused failures, CEs first appear <1 h before. So marking must happen on the first chip-confined correction. Field data are at standard refresh, and the share of "sudden" UEs (no CE first) is not public |
| 16 | The servo's 1 h grade holds for 1,000 h on ≥95% of modules | NOT TESTABLE WITH PUBLIC DATA | No timestamps. Warning: 6 of 17 modules show >3x spread between repeated tests at one condition, larger than the 3x guard; the cause is unresolved |
| 17 | UE budget basis: field DIMM UE rates ~0.2-1% per year (model line 49) | NOT TESTABLE WITH PUBLIC DATA | M2-MFP gives 0.56% per month of *CE-logging* DIMMs failing; the fleet denominator is not published |
| 18 | Row hammer at relaxed refresh (kill #5) | NOT TESTABLE WITH PUBLIC DATA | No public data at relaxed refresh |

---

## 6. What it means for the ~9x claim

- **The ~9x comes from the model's assumed tail, not from data.** The anchors trace back to RAIDR-era cell counts with a 4x temperature derate (model lines 75-79).
- **Real 2015-16 DDR3L modules have far fewer weak cells.** Their tail sits 2-3 orders of magnitude lower at 1-2 s. Its width is similar.
- **Re-run with the real tail, DDR5's interval moves from 0.285 s to ~0.8-1.0 s at 85 °C.** That keeps every other model input, including the model's own 0.5x DDR5 derate and its 0.72 eV above 70 °C. The energy cut moves from 8.9x to ~25-30x. The worst module still gives 18x, and the no-extrapolation bound gives ≥11.5x.
- **So the claim is safe on DDR3-class silicon.** Four things keep it from being proven for DDR5:
  1. **The part is old.** DDR3L 4Gb (2015-16) is not DDR5 1a/1b 16Gb. The 0.5x derate is a guess (model line 140) that no public data tests. If DDR5's true derate were 0.15x instead of 0.5x, case B would fall back to about the 9x headline [ESTIMATE: interval scales with the derate].
  2. **On-die SEC changes the error structure.** The model says it turns doublets into 3-bit events (§2.4). No public chip data exists; EINSim's real-chip data is confidential.
  3. **VRT growth is unmeasured.** At 700x/day the DDR5 case falls to 14x.
  4. **The sample is small.** It is 31 modules from one study, while the dossier wants ≥30 lots per vendor.
- **The cooling bonus is unproven, and probably overstated.** At the measured BER the weakest cells have Ea ~0.13-0.16 eV, so a temperature-tracking controller may gain little below 70 °C. At the operating BER it is unmeasured. The 65 °C GO line still passes, because the whole tail sits so much further right. But the dossier's 45 °C figures (x16, e.g. 13-24 s in §2.5) should not be used.
- **Recommendation.** Keep ~9x as the planning number. Public DDR3L data suggests the true value could be ~3x higher. Drop the x16 45 °C multiplier from any headline. Redefine the multi-chip kill line against the independent-error expectation.

---

## 7. What data would settle the rest

| Open question | Who can answer it | What to run |
|---|---|---|
| Bit-level clusters in codewords (kill #2); VRT fraction and growth g (kill #4); Ea of the *same* cells at 25/45/65 °C (not fleet means) | **Home-lab E6** ([../../home-lab/E6_retention_tail_real_dram.md](../../home-lab/E6_retention_tail_real_dram.md)) | Log every failing address on a 64 Mbit SDRAM at 64 ms-65 s and 25/45/65 °C, with repeat maps every 20 s-20 min for VRT. Going out to 16-65 s reaches BER 1e-5-1e-4 *directly*, removing this report's 2-decade extrapolation (for that chip). Feed the address logs to `field_logs.py`-style census code and to E6's `retention_map.py analyze`. It cannot answer the DDR5 questions |
| DDR5 derate, post-SEC event structure, ECS (error check and scrub) counts, chipkill-safe interval on 1a/1b RDIMMs | **Dossier Phase 1, DDR5 leg** (§5.R step 3; ~$124k Phase 1 total, ~$20k for the two open testers [ESTIMATE: dossier]) | ≥24 RDIMMs on the open Antmicro DDR5 testers; BEER-style H-matrix recovery (https://github.com/CMU-SAFARI/BEER) |
| Lot-to-lot spread; ≥30 lots per vendor; 1 h grade vs 1,000 h hold | Dossier Phase 1 steps 1 and 6 | 150 DDR4 modules screened, 60 deep-mapped, 20 soaked 1,000 h |
| Multi-chip event share in the field; CE-before-UE share; DQ x beat patterns | SmartMem / M2-MFP (register on Codabench) or the Alibaba set (Tianchi) | `python3 -I research/realdata/field_logs.py --log <log files> --tickets <tickets>` (SmartMem: pass the per-DIMM files; each takes its serial from its file name). Do not commit SmartMem data: its rules forbid redistribution and allow non-commercial use only, so a company decision probably needs an academic partner or Huawei's permission [UNVERIFIED: not legal advice] |
| VRT over months on DDR3 | Khan et al. 2014 full data (host blocked here) | Allow www.ece.cmu.edu, fetch it, and extend `retention_fit.py` if it holds per-cell lists |
| Behaviour above 70 °C | E6 cannot go there (chip rated ~70 °C); Phase 1 thermal rigs can | Map at 85 °C directly; drop the 0.72 eV assumption |

**How to reproduce this report.**

```bash
python3 -I research/realdata/fetch_data.py --dest ~/dram-realdata
python3 -I research/realdata/retention_fit.py --csv ~/dram-realdata/safari_ddr3l_retention/retention_time_profile.csv
python3 -I research/realdata/field_logs.py --published
python3 -I research/realdata/retention_fit.py --selftest && python3 -I research/realdata/field_logs.py --selftest && python3 -I research/realdata/fetch_data.py --selftest
```

Outputs: `retention_fit_summary.json` (all numbers above), `retention_per_dimm.csv` (per-module fits and intervals), `field_published_summary.json`.

---

## 8. Limits of this report

- **One retention dataset, from one lab, on one old DDR3L generation.** All retention verdicts are for DDR3-class cells.
- **Assumptions about the file.** The file does not say which data pattern each test used, or whether the whole module was tested. "Mean over tests = random data" rests on the 50% zero-test pattern [ESTIMATE]. If only part of each module was tested, every BER here is too low by that fraction [UNVERIFIED].
- **The 20 °C data is odd.** Some modules (A1, B5) show almost no temperature dependence. That could be real (field-enhanced leakage) or a labeling or setup issue [UNVERIFIED].
- **The field verdicts rest on published aggregates read through search snippets,** not on raw logs.
- **DDR4 line geometry (C2; resolved 2026-11-04, section 10).** The model's DDR4 cases used the DDR5 line: 640 bits with 128 check bits (RS(80,64)). A DDR4 x4 ECC RDIMM moves 18 chips × 32 bits per 64-byte line, with 64 check bits [REPORTED: section 10]. The model now has three DDR4 layouts, and this report uses all three.
- **Licences (C2).** The committed files hold statistics derived from the SAFARI file (fits, fleet means, per-module means at three conditions), with attribution, and no raw rows. The five M2-MFP monthly rows in `field_logs.py` are quoted from a CC BY-NC-SA 4.0 README with attribution; recheck that use if this work turns commercial [UNVERIFIED: not legal advice].
- **Network.** Many hosts were blocked in this session (listed below). The SmartMem dataset and terms pages were read from the site's source repository on github.com because its github.io site was blocked. No data was fetched that way. Task C2 read the same repository (commit 76988b9) the same way, and tried research.nvidia.com once for the paper; it did not resolve and was not retried.

**Blocked hosts in this session:** zenodo.org, courses.grainger.illinois.edu, people.inf.ethz.ch, users.ece.cmu.edu, www.ece.cmu.edu, hwcloud-ras.github.io, hyxie2023.github.io, github.com web pages and API (git clone and raw.githubusercontent.com worked), tianchi.aliyun.com, www.usenix.org, www.osti.gov, safari.ethz.ch, people.cs.rutgers.edu, www.pdl.cmu.edu, www.research-collection.ethz.ch, figshare.com, dataverse.harvard.edu, www.kaggle.com, huggingface.co, ar5iv.labs.arxiv.org, www.semanticscholar.org, api.semanticscholar.org, dl.acm.org, export.arxiv.org, doi.org, www.sandia.gov, ieee-dataport.org, data.mendeley.com, osf.io, research.nvidia.com (C2). Hosts blocked in earlier sessions (arxiv.org, ieeexplore.ieee.org and others) were not retried.

---

## 9. Review by task C2 (2026-11-04)

An adversarial statistics and device-physics review. All three scripts and their `--selftest` were re-run; the retention outputs were reproduced byte for byte before the fixes below.

| What was checked | Result |
|---|---|
| Data file | Hash and pinned commit match; no licence file in the repository; README confirms 31 DDR3L SO-DIMMs from 2015-16 and points the file to the paper's section 4.6. Row-weighted means equal the paper's averages (section 3) |
| Key numbers re-derived with separate code | σ_ln, Ea, the 0.96 s DDR5 interval, 166-10,000x model excess and the bound: all reproduced. A plain probit fit gives 0.80 s (section 4.2) |
| Standard-refresh field logs used as relaxed-refresh evidence | Not found. Field data is used only for hard-fault shares and warning time, both independent of refresh rate |
| Selection bias | Fleet Ea is driven by the 10 modules with 20 °C errors, C4 most (fixed in text). M2-MFP denominators are CE-logging DIMMs (already flagged). Field fault shares are shares of faulty DIMMs, used only to argue for chipkill |
| Event definitions | Kill #2 counts bytes; the chance level is now given both ways. `field_logs.py` now counts a chip as (rank, device) and adds a DIMM-level share, because events cluster in a few DIMMs |
| Independence in ECC math | Untestable here (no addresses). Bank χ² was understated by half (fixed: 11 of 28 uneven, not 2) |
| Units, temperatures | Bits and BER definitions consistent. Temperatures are ambient [REPORTED]; sensitivity added |
| Licences, raw data in the repository | No raw rows anywhere in the repository. SmartMem is non-commercial only (added). Tianchi licence and the Zenodo record could not be confirmed (tagged) |

**Fixes made.** `retention_fit.py`: bank χ² on one charged test; new outputs for Ea without the dominant module, the BER at which Ea is matched, the local tail width and the fleet energy cut. `field_logs.py`: SmartMem per-DIMM files take their serial from the file name (before, failures could never match their logs); several `--log` files; chip = (rank, device); DIMM-level multi-chip share; chance level by bytes and for the DDR4 x4 line. This report: verdicts 2, 3, 12, 13 and 15 reworded; finding 3 scoped to the measured BER.

**Verdicts not changed.** The ~9x claim stays SUPPORTED as conservative for DDR3-class cells and NOT TESTABLE for DDR5.


---

## 10. Correction: DDR4 line geometry (2026-11-04)

**What was wrong.** The model's DDR4 ("retired DDR4") cases used the DDR5 RDIMM line: 640 bits = 512 data + 128 check bits, decoded as RS(80,64) with an x4 chip worth 8 bytes. A DDR4 ECC RDIMM has a 72-bit bus (64 data + 8 ECC bits) and a burst of 8, so a 64 B line carries 512 data + 64 check bits (12.5%), and an x4 chip gives 32 bits (4 bytes) [REPORTED: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11437114 and a Micron DDR4 RDIMM datasheet, https://dtsheet.com/model/4467123, via search snippets]. x4 chipkill on DDR4 is done either on one channel with a single-symbol code (8-bit symbols, 16 data + 2 check symbols per codeword, four codewords per line) [REPORTED: https://arxiv.org/pdf/1908.01806, via search snippet], or with two channels in lockstep: a 144-bit word of 128 data + 16 check bits per beat over 36 x4 chips [REPORTED: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9772900 and arXiv 1908.01806, via search snippets]. The DDR5 geometry is right: two 40-bit sub-channels of 32 data + 8 ECC bits, burst 16, 10 x4 chips per sub-channel [REPORTED: https://www.rambus.com/memory-interface-chips/ddr5-dimm-chipset/ddr5-rcd/, via search snippet]. Nothing in the dossier or the red-team responses said the DDR4 design trades capacity for check bits; the dossier said the opposite ("no new storage"). So it was an error, not a design choice.

**What changed.** The model gained section 10.11 with three DDR4 layouts. `retention_fit.py` now re-runs all three (the old "DDR4" case is kept as layout c). `field_logs.py` adds the chance levels for layouts a and b. The DDR5 numbers did not move.

| DDR4 number, 85 °C unless stated | First version | (b) two channels in lockstep, RS(144,128) | (a) one channel, RS(72,64) | (c) 640-bit, −11.1% capacity |
|---|---|---|---|---|
| Code limit (max raw BER) | 5.4e-5 | 3.0e-5 | 8.3e-7 | 5.4e-5 (same) |
| Model, central | 0.837 s (13.1x) | 0.698 s (10.9x) | 0.258 s (4.0x) | same |
| Model, one chip dead | 0.258 s (4.0x) | 0.446 s (7.0x) | 0.065 s (1.0x: none) | same |
| Real tail, case B | 2.66 s (42x) | 2.28 s (36x) | 0.98 s (15x) | same |
| Real tail, cases C-E | 34-36x | 30-32x | 13-15x | same |
| Real tail, one chip dead, case B | 0.98 s (15x) | 1.56 s (24x) | 0.31 s (4.8x) | same |
| Bound, no BER extrapolation | ≥0.74 s (11.5x) | ≥0.74 s (11.5x) | ≥0.74 s (11.5x); worst module ≥0.55 s (8.6x) | same |
| Per module, worst / median (case B) | 24x / 40x | 21x / 35x | 11x / 18x | same |
| Fleet-mean BER margin below the limit at 70 °C, 2.048 s | 276x (worst module 44x) | 153x (24x) | 4.2x (worst module over the limit; passes at 1.536 s) | same |

**Verdicts changed.** Verdict 9 (~13x on retired DDR4) is now CORRECTED: ~11x in lockstep and ~4x on one channel in the model, and 15-36x with the measured tail. Verdict 10 (degraded mode) is corrected for DDR4. Verdicts 6 and 7 gain the one-channel worst-module bounds (24x at 70 °C, 8.6x at 85 °C), which still pass kill #1 and the 85 °C GO line. The ~9x DDR5 verdict is unchanged.

---

## Sources

**Data and code**
- https://github.com/CMU-SAFARI/DRAM-Voltage-Study (dataset 1; commit b2089c3c7c2aac1d0936b4cfc572a675f5fd73f4)
- https://raw.githubusercontent.com/CMU-SAFARI/DRAM-Voltage-Study/b2089c3c7c2aac1d0936b4cfc572a675f5fd73f4/characterization_results/retention_time_profile.csv
- https://arxiv.org/abs/1705.10292 (Chang et al., SIGMETRICS 2017: 124 DDR3L chips, 31 modules, 4Gb chips, 2 GB modules; 2,510 and 2,641 average weak cells at 70 °C and 2.048 s; via search snippets)
- https://arxiv.org/pdf/1712.08304 (Chang, PhD thesis: tests at an ambient 20±1 °C; 66 and 75 weak cells at 20 °C and 2.048 s; via search snippet)
- https://github.com/alibaba-edu/dcbrain/tree/master/dramdata
- https://tianchi.aliyun.com/dataset/132973
- https://github.com/zncheng/dramanalysis
- https://github.com/hwcloud-RAS/SmartMem.github.io (dataset and terms pages; commit 76988b92bb6a6afc095d7334651099b125f9f180)
- https://www.codabench.org/competitions/3586/
- https://github.com/hwcloud-RAS/M2-MFP
- https://doi.org/10.5281/zenodo.6515019
- http://www.ece.cmu.edu/~safari/tools/dram-sigmetrics2014-fulldata.html
- https://www.pdl.cmu.edu/ftp/NVM/khan-efficacy-sigmetrics2014.pdf
- https://github.com/CMU-SAFARI/EINSim (and tag full-size-dataset-v1.0, README "Running the examples")
- https://github.com/CMU-SAFARI/BEER
- https://github.com/CMU-SAFARI/HARP
- https://github.com/CMU-SAFARI/SoftMC
- https://github.com/CMU-SAFARI/DRAM-Bender

**Field studies**
- https://arxiv.org/pdf/2408.15302 (Beigi et al., corrigendum: ~23% multi-bit)
- https://ieeexplore.ieee.org/document/10071066 (Beigi et al., HPCA 2023)
- https://sc.osti.gov/-/media/ascr/ascac/pdf/meetings/201512/ResilienceASCAC2015.pdf (Sridharan, fault-mode shares)
- https://pages.cs.wisc.edu/~remzi/Classes/739/Web/Papers/memoryerrors-asplos15.pdf (Sridharan et al., ASPLOS 2015)
- https://math.nist.gov/mcsd/Seminars/2015/2015-07-21-Diniz-presentation.pdf (Jaguar summary)
- https://sc12.supercomputing.org/schedule/event_detail.php-evid=pap113.html (Sridharan and Liberty, SC12)
- https://shujiehan.github.io/_pages/files/srds22.pdf (Cheng et al., SRDS 2022)
- https://www.osti.gov/biblio/2003151 (Ferreira et al., Astra, HPDC 2022)
- https://www.sandia.gov/research/publications/details/understanding-memory-failures-on-a-petascale-arm-system-2022-06-27/ (Astra paper page; data "will be made publicly available")
- https://arxiv.org/pdf/2406.05354 (Yu et al., DSN 2024)
- https://arxiv.org/pdf/2312.02855 (Yu et al., error bits)
- https://sc22.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap137.html (Li et al., SC22)
- https://research.google/pubs/dram-errors-in-the-wild-a-large-scale-field-study/ (Schroeder et al., 2009)

**Retention physics**
- https://next.sciencegate.app/document/10.1109/16.678551 (Hamamoto et al., 1998)
- https://www.bohrium.com/paper-details/on-the-retention-time-distribution-of-dynamic-random-access-memory-dram/812461776217047041-3976 (Hamamoto abstract: the deep level's Ea is normally distributed among cells)
- https://tore.tuhh.de/entities/publication/d044c2f2-f544-42c7-8293-2985814bdad2 (Weber et al., tail activation energies)
- https://arxiv.org/pdf/2306.16037 (Liu et al. ISCA 2013, retrospective)
- https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_paper.pdf (Patel et al., REAPER)
- https://fast.cc.gatech.edu/papers/DSN_2015_1.pdf (Qureshi et al., AVATAR)
- https://www.pdl.cmu.edu/ftp/NVM/raidr-isca12.pdf (RAIDR, the source of the model's anchors)

**DDR4 and DDR5 line geometry (section 10; all via search snippets)**
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11437114 (DDR4 DIMM bus: 72 bits = 64 data + 8 ECC)
- https://dtsheet.com/model/4467123 (Micron DDR4 RDIMM datasheet: burst length 8)
- https://arxiv.org/pdf/1908.01806 (x4 chipkill codes: 144-bit lockstep SSC-DSD; AMD 2013 8-bit-symbol SSC on a 72-bit bus, 18 chips)
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9772900 (lockstep chipkill word: 36 x4 symbols, 128 data + 16 ECC bits; halves parallelism, doubles prefetch energy at burst 8)
- https://www.rambus.com/memory-interface-chips/ddr5-dimm-chipset/ddr5-rcd/ (DDR5 RDIMM: two 40-bit sub-channels, 10 x4 devices each)
- https://www.intel.com/content/www/us/en/developer/articles/technical/new-reliability-availability-and-serviceability-ras-features-in-the-intel-xeon-processor.html (Intel ADDDC: a failing device is mapped out into virtual lockstep)

**Study files used**
- ../../dossiers/raw-ber-contract.md (§2.4, §2.5, §5.R, §9, §11)
- ../../models/raw-ber-contract.py (lines 49, 75-82, 140, 335, 655, 704-746, 963, 1057-1071, 1383 onward)
- ../../home-lab/E6_retention_tail_real_dram.md
