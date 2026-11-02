# CHARGE-RIVER: research notes

**Agent:** `dos-charge-river` · **Written:** 2026-11-02 · **Concept rank:** 7 (EV 40) in `research/stage3/FINAL_CONCEPTS.md`
**Model:** `models/charge-river.py` (stdlib; `python3 models/charge-river.py` from `dram-moonshot/`, exits 0) → `research/stage3/charge-river_model_output.md`
**Sources:** `research/sources/dos-charge-river.jsonl` (41 entries; 6 new web searches this turn, the rest reused from C0/S2/ram-venture logs). **Assumptions:** `research/assumptions/dos-charge-river.md`.
Tags: [VERIFIED] primary source opened · [REPORTED] search snippet or secondary · [ESTIMATE] my computation · [UNVERIFIED] training knowledge, not confirmed this session.

---

## 0. Bottom line

1. **The physics floor is CTE ≈ 0.997 per transfer, not 0.999.** A regenerated binary packet does not need 91% survival. It needs an eye that clears ~6.1σ for raw BER ≤ 4.9e-10 (BCH t=2/512 b, 10 FIT per 16 Gb die). With 313-electron packets, 98 transfers per segment, 8 e- read noise, a 1.5x worst-string factor and a 10% DFE residual, the minimum median CTE is **0.9970 with DFE** and **0.9979 without** (model §4). The chief's 0.999 stays the STRONG-GO line, because it buys margin against worst strings or 64-stage segments. DFE helps less than the concept claimed: binomial partition noise, N_s·h0·(1−h0), grows as charge is deferred, and no correction removes it.
2. **Everything hinges on one ambiguous number.** imec's IEDM 2024 planar IGZO CCD reports "CTE >98%" ([imec, 2024-12](https://imec-publications.be/handle/20.500.12860/59420)) [REPORTED]. If that is per transfer, CHARGE-RIVER needs a ~7x cut in deferral (model §5). If it is end-to-end over 142 bits × 4 phases, the per-transfer CTE is 0.99996, and the device already clears the floor with ~80x margin. **Buying the paper (~$35) is step 0 of the decisive experiment.**
3. **Do not "refresh by circulation."** Continuous lapping at 50 MHz makes ~1.6e6 decisions per bit per second (~5e4x the decode read rate) and ~8e15 plate cycles over 5 years. The design that works is **park-and-shift**: packets sit still (imec: >200 s retention), lap only when read, and get a scrub lap every ~20 s. Scrub power is then ~0.06 mW per 16 Gb die against DDR5's ~11.5 mW refresh (~190x lower) (model §3, §8, §9).
4. **The hard corner is fast and *cool*.** With SRH emission, the traps that steal charge sit at depth E_w = kT·ln(ν0·t_dwell). A 50 MHz stage clock at 85 °C probes traps only ~14 meV shallower than imec's 6.25 MHz room-temperature point, but at 25 °C it probes ~46 meV shallower, into the denser band tail (model §5). The experiment must report CTE at 25 °C as well as 85 °C.
5. **Schedulability is about lead time, not predictability.** An address only has to be known *one lap* (0.64 µs at 50 MHz) ahead. A decode layer takes tens of µs, so routed experts and top-k KV are mostly schedulable. The binding term is the truly random floor. At 0.5% (dense decode), even imec's 4-6 MHz meets a 40 ns average. At 2% plus µs lead times (MoE + sparse attention), 4-6 MHz gives 0.7-1.5 µs and 50 MHz gives ~26 ns (model §7).
6. **Headline numbers** (model §2, §8, §11): 64 bits per hole, **1.62 Gb/mm² user (3.6x 1-beta)**, **~$0.71/GB (2.1x below the $1.48/GB DDR5 cost)**, 313 e- packets (167 mV at a 0.3 fF floating diffusion), ~0.07 pJ/bit core read, 6.3 TB/s peak per die. The NAND-price cross-check gives ~$0.84/GB. **The cost step is ~2x, not 10x**, because a CCD hole stores 64 bits where a TLC NAND hole stores ~600.

---

## 1. Concept in one paragraph

A 3D-NAND-like stack of ~200 W/SiO2 plates (40 nm pitch) has one hole etch, ALD gate dielectric and an ALD oxide channel. The plates are clocked in 3 phases, so electron packets shift along the hole like a vertical CCD: no transistor, capacitor or contact per bit, and no staircase, because 3-6 clock lines replace per-plate word lines. CHARGE-RIVER adds: a buried oxide heterochannel (IGO/IGZO or Ga-free ITZO/ZTO), fat zero, decision-feedback correction of deferred charge at the sense node, regeneration every ≤32 stages (implemented here as a sense node at **both** ends of each hole), and a SOAP-style placement compiler plus SRAM front buffer that schedule LLM weights and KV so packets arrive just in time.

---

## 2. Prior art and who is pursuing it

| Thread | Who / what | Date | Status and key numbers | Source |
|---|---|---|---|---|
| Oxide CCD memory (planar) | imec: IGZO 4-phase 142-bit CCD buffer memory | IEDM 2024-12 | CTE >98% (definition unclear), retention >200 s, >1e10 cycles without degradation, >6.25 MHz | [imec pubs](https://imec-publications.be/handle/20.500.12860/59420) [REPORTED] |
| Oxide CCD memory (3D) | imec: first vertical IGZO CCD, 3 word lines as phase gates, punch-and-plug, ALD IGZO | IMW 2026 | >4 MHz transfer, "a few thousand" electrons per packet; next: more word lines, better readout; quote from Maarten Rosmeulen | [EE Journal](https://www.eejournal.com/industry_news/imec-demonstrates-the-first-3d-implementation-of-a-charge-coupled-device-for-ai-memory-applications/), [Silicon Semiconductor](https://siliconsemiconductor.net/article/124234/Imec_demonstrates_the_first_3D_implementation_of_a_charge_coupled_device_for_AI_memory_applications) [REPORTED] |
| Positioning | imec: block-addressable CXL type-3 buffer, "~5x the bit density of 2D DRAM expected in 2030" (company claim) | 2026 | One outlet reports ">4 GHz", which is almost certainly an error for 4 MHz | [eeNews](https://www.eenewseurope.com/en/imec-taps-ccd-for-3d-cxl-memory-in-data-centres), [TechSpot](https://www.techspot.com/news/112437-researchers-unveil-nand-dram-hybrid-could-outperform-traditional.html) [REPORTED] |
| CCD block-memory architecture | Univ. Jyväskylä MSc thesis: RTL emulation of 3D IGZO CCD block memory | 2025 | Bidirectional shifting cuts latency and energy ~20% vs cyclic | [JYX](https://jyx.jyu.fi/handle/123456789/105533) [REPORTED] |
| 1970s CCD main memories | Intel 2416 (16 kb), Fairchild F464 (64 kb) | 1975-79 | Died to DRAM on serial latency and silicon dark current | [UNVERIFIED: training knowledge] |
| Modern Si CCDs | MIT Lincoln Lab (Lynx x-ray CCDs) | 2019, 2024 | 4.6 e- read noise at 2.5 MHz; narrow 0.8 µm buried-channel trough implants improve transfer; CTE degrades on cooling from −30 to −60 °C; single-poly gates cut capacitance for speed | [JATIS 2019](https://www.spiedigitallibrary.org/journals/JATIS/volume-5/issue-02/021015/Toward-fast-low-noise-charge-coupled-devices-for-Lynx/10.1117/1.JATIS.5.2.021015.full), [SPIE 2024](https://proceedings.spiedigitallibrary.org/conference-proceedings-of-spie/13103/1310317/Directions-for-advancement-of-MIT-LL-CCDs-for-x-ray/10.1117/12.3020459.full) [REPORTED] |
| Deferred-charge correction | LSST camera (Snyder et al.) | 2021 | Deferred charge from bulk traps is largely modelable; a reverse correction moves it back to its packet | [JATIS 2021](https://spiedigitallibrary.org/journals/Journal-of-Astronomical-Telescopes-Instruments-and-Systems/volume-7/issue-04/048002/Characterization-and-correction-of-serial-deferred-charge-in-LSST-camera/10.1117/1.JATIS.7.4.048002.full) [REPORTED] |
| CTI correction patent | US RE43,639: model-based CTI correction in a charge-domain ADC | ? | Closest patent art to DFE-corrected CCD memory | [USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/RE43639) [REPORTED] |
| Oxide heterochannels | In2O3/IGZO (2DEG-like interface, AEM 2023); ITO/IGZO >61 cm²/Vs; review: band-offset engineering suppresses trapping and improves bias stability; mechanism still debated | 2019-2024 | No buried-channel oxide **CCD** found anywhere | [AEM](https://doaj.org/article/cc5dc9a2a70046a4bc9083b39931ca09), [CAU](https://scholarworks.bwise.kr/cau/handle/2019.sw.cau/59170), [SKKU review](https://scholarx.skku.edu/item/fde13622-0afc-4041-b0c9-2bc148ffea51), [J. Semicond.](https://www.researching.cn/articles/OJ24629ba9f9864632) [REPORTED] |
| Oxide trap kinetics | InHfZnO/HfInZnO TFT transients over 5 µs-5 ms, ~17-24 µs constants; fast (temperature-insensitive) vs slow (activated) charging; SRH capture and emission times depend exponentially on gate voltage | 2017-2022 | The only kinetics data; nothing in the ns window that matters at 50 MHz | [Sci. Rep.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5605542/), [OUCI](https://ouci.dntb.gov.ua/works/4Varq057), [SSE 2022](https://in4.iue.tuwien.ac.at/pdfs/sispad2022/A-dynamic-current-hysteresis-model-for-IGZO-TFT_2022_Solid-State-Electronics.pdf) [REPORTED] |
| Placement for shift memories | IBM 650 SOAP (1950s); ShiftsReduce for racetrack (TU Dresden, TACO 2019: up to 52.5% fewer shifts) | 2019 | Published art: broad "placement for shift memory" claims are dead; LLM-specific lead-time scheduling is not found | [arXiv](https://arxiv.org/abs/1903.03597) [REPORTED] |
| Competing weights tier | SanDisk + SK hynix High Bandwidth Flash: OCP spec Aug-2026, 256 GB/die, 512 GB per 16-high stack, 1.6 TB/s read; samples 2H26 | 2026 | The real competitor for read-mostly weights; KV and write-heavy traffic remain HBM's | [SanDisk](https://www.sandisk.com/company/newsroom/press-releases/2026/2026-02-25-sandisk-and-sk-hynix-begin-global-standardization-of-next-generation-memory-solution-high-bandwidth-flash-hbf), [Sovereign](https://sovereignmagazine.com/article/hbf-open-standard-ai-inference-512gb) [REPORTED] |
| Competing weights tier | Taalas HC1: hard-wired weights in mask ROM plus SRAM KV; AMD agreed to acquire it (Aug-2026) | 2026 | Shows the market values a static-weights tier | [Next Platform](https://www.nextplatform.com/2026/02/19/taalas-etches-ai-models-onto-transistors-to-rocket-boost-inference/) [REPORTED] |
| Alternate device | IBM racetrack (Parkin, 2008) → capacitor-hole racetrack (I-11581) | 2008- | Shift errors <1e-9 at ≤30 nm unshown | Stage 2 critiques [UNVERIFIED] |

**Novelty verdict.** imec owns the device direction: planar 2024 and vertical 2026 IGZO CCD memory. The defensible deltas are: (a) a buried oxide heterochannel CCD, with nothing found; (b) DFE and partition-noise-aware sensing for a CCD *memory*, where the only near art is RE43,639 and LSST; (c) two-ended ≤32-stage strings with park-and-shift control; (d) a lead-time-based LLM placement controller, which is new beyond SOAP and ShiftsReduce.

---

## 3. Best demonstrated numbers by component

| Component | Best demonstrated | Needed by CHARGE-RIVER | Gap | Source |
|---|---|---|---|---|
| Oxide CCD CTE | >0.98 at 6.25 MHz, planar surface channel (definition unclear) | ≥0.997 at 150 M transfers/s, 25 and 85 °C | 0x to 7x | imec 2024 [REPORTED]; model §4 |
| Oxide CCD clock | >6.25 MHz planar; >4 MHz vertical | ≥50 MHz stage (150 MT/s) | 8-12x | imec 2024 / 2026 [REPORTED] |
| Transport limit | n/a | Drift 0.6 ps, diffusion 24 ps across 25 nm | None (traps rule) | model §5 [ESTIMATE] |
| Packet size | "a few thousand" e- (3D, larger features) | ~313 e- at 40 nm plates | Must work 10x smaller | IMW 2026 [REPORTED]; model §1 |
| Retention | >200 s (planar) | ≥20 s scrub interval, ≤0.25 aA per well | Met | imec 2024 [REPORTED]; model §9 |
| Endurance | >1e10 cycles, no degradation | ~1.5e11 plate cycles over 5 yr (park-and-shift) | 15x to demonstrate (1.4 h at 200 MHz) | imec 2024; model §9 |
| Read noise (Si CCD) | 4.6 e- at 2.5 MHz (MIT LL) | ≤8 e- post-CDS at a 0.3 fF oxide SF | Plausible; oxide 1/f unmeasured | JATIS 2019 [REPORTED] |
| Oxide heterochannel mobility | >40 (review), >61 cm²/Vs (ITO/IGZO) | Any; mobility is not the limit | n/a | [REPORTED] |
| Oxide leakage | IGZO Ioff <1 aA (OCTRAM); 2T0C >400 s | ≤0.25 aA per well | Same class | A1 / [EE Journal 2020](https://www.eejournal.com/industry_news/imec-demonstrates-capacitor-less-igzo-based-dram-cell-with-400s-retention-time/) |
| Plate stack | 3D NAND >200 layers in production | 200 plates, 40 nm pitch, AR 80 hole | NAND-class | [UNVERIFIED: training knowledge] |
| Shift placement | ShiftsReduce −52.5% shifts | ≥92% bytes known one lap ahead | Needs LLM traces | arXiv 2019 |
| Weights tier competitor | HBF 1.6 TB/s per stack | — | — | [REPORTED] |

---

## 4. What the model says (all from `charge-river_model_output.md`)

- **Geometry:** 200 plates → 2 segments × 32 stages = **64 bits/hole**; 141 nm hole pitch; slit efficiency 0.70 × periphery 0.75 = 0.53; ECC rate 0.962 → **1.62 Gb/mm² (3.63x 1-beta)**. A 16 Gb die is ~9.9 mm² vs 35.8 mm².
- **Signal/noise:** Cox 6.9 fF/µm²; 0.048 fF per plate per hole; full well 447 e-; signal 313 e- (167 mV at 0.3 fF); read noise 8 e- (4.3 mV); raw SNR 39:1.
- **Reliability:** raw BER ≤ 4.9e-10 per segment read (6.1σ) at 30 reads/s per bit. With continuous circulation it would be 1.3e-11.
- **Minimum CTE (§4):** 0.9970 (DFE) / 0.9979 (no DFE) at 98 transfers. At 194 transfers (64-stage segments): 0.9985 / 0.9989. Packet-size dependence: 150 e- needs 0.9990; 3,000 e- needs 0.9926. Noise sensitivity: at 30 e- read noise the 313 e- packet fails at any CTE, so readout noise is a co-equal spec.
- **Trap transfer (§5):** under the per-transfer reading of imec, surface IGZO at 50 MHz/25 °C lands at 0.56-0.97 depending on the tail slope. A buried channel plus fat zero (assumed 0.18x) brings the flatter-tail cases to 0.992-0.995, "marginal". Under the end-to-end reading, every case passes.
- **Key-unknown sensitivity (§6):** CTE 0.98 → 8 bits/hole, 0.5x 1-beta, $3.86/GB (dead). 0.99 → 0.9x, $2.06/GB. 0.995 → 2.0x, $1.06/GB. **0.997 → 3.5x, $0.72/GB.** ≥0.998 → 3.6x, $0.71/GB (plate-limited). NO-GO boundary (1.5x density): **CTE 0.9934**, ~$1.29/GB.
- **Latency (§7):** at 50 MHz a 32-stage lap takes 0.64 µs, and ≥92.2% of bytes must be schedulable for a 40 ns average. Dense decode: 99.5% → 17 ns. MoE + sparse: 96.7% → 26 ns.
- **Energy/bandwidth (§8):** 90 fJ/bit shift at CV² (45 fJ recycled) + 28 fJ sense = **72 fJ/bit core**; 1.0e6 sense nodes; 6.3 TB/s peak per die. A 70B decode at 30 steps/s needs 3.4 TB/s across 56 dies, only 0.9% of peak per die, so bandwidth is not the constraint.
- **Plate RC (§10):** one-hole-wide rows leave 41 nm of W, 145 Ω/µm, 0.73 fF/µm. A 50 MHz clock needs a strap or driver every ~100 µm, which is easy on bonded CMOS. The critics' 5 mm word-plane RC (~160 ns) does not apply.
- **Cost (§11):** wafer ~$5.3k (array $1.2k + 198 × $10 + CMOS $1.8k + bond $0.3k) → $0.71/GB. Range $0.42-1.47/GB over wafer cost ×0.7-1.3 and relative yield 0.5-0.95.

---

## 5. U.S. facilities for the demo

| Facility | Use in this plan | Access / cost info | Tag |
|---|---|---|---|
| **Penn Singh Center (Quattrone Nanofab)** | Planar CCD runs (litho, ALD, sputter, metrology) | From 2025-07-01: door $66-77/h industry ($34-39 academic); staff $150/h industry; tools $0-495/h industry | [REPORTED] [fee page](https://www.nano.upenn.edu/resources/fee-structure) |
| **Stanford SNF** | E-beam gates (25-50 nm), ALD oxide channels, sputter | Open to external academic and industry users; rates not found this session | [UNVERIFIED] |
| **Cornell CNF** | JEOL-class e-beam, DUV stepper for gate arrays at wafer scale | NNCI site; rates not found | [UNVERIFIED] |
| **Georgia Tech IEN** | Oxide TFT/CCD process; Georgia Tech oxide-memory groups nearby | New rate structure from 2025-09-01; amounts not in snippet | [REPORTED] [SENIC](https://senic.gatech.edu/about/rates) |
| **MIT.nano / MIT Lincoln Laboratory Microelectronics Lab** | LL is the U.S. reference CCD fab (buried channel, single-poly, x-ray CCDs): ideal for a CCD-veteran collaboration or a government-sponsored run | LL access normally via government programs (NASA/DoD) | CCD work [REPORTED] (SPIE 2024); access [UNVERIFIED] |
| Purdue Birck, ASU, UT Austin | Alternates for ALD In2O3/IGZO and stack etch | Rates not found | [UNVERIFIED] |
| Other rate anchors | KU $143/h external market; UD $79/h corporate; Notre Dame $124/h external; Texas A&M $150/h industry; Michigan LNF 2025 +9% non-academic | — | [REPORTED] [KU](https://nanofab.ku.edu/rates-fees), [UD](https://udnf.udel.edu/?p=81), [ND](https://nanofabrication.nd.edu/facility-access/fees/), [TAMU](https://aggiefab.tamu.edu/fees), [LNF](https://lnf-wiki.eecs.umich.edu/wiki/Financial_Memos) |
| **Argonne CNM** | ALD of buried heterochannels (IGO/IGZO/In2O3, Ga-free ZTO/ITZO), XPS for band offsets | User proposals; non-proprietary at no cost, proprietary at cost recovery | [UNVERIFIED: training knowledge] |
| LBNL Molecular Foundry, ORNL CNMS, NIST CNST NanoFab, Sandia/LANL CINT | TEM of channel stacks; NIST NanoFab is fee-based and open to industry; Sandia MESA via government work only | Same user-proposal model | [UNVERIFIED] |
| **ChipFoundry sky130 (SkyWater, U.S.)** | Readout/regenerator/DFE test chip for the loop demo (or FPGA + discretes) | ~$15k per 100 chips; runs slip if <50% full; SkyWater IonQ-owned since 2026-07-31 per ram-venture | [REPORTED] [eeNews](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/) |
| wafer.space GF180 | Cheaper alternate for the readout chip | ~$7-7.5k per full slot (1,000 dies); fabbed at GF Singapore | [REPORTED] [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2) |
| MOSIS | Commercial MPW fallback | Quote needed | [UNVERIFIED] |
| Test | In-house: used ≥200 MHz 4-channel pattern generator, charge amplifier, digitizer, FPGA; hot/cold chuck at the host university | ~$95k in budget | [ESTIMATE] |

---

## 6. Collaborators and recruits (named groups)

- **imec storage-memory program (Maarten Rosmeulen)**: device owner. The options are to partner (IIAP membership is costly) or to license the heterochannel/DFE IP to them. Quoted in IMW 2026 coverage [REPORTED].
- **MIT Lincoln Laboratory, Advanced Imager Technology group**: buried-channel CCD process, CTE at speed, the single-poly transition (SPIE 2024) [REPORTED for the work; group name UNVERIFIED]. MIT Kavli Lynx CCD collaborators (JATIS 2019).
- **LSST Camera deferred-charge team (Snyder et al., 2021)**: DFE kernel extraction and correction methodology [REPORTED].
- **Fermilab skipper-CCD group (Tiffenberg et al., PRL 2017)**: low-noise CCD readout [UNVERIFIED: training knowledge].
- **LBNL fully-depleted CCD group (MicroSystems Lab)**: CCD design and test [UNVERIFIED].
- **Oxide-channel device groups**: Stanford (H.-S. P. Wong; K. Saraswat, BEOL oxide), Purdue (P. Ye, ALD In2O3), Georgia Tech (S. Yu, S. Datta: oxide-channel memory, 3D), Notre Dame (K. Ni: 3D FeRAM, per A3), Penn (D. Jariwala) [UNVERIFIED: training knowledge, except Georgia Tech/Purdue/Notre Dame, which A3 lists].
- **Systems**: UC Berkeley Sky Computing Lab (vLLM) and LMSYS (SGLang) for traces; TU Dresden compiler chair (ShiftsReduce authors) for placement [arXiv 2019 REPORTED; affiliations UNVERIFIED].
- **Recruit profile for the device co-founder**: a CCD device/process engineer from the Si CCD lineage (Teledyne e2v/DALSA, ex-Kodak/Truesense/onsemi CCD, MIT LL, LBNL), *plus* an oxide-TFT process engineer from display (IGZO backplanes) as the first hire or advisor [ESTIMATE].

---

## 7. Decisive experiment

**Question:** Can any deposited oxide channel reach median per-transfer CTE ≥ 0.997, with DFE, at ≥150 M transfers/s, at both 25 °C and 85 °C, with sheet charge ~4.5e12 cm⁻², the density a 40 nm-plate packet carries? And do ≥92% of LLM-serving bytes have ≥0.64 µs of lead time?

### 7.1 Design, step by step

0. **Month 0, ~$35 plus 1 day.** Buy imec's IEDM 2024 and IMW 2026 papers. Record the CTE definition, packet size, gate length, temperature and fat-zero use. If 98% is end-to-end, reset the priors: the risk moves from CTE to scaling and readout noise.
1. **Months 0-2: provisional #1 and TCAD.** File the heterochannel + DFE + two-ended-string provisional before any outreach. Fit the trap model (`models/charge-river.py` §5) in DEVSIM or a university Sentaurus license. Design masks.
2. **Months 1-4: trap spectroscopy on companion TFTs.** Same stacks as the CCDs. Transient drain current from 1 ns to 1 ms at 0, 25, 85 and 125 °C extracts the trap DOS at 0.1-0.3 eV below Ec, the window a 50 MHz clock probes. This de-risks the extrapolation even before CCD data arrives.
3. **Months 3-9: CCD run 1, planar (Penn/SNF/CNF plus Argonne ALD).** Si/SiO2 wafers.
   - **Gates:** single-level W/Mo, 3-phase interdigitated, Lg = 25, 40, 100 and 250 nm. Gaps are 12-20 nm (e-beam), which mirrors the 15 nm inter-plate oxide of the vertical string.
   - **Dielectric:** ALD SiO2/Al2O3, EOT ~5 nm.
   - **Channels (4 variants):** (a) surface a-IGZO 8 nm (imec baseline); (b) buried: 2 nm Ga-rich IGO barrier / 5 nm In-rich IGZO or In2O3 core / 3 nm cap; (c) Ga-free ITZO or ZTO; (d) buried In2O3/ZTO. All with ≤400 °C anneal.
   - **Input:** fill-and-spill input gate for signal and fat zero (0-30%).
   - **Output:** output gate, floating diffusion, reset.
   - **Two channel widths:** *wide* (W = 20 µm) gives ~3.6e4 e- packets at the target sheet charge, read with a discrete charge amplifier; *narrow* (W ≤ 150 nm) has an on-chip IGZO source follower and measures string-to-string spread (k_ws) and Poisson granularity.
   - **Lengths:** 16, 64 and 256 stages, plus a 32-stage loop whose output goes to an FPGA regenerator and back to the input (98 transfers per lap).
4. **Months 6-11: measurement.**
   - **Clocking:** burst mode, fast through the device under test (stage clock 4-200 MHz) and slow at the output, so trailing charge reads cleanly.
   - **CTE metrology:** first-pixel response and extended-pixel-edge response vs clock, fat zero and temperature (0, 25, 85, 125 °C).
   - **DFE:** extract the deferred-charge kernel, replay through the DFE offline, and compute the eye and BER with the model's partition-noise term.
   - **Endurance:** 1e12 plate cycles at 85 °C, which takes 1.4 h at 200 MHz.
   - **Retention:** at 85 °C.
5. **Month 10: GATE 1.** GO if any variant reaches median CTE ≥ 0.997 at ≥150 MT/s at 25 and 85 °C (STRONG GO ≥ 0.999). NO-GO if every variant is < 0.993 at ≥50 MT/s. In between, run 2 targets the dominant trap class found in step 2.
6. **Months 10-16: CCD run 2.** Best stack at Lg 25-40 nm with narrow channels. Add the sky130 readout/DFE chip ($15k slot) or keep an FPGA plus discrete readout.
7. **Months 6-15: trace-driven SOAP simulator** (founder-written software, ~$15k of GPU time). Capture vLLM/SGLang traces for dense Llama-70B-class, MoE (DeepSeek/Mixtral-class) and long-context sparse attention. Tag each access with the moment its address became known (its lead time). Simulate laps, the SRAM front buffer, row conflicts and scrub. Report the schedulable share vs lap time, effective latency, and pJ/bit vs HBM. Open-source the trace format.
8. **Months 16-21: DEMO.** The 98-transfer loop with regeneration runs ≥1e12 bit-decisions at a 50 MHz stage clock, 25 and 85 °C. Measure raw BER ≤ 5e-10 directly. Show ≥92% schedulable bytes on real traces.
9. **Months 18-24: raise milestone (partner-funded, outside $1M).** An 8-16-plate vertical coupon via imec, MIT LL or a university with deep W/SiO2 stack etch. Prepare the $10-50M raise.

### 7.2 Budget (from model §13; standalone CHARGE-RIVER seed)

| Item | USD |
|---|---|
| Founder salaries, 2 × 24 mo lean, incl. payroll tax | 330k |
| CCD/device advisor (~10%) | 40k |
| University nanofab fees (~1,400 h at ~$140/h blended industry rate) | 200k |
| E-beam lithography (~150 h) | 40k |
| Wafers, ALD precursors, oxide targets, masks | 45k |
| National-lab user time (Argonne CNM, LBNL Foundry) | 15k |
| Test hardware (pattern generator, charge amp, digitizer, FPGA, chuck access) | 95k |
| sky130 readout/DFE chip (ChipFoundry slot) | 15k |
| Packaging, PCBs, wire bond | 15k |
| Simulator GPU time | 15k |
| IP (3 provisionals + 1 PCT) | 45k |
| Legal, accounting, insurance | 35k |
| Travel (IEDM, IMW, imec/LL) | 20k |
| Contingency | 80k |
| **Total** | **990k** |

**Portfolio mode** (per FINAL_CONCEPTS.md, where CHARGE-RIVER shares the seed): the minimal CCD structure set rides the shared oxide coupon run (~$80-100k), and the simulator is ~$150k or grant-funded. In this mode only GATE 1 is funded.

### 7.3 Timeline

| Months | 0-2 | 2-4 | 4-6 | 6-9 | 9-12 | 12-16 | 16-21 | 21-24 |
|---|---|---|---|---|---|---|---|---|
| Device | papers, provisional, TCAD, masks | TFT trap spectroscopy | run 1 fab | run 1 fab and test | **GATE 1** (M10) | run 2 (narrow, 25-40 nm) | loop BER demo | vertical coupon (partner) |
| System | trace capture plan | trace capture | simulator v1 | simulator v1 | schedulability report | controller + front-buffer sizing | demo integration | raise |

---

## 8. IP landscape

**Patents and art to watch**
- **imec**: no CCD-memory patent surfaced in a targeted search (negative result, [USPTO hits unrelated](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11737274)). Given IEDM 2024 publication, expect 2022-2024 priority filings. Commission a professional Espacenet/USPTO search (assignee IMEC; "charge coupled" AND "oxide semiconductor"), ~$3-5k [ESTIMATE].
- **3D NAND vertical-channel patents** (Samsung, YMTC, Macronix, Kioxia) cover hole/plate structures but not CCD shifting ([US 8,921,182](https://patents.google.com/patent/US8921182), [US 9,935,121](https://patents.google.com/patent/US9935121) negative results). Freedom to operate on stack *process* needs checking.
- **Semiconductor Energy Laboratory (SEL)** holds broad oxide-semiconductor memory/device portfolios [UNVERIFIED: training knowledge]; screen it for oxide-CCD claims.
- **US RE43,639** (CTI correction in a charge-domain ADC) and LSST (2021) are prior art against broad "CTI correction" claims, so DFE claims must be memory- and decision-specific.
- **ShiftsReduce (2019)** and SOAP are prior art against broad placement claims; claim the lead-time/lap-time scheduling of LLM tensors with a front buffer.
- **Expired foundations**: buried-channel CCDs ([US 4,285,000](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4285000)) and 1970s CCD memories. IBM racetrack family likely expired or expiring [UNVERIFIED].
- **HBF** (SanDisk/SK hynix) system claims on weights-streaming stacks: watch them for the scale path.

**What to file (provisionals before any external talk)**
1. A buried oxide heterochannel CCD for memory: core/barrier conduction-band offset ≥0.3 eV, Ga-free ITZO/ZTO variants, packet held off the gate interface.
2. A history-aware DFE sense node for CCD memory: kernel calibration from training patterns, partition-noise-aware threshold, and per-string kernel tables.
3. A two-ended vertical CCD string with sense and regeneration at both ends (bonded CMOS below, top metal above), segment ≤32 stages, no staircase (3-6 clock lines).
4. Park-and-shift control: lap on demand plus a scrub interval tied to retention, rather than continuous circulation. Temperature-compensated clocking that holds the probed trap depth E_w constant (slower when cold, faster when hot).
5. An LLM placement controller that guarantees lead time ≥ one lap, with front-buffer sizing from the measured random floor.
6. (Method) Sheet-charge-matched wide-channel CTE metrology predicting nanoscale-gate CTE. Weak as a patent; publish it instead.

---

## 9. Open gaps

1. **The definition of imec's ">98% CTE"** (per transfer vs end-to-end), plus its packet size, temperature and fat-zero use. This is the single biggest prior.
2. **IGZO trap DOS at 0.1-0.3 eV below Ec** (emission times of 1-50 ns). No data was found; the model's tail slope W (15-60 meV) spans PASS to FAIL.
3. **Whether buried oxide heterochannels exist as deposited by ALD in an AR-80 hole**, and their real interface-trap share. Bilayer TFT data exists, but the mechanism is debated.
4. **Packet scaling**: imec works at "a few thousand" e-, while CHARGE-RIVER needs ~300-450 e-. Granularity and the worst string (k_ws) are unmeasured.
5. **Readout noise of a 0.3 fF oxide source follower after CDS.** At ≥15 e- the CTE floor rises to ~0.998, and at 30 e- the base packet fails.
6. **Gate-stress endurance** at 1.5e11-1e12 cycles at 85 °C with a ~3 V clock swing (PBTI/H drift in IGZO).
7. **The random-traffic floor and lead-time distribution** on real MoE/sparse-attention traces. The model's 0.5-2% floor and lognormal lead times are estimates.
8. **Cost inputs**: per-plate deposition cost, CMOS wafer cost and yield for a bonded 200-plate stack are estimates. NAND price is only a cross-check.
9. **Competitive bar**: HBF already serves weights at 1.6 TB/s per stack, so CHARGE-RIVER must win on write endurance (KV), latency or $/GB-with-endurance, not on read bandwidth alone.
10. **Stanford SNF / Cornell CNF / GT IEN rates and national-lab proprietary-use terms** were not verified this session.

**Revival condition if GATE 1 fails** (CTE < 0.993 everywhere): an oxide or other deposited channel reaches ≥0.997 at ≥50 MT/s, or a mid-stack oxide-TFT regenerator tier works (PIXEL-STACK-style, [SPECULATIVE]) so that 10-stage segments keep the full plate count. Or retreat to dense-decode-only use at imec's 4-6 MHz, which the model shows meets 40 ns when the random floor is ≤0.5%, or to the racetrack alternate at ≤1e-9 shift error.
