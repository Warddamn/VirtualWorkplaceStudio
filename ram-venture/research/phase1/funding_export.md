# Phase 1: Government money, procurement preference, and export controls

**Agent:** `p1-funding` · **Date:** 2026-11-01 · **Scope:** mission §3C, last two bullets (government money and preference; export controls and ITAR)
**Sources:** `research/sources/p1-funding.jsonl` · **Assumptions:** `research/assumptions/p1-funding.md`

---

## 0. Read this first: how much of this is verified

**I could not verify anything independently this session.** This is a material limitation. Three things went wrong:

1. **The shared WebSearch budget was used up.** Other Phase 1 and Phase 2 agents had already spent the 200-call per-turn limit before my first query. All three of my first searches were refused.
2. **WebFetch is blocked for the hosts that matter.** `www.nist.gov` and `en.wikipedia.org` both failed DNS resolution with "outside the session's allowed network domains". Under session rules I stopped trying more hosts after the second failure. The proxy log also shows 403s for `www.sec.gov`, `www.trendforce.com` and `investors.micron.com`. **To finish verification, `nist.gov`, `bis.gov`, `federalregister.gov`, `sbir.gov`, `acquisition.gov`, `ecfr.gov`, `congress.gov`, `darpa.mil` and `dmea.osd.mil` need to be allowed in the session's network settings, or the search budget raised (`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`).**
3. **What is here therefore comes from two places:**
   - **Cross-referenced sibling sources.** These are search snippets that `p1-micron`, `p1-backend`, `A1` and `A2` logged this session. They are re-logged in my sources file with a CROSS-REFERENCE flag and tagged here as **[REPORTED via <agent>]**.
   - **My prior knowledge.** My training data runs to about mid-2026 and is densest through 2025. These facts are tagged **[UNVERIFIED-H/M/L]**: not re-checked this session, with my confidence that they are still correct on 2026-11-01 rated High, Medium or Low. **No URL is given for these, because I may not invent URLs.** Named legal citations (e.g., "89 FR 96790") are given where I am confident of them so that someone can check them quickly.

**How to use this file:**
- Treat every [UNVERIFIED-M/L] line as a lead to check, not a fact.
- §14 is the verification queue in priority order. The top five items each take about 10 minutes once the network is open.
- The **structural conclusions** in §2 (who can get what money, which rules bind) depend mostly on [UNVERIFIED-H] statute-level facts and are unlikely to flip. The **2026 status** details (SBIR terms, NSTC operator, CXMT listing) are the weak points.

Tag key: [VERIFIED] means primary opened this session (none). [REPORTED via X] means a sibling agent's logged source. [UNVERIFIED-H/M/L] means prior knowledge. [ESTIMATE: basis] means my own computation or judgment.

---

## 1. Master table

$ figures in the third column are what a **small, new company** can realistically reach, not the program's size.

| # | Program | Status (late 2026) | $ available to a small co. | Fits which concept types | Source / tag |
|---|---|---|---|---|---|
| 1 | **CHIPS manufacturing incentives** ($39B direct funding; $75B loan authority) | Nearly all committed by Jan 2025. CHIPS Program Office now sits under the **U.S. Investment Accelerator** (EO, 2025-03-31). Awards renegotiated for bigger investment or converted to **equity** (Intel, Aug 2025). No evidence of an open NOFO | **≈$0** for a new entrant. Precedent small-supplier awards were $6.7M–$18M, all before 2025 | Capex for packaging, test or materials (T2+). Not T0/T1 | Micron awards [REPORTED via p1-micron] ([NIST, 2024-12-10](https://www.nist.gov/node/1855121)); structure and Intel [UNVERIFIED-H]; NOFO status [UNVERIFIED-M] |
| 2 | **§48D Advanced Manufacturing Investment Credit** | **35%** for property placed in service after 2025-12-31 (OBBBA, July 2025). **Construction must begin by 2026-12-31, 60 days from today.** BASIC Act extension (H.R. 3204) pending, not enacted | 35% of qualified property, **refundable via elective pay**. Example: $3M line gives $1.05M [ESTIMATE: 0.35 × $3M], but only if construction starts in the next 60 days | Only a qualifying semiconductor/SME manufacturing facility already in planning. In practice **closed** to this venture | [REPORTED via p1-micron] ([Baker Tilly, 2025](https://www.bakertilly.com/insights/advanced-manufacturing-credits-section-48d); [Instead, 2026-03-31](https://instead.com/resources/blog/section-48d-credit-rises-to-35-and-why-you-must-act-before-2027); [Congress.gov H.R. 3204](https://www.congress.gov/119/bills/hr3204/BILLS-119hr3204ih.htm)); elective pay [UNVERIFIED-H] |
| 3 | **CHIPS R&D ($11B): NSTC** | **Natcast's operator agreement voided by Commerce, Aug 2025**; NIST took direct control. Status in 2026 unclear | **Assume $0.** No membership program to join was confirmed | Device and materials R&D | [UNVERIFIED-M]; sibling p1-fabs has same claim [UNVERIFIED] |
| 4 | **NAPMP** (advanced packaging) and **SMART USA** (CHIPS Manufacturing USA institute, digital twins; SRC-led) | Awards made late 2024 (substrates; SMART USA ~$285M). 2025–26 activity unverified | Sub-awards or membership only. Typical team-member slices are $100k–$1M [ESTIMATE] | Packaging/KGD, digital-twin and fab software | [UNVERIFIED-M] |
| 5 | **DoD Microelectronics Commons** (8 hubs; $2B over FY23–27) | Running through FY2027 (statutory window). Project calls via consortium manager NSTXL. FY26–27 call sizes unverified | Team-member share of hub projects. Order of $0.1–2M per company per project [ESTIMATE] | Device prototyping (eNVM, CIM, AI hardware), packaging | [UNVERIFIED-M] |
| 6 | **DMEA Trusted Accreditation** | Ongoing. Accreditation, not money | **$0**, but it is **market access** to DoD programs that need trusted parts | Trusted/rad-hard memory, packaging, test, brokerage | [UNVERIFIED-H] |
| 7 | **RAMP-C / SHIP / Secure Enclave** | Prime-level programs (Intel, Qorvo). Secure Enclave ($3.2B) folded into Intel equity, Aug 2025 | $0 direct. Possible design-access subcontracts | Chiplet memory designers only | [UNVERIFIED-M] |
| 8 | **DPA Title III** | No memory or memory-packaging award found | $0 expected. Awards are typically $5–50M+ to established firms | Packaging capex if DoD declares a gap | [UNVERIFIED-L] |
| 9 | **DoD Office of Strategic Capital** (loans) | Lending for "critical components" since 2024 | Debt, not grants. Needs an operating business | Later-stage capex | [UNVERIFIED-L] |
| 10 | **DARPA NGMM** (3DHI center at UT Austin's TIE) | ~$840M DARPA (2024) plus Texas match; building shared 3DHI prototyping capability | Fee-based user access, not grants | 3D memory-on-logic, HBM-like stacks (T2+) | [UNVERIFIED-M] |
| 11 | **DARPA MTO: SBIR topics and seedlings** | **DPA26BZ04-DV017** "Non-Volatile Memory for Extreme Environments" (−269 °C to +600 °C, rad-tolerant NOR, co-packaged). Direct-to-Phase II, **opened 2026-07-22, closed 2026-08-19**. OPTIMA (CIM) and Microsystems Exploration (μE) exist; performers and status unverified | **~$1.2M** (DV017). μE seedlings ~$1M class [UNVERIFIED-L] | Rad-tolerant/extreme-env NVM, CIM | [REPORTED via A1] ([DARPA, 2026-07](https://www.darpa.mil/research/programs/non-volatile-memory-extreme-environments); [BWCO, 2026-07](https://www.bwcoconsulting.com/fod/dpa26bz04-dv017)); rest [UNVERIFIED-M/L] |
| 12 | **JUMP 2.0** (SRC + DARPA; 7 centers incl. **PRISM**, memory-centric) | 2023–2027 | Not money. Industry membership is costly; value is **IP and talent to license or hire** | Device IP licensing, CIM | [UNVERIFIED-M] |
| 13 | **IARPA** | No current memory-specific program confirmed | — | — | [UNVERIFIED-L] |
| 14 | **SBIR/STTR** | **Lapsed 2025-10-01.** DoD SBIR topics opening again in July 2026 imply authority was restored by mid-2026 [ESTIMATE: inference]. **Reauthorization terms NOT verified** | Phase I ~$150–315k; Phase II ~$1–2.1M; DoD Direct-to-Phase II ~$1.2M. **The PI must be >50% employed by the company, which rules out this founder while he keeps the day job** | Device R&D, rad-hard NVM, provenance/test tooling, memory-efficiency software (NSF) | DV017 and AF254-D0806 [REPORTED via A1] ([SBIR.gov AF254-D0806, 2025](https://www.sbir.gov/topics/12036)); rules and caps [UNVERIFIED-H/M] |
| 15 | **AFWERX TACFI/STRATFI** (SBIR matching) | Exists for Phase II performers | Up to ~$15M gov't with private match (STRATFI) | Post-Phase-II DoD products | [UNVERIFIED-M] |
| 16 | **New York: Green CHIPS and others** | Green CHIPS: $10B in refundable Excelsior credits over 20 yrs for megaprojects; **Micron up to $5.5B** | **$0** from Green CHIPS for a small co. Other NY paths (Excelsior Jobs, FuzeHub grants, NY CREATES fee-based access, NORDTECH hub) are worth $10k–$100k [ESTIMATE] | NY-sited manufacturing or R&D | Micron $5.5B [REPORTED via p1-micron] ([eeNews Europe, 2026-01](https://www.eenewseurope.com/en/micron-new-york-megafab-breaks-ground-2026/)); rest [UNVERIFIED-M] |
| 17 | **Texas: TSIF** | Texas CHIPS Act 2023, ~$698M. Biggest grant is TIE ($552M) | Grants mostly to institutions and large projects | TIE/NGMM users | [UNVERIFIED-M] |
| 18 | **Massachusetts: MassVentures START; MassTech/NEMC hub** | START funds SBIR Phase II companies | ~$100k–$500k across stages [UNVERIFIED-L] | SBIR-stage MA companies | [UNVERIFIED-M/L] |
| 19 | **North Carolina: One NC Small Business Program** | SBIR/STTR proposal reimbursement plus Phase I matching | ~$12k proposal reimbursement; matching up to ~$100–150k [UNVERIFIED-L] | SBIR-stage NC companies | [UNVERIFIED-M] |
| 20 | **Virginia: VIPC Commonwealth Commercialization Fund** | Ongoing [UNVERIFIED-M] | ~$50–100k [UNVERIFIED-L] | VA tech startups | [UNVERIFIED-M] |
| 21 | **Arizona / Idaho / Ohio** | AZ: Innovation Challenge, Qualified Facility credit, SWAP hub. ID: Reimbursement Incentive (job-based). OH: Third Frontier, JobsOhio | AZ ~$100–150k grant class; ID/OH mostly job-count-based [UNVERIFIED-L] | Location-dependent | [UNVERIFIED-L] |
| 22 | **DOE labs: CRADA, SPP, licensing, TCF** | Ongoing | **Company pays** (CRADA/SPP). TCF money goes to the lab with 50% partner match | **Licensing lab memory IP** (e.g., Sandia HZO FeRAM integrated into the trusted MESA fab, 2026-05) | Sandia [REPORTED via A1] ([Sandia, 2026-05-13](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/)); mechanisms [UNVERIFIED-H] |
| 23 | **DOE Lab-Embedded Entrepreneurship** (Chain Reaction Innovations/ANL, Innovation Crossroads/ORNL, Cyclotron Road–Activate/LBNL, West Gate/NREL) | Ongoing through 2025. 2026 funding unverified | Fellowship stipend plus R&D support for **full-time** technical founders (~2 yrs) | Device/materials founder (not this founder unless a technical co-founder applies) | [UNVERIFIED-M] |
| 24 | **NSF: I-Corps, NNCI fab access, SBIR** | Ongoing. NSF budget pressure in 2025–26 | I-Corps ~$50k per team; NNCI gives cleanroom access at academic-affiliate rates | Customer discovery (I-Corps); prototype devices (NNCI) | [UNVERIFIED-M] |
| 25 | **Buy American Act / TAA** | BAA domestic content **65% (2024–28) → 75% (2029)**; COTS exempt from the component test. TAA treats Korea, Taiwan and Japan the same as the U.S. | **No money and no real moat** for memory | — | [UNVERIFIED-H] |
| 26 | **FY2023 NDAA §5949** | Bars federal agencies from procuring products containing **CXMT, YMTC or SMIC** chips from **2027-12-23** (417 days) | No money. **Creates compliance demand** for provenance-verified memory | Provenance, test, screening, "clean" module supply | [REPORTED via p1-micron] ([XenoSpectrum, 2026-07](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/)); exact date [UNVERIFIED-H] |
| 27 | **DFARS counterfeit-parts rules; CMMC** | DFARS 252.246-7007/-7008 in force. **CMMC Phase 2 (Level 2 C3PAO) from ~2026-11-10** | Cost, not money: a CMMC L2 assessment for DoD-facing work [ESTIMATE: $30–100k] | Constrains recertified/broker concepts. Bar to entry for defense suppliers | [UNVERIFIED-H/M] |
| 28 | **BIS export controls** (Oct 2022, Oct 2023, Dec 2024 HBM, 2025 VEU and affiliates rules) | In force. **CXMT still not on the Entity List** as of mid-2026 (reports conflict). 50% affiliates rule reportedly suspended for 1 yr from ~2025-11-10, so **may resume ~2026-11-10** | — | Protects incumbents. Constrains HBM, advanced tools, and rad-hard exports | CXMT [REPORTED via p1-micron] ([TrendForce, 2025-05-16](https://www.trendforce.com/news/2025/05/16/news-u-s-rumored-to-mull-adding-dram-giant-cxmt-and-more-chinese-tech-firms-to-entity-list); [Simpson Thacher, 2025-10-17](https://www.stblaw.com/about-us/publications/view/2025/10/17/simpson-thacher-attorneys-author-i-law360-i-article-on-bis-50-rule-for-entity-list-and-other-export-restrictive-lists)); rule details [UNVERIFIED-M] |
| 29 | **ITAR / EAR rad-hard** (USML XV(d); ECCN 9A515.d/.e; 3A001.a.1) | In force | — | Rad-hard memory becomes export-controlled: smaller export market, more compliance cost | [UNVERIFIED-M] |

---

## 2. Decision-relevant findings and corrections to the mission premise

1. **The big federal capital is closed to us.**
   - CHIPS manufacturing money was almost entirely committed by January 2025 [UNVERIFIED-M].
   - The program now runs through the Investment Accelerator, which **trades money for equity or larger investment commitments** (Intel: ~9.9% stake, 433.3M shares × $20.47 ≈ **$8.87B** [ESTIMATE: arithmetic on UNVERIFIED-H terms]).
   - **§48D (35%, refundable) shuts to any project that has not begun construction by 2026-12-31** [REPORTED via p1-micron].
   - Plan every T2/T3 manufacturing concept with **0% CHIPS grant and 0% ITC**.
   - This *corrects* the implicit premise that "CHIPS money" is available to a new U.S. memory entrant. It is available to Micron (up to $6.165B ID/NY plus $275M Manassas [REPORTED via p1-micron]), not to us.
2. **The NSTC is not a usable on-ramp right now.** Commerce voided the Natcast operator agreement in Aug 2025 and moved the NSTC under NIST [UNVERIFIED-M]. Do not build a plan that needs NSTC membership, NSTC prototyping or NSTC funding until a 2026 operating model is published.
3. **SBIR/STTR is the only realistic non-dilutive money, but it has two problems:**
   - **Status:** authority lapsed 2025-10-01 [UNVERIFIED-H]. DoD SBIR memory topics were open again in July 2026 (DARPA DV017, ~$1.2M Direct-to-Phase II [REPORTED via A1]), so the program is evidently running. The **reauthorization terms are unverified**.
   - **Founder fit:** an SBIR PI must be primarily (>50%) employed by the awardee [UNVERIFIED-H]. **While the founder keeps his day job he cannot be the PI.** Routes are **STTR with a university PI** or a **hired full-time PI**.
4. **There is no general "U.S.-made memory" procurement preference, and nobody is paying a broad premium for it.**
   - TAA treats Korean, Taiwanese and Japanese DRAM as equal to U.S. DRAM.
   - BAA's component test does not apply to COTS items [UNVERIFIED-H].
   - Tariffs give U.S. memory no structural edge either: memory is outside Section 232 phase 1, and only China-origin chips pay 50% [REPORTED via p1-micron].
   - **What *does* exist is a "not-Chinese" requirement**: NDAA §5949 bans CXMT/YMTC/SMIC-containing products from federal procurement from **2027-12-23** [REPORTED via p1-micron; date UNVERIFIED-H].
   - **The moat is provenance, not U.S. origin.** This *corrects* the mission's "Made in America … potential moat". For federal and defense buyers, the paying need is **proof that there is no Chinese die**, plus trusted or rad-hard supply for a narrow set of programs.
5. **Trusted and rad-hard is the only place where U.S. memory earns a real premium today.** But it carries export controls (3A001.a.1, 9A515, possibly ITAR XV(d)), DMEA accreditation, CMMC, and incumbents (Honeywell, BAE Systems, Frontgrade, Infineon) [UNVERIFIED-M].
   - DoD is actively funding extreme-environment non-volatile memory (DARPA DV017 2026; USAF AF254-D0806 2025 [REPORTED via A1]).
   - Sandia has HZO FeRAM running in its trusted MESA fab (2026-05-13 [REPORTED via A1]). That is a **lab-licensing lead**.
6. **Export controls mostly protect incumbents and prolong the shortage. They do little for a U.S. startup.**
   - Tool controls (≤18nm-class DRAM since Oct 2022), the Dec 2024 HBM controls, and the 2025 revocation of Samsung/SK hynix China-fab VEU status [UNVERIFIED-M] slow Chinese and China-sited capacity.
   - **CXMT keeps shipping** (not Entity-Listed as of mid-2026 [REPORTED via p1-micron]).
   - For us, export controls mainly *constrain* rad-hard and HBM-class products and the hiring of foreign nationals (deemed exports). Software and CXL-type concepts are essentially unconstrained.
7. **Dated cliffs in the next 14 months that a plan must respect** [ESTIMATE: day counts from 2026-11-01]:

   | Date | What happens | Days from today |
   |---|---|---|
   | ~2026-11-10 | CMMC Phase 2 starts | 9 |
   | ~2026-11-10 | BIS affiliates-rule suspension may lapse | 9 |
   | 2026-12-31 | §48D construction-start deadline | 60 |
   | 2027-12-23 | §5949 effective | 417 |
   | 2029 | BAA 75% domestic content | — |

---

## 3. CHIPS and Science Act (late-2026 status)

### 3.1 What the Act appropriated (baseline)

CHIPS and Science Act, P.L. 117-167, signed **2022-08-09** [UNVERIFIED-H]. Total CHIPS appropriations were **$52.7B**:
- **$39B** manufacturing incentives (including up to $75B in loans and guarantees, and a ~$2B mature-node set-aside).
- **$11B** Commerce R&D: NSTC, NAPMP, Manufacturing USA institute(s), metrology.
- **$2B** DoD Microelectronics Commons.
- **$0.5B** State Department ITSI Fund.
- **$0.2B** workforce.

It also created the **25% §48D** credit [UNVERIFIED-H].

### 3.2 Awards and the Micron baseline

- By the Jan 2025 transition, Commerce had finalized most major awards and issued PMTs (preliminary memoranda of terms) for nearly all of the $39B [UNVERIFIED-M]. Sibling `p1-fabs` lists recipients (Intel $7.865B; TSMC; Samsung $4.745B; GF $1.5B; TI up to $1.6B; Polar ~$123M; SK hynix up to $458M + $500M loans; and others), mostly [UNVERIFIED].
- **Micron** has a final award of up to **$6.165B** (2024-12-10; ID ~$1.5B, NY ~$4.6B), amended June 2025 to add ID2, plus **$275M** for Manassas [REPORTED via p1-micron]. Micron's FY2026 10-K describes the direct funding as unchanged, with no equity conversion disclosed [REPORTED via p1-micron].
  - **Memory read-across:** Micron took the "invest more" path (the ~$200B U.S. plan, June 2025) rather than the equity path [REPORTED via p1-micron (Business Facilities)].

### 3.3 Reorganization under the current administration

- **2025-03-31: Executive Order establishing the "United States Investment Accelerator"** inside Commerce. It manages the CHIPS Program Office and facilitates >$1B investments [UNVERIFIED-H; EO number believed to be 14255, UNVERIFIED-M]. Secretary Lutnick told Congress and the press in 2025 that awards would be renegotiated for "better deals" and that some PMTs would not be finalized as written [UNVERIFIED-M].
- **2025-08-22: Intel equity deal** [UNVERIFIED-H]:
  - The U.S. took ~**9.9%** of Intel (433.3M shares at $20.47, ≈$8.9B).
  - It was funded by the **$5.7B** of unpaid CHIPS grants plus **$3.2B** of Secure Enclave funds.
  - The U.S. also got a 5-year warrant for a further 5% at $20, exercisable if Intel's ownership of its foundry falls below 51%.
  - The government agreed to vote with the board.
- **Other CHIPS-funded equity-style deals**, as I recall them [UNVERIFIED-M/L]:
  - Up to **$150M** to **xLight** (EUV free-electron-laser startup) for equity, Dec 2025, reported as the first CHIPS R&D award of the new administration.
  - Reports in 2025 of CHIPS funds redirected to critical-minerals and magnet deals (e.g., Vulcan Elements).
  - **Implication:** the Investment Accelerator does fund *startups*, but only strategic, $50M+ cheques in exchange for equity, on Commerce's initiative. It is not an application program a $40k founder can enter [ESTIMATE: judgment].
- **Awards that did not close** [UNVERIFIED-M]:
  - Wolfspeed's $750M PMT was never finalized; the company went through Chapter 11 in 2025.
  - Microchip reportedly paused its $162M process in 2025.
- **Open NOFOs in 2026:** none found [UNVERIFIED-M]. The 2023–24 incentive NOFOs, including the "small supplier" track for projects under ~$300M, appear closed or dormant.
  - **Precedent sizes for small-supplier awards (2024):** Rogue Valley Microdevices up to ~$6.7M; Akash Systems ~$18.2M; Infinera ~$93M [UNVERIFIED-M]. Even when open, the track needed capex projects of several million dollars or more and private co-investment.

### 3.4 Small-company access to CHIPS money today [ESTIMATE: judgment]

- **Direct:** effectively none.
- **Indirect routes:**
  - Become a **supplier or service provider to an awardee**: Micron ID/NY/VA, SK hynix Indiana packaging, GF, SkyWater.
  - Join an R&D consortium as a **sub-awardee**: SMART USA, NAPMP projects, Microelectronics Commons hubs.
  - Use **workforce-program** funded training.
- None of these is cash to the venture in year one.

### 3.5 §48D Advanced Manufacturing Investment Credit

- **Original terms:** 25% ITC for "qualified property" that is integral to an "advanced manufacturing facility" whose primary purpose is manufacturing semiconductors or semiconductor manufacturing equipment. Construction must begin **before 2027-01-01**. **Elective (direct) payment** is available, so it works without tax liability. There is a 10-year **recapture** if the taxpayer expands semiconductor capacity in a "foreign country of concern" [UNVERIFIED-H].
- **OBBBA** (P.L. 119-21, signed July 2025) raised the rate to **35%** for property **placed in service after 2025-12-31**. It did **not** extend the construction-start deadline [REPORTED via p1-micron: Baker Tilly; Instead 2026-03-31; Bloomberg 2025-07-01; SIA]. H.R. 3204 (BASIC Act) would extend to 2030 but is not enacted [REPORTED via p1-micron: Congress.gov].
- **Beginning construction:** Treasury's final §48D regulations (Oct 2024) use a physical-work test and a 5% safe harbor. They also clarified that wafer and ingot production can qualify [UNVERIFIED-M]. Whether **back-end test and packaging alone** qualifies as "manufacturing semiconductors" has to be checked in the final regs [UNVERIFIED-L].
- **For this venture:** a qualifying facility would have to start physical work, or incur 5% of cost, within **60 days**. No concept in the current pipeline is at that stage. **Model 0% ITC.** If the BASIC Act or a similar extension passes, a small packaging, KGD or test line could recover 35% of equipment cost in cash (e.g., $3M of tools gives $1.05M [ESTIMATE]). That makes it a **watch item**, not a plan.

---

## 4. NSTC, NAPMP, SMART USA, Microelectronics Commons

### 4.1 NSTC

- **Original design:** NIST chose **Natcast** (nonprofit) as NSTC operator (2023–24). Commerce and Natcast signed a large multi-year funding agreement shortly before the Jan 2025 transition, reported at ~$7.4B [UNVERIFIED-M].
- **Designated NSTC facilities (2024–Jan 2025)** [UNVERIFIED-M]:
  - The **EUV Accelerator** at Albany NanoTech (NY CREATES).
  - A **Prototyping and NAPMP Advanced Packaging Piloting Facility** in Arizona (ASU, Tempe).
  - A **Design and Collaboration Facility** in Sunnyvale, CA.
- **Aug 2025:** Secretary Lutnick called the Natcast arrangement unlawful (a "slush fund"), Commerce declined to fund it, and **NIST took direct control of NSTC functions** [UNVERIFIED-M]. Natcast then cut staff and wound down [UNVERIFIED-L]. Sibling `p1-fabs` reports that the Albany EUV Accelerator continues under NY CREATES [UNVERIFIED].
- **2026 status:** I could not verify whether NIST runs the NSTC directly, re-competed the operator role, or folded the R&D money into Investment-Accelerator-style deals such as xLight. **Treat NSTC membership, funding and facility access as unavailable until confirmed** [ESTIMATE].

### 4.2 NAPMP (National Advanced Packaging Manufacturing Program)

- About **$3B** of the R&D appropriation [UNVERIFIED-M].
- Nov 2024: up to **$300M** for advanced-substrate R&D, to Absolics (GA), Applied Materials, and Arizona State University [UNVERIFIED-M]. Plus a 2024–25 NOFO covering further R&D areas (chiplets, power delivery, thermal, connectors, co-design), with awards up to ~$150M each [UNVERIFIED-L].
- **Memory relevance:** HBM-class stacking and chiplet memory fall in NAPMP's scope.
- **Small-co path:** be a named team member on a university-led award. Any open calls in 2026 are unverified.

### 4.3 SMART USA (CHIPS Manufacturing USA institute)

- Semiconductor Research Corporation (SRC)–led institute focused on **digital twins** for semiconductor manufacturing, about **$285M** federal over 5 years (announced late 2024) [UNVERIFIED-M].
- **Membership** gives access to project calls.
- **Fit:** fab/test **software** (yield digital twins, test-flow simulation) suits a software founder better than any device program [ESTIMATE].
- 2026 operating status and membership fees: [UNVERIFIED].

### 4.4 DoD Microelectronics Commons

- **$2B over FY2023–27** from the CHIPS for America Defense Fund. **8 regional hubs** announced **2023-09-20** with ~$238M first-year funding [UNVERIFIED-H]:

| Hub | Lead / region | Memory relevance [ESTIMATE] |
|---|---|---|
| **NORDTECH** | Research Foundation for SUNY / NY CREATES, Albany NY | **High.** East Coast; 300mm tools at Albany NanoTech; AI hardware and HI |
| **NEMC** (Northeast Microelectronics Coalition) | MassTech, MA | Medium. East Coast; broad tech areas |
| **CLAWS** | NC State, NC | **Low.** Wide-bandgap focus |
| **SWAP** | Arizona State University, AZ | Medium. Prototyping and packaging |
| **Silicon Crossroads (SCMC)** | Applied Research Institute, IN | Medium. Near SK hynix West Lafayette HBM packaging |
| **MMEC** (Midwest Microelectronics Consortium) | Ohio | Low–medium |
| **California DREAMS** | USC, CA | Medium |
| **Northwest-AI-Hub** | Stanford, CA | **High.** AI hardware, CIM and eNVM research |

- **Project awards:** ~**$269M across 33 projects** announced Sept 2024 [UNVERIFIED-M]. Technical areas: secure edge/IoT, 5G/6G, **AI hardware**, quantum, electronic warfare, commercial leap-ahead. **AI hardware** is the natural home for compute-in-memory and embedded NVM. **I could not confirm any memory-specific Commons project** this session [UNVERIFIED].
- **How a small company joins** [UNVERIFIED-M]:
  1. Join the **Microelectronics Commons consortium** through its consortium manager (NSTXL; paid membership tiers).
  2. Join **one or more hubs** (some free; some charge fees).
  3. Get named on a hub's proposal in a project call.
  - Money flows through **Other Transaction** agreements via the hub, so small firms receive sub-awards rather than prime contracts.
- **Status risk:** the statutory window ends with FY2027 money. Whether Congress or DoD extends Commons beyond FY2027 is unknown [UNVERIFIED-L].

---

## 5. DoD: trusted supply, prototyping programs, memory needs

### 5.1 DMEA Trusted Accreditation Program

- DMEA (Defense Microelectronics Activity, Sacramento) accredits **Trusted Suppliers** by category: design, aggregation/brokering, mask data prep, photomask, wafer fabrication, packaging/assembly, test. There are on the order of 70–80 accredited suppliers [UNVERIFIED-M].
- DoDI 5200.44 requires trusted sources mainly for **custom/ASIC parts in mission-critical functions**. **COTS memory is normally bought commercially**, with counterfeit-avoidance controls rather than trust accreditation [UNVERIFIED-M].
- **Memory-relevant trusted or defense memory sources (U.S.)** [UNVERIFIED-M unless noted]:

| Source | Location | Memory relevance |
|---|---|---|
| **SkyWater** | Bloomington MN | Trusted wafer fab (Cat 1A, per p1-fabs, UNVERIFIED). Hosts **Weebit ReRAM in S130** [REPORTED via A2] |
| **GlobalFoundries** | Malta NY, Essex Junction VT | Trusted; 10-yr ~$3.1B DoD agreement 2023 (p1-fabs, UNVERIFIED) |
| **Honeywell Aerospace** | Plymouth MN | Rad-hard SRAM and MRAM; DoD-trusted fab |
| **BAE Systems** | Manassas VA | Rad-hard SRAM; trusted fab. **East Coast** |
| **Frontgrade** (formerly CAES/Cobham) | Colorado Springs | Rad-hard memories, including MRAM modules |
| **Sandia MESA** | Albuquerque | Government trusted rad-hard fab; HZO FeRAM integration 2026 [REPORTED via A1] |
| **Micross Components** | — | Bare die, including DRAM die, and hi-rel packaging. Trusted accreditation [UNVERIFIED-L] |
| **Mercury Systems** | — | Trusted secure memory/processing modules [UNVERIFIED-L] |

- **Micron is not known to me to be DMEA-accredited** [UNVERIFIED-L]. Verify on the DMEA list. If true, **no trusted-accredited U.S. DRAM wafer source exists**, which matters for any "trusted DRAM" concept.
- DMEA also runs a small government foundry (**ARMS**) that re-creates obsolete parts for DoD [UNVERIFIED-M]. It is a potential partner or competitor for **legacy memory replacement**.

### 5.2 RAMP-C, SHIP, Secure Enclave, T&AM

- **RAMP-C** (Rapid Assured Microelectronics Prototypes – Commercial): OUSD(R&E) program giving the defense industrial base access to Intel 18A (with IBM, Cadence, Synopsys and others) [UNVERIFIED-M].
- **SHIP** (State-of-the-art Heterogeneous Integration Prototype): NSWC Crane; Intel (digital) and Qorvo (RF) [UNVERIFIED-M].
- **Secure Enclave:** up to $3B to Intel (2024). The **$3.2B** balance was converted into the Aug 2025 equity stake [UNVERIFIED-H].
- **Relevance:** these are prime-scale programs. A memory chiplet startup could only ride them as an IP supplier inside an Intel/defense-prime package (e.g., an HBM or SRAM chiplet in a SHIP prototype). Not a near-term path [ESTIMATE].

### 5.3 Microelectronics strategy

- DoD treats microelectronics under its Trusted & Assured Microelectronics (T&AM) program and publishes roadmaps through OUSD(R&E) [UNVERIFIED-M].
- In late 2025 the department reportedly **narrowed its list of critical technology areas**. Whether microelectronics remained a stand-alone area is unverified [UNVERIFIED-L].
- **Do not cite a specific 2025–26 "DoD Microelectronics Strategy" document until it is found.**

### 5.4 DoD memory needs (where money and premiums exist) [UNVERIFIED-M; ESTIMATE judgments]

- **Rad-hard and rad-tolerant memory for space, strategic and nuclear systems:** SRAM, MRAM, NOR, FeRAM, and increasingly DDR4/DDR5 for on-board AI.
  - Incumbents are Honeywell, BAE, Frontgrade, Infineon (rad-hard SRAM/NOR) and Microchip.
  - Upscreened commercial DDR comes from Teledyne e2v and 3D Plus (European, marketed as **"ITAR-free"**) and Data Device Corp.
  - Unit prices are **orders of magnitude** above commercial [UNVERIFIED-L; no price source this session].
- **Extreme-environment NVM:** USAF **AF254-D0806** (500 °C-capable kB-scale NVM, manufacturing scale-up; 2025, closed) and DARPA **DPA26BZ04-DV017** (−269 °C to +600 °C, rad-tolerant, co-packaged NOR flash, ~$1.2M Direct-to-Phase II, 2026-07-22 → 2026-08-19) [REPORTED via A1]. **These are the only 2025–26 memory-specific DoD solicitations confirmed in this session's logs.**
- **Obsolescence / DMSMS (diminishing manufacturing sources and material shortages):** legacy DDR2/DDR3/DDR4 for fielded systems. DDR4 makers exiting in 2026 increases DMSMS pressure [REPORTED via A2: TrendForce 2026-01-19]. Micron Manassas 1-alpha DDR4 (May 2026) targets exactly this long-lifecycle buyer [REPORTED via p1-backend: eeNews 2026-05].
- **"Trusted DRAM":** no program found that pays for trusted/accredited commodity DRAM. DoD buys COTS DRAM under counterfeit-avoidance rules [UNVERIFIED-M].

### 5.5 DPA Title III; Office of Strategic Capital

- **DPA Title III:** I know of no award for DRAM, NAND or memory packaging [UNVERIFIED-L]. Title III microelectronics money has historically gone to rad-hard, specialty and packaging capacity at established firms. **Expect $0** for a startup in the first 3 years.
- **Office of Strategic Capital (OSC):** created Dec 2022. It issued its first loan notices in 2024 for "critical components" in critical-technology areas, including microelectronics [UNVERIFIED-M]. Size and terms in 2026 are unverified. This is **debt for revenue-generating capex**, relevant only later (T2+).

---

## 6. DARPA and IARPA

| Program | What | Memory relevance | Status (to my knowledge) | Small-co route | Tag |
|---|---|---|---|---|---|
| **NGMM** (Next-Generation Microelectronics Manufacturing) | National 3DHI prototyping center at **Texas Institute for Electronics (TIE), UT Austin**, ~$840M DARPA (2024) plus ~$552M Texas TSIF | 3D stacking of memory on logic; HBM-like integration prototypes | Phase 1 build-out 2024–26; Phase 2 later | Fee-for-service user / TIE member | [UNVERIFIED-M] |
| **OPTIMA** | Compute-in-memory accelerators (area/power-efficient in-memory MAC) | **Direct** (CIM) | Awarded ~2023; performer list not verified | Sub to performers; license results | [UNVERIFIED-L] |
| **MTO Microsystems Exploration (μE)** | Short, ~$1M-class seedlings via topic announcements | Possible for novel memory devices | Ongoing mechanism | Respond to μE topics | [UNVERIFIED-L] |
| **DARPA SBIR DPA26BZ04-DV017** | NVM for extreme environments | **Direct** | Closed 2026-08-19 | SBIR Direct-to-Phase II (~$1.2M) | [REPORTED via A1] |
| **ERI 2.0** | DARPA microelectronics umbrella incl. 3DHI | Indirect | Ongoing | — | [UNVERIFIED-M] |
| **JUMP 2.0** (SRC + DARPA, launched Jan 2023, 5 yrs, 7 centers) | **PRISM** (Processing with Intelligent Storage and Memory, UC San Diego); **SUPREME** (materials/devices, Cornell); **CHIMES** (heterogeneous integration, Penn State); **CoCoSys** and **COGNISENSE** (Georgia Tech); **ACE** (UIUC); **CUBIC** (connectivity, Columbia) | PRISM = memory-centric computing; SUPREME = ferroelectric/oxide devices; CHIMES = HI/packaging | Through ~2027 | SRC membership is expensive. The practical route is **licensing** university IP from these centers or **hiring** their graduates | [UNVERIFIED-M] |
| **IARPA** | AGILE (data-movement-centric architectures, ~2020–25) was the closest | Indirect | No current memory program confirmed | — | [UNVERIFIED-L] |

**Read-across [ESTIMATE]:**
- DARPA money for memory in 2025–26 is **niche** (extreme environment, CIM). It suits a device concept with a technical PI.
- It does not fund commodity DRAM, CXL software or brokerage.
- The East Coast–relevant JUMP centers are **CUBIC (Columbia, NYC)**, **SUPREME (Cornell, NY)** and **CHIMES (Penn State, PA)**.

---

## 7. SBIR/STTR

### 7.1 Authorization status

- The SBIR and STTR Extension Act of 2022 extended both programs to **2025-09-30** [UNVERIFIED-H].
- **Authority lapsed on 2025-10-01.** That was the same day the government shutdown began; the shutdown ended ~2025-11-12. Agencies paused new solicitations and awards [UNVERIFIED-H].
- **Competing reauthorization approaches in 2025** [UNVERIFIED-M]:
  - The Senate Small Business chair (Sen. Ernst) sought reforms: limits on high-volume "SBIR mill" awardees, stronger foreign-ties due diligence, and larger "strategic breakthrough" follow-on awards.
  - House leaders favored a cleaner multi-year extension.
- **Evidence the program is running again in 2026:**
  - DoD SBIR topic **DPA26BZ04-DV017** opened **2026-07-22** and closed **2026-08-19** [REPORTED via A1]. A DoD component would not open a new SBIR cycle without authority.
  - **Inference:** SBIR/STTR authority was restored (reauthorized or extended) by mid-2026 [ESTIMATE: inference, moderate confidence].
  - **The length and terms are NOT verified.** Check the enacting public law, any changed award caps, mill limits, and any new foreign-risk certification. This is the #1 item in §14.

### 7.2 Award sizes (ceilings move; verify per solicitation)

| Agency | Phase I | Phase II | Notes | Tag |
|---|---|---|---|---|
| SBA guideline caps (2024 adjustment) | ~$314k | ~$2.1M | Agencies may exceed with SBA waiver | [UNVERIFIED-L] |
| DoD (Army/Navy/AF/DARPA/MDA/DMEA) | ~$50k–$250k | ~$0.75M–$1.9M | **Direct-to-Phase II** common; DV017 ~$1.2M | [REPORTED via A1] for DV017; rest [UNVERIFIED-M] |
| AFWERX TACFI / STRATFI | — | Matching: TACFI ~$0.4–2M; STRATFI up to ~$15M gov't with ≥1:1 private/program match | For Phase II performers with a transition customer | [UNVERIFIED-M] |
| NSF SBIR/STTR (America's Seed Fund) | up to ~$305k | up to ~$1.25M | Project Pitch first; equity-free; broad topics incl. semiconductors and AI systems | [UNVERIFIED-M] |
| DOE SBIR/STTR | ~$200–250k | ~$1.1–1.6M | Topics via Office of Science (incl. microelectronics) | [UNVERIFIED-L] |
| NASA SBIR/STTR | ~$150k | ~$850k–$1M | Topics on rad-tolerant avionics and memory recur | [UNVERIFIED-L] |

### 7.3 Eligibility rules that hit this founder hardest [UNVERIFIED-H, from SBA Policy Directive]

- **PI primary employment:** for **SBIR**, the PI's primary employment (>50% of time) must be with the awardee at award and during the project. **A founder who keeps a full-time day job cannot be SBIR PI.**
- **STTR** lets the PI be employed by the partner research institution. It requires ≥40% of work by the small business and ≥30% by the research institution.
- **Work share:** SBIR Phase I ≥ 2/3 and Phase II ≥ 1/2 of the work must be performed by the small business.
- **Ownership:** ≤500 employees; >50% owned and controlled by U.S. citizens or permanent residents (some agencies allow VC-majority).
- **Foreign-risk due diligence** (from the 2022 Act): agencies screen for ties to PRC talent programs, PRC ownership and similar. A team member with PRC-entity affiliations can sink an application [UNVERIFIED-H].
- **Upside:**
  - **SBIR data rights** are protected for 20 years.
  - **Phase III** awards can be made **sole-source** by any federal agency, with no dollar cap and no SBIR funds required. This is how SBIR becomes **revenue** rather than grant farming [UNVERIFIED-H].

### 7.4 Relevant recent or open memory topics

**Confirmed (via sibling logs):**
- **DARPA DPA26BZ04-DV017**: NVM for extreme environments (~$1.2M, D2P2, closed 2026-08-19).
- **USAF AF254-D0806**: 500 °C kB-scale NVM manufacturing scale-up (2025, closed; cites ferroelectric-diode memory stable to 600 °C) [REPORTED via A1].

**Likely recurring areas** (to search on sbir.gov / dodsbirsttr.mil once the network is available) [ESTIMATE]:
- Rad-hard/rad-tolerant DDR4/DDR5 and NVM for space (AF/SSC/NASA/MDA).
- DMSMS and legacy-part replacement (DLA, Navy).
- Microelectronics **supply-chain illumination and counterfeit detection** (DoD-wide; fits §5949 provenance).
- Compute-in-memory for edge AI (Army/AF).
- Energy-efficient microelectronics (DOE, aligned with the EES2 initiative).
- NSF open topics in semiconductors and AI-systems software (memory tiering, KV-cache management).

---

## 8. State incentives: what a small company can actually get

| State | Headline program | Small-company reality | Tag |
|---|---|---|---|
| **New York** | **Green CHIPS** (2022): up to $10B of refundable Excelsior tax credits over 20 years for very large "green CHIPS projects". **Micron up to $5.5B** | Green CHIPS is megaproject-only (high investment and job thresholds). A small NY firm can use: **Excelsior Jobs Program** credits (job-based); **FuzeHub** manufacturing grants (~$50k class); **NYSTAR** Centers for Advanced Technology/Centers of Excellence matching; **START-UP NY** tax-free zones on campuses; fee-based **NY CREATES/Albany NanoTech** 300mm tool access; **NORDTECH** hub membership | Micron $5.5B [REPORTED via p1-micron]; rest [UNVERIFIED-M/L] |
| **Idaho** | Idaho Reimbursement Incentive (rebate of up to ~30% of new income/payroll/sales taxes for up to 15 yrs; job thresholds) | Little for a sub-20-person firm. Value is proximity to Micron Boise supplier programs | [UNVERIFIED-L] |
| **Arizona** | ACA **Arizona Innovation Challenge** (~$100–150k grants); refundable **Qualified Facility** credit (manufacturing/HQ/R&D capex); **SWAP** hub and ASU MacroTechnology Works | The Innovation Challenge is the realistic small-co cash. SWAP/ASU gives prototyping and packaging access | [UNVERIFIED-L/M] |
| **Texas** | **Texas CHIPS Act (2023)**: Texas Semiconductor Innovation Fund (TSIF, ~$698M initial) and Texas Semiconductor Innovation Consortium. TSIF matched **TIE $552M** | TSIF grants skew to universities and large projects. A small firm benefits mostly as a **TIE/NGMM user**. Texas Enterprise Fund is job-count-driven | [UNVERIFIED-M] |
| **Ohio** | JobsOhio (Intel package ~$2B); **Ohio Third Frontier** (Technology Validation & Start-up Fund; historically SBIR-related incentives); MMEC hub | Third Frontier is the small-co route [UNVERIFIED-L]. Intel Ohio slipped to ~2030–31 (p1-fabs [UNVERIFIED]) | [UNVERIFIED-L] |
| **Virginia** | VIPC **Commonwealth Commercialization Fund (CCF)** (~$50–100k grants incl. SBIR-adjacent); VIPC venture funds; incentives for Micron Manassas | CCF is directly accessible. Manassas (Micron Fab 6, BAE Systems) is an East Coast defense-memory cluster | [UNVERIFIED-M/L] |
| **Massachusetts** | **MassVentures START** (SBIR Phase II companies; staged grants ~$100k–$500k total); MassTech's **NEMC** hub; Mass Leads Act (Nov 2024) economic-development package incl. the M2I2 manufacturing-innovation grants | START is the best small-co cash in the Northeast for an SBIR-stage company | [UNVERIFIED-M/L] |
| **North Carolina** | **One NC Small Business Program**: SBIR/STTR proposal-cost reimbursement (~$12k) and Phase I **matching funds** (~$100–150k); CLAWS hub (wide-bandgap); SMART USA ties to RTP | Matching is accessible but only after a federal Phase I award | [UNVERIFIED-M/L] |

**Read-across [ESTIMATE]:**
- No state program funds a T0 founder's first $50k.
- State money **multiplies SBIR** (MA START, NC One NC, VA CCF) or **subsidizes jobs**.
- For an East Coast founder:
  - **NY** (NY CREATES and NORDTECH access; Micron Clay supplier ecosystem) and **VA** (Manassas memory/defense cluster) are the most memory-relevant.
  - **MA** has the richest SBIR-match program.

---

## 9. DOE national labs, tech transfer, and NSF infrastructure

### 9.1 Labs with memory-relevant work

| Lab | Memory-relevant assets | Use for a small venture | Tag |
|---|---|---|---|
| **Sandia** (NM) | **MESA** trusted rad-hard CMOS fab. **HZO ferroelectric memory integrated into MESA at 200mm**: FeRAM plus binary and 32-state FTJs (LDRD; 2026-05-13). Radiation test facilities | **License or CRADA the HZO FeRAM/FTJ IP** for a rad-hard NVM product. Rad testing | HZO [REPORTED via A1]; rest [UNVERIFIED-M] |
| **Los Alamos** (NM) | **LANSCE** neutron beam (ICE House / WNR), widely used by industry for **single-event-effect testing of DRAM/SRAM** | Paid beam time for qualifying rad-tolerant or upscreened memory | [UNVERIFIED-M] |
| **Oak Ridge** (TN) | CNMS nanoscience user facility; neuromorphic/materials work; **Innovation Crossroads** (LEEP) | Free non-proprietary user access by proposal; LEEP fellowship | [UNVERIFIED-M] |
| **Lawrence Berkeley** (CA) | **Molecular Foundry**; X-ray characterization (ALS); oxide/ferroelectric materials; **Cyclotron Road** (with Activate) | User access; LEEP fellowship | [UNVERIFIED-M] |
| **Argonne** (IL) | Center for Nanoscale Materials; APS X-ray; microelectronics co-design; **Chain Reaction Innovations** (LEEP) | User access; LEEP | [UNVERIFIED-M] |
| **NREL** (CO) | **West Gate** (LEEP), energy-focused | Low memory relevance | [UNVERIFIED-M] |
| **PNNL** (WA) | Data-centric/memory-centric HPC architecture research | Software and architecture collaboration | [UNVERIFIED-L] |
| **Brookhaven** (NY) | Center for Functional Nanomaterials; NSLS-II. **East Coast** | User access for materials characterization | [UNVERIFIED-M] |

- **DOE Microelectronics Science Research Centers:** about **$179M** for three centers (Aug 2024), led by national labs, covering energy-efficient microelectronics, extreme environments and lithography/materials [UNVERIFIED-L; names not re-checked].
- **DOE AMMTO "EES2"** (Energy Efficiency Scaling for 2 Decades): an industry-pledge initiative targeting 1,000× microelectronics energy efficiency. It aligns DOE funding with **W/GB and data-movement energy**, which is the axis where memory-efficiency concepts win [UNVERIFIED-M].

### 9.2 Mechanisms [UNVERIFIED-H unless noted]

- **CRADA:** no federal money flows to the company. The company contributes funds or in-kind work, and IP terms are negotiated. Useful for co-developing with lab staff on licensed IP.
- **Strategic Partnership Projects (SPP):** the company pays the lab for work.
- **Licensing:** labs license patents, often with startup-friendly terms (option agreements, deferred fees). This is **the cheapest way for a non-engineer to own memory IP** (mission §3E). Sandia HZO is the strongest lead in this repo.
- **Technology Commercialization Fund (TCF):** DOE OTT money goes **to the lab** for maturation with an industry partner who provides **≥50% match** [UNVERIFIED-M].
- **Lab-Embedded Entrepreneurship Program (LEEP):** ~2-year fellowships for **full-time technical founders**, with stipend, R&D budget and lab access. Programs are Chain Reaction Innovations (ANL), Innovation Crossroads (ORNL), Cyclotron Road (LBNL/Activate) and West Gate (NREL) [UNVERIFIED-M]. Activate runs similar NSF- and philanthropy-backed fellowships outside labs [UNVERIFIED-M]. **Not for a founder keeping a day job; possibly for a technical co-founder.**
- **Energy I-Corps:** for **lab researchers**, not outside companies.
- **New Mexico Small Business Assistance (NMSBA):** free Sandia/LANL technical help, but **only for NM businesses** [UNVERIFIED-M].
- **Discovery:** DOE's Lab Partnering Service portal and each lab's tech-transfer office.

### 9.3 NSF infrastructure that matters for prototypes [UNVERIFIED-M]

- **NNCI** (National Nanotechnology Coordinated Infrastructure) sites give **outside companies cleanroom access** at published hourly rates. This is the cheapest legitimate way to fabricate device test structures without owning a fab.
- **East Coast sites** include Cornell CNF, Penn Singh Center, Harvard CNS, MIT.nano, Georgia Tech IEN and RTNN (NC State/Duke/UNC).
- **NSF I-Corps** (~$50k per team) funds customer discovery. It is the right first grant for a software/market concept and needs no PI employment test, but requires an academic team lead [UNVERIFIED-M].

---

## 10. Procurement preference: does "U.S.-made memory" get paid for?

### 10.1 Buy American Act (BAA) [UNVERIFIED-H]

- **Domestic end product test:** the item is manufactured in the U.S. **and** domestic components exceed a cost threshold of **60% (2022–23), 65% (2024–28), 75% (2029+)**. Fallback and enhanced-preference rules apply for "critical items".
- **Price preference** in evaluation:
  - Civilian agencies add **20%** to foreign offers if the low domestic offer is from a large business, **30%** if from a small business.
  - **DoD uses 50%**.
- **The catch for memory:** the **component test is waived for COTS items** (41 U.S.C. 1907). A memory module assembled in the U.S. from imported DRAM dies can still be a domestic end product, provided the U.S. assembly counts as manufacturing. Conversely, a U.S. DRAM die gets no extra credit when it goes into a COTS product.
- **The bigger catch:** BAA applies only where TAA does not (below the TAA threshold, or exempt buys).
- **2025 FAR rewrite:** the "Revolutionary FAR Overhaul" under the April 2025 procurement executive order is rewriting FAR Part 25. Check that the thresholds and COTS waiver survive [UNVERIFIED-M].

### 10.2 Trade Agreements Act (TAA) [UNVERIFIED-H/M]

- Above the WTO GPA threshold (~$174k for supplies in 2024–25; adjusted every two years), agencies may buy only U.S.-made or **designated-country** end products.
- **Korea, Taiwan, Japan, the EU, Singapore and Israel are designated. China is not; Malaysia is not.**
- For integrated circuits, CBP generally assigns origin to the country of **wafer diffusion**, not assembly [UNVERIFIED-M].
- **So:** Samsung, SK hynix, Micron-Taiwan/Japan DRAM is TAA-compliant. CXMT DRAM in an end product being sold *as* the end product is not. **TAA gives a U.S. memory maker no advantage over Korean, Taiwanese or Japanese memory.**

### 10.3 FY2023 NDAA §5949: the one real memory-specific preference

- Enacted **2022-12-23** (P.L. 117-263). Effective **5 years after enactment, i.e., 2027-12-23** [UNVERIFIED-H]. Sibling reporting says "Dec 2027" [REPORTED via p1-micron (XenoSpectrum)].
- **Prohibits executive agencies from:**
  1. procuring or obtaining any electronic part, product or service that **includes covered semiconductor products or services**; and
  2. contracting with an entity to procure or obtain electronic parts or products that **use** them (scope language on "critical systems" to be checked).
- **Covered:** semiconductors designed, produced or provided by **SMIC, YMTC, CXMT**, their subsidiaries, affiliates or successors, plus entities later designated (owned or controlled by a foreign country of concern) [UNVERIFIED-M].
- **Waivers** are possible. The **FAR implementing rule's status is unverified** [UNVERIFIED-L].
- **Political salience is rising:**
  - In 2026 Apple lobbied Commerce for permission to buy CXMT DRAM. Senators demanded Apple commit by 2026-08-21 not to [REPORTED via p1-micron] ([The Next Web, 2026-06-27](https://thenextweb.com/news/apple-lobbying-us-approval-cxmt-blacklisted-memory-chips); [Sen. Schumer, 2026-07-30](https://www.schumer.senate.gov/newsroom/press-releases/citing-core-national-security-and-economic-reasons-schumer-demands-apple-reject-chinese-military-linked-chips)).
  - CXMT was re-added to the DoD 1260H list ~June 2026 [REPORTED via p1-micron].
- **What it creates [ESTIMATE: judgment]:**
  - Every federal contractor shipping servers, PCs, networking or embedded systems needs **component-level proof of no CXMT/YMTC die** by end-2027.
  - Chinese dies are often sold inside third-party-branded modules and SSDs, so proof needs **die-level provenance** (supplier attestations, plus X-ray/decap or marking analysis on samples).
  - **This is a paid compliance need with a hard date. It is the most concrete "U.S. policy creates a buyer" signal for a small memory venture**, and it fits a software/test/provenance concept (T0–T1) far better than a fab concept.
  - It **rewards "verified non-Chinese," not "U.S.-made"**: Korean and Taiwanese memory satisfies it.

### 10.4 DFARS and DoD rules [UNVERIFIED-H unless noted]

- **DFARS 252.246-7007/-7008 (counterfeit electronic parts):** DoD contractors must buy from original manufacturers or authorized distributors where available. Otherwise they must use "contractor-approved suppliers" under industry standards (AS6081/AS5553) with traceability and testing, and they bear liability for counterfeits. **Directly constrains a recertified/recovered-DRAM concept in the defense channel.** Such parts sell only with documented traceability and test (and at a discount), or to non-DoD buyers.
- **DFARS 252.204-7018 / FAR 52.204-25 (Section 889):** the telecom-equipment ban is the precedent for how §5949 compliance will work (representations, reasonable inquiry). Its ecosystem of compliance tooling is a template [ESTIMATE].
- **CMMC 2.0:**
  - 32 CFR Part 170 in force since **2024-12-16**.
  - DFARS clause rule effective **~2025-11-10**.
  - **Phase 1** (self-assessments) from ~2025-11-10. **Phase 2** (Level 2 third-party C3PAO certification in solicitations) from **~2026-11-10**. Phases 3–4 in 2027–28 [UNVERIFIED-M].
  - A memory firm handling CUI for DoD needs Level 2: an assessment plus NIST SP 800-171 controls, roughly **$30–100k+** first-year cost [ESTIMATE: typical small-business quotes, not sourced this session].
- **Specialty metals / DFARS 225.7018 magnets:** not relevant to memory.

### 10.5 Is anyone paying for U.S.-made memory? [ESTIMATE: judgment from the above]

- **Federal civilian and commercial buyers:** no general premium. TAA/BAA do not distinguish U.S. from allied memory, and Section 232 phase 1 does not tariff memory [REPORTED via p1-micron].
- **DoD (trusted, rad-hard, DMSMS):** **yes, but narrow.** Premiums are paid for rad-hard parts and for guaranteed long-lifecycle supply. Micron Manassas (DDR4/LP4 for auto, defense and industrial) is positioning for this [REPORTED via p1-backend].
- **Policy optionality:** a future Section 232 phase 2 or a "tariff offset" regime (Taiwan's deal gives duty-free import quota for U.S. capacity [REPORTED via p1-micron]) could create a U.S.-origin premium. Lutnick's ~100% memory-tariff threat (2026-01-16) is **not implemented** [REPORTED via p1-micron]. **Price it at zero today.**

---

## 11. Export controls and ITAR

### 11.1 BIS semiconductor rules timeline (memory-relevant)

| Date | Rule | Memory content | Tag |
|---|---|---|---|
| **2022-10-07** | Advanced computing and semiconductor manufacturing interim final rule (87 FR 62186) | License requirement for items destined to China fabs producing **DRAM ≤18nm half-pitch**, **NAND ≥128 layers**, or logic ≤16/14nm. U.S.-person support restrictions | [UNVERIFIED-H] |
| **2022-12** | Entity List additions | **YMTC** added | [UNVERIFIED-H] |
| **2023-10-17** | Updated advanced computing and SME rules | Expanded SME controls and country scope. Performance-density metric for AI chips | [UNVERIFIED-M] |
| **2024-12-02** (FR 2024-12-05, 89 FR 96790) | FDP rule additions; SME and HBM controls | **HBM controlled** (new **3A090.c**: memory-bandwidth density >2 GB/s/mm²; HBM2E and above effectively licensed to China). **24 SME types + 3 software tools.** DRAM "advanced-node" test redefined as **cell area <0.0019 µm² or density >0.288 Gb/mm²** (replacing ≤18nm half-pitch). ~140 Entity List additions. **CXMT left off** | Rule [UNVERIFIED-M]; CXMT omission [REPORTED via p1-micron] |
| 2025-01 | AI Diffusion rule (rescinded May 2025); foundry due-diligence rule | Logic/AI focus. Not memory-specific | [UNVERIFIED-M] |
| **2025-08-29** | **VEU revocation** for Samsung China, SK hynix China and Intel Dalian (now SK hynix), effective **2025-12-31** | Chinese DRAM/NAND fabs of Korean firms need licences. BIS signalled licences for status-quo operation but **not capacity expansion or tech upgrades**. Reportedly annual licences granted for 2026 [UNVERIFIED-L] | [UNVERIFIED-M] |
| **2025-09-29** | **Affiliates ("50%") rule** | Entity List / MEU restrictions extend to ≥50%-owned affiliates. **Reportedly suspended for one year from ~2025-11-10** under the U.S.–China truce (Busan, 2025-10-30). **May resume ~2026-11-10** absent extension | Rule [REPORTED via p1-micron: Simpson Thacher]; suspension [UNVERIFIED-M] |
| **2026-01** | 232 proclamation and a BIS rule on advanced-chip exports to China (H200-class case-by-case) | Not memory directly. HBM counted only via accelerator thresholds | [REPORTED via p1-micron (Covington; CRS)] |
| **2026 (to mid-year)** | **CXMT status** | **Not on the Entity List** as of mid-2026 (reports conflict). On the DoD **1260H** list (re-added ~June 2026). Considered for listing again in 2025 | [REPORTED via p1-micron] |

### 11.2 What they restrict, and who they help

- **Restricted:**
  - Exports to China of HBM (3A090.c).
  - Tools, software and technology for advanced DRAM/NAND (3B001/3B090/3B993, 3D/3E).
  - U.S.-person support to Chinese advanced fabs.
  - Upgrades at Samsung and SK hynix China fabs (post-VEU).
  - Dealings with listed entities (YMTC and others) [UNVERIFIED-M].
- **Not restricted:**
  - Imports of Chinese memory into the U.S. That is handled by tariffs (50% Section 301 on China-origin chips [REPORTED via p1-micron]) and by §5949 procurement rules, not export controls.
  - CXMT's mature-node DDR4/DDR5/LPDDR5 sales.
- **Effect on supply [ESTIMATE]:**
  - The controls slow CXMT/YMTC technology advances and freeze capacity at the Korean firms' China fabs (SK hynix Wuxi is a large share of its DRAM wafers [UNVERIFIED-M]). That tilts toward a **longer shortage** and supports Micron's U.S. build-out.
  - They do not stop Chinese legacy-node output, which drove the 2024–25 DDR4 price collapse.
- **Related regimes:**
  - **Treasury outbound investment rule** (31 CFR Part 850, effective **2025-01-02**): prohibits or requires notification for U.S.-person investment in PRC entities developing or producing advanced ICs, including DRAM/NAND above thresholds [UNVERIFIED-M]. It bars a "partner with a Chinese memory fab" path.
  - **CFIUS:** a U.S. startup whose products are export-controlled (e.g., 3A001.a.1 rad-hard) is a "critical technology" business. Some foreign investments into it can trigger **mandatory CFIUS filing**. This narrows the investor pool [UNVERIFIED-M].

### 11.3 Rad-hard memory: ITAR vs EAR

- **USML Category XV(d)** (ITAR): radiation-hardened microelectronic circuits that meet **all five** of:
  1. total dose ≥5×10⁵ rad(Si);
  2. dose-rate upset ≥5×10⁸ rad(Si)/s;
  3. neutron fluence ≥1×10¹⁴ n/cm²;
  4. SEU ≤1×10⁻¹⁰ errors/bit-day;
  5. SEL-free at LET ≥80 MeV·cm²/mg.

  [UNVERIFIED-M]. A memory meeting all five is **ITAR**. That means DDTC registration (~$3k/yr Tier 1 [UNVERIFIED-L]), U.S.-person-only access to technical data, and licences for nearly all exports.
- **ECCN 9A515.d / .e** (EAR, "spacecraft" series): radiation-hardened/-tolerant microelectronic circuits below the XV(d) bar but meeting the ECCN's specified thresholds or "specially designed" for spacecraft. Licences are needed to most destinations, with limited licence exceptions [UNVERIFIED-L: check exact thresholds in 15 CFR 774 Supp. 1].
- **ECCN 3A001.a.1** (EAR, NS/MT-type controls): ICs rated or designed as radiation-hardened to withstand **total dose ≥5×10³ Gy(Si)** (=500 krad), **or dose-rate upset ≥5×10⁶ Gy(Si)/s**, **or neutron fluence ≥5×10¹³ n/cm²** (1 MeV eq.) [UNVERIFIED-M]. A licence is needed for many non-allied destinations. Releasing the technology (3E001) to foreign-national employees is a **deemed export**.
- **Practical effect [ESTIMATE]:**
  - A U.S. rad-hard memory product sells mainly to U.S. primes and allied space programs.
  - It competes against European "ITAR-free" parts (3D Plus, Teledyne e2v) that market precisely on avoiding these rules.
  - Compliance (classification, Technology Control Plan, licences) costs ~$25–75k/yr for a small firm. This estimate is unsourced.
  - **Protection** comes from DoD trusted/domestic-sourcing preferences on specific programs, not from export controls themselves.

### 11.4 Which venture concepts are constrained vs protected [ESTIMATE: judgment, built on 11.1–11.3]

| Concept family (mission §3) | Export/ITAR exposure | Protection from policy | Net |
|---|---|---|---|
| Software: KV-cache/tiering, compression, price intelligence, QVL tools (§3D) | EAR99 / 5D992 mass-market; only Entity-List/end-use screening | None needed | **Unconstrained** |
| CXL memory appliances/pooling (§3B) | Generally 4A994/5A992/EAR99. Becomes 4A090-adjacent if bundled with controlled GPUs to China | None | Lightly constrained |
| Provenance/test/compliance service for §5949 (§3C) | EAR99 services. Possible deemed-export care if doing failure analysis on controlled parts | **§5949 creates the demand** (2027-12-23) | **Protected by policy demand** |
| Recertified/recovered DRAM (§3C) | EAR99 exports; China military-end-user rule (§744.21) screening | Counterfeit rules (DFARS) **constrain** DoD sales. 50% Section 301 on China-origin dies applies on import [ESTIMATE: duty follows origin] | Constrained in defense; open commercially |
| Trailing-node / legacy DRAM made in U.S. (§3C) | Commodity DRAM is not controlled (EAR99/3A991-type) | Indirect: §5949 and the 50% China tariff tilt federal and U.S. channels toward non-Chinese supply. **No U.S.-origin premium** (TAA/BAA). Competes with Micron Manassas | Weakly protected |
| HBM/advanced stacked memory/packaging (§3B/§3C) | **3A090.c** licence to China; tool/tech controls | Benefits from China being cut off from HBM | Constrained on China sales (irrelevant at small scale) |
| Rad-hard / extreme-environment NVM, e.g., HZO FeRAM, ReRAM on SkyWater S130 (§3A) | **3A001.a.1 / 9A515.d-e / possibly USML XV(d)**; deemed exports | DoD trusted-supply preference; SBIR topics | **Constrained exports, protected U.S. defense market** |
| Oxide-semiconductor/FeRAM/MRAM device IP for licensing (§3A) | Technology controls only if the item is controlled. Deemed exports for PRC nationals on controlled tech | None | Mostly unconstrained; licensing to Chinese fabs restricted if advanced |
| Used-tool/200mm capacity arbitrage (§3A(c)) | Selling DRAM-capable tools or tech to China needs licences | Controls keep some used tools in the non-China market [ESTIMATE] | Mixed |

---

## 12. Fit matrix: which concepts are fundable with non-dilutive money? [ESTIMATE: judgment]

| Concept family | Best non-dilutive routes | Realistic first-24-month $ | Blocking requirement |
|---|---|---|---|
| Rad-hard / extreme-environment NVM (device) | DoD SBIR/STTR (DARPA, AF, SSC, NASA); Sandia license + CRADA; Microelectronics Commons sub-award; AFWERX STRATFI later | $0.3–2M (Phase I → D2P2) | **Technical PI working full time**; DMEA/ITAR/CMMC compliance; foundry (SkyWater) |
| CIM / memory-centric accelerators | DARPA (OPTIMA follow-ons, μE), NSF SBIR, JUMP 2.0 IP license | $0.3–1.5M | Technical PI; tape-out budget |
| Oxide-DRAM / FeRAM / MRAM IP licensing | DOE CRADA/TCF (lab gets money); NSF SBIR; NNCI fab access | $0.2–1.3M | Technical PI; lab license |
| Packaging / KGD / test line | (CHIPS and 48D effectively closed); state job credits; OSC debt later | ≈$0 grant; debt later | Private capital |
| §5949 provenance / screening / compliance | DoD SBIR (supply-chain illumination, counterfeit detection); DLA/DMSMS topics; state SBIR matches | $0.15–1.2M | SBIR PI rule (use STTR or hire). **Revenue from compliance customers is the real goal** |
| Memory-efficiency software (KV-cache, tiering, CXL orchestration) | NSF SBIR (AI/systems); DOE (EES2-aligned energy efficiency); NSF I-Corps for discovery | $0.05–1.5M | SBIR PI rule; NSF commercial-impact bar |
| Price intelligence / marketplace / QVL tools | Essentially none (commercial) | $0 | — |
| Recertified DRAM brokerage | None; DFARS counterfeit rules constrain the DoD channel | $0 | AS6081-type quality system to sell into defense |
| Trailing-node U.S. DRAM fab (T3/T4) | Would need Investment Accelerator equity, state megaproject money, DoD | Not available to this founder | Rule 3 / capital |

---

## 13. Implications for the venture

1. **Do not plan on CHIPS, §48D, NSTC or DPA money.** Use 0% in every model for T0–T2 concepts. (This narrows "fundable with non-dilutive money" to SBIR/STTR, DOE lab partnerships and small state matches.)
2. **The single most important policy demand signal is §5949 (2027-12-23)**, not "Made in America." A provenance, screening and "verified non-Chinese memory" offering fits:
   - the founder's software and operations skills;
   - T0–T1 capital;
   - a hard deadline 13.7 months out;
   - a credible DoD SBIR angle (supply-chain illumination).

   Phase 2/3 should card and score it explicitly. **Glut-proofing:** the compliance need persists in a glut because it is regulatory, not price-driven [ESTIMATE].
3. **If any device concept survives** (e.g., rad-hard HZO FeRAM via a Sandia license on SkyWater or MESA; ReRAM on S130), the funding path is **STTR with a university PI, or a full-time technical co-founder as SBIR PI**. Pair it with a Sandia CRADA, DoD SBIR D2P2 (~$1.2M class), then **SBIR Phase III sole-source** production as revenue. Budget ~$25–75k/yr of export and CMMC compliance [ESTIMATE].
4. **East Coast assets to use:**
   - NY: NY CREATES/Albany NanoTech, NORDTECH hub, Cornell CNF, Brookhaven CFN; Columbia (CUBIC) and Cornell (SUPREME) JUMP centers.
   - MA: MassVentures START.
   - VA: Manassas memory/defense cluster (Micron Fab 6, BAE Systems).
   - PA: Penn State CHIMES and Penn's AlScN ferroelectric work (A1).
5. **Watch items that could change the calculus:**
   - A **§48D extension** (BASIC Act).
   - A **Section 232 phase 2** that tariffs memory and creates a U.S.-origin premium.
   - **CXMT Entity-Listing** (would sharpen §5949 demand and possibly cut CXMT's tool access).
   - Resumption of the **affiliates rule** (~2026-11-10).
   - **SBIR reauthorization terms.**
   - A published **NSTC 2026 operating model**.

---

## 14. Verification queue (priority order; where to check)

Each item names the primary place to check. All of these were blocked or search-budget-limited this session.

1. **SBIR/STTR reauthorization:** public law number, date, length, changed caps and PI rules (sbir.gov news; congress.gov). Also current Phase I/II ceilings (SBA Policy Directive).
2. **CHIPS Program Office / U.S. Investment Accelerator 2026 status:** any open NOFOs; list of renegotiated awards; equity deals (nist.gov/chips; commerce.gov press releases).
3. **NSTC 2026 operating model** after Natcast; Albany EUV Accelerator and Arizona PPF access terms (nist.gov; NY CREATES).
4. **CXMT Entity List status:** check 15 CFR 744 Supp. 4 on ecfr.gov and Federal Register 2026 BIS rules. Also whether the **affiliates rule** suspension ends ~2026-11-10.
5. **§5949 FAR implementing rule status** and exact scope ("use" prohibition; critical-systems language) (acquisition.gov FAR cases; federalregister.gov).
6. **§48D final regs:** does back-end test/packaging qualify? Exact begin-construction safe harbors; BASIC Act progress (IRS/Treasury; congress.gov).
7. **DMEA accredited-supplier list:** memory-relevant entries; is Micron accredited? Is Micross? (dmea.osd.mil).
8. **Microelectronics Commons** FY2025–27 project calls and any memory projects; NSTXL membership cost.
9. **CMMC Phase 2 start date** confirmation (DFARS final rule, Federal Register Sept 2025).
10. **ITAR XV(d), 9A515.d/.e and 3A001.a.1 exact thresholds** (ecfr.gov 22 CFR 121; 15 CFR 774).
11. **State programs:** MassVentures START amounts; NC One NC matching; VIPC CCF; NY FuzeHub; AZ Innovation Challenge 2026 cycles.
12. **DOE:** LEEP 2026 cohorts and funding; TCF 2026; Sandia HZO FeRAM licensing availability (Sandia IP portal; DOE Lab Partnering Service).
13. **DARPA OPTIMA** performers and follow-ons; any 2026 memory BAAs; NGMM/TIE user-access terms.

---

## 15. Sources used

All are cross-references to sibling agents' logged search snippets. I did not open them; see §0. Full entries are in `research/sources/p1-funding.jsonl`.

- CHIPS/Micron: NIST Micron final award 2024-12-10 (nist.gov/node/1855121); NIST Manassas PMT (nist.gov/node/1869301); Transport Topics/AP 2024-12-10; Business Facilities 2025-06; Micron FY2026 10-K (SEC); eeNews Europe 2026-01 (NY $5.5B); eeNews Europe 2026-05 (Manassas DDR4).
- §48D: Baker Tilly (2025); Instead (2026-03-31); Bloomberg (2025-07-01); SIA (2025-07); Congress.gov H.R. 3204.
- DoD/DARPA memory topics: DARPA "Non-Volatile Memory for Extreme Environments" (2026-07); BWCO Consulting DV017 (~$1.2M); SBIR.gov topic AF254-D0806 (2025); Sandia "Facing radiation challenges head on" (2026-05-13); Weebit/SkyWater S130 qualification (2023-06).
- §5949 / CXMT: XenoSpectrum (2026-07); Schumer press release (2026-07-30) and letter (2025-05-15); The Next Web (2026-06-27); Gigazine (2026-08-10); Hardware Busters (2026); TrendForce (2025-05-16); Notebookcheck (2025).
- Export/tariff context: Simpson Thacher on BIS 50% rule (2025-10-17); Covington Global Policy Watch (2026-02); CRS LSB11409 (2026); Korea Times (2026-09-15); TrendForce (2026-01-19, Lutnick 100% threat); UHY (2026-07).
