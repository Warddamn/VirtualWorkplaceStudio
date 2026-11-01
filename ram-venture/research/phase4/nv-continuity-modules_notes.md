# DD3 research notes: Drop-in Non-Volatile Continuity Modules

**Agent:** `p4-nv-continuity-modules` · **As of:** 2026-11-01 · **Anchor:** C-12 · **Folded in:** C-16
**Files:**
- Model: `models/nv-continuity-modules.py` (exit 0); printed output in `research/phase4/nv-continuity-modules_model_output.md`
- Sources: `research/sources/p4-nv-continuity-modules.jsonl` (74 entries)
- Assumptions: `research/assumptions/p4-nv-continuity-modules.md`

> **Evidence grade.** I used all 28 of my WebSearch calls. All 3 WebFetch attempts failed DNS: dosupply.com, tindie.com and usitc.gov. Every external fact below therefore comes from a search-result snippet. Nothing is [VERIFIED].
> - **[REPORTED-P]:** a primary page (manufacturer, distributor, USITC, Mitsubishi bulletin) seen only through a snippet.
> - **[REPORTED]:** secondary coverage, forums, or reseller and marketplace listings.
> - **[ESTIMATE]:** computed in the model, or my judgment.
> - **[UNVERIFIED]:** prior knowledge with no URL found.
>
> To upgrade these grades, allow memex.ca, dosupply.com, tindie.com, usitc.gov, digikey.com and everspin.com in the session's network settings.

---

## 0. Verdict first

| Question | Answer |
|---|---|
| **POSSIBLE?** | **Yes, TRL 9 parts.** Everspin MR4A16B 16Mb Toggle MRAM has true asynchronous-SRAM timing and sells for $37.67–46.03 with a 20–26-week lead time. FM18W08 F-RAM is 5V-capable and in stock at $12.87. The engineering is a 5V-tolerant PC Card or DIP adapter. Nobody has yet shown that a Fanuc or Mitsubishi control accepts an MRAM card; that is test 1. |
| **PROFITABLE?** | **Yes, as a small business.** The card line has a **57–61% unit GM** and **44–46% contribution**. The DIP line is a traffic line, with −1% to +17% contribution. BASE breaks even in **month 11**, the cash low is **$10.8k (month 6)**, run-rate revenue is **$122k/yr at month 18** and **$196k/yr at month 36**, and cumulative net is $79k. **It is not venture-scale.** Total worldwide demand for replacement PC-card SRAM is about **$3M/yr and shrinking** [ESTIMATE]. Even a stretch path (12% global share, white-label MRO distribution, four DMSMS contracts) reaches only **~$0.52M/yr**. |
| **DOABLE BY THIS FOUNDER?** | **Yes.** The product has no firmware and is pure logic. It needs one ~$9k contract EE engagement and bench access to legacy controls. The founder's software skills go into the store, the compatibility database and an optional backup-vault subscription. A part-time founder never earns a full-time salary in BASE. |
| **"Better than RAM" axis** | **Non-volatility and lifecycle, not $/GB.** MR4A16B is about **$21,500/GB**, roughly 1,000× the $20.37/GB DDR5 contract price. It wins only where the alternative is a **lithium-backed SRAM card or a Dallas NVSRAM** in a legacy CNC, PLC, robot or instrument whose owner loses parameters when the cell dies. |
| **Glut test** | **Passes.** Run-rate at month 36 is $196k in BASE, $186k in GLUT and $154k in SEVERE. The whole SEVERE drop comes from assumed macro and copycat multipliers, not from DRAM. The core never sells against DRAM. |
| **C-16 PLP kit** | **Defer.** The computed MRAM premium is **$362–394 per board** against DRAM plus supercaps in every scenario. Expected value at T0 is **−$45k to −$48k**; it needs ~3 paid design-ins to break even. The ITC 337-TA-1487 target date is now **2027-08-16** ([USITC notice 2026-08-26](https://www.usitc.gov/sites/default/files/secretary/fed_reg_notices/337/337_1487_notice08262026sgl.pdf)) [REPORTED-P]. |
| **Role in the portfolio** | **FALLBACK or bridge-revenue candidate, not PRIMARY.** It is cheap, fast, glut-proof and founder-doable. Its ceiling is the size of a declining installed base. |

---

## 1. Q1: Market evidence: who still relies on battery-backed SRAM, and what replacements cost

### 1.1 Installed base

| Family | Evidence | What it means for us |
|---|---|---|
| **Fanuc CNC** | 5 million cumulative CNCs produced by Feb-2022 ([Metalworking News](https://metalworkingnews.info/fanuc-reaches-cnc-production-milestone-of-5-million/); [MONOist 2022-04](https://monoist.itmedia.co.jp/mn/spv/2204/19/news036.html)) [REPORTED]. Fanuc 20/21 rejects CompactFlash in a PC Card adapter and needs a genuine SRAM card ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-2021-parameter-backup-via-pcmcia-sram-card)). 18i-T needs a true SRAM card ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-18i-t-memory-card-not-reading-sram-vs-flash-fix)). 16i-B and later use flash cards ([CNCzone](https://www.cnczone.com/forums/fanuc/421202-fanuc-16ia-sram-memory-card-backup.html)) [REPORTED, low-authority] | The SRAM-card need is concentrated on **pre-~2005 controls** (0/15/16/18/20/21, i-A). It is a **backup tool, so demand is per shop or technician, not per machine.** |
| **Fanuc robots** | RJ-2 controllers use PCMCIA SRAM cards for backup; not every card is compatible ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-rj-2-pcmcia-sram-memory-card-compatibility-guide)) [REPORTED] | Same card, different validation. |
| **Fanuc internal SRAM module** | MRO Electric sells and repairs the A20B-2900-0531 128KB SRAM module for Series 16/18, with core exchange and a 2-year warranty ([MRO Electric](https://www.mroelectric.com/product/A20B-2900-0531)) [REPORTED] | A board-level NV clone is possible, but it means cloning a Fanuc board (IP and liability exposure). **Not in the plan.** |
| **Mitsubishi MELSEC-Q** | Q2MEM-1MBS/2MBS SRAM cards were discontinued in Oct-2018. The -1MBSN/-2MBSN replacements came out at the "same standard price", and both need battery backup ([Mitsubishi FA-A-0267-A](https://mitsubishielectric.com/fa/document/technews/plc/fa-a-0267/faa0267a.pdf)) [REPORTED-P]. A card used without its battery **may not raise a battery error, and loses its data at power-off** ([Mitsubishi T30-0007](https://mitsubishielectric.co.jp/fa/document/technews/plc/t30-0007/t300007.pdf)) [REPORTED-P] | **The clearest statement of the pain:** silent data loss. Mitsubishi Q is a second validated family. |
| **Allen-Bradley PLC-5** | Rockwell calls it "among the largest installed base of any one control platform", with spares, repairs and engineers increasingly scarce ([Rockwell](https://www.rockwellautomation.com/en-be/capabilities/industrial-maintenance-support/modernization/plc-5-migration.html)) [REPORTED-P]. The program sits in battery-backed CMOS RAM, but a **1785 EEPROM (NVR) option already removes the battery** ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/plc-515-battery-failure-does-program-memory-get-lost)) [REPORTED, low-authority] | **No module opening.** Rockwell already sells the non-volatile option. |
| **Siemens S5** | 6ES5 375 RAM submodules depend on the CPU battery ([Cirele](https://cirele.com/en/plc/siemens-simatic-s5-6es5375-0lc41-2-2/)). Used units sell for €22 ([Machineseeker](https://www.machineseeker.com/siemens-6es5+375-1la21/i-6975873)) up to $58–700 on U.S. eBay ([eBay](https://www.ebay.com/p/169944593)) [REPORTED] | The market is Europe-heavy and cheap, and EPROM submodules already exist. **Deprioritized.** |
| **Okuma, Mazak, Heidenhain, Haas** | **Nothing found** in two searches [UNVERIFIED] | Treat as unknown. Do not plan SKUs until a control is on the bench. |
| **Dallas DS12xx and ST M48 NVSRAM** | ADI still lists some DS1230Y order codes as in production ([ADI](https://www.analog.com/ja/products/ds1230y)). DS1245Y is obsolete or "not recommended for new design" ([Digipart](https://www.digipart.com/part/DS1245Y-85)). Rochester Electronics holds DS1230AB stock, date code 24+ ([Digipart](https://www.digipart.com/part/DS1230AB-85)). ST M48T08 is active ([ST](https://www.st.com/en/clocks-and-timers/m48t08.html)), while some M48T35 codes are obsolete ([Lisleapex](https://www.lisleapex.com.tw/series-m48t35)) [REPORTED] | Supply is **still available** for DS1230. The DS1245/DS1250 tier is where obsolescence bites. TIMEKEEPER parts (M48T) include an RTC that cannot run battery-free, so they are **out of scope**. |

### 1.2 Demand sizing (computed, `models/nv-continuity-modules.py` §[3])

The chain multiplies 5M Fanuc CNCs × 15% U.S. × 35% SRAM-card-era controls × 50% still running, which gives **~131k U.S. legacy machines**. At ~8 machines per shop that is **~16k shops**; for scale, the U.S. has more than 20,000 job shops ([MMS/Gardner](https://www.mmsonline.com/blog/post/capital-spending-survey-projects-5-decline-in-machine-tool-buying-for-2020-but-spending-level-still-above-average)).

One card per shop every 8 years, × 1.5 for other families (Mitsubishi Q, robots, avionics, test and measurement, synths), gives **~3,100 cards/yr in the U.S. and ~12,300/yr globally**. At a blended net $241 per card that is **$0.74M/yr (U.S.) and ~$3.0M/yr (global)** [ESTIMATE].

**This is the cap.** Our battery-free card also removes the replacement cycle. Every unit we sell takes a future replacement out of the market.

### 1.3 Prices of existing replacement products and who sells them

| Product | Price | Seller | Battery? | Source |
|---|---|---|---|---|
| Synchrotech 2MB SRAM PC Card (replaceable primary + rechargeable cell) | **$239.39** | CDW Government | Yes | [CDW-G](https://www.cdwg.com/product/synchrotech-sram-pcmcia-memory-pc-cards-replaceable-battery-flash-memory/5006798) [REPORTED-P] |
| Used 2MB SRAM PC cards (Pretec, Epson, Panasonic, Melcard) | **$160–440** | eBay | Yes | [eBay](https://www.ebay.de/itm/306136207868) (via snippet summary) [REPORTED] |
| Fanuc-compatible SRAM cards, per forum | **~$200–500 on eBay**; Fanuc OEM "big $$$" | eBay / Fanuc | Yes | [CNCzone](https://www.cnczone.com/forums/fanuc/421202-fanuc-16ia-sram-memory-card-backup.html) [REPORTED] |
| Memex Fanuc SRAM cards (1/2/4MB) | Not shown; **only 2MB in stock**, and "hard to get" | Memex (Ontario) | Rechargeable lithium, ~1 yr retention | [Memex](https://memex.ca/?p=596) [REPORTED] |
| Mitsubishi Q2MEM-2MBS (new) / -2MBSN | **$200 / $403.81** | eBay | Yes | [eBay](https://www.ebay.de/itm/197650556492); [eBay](https://www.ebay.de/itm/406086802130) [REPORTED] |
| Do Supply Fanuc 2MB SRAM card DISKMF32M1LCDA7 | Not shown (fetch failed) | Do Supply | Yes | [Do Supply](https://www.dosupply.com/automation/fanuc/other/DISKMF32M1LCDA7) [REPORTED] |
| Pretec and CSM industrial SRAM PC cards, 256KB–16MB | Not shown; 2009-era lines | Pretec, CSM | Yes (dual battery) | [TweakTown/Pretec](https://www.tweaktown.com/pressrelease/1122/pretec_extends_dual_battery_sram_pc_card_to_16mb/index.html); [CSM](https://csi.pl/wp-content/uploads/2020/05/Karta-katalogowa-SuperStore-SRAM-blue.pdf) [REPORTED] |
| DS1230Y-85 (new, ADI) | **$35–44 qty 1; ~$25 @1k** | Distributors | Yes (sealed) | [Findchips](https://findchips.com/search/DS1230Y-85?f=dsa) [REPORTED] |
| Glitch Works GW-1225-1 (DS1225 drop-in, CR1225 cell) | **~$30** (unconfirmed) | Tindie | Yes (replaceable) | [Tindie](https://tindie.com/products/glitchwrks/glitch-works-gw-1225-1-dallas-ds1225-replacement) [REPORTED] |
| Open FM18W08 DS1230 / DS1225 / 3458A adapters | **Free** design; board $5.25 | PCBWay / OSH Park | **No** | [PCBWay](https://www.pcbway.com/project/shareproject/Dallas_DS1230Y_DS1235YW_NVRAM_FRAM_Replacement_Adapter_79f70ace.html); [PCBWay DS1225](https://www.pcbway.com/project/shareproject/Dallas_DS1225Y_FRAM_Adapter_3c961bed.html); [OSH Park 3458A](https://oshpark.com/shared_projects/GCTJUxu1) [REPORTED] |
| Infineon CY14B101 1Mb nvSRAM (chip-level alternative) | **$17.45 @1k to $43.70 qty 1**; lead time 8–40 weeks | Future, Cytech | No (QuantumTrap) | [Cytech](https://www.cytechsystems.com/fr/product/cy14b101la-sp25xi); [Future](https://futureelectronics.com/p/semiconductors--memory--RAM--nvram--quantum-trap-nvsram/cy14b101la-zs45xit-infineon-7001471); [Future 40 wk](https://www.futureelectronics.com/p/semiconductors--memory--quantum-trap-nvsram/cy14b101i-sfxi-cypress-9088809) [REPORTED] |

**No battery-free PC-card SRAM product was found** in three targeted searches. RAMXEED markets its 8Mbit parallel FRAM to "eliminate batteries for SRAM in industrial machinery", but only at chip level, for OEM redesigns ([Radiolocman](https://www.radiolocman.com/news/new.html?di=514081); [Rutronik](https://www.rutronik.com/article/alternative-for-srams-new-8-mbit-fram-from-fujitsu)) [REPORTED]. A Japanese-market product may exist that English searches missed [UNVERIFIED].

**Pricing power.** The anchors are $200–440 battery cards. A battery-free card at **$249 is priced at parity with the new Synchrotech card**, not at a premium, because the buyer's alternative is "$200 on eBay". The model's sensitivity table shows that a 30% price cut takes the cash low to **$577** and breakeven to month 17. Price is the variable that matters most.

---

## 2. Q2: Component supply, cost and fab location

| Part | Role | Price | Lead time / stock | Fab | Source |
|---|---|---|---|---|---|
| **Everspin MR4A16B** (16Mb ×16 Toggle MRAM, 35ns, 3.3V) | PC Card core: 1 chip = 2MB, 2 chips = 4MB | **$46.03 qty 1** (DigiKey, 0 stock); **$37.67 @1k** (Future); $45.54 (IBS, multiples of 368) | **20–26 weeks** | **Chandler AZ** (Toggle made in-house on 200mm; Everspin 10-K) [REPORTED-P via Phase 1/2]. Package site unknown [UNVERIFIED] | [DigiKey](https://www.digikey.com/en/products/detail/everspin-technologies-inc/MR4A16BYS35/4021237); [Future](https://www.futureelectronics.com/p/memory--RAM--nvram/mr4a16bcys35r-everspin-technologies-6114651); [IBS](https://www.ibselectronics.com/part/everspin/mr4a16bma35r/2121039/); [10-K](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm) |
| **Infineon FM18W08** (256Kb ×8 F-RAM, 2.7–5.5V) | DS1225/DS1230 DIP drop-in | **$12.87 qty 1** | ~775 in stock; 8-week standard lead time | Unconfirmed. 130nm F-RAM moved to TI Dallas, and Fab 25 Austin was qualified for Kb parts (Cypress PCN, via A1) [REPORTED]. Fab 25 has belonged to SkyWater, an IonQ subsidiary, since 2026-07-31 | [DigiKey](https://azcus.digikey.com/en/products/detail/infineon-technologies/FM18W08-SG/4090358); [DigiKey CN](https://digikey.cn/en/products/detail/infineon-technologies/FM18W08-SG/4090358); [Cypress PCN](https://community.infineon.com/gfawx74859/attachments/gfawx74859/NonVolatileRAM/1143/1/002-18474_00_V.pdf) |
| **Infineon FM28V100** (1Mb ×8 F-RAM, 2.0–3.6V) | DS1245 drop-in, which needs 5V-tolerant translators | **$17.7–29.9 qty 1**; $19.38 @2 (Future) | 216–2,326 in stock across distributors | As above | [Findchips](https://findchips.com/search/fm28v100); [Future](https://www.futureelectronics.com/p/semiconductors--memory--RAM--nvram--fram-mram/fm28v100-tg-infineon-6750863) |
| **RAMXEED MB85R8M1 / MB85R8M2TA** (8Mbit FRAM) | Alternative core for the card | **$51.21 qty 1** | 141–703 in stock | Japan | [Mouser](https://www.mouser.com/en/c/embedded-solutions/?m=RAMXEED); [datasheet Oct-2025](https://www.ramxeed.com/jp/home/wp-content/uploads/2025/10/MB85R8M2TA-DS3v0-J.pdf) |
| **Everspin EMD4E001G** (1Gb STT, ST-DDR4) | C-16 PLP journal | **$102.60 @500** (~$821/GB) | n/a | **GF Singapore** CMOS + Chandler BEOL; **in scope of the ITC case** | [LCSC](https://www.lcsc.com/product-image/C20342497.html) |
| PC Card frame kit + 68-pos connector | Card housing | **No small-quantity price found** ($12 [ESTIMATE]) | ITT StarCard kits exist; one 68-pos connector is **Last Time Buy**; 3M connector sold in packs of 10 | n/a | [Design News/ITT](https://www.designnews.com/motion-control/itt-interconnect-solutions-snap-on-and-ultrasonic-pcmcia-i-o-card-kits); [Cytech LTB](https://www.cytechsystems.com/de/product/ic1k-68rd-1.27sfa71); [Aeri/3M](https://www.aeri.com/pn/3m/mch068tan07lphtr30) |

**Design choice, made and logged.** The card uses **Toggle MRAM rather than F-RAM** for three reasons:
1. Toggle MRAM has genuine asynchronous-SRAM timing. FM18W08-class F-RAM latches the address on /CE falling and fails in sockets that hold /CE low (veteran scorer, Phase 3).
2. A single 16Mb chip makes a 2MB card.
3. Toggle MRAM is **U.S.-fabbed** and, per Everspin, **not implicated** in the ITC case (A2 notes) [REPORTED].

The cost is a 3.3V part on a 5V bus, so the card carries 5V-tolerant LVC buffers [ESTIMATE].

**Supply risks.** The first is the **26-week MRAM lead time**: order at month 3 for a month-9 launch, and hold 3 months of cover. The second is the **frame kit**: its MOQ and pricing are unknown, and the connectors are going Last Time Buy.

---

## 3. Q3: U.S. assembly cost and certification

- **Cost evidence.**
  - Turnkey fab plus assembly quotes for 10 boards ranged **$415–1,300** ([SparkFun forum](https://community.sparkfun.com/t/pcb-assembly-service/27265)) [REPORTED, dated].
  - Screaming Circuits prices best on runs of **25+** ([PICList 2008](https://pic.hallikainen.org/piclist/2008/a/01/29/165504a.txt)).
  - MacroFab (Houston) quotes in real time ([MacroFab](https://macrofab.com/index.php)).
  - On the East Coast, Rush PCB advertises turnkey assembly to IPC-A-610 and ISO 13485 ([Rush PCB](https://rushpcb.com/?p=839)). Its Massachusetts location comes from the search summary and is unverified.
- **Model.** Assembly **$14/card**, plus **$4 setup amortization** (~$400 stencil and setup per 100-card lot) and **$4 test/label/ESD bag/CoC**, so **$22 of the $85.50 2MB COGS** [ESTIMATE]. Assembly is **~26% of COGS** here, against ~1% for a DRAM module (01_LANDSCAPE F3). At these volumes, U.S. assembly costs real money but is affordable.
- **Certification** [ESTIMATE/UNVERIFIED]:
  - A memory-card subassembly needs **no UL listing or FCC authorization** for U.S. sale. CE and RoHS are needed only to sell into the EU.
  - The EMS line should follow ANSI/ESD S20.20.
  - Industrial temperature (−40 to 85 °C) comes from part grade.
  - Removing the lithium cell **removes lithium-metal battery shipping rules**, a small logistics advantage.
- **Origin claims.** Say "Assembled in USA" only, under the FTC all-or-virtually-all standard (A-09; 01_LANDSCAPE §10.3 rule 6). The Toggle die is U.S.-fabbed, but its package origin is unknown.

---

## 4. Q4: Channels and pricing power

| Channel | Evidence | Role in model |
|---|---|---|
| **MRO/surplus resellers**: Memex, MRO Electric, Do Supply; Radwell (Willingboro NJ) [UNVERIFIED] | Memex is out of most capacities ([Memex](https://memex.ca/?p=596)). MRO Electric runs Fanuc SRAM exchange ([MRO Electric](https://www.mroelectric.com/product/A20B-2900-0531)). Do Supply lists a Fanuc 2MB card ([Do Supply](https://www.dosupply.com/automation/fanuc/other/DISKMF32M1LCDA7)) [REPORTED] | 40% of card units in BASE at a 30% discount; 65% in scale path S1 |
| **Federal reseller channel** (CDW-G) | CDW-G sells Synchrotech SRAM cards at $239.39 and lists Synchrotech PC cards as **TAA compliant** ([CDW-G](https://www.cdwg.com/product/synchrotech-sram-pcmcia-memory-pc-cards-replaceable-battery-flash-memory/5006798); [CDW](https://www.cdw.com/product/synchrotech-srx-series-flash-memory-card-4-mb-pc-card-taa-compliant/9204293)) [REPORTED] | U.S. assembly with U.S. or Japanese die is TAA-clean, and §5949-clean (Everspin, Infineon and RAMXEED are not CXMT/YMTC/SMIC). This is a modest differentiator, not a moat |
| **eBay / own web store** | The eBay comps above; forum threads on CNCzone and Practical Machinist; IMD-style how-to blogs drive search | 60% of units in BASE; CAC $30 per store card order; eBay fee 13.6% [ESTIMATE] |
| **DMSMS / DLA** | DIBBS is DLA's RFQ portal ([DLA](https://www.dla.mil/Portals/104/Documents/SmallBusiness/DIBBS%20Solicitations%20-%20With%20Notes.pdf)). 5962 memory microcircuits are bought by NSN with approved-source lists ([HigherGov](https://www.highergov.com/nsn/5962012622185/)) [REPORTED]. **No NSN for DS12xx-class demand was found** | Two $24k/yr LTSAs from months 27 and 33 in BASE [ESTIMATE]. Form-fit-function substitution needs program engineering approval, typically 12–24 months |
| **CNC repair and retrofit shops** | MRO Electric is one. Others were not searched | They are resellers and the validation partners who own the controls on their benches |

---

## 5. Q5: The C-16 PLP kit

**Who designs PLP into SSD and RAID boards?**
- **Controller vendors.** Phison announced 1Gb STT-MRAM support ([eeNews](https://www.eenewseurope.com/en/phison-memory-controllers-to-support-1gbit-mram/)). Sage paired its controllers with Everspin 1Gb ([ECD](https://embeddedcomputing.com/technology/storage/sage-microelectronics-and-everspin-partner-to-bring-spin-transfer-torque-mram-to-next-generation-enterprise-ssd-devices)).
- **In-house teams.** IBM FlashCore: FCM3 used up to 128MB of Toggle, FCM4 the 1Gb PERSYST, and FCM5 uses MRAM instead of capacitors ([Blocks & Files 2026-10-05](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966)).
- **RAID.** Dell and LSI/Avago use Everspin in some RAID controllers, per secondary coverage ([Blocks & Files 2019](https://blocksandfiles.com/2019/05/14/everspin-ibm-u-2-flash-drives-mram/)).
- **Industrial SSD makers with their own PLP.** Swissbit PowerSafe ([EFY](https://www.electronicsforu.com/news/new-products/swissbit-introduces-powersafe-a-power-loss-protection-system-for-industrial-ssds)) and Apacer CorePower ([SOS](https://www.soselectronic.com/en-us/articles/apacer/apacer-corepower-your-valuable-data-deserves-top-tier-protection-3065)) [REPORTED].
- Samsung's enterprise drives use tantalum capacitors ([Samsung](https://image-us.samsung.com/SamsungUS/b2b/resource/2016/07/08/b2b_resource_WHP-SSD-POWERLOSSPROTECTION-r1-JUL16J.pdf)).

**Does IBM FlashCore use MRAM?** Yes, in FCM3, FCM4 and FCM5 [REPORTED].

**Everspin reference design?** None found in this search or in Phase 3's. This gap is the only argument for the kit.

**ITC 337-TA-1487:**
- Instituted 2026-02-27 ([USITC](https://www.usitc.gov/press_room/news_release/2026/er0227_68226.htm)).
- Avalanche asserts 37 claims from 4 patents ([Avalanche](https://www.avalanche-technology.com/itc-institutes-investigation-into-everspin-technology-based-on-avalanche-claims-of-patent-infringement/)).
- The ALJ's order extending the **target date to 2027-08-16** was left unreviewed on 2026-08-26 ([USITC](https://www.usitc.gov/sites/default/files/secretary/fed_reg_notices/337/337_1487_notice08262026sgl.pdf)) [REPORTED-P].
- An exclusion order would hit the imported STT parts (1Gb, xSPI) that the PLP kit needs. **The C-12 card is built on Toggle and is insulated.**

**Computed economics** (model §[7]). A DRAM-less design swaps 2GB of DRAM plus $12 of supercaps for 512MB of STT-MRAM ($410):

| Scenario | DRAM $/GB | DRAM + caps saved | MRAM premium per board | p(paid design-in by m36) | Option EV (cost $50k) |
|---|---|---|---|---|---|
| BASE | $18.33 | $49 | **$362** | 0.32 | **−$44.8k** |
| GLUT | $8.15 | $28 | **$382** | 0.19 | **−$47.0k** |
| SEVERE | $2.04 | $16 | **$394** | 0.11 | **−$48.3k** |

The glut moves the per-board gap by only $20–33. MRAM is bought for reliability, and the controller vendors decide where it goes. It takes ~3.1 paid design-ins at $40k and 40% GM just to recover the $50k option. **Licensing value is close to zero:** we would own no IP, and Everspin or the controller vendor can publish the same design. **Verdict: defer C-16. Run only the zero-cost interest test in §8.**

---

## 6. Q6: First ten customers (by name or precise type, and where to find them)

| # | Customer | Type | Why they buy | Where to find them |
|---|---|---|---|---|
| 1 | **Memex Inc.** | Fanuc-card reseller (Ontario) | Most capacities out of stock; "hard to get" ([Memex](https://memex.ca/?p=596)) | memex.ca sales; white-label or wholesale |
| 2 | **MRO Electric** | Fanuc repair/exchange house | Already sells Fanuc SRAM modules on exchange with a 2-year warranty ([MRO Electric](https://www.mroelectric.com/product/A20B-2900-0531)) | Their product pages and RFQ form |
| 3 | **Do Supply** | MRO surplus reseller | Lists a Fanuc 2MB SRAM card ([Do Supply](https://www.dosupply.com/automation/fanuc/other/DISKMF32M1LCDA7)) and Mitsubishi Q2MEM-2MBS ([Do Supply](https://www.dosupply.com/automation/mitsubishi/melsec-q/Q2MEM-2MBS)) | Vendor onboarding |
| 4 | **Radwell International** [UNVERIFIED for this product] | East Coast MRO/repair giant | Catalogs obsolete automation parts | Vendor program |
| 5 | **U.S. job shops running Fanuc 0/16/18/20/21 or i-A controls** | End user | Parameter loss on battery failure; the CF workaround is rejected | Threads such as CNCzone [421202](https://www.cnczone.com/forums/fanuc/421202-fanuc-16ia-sram-memory-card-backup.html); Practical Machinist; >20,000 U.S. job shops |
| 6 | **Fanuc robot maintenance teams (RJ-2/RJ-3)** at Tier-2 auto and metal-fab plants | End user / integrator | Backups need a compatible SRAM card ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-rj-2-pcmcia-sram-memory-card-compatibility-guide)) | Robot integrator forums; local integrators |
| 7 | **MELSEC-Q plant maintenance** (Q2MEM-1MBS/2MBS users) | End user | Silent data loss without the battery ([Mitsubishi](https://mitsubishielectric.co.jp/fa/document/technews/plc/t30-0007/t300007.pdf)) | eBay Q2MEM buyers; Mitsubishi integrators |
| 8 | **Test and measurement calibration and repair labs** (HP/Agilent 3458A DS1230) | End user | Open 3458A FRAM adapters exist ([OSH Park](https://oshpark.com/shared_projects/GCTJUxu1)), but labs need tested parts with a CoC | xDevs/EEVblog communities; independent cal labs |
| 9 | **Federal and defense buyers via CDW-G-type resellers** | Reseller / government | Synchrotech cards are sold there, and TAA status is screened ([CDW-G](https://www.cdwg.com/product/synchrotech-sram-pcmcia-memory-pc-cards-replaceable-battery-flash-memory/5006798)) | CDW-G and GSA reseller vendor onboarding |
| 10 | **DLA Land & Maritime and depot DMSMS engineers** | Government | Obsolete NVSRAM in legacy boards | DIBBS NSN searches ([DLA](https://www.dla.mil/Portals/104/Documents/SmallBusiness/DIBBS%20Solicitations%20-%20With%20Notes.pdf)); GIDEP; DMSMS conference |
| (alt) | **Arcade, pinball and retro restorers** | Hobby | The DS1225/DS1230 crowd. Price-capped by free adapters and Glitch Works (~$30) | Tindie, KLOV and Pinside forums |

C-16 interest targets, for an email-only test: Swissbit, Apacer, Sage Microelectronics and Phison. Teledyne HiRel resells Everspin PERSYST to mil/aero from 4Q-2026 (C-16 card evidence).

---

## 7. Q7: Is there a path beyond ~$0.5M/yr? (model §[6b])

| Path | Run-rate at m36 | Recurring ARR at m36 | 36-mo net | Founder full-time | Share of global card demand |
|---|---|---|---|---|---|
| S0 BASE | $196k | $56k | $79k | never | 4% |
| S1 + white-label in 3–4 MRO catalogs | $293k | $58k | $163k | never | 8% |
| S2 + DMSMS/OEM program (4 LTSAs) | $292k | $152k | $110k | never | 4% |
| S3 + adjacent form factors (cards ×1.5) | $258k | $60k | $132k | never | 6% |
| **S4 stretch (all of the above, cards ×3)** | **$521k** | **$180k** | $158k | **month 22** | **12%** |

**Honest cap.** The hardware tops out at **~$0.2–0.3M/yr realistically and ~$0.5M/yr at a stretch**. That needs ~12% of worldwide PC-card SRAM replacement demand plus four DMSMS contracts.

The global market is ~$3M/yr [ESTIMATE]. It shrinks as legacy controls retire, and every battery-free unit sold removes a future replacement. The only route past ~$0.5M/yr is to turn the "continuity" customer list into a software business: backup vaults, battery and obsolescence tracking for whole fleets of legacy controls. That is a different company, it competes with DNC/MDC vendors (not researched, [UNVERIFIED]), and BASE puts it at only $8k ARR by month 36. **The scorers' "low-$100ks side SKU" call holds.**

---

## 8. The kill experiment (<$10k, <30 days)

Three tracks run in parallel from day 1.

| Track | What | Cost | Kill criterion |
|---|---|---|---|
| **A. Demand** | Landing page and store listing for an "NV-CARD 2MB/4MB battery-free SRAM card for Fanuc and Mitsubishi Q", with a **$25 refundable deposit** and a 120-day ship date. $600 of search ads on part-number terms ("fanuc sram card", "Q2MEM-2MBS", "Q2MEM-2MBSN", "DS1245 replacement"). Posts on CNCzone and Practical Machinist. **20 emails and calls** to Memex, MRO Electric, Do Supply, Radwell, CDW-G's Synchrotech category and five local CNC repair shops, asking for a **wholesale LOI at $175/card, MOQ 10** | ~$1.2k | **<15 deposits AND <2 reseller LOIs → kill as a venture** (keep at most as a hobby SKU) |
| **B. Technical** | Buy a used Fanuc 16i/18i/21i or 0i-A control, or rent bench time at a local CNC repair shop, plus a used MELSEC-Q CPU and a PC-card reader. Have 10 bare 0.8mm PCBs made offshore; buy 6× MR4A16B from distributor or broker stock, plus LVC buffers. Reuse **shells from 3–5 used SRAM cards** ($20–50 each on eBay) so no frame-kit MOQ is needed. Hand-build 3–5 cards. **Tests:** Fanuc boot-menu SRAM backup and restore; ALL-I/O punch to card; card format; Mitsubishi format plus parameter write; 100 power cycles with verify; 72-hour read/write soak; confirm no battery alarm from BVD strapping | ~$5.5k (control $2.5k, parts and PCBs $0.8k, donor cards $0.2k, contract EE $2k) | **Any target control rejects the card** (CIS/attribute or timing) and a ≤$5 CPLD fix does not cure it → kill that family. **Both Fanuc and Mitsubishi fail → kill C-12** |
| **C. Supply** | RFQs for 250× MR4A16B (price and lead time), PC Card frame kits (MOQ and price from ITT and other kit makers), and a 100-card U.S. EMS build quote | $0 | Landed 2MB **COGS above $120**, or frame-kit **MOQ above 1,000 / price above $20** → reprice to ≥$299 or kill |
| **C-16 interest** | Email Swissbit, Apacer, Sage and Phison application engineering: "Would you pay $40k for a validated MRAM-PLP design-in package?" | $0 | Fewer than 2 "yes, send terms" replies → C-16 stays dead |

**Total: ~$6.7k, with ~$3k contingency**, inside $10k. The 30-day risk is MR4A16B stock: DigiKey showed 0 units, and Mouser had 5 of the 45ns variant. If no MRAM arrives within 7 days, prototype on FM28V100 or MB85R8M1 for the *compatibility* test only, and log that timing results do not transfer.

---

## 9. Regulatory, funding and IP facts

- **§5949 (from 2027-12-23):** every core part is from Everspin, Infineon or RAMXEED, none of which is CXMT, YMTC or SMIC. A one-line supplier certification on the CoC matches the proposed rule's self-certification safe harbor (FAR Case 2023-008 is still *proposed*, 2026-02-17). This is worth something in the CDW-G channel; it is not a moat (01_LANDSCAPE §0 item 8).
- **TAA:** U.S. assembly with U.S. or Japanese die is TAA-clean. Chinese-assembled clones are not (CDW screens TAA, as cited above).
- **ITC 337-TA-1487:** target date 2027-08-16. It affects C-16 (STT parts), not C-12 (Toggle).
- **IP:** there is no patent moat. The defensible asset is a **compatibility-validation database** of which control, firmware and card attribute combinations work. Free open designs exist for DIP parts. Do not clone Fanuc boards such as the A20B-2900-0531.
- **SBIR/STTR:** reauthorized through 2031-09-30, but the founder cannot be PI while keeping the day job. It is not needed: this is a T0 business. DLA or Navy DMSMS topics could fund a mil-temperature qualification later, with a full-time PI [UNVERIFIED topic availability].
- **CHIPS, §48D, IonQ/SkyWater, ChipFoundry, wafer.space:** irrelevant, because there is no custom silicon. Fab 25 Austin, a historical alternate F-RAM fab, is now SkyWater/IonQ.

---

## 10. Single biggest risk

**The ceiling, not feasibility.** Worldwide PC-card SRAM replacement demand is about **$3M/yr and declining** [ESTIMATE], and the product kills its own replacement cycle. The business can never fund a full-time founder without ~10% of global demand. The near-term risk, which the kill experiment checks, is whether Fanuc and Mitsubishi controls accept an MRAM card and buyers pay ~$249 when used battery cards sell for $160–440.

## 11. Open gaps (ranked)

1. **Control compatibility:** whether legacy Fanuc and Mitsubishi Q hosts read CIS/attribute memory, check BVD battery pins, or impose timing that a 35ns MRAM behind LVC buffers fails. *Bench test only.*
2. **PC Card frame kit and connector supply:** MOQ and price unknown; at least one connector is Last Time Buy.
3. **Real volumes:** no seller publishes unit volumes, and the TAM chain is ESTIMATE on one REPORTED anchor (5M Fanuc CNCs). Track A is the substitute.
4. **Okuma, Mazak, Heidenhain and Haas** memory-card usage: no evidence found.
5. **Memex, Do Supply and Radwell pricing and margins:** fetches failed. The listed hosts need allowing.
6. **Infineon EXCELON and FM18W08 fab site**, and the MR4A16B package and assembly site, both needed for any "U.S.-fabbed die" claim.
7. **DLA demand for DS12xx form-fit-function parts:** no NSN found.
8. **A Japanese-market battery-free FRAM PC card** may exist [UNVERIFIED].
9. **DNC/backup software competitors** (Memex MERLIN, CIMCO, Predator and similar) for the cloud line [UNVERIFIED, not searched].
10. **C-16:** whether any Everspin application note already covers PLP (everspin.com is blocked).
