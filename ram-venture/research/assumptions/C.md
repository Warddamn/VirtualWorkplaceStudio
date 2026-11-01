# Assumptions: agent C (Phase 2, Branch C: U.S. manufacturing and supply chain)

Format: `- [C] <assumption> — basis: <why / source>`. The numbers feed the estimate script reproduced in `research/phase2/C_notes.md` Appendix A (scratch copy: `scratchpad/c_estimates.py`, exits 0).

## Research-environment limits (these set the confidence of everything below)
- [C] No fact in Branch C is [VERIFIED] from a primary page opened by C, except the two GitHub repositories (memtest86plus, stressapptest), which were cloned and read. — basis: the shared WebSearch budget (200 per turn) was exhausted before C started (3 queries refused), and WebFetch could not resolve www.acquisition.gov, www.alliancememory.com or www.powerchip.com (outside the session's allowed network domains). C stopped trying more hosts after those 3 failures, as instructed by the tool.
- [C] URLs that sibling agents logged from search snippets are reused as CROSS-REFERENCE with the sibling's title and date, and are flagged as not opened by C. — basis: CONVENTIONS.md source-logging rule.
- [C] Company facts from training knowledge (to about mid-2026) are tagged `[UNVERIFIED-training]` and carry no URL. Examples: Qimonda Richmond fab closure (2009), CXMT's use of Qimonda documents and patents (2019), PSMC's DRAM-foundry service, Etron/Zentel sourcing, Intelligent Memory's stacked DDR3, CAMM2 (JEDEC), Iron Mountain/ITRenew (2022), Champion Spark Plug v. Sanders (1947), BAA domestic-content thresholds, SPD byte offsets. — basis: no web access.

## Price anchors ($/GB; 8Gb = 1 GB)
- [C] DDR4 8Gb contract = $16/GB "now" — basis: TrendForce price page snapshot, June 2026 (cross-ref A2).
- [C] DDR4 8Gb spot = $21–44/GB — basis: TrendForce spot 2026-08-03 ($21.00) and DRAMeXchange via BuySellRAM 2026-08-31 ($44.37) (cross-ref p1-backend/B).
- [C] DDR3 4Gb contract = $10 per chip = $20/GB — basis: TrendForce price page snapshot, June 2026 (cross-ref A2).
- [C] DDR5 16Gb spot = $26.96/GB — basis: $53.92 average on 2026-08-31 (BuySellRAM, cross-ref).
- [C] Glut (A-05): DDR5 at 40% of now; legacy DDR4 at 45% of now ($7.2/GB contract), DDR3 at 45% of now — basis: ASSUMPTIONS A-05 says DDR4 falls less in % than DDR5's 60%. A separate "stress" case ($2/GB DDR4, $1/GB used RDIMM) mimics 2023 (DDR4 8Gb fixed price bottomed at $1.30, KED Global Sep 2023).
- [C] Used DDR4 RDIMM resale = $4–10/GB in 2026 (mid $6) — basis: ESTIMATE; p1-backend estimated $3–8/GB, but new DDR4 chips at $16–44/GB imply used modules could trade higher. **Kill-check: 90 days of eBay sold listings for 32GB PC4-2933Y / 64GB PC4-3200AA RDIMMs.**

## C-01 legacy DRAM fab
- [C] 25nm-class DDR4 density = 0.11 Gb/mm² (8Gb die ≈ 73 mm²) — basis: ESTIMATE, between 3x-nm DDR3 (~0.07) and 1z DDR4 (~0.18) used by p1-backend; Micron 1-alpha ≈ 0.3 Gb/mm² class [ESTIMATE], 1b ≈ 0.436 (Kurnal via KitGuru, cross-ref).
- [C] Capex $2.0–3.5B for 10–20k wafers/month at 300mm with refurbished tools; 5-year straight-line depreciation; cash opex $1,800/wafer; 80% yield; $0.60/GB package and test — basis: ESTIMATE anchored on Micron's >$2B Manassas expansion (HPCwire, cross-ref) for a smaller, existing-shell project.

## C-02 fabless legacy brand
- [C] Foundry DRAM wafer price $3,000 (25nm-class, 300mm); package and test $1.20/GB; brand longevity premium 15% over contract; NRE ≈ $15M (design $10M, masks and qualification $3M, test programs $2M) — basis: ESTIMATE; no PSMC price list could be opened.

## C-03 module assembly
- [C] DDR5 64GB RDIMM = 80 GB raw DRAM + $25 other parts + $12 U.S. assembly and test — basis: p1-backend §3.4 construction; prices from Counterpoint via EE Times Asia and ServNet (cross-ref).

## C-04 continuity vault
- [C] Fee 4% per year of consigned inventory value + $12k/yr software per OEM; space $60k/yr (3,000 sq ft); one nitrogen dry cabinet (~$5k, 7-year life) per $400k of DRAM; insurance 0.3% of inventory; staff $90k (≤8 OEMs) or $180k; audits and certifications $30k/yr — basis: ESTIMATE from general warehousing and component-storage norms; no vendor quotes.

## C-05 recovered RDIMM recert
- [C] Acquisition at 60% of resale price; eBay fees 13.25% vs B2B 3%; shipping $5 (eBay) vs $1.50 (B2B bulk); 6 min test labor at $28/hr loaded; $0.50 test-bed amortization; 3% failures written off; 2% returns — basis: p1-backend §6.6 inputs, adjusted for a B2B channel [ESTIMATE].
- [C] In a glut, acquisition prices reprice at the same ratio (optimistic); real inventory losses during the fall add ~3 points of margin loss — basis: judgment.
- [C] Starter kit $8–20k (bench SPD tester, 4–6 used DDR4 servers, ESD bench, thermal chamber) — basis: p1-backend §7.

## C-06 harvest
- [C] Rework cost $3.60 per chip (6 min labor at $28/hr + $0.30 materials + $0.50 X-ray share); harvested-die value 35% of new — basis: ESTIMATE.

## C-07 CleanBOM
- [C] Tiers: reseller $1.5k/month (25 customers), integrator $5k/month (10), OEM/ODM $12k/month (2); 6 lab samples per customer-year at $1,200 pass-through +30%; software and support cost 15% of ARR — basis: ESTIMATE; Section 889 compliance-tool pricing as analog [UNVERIFIED-training].
- [C] §5949 takes effect 2027-12-23 (417 days from 2026-11-01) — basis: p1-funding (enactment 2022-12-23 + 5 years) and XenoSpectrum "Dec 2027" (cross-ref). The FAR implementing rule's status and text are UNVERIFIED and are the single biggest swing factor for C-07.
- [C] DDR4 SPD bytes 350–351 and DDR5 SPD bytes 552–553 hold the DRAM-die manufacturer JEP106 ID — basis: [UNVERIFIED-training] JEDEC SPD annexes; memtest86+ source confirms the module-maker offsets (320–321 / 512–513) only.
- [C] GigaDevice-branded DDR4 is CXMT-fabbed — basis: [UNVERIFIED-training]; used only to argue that module/package labels cannot prove die origin.

## C-08 hi-rel MCM
- [C] 9 × 8Gb x8 KGD at contract +30% KGD premium; $120 U.S. substrate and assembly; $150 screening and data pack; ASP $800–3,000; NRE $1.5M — basis: ESTIMATE; hi-rel memory 10–100x commodity $/bit (p1-backend §4.3).

## C-09 stacked legacy module
- [C] 32GB DDR3 RDIMM = 72 × 4Gb in 36 DDPs; DDP packaging $1.20 each; $25 PCB/register/assembly; 25% markup — basis: ESTIMATE.

## C-10 rugged module
- [C] 16GB DDR5 SODIMM: industrial-temp component premium 5%; $15 PCB/PMIC/SPD + $25 U.S. EMS assembly, conformal coat and screen; commodity module = 1.10 × chip value; rugged premium 1.3–1.6× commodity — basis: ESTIMATE.

## C-12 KGD test house
- [C] Startup capex $750k (used ATE $250k, prober $150k, two probe cards $100k each, program development $150k); $600 per wafer probe revenue; $150 per wafer variable cost; $300k/yr fixed (2 engineers + facility) — basis: ESTIMATE from p1-backend §7 ranges.

## C-14 trusted SDRAM
- [C] 1T1C MIM cell 0.25 µm² at 65nm, array efficiency 55%, 200mm wafer $2,000 incl. extra capacitor masks, 60% yield, $15 package and test, NRE $10–20M, DoD DMSMS demand 10–100k units/yr at $40–60 — basis: ESTIMATE; no SkyWater quote.

## C-15 buying cooperative
- [C] Agency model fee 2.5% of pooled spend + $10k/yr membership; opex $150k + $2k per member; title model needs ~50 days of GMV as working capital — basis: ESTIMATE; distributor gross margins on memory 3–8% [UNVERIFIED-training].

## Judgment calls
- [C] Optane/PCM revival and CXL-DDR4 reuse are not re-carded in Branch C because A2-10, A2-11, B-01, B-09 and B-14 already cover them — basis: avoid cross-branch duplicates; kill reasons are recorded in C_notes.md §6.
- [C] "U.S.-made" premium is priced at zero for commodity memory today — basis: TAA treats Taiwan/Korea/Japan as designated countries; memory is excluded from Section 232 phase 1 (Korea Times 2026-09-15, cross-ref); the 100% memory-tariff threat was not implemented (TrendForce 2026-01-19, cross-ref).
- [C] DoD channel is closed to recovered DRAM (DFARS 252.246-7008 / FAR 52.211-5 new-material rule) unless a contracting officer approves — basis: [UNVERIFIED-training], consistent with p1-backend and p1-funding.
