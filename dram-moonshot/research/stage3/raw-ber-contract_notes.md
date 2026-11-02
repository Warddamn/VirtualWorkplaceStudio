# RAW-BER CONTRACT: Stage 3 research notes

Agent `dos-raw-ber-contract`, 2026-11-02. Concept rank 4 (EV 60) in `FINAL_CONCEPTS.md`.
- **Model:** `models/raw-ber-contract.py`. Output: `research/stage3/raw-ber-contract_model_output.md`.
- **Sources:** `research/sources/dos-raw-ber-contract.jsonl` (43 entries).
- **Assumptions:** `research/assumptions/dos-raw-ber-contract.md`.
- **Network:** 6 of 6 WebSearch calls used. Every web fact below came from a search snippet, marked "(via search snippet)" in the log. Facts I could not verify this session are tagged [UNVERIFIED: training knowledge].

---

## 1. Verdict

The concept survives on physics, but four of its claims need correction. The decisive experiment stays cheap and binary.

**What the model confirms.**
- A raw-BER-1e-4 operating point buys 7 → 3.72 σ of sense margin: 50 → 26.6 mV and Cs 5.4 → 2.7 fF (pillar 1,300 → 644 nm) on the A1 bitline. That is exactly the 1.88x the concept claims.
- Relaxed refresh at ~1 s cuts refresh power 0.49 → 0.03 W per 64 GB RDIMM (15x). The refresh-blocked time on 16Gb dies falls from 7.6% to 0.5%.

**What the model changes.**

1. **The reliability target is ~100x tighter than the concept assumed.** A t=8 BCH at 1e-4 fails 2.3e-17 per read. At 10 GB/s that is ~10% UE per module-year. A realistic budget (≤0.1%/yr from random raw errors) needs **2e-19 per read**, which means **t=9 (90 bits, 17.6%)**. The ~9-21-point die-area cost of check bits on a new die is real: a 1β cell with t=9 parity drops to 0.404 Gb/mm² (0.90x).

2. **Erasure flags are a margin-error tool, not a refresh tool.**
   - *Refresh latching.* A retention error that happens before the next refresh is sensed wrong and restored to a full, confident rail. For long-resident data, retention and VRT errors are therefore almost all *confident*. Only bits read in their first period after a write can be flagged (14-60% of those).
   - *False flags.* For margin errors (Gaussian), false flags outnumber caught errors 1.6-130x, depending on the window.
   - *What flags are worth.* With a narrow window (δ ≈ 0.5 σ ≈ 3.6 mV) and Chase/GMD decoding, flags save **20 check bits (90 → 70)** or **~8% more dV**, not the "d=5, 3.9%" in the concept text. Half the errors confident → 10 bits saved. All confident → nothing.

3. **Error geometry matters as much as flaggability.** Under a 2e-19 target, a binary BCH-12 line code tolerates only **~0.4% of error bits arriving in 3-bit clusters** at 1e-4, and essentially no 8-bit clusters. An RS(80,64) byte-symbol code in the same 128-bit side band is 6x weaker on iid bits (5.4e-5 vs 3.3e-4). It is indifferent to byte-confined clusters and keeps chipkill. The key unknown should be restated as: *the per-codeword cluster-size spectrum, plus the flaggable share of margin errors, plus the VRT growth rate.*

4. **Margin and refresh are one budget, not two dividends.** The code grants one raw-BER allowance. Spending all of it on margin (Cs 2.44 fF) leaves only 371 ms refresh. Spending all of it on refresh gives ~1.5 s at today's 50 mV. A 50/50 split gives 25.6 mV *and* 1.2 s (18x), because both tails are steep. The portfolio concepts that bank the 1.88x (MARGIN STACK, PIXEL-STACK, DIODE-TOWER, AND-STACK MLC) must not also bank the 10-15x refresh cut on the same cells unless the retention tail moves right (oxide channels).

**A positive finding the concept missed.** The commodity path needs **no new code storage and no page code for iid errors**. A DDR5 ECC RDIMM already carries 128 check bits per 64 B line. As BCH-12 that takes iid raw BER up to 3.3e-4. Behind DDR5 on-die SEC, the same code takes an internal raw BER up to 1.7e-4. On the central (lognormal) retention model that allows **~1.5 s refresh at 85 C (iid) or ~0.84 s (clustered, RS)**, and 4-16x longer at 45-65 C DIMM temperatures. The pessimistic bound with RS is 0.5 s at 85 C, which is still 7.7x.

**Where the value lies.**
- The refresh-energy dollar value on commodity DRAM is small: **$0.041/GB over 5 years** (2.7% of $1.48/GB), ~7 MW per exabyte of server DRAM.
- The tRFC time win grows with die density: 10.5% → 0.7% at 32Gb, and 41% → 2.6% at 64Gb on DDR5's 3.9 µs tREFI.
- The strategic value is the **interface**: a published raw-BER/geometry spec lets new cells qualify against a controller instead of against 64 ms / 7σ.

---

## 2. Prior art and who is pursuing it

| Year | Work (who) | What it shows | Relation |
|---|---|---|---|
| 2000s | Micron "memory controller compensating for memory cell data losses" family, incl. [US 7,447,974](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7447974) and [US 9,064,600](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9064600) | Controller ECC lets the refresh timer slow down because the resulting errors are correctable; notes the ECC capacity cost (via search snippet) | **The core "ECC buys refresh" idea is old.** Early family members are likely expired or near expiry [UNVERIFIED: term not checked]. The novelty must sit elsewhere. |
| 2009 | Elpida [US 7,493,531](https://patents.google.com/patent/US7493531) | Sets the refresh period by measuring error rate on expected-value data in self-refresh (via search snippet) | Prior art for error-rate-driven intervals |
| 2010 | Hi-ECC ([Wilkerson et al., ISCA 2010](https://courses.grainger.illinois.edu/CS534/fa2021/reading_list/9a.pdf), Intel) | Multi-bit BCH over large lines cuts eDRAM refresh power ~93% at ~2% storage (via search snippet) | Closest academic ancestor of the page code |
| 2011 | Qimonda [US 7,975,170](https://patents.google.com/patent/US7975170) | Per-page refresh intervals from refresh-fail information; search also surfaced SECRET (ECC on leaky cells, up to 87% refresh-power cut) (via search snippet) | Retention-aware refresh |
| 2012 | RAIDR ([CMU, ISCA 2012](https://www.pdl.cmu.edu/ftp/NVM/raidr-isca12.pdf)) | 74.6% fewer refreshes, 16.1% DRAM power (via search snippet) | The ~4x "no-ECC" baseline that the NO-GO line references |
| 2012 | LOT-ECC ([Utah, ISCA 2012](https://users.cs.utah.edu/~rajeev/pubs/isca12.pdf)) | Tiered chipkill-class ECC on commodity DRAM | Code-architecture prior art |
| 2013 | ArchShield ([Georgia Tech, ISCA 2013](https://memlab.ece.gatech.edu/papers/ISCA_2013_1.pdf)) | Tolerates error rates up to 1e-4 at 4% capacity, <2% performance (via search snippet) | Closest system precedent for a 1e-4 contract |
| 2017 | REAPER ([Patel et al., ISCA 2017](https://people.cs.rutgers.edu/~mp2099/files/patel_isca2017_reach_paper.pdf)) | Profiling 250 ms beyond the target finds >99% of failing cells with <50% false positives; 368 LPDDR4 chips; VRT makes profiling hard (via search snippet) | Method template for Phase 1 |
| 2018 | Solar-DRAM ([ICCD 2018](https://people.cs.rutgers.edu/~mp2099/files/kim_iccd18_solar_paper.pdf)) | Cells that fail at reduced tRCD are weak and stable over time (via search snippet) | Basis for the reduced-tRCD flag proxy |
| 2018 | Charge-level-aware partial restoration ([MICRO 2018 poster](https://people.cs.rutgers.edu/~mp2099/files/wang_micro18_reducing_poster.pdf)) | Restoration is up to 43.6% of access latency (via search snippet) | Partial-restore emulation |
| 2022-23 | DRAM Bender ([ETH/CMU, IEEE TCAD](https://arxiv.org/pdf/2211.05838)) | Open-source FPGA tester: any command at any timing; DDR3/DDR4 on five boards, plus an HBM2 board ([FMS 2024](https://files.futurememorystorage.com/proceedings/2024/20240808_TEST-301-1_LUO.pdf)) (via search snippet) | **Phase 1 instrument.** No DDR5 support found. |
| 2024 | PRAC overhead study ([SAFARI, arXiv 2406.19094](https://arxiv.org/pdf/2406.19094v1)) | JEDEC PRAC: <13% overhead today, up to 94% for future chips (via search snippet) | Hammer-safety cost |
| 2025 | PaCRAM ([SAFARI, HPCA 2025](https://www.arxiv.org/pdf/2502.11745)) | 388 DDR4 chips; preventive-refresh latency cut ~64% with partial charge restoration, if mitigation is made more aggressive (via search snippet) | **Direct precedent for truncated-tRAS half-charge emulation**; open code |
| 2025 | X-PPR ([IEEE CAL 2025](https://ieeexplore.ieee.org/document/10935665)) | Field repair of faulty words in recycled DDR4 inside a commercial CXL device (via search snippet) | CXL-controller repair of weak DRAM |
| 2025 | CnC-PRAC ([arXiv 2506.11970](https://www.arxiv.org/pdf/2506.11970)) | PRAC alternative with ~1% energy overhead (via search snippet) | Hammer option |
| 2025 | [US 12,488,827](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12488827) CXL device | CXL device refresh controller counts commands and does targeted refresh for row hammer; no relaxed-refresh/ECC claim seen (via search snippet) | Neighbouring CXL IP |
| 2025-26 | EasyDRAM ([SAFARI](https://arxiv.org/html/2506.10441v2)) | FPGA framework for end-to-end evaluation of DRAM techniques on real chips (via search snippet) | Possible Phase 2 shortcut |
| 2026 | Meta Vistara CXL ASIC ([StorageNewsletter 2026-07](https://www.storagenewsletter.com/2026/07/02/meta-uses-cxl-for-memory-expansion-to-replace-ddr4/)); Marvell Structera X/XA ([Marvell](https://www.marvell.com/blogs/structera-xa-cxl-compression-every-gigabyte-counts.html)) | Mixed-vendor retired DDR4 behind a CXL controller; inline compression | **Commercial landing zone.** Neither is known to run relaxed refresh. |
| 2026 | SHIELD ([arXiv 2604.07396](https://arxiv.org/pdf/2604.07396)) | KV mantissa tolerates BER 1e-4; relaxed refresh saves 35% refresh energy (via search snippet) | Typed-page evidence ("lossy-bounded") |
| 2026 | DejaVu ([CISPA, ISCA 2026](https://cispa.de/de/research/publications/213276-dejavu-why-you-should-write-to-your-dram-rows-twice-carefully)) | Prior data and under-restoration change read-disturb ACmin (via search snippet) | Hammer × partial-restore interaction risk |
| 2024 | SanDisk/WD soft-bit NAND patents, e.g. [US 11,907,545](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11907545) | Second sense with a longer discharge time gives a soft bit; soft data is compressed on die before going to the controller (via search snippet) | **Nearest analogue of the DRAM SA delayed-sample flag.** Design-around needed. |

**Not found in this session's searches** (it is a limited sample, so the IP check below matters):
- a DRAM sense-amp per-bit reliability/erasure output used by a memory-controller decoder;
- a CXL Type-3 device combining relaxed refresh with strong ECC;
- an open raw-BER device grade;
- typed pages (exact/regenerable/lossy) as device-side code classes.

These are the claimable deltas.

**Training-knowledge context [UNVERIFIED]:**
- XED (ISCA 2016) exposes on-die ECC flags.
- HBM3 reports per-read ECC severity.
- AVATAR (DSN 2015) upgrades rows that show VRT.
- BEER/HARP (MICRO 2020/2021) reverse-engineer and profile behind on-die ECC.

---

## 3. Best demonstrated numbers per component

| Component | Best number found | Source | Model value used |
|---|---|---|---|
| Strong ECC → refresh | eDRAM refresh power −93% at ~2% storage | Hi-ECC (via snippet) | DRAM 64 ms → 1 s: 15x (section 5) |
| Architecture-level BER tolerance | 1e-4 at 4% capacity, <2% performance | ArchShield (via snippet) | BCH-12 side band 3.3e-4 iid |
| Retention-aware refresh (no ECC) | −74.6% refreshes, −16.1% DRAM power | RAIDR (via snippet) | NO-GO baseline ~4x |
| Retention profiling | >99% coverage, <50% false positives | REAPER (via snippet) | Phase 1 method |
| Partial restore | ~64% preventive-refresh latency cut | PaCRAM (via snippet) | Half-charge emulation |
| Hammer counters | PRAC <13% now; CnC-PRAC ~1% energy | SAFARI (via snippet) | RFM substitution 0.4% typical / 8% attack [ESTIMATE] |
| App BER tolerance | KV mantissa 1e-4, 35% refresh-energy cut | SHIELD (via snippet) | Typed pages |
| CXL reuse | Structera X 2404: 12 DDR4 DIMMs per controller; Meta Vistara | TechSpot / StorageNewsletter (prior logs) | Landing zone |
| FPGA CXL platform | Agilex 7 I-Series kit ~€9k; CXL Type-3 IP ~€192k list | [KIT OS group page](https://os.itec.kit.edu/4012.php), Jan 2025 (via snippet) | Phase 2 budget |
| Line BCH decoder at 28 nm | No measured figure found | none | ESTIMATE: 0.05 pJ/bit syndrome fast path, ~10-20 ns slow path |
| SA delayed-sample flag latch | No DRAM silicon found; NAND soft-bit sensing is shipping | US 11,907,545 (via snippet) | 3-7% die area (Stage 2 critic estimate) |
| Analog hammer counter | Micron patents; no silicon data found | US 10,943,636, US 11,568,918 | Phase 3 test structure |

---

## 4. Model headline numbers (from `models/raw-ber-contract.py`)

**Target.** 2e-19 per 64 B read (1e-3 UE per module-year at 10 GB/s).

**Line code at 1e-4** (hard decisions):

| t | Check bits | Parity |
|---|---|---|
| 9 | 90 | 17.6% |

**Line code across raw BER:**

| Raw BER | t |
|---|---|
| 1e-5 | 6 |
| 3e-4 | 12 |
| 1e-3 | 17 |

**4 KB page code parity:**

| Raw BER | BCH parity | Shannon floor |
|---|---|---|
| 1e-4 | 1.46% | 0.15% |
| 1e-3 | 4.8% | — |
| 1e-2 | 30.5% | 8.8% |

**Commodity side band (128 bits per line):**
- BCH-12: iid raw BER up to 3.3e-4.
- RS-8: up to 5.4e-5. RS headroom is unchanged by byte-confined clusters and falls to ~8e-7 with a dead chip marked.
- Behind DDR5 on-die SEC: internal raw BER up to 1.7e-4.

**Margin:**

| Raw BER | dV (mV) | Cs (fF) |
|---|---|---|
| 1e-4 | 26.6 | 2.68 |
| 1e-3 | 22.1 | 2.20 |

The step from 1e-4 to 1e-3 buys only 1.22x more Cs.

**Flags** (δ = 0.5 σ, at 1e-4). Check bits by confident share:

| Confident share | Check bits (Chase) |
|---|---|
| 0 | 70 |
| 0.5 | 80 |
| 1 | 90 |

**Refresh interval at 85 C** (BCH-12 iid / RS-8 clustered):

| Retention model | BCH-12 iid | RS-8 clustered |
|---|---|---|
| pow3 | 3.6 s | 2.0 s |
| Lognormal | 1.5 s | 0.84 s |
| pow5 | 0.72 s | 0.50 s |

**VRT sensitivity.** At 100x/day VRT growth with a 24 h scrub, the interval falls to 375 ms. The scrub interval is the lever: a 10-min scrub holds 1.3 s.

**Power per 64 GB RDIMM:**

| Interval | Refresh + scrub | Cut vs 64 ms |
|---|---|---|
| 0.5 s | 0.063 W | 7.7x |
| 1 s | 0.032 W | 15.3x |
| 2 s | 0.016 W | 30x |

Scrub power is 0.6 mW. Idle power falls 14-16%.

**Hammer.** Controller RFM substitution costs 0.4% of bank time typical and 8% under attack, against the 7.6% tRFC it removes [ESTIMATE].

**Page codes.**
- 64 B writes need ≥99% SRAM coalescing, which brings traffic to ≤2.3 line transfers per write.
- Page decode beats refresh only for pages read less than ~0.7 times per second.

**Value.**
- $2.60 per 64 GB over 5 years ($0.041/GB, 2.7% of $1.48/GB).
- Refresh-blocked time recovered: 7.1 points (16Gb), 9.8 (32Gb), 38 (64Gb, DDR5 tREFI basis).

---

## 5. Facilities that could build the demo (U.S.)

This concept needs a **bench lab, not a cleanroom**, for Phases 1-2. Fab access is needed only for the Phase 3 test structures.

| Need | Facility | Cost / rate info | Notes |
|---|---|---|---|
| DRAM characterization | Own bench, 4 DRAM Bender stations | ~$14k per station [ESTIMATE]; open-source gateware ([GitHub CMU-SAFARI/DRAM-Bender](https://www.research-collection.ethz.ch/handle/20.500.11850/642507)) | DDR3/DDR4 + HBM2 only. DDR5 needs a collaborator or Phase 2's FPGA DDR5 PHY. |
| Collaborating DRAM-test labs | CMU (SAFARI's U.S. arm, Mutlu lineage); Rutgers (Minesh Patel, REAPER/BEER/HARP); Georgia Tech (Qureshi, ArchShield) | Subaward / student time ~$60k [ESTIMATE] | Existing rigs and chip populations; SAFARI-lineage PhD students already run DRAM Bender |
| CXL controller prototype | Agilex 7 I-Series dev kit (2x R-Tile, PCIe/CXL 5.0 x16), [Altera Rev B](https://www.altera.com/products/devkit/po-3247/agilex-7-fpga-i-series-development-kit-2x-r-tile-and-1x-f-tile-rev-b) | ~€9k per kit; CXL Type-3 IP ~€192k list (Jan 2025, via KIT snippet); a separate IP license is required ([Intel UG](https://www.intel.com/content/www/us/en/docs/programmable/683288/current/i-series-fpga.html)) | The IP license is the largest single budget risk. Mitigations: university/startup license, a partner who owns IP, or PCIe-BAR emulation for reliability soak. |
| CXL hosts | Intel Xeon (Sapphire/Emerald/Granite Rapids) or AMD EPYC Genoa/Turin servers | ~$15-20k each [ESTIMATE] | UIUC (Nam Sung Kim) runs CXL testbeds [UNVERIFIED: training knowledge] |
| Test-structure MPW (SA flag latch, analog counters) | ChipFoundry sky130 (SkyWater, Minnesota) | $15k per 100 chips; a shuttle runs only if ≥50% of slots fill ([Tiny Tapeout](https://tinytapeout.com/news/chipfoundry-sponsor/); [eeNews](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)) | ~8 months from submission to chips (prior TT data in logs) |
| Advanced-node MPW (if a 22/28 nm flag latch is needed) | MOSIS 2.0 (USC ISI): 12-350 nm, >35 shuttles; GF partner agreement ([ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/), [AAC 2026-07](https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy)) | No price found | Better shared with MARGIN STACK's 28/22 nm MPW (~$275k portfolio line) |
| Non-U.S. alternative | wafer.space GF180 | GF Singapore fab (prior log) | Not U.S.-fab |
| University nanofabs (Stanford SNF, Cornell CNF, MIT.nano, Penn Singh, GT IEN, ASU, Purdue Birck, UT Austin) | Not needed for this concept | — | GT IEN or ASU could package/bond test die if needed |
| National labs | LLNL (zfp, lossy-bounded page class); NERSC/TACC/ALCF (HPC traces, soak partners); LANL/Sandia (field DRAM-fault datasets for correlation priors) [UNVERIFIED: training knowledge] | User proposals; no fee for open science | Sandia MESA/CINT, Argonne CNM, ORNL CNMS, LBNL Foundry and NIST CNST are not needed |
| Thermal / soak | Benchtop chamber plus DRAM Bender heater-pad PID control (FMS 2024 slides) | ~$12k [ESTIMATE] | 45/65/85 C campaigns |

---

## 6. Collaborators and recruits

Named groups. Affiliations are from training knowledge unless a URL is given.
- **Onur Mutlu, SAFARI (ETH Zürich / CMU).** DRAM Bender, PaCRAM, REAPER, RAIDR, EasyDRAM. The natural Phase 1 partner, and the source of DDR5 access and characterization know-how. Students on the logged papers include A. G. Yağlıkçı, A. Olgun and H. Luo (FMS 2024 slides).
- **Minesh Patel (Rutgers; files hosted at people.cs.rutgers.edu/~mp2099).** REAPER, plus profiling behind on-die ECC ([thesis](https://arxiv.org/pdf/2204.10387)). The best single advisor on "raw errors behind on-die ECC".
- **Moinuddin Qureshi (Georgia Tech).** ArchShield (1e-4 tolerance), AVATAR (VRT) and hammer work. Georgia Tech is also named in the concept's U.S.-buildable line.
- **Chris Wilkerson (Intel Labs) [UNVERIFIED current affiliation].** Hi-ECC.
- **Prashant Nair (UBC) [UNVERIFIED].** XED, on-die-ECC flag export.
- **Mattan Erez (UT Austin) [UNVERIFIED].** Frugal ECC and memory resilience.
- **Rajeev Balasubramonian (Utah).** LOT-ECC.
- **Lara Dolecek (UCLA) [UNVERIFIED].** Coding theory for memories. Could lead the code design (Chase/GMD at 2e-19, RS vs BCH under clustering).
- **Nam Sung Kim (UIUC) [UNVERIFIED].** CXL device characterization testbeds.
- **Peter Lindstrom (LLNL) [UNVERIFIED].** zfp, for the lossy-bounded page class.
- **Kaveh Razavi (ETH COMSEC) [UNVERIFIED].** DDR5 hammer and TRR reverse engineering.

Recruit profiles:
- **Device/circuit co-founder.** A DRAM sense-amp/periphery designer, e.g. ex-Micron Boise. Owns the half-charge emulation interpretation, the SA delayed-sample flag latch and the JEDEC grade definition.
- **First hire or contractor.** An SSD-controller ECC architect (BCH/LDPC RTL, Chase decoders) from a flash-controller team. The concept *is* the NAND controller playbook, and those people exist in volume.
- **Student / postdoc.** Someone who has already run DRAM Bender, through a SAFARI-, Rutgers- or GT-lineage subaward.

---

## 7. Decisive experiment

### 7.1 Design, step by step

**Phase 1: error physics on real DRAM (months 0-6, ~$96k; this phase alone decides GO/NO-GO).**

1. **Rigs.** Build 4 DRAM Bender stations on the listed Xilinx/BittWare DDR4 boards. Each gets heater-pad PID temperature control and DDR4 VPP control (both supported per FMS 2024), plus a benchtop chamber for cross-checks.
2. **Population.**
   - 60 DDR4 modules: 3 vendors × 2-3 date codes, x4 and x8.
   - 20 retention-reject or recycled DDR4 modules from second-life brokers.
   - Optionally the HBM2 board.

   DDR4 is the right primary vehicle because it has no on-die ECC, so it shows raw physics. DDR5 is handled in step 9.
3. **Retention map.** Sweep P ∈ {0.128, 0.256, 0.5, 1, 2, 4} s × T ∈ {45, 65, 85} C × {random, checkerboard, solid, row-stripe} patterns. Write, wait with REF suppressed, read, and log every failing address.
   - *Fit:* BER(P, T); which of pow3, lognormal or pow5 holds; σ_ln.
4. **Refresh-latching test.** At P = 1 s, run N refresh periods after a write, then read. Use a second read at reduced tRCD steps as the flag proxy.
   - *Measure:* first-period vs steady-state flagged share. This directly tests the "flags don't help retention" prediction (§1, point 2).
5. **VRT soak.** Re-map 20 modules hourly for ≥4 weeks at 65/85 C.
   - *Measure:* VRT growth g (new latched errors per day, as a multiple of static BER). This is the model's scrub-interval sensitivity.
6. **Cluster spectrum.** Map each failing bit into the 64 B codeword geometry (chip slice, DQ, beat, x4/x8).
   - *Measure:* the per-codeword error histogram, overdispersion vs Poisson, and the cluster-size spectrum (1, 2-3, 4-8, >8 bits; byte-confined or not).
   - *Score:* run the maps through BCH-12, RS-8 and Chase decoders (the model's functions).
7. **Margin emulation (new-cell regime).**
   - *Setup:* truncated-tRAS partial restore (the PaCRAM method, open code) plus reduced VPP, sweeping raw BER from 1e-5 to 1e-3 at nominal refresh. Double-read at nominal and stepped-reduced tRCD.
   - *Measure:* flagged share, false-flag ratio vs window, and per-codeword statistics.
8. **Hammer × relaxed refresh.** Run double- and many-sided hammer at P = 64 ms vs 1 s, with controller-issued directed neighbour activation standing in for REF-hosted TRR.
   - *Measure:* HCfirst for retention-weakened victims. DejaVu and PaCRAM both show that restoration level shifts read-disturb thresholds.
9. **DDR5 cross-check.** Through a collaborator's DDR5 tester, or the Phase 2 FPGA DDR5 PHY at controller-controlled REF rates, measure post-on-die-ECC error patterns against the model's on-die-SEC prediction (internal limit 1.7e-4).
10. **GO/NO-GO #1 (month 6).** Apply the line in §7.3.

**Phase 2: CXL controller and soak (months 5-16, ~$262k; the chief's plan treats this as a raise milestone or grant).**

11. **Agilex 7 CXL Type-3 controller design:**
    - selectable BCH-12 / RS-8 line codec using the RDIMM ECC side band;
    - Chase slow path;
    - 4 KB page BCH for cold pages, with an SRAM write-coalescing buffer (≥99% hit target);
    - temperature-tracking REF scheduler (DDR5 RDIMM thermal sensor) with RFM substitution;
    - hourly scrubber;
    - typed-page HDM regions: exact / regenerable (CRC-only + recompute hook) / lossy-bounded;
    - graceful degradation: a rank with a marked dead chip returns to ≤256 ms.
12. **Soak.** 1,000 h at 1 s refresh on 2 boards, under Redis, SPEC CPU and vLLM+LMCache traces. Use commodity and retention-reject DDR5 RDIMMs.
    - *Pass:* zero UE, and corrected-error counts within 2x of the Phase 1 model.

    A 1,000 h soak (~5.6e14 reads per board) cannot prove 2e-19 directly. It catches surprises; the reliability claim rests on the Phase 1 statistics.

**Phase 3: flag and counter silicon (months 8-18, ~$50k).**

13. **sky130 test structures** (ChipFoundry shuttle):
    - a delayed-sample SA flag-latch array on a mimic bitline (measures the flag window δ vs offset σ);
    - 1k reset-on-REF analog activity counters (trip-count spread, 25-110 C).

    Share the 28/22 nm MARGIN STACK MPW if it is funded.
14. **Contract spec v0.9.** Draft an OCP/CXL contribution covering raw BER, the cluster-spectrum limits, VRT growth, the flag protocol and the typed-page classes. Pair it with a JEDEC "ECC-native grade" proposal.

### 7.2 Budget (standalone; under $1M)

Inside the portfolio seed, only Phase 1 is funded; the rest is a raise milestone.

| # | Item | Cost | Basis |
|---|---|---|---|
| 1 | 4 DRAM Bender stations (FPGA board, DIMM interposer, heater/PID, VPP supply) | $56k | ESTIMATE ~$14k each |
| 2 | Modules: 60 DDR4 + 20 reject/recycled DDR4 + 20 DDR5 RDIMM | $18k | ESTIMATE |
| 3 | Benchtop thermal chamber and thermometry | $12k | ESTIMATE |
| 4 | Error-map storage and analysis server (~50 TB) | $10k | ESTIMATE |
| | **Phase 1 subtotal** | **$96k** | |
| 5 | 2 × Agilex 7 I-Series dev kit | $22k | ~€9k each (KIT page, Jan 2025, via snippet) |
| 6 | CXL Type-3 IP license (negotiated) or partner IP | $100k reserve | List ~€192k (via snippet) |
| 7 | 2 CXL-capable host servers | $35k | ESTIMATE |
| 8 | RTL/verification contractor (codecs, Chase, scheduler, scrubber) | $90k | ESTIMATE |
| 9 | Soak operations (power, colo, traces) | $15k | ESTIMATE |
| | **Phase 2 subtotal** | **$262k** | |
| 10 | 2 sky130 shuttle slots + packaging/PCB/test | $50k | $15k per 100 chips (via snippet) + ESTIMATE |
| 11 | Collaborator subawards (student time, DDR5 access) | $60k | ESTIMATE |
| 12 | IP: 3 provisionals + 1 PCT | $45k | ESTIMATE |
| 13 | Two founders, lean ($75k/yr each × 2 yr) | $300k | ESTIMATE |
| 14 | Lab rent, insurance, travel (JEDEC/OCP) | $60k | ESTIMATE |
| 15 | Contingency (~8%) | $70k | |
| | **Total** | **$943k** | |

### 7.3 Timeline (24 months)

| Month | Milestone |
|---|---|
| 0-2 | Rigs up; module population procured; collaborator subaward signed |
| 2-6 | Retention, latching, cluster and margin campaigns; VRT soak running (steps 3-8) |
| 6 | **GO/NO-GO #1** |
| 4-12 | Controller RTL on Agilex; CXL IP path resolved by month 6 |
| 8 | sky130 submission (chips ~month 16) |
| 12-16 | 1,000 h soak (~6 weeks per board run, staggered) |
| 16-19 | Flag-latch and counter silicon measured |
| 18 | Contract spec v0.9; DDR5 cross-check complete |
| 20-24 | Raise package: measured error statistics, soak, spec, IP |

**GO/NO-GO line (from the model).**
- **GO** if both hold:
  - the measured error stream fits the 128-bit side band at the 2e-19/read target with refresh ≥0.5 s at 85 C. That means BCH-12 ≤3.3e-4 with ≤0.4% of error bits in ≥3-bit clusters, or RS-8 ≤5.4e-5 with byte-confined clusters;
  - ≥50% of half-charge (margin) errors are flaggable at a ≤0.5 σ window.
- **NO-GO** if any of these holds:
  - the largest safe interval is <256 ms at 65 C even with RS-8;
  - >10% of error events span more than one byte;
  - <25% of margin errors are flaggable.
- **Revival condition:** re-run the identical test on oxide (IGZO) cells, whose retention tail sits 1e3-1e4x to the right.

---

## 8. IP landscape

**Patents to watch.**
- **Micron ECC-relaxed-refresh family:** US 7,447,974; 7,428,687; 7,447,973; 8,689,077; 9,064,600. This is foundational prior art. Check expiry; the early members date from the mid-2000s.
- **Elpida US 7,493,531:** error-rate-driven refresh period.
- **Qimonda US 7,975,170:** per-page refresh.
- **US 8,898,544:** static weak-cell maps used as ECC erasures. It blocks "erasure from a stored map", but not per-read SA timing.
- **US 10,691,532:** strong-ECC scrubbing for DRAM retention.
- **Micron analog row-activity accumulators:** US 10,964,378; US 11,568,918; US 10,943,636. These cover the analog hammer counter core. A reset-on-REF, no-leak variant still needs a freedom-to-operate opinion.
- **US 12,488,827:** CXL device with a command-counting refresh controller.
- **SanDisk/WD soft-bit sensing family:** US 11,907,545; 11,971,829; 11,971,826; 11,901,019; 12,057,188. Longer-discharge second sense plus on-die soft-data compression is the NAND analogue of the DRAM flag. Claims are NAND-specific per the snippets, but claim language must be checked.
- **US 8,458,568:** compression funds ECC.
- **US 11,347,650:** lossy controller.
- **JEDEC PRAC/RFM:** standard-essential patents under FRAND.

**What to file** (3 provisionals by month 6, PCT by month 18):
1. **DRAM sense-amp reliability flag.** A time-delayed second sample or slow-resolution detector per SA; a burst-level flag transfer protocol (side-band or repurposed ECC beats); and its use by a controller Chase/GMD decoder with a bounded flag count. This is the strongest novelty: no DRAM analogue was found.
2. **Raw-BER device grade and test method.** A device characterised by raw BER, cluster-size spectrum per codeword and VRT growth rate at a stated refresh interval and temperature; binning and test flow; a controller that selects code type (binary vs symbol) and refresh interval from the grade. This is the JEDEC route.
3. **Latching-aware relaxed refresh.**
   - temperature-tracking interval;
   - scrub scheduling sized to VRT growth;
   - RFM/PRAC substitution for REF-hosted TRR;
   - graceful degradation when a chip is marked dead.

   The novelty is in the combination and the latching-aware scrub. The base idea is old.
4. **Typed pages in a CXL memory device.** Host-visible page classes mapped to device code classes: exact (BCH/RS), regenerable (CRC-only plus a recompute interrupt), lossy-bounded (fixed-rate).
5. **Tier-orthogonal codeword mapping for 3D DRAM.** Low priority until a 3D cell exists; file as a continuation later.

---

## 9. Open gaps

1. **DDR5 raw access.** DRAM Bender showed no DDR5 support, and DDR5 on-die ECC generally cannot be disabled [UNVERIFIED]. Post-on-die statistics are therefore what a product sees. The model predicts an internal limit of 1.7e-4 behind SEC, and that needs measuring.
2. **The retention tail at 85 C, 0.5-2 s, on current 1α/1β parts is unmeasured here.** The three models span 0.72-3.6 s for the iid case. RAIDR-era anchors are 2009-2012 silicon.
3. **No VRT growth rate was found in snippets.** The model sweeps 0.1-100/day.
4. **Cluster spectrum per codeword is unknown,** and it dominates code choice (§1, point 3). Sub-wordline and MAT faults could produce multi-byte clusters that neither code handles.
5. **The half-charge emulation is a proxy.** Truncated tRAS is not a smaller capacitor: bitline coupling and offset statistics differ. The new-cell flag share must be re-measured on MARGIN STACK silicon.
6. **The cost of the CXL Type-3 IP license** (~€192k list) could consume Phase 2. A partner or an emulation path must be locked by month 6.
7. **Self-refresh cannot be stretched** on commodity parts. Idle savings need controller-issued REF in power-down. The background-power delta is not modelled.
8. **Hammer under relaxed refresh** with partially restored or retention-weakened victims (DejaVu, PaCRAM) is a security risk. It must be measured, not assumed safe via RFM.
9. **The decoder energy and latency figures** (0.05 pJ/bit fast path, 1 pJ/bit page) are estimates. No 28 nm silicon figure was found.
10. **Standards adoption** (OCP/CXL/JEDEC) is outside physics. It is the scale path, not a kill criterion.
