# Lab targets: where to get the Oxide Tail Spec run

*Outreach file for the [dram-moonshot](../README.md) study. As of 2026-11-04. Written for you, a software builder on the US East Coast who is not a chip engineer.*

**What this file answers.** The study's biggest unknown is the worst-case behaviour of small oxide transistors: the 1e-4 to 2e-5 quantile of off-state leakage, and the 1e-4 quantile of random telegraph noise (RTN), after a ≤400 °C hydrogen, heat and bonding budget ([report §1](../DRAM_MOONSHOT_REPORT.md)). The Monday action is to send a one-page "Oxide Tail Spec" to a lab that can run it. This file says which nanofabs, which faculty groups and which DRAM test partners to send it to, and in what order.

**Evidence tags.**
- [DATASHEET]: a maker's or facility's published spec.
- [REPORTED]: a paper, official page or press item, with its URL in the Sources section. Almost all of these come from web-search snippets, not full pages.
- [ESTIMATE]: our own arithmetic or judgment.
- [UNVERIFIED]: not confirmed by a source found in this pass.

**Limits of this pass.**
- 50 web searches were run. Direct page fetches failed for nnci.net and www.nsf.gov, so no page was opened in full. Every rate, name and capability below rests on search snippets and should be confirmed by email before you budget.
- arXiv links appear only as citations seen in search results. arxiv.org was not opened.
- Rates change every fiscal year, and several pages showed conflicting dates.
- No personal email addresses or phone numbers are listed. Every contact goes through the official page linked here.
- **Re-check pass (2026-11-04, 15 more searches, snippets only).** Re-confirmed: Ye, Datta, Alam, Yu, Patel, Peterson, Hirschman and Qureshi (person, current institution, topic), plus the Purdue staff rates, the Georgia Tech IMS rates and the RIT rates. Corrections from it are marked "re-check". Every other facility row (Cornell, Penn, NIST, MIT.nano, Harvard, UMD, NC State, Columbia, Yale, Princeton, RPI, NY CREATES) still rests on the first pass's snippets only [REPORTED, not re-checked].

**Acronyms.**
- ALD: atomic layer deposition. PECVD: plasma-enhanced chemical vapour deposition. SIMS: secondary-ion mass spectrometry.
- IGZO: indium gallium zinc oxide. IGO: indium gallium oxide. ZTO: zinc tin oxide. In₂O₃: indium oxide. IWO: tungsten-doped indium oxide. AOS: amorphous oxide semiconductor.
- TFT / FET: thin-film / field-effect transistor. BEOL: back end of line, the wiring layers built after the silicon transistors, which must stay at ≤400 °C.
- 2T0C: a gain cell with two transistors and no capacitor.
- PBTI / BTI: (positive) bias-temperature instability, a slow threshold-voltage drift under voltage and heat.
- NNCI: National Nanotechnology Coordinated Infrastructure, the NSF network of open-access university nanofabs. NQNI: its successor program. NSF: National Science Foundation.
- IMS: Georgia Tech's Institute for Matter and Systems. IEN: Georgia Tech's Institute for Electronics and Nanotechnology.
- CNF: Cornell NanoScale Facility. CNS: Harvard Center for Nanoscale Systems. CNST: NIST Center for Nanoscale Science and Technology. NIST: National Institute of Standards and Technology.
- PO: purchase order. F&A: facilities and administrative overhead. NDA: non-disclosure agreement.
- DRAM: dynamic random-access memory. ECC: error-correcting code. RDIMM: registered memory module. FPGA: field-programmable gate array.

---

## 0. The answer in one screen

**Ranked shortlist** (details in [Part 4](#part-4--ranked-shortlist)):

| # | Facility | One line on why |
|---|---|---|
| 1 | **Purdue Birck Nanotechnology Center** (West Lafayette, IN) | Purdue is the only US university found that has reported three stacked ALD In₂O₃ transistor tiers on 200 mm wafers (2026). Birck staff offer processing services, and the Ye and Alam groups are on the same campus [REPORTED]. That the stack was built at Birck is likely but [UNVERIFIED] |
| 2 | **Georgia Tech cleanroom (IMS, older pages say IEN)** (Atlanta, GA) | Home of the Datta, Yu and Khan oxide-memory groups. It has the cheapest published industry rates found: $39/h, $850/month entry, $100/h staff [REPORTED] |
| 3 | **RIT Semiconductor Nanofabrication Lab** (Rochester, NY) | The East Coast option. It offers a staff-run service level at $95/h (FY24), and it has IGZO TFT papers from 2014 (with Corning) to 2024 [REPORTED] |

| # | Group | One line on why |
|---|---|---|
| 1 | **Peide Ye**, Purdue ECE | ALD In₂O₃ FETs built for DRAM, which survive 600 °C (EDL 2024) [REPORTED]. Purdue's 2026-09-16 news item names him as lead of the 3-tier 200 mm platform [REPORTED, re-check] |
| 2 | **Suman Datta**, Georgia Tech ECE | Senior author of the first IWO (tungsten-doped In₂O₃) 2T gain-cell eDRAM, with leakage and retention measured at 25 and 85 °C (IEDM 2020). Now works on oxide BEOL memory at Georgia Tech [REPORTED] |
| 3 | **Muhammad Ashraful Alam**, Purdue ECE | A reliability physicist who has measured PBTI and hot-carrier drift in ALD In₂O₃ TFTs (EDL 2022). The tail question is a reliability question [REPORTED] |
| 4 | **Shimeng Yu**, Georgia Tech ECE | Oxide 2T gain-cell arrays and benchmarking (IEEE Trans. Computers 2026); knows what a ≥1e5-cell test array needs [REPORTED] |
| 5 | **Minesh Patel**, Rutgers CS (New Jersey) | The FASTEST PROOF track: DRAM error profiling and on-die ECC (BEER, HARP), with 2026 real-chip work on 212 DDR4 chips [REPORTED] |

**How to use it.**
- Send the one-page spec to groups 1-4 in the same week.
- Ask for a sponsored-research quote, and ask whether they already hold per-device leakage or RTN data on ≥1e4 devices that they would share under NDA ([report §9](../DRAM_MOONSHOT_REPORT.md), Day 1).
- Send the RAW-BER plan to group 5 at the same time.
- File the provisionals first. The spec lists test structures and pass lines only ([report §9](../DRAM_MOONSHOT_REPORT.md), "One rule").

**The key finding for a non-engineer.** A nanofab rents tools. It does not run your experiment. MIT.nano says outright that its staff generally do not do project processing [REPORTED]. Two routes work for you:
- **Route A (recommended).** A sponsored-research agreement with a faculty group. The group's students fabricate and measure in their home cleanroom [ESTIMATE].
- **Route B.** Fee-for-service staff processing (Purdue, Georgia Tech, RIT, Penn, NIST CNST). It needs a written process "traveler", meaning step-by-step recipes. Only a device engineer can write one, so Route B waits for your device co-founder hire [ESTIMATE].

**A gap no lab fills yet.** No US group was found that publishes RTN tail statistics on IGZO or other oxide transistors (search, 2026-11) [REPORTED as a negative result]. The closest published hydrogen and PBTI study on In-ratio splits that this pass found is from imec in Belgium [REPORTED]. So your spec asks for a dataset this search did not find in print. A group can win a first paper from it, so use that as leverage [ESTIMATE].

---

## 1. What the job needs (from the dossiers)

The facility must support every row below. The rows are copied from [hot-side-memory §5](../dossiers/hot-side-memory.md), [pixel-stack §5](../dossiers/pixel-stack.md) and the [REDTEAM](../REDTEAM.md) responses.

| Need | Spec value | Source |
|---|---|---|
| Oxide channels | IGZO, In-poor IGZO, IGO, Ga-free ZTO or In₂O₃; 8-10 nm ALD | hot-side §5, pixel-stack §5 |
| Dielectrics and encapsulation | ALD HfO₂/Al₂O₃; PECVD SiN; H-lean vs PECVD encapsulation, with and without ALD Al₂O₃ | hot-side §5 |
| Patterning | Read-gate area ≥0.01 µm², which needs e-beam or a stepper; vertical channel-all-around arrays | hot-side §5 |
| Heat and hydrogen dose | 350 °C/2 h, then 400 °C/30 min forming gas, then PECVD SiN, then a 400 °C anneal; 1x/2x/4x cumulative dose splits | hot-side §5, REDTEAM |
| Bond split | D₂O-hydrated, plasma-activated cap chips fusion-bonded at 350-400 °C; SIMS H/D at a DOE nanoscience center | hot-side §5 |
| Count | ≥25 arrays × 4 kb = ≥1e5 cells per split | hot-side §5 |
| Measurement | Drift, retention and RTN at 85/105/125 °C on a hot-chuck prober | hot-side §5, and-stack |
| Budget line | Coupon run $130k (6 splits, 2 lots); the physicist judge's lot budget was $220k | hot-side §5 [ESTIMATE], decision.json (physicist budget) |

**One sample-size check.** To see a p-quantile you need N ≳ 3/p devices ([FIRST_PRINCIPLES §4](../home-lab/FIRST_PRINCIPLES.md)).
- The 1e-4 quantile needs ≥30,000 cells.
- The 2e-5 quantile needs ≥150,000 cells.

So the dossier's 1e5 cells per split covers the 1e-4 lines but is short for the 2e-5 leakage line. Ask for ≥1.5e5 cells per split on the leakage structures [ESTIMATE].

---

## Part 1 — Nanofabrication facilities with external or industry access

### 1.1 Network, access mode and published rates

The NNCI column reflects what the search snippets support. The full 16-site list could not be opened because nnci.net was blocked. NNCI support ran 2015-2025. Its successor is NQNI (NSF 26-505): up to 16 sites, up to $100M, letters of intent due 2026-03-16 [REPORTED]. No NQNI awards were found as of 2026-11-04, so any facility's network status may change in 2026-27 [REPORTED].

| Facility | Where | Network | Staff-run or remote work? | Published external / industry rates | Official program page |
|---|---|---|---|---|---|
| **Purdue Birck Nanotechnology Center** | West Lafayette, IN | Not seen in any NNCI list [UNVERIFIED] | **Yes.** Most users run the tools themselves, but staff offer processing or measurement services [REPORTED] | Engineering staff time: $144/h for external non-profit and small business, $166/h for external for-profit (iLab, undated; the same two rates appear in a Birck rate memo effective 2023-06-01, marked pending approval) [REPORTED, re-check]. Other iLab rows, items not shown: $115/h and $132/h (first pass; E8 lists 2023 e-beam lithography at $115-132/h) and $166/h and $191/h (re-check) [UNVERIFIED]. External rates include 57% F&A [REPORTED] | [birck.research.purdue.edu/equipment/become-a-user](https://birck.research.purdue.edu/equipment/become-a-user/) |
| **Georgia Tech cleanroom (IMS; older pages say IEN)** | Atlanta, GA | NNCI site (SENIC, with JSNN at NC A&T/UNCG) [REPORTED] | **Yes**, staff time is billable. Academic and government users pay internal rates [REPORTED] | Industry and foreign academic, effective 2025-09-01: $850/month entry, $39/h cleanroom use, $100/h staff. Excludes indirect costs. Older 2023-26 lists show different lines [REPORTED] | [matter-systems.gatech.edu/cleanroom/getting-started/rates](https://matter-systems.gatech.edu/cleanroom/getting-started/rates) |
| **Cornell NanoScale Facility (CNF)** | Ithaca, NY | NNCI site [REPORTED] | **Probably.** CNF advertises "remote services"; a 2014 staff post describes staff hired per hour or lump sum [REPORTED, dated] | Rates are in its NEMO system. NSF requires that industry fees not undercut commercial services [REPORTED] | [cnf.cornell.edu/node/642](https://cnf.cornell.edu/node/642) |
| **Penn Singh Center for Nanotechnology** | Philadelphia, PA | NNCI site (MANTH, the Mid-Atlantic Nanotechnology Hub) [REPORTED] | **Yes**, staff time is billable. Industry users and startups are welcome ("Club Nano Edge") [REPORTED] | Effective 2025-07-01, industry: door $66-77/h, staff $150/h, tools $0-495/h [REPORTED] | [nano.upenn.edu/resources/fee-structure](https://www.nano.upenn.edu/resources/fee-structure) |
| **NIST CNST NanoFab** | Gaithersburg, MD | Federal user facility, not NNCI [UNVERIFIED] | **Yes.** "Remote jobs": you specify the work and NanoFab staff perform it, at an extra hourly rate [REPORTED] | Rates depend on the nature of the work, not who you are. Non-proprietary projects can get reduced rates [REPORTED] | [nist.gov/cnst](https://www.nist.gov/cnst) |
| **MIT.nano (Fab.nano)** | Cambridge, MA | Not NNCI [UNVERIFIED] | **Mostly no.** "In general, processing for a project will not be done by MIT.nano staff members" [REPORTED] | External rate sheet dated March 2026 exists (amounts not seen). No membership fee; consortium members pay less [REPORTED] | [nanousers.mit.edu/node/98](https://nanousers.mit.edu/node/98) |
| **Harvard CNS** | Cambridge, MA | NNCI site [REPORTED] | Not found [UNVERIFIED] | Fee PDFs exist on the user-info page (not read). About 15% of ~1,500 yearly users are corporate [REPORTED] | [cns1.rc.fas.harvard.edu/user-info](https://cns1.rc.fas.harvard.edu/user-info/) |
| **University of Maryland NanoCenter FabLab** | College Park, MD | Not NNCI [UNVERIFIED] | Not confirmed. Outside users are trained and approved case by case [REPORTED] | Process tools: $126/h external non-profit, $166/h small commercial, $242/h large commercial. Page dates conflict (2024 vs 2026) [REPORTED] | [nanocenter.umd.edu/fablab/fees](https://www.nanocenter.umd.edu/fablab/fees/) |
| **NC State Nanofabrication Facility (NNF)** | Raleigh, NC | NNCI site (RTNN, with Duke and UNC) [REPORTED] | Not found [UNVERIFIED] | Not found; a fee page exists [REPORTED] | [nnf.ncsu.edu/fees](https://nnf.ncsu.edu/fees/) |
| **RIT Semiconductor Nanofabrication Lab (formerly SMFL)** | Rochester, NY | Not NNCI [UNVERIFIED] | **Yes.** Two service levels for external customers: staff-run work or your own work [REPORTED] | FY24: $95/h dedicated staff, $100/month per-user equipment fee, one-time training charge. External academic: Tier 1 $37/h, Tier 2 $58/h [REPORTED] | [rit.edu/nanofab/external-customers](https://www.rit.edu/nanofab/external-customers) |
| **Columbia Nano Initiative (CNI) cleanroom** | New York, NY | Not NNCI [UNVERIFIED] | Not found [UNVERIFIED] | Separate industry schedule; industry pays about 3x internal (2019). External academic: internal + 20%. Payment by check [REPORTED] | [cni.columbia.edu/external-user-program-1](https://cni.columbia.edu/external-user-program-1) |
| **Yale cleanrooms (SEAS and West Campus)** | New Haven, CT | Not NNCI [UNVERIFIED] | Not found [UNVERIFIED] | "External users, please contact us directly for the rates" [REPORTED] | [cleanroom.yale.edu/node/100](https://cleanroom.yale.edu/node/100) |
| **Princeton PRISM Micro/Nano Fabrication Center** | Princeton, NJ | Not NNCI [UNVERIFIED] | Not found [UNVERIFIED] | Open to external users, billed hourly; only internal prices are published [REPORTED] | [materials.princeton.edu/core-facilities](https://materials.princeton.edu/core-facilities) |
| **RPI Micro and Nano Fabrication Clean Room (CMDIS)** | Troy, NY | Not NNCI [UNVERIFIED] | "Assisted" service level in the rate table [REPORTED] | Dec 2023 table: standard, training and assisted rates; a "proprietary" tier for non-publishable work. Amounts unreadable in the snippet [REPORTED] | [cmdis.rpi.edu fee structure (PDF)](https://cmdis.rpi.edu/sites/default/files/CMDIS-Feestructure-2024_0.pdf) |
| **NY CREATES, Albany NanoTech** | Albany, NY | NSTC EUV Accelerator site; leads the NORDTECH Microelectronics Commons hub [REPORTED] | 300 mm R&D access for startups and universities; terms not found [REPORTED] | Not found [UNVERIFIED] | [ny-creates.org](https://ny-creates.org) |
| **Stony Brook University** | Stony Brook, NY | Not found | Not found | Not found. The search returned nothing on a Stony Brook nanofab [UNVERIFIED] | Not found |

**Staff hours compared.** The cost of 100 staff hours at each published rate [ESTIMATE]. This excludes tool fees, materials and overhead.

| Facility (rate basis) | 100 staff hours |
|---|---|
| RIT, dedicated staff, FY24 | $9,500 |
| Georgia Tech, industry, 2025-09-01 | $10,000 |
| Purdue, external non-profit / Indiana small business (undated) | $14,400 |
| Penn, industry, 2025-07-01 | $15,000 |
| Purdue, external for-profit (undated) | $16,600 |

At Georgia Tech, one month of 100 cleanroom hours, 100 staff hours and the entry fee comes to $14,750 [ESTIMATE].

### 1.2 Capability fit for the Oxide Tail Spec

"Ask" means no source was found in this pass, so the item goes on the question list (§1.4).

| Facility | Oxide channel (ALD or sputter IGZO/In₂O₃/IGO/ZTO) | ALD dielectrics | Fine litho (e-beam or stepper) | ≤400 °C forming-gas / D₂O anneals | Hot-chuck probing to 125 °C | Wafer bonding |
|---|---|---|---|---|---|---|
| Purdue Birck | **Likely.** Purdue reported ALD In₂O₃ in 3 tiers on 200 mm, >100,000 devices over 52 dies (2026), and 600 °C survival (2024) [REPORTED]; the fab site is not stated in the snippets [UNVERIFIED] | Ask | Ask (the study planned 250 nm e-beam holes at Birck [UNVERIFIED]) | Ask | Ask | Ask |
| Georgia Tech | Groups publish on IWO and IGZO, but GT-made devices not confirmed [UNVERIFIED] | Ask | Ask | Ask | Ask | Ask |
| RIT | **Yes.** IGZO TFTs incl. boron-implanted self-aligned bottom gate (2024); 400 °C air anneals with Al₂O₃ passivation (2014) [REPORTED] | Ask | Ask; CMOS foundry service existed (older wiki) [REPORTED] | Ask | Ask | Ask |
| MIT.nano | Oxide-channel (ITO) FeFETs from the del Alamo group [REPORTED] | Ask | Ask | Ask | Ask | Listed as a bonder site in the dossier [UNVERIFIED] |
| Cornell CNF | Ask | Ask | Ask | Ask | Ask | Listed as a bonder site in the dossier [UNVERIFIED] |
| UMD FabLab | Ask | ALD, furnace and sputter billed at variable rates [REPORTED] | Ask | Ask | Ask | Ask |
| NIST CNST | Ask | Ask | Ask | Ask | Ask | Ask |
| Penn, Harvard, NC State, Columbia, Yale, Princeton, RPI | Ask | Ask | Ask | Ask | Ask | Ask |
| NY CREATES | 300 mm line; oxide not confirmed | Ask | 300 mm litho, incl. EUV [REPORTED] | Ask | Ask | Bond metrology is a later-stage use in the dossier [UNVERIFIED] |

### 1.3 Onboarding steps found

| Facility | Steps found | Source |
|---|---|---|
| Purdue Birck | External-user onboarding checklist: make contact, complete two forms, set up accounts, training [REPORTED] | become-a-user page |
| Georgia Tech | Contact an IMS staff member; join a billing group and an equipment group in SUMS (the booking system); orientation and entrance tests [REPORTED] | become-user page |
| Cornell CNF | Follow the new-project steps; external accounts need a PO sent to CNF Accounting. In 2014, privately hired remote staff needed their own insurance [REPORTED] | node/30, node/642, 2014 post |
| Penn Singh | Staff approval before requesting access [REPORTED] | nano.upenn.edu |
| MIT.nano | One external-user agreement per institution, plus a valid PO; every person completes EHS (environment, health and safety) training and is qualified on each tool [REPORTED] | node/27, node/98, External User Agreement (2024) |
| Harvard CNS | Enroll in the CNS User Program with active status [REPORTED] | user-info page |
| UMD FabLab | PO or valid credit card; training; case-by-case approval [REPORTED] | fablab page |
| RIT | Sign a visitor agreement; complete safety training and certification; external academic users submit a proposal for work [REPORTED] | external-customers page |
| NIST CNST | Training and a cleanroom safety exam before access; remote jobs skip hands-on use [REPORTED] | nist.gov/cnst |
| Columbia CNI | External user program; monthly invoice; payment by check within 30 days [REPORTED] | external-user-program page |
| Yale | Approval by the SEAS Business Office [REPORTED] | cleanroom.yale.edu |
| Others | Not found [UNVERIFIED] | - |

**What every site will need from you** [ESTIMATE]: a legal entity, which means incorporating first (weeks 9-10 in [report §9](../DRAM_MOONSHOT_REPORT.md)); a PO or payment method; certificates of general-liability insurance if your own people enter the cleanroom; and an NDA or sponsored-research agreement that settles IP before you share anything beyond the spec.

### 1.4 Ask list (paste into the first email)

1. Can your staff, or a group in your building, run a staff-processed oxide TFT lot from our traveler? At what staff rate and turnaround?
2. Which oxide channels can you deposit today (ALD or sputter): IGZO at two In ratios, IGO, ZTO, In₂O₃?
3. Can you run 350-400 °C anneals in forming gas, and do you allow D₂O-hydrated bonding or anneals?
4. What is your smallest reliable feature and overlay (e-beam or stepper), for a read-gate area of 0.01-0.02 µm²?
5. Do you have a semi-automatic prober with a hot chuck to 125 °C, and can it measure ≥1.5e5 cells per split?
6. What are your current external for-profit rates (FY26), and do startups or small businesses get a discount?
7. What are your IP terms for staff-processed work and for sponsored research?
8. Do you hold per-device leakage or RTN data on ≥1e4 oxide devices that could be shared under NDA?

### 1.5 Ranking of facilities for this job

The criteria, in order [ESTIMATE]:
1. An oxide-transistor group already works on the same campus.
2. A staff-run route exists.
3. Rates are published.
4. It is on the East Coast or in Eastern Time.

| Rank | Facility | Why | Main gap |
|---|---|---|---|
| 1 | Purdue Birck | Reported ALD In₂O₃ multi-tier know-how at Purdue; staff services; the Ye and Alam groups | Not on the East Coast (Indiana, Eastern Time [UNVERIFIED]); staff rate is the highest of those found |
| 2 | Georgia Tech (IMS/IEN) | Three oxide-memory groups; lowest industry rates found; NNCI site | Whether GT fabricates oxide devices on site is not confirmed |
| 3 | RIT | East Coast; staff-run tier; cheapest staff rate; IGZO process lineage | No scaled (≤0.02 µm²) oxide devices or e-beam confirmed; no hydrogen-reliability record found |
| 4 | Cornell CNF | East Coast NNCI site with a broad tool set; remote services | No in-house oxide-memory group found; remote-staff details date from 2014 |
| 5 | NIST CNST NanoFab | Explicit staff "remote jobs"; Maryland | No oxide-transistor group found; rates not published |
| 6 | Penn Singh | Published 2025 industry rates; startup program | No oxide-memory group found |
| 7 | MIT.nano | Strong tools; oxide-channel FeFET work (del Alamo); bonding later | Staff generally do not process, so you need your own engineer on site |
| 8 | UMD FabLab | Published rates; ALD on site | No group or staff-run route found |
| 9-14 | NC State NNF, Harvard CNS, Columbia, Yale, Princeton, RPI | Open to external users | Rates or staff routes not found; no oxide-memory group found |
| Later | NY CREATES | 300 mm for a fab-grade split or bond metrology after Gate A+ | Not for first coupons; terms not found |
| - | Stony Brook | - | Nothing found |

---

## Part 2 — Research groups on oxide-semiconductor transistors for memory

**Verification rule.** Name, current institution and topic must each be backed by a source. A ✔ means a source was found. [UNVERIFIED] marks what was not.

### 2.1 Groups that fit (verified)

| Faculty | Institution | Matching publication (title, year) | Why they fit the spec | Official page | Name / institution / topic |
|---|---|---|---|---|---|
| **Peide Ye** | Purdue University, ECE | Lin et al., top-gate enhancement-mode ALD In₂O₃ FETs with a 600 °C thermal budget "for DRAM applications", IEEE EDL 2024; Si et al., ultimately scaled ALD In₂O₃ transistors (8 nm channel), Nature Electronics 2022 [REPORTED]. Purdue's 2026-09-16 news item on the 3-tier In₂O₃ platform on 200 mm names him as lead [REPORTED, re-check] | The In₂O₃ channel split and the hydrogen-tolerant 600 °C option; Purdue has reported >1e5 devices on 200 mm [REPORTED] | [engineering.purdue.edu/~yep](https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf) (group papers); [Purdue ECE 2026 news](https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing) | ✔ / ✔ (2024 papers on Purdue's site) / ✔ |
| **Suman Datta** | Georgia Tech, ECE | H. Ye, …, K. Ni, A. Raychowdhury, S. Datta, "Double-gate W-doped amorphous indium oxide transistors for monolithic 3D capacitorless gain cell eDRAM", IEDM 2020 (done at Notre Dame); Phadke, Datta, Yu et al., capacitive coupling in oxide-channel 2T gain cells, IEEE TED 2024 [REPORTED] | First IWO 2T gain cell (per the Notre Dame thesis), with leakage and retention measured at 25 and 85 °C; his GT page lists AOS for BEOL memory | [ece.gatech.edu/faculty-staff-directory/suman-datta](https://www.ece.gatech.edu/faculty-staff-directory/suman-datta) | ✔ / ✔ / ✔ |
| **Shimeng Yu** | Georgia Tech, ECE | Waqar, Kwak, Lee, Phadke, Shon, Gholamrezaei, Skadron, Yu, "Optimization and Benchmarking of Monolithically Stackable Gain Cell Memory for Last-Level Cache", IEEE Trans. Computers 75(3), March 2026 (AOS 2T gain cells) [REPORTED] | Array and circuit side: what a ≥1e5-cell structure and its readout need; system benchmarks against SRAM and eDRAM | [shimeng.ece.gatech.edu](https://shimeng.ece.gatech.edu/?p=916) | ✔ / ✔ / ✔ |
| **Asif Islam Khan** | Georgia Tech, ECE (courtesy MSE) | T. Song, A. I. Khan, "3D DRAM with stacked oxide-semiconductor channel transistors", Nature Electronics 2025 (listed on his directory page) [REPORTED] | Ferroelectric and oxide BEOL devices; 3D oxide DRAM view relevant to AND-STACK | [ece.gatech.edu/faculty-staff-directory/asif-islam-khan](https://www.ece.gatech.edu/faculty-staff-directory/asif-islam-khan) | ✔ / ✔ / ✔ (main focus is ferroelectrics) |
| **Muhammad Ashraful Alam** | Purdue University, ECE | IEEE EDL 2022 on PBTI and hot-carrier degradation in ultrathin ALD In₂O₃ TFTs, flagging BEOL self-heating; Y.-P. Chen PhD thesis, "Reliability Characterizations of Power Transistors: From Silicon to Oxide Semiconductors" [REPORTED] | The tail question is a reliability and statistics question; PBTI and self-heating at 105-125 °C | [Purdue CRISP profile](https://engineering.purdue.edu/CRISP/people/affiliate-faculty-expertise/ashraf-alam) | ✔ / ✔ / ✔ |
| **Becky Peterson** (listed as Becky Lorenz Peterson; also R. L. Peterson) | University of Michigan, ECE (an MSE page also lists her). A faculty page lists her as director of the Lurie Nanofabrication Facility [REPORTED, re-check; page undated] | First ZTO-TFT 2T0C memory, retention >1,500 s (T. Newsom PhD thesis, Peterson on committee); Allemang, Cho, Dasgupta, Peterson on In-free ZTO [REPORTED] | The Ga-free and In-free ZTO split the spec requires | [mse.engin.umich.edu/people/blpeters](https://mse.engin.umich.edu/people/blpeters) | ✔ / ✔ / ✔ (Midwest) |
| **Jesús A. del Alamo** | MIT, EECS | BEOL ferroelectric FETs with HZO gates on AOS transistors; 2024 conference paper on scaled oxide-channel (ITO) FeFETs [REPORTED] | East Coast group that builds oxide-channel BEOL devices; where they are fabricated [UNVERIFIED] | [MIT project page](https://mtlsites.mit.edu/users/alamo/Projects/Project14.htm) | ✔ / ✔ / ✔ (FeFET focus; page date unclear) |
| **Karl D. Hirschman** | RIT, Electrical & Microelectronic Engineering | Mudgal, Walsh, Manley, Hirschman (RIT/Corning), "Passivation and Annealing for Improved Stability of High Performance IGZO TFTs", MRS 2014; Powell et al., "Dose-Dependent Performance of Boron-Implanted Self-Aligned Bottom-Gate IGZO TFTs", ECS Trans. 114 (2024) [REPORTED] | IGZO TFT anneal and passivation stability; faculty director of the RIT fab | [RIT directory](https://www.rit.edu/engineering/directory/kdhemc-karl-hirschman); [RIT news (undated)](https://www.rit.edu/news/299k-grant-rit-supports-flat-panel-display-development) | ✔ / ✔ (RIT directory: faculty director of the Semiconductor Nanofabrication Laboratory since 2001; silicon and metal-oxide thin-film electronics) [REPORTED, re-check] / ✔ |

### 2.2 Partial fits and leads (verification incomplete)

| Person or group | What was found | What is missing |
|---|---|---|
| **Kai Ni**, University of Notre Dame, EE | Co-author on the IEDM 2020 IWO 2T gain cell; listed at Notre Dame on a 2025 arXiv paper and as PI of a Notre Dame student project [REPORTED] | Official faculty page not found; his own oxide-channel memory papers not confirmed [UNVERIFIED] |
| **Jason P. Campbell**, NIST (Gaithersburg, MD) | RTN in highly scaled nMOSFETs (2009) and fast-BTI methods (2008) [REPORTED] | Silicon, not oxide; current role at NIST [UNVERIFIED]. A method partner for fast RTN capture, not a fab |
| **Thomas N. Jackson**, Penn State | PEALD ZnO TFTs and circuits at 200 °C, 2008-2016 [REPORTED] | Current activity [UNVERIFIED] |
| **Ioannis Kymissis**, Columbia | Thin-film and metal-oxide hybrid electronics [REPORTED] | No IGZO or memory paper found; weak fit |
| **Arijit Raychowdhury**, Georgia Tech | Array-level evaluation of the IEDM 2020 gain cell [REPORTED, 2020] | Current role [UNVERIFIED] |

### 2.3 Non-US benchmarks to cite in the spec (not vendors)

- **imec (Leuven, Belgium), G. S. Kar's team.** A. Kruv et al., "In-poor IGZO: superior resilience to hydrogen in forming gas anneal and PBTI", 2025, ACS (arXiv 2412.07362). In-poor (≤17% In) IGZO was stable through a 420 °C/2 h forming-gas anneal (ΔVth 0.06-0.33 V), with no hydrogen-driven shift under PBTI at 125 °C [REPORTED]. A related imec IEDM 2025 paper finds that standard and In-poor IGZO fail opposite reliability tests [REPORTED]. This is the closest published match to your In-ratio and hydrogen-dose splits. Quote it so a US group sees the gap it can fill.
- **TU Wien.** RTN and charge-trapping models for IGZO TFTs (SISPAD 2022-2025, logged in the dossiers) [REPORTED]. A modelling partner for heavy RTN tails.

---

## Part 3 — DRAM characterization partners (RAW-BER contract)

The FASTEST PROOF needs DRAM Bender-style FPGA rigs for DDR4, plus open DDR5 RDIMM testers ([raw-ber-contract §5](../dossiers/raw-ber-contract.md)). The dossier already names CMU/SAFARI, Rutgers (Patel) and Georgia Tech (Qureshi) as subaward candidates.

| Partner | Where | Matching work (title, year) | Why they fit | Official page | Name / institution / topic |
|---|---|---|---|---|---|
| **Minesh Patel** | Rutgers University, Computer Science (NJ) | BEER (infers on-die ECC from post-correction errors) and HARP (error profiling with on-die ECC); 2026 arXiv on read-disturb thresholds in 212 real DDR4 chips (DiscoRD), with Rutgers and ETH co-authors; joined Rutgers 2024 [REPORTED] | Exactly the RAW-BER skill set: post-ECC error statistics and profiling on real chips; East Coast | [researchwithrutgers.com/en/persons/minesh-patel](https://www.researchwithrutgers.com/en/persons/minesh-patel/) | ✔ / ✔ / ✔ |
| **SAFARI Research Group** (Onur Mutlu) | ETH Zürich, Switzerland (CMU lineage) | DRAM Bender (FPGA DDR4 tester, IEEE TCAD); SoftMC (HPCA 2017); "A Modern Large-Scale Memory Characterization Laboratory", arXiv 2606.13725 (2026); DRAM Bender workshop at ASPLOS 2026 [REPORTED] | Owns the tools and the method; best for training and rig setup | [DRAM Bender record](https://www.research-collection.ethz.ch/handle/20.500.11850/642507) | ✔ / ✔ / ✔ (not US) |
| **Moinuddin Qureshi** | Georgia Tech, School of Computer Science | ArchShield (ISCA 2013): tolerates DRAM error rates up to 1e-4 at 4% capacity cost; Rowhammer mitigations MINT (MICRO 2024), AutoRFM (HPCA 2025), MOAT (ASPLOS 2025), DREAM (ISCA 2025) [REPORTED] | The architectural ancestor of "let ECC carry weak bits"; same campus as the oxide groups | [cc.gatech.edu/cv/mqureshi4](https://www.cc.gatech.edu/cv/mqureshi4) | ✔ / ✔ / ✔; whether his lab runs real-chip FPGA rigs [UNVERIFIED] |
| **Xun (Steve) Jian** | Virginia Tech, Computer Science | Adaptive Reliability Chipkill Correct (HPCA 2013); double-chipkill reliability models (2013); patents on iterative decoding for DRAM device failures; ISCA 2021 on server memory frequency margin [REPORTED] | The chipkill side of the contract: code choice and multi-chip-event math | [Virginia Tech news (2018)](https://news.vt.edu/articles/2018/02/SteveJian-cs-eng.html) | ✔ / ✔ (DBLP lists VT through 2021) / ✔ |
| **Saugata Ghose** | University of Illinois Urbana-Champaign, Siebel School of Computing | SoftMC co-author (CMU era); processing-in-memory primer (2020, UIUC) [REPORTED] | Knows the FPGA test method from the inside | Official page not found | ✔ / ✔ / ✔; rank [UNVERIFIED] |
| **Antmicro + Google open DDR5 testers** | Antmicro (company); Google funded | Open-hardware Data Center RDIMM DDR5 Tester, Rev 2.0 (Dec 2024) on an AMD Artix UltraScale+ FPGA; SO-DIMM and LPDDR5 boards; used for ETH's "Phoenix" DDR5 TRR study (IEEE S&P 2026) [REPORTED] | The DDR5 leg of Phase 1; Apache-2.0 designs you can build or buy | [antmicro.com blog](https://antmicro.com/blog/2024/12/data-center-rdimm-ddr5-tester-2-0/), [github.com/antmicro/ddr5-tester](https://github.com/antmicro/ddr5-tester) | ✔ / company HQ [UNVERIFIED] / ✔ |
| **FuturePlus Systems** | Merrimack, NH | DDR5 RDIMM/LRDIMM bus-analyzer probes (e.g., FS2600A) [REPORTED] | An instrument for checking command timing, not a retention tester | [futureplus.com](https://www.futureplus.com/get-quote) | ✔ / ✔ / partial fit |
| **Introspect Technology** | Location [UNVERIFIED] | M5513 DDR5 MRDIMM test system (third-party listing) [REPORTED] | A commercial DDR5 module tester to price against the open boards | No official page seen | partial |

**Negative result.** No US commercial lab was found that sells DDR5 retention characterization as a contract service [REPORTED as a negative result]. So the DRAM leg should be a subaward to a university lab plus your own open-hardware rigs, as the dossier plans [ESTIMATE].

---

## Part 4 — Ranked shortlist

**First 3 facilities to contact.**
1. **Purdue Birck.** Purdue is the only US university found with reported multi-tier ALD In₂O₃ device production; Birck has staff processing services; the Ye and Alam groups are on campus [REPORTED]. Use it for the main lot.
2. **Georgia Tech cleanroom (IMS, formerly listed as IEN).** The second source the study already named. It has three oxide-memory groups and the lowest published industry rates ($39/h, $850/month, $100/h staff) [REPORTED].
3. **RIT Semiconductor Nanofabrication Lab.** The East Coast option: a staff-run tier at $95/h (FY24), a long IGZO TFT record [REPORTED], and a day's drive from New York or Boston [UNVERIFIED]. Use it for a cheap planar IGZO screening lot or a hydrogen-dose split.
   - Alternate if RIT cannot pattern 0.01 µm²: **Cornell CNF** (NNCI, remote services) or **NIST CNST** (staff remote jobs) [REPORTED].

**First 5 groups to contact.**
1. **Peide Ye (Purdue):** In₂O₃ FETs for DRAM that survive 600 °C, at a university that has reported >1e5-device 200 mm runs [REPORTED].
2. **Suman Datta (Georgia Tech):** led the first IWO 2T gain cell and measured its 85 °C leakage and retention [REPORTED].
3. **Muhammad Ashraful Alam (Purdue):** PBTI and self-heating on In₂O₃, the reliability lens the tails need [REPORTED].
4. **Shimeng Yu (Georgia Tech):** gain-cell arrays and readout, so the ≥1e5-cell structures get designed right [REPORTED].
5. **Minesh Patel (Rutgers):** runs the FASTEST PROOF in parallel; post-ECC error profiling on real DRAM chips, in New Jersey [REPORTED].
   - Next in line: Becky Peterson (Michigan, ZTO split), Karl Hirschman (RIT, IGZO process), Moinuddin Qureshi (Georgia Tech, ECC architecture), Xun Jian (Virginia Tech, chipkill) [REPORTED].

**Order of operations** [ESTIMATE]:
1. Incorporate.
2. File the two provisionals.
3. Send the spec (test structures and pass lines only) to Ye, Datta, Alam and Yu, and the RAW-BER plan to Patel, in one week.
4. Open the Purdue and Georgia Tech external-user files the same day.
5. Hold RIT and Cornell as East Coast second sources until your device co-founder can write a traveler.

---

## Unverified items (consolidated)

- NNCI status of Purdue, MIT, UMD, Columbia, Yale, Princeton, RPI, RIT, NIST CNST and NY CREATES. They were absent from the snippets, and the full list on nnci.net could not be opened.
- NQNI award results and how they change any site's status.
- Purdue iLab rates: the staff rates match a 2023 memo marked pending approval; the items behind the $115/$132 and $166/$191 rows are unknown.
- Georgia Tech: how IMS and IEN relate. The search did not confirm a merger.
- Georgia Tech: whether oxide devices are fabricated on site.
- Cornell CNF: the current remote-processing policy (the source is from 2014) and current rates (in NEMO).
- Rates not found: Harvard CNS, NC State NNF, MIT.nano (amounts), Yale, Princeton, RPI (amounts unreadable), NIST CNST, NY CREATES.
- Stony Brook: no nanofab found.
- Purdue's 3-tier In₂O₃ platform (2026): that it was built at Birck. (Ye's lead role is confirmed by Purdue's news item; re-check.)
- Every tool-capability cell marked "Ask" in §1.2: ALD, e-beam or stepper, forming-gas and D₂O anneals, 125 °C hot-chuck probers and bonders.
- Karl Hirschman: the 2024 papers' affiliations were not shown. (His current RIT role is now sourced to the RIT directory; re-check.)
- Kai Ni: official Notre Dame page; his own oxide-memory papers.
- Jason P. Campbell: current NIST role.
- Thomas N. Jackson: current activity.
- Arijit Raychowdhury: current role.
- Saugata Ghose: academic rank and official page.
- Becky Peterson: whether the Lurie Nanofabrication Facility director role is current (the page is undated).
- Minesh Patel: the year he joined Rutgers (2024) was not re-checked.
- Moinuddin Qureshi: whether his lab runs real-chip FPGA test rigs.
- Antmicro: headquarters location.
- Introspect Technology: location.
- Time zones and drive times (Purdue in Eastern Time; RIT a day's drive from New York or Boston): prior knowledge, not sourced.
- The study's earlier names, which were not re-verified here: Mattan Erez (UT Austin), Nam Sung Kim (UIUC), Lara Dolecek (UCLA), Kaveh Razavi (ETH) ([raw-ber-contract §6](../dossiers/raw-ber-contract.md)).

**Blocked hosts in this pass:** nnci.net and www.nsf.gov (page fetch failed: the host does not resolve in this session). In the re-check, matter-systems.gatech.edu, www.rit.edu and birck.research.purdue.edu failed the same way, so the re-check also used search snippets only. After those two failures, no other page was fetched. arxiv.org was not opened; arXiv items are cited from search results only.

---

## Sources

*All accessed 2026-11-04 through web-search results unless marked "study log", meaning logged earlier in `research/sources/`.*

**Networks and programs**
- NQNI solicitation NSF 26-505: https://www.nsf.gov/funding/opportunities/nqni-national-quantum-nanotechnology-infrastructure/nsf26-505/solicitation
- NSF NQNI announcement (quantum.gov): https://www.quantum.gov/nsf-launches-100m-national-quantum-nanotechnology-research/
- NSF NNCI renewal: https://www.nsf.gov/news/nsf-renews-investment-national-nanotechnology
- NNCI coordinating office (Georgia Tech): https://www.tlwarc.hg.gatech.edu/node/449831
- SENIC renewal with JSNN: https://ncat.edu/news/2020/09/jsnn-georgia-tech-senic-grant-renewal.php
- Harvard CNS as NNCI site: https://www.nnci.net/sites/cns
- Penn MANTH (NNCI): https://nnci.net/sites/default/files/inline-files/MANTH%20NNCI%201-19-17.pdf
- RTNN in NNCI: https://rtnn.ncsu.edu/news/page/34/
- CNF and NNCI: https://www.cnf.cornell.edu/node/327

**Facilities**
- Purdue Birck access: https://birck.research.purdue.edu/equipment/become-a-user/
- Purdue Birck partner page: https://birck.research.purdue.edu/partner-with-us
- Purdue Birck iLab rates: https://purdue.ilab.agilent.com/service_center/show_external/4127/1000
- Purdue Birck FY24 rate listing: https://mailman.ecn.purdue.edu/archives/list/bnc-all@ecn.purdue.edu/message/QV6GR6XQBKTW7PU5OCDG7VQOPHRKJ2JN/attachment/5/BRKFY24RateListing.pdf
- Purdue Birck fabrication brochure (2025): https://birck.research.purdue.edu/app/uploads/2025/04/25-Fabrication-Broch-web.pdf
- Purdue 3D In₂O₃ platform (study log, 2026-09-16): https://engineering.purdue.edu/ECE/News/2026/purdue-researchers-build-3d-chip-platform-for-faster-more-efficient-ai-computing
- Georgia Tech cleanroom rates (effective 2025-09-01): https://matter-systems.gatech.edu/cleanroom/getting-started/rates
- Georgia Tech become a user: https://matter-systems.research.gatech.edu/cleanroom/getting-started/become-user
- Georgia Tech use our facilities: https://matter-systems.gatech.edu/use-our-facilities
- SENIC rates: https://senic.gatech.edu/about/rates
- SENIC facilities: https://senic.gatech.edu/facilities
- Cornell CNF rates overview: https://cnf.cornell.edu/node/642
- Cornell CNF new project steps: https://wwx.cnf.cornell.edu/node/30
- Cornell CNF what we do: https://cnf.cornell.edu/node/199
- CNF remote-processing post (2014): https://mtl.mit.edu/pipermail/labnetwork/attachments/20140103/91bcabe2/attachment.html
- Penn Singh fee structure (study log, effective 2025-07-01): https://www.nano.upenn.edu/resources/fee-structure
- Penn Singh access: https://www.nano.upenn.edu/?p=11
- MIT.nano non-academic criteria: https://nanousers.mit.edu/node/98
- MIT.nano new external users: https://nanousers.mit.edu/node/27
- MIT.nano external rates (March 2026): https://nanousers.mit.edu/sites/default/files/documents/Fab.nano%20Equipment%20Rates%20External%20March%202026.pdf
- MIT.nano external user agreement (2024): https://nanousers.mit.edu/sites/default/files/documents/External%20User%20Agreement%20MIT%20Nano%202-29-2024.pdf
- Harvard CNS user info: https://cns1.rc.fas.harvard.edu/user-info/
- UMD FabLab fees: https://www.nanocenter.umd.edu/fablab/fees/
- UMD FabLab: https://www.nanocenter.umd.edu/fablab
- NC State NNF fees: https://nnf.ncsu.edu/fees/
- NC State NNF open to industry (lab page): https://sites.google.com/ncsu.edu/hip-lab/facilities
- NIST CNST: https://www.nist.gov/cnst
- NIST NanoFab remote jobs: https://www.nist.gov/node/419896
- RIT external customers: https://www.rit.edu/nanofab/external-customers
- RIT nanofab: https://www.rit.edu/nanofab/
- Columbia CNI external user program: https://cni.columbia.edu/external-user-program-1
- Columbia CNI industry article (2019): https://news.columbia.edu/node/1927
- Yale cleanroom policies and rates: https://cleanroom.yale.edu/node/100
- Yale cleanroom core: https://research.yale.edu/cores/cleanroom
- Princeton core facilities: https://materials.princeton.edu/core-facilities
- RPI CMDIS fee structure: https://cmdis.rpi.edu/sites/default/files/CMDIS-Feestructure-2024_0.pdf
- NY CREATES: https://ny-creates.org
- New York NSTC roadmap: https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york

**Oxide-transistor groups**
- Ye, EDL 2024 In₂O₃ 600 °C: https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3%20600C_Lin.pdf
- Ye, scaled In₂O₃ (Purdue ECE 2022): https://engineering.purdue.edu/ECE/News/2022/new-material-advances-lead-to-smaller-and-better-performing-transistors
- Ye, ALD In₂O₃ for BEOL logic and memory (talk, 2021): https://www.aihardware.mit.edu/atomic-layer-deposited-atomically-thin-in2o3-channel-for-beol-logic-and-memory-applications/
- Datta, Georgia Tech directory: https://www.ece.gatech.edu/faculty-staff-directory/suman-datta
- Datta, IWO gain cell (Notre Dame news): https://engineering.nd.edu/news/electrical-engineering-team-spotlighted-for-work-developing-a-new-kind-of-semiconductor-memory/
- IWO gain cell (NSF PAR copy): https://par.nsf.gov/servlets/purl/10423741
- H. Ye IWO thesis (Notre Dame): https://curate.nd.edu/articles/thesis/High-Performance_Back-End-of-Line_Compatible_Indium_Tungsten_Oxide_IWO_sub_sub_Transistors_for_Monolithic-3D_Application/24869733
- Yu, gain-cell LLC paper (TC 2026): https://faaiqgwaqar.github.io/assets/gain-cell-llc-paper.pdf
- Yu group page (study log): https://shimeng.ece.gatech.edu/?p=916
- Khan, Georgia Tech directory: https://www.ece.gatech.edu/faculty-staff-directory/asif-islam-khan
- Alam, Purdue CRISP profile: https://engineering.purdue.edu/CRISP/people/affiliate-faculty-expertise/ashraf-alam
- Alam group thesis (Y.-P. Chen): https://hammer.purdue.edu/articles/thesis/Reliability_Characterizations_of_Power_Transistors_From_Silicon_to_Oxide_Semiconductors/17155664
- Peterson, Michigan MSE: https://mse.engin.umich.edu/people/blpeters
- ZTO 2T0C thesis (Newsom): https://deepblue.lib.umich.edu/items/e6ac2d99-46aa-444a-bc41-2851e63c965c
- del Alamo, AOS FeFET project: https://mtlsites.mit.edu/users/alamo/Projects/Project14.htm
- del Alamo group: https://alamo.mit.edu/?p=840
- Hirschman, MRS 2014 IGZO paper: https://www.cambridge.org/core/journals/mrs-online-proceedings-library-archive/article/abs/passivation-and-annealing-for-improved-stability-of-high-performance-igzo-tfts/F539281481BA1AB93EE8AFD3323F4E1F
- ECS Trans. 114 (TFT 17) contents: https://proceedings.com/content/078/078795webtoc.pdf
- Hirschman, RIT news: https://www.rit.edu/news/299k-grant-rit-supports-flat-panel-display-development
- Kai Ni, Notre Dame project: https://strand.nd.edu/projects/ee-fabricating-ferroelectric-capacitor-crossbar-storage-and-computing
- Kai Ni, 2025 arXiv (search result only): https://arxiv.org/html/2504.09713v1
- Campbell, NIST publications: https://www.nist.gov/publications/search_by_author/1156601?page=2
- Jackson, Penn State ZnO TFTs: https://pure.psu.edu/en/publications/zno-thin-film-transistors-for-more-than-just-displays/
- Jackson, AVS 2008 abstract: https://www2.avs.org/symposium2008/Papers/Paper_EM-TuM11.html
- Kymissis, Columbia directory: https://www.engineering.columbia.edu/faculty-staff/directory/ioannis-kymissis
- imec In-poor IGZO (search result only): https://arxiv.org/abs/2412.07362v3
- imec IEDM 2025 IGZO reliability: https://imec-publications.be/handle/20.500.12860/59908
- imec IGZO 2T0C overview: https://www.imec-int.com/en/articles/disrupting-dram-roadmap-capacitor-less-igzo-dram-technology
- Negative RTN search (example result): https://researchonline.ljmu.ac.uk/id/eprint/23450/

**DRAM characterization**
- Patel, Rutgers profile: https://www.researchwithrutgers.com/en/persons/minesh-patel/
- Patel, Rutgers faculty-mentor page: https://honorsadvising.sas.rutgers.edu/opportunities/faculty-mentor-program/faculty-mentors/faculty-mentor/4455-patel-minesh
- Patel, CV: https://people.cs.rutgers.edu/~mp2099/files/minesh_patel_cv.pdf
- Patel, DiscoRD (search result only): https://arxiv.org/html/2603.12435v1
- DRAM Bender (ETH): https://www.research-collection.ethz.ch/handle/20.500.11850/642507
- DRAM Bender workshop (ASPLOS 2026): https://events.safari.ethz.ch/asplos26-ramulator-drambender
- Memory characterization lab (search result only): https://arxiv.org/pdf/2606.13725
- SoftMC (search result only): https://arxiv.org/pdf/1805.03195
- Qureshi, CV: https://www.cc.gatech.edu/cv/mqureshi4
- ArchShield (study log): https://memlab.ece.gatech.edu/papers/ISCA_2013_1.pdf
- Ghose, UIUC (student page): https://rwong.cs.illinois.edu/
- Ghose, PIM primer (UIUC affiliation): https://ar5iv.labs.arxiv.org/html/2012.03112
- Jian, Virginia Tech: https://news.vt.edu/articles/2018/02/SteveJian-cs-eng.html
- Jian, DBLP: https://dblp.dagstuhl.de/pid/130/7707-2.html
- Jian, patent: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11962327
- Antmicro RDIMM DDR5 tester 2.0: https://antmicro.com/blog/2024/12/data-center-rdimm-ddr5-tester-2-0/
- Antmicro RDIMM DDR5 tester (2023): https://antmicro.com/blog/2023/07/open-source-data-center-rdimm-ddr5-tester-for-memory-vulnerability-research/
- Antmicro DDR5 tester repo (study log): https://github.com/antmicro/ddr5-tester
- Google Rowhammer research support: https://blog.google/security/supporting-rowhammer-research-to/
- CHIPS Alliance SO-DIMM/LPDDR5 platform: https://chipsalliance.org/news/versatile-rowhammer-testing-platform/
- FuturePlus Systems: https://www.futureplus.com/get-quote
- Introspect M5513 listing: https://instrument.com.cn/show/C562419.html

**Re-check pass (2026-11-04, search snippets only)**
- Ye, EDL 2024 (vol. 45, no. 10, DOI 10.1109/LED.2024.3442729, via UNIST record): https://scholarworks.unist.ac.kr/handle/201301/85599
- Datta et al., IEDM 2020 IWO gain cell, leakage and retention at 25 and 85 °C (abstract record): https://investigadores.uandes.cl/en/publications/double-gate-w-doped-amorphous-indium-oxide-transistors-for-monoli/
- Alam, Purdue profile: https://engineering.purdue.edu/jump/1836580 ; Alam group: https://sites.google.com/view/alam-research-group/people
- Yu, gain-cell LLC paper (arXiv version; TC 75(3), March 2026): https://arxiv.org/pdf/2503.06304
- Patel, DiscoRD, 212 DDR4 chips (Semiconductor Engineering summary): https://semiengineering.com/identifying-read-disturbance-threshold-of-dram-chips-eth-zurich-rutgers/
- Peterson, Michigan pages: https://mse.engin.umich.edu/?p=1842 ; https://sites.google.com/a/umich.edu/petersonlab ; ZTO 2T0C thesis record: https://deepblue.lib.umich.edu/items/e6ac2d99-46aa-444a-bc41-2851e63c965c/full
- Hirschman, RIT directory: https://www.rit.edu/engineering/directory/kdhemc-karl-hirschman ; https://www.rit.edu/nanofab/directory/kdhemc-karl-hirschman
- Qureshi, FAST Lab (Georgia Tech School of Computer Science): https://fast.cc.gatech.edu/ ; DBLP: https://dblp.uni-trier.de/pid/60/6934.html
- Purdue Birck FY24 rates vs current (memo): https://mailman.ecn.purdue.edu/archives/list/bnc-all@ecn.purdue.edu/message/QV6GR6XQBKTW7PU5OCDG7VQOPHRKJ2JN/attachment/6/BRKFY24RatesvsCurrent.pdf
- Georgia Tech service-center rate list (April 2026): https://www.grants.gatech.edu/sites/default/files/inline-files/Srv%20Ctr%20Rate%20List%204.20.26.pdf ; IMS Micro/Nano Fabrication Facility: https://cleanroom.gatech.edu/articles/RateExamples
