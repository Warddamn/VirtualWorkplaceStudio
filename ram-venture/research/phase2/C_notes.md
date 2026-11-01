# Phase 2, Branch C: U.S. manufacturing and supply chain (research notes)

Agent: `C` · Written: 2026-11-01 · Cards: `research/phase2/C.json` (15 cards, C-01…C-15) · Sources: `research/sources/C.jsonl` (77 entries) · Assumptions: `research/assumptions/C.md` · Estimates: Appendix A (scratch copy `scratchpad/c_estimates.py`, exits 0)

> **How far to trust this file.**
> - **The web was closed to this agent.** My first three WebSearch calls (NDAA §5949 FAR rule; PSMC DRAM-foundry customers; Alliance Memory supply) came back "budget used up": the 200 searches per turn, shared by every agent, were gone. WebFetch could not resolve `www.acquisition.gov`, `www.alliancememory.com` or `www.powerchip.com` ("outside the session's allowed network domains"). As the tool instructed, I stopped trying more hosts after those three failures. The target of 40–80 searches was therefore impossible; I did zero successful web searches.
> - **What I did open:** two GitHub repositories by `git clone` (GitHub was reachable): `memtest86plus/memtest86plus` (HEAD 2026-10-28) and `stressapptest/stressapptest`. I read the source of memtest86+ to check a concrete claim behind C-07 (see §7.7). These are the only **[VERIFIED]** facts in this file.
> - **Everything else** is either (a) **[REPORTED]**: a URL a sibling agent logged from a search snippet, re-logged in `sources/C.jsonl` as a CROSS-REFERENCE with the sibling's title and date (no URL was retyped; they were copied programmatically), or (b) **[UNVERIFIED-training]**: my training knowledge (to about mid-2026), carried without a URL, or (c) **[ESTIMATE]**: computed in Appendix A.
> - I leaned on the Phase-1 notes `phase1/us_backend.md`, `us_fabs.md`, `funding_export.md` and `market.md`. Their authors also had no web access, so their company facts are mostly prior knowledge. Where I repeat them I keep their tags.
> - §9 is the verification queue. About 25 searches would settle the facts the ranking depends on.

---

## 1. Bottom line

**The U.S. gap in memory manufacturing is not where the mission premise puts it.** The U.S. can assemble modules (Kingston, Virtium, any EMS line), package small lots of hi-rel memory (Micross, Mercury, DDC, Integra, QP Technologies), decommission servers at scale (Iron Mountain/ITRenew, Sims, SK tes) and resell used memory. It cannot make DRAM wafers outside Micron, cannot package commodity DRAM at volume, and cannot get die as a small buyer. The value sits almost entirely in the die: assembly is **~0.6–1.0%** of a 2026 64GB RDIMM's cost (Appendix A, C-03), so "made/assembled in USA" is not a business by itself.

**What is arbitrageable for a founder with <$50k is information and trust, not silicon:**
1. **C-07 CleanBOM-5949** (T0, survives glut). NDAA §5949 bars federal agencies from buying products that contain CXMT/YMTC/SMIC chips from **2027-12-23**, 417 days from today ([XenoSpectrum, 2026-07](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/)) [REPORTED]. CXMT is now ~9.5% of DRAM revenue ([Herald/TrendForce, 2026-09-07](https://biz.heraldcorp.com/article/10866656)) [REPORTED], and Apple has lobbied to buy its DRAM ([TNW, 2026-06-27](https://thenextweb.com/news/apple-lobbying-us-approval-cxmt-blacklisted-memory-chips)) [REPORTED]. Verified non-Chinese memory is the one "U.S. policy creates a buyer" signal that a software founder can serve. **Biggest unknown:** whether the FAR implementing rule lets OEMs self-attest.
2. **C-05 ProvenRAM** (T0, partial glut survival). Graded, serialized recovered RDIMMs. It is the fastest path to revenue (2–4 months), clears a 17–32% contribution today and builds the test-record data that C-07 needs. It is a window business, not a venture, unless the provenance layer becomes the product.
3. **C-04 DRAM Continuity Vault** (T1, survives glut). Consignment last-time-buy storage plus LTB-sizing software for mid-size OEMs being orphaned by the DDR4 exits. Breakeven needs ~8–10 OEMs; ~70% GM at 25.

**Kills with the most information value:**
- **C-01 (trailing-node DRAM fab, licensed process): dead.** No U.S. fab can host a DRAM capacitor module. Micron Manassas is already making exactly the long-lifecycle DDR4/LPDDR4 product on a denser node, with CHIPS money ([HPCwire, 2026-05-22](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia)) [REPORTED]. A new fab would land around 2031 at $5.5–7.8/GB against a $7.2/GB A-05 glut price and a $1.30/GB 2023 trough.
- **C-03 ("Assembled in USA" module brand): dead.** Assembly is ~1% of value, TAA counts Taiwan and Korea as compliant, memory carries no Section 232 tariff ([Korea Times, 2026-09-15](https://www.koreatimes.co.kr/opinion/20260915/what-us-tariff-push-means-for-koreas-semiconductor-industry)) [REPORTED], die is allocated away from module makers ([TrendForce abstract, 2026-01-14](https://www.trendforce.com/research/download/RP260114IU)) [REPORTED], and Netlist's patents read on new DDR5 RDIMM brands [UNVERIFIED-training].
- **C-06 (die harvesting, Shenzhen model): dead in the U.S.** Server x4 die fit only RDIMMs. An intact tested 32GB module is worth ~2.7× its harvested chips. Reballed parts fail AS6171 inspection. In a glut, rework costs more ($3.60/chip) than the chip is worth ($2.50).
- Also dead or not founder-doable: C-11 (HBM adjacency: captive plants, no outside customer before 2029), C-12 (KGD test house: below breakeven volume), C-14 (trusted SDRAM on SkyWater: no buyer at $30–60/unit when COTS SDRAM is $2–5).

---

## 2. What exists, what is missing, what is arbitrageable (U.S., 2026-11)

| Layer | Exists in the U.S. | Missing | Arbitrageable by a small entrant? | Card |
|---|---|---|---|---|
| DRAM wafers | Micron Manassas Fab 6 (1-alpha DDR4/LP4 since 2026-05-22; $275M CHIPS) ([HPCwire](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia); [NIST](https://www.nist.gov/node/1869301)) [REPORTED]. Boise ID1 first wafers mid-2027. | Any non-Micron DRAM wafer capacity; any foundry with a DRAM capacitor module | **No.** T4, and Micron already serves the long-lifecycle niche | C-01, C-14 |
| Legacy DRAM IP/process | None owned by a U.S. entity except Micron | Licensable process know-how sits in Taiwan: Winbond (Qimonda-derived 46/38nm lineage, own 25/20nm), Nanya (Micron-licensed lineage, own 1B), PSMC (DRAM-foundry service). Qimonda's documents and patents went to CXMT via WiLAN/Polaris in 2019 [all UNVERIFIED-training] | No: patents without fab know-how are worthless, and the know-how holders are competitors | C-01, C-02 |
| Fabless legacy brands | Alliance Memory (Kirkland WA) [UNVERIFIED-training] | — | Theoretically (Etron/Zentel model), but wafer allocation goes to incumbents in a shortage | C-02 |
| Bare die / KGD | Micross (largest authorized die distributor; DRAM on its line card) ([flyer](https://micross.com/uploads/05827c98-1b61-4d4d-bb3c-04dc1b207e5a/Die_and_Wafer_Flyer_Rev_1_WEB.pdf)); SpecTek wafers ([SpecTek](https://micron.net/sales-support/customer-support/spectek-support)); Taiwanese KGD programs ([Winbond](https://winbond.com/hq/product/customized-memory-solution/kgd/), [ESMT](https://esmt.com.tw/en/Applications/Known-Good-Die), [Etron](https://etron.com/kgdm/)) [REPORTED] | Open KGD of current-node DDR4/DDR5 for small buyers (Samsung and SK hynix sell KGD only to strategic MCP customers [UNVERIFIED-training]) | Only legacy KGD, at wafer-lot MOQs of ~$3k–22k per wafer (p1-backend §4.2) | C-08, C-12, C-13 |
| Commodity DRAM packaging (FBGA) | Nobody at volume | The whole layer | No: needs die supply first | C-13 |
| Hi-rel memory packaging | Micross (FL/NC), Mercury (AZ), DDC (NY), Integra (KS), QP Technologies (CA) [UNVERIFIED-training] | Mid-volume JEDEC FBGA | Only as a design house on top of them (C-08), qualification-gated | C-08 |
| HBM stacking | Nothing until SK hynix West Lafayette (HBM4E from Q3 2029) ([Herald](https://mbiz.heraldcorp.com/article/10853891)) and Micron after ID2 (late 2028+) ([The Manufacturer](https://www.themanufacturer.com/articles/micron-technology-announces-200bn-investment-in-semiconductor-manufacturing-and-rd-in-idaho-new-york-and-virginia/)) [REPORTED] | Everything before 2029; all of it captive | No | C-11 |
| Module SMT | Kingston (Fountain Valley CA), Virtium (CA), any EMS [UNVERIFIED-training] | Not a gap | No: ~1% of value | C-03, C-10 |
| Decommissioning / ITAD | Iron Mountain (ITRenew, Sesame), Sims Lifecycle, SK tes, ERI, many R2 firms [UNVERIFIED-training] | Trusted, documented grading of the DRAM flow | **Yes**: test, grade, document, sell | C-05 |
| Counterfeit-avoidance and provenance | AS6081 distributors and AS6171 labs (dozens), Mobius Materials (VA) ([PR](https://www.prnewswire.com/news-releases/mobius-materials-raises-3m-to-combat-one-of-manufacturings-biggest-issues-amid-us-china-trade-tariffs-302643403.html)) [REPORTED] | **A memory-specific §5949 die-origin verification product** (none known) | **Yes** | C-07 |
| Long-lifecycle continuity | Rochester (MA), Micross; distributor bonded stock [UNVERIFIED-training] | Service sized for mid-size OEMs ($0.5–5M/yr of legacy DRAM) | **Yes**, at the low end the incumbents underserve | C-04, C-15 |

---

## 3. Key numbers (with sources)

| Quantity | Value | Date | Source / tag |
|---|---|---|---|
| DDR4 8Gb contract | **$16.00** (=$16/GB) | Jun 2026 | [TrendForce price page](https://www.trendforce.com/price) [REPORTED] |
| DDR3 4Gb contract | **$10.00** (=$20/GB) | Jun 2026 | same [REPORTED] |
| DDR3 4Gb spot | ~$3.19/Gb (~$25.5/GB) | early Jul 2026 | [Wccftech](https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/) [REPORTED] |
| DDR4 8Gb spot | $21.00 (TrendForce) to $44.37 (branded avg) | 2026-08-03 / 2026-08-31 | [TrendForce spot](https://www.trendforce.com/price_dram.html); [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/) [REPORTED] |
| DDR4 8Gb (Mobius) | $42.08 | 2026-07-28 | [Mobius](https://www.mobiusmaterials.com/whitepapers/dram-market-report-2026) [REPORTED] |
| DDR5 16Gb spot | $53.92 avg (~$27/GB) | 2026-08-31 | [BuySellRAM](https://www.buysellram.com/blog/ram-market-update/) [REPORTED] |
| DDR4 vs DDR5 | DDR4 dearer than DDR5 in some channels; DDR4 contract +24% over 3 months | Oct 2026 | [TechNews](https://finance.technews.tw/2026/10/13/the-shortage-of-memory-chips-may-continue-for-another-two-years/); [Guru3D/Barclays](https://www.guru3d.com/story/ddr4-memory-prices-now-also-rise-as-dram-supply-shortages-intensify-through-2028/) [REPORTED] |
| DDR4 trough | $1.30 (8Gb fixed) | Sep 2023 | [KED Global](https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013) [REPORTED] |
| 64GB RDIMM | $450 → >$900 contract; ~$2,064 street (DDR5) | 4Q25 → 1Q26; Aug 2026 | [EE Times Asia](https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/); [ServNet](https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026) [REPORTED] |
| Nanya 3Q26 | GM 85.7%, OPM 80%; LTAs repriced >60% from July | 2026-10-12 | [TrendForce News](https://www.trendforce.com/news/?p=65146) [REPORTED] |
| CXMT | ~9.5% DRAM revenue share (2Q26); ~320K → 420K wpm by 2027; $8.54B IPO | 2026 | [Herald](https://biz.heraldcorp.com/article/10866656); [Counterpoint](https://counterpointresearch.com/en/insights/cxmt-stock-market-big-three-memory-club); [Tom's Hardware](https://www.tomshardware.com/tech-industry/cxmt-closes-up-466-percent-in-shanghai-debut-with-no-hbm-project-in-its-ipo-prospectus) [REPORTED] |
| DDR4 buyer pain | Auto/industrial DDR4 buffers 31+ → 6–8 weeks; zero authorized stock of a Micron DDR4 part at Newark/Avnet/Mouser | May 2026 | [eeNews](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/); [Findchips](https://blog.findchips.com/memory-shortage-watch-ddr3l-ddr4-may-2026/) [REPORTED] |
| §5949 effective | 2027-12-23 (417 days) | — | p1-funding (enactment + 5 yr) [UNVERIFIED-H]; [XenoSpectrum](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/) "Dec 2027" [REPORTED] |
| Assembly share, 64GB DDR5 RDIMM | 0.55% (2026 spot) – 1.04% (2026 contract) – 1.33% (A-05 glut) | — | [ESTIMATE] Appendix A |
| Legacy fab cost | $5.45–7.79/GB (25nm-class, $2.0–3.5B capex) | — | [ESTIMATE] Appendix A |
| Recovered RDIMM contribution | $21–101 per 32GB (17–32%) now; $12–24 (13–28%) in the A-05 glut; ≤$6 in a 2023-like trough | — | [ESTIMATE] Appendix A |

---

## 4. Trailing-node DRAM: who could fab it, who owns the IP, who buys it

**Could DDR3/DDR4/LPDDR4 be fabbed on depreciated 25–40nm U.S. capacity?** No such capacity exists. U.S. trailing-edge foundries are 200mm logic, analog and power lines (SkyWater Bloomington and Austin Fab 25, GF Essex VT, TI, Microchip, Polar, X-FAB Lubbock, Tower) at 65nm and above (p1-fabs §1). None has a DRAM stack or trench capacitor module. IBM's deep-trench eDRAM (East Fishkill / GF 14HP) is the one historical U.S. DRAM-capacitor capability in a logic fab, and its 2026 status is unknown (p1-fabs; A3-05 cards it). The only U.S. DRAM front end is Micron (Manassas, Boise), and it is captive. **Trailing-node DRAM in the U.S. means Micron Manassas or nothing** (p1-fabs, concurring).

**Who owns usable legacy DRAM process know-how?** [UNVERIFIED-training throughout]
- **Winbond.** Licensed Qimonda's 46nm buried-wordline technology in 2008 before Qimonda's insolvency, then developed its own 38/25/20nm nodes (Taichung, Kaohsiung). It makes and sells specialty DRAM and KGD ([Winbond KGD](https://winbond.com/hq/product/customized-memory-solution/kgd/)) [REPORTED].
- **Nanya.** Its lineage is Micron-licensed (via Inotera), and it now runs its own 1B node. It is a pure DRAM maker with 80% operating margin in 3Q26 [REPORTED].
- **PSMC (Powerchip).** Elpida-era DRAM partner. Offers DRAM foundry service and its own DRAM. Customers reportedly include fabless DRAM brands (Etron, Zentel). I recall but **cannot confirm** 2026 reports that PSMC agreed to sell a 300mm fab (Tongluo) to Micron; if true, PSMC's DRAM-foundry capacity is shrinking. **Verify first** (§9).
- **Qimonda's estate.** Its patents went to Polaris Innovations (WiLAN, now Quarterhill) around 2014–15. In 2019 CXMT announced it had licensed them and obtained ~10,000 Qimonda technical documents. CXMT still needed about 8 years, ex-Elpida/Hynix engineers and state capital to reach 0.239 Gb/mm² DDR5 ([SemiWiki](https://semiwiki.com/forum/threads/chinas-cxmts-ddr5-reveals-3-year-technology-gap.23270/latest)) [REPORTED]. **Lesson: documents plus patents is not a process.**
- **Qimonda Richmond (Sandston VA).** A 300mm DRAM fab closed in early 2009 and its tools were sold. A U.S. DRAM fab has been stranded before, in a downturn.
- **Fabless legacy brands:** Alliance Memory (Kirkland WA), Etron, Zentel, ISSI (owned by Beijing Ingenic), Intelligent Memory, and GigaDevice (DDR4 made by CXMT). These buy foundry wafers or partner die.

**Who buys legacy DRAM in a shortage, and what they pay for:**

| Buyer | Pays for | Evidence |
|---|---|---|
| Industrial PC / automation (Advantech-class) | Continuity, avoiding EOL redesigns | Advantech tells customers to avoid Samsung DDR4 in new designs ([Advantech](https://www.advantech.com/en/resources/news/response-measures-to-samsung-ddr4-ic-eol-announcement)) [REPORTED] |
| Automotive, industrial | Allocation; buffers fell from 31+ to 6–8 weeks | [eeNews](https://www.eenewseurope.com/en/micron-ramps-us-made-ddr4-production-in-virginia/) [REPORTED] |
| Defense (DMSMS), avionics | 30–50-year sustainment; requalification costs millions | p1-backend §5.3 [UNVERIFIED-training] |
| Medical imaging, rail, grid protection | FDA and safety re-validation avoidance | p1-backend §5.3 [UNVERIFIED-training] |
| Networking/telecom, legacy servers | High-density DDR3 capacity | TrendForce: high-density DDR3 in acute shortage ([TrendForce, 2026-01-19](https://www.trendforce.com/news/2026/01/19/news-ddr4-reportedly-leads-legacy-memory-rally-with-q1-prices-up-to-50-ddr3-in-tight-supply/)) [REPORTED] |

The incumbents for "will still exist in 2040" are Micron Manassas (supply), Rochester and Micross (die banks, re-creation), Alliance and ISSI (fabless continuity), and Intelligent Memory (stacked legacy capacity). **A new entrant's opening is services for mid-size OEMs that these incumbents underserve: C-04 and C-15.**

---

## 5. Module assembly, die supply and the "U.S.-made" premium

- **Assembly share.** Across 2023-trough to 2026-spot prices, assembly and test are 0.55–7.6% of a 64GB RDIMM (Appendix A, C-03). In 2026 they are about 1%. A 10% "Assembled in USA" premium on that step moves the module price by under 0.2%.
- **Die terms** (p1-backend §4.2, [ESTIMATE]): MOQ of one wafer to one 25-wafer lot. Payment is NDA plus end-use statement plus prepayment or a letter of credit. Wafers are non-returnable. KGD sells at a 15–40% premium over packaged $/GB. One legacy lot is ~$75k; one DDR4/DDR5 lot is ~$550k. **SpecTek** is the only visible door to Micron silicon in wafer form, and one email answers whether it is open.
- **Premiums that exist** [UNVERIFIED-training; p1-funding §10]:
  - TAA: Taiwan, Korea and Japan are designated countries, so TAA gives no U.S. advantage.
  - BAA: a 20–30% civilian / 50% DoD evaluation factor, only on small buys under the TAA threshold. The non-COTS domestic-content threshold is 65% through 2028 and 75% from 2029.
  - FTC "Made in USA": an unqualified claim needs U.S. wafers. Only Manassas die qualify (C-13).
  - DFARS 252.246-7008: favors authorized sources and effectively bars recovered DRAM from DoD deliverables.
  - §5949: the only memory-specific preference, and it pays for **provenance, not U.S. origin**.
  - Section 232: memory is excluded from phase 1 ([Korea Times](https://www.koreatimes.co.kr/opinion/20260915/what-us-tariff-push-means-for-koreas-semiconductor-industry)) [REPORTED]. The 100% tariff threat was not implemented ([TrendForce](https://www.trendforce.com/news/2026/01/19/news-lutnick-reportedly-signals-100-memory-tariff-on-non-u-s-output-pressuring-samsung-and-sk-hynix/)) [REPORTED]. Taiwan's deal gives duty-free quota tied to U.S. capacity ([Manufacturing Dive](https://www.manufacturingdive.com/news/us-taiwan-ink-tariff-deal/809829/)) [REPORTED].
  - China-origin DRAM carries a +50% Section 301 duty ([Wove aggregator](https://tariffs.wove.com/us/tariff/8542.32.00.02/16mb-dram-chip/from/CN)) [REPORTED]. It does not reach CXMT die packaged or moduled outside China.
- **Export controls as protection.** BIS rules restrict tools and HBM going *to* China. They do not stop Chinese DRAM coming *in*. CXMT is not on the Entity List as of mid-2026 ([TrendForce, 2025-05-16](https://www.trendforce.com/news/2025/05/16/news-u-s-rumored-to-mull-adding-dram-giant-cxmt-and-more-chinese-tech-firms-to-entity-list)) [REPORTED], but it is on the DoD 1260H list ([HWBusters](https://hwbusters.com/news/cxmt-ymt-pentagons-list-a-memory-war/)) [REPORTED]. The BIS 50% affiliates rule ([Simpson Thacher](https://www.stblaw.com/about-us/publications/view/2025/10/17/simpson-thacher-attorneys-author-i-law360-i-article-on-bis-50-rule-for-entity-list-and-other-export-restrictive-lists)) [REPORTED] was reportedly suspended until about 2026-11-10 (p1-funding). **The protection a U.S. supplier gets is procurement-side (§5949, 1260H, the political pressure on Apple), not export-side.** That favors C-07.

---

## 6. Recovered and recertified DRAM: law, flows and economics

- **Legal frame** [UNVERIFIED-training]:
  - Buying used equipment, testing the modules and reselling them disclosed as used/refurbished is lawful (first sale).
  - Reconditioned goods may keep the original mark only if clearly labeled (Champion Spark Plug v. Sanders, 1947).
  - Remarking, or selling as new, is counterfeiting under 18 U.S.C. §2320, with enhanced penalties for military goods.
  - AS6081 (independent distributors) and AS6171 (test methods) govern any sale into aerospace and defense. DFARS 252.246-7008 and FAR 52.211-5 effectively close DoD to used parts.
  - R2v3 or e-Stewards certification is what ITAD suppliers expect from a downstream buyer.
  - DRAM is volatile, so there is no data-sanitization burden (NIST SP 800-88).
- **Flow.** p1-backend estimates ~4.6 EB/yr of DDR4 retiring globally, with ~0.65 EB/yr of U.S. supply reaching the open market (mid case), worth ~$1.9–5.2B at 2026 prices and ~$0.3–1.0B in a glut [ESTIMATE, p1-backend §6.4]. Hyperscalers increasingly reuse DDR4 internally behind CXL (Microsoft GreenSKU; Marvell Structera) [UNVERIFIED-training], which caps that flow. B-01 and B-14 card the CXL reuse device.
- **Economics** (Appendix A, C-05):

| Channel | 2026 mid ($6/GB used) | A-05 glut | 2023-like ($1/GB) |
|---|---|---|---|
| eBay contribution per 32GB | $35.8 (18.6%) | $11.5 (13.3%) | −$1.0 |
| B2B contribution per 32GB | $58.9 (30.7%) | $23.9 (27.6%) | $5.8 |

  The glut column assumes acquisition prices reprice instantly. In reality inventory held through the fall loses roughly 3 more points.
- **Test stack (VERIFIED by clone).** memtest86+ is GPLv2 and active: last commit 2026-10-28, "Add BIOS version and date (SMBIOS type 0) to USB report". It writes USB and serial reports with SPD vendor/SKU, ECC flag and per-test results, and its test 3 targets DDR5-era interface faults including PMIC droop. stressapptest is Google's Apache-2.0 memory-interface stress test. **Neither records the module serial number or the DRAM-die manufacturer.** That gap is where the founder's software adds value: a per-module ledger keyed to an SPD serial plus a laser-etched label.
- **Variant considered:** BGA-level repair of failed RDIMMs (replace one failing chip with a tested donor chip, retest, sell disclosed as repaired). This turns $5–20 scrap into a $200–300 module at 2026 prices [ESTIMATE]. It needs a $3–15k rework station and X-ray access. I folded it into C-05 as upside, not a separate card, because it is the same business and channel.

---

## 7. Evidence behind each card, and its cheapest kill experiment (<$10k, <30 days)

### 7.1 C-01 Legacy-DRAM fab (dead)
- Evidence: Micron Manassas is already the U.S. long-lifecycle DDR4/LP4 fab ([HPCwire](https://www.hpcwire.com/off-the-wire/micron-advances-made-in-america-memory-with-manufacturing-expansion-in-virginia); [TrendForce abstract RP260525NN](https://www.trendforce.com/research/download/RP260525NN): an internal shift, no return to consumer DDR4). The DDR4 shortage persists, and DDR4 is ~7% of Micron output ([I-Connect007](https://iconnect007.com/article/150148/microns-fab-6-starts-lpddr4-and-ddr4-production-but-ddr4-shortage-is-expected-to-persist/150145/flex)) [REPORTED].
- Model: a 25nm-class die is ~0.11 Gb/mm² against ~0.436 for 1b ([KitGuru/Kurnal](https://www.kitguru.net/channel/generaltech/joao-silva/new-dram-value%E2%80%91per%E2%80%91area-chart-draws-attention-amid-rising-memory-prices/)) [REPORTED]. Cost is $5.45–7.79/GB.
- Kill experiment: none needed. It fails rule 3 in spirit, and the timing lands it in the glut.

### 7.2 C-02 Fabless legacy brand
- Evidence: Etron and Winbond KGD programs; DDR4 exit timelines ([TrendForce 2025-07-09](https://www.trendforce.com/news/2025/07/09/news-ddr4-exit-timeline-unfolds-for-top-memory-makers-plans-for-samsung-sk-hynix-and-micron); [2025-09-02](https://www.trendforce.com/news/2025/09/02/news-samsung-sk-hynix-reportedly-delay-phase-out-to-2026-as-ddr4-becomes-unexpected-cash-cow/)); Micron cutting DDR4 and shifting demand to Taiwan ([TrendForce 2025-04-23](https://www.trendforce.com/news/2025/04/23/news-micron-reportedly-joins-samsung-in-cutting-ddr4-output-spurring-opportunities-for-taiwanese-suppliers/)) [REPORTED].
- Model: GM is 71% at 2026 contract and −135% at a 2023-like trough. The swing is the business.
- Kill experiment: ask PSMC and Winbond for DRAM-foundry wafer availability for a new customer in 2027. Expect a refusal or a 2028+ slot.

### 7.3 C-03 Assembled-in-USA modules (dead)
- Evidence and model: §5. Netlist jury verdicts ($303M vs Samsung 2023, $445M vs Micron 2024, $118M vs Samsung 2024) [UNVERIFIED-training; p1-backend §3.5] mean a new DDR5 RDIMM maker needs a freedom-to-operate check.
- Kill experiment: email SpecTek and two franchised distributors for a 2027 DDR5 16Gb component quote and allocation. No allocation confirms the kill.

### 7.4 C-04 Continuity Vault
- Evidence: §4 buyer table.
- Model: losses below ~8 OEMs, ~27% GM at 10, ~70% at 25 (Appendix A).
- Competitors: Rochester's die/wafer banking, Micross, distributor bonded stock, HTV (Germany) [UNVERIFIED-training].
- Kill experiment (~$2k, 3 weeks): interview 15 mid-size OEMs (industrial PC, rail, medical, test equipment) from the founder's manufacturing network and ask two questions. (1) Did you place a DDR3/DDR4 LTB in 2025–26? (2) Would you pay ~4%/yr to have someone else hold and manage it, with call-offs? Kill if fewer than 3 say yes with a number. Get Rochester's die-bank fee schedule as the price anchor.

### 7.5 C-05 ProvenRAM
- Evidence: §6. Comparables: BuySellRAM, Mobius, TechMikeNY, ServerMonkey.
- Kill experiment (~$3–5k, 3 weeks):
  1. Pull 90 days of eBay *sold* prices for 32GB PC4-2933Y and 64GB PC4-3200AA RDIMMs.
  2. Get quotes on two ITAD lots (Sesame/ITRenew and one regional R2 recycler).
  3. Buy 50 modules, test them on one used DDR4 server, and sell 25 on eBay and 25 to one B2B buyer.
  
  Kill if median resale is below $3/GB or measured contribution is below 12%.

### 7.6 C-06 Die harvesting (dead)
- Model: a harvested chip is worth $5.6–7.4 against $3.60 of rework now, and $2.5 against $3.60 in the glut. An intact module is worth $192 against ~$72 of harvested chips.
- Kill reason: geometry and law. No experiment needed.

### 7.7 C-07 CleanBOM-5949
- Evidence:
  - §5949 date and scope ([XenoSpectrum](https://xenospectrum.com/en/apple-china-memory-federal-procurement-ban-2027/)) [REPORTED].
  - Apple lobbying for and testing CXMT ([TNW](https://thenextweb.com/news/apple-lobbying-us-approval-cxmt-blacklisted-memory-chips); [Gigazine](https://gigazine.net/gsc_news/en/20260810-apple-tests-cxmt/)) [REPORTED].
  - Senate pressure ([Schumer, 2026-07-30](https://www.schumer.senate.gov/newsroom/press-releases/citing-core-national-security-and-economic-reasons-schumer-demands-apple-reject-chinese-military-linked-chips)) [REPORTED].
  - Die-ID by teardown is a commercial service ([TechInsights](https://www.techinsights.com/blog/spectek-pt040-56b-ddr5-dram-micron-1a-memory-floorplan-analysis)) [REPORTED].
- **[VERIFIED]** by reading memtest86+ source:
  - `system/jedec_id.h` lists `0x0A11 "CXMT"`, `0x091B "YMTC"`, `0x0648 "GigaDevice"` and `0x0235 "SpecTek"`.
  - `system/spd.c` reads the module-maker ID at DDR4 SPD bytes 320–321 and DDR5 bytes 512–513.
  - It does **not** read the DRAM-die manufacturer field (DDR4 bytes 350–351 and DDR5 bytes 552–553 per the JEDEC SPD annexes [UNVERIFIED-training]).
  - So an SPD-based CXMT flag is a small, concrete code extension. It is also **insufficient alone**: SPD is writable, and rebadged die (e.g., GigaDevice-branded DDR4 fabbed by CXMT [UNVERIFIED-training]) need a part-number cross-reference and sampled decap.
- Model: 37 customers give $1.34M ARR + $0.35M lab = $1.68M at ~72% GM.
- Kill experiment (~$1–3k, 4 weeks):
  1. Find the FAR case implementing §5949 and read its proposed rep/cert text. If the FAR accepts an unsupported offeror representation with no testing expectation, downgrade sharply.
  2. Interview 10 GSA MAS IT / SEWP resellers and 3 federal integrators. Kill if fewer than 3 would pay ≥$1k/month for a per-SKU attestation package.
  3. Build an SPD-scan prototype (fork memtest86+ or use Linux `decode-dimms`) and run it on 20 mixed modules.

### 7.8 C-08 Hi-rel MCM
- Evidence: Micross, KGD vendors, JESD49B.01, DARPA DV017.
- Model: 43–85% GM, NRE ~$1.5M, ~1,400 units to recover.
- Kill experiment: request quotes for MCM substrate and assembly from QP Technologies and Micross, and ask two primes' memory commodity managers about qualification timelines. Expect 24–36 months, which kills it for this founder.

### 7.9 C-09 Stacked legacy modules
- Evidence: TrendForce DDR3 shortage; price page.
- Model: ~$788 cost, ~$985 price, and the value falls ~75% in a stress glut.
- Kill experiment: check Intelligent Memory's catalog and pricing for 32GB DDR3 modules. If it already ships them, the card is a me-too.

### 7.10 C-10 Rugged / CAMM2 modules
- Evidence: Micron industrial LPDDR4 ([Micron](https://micron.net/products/memory/dram-components/lpddr4)); Manassas positioning; Advantech.
- Model: 20–35% GM now, 10–27% in the glut.
- Kill experiment: ask three rugged-computer makers (GMS, Crystal Group, a VPX house) whether they would add a fourth rugged-memory supplier and what they pay over commodity.

### 7.11 C-11 HBM adjacency (dead for founder)
- Evidence: SK hynix Indiana timing ([Evertiq](https://evertiq.com/news/2026-08-28-sk-hynix-breaks-ground-on-4-billion-packaging-facility-in-indiana); [Herald](https://mbiz.heraldcorp.com/article/10853891)); packaging-only ([Taipei Times](https://www.taipeitimes.com/News/biz/archives/2026/01/19/2003850817)); Micron 10-K; HBM is ~3× DDR5 wafer area per bit ([Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-ddr5-is-widening-with-every-generation)) [REPORTED].
- Correction to the mission premise (agreeing with p1-backend): **Amkor Peoria is logic 2.5D packaging, not memory capacity, with production around 2028** [UNVERIFIED-training].

### 7.12 C-12 KGD test house
- Evidence: KGD vendors already ship tested die.
- Model: breakeven at ~700 wafers/yr.
- Kill experiment: ask Micross and two MCM makers how many untested DRAM wafers per year they would send out. Expect fewer than 200.

### 7.13 C-13 All-domestic DRAM component
- Evidence: Manassas, CHIPS $275M ([NIST](https://www.nist.gov/node/1869301)), SpecTek, Micross.
- Kill experiment: one email to SpecTek and Micron's government/aerospace sales asking whether Manassas wafers or KGD are available to a U.S. packager, and on what MOQ.

### 7.14 C-14 Trusted SDRAM on SkyWater (dead on economics)
- Evidence: SkyWater Fab 25 ([BusinessWire](https://www.businesswire.com/news/home/20250226773415/en/SkyWater-to-Acquire-Infineons-Austin-Fab-and-Establish-Strategic-Partnership-to-Expand-U.S.-Foundry-Capacity-for-Foundational-Chips); [LaPedus](https://marklapedus.substack.com/p/skywater-acquires-infineons-200mm)); outside memory IP at SkyWater ([Weebit](https://www.weebit-nano.com/news/press-releases/weebit-nanos-reram-ip-now-fully-qualified-in-skywater-technologys-s130-process/)); a government trusted-fab memory precedent ([Sandia](https://www.sandia.gov/research/news/evolving-semiconductor-technology-for-national-security-applications/)); COTS SDRAM still made ([Winbond SDR KGD](https://www.winbond.com/hq/about-winbond/news-and-events/news/winbond-launchs-32bit-sdr-ddr-kgd-for-SiP-application.html)) [REPORTED].
- Model: ~$30/unit; $0.3–1.5M/yr gross profit against $10–20M NRE.

### 7.15 C-15 Buying cooperative
- Evidence: TrendForce allocation abstract; Nanya LTA repricing; Findchips; eeNews; Mobius as a funded aggregator ([YC](https://www.ycombinator.com/companies/mobius-materials)) [REPORTED].
- Model: 40 members give $60M pooled spend, ~$1.9M revenue (agency model). A title model needs $8–27M of working capital.
- Kill experiment: ask Winbond's and Nanya's U.S. sales offices and one franchised distributor whether they would honor a pooled LTA signed by a co-op on members' LCs. A "no" kills the agency model.

---

## 8. Post-mortems used

1. **Qimonda Richmond (2009)** [UNVERIFIED-training]. A modern U.S. 300mm DRAM fab was stranded in a glut, despite strong local incentives. Its tools went abroad. It shows that U.S. legacy DRAM capacity dies in downturns unless a captive owner (Micron) absorbs it.
2. **CXMT's Qimonda path (2016–2026)** [UNVERIFIED-training; density REPORTED]. Patents plus documents plus hired teams plus state capital (now an $8.5B IPO) produced a competitive DRAM maker, but it took about 8 years and tens of billions. There is no small-company version.
3. **Commodity module houses** (p1-backend §3.3). GM runs 5–15% in normal years, with losses on inventory write-downs in the 2019 and 2022–23 gluts. Netlist (low GM, litigation-driven) shows patents, not assembly, are where the money was. Crucial's 2025 exit shows even Micron would not keep a consumer module brand.
4. **Shenzhen recycled-chip trade.** It works on cheap labor, x8/x16 consumer die and weak enforcement. Every one of those conditions inverts in the U.S.
5. **Optane / 3D XPoint.** Already post-mortemed and carded dead in A2-10, A2-11 and B-09. Not re-carded here. The supply-chain angle is that Optane ran on a single captive fab (Lehi, sold to TI for ~$900M in 2021 with no XPoint capability retained, per A2/p1-fabs), and Intel wrote off the business on exit in 2022 [UNVERIFIED-training]. The lesson for Branch C: a single captive fab with one customer and no second source cannot survive the DRAM price swings it was meant to arbitrage.

---

## 9. Ideas considered but NOT carded

| Idea | Reason not carded |
|---|---|
| Optane/PCM revival (CXL tier or salvage) | Already carded dead in A2-10, A2-11, B-09; re-carding would duplicate |
| DDR4 second-life CXL expander / TrustedCXL | Branch B (B-01, B-14) |
| Buy a distressed U.S. fab (Akoustis 150mm NY, Wolfspeed Durham 150mm, Microchip Tempe 200mm) for DRAM | Merged into C-01: 150/200mm cannot make competitive DRAM, and it is still T3–T4 |
| Independent AS6081 memory broker for DoD shortages | Crowded (Fusion Worldwide, America II, Smith and dozens more [UNVERIFIED-training]), no moat, dies when the shortage ends; its provenance part lives in C-07 |
| DMEA Trusted Broker / Trusted Supplier accreditation as a standalone business | Accreditation is a moat, not a product; needs a facility clearance and a DoD sponsor; noted as a later step for C-07/C-08 |
| U.S. DDR5 PMIC/RCD/SPD-hub second source | U.S. suppliers already exist (MPS, TI, Renesas/IDT lineage, Rambus) [UNVERIFIED-training]; T2+ chip design; Montage (China) exposure is handled by C-07's BOM scan |
| U.S. DIMM PCB onshoring (TTM-class) | ~$8 of a $1,100–2,000 module; no buyer pays for it |
| FPGA/ASIC emulation of obsolete SDR/DDR1/DDR2 DRAM | Alliance, ISSI and Winbond still make these parts; protocol timing risk; DMEA ARMS and Rochester re-creation cover true orphans |
| LPDDR harvesting from phones and laptops | Same failure as C-06 (soldered, x16, AS6171, counterfeit law) |
| B2B graded-DRAM marketplace / ITAD offtake platform | A channel variant of C-05, and Mobius Materials already occupies the marketplace slot |
| DRAM upscreening / radiation-data service for NewSpace | Overlaps A2-03 (MRAM); for DRAM it is a feature of C-08 |
| U.S. HBM base-die foundry | TSMC makes HBM4E base dies; leading-edge logic, T4 |
| Section 232 tariff-quota arbitrage (import under Taiwan's U.S.-capacity quota) | Memory currently pays 0% under Section 232; a policy bet, not a business |
| Qimonda-patent assertion (licensing) play | Not a memory business; Polaris/Quarterhill already monetized the portfolio [UNVERIFIED-training] |
| SOCAMM/SOCAMM2 module maker for NVIDIA platforms | Memory makers supply SOCAMM directly to NVIDIA; no third-party slot [UNVERIFIED-training] |
| DRAM price newsletter / tracker | Branch D; Mobius and BuySellRAM already publish free reports as lead generation |

---

## 10. Cross-branch notes for the dedup reviewer

- C-05 (recert modules) and B-01/B-14 (CXL DDR4 reuse devices) share the recovered-DDR4 supply. They differ in product: a graded module versus a CXL device. C-05 could be B-14's supplier.
- C-07 (§5949 provenance) and B-14 (TrustedCXL "U.S.-provenance" expander) share the policy driver. C-07 is a service for all federal IT, not a device.
- C-04 (continuity vault) and A2-15 (NVM-EOL migration finder) are both EOL tools. A2-15 cross-references NVM replacements; C-04 stores and manages DRAM LTBs. They are distinct.
- C-14 (trusted SDRAM on SkyWater) and A3-05/A3-07 (IBM deep-trench eDRAM revival; long-lifecycle SRAM on Fab 25) share the "U.S. trailing-node memory for DoD continuity" thesis. The Phase-3 merge could absorb C-14 into A3-07.

---

## 11. Verification queue (about 25 searches; in priority order)

1. **FAR implementing rule for NDAA §5949**: case number, proposed/final status, rep-and-cert text, and whether it covers DIMMs/SSDs inside servers. (Decides C-07.)
2. **eBay sold-listing medians** for 32GB/64GB DDR4 RDIMMs (2026 vs 2024). (Decides C-05.)
3. **PSMC DRAM-foundry status in 2026**, including the recalled fab sale to Micron (Tongluo). (C-02, C-01.)
4. **SpecTek wafer/KGD terms** and whether Manassas silicon is available in wafer form. (C-13, C-12.)
5. **CXMT's JEP106 code usage in SPD** of CXMT-die modules, and GigaDevice DDR4 fab source. (C-07 method.)
6. **Rochester Electronics die-bank fees** and minimums; HTV long-term-storage pricing. (C-04.)
7. **Intelligent Memory catalog**: high-capacity DDR3/DDR4. (C-09.)
8. **Iron Mountain ALM / ITRenew volumes** and Sesame's DDR4 resale policy. (C-05.)
9. **Netlist 2025–26 CAFC/PTAB outcomes.** (C-03.)
10. **Amkor Peoria scope and timing**; SK hynix Indiana customer model. (C-11.)
11. **CAMM2/LPCAMM2 third-party module makers**; SOCAMM2 standardization. (C-10.)
12. **DMEA accredited supplier list** (is Micron accredited? Micross?). (C-13, C-14.)
13. **Alliance Memory DDR4 sourcing and longevity terms.** (C-02, C-04.)
14. **CXMT Entity-List status and the BIS affiliates-rule suspension end date (~2026-11-10).** (C-07.)

---

## Appendix A: estimate script (verbatim) and output

The script below is the one I ran: `python3 c_estimates.py` exits 0. It lives in my scratchpad because this agent owns only `C.json`, `C_notes.md` and its sources and assumptions files. Lift it to `models/` if a C card reaches Phase 4. Inputs are documented in `research/assumptions/C.md`.

```python
#!/usr/bin/env python3
"""Branch C (manufacturing & supply chain) scratch estimates for Phase 2 cards.

Every input is logged in research/assumptions/C.md. Price anchors are cited in
research/phase2/C_notes.md. Run: python3 c_estimates.py  (exits 0).
"""
import math

# ---------------------------------------------------------------- price anchors
# DDR4 8Gb (=1 GB) contract, TrendForce price page snapshot June 2026: $16/chip
DDR4_CONTRACT_NOW = 16.0      # $/GB
DDR4_SPOT_LOW, DDR4_SPOT_HIGH = 21.0, 44.37   # $/GB, TrendForce 2026-08-03 / BuySellRAM 2026-08-31
DDR3_CONTRACT_NOW = 10.0 / 0.5  # DDR3 4Gb (0.5 GB) $10 -> $20/GB, June 2026
DDR5_SPOT_NOW = 53.92 / 2       # DDR5 16Gb spot avg $53.92 -> $26.96/GB, 2026-08-31
DDR4_TROUGH_2023 = 1.30         # $/GB, KED Global Sep 2023
# Glut per ASSUMPTIONS A-05: DDR5 -60%; legacy DDR4 falls less in % (use -55%)
DDR5_GLUT = DDR5_SPOT_NOW * 0.40
DDR4_GLUT = DDR4_CONTRACT_NOW * 0.45
DDR4_STRESS = 2.0               # 2023-like stress case, not A-05


def hdr(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


def gross_die(wafer_mm, die_mm2):
    d = wafer_mm
    return int(math.pi * d * d / (4 * die_mm2) - math.pi * d / math.sqrt(2 * die_mm2))


# ------------------------------------------------- C-01 licensed legacy DRAM fab
hdr("C-01 legacy-DRAM fab in the U.S. (25nm-class DDR4 8Gb, 300mm)")
for capex_b, wpm in [(2.0, 20000), (3.5, 20000), (2.0, 10000)]:
    dep = capex_b * 1e9 / (wpm * 12 * 5)          # 5-yr straight line
    opex = 1800.0                                   # $/wafer materials+labor+utilities
    wafer_cost = dep + opex
    die_mm2 = 8 / 0.11                              # 8Gb at ~0.11 Gb/mm2 (25nm-class)
    gd = gross_die(300, die_mm2)
    good = gd * 0.80
    gb = good * 1.0
    cost_gb = wafer_cost / gb + 0.60               # + package/test $/GB
    print(f"capex ${capex_b:.1f}B @ {wpm} wpm: dep ${dep:,.0f}/wfr, wafer ${wafer_cost:,.0f}, "
          f"die {die_mm2:.0f} mm2, gross {gd}, good GB/wfr {gb:.0f}, cost ${cost_gb:.2f}/GB | "
          f"now ${DDR4_CONTRACT_NOW:.0f}, A-05 glut ${DDR4_GLUT:.1f}, 2023 trough ${DDR4_TROUGH_2023}")
# Compare: Micron 1-alpha ~0.3 Gb/mm2 class -> ~2.7x more bits/wafer than 25nm-class

# ------------------------------------------------- C-02 fabless legacy brand
hdr("C-02 fabless DDR4 brand on PSMC/Winbond foundry wafers")
foundry_wafer = 3000.0      # $/wafer 25nm-class foundry DRAM wafer, ESTIMATE
die_mm2 = 8 / 0.11
good_gb = gross_die(300, die_mm2) * 0.80
pkg_test = 1.20             # $/GB Asian OSAT package + DRAM ATE test, ESTIMATE
cost = foundry_wafer / good_gb + pkg_test
for label, asp in [("2026 contract", DDR4_CONTRACT_NOW), ("cycle-avg", 8.0), ("A-05 glut", DDR4_GLUT), ("stress", DDR4_STRESS)]:
    asp_brand = asp * 1.15   # longevity premium over commodity contract
    gm = (asp_brand - cost) / asp_brand
    print(f"{label:14s} ASP ${asp_brand:5.2f}/GB  cost ${cost:4.2f}/GB  GM {gm*100:6.1f}%")
nre = 10e6 + 3e6 + 2e6   # design team, masks+qual, test programs
print(f"NRE before first revenue ~${nre/1e6:.0f}M (design ~$10M, masks/qual ~$3M, test ~$2M)")

# ------------------------------------------------- C-03 assembly share
hdr("C-03 assembly share of a DDR5 64GB RDIMM (80 GB raw incl. ECC)")
other, asm = 25.0, 12.0
for label, p in [("2023 trough", 1.5), ("2026 contract low", 14.0), ("2026 spot", DDR5_SPOT_NOW), ("A-05 glut", DDR5_GLUT)]:
    dram = 80 * p
    tot = dram + other + asm
    print(f"{label:18s} DRAM ${dram:7.0f}  total ${tot:7.0f}  assembly share {asm/tot*100:5.2f}%")
# Even a 10% 'Assembled in USA' premium on assembly cost moves module price by <0.2%.

# ------------------------------------------------- C-04 continuity vault
hdr("C-04 DRAM Continuity Vault (consignment LTB storage + sizing SaaS)")
def vault(n_oem, inv_per_oem, fee_pct=0.04, saas=12000):
    inv = n_oem * inv_per_oem
    rev = inv * fee_pct + n_oem * saas
    cabinets = max(4, math.ceil(inv / 400000))      # one N2 cabinet per ~$400k of DRAM
    cogs = (60000                                    # space 3,000 sqft
            + cabinets * 5000 / 7                    # cabinet capex amortized 7 yr
            + inv * 0.003                            # insurance
            + (90000 if n_oem <= 8 else 180000)      # staff
            + 30000)                                 # audits / ISO / AS6081 surveillance
    return rev, cogs, inv
for n, per in [(3, 0.5e6), (10, 0.75e6), (25, 1.0e6)]:
    r, c, inv = vault(n, per)
    print(f"{n:3d} OEMs, inventory ${inv/1e6:5.1f}M: revenue ${r/1e3:6.0f}k cost ${c/1e3:5.0f}k GM {(r-c)/r*100:6.1f}%")

# ------------------------------------------------- C-05 recovered RDIMM recert
hdr("C-05 graded recovered DDR4 RDIMMs (per 32GB module)")
def recert(per_gb, channel="ebay", buy_frac=0.60):
    price = 32 * per_gb
    buy = price * buy_frac
    fees = price * (0.1325 if channel == "ebay" else 0.03)
    ship = 5.0 if channel == "ebay" else 1.5
    labor = 0.1 * 28.0           # 6 min @ $28/hr loaded
    bed = 0.50                   # test-server + tester amortization
    fail = buy * 0.03            # failures written off
    ret = price * 0.02           # returns / warranty
    contrib = price - buy - fees - ship - labor - bed - fail - ret
    return price, contrib
for label, p in [("2026 low $4/GB", 4.0), ("2026 mid $6/GB", 6.0), ("2026 high $10/GB", 10.0),
                 ("A-05 glut (mid x0.45)", 6.0 * 0.45), ("2023-like $1/GB", 1.0)]:
    for ch in ["ebay", "b2b"]:
        pr, cm = recert(p, ch)
        print(f"{label:24s} {ch:4s} price ${pr:6.0f} contribution ${cm:6.1f} ({cm/pr*100:5.1f}%)  "
              f"modules/mo for $8k: {8000/cm if cm>0 else float('inf'):7.0f}")
# working capital for a T0 start
inv0 = 20000
pr, cm = recert(6.0, "ebay")
mods = inv0 / (pr * 0.60)
print(f"$20k inventory buys {mods:.0f} modules @ $6/GB; two turns/month -> ${2*mods*cm:,.0f}/mo contribution")

# ------------------------------------------------- C-06 die harvest
hdr("C-06 die harvesting / rebuild (per DDR4 8Gb x4 chip)")
labor_min = 6.0
cost_chip = labor_min / 60 * 28 + 0.30 + 0.5       # labor + solder balls/flux + X-ray share
for label, p in [("2026 spot low", DDR4_SPOT_LOW), ("2026 contract", DDR4_CONTRACT_NOW), ("A-05 glut", DDR4_GLUT)]:
    harvested_value = p * 0.35                     # used-die discount, disclosed
    print(f"{label:14s} harvested-chip value ${harvested_value:5.2f} vs rework cost ${cost_chip:4.2f} "
          f"(but x4 die only re-usable on RDIMMs; intact module > sum of chips)")
# Intact 32GB RDIMM at $6/GB = $192 vs 36 chips x harvested value net of rework at A-05 glut:
print(f"intact 32GB RDIMM @ $6/GB = ${32*6:.0f}; 36 harvested chips net @ contract = ${36*(DDR4_CONTRACT_NOW*0.35-cost_chip):.0f} "
      f"before RCD/PCB/assembly of a new module and before 5-10% reball fallout")

# ------------------------------------------------- C-07 CleanBOM
hdr("C-07 Section 5949 CleanBOM subscription")
tiers = {"reseller": (1500 * 12, 25), "integrator": (5000 * 12, 10), "OEM/ODM": (12000 * 12, 2)}
arr = sum(p * n for p, n in tiers.values())
n_cust = sum(n for _, n in tiers.values())
lab_rev = n_cust * 6 * 1200 * 1.30   # 6 lab samples/yr each, $1,200 pass-through +30%
lab_cost = n_cust * 6 * 1200
sw_cost = arr * 0.15
rev = arr + lab_rev
gm = (rev - lab_cost - sw_cost) / rev
print(f"customers {n_cust}: ARR ${arr/1e6:.2f}M + lab ${lab_rev/1e6:.2f}M = ${rev/1e6:.2f}M, GM {gm*100:.0f}%")
# compliance clock
from datetime import date
print(f"days from 2026-11-01 to 5949 effective 2027-12-23: {(date(2027,12,23)-date(2026,11,1)).days}")

# ------------------------------------------------- C-08 hi-rel MCM
hdr("C-08 hi-rel DDR4 x72 8GB MCM (9 x 8Gb x8 KGD)")
kgd = 9 * DDR4_CONTRACT_NOW * 1.30      # KGD premium 30%
substrate_asm = 120.0                    # U.S. low-volume substrate + assembly (Micross/QP)
screen = 150.0                           # burn-in, temp cycling, X-ray, data pack
cost = kgd + substrate_asm + screen
for price in [800.0, 1500.0, 3000.0]:
    print(f"price ${price:,.0f}: unit cost ${cost:,.0f} GM {(price-cost)/price*100:5.1f}%")
nre = 1.5e6
print(f"NRE ~${nre/1e6:.1f}M; units to recover NRE at $1,500 ASP: {nre/(1500-cost):,.0f}")

# ------------------------------------------------- C-09 stacked legacy module
hdr("C-09 stacked-die 32GB DDR3 RDIMM (72 x 4Gb in 36 DDPs)")
for label, p in [("2026", DDR3_CONTRACT_NOW), ("A-05 glut", DDR3_CONTRACT_NOW * 0.45), ("stress", 3.0)]:
    die = 72 * 0.5 * p
    ddp = 36 * 1.20
    rest = 25.0
    cost = die + ddp + rest
    price = cost * 1.25
    print(f"{label:10s} die ${die:6.0f} DDP ${ddp:4.0f} cost ${cost:6.0f} price@25% markup ${price:6.0f}")

# ------------------------------------------------- C-10 rugged module
hdr("C-10 rugged 16GB DDR5 SODIMM (8 x 16Gb), conformal coat, -40..95C screen")
for label, p in [("2026 spot", DDR5_SPOT_NOW), ("A-05 glut", DDR5_GLUT)]:
    comp = 16 * p * 1.05      # industrial-temp component premium 5%
    rest = 15.0 + 25.0        # PCB/PMIC/SPD + assembly/coat/screen at U.S. EMS
    cost = comp + rest
    commodity = 16 * p * 1.10
    for prem in [1.30, 1.60]:
        price = commodity * prem
        print(f"{label:10s} premium {prem:.2f}x: price ${price:6.0f} cost ${cost:6.0f} GM {(price-cost)/price*100:5.1f}%")

# ------------------------------------------------- C-12 KGD test house
hdr("C-12 U.S. KGD wafer-probe house (legacy DRAM)")
capex = 250e3 + 150e3 + 2 * 100e3 + 150e3   # used ATE + prober + 2 probe cards + program dev
for wafers in [200, 500, 1500]:
    rev = wafers * 600.0
    var = wafers * 150.0
    fixed = 2 * 110e3 + 80e3
    print(f"{wafers:5d} wafers/yr: revenue ${rev/1e3:5.0f}k, contribution ${(rev-var-fixed)/1e3:6.0f}k, startup capex ${capex/1e3:.0f}k")

# ------------------------------------------------- C-14 trusted SDRAM on Fab 25
hdr("C-14 256Mb SDRAM, 1T1C MIM on 65nm 200mm (SkyWater Fab 25)")
cell_um2, eff = 0.25, 0.55
die = 256e6 * cell_um2 / eff / 1e6
gd = gross_die(200, die)
good = gd * 0.60
wafer = 2000.0
die_cost = wafer / good
pkg = 15.0
print(f"die {die:.0f} mm2, gross {gd}, good {good:.0f}, die ${die_cost:.1f}, +pkg/test ${pkg:.0f} -> ${die_cost+pkg:.0f}/unit "
      f"vs commercial 256Mb SDRAM ~$2-5 (Alliance/ISSI/Winbond, ESTIMATE)")
for units, asp in [(10000, 60), (50000, 60), (100000, 40)]:
    gp = units * (asp - die_cost - pkg)
    print(f"{units:7d} units @ ${asp}: gross profit ${gp/1e6:5.2f}M/yr vs NRE $10-20M")

# ------------------------------------------------- C-15 buying cooperative
hdr("C-15 legacy-DRAM buying cooperative (agency model)")
for members, spend in [(10, 1.0e6), (40, 1.5e6), (100, 2.0e6)]:
    gmv = members * spend
    rev = gmv * 0.025 + members * 10000
    cost = 150e3 + members * 2000
    print(f"{members:4d} members GMV ${gmv/1e6:6.1f}M: revenue ${rev/1e6:5.2f}M, opex ${cost/1e6:4.2f}M, "
          f"title-model working capital (50 days) ${gmv*50/365/1e6:5.1f}M")

print("\nOK")
```

Output (2026-11-01):

```text

==============================================================================
C-01 legacy-DRAM fab in the U.S. (25nm-class DDR4 8Gb, 300mm)
==============================================================================
capex $2.0B @ 20000 wpm: dep $1,667/wfr, wafer $3,467, die 73 mm2, gross 893, good GB/wfr 714, cost $5.45/GB | now $16, A-05 glut $7.2, 2023 trough $1.3
capex $3.5B @ 20000 wpm: dep $2,917/wfr, wafer $4,717, die 73 mm2, gross 893, good GB/wfr 714, cost $7.20/GB | now $16, A-05 glut $7.2, 2023 trough $1.3
capex $2.0B @ 10000 wpm: dep $3,333/wfr, wafer $5,133, die 73 mm2, gross 893, good GB/wfr 714, cost $7.79/GB | now $16, A-05 glut $7.2, 2023 trough $1.3

==============================================================================
C-02 fabless DDR4 brand on PSMC/Winbond foundry wafers
==============================================================================
2026 contract  ASP $18.40/GB  cost $5.40/GB  GM   70.7%
cycle-avg      ASP $ 9.20/GB  cost $5.40/GB  GM   41.3%
A-05 glut      ASP $ 8.28/GB  cost $5.40/GB  GM   34.8%
stress         ASP $ 2.30/GB  cost $5.40/GB  GM -134.8%
NRE before first revenue ~$15M (design ~$10M, masks/qual ~$3M, test ~$2M)

==============================================================================
C-03 assembly share of a DDR5 64GB RDIMM (80 GB raw incl. ECC)
==============================================================================
2023 trough        DRAM $    120  total $    157  assembly share  7.64%
2026 contract low  DRAM $   1120  total $   1157  assembly share  1.04%
2026 spot          DRAM $   2157  total $   2194  assembly share  0.55%
A-05 glut          DRAM $    863  total $    900  assembly share  1.33%

==============================================================================
C-04 DRAM Continuity Vault (consignment LTB storage + sizing SaaS)
==============================================================================
  3 OEMs, inventory $  1.5M: revenue $    96k cost $  187k GM  -95.2%
 10 OEMs, inventory $  7.5M: revenue $   420k cost $  306k GM   27.1%
 25 OEMs, inventory $ 25.0M: revenue $  1300k cost $  390k GM   70.0%

==============================================================================
C-05 graded recovered DDR4 RDIMMs (per 32GB module)
==============================================================================
2026 low $4/GB           ebay price $   128 contribution $  21.1 ( 16.5%)  modules/mo for $8k:     380
2026 low $4/GB           b2b  price $   128 contribution $  37.7 ( 29.4%)  modules/mo for $8k:     212
2026 mid $6/GB           ebay price $   192 contribution $  35.8 ( 18.6%)  modules/mo for $8k:     224
2026 mid $6/GB           b2b  price $   192 contribution $  58.9 ( 30.7%)  modules/mo for $8k:     136
2026 high $10/GB         ebay price $   320 contribution $  65.1 ( 20.4%)  modules/mo for $8k:     123
2026 high $10/GB         b2b  price $   320 contribution $ 101.4 ( 31.7%)  modules/mo for $8k:      79
A-05 glut (mid x0.45)    ebay price $    86 contribution $  11.5 ( 13.3%)  modules/mo for $8k:     694
A-05 glut (mid x0.45)    b2b  price $    86 contribution $  23.9 ( 27.6%)  modules/mo for $8k:     335
2023-like $1/GB          ebay price $    32 contribution $  -1.0 ( -3.0%)  modules/mo for $8k:     inf
2023-like $1/GB          b2b  price $    32 contribution $   5.8 ( 18.2%)  modules/mo for $8k:    1374
$20k inventory buys 174 modules @ $6/GB; two turns/month -> $12,418/mo contribution

==============================================================================
C-06 die harvesting / rebuild (per DDR4 8Gb x4 chip)
==============================================================================
2026 spot low  harvested-chip value $ 7.35 vs rework cost $3.60 (but x4 die only re-usable on RDIMMs; intact module > sum of chips)
2026 contract  harvested-chip value $ 5.60 vs rework cost $3.60 (but x4 die only re-usable on RDIMMs; intact module > sum of chips)
A-05 glut      harvested-chip value $ 2.52 vs rework cost $3.60 (but x4 die only re-usable on RDIMMs; intact module > sum of chips)
intact 32GB RDIMM @ $6/GB = $192; 36 harvested chips net @ contract = $72 before RCD/PCB/assembly of a new module and before 5-10% reball fallout

==============================================================================
C-07 Section 5949 CleanBOM subscription
==============================================================================
customers 37: ARR $1.34M + lab $0.35M = $1.68M, GM 72%
days from 2026-11-01 to 5949 effective 2027-12-23: 417

==============================================================================
C-08 hi-rel DDR4 x72 8GB MCM (9 x 8Gb x8 KGD)
==============================================================================
price $800: unit cost $457 GM  42.8%
price $1,500: unit cost $457 GM  69.5%
price $3,000: unit cost $457 GM  84.8%
NRE ~$1.5M; units to recover NRE at $1,500 ASP: 1,438

==============================================================================
C-09 stacked-die 32GB DDR3 RDIMM (72 x 4Gb in 36 DDPs)
==============================================================================
2026       die $   720 DDP $  43 cost $   788 price@25% markup $   985
A-05 glut  die $   324 DDP $  43 cost $   392 price@25% markup $   490
stress     die $   108 DDP $  43 cost $   176 price@25% markup $   220

==============================================================================
C-10 rugged 16GB DDR5 SODIMM (8 x 16Gb), conformal coat, -40..95C screen
==============================================================================
2026 spot  premium 1.30x: price $   617 cost $   493 GM  20.1%
2026 spot  premium 1.60x: price $   759 cost $   493 GM  35.1%
A-05 glut  premium 1.30x: price $   247 cost $   221 GM  10.4%
A-05 glut  premium 1.60x: price $   304 cost $   221 GM  27.2%

==============================================================================
C-12 U.S. KGD wafer-probe house (legacy DRAM)
==============================================================================
  200 wafers/yr: revenue $  120k, contribution $  -210k, startup capex $750k
  500 wafers/yr: revenue $  300k, contribution $   -75k, startup capex $750k
 1500 wafers/yr: revenue $  900k, contribution $   375k, startup capex $750k

==============================================================================
C-14 256Mb SDRAM, 1T1C MIM on 65nm 200mm (SkyWater Fab 25)
==============================================================================
die 116 mm2, gross 228, good 137, die $14.6, +pkg/test $15 -> $30/unit vs commercial 256Mb SDRAM ~$2-5 (Alliance/ISSI/Winbond, ESTIMATE)
  10000 units @ $60: gross profit $ 0.30M/yr vs NRE $10-20M
  50000 units @ $60: gross profit $ 1.52M/yr vs NRE $10-20M
 100000 units @ $40: gross profit $ 1.04M/yr vs NRE $10-20M

==============================================================================
C-15 legacy-DRAM buying cooperative (agency model)
==============================================================================
  10 members GMV $  10.0M: revenue $ 0.35M, opex $0.17M, title-model working capital (50 days) $  1.4M
  40 members GMV $  60.0M: revenue $ 1.90M, opex $0.23M, title-model working capital (50 days) $  8.2M
 100 members GMV $ 200.0M: revenue $ 6.00M, opex $0.35M, title-model working capital (50 days) $ 27.4M

OK
```
