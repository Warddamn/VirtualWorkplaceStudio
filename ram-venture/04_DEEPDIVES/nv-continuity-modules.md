# DD3: Drop-in Non-Volatile Continuity Modules

**Slug:** `nv-continuity-modules` · **As of:** 2026-11-01 · **Author agent:** `p4w-nv-continuity-modules`
**Phase 5 red team:** 25 objections answered by `p5r-nv-continuity-modules` (§14; `research/phase5/responses_nv-continuity-modules.json`). **FINAL STATUS: KILLED** (revised after red team). Numbers marked "(revised after red team)" come from the re-run model; `python3 models/nv-continuity-modules.py --phase4` reproduces the Phase 4 numbers.
**Inputs:** `models/nv-continuity-modules.py` (re-run 2026-11-01 after the red team, exit 0; output in `research/phase4/nv-continuity-modules_model_output.md`) · `research/phase4/nv-continuity-modules_notes.md` · `research/phase2/concepts_master.json` (C-12, C-16) · `research/phase3/scores_raw/*.json` · `scores.csv` · `01_LANDSCAPE.md`
**Evidence grade.** Every external fact comes from a search-result snippet (the research agent's fetches failed DNS), so nothing is `[VERIFIED]`. `[REPORTED-P]` = primary page seen via snippet. Model outputs are `[ESTIMATE]` and cite e.g. `model §[5]`.

---

## 0. Header

**Pitch (revised after red team).** A battery-free **backup card** for legacy controls that still need a PC Card "SRAM" card: mainly pre-i Fanuc CNCs (Series 15, 16/18-A/B/C, 20/21-B) and RJ-2 robots, plus a residual share of early i-series. It is built on U.S.-fabbed Everspin Toggle MRAM, validated on the real controls and assembled at a U.S. contract manufacturer. It replaces the lithium-backed backup *card*. It does not replace the control's internal battery-backed SRAM, and it does not prevent the loss event; it makes the backup that recovers from it more reliable (RT-VC-DD3-01). On i-series controls a ~$20 CompactFlash card in an adapter already does the boot-menu backup (RT-VET-DD3-01).

*Phase 4 pitch, kept for the record:* "Battery-free drop-in replacements for the battery-backed memory in legacy CNC, PLC, robot and instrument controls... plus DIP NVSRAM modules built on Infineon F-RAM." The DIP leg and the C-16 option were **killed** in Phase 5 (§14).

| Field | Value |
|---|---|
| **Anchor** | **C-12** Battery-free NV-cache / NVSRAM-replacement modules (T0) |
| **Folded in** | **C-16** Supercap-Killer MRAM PLP kit (T1). Phase 4 carried it as a deferred option; **killed in Phase 5** (RT-PHY-DD3-07: hold-up energy is still needed for in-flight NAND programs unless the FTL changes, and the founder owns no FTL) |
| **Why folded** | Same competence (boards plus validation) and the same lifecycle axis: "F-RAM replaces battery-backed SRAM, and MRAM replaces PLP supercaps" (`03_SCORING.md` §7.3). The scorers kept C-16 small. Founder: "worth a cheap test, not the core of a venture." VC: "Real mechanism in the wrong slot of the value chain." The veteran's C-12 warning, "watch the F-RAM /CE-latch timing trap", is why the card uses Toggle MRAM (§1). |
| **Capital tier** | **T0 on paper, T1 in practice (revised after red team).** BASE peak cash need is **$49.2k**: the cash low is **−$9.2k at m13**, which is above the $40k deployable (A-03). Phase 4 had $29.2k. The new costs are qualification, the connector lifetime buy and the later launch (model §[0], §[5]). A lean re-plan keeps the low at +$3.7k (peak need $36.3k) but still loses $22.4k over 36 months (model §[6]). |
| **TRL** | 9 for the parts: Everspin MR4A16B Toggle MRAM ships ([DigiKey, 2026](https://www.digikey.com/en/products/detail/everspin-technologies-inc/MR4A16BYS35/4021237)) [REPORTED-P]. The card itself is about TRL 4 until it is shown working on a pre-i control. It also has three open engineering risks that the red team found (revised after red team): magnetic immunity (datasheet Hmax_write 8,000 A/m ≈ 10 mT, RT-PHY-DD3-01), hot removal during a write (RT-PHY-DD3-05), and 8-bit byte-lane steering (RT-PHY-DD3-04). The F-RAM DIP leg is dropped (RT-VET-DD3-03). |
| **"Better than RAM" axis** | **Non-volatility and lifecycle, not $/GB.** At $42 per 2MB chip, MRAM costs **$21,504/GB**, about 1,056× the $20.37/GB DDR5 contract price (model §[1]; `models/dram_cost_stack.py`). It wins only where the alternative is a lithium-backed SRAM card or a sealed Dallas NVSRAM whose cell eventually dies and takes the machine's parameters with it. |

**Scores (`scores.csv`, Phase 3; not re-scored here):**

| ID | Default | Capital-constrained | Moonshot | tech / capital / ttr / usmfg / margin / moat / comp / reg / cycle / founder |
|---|---|---|---|---|
| C-12 | **80.0 (#2)** | **82.5 (#2)** | **75.0 (#6)** | 5 / 5 / 4 / 3 / 3 / 2 / 3 / 5 / 5 / 4 |
| C-16 | 66.0 (#19) | 67.5 (#18) | 63.3 (#18) | 5 / 4 / 2 / 3 / 3 / 2 / 3 / 3 / 3 / 3 |

The #2 rank comes from a rubric with no market-size criterion (`03_SCORING.md` §6, blind spot #1, which uses C-12 as its example). All three scorers called it a side business. Founder: "a profitable side business, not a venture." VC: "good cash, not a company anyone should raise for."

### Three verdicts (revised after red team)

| Question | Phase 4 | **Revised after red team** | One line |
|---|---|---|---|
| **POSSIBLE?** | YES | **YES, conditionally** | The parts are TRL 9 and nothing in the physics kills the card (PHY). It still needs dual-supply translators, a CPLD that is now mandatory, power-fail gating and a magnetic shield, and none of these is proven. No pre-i Fanuc control has accepted an MRAM card yet. |
| **PROFITABLE?** | MARGINAL | **NO** | BASE 36-month net is **−$29.8k**. Year nets are −$33.5k, −$0.6k and +$4.4k. Breakeven comes at m19 and the founder is **never** paid. Run-rate is **$29.4k at m18 and $39.9k at m36**; recurring ARR is $2.7k. The addressable card market is about **$0.62M/yr** (2,591 cards/yr), down from the $2.97M "global" figure. A 36-month cumulative breakeven needs **33 cards/month**, 30% of revised U.S. demand. Even a demand-validated 40/month case nets only **$13.3k** over 36 months. |
| **DOABLE BY THIS FOUNDER?** | YES | **PARTLY** | The work still fits: a contract EE, a U.S. EMS, a web store and a compatibility database. Two things changed. The full plan needs ~$49k of peak cash, more than the $40k available. And a qualification programme (outside-lab ESD and temperature tests, three control families, a CNC-service support retainer) adds cost and fixed overhead with no matching revenue. |

**Portfolio role (revised after red team).** Phase 4 called this the **FALLBACK**. It is now **dropped (KILLED)**. Two legs died outright: the F-RAM DIP leg (/CE-latch timing) and C-16. The card leg loses money in BASE, GLUT and SEVERE. It can be reopened only through the $1.2k demand probe in §10, and the founder should spend no hardware money until that probe passes.

---

## 1. How it works (for a smart non-engineer)

A 1990s Fanuc CNC lathe (Series 0, 16, 18, 20 or 21) knows how to cut accurately because of thousands of stored numbers: tool offsets, axis parameters, error compensation, the ladder program. They sit in memory that forgets everything without power, so a small battery keeps it alive. If that battery dies during a shutdown, the settings are gone, and getting the machine back can take days of a service engineer's time.

The usual insurance is a backup card: a credit-card-sized **PC Card (PCMCIA) "SRAM card"** that the technician plugs in and copies everything onto. That card keeps its own data alive with a **lithium battery inside it**. Three problems follow:
- **It fails silently.** Mitsubishi warns that an SRAM card without its battery "may not raise a battery error" and loses its data at power-off ([Mitsubishi, T30-0007](https://mitsubishielectric.co.jp/fa/document/technews/plc/t30-0007/t300007.pdf)) [REPORTED-P].
- **The cheap substitute is refused, but only on older controls.** Older Fanuc controls reject CompactFlash in an adapter ([IMD](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-2021-parameter-backup-via-pcmcia-sram-card)) [REPORTED]. *(Revised after red team.)* On i-series controls (0i, 16i, 18i, 21i), boot-menu SRAM backup to CF in an adapter is a documented routine ([IMD 0i-Mate CF procedure](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-oi-mate-parameter-backup-to-compactflash-procedure)) [REPORTED]. The remaining i-series need is partial: normal-mode I/O on an 18i-T, and one 16iA user's CF format NMI ([CNCzone](https://www.cnczone.com/forums/fanuc/421202-fanuc-16ia-sram-memory-card-backup.html)). The SRAM card is the documented medium on 16-B/C and 18-B/C ([Memex manual](https://memex.ca/wp-content/uploads/M100741G-Fanuc-16-18-Memory-Upgrade-Manual.pdf)) [REPORTED-P].
- **New cards are scarce.** A reseller calls them "hard to get" ([Memex](https://memex.ca/?p=596)) [REPORTED].

**The product replaces the backup card's battery and SRAM with memory that remembers without power.** It does not touch the control's internal battery-backed SRAM (revised after red team, RT-VC-DD3-01).

```
   Legacy control's PC Card slot (68 pins, 5 V signals)
              |
   +----------v-------------------------------------------------+
   | dual-supply translators (74LVC16T245-class) 5 V <-> 3.3 V  |
   | small CPLD: 8-bit byte-lane steering, REG# decode, E/W     |
   |   gating on power-fail + supervisor + hold-up cap  [P5]    |
   | Ni-Fe foil magnetic shield over the MRAM            [P5]   |
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
- **The cost:** a 3.3V chip on a 5V bus needs level translation. *(Revised after red team, RT-PHY-DD3-04/05.)* Single-supply 74LVC16245 parts drive only ~3 V onto the host bus, so the card uses dual-supply translators. A small CPLD is now mandatory: it does the PC Card 8-bit byte-lane steering from the ×16 MRAM, decodes attribute memory, and holds E and W high while VCC collapses. The logic line goes from $5 to **$9**, and a **$3 magnetic shield** is added (model §[0]).
- **Magnetic limit (added after red team).** MR4A16B is rated to Hmax_write = 8,000 A/m (~10 mT) (Everspin datasheet Rev 11.7 and AN02049, via reviewer snippets) [REPORTED-P]. A magnetic dial-indicator base, tool strip or chuck reaches hundreds of mT at contact. A lithium SRAM card does not care about magnets, so this is a new failure mode the product introduces. §10 tests it, and §11 kills the card line if a shielded card fails at 30 mT or after 60 s on a 0.3 T base.

**Second product: DIP modules (KILLED in Phase 5).** Old instruments, controllers and arcade boards use Dallas DS1225/DS1230/DS1245 chips with a lithium cell sealed inside. Phase 4 planned a small board carrying Infineon FM18W08 F-RAM (5V-capable, $12.87) for the same socket. Free open designs exist ([PCBWay](https://www.pcbway.com/project/shareproject/Dallas_DS1230Y_DS1235YW_NVRAM_FRAM_Replacement_Adapter_79f70ace.html)) [REPORTED]. *(Revised after red team.)* The F-RAM latches the address on /CE falling and needs ~130 ns cycles, which is the same /CE trap that moved the card to MRAM. The FM28V100 version adds translator delay. F-RAM's destructive reads also wear out hot rows when the chip is used as working RAM. The originals (DS1230Y, DS1245Y) are still listed in ADI production ([ADI DS1245Y](https://www.analog.com/en/products/ds1245y.html); [ADI DS1230Y](https://www.analog.com/en/products/DS1230Y.html)) [REPORTED-P]. A redesign on a true asynchronous core cannot be sold at $34. The leg is dropped (RT-VET-DD3-03, RT-PHY-DD3-02/03).

**Who builds what.** A contract EE designs the board and a U.S. EMS assembles it. The founder builds the store, the compatibility database (which control, firmware and card combinations are proven) and an optional cloud vault for backup files. There is no chip design. The CPLD equations are the only "firmware" (revised after red team).

**The folded option (C-16)** applies the same idea inside SSDs: an MRAM journal replaces the DRAM cache and its hold-up supercapacitors, as in IBM's FlashCore Modules ([Blocks & Files, 2026-10-05](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966)) [REPORTED]. *(Revised after red team, RT-PHY-DD3-07.)* In MLC, TLC and QLC NAND, an interrupted upper-page program can corrupt lower-page data. So hold-up energy, or a paired-page-aware FTL, is still needed. IBM owns its FTL; a kit vendor does not. **C-16 is killed** (§2.7).

---

## 2. Cost and unit-economics model

All numbers come from `models/nv-continuity-modules.py` unless another source is cited. The model has a 36-month horizon, month 1 = 2026-11, $40k start cash, and a part-time founder with no salary until trailing operating profit reaches at least $12k/month. **Every table below is revised after red team** (model §[0] lists each changed input with its objection id). The Phase 4 values appear in brackets or in "Phase 4" columns; `--phase4` reproduces them.

### 2.1 Unit economics (BASE; model §[1]) (revised after red team)

Net revenue is blended across channels: 25% eBay, 35% own store, and 40% resellers at a 30% discount. The DIP rows are dropped because that leg was killed (RT-VET-DD3-03).

| SKU | List | Net rev/unit | COGS | GM | Fees+CAC+ship+warranty | Contribution | Contrib. % |
|---|---|---|---|---|---|---|---|
| NV-CARD 2MB (1× MR4A16B) | $249 | $219.12 | **$95.50** [$85.50] | 56% [61%] | $40.25 [$33.67] | **$83.37** [$99.95] | 38% [46%] |
| NV-CARD 4MB (2× MR4A16B) | $349 | $307.12 | **$141.50** [$131.50] | 54% [57%] | $49.94 [$40.73] | **$115.68** [$134.89] | 38% [44%] |
| ~~NV-DIP 256Kb (FM18W08)~~ | $34 | $32.64 | $23.00 | 30% | $10.88 | −$1.24 | −4%. **KILLED** |
| ~~NV-DIP 1Mb (FM28V100)~~ | $59 | $56.64 | $35.00 | 38% | $13.97 | $7.67 | 14%. **KILLED** |

**2MB COGS stack ($95.50, revised after red team):**
- MRAM $42.00 (44%), between $37.67 @1k ([Future](https://www.futureelectronics.com/p/memory--RAM--nvram/mr4a16bcys35r-everspin-technologies-6114651)) and $46.03 qty 1 ([DigiKey](https://www.digikey.com/en/products/detail/everspin-technologies-inc/MR4A16BYS35/4021237)) [REPORTED-P]
- Frame kit and connector **$15** [$12] `[ESTIMATE: no current-production card-side quote found; Hirose IC1K is Last Time Buy (Cytech); RT-HYP-DD3-03, RT-VET-DD3-04]`
- PCB $4.50 `[ESTIMATE]`
- Logic **$9** [$5]: dual-supply translators, a mandatory CPLD, a supervisor and a hold-up cap `[ESTIMATE; RT-PHY-DD3-04/05]`
- Magnetic shield **$3** [new] `[ESTIMATE; RT-PHY-DD3-01]`
- U.S. EMS assembly $14, setup $4 and test/pack/CoC $4 `[ESTIMATE]`

The warranty and returns allowance doubles from 3% to **6%** of revenue (RT-VC-DD3-06). **Blended card contribution is $91 [$109].**

### 2.2 Revenue, run-rate and recurring ARR (model §[5]) (revised after red team)

| Scenario | Run-rate m12 (2027-10) | m18 (2028-04) | m24 (2028-10) | m36 (2029-10) | Recurring ARR m12 / m18 / m24 / m36 |
|---|---|---|---|---|---|
| BASE | $7.6k | **$29.4k** [$121.7k] | $42.6k | **$39.9k** [$195.8k] | $0 / $0.4k / $1.3k / **$2.7k** [$56.2k] |
| GLUT | $7.3k | $28.0k | $40.5k | $37.9k [$186.0k] | $0 / $0.4k / $1.2k / $2.6k |
| SEVERE | $5.9k | $22.5k | $32.6k | $30.5k [$153.9k] | $0 / $0.3k / $1.0k / $2.1k |

"Run-rate" is that month's revenue × 12, from repeat hardware purchases with no contract behind them. "Recurring ARR" is cloud-vault MRR plus LTSA monthly × 12.

**The recurring line is now honest and almost empty.** The two assumed $24k/yr DMSMS blanket orders are out of BASE (RT-VC-DD3-04). Two searches, in Phase 4 and Phase 5, found no NSN or DLA award history for DS12xx or PC Card SRAM. The LTSAs survive only in scale paths S2 and S4. BASE recurring ARR at m36 is the cloud vault alone: **$2.7k**. **The founder's recurring-revenue goal is not met.**

The m36 run-rate is below m24 because demand decays 10%/yr after launch. That rate is ~6% for retirement of pre-i controls plus ~4% because each battery-free card removes a future 8-year replacement (RT-HYP-DD3-02) [ESTIMATE].

### 2.3 Breakeven, cash low point and 36-month totals (model §[4b], §[5]) (revised after red team)

| Scenario | Breakeven month | Cash low | Cash m18 | Cash m36 | 36-mo revenue | 36-mo net | Founder full-time |
|---|---|---|---|---|---|---|---|
| BASE | **19 (2028-05)** [11] | **−$9.2k (m13, 2027-11)** [$10.8k] | −$6.1k | $5.2k | $72.1k [$310.9k] | **−$29.8k** [$79.1k] | **never** |
| GLUT | 19 | −$8.5k (m13) | −$5.8k | $5.5k | $68.5k | −$29.8k | never |
| SEVERE | 22 | −$8.2k (m14) | −$6.9k | −$1.5k | $55.2k | −$36.9k | never |

**First revenue** now comes in **month 11 (2027-09)** [m4]. The DIP leg that supplied revenue from m4 is gone, and card launch slips from m9 to **m11** (RT-VET-DD3-05, RT-PHY-DD3-06). The slip comes from validation on a pre-i control, a three-family bench, outside-lab ESD/temperature/insertion tests and a rev-B respin before the first 100-card lot. The month is still within the 18-month first-revenue window.

**Net by year in BASE:** −$33.5k, then −$0.6k, then +$4.4k [Phase 4: −$17.8k / +$34.3k / +$62.6k] [ESTIMATE: model `simulate` summed by year]. Steady-state monthly net is ~$350–380: **about $6 per part-time hour in year 3.** The negative cash low means the full plan needs ~$49k, above the $40k deployable.

### 2.4 Sensitivity (BASE, one variable at a time; model §[6]) (revised after red team)

| Case | Breakeven | Cash low | Run-rate m18 | Run-rate m36 | Rec. ARR m36 | 36-mo net |
|---|---|---|---|---|---|---|
| **Baseline (revised)** | 19 | −$9.2k | $29.4k | $39.9k | $2.7k | **−$29.8k** |
| Price −30% | never | −$14.1k | $20.6k | $27.9k | $1.9k | −$49.1k |
| Price +30% | 16 | −$8.7k | $38.3k | $51.9k | $3.5k | −$10.4k |
| Price ×0.8 (RT-HYP-DD3-04) | never | −$9.7k | $23.5k | $31.9k | $2.2k | −$42.7k |
| Conversion −30% | never | −$10.0k | $20.6k | $27.9k | $1.9k | −$38.4k |
| Conversion +30% | 17 | −$8.7k | $38.3k | $51.9k | $3.5k | −$21.2k |
| Volume ×0.5 (RT-HYP-DD3-02) | never | −$11.1k | $14.7k | $19.9k | $1.4k | −$44.1k |
| COGS −30% | 17 | −$4.4k | $29.4k | $39.9k | $2.7k | −$20.5k |
| COGS +30% | never | −$13.9k | $29.4k | $39.9k | $2.7k | −$39.0k |
| Card launch +6 months | 25 | −$12.6k | $7.7k | $41.4k | $2.2k | −$35.2k |
| Copycat from m24, price ×0.75 (RT-VC-DD3-05) | never | −$9.2k | $29.4k | $30.6k | $2.7k | −$39.2k |
| + 2 LTSAs from m27/m33 (upside only) | 19 | −$9.2k | $29.4k | $87.9k | $50.7k | −$15.8k |
| No demand decay | 19 | −$9.2k | $31.3k | $49.4k | $3.1k | −$25.9k |
| Connector LTB at MOQ 1,000 sets | 19 | −$18.9k | $29.4k | $39.9k | $2.7k | −$29.8k |
| No LTB (two live connector sources found) | 19 | −$3.8k | $29.4k | $39.9k | $2.7k | −$28.9k |
| DIP line restored as in Phase 4 | 20 | −$10.2k | $53.3k | $63.8k | $2.7k | −$32.7k |
| Lean re-plan (partner benches, lab $4k, 50-card lots) | 20 | **+$3.7k** | $29.4k | $39.9k | $2.7k | −$22.4k |
| **Demand-validated: 40 cards/mo** (Phase 4 volume, revised costs) | 14 | −$16.1k | $73.6k | $99.7k | $6.8k | **+$13.3k** |

**Volume now decides this business, ahead of price.** Every revised case at the BASE volume loses money. Breaking even over 36 months takes **33 cards/month**, which is 15% of the addressable market and 30% of revised U.S. demand (model §[8f]). Even at Phase 4's 40/month, the revised costs leave **$13.3k** over 36 months, with a year-3 net of ~$29k.

### 2.5 Market ceiling and scale paths (model §[3], §[6b]) (revised after red team)

**TAM chain** [ESTIMATE on one REPORTED anchor; revised after red team, RT-VET-DD3-01, RT-VC-DD3-02/03, RT-HYP-DD3-01, RT-VET-DD3-06]:
- 5M cumulative Fanuc CNCs ([Metalworking News, 2022](https://metalworkingnews.info/fanuc-reaches-cnc-production-milestone-of-5-million/)) × 15% in the U.S.
- **Pre-i controls** (CF-rejecting): × 15% [Phase 4: 35%, which included i-A] × 40% still running [50%] = **45,000 machines**
- **i-series residual:** × 20% i-A/early-i × 60% running × 20% residual SRAM-card need = **18,000 machine-equivalents**
- = **63,000 U.S. machines** [131,250], ÷ 8 per shop = 7,875 shops
- One card per shop every 8 years, × 1.35 for other families [1.5; Mitsubishi cut per FA-A-0184] = **1,329 cards/yr in the U.S.** [3,076]
- **Addressable (SAM)** = U.S. × 1.10 (Canada) + 15% of non-U.S. demand reachable through eBay and web if the card is EAR99 [ESTIMATE, unconfirmed] = **2,591 cards/yr ≈ $0.62M/yr** [Phase 4 treated $2.97M "global" as the market]
- Global, for information only: U.S. ÷ 0.15 = 8,859 cards/yr ($2.14M/yr). Phase 4's ×4.0 contradicted its own 15% U.S. share (RT-VC-DD3-03).

**BASE assumes 16 cards/month** [40]: 7% of SAM and 14% of U.S. demand, decaying 10%/yr. Phase 4's 40/month would be 19% of SAM and 36% of U.S. demand.

| Path | Run-rate m36 | Rec. ARR m36 | 36-mo net | Full-time month | Share of SAM |
|---|---|---|---|---|---|
| S0 BASE (no LTSA) | $39.9k | $2.7k | −$29.8k | never | 7% |
| S1 + white-label in 3–4 MRO catalogs (cards ×2) | $71.2k | $3.2k | −$7.4k | never | 15% |
| S2 + 4 DMSMS/OEM LTSAs (upside only) | $183.9k | $146.7k | $15.2k | never | 7% |
| S3 + adjacent form factors (cards ×1.5) | $59.8k | $4.1k | −$15.4k | never | 11% |
| **S4 stretch (all, cards ×3)** | **$257.9k** | $155.9k | $69.4k | **never** [m22] | **22%** |

No path pays the founder a salary any more. S4 needs 22% of the addressable market plus four defense contracts nobody has found.

### 2.6 What must be true (model §[8], plus judgment) (revised after red team)

1. **Part-time breakeven:** **11 cards/month** [8] cover the **$1,025/month** [$900] of fixed opex. That opex is tools, insurance at $250/month, bookkeeping, marketing and a $150/month CNC-service retainer. BASE sells 10 cards/month at m18.
2. **36-month cumulative breakeven** needs **33 cards/month**: 15% of SAM, 30% of U.S. demand.
3. **A founder salary** ($120k/yr) needs **121 cards/month: 56% of SAM.** It is not achievable.
4. **Controls accept the card.** A **pre-i** Fanuc (16-C/18-C or 21-B) must read, write, format and restore with no battery alarm, in both 8-bit and 16-bit access. *Untested.* The i-series and Mitsubishi Q are secondary (RT-VC-DD3-02, RT-VET-DD3-06).
5. **The card survives shop magnets.** A shielded card must keep its data at 30 mT and after 60 s on a 0.3 T magnetic base. *Untested;* the datasheet guarantees only 8,000 A/m.
6. **Buyers pay ~$249 for a battery-free backup card** when used battery cards sell for $160–440 ([eBay listings, 2026](https://www.ebay.de/itm/306136207868)) [REPORTED]. Deposits count only at full list with no discount code (RT-HYP-DD3-04).
7. **Supply holds.** Either two current-production card-side connector and frame sources, or a funded lifetime buy. The model holds **350 sets at $15 ($5.2k at m9)** (model §[0b]). MR4A16B lead time must stay at or under 26 weeks.

### 2.7 C-16 PLP kit option (model §[7]) (revised after red team: KILLED)

The kit would replace 2GB of DRAM plus hold-up capacitors with 512MB of STT-MRAM costing $410 ([LCSC, 2026](https://www.lcsc.com/product-image/C20342497.html)). RT-PHY-DD3-07 changes the capacitor side of that swap. Hold-up energy is still needed to finish or abort in-flight NAND programs (the paired-page problem) unless the FTL changes. So only ~$4 of the $12 capacitor BOM is removable [ESTIMATE].

| Scenario | DRAM $/GB | MRAM premium/board | p(paid design-in by m36) | Option EV (cost $50k) |
|---|---|---|---|---|
| BASE | $18.33 | $370 [$362] | 0.32 | **−$44.9k** |
| GLUT | $8.15 | $390 [$382] | 0.16 | −$47.5k |
| SEVERE | $2.04 | $402 [$394] | 0.06 | −$49.0k |

**Verdict: C-16 killed.** The value accrues to whoever owns the FTL, such as IBM with FlashCore, and the founder owns none. The 1Gb STT part is also the target of ITC 337-TA-1487. The $0 email interest test is dropped as well.


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

**Revised after red team:**
- **#1 Memex and #2 MRO Electric:** the ask changes from "wholesale at $175, MOQ 10" to **an exclusive white-label supply agreement of ≥200 cards/yr for 2 years**, or an LOI of ≥100 cards/yr. A MOQ-10 wholesale offer shows the cost structure to the most likely copier and locks nothing (RT-VC-DD3-05).
- **#5:** the target is **pre-i** controls (15, 16/18-A/B/C, 20/21-B). i-A owners count only as a residual market (RT-VET-DD3-01).
- **#7 MELSEC-Q:** narrowed to QnH/QnUD CPUs that use SRAM-card file registers. High-speed Universal QCPU users were pointed to SD cards ([Mitsubishi FA-A-0184](https://mitsubishielectric.com/fa/document/technews/plc/fa-a-0184/faa0184.pdf); RT-VET-DD3-06).
- **#8 cal labs:** dropped with the DIP leg.
- **#10 DLA:** upside only. No NSN demand was found (RT-VC-DD3-04).
- **C-16 targets:** dropped.

---

## 4. Go-to-market

> **Revised after red team.** These GTM changes apply only if the §10 reopen probe passes:
> - DIP pricing and listings are void; that leg is killed.
> - Deposits count only at full list ($249/$349) with no discount code (RT-HYP-DD3-04).
> - Reseller onboarding asks for an exclusive white-label commitment, not MOQ-10 wholesale (RT-VC-DD3-05).
> - Vendor onboarding needs a $1–2M product-liability certificate (~$250/month), a short quality manual and an RMA process ($1.5k one-time). Terms of sale limit liability to the purchase price (RT-HYP-DD3-05).
> - The pitch is "a battery-free backup card", not "save your machine" (RT-VC-DD3-01).
> - Card launch is m11 (2027-09), not m9.
>
> The tables below are the Phase 4 plan, kept for the record.

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

**Revised after red team.** A Phase 5 search again found no battery-free PC Card SRAM product ([Memex](https://memex.ca/?p=596); [Radiolocman on chip-level FRAM](https://www.radiolocman.com/news/new.html?di=514081)) [REPORTED]. So the gap is real, but it is not a moat. A copycat entering at m24 at 75% of our price takes BASE 36-month net from −$29.8k to −$39.2k (model §[6]; RT-VC-DD3-05).

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
| **Bootstrap from $40k (A-03)** | Phase 4: peak need $29.2k; kill test ~$6.7k. **Revised after red team:** peak need **$49.2k** in BASE (cash low −$9.2k), or $36.3k on the lean re-plan. The only spend authorised now is the **$1.2k reopen probe** (§10) | **Only the probe.** The full plan does not fit $40k without the lean re-plan, and it loses money in BASE |
| **SBIR/STTR** | Reauthorized to 2031-09-30 ([UW Federal Relations, 2026-04-14](https://www.washington.edu/federalrelations/2026/04/14/trump-signs-sbir-sttr-reauthorization-bill-into-law/)). **The SBIR PI must spend more than half their time employed by the small business** ([NIST](https://www.nist.gov/tpo/small-business-innovation-research-program-sbir/resources/participation-eligibility-and)), **which excludes this founder while they keep the day job.** STTR needs a university partner, which is absurd for a product with no research in it | **No.** A DLA or Navy DMSMS topic could fund mil-temperature qualification later, only with a full-time PI [UNVERIFIED topic availability] |
| **CHIPS, §48D, state programs** | No silicon and no capex; state programs mostly multiply SBIR (`01_LANDSCAPE.md` §7.1) | **No** |
| **Equity** | Scorers: "good cash, not a company anyone should raise for" (VC) | **Never raise for C-12 alone.** Reconsider only if the S4 stretch path plus a software vault shows >$0.5M run-rate with >30% recurring revenue [ESTIMATE] |
| **Supplier terms or a small inventory line** | Inventory peaks at ~$15.6k in Phase 4. Revised: ~$10.7k first lot plus a $5.2k connector lifetime buy (model §[0b]) | Ask the EMS and distributor for net-30 once there are 3 months of order history [ESTIMATE] |

---

## 8. 18-month roadmap with milestones

Month numbers follow the model (m1 = 2026-11). Each gate is pass/fail on the date shown.

> **Revised after red team.** This roadmap runs only if the §10 reopen probe passes (decision 2026-11-30). The changes are:
> - No DIP launch at m4.
> - Q2 validation moves to a **pre-i** control (16-C/18-C or 21-B), with i-A and Mitsubishi Q secondary.
> - A qualification block runs m6–m8 before the first lot: ≥10 rev-B cards on ≥3 families or firmware revisions, ≥1,000 power cycles at 0–55 °C, outside-lab IEC 61000-4-2 ±8 kV, insertion life, magnetic exposure (§10) and ≥500 hot removals.
> - The first lot is ordered m10 and **card launch is m11**.
> - G3 becomes "pre-i family passes the full protocol; cash ≥$5k with the lean re-plan".
> - G5 (m12) becomes "≥10 cumulative cards".
> - G7 (m18) becomes "run-rate ≥$60k". That is below the demand-validated case ($73.6k) and above BASE ($29.4k), so BASE fails G7 by design.
>
> The table below is the Phase 4 plan, kept for the record.

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
| **Contract EE** (PC Card layout, dual-supply translators, attribute memory, **mandatory** CPLD for byte steering and power-fail gating; revised after red team) | m1 (kill test, $2k) and m2–4 (rev A) | People who already ship DS12xx drop-ins (Glitch Works on Tindie); designers of the 3458A FRAM adapter in the xDevs and EEVblog communities; retired Fanuc field-service engineers active on CNCzone and Practical Machinist | $9k card + $1.5k rev-B respin; DIP design dropped (revised after red team; model §[0]) |
| **Bench and validation partner** (Fanuc and Mitsubishi controls) | m1–6 | Buy a used control (budget $2.5k), or rent bench time at a CNC repair house; MRO Electric is customer #2 and a natural partner. Fallback: a local community-college CNC program [ESTIMATE] | $2.5k one-time |
| **U.S. EMS** | m5 (prototype), m8 (first lot) | MacroFab, Houston, with real-time online quotes ([MacroFab](https://macrofab.com/index.php)); Screaming Circuits, best on runs of 25+ ([PICList, 2008](https://pic.hallikainen.org/piclist/2008/a/01/29/165504a.txt)); Rush PCB on the East Coast, IPC-A-610, location unverified ([Rush PCB](https://rushpcb.com/?p=839)) | $14 + $4 + $4 per card (in COGS) |
| **Bookkeeper and insurance** | m4 onward | Local small-business bookkeeper; product-liability policy with a $1–2M COI | $350/month (revised after red team, was $225; model §[0]) |
| **Part-time fulfilment help** | Only on the S1 path (>100 orders/month) | Local hourly help or a 3PL | Not in BASE [ESTIMATE ~$500/month if needed] |
| **DMSMS business-development advisor** | m24+, only if pursuing LTSAs | Retired DLA or NAVSUP DMSMS engineers, on commission | Not in BASE [ESTIMATE: commission only] |

**Revised after red team:**
- **CNC field-service technician on retainer**, $150/month from launch, to handle compatibility tickets (RT-VC-DD3-06).
- **Outside test lab**, $7.5k at m8, for ESD, temperature and insertion life (RT-VET-DD3-05).
- **Bench time on two more control families**, $3k at m6 (RT-PHY-DD3-06).
- **QMS manual and RMA process**, $1.5k at m7 (RT-HYP-DD3-05).
- The DIP designer ($1.5k) is dropped.
- Product-liability insurance rises to ~$250/month.

BASE never hires an employee: the founder plus ~$10.5k of contract engineering ($9k card + $1.5k rev-B respin, revised after red team; model §[0] `one_time`; the probe-stage $2k EE fee is part of the $9k, pulled forward), plus the retainer and the outside lab listed above.

---

## 10. The cheapest experiment that could kill it (revised after red team: now a reopen probe)

**Status change.** Phase 4 planned a $6.7k, 29-day, three-track experiment. After the red team the concept is **KILLED** in BASE (§14), so that experiment is not authorised. What remains is a **demand-only reopen probe**. The founder runs it only with spare capacity after the PRIMARY pick, and it involves **no hardware spend**. The technical and supply tracks run only if the probe passes. Thresholds are fixed now, before any data.

**Step 1: Reopen probe (~$1.2k, 28 days; day 0 = 2026-11-02, decision 2026-11-30)** [ESTIMATE: $600 ads + landing page, store and deposit-processing setup]
1. Day 1–3: landing page for "NV-CARD 2MB/4MB battery-free backup card". It names the target controls: Fanuc 15, 16/18-A/B/C, 20/21-B and RJ-2, with i-series for normal-mode I/O only. Prices are $249/$349 with a **$25 refundable deposit at full list and no discount codes** (RT-HYP-DD3-04). Target ship date is **2027-09** (model m11).
   - The deposit form records control model and firmware.
   - It also asks what the buyer would otherwise buy: a used battery card at $X, a new Synchrotech card, CF, or RS-232/DNC (RT-VC-DD3-01).
2. Day 3–28: $600 of search ads on "fanuc sram card", "fanuc 16-C/18-C memory card" and "RJ-2 sram card", plus CNCzone and Practical Machinist posts. Mitsubishi terms are tracked separately and limited to QnH/QnUD users (RT-VET-DD3-06).
3. Day 3–20: 20 emails and calls to Memex, MRO Electric, Do Supply, Radwell, CDW-G's Synchrotech category manager and five CNC repair shops.
   - **Ask:** an exclusive white-label supply agreement of ≥200 cards/yr for 2 years, or an LOI of ≥100 cards/yr at ≥$175 (RT-VC-DD3-05).
   - **Also ask:** each reseller's annual sell-through of SRAM cards (RT-HYP-DD3-02, RT-VC-DD3-03).

| Probe result (fixed now) | Action |
|---|---|
| **REOPEN:** (≥30 deposits at full list, no more than 1/3 from i-series owners, AND ≥1 reseller LOI ≥100 cards/yr at ≥$175) **OR** a signed white-label commitment ≥200 cards/yr × 2 yrs **OR** reseller-reported North-American sell-through ≥1,000 SRAM cards/yr plus ≥15 full-list deposits | Re-run the model at the evidenced volume. Go to step 2 only if the re-run 36-month net is >$0 on the lean re-plan |
| Anything less | **Stays killed.** Refund deposits. No hardware spend |

The 30-deposit bar exists because 36-month breakeven needs 33 cards/month (model §[8f]); 15 deposits no longer signal enough.

**Step 2: Technical (only after REOPEN; ~$6k: pre-i control $2.5k, parts and PCBs $0.8k, donor shells $0.2k, contract EE $2k, gaussmeter and test magnets $0.3k)**
1. Bench target: **a pre-i Fanuc (16-C/18-C or 21-B) first**, then an i-A, then Mitsubishi QnH (RT-VET-DD3-01, RT-VC-DD3-02).
2. Rev-A design (RT-PHY-DD3-04/05):
   - dual-supply translators (74LVC16T245-class) and a CPLD for 8-bit byte-lane steering, REG# decode and E/W gating
   - a supervisor and hold-up capacitor
   - a Ni-Fe foil shield inside the 3.3 mm Type I envelope
3. Functional tests:
   - boot-menu SRAM backup and restore
   - ALL-I/O punch
   - format
   - **8-bit and 16-bit access**
   - 100 power cycles with verify
   - 72-hour soak
   - no battery alarm with BVD strapped
4. **Magnetic tests (replacing Phase 4's "72 h beside a spindle motor"; RT-PHY-DD3-01, RT-VET-DD3-02, RT-HYP-DD3-06):**
   - calibrated exposure at 10, 30 and 100 mT, in standby and during write, with a full-array CRC
   - 5 cards, shielded and unshielded: each face held 60 s against a 0.3 T dial-indicator base, then verify
   - 10 cycles on a surface-grinder magnetic chuck, then verify
5. **Hot removal (RT-PHY-DD3-05):** ≥500 removals during active writes, with CRC of every non-addressed block.

**Step 3: Supply (only after REOPEN; $0)**
- Written quotes from **two current-production card-side 68-pin connector and frame sources**, or one lifetime-buy quote of ≤500 sets at ≤$20 landed (RT-HYP-DD3-03, RT-VET-DD3-04). Phase 5 found only an LTB Hirose part, an obsolete FCI part, a broker-stocked 3M part and a TE "assemblies with frames" page of unknown status.
- MR4A16B: 250-piece price and lead time.
- A 50- or 100-card U.S. EMS quote.

**Step 4: Qualification before the first lot (m6–m10; ~$12k: bench $3k, lab $7.5k, respin $1.5k).**
- ≥10 rev-B cards on ≥3 control families or firmware revisions
- ≥1,000 power cycles at 0–55 °C
- outside-lab IEC 61000-4-2 ±8 kV contact on shell and pins, plus insertion life
- the Step 2 magnetic and hot-removal tests repeated on rev-B (RT-PHY-DD3-06, RT-VET-DD3-05)

**C-16 interest test: dropped** (C-16 killed, RT-PHY-DD3-07).

| Test | PASS | FAIL → action |
|---|---|---|
| Reopen probe (2026-11-30) | Thresholds above | **Stays killed** |
| Technical (pre-i) | Pre-i Fanuc passes every functional test after a ≤$5 CPLD fix | **Kill the card line.** Mitsubishi or i-A alone is too small |
| Magnetic | Shielded card: zero bit errors at 30 mT standby and after 60 s on a 0.3 T base | Fails either → **kill the card line**. Fails only on chuck contact → launch with a label and a warranty exclusion |
| Hot removal | Zero corruption outside the addressed word in 500 removals | Fix in rev-B; still failing at rev-C → **kill** |
| Supply | Two live connector sources, or LTB ≤$20 at ≤500 sets | **Kill.** The $299 reprice path is dropped: price ×1.2 still loses $16.9k in BASE |

**Cash effect.** Only the $1.2k probe is spent unless the probe passes. Phase 4's ~$6.7k experiment and its $9.4k cash-low estimate are void.

---

## 11. Explicit kill criteria (revised after red team)

0. **Phase 5 decision (2026-11-01): KILLED in BASE.** The revised BASE loses $29.8k over 36 months and needs $49.2k of peak cash. Reopen only through criterion 1.
1. **2026-11-30:** reopen-probe thresholds not met (§10) → stays killed; no hardware spend. *(Phase 4: <15 deposits AND <2 LOIs, 2026-12-01.)*
2. **Technical, after reopen:** a pre-i Fanuc (16-C/18-C/21-B) rejects the card (format, read, write, restore, or 8-bit access) after a ≤$5 CPLD fix → kill the card line. *(Phase 4: Fanuc i-series or Mitsubishi Q.)*
3. **Magnetic, after reopen:** a shielded card loses any bit at 30 mT standby, or after 60 s on a 0.3 T magnetic base → kill the card line. *(New.)*
4. **Hot removal, after reopen:** any corruption outside the addressed word in 500 hot removals that a rev-C does not fix → kill. *(New.)*
5. **Supply, after reopen:** no two current-production card-side connector and frame sources, and no LTB quote ≤$20 landed at ≤500 sets → kill. The reprice-to-$299 path is dropped. *(Phase 4: reprice and re-test.)*
6. **MR4A16B:** order not confirmed for delivery by 2027-09-30, and no alternative core passes timing → slip launch. A slip past m14 → re-run the model; the launch +6 months case loses $35.2k, so stop. EOL/LTB notice or lead time >40 weeks with no validated alternative core within 90 days → stop new lots and sell through.
7. **Qualification gate (before the first lot, m10):** compatibility failure on the 3-family / 1,000-cycle bench >3%, or an ESD failure at ±8 kV contact → no first lot. *(New; RT-PHY-DD3-06, RT-VET-DD3-05.)*
8. **Cash, any month:** <$5k → halt all non-inventory spend. The lean re-plan is mandatory after a reopen, because the full plan's cash low is −$9.2k. Cash <$0 is not allowed → wind down. *(Phase 4: <$5k halt, <$3k wind down.)*
9. **2027-12-31 (m14):** <25 cumulative cards (the demand-validated case expects 33) or <2 active reseller accounts → kill the card line.
10. **First 100 cards shipped:** compatibility returns >5% → stop sales until fixed; >10% → kill. *(Phase 4: 10% / 20%; tightened per RT-VC-DD3-06.)*
11. **Any month:** realized blended card price <$175 for 3 consecutive months, or a battery-free copy listed at <75% of our price → exit (RT-VC-DD3-05).
12. **2028-04-30 (m18):** run-rate <$60k → wind down. The demand-validated case reaches $73.6k; BASE reaches only $29.4k. *(Phase 4: <$85k freeze, <$60k wind down.)*
13. **C-16 and the DIP leg:** killed in Phase 5 (RT-PHY-DD3-07; RT-VET-DD3-03, RT-PHY-DD3-02). Reopen the DIP leg only with a true-async core (Toggle MRAM or nvSRAM) and a published list of ≥10 passing hosts, including one with /CE tied low and one cycling at ≤100 ns, at a price that covers the translators.


---

## 12. Cycle test: 2028–29 glut (DDR5 −60%) and severe (−90%)

The DRAM decks come from `models/dram_cost_stack.py` `ddr5_reference()`: shortage $20.37/GB, glut $8.15/GB, severe $2.04/GB. Glut and severe ramp in over 2028-H1 (m15–20); BASE eases 10% over 2028 (m15–26).

| Metric (revised after red team) | BASE | GLUT (−60%) | SEVERE (−90%) |
|---|---|---|---|
| Breakeven month | 19 [11] | 19 [11] | 22 [12] |
| Cash low | −$9.2k (m13) [$10.8k] | −$8.5k (m13) [$11.6k] | −$8.2k (m14) [$12.2k] |
| Run-rate m18 / m36 | $29.4k / $39.9k [$121.7k / $195.8k] | $28.0k / $37.9k [$115.6k / $186.0k] | $22.5k / $30.5k [$93.1k / $153.9k] |
| 36-mo net | −$29.8k [$79.1k] | −$29.8k [$79.0k] | −$36.9k [$49.3k] |
| Cash m36 | $5.2k [$103.5k] | $5.5k [$104.9k] | −$1.5k [$77.4k] |
| C-16 MRAM premium/board | $370 [$362] | $390 [$382] | $402 [$394] |
| C-16 option EV | −$44.9k (killed) | −$47.5k | −$49.0k |

**The core still passes the glut test, but it fails the profit test in every scenario (revised after red team).** It sells against lithium cells, never against DRAM, so GLUT ≈ BASE. The scenario drops come entirely from judgment multipliers, not DRAM prices:
- **GLUT:** demand × 0.95 for a capex slowdown, offset by COGS × 0.95 as specialty NVM softens. Net is unchanged at −$29.8k (revised after red team) [$79.0k].
- **SEVERE:** demand × 0.85, price × 0.90 (copycats) and COGS × 0.90. Net falls to −$36.9k (revised after red team) [$49.3k].

A glut may even help slightly, as shops keep legacy controls longer [ESTIMATE].

**The cycle that does threaten this business is the retirement curve, not DRAM.**
The base shrinks yearly, and each battery-free card removes an 8-year replacement. *(Revised after red team, RT-HYP-DD3-02.)* The model now decays card demand by 10%/yr after launch. Removing the decay improves BASE only to −$25.9k, because the main problem is the smaller pre-i market, not the decay rate.

**C-16 gets worse in a glut**, as the scorers predicted. Cheaper DRAM widens the MRAM premium by $20–33 per board and cuts p(design-in) from 0.32 to 0.06 (revised). It is killed (RT-PHY-DD3-07).

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

---

## 14. Red-team outcome

**Phase 5, 2026-11-01, agent `p5r-nv-continuity-modules`.** Four reviewers raised 25 DD3 objections: VET (30-year DRAM process veteran), VC (semiconductor VC), HYP (hyperscaler procurement lead) and PHY (condensed-matter physicist). Each one is answered in full in `research/phase5/responses_nv-continuity-modules.json`. None was deleted, and none could be refuted with evidence.

**Dispositions:** REFUTED 0 · ACCEPTED-MITIGATED 8 · ACCEPTED-DOWNGRADE 14 · ACCEPTED-KILL 3 (the DIP leg, twice, and C-16).

| Objection | Severity | Disposition | Action |
|---|---|---|---|
| RT-HYP-DD3-01 | MAJOR | ACCEPTED-DOWNGRADE | TAM split into pre-i (15%, 40% running) plus an i-series residual (20% × 60% × 20%); U.S. demand 3,076 → 1,329 cards/yr; probe caps i-series deposits |
| RT-HYP-DD3-02 | MAJOR | ACCEPTED-DOWNGRADE | Volume 40 → 16 cards/mo with 10%/yr decay; BASE net +$79.1k → −$29.8k; 36-mo breakeven needs 33/mo |
| RT-HYP-DD3-03 | MAJOR | ACCEPTED-DOWNGRADE | Connector $12 → $15; funded LTB of 350 sets ($5.2k, m9); kill if no two live sources and no LTB ≤$20 at ≤500 sets |
| RT-HYP-DD3-04 | MAJOR | ACCEPTED-MITIGATED | Deposits count only at full list with no discount code; price ×0.8 row (−$42.7k); exit if realized price <$175 |
| RT-HYP-DD3-05 | MINOR | ACCEPTED-DOWNGRADE | Insurance → ~$250/mo; $1.5k QMS and RMA; liability capped in terms of sale (−$5.6k) |
| RT-HYP-DD3-06 | MINOR | ACCEPTED-MITIGATED | Calibrated magnet tests, $3 shield, label and warranty exclusion (see PHY-01) |
| RT-PHY-DD3-01 | MAJOR | ACCEPTED-MITIGATED | 10/30/100 mT tests, 0.3 T base contact, chuck cycles; $3 shield; new kill criterion 3 |
| RT-PHY-DD3-02 | MINOR | ACCEPTED-KILL | F-RAM DIP leg killed (/CE latch, 130 ns cycle, translator delay) |
| RT-PHY-DD3-03 | MINOR | ACCEPTED-MITIGATED | Moot after DIP kill; any revival must use a non-wearing core and exclude working-RAM use |
| RT-PHY-DD3-04 | MINOR | ACCEPTED-MITIGATED | Dual-supply translators and a mandatory CPLD; logic $5 → $9; rev-B respin $1.5k; 8/16-bit tests |
| RT-PHY-DD3-05 | MINOR | ACCEPTED-MITIGATED | Supervisor plus CPLD E/W gating and hold-up cap; ≥500 hot-removal test; kill criterion 4 |
| RT-PHY-DD3-06 | MINOR | ACCEPTED-MITIGATED | ≥10 cards × ≥3 families × 1,000 cycles at 0–55 °C before the first lot; +$3k; launch m9 → m11 |
| RT-PHY-DD3-07 | MINOR | ACCEPTED-KILL | C-16 killed (hold-up energy still needed); capacitor saving $12 → $4; email test dropped |
| RT-VC-DD3-01 | MAJOR | ACCEPTED-DOWNGRADE | Pitch narrowed to "battery-free backup card"; the probe asks for the buyer's alternative |
| RT-VC-DD3-02 | MAJOR | ACCEPTED-DOWNGRADE | Bench target moves to a pre-i 16-C/18-C/21-B; TAM counts CF-rejecting families plus a residual |
| RT-VC-DD3-03 | MAJOR | ACCEPTED-DOWNGRADE | Global multiplier 4.0 → 6.67 (info only); SAM = 1.1 × U.S. + 15% of non-U.S. = 2,591/yr; decay added |
| RT-VC-DD3-04 | MAJOR | ACCEPTED-DOWNGRADE | LTSAs out of BASE (upside S2/S4 only); recurring ARR m36 $56.2k → $2.7k |
| RT-VC-DD3-05 | MAJOR | ACCEPTED-DOWNGRADE | Copycat row (−$39.2k); ask Memex or MRO Electric for an exclusive white-label deal, not MOQ-10 wholesale |
| RT-VC-DD3-06 | MINOR | ACCEPTED-DOWNGRADE | Returns 3% → 6%; CNC-tech retainer $150/mo; returns kill tightened to 5%/10% |
| RT-VET-DD3-01 | MAJOR | ACCEPTED-DOWNGRADE | Same TAM cut as HYP-01; ~$53k of the $109k swing in 36-mo net |
| RT-VET-DD3-02 | MAJOR | ACCEPTED-MITIGATED | Reviewer's 5-card / 0.3 T / 60 s protocol adopted verbatim; shield checked against the envelope |
| RT-VET-DD3-03 | MAJOR | ACCEPTED-KILL | F-RAM DIP leg killed; restoring it makes BASE worse (−$32.7k) |
| RT-VET-DD3-04 | MAJOR | ACCEPTED-DOWNGRADE | Same as HYP-03: LTB 350 sets; written two-source quote required; kill criterion 5 |
| RT-VET-DD3-05 | MAJOR | ACCEPTED-DOWNGRADE | Outside-lab ESD ±8 kV, insertion life and 0–55 °C ($7.5k); launch m11; kill criterion 7 |
| RT-VET-DD3-06 | MINOR | ACCEPTED-DOWNGRADE | Other-families multiplier 1.5 → 1.35; Mitsubishi narrowed to QnH/QnUD and benched third |

### Changes made

**Model** (`models/nv-continuity-modules.py`). A "RED-TEAM REVISIONS (Phase 5)" block lists 26 changed inputs with their old values and objection ids. `--phase4` reproduces Phase 4. The changes:
- **TAM split.** Pre-i 0.15, still running 0.40, plus an i-series residual. Other families 1.35. Global ×6.67 is information only; SAM is 1.1 × U.S. plus 15% of non-U.S.
- **Card demand.** Volume 16/mo with a 10%/yr decay.
- **Legs killed.** DIP volume 0. C-16 capacitor saving $12 → $4, and C-16 is printed as killed.
- **Card COGS.** Logic $9/$10, shield $3, connector $15, and a 350-set connector lifetime buy at m9.
- **Returns and opex.** Returns 6%, insurance $250/mo, CNC-service retainer $150/mo.
- **Launch and one-time costs.** Card launch m11. One-time additions: $7.5k outside lab, $3k bench time on two more families, $1.5k QMS/RMA, $1.5k rev-B respin and $0.3k magnetic test kit. The $1.5k DIP design is removed.
- **LTSAs** are removed from BASE.
- **New code paths:** a demand-decay term, a lifetime-buy cash line, a copycat price step, scale paths relative to the BASE volume, and section [0] with a before/after headline table. The re-run output is in `research/phase4/nv-continuity-modules_model_output.md`.

**Deep dive:**
- §0: pitch narrowed to a battery-free backup card for pre-i controls; verdicts and capital tier revised; portfolio role is now drop.
- §1: i-series CF caveat, revised block diagram, magnetic limit, DIP and C-16 kills.
- §2: every table re-run.
- §3, §4, §5, §7, §8, §9 and §12: revision notes.
- §10: replaced by a $1.2k demand-only reopen probe, followed by the technical, supply and qualification steps only after a reopen.
- §11: 14 revised kill criteria.

### Revised headline economics (re-run model, §[0] and §[5])

| | Phase 4 | **Revised after red team** |
|---|---|---|
| Run-rate m18 BASE | $121.7k | **$29.4k** |
| Run-rate m36 BASE / GLUT / SEVERE | $195.8k / $186.0k / $153.9k | **$39.9k / $37.9k / $30.5k** |
| Recurring ARR m36 BASE | $56.2k | **$2.7k** |
| Breakeven month BASE | m11 | **m19** (GLUT m19, SEVERE m22) |
| Cash low BASE | $10.8k (m6) | **−$9.2k (m13)**: peak need $49.2k > $40k |
| 36-month net BASE / GLUT / SEVERE | $79.1k / $79.0k / $49.3k | **−$29.8k / −$29.8k / −$36.9k** |
| Founder full-time month BASE | never | **never** (no scale path reaches it; S4 was m22 in Phase 4) |
| First revenue | m4 (DIPs) | **m11 (2027-09)**, cards only |
| Volume for 36-month cumulative breakeven | n/a | **33 cards/mo** (BASE 16) |
| Demand-validated case (40/mo, revised costs) | n/a | 36-month net +$13.3k; lean re-plan +$18.9k |

### Revised verdicts

| Question | Phase 4 | Revised after red team |
|---|---|---|
| **POSSIBLE?** | YES | **YES, conditionally.** The parts are TRL 9 and nothing physical kills the card. Still unproven: the magnet tolerance (8,000 A/m rating), hot removal, 8-bit steering, and acceptance by a pre-i Fanuc control. |
| **PROFITABLE?** | MARGINAL | **NO.** BASE 36-month net is −$29.8k and the founder is never paid. Even 40 cards/month nets only $13.3k. |
| **DOABLE BY THIS FOUNDER?** | YES | **PARTLY.** The work fits a part-time founder, but the ~$49k peak cash need does not fit the $40k deployable without the lean re-plan, which still loses $22.4k. |

### FINAL STATUS: **KILLED**

**Reason.** Most of the market was in i-series controls that already take a $20 CF card. Once those are removed, along with the two defense contracts nobody found, the BASE card business loses $29.8k over 36 months, needs more cash than the founder has, and never pays them. The F-RAM DIP leg and the C-16 PLP option each died to a specific technical objection. The card itself is sound but too small. A 36-month breakeven needs 33 cards/month, about 30% of revised U.S. demand, and no evidence supports that.

**What would reopen it.** A $1.2k, 28-day demand-only probe (§10). It reopens on ≥30 full-list deposits (no more than one-third from i-series owners) plus a reseller LOI of ≥100 cards/yr, or on a white-label commitment of ≥200 cards/yr for 2 years. The founder should run it only with spare capacity after the PRIMARY pick.

**Phase 5 sources** (logged in `research/sources/p5r-nv-continuity-modules.jsonl`; all seen via search snippets, 2026-11-01):
- Connectors: [Cytech, Hirose IC1K LTB](https://www.cytechsystems.com/de/product/ic1k-68rd-1.27sfa71); [TE PC Card connectors at TTI](https://www.ttiasia.com/content/ttiasia/en/manufacturers/te-connectivity/products/TE-Connectivity-PC-Card-PCMCIA-Connectors-and-Accessories.html); [AERI, 3M MCH068](https://www.aeri.com/pn/3m/mch068tan07lphtr30); [Rhombus Tech PCMCIA sources (not verified)](https://rhombus-tech.net/pcmcia_sources/)
- Fanuc controls: [Memex 16/18 upgrade manual](https://memex.ca/wp-content/uploads/M100741G-Fanuc-16-18-Memory-Upgrade-Manual.pdf); [CNCzone 16iA thread](https://www.cnczone.com/forums/fanuc/421202-fanuc-16ia-sram-memory-card-backup.html); [IMD 0i-Mate CF procedure](https://industrialmonitordirect.com/blogs/knowledgebase/fanuc-oi-mate-parameter-backup-to-compactflash-procedure)
- MRAM magnetic limit: [MR4A16B datasheet mirror](https://static.chipdip.ru/lib/050/DOC035050573.pdf); [Everspin AN02049](https://www.mouser.lt/pdfDocs/magnetic-field.pdf)
- DIP originals: [ADI DS1245Y](https://www.analog.com/en/products/ds1245y.html); [ADI DS1230Y](https://www.analog.com/en/products/DS1230Y.html)
- Mitsubishi: [FA-A-0184](https://mitsubishielectric.com/fa/document/technews/plc/fa-a-0184/faa0184.pdf)
