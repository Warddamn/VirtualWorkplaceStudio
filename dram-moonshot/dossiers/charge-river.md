# CHARGE-RIVER: technical dossier

**Agent:** `dosw-charge-river` · **Written:** 2026-11-02 · **Inputs:** `research/stage3/FINAL_CONCEPTS.{json,md}`, `research/stage3/charge-river_notes.md`, `research/stage3/charge-river_model_output.md`, `models/charge-river.py` (re-run 2026-11-02, exit 0), `MISSION.md`. Sources are logged in `research/sources/*.jsonl`; assumptions are in `research/assumptions/dos-charge-river.md`.

**Tags.** [REPORTED] = search snippet or secondary source. [ESTIMATE] = our arithmetic. [SPECULATIVE] = physics nobody has shown. [UNVERIFIED] = training knowledge, not confirmed this session.

---

## 0. Header

| | |
|---|---|
| **Name** | CHARGE-RIVER: buried-channel oxide CCD strings, scheduled like a drum for LLM weight and KV streaming |
| **Thesis** | Store bits as electron packets that march through a deposited oxide channel in a 3D-NAND-like hole, with no transistor, capacitor or contact per bit, and let an LLM-aware scheduler hide the serial latency. |
| **Rank / EV** | 7 of 10. EV 40 = S4 × P2 × D5 |
| **Category** | cell/array |
| **Merged from** | device-lens CHARGE-RIVER + system-lens Circulating Tensor Memory |

**Constituent ideas and technique lineage**

| Idea | Technique | Contribution |
|---|---|---|
| I-08763 | Failure mining | Why 1970s CCD memory died; the fix is wide-gap IGZO plus a buried channel |
| I-10793 | Wishful thinking / ideal final result | No transistor, capacitor or contact per bit; regeneration every ~32 tiers |
| I-06518 | Provocation ("Po: the bit is a rumour passed down a line") | One regenerating sense amp per string |
| I-01064 | SCAMPER-Adapt (CCD imagers) | Vertical register into a floating diffusion; its critic forced per-row slits |
| I-04670 | Assumption inversion | 200-layer stack, one hole etch; its critic: ~2-3x cheaper than DRAM, not 100x |
| I-04284, I-04245 | Forgotten-technology revival (CCD memory, delay lines) | NAND geometry clocked as a CCD; recirculation past a regenerator |
| I-04285 | Forgotten-technology revival (IBM 650 SOAP) | Just-in-time placement compiler |
| I-11504 | Phase B lens (B1 cell physics) | W/SiO2 plate stack, ALD oxide channel, density arithmetic |
| I-01381 | SCAMPER-Magnify/Minify | Few-hundred-electron bits, where readout noise sets the floor |
| I-11148 | Scarcity and constraint as engine | Decision quality at the sense amp, which becomes DFE + ECC here |
| I-11581 | Phase B lens (B5 first principles) | Capacitor-hole racetrack, the magnetic alternate device |

**Verdicts**

- **PHYSICALLY POSSIBLE? YES.** No law is violated. CCDs work, imec has built oxide CCD memories, and IGZO thermal generation is ~1e-13 e-/s per well. What nobody has measured is oxide trap emission at a 6.7 ns gate dwell.
- **STEP CHANGE IF IT WORKS? YES, on density and bits per dollar for a streaming tier.** Density is ~3.6x 1-beta (1.62 Gb/mm²) and cost is ~2.1x lower per GB (range 1.0-3.5x). Scrub power is ~190x below DDR5 refresh. It does not win on general random access.
- **PROVABLE WITH $1M IN 24 MONTHS? YES, for the go/no-go.** For $990k the program measures planar CTE against clock, regenerated-loop BER and LLM-trace schedulability. A vertical 200-plate string is a partner or raise milestone.

---

## 1. How it works

DRAM gives every bit a bucket (capacitor) and a tap (transistor), and shrinking them is the industry's wall. CHARGE-RIVER removes both. Picture a bucket brigade inside a straw:

1. Drill one deep hole through ~200 alternating metal and glass plates, the structure every 3D NAND chip already uses.
2. Line the hole with a few nanometres of oxide semiconductor (IGZO, as in phone displays).
3. Pulse three neighbouring plates in sequence, like marquee lights. A puddle of ~300 electrons slides one plate along. A puddle is a "1"; an empty spot is a "0".

Each hole holds 64 bits, made by deposition rather than lithography. At each end, a sense node reads each puddle, decides 1 or 0, and re-injects a fresh full-size puddle, so losses never pile up beyond 32 steps. A correction circuit learns the faint "smear" each puddle leaves, a trick from astronomy cameras, and subtracts it from the next decision.

The catch: reading bit 20 means shifting 20 places, which is why 1970s CCD memories lost to DRAM. Language models, though, read weights in the same order every token and their KV cache append-then-scan, so a scheduler can lay data out to arrive just in time, with a small SRAM buffer for the rare surprise. This is the IBM 650 drum trick applied to AI serving.

```
        end B: floating diffusion + oxide source follower (top metal)
                            |  sense / regenerate / DFE
  ===== plate 200 =====|  ~  |=====    ~   = oxide channel (IGZO / IGO / ZTO)
  ===== plate 199 =====| (o) |=====    (o) = ~313 electrons = "1"; empty = "0"
  ===== plate 198 =====|     |=====    3 plates (phases 1-2-3) per bit
         ...           | (o) |         segment B: 32 bits (98 transfers)
  ===== plate   2 =====| (o) |=====    segment A: 32 bits (98 transfers)
  ===== plate   1 =====|     |=====
                            |  sense / regenerate / DFE
        end A: bonded CMOS wafer (sense amps, DFE, clock drivers)

  [placement compiler] -> [lap scheduler] -> [SRAM front buffer] -> accelerator
   weights fixed order;    start a lap one     catches the ~0.5-3%
   KV append-then-scan     lap before need     unpredictable bytes
```

Packets sit **still** between reads and get a scrub lap every ~20 s. They do not circulate continuously (see section 2.6).

---

## 2. The physics and the numbers

All values come from `models/charge-river.py`. Every input is listed in its output with a source or `ESTIMATE` basis.

### 2.1 Packet and signal

- **Gate capacitance.** Cox = 3.9 ε0 / 5 nm EOT = 6.91 fF/µm². One plate around one hole covers π × 88 nm × 25 nm = 0.0069 µm², so **C = 0.048 fF**.
- **Packet.** Full well = 0.048 fF × 1.5 V / q = **447 e-**. The design runs at 70%, so **N_s = 313 e-**, with a 47 e- fat zero. Sheet charge is 4.5e12 cm⁻².
- **Signal.** At a 0.3 fF floating diffusion: 534 µV/e-, so **167 mV**. Read noise of 8 e- [ESTIMATE] gives SNR 39:1.
- **Scale.** imec's vertical device holds "a few thousand" electrons ([EE Journal](https://www.eejournal.com/industry_news/imec-demonstrates-the-first-3d-implementation-of-a-charge-coupled-device-for-ai-memory-applications/)) [REPORTED]. CHARGE-RIVER is a **few-hundred-electron CCD**, so transfer loss, not read noise, sets the margin.

### 2.2 Density and cost against 1-beta DDR5

- **Stages.** (200 plates − 6 overhead) / (2 segments × 3 phases) gives **32 stages per segment, 64 bits per hole, 98 transfers per read** (3 × 32 + 2).
- **Density.** 64 b / 0.02 µm² = 3.2 Gb/mm² raw. × 0.70 slit efficiency (the critic's per-row slits) × 0.75 periphery × 0.962 ECC = **1.62 Gb/mm², 3.63x 1-beta** (0.447).
- **Wafer cost.** $1,200 array base + 198 plates × $10 + $1,800 CMOS wafer + $300 hybrid bond = **$5,280**.
- **$/GB.** Good area is calibrated to the 1-beta $3.8k wafer → $1.48/GB. At 0.8x yield: **$0.71/GB**. A NAND-price cross-check gives ~$0.84/GB. Over wafer cost ×0.7-1.3 and yield 0.5-0.95, the range is **$0.42-1.47/GB**.

| Metric (16 Gb die) | 1-beta DDR5 | CHARGE-RIVER (model) |
|---|---|---|
| Density / die area | 0.447 Gb/mm² / 35.8 mm² | **1.62 Gb/mm² (3.6x) / 9.9 mm²** |
| Cost | $1.48/GB | **$0.71/GB** ($0.42-1.47) |
| Per-bit devices | 1 transistor + 1 HAR capacitor | none |
| Refresh / scrub power | 11.5 mW (46 fJ/bit per 64 ms) | **0.06 mW** (20 s scrub; ~191x lower) |
| Core read energy | (HBM3 3.44 pJ/bit incl. I/O, [RPU](https://arxiv.org/pdf/2602.18568)) | 0.072 pJ/bit (45 fJ recycled shift + 28 fJ sense) |
| Latency | ~45 ns tRC-class, random | 0.32 µs unscheduled mean wait; 17-26 ns scheduled average |
| Write wear | none | gate stress: >1e10 shown, 1.5e11 needed |
| EUV layers | Micron 0; Samsung/SK hynix 1c: 5-7 | 0 (one ArF hole lattice, 3-6 clock contacts) |

**Corrections carried.**
- **Cost.** Early idea cards claimed ~$0.05/GB ("100x"). The critic's 2-3x is right: **a CCD hole stores 64 bits; a TLC NAND hole stores ~600**.
- **Density.** The concept's "4-8x for streaming" needs more than 200 plates or no slits. At 200 plates density is plate-limited at 3.6x.
- **EUV.** No-EUV is parity against Micron's EUV-free 1-beta and an advantage only against EUV 1c nodes ([TrendForce](https://www.trendforce.com/news/2026/09/09/news-the-race-to-2028-samsung-sk-hynix-set-high-na-euv-timelines-for-dram-as-micron-stays-tight-lipped/)).

### 2.3 Reliability target and minimum CTE

**Target.** At 10 FIT per 16 Gb die, BCH t=2 over 512 b and ~30 reads per bit per second (decode at 20-50 tok/s), raw BER must be **≤ 4.9e-10 per segment read (Q = 6.11σ)**.

**Model.** Per-transfer deferral is ε = k_ws(1 − CTE), with a worst-string factor k_ws = 1.5. A '1' keeps h0 = (1 − ε)^98 of its charge. The noise is read noise, fat-zero noise, Poisson noise on the deferred charge, and binomial partition noise N_s·h0·(1 − h0). **No correction removes partition noise.** With DFE the eye is h0·N_s − 2κ·tail, with κ = 10% residual (method from [LSST, Snyder 2021](https://spiedigitallibrary.org/journals/Journal-of-Astronomical-Telescopes-Instruments-and-Systems/volume-7/issue-04/048002/Characterization-and-correction-of-serial-deferred-charge-in-LSST-camera/10.1117/1.JATIS.7.4.048002.full)).

| Transfers | N_s | min CTE, no DFE | min CTE, DFE |
|---|---|---|---|
| 50 | 313 e- | 0.9959 | 0.9942 |
| **98 (base)** | **313 e-** | **0.9979** | **0.9970** |
| 194 (64 stages) | 313 e- | 0.9989 | 0.9985 |
| 98 | 150 e- | 0.9992 | 0.9990 |
| 98 | 3,000 e- | 0.9962 | 0.9926 |

**Corrections carried.**
1. **The physics floor is CTE ≈ 0.997, not 0.999.** The chief framed the requirement as packet survival (0.98^96 = 14%, 0.999^96 = 91%). A regenerated binary packet needs only a 6.1σ eye, which the base case reaches at **~65% worst-string survival** ((1 − 1.5 × 0.003)^98 = e^−0.44). **0.999 stays the STRONG-GO line**, since it buys 64-stage segments or 3x the worst-string spread.
2. **DFE helps far less than claimed.** Regeneration does most of the work. DFE lowers the CTE floor only from 0.9979 to 0.9970, i.e. ~1.4x more allowed loss per transfer, because partition noise grows with deferral. The concept claimed "0.9999 → 0.999".
3. **Readout noise is a co-equal spec.** At 15 e- the floor rises to ~0.998, and at 30 e- a 313 e- packet fails at any CTE.

**Sensitivity.** Across read noise 4-15 e-, k_ws 1.0-3.0 and κ 0.05-0.3, the floor spans **0.9945-0.9993**. The worst-string factor dominates: k_ws = 3 alone means ~0.9985.

### 2.4 Trap kinetics: from imec's 6.25 MHz to a 50 MHz stage clock

**Transport is not the limit.** Drift across 25 nm takes ~0.6 ps and diffusion ~24 ps, against a 6.7 ns dwell.

**Traps are.** With SRH emission (ν0 = σ·v_th·N_c ≈ 1.1e11 s⁻¹), a clock probes trap depth E_w = kT·ln(ν0·t_dwell):
- imec at 6.25 MHz, 4-phase, 25 °C: 25.7 meV × ln(4,400) = **0.216 eV**.
- CHARGE-RIVER at a 50 MHz stage clock (6.67 ns dwell): **0.203 eV at 85 °C**, but **0.170 eV at 25 °C**.

**The hard corner is fast and cool.** At 25 °C the clock probes ~46 meV deeper into the dense band tail, so the test must cover 25 °C as well as 85 °C.

**Everything hinges on one ambiguous number.** imec's IEDM 2024 abstract says "CTE >98%" ([imec](https://imec-publications.be/handle/20.500.12860/59420)) [REPORTED], without saying per transfer or end-to-end.

| Reading of imec's 98% | Surface IGZO, 50 MHz, 25 °C | Buried + fat zero, 25 °C | vs the 0.9970 floor |
|---|---|---|---|
| Per transfer | 0.56-0.97 (tail slope 15-60 meV) | 0.92-0.995 | NO-GO to marginal |
| End-to-end (142 b × 4 ph → 0.99996 per transfer) | ≥ 0.9992 | ≥ 0.9999 | GO, ~80x margin |

**The buried-channel factor is a guess.** The model assumes buried channel + fat zero cut deferral to 0.18x [ESTIMATE]: (1 − 0.6 interface share × 0.9 removed) × 0.4 for fat zero. **No oxide buried-channel CCD has ever been measured.**

**Step 0 is a $35 paper.** Our judgment: P(pass) ≈ 15-25% if the 98% is per transfer, ≥ 50% if end-to-end.

### 2.5 What each CTE buys

| Median CTE | Bits/hole | Gb/mm² (× 1-beta) | $/GB | Verdict |
|---|---|---|---|---|
| 0.980 | 8 | 0.20 (0.5x) | $3.86 | dead |
| 0.990 | 16 | 0.41 (0.9x) | $2.06 | NO-GO |
| 0.995 | 36 | 0.91 (2.0x) | $1.06 | weak |
| **0.997** | 62 | **1.57 (3.5x)** | **$0.72** | GO |
| ≥ 0.998 | 64 (plate-limited) | 1.62 (3.6x) | $0.71 | GO |

**NO-GO boundary:** CTE 0.9934 gives < 1.5x 1-beta density (~$1.29/GB).

### 2.6 Latency, bandwidth, endurance, retention and RC

- **Latency.** L = t_hit + (1 − s)·T_lap/2.
  - A 32-stage lap at 50 MHz takes 0.64 µs, so 40 ns = 15 + (1 − s) × 320 ns gives **s ≥ 92.2%**. The "phase-clock" definition (a 3.84 µs lap) would need 98-99%.
  - Each address must be known **one lap (0.64 µs) ahead**; a decode layer takes tens of µs.
  - **Dense 70B decode** (0.5% random floor [ESTIMATE]) averages 17 ns, and meets 40 ns even at imec's 4-6 MHz.
  - **MoE + sparse attention** (2% floor) averages 26 ns at 50 MHz, but 0.7-1.5 µs at 4-6 MHz. That is the real case for 50 MHz.
- **Bandwidth is not the constraint.** 1.0e6 sense nodes × 50 Mb/s = **6.3 TB/s peak per die** (3.7 W core). A 70B FP8 model (batch 32, 8k context) moves 113 GB per step, i.e. 3.4 TB/s over 56 dies, or 0.9% of each die's peak.
- **Endurance.** Never circulate continuously.
  - Continuous lapping at 50 MHz means ~1.6e6 decisions per bit per second. That tightens the BER target ~37x and costs ~8e15 plate cycles in 5 years.
  - **Park-and-shift** costs 32 × 30/s × 5 yr = **1.5e11 cycles**, 15x beyond imec's >1e10, and a 1e12 test (1.4 h at 200 MHz) settles it.
  - This corrects the "refresh by circulation" claim of I-04670 and I-04245.
- **Retention.** A 20 s scrub at 10% loss allows ≤ 0.25 aA per well. That is the IGZO 2T0C class ([imec 400 s cell](https://www.eejournal.com/industry_news/imec-demonstrates-capacitor-less-igzo-based-dram-cell-with-400s-retention-time/)). Thermal generation (~1e-13 e-/s) is negligible.
- **Plate RC.** One-hole-wide rows (41 nm of W: 145 Ω/µm, 0.73 fF/µm) need a strap every ~100 µm at 50 MHz. **The critic's 5 mm word-plane RC (~160 ns) does not apply.**

### 2.7 GO / NO-GO

- **GO:**
  - planar CCDs at ~4.5e12 cm⁻² sheet charge, worst-case 1-after-0s pattern, reach median per-transfer **CTE ≥ 0.9970 with DFE** at a **≥ 50 MHz stage clock (≥ 150 MT/s)** at **both 25 °C and 85 °C**;
  - **and** a regenerated 98-transfer loop logs **raw BER ≤ 5e-10**;
  - **and** traces show **≥ 92%** of bytes known ≥ 0.64 µs ahead.
- **STRONG GO:** CTE ≥ 0.999.
- **NO-GO:** every variant is below **0.9934** at ≥ 50 MT/s.

---

## 3. What is new versus prior art

| Date | Who / what | Key facts | Source |
|---|---|---|---|
| 1950s | IBM 650 SOAP drum placement | The placement idea | [UNVERIFIED] |
| 1975-79 | Intel 2416, Fairchild F464 CCD memories | Lost on serial latency and Si dark current | [UNVERIFIED] |
| expired | Buried-channel CCD, US 4,285,000 | Packets kept off interface traps (Si) | [USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4285000) |
| 2019, 2024 | MIT Lincoln Laboratory fast CCDs | 4.6 e- at 2.5 MHz; narrow buried troughs; single-poly gates | [JATIS](https://www.spiedigitallibrary.org/journals/JATIS/volume-5/issue-02/021015/Toward-fast-low-noise-charge-coupled-devices-for-Lynx/10.1117/1.JATIS.5.2.021015.full), [SPIE](https://proceedings.spiedigitallibrary.org/conference-proceedings-of-spie/13103/1310317/Directions-for-advancement-of-MIT-LL-CCDs-for-x-ray/10.1117/12.3020459.full) |
| 2019 | ShiftsReduce racetrack placement | Up to 52.5% fewer shifts | [arXiv](https://arxiv.org/abs/1903.03597) |
| 2021 | LSST deferred-charge correction | Deferred charge is modelable and reversible | [JATIS](https://spiedigitallibrary.org/journals/Journal-of-Astronomical-Telescopes-Instruments-and-Systems/volume-7/issue-04/048002/Characterization-and-correction-of-serial-deferred-charge-in-LSST-camera/10.1117/1.JATIS.7.4.048002.full) |
| n.d. | US RE43,639: CTI correction in a charge-domain ADC | Closest patent art to DFE | [USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/RE43639) |
| 2017-24 | Oxide heterochannel TFTs | Band offsets suppress trapping; **no oxide CCD** | [AEM](https://doaj.org/article/cc5dc9a2a70046a4bc9083b39931ca09), [CAU](https://scholarworks.bwise.kr/cau/handle/2019.sw.cau/59170), [J. Semicond.](https://www.researching.cn/articles/OJ24629ba9f9864632), [SKKU](https://scholarx.skku.edu/item/fde13622-0afc-4041-b0c9-2bc148ffea51) |
| 2017-22 | Oxide TFT trap transients | µs-ms only, **no ns data** | [Sci. Rep.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5605542/), [OUCI](https://ouci.dntb.gov.ua/works/4Varq057), [SSE](https://in4.iue.tuwien.ac.at/pdfs/sispad2022/A-dynamic-current-hysteresis-model-for-IGZO-TFT_2022_Solid-State-Electronics.pdf) |
| **2024-12** | **imec IEDM: planar 142-bit 4-phase IGZO CCD** | CTE >98% (undefined), >200 s, >1e10 cycles, >6.25 MHz | [imec](https://imec-publications.be/handle/20.500.12860/59420), [paper record](https://imec-publications.be/signposting/describedby/50787757-afdf-4351-afd1-5b041dcb6738), [article](https://www.imec-int.com/en/articles/novel-3d-buffer-memory-ai-and-machine-learning) |
| 2025 | Jyväskylä: 3D IGZO CCD block-memory RTL | Bidirectional shifting saves ~20% | [JYX](https://jyx.jyu.fi/handle/123456789/105533) |
| **2026 IMW** | **imec: first vertical IGZO CCD** (3 word lines) | >4 MHz; "a few thousand" e-; CXL buffer; "~5x 2D DRAM by 2030" (claim) | [EE Journal](https://www.eejournal.com/industry_news/imec-demonstrates-the-first-3d-implementation-of-a-charge-coupled-device-for-ai-memory-applications/), [eeNews](https://www.eenewseurope.com/en/imec-taps-ccd-for-3d-cxl-memory-in-data-centres) |
| 2026 | SanDisk + SK hynix HBF | 512 GB/stack, 1.6 TB/s read weights tier | [SanDisk](https://www.sandisk.com/company/newsroom/press-releases/2026/2026-02-25-sandisk-and-sk-hynix-begin-global-standardization-of-next-generation-memory-solution-high-bandwidth-flash-hbf), [Sovereign](https://sovereignmagazine.com/article/hbf-open-standard-ai-inference-512gb) |
| 2026-02 | Taalas hard-wired weights + SRAM KV | Market values a static-weights tier | [Next Platform](https://www.nextplatform.com/2026/02/19/taalas-etches-ai-models-onto-transistors-to-rocket-boost-inference/) |

**Honest position.**
- imec owns vertical oxide CCD memory (planar 2024, vertical 2026). The device direction is not ours to claim.
- Patent searches found only unrelated 3D NAND hits ([US 9,935,121](https://patents.google.com/patent/US9935121), [US 8,921,182](https://patents.google.com/patent/US8921182), [US 11,737,274](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11737274)). That is a negative result, not clearance.

**The genuine delta** (none of these was found in prior art):
1. **A buried oxide heterochannel CCD.** The core/barrier offset is ≥ 0.3 eV, with Ga-free variants.
2. **A partition-noise-aware DFE sense node for memory decisions**, with per-string kernels.
3. **Two-ended ≤ 32-stage strings with park-and-shift and temperature-compensated clocking.** Clocking slower when cold holds E_w constant.
4. **A lead-time LLM placement controller** that guarantees ≥ one lap of lead and sizes the front buffer from the measured random floor. Broad placement claims are dead (SOAP, ShiftsReduce).

---

## 4. Show-stoppers and workarounds

| # | Show-stopper | Number | Workaround path |
|---|---|---|---|
| 1 | **Oxide traps cap CTE at speed** | Need ≥ 0.9970 at 150 MT/s, 25 and 85 °C. The per-transfer reading gives only 0.92-0.995 even buried | Buried heterochannel (≥ 0.3 eV); 15-30% fat zero; H-lean ≤ 400 °C anneal; temperature-compensated clocks; burst clocking. [SPECULATIVE] a mid-stack oxide-TFT regenerator tier every 10-16 stages, so a CTE ~0.99 device keeps its plate count |
| 2 | **Few-hundred-electron packets** | 313 e- vs imec's thousands. ~10-90 traps per gate (critic, I-04670). k_ws > 3 → floor ~0.9985 | Fat zero; per-string DFE kernels; spare holes to map out bad strings (as NAND bad blocks). Bigger packets (thicker plates, wider holes) at a density cost: 600 e- → 0.9956, 3,000 e- → 0.9926 |
| 3 | **Readout noise, 0.3 fF oxide SF** | ≤ 8 e- needed; 15 e- → 0.998; 30 e- fails | CDS. Si CMOS sense at the bonded end. Skipper-style repeated sampling (I-01381) at a latency cost. One-ended strings (half the bits) as a fallback |
| 4 | **Unpredictable traffic** | ≥ 92.2% with 0.64 µs lead; MoE at a 2% floor → 26 ns at 50 MHz, 0.7-1.5 µs at 6 MHz | Front buffer sized to the measured floor; pin hot experts; bidirectional shifting (−20%); 16-stage KV segments. Fallback: dense decode only at 4-6 MHz |
| 5 | **Gate-stress endurance** | 1.5e11 needed vs >1e10 shown | Park-and-shift; 2-2.5 V swing with recycling drivers. A 1e12 test takes 1.4 h |
| 6 | **Vertical integration** | AR-80 hole (8 µm, 100 nm), conformal ALD heterochannel, top-end floating diffusion | Two 100-plate decks (NAND practice [UNVERIFIED]), which matches two segments; PEALD In2O3/ZTO; partner coupons (imec, MIT LL, NAND pilot). A raise milestone |
| 7 | **Cost ceiling ~2x** | 64 b/hole vs ~600 for NAND | [SPECULATIVE] 2-bit packets (needs ~3x tighter deferral); 300-400 plates with mid-stack regenerators |
| 8 | **Gallium** | ~98% Chinese, export-licensed (A2) | Ga-free ITZO/ZTO in the matrix from day 1 |

None violates physics. Only number 1 could end the program, and it is what the seed measures.

---

## 5. The decisive experiment

**Question.** Does any deposited oxide channel reach median per-transfer CTE ≥ 0.997 (with DFE) at ≥ 150 MT/s, at 25 °C and 85 °C, at a 40 nm-plate packet's sheet charge (~4.5e12 cm⁻²)? And do ≥ 92% of LLM bytes have ≥ 0.64 µs of lead?

**Why planar first.** Traps per electron depend on sheet charge, not area, so wide planar CCDs at matched sheet charge measure the vertical-plate physics; narrow channels measure granularity and k_ws.

### Steps

0. **M0 (~$35).** Buy imec's IEDM 2024 and IMW 2026 papers. Record the CTE definition, packet size, temperature and fat zero, then reset the priors.
1. **M0-2.** File provisional #1. Fit the trap model in DEVSIM or Sentaurus. Design masks.
2. **M1-4: companion TFT trap spectroscopy** on the same stacks. Transient drain current from 1 ns to 1 ms at 0/25/85/125 °C extracts the trap DOS at 0.1-0.3 eV below Ec, which predicts CTE before any CCD exists.
3. **M3-9: planar CCD run 1** (single-level 3-phase W/Mo gates).
   - **Gates:** Lg 25/40/100/250 nm with 12-20 nm e-beam gaps; ALD SiO2/Al2O3 at EOT 5 nm.
   - **Channels:** (a) surface IGZO, 8 nm (imec baseline); (b) buried IGO/IGZO-or-In2O3/cap; (c) Ga-free ITZO or ZTO; (d) buried In2O3/ZTO; all at ≤ 400 °C.
   - **I/O:** fill-and-spill input with 0-30% fat zero; floating-diffusion output.
   - **Widths:** wide (20 µm, discrete charge amp) and narrow (≤ 150 nm, on-chip IGZO follower).
   - **Lengths:** 16, 64 and 256 stages, plus a 32-stage loop through an FPGA regenerator.
4. **M6-11: measure.**
   - First-pixel and extended-pixel-edge response against a 4-200 MHz stage clock, fat zero and temperature.
   - Extract the deferred-charge kernel, replay it through the DFE, and compute BER with the partition-noise term.
   - Run 1e12 cycles and retention, both at 85 °C.
5. **M10: GATE 1.**
6. **M10-16: run 2.** Best stack, Lg 25-40 nm, narrow channels, plus a sky130 readout/DFE chip.
7. **M6-15: trace simulator** (founder-written).
   - Capture vLLM/SGLang traces (dense 70B-class, MoE, sparse attention) with each access's lead time.
   - Simulate laps, the front buffer, conflicts and scrub.
8. **M16-21: DEMO.** The regenerated 98-transfer loop runs ≥ 1e12 decisions at a 50 MHz stage clock, at 25 and 85 °C, with BER measured directly.

### Facilities

- **Fab:** Penn Singh Center (2025 industry rates: door $66-77/h, staff $150/h, tools $0-495/h ([fee page](https://www.nano.upenn.edu/resources/fee-structure))), Stanford SNF, Cornell CNF or Georgia Tech IEN ([rates](https://senic.gatech.edu/about/rates)). SNF and CNF rates are [UNVERIFIED].
- **ALD and XPS:** Argonne CNM.
- **TEM:** LBNL Molecular Foundry.
- **CCD partner:** MIT Lincoln Laboratory (access via government programs [UNVERIFIED]).
- **Readout chip:** ChipFoundry sky130, ~$15k per 100 chips ([eeNews](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)), or wafer.space GF180 ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2)).

### Budget (direct experimental cost)

| Item | USD |
|---|---|
| Nanofab fees (~1,400 h at ~$140/h blended industry rate) | 200k |
| E-beam for 25-50 nm gates and gaps (~150 h) | 40k |
| Wafers, ALD precursors, oxide targets, masks | 45k |
| National-lab user time (Argonne CNM, LBNL) | 15k |
| Test hardware (used ≥ 200 MHz pattern generator, charge amp, digitizer, FPGA, hot/cold chuck) | 95k |
| sky130 readout/regenerator/DFE chip | 15k |
| Packaging, PCBs, wire bond | 15k |
| GPU time for traces | 15k |
| CCD device advisor (~10%) | 40k |
| **Direct total** | **480k** |
| **Fully loaded with founders, IP, legal, contingency (section 6)** | **990k** |

**Portfolio mode.** The minimal structures ride the shared oxide coupon run (~$80-100k), and the simulator costs ~$150k or is grant-funded. Only GATE 1 is funded in this mode.

### Pre-set pass/fail

| Test | PASS | STRONG | FAIL |
|---|---|---|---|
| Median CTE at ≥ 150 MT/s, 25 and 85 °C, best variant | ≥ 0.9970 (DFE) / ≥ 0.9979 (none) | ≥ 0.999 | < 0.9934 at ≥ 50 MT/s, all variants |
| Buried vs surface deferral (matched sheet charge) | ≥ 3x lower | ≥ 5x | < 2x |
| Narrow-channel k_ws (1e-4 tail / median) | ≤ 1.5 | ≤ 1.2 | > 3 |
| Post-CDS read noise | ≤ 8 e- | ≤ 5 e- | > 15 e- |
| Loop raw BER, ≥ 1e12 decisions, 50 MHz stage clock | ≤ 5e-10 | ≤ 1e-12 | > 1e-8 |
| 1e12 cycles at 85 °C | ΔCTE ≤ 5e-4 | none | > 1e-3 |
| Retention at 85 °C (≤ 10% loss) | ≥ 20 s | ≥ 200 s | < 2 s |
| Bytes with ≥ 0.64 µs lead (dense / MoE) | ≥ 92% / ≥ 92% | ≥ 99% / ≥ 96% | < 90% on both |

---

## 6. The $1M, 24-month plan

### Quarterly milestones (M0 = funding close, assumed 2027-01-01)

| Q | Milestones | Gate |
|---|---|---|
| Q1 | Papers read; provisionals #1-3 filed; advisor signed; TCAD fit; run-1 masks; FTO search on imec/SEL ($3-5k) | imec CTE definition known |
| Q2 | TFT trap spectroscopy (4 stacks); run 1 in fab; first traces | Trap DOS predicts CTE ≥ 0.993 at 50 MHz for ≥ 1 stack |
| Q3 | First CTE vs clock and temperature; simulator v1 | — |
| Q4 | **GATE 1 (M10)**; schedulability report (M12) | GO ≥ 0.997 / targeted run 2 at 0.993-0.997 / NO-GO < 0.993; ≥ 92% schedulable |
| Q5 | Run 2 (narrow, Lg 25-40 nm); sky130 tapeout; **PCT filing**; front-buffer sizing | — |
| Q6 | k_ws, read noise, granularity | **GATE 2 (M18)**: k_ws ≤ 3 and noise ≤ 15 e- |
| Q7 | **DEMO**: 1e12-decision loop at a 50 MHz stage clock; trace results; IEDM/VLSI submission | Raw BER ≤ 5e-10 |
| Q8 | 8-16-plate vertical coupon with a partner; data room; $10-50M raise | Raise |

### Budget allocation ($990k)

| Bucket | USD |
|---|---|
| Two founders, 24 months lean, incl. payroll tax | 330k (33%) |
| Fab, e-beam, materials, national-lab time | 300k (30%) |
| Test hardware, readout chip, packaging, GPU | 140k (14%) |
| Advisor | 40k (4%) |
| IP: 3 provisionals + 1 PCT | 45k (5%) |
| Legal, accounting, insurance, travel | 55k (6%) |
| Contingency | 80k (8%) |

### Team (where to recruit)

- **Founder A, device lead.** A CCD device and process engineer.
  - Recruit from: MIT Lincoln Laboratory's CCD group (the SPIE 2024 authors), Teledyne e2v/DALSA, onsemi image sensors (ex-Kodak/Truesense), the LBNL MicroSystems Lab, or Fermilab's skipper-CCD group (Tiffenberg 2017) [affiliations UNVERIFIED].
- **Founder B, systems lead.** LLM serving and memory controllers; writes the simulator and the controller.
  - Recruit from: UC Berkeley Sky Computing Lab (vLLM), LMSYS (SGLang), or accelerator memory teams.
- **First hire or contractor: oxide-TFT process engineer.**
  - From IGZO display backplanes (Sharp, LG Display, Samsung Display) [UNVERIFIED].
  - Or from academic oxide groups: Purdue (P. Ye), Georgia Tech (S. Yu, S. Datta), Stanford (H.-S. P. Wong), Notre Dame (K. Ni), Penn (D. Jariwala).
- **Collaborators:** the LSST Camera deferred-charge team (DFE), the ShiftsReduce authors (TU Dresden [UNVERIFIED]) for placement, and an ex-3D NAND integration engineer.
- **Non-dilutive** [UNVERIFIED amounts]: NSF SBIR/STTR, DoD microelectronics programs (a door to MIT LL), DOE user proposals.

### IP strategy

- **File first** (provisionals, before any outreach):
  1. buried oxide heterochannel CCD memory (≥ 0.3 eV offset, Ga-free variants);
  2. history-aware DFE sense node with per-string kernels and a partition-noise-aware threshold;
  3. two-ended ≤ 32-stage string with park-and-shift scrub and temperature-compensated clocking.
- **File second:** (4) the lead-time LLM placement controller with measured-floor buffer sizing.
- **Publish instead:** sheet-charge-matched CTE metrology.
- **Freedom-to-operate risks:**
  - imec: likely 2022-24 priority filings. Our search found none, so commission a professional one. The likely outcome is a cross-licence, not a fight.
  - Semiconductor Energy Laboratory oxide portfolios [UNVERIFIED].
  - 3D NAND process patents (Samsung, Kioxia, Micron, YMTC, Macronix).
  - HBF system claims (SanDisk, SK hynix).
- **Prior art that narrows claims:** LSST and RE43,639 (CTI correction); SOAP and ShiftsReduce (placement).
- **Free to use:** the expired buried-channel CCD (US 4,285,000) and 1970s CCD memories.

---

## 7. After the demo: scale path

| Partner | Why | Deal |
|---|---|---|
| **imec program partners** | Own the oxide CCD line and its 3D flow | Licence heterochannel + DFE, or co-develop. Fastest route to a vertical string |
| **Micron** | U.S. DRAM maker with NAND stack expertise and U.S. fabs being built [UNVERIFIED] | Joint development of a U.S.-built CXL or near-HBM streaming tier |
| **SK hynix** | HBM leader and HBF co-author | CHARGE-RIVER as the write-endurant KV companion to HBF's read-mostly weights |
| **Samsung, Kioxia / SanDisk** | 3D NAND plate stacks at scale; HBF | Licence: "a CCD hole in a NAND line" |
| **Foundries** (GlobalFoundries, SkyWater, TSMC) | 28-40 nm bonded periphery | Supply; pairs with CELL-WAFER FOUNDRY |
| **Display makers** (Sharp, LG Display, Samsung Display, BOE) | Volume IGZO deposition and reliability data | Channel know-how licence |
| **Tool makers** (Applied Materials, Lam, TEL, ASM); **accelerator vendors** | ALD in a hole; the serving stack | Process and controller co-development |

**What $10-50M buys.**
- **$10-15M over 18 months:** 16-32-plate vertical coupons that test CTE in an ALD-in-hole channel; a 28-40 nm readout/DFE chip; an FPGA CXL Type-3 prototype serving real vLLM traffic.
- **$30-50M over 36 months:** a 64-128-plate bonded Gb-class demonstrator with a partner; a controller ASIC; 85 °C/1e12-cycle/FIT qualification; a spec co-signed by a memory maker and an accelerator vendor.

**Standards.**
- CXL Type-3 first.
- An OCP "streaming DRAM-class tier" spec with lead-time hints, following the HBF precedent.
- Later, a JEDEC raw-BER-graded device shared with RAW-BER CONTRACT.

---

## 8. Resources and America

**Scarce inputs.**
- **Gallium.** ~98% Chinese. The U.S. ban suspension ends 2026-11-27 ([Engineering News](https://www.engineeringnews.co.za/article/china-halts-ban-on-gallium-germanium-antimony-exports-to-us-but-controls-remain-2025-11-10)). Quantity is trivial (< 0.4% of world Ga, A2); licensing is the risk. **ZTO is In- and Ga-free; ITZO is Ga-free.**
- **Indium** refining is concentrated [UNVERIFIED].
- **Tungsten.** China mines ~80%, but plates cost ~$3 per wafer even at record prices (A2). Mo is a drop-in.
- **Rare earths.** China's suspended 2025-10 package names "≥256-layer memory" for review ([TrendForce](https://www.trendforce.com/news/2025/10/09/news-china-expands-rare-earth-curbs-subjects-14nm-logic-and-256-layer-memory-chips-to-case-by-case-review/)). A 200-plate stack sits just under that line, but tool magnets are exposed either way.

**EUV.** None. One ArF hole lattice at 141 nm pitch, no staircase, 3-6 clock contacts. That is parity with EUV-free Micron 1-beta, and saves $825-1,155 per wafer against EUV 1c nodes (A1).

**Energy and water** [ESTIMATE].
- **Fab.** DRAM takes ~0.42 kWh and ~2.6 L per GB (A2; [Silicon Analysts](https://siliconanalysts.com/analysis/chip-manufacturing-energy-cost)). A bonded pair (~1,300 kWh array + ~1,000 kWh CMOS) yields ~2.9x a 1-beta wafer's GB, so CHARGE-RIVER lands near **~0.26 kWh/GB**.
- **Use phase.** Use energy is ~16x fab energy for a server GB, so the **~190x scrub saving** matters more.
- **Chemistry.** One HAR etch replaces the capacitor module, which lowers PFAS etch load and helium-cooling exposure.

**U.S. manufacturability.**
- **The demo is all-U.S.:** university nanofabs, Argonne, LBNL, MIT LL, SkyWater.
- **Volume has a gap:** the U.S. has no high-volume 3D NAND fab [UNVERIFIED].
- **The realistic route:** a deposition-heavy array line beside Micron's new U.S. DRAM fabs, U.S.-foundry CMOS (GlobalFoundries NY, SkyWater MN), and U.S. deposition and etch tools.
- **Why it fits:** with no EUV and no display fab, it is a more natural U.S. build than leading-edge DRAM.

---

## 9. Kill criteria

Dated from an assumed funding close on 2027-01-01. Each kill names its revival condition, as MISSION.md requires.

1. **2027-03-31 (reprioritise).** If imec's 98% is per transfer **and** imec already got < 2x from a buried channel or fat zero, cut run 1 to two channels and shift money to trap spectroscopy. *Revival:* any stack with tail-trap DOS ≥ 5x below surface IGZO.
2. **2027-06-30.** Kill if trap spectroscopy predicts **CTE < 0.990 at a 50 MHz stage clock and 25 °C for all four stacks** before run 1 starts. *Revival:* a channel (e.g. crystalline In2O3) with a tail ≥ 3x shallower.
3. **2027-10-31 (GATE 1).** Kill the device if **every variant has median CTE < 0.9934 at ≥ 50 MT/s** at 25 or 85 °C. *Revival:* ≥ 0.997 from any deposited channel; a working mid-stack regenerator [SPECULATIVE]; or dense-decode-only use at 4-6 MHz (≤ 0.5% random floor).
4. **2027-10-31.** Drop IP claim #1 if **buried deferral is < 2x below surface** at matched sheet charge. The program continues only if the surface channel itself passes item 3. *Revival:* an XPS-confirmed ≥ 0.3 eV offset together with ≥ 3x lower deferral.
5. **2027-12-31.** Kill the DRAM-class latency claim if **< 90% of bytes have ≥ 0.64 µs lead on both dense and MoE traces** with a ≤ 64 MB front buffer per 16 GB [ESTIMATE sizing]. Retreat to a capacity tier. *Revival:* stage clocks ≥ 200 MHz (where s ≥ 69% suffices).
6. **2028-06-30 (GATE 2).** Kill if **k_ws > 3 and median CTE < 0.9985**, or if **read noise > 30 e-**. *Revival:* ≥ 1,000 e- packets with density still ≥ 2x 1-beta, or Si readout at both ends.
7. **2028-06-30.** Kill if **85 °C retention < 2 s** (park-and-shift then fails on endurance) or if **ΔCTE > 1e-3 after 1e12 cycles at 85 °C**. *Revival:* a stack with ≤ 0.25 aA per well and stable Vt to 1e12 cycles.
8. **2028-09-30 (DEMO).** Do not raise on a DRAM-class claim if **loop raw BER > 1e-8** over ≥ 1e12 decisions at a 50 MHz stage clock. Between 5e-10 and 1e-8, raise only with t=4 ECC (≤ 3.7e-7 allowed). *Revival:* BER ≤ 5e-10 at ≥ 25 MHz together with s ≥ 96%.

---

## 10. Sources

All URLs are logged in `research/sources/*.jsonl`; [dcr] = `dos-charge-river.jsonl`. Facts tagged [UNVERIFIED] or training knowledge (Intel/Fairchild CCD memories, IBM 650 SOAP, Tiffenberg 2017, display and NAND industry facts) have no URL.

**imec oxide CCD and coverage:** https://imec-publications.be/handle/20.500.12860/59420 [dcr] · https://imec-publications.be/signposting/describedby/50787757-afdf-4351-afd1-5b041dcb6738 [dcr] · https://www.imec-int.com/en/articles/novel-3d-buffer-memory-ai-and-machine-learning [dcr] · https://www.eejournal.com/industry_news/imec-demonstrates-the-first-3d-implementation-of-a-charge-coupled-device-for-ai-memory-applications/ [dcr] · https://siliconsemiconductor.net/article/124234/Imec_demonstrates_the_first_3D_implementation_of_a_charge_coupled_device_for_AI_memory_applications [dcr] · https://www.reinraum.de/en/news/imec-presents-the-first-three-dimensional-implementation-of-a-charge-coupled-device-for-ai-memory-applications.html [dcr] · https://www.eenewseurope.com/en/imec-taps-ccd-for-3d-cxl-memory-in-data-centres [dcr] · https://www.techspot.com/news/112437-researchers-unveil-nand-dram-hybrid-could-outperform-traditional.html [dcr] · https://jyx.jyu.fi/handle/123456789/105533 [dcr] · https://www.eejournal.com/industry_news/imec-demonstrates-capacitor-less-igzo-based-dram-cell-with-400s-retention-time/ [dcr]

**CCD physics and correction:** https://www.spiedigitallibrary.org/journals/JATIS/volume-5/issue-02/021015/Toward-fast-low-noise-charge-coupled-devices-for-Lynx/10.1117/1.JATIS.5.2.021015.full [dcr] · https://proceedings.spiedigitallibrary.org/conference-proceedings-of-spie/13103/1310317/Directions-for-advancement-of-MIT-LL-CCDs-for-x-ray/10.1117/12.3020459.full [dcr] · https://spiedigitallibrary.org/journals/Journal-of-Astronomical-Telescopes-Instruments-and-Systems/volume-7/issue-04/048002/Characterization-and-correction-of-serial-deferred-charge-in-LSST-camera/10.1117/1.JATIS.7.4.048002.full [dcr] · https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/RE43639 [dcr] · https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4285000 [dcr]

**Oxide channels and traps:** https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5605542/ [dcr] · https://ouci.dntb.gov.ua/works/4Varq057 [dcr] · https://in4.iue.tuwien.ac.at/pdfs/sispad2022/A-dynamic-current-hysteresis-model-for-IGZO-TFT_2022_Solid-State-Electronics.pdf [dcr] · https://doaj.org/article/cc5dc9a2a70046a4bc9083b39931ca09 [dcr] · https://scholarx.skku.edu/item/fde13622-0afc-4041-b0c9-2bc148ffea51 [dcr] · https://scholarworks.bwise.kr/cau/handle/2019.sw.cau/59170 [dcr] · https://www.researching.cn/articles/OJ24629ba9f9864632 [dcr]

**Placement, competitors, system:** https://arxiv.org/abs/1903.03597 [dcr] · https://www.sandisk.com/company/newsroom/press-releases/2026/2026-02-25-sandisk-and-sk-hynix-begin-global-standardization-of-next-generation-memory-solution-high-bandwidth-flash-hbf [dcr] · https://sovereignmagazine.com/article/hbf-open-standard-ai-inference-512gb [dcr] · https://www.nextplatform.com/2026/02/19/taalas-etches-ai-models-onto-transistors-to-rocket-boost-inference/ [dcr] · https://arxiv.org/pdf/2602.18568 [A1-scaling.jsonl]

**Patents (negative FTO results):** https://patents.google.com/patent/US9935121 [dcr] · https://patents.google.com/patent/US8921182 [s2-physics-R03.jsonl] · https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11737274 [dcr]

**Facilities and MPW:** https://www.nano.upenn.edu/resources/fee-structure [dcr] · https://senic.gatech.edu/about/rates [dcr] · https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/ [dcr] · https://www.crowdsupply.com/wafer-space/gf180mcu-run-2 [dcr]

**Resources, EUV, energy:** https://www.trendforce.com/news/2026/09/09/news-the-race-to-2028-samsung-sk-hynix-set-high-na-euv-timelines-for-dram-as-micron-stays-tight-lipped/ [A1-scaling.jsonl] · https://www.engineeringnews.co.za/article/china-halts-ban-on-gallium-germanium-antimony-exports-to-us-but-controls-remain-2025-11-10 [A2-resources.jsonl] · https://www.trendforce.com/news/2025/10/09/news-china-expands-rare-earth-curbs-subjects-14nm-logic-and-256-layer-memory-chips-to-case-by-case-review/ [A2-resources.jsonl] · https://siliconanalysts.com/analysis/chip-manufacturing-energy-cost [A2-resources.jsonl]
