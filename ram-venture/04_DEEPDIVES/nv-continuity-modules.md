# DD3: Drop-in Non-Volatile Continuity Modules

**Slug:** `nv-continuity-modules` · **As of:** 2026-11-01 · **Author agent:** `p4w-nv-continuity-modules`
**Inputs:** `models/nv-continuity-modules.py` (re-run 2026-11-01, exit 0; output identical to `research/phase4/nv-continuity-modules_model_output.md`) · `research/phase4/nv-continuity-modules_notes.md` · `research/phase2/concepts_master.json` (C-12, C-16) · `research/phase3/scores_raw/*.json` · `scores.csv` · `01_LANDSCAPE.md`
**Evidence grade.** Every external fact comes from a search-result snippet (the research agent's fetches failed DNS), so nothing is `[VERIFIED]`. `[REPORTED-P]` = primary page seen via snippet. Model outputs are `[ESTIMATE]` and cite e.g. `model §[5]`.

---

## 0. Header

**Pitch.** Battery-free drop-in replacements for the battery-backed memory in legacy CNC, PLC, robot and instrument controls. The product is PC Card "SRAM" cards built on U.S.-fabbed Everspin Toggle MRAM, plus DIP NVSRAM modules built on Infineon F-RAM. Each is validated on the real controls and assembled at a U.S. contract manufacturer.

| Field | Value |
|---|---|
| **Anchor** | **C-12** Battery-free NV-cache / NVSRAM-replacement modules (T0) |
| **Folded in** | **C-16** Supercap-Killer MRAM PLP kit (T1), carried as a deferred option |
| **Why folded** | Same competence (boards plus validation) and the same lifecycle axis: "F-RAM replaces battery-backed SRAM, and MRAM replaces PLP supercaps" (`03_SCORING.md` §7.3). The scorers kept C-16 small. Founder: "worth a cheap test, not the core of a venture." VC: "Real mechanism in the wrong slot of the value chain." The veteran's C-12 warning, "watch the F-RAM /CE-latch timing trap", is why the card uses Toggle MRAM (§1). |
| **Capital tier** | **T0.** Peak cash need is $29.2k of the $40k deployable: start cash minus the $10.8k low at month 6 (model §[5]; A-03). C-16 would be low T1 (~$50k option) and is deferred. |
| **TRL** | 9. Everspin MR4A16B Toggle MRAM ships ([DigiKey, 2026](https://www.digikey.com/en/products/detail/everspin-technologies-inc/MR4A16BYS35/4021237)) and Infineon FM18W08 F-RAM ships ([DigiKey, 2026](https://azcus.digikey.com/en/products/detail/infineon-technologies/FM18W08-SG/4090358)) [REPORTED-P]. Only the adapter is new. |
| **"Better than RAM" axis** | **Non-volatility and lifecycle, not $/GB.** At $42 per 2MB chip, MRAM costs **$21,504/GB**, about 1,056× the $20.37/GB DDR5 contract price (model §[1]; `models/dram_cost_stack.py`). It wins only where the alternative is a lithium-backed SRAM card or a sealed Dallas NVSRAM whose cell eventually dies and takes the machine's parameters with it. |

**Scores (`scores.csv`):**

| ID | Default | Capital-constrained | Moonshot | tech / capital / ttr / usmfg / margin / moat / comp / reg / cycle / founder |
|---|---|---|---|---|
| C-12 | **80.0 (#2)** | **82.5 (#2)** | **75.0 (#6)** | 5 / 5 / 4 / 3 / 3 / 2 / 3 / 5 / 5 / 4 |
| C-16 | 66.0 (#19) | 67.5 (#18) | 63.3 (#18) | 5 / 4 / 2 / 3 / 3 / 2 / 3 / 3 / 3 / 3 |

The #2 rank comes from a rubric with no market-size criterion (`03_SCORING.md` §6, blind spot #1, which uses C-12 as its example). All three scorers called it a side business. Founder: "a profitable side business, not a venture." VC: "good cash, not a company anyone should raise for."

### Three verdicts

| Question | Verdict | One line |
|---|---|---|
| **POSSIBLE?** | **YES** | The parts are TRL 9 and the adapter is simple logic. The one unproven step is whether Fanuc and Mitsubishi controls accept an MRAM card, and the kill experiment tests that in weeks 2–4. |
| **PROFITABLE?** | **MARGINAL** | The card's unit economics are good: 57–61% gross margin and 44–46% contribution, with breakeven in month 11. The business is not. Run-rate is **$196k/yr at month 36**, and a quarter of that comes from two defense contracts nobody has found yet. It **never pays the founder a salary** in BASE, GLUT or SEVERE; only the S4 stretch path does, from m22. The 36-month cumulative net of $79k works out to about **$34 per part-time hour**. Global demand is about **$3M/yr and shrinking**. |
| **DOABLE BY THIS FOUNDER?** | **YES** | It is T0 and runs without firmware: one ~$9k contract EE, a U.S. contract manufacturer, a web store and a compatibility database. That fits a software builder whose day job is in product development and operations. The one hard dependency is bench access to legacy controls. |

**Portfolio role.** This is a FALLBACK or bridge-revenue line, not the PRIMARY pick. It is cheap, fast, glut-proof and founder-doable, and its ceiling is set by a declining installed base.

---

## 1. How it works (for a smart non-engineer)

A 1990s Fanuc CNC lathe (Series 0, 16, 18, 20 or 21) knows how to cut accurately because of thousands of stored numbers: tool offsets, axis parameters, error compensation, the ladder program. They sit in memory that forgets everything without power, so a small battery keeps it alive. If that battery dies during a shutdown, the settings are gone, and getting the machine back can take days of a service engineer's time.

The usual insurance is a backup card: a credit-card-sized **PC Card (PCMCIA) "SRAM card"** that the technician plugs in and copies everything onto. That card keeps its own data alive with a **lithium battery inside it**. Three problems follow:
- **It fails silently.** Mitsubishi warns that an SRAM card without its battery "may not raise a battery error" and loses its data at power-off ([Mitsubishi, T30-0007](https://mitsubishielectric.co.jp/fa/document/technews/plc/t30-0007/t300007.pdf)) [REPORTED-P].
- **The cheap substitute is refused.** Older Fanuc controls reject CompactFlash in an adapter ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-2021-parameter-backup-via-pcmcia-sram-card)) [REPORTED].
- **New cards are scarce.** A reseller calls them "hard to get" ([Memex](https://memex.ca/?p=596)) [REPORTED].

**The product replaces the battery and SRAM with memory that remembers without power.**

```
   Legacy control's PC Card slot (68 pins, 5 V signals)
              |
   +----------v-------------------------------------------------+
   | 5V-tolerant buffers (3x 74LVC16245-class)   5 V <-> 3.3 V  |
   | small ID memory (attribute EEPROM)          "I am an SRAM  |
   |                                              card, 2 MB"   |
   | battery-status pins (BVD1/BVD2) wired to "battery good"    |
   | Everspin MR4A16B 16Mb Toggle MRAM  (2 MB; x2 for 4 MB)     |
   |   - reads/writes like SRAM, 35 ns, no wear-out             |
   |   - keeps data with zero power: no battery at all          |
   +------------------------------------------------------------+
   Old card: same slot, plain SRAM + lithium cell (lasts years, fails silently)
```

**Why MRAM, not the cheaper F-RAM named in the original concept card.**
- **Timing.** The veteran scorer warned that FM18W08-class F-RAM latches the address on /CE falling, "which breaks sockets that hold /CE low" (`scores_raw/veteran_1.json`). Toggle MRAM behaves like true SRAM.
- **Density.** One chip makes a 2MB card.
- **Origin.** It is fabbed in Chandler, Arizona ([Everspin 10-K](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm)) [REPORTED-P].
- **Litigation.** It is outside the Avalanche ITC case, which targets Everspin's STT-MRAM ([Avalanche, 2026-02](https://www.avalanche-technology.com/itc-institutes-investigation-into-everspin-technology-based-on-avalanche-claims-of-patent-infringement/)) [REPORTED].
- **The cost:** a 3.3V chip on a 5V bus needs buffers, inside a ~$5 buffer/supervisor/ID-memory logic line (model §[9]).

**Second product: DIP modules.** Old instruments, controllers and arcade boards use Dallas DS1225/DS1230/DS1245 chips with a lithium cell sealed inside. A small board carrying Infineon FM18W08 F-RAM (5V-capable, $12.87) plugs into the same socket and needs no battery. Free open designs exist ([PCBWay](https://www.pcbway.com/project/shareproject/Dallas_DS1230Y_DS1235YW_NVRAM_FRAM_Replacement_Adapter_79f70ace.html)) [REPORTED]; ours adds testing, a certificate of conformance and a warranty.

**Who builds what.** A contract EE designs the boards and a U.S. EMS assembles them. The founder builds the store, the compatibility database (which control, firmware and card combinations are proven) and an optional cloud vault for backup files. There is no firmware and no chip design.

**The folded option (C-16)** applies the same idea inside SSDs: an MRAM journal replaces the DRAM cache and its hold-up supercapacitors, as in IBM's FlashCore Modules ([Blocks & Files, 2026-10-05](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966)) [REPORTED]. §2 explains why we do not build it.

---

## 2. Cost and unit-economics model

All numbers come from `models/nv-continuity-modules.py` unless another source is cited. The model has a 36-month horizon, month 1 = 2026-11, $40k start cash, and a part-time founder with no salary until trailing operating profit reaches at least $12k/month.

### 2.1 Unit economics (BASE; model §[1])

Net revenue is blended across channels: 25% eBay, 35% own store and 40% resellers at a 30% discount for cards; 40/40/20 for DIPs.

| SKU | List | Net rev/unit | COGS | GM | Fees+CAC+ship+warranty | Contribution | Contrib. % |
|---|---|---|---|---|---|---|---|
| NV-CARD 2MB (1× MR4A16B) | $249 | $219.12 | $85.50 | 61% | $33.67 | **$99.95** | 46% |
| NV-CARD 4MB (2× MR4A16B) | $349 | $307.12 | $131.50 | 57% | $40.73 | **$134.89** | 44% |
| NV-DIP 256Kb (FM18W08), DS1225/1230 | $34 | $32.64 | $23.00 | 30% | $9.90 | **−$0.26** | −1% |
| NV-DIP 1Mb (FM28V100), DS1245 | $59 | $56.64 | $35.00 | 38% | $12.27 | $9.37 | 17% |

**2MB COGS stack ($85.50):**
- MRAM $42.00 (49%), at our 100–500/yr volume, between $37.67 @1k ([Future](https://www.futureelectronics.com/p/memory--RAM--nvram/mr4a16bcys35r-everspin-technologies-6114651)) and $46.03 qty 1 ([DigiKey](https://www.digikey.com/en/products/detail/everspin-technologies-inc/MR4A16BYS35/4021237)) [REPORTED-P]
- Frame kit and connector $12 `[ESTIMATE: no small-quantity price found]`
- PCB $4.50 and buffer/ID logic $5 `[ESTIMATE]`
- U.S. EMS assembly $14, setup amortization $4, and test/pack/CoC $4 `[ESTIMATE: 10-board turnkey anecdote $415–1,300]` ([SparkFun forum](https://community.sparkfun.com/t/pcb-assembly-service/27265))

**Blended contribution** is **$109 per card** and **$3 per DIP** (model §[8]). **The DIP line does not make money**; it is a traffic line, to drop if it eats founder time.

### 2.2 Revenue, run-rate and recurring ARR (model §[5])

| Scenario | Run-rate m12 (2027-10) | m18 (2028-04) | m24 (2028-10) | m36 (2029-10) | Recurring ARR m12 / m18 / m24 / m36 |
|---|---|---|---|---|---|
| BASE | $62.5k | $121.7k | $143.6k | **$195.8k** | $0 / $1.4k / $4.0k / **$56.2k** |
| GLUT | $59.4k | $115.6k | $136.4k | $186.0k | $0 / $1.3k / $3.8k / $53.4k |
| SEVERE | $47.8k | $93.1k | $109.9k | $153.9k | $0 / $1.1k / $3.0k / $47.1k |

"Run-rate" is that month's revenue × 12, from repeat hardware purchases with no contract behind them. "Recurring ARR" is cloud-vault MRR plus LTSA monthly × 12.

**Read the recurring line honestly.** $48k of the $56.2k comes from two assumed $24k/yr DMSMS blanket orders (from m27 and m33), and **no DLA demand for DS12xx-class parts was found** (notes §4). **Without them, m36 run-rate is $147.8k and recurring ARR $8.2k** (model §[6]). At m36, revenue is 59% cards, 12% DIPs, 25% LTSA and 4% cloud [ESTIMATE: model `simulate('BASE')` at month 36].

### 2.3 Breakeven, cash low point and 36-month totals (model §[4b], §[5])

| Scenario | Breakeven month | Cash low | Cash m18 | Cash m36 | 36-mo revenue | 36-mo net | Founder full-time |
|---|---|---|---|---|---|---|---|
| BASE | **11 (2027-09)** | **$10.8k (m6, 2027-04)** | $18.8k | $103.5k | $310.9k | **$79.1k** | **never** |
| GLUT | 11 | $11.6k (m6) | $20.7k | $104.9k | $295.3k | $79.0k | never |
| SEVERE | 12 | $12.2k (m7) | $16.7k | $77.4k | $240.2k | $49.3k | never |

**First revenue** comes in month 4 (2027-02) from DIPs. **First card revenue** comes in month 9 (2027-07), after design, validation and the 20–26-week MRAM lead time.

**Net by year in BASE:** −$17.8k, then +$34.3k, then +$62.6k [ESTIMATE: model `simulate` summed by year]. At ~15 hours a week (A-03), the 36-month net is about **$34/hour**. Year 3 alone is about $80/hour. That is decent moonlighting income, not a company.

### 2.4 Sensitivity (BASE, one variable at a time; model §[6])

| Case | Breakeven | Cash low | Run-rate m18 | Run-rate m36 | Rec. ARR m36 | 36-mo net |
|---|---|---|---|---|---|---|
| Baseline | 11 | $10.8k | $121.7k | $195.8k | $56.2k | $79.1k |
| **Price −30%** | **17** | **$577** | $85.2k | $151.5k | $53.7k | **$1.2k** |
| Price +30% | 9 | $11.2k | $158.2k | $240.2k | $58.6k | $157.1k |
| Conversion −30% | 12 | $11.3k | $85.2k | $137.1k | $39.3k | $42.3k |
| Conversion +30% | 10 | $10.2k | $158.2k | $254.6k | $73.0k | $116.0k |
| COGS +30% | 13 | $3.7k | $121.7k | $195.8k | $56.2k | $41.4k |
| COGS −30% | 10 | $14.7k | $121.7k | $195.8k | $56.2k | $116.9k |
| No LTSA/DMSMS contract | 11 | $10.8k | $121.7k | $147.8k | $8.2k | $65.1k |
| Card launch +6 months | 17 | $6.0k | $62.9k | $194.4k | $54.8k | $52.5k |
| Churn ±30% | 11 | $10.8k | $121.7k | ~$196k | $55.6–56.8k | $78.8–79.5k |

**Price is the variable that decides this business.** A 30% price cut, which a Shenzhen copy or a buyer anchored on "$200 on eBay" could force, wipes out all 36-month profit.

### 2.5 Market ceiling and scale paths (model §[3], §[6b])

**TAM chain** [ESTIMATE on one REPORTED anchor]:
- 5M cumulative Fanuc CNCs ([Metalworking News, 2022](https://metalworkingnews.info/fanuc-reaches-cnc-production-milestone-of-5-million/))
- × 15% in the U.S. × 35% on SRAM-card-era controls × 50% still running = **131k U.S. legacy machines**
- ÷ 8 machines per shop = **16.4k shops**
- One card per shop every 8 years, × 1.5 for other families = **3,076 cards/yr in the U.S. and 12,305/yr globally**
- At $241/card: **$0.74M/yr U.S. and $2.97M/yr global**

**BASE assumes** 40 cards/month at steady state: **4% of global and 16% of U.S. demand**, which is not conservative for a new entrant. It also holds demand flat, although the installed base shrinks and **every battery-free card sold removes a future replacement.**

| Path | Run-rate m36 | Rec. ARR m36 | 36-mo net | Full-time month | Share of global card demand |
|---|---|---|---|---|---|
| S0 BASE | $195.8k | $56.2k | $79.1k | never | 4% |
| S1 + white-label in 3–4 MRO catalogs | $293.2k | $57.5k | $163.4k | never | 8% |
| S2 + 4 DMSMS/OEM LTSAs | $291.8k | $152.2k | $110.1k | never | 4% |
| S3 + adjacent form factors | $257.8k | $60.3k | $131.7k | never | 6% |
| **S4 stretch (all, cards ×3)** | **$521.3k** | $179.8k | $158.1k | **m22** | **12%** |

### 2.6 What must be true (model §[8], plus judgment)

1. **Part-time breakeven:** 8 cards/month cover the $900/month of fixed opex. BASE sells 33 cards/month at m18.
2. **A founder salary** ($120k/yr) needs **100 cards/month, 10% of global demand**. **$0.5M/yr from cards alone** needs 173/month: 17% of global and 67% of U.S. demand.
3. **By m18:** 733 cumulative units (183 cards and 550 DIPs), and **at least 3 active reseller accounts by m12**.
4. **Controls accept the card.** Fanuc 16i/18i/21i or 0i-A, and Mitsubishi Q, read, write, format and restore on an MRAM card with no battery alarm. *Untested.*
5. **Buyers pay ~$249** for battery-free when used battery cards sell for $160–440 ([eBay listings, 2026](https://www.ebay.de/itm/306136207868)) [REPORTED].
6. **Supply holds.** MR4A16B lead time stays at or under 26 weeks, and frame kits cost ≤$20 at MOQ ≤1,000. Both are unconfirmed (notes §2).

### 2.7 C-16 PLP kit option (model §[7])

The kit would replace 2GB of DRAM plus $12 of supercaps with 512MB of STT-MRAM costing $410 ([LCSC, 2026](https://www.lcsc.com/product-image/C20342497.html)).

| Scenario | DRAM $/GB | MRAM premium/board | p(paid design-in by m36) | Option EV (cost $50k) |
|---|---|---|---|---|
| BASE | $18.33 | $362 | 0.32 | **−$44.8k** |
| GLUT | $8.15 | $382 | 0.19 | −$47.0k |
| SEVERE | $2.04 | $394 | 0.11 | −$48.3k |

Breaking even takes 3.1 paid design-ins at $40k each and 40% GM. **Verdict: defer.** The only C-16 work is a $0 email interest test (§10).

---

## 3. Target customer and the first ten customers

**The buyer is a maintenance technician or maintenance manager, or the MRO reseller who serves them.** They buy a card per shop or per technician, not per machine. They search by part number ("Q2MEM-2MBS", "fanuc sram card") and buy from MRO catalogs or eBay.

| # | Customer | Why they buy | How to reach them |
|---|---|---|---|
| 1 | **Memex Inc.** (Ontario), Fanuc-card reseller | Lists most PCMCIA capacities as unavailable: "hard to get" ([Memex](https://memex.ca/?p=596)) | Sales inbox; offer a white-label or wholesale card at $175, MOQ 10 |
| 2 | **MRO Electric**, Fanuc repair and exchange | Already sells the Fanuc A20B-2900-0531 SRAM module with a 2-year warranty ([MRO Electric](https://www.mroelectric.com/product/A20B-2900-0531)); a card adds to that line | Product-page RFQ form, then a call; also ask for bench time on their controls |
| 3 | **Do Supply**, MRO surplus reseller | Lists a Fanuc 2MB SRAM card ([Do Supply](https://www.dosupply.com/automation/fanuc/other/DISKMF32M1LCDA7)) and the Mitsubishi Q2MEM-2MBS ([Do Supply](https://www.dosupply.com/automation/mitsubishi/melsec-q/Q2MEM-2MBS)) | Vendor onboarding |
| 4 | **Radwell International** (Willingboro NJ), East Coast obsolete-automation giant [UNVERIFIED for this product] | Catalogs obsolete automation parts | Vendor program; a short drive from an East Coast founder |
| 5 | **U.S. job shops on Fanuc 0/16/18/20/21 or i-A controls** (>20,000 U.S. job shops ([MMS/Gardner](https://www.mmsonline.com/blog/post/capital-spending-survey-projects-5-decline-in-machine-tool-buying-for-2020-but-spending-level-still-above-average))) | Parameter loss when a battery dies; the CF workaround is rejected | Part-number search ads; CNCzone and Practical Machinist threads ([CNCzone](https://www.cnczone.com/forums/fanuc/421202-fanuc-16ia-sram-memory-card-backup.html)) |
| 6 | **Fanuc robot maintenance teams (RJ-2/RJ-3)** at Tier-2 auto and metal-fab plants | Backups need a compatible SRAM card, and not every card works ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-rj-2-pcmcia-sram-memory-card-compatibility-guide)) | Robot integrators; a validated-robot line in the compatibility DB |
| 7 | **MELSEC-Q plant maintenance** (Q2MEM-1MBS/2MBS users) | The originals were discontinued in 2018 ([Mitsubishi FA-A-0267](https://mitsubishielectric.com/fa/document/technews/plc/fa-a-0267/faa0267a.pdf)); the replacements still need batteries and lose data silently | eBay Q2MEM buyers; Mitsubishi system integrators |
| 8 | **Independent calibration and repair labs** (HP/Agilent 3458A DS1230) | Open FRAM adapters exist ([OSH Park](https://oshpark.com/shared_projects/GCTJUxu1)), but labs need tested parts with a CoC | xDevs and EEVblog communities; direct email to cal labs |
| 9 | **Federal and defense buyers through CDW-G-type resellers** | CDW-G sells Synchrotech battery SRAM cards at $239.39 and screens for TAA ([CDW-G](https://www.cdwg.com/product/synchrotech-sram-pcmcia-memory-pc-cards-replaceable-battery-flash-memory/5006798); [CDW](https://www.cdw.com/product/synchrotech-srx-series-flash-memory-card-4-mb-pc-card-taa-compliant/9204293)) | Reseller vendor onboarding after month 13 |
| 10 | **DLA Land & Maritime and depot DMSMS engineers** | Obsolete NVSRAM in legacy boards; 5962 memory bought by NSN ([HigherGov](https://www.highergov.com/nsn/5962012622185/)) | DIBBS ([DLA](https://www.dla.mil/Portals/104/Documents/SmallBusiness/DIBBS%20Solicitations%20-%20With%20Notes.pdf)); SAM/CAGE registration first. 12–24 months to an approved source [ESTIMATE: notes §4, typical form-fit-function engineering approval] |

**Low-value alternate:** arcade and retro restorers, price-capped by free adapters and the ~$30 Glitch Works drop-in ([Tindie](https://tindie.com/products/glitchwrks/glitch-works-gw-1225-1-dallas-ds1225-replacement)).

**C-16 interest targets (email only).** Swissbit, which sells PowerSafe ([EFY](https://www.electronicsforu.com/news/new-products/swissbit-introduces-powersafe-a-power-loss-protection-system-for-industrial-ssds)); Apacer, which sells CorePower ([SOS](https://www.soselectronic.com/en-us/articles/apacer/apacer-corepower-your-valuable-data-deserves-top-tier-protection-3065)); and Sage and Phison, which already pair controllers with Everspin 1Gb parts ([ECD](https://embeddedcomputing.com/technology/storage/sage-microelectronics-and-everspin-partner-to-bring-spin-transfer-torque-mram-to-next-generation-enterprise-ssd-devices); [eeNews](https://www.eenewseurope.com/en/phison-memory-controllers-to-support-1gbit-mram/)).

**Shared funnel:** DD2's C-29 was scored "lead-gen for C-12/C-80, not a company" (VC); its EOL search traffic can feed this store.

---

## 4. Go-to-market

**Channels** (model §[2]):

| Product | eBay | Own store | Resellers |
|---|---|---|---|
| Cards | 25% | 35% | 40% |
| DIPs | 40% | 40% | 20% |

Resellers matter because maintenance techs search MRO catalogs.

**Pricing:**
- **2MB card $249**, priced at parity with the new Synchrotech battery card ($239.39), not at a premium.
- **4MB card $349.**
- **DIPs $34 / $59**, against DS1230Y at $35–44 for qty 1 ([Findchips, 2026](https://findchips.com/search/DS1230Y-85?f=dsa)) [REPORTED].
- **Wholesale** is 30% off cards ($174.30) and 20% off DIPs.
- Free shipping on direct orders and a 2-year warranty, matching MRO Electric's module warranty.
- A Mitsubishi-format card could later test $299 against the $403.81 Q2MEM-2MBSN listing ([eBay, 2026](https://www.ebay.de/itm/406086802130)) [ESTIMATE]. +30% price moves breakeven to m9 (model §[6]).

**Sales motion.**
- **Inbound:** part-number search, plus how-to articles in the style of the IMD knowledgebase posts that already rank.
- **Reseller onboarding:** wholesale at $175, MOQ 10, and a public compatibility matrix as the sales tool.
- **Federal:** CDW-G/GSA resellers and DIBBS after month 13.

No field sales; the day job limits outbound to ~5 calls a week [ESTIMATE: A-03, ~15 h/week].

### First 90 days of selling

| Window | Actions | Targets |
|---|---|---|
| **Days 1–30 (2026-11)** | Run the kill experiment (§10). Landing page with a $25 refundable deposit; $600 of part-number ads; CNCzone and Practical Machinist posts; 20 calls and emails to resellers and repair shops | ≥15 deposits OR ≥2 reseller LOIs, and the bench pass |
| **Days 31–60 (2026-12)** | Turn LOIs into wholesale terms. Publish compatibility matrix v0 from the bench results. Draft the DIP listings. Place the first MRAM order for ~125 chips (100 cards at a 25% 4MB mix). Register SAM.gov/CAGE ($0) | 2 signed reseller agreements; MRAM PO confirmed |
| **Days 61–90 (2027-01)** | Second round of 10 calls to CNC repair shops and Mitsubishi integrators. Post 3458A and DS1245 content on xDevs/EEVblog. Pre-announce the DIP launch | ≥25 cumulative deposits; ≥3 LOIs or agreements |
| **Card launch +90 days (2027-07 to 09)** | Ship deposit holders first; then eBay listings; then reseller stock | Model: 3 / 7 / 10 cards in m9–11; monthly net ≥0 by m11 |

---

## 5. Competitors and why you would win

| Competitor | Product and position | Price | Threat |
|---|---|---|---|
| **Used battery cards on eBay** (Pretec, Epson, Panasonic, Melcard) | The default buyer choice | **$160–440** ([eBay](https://www.ebay.de/itm/306136207868)) [REPORTED] | **Highest.** Sets the price ceiling |
| **Synchrotech** (via CDW-G) | New 2MB SRAM PC Card, replaceable primary cell plus rechargeable cell; TAA compliant | **$239.39** ([CDW-G](https://www.cdwg.com/product/synchrotech-sram-pcmcia-memory-pc-cards-replaceable-battery-flash-memory/5006798)) | High in the federal channel |
| **Memex** | Fanuc SRAM cards with rechargeable lithium, ~1-yr retention; most capacities out of stock | Not shown ([Memex](https://memex.ca/?p=596)) | Medium; also customer #1 |
| **Fanuc OEM cards** | Genuine cards | "big $$$" per forum users ([CNCzone](https://www.cnczone.com/forums/fanuc/421202-fanuc-16ia-sram-memory-card-backup.html)) | Low on price, high on trust |
| **Mitsubishi Q2MEM-1MBSN/2MBSN** | Current OEM cards; battery required | "Same standard price" as originals ([Mitsubishi](https://mitsubishielectric.com/fa/document/technews/plc/fa-a-0267/faa0267a.pdf)); $403.81 on eBay | Medium |
| **Pretec / CSM industrial SRAM cards** | Dual-battery lines from the 2009 era | Not shown ([TweakTown/Pretec](https://www.tweaktown.com/pressrelease/1122/pretec_extends_dual_battery_sram_pc_card_to_16mb/index.html); [CSM](https://csi.pl/wp-content/uploads/2020/05/Karta-katalogowa-SuperStore-SRAM-blue.pdf)) | Low (legacy) |
| **DIP: ADI DS1230Y**, still in production; Rochester DS1230AB stock | Sealed-battery originals | $35–44 qty 1 ([Findchips](https://findchips.com/search/DS1230Y-85?f=dsa); [ADI](https://www.analog.com/ja/products/ds1230y); [Digipart](https://www.digipart.com/part/DS1230AB-85)) | High for DS1230 |
| **DIP: free open FM18W08 adapters; Glitch Works GW-1225-1** | Battery-free (free) / coin cell (~$30) | $5.25 board / ~$30 ([PCBWay](https://www.pcbway.com/project/shareproject/Dallas_DS1230Y_DS1235YW_NVRAM_FRAM_Replacement_Adapter_79f70ace.html); [OSH Park](https://oshpark.com/shared_projects/GCTJUxu1); [Tindie](https://tindie.com/products/glitchwrks/glitch-works-gw-1225-1-dallas-ds1225-replacement)) | **High** in the hobby segment |
| **Chip vendors:** RAMXEED MB85R8M2T, Infineon CY14B101 nvSRAM | Battery removal for OEM *redesigns*, at chip level | $51.21 ([Mouser](https://www.mouser.com/en/c/embedded-solutions/?m=RAMXEED)); $17.45–43.70 ([Future](https://futureelectronics.com/p/semiconductors--memory--RAM--nvram--quantum-trap-nvsram/cy14b101la-zs45xit-infineon-7001471); [Cytech](https://www.cytechsystems.com/fr/product/cy14b101la-sp25xi)) | Low; they do not sell drop-ins |
| **Substitutes:** control retrofit; RS-232/DNC backup software; Rockwell's 1785 EEPROM option on PLC-5 ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/plc-515-battery-failure-does-program-memory-get-lost)) | Remove the need entirely | Retrofit ≫ $249 | **Secular.** This is why the base shrinks |
| **C-16 space:** IBM in-house, Phison, Sage, Swissbit PowerSafe, Apacer CorePower, Samsung tantalum caps ([Samsung](https://image-us.samsung.com/SamsungUS/b2b/resource/2016/07/08/b2b_resource_WHP-SSD-POWERLOSSPROTECTION-r1-JUL16J.pdf)) | They own the PLP decision | n/a | Decisive. This is why C-16 is deferred |

### Honest win conditions

1. **There is a product gap.** Three targeted searches found **no battery-free PC Card SRAM product** (notes §1.3). A Japanese-market product may exist [UNVERIFIED].
2. **There is a supply gap.** Memex is out of most capacities, and the Mitsubishi successors still need batteries.
3. **Validation is the asset.** A public, growing matrix of controls that accept the card is the only thing a copycat lacks on day one.
4. **The federal channel favors us.** U.S. assembly of U.S. or Japanese die is TAA-clean and §5949-clean, which matters for the CDW-G channel only.

### Where you lose

- **On price** against a $160 used card bought by someone who doesn't value "no battery".
- **In the DIP hobby segment** against free designs.
- **Against a copy.** Moat is 2/5: "Any Fanuc-card reseller (Memex) can copy it once a working design is in the field" (veteran).
- **Against retirement.** Every retrofit removes a customer for good.

---

## 6. IP position

| Category | Detail |
|---|---|
| **Own** | Board designs and the CPLD/attribute configuration (trade secret). The **compatibility-validation database** (control × firmware × card attribute × result). Test fixtures and procedures. Brand and trademark. None of it is patentable in any way that matters, and the scorers rate moat 2/5. |
| **License** | Nothing. Chips are bought through distribution, so patent rights on Toggle MRAM and F-RAM are exhausted at sale. |
| **Can't** | Clone Fanuc boards such as the A20B-2900-0531 SRAM module (IP and liability exposure; notes §1.1). Use Fanuc or Mitsubishi logos; say "compatible with" only. Copy the open DIP adapters without checking their licenses; design our own instead. |

**FTO risks:**

1. **ITC 337-TA-1487 (Avalanche v. Everspin).**
   - Instituted 2026-02-27 ([USITC](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm)). The target date is now **2027-08-16** ([USITC notice, 2026-08-26](https://www.usitc.gov/sites/default/files/secretary/fed_reg_notices/337/337_1487_notice08262026sgl.pdf)) [REPORTED-P].
   - Avalanche asserts 37 claims from 4 patents against Everspin **STT-MRAM** imports.
   - The card uses Toggle and is insulated. The MR4A16B package site is unknown, so residual risk is low but not zero [UNVERIFIED].
   - The case would directly hit C-16, which needs the 1Gb STT part.
2. **The PC Card standard.** Whether a licence or logo program still applies to new PC Cards is unknown [UNVERIFIED]. Mitigation: no PCMCIA logo.
3. **The founder's day-job invention-assignment clause** (they work in product development at a manufacturer). Read it before any design work; get a written carve-out if it is broad [ESTIMATE: standard employment-agreement risk].

---

## 7. Regulatory and funding path

**Rules that matter:**

- **No UL or FCC authorization** for a memory-card subassembly sold in the U.S. CE and RoHS apply only for EU sales [UNVERIFIED].
- **Lithium shipping rules (UN3090/3091) disappear** with the battery: a small logistics win [UNVERIFIED].
- **FTC "Made in USA"** (16 CFR 323, "all or virtually all"). Claim **"Assembled in USA"** only. The Toggle die is fabbed in Arizona, but its package origin is unknown (A-09; `01_LANDSCAPE.md` §7.3, §10.3 rule 6).
- **TAA.** U.S. assembly of U.S. or Japanese die is clean, and CDW screens for it ([CDW](https://www.cdw.com/product/synchrotech-srx-series-flash-memory-card-4-mb-pc-card-taa-compliant/9204293)).
- **NDAA §5949**, effective 2027-12-23.
  - The FAR rule is still **proposed** ([GovInfo FR 2026-03065, 2026-02-17](https://www.govinfo.gov/content/pkg/FR-2026-02-17/html/2026-03065.htm)) [REPORTED-P].
  - Supplier certification after "reasonable inquiry" is enough ([Crowell, 2026-02](https://www.crowell.com/en/insights/client-alerts/section-5949-proposed-rule-puts-the-far-councils-chips-on-the-table)) [REPORTED].
  - Everspin, Infineon and RAMXEED are not CXMT, YMTC or SMIC. Add one line to the CoC. This is not a moat.
- **DFARS counterfeit-avoidance rules** (252.246-7007/-7008) for DoD sales: buy only from franchised distribution with traceable lots, not brokers [UNVERIFIED-H, `01_LANDSCAPE.md` §7.3].
- **Export:** not assessed. Confirm the classification before the first non-U.S. sale [UNVERIFIED].

**Funding:**

| Option | Fit | Call |
|---|---|---|
| **Bootstrap from $40k (A-03)** | Peak need $29.2k; kill test ~$6.7k | **Yes. The whole plan.** |
| **SBIR/STTR** | Reauthorized to 2031-09-30 ([UW Federal Relations, 2026-04-14](https://www.washington.edu/federalrelations/2026/04/14/trump-signs-sbir-sttr-reauthorization-bill-into-law/)). **The SBIR PI must spend more than half their time employed by the small business** ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)), **which excludes this founder while they keep the day job.** STTR needs a university partner, which is absurd for a product with no research in it | **No.** A DLA or Navy DMSMS topic could fund mil-temperature qualification later, only with a full-time PI [UNVERIFIED topic availability] |
| **CHIPS, §48D, state programs** | No silicon and no capex; state programs mostly multiply SBIR (`01_LANDSCAPE.md` §7.1) | **No** |
| **Equity** | Scorers: "good cash, not a company anyone should raise for" (VC) | **Never raise for C-12 alone.** Reconsider only if the S4 stretch path plus a software vault shows >$0.5M run-rate with >30% recurring revenue [ESTIMATE] |
| **Supplier terms or a small inventory line** | Inventory peaks at ~$15.6k (model §[4]) | Ask the EMS and distributor for net-30 once there are 3 months of order history [ESTIMATE] |

---

## 8. 18-month roadmap with milestones

Month numbers follow the model (m1 = 2026-11). Each gate is pass/fail on the date shown.

| Quarter | Work | Gate (measurable) |
|---|---|---|
| **Q1: m1–3 (2026-11 → 2027-01)** | Kill experiment (§10). LLC ($800). Contract EE starts the card design ($9k over m2–4) and DIP designs ($1.5k). MRAM PO for ~125 chips. Frame-kit and EMS RFQs | **G1 2026-12-01:** kill-test pass (§10). **G2 2027-01-31:** card rev-A layout done; MRAM PO confirmed with date ≤2027-07; landed 2MB COGS quote ≤$90 (model $85.50; >$120 triggers kill criterion 3) |
| **Q2: m4–6 (2027-02 → 04)** | **DIP launch, m4.** Card prototype run ($1.5k, m5). Full validation on Fanuc 16i/18i/21i or 0i-A and on MELSEC-Q: 100 power cycles, 72-h soak, format, backup and restore. Cash low $10.8k at m6 | **G3 2027-04-30:** ≥30 DIPs sold (model: 33); ≥1 card family passes the full protocol; ≥2 signed reseller agreements; cash ≥$8k |
| **Q3: m7–9 (2027-05 → 07)** | First 100-card U.S. EMS lot. Compatibility matrix v1 published. **Card launch, m9.** Deposit holders ship first | **G4 2027-07-31:** 100-card lot delivered at ≤$90 landed 2MB COGS; ≥60% of deposits convert to orders |
| **Q4: m10–12 (2027-08 → 10)** | eBay and reseller stock. Watch the ITC target date (2027-08-16) for C-16. **Breakeven, m11** | **G5 2027-10-31:** net ≥0 in 2 of the last 3 months; ≥3 reseller accounts ordering; ≥25 cumulative cards (model: 33); returns <5% |
| **Q5: m13–15 (2027-11 → 2028-01)** | §5949 CoC line from 2027-12-23. CDW-G/GSA-reseller onboarding. **Cloud backup vault, m15** ($29/shop/month) | **G6 2028-01-31:** ≥20 cards/month (model m14: 20); ≥1 federal-reseller listing live |
| **Q6: m16–18 (2028-02 → 04)** | Adjacent SKUs: Fanuc robot (RJ-2/3) validation and a Mitsubishi-format card. First DIBBS quote attempts. Glut watch begins | **G7 2028-04-30:** run-rate ≥$120k (model: $121.7k); cash ≥$18k (model: $18.8k); cumulative 183 cards + 550 DIPs (±20%). **Decision:** keep as a side business or pursue S1 white-label |

---

## 9. Team required

| Role | When | Where to find them | Cost (model) |
|---|---|---|---|
| **Founder** (store, compatibility DB, cloud vault, supplier and EMS management, reseller sales, fulfilment) | m1 onward, ~15 h/week (A-03) | n/a. The day job in product development and operations at a manufacturing company is directly relevant to EMS and quality work | $0 salary in BASE, GLUT and SEVERE (model §[5]) |
| **Contract EE** (PC Card layout, 5V-tolerant interface, attribute memory, optional ≤$5 CPLD fix) | m1 (kill test, $2k) and m2–4 (rev A) | People who already ship DS12xx drop-ins (Glitch Works on Tindie); designers of the 3458A FRAM adapter in the xDevs and EEVblog communities; retired Fanuc field-service engineers active on CNCzone and Practical Machinist | $9k card + $1.5k DIP (model §[9] `one_time`) |
| **Bench and validation partner** (Fanuc and Mitsubishi controls) | m1–6 | Buy a used control (budget $2.5k), or rent bench time at a CNC repair house; MRO Electric is customer #2 and a natural partner. Fallback: a local community-college CNC program [ESTIMATE] | $2.5k one-time |
| **U.S. EMS** | m5 (prototype), m8 (first lot) | MacroFab, Houston, with real-time online quotes ([MacroFab](https://macrofab.com/index.php)); Screaming Circuits, best on runs of 25+ ([PICList, 2008](https://pic.hallikainen.org/piclist/2008/a/01/29/165504a.txt)); Rush PCB on the East Coast, IPC-A-610, location unverified ([Rush PCB](https://rushpcb.com/?p=839)) | $14 + $4 + $4 per card (in COGS) |
| **Bookkeeper and insurance** | m4 onward | Local small-business bookkeeper; product-liability policy | $225/month (model §[9]) |
| **Part-time fulfilment help** | Only on the S1 path (>100 orders/month) | Local hourly help or a 3PL | Not in BASE [ESTIMATE ~$500/month if needed] |
| **DMSMS business-development advisor** | m24+, only if pursuing LTSAs | Retired DLA or NAVSUP DMSMS engineers, on commission | Not in BASE [ESTIMATE: commission only] |

BASE never hires an employee: the founder plus ~$10.5k of contract engineering ($9k card + $1.5k DIP design; model §[9] `one_time`; the kill test's $2k EE fee is part of the $9k, pulled forward).

---

## 10. The cheapest experiment that could kill it

**Budget ~$6.7k plus ~$3k contingency (≤$9.7k, <$10k). Duration 29 days (day 0 = 2026-11-02; decision on day 29 = 2026-12-01). The thresholds below are fixed before any data comes in.** Three tracks run in parallel. The plan comes from notes §8, with two changes I made: the deposit page states the real ship date, and a magnetic-field check is added.

**Track A: Demand (~$1.2k)** [ESTIMATE: notes §8; $600 of it is ads, the rest landing page, store and deposit-processing setup]
1. Day 1–3: landing page and store listing for "NV-CARD 2MB/4MB battery-free SRAM card for Fanuc and Mitsubishi Q". $249/$349, **$25 refundable deposit, target ship 2027-07** (model m9), refundable on request at any time.
2. Day 3–28: $600 of search ads on "fanuc sram card", "Q2MEM-2MBS", "Q2MEM-2MBSN" and "DS1245 replacement". Posts on CNCzone and Practical Machinist.
3. Day 3–20: 20 emails and calls to Memex, MRO Electric, Do Supply, Radwell, CDW-G's Synchrotech category manager and five local CNC repair shops. The ask is **a wholesale LOI at $175/card, MOQ 10.**

**Track B: Technical (~$5.5k: control $2.5k, parts and PCBs $0.8k, donor cards $0.2k, contract EE $2k; notes §8)**
1. Day 1–7: buy a used Fanuc 16i/18i/21i or 0i-A control ($2.5k), or book bench time. Borrow or buy a MELSEC-Q CPU. Buy a PC Card reader.
2. Day 1–10: 10 bare 0.8mm PCBs; 6× MR4A16B from distributor or broker stock; LVC buffers. Reuse the shells of 3–5 used SRAM cards ($20–50 each) so no frame-kit MOQ is needed. The contract EE hand-builds 3–5 cards ($2k).
3. Day 12–28, tests:
   - Fanuc boot-menu SRAM backup and restore
   - ALL-I/O punch to card
   - Card format
   - Mitsubishi format plus parameter write
   - 100 power cycles with verify
   - 72-hour read/write soak
   - No battery alarm with BVD strapped
   - *Added:* 72 hours stored beside a spindle motor or magnetic chuck, then verify. Toggle MRAM's tolerance of shop-floor magnetic fields is untested [UNVERIFIED risk].
4. Fallback: if no MRAM arrives by day 7, prototype on FM28V100 or RAMXEED MB85R8M1 **for the compatibility test only**, and log that the timing results do not transfer.

**Track C: Supply ($0)**
- RFQs for 250× MR4A16B (price and lead time), PC Card frame kits (MOQ and price) and a 100-card U.S. EMS build.

**C-16 interest ($0)**
- Email Swissbit, Apacer, Sage and Phison application engineering: "Would you pay $40k for a validated MRAM-PLP design-in package?"

### Pass/fail thresholds (decided now)

| Test | PASS | FAIL → action |
|---|---|---|
| Demand | ≥15 deposits **or** ≥2 reseller LOIs | <15 deposits **and** <2 LOIs → **kill as a venture**; at most a hobby DIP SKU |
| Technical | ≥1 of {Fanuc, Mitsubishi Q} passes every test | A family that rejects the card after a ≤$5 CPLD fix is dropped. **Both fail → kill C-12** |
| Supply | Landed 2MB COGS ≤$120; frame kit ≤$20 at MOQ ≤1,000 | Above either → reprice to ≥$299 and re-run demand for 14 days; <10 deposits at $299 → kill |
| C-16 | ≥2 "yes, send terms" | <2 → C-16 stays dead |

The $299 demand re-test runs only if the supply test fails. It is a follow-on gate (kill criterion 3, 2026-12-15), outside the 29-day experiment, paid from the contingency.

**Cash effect.** The test pulls forward ~$5.3k the model already books for m2–5 (control, part of the EE fee, prototype parts). It adds ~$1.4k of new spend (ads, donor cards), so the modeled cash low falls from $10.8k to about **$9.4k** [ESTIMATE].

---

## 11. Explicit kill criteria

1. **2026-12-01:** <15 paid deposits AND <2 reseller LOIs → kill as a venture.
2. **2026-12-01:** both Fanuc and Mitsubishi Q reject the MRAM card (format, read, write or restore) after a ≤$5 CPLD fix → kill the card line.
3. **2026-12-15:** landed 2MB COGS >$120 or frame-kit MOQ >1,000 or price >$20, and <10 deposits at a $299 re-test → kill.
4. **2027-01-31:** the MR4A16B order cannot be confirmed for delivery by 2027-07-31, and no alternative core passes timing → slip the card launch. If that pushes launch past 2027-10 (+3 months), re-run the model. If the card launch +6 months case (breakeven m17, cash low $6.0k) would be breached, stop.
5. **2027-04-30:** cash <$5k → halt all non-inventory spend; cash <$3k → wind down.
6. **2027-10-31 (m12):** <20 cumulative cards sold or <2 active reseller accounts → kill the card line (model expects 33 cards and ≥3 accounts).
7. **First 100 cards shipped:** compatibility returns >10% → stop sales until fixed; >20% → kill.
8. **2028-03-31 (m17):** not at monthly breakeven (net ≥0 for 3 consecutive months) → wind down to a DIP-only hobby SKU. m17 is the worst modeled case (price −30% or launch +6 months).
9. **Any month:** realized blended card price <$175 for 3 consecutive months, the copycat signal → exit. The model's price −30% case leaves $1.2k of 36-month net.
10. **2028-04-30 (m18):** run-rate <$85k (the conversion −30% case) → freeze investment and run for cash. <$60k → wind down.
11. **Everspin MR4A16B EOL/LTB notice, or lead time >40 weeks:** no validated alternative core within 90 days → stop new card lots and sell through.
12. **C-16, 2026-12-01:** <2 "send terms" replies → dead. Reopen only if, after the ITC final determination (target 2027-08-16), an SSD or logger OEM asks for it unprompted.

---

## 12. Cycle test: 2028–29 glut (DDR5 −60%) and severe (−90%)

The DRAM decks come from `models/dram_cost_stack.py` `ddr5_reference()`: shortage $20.37/GB, glut $8.15/GB, severe $2.04/GB. Glut and severe ramp in over 2028-H1 (m15–20); BASE eases 10% over 2028 (m15–26).

| Metric | BASE | GLUT (−60%) | SEVERE (−90%) |
|---|---|---|---|
| Breakeven month | 11 | 11 | 12 |
| Cash low | $10.8k (m6) | $11.6k (m6) | $12.2k (m7) |
| Run-rate m18 / m36 | $121.7k / $195.8k | $115.6k / $186.0k | $93.1k / $153.9k |
| 36-mo net | $79.1k | $79.0k | $49.3k |
| Cash m36 | $103.5k | $104.9k | $77.4k |
| C-16 MRAM premium/board | $362 | $382 | $394 |
| C-16 option EV | −$44.8k | −$47.0k | −$48.3k |

**The core passes.** It sells against lithium cells and obsolete NVSRAM, never against DRAM. The scenario drops come entirely from judgment multipliers, not DRAM prices:
- **GLUT:** demand × 0.95 for a capex slowdown, offset by COGS × 0.95 as specialty NVM softens. Net is unchanged at $79.0k.
- **SEVERE:** demand × 0.85, price × 0.90 (copycats) and COGS × 0.90. This cuts 36-month net by 38% to $49.3k.

A glut may even help slightly, as shops keep legacy controls longer [ESTIMATE].

**The cycle that does threaten this business is the retirement curve, not DRAM.**
The base shrinks yearly, each battery-free card removes an 8-year replacement, and the model does not decay demand. A 10%/yr shrink over three years [ESTIMATE: 0.9³ ≈ 0.73] is close to the "conversion −30%" case: m36 run-rate $137.1k, 36-month net $42.3k. Survivable as a side business; it caps every scale path.

**C-16 gets worse in a glut**, as the scorers predicted. Cheaper DRAM widens the MRAM premium by $20–33 per board and cuts p(design-in) from 0.32 to 0.11. It stays deferred.

---

## 13. Sources

Every URL below appears in `research/sources/p4-nv-continuity-modules.jsonl` or another `research/sources/*.jsonl` log. All are cross-referenced in `research/sources/p4w-nv-continuity-modules.jsonl`. All were seen through search snippets (accessed 2026-11-01).

**Market, installed base, pain**
- https://memex.ca/?p=596 (Memex; cards "hard to get")
- https://www.cnczone.com/forums/fanuc/421202-fanuc-16ia-sram-memory-card-backup.html (eBay ~$200–500; OEM "big $$$")
- https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-2021-parameter-backup-via-pcmcia-sram-card
- https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-rj-2-pcmcia-sram-memory-card-compatibility-guide
- https://industrialmonitordirect.com/blogs/knowledgebase/plc-515-battery-failure-does-program-memory-get-lost
- https://mitsubishielectric.co.jp/fa/document/technews/plc/t30-0007/t300007.pdf
- https://mitsubishielectric.com/fa/document/technews/plc/fa-a-0267/faa0267a.pdf (2018-10)
- https://metalworkingnews.info/fanuc-reaches-cnc-production-milestone-of-5-million/ (2022)
- https://www.mmsonline.com/blog/post/capital-spending-survey-projects-5-decline-in-machine-tool-buying-for-2020-but-spending-level-still-above-average (2019)
- https://www.mroelectric.com/product/A20B-2900-0531
- https://www.dosupply.com/automation/fanuc/other/DISKMF32M1LCDA7
- https://www.dosupply.com/automation/mitsubishi/melsec-q/Q2MEM-2MBS

**Competitor and alternative pricing**
- https://www.cdwg.com/product/synchrotech-sram-pcmcia-memory-pc-cards-replaceable-battery-flash-memory/5006798 ($239.39)
- https://www.cdw.com/product/synchrotech-srx-series-flash-memory-card-4-mb-pc-card-taa-compliant/9204293 (TAA)
- https://www.ebay.de/itm/306136207868 ($160–440 used)
- https://www.ebay.de/itm/406086802130 (Q2MEM-2MBSN $403.81)
- https://www.tweaktown.com/pressrelease/1122/pretec_extends_dual_battery_sram_pc_card_to_16mb/index.html (2009)
- https://csi.pl/wp-content/uploads/2020/05/Karta-katalogowa-SuperStore-SRAM-blue.pdf
- https://findchips.com/search/DS1230Y-85?f=dsa (2026)
- https://www.analog.com/ja/products/ds1230y
- https://www.digipart.com/part/DS1230AB-85
- https://www.pcbway.com/project/shareproject/Dallas_DS1230Y_DS1235YW_NVRAM_FRAM_Replacement_Adapter_79f70ace.html
- https://oshpark.com/shared_projects/GCTJUxu1
- https://tindie.com/products/glitchwrks/glitch-works-gw-1225-1-dallas-ds1225-replacement
- https://www.mouser.com/en/c/embedded-solutions/?m=RAMXEED (2026)
- https://futureelectronics.com/p/semiconductors--memory--RAM--nvram--quantum-trap-nvsram/cy14b101la-zs45xit-infineon-7001471 (2026)
- https://www.cytechsystems.com/fr/product/cy14b101la-sp25xi (2026; CY14B101 ~$43.70 qty 1)

**Components and manufacturing**
- https://www.digikey.com/en/products/detail/everspin-technologies-inc/MR4A16BYS35/4021237 ($46.03)
- https://www.futureelectronics.com/p/memory--RAM--nvram/mr4a16bcys35r-everspin-technologies-6114651 ($37.67 @1k; 26 wk)
- https://azcus.digikey.com/en/products/detail/infineon-technologies/FM18W08-SG/4090358 ($12.87)
- https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm (Everspin 10-K, 2026-03)
- https://www.lcsc.com/product-image/C20342497.html (1Gb STT $102.60 @500)
- https://community.sparkfun.com/t/pcb-assembly-service/27265
- https://pic.hallikainen.org/piclist/2008/a/01/29/165504a.txt (2008-01)
- https://macrofab.com/index.php
- https://rushpcb.com/?p=839

**C-16 PLP**
- https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966 (2026-10-05)
- https://www.eenewseurope.com/en/phison-memory-controllers-to-support-1gbit-mram/ (2018)
- https://embeddedcomputing.com/technology/storage/sage-microelectronics-and-everspin-partner-to-bring-spin-transfer-torque-mram-to-next-generation-enterprise-ssd-devices (2019)
- https://www.electronicsforu.com/news/new-products/swissbit-introduces-powersafe-a-power-loss-protection-system-for-industrial-ssds
- https://www.soselectronic.com/en-us/articles/apacer/apacer-corepower-your-valuable-data-deserves-top-tier-protection-3065
- https://image-us.samsung.com/SamsungUS/b2b/resource/2016/07/08/b2b_resource_WHP-SSD-POWERLOSSPROTECTION-r1-JUL16J.pdf (2016-07)

**Legal, regulatory, funding, government**
- https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm (2026-02-27)
- https://www.usitc.gov/sites/default/files/secretary/fed_reg_notices/337/337_1487_notice08262026sgl.pdf (2026-08-26)
- https://www.avalanche-technology.com/itc-institutes-investigation-into-everspin-technology-based-on-avalanche-claims-of-patent-infringement/ (2026-02)
- https://www.govinfo.gov/content/pkg/FR-2026-02-17/html/2026-03065.htm (2026-02-17)
- https://www.crowell.com/en/insights/client-alerts/section-5949-proposed-rule-puts-the-far-councils-chips-on-the-table (2026-02)
- https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and (SBIR PI rule)
- https://www.washington.edu/federalrelations/2026/04/14/trump-signs-sbir-sttr-reauthorization-bill-into-law/ (2026-04-14)
- https://www.dla.mil/Portals/104/Documents/SmallBusiness/DIBBS%20Solicitations%20-%20With%20Notes.pdf (logged with spaces in `p4-nv-continuity-modules.jsonl`)
- https://www.highergov.com/nsn/5962012622185/ (2026)

**Internal:** `models/nv-continuity-modules.py`; `models/dram_cost_stack.py`; `research/assumptions/p4-nv-continuity-modules.md`; `research/assumptions/p4w-nv-continuity-modules.md`; `ASSUMPTIONS.md` (A-03, A-05, A-09); `01_LANDSCAPE.md` §7, §10.3; `03_SCORING.md` §6, §7.3.
