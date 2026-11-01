# DD5: U.S. Open Memory IP (compiler service → gain-cell and ReRAM macros): research notes

**Agent:** `p4-open-memory-ip` · **As of:** 2026-11-01 · **Bundle:** anchor C-33 (OpenRAM macro service), folded C-32 (Si gain-cell eDRAM IP) and C-22 (ReRAM secure NVM on SkyWater S130).
**Model:** `models/open-memory-ip.py` (exit 0). Output: `research/phase4/open-memory-ip_model_output.md`. **Sources:** `research/sources/p4-open-memory-ip.jsonl` (66 entries). **Assumptions:** `research/assumptions/p4-open-memory-ip.md`.

> **Evidence grade.** I used all 30 WebSearch calls. All 3 WebFetch attempts failed DNS (tinytapeout.com, pmc.ncbi.nlm.nih.gov, electronics-lab.com).
>
> I did get direct access to GitHub and GitLab over anonymous `git`. That let me pull **primary data** that no search snippet gives:
> - shuttle project counts for Tiny Tapeout and wafer.space;
> - SRAM macro LEF sizes for sky130 and GF180;
> - OpenRAM commit activity;
> - the community SRAM projects now in flight.
>
> These are tagged **[VERIFIED-git]**. Everything else is **[REPORTED]** (search snippet), **[ESTIMATE]** (computed or judged) or **[UNVERIFIED]**.

---

## 0. Verdict in five lines

1. **The wedge (C-33) is real, cheap to test and small.**
   - The gap holds: the largest free macros are 4 KB on sky130 and 1 KB on GF180, and only a 1 KB sky130 macro is silicon-verified [VERIFIED-git].
   - About **36 paying projects a year** reach this gap, which puts a serviceable ceiling of about **$0.75M/yr** on the wedge (`models/open-memory-ip.py` §2) [ESTIMATE].
2. **Economics (base case):**
   - 66% gross margin over 36 months.
   - First revenue in month 4 (Mar-2027) and three cash-positive months from month 8.
   - The founder can go full-time in month 20 (Jul-2028).
   - Recurring ARR is **$67k at m18 and $158k at m36**. The revenue run-rate, including services, is **$214k and $424k**.
   - The DRAM glut barely matters (the GLUT case gives $126k ARR at m36; SEVERE gives $106k), because macros are priced per design, not per GB.
3. **The biggest risk is not the DRAM cycle. It is free substitutes in the same channel.**
   - Open Circuit Design LLC (GF180 SRAM, Apache-2.0, last commit 2026-10-30), Chips4Makers (Arrakeen SRAM generator, test chips on wafer.space Run 2, Jul-2026) and UCSC OpenRAM (116 commits in 12 months) are all closing the gap for free.
   - With a free-bundle shock at m18, the founder never goes full-time and ARR at m36 is about **$50k**.
4. **The T2 climb is weaker than the hypothesis said.**
   - **C-32 (gain cell):** gain cells give **1.25–1.43× bitcell density in 65nm silicon** (vendor claims are 1.67–2.0×), not 2–4×. RAAAM (NXP-led $17.5M) is ahead, and Stanford's OpenGCRAM is free.
   - **C-22 (ReRAM): a cheap prototype path exists after all.** The Cadence SKY130 MPW ran a **Weebit-ReRAM option at $10–12k per block** in 2026, which corrects 01_LANDSCAPE. But a production part still needs a Weebit licence, a mask set and qualification (about $1–3M), and still competes with Toggle MRAM.
5. **Call:**
   - Run C-33 as a **T0 part-time wedge with a hard 30-day kill test**.
   - Treat gain-cell and ReRAM as **gated options funded only by STTR plus a seed round**: about $4.3M external, with no meaningful product revenue before month 36.
   - **This is not a venture-scale primary. It is a credible fallback or side line.**

---

## 1. Market: projects per year, the memory they need, what they pay

### 1.1 Shuttle and project counts (dated)

| Channel | Process / fab | Projects | Price to the designer | Source |
|---|---|---|---|---|
| Tiny Tapeout SKY26a / SKY26b | SkyWater 130nm (ChipFoundry CI2605) | **289 / 275** project dirs (2026) | ~€70/tile expected, devkit ~€300 | git tree count [VERIFIED-git] ([TT sky-26a](https://github.com/TinyTapeout/tinytapeout-sky-26a), [sky-26b](https://github.com/TinyTapeout/tinytapeout-sky-26b)); price ([eeNews, undated](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)) [REPORTED] |
| Tiny Tapeout SKY25a / SKY25b | SkyWater 130nm (ChipFoundry CI2509 / CI2511) | **~237 / 317** | same | [TT sky-25b](https://github.com/TinyTapeout/tinytapeout-sky-25b) [VERIFIED-git] |
| Tiny Tapeout IHP26a / IHP25a | IHP SG13G2 (Germany, *not U.S.*) | **283 / 329** | — | [TT ihp-26a](https://github.com/TinyTapeout/tinytapeout-ihp-26a) [VERIFIED-git] |
| Tiny Tapeout GF 0.2 | GF180MCU | **52** | — | [TT gf-0p2](https://github.com/TinyTapeout/tinytapeout-gf-0p2) [VERIFIED-git] |
| wafer.space Run 1 (G801) | GF180MCU | **40 slots**, 32 listed | ~$7–7.5k per full slot (1,000 dies) | [ws-run1](https://github.com/wafer-space/ws-run1) [VERIFIED-git]; [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2) [REPORTED] |
| wafer.space Run 2 (G802, Jul-2026) | GF180MCU | **54 slots** (18 full, 36 half, 9 quarter), 51 listed, 11 private | half slots new | [ws-run2](https://github.com/wafer-space/ws-run2) [VERIFIED-git] |
| ChipFoundry sky130 (Efabless successor, Umbralogic; assets bought 2025-09) | SkyWater 130nm | **not published**; Efabless chipIgnite did 80 commercial designs + 50 universities cumulatively | **$15k per 100 chips** (was $10k); a shuttle runs only if ≥50% full | [ChipFoundry acquisition](https://business.minstercommunitypost.com/minstercommunitypost/article/gnwcq-2025-9-3-chipfoundry-acquires-efabless-assets-to-propel-custom-silicon-innovation); [eeNews](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/); [EE Journal](https://www.eejournal.com/industry_news/efabless-empowers-40-commercial-companies-to-design-chips/) [REPORTED] |
| Cadence SKY130 MPW aggregation (2026 run) | SkyWater 130nm, **standard or Weebit-ReRAM option** | not published; "multiple runs per year" planned | **$10–12k per design block** (ReRAM at the upper end); deadline 2026-01-16, die July 2026 | [SkyWater/Cadence](https://www.skywatertechnology.com/lowering-barriers-to-silicon-cadence-launches-mpw-aggregation-service-for-sky130/) [REPORTED] |
| Google Open MPW (history, ended) | sky130 ×8 + GF180 ×1 | **360 designs fabricated** from 600+ submissions (40 slots per shuttle) | free | [Google, 2023-11](https://opensource.googleblog.com/2023/11/open-source-pdks-joining-linux-foundation-chips-alliance.html?m=0) [REPORTED] |
| Synopsys + GF university pilot (from fall 2025) | GF180MCU via GlobalShuttle | **40 universities** | sponsored | [Synopsys, 2025-09-04](https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms?asPDF=1) [REPORTED] |
| MOSIS 2.0 (USC ISI / CA DREAMS hub) | 12–350nm; GF value-added partner (Jul-2026) | access to **>35 MPW shuttles**; counts not published | — | [USC ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/); [AAC 2026-07](https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy) [REPORTED] |
| DoD Microelectronics Commons (8 hubs, ~$2B FY23–27) | various | **>61,000 chips fabricated domestically**; >1,500 members in 47 states (2026-03) | hub-funded | [NSTXL 2026-03](https://nstxl.org/microelectronics-commons-delivering-results-2026/) [REPORTED] |

**Market count used in the model** [ESTIMATE, `models/open-memory-ip.py` §2]:
- **Full-chip projects on U.S.-fab open/academic shuttles: ~298 per year.** That is wafer.space 2×54, ChipFoundry ~60, Cadence ~30, the GF university pilot 40, and MOSIS 2.0, the Commons and others ~60.
- **Tiny Tapeout's ~900 tiles a year are a funnel, not buyers.** A tile cannot hold an 8 KB+ macro.
- **Need and willingness to pay:** ×30% need memory beyond the free macros, and ×40% of those pay. That gives **~36 paying projects a year** and an active-account cap of **~72**.

### 1.2 What memory they need (primary evidence from the wafer.space listings) [VERIFIED-git]

- **Run 2: ~10 of 51 listed projects mention SRAM or RAM:**
  - TinyQV RISC-V SoC with 9.5 kB of scratch RAM;
  - FABulous eFPGA using SRAM macros;
  - bio180 (Baochip BIO) with 4 Kb of SRAM;
  - an SDRAM controller (SCUP) and a "retro DRAM controller" (AS04);
  - **four SRAM test chips**: Chips4Makers FS01/FS02/FS03 (3.3V with regular rules vs SRAM rules, and 5V) and OCD3.
- **Run 1:**
  - SERV multi-core SoCs with local SRAM per core (Racquet, 9–23 cores);
  - the OCD SRAM test chip (256 B / 512 B / 1 KB);
  - the Tillitis/Zedulo **eFUSE + SRAM** test chip (security keys).
- **Demand shape:**
  - 1–16 KB single- and dual-port SRAM for RISC-V scratch and caches;
  - register files and FPGA configuration memory;
  - one-time or non-volatile key storage (eFUSE today, ReRAM later);
  - external DRAM/SDRAM controller IP.

### 1.3 What they pay today

- **For memory IP: effectively $0.** The free options are:
  - OpenRAM (BSD-3);
  - OCD GF180 SRAM (Apache-2.0);
  - GF's fd_ip_sram (64–512 B);
  - DFFRAM (latch/flip-flop RAM up to 2,048 words);
  - Chips4Makers Arrakeen.

  No paid open-PDK macro vendor was found (consistent with the C-33 audit) [VERIFIED-git / REPORTED].
- **For silicon:**
  - ~€70 per TT tile;
  - ~$7–7.5k per wafer.space full slot;
  - $10–12k per Cadence block;
  - $15k per 100 chips at ChipFoundry.

  So a memory service must price at a **fraction of the slot price** for academics (≤$3k). Funded startups and SBIR teams can pay more (≤$10–20k), because a failed macro wastes the whole spin and 6 months [ESTIMATE].
- **Commercial NDA-PDK customers are not a market.**
  - SkyWater says its commercial S130 platform "already offers… SRAM compilers" ([SkyWater/Infineon release, 2025-07-29](https://www.silicon.co.uk/press-release/skywater-technology-expands-leadership-in-u-s-semiconductor-manufacturing-with-infineon-ip-license-agreement)) [REPORTED].
  - At mature nodes, foundry-sponsored compilers are traditionally **free to the designer**, with the foundry paying the IP vendor (the Artisan model: [D&R analysis](https://www.design-reuse.com/news/9192/analysis-arm-artisan-merger-defining-moment.html); [Arm 22nm foundry-sponsored compilers](https://us.design-reuse.com/industryexpertblogs/44866/arm-tsmc-22nm-ulp-ull-physical-ip-platform.html)) [REPORTED].
  - **The market is therefore only open-PDK teams.** That is the binding size constraint.

---

## 2. Competitors and prices

| Competitor | What | Price | Status (dated) | Threat |
|---|---|---|---|---|
| **OpenRAM** (UCSC VLSIDA, Guthaus) | Open SRAM compiler, sky130 + gf180mcu + freepdk45 + scn4m | Free (BSD-3) | v1.2.50 on 2026-10-27; **116 commits 2025-11-01 → 2026-10-27**. Prebuilt sky130 macros are **only 1/2/4 KB**; the 16 KB attempt left only a log. The **2 KB macro gives 57.6 kbit/mm²** against a bitcell limit of 527 kbit/mm² ([OpenRAM](https://github.com/VLSIDA/OpenRAM); [efabless/sky130_sram_macros](https://github.com/efabless/sky130_sram_macros)) [VERIFIED-git] | **High.** It can close the large-macro gap at any time; also the obvious STTR PI |
| **Open Circuit Design LLC** (Tim Edwards) | GF180 3.3V SRAM macros 64 B–1 KB | Free (Apache-2.0) | Last commit **2026-10-30**; 1 KB macro = 0.155 mm², **52.7 kbit/mm²**; silicon on wafer.space Run 1/Run 2 ([repo](https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram)) [VERIFIED-git] | **High** (GF180), and also the best **contract partner** |
| **Chips4Makers** (Arrakeen generator) | GF180 SRAM generator; test chips in 3 rule/voltage variants | Free | v0.3 taped out on wafer.space G802, Jul-2026 ([GitLab](https://gitlab.com/Chips4Makers/arrakeen-sram-testchip)) [VERIFIED-git] | **High** (GF180) |
| GF `gf180mcu_fd_ip_sram` | GF180 SRAM 64×8 … 512×8 | Free | Static since 2022-08; 512 B = **19.6 kbit/mm²** ([repo](https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram)) [VERIFIED-git] | Low |
| **DFFRAM** (AUCOHL) | Standard-cell latch/DFF RAM up to 2,048 words | Free | sky130A OK; **gf180mcuD flagged for hold violations** (2025-11) ([repo](https://github.com/AUCOHL/DFFRAM)) [VERIFIED-git] | Medium (small RAMs) |
| **OpenGCRAM** (Stanford, Wang et al.) | Open gain-cell (and SRAM) compiler, DRC/LVS-clean banks for commercial CMOS (TSMC N40) | Free (code "with final version") | arXiv 2507.10849 (Jul-2025), follow-up 2602.21278 (Feb-2026) ([arXiv](https://arxiv.org/html/2507.10849v1); [Stanford slides](https://dam.stanford.edu/assets/2025-retreat/dam-sr25-wang.pdf)) [REPORTED] | **High for C-32**: removes "compiler" as a moat |
| **RAAAM Memory Technologies** (Israel/Switzerland) | Proprietary 3T Si gain cell (GCRAM) | Not public (licence + royalty) | **$17.5M Series A led by NXP (Nov-2025)**; >$24M total (CB Insights $27.19M); 22 staff. Lead licensee is a top-10 TSMC customer (2024). **TSMC N2 test chip taped out Mar-2026** via Avnet ASIC (Jun-2026). **GF FDX test vehicle taped out; lead-customer access early 2027** (Sep-2026) ([AnySilicon](https://anysilicon.com/news/raaam-memory-technologies-raises-17-5-million-in-oversubscribed-series-a-led-by-nxp-semiconductors/); [Avnet](https://anysilicon.com/news/raaam-selects-avnet-asic-as-its-vca-partner-for-tsmcs-2nm-gcram-development-and-qualification/); [Silicon Saxony](https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/); [eeNews](https://www.eenewseurope.com/en/raaam-signs-lead-licensee-for-sram-replacement-technology/)) [REPORTED] | **Decisive for C-32** |
| **Mobile Semiconductor** (Seattle) | Commercial SRAM compilers incl. **SkyWater RH90** rad-hard SP/DP with bit interleaving and ECC; 180nm compilers licensed to **Sandia** | Not public | RH90 announced 2022-06-09 (DoD $170M rad-hard investment) ([SkyWater](https://www.skywatertechnology.com/skywater-announces-availability-of-sram-memory-compiler-for-90-nm-strategic-rad-hard-by-process-offering/); [D&R Sandia](https://us.design-reuse.com/news/45774/mobile-semiconductor-180nm-memory-compilers-sandia-national-laboratories.html)) [REPORTED] | **High for DoD/trusted**: already SkyWater's memory-compiler partner |
| SkyWater S130 in-house "SRAM compilers" | For NDA S130 customers; vendor unnamed | Bundled | 2025-07-29 release [REPORTED] | Closes the commercial S130 market |
| Synopsys; Arm Artisan → **Cadence** | Commercial compilers; foundry-sponsored at mature nodes | Not public; designer often pays $0 (foundry pays) | Cadence acquired Artisan foundation IP ([Silicon UK](https://www.silicon.co.uk/press-release/cadence-to-acquire-arm-artisan-foundation-ip-business)) [REPORTED] | Medium. **Cadence also runs the SKY130 MPW** and could bundle memory |
| Dolphin, sureCore, eMemory | Low-power SRAM / NVM IP | Not found | eMemory royalties track wafer prices; its 8-inch royalties fell 15.9% YoY ([Yahoo](https://finance.yahoo.com/markets/stocks/articles/ememory-technology-inc-roco-3529-030030531.html)) [REPORTED] | Low at open-PDK scale |
| **Weebit Nano** (for C-22) | ReRAM IP; S130 module = 256 Kb + control + ECC | Upfront ~$0.1M (first-ever) to $0.29M (DB HiTek) and $1.8–2.6M (onsemi), analyst estimates (01_LANDSCAPE §9), plus NRE and royalties. SkyWater's 2021 licence is non-exclusive, with fees "not material" and contingent on customers | TI licence (2026-02-27); 3 product customers taped out (quarter to 2026-06-30); cash A$167M ([DataCenterNews 2026-07-30](https://datacenter.news/story/weebit-lifts-guidance-after-chip-tape-outs-licence-wins); [Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/)) [REPORTED] | Supplier, not competitor; its first U.S. security licensee may hold the C-22 slot |
| Historical price anchor | Virage 1T-SRAM compiler, TSMC 0.18 µm | **From $300k list (2001)** | ([Design World](https://www.designworldonline.com/synopsys-enters-embedded-memory-market/)) [REPORTED] | Context only |

---

## 3. Gain-cell eDRAM evidence (C-32)

- **Mask adder: none.** 2T/3T Si gain cells use standard logic transistors. RAAAM/GF describe GCRAM as an SRAM replacement on standard FDX and N2, and OpenGCRAM generates banks "for commercially available foundry CMOS" ([arXiv 2507.10849](https://arxiv.org/html/2507.10849v1)) [REPORTED].
- **Density vs 6T SRAM: much less than the 2–4× in the hypothesis.**
  - **65nm silicon (Teman group, Bar-Ilan):** 16-kbit macros with **up to 20% (ISCAS 2021) and up to 30% (PRIME 2024) bitcell-area reduction vs SRAM**, i.e. **1.25–1.43× density** ([BIU CRIS](https://cris.biu.ac.il/en/publications/4t-gain-cell-providing-unlimited-availability-through-hidden-refr/)) [REPORTED].
  - **Vendor claims:** ~40% area saving (GF/RAAAM) and up to 50% (RAAAM via OpenGCRAM), i.e. **1.67–2.0×** [REPORTED].
  - **sky130 caveat** [ESTIMATE]:
    - The 1.896 µm² 6T cell uses SkyWater's SRAM build-space ("pushed") rules ([sky130_fd_bd_sram](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram)) [VERIFIED].
    - A gain cell drawn with logic rules may land near parity unless the foundry grants rule waivers.
    - Chips4Makers' G802 "regular vs SRAM design rules" test chips are testing exactly this effect on GF180.
- **Retention (sets refresh cost):**
  - **28nm:** 2T 0.14 µm² → **22.4 ns**; 3T 0.209 µm² → **50 ns** ([PMC review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9185588)) [REPORTED].
  - **65nm:** 16 kB 3T-1C macro with an on-chip boosted bias gives **>100 µs** ([JSSC 2025, Harel/Teman](https://cris.bgu.ac.il/en/publications/a-16-kb-65-nm-gc-edram-macro-with-internal-bias-voltage-generatio/)) [REPORTED].
  - **180nm:** a 0.18 µm silicon test chip verified a log-normal per-cell retention model, with write-transistor VT variation dominating ([Edri/Meinerzhagen/Teman, TCAS-I 2016](https://infoscience.epfl.ch/entities/publication/883bc084-69a3-4e4d-a683-5434f4cec673/articledetails)). 2T retention falls **>3 orders of magnitude from 180nm to 28nm** ([US 11,127,455](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11127455)). A 3T array showed **0.8 ms worst case at 900 mV** (node not in the snippet) ([TVLSI 2016](https://cris.iucc.ac.il/en/publications/single-supply-3t-gain-cell-for-low-voltage-low-power-applications/)) [REPORTED].
  - **At 130/180nm, then, expect tens of µs to ~1 ms**, shrinking at 85–125 °C [ESTIMATE].
- **So the gain-cell edge at 130nm is roughly:**
  - **standby leakage** (no 6T cross-coupled leakage path) and **two-port operation**;
  - a modest **1.2–2× bitcell density**;
  - minus a refresh controller and its power and availability overhead.
- **What the hypothesis missed: a bigger, cheaper density lever exists.** Banked 32–64 KB SRAM macros at ~60% array efficiency reach **~316 kbit/mm², 5.5× today's 2 KB OpenRAM macro**, with no new cell (`models/open-memory-ip.py` §1). That is compiler software, the founder's skill set. Gain cells add at most ~1.3–2× on top.
- **Verdict:** C-32 stays alive only as a sky130/S130 trusted-ASIC niche. RAAAM (silicon from 180nm to N2, NXP, GF, TSMC) can port at will, and OpenGCRAM removes the compiler moat. **Profitability: no to marginal. TRL 5 for this venture's macro.**

---

## 4. ReRAM on SkyWater S130 (C-22)

- **Qualification:** Weebit's 256 Kb 1T1R module in S130 is JEDEC-qualified (3 lots), with 10-year retention and qualification to 125 °C. The module includes control, decoders, IOs and **ECC** ([Weebit product page](https://www.weebit-nano.com/products/embedded-reram-ip/weebit-reram-nvm-in-skywater-130nm-cmos/); 01_LANDSCAPE §6.1 row 6) [REPORTED].
- **Access path after Efabless and the IonQ deal: better than 01_LANDSCAPE says.**
  - **Prototype:** the **Cadence SKY130 MPW aggregation offered a Weebit-ReRAM process option at $10–12k per design block** (deadline 2026-01-16, die July 2026, "students, researchers and start-ups", multiple runs per year planned) ([SkyWater/Cadence](https://www.skywatertechnology.com/lowering-barriers-to-silicon-cadence-launches-mpw-aggregation-service-for-sky130/)) [REPORTED]. **This corrects 01_LANDSCAPE §10.3 rule 8 ("no T0 path to a ReRAM test chip").**
  - **Open questions:**
    - (a) whether a post-July-2026 run is scheduled;
    - (b) whether use of the ReRAM block on that shuttle requires a Weebit evaluation licence;
    - (c) whether parts made from it can be sold.
  - **Production** needs a direct Weebit licence (fee + NRE + royalties) plus an S130 mask set (~$0.5–0.6M) and qualification (~$0.3–0.5M). That is **T1–T2**.
- **IonQ ownership:** the acquisition closed 2026-07-31. IonQ says SkyWater "remains fully committed to all of our semiconductor foundry customers", and SkyWater is a **DMEA Category 1A Trusted Foundry** ([IonQ](https://ionq.com/news/ionq-completes-acquisition-of-skywater-technology); [BusinessWire 2026-01-26](https://www.businesswire.com/news/home/20260125927336/en/IonQ-to-Acquire-SkyWater-Technology-Creating-the-Only-Vertically-Integrated-Full-Stack-Quantum-Platform-Company)) [REPORTED, company assertion; no post-close DMEA statement found].
- **Radiation (the DoD axis):**
  - Weebit's data covers only 16-kbit arrays under gamma (C-22 audit).
  - **Analogues:** NASA (2015) heavy-ion testing of a TaOx 1T1R ReRAM MCU found **no array bit upsets**; failures were single-event functional interrupts in the periphery ([NASA NTRS](https://ntrs.nasa.gov/api/citations/20150000273/downloads/20150000273.pdf)). Vanderbilt/imec (2014) found HfO₂ 1T1R SEUs driven by **access-transistor transients**, in the high-resistance state only ([imec](https://imec-publications.be/handle/20.500.12860/23537)) [REPORTED].
  - **Implication:** the cell is likely robust; bulk-CMOS S130 periphery is the weak point.
  - **No 2026 Weebit radiation qualification or U.S. defense customer was found.**
- **DoD demand for secure NVM:**
  - No 2026 SBIR/STTR topic for trusted or secure embedded NVM or memory compilers was found (searched, none returned).
  - The only memory-specific DoD topics found are extreme-environment NVM (DARPA DV017, closed 2026-08-19; 01_LANDSCAPE §7).
  - **Evidence that DoD funds memory IP at SkyWater:** the Mobile Semiconductor RH90 compilers came out of the DoD's $170M rad-hard investment (2022).
  - **Demand is real but slow and prime-mediated** [ESTIMATE].
- **Verdict:**
  - C-22's prototype cost falls from "T1" to about $12–25k per spin.
  - The product (1–4 Mb secure NVM) still needs ~$1.5–3M and 12–18 months of qualification after tape-out (Weebit's own figure), and it loses on density and endurance to U.S.-made Toggle MRAM.
  - **The narrow win:** magnet-immune key storage in a trusted U.S. flow. Keep it as an option, not a plan.

---

## 5. Funding

| Program | Fit | Terms (dated) | Source |
|---|---|---|---|
| **STTR** (university PI) | Gain-cell sky130 macro + test chip; trusted-memory characterization | Reauthorized through 2031-09-30. NSF Phase I up to **$305k** (NSF 26-510); Strategic Breakthrough up to $30M after Phase II. NSF **Semiconductors** topic includes an **IC Design** subtopic. Last Project Pitch deadline seen: 2026-07-27. **The founder cannot be SBIR PI while keeping the day job; STTR with a university PI works** | [NSF Seed Fund](https://seedfund.nsf.gov/topics/semiconductors/); [NSF 26-510 summary](https://grantedai.com/grants/semiconductors-s-sbir-sttr-program-national-science-foundation-nsf-small-bu-ef99bad7) [REPORTED]; 01_LANDSCAPE §7 |
| PI candidates | — | **UCSC VLSIDA (Guthaus, OpenRAM)**; **Stanford OpenGCRAM group**; East Coast: **Brown (Saligane lab, wafer.space Run 1 course tapeout)** | [ws-run1](https://github.com/wafer-space/ws-run1) [VERIFIED-git] |
| **NSF Chip Design Hub** (NSF 24-522) | A hub mandated to give academics EDA, PDKs and **design IP cores**, so a natural buyer or distributor of academic macro licences | 2024 solicitation | [NSF](https://www.nsf.gov/funding/opportunities/chip-design-hub-enabling-access-semiconductor-chip-ecosystem-design) [REPORTED] |
| **DoD Microelectronics Commons** | East Coast hubs: **NORDTECH** (NY; renewed 2026-04-29), **NEMC** (MA; **PROPEL** subsidizes lab and fab resources) | ~$2B FY23–27; year-3 project calls | [Cornell](https://research-and-innovation.cornell.edu/?p=6460); [MassTech](https://masstech.org/news/northeast-microelectronics-coalition-hub-celebrates-3725-million-federal-funding-power) [REPORTED] |
| MOSIS 2.0 / CA DREAMS | Channel more than funder | GF value-added partner (2026-07) | above |
| State | MA START ($100–500k for SBIR Phase II companies), VA CCF, NY (megaproject-heavy) | 01_LANDSCAPE §7 [UNVERIFIED-L/M] | — |
| CHIPS / NSTC | ≈$0 for us | 01_LANDSCAPE §7 | — |

**A DoD/Navy/AF SBIR topic on memory compilers or trusted memory IP in 2026: not found** [gap].

---

## 6. Unit economics (from `models/open-memory-ip.py`)

| Product line | Price | COGS | GM |
|---|---|---|---|
| A1 Subscription, academic | $200/mo | $58 | 71% |
| A2 Subscription, commercial | $800/mo | $102 | 87% |
| B1 Tapeout service, academic | $3,000 | $1,690 | 44% |
| B2 Tapeout service, commercial | $10,000 | $4,150 | 58% |
| C Characterized macro licence (12-mo warranty) | $20,000 | $6,350 | 68% |

- **Acquisition:**
  - 30 contacts/mo part-time × 25% reply × 15% close = 1.1 accounts/mo, plus inbound ramping to 1.2/mo.
  - Loaded CAC ~$1.3k, against lifetime gross profit of $5.4k (academic) and $31k (commercial).
  - The close rate is the unverified input the kill test measures.
- **Characterization costs (one-time):**
  - wafer.space GF180 half slot ~$3.75k (m4) and full slot ~$7.25k (m16);
  - ChipFoundry sky130 slots $15k (m7, m19);
  - test bench $4k;
  - characterization contractor 3 × 40 h × $125.

  These come to **$60k over 24 months** ($67.5k including the $7.5k build-out in m2–m3), funded from operating cash after month 7.
- **Royalties at trailing nodes:** no royalty line in the wedge. Royalty pools are small at sky130/GF180 volumes, and eMemory's 8-inch royalties fell 15.9% YoY. A royalty appears only in the T2 overlay [REPORTED / ESTIMATE].

| Scenario | 3-mo cash-positive from | Founder full-time | ARR m12 / m18 / m24 / m36 (recurring) | Run-rate m18 / m36 (incl. services) | Cash low |
|---|---|---|---|---|---|
| **BASE** | m8 (Jul-2027) | m20 (Jul-2028) | $41k / $67k / $106k / $158k | $214k / $424k | $20.4k at m7 |
| **GLUT** (DDR5 −60% from 2028-Q1) | m8 | m25 (Dec-2028) | $41k / $59k / $78k / $126k | $184k / $342k | $20.4k |
| **SEVERE** ($2.04/GB) | m8 | m30 (May-2029) | $41k / $55k / $71k / $106k | $167k / $291k | $20.4k |
| BASE + free-bundle shock at m18 | m8 | **never** | — / $50k (m18) / — / **$50k** | — / $154k | $20.4k |
| SEVERE + price, close, churn and COGS all adverse 30% | m20 | **never** | $26k (m18) / $43k (m36) | $122k (m36) | **−$14.7k** (needs ~$15k more capital) |

- **Most sensitive inputs:** price ×0.7 → full-time never (cash-positive only from m20); close rate ×0.7 → full-time slips to m27.
- **What must be true:** about **18 active paying accounts (≈11 academic + 7 commercial) by month 18** to pay the founder full-time. That is **25% of the whole wedge cap (72)**, or about 2 commercial tapeout services or 0.9 licences a month.

---

## 7. First ten customers (named or precisely typed; where to find them)

| # | Candidate | Type | Why they buy | Where found |
|---|---|---|---|---|
| 1 | **Brown University, ENGN2912e (Saligane lab)** | U.S. course/lab, East Coast | Taped out on wafer.space Run 1 (project BRWN). Course tapeouts need >1 KB GF180 SRAM; also an STTR PI candidate | [ws-run1](https://github.com/wafer-space/ws-run1) [VERIFIED-git] |
| 2 | **U.S. members of the Synopsys–GF GF180MCU university pilot** (40 universities) | Course instructors | A recurring tapeout every term; largest free GF180 macro is 1 KB | GF University Partnership Program / Synopsys SARA contacts ([Synopsys 2025-09-04](https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms?asPDF=1)) |
| 3 | **Avalon Semiconductors** (AS03/AS04 multi-project dies) | Small commercial aggregator | Multi-project dies with RISC-V cores and a DRAM controller; recurring wafer.space customer | [ws-run1](https://github.com/wafer-space/ws-run1), [ws-run2](https://github.com/wafer-space/ws-run2) |
| 4 | **TinyQV / Tiny Tapeout SoC builders** | Open SoC designers | Already pushing 9.5 kB scratch RAM on GF180 (TQVE); a memory tile/macro offering for TT | [ws-run2](https://github.com/wafer-space/ws-run2) |
| 5 | **FABulous eFPGA (mole99)** | Open FPGA fabric | Uses SRAM macros for configuration; needs denser configuration memory | [ws-run2](https://github.com/wafer-space/ws-run2) |
| 6 | **Cloneless (tamper-resistant ASIC series)** | Hardware-security research | Secure key storage; a natural first ReRAM (C-22) prototype partner | [ws-run1/run2](https://github.com/wafer-space/ws-run2) |
| 7 | **Sandia National Laboratories (MESA)** | DoD/DOE lab | Already licensed commercial 180nm compilers (Mobile Semiconductor); a trusted-flow characterized-macro buyer | [D&R](https://us.design-reuse.com/news/45774/mobile-semiconductor-180nm-memory-compilers-sandia-national-laboratories.html) |
| 8 | **DoD SBIR/STTR performers taping out on SkyWater 130/90nm** | Funded small businesses | Need U.S.-fab, characterized memory with a warranty | SBIR.gov award search ("SkyWater", "130nm", "sky130", "ASIC") [method; not run this session] |
| 9 | **NORDTECH (NY) and NEMC (MA) hub project teams** | Commons-funded prototyping | East Coast; PROPEL subsidizes lab and fab cost | nordtechub.org, nemicroelectronics.org |
| 10 | **Channels: ChipFoundry Marketplace, Cadence SKY130 MPW, MOSIS 2.0** | Resellers/bundlers | List macros per shuttle; *also the parties most able to bundle for free* | [ChipFoundry](https://github.com/chipfoundry/caravel_user_project); Cadence MPW; MOSIS 2.0 |

- **Partner-or-competitor to approach first:**
  - **Open Circuit Design LLC (Tim Edwards)**, as contract characterization partner;
  - **UCSC VLSIDA**, as STTR PI and upstream.

---

## 8. Honest ceiling and the path to T2

- **Wedge ceiling:**
  - ~$0.75M/yr serviceable at full share; the model reaches a ~$0.42M run-rate at m36 in BASE with ~30 accounts.
  - This matches the Phase 3 scorers' "<$0.5–1M ARR lifestyle line".
  - **It is glut-proof.** A 60% DDR5 drop costs about 20% of m36 ARR, through commercial design starts only.
  - **It is not proof against free substitutes**, the decisive risk.
- **Path to T2** (`models/open-memory-ip.py` §9), with roughly **$4.3M external** before a qualified macro:
  1. STTR Phase I with a university PI, submitted m6–m9 and awarded ~m15 ($305k): gain-cell sky130 macro and 2 spins.
  2. A Cadence ReRAM MPW probe (~$12k, m18).
  3. Weebit evaluation (~$100k anchor; fee for a startup unknown).
  4. STTR Phase II (~$1.5M, ~m30).
  5. A seed round (~$2.5M, m27–30), conditional on ≥$250k wedge ARR and gain-cell silicon.
  6. A full-time circuit cofounder ($220k/yr loaded).
  7. A ReRAM chiplet mask set plus qualification (~$0.95M, m36–54).
- **Timing:** at most **one gain-cell evaluation licence before m36**. ReRAM product revenue comes after m40.
- **Who funds it:** NSF/DoD STTR, then a seed round. Strategic interest from SkyWater/IonQ (trusted-foundry IP catalog) or a defense prime is plausible but **unevidenced**.

---

## 9. Kill experiment (<$10k, <30 days)

**Hypothesis to kill:** "Funded open-PDK teams will pay for larger, characterized macros, and no one in the channel will give them away within a year."

1. **Days 1–7 (~$2.4k):**
   - Use OpenRAM in the cloud to generate DRC/LVS-clean **8/16/32 KB sky130** and **2/4/8 KB GF180** macros with simulated Liberty files.
   - Hire a contract memory designer for 16 h (~$2k) to check timing margins on the ≥16 KB macros. *This tests whether OpenRAM can produce working large macros at all*: the published 16 KB sky130 attempt left only a log.
   - Publish previews (LEF and datasheet only) on a landing page with real prices: $200/$800 per month; $3k/$10k per tapeout; $20k licence. Take refundable **$500 deposits** to "reserve a characterized macro for the next ChipFoundry/wafer.space deadline".
2. **Days 3–25 (~$0.2k):**
   - Send named outreach to **~120 contacts**: every public wafer.space Run 1/Run 2 project owner (~70), Tiny Tapeout SoC builders, U.S. GF-pilot instructors, ~20 SBIR performers on SkyWater, NORDTECH/NEMC hub managers, and MOSIS 2.0.
3. **Days 7–20 (no cost):** five channel calls.
   - **ChipFoundry:** marketplace terms; any plan for free large macros?
   - **Cadence MPW:** next SKY130/ReRAM run date; open to bundling?
   - **UCSC VLSIDA:** roadmap for characterized large macros; interest in being STTR PI?
   - **Open Circuit Design:** roadmap; availability as a contractor?
   - **Weebit:** fabless evaluation terms, and whether die from the Cadence ReRAM MPW can be used in a paid product.
4. **Budget:** ~$2k contractor, $0.3k compute, $0.2k web/Stripe/domain, $0.1k Sales Navigator, $1k IP/terms template, ≤$1.5k for one hub event. **Total ≈ $5k.**
5. **Kill on day 30 if any one of these is true:**
   - (a) fewer than **3 paid deposits or pre-orders**, or less than **$15k in signed LOIs**;
   - (b) ChipFoundry, Cadence, UCSC or OCD confirms **free silicon-characterized ≥16 KB macros within 12 months**;
   - (c) the reviewer finds OpenRAM cannot produce timing-clean ≥16 KB sky130 macros without more than ~200 h of custom work.

   **Continue if** ≥3 paid and at least one commercial or SBIR buyer commits at ≥$10k.

---

## 10. Corrections to earlier phases (carry forward)

1. **01_LANDSCAPE §10.3 rule 8 / §0 item 12** said there is no T0 path to a ReRAM test chip. **Corrected:** the Cadence SKY130 MPW offered a Weebit-ReRAM option at $10–12k per block in 2026 [REPORTED]. Production licensing and the next run are still unknown.
2. **The DD5 hypothesis said gain cells give "~2–4× SRAM density".** **Corrected:** 1.25–1.43× in 65nm silicon and 1.67–2.0× in vendor claims. At sky130 it may be near parity with the pushed-rule 6T cell [ESTIMATE].
3. **C-33 said "only 1–4 KB sky130 macros exist".** **Holds** [VERIFIED-git]. **Added:** the GF180 gap is larger (max free macro 1 KB), and the community is actively filling it for free (OCD, Chips4Makers).
4. **Commercial S130 already ships SRAM compilers**, and mature-node compilers are foundry-sponsored, so the buyer set is open-PDK teams only.
5. **RAAAM status updated:** N2 test chip taped out Mar-2026; GF FDX test vehicle taped out; lead-customer access early 2027.

---

## 11. Open gaps

- ChipFoundry's real 2026 shuttle count, price and marketplace terms (chipfoundry.io was not reachable).
- The Cadence SKY130 MPW schedule after July 2026, the ReRAM-option licence terms, and whether die can go into a product.
- The Weebit fee for a fabless startup (only ~$0.1M first-ever, $0.29M and $1.8–2.6M anchors).
- Measured retention for a gain cell **on sky130/GF180** (none found). The 180nm paper values sit behind a paywall; full text of TCAS-I 2016 / JSSC 2025 is needed.
- Any 2026 DoD SBIR/STTR topic on memory compilers or trusted NVM (none found).
- Whether SkyWater's DMEA accreditation was re-confirmed after the IonQ close.
- **Willingness to pay for characterized macros: zero data.** This is what the kill experiment measures.
- Whether NSF Chip Design Hub awardees buy or distribute design-IP licences.
