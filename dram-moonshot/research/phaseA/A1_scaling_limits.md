# A1 — DRAM scaling limits: the physics and engineering bottleneck map

**Phase A, agent `A1-scaling`. Written 2026-11-01.**

**Inputs.** All numbers come from `models/dram_cell_physics.py` (pure Python, exit 0) unless a citation is given. Sources are logged in `research/sources/A1-scaling.jsonl` (60 entries) and assumptions in `research/assumptions/A1-scaling.md`.

**Evidence base.** The network rules allowed 25 web searches and no page fetches. Every web fact here comes from a search snippet [REPORTED via snippet]. Physics derived in this document is tagged [ESTIMATE] with its arithmetic. Prior work reused, not redone:
- `../ram-venture/` cost stack: 1β wafer $3.8k, die 36.5 mm², $1.48/GB.
- Teardown densities, EUV $/layer, and the device cards A1-01…A3-14.

**Framing (MISSION.md).** Judge physics, not business. For each limit, this map separates three kinds:
- a **physics floor** (thermodynamics, electrostatics);
- a **materials wall** (no known material yet);
- an **engineering wall** (known physics, unsolved manufacturing).

---

## 0. Key findings in ten lines

1. **The capacitor is the master bottleneck.** A 1β pillar capacitor (~21 nm diameter, ~1.3 µm tall, aspect ratio ~60, EOT ~0.55 nm) holds only **~5.4 fF**, and the 1c-class cell holds **~4.5 fF** [ESTIMATE, model §2]. That matches TechInsights' "<10 fF at D1z/D1a, 5–6 fF projected at 1c, k>50 needed to stay above 7 fF" ([TechInsights/Choe](https://www.techinsights.com/ja/node/37840)). Holding 7 fF at 1c needs either an aspect ratio of ~115 or k ≈ 70.
2. **The capacitor exists only to beat the bitline.** The sense signal is ΔV = (V_cell − V_pre)·Cs/(Cs + Cbl). At ~35 fF Cbl (512 cells per bitline) the fresh signal is ~71 mV, and a stored "1" can lose only ~15% of its voltage before the margin is gone. **At 64 cells per bitline, ~1.2 fF suffices.** That capacitor is a 300 nm stub, not a 1.3 µm skyscraper (model §3).
3. **Retention is set by a ~6σ tail cell leaking ≤13 fA (64 ms) to ≤26 fA (32 ms, >85 °C).** A 1 s worst-case retention needs ≤0.84 fA, and 10 s needs ≤0.08 fA. Si BCAT tails are dominated by GIDL/GIJL. IGZO channels at <1 aA ([Kioxia OCTRAM, via ram-venture A1-04](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology)) would give ~800 s with today's capacitor.
4. **Refresh costs ~46 fJ per bit-refresh.** That is ~12 mW per 16Gb die and ~0.5 W per 64GB RDIMM at 64 ms, doubling above 85 °C: ~4–8% of active power and **16–33% of idle** [ESTIMATE]. DDR5 16Gb is unavailable for **7.6%** of the time (295/3,900 ns). Literature puts refresh at >20% of DRAM energy at 32Gb ([UMD](https://terpconnect.umd.edu/~blj/papers/ieeetc65-1.pdf)).
5. **Lithography.** 6F² sits at F ≈ 13.4 nm (1β) and 12.0 nm (1c) [ESTIMATE, calibrated to teardowns]. 4F² VCT gives the same cell area at **1.22× larger F**: the same density with relaxed litho, or +50% density at the same F (~+100% with periphery under cell). Samsung has a working 10a 4F² IGZO-channel VCT die with periphery wafer-bonded underneath, targeting 2028 ([TrendForce 2026-04-24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)).
6. **EUV.** Five to seven layers at 1c cost **$825–1,155 per wafer (19–27% of a $4.3k wafer)** before netting out the DUV steps they replace. High-NA is targeted for 2028 ([TrendForce 2026-09-09](https://www.trendforce.com/news/2026/09/09/news-the-race-to-2028-samsung-sk-hynix-set-high-na-euv-timelines-for-dram-as-micron-stays-tight-lipped/)).
7. **3D DRAM economics.** It breaks even with 1β at **~26 tiers (base)**, 7–10 (optimistic) or 57–156 (pessimistic). That is consistent with SK hynix's "32–192 layers needed" ([Guru3D](https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development)). Its 5-tier 56.1% test yield implies ~0.89 per tier; 64 tiers need ≥0.998 per tier after repair.
8. **The HBM tax.** HBM uses ~3× the wafer per bit of DDR5 (Micron, Hot Chips 2026, [Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation)). Hybrid bonding keeps slipping (now HBM4E/HBM5).
9. **Interface energy.** HBM costs ~3–4 pJ/bit, of which ~2.5 pJ/bit is the interposer path; removing the interposer would cut that path to ~0.35–0.4 pJ/bit ([Dally via 36Kr](https://eu.36kr.com/en/p/4002393085071497)). At 8–16 TB/s that is **224–448 W per accelerator**, ~20–25% of its power [ESTIMATE].
10. **Physics headroom is enormous.** kT/C noise on a bitline is 0.38 mV against a 50 mV budget, a bit is ~17,800 electrons, and Landauer's limit is ~10⁷× below the refresh energy. **Nothing here is near a thermodynamic floor.** Every wall is a materials wall or an engineering wall.

---

## 1. The reference cell today (6F² BCAT 1T1C, 1β/1c)

| Quantity | 1β (Micron D1β 16Gb) | 1c / 1γ | Basis |
|---|---|---|---|
| Die / density | 35.83 mm² / **0.447 Gb/mm²** | ~29.1 mm² / ~0.55 Gb/mm² | TechInsights teardown via ram-venture cost_stack §3.1 [REPORTED-P]; 1c [ESTIMATE] |
| Array efficiency | ~0.51 | ~0.51 | CXMT G4: 0.0020 µm² cell × 17 Gb physical / 66.99 mm² [ESTIMATE] |
| Cell area / F (6F²) | ~1,070 nm² / 13.4 nm | ~870 nm² / 12.0 nm | Density ratio vs CXMT G4 [ESTIMATE] |
| Capacitor lattice pitch / pillar Ø | 35 nm / 21 nm | 32 nm / 18 nm | Honeycomb, 14 nm gap for dielectric + top electrode [ESTIMATE] |
| Capacitor height / AR | ~1.3 µm / ~60 | ~1.3 µm / ~74 | Patents cite 50–100:1 ([US 12,193,208](https://patents.google.com/patent/US12193208); [US 2022/0238532](https://patents.justia.com/patent/20220238532)) |
| Cs | **~5.4 fF** | **~4.5 fF** | Model §2; TechInsights "<10 fF, 1c 5–6 fF" |
| Signal charge | 2.85 fC ≈ 17,800 e⁻ | ~2.4 fC | Cs·VARY/2 |
| Bitline | ~512 cells, ~35 fF, Cbl/Cs ≈ 6.4 | Cbl/Cs ≈ 7.7 | [ESTIMATE] |
| Refresh | 64 ms (<85 °C), 32 ms (85–95 °C); DDR5 tREFI 3.9 µs, tRFC 295 ns (16Gb) | Same | [SQR DDR5 datasheet](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7134/SQR-RD5N16G5K6HZZG.pdf) |
| EUV layers | Micron 0; Samsung ~5–6; SK hynix ~3–5 | Samsung 6–7 (cut from 8–9); SK hynix "≥5"; Micron 1γ 1 | ram-venture cost_stack §2.4; [TrendForce 2025-03-11](https://www.trendforce.com/news/2025/03/11/news-micron-pioneers-1%CE%B3-ddr5-samples-with-reduced-euv-use-but-future-risks-loom/); [TechNews 2025-08-12](https://technews.tw/2025/08/12/euv-sk-hynix-1c-dram/) |
| Masks | ~70–80 incl. multipatterning | Higher | ram-venture A1 REF-DDR5-1b [ESTIMATE] |
| Cost | $3.8k wafer → **$1.48/GB** | $4.3k wafer → $1.36–1.50/GB | ram-venture `models/dram_cost_stack.py` |
| Yield signal | — | Samsung enlarged its 1c die after the shrink hurt stability; ~50–60% early 2025 → ~80% hot-test Feb 2026 | [SemiWiki](https://semiwiki.com/forum/threads/samsung-enlarges-1c-dram-die-size-yields-stuck-at-60.24623/latest); [ITHome](https://www.ithome.com/0/923/283.htm) [REPORTED] |

**Reading:** each node now buys ~20–25% density for ~10–15% more wafer cost, a net cost-per-bit gain of only ~10–20% per node (ram-venture cost_stack §2.5). Samsung's 1c die *enlargement* is the clearest sign that lateral scaling is now being paid for in yield.

---

## 2. Storage capacitor: the charge-storage wall

**Physics.** A pillar capacitor's capacitance is C = 3.9·ε₀·(π·d·h)/EOT. At fixed footprint, C can grow only through:
- height h, which is limited by etch aspect ratio, pillar leaning and collapse, and the uniformity of conformal ALD down the hole;
- a lower EOT, which needs higher k at acceptable leakage (≤~10⁻⁷ A/cm² at ~0.8 V).

| Cell | Pitch | Pillar Ø | AR @1.3 µm | Cs | To hold 7 fF you need… |
|---|---|---|---|---|---|
| 1a-class (0.0015 µm²) | 41.6 nm | 27.6 nm | 47 | 7.1 fF | Already there (matches "<10 fF at D1z/D1a") |
| **1β** | 35.1 nm | 21.1 nm | 62 | **5.4 fF** | h = 1.68 µm (AR 79) **or** k ≈ 60 at 6.5 nm |
| **1c** | 31.7 nm | 17.7 nm | 74 | **4.5 fF** | h = 2.0 µm (AR 114) **or** k ≈ 71 |
| Next (0.0006 µm²) | 26.3 nm | 12.3 nm | 106 | 3.2 fF | AR 234 **or** k ≈ 100 at EOT 0.25 nm |

[ESTIMATE, `dram_cell_physics.py` §2.] The 1a row reproduces the reported sub-10 fF figure, and the 1c row reproduces TechInsights' 5–6 fF projection ([Choe](https://www.techinsights.com/ja/node/37840)). The legacy benchmark was ~20 fF with ZrO2/Al2O3/ZrO2 at >1.7 µm height for sub-40 nm DRAM ([US 9,058,984](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9058984)). **Cs has fallen ~4× in ~15 years, and the sense chain has absorbed it.**

**Materials wall.** These are the candidate dielectrics beyond ZrO2/HfO2 (k ~ 35–45):

| Dielectric | k | Advantage | Problem |
|---|---|---|---|
| Rutile TiO2 | ~80+ (anatase <40) | High k | Anatase dominates normal growth; the rutile transition needs >800 °C; the ~3.0–3.2 eV bandgap leaks ([patent snippets](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8551851); [ECS 2013](https://ecs.confex.com/ecs/224/webprogram/Abstract/Paper24478/E2-1876.pdf)) |
| SrTiO3 on Ru | — | EOT 0.42 nm demonstrated (2011–14 era) | Jg ~10⁻⁶ A/cm², ~10× too leaky ([ECS](https://ecs.confex.com/ecs/224/webprogram/Abstract/Paper24478/E2-1876.pdf)) |
| Plasma-assisted rutile TiO2 (2026) | — | — | Still only EOT 1.32 nm at 10⁻⁵ A/cm² ([SeoulTech, Mar 2026](https://pure.seoultech.ac.kr/en/publications/performance-enhancement-of-tio2-based-capacitors-via-plasma-enhan/)) |

**No production-ready k > 60 dielectric with DRAM leakage exists [REPORTED + ESTIMATE].**

**Engineering wall.** Patents describe the problems:
- AR ≥ 70 as the regime of sloped or unopened profiles and leaning nodes ([US 8,962,437](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8962437));
- container under-etch and shorting at >50–100:1 ([US 12,193,208](https://patents.google.com/patent/US12193208)).

Lam is positioning cryogenic etch for "emerging 4F² DRAM" HAR silicon ([Lam FY24 Q4 call](https://www.roic.ai/quote/LRCX/transcripts/2024-year/4-quarter)).

**Why it gates everything else:**
- In 3D DRAM the capacitor must lie on its side inside a ≤60–75 nm tier.
- In 4F² the same capacitor must fit the same (or smaller) footprint.
- A 300 nm stub gives only **1.2 fF** (EOT 0.55) or **2.2 fF** (EOT 0.30). A 500 nm stub gives 2.0 / 3.6 fF (model §2).

So a 3D-compatible capacitor works only if the bitline shrinks (§4) or the cell gains gain (§9).

---

## 3. Access transistor, leakage, retention and refresh

**The retention budget [ESTIMATE, model §3–4].**

- **Allowed leakage.** With Cs = 5.4 fF and 512 cells per bitline, a stored "1" may droop 155 mV (15% of VARY) before the 50 mV sense budget fails. So the weakest of ~1.7×10¹⁰ cells (~6.4σ) may leak at most:
  - 13 fA (64 ms);
  - 26 fA (32 ms, >85 °C);
  - 0.84 fA for 1 s;
  - 0.084 fA for 10 s.
- **Mechanism.** In BCAT cells GIDL and GIJL dominate the tail. Fin-profile tuning cut them by only 9.8% and 22.3% respectively ([TechConnect 2019](https://techconnectworld.com/World2019/a.php?i=1100)). Retention ∝ Cs/I_leak ([US 7,064,373](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7064373)), so **every fF lost from the capacitor tightens the leakage spec proportionally.**
- **The decade budget.** Ion ≈ 20 µA against Ioff ≈ 17 fA is 9.1 decades. At a realistic ~95 mV/dec at 85 °C (ideal 71.6) that needs ~0.86 V of gate swing; 1 aA-class Ioff needs ~1.26 V. This is why the wordline is boosted to ~3 V with a negative WL-off bias, and why VARY cannot drop much below ~1 V (§4).
- **Temperature.** Retention roughly halves per ~10 °C. A Si cell at 105 °C needs ~16 ms refresh and at 125 °C ~4 ms [ESTIMATE]. **This is the single biggest physical obstacle to putting DRAM directly on hot logic (§8).**
- **Oxide channels.** IGZO (Eg ~3.2 eV) has no band-to-band GIDL path. OCTRAM reports Ioff <1 aA per cell with Ion >15–30 µA (ram-venture A1-04). With today's 5.4 fF capacitor that gives **~840 s** retention [ESTIMATE; ignores Vt drift and storage-node junction leakage, which IGZO-on-capacitor still has at the Si contact]. imec's capacitor-less 2T0C IGZO cell shows >400 s ([EE Journal 2020](https://www.eejournal.com/industry_news/imec-demonstrates-capacitor-less-igzo-based-dram-cell-with-400s-retention-time/)). Samsung's 10a VCT moved to IGZO for exactly this reason ([TrendForce](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)).

**The refresh bill [ESTIMATE, model §5].**

| Item | Value |
|---|---|
| Energy per refreshed bit | BL 20 fJ (Cbl·VARY²/2) + WL 3 fJ (pumped), ×2 periphery → **~46 fJ** |
| Per 16Gb die | 12 mW (64 ms) / 24 mW (32 ms) |
| Per 64GB RDIMM (40 dies) | **0.49 / 0.98 W**: 4–8% of ~12 W active, **16–33% of ~3 W idle** |
| Time lost (all-bank) | 16Gb: 295/3,900 ns = **7.6%** (15% above 85 °C). 32Gb: ~10.5% (tRFC 410 ns [UNVERIFIED]). 64Gb extrapolated tRFC ~1.6 µs ([Chang thesis](https://arxiv.org/pdf/1712.08304)) → 20% at 7.8 µs tREFI, more at DDR5's 3.9 µs unless hidden |
| Literature | Refresh >20% of DRAM energy at 32Gb ([UMD](https://terpconnect.umd.edu/~blj/papers/ieeetc65-1.pdf)); 16.6% performance loss at 32Gb even with per-bank refresh ([Chang et al.](https://arxiv.org/pdf/1712.07754)) |

**What removing it would buy:**
- Worst-case retention ×16 (to 1 s) cuts refresh energy and time 16×.
- ×160 (to 10 s) takes refresh to under 1% of idle power and removes the tRFC scaling crisis.
- It also enables multi-level storage, since longer retention gives more droop budget per level.

---

## 4. Sense margin, bitline capacitance and the voltage floor

**Charge sharing.** ΔV = (V_cell − V_BLEQ)·Cs/(Cs + Cbl) ([Vollrath](https://personalpages.hs-kempten.de/~vollratj/Publications/2002_DELTA_SignalMargin.html)). The usable margin is ΔV_BL − (V_OS + coupling noise), with offset set by sense-amp Vt mismatch, and lower supply voltages make offset dominate ([US 11,763,878](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11763878)). Cbl = n·c_cell + c_SA ([US 12,106,797](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12106797)).

| Cells/BL | Cbl | Cbl/Cs (1β) | Fresh ΔV | Cs_min (15% droop) | Cs_min (no droop) |
|---|---|---|---|---|---|
| 1,024 | 65 fF | 12.1 | 40 mV | 10.2 fF | 6.9 fF |
| **512** | **35 fF** | **6.4** | **71 mV** | **5.4 fF** | 3.7 fF |
| 256 | 19 fF | 3.6 | 115 mV | 3.0 fF | 2.0 fF |
| 128 | 12 fF | 2.2 | 166 mV | 1.8 fF | 1.2 fF |
| 64 | 8 fF | 1.5 | 215 mV | **1.2 fF** | 0.8 fF |

[ESTIMATE, model §3; Cbl coefficients assumed.]

**The voltage floor.** With Cbl at 35 fF:
- halving Cs to 2.7 fF would need VARY ≈ 2.0 V for the same margin;
- 1 fF would need ~5 V.

Conversely, keeping today's 5.4 fF but cutting the bitline to 64–128 cells allows **VARY ≈ 0.35–0.45 V**. That cuts the array's CV² energy by **~16× per bit** (smaller C *and* smaller V). The catch is 4–8× more sense amps, which costs array efficiency unless the sense amps move off the array plane, under it through wafer bonding (§5, §9).

**Noise is not the limit.** kT/C on a 35 fF bitline at 85 °C is 0.38 mV rms, against a ~50 mV budget. The binding limits are Vt mismatch and coupling, which are engineering problems.

---

## 5. Cell size and lithography: 6F² → 4F² VCT, periphery under cell, EUV

| Option | Cell | Array eff. | Gb/mm² | × 1β |
|---|---|---|---|---|
| 6F² 1β | 1,070 nm² | 0.51 | 0.447 | 1.00 |
| 6F² 1c | 870 nm² | 0.51 | 0.55 | 1.23 |
| 4F² VCT at 1c F (12 nm) | 576 nm² | 0.51 | 0.83 | 1.85 |
| 4F² VCT at 12 nm + periphery under cell | 576 nm² | 0.70 | 1.14 | 2.55 |
| 4F² at F = 14.7 nm (= 6F² area at 12 nm) + PUC | 864 nm² | 0.70 | 0.76 | 1.71 |
| OCTRAM 275 Mb demo (54 × 63 nm pitch) | 3,400 nm² | 0.51 | 0.14 | 0.31 |

[ESTIMATE, model §1.]

**Reported program status:**
- Samsung reports **+30–50% density** in the same die area for 4F² VCT.
- The channel moved from Si to IGZO.
- Periphery is built on a separate logic-process wafer and joined W2W by hybrid bonding (periphery under cell).
- 4F² spans 10a–10c, with **3D DRAM from 10d**; development completes 2026 and mass production is set for 2028 ([TrendForce 2026-04-24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)).
- CXMT, which has **no EUV**, says it will launch 4F² server DRAM by end-2026 ([SamMobile 2026-10](https://www.sammobile.com/?p=16683332)) [REPORTED].

That last point is the tell. **4F² is partly an EUV-avoidance technology:** at equal density it allows F to be 22% larger.

**What 4F² does *not* fix.** At equal cell area it leaves the capacitor footprint unchanged (4.5 fF at F = 14.7 nm, same as 6F² 1c). It also adds a vertical-transistor problem: the channel, the gate-all-around wordline and the floating body/back-gate all sit in a ~15 nm pillar. Periphery under cell turns the ~49% of the die that is periphery into a second wafer, so the wafer cost roughly doubles before the density gain is netted out [ESTIMATE].

**EUV and capital:**
- Using ram-venture's $165 per wafer per layer ($115–270): 5 / 7 / 10 layers cost $825 / $1,155 / $1,650 per wafer, or 19% / 27% / 38% of a $4.3k 1c wafer, before netting the SAQP steps removed (model §8).
- Samsung and SK hynix target **High-NA EUV in DRAM by 2028**. SK hynix had ~13% of its DRAM output on 1c in 2Q26, heading to 34% in 4Q26 ([TrendForce 2026-09-09](https://www.trendforce.com/news/2026/09/09/news-the-race-to-2028-samsung-sk-hynix-set-high-na-euv-timelines-for-dram-as-micron-stays-tight-lipped/)).
- Each EUV scanner costs ~$290M (ram-venture), and depreciation is ~55% of the leading-edge wafer cost.
- Greenfield capex is ~$145–170k per wpm, so a 100k wpm fab costs ~$15–17B [UNVERIFIED rule of thumb]. Samsung P5 at ~$22B for ~150k wpm of investment ≈ $147k/wpm is a cross-check ([Capital and Compute](https://capitalandcompute.net/blog/memory-capex-buildout-2026/), secondary).
- Micron's FY2026 net capex was **$27.37B**, up from $13.80B ([10-K via snippet](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm)).
- SK hynix plans ~550k → ~1M DRAM wpm by 2030 ([TrendForce 2026-06-05](https://www.trendforce.com/news/2026/06/05/news-sk-hynix-reportedly-to-double-dram-capacity-to-1m-monthly-wafers-by-2030-speeds-yongin-expansion/)). At ~$150k/wpm that is ~$65–75B of tools and shell [ESTIMATE].

**Capital intensity is a consequence of litho-driven scaling.** NAND escaped it by scaling in z with deposition and etch.

---

## 6. 3D DRAM (VS-DRAM, lateral 1T1C, 3D stacking): what blocks it

**State of play [REPORTED]:**
- **SK hynix:** a 5-layer stacked 3D DRAM at VLSI 2024 with **56.1% yield** on a test wafer, which it says is "unstable vs 2D" and needs **32–192 layers** ([Guru3D](https://www.guru3d.com/story/sk-hynix-achieves-yield-in-fivelayer-3d-dram-development)).
- **Samsung VS-DRAM:** 16 layers with gate-all-around lateral transistors, horizontal capacitors, a bitline shield and a shared back-gate ([CloudNews](https://cloudnews.tech/samsung-and-sk-hynix-seek-another-solution-to-the-physical-limit-of-dram/)), aimed at ~2030 ([SemiEngineering](https://semiengineering.com/baby-steps-towards-3d-dram/)). Samsung's roadmap moves to 3D from 10d.
- **imec and Ghent:** **120 Si/SiGe bilayers** (65 nm Si / 10 nm Si₀.₈Ge₀.₂) grown on 300 mm ([SemiEngineering](https://semiengineering.com/tag/light-scattering/); [TechNews](https://technews.tw/2025/08/25/3d-dram-120-layers/)). As of May 2026 the stack still has edge dislocations and embedded defects ([ECS Q&A](https://www.electrochem.org/ecsnews/ecs-webinar-qa-epitaxial-si-sige-multilayers-for-novel-logic-and-memory-devices)).
- **Other routes:** a 1-Mbit oxide-semiconductor vertical-FET 3D DRAM on Si CMOS (IEEE J-EDS 2024, [DOAJ](https://doaj.org/article/936c403535f14b428f2a5a71bfb5a0ef)); IMECAS 4-layer 2T0C, 3 bits/cell, 400 s (VLSI 2026, ram-venture A1-02); Kioxia 8-layer horizontal IGZO transistors (IEDM 2025, ram-venture A1-04); a NEO 3D X-DRAM PoC (company-reported, ram-venture A1-05); a TEL horizontal-capacitor patent ([US 12,464,703](https://patentsgazette.uspto.gov/week44/OG/html/1540-1/US12464703-20251104.html)).

**The five blockers:**
1. **A capacitor in a tier.** A horizontal capacitor in a ≤60–75 nm tier must reach a few fF. That needs ~0.3–1 µm of lateral length per cell, which sets the per-tier footprint (§2). Lam's view is that the lateral recess etch is hard because recess sizes vary along the stack ([SemiEngineering](https://semiengineering.com/baby-steps-towards-3d-dram/)).
2. **The lateral transistor.** It needs a single-crystal channel (epi Si from the Si/SiGe superlattice, which carries defects) or a deposited channel (IGZO: low leakage, but mobility, contacts and PBTI are concerns). Either way it must hit the same Ion/Ioff decade budget (§3) inside a GAA wrap-around.
3. **Bitline and wordline routing.** A vertical bitline running through all tiers grows Cbl with tier count, which worsens §4. Hence Samsung's bitline shield.
4. **Tier economics.** See the table below.
5. **Compound yield.** If the 56.1% for 5 tiers were independent and unrepaired, it would imply 0.891 per tier, giving 2.5% at 32 tiers. Per-tier killer-defect probability must reach ≤0.2% after repair (0.998 → 88% at 64 tiers). That needs NAND-style block redundancy plus ECC [ESTIMATE, model §7].

| Scenario (cell footprint per tier, $/tier) | Gb/mm² per tier | Density break-even vs 1β | Cost break-even | 64 tiers → density, $/bit vs 1β |
|---|---|---|---|---|
| Optimistic (40×300 nm, $20) | 0.047 | 9.5 tiers | 7 tiers | 3.0 Gb/mm² (6.7×), 0.16× |
| **Base (50×600 nm, $30)** | **0.017** | **26 tiers** | **26 tiers** | **1.10 Gb/mm² (2.5×), 0.52×** |
| Pessimistic (60×1,000 nm, $45) | 0.008 | 57 tiers | 156 tiers | 0.50 Gb/mm² (1.1×), 1.47× |

[ESTIMATE, low confidence on $/tier; before tier yield.]

**The insight.** The capacitor's lateral length is the lever:
- shortening it from 600 nm to 300 nm cuts the break-even tier count by ~2.5×;
- deleting it entirely (a gain cell) cuts it further, to roughly the transistor footprint.

**3D DRAM is a capacitor problem wearing a stacking costume.**

---

## 7. HBM: the TSV/stacking tax and power

**Area and yield.**
- HBM dies are **35–45% larger** than DDR5 at the same node and capacity, and yield (TSV packaging included) is **20–30% lower** ([TrendForce 2024-03-18](https://www.trendforce.com/presscenter/news/20240318-12081.html)). Combined, that is ~1.7–2.1× wafer per good bit [ESTIMATE].
- Micron puts HBM3E at **~3×** DDR5's wafer area per bit, "not getting better" ([Tom's Hardware, Hot Chips 2026](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation)).
- The gap comes from TSV keep-out, more banks and wider datapaths. HBM4 has 256 banks against DDR5's 32, and SK hynix D1z DDR4 reached 0.296 Gb/mm² against HBM3's 0.16 ([SemiAnalysis](https://newsletter.semianalysis.com/p/scaling-the-memory-wall-the-rise-and-roadmap-of-hbm)).

**Stack mechanics.**
- Package height limits went from 720 µm (to HBM3E) to 775 µm (HBM4), with proposals of 825 to >900 µm and up to 1,000 µm for 20-high ([TechNews 2026-07-07](https://technews.tw/2026/07/07/jedec-samsung-and-sk-hynix-hybrid-bonding/)).
- Hybrid bonding has slipped to 16-high HBM4E at the earliest (Samsung) or to HBM5 (SK hynix) ([TrendForce 2026-07-07](https://www.trendforce.com/news/2026/07/07/news-samsung-sk-hynix-reportedly-reconsider-hybrid-bonding-timeline-16-high-hbm4e-may-be-earliest-adoption/); [Bits&Chips](https://bits-chips.com/article/besi-faces-longer-wait-as-sk-hynix-pushes-hybrid-bonding-to-hbm5/)).
- The cause is CMP, particle and alignment yield collapsing across 16–20 bonds.

**Power.** An HBM4 stack (2,048 bits × 8–10 Gb/s = 2.0–2.6 TB/s) draws **57–72 W** at 3.5 pJ/bit [ESTIMATE]. A secondary source quotes 75–100 W per stack [UNVERIFIED]. The energy splits as:
- row activation ~0.18 pJ/bit;
- TSV ~0.15 pJ/bit per layer;
- I/O ~0.25 pJ/bit;
- on-die movement ~0.2 pJ/bit/mm.

The model behind this split is validated against 3.44 pJ/bit for HBM3E ([RPU, arXiv 2602.18568](https://arxiv.org/pdf/2602.18568)).

---

## 8. Interface energy and DRAM's share of AI-server power

| Path | pJ/bit | Basis |
|---|---|---|
| DDR5 off-package (core + I/O) | ~10–20 | [UNVERIFIED: training knowledge] |
| HBM3/HBM3E | 3.44 (model-validated); 5–7 in some tables | [RPU](https://arxiv.org/pdf/2602.18568); [Profesional Review](https://www.profesionalreview.com/2025/11/02/hbm4e-vs-hbm3/amp/) (weak; different scope) |
| HBM4 read | ~3–4 | [Dally GTC 2026 via 36Kr](https://eu.36kr.com/en/p/4002393085071497) |
| Interposer path share | ~2.5 → **0.35–0.4 without interposer** | Same (projection) |
| Wire floor | ~0.05–0.2 pJ/bit/mm | RPU 0.2 pJ/bit/mm; 0.05 = 200 fF/mm × (0.5 V)² full swing [ESTIMATE] |

**Accelerator-level arithmetic [ESTIMATE, model §8]:**

| Case | Bandwidth × energy | Power | Share |
|---|---|---|---|
| H200-class | 4.8 TB/s × 3.5 pJ/bit | **134 W** | ~19% of 700 W ([Micron](https://micron.cn/about/blog/storage/ai/ai-drives-power-consumption-micron-drives-power-efficiency)) |
| B200-class | 8 TB/s | **224 W** | ~22% of ~1 kW |
| Hypothetical HBM4 | 8 × 2 TB/s | **448 W** | — |
| Same 16 TB/s, 3D-stacked at ~1.3 pJ/bit | — | 166 W | — |
| Same, I/O at only 0.4 pJ/bit | — | 51 W | — |

Measured context:
- On an A100, data movement is up to **84% of GPU dynamic energy**, with DRAM the largest part ([Montpellier 2024](https://hal.umontpellier.fr/hal-04604802)).
- HBM's share of AI-chip *component cost* rose 52% → 63% from 1Q24 to 4Q25 ([Epoch AI](https://epoch.ai/data-insights/ai-chip-component-cost-shares)).
- Host DDR5 at ~0.5 TB/s and ~15 pJ/bit adds ~60 W per server.

**Net: DRAM, mostly HBM, is ~15–25% of an AI server's power during bandwidth-bound decode [ESTIMATE].** Most of that energy is spent moving bits across the interposer and in destructive-read overfetch, not storing them.

**Overfetch [ESTIMATE, model §6].** A DDR5 RDIMM activation moves ~10 KB to deliver 64 B + ECC. That is 128× overfetch, ≈ **5.9 pJ per useful bit** for random closed-page access, or 1.5 pJ with 4 hits per activation. HBM streaming amortises it to ~0.05–0.18 pJ/bit. The read is destructive, so every activated bit must be restored, which is why page size is an energy problem.

---

## 9. Row hammer / read disturb

- **HCfirst trend:** DDR3 old → new 69.2K → 22.4K; DDR4 17.5K → 10K; LPDDR4 16.8K → **4.8K** ([Kim et al. ISCA 2020](https://arxiv.org/pdf/2005.13121)). A 2022 value of 3.2K was also reported [UNVERIFIED: snippet, source not pinned].
- **Extrapolation:** ~500–950 by 2026 and ~200–500 by 2028 [ESTIMATE, log-linear, not measured].
- **Mitigation cost:** JEDEC PRAC adds <13% performance overhead today but **up to 94%** for future, more vulnerable chips ([ETH, arXiv 2406.19094](https://arxiv.org/pdf/2406.19094v1)). Proposed fixes cut this to ~1% (CnC-PRAC: 0.84–1% energy; [arXiv 2506.11970](https://www.arxiv.org/pdf/2506.11970)), at the price of per-bank counter storage and controller complexity.
- **Physics:** a buried wordline ~10–15 nm from a neighbour's storage node couples charge and injects carriers (trap-assisted electron migration in the Si). The disturb grows as pitch shrinks and as Cs shrinks: fewer electrons have to move to flip a bit, and ~17,800 electrons at 1β are a smaller target each node.
- **Escape:** cells with no floating Si body near the switching wordline (oxide channels) or with non-destructive gain readout. Whether IGZO VCT is hammer-immune is **unknown**; no data was found [UNVERIFIED].

---

## 10. RANKED: the 10 bottlenecks whose removal most improves cost/bit, density, energy/bit or capital intensity

Ranked by impact across the MISSION axes, weighted by how many other bottlenecks each one gates (assumptions file, "Judgment calls").

| # | Bottleneck | Today's numbers | Axes it caps | What a solution would have to do (physical terms) | Wall type | Known attackers |
|---|---|---|---|---|---|---|
| 1 | **Storage-capacitor charge wall** | Cs 5.4 fF (1β) → 4.5 fF (1c); AR 60–75 at ~1.3 µm; EOT ~0.55 nm ZrO2-based; 7 fF at 1c needs AR ~115 or k ~70 | Density, cost/bit, capital (HAR etch/ALD), 3D feasibility | Deliver ≥ the sense charge (Q ≥ ΔV_min·(Cs+Cbl) ≈ 2 fC at 512 cells/BL) from a capacitor **≤300 nm tall in ≤4F²**, i.e. k ≥ 100 at ≤10⁻⁷ A/cm² and 0.8 V with EOT ≤ 0.3 nm. **Or** remove the need for stored charge: in-cell gain (read current ≥1 µA from a ≤1 fF storage node), or Cbl cut ≥5× (§4) | Materials + engineering | Fabs (ZrO2/HfO2 stacks), Lam cryo-etch, academic STO/rutile TiO2, gain cells (imec, IMECAS, NEO) |
| 2 | **No manufacturable 3D DRAM cell** | Break-even ~26 tiers (base; 7–156 range); SK hynix 5 tiers at 56.1%; imec 120 Si/SiGe bilayers still defective; Samsung 3D at "10d", ~2030 | Density (10×), cost/bit, capital (z-scaling instead of litho) | A cell with **per-tier footprint ≤0.012–0.02 µm², tier ≤60 nm, all tiers patterned by one HAR etch + lateral recess/fill**, per-tier killer-defect rate ≤0.2% after repair, per-tier cost ≤$20–30/wafer, and Cbl that does *not* grow with tier count (local sensing every N tiers) | Engineering (gated by #1, #3) | Samsung VS-DRAM, SK hynix, Micron, imec, NEO, TEL, Lam/AMAT |
| 3 | **Access-device leakage tail → refresh** | Tail ≤13 fA (64 ms) / 26 fA (32 ms); GIDL/GIJL-dominated; refresh ~46 fJ/bit → 0.5–1 W per RDIMM, 16–33% of idle power; tRFC/tREFI 7.6% (16Gb) → ~10–20% (32–64Gb) | Energy/bit, bandwidth availability, thermal envelope, MLC feasibility | **Worst-case Ioff ≤0.1 fA at 85–125 °C** (≥130× today) with Ion ≥10 µA in ≤4F², stable Vt (PBTI/H drift ≤50 mV over 10 yr), and thermal-budget compatibility (≤400–450 °C if built over CMOS). Target: worst-cell retention ≥10 s at 85 °C, ≥1 s at 125 °C | Materials (IGZO/IWO/In2O3 are close) | Samsung 10a IGZO VCT, Kioxia/Nanya OCTRAM, imec, SK hynix |
| 4 | **Litho-bound lateral scaling and capital intensity** | 6F² at F ≈ 12–13 nm; EUV 5–7 layers at 1c ($825–1,155/wafer), High-NA by 2028; ~$145–170k/wpm; depreciation ~55% of wafer cost; ~10–20% cost/bit gain per node | Cost/bit, capital, EUV dependence, U.S./export-control exposure | Get the density step from **structure, not wavelength**: ≤4F² (or <4F² effective via multi-bit or tiers) with **≤1 critical litho exposure per tier** (self-aligned), at 1.2–1.5× larger F than 6F² for the same bits/mm² | Engineering | 4F² VCT (Samsung, SK hynix at 10b, CXMT without EUV), 3D (#2) |
| 5 | **Interface / data-movement energy** | HBM 3–4 pJ/bit, ~2.5 of it the interposer path; 134–448 W per accelerator (~20–25% of power); DDR5 ~10–20 pJ/bit [UNVERIFIED] | Energy/bit, system power, bandwidth/W | Put the bits **≤100 µm from the compute that uses them**: µm-pitch 3D bonding directly onto logic, ≤0.4 pJ/bit transport, **and** cells that retain data at the 85–125 °C junction temperature of the logic below (→ #3) | Engineering + thermal | NVIDIA (Dally: interposer removal), custom HBM base dies, SRAM-heavy accelerators |
| 6 | **HBM TSV/stacking tax** | ~3× wafer per bit vs DDR5 (Micron); die +35–45%, yield −20–30%; 775 → 900–1,000 µm stack height; hybrid bonding slipping to HBM4E/HBM5; 57–72 W per HBM4 stack | Cost/bit (HBM), capital (wafer starts diverted), power | Vertical bandwidth **without per-die TSV area and per-bond yield loss**: monolithic tiers (no TSVs), or TSV/bond area <5% of die with >99.5% per-bond-layer yield; or 10× bits per die so fewer dies are stacked | Engineering | SK hynix/Samsung/Micron (hybrid bonding), Besi/AMAT, monolithic 3D (#2) |
| 7 | **Periphery overhead (array efficiency ~51%)** | ~49% of a DDR5 die is sense amps, SWDs, decoders, I/O and pads; PUC needs a second, bonded logic wafer | Density, cost/bit | Move periphery **under/over the array at no area cost**: wafer bonding at a pitch fine enough for per-mat (or per-bitline-group) connections, with the bonded wafer costing less than the area it frees (array efficiency → 0.7–0.85) | Engineering | Samsung PUC (10a 4F²), CBA in 3D NAND (YMTC Xtacking, Kioxia CBA) |
| 8 | **Destructive read + page overfetch** | 10 KB activated per 64 B on DDR5 RDIMM (128× overfetch) → ~5.9 pJ/useful bit random; HBM streaming ~0.05–0.18 pJ/bit | Energy/bit, random-access throughput | **Non-destructive or sub-page activation:** sense/restore only the ≤64–256 B being accessed (per-segment wordlines or local sense amps), or a gain cell whose read does not disturb the storage node so no restore is needed | Architecture + cell | Gain cells, fine-grained activation research, HBM pseudo-channels |
| 9 | **Read disturb / row hammer** | HCfirst 69.2K → 4.8K (2010s → 2020); ~0.5–1K by 2026 [extrapolated]; PRAC <13% now, up to 94% future overhead | Reliability, effective bandwidth, controller cost; gates further pitch shrink | A cell with **no charge-injection path from a toggling neighbour wordline**: no floating Si body, wordline-to-storage-node coupling ≤1% of Q per 10⁵ toggles; HCfirst ≥100K without counters | Device physics (partly unknown for oxide channels) | JEDEC PRAC/RFM, ETH SAFARI, IGZO VCT (untested for hammer) |
| 10 | **Array voltage floor (VARY ~1 V, WL ~3 V)** | Signal ∝ VARY·Cs/(Cs+Cbl) → VARY can't drop without more Cs; the Ion/Ioff decade budget (9–13 decades × ~95 mV/dec) forces ~3 V wordlines; CV² energy stuck | Energy/bit (core and refresh) | Get a ≥50 mV signal at **VARY ≤0.4 V** via Cbl ≤12 fF (≤128 cells/BL with SAs under the array) or in-cell gain; plus a steep-slope or wide-bandgap access device so the wordline swing falls toward ≤1.5 V → ~5–16× lower array energy | Engineering (SS ~60 mV/dec is a physics floor at 300 K unless steep-slope) | Short-bitline/PUC designs, gain cells, steep-slope (NC-FET, TFET; research) |

**How the bottlenecks couple.** Bottlenecks #1, #3, #4 and #10 trace back to one cause: the bit is stored as passive charge on a capacitor read through a long bitline, behind a leaky Si switch. Bottlenecks #5, #6 and #8 trace back to a second cause: the bits sit far from compute and are read destructively in large pages.

---

## 11. White spaces (physics-first, provable at small scale)

1. **"Short bitline, short capacitor": sense amps under the array via fine-pitch wafer bonding.**
   - *Physics.* Cut the bitline to 64–128 cells (Cbl 8–12 fF). The required Cs then drops from ~5.4 to **~1.2–1.8 fF**, achievable with a 300–500 nm capacitor, and VARY can drop to ~0.4 V. Array energy falls ~16× per bit, the HAR etch disappears, and the same short capacitor fits a 3D tier.
   - *What has to be true.* At 1β cell size, a 64–128-cell bitline covers ~0.07–0.14 µm², and an open-bitline sense amp serving two of them gets ~0.14–0.27 µm². That needs a ~10-transistor sense amp in that area on an advanced-logic wafer, plus one vertical connection per bitline: a ~0.26–0.37 µm bond pitch, or ~0.5 µm with 2:1 muxing in the array layer, which is beyond production hybrid bonding today [ESTIMATE].
   - *Novelty.* Samsung's periphery-under-cell moves *periphery* under the array; nobody has publicly coupled per-bitline-group sensing to shrinking the capacitor.
   - *Proof.* Testable on an MPW logic wafer bonded to a university-fab short-capacitor array, or first in BEOL IGZO.
2. **A stackable oxide-semiconductor gain cell (2T0C/3T0C) built 3D-NAND-style.**
   - *Physics.* No capacitor (#1). Ioff ≤1 aA gives retention ≫10 s (#3: refresh ≈ 0, and multi-bit becomes possible, cf. IMECAS 3 bits/cell). The read is non-destructive (#8). The BEOL thermal budget allows stacking on logic (#5).
   - *What has to be true.* Per-tier footprint ≤0.012–0.02 µm² so it breaks even at ≤25 tiers. Vertical channels deposited by ALD in punched holes, so one HAR etch serves all tiers. Read current ≥1 µA. Vt variation tight enough for 2–3 bits.
   - *Known players.* imec, IMECAS, NEO (3T0C claim), Kioxia (horizontal IGZO).
   - *The open twist.* Multi-level plus NAND-like single-etch integration, with a target of matching DRAM bandwidth rather than flash.
3. **A "thermally hardened" DRAM tier bonded directly on logic (memory-on-compute).**
   - *Physics.* Interface energy falls from ~3.5 to ≤1.3 pJ/bit, saving ~130–280 W per accelerator at 8–16 TB/s. It also removes the HBM TSV/stack tax (#6).
   - *The blocker it must beat.* Si-cell retention collapses ~16× at 125 °C; IGZO cells (Ioff ≤1 aA → ~840 s at 85 °C) have the margin.
   - *What has to be true.* ≥1 s worst-case retention at 125 °C; bits/mm² ≥0.3–0.5 Gb/mm² per tier (≥10× SRAM, which is ~0.04 Gb/mm² at N2 macro level per ram-venture A3-06-n2), so it beats SRAM by an order of magnitude on the same footprint; and stacked tiers to reach ≥4–8 GB per accelerator footprint.
   - *Proof.* Test chips on a 2T0C IGZO BEOL over an MPW logic die, with retention-vs-temperature curves.

**Also noted (not top 3):**
- Sub-page / non-destructive activation as an architecture overlay on any cell (#8).
- Hammer-immunity characterisation of IGZO cells: a cheap, unanswered measurement (#9).
- k ≥ 100 low-leakage dielectrics at ≤450 °C: a high-risk materials bet (#1).

---

## 12. Physics floors vs walls (for phase C triage)

| Quantity | Today | Physics floor | Gap |
|---|---|---|---|
| Energy to refresh a bit | ~46 fJ | kT·ln2 ≈ 3.4×10⁻²¹ J at 85 °C | ~10⁷ |
| Energy to deliver a bit to a GPU | ~3.5 pJ | Wire ~0.05 pJ/mm × ~1 mm | ~10–70× |
| Sense-signal noise | 50 mV budget | kT/C on 35 fF ≈ 0.38 mV | ~130× (mismatch-limited, not thermal) |
| Charge per bit | ~17,800 e⁻ | ~100–1,000 e⁻ before shot noise and soft errors dominate [ESTIMATE] | ~20–180× |
| Retention | 64 ms worst-case | No floor; IGZO cells demonstrated >400 s | ≥6,000× available |
| Subthreshold swing | ~95 mV/dec (85 °C) | 71.6 mV/dec thermionic at 85 °C (beatable only with steep-slope devices) | ~1.3× (a true physics floor) |

**Verdict for MISSION triage.** None of the ten bottlenecks is a physics wall. Only the subthreshold slope is near a fundamental floor, and it matters only through the voltage floor (#10), which shorter bitlines or gain cells sidestep.

**Revival conditions for ideas killed in ram-venture on these axes:**
- **IGZO 2T0C as commodity DRAM** (ram-venture A1-02, killed for $/GB) revives if per-tier footprint ≤0.02 µm² and ≥25 tiers become manufacturable on a 300 mm BEOL line.
- **3D X-DRAM** (A1-05, marginal) revives if array-level retention and yield data appear for ≥32 tiers.

---

## Sources

Full log in `research/sources/A1-scaling.jsonl`. Key URLs are cited inline above.

All web facts are via search snippets (25 searches; no fetches). Prior-work figures carry their ram-venture provenance.
