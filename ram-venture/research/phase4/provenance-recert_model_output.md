# DD1 Provenance & Recertified Memory: model output (revised after Phase 5 red team)

Produced by `python3 models/provenance-recert.py`, run from `/home/user/VirtualWorkplaceStudio/ram-venture` on 2026-11-01 (exit 0). Pure stdlib. The DDR5 deck is a live import of `models/dram_cost_stack.py ddr5_reference()`.

**Phase 5 (red team, agent `p5r-provenance-recert`):** every number below uses Phase 4 INPUTS plus the RED-TEAM REVISIONS block in the script (section 0 lists each change, old → new, with its objection id). `P_PHASE4` in the script reproduces the Phase 4 output exactly (section 8a, first row: $445,543 ARR at m36, founder full-time m14). Section 8 attributes the change revision group by revision group, re-runs the reviewers' own variants, and runs the kill-test outcomes. Responses to all 28 objections: `research/phase5/responses_provenance-recert.json`; the write-up is `04_DEEPDIVES/provenance-recert.md` §14. Phase 4 inputs and their sources are in the INPUTS block; Phase 4 assumptions are in `research/assumptions/p4-provenance-recert.md`; research notes in `research/phase4/provenance-recert_notes.md`.

```
DD1 Provenance & Recertified Memory -- unit economics and 36-month P&L (models/provenance-recert.py)
As of 2026-11-01. Month 1 = Nov-26, month 36 = Oct-29. DDR5 deck: models/dram_cost_stack.py ddr5_reference() (live import)
  DDR5 component cost $1.48/GB | Q4-26 contract $20.37/GB | glut $8.15/GB (x0.40) | severe $2.04/GB (x0.10)
  New 64GB DDR5 RDIMM contract $25.78/user-GB; used 64GB DDR5 resale $16.33/GB = 63% of new (amcompute 55-74% band check)
  Used resale index applied to all recert SKUs, PMem and spares; CleanBOM demand is statutory (same in all).
  INPUTS: 97 values, each with a source or 'ESTIMATE: basis' (see the INPUTS dict in this file).
  PHASE 5: every number below uses P0 = Phase 4 INPUTS + the 29 RED-TEAM REVISIONS listed in section 0.

========================================================================================================
0. RED-TEAM REVISIONS (Phase 5): every changed input, old -> new, objection id (2026-11-01)
========================================================================================================
Input                     Phase 4        Phase 5  Objection id(s)                                                                       
------------------------  -------  -------------  --------------------------------------------------------------------------------------
buy_frac                     0.65            0.7  RT-HYP-DD1-04, RT-VC-DD1-05                                                           
b2b_price_factor             0.88            0.8  RT-HYP-DD1-05, RT-VET-DD1-05                                                          
ebay_share_m12                0.4            0.5  consequence of RT-HYP-DD1-05 / RT-VET-DD1-05                                          
fail_rate                    0.03           0.07  RT-VET-DD1-03, RT-PHY-DD1-03                                                          
return_rate                  0.02           0.03  RT-VET-DD1-03, RT-PHY-DD1-03                                                          
minutes_per_module           12.0           15.0  RT-VET-DD1-03, RT-PHY-DD1-03                                                          
capex_m1                   4200.0         4700.0  RT-VET-DD1-03, RT-PHY-DD1-03                                                          
mix_ddr4_32                   0.6           0.65  RT-VET-DD1-04                                                                         
mix_ddr4_64                   0.3           0.32  RT-VET-DD1-04                                                                         
mix_ddr5_64                   0.1           0.03  RT-VET-DD1-04                                                                         
units_cap_pt                  400            300  RT-HYP-DD1-04                                                                         
units_cap_ft                  600            450  RT-HYP-DD1-04                                                                         
ebay_new_seller_caps           ()  (20, 50, 100)  RT-VC-DD1-04                                                                          
ebay_hold_selling_months        0              3  RT-VC-DD1-04                                                                          
b2b_terms_months                0              1  RT-VC-DD1-04                                                                          
tax_rate                      0.0            0.3  RT-VC-DD1-07                                                                          
pmem_fail_rate                0.0            0.1  RT-PHY-DD1-05, RT-VET-DD1-07                                                          
pmem_return_rate             0.02           0.05  RT-PHY-DD1-05, RT-VET-DD1-07                                                          
lib_bundle_pays_module      False           True  RT-PHY-DD1-01, RT-HYP-DD1-02, RT-VC-DD1-02                                            
lib_module_cost             150.0          600.0  RT-PHY-DD1-01, RT-HYP-DD1-02, RT-VC-DD1-02                                            
lib_samples_early             3.0            1.0  RT-PHY-DD1-02, RT-VET-DD1-02, RT-HYP-DD1-03, RT-VC-DD1-03                             
lib_samples_late              1.0            0.5  as above                                                                              
lab_cost                    400.0          600.0  RT-VET-DD1-06                                                                         
cb_close_bundle               0.1           0.05  RT-HYP-DD1-01, RT-VC-DD1-01, RT-VET-DD1-01, RT-HYP-DD1-02, RT-PHY-DD1-01, RT-VC-DD1-02
cb_close_standalone          0.07           0.05  as above; no bundle/standalone difference remains                                     
cb_hi_share                  0.35            0.1  RT-HYP-DD1-06 + the three FATALs                                                      
cb_pack_rate                 0.15            0.1  RT-HYP-DD1-07                                                                         
opex_eo                     400.0          600.0  RT-HYP-DD1-08                                                                         
dh_in_bundle                 True          False  RT-PHY-DD1-04                                                                         
  Basis for each revision: RED_TEAM_REVISIONS in this file. Section 8 shows what each group costs.

========================================================================================================
1. UNIT ECONOMICS PER PRODUCT LINE (per unit, at each price deck; steady state, no inventory lag)
========================================================================================================

1a. Recert RDIMM (mix 65% 32GB DDR4 / 32% 64GB DDR4 / 3% 64GB DDR5), per good module; buy at 70% of realized resale; fallout 7%, returns 3%
Deck                  Channel  Price  Buy+fallout  Fees+ship  Ret+cons+labor  Contrib    GM
--------------------  -------  -----  -----------  ---------  --------------  -------  ----
Today (BASE 2026-27)  eBay      $212         $159        $34             $14       $4    2%
                      B2B       $169         $159         $7             $13      $-9   -6%
                      mix m12   $191         $159        $20             $13      $-3   -1%
GLUT (x0.40)          eBay       $85          $64        $17             $10      $-6   -7%
                      B2B        $68          $64         $4             $10      $-9  -14%
                      mix m12    $76          $64        $10             $10      $-8  -10%
SEVERE (x0.10)        eBay       $44          $33        $11              $9     $-10  -21%
                      B2B        $36          $33         $3              $9      $-9  -26%
                      mix m12    $40          $33         $7              $9      $-9  -23%
  Per SKU, today, mixed channel:
SKU        Resale/GB  Avg price   Buy  Contrib   GM  Cash tied/unit
---------  ---------  ---------  ----  -------  ---  --------------
DDR4 32GB   $3.91/GB       $112   $88      $-6  -5%             $88
DDR4 64GB   $4.84/GB       $279  $217       $1   0%            $217
DDR5 64GB  $16.33/GB       $940  $732      $31   3%            $732
  Inventory lag: buying at today's price and selling one GLUT month later (-5%/month) gives $-11 contribution per module (-6%).

1b. Optane PMem 128GB (C-26 SKU), eBay only; fallout 10% (locked/unsanitizable), returns 5%
Deck                  Price   Buy  Fees  Labor  Contrib    GM
--------------------  -----  ----  ----  -----  -------  ----
Today (BASE 2026-27)   $200  $122   $28     $7      $27   14%
GLUT (x0.40)            $80   $49   $11     $7       $3    4%
SEVERE (x0.10)          $20   $12    $3     $7      $-9  -46%

1c. CleanBOM-5949 per subscriber-month (blended 90% $750 / 10% $2500) -- same in every deck
Item                      $/month
------------------------  -------
Subscription ARPA            $925
Lab pass-through revenue     $384
Lab cost                    $-240
Software COGS (12%)         $-111
Gross profit                 $958
GM                            73%
  One-off evidence pack: $900 at ~88% GM (software cost only).

1d. DIMM-health per customer-year (1200 DIMMs at $0.60/DIMM-month) -- Phase 5: DROPPED from the bundle (RT-PHY-DD1-04); shown for reference only
Deck                  Spares from  Revenue/yr  COGS/yr   GM  Spare cost  Pool capital  Fee/DIY spares
--------------------  -----------  ----------  -------  ---  ----------  ------------  --------------
Today (BASE 2026-27)  bundle           $8,640   $3,332  61%        $100        $2,408            4.1x
                      standalone       $8,640   $4,008  54%        $130        $3,120            3.2x
GLUT (x0.40)          bundle           $8,640   $2,045  76%         $44        $1,053            7.8x
                      standalone       $8,640   $2,298  73%         $55        $1,320            6.6x
SEVERE (x0.10)        bundle           $8,640   $1,736  80%         $30          $728            9.9x
                      standalone       $8,640   $1,888  78%         $37          $888            8.7x

1e. Customer acquisition (founder time imputed at $75/h, 3 h per conversation; marketing $300/mo)
Line         Close/conv      CAC  Gross profit/mo  Churn/mo      LTV  LTV/CAC  Payback (mo)
-----------  ----------  -------  ---------------  --------  -------  -------  ------------
CleanBOM             5%   $5,100             $958        2%  $47,900       9x           5.3
DIMM-health         ~5%   $4,500             $482      1.5%  $32,166       7x           9.3
Recert B2B          n/a  in fees       per module       n/a      n/a      n/a           n/a
  LTV/CAC looks high only because the close rate and churn are untested; the kill experiment measures them.

========================================================================================================
2. MONTHLY P&L AND CASH, BASE scenario (bundle = recert+pmem+cb; $; FT = founder full-time)
========================================================================================================
Month    Idx  Mods  Recert+PMem  CleanBOM  DIMM-h  Revenue    GP   Opex  Salary  EBITDA   Tax   Cash    AR  Inv buy  CB subs  DH cust    ARR  
------  ----  ----  -----------  --------  ------  -------  ----  -----  ------  ------  ----  -----  ----  -------  -------  -------  -----  
Nov-26  1.00     0         0.0k      0.0k    0.0k     0.0k  0.0k   3.3k    0.0k   -3.3k  0.0k  32.0k  0.0k     0.0k      0.0      0.0   0.0k  
Dec-26  1.00     0         0.0k      0.0k    0.0k     0.0k  0.0k   0.8k    0.0k   -0.8k  0.0k  30.6k  0.0k     0.6k      0.0      0.0   0.0k  
Jan-27  1.00     4         5.7k      0.0k    0.0k     5.7k  0.9k   0.8k    0.0k    0.1k  0.0k  29.4k  0.7k     1.2k      0.0      0.0   0.0k  
Feb-27  1.00     7         6.5k      0.0k    0.0k     6.5k  0.9k   2.0k    0.0k   -1.1k  0.0k  26.9k  1.5k     1.8k      0.0      0.0   0.0k  
Mar-27  1.00    11         7.2k      0.0k    0.0k     7.2k  0.9k   2.0k    0.0k   -1.1k  0.0k  24.5k  2.2k     2.4k      0.0      0.0   0.0k  
Apr-27  1.00    15         7.9k      0.0k    0.0k     7.9k  0.9k   2.0k    0.0k   -1.1k  0.0k  20.1k  1.0k     3.0k      0.0      0.0   0.0k  
May-27  1.00    19         8.6k      0.0k    0.0k     8.6k  1.0k   2.0k    0.0k   -1.0k  0.0k  18.1k  1.3k     3.6k      0.0      0.0   0.0k  
Jun-27  1.00    22         9.3k      0.0k    0.0k     9.3k  1.0k   2.0k    0.0k   -1.0k  0.0k  16.2k  1.6k     4.2k      0.0      0.0   0.0k  
Jul-27  1.00    26        10.0k      0.0k    0.0k    10.0k  1.0k   8.0k    0.0k   -7.0k  0.0k   8.5k  2.0k     4.4k      0.0      0.0   0.0k  
Aug-27  1.00    28        10.4k      0.8k    0.0k    11.1k  1.6k   6.0k    0.0k   -4.3k  0.0k   5.0k  2.2k     3.4k      0.2      0.0   2.8k  
Sep-27  1.00    21         9.1k      1.1k    0.0k    10.2k  1.8k   3.0k    0.0k   -1.1k  0.0k   5.0k  1.7k     2.7k      0.5      0.0   5.5k  
Oct-27  1.00    17         8.3k      1.4k    0.0k     9.7k  2.0k   3.0k    0.0k   -0.9k  0.0k   5.0k  1.4k     2.1k      0.7      0.0   8.2k  
Nov-27  1.00    13         4.5k      1.7k    0.0k     6.2k  1.7k   3.0k    0.0k   -1.2k  0.0k   5.0k  1.1k     1.2k      1.0      0.0  10.8k  
Dec-27  1.00     8         3.4k      2.0k    0.0k     5.5k  1.9k   3.0k    0.0k   -1.0k  0.0k   5.0k  0.6k     0.6k      1.2      0.0  13.3k  
Jan-28  0.99     4         2.7k      2.3k    0.0k     5.1k  2.1k  12.9k    0.0k  -10.8k  0.0k  -4.9k  0.3k     0.0k      1.4      0.0  15.8k  
Feb-28  0.98     0         2.0k      2.6k    0.0k     4.6k  2.3k   3.0k    0.0k   -0.6k  0.0k  -5.2k  0.0k     0.0k      1.6      0.0  18.3k  
Mar-28  0.97     0         1.9k      2.9k    0.0k     4.8k  2.5k   3.0k    0.0k   -0.4k  0.0k  -5.6k  0.0k     0.0k      1.9      0.0  20.7k  
Apr-28  0.97     0         1.9k      3.2k    0.0k     5.1k  2.7k   3.0k    0.0k   -0.2k  0.0k  -5.9k  0.0k     0.0k      2.1      0.0  23.1k  
May-28  0.96     0         1.9k      3.4k    0.0k     5.4k  2.9k   2.4k    0.0k    0.6k  0.0k  -5.3k  0.0k     0.0k      2.3      0.0  25.4k  
Jun-28  0.95     0         1.9k      3.7k    0.0k     5.6k  3.1k   2.4k    0.0k    0.8k  0.0k  -4.5k  0.0k     0.0k      2.5      0.0  27.6k  
Jul-28  0.94     0         1.9k      4.0k    0.0k     5.9k  3.3k   2.4k    0.0k    0.9k  0.0k  -3.6k  0.0k     0.0k      2.7      0.0  29.9k  
Aug-28  0.93     0         1.9k      4.2k    0.0k     6.1k  3.5k   2.4k    0.0k    1.1k  0.0k  -2.5k  0.0k     0.0k      2.9      0.0  32.0k  
Sep-28  0.93     0         1.9k      4.5k    0.0k     6.3k  3.7k   2.4k    0.0k    1.3k  0.0k  -1.2k  0.0k     0.0k      3.1      0.0  34.2k  
Oct-28  0.92     0         1.8k      4.7k    0.0k     6.6k  3.8k   2.4k    0.0k    1.5k  0.0k   0.3k  0.0k     0.0k      3.3      0.0  36.3k  
Nov-28  0.91     0         1.8k      5.0k    0.0k     6.8k  4.0k   2.4k    0.0k    1.7k  0.0k   2.0k  0.0k     0.0k      3.5      0.0  38.3k  
Dec-28  0.90     0         1.8k      5.2k    0.0k     7.0k  4.2k   2.4k    0.0k    1.8k  0.0k   3.8k  0.0k     0.0k      3.6      0.0  40.3k  
Jan-29  0.89     0         1.8k      5.4k    0.0k     7.2k  4.3k   5.3k    0.0k   -1.0k  0.0k   2.8k  0.0k     0.0k      3.8      0.0  42.3k  
Feb-29  0.88     0         1.8k      5.7k    0.0k     7.4k  4.5k   2.4k    0.0k    2.2k  0.0k   4.9k  0.0k     0.0k      4.0      0.0  44.2k  
Mar-29  0.87     0         1.7k      5.9k    0.0k     7.6k  4.7k   2.4k    0.0k    2.3k  0.0k   5.0k  0.0k     2.3k      4.2      0.0  46.1k  
Apr-29  0.86    16         4.4k      6.1k    0.0k    10.5k  4.8k   2.4k    0.0k    2.5k  0.0k   5.2k  1.2k     3.4k      4.3      0.0  48.0k  
May-29  0.85    25         5.7k      6.3k    0.0k    12.0k  5.0k   2.4k    0.0k    2.7k  0.0k   7.3k  1.8k     3.3k      4.5      0.0  49.8k  
Jun-29  0.84    24         5.6k      6.5k    0.0k    12.1k  5.2k   2.4k    0.0k    2.8k  0.0k  10.2k  1.7k     3.2k      4.6      0.0  51.6k  
Jul-29  0.83    24         5.5k      6.7k    0.0k    12.2k  5.3k   2.4k    0.0k    2.9k  0.0k  13.3k  1.7k     3.2k      4.8      0.0  53.3k  
Aug-29  0.82    24         5.4k      6.9k    0.0k    12.3k  5.4k   2.4k    0.0k    3.1k  0.0k  16.5k  1.7k     3.1k      5.0      0.0  55.0k  
Sep-29  0.81    24         5.3k      7.1k    0.0k    12.4k  5.6k   2.4k    0.0k    3.2k  0.0k  19.8k  1.6k     3.0k      5.1      0.0  56.7k  
Oct-29  0.80    23         5.2k      7.3k    0.0k    12.5k  5.7k   2.4k    0.0k    3.4k  0.0k  23.3k  1.6k     3.0k      5.3      0.0  58.3k  
  Mods = good recert modules sold. Inv buy = lots bought this month for next month (cash already out).
  Tax = 30% provision on positive taxable income (Phase 5). AR = eBay held proceeds + B2B net-30 invoices (Phase 5),
  collected next month. Recert buying stops (10% trickle) when expected contribution < 5% of price.

========================================================================================================
2. MONTHLY P&L AND CASH, GLUT scenario (bundle = recert+pmem+cb; $; FT = founder full-time)
========================================================================================================
Month    Idx  Mods  Recert+PMem  CleanBOM  DIMM-h  Revenue    GP   Opex  Salary  EBITDA   Tax   Cash    AR  Inv buy  CB subs  DH cust    ARR  
------  ----  ----  -----------  --------  ------  -------  ----  -----  ------  ------  ----  -----  ----  -------  -------  -------  -----  
Nov-26  1.00     0         0.0k      0.0k    0.0k     0.0k  0.0k   3.3k    0.0k   -3.3k  0.0k  32.0k  0.0k     0.0k      0.0      0.0   0.0k  
Dec-26  1.00     0         0.0k      0.0k    0.0k     0.0k  0.0k   0.8k    0.0k   -0.8k  0.0k  30.6k  0.0k     0.6k      0.0      0.0   0.0k  
Jan-27  1.00     4         5.7k      0.0k    0.0k     5.7k  0.9k   0.8k    0.0k    0.1k  0.0k  29.4k  0.7k     1.2k      0.0      0.0   0.0k  
Feb-27  1.00     7         6.5k      0.0k    0.0k     6.5k  0.9k   2.0k    0.0k   -1.1k  0.0k  26.9k  1.5k     1.8k      0.0      0.0   0.0k  
Mar-27  1.00    11         7.2k      0.0k    0.0k     7.2k  0.9k   2.0k    0.0k   -1.1k  0.0k  24.5k  2.2k     2.4k      0.0      0.0   0.0k  
Apr-27  1.00    15         7.9k      0.0k    0.0k     7.9k  0.9k   2.0k    0.0k   -1.1k  0.0k  20.1k  1.0k     3.0k      0.0      0.0   0.0k  
May-27  1.00    19         8.6k      0.0k    0.0k     8.6k  1.0k   2.0k    0.0k   -1.0k  0.0k  18.1k  1.3k     3.6k      0.0      0.0   0.0k  
Jun-27  1.00    22         9.3k      0.0k    0.0k     9.3k  1.0k   2.0k    0.0k   -1.0k  0.0k  16.2k  1.6k     4.2k      0.0      0.0   0.0k  
Jul-27  1.00    26        10.0k      0.0k    0.0k    10.0k  1.0k   8.0k    0.0k   -7.0k  0.0k   8.5k  2.0k     4.4k      0.0      0.0   0.0k  
Aug-27  1.00    28        10.4k      0.8k    0.0k    11.1k  1.6k   6.0k    0.0k   -4.3k  0.0k   5.0k  2.2k     3.4k      0.2      0.0   2.8k  
Sep-27  1.00    21         9.1k      1.1k    0.0k    10.2k  1.8k   3.0k    0.0k   -1.1k  0.0k   5.0k  1.7k     2.7k      0.5      0.0   5.5k  
Oct-27  1.00    17         8.3k      1.4k    0.0k     9.7k  2.0k   3.0k    0.0k   -0.9k  0.0k   5.0k  1.4k     2.1k      0.7      0.0   8.2k  
Nov-27  1.00    13         4.5k      1.7k    0.0k     6.2k  1.7k   3.0k    0.0k   -1.2k  0.0k   5.0k  1.1k     1.2k      1.0      0.0  10.8k  
Dec-27  1.00     8         3.4k      2.0k    0.0k     5.5k  1.9k   3.0k    0.0k   -1.0k  0.0k   5.0k  0.6k     0.6k      1.2      0.0  13.3k  
Jan-28  0.95     4         2.6k      2.3k    0.0k     5.0k  2.1k  12.9k    0.0k  -10.9k  0.0k  -4.9k  0.3k     0.0k      1.4      0.0  15.8k  
Feb-28  0.90     0         1.8k      2.6k    0.0k     4.4k  2.3k   3.0k    0.0k   -0.7k  0.0k  -5.3k  0.0k     0.0k      1.6      0.0  18.3k  
Mar-28  0.85     0         1.7k      2.9k    0.0k     4.6k  2.5k   3.0k    0.0k   -0.5k  0.0k  -5.8k  0.0k     0.0k      1.9      0.0  20.7k  
Apr-28  0.80     0         1.6k      3.2k    0.0k     4.8k  2.6k   3.0k    0.0k   -0.3k  0.0k  -6.1k  0.0k     0.0k      2.1      0.0  23.1k  
May-28  0.75     0         1.5k      3.4k    0.0k     4.9k  2.8k   2.4k    0.0k    0.5k  0.0k  -5.6k  0.0k     0.0k      2.3      0.0  25.4k  
Jun-28  0.70     0         1.4k      3.7k    0.0k     5.1k  3.0k   2.4k    0.0k    0.7k  0.0k  -4.9k  0.0k     0.0k      2.5      0.0  27.6k  
Jul-28  0.65     0         1.3k      4.0k    0.0k     5.3k  3.2k   2.4k    0.0k    0.8k  0.0k  -4.1k  0.0k     0.0k      2.7      0.0  29.9k  
Aug-28  0.60     0         1.2k      4.2k    0.0k     5.4k  3.3k   2.4k    0.0k    1.0k  0.0k  -3.1k  0.0k     0.0k      2.9      0.0  32.0k  
Sep-28  0.55     0         1.1k      4.5k    0.0k     5.6k  3.5k   2.4k    0.0k    1.2k  0.0k  -2.0k  0.0k     0.0k      3.1      0.0  34.2k  
Oct-28  0.50     0         1.0k      4.7k    0.0k     5.7k  3.7k   2.4k    0.0k    1.3k  0.0k  -0.6k  0.0k     0.0k      3.3      0.0  36.3k  
Nov-28  0.45     0         0.9k      5.0k    0.0k     5.9k  3.8k   2.4k    0.0k    1.5k  0.0k   0.8k  0.0k     0.0k      3.5      0.0  38.3k  
Dec-28  0.40     0         0.1k      5.2k    0.0k     5.3k  3.9k   2.4k    0.0k    1.5k  0.0k   2.4k  0.0k     0.0k      3.6      0.0  40.3k  
Jan-29  0.40     0         0.1k      5.4k    0.0k     5.5k  4.1k   5.3k    0.0k   -1.3k  0.0k   1.1k  0.0k     0.0k      3.8      0.0  42.3k  
Feb-29  0.40     0         0.1k      5.7k    0.0k     5.7k  4.2k   2.4k    0.0k    1.9k  0.0k   2.9k  0.0k     0.0k      4.0      0.0  44.2k  
Mar-29  0.40     0         0.1k      5.9k    0.0k     6.0k  4.4k   2.4k    0.0k    2.0k  0.0k   5.0k  0.0k     0.0k      4.2      0.0  46.1k  
Apr-29  0.40     0         0.1k      6.1k    0.0k     6.2k  4.5k   2.4k    0.0k    2.2k  0.0k   6.3k  0.0k     0.9k      4.3      0.0  48.0k  
May-29  0.40    14         1.1k      6.3k    0.0k     7.5k  4.7k   2.4k    0.0k    2.3k  0.0k   8.2k  0.5k     0.9k      4.5      0.0  49.8k  
Jun-29  0.40    14         1.1k      6.5k    0.0k     7.7k  4.8k   2.4k    0.0k    2.5k  0.0k  10.6k  0.5k     0.9k      4.6      0.0  51.6k  
Jul-29  0.40    14         1.1k      6.7k    0.0k     7.9k  5.0k   2.4k    0.0k    2.6k  0.0k  13.3k  0.5k     0.9k      4.8      0.0  53.3k  
Aug-29  0.40    14         1.1k      6.9k    0.0k     8.1k  5.1k   2.4k    0.0k    2.8k  0.0k  16.1k  0.5k     0.9k      5.0      0.0  55.0k  
Sep-29  0.40    14         1.1k      7.1k    0.0k     8.3k  5.3k   2.4k    0.0k    2.9k  0.0k  19.0k  0.5k     0.9k      5.1      0.0  56.7k  
Oct-29  0.40    14         1.1k      7.3k    0.0k     8.5k  5.4k   2.4k    0.0k    3.1k  0.0k  22.1k  0.5k     0.9k      5.3      0.0  58.3k  
  Mods = good recert modules sold. Inv buy = lots bought this month for next month (cash already out).
  Tax = 30% provision on positive taxable income (Phase 5). AR = eBay held proceeds + B2B net-30 invoices (Phase 5),
  collected next month. Recert buying stops (10% trickle) when expected contribution < 5% of price.

========================================================================================================
2. MONTHLY P&L AND CASH, SEVERE scenario (bundle = recert+pmem+cb; $; FT = founder full-time)
========================================================================================================
Month    Idx  Mods  Recert+PMem  CleanBOM  DIMM-h  Revenue    GP   Opex  Salary  EBITDA   Tax   Cash    AR  Inv buy  CB subs  DH cust    ARR  
------  ----  ----  -----------  --------  ------  -------  ----  -----  ------  ------  ----  -----  ----  -------  -------  -------  -----  
Nov-26  1.00     0         0.0k      0.0k    0.0k     0.0k  0.0k   3.3k    0.0k   -3.3k  0.0k  32.0k  0.0k     0.0k      0.0      0.0   0.0k  
Dec-26  1.00     0         0.0k      0.0k    0.0k     0.0k  0.0k   0.8k    0.0k   -0.8k  0.0k  30.6k  0.0k     0.6k      0.0      0.0   0.0k  
Jan-27  1.00     4         5.7k      0.0k    0.0k     5.7k  0.9k   0.8k    0.0k    0.1k  0.0k  29.4k  0.7k     1.2k      0.0      0.0   0.0k  
Feb-27  1.00     7         6.5k      0.0k    0.0k     6.5k  0.9k   2.0k    0.0k   -1.1k  0.0k  26.9k  1.5k     1.8k      0.0      0.0   0.0k  
Mar-27  1.00    11         7.2k      0.0k    0.0k     7.2k  0.9k   2.0k    0.0k   -1.1k  0.0k  24.5k  2.2k     2.4k      0.0      0.0   0.0k  
Apr-27  1.00    15         7.9k      0.0k    0.0k     7.9k  0.9k   2.0k    0.0k   -1.1k  0.0k  20.1k  1.0k     3.0k      0.0      0.0   0.0k  
May-27  1.00    19         8.6k      0.0k    0.0k     8.6k  1.0k   2.0k    0.0k   -1.0k  0.0k  18.1k  1.3k     3.6k      0.0      0.0   0.0k  
Jun-27  1.00    22         9.3k      0.0k    0.0k     9.3k  1.0k   2.0k    0.0k   -1.0k  0.0k  16.2k  1.6k     4.2k      0.0      0.0   0.0k  
Jul-27  1.00    26        10.0k      0.0k    0.0k    10.0k  1.0k   8.0k    0.0k   -7.0k  0.0k   8.5k  2.0k     4.4k      0.0      0.0   0.0k  
Aug-27  1.00    28        10.4k      0.8k    0.0k    11.1k  1.6k   6.0k    0.0k   -4.3k  0.0k   5.0k  2.2k     3.4k      0.2      0.0   2.8k  
Sep-27  1.00    21         9.1k      1.1k    0.0k    10.2k  1.8k   3.0k    0.0k   -1.1k  0.0k   5.0k  1.7k     2.7k      0.5      0.0   5.5k  
Oct-27  1.00    17         8.3k      1.4k    0.0k     9.7k  2.0k   3.0k    0.0k   -0.9k  0.0k   5.0k  1.4k     2.1k      0.7      0.0   8.2k  
Nov-27  1.00    13         4.5k      1.7k    0.0k     6.2k  1.7k   3.0k    0.0k   -1.2k  0.0k   5.0k  1.1k     1.2k      1.0      0.0  10.8k  
Dec-27  1.00     8         3.4k      2.0k    0.0k     5.5k  1.9k   3.0k    0.0k   -1.0k  0.0k   5.0k  0.6k     0.6k      1.2      0.0  13.3k  
Jan-28  0.93     4         2.6k      2.3k    0.0k     4.9k  2.0k  12.9k    0.0k  -10.9k  0.0k  -4.9k  0.3k     0.0k      1.4      0.0  15.8k  
Feb-28  0.85     0         1.7k      2.6k    0.0k     4.3k  2.3k   3.0k    0.0k   -0.7k  0.0k  -5.3k  0.0k     0.0k      1.6      0.0  18.3k  
Mar-28  0.78     0         1.6k      2.9k    0.0k     4.4k  2.4k   3.0k    0.0k   -0.5k  0.0k  -5.8k  0.0k     0.0k      1.9      0.0  20.7k  
Apr-28  0.70     0         1.4k      3.2k    0.0k     4.6k  2.6k   3.0k    0.0k   -0.3k  0.0k  -6.2k  0.0k     0.0k      2.1      0.0  23.1k  
May-28  0.63     0         1.3k      3.4k    0.0k     4.7k  2.8k   2.4k    0.0k    0.4k  0.0k  -5.8k  0.0k     0.0k      2.3      0.0  25.4k  
Jun-28  0.55     0         1.1k      3.7k    0.0k     4.8k  2.9k   2.4k    0.0k    0.6k  0.0k  -5.2k  0.0k     0.0k      2.5      0.0  27.6k  
Jul-28  0.48     0         1.0k      4.0k    0.0k     4.9k  3.1k   2.4k    0.0k    0.8k  0.0k  -4.4k  0.0k     0.0k      2.7      0.0  29.9k  
Aug-28  0.40     0         0.1k      4.2k    0.0k     4.3k  3.2k   2.4k    0.0k    0.8k  0.0k  -3.6k  0.0k     0.0k      2.9      0.0  32.0k  
Sep-28  0.33     0         0.1k      4.5k    0.0k     4.5k  3.4k   2.4k    0.0k    1.0k  0.0k  -2.6k  0.0k     0.0k      3.1      0.0  34.2k  
Oct-28  0.25     0         0.1k      4.7k    0.0k     4.8k  3.5k   2.4k    0.0k    1.2k  0.0k  -1.4k  0.0k     0.0k      3.3      0.0  36.3k  
Nov-28  0.18     0         0.0k      5.0k    0.0k     5.0k  3.7k   2.4k    0.0k    1.4k  0.0k  -0.0k  0.0k     0.0k      3.5      0.0  38.3k  
Dec-28  0.10     0         0.0k      5.2k    0.0k     5.2k  3.9k   2.4k    0.0k    1.5k  0.0k   1.5k  0.0k     0.0k      3.6      0.0  40.3k  
Jan-29  0.10     0         0.0k      5.4k    0.0k     5.5k  4.0k   5.3k    0.0k   -1.3k  0.0k   0.2k  0.0k     0.0k      3.8      0.0  42.3k  
Feb-29  0.10     0         0.0k      5.7k    0.0k     5.7k  4.2k   2.4k    0.0k    1.9k  0.0k   2.0k  0.0k     0.0k      4.0      0.0  44.2k  
Mar-29  0.10     0         0.0k      5.9k    0.0k     5.9k  4.4k   2.4k    0.0k    2.0k  0.0k   4.1k  0.0k     0.0k      4.2      0.0  46.1k  
Apr-29  0.10     0         0.0k      6.1k    0.0k     6.1k  4.5k   2.4k    0.0k    2.2k  0.0k   5.8k  0.0k     0.5k      4.3      0.0  48.0k  
May-29  0.10    14         0.6k      6.3k    0.0k     6.9k  4.7k   2.4k    0.0k    2.3k  0.0k   7.8k  0.2k     0.5k      4.5      0.0  49.8k  
Jun-29  0.10    14         0.6k      6.5k    0.0k     7.1k  4.8k   2.4k    0.0k    2.5k  0.0k  10.3k  0.2k     0.5k      4.6      0.0  51.6k  
Jul-29  0.10    14         0.6k      6.7k    0.0k     7.3k  5.0k   2.4k    0.0k    2.6k  0.0k  12.9k  0.2k     0.5k      4.8      0.0  53.3k  
Aug-29  0.10    14         0.6k      6.9k    0.0k     7.5k  5.1k   2.4k    0.0k    2.8k  0.0k  15.6k  0.2k     0.5k      5.0      0.0  55.0k  
Sep-29  0.10    14         0.6k      7.1k    0.0k     7.7k  5.2k   2.4k    0.0k    2.9k  0.0k  18.5k  0.2k     0.5k      5.1      0.0  56.7k  
Oct-29  0.10    14         0.6k      7.3k    0.0k     7.9k  5.4k   2.4k    0.0k    3.0k  0.0k  21.6k  0.2k     0.5k      5.3      0.0  58.3k  
  Mods = good recert modules sold. Inv buy = lots bought this month for next month (cash already out).
  Tax = 30% provision on positive taxable income (Phase 5). AR = eBay held proceeds + B2B net-30 invoices (Phase 5),
  collected next month. Recert buying stops (10% trickle) when expected contribution < 5% of price.

========================================================================================================
3. SCENARIO SUMMARY (bundle = recert+pmem+cb)
========================================================================================================
Scenario  Breakeven (actual)  Breakeven @$10k salary      Cash low  Cash+inv low  ARR m12  ARR m18  ARR m24  ARR m36  Run-rate m18  Run-rate m36  Cash m36  Inventory m36  Founder FT from
--------  ------------------  ----------------------  ------------  ------------  -------  -------  -------  -------  ------------  ------------  --------  -------------  ---------------
BASE            m19 (May-28)                   never  $-5,863 @m18  $-5,863 @m18   $8,160  $23,067  $36,274  $58,335       $61,244      $150,124   $23,270         $2,965            never
GLUT            m19 (May-28)                   never  $-6,061 @m18  $-6,061 @m18   $8,160  $23,067  $36,274  $58,335       $57,244      $101,676   $22,086           $890            never
SEVERE          m19 (May-28)                   never  $-6,179 @m18  $-6,179 @m18   $8,160  $23,067  $36,274  $58,335       $54,844       $94,884   $21,588           $466            never
  The operator buys inventory down to the $5k reserve, so a cash low AT the reserve is working capital; a low
  BELOW it is operating losses (Phase 5 BASE: CleanBOM's fixed costs before it covers them).
  'Cash+inv low' adds back the lots bought that month.
  BASE   cumulative EBITDA $-3,473; tax provision $0; receivables at m36 $1,592; founder full-time months 0
  GLUT   cumulative EBITDA $-7,852; tax provision $0; receivables at m36 $473; founder full-time months 0
  SEVERE cumulative EBITDA $-8,998; tax provision $0; receivables at m36 $248; founder full-time months 0
  ARR = recurring only (CleanBOM subscriptions + DIMM-health) x 12. Run-rate = all revenue in that month x 12.
  'Breakeven (actual)' = first of 3 straight months with EBITDA >= 0 as actually incurred (founder unpaid
  until the full-time trigger). 'Breakeven @$10k salary' charges a market founder salary every month.
  BASE   cumulative revenue $273,517: recert+PMem $156,667 (57%), CleanBOM $116,851, DIMM-health $0; recert modules sold 355
  GLUT   cumulative revenue $231,157: recert+PMem $114,307 (49%), CleanBOM $116,851, DIMM-health $0; recert modules sold 278
  SEVERE cumulative revenue $222,072: recert+PMem $105,221 (47%), CleanBOM $116,851, DIMM-health $0; recert modules sold 278
  Gross margin over 36 months (GP / revenue; recert GP is after technician labor):
  BASE   blended 38% | recert+PMem 11% | CleanBOM 75% | DIMM-health n/a
  GLUT   blended 43% | recert+PMem 11% | CleanBOM 75% | DIMM-health n/a
  SEVERE blended 44% | recert+PMem 11% | CleanBOM 75% | DIMM-health n/a
  Die-source library by m36: 24 lab samples (Phase 5: validation/exception samples of NEW third-party DDR5
  RDIMMs bought at market, keyed on DRAM package marking + die outline; NOT module-P/N coverage).

========================================================================================================
4. IS THE WHOLE BETTER THAN ITS PARTS?  (same founder, same $40k, run line-by-line)
========================================================================================================
Scenario  Configuration                              Cash low     Breakeven  ARR m18  ARR m36  Run-rate m36  Cash m36  Cum EBITDA  FT months
--------  ------------------------------------  -------------  ------------  -------  -------  ------------  --------  ----------  ---------
BASE      Bundle (recert+pmem+cb)                $-5,863 @m18  m19 (May-28)  $23,067  $58,335      $150,124   $23,270     $-3,473          0
          Recert + PMem only                      $4,815 @m36   m3 (Jan-27)       $0       $0       $21,565    $4,815    $-26,398          0
          CleanBOM standalone                   $-10,164 @m18  m19 (May-28)  $23,067  $58,335       $87,952   $18,068    $-20,432          0
          DIMM-health standalone                   $-849 @m30  m28 (Feb-29)   $8,674  $27,187       $27,187       $83    $-26,165          0
BASE      Bundle + DIMM-health (Phase 4 line)    $-6,423 @m18  m18 (Apr-28)  $31,741  $85,522      $177,310   $34,121     $16,811          0
BASE      Bundle, no evidence lift               $-5,863 @m18  m19 (May-28)  $23,067  $58,335      $150,124   $23,270     $-3,473          0
BASE      Bundle, founder never FT               $-5,863 @m18  m19 (May-28)  $23,067  $58,335      $150,124   $23,270     $-3,473          0
BASE      Bundle, FT gate >=5 subs (DD §11 #7)   $-5,863 @m18  m19 (May-28)  $23,067  $58,335      $150,124   $23,270     $-3,473          0
GLUT      Bundle (recert+pmem+cb)                $-6,061 @m18  m19 (May-28)  $23,067  $58,335      $101,676   $22,086     $-7,852          0
          Recert + PMem only                     $-1,761 @m36   m3 (Jan-27)       $0       $0          $960   $-1,761    $-33,061          0
          CleanBOM standalone                   $-10,164 @m18  m19 (May-28)  $23,067  $58,335       $87,952   $18,068    $-20,432          0
          DIMM-health standalone                  $2,090 @m27  m24 (Oct-28)   $8,239  $21,868       $21,868    $4,748    $-25,225          0
GLUT      Bundle + DIMM-health (Phase 4 line)    $-6,356 @m18  m18 (Apr-28)  $31,307  $80,203      $123,544   $36,898     $12,158          0
GLUT      Bundle, no evidence lift               $-6,061 @m18  m19 (May-28)  $23,067  $58,335      $101,676   $22,086     $-7,852          0
GLUT      Bundle, founder never FT               $-6,061 @m18  m19 (May-28)  $23,067  $58,335      $101,676   $22,086     $-7,852          0
GLUT      Bundle, FT gate >=5 subs (DD §11 #7)   $-6,061 @m18  m19 (May-28)  $23,067  $58,335      $101,676   $22,086     $-7,852          0
SEVERE    Bundle (recert+pmem+cb)                $-6,179 @m18  m19 (May-28)  $23,067  $58,335       $94,884   $21,588     $-8,998          0
          Recert + PMem only                     $-3,508 @m36   m3 (Jan-27)       $0       $0          $240   $-3,508    $-34,808          0
          CleanBOM standalone                   $-10,164 @m18  m19 (May-28)  $23,067  $58,335       $87,952   $18,068    $-20,432          0
          DIMM-health standalone                  $3,278 @m27  m23 (Sep-28)   $8,239  $21,868       $21,868    $6,912    $-23,928          0
SEVERE    Bundle + DIMM-health (Phase 4 line)    $-6,355 @m18  m18 (Apr-28)  $31,307  $80,203      $116,751   $38,025     $11,911          0
SEVERE    Bundle, no evidence lift               $-6,179 @m18  m19 (May-28)  $23,067  $58,335       $94,884   $21,588     $-8,998          0
SEVERE    Bundle, founder never FT               $-6,179 @m18  m19 (May-28)  $23,067  $58,335       $94,884   $21,588     $-8,998          0
SEVERE    Bundle, FT gate >=5 subs (DD §11 #7)   $-6,179 @m18  m19 (May-28)  $23,067  $58,335       $94,884   $21,588     $-8,998          0
  Standalone CleanBOM closes at 5% vs 5% in the bundle. Phase 5: the two are equal and the bundle
  pays for library modules too, because recert flow samples the wrong population (RT-PHY-DD1-01 et al.).
  Standalone DIMM-health buys spares at resale, not recert buy cost.
  'No evidence lift' keeps the recert cash but gives CleanBOM the standalone close rate and sample cost:
  the gap to the full bundle is what the die-source library is worth; the gap to 'founder never FT' is
  what recert cash (buying founder time) is worth.

========================================================================================================
5. SENSITIVITY (BASE scenario, bundle; one input moved at a time)
========================================================================================================
Input                                      Move      Breakeven  Cash low  ARR m18   ARR m36  Cash m36  Cum EBITDA
-----------------------------------------  -----  ------------  --------  -------  --------  --------  ----------
Base case                                  --     m19 (May-28)   $-5,863  $23,067   $58,335   $23,270     $-3,473
Recert resale price                        -30%   m19 (May-28)  $-10,251  $23,067   $58,335   $18,076    $-10,035
Recert resale price                        +30%   m19 (May-28)   $-2,092  $23,067   $58,335   $28,936      $3,560
SaaS / subscription price                  -30%   m20 (Jun-28)   $-9,713  $16,147   $40,835    $4,862    $-26,438
SaaS / subscription price                  +30%   m17 (Mar-28)   $-3,457  $29,988   $75,836   $43,051     $19,568
Close rate (CB + DH)                       -30%   m20 (Jun-28)   $-9,066  $16,147   $40,835    $4,634    $-26,666
Close rate (CB + DH)                       +30%   m17 (Mar-28)   $-3,809  $29,988   $75,836   $43,198     $19,778
Churn (CB + DH)                            -30%   m19 (May-28)   $-5,700  $23,621   $62,754   $27,114        $371
Churn (CB + DH)                            +30%   m19 (May-28)   $-6,023  $22,529   $54,325   $19,693     $-7,050
COGS (buy %, fees, lab, hosting)           -30%    m3 (Jan-27)    $5,652  $45,243  $132,970  $257,903    $398,572
COGS (buy %, fees, lab, hosting)           +30%   m20 (Jun-28)  $-26,707  $23,067   $58,335   $-7,748    $-39,048
Final FAR rule slips 6 mo (CB launch m16)  +6 mo  m23 (Sep-28)  $-12,889   $8,160   $47,972    $3,240    $-28,060
Founder stays part-time all 36 months      PT     m19 (May-28)   $-5,863  $23,067   $58,335   $23,270     $-3,473
ITAD buy fraction = 0.55                   abs     m3 (Jan-27)    $5,000  $23,067   $58,335  $134,797    $200,143
ITAD buy fraction = 0.60                   abs     m3 (Jan-27)    $5,000  $23,067   $58,335   $67,498    $107,028
ITAD buy fraction = 0.62                   abs     m3 (Jan-27)    $5,000  $23,067   $58,335   $41,777     $71,494
ITAD buy fraction = 0.65                   abs     m3 (Jan-27)    $3,407  $23,067   $58,335   $37,054     $10,698
ITAD buy fraction = 0.75                   abs    m19 (May-28)   $-7,818  $23,067   $58,335   $19,750     $-6,781
B2B price factor = 0.75                    abs    m19 (May-28)   $-6,711  $23,067   $58,335   $21,883     $-4,960
B2B price factor = 0.88                    abs    m19 (May-28)   $-4,197  $23,067   $58,335   $26,013       $-571
  Glut and severe sensitivities: see sections 3-4 (CleanBOM is price-independent; recert is not).

========================================================================================================
6. WHAT MUST BE TRUE
========================================================================================================
a) Recert: lots must cost less than 72% (eBay) / 66% (B2B) / 69% (m12 mix) of realized resale for any
   contribution at today's prices; at the modeled 70% the mixed-channel margin is $-3 per module (-1%).
b) Recert cannot cover a founder salary + ~$3,550 fixed opex at ANY volume: contribution is $-3 per module at 70% buy.
c) For the business to survive the glut on recurring revenue alone, CleanBOM needs ~14 paying subscribers (at $958 GP/sub-month)
   by the 2028 turn (month 15-18). Modeled BASE: 2.1 subscribers at m18, 5.3 at m36.
   Getting there by m18 from a m10 launch needs a 34% close rate at 5 conversations/month, or 34 conversations/month at a 5% close.
d) Equivalently: by month 18 the founder needs ~14 signed provenance customers (e.g. 1 high-tier white-box builders at $2500 + 13 resellers/integrators at $750).
e) DIMM-health must sell at 4.1x the buyer's DIY spares cost against free OEM/BMC prediction (Lenovo MPFA,
   Intel MFP) and ParkView-bundled TPM: it must be sold as a wholesale feed + spares to TPMs/MSPs, or dropped.
f) $1M ARR at m36 would need ~90 CleanBOM subscribers at the blended ARPA; the model reaches 5.3.
g) (Phase 5) For the 8% contribution that kill track A requires, lots must cost <= 62% of realized resale
   (m12 mix), or <= 64% selling eBay-only; the 5% buy/no-buy line sits at 65%.

========================================================================================================
7. GLUT BEHAVIOR PER LINE (steady-state unit margin and modeled revenue in the last 12 months)
========================================================================================================
Scenario  Idx m36  Recert GM  PMem GM  CleanBOM GM  Recert rev (last 12m)  CB rev (last 12m)  DH rev (last 12m)  DH cust m36
--------  -------  ---------  -------  -----------  ---------------------  -----------------  -----------------  -----------
BASE         0.80        -3%      12%          73%                $45,907            $74,268                 $0          0.0
GLUT         0.40       -10%       4%          73%                 $8,162            $74,268                 $0          0.0
SEVERE       0.10       -23%     -46%          73%                 $3,601            $74,268                 $0          0.0
  Recert dies as a profit line in GLUT/SEVERE (buying stops; trickle kept for spares/library). PMem dies on
  2027-10-11 (VMware) regardless. CleanBOM is unaffected by price. DIMM-health margin rises (cheap spares) but
  customers churn faster once DDR5 refresh is cheap.

========================================================================================================
8. RED-TEAM ATTRIBUTION AND VARIANTS (Phase 5)
========================================================================================================

8a. Phase 4 inputs reproduced (P_PHASE4), then revision groups applied CUMULATIVELY (BASE):
Run                                                                                            Scn   Recert/module   ARR m18   ARR m36  Cash m36      Cash low    Founder FT  BE @$10k salary  CB subs m18/m36  Cum EBITDA
---------------------------------------------------------------------------------------------  ----  -------------  --------  --------  --------  ------------  ------------  ---------------  ---------------  ----------
Phase 4 (as published)                                                                         BASE      $37 (15%)  $139,995  $445,543  $610,097   $5,000 @m10  m14 (Dec-27)     m11 (Sep-27)       7.5 / 23.5    $662,971
+ Tax provision 30% (VC-07)                                                                    BASE      $37 (15%)  $102,721  $419,301  $378,961    $5,000 @m7  m17 (Mar-28)     m11 (Sep-27)       5.5 / 22.1    $612,032
+ Cash cycle: eBay limits/holds, B2B net-30 (VC-04)                                            BASE      $37 (15%)   $76,629  $340,928  $215,670    $5,000 @m4  m24 (Oct-28)     m17 (Mar-28)       4.2 / 18.0    $455,577
+ Buy fraction 0.70 + supply caps 300/450 (HYP-04, VC-05)                                      BASE       $23 (9%)   $76,629  $308,396  $108,125    $5,000 @m4  m26 (Dec-28)     m20 (Jun-28)       4.2 / 16.3    $261,861
+ B2B at 0.80x eBay, eBay share 0.50 (HYP-05, VET-05)                                          BASE       $12 (5%)   $76,629  $250,221  $131,750    $5,000 @m4  m33 (Jul-29)     m28 (Feb-29)       4.2 / 13.2    $163,610
+ CE-logging test protocol: fallout 7%, returns 3% (VET-03, PHY-03)                            BASE       $0 (-0%)   $76,629  $237,798  $119,753   $5,000 @m15  m34 (Aug-29)     m28 (Feb-29)       4.2 / 12.6    $146,867
+ SKU mix: DDR5 10% -> 3% (VET-04)                                                             BASE      $-3 (-1%)   $76,629  $237,798  $120,542   $5,000 @m15  m34 (Aug-29)     m28 (Feb-29)       4.2 / 12.6    $145,196
+ PMem fallout/returns (PHY-05, VET-07)                                                        BASE      $-3 (-1%)   $76,629  $237,798  $114,512   $3,318 @m15  m34 (Aug-29)     m28 (Feb-29)       4.2 / 12.6    $136,582
+ DIMM-health subscription dropped (PHY-04)                                                    BASE      $-3 (-1%)   $67,956  $171,852  $129,026   $4,050 @m15         never     m30 (Apr-29)       4.2 / 10.5    $142,389
+ Library re-keyed, bought at market, lab $600 (PHY-01/02, HYP-02/03, VC-02/03, VET-02/06)     BASE      $-3 (-1%)   $67,956  $183,297  $123,595   $4,540 @m15  m36 (Oct-29)     m30 (Apr-29)       4.2 / 11.2    $136,749
+ CleanBOM demand: close 5%, high tier 10%, packs 10% (HYP-01, VC-01, VET-01, HYP-06, HYP-07)  BASE      $-3 (-1%)   $23,067   $58,335   $28,798  $-4,026 @m15         never            never        2.1 / 5.3      $2,055
+ E&O $600/month (HYP-08)                                                                      BASE      $-3 (-1%)   $23,067   $58,335   $23,270  $-5,863 @m18         never            never        2.1 / 5.3     $-3,473

8b. Each revision group applied ALONE to Phase 4 inputs (BASE):
Run                                                                                          Scn   Recert/module   ARR m18   ARR m36  Cash m36     Cash low    Founder FT  BE @$10k salary  CB subs m18/m36  Cum EBITDA
-------------------------------------------------------------------------------------------  ----  -------------  --------  --------  --------  -----------  ------------  ---------------  ---------------  ----------
Phase 4 (as published)                                                                       BASE      $37 (15%)  $139,995  $445,543  $610,097  $5,000 @m10  m14 (Dec-27)     m11 (Sep-27)       7.5 / 23.5    $662,971
Tax provision 30% (VC-07)                                                                    BASE      $37 (15%)  $102,721  $419,301  $378,961   $5,000 @m7  m17 (Mar-28)     m11 (Sep-27)       5.5 / 22.1    $612,032
Cash cycle: eBay limits/holds, B2B net-30 (VC-04)                                            BASE      $37 (15%)   $76,629  $381,840  $401,278   $5,000 @m4  m21 (Jul-28)     m16 (Feb-28)       4.2 / 20.2    $508,291
Buy fraction 0.70 + supply caps 300/450 (HYP-04, VC-05)                                      BASE       $23 (9%)   $76,629  $341,342  $269,089  $5,000 @m12  m25 (Nov-28)     m19 (May-28)       4.2 / 18.0    $305,518
B2B at 0.80x eBay, eBay share 0.50 (HYP-05, VET-05)                                          BASE      $26 (11%)   $76,629  $400,936  $399,126  $5,000 @m10  m19 (May-28)     m16 (Feb-28)       4.2 / 21.2    $450,405
CE-logging test protocol: fallout 7%, returns 3% (VET-03, PHY-03)                            BASE      $25 (10%)   $76,629  $381,840  $344,113  $5,000 @m12  m21 (Jul-28)     m16 (Feb-28)       4.2 / 20.2    $395,890
SKU mix: DDR5 10% -> 3% (VET-04)                                                             BASE      $27 (14%)   $76,629  $400,936  $428,963  $5,000 @m10  m19 (May-28)     m12 (Oct-27)       4.2 / 21.2    $464,460
PMem fallout/returns (PHY-05, VET-07)                                                        BASE      $37 (15%)  $139,995  $445,543  $599,228   $5,000 @m6  m14 (Dec-27)     m11 (Sep-27)       7.5 / 23.5    $652,103
DIMM-health subscription dropped (PHY-04)                                                    BASE      $37 (15%)  $122,937  $384,530  $580,439  $5,000 @m10  m14 (Dec-27)     m11 (Sep-27)       7.5 / 23.5    $619,489
Library re-keyed, bought at market, lab $600 (PHY-01/02, HYP-02/03, VC-02/03, VET-02/06)     BASE      $37 (15%)  $139,995  $445,543  $622,226   $5,000 @m9  m14 (Dec-27)     m11 (Sep-27)       7.5 / 23.5    $675,100
CleanBOM demand: close 5%, high tier 10%, packs 10% (HYP-01, VC-01, VET-01, HYP-06, HYP-07)  BASE      $37 (15%)   $53,382  $187,670  $318,493   $5,000 @m9  m14 (Dec-27)     m11 (Sep-27)       3.4 / 11.5    $371,048
E&O $600/month (HYP-08)                                                                      BASE      $37 (15%)  $139,995  $445,543  $604,657   $5,000 @m9  m14 (Dec-27)     m11 (Sep-27)       7.5 / 23.5    $657,531

8c. Reviewers' own runs, re-run on Phase 4 inputs (checks their numbers):
Run                                          Scn   Recert/module   ARR m18   ARR m36  Cash m36     Cash low    Founder FT  BE @$10k salary  CB subs m18/m36  Cum EBITDA
-------------------------------------------  ----  -------------  --------  --------  --------  -----------  ------------  ---------------  ---------------  ----------
HYP-05: B2B 0.80                             BASE      $24 (10%)   $76,629  $391,481  $367,204   $5,000 @m6  m20 (Jun-28)     m16 (Feb-28)       4.2 / 20.7    $418,158
HYP-05/VET-05: B2B 0.75                      BASE       $17 (7%)   $76,629  $341,342  $238,343  $5,000 @m14  m25 (Nov-28)     m19 (May-28)       4.2 / 18.0    $287,656
HYP-05/VET-05: B2B 0.75                      GLUT       $17 (7%)   $76,195  $232,377  $214,896  $5,000 @m14  m34 (Aug-29)     m28 (Feb-29)       4.2 / 12.6    $189,426
HYP-05: B2B 0.80 + buy 0.70                  BASE       $10 (4%)   $76,629  $250,221  $178,487   $5,000 @m5  m33 (Jul-29)     m28 (Feb-29)       4.2 / 13.2    $162,428
HYP-06: high-tier share 0.15                 BASE      $37 (15%)  $108,415  $346,764  $509,169   $5,000 @m9  m14 (Dec-27)     m11 (Sep-27)       7.5 / 23.5    $562,044
HYP-06: high-tier share 0.15                 GLUT      $37 (15%)  $107,652  $335,234  $291,191   $5,000 @m9  m14 (Dec-27)     m11 (Sep-27)       7.5 / 23.5    $288,653
VET-03: fallout 8%, returns 5%               BASE       $19 (8%)   $76,629  $351,765  $247,820  $5,000 @m13  m24 (Oct-28)     m19 (May-28)       4.2 / 18.6    $298,005
VET-04: no DDR5 (70/30 DDR4)                 BASE      $21 (13%)   $76,629  $372,010  $344,648  $5,000 @m10  m22 (Aug-28)     m17 (Mar-28)       4.2 / 19.7    $371,031
VET-04: no DDR5 + 8%/5% + buy 0.70           BASE       $0 (-0%)   $76,629  $237,798  $165,244  $6,564 @m15  m34 (Aug-29)     m28 (Feb-29)       4.2 / 12.6    $146,639
VET-06: lab $1,200, close 7%                 BASE      $37 (15%)   $56,243  $297,042  $401,241   $5,000 @m6  m19 (May-28)     m16 (Feb-28)       2.9 / 14.8    $452,519
PHY-01: library modules $1,000, bundled too  BASE      $37 (15%)   $56,243  $290,023  $329,449  $5,000 @m14  m20 (Jun-28)     m17 (Mar-28)       2.9 / 14.5    $380,404

8d. Revised model (P0) under stress and under the kill-test outcomes:
Run                                                   Scn     Recert/module  ARR m18   ARR m36  Cash m36       Cash low    Founder FT  BE @$10k salary  CB subs m18/m36  Cum EBITDA
----------------------------------------------------  ------  -------------  -------  --------  --------  -------------  ------------  ---------------  ---------------  ----------
Revised base                                          BASE        $-3 (-1%)  $23,067   $58,335   $23,270   $-5,863 @m18         never            never        2.1 / 5.3     $-3,473
Revised base                                          GLUT        $-3 (-1%)  $23,067   $58,335   $22,086   $-6,061 @m18         never            never        2.1 / 5.3     $-7,852
Revised base                                          SEVERE      $-3 (-1%)  $23,067   $58,335   $21,588   $-6,179 @m18         never            never        2.1 / 5.3     $-8,998
Turn early (Oct-27)                                   GLUT        $-3 (-1%)  $23,067   $58,335   $20,740   $-6,777 @m18         never            never        2.1 / 5.3     $-9,197
FAR rule slips 6 months                               BASE        $-3 (-1%)   $8,160   $47,972    $3,240  $-12,889 @m27         never            never        0.7 / 4.3    $-28,060
CleanBOM sells nothing                                BASE        $-3 (-1%)       $0        $0  $-59,798  $-59,798 @m36         never            never        0.0 / 0.0    $-91,098
Recert + PMem only                                    BASE        $-3 (-1%)       $0        $0    $4,815    $4,815 @m36         never            never        0.0 / 0.0    $-26,398
No tax provision (VC-07 check)                        BASE        $-3 (-1%)  $23,067   $58,335   $23,270   $-5,863 @m18         never            never        2.1 / 5.3     $-3,473
Track A passes at buy 0.62                            BASE         $16 (8%)  $23,067   $58,335   $41,777     $5,000 @m4         never            never        2.1 / 5.3     $71,494
Track A passes at buy 0.62                            GLUT         $16 (8%)  $23,067   $58,335   $48,983     $5,000 @m4         never            never        2.1 / 5.3     $23,333
Track C passes (close 10%, high tier 35%, packs 15%)  BASE        $-3 (-1%)  $67,956  $171,852  $128,084    $3,326 @m15         never     m30 (Apr-29)       4.2 / 10.5    $141,044
Tracks A (0.62) and C both pass                       BASE         $16 (8%)  $67,956  $226,833  $106,959     $5,000 @m4  m32 (Jun-29)     m28 (Feb-29)       4.2 / 13.9    $194,738
Tracks A (0.62) and C both pass                       GLUT         $16 (8%)  $67,956  $171,852  $150,359     $5,000 @m4         never     m31 (May-29)       4.2 / 10.5    $168,156
Tracks A (0.62) and C both pass                       SEVERE       $16 (8%)  $67,956  $171,852  $148,278     $5,000 @m4         never     m31 (May-29)       4.2 / 10.5    $164,327
A + C pass, FT gate >=5 subs                          BASE         $16 (8%)  $67,956  $226,833  $106,959     $5,000 @m4  m32 (Jun-29)     m28 (Feb-29)       4.2 / 13.9    $194,738
  Track C 'passes' restores the Phase 4 CleanBOM demand inputs (what the red team says is unproven).
  Under the revised inputs, kill criteria 1-2 fire on day 29: recert is not bought and CleanBOM is not built.

Done. exit 0
```
