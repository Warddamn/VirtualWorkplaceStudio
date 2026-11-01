# DD1 Provenance & Recertified Memory: model output

Produced by `python3 models/provenance-recert.py`, run from `/home/user/VirtualWorkplaceStudio/ram-venture` on 2026-11-01 (exit 0). Pure stdlib. The DDR5 deck is a live import of `models/dram_cost_stack.py ddr5_reference()`. Inputs and their sources are in the INPUTS block of the script, and assumptions are in `research/assumptions/p4-provenance-recert.md`. The research notes are `research/phase4/provenance-recert_notes.md`.

```
DD1 Provenance & Recertified Memory -- unit economics and 36-month P&L (models/provenance-recert.py)
As of 2026-11-01. Month 1 = Nov-26, month 36 = Oct-29. DDR5 deck: models/dram_cost_stack.py ddr5_reference() (live import)
  DDR5 component cost $1.48/GB | Q4-26 contract $20.37/GB | glut $8.15/GB (x0.40) | severe $2.04/GB (x0.10)
  New 64GB DDR5 RDIMM contract $25.78/user-GB; used 64GB DDR5 resale $16.33/GB = 63% of new (amcompute 55-74% band check)
  Used resale index applied to all recert SKUs, PMem and spares; CleanBOM demand is statutory (same in all).
  INPUTS: 97 values, each with a source or 'ESTIMATE: basis' (see the INPUTS dict in this file).

========================================================================================================
1. UNIT ECONOMICS PER PRODUCT LINE (per unit, at each price deck; steady state, no inventory lag)
========================================================================================================

1a. Recert RDIMM (mix 60% 32GB DDR4 / 30% 64GB DDR4 / 10% 64GB DDR5), per good module; buy at 65% of realized resale
Deck                  Channel  Price  Buy+fallout  Fees+ship  Ret+cons+labor  Contrib   GM
--------------------  -------  -----  -----------  ---------  --------------  -------  ---
Today (BASE 2026-27)  eBay      $272         $183        $42             $12      $36  13%
                      B2B       $240         $183         $9             $11      $38  16%
                      mix m12   $253         $183        $22             $11      $37  15%
GLUT (x0.40)          eBay      $109          $73        $20              $8       $7   7%
                      B2B        $96          $73         $4              $8      $10  11%
                      mix m12   $101          $73        $11              $8       $9   9%
SEVERE (x0.10)        eBay       $49          $33        $12              $7      $-3  -6%
                      B2B        $43          $33         $3              $7       $0   1%
                      mix m12    $45          $33         $6              $7      $-1  -2%
  Per SKU, today, mixed channel:
SKU        Resale/GB  Avg price   Buy  Contrib   GM  Cash tied/unit
---------  ---------  ---------  ----  -------  ---  --------------
DDR4 32GB   $3.91/GB       $116   $81      $12  10%             $81
DDR4 64GB   $4.84/GB       $288  $202      $43  15%            $202
DDR5 64GB  $16.33/GB       $970  $679     $167  17%            $679
  Inventory lag: buying at today's price and selling one GLUT month later (-5%/month) gives $25 contribution per module (11%).

1b. Optane PMem 128GB (C-26 SKU), eBay only
Deck                  Price   Buy  Fees  Labor  Contrib    GM
--------------------  -----  ----  ----  -----  -------  ----
Today (BASE 2026-27)   $200  $110   $28     $6      $46   23%
GLUT (x0.40)            $80   $44   $11     $6      $11   14%
SEVERE (x0.10)          $20   $11    $3     $6      $-7  -34%

1c. CleanBOM-5949 per subscriber-month (blended 65% $750 / 35% $2500) -- same in every deck
Item                      $/month
------------------------  -------
Subscription ARPA          $1,362
Lab pass-through revenue     $256
Lab cost                    $-160
Software COGS (12%)         $-164
Gross profit               $1,295
GM                            80%
  One-off evidence pack: $900 at ~88% GM (software cost only).

1d. DIMM-health per customer-year (1200 DIMMs at $0.60/DIMM-month)
Deck                  Spares from  Revenue/yr  COGS/yr   GM  Spare cost  Pool capital  Fee/DIY spares
--------------------  -----------  ----------  -------  ---  ----------  ------------  --------------
Today (BASE 2026-27)  bundle           $8,640   $3,068  64%         $89        $2,130            4.5x
                      standalone       $8,640   $4,008  54%        $130        $3,120            3.2x
GLUT (x0.40)          bundle           $8,640   $1,922  78%         $39          $924            8.5x
                      standalone       $8,640   $2,298  73%         $55        $1,320            6.6x
SEVERE (x0.10)        bundle           $8,640   $1,647  81%         $26          $635           10.8x
                      standalone       $8,640   $1,888  78%         $37          $888            8.7x

1e. Customer acquisition (founder time imputed at $75/h, 3 h per conversation; marketing $300/mo)
Line         Close/conv      CAC  Gross profit/mo  Churn/mo      LTV  LTV/CAC  Payback (mo)
-----------  ----------  -------  ---------------  --------  -------  -------  ------------
CleanBOM            10%   $2,550           $1,295        2%  $64,750      25x           2.0
DIMM-health         ~5%   $4,500             $500      1.5%  $33,324       7x           9.0
Recert B2B          n/a  in fees       per module       n/a      n/a      n/a           n/a
  LTV/CAC looks high only because the close rate and churn are untested; the kill experiment measures them.

========================================================================================================
2. MONTHLY P&L AND CASH, BASE scenario (all four lines; $; FT = founder full-time)
========================================================================================================
Month    Idx  Mods  Recert+PMem  CleanBOM  DIMM-h  Revenue     GP   Opex  Salary  EBITDA    Cash  Inv buy  CB subs  DH cust     ARR    
------  ----  ----  -----------  --------  ------  -------  -----  -----  ------  ------  ------  -------  -------  -------  ------  --
Nov-26  1.00     0         0.0k      0.0k    0.0k     0.0k   0.0k   3.3k    0.0k   -3.3k   32.5k     0.0k      0.0      0.0    0.0k    
Dec-26  1.00     0         0.0k      0.0k    0.0k     0.0k   0.0k   0.8k    0.0k   -0.8k   24.6k     7.1k      0.0      0.0    0.0k    
Jan-27  1.00    39        15.1k      0.0k    0.0k    15.1k   2.9k   0.8k    0.0k    2.1k   19.7k    14.2k      0.0      0.0    0.0k    
Feb-27  1.00    78        25.2k      0.0k    0.0k    25.2k   4.5k   2.0k    0.0k    2.5k   15.1k    21.3k      0.0      0.0    0.0k    
Mar-27  1.00   116        35.2k      0.0k    0.0k    35.2k   6.2k   2.0k    0.0k    4.2k   12.2k    28.3k      0.0      0.0    0.0k    
Apr-27  1.00   155        45.1k      0.0k    0.0k    45.1k   7.7k   2.0k    0.0k    5.7k    6.8k    35.4k      0.0      0.0    0.0k    
May-27  1.00   194        54.9k      0.0k    0.0k    54.9k   9.1k   2.0k    0.0k    7.1k    6.9k    42.5k      0.0      0.0    0.0k    
Jun-27  1.00   233        64.7k      0.0k    0.0k    64.7k  10.6k   2.0k    0.0k    8.6k    8.3k    49.6k      0.0      0.0    0.0k    
Jul-27  1.00   272        74.4k      0.0k    0.0k    74.4k  12.0k   9.5k    0.0k    2.5k    5.0k    55.4k      0.0      0.0    0.0k    
Aug-27  1.00   304        82.3k      1.5k    0.0k    83.8k  14.4k   7.2k    0.0k    7.2k    5.0k    62.6k      0.5      0.0    8.2k    
Sep-27  1.00   343        92.0k      2.3k    0.0k    94.3k  16.5k   4.2k    0.0k   12.3k    9.1k    70.8k      1.0      0.0   16.2k    
Oct-27  1.00   388       103.1k      3.1k    0.1k   106.3k  18.9k   4.2k    0.0k   14.7k   23.4k    70.8k      1.5      0.1   25.3k    
Nov-27  1.00   388       100.1k      3.8k    0.2k   104.1k  18.9k   4.2k    0.0k   14.6k   37.7k    70.8k      1.9      0.3   34.3k    
Dec-27  1.00   388       100.1k      6.6k    0.5k   107.2k  22.0k   4.2k   10.0k    7.8k   23.5k    92.1k      3.1      0.6   56.3k  FT
Jan-28  0.99   504       128.5k      8.5k    0.7k   137.7k  27.0k  14.2k   10.0k    2.7k   19.2k    98.4k      4.2      1.0   77.8k  FT
Feb-28  0.98   543       137.0k     10.3k    0.9k   148.3k  29.7k   4.2k   10.0k   15.4k   29.3k   103.1k      5.4      1.3   99.0k  FT
Mar-28  0.97   574       143.5k     12.1k    1.2k   156.7k  32.1k   4.2k   10.0k   17.8k   48.0k   101.5k      6.4      1.6  119.7k  FT
Apr-28  0.97   570       141.2k     13.8k    1.4k   156.5k  33.3k   4.2k   10.0k   19.0k   67.9k    99.9k      7.5      2.0  140.0k  FT
May-28  0.96   566       139.0k     15.5k    1.7k   156.2k  34.4k   3.5k   10.0k   21.0k   89.8k    98.3k      8.6      2.3  159.9k  FT
Jun-28  0.95   562       136.9k     17.2k    1.9k   155.9k  35.5k   3.5k   10.0k   22.1k  112.8k    96.8k      9.6      2.6  179.5k  FT
Jul-28  0.94   558       134.7k     18.8k    2.1k   155.6k  36.6k   3.5k   10.0k   23.2k  136.9k    95.2k     10.6      2.9  198.6k  FT
Aug-28  0.93   554       132.6k     20.4k    2.3k   155.3k  37.7k   3.5k   10.0k   24.3k  162.1k    93.7k     11.6      3.2  217.4k  FT
Sep-28  0.93   550       130.4k     22.0k    2.5k   154.9k  38.8k   3.5k   10.0k   25.3k  188.4k    92.2k     12.6      3.5  235.9k  FT
Oct-28  0.92   546       128.3k     23.5k    2.8k   154.6k  39.8k   3.5k   10.0k   26.3k  215.6k    90.7k     13.5      3.8  253.9k  FT
Nov-28  0.91   542       126.2k     25.0k    3.0k   154.2k  40.8k   3.5k   10.0k   27.3k  243.9k    89.2k     14.4      4.1  271.7k  FT
Dec-28  0.90   538       124.1k     26.5k    3.2k   153.8k  41.8k   3.5k   10.0k   28.3k  273.1k    87.7k     15.4      4.4  289.1k  FT
Jan-29  0.89   533       121.9k     27.9k    3.4k   153.1k  42.5k   6.5k   10.0k   26.1k  300.4k    85.9k     16.2      4.7  306.1k  FT
Feb-29  0.88   529       119.4k     29.3k    3.6k   152.3k  43.4k   3.5k   10.0k   30.0k  331.6k    84.2k     17.1      5.0  322.8k  FT
Mar-29  0.87   524       117.0k     30.7k    3.8k   151.5k  44.3k   3.5k   10.0k   30.8k  363.6k    82.4k     18.0      5.2  339.2k  FT
Apr-29  0.86   519       114.6k     32.1k    4.0k   150.6k  45.1k   3.5k   10.0k   31.6k  396.5k    80.7k     18.8      5.5  355.3k  FT
May-29  0.85   514       112.2k     33.4k    4.2k   149.8k  45.9k   3.5k   10.0k   32.5k  430.1k    79.0k     19.6      5.8  371.1k  FT
Jun-29  0.84   509       109.9k     34.7k    4.4k   148.9k  46.7k   3.5k   10.0k   33.3k  464.6k    77.4k     20.4      6.0  386.6k  FT
Jul-29  0.83   504       107.5k     36.0k    4.5k   148.1k  47.5k   3.5k   10.0k   34.1k  499.9k    75.7k     21.2      6.3  401.8k  FT
Aug-29  0.82   500       105.2k     37.3k    4.7k   147.2k  48.3k   3.5k   10.0k   34.8k  535.9k    74.1k     22.0      6.6  416.6k  FT
Sep-29  0.81   495       103.0k     38.5k    4.9k   146.3k  49.0k   3.5k   10.0k   35.6k  572.6k    72.5k     22.8      6.8  431.2k  FT
Oct-29  0.80   490       100.7k     39.7k    5.1k   145.5k  49.8k   3.5k   10.0k   36.3k  610.1k    70.8k     23.5      7.1  445.5k  FT
  Mods = good recert modules sold. Inv buy = lots bought this month for next month (cash already out).

========================================================================================================
2. MONTHLY P&L AND CASH, GLUT scenario (all four lines; $; FT = founder full-time)
========================================================================================================
Month    Idx  Mods  Recert+PMem  CleanBOM  DIMM-h  Revenue     GP   Opex  Salary  EBITDA    Cash  Inv buy  CB subs  DH cust     ARR    
------  ----  ----  -----------  --------  ------  -------  -----  -----  ------  ------  ------  -------  -------  -------  ------  --
Nov-26  1.00     0         0.0k      0.0k    0.0k     0.0k   0.0k   3.3k    0.0k   -3.3k   32.5k     0.0k      0.0      0.0    0.0k    
Dec-26  1.00     0         0.0k      0.0k    0.0k     0.0k   0.0k   0.8k    0.0k   -0.8k   24.6k     7.1k      0.0      0.0    0.0k    
Jan-27  1.00    39        15.1k      0.0k    0.0k    15.1k   2.9k   0.8k    0.0k    2.1k   19.7k    14.2k      0.0      0.0    0.0k    
Feb-27  1.00    78        25.2k      0.0k    0.0k    25.2k   4.5k   2.0k    0.0k    2.5k   15.1k    21.3k      0.0      0.0    0.0k    
Mar-27  1.00   116        35.2k      0.0k    0.0k    35.2k   6.2k   2.0k    0.0k    4.2k   12.2k    28.3k      0.0      0.0    0.0k    
Apr-27  1.00   155        45.1k      0.0k    0.0k    45.1k   7.7k   2.0k    0.0k    5.7k    6.8k    35.4k      0.0      0.0    0.0k    
May-27  1.00   194        54.9k      0.0k    0.0k    54.9k   9.1k   2.0k    0.0k    7.1k    6.9k    42.5k      0.0      0.0    0.0k    
Jun-27  1.00   233        64.7k      0.0k    0.0k    64.7k  10.6k   2.0k    0.0k    8.6k    8.3k    49.6k      0.0      0.0    0.0k    
Jul-27  1.00   272        74.4k      0.0k    0.0k    74.4k  12.0k   9.5k    0.0k    2.5k    5.0k    55.4k      0.0      0.0    0.0k    
Aug-27  1.00   304        82.3k      1.5k    0.0k    83.8k  14.4k   7.2k    0.0k    7.2k    5.0k    62.6k      0.5      0.0    8.2k    
Sep-27  1.00   343        92.0k      2.3k    0.0k    94.3k  16.5k   4.2k    0.0k   12.3k    9.1k    70.8k      1.0      0.0   16.2k    
Oct-27  1.00   388       103.1k      3.1k    0.1k   106.3k  18.9k   4.2k    0.0k   14.7k   23.4k    70.8k      1.5      0.1   25.3k    
Nov-27  1.00   388       100.1k      3.8k    0.2k   104.1k  18.9k   4.2k    0.0k   14.6k   37.7k    70.8k      1.9      0.3   34.3k    
Dec-27  1.00   388       100.1k      6.6k    0.5k   107.2k  22.0k   4.2k   10.0k    7.8k   23.5k    92.1k      3.1      0.6   56.3k  FT
Jan-28  0.95   504       123.1k      8.5k    0.7k   132.3k  22.1k  14.2k   10.0k   -2.1k   18.6k    94.2k      4.2      1.0   77.7k  FT
Feb-28  0.90   543       125.4k     10.3k    0.9k   136.6k  23.4k   4.2k   10.0k    9.2k   33.7k    87.7k      5.4      1.3   98.7k  FT
Mar-28  0.85   534       116.4k     12.1k    1.1k   129.6k  23.5k   4.2k   10.0k    9.3k   51.0k    79.0k      6.4      1.6  119.2k  FT
Apr-28  0.80   509       104.6k     13.8k    1.4k   119.8k  23.3k   4.2k   10.0k    9.1k   67.8k    70.9k      7.5      1.9  139.2k  FT
May-28  0.75   485        93.5k     15.5k    1.6k   110.5k  23.3k   3.5k   10.0k    9.8k   84.9k    63.1k      8.6      2.2  158.8k  FT
Jun-28  0.70   461        83.0k     17.2k    1.8k   101.9k  23.3k   3.5k   10.0k    9.8k  101.6k    55.8k      9.6      2.4  178.0k  FT
Jul-28  0.65   436        73.0k     18.8k    2.0k    93.8k  23.3k   3.5k   10.0k    9.9k  118.0k    48.9k     10.6      2.7  196.8k  FT
Aug-28  0.60   412        63.8k     20.4k    2.1k    86.3k  23.5k   3.5k   10.0k   10.1k  134.1k    42.5k     11.6      3.0  215.2k  FT
Sep-28  0.55   388        55.1k     22.0k    2.3k    79.3k  23.8k   3.5k   10.0k   10.3k  183.0k     3.7k     12.6      3.2  233.1k  FT
Oct-28  0.50    36         5.6k     23.5k    2.5k    31.6k  21.4k   3.5k   10.0k    7.9k  191.2k     3.1k     13.5      3.4  250.7k  FT
Nov-28  0.45    34         4.8k     25.0k    2.6k    32.4k  22.6k   3.5k   10.0k    9.2k  200.7k     2.6k     14.4      3.7  267.9k  FT
Dec-28  0.40    32         4.0k     26.5k    2.8k    33.3k  23.8k   3.5k   10.0k   10.4k  211.3k     2.1k     15.4      3.9  284.7k  FT
Jan-29  0.40    29         3.7k     27.9k    3.0k    34.6k  25.4k   6.5k   10.0k    8.9k  200.9k    21.3k     16.2      4.1  301.1k  FT
Feb-29  0.40   291        30.2k     29.3k    3.1k    62.7k  30.2k   3.5k   10.0k   16.8k  217.5k    21.3k     17.1      4.3  317.2k  FT
Mar-29  0.40   291        30.2k     30.7k    3.3k    64.2k  31.4k   3.5k   10.0k   18.0k  235.3k    21.3k     18.0      4.5  332.9k  FT
Apr-29  0.40   291        30.2k     32.1k    3.4k    65.7k  32.6k   3.5k   10.0k   19.2k  254.3k    21.3k     18.8      4.7  348.3k  FT
May-29  0.40   291        30.2k     33.4k    3.5k    67.2k  33.8k   3.5k   10.0k   20.4k  274.5k    21.3k     19.6      4.9  363.4k  FT
Jun-29  0.40   291        30.2k     34.7k    3.7k    68.6k  34.9k   3.5k   10.0k   21.5k  295.8k    21.3k     20.4      5.1  378.2k  FT
Jul-29  0.40   291        30.2k     36.0k    3.8k    70.0k  36.1k   3.5k   10.0k   22.6k  318.3k    21.3k     21.2      5.2  392.6k  FT
Aug-29  0.40   291        30.2k     37.3k    3.9k    71.4k  37.2k   3.5k   10.0k   23.7k  341.8k    21.3k     22.0      5.4  406.7k  FT
Sep-29  0.40   291        30.2k     38.5k    4.0k    72.7k  38.2k   3.5k   10.0k   24.8k  366.4k    21.3k     22.8      5.6  420.5k  FT
Oct-29  0.40   291        30.2k     39.7k    4.1k    74.0k  39.3k   3.5k   10.0k   25.8k  392.1k    21.3k     23.5      5.7  434.0k  FT
  Mods = good recert modules sold. Inv buy = lots bought this month for next month (cash already out).

========================================================================================================
2. MONTHLY P&L AND CASH, SEVERE scenario (all four lines; $; FT = founder full-time)
========================================================================================================
Month    Idx  Mods  Recert+PMem  CleanBOM  DIMM-h  Revenue     GP   Opex  Salary  EBITDA    Cash  Inv buy  CB subs  DH cust     ARR    
------  ----  ----  -----------  --------  ------  -------  -----  -----  ------  ------  ------  -------  -------  -------  ------  --
Nov-26  1.00     0         0.0k      0.0k    0.0k     0.0k   0.0k   3.3k    0.0k   -3.3k   32.5k     0.0k      0.0      0.0    0.0k    
Dec-26  1.00     0         0.0k      0.0k    0.0k     0.0k   0.0k   0.8k    0.0k   -0.8k   24.6k     7.1k      0.0      0.0    0.0k    
Jan-27  1.00    39        15.1k      0.0k    0.0k    15.1k   2.9k   0.8k    0.0k    2.1k   19.7k    14.2k      0.0      0.0    0.0k    
Feb-27  1.00    78        25.2k      0.0k    0.0k    25.2k   4.5k   2.0k    0.0k    2.5k   15.1k    21.3k      0.0      0.0    0.0k    
Mar-27  1.00   116        35.2k      0.0k    0.0k    35.2k   6.2k   2.0k    0.0k    4.2k   12.2k    28.3k      0.0      0.0    0.0k    
Apr-27  1.00   155        45.1k      0.0k    0.0k    45.1k   7.7k   2.0k    0.0k    5.7k    6.8k    35.4k      0.0      0.0    0.0k    
May-27  1.00   194        54.9k      0.0k    0.0k    54.9k   9.1k   2.0k    0.0k    7.1k    6.9k    42.5k      0.0      0.0    0.0k    
Jun-27  1.00   233        64.7k      0.0k    0.0k    64.7k  10.6k   2.0k    0.0k    8.6k    8.3k    49.6k      0.0      0.0    0.0k    
Jul-27  1.00   272        74.4k      0.0k    0.0k    74.4k  12.0k   9.5k    0.0k    2.5k    5.0k    55.4k      0.0      0.0    0.0k    
Aug-27  1.00   304        82.3k      1.5k    0.0k    83.8k  14.4k   7.2k    0.0k    7.2k    5.0k    62.6k      0.5      0.0    8.2k    
Sep-27  1.00   343        92.0k      2.3k    0.0k    94.3k  16.5k   4.2k    0.0k   12.3k    9.1k    70.8k      1.0      0.0   16.2k    
Oct-27  1.00   388       103.1k      3.1k    0.1k   106.3k  18.9k   4.2k    0.0k   14.7k   23.4k    70.8k      1.5      0.1   25.3k    
Nov-27  1.00   388       100.1k      3.8k    0.2k   104.1k  18.9k   4.2k    0.0k   14.6k   37.7k    70.8k      1.9      0.3   34.3k    
Dec-27  1.00   388       100.1k      6.6k    0.5k   107.2k  22.0k   4.2k   10.0k    7.8k   23.5k    92.1k      3.1      0.6   56.3k  FT
Jan-28  0.93   504       119.8k      8.5k    0.7k   129.0k  19.2k  14.2k   10.0k   -5.0k   18.2k    91.8k      4.2      1.0   77.7k  FT
Feb-28  0.85   543       118.5k     10.3k    0.9k   129.7k  19.7k   4.2k   10.0k    5.4k   35.7k    79.0k      5.4      1.3   98.7k  FT
Mar-28  0.78   509       101.4k     12.1k    1.1k   114.6k  18.9k   4.2k   10.0k    4.6k   52.0k    66.9k      6.4      1.6  119.2k  FT
Apr-28  0.70   473        85.1k     13.8k    1.4k   100.3k  18.3k   4.2k   10.0k    4.1k  116.9k     5.6k      7.5      1.9  139.2k  FT
May-28  0.63    44         8.1k     15.5k    1.6k    25.2k  14.5k   3.5k   10.0k    1.0k  118.5k     4.6k      8.6      2.2  158.8k  FT
Jun-28  0.55    40         6.7k     17.2k    1.8k    25.6k  15.7k   3.5k   10.0k    2.3k  121.4k     3.7k      9.6      2.4  178.0k  FT
Jul-28  0.48    36         5.3k     18.8k    2.0k    26.1k  17.0k   3.5k   10.0k    3.6k  125.5k     2.8k     10.6      2.7  196.8k  FT
Aug-28  0.40    33         4.1k     20.4k    2.1k    26.6k  18.3k   3.5k   10.0k    4.8k  130.8k     2.1k     11.6      3.0  215.2k  FT
Sep-28  0.33    29         3.0k     22.0k    2.3k    27.3k  19.6k   3.5k   10.0k    6.1k  137.2k     1.7k     12.6      3.2  233.1k  FT
Oct-28  0.25    29         1.9k     23.5k    2.5k    27.9k  20.8k   3.5k   10.0k    7.3k  144.7k     1.3k     13.5      3.4  250.7k  FT
Nov-28  0.18    29         1.6k     25.0k    2.6k    29.2k  22.2k   3.5k   10.0k    8.8k  153.6k     1.1k     14.4      3.7  267.9k  FT
Dec-28  0.10    29         1.3k     26.5k    2.8k    30.6k  23.5k   3.5k   10.0k   10.1k  163.7k     1.0k     15.4      3.9  284.7k  FT
Jan-29  0.10    29         1.3k     27.9k    3.0k    32.2k  25.0k   6.5k   10.0k    8.5k  172.1k     1.0k     16.2      4.1  301.1k  FT
Feb-29  0.10    29         1.3k     29.3k    3.1k    33.8k  26.2k   3.5k   10.0k   12.8k  184.7k     1.0k     17.1      4.3  317.2k  FT
Mar-29  0.10    29         1.3k     30.7k    3.3k    35.3k  27.5k   3.5k   10.0k   14.0k  198.6k     1.0k     18.0      4.5  332.9k  FT
Apr-29  0.10    29         1.3k     32.1k    3.4k    36.8k  28.7k   3.5k   10.0k   15.2k  213.7k     1.0k     18.8      4.7  348.3k  FT
May-29  0.10    29         1.3k     33.4k    3.5k    38.3k  29.8k   3.5k   10.0k   16.4k  230.0k     1.0k     19.6      4.9  363.4k  FT
Jun-29  0.10    29         1.3k     34.7k    3.7k    39.7k  31.0k   3.5k   10.0k   17.5k  247.4k     1.0k     20.4      5.1  378.2k  FT
Jul-29  0.10    29         1.3k     36.0k    3.8k    41.1k  32.1k   3.5k   10.0k   18.7k  265.9k     1.0k     21.2      5.2  392.6k  FT
Aug-29  0.10    29         1.3k     37.3k    3.9k    42.5k  33.2k   3.5k   10.0k   19.8k  285.6k     1.0k     22.0      5.4  406.7k  FT
Sep-29  0.10    29         1.3k     38.5k    4.0k    43.8k  34.3k   3.5k   10.0k   20.8k  306.3k     1.0k     22.8      5.6  420.5k  FT
Oct-29  0.10    29         1.3k     39.7k    4.1k    45.1k  35.3k   3.5k   10.0k   21.9k  328.1k     1.0k     23.5      5.7  434.0k  FT
  Mods = good recert modules sold. Inv buy = lots bought this month for next month (cash already out).

========================================================================================================
3. SCENARIO SUMMARY (bundle, all four lines)
========================================================================================================
Scenario  Breakeven (actual)  Breakeven @$10k salary     Cash low  Cash+inv low  ARR m12   ARR m18   ARR m24   ARR m36  Run-rate m18  Run-rate m36  Cash m36  Inventory m36  Founder FT from
--------  ------------------  ----------------------  -----------  ------------  -------  --------  --------  --------  ------------  ------------  --------  -------------  ---------------
BASE             m3 (Jan-27)            m11 (Sep-27)  $5,000 @m10   $31,700 @m2  $25,334  $139,995  $253,948  $445,543    $1,877,409    $1,745,612  $610,097        $70,850     m14 (Dec-27)
GLUT             m3 (Jan-27)            m11 (Sep-27)  $5,000 @m10   $31,700 @m2  $25,334  $139,232  $250,679  $434,012    $1,437,256      $888,533  $392,118        $21,256     m14 (Dec-27)
SEVERE           m3 (Jan-27)            m11 (Sep-27)  $5,000 @m10   $31,700 @m2  $25,334  $139,232  $250,679  $434,012    $1,203,055      $541,772  $328,128           $953     m14 (Dec-27)
  Cash low sits on the $5k reserve by design: the operator buys inventory down to the reserve, so working
  capital, not losses, is what binds in year 1. 'Cash+inv low' adds back the lots bought that month.
  ARR = recurring only (CleanBOM subscriptions + DIMM-health) x 12. Run-rate = all revenue in that month x 12.
  'Breakeven (actual)' = first of 3 straight months with EBITDA >= 0 as actually incurred (founder unpaid
  until the full-time trigger). 'Breakeven @$10k salary' charges a market founder salary every month.
  BASE   cumulative revenue $4,143,093: recert+PMem $3,506,010 (85%), CleanBOM $570,158, DIMM-health $66,925; recert modules sold 14,618
  GLUT   cumulative revenue $2,548,729: recert+PMem $1,920,306 (75%), CleanBOM $570,158, DIMM-health $58,265; recert modules sold 9,919
  SEVERE cumulative revenue $1,890,940: recert+PMem $1,262,518 (67%), CleanBOM $570,158, DIMM-health $58,265; recert modules sold 5,486
  Gross margin over 36 months (GP / revenue; recert GP is after technician labor):
  BASE   blended 25% | recert+PMem 15% | CleanBOM 81% | DIMM-health 68%
  GLUT   blended 30% | recert+PMem 13% | CleanBOM 81% | DIMM-health 76%
  SEVERE blended 36% | recert+PMem 13% | CleanBOM 81% | DIMM-health 79%
  Die-source library by m36: 63 lab-confirmed module part numbers (X-ray+decap), plus SPD records on every recert module.

========================================================================================================
4. IS THE WHOLE BETTER THAN ITS PARTS?  (same founder, same $40k, run line-by-line)
========================================================================================================
Scenario  Configuration                 Cash low     Breakeven   ARR m18   ARR m36  Run-rate m36  Cash m36  Cum EBITDA  FT months
--------  ------------------------  ------------  ------------  --------  --------  ------------  --------  ----------  ---------
BASE      Bundle (all four)          $5,000 @m10   m3 (Jan-27)  $139,995  $445,543    $1,745,612  $610,097    $662,971         23
          Recert + PMem only         $10,410 @m6   m3 (Jan-27)        $0        $0    $1,208,380  $169,467    $208,516         24
          CleanBOM standalone       $-6,529 @m15  m16 (Feb-28)   $47,569  $120,296      $150,999   $91,351     $52,851          0
          DIMM-health standalone      $-349 @m30  m28 (Feb-29)    $8,674   $27,187       $27,187      $583    $-26,165          0
          Recert + CleanBOM          $5,000 @m10   m3 (Jan-27)  $122,937  $384,530    $1,684,599  $580,439    $619,489         23
BASE      Bundle, no evidence lift    $5,000 @m9   m3 (Jan-27)   $93,744  $323,558    $1,600,947  $461,433    $513,988         22
BASE      Bundle, founder never FT   $5,000 @m10   m3 (Jan-27)   $76,629  $199,038    $1,051,414  $480,218    $501,841          0
GLUT      Bundle (all four)          $5,000 @m10   m3 (Jan-27)  $139,232  $434,012      $888,533  $392,118    $389,580         23
          Recert + PMem only         $5,000 @m29   m3 (Jan-27)        $0        $0      $245,088   $22,058      $4,429         17
          CleanBOM standalone       $-6,529 @m15  m16 (Feb-28)   $47,569  $120,296      $150,999   $91,351     $52,851          0
          DIMM-health standalone     $2,590 @m27  m24 (Oct-28)    $8,239   $21,868       $21,868    $5,248    $-25,225          0
          Recert + CleanBOM          $5,000 @m10   m3 (Jan-27)  $122,937  $384,530      $839,051  $357,047    $346,502         23
GLUT      Bundle, no evidence lift    $5,000 @m9   m3 (Jan-27)   $93,048  $312,457      $744,298  $246,349    $243,548         22
GLUT      Bundle, founder never FT   $5,000 @m10   m3 (Jan-27)   $76,195  $193,720      $479,197  $350,998    $337,038          0
SEVERE    Bundle (all four)          $5,000 @m10   m3 (Jan-27)  $139,232  $434,012      $541,772  $328,128    $303,874         23
          Recert + PMem only        $-7,604 @m36   m3 (Jan-27)        $0        $0          $240   $-7,604    $-39,404         14
          CleanBOM standalone       $-6,529 @m15  m16 (Feb-28)   $47,569  $120,296      $150,999   $91,351     $52,851          0
          DIMM-health standalone     $3,778 @m27  m23 (Sep-28)    $8,239   $21,868       $21,868    $7,412    $-23,928          0
          Recert + CleanBOM          $5,000 @m10   m3 (Jan-27)  $122,937  $384,530      $492,290  $288,639    $257,791         23
SEVERE    Bundle, no evidence lift    $5,000 @m9   m3 (Jan-27)   $73,790  $154,149      $197,596  $256,313    $228,846          2
SEVERE    Bundle, founder never FT   $5,000 @m10   m3 (Jan-27)   $76,195  $193,720      $244,903  $315,402    $287,326          0
  Standalone CleanBOM pays for each library sample module and closes at 7% vs 10% (the bundle
  hypothesis, untested). Standalone DIMM-health buys spares at resale, not recert buy cost.
  'No evidence lift' keeps the recert cash but gives CleanBOM the standalone close rate and sample cost:
  the gap to the full bundle is what the die-source library is worth; the gap to 'founder never FT' is
  what recert cash (buying founder time) is worth.

========================================================================================================
5. SENSITIVITY (BASE scenario, bundle; one input moved at a time)
========================================================================================================
Input                                      Move      Breakeven  Cash low   ARR m18   ARR m36    Cash m36  Cum EBITDA
-----------------------------------------  -----  ------------  --------  --------  --------  ----------  ----------
Base case                                  --      m3 (Jan-27)    $5,000  $139,995  $445,543    $610,097    $662,971
Recert resale price                        -30%    m3 (Jan-27)    $5,000   $76,629  $381,840    $366,995    $393,112
Recert resale price                        +30%    m3 (Jan-27)    $5,000  $151,943  $453,955    $783,989    $862,412
SaaS / subscription price                  -30%    m3 (Jan-27)    $5,000   $97,997  $311,880    $461,565    $514,439
SaaS / subscription price                  +30%    m3 (Jan-27)    $5,000  $181,994  $579,205    $758,629    $811,503
Close rate (CB + DH)                       -30%    m3 (Jan-27)    $5,000   $97,997  $311,880    $473,893    $522,620
Close rate (CB + DH)                       +30%    m3 (Jan-27)    $5,000  $181,994  $579,205    $746,300    $803,322
Churn (CB + DH)                            -30%    m3 (Jan-27)    $5,000  $142,483  $475,378    $630,457    $684,003
Churn (CB + DH)                            +30%    m3 (Jan-27)    $5,000  $137,563  $418,188    $591,030    $643,274
COGS (buy %, fees, lab, hosting)           -30%    m3 (Jan-27)   $26,740  $183,332  $475,880  $1,552,772  $1,580,942
COGS (buy %, fees, lab, hosting)           +30%   m16 (Feb-28)  $-12,172   $76,629  $199,038    $125,914    $108,188
Final FAR rule slips 6 mo (CB launch m16)  +6 mo   m3 (Jan-27)    $6,101   $35,990  $372,904    $458,278    $510,190
Founder stays part-time all 36 months      PT      m3 (Jan-27)    $5,000   $76,629  $199,038    $480,218    $501,841
ITAD buy fraction = 0.55                   abs     m3 (Jan-27)   $21,650  $183,332  $475,880  $1,047,669  $1,088,175
ITAD buy fraction = 0.75                   abs    m11 (Sep-27)    $6,469   $76,629  $250,221    $163,673    $148,705
  Glut and severe sensitivities: see sections 3-4 (CleanBOM is price-independent; recert is not).

========================================================================================================
6. WHAT MUST BE TRUE
========================================================================================================
a) Recert: lots must cost less than 78% (eBay) / 78% (B2B) / 78% (m12 mix) of realized resale for any
   contribution at today's prices; at the modeled 65% the mixed-channel margin is $37 per module (15%).
b) Recert alone covers a $10k/mo founder salary + ~$3,450 fixed opex at 364 good modules/month at today's prices
   (needs ~$64,624 of inventory cash per month at 65% buy) -- and only until the 2028 turn.
c) For the business to survive the glut on recurring revenue alone, CleanBOM needs ~10 paying subscribers (at $1,295 GP/sub-month)
   by the 2028 turn (month 15-18). Modeled BASE: 7.5 subscribers at m18, 23.5 at m36.
   Getting there by m18 from a m10 launch needs a 25% close rate at 5 conversations/month, or 12 conversations/month at a 10% close.
d) Equivalently: by month 18 the founder needs ~10 signed provenance customers (e.g. 4 module makers at $2500 + 7 integrators at $750).
e) DIMM-health must sell at 4.5x the buyer's DIY spares cost against free OEM/BMC prediction (Lenovo MPFA,
   Intel MFP) and ParkView-bundled TPM: it must be sold as a wholesale feed + spares to TPMs/MSPs, or dropped.
f) $1M ARR at m36 would need ~61 CleanBOM subscribers at the blended ARPA; the model reaches 23.5.

========================================================================================================
7. GLUT BEHAVIOR PER LINE (steady-state unit margin and modeled revenue in the last 12 months)
========================================================================================================
Scenario  Idx m36  Recert GM  PMem GM  CleanBOM GM  Recert rev (last 12m)  CB rev (last 12m)  DH rev (last 12m)  DH cust m36
--------  -------  ---------  -------  -----------  ---------------------  -----------------  -----------------  -----------
BASE         0.80        14%      21%          80%             $1,361,633           $391,022            $48,619          7.1
GLUT         0.40         9%      14%          80%               $284,620           $391,022            $41,150          5.7
SEVERE       0.10        -2%     -34%          80%                $16,297           $391,022            $41,150          5.7
  Recert dies as a profit line in GLUT/SEVERE (buying stops; trickle kept for spares/library). PMem dies on
  2027-10-11 (VMware) regardless. CleanBOM is unaffected by price. DIMM-health margin rises (cheap spares) but
  customers churn faster once DDR5 refresh is cheap.

Done. exit 0
```
