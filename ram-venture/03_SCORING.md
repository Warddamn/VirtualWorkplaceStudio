# 03 — Kill & Score (Phase 3)

**American Memory venture study · Phase 3 deliverable · as of 2026-11-01 · agent `p3-writer`**

Inputs: `research/phase2/concepts_master.json`, `research/phase3/verify/batch_01..14.json` (kill-pass audits), `research/phase3/scores_raw/*.json` (9 scorer files), `models/scoring.py` → `scores.csv` + `research/phase3/rankings.md`, `research/phase3/selection.json`, `research/phase2/device_cost_output.md`. `python3 models/scoring.py` exits 0, and a re-run into a scratch directory reproduced `scores.csv` byte for byte. The tables in §2, §4, §5 and §7 are generated from these files. Revenue ceilings (§6) are [ESTIMATE] and are **not** part of any score.

---

## 0. Summary

| Stage | Count | What happened | Source |
|---|---|---|---|
| Raw Phase 2 cards | 102 | Five branch agents (A1–A3, B, C, D, E) | `concepts_master.json` |
| Distinct concepts | **98** | 4 same-idea merges (C-25, C-51, C-64, C-73) | `dedup_notes` |
| Killed in pre-scoring kill pass | **58** | 14 adversarial audits; one named rule per kill | `verify/batch_01..14.json` |
| Scored | **40** | 3 independent lenses × 10 criteria × 3 weightings | `scores.csv` |
| Killed at scoring | **9** | Default total < 55 and in no bundle | `selection.json` |
| Alive at end of Phase 3 | **31** | 17 in deep dives + 14 parked | `concepts_master.json` (Phase 3 state) |
| Deep dives | **5 bundles / 17 concepts** | Anchor plus the concepts scorers said belong inside it | `selection.json` |

> **Phase-3 snapshot; current status is in `SUMMARY_TABLE.md`.** Counts and statuses in §0–§8 (67 killed, 31 alive, 17 in deep dives, 14 parked, the §4 Status column) are as of the end of Phase 3. Later phases killed 16 more: 15 by the Phase 5 red team (C-12, C-16, C-22, C-26, C-32, C-48, C-62, C-64, C-65, C-73, C-74, C-75, C-85, C-86, C-91; see §9 and `05_REDTEAM.md`) and C-72 at the Phase 7 gate (`R1-UNSUPPORTED`). That leaves **15 alive and 83 killed** of 98.

**More "no" than "yes": by the end of Phase 3, 67 of 98 concepts (68%) were killed and only 17 went forward.**

1. **The device branch was gutted.** In Phase 3, branch A lost 32 of 43 concepts, and all 24 T3/T4 concepts are dead. None of the five T2 concepts that survived Phase 3 ranks above #20 under any weighting (the best is C-36, #20 under moonshot).
2. **Nothing this founder can build beats DDR5 on $/GB** (§3).
3. **The default top 20 is 100% T0/T1.** #1 (C-73, a cloud memory FinOps audit) is "not a memory business at all" (veteran scorer).
4. **Rank is not venture quality.** The rubric has no market-size criterion. By our [ESTIMATE], 11 of the top 15 top out below $0.5M ARR, and 12 of the 15 draw a scorer verdict of "side business", "feature", "lifestyle", "SKU", "gig", "lead-gen" or "not a venture" (§6). The deep dives exist to combine these small lines (§7).
5. **The lenses barely disagreed.** No criterion was flagged for disagreement, and 306 of 400 criterion scores were unanimous. That reflects shared inputs as much as truth (§1.5).

---

## 1. Method

### 1.1 Kill rules

| Rule | Fires when | Mission basis | Kills |
|---|---|---|---|
| `R1-UNSUPPORTED` | No credible evidence supports the core mechanism or core value claim | §2 rule 1 | 4 |
| `R3-FAB/T4` | The minimum path needs a DRAM-, NAND- or crosspoint-class fab, or more than $1B | §2 rule 3; A-11 | 7 |
| `R4-NO-WINNING-AXIS` | Loses on every axis the named buyer pays for, against that buyer's real (including free) alternatives | §2 rule 4 | 27 |
| `FACT-COLLAPSE` | Verification shows the premise is false (seat filled, supplier gone, product exists) | §5 quality bar | 8 |
| `NOT-A-VENTURE` | Bridge or content revenue, or speculation on the price cycle | §3D; §2 rule 10 | 6 |
| `QB-INCOMPLETE` | No fab, partner or buyer exists inside any horizon | §5 | 2 |
| `DUPLICATE` | The same idea as a kept card under another name or business-model lens | Phase 2 | 4 |
| `SCORE<55` | Default total < 55/100 and not in a deep-dive bundle | `selection.json` | 9 |

No file defines these rules in one place. The definitions above are reconstructed from how the 14 auditors applied them (`research/assumptions/p3-writer.md`). Rule 1 kills happen before scoring, as mission Phase 3 requires. The Kills column counts Phase 3 only; the later `RED-TEAM` (15) and Phase 7 gate `R1-UNSUPPORTED` (1) kills are tallied in `SUMMARY_TABLE.md`.

### 1.2 Evidence limits
- **Search budget.** The shared WebSearch budget (200 per turn) ran out during ideation. Branches C, D and E, and parts of A3 and B, relied on other agents' URLs, GitHub/PyPI and training knowledge tagged UNVERIFIED (`dedup_notes`).
- **Audit depth.** Of 497 card-cited URLs, auditors **opened 14**, confirmed 89 via search snippet, could not reach 9 and did not check 385. Of their 249 new evidence items, 242 came from snippets. Most facts here are therefore [REPORTED], not [VERIFIED].
- **What follows.** Kills that rest on the card's own numbers (most R3/R4) are robust. **Willingness to pay is STILL-UNVERIFIED for every survivor.** That is Phase 4's job.
- **Two price decks.** Kill reasons use $15.99 / $6.40 / $1.64 per GB (DDR5 4Q26 contract / glut / incumbent cost). The device model uses $20.37 / $8.15 / $1.48. Only C-26 and C-40 change $/GB tier between the decks, and the list of concepts that cannot beat the glut is identical on both. Some kill reasons also quote the card's own scratch $/GB rather than the device model's: C-02 ~$336 (model $360), C-03 ~$266 (model $291), C-04 $8.4 (model $8.50), C-58 $5.5–7.8 with 5-year depreciation (model $3.28). Model values are in §3 and `research/phase2/device_cost_output.md`; no kill changes.

### 1.3 Rubric anchors (`research/phase3/RUBRIC.md`; 5 is always best for the venture)

| Key | Criterion (weight) | 1 | 3 | 5 |
|---|---|---|---|---|
| `tech` | Technical feasibility (20) | TRL ≤ 3, shaky physics | TRL 4–6 | TRL 8–9, or software built with known techniques |
| `capital` | Capital, inverse (15) | T3/T4 | High T1 (4 = low T1; 2 = T2) | T0 (< $50k) |
| `ttr` | Time to revenue (15) | > 36 mo | 13–18 mo (4 = 7–12; 2 = 19–36) | ≤ 6 mo |
| `usmfg` | U.S. manufacturability (10) | Offshore only | Software/services, or U.S. assembly of imported die | U.S.-made with open partners |
| `margin` | Gross margin (10) | < 15% | 30–50% | ≥ 70% |
| `moat` | Moat (10) | Commodity | Know-how, certifications | Exclusive IP, qualification lock-in |
| `competition` | Density, inverse (5) | Crowded with funded incumbents | A few players | None in this niche |
| `regulatory` | Regulatory/export, inverse (5) | Gray zone or export-controlled | Manageable (ITAR, AS6081) | Negligible |
| `cycle` | Cycle-proofing (5) | Dies in a 2028–29 glut | Shrinks but survives | Glut-indifferent |
| `founder` | Founder-fit (5) | Process experts full-time from day one | 1–2 key hires | Founder's skills; part-time start |

### 1.4 Weightings (`models/scoring.py`)

| Weighting | tech | capital | ttr | usmfg | margin | moat | comp | reg | cycle | founder | Σ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Default | 20 | 15 | 15 | 10 | 10 | 10 | 5 | 5 | 5 | 5 | 100 |
| Capital-constrained | 20 | **30** | 15 | 10 | 10 | 10 | 5 | 5 | 5 | **10** | 120 |
| Moonshot | 20 | 15 | 15 | 10 | **20** | **20** | 5 | 5 | 5 | 5 | 120 |

Total = Σ(weight × score) / (5 × Σweights) × 100. Ties are broken by `tech`, then by id.

### 1.5 Lenses, consensus and disagreement
- **Lenses.** **veteran** (30-year DRAM process veteran plus device physicist), **vc** (memory VC who has lost money) and **founder** (bootstrapped, needs revenue). Each lens scored three chunks of 14/13/13 concepts, so every concept has three scores per criterion (`n_scorers` = 3).
- **Consensus = lower median.** With three scores that is just the median, so the conservative tie rule never fires. The justification is taken from a scorer whose score equals the consensus.
- **Disagreement flag = spread ≥ 3: 0 flags.** Of 400 cells, 306 were unanimous, 91 had spread 1 and 3 had spread 2 (C-67 regulatory, C-72 competition, C-51 regulatory).
- **Candidly,** the agents were independent but their inputs were not. All three read the same audits, anchors and calibration sheet (`research/phase3/survivors_compact.md`), so their agreement is not independent confirmation.

---

## 2. Kill register: all 67 concepts killed in Phase 3

Reasons are condensed from `kill_reason` (`concepts_master.json`). Full text and sources are in the audit batch named in each row (`bNN` = `research/phase3/verify/batch_NN.json`).

**Kills by rule and branch** (A device/materials · B architecture/systems · C U.S. manufacturing/supply chain · D software · E business-model lenses)

| Rule | A | B | C | D | E | Total |
|---|---|---|---|---|---|---|
| `R4-NO-WINNING-AXIS` | 15 | 3 | 4 | 2 | 3 | **27** |
| `FACT-COLLAPSE` | 3 | 2 | 3 | 0 | 0 | **8** |
| `R3-FAB/T4` | 5 | 0 | 1 | 0 | 1 | **7** |
| `NOT-A-VENTURE` | 1 | 0 | 0 | 2 | 3 | **6** |
| `R1-UNSUPPORTED` | 0 | 1 | 1 | 1 | 1 | **4** |
| `DUPLICATE` | 1 | 0 | 0 | 1 | 2 | **4** |
| `QB-INCOMPLETE` | 2 | 0 | 0 | 0 | 0 | **2** |
| `SCORE<55` | 5 | 4 | 0 | 0 | 0 | **9** |
| Killed pre-scoring | 27 | 6 | 9 | 6 | 10 | **58** |
| **Killed total (Phase 3)** | **32** | **10** | **9** | **6** | **10** | **67** |
| Alive (end of Phase 3) | 11 | 4 | 6 | 6 | 4 | **31** |
| Concepts | 43 | 14 | 15 | 12 | 14 | **98** |
| Kill rate (Phase 3) | 74% | 71% | 60% | 50% | 71% | **68%** |

**By capital tier (end of Phase 3):** T0 8 killed / 12 alive · T1 12 killed / 14 alive · T2 23 killed / 5 alive · T3 17 killed / 0 alive · T4 7 killed / 0 alive

### `R4-NO-WINNING-AXIS` — 27 killed

| ID | Concept | Br | Tier | Audit | Reason |
|---|---|---|---|---|---|
| C-02 | Standalone IGZO 2T0C DRAM die on a depreciated U.S. 200mm line (commodity DRAM substitute) | A | T3 | b01 | ~$336/GB (52x glut) for a buyer who pays on $/GB; even a hypothetical 300mm version is 1.8x glut. |
| C-03 | IGZO memory printed on idle display-fab glass | A | T3 | b01 | ~$266/GB, microsecond access, buyer "none"; no Gen-scale U.S. panel fab exists. |
| C-15 | Onshore In-Ga-Zn oxide sputter-target and ALD-precursor supply for IGZO-channel DRAM | A | T2 | b02 | Only axis is supply security; incumbents already non-Chinese; no onshore IGZO-DRAM volume customer. |
| C-17 | DDR3-EOL Socket Swap to ST-DDR4 MRAM | A | T0 | b03 | ST-DDR4 is ~32x DDR3 spot and not pin-compatible; respin to U.S.-made Manassas DDR4 is cheaper. |
| C-19 | New Fabless Discrete STT-MRAM Vendor | A | T2 | b03 | Avalanche already ships 1-8Gb STT-MRAM; a 4Gb entrant 42 months out at ~$72/GB, mid patent war. |
| C-20 | MRAM Main-Memory DIMM / CXL Module | A | T2 | b03 | ~$94.9/GB (14.8x glut), 42-46x less dense; the card's own buyer is "none at scale". |
| C-23 | University / Expired-Patent CBRAM-ReRAM IP Licensor | A | T2 | b04 | Weebit, TSMC RRAM and GF CBRAM are qualified; expired patents give nothing exclusive. |
| C-24 | RRAM Analog In-Memory-Compute Edge AI Chip | A | T3 | b04 | TetraMem already ships this (MLX200/MLX300); an entrant reaches silicon ~2029-30 on T3 money. |
| C-30 | Floating-body 1T-DRAM (Z-RAM lineage) on U.S. SOI | A | T3 | b05 | ~$24/GB (3.8x glut) and still refreshes; no retention or latency edge behind DDR. |
| C-31 | Thyristor RAM revival (T-RAM TCCT / Kilopass VLT) | A | T3 | b05 | Only the never-arrayed VLT beats DRAM; TCCT ~$18/GB; gain cells win the cache socket. |
| C-34 | Depreciated-fab revival of IBM-heritage deep-trench eDRAM | A | T3 | b05 | ~$20/GB on depreciated wafers; the 2 ns edge is lost behind DDR; no host fab. |
| C-35 | Trailing-node bulk SRAM as a DRAM substitute (SRAM-DIMM/CXL) | A | T2 | b05 | SRAM ~$55-120/GB, silicon to tested die (9-19x glut); latency lost behind a DDR4/CXL controller; no buyer. |
| C-38 | Memory-only wafer-scale SRAM ('Cerebras for RAM') | A | T3 | b06 | ~$1,000/GB packaged (~156x glut); the SerDes perimeter yields CXL-class performance. |
| C-40 | Nantero NRAM (carbon-nanotube) license and U.S. second source | A | T2 | b06 | CNT advantages hidden by bulk-CMOS periphery; ties MRAM/F-RAM/ReRAM 48 months late; licensor dormant. |
| C-42 | Printed organic ferroelectric memory (Thinfilm post-mortem) | A | T2 | b06 | ~$4x10^7/GB, ms latency, 10^3-10^5 endurance; only market is anti-counterfeit labels. |
| C-46 | Flash KV Accelerator (U.S. Pliops-style NVMe KV engine) | B | T2 | b07 | Free NVMe KV tiers (Dynamo KVBM, LMCache); the Pliops ASIC and NVIDIA ICMS beat an FPGA card. |
| C-50 | Rack-Scale CXL Pooling Appliance | B | T3 | b07 | Pond saves ~7% of DRAM; Octopus finds switches raise net cost; ~$7-22k per 12 TB pod. |
| C-57 | Memory-Fabric SuperNIC (Ethernet-attached DRAM for GPUs) | B | T3 | b08 | NVIDIA bought Enfabrica (>$900M); RDMA + Mooncake/NIXL already give GPU-reachable memory. |
| C-59 | U.S.-HQ fabless long-lifecycle DRAM brand on Taiwanese foundry wafers | C | T2 | b09 | Alliance Memory et al. already run it; ~$15M NRE, 36-48 months; PSMC is selling its fab to Micron. |
| C-60 | 'Assembled in USA' commodity DDR4/DDR5 module brand | C | T1 | b09 | U.S. assembly adds 0.7% of module value, and nobody pays a premium for it (TAA, 0% Section 232). |
| C-63 | Die harvesting and module rebuild from e-waste, Shenzhen-style | C | T0 | b09 | An intact RDIMM (~$192) is worth more than its harvested chips (~$72); reballs read as counterfeit. |
| C-71 | Trusted low-density SDRAM (64-512Mb) on SkyWater Fab 25 with 1T1C MIM cells | C | T2 | b10 | ~$30 cost vs $2-5 COTS SDRAM still in production; DoD does not require trusted COTS memory. |
| C-77 | NVMe-as-RAM Virtual Memory Software | D | T1 | b11 | Linux swap+zswap and K8s LimitedSwap do NAND-as-memory free; NAND is ~1000x slower. |
| C-81 | Secondary DRAM Marketplace for Excess Inventory | D | T1 | b12 | Mobius Materials already runs this marketplace with in-house inspection; a cold start has no liquidity. |
| C-90 | DIMM leasing / memory-as-a-service financing for neoclouds | E | T2 | b13 | Neoclouds already finance DRAM inside cheaper GPU-backed debt; residual losses run -29% to -58% IRR. |
| C-93 | 'Compliant memory' federal reseller on GSA MAS / SEWP (compliance-as-a-product) | E | T1 | b14 | Every major-brand reseller is already compliant; no SEWP seat vs 2,115 SEWP VI holders. |
| C-98 | Memory patent expiry and litigation radar | E | T0 | b14 | Unified Patents, Google Patents and USPTO are free; FTO needs attorney opinions, not dashboards. |

### `FACT-COLLAPSE` — 8 killed

| ID | Concept | Br | Tier | Audit | Reason |
|---|---|---|---|---|---|
| C-09 | U.S. design-in and module partner for FMC DRAM+ (HfO2 non-volatile DRAM) | A | T1 | b02 | FMC has no chips, specs or timeline; Neumonda already fills the partner seat. |
| C-10 | FeFET embedded NVM licensing on GlobalFoundries 22FDX for U.S. MCU/edge SoCs | A | T3 | b02 | FMC licenses foundries directly; GF FDX eNVM is eMRAM made in Dresden; 0% margin for us. |
| C-21 | Second U.S. MTJ BEOL Line on a Depreciated 200mm Fab | A | T2 | b03 | The Everspin-Microchip Fab 4 deal (2H-2027) already builds it; Honeywell sells rad-hard MRAM. |
| C-53 | High-Bandwidth Flash (HBF) Weight-Store Module | B | T3 | b08 | HBF attaches over UCIe in-package, so only NVIDIA/AMD/hyperscaler package owners can integrate it. |
| C-54 | PIM DIMM Accelerator Servers (UPMEM / AiM) for Scans and Genomics | B | T1 | b08 | UPMEM, the only merchant PIM DIMM, was acquired by Qualcomm (2025-06); AiMX is still a prototype. |
| C-66 | High-capacity stacked-die legacy modules (32GB DDR3 RDIMM, 32GB DDR3L SODIMM) | C | T1 | b10 | Intelligent Memory already sells 32GB DDR3 RDIMMs; a 32GB DDR3L SO-DIMM cannot be built. |
| C-68 | HBM-adjacent U.S. test and rework services near Amkor Peoria / SK hynix West Lafayette | C | T3 | b10 | U.S. HBM plants are captive; Amkor Peoria does not stack HBM; failed stacks are scrapped. |
| C-69 | U.S. known-good-die wafer-probe and die-processing house for legacy DRAM | C | T1 | b10 | Micross Apopka already probes ~850 wafers/yr; the choke point is die supply, not probing. |

### `R3-FAB/T4` — 7 killed

| ID | Concept | Br | Tier | Audit | Reason |
|---|---|---|---|---|---|
| C-04 | OCTRAM-class 4F2 IGZO-on-capacitor low-refresh DRAM as a U.S. second source | A | T4 | b01 | Needs a DRAM capacitor fab (only Micron's, captive); demo cost is 5.1x incumbent. |
| C-05 | License NEO Semiconductor 3D X-DRAM and build it in the U.S. | A | T4 | b01 | Needs a 3D-NAND-class fab; single-cell company proof of concept; NEO licenses only to makers. |
| C-08 | Ferroelectric 'Optane-slot' persistent memory (NVDRAM-class HZO 1T1C NVDIMM/CXL) | A | T4 | b01 | Needs a captive DRAM capacitor fab; Micron never productized NVDRAM. |
| C-11 | SunRise-style 3D NOR 'quasi-volatile' memory as a DRAM substitute | A | T4 | b02 | Needs a NAND-class fab; no public array silicon after $75M+; pivoting to FeRAM. |
| C-25 | 3D XPoint / PCM Crosspoint Revival for the CXL Memory Tier | A | T4 | b04 | Needs a new 300mm crosspoint fab; Intel lost >$7B; $0.99/GB holds only at full loading. |
| C-58 | Legacy-DRAM fab in the U.S. on a licensed 25-46nm process | C | T4 | b09 | $2.0-3.5B capex for $5.5-7.8/GB vs $7.2/GB glut DDR4; Manassas already serves these buyers. |
| C-96 | Acquire the 3D XPoint/Optane IP estate and license it (business-model Optane revival) | E | T4 | b14 | IP without a line is worthless; any product path needs a >$1B fab; title is contested. |

### `NOT-A-VENTURE` — 6 killed

| ID | Concept | Br | Tier | Audit | Reason |
|---|---|---|---|---|---|
| C-14 | MemTech Atlas: emerging-memory device-parameter and $/GB cost-model data product | A | T0 | b02 | Research-content subscription (bridge only); Stanford Memory Trends and NVMDB are free. |
| C-82 | Consumer RAM Price Tracker + Upgrade Compatibility Advisor | D | T0 | b12 | Affiliate/SEO site; PCPartPicker and 37+ trackers already free. |
| C-83 | Shortage Briefing: Paid Memory-Market Newsletter | D | T0 | b12 | Self-labeled bridge newsletter at $2-6k MRR; the topic dies in a glut. |
| C-88 | DRAM price-cap / allocation-guarantee subscription | E | T2 | b13 | A short call on the DRAM price (99th-percentile loss $1.5-2.1M per $1M); needs an insurer. |
| C-89 | Buy-and-hold DRAM inventory arbitrage | E | T1 | b13 | Spot is ~1.69x contract, so the expected 12-month return is -46%; pure speculation. |
| C-95 | SBA/search-fund acquisition of a small memory reseller at peak earnings | E | T2 | b14 | DSCR 0.65 in a normal year, 0.33 in a glut: a leveraged long DRAM bet; no target named. |

### `R1-UNSUPPORTED` — 4 killed

| ID | Concept | Br | Tier | Audit | Reason |
|---|---|---|---|---|---|
| C-56 | TrustedCXL: U.S.-Provenance DDR4 CXL Expander for DoD/DOE HPC | B | T2 | b08 | No evidence DoD pays a U.S.-origin DRAM premium (TAA, BAA-exempt COTS, 0% Section 232). |
| C-70 | All-domestic DRAM component: Micron Manassas wafer to U.S. package to U.S. module | C | T2 | b10 | The same unsupported premium; Manassas takes no outside customers; ~0% GM without it. |
| C-78 | Consumer 'Virtual RAM Booster' App | D | T0 | b11 | OSes already compress memory by default; the card itself marks the claim UNSUPPORTED. |
| C-87 | DRAM futures/swap market (index-settled forwards) | E | T3 | b13 | Every DRAM futures attempt has failed (SGX 2003 onward); no settlement-grade index. |

### `DUPLICATE` — 4 killed

| ID | Concept | Br | Tier | Audit | Reason |
|---|---|---|---|---|---|
| C-43 | Cryo-CMOS gain-cell eDRAM IP for quantum-computer control | A | T1 | b06 | C-32 plus a 4 K characterization deck; physics fine (TRL 4). |
| C-76 | Software-Defined Memory Pooling / RAM-as-a-Service over CXL | D | T2 | b11 | C-50 under a software-licensing lens; Kove:SDM still sells. |
| C-94 | STTR vehicle on a national-lab / university memory patent (lab-patent studio) | E | T1 | b14 | A funding structure for C-06/C-07, not a product; revenue ~46 months out. |
| C-97 | CXL memory-tiering integration practice (consulting -> managed tuning) | E | T0 | b14 | Services packaging of C-49: same buyers, modules and tuning stack. |

### `QB-INCOMPLETE` — 2 killed

| ID | Concept | Br | Tier | Audit | Reason |
|---|---|---|---|---|---|
| C-27 | SOT-MRAM Last-Level-Cache Chiplet | A | T3 | b04 | No foundry offers SOT-MRAM; Antaios closed; ~$280/GB. |
| C-41 | 2D-material (MoS2/WSe2) gain-cell DRAM or 2D flash | A | T3 | b06 | No buyer and no production partner; the cited result is graphene flash. |

### `SCORE<55` — 9 killed (at scoring: default total < 55 and in no bundle; `selection.json` records the scorers as unanimous "pass")

| ID | Concept | Br | Tier | Default (rank) | Reason |
|---|---|---|---|---|---|
| C-51 | Persistent CXL Log Card (post-Optane PMem for WAL/journals) | B | T2 | 53.0 (#32) | SMART/Penguin NV-CMM is already sampling at Tier-1 OEMs; entrant 36 months late. |
| C-07 | AlScN ferro-diode memory for 500-600C electronics (Penn/AFRL license + STTR) | A | T1 | 52.0 (#33) | Empty niche, but ~42 months and no 500C periphery; a grant program, not revenue. |
| C-06 | U.S.-made HZO FeRAM family (1-16 Mb, rad-hard option) via SkyWater + Sandia | A | T2 | 50.0 (#34) | 54 months and $10-30M; Infineon F-RAM is already fabbed in Dallas. |
| C-44 | DDR4 Second-Life CXL Expander | B | T2 | 50.0 (#35) | T2 hardware needing Marvell allocation; ~$270-540 kept per card; hyperscalers DIY. |
| C-01 | OS-eDRAM: IGZO/IWO 2T0C gain-cell memory IP on a U.S. 200mm foundry | A | T2 | 48.0 (#36) | TRL 4, ~48 months, needs an oxide module no U.S. fab has; C-32 is the cheaper path. |
| C-28 | eMRAM-Unified-Memory Edge MCU (no external DRAM) | A | T2 | 45.0 (#37) | Head-on against four MCU giants, fabbed in Dresden, 48 months out. |
| C-39 | U.S.-fabbed SRAM-only LLM inference accelerator (Groq pattern) | A | T3 | 45.0 (#38) | A $150-400M chip program vs Groq/NVIDIA/Cerebras on a node 2-3x behind. |
| C-47 | Compressed CXL Expander (licensed inline compression IP) | B | T2 | 45.0 (#39) | FPGA integrator of non-exclusive IP vs Marvell's ASIC; the glut erases the savings. |
| C-52 | LPDDR 'HBM-lite' Memory Chiplet (UCIe/AIB-attached) | B | T3 | 40.0 (#40) | A $50-90M chip with under half an HBM3E stack's bandwidth; buyers license PHYs directly. |

---

## 3. Device $/GB verdict: what Rule 4 did to the device branch

From `research/phase2/device_cost_output.md` (`models/device_cost_compare.py`): DDR5 incumbent **cost $1.48/GB**, 4Q26 contract **$20.37**, A-05 glut **$8.15**, severe glut $2.04. Best case = wafer cost −30% and yield 0.95.

| Concept | Device | Base $/GB | Best $/GB | ÷ glut | Fate (end of Phase 3) |
|---|---|---|---|---|---|
| C-25 | 3D XPoint PCM, 4-deck | 0.99 | 0.57 | 0.12× | KILLED R3: T4 crosspoint fab, cost holds only at Optane-killing loading |
| C-05 | NEO 3D X-DRAM (claim) | 1.22 | 0.96 | 0.15× | KILLED R3: 3D-NAND fab; single-cell company proof |
| C-26 | Salvaged Optane PMem | 2.06 | 1.53 | 0.25× | **ALIVE (DD1)**: resale, not a build; sunsets 2027-10-11 |
| C-15 | Samsung IGZO 4F2 (demand) | 2.94 | 1.90 | 0.36× | KILLED R4: Samsung's device; the venture sells only targets |
| C-58 | Licensed DDR4, new U.S. fab | 3.28 | 2.17 | 0.40× | KILLED R3: $2.0–3.5B |
| C-59 | Fabless DDR3 on PSMC | 4.12 | 2.94 | 0.51× | KILLED R4: no wafers in a shortage |
| C-08 | NVDRAM HZO 1T1C | 4.19 | 2.41 | 0.51× | KILLED R3: captive DRAM fab |
| C-11 | SunRise 3D NOR | 5.08 | 2.50 | 0.62× | KILLED R3: NAND fab; claimed density |
| C-04 | OCTRAM IGZO-on-capacitor | 8.50 | 4.26 | 1.04× | KILLED R3: DRAM capacitor fab |
| C-31/30/40 | T-RAM / 1T-DRAM / NRAM | 17.7–30.7 | 11.5–18.1 | 2.2–3.8× | KILLED R4: dead in a glut |
| C-32 | Si gain-cell eDRAM 28nm | 47.1 | 31.3 | 5.8× | **ALIVE (DD5)**: competes with 6T SRAM ($87.3/GB), not DDR5 |
| C-16 | 1Gb STT-MRAM (PLP) | 94.9 | 64.2 | 12× | **ALIVE (DD3)**: sold per SSD design |
| C-37 | GSI APU in-SRAM compute | 291 | 182 | 36× | parked: compute-energy axis |
| C-12 | F-RAM (PZT) | 700 | 515 | 86× | **ALIVE (DD3)**: priced against a lithium battery |
| C-36 / C-33 | SRAM, Fab 25 / S130 | 1,234 / 1,455 | 1,071 / 965 | 151–179× | C-36 parked; C-33 DD5: provenance, lifecycle |
| C-22 / C-18 | ReRAM S130 / Toggle MRAM | 3,539 / 3,797 | 2,982 / 2,665 | 434–466× | C-22 DD5; C-18 parked: rad-hard, non-volatility |

**Verdict.** 34 of the 44 costed concepts cannot beat the glut price under any sensitivity, on either price deck. Only the T4-fab concepts C-05 and C-25 approach DDR5 cost. Eight beat the glut at base inputs. Each of them needs a T3/T4 fab or foundry wafers that are allocated away in a shortage, rests on a claim, is someone else's device (C-15), or (C-26) is salvage. **None beats the glut on $/GB with something this founder can build.** Rule 4 killed every $/GB-only device (C-02, C-03, C-30, C-35, C-38, C-42). Eight of the nine Phase-3 branch-A survivors with device rows sell on another axis (non-volatility, lifecycle, rad-hard, provenance, compute energy, density vs SRAM), per part or per card rather than per GB. The ninth, C-26, wins on $/GB only as salvage.

---

## 4. Scores of all 40 scored concepts

Consensus scores (1–5) from `scores.csv`. Column order: te tech · ca capital · tt time to revenue · mf U.S. mfg · mg margin · mo moat · co competition · re regulatory · cy cycle · fo founder. Totals are 0–100, with rank in brackets. Status (end of Phase 3; current status in `SUMMARY_TABLE.md`): DDn = in deep dive n; parked = alive, not selected; KILLED = `SCORE<55`.

| # | ID | Concept | Tier | te | ca | tt | mf | mg | mo | co | re | cy | fo | Default | Cap-con | Moonshot | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | C-73 | Memory FinOps Audit (cloud SaaS) | T0 | 5 | 5 | 5 | 3 | 4 | 1 | 1 | 5 | 5 | 5 | 82.0 (1) | 85.0 (1) | 76.7 (1) | DD4 |
| 2 | C-12 | Battery-free F-RAM NVSRAM modules | T0 | 5 | 5 | 4 | 3 | 3 | 2 | 3 | 5 | 5 | 4 | 80.0 (2) | 82.5 (2) | 75.0 (6) | DD3 |
| 3 | C-33 | OpenRAM macro service (SkyWater S130) | T0 | 4 | 5 | 4 | 4 | 4 | 2 | 3 | 5 | 5 | 4 | 80.0 (3) | 82.5 (5) | 76.7 (2) | DD5 |
| 4 | C-29 | NVM-EOL Migration Finder | T0 | 5 | 5 | 4 | 3 | 5 | 1 | 1 | 5 | 3 | 5 | 79.0 (4) | 82.5 (3) | 75.8 (4) | DD2 |
| 5 | C-80 | DRAM Cost & Allocation Intel (SMB OEMs) | T0 | 5 | 5 | 5 | 3 | 5 | 1 | 1 | 4 | 1 | 5 | 79.0 (5) | 82.5 (4) | 75.8 (5) | DD2 |
| 6 | C-64 | CleanBOM-5949 provenance verification | T0 | 4 | 5 | 4 | 3 | 5 | 2 | 3 | 2 | 5 | 5 | 78.0 (6) | 81.7 (6) | 76.7 (3) | DD1 |
| 7 | C-75 | KV-cache tier integration & tuning | T0 | 5 | 5 | 4 | 3 | 4 | 1 | 1 | 4 | 5 | 3 | 76.0 (7) | 78.3 (8) | 71.7 (9) | DD4 |
| 8 | C-86 | Memory Cost Escalation Index + EPA kit | T0 | 4 | 5 | 3 | 3 | 4 | 3 | 3 | 4 | 4 | 4 | 75.0 (8) | 78.3 (9) | 74.2 (7) | DD2 |
| 9 | C-26 | Optane PMem salvage | T0 | 5 | 5 | 5 | 3 | 2 | 1 | 2 | 4 | 1 | 5 | 74.0 (9) | 78.3 (7) | 66.7 (12) | DD1 |
| 10 | C-74 | Fleet Memory-Reclaim Autopilot (on-prem) | T1 | 4 | 4 | 4 | 3 | 5 | 2 | 3 | 5 | 3 | 3 | 74.0 (10) | 74.2 (13) | 73.3 (8) | DD4 |
| 11 | C-85 | DIMM Health Subscription + spares | T0 | 4 | 5 | 4 | 3 | 4 | 2 | 2 | 4 | 3 | 4 | 74.0 (11) | 77.5 (10) | 71.7 (10) | DD1 |
| 12 | C-84 | Embedded RAM-Diet Profiler | T0 | 5 | 5 | 4 | 3 | 4 | 1 | 3 | 4 | 1 | 2 | 73.0 (12) | 75.0 (12) | 69.2 (11) | parked |
| 13 | C-79 | TB-RAM rental on recovered DDR4 | T1 | 5 | 4 | 5 | 3 | 3 | 1 | 2 | 4 | 2 | 3 | 72.0 (13) | 72.5 (14) | 66.7 (14) | parked |
| 14 | C-62 | ProvenRAM graded recovered RDIMMs | T0 | 5 | 5 | 5 | 3 | 2 | 1 | 1 | 3 | 1 | 4 | 71.0 (14) | 75.0 (11) | 64.2 (16) | DD1 |
| 15 | C-48 | On-prem MoE Box | T1 | 5 | 4 | 4 | 3 | 2 | 1 | 2 | 4 | 4 | 4 | 70.0 (15) | 71.7 (15) | 63.3 (19) | parked |
| 16 | C-61 | DRAM Continuity Vault (LTB) | T1 | 5 | 4 | 3 | 3 | 2 | 3 | 2 | 4 | 4 | 3 | 70.0 (16) | 70.8 (16) | 66.7 (13) | DD2 |
| 17 | C-18 | NewSpace MRAM rad-data & upscreen | T1 | 5 | 4 | 3 | 3 | 2 | 2 | 2 | 2 | 5 | 3 | 67.0 (17) | 68.3 (17) | 62.5 (21) | parked |
| 18 | C-13 | Emerging-memory test & qual lab | T1 | 5 | 3 | 3 | 3 | 3 | 2 | 3 | 4 | 3 | 2 | 66.0 (18) | 64.2 (20) | 63.3 (17) | parked |
| 19 | C-16 | Supercap-Killer MRAM PLP kit | T1 | 5 | 4 | 2 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 66.0 (19) | 67.5 (18) | 63.3 (18) | DD3 |
| 20 | C-72 | Legacy-DRAM buying co-op | T1 | 3 | 4 | 3 | 3 | 5 | 2 | 3 | 4 | 1 | 3 | 64.0 (20) | 65.8 (19) | 65.0 (15) | DD2 |
| 21 | C-36 | Fab 25 long-life SRAM second source | T2 | 4 | 2 | 2 | 4 | 4 | 3 | 2 | 4 | 5 | 1 | 62.0 (21) | 57.5 (26) | 63.3 (20) | parked |
| 22 | C-49 | TB-class CXL node | T1 | 5 | 3 | 3 | 3 | 2 | 1 | 1 | 5 | 2 | 2 | 60.0 (22) | 59.2 (22) | 55.0 (28) | parked |
| 23 | C-92 | AS6171 counterfeit-detection lab | T1 | 5 | 3 | 3 | 3 | 2 | 2 | 1 | 3 | 2 | 2 | 60.0 (23) | 59.2 (23) | 56.7 (26) | parked |
| 24 | C-45 | KV Pool Node appliance | T1 | 5 | 3 | 3 | 3 | 1 | 1 | 1 | 5 | 3 | 2 | 59.0 (24) | 58.3 (24) | 52.5 (32) | parked |
| 25 | C-32 | Si gain-cell eDRAM IP | T2 | 3 | 2 | 2 | 4 | 5 | 2 | 2 | 4 | 5 | 2 | 59.0 (25) | 55.8 (28) | 60.8 (22) | DD5 |
| 26 | C-67 | Rugged CAMM2/SODIMM at U.S. EMS | T1 | 5 | 3 | 2 | 3 | 2 | 2 | 1 | 4 | 2 | 2 | 58.0 (26) | 57.5 (25) | 55.0 (29) | parked |
| 27 | C-55 | Analog CIM edge module | T1 | 4 | 3 | 2 | 3 | 3 | 2 | 2 | 3 | 4 | 2 | 58.0 (27) | 57.5 (27) | 56.7 (27) | parked |
| 28 | C-91 | Authorized EOL DRAM die bank | T2 | 5 | 2 | 1 | 3 | 3 | 4 | 1 | 3 | 3 | 1 | 57.0 (28) | 53.3 (30) | 59.2 (23) | parked |
| 29 | C-37 | GSI APU vector-search appliance | T1 | 4 | 4 | 2 | 3 | 2 | 1 | 2 | 3 | 3 | 3 | 57.0 (29) | 60.0 (21) | 52.5 (33) | parked |
| 30 | C-65 | Hi-rel DDR4 MCM design house | T2 | 4 | 2 | 2 | 4 | 3 | 3 | 1 | 3 | 4 | 1 | 57.0 (30) | 53.3 (31) | 57.5 (25) | parked |
| 31 | C-22 | TrustNVM ReRAM chiplet (S130) | T2 | 3 | 2 | 1 | 5 | 4 | 3 | 2 | 3 | 5 | 2 | 57.0 (31) | 54.2 (29) | 59.2 (24) | DD5 |
| 32 | C-51 | Persistent CXL log card | T2 | 4 | 2 | 2 | 3 | 2 | 2 | 2 | 3 | 4 | 2 | 53.0 (32) | 50.8 (33) | 50.8 (35) | KILLED |
| 33 | C-07 | AlScN ferro-diode 600C memory | T1 | 2 | 3 | 1 | 3 | 3 | 3 | 4 | 3 | 5 | 2 | 52.0 (33) | 52.5 (32) | 53.3 (31) | KILLED |
| 34 | C-06 | HZO FeRAM family (SkyWater+Sandia) | T2 | 3 | 2 | 1 | 2 | 4 | 3 | 2 | 3 | 5 | 1 | 50.0 (34) | 47.5 (35) | 53.3 (30) | KILLED |
| 35 | C-44 | DDR4 second-life CXL expander | T2 | 3 | 2 | 2 | 3 | 2 | 2 | 3 | 4 | 3 | 2 | 50.0 (35) | 48.3 (34) | 48.3 (36) | KILLED |
| 36 | C-01 | OS-eDRAM IGZO 2T0C IP | T2 | 2 | 2 | 1 | 2 | 4 | 3 | 3 | 4 | 5 | 1 | 48.0 (36) | 45.8 (36) | 51.7 (34) | KILLED |
| 37 | C-28 | eMRAM unified-memory edge MCU | T2 | 4 | 2 | 1 | 1 | 3 | 2 | 1 | 4 | 2 | 1 | 45.0 (37) | 43.3 (37) | 45.8 (37) | KILLED |
| 38 | C-39 | SRAM-only LLM accelerator | T3 | 4 | 1 | 1 | 4 | 2 | 2 | 1 | 3 | 2 | 1 | 45.0 (38) | 40.8 (39) | 44.2 (38) | KILLED |
| 39 | C-47 | Compressed CXL expander | T2 | 3 | 2 | 2 | 3 | 2 | 1 | 2 | 5 | 1 | 1 | 45.0 (39) | 43.3 (38) | 42.5 (39) | KILLED |
| 40 | C-52 | LPDDR "HBM-lite" chiplet | T3 | 3 | 1 | 1 | 2 | 3 | 2 | 2 | 3 | 2 | 1 | 40.0 (40) | 36.7 (40) | 41.7 (40) | KILLED |

### 4.1 Top 15 (default): per-criterion justification
Each line is condensed from the matching `*_why` column of `scores.csv`. Totals are shown as default / capital-constrained / moonshot.

**#1 C-73 Memory FinOps Audit (cloud SaaS)** (T0; 82.0 / 85.0 / 76.7)

- tech 5: FinOps right-sizing on known tools; TRL 9.
- capital 5: T0 web app plus audits.
- ttr 5: ~6 months to first audit.
- U.S. mfg 3: Software; no U.S. manufacturing.
- margin 4: 60-80%; year 1 is consulting.
- moat 1: Free floor: Compute Optimizer, KRR, OpenCost.
- competition 1: CAST AI, ScaleOps, Kubecost and others.
- regulatory 5: Negligible.
- cycle 5: EC2 prices flat; glut irrelevant.
- founder 5: Web app + AWS APIs, part-time.

**#2 C-12 Battery-free F-RAM NVSRAM modules** (T0; 80.0 / 82.5 / 75.0)

- tech 5: Shipping parallel F-RAM; controller validation only.
- capital 5: T0: PCB, EMS run, inventory.
- ttr 4: ~10 months to first SKUs.
- U.S. mfg 3: U.S. EMS assembly of imported F-RAM.
- margin 3: 40-55%; free adapters cap DIP prices.
- moat 2: Validation know-how only.
- competition 3: No battery-free validated PCMCIA card found.
- regulatory 5: Negligible; removes lithium hazmat.
- cycle 5: Priced against batteries, not DDR5.
- founder 4: PCB/firmware fit; needs CNC access.

**#3 C-33 OpenRAM macro service (SkyWater S130)** (T0; 80.0 / 82.5 / 76.7)

- tech 4: Only 1-4 KB macros published; 1 KB silicon-proven.
- capital 5: ~200 h layout + one shuttle slot.
- ttr 4: 9-15 months.
- U.S. mfg 4: Silicon made at SkyWater Bloomington.
- margin 4: 55-75%.
- moat 2: BSD base; funnel owners could bundle free.
- competition 3: No paid sky130 macro vendor found.
- regulatory 5: EAR99.
- cycle 5: Tracks MPW activity, not DRAM.
- founder 4: Python/web fit; buys ~200 VLSI hours.

**#4 C-29 NVM-EOL Migration Finder** (T0; 79.0 / 82.5 / 75.8)

- tech 5: Software on distributor APIs; TRL 9.
- capital 5: Hosting and APIs.
- ttr 4: 6-9 months.
- U.S. mfg 3: Software.
- margin 5: 75-85% SaaS.
- moat 1: Copyable; Octopart/Nexar building it.
- competition 1: SiliconExpert, Z2Data, Accuris, Supplyframe.
- regulatory 5: EAR99.
- cycle 3: EOLs persist; premium appetite falls.
- founder 5: Pure software; market size is the risk.

**#5 C-80 DRAM Cost & Allocation Intel (SMB OEMs)** (T0; 79.0 / 82.5 / 75.8)

- tech 5: Public distributor APIs plus spot trackers.
- capital 5: Web app.
- ttr 5: MVP in months; revenue ~2Q27.
- U.S. mfg 3: Software.
- margin 5: 70-85% after a data licence.
- moat 1: No proprietary data.
- competition 1: Supplyframe CIQ, Counterpoint, SiliconExpert.
- regulatory 4: Contract data not redistributable.
- cycle 1: Alerts worthless at the glut.
- founder 5: Founder is a sample buyer.

**#6 C-64 CleanBOM-5949 provenance verification** (T0; 78.0 / 81.7 / 76.7)

- tech 4: SPD scan commodity; die-source database unproven.
- capital 5: Software plus lab pass-through.
- ttr 4: 9-15 months; awaits final FAR rule.
- U.S. mfg 3: Software; U.S. AS6171 labs.
- margin 5: 65-75%.
- moat 2: Only a die-source dataset defends.
- competition 3: No memory §5949 product yet.
- regulatory 2: Proposed rule allows self-attestation.
- cycle 5: Statute-driven; glut raises CXMT share.
- founder 5: Software; lab outsourced.

**#7 C-75 KV-cache tier integration & tuning** (T0; 76.0 / 78.3 / 71.7)

- tech 5: Shipping OSS (LMCache, Dynamo, Mooncake).
- capital 5: ~$5-15k public benchmark.
- ttr 4: ~12 months to $15-40k engagements.
- U.S. mfg 3: Services on U.S. GPU clusters.
- margin 4: 50-70%, services-heavy.
- moat 1: Apache-2.0; Tensormesh owns monitoring.
- competition 1: Tensormesh ($24.5M), free Dynamo, WEKA.
- regulatory 4: Possible BAAs for health/legal buyers.
- cycle 5: Saves GPU-hours; the glut helps.
- founder 3: Needs GPU-serving credibility not yet earned.

**#8 C-86 Memory Cost Escalation Index + EPA kit** (T0; 75.0 / 78.3 / 74.2)

- tech 4: Standard method; basis risk vs contract prices.
- capital 5: Pipeline, history, clause templates.
- ttr 3: 9-15 months; two legal teams per sale.
- U.S. mfg 3: Software/data.
- margin 4: 57-89%.
- moat 3: Sticky once in EPA clauses.
- competition 3: No memory EPA index found.
- regulatory 4: FAR allows index EPA; antitrust care.
- cycle 4: Two-sided: earns on the down-leg.
- founder 4: Software; the day job is the buyer persona.

**#9 C-26 Optane PMem salvage** (T0; 74.0 / 78.3 / 66.7)

- tech 5: TRL 9 parts; ipmctl checks scripted.
- capital 5: ~$1-3k test server + inventory.
- ttr 5: 2-6 months.
- U.S. mfg 3: Resale and test.
- margin 2: 20-35%; prices public on eBay.
- moat 1: None.
- competition 2: Many eBay sellers and ITADs.
- regulatory 4: Sanitize App Direct media.
- cycle 1: vSphere 8 EoGS 2027-10-11, then glut.
- founder 5: Scripting plus e-commerce.

**#10 C-74 Fleet Memory-Reclaim Autopilot (on-prem)** (T1; 74.0 / 74.2 / 73.3)

- tech 4: TMO saves 20-32%; SLO risk is real.
- capital 4: ~$45-60k kernel contractor: low T1.
- ttr 4: ~12 months to a paid pilot.
- U.S. mfg 3: Software.
- margin 5: 75-85% per-node SaaS.
- moat 2: Tuning of free kernel features.
- competition 3: No commercial on-prem rival; DIY is.
- regulatory 5: Negligible.
- cycle 3: Deferred-DRAM value ~$154k to ~$61k.
- founder 3: Needs kernel help; one outage ends it.

**#11 C-85 DIMM Health Subscription + spares** (T0; 74.0 / 77.5 / 71.7)

- tech 4: CE-to-UE prediction published; small fleets unproven.
- capital 5: Test servers + ~$7k spares pool.
- ttr 4: 6-12 months.
- U.S. mfg 3: U.S. burn-in plus software.
- margin 4: 59% now, 82% in a glut.
- moat 2: Spares logistics only.
- competition 2: Park Place ParkView bundles it.
- regulatory 4: Barred from federal deliverables.
- cycle 3: Margin up, demand down after ~2029.
- founder 4: Agent + console; 3PL swaps.

**#12 C-84 Embedded RAM-Diet Profiler** (T0; 73.0 / 75.0 / 69.2)

- tech 5: smem, cgroups, zram; proven.
- capital 5: Contractor paid from fees.
- ttr 4: ~12 months to first audits.
- U.S. mfg 3: Services.
- margin 4: 45-65%; contractor labor.
- moat 1: Engineers can do it free.
- competition 3: No direct product.
- regulatory 4: Medical re-validation friction.
- cycle 1: ~$2.5/unit saving at the glut.
- founder 2: Engineers rarely buy from non-engineers.

**#13 C-79 TB-RAM rental on recovered DDR4** (T1; 72.0 / 72.5 / 66.7)

- tech 5: Plain hosting on off-lease servers.
- capital 4: 10-box fleet $75-104k: low T1.
- ttr 5: 4-8 months.
- U.S. mfg 3: Services on recovered hardware.
- margin 3: ~47-53% before remote hands.
- moat 1: Commodity hosting.
- competition 2: Hetzner, OVH, PhoenixNAP, Vultr.
- regulatory 4: Hosting AUP only.
- cycle 2: A glut rent cut means 11-22% GM.
- founder 3: On-call clashes with the day job.

**#14 C-62 ProvenRAM graded recovered RDIMMs** (T0; 71.0 / 75.0 / 64.2)

- tech 5: Existing trade; free test tools.
- capital 5: $20-40k bench + first lot.
- ttr 5: 2-4 months.
- U.S. mfg 3: U.S. test and grading.
- margin 2: ~20% contribution.
- moat 1: SPD serial already public.
- competition 1: ServerMonkey, ITADs, Mobius, eBay.
- regulatory 3: Closed to DoD; counterfeit rules.
- cycle 1: 1-6% contribution in a glut.
- founder 4: Part-time, but ops work, not software.

**#15 C-48 On-prem MoE Box** (T1; 70.0 / 71.7 / 63.3)

- tech 5: Documented KTransformers configs.
- capital 4: ~$15.6k DRAM per box: low T1.
- ttr 4: 8-14 months; security reviews.
- U.S. mfg 3: U.S. bench assembly of imported parts.
- margin 2: 18-25% hardware.
- moat 1: Open configs; no moat.
- competition 2: Puget, Exxact, DGX Station, Mac Studio.
- regulatory 4: Low.
- cycle 4: A glut cheapens the box.
- founder 4: Closest hardware fit; support strains.

---

## 5. How the rankings shift across weightings

| Rank | Default | Capital-constrained | Moonshot |
|---|---|---|---|
| 1 | C-73 Memory FinOps Audit (cloud SaaS) (82.0, T0) | C-73 Memory FinOps Audit (cloud SaaS) (85.0, T0) | C-73 Memory FinOps Audit (cloud SaaS) (76.7, T0) |
| 2 | C-12 Battery-free F-RAM NVSRAM modules (80.0, T0) | C-12 Battery-free F-RAM NVSRAM modules (82.5, T0) | C-33 OpenRAM macro service (SkyWater S130) (76.7, T0) |
| 3 | C-33 OpenRAM macro service (SkyWater S130) (80.0, T0) | C-29 NVM-EOL Migration Finder (82.5, T0) | C-64 CleanBOM-5949 provenance verification (76.7, T0) |
| 4 | C-29 NVM-EOL Migration Finder (79.0, T0) | C-80 DRAM Cost & Allocation Intel (SMB OEMs) (82.5, T0) | C-29 NVM-EOL Migration Finder (75.8, T0) |
| 5 | C-80 DRAM Cost & Allocation Intel (SMB OEMs) (79.0, T0) | C-33 OpenRAM macro service (SkyWater S130) (82.5, T0) | C-80 DRAM Cost & Allocation Intel (SMB OEMs) (75.8, T0) |
| 6 | C-64 CleanBOM-5949 provenance verification (78.0, T0) | C-64 CleanBOM-5949 provenance verification (81.7, T0) | C-12 Battery-free F-RAM NVSRAM modules (75.0, T0) |
| 7 | C-75 KV-cache tier integration & tuning (76.0, T0) | C-26 Optane PMem salvage (78.3, T0) | C-86 Memory Cost Escalation Index + EPA kit (74.2, T0) |
| 8 | C-86 Memory Cost Escalation Index + EPA kit (75.0, T0) | C-75 KV-cache tier integration & tuning (78.3, T0) | C-74 Fleet Memory-Reclaim Autopilot (on-prem) (73.3, T1) |
| 9 | C-26 Optane PMem salvage (74.0, T0) | C-86 Memory Cost Escalation Index + EPA kit (78.3, T0) | C-75 KV-cache tier integration & tuning (71.7, T0) |
| 10 | C-74 Fleet Memory-Reclaim Autopilot (on-prem) (74.0, T1) | C-85 DIMM Health Subscription + spares (77.5, T0) | C-85 DIMM Health Subscription + spares (71.7, T0) |

**Biggest movers** (`research/phase3/rankings.md`). In the Driver column, "up" and "down" refer to the weighting that doubles those criteria.

| ID | Concept | Tier | Default → Cap-con → Moonshot | Shift | Driver |
|---|---|---|---|---|---|
| C-37 | GSI APU vector-search appliance | T1 | #29 → #21 → #33 | 12 | capital 4/founder 3 up; margin 2/moat 1 down |
| C-45 | KV Pool Node appliance | T1 | #24 → #24 → #32 | 8 | margin 1/moat 1 down |
| C-91 | Authorized EOL DRAM die bank | T2 | #28 → #30 → #23 | 7 | moat 4 up; capital 2/founder 1 down |
| C-22 | TrustNVM ReRAM chiplet (S130) | T2 | #31 → #29 → #24 | 7 | margin 4/moat 3 up; capital 2 down |
| C-36 | Fab 25 long-life SRAM second source | T2 | #21 → #26 → #20 | 6 | founder 1/capital 2 down; margin 4/moat 3 up |
| C-49 | TB-class CXL node | T1 | #22 → #22 → #28 | 6 | margin 2/moat 1 down |
| C-32 | Si gain-cell eDRAM IP | T2 | #25 → #28 → #22 | 6 | margin 5 up; capital 2/founder 2 down |
| C-65 | Hi-rel DDR4 MCM design house | T2 | #30 → #31 → #25 | 6 | moat 3 up; founder 1 down |
| C-26 | Optane PMem salvage | T0 | #9 → #7 → #12 | 5 | capital 5/founder 5 up; margin 2/moat 1 down |
| C-74 | Fleet Memory-Reclaim Autopilot (on-prem) | T1 | #10 → #13 → #8 | 5 | capital 4/founder 3 down; margin 5 up |

**Why the rankings shift:**
- **What the weights reward.** Tech + capital + ttr + founder hold **55%** of the default weight, **62.5%** of capital-constrained and **45.8%** of moonshot. Moat + margin hold 20%, 16.7% and 33.3%. Software scores `tech` 5 by anchor definition, so T0 software starts every weighting with most of the points already won.
- **Capital-constrained lifts T0 resale and services.** C-26 rises #9→#7, C-62 #14→#11 and C-85 #11→#10. T2 concepts (capital 2, founder 1–2) fall: C-36 #21→#26, C-32 #25→#28. C-74 (low T1) drops from #10 to #13.
- **Moonshot has no moonshot to lift.** No concept has moat 5, and only C-91 has a 4. The highest moat + margin is 7 of 10 (C-01, C-06, C-22, C-32, C-36, C-64, C-72, C-74, C-86, C-91). So moonshot reshuffles mid-table: C-64 #6→#3, C-91 #28→#23, C-22 #31→#24. Low-margin resale falls: C-26 #9→#12, C-48 #15→#19.
- **T0 software still leads under moonshot.** C-73 is #1 under all three weightings: it scores 5 on six criteria, and its moat 1 and competition 1 cost only 15% of the weight. As a check [ESTIMATE: arithmetic on `models/scoring.py`], a commodity software profile (5/5/5/3, margin 1, moat 1, comp 1, reg 5, cycle 1, founder 5) scores **72.0** default (≈ #13). An ideal T2 device (tech 3, capital 2, ttr 1, then 5s except founder 1) scores **67.0** (≈ #17). The device wins only under moonshot (72.5 vs 63.3), and the real T2 survivors have moats of 2–4.
- **Stable core.** 12 concepts move at most one rank, and C-73, C-55, C-28, C-52 do not move at all. The top 6 is the same six concepts under every weighting, and only C-26, C-74, C-85 rotate through the bottom of the top 10.

---

## 6. Rubric blind spots

1. **No market-size or revenue-ceiling criterion.** C-12 ranks #2 with a "low-$100ks/yr" ceiling (`verify/batch_02.json`).
2. **No mission-fit criterion.** #1 C-73 sells into a cloud market where AWS's 2026 increases hit only Capacity Blocks for ML, and other EC2 prices were reported unchanged ([The Register, 2026-01-05](https://www.theregister.com/2026/01/05/aws_price_increase/)) [REPORTED]. The one mission-adjacent criterion, `usmfg`, barely discriminates: 30 of 40 concepts score 3, because software and U.S. assembly of imported die share that anchor. In the top 15 only C-33 scores above 3.
3. **Inverse capital + ttr + founder-fit make cheap software structurally dominant.** In the §5 arithmetic, a moatless, crowded, glut-killed software profile beats an ideal T2 device under the default weighting.
4. **Every T2+ concept ranks #21 or lower** under default (#26 or lower under capital-constrained). The one exception is moonshot, where C-36 reaches **#20**. The default top 20 is all T0/T1.
5. **The moat scale is compressed** (no 5s, one 4), so the moonshot weighting has little to amplify.
6. **Cycle weighs only 5%.** C-80 (cycle 1) still ranks #5, C-26 (cycle 1) #9 and C-62 (cycle 1) #14.
7. **`ttr` scores the first invoice, not the ramp.** A $5k audit at month 6 scores the same as a recurring contract at month 6.

**The scorers' own verdicts on the top 15** (`scores_raw/*.json` `one_line_view`; F founder, V vc, T veteran):

| # | ID | Verdict (exact quote) | Side/feature/lifestyle/SKU/gig/lead-gen/not-a-venture? |
|---|---|---|---|
| 1 | C-73 | F: "A consulting side gig, not the venture."<br>T: "it is not a memory business at all" | **yes** |
| 2 | C-12 | F: "a profitable side business, not a venture."<br>T: "good as a side SKU, not a venture" | **yes** |
| 3 | C-33 | V: "likely a <$0.5-1M ARR lifestyle business."<br>F: "a credible part-time wedge, not an endgame." | **yes** |
| 4 | C-29 | F: "a feature for C-80 or lead-gen for C-12, not a standalone business." | **yes** |
| 5 | C-80 | V: "lead-gen, not a company." | **yes** |
| 6 | C-64 | V: "it is a feature for Exiger or SiliconExpert unless it owns die-source data." | **yes** |
| 7 | C-75 | V: "a services gig with a closing window, not a venture." | **yes** |
| 8 | C-86 | V: "the ceiling is ~$0.3M ARR unless it wins that fight." | no (ceiling/ROI cap) |
| 9 | C-26 | V: "fine as a C-62 SKU, uninvestable on its own." | **yes** |
| 10 | C-74 | V: "one production incident from zero, and no moat." | no (ceiling/ROI cap) |
| 11 | C-85 | V: "weak customer ROI caps it." | no (ceiling/ROI cap) |
| 12 | C-84 | V: "a consulting gig with no recurring layer." | **yes** |
| 13 | C-79 | V: "a cash-flow side hustle, not a fundable company." | **yes** |
| 14 | C-62 | V: "a cash-flow side hustle, not a venture." | **yes** |
| 15 | C-48 | V: "a lifestyle business unless a support subscription attaches." | **yes** |

The flag column checks all three lenses' full verdicts. **12 of 15** carry such a verdict; the other 3 are capped by a ceiling or a customer-ROI objection instead.

**Supplementary: 5-year revenue ceiling. [ESTIMATE], NOT part of any weighted score.** Bands are year-5 ARR or annual revenue for this founder, base case.

| # | ID | Concept | 5-yr ceiling band [ESTIMATE] | Basis |
|---|---|---|---|---|
| 1 | C-73 | Memory FinOps Audit (cloud SaaS) | < $0.5M | ~$270/month ACV; $20k MRR needs ~74 customers; churn once savings are booked (card). |
| 2 | C-12 | Battery-free F-RAM NVSRAM modules | < $0.5M | "Low-$100ks/yr" (batch_02, all three lenses); one-time hardware sales. |
| 3 | C-33 | OpenRAM macro service (SkyWater S130) | < $0.5M (≤ $1M) | Card: "<$0.5-1M ARR" unless it grows into a broader open-PDK IP house. |
| 4 | C-29 | NVM-EOL Migration Finder | < $0.5M | A narrow NVM-migration slice; lead-gen per all three lenses. |
| 5 | C-80 | DRAM Cost & Allocation Intel (SMB OEMs) | < $0.5M, then ~0 | Card: ~$24k MRR (80 x $300) ≈ $0.29M ARR; churn at the 2028 turn. |
| 6 | C-64 | CleanBOM-5949 provenance verification | $0.5–2M | Card model (`research/phase2/C_notes.md`): 37 customers on $1.5–12k/month tiers = $1.34M ARR + $0.35M lab = $1.68M, cut by the safe harbor. |
| 7 | C-75 | KV-cache tier integration & tuning | < $0.5M | ~6–12 engagements/yr × $15–40k part-time; Tensormesh holds the recurring line. |
| 8 | C-86 | Memory Cost Escalation Index + EPA kit | < $0.5M (upside $2–10M) | Card: $0.3M ARR; upside only if it displaces TrendForce in contracts. |
| 9 | C-26 | Optane PMem salvage | < $0.5M, non-recurring | A two-year liquidation window to 2027-10-11; 20–35% margin. |
| 10 | C-74 | Fleet Memory-Reclaim Autopilot (on-prem) | $0.5–2M | $6–24k/yr per customer, so it needs ~50–100 customers; value per fleet falls 2.5x in a glut. |
| 11 | C-85 | DIMM Health Subscription + spares | $0.5–2M (low end) | Card: 25 × $21.6k = $0.54M ARR, but the fee is ~3.6x DIY cost. |
| 12 | C-84 | Embedded RAM-Diet Profiler | < $0.5M, non-recurring | One-off $5–20k audits; demand gone at glut prices. |
| 13 | C-79 | TB-RAM rental on recovered DDR4 | < $0.5M | $1,200/month per box with capital-limited growth (10 boxes ≈ $0.14M/yr). |
| 14 | C-62 | ProvenRAM graded recovered RDIMMs | < $0.5M contribution | ~$12k/month contribution (card model), falling to 1–6% in the glut. |
| 15 | C-48 | On-prem MoE Box | $0.5–2M revenue | 20–50 boxes/yr at ~$25–45k each; GP < $0.5M at 22% margin. |

**11 of 15 fall in the < $0.5M band, 4 in $0.5–2M, and none in $2–10M.** The only credible path above $2M is C-86 becoming the contract reference index, which means displacing TrendForce. The other path is bundling, which is the job of §7.

---

## 7. From concepts to ventures: the five deep dives

Rule (`selection.json`): each deep dive is anchored on a top-ranked concept and folds in the adjacent survivors that scorers said should be run as a SKU, feeder or feature of it. Ranks are default / capital-constrained / moonshot.

### 7.1 DD1 — Provenance & Recertified Memory (`provenance-recert`, T0)

| Role | ID | Concept | Tier | Ranks D/C/M | Why it is here (exact quote) |
|---|---|---|---|---|---|
| anchor | C-64 | CleanBOM-5949 provenance verification | T0 | 6/6/3 | V: "The best-shaped business in my batch (T0, ~70% GM, glut-proof, founder-fit)" |
| folded | C-62 | ProvenRAM graded recovered RDIMMs | T0 | 14/11/16 | T: "run it as a cash cow or a provenance-data feeder, not a venture." |
| folded | C-85 | DIMM Health Subscription + spares | T0 | 11/10/10 | F: "Sell it wholesale to TPMs or not at all."<br>selection link (not a scorer quote): same R2 ITAD supply and burn-in bench as C-62 |
| folded | C-26 | Optane PMem salvage | T0 | 9/7/12 | V: "fine as a C-62 SKU, uninvestable on its own."<br>audit b04: "This is effectively a SKU of C-62" |

**Bundle logic.** Recert (C-62, with C-26 as a SKU) is the fastest cash in the set (2–4 months). It also builds the module-to-die-source dataset without which, in the vc's words, C-64 is "a feature for Exiger or SiliconExpert." C-85 reuses the same supply as a subscription. C-64 (cycle 5) has to carry the bundle once recert falls to 1–6% contribution in the glut.

### 7.2 DD2 — Memory Lifecycle & Cost Intelligence for OEMs (`lifecycle-intel`, T0)

| Role | ID | Concept | Tier | Ranks D/C/M | Why it is here (exact quote) |
|---|---|---|---|---|---|
| anchor | C-80 | DRAM Cost & Allocation Intel (SMB OEMs) | T0 | 5/4/5 | T: "use it only as a free lead-gen front end." |
| folded | C-29 | NVM-EOL Migration Finder | T0 | 4/3/4 | V: "lead-gen for C-12/C-80, not a company." |
| folded | C-86 | Memory Cost Escalation Index + EPA kit | T0 | 8/9/7 | T: "its clauses persist through the glut" |
| folded | C-61 | DRAM Continuity Vault (LTB) | T1 | 16/16/13 | F: "The LTB-sizing software fits the founder"<br>fold the software only, not the vault |
| folded | C-72 | Legacy-DRAM buying co-op | T1 | 20/19/15 | F: "A free kill test, not a venture." |

**Bundle logic.** One buyer (procurement at U.S. SMB hardware OEMs) and one data pipeline. C-80 is the shortage-era funnel (cycle 1). C-29 and C-61's software are the EOL modules that survive a glut, and C-86 earns on both legs of the cycle. C-72 is three free supplier calls, not a business.

### 7.3 DD3 — Drop-in Non-Volatile Continuity Modules (`nv-continuity-modules`, T0)

| Role | ID | Concept | Tier | Ranks D/C/M | Why it is here (exact quote) |
|---|---|---|---|---|---|
| anchor | C-12 | Battery-free F-RAM NVSRAM modules | T0 | 2/2/6 | T: "watch the F-RAM /CE-latch timing trap." |
| folded | C-16 | Supercap-Killer MRAM PLP kit | T1 | 19/18/18 | F: "worth a cheap test, not the core of a venture." |

**Bundle logic.** Drop-in non-volatile continuity built on shipping NVM: F-RAM replaces battery-backed SRAM, and MRAM replaces PLP supercaps. Same competence (boards plus controller validation), same lifecycle axis. C-29 (DD2) is named as lead-gen for C-12, so DD2 and DD3 share a funnel.

### 7.4 DD4 — Memory Efficiency for On-Prem & Self-Hosted Fleets (`memory-efficiency`, T0/T1)

| Role | ID | Concept | Tier | Ranks D/C/M | Why it is here (exact quote) |
|---|---|---|---|---|---|
| anchor | C-73 | Memory FinOps Audit (cloud SaaS) | T0 | 1/1/1 | T: "it is not a memory business at all, since the DRAM shortage never reached EC2 list prices" |
| folded | C-74 | Fleet Memory-Reclaim Autopilot (on-prem) | T1 | 10/13/8 | F: "The best software economics in my chunk (80% GM, low T1)" |
| folded | C-75 | KV-cache tier integration & tuning | T0 | 7/8/9 | T: "a consulting gig with a ~12-month half-life." |

**Bundle logic.** One "GB of DRAM not bought" ledger, sold three ways. C-74 answers the veteran's objection to C-73, because on-prem buyers pay for DRAM directly (~$14–16/GB DDR5 contract per the card). C-75 is the services entry into the KV-cache workload.

### 7.5 DD5 — U.S. Open Memory IP (compiler service -> gain-cell & ReRAM macros) (`open-memory-ip`, T0 wedge -> T2 product)

| Role | ID | Concept | Tier | Ranks D/C/M | Why it is here (exact quote) |
|---|---|---|---|---|---|
| anchor | C-33 | OpenRAM macro service (SkyWater S130) | T0 | 3/5/2 | F: "a credible part-time wedge, not an endgame."<br>card: "unless it becomes a broader open-PDK IP/characterization house (gf180mcu, IHP, gain-cell IP)" |
| folded | C-32 | Si gain-cell eDRAM IP | T2 | 25/28/22 | T: "Better engineering than C-01 (zero masks, no contamination fight)" |
| folded | C-22 | TrustNVM ReRAM chiplet (S130) | T2 | 31/29/24 | F: "The cleanest U.S.-made device path in the set" |

**Bundle logic.** A wedge that leads to a product. The S130 macro service earns revenue and tapeout credibility, and the same PDK hosts a zero-mask Si gain cell (C-32) and Weebit's qualified ReRAM (C-22). The T2 stage is exercised only on wedge traction and a clean FTO read. The same scorers warn that "RAAAM already owns the commercial Si gain-cell seat" (T) and "a non-exclusive license buys no moat" (V).

### 7.6 Coverage proof: every concept in the top 10 under any weighting is in a deep dive

| ID | Concept | Top-10 under | Ranks D/C/M | Deep dive |
|---|---|---|---|---|
| C-73 | Memory FinOps Audit (cloud SaaS) | default, cap-con, moonshot | 1/1/1 | DD4 |
| C-12 | Battery-free F-RAM NVSRAM modules | default, cap-con, moonshot | 2/2/6 | DD3 |
| C-33 | OpenRAM macro service (SkyWater S130) | default, cap-con, moonshot | 3/5/2 | DD5 |
| C-29 | NVM-EOL Migration Finder | default, cap-con, moonshot | 4/3/4 | DD2 |
| C-80 | DRAM Cost & Allocation Intel (SMB OEMs) | default, cap-con, moonshot | 5/4/5 | DD2 |
| C-64 | CleanBOM-5949 provenance verification | default, cap-con, moonshot | 6/6/3 | DD1 |
| C-75 | KV-cache tier integration & tuning | default, cap-con, moonshot | 7/8/9 | DD4 |
| C-86 | Memory Cost Escalation Index + EPA kit | default, cap-con, moonshot | 8/9/7 | DD2 |
| C-26 | Optane PMem salvage | default, cap-con | 9/7/12 | DD1 |
| C-74 | Fleet Memory-Reclaim Autopilot (on-prem) | default, moonshot | 10/13/8 | DD4 |
| C-85 | DIMM Health Subscription + spares | cap-con, moonshot | 11/10/10 | DD1 |

**11 of 11 are bundled.**

`selection.json` words the rule as "top 10 under all three weightings". The check above uses the union of the three top-10 lists, which is stricter.

### 7.7 Constraint proof (≥ 1 T0/T1 and ≥ 1 T2+)
- **T0/T1:** DD1–DD4.
- **T2+:** C-32 and C-22, the product stage of DD5 (both T2 in `concepts_master.json`). **This is the weakest part of the selection.** They rank #25/#28/#22 and #31/#29/#24, and they are in because they share a T0 wedge (C-33, on the same SkyWater S130 PDK) that the founder can start part-time. The best T2 concept, C-36 (#21/#26/#20), was left out: its founder-fit is 1, and Infineon is the anchor customer of the very fab it would use. The T2 slot is an option inside DD5, not a recommendation.

### 7.8 Why NOT the other 14 Phase-3 survivors (alive and parked at the end of Phase 3)

| ID | Concept | Tier | Ranks D/C/M | Why not |
|---|---|---|---|---|
| C-84 | Embedded RAM-Diet Profiler | T0 | 12/12/11 | One-off audits engineers can do free; ~$2.5/unit saving at the glut; founder-fit 2. |
| C-79 | TB-RAM rental on recovered DDR4 | T1 | 13/14/14 | Commodity hosting vs Hetzner/OVH on peak-priced DDR4; on-call clashes with the day job. |
| C-48 | On-prem MoE Box | T1 | 15/15/19 | 18–25%-margin white-box reseller; Puget, Exxact and DGX Station can copy it; no moat. |
| C-18 | NewSpace MRAM rad-data & upscreen | T1 | 17/17/21 | Teledyne HiRel became Everspin's authorized screening channel ([Teledyne, 2026-09-02](https://www.teledyne-ade.com/en-us/news/Pages/Teledyne-HiRel-Semiconductors-and-Everspin-Technologies-Partner-to-Accelerate-MRAM-Adoption-in-Aerospace-and-Defense-Applic.aspx)); NASA data is free. |
| C-13 | Emerging-memory test & qual lab | T1 | 18/20/17 | Value rests on a reliability-physicist hire; 10–30 U.S. customers can rent university testers. |
| C-36 | Fab 25 long-life SRAM second source | T2 | 21/26/20 | Infineon anchors the same Fab 25; founder-fit 1; a $5–15M fight over a shrinking pie. |
| C-49 | TB-class CXL node | T1 | 22/22/28 | Below ~6 TB/socket CXL loses on $/TB; Dell, HPE, Supermicro and Penguin sell the box. |
| C-92 | AS6171 counterfeit-detection lab | T1 | 23/23/26 | SMT Corp and Micross are already accredited nearby; ~$650k; underwater below 36 lots/month. |
| C-45 | KV Pool Node appliance | T1 | 24/24/32 | Penguin's MemoryAI KV server (2026-03-16) already is this box; 10–20% margin. |
| C-67 | Rugged CAMM2/SODIMM at U.S. EMS | T1 | 26/25/29 | Innodisk, Virtium, SMART and ATP fight for scarce die at 20–35% margin. |
| C-55 | Analog CIM edge module | T1 | 27/27/27 | Mythic and EnCharge sell their own M.2 cards; analog drift; no defense BD. |
| C-91 | Authorized EOL DRAM die bank | T2 | 28/30/23 | Rochester has >10B banked die and 70+ OCM authorizations; first sale in year 3+. |
| C-37 | GSI APU vector-search appliance | T1 | 29/21/33 | A thin VAR on a ~$25M/yr vendor that already sells the same servers and plugin. |
| C-65 | Hi-rel DDR4 MCM design house | T2 | 30/31/25 | Teledyne e2v has shipped this x72 DDR4 MCM since 2020; $2–4M to undercut it. |

C-84, C-79 and C-48 outrank some bundled concepts. Bundles fold by adjacency, and these three have no anchor to fold into.

---

## 8. What Phase 4 must answer for each deep dive

| DD | Single biggest open question | Why it is the crux | Cheapest test |
|---|---|---|---|
| DD1 | **Does the proposed §5949 FAR rule's self-certification safe harbor leave anyone willing to pay for die-source verification, and can an SPD scan prove die source at all?** | Proposed 2026-02-17, effective 2027-12-23, no final rule yet ([GovInfo FR 2026-03065](https://www.govinfo.gov/content/pkg/FR-2026-02-17/html/2026-03065.htm)). A "reasonable inquiry" needs no third-party audit ([Crowell, 2026-02](https://www.crowell.com/en/insights/client-alerts/section-5949-proposed-rule-puts-the-far-councils-chips-on-the-table)) [REPORTED]. The veteran adds that "SPD die bytes are assembler-written." | Ten paid-pilot asks to OEM/ODM and module makers; X-ray/decap 20 modules against their SPD bytes |
| DD2 | **Will any line survive the 2028 turn? Will a buyer and a seller both sign an EPA clause that cites a non-TrendForce memory index?** | C-80 scores cycle 1, and C-86 caps at ~$0.3M ARR unless it becomes the reference. Federal use goes through DLAD 16.203-4's BLS-first rule ([acquisition.gov](https://www.acquisition.gov/index%2ephp/dlad/subpart-16.2-%E2%80%93-fixed%E2%80%93price-contracts)). C-72 hinges on Winbond or Nanya signing a pooled LTA (`batch_10`). | Have three integrator/EMS pairs redline a draft clause; make C-72's three supplier calls |
| DD3 | **Is the battery-backed SRAM installed base big enough to clear ~$0.5M/yr against free adapters, and does an F-RAM card pass Fanuc controller validation?** | Scorers cap C-12 at "low $100ks/yr" and C-16 below ~$1M/yr, and warn of the "/CE-latch timing trap." Fanuc SRAM cards are "hard to get" ([Memex](https://memex.ca/?p=596)). Everspin and the SSD-controller vendors already own the PLP decision ([Blocks & Files, 2026-10-05](https://www.blocksandfiles.com/flash/2026/10/05/ibm-using-everspin-mram-in-5th-gen-flashcore-modules/5300966)). | One PCMCIA prototype on a borrowed 0i/16i controller; a 20-shop MRO price survey |
| DD4 | **Will on-prem DDR5 operators pay a per-node fee to a part-time vendor whose agent tunes swap on production nodes, when the features are free and one OOM incident ends the account?** | The cloud has no shortage tailwind, so the memory-specific buyer is on-prem. Hetzner raised prices up to 37% citing RAM ([heise, 2026-02](https://heise.de/-11185981)). TMO saves 20–32% ([ASPLOS 2022](https://par.nsf.gov/servlets/purl/10332477)). But DDR4 fleets value the reclaim at only $40–59k (`batch_11`: ~10 TB freed on a 200-server reference fleet at $3.9–5.8/GB used DDR4, [amcompute](https://www.amcompute.com/appraisals/ddr4-64gb-rdimm)), and Tensormesh owns the KV recurring line ([SiliconANGLE, 2026-05-27](https://siliconangle.com/2026/05/27/tensormesh-taps-nvidia-amd-coreweave-funding-fix-llm-memory-problems/)). | A two-week volunteer-host SLO test, then three paid 60-day pilot asks |
| DD5 | **Will tapeout teams pay for characterized sky130 macros that ChipFoundry, Cadence or UCSC could bundle free, and is there an FTO-clear path from that wedge to a gain-cell or ReRAM product?** | Only 1–4 KB macros exist ([VLSIDA](https://github.com/VLSIDA/sky130_sram_macros)), and willingness to pay is STILL-UNVERIFIED (`batch_05`). RAAAM holds the Si gain-cell seat with GF ([Silicon Saxony, 2026](https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/)), and Weebit's S130 license is non-exclusive ([Weebit](https://www.weebit-nano.com/products/embedded-reram-ip/weebit-reram-nvm-in-skywater-130nm-cmos/)). | Pre-sell a 16 KB characterized macro to five shuttle teams; a patent-landscape read on RAAAM |

---

## Appendix: validation and input inconsistencies

A standalone Python check (a scratch script, not part of the repo, run after this file was written) confirms:
- all 40 `scores.csv` ids appear as §4 rows (40/40), and all 67 ids `KILLED` at the end of Phase 3 appear as §2 rows (67/67: 58 kill-pass + 9 `SCORE<55`);
- the 17 deep-dive ids match `selection.json` and the `deep_dive` tags, every id in any top 10 is bundled, and the 14 parked survivors are in §7.8;
- every scorer quote is an exact substring of that scorer's `one_line_view` (asserted at build time);
- re-running `models/scoring.py` into a scratch directory reproduces `scores.csv` and `rankings.md` byte for byte (exit 0).

**Input inconsistencies (none changes a kill or a rank):**
1. **Two price decks.** Kill reasons use $15.99 / $6.40 / $1.64 per GB (the pre-Phase-1b deck); `device_cost_output.md` and some `*_why` notes use the canonical post-Phase-1b deck $20.37 / $8.15 / $1.48 (`models/dram_cost_stack.py` `ddr5_reference()`). The list of concepts that cannot beat the glut is the same on both (device model §5 re-runs every verdict on both decks), so no kill changes. **Canonical deck for all later phases: $1.48 cost / $20.37 contract / $8.15 glut / $2.04 severe.**
2. **C-22 tier.** `device_cost_output.md` said T1; `concepts_master.json` and `scores.csv` say T2. C-32 (T2 everywhere) meets the T2+ constraint regardless. *Resolved: the current `device_cost_output.md` (re-run in Phase 7) shows C-22 as T2.*
3. **Rule labels.** `device_cost_output.md` called C-11, C-41 and C-42 'Rule-1 UNSUPPORTED'; their primary kill rules are R3, QB-INCOMPLETE and R4. *Resolved: the current `device_cost_output.md` flags only C-11, whose primary kill rule is R3.*
4. **'Every T2+ ranks ≥ #21'** holds under default and capital-constrained, but under moonshot C-36 is #20.
5. **Coverage wording.** `selection.json` said 'top 10 under all three weightings'; the property holds for the union (11 ids). *Resolved by the orchestrator: `selection.json` now states the union rule.*
6. **Lower median.** With three scorers it is the plain median.
7. **Pronouns.** Several `*_why` texts called the founder 'he'. *Resolved by the orchestrator: all scorer files, `scores.csv` and `concepts_master.json` now use they/them; `scores.csv` was regenerated (scores unchanged).*

## 9. Addendum — Round 2 selection (added after the Phase 5 red team)

The round-1 red team (`05_REDTEAM.md`) killed DD1, DD3 and DD4 and downgraded DD2 and DD5 to side lines; **0 of 127 objections were refuted**. That left no PRIMARY-grade venture and no MOONSHOT candidate, and DD5's T2 legs (C-32, C-22) were killed. Rather than pick from a pool the red team had already gutted, a **second deep-dive + red-team round** was run on the strongest scored survivors not selected in round 1, chosen for the two empty roles (`research/phase3/selection.json` → `round2`):

| Round-2 deep dive | Anchor (+ folded) | Tier | Ranks (default / cap / moon) | Role candidate | Why |
|---|---|---|---|---|---|
| DD6 Private MoE Inference Appliance (DRAM instead of HBM) | C-48 | T1 | #15 / #15 / #19 | PRIMARY | Highest founder-fit hardware survivor (founder 4, cycle 4, TTR 10 mo); the only concept that *benefits* from a DRAM glut; uses DRAM to do HBM's job for LLM inference |
| DD7 Authorized-Aftermarket Legacy DRAM Die Bank (+ hi-rel MCMs) | C-91 (+ C-65) | T2 | #28 / #30 / #23 (C-65: #30 / #31 / #25) | MOONSHOT | Highest ceiling among survivors (Rochester-scale model), moat 4 (DFARS authorized-aftermarket status), glut-proof lifecycle demand; strongest surviving T2+ path |

Both go through the same Phase 4 pipeline (research+model → write → verify) and the same four-persona Phase 5 red team as round 1.
