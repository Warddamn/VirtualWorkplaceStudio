# DD5 Open Memory IP: model output

Captured stdout of `python3 models/open-memory-ip.py` (run 2026-11-01 from the repo root, exit 0). Agent `p4-open-memory-ip`. Notes: `research/phase4/open-memory-ip_notes.md`.

```text
============================================================================================================
DD5 U.S. OPEN MEMORY IP - unit economics & 36-month P&L (models/open-memory-ip.py, as of 2026-11-01)
============================================================================================================
DDR5 reference source: models/dram_cost_stack.py ddr5_reference()
  incumbent cost $1.48/GB | Q4-26 contract $20.37/GB | glut $8.15/GB | severe $2.04/GB

1. WHY THE AXIS IS NOT $/GB (density and $/GB context)
  sky130 6T bitcell limit                      527.4 kbit/mm2  (1.896 um2 cell)
  sky130 OpenRAM 1KB / 2KB macros (largest)     43.0 /  57.6 kbit/mm2
  sky130 banked 32-64KB macro @60% array eff   316.5 kbit/mm2  -> 5.5x the 2KB macro (compiler work, no new cell)
  GF180 open macros: GF 512B / OCD 1KB          19.6 /  52.7 kbit/mm2 (largest free GF180 macro = 1KB)
  Gain-cell density vs 6T: silicon (65nm, Teman) 1.25-1.43x; vendor claims (RAAAM/GF) 1.67-2.00x -> NOT the 2-4x in the hypothesis
  sky130 SRAM silicon ~$1330/GB vs DDR5: BASE $18.33/GB -> 73x | GLUT $8.15/GB -> 163x | SEVERE $2.04/GB -> 653x
  => macros are priced per design/tapeout, not per GB; the DDR5 cycle touches this only via design-start budgets.

2. MARKET SIZING (projects per year on U.S.-fab open/academic shuttles)
  Tiny Tapeout 2026 tiles (funnel only, not macro buyers): 899
  wafer.space 54 x 2 + ChipFoundry 60 + Cadence MPW 30 + GF univ pilot 40 + MOSIS2/Commons/other 60 = 298 full-chip projects/yr
  x need memory beyond free macros 30% x willing to pay 40% = 36 paying projects/yr
  active-account cap (x 2.0 yr groups): academic 43, commercial 29
  => serviceable revenue ceiling of the wedge at full share: $747.3k/yr (subscriptions + services + licenses)

3. UNIT ECONOMICS PER PRODUCT LINE (BASE prices)
  Product line                      Price       COGS       GM
  A1 Sub academic (/mo)              $200        $58      71%
  A2 Sub commercial (/mo)            $800       $102      87%
  B1 Tapeout svc academic          $3,000     $1,690      44%
  B2 Tapeout svc commercial       $10,000     $4,150      58%
  C  Characterized license        $20,000     $6,350      68%
  Lifetime GP: academic sub $5.4k (life 33 mo) | commercial sub $31.4k (life 40 mo), incl. first tapeout service
  Acquisition: 30 contacts/mo x 25% reply x 15% close = 1.12 outbound accounts/mo part-time (+ inbound ramp to 1.2/mo)
  CAC: cash $0.2k/account; loaded with 16 founder h/mo @ $75/h = $1.3k/account -> LTV/CAC (blended 60% acad) 12.3x

4. SCENARIOS (bootstrap wedge only; month 1 = 2026-12; glut from m14 = 2028-01)
  BASE   DDR5 drop 10% -> commercial demand x0.97, commercial price x0.98, commercial churn x1.05
  GLUT   DDR5 drop 60% -> commercial demand x0.80, commercial price x0.91, commercial churn x1.30
  SEVERE DDR5 drop 90% -> commercial demand x0.70, commercial price x0.87, commercial churn x1.45

5. MONTHLY P&L AND CASH - BASE (accounts are expected values)
  m    month    acad   com   svc   lic    rev A    rev B    rev C  revenue       GP    opex one-time      cash  FT
  1    2026-12   0.0   0.0  0.00  0.00    $0.0k    $0.0k    $0.0k    $0.0k    $0.0k   $0.8k    $1.0k    $38.1k   -
  2    2027-01   0.0   0.0  0.00  0.00    $0.0k    $0.0k    $0.0k    $0.0k    $0.0k   $0.8k    $2.5k    $34.8k   -
  3    2027-02   0.0   0.0  0.00  0.00    $0.0k    $0.0k    $0.0k    $0.0k    $0.0k   $0.8k    $5.0k    $28.9k   -
  4    2027-03   0.5   0.3  0.68  0.00    $0.4k    $4.2k    $0.0k    $4.5k    $2.6k   $0.8k    $3.8k    $26.9k   -
  5    2027-04   1.0   0.7  0.75  0.00    $0.7k    $4.6k    $0.0k    $5.3k    $3.1k   $0.8k    $0.0k    $29.2k   -
  6    2027-05   1.5   1.0  0.81  0.00    $1.1k    $5.0k    $0.0k    $6.1k    $3.7k   $0.8k    $0.0k    $32.0k   -
  7    2027-06   2.0   1.4  0.88  0.00    $1.5k    $5.4k    $0.0k    $6.9k    $4.2k   $0.8k   $15.0k    $20.4k   -
  8    2027-07   2.5   1.7  0.94  0.00    $1.9k    $5.9k    $0.0k    $7.7k    $4.7k   $0.8k    $0.0k    $24.2k   -
  9    2027-08   3.0   2.0  1.01  0.00    $2.2k    $6.3k    $0.0k    $8.5k    $5.3k   $0.8k    $4.0k    $24.7k   -
  10   2027-09   3.5   2.4  1.07  0.02    $2.6k    $6.7k    $0.5k    $9.8k    $6.2k   $1.1k    $5.0k    $24.7k   -
  11   2027-10   4.1   2.7  1.14  0.03    $3.0k    $7.1k    $0.6k   $10.7k    $6.8k   $1.1k    $0.0k    $30.4k   -
  12   2027-11   4.6   3.1  1.20  0.03    $3.4k    $7.5k    $0.6k   $11.5k    $7.3k   $1.1k    $0.0k    $36.6k   -
  13   2027-12   5.1   3.5  1.26  0.15    $3.8k    $7.9k    $3.0k   $14.7k    $9.5k   $1.1k    $5.0k    $40.1k   -
  14   2028-01   5.6   3.8  1.31  0.16    $4.1k    $8.0k    $3.1k   $15.2k    $9.8k   $1.1k    $0.0k    $48.8k   -
  15   2028-02   6.1   4.1  1.36  0.16    $4.5k    $8.4k    $3.2k   $16.1k   $10.4k   $1.1k    $0.0k    $58.1k   -
  16   2028-03   6.6   4.5  1.42  0.17    $4.8k    $8.8k    $3.4k   $17.0k   $11.0k   $1.1k    $7.2k    $60.8k   -
  17   2028-04   7.1   4.8  1.48  0.18    $5.2k    $9.1k    $3.5k   $17.8k   $11.6k   $1.1k    $0.0k    $71.3k   -
  18   2028-05   7.6   5.1  1.53  0.18    $5.6k    $9.5k    $3.6k   $18.7k   $12.2k   $1.1k    $0.0k    $82.4k   -
  19   2028-06   8.1   5.4  1.59  0.19    $5.9k    $9.8k    $3.8k   $19.5k   $12.8k   $1.1k   $15.0k    $79.1k   -
  20   2028-07   9.0   6.0  2.16  0.20    $6.5k   $13.3k    $4.0k   $23.8k   $15.3k  $11.8k    $0.0k    $82.5k   Y
  21   2028-08   9.8   6.6  2.22  0.21    $7.1k   $13.7k    $4.2k   $25.0k   $16.2k  $11.8k    $0.0k    $86.8k   Y
  22   2028-09  10.6   7.1  2.28  0.23    $7.7k   $14.0k    $4.4k   $26.2k   $17.0k  $11.8k    $0.0k    $92.0k   Y
  23   2028-10  11.4   7.6  2.33  0.24    $8.3k   $14.4k    $4.7k   $27.3k   $17.8k  $11.8k    $0.0k    $97.9k   Y
  24   2028-11  12.1   8.1  2.36  0.25    $8.8k   $14.6k    $4.9k   $28.2k   $18.5k  $11.8k    $5.0k    $99.6k   Y
  25   2028-12  12.8   8.6  2.38  0.26    $9.3k   $14.8k    $5.0k   $29.1k   $19.1k  $11.8k    $0.0k   $106.8k   Y
  26   2029-01  13.4   9.0  2.41  0.26    $9.8k   $14.9k    $5.2k   $29.9k   $19.7k  $11.8k    $0.0k   $114.7k   Y
  27   2029-02  14.0   9.4  2.43  0.27   $10.2k   $15.1k    $5.4k   $30.7k   $20.3k  $11.8k    $0.0k   $123.1k   Y
  28   2029-03  14.6   9.8  2.45  0.28   $10.6k   $15.2k    $5.5k   $31.4k   $20.8k  $11.8k    $0.0k   $132.1k   Y
  29   2029-04  15.1  10.1  2.47  0.29   $11.0k   $15.4k    $5.7k   $32.1k   $21.3k  $11.8k    $0.0k   $141.5k   Y
  30   2029-05  15.6  10.5  2.49  0.30   $11.4k   $15.5k    $5.8k   $32.7k   $21.8k  $11.8k    $0.0k   $151.5k   Y
  31   2029-06  16.0  10.8  2.51  0.30   $11.7k   $15.6k    $6.0k   $33.3k   $22.2k  $11.8k    $0.0k   $161.8k   Y
  32   2029-07  16.5  11.1  2.53  0.31   $12.0k   $15.7k    $6.1k   $33.8k   $22.6k  $11.8k    $0.0k   $172.6k   Y
  33   2029-08  16.9  11.4  2.54  0.31   $12.3k   $15.9k    $6.2k   $34.4k   $23.0k  $11.8k    $0.0k   $183.7k   Y
  34   2029-09  17.2  11.6  2.56  0.32   $12.6k   $16.0k    $6.3k   $34.9k   $23.4k  $11.8k    $0.0k   $195.3k   Y
  35   2029-10  17.6  11.9  2.57  0.32   $12.9k   $16.1k    $6.4k   $35.3k   $23.7k  $11.8k    $0.0k   $207.1k   Y
  36   2029-11  17.9  12.1  2.58  0.33   $13.1k   $16.1k    $6.5k   $35.8k   $24.0k  $11.8k    $0.0k   $219.3k   Y

6. SCENARIO SUMMARY
  scen      1st rev   cash low    3-mo CF+ from       founder FT     GM (36 mo)    ARR m12    ARR m18    ARR m24    ARR m36   end cash
  BASE           m4  $20.4k@m7     m8 (2027-07)    m20 (2028-07)            66%     $40.7k     $66.6k    $105.7k    $157.6k    $219.3k
  GLUT           m4  $20.4k@m7     m8 (2027-07)    m25 (2028-12)            64%     $40.7k     $58.9k     $78.2k    $125.8k    $175.4k
  SEVERE         m4  $20.4k@m7     m8 (2027-07)    m30 (2029-05)            62%     $40.7k     $54.6k     $70.9k    $105.7k    $175.4k
  ARR = subscription MRR x 12 (recurring only). Revenue run-rate (last 3 months x 4) incl. services/licenses:
  BASE    run-rate m12 $127.9k | m18 $213.6k | m24 $327.0k | m36 $423.9k | 36-mo revenue $713.9k | accounts at m36: 18 acad + 12 com
  GLUT    run-rate m12 $127.9k | m18 $183.8k | m24 $229.0k | m36 $342.1k | 36-mo revenue $582.2k | accounts at m36: 17 acad + 10 com
  SEVERE  run-rate m12 $127.9k | m18 $167.1k | m24 $205.0k | m36 $291.2k | 36-mo revenue $506.6k | accounts at m36: 16 acad + 8 com

7. SENSITIVITY (BASE scenario, one input at a time)
  case                       cash low    3-mo CF+ from       founder FT    ARR m18    ARR m36 rev m36 RR
  base                         $20.4k     m8 (2027-07)    m20 (2028-07)     $66.6k    $157.6k    $423.9k
  price x0.7                   $10.5k    m20 (2028-07)            never     $46.6k     $88.5k    $238.8k
  price x1.3                   $27.0k     m8 (2027-07)    m15 (2028-02)    $102.9k    $211.7k    $563.8k
  close rate x0.7              $16.0k    m11 (2027-10)    m27 (2029-02)     $48.1k    $112.6k    $316.0k
  close rate x1.3              $24.3k     m8 (2027-07)    m16 (2028-03)     $95.8k    $191.8k    $504.6k
  churn x0.7                   $20.4k     m8 (2027-07)    m19 (2028-06)     $69.9k    $172.1k    $448.6k
  churn x1.3                   $20.3k    m11 (2027-10)    m21 (2028-08)     $63.6k    $144.8k    $402.2k
  COGS x0.7                    $23.0k     m8 (2027-07)    m17 (2028-04)     $73.2k    $160.9k    $430.0k
  COGS x1.3                    $17.7k    m11 (2027-10)    m23 (2028-10)     $66.6k    $153.8k    $416.8k
  FREE-BUNDLE shock m18        $20.4k     m8 (2027-07)            never     $49.5k     $50.0k    $154.4k
  GLUT + free shock            $20.4k     m8 (2027-07)            never     $43.7k     $39.1k    $122.1k
  SEVERE + all adverse        -$14.7k    m20 (2028-07)            never     $26.0k     $43.2k    $121.7k

8. WHAT MUST BE TRUE
  To pay the founder full-time ($10k/mo) + FT opex from gross profit needs $11.8k GP/month.
  At the base mix one active account yields $0.7k GP/mo (academic $0.2k, commercial $1.3k).
  => ~18 active paying accounts (~11 academic + 7 commercial) by month 18; model has 7.6 + 5.1 = 12.7 at m18.
  => that is 25% of the whole wedge cap (72 accounts) - i.e. near-total share of a tiny market.
  Equivalently (no subscriptions): 2.0 commercial tapeout services/mo or 0.9 licenses/mo.
  Kill line for the 30-day experiment: >=3 paid pre-orders (>=$2k each) or >=$15k in signed LOIs from the outreach list.

9. PATH TO T2 (gain-cell + ReRAM macros) - funding, not revenue (A-04)
  m6-m9    STTR Phase I proposal with university PI (e.g. UCSC OpenRAM / Stanford OpenGCRAM group)          -  founder time
  m15      STTR Phase I award: sky130 gain-cell macro + test chip                                $305.0k  NSF/DoD STTR
  m15-m21    of which >=30% to university; 2 ChipFoundry sky130 spins                             $30.0k  inside Phase I
  m18      ReRAM probe: Cadence SKY130 MPW block with Weebit ReRAM option                         $12.0k  Phase I / cash
  m18-m24  Weebit evaluation/licence (first-ever fee anchor; startup fee unknown)                $100.0k  seed or Phase II
  m30      STTR Phase II: characterization, compiler, reliability                              $1,500.0k  NSF/DoD STTR
  m27-m30  Seed round, conditional on >=$250k ARR wedge + gain-cell silicon                    $2,500.0k  VC / strategic (SkyWater/IonQ?)
  m30-m48  Full-time circuit cofounder (2 yrs loaded)                                            $440.0k  seed
  m36-m54  ReRAM secure-NVM chiplet: S130 mask set + JEDEC qual + packaging                      $950.0k  seed / Phase II / DoD
  Total external capital to reach a qualified macro: ~$4,305.0k (T2). Product revenue from gain-cell/ReRAM before m36: at most 1 gain-cell eval licence(s).
  BASE + T2 overlay (STTR fees, ReRAM MPW block, 1 gain-cell eval licence @ $75.0k, seed $2,500.0k at m28, cofounder + Weebit fee):
    36-mo revenue $788.9k (wedge $713.9k + T2 $75.0k) | end cash $2,661.6k, of which seed $2,500.0k -> operating cash excl. seed $161.6k (vs BASE wedge $219.3k).

10. HEADLINE
  36-mo gross margin 66% (base). Cash-flow breakeven (first of 3 cash-positive months) m8 (2027-07); founder can go full-time m20 (2028-07).
  Recurring ARR m18 / m36: BASE $66.6k / $157.6k | GLUT $58.9k / $125.8k | SEVERE $54.6k / $105.7k
  Revenue run-rate m18 / m36: BASE $213.6k / $423.9k | GLUT $183.8k / $342.1k | SEVERE $167.1k / $291.2k
  Cash low point BASE $20.4k at m7 (starting from $40.0k).

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
  chipfoundry_sky130_projects_per_year                 60 | ESTIMATE: 2-3 ChipFoundry shuttles/yr at >=50% fill (eeNews) ~20-30 paid slots; Efabless chipIgnite did 80 commercial designs + 50 universities over ~3 yrs (eejournal)
  cadence_sky130_mpw_projects_per_year                 30 | ESTIMATE: Cadence SKY130 aggregation, $10-12k/block, 'multiple runs per year' (skywatertechnology.com Cadence MPW page, via snippet)
  gf_university_pilot_projects_per_year                40 | https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms (40 universities, GF180MCU)
  mosis2_commons_other_projects_per_year               60 | ESTIMATE: MOSIS 2.0 (>35 MPW shuttles, isi.edu 2026) + Microelectronics Commons hubs (>61,000 chips, nstxl.org 2026-03) full-chip projects on U.S. trailing nodes
  share_projects_needing_memory_beyond_free_macros     0.3 | ESTIMATE: wafer.space Run 2 listing - ~10 of 51 projects mention SRAM/RAM (git README 2026-10-17); full SoCs need >4KB (sky130) / >1KB (GF180) which no free macro covers
  share_of_those_that_pay                              0.4 | ESTIMATE: hobby/student projects use free OpenRAM/OCD/DFFRAM; funded labs, startups, SBIR teams pay to de-risk a $7-15k slot
  avg_active_years_per_paying_group                    2.0 | ESTIMATE: labs/startups tape out repeatedly over a 2-3 yr grant/funding cycle
  academic_share_of_accounts                           0.6 | ESTIMATE: wafer.space/TT listings dominated by universities and hobbyists; commercial minority
  price_sub_academic_month                             200 | ESTIMATE: $2.4k/yr, <25% of one $7-15k shuttle slot (ChipFoundry $15k/100 chips; wafer.space ~$7k/1,000 dies)
  price_sub_commercial_month                           800 | ESTIMATE: $9.6k/yr, < one contract-engineer week; far below commercial compiler licences (Virage 0.18um from $300k list, 2001: designworldonline.com)
  price_tapeout_service_academic                       3000 | ESTIMATE: ~20-40% of a $7.5-15k MPW slot
  price_tapeout_service_commercial                     10000 | ESTIMATE: ~65-100% of a $10-15k MPW slot; buyer is de-risking the whole tapeout
  price_characterized_macro_license                    20000 | ESTIMATE: per design, 12-mo support + warranty; anchors: Weebit first-ever eNVM licence ~US$0.1M (MST Access), foundry-sponsored compilers free to NDA-PDK customers (Artisan model, design-reuse.com)
  contract_vlsi_rate_per_hour                          125 | ESTIMATE: U.S. freelance analog/memory layout & characterization engineer
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
  licenses_per_commercial_account_year                 0.25 | ESTIMATE
  dod_sbir_license_channel_per_month                   0.08 | ESTIMATE: ~1/yr; precedent Sandia licensed Mobile Semiconductor 180nm compilers (design-reuse.com)
  churn_academic_month                                 0.03 | ESTIMATE: students graduate, grants end
  churn_commercial_month                               0.025 | ESTIMATE: startups die or move to NDA PDK + foundry compiler
  services_start_month                                 4 | ESTIMATE: simulated (pre-silicon) macros sellable after 3 months of build-out, timed to the next ChipFoundry/wafer.space deadline
  gf180_characterized_month                            10 | ESTIMATE: wafer.space slot m4 + ~12 wk fab (Run 1: 12 weeks at GF) + packaging/test
  sky130_characterized_month                           13 | ESTIMATE: ChipFoundry slot m7 + ~6-month SkyWater turn (Cadence MPW: Jan submit -> Jul die)
  opex_fixed_month                                     600 | ESTIMATE: hosting base $150 + software/domain $100 + accounting/legal $350
  e_and_o_insurance_month_after_first_license          250 | ESTIMATE
  marketing_travel_month_parttime                      250 | ESTIMATE: FSiC/ORConf-type community events remote; small ads
  marketing_travel_month_fulltime                      1000 | ESTIMATE: DAC/GOMACTech travel, hub events
  one_time_spends                                      m1 company formation + templates $1,000; m2 contract VLSI build-out 20h $2,500; m3 contract VLSI build-out 40h $5,000; m4 wafer.space GF180 half slot (test macros) $3,750; m7 ChipFoundry sky130 slot (test macros) $15,000; m9 test bench: FPGA carrier + PCB + bench time $4,000; m10 GF180 characterization contractor 40h $5,000; m13 sky130 characterization contractor 40h $5,000; m16 wafer.space GF180 full slot: 8-32KB macros $7,250; m19 ChipFoundry sky130 slot: 16-64KB macros $15,000; m24 characterization contractor 40h $5,000 | ESTIMATE; slot prices: ChipFoundry ~$15k/100 chips (eeNews), wafer.space ~$7-7.5k per full slot/1,000 dies (crowdsupply Run 2), half slot = 1/2
  commercial_demand_elasticity_to_ddr5_drop            0.33 | ESTIMATE: on-chip macros are priced per design, not per GB; a DRAM glut hits startup/tapeout budgets only through the semiconductor cycle - assume 1/3 pass-through
  commercial_price_elasticity_to_ddr5_drop             0.15 | ESTIMATE
  commercial_churn_elasticity_to_ddr5_drop             0.5 | ESTIMATE
  base_2028_ddr5_asp_drop                              0.1 | 01_LANDSCAPE.md s1 row 4b (BofA -10% ASP 2028, REPORTED)
  sky130_6t_bitcell_um2                                1.896 | https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram (1.200 x 1.580 um, VERIFIED)
  sky130_openram_1kb_macro_mm2                         0.19071255 | https://github.com/efabless/sky130_sram_macros (32x256 LEF 479.78 x 397.5 um)
  sky130_openram_2kb_macro_mm2                         0.28453847400000004 | https://github.com/VLSIDA/sky130_sram_macros (683.1 x 416.54 um)
  gf180_ocd_1kb_macro_mm2                              0.155413553 | https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram (1024x8 LEF 301.3 x 515.81 um)
  gf180_gf_512b_macro_mm2                              0.2094002768 | https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram (512x8 LEF)
  large_macro_array_efficiency                         0.6 | ESTIMATE: banked 32-64KB macro; typical commercial compiler 0.6-0.75
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
  jedec_qual_and_packaging_usd                         400000 | C-22 verify_corrections (~$0.3-0.5M)
  circuit_cofounder_loaded_year                        220000 | ESTIMATE: U.S. memory/mixed-signal designer, loaded
```
