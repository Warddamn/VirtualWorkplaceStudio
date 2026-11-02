# LEAN ARRAY MODULE: research notes (stage 3 dossier, rank 8, EV 40)

Agent `dos-lean-array-module`, 2026-11-02. Model: `models/lean-array-module.py`, which writes `research/stage3/lean-array-module_model_output.md`. Sources: `research/sources/dos-lean-array-module.jsonl` (40 entries; 6 WebSearch calls, all facts via search snippets). Assumptions: `research/assumptions/dos-lean-array-module.md`.

Tags: [REPORTED] means a search snippet or secondary source. [ESTIMATE] means my arithmetic (see model). [UNVERIFIED-PK] means prior knowledge with no URL found this session.

---

## 0. Verdict in five lines

1. **The physics is sound, and better than the card claims on arcing and uniformity.** In the free-molecular limit H2 carries 2.09x the heat of He per unit accommodation. Its continuum conductivity is 1.17x He's. Its Paschen minimum is ~2.3x higher. Like He, and unlike N2 or Ar, it gives gap-insensitive cooling (section A of the model).
2. **The key number is the H2 accommodation coefficient a_H2 on film-coated backsides. GO is a_H2 >= 0.17 and NO-GO is a_H2 < 0.10.** At 0.17 or above, H2 matches He at <=1.5x the He pressure. Below 0.10, parity needs more than the ~40 Torr clamp limit. The first-principles prior is ~0.27 (Baule mass scaling of Sandia's measured He value of 0.45); the planning value is 0.20.
3. **The helium lever is small in volume and cost.** Backside cooling uses ~7.5 L of He per DRAM wafer, about **3 % (range 1-11 %) of DRAM's pro-rata helium**. That is $0.32 per wafer, or ~104 u$/GB against $1.48/GB. A fab under a partial cut would keep backside cooling and shed other He uses first. H2 cooling is therefore a **tail-risk hedge and the last step to a fully He-free line**, not a cost lever. This finding is new versus the card, and it is the second thing to pin down.
4. **The secondary modules are honest-sized.** AAO at the 1-beta pitch gives 5.8-7.0 fF (parity to +30 %), not +37-64 %. Its value is the deleted fluorocarbon HAR etch. IL/NIL meets only ~10 nm overlay with per-field phase lock. That is legal only for F~40 nm oxide cells, which need >=5 tiers to reach 1-beta density.
5. **Decisive experiment:** a $100k Sandia-style gas-gap accommodation rig (8 months, binary gate). Then a $120k university ICP etcher test (H2 backside plus H2 bleed). Then a $300k partner-hosted 300 mm chamber swap. All of it fits in **$995k over 22 months** with the AAO coupon and IP included.

---

## 1. Prior art and who is pursuing it

### 1a. H2 (or non-He) backside gas
| Item | Who / date | What it shows | Source |
|---|---|---|---|
| ESC patents listing H2 as a backside gas | unknown assignee; US 10,395,963 (the carrier within the result set is not pinned) | H2 named beside He/Ar/N2; no production use shown | [USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10395963) [REPORTED] |
| He bypass/dump ESC | US 9,753,463 | ~0.5 sccm crosses the seal and ~19.5 sccm is dumped; some makers use **N2/Ar for cost**, accepting ionization, thermal and arcing limits | [USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9753463) [REPORTED] |
| Backside cooling, He standard | US 6,170,496 | He standard, N2 alternative; ionized gas can arc | [Justia](https://patents.justia.com/patent/6170496) [REPORTED] |
| Gas-gap wafer cooling | US 5,810,933 | Measured transfer falls below prediction, attributed to accommodation | [USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5810933) [REPORTED] |
| Substrate-to-chuck heat transfer | US 7,017,652 | Title only seen | [Justia](https://patents.justia.com/patent/7017652) |
| **Closest production analogue: EUV electrostatic clamps** | ASML-related filings, e.g. US 12,174,552; US 12,461,452; US 12,717,249; US 12,189,309 | The clamp operates in a **low-pressure hydrogen-rich environment**. Backfill gas at the burl interface aids cooling. Charge builds on dielectric surfaces. No plasma bias, low heat flux. Whether the backfill gas itself is H2 is not confirmed in the snippets | [USPTO 12174552](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12174552), [USPTO 12461452](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12461452), [USPTO 12717249](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12717249), [Google 12189309](https://patents.google.com/patent/US12189309) [REPORTED] |
| Surfaces engineered to raise accommodation, H2 target >=0.4 | US 8,970,818 (lithography component) | Prior art for "coat the surface to raise a_H2". Both a fallback route and an IP constraint | [USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8970818) [REPORTED] |

**Conclusion:** no production H2 backside use in a plasma chamber was found, across 3 searches over Stage 2 and this stage. The EUV clamp proves that an ESC, H2 and gas-gap conduction can coexist in high-volume tools, but without RF bias or fluorocarbon chemistry.

### 1b. Helium mitigation incumbents (the real competitor)
- **Samsung HeRS** (in-house Helium Reuse System) has run on select lines since **April 2025**. A post attributed to Samsung Semiconductor puts the first line's saving at ~4.7 t/yr ([TrendForce 2026-03-23](https://www.trendforce.com/news/2026/03/23/news-under-qatars-shadow-helium-crunch-hits-south-korea-harder-putting-samsung-sk-hynix-tsmc-in-spotlight/); [LinkedIn, weak attribution](https://kr.linkedin.com/in/haneul-yu-49296072)) [REPORTED]. That is ~22 L/wafer on a ~1.2M wafer/yr line [ESTIMATE], the same order as my 7.5 L/wafer backside estimate.
- Leading fabs reach ~80-90 % on-site recovery ([TrendForce 2026-04-08](https://www.trendforce.com/news/2026/04/08/news-decoding-impact-asia-chipmakers-move-to-tackle-helium-strain-as-intel-gains-relative-buffer/)) [REPORTED]. Recycling and diversification do not solve dependence near term ([Nasdaq 2026](https://www.nasdaq.com/articles/war-or-peace-artificial-intelligence-ai-chip-industry-just-learned-depending-one-route-30)) [REPORTED]. SK hynix claims diversified supply and adequate inventory ([Tom's Hardware 2026-03](https://tomshardware.com/tech-industry/qatar-helium-shutdown-puts-chip-supply-chain-on-a-two-week-clock)) [REPORTED].
- Context: Qatar ~30 % of supply, offline since March 2026; Korea 64.7 % Qatar-sourced; ~6 weeks of on-site storage ([AP via WTOP 2026-03-21](https://wtop.com/news/2026/03/iran-war-halts-qatar-helium-output-threatening-global-tech-supply-chains/)). Spot $1,000-1,200/Mcf vs ~$500 before the war ([Tom's Hardware 2026](https://tomshardware.com/tech-industry/semiconductors/the-global-helium-shortage-is-a-direct-threat-to-chipmaking)) [REPORTED, from A2].

### 1c. Accommodation science
- **Sandia, Trott et al. (2010)** built a parallel-plate, pressure-swept heat-flux assembly. On untreated surfaces including silicon it measured ~0.95 Ar, ~0.85 N2 and ~0.45 He. An in-situ Ar-plasma clean lowers He by up to 0.10. Roughness matters little; contamination matters more ([Sandia 2010-11](https://www.sandia.gov/research/publications/details/an-experimental-assembly-for-precise-measurement-of-thermal-accommodation-c-2010-11-01/); [Sandia 2010-10](https://sandia.gov/research/publications/details/determination-of-thermal-accommodation-coefficients-from-heat-transfer-meas-2010-10-01)) [REPORTED]. **This is the template for Step 1, and Sandia is the obvious collaborator.**
- APS DFD 2006: heat-flux TAC for He on Si-based surfaces; the Maxwell model is adequate ([APS](https://meetings-archive.aps.org/dfd/2006/ho/3/)) [REPORTED].
- He on crystalline Si at 11-30 K, up to ~0.7 (cryogenic, not applicable at room temperature) ([arXiv 2402.11977](https://arxiv.org/pdf/2402.11977)) [REPORTED].
- Engineering surfaces 0.2-0.5 ([UMich JCP 58, 4080](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/70040/JCPSA6-58-10-4080-1.pdf;sequence=2), attribution likely) [REPORTED]. Song and Yovanovich gap-conductance theory, 1988-89 ([Waterloo MHTL](https://uwaterloo.ca/microelectronics-heat-transfer-laboratory/publications/contributors/ssong)) [REPORTED, correlation not seen].
- **No measured H2 accommodation on SiO2, SiN or poly-coated Si was found.** This confirms the card's key unknown.

### 1d. PFAS-light capacitor modules
- **AAO MIM:** Banerjee et al., Nat. Nanotech. 2009 (UMD, Rubloff/Lee). ALD TiN/Al2O3/TiN in AAO, ~10 uF/cm2 at 1 um ([DOI](https://dx.doi.org/10.1038/nnano.2009.37)). Imprint-pretextured ideal ordering at 40-500 nm interval (Masuda, [MRS-J](https://www.mrs-j.org/pub/tmrsj/vol29_no3/vol29_no3_0855.pdf)) [REPORTED, from B2].
- **One search found no AAO-template DRAM capacitor patent** (a negative result). The closest is Micron's template-based storage node, US 7,829,410 ([Google](https://patents.google.com/patent/US7829410)), plus Micron's Al2O3-dielectric capacitor, US 7,126,181 ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7126181)) [REPORTED]. Korean and Japanese 2000s AAO-DRAM filings may exist [UNVERIFIED-PK]; a proper FTO search is needed.
- **Fluorine-free carbon mold (N-29):** a-C hardmasks are standard in 3D NAND [UNVERIFIED-PK]. Cornell CNF / Atkinson runs a 2026 PFAS-in-plasma-etch project with a chipmaker advisory board ([Cornell](https://atkinson.cornell.edu/research/dashboard/optimizing-semiconductor-manufacturing-processes-to-eliminate-emissions-of-pfass-and-high-global-warming-potential-gases/)) [REPORTED, from B2].

### 1e. EUV-free periodic patterning
- **Micron 1-beta (0.447 Gb/mm2) uses zero EUV, and CXMT ships DDR5 without EUV** (A1/A2).
- **Canon NIL:** SPIE 2024 reports better than 10 nm resolution, single-mask printing of critical memory levels, and a cheaper tool ([SPIE 12956](https://spiedigitallibrary.org/conference-proceedings-of-spie/12956/3012070/Nanoimprint-lithography-performance-advances-for-new-application-spaces/10.1117/12.3012070.full); [SPIE 13177](https://proceedings.spiedigitallibrary.org/conference-proceedings-of-spie/13177/1317708/Nanoimprint-performance-improvements-for-high-volume-semiconductor-device-manufacturing/10.1117/12.3034104.full)). DRAM layouts often do not suit SADP/SAQP ([SPIE 12956-04](https://spiedigitallibrary.org/conference-proceedings-of-spie/12956/1295604/Optimization-of-NIL-and-associated-pattern-transfer-processes-for-the/10.1117/12.3012453.full)). SK hynix and Kioxia tested Canon NIL for years ([Bits&Chips 2023](https://bits-chips.com/magazine/bc202308/?pagenr=7)). DNP showed a 10 nm NIL template in Dec 2025 ([TrendForce listing](https://www.trendforce.com/news/category/Semiconductors/page/5)). A claim that Micron uses NIL on some DRAM layers is undated and uncorroborated ([techovedas](https://techovedas.com/?p=15160)) [UNVERIFIED]. All [REPORTED].
- **IL:** 193i IL reaches ~33.5 nm half-pitch ([US 8,685,628](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8685628)). Also MIT SBIL / Nanoruler (Schattenburg), Eulitha displacement Talbot, and Intel/Borodovsky complementary lithography [UNVERIFIED-PK except the patent].

### 1f. Ga-free channels (N-26)
- UMich ZTO 2T0C, >1,500 s retention ([Deep Blue](https://deepblue.lib.umich.edu/items/e6ac2d99-46aa-444a-bc41-2851e63c965c)) [REPORTED, from B2]. The U.S. Ga export-ban suspension ends 2026-11-27 (A2).

---

## 2. Best demonstrated numbers for each component

| Component | Best demonstrated | Needed here | Gap |
|---|---|---|---|
| He accommodation, technical Si/metal | ~0.45 (Sandia) | baseline | none |
| H2 accommodation, coated Si | **not measured** | >=0.17 (GO) | **the experiment** |
| H2 backside in a plasma ESC | none found | 300 mm, 2-5 kW, +/-2 K vs He | full qualification |
| ESC + H2 environment | EUV clamps in low-p H2 (production) | plus RF bias and fluorocarbon chemistry | plasma interaction |
| He recapture | 80-90 % at leading fabs; Samsung HeRS ~4.7 t/yr on line 1 | competitor | n/a |
| AAO pore AR with ALD MIM | ~200 (50 nm pores, 10 um; UMD) | ~70-85 at 35-40 nm pitch | pitch 35 nm, registration to pads |
| AAO ordered interval | 40-500 nm (imprint-pretextured) | 35-40 nm | at the lower edge |
| NIL resolution | <10 nm (Canon; DNP template 10 nm) | 20-40 nm periodic | overlay and defects, not resolution |
| 193i IL half-pitch | ~33.5 nm | 40 nm periodic (+SADP for 20 nm) | overlay ~10 nm |
| Ga-free oxide 2T0C retention | >1,500 s (ZTO) | >=64 ms (refresh-free is a bonus) | Vt control at short Lg |

---

## 3. Model headline numbers (from `lean-array-module_model_output.md`)

- **Gas physics:** H2/He conductance per unit accommodation is 2.09x free-molecular and 1.17x continuum. The jump model reproduces Corruccini to within 0.0 % at the free-molecular limit.
- **At 3 kW (34 kW/m2), 10 um gap:**
  - He at 15 Torr gives h = 1,180 W/m2K and a 28.8 K wafer-chuck dT.
  - H2 (a = 0.20) gives 976 W/m2K at 15 Torr (+6 K) and parity at **18.5 Torr**.
  - N2 (a = 0.85) gives a similar average, 1,098 W/m2K, but an **11.9 K dT spread for a +/-5 um gap, against He's 2.0 K and H2's 1.7 K**. That uniformity is why He, and only H2 after it, is the drop-in.
- **Break-even a_H2:** 0.24 for a drop-in, **0.17 at <=1.5x pressure (GO)**, and **0.10 at the 40 Torr clamp limit (NO-GO)**. These values hold within +/-0.005 for gaps of 5-40 um.
- **Asymmetric case:** wafer 0.10 against chuck 0.45 still reaches parity at 23 Torr. A chuck face that accommodates H2 well rescues a poor wafer side.
- **Paschen minimum:** He 142 V, H2 326 V (2.3x), N2 358 V, Ar 188 V. These use textbook constants.
- **Leak at the GO pressure:** 1.1-2.5 sccm into the plasma, giving H/F atoms 0.5-1.2 %. The foreline sits at 2.1 % of LFL in normal operation and 10 % of LFL under an RFO-limited single fault.
- **Helium lever:** 7.5 L/wafer, ~3 % of DRAM pro-rata helium (1-11 %), $0.32/wafer. An H2 retrofit of 1,500 chambers at $50k costs ~$75M and pays back after ~2.4 days of avoided full stoppage at a 100k-wpm fab.
- **AAO, 1-beta pitch (35.2 nm, ~14 V):** 5.84 fF at 2.5 um and 7.01 fF at 3 um, giving 76-88 mV of signal and 67-81 ms at a 13 fA tail. At 40 nm pitch it is 7.4-8.9 fF, matching B2-01. Anodization takes ~34 Wh/wafer.
- **IL overlay:** per-field phase lock at 0.3 ppm residual gives 6.3 nm. A single full-wafer grating gives 39 nm per 0.1 K. An F = 40 nm oxide 4F2 cell gives 0.109 Gb/mm2 per tier (0.24x 1-beta, so >=5 tiers).

---

## 4. U.S. facilities that could build the demo

| Facility | Use in this program | Cost / access info |
|---|---|---|
| **Sandia National Labs** (Engineering Sciences; Trott et al. TAC assembly) | Step 1 partner: its parallel-plate TAC rig design or the rig itself; DSMC modeling | CRADA / Strategic Partnership; CINT is a DOE user facility, free by proposal for non-proprietary work [UNVERIFIED-PK]. MESA is Sandia's fab, reached via CRADA, not open user access [UNVERIFIED-PK] |
| **NY CREATES Albany NanoTech** (+ Applied Materials META Center, Albany) | Step 2: 300 mm etch chamber with H2 backside | 300 mm prototyping access for startups, SMEs and universities ([NY.gov 2024](https://www.ny.gov/roadmap-national-semiconductor-technology-center-new-york)) [REPORTED]. Memory JDA precedent: Fraunhofer IPMS 2025 ([idw](https://nachrichten.idw-online.de/2025/05/16/ny-creates-and-fraunhofer-ipms-announce-joint-development-agreement-to-advance-memory-devices-at-300mm-wafer-scale)) [REPORTED]. Campaign ~$300k plus partner in-kind [ESTIMATE] |
| **Cornell CNF** | Step 1b ICP fluorocarbon oxide etch; synergy with its 2026 PFAS-etch project | NNCI site; industrial hourly rates ~$100-300/h class [ESTIMATE, not verified] |
| **UIUC (CPMI, Ruzic) / Univ. of Maryland (Oehrlein lab, plus FabLab)** | Plasma-surface measurement of the H2 leak-in effect on fluorocarbon films; UMD also has the AAO-MIM heritage (Rubloff/Lee) | Collaboration / sponsored research [UNVERIFIED-PK] |
| Stanford SNF, MIT.nano, Penn Singh, Georgia Tech IEN, Purdue Birck, ASU | Alternatives for Step 1b etch and AAO coupons (Al sputter, anodization, ALD, SEM/TEM) | NNCI-class rates [ESTIMATE] |
| **UT Austin / Texas Institute for Electronics** | NIL pretexture for AAO, and the later IL/NIL module | Canon NIL tool at TIE [UNVERIFIED-PK; not confirmed by this session's search] |
| Argonne CNM, ORNL CNMS, LBNL Molecular Foundry, NIST CNST | ALD in pores and pore metrology (CNM); TEM (Foundry, CNMS); NIL/e-beam pretexture (CNST) | DOE/NIST user proposals, free for non-proprietary work [UNVERIFIED-PK] |
| MIT Space Nanotechnology Lab / Plymouth Grating Lab | SBIL for the deferred IL overlay test | Contract [UNVERIFIED-PK] |
| MPW shuttles: ChipFoundry sky130, wafer.space GF180, MOSIS 2.0 | Only if AAO capacitors are post-processed onto CMOS access die (stretch) | sky130 ~$15k per 100 chips ([eeNews](https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)); GF180 ~$7k per 1,000 ICs, fabbed in Singapore ([electronics-lab](https://www.electronics-lab.com/e-lab-interview-wafer-space-founder-aims-to-make-custom-silicon-accessible-again/); [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-3)); MOSIS 2.0 reaches >35 MPW shuttles ([ISI](https://www.isi.edu/news/80945/mosis-2-0-revives-a-legacy-rehan-kapadia-outlines-a-bold-future-for-rapid-microelectronics-prototyping/)) [REPORTED, cross-referenced] |
| Test and safety | Thermocouple wafers (KLA SensArray class) [UNVERIFIED-PK]; third-party SEMI S2 / NFPA 55 / NFPA 2 assessor (TUV/UL class) [UNVERIFIED-PK] | ~$30k for the safety review [ESTIMATE] |

---

## 5. Collaborators and recruits (named groups)

All names are [UNVERIFIED-PK] except Trott (Sandia) and the UMD AAO work (Banerjee/Rubloff/Lee), which the search confirmed.
- **Recruit (device/process co-founder):** an ESC/thermal or etch-process engineer from Lam Research, Applied Materials or TEL with backside-gas and chuck-qualification experience. That background carries Step 2 and the OEM licensing path.
- **Gas-surface accommodation:** Sandia Engineering Sciences (W. M. Trott; J. R. Torczynski, M. A. Gallis, D. J. Rader on DSMC and the TAC assembly). Univ. of Waterloo MHTL (the Yovanovich gap-conductance lineage).
- **Fluorocarbon plasma-surface (H2 leak-in):** G. Oehrlein (UMD), J. P. Chang (UCLA), V. Donnelly / D. Economou (Houston), D. Ruzic (UIUC CPMI). For modeling, M. Kushner (Michigan, HPEM) for an H2-bleed simulation before the 300 mm run.
- **AAO:** G. Rubloff / S. B. Lee (UMD), H. Masuda (Tokyo Metropolitan Univ., ordered AAO), and J. Elam (Argonne, ALD in high-AR pores).
- **IL/NIL:** M. Schattenburg (MIT SNL, SBIL), S. Brueck (UNM CHTM, immersion IL), and the Canon NIL / TIE team.
- **Ga-free oxide channels:** the U. Michigan oxide-TFT group behind the ZTO 2T0C thesis.
- **Industrial pull:** Samsung and SK hynix procurement (Korea is 64.7 % Qatar-exposed). Linde and Air Products, as both helium suppliers and on-site H2 suppliers.

---

## 6. Decisive experiment (step by step)

**Step 1, months 1-8, ~$100k: H2 accommodation matrix (the binary gate).**
1. Build a Sandia-style parallel-plate cell. The hot plate (50 mm, heater plus guard ring) carries a wafer coupon. The cold plate carries a chuck-ceramic coupon. Gaps of 5, 10, 20 and 50 um are set by spacers and read capacitively. Pressure runs 0.05-50 Torr on capacitance manometers. The heat flux comes from guard-balanced heater power.
2. Gases: He (calibrate against Sandia's ~0.45), H2, N2, Ar, plus 25/50/75 % H2-He blends.
3. Wafer faces: native-oxide Si, thermal SiO2, LPCVD SiN, poly-Si, backsides after a fluorocarbon-plasma exposure (CFx film), and backsides after post-etch wet clean. Chuck faces: Al2O3, AlN, and Y2O3-coated Al2O3. Temperatures: 20, 40 and 60 C.
4. Fit a_wafer and a_chuck from the pressure and gap sweeps with `h_gas()` in the model. The target uncertainty is +/-0.02.
5. **Gate:**
   - a_H2 (symmetric equivalent) **>= 0.17: GO**.
   - 0.10-0.17: CONDITIONAL. Test a chuck coating that raises a_H2 (mind US 8,970,818), or a blend.
   - **< 0.10: NO-GO** for pure H2. Pivot to a blend or He recapture.

**Step 1b, months 4-10, ~$120k: university ICP etcher (150/200 mm ESC).**
1. Install an H2 backside line with an RFO, an H2 sensor and an N2-purged plenum. Most NNCI fabs already run H2 for CVD and furnaces.
2. Compare a thermocouple wafer under He vs H2 at 5-30 Torr and 1-3 kW bias.
3. Bleed 0-4 sccm H2 into a C4F6/C4F8/O2/Ar SiO2 etch, which is 2x the predicted 1.1-2.5 sccm leak. Measure etch rate, selectivity to the a-C/poly mask, and profile on AR 10-20 coupons. Track H-alpha and CF2 by OES.
4. Pass: etch-rate drift <=2 %, selectivity drift <=5 %, and dT within +/-2 K of He after pressure tuning.

**Step 2, months 10-20, ~$300k plus partner in-kind: 300 mm chamber swap (NY CREATES or an OEM demo lab).**
1. Run a hazard analysis on the SEMI S2 / NFPA 55 / NFPA 2 path. Build the RFO plus purge interlock (the model gives 10 % LFL in single fault).
2. Map thermocouple-wafer temperatures for He vs H2 at 2-5 kW, center and edge zones.
3. Etch HAR oxide (AR >=40) on patterned wafers. Measure etch rate, selectivity, bow and CD against the He baseline. Log foreline H2 for >=100 wafer-hours.
4. Pass: +/-2 K across the wafer, etch-rate drift <=2 %, selectivity drift <=5 %, and no backside arcing events.

**Step 3, months 12-20, ~$80k (parallel, secondary): AAO capacitor coupon.**
1. Sputter 2.5-3 um of Al on Si with TiN pads.
2. Pretexture at 40 nm pitch with e-beam or NIL, then anodize at 14-16 V.
3. Thin the barrier and remove it. ALD TiN/ZrO2/TiN.
4. Measure fF per pore (array capacitance / count), leakage at 85 C, pore-order defects and pore-to-pad registration yield.
5. Pass: >=5.5 fF per pore at <=40 nm pitch, leakage <=1 fA per cell-equivalent, registration yield >=99.9 % (a first look; DRAM needs far more).

**Deferred:** the IL moire overlay test (~$500k, I-07130) waits until a periodic oxide cell wafer exists.

### Budget (USD, <= $1M)
| Line | $k |
|---|---|
| Step 1 rig: manometers, heater/guard, vacuum, DAQ, spacers ($55k); coupons and films ($15k); lab fees / student ($30k) | 100 |
| Step 1b: ICP tool time, thermocouple wafers, H2 install at host fab, SEM | 120 |
| Step 2: 300 mm chamber campaign (cash share; partner in-kind excluded) | 300 |
| Safety / regulatory third-party review (SEMI S2, NFPA 55/2) | 30 |
| Step 3: AAO coupon (Al sputter, pretexture, anodization, ALD, metrology) | 80 |
| Plasma modeling collaboration (H2-bleed simulation, 1 student-year) | 40 |
| IP: 3 provisionals + 1 PCT | 45 |
| Two lean founder stipends (portfolio frame) | 230 |
| Contingency (~5 %) | 50 |
| **Total** | **995** |

### Timeline (22 months)
| Months | Milestone |
|---|---|
| 0-2 | Rig design, coupon procurement, Sandia CRADA, host-fab H2 safety plan |
| 2-8 | Step 1 measurements; **gate at month 8** (GO / CONDITIONAL / NO-GO) |
| 4-10 | Step 1b ICP He-vs-H2 and H2-bleed etch |
| 10-20 | Step 2 300 mm chamber swap; safety package |
| 12-20 | Step 3 AAO coupon |
| 20-22 | Data package for OEM licensing and the $10-50M raise |

---

## 7. IP landscape

**Patents to watch, or prior art that limits claims:**
- **ESC backside gas:** US 10,395,963 (lists H2), US 9,753,463 (He dump; N2/Ar), US 6,170,496, US 5,810,933, US 7,017,652. Because H2 is already named as a backside gas, **a broad "H2 as backside gas" claim is not patentable**. Some older filings are likely expired [ESTIMATE].
- **Accommodation-raising surfaces:** US 8,970,818 (H2 TAC target >=0.4).
- **EUV clamp in H2 / backfill gas:** US 12,174,552, US 12,461,452, US 12,717,249, US 12,189,309, and US 7,187,433 (backfill release; seen in a snippet, URL not given).
- **Capacitor templates:** Micron US 7,829,410 and US 7,126,181. A deeper KR/JP search for AAO-DRAM filings is required [open gap].
- **NIL:** the Canon portfolio. **IL:** the MIT SBIL patents and US 8,685,628.

**What to file (narrow, defensible):**
1. **Accommodation-mapped H2 backside control.** Set H2 (or blend) pressure per zone from a measured a_H2 map of the incoming wafer's backside film stack, with closed-loop wafer-temperature control.
2. **Leak-compensated recipe.** Feed forward the measured H2 seal leak (sccm) into the recipe by trimming deliberate H-additive (CH2F2/H2) flows, so the plasma H/F ratio stays fixed.
3. **Composition as a zone actuator.** Vary the H2/He or H2/N2 ratio per ESC zone to tune local h independently of pressure. Gases with different a and k give a control knob that pressure alone lacks.
4. **Wafer-side or chuck-side surface treatment** that raises a_H2 in plasma-chamber ESCs. Claims must avoid the US 8,970,818 scope.
5. **AAO capacitor mold** registered by imprint pretexture to landing pads. The barrier removal stops on TiN, and the alumina is retained as the support lattice. File only after the FTO search.
6. **Safety architecture:** an RFO-limited H2 backside line with an N2-purged plenum and foreline-dilution interlock, sized to <=25 % LFL in single fault.

---

## 8. Open gaps and risks

1. **a_H2 on coated backsides is unmeasured.** This is the decisive unknown, and it is cheap to measure.
2. **The backside share of fab helium is unverified.** My estimate is ~3 %, with a 1-11 % range. If it is small, H2 cooling matters only in a near-total cutoff, or as the last step to He-free. If HeRS-type data show backside cooling is a large share, the hedge value rises. Ask Samsung, SK hynix, Linde or Air Products for use splits.
3. **Substitutability of the other He uses** (leak check, PECVD diluent, purge, RTP/laser anneal) decides whether a He-free line is reachable at all.
4. **Plasma interaction:** whether a ~1-2.5 sccm H2 leak shifts HAR selectivity beyond tolerance. This is a 0.5-1.2 % H/F perturbation, and only Step 1b/2 can settle it.
5. **Materials:** H2 effects on Y2O3/AlN chucks under plasma, ESC bond layers, elastomer-seal permeation, and Ti/metal embrittlement. For CVD heaters at 400-650 C, H2 reduction of backside films. W CVD already runs H2, which reassures but does not prove [UNVERIFIED-PK].
6. **Clamp limit:** the 40 Torr p_max is an estimate. A J-R chuck with higher clamp force widens the GO window.
7. **Unverified inputs:** the Paschen constants, the world helium production figure and nanofab rates were not verified this session.
8. **Low step size:** this is a supply-chain hedge (EV S = 2). Its best role in the portfolio is the He/PFAS/EUV-free recipe for whichever cell wins, licensed to OEMs as a qualification package.

**Kill condition and revival.** The concept is killed if a_H2 < 0.10 on every realistic backside/chuck pair and no coating lifts it. It revives if a chuck-face treatment reaches a_H2 >= 0.2, or if a 50/50 H2/He blend holds He-level h while halving He use.
