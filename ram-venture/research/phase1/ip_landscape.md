# Phase 1: Patent, licensing and tech-transfer landscape for memory (mission §3A and §3E)

**Agent:** `p1-ip` · **Written:** 2026-11-01 · **Owner files:** this file, `research/sources/p1-ip.jsonl`, `research/assumptions/p1-ip.md`

> **Read this first: evidence limits.** I had **no live web access**.
> - My first WebSearch call came back "budget used up". All agents in this run share a 200-call cap, and it was spent before I started.
> - WebFetch failed DNS for every host I tried: neosemitech.com, patents.google.com, en.wikipedia.org and techfinder.stanford.edu.
> - Per the tool instructions, I did not route around either block.
>
> As a result:
> - **No fact below is [VERIFIED] by me.**
> - Facts with a URL come from **other agents' search results** (A1, A2, A3, B, p1-*). They are logged as CROSS-REFERENCE in `sources/p1-ip.jsonl` and tagged **[REPORTED]**.
> - Facts with no URL are my **training knowledge**, tagged **[UNVERIFIED-training]**. They are not re-checked as of 2026-11-01.
> - I give no tech-transfer docket numbers, because none could be retrieved. §6 lists the targets by institution, inventor and evidence. §9 is a **verification queue** with exact queries to run once access returns.
> - Treat every "patent number" here as a pointer to check, not as a cited fact.

---

## 0. Bottom line (decision-relevant, ranked)

1. **Every DRAM-class technology's corporate IP is closed to a startup.** This covers oxide-semiconductor DRAM, 3D DRAM, HfO₂ ferroelectric DRAM and 3D XPoint/PCM.
   - The independents that do license, NEO Semiconductor (3D X-DRAM) and FMC (HfO₂ DRAM+), sell **only to fab-owning memory makers or foundries**.
   - Sources: [eeNews Europe, 2017](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-to-be-the-arm-of-memories/); [HPCwire, 2025-11-13](https://www.hpcwire.com/off-the-wire/fmc-raises-e100m-to-set-new-standards-for-memory-chips/); [StorageNewsletter, 2026-04-23](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/) [REPORTED].
   - A <$50k founder cannot be their customer. **Licensability: closed.**
2. **Memory IP that is licensable *and* U.S.-manufacturable today is all embedded/NVM, not DRAM.** Four paths:
   - **(a) Weebit ReRAM in SkyWater S130**, Bloomington MN. Qualified in 2023 and in the PDK ([Weebit, 2023-06](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/)). TI took a license on 2025-12-29 ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nano-secures-a-license-agreement-with-texas-instruments/)).
   - **(b) Everspin Toggle MRAM process tech.** A $40M, 2.5-year transfer to a U.S. defense prime (Amentum) in Apr-2026 ([Electronics360](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services)).
   - **(c) Sandia HZO FeRAM/FTJ**, integrated into the trusted MESA fab at 200mm on 2026-05-13 ([Sandia](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/)). Path: license plus CRADA. *v2 (2026-11-01): no public licensing listing or CRADA offer surfaced. This is internal LDRD work, so licensability is [UNVERIFIED].*
   - **(d) OpenRAM SRAM compiler**, BSD-3 and free, supporting sky130 ([GitHub, opened by A3](https://github.com/VLSIDA/OpenRAM)).
   - All [REPORTED].
3. **Most "basic" patents are already public domain. That does not buy freedom to operate.** [UNVERIFIED-training; ESTIMATE 20-year rule]
   - STT switching (IBM/Slonczewski, US 5,695,864, 1995 filing): expired ~2015.
   - Toggle MRAM (Motorola, US 6,545,906, ~2001): expired ~2021.
   - PMC/CBRAM (ASU/Kozicki, US 5,761,115, 1996): expired ~2016.
   - PZT FeRAM cell (Ramtron): 1980s–90s, expired.
   - Z-RAM and T-RAM: early 2000s, expired or expiring 2018–2026.
   - a-IGZO TFT (JST/Hosono, ~2003–04): ~2023–25.
   - **HfO₂ ferroelectric base (Qimonda, ~2007): expires ~2027–28.**
   - What a startup would actually infringe is the **2006–2026 improvement and integration estates**: SEL in oxide semiconductors, Samsung/SK hynix/Micron in VCT/3D, and Micron/Intel/FMC in HfO₂.
4. **Two live litigation hot zones bear directly on §3B/§3C concepts.**
   - **Netlist (DIMM/PMIC/HBM).** E.D. Tex. verdicts: **$303M vs Samsung (2023-04)**, **$445M vs Micron (2024-05)**, **$118M vs Samsung (2024-11)**. The PMIC-on-DIMM claims read on DDR5 RDIMMs. Appeals and PTAB outcomes for 2025–26 are UNKNOWN [UNVERIFIED-training].
   - **Avalanche v. Everspin**, ITC 337-TA-1487 (STT-MRAM; asserted US 9,318,179, 9,419,210, 11,678,586 and 10,490,737, plus a parallel D. Del. suit). Instituted 2026-02-27; no final determination as of 2026-11-01; target date ~Jul-2027 ([USITC](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm); [Bloomberg Gov](https://news.bgov.com/ip-law/avalanche-beats-early-bid-to-end-itc-patent-case-over-fee-errors)) [REPORTED]. Everspin booked **$6.0M of litigation cost in Q3-2026 alone** ([Everspin 8-K](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm)) [REPORTED].
5. **University and national-lab licensing is cheap and reasonably fast. It is not the bottleneck.**
   - Typical startup terms: option **$1k–10k**; exclusive license in **2–6 months**; **2–10% equity**; **1–5% running royalty** (1–3% typical for semiconductor components). Past patent costs of **$10k–150k** are usually the largest cash item and are often deferred [UNVERIFIED-training].
   - The binding constraints are elsewhere: (i) a fab that will run the module, (ii) the lab's unpatented know-how, (iii) a technical PI. Bayh-Dole §204 and DOE's 2021 U.S.-manufacturing rule make licensed federally funded IP a "Made in USA" asset, but also **restrict offshore fabbing** (e.g., TSMC/TSRI) without a waiver [UNVERIFIED-training].
6. **Being a memory-IP *licensor* is a slow business.**
   - Weebit, the best-run independent ReRAM licensor, took ~10 years to reach **≥A$13.5M FY26 revenue guidance** ([Weebit, 2026-07](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/)). *v2:* **FY26 actual was A$15.28M**, all licence and NRE, with no royalties yet; first royalties are expected in CY2027 ([Kalkine, 2026-08-28](https://kalkinemedia.com/au/news/announcements/weebit-nano-reports-153-million-revenue-for-fiscal-year-2026)) [REPORTED].
   - Everspin's whole licensing/royalty/services line was **$6.9M in FY2025** ([BusinessWire, 2026-03-04](https://www.businesswire.com/news/home/20260304733194/en/Everspin-Reports-Unaudited-Fourth-Quarter-and-Full-Year-2025-Financial-Results)).
   - FMC has raised €120M+ over ~9 years with no product on the market ([heise, 2026](https://heise.de/-11151026)).
   - All [REPORTED]. **The founder should be a licensee building a product, not a licensor.**
7. **Distressed and orphaned estates are a real but niche option.** Candidates:
   - 4DS Memory: suspended from ASX quotation 2026-04-29 ([filings](https://financialfilings.com/companies/4ds-memory-limited/)) [REPORTED].
   - Antaios (SOT-MRAM): listed "closed" ([Dealroom](https://app.dealroom.co/companies/antaios)) [UNVERIFIED].
   - Spin Memory: ceased operations ~2021 [UNVERIFIED-training].
   - Nantero NRAM: no 2025–26 news found. A third-party directory tags it "Defunct" (2026-09) ([apis.io](https://apis.io/providers/nantero/)) [UNVERIFIED].
   - HPE memristor estate: shelved 2016 ([The Register](https://www.theregister.com/2016/11/29/hp_labs_delivered_machine_proof_of_concept_prototype_but_machine_product_is_no_more/)).

   These patents could be bought cheaply, but a patent without a fab and a customer is a litigation asset, not a business.

**Correction to the mission premise (§3E).** The mission calls university/lab licensing "an underused path for a small team". That is **true on cost and access**: option fees are T0-sized. It is **false as a shortcut to revenue**:
- No surveyed university memory technology is past TRL 4–5 on a U.S. production line. The exceptions are Sandia's HZO (internal trusted fab) and Purdue's 200mm oxide BEOL demo (research tool).
- The fastest IP-enabled revenue comes from **commercial** IP already in a U.S. PDK (Weebit/SkyWater, OpenRAM) or from buying finished parts (Everspin). Patent exhaustion means no license is needed to resell or design in a purchased part.
- University IP fits the **T1 STTR moonshot**, not the 18-month revenue line.

---

## 1. Summary table (required)

Licensability for a **small U.S. startup**:
- **Open:** published license or PDK-integrated commercial IP.
- **Likely:** an active licensing program, or a tech-transfer office with a startup track record.
- **Closed:** no licensing to non-IDMs seen.

Litigation risk:
- **HIGH:** an active suit or verdict on this product class in 2023–26.
- **MED:** a dense incumbent estate with an assertion history nearby.
- **LOW:** none seen.

| Technology | Key IP holders | Licensability | Expiring basics? | Litigation risk | Best licensing path for a startup |
|---|---|---|---|---|---|
| **Oxide-semiconductor DRAM** (IGZO/ITO/IWO/In₂O₃; 2T0C, 3T, 1T1C, OCTRAM) | **SEL** (dominant estate; DOSRAM/NOSRAM marks), JST/Hosono (a-IGZO base), Kioxia+Nanya (OCTRAM), Samsung (IGZO 4F² VCT), SK hynix, Micron, TSMC, imec (member-licensed), Sharp (CAAC co-dev), Huawei, IMECAS | Corporate: **Closed**. SEL: **likely but costly**; it licenses panel makers and has no startup program seen. U.S. universities: **Likely** | **Partly.** a-IGZO TFT base ~2023–25 expired. CAAC-IGZO (~2009–12) live to ~2029–32. Memory-cell filings (2010–26) live | **MED-HIGH** (SEL density; a 2T IGZO gain cell already granted, US 12,191,135, assignee unverified) | Option a **Purdue (In₂O₃, 200mm M3D)** or **Georgia Tech (IWO 3T eDRAM)** cell/process plus an SEL FTO search. Stay out of 4F² VCT |
| **Ferroelectric** (HZO FeRAM/FeFET/FeCAP/FTJ; PZT legacy; AlScN) | **FMC** (DE), NaMLab/Fraunhofer IPMS, Qimonda estate (HfO₂-FE discovery), **Micron** (NVDRAM), **Intel** (BEOL FeCAP, e.g. US 11,751,402), Samsung, SK hynix, Kepler Computing, SunRise (3D NOR), **Sandia** (rad-hard HZO); PZT: Infineon (Ramtron/Cypress), TI (licensee), RAMXEED; AlScN: Penn + AFRL | FMC/Micron/Intel: **Closed**. **Sandia: Unconfirmed** (license + CRADA hoped for; no public listing found, v2). Penn AlScN, Notre Dame/GT FeFET, Purdue FeS-FET: **Likely** | **Yes** for PZT FeRAM (expired). **HfO₂-FE base ~2027–28** [ESTIMATE]. Integration patents live | **LOW-MED** now; no major FE suits seen. Rises when products ship | **Sandia HZO license + CRADA + STTR** for rad-hard NVM. Or **Penn AlScN** for >500 °C NVM (USAF/DARPA demand) |
| **MRAM** (Toggle, STT, SOT, VCMA) | **Everspin** (Motorola/Freescale estate), **Avalanche**, IBM (STT origin), Samsung, TSMC, GF, Tohoku/CIES (pMTJ), NVE (early spintronics), Spin Memory (defunct), Antaios (closed?); universities UMN, Cornell, UCLA, Northwestern, MIT | Everspin: **Likely, at defense-prime scale** ($40M Amentum precedent). Avalanche: foundries only. Fabs: **Closed**. University SOT/VCMA: **Likely** | **Yes:** STT concept ~2015, Toggle ~2021, MgO-MTJ ~2021–25 expired. pMTJ CoFeB/MgO (~2009–10) to ~2029–30 | **HIGH** (Avalanche v. Everspin ITC 337-TA-1487) | **Buy Everspin parts** (exhaustion: no license needed) or partner with Everspin on defense. University SOT only for a T2 moonshot |
| **ReRAM / memristor / CBRAM** | **Weebit/CEA-Leti**, **Crossbar** (UMich lineage), **TetraMem**, HPE (memristor), 4DS (suspended), **GF** (bought Adesto/Dialog CBRAM from Renesas 2023), TSMC/Infineon (embedded), Panasonic→Nuvoton, ASU/Axon (PMC base) | **Weebit: Open** via SkyWater S130 PDK; startup terms unknown (analyst-estimated upfront fees ~$0.3M for a foundry, $1.8–2.6M for an IDM, plus NRE and royalties; v2). **TetraMem: Open** (states IP is licensable). Crossbar: Likely. GF CBRAM: **Closed**. 4DS/HPE: distressed or unknown | **Yes:** PMC/CBRAM base ~2016 expired. HP memristor (2008+) live to ~2028+ | **LOW-MED** | **License Weebit ReRAM through SkyWater S130** for a U.S.-made eNVM/secure part. UMich/UMass/USC only for an analog-CIM moonshot |
| **PCM / 3D XPoint** | **Intel & Micron** (XPoint/OTS estate, stranded), IBM (analog-AI PCM), ST+Samsung (ePCM, captive), SanDisk (3D Matrix Memory), SK hynix (selector-only memory), Ovonyx/ECD lineage | **Closed** (no program; captive) | **Yes** for Ovshinsky-era base. XPoint (2005–15 filings) live to ~2025–35 | **LOW** now. **Latent:** a stranded XPoint estate could be sold to NPEs | None. Resale of used Optane (A2-11) needs **no license** (exhaustion) |
| **Capacitor-less Si DRAM** (Z-RAM, T-RAM/TCCT, FBC, Kilopass VLT) | Micron (reportedly ISi Z-RAM estate), Stanford (Nemati/Plummer TCCT base), T-RAM (defunct), Synopsys (Kilopass VLT, 2018), Toshiba (FBC), **Unisantis** (SGT/DFM; licensing company) | **Effectively open** for early art (expired). Unisantis licenses actively | **Yes:** 1998–2006 filings expired 2018–26 | **LOW**; except Unisantis vertical-transistor claims (MED for any VCT) | Free to practice the early art, but the physics killed it (A3 post-mortems). **Nothing worth licensing** |
| **3D DRAM** (VCT/4F², VS-DRAM, 3D X-DRAM, 3D 2T0C) | Samsung, SK hynix, Micron, CXMT, Kioxia/Nanya, **NEO Semiconductor**, Unisantis, imec, IMECAS, tool makers (Lam/AMAT/TEL) | **Closed** for a startup. NEO licenses to IDMs only | **No** (2015–26 filings) | **HIGH, later** (from 2028, when products ship) | None. Not a startup play |
| **NRAM (CNT)** | **Nantero** (Woburn MA; Fujitsu license 2016) | **Unknown.** No 2025–26 news found; a directory tags it "Defunct" (v2); possibly a distressed estate | Early (2001–04) filings expired ~2021–24 | LOW | Verify status and assignments. A distressed buy is possible, but 20+ years without volume |
| **2D / CNT-FET / organic / printed** | Universities (Northwestern, UT Austin, Penn State, Stanford, MIT); Thinfilm (exited) | **Likely** (universities, cheap) | Organic-memory early filings expired | LOW | Not worth licensing (TRL 2–4) |
| **SRAM / open-source macros** | OpenRAM (BSD-3), SkyWater sky130 open PDK | **Open** | n/a | LOW | Use freely (A3-04) |
| *Adjacent §3C:* **DRAM modules / interfaces** | **Netlist** (LRDIMM, rank multiplication, **PMIC-on-DIMM**, HBM), Rambus, Polaris Innovations (Qimonda DRAM estate) | Netlist: license **unlikely** for a small entrant. Rambus: licensable for fees | Older DIMM patents expired. **Netlist PMIC family (2010s) live** | **HIGH** | **Buy finished modules from licensed makers.** Run FTO before any DDR5 RDIMM/MRDIMM |

---

## 2. How to read "expired" (patent-term mechanics)

- **Term.** U.S. utility patents filed on or after 1995-06-08 run **20 years from the earliest non-provisional US/PCT filing**, plus any patent-term adjustment (PTA). Patents filed earlier run the later of 17 years from grant or 20 years from filing. Maintenance fees fall due at 3.5, 7.5 and 11.5 years; many patents lapse early for non-payment. Large-entity fees are ~$2,150, $4,040 and $8,280 after the 2025 fee rule; small entities pay 40% and micro entities 20% [UNVERIFIED-training].
  - **Practical rule for 2026-11:** anything first filed **before ~Nov-2006** is expired unless it has PTA. The patent office's assignment and fee-status records show lapses.
- **Foreign counterparts** (JP/KR/TW/CN/EP) follow the same 20-year logic. A product sold only in the U.S. needs only U.S. FTO.
- **Expired base ≠ freedom to operate.** Every §3A technology has a dense **second-generation estate** of integration, materials, cell-layout, sense-amp and process patents (2006–2026) owned by incumbents. Two examples:
  - SEL keeps filing oxide-semiconductor memory families, such as the DOSRAM family ([USPTO 10,276,578](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10276578); [Justia 11,404,107](https://patents.justia.com/patent/11404107)) [REPORTED].
  - A **2T IGZO gain cell** was granted in 2025 ([USPTO 12,191,135](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12191135); assignee not verified) [REPORTED].
- **Know-how is not in the patents.** Deposition recipes, anneal windows, PBTI mitigation and MTJ etch are trade secrets. A university license usually includes a paid **know-how/consulting** clause or a sponsored-research agreement. Budget for it.
- **Patent exhaustion is the cheapest "license".** Buying an authorized part (Everspin MRAM, Infineon F-RAM, Weebit-enabled SkyWater wafers) lets you use and resell it without your own license. Module, appliance, recert and brokerage concepts (§3B–D) should rely on this, **except** where the module itself practices separate claims (Netlist PMIC-on-DIMM, §4).

---

## 3. Technology by technology

### 3.1 Oxide-semiconductor DRAM (IGZO/ITO/IWO/In₂O₃ gain cells; 1T1C OCTRAM)

**Who holds the key IP**
- **Semiconductor Energy Laboratory (SEL, Atsugi, Japan).** The single largest oxide-semiconductor estate.
  - SEL is an R&D-and-licensing company. Founder Shunpei Yamazaki is reported to be the most prolific patent inventor on record, with well over 10,000 patents [UNVERIFIED-training].
  - SEL co-developed **CAAC-IGZO with Sharp (2012)** ([Compound Semiconductor](https://compoundsemiconductor.net/article/89586/Revolutionising_displays_with_indium_gallium_and_zinc_oxide_technology)) [REPORTED].
  - It licenses CAAC-IGZO to panel makers: JDI co-development and an LG Display license renewal ([Display Daily](https://displaydaily.com/jdi-enters-agreement-with-sel/)) [REPORTED].
  - Its memory brands: **DOSRAM** (oxide-semiconductor DRAM; registered SEL mark) and **NOSRAM** (oxide gain-cell NVM). The DOSRAM patent family is live ([USPTO 10,276,578](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10276578)) [REPORTED]. SEL papers report DOSRAM leakage ≤200 zA (via A1).
  - **Implication:** any IGZO 1T1C or 2T0C memory sold in the U.S. needs an **SEL FTO review first**. SEL licenses large firms. No startup program and no published terms were seen. [UNVERIFIED-training]
- **JST / Tokyo Tech (Hideo Hosono).** Holds the amorphous-IGZO TFT base (Nomura et al., *Nature* 2004).
  - JST licensed it to Samsung (2011) and others [UNVERIFIED-training].
  - Base filings date from ~2003–05, so **expired or expiring 2023–25** [ESTIMATE: 20-year rule].
  - This frees the *material*, not the *memory cell*.
- **Kioxia + Nanya.** **OCTRAM** (IEDM 2024): 4F² vertical InGaZnO transistor on a capacitor, Ioff <1 aA/cell, a 275 Mbit array ([BusinessWire, 2024-12-09](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology)). At IEDM 2025 they showed eight stacked IGZO transistors ([Kioxia, 2025-12-12](https://www.kioxia.com/en-jp/about/news/2025/20251212-1.html)) [REPORTED]. Joint development; **closed**.
- **Samsung.** Reported 10a-class (sub-10nm) DRAM working die using **4F² VCT with an IGZO channel** (Mar-2026), targeting 2028 production ([TrendForce, 2026-04-24](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)) [REPORTED]. Implies a very large 2020–26 filing wave on VCT/IGZO integration. **Closed**.
- **SK hynix:**
  - 5-layer stacked 3D DRAM at 56.1% yield, VLSI 2024 ([TrendForce](https://trendforce.com/news/?p=10820)).
  - 4F² vertical-gate DRAM, VLSI 2026 T8.5 ([VLSI](https://www.vlsisymposium.org/?p=2390)).
  - Both [REPORTED]. **Closed**.
- **Micron.** 4F² DRAM with a vertical oxide TFT access device appears in granted families ([USPTO 11,653,487](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11653487); assignee not verified) [REPORTED]. **Closed**.
- **imec.** IGZO 2T0C (IEDM 2020/2021) and vertical stacking ([imec, 2023](https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology)) [REPORTED]. IP flows to members of imec's industrial affiliation program (Samsung, SK hynix, Micron, TSMC, Intel, Kioxia and others). Non-members pay for bilateral contracts, typically €1M+/yr [UNVERIFIED-training]. **Closed** to this founder.
- **Others:** TSMC (BEOL oxide-transistor publications) [UNVERIFIED-training]; Huawei (vertical CAA IGZO); IMECAS (4-layer 3D 2T0C, 3 bits/cell, VLSI 2026 ([IT Home](https://www.ithome.com/0/966/543.htm))) [REPORTED]; Sharp (CAAC producer); Intel (FE capacitor on BEOL TFT, [US 11,751,402](https://patents.google.com/patent/US11751402)) [REPORTED].

**U.S. university pool (licensable, unverified status).**
- **Purdue (Peide Ye group).**
  - ALD In₂O₃ transistors: 8nm channel, 0.5nm thick, BEOL-compatible, *Nature Electronics* 2022 ([Purdue, 2022-02-21](https://engineering.purdue.edu/ECE/News/2022/new-material-advances-lead-to-smaller-and-better-performing-transistors)).
  - Three stacked tiers on **200mm** wafers, >100,000 devices ([Purdue, 2026-09-16](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing)) [REPORTED].
- **Georgia Tech (Shimeng Yu).** 3T IWO BEOL eDRAM ([GT, 2024](https://hg.gatech.edu/node/675050)) [REPORTED].
- **UT Austin.** 3T1C IGZO gain cell for compute-in-eDRAM ([ISCAS 2021 PDF](https://sites.utexas.edu/CRL/files/2021/05/IGZO_eDRAM_CIM_ISCAS_2021.pdf)) [REPORTED].

**Assessment**
- Licensability:
  - Corporate: closed.
  - SEL: possible at a price, with no startup track record.
  - University: likely.
- Expiring basics: the a-IGZO TFT base, yes. The memory cell, no.
- Litigation risk: **MED-HIGH**. SEL's estate is dense. Samsung/Micron VCT filings will be asserted against each other first, and against any VCT-like entrant later.
- Best path: a university option on **non-VCT, BEOL gain-cell** IP (Purdue/GT), plus an SEL-focused FTO before any tape-out. Budget $15–30k for FTO [UNVERIFIED-training].

### 3.2 Ferroelectric memory (HfZrO FeRAM/FeFET/FeCAP/FTJ; PZT legacy; AlScN)

**Lineage and base patents**
- **PZT FeRAM.** Ramtron (Colorado Springs, founded 1984).
  - Its 1T1C/2T2C self-restoring architecture (e.g., US 4,873,664, Eaton, 1989) and 1980s–90s materials patents are **expired** [UNVERIFIED-training].
  - Ramtron licensed FRAM to **TI in 2001**. A 2007 deal put Ramtron FRAM on TI's 130nm process ([Digitimes, 2007-03-14](https://digitimes.com/news/a20070314PR204.html)) [REPORTED]. That lineage became TI's MSP430 FRAM MCUs.
  - Cypress acquired Ramtron (2012) and Infineon acquired Cypress (2020), so **Infineon owns the remaining Ramtron/Cypress F-RAM estate** [UNVERIFIED-training].
  - Fujitsu's FeRAM business is now **RAMXEED**, renamed effective 2025-01-01 ([eeNews Europe](https://www.eenewseurope.com/en/fujitsu-memory-spin-off-renames-as-ramxeed/)) [REPORTED].
  - **Take-away:** PZT FeRAM is free to practice at the concept level, but PZT doesn't scale and making it is unattractive (A1).
- **HfO₂ ferroelectric.** Discovered at **Qimonda Dresden in 2007** (Böscke, Müller, Schröder et al.; *Appl. Phys. Lett.* 99, 102903, 2011) [UNVERIFIED-training].
  - The base filings (~2007–08) would expire **~2027–28** [ESTIMATE].
  - Ownership after Qimonda's 2009 insolvency is **unverified**. Qimonda's DRAM patents were largely sold on (e.g., to Polaris Innovations/WiLAN, ~2015), but whether the HfO₂-FE family went with them, or to NaMLab/FMC, is unknown [UNVERIFIED-training].
  - **Action:** search the patent office's assignment records for assignor "Qimonda" and "ferroelectric hafnium".

**Who holds the active estates**
- **FMC (Ferroelectric Memory Company, Dresden).** NaMLab/TU Dresden spin-out (2016).
  - Business model is to be "the ARM of memories", licensing to foundries and IDMs ([eeNews Europe, 2017](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-to-be-the-arm-of-memories/)); first target GF 22FDX ([eeNews Europe, 2016](https://www.eenewseurope.com/en/ferroelectric-memory-startup-aims-at-glofos-22fdx/)).
  - $20M Series B (2020) with SK hynix, Bosch VC and TEL ([VentureBeat](https://venturebeat.com/ai/fmc-raises-20-million-to-mass-produce-ferroelectric-computer-memory)).
  - **€100M (€77M Series C + €23M public) in Nov-2025** for DRAM+ and 3D CACHE+, working with "two major DRAM makers" ([HPCwire, 2025-11-13](https://www.hpcwire.com/off-the-wire/fmc-raises-e100m-to-set-new-standards-for-memory-chips/); [BeBeez](https://bebeez.eu/2025/11/14/fmc-raises-e100m-for-its-hafnium-oxide-based-memory-chips/)).
  - Still no chips on the market, and pursuing a ~€1.3B fab near Magdeburg ([heise, 2026](https://heise.de/-11151026); [CIO.de, 2025-07](https://www.cio.de/article/4026335/kommt-die-erste-chip-fabrik-von-fmc-nach-magdeburg.html)). All [REPORTED].
  - *v2:* the €100M split (€77M Series C + €23M public money, including EIC) is confirmed ([DCD](https://www.datacenterdynamics.com/en/news/fmc-raises-100m-for-its-hafnium-oxide-based-memory-chips/)). **No U.S. office found.**
  - A Taiwanese report has FMC bidding for Intel's cancelled Magdeburg site with a **~€3B** plant and ~50% subsidy sought ([cnyes](https://hao.cnyes.com/post/259683)) [UNVERIFIED]. That conflicts with the €1.3B figure above.
  - CEO **Thomas Rueckes** is Nantero's co-founder (see §3.8). **Licensability for this founder: closed.**
- **Fraunhofer IPMS / NaMLab.**
  - HfO₂ FE stacks are being evaluated for GF 22FDX memory under the EU FAMES pilot line ([Fraunhofer IPMS, 2026](https://www.ipms.fraunhofer.de/en/press-media/press/2026/FAMES-wafer-exchange.html)).
  - **NY CREATES (Albany) + Fraunhofer IPMS JDA** on 300mm HfO₂ FE memory, 2025-05-16 ([idw](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale)) [REPORTED].
  - Contract R&D is possible. IP sits with the JDA parties and is not on a portal.
- **Micron.**
  - 32Gb dual-layer FE 1T1C **NVDRAM**, IEDM 2023 ([eeNews Europe](https://www.eenewseurope.com/en/iedm-micron-to-present-dram-like-non-volatile-memory-for-ai/)).
  - Not productized: "might never become a product" ([Blocks & Files, 2024-01-09](https://blocksandfiles.com/2024/01/09/micron-nvdram-might-never-become-a-product/)); still uncommitted in 2025 ([Design & Reuse](https://www.design-reuse.com/news/202501939-ferroelectric-ram-looking-rusty-and-stuck-/)). [REPORTED]
  - Holds the largest stacked-FE-DRAM estate. **Closed.**
- **Intel.** BEOL FeCAP-on-TFT patents ([US 11,751,402](https://patents.google.com/patent/US11751402)) [REPORTED]. Kepler Computing (ex-Intel founders, FE memory/logic) is Intel-adjacent; its status is unverified [UNVERIFIED-training]. **Closed.**
- **SunRise Memory (San Jose, Eli Harari).** 3D NOR as a DRAM alternative; still granted patents in 2024–26 ([CB Insights](https://www.cbinsights.com/company/sunrise-memory); [US 12,052,867](https://patents.google.com/patent/US12052867)) [REPORTED]. No licensing program seen.
- **Samsung and SK hynix** both file heavily on FeFET V-NAND and FE capacitors [UNVERIFIED-training]. **Closed.**
- **Sandia National Laboratories.**
  - HfO₂/HZO rad-hard FeRAM integrated into the **trusted MESA CMOS fab at 200mm**, plus binary and 32-state FTJs (LDRD, 2026-05-13) ([Sandia](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/)) [REPORTED].
  - **This is the strongest licensable U.S. ferroelectric lead in the repo.** Path: Sandia license plus CRADA, aimed at rad-hard NVM for DoD/space.
  - **v2 caveat (2026-11-01):** searches found no Sandia IP-portal listing and no CRADA offer for HZO FeRAM/FTJ. The 2026-05-13 article describes internal LDRD work with follow-on circuit projects. The only Sandia FE memory patents found are old ones, e.g. US 5,578,846, now expired ([Google Patents](https://patents.google.com/patent/US5578846)). **Treat it as an unconfirmed lead** until Sandia Licensing & Technology Transfer confirms that filings exist and are available [UNVERIFIED].
- **Penn (Deep Jariwala, Roy Olsson) + AFRL.** **AlScN ferroelectric diode** NVM operating at **600 °C** for >60 h (*Nature Electronics*, 2024-04-29) ([Penn Engineering](https://www.engineering.upenn.edu/stories/turning-up-the-heat-on-data-storage/)) [REPORTED].
  - Demand signal 1: a USAF SBIR topic (AF254-D0806) cites ferro-diode memory to 600 °C ([SBIR.gov](https://www.sbir.gov/topics/12036)).
  - Demand signal 2: DARPA SBIR DPA26BZ04-DV017, Direct-to-Phase II, ~$1.2M, −269 °C to +600 °C NVM, opened 2026-07-22 ([DARPA](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments); [BW Consulting](https://www.bwcoconsulting.com/fod/dpa26bz04-dv017)) [REPORTED].
  - Penn's licensing status is **unverified**. AFRL co-invention means the government holds rights.
  - *v2:* no Penn Center for Innovation listing or spin-out found. The earlier AlScN FE-FET/ferro-diode work (Jariwala, Olsson, Stach) was **DARPA TUFEN-funded** ([Penn Engineering](https://www.engineering.upenn.edu/stories/penn-engineers-pave-way-for-chip-components-that-could-serve-as-both-ram-and-rom/)) [REPORTED-P], so government-use rights apply on top of the AFRL co-invention.
- **Other U.S. academic FE groups** [UNVERIFIED-training]:
  - **Notre Dame:** Kai Ni (FeFET).
  - **Georgia Tech:** Asif Khan (HZO, FE NAND), Shimeng Yu (FeFET CIM), Suman Datta.
  - **Purdue:** Peide Ye (α-In₂Se₃ ferroelectric-semiconductor FET; In₂O₃ FeFET tiers in the 2026 M3D demo).
  - **Penn State:** Jon-Paul Maria and Susan Trolier-McKinstry (wurtzite AlBN ferroelectrics).
  - **Berkeley:** Sayeef Salahuddin (HZO, negative capacitance).

**Assessment**
- Licensability: corporate closed; **Sandia and Penn likely**.
- Expiring basics: PZT, yes. HfO₂ base, ~2027–28.
- Litigation: **LOW-MED** today. I recall no major FE patent suits, but Micron/Intel/Samsung estates will matter at production.
- Best path: **Sandia HZO license + CRADA + STTR** (rad-hard NVM), or **Penn AlScN + STTR** (extreme-temperature NVM). Both are niche, defense-funded and glut-proof, and neither is a DRAM substitute.

### 3.3 MRAM (Toggle, STT, SOT, VCMA)

**Base patents (expired)** [UNVERIFIED-training]
- **STT switching:** J. Slonczewski / IBM, US 5,695,864 (filed 1995), expired ~2015. Berger's parallel work is also old.
- **Toggle MRAM:** Savtchenko et al. / Motorola, US 6,545,906 (filed ~2001), expired ~2021. Toggle is Everspin's rad-hard product line.
- **MgO tunnel barrier** (Parkin/IBM; Yuasa/AIST, ~2001–04): expired or expiring ~2021–25.
- **Perpendicular CoFeB/MgO pMTJ** (Ikeda/Ohno, Tohoku, *Nature Materials* 2010): filings ~2009–10, live to ~2029–30. Tohoku's CIES consortium licenses to members.
- **NVE Corp** (Eden Prairie MN) holds early GMR/MRAM patents licensed to Motorola and Cypress in the 1990s–2000s. These are now mostly expired. NVE is a sensor/coupler company today: FY26 revenue $26.3M, not memory ([NVE, 2026-05-06](https://www.nve.com/earningsreports/may62026)) [REPORTED].

**Live estates and licensing behaviour**
- **Everspin (Chandler AZ; Freescale spin-out 2008).**
  - Holds the Motorola/Freescale estate plus its own STT filings.
  - Licensing/royalty/services: **$6.9M in FY2025** ([BusinessWire](https://www.businesswire.com/news/home/20260304733194/en/Everspin-Reports-Unaudited-Fourth-Quarter-and-Full-Year-2025-Financial-Results)); **$3.7M in Q3-2026** ([8-K](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm)) [REPORTED].
  - *v2 financials:*
    - **FY25:** revenue $55.2M (product $48.3M), GM 51.2%, GAAP net loss $0.6M, 238 design wins.
    - **Q3-26:** revenue $20.6M, GM 51.4%, GAAP net loss $7.2M after $6.0M litigation and a $2.7M regulatory provision ([10-K/ARS FY25](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024092/mram_20251231xarsx10k.pdf); [Q3-26 8-K](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm); via snippet) [REPORTED-P].
    - **No DRAM-replacement design win found.** Data-centre CXL MRAM is still in development with no revenue projected (2026-08) ([MarketBeat](https://www.marketbeat.com/instant-alerts/everspin-tech-q2-earnings-call-highlights-2026-08-05/)) [REPORTED].
  - Deal precedents:
    - GF 300mm STT partnership (2014) ([Design & Reuse](https://us.design-reuse.com/news/35789/everspin-globalfoundries-300mm-cmos-wafer-st-mram.html)).
    - $5.26M tranche of a DoD rad-hard FPGA program with QuickLogic, using Chandler 8-inch Toggle (2024-07-24) ([BusinessWire](https://www.businesswire.com/news/home/20240724863768/en/Everspin-Announces-Contract-to-Provide-MRAM-Technology-for-Strategic-Radiation-Hardened-FPGA)).
    - **$40M / 2.5-year subcontract to transfer Toggle MRAM process tech to a U.S. prime, named as Amentum (Apr-2026)** ([Electronics360](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services); [MRAM-Info](https://www.mram-info.com/everspin-enters-40-million-subcontract-agreement-amentum-establish-us-mram-processes-and)).
    - 10-year Microchip foundry deal (Gresham OR, 8-inch); Microchip is barred from making TMR devices for others ([8-K, 2026-04-08](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm)).
    - All [REPORTED].
  - **Reading:** Everspin licenses process know-how in exchange for engineering fees, at defense-prime scale. A small company is more likely a **customer or channel partner** than a licensee.
- **Avalanche Technology (Fremont CA).**
  - pMTJ STT-MRAM; 512Mb parts on **UMC 22nm** ([TechInsights](https://www.techinsights.com/blog/avalanche-as301g208-umc-22-nm-512mb-mram-process-analysis)).
  - A U.S.-government MTJ-scaling program toward 22nm space MRAM ([Avalanche, 2026-03](https://www.avalanche-technology.com/avalanche-technology-phase-one-magnetic-cell-scaling-space-grade-mram-us-government/)).
  - **Complainant in ITC 337-TA-1487 against Everspin** ([Avalanche](https://www.avalanche-technology.com/itc-institutes-investigation-into-everspin-technology-based-on-avalanche-claims-of-patent-infringement/)) [REPORTED].
  - Licensing to foundries (UMC partnership, ~2018) [UNVERIFIED-training]. **Not a startup licensor; an active asserter.**
- **IBM.** STT and MgO origins, plus a 14nm eMRAM cell. IBM runs a large general IP-licensing business, so licensable in principle at IBM rates [UNVERIFIED-training].
- **Foundry eMRAM is captive**:
  - Samsung: 14nm, then 8nm, then 5nm ([MRAM-Info](https://mram-info.com/samsung-track-start-14-nm-emram-production-end-2024-8-nm-2026-and-5-nm-2027)).
  - TSMC: 22/16nm.
  - GF: AutoPro150 eMRAM, volume 2H-2026 at **Dresden, not the U.S.** ([GlobeNewswire, 2026-03-09](https://www.globenewswire.com/news-release/2026/03/09/3251832/0/en/GlobalFoundries-Announces-Availability-of-AutoPro150-eMRAM-Technology-on-Enhanced-FDX-Platform-for-Advanced-Automotive-Applications.html)) [REPORTED].
- **Defunct or orphaned:**
  - **Spin Memory** (ex-Spin Transfer Technologies; Allied Minds; Applied Materials and Arm invested 2018) ceased ~2021. **The disposition of its patents is unverified** [UNVERIFIED-training].
  - **Antaios** (Grenoble, SOT): taped out a test chip in 2021 ([eeNews Europe](https://www.eenewseurope.com/en/mram-startup-makes-progress-as-rival-closes/)); listed "closed" ([Dealroom](https://app.dealroom.co/companies/antaios)) [UNVERIFIED].
  - **eVaderis** (STT-MRAM IP) closed in 2017 ([eeNews Europe](https://www.eenewseurope.com/en/mram-startup-evaderis-closes-here-comes-antaios)) [REPORTED].
  - **Pattern:** independent MRAM-IP startups do not survive. Their estates may be buyable.
- **Universities** [UNVERIFIED-training]:
  - **UMN:** Jian-Ping Wang (SOT with topological/novel materials; C-SPIN center legacy). UMN's "MN-IP Try-and-Buy" startup program historically offered pre-set low-cost terms.
  - **Cornell:** Dan Ralph and Robert Buhrman (spin-Hall SOT; Liu et al., *Science* 2012).
  - **UCLA:** Kang Wang (VCMA "MeRAM"; spin-out Inston Inc., status unknown).
  - **Northwestern:** Pedram Khalili (SOT/VCMA).
  - **MIT:** Luqiao Liu, Geoffrey Beach.

**Litigation.** **HIGH.**
- **ITC 337-TA-1487 (Avalanche v. Everspin)** was instituted 2026-02-27. The ALJ denied Everspin's early-termination bid in June 2026, and a result is expected ~Jul-2027 ([USITC](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm); [Bloomberg Gov](https://news.bgov.com/ip-law/avalanche-beats-early-bid-to-end-itc-patent-case-over-fee-errors); [notice, 2026-08-26](https://www.usitc.gov/sites/default/files/secretary/fed_reg_notices/337/337_1487_notice08262026sgl.pdf)) [REPORTED].
  - *v2 detail:*
    - **Filings:** complaint 2026-01-28, amended 2026-02-05. Avalanche Technology (Fremont CA) v. Everspin, the sole respondent.
    - **Asserted patents:** US 9,318,179, 9,419,210, 11,678,586 and 10,490,737. Parallel D. Del. suit on the same four ([USITC notice](https://www.usitc.gov/secretary/fed_reg_notices/337/337_1487_notice02272026sgl.pdf); [Avalanche](https://www.avalanche-technology.com/itc-institutes-investigation-into-everspin-technology-based-on-avalanche-claims-of-patent-infringement/)) [REPORTED-P].
    - **Status:** no final determination, exclusion order or settlement found as of 2026-11-01. Everspin has booked no loss accrual. The ~Jul-2027 target comes from secondary sources only.
- An exclusion order would hit **imported** Everspin STT-MRAM. Those parts are built on GF Singapore CMOS wafers ([Everspin 10-K](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm)) [REPORTED].
- **Supply-risk note for any concept that designs in Everspin 1Gb STT parts:** plan a second source (Avalanche or Netsol) or use Toggle.

**Assessment.**
- Licensability: commercial (Everspin) at prime scale; universities likely.
- Basics: largely expired.
- Litigation: HIGH.
- Best path: **buy and design in, don't license**. University SOT/VCMA only as a T2 moonshot.

### 3.4 ReRAM / memristor / CBRAM

- **Weebit Nano (ASX: WBT; tech co-developed with and licensed from CEA-Leti)** [UNVERIFIED-training on the CEA license structure].
  - Licensees and qualifications:
    - **SkyWater S130**: JEDEC-qualified 2023-06, 10-year retention; qualified to 125 °C and in the PDK 2023-11 ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/); [SkyWater](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/)).
    - **onsemi** Treo 65nm BCD (2025-01) ([Design & Reuse](https://us.design-reuse.com/news/57216/weebit-nano-reram-onsemi.html)).
    - **DB HiTek** 130nm BCD (2026-01) ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nano-signs-largest-customer-to-date-technology-qualified-at-db-hitek/)).
    - **Texas Instruments** (2025-12-29; tech transfer plus qualification) ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nano-secures-a-license-agreement-with-texas-instruments/)).
  - Three customer tape-outs; FY26 revenue guidance ≥A$13.5M; cash A$167M (2026-07) ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nano-expands-licensing-agreements-with-key-customers-three-customer-chip-designs-taped-out-to-date/)). H1 FY26 revenue A$5.6M ([itbrief](https://itbrief.com.au/story/weebit-nano-posts-record-h1-revenue-on-reram-deals)). All [REPORTED].
  - **For a fabless U.S. startup, this is the only qualified, U.S.-fab, PDK-resident memory IP found in this engagement.** Per-customer license and royalty terms are **unknown**. Ask SkyWater and Weebit directly (see §9).
  - **v2 verification (2026-11-01):**
    - **FY26 actual:** revenue was A$15.28M (FY25 A$4.41M), from licence and NRE fees (TI, onsemi). First royalties are expected in CY2027, and 1H FY27 guidance is ≥A$7.1M ([Kalkine, 2026-08-28](https://kalkinemedia.com/au/news/announcements/weebit-nano-reports-153-million-revenue-for-fiscal-year-2026); [Motley Fool AU, 2026-08-28](https://www.fool.com.au/2026/08/28/weebit-nano-fy26-record-revenue-new-customer-wins/)) [REPORTED].
    - **Model:** a manufacturing licence fee, NRE, and royalties based on production volume.
      - Weebit's first-ever licence fee was $100k ([RRAM-Info](https://rram-info.com/weebit-nano-announces-first-ip-licensing-revenue-its-embedded-rram-technology)).
      - Analyst estimates put DB HiTek's upfront fee at ~$0.29M and onsemi's at ~$1.8–2.6M ([MST, 2025-09-01](https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf)) [REPORTED].
      - No royalty rate is disclosed.
    - **Tape-outs:** the three customer tape-outs **do not name a foundry**, and none is shown to be on SkyWater S130.
    - **Access:** the S130 prototype route was Efabless chipIgnite ("small fee"; production licence direct from Weebit) ([StorageNewsletter, 2024-06-05](https://www.storagenewsletter.com/2024/06/05/weebit-nano-and-efabless-collaborate-to-enable-prototyping-of-soc-designs/)). It died with Efabless in early 2025.
    - **Ownership:** SkyWater is an IonQ subsidiary since 2026-07-31 ([Quantum Insider](https://thequantuminsider.com/2026/07/31/ionq-completes-skywater-acquisition-quantum-manufacturing/)) [REPORTED].
- **Crossbar (Santa Clara).** Founded 2010 on Univ. of Michigan RRAM (Wei Lu) [UNVERIFIED-training]. Still granting patents (Feb-2026); last raise ~$5M around 2024; no product evidence (A2) [REPORTED via A2]. Historic licensees: SMIC 40nm (~2016) and Microsemi (2018) [UNVERIFIED-training]. **Likely** licensable.
- **TetraMem (Fremont).** Multi-level RRAM for analog in-memory compute. MLX200 on TSMC 22nm validated (2026-05-16), and the company says its **RRAM IP is available for licensing** ([BusinessWire](https://www.businesswire.com/news/home/20260516556464/en/TetraMem-Announces-22nm-Multi-Level-RRAM-Analog-In-Memory-Computing-SoC-Milestone)). MLX300 at 12nm taped out 2026-10-27 ([STT Info](https://www.sttinfo.fi/tiedote/72447857/tetramem-advances-analog-in-memory-computing-with-tapeout-of-new-12nm-ai-soc?publisherId=58763726)) [REPORTED]. Academic lineage: UMass Amherst (Qiangfei Xia) and USC (J. Joshua Yang, ex-HP Labs) [UNVERIFIED-training].
- **HPE (HP Labs) memristor.**
  - Large 2008–2016 filing program (Strukov et al., *Nature* 2008) [UNVERIFIED-training].
  - Dropped from The Machine in 2015 as not economically viable for volume ([MIT Technology Review](https://www.technologyreview.com/2015/06/04/167804/hp-puts-the-future-of-computing-on-hold/)); the SK hynix JV was starved and the product shelved in Nov-2016 ([The Register](https://www.theregister.com/2016/11/29/hp_labs_delivered_machine_proof_of_concept_prototype_but_machine_product_is_no_more/)) [REPORTED].
  - Estate status: **unknown**; earliest filings expire from ~2028.
- **4DS Memory (Perth; PCMO "interface switching" ReRAM, imec partner).** Suspended from ASX quotation 2026-04-29; market cap ~$16M; still announcing AI-oriented ReRAM in May-2026 ([filings](https://financialfilings.com/companies/4ds-memory-limited/); [4DS announcement](https://bulletin.webull.com/qbd/announcement/20260512/499501739/96c453452930114048cbe32bc0163383.pdf)) [REPORTED]. **A distressed-estate candidate.**
- **CBRAM.**
  - Lineage: Michael Kozicki (ASU) programmable-metallization cell, **US 5,761,115** (filed 1996, expired ~2016) [UNVERIFIED-training].
  - Licensed through Axon Technologies to Adesto (and historically Infineon/Qimonda and Micron) [UNVERIFIED-training].
  - Adesto went to Dialog (2020), then Renesas (2021), and **GF acquired the CBRAM technology from Renesas on 2023-02-09** to qualify on 22FDX ([GF](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/)) [REPORTED]. **Closed.**
- **Foundry embedded RRAM (captive):** TSMC 22RRAM and N12e ([TSMC AR 2025](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf)); Infineon AURIX TC4x on TSMC 28nm RRAM ([eeNews Europe](https://www.eenewseurope.com/en/infineon-and-tsmc-to-introduce-rram-for-automotive-mcus)) [REPORTED]. Panasonic's ReRAM went to Nuvoton (2020) [UNVERIFIED-training].
- **Universities** [UNVERIFIED-training]: UMich (Wei Lu), UMass (Xia), USC (Yang), Stanford (H.-S. Philip Wong), UCSB (Dmitri Strukov), ASU (Kozicki; Hugh Barnaby on rad effects).

**Assessment.**
- Licensability: **Weebit and TetraMem open**, Crossbar likely, GF closed.
- Basics: PMC expired.
- Litigation: **LOW-MED**; no major ReRAM suits seen.
- Best path: **Weebit ReRAM on SkyWater S130** for a U.S.-made secure/eNVM part (A2-07 lineage).

### 3.5 PCM and 3D XPoint

- **What happened to XPoint IP.**
  - Micron exited 3D XPoint in **Mar-2021**, citing "insufficient market validation" ([Micron via Nasdaq, 2021-03-16](https://www.nasdaq.com/press-release/micron-updates-data-center-portfolio-strategy-to-address-growing-opportunity-for)), and sold the Lehi fab to **TI for $900M** (2021-06-30) ([AnandTech](https://www.anandtech.com/show/16800)).
  - Intel began the Optane wind-down in Q2-2022 with a **$559M inventory impairment** ([Intel 10-Q](https://www.sec.gov/Archives/edgar/data/50863/000005086322000030/intc-20220702.htm)). Cumulative Optane losses were reported at >$7B ([SNIA/Coughlin-Handy](https://www.snia.org/sites/default/files/2025-05/SNIA-SDC22-Coughlin-Handy-Persistent-Memories-Without-Optane-Where-Would-We-Be.pdf)) [REPORTED].
  - **The patents did not go anywhere public.** Intel and Micron each retain their XPoint/OTS-selector families. No licensing program has been announced [UNVERIFIED-training].
  - Filings from 2005–2015 run to ~2025–2035. A sale to an NPE is the latent risk for any future cross-point product.
- **Live PCM holders.**
  - **ST + Samsung Foundry:** 18nm FD-SOI ePCM; STM32V8 announced 2025-11-18 ([ST](https://newsroom.st.com/?p=17292)). Captive.
  - **SanDisk:** "3D Matrix Memory" prototypes on 300mm, aiming at ~half DRAM cost/bit, with imec "Project Neo" since 2024 and a $35M AFRL award in 2023 ([Notebookcheck](https://www.notebookcheck.net/SanDisk-makes-first-3D-Matrix-Memory-chips-aiming-for-half-the-cost-per-bit-of-DRAM.1374351.0.html); [eeNews Europe](https://www.eenewseurope.com/en/does-phase-change-memory-ride-again-with-sandisk)).
  - **SK hynix:** chalcogenide selector-only memory (SOM) ([eeNews Europe](https://www.eenewseurope.com/en/selector-only-memory-gains-advocates-including-sk-hynix/)).
  - **IBM:** analog-AI PCM [UNVERIFIED-training].
  - All [REPORTED] unless tagged.
- **Base patents.** Ovshinsky/ECD/Ovonyx (1960s–1990s) are expired. Post-2012 ownership of the Ovonyx estate (after ECD's bankruptcy) is unverified [UNVERIFIED-training].

**Assessment.**
- Licensability: **closed**. Basics: expired. Litigation: LOW now, latent later.
- Startup path: **none for making PCM**.
- The A2-11 Optane resale idea needs no license, because exhaustion covers authorized parts.

### 3.6 Capacitor-less silicon DRAM (Z-RAM, T-RAM/TCCT, FBC, Kilopass VLT)

All [UNVERIFIED-training]; consistent with A3's post-mortems.
- **Z-RAM (Innovative Silicon, EPFL spin-out ~2002).**
  - Licensed to AMD (2006) and Hynix (2007). Closed in 2010.
  - The estate **reportedly went to Micron**.
  - Early filings (2002–06) expire 2022–26.
- **T-RAM (thin capacitively-coupled thyristor).**
  - Stanford base: Nemati & Plummer, US 6,229,161 (filed ~1998), expired ~2018.
  - T-RAM Semiconductor licensed to AMD (2006) and co-developed with GF (2009); defunct ~2010–11.
  - Estate disposition unverified.
- **Kilopass VLT.** Vertical-thyristor DRAM; Kilopass was acquired by **Synopsys (2018)**, and VLT disappeared.
- **Toshiba FBC.** Old filings, expired.
- **Unisantis Electronics (Fujio Masuoka; SGT surrounding-gate transistors; "Dynamic Flash Memory" 2021).**
  - A **licensing company with a large vertical-GAA-transistor estate**.
  - Low relevance to planar capacitor-less cells, but **MED risk for any vertical-channel (VCT) DRAM**.

**Assessment.**
- Licensability: **effectively open** (expired early art).
- What killed these technologies was physics and integration, not IP: sense margin, temperature retention and holding current. **Nothing here is worth licensing.**

### 3.7 3D DRAM (VCT/4F², vertically stacked DRAM, 3D X-DRAM, 3D 2T0C)

- **NEO Semiconductor (San Jose; CEO Andy Hsu).**
  - 3D X-DRAM: a 1T0C floating-body cell (2023). 1T1C and 3T0C IGZO variants were announced in May-2025, with TCAD-only claims at the time ([Evertiq](https://evertiq.com/news/2025-05-09-neo-unveils-1t1c-and-3t0c-igzo-based-3d-x-dram-tech); [eeNews Europe](https://www.eenewseurope.com/en/neo-semiconductor-adds-igzo-to-3d-dram-designs/)). NEO says the cell uses a modified 3D-NAND process ([Blocks & Files](https://blocksandfiles.com/?p=73750)).
  - **PoC on 2026-04-23:** retention >1 s at 85 °C, endurance >1e14, <10 ns R/W. Test chips were made with NYCU and fabbed at TSRI, and Stan Shih led a strategic investment ([StorageNewsletter](https://www.storagenewsletter.com/2026/05/13/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/)) [REPORTED].
  - **Business model:** license to memory makers (A1). The number of granted U.S. patents is unverified (NEO's site was DNS-blocked). *v2:* the licensing/co-development model is confirmed, with "active discussions" with memory companies. **No licensee has been named** as of the latest news found, 2026-04/05 ([Yole/PR, 2026-04-23](https://www.yolegroup.com/industry-news/neo-semiconductor-demonstrates-3d-x-dram-proof-of-concept-secures-strategic-investment-to-advance-ai-memory/)) [REPORTED].
  - **For this founder:** closed. Partnering means being a 3D-NAND-class fab.
- **Incumbents:**
  - Samsung: 4F² VCT IGZO, targeting 2028 ([TrendForce](https://www.trendforce.com/news/2026/04/24/news-samsung-reportedly-produces-sub-10nm-10a-dram-working-die-using-4f-square-and-vct-targets-2028-production/)).
  - SK hynix: 5-layer 3D and 4F² VG ([TrendForce](https://trendforce.com/news/?p=10820); [VLSI 2026](https://www.vlsisymposium.org/?p=2390)).
  - Micron: [USPTO 11,653,487](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11653487), assignee unverified.
  - Kioxia/Nanya: OCTRAM.
  - IMECAS: 3D 2T0C.
  - CXMT.
  - Analyst landscape reports have put **Micron and Samsung as the leading 3D-DRAM filers**; numbers unverified [UNVERIFIED-training].
- **Litigation:** none yet. Expect cross-assertion among the big four (plus CXMT) once VCT ships around 2028–30. Unisantis is a wildcard.

**Assessment.** Closed. No expiring basics that matter. **Not a startup play** (consistent with A1-05 "dead for us").

### 3.8 NRAM (carbon-nanotube resistive memory)

- **Nantero (Woburn, MA; founded 2001)** [UNVERIFIED-training].
  - Spin-coated CNT fabric with van-der-Waals switching.
  - Licensed to **Fujitsu Semiconductor / Mie Fujitsu (2016)** for 55nm; it is not known to have shipped. The Mie fab became UMC's USJC.
  - The company claimed a large estate (hundreds of patents). Early filings (2001–04) expired ~2021–24.
- **Status in 2025–26: UNKNOWN.** There is no evidence of an acquisition in any agent's logs.
  - *v2:* a search found no 2025–26 news.
  - A third-party directory tags Nantero **"Defunct"** (2026-09) ([apis.io](https://apis.io/providers/nantero/)) [UNVERIFIED].
  - History confirmed: government unit sold to Lockheed Martin (2008); Fujitsu 55nm licence ([Electronic Design](https://www.electronicdesign.com/technologies/embedded/article/21806368/startup-planting-the-seeds-of-nonvolatile-random-access-memory)) [REPORTED].
  - Thomas Rueckes, a Nantero co-founder, now leads FMC ([HPCwire, 2025-11-13](https://www.hpcwire.com/off-the-wire/fmc-raises-e100m-to-set-new-standards-for-memory-chips/)) [REPORTED]. That is weak evidence the original technical leadership has moved on.

**Assessment.**
- Licensability: unknown; possibly distressed.
- 20+ years without volume and a transistor-limited 1T1R cost (~$31/GB hypothetical, A3) make it a **kill** as a venture base.
- Worth one assignment-records check (§9) in case the estate is for sale cheaply as **defensive or rad-hard IP**.

### 3.9 2D, CNT-FET, organic and printed memory

- **Universities hold essentially all the IP** [UNVERIFIED-training]:
  - Northwestern (Mark Hersam: MoS₂ memtransistor, *Nature* 2018).
  - UT Austin (Deji Akinwande: "atomristor").
  - Penn State (Saptarshi Das: 2D in-memory devices).
  - Stanford (Eric Pop; Subhasish Mitra: N3XT CNT+RRAM).
  - MIT (Max Shulaker: CNFET + RRAM monolithic 3D under DARPA 3DSoC with SkyWater).
- **Thinfilm** (printed ferroelectric-polymer memory) pivoted and reportedly became insolvent (A3).
- **Assessment:** licensable and cheap, but TRL 2–4. **Kill** for a revenue-bound founder. Keep MIT/SkyWater CNFET+RRAM in mind only as a DARPA-funded U.S. monolithic-3D precedent.

### 3.10 SRAM and open-source memory IP

- **OpenRAM** (BSD-3) compiles SRAM for sky130, gf180mcu and freepdk45. Version 1.2.50 was released 2026-10-27 ([GitHub, opened by A3](https://github.com/VLSIDA/OpenRAM)) [REPORTED, primary opened by A3]. *v2 conflict:* snippets show the repo's last push as 2026-04-17 and PyPI 1.2.48 ([gittrend](https://gittrend.io/repo/VLSIDA/OpenRAM); [PyPI](https://pypi.org/project/openram/)). BSD-3 and active in 2026 either way; the exact version is [UNVERIFIED].
- **sky130 open PDK** is Apache-2.0 [UNVERIFIED-training]. A ChipFoundry/Caravel MPW channel is active as of 2026-04 ([GitHub](https://github.com/chipfoundry/caravel_user_project)) [REPORTED].
  - *v2:* ChipFoundry, founded by Efabless's founders after Efabless closed in early 2025, charges ~$15k per 100 sky130 chips ([eeNews Europe](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)) [REPORTED].
  - **GF180MCU via wafer.space** costs $7,000–7,500 per 1,000-die slot ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2)) [REPORTED-P]. OpenRAM also supports gf180mcu.
- **The only fully open memory IP stack found.** No license cost and no royalty. It is the natural base for A3-04 / A3-07.

### 3.11 Adjacent hazard: DRAM module and interface patents (relevant to §3B/§3C)

- **Netlist (Irvine CA)** [UNVERIFIED-training; figures match p1-backend's [UNVERIFIED: PK]]:
  - **E.D. Tex. verdicts:**
    - **$303.15M vs Samsung** (2023-04-21). Patents included the '918/'054 PMIC family and '339.
    - **$445M vs Micron** (2024-05-23; '918 = US 11,016,918 and '054 = US 11,232,054, on-DIMM power management).
    - **$118M vs Samsung** (2024-11; '912 = US 7,619,912 family and others).
  - **PTAB:** Samsung and Micron IPRs found several asserted claims unpatentable (2023–24). Federal Circuit appeals were pending into 2025. **Outcome as of 2026-11: UNKNOWN.**
  - **C.D. Cal.:** juries (2021, 2024) found Samsung breached the 2015 JDLA, ending Samsung's license.
  - **Other fronts:** Micron sued Netlist under Idaho's bad-faith-assertion statute (2023). I also have a weak recollection of a 2025 Netlist ITC complaint against Samsung (DDR5/HBM); **verify**.
  - SK hynix holds a 2021 license (per p1-backend).
  - **Exposure:** anyone *making* DDR5 RDIMM/MRDIMM or HBM-stack modules in the U.S. **Mitigation:** buy finished modules from licensed makers, or get an FTO opinion before shipping.
- **Rambus.** A litigation-era licensor (Samsung $900M settlement in 2010; Micron settlement 2013) that now licenses interface IP commercially [UNVERIFIED-training]. Relevant only to custom controller/PHY chips.
- **Polaris Innovations (WiLAN/Quarterhill; ex-Qimonda DRAM estate).** Asserted against module makers such as Kingston (~2016) [UNVERIFIED-training]. Much of that estate is now expired or near expiry.
- **Other memory NPE patterns** [UNVERIFIED-training]: Longitude Licensing (Elpida estate), Mosaid/Conversant, Daedalus Prime (Intel estate), Monterey Research (Cypress/Spansion estate), Bell Semiconductor (LSI/Avago estate). YMTC v. Micron (N.D. Cal., 2023, NAND) shows Chinese makers asserting in the U.S.

---

## 4. Litigation register (memory-relevant, 2023–2026)

| Case / forum | Parties | Key dates | Status (as known) | Bears on | Tag |
|---|---|---|---|---|---|
| ITC 337-TA-1487 | Avalanche v. Everspin (STT-MRAM imports) | Instituted 2026-02-27; early-termination denied 2026-06; notice 2026-08-26; target ~2027-07 | **Active** | Any design-in of imported Everspin STT parts; MRAM concepts | [REPORTED] ([USITC](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm), [BGov](https://news.bgov.com/ip-law/avalanche-beats-early-bid-to-end-itc-patent-case-over-fee-errors)) |
| Everspin Q3-26 cost line | Everspin | Q3-2026 | $6.0M litigation in $18.5M opex | Signals cost of an ITC defense for a small public memory firm | [REPORTED] ([8-K](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm)) |
| E.D. Tex. 2:21-cv-463 | Netlist v. Samsung | Verdict 2023-04-21, $303M | Post-trial/appeal; PTAB invalidations of several claims | DDR4/DDR5 RDIMM/LRDIMM | [UNVERIFIED-training] |
| E.D. Tex. (2022 case) | Netlist v. Micron | Verdict 2024-05-23, $445M (PMIC '918/'054) | Appeal/PTAB interplay; outcome unknown | **DDR5 RDIMM PMIC**; U.S. module assembly concepts | [UNVERIFIED-training] |
| E.D. Tex. (2022 case) | Netlist v. Samsung II | Verdict 2024-11, $118M | Unknown | As above | [UNVERIFIED-training] |
| C.D. Cal. | Netlist v. Samsung (contract) | Juries 2021, 2024 for Netlist | License terminated | Samsung's defenses | [UNVERIFIED-training] |
| Idaho / D. Idaho | Micron v. Netlist (bad-faith assertion statute) | 2023 | Unknown | Shows defendants' counter-tools | [UNVERIFIED-training] |
| N.D. Cal. | YMTC v. Micron (3D NAND) | Filed 2023-11 | Unknown | Signals Chinese makers asserting in the U.S. | [UNVERIFIED-training] |

**What a small company should budget.**
- Defending one NPE suit runs **~$0.6M–$4M through trial**, depending on the amount at stake. Typical early settlements for small defendants are **$50k–$500k**. An ITC 337 defense is costlier and faster [UNVERIFIED-training; AIPLA survey bands recalled].
- **Cheap defenses:**
  - Join the **LOT Network**; historically free below ~$25M revenue [UNVERIFIED-training].
  - Buy only licensed parts (exhaustion).
  - Get a scoped FTO before first ship ($10k–$30k).
  - Keep revenue small and invisible until FTO is done. NPEs target revenue.

---

## 5. Benchmarks: what commercial memory-IP licensing earns

| Licensor | What it licenses | Years active | Revenue signal | Lesson | Tag |
|---|---|---|---|---|---|
| Weebit Nano | ReRAM (CEA-Leti) to fabs/IDMs | ~10 | FY26 actual A$15.28M (guide ≥A$13.5M; v2); H1 FY26 A$5.6M; cash A$167M; royalties from CY2027 | Best-run independent; still sub-scale after a decade | [REPORTED] |
| Everspin (licensing line) | MRAM process/tech + services | Since 2008 | $6.9M FY25; $3.7M Q3-26 | Licensing is a side line to product sales; the big deal is defense-prime services | [REPORTED] |
| FMC | HfO₂ FeFET/DRAM+ | ~9 | No product; €100M raise 2025-11; fab ambitions | Licensing alone did not reach product; now wants a fab | [REPORTED] |
| NEO Semiconductor | 3D X-NAND/X-DRAM | ~5 | Not disclosed; PoC only (2026-04) | Licensing pre-silicon architecture is a long sell to IDMs | [REPORTED] |
| TetraMem | Multi-level RRAM + A-IMC SoC | ~8 | Not disclosed; chips sampling 2H-2026 | Licensing plus own chips | [REPORTED] |
| MoSys (1T-SRAM) | eDRAM-as-SRAM IP | 1991–2021 | Modest, declining royalties; merged into Peraso | Trailing-node embedded-memory royalties support a small firm at best | [UNVERIFIED-training via A3] |
| Kilopass | OTP and VLT DRAM | ~2001–2018 | Acquired by Synopsys | Exit to an EDA/IP major is the realistic outcome | [UNVERIFIED-training] |
| Rambus | Memory interfaces | 1990– | Hundreds of $M/yr after decades of litigation | The success case required litigation stamina | [UNVERIFIED-training] |

**Conclusion:** licensing memory IP *to* fabs is a 5–10-year, VC-scale path (T2–T3). It fails the founder's 18/36-month revenue test. Use licensing **inbound**: take a license and sell a product or service.

---

## 6. University and national-lab tech transfer

### 6.1 What could and could not be done

The task asked for concrete available technologies with URL, inventor, patent number and status from each portal. **This could not be done.** Every portal fetch was DNS-blocked and the search budget was gone.

Below, each institution gets:
- the memory-relevant inventors and technologies I can document (cross-ref sources) or recall (training);
- a fit judgment.

Exact portal queries are in §9. **Every "status" is UNVERIFIED** until the portal is checked.

### 6.2 Target list: universities

| Institution (office) | Technology | Inventor(s) | Evidence | Patent # | Status | Fit for this venture |
|---|---|---|---|---|---|---|
| **Purdue** (Purdue Research Foundation OTC) | ALD **In₂O₃ BEOL transistors**; 3-tier monolithic 3D on 200mm incl. FeFET tiers | Peide Ye (+ Li) | [Purdue, 2026-09-16](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing); [Purdue, 2022-02-21](https://engineering.purdue.edu/ECE/News/2022/new-material-advances-lead-to-smaller-and-better-performing-transistors) [REPORTED] | Not retrieved | Unverified | **High** for oxide gain-cell IP (A1-01). 200mm process is closest to a U.S. foundry |
| **Purdue** | α-In₂Se₃ ferroelectric-semiconductor FET | Peide Ye | [UNVERIFIED-training] | Not retrieved | Unverified | Low-med (TRL 3) |
| **Purdue** (v2: portal listing found) | **Tech No. 65866 "FETRAM: A Novel Organic Ferroelectric Based Random Access Memory"**, CMOS-compatible FeFET NVM, TRL 4 | Saptarshi Das (listed contact) | [licensing.prf.org](https://licensing.prf.org/product/fetram--a-novel-organic-ferroelectric-based-random-access-memory) [REPORTED-P, via snippet] | Not shown | **Listed as available** | Low-med (organic FE; an older concept) |
| **Georgia Tech** (Office of Technology Licensing) | **3T IWO BEOL eDRAM**; FeFET CIM; 3D NAND CIM | Shimeng Yu | [GT, 2024](https://hg.gatech.edu/node/675050) [REPORTED] | Not retrieved | Unverified | **High** (oxide gain cell) |
| **Georgia Tech** | HZO ferroelectric capacitors / FE NAND | Asif Khan; Suman Datta | [UNVERIFIED-training] | Not retrieved | Unverified | Med |
| **Penn** (Penn Center for Innovation) | **AlScN ferroelectric diode NVM to 600 °C** (with AFRL) | Deep Jariwala, Roy Olsson | [Penn Engineering, 2024-05](https://www.engineering.upenn.edu/stories/turning-up-the-heat-on-data-storage/) [REPORTED] | Not retrieved | Unverified; AFRL co-ownership likely | **High** for a defense extreme-temperature NVM (DARPA/USAF topics exist) |
| **UT Austin** (Discovery to Impact) | 3T1C IGZO gain cell for compute-in-eDRAM; 2D "atomristor"; spintronic devices | ISCAS-2021 authors; Deji Akinwande; Jean Anne Incorvia | [ISCAS 2021](https://sites.utexas.edu/CRL/files/2021/05/IGZO_eDRAM_CIM_ISCAS_2021.pdf) [REPORTED]; rest [UNVERIFIED-training] | Not retrieved | Unverified | Med |
| **Univ. of Minnesota** (Technology Commercialization; MN-IP program) | SOT-MRAM, novel spin-orbit materials; gain-cell eDRAM circuits | Jian-Ping Wang; Chris H. Kim | v2: UMN-assigned **US 10,529,775** "Two-terminal spintronic devices" (Wang) ([Justia, via snippet](https://patents.justia.com/inventor/jian-an-wang?page=13)) [REPORTED-P]. New UMN **Spin Technology Center** with Polar Semiconductor and Honeywell Aerospace ([UMN CSE](https://cse.umn.edu/node/194186)) [REPORTED-P] | US 10,529,775 (licence status not shown) | No portal listing surfaced | Med (MRAM moonshot); UMN's pre-set startup terms are a plus; the Polar/Honeywell link gives a U.S. 200mm path |
| **Univ. of Michigan** (Innovation Partnerships) | RRAM / memristor arrays (Crossbar origin); memristor CIM (MemryX lineage) | Wei Lu; Zhengya Zhang | [UNVERIFIED-training] | Not retrieved | Core RRAM likely already licensed to Crossbar | Low-med |
| **Stanford** (OTL) | TCCT thyristor (expired); RRAM/PCM/monolithic 3D; 2D/PCM superlattice; N3XT | Nemati & Plummer; H.-S. Philip Wong; Eric Pop; Subhasish Mitra | [UNVERIFIED-training]. v2: **Docket S18-116**, multi-bit (3 b/cell) programming/read for HfO₂ 1T1R ReRAM, shown on a 4Kb array in 130nm; related S18-124 ([Stanford TechFinder](https://techfinder.stanford.edu/print/pdf/node/30553)) [REPORTED-P, via snippet] | US 6,229,161 (TCCT, expired) [UNVERIFIED-training]; S18-116 patent no. not shown | S18-116 listed (licensing contact given) | Low-med; S18-116 is the most relevant to a ReRAM-on-130nm product |
| **MIT** (TLO) | Protonic programmable resistors (analog memory); SOT; CNFET+RRAM M3D | Bilge Yildiz, Ju Li, Jesús del Alamo; Luqiao Liu; Max Shulaker | [UNVERIFIED-training] | Not retrieved | Unverified | Low (TRL 3–4) |
| **Cornell** (Center for Technology Licensing) | Spin-Hall SOT switching; nitride ferroelectrics (ScAlN); SUPREME JUMP 2.0 center | Dan Ralph, Robert Buhrman; Debdeep Jena, Huili Grace Xing | [UNVERIFIED-training]; SUPREME per p1-funding | Not retrieved | Unverified | Low-med |
| **UCLA** (TDG) | VCMA "MeRAM" (spin-out Inston Inc.) | Kang L. Wang; Pedram Khalili (now Northwestern) | [UNVERIFIED-training] | Not retrieved | Likely licensed to Inston; status unknown | Low |
| **UC Berkeley** (IPIRA) | HZO / negative-capacitance FE devices; magnetoelectric (MESO lineage) | Sayeef Salahuddin; R. Ramesh (moved to Rice ~2023) | [UNVERIFIED-training] | Not retrieved | Unverified | Low |
| **UC San Diego** (Office of Innovation & Commercialization) | PRISM JUMP 2.0 center (memory-centric computing); neuromorphic devices | PRISM PIs; Duygu Kuzum | PRISM per p1-funding [UNVERIFIED]; rest [UNVERIFIED-training] | Not retrieved | Unverified | Med for software/architecture IP |
| **Arizona State** (Skysong Innovations) | PMC/CBRAM (base **expired**); dendritic PUF/anti-counterfeit; rad-effects | Michael Kozicki; Hugh Barnaby | US 5,761,115 (expired) [UNVERIFIED-training] | — | Base free to practice; newer filings unverified | Low for memory; med for **anti-counterfeit tagging** of recert memory (§3C link) |
| **Notre Dame** (IDEA Center) | FeFET devices/arrays; FeFET-based CIM | Kai Ni; X. Sharon Hu | [UNVERIFIED-training]. v2: **US 11,532,355**, FE-superlattice multi-level NVM cell, co-assigned to UC Regents and Notre Dame (Kai Ni, Suman Datta) ([StorageNewsletter, via snippet](https://www.storagenewsletter.com/?p=257234)) [REPORTED] | US 11,532,355 | Licence status not shown | Med |
| **WARF (UW-Madison)** (v2) | Field-free perpendicular **SOT-MRAM** cell | n/a | [WARF P190333US01](https://warf.org/technologies/summary/P190333US01) [REPORTED-P, via snippet] | Not shown | **Listed** (contact WARF for status) | Low-med (MRAM moonshot) |
| **Univ. of Tennessee (UTRF)** (v2) | Energy-efficient **STT-MRAM read/write circuits** | n/a | [UTRF 23156](https://utrf.tennessee.edu/technologies/23156) [REPORTED-P, via snippet] | Patent pending | **Listed** | Low (circuit IP; useful only to an MRAM-macro designer) |
| **Penn State** (Office of Technology Transfer) | Wurtzite AlBN ferroelectrics; 2D memtransistors; CHIMES JUMP 2.0 | Jon-Paul Maria, Susan Trolier-McKinstry; Saptarshi Das | [UNVERIFIED-training]; CHIMES per p1-funding | Not retrieved | Unverified | Med (FE nitrides overlap Penn AlScN) |
| **Northwestern** (INVO) | MoS₂ memtransistors; SOT/VCMA MRAM | Mark Hersam; Pedram Khalili | [UNVERIFIED-training] | Not retrieved | Unverified | Low |
| **UMass Amherst / USC** | Multi-level RRAM (TetraMem lineage) | Qiangfei Xia; J. Joshua Yang | [UNVERIFIED-training]; TetraMem [REPORTED] | Not retrieved | Core likely licensed to TetraMem | Low |
| **Princeton** (Office of Technology Licensing) | Charge-domain SRAM in-memory compute (EnCharge AI lineage) | Naveen Verma | [UNVERIFIED-training] | Not retrieved | Likely licensed to EnCharge | Low (precedent only) |
| **SUNY Albany / NY CREATES** | 300mm HfO₂ FE memory JDA with Fraunhofer IPMS | — | [idw, 2025-05-16](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale) [REPORTED] | — | JDA IP, not portal-listed | Med as an **East Coast 300mm FE R&D access point**, not a license |
| **NC State, RPI, Columbia** | No memory-specific licensable lead identified from evidence or memory | — | — | — | Run portal queries (§9) | Unknown |

### 6.3 National labs and federal sources

| Lab / agency | Memory-relevant IP or asset | Mechanism | Evidence | Fit |
|---|---|---|---|---|
| **Sandia** (NM) | **HZO FeRAM + binary/32-state FTJs in trusted MESA fab, 200mm** (2026-05-13); ionic/ECRAM synaptic devices (training) | License + CRADA; Strategic Partnership Project; NM Small Business Assistance (NM firms only) | [Sandia](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) [REPORTED]; licensing listing / CRADA offer **not found** (v2) [UNVERIFIED] | **Best single lead, but unconfirmed** (internal LDRD; confirm with Sandia LTT before relying on it). Rad-hard NVM for space/DoD; trusted-foundry provenance |
| **AFRL** (+ TechLink as DoD licensing intermediary) | AlScN ferro-diode co-invention with Penn; DoD lab patents brokered by TechLink | DoD patent license via TechLink; CRADA | Penn [REPORTED]; TechLink role [UNVERIFIED-training] | High (pairs with Penn) |
| **NRL** | Spintronics/magnetics research | Navy tech-transfer license | [UNVERIFIED-training] | Low |
| **LANL** | LANSCE neutron single-event-effect testing (asset, not IP) | Paid beam time | p1-funding [UNVERIFIED-M] | Supports rad-hard qualification |
| **ORNL / LBNL / Argonne / BNL** | Nanoscience user facilities (CNMS, Molecular Foundry, CNM, CFN); ferroelectric/oxide materials science | User proposals (free for non-proprietary work); licensing; LEEP fellowships (ORNL, LBNL, ANL) | p1-funding [UNVERIFIED-M] | Characterization access; no specific licensable memory device identified |
| **NREL / PNNL** | Low memory relevance (PNNL: memory-centric HPC architecture) | — | p1-funding | Low |
| **NASA** (T2 portal) | High-temperature SiC electronics (Glenn); rad-tolerant systems; no memory device identified | NASA patent license (startup program historically low-cost) | [UNVERIFIED-training] | Low |

**Federal rights that come with lab/university IP** [UNVERIFIED-training]:
- **Government-use license.** Bayh-Dole §202(c)(4) gives the U.S. government a non-exclusive license to federally funded inventions. You cannot charge DoD royalties on the licensed patent itself, though you can sell products.
- **U.S.-manufacture preference.** Bayh-Dole §204: an exclusive licensee must "substantially manufacture" in the U.S. any product sold in the U.S. Waivers are possible.
  - DOE's **2021 Determination of Exceptional Circumstances** extends this to DOE-funded inventions more strictly.
  - **This aligns with "American Memory".** It also means a Sandia-licensed part fabbed at TSMC or TSRI needs a waiver.
- **March-in rights.** Rarely used.

### 6.4 Typical license terms for a university-IP startup

[UNVERIFIED-training ranges; no 2025–26 survey retrieved]

| Term | Typical range | Notes for this founder |
|---|---|---|
| Option (6–12 months, to evaluate and raise money) | $1k–$10k | Lets an STTR/SBIR proposal name licensed IP. **Do this first.** |
| Exclusive-license issue fee | $0–$50k | Startups often defer it until a financing (e.g., the first $1–2M raised) |
| Reimbursement of past patent costs | $10k–$150k | Usually the **largest real cash item**. Negotiate deferral or a narrower family |
| Equity | 2–10% (≈5% typical) | Often anti-dilutive through the first ~$1–5M raised |
| Running royalty | 1–5% of net sales (1–3% for semiconductor components) | Royalty stacking matters if you also license Weebit or Sandia IP |
| Sublicense revenue share | 10–50%, declining with stage | Matters only if you become a licensor (not recommended, §5) |
| Annual minimum royalty / license maintenance | $5k–$50k, escalating from year 2–4 | Kills zombie licenses; plan for it |
| Milestone payments | $10k–$250k (first sale, financing, sublicense) | Negotiable |
| Field of use | Narrow fields cut cost (e.g., "rad-hard NVM for space") | Ask for a narrow exclusive field plus a non-exclusive wider field |
| Diligence obligations | Product-development milestones; termination if missed | Align with the 18-month plan |
| Know-how / sponsored research | $50k–$300k/yr if bundled | Often needed to make oxide/FE processes reproducible |
| National-lab specifics | Labs offer licenses and options. DOE's 2011 "America's Next Top Energy Innovator" set $1,000 option fees; some labs keep low-cost startup options | CRADA: no federal money flows to the company. U.S.-manufacture clauses are stricter |

### 6.5 How fast deals close

[UNVERIFIED-training / ESTIMATE]

| Instrument | Typical time | What slows it |
|---|---|---|
| Option agreement | 2–8 weeks | Inventor conflicts; prior options |
| Express / standard startup license (pre-set terms, where offered) | Days to 4 weeks | — |
| Negotiated exclusive startup license | 2–6 months | Equity terms, patent-cost deferral, field of use |
| National-lab license | 3–9 months | Federal approvals; U.S.-manufacture plan; export-control review |
| CRADA | 3–12 months | Statement of work, IP terms, DOE site-office approval |
| DoD lab license via TechLink | 2–6 months | — |

### 6.6 What the IP path costs at T0

[ESTIMATE; assumptions file]
- Option $5k + scoped FTO search and memo ~$15k + provisional filings on own improvements ~$5k = **≈$25k**, about **half of the founder's <$50k budget**.
- Converting the option to an exclusive license typically adds **$10k–$150k** in deferred patent costs plus annual minimums. That is a **T1 event**, to be funded by an STTR Phase I (~$150k–$300k, per p1-funding) or by angels.
- **Gate:** don't exercise until a fab (SkyWater, Sandia MESA, NNCI cleanroom) has agreed in writing to run the module.

---

## 7. Implications for the venture (handed to Phase 2/3)

1. **Kill as IP plays:**
   - Licensing in DRAM-class IP: oxide 4F², 3D DRAM, HfO₂ DRAM+, XPoint. All closed.
   - Capacitor-less Si: free but dead.
   - NRAM / 2D / organic: premature or zombie.
   - Becoming a memory-IP licensor: 5–10 years to revenue.
2. **Viable IP-enabled paths, ranked for this founder:**
   - **(a) Product on licensed, PDK-resident IP:** Weebit ReRAM or OpenRAM SRAM on SkyWater S130, for a U.S.-made secure/eNVM/long-lifecycle part. T1–T2; IP cost known after one call.
   - **(b) Sandia HZO FeRAM license + CRADA + STTR:** rad-hard NVM for space and defense. T1; needs a technical PI.
   - **(c) Penn/AFRL AlScN extreme-temperature NVM + DARPA/USAF SBIR:** T1; TRL ~3–4; moonshot within the niche.
   - **(d) University oxide gain-cell option (Purdue/GT):** keeps an A1-01 door open for ~$5k. Exercise only if a fab partner appears.
3. **Patent intelligence as a T0 software product.** It overlaps A1-14 "MemTech Atlas". Expiry calendars, assignment tracking and litigation dockets for memory IP are the kind of data a software founder can build fast. They would serve FTO counsel, recert/brokerage firms and investors. This is a candidate card for Phase 2 rather than a finding; it needs demand validation.
4. **FTO gates to add to Phase 3 scoring:**
   - Any DDR5 module or appliance concept → Netlist PMIC FTO.
   - Any IGZO cell → SEL FTO.
   - Any Everspin STT design-in → ITC 337-TA-1487 outcome (~2027-07).
   - Any VCT-like device → Samsung/Micron/Unisantis FTO.
5. **Cycle-proofing.** IP-licensed niche NVM (rad-hard FeRAM, ReRAM eNVM, Toggle-class MRAM) is **indifferent to a 2028–29 DRAM glut**. It is priced per part or per wafer to defense and industrial buyers. DRAM-substitute IP would die in a glut.

---

## 8. What contradicts or corrects the mission premise

- **§3E "licensing a university/lab patent is underused":** partly true. Cheap and accessible, yes. But it is **not the binding constraint**; fab access, know-how and a technical PI are. No university memory IP found is production-ready on a U.S. line.
- **§3A "cheaper material systems" (IGZO):**
  - The *material* is IP-cheap now: the a-IGZO base expired ~2023–25.
  - The *memory cell and integration* are thickly patented by SEL and by the DRAM makers' 4F² VCT programs.
  - "Cheaper materials" ≠ "unencumbered IP".
- **§3A Ferroelectric "any licensable path?":** yes, but for niche **rad-hard/extreme-temperature NVM** (Sandia, Penn/AFRL), not DRAM replacement. FMC and Micron are closed.
- **§3A MRAM "which DRAM sockets can MRAM take":** that question now carries an **IP-supply caveat**. Everspin STT faces a possible ITC exclusion around mid-2027.
- **§3C U.S. module assembly:** the Netlist PMIC verdicts make "Assembled in USA DDR5 RDIMM" an IP problem as well as a die-supply problem (consistent with p1-backend's S5 kill).

---

## 9. Verification queue (run when web access returns)

Exact actions, in priority order:

1. **Weebit/SkyWater terms.** Ask SkyWater's S130 ReRAM IP page or sales contact for the license/royalty model for a fabless startup, and the minimum order (MPW vs full lot).
   - *v2 partial:* model = licence fee + NRE + volume royalties. Analyst-estimated upfront fees are $0.3–2.6M.
   - The Efabless prototype route is gone. **Ask whether ChipFoundry or SkyWater MPW offers the ReRAM block**, and how IonQ ownership affects terms.
2. **Sandia.** Sandia IP/licensing portal and DOE Lab Partnering Service. Search "hafnium zirconium oxide ferroelectric", "ferroelectric tunnel junction", "MESA". Ask about CRADA availability for HZO FeRAM.
   - *v2:* web searches found no listing. This needs a direct inquiry; the portal itself was not reachable.
3. **Penn Center for Innovation.** Search "AlScN ferroelectric diode" and "Jariwala". Also query TechLink for AFRL co-owned filings.
4. **Purdue OTC.** Search "indium oxide transistor", "Peide Ye", "monolithic 3D". **Georgia Tech OTL:** "Shimeng Yu", "IWO", "gain cell".
5. **Netlist status.** Federal Circuit decisions 2025–26 on US 11,016,918, US 11,232,054, US 10,949,339 and US 7,619,912; any Netlist ITC complaint (2025–26); Netlist 10-Q (2026-Q3) legal proceedings section.
6. **ITC 337-TA-1487.** EDIS docket: asserted patent numbers, the evidentiary-hearing date and the target date. *v2: patent numbers resolved (§3.3); the hearing and target dates are still open.*
7. **Assignment-record searches** at the patent office: assignor "Spin Memory, Inc." or "Spin Transfer Technologies"; "Nantero"; "T-RAM Semiconductor"; "Innovative Silicon"; "Qimonda" + "ferroelectric"; "4DS Memory"; "Antaios".
8. **Base-patent checks** (Google Patents): US 5,695,864; US 6,545,906; US 5,761,115; US 4,873,664; US 6,229,161 (title, assignee, expiry); the earliest Qimonda HfO₂-FE family member (priority date and owner); and the JST a-IGZO family (expiry).
9. **SEL.** Count granted U.S. patents with assignee "Semiconductor Energy Laboratory" and terms "memory" + "oxide semiconductor" (2015–2026). Check for any SEL licensing program for non-display LSI.
10. **NEO Semiconductor.** Granted U.S. patent count and any 2026 licensee announcement. *v2: no licensee as of 2026-05.*
11. **University terms.** The latest AUTM Licensing Activity Survey (median royalty and equity by field), and UMN MN-IP or other pre-set startup-license programs still offered in 2026.
12. **Nantero, Kepler Computing, SunRise Memory, Crossbar.** 2025–26 status (funding, acquisitions, licensees).

---

## 10. Sources

Every URL above is logged in `research/sources/p1-ip.jsonl` (89 records). Each is marked CROSS-REFERENCE, meaning another agent saw it in search results this session and p1-ip did not open it. Training-knowledge statements carry **[UNVERIFIED-training]** and no URL, per CONVENTIONS ("never invent a URL").
