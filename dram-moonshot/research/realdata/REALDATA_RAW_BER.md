# The FASTEST PROOF on real public data: raw-ber-contract

*Task C1. As of 2026-11-04. Scripts and derived numbers are in this folder. Raw data stays outside the repository; `fetch_data.py` re-downloads it.*

**Evidence tags.** [DATASHEET] = a part's datasheet. [REPORTED] = a paper, press or official page, with its URL. [ESTIMATE] = arithmetic in this folder's scripts on real data, or the study's own model. [UNVERIFIED] = not checked.

**Acronyms.** DRAM: dynamic random-access memory. BER: bit error rate. ECC: error-correcting code. RS-8: the Reed-Solomon byte code the dossier uses, which keeps chipkill (it survives one dead chip). BCH-12: a binary code that does not keep chipkill. SEC: the single-error-correcting code inside each DDR5 chip (on-die ECC). VRT: variable retention time, when a cell's retention time jumps between values. Ea: activation energy, which sets how fast leakage grows with temperature. CE / UE: correctable / uncorrectable error. CI: 95% confidence interval. DIMM: memory module.

---

## 1. The answer in one page

**What could be tested.** Only one public raw dataset was both reachable and on topic: CMU SAFARI's retention measurements of 31 DDR3L modules from 2015-16, at 20 and 70 °C, with refresh paused for 64 ms to 2.048 s. No public field log with chip-level fields could be downloaded here. No public DDR4 or DDR5 retention data, and no public on-die-ECC chip data, were found.

**Main findings** [ESTIMATE unless tagged]:

1. **The model's retention tail is far too pessimistic for these parts.** At 70 °C the model expects 166x to 10,000x more failing bits than were measured between 0.5 and 2 s. At 256 ms it expects ~158 failing bits per module per test. All 28 modules measured at 70 °C showed 0.
2. **The tail's shape is close to the model's; its position is not.** The fitted lognormal width σ_ln (the spread of log retention time) is 1.05 (CI 0.97-1.12). The model uses 1.24. Per module it ranges 0.73-1.25.
3. **The weakest cells barely speed up with heat.** Between 20 and 70 °C their retention time shrinks only ~2x. That is Ea = 0.13 eV (CI 0.10-0.17). The model assumes ~0.72 eV ("x4 per 20 °C"). So cooling a module buys much less than the model says: 45 °C gives ~1.4x over 70 °C, not the model's ~5.7x.
4. **Re-running the model with the measured tail lengthens the safe interval about 3x.** DDR5 case, chipkill kept, 85 °C, with the model's own 0.5x DDR5 derate and its 0.72 eV above 70 °C: **0.96 s (CI 0.85-1.14 s), i.e. 30x the 32 ms window**. The model says 0.285 s (8.9x). Three pessimistic variants give 0.80-0.89 s (25-28x). The worst single module gives 0.59 s (18x). A bound that needs no extrapolation in BER gives at least 0.37 s (11.5x).
5. **Kill line at 65 °C: not triggered on these parts.** The data is taken at 70 °C, which is hotter than 65 °C, so it is a conservative check. At 2.048 s the fleet-mean BER sits 276x below the DDR4 chipkill limit, and the worst module 44x below. For the DDR5 case (0.5x derate, so the same cells at 1.024 s) the margins are 77x and 12x. That is ≥32x the window with no BER extrapolation, against a NO-GO line of <4x.
6. **Field data.** Public field studies show that 30-42% of DRAM faults are not single-bit, and ~23% of DDR4 faults hit several bits [REPORTED]. That supports keeping chipkill. Over 40% of DRAM-caused server failures show CEs within the hour before [REPORTED]. That supports the "mark the chip on its first correction" rule. The multi-chip kill line (>10% of events) cannot be tested with public data.
7. **A flaw found in the kill line.** If errors are independent, chance alone puts 0.5-1.6% of events on two chips with RS-8. At the BCH-12 limit it is 9.3%, close to the 10% NO-GO line. The census must compare against this chance level.

**Verdict on the ~9x claim.** Public data does not contradict it. For DDR3-class cells it looks conservative by about 3x (25-30x instead of 9x). It is **not testable for DDR5 with public data**. The DDR5 number rests on three untested inputs: the 0.5x retention derate, the on-die SEC error structure and VRT growth. Keep ~9x as the planning number. Treat ~25-30x as upside that only the Phase 1 DDR5 leg can confirm.

---

## 2. Datasets found

| # | Name | Source URL | License | Size | What it has | Used? |
|---|---|---|---|---|---|---|
| 1 | SAFARI DRAM-Voltage-Study, `retention_time_profile.csv` | https://github.com/CMU-SAFARI/DRAM-Voltage-Study | No license file in the repo, so all rights are reserved by default [REPORTED: repo tree, commit b2089c3] | 1,539,105 bytes, 28,657 rows | 31 DDR3L SO-DIMMs (10 vendor A, 12 B, 9 C); 2 GB each, 4 x 4Gb chips [REPORTED: https://arxiv.org/abs/1705.10292, via search snippet]; 20 and 70 °C ambient; 1.15/1.2/1.35 V; refresh paused 64-2048 ms; bit-error counts per bank per test | **Yes.** Raw file kept out of git; only fits and fleet means are committed |
| 2 | Same repo, `dimm_faulty_cachelines_out.csv` | same | same | 3,848 bytes | Voltage-induced errors, not retention | No (off topic) |
| 3 | Alibaba SRDS'22 DRAM error logs (`dramdata`) | https://github.com/alibaba-edu/dcbrain/tree/master/dramdata ; data at https://tianchi.aliyun.com/dataset/132973 | CC BY-SA 4.0 [REPORTED: Tianchi page via search snippet] | ~410 MB zip [REPORTED] | >70M CEs from >250K servers and 3M DIMMs over 8 months. Fields: server, DIMM, rank, bank, row, column, error type, time. Trouble tickets with UE/CE-driven failure type and time. **No chip (device) field** [REPORTED: readme] | No. Tianchi was blocked from this session and needs a login; it is also above the 200 MB budget. `field_logs.py` reads it as is |
| 4 | Huawei SmartMem (WWW 2025 competition) | https://www.codabench.org/competitions/3586/ ; site source https://github.com/hwcloud-RAS/SmartMem.github.io | CC BY-NC 4.0 under competition rules that forbid redistribution [REPORTED: the site's terms page] | Not stated | Per-DIMM mcelog with 23 columns, **including deviceid (chip), bank group, bank, row, column and a DQ x beat error bitmap**; DIMM failure tickets [REPORTED: the site's dataset page] | No. Needs Codabench registration; cannot be shared. The best public source for the multi-chip question |
| 5 | Huawei M2-MFP repository | https://github.com/hwcloud-RAS/M2-MFP | CC BY-NC-SA 4.0 [REPORTED: README] | README and code only; data "will be provided in future updates" | Monthly counts: DIMMs with CEs, failed DIMMs, CE totals (Jan-Jul 2024, Intel Purley and Cascade) | Aggregates only (section 4.8) |
| 6 | Sandia Astra memory error and system monitoring data | https://doi.org/10.5281/zenodo.6515019 [REPORTED: cited in a later paper, via search snippet] | Not verified [UNVERIFIED] | Not verified | CE records plus power and temperature for a petascale Arm system [REPORTED: https://www.osti.gov/biblio/2003151] | No. zenodo.org was blocked |
| 7 | Khan et al. SIGMETRICS 2014 "full data sets" (retention, VRT) | http://www.ece.cmu.edu/~safari/tools/dram-sigmetrics2014-fulldata.html [REPORTED: search snippet] | Not verified | Not verified | Retention-failure data from the VRT study [UNVERIFIED: contents] | No. Host blocked. **The most valuable missing set for VRT** |
| 8 | EINSim (on-die ECC simulator) | https://github.com/CMU-SAFARI/EINSim | MIT [REPORTED: README] | Small | Simulator. The README says the real-chip experimental data was **withheld for confidentiality**; only simulated "proxy" data ships [REPORTED] | No (no chip data) |
| 9 | BEER, HARP (on-die ECC tools) | https://github.com/CMU-SAFARI/BEER , https://github.com/CMU-SAFARI/HARP | MIT [REPORTED: READMEs] | Small | Tools that recover or work around on-die ECC; simulated errors | No (tools, not data). Useful for Phase 1 |
| 10 | SoftMC, DRAM Bender (test platforms) | https://github.com/CMU-SAFARI/SoftMC , https://github.com/CMU-SAFARI/DRAM-Bender | Not checked | - | Retention-test programs, no result data | No. These are the Phase 1 tools |
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
- At long intervals, exactly half the tests on a module show 0 errors and the other half show thousands. That is the classic signature of a data pattern and its inverse: only charged cells can leak. So the **mean over tests equals random data**, where half the cells are charged. This matches the model's `data_pattern_factor` = 0.5 (models/raw-ber-contract.py line 79).
- Bits per module = 2 GB × 8 = 1.718e10.
- Temperatures are the reported ambient values; chips may run a few °C warmer [UNVERIFIED]. That makes the 70 °C data a conservative stand-in for 65 °C.

**Fits** [ESTIMATE].
- **Tail.** Cell failure fraction F(t) = Φ((ln t − μ)/σ_ln), fitted by a Poisson likelihood over all seven intervals, including the zero counts. Done per module and on the fleet mean (each module weighted equally). 400 bootstrap resamples over modules.
- **Activation energy.** The time shift between 20 °C and 70 °C at equal BER. The 20 °C BER at 2.048 s is matched to the time at which the 70 °C curve reaches the same BER. Ea = k·ln(shift)/(1/T₂₀ − 1/T₇₀). A module with no errors at 20 °C gives only a lower bound.
- **Model re-run.** The script imports `models/raw-ber-contract.py` and swaps in the fitted tail. It replaces `lognormal_params` (lines 664-669) or `ber_ret` (lines 672-682). It then calls the model's own `p_max_interval` (lines 685-698) at the model's own code limits: `max_p_rs` (line 615), `max_p_rs_ondie` (line 917) and `max_p_hard` (line 296). It does this for the model's section 10.1 case table (lines 1007-1021). That keeps the 2e-19 per-read target, VRT growth 1x/day, the 1 h scrub, the 0.5x DDR5 derate (line 138) and the energy arithmetic (`refresh_numbers`, line 701) unchanged.
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

[ESTIMATE] Model values use its own temperature rule (x4 per 20 °C, so 85 → 70 °C is x2.83) and its anchors (BER 3.6e-9 at 64 ms and 1.1e-10 at 32 ms at 85 °C; lines 73-77). Even the model's *optimistic* "pow3" curve is 13x-68x above the data between 1 and 2 s.

### 4.2 Tail shape

| Quantity | Measured [ESTIMATE] | Model |
|---|---|---|
| σ_ln, fleet fit | **1.05** (CI 0.97-1.12) | 1.24 |
| σ_ln per module | median 1.00; 10th-90th percentile 0.78-1.19; range 0.73-1.25 | - |
| By vendor (median σ_ln) | A 1.18, B 0.82, C 1.10 | - |
| Local slope d ln BER / d ln t at 2 s | 4.9 (lognormal); 4.86 (CI 4.51-5.27) between 1.5 and 2 s | ~5 at 64 ms, falling (model note, line 713) |
| Median retention at 70 °C (fit extrapolation, not a measured median) | 358 s | 232 s |

The fitted μ and median describe the tail's shape only. The data reaches at most F ≈ 2.5e-6 in one module, so the main body of the distribution is never seen.

### 4.3 Temperature

| Quantity | Value [ESTIMATE] |
|---|---|
| Fleet Ea of the weakest cells (BER ~3e-9) | **0.13 eV** (CI 0.10-0.17); 0.11 eV matched at 1.536 s; 0.16 eV with the outlier-resistant estimator |
| Per-module point estimates (10 modules with errors at 20 °C) | 0.016-0.197 eV |
| Per-module lower bounds (18 modules with no errors at 20 °C) | ≥0.09 to ≥0.25 eV |
| Model's implied Ea | 0.72 eV (85-65 °C), 0.64 eV (65-45 °C) |

- **What it means.** For these weakest cells, 70 °C retention is only ~2x shorter than at 20 °C. This fits published device work: the extreme tail holds a low-Ea share, and that share shrinks toward the main distribution [REPORTED: Weber et al., https://tore.tuhh.de/entities/publication/d044c2f2-f544-42c7-8293-2985814bdad2 ; Hamamoto et al. 1998, https://next.sciencegate.app/document/10.1109/16.678551].
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
- 2 of 28 modules fail a χ² evenness test at p < 0.001.
- **Reading.** Retention errors are spread evenly at bank scale. That fits the model's independent-error assumption at coarse scale only. Codeword-level clusters need bit addresses, which this file lacks.

### 4.6 Re-run of the model's safe interval

Chipkill kept (RS-8), 2e-19 per read, 1 h scrub, VRT 1x/day; "cut" = interval ÷ the part's own JEDEC window [ESTIMATE].

| Part / code | Model as published | A optimistic | **B central** (CI) | C pessimistic | D 2x pattern | E worst test | Bound, no BER extrapolation |
|---|---|---|---|---|---|---|---|
| DDR5, RS-8 behind SEC, 0.5x derate, 85 °C | 0.285 s (8.9x) | 2.23 s (70x) | **0.96 s (30x)**; CI 0.85-1.14 s | 0.89 s (28x) | 0.82 s (26x) | 0.80 s (25x) | ≥0.37 s (11.5x) |
| same, 70 °C | 0.81 s (25x) | 2.68 s (84x) | 2.68 s (84x); CI 2.37-3.16 s | 2.48 s (78x) | 2.28 s (71x) | 2.24 s (70x) | ≥1.02 s (32x) |
| same, 65 °C | 1.14 s (36x) | 2.85 s (89x) | 2.85 s (89x) | 2.65 s (83x) | 2.43 s (76x) | 2.39 s (75x) | ≥1.02 s (32x), from 70 °C data |
| same, 45 °C | 4.56 s | 3.77 s | 3.77 s | 3.50 s | 3.21 s | 3.16 s | - |
| DDR5, one chip dead, 85 °C | 0.092 s (2.9x) | 0.85 s (27x) | 0.37 s (11.5x) | 0.37 s | 0.32 s | 0.32 s | ≥0.18 s (5.7x) worst module |
| DDR4 (retired-DDR4 proxy), RS-8, 85 °C | 0.837 s (13.1x) | 6.17 s (96x) | **2.66 s (42x)**; CI 2.32-3.20 s | 2.32 s (36x) | 2.25 s (35x) | 2.21 s (34x) | ≥0.74 s (11.5x) |
| DDR4, RS-8, 70 °C | 2.37 s (37x) | 7.41 s | 7.41 s (116x) | 6.45 s | 6.26 s | 6.15 s | ≥2.05 s (32x) |
| DDR4, one chip dead, 85 °C | 0.258 s (4.0x) | 2.28 s | 0.98 s (15x) | 0.98 s | 0.85 s | 0.84 s | ≥0.55 s (8.6x) worst module |

**Refresh-energy cut, DDR5 at 85 °C against the 32 ms window** (refresh + scrub, the model's `refresh_numbers`) [ESTIMATE]:

| Case | Model | A | B | C | D | E |
|---|---|---|---|---|---|---|
| Cut | 8.9x | 67x | **29.5x** | 27x | 25x | 25x |

**Per module, case B** (28 modules):

| Part, 85 °C | Worst module | 10th percentile | Median |
|---|---|---|---|
| DDR5 | 0.59 s (18x) | 0.81 s (25x) | 0.99 s (31x) |
| DDR4 | 1.55 s (24x) | 2.20 s (34x) | 2.59 s (40x) |

The worst module is B7. Vendor B has the steepest tails (σ_ln 0.73-0.89) and the shortest intervals.

**How far the re-run extrapolates.**
- The highest fleet-mean BER measured is 2.0e-7; the highest single-module BER is 1.2e-6.
- The DDR5 code limit is 1.5e-5 and the DDR4 limit is 5.4e-5.
- So cases A-E extrapolate 1.9 decades (DDR5) to 2.4 decades (DDR4) in BER beyond the fleet mean.
- The tail bends the safe way over the measured range: its slope falls from 8.0 to 5.7 to 4.9. Case C holds the last slope fixed and still gives 0.89 s.
- A second, steeper population could appear beyond 2 s. Only the bound column is free of that risk.

### 4.7 VRT sensitivity (the growth rate g is not in the data), case B, 1 h scrub [ESTIMATE]

| VRT growth g | DDR5 85 °C | DDR5 70 °C | DDR4 85 °C |
|---|---|---|---|
| 1x/day (model default) | 0.96 s (30x) | 2.68 s | 2.66 s |
| 100x/day | 0.66 s (21x) | 1.83 s | 1.77 s |
| 700x/day (dossier kill line #4) | 0.45 s (14x) | 1.24 s | 1.18 s |

Even at the kill-line growth rate, the DDR5 case stays above the 6x GO line at 85 °C.

### 4.8 Field data: what public aggregates say

| Item | Value | Tag |
|---|---|---|
| Share of DDR4 field faults that hit several bits (corrected paper) | ~23% | [REPORTED] https://arxiv.org/pdf/2408.15302 |
| Same, original HPCA 2023 abstract (superseded by a decoding-bug corrigendum) | >45% | [REPORTED] https://ieeexplore.ieee.org/document/10071066 |
| Single-bit share of DRAM faults, Cielo/Hopper, vendors A/B/C | 64.6% / 69.5% / 58.4% | [REPORTED] https://sc.osti.gov/-/media/ascr/ascac/pdf/meetings/201512/ResilienceASCAC2015.pdf |
| Single-column share, same | 8.7% / 8.8% / 11.9% | [REPORTED] same |
| Jaguar: permanent faults; multi-bit (row, column, bank) faults | ≥70%; almost 50% of failures | [REPORTED] https://math.nist.gov/mcsd/Seminars/2015/2015-07-21-Diniz-presentation.pdf |
| Alibaba: DRAM-caused server failures with CEs within 1 h before | >40% of 2,137 | [REPORTED] https://shujiehan.github.io/_pages/files/srds22.pdf (search snippet) |
| Huawei: UEs that CEs warn of first ("predictable") are the majority | qualitative | [REPORTED] https://arxiv.org/pdf/2406.05354 |
| Astra: faults even over socket, column and bank; uneven over node, rank and slot | qualitative | [REPORTED] https://www.osti.gov/biblio/2003151 |
| Google fleet: CE rate; DIMMs with errors per year | 25,000-70,000 FIT per Mbit; >8% of DIMMs | [REPORTED] https://research.google/pubs/dram-errors-in-the-wild-a-large-scale-field-study/ |
| M2-MFP (Huawei), Jan-May 2024, Purley: CE-logging DIMMs that failed in the month | 0.56% per month (CI 0.52-0.60%); ~3,600-4,100 CEs per CE-logging DIMM per month | [ESTIMATE] from [REPORTED] counts, https://github.com/hwcloud-RAS/M2-MFP |

FIT = failures per billion device-hours.

**Chance level of multi-chip events** [ESTIMATE]. Assume independent raw errors on a 10-chip x4 line, 64 bits per chip (`field_logs.py`, checked by Monte Carlo):

| Operating point | Share of erroneous lines with errors on ≥2 chips |
|---|---|
| DDR4 RS-8 at its limit (5.4e-5) | 1.6% |
| DDR4 RS-8 servoed (limit ÷ 3) | 0.52% |
| DDR4 BCH-12 at its limit (3.3e-4) | **9.3%** |
| DDR5 behind on-die SEC, post-SEC events at the RS-8 limit | ~0.001% |

The dossier's ">10% multi-chip events" line is almost reached by chance alone at the BCH-12 operating point. It should read ">10% *above the independent-error expectation*".

---

## 5. Verdict per testable claim

| # | Claim (dossier / model) | Verdict | Evidence |
|---|---|---|---|
| 1 | Retention tail anchors: BER 3.6e-9 at 64 ms and 1.1e-10 at 32 ms (85 °C), lognormal (model lines 73-77, 664) | **CONTRADICTED** (too pessimistic, on DDR3L 2015-16) | 166-603x above measured at 1-2 s and 70 °C; ~158 bits per test expected at 256 ms, 0 seen on 28 modules |
| 2 | Tail width σ_ln ≈ 1.24 | **WEAKENED** (slightly; conservative side) | 1.05 (CI 0.97-1.12); per module 0.73-1.25 |
| 3 | Retention x4 per 20 °C (Ea ≈ 0.64-0.72 eV) for the cooling bonus (65 °C, 45 °C) | **CONTRADICTED** for the weakest cells, 20-70 °C | Ea 0.13 eV (CI 0.10-0.17). 45 °C gives ~1.4x over 70 °C, not the model's ~5.7x. The model's 45 °C DDR5 interval (4.56 s) is above the data-based one (3.2-3.8 s) |
| 4 | Same rule from 70 to 85 °C | NOT TESTABLE WITH PUBLIC DATA | No data above 70 °C. The re-run uses the model's 0.72 eV there (pessimistic) |
| 5 | Tail versus main Ea | NOT TESTABLE WITH PUBLIC DATA | Main distribution not reached (max F ≈ 2.5e-6) |
| 6 | Kill #1: NO-GO if the RS-8 interval incl. VRT is <4x the window at 65 °C | **SUPPORTED** (not triggered) for DDR3-class cells; NOT TESTABLE for DDR5 | ≥32x measured at 70 °C with no BER extrapolation; 84-116x modelled (case B) |
| 7 | GO: ≥6x at 85 °C and ≥24x at 65 °C | **SUPPORTED** for DDR3-class cells | 85 °C: ≥11.5x bound, 25-30x cases B-E; 65 °C: ≥32x bound |
| 8 | **~9x refresh-energy cut on DDR5 RDIMMs at 85 °C** | **SUPPORTED as conservative for DDR3-class cells; NOT TESTABLE for DDR5** | Case B 29.5x (CI 0.85-1.14 s → 27-36x); worst module 18x; bound 11.5x. The 0.5x DDR5 derate, the on-die SEC structure and VRT are untested |
| 9 | ~13x on retired DDR4 behind CXL | **SUPPORTED** (conservative; DDR3L used as the proxy) | 2.66 s = 42x (case B); 34-36x pessimistic; bound 11.5x |
| 10 | Degraded mode (one chip dead): 2.9x DDR5, 4.0x DDR4 at 85 °C | **SUPPORTED** (conservative) | 11.5x / 15x (case B); worst-module bounds 5.7x / 8.6x |
| 11 | VRT growth ≤700x/day (kill #4); VRT pairs within 2x of chance | NOT TESTABLE WITH PUBLIC DATA | No addresses or timestamps. Even at 700x/day, case B keeps DDR5 at 14x |
| 12 | Kill #2: BCH dies if >0.4% of error bits sit in ≥3-bit clusters; both codes die if >10% of events span >1 byte | NOT TESTABLE WITH PUBLIC DATA | No bit addresses. Bank-level spread is even (2 of 28 modules uneven), which is consistent with, but does not prove, independent errors |
| 13 | Multi-chip events ≤10% (GO line) | NOT TESTABLE WITH PUBLIC DATA | Field logs run at normal refresh, and the only chip-level logs (SmartMem) are gated. Chance alone gives 0.5-1.6% with RS-8 and 9.3% at the BCH-12 limit, so the line needs a chance-corrected definition |
| 14 | Chipkill must be the default (RT-CIRC-03) | **SUPPORTED** | 30-42% of field faults are not single-bit; ~23% of DDR4 faults are multi-bit; column faults are 9-12% |
| 15 | First-read chip marking works because faults show CEs before UEs (kill #10, model §10.6) | **SUPPORTED** (weakly) | >40% of DRAM-caused failures show CEs within 1 h before; predictable UEs are the majority. The share of "sudden" UEs (no CE first) is not public |
| 16 | The servo's 1 h grade holds for 1,000 h on ≥95% of modules | NOT TESTABLE WITH PUBLIC DATA | No timestamps. Warning: 6 of 17 modules show >3x spread between repeated tests at one condition, larger than the 3x guard; the cause is unresolved |
| 17 | UE budget basis: field DIMM UE rates ~0.2-1% per year (model line 47) | NOT TESTABLE WITH PUBLIC DATA | M2-MFP gives 0.56% per month of *CE-logging* DIMMs failing; the fleet denominator is not published |
| 18 | Row hammer at relaxed refresh (kill #5) | NOT TESTABLE WITH PUBLIC DATA | No public data at relaxed refresh |

---

## 6. What it means for the ~9x claim

- **The ~9x comes from the model's assumed tail, not from data.** The anchors trace back to RAIDR-era cell counts with a 4x temperature derate (model lines 73-77).
- **Real 2015-16 DDR3L modules have far fewer weak cells.** Their tail sits 2-3 orders of magnitude lower at 1-2 s. Its width is similar.
- **Re-run with the real tail, DDR5's interval moves from 0.285 s to ~0.8-1.0 s at 85 °C.** That keeps every other model input, including the model's own 0.5x DDR5 derate and its 0.72 eV above 70 °C. The energy cut moves from 8.9x to ~25-30x. The worst module still gives 18x, and the no-extrapolation bound gives ≥11.5x.
- **So the claim is safe on DDR3-class silicon.** Four things keep it from being proven for DDR5:
  1. **The part is old.** DDR3L 4Gb (2015-16) is not DDR5 1a/1b 16Gb. The 0.5x derate is a guess (model line 138) that no public data tests. If DDR5's true derate were 0.15x instead of 0.5x, case B would fall back to about the 9x headline [ESTIMATE: interval scales with the derate].
  2. **On-die SEC changes the error structure.** The model says it turns doublets into 3-bit events (§2.4). No public chip data exists; EINSim's real-chip data is confidential.
  3. **VRT growth is unmeasured.** At 700x/day the DDR5 case falls to 14x.
  4. **The sample is small.** It is 31 modules from one study, while the dossier wants ≥30 lots per vendor.
- **The cooling bonus is overstated.** The weakest cells have Ea ~0.13 eV, so a temperature-tracking controller gains little below 70 °C. The 65 °C GO line still passes, because the whole tail sits so much further right. But the dossier's 45 °C figures (x16, e.g. 13-24 s in §2.5) should not be used.
- **Recommendation.** Keep ~9x as the planning number. Public DDR3L data suggests the true value could be ~3x higher. Drop the x16 45 °C multiplier from any headline. Redefine the multi-chip kill line against the independent-error expectation.

---

## 7. What data would settle the rest

| Open question | Who can answer it | What to run |
|---|---|---|
| Bit-level clusters in codewords (kill #2); VRT fraction and growth g (kill #4); Ea of the *same* cells at 25/45/65 °C (not fleet means) | **Home-lab E6** ([../../home-lab/E6_retention_tail_real_dram.md](../../home-lab/E6_retention_tail_real_dram.md)) | Log every failing address on a 64 Mbit SDRAM at 64 ms-65 s and 25/45/65 °C, with repeat maps every 20 s-20 min for VRT. Going out to 16-65 s reaches BER 1e-5-1e-4 *directly*, removing this report's 2-decade extrapolation (for that chip). Feed the address logs to `field_logs.py`-style census code and to E6's `retention_map.py analyze`. It cannot answer the DDR5 questions |
| DDR5 derate, post-SEC event structure, ECS (error check and scrub) counts, chipkill-safe interval on 1a/1b RDIMMs | **Dossier Phase 1, DDR5 leg** (§5.R step 3; ~$124k Phase 1 total, ~$20k for the two open testers [ESTIMATE: dossier]) | ≥24 RDIMMs on the open Antmicro DDR5 testers; BEER-style H-matrix recovery (https://github.com/CMU-SAFARI/BEER) |
| Lot-to-lot spread; ≥30 lots per vendor; 1 h grade vs 1,000 h hold | Dossier Phase 1 steps 1 and 6 | 150 DDR4 modules screened, 60 deep-mapped, 20 soaked 1,000 h |
| Multi-chip event share in the field; CE-before-UE share; DQ x beat patterns | SmartMem / M2-MFP (register on Codabench) or the Alibaba set (Tianchi) | `python3 -I research/realdata/field_logs.py --log <log> --tickets <tickets>`. Do not commit SmartMem data: its rules forbid redistribution |
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
- **Network.** Many hosts were blocked in this session (listed below). The SmartMem dataset and terms pages were read from the site's source repository on github.com because its github.io site was blocked. No data was fetched that way.

**Blocked hosts in this session:** zenodo.org, courses.grainger.illinois.edu, people.inf.ethz.ch, users.ece.cmu.edu, www.ece.cmu.edu, hwcloud-ras.github.io, hyxie2023.github.io, github.com web pages and API (git clone and raw.githubusercontent.com worked), tianchi.aliyun.com, www.usenix.org, www.osti.gov, safari.ethz.ch, people.cs.rutgers.edu, www.pdl.cmu.edu, www.research-collection.ethz.ch, figshare.com, dataverse.harvard.edu, www.kaggle.com, huggingface.co, ar5iv.labs.arxiv.org, www.semanticscholar.org, api.semanticscholar.org, dl.acm.org, export.arxiv.org, doi.org, www.sandia.gov, ieee-dataport.org, data.mendeley.com, osf.io. Hosts blocked in earlier sessions (arxiv.org, ieeexplore.ieee.org and others) were not retried.

---

## Sources

**Data and code**
- https://github.com/CMU-SAFARI/DRAM-Voltage-Study (dataset 1; commit b2089c3c7c2aac1d0936b4cfc572a675f5fd73f4)
- https://raw.githubusercontent.com/CMU-SAFARI/DRAM-Voltage-Study/b2089c3c7c2aac1d0936b4cfc572a675f5fd73f4/characterization_results/retention_time_profile.csv
- https://arxiv.org/abs/1705.10292 (Chang et al., SIGMETRICS 2017: 124 DDR3L chips, 31 modules, 4Gb chips, 2 GB modules; via search snippet)
- https://github.com/alibaba-edu/dcbrain/tree/master/dramdata
- https://tianchi.aliyun.com/dataset/132973
- https://github.com/zncheng/dramanalysis
- https://github.com/hwcloud-RAS/SmartMem.github.io (dataset and terms pages)
- https://www.codabench.org/competitions/3586/
- https://github.com/hwcloud-RAS/M2-MFP
- https://doi.org/10.5281/zenodo.6515019
- http://www.ece.cmu.edu/~safari/tools/dram-sigmetrics2014-fulldata.html
- https://www.pdl.cmu.edu/ftp/NVM/khan-efficacy-sigmetrics2014.pdf
- https://github.com/CMU-SAFARI/EINSim
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
- https://arxiv.org/pdf/2406.05354 (Yu et al., DSN 2024)
- https://arxiv.org/pdf/2312.02855 (Yu et al., error bits)
- https://sc22.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap137.html (Li et al., SC22)
- https://research.google/pubs/dram-errors-in-the-wild-a-large-scale-field-study/ (Schroeder et al., 2009)

**Retention physics**
- https://next.sciencegate.app/document/10.1109/16.678551 (Hamamoto et al., 1998)
- https://tore.tuhh.de/entities/publication/d044c2f2-f544-42c7-8293-2985814bdad2 (Weber et al., tail activation energies)
- https://arxiv.org/pdf/2306.16037 (Liu et al. ISCA 2013, retrospective)
- https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_paper.pdf (Patel et al., REAPER)
- https://fast.cc.gatech.edu/papers/DSN_2015_1.pdf (Qureshi et al., AVATAR)
- https://www.pdl.cmu.edu/ftp/NVM/raidr-isca12.pdf (RAIDR, the source of the model's anchors)

**Study files used**
- ../../dossiers/raw-ber-contract.md (§2.4, §2.5, §5.R, §9, §11)
- ../../models/raw-ber-contract.py (lines 47, 73-80, 138, 296, 615, 664-706, 917, 1007-1021)
- ../../home-lab/E6_retention_tail_real_dram.md
