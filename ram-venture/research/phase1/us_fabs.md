# Phase 1: U.S. wafer-fab capacity for memory (front end) and U.S. TFT/display capacity

Agent: `p1-fabs` · Written: 2026-11-01 · Sources: `research/sources/p1-fabs.jsonl` · Assumptions: `research/assumptions/p1-fabs.md`
Mission scope: §3A (IGZO: "What U.S. TFT/display capacity actually exists? Could idle or trailing-node silicon fabs run it?") and §3C (map U.S. memory-adjacent capacity, front end only).

> **Evidence warning: read this first.**
> - **No web searches were possible.** My first WebSearch call came back "budget used up": all 200 searches allowed per turn, shared by every agent, were gone before this agent started.
> - **Direct fetches were blocked.** www.everspin.com and www.skywatertechnology.com were refused as outside the session's allowed domains. The proxy log also shows sec.gov, trendforce.com and investors.micron.com refused. Following the tool's instructions, I stopped trying further sites.
>
> So every fact here comes from one of two places:
> 1. **Snippets that other agents logged** (A1, A2, p1-micron). I cross-reference these in my source log with a provenance note and tag them **[REPORTED]**, or **[REPORTED-P]** where the snippet quotes a primary filing.
> 2. **My prior knowledge** (training data through about mid-2026), tagged **[UNVERIFIED]**. These carry a source name and date but no link, because I will not invent URLs.
>
> Nothing is [VERIFIED]. Treat this file as a structured, dated hypothesis map, strong on structure and weaker on post-2025 specifics. §11 lists the 15 re-checks that matter most. If the orchestrator can lift the search cap or allowlist the company domains, re-running those 15 checks would take about 30 searches.

---

## 0. Bottom line (decision-relevant)

1. **No U.S. foundry offers a DRAM process, and no U.S. foundry offers an oxide-semiconductor (IGZO) TFT module.**
   - The only U.S. DRAM wafer capacity belongs to Micron: Manassas Fab 6, which started 1-alpha DDR4/LP4 on 2026-05-22, plus Boise R&D, with ID1/ID2/NY1 under construction. Micron takes no foundry customers ([HPCwire/Micron PR, 2026-05-22](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia)) [REPORTED]; see `phase1/micron_us_makers.md`.
   - The mission's idea of trailing-node DRAM on depreciated 25–40nm U.S. capacity has no host. No U.S. 22–65nm foundry line has a DRAM capacitor module. **[ESTIMATE: absence of any offering in my knowledge or in other agents' logs]**
2. **Everspin's U.S. manufacturing is narrower than the mission premise implies.**
   - Chandler, AZ adds magnetic back-end layers (BEOL) to purchased 200mm CMOS wafers, but only for **Toggle MRAM** (densities up to ~16–32 Mb).
   - All of Everspin's higher-density **STT-MRAM** (256 Mb, 1 Gb, xSPI) is made at **GlobalFoundries Singapore**, its single foundry for those parts ([Everspin FY2025 10-K via A2 snippet](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm)) [REPORTED-P].
   - The next 256 Mb xSPI part is to tape out on **TSMC 16nm** in 2H-2026 ([Q4-25 call via A2](https://www.insidermonkey.com/blog/everspin-technologies-inc-nasdaqmram-q4-2025-earnings-call-transcript-1710559/)) [REPORTED].
   - **New U.S. MRAM capacity** comes from a **10-year Microchip foundry deal**: 200mm wafers at **Fab 4, Gresham OR**, ramping to a maximum of **1,300 wafers/quarter**, first products **2H-2027**. Microchip is contractually barred from making tunnel-magnetoresistance (TMR) devices for Everspin's competitors ([Everspin 8-K, 2026-04-08, via A2](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm)) [REPORTED-P]. **Gresham is closed to an MTJ startup.**
     - *v2 verification (2026-11-01):* the bar runs for the **term plus 2 years** (so to ≥2038). Toggle/sensor flows start ~18 months after signing (~Q4-2027); **STT flows ~30 months (~Q4-2028)**. Everspin reimburses **~$13.95M** of tooling/installation. Process foreground IP goes to Microchip. The term auto-renews in 2-year steps ([8-K](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408.htm); [10-Q Q1-26](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026028464/mram-20260331.htm); both via search snippet) [REPORTED-P].
3. **The only open, qualified U.S. foundry offering for BEOL emerging memory is SkyWater S130 + Weebit ReRAM.**
   - The module is 256 Kb, JEDEC-qualified on 3 lots, rated to 125 °C, in the S130 PDK, at Bloomington MN, a DMEA Trusted Foundry ([Weebit, 2023-06](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/); [SkyWater, 2023-11](https://www.skywatertechnology.com/weebit-nano-reram-ip-achieves-high-temperature-qualification-in-skywater-s130-process/)) [REPORTED].
   - *v2 verification (2026-11-01):* the default macro is 256 Kb, configurable from 128 Kb to 2 Mb ([SkyWater, 2023-03-07](https://www.skywatertechnology.com/weebit-nano-reram-ip-now-available-in-skywater-technologys-s130-process/)) [REPORTED-P].
     - **Prototype access** was through Efabless chipIgnite for a "small fee", with the **production licence signed directly with Weebit** ([StorageNewsletter, 2024-06-05](https://www.storagenewsletter.com/2024/06/05/weebit-nano-and-efabless-collaborate-to-enable-prototyping-of-soc-designs/)) [REPORTED]. That route died with Efabless (early 2025). Whether ChipFoundry carries the ReRAM block is [UNVERIFIED].
     - Weebit's three customer tape-outs (by 2026-07) name **no foundry**. No 2025–26 customer tape-out on S130 was found.
     - **SkyWater has been owned by IonQ since 2026-07-31** (see §2.3).
   - GF's eMRAM (AutoPro150, volume 2H-2026) and its CBRAM/ReRAM run on 22FDX in **Dresden**, not in the U.S. ([GF, 2026-03-09, via A2](https://www.globenewswire.com/news-release/2026/03/09/3251832/0/en/GlobalFoundries-Announces-Availability-of-AutoPro150-eMRAM-Technology-on-Enhanced-FDX-Platform-for-Advanced-Automotive-Applications.html)) [REPORTED].
   - TI licensed Weebit ReRAM in Dec 2025, but only for its own captive use ([Weebit, 2025-12-29, via A2](https://www.weebit-nano.com/news/press-releases/weebit-nano-secures-a-license-agreement-with-texas-instruments/)) [REPORTED]. A broker note puts TI's integration at 28–65nm ([MST, 2025-12-30, via search snippet](https://www.weebit-nano.com/wp-content/uploads/2025/12/251230.-MST-Access_Weebit-signs-Texas-Instruments.pdf)) [REPORTED].
   - onsemi's Weebit licence (2025-01, Treo 65nm BCD) is **confirmed**. As of 2026-07, onsemi was nearing the start of qualification ([Motley Fool AU, 2026-07-31](https://www.fool.com.au/2026/07/31/weebit-nano-lifts-revenue-guidance-on-new-deals-and-chip-tape-outs/)) [REPORTED]. It is captive.
4. **SkyWater roughly tripled its trailing-edge foundry capacity by buying Infineon's Fab 25 in Austin.**
   - Fab 25 is 200mm at 130–65nm, about **400k wafer starts/yr**, roughly 1,000 staff, bought for about **$73M at close + ~$20M working capital**. The deal **closed 2025-06-30**, and Infineon keeps a long-term supply agreement ([LaPedus, 2025, via A1](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm); [SkyWater/BusinessWire, 2025-02-26, via A1](https://www.businesswire.com/news/home/20250226773415/en/SkyWater-to-Acquire-Infineons-Austin-Fab-and-Establish-Strategic-Partnership-to-Expand-U.S.-Foundry-Capacity-for-Foundational-Chips)) [REPORTED].
   - That works out to about **$230 of purchase price per annual wafer start**, a sign of how cheap depreciated U.S. 200mm capacity is [ESTIMATE: $93M / 400k].
   - **SkyWater is the most plausible U.S. host** for a BEOL memory module from a small company (IGZO 2T0C, HZO FeCAP, ReRAM).
5. **There is no Gen-scale LCD, OLED or oxide-TFT panel fab anywhere in the U.S.**
   - Foxconn's Wisconsin Gen 10.5 plan was never built [UNVERIFIED: prior knowledge], and TrendForce's public TFT-capacity data shows no U.S. fabs ([TrendForce abstract, 2026-08, via A1](https://www.trendforce.com/research/download/RP260831UV)) [REPORTED].
   - U.S. display activity is microdisplays (Kopin; eMagin, now Samsung Display, which makes OLED-on-CMOS in Hopewell Junction NY), glass (Corning) and tool R&D (Applied Materials) [UNVERIFIED].
   - **The display-fab-compatible cheap-capital angle for IGZO memory does not exist in the U.S.** IGZO would have to run as a BEOL add-on in a silicon fab.
6. **IGZO BEOL fits a silicon fab's thermal budget, but a 130nm U.S. host gives very low density.**
   - The process is ≤400 °C, uses sputter or ALD, and needs hydrogen control plus segregation of In/Ga/Zn contamination; any 200mm fab with a dedicated PVD chamber and BEOL-only tools can run it.
   - At 130nm, a planar 2T0C array is about **250–490× less dense than DDR5 1b** per tier. At 65nm (Fab 25) it is about **60–120×** less dense [ESTIMATE; `assumptions/p1-fabs.md`].
   - So U.S.-made IGZO memory is an **embedded or niche** product (low standby power, long retention, rad-tolerance), never a $/GB DRAM substitute.
7. **The cheapest real prototype path is a university or national-lab nanofab, at $20–80k for device-level learning** [ESTIMATE].
   - East-Coast options: Cornell CNF, Penn Singh Center, Harvard CNS, NIST CNST NanoFab, Brookhaven CFN, Penn State, RIT SMFL, MIT.nano.
   - Next step up: a SkyWater S130 shuttle plus university BEOL post-processing (~$15–60k per iteration), then a dedicated 130nm mask set at **$500–600k** ([AnySilicon via A1](https://anysilicon.com/130nm-wafer-mpw-cost/)) [REPORTED].
   - Albany NY CREATES (300mm) is real and already hosts HfO2 ferroelectric memory work with Fraunhofer ([IDW, 2025-05-16, via A1](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale)) [REPORTED]. But it is a T1–T2 joint-development engagement, not a T0 path.
8. **An overlooked U.S. asset is magnetic thin-film know-how in Minnesota.** The Seagate Bloomington head-wafer fab (TMR readers are MTJs), NVE (Eden Prairie), Honeywell Plymouth (rad-hard SRAM/MRAM), SkyWater and Polar all sit there, next to the University of Minnesota's MNC nanofab [UNVERIFIED: prior knowledge]. None sells MTJ foundry service, but it is where an MTJ or BEOL team would be recruited.
   - *v2:* UMN is setting up a **Spin Technology Center** with **Polar Semiconductor and Honeywell Aerospace**, led by Jian-Ping Wang ([UMN CSE, via search snippet](https://cse.umn.edu/node/194186)) [REPORTED-P; date not captured]. It is the most concrete spintronics industry-academic node in the U.S.

**Corrections to the mission premise (§1/§3):**
- **(a)** "Everspin (AZ), a U.S. memory company shipping today" is true only for **Toggle MRAM**. Its densest products are Singapore-made.
- **(b)** SkyWater is now **MN + FL + TX**, not "MN/FL".
- **(c)** TI Lehi kept none of its 3D XPoint capability. It runs captive 65/45nm analog/embedded production.
- **(d)** No idle U.S. display fab exists to arbitrage.
- **(e)** Trailing-node DRAM in the U.S. means Micron Manassas or nothing.

---

## 1. Summary table

Legend: **Outside customers** = Yes (open foundry) / Ltd (program or strategic only) / No (captive). Tags apply to the row's key facts.

| Facility | Owner | Wafer size / node | Memory-relevant capability | Outside customers? | Notes / source |
|---|---|---|---|---|---|
| Boise ID: R&D fab + ID1/ID2 (construction) | Micron | 300mm, leading-edge DRAM (1-gamma class R&D) | DRAM R&D; ID1 first wafer mid-CY2027, ID2 late CY2028 | **No** | [Micron 10-K FY2026 via p1-micron](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm) [REPORTED-P] |
| Manassas VA: Fab 6 | Micron | 300mm, 1-alpha DRAM (DDR4/LP4) since 2026-05-22 | **Only U.S. DRAM production** | **No** (sells parts; SpecTek sells wafers, consumer grade) | CHIPS $275M ([NIST PMT](https://www.nist.gov/node/1869301)) [REPORTED-P]; >$2B project ([HPCwire](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia)) [REPORTED] |
| Chandler AZ (inside NXP's fab) | Everspin | 200mm, magnetic BEOL on purchased CMOS | Toggle MRAM (≤16–32 Mb), Chandler foundry services for DoD programs | **Ltd** (DoD program foundry services) | [10-K FY2025 via A2](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm) [REPORTED-P]; co-located at NXP ([SiliconSemi via A2](https://siliconsemiconductor.net/article/123971/Everspin_Technologies_expands_on-shore_MRAM_manufacturing_capacity)) [REPORTED] |
| Gresham OR: Fab 4 | Microchip (for Everspin) | 200mm | MRAM / TMR / STT-MRAM for Everspin; first products 2H-2027 (Toggle/sensor ~Q4-27, STT ~Q4-28); max 1,300 wfr/qtr | **No** for others (TMR exclusivity for the term + 2 years) | [Everspin 8-K 2026-04-08 via A2](https://www.sec.gov/Archives/edgar/data/1438423/000162828026024696/mram-20260408xexx991.htm) [REPORTED-P] |
| Bloomington MN | SkyWater | 200mm, 350–90nm (S130, S90/RH90 FDSOI rad-hard), MEMS, superconducting | **Weebit ReRAM in S130** (qualified); low-temp BEOL precedents (CNFET + RRAM, DARPA 3DSoC) | **Yes** (pure-play foundry, DMEA Trusted Cat 1A; IonQ subsidiary since 2026-07-31) | ReRAM [REPORTED]; IonQ ownership [REPORTED] ([Quantum Insider](https://thequantuminsider.com/2026/07/31/ionq-completes-skywater-acquisition-quantum-manufacturing/)); Trusted status, RH90 and 3DSoC [UNVERIFIED] |
| Austin TX: Fab 25 | SkyWater (from Infineon, closed 2025-06-30) | 200mm, 130–65nm | Cypress/Infineon CMOS heritage; SONOS eNVM know-how [UNVERIFIED]; **smallest-geometry U.S. 200mm pure-play** | **Yes** (converting to foundry; Infineon anchor) | [LaPedus via A1](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm) [REPORTED] |
| Kissimmee FL (Osceola County's Center for NeoVation) | SkyWater (operator; county owns) | 200/300mm advanced packaging (fan-out, interposer) | Packaging of memory chiplets (back end, out of scope) | **Yes** | [UNVERIFIED: prior knowledge] |
| Malta NY: Fab 8 | GlobalFoundries | 300mm, 14/12nm FinFET (12LP/12LP+), 45nm RF-SOI / silicon photonics | No eMRAM/ReRAM in U.S. volume production [UNVERIFIED]; **14HP (IBM) deep-trench eDRAM existed; 2026 status unknown** | **Yes** (Trusted Foundry; DoD 10-yr contract) | [UNVERIFIED] |
| Essex Junction VT: Fab 9 | GlobalFoundries | 200mm, 350–90nm, RF SiGe, GaN-on-Si development | No memory offering of note | **Yes** (Trusted) | [UNVERIFIED] |
| Dresden (for contrast) | GlobalFoundries | 300mm 22FDX / FDX+ | **eMRAM (AutoPro150, 2H-26), CBRAM/ReRAM, FeFET R&D**: not U.S. | Yes | [GF 2026-03-09 via A2](https://www.globenewswire.com/news-release/2026/03/09/3251832/0/en/GlobalFoundries-Announces-Availability-of-AutoPro150-eMRAM-Technology-on-Enhanced-FDX-Platform-for-Advanced-Automotive-Applications.html); [CBRAM via A2](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/); [Fraunhofer via A1](https://www.ipms.fraunhofer.de/en/press-media/press/2026/FAMES-wafer-exchange.html) [REPORTED] |
| Sherman TX: SM1 (+SM2–4 planned) | Texas Instruments | 300mm analog/embedded (~45–130nm) | Captive embedded NVM (FRAM; Weebit ReRAM licensed Dec 2025) | **No** | [Weebit-TI via A2](https://www.weebit-nano.com/news/press-releases/weebit-nano-secures-a-license-agreement-with-texas-instruments/) [REPORTED]; fab status [UNVERIFIED] |
| Richardson TX: RFAB1/RFAB2; Dallas DMOS5/6 | Texas Instruments | 300mm (RFAB), 200mm (DMOS5) | Captive embedded FRAM (MSP430FR) [UNVERIFIED site] | **No** | [UNVERIFIED] |
| Lehi UT: LFAB1 (+LFAB2) | Texas Instruments (bought from Micron 2021) | 300mm, 65/45nm analog/embedded | Former 3D XPoint fab; **XPoint capability not retained** | **No** | $900M sale ([AnandTech via A2](https://www.anandtech.com/show/16800)) [REPORTED] |
| Bloomington MN | Polar Semiconductor | 200mm, power/BCD, high-voltage, magnetic sensors | Little direct memory relevance; a candidate BEOL host | **Yes, emerging** (moving from captive to commercial foundry) | CHIPS ~$123M [UNVERIFIED] |
| Chandler AZ (Fab 52/62), Hillsboro OR (D1X), Rio Rancho NM (Fab 9/11X), Ohio (delayed) | Intel Foundry | 300mm; external: Intel 16, Intel 3, 18A (HVM late 2025), 18A-P, 14A (customer-dependent); 12nm with UMC (2027) | No memory product; eMRAM/ReRAM (22FFL, ISSCC 2019) and BEOL IGZO-TFT/FeRAM **R&D only** | **Yes** (Intel Foundry; RAMP-C for DoD) | [UNVERIFIED]; BEOL-TFT patent ([Google Patents via A1](https://patents.google.com/patent/US11751402)) |
| Rio Rancho NM (inside Intel Fab 11X) | Tower Semiconductor (tools) / Intel (fab) | 300mm, 65nm BCD / RF-SOI | None | **Yes** (via Tower) | ~$300M Tower tool investment, Sept 2023 [UNVERIFIED] |
| Newport Beach CA: Fab 3 | Tower Semiconductor | 200mm, 350–130nm SiGe BiCMOS, RF, silicon photonics | Embedded OTP/MTP NVM only [UNVERIFIED] | **Yes** (MPW program) | [UNVERIFIED] |
| San Antonio TX: Fab 9 | Tower Semiconductor | 200mm, ~180nm power/mixed-signal | None | **Yes** | [UNVERIFIED] |
| Austin TX: S2; Taylor TX | Samsung Foundry | 300mm, 14–65nm (Austin); 2nm (Taylor) | eMRAM (28FDS) is made in Korea, **not Austin** [UNVERIFIED] | **Yes** | Taylor = logic (see `phase1/micron_us_makers.md`) |
| Phoenix AZ: Fab 21; Camas WA: WaferTech | TSMC | 300mm N4/N3 (AZ); 200mm 350–160nm (WaferTech) | No eNVM in AZ; possible legacy eFlash at WaferTech [UNVERIFIED] | **Yes** | [UNVERIFIED] |
| East Fishkill NY | onsemi (from GF, closed 2022-12-31) | 300mm, power / analog (65nm-class BCD) | Ex-IBM site where IBM ran SOI eDRAM; **Weebit ReRAM licensed for onsemi's Treo 65nm BCD (2025-01; confirmed), nearing qualification 2026-07**. Whether Treo runs at East Fishkill is [UNVERIFIED] | **No** (captive) | Licence [REPORTED] ([Motley Fool AU, 2026-07-31](https://www.fool.com.au/2026/07/31/weebit-nano-lifts-revenue-guidance-on-new-deals-and-chip-tape-outs/)); fab [UNVERIFIED] |
| Colorado Springs CO: Fab 5 / Tempe AZ: Fab 2 (closing) | Microchip | 200mm | Captive EEPROM / SuperFlash eNVM | **No** (except the Everspin deal at Fab 4) | Tempe Fab 2 closure announced 2025; CHIPS PMT $162M (Jan 2024) [UNVERIFIED] |
| Chandler AZ (CHD), Austin TX (ATMC) | NXP | 200mm (+150mm GaN in Chandler) | Hosts Everspin's Chandler line | **No** | Long-term 200mm rationalization toward VSMC Singapore 300mm (2027) is a **risk to Everspin's co-location** [ESTIMATE: inference] |
| Beaverton OR, Camas WA, Wilmington MA | Analog Devices | 150/200mm | None (captive analog) | **No** | CHIPS PMT ~$105M (Jan 2025) [UNVERIFIED] |
| Lubbock TX | X-FAB Texas | **150mm**, SiC + legacy Si | None | **Yes** (foundry) | [UNVERIFIED] |
| Roseville CA | Bosch (ex-TSI Semiconductors) | 200mm, converting to SiC | None | **No** | CHIPS PMT up to $225M (Dec 2024) [UNVERIFIED] |
| Marcy NY (Mohawk Valley), Durham NC | Wolfspeed (Ch. 11 June 2025, emerged ~Sept 2025) | 200mm SiC (NY); 150mm SiC (NC, winding down) | None | **No** | [UNVERIFIED] |
| Greensboro NC; Richardson TX | Qorvo | 150mm GaAs / GaN | None (III-V; tolerates In/Ga) | Ltd | [UNVERIFIED] |
| Bloomington MN (Normandale) | Seagate | AlTiC head wafers | **Volume MTJ/TMR sputter + ion-beam etch** (HDD readers) | **No** | [UNVERIFIED: prior knowledge] |
| Eden Prairie MN | NVE Corp. | Spintronic BEOL on foundry CMOS (150/200mm) [UNVERIFIED] | GMR/TMR sensors and isolators; historic MRAM licensor | **No** (product company) | [UNVERIFIED] |
| Plymouth MN | Honeywell Aerospace | 150mm rad-hard SOI CMOS (Trusted) | Rad-hard SRAM; 1–16 Mb rad-hard MRAM products | **Ltd** (DoD) | [UNVERIFIED] |
| Albuquerque NM: MESA | Sandia (DOE/NNSA) | 150mm rad-hard CMOS (~350nm) + III-V; FeRAM work at 200mm scale | **HZO FeRAM integrated into the trusted MESA CMOS flow (2026)** | **Ltd** (CRADA / strategic-partnership projects; *v2: no public HZO licensing listing or CRADA offer found, internal LDRD*) | [Sandia 2026-05-13 via A1](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/) [REPORTED]; access route [UNVERIFIED] |
| Lexington MA: Microelectronics Lab | MIT Lincoln Laboratory | 200mm, 90nm FDSOI, superconducting (Trusted) | 3D integration R&D | **Ltd** (government sponsors) | [UNVERIFIED] |
| Albany NY: NY CREATES / Albany NanoTech | NY CREATES (state non-profit) | 300mm, leading-edge incl. EUV | **HfO2 ferroelectric memory JDA with Fraunhofer IPMS (2025-05)**; Applied Materials META Center | **Yes** (JDA/membership; startups/SMEs) | [IDW via A1](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale); [NY.gov via A1](https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york) [REPORTED] |
| Corvallis OR | HP Inc. | Thin-film MEMS (inkjet) | Thin-film/oxide know-how; no TFT line | **No** | CHIPS PMT ~$50M (2024) [UNVERIFIED] |
| Canandaigua NY | Akoustis (Ch. 11 Dec 2024) | 150mm BAW/MEMS (AlScN PVD) | Sputter-heavy 150mm line; **distressed asset** | n/a | [UNVERIFIED] |
| Newburyport MA | Rochester Electronics | Back end (die bank, re-creation) | Legacy memory continuity (no front end) | **Yes** | Out of front-end scope; [UNVERIFIED] |

---

## 2. Facility notes

### 2.1 Micron: Boise ID and Manassas VA (cross-reference: `phase1/micron_us_makers.md`)
- **Boise ID** has a 300mm R&D fab (where leading-edge DRAM nodes are developed) plus ID1 and ID2. ID1 is to produce its first DRAM wafers mid-CY2027, with meaningful output in 2028. ID2's initial output is late CY2028 ([10-K FY2026 via p1-micron](https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000023/mu-20260903.htm)) [REPORTED-P].
- **Manassas VA (Fab 6)** was formerly Dominion Semiconductor (IBM/Toshiba) and has been Micron's since 2002 [UNVERIFIED: prior knowledge]. Micron began 1-alpha DDR4/LP4 production there on 2026-05-22. The output is aimed at auto, defense, aerospace and industrial buyers ([HPCwire/Micron, 2026-05-22](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia)) [REPORTED]. CHIPS support is up to $275M ([NIST PMT, 2024-12-10](https://www.nist.gov/node/1869301)) [REPORTED-P].
- **What it can do for memory:** everything, but only for Micron.
- **What it cannot do:** take foundry customers. Micron has no foundry business, and its trusted-supplier status for Manassas is [UNVERIFIED].
- **The die path for a small company** is SpecTek (Micron's division that sells wafers and down-binned parts). That is covered by p1-micron.
- **Lehi UT**, the former IM Flash 3D XPoint fab, went to TI in 2021 for $900M cash ([AnandTech via A2](https://www.anandtech.com/show/16800)) [REPORTED]. Micron had taken about $545M in underutilization charges there over four quarters before exiting ([The Register, 2021-03-17, via A2](https://www.theregister.com/2021/03/17/micron_pulls_the_plug_on/)) [REPORTED].

### 2.2 Everspin: Chandler AZ (and now Gresham OR via Microchip)
- **Business model** ([FY2025 10-K via A2](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm)) [REPORTED-P]:
  - Everspin buys base CMOS wafers from foundries.
  - It adds the magnetic BEOL (the magnetic tunnel junction, MTJ, stack plus its patterning) in its own Chandler line.
  - **GLOBALFOUNDRIES Singapore is the single foundry for its higher-density, advanced-node (STT-MRAM) products**, and GF may discontinue supply on notice.
- **Where the line sits:** the Chandler line is co-located inside NXP's Chandler fab ([Silicon Semiconductor via A2](https://siliconsemiconductor.net/article/123971/Everspin_Technologies_expands_on-shore_MRAM_manufacturing_capacity)) [REPORTED]. That is a legacy of Everspin's 2008 spin-out from Freescale [UNVERIFIED: prior knowledge].
- **In-house vs. GF, by product family** (product-to-fab mapping is my inference from the 10-K snippet plus prior knowledge):

| Product family | Density | Cell / process | Where made | Tag |
|---|---|---|---|---|
| Toggle MRAM (parallel/SPI, industrial, aerospace; QML parts via partners) | 128 Kb – 16 Mb (32 Mb as stacked/dual-die) | Field-switched MTJ on ~180/130nm CMOS | **Chandler AZ BEOL on purchased 200mm CMOS** | Location [REPORTED-P]; densities [UNVERIFIED] |
| STT-MRAM DDR3/DDR4-interface (EMD3D256M, EMD4E001G) | 256 Mb (40nm), 1 Gb (28nm) | pMTJ STT on 300mm | **GF Singapore** (front to back) | 1 Gb on GF 28nm ([TechInsights via A2](https://www.techinsights.com/blog/memory/worlds-first-1-gb-28-nm-stt-mram-product-everspin)) [REPORTED]; Singapore [REPORTED-P] |
| PERSYST xSPI STT-MRAM | 64–256 Mb | pMTJ STT, 28nm-class | **GF Singapore** (current); **TSMC 16nm** tape-out for monolithic 256 Mb in 2H-2026 | [REPORTED] ([Q4-25 call via A2](https://www.insidermonkey.com/blog/everspin-technologies-inc-nasdaqmram-q4-2025-earnings-call-transcript-1710559/)) |
| Future MRAM / TMR sensors / STT | n/a | 200mm | **Microchip Fab 4, Gresham OR**: Toggle/sensor from ~Q4-2027, STT from ~Q4-2028 | [REPORTED-P] (8-K, 10-Q via snippet) |

- **Is the Chandler line 200mm only?** I believe yes. Everspin's early 300mm STT development moved to GF in 2014 ([Design-Reuse via A2](https://us.design-reuse.com/news/35789/everspin-globalfoundries-300mm-cmos-wafer-st-mram.html)) [REPORTED]. That Chandler has no 300mm MTJ tooling today is [UNVERIFIED].
- **Outside customers:** limited, through government programs.
  - A $5.26M tranche of a strategic rad-hard FPGA program with QuickLogic used "Chandler 8-inch Toggle production and foundry services" ([BusinessWire, 2024-07-24, via A2](https://www.businesswire.com/news/home/20240724863768/en/Everspin-Announces-Contract-to-Provide-MRAM-Technology-for-Strategic-Radiation-Hardened-FPGA)) [REPORTED].
  - A **$40M, 2.5-year subcontract (Apr 2026)**, reportedly with Amentum, transfers Toggle MRAM process technology and provides engineering and foundry services to establish on-shore Toggle MRAM capability for the defense industrial base ([Electronics360 via A2](https://electronics360.globalspec.com/article/23702/everspin-earns-40-million-mram-deal-for-defense-memory-services); [MRAM-Info via A2](https://www.mram-info.com/everspin-enters-40-million-subcontract-agreement-amentum-establish-us-mram-processes-and)) [REPORTED]. The receiving fab is not named in the snippets [UNVERIFIED].
- **Scale:** Q3-2026 revenue was $20.6M, of which MRAM product sales were $16.9M, at a 51.4% gross margin, with $43.0M cash ([8-K via A2](https://www.sec.gov/Archives/edgar/data/0001438423/000162828026067890/mram-20260930xexx991.htm)) [REPORTED-P]. That is roughly a **$65–70M/yr MRAM product run-rate** [ESTIMATE: 4 × $16.9M]. The whole U.S. discrete-MRAM manufacturing base is a small business.
- **Risk:** the Chandler line depends on NXP keeping its Chandler 200mm fab open. NXP's shift to 300mm at VSMC (Singapore) makes long-term 200mm consolidation plausible [ESTIMATE: inference]. The Gresham deal reads partly as a hedge against that.
- **For American Memory:** Everspin is a possible customer, partner or acquirer for MTJ-adjacent work, not an open foundry. Its Microchip exclusivity closes the only new U.S. 200mm MTJ capacity to others.

### 2.3 SkyWater Technology: Bloomington MN, Austin TX (Fab 25), Kissimmee FL
- **Bloomington MN (200mm).** This is the former Cypress Minnesota fab, sold in 2017 ([Design-Reuse via A1](https://us.design-reuse.com/news/41552/cypress-minnesota-wafer-fabrication-facility-sale.html)) [REPORTED]. It was a U.S.-owned public pure-play foundry (Nasdaq: SKYT, IPO 2021).
  - **Correction (v2, 2026-11-01):** IonQ agreed to buy SkyWater on 2026-01-26 and **closed the ~$1.8B deal on 2026-07-31**. SkyWater shareholders got $15.00 cash + 0.4883 IONQ shares per share, and the FTC granted early termination.
  - SkyWater now runs as a wholly owned IonQ subsidiary under its own name and is no longer separately listed. Its CEO says customer access and IP protections are unchanged.
  - The press has flagged a neutrality concern, but it concerns IonQ's quantum rivals ([Quantum Insider, 2026-07-31](https://thequantuminsider.com/2026/07/31/ionq-completes-skywater-acquisition-quantum-manufacturing/); [Runtime Wire](https://runtimewire.com/article/ionq-closes-skywater-acquisition-ftc-clears-deal-without-conditions)) [REPORTED]. It is still U.S.-owned.
  - **Processes** [UNVERIFIED]: S130 (130nm CMOS, plus the open-source sky130 PDK released with Google in 2020), S90 and the **RH90 rad-hard 90nm FDSOI** (DoD-funded, ~$170M, 2019–20), MEMS, superconducting (D-Wave), ThermaView.
  - **Trust:** DMEA Trusted Foundry, Category 1A [UNVERIFIED].
  - **Memory:**
    - Weebit 1T1R ReRAM is qualified and in the S130 PDK [REPORTED, above]. No 2025–26 *customer* tape-out on S130 is public (v2). The prototype route was Efabless chipIgnite, now defunct, and production use needs a direct Weebit licence.
    - Analyst-estimated Weebit upfront fees run from ~$0.3M (DB HiTek, a foundry) to $1.8–2.6M (onsemi, an IDM). On top come NRE and royalties, which start in CY2027 ([MST, 2025-09-01, via search snippet](https://www.weebit-nano.com/wp-content/uploads/2025/09/250901.-MST-Access-Report_WBT.AX-Not-just-play-money-090125.pdf)) [REPORTED]. A fabless startup's terms are unknown.
    - Under DARPA's 3DSoC program (2018–2023), MIT/Stanford and SkyWater built monolithic 3D chips with carbon-nanotube FETs and **RRAM layered over silicon CMOS at <400 °C** on SkyWater's 200mm line [UNVERIFIED: prior knowledge]. This is the closest U.S. commercial-foundry precedent for a new-material BEOL memory module, and it bears directly on IGZO feasibility.
    - Whether Cypress-heritage SONOS is still offered is [UNVERIFIED].
- **Austin TX, Fab 25 (200mm, 130–65nm).** Bought from Infineon; the deal closed 2025-06-30. The terms were about $73M at close plus ~$20M working capital, about 400k wafer starts/yr and about 1,000 employees. The fab is being converted to a foundry, with Infineon as the anchor customer under a long-term supply agreement ([LaPedus via A1](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm); [Infineon PR via A1](https://new-origin.infineon.com/cms/en/about-infineon/press/press-releases/2025/INFXX202502-066.html)) [REPORTED].
  - Fab 25 was Cypress's main fab for PSoC/SONOS and nvSRAM-class products [UNVERIFIED: prior knowledge]. If the SONOS/eNVM flows are offered to foundry customers, this becomes the **only U.S. pure-play 65nm-class line with embedded charge-trap NVM heritage**. Re-check this first (§11).
- **Kissimmee FL.** SkyWater operates Osceola County's Center for NeoVation for advanced packaging: fan-out wafer-level packaging and interposers [UNVERIFIED]. This is back-end and out of scope, though relevant for memory chiplets.
- **Indiana (West Lafayette).** A $1.8B fab plan announced in 2022 is dormant [UNVERIFIED].
- **CHIPS:** a preliminary memorandum of terms (PMT) of up to ~$16M for Bloomington (Dec 2024) [UNVERIFIED, low confidence]. Final status is unknown.
- **Outside customers:** yes; this is the whole business model.
  - **Shuttles:** the open-source sky130 shuttles ran through Efabless (Google-sponsored Open MPW, then paid chipIgnite at ~$10–15k per ~10 mm² slot). Efabless **shut down in early 2025**, with a successor (ChipFoundry) reported.
    - **Confirmed (v2):** Efabless founders Jeff DiCorpo and Mohammed Kassem launched **ChipFoundry.io**, which restored sky130 open-PDK shuttles.
    - Pricing was reported as rising from $10k to **~$15k per 100 chips**, and a run can slip if it is <50% full ([eeNews Europe, 2025](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)) [REPORTED].
    - Tiny Tapeout's TTSKY26b went on ChipFoundry run CI2605, which closed 2026-05-18 ([Tiny Tapeout](https://tinytapeout.com/chips/ttsky26b/)) [REPORTED-P].
  - **GF180 alternative (v2):** wafer.space (Tim Ansell) runs GF180MCU shuttles.
    - Run 2 costs **$7,000 early-bird / $7,500 standard for a full slot of 1,000 dies**, or $4,000/$4,500 for a half slot. Run 1 was functional ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2); [Tiny Tapeout](https://tinytapeout.com/news/wafer-space-gf180/)) [REPORTED-P].
    - Tiny Tapeout tiles cost ~€70 each on both processes [REPORTED-P].
  - SkyWater's own commercial MPW pricing is not public [UNVERIFIED].
- **Wafer price:** not public. I use **~$1,200–1,600 per 200mm S130 wafer**, consistent with A1 ($1,200) and A2 (S130 + ReRAM ≈ $1,600) [ESTIMATE].

### 2.4 GlobalFoundries: Malta NY (Fab 8), Essex Junction VT (Fab 9)
- **Malta Fab 8 (300mm):** 14LPP/12LP/12LP+ FinFET, plus 45RFSOI and the Fotonix silicon-photonics platform [UNVERIFIED].
- **Essex Junction Fab 9 (200mm):** ex-IBM, 350–90nm, RF SiGe, plus GaN-on-Si development [UNVERIFIED].
- **East Fishkill (Fab 10)** was sold to onsemi; the deal closed 2022-12-31 [UNVERIFIED].
- **Trusted Foundry.** GF U.S. inherited IBM's Trusted Foundry accreditation in 2015. In Sept 2023 the DoD signed a **10-year, ~$3.1B** agreement with GF for securely made chips [UNVERIFIED: prior knowledge]. Malta and Essex Junction are accredited trusted suppliers [UNVERIFIED].
- **Embedded memory offerings and where they are made:**
  - **22FDX eMRAM:** in production at **Dresden** since about 2020. AutoPro150 (Auto Grade 1, 500k-cycle endurance, <10 ns read) reaches volume in 2H-2026 at Dresden ([GF/GlobeNewswire, 2026-03-09, via A2](https://www.globenewswire.com/news-release/2026/03/09/3251832/0/en/GlobalFoundries-Announces-Availability-of-AutoPro150-eMRAM-Technology-on-Enhanced-FDX-Platform-for-Advanced-Automotive-Applications.html)) [REPORTED].
  - **CBRAM/ReRAM:** GF bought Adesto/Dialog CBRAM technology from Renesas (2023-02-09). It is being qualified on 22FDX with about one extra mask ([GF via A2](https://gf.com/gf-press-release/globalfoundries-acquires-renesas-non-volatile-resistive-ram-technology-to-proliferate-iot-and-5g-applications/)) [REPORTED].
  - **Ferroelectric (FeFET/FeCAP):** HfO2 stacks are being evaluated in "upcoming" 22nm FDX memory (Fraunhofer FAMES, 2026), so not yet a product ([Fraunhofer via A1](https://www.ipms.fraunhofer.de/en/press-media/press/2026/FAMES-wafer-exchange.html)) [REPORTED].
  - **28nm / 40nm STT-MRAM:** this capacity serves Everspin's standalone parts at **GF Singapore** ([Everspin 10-K via A2](https://www.sec.gov/Archives/edgar/data/1438423/000162828026014733/mram-20251231.htm)) [REPORTED-P]. It is not a general eMRAM menu item in the U.S. [UNVERIFIED].
  - **U.S. fabs:** I know of **no eMRAM or ReRAM in volume production at Malta or Essex Junction** [UNVERIFIED]. GF's CHIPS award was described as onshoring technologies now made only abroad. Whether that includes 22FDX/eNVM at Malta is a key re-check (§11).
  - **14HP:** IBM's 14nm FinFET-on-SOI with **deep-trench eDRAM** ran at Malta for IBM z15/POWER9 [UNVERIFIED]. If still running, it is the **only U.S. foundry process with high-density embedded DRAM**. IBM moved later chips to Samsung, so 14HP may be legacy-only.
- **CHIPS:** $1.5B direct funding, final Nov 2024, for Malta expansion, a new Malta fab and Essex Junction modernization (GaN). GF then pledged **$16B in U.S. investment** in June 2025 [UNVERIFIED].
- **Outside customers:** yes.
  - GF runs MPW shuttles (12LP/22FDX/45RFSOI) and a university program.
  - 22FDX MPW is roughly **$10–25k/mm²** [ESTIMATE].
  - Wafer prices: 300mm 12/14nm ≈ **$4,000–6,000**; 22FDX + eMRAM ≈ **$4,500** (A2) [ESTIMATE].

### 2.5 Texas Instruments: Sherman, Richardson, Lehi
- **Sites:** RFAB1 (2009) and RFAB2 (production from Sept 2022) in Richardson; LFAB in Lehi (bought from Micron in 2021, producing from late 2022 at 65/45nm), with LFAB2 under construction and production expected ~2026; SM1 in Sherman (production started ~late 2025), with SM2–SM4 planned [UNVERIFIED].
- **Older fabs:** TI said it would close its last 150mm fabs (DFAB Dallas, SFAB Sherman) [UNVERIFIED].
- **CHIPS and investment:** up to $1.6B direct funding, final Dec 2024. In June 2025 TI announced a "$60B+ across seven U.S. fabs" plan [UNVERIFIED].
- **Memory relevance:** **captive only.**
  - TI is the volume U.S. maker of **embedded FRAM**: MSP430FR MCUs with 130nm PZT FeRAM, from the Ramtron license lineage [UNVERIFIED].
  - TI added Weebit ReRAM in Dec 2025 ([via A2](https://www.weebit-nano.com/news/press-releases/weebit-nano-secures-a-license-agreement-with-texas-instruments/)) [REPORTED].
- **Lehi:** TI did not keep any 3D XPoint capability; the fab runs 65/45nm analog/embedded ([AnandTech via A2](https://www.anandtech.com/show/16800)) [REPORTED].
- **Outside customers:** none. TI has no foundry business.
- **For American Memory:** TI is a **buyer or partner** (embedded-NVM IP), not a fab.

### 2.6 Polar Semiconductor: Bloomington MN
- **Technology:** 200mm power, BCD and high-voltage processes, plus magnetic sensors. Historically Polar was Sanken's captive fab, making parts for Allegro.
- **Ownership and money:** in 2024 it became majority U.S.-owned after a **~$175M** private investment (Niobrara Capital, Prysm Capital), backed by **~$123M of CHIPS funding** (final 2024) for a ~$525M expansion that **roughly doubles capacity**. It is transitioning to a **commercial foundry** [UNVERIFIED: prior knowledge].
- **Memory relevance:** low. It has no NVM offering I know of. Its value is as a U.S.-owned 200mm line open to new customers, with magnetic-sensor process experience, next door to SkyWater, Seagate and NVE. **A candidate BEOL-module host (IGZO, HZO) if SkyWater declines.** *v2:* Polar is an industry partner in UMN's new Spin Technology Center, alongside Honeywell Aerospace ([UMN CSE, via search snippet](https://cse.umn.edu/node/194186)) [REPORTED-P]. That makes it the likeliest U.S. 200mm line to pick up spintronic/MTJ process work.

### 2.7 Intel Foundry
- **External nodes** [UNVERIFIED]:
  - **Intel 16** (22FFL-derived; for RF/mixed-signal/IoT, with MPW access through Intel and EDA partners).
  - **Intel 3** (with -T for 3D stacking).
  - **Intel 18A** (high-volume production at Fab 52, Chandler, from ~Oct 2025; Panther Lake launched Jan 2026).
  - **18A-P**, and **14A** (Intel has said 14A depends on securing external customers).
  - A **12nm** node with UMC in Arizona (~2027).
- **Government ties:** RAMP-C (DoD) gives defense-industrial-base customers 18A access. Secure Enclave is ~$3B. In Aug 2025 the U.S. government took a **~9.9% equity stake** (~$8.9B) by converting CHIPS grants. The Ohio fab slipped to ~2030–31 [UNVERIFIED].
- **Memory:** Intel makes **no memory products** now; it exited Optane in 2022 and sold NAND to SK hynix/Solidigm. It has R&D only:
  - 22FFL STT-MRAM (7 Mb) and ReRAM (3.6 Mb, ~10 Mb/mm²) macros (ISSCC 2019) [UNVERIFIED: prior knowledge];
  - BEOL thin-film transistors for 1T1C eDRAM with ferroelectric capacitors ([Intel patent US11751402 via A1](https://patents.google.com/patent/US11751402)) [REPORTED];
  - 3D ferroelectric capacitor stacks (IEDM 2023) [UNVERIFIED];
  - Saimemory, a SoftBank-led stacked-DRAM venture using Intel technology (Japan, 2025) [UNVERIFIED].
- **For American Memory:** Intel 16 is the cheapest 300mm U.S. logic node open to outsiders. **Ask Intel Foundry whether Intel 16 offers its 22FFL-heritage eMRAM/ReRAM**; if yes, it would be the only U.S. 300mm foundry eNVM (§11). Otherwise Intel matters as a possible logic-die partner for a memory-controller or CXL chip, not as a memory fab.

### 2.8 Other trailing-edge 150/200/300mm fabs

| Fab | Status (as I know it; all [UNVERIFIED] unless cited) | Memory use? | Outside customers? |
|---|---|---|---|
| **Tower Newport Beach (Fab 3)** | 200mm, SiGe BiCMOS / RF / silicon photonics, 350–130nm; ex-Jazz (I believe it has trusted accreditation) | Only OTP/MTP NVM IP; no BEOL memory module | Yes, scheduled MPW program |
| **Tower San Antonio (Fab 9)** | 200mm, ex-Maxim (2016), ~180nm power/mixed-signal | None | Yes |
| **Tower @ Intel Rio Rancho (Fab 11X)** | Tower put ~$300M of tools into Intel NM, 300mm, 65nm BCD / RF-SOI (deal Sept 2023) | None | Yes (Tower) |
| **X-FAB Lubbock** | **150mm**, SiC + legacy silicon; only open 150mm SiC foundry in the U.S.; CHIPS PMT ~$50M (Dec 2024; low confidence) | None (150mm, no BEOL memory) | Yes |
| **onsemi East Fishkill** | 300mm, ex-IBM/GF; acquired 2022-12-31 (~$430M); power and analog (Treo 65nm BCD) | Weebit ReRAM licensed for Treo (2025-01, confirmed v2; fab location unverified); IBM's SOI eDRAM history | No |
| **onsemi Nampa ID / Mountain Top PA** | 200mm power; onsemi has been rationalizing fabs (2024–25) | None | No |
| **Microchip Fab 5 Colorado Springs** | 200mm (ex-Atmel), EEPROM / eFlash | Captive serial EEPROM, SuperFlash | No |
| **Microchip Fab 2 Tempe** | **Closure announced ~2025** (part of restructuring) | Possible idle 200mm shell/tools | n/a |
| **Bosch Roseville** | 200mm (ex-TSI), converting to SiC by ~2026; CHIPS PMT up to $225M | None | No |
| **NXP Chandler / Austin ATMC** | 200mm (+150mm GaN Chandler, 2020) | Hosts Everspin | No |
| **ADI Beaverton / Camas / Wilmington** | 150/200mm analog; CHIPS PMT ~$105M (Jan 2025) | None | No |
| **Wolfspeed Mohawk Valley / Durham** | Ch. 11 filed 2025-06-30, emerged ~Sept 2025; 200mm SiC (NY); 150mm Durham being wound down; CHIPS PMT $750M never finalized | None | No |
| **Qorvo Greensboro / Richardson** | 150mm GaAs / GaN; trusted for GaN | None (but tolerates In/Ga) | Limited |
| **BAE Systems Nashua NH** | 150mm GaN/GaAs, trusted; first CHIPS award (~$35.5M, Dec 2023) | None | DoD |
| **Samsung Austin S2** | 300mm 14–65nm foundry | No eMRAM in Austin (28FDS eMRAM made in Korea) | Yes |
| **TSMC Arizona / WaferTech** | AZ: N4/N3 production since late 2024, N2/A16 planned; WaferTech: 200mm, 350–160nm | No eNVM in AZ; WaferTech eFlash unclear | Yes |
| **Rochester Electronics** | Back end (die bank, licensed re-creation of end-of-life parts) | Legacy memory continuity | Yes (out of front-end scope) |

---

## 3. Memory technology × U.S. fab availability

| Technology | Made on U.S. wafers today? | By whom | Open to an outside small company in the U.S.? | Tag |
|---|---|---|---|---|
| Commodity DRAM (1-alpha and newer) | Yes | Micron Manassas (Boise R&D) | **No** | [REPORTED] |
| Trailing-node DRAM (25–40nm) | **No** | none | **No host exists** | [ESTIMATE] |
| Embedded DRAM (deep trench) | Possibly (legacy) | GF Malta 14HP (IBM) | Unknown; probably IBM/DoD only | [UNVERIFIED] |
| SRAM (embedded / discrete on trailing nodes) | Yes | Any foundry (SkyWater, GF, Tower, Intel 16, Samsung Austin, TSMC AZ) | **Yes** | standard |
| Toggle MRAM | Yes | Everspin Chandler (200mm BEOL); Honeywell rad-hard MRAM | **Ltd** (Everspin DoD programs) | [REPORTED-P]/[UNVERIFIED] |
| STT-MRAM (standalone) | **No** (GF Singapore, soon TSMC 16nm); U.S. STT flow at Gresham ~Q4-2028 (Toggle/sensor ~Q4-2027; captive to Everspin) | Everspin via Microchip | **No** | [REPORTED-P] |
| Embedded STT-MRAM (foundry) | **No** in the U.S. (GF Dresden 22FDX; TSMC/Samsung/UMC in Asia) | n/a | **No** (unless Intel 16 offers it) | [REPORTED]/[UNVERIFIED] |
| ReRAM (embedded) | Yes | SkyWater S130 (Weebit, qualified); TI (licensed, captive); onsemi Treo (licensed 2025-01, captive) | **Yes: SkyWater S130** | [REPORTED] |
| CBRAM | No (GF 22FDX in Dresden) | n/a | No | [REPORTED] |
| FeRAM (PZT, embedded) | Yes | TI (MSP430FR) | No (captive) | [UNVERIFIED] |
| FeRAM / FeFET (HfO2/HZO) | R&D only | Sandia MESA (trusted, 2026); NY CREATES + Fraunhofer (300mm JDA); GF 22FDX (Dresden, upcoming) | **R&D access** (Albany JDA; Sandia CRADA) | [REPORTED] |
| SONOS / charge-trap eNVM | Yes (captive/legacy) | SkyWater Fab 25 heritage (Cypress/Infineon); Microchip SuperFlash (floating gate) | Possibly at Fab 25 | [UNVERIFIED] |
| PCM / 3D XPoint | **No** (Lehi converted; Intel/Micron exited) | none | No | [REPORTED] |
| 3D NAND | **No** U.S. fab | none (Kioxia/SanDisk in Japan) | No | [UNVERIFIED]; see p1-micron |
| IGZO / oxide-TFT memory | **No production anywhere in the U.S.**; R&D at universities and Intel | Purdue (ALD In2O3, 3 tiers on 200mm, 2026), others in §7.4 | **Research access only** (nanofabs) | [REPORTED] ([Purdue, 2026-09-16, via A1](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing)) |

---

## 4. Wafer prices and MPW / shuttle access

No foundry publishes wafer prices. The figures below are estimates kept consistent with A1/A2 so the models agree.

| Item | Value | Tag / basis |
|---|---|---|
| 200mm 130–180nm processed logic wafer (SkyWater S130, Tower, X-FAB class) | **$900–1,600** (A1 uses $1,200; A2 uses $1,400 + $200 ReRAM adder) | [ESTIMATE] |
| 200mm 65–90nm (Fab 25, RH90) | **$1,500–2,500** (rad-hard / trusted carries a premium) | [ESTIMATE] |
| 300mm 22FDX (+eMRAM) | **$3,500–4,500** | [ESTIMATE] (A2) |
| 300mm 12/14nm (GF Malta, Intel 16, Samsung Austin) | **$4,000–6,000** | [ESTIMATE] |
| 300mm 28nm + MTJ module | ~$4,300 | [ESTIMATE] (A2) |
| Dedicated 130nm mask set | **$500–600k** | [REPORTED] ([AnySilicon via A1](https://anysilicon.com/130nm-wafer-mpw-cost/)) |
| MPW shuttle (node-agnostic range) | **$5k–100k**; direct foundry NRE $0.5–15M+; per-wafer $2.5–20k | [REPORTED] ([Silicon Analysts via A1](https://siliconanalysts.com/mpw-access-planning-guide/)) |
| sky130 open-source-style shuttle slot (~10 mm², ~100 parts) | **~$15k per 100 chips** via ChipFoundry, Efabless's successor (up from ~$10k in the chipIgnite era) | [REPORTED] ([eeNews Europe](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)) |
| GF180MCU shuttle via wafer.space (full slot, 1,000 dies) | **$7,000 early-bird / $7,500 standard**; half slot $4,000/$4,500 | [REPORTED-P] ([Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2)) |
| 22FDX MPW | ~$10–25k/mm² | [ESTIMATE] |
| 8-inch foundry pricing trend 2026 | Reports (late 2025) of TSMC/Samsung trimming 8-inch capacity and of 2026 8-inch price increases | [UNVERIFIED] |

**Implication:** a full SkyWater 130nm engineering run (masks plus ~25 wafers) costs about **$0.55–0.65M** [ESTIMATE: $550k masks + 25 × $1.5k]. That is T1. A shuttle die is T0, but MPW dies are small and diced, which makes BEOL post-processing awkward (§9).

---

## 5. CHIPS Act and related awards for these facilities

| Recipient / facility | Award | Status (date) | Tag |
|---|---|---|---|
| Micron: ID/NY | up to $6.165B | Final 2024-12-10; amended June 2025 (ID2) | [REPORTED-P] via p1-micron |
| Micron: Manassas | up to $275M | PMT 2024-12-10; final June 2025 | [REPORTED-P] ([NIST](https://www.nist.gov/node/1869301)) |
| GlobalFoundries: Malta, Essex Junction | $1.5B | Final Nov 2024 | [UNVERIFIED] |
| Texas Instruments: Sherman, Lehi, Richardson | up to $1.6B | Final Dec 2024 | [UNVERIFIED] |
| Intel: AZ/OH/NM/OR | $7.865B (+$3B Secure Enclave) | Final Nov 2024; **converted to ~9.9% federal equity, Aug 2025** | [UNVERIFIED] |
| Polar Semiconductor: Bloomington | ~$123M | Final 2024 | [UNVERIFIED] |
| SkyWater: Bloomington | up to ~$16M | PMT ~Dec 2024; final unknown | [UNVERIFIED, low confidence] |
| Microchip: Colorado Springs, Gresham | $162M | PMT Jan 2024; reportedly paused 2025 | [UNVERIFIED] |
| Bosch: Roseville | up to $225M | PMT Dec 2024 | [UNVERIFIED] |
| Analog Devices: OR/WA/MA | up to ~$105M | PMT Jan 2025 | [UNVERIFIED] |
| Wolfspeed: NY/NC | $750M | PMT Oct 2024; not finalized; company went through Ch. 11 in 2025 | [UNVERIFIED] |
| HP: Corvallis | ~$50M | PMT 2024 | [UNVERIFIED] |
| BAE Systems: Nashua | ~$35.5M | Dec 2023 (first award) | [UNVERIFIED] |
| Samsung (Taylor/Austin), SK hynix (IN packaging) | $4.745B; up to $458M | Dec 2024 | via p1-micron |
| Everspin, NVE, Seagate, Tower U.S., X-FAB (final) | none found | n/a | [UNVERIFIED] |

**Policy context (2025–26), all [UNVERIFIED] except where cross-referenced:**
- Commerce under Secretary Lutnick renegotiated or reviewed awards, and Intel's grants became equity.
- Natcast's role as NSTC operator was ended in Aug 2025, with NIST taking direct control. The Albany EUV Accelerator continues under NY CREATES.
- The §48D investment tax credit rose to **35%**, but only for construction that begins by **2026-12-31** (p1-micron §1.6). That window is too short for any new founder-led line.

---

## 6. Idle, for-sale, closed or distressed U.S. fabs (2024–2026)

| Asset | Event | Wafer / type | Memory reuse potential |
|---|---|---|---|
| Infineon Fab 25 Austin | **Sold to SkyWater; closed 2025-06-30** ([LaPedus via A1](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm)) [REPORTED] | 200mm 130–65nm | Already absorbed; now the best open host |
| Microchip Fab 2 Tempe AZ | Closure announced ~2025 [UNVERIFIED] | 200mm | Shell/tools could host a BEOL pilot. Cleanroom reuse is cheaper than greenfield, but site control sits with Microchip |
| Wolfspeed Durham 150mm SiC device fab | Wind-down tied to the move to 200mm Mohawk Valley; Ch. 11 June–Sept 2025 [UNVERIFIED] | 150mm SiC | Low: SiC-specific; 150mm |
| Akoustis Canandaigua NY | Ch. 11 Dec 2024 after the Qorvo trade-secret verdict; assets sold 2025 [UNVERIFIED] | 150mm BAW/MEMS (AlScN PVD) | Sputter-rich, East Coast; plausible for a **150mm research-grade IGZO/oxide line** but not for CMOS |
| TI DFAB (Dallas) / SFAB (Sherman) 150mm | Announced phase-out [UNVERIFIED] | 150mm | Low; TI rarely sells fabs to competitors |
| Bosch Roseville (ex-TSI) | Converted from silicon to SiC [UNVERIFIED] | 200mm | No longer available |
| Intel Ohio | Delayed to ~2030–31 [UNVERIFIED] | 300mm shell | Not available to third parties |
| Foxconn Wisconsin (Mt. Pleasant) | Gen 10.5 LCD fab **never built**; site repurposed (servers, data center) [UNVERIFIED] | n/a | None |
| Foreign idle display fabs (context) | Sharp Sakai Gen 10 stopped LCD panel output ~2024; JDI Mobara closure ~2025 [UNVERIFIED] | Gen 6–10 | Real, but **not U.S.-made**, so it fails the mission's "Made in America" moat |

**Takeaway:** the U.S. market in idle 200mm capacity is thin, and the good assets get absorbed: Fab 25 went for about $93M. A founder cannot buy a fab (T3 and up), but **depreciated 200mm capacity is cheap to rent through SkyWater or Polar**. That is the realistic form of the mission's "cheaper capital" (5c) in the U.S.

---

## 7. U.S. display / TFT capacity

### 7.1 Gen-scale panel fabs: none
- **No LCD, OLED or oxide-TFT panel fab at Gen 4 or larger operates in the U.S.** (2026-11) [UNVERIFIED: prior knowledge; consistent with [TrendForce TFT capacity abstract via A1](https://www.trendforce.com/research/download/RP260831UV) showing no U.S. fabs, REPORTED].
- Foxconn's 2017 Wisconsin plan (Gen 10.5, later shrunk to Gen 6) was never built [UNVERIFIED].
- Every IGZO backplane line runs in Japan, Korea, China or Taiwan: Sharp, LG Display, Samsung Display, BOE, CSOT, AUO.
- The one oxide-TFT "chip" fab outside Asia is **Pragmatic Semiconductor (Durham, UK)**, which makes IGZO FlexICs on 300mm; it has no U.S. fab ([Semiconductor Today, 2024-03, via A1](https://www.semiconductor-today.com/news_items/2024/mar/pragmatic-280324.shtml)) [REPORTED].

### 7.2 Niche U.S. display manufacturing (none is a TFT backplane line usable for memory)

| Company / site | What it makes | TFT? | Memory relevance | Tag |
|---|---|---|---|---|
| **eMagin (Samsung Display since Oct 2023, ~$218M)**, Hopewell Junction NY | OLED-on-silicon microdisplays; OLED deposition and direct patterning (dPd) on purchased 200mm CMOS backplanes; DoD-funded | No (silicon backplane) | None; shows a U.S. BEOL-style deposition line on 200mm CMOS | [UNVERIFIED] |
| **Kopin**, Westborough MA | Microdisplays (AMLCD with transferred single-crystal Si, LCOS, OLED-on-Si via partners, microLED R&D); DoD programs | Si-based, not oxide | None | [UNVERIFIED] |
| **Kent Displays**, Kent OH | Cholesteric LCD (Boogie Board), roll-to-roll | No active TFT | None | [UNVERIFIED] |
| **Corning**, NY/KY | Display glass (EAGLE XG; most display-glass melting is in Asia), Gorilla Glass (Harrodsburg KY), glass for semiconductor packaging | Substrate only | Glass-substrate concepts; no TFT | [UNVERIFIED] |
| **Applied Materials** (Santa Clara; AKT display group) | Gen 8.5–10.5 PECVD/PVD/array-test tools; Max OLED; EPIC R&D center | Tools, not panels | Tool vendor for any IGZO line; no U.S. panel line | [UNVERIFIED] |
| **Akoustis** (Canandaigua NY) | BAW RF filters on a 150mm MEMS line (bankrupt Dec 2024) | No | Sputter-heavy 150mm line (see §6) | [UNVERIFIED] |
| **Amorphyx** (Corvallis OR) | Amorphous-metal nonlinear resistor backplane IP (TFT alternative) | Alternative | Oregon State oxide/thin-film lineage | [UNVERIFIED] |

### 7.3 Research lines with oxide-TFT capability

| Institution | Capability | Access | Tag |
|---|---|---|---|
| **ASU Flexible Electronics & Display Center (FEDC) → MacroTechnology Works (MTW)**, Tempe AZ | FEDC (Army-funded, from 2004) ran a **Gen-II (370×470 mm) display pilot line** and showed flexible a-Si and mixed-oxide TFT backplanes, including ~2012 flexible OLED demonstrators. MTW is the ex-Motorola building that now houses ASU's semiconductor work, the SWAP Microelectronics Commons hub and the ASU–Applied Materials Materials-to-Fab Center. **Whether the Gen-II line still runs is unknown** | ASU core facilities: external/industry rates | [UNVERIFIED] |
| **Purdue** (Birck Nanotechnology Center; Peide Ye) | **ALD In2O3** transistors (8nm channel, Nature Electronics 2022); **three stacked oxide-transistor tiers on 200mm Si**, >100k devices across 52 dies (2026-09) | Birck: external users | [REPORTED] ([Purdue 2026 via A1](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing)) |
| **Georgia Tech** (IEN, NNCI; Suman Datta's group, ex-Notre Dame) | BEOL oxide-channel transistors (IWO/ITO), 2T gain-cell eDRAM, ferroelectrics | NNCI rates | [UNVERIFIED]; related IWO 2T result logged by A1 |
| **Oregon State** (John Wager, Doug Keszler) | Pioneering amorphous-oxide TFT and solution-processed oxides (Inpria spin-out) | University | [UNVERIFIED] |
| **Penn State** (Nanofab / MRI; Tom Jackson; 2DCC-MIP) | PEALD ZnO/oxide TFTs, flexible electronics, 2D materials | External users; East Coast | [UNVERIFIED] |
| **UT Dallas** | Flexible electronics / oxide TFT (Gnade lineage) | University | [UNVERIFIED] |
| **Stanford** (SNF, NNCI; H.-S. Philip Wong, Saraswat) | Oxide-channel and RRAM/MRAM research | NNCI rates | [UNVERIFIED] |
| **MIT.nano / MIT Lincoln Lab** | 150/200mm shared fab (MIT.nano, open to industry); 200mm 90nm FDSOI (MIT LL) | Industry rates / government sponsors | [UNVERIFIED] |
| **Cornell CNF** (NNCI) | General nanofab: sputter, ALD, i-line/e-beam litho | NNCI rates; East Coast | [UNVERIFIED] |
| **Sandia MESA / CINT** | MESA: trusted rad-hard CMOS with **HZO FeRAM integrated (2026)**; CINT (with LANL): DOE user facility | CINT: free for open research by proposal; MESA: CRADA | [REPORTED] ([Sandia via A1](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/)) |
| **Intel** (Hillsboro) | BEOL IGZO-TFT eDRAM / FeCAP R&D (IEDM papers, patents) | Not open | [REPORTED] (patent) / [UNVERIFIED] |

### 7.4 Verdict on U.S. TFT capacity
- **Zero production capacity, and research capacity only at the 100–200mm device level.**
- The mission asks whether IGZO's display-fab compatibility could unlock cheap U.S. capacity. The answer is **no**, because there is no U.S. display fab.
- The IGZO path in the U.S. is therefore (i) a **BEOL module on a 200mm silicon foundry** (SkyWater or Polar) or (ii) a **university pilot**. Both are slow and low-density (§8).

---

## 8. Can an idle or trailing silicon fab run IGZO BEOL?

**Short answer:** technically yes. IGZO's thermal budget and tools fit a standard back-end-of-line flow. The barriers are contamination policy, hydrogen control, reliability and density, not physics.

### 8.1 Process requirements

| Step | Typical IGZO process | Fit with a 200mm CMOS BEOL | Notes / evidence |
|---|---|---|---|
| Channel deposition | **DC/RF or pulsed-DC magnetron sputter** from a ceramic InGaZnO4 (1:1:1:4) target in Ar/O2, at room temperature to ~300 °C, 10–50 nm thick. **ALD/PEALD** (In/Ga/Zn precursors) for conformal 3D or vertical channels | Every fab has a PVD cluster, but needs a **dedicated chamber/target**. ALD is less common at 130nm fabs (no high-k there) | Room-temperature a-IGZO TFT: Nomura et al., *Nature* 432, 488 (2004) [UNVERIFIED citation from memory]. ALD oxide channels on 200mm ([Purdue via A1](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing)) [REPORTED]. Kioxia OCTRAM vertical IGZO ([BusinessWire, 2024-12-09, via A1](https://www.businesswire.com/news/home/20241209099702/en/Kioxia-Develops-OCTRAM-Oxide-Semiconductor-Channel-Transistor-DRAM-Technology)) [REPORTED] |
| Gate dielectric | Low-hydrogen PECVD SiO2, or ALD Al2O3/HfO2 | Standard tools | Hydrogen is a shallow donor in IGZO and shifts the threshold voltage, so low-H films and H barriers are required (Kamiya/Nomura/Hosono review, *Sci. Technol. Adv. Mater.* 11 (2010) 044305) [UNVERIFIED citation] |
| Anneal | 300–400 °C in O2/N2/air | **≤400 °C fits an Al or Cu BEOL limit of ~400–450 °C** | imec ran its 2T0C on **300mm, BEOL-compatible** ([TechXplore via A1](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html); [eeNews, 2020, via A1](https://www.eenewseurope.com/news/imec-shows-capacitor-free-dram)) [REPORTED] |
| Patterning | Wet (oxalic / dilute HCl) or ICP dry (CH4/H2/Ar or Cl-based) | Standard | IGZO etches easily; selectivity to contacts matters |
| Contacts / electrodes | Mo, W, TiN, ITO, Ti/Au | Standard BEOL metals (except Au) | n/a |
| Lithography | Display: 2–4 µm rules. Memory density needs ≤130nm (KrF) or better | 130nm (SkyWater) or 65nm (Fab 25) available | Density, not printability, is the issue (8.3) |
| Passivation / encapsulation | PECVD SiO2/SiNx with H control; Al2O3 cap | Standard | SiNx is H-rich; use with care |
| Reliability | **PBTI/NBTI threshold drift** is the known weakness | Needs a qualification program | imec 2T0C: PBTI lifetime ~1 yr vs a 5-yr target (IEDM 2021) ([TechXplore via A1](https://techxplore.com/news/2021-12-capacitor-less-igzo-based-dram-cell-excellent.html)) [REPORTED] |

### 8.2 Contamination and fab policy (the real blocker)
- **In, Ga and Zn are restricted metals in silicon front-end (FEOL) fabs.** Ga and In act as acceptors in Si, and Zn is a fast-diffusing deep-level contaminant [UNVERIFIED: general process knowledge].
- A fab that runs FEOL CMOS will only accept IGZO on **dedicated BEOL tools**, with segregated wafer carriers and wet benches, after the first metal layer or above. The same discipline is used today for copper.
- That means **NRE and a tool set**, not just a recipe change. Expect the host to want ~$4–10M of dedicated refurbished tools (oxide PVD, ALD, PECVD, anneal, ICP etch, wet bench, parametric test), plus months of contamination qualification [ESTIMATE; assumptions file]. This is **T2**.
- Fabs that already tolerate In/Ga (III-V lines such as Qorvo or BAE, and MEMS lines such as Akoustis's former fab) have no CMOS underneath. They suit TFT-only test vehicles but not monolithic CMOS + IGZO memory.

### 8.3 Density at U.S.-available design rules
These figures were computed in scratch (igzo_density.py, not a deliverable). Inputs are assumptions: planar 2T0C cell = 20–40 F², array efficiency 60%, DDR5 1b = 0.436 Gb/mm² (A1 basis).

| Host design rule | IGZO 2T0C density per tier | DDR5-1b advantage |
|---|---|---|
| 130nm (SkyWater S130 / Fab 25) | 0.9–1.8 Mb/mm² | **250–490×** |
| 65nm (Fab 25) | 3.6–7.1 Mb/mm² | **60–120×** |
| ~50nm (GF Malta 12/14nm BEOL, hypothetical) | 6–12 Mb/mm² | **36–73×** |
| 2 µm display rule | ~0.01 Mb/mm² (~3–5 GB per Gen 8.5 sheet) | ~60,000–115,000× |

[ESTIMATE] Stacking 4–8 tiers narrows the 65nm gap to roughly 8–30×, at the cost of 4–8 times the BEOL steps. **Conclusion:** U.S.-made IGZO memory cannot be a $/GB DRAM product on any available U.S. line. Its possible value lies on other axes:
- **retention and standby power**: Ioff of ~1e-19 A/µm or lower vs ~1e-12 for Si, which allows refresh-free or near-non-volatile buffers;
- **monolithic BEOL stacking over logic**: embedded "gain-cell eDRAM" above a SkyWater or Intel 16 logic die;
- **rad-hardness** (an oxide channel has no body; [UNVERIFIED]).

This agrees with A1's conclusion that only a 300mm, ~28nm-class BEOL line makes IGZO DRAM-like, and no U.S. foundry offers one (`phase2/A1_device_params.json`).

### 8.4 Fab-by-fab fit for an IGZO BEOL module

| Host | Fit | Why |
|---|---|---|
| **SkyWater Bloomington (S130)** | **Best** | Pure-play; has done low-temperature new-material BEOL (DARPA 3DSoC CNT + RRAM [UNVERIFIED]) and Weebit ReRAM; Trusted (DoD buyers); DoD/Microelectronics Commons money available |
| **SkyWater Fab 25 (65nm)** | Good, later | Better density; still converting to a foundry, so lower priority for new modules in 2026–27 |
| **Polar Bloomington** | Possible | New foundry hungry for customers; but power/BCD focus and no NVM experience |
| **GF Malta** | Unlikely for a startup | 300mm tool cost; startup NRE in the $M; trusted-program priorities |
| **Intel 16 / 18A** | Unlikely | No public BEOL-module customization for small customers |
| **Sandia MESA** | R&D / defense only | Already integrating HZO; a CRADA route for rad-hard memory |
| **NY CREATES Albany** | R&D at 300mm | JDA model; already doing HfO2 FE memory with Fraunhofer; IGZO tools plausible |
| **University fabs (Purdue, GT, Penn State, Cornell)** | **Prototype now** | Have sputter/ALD; device-level; cheapest |

---

## 9. Nanofabs and national labs open to external users: the cheap prototype path

### 9.1 Who offers external access

| Facility | Location | Wafer size / class | External access model | Rate guidance |
|---|---|---|---|---|
| **NSF NNCI** (16 sites through 2025: Cornell CNF; Stanford; Georgia Tech/UGA SENIC; Harvard CNS; UW; Penn (Singh); Northwestern/UChicago SHyNE; ASU NCI-SW; UT Austin TNF; UCSD SDNI; Montana State; Minnesota MNC; Kentucky/Louisville KY Multiscale; Nebraska; NC State/Duke/UNC RTNN; Virginia Tech NanoEarth) | National | 100–150mm typical, some 200mm tools | Open to academic and industry users; hourly tool + staff fees; NDA available | [ESTIMATE] industry **$75–250/tool-hour**, staff **$100–200/hr**; academic $30–90/hr. Program status after the 2025 renewal cycle [UNVERIFIED] |
| **NIST CNST NanoFab** | Gaithersburg MD | 100–200mm tools | Shared access for industry and academia; proprietary OK | [UNVERIFIED] hourly; East Coast |
| **DOE NSRCs**: CINT (Sandia/LANL), CFN (Brookhaven NY), CNM (Argonne), CNMS (ORNL), Molecular Foundry (LBNL) | National | Device-level | **Free for non-proprietary research by peer-reviewed proposal** (cycles ~2×/yr); proprietary at full cost recovery | Free / cost-recovery [UNVERIFIED] |
| **Sandia MESA** | Albuquerque NM | 150mm rad-hard CMOS; FeRAM at 200mm scale | CRADA / strategic-partnership projects; trusted | Contract-priced; slow [UNVERIFIED] |
| **NY CREATES / Albany NanoTech** | Albany NY | **300mm**, EUV | Membership / JDA; startups and SMEs ([NY.gov via A1](https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york)) [REPORTED] | T1–T2 (likely $0.25–2M+ engagements) [ESTIMATE] |
| **MIT.nano** | Cambridge MA | 150/200mm | Open to outside industry users | [UNVERIFIED] |
| **RIT SMFL** | Rochester NY | 150mm CMOS teaching / research fab | External services | [UNVERIFIED] |
| **Penn State Nanofab** | University Park PA | 100–200mm | External users | [UNVERIFIED] |
| **Purdue Birck** | West Lafayette IN | 100–200mm | External users | [UNVERIFIED] |
| **ASU core facilities / MTW** | Tempe AZ | 150/200mm; legacy Gen-II display line | External / industry; SWAP hub | [UNVERIFIED] |

### 9.2 Ranked prototype paths for an IGZO 2T0C or HZO FeCAP memory test chip

| Rank | Path | What you get | Cost | Time | Tier |
|---|---|---|---|---|---|
| 1 | **Sponsored-research agreement or user account at one university fab with an oxide-TFT group** (Purdue, Georgia Tech, Penn State, Cornell) | Discrete TFTs, 2T0C cells, retention/PBTI data on 100–200mm | **$20–80k** (tool time plus a student or postdoc stipend, or a staff engineer) | 3–6 months | T0/T1 [ESTIMATE] |
| 2 | **DOE NSRC proposal** (CINT/CFN) | Free tool access; results must be published | ~$0 cash + travel | 6–9 months (proposal cycle) | T0 [UNVERIFIED] |
| 3 | **SkyWater S130 shuttle die + university BEOL post-process** | CMOS sense/periphery under IGZO cells; monolithic demonstrator | **$15–60k** per iteration (shuttle $10–15k+; post-processing $5–45k) | 6–9 months | T0/T1 [ESTIMATE]. Diced MPW dies make lithography and planarization hard, so expect yield pain |
| 4 | **Full 130nm engineering run at SkyWater with a co-developed IGZO module** | Wafer-level, qualifiable | **$0.55–0.65M** wafers/masks + module NRE ($1–5M+) | 12–24 months | T1→T2 [ESTIMATE] |
| 5 | **Albany NY CREATES JDA at 300mm** | Leading-edge integration, high density | **$0.25–2M+** | 12+ months | T1/T2 [ESTIMATE] |

**Recommendation for the founder (T0, <$10k kill test):** before any money moves, **email two oxide-TFT groups** (Purdue's Ye group, Georgia Tech's Datta group) and **SkyWater's foundry business development** with one question: *will you run an IGZO (or HZO) BEOL module above S130, and what NRE and contamination rules apply?* The answers show whether path 3 or 4 exists.

---

## 10. What this means for American Memory

1. **Kill or downgrade concepts that need U.S. DRAM foundry capacity** (trailing-node DRAM dies, DRAM capacitor processes). No host exists outside Micron. Any trailing-node DRAM concept must source **dies** (SpecTek, Winbond KGD; p1-micron), not wafers from a U.S. foundry.
2. **Device concepts with a real U.S. foundry path today:**
   - **SkyWater S130 + Weebit ReRAM**: embedded NVM chiplets, trusted, DoD buyers.
   - **SkyWater/Polar + a co-developed BEOL module** (IGZO gain cell, HZO FeCAP); T2, 18–36 months.
   - **Everspin partnership** for MTJ (Toggle/STT); the founder is a customer, not a fab user.
3. **"U.S.-made" moat claims must be precise.**
   - Everspin STT-MRAM is Singapore-made, and moving to TSMC 16nm, until Gresham's STT flow arrives (~Q4-2028; Toggle/sensor ~Q4-2027) (v2).
   - The only U.S.-made MRAM today is Toggle (Chandler) and Honeywell rad-hard.
   - For DoD buyers, **trusted-foundry provenance** (SkyWater, GF U.S., Sandia, Honeywell) matters more than "U.S.-made" alone.
4. **IGZO's cheap display capacity is not available in the U.S.** Any IGZO concept that relies on display-fab economics must either go abroad (and lose the moat) or accept silicon-BEOL economics and density (§8.3).
5. **Cheaper capital (mission 5c), U.S. version:** rent depreciated 200mm capacity (SkyWater, Polar). Fab 25's ~$93M price for ~400k wafer starts/yr shows how cheap the capacity is, but buying a fab is still T3. University nanofabs ($20–80k) are the T0/T1 learning path.
6. **Glut sensitivity:** none of the U.S. foundry paths above competes on $/GB, so a 2028–29 DDR5 glut does not directly kill embedded or trusted niches. It does kill any pitch that frames IGZO or ReRAM as "cheaper DRAM."

---

## 11. Re-verification list (priority order; ~30 searches would clear it)

1. **SkyWater**: Fab 25 foundry offerings (65nm; SONOS/eNVM?); CHIPS status; post-Efabless shuttle access and pricing (*v2: ChipFoundry ~$15k/100 chips; is the Weebit ReRAM block offered?*); IonQ-era customer and IP terms (no more 10-K: IonQ subsidiary since 2026-07-31).
2. **GF Malta**: does Malta offer 22FDX/eMRAM/ReRAM in 2026, or plan to under the CHIPS onshoring? Is 14HP eDRAM still running?
3. **Everspin**: which fab receives the Amentum Toggle transfer; Chandler 200mm-only status; NXP Chandler fab longevity (FY2026 10-K risk factors).
4. **Intel 16**: is eMRAM/ReRAM offered to external customers?
5. **TI**: SM1 production date; LFAB2 status; where MSP430FR FRAM is made.
6. **Polar**: final CHIPS amount and date; foundry-services status in 2026.
7. **Microchip**: Tempe Fab 2 closure date and asset disposition; CHIPS status.
8. **onsemi–Weebit** Treo license (*v2: exists, signed 2025-01; still open: which fab*).
9. **ASU MTW**: is the Gen-II display line operational? Rates.
10. **NNCI**: 2025 renewal outcome and current site list; 2026 industry rate sheets at Cornell CNF, Penn Singh, Georgia Tech IEN, Purdue Birck, NIST CNST.
11. **Akoustis** asset sale outcome (2025).
12. **Wolfspeed** Durham status; Bosch Roseville CHIPS final.
13. **CHIPS award list**: final vs. PMT for every row in §5 (NIST CHIPS awards page).
14. **NSTC** operator status in 2026 (NIST vs. Natcast) and Albany EUV Accelerator access terms.
15. **TrendForce 8-inch foundry price trend 2026** (free press center).
