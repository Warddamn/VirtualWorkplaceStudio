# DD5 — U.S. Open Memory IP (compiler service → gain-cell & ReRAM macros)

`04_DEEPDIVES/open-memory-ip.md` · Author `p4w-open-memory-ip` · As of 2026-11-01

- **Model:** `models/open-memory-ip.py`, re-run 2026-11-01, exit 0. Output is captured in `research/phase4/open-memory-ip_model_output.md`.
- **Research notes:** `research/phase4/open-memory-ip_notes.md`.
- **Sources:** `research/sources/p4-open-memory-ip.jsonl`, plus cross-references in `p4w-open-memory-ip.jsonl`.
- **Model calendar:** m1 = Dec-2026. The glut scenario starts at m14 (Jan-2028).
- **Tags:** [VERIFIED-git] marks primary data read directly from a public git repository. Other tags follow `research/CONVENTIONS.md`.

---

## 0. Header

**Name:** U.S. Open Memory IP.

**Pitch:** Sell SRAM macros that are bigger than anything available free, silicon-characterized and warrantied, to university labs, startups and SBIR teams taping out on SkyWater 130nm and GF180 open shuttles. Charge a subscription plus a fee per tapeout, and use the revenue and credibility to earn an option on gain-cell and ReRAM macros.

**Anchor and folded concepts.** The quotes are exact text from `03_SCORING.md` §7.5 and `research/phase3/scores_raw/*.json`.

| Role | ID | Concept | Tier | Why it is in this bundle |
|---|---|---|---|---|
| Anchor | C-33 | OpenRAM macro service for U.S. open-PDK tapeouts (SkyWater S130) | T0 | Founder scorer: "a credible part-time wedge, not an endgame." Card: "unless it becomes a broader open-PDK IP/characterization house (gf180mcu, IHP, gain-cell IP)" |
| Folded | C-32 | Si gain-cell eDRAM (GCRAM) IP for U.S. trailing-node SoCs | T2 | Veteran scorer: "Better engineering than C-01 (zero masks, no contamination fight)". Same PDK and the same compiler skills as C-33. |
| Folded | C-22 | TrustNVM: U.S.-made ReRAM secure-NVM chiplet on SkyWater S130 | T2 | Founder scorer: "The cleanest U.S.-made device path in the set". Weebit ReRAM is already qualified in S130. |

**Why folded:** one PDK, with the anchor as the wedge into the other two. The same scorers warn against the product stage: "RAAAM already owns the commercial Si gain-cell seat" (veteran, C-32), "a non-exclusive license buys no moat" (VC, C-22), and on the anchor, "likely a <$0.5-1M ARR lifestyle business." (VC). So C-32 and C-22 are a gated option. They go ahead only after wedge traction, an STTR award and a clean freedom-to-operate (FTO) read.

**Capital tier:** the wedge is **T0**, run on the founder's $40k, with a cash low of $20.4k at m7 (model §6). The product stage is **T2**: about $4.3M external to reach a qualified macro (model §9).

**Scores and ranks** (`scores.csv`, 40 scored concepts):

| ID | Default | Capital-constrained | Moonshot |
|---|---|---|---|
| C-33 (anchor) | 80.0 (#3) | 82.5 (#5) | 76.7 (#2) |
| C-32 (folded) | 59.0 (#25) | 55.8 (#28) | 60.8 (#22) |
| C-22 (folded) | 57.0 (#31) | 54.2 (#29) | 59.2 (#24) |

**Three separate verdicts**

| Question | Verdict | One line |
|---|---|---|
| **POSSIBLE?** | **Yes** (wedge); **yes, but not by us** (T2) | The compiler and PDKs exist, and a 1 KB sky130 macro is silicon-verified (TRL 6). No public sky130 macro of 16 KB or more exists; the published 16 KB attempt left only a log [VERIFIED-git]. Gain cells (TRL 5) and Weebit ReRAM (TRL 6) are real, but other companies own them. |
| **PROFITABLE?** | **Marginal** | 66% gross margin and cash-positive from m8, but only with the founder unpaid. The founder can be paid from m20. ARR at m36 is $158k ($424k run-rate with services) against a ~$0.75M/yr market ceiling. A free large-macro release in the same channel means the founder is never paid (model §6–7). |
| **DOABLE BY THIS FOUNDER?** | **Yes** (wedge); **no** (T2) | Automation, CI, the portal and sales are the founder's skills; part-time work plus ~200 contract VLSI hours is enough. T2 needs a full-time circuit cofounder, a university STTR PI (the SBIR PI rule excludes the founder while employed) and ~$4.3M. |

**Brutal summary**
- **Real gap, cheap test, glut-proof.** The largest free macros are 4 KB on sky130 and 1 KB on GF180 [VERIFIED-git]. A 60% DDR5 glut cuts m36 ARR by only 20%.
- **Too small.** About 36 paying projects a year sets a ceiling of about $0.75M/yr.
- **Mostly services.** Subscriptions are only 30–37% of revenue.
- **Paying the founder needs about 18 accounts by m18,** which is 25% of every account that could exist.
- **The killer is "free", not DRAM.** OCD and UCSC committed code in the past week, and Chips4Makers taped out SRAM test chips in Jul-2026.
- **The T2 climb is weak.**
  - Gain cells give 1.25–1.43× density, not 2–4×, and RAAAM holds the seat.
  - ReRAM loses to Toggle MRAM everywhere except magnet immunity.

**Verdict: a credible FALLBACK or side line, not a venture-scale PRIMARY.**

---

## 1. How it works (for a smart non-engineer)

**Every useful chip needs a scratchpad,** a block of fast on-chip memory (SRAM). Designers don't draw it by hand. They drop in a pre-built block called a *macro*.

A macro is like a pre-engineered roof truss. Someone has drawn it, checked it against the factory's rules and, ideally, built one and measured how fast it runs and when it fails. Big chip companies get these trusses free from their foundry, or they buy compilers from Synopsys or Cadence under NDA.

**A second, open world now exists.** It has three parts:
- **Public design rules (PDKs):** for SkyWater's 130nm fab in Bloomington, MN ("sky130") and for GlobalFoundries' 180nm process ("GF180").
- **Cheap shared wafer runs ("shuttles"):** dozens of projects split one wafer for about $7–15k a slot.
- **Volume:** about 300 full-chip projects a year use U.S.-fab open or academic shuttles (model §2).

**The free memory blocks for these processes are small:**
- The largest are 4 KB on sky130 and 1 KB on GF180.
- Only a 1 KB sky130 macro has been proven in silicon.
- A small RISC-V microcontroller wants 8–64 KB.

**Small blocks also waste space.** A 2 KB sky130 macro packs 57.6 kbit/mm², while the cell itself allows 527 kbit/mm². Most of the block is "plumbing": decoders and sense amplifiers around a tiny array. A properly banked 32–64 KB macro reaches about 316 kbit/mm², 5.5× better. That takes better generator software and verification, not new physics (model §1).

**What the company does:**

```
 OpenRAM (free) ──► founder's automation: generate 8–64 KB, DRC/LVS check, timing models, CI
                                   │
                                   ▼
             contract VLSI engineer reviews ──► test macros ride a shuttle slot ($3.75–15k)
                                                         │   3–6 months in the fab
                                                         ▼
                             bench measurement: speed, voltage, temperature, yield
                                                         │
                                                         ▼
   customer gets: layout + measured timing + integration help + warranty
   pays: $200 or $800/month · $3k or $10k per tapeout · $20k characterized licence
```

**Why pay for something built on free code?** A failed memory block wastes the whole $7–15k slot and 3–6 months. The customer buys confidence, not files.

**The later options (T2):**
- **A gain cell (C-32)** uses 2–3 transistors instead of SRAM's 6. It holds a tiny charge that leaks away in microseconds to milliseconds, so it must be rewritten ("refreshed") like DRAM. The payoff is lower idle leakage and 1.25–1.43× density in measured silicon ([BIU CRIS](https://cris.biu.ac.il/en/publications/4t-gain-cell-providing-unlimited-availability-through-hidden-refr/)) [REPORTED].
- **ReRAM (C-22)** stores data by switching a thin oxide's resistance, so it keeps the data with the power off. Weebit Nano has already qualified a 256 Kb ReRAM block in SkyWater's 130nm process. We would license it to build a small key-storage chip.

**Where it beats "RAM" (Rule 4).** Not on $/GB: sky130 SRAM costs about $1,330/GB in silicon, 73× DDR5's base-case price (model §1).
- **Wedge axis: supply security and access.** That means the time and cost to get characterized on-chip memory into a U.S.-fabbed ASIC. The buyer is an open-shuttle team with no NDA compiler.
- **C-22 axis: trusted U.S. flow plus magnet immunity.** The buyer is a defense secure-boot socket.

---

## 2. Cost and unit-economics model

All figures come from `models/open-memory-ip.py` (section numbers refer to its printed output) unless another source is cited. Every price, rate and conversion assumption is an [ESTIMATE]; the basis for each is listed in the model's INPUTS block and in `research/assumptions/p4-open-memory-ip.md`.

### 2.1 The axis is not $/GB

| Item | Value | Source |
|---|---|---|
| sky130 6T bitcell (1.896 µm²) | 527.4 kbit/mm² limit | [SkyWater bitcell lib](https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram) [VERIFIED-git] |
| Largest free sky130 macros (OpenRAM 1 KB / 2 KB) | 43.0 / 57.6 kbit/mm² | [efabless macros](https://github.com/efabless/sky130_sram_macros), [VLSIDA macros](https://github.com/VLSIDA/sky130_sram_macros) [VERIFIED-git] |
| Banked 32–64 KB macro, 60% array efficiency | 316.5 kbit/mm² (5.5×) | model §1 [ESTIMATE] |
| Largest free GF180 macros (GF 512 B / OCD 1 KB) | 19.6 / 52.7 kbit/mm² | [GF IP](https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram), [OCD](https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram) [VERIFIED-git] |
| Gain cell vs 6T density | 1.25–1.43× (silicon); 1.67–2.0× (vendor) | [Silicon Saxony 2026-09](https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/) [REPORTED] |
| sky130 SRAM vs DDR5 (BASE $18.33 / GLUT $8.15 / SEVERE $2.04 per GB, from `models/dram_cost_stack.py`) | ~$1,330/GB = 73× / 163× / 653× | model §1; 01_LANDSCAPE §4.4 [ESTIMATE] |

Macros are priced per design. The DRAM cycle reaches this business only through design-start budgets.

### 2.2 Market

| Funnel step | Count | Source |
|---|---|---|
| Full-chip projects/yr on U.S.-fab open/academic shuttles | 298 | model §2. wafer.space 2×54 ([ws-run2](https://github.com/wafer-space/ws-run2)) [VERIFIED-git]; GF university pilot 40 ([Synopsys 2025-09-04](https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms?asPDF=1)). ChipFoundry 60, Cadence 30 and MOSIS/Commons/other 60 are [ESTIMATE] |
| Tiny Tapeout tiles in 2026 (a funnel, not buyers) | 899 | [TT sky-26a](https://github.com/TinyTapeout/tinytapeout-sky-26a), [sky-26b](https://github.com/TinyTapeout/tinytapeout-sky-26b), [ihp-26a](https://github.com/TinyTapeout/tinytapeout-ihp-26a), [gf-0p2](https://github.com/TinyTapeout/tinytapeout-gf-0p2) [VERIFIED-git] |
| × need memory beyond free macros | 30% | About 10 of 51 wafer.space Run 2 listings mention SRAM/RAM [VERIFIED-git] |
| × willing to pay | 40% | [ESTIMATE]; there is no willingness-to-pay data, and the kill test measures it |
| **Paying projects/yr** | **36** | model §2 |
| Active-account cap (×2 years per group) | 72 (43 academic, 29 commercial) | model §2 |
| **Serviceable ceiling at 100% share** | **$747.3k/yr** | model §2 |

**Commercial NDA customers are out of reach.** SkyWater's S130 "already offers… SRAM compilers" ([Silicon UK, 2025-07-29](https://www.silicon.co.uk/press-release/skywater-technology-expands-leadership-in-u-s-semiconductor-manufacturing-with-infineon-ip-license-agreement)), and mature-node compilers are traditionally foundry-sponsored ([D&R](https://www.design-reuse.com/news/9192/analysis-arm-artisan-merger-defining-moment.html)) [REPORTED].

### 2.3 Unit economics (BASE prices, model §3)

| Product line | Price | COGS | GM |
|---|---|---|---|
| A1 Subscription, academic | $200/mo | $58 | 71% |
| A2 Subscription, commercial | $800/mo | $102 | 87% |
| B1 Tapeout service, academic (12 contract h at $125) | $3,000 | $1,690 | 44% |
| B2 Tapeout service, commercial (30 contract h) | $10,000 | $4,150 | 58% |
| C Characterized licence (30 h + 10% warranty reserve) | $20,000 | $6,350 | 68% |

**Acquisition:**
- **Outbound:** 30 contacts a month × 25% reply × 15% close = 1.12 accounts a month.
- **Inbound:** ramps to 1.2 accounts a month.
- **CAC:** $0.2k cash, or $1.3k loaded with founder time.
- **Lifetime GP:** $5.4k academic and $31.4k commercial, for a blended LTV/CAC of 12.3×.

The 15% close rate is invented. The kill test measures it.

### 2.4 ARR, breakeven and cash low point (model §6)

| | BASE (DDR5 −10% in 2028) | GLUT (−60% from m14) | SEVERE (−90%) |
|---|---|---|---|
| First revenue | m4 (Mar-2027) | m4 | m4 |
| **Cash low point** (from $40.0k) | **$20.4k at m7** (Jun-2027) | $20.4k at m7 | $20.4k at m7 |
| Cash-flow breakeven, **founder unpaid** (first of 3 positive months) | m8 (Jul-2027) | m8 | m8 |
| First month with GP ≥ $11.85k (founder-paid breakeven)¹ | m18 | m23 | m28 |
| Founder full-time | **m20 (Jul-2028)** | m25 (Dec-2028) | m30 (May-2029) |
| Gross margin, 36 months | 66% | 64% | 62% |
| **Recurring ARR m12 / m18 / m24 / m36** | **$40.7k / $66.6k / $105.7k / $157.6k** | $40.7k / $58.9k / $78.2k / $125.8k | $40.7k / $54.6k / $70.9k / $105.7k |
| Run-rate incl. services m12 / m18 / m24 / m36 | $127.9k / $213.6k / $327.0k / $423.9k | $127.9k / $183.8k / $229.0k / $342.1k | $127.9k / $167.1k / $205.0k / $291.2k |
| 36-month revenue | $713.9k | $582.2k | $506.6k |
| Accounts at m36 (academic + commercial) | 18 + 12 | 17 + 10 | 16 + 8 |
| End cash at m36 | $219.3k | $175.4k | $175.4k |

¹ From the model's `summarize()["fte_be"]`, computed in the same run but not printed. The BASE m18 GP of $12.2k does appear in the printed §5 table.

**"Cash-positive from m8" means the business stops eating the founder's savings while the founder works for free.**

### 2.5 Revenue mix: a services business (BASE, model §5)

| Month | Subscriptions | Tapeout services | Licences | Total/month | Recurring share |
|---|---|---|---|---|---|
| m12 (Nov-2027) | $3.4k | $7.5k | $0.6k | $11.5k | 30% |
| m18 (May-2028) | $5.6k | $9.5k | $3.6k | $18.7k | 30% |
| m36 (Nov-2029) | $13.1k | $16.1k | $6.5k | $35.8k | 37% |

Every service and licence sale consumes contract VLSI hours. "SaaS" overstates it.

### 2.6 Sensitivity (BASE, one input at a time; model §7)

| Case | Cash low | 3-mo cash-positive from | Founder full-time | ARR m18 | ARR m36 | Run-rate m36 |
|---|---|---|---|---|---|---|
| Base | $20.4k | m8 | m20 | $66.6k | $157.6k | $423.9k |
| Price ×0.7 | $10.5k | m20 | **never** | $46.6k | $88.5k | $238.8k |
| Price ×1.3 | $27.0k | m8 | m15 | $102.9k | $211.7k | $563.8k |
| Close rate ×0.7 | $16.0k | m11 | m27 | $48.1k | $112.6k | $316.0k |
| Close rate ×1.3 | $24.3k | m8 | m16 | $95.8k | $191.8k | $504.6k |
| Churn ×1.3 | $20.3k | m11 | m21 | $63.6k | $144.8k | $402.2k |
| COGS ×1.3 | $17.7k | m11 | m23 | $66.6k | $153.8k | $416.8k |
| **Free-bundle shock at m18** | $20.4k | m8 | **never** | $49.5k | **$50.0k** | $154.4k |
| GLUT + free shock | $20.4k | m8 | **never** | $43.7k | $39.1k | $122.1k |
| SEVERE + all adverse 30% | **−$14.7k** | m20 | **never** | $26.0k | $43.2k | $121.7k |

**Price and free substitutes decide this business. DRAM barely matters.**

### 2.7 What must be true (model §8)

1. **Enough paying projects.** At least 36 a year: 298 projects × 30% need × 40% pay.
2. **Prices hold.** At ×0.7 the founder is never paid.
3. **Selling works.** Reply rate ≥25%, close rate ≥15%.
4. **About 18 active paying accounts (≈11 academic + 7 commercial) by m18.** That is **25% of the 72-account cap**; BASE reaches 12.7. The equivalent is 2.0 commercial tapeout services a month, or 0.9 licences a month.
5. **Large macros are buildable.** OpenRAM plus at most about 200 contract hours must yield timing-clean sky130 macros of 16 KB or more. This is untested [VERIFIED-git that only a log exists].
6. **No free release.** No channel owner gives away silicon-characterized macros of 16 KB or more for at least 18 months.
7. **Shuttles keep running.**
   - ChipFoundry runs a shuttle only if it is at least 50% full ([eeNews](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)) [REPORTED].
   - wafer.space Run 3 is listed only as "coming soon" ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2)) [REPORTED].

### 2.8 The T2 overlay: funding, not revenue (model §9)

| When | Step | $ | Funder |
|---|---|---|---|
| m6–m9 | STTR Phase I proposal with a university PI | founder time | — |
| m15 | STTR Phase I: sky130 gain-cell macro + test chip (≥30% to the university; only the ~7% fee is free cash) | $305.0k | NSF/DoD STTR |
| m18 | ReRAM probe on the Cadence SKY130 MPW (Weebit option) | $12.0k | Phase I / cash |
| m18–m24 | Weebit evaluation or licence (fee for a fabless startup unknown) | ~$100.0k | seed or Phase II |
| m27–m30 | Seed round, gated on run-rate ≥$250k plus gain-cell silicon | $2,500.0k | VC / strategic |
| m30 | STTR Phase II | $1,500.0k | NSF/DoD STTR |
| m30–m48 | Full-time circuit cofounder (2 years, loaded) | $440.0k | seed |
| m36–m54 | ReRAM chiplet: S130 mask set + JEDEC qualification + packaging | $950.0k | seed / Phase II / DoD |
| **Total external** | | **~$4,305k** | |

**What the overlay adds:**
- **Revenue:** at most one $75k gain-cell evaluation licence before m36, for 36-month revenue of $788.9k.
- **Cash:** operating cash excluding the seed falls to $161.6k, against $219.3k for the wedge alone.
- **Grants:** not revenue (A-04).

**Recurring ARR never reaches $250k in any modeled scenario by m36,** so the seed gate can only be met on run-rate.

---

## 3. Target customer and the first ten customers

**Beachhead:** funded open-shuttle teams with a real memory need. These are university labs and courses that tape out repeatedly, small commercial aggregators, open SoC and FPGA builders, and SBIR teams on SkyWater. Tiny Tapeout hobbyists are the free funnel, not buyers.

| # | Customer | Why they buy | How to reach |
|---|---|---|---|
| 1 | **Brown University ENGN2912e (Saligane lab)**, project BRWN on wafer.space Run 1 ([ws-run1](https://github.com/wafer-space/ws-run1)) [VERIFIED-git] | A repeat course tapeout on GF180, where the largest free macro is 1 KB. East Coast; also an STTR PI candidate. | Email the instructor. Offer a course pack ($200/mo) plus a $3k service each term. |
| 2 | **U.S. members of the Synopsys–GF GF180MCU university pilot** (40 universities) ([Synopsys](https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms?asPDF=1)) | A tapeout every term; the largest free GF180 macro is 1 KB. | Course pages and GF University Partnership contacts. Offer a per-course licence. |
| 3 | **Avalon Semiconductors** (AS03/AS04 multi-project dies with RISC-V cores and a DRAM controller) ([ws-run1](https://github.com/wafer-space/ws-run1), [ws-run2](https://github.com/wafer-space/ws-run2)) | A repeat commercial customer packing several designs per die, so area and confidence both matter. | Through the project listing. Commercial subscription plus a $10k service. |
| 4 | **TinyQV / TQVE builders** (RISC-V SoC, 9.5 kB scratch RAM on GF180) ([ws-run2](https://github.com/wafer-space/ws-run2)) | Already beyond the free 1 KB macro. | GitHub and the Tiny Tapeout community. Offer a free preview to win the reference design. |
| 5 | **FABulous eFPGA (mole99)** ([ws-run2](https://github.com/wafer-space/ws-run2)) | FPGA configuration memory built from SRAM macros, so density is the product. | GitHub. Academic licence. |
| 6 | **Cloneless** (tamper-resistant ASICs) and the **Tillitis/Zedulo eFUSE + SRAM** chip ([ws-run1](https://github.com/wafer-space/ws-run1)) | Secure key storage; the natural first C-22 ReRAM partners. | Project listings. Propose a joint Cadence ReRAM MPW block. |
| 7 | **Sandia National Laboratories (MESA)**, which licensed Mobile Semiconductor's 180nm compilers ([D&R](https://us.design-reuse.com/news/45774/mobile-semiconductor-180nm-memory-compilers-sandia-national-laboratories.html)) [REPORTED] | Has already paid for trailing-node memory IP. | After sky130 silicon data exists (m13+). Procurement-led; a long shot. |
| 8 | **DoD SBIR/STTR performers on SkyWater 130/90nm** (precise type) | Funded; need U.S.-fab memory with a warranty; can expense $10–20k. | SBIR.gov award search on "SkyWater", "130nm", "sky130" and "ASIC", then email the PIs (method; not yet run). |
| 9 | **NORDTECH (NY) and NEMC (MA) hub project teams** ([Cornell 2026-04-29](https://research-and-innovation.cornell.edu/?p=6460); [MassTech](https://masstech.org/news/northeast-microelectronics-coalition-hub-celebrates-3725-million-federal-funding-power)) | East Coast prototyping; PROPEL subsidizes lab and fab time. | Hub events. Ask to be listed as a hub IP resource. |
| 10 | **Channels: ChipFoundry Marketplace, Cadence SKY130 MPW, MOSIS 2.0** ([ChipFoundry](https://github.com/chipfoundry/caravel_user_project); [SkyWater/Cadence](https://www.skywatertechnology.com/lowering-barriers-to-silicon-cadence-launches-mpw-aggregation-service-for-sky130/); [USC ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/)) | They resell per shuttle. **They are also the parties best placed to bundle macros for free.** | Partnership calls in the kill test (§10). Offer a revenue share. |

**Partners to approach first:**
- **Open Circuit Design LLC (Tim Edwards)** as contract characterization partner.
- **UCSC VLSIDA** as STTR PI and upstream.

Both are also the likeliest free substitutes (§5).

---

## 4. Go-to-market

**Channel**
1. **Direct, named technical outreach** to the owners of public shuttle projects (they are listed in the wafer.space and Tiny Tapeout repositories).
2. **Open-core distribution.** Free preview macros (LEF and a datasheet) go on GitHub and PyPI; characterized data and support are paid.
3. **Listings and distributors.** Listings on ChipFoundry Marketplace and MOSIS 2.0. NSF Chip Design Hub awardees could distribute to academics ([NSF](https://www.nsf.gov/funding/opportunities/chip-design-hub-enabling-access-semiconductor-chip-ecosystem-design)).

**Pricing (model §3)**

| Offer | Academic | Commercial / SBIR | Anchor |
|---|---|---|---|
| Subscription: hosted generator, library, CI regression, support | $200/mo | $800/mo | $2.4k/yr is a sixth to a third of one $7–15k slot; $9.6k/yr is about two contract-engineer weeks at $125/h |
| Tapeout service: configuration, DRC/LVS, timing sign-off, integration review | $3,000 | $10,000 | 20–100% of a slot; the buyer is de-risking the whole spin |
| Characterized licence: measured data, PVT corners, 12-month warranty | — | $20,000 | Below Weebit's ~$0.1M first-ever eNVM licence ([MST Access](https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf)); Virage listed a compiler at $300k in 2001 ([Design World](https://www.designworldonline.com/synopsys-enters-embedded-memory-market/)) |

**Sales motion**
- **Founder-led and asynchronous, which fits the day job:** a technical email, a 20-minute call, then a deposit tied to a shuttle deadline.
- **The next ChipFoundry or wafer.space submission date is the closing event.**
- **Tiny Tapeout designers** get free macros, then convert to paid when they buy full-chip slots.

**First 90 days of selling** (from 2026-11-02, before the academic winter break; days 1–30 are the §10 experiment)

| Days | Actions | Measurable output |
|---|---|---|
| 1–30 | Landing page with real prices and $500 refundable deposits; 120 named contacts; 5 channel calls; contract review of the 16–32 KB macros | ≥3 paid deposits or ≥$15k in LOIs; written channel answers |
| 31–60 | Convert deposits into signed orders. Publish preview library v0.1 (8/16/32 KB sky130; 2/4/8 KB GF180). Sign a contractor statement of work (SOW). Apply for the ChipFoundry Marketplace. | ≥3 signed orders; SOW signed; ≥200 PyPI downloads [ESTIMATE target] |
| 61–90 | Schedule first deliveries against the next shuttle deadline. Follow-up sequence. Draft the NSF Project Pitch with a candidate PI. | ≥5 paying or committed accounts by m4 (Mar-2027, first model invoices); a PI letter of interest |

---

## 5. Competitors and why you would win

| Competitor | Offer | Price / position | Threat |
|---|---|---|---|
| **OpenRAM (UCSC VLSIDA)** | Open SRAM compiler for sky130 and gf180mcu | Free (BSD-3). v1.2.50 on 2026-10-27; 116 commits in 12 months ([OpenRAM](https://github.com/VLSIDA/OpenRAM)) [VERIFIED-git] | **High.** It can publish large characterized macros at any time. |
| **Open Circuit Design LLC** | GF180 SRAM, 64 B–1 KB, on wafer.space silicon | Free (Apache-2.0); last commit 2026-10-30 ([repo](https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram)) [VERIFIED-git] | **High on GF180.** Also the best contractor. |
| **Chips4Makers (Arrakeen)** | GF180 SRAM generator; 3 test chips on wafer.space G802 (Jul-2026) | Free ([GitLab](https://gitlab.com/Chips4Makers/arrakeen-sram-testchip)) [VERIFIED-git] | **High on GF180** |
| DFFRAM / GF `fd_ip_sram` | Flip-flop RAM up to 2,048 words; 64–512 B macros | Free; DFFRAM is flagged for hold violations on gf180mcuD ([DFFRAM](https://github.com/AUCOHL/DFFRAM)) [VERIFIED-git] | Medium / low |
| **SkyWater S130 compilers** | NDA SRAM compilers | Bundled ([Silicon UK](https://www.silicon.co.uk/press-release/skywater-technology-expands-leadership-in-u-s-semiconductor-manufacturing-with-infineon-ip-license-agreement)) [REPORTED] | Closes off all commercial S130 work |
| **Mobile Semiconductor** | SkyWater RH90 rad-hard SRAM compilers; 180nm compilers licensed to Sandia | Price not public ([SkyWater 2022-06-09](https://www.skywatertechnology.com/skywater-announces-availability-of-sram-memory-compiler-for-90-nm-strategic-rad-hard-by-process-offering/)) [REPORTED] | **High in DoD/trusted** |
| Cadence (ex-Arm Artisan), Synopsys | Commercial and foundry-sponsored compilers | The designer often pays $0 ([Silicon UK](https://www.silicon.co.uk/press-release/cadence-to-acquire-arm-artisan-foundation-ip-business)) [REPORTED]; Cadence also runs the SKY130 MPW | Medium; could bundle |
| **RAAAM** (C-32) | Proprietary 3T Si gain cell | $17.5M Series A led by NXP, Nov-2025 ([AnySilicon](https://anysilicon.com/news/raaam-memory-technologies-raises-17-5-million-in-oversubscribed-series-a-led-by-nxp-semiconductors/)); TSMC N2 test chip taped out Mar-2026 ([AnySilicon](https://anysilicon.com/news/raaam-selects-avnet-asic-as-its-vca-partner-for-tsmcs-2nm-gcram-development-and-qualification/)); GF FDX lead-customer access early 2027 ([Silicon Saxony](https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/)) [REPORTED] | **Decisive for C-32** |
| **OpenGCRAM (Stanford)** | Open gain-cell compiler (TSMC N40) | Free with the final paper ([arXiv 2507.10849](https://arxiv.org/html/2507.10849v1); [arXiv 2602.21278](https://arxiv.org/abs/2602.21278v1)) [REPORTED] | Removes "compiler" as a moat |
| **Everspin Toggle MRAM**, Honeywell trusted MRAM (C-22) | 16–32 Mb U.S.-made rad-tolerant NVM | Everspin: $40M DoW onshore program ([Electronics360 2026-04](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services)) [REPORTED] | **Decisive for C-22**, except where magnet immunity matters |

**Win conditions (honest)**
1. **Be first, by at least one shuttle cycle (about 6 months),** with silicon-characterized sky130 macros of 16 KB or more, measured-corner timing and a warranty.
2. **Sell what free code lacks:** sign-off, integration review, a named person on deadline day, a warranty. The layout files will leak by design, since only 11 of 51 listed wafer.space Run 2 projects are private [VERIFIED-git].
3. **Hire the free authors** as contractors or STTR partners.
4. **Serve the SBIR and Commons teams** on open PDKs, which Mobile Semiconductor does not.

**Where you lose:**
- **GF180,** probably within 12 months, because OCD and Chips4Makers already have silicon.
- **Commercial S130,** where the foundry compiler is free.
- **DoD rad-hard.**
- **Gain cells,** against RAAAM.
- **ReRAM,** against Toggle MRAM.
- **Whenever a channel owner makes memory a loss leader.**

---

## 6. IP position

**What you own:** almost nothing foundational.
- **The base is open.** OpenRAM is BSD-3, OCD is Apache-2.0, and the PDKs are open ([Google, 2023-11](https://opensource.googleblog.com/2023/11/open-source-pdks-joining-linux-foundation-chips-alliance.html?m=0)) [REPORTED].
- **What you would own:**
  - measured characterization data and test-chip designs;
  - banking, timing and CI automation, kept as trade secrets;
  - customer relationships and a warranty brand;
  - possibly weak patents on the periphery [ESTIMATE].
- **The moat** is "a first-mover lead that takes one shuttle cycle to copy" (VC scorer).

**What you license:**
- **For C-22: Weebit ReRAM.** SkyWater's licence is non-exclusive, with fees "not material" and contingent on customers ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/)). A product needs its own licence. Analysts estimate past upfront fees at about $0.1M (first ever), $0.29M and $1.8–2.6M (01_LANDSCAPE §9; [MST Access](https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf)) [REPORTED]. The fee for a fabless startup is unknown.
- **For C-32:** STTR or university IP, from UCSC VLSIDA or Stanford.

**What you can't own or use:** RAAAM's GCRAM (Bar-Ilan/EPFL lineage), SkyWater's NDA compilers, or Mobile Semiconductor's RH90 compilers.

**FTO risks, ranked**
1. **Gain-cell patents (C-32).** RAAAM and its Bar-Ilan/EPFL lineage hold an active estate, and the area is crowded: for example, 2T-cell retention scaling is described in [US 11,127,455](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11127455) [REPORTED]. Get a landscape read before any C-32 spend (§11 #10).
2. **Efabless platform patents.** ChipFoundry acquired 15 issued and 3 pending patents ([Minster/GlobeNewswire 2025-09-03](https://business.minstercommunitypost.com/minstercommunitypost/article/gnwcq-2025-9-3-chipfoundry-acquires-efabless-assets-to-propel-custom-silicon-innovation)) [REPORTED]. Their scope is [UNVERIFIED]. Check them before building an Efabless-like hosted generator or marketplace.
3. **Open-source licence terms.** BSD-3 needs attribution. Apache-2.0 needs notices and carries a patent-termination clause. Low risk if followed.
4. **ReRAM resale.** Weebit's terms may bar selling parts made from Cadence-MPW die [UNVERIFIED]. This is a kill-test question.

---

## 7. Regulatory and funding path

**Rules that matter**
- **Export controls.**
  - **The wedge is EAR99-class.** Scorer: "Negligible; BSD open-source tooling, EAR99".
  - **The C-22 rad variant is controlled.** It falls under 3A001.a.1 / 9A515, possibly ITAR XV(d), which means U.S.-person-only data and about $25–75k/yr of compliance (01_LANDSCAPE §8) [UNVERIFIED-M].
  - **Screen customers at onboarding.** Tiny Tapeout users are global.
- **Trusted foundry.**
  - SkyWater is a DMEA Category 1A Trusted Foundry ([BusinessWire 2026-01-26](https://www.businesswire.com/news/home/20260125927336/en/IonQ-to-Acquire-SkyWater-Technology-Creating-the-Only-Vertically-Integrated-Full-Stack-Quantum-Platform-Company)).
  - IonQ, which closed its acquisition on 2026-07-31, says SkyWater "remains fully committed to all of our semiconductor foundry customers" ([IonQ](https://ionq.com/news/ionq-completes-acquisition-of-skywater-technology)) [REPORTED]. There is no post-close DMEA confirmation.
  - Open-MPW die are not trusted-flow parts [ESTIMATE].
- **Warranty.** E&O insurance at $250/mo from the first licence (model).

**Non-dilutive funding**
- **SBIR PI constraint.**
  - The SBIR PI must spend more than half their time with the small business, at award and for the whole project ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)). **That excludes the founder while they keep the day job.**
  - The STTR PI may be employed by the research institution ([NIH GPS 18.5](https://grants.nih.gov/grants/policy/nihgps/html5/section_18/18.5_small_business_innovation_research_and_small_business_technology_transfer_programs.htm)).
  - **So the route is STTR with a university PI:** UCSC VLSIDA (Guthaus), the Stanford OpenGCRAM group, or the Brown Saligane lab.
- **STTR terms.**
  - NSF Phase I is up to $305k (NSF 26-510). The Semiconductors topic includes an IC Design subtopic ([NSF Seed Fund](https://seedfund.nsf.gov/topics/semiconductors/); [summary](https://grantedai.com/grants/semiconductors-s-sbir-sttr-program-national-science-foundation-nsf-small-bu-ef99bad7)) [REPORTED]. A Project Pitch comes first.
  - The program is reauthorized through 2031-09-30 ([IEDC 2026-04-15](https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/)).
  - New rules: per-firm proposal caps from FY2027, foreign-ownership screening, and Strategic Breakthrough awards that need a prior Phase II and a 1:1 match ([Wiley](https://www.wiley.law/alert-SBIR-STTR-Reauthorization-Brings-New-Opportunities-and-Obligations-to-Consider)).
  - At least 30% of the award goes to the university [UNVERIFIED].
  - **Grants are funding, not revenue** (A-04).
- **DoD.** No 2026 topic on memory compilers or trusted NVM was found. The only one found, DARPA DV017 on extreme-environment NVM, closed 2026-08-19 ([DARPA](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments)).
- **Other programs.**
  - Microelectronics Commons hubs: NORDTECH, and NEMC with PROPEL. The Commons has fabricated more than 61,000 chips ([NSTXL 2026-03](https://nstxl.org/microelectronics-commons-delivering-results-2026/)).
  - NSF Chip Design Hub, and MOSIS 2.0 ([AAC 2026-07](https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy)), as channels.
  - MA START ($100–500k), but only after a Phase II [UNVERIFIED-L/M].

**When and whether to raise**
- **Never for the wedge.** The cash low is $20.4k of $40k.
- **A $2.5M seed only at m27–m30, and only if all four of these hold:**
  1. run-rate ≥$250k (BASE reaches $327k at m24);
  2. STTR gain-cell silicon measuring ≥1.2× density;
  3. a clean FTO read;
  4. a named strategic investor or design partner. SkyWater/IonQ or a defense prime is plausible but unevidenced.
- **Otherwise stay T0 and harvest the cash.**

---

## 8. 18-month roadmap with milestones

| Month | Calendar | Milestone | Gate (measurable) |
|---|---|---|---|
| m0 | Nov-2026 | Kill experiment (§10) | §10 pass rules |
| m1 | Dec-2026 | Form the LLC; licence and warranty templates ($1k) | Terms reviewed |
| m2–m3 | Jan–Feb-2027 | Contract build-out, 60 h ($7.5k); library v0.1 in CI; hosted generator beta | ≥6 macros (8/16/32 KB sky130; 2/4/8 KB GF180) DRC/LVS-clean in CI |
| **m4** | Mar-2027 | **First invoices.** wafer.space GF180 half slot with test macros ($3.75k) | ≥2 paying accounts (model: first revenue $4.5k) |
| m5–m6 | Apr–May-2027 | NSF Project Pitch with a university PI; inbound from the previews | ≥2.5 accounts and ≥$15k cumulative revenue (model); PI letter |
| m7 | Jun-2027 | ChipFoundry sky130 slot with 8–32 KB test macros ($15k) | Pay only if cash is ≥$30k beforehand (model: $32.0k at m6, $20.4k after) |
| m8 | Jul-2027 | Three cash-positive months begin | Net cash flow ≥0 for 3 months |
| m9 | Aug-2027 | Test bench ($4k); STTR Phase I submitted | Submitted by 2027-08-31 |
| m10 | Sep-2027 | GF180 silicon characterized ($5k); first GF180 licence | ≥2 of 3 sizes working on ≥80% of tested die; access time ≤1.5× simulated |
| **m12** | Nov-2027 | One-year review | ARR ≥$40k (model $40.7k); run-rate ≥$128k; ≥7 accounts |
| m13 | Dec-2027 | sky130 silicon characterized ($5k); sky130 licences open | The 16 KB-plus macro passes the m10 test |
| m14 | Jan-2028 | The glut scenario starts | ≥1.5 new accounts/month (model `new` field: BASE 1.55, GLUT 1.45) |
| m15 | Feb-2028 | STTR Phase I decision ($305k) | Award, or drop C-32 at m19 |
| m16 | Mar-2028 | wafer.space GF180 full slot with 8–32 KB production macros ($7.25k) | Second-spin yield ≥ first |
| **m18** | May-2028 | Full-time decision; Cadence ReRAM probe ($12k), only if Weebit terms allow product use | ≥12 accounts, ARR ≥$66k and GP ≥$11.85k/mo for 3 months → founder full-time at m20 |

Dollar amounts are the model's one-time spends. The gates are this author's [ESTIMATE], set near BASE values.

---

## 9. Team required

| Role | When | Cost | Where to find |
|---|---|---|---|
| **Founder (CEO):** automation, CI, portal, sales, grant administration | m0 onward; 15 h/week until m20 | $0, then $10k/mo (A-03) | — |
| **Contract memory/VLSI engineer:** macro review, timing sign-off, integration | m0 (16 h), m2–m3 (60 h), then 12–30 h per job | $125/h [ESTIMATE]; $22.5k of one-time build-out and characterization over 24 months, plus service COGS (model) | Open Circuit Design LLC; OpenRAM contributors and UCSC VLSIDA alumni; Chips4Makers; the FOSSi (ORConf, Latch-Up) and Tiny Tapeout communities; retired SRAM designers on the East Coast |
| **Characterization contractor** with bench access | m10, m13, m24 | $5k each + $4k bench (model) | University labs (Brown; NEMC/NORDTECH members through PROPEL) |
| **University STTR PI** | Writing m5–m9; award m15 | ≥30% of the award [UNVERIFIED] | UCSC VLSIDA, Stanford OpenGCRAM, Brown Saligane lab |
| Bookkeeper and attorney (licence, warranty, export screening) | m1 onward | $350/mo inside $600/mo fixed opex (model) | Local small-business firms |
| **FTO patent counsel** | Before any C-32 spend | [ESTIMATE] ~$10–20k, not in the model; paid from STTR or seed | Semiconductor patent boutiques |
| **Full-time circuit cofounder** (T2) | m30, after a seed | $220k/yr loaded (model §9) | Gain-cell PhDs (Bar-Ilan/EPFL lineage, Stanford), Mobile Semiconductor alumni |
| Mixed-signal IC designer + test engineer (C-22) | m36+ | ~$0.6–1M over 2–3 years (C-22 card) | Packaging and test at the U.S. OSATs Integra and Promex |

**The single point of failure** is the contract memory engineer. The best candidate (OCD) is also the likeliest free competitor.

---

## 10. The cheapest experiment that could kill it

**Hypothesis to kill:** "Funded open-PDK teams will pay for larger, characterized macros, and no one in the channel will give them away within a year."

**Budget and timing:** about $5.1k over 30 days, 2026-11-02 to 2026-12-01, before the academic winter break. About $3k of it is already in the model (the m1 templates and the m2 contractor). The roughly $2.1k that is new lowers the cash low point from $20.4k to about $18.3k [ESTIMATE: arithmetic].

**Steps**
1. **Days 1–7 ($2.3k): build the previews.**
   - Run OpenRAM in the cloud for DRC/LVS-clean 8/16/32 KB sky130 and 2/4/8 KB GF180 macros with simulated Liberty files ($0.3k).
   - Have a contract memory designer spend 16 h ($2k) checking timing margins on the macros of 16 KB and up. *This tests whether OpenRAM can make large macros at all.*
2. **Days 3–7 ($1.2k): put up the offer.** A landing page with real prices, LEF/datasheet previews and Stripe **$500 refundable deposits** to "reserve a characterized macro for the next ChipFoundry/wafer.space deadline" ($0.2k), plus a licence and terms template ($1k).
3. **Days 3–25 ($0.1k): contact about 120 named people.**
   - All public wafer.space Run 1/2 project owners (about 70);
   - Tiny Tapeout SoC builders;
   - U.S. GF-pilot instructors;
   - about 20 SBIR performers on SkyWater;
   - the NORDTECH and NEMC managers;
   - MOSIS 2.0.
4. **Days 7–20 ($0): five written channel questions.**
   - **ChipFoundry:** marketplace terms? Any plan for free large macros?
   - **Cadence:** next SKY130/ReRAM run? Would they bundle?
   - **UCSC VLSIDA:** large-macro roadmap? Would they be STTR PI?
   - **OCD:** roadmap? Available to contract?
   - **Weebit:** fabless evaluation terms? Can MPW die be sold in a product?
5. **Days 20–30 (≤$1.5k): one hub or community event.** Convert deposits into LOIs.

**Pass/fail, decided now**

PASS (continue) only if **all four** hold:
- **(i) Paid demand:** at least 3 paid $500 deposits against orders of $2k or more each, **or** at least $15k in signed LOIs.
- **(ii) A serious buyer:** at least one commercial or SBIR buyer commits at $10k or more.
- **(iii) Buildable:** the reviewer confirms timing-clean sky130 macros of 16 KB or more are reachable in 200 h or less.
- **(iv) No free release coming:** no channel owner confirms free silicon-characterized macros of 16 KB or more within 12 months.

**KILL** if (i), (iii) or (iv) fails. **PIVOT** to an academic-only side line, with no full-time goal, if only (ii) fails.

---

## 11. Explicit kill criteria

"Model" means the BASE value in `models/open-memory-ip.py`.

1. **2026-12-01 (day 30).** The experiment fails (i), (iii) or (iv) → **kill DD5.**
2. **2027-05-31 (m6).** Fewer than 2 paying accounts, or less than $8k invoiced in total (model: 2.5 and $15.9k) → **kill.**
3. **2027-10-31 (m11).** On GF180 silicon, fewer than 2 of 3 macro sizes work on ≥80% of die, or access time is more than 1.5× simulated → **stop selling characterized licences.** Kill if operating cash cannot fund a re-spin.
4. **2027-11-30 (m12).** ARR below $20k, or run-rate below $64k (about half of the model's $40.7k / $127.9k) → **kill**; it becomes a hobby.
5. **2028-01-31 (m14).** The sky130 macro of 16 KB or more fails test #3 → **kill the sky130 line.** That is the only line with SBIR and DoD buyers.
6. **Any date.** ChipFoundry, Cadence, UCSC VLSIDA, OCD or Chips4Makers releases free silicon-characterized macros of 16 KB or more for the same shuttle → **stop all one-time spend within 30 days.** The founder never goes full-time (model: ARR at m36 $50.0k). Harvest, or sell the contracts to the releaser.
7. **2028-05-31 (m18).** Fewer than 9 paying accounts, or trailing-3-month GP below $8k/mo (model: 12.7 accounts and $12.2k; full-time needs about 18 and $11.85k) → **the founder does not quit**, and DD5 stays a side line permanently.
8. **2027-08-31 (m9).** No STTR proposal submitted with a signed university PI → **drop C-32.**
9. **2028-06-30 (m19).** No STTR Phase I award → **drop C-32.**
10. **Before any C-32 spend beyond the STTR.** The FTO read flags a blocking claim, or the sky130 gain-cell macro measures below 1.2× density against the 1.896 µm² 6T cell → **kill C-32.**
11. **2028-05-31 (m18), before the $12k probe.** Any one of these → **kill C-22:**
    - Weebit asks more than $100k for a fabless evaluation;
    - MPW die cannot go into a paid product;
    - no defense or security buyer signs a paid-evaluation LOI of $25k or more [ESTIMATE threshold].
12. **2029-05-31 (m30).** Run-rate below $250k → **no seed, and T2 is permanently off.**

---

## 12. Cycle test: the 2028–29 glut (DDR5 −60%) and the severe case

**How the DRAM price reaches this business.** Macros are priced per design, so DRAM prices matter only through commercial design-start budgets:
- One-third of the DDR5 drop passes through to commercial demand.
- 0.15 of it passes to commercial price, and 0.5 to commercial churn.
- Academic demand is held flat [ESTIMATE; `research/assumptions/p4-open-memory-ip.md`].
- The glut starts at m14, after the cash trough, so the cash low point stays $20.4k in every case.

| | BASE (−10%) | GLUT (−60%, DDR5 $8.15/GB) | SEVERE (−90%, $2.04/GB) |
|---|---|---|---|
| Commercial demand / price / churn | ×0.97 / ×0.98 / ×1.05 | ×0.80 / ×0.91 / ×1.30 | ×0.70 / ×0.87 / ×1.45 |
| ARR m36 | $157.6k | $125.8k (−20%) | $105.7k (−33%) |
| Run-rate m36 | $423.9k | $342.1k (−19%) | $291.2k (−31%) |
| 36-month revenue | $713.9k | $582.2k (−18%) | $506.6k (−29%) |
| Founder full-time | m20 (Jul-2028) | m25 (Dec-2028) | m30 (May-2029) |
| Commercial accounts at m36 | 12 | 10 | 8 |
| sky130 SRAM $/GB vs DDR5 | 73× | 163× | 653× |

(Model §1, §4 and §6. The percentages are computed from those values.)

**What actually hurts is a glut combined with something else:**
- **GLUT plus a free-bundle shock:** ARR at m36 is $39.1k, and the founder is never paid.
- **SEVERE with all inputs 30% adverse:** cash bottoms at **−$14.7k**, which needs about $15k more than the founder has.

**T2 in a glut:**
- **Gain-cell IP is priced in die area.** But trailing-node royalties track wafer prices: eMemory's 8-inch royalties fell 15.9% year on year ([Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/ememory-technology-inc-roco-3529-030030531.html)) [REPORTED].
- **Defense secure-NVM demand (C-22) is decoupled** from DRAM prices.
- **A seed round is harder to raise in a downturn** [ESTIMATE].

**Verdict: it survives the glut but not "free".** The DRAM cycle moves the founder's full-time date by 5–10 months. One free release by a channel owner ends the venture case.

---

## 13. Sources

All URLs below are logged in `research/sources/p4-open-memory-ip.jsonl` or other `research/sources/*.jsonl` files, with cross-references in `p4w-open-memory-ip.jsonl`.

**Market, shuttles and channels**
- https://github.com/TinyTapeout/tinytapeout-sky-26a
- https://github.com/TinyTapeout/tinytapeout-sky-26b
- https://github.com/TinyTapeout/tinytapeout-ihp-26a
- https://github.com/TinyTapeout/tinytapeout-gf-0p2
- https://github.com/wafer-space/ws-run1
- https://github.com/wafer-space/ws-run2
- https://www.crowdsupply.com/wafer-space/gf180mcu-run-2
- https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/
- https://business.minstercommunitypost.com/minstercommunitypost/article/gnwcq-2025-9-3-chipfoundry-acquires-efabless-assets-to-propel-custom-silicon-innovation
- https://github.com/chipfoundry/caravel_user_project
- https://www.skywatertechnology.com/lowering-barriers-to-silicon-cadence-launches-mpw-aggregation-service-for-sky130/
- https://opensource.googleblog.com/2023/11/open-source-pdks-joining-linux-foundation-chips-alliance.html?m=0
- https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms?asPDF=1
- https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/
- https://allaboutcircuits.com/news/mosis-partners-with-globalfoundries-extending-40-year-prototyping-legacy
- https://nstxl.org/microelectronics-commons-delivering-results-2026/
- https://research-and-innovation.cornell.edu/?p=6460
- https://masstech.org/news/northeast-microelectronics-coalition-hub-celebrates-3725-million-federal-funding-power
- https://www.nsf.gov/funding/opportunities/chip-design-hub-enabling-access-semiconductor-chip-ecosystem-design

**Memory IP, macros and competitors**
- https://github.com/VLSIDA/OpenRAM
- https://github.com/VLSIDA/sky130_sram_macros
- https://github.com/efabless/sky130_sram_macros
- https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram
- https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram
- https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram
- https://gitlab.com/Chips4Makers/arrakeen-sram-testchip
- https://github.com/AUCOHL/DFFRAM
- https://www.silicon.co.uk/press-release/skywater-technology-expands-leadership-in-u-s-semiconductor-manufacturing-with-infineon-ip-license-agreement
- https://www.design-reuse.com/news/9192/analysis-arm-artisan-merger-defining-moment.html
- https://www.silicon.co.uk/press-release/cadence-to-acquire-arm-artisan-foundation-ip-business
- https://www.designworldonline.com/synopsys-enters-embedded-memory-market/
- https://www.skywatertechnology.com/skywater-announces-availability-of-sram-memory-compiler-for-90-nm-strategic-rad-hard-by-process-offering/
- https://us.design-reuse.com/news/45774/mobile-semiconductor-180nm-memory-compilers-sandia-national-laboratories.html
- https://finance.yahoo.com/markets/stocks/articles/ememory-technology-inc-roco-3529-030030531.html

**Gain cell (C-32)**
- https://arxiv.org/html/2507.10849v1
- https://arxiv.org/abs/2602.21278v1
- https://cris.biu.ac.il/en/publications/4t-gain-cell-providing-unlimited-availability-through-hidden-refr/
- https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/
- https://anysilicon.com/news/raaam-memory-technologies-raises-17-5-million-in-oversubscribed-series-a-led-by-nxp-semiconductors/
- https://anysilicon.com/news/raaam-selects-avnet-asic-as-its-vca-partner-for-tsmcs-2nm-gcram-development-and-qualification/
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11127455

**ReRAM, SkyWater and C-22 incumbents**
- https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/
- https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf
- https://ionq.com/news/ionq-completes-acquisition-of-skywater-technology
- https://www.businesswire.com/news/home/20260125927336/en/IonQ-to-Acquire-SkyWater-Technology-Creating-the-Only-Vertically-Integrated-Full-Stack-Quantum-Platform-Company
- https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services

**Funding and regulation**
- https://seedfund.nsf.gov/topics/semiconductors/
- https://grantedai.com/grants/semiconductors-s-sbir-sttr-program-national-science-foundation-nsf-small-bu-ef99bad7
- https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and
- https://grants.nih.gov/grants/policy/nihgps/html5/section_18/18.5_small_business_innovation_research_and_small_business_technology_transfer_programs.htm
- https://www.iedconline.org/news/2026/04/15/federal-policy-updates/federal-policy-update-sbir-and-sttr-reauthorized/
- https://www.wiley.law/alert-SBIR-STTR-Reauthorization-Brings-New-Opportunities-and-Obligations-to-Consider
- https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments

**Internal sources:**
- `models/open-memory-ip.py` and `models/dram_cost_stack.py`
- `research/phase4/open-memory-ip_notes.md`
- `research/phase2/concepts_master.json` (C-33, C-32, C-22)
- `research/phase3/selection.json` and `research/phase3/scores_raw/*.json`
- `scores.csv`, `03_SCORING.md` §7.5, `01_LANDSCAPE.md` §4.4, §7, §8 and §9
- `ASSUMPTIONS.md` A-03, A-04 and A-05
