# DD3 nv-continuity-modules: model output

- **Model:** `models/nv-continuity-modules.py` (pure Python 3 stdlib; exit 0 on 2026-11-01)
- **Command:** `python3 models/nv-continuity-modules.py` from `/home/user/VirtualWorkplaceStudio/ram-venture`
- **DRAM reference:** imported from `models/dram_cost_stack.py` `ddr5_reference()`
- **Agent:** `p4-nv-continuity-modules`. Research notes: `research/phase4/nv-continuity-modules_notes.md`
- **Evidence grade:** every input has a URL or an `ESTIMATE: basis` (section [9]). Prices are search-snippet grade ([REPORTED]), because all WebFetch attempts failed DNS.

```text
====================================================================================================
DD3 nv-continuity-modules - unit economics, 36-month P&L (month 1 = 2026-11)
DRAM reference: models/dram_cost_stack.py ddr5_reference() (as_of 2026-11-01)
  Q4-2026 contract $20.37/GB | glut $8.15/GB | severe $2.04/GB | incumbent cost $1.48/GB
====================================================================================================

[1] UNIT ECONOMICS PER SKU (BASE; revenue blended over eBay / own store / reseller)
SKU                                 list  net rev/unit     COGS   GM  fees+CAC+ship+warr  contrib  contrib%
----------------------------------  ----  ------------  -------  ---  ------------------  -------  --------
NV-CARD 2MB (1x MR4A16B)            $249       $219.12   $85.50  61%              $33.67   $99.95       46%
NV-CARD 4MB (2x MR4A16B)            $349       $307.12  $131.50  57%              $40.73  $134.89       44%
NV-DIP 256Kb (FM18W08) DS1225/1230   $34        $32.64   $23.00  30%               $9.90   $-0.26       -1%
NV-DIP 1Mb (FM28V100) DS1245         $59        $56.64   $35.00  38%              $12.27    $9.37       17%
  MRAM per 2MB card = $42.00 of $85.50 COGS (49%); per-bit: MR4A16B $21504/GB vs DDR5 contract $20.37/GB
  L3 cloud: $29/shop/mo, COGS $3 -> GM 90% | L4 LTSA GM 50%

[2] CUSTOMER-ACQUISITION ASSUMPTIONS
line     channel mix (eBay/store/reseller)  CAC per store order  launch m  steady units/mo
-------  ---------------------------------  -------------------  --------  ---------------
NV-CARD                          25/35/40%                  $30         9               40
NV-DIP                           40/40/20%                   $6         4               50
CLOUD      6% attach of direct card buyers         $0 (bundled)        15    churn 2.5%/mo
LTSA                  direct (DMSMS / OEM)         founder time    27, 33    $2000/mo each

[3] DEMAND SIZING (TAM, ESTIMATE chain)
  Fanuc cumulative CNCs 5,000,000 x US 15% x legacy 35% x still running 50% = 131,250 U.S. legacy machines
  / 8 machines per shop = 16,406 shops; replacement every 8 yrs x 1.5 other families = 3,076 cards/yr U.S.; x4 global = 12,305/yr
  Base plan steady state 40 cards/mo = 480/yr = 4% of global, 16% of U.S. demand
  Whole global card market at blended $241/card = $2.97M/yr; U.S. = $741.7k/yr

[4] MONTHLY P&L AND CASH - BASE (founder part-time, no salary until trigger)
m     month  cards  DIPs  subs  revenue  gross  var+fixed  one-time  salary     net  inventory     cash
--  -------  -----  ----  ----  -------  -----  ---------  --------  ------  ------  ---------  -------
1   2026-11      0     0     0       $0     $0        $75      $800      $0   -$875       $148   $39.0k
2   2026-12      0     0     0       $0     $0        $75     $4.5k      $0  -$4.6k       $443   $34.1k
3   2027-01      0     0     0       $0     $0        $75     $3.0k      $0  -$3.1k      $5.3k   $26.2k
4   2027-02      0     6     0     $221    $74       $659     $5.5k      $0  -$6.1k      $5.2k   $20.2k
5   2027-03      0    11     0     $443   $147       $718     $1.5k      $0  -$2.1k      $4.9k   $18.4k
6   2027-04      0    17     0     $664   $221       $777        $0      $0   -$556     $11.9k   $10.8k
7   2027-05      0    22     0     $885   $294       $836        $0      $0   -$542     $11.3k   $10.9k
8   2027-06      0    28     0    $1.1k   $368       $895        $0      $0   -$527     $10.6k   $11.1k
9   2027-07      3    33     0    $2.1k   $922      $1.4k        $0      $0   -$450      $9.4k   $11.9k
10  2027-08      7    39     0    $3.2k  $1.5k      $1.5k        $0      $0    -$73      $7.7k   $13.4k
11  2027-09     10    44     0    $4.2k  $2.0k      $1.7k        $0      $0    $304      $8.8k   $12.6k
12  2027-10     13    50     0    $5.2k  $2.6k      $1.9k        $0      $0    $680      $9.8k   $12.3k
13  2027-11     17    50     0    $6.0k  $3.1k      $2.0k        $0      $0   $1.0k     $10.8k   $12.4k
14  2027-12     20    50     0    $6.8k  $3.5k      $2.1k        $0      $0   $1.4k     $11.8k   $12.9k
15  2028-01     23    50     1    $7.6k  $4.0k      $2.3k        $0      $0   $1.8k     $12.7k   $13.7k
16  2028-02     27    50     2    $8.5k  $4.6k      $2.4k        $0      $0   $2.2k     $13.7k   $14.9k
17  2028-03     30    50     3    $9.3k  $5.1k      $2.5k        $0      $0   $2.6k     $14.7k   $16.5k
18  2028-04     33    50     4   $10.1k  $5.6k      $2.6k        $0      $0   $3.0k     $15.3k   $18.8k
19  2028-05     37    50     5   $11.0k  $6.1k      $2.7k        $0      $0   $3.4k     $15.6k   $21.8k
20  2028-06     40    50     6   $11.8k  $6.6k      $2.8k        $0      $0   $3.7k     $15.6k   $25.6k
21  2028-07     40    50     8   $11.9k  $6.6k      $2.8k        $0      $0   $3.8k     $15.6k   $29.3k
22  2028-08     40    50     9   $11.9k  $6.7k      $2.8k        $0      $0   $3.8k     $15.6k   $33.1k
23  2028-09     40    50    10   $11.9k  $6.7k      $2.8k        $0      $0   $3.8k     $15.6k   $37.0k
24  2028-10     40    50    11   $12.0k  $6.7k      $2.8k        $0      $0   $3.9k     $15.6k   $40.9k
25  2028-11     40    50    13   $12.0k  $6.8k      $2.8k        $0      $0   $3.9k     $15.6k   $44.8k
26  2028-12     40    50    14   $12.0k  $6.8k      $2.8k        $0      $0   $3.9k     $15.6k   $48.7k
27  2029-01     40    50    15   $14.1k  $7.8k      $2.8k        $0      $0   $5.0k     $15.6k   $53.7k
28  2029-02     40    50    16   $14.1k  $7.8k      $2.8k        $0      $0   $5.0k     $15.6k   $58.7k
29  2029-03     40    50    17   $14.1k  $7.9k      $2.8k        $0      $0   $5.0k     $15.6k   $63.7k
30  2029-04     40    50    18   $14.2k  $7.9k      $2.8k        $0      $0   $5.0k     $15.6k   $68.7k
31  2029-05     40    50    19   $14.2k  $7.9k      $2.8k        $0      $0   $5.1k     $15.6k   $73.8k
32  2029-06     40    50    20   $14.2k  $7.9k      $2.8k        $0      $0   $5.1k     $15.6k   $78.9k
33  2029-07     40    50    21   $16.2k  $9.0k      $2.8k        $0      $0   $6.1k     $15.6k   $85.0k
34  2029-08     40    50    22   $16.3k  $9.0k      $2.8k        $0      $0   $6.1k     $15.6k   $91.2k
35  2029-09     40    50    23   $16.3k  $9.0k      $2.8k        $0      $0   $6.2k     $15.6k   $97.3k
36  2029-10     40    50    24   $16.3k  $9.0k      $2.8k        $0      $0   $6.2k     $15.6k  $103.5k

[4b] CASH CURVE BY SCENARIO (end of quarter; start $40k)
scenario      m3      m6      m9     m12     m15     m18     m21     m24     m27     m30     m33      m36
--------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  -------
BASE      $26.2k  $10.8k  $11.9k  $12.3k  $13.7k  $18.8k  $29.3k  $40.9k  $53.7k  $68.7k  $85.0k  $103.5k
GLUT      $26.4k  $11.6k  $12.4k  $13.6k  $15.3k  $20.7k  $31.4k  $42.9k  $55.7k  $70.6k  $86.7k  $104.9k
SEVERE    $26.7k  $12.3k  $12.5k  $13.5k  $13.7k  $16.7k  $23.9k  $31.9k  $40.8k  $51.7k  $63.6k   $77.4k

[5] SCENARIO SUMMARY (core lines L1-L4; PLP option excluded - see [7])
scenario  breakeven m     cash low  cash m36  full-time m  36-mo revenue  36-mo net  GM m36
--------  -----------  -----------  --------  -----------  -------------  ---------  ------
BASE               11  $10.8k (m6)   $103.5k        never        $310.9k     $79.1k     55%
GLUT               11  $11.6k (m6)   $104.9k        never        $295.3k     $79.0k     57%
SEVERE             12  $12.2k (m7)    $77.4k        never        $240.2k     $49.3k     55%

  ARR at months 12 / 18 / 24 / 36
scenario  run-rate m12      m18      m24      m36  recurring ARR m12    m18    m24     m36
--------  ------------  -------  -------  -------  -----------------  -----  -----  ------
BASE            $62.5k  $121.7k  $143.6k  $195.8k                 $0  $1.4k  $4.0k  $56.2k
GLUT            $59.4k  $115.6k  $136.4k  $186.0k                 $0  $1.3k  $3.8k  $53.4k
SEVERE          $47.8k   $93.1k  $109.9k  $153.9k                 $0  $1.1k  $3.0k  $47.1k
  run-rate = that month's revenue x 12 (hardware is repeat-purchase, not contracted).
  recurring ARR = (cloud MRR + LTSA monthly) x 12 = the only contracted/subscription revenue.
  DRAM $/GB used per scenario at m24: BASE $18.67, GLUT $8.15, SEVERE $2.04

[6] SENSITIVITY (BASE; one variable at a time, -30% / +30%)
case                                           breakeven m  cash low  run-rate m18  run-rate m36  rec. ARR m36  36-mo cum. net
---------------------------------------------  -----------  --------  ------------  ------------  ------------  --------------
baseline                                                11    $10.8k       $121.7k       $195.8k        $56.2k          $79.1k
price -30%                                              17      $577        $85.2k       $151.5k        $53.7k           $1.2k
price +30%                                               9    $11.2k       $158.2k       $240.2k        $58.6k         $157.1k
conversion/close -30%                                   12    $11.3k        $85.2k       $137.1k        $39.3k          $42.3k
conversion/close +30%                                   10    $10.2k       $158.2k       $254.6k        $73.0k         $116.0k
churn -30%                                              11    $10.8k       $121.7k       $196.4k        $56.8k          $79.5k
churn +30%                                              11    $10.8k       $121.7k       $195.3k        $55.6k          $78.8k
COGS -30%                                               10    $14.7k       $121.7k       $195.8k        $56.2k         $116.9k
COGS +30%                                               13     $3.7k       $121.7k       $195.8k        $56.2k          $41.4k
no LTSA/DMSMS contract                                  11    $10.8k       $121.7k       $147.8k         $8.2k          $65.1k
card launch +6 mo (MRAM lead/validation slip)           17     $6.0k        $62.9k       $194.4k        $54.8k          $52.5k

[6b] SCALE PATH BEYOND THE 'LOW-$100ks' CEILING (BASE market; overrides are ESTIMATES)
path                                                                     run-rate m36  rec. ARR m36  36-mo net  full-time m  share of global card TAM
-----------------------------------------------------------------------  ------------  ------------  ---------  -----------  ------------------------
S0 BASE (direct + 40% resellers, 2 LTSAs)                                     $195.8k        $56.2k     $79.1k        never                        4%
S1 + white-label in 3-4 MRO catalogs (cards x2, 65% reseller)                 $293.2k        $57.5k    $163.4k        never                        8%
S2 + DMSMS/OEM program (4 LTSAs, 2 at $4k/mo)                                 $291.8k       $152.2k    $110.1k        never                        4%
S3 + adjacent form factors (Q2MEM, robots, avionics, synth; cards x1.5)       $257.8k        $60.3k    $131.7k        never                        6%
S4 stretch: S1+S2+S3 combined (cards x3), cloud attach 15%                    $521.3k       $179.8k    $158.1k           22                       12%
  Even the stretch path needs ~12% of all PC-card SRAM replacement demand worldwide and stays well under $1M/yr.

[7] C-16 PLP OPTION - MRAM journal vs DRAM cache + supercaps (per board) and option value
scenario  DRAM $/GB (2028+)  MRAM 512MB cost  DRAM 2GB + caps saved  MRAM premium/board  p(paid design-in by m36)  option cost  EV gross profit   EV net  design-ins to break even
--------  -----------------  ---------------  ---------------------  ------------------  ------------------------  -----------  ---------------  -------  ------------------------
BASE                 $18.33             $410                    $49                $362                      0.32       $50.0k            $5.2k  -$44.8k                       3.1
GLUT                  $8.15             $410                    $28                $382                      0.19       $50.0k            $3.0k  -$47.0k                       3.1
SEVERE                $2.04             $410                    $16                $394                      0.11       $50.0k            $1.7k  -$48.3k                       3.1
  MRAM never wins on BOM; the DRAM glut moves the per-board gap by only ~$20-33. Buyers adopt for
  reliability (no supercap aging), so the kit's market is set by controller vendors, not price.
  ITC 337-TA-1487 target date 2027-08-16: exclusion risk applies to Everspin STT (1Gb, xSPI), not to Toggle MR4A16B.
  VERDICT: negative EV at T0 in every scenario -> defer C-16; run only a zero-cost interest test.

[8] WHAT MUST BE TRUE
  Contribution per card $109, per DIP $3; fixed opex at full launch $900/mo.
  (a) Part-time breakeven: 8 cards/mo (or 343 DIPs/mo) cover fixed opex. BASE at m18 sells 33 cards + 50 DIPs.
  (b) Founder full-time ($120k/yr): 100 cards/mo = 10% of estimated global card demand.
  (c) $0.5M/yr run-rate from cards alone: 173 cards/mo = 17% of global / 67% of U.S. demand.
  (d) Cumulative orders by m18 in BASE: 733 units (183 cards, 550 DIPs); reseller accounts needed: >=3 by m12.
  (e) Kill line: <15 paid pre-orders + <2 reseller LOIs in the 30-day test, or a Fanuc 16i/18i/21i or Mitsubishi Q CPU rejects the MRAM card (format/read/write).

[9] INPUTS (value | source)
  start_cash                           40000                        | ASSUMPTIONS.md A-03 ($40k deployable)
  months                               36                           | MISSION_PROMPT.md founder profile (36-month ceiling)
  founder_salary_monthly_fulltime      10000                        | ASSUMPTIONS.md A-03 (~$120k/yr loaded)
  fulltime_trigger_op_profit_monthly   12000                        | ESTIMATE: go full-time only when trailing-3-mo operating profit covers salary + 20% buffer
  dram_contract_q4_2026_usd_gb         20.37                        | models/dram_cost_stack.py ddr5_reference() (as_of 2026-11-01)
  dram_glut_usd_gb                     8.147                        | models/dram_cost_stack.py ddr5_reference() (as_of 2026-11-01)
  dram_severe_usd_gb                   2.037                        | models/dram_cost_stack.py ddr5_reference() (as_of 2026-11-01)
  dram_base_2028_decline               0.1                          | https://www.tmgm.com/en/analysis/market-insight/micron-dram-supply-tightening (BofA -10% ASP 2028, via 01_LANDSCAPE 1-4b)
  mr4a16b_usd_qty1                     46.03                        | https://www.digikey.com/en/products/detail/everspin-technologies-inc/MR4A16BYS35/4021237
  mr4a16b_usd_qty1000                  37.67                        | https://www.futureelectronics.com/p/memory--RAM--nvram/mr4a16bcys35r-everspin-technologies-6114651
  mr4a16b_usd_our_qty                  42                           | ESTIMATE: 100-500 pcs/yr sits between $37.67 @1k (Future) and $46.03 qty1 (DigiKey)
  mr4a16b_lead_weeks                   26                           | https://www.futureelectronics.com/p/memory--RAM--nvram/mr4a16bcys35r-everspin-technologies-6114651 (20-26 wk)
  fm18w08_usd_qty1                     12.87                        | https://azcus.digikey.com/en/products/detail/infineon-technologies/FM18W08-SG/4090358
  fm18w08_usd_our_qty                  11.5                         | ESTIMATE: ~10% below DigiKey qty-1 $12.87 at 100-pc breaks
  fm28v100_usd_our_qty                 19                           | https://www.futureelectronics.com/p/semiconductors--memory--RAM--nvram--fram-mram/fm28v100-tg-infineon-6750863 ($19.38 @2); findchips $17.7-25.9
  mram_1gb_stt_usd                     102.6                        | https://www.lcsc.com/product-image/C20342497.html ($102.60 @500, ~$821/GB)
  card_frame_kit_connector_usd         12                           | ESTIMATE: no small-qty price found; ITT StarCard kits exist (https://www.designnews.com/motion-control/itt-interconnect-solutions-snap-on-and-ultrasonic-pcmcia-i-o-card-kits); one 68-pos connector is Last Time Buy
  card_pcb_2mb_usd                     4.5                          | ESTIMATE: 0.8mm 4-layer, 100-pc offshore fab
  card_pcb_4mb_usd                     5.5                          | ESTIMATE: as above, larger
  card_logic_2mb_usd                   5                            | ESTIMATE: 3x 74LVC16245-class 5V-tolerant buffers + supervisor + attribute EEPROM + passives
  card_logic_4mb_usd                   6                            | ESTIMATE: as above + decode
  card_assembly_usd                    14                           | ESTIMATE: U.S. EMS at 100-pc lots; anecdote $415-1,300 per 10 turnkey boards (https://community.sparkfun.com/t/pcb-assembly-service/27265)
  card_assembly_4mb_usd                16                           | ESTIMATE: +1 BGA/TSOP placement
  card_setup_amort_usd                 4                            | ESTIMATE: ~$400 stencil/setup per 100-card lot (Screaming Circuits best at 25+: https://pic.hallikainen.org/piclist/2008/a/01/29/165504a.txt)
  card_test_pack_usd                   4                            | ESTIMATE: functional test on fixture, label, ESD bag, CoC
  card2_price_direct                   249                          | ESTIMATE anchored on Synchrotech 2MB battery card $239.39 (https://www.cdwg.com/product/synchrotech-sram-pcmcia-memory-pc-cards-replaceable-battery-flash-memory/5006798); used 2MB $160-440 eBay; Q2MEM-2MBSN $403.81 (https://www.ebay.de/itm/406086802130)
  card4_price_direct                   349                          | ESTIMATE: +$100 for second MRAM die; Memex lists 4MB unavailable (https://memex.ca/?p=596)
  card_reseller_discount               0.3                          | ESTIMATE: MRO reseller margin 30% (Memex/MRO Electric/DoSupply class)
  card_mix_4mb                         0.25                         | ESTIMATE: Fanuc formats to 4MB max per Memex; most backup jobs fit 1-2MB
  dip256_cogs_parts_other_usd          4                            | ESTIMATE: PCB $1.50 + machined round pins $2.50 (square pins damage sockets per https://www.pcbway.com/project/shareproject/Dallas_DS1230Y_DS1235YW_NVRAM_FRAM_Replacement_Adapter_79f70ace.html)
  dip256_assembly_test_usd             7.5                          | ESTIMATE: assembly $4 + setup $1.50 + test/pack $2
  dip1m_cogs_parts_other_usd           7.5                          | ESTIMATE: 5V-tolerant translators $2.50 + PCB $2 + pins $3
  dip1m_assembly_test_usd              8.5                          | ESTIMATE: assembly $5 + setup $1.50 + test/pack $2
  dip256_price_direct                  34                           | ESTIMATE vs DS1230Y-85 new $35-44 qty1 (https://findchips.com/search/DS1230Y-85?f=dsa) and Glitch Works battery DS1225 drop-in ~$30 (https://tindie.com/products/glitchwrks/glitch-works-gw-1225-1-dallas-ds1225-replacement)
  dip1m_price_direct                   59                           | ESTIMATE: DS1245 obsolete/NRND, broker-only (https://www.digipart.com/part/DS1245Y-85); no price found
  dip_reseller_discount                0.2                          | ESTIMATE: component reseller margin
  dip_mix_1m                           0.3                          | ESTIMATE
  ebay_fee_pct                         0.136                        | ESTIMATE: eBay final value fee ~13.6% most categories (not re-verified 2026)
  ebay_fee_fixed                       0.4                          | ESTIMATE: per-order fixed fee
  store_payment_pct                    0.029                        | ESTIMATE: card processing 2.9%
  store_payment_fixed                  0.3                          | ESTIMATE
  cac_store_card_order                 30                           | ESTIMATE: niche search terms ('fanuc sram card', 'Q2MEM-2MBS'); ~$1.5 CPC / 5% conv
  cac_store_dip_order                  6                            | ESTIMATE: mostly organic (forums, part-number search)
  ship_cost_card                       9                            | ESTIMATE: free USPS Priority on direct card orders
  ship_cost_dip                        5                            | ESTIMATE: free First-Class on direct DIP orders
  warranty_returns_pct                 0.03                         | ESTIMATE: 3% of revenue (compatibility returns)
  card_channel_mix                     {'ebay': 0.25, 'store': 0.35 | ESTIMATE: resellers matter because the buyer is a maintenance tech searching MRO catalogs
  dip_channel_mix                      {'ebay': 0.4, 'store': 0.4,  | ESTIMATE
  card_launch_month                    9                            | ESTIMATE: design m1-3, proto/validate m4-6, MRAM lead 20-26 wk ordered m3
  card_ramp_months                     12                           | ESTIMATE
  card_units_steady_month              40                           | ESTIMATE: ~5% of est. global ~10k/yr PC-card SRAM replacement demand (see TAM block)
  dip_launch_month                     4                            | ESTIMATE: FM18W08 in stock (~775 at DigiKey), 8-wk standard lead
  dip_ramp_months                      9                            | ESTIMATE
  dip_units_steady_month               50                           | ESTIMATE: free open adapters cap the hobby segment; sells on test report + warranty
  cloud_launch_month                   15                           | ESTIMATE: after cards are in the field
  cloud_price_month                    29                           | ESTIMATE: per shop; below DNC/MDC suites
  cloud_attach_rate                    0.06                         | ESTIMATE: 6% of direct card buyers subscribe
  cloud_churn_month                    0.025                        | ESTIMATE: SMB tool churn
  cloud_cogs_month                     3                            | ESTIMATE: hosting + support per sub
  ltsa_contracts                       [(27, 2000.0), (33, 2000.0)] | ESTIMATE: two $24k/yr blanket orders (start month, $/month); DLA buys 5962 memory by NSN via DIBBS (https://www.highergov.com/nsn/5962012622185/)
  ltsa_gm                              0.5                          | ESTIMATE: screened, traceable lots with CoC
  opex_tools_month                     75                           | ESTIMATE: domain, Shopify-class store, email
  opex_from_launch_month               225                          | ESTIMATE: product liability insurance ~$125 + bookkeeping ~$100
  opex_marketing_dip                   300                          | ESTIMATE: ads + samples from DIP launch
  opex_marketing_card                  300                          | ESTIMATE: extra ads + trade-forum presence from card launch
  one_time                             {1: 800.0, 2: 4500.0, 3: 300 | ESTIMATE: m1 LLC/legal $800; m2 DIP designs $1.5k + card design 1/3; m3 card design 2/3; m4 card design 3/3 + used Fanuc 16i/18i control + Mitsubishi Q CPU + PC-card reader $2.5k; m5 prototype run $1.5k
  inventory_cover_months               3                            | ESTIMATE: 26-week MRAM lead time forces >= 3 months of stock
  first_lot_cards                      100                          | ESTIMATE: minimum economic EMS lot
  first_lot_dip                        200                          | ESTIMATE
  scn_demand_mult                      {'BASE': 1.0, 'GLUT': 0.95,  | ESTIMATE: glut correlates with AI/industrial capex slowdown; legacy-MRO demand partly counter-cyclical
  scn_price_mult                       {'BASE': 1.0, 'GLUT': 1.0, ' | ESTIMATE: SEVERE adds copycat (Shenzhen) price pressure
  scn_cogs_mult                        {'BASE': 1.0, 'GLUT': 0.95,  | ESTIMATE: specialty NVM softens a little in a memory downturn
  fanuc_cnc_cumulative                 5000000                      | https://metalworkingnews.info/fanuc-reaches-cnc-production-milestone-of-5-million/ (Feb-2022)
  us_share_installed                   0.15                         | ESTIMATE: U.S. share of Fanuc installed base
  legacy_share                         0.35                         | ESTIMATE: share of Fanuc base on SRAM-card-era controls (0/15/16/18/20/21, i-A)
  legacy_still_running                 0.5                          | ESTIMATE
  machines_per_shop                    8                            | ESTIMATE; >20,000 U.S. job shops (https://www.mmsonline.com/blog/post/capital-spending-survey-projects-5-decline-in-machine-tool-buying-for-2020-but-spending-level-still-above-average)
  card_replacement_years               8                            | ESTIMATE: battery card life; Memex states >=10-yr rechargeable cell
  other_families_mult                  1.5                          | ESTIMATE: +Mitsubishi Q2MEM, Fanuc robots, Okuma/other, avionics/T&M/synth
  global_over_us_mult                  4                            | ESTIMATE
  plp_ee_contract_usd                  4.5e+04                      | card C-16: contract EE ~$30-60k year 1
  plp_eval_boards_usd                  5000                         | ESTIMATE
  plp_designin_fee_usd                 4e+04                        | ESTIMATE: package + integration services per OEM design-in
  plp_services_gm                      0.4                          | card C-16 verify_corrections: services ~40% GM years 1-3
  plp_p_designin_by_m36_base           0.35                         | ESTIMATE: controller vendors/IBM gate PLP; Swissbit PowerSafe, Apacer CorePower own PLP (https://www.electronicsforu.com/news/new-products/swissbit-introduces-powersafe-a-power-loss-protection-system-for-industrial-ssds)
  plp_dram_cache_gb_replaced           2                            | ESTIMATE: DRAM-less design replaces 2GB cache
  plp_mram_mb                          512                          | ESTIMATE: 4x 1Gb STT journal
  plp_supercap_bom_usd                 12                           | ESTIMATE: 2-15 tantalum-polymer caps per drive (https://jisaku.com/glossary/storage-ssd-power-loss-protection-tantalum-cap, unverified)
  itc_target_date                      2027-08-16                   | https://www.usitc.gov/sites/default/files/secretary/fed_reg_notices/337/337_1487_notice08262026sgl.pdf
```
