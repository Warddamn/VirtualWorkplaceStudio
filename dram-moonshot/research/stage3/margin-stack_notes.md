# MARGIN STACK: research notes

**Agent:** `dos-margin-stack` · **Date:** 2026-11-02 · **Model:** `models/margin-stack.py` (output in `research/stage3/margin-stack_model_output.md`) · **Sources:** `research/sources/dos-margin-stack.jsonl` · **Assumptions:** `research/assumptions/dos-margin-stack.md`

**Evidence grade.** I used all 6 of my WebSearch calls and no WebFetch. Every new web fact comes from a search snippet [REPORTED]. Facts carried over from earlier agents' logs are marked CROSS-REFERENCE in the source log. Prior knowledge without a URL is tagged [training knowledge]. My own arithmetic is tagged [ESTIMATE] and lives in the model.

---

## 0. Bottom line

MARGIN STACK survives the physics, but the model changes which lever carries it.

- **CDS is load-bearing, not the stretch.** With a realistic 32-cell segment (1.48 fF, not 1.0 fF), a same-step oxide gain FET (σVt ≈ 47 mV from Pelgrom at AVT 2.5 mV·µm), data-dependent coupling and wordline kick, local gain + ECC *without* CDS needs **1.8 fF**: a 3.1x cut, not 10x. Four parallel gain pillars bring that to 0.60 fF at +9% array area. With CDS the sensing-limited cell is **0.14 fF** (central), with a range of 0.09–0.32 fF.
- **Once CDS works, retention sets the capacitor, not sensing.** The planning point is **0.5 fF**: a 10.8x cut, a 120 nm stub (AR 5.7 instead of 62), and 1,561 stored electrons instead of 17,762. At that size, a 1-in-1e10 IGZO leakage tail must be ≤586 aA at 85 °C to match DDR5's 64 ms refresh, and ≤59 aA for a 10x refresh cut.
- **Two new physics terms.** (1) **Wordline kick-back** on a ~1.7 fF local node is ~46 mV, 20x what it is on a 35 fF bitline, so it needs dummy-edge compensation. (2) **A bias conflict.** The same-step gain FET inherits the access FET's high Vt, so it needs a pulsed read-source line or a back gate.
- **Erasure flags buy ~4% of margin, not 2x.** With Gaussian noise, a flag window that catches 83% of errors also flags ~4x as many correct bits. Against BCH t=8 it raises the allowed raw BER only from 1.0e-4 to 1.4–1.7e-4, and it does not shorten the code. The iid criterion that matters is the **same-codeword pair fraction**. At 1% pairs the allowed raw BER falls to 6.3e-5; at 10% it falls to 1.7e-5.
- **$/bit is flat** (−3% to +4%). Density is 0.70 Gb/mm² (1.57x 1-beta, −8% against plain 4F² VCT). The win is the capacitor module: ~10x less HAR etch depth (PFAS, helium-cooled chuck hours), no support lattice, ~100x less ALD exposure, no push to k>50 or Ru, ~2.3x lower array energy per access [ESTIMATE], and a 3D-tier capacitor that falls from 450 to 63 nm, so 3D breaks even at ~10 tiers.
- **Decisive experiment:** one 22FDX MPW plus IGZO coupons plus a DRAM Bender study: **$675k of experiments, $955k with two lean founders, GO/NO-GO at month 16–17.**

---

## 1. Corrections to the Stage 3 concept text

| Concept claim | Model finding | Section of model output |
|---|---|---|
| Base case "local gain + ECC" gives 0.54 fF (Cseg 1.0 fF, 40 mV) | Reproduced exactly (row F). With Cseg 1.48 fF, σVt 47 mV, α=0.1 coupling and kick, it becomes **1.77 fF** without CDS, or 0.60 fF with a 4-pillar gain FET | §3 |
| CDS is the [SPECULATIVE] stretch to 0.13–0.25 fF | CDS is required to reach ≤0.5 fF. Central residual 5.0 mV gives 0.14 fF; pessimistic (11.6 mV, α 0.15) gives 0.32 fF | §2, §3 |
| Coupling is a fixed 20 mV | Data-dependent BL-BL coupling scales with the neighbours' signal, so it is a fractional loss (1−2α). At α=0.1 that is 20% of the signal | §2, §10 |
| WL kickback adds ~2 mV (Stage 2 I-05218 critic) | True on a 35 fF line (2.3 mV). On the 1.73 fF segment it is **46 mV mean**, plus a 7 mV data asymmetry ('0' turns on harder). After 90% dummy-edge cancellation, 8.1 mV deterministic + 2.4 mV random remain | §2 |
| Erasure flags: known-location errors cost half the parity | Under Gaussian noise the best window flags 83% of errors plus 3.9x as many correct bits. Margin gain 1.04x; no shorter code at the 2.3e-17 target | §4 |
| Go needs ≥80% of errors flagged | Secondary. Go needs **<1% same-codeword pairs** and iid singles | §4, §12 |
| Retention 0.8–81 s at 1–100 aA; ~6 ms at 13 fA (0.54 fF) | Those figures use a 150 mV droop. At the concept's own 0.425 V signal convention (75 mV droop) they halve: 3.1 ms at 13 fA. The droop-optimised CDS case recovers a lot (0.5 fF can droop 370 mV → 1.8 s at 100 aA) | §5 |
| Charge-transfer pre-sense reaches 0.5 fF on an unchanged 512-cell line (N-04) | Only if its BL-referred residual is ≤~1.6 mV, because any BL-referred error costs Cbl × δV = 35 aC/mV of charge. At 3 mV it gives 0.91 fF | §3 row E |
| Neutraliser at Cn/Cbl 0.5 gives 0.96 fF | 1.26 fF at Vsig 0.425 V, including the amp-offset gain r/(1−r) | §3 row D |

---

## 2. Prior art and who is pursuing it

| Year | Who | What | Relation to MARGIN STACK | Source |
|---|---|---|---|---|
| 2007–08 | IBM (Barth et al.) | SOI eDRAM with a **3T micro sense amp on ~32-cell local bitlines**; 500 MHz random cycle, 1.5 ns latency | The circuit ancestor: local gain per short segment, on Si eDRAM, no CDS, no capacitor co-design | [IBM Research](https://researcher.ibm.com/publications/a-500-mhz-random-cycle-15-ns-latency-soi-embedded-dram-macro-featuring-a-three-transistor-micro-sense-amplifier) |
| 2010s–2020s | Semiconductor Energy Laboratory (SEL) | **DOSRAM**: oxide-semiconductor 1T1C cells with the **sense-amp array stacked under the cell array** (Si SAs, IGZO write FET) | Closest *stacked oxide short-bitline* prior art. The snippets gave no Cs value. SEL's oxide-memory patent estate is the main FTO risk | [US 12,230,314](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12230314); [US 11,694,594](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11694594); [US 11,488,528](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11488528) |
| 2010 | Wilkerson et al. (Intel), Hi-ECC | Strong BCH over large lines cuts eDRAM refresh power ~93% at ~2% storage | ECC-paid margin precedent; nobody has used it to shrink the capacitor | [UIUC reading list](https://courses.grainger.illinois.edu/CS534/fa2021/reading_list/9a.pdf) |
| Shipping | Samsung, SK hynix | Offset-cancellation sense amps; margin = ΔV_BL − (V_OS + coupling) | The 50 mV budget = 7σ × 7.1 mV; with ECC it becomes 26.6 mV | [US 11,763,878](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11763878) |
| Various | Charge-transfer SA family | Pre-sense amplification for small cell capacitance | Global-line lever (N-04); needs ≤1.6 mV BL-referred residual | [US 8,320,208](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8320208) |
| Various | SRAM negative-capacitance bitlines; NC SA patent; Blalock clamped-BL SA | Active bitline-load cancellation | Neutraliser prior art; no DRAM version found | [academia.edu (TVLSI)](https://www.academia.edu/11650472/Statistical_SRAM_Read_Access_Yield_Improvement_Using_Negative_Capacitance_Circuits); [US 8,872,938](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8872938); [IEICE](https://global.ieice.org/en_transactions/Author/a_name=Travis%20N.%20BLALOCK) |
| 2024-12 | Kioxia + Nanya | **OCTRAM** 275 Mb, 4F² vertical IGZO on a HAR capacitor; Ion >15 µA, Ioff <1 aA | Target platform; keeps the HAR capacitor | [BusinessWire](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology); [Blocks & Files](https://blocksandfiles.com/2024/10/22/kioxia-developing-new-dram-scm-and-nand-tech/) |
| 2025-12 | Kioxia | 3D OCTRAM: 8-layer horizontal IGZO, Ion >30 µA, Ioff <1 aA, no retention published | 3D-tier platform for the stub | [Kioxia](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html) |
| 2026-02 / 04 | Samsung | 16Gb 4F² VCT DRAM at ISSCC 2026; 10a IGZO VCT working die with W2W-bonded periphery; MP target 2028, but the CTO gave no schedule in Oct 2026 | Target platform; the snippets show no capacitor cut | [SemiWiki](https://semiwiki.com/forum/threads/isscc-2026-samsung-electronics-demonstrated-a-16gb-dram.24808/latest); [TrendForce](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/); [Sammy Fans](https://www.sammyfans.com/2026/10/22/samsung-sk-hynix-micron-cxmt-4f2-dram-technology/amp/) |
| 2026-06 | SK hynix | Vertical-gate 4F² with **bitline shielding** (VLSI 2026 late news) | Shielding attacks α directly, which helps this concept | [VLSI 2026 tipsheet](https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-NO-IMAGES-4.24.26.docx) |
| 2018–2025 | ETH SAFARI | SoftMC; reduced-VPP RowHammer; **PaCRAM**: partial charge restoration on 388 DDR4 chips, preventive-refresh latency −64% | The method to emulate reduced cell charge on real DRAM (the Bender study) | [SoftMC](https://arxiv.org/pdf/1805.03195); [arXiv 2206.09999](https://arxiv.org/pdf/2206.09999); [PaCRAM](https://www.arxiv.org/pdf/2502.11745) |
| 2016–2025 | BGU/Bar-Ilan, EPFL, Georgia Tech, UT Austin | Gain-cell eDRAM macros, retention statistics, oxide 3T eDRAM | Circuit collaborators | [BGU 2025](https://cris.bgu.ac.il/en/publications/a-16-kb-65-nm-gc-edram-macro-with-internal-bias-voltage-generatio/); [GT](https://hg.gatech.edu/node/675050); [UT Austin](https://sites.utexas.edu/CRL/files/2021/05/IGZO_eDRAM_CIM_ISCAS_2021.pdf) |
| Decades | CMOS image sensors | Pinned photodiode + source follower + **CDS** reads a few-hundred-electron packet with a few e- of noise | The conceptual source of the CDS lever [training knowledge] | — |

**Novelty verdict.** Every part is known. What has not been published (no hit in the snippets) is the *co-designed* stack. It has four parts: a same-step oxide gain FET per segment, CDS through that same FET, dummy-edge kick compensation, and a capacitor sized to the post-CDS residual.

---

## 3. Best demonstrated numbers for each component

| Component | Best demonstrated | MARGIN STACK needs | Gap |
|---|---|---|---|
| Local gain per short bitline | IBM 3T micro-SA, ~32 cells/LBL, 1.5 ns latency (Si SOI) | Same on an oxide VCT pillar, ~3.6 ns sense+restore (model §9) | Oxide gm, Vt and bias (pulsed source) |
| Oxide access FET | OCTRAM Ion >15 µA, Ioff <1 aA; 3D OCTRAM Ion >30 µA | 1-in-1e10 tail ≤586 aA (parity) / ≤59 aA (10x refresh) at 0.5 fF, 85 °C | Tail not published; "<1 aA" is likely median/extracted |
| Oxide FET Vt stability | imec H+O anneal: ~30x less H-doping under PBTI, 1.2 V overdrive for 5 yr at 95 °C ([imec](https://imec-publications.be/handle/20.500.12860/59908)) | Gain-FET drift handled by CDS; access-FET drift sets the leakage | OK in principle |
| Oxide gain-cell retention | imec >200 s at 95 °C, >1e12 cycles (EDL 2025); IMECAS 4-tier, 3 b/cell, 400 s (A3) | ≥1 s worst-cell at 85 °C | Array-tail data missing |
| Oxide FET mismatch (AVT) | **Not found** (search 2026-11-02) | ≤~50 mV for 1 pillar (CDS cancels it anyway), but gain spread must keep a −4σ FET at ≥50% gm | Biggest unsourced number |
| Post-auto-zero comparator offset | ~3 mV [ESTIMATE, system inventor] | ≤3–6 mV | Standard |
| Capacitor | 1β ~5.4 fF at ~1.3 µm, AR ~62, EOT ~0.55 nm (A1) | 0.5 fF at ~120 nm, AR ~6 | Easier, not harder |
| Raw-BER ECC | DDR5 on-die SEC; Hi-ECC strong BCH | BCH t=8 per 512 b; failure 2.3e-17 at 1e-4 | Pair fraction unmeasured |
| Partial-charge emulation on real DRAM | PaCRAM: 388 DDR4 chips, −64% restore latency | Error maps at raw BER 1e-5 to 1e-3 | Method exists |
| Bonding (for the 3D/merchant variants) | imec W2W 300 nm pitch (ECTC 2025, A3) | Not needed for in-array gain | — |

---

## 4. Model headline numbers (`models/margin-stack.py`)

- **Residual budget (central, 85 °C):** 1/f+RTN 4.0 mV [SPECULATIVE] ⊕ comparator 1.9 mV ⊕ sampling kTC 0.3 mV ⊕ kick (random) 2.4 mV = **5.0 mV rms**, plus 8.1 mV deterministic and a 20% coupling loss.
- **Required Cs:** 1.77 fF (no CDS, 1 pillar); 0.60 fF (no CDS, 4 pillars); **0.14 fF** (CDS central); 0.32 fF (CDS pessimistic). Thermodynamic floor 0.024 fF.
- **Thresholds (α = 0.1):** σ_res ≤ **20.5 mV** gives Cs ≤ 0.5 fF; ≤10.6 mV gives ≤0.25 fF; >34 mV keeps Cs ≥1 fF.
- **Retention at 0.5 fF** (75 mV droop): 20.9 s at 1 aA, 3.5 s at 10 aA, 372 ms at 100 aA, 37 ms at 1 fA. The dielectric at 1e-8 A/cm² caps any size at ~47 s.
- **Refresh power, 16Gb die:** 12.2 mW (1β, 64 ms) vs 0.43 mW (0.5 fF, 100 aA tail, droop optimised, 2x guard), a 28x cut.
- **Array energy per sensed bit:** 20.1 fJ (1β) vs 8.8 fJ [ESTIMATE, C_GBL 6 fF].
- **Area/cost:** +12.5% array area (3T + strap per 32 cells), die +8.8%, 0.70 Gb/mm². $/GB $1.44–1.53 against the $1.48 anchor, depending on the capacitor-module share (10–20%).
- **3D:** lateral capacitor 450 → 63 nm at 0.5 fF; per-tier density 2.8x A1's base; 9.8 tiers to match 1β (A1 base ~26).
- **Segment length:** 32–64 cells is the sweet spot (16 cells costs 17.5% of die for little Cs gain).

---

## 5. U.S. facilities that could build the demo

**MPW / shuttles**
| Route | Process | Price / terms | Use | Source |
|---|---|---|---|---|
| GF 22FDX via CMC (Canada) | 22 nm FD-SOI | **$24,075/mm²** (1 mm² min, academic) or **$17,997/mm²** (4 mm² min); a 6.02 mm² design was $108,342 with 100 untested dies (run 2602DJ, early 2026) | Main MARGIN STACK chip | [CMC](https://www.cmc.ca/globalfoundries-22fdx-fdsoi-22-nm-process/); [CMC listing](https://products.cmc.ca/Fabrication/DMT_Fab) |
| GF via MOSIS 2.0 (USC ISI) | GF nodes; 12–350 nm across partners | GF value-added partner agreement (2026-07); pricing not found | U.S. route to the same shuttle | [ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/); [AAC](https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy) |
| EUROPRACTICE | Many | 2026 schedule published; 22FDX price not in the snippet; U.S.-startup eligibility unclear | Fallback | [EUROPRACTICE](https://europractice-ic.com/schedules-prices-2026/) |
| ChipFoundry SKY130 | 130 nm | $15k per 100 chips (raised from $10k) | Cheap early pass for the CDS/BIST architecture; mismatch not representative | [eeNews](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/) |
| wafer.space GF180MCU | 180 nm | Full slot up to 1,000 dies; Run 1 back after ~12 weeks | Test-board controllers, charge-injection DACs | [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2) |

**University nanofabs (IGZO FET + MIM coupons)**
| Facility | Rate info | Why | Source |
|---|---|---|---|
| Stanford SNF | FY20: **$135/h industry, $50/h academic** base rate, monthly soft cap, 25% of base above the cap; SNF/SNSF merging | Oxide ALD/sputter, H.-S. P. Wong's oxide/3D memory group nearby [training knowledge] | [FY20 sheet](https://snfguide.stanford.edu/sites/default/files/sections/diplayfiles/fy20ratesheets-labuse.pdf); [rates page](https://nanolabs.stanford.edu/snfrates) |
| Purdue Birck | 2023 recharge in 3 tiers (internal / external academic / for-profit); daily lab fee **$14 / $44 / $51** | Peide Ye's ALD In₂O₃/IGZO FETs [training knowledge] | [Birck FY24 PDF](https://mailman.ecn.purdue.edu/archives/list/bnc-all@ecn.purdue.edu/message/QV6GR6XQBKTW7PU5OCDG7VQOPHRKJ2JN/attachment/6/BRKFY24RatesvsCurrent.pdf) |
| Georgia Tech IEN | Not searched | Shimeng Yu (oxide eDRAM), Suman Datta (BEOL oxide FETs) [training knowledge] | [GT](https://hg.gatech.edu/node/675050) |
| Cornell CNF | No public rates found; NSF NNCI, 5-yr $7.5M renewal | Strong e-beam and ALD | [Cornell](https://as.cornell.edu/index%2Ephp/news/nanotech-facility-gets-5-year-75m-renewal-nsf) |
| MIT.nano, Penn Singh, ASU, UT Austin | Not searched | Backups; UT Austin has IGZO eDRAM circuit authors | — |

**National-lab user facilities** [training knowledge: DOE NSRC user time is generally no-cost for non-proprietary work that will be published, and cost-recovery for proprietary work; verify per facility]. Sandia/LANL **CINT**, Argonne **CNM**, ORNL **CNMS**, LBNL **Molecular Foundry**: PEALD of IGZO/ZrO₂, TEM cross-sections of stubs, variable-temperature electrical work. NIST **CNST** NanoFab: fee-based, open to companies. Sandia **MESA** is not an open user facility; access is through CRADA or Strategic Partnership [training knowledge].

**Test.** Our own bench (FPGA + SMUs + thermal forcer). The ETH SAFARI open-source FPGA DRAM testers (SoftMC; its successor DRAM Bender [training knowledge]) for the error study. aA leakage is measured by the integration (droop) method through a 2T read structure, not by direct current.

---

## 6. Collaborators and recruits

- **Device/circuit co-founder profile:** a DRAM sense-amp designer, or a **CMOS image-sensor readout designer** (CDS, column ADC, source-follower noise, Monte Carlo tails). The CIS skill set maps one-to-one onto the key unknown. Pools: ex-Micron Boise DRAM design; U.S. image-sensor teams [training knowledge].
- **Advisors:** the IBM eDRAM micro-SA authors (Barth et al.) for local-bitline circuit lore.
- **Academic partners:** ETH SAFARI (O. Mutlu) for the Bender/PaCRAM-style study; Georgia Tech (S. Yu, S. Datta) and Purdue (P. Ye; K. Roy for circuits) for oxide FETs and IGZO coupons; Stanford (H.-S. P. Wong) for oxide 3D memory; the BGU/Bar-Ilan gain-cell eDRAM group and EPFL (A. Burg) for retention statistics; UT Austin IGZO eDRAM authors. [Names are training knowledge, except the institutional links in §2.]
- **Industrial counterparties (licensees):** Kioxia/Nanya (OCTRAM), Samsung (VCT, VS-DRAM), SK hynix (VG 4F² with shielding), Micron (reportedly skipping 4F², per Sammy Fans; a possible 3D-tier licensee), CXMT (excluded by U.S. policy).

---

## 7. Decisive experiment

**Question.** On silicon that emulates an oxide 4F² segment, is the post-CDS input-referred residual ≤~20 mV (Cs ≤0.5 fF) under worst-case data at 85 °C? Are the errors iid singles (<1% same-codeword pairs)? And is the IGZO leakage tail ≤586 aA (≤59 aA for a 10x refresh cut)?

**Step by step**
1. **M0–4. Simulation and TCAD.** Run SPICE Monte Carlo on the 22FDX PDK, plus a VCT/IGZO compact model fitted to published OCTRAM Ion/Ioff. Use TCAD (via a partner) for GAA channel-charge partition (the kick) and BL-BL α on VCT geometry, with and without shields. *Exit:* simulated σ_res ≤10 mV, α ≤0.1 with shielding.
2. **M0–6. DRAM Bender study** (shared with RAW-BER CONTRACT). Emulate reduced charge on DDR4/DDR5 from three vendors with truncated restore (PaCRAM method), reduced VPP and stretched refresh. Map raw BER from 1e-5 to 1e-3 at 45–95 °C. Log the **error multiplicity per 512-bit row codeword** (pair fraction c) and the reduced-tRCD flag proxy (flaggable fraction f). *Exit:* c <1%.
3. **M2–7. MPW design (22FDX, ~6 mm²).**
   - (A) 64k segments × 32 cells (2.1M cells), in four Cs quadrants built from custom MOM stubs (0.125/0.25/0.5/1.0 fF). Thick-oxide access FETs; LBL dummy loads giving Cseg 0.8 or 1.5 fF (16- and 32-cell variants). 3T local amp with a minimum-size gain FET (σVt ~40–50 mV, emulating VCT) and a 4-finger variant. Pulsed read-source line; dummy-WL kick compensation switchable on/off.
   - (B) Global CDS: a sampling pair, an auto-zeroed comparator, a delayed second compare as the flag, and a trim DAC for centring.
   - (C) Aggressor control: all-0, all-1, checkerboard and stripe patterns; interleaved/shielded activation on/off.
   - (D) 64 emulated 35 fF global lines with 0.25–5 fF stubs, charge-transfer pre-sense, and a neutraliser (Cn/Cbl 0.3–0.8) with a stability monitor.
   - (E) BIST: per-cell margin sweep via a calibrated charge-injection C-DAC on each LBL, per-row/column error counters, SPI to an FPGA.
   - (F) Monitors: matched-FET arrays (AVT) and MOM capacitance/spread structures.
   - *Note:* Si access FETs leak far more than IGZO, so the MPW reads immediately after write. The leakage tail comes from the coupons.
4. **M7–11.** Fabrication (~12 weeks), packaging, boards.
5. **M3–12. IGZO coupons** (shared oxide run). Planar IGZO FETs at the smallest lithographic sizes; 0.5 fF-class ALD ZrO₂/HfO₂ MIM; 2T read structures (storage node on a read-FET gate) holding ≥1,000 cells. Measure droop over 10³–10⁵ s at 25–110 °C and fit a lognormal to extrapolate the 1e-10 tail. Measure IGZO 1/f and RTN spectra, and run a discrete CDS on IGZO gain FETs with an external low-noise sampler. This gives the oxide 1/f term that Si cannot emulate.
6. **M11–16. Test.** Per-cell margin maps on 20 chips (42M cells; direct tail to 5.5σ). Measure raw BER vs Cs at 25/85/110 °C × patterns × CDS on/off × kick compensation on/off × shield on/off. Extract σ_res, the deterministic offset D and α. Collect codeword multiplicity, flag statistics and a neutraliser stability map.
7. **M16–17. GO/NO-GO.** Combine the Si σ_res with the oxide 1/f term from the coupons to get the projected oxide-VCT σ_res, and test it against the thresholds below.
8. **M17–24.** Second spin (16-cell variant, improved kick compensation), data room, PCT filings, $10–50M raise.

**GO/NO-GO (from the model).**
- **GO** if all three hold:
  - post-CDS residual ≤**20 mV** at 85 °C under worst-case neighbour data, i.e. raw BER ≤1e-4 at Cs = 0.5 fF for iid errors (≤1.4e-4 if ≥80% of errors are flaggable; ≤11 mV unlocks 0.25 fF);
  - <1% of errors arrive as same-codeword pairs;
  - the IGZO 1-in-1e10 85 °C leakage tail is ≤**586 aA** at 0.5 fF (≤59 aA for a 10x refresh cut).
- **NO-GO** if the residual is >34 mV (Cs ≥1 fF, a ~5x cut that a 4-pillar gain FET without CDS already gives), or if pairs exceed ~10% of errors.

**Budget (standalone, ≤$1M, 24 months)**
| Item | $ | When |
|---|---|---|
| DRAM Bender error-tail study (2 FPGA boards, DDR4/5 parts, thermal rigs, 0.5 FTE × 6 mo) | 80,000 | M0–6 |
| Pre-silicon SPICE MC + TCAD access | 30,000 | M0–4 |
| 22FDX MPW ~6 mm² at $17,997/mm² + 20% U.S.-route premium | 130,000 | tape-out M7 |
| EDA/PDK access | 25,000 | M2–7 |
| Layout/verification contractor | 45,000 | M3–7 |
| Packages, PCBs, sockets, probe cards | 30,000 | M9–11 |
| Test bench (SMUs, thermal forcer, FPGA, low-noise sampler) | 60,000 | M6–11 |
| IGZO FET + 0.5 fF MIM coupons (~400 cleanroom h at ~$135–150/h, staff assist, materials, 2T readout) | 120,000 | M3–12 |
| Second MPW spin (contingent) | 110,000 | M15–22 |
| IP: 2 provisionals, 1 PCT, FTO search | 45,000 | M2, M10, M14 |
| Two founders, $5k/month each × 24 months | 240,000 | M0–24 |
| Overhead (insurance, travel, accounting, legal) | 40,000 | M0–24 |
| **Total** | **955,000** | headroom $45k |

In the portfolio plan (FINAL_CONCEPTS.md), the Bender study ($80k) and the oxide coupon run (~$150k) are shared with RAW-BER CONTRACT, PIXEL-STACK, DIODE-TOWER and CHARGE-RIVER. That puts MARGIN STACK's incremental cost at ≈ the ~$275k MPW line plus test bench. The MPW also reads the other concepts' coupons.

**Timeline**
| Month | 0–3 | 3–6 | 6–9 | 9–12 | 12–15 | 15–18 | 18–21 | 21–24 |
|---|---|---|---|---|---|---|---|---|
| Recruit, SPICE/TCAD | ■ | | | | | | | |
| DRAM Bender study | ■ | ■ | | | | | | |
| MPW design → tape-out (M7) | ■ | ■ | ■ | | | | | |
| Fab + packaging | | | ■ | ■ | | | | |
| IGZO coupons | | ■ | ■ | ■ | | | | |
| MPW test, margin maps | | | | ■ | ■ | ■ | | |
| GO/NO-GO (M16–17) | | | | | | ■ | | |
| Spin 2, PCT, raise | | | | | | ■ | ■ | ■ |

---

## 8. IP landscape

**Patents to watch**
- **SEL oxide-semiconductor memory (DOSRAM) family:** SA array stacked under OS 1T1C cells ([US 12,230,314](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12230314), [US 11,694,594](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11694594), [US 11,488,528](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11488528)). Broad OS-transistor claims; a formal FTO search is needed before filing.
- **IBM micro-SA family** (Barth, ~2006–08 filings). Likely at or near expiry on a 20-year term [training knowledge; verify]. Expired patents are free prior art.
- **Sense-margin / offset-cancellation SAs:** [US 11,763,878](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11763878); Samsung/SK hynix OCSA families.
- **Bitline load and charge transfer:** [US 8,872,938](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8872938) (NC SA); [US 8,320,208](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8320208) family (charge transfer); [US 12,106,797](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12106797) (Cbl composition).
- **Cell/process:** Kioxia/Nanya OCTRAM and Samsung VCT. We do not claim the cell.
- **Weak-cell erasure maps:** US 8,898,544, cited in Stage 2; not opened here.

**What to file (provisionals at M2 and M10)**
1. **Segmented oxide 1T1C read method.** A same-step vertical gain FET per segment. Sample 1 through that FET after reset, sample 2 through the same FET after charge sharing, compare. Claim Cs < Cseg (e.g. Cs ≤ 0.5·Cseg) and capacitor height ≤ ~10x pillar diameter.
2. **WL kick-back compensation for short segments** (new in this dossier). A complementary dummy-WL edge timed between the samples, or a reference sample taken after a dummy edge, plus per-mat trim of the data-dependent asymmetry.
3. **Biasing a high-Vt same-step gain FET** through a pulsed read-source line or back gate during the CDS window.
4. **Pair-aware ECC orientation** for segmented arrays. Row codewords across distinct segment amps; flag-driven scrub and weak-cell telemetry.
5. **3D tier:** a ≤100 nm lateral stub capacitor sized to a 16-tier local-gain segment (coordinate with PIXEL-STACK).
6. **DRAM bitline neutraliser with stability control.** File only if the MPW shows a stable Cn/Cbl ≥0.5.

---

## 9. Open gaps

1. **Oxide FET AVT, 1/f and RTN at VCT geometry.** No source found. This is the biggest unsourced input: it sets the 1/f term of the residual and the gain-spread tail.
2. **VCT bitline capacitance per cell.** The ISSCC 2026 snippets gave no circuit detail; Cseg uses 0.04 fF/cell [ESTIMATE].
3. **Kick model.** The GAA channel-charge partition and the data-dependent asymmetry are first-principles only. TCAD plus MPW block (A) measure them.
4. **IGZO leakage tail at the 1e-10 quantile.** Not published; OCTRAM's "<1 aA" is likely a median or an extraction. This decides 0.25 vs 0.5 vs 1 fF.
5. **Capacitor-module share of wafer cost** (10–20%) is unsourced. It decides whether $/bit is −3% or +4%.
6. **Soft errors for a ~1,500-electron cell.** An oxide storage node with no Si junction should collect less charge; unmeasured.
7. **Row hammer in IGZO VCT.** Unknown (A1). Hammer bursts would produce exactly the same-codeword pairs that the ECC cannot absorb.
8. **U.S. pricing for 22FDX MPW** (MOSIS 2.0 or GF direct) is unverified; CMC is a Canadian broker.
9. **Whether the 22FDX PDK can make matched 0.1–0.25 fF MOM stubs.** Check before layout; the fallback is gate-capacitance stubs.
10. **DOSRAM's published Cs and bitline numbers.** Not found. If SEL already runs a ~1 fF oxide cell on short stacked bitlines, the novelty narrows to CDS + kick compensation + the capacitor co-design.
11. **The concept's retention arithmetic** used a 150 mV droop against its own 75 mV signal convention. The FINAL_CONCEPTS text should be corrected.
