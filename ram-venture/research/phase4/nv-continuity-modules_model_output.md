# DD3 nv-continuity-modules: model output (revised after Phase 5 red team)

- **Model:** `models/nv-continuity-modules.py` (pure Python 3 stdlib; exit 0 on 2026-11-01)
- **Command:** `python3 models/nv-continuity-modules.py` from `/home/user/VirtualWorkplaceStudio/ram-venture`
- **Phase 4 reproduction:** `python3 models/nv-continuity-modules.py --phase4` prints the Phase 4 output unchanged (BASE 36-month net $79.1k).
- **Phase 5 revisions:** section [0] below lists every changed input (Phase 4 value -> revised value, objection ids). Responses to all 25 DD3 objections: `research/phase5/responses_nv-continuity-modules.json`. Agent: `p5r-nv-continuity-modules`.
- **DRAM reference:** imported from `models/dram_cost_stack.py` `ddr5_reference()`
- **Evidence grade:** every input has a URL or an `ESTIMATE: basis` (section [9]). Prices are search-snippet grade ([REPORTED]).
- **Headline (BASE, revised):** run-rate $29.4k at m18 and $39.9k at m36; recurring ARR $2.7k at m36; breakeven m19; cash low -$9.2k (m13); 36-month net -$29.8k; founder full-time never. GLUT m36 $37.9k, SEVERE m36 $30.5k. 36-month cumulative breakeven needs 33 cards/month (BASE 16).

```text
====================================================================================================
DD3 nv-continuity-modules - unit economics, 36-month P&L (month 1 = 2026-11)
DRAM reference: models/dram_cost_stack.py ddr5_reference() (as_of 2026-11-01)
  Q4-2026 contract $20.37/GB | glut $8.15/GB | severe $2.04/GB | incumbent cost $1.48/GB
====================================================================================================

[0] RED-TEAM REVISIONS (Phase 5): Phase 4 value -> revised value (objection ids)
  legacy_share                  0.35                           -> 0.15                           RT-VET-DD3-01, RT-VC-DD3-02, RT-HYP-DD3-01
  legacy_still_running          0.5                            -> 0.4                            RT-VET-DD3-01, RT-HYP-DD3-02
  iseries_share                 0                              -> 0.2                            RT-HYP-DD3-01, RT-VC-DD3-02
  iseries_card_need             0                              -> 0.2                            RT-HYP-DD3-01, RT-VET-DD3-01
  other_families_mult           1.5                            -> 1.35                           RT-VET-DD3-06
  global_over_us_mult           4                              -> 6.667                          RT-VC-DD3-03
  sam_over_us_mult              4                              -> 1.1                            RT-VC-DD3-03
  sam_intl_reach                0                              -> 0.15                           RT-VC-DD3-03
  card_units_steady_month       40                             -> 16                             RT-HYP-DD3-02, RT-VC-DD3-03, RT-VET-DD3-01
  card_demand_decay_yr          0                              -> 0.1                            RT-HYP-DD3-02, RT-VC-DD3-03
  dip_units_steady_month        50                             -> 0                              RT-VET-DD3-03, RT-PHY-DD3-02, RT-PHY-DD3-03
  first_lot_dip                 200                            -> 0                              RT-VET-DD3-03
  opex_marketing_dip            300                            -> 150                            RT-VET-DD3-03
  card_logic_2mb_usd            5                              -> 9                              RT-PHY-DD3-04, RT-PHY-DD3-05
  card_logic_4mb_usd            6                              -> 10                             RT-PHY-DD3-04, RT-PHY-DD3-05
  card_shield_usd               0                              -> 3                              RT-PHY-DD3-01, RT-VET-DD3-02, RT-HYP-DD3-06
  card_frame_kit_connector_usd  12                             -> 15                             RT-HYP-DD3-03, RT-VET-DD3-04
  ltb_connector_sets            0                              -> 350                            RT-HYP-DD3-03, RT-VET-DD3-04
  ltb_month                     0                              -> 9                              RT-HYP-DD3-03, RT-VET-DD3-04
  warranty_returns_pct          0.03                           -> 0.06                           RT-VC-DD3-06, RT-VET-DD3-05, RT-PHY-DD3-06
  opex_from_launch_month        225                            -> 350                            RT-HYP-DD3-05
  opex_support_retainer         0                              -> 150                            RT-VC-DD3-06
  card_launch_month             9                              -> 11                             RT-VET-DD3-05, RT-PHY-DD3-06, RT-PHY-DD3-04
  one_time                      {1: 800.0, 2: 4500.0, 3: 30... -> {1: 1100.0, 2: 3000.0, 3: 3... RT-VET-DD3-03, RT-VET-DD3-05, RT-PHY-DD3-06, RT-HYP-DD3-05, RT-PHY-DD3-01
  ltsa_contracts                [(27, 2000.0), (33, 2000.0)]   -> []                             RT-VC-DD3-04
  plp_supercap_bom_usd          12                             -> 4                              RT-PHY-DD3-07

  Headline before / after red team
model               scenario  run-rate m18  run-rate m36  rec. ARR m36  breakeven m      cash low  36-mo net  full-time m  first rev
------------------  --------  ------------  ------------  ------------  -----------  ------------  ---------  -----------  ---------
Phase 4                 BASE       $121.7k       $195.8k        $56.2k           11   $10.8k (m6)     $79.1k        never         m4
Phase 4                 GLUT       $115.6k       $186.0k        $53.4k           11   $11.6k (m6)     $79.0k        never         m4
Phase 4               SEVERE        $93.1k       $153.9k        $47.1k           12   $12.2k (m7)     $49.3k        never         m4
Phase 5 (red team)      BASE        $29.4k        $39.9k         $2.7k           19  -$9.2k (m13)    -$29.8k        never        m11
Phase 5 (red team)      GLUT        $28.0k        $37.9k         $2.6k           19  -$8.5k (m13)    -$29.8k        never        m11
Phase 5 (red team)    SEVERE        $22.5k        $30.5k         $2.1k           22  -$8.2k (m14)    -$36.9k        never        m11

[0b] CONNECTOR/FRAME LIFETIME BUY: 350 sets at $15.00 = $5.2k in m9; BASE needs 288 cards m11-m36 (x1.2 = 346); 62 sets left at m36

[1] UNIT ECONOMICS PER SKU (BASE; revenue blended over eBay / own store / reseller)
SKU                                             list  net rev/unit     COGS   GM  fees+CAC+ship+warr  contrib  contrib%
----------------------------------------------  ----  ------------  -------  ---  ------------------  -------  --------
NV-CARD 2MB (1x MR4A16B)                        $249       $219.12   $95.50  56%              $40.25   $83.37       38%
NV-CARD 4MB (2x MR4A16B)                        $349       $307.12  $141.50  54%              $49.94  $115.68       38%
NV-DIP 256Kb (FM18W08) DS1225/1230 [KILLED P5]   $34        $32.64   $23.00  30%              $10.88   $-1.24       -4%
NV-DIP 1Mb (FM28V100) DS1245 [KILLED P5]         $59        $56.64   $35.00  38%              $13.97    $7.67       14%
  MRAM per 2MB card = $42.00 of $95.50 COGS (44%); per-bit: MR4A16B $21504/GB vs DDR5 contract $20.37/GB
  L3 cloud: $29/shop/mo, COGS $3 -> GM 90% | L4 LTSA GM 50%

[2] CUSTOMER-ACQUISITION ASSUMPTIONS
line     channel mix (eBay/store/reseller)  CAC per store order      launch m      steady units/mo
-------  ---------------------------------  -------------------  ------------  -------------------
NV-CARD                          25/35/40%                  $30            11                   16
NV-DIP                           40/40/20%                   $6             4                    0
CLOUD      6% attach of direct card buyers         $0 (bundled)            15        churn 2.5%/mo
LTSA                  direct (DMSMS / OEM)         founder time  none in BASE  upside only (S2/S4)

[3] DEMAND SIZING (TAM, ESTIMATE chain)
  Fanuc cumulative CNCs 5,000,000 x US 15% x pre-i/CF-rejecting 15% x still running 40% = 45,000 U.S. machines
  + i-series residual: x i-A/early-i 20% x running 60% x residual SRAM-card need 20% = 18,000 machine-equivalents
  = 63,000 U.S. machines / 8 per shop = 7,875 shops; replacement every 8 yrs x 1.35 other families = 1,329 cards/yr U.S.
  Addressable (SAM) = U.S. x 1.10 + 15% of non-U.S. = 2,591 cards/yr; global = U.S. x 6.67 = 8,859 cards/yr
  Base plan steady state 16 cards/mo = 192/yr = 7% of SAM, 14% of U.S., 2% of global demand (before the 10%/yr decay)
  Card market at blended $241/card: SAM $624.8k/yr; U.S. $320.4k/yr; global $2.14M/yr

[4] MONTHLY P&L AND CASH - BASE (founder part-time, no salary until trigger)
m     month  cards  DIPs  subs  revenue  gross  var+fixed  one-time  salary     net  inventory    cash
--  -------  -----  ----  ----  -------  -----  ---------  --------  ------  ------  ---------  ------
1   2026-11      0     0     0       $0     $0        $75     $1.1k      $0  -$1.2k         $0  $38.8k
2   2026-12      0     0     0       $0     $0        $75     $3.0k      $0  -$3.1k         $0  $35.8k
3   2027-01      0     0     0       $0     $0        $75     $3.0k      $0  -$3.1k         $0  $32.7k
4   2027-02      0     0     0       $0     $0       $575     $5.5k      $0  -$6.1k         $0  $26.6k
5   2027-03      0     0     0       $0     $0       $575     $1.5k      $0  -$2.1k         $0  $24.5k
6   2027-04      0     0     0       $0     $0       $575     $3.0k      $0  -$3.6k         $0  $20.9k
7   2027-05      0     0     0       $0     $0       $575     $1.5k      $0  -$2.1k         $0  $18.9k
8   2027-06      0     0     0       $0     $0       $575     $9.0k      $0  -$9.6k     $10.7k  -$1.4k
9   2027-07      0     0     0       $0     $0       $575        $0      $0   -$575     $10.7k  -$7.2k
10  2027-08      0     0     0       $0     $0       $575        $0      $0   -$575     $10.7k  -$7.8k
11  2027-09      1     0     0     $321   $179      $1.1k        $0      $0   -$903     $10.6k  -$8.5k
12  2027-10      3     0     0     $637   $355      $1.1k        $0      $0   -$783     $10.3k  -$9.0k
13  2027-11      4     0     0     $948   $527      $1.2k        $0      $0   -$666      $9.9k  -$9.2k
14  2027-12      5     0     0    $1.3k   $697      $1.2k        $0      $0   -$550      $9.3k  -$9.1k
15  2028-01      6     0     0    $1.6k   $869      $1.3k        $0      $0   -$430      $8.6k  -$8.7k
16  2028-02      8     0     1    $1.9k  $1.0k      $1.4k        $0      $0   -$312      $7.8k  -$8.1k
17  2028-03      9     0     1    $2.2k  $1.2k      $1.4k        $0      $0   -$194      $6.8k  -$7.2k
18  2028-04     10     0     1    $2.5k  $1.4k      $1.5k        $0      $0    -$78      $5.8k  -$6.1k
19  2028-05     11     0     2    $2.7k  $1.5k      $1.5k        $0      $0     $38      $4.6k  -$4.7k
20  2028-06     12     0     2    $3.0k  $1.7k      $1.6k        $0      $0    $152      $4.5k  -$4.3k
21  2028-07     13     0     2    $3.3k  $1.9k      $1.6k        $0      $0    $265      $4.6k  -$3.9k
22  2028-08     15     0     3    $3.6k  $2.0k      $1.6k        $0      $0    $377      $4.6k  -$3.3k
23  2028-09     14     0     3    $3.6k  $2.0k      $1.6k        $0      $0    $377      $4.5k  -$2.7k
24  2028-10     14     0     4    $3.5k  $2.0k      $1.6k        $0      $0    $377      $4.5k  -$2.0k
25  2028-11     14     0     4    $3.5k  $2.0k      $1.6k        $0      $0    $376      $4.5k  -$1.4k
26  2028-12     14     0     5    $3.5k  $2.0k      $1.6k        $0      $0    $375      $4.4k   -$787
27  2029-01     14     0     5    $3.5k  $2.0k      $1.6k        $0      $0    $374      $4.4k   -$166
28  2029-02     14     0     5    $3.5k  $2.0k      $1.6k        $0      $0    $373      $4.3k    $452
29  2029-03     14     0     6    $3.5k  $2.0k      $1.6k        $0      $0    $371      $4.3k   $1.1k
30  2029-04     14     0     6    $3.4k  $2.0k      $1.6k        $0      $0    $369      $4.3k   $1.7k
31  2029-05     13     0     6    $3.4k  $2.0k      $1.6k        $0      $0    $367      $4.2k   $2.3k
32  2029-06     13     0     7    $3.4k  $2.0k      $1.6k        $0      $0    $365      $4.2k   $2.9k
33  2029-07     13     0     7    $3.4k  $1.9k      $1.6k        $0      $0    $362      $4.2k   $3.5k
34  2029-08     13     0     7    $3.4k  $1.9k      $1.6k        $0      $0    $359      $4.1k   $4.1k
35  2029-09     13     0     8    $3.3k  $1.9k      $1.6k        $0      $0    $356      $4.1k   $4.7k
36  2029-10     13     0     8    $3.3k  $1.9k      $1.6k        $0      $0    $353      $4.1k   $5.2k

[4b] CASH CURVE BY SCENARIO (end of quarter; start $40k)
scenario      m3      m6      m9     m12     m15     m18     m21     m24     m27     m30     m33     m36
--------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------  ------
BASE      $32.7k  $20.9k  -$7.2k  -$9.0k  -$8.7k  -$6.1k  -$3.9k  -$2.0k   -$166   $1.7k   $3.5k   $5.2k
GLUT      $32.7k  $20.9k  -$6.4k  -$8.2k  -$8.2k  -$5.8k  -$3.3k  -$1.5k    $322   $2.1k   $3.8k   $5.5k
SEVERE    $32.7k  $20.9k  -$5.6k  -$7.6k  -$8.2k  -$6.9k  -$4.6k  -$3.9k  -$3.3k  -$2.6k  -$2.0k  -$1.5k

[5] SCENARIO SUMMARY (core lines L1-L4; PLP option excluded - see [7])
scenario  breakeven m      cash low  cash m36  full-time m  36-mo revenue  36-mo net  GM m36
--------  -----------  ------------  --------  -----------  -------------  ---------  ------
BASE               19  -$9.2k (m13)     $5.2k        never         $72.1k    -$29.8k     58%
GLUT               19  -$8.5k (m13)     $5.5k        never         $68.5k    -$29.8k     60%
SEVERE             22  -$8.2k (m14)    -$1.5k        never         $55.2k    -$36.9k     58%
  first revenue month (BASE): m11 (2027-09); cumulative cards m18 / m36: 46 / 288

  ARR at months 12 / 18 / 24 / 36
scenario  run-rate m12     m18     m24     m36  recurring ARR m12   m18    m24    m36
--------  ------------  ------  ------  ------  -----------------  ----  -----  -----
BASE             $7.6k  $29.4k  $42.6k  $39.9k                 $0  $400  $1.3k  $2.7k
GLUT             $7.3k  $28.0k  $40.5k  $37.9k                 $0  $380  $1.2k  $2.6k
SEVERE           $5.9k  $22.5k  $32.6k  $30.5k                 $0  $306   $987  $2.1k
  run-rate = that month's revenue x 12 (hardware is repeat-purchase, not contracted).
  recurring ARR = (cloud MRR + LTSA monthly) x 12 = the only contracted/subscription revenue.
  DRAM $/GB used per scenario at m24: BASE $18.67, GLUT $8.15, SEVERE $2.04

[6] SENSITIVITY (BASE; one variable at a time, -30% / +30%)
case                                                      breakeven m  cash low  run-rate m18  run-rate m36  rec. ARR m36  36-mo cum. net
--------------------------------------------------------  -----------  --------  ------------  ------------  ------------  --------------
baseline                                                           19    -$9.2k        $29.4k        $39.9k         $2.7k         -$29.8k
price -30%                                                      never   -$14.1k        $20.6k        $27.9k         $1.9k         -$49.1k
price +30%                                                         16    -$8.7k        $38.3k        $51.9k         $3.5k         -$10.4k
conversion/close -30%                                           never   -$10.0k        $20.6k        $27.9k         $1.9k         -$38.4k
conversion/close +30%                                              17    -$8.7k        $38.3k        $51.9k         $3.5k         -$21.2k
churn -30%                                                         19    -$9.2k        $29.4k        $40.1k         $2.9k         -$29.7k
churn +30%                                                         19    -$9.2k        $29.4k        $39.7k         $2.5k         -$29.9k
COGS -30%                                                          17    -$4.4k        $29.4k        $39.9k         $2.7k         -$20.5k
COGS +30%                                                       never   -$13.9k        $29.4k        $39.9k         $2.7k         -$39.0k
no LTSA/DMSMS contract                                             19    -$9.2k        $29.4k        $39.9k         $2.7k         -$29.8k
card launch +6 mo (MRAM lead/validation slip)                      25   -$12.6k         $7.7k        $41.4k         $2.2k         -$35.2k
RT price x0.8 (RT-HYP-DD3-04)                                   never    -$9.7k        $23.5k        $31.9k         $2.2k         -$42.7k
RT volume x0.5 (RT-HYP-DD3-02)                                  never   -$11.1k        $14.7k        $19.9k         $1.4k         -$44.1k
RT copycat from m24, price x0.75 (RT-VC-DD3-05)                 never    -$9.2k        $29.4k        $30.6k         $2.7k         -$39.2k
RT + 2 LTSAs from m27/m33 (upside, RT-VC-DD3-04)                   19    -$9.2k        $29.4k        $87.9k        $50.7k         -$15.8k
RT no demand decay                                                 19    -$9.2k        $31.3k        $49.4k         $3.1k         -$25.9k
RT volume back to Phase 4 (40/mo)                                  14    -$8.1k        $73.6k        $99.7k         $6.8k          $13.3k
RT LTB at MOQ 1,000 sets                                           19   -$18.9k        $29.4k        $39.9k         $2.7k         -$29.8k
RT no connector LTB (two live sources found)                       19    -$3.8k        $29.4k        $39.9k         $2.7k         -$28.9k
RT DIP line restored as Phase 4 (F-RAM)                            20   -$10.2k        $53.3k        $63.8k         $2.7k         -$32.7k
RT lean re-plan (partner benches, lab $4k, 50-card lots)           20     $3.7k        $29.4k        $39.9k         $2.7k         -$22.4k
RT demand-validated: 40/mo, price x1.0, LTB 880                    14   -$16.1k        $73.6k        $99.7k         $6.8k          $13.3k

[6b] SCALE PATH BEYOND THE 'LOW-$100ks' CEILING (BASE market; overrides are ESTIMATES)
path                                                                     run-rate m36  rec. ARR m36  36-mo net  full-time m  share of SAM  share of global
-----------------------------------------------------------------------  ------------  ------------  ---------  -----------  ------------  ---------------
S0 BASE (direct + 40% resellers, no LTSA)                                      $39.9k         $2.7k    -$29.8k        never            7%               2%
S1 + white-label in 3-4 MRO catalogs (cards x2, 65% reseller)                  $71.2k         $3.2k     -$7.4k        never           15%               4%
S2 + DMSMS/OEM program (4 LTSAs, 2 at $4k/mo) [upside only]                   $183.9k       $146.7k     $15.2k        never            7%               2%
S3 + adjacent form factors (Q2MEM, robots, avionics, synth; cards x1.5)        $59.8k         $4.1k    -$15.4k        never           11%               3%
S4 stretch: S1+S2+S3 combined (cards x3), cloud attach 15%                    $257.9k       $155.9k     $69.4k        never           22%               7%
  Even the stretch path stays well under $1M/yr; card shares are of steady-state demand before decay.

[7] C-16 PLP OPTION - MRAM journal vs DRAM cache + supercaps (per board) and option value
scenario  DRAM $/GB (2028+)  MRAM 512MB cost  DRAM 2GB + caps saved  MRAM premium/board  p(paid design-in by m36)  option cost  EV gross profit   EV net  design-ins to break even
--------  -----------------  ---------------  ---------------------  ------------------  ------------------------  -----------  ---------------  -------  ------------------------
BASE                 $18.33             $410                    $41                $370                      0.32       $50.0k            $5.1k  -$44.9k                       3.1
GLUT                  $8.15             $410                    $20                $390                      0.16       $50.0k            $2.5k  -$47.5k                       3.1
SEVERE                $2.04             $410                     $8                $402                      0.06       $50.0k            $1.0k  -$49.0k                       3.1
  MRAM never wins on BOM; the DRAM glut moves the per-board gap by only ~$20-33. Buyers adopt for
  reliability (no supercap aging), so the kit's market is set by controller vendors, not price.
  ITC 337-TA-1487 target date 2027-08-16: exclusion risk applies to Everspin STT (1Gb, xSPI), not to Toggle MR4A16B.
  RED-TEAM (RT-PHY-DD3-07): hold-up energy is still needed for in-flight NAND program/erase (paired pages)
  unless the FTL changes, and the founder owns no FTL. Only $4 of the $12 cap BOM is removable.
  VERDICT: C-16 KILLED (Phase 5). The email interest test is dropped.

[8] WHAT MUST BE TRUE
  Contribution per card $91, per DIP $1; fixed opex at full launch $1025/mo.
  (a) Part-time breakeven: 11 cards/mo (or 716 DIPs/mo) cover fixed opex. BASE at m18 sells 10 cards + 0 DIPs.
  (b) Founder full-time ($120k/yr): 121 cards/mo = 56% of addressable (SAM) / 16% of global card demand.
  (c) $0.5M/yr run-rate from cards alone: 173 cards/mo = 80% of SAM / 23% of global demand.
  (f) 36-month cumulative net >= 0 needs 33 cards/mo steady (BASE has 16) = 15% of SAM / 30% of U.S. demand.
  (d) Cumulative orders by m18 in BASE: 46 units (46 cards, 0 DIPs); reseller accounts needed: >=3 by m12.
  (e) Status after red team: KILLED in BASE. Reopen only if a $1.2k demand probe gets >=30 full-list deposits (<=1/3 i-series) AND a reseller LOI >=100 cards/yr at >=$175, or a white-label commitment >=200 cards/yr x 2 yrs.
      After a reopen, the card line dies if a pre-i Fanuc (16-C/18-C/21-B) rejects it, if a shielded card loses data at 30 mT or after 60 s on a 0.3 T magnetic base, or if hot removal corrupts non-addressed data.

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
  card_frame_kit_connector_usd         15                           | RED-TEAM (Phase 5) RT-HYP-DD3-03, RT-VET-DD3-04: was 12.0. ESTIMATE: no current-production card-side quote found (Hirose IC1K LTB; FCI 90937 obsolete; TE assemblies status unknown); broker/LTB premium. [Phase 4 src: ESTIMATE: no small-qty price found; ITT StarCard kits exist (https://www.designnews.com/motion-control/itt-interconnect-solutions-snap-on-and-ultrasonic-pcmcia-i-o-card-kits); one 68-pos connector is Last Time Buy]
  card_pcb_2mb_usd                     4.5                          | ESTIMATE: 0.8mm 4-layer, 100-pc offshore fab
  card_pcb_4mb_usd                     5.5                          | ESTIMATE: as above, larger
  card_logic_2mb_usd                   9                            | RED-TEAM (Phase 5) RT-PHY-DD3-04, RT-PHY-DD3-05: was 5.0. ESTIMATE: 74LVC16T245-class dual-supply translators + mandatory small CPLD (8-bit byte-lane steering, REG#/attribute decode, E/W gating) + supervisor + hold-up cap. [Phase 4 src: ESTIMATE: 3x 74LVC16245-class 5V-tolerant buffers + supervisor + attribute EEPROM + passives]
  card_logic_4mb_usd                   10                           | RED-TEAM (Phase 5) RT-PHY-DD3-04, RT-PHY-DD3-05: was 6.0. as above + chip-select decode. [Phase 4 src: ESTIMATE: as above + decode]
  card_assembly_usd                    14                           | ESTIMATE: U.S. EMS at 100-pc lots; anecdote $415-1,300 per 10 turnkey boards (https://community.sparkfun.com/t/pcb-assembly-service/27265)
  card_assembly_4mb_usd                16                           | ESTIMATE: +1 BGA/TSOP placement
  card_setup_amort_usd                 4                            | ESTIMATE: ~$400 stencil/setup per 100-card lot (Screaming Circuits best at 25+: https://pic.hallikainen.org/piclist/2008/a/01/29/165504a.txt)
  card_test_pack_usd                   4                            | ESTIMATE: functional test on fixture, label, ESD bag, CoC
  card_shield_usd                      3                            | RED-TEAM (Phase 5) RT-PHY-DD3-01, RT-VET-DD3-02, RT-HYP-DD3-06: was 0.0. ESTIMATE: Ni-Fe/mu-metal foil over the MRAM inside the Type I envelope (or ferritic-steel cover); MR4A16B Hmax_write 8,000 A/m. [Phase 4 src: Phase 4: no magnetic shield (neutral default; see RED-TEAM REVISIONS)]
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
  warranty_returns_pct                 0.06                         | RED-TEAM (Phase 5) RT-VC-DD3-06, RT-VET-DD3-05, RT-PHY-DD3-06: was 0.03. ESTIMATE: dozens of firmware/option combinations; validation on 3 families, not all; magnet-exposure claims. [Phase 4 src: ESTIMATE: 3% of revenue (compatibility returns)]
  card_channel_mix                     {'ebay': 0.25, 'store': 0.35 | ESTIMATE: resellers matter because the buyer is a maintenance tech searching MRO catalogs
  dip_channel_mix                      {'ebay': 0.4, 'store': 0.4,  | ESTIMATE
  card_launch_month                    11                           | RED-TEAM (Phase 5) RT-VET-DD3-05, RT-PHY-DD3-06, RT-PHY-DD3-04: was 9. pre-i bench + 3-family validation + outside-lab ESD/temp/insertion + rev-B respin before the first 100-card lot. [Phase 4 src: ESTIMATE: design m1-3, proto/validate m4-6, MRAM lead 20-26 wk ordered m3]
  card_ramp_months                     12                           | ESTIMATE
  card_demand_decay_yr                 0.1                          | RED-TEAM (Phase 5) RT-HYP-DD3-02, RT-VC-DD3-03: was 0.0. ESTIMATE: ~6%/yr pre-i retirement + ~4%/yr self-depletion (each battery-free card removes an 8-yr replacement). [Phase 4 src: Phase 4: demand held flat after ramp (neutral default; see RED-TEAM REVISIONS)]
  card_units_steady_month              16                           | RED-TEAM (Phase 5) RT-HYP-DD3-02, RT-VC-DD3-03, RT-VET-DD3-01: was 40. ~13% of revised North-American SAM (see [3]); a new entrant's share, to be re-set by track A deposits. [Phase 4 src: ESTIMATE: ~5% of est. global ~10k/yr PC-card SRAM replacement demand (see TAM block)]
  dip_launch_month                     4                            | ESTIMATE: FM18W08 in stock (~775 at DigiKey), 8-wk standard lead
  dip_ramp_months                      9                            | ESTIMATE
  dip_units_steady_month               0                            | RED-TEAM (Phase 5) RT-VET-DD3-03, RT-PHY-DD3-02, RT-PHY-DD3-03: was 50. DIP leg killed: FM18W08/FM28V100 latch address on /CE fall (130 ns cycle); originals DS1230Y/DS1245Y still in ADI production. [Phase 4 src: ESTIMATE: free open adapters cap the hobby segment; sells on test report + warranty]
  cloud_launch_month                   15                           | ESTIMATE: after cards are in the field
  cloud_price_month                    29                           | ESTIMATE: per shop; below DNC/MDC suites
  cloud_attach_rate                    0.06                         | ESTIMATE: 6% of direct card buyers subscribe
  cloud_churn_month                    0.025                        | ESTIMATE: SMB tool churn
  cloud_cogs_month                     3                            | ESTIMATE: hosting + support per sub
  ltsa_contracts                       []                           | RED-TEAM (Phase 5) RT-VC-DD3-04: was [(27, 2000.0), (33, 2000.0)]. no DLA/NSN demand for DS12xx or PC Card SRAM found (Phase 4 and Phase 5 searches); LTSAs kept only in scale path S2/S4. [Phase 4 src: ESTIMATE: two $24k/yr blanket orders (start month, $/month); DLA buys 5962 memory by NSN via DIBBS (https://www.highergov.com/nsn/5962012622185/)]
  ltsa_gm                              0.5                          | ESTIMATE: screened, traceable lots with CoC
  opex_tools_month                     75                           | ESTIMATE: domain, Shopify-class store, email
  opex_from_launch_month               350                          | RED-TEAM (Phase 5) RT-HYP-DD3-05: was 225.0. product liability $1-2M COI ~$250/mo [ESTIMATE] + bookkeeping $100. [Phase 4 src: ESTIMATE: product liability insurance ~$125 + bookkeeping ~$100]
  opex_marketing_dip                   150                          | RED-TEAM (Phase 5) RT-VET-DD3-03: was 300.0. DIP ads dropped; $150/mo pre-launch card-deposit marketing kept from m4. [Phase 4 src: ESTIMATE: ads + samples from DIP launch]
  opex_marketing_card                  300                          | ESTIMATE: extra ads + trade-forum presence from card launch
  opex_support_retainer                150                          | RED-TEAM (Phase 5) RT-VC-DD3-06: was 0.0. ESTIMATE: retainer for a CNC field-service technician who handles 'won't format on my 18-B' tickets. [Phase 4 src: Phase 4: no paid CNC-service support (neutral default; see RED-TEAM REVISIONS)]
  one_time                             {1: 1100.0, 2: 3000.0, 3: 30 | RED-TEAM (Phase 5) RT-VET-DD3-03, RT-VET-DD3-05, RT-PHY-DD3-06, RT-HYP-DD3-05, RT-PHY-DD3-01: was {1: 800.0, 2: 4500.0, 3: 3000.0, 4: 5500.0, 5: 1500.0}. m1 +$300 gaussmeter/test magnets; m2 DIP design $1.5k removed; m4 control budget now buys a pre-i 16-C/18-C/21-B; m6 +$3k bench time on 2 more families/firmware revs; m7 +$1.5k QMS manual + RMA process; m8 +$7.5k outside-lab ESD (IEC 61000-4-2), 0-55C, insertion life + $1.5k rev-B respin. [Phase 4 src: ESTIMATE: m1 LLC/legal $800; m2 DIP designs $1.5k + card design 1/3; m3 card design 2/3; m4 card design 3/3 + used Fanuc 16i/18i control + Mitsubishi Q CPU + PC-card reader $2.5k; m5 prototype run $1.5k]
  inventory_cover_months               3                            | ESTIMATE: 26-week MRAM lead time forces >= 3 months of stock
  first_lot_cards                      100                          | ESTIMATE: minimum economic EMS lot
  first_lot_dip                        0                            | RED-TEAM (Phase 5) RT-VET-DD3-03: was 200. no DIP inventory. [Phase 4 src: ESTIMATE]
  ltb_connector_sets                   350                          | RED-TEAM (Phase 5) RT-HYP-DD3-03, RT-VET-DD3-04: was 0. funded lifetime buy = modeled BASE card need m11-m36 (288) x 1.2, rounded (see [0b]). [Phase 4 src: Phase 4: no connector/frame lifetime buy (neutral default; see RED-TEAM REVISIONS)]
  ltb_month                            9                            | RED-TEAM (Phase 5) RT-HYP-DD3-03, RT-VET-DD3-04: was 0. bought with the first EMS lot. [Phase 4 src: Phase 4: n/a]
  scn_demand_mult                      {'BASE': 1.0, 'GLUT': 0.95,  | ESTIMATE: glut correlates with AI/industrial capex slowdown; legacy-MRO demand partly counter-cyclical
  scn_price_mult                       {'BASE': 1.0, 'GLUT': 1.0, ' | ESTIMATE: SEVERE adds copycat (Shenzhen) price pressure
  scn_cogs_mult                        {'BASE': 1.0, 'GLUT': 0.95,  | ESTIMATE: specialty NVM softens a little in a memory downturn
  fanuc_cnc_cumulative                 5000000                      | https://metalworkingnews.info/fanuc-reaches-cnc-production-milestone-of-5-million/ (Feb-2022)
  us_share_installed                   0.15                         | ESTIMATE: U.S. share of Fanuc installed base
  legacy_share                         0.15                         | RED-TEAM (Phase 5) RT-VET-DD3-01, RT-VC-DD3-02, RT-HYP-DD3-01: was 0.35. pre-i controls only (16/18-A/B/C, 15, 20/21-B, RJ-2); i-series moved to iseries_* rows; VET estimate ~0.15. [Phase 4 src: ESTIMATE: share of Fanuc base on SRAM-card-era controls (0/15/16/18/20/21, i-A)]
  legacy_still_running                 0.4                          | RED-TEAM (Phase 5) RT-VET-DD3-01, RT-HYP-DD3-02: was 0.5. pre-i controls are 26-38 years old; the 0.50 blend assumed younger i-A units. [Phase 4 src: ESTIMATE]
  machines_per_shop                    8                            | ESTIMATE; >20,000 U.S. job shops (https://www.mmsonline.com/blog/post/capital-spending-survey-projects-5-decline-in-machine-tool-buying-for-2020-but-spending-level-still-above-average)
  card_replacement_years               8                            | ESTIMATE: battery card life; Memex states >=10-yr rechargeable cell
  other_families_mult                  1.35                         | RED-TEAM (Phase 5) RT-VET-DD3-06: was 1.5. Mitsubishi FA-A-0184 points High-speed Universal QCPU users to SD; SRAM card only for QnH/QnUD file registers. [Phase 4 src: ESTIMATE: +Mitsubishi Q2MEM, Fanuc robots, Okuma/other, avionics/T&M/synth]
  global_over_us_mult                  6.667                        | RED-TEAM (Phase 5) RT-VC-DD3-03: was 4.0. internal consistency: a 15% U.S. share implies global = 6.7x U.S. (information only, not addressable). [Phase 4 src: ESTIMATE]
  iseries_share                        0.2                          | RED-TEAM (Phase 5) RT-HYP-DD3-01, RT-VC-DD3-02: was 0.0. ESTIMATE: i-A / early i-B / 0i-A/B share of cumulative Fanuc units. [Phase 4 src: Phase 4: i-A folded into legacy_share (neutral default; see RED-TEAM REVISIONS)]
  iseries_still_running                0.6                          | ESTIMATE: i-series controls are younger (1996-2008) than pre-i
  iseries_card_need                    0.2                          | RED-TEAM (Phase 5) RT-HYP-DD3-01, RT-VET-DD3-01: was 0.0. ESTIMATE: residual SRAM-card need on i-series (normal-mode I/O on 18i-T; CF format NMI on a 16iA, CNCzone 421202); boot backup works on CF. [Phase 4 src: Phase 4: n/a (neutral default)]
  sam_over_us_mult                     1.1                          | RED-TEAM (Phase 5) RT-VC-DD3-03: was 4.0. core addressable = U.S. + Canada: every named channel is North American. [Phase 4 src: Phase 4 treated the global market as addressable (SAM = U.S. x 4.0)]
  sam_intl_reach                       0.15                         | RED-TEAM (Phase 5) RT-VC-DD3-03: was 0.0. partial counter: a plain memory card is very likely EAR99 [ESTIMATE, unconfirmed], so eBay/web can reach ~15% of non-U.S. demand. [Phase 4 src: Phase 4: n/a (neutral default)]
  plp_ee_contract_usd                  4.5e+04                      | card C-16: contract EE ~$30-60k year 1
  plp_eval_boards_usd                  5000                         | ESTIMATE
  plp_designin_fee_usd                 4e+04                        | ESTIMATE: package + integration services per OEM design-in
  plp_services_gm                      0.4                          | card C-16 verify_corrections: services ~40% GM years 1-3
  plp_p_designin_by_m36_base           0.35                         | ESTIMATE: controller vendors/IBM gate PLP; Swissbit PowerSafe, Apacer CorePower own PLP (https://www.electronicsforu.com/news/new-products/swissbit-introduces-powersafe-a-power-loss-protection-system-for-industrial-ssds)
  plp_dram_cache_gb_replaced           2                            | ESTIMATE: DRAM-less design replaces 2GB cache
  plp_mram_mb                          512                          | ESTIMATE: 4x 1Gb STT journal
  plp_supercap_bom_usd                 4                            | RED-TEAM (Phase 5) RT-PHY-DD3-07: was 12.0. ESTIMATE: only ~1/3 of the $12 hold-up BOM is removable; paired-page protection still needs hold-up or an FTL change. [Phase 4 src: ESTIMATE: 2-15 tantalum-polymer caps per drive (https://jisaku.com/glossary/storage-ssd-power-loss-protection-tantalum-cap, unverified)]
  itc_target_date                      2027-08-16                   | https://www.usitc.gov/sites/default/files/secretary/fed_reg_notices/337/337_1487_notice08262026sgl.pdf
```
