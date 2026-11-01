# DD5 Open Memory IP: model output

Captured stdout of `python3 models/open-memory-ip.py` (re-run 2026-11-01 from the repo root after the Phase 5 red team, exit 0). Phase 4 agent `p4-open-memory-ip`; Phase 5 revisions by `p5r-open-memory-ip` (see the "RED-TEAM REVISIONS (Phase 5)" block in the model and section 0 below). Notes: `research/phase4/open-memory-ip_notes.md`. Red-team responses: `research/phase5/responses_open-memory-ip.json`.

Section 0 prints every changed input (old -> new, objection id) and the Phase 4 and Phase 5 headlines side by side. Sections 1-10 use the revised inputs. The T2 path (section 9) is killed and printed for reference only.

```text
============================================================================================================
DD5 U.S. OPEN MEMORY IP - unit economics & 36-month P&L (models/open-memory-ip.py, as of 2026-11-01)
PHASE 5 REVISED (red team, p5r-open-memory-ip). Sections 1-10 use the revised inputs; section 0 compares.
============================================================================================================
DDR5 reference source: models/dram_cost_stack.py ddr5_reference()
  incumbent cost $1.48/GB | Q4-26 contract $20.37/GB | glut $8.15/GB | severe $2.04/GB

0. RED-TEAM REVISIONS (Phase 5): every changed input, old -> new, objection id
  R1  CF_PROJECTS_PER_YEAR     60 -> 30  [RT-VC-DD5-01]
      basis: the Phase 4 input note itself says 2-3 shuttles/yr at >=50% fill = ~20-30 paid slots; Efabless chipIgnite peaked at ~43/yr (80 commercial + 50 university designs over ~3 yrs) with subsidised demand
  R2  CADENCE_PROJECTS_PER_YEAR 30 -> 20  [RT-VC-DD5-01]
      basis: only one 2026 Cadence SKY130 run is documented (deadline 2026-01-16); 'multiple runs per year' is a plan, not a count
  R3  OTHER_US_ACAD_PROJECTS   60 -> 30  [RT-VC-DD5-01]
      basis: MOSIS 2.0 and the Commons publish no counts of full-chip open-PDK projects; halved for lack of any count
  R4  ACAD_SHARE               0.6 -> 0.7  [RT-HYP-DD5-03; RT-VC-DD5-05]
      basis: named commercial targets are microfirms (Avalon, Cloneless, Tillitis/Zedulo); funded SBIR teams going to production move to the S130 NDA PDK with SkyWater's bundled compilers; 0.80 is run as a sensitivity
  R5  P_LIC                    20000 -> 12000  [RT-HYP-DD5-02; RT-PHY-DD5-01; RT-VET-DD5-02; RT-VC-DD5-06]
      basis: licence restated as 'one nominal MPW lot measured at voltage/temperature points (rented thermal forcing), process corners simulated and correlated to that lot, yield on >=50 die, warranty = re-delivery or refund of fees'; priced at 1.2x the commercial service fee [ESTIMATE]
  R6  LIC_RATE_COM_YR          0.25 -> 0.15  [RT-HYP-DD5-02; RT-PHY-DD5-01; RT-VET-DD5-02]
      basis: without skew-corner data the licence's edge over free simulated OpenRAM corners is smaller, so fewer commercial teams buy it [ESTIMATE]
  R7  LIC_DOD_MONTH            0.08 -> 0.04  [RT-PHY-DD5-07; RT-VET-DD5-04; RT-HYP-DD5-05]
      basis: DoD/SBIR buyers usually need SEE/TID data the plan will not fund, and the U.S.-fab axis covers only sky130 (wafer.space Run 3 page: GF180MCU chips fabricated at GF in Singapore)
  R8  CONTRACT_RATE            125 -> 150  [RT-VC-DD5-03]
      basis: retainer premium for a memory contractor who signs a 12-month exclusivity / non-compete on publishing free characterized >=16 KB sky130 macros [ESTIMATE: +20%]
  R9  GF180_CHAR_DONE          10 -> 11  [RT-VC-DD5-04]
      basis: wafer.space Run 3 dates are unpublished; one month of slack on the m4 GF180 slot
  R10 SKY130_CHAR_DONE         13 -> 16  [RT-VET-DD5-06; RT-VC-DD5-04]
      basis: TTSKY25b on ChipFoundry CI2511: submissions closed 2025-11-10, chips expected Jul-2026 (~8 months), plus ~1 month on the bench; ChipFoundry moves an under-filled run to the next shuttle
  R11 OUTREACH_UNIVERSE_CAP    False -> True  [RT-HYP-DD5-01]
      basis: outbound contacts/month capped at distinct new project teams = full-chip projects per year / 12; the 120-name list is spent in the m0 kill test, and full-time work adds no fresh names
  R12 ACAD_PROC_LAG            0 -> 2  [RT-HYP-DD5-06]
      basis: university vendor registration and POs add 30-90 days (DD4 s7); the academic offer becomes a per-term course pack at the same $1.2k/term
  R13 P_GF180_FREE             0.0 -> 0.6  [RT-HYP-DD5-04; RT-VC-DD5-01]
      basis: OCD (last commit 2026-10-30) and Chips4Makers (3 GF180 SRAM test chips, Jul-2026) already have silicon, and DD s5 says GF180 is probably lost within 12 months; the haircut weight is GF180 share of projects x 0.6, applied from m24 to close rate, churn, subscription price and licences through the free_bundle_shock parameters
  R14 LARGE_MACRO_ARRAY_EFF    0.6 -> 0.3  [RT-PHY-DD5-06]
      basis: no OpenRAM evidence for 60%; going from the 1 KB to the 2 KB OpenRAM sky130 macro adds 11.4 um2 per added bit (6x the 1.896 um2 bitcell), so OpenRAM's periphery does not amortise like a commercial compiler's; 30% until the day 1-7 run measures a 32 KB macro
  R15 ONE_TIME_LIST            11 items, $68,500 total -> 17 items, $94,600 total  [RT-VET-DD5-01; RT-PHY-DD5-02; RT-VET-DD5-02; RT-VC-DD5-03]
      basis: adds test structures that make ns access time measurable, thermal forcing for -40/125C [ESTIMATE: ThermoStream-class rental ~$2-4k/week], the stronger kill-test gate (kill test now ~$9.1k, of which $1k template is the m1 item), and moves characterization to m11/m16
  R16 CASH_GATE_FLOOR          None -> 2500  [RT-PHY-DD5-02; RT-VET-DD5-02; RT-VC-DD5-04 (consequence)]
      basis: the added spends push BASE cash to -$8.2k at m11 on the Phase 4 schedule, beyond the $40k deployable (A-03); deferrable spends (test chips, slots, bench, characterization) now wait until cash after the spend stays >= $2.5k, and the characterized month moves with them
  R17 QUAL_LOTS                400000 -> 1000000  [RT-VET-DD5-05]
      basis: JESD47 needs HTOL 1,000 h on 3 lots x 77 units plus retention bakes, ESD/latch-up and MSL on a production S130+ReRAM flow: three engineering lots plus a qual house, not one lot [ESTIMATE]; T2 is killed, so this is reference only
  Phase 4 vs Phase 5 headline (same code; Phase 4 = the inputs above swapped back):
  inputs             scen       cash low      3-mo CF+   founder FT   ARR m18   ARR m36     RR m36   end cash sky130 ch
  Phase 4            BASE      $20.4k@m7            m8          m20    $66.6k   $157.6k    $423.9k    $219.3k       m13
  Phase 4            GLUT      $20.4k@m7            m8          m25    $58.9k   $125.8k    $342.1k    $175.4k       m13
  Phase 4            SEVERE    $20.4k@m7            m8          m30    $54.6k   $105.7k    $291.2k    $175.4k       m13
  Phase 5            BASE      $4.0k@m15           m12        never    $41.2k    $65.7k    $164.1k     $88.4k       m24
  Phase 5            GLUT      $2.8k@m15           m12        never    $36.8k    $54.9k    $137.9k     $60.4k       m24
  Phase 5            SEVERE    $3.6k@m18           m12        never    $34.3k    $49.3k    $123.9k     $45.1k       m27

1. WHY THE AXIS IS NOT $/GB (density and $/GB context)
  sky130 6T bitcell limit                      527.4 kbit/mm2  (1.896 um2 cell)
  sky130 OpenRAM 1KB / 2KB macros (largest)     43.0 /  57.6 kbit/mm2
  sky130 banked 32-64KB macro @30% array eff   158.2 kbit/mm2  -> 2.7x the 2KB macro (compiler work, no new cell)
    revised after red team (RT-PHY-DD5-06): Phase 4 assumed 60% (316.5 kbit/mm2, 5.5x). OpenRAM 1KB->2KB adds 11.5 um2 per added bit
    (6.0x the bitcell), so periphery does not amortise like a commercial compiler; the kill test measures a real 32KB macro.
  GF180 open macros: GF 512B / OCD 1KB          19.6 /  52.7 kbit/mm2 (largest free GF180 macro = 1KB)
  Gain-cell density vs 6T: silicon (65nm, Teman) 1.25-1.43x; vendor claims (RAAAM/GF) 1.67-2.00x -> NOT the 2-4x in the hypothesis
  sky130 SRAM silicon ~$1330/GB vs DDR5: BASE $18.33/GB -> 73x | GLUT $8.15/GB -> 163x | SEVERE $2.04/GB -> 653x
  => macros are priced per design/tapeout, not per GB; the DDR5 cycle touches this only via design-start budgets.

2. MARKET SIZING (projects per year on open/academic shuttles: U.S.-fab sky130 + GF180MCU fabbed in Singapore)
  Tiny Tapeout 2026 tiles (funnel only, not macro buyers): 899
  wafer.space 54 x 2 + ChipFoundry 30 + Cadence MPW 20 + GF univ pilot 40 + MOSIS2/Commons/other 30 = 228 full-chip projects/yr
  of which GF180MCU (wafer.space + GF pilot; fabbed by GF in Singapore per wafer.space Run 3) 148 | U.S.-fab sky130/MOSIS/Commons 80
  -> the supply-security axis ('U.S.-fabbed ASIC') covers only the 80 U.S.-fab projects/yr (RT-VET-DD5-04, RT-HYP-DD5-05)
  x need memory beyond free macros 30% x willing to pay 40% = 27 paying projects/yr
  active-account cap (x 2.0 yr groups): academic 38, commercial 16
  => serviceable revenue ceiling of the wedge at full share: $424.4k/yr (subscriptions + services + licenses)

3. UNIT ECONOMICS PER PRODUCT LINE (BASE prices)
  Product line                      Price       COGS       GM
  A1 Sub academic (/mo)              $200        $66      67%
  A2 Sub commercial (/mo)            $800       $114      86%
  B1 Tapeout svc academic          $3,000     $1,990      34%
  B2 Tapeout svc commercial       $10,000     $4,900      51%
  C  Characterized license        $12,000     $6,060      50%
  C licence restated after red team: one nominal MPW lot measured at V/T points, process corners simulated,
    yield on >=50 die, warranty = re-delivery or refund of fees (Phase 4: 'measured PVT corners', $20,000).
  Academic subscription sold as a per-term course pack ($1.2k/term = $200/mo); POs lag 2 months.
  Lifetime GP: academic sub $5.0k (life 33 mo) | commercial sub $30.5k (life 40 mo), incl. first tapeout service
  Acquisition: 19 contacts/mo (capped at distinct new teams) x 25% reply x 15% close = 0.71 outbound accounts/mo (+ inbound ramp to 1.2/mo)
  CAC: cash $0.4k/account; loaded with 16 founder h/mo @ $75/h = $2.0k/account -> LTV/CAC (blended 70% acad) 6.2x

4. SCENARIOS (bootstrap wedge only; month 1 = 2026-12; glut from m14 = 2028-01)
  BASE   DDR5 drop 10% -> commercial demand x0.97, commercial price x0.98, commercial churn x1.05
  GLUT   DDR5 drop 60% -> commercial demand x0.80, commercial price x0.91, commercial churn x1.30
  SEVERE DDR5 drop 90% -> commercial demand x0.70, commercial price x0.87, commercial churn x1.45
  All scenarios carry an expected-value free-release haircut from m24: weight 0.39 = GF180 share 0.65 x P(free GF180 macros) 0.6
  Outbound contacts capped at 19.0 distinct new teams/month; one-time spends gated at cash >= $2.5k.

5. MONTHLY P&L AND CASH - BASE (accounts are expected values)
  m    month    acad   com   svc   lic    rev A    rev B    rev C  revenue       GP    opex one-time      cash  FT
  1    2026-12   0.0   0.0  0.00  0.00    $0.0k    $0.0k    $0.0k    $0.0k    $0.0k   $0.8k    $9.1k    $30.1k   -
  2    2027-01   0.0   0.0  0.00  0.00    $0.0k    $0.0k    $0.0k    $0.0k    $0.0k   $0.8k    $3.0k    $26.2k   -
  3    2027-02   0.0   0.0  0.00  0.00    $0.0k    $0.0k    $0.0k    $0.0k    $0.0k   $0.8k    $9.0k    $16.4k   -
  4    2027-03   0.0   0.2  0.15  0.00    $0.1k    $1.5k    $0.0k    $1.6k    $0.9k   $0.8k    $3.8k    $12.6k   -
  5    2027-04   0.0   0.3  0.17  0.00    $0.3k    $1.7k    $0.0k    $2.0k    $1.1k   $0.8k    $0.0k    $12.9k   -
  6    2027-05   0.4   0.5  0.48  0.00    $0.5k    $2.7k    $0.0k    $3.2k    $1.7k   $0.8k    $3.0k    $10.7k   -
  7    2027-06   0.8   0.7  0.53  0.00    $0.7k    $3.1k    $0.0k    $3.8k    $2.0k   $0.8k    $0.0k    $11.8k   -
  8    2027-07   1.2   0.9  0.59  0.00    $0.9k    $3.4k    $0.0k    $4.3k    $2.3k   $0.8k    $0.0k    $13.2k   -
  9    2027-08   1.6   1.1  0.65  0.00    $1.2k    $3.7k    $0.0k    $4.9k    $2.6k   $0.8k    $4.0k    $11.0k   -
  10   2027-09   2.1   1.3  0.70  0.00    $1.4k    $4.0k    $0.0k    $5.4k    $3.0k   $0.8k    $0.0k    $13.1k   -
  11   2027-10   2.5   1.5  0.76  0.01    $1.7k    $4.3k    $0.1k    $6.1k    $3.3k   $1.1k    $8.5k     $6.8k   -
  12   2027-11   3.0   1.7  0.81  0.01    $1.9k    $4.6k    $0.1k    $6.7k    $3.7k   $1.1k    $0.0k     $9.4k   -
  13   2027-12   3.4   1.9  0.87  0.01    $2.2k    $4.9k    $0.1k    $7.2k    $4.0k   $1.1k    $0.0k    $12.4k   -
  14   2028-01   3.9   2.1  0.91  0.01    $2.4k    $5.1k    $0.2k    $7.6k    $4.3k   $1.1k    $0.0k    $15.5k   -
  15   2028-02   4.4   2.3  0.97  0.01    $2.7k    $5.4k    $0.2k    $8.2k    $4.6k   $1.1k   $15.0k     $4.0k   -
  16   2028-03   4.9   2.5  1.02  0.02    $2.9k    $5.6k    $0.2k    $8.7k    $4.9k   $1.1k    $0.0k     $7.8k   -
  17   2028-04   5.3   2.7  1.07  0.02    $3.2k    $5.9k    $0.2k    $9.3k    $5.3k   $1.1k    $7.2k     $4.7k   -
  18   2028-05   5.8   2.9  1.12  0.02    $3.4k    $6.2k    $0.2k    $9.8k    $5.6k   $1.1k    $0.0k     $9.2k   -
  19   2028-06   6.3   3.1  1.17  0.02    $3.7k    $6.5k    $0.2k   $10.4k    $5.9k   $1.1k    $0.0k    $14.1k   -
  20   2028-07   6.8   3.3  1.22  0.02    $4.0k    $6.7k    $0.2k   $10.9k    $6.3k   $1.1k    $0.0k    $19.2k   -
  21   2028-08   7.3   3.5  1.27  0.02    $4.2k    $7.0k    $0.3k   $11.5k    $6.6k   $1.1k    $0.0k    $24.7k   -
  22   2028-09   7.8   3.7  1.32  0.02    $4.5k    $7.3k    $0.3k   $12.0k    $6.9k   $1.1k    $0.0k    $30.5k   -
  23   2028-10   8.3   3.9  1.36  0.02    $4.7k    $7.5k    $0.3k   $12.5k    $7.2k   $1.1k    $0.0k    $36.6k   -
  24   2028-11   8.7   4.0  1.34  0.07    $4.5k    $7.1k    $0.8k   $12.5k    $7.0k   $1.1k   $17.0k    $25.6k   -
  25   2028-12   9.0   4.1  1.37  0.07    $4.6k    $7.2k    $0.9k   $12.7k    $7.2k   $1.1k    $0.0k    $31.7k   -
  26   2029-01   9.3   4.2  1.27  0.07    $4.7k    $7.0k    $0.9k   $12.6k    $7.2k   $1.1k    $0.0k    $37.8k   -
  27   2029-02   9.5   4.3  1.28  0.07    $4.8k    $7.0k    $0.9k   $12.7k    $7.3k   $1.1k   $15.0k    $29.0k   -
  28   2029-03   9.6   4.3  1.28  0.07    $4.9k    $7.1k    $0.9k   $12.9k    $7.4k   $1.1k    $0.0k    $35.3k   -
  29   2029-04   9.8   4.4  1.29  0.08    $5.0k    $7.1k    $0.9k   $13.0k    $7.5k   $1.1k    $0.0k    $41.6k   -
  30   2029-05  10.0   4.5  1.30  0.08    $5.1k    $7.1k    $0.9k   $13.1k    $7.6k   $1.1k    $0.0k    $48.1k   -
  31   2029-06  10.1   4.5  1.30  0.08    $5.2k    $7.2k    $0.9k   $13.3k    $7.6k   $1.1k    $0.0k    $54.6k   -
  32   2029-07  10.3   4.6  1.31  0.08    $5.2k    $7.2k    $0.9k   $13.4k    $7.7k   $1.1k    $0.0k    $61.2k   -
  33   2029-08  10.4   4.7  1.32  0.08    $5.3k    $7.3k    $0.9k   $13.5k    $7.8k   $1.1k    $0.0k    $67.9k   -
  34   2029-09  10.5   4.7  1.32  0.08    $5.4k    $7.3k    $0.9k   $13.6k    $7.9k   $1.1k    $0.0k    $74.7k   -
  35   2029-10  10.6   4.8  1.33  0.08    $5.4k    $7.3k    $0.9k   $13.7k    $7.9k   $1.1k    $0.0k    $81.5k   -
  36   2029-11  10.7   4.8  1.33  0.08    $5.5k    $7.4k    $0.9k   $13.8k    $8.0k   $1.1k    $0.0k    $88.4k   -

6. SCENARIO SUMMARY
  scen      1st rev   cash low    3-mo CF+ from       founder FT     GM (36 mo)    ARR m12    ARR m18    ARR m24    ARR m36   end cash
  BASE           m4  $4.0k@m15    m12 (2027-11)            never            57%     $23.1k     $41.2k     $54.0k     $65.7k     $88.4k
  GLUT           m4  $2.8k@m15    m12 (2027-11)            never            55%     $23.1k     $36.8k     $46.8k     $54.9k     $60.4k
  SEVERE         m4  $3.6k@m18    m12 (2027-11)            never            53%     $23.1k     $34.3k     $42.9k     $49.3k     $45.1k
  Characterized silicon after cash gate: GF180 m11 (2027-10); sky130 m24 (2028-11) / m24 (2028-11) / m27 (2029-02) (BASE/GLUT/SEVERE). Founder-paid GP month (GP >= $11.8k): never / never / never.
  ARR = subscription MRR x 12 (recurring only). Revenue run-rate (last 3 months x 4) incl. services/licenses:
  BASE    run-rate m12 $72.6k | m18 $111.5k | m24 $148.1k | m36 $164.1k | 36-mo revenue $316.9k | accounts at m36: 11 acad + 5 com
  GLUT    run-rate m12 $72.6k | m18 $98.3k | m24 $128.3k | m36 $137.9k | 36-mo revenue $278.6k | accounts at m36: 11 acad + 4 com
  SEVERE  run-rate m12 $72.6k | m18 $91.0k | m24 $115.7k | m36 $123.9k | 36-mo revenue $256.5k | accounts at m36: 11 acad + 3 com

7. SENSITIVITY (BASE scenario, one input at a time)
  case                       cash low    3-mo CF+ from       founder FT    ARR m18    ARR m36 rev m36 RR
  base                          $4.0k    m12 (2027-11)            never     $41.2k     $65.7k    $164.1k
  price x0.7                    $2.6k    m10 (2027-09)            never     $28.8k     $46.0k    $109.4k
  price x1.3                    $2.6k    m13 (2027-12)            never     $53.5k     $85.4k    $213.4k
  close rate x0.7               $3.4k    m13 (2027-12)            never     $29.6k     $49.1k    $124.4k
  close rate x1.3               $4.3k    m17 (2028-04)            never     $52.2k     $80.2k    $198.3k
  churn x0.7                    $4.4k    m12 (2027-11)            never     $43.0k     $74.3k    $178.0k
  churn x1.3                    $3.6k    m12 (2027-11)            never     $39.4k     $58.4k    $152.4k
  COGS x0.7                     $3.1k    m17 (2028-04)            never     $41.2k     $65.7k    $164.1k
  COGS x1.3                     $2.8k    m12 (2027-11)            never     $41.2k     $65.7k    $164.1k
  FREE-BUNDLE shock m18         $3.4k    m12 (2027-11)            never     $31.1k     $34.0k     $96.3k
  GLUT + free shock             $2.8k    m12 (2027-11)            never     $27.7k     $27.5k     $79.0k
  no free release at all        $4.0k    m12 (2027-11)            never     $41.2k     $86.1k    $203.7k
  close rate x0.5               $2.6k    m10 (2027-09)            never     $21.5k     $36.6k     $88.1k
  licences removed              $4.9k    m12 (2027-11)            never     $41.2k     $65.7k    $152.9k
  sky130 slot slips 6 mo        $4.0k     m5 (2027-04)            never     $41.2k     $65.7k    $164.1k
  price+close x1.3,nofree        $6.1k    m12 (2027-11)    m22 (2028-09)     $67.8k    $135.6k    $317.0k
  academic share 0.80           $2.9k    m12 (2027-11)            never     $34.1k     $55.1k    $136.4k
  SEVERE + all adverse          $0.2k            never            never     $16.3k     $22.1k     $55.3k

8. WHAT MUST BE TRUE
  To pay the founder full-time ($10k/mo) + FT opex from gross profit needs $11.8k GP/month.
  At the base mix one active account yields $0.4k GP/mo (academic $0.2k, commercial $1.1k).
  => ~27 active paying accounts (~19 academic + 8 commercial) by month 18; model has 5.8 + 2.9 = 8.7 at m18.
  => that is 48% of the whole wedge cap (55 accounts) - i.e. near-total share of a tiny market.
  Equivalently (no subscriptions): 2.3 commercial tapeout services/mo or 2.0 licenses/mo.
  Best revised BASE month: GP $8.0k at m36 vs $11.8k needed -> the founder is not paid inside 36 months in any scenario.
  Kill line for the 30-day experiment: >=3 paid pre-orders (>=$2k each) or >=$15k in signed LOIs from >=100 distinct funded teams,
  plus extracted-SPICE corner + 1,000-pt Monte Carlo pass on a 16KB macro, plus written no-free-release statements (UCSC, OCD).

9. PATH TO T2 (gain-cell + ReRAM macros) - KILLED in Phase 5; printed for reference only
  Killed by RT-VC-DD5-02, RT-HYP-DD5-07, RT-PHY-DD5-03/04/05, RT-VET-DD5-03/05: no named buyer; a logic-rule sky130 gain cell
  is unlikely to beat the pushed-rule 1.896 um2 6T; no leakage case at 130nm; magnet immunity is shared by OTP/eFuse and
  S130's own eNVM options; JESD47 needs ~3 lots (qual line now $1,000.0k). Not part of any revised verdict or headline.
  m6-m9    STTR Phase I proposal with university PI (e.g. UCSC OpenRAM / Stanford OpenGCRAM group)          -  founder time
  m15      STTR Phase I award: sky130 gain-cell macro + test chip                                $305.0k  NSF/DoD STTR
  m15-m21    of which >=30% to university; 2 ChipFoundry sky130 spins                             $30.0k  inside Phase I
  m18      ReRAM probe: Cadence SKY130 MPW block with Weebit ReRAM option                         $12.0k  Phase I / cash
  m18-m24  Weebit evaluation/licence (first-ever fee anchor; startup fee unknown)                $100.0k  seed or Phase II
  m30      STTR Phase II: characterization, compiler, reliability                              $1,500.0k  NSF/DoD STTR
  m27-m30  Seed round, conditional on >=$250k ARR wedge + gain-cell silicon                    $2,500.0k  VC / strategic (SkyWater/IonQ?)
  m30-m48  Full-time circuit cofounder (2 yrs loaded)                                            $440.0k  seed
  m36-m54  ReRAM secure-NVM chiplet: S130 mask set + JEDEC qual + packaging                    $1,550.0k  seed / Phase II / DoD
  Total external capital to reach a qualified macro: ~$4,305.0k (T2). Product revenue from gain-cell/ReRAM before m36: at most 1 gain-cell eval licence(s).
  BASE + T2 overlay (STTR fees, ReRAM MPW block, 1 gain-cell eval licence @ $75.0k, seed $2,500.0k at m28, cofounder + Weebit fee):
    36-mo revenue $391.9k (wedge $316.9k + T2 $75.0k) | end cash $2,509.1k, of which seed $2,500.0k -> operating cash excl. seed $9.1k (vs BASE wedge $88.4k).

10. HEADLINE (Phase 5 revised; T2 killed)
  36-mo gross margin 57% (base). Cash-flow breakeven (first of 3 cash-positive months) m12 (2027-11); founder can go full-time never.
  Recurring ARR m18 / m36: BASE $41.2k / $65.7k | GLUT $36.8k / $54.9k | SEVERE $34.3k / $49.3k
  Revenue run-rate m18 / m36: BASE $111.5k / $164.1k | GLUT $98.3k / $137.9k | SEVERE $91.0k / $123.9k
  Cash low point BASE $4.0k at m15 (starting from $40.0k).

INPUTS (value | source)
  start_cash                                           40000 | ASSUMPTIONS.md A-03 ($40k deployable)
  months                                               36 | Mission: 36-month hard ceiling for PRIMARY (ASSUMPTIONS A-12)
  month1                                               (2026, 12) | ESTIMATE: month 1 = Dec-2026 (study date 2026-11-01)
  founder_ft_salary_month                              10000 | ASSUMPTIONS.md A-03 (~$120k/yr loaded once revenue covers it)
  ft_cash_buffer                                       25000 | ESTIMATE: founder quits day job only with >=$25k cash on hand
  glut_start_month                                     14 | ASSUMPTIONS A-05 glut from 2028-Q1; month 14 = Jan-2028
  tinytapeout_projects_2026_sky_ihp_gf                 899 | https://github.com/TinyTapeout/tinytapeout-sky-26a (289), -sky-26b (275), -ihp-26a (283), -gf-0p2 (52): git tree counts 2026-11-01; tiles are a funnel, not macro buyers
  wafer_space_slots_per_run                            54 | https://github.com/wafer-space/ws-run2 (G802: 54 slots; Run 1 G801: 40)
  wafer_space_runs_per_year                            2 | ESTIMATE: Run 1 wafers May-2026, Run 2 Jul-2026 tapeout, Run 3 'coming soon' (crowdsupply.com/wafer-space)
  chipfoundry_sky130_projects_per_year                 30 | RED-TEAM Phase 5 (RT-VC-DD5-01): 60 -> 30; the Phase 4 input note itself says 2-3 shuttles/yr at >=50% fill = ~20-30 paid slots; Efabless chipIgnite peaked at ~43/yr (80 commercial + 50 university designs over ~3 yrs) with subsidised demand | Phase 4 source: ESTIMATE: 2-3 ChipFoundry shuttles/yr at >=50% fill (eeNews) ~20-30 paid slots; Efabless chipIgnite did 80 commercial designs + 50 universities over ~3 yrs (eejournal)
  cadence_sky130_mpw_projects_per_year                 20 | RED-TEAM Phase 5 (RT-VC-DD5-01): 30 -> 20; only one 2026 Cadence SKY130 run is documented (deadline 2026-01-16); 'multiple runs per year' is a plan, not a count | Phase 4 source: ESTIMATE: Cadence SKY130 aggregation, $10-12k/block, 'multiple runs per year' (skywatertechnology.com Cadence MPW page, via snippet)
  gf_university_pilot_projects_per_year                40 | https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms (40 universities, GF180MCU)
  mosis2_commons_other_projects_per_year               30 | RED-TEAM Phase 5 (RT-VC-DD5-01): 60 -> 30; MOSIS 2.0 and the Commons publish no counts of full-chip open-PDK projects; halved for lack of any count | Phase 4 source: ESTIMATE: MOSIS 2.0 (>35 MPW shuttles, isi.edu 2026) + Microelectronics Commons hubs (>61,000 chips, nstxl.org 2026-03) full-chip projects on U.S. trailing nodes
  share_projects_needing_memory_beyond_free_macros     0.3 | ESTIMATE: wafer.space Run 2 listing - ~10 of 51 projects mention SRAM/RAM (git README 2026-10-17); full SoCs need >4KB (sky130) / >1KB (GF180) which no free macro covers
  share_of_those_that_pay                              0.4 | ESTIMATE: hobby/student projects use free OpenRAM/OCD/DFFRAM; funded labs, startups, SBIR teams pay to de-risk a $7-15k slot
  avg_active_years_per_paying_group                    2.0 | ESTIMATE: labs/startups tape out repeatedly over a 2-3 yr grant/funding cycle
  academic_share_of_accounts                           0.7 | RED-TEAM Phase 5 (RT-HYP-DD5-03; RT-VC-DD5-05): 0.6 -> 0.7; named commercial targets are microfirms (Avalon, Cloneless, Tillitis/Zedulo); funded SBIR teams going to production move to the S130 NDA PDK with SkyWater's bundled compilers; 0.80 is run as a sensitivity | Phase 4 source: ESTIMATE: wafer.space/TT listings dominated by universities and hobbyists; commercial minority
  price_sub_academic_month                             200 | ESTIMATE: $2.4k/yr, <25% of one $7-15k shuttle slot (ChipFoundry $15k/100 chips; wafer.space ~$7k/1,000 dies)
  price_sub_commercial_month                           800 | ESTIMATE: $9.6k/yr, < one contract-engineer week; far below commercial compiler licences (Virage 0.18um from $300k list, 2001: designworldonline.com)
  price_tapeout_service_academic                       3000 | ESTIMATE: ~20-40% of a $7.5-15k MPW slot
  price_tapeout_service_commercial                     10000 | ESTIMATE: ~65-100% of a $10-15k MPW slot; buyer is de-risking the whole tapeout
  price_characterized_macro_license                    12000 | RED-TEAM Phase 5 (RT-HYP-DD5-02; RT-PHY-DD5-01; RT-VET-DD5-02; RT-VC-DD5-06): 20000 -> 12000; licence restated as 'one nominal MPW lot measured at voltage/temperature points (rented thermal forcing), process corners simulated and correlated to that lot, yield on >=50 die, warranty = re-delivery or refund of fees'; priced at 1.2x the commercial service fee [ESTIMATE] | Phase 4 source: ESTIMATE: per design, 12-mo support + warranty; anchors: Weebit first-ever eNVM licence ~US$0.1M (MST Access), foundry-sponsored compilers free to NDA-PDK customers (Artisan model, design-reuse.com)
  contract_vlsi_rate_per_hour                          150 | RED-TEAM Phase 5 (RT-VC-DD5-03): 125 -> 150; retainer premium for a memory contractor who signs a 12-month exclusivity / non-compete on publishing free characterized >=16 KB sky130 macros [ESTIMATE: +20%] | Phase 4 source: ESTIMATE: U.S. freelance analog/memory layout & characterization engineer
  hosting_per_account_month                            15 | ESTIMATE: cloud CPU for OpenRAM/ngspice/Xyce runs per active account
  support_hours_academic_month                         0.3 | ESTIMATE
  support_hours_commercial_month                       0.5 | ESTIMATE
  service_contract_hours_academic                      12 | ESTIMATE: macro generation + DRC/LVS + integration review
  service_contract_hours_commercial                    30 | ESTIMATE: custom configuration + timing sign-off + integration
  service_compute_per_job                              100 | ESTIMATE
  license_contract_hours                               30 | ESTIMATE: delivery, PVT corner check, 12-mo support
  license_warranty_reserve_share                       0.1 | ESTIMATE: reserve for re-spin support
  payment_processing_share                             0.03 | ESTIMATE: card/ACH + invoicing
  outreach_contacts_month_parttime                     30 | ESTIMATE: ~4 h/week of the founder's 15 h (A-03)
  outreach_contacts_month_fulltime                     60 | ESTIMATE
  reply_rate                                           0.25 | ESTIMATE: warm, named technical outreach to public tapeout teams (wafer.space/TT repos list owners)
  close_rate_of_replies                                0.15 | ESTIMATE: no paid demand found yet (C-33 verify: WTP STILL-UNVERIFIED) - the kill experiment measures this
  inbound_start_month                                  4 | ESTIMATE: after public launch of macro library on GitHub/PyPI
  inbound_accounts_added_per_month_per_month           0.06 | ESTIMATE
  inbound_accounts_max_per_month                       1.2 | ESTIMATE
  subscription_attach_rate                             0.7 | ESTIMATE
  first_tapeout_service_prob_academic                  0.5 | ESTIMATE
  first_tapeout_service_prob_commercial                0.6 | ESTIMATE
  tapeouts_per_year_academic_group                     1.0 | ESTIMATE: course/lab cadence
  tapeouts_per_year_commercial                         1.5 | ESTIMATE: 1-2 MPW spins per year
  repeat_service_attach                                0.5 | ESTIMATE
  licenses_per_commercial_account_year                 0.15 | RED-TEAM Phase 5 (RT-HYP-DD5-02; RT-PHY-DD5-01; RT-VET-DD5-02): 0.25 -> 0.15; without skew-corner data the licence's edge over free simulated OpenRAM corners is smaller, so fewer commercial teams buy it [ESTIMATE] | Phase 4 source: ESTIMATE
  dod_sbir_license_channel_per_month                   0.04 | RED-TEAM Phase 5 (RT-PHY-DD5-07; RT-VET-DD5-04; RT-HYP-DD5-05): 0.08 -> 0.04; DoD/SBIR buyers usually need SEE/TID data the plan will not fund, and the U.S.-fab axis covers only sky130 (wafer.space Run 3 page: GF180MCU chips fabricated at GF in Singapore) | Phase 4 source: ESTIMATE: ~1/yr; precedent Sandia licensed Mobile Semiconductor 180nm compilers (design-reuse.com)
  churn_academic_month                                 0.03 | ESTIMATE: students graduate, grants end
  churn_commercial_month                               0.025 | ESTIMATE: startups die or move to NDA PDK + foundry compiler
  services_start_month                                 4 | ESTIMATE: simulated (pre-silicon) macros sellable after 3 months of build-out, timed to the next ChipFoundry/wafer.space deadline
  gf180_characterized_month                            11 | RED-TEAM Phase 5 (RT-VC-DD5-04): 10 -> 11; wafer.space Run 3 dates are unpublished; one month of slack on the m4 GF180 slot | Phase 4 source: ESTIMATE: wafer.space slot m4 + ~12 wk fab (Run 1: 12 weeks at GF) + packaging/test
  sky130_characterized_month                           16 | RED-TEAM Phase 5 (RT-VET-DD5-06; RT-VC-DD5-04): 13 -> 16; TTSKY25b on ChipFoundry CI2511: submissions closed 2025-11-10, chips expected Jul-2026 (~8 months), plus ~1 month on the bench; ChipFoundry moves an under-filled run to the next shuttle | Phase 4 source: ESTIMATE: ChipFoundry slot m7 + ~6-month SkyWater turn (Cadence MPW: Jan submit -> Jul die)
  opex_fixed_month                                     600 | ESTIMATE: hosting base $150 + software/domain $100 + accounting/legal $350
  e_and_o_insurance_month_after_first_license          250 | ESTIMATE
  marketing_travel_month_parttime                      250 | ESTIMATE: FSiC/ORConf-type community events remote; small ads
  marketing_travel_month_fulltime                      1000 | ESTIMATE: DAC/GOMACTech travel, hub events
  one_time_spends                                      m1 company formation + templates $1,000; m2 contract VLSI build-out 20h $2,500; m3 contract VLSI build-out 40h $5,000; m4 wafer.space GF180 half slot (test macros) $3,750; m7 ChipFoundry sky130 slot (test macros) $15,000; m9 test bench: FPGA carrier + PCB + bench time $4,000; m10 GF180 characterization contractor 40h $5,000; m13 sky130 characterization contractor 40h $5,000; m16 wafer.space GF180 full slot: 8-32KB macros $7,250; m19 ChipFoundry sky130 slot: 16-64KB macros $15,000; m24 characterization contractor 40h $5,000 | SUPERSEDED in Phase 5 by one_time_spend_items (the model no longer reads this dict) | ESTIMATE; slot prices: ChipFoundry ~$15k/100 chips (eeNews), wafer.space ~$7-7.5k per full slot/1,000 dies (crowdsupply Run 2), half slot = 1/2
  commercial_demand_elasticity_to_ddr5_drop            0.33 | ESTIMATE: on-chip macros are priced per design, not per GB; a DRAM glut hits startup/tapeout budgets only through the semiconductor cycle - assume 1/3 pass-through
  commercial_price_elasticity_to_ddr5_drop             0.15 | ESTIMATE
  commercial_churn_elasticity_to_ddr5_drop             0.5 | ESTIMATE
  base_2028_ddr5_asp_drop                              0.1 | 01_LANDSCAPE.md s1 row 4b (BofA -10% ASP 2028, REPORTED)
  sky130_6t_bitcell_um2                                1.896 | https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram (1.200 x 1.580 um, VERIFIED)
  sky130_openram_1kb_macro_mm2                         0.19071255 | https://github.com/efabless/sky130_sram_macros (32x256 LEF 479.78 x 397.5 um)
  sky130_openram_2kb_macro_mm2                         0.28453847400000004 | https://github.com/VLSIDA/sky130_sram_macros (683.1 x 416.54 um)
  gf180_ocd_1kb_macro_mm2                              0.155413553 | https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram (1024x8 LEF 301.3 x 515.81 um)
  gf180_gf_512b_macro_mm2                              0.2094002768 | https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram (512x8 LEF)
  large_macro_array_efficiency                         0.3 | RED-TEAM Phase 5 (RT-PHY-DD5-06): 0.6 -> 0.3; no OpenRAM evidence for 60%; going from the 1 KB to the 2 KB OpenRAM sky130 macro adds 11.4 um2 per added bit (6x the 1.896 um2 bitcell), so OpenRAM's periphery does not amortise like a commercial compiler's; 30% until the day 1-7 run measures a 32 KB macro | Phase 4 source: ESTIMATE: banked 32-64KB macro; typical commercial compiler 0.6-0.75
  gain_cell_bitcell_area_saving_65nm_silicon           (0.2, 0.3) | https://cris.biu.ac.il/en/publications/4t-gain-cell-providing-unlimited-availability-through-hidden-refr/ (Teman group 16-kbit 65nm macros: up to 20% (2021) / 30% (2024) vs SRAM)
  gain_cell_area_saving_vendor_claim                   (0.4, 0.5) | https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/ (~40%); OpenGCRAM citing RAAAM up to 50% (arxiv 2507.10849)
  sram_silicon_sky130_usd_per_gb                       1330 | 01_LANDSCAPE.md s4.4 (cost_stack.md s8.5, ESTIMATE)
  sttr_phase1_usd                                      305000 | NSF 26-510 Phase I up to $305k (grantedai.com summary; 01_LANDSCAPE s7: NSF Phase I $305k)
  sttr_phase1_award_month                              15 | ESTIMATE: submit m6-m9 with university PI, ~6-month review
  sttr_min_research_institution_share                  0.3 | STTR rule: >=30% to the research institution (SBA policy, UNVERIFIED this session)
  sttr_allowed_fee_share                               0.07 | ESTIMATE: typical 7% fee on SBIR/STTR awards
  sttr_phase2_usd                                      1500000 | ESTIMATE within ~$2.15M Phase II guideline (01_LANDSCAPE s7)
  sttr_phase2_award_month                              30 | ESTIMATE: Phase I 12 mo + ~3-mo review
  gain_cell_eval_license_usd                           75000 | ESTIMATE: below Weebit first-ever ~US$0.1M fee (MST Access) - a zero-heritage entrant
  gain_cell_eval_license_months                        (34,) | ESTIMATE: one eval licence after sky130 gain-cell silicon (m21-m27) and characterization; buyer = a trusted-ASIC team on SkyWater
  seed_round_usd                                       2500000 | ESTIMATE: T2 seed for a memory-IP startup; conditional on wedge traction + gain-cell silicon
  seed_round_month                                     28 | ESTIMATE
  free_bundle_shock                                    {'month': 18, 'close': 0.5, 'churn': 2.0, 'sub_price': 0.8, 'lic': 0.5} | ESTIMATE: ChipFoundry/Cadence/UCSC/OCD ship free characterized >=16KB macros (C-33 fatal flaw); halves close rate and licences, doubles churn, -20% sub price
  cadence_sky130_reram_block_usd                       12000 | https://www.skywatertechnology.com/lowering-barriers-to-silicon-cadence-launches-mpw-aggregation-service-for-sky130/ ($10-12k; upper end = ReRAM option, via snippet)
  weebit_first_ever_license_fee_usd                    100000 | MST Access report via 01_LANDSCAPE s9 (~US$0.1M first-ever licence; fabless-startup fee unknown)
  s130_production_mask_set_usd                         550000 | 01_LANDSCAPE s6 (130nm full mask set $500-600k, AnySilicon)
  jedec_qual_and_packaging_usd                         1000000 | RED-TEAM Phase 5 (RT-VET-DD5-05): 400000 -> 1000000; JESD47 needs HTOL 1,000 h on 3 lots x 77 units plus retention bakes, ESD/latch-up and MSL on a production S130+ReRAM flow: three engineering lots plus a qual house, not one lot [ESTIMATE]; T2 is killed, so this is reference only | Phase 4 source: C-22 verify_corrections (~$0.3-0.5M)
  circuit_cofounder_loaded_year                        220000 | ESTIMATE: U.S. memory/mixed-signal designer, loaded
  outreach_capped_at_distinct_teams_per_month          True | RED-TEAM Phase 5 (RT-HYP-DD5-01): False -> True; outbound contacts/month capped at distinct new project teams = full-chip projects per year / 12; the 120-name list is spent in the m0 kill test, and full-time work adds no fresh names | Phase 4 source: Phase 4: outbound contacts/month not capped by the number of distinct project teams
  academic_procurement_lag_months                      2 | RED-TEAM Phase 5 (RT-HYP-DD5-06): 0 -> 2; university vendor registration and POs add 30-90 days (DD4 s7); the academic offer becomes a per-term course pack at the same $1.2k/term | Phase 4 source: Phase 4: academic accounts pay in the month they are won
  prob_free_characterized_gf180_macros_by_partial_month 0.6 | RED-TEAM Phase 5 (RT-HYP-DD5-04; RT-VC-DD5-01): 0.0 -> 0.6; OCD (last commit 2026-10-30) and Chips4Makers (3 GF180 SRAM test chips, Jul-2026) already have silicon, and DD s5 says GF180 is probably lost within 12 months; the haircut weight is GF180 share of projects x 0.6, applied from m24 to close rate, churn, subscription price and licences through the free_bundle_shock parameters | Phase 4 source: Phase 4: a free release appears only as a sensitivity case (free_bundle_shock)
  partial_free_release_month                           24 | ESTIMATE: month from which the expected-value free-release haircut applies (Nov-2028)
  one_time_spend_items                                 m1 company formation + licence/warranty templates $1,000; m1 kill-test spend not elsewhere in model: 40 h extracted-SPICE + 1,000-pt bitcell Monte Carlo review, compute, web, outreach, hub event $8,100; m2 contract VLSI build-out 20h $3,000; m3 contract VLSI build-out 40h $6,000; m3 GF180 test chip: on-chip BIST + programmable delay-line / ring-oscillator timing structures 20h $3,000; m4 wafer.space GF180 half slot (test macros + BIST) $3,750; m6 sky130 test chip: on-chip BIST + delay-line timing structures 20h $3,000; m7 ChipFoundry sky130 slot (test macros) $15,000; m9 test bench: FPGA carrier + PCB + bench time $4,000; m11 GF180 characterization contractor 40h $6,000; m11 GF180 thermal-forcing rental (-40/125C, ~1 week) $2,500; m16 wafer.space GF180 full slot: 8-32KB macros $7,250; m16 sky130 characterization contractor 40h $6,000; m16 sky130 thermal-forcing rental (-40/125C, ~1 week) $2,500; m19 ChipFoundry sky130 slot: 16-64KB macros $15,000; m24 characterization contractor 40h $6,000; m24 thermal-forcing rental $2,500 | RED-TEAM Phase 5 (RT-VET-DD5-01; RT-PHY-DD5-02; RT-VET-DD5-02; RT-VC-DD5-03): 11 items, $68,500 total -> 17 items, $94,600 total; adds test structures that make ns access time measurable, thermal forcing for -40/125C [ESTIMATE: ThermoStream-class rental ~$2-4k/week], the stronger kill-test gate (kill test now ~$9.1k, of which $1k template is the m1 item), and moves characterization to m11/m16 | Phase 4 source: Phase 4 one-time spends (identical to one_time_spends); items whose label contains 'sky130' shift in the slip case
  cash_gate_floor_usd                                  2500 | RED-TEAM Phase 5 (RT-PHY-DD5-02; RT-VET-DD5-02; RT-VC-DD5-04 (consequence)): None -> 2500; the added spends push BASE cash to -$8.2k at m11 on the Phase 4 schedule, beyond the $40k deployable (A-03); deferrable spends (test chips, slots, bench, characterization) now wait until cash after the spend stays >= $2.5k, and the characterized month moves with them | Phase 4 source: Phase 4: no gate in the model (the DD text gated the m7 slot on cash >= $30k, but the model paid every spend on schedule)
```
