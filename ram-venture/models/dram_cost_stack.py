#!/usr/bin/env python3
"""DRAM cost-stack model -- American Memory study, Phase 1 (agent key: p1-model). As of 2026-11-01.

Chain, per case:
    wafer cost -> gross dies per wafer (GDPW; edge exclusion + scribe) -> die yield -> good dies
    -> bits per die -> wafer-level $/GB -> + probe / final test / burn-in -> + package (FBGA)
    -> + final-test fallout -> component $/GB -> + module BOM & assembly -> module $/user-GB
It then compares cost with market prices: Q4-2026 contract price, the GLUT scenario
(ASSUMPTIONS.md A-05: DDR5 contract falls 60% from its 2026 peak) and the 2023 trough. Finally it
runs a +/-20% sensitivity on wafer cost, yield and die size, printed as tornado tables.

Inputs: research/phase1/cost_inputs.json (written by agent p1-cost), plus hard-coded fallbacks in
_SPEC so the script runs standalone. Every INPUTS entry carries `source`, which is either a URL or
"ESTIMATE: <basis>", plus a confidence `tag`:
    VERIFIED   = primary source opened by p1-cost (e.g. open-source cost-model repos)
    REPORTED   = URL that another agent saw in a search snippet
    UNVERIFIED = prior knowledge, with no URL
    ESTIMATE   = an agent's own computation
None of the market prices was opened first-hand: the web-search budget was spent and the
trendforce.com, eetasia.com and buysellram.com fetches failed DNS on 2026-11-01. Treat the outputs
as an ESTIMATE with ranges.

Formulas:
    GDPW  = pi*(d/2)^2/S - pi*d/sqrt(2*S),  d = wafer_diameter - 2*edge_exclusion,
            S = (sqrt(die_mm2) + scribe)^2                      [Chiplet Actuary form]
    Yield = (1 + A*D0/alpha)^-alpha (negative binomial). D0 is calibrated so that the
            reference die on each node hits the stated yield. Larger dies on the same node
            (24Gb/32Gb) and die-size sensitivities therefore move yield as well as GDPW.
    Probe cost is incurred on every gross die (divided by yield). Probe and final test scale
            with (Gb/ref_Gb)^0.5 per die. The package cost is flat per die.

Run:     cd ram-venture && python3 models/dram_cost_stack.py
         (prints the tables, writes research/phase1/cost_stack_output.md, exits 0)
Import (from another script in models/):
         import sys; from pathlib import Path
         sys.path.insert(0, str(Path(__file__).resolve().parent))
         from dram_cost_stack import ddr5_reference
         ref = ddr5_reference()      # dict of $/GB reference numbers; no printing, no file writes
"""
import io
import json
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path

AS_OF = "2026-11-01"
RV = Path(__file__).resolve().parents[1]
INPUTS_JSON = RV / "research" / "phase1" / "cost_inputs.json"
OUT_MD = RV / "research" / "phase1" / "cost_stack_output.md"
YIELD_CAP = 0.99      # a +20% yield sensitivity cannot push die yield above this
SENS_STEP = 0.20      # +/-20% sensitivity step (task spec)

# ----------------------------------------------------------------------------------------------
# INPUT SPEC: (name, cost_inputs.json key or None, value, low, high, unit, tag, fallback source)
# When the json key exists, value/low/high/source/tag are taken from cost_inputs.json. Otherwise
# the hard-coded fallback below is used. json key None means a p1-model input.
# ----------------------------------------------------------------------------------------------
_CA = "https://github.com/Yinxiao-Feng/DAC2022"
_EET = "https://www.eetasia.com/memory-prices-surging-by-90-from-4q-2025/"
_TF0930 = "https://www.trendforce.com/presscenter/news/20260930-13258.html"
_IGOR = ("https://www.igorslab.de/en/dram-and-nand-remain-more-expensive-trendforce-sees-slowing-"
         "but-still-rising-memory-prices-q3-2026/")
_TECHNEWS_2Q = ("https://technews.tw/2026/03/31/ai-server-demand-drives-2q26-memory-contract-price-"
                "increase-csps-lock-supply-long-term-deals/")
_BARCLAYS = "https://finance.technews.tw/2026/10/13/the-shortage-of-memory-chips-may-continue-for-another-two-years/"
_PK = "[UNVERIFIED-PK]"

_SPEC = [
    # --- geometry & yield -------------------------------------------------------------------
    ("wafer_diameter_mm", "wafer_diameter_mm", 300, 300, 300, "mm", "VERIFIED", _CA),
    ("edge_exclusion_mm", "edge_exclusion_mm", 3, 2, 5, "mm", "ESTIMATE",
     "ESTIMATE: DRAM fabs ~2-3 mm; high = Chiplet Actuary 5 mm | ref: " + _CA),
    ("scribe_lane_mm", "scribe_lane_mm", 0.08, 0.06, 0.2, "mm", "ESTIMATE",
     "ESTIMATE: memory scribe 60-100 um; high = Chiplet Actuary 0.2 mm | ref: " + _CA),
    ("yield_negbin_alpha", "yield_negbin_alpha", 10, 3, 10, "-", "VERIFIED", _CA),
    ("dram_die_yield_mature", "dram_die_yield_mature", 0.90, 0.85, 0.95, "fraction", "UNVERIFIED",
     "ESTIMATE: " + _PK + " mature DRAM die yield after laser/eFuse redundancy repair"),
    ("dram_die_yield_1c_1gamma_2026", "dram_die_yield_1c_1gamma_2026", 0.80, 0.60, 0.90, "fraction",
     "ESTIMATE", "ESTIMATE: 1c/1-gamma in its 2nd ramp year (2026)"),
    ("dram_die_yield_legacy_depreciated", None, 0.92, 0.88, 0.95, "fraction", "ESTIMATE",
     "ESTIMATE: p1-cost cost_stack.md s9 -- mature 2x/1x-nm line with years of learning"),
    ("dram_die_yield_legacy_new_line", None, 0.85, 0.75, 0.90, "fraction", "ESTIMATE",
     "ESTIMATE: p1-cost cost_stack.md s9 -- new-build 1x-nm line, early years"),
    ("dram_die_yield_foundry_legacy", None, 0.90, 0.85, 0.93, "fraction", "ESTIMATE",
     "ESTIMATE: p1-cost cost_stack.md s9 -- PSMC-class DRAM foundry, mature 25nm"),
    ("hbm3e_core_die_yield", None, 0.80, 0.70, 0.88, "fraction", "ESTIMATE",
     "ESTIMATE: p1-cost cost_stack.md s5.4 base (KGD core die incl. TSV); TrendForce 2024 'HBM yield "
     "20-30% below DDR5' " + _PK),
    ("hbm3e_12h_stack_yield", "hbm3e_12h_stack_yield", 0.75, 0.60, 0.90, "fraction", "UNVERIFIED",
     "ESTIMATE: " + _PK + " SK hynix HBM3E yield 'nearly 80%' (FT 2024-05); 12-high harder"),
    ("final_test_yield", None, 0.99, 0.97, 0.995, "fraction", "ESTIMATE",
     "ESTIMATE: p1-model -- packaged-part final test / burn-in fallout ~1%"),
    ("module_assembly_yield", "module_assembly_yield", 0.985, 0.97, 0.995, "fraction", "ESTIMATE",
     "ESTIMATE: SMT + module test fallout; failed modules mostly reworked"),
    # --- wafer cost ---------------------------------------------------------------------------
    ("dram_capex_per_wpm_1alpha_usd", "dram_capex_per_wpm_1alpha_usd", 130000, 110000, 150000, "USD/wpm",
     "UNVERIFIED", "ESTIMATE: " + _PK + " analyst rule of thumb $1.1-2.1B per 10k wpm"),
    ("dram_capex_per_wpm_1beta_usd", "dram_capex_per_wpm_1beta_usd", 145000, 120000, 180000, "USD/wpm",
     "UNVERIFIED", "ESTIMATE: " + _PK + " as 1-alpha; 1b adds EUV at Samsung/SK hynix"),
    ("dram_capex_per_wpm_1gamma_usd", "dram_capex_per_wpm_1gamma_usd", 170000, 140000, 210000, "USD/wpm",
     "UNVERIFIED", "ESTIMATE: " + _PK + " 1c/1-gamma: more EUV layers"),
    ("dram_tool_share_of_capex", "dram_tool_share_of_capex", 0.78, 0.70, 0.85, "fraction", "ESTIMATE",
     "ESTIMATE: equipment vs building/cleanroom"),
    ("dram_tool_depreciation_years", "dram_tool_depreciation_years", 5, 5, 7, "years", "UNVERIFIED",
     "ESTIMATE: " + _PK + " Korean makers ~5y straight-line; Micron 5-7y"),
    ("dram_building_depreciation_years", "dram_building_depreciation_years", 25, 20, 40, "years",
     "ESTIMATE", "ESTIMATE: building/cleanroom life"),
    ("fab_utilization", "fab_utilization", 0.95, 0.75, 1.0, "fraction", "ESTIMATE",
     "ESTIMATE: 2026 full; 2Q23 trough ~74-82% (TrendForce via p1-market)"),
    ("dram_wafer_cash_cost_1alpha_usd", "dram_wafer_cash_cost_1alpha_usd", 1550, 1400, 1800, "USD/wafer",
     "ESTIMATE", "ESTIMATE: materials+consumables $700-900, labor $300-500, utilities, spares"),
    ("dram_wafer_cash_cost_1beta_usd", "dram_wafer_cash_cost_1beta_usd", 1650, 1500, 2000, "USD/wafer",
     "ESTIMATE", "ESTIMATE: as 1-alpha + more patterning steps"),
    ("dram_wafer_cash_cost_1gamma_usd", "dram_wafer_cash_cost_1gamma_usd", 1850, 1650, 2300, "USD/wafer",
     "ESTIMATE", "ESTIMATE: as 1-beta + EUV consumables/power"),
    ("wafer_cost_1alpha_usd", "wafer_cost_1alpha_usd", 3400, 3000, 4000, "USD/wafer", "ESTIMATE",
     "ESTIMATE: bottom-up depreciation + cash cost (cost_stack.md s2)"),
    ("wafer_cost_1beta_usd", "wafer_cost_1beta_usd", 3800, 3200, 5500, "USD/wafer", "ESTIMATE",
     "ESTIMATE: bottom-up $3.75k; high $5.5k = new fab under-loaded (A1/A2 phase-2 value)"),
    ("wafer_cost_1gamma_usd", "wafer_cost_1gamma_usd", 4300, 3700, 6000, "USD/wafer", "ESTIMATE",
     "ESTIMATE: bottom-up $4.3k (1c/1-gamma, 1-7 EUV layers)"),
    ("wafer_cost_1z_usd", None, 3000, 2600, 3500, "USD/wafer", "ESTIMATE",
     "ESTIMATE: p1-cost cost_stack.md s6.1 1z reference row; DUV-only 1z-class line (CXMT-class) at full load"),
    ("wafer_cost_legacy_dram_depreciated_usd", "wafer_cost_legacy_dram_depreciated_usd", 1300, 1000, 1800,
     "USD/wafer", "ESTIMATE", "ESTIMATE: 300mm 2x/1x-nm DRAM line fully depreciated: cash cost only"),
    ("wafer_cost_legacy_dram_new_line_usd", "wafer_cost_legacy_dram_new_line_usd", 2800, 2300, 3500,
     "USD/wafer", "ESTIMATE", "ESTIMATE: new-build 2x/1x-nm DUV DRAM line (~$80-110k/wpm) at full load"),
    ("psmc_dram_foundry_wafer_usd", "psmc_dram_foundry_wafer_usd", 1600, 1200, 2200, "USD/wafer",
     "UNVERIFIED", "ESTIMATE: " + _PK + " PSMC 25/38nm DRAM foundry wafer; no public price"),
    ("tsv_process_wafer_adder_usd", "tsv_process_wafer_adder_usd", 650, 450, 1000, "USD/wafer", "ESTIMATE",
     "ESTIMATE: via-middle TSV, thinning, backside reveal, microbumps on HBM core wafer"),
    # --- die size / bits ------------------------------------------------------------------------
    ("die_ddr5_16gb_1alpha_mm2", "die_ddr5_16gb_1alpha_mm2", 53.3, 48.5, 57.1, "mm2", "ESTIMATE",
     "ESTIMATE: 16Gb / 0.30 Gb/mm2 " + _PK),
    ("die_ddr5_16gb_1beta_mm2", "die_ddr5_16gb_1beta_mm2", 41.0, 36.4, 48.5, "mm2", "ESTIMATE",
     "ESTIMATE: 16Gb / 0.39 Gb/mm2; high-density bound 0.436 Gb/mm2 (Kurnal via KitGuru, REPORTED)"),
    ("die_ddr5_24gb_1beta_mm2", "die_ddr5_24gb_1beta_mm2", 61.5, 54.5, 72.7, "mm2", "ESTIMATE",
     "ESTIMATE: 24Gb / 0.39 Gb/mm2"),
    ("die_ddr5_32gb_1beta_mm2", "die_ddr5_32gb_1beta_mm2", 80.0, 72.7, 97.0, "mm2", "ESTIMATE",
     "ESTIMATE: 32Gb at ~0.40 Gb/mm2; Samsung 12nm-class 32Gb DDR5 (2023-09) " + _PK),
    ("die_ddr5_16gb_1gamma_mm2", "die_ddr5_16gb_1gamma_mm2", 33.3, 29.1, 36.4, "mm2", "ESTIMATE",
     "ESTIMATE: 16Gb / 0.48 Gb/mm2"),
    ("die_ddr5_32gb_1gamma_mm2", "die_ddr5_32gb_1gamma_mm2", 66.7, 58.2, 72.7, "mm2", "ESTIMATE",
     "ESTIMATE: 32Gb / 0.48 Gb/mm2"),
    ("die_ddr5_16gb_cxmt_mm2", "die_ddr5_16gb_cxmt_mm2", 66.99, 66.99, 66.99, "mm2", "REPORTED",
     "https://semiwiki.com/forum/threads/chinas-cxmts-ddr5-reveals-3-year-technology-gap.23270/latest"),
    ("die_hbm3e_24gb_core_mm2", "die_hbm3e_24gb_core_mm2", 110, 95, 125, "mm2", "UNVERIFIED",
     "ESTIMATE: " + _PK + " HBM3E 24Gb core die on 1b/1-beta"),
    ("die_ddr4_8gb_1x_mm2", "die_ddr4_8gb_1x_mm2", 55, 50, 62, "mm2", "UNVERIFIED",
     "ESTIMATE: " + _PK + " 1x (18-19nm) DDR4 8Gb"),
    ("die_ddr4_16gb_1y_mm2", None, 88, 76, 107, "mm2", "ESTIMATE",
     "ESTIMATE: p1-model -- DDR4 8Gb 1y 45 mm2 x 1.95 (16Gb/8Gb area ratio at 1z: 76/39); low = 16Gb 1z "
     "76 mm2, high = 8Gb 1x 55 mm2 x 1.95"),
    ("die_ddr3_4gb_25nm_mm2", "die_ddr3_4gb_25nm_mm2", 60, 50, 70, "mm2", "UNVERIFIED",
     "ESTIMATE: " + _PK + " 25nm-class 4Gb DDR3 (Winbond/Nanya/PSMC-class)"),
    ("rdimm_ecc_bit_overhead", "rdimm_ecc_bit_overhead", 0.25, 0.25, 0.25, "fraction", "UNVERIFIED",
     "ESTIMATE: " + _PK + " DDR5 RDIMM 2 subchannels x (32 data + 8 ECC) bits (JESD79-5)"),
    ("hbm3e_core_dies_per_stack", None, 12, 8, 12, "dies", "ESTIMATE",
     "ESTIMATE: HBM3E 12-high 36GB stack (24Gb core dies)"),
    ("hbm3e_wafer_trade_ratio", "hbm3e_wafer_trade_ratio", 3.0, 2.5, 3.5, "x", "REPORTED",
     "https://www.tomshardware.com/tech-industry/semiconductors/micron-says-the-silicon-gap-between-hbm-and-"
     "ddr5-is-widening-with-every-generation"),
    # --- back-end ---------------------------------------------------------------------------------
    ("probe_sort_cost_per_die_usd", "probe_sort_cost_per_die_usd", 0.10, 0.05, 0.15, "USD/die", "ESTIMATE",
     "ESTIMATE: hot/cold sort + redundancy repair on parallel memory ATE (16Gb DDR5)"),
    ("fbga_assembly_cost_per_die_usd", "fbga_assembly_cost_per_die_usd", 0.18, 0.10, 0.35, "USD/die",
     "ESTIMATE", "ESTIMATE: single-die FBGA incl. substrate; p1-backend <$0.10 assembly-only in Asia"),
    ("final_test_burnin_cost_per_die_usd", "final_test_burnin_cost_per_die_usd", 0.17, 0.10, 0.30, "USD/die",
     "ESTIMATE", "ESTIMATE: at-speed final test + burn-in; DDR5 test times long"),
    ("backend_usd_per_gb_legacy_ddr4_8gb", "backend_usd_per_gb_legacy_ddr4_8gb", 0.30, 0.25, 0.50, "USD/GB",
     "ESTIMATE", "ESTIMATE: ~$0.30 per 8Gb DDR4 die"),
    ("backend_usd_per_gb_legacy_ddr3_4gb", "backend_usd_per_gb_legacy_ddr3_4gb", 0.60, 0.45, 0.90, "USD/GB",
     "ESTIMATE", "ESTIMATE: ~$0.30 per 4Gb DDR3 die"),
    ("backend_bit_scaling_exponent", None, 0.5, 0.0, 1.0, "-", "ESTIMATE",
     "ESTIMATE: p1-model -- probe/final-test cost per die grows ~sqrt(bits) on parallel ATE; package flat"),
    ("hbm_stack_assembly_test_usd", "hbm_stack_assembly_test_usd", 25, 15, 45, "USD/stack", "ESTIMATE",
     "ESTIMATE: TC-NCF or MR-MUF stacking, molding, stack test"),
    ("hbm3e_base_die_usd", "hbm3e_base_die_usd", 15, 8, 30, "USD/die", "ESTIMATE",
     "ESTIMATE: DRAM-process base die (HBM3E)"),
    # --- module BOM -------------------------------------------------------------------------------
    ("rcd_ddr5_usd", "rcd_ddr5_usd", 7.0, 4.0, 12.0, "USD", "UNVERIFIED",
     "ESTIMATE: " + _PK + " DDR5 RCD (Renesas/Rambus/Montage)"),
    ("pmic_rdimm_usd", "pmic_rdimm_usd", 3.5, 2.0, 6.0, "USD", "UNVERIFIED", "ESTIMATE: " + _PK + " 12V server PMIC"),
    ("pmic_client_usd", "pmic_client_usd", 1.5, 0.8, 2.5, "USD", "UNVERIFIED", "ESTIMATE: " + _PK + " 5V client PMIC"),
    ("spd_hub_usd", "spd_hub_usd", 0.7, 0.4, 1.2, "USD", "UNVERIFIED", "ESTIMATE: " + _PK + " SPD5118 hub"),
    ("temp_sensor_usd", "temp_sensor_usd", 0.35, 0.2, 0.6, "USD", "UNVERIFIED",
     "ESTIMATE: " + _PK + " TS5110 class; 2 per RDIMM"),
    ("pcb_rdimm_usd", "pcb_rdimm_usd", 4.0, 2.5, 8.0, "USD", "UNVERIFIED", "ESTIMATE: " + _PK + " 10-12 layer PCB"),
    ("pcb_udimm_usd", "pcb_udimm_usd", 1.5, 1.0, 2.5, "USD", "UNVERIFIED", "ESTIMATE: " + _PK + " 8-layer PCB"),
    ("passives_rdimm_usd", "passives_rdimm_usd", 1.2, 0.8, 2.0, "USD", "UNVERIFIED", "ESTIMATE: " + _PK),
    ("passives_udimm_usd", "passives_udimm_usd", 0.5, 0.3, 0.8, "USD", "UNVERIFIED", "ESTIMATE: " + _PK),
    ("module_assembly_test_rdimm_asia_usd", "module_assembly_test_rdimm_asia_usd", 3.5, 2.0, 6.0, "USD",
     "UNVERIFIED", "ESTIMATE: " + _PK + " SMT + at-speed module test + burn-in, Asian volume"),
    ("module_assembly_test_rdimm_us_usd", "module_assembly_test_rdimm_us_usd", 12.0, 8.0, 15.0, "USD",
     "ESTIMATE", "ESTIMATE: p1-backend U.S.-labor figure (research/phase1/us_backend.md)"),
    ("module_assembly_test_udimm_usd", "module_assembly_test_udimm_usd", 1.5, 0.8, 2.5, "USD", "UNVERIFIED",
     "ESTIMATE: " + _PK + " SMT + module test"),
    # --- market prices ------------------------------------------------------------------------------
    ("contract_64gb_rdimm_4q26_usd", None, 1300, 1200, 1586, "USD/module", "ESTIMATE",
     "ESTIMATE: p1-model -- Counterpoint 64GB RDIMM 2Q26 ~$1,000 (" + _EET + ") x TrendForce 3Q26 +15.5% (" +
     _IGOR + ") x 4Q26 +12.5% (" + _TF0930 + "); high = Citi 4Q26F $1,586 [UNVERIFIED]; low = p1-cost low"),
    ("price_64gb_rdimm_contract_4q26f_usd", "price_64gb_rdimm_contract_4q26f_usd", 1586, 1200, 1586,
     "USD/module", "UNVERIFIED", "ESTIMATE: [UNVERIFIED] Citi note (May 2026) per p1-market; page not identified"),
    ("price_64gb_rdimm_contract_1q26_usd", "price_64gb_rdimm_contract_1q26_usd", 900, 900, 1000, "USD/module",
     "REPORTED", _EET),
    ("price_64gb_rdimm_contract_4q25_usd", "price_64gb_rdimm_contract_4q25_usd", 450, 450, 450, "USD/module",
     "REPORTED", _EET),
    ("contract_dram_qoq_2q26", None, 0.605, 0.58, 0.63, "fraction", "REPORTED", _TECHNEWS_2Q),
    ("contract_dram_qoq_3q26", None, 0.155, 0.13, 0.18, "fraction", "REPORTED", _IGOR),
    ("contract_dram_qoq_4q26f", "contract_dram_qoq_4q26f", 0.125, 0.10, 0.15, "fraction", "REPORTED", _TF0930),
    ("price_ddr5_16gb_contract_4q26_derived_usd", "price_ddr5_16gb_contract_4q26_derived_usd", 30.7, 22.0,
     39.1, "USD/chip", "ESTIMATE", "ESTIMATE: p1-cost, backed out of RDIMM contract (cost_stack.md s7)"),
    ("price_ddr5_16gb_spot_2026_08_31_usd", "price_ddr5_16gb_spot_2026_08_31_usd", 53.92, 37.2, 67.5,
     "USD/chip", "REPORTED", "https://www.buysellram.com/blog/ram-market-update/"),
    ("price_ddr5_16gb_spot_2023_trough_usd", "price_ddr5_16gb_spot_2023_trough_usd", 3.2, 2.8, 3.6,
     "USD/chip", "UNVERIFIED", "ESTIMATE: " + _PK + " DDR5 16Gb spot low 2Q-3Q23 (~$1.4-1.8/GB)"),
    ("price_ddr4_8gb_contract_2023_09_usd", "price_ddr4_8gb_contract_2023_09_usd", 1.30, 1.30, 1.30,
     "USD/chip", "REPORTED", "https://www.kedglobal.com/korean-chipmakers/newsView/ked202310040013"),
    ("price_ddr4_8gb_spot_2026_08_31_usd", "price_ddr4_8gb_spot_2026_08_31_usd", 44.37, 23.8, 76.0,
     "USD/chip", "REPORTED", "https://www.buysellram.com/blog/ram-market-update/"),
    ("price_ddr3_4gb_spot_2026_07_usd_per_gb", "price_ddr3_4gb_spot_2026_07_usd_per_gb", 25.52, 25.52, 25.52,
     "USD/GB", "REPORTED",
     "https://wccftech.com/memory-shortages-drive-ddr4-prices-over-50-in-q3-2026-ddr3-also-impacted-by-higher-costs/"),
    ("legacy_contract_vs_ddr5_ratio", None, 1.0, 0.8, 1.65, "x", "ESTIMATE",
     "ESTIMATE: p1-model -- no 4Q26 DDR4 contract level found; Barclays Oct-2026: DDR4 contract rising "
     "faster than DDR5, dearer in some channels (" + _BARCLAYS + " via p1-market); high = 2026-08-31 "
     "DDR4/DDR5 spot $/GB ratio 1.65"),
    ("price_hbm3e_usd_per_gb_2026", "price_hbm3e_usd_per_gb_2026", 12.0, 12.0, 12.0, "USD/GB", "REPORTED",
     "https://www.sammyfans.com/2026/10/02/samsung-seeks-more-than-3x-hbm3e-pricing-for-hbm4/"),
    ("price_hbm4_usd_per_gb_2027f", "price_hbm4_usd_per_gb_2027f", 36.0, 32.0, 40.0, "USD/GB", "REPORTED",
     "https://siliconanalysts.com/market/samsung-hbm4-2027-pricing-set-to-more-than-double-2026-10-07"),
    ("price_ddr5_retail_usd_per_gb_2026_09", "price_ddr5_retail_usd_per_gb_2026_09", 18.04, 13.0, 18.04,
     "USD/GB", "REPORTED", "https://rampricesusa.com/insights/monthly/2026-09"),
    ("price_ddr5_32gb_kit_retail_2026_usd", "price_ddr5_32gb_kit_retail_2026_usd", 450, 409, 470, "USD/kit",
     "REPORTED", "https://www.digitalcitizen.life/ddr5-ram-prices-surge-in-2026-as-32gb-kits-reach-450-amid-"
     "global-memory-shortage/"),
    ("glut_price_decline_fraction", "glut_price_decline_fraction", 0.60, 0.60, 0.90, "fraction", "ESTIMATE",
     "ESTIMATE: ASSUMPTIONS.md A-05 (mission rule 6) -60% from 2026 peak; high = 2023-style floor -85-90%"),
    ("gross_margin_nanya_3q26", "gross_margin_nanya_3q26", 0.857, 0.857, 0.857, "fraction", "REPORTED",
     "https://www.trendforce.com/news/?p=65146"),
    ("gross_margin_micron_fq4_26_nongaap", "gross_margin_micron_fq4_26_nongaap", 0.87, 0.86, 0.87, "fraction",
     "REPORTED", "https://finviz.com/news/397277/micron-technology-inc-reports-record-fiscal-fourth-quarter-"
     "and-full-year-2026-results"),
    ("op_margin_skhynix_3q26", "op_margin_skhynix_3q26", 0.797, 0.797, 0.797, "fraction", "REPORTED",
     "https://www.placera.se/pressmeddelanden/sk-hynix-announces-3q26-financial-results-20261028"),
]


def _clean_basis(text):
    text = (text or "").replace(
        "[UNVERIFIED: prior knowledge (training data <= mid-2026); web search/fetch unavailable to p1-cost]",
        _PK)
    return " ".join(text.split())


def _load_inputs():
    """Build INPUTS: name -> {value, low, high, unit, tag, source, origin}."""
    records, status = {}, ""
    try:
        raw = json.loads(INPUTS_JSON.read_text(encoding="utf-8"))
        records = {r["key"]: r for r in raw.get("inputs", []) if "key" in r}
        status = "loaded %d records from research/phase1/cost_inputs.json" % len(records)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        status = "cost_inputs.json unavailable (%s); hard-coded fallbacks used" % exc.__class__.__name__
    out, n_json = {}, 0
    for name, jkey, val, low, high, unit, tag, src in _SPEC:
        rec = records.get(jkey) if jkey else None
        if rec is not None:
            try:
                url = rec.get("source_url") or ""
                rtag = rec.get("tag") or rec.get("confidence") or "ESTIMATE"
                if url.startswith("http") and rtag in ("VERIFIED", "REPORTED"):
                    source = url
                else:
                    source = "ESTIMATE: " + _clean_basis(rec.get("basis")) + (" | ref: " + url if url else "")
                out[name] = dict(value=float(rec["value"]), low=float(rec["low"]), high=float(rec["high"]),
                                 unit=rec.get("unit") or unit, tag=rtag, source=source,
                                 origin="cost_inputs.json")
                n_json += 1
                continue
            except (KeyError, TypeError, ValueError):
                pass
        out[name] = dict(value=float(val), low=float(low), high=float(high), unit=unit, tag=tag, source=src,
                         origin="fallback" if jkey else "p1-model")
    return out, "%s; %d of %d INPUTS taken from it" % (status, n_json, len(_SPEC))


INPUTS, INPUTS_STATUS = _load_inputs()
BASE = {k: v["value"] for k, v in INPUTS.items()}

# ----------------------------------------------------------------------------------------------
# Cases. yref_die = the die whose area the stated yield refers to (same node); None = this die.
# ----------------------------------------------------------------------------------------------
CASES = [
    dict(id="ddr5_16g_1a", label="DDR5 16Gb 1-alpha (mature)", fam="DDR5", gbit=16,
         die="die_ddr5_16gb_1alpha_mm2", wafer="wafer_cost_1alpha_usd", yld="dram_die_yield_mature",
         yref_die=None, be="ddr5"),
    dict(id="ddr5_16g_1b", label="DDR5 16Gb 1-beta (BASE)", fam="DDR5", gbit=16,
         die="die_ddr5_16gb_1beta_mm2", wafer="wafer_cost_1beta_usd", yld="dram_die_yield_mature",
         yref_die=None, be="ddr5"),
    dict(id="ddr5_16g_1b_cash", label="DDR5 16Gb 1-beta cash cost only", fam="DDR5", gbit=16,
         die="die_ddr5_16gb_1beta_mm2", wafer="dram_wafer_cash_cost_1beta_usd", yld="dram_die_yield_mature",
         yref_die=None, be="ddr5"),
    dict(id="ddr5_24g_1b", label="DDR5 24Gb 1-beta", fam="DDR5", gbit=24,
         die="die_ddr5_24gb_1beta_mm2", wafer="wafer_cost_1beta_usd", yld="dram_die_yield_mature",
         yref_die="die_ddr5_16gb_1beta_mm2", be="ddr5"),
    dict(id="ddr5_32g_1b", label="DDR5 32Gb 1-beta", fam="DDR5", gbit=32,
         die="die_ddr5_32gb_1beta_mm2", wafer="wafer_cost_1beta_usd", yld="dram_die_yield_mature",
         yref_die="die_ddr5_16gb_1beta_mm2", be="ddr5"),
    dict(id="ddr5_16g_1c_ramp", label="DDR5 16Gb 1-gamma (2026 ramp)", fam="DDR5", gbit=16,
         die="die_ddr5_16gb_1gamma_mm2", wafer="wafer_cost_1gamma_usd", yld="dram_die_yield_1c_1gamma_2026",
         yref_die=None, be="ddr5"),
    dict(id="ddr5_16g_1c", label="DDR5 16Gb 1-gamma (mature 2027+)", fam="DDR5", gbit=16,
         die="die_ddr5_16gb_1gamma_mm2", wafer="wafer_cost_1gamma_usd", yld="dram_die_yield_mature",
         yref_die=None, be="ddr5"),
    dict(id="ddr5_32g_1c", label="DDR5 32Gb 1-gamma (mature 2027+)", fam="DDR5", gbit=32,
         die="die_ddr5_32gb_1gamma_mm2", wafer="wafer_cost_1gamma_usd", yld="dram_die_yield_mature",
         yref_die="die_ddr5_16gb_1gamma_mm2", be="ddr5"),
    dict(id="hbm3e_12h", label="HBM3E 12-high 36GB (1-beta + TSV)", fam="HBM", gbit=24,
         die="die_hbm3e_24gb_core_mm2", wafer="wafer_cost_1beta_usd", yld="hbm3e_core_die_yield",
         yref_die=None, be="hbm"),
    dict(id="ddr5_16g_1z", label="Trailing: DDR5 16Gb 1z-class (CXMT G4 die)", fam="DDR5", gbit=16,
         die="die_ddr5_16gb_cxmt_mm2", wafer="wafer_cost_1z_usd", yld="dram_die_yield_mature",
         yref_die=None, be="ddr5"),
    dict(id="ddr4_16g_1y_dep", label="DDR4 16Gb 1y, depreciated line", fam="LEGACY", gbit=16,
         die="die_ddr4_16gb_1y_mm2", wafer="wafer_cost_legacy_dram_depreciated_usd",
         yld="dram_die_yield_legacy_depreciated", yref_die="die_ddr4_8gb_1x_mm2", be="ddr4"),
    dict(id="ddr4_8g_1x_new", label="Trailing: DDR4 8Gb 1x, NEW U.S.-style line", fam="LEGACY", gbit=8,
         die="die_ddr4_8gb_1x_mm2", wafer="wafer_cost_legacy_dram_new_line_usd",
         yld="dram_die_yield_legacy_new_line", yref_die=None, be="ddr4"),
    dict(id="ddr3_4g_fdry", label="Trailing: DDR3 4Gb 25nm, PSMC-class foundry", fam="LEGACY", gbit=4,
         die="die_ddr3_4gb_25nm_mm2", wafer="psmc_dram_foundry_wafer_usd",
         yld="dram_die_yield_foundry_legacy", yref_die=None, be="ddr3"),
]
CASE_BY_ID = {c["id"]: c for c in CASES}
REF_CASE = "ddr5_16g_1b"

# Modules: kind rdimm = side-band ECC (+25% raw bits), x4 devices; udimm = non-ECC client module.
MODULES = [
    dict(id="rdimm64_16g_1b", label="64GB RDIMM 2Rx4, 16Gb 1-beta", kind="rdimm", user_gb=64,
         case="ddr5_16g_1b", assy="asia"),
    dict(id="rdimm64_16g_1b_us", label="64GB RDIMM 16Gb 1-beta, U.S. assembly", kind="rdimm", user_gb=64,
         case="ddr5_16g_1b", assy="us"),
    dict(id="rdimm64_16g_1c", label="64GB RDIMM 2Rx4, 16Gb 1-gamma ramp", kind="rdimm", user_gb=64,
         case="ddr5_16g_1c_ramp", assy="asia"),
    dict(id="rdimm64_32g_1b", label="64GB RDIMM 1Rx4, 32Gb 1-beta", kind="rdimm", user_gb=64,
         case="ddr5_32g_1b", assy="asia"),
    dict(id="rdimm64_32g_1c", label="64GB RDIMM 1Rx4, 32Gb 1-gamma mature", kind="rdimm", user_gb=64,
         case="ddr5_32g_1c", assy="asia"),
    dict(id="rdimm96_24g_1b", label="96GB RDIMM 2Rx4, 24Gb 1-beta", kind="rdimm", user_gb=96,
         case="ddr5_24g_1b", assy="asia"),
    dict(id="udimm32_16g_1b", label="32GB UDIMM 2Rx8, 16Gb 1-beta", kind="udimm", user_gb=32,
         case="ddr5_16g_1b", assy="asia"),
    dict(id="udimm32_32g_1c", label="32GB UDIMM 1Rx8, 32Gb 1-gamma mature", kind="udimm", user_gb=32,
         case="ddr5_32g_1c", assy="asia"),
    dict(id="udimm48_24g_1b", label="48GB UDIMM 2Rx8, 24Gb 1-beta", kind="udimm", user_gb=48,
         case="ddr5_24g_1b", assy="asia"),
]


# ----------------------------------------------------------------------------------------------
# Core formulas
# ----------------------------------------------------------------------------------------------
def gross_dies_per_wafer(die_mm2, wafer_mm, edge_mm, scribe_mm):
    d = wafer_mm - 2.0 * edge_mm
    s = (math.sqrt(die_mm2) + scribe_mm) ** 2
    return math.pi * (d / 2.0) ** 2 / s - math.pi * d / math.sqrt(2.0 * s)


def negbin_yield(area_mm2, d0_per_cm2, alpha):
    return (1.0 + (area_mm2 / 100.0) * d0_per_cm2 / alpha) ** (-alpha)


def calibrate_d0(yield_ref, area_ref_mm2, alpha):
    """Effective (unrepairable) defect density that gives yield_ref at area_ref."""
    return (yield_ref ** (-1.0 / alpha) - 1.0) * alpha / (area_ref_mm2 / 100.0)


def wafer_cost_bottom_up(p, node):
    capex = p["dram_capex_per_wpm_%s_usd" % node]
    util, share = p["fab_utilization"], p["dram_tool_share_of_capex"]
    tools = capex * share / p["dram_tool_depreciation_years"] / (12.0 * util)
    bldg = capex * (1.0 - share) / p["dram_building_depreciation_years"] / (12.0 * util)
    cash = p["dram_wafer_cash_cost_%s_usd" % node]
    return dict(tools=tools, bldg=bldg, cash=cash, total=tools + bldg + cash)


def backend_profile(kind, p):
    """Per-die (probe, package, final test+burn-in) at the profile's reference density."""
    pr, pk, ft = (p["probe_sort_cost_per_die_usd"], p["fbga_assembly_cost_per_die_usd"],
                  p["final_test_burnin_cost_per_die_usd"])
    tot = pr + pk + ft
    if kind in ("ddr5", "hbm"):
        return pr, pk, ft, 16.0
    if kind == "ddr4":      # $/GB x 1 GB per 8Gb die, split in DDR5 proportions
        t = p["backend_usd_per_gb_legacy_ddr4_8gb"] * 1.0
        return t * pr / tot, t * pk / tot, t * ft / tot, 8.0
    if kind == "ddr3":      # $/GB x 0.5 GB per 4Gb die
        t = p["backend_usd_per_gb_legacy_ddr3_4gb"] * 0.5
        return t * pr / tot, t * pk / tot, t * ft / tot, 4.0
    raise ValueError(kind)


def compute_case(c, p, wafer_mult=1.0, yield_mult=1.0, die_mult=1.0, backend_mult=1.0):
    alpha = p["yield_negbin_alpha"]
    area = p[c["die"]] * die_mult
    area_ref = p[c["yref_die"]] if c["yref_die"] else p[c["die"]]
    y_ref = min(p[c["yld"]] * yield_mult, YIELD_CAP)
    d0 = calibrate_d0(y_ref, area_ref, alpha)
    y = negbin_yield(area, d0, alpha)
    gdpw = gross_dies_per_wafer(area, p["wafer_diameter_mm"], p["edge_exclusion_mm"], p["scribe_lane_mm"])
    wafer = p[c["wafer"]] + (p["tsv_process_wafer_adder_usd"] if c["fam"] == "HBM" else 0.0)
    wafer *= wafer_mult
    good = gdpw * y
    gb_die = c["gbit"] / 8.0
    fe_die = wafer / good
    pr, pk, ft, ref_gbit = backend_profile(c["be"], p)
    scale = (c["gbit"] / ref_gbit) ** p["backend_bit_scaling_exponent"]
    probe_die = pr * scale * backend_mult / y          # every gross die is probed
    r = dict(id=c["id"], label=c["label"], fam=c["fam"], gbit=c["gbit"], gb_die=gb_die, die_mm2=area,
             density=c["gbit"] / area, gdpw=gdpw, yld=y, d0=d0, good=good, wafer=wafer, fe_die=fe_die)
    if c["fam"] == "HBM":
        n = p["hbm3e_core_dies_per_stack"]
        stack_gb = n * gb_die
        sy = p["hbm3e_12h_stack_yield"]
        pre_core = n * (fe_die + probe_die)
        adders = (p["hbm3e_base_die_usd"] + p["hbm_stack_assembly_test_usd"]) * backend_mult
        stack = (pre_core + adders) / sy
        r.update(stack_gb=stack_gb, stack_usd=stack, stack_yield=sy,
                 wafer_gb=n * fe_die / stack_gb, probe_test_gb=n * probe_die / stack_gb,
                 package_gb=adders / stack_gb, gb_per_wafer=good * gb_die * sy)
        pre = r["wafer_gb"] + r["probe_test_gb"] + r["package_gb"]
        r["component_gb"] = stack / stack_gb
    else:
        ft_die = ft * scale * backend_mult
        pk_die = pk * backend_mult
        r.update(wafer_gb=fe_die / gb_die, probe_test_gb=(probe_die + ft_die) / gb_die,
                 package_gb=pk_die / gb_die, gb_per_wafer=good * gb_die)
        pre = r["wafer_gb"] + r["probe_test_gb"] + r["package_gb"]
        r["component_gb"] = pre / p["final_test_yield"]
    r["fallout_gb"] = r["component_gb"] - pre
    r["component_die"] = r["component_gb"] * gb_die
    return r


def module_nondram(kind, assy, p):
    if kind == "rdimm":
        bom = (p["rcd_ddr5_usd"] + p["pmic_rdimm_usd"] + p["spd_hub_usd"] + 2 * p["temp_sensor_usd"] +
               p["pcb_rdimm_usd"] + p["passives_rdimm_usd"])
        a = p["module_assembly_test_rdimm_us_usd"] if assy == "us" else p["module_assembly_test_rdimm_asia_usd"]
    else:
        bom = p["pmic_client_usd"] + p["spd_hub_usd"] + p["pcb_udimm_usd"] + p["passives_udimm_usd"]
        a = p["module_assembly_test_udimm_usd"]
    return bom, a


def compute_module(m, p, comp):
    raw_gb = m["user_gb"] * ((1.0 + p["rdimm_ecc_bit_overhead"]) if m["kind"] == "rdimm" else 1.0)
    n_dev = raw_gb / comp["gb_die"]
    dram = raw_gb * comp["component_gb"]
    bom, assy = module_nondram(m["kind"], m["assy"], p)
    total = (dram + bom + assy) / p["module_assembly_yield"]
    return dict(id=m["id"], label=m["label"], kind=m["kind"], user_gb=m["user_gb"], raw_gb=raw_gb,
                n_dev=n_dev, dram=dram, bom=bom, assy=assy, total=total, per_gb=total / m["user_gb"],
                yield_loss=total - (dram + bom + assy))


def market(p):
    """Market price decks in $/GB. Component prices are per raw GB; module prices per user GB."""
    glut, severe = p["glut_price_decline_fraction"], INPUTS["glut_price_decline_fraction"]["high"]
    bom_r, assy_r = module_nondram("rdimm", "asia", p)
    raw_r = 64 * (1.0 + p["rdimm_ecc_bit_overhead"])
    rdimm = p["contract_64gb_rdimm_4q26_usd"]
    ddr5 = (rdimm - bom_r - assy_r) / raw_r                    # DRAM content of the RDIMM contract
    ddr5_trough = p["price_ddr5_16gb_spot_2023_trough_usd"] / 2.0
    legacy = ddr5 * p["legacy_contract_vs_ddr5_ratio"]
    m = dict(
        ddr5=dict(today=ddr5, glut=ddr5 * (1 - glut), severe=ddr5 * (1 - severe), trough=ddr5_trough),
        LEGACY=dict(today=legacy, glut=legacy * (1 - glut), severe=legacy * (1 - severe),
                    trough=p["price_ddr4_8gb_contract_2023_09_usd"]),
        HBM=dict(today=p["price_hbm3e_usd_per_gb_2026"], glut=p["price_hbm3e_usd_per_gb_2026"] * (1 - glut),
                 severe=None, trough=None),
        rdimm_module=rdimm, rdimm_nondram=bom_r + assy_r, glut=glut, severe=severe,
    )
    m["DDR5"] = m["ddr5"]
    m["rdimm"] = dict(today=rdimm / 64.0, glut=rdimm / 64.0 * (1 - glut),
                      severe=rdimm / 64.0 * (1 - severe), trough=(ddr5_trough * raw_r + bom_r + assy_r) / 64.0)
    bom_u, assy_u = module_nondram("udimm", "asia", p)
    m["udimm_fn"] = lambda gb, price_gb: (price_gb * gb + bom_u + assy_u) / gb
    u_today = m["udimm_fn"](32, ddr5)
    m["udimm"] = dict(today=u_today, glut=u_today * (1 - glut), severe=u_today * (1 - severe),
                      trough=m["udimm_fn"](32, ddr5_trough))
    return m


def gm(price, cost):
    return None if price in (None, 0) else 1.0 - cost / price


# ----------------------------------------------------------------------------------------------
# Whole-model run (pure; no printing) and importable reference values
# ----------------------------------------------------------------------------------------------
def run_model(p=None):
    p = dict(BASE if p is None else p)
    cases = {c["id"]: compute_case(c, p) for c in CASES}
    modules = {m["id"]: compute_module(m, p, cases[m["case"]]) for m in MODULES}
    return dict(p=p, cases=cases, modules=modules, market=market(p))


_REF_CACHE = {}


def ddr5_reference():
    """Key DDR5 reference numbers ($/GB, nominal USD, as of 2026-11-01) for downstream models.

    Component values are per raw GB of packaged DDR5 (16Gb, 1-beta unless noted). Module values are
    per user GB of a 64GB DDR5 RDIMM. Prices: Q4-2026 contract (derived from the 64GB RDIMM contract
    anchor), the A-05 glut (-60% from the 2026 peak = Q4-2026), and the 2023 trough. All [ESTIMATE].
    """
    if not _REF_CACHE:
        r = run_model()
        c, mk, mod = r["cases"], r["market"], r["modules"]["rdimm64_16g_1b"]
        ref = c[REF_CASE]["component_gb"]
        _REF_CACHE.update(dict(
            as_of=AS_OF, source="models/dram_cost_stack.py", basis="raw GB, packaged component unless noted",
            cost_component_usd_per_gb=round(ref, 3),
            cost_component_usd_per_gb_1gamma_2026_ramp=round(c["ddr5_16g_1c_ramp"]["component_gb"], 3),
            cost_component_usd_per_gb_1gamma_mature=round(c["ddr5_16g_1c"]["component_gb"], 3),
            cost_cash_only_usd_per_gb=round(c["ddr5_16g_1b_cash"]["component_gb"], 3),
            cost_rdimm64_usd_per_user_gb=round(mod["per_gb"], 3),
            contract_component_usd_per_gb_q4_2026=round(mk["ddr5"]["today"], 3),
            contract_rdimm64_usd_per_user_gb_q4_2026=round(mk["rdimm"]["today"], 3),
            glut_component_usd_per_gb=round(mk["ddr5"]["glut"], 3),
            glut_rdimm64_usd_per_user_gb=round(mk["rdimm"]["glut"], 3),
            severe_glut_component_usd_per_gb=round(mk["ddr5"]["severe"], 3),
            trough_2023_ddr5_usd_per_gb=round(mk["ddr5"]["trough"], 3),
            trough_2023_ddr4_usd_per_gb=round(mk["LEGACY"]["trough"], 3),
            spot_ddr5_usd_per_gb_2026_08_31=round(r["p"]["price_ddr5_16gb_spot_2026_08_31_usd"] / 2.0, 3),
            gm_component_q4_2026=round(gm(mk["ddr5"]["today"], ref), 4),
            gm_component_glut=round(gm(mk["ddr5"]["glut"], ref), 4),
            gm_component_trough_2023=round(gm(mk["ddr5"]["trough"], ref), 4),
            hbm3e_cost_usd_per_gb=round(c["hbm3e_12h"]["component_gb"], 3),
            hbm3e_price_usd_per_gb_2026=r["p"]["price_hbm3e_usd_per_gb_2026"],
            ddr4_new_us_line_cost_usd_per_gb=round(c["ddr4_8g_1x_new"]["component_gb"], 3),
            ddr4_depreciated_cost_usd_per_gb=round(c["ddr4_16g_1y_dep"]["component_gb"], 3),
        ))
    return dict(_REF_CACHE)


# ----------------------------------------------------------------------------------------------
# Printing helpers (ASCII only so any terminal encoding works)
# ----------------------------------------------------------------------------------------------
def table(headers, rows, align=None):
    rows = [["" if v is None else str(v) for v in r] for r in rows]
    w = [max(len(str(h)), *(len(r[i]) for r in rows)) if rows else len(str(h)) for i, h in enumerate(headers)]
    align = align or ["l"] + ["r"] * (len(headers) - 1)
    fmt = lambda cells: "  ".join(c.ljust(w[i]) if align[i] == "l" else c.rjust(w[i]) for i, c in enumerate(cells))
    lines = [fmt([str(h) for h in headers]), "  ".join("-" * x for x in w)] + [fmt(r) for r in rows]
    print("\n".join(lines))


def f2(x):
    return "n/a" if x is None else "%.2f" % x


def pct(x):
    return "n/a" if x is None else "%.0f%%" % (round(100 * x) + 0.0)


def section(title):
    print("\n" + "=" * 100 + "\n" + title + "\n" + "=" * 100)


def tornado(rows, base, width=34, fmt=f2):
    """rows: (label, value_at_minus, value_at_plus). Sorted by swing, ASCII bars around base '|'."""
    rows = sorted(rows, key=lambda r: -abs(r[2] - r[1]))
    vmin = min([base] + [min(r[1], r[2]) for r in rows])
    vmax = max([base] + [max(r[1], r[2]) for r in rows])
    span = (vmax - vmin) or 1.0
    pos = lambda v: int(round((v - vmin) / span * (width - 1)))
    out = []
    for lab, lo, hi in rows:
        bar = [" "] * width
        a, b = sorted((pos(lo), pos(hi)))
        for i in range(a, b + 1):
            bar[i] = "="
        bar[pos(base)] = "|"
        out.append([lab, fmt(lo), fmt(hi), fmt(abs(hi - lo)), "[" + "".join(bar) + "]"])
    table(["Driver", "at -", "at +", "swing", "%s .. %s  ('|' = base %s)" % (fmt(vmin), fmt(vmax), fmt(base))],
          out, ["l", "r", "r", "r", "l"])


# ----------------------------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------------------------
def report():
    r = run_model()
    p, cases, mods, mk = r["p"], r["cases"], r["modules"], r["market"]
    ref = cases[REF_CASE]

    section("DRAM COST STACK -- American Memory, Phase 1 (models/dram_cost_stack.py)   as of %s" % AS_OF)
    print("Inputs: %s." % INPUTS_STATUS)
    print("All outputs are [ESTIMATE]. Market prices are [REPORTED] via other agents' search snippets, or\n"
          "[UNVERIFIED]. Component $/GB = per raw GB; module $/GB = per user GB (RDIMM carries +25% ECC bits).")

    section("1. KEY INPUTS (value, low-high range; full source strings in INPUTS / cost_inputs.json)")
    rows = []
    for name, d in INPUTS.items():
        src = d["source"]
        rows.append([name, "%g" % d["value"], "%g-%g" % (d["low"], d["high"]), d["unit"][:12], d["tag"][:10],
                     (src[:58] + "..") if len(src) > 60 else src])
    table(["input", "value", "range", "unit", "tag", "source (URL or ESTIMATE: basis)"], rows,
          ["l", "r", "r", "l", "l", "l"])

    section("2. WAFER COST CROSS-CHECK: bottom-up (capex/wpm, depreciation, utilization, cash) vs model input")
    rows = []
    for node, key in (("1alpha", "wafer_cost_1alpha_usd"), ("1beta", "wafer_cost_1beta_usd"),
                      ("1gamma", "wafer_cost_1gamma_usd")):
        b = wafer_cost_bottom_up(p, node)
        rows.append([node, "%.0f" % p["dram_capex_per_wpm_%s_usd" % node], "%.0f" % b["tools"], "%.0f" % b["bldg"],
                     "%.0f" % b["cash"], "%.0f" % b["total"], "%.0f" % p[key],
                     pct((b["tools"] + b["bldg"]) / b["total"])])
    table(["node", "capex $/wpm", "tool depr", "bldg depr", "cash", "bottom-up", "model input", "depr share"], rows)
    print("Other wafer inputs: 1z-class $%.0f | legacy depreciated (cash) $%.0f | legacy NEW line $%.0f | "
          "PSMC-class foundry $%.0f | HBM TSV adder +$%.0f"
          % (p["wafer_cost_1z_usd"], p["wafer_cost_legacy_dram_depreciated_usd"],
             p["wafer_cost_legacy_dram_new_line_usd"], p["psmc_dram_foundry_wafer_usd"],
             p["tsv_process_wafer_adder_usd"]))

    section("3. WAFER -> GOOD DIES -> BITS  (300mm, edge excl %.0f mm, scribe %.0f um, neg-binomial alpha=%g)"
            % (p["edge_exclusion_mm"], p["scribe_lane_mm"] * 1000, p["yield_negbin_alpha"]))
    rows = []
    for c in CASES:
        x = cases[c["id"]]
        rows.append([x["label"], "%.0f" % x["wafer"], "%.1f" % x["die_mm2"], "%.3f" % x["density"],
                     "%.0f" % x["gdpw"], "%.3f" % x["yld"], "%.2f" % x["d0"], "%.0f" % x["good"],
                     "%.0f" % x["gb_per_wafer"]])
    table(["case", "wafer $", "die mm2", "Gb/mm2", "GDPW", "yield", "D0eff/cm2", "good dies", "GB/wafer"], rows)
    print("D0eff = unrepairable defect density calibrated to the stated yield on the node's reference die\n"
          "(DRAM redundancy repairs most array defects). HBM GB/wafer includes the stack yield.")

    section("4. COST CHAIN  $/GB:  wafer-level -> +probe/test/burn-in -> +package -> +test fallout = COMPONENT")
    rows = []
    for c in CASES:
        x = cases[c["id"]]
        rows.append([x["label"], f2(x["wafer_gb"]), f2(x["probe_test_gb"]), f2(x["package_gb"]),
                     f2(x["fallout_gb"]), f2(x["component_gb"]), f2(x["component_die"])])
    table(["case", "wafer $/GB", "+probe/test", "+package", "+fallout", "COMPONENT $/GB", "$/die|stack"], rows)
    h = cases["hbm3e_12h"]
    ratio = ref["gb_per_wafer"] / h["gb_per_wafer"]
    print("HBM3E: 'package' column = base die $%.0f + stacking/stack test $%.0f per stack; fallout = stack yield "
          "%.2f.\n  Stack cost $%.0f (%.0f GB) = $%.2f/GB, %.1fx DDR5 1-beta. Wafer trade ratio (DDR5 GB/wafer "
          "/ HBM GB/wafer)\n  = %.2fx vs Micron's reported ~%.0f:1 (Tom's Hardware 2026) -> model penalty is "
          "consistent."
          % (p["hbm3e_base_die_usd"], p["hbm_stack_assembly_test_usd"], h["stack_yield"], h["stack_usd"],
             h["stack_gb"], h["component_gb"], h["component_gb"] / ref["component_gb"], ratio,
             p["hbm3e_wafer_trade_ratio"]))

    section("5. MODULES  (component $/GB x raw GB + non-DRAM BOM + assembly/test) / module yield %.3f"
            % p["module_assembly_yield"])
    rows = []
    for m in MODULES:
        x = mods[m["id"]]
        rows.append([x["label"], "%.0f" % x["n_dev"], "%.0f" % x["raw_gb"], "%.2f" % x["dram"], "%.2f" % x["bom"],
                     "%.2f" % x["assy"], "%.2f" % x["yield_loss"], "%.2f" % x["total"], f2(x["per_gb"])])
    table(["module", "devices", "raw GB", "DRAM $", "BOM $", "assy $", "yld loss", "MODULE $", "$/user-GB"], rows)
    us, asia = mods["rdimm64_16g_1b_us"], mods["rdimm64_16g_1b"]
    print("U.S. module assembly adds $%.2f per 64GB RDIMM (+%.1f%% of module cost; %.1f%% of a $%.0f contract "
          "module)." % (us["total"] - asia["total"], 100 * (us["total"] / asia["total"] - 1),
                        100 * (us["total"] - asia["total"]) / mk["rdimm_module"], mk["rdimm_module"]))

    section("6. MARKET PRICE DECKS ($/GB)  -- glut = A-05: -%.0f%% from 2026 peak (Q4-2026); severe = -%.0f%%"
            % (100 * mk["glut"], 100 * mk["severe"]))
    q2 = p["price_64gb_rdimm_contract_1q26_usd"] * (1 + p["contract_dram_qoq_2q26"]) * \
        (1 + p["contract_dram_qoq_3q26"]) * (1 + p["contract_dram_qoq_4q26f"])
    rows = [
        ["64GB RDIMM contract 4Q26 (model base) $/module", "%.0f" % mk["rdimm_module"],
         "Counterpoint 2Q26 ~$1,000 x TrendForce 3Q +15.5%, 4Q +12.5% [ESTIMATE]"],
        ["  cross-check: Citi 4Q26F $/module", "%.0f" % p["price_64gb_rdimm_contract_4q26f_usd"], "[UNVERIFIED]"],
        ["  cross-check: 1Q26 $900 x TrendForce 2Q-4Q $/module", "%.0f" % q2, "[ESTIMATE] upper bound"],
        ["DDR5 component contract 4Q26, $/raw GB", f2(mk["ddr5"]["today"]),
         "(RDIMM - $%.1f non-DRAM)/80 GB raw" % mk["rdimm_nondram"]],
        ["  cross-check: p1-cost derived 16Gb chip $%.1f -> $/GB" % p["price_ddr5_16gb_contract_4q26_derived_usd"],
         f2(p["price_ddr5_16gb_contract_4q26_derived_usd"] / 2), "cost_inputs.json"],
        ["DDR5 component, GLUT (A-05)", f2(mk["ddr5"]["glut"]), "x (1 - %.2f)" % mk["glut"]],
        ["DDR5 component, severe glut", f2(mk["ddr5"]["severe"]), "x (1 - %.2f)" % mk["severe"]],
        ["DDR5 16Gb 2023 trough (spot)", f2(mk["ddr5"]["trough"]), "[UNVERIFIED-PK] $3.2/chip"],
        ["64GB RDIMM 4Q26 contract, $/user GB", f2(mk["rdimm"]["today"]), ""],
        ["64GB RDIMM GLUT, $/user GB", f2(mk["rdimm"]["glut"]), ""],
        ["64GB RDIMM at 2023 trough chip price, $/user GB", f2(mk["rdimm"]["trough"]), "[ESTIMATE] derived"],
        ["32GB UDIMM contract-equivalent 4Q26, $/GB", f2(mk["udimm"]["today"]), "chip contract + client BOM"],
        ["Legacy DDR4/DDR3 contract 4Q26, $/GB", f2(mk["LEGACY"]["today"]),
         "DDR5 x %.2f [ESTIMATE]" % p["legacy_contract_vs_ddr5_ratio"]],
        ["DDR4 8Gb contract, Sep-2023 trough, $/GB", f2(mk["LEGACY"]["trough"]), "KED Global [REPORTED]"],
        ["HBM3E 2026 contract / HBM4 2027F, $/GB", "%s / %s" % (f2(mk["HBM"]["today"]),
                                                              f2(p["price_hbm4_usd_per_gb_2027f"])), "[REPORTED]"],
        ["Reference: DDR5 16Gb spot 2026-08-31, $/GB", f2(p["price_ddr5_16gb_spot_2026_08_31_usd"] / 2),
         "DRAMeXchange via BuySellRAM [REPORTED]"],
        ["Reference: DDR4 8Gb spot 2026-08-31 / DDR3 spot Jul-26", "%s / %s" % (
            f2(p["price_ddr4_8gb_spot_2026_08_31_usd"]), f2(p["price_ddr3_4gb_spot_2026_07_usd_per_gb"])),
         "[REPORTED]"],
        ["Reference: DDR5 retail Sep-26 / 32GB kit $450", "%s / %s" % (
            f2(p["price_ddr5_retail_usd_per_gb_2026_09"]), f2(p["price_ddr5_32gb_kit_retail_2026_usd"] / 32)),
         "rampricesusa / Digital Citizen [REPORTED]"],
    ]
    table(["price point", "$", "basis"], rows, ["l", "r", "l"])

    section("7. COST vs MARKET: implied gross margin (component level)")
    rows = []
    for c in CASES:
        x = cases[c["id"]]
        d = mk[c["fam"]]
        cost = x["component_gb"]
        rows.append([x["label"], f2(cost), f2(d["today"]), pct(gm(d["today"], cost)), f2(d["glut"]),
                     pct(gm(d["glut"], cost)), "%.1fx" % (d["glut"] / cost),
                     f2(d["trough"]), pct(gm(d["trough"], cost))])
    table(["case", "cost", "4Q26", "GM", "GLUT", "GM glut", "glut/cost", "2023", "GM 2023"], rows)
    print("Prices in $/GB. DDR5 cases use the DDR5 deck; DDR4/DDR3 use the legacy deck (4Q26 = DDR5 parity "
          "[ESTIMATE];\n2023 = DDR4 8Gb contract $1.30). HBM glut applies -60% only for illustration "
          "(HBM is sold on annual LTAs).\nNote: GM at 4Q26 also equals the price fall from 4Q26 needed to reach "
          "breakeven on full cost.")

    section("8. COST vs MARKET: modules ($/user GB)")
    rows = []
    for m in MODULES:
        x = mods[m["id"]]
        if m["kind"] == "rdimm":
            dk = mk["rdimm"]
        else:
            t = mk["udimm_fn"](m["user_gb"], mk["ddr5"]["today"])
            dk = dict(today=t, glut=t * (1 - mk["glut"]), trough=mk["udimm_fn"](m["user_gb"], mk["ddr5"]["trough"]))
        rows.append([x["label"], f2(x["per_gb"]), "%.0f" % x["total"], f2(dk["today"]), pct(gm(dk["today"], x["per_gb"])),
                     f2(dk["glut"]), pct(gm(dk["glut"], x["per_gb"])), f2(dk["trough"]),
                     pct(gm(dk["trough"], x["per_gb"]))])
    table(["module", "cost/GB", "cost $", "4Q26", "GM", "GLUT", "GM glut", "2023", "GM 2023"], rows)
    print("RDIMM prices: 64GB contract anchor per user GB (applied to the 96GB module too). UDIMM: contract-"
          "equivalent\n= DDR5 chip contract x GB + client BOM (no public PC-module contract series in inputs); "
          "U.S. retail Sep-26\nwas $%.2f-%.2f/GB." % (p["price_ddr5_32gb_kit_retail_2026_usd"] / 32,
                                                    p["price_ddr5_retail_usd_per_gb_2026_09"]))

    section("9. VALIDATION: model margin vs reported margins")
    p3 = mk["ddr5"]["today"] / (1 + p["contract_dram_qoq_4q26f"])
    table(["metric", "value"], [
        ["Model GM, DDR5 1-beta at 4Q26 contract", pct(gm(mk["ddr5"]["today"], ref["component_gb"]))],
        ["Model GM, DDR5 1-beta at 3Q26 contract (4Q26 / 1.125)", pct(gm(p3, ref["component_gb"]))],
        ["Micron FQ4-26 non-GAAP GM (all products) [REPORTED]", pct(p["gross_margin_micron_fq4_26_nongaap"])],
        ["Nanya 3Q26 GM (commodity DRAM) [REPORTED]", pct(p["gross_margin_nanya_3q26"])],
        ["SK hynix 3Q26 operating margin [REPORTED]", pct(p["op_margin_skhynix_3q26"])],
    ], ["l", "r"])
    print("Reported GMs include HBM, NAND (Micron), older nodes and period costs, so they should sit a few points "
          "below\na pure 1-beta DDR5 component GM. A model GM within ~5 pp is consistent.")

    section("10. SENSITIVITY: +/-%d%% on wafer cost, yield, die size (reference: DDR5 16Gb 1-beta)"
            % (100 * SENS_STEP))
    lo, hi = 1 - SENS_STEP, 1 + SENS_STEP
    c0 = CASE_BY_ID[REF_CASE]
    drivers = [("Wafer cost +/-20%", dict(wafer_mult=lo), dict(wafer_mult=hi)),
               ("Die yield +/-20%% (cap %.2f)" % YIELD_CAP, dict(yield_mult=lo), dict(yield_mult=hi)),
               ("Die size +/-20% (GDPW+yield)", dict(die_mult=lo), dict(die_mult=hi)),
               ("Back-end cost +/-20%", dict(backend_mult=lo), dict(backend_mult=hi))]
    bom, assy = module_nondram("rdimm", "asia", p)

    def rdimm_gb(comp):
        return (80 * comp + bom + assy) / p["module_assembly_yield"] / 64

    trows, grows, ggrows = [], [], []
    for lab, a, b in drivers:
        ca, cb = compute_case(c0, p, **a)["component_gb"], compute_case(c0, p, **b)["component_gb"]
        trows.append((lab, ca, cb))
        grows.append((lab, gm(mk["ddr5"]["today"], ca), gm(mk["ddr5"]["today"], cb)))
        ggrows.append((lab, gm(mk["ddr5"]["glut"], ca), gm(mk["ddr5"]["glut"], cb)))
    print("(a) Component cost, $/GB (base %.3f). '-' and '+' refer to the driver moving -20%% / +20%%." %
          ref["component_gb"])
    tornado(trows, ref["component_gb"], fmt=lambda v: "%.3f" % v)
    print("\n(b) 64GB RDIMM cost, $/user GB (base %.3f)" % rdimm_gb(ref["component_gb"]))
    tornado([(l, rdimm_gb(a), rdimm_gb(b)) for l, a, b in trows], rdimm_gb(ref["component_gb"]),
            fmt=lambda v: "%.3f" % v)
    pr = mk["ddr5"]["today"]
    grows.append(("4Q26 contract price +/-20%", gm(pr * lo, ref["component_gb"]), gm(pr * hi, ref["component_gb"])))
    pg = mk["ddr5"]["glut"]
    ggrows.append(("Glut price +/-20%", gm(pg * lo, ref["component_gb"]), gm(pg * hi, ref["component_gb"])))
    print("\n(c) Implied GM at 4Q26 contract (base %s)" % pct(gm(pr, ref["component_gb"])))
    tornado(grows, gm(pr, ref["component_gb"]), fmt=pct)
    print("\n(d) Implied GM in the A-05 GLUT (base %s)" % pct(gm(pg, ref["component_gb"])))
    tornado(ggrows, gm(pg, ref["component_gb"]), fmt=pct)

    print("\n(e) Input low/high ranges from cost_inputs.json, DDR5 16Gb 1-beta component $/GB")
    rng = [("Wafer cost 1-beta ($3.2k-5.5k)", {"wafer_cost_1beta_usd": None}),
           ("Die size 16Gb 1-beta (36.4-48.5 mm2)", {"die_ddr5_16gb_1beta_mm2": None}),
           ("Mature die yield (0.95-0.85)", {"dram_die_yield_mature": "rev"}),
           ("Back-end per die (probe+pkg+test)", {"probe_sort_cost_per_die_usd": None,
                                                  "fbga_assembly_cost_per_die_usd": None,
                                                  "final_test_burnin_cost_per_die_usd": None}),
           ("Edge exclusion (2-5 mm)", {"edge_exclusion_mm": None}),
           ("Scribe lane (60-200 um)", {"scribe_lane_mm": None}),
           ("Final-test yield (0.995-0.97)", {"final_test_yield": "rev"})]
    rrows, all_lo, all_hi = [], dict(p), dict(p)
    for lab, keys in rng:
        pl, ph = dict(p), dict(p)
        for k, mode in keys.items():
            good_end, bad_end = ("high", "low") if mode == "rev" else ("low", "high")
            pl[k] = all_lo[k] = INPUTS[k][good_end]
            ph[k] = all_hi[k] = INPUTS[k][bad_end]
        rrows.append((lab, compute_case(c0, pl)["component_gb"], compute_case(c0, ph)["component_gb"]))
    tornado(rrows, ref["component_gb"], fmt=lambda v: "%.3f" % v)
    print("All-favourable / all-unfavourable combined: $%.2f / $%.2f per GB (base $%.2f)."
          % (compute_case(c0, all_lo)["component_gb"], compute_case(c0, all_hi)["component_gb"],
             ref["component_gb"]))

    print("\n(f) +/-20% by case: component $/GB at driver -20% / +20%")
    rows = []
    for c in CASES:
        b = cases[c["id"]]["component_gb"]
        cells = [c["label"], f2(b)]
        for kw in ("wafer_mult", "yield_mult", "die_mult"):
            cells.append("%s / %s" % (f2(compute_case(c, p, **{kw: lo})["component_gb"]),
                                      f2(compute_case(c, p, **{kw: hi})["component_gb"])))
        rows.append(cells)
    table(["case", "base", "wafer -/+", "yield -/+", "die -/+"], rows)

    section("11. REFERENCE VALUES  (from dram_cost_stack import ddr5_reference)")
    table(["key", "value"], [[k, v] for k, v in ddr5_reference().items()], ["l", "r"])
    return r


def interpretation(r):
    p, c, mods, mk = r["p"], r["cases"], r["modules"], r["market"]
    ref = c[REF_CASE]["component_gb"]
    rd = mods["rdimm64_16g_1b"]
    g = lambda price, cost: 100 * gm(price, cost)
    hb = c["hbm3e_12h"]
    new4, dep4 = c["ddr4_8g_1x_new"]["component_gb"], c["ddr4_16g_1y_dep"]["component_gb"]
    cash = c["ddr5_16g_1b_cash"]["component_gb"]
    c0, lo, hi = CASE_BY_ID[REF_CASE], 1 - SENS_STEP, 1 + SENS_STEP
    sens = []
    for name, kw in (("die size", "die_mult"), ("wafer cost", "wafer_mult"), ("die yield", "yield_mult")):
        a, b = compute_case(c0, p, **{kw: lo})["component_gb"], compute_case(c0, p, **{kw: hi})["component_gb"]
        sens.append((abs(b - a), name, a, b))
    sens.sort(reverse=True)
    sens_txt = "; ".join("%s $%.2f to $%.2f" % (n, min(a, b), max(a, b)) for _, n, a, b in sens)
    gms = [gm(mk["ddr5"]["today"], v) for _, _, a, b in sens for v in (a, b)]
    gmg = [gm(mk["ddr5"]["glut"], v) for _, _, a, b in sens for v in (a, b)]
    return f"""## Interpretation (p1-model, {AS_OF})

All numbers below come from `models/dram_cost_stack.py` and are **[ESTIMATE]**. The inputs come from `research/phase1/cost_inputs.json` (agent p1-cost). This agent could not reach the web: the WebSearch budget was spent, and trendforce.com, eetasia.com and buysellram.com failed DNS on {AS_OF}. Every market price is therefore **[REPORTED]** through other agents' search snippets, or **[UNVERIFIED]**.

1. **Making DDR5 costs about ${ref:.2f}/GB at the component level** (16Gb, 1-beta, mature yield, fully loaded wafer of ${p['wafer_cost_1beta_usd']:,.0f}).
   - 1-gamma costs ${c['ddr5_16g_1c_ramp']['component_gb']:.2f}/GB during its 2026 ramp and ${c['ddr5_16g_1c']['component_gb']:.2f}/GB once mature.
   - Cash cost alone, the glut floor, is ${cash:.2f}/GB.
   - A 64GB RDIMM costs **${rd['total']:.0f}, or ${rd['per_gb']:.2f} per user-GB**.
   - Front-end silicon is {100 * c[REF_CASE]['wafer_gb'] / ref:.0f}% of component cost. Non-DRAM module parts plus assembly are ${rd['bom'] + rd['assy']:.0f} per RDIMM.
2. **Contract price today (Q4-2026) is about ${mk['ddr5']['today']:.2f}/GB at the component level and ${mk['rdimm']['today']:.2f} per user-GB on a 64GB RDIMM** (${mk['rdimm_module']:,.0f} per module).
   - Implied gross margin is **{g(mk['ddr5']['today'], ref):.0f}%** for components and {g(mk['rdimm']['today'], rd['per_gb']):.0f}% for the RDIMM.
   - That agrees with the reported Micron (~87%) and Nanya (85.7%) gross margins, which is the main check that the cost stack is roughly right.
3. **In the A-05 glut (−60% from the 2026 peak), DDR5 sells for ${mk['ddr5']['glut']:.2f}/GB** (${mk['rdimm']['glut']:.2f} per user-GB on an RDIMM).
   - That price is still **{mk['ddr5']['glut'] / ref:.1f}× full cost**, so incumbent gross margin stays at about **{g(mk['ddr5']['glut'], ref):.0f}%**.
   - Prices would have to fall **{100 * (1 - ref / mk['ddr5']['today']):.0f}%** before 1-beta full cost bites, and **{100 * (1 - cash / mk['ddr5']['today']):.0f}%** before cash cost does.
   - **A 60% glut hurts high-cost entrants, not incumbents.** A concept whose $/GB is above about ${mk['ddr5']['glut']:.0f} loses its price umbrella.
4. **At the 2023 trough (DDR5 about ${mk['ddr5']['trough']:.2f}/GB; DDR4 $1.30/GB), 1-beta DDR5 runs at {g(mk['ddr5']['trough'], ref):.0f}% gross margin on full cost and is cash-positive only at {g(mk['ddr5']['trough'], cash):.0f}%.** That is consistent with SK hynix's −67% operating margin in 1Q23.
5. **HBM3E 12-high costs about ${hb['component_gb']:.2f}/GB** ({hb['component_gb'] / ref:.1f}× DDR5).
   - The model's wafer trade ratio is {c[REF_CASE]['gb_per_wafer'] / hb['gb_per_wafer']:.1f}:1, against Micron's reported ~3:1.
   - At a 2026 price of $12/GB the margin is about **{g(12.0, hb['component_gb']):.0f}%**, below DDR5. HBM4 at about $36/GB in 2027 restores the premium.
6. **Legacy and trailing-node DRAM:**
   - DDR4 16Gb on a depreciated 1y line costs ${dep4:.2f}/GB.
   - DDR4 8Gb on a *new* U.S.-style 1x line costs **${new4:.2f}/GB**. That is profitable today and in the glut if DDR4 holds parity with DDR5, but at the 2023 trough of $1.30 it runs at **{g(1.30, new4):.0f}% gross margin**.
   - **A new U.S. legacy line is a shortage-only business.**
7. **Sensitivity:**
   - At ±20%, the 1-beta cost drivers rank as: {sens_txt} per GB. Die size ranks first because it moves both GDPW and the negative-binomial yield.
   - Using the input low/high ranges instead, wafer cost ($3.2–5.5k) dominates (section 10e).
   - Margin barely moves: across all ±20% cost cases, GM stays within {100 * min(gms):.0f}–{100 * max(gms):.0f}% at the Q4-2026 price and {100 * min(gmg):.0f}–{100 * max(gmg):.0f}% in the glut. **Margin is set by price, not cost.**
8. **The weakest inputs:**
   - **Die sizes** for 1-beta and 1-gamma 16/24/32Gb are ESTIMATEs from density; the only teardown anchor is CXMT/Micron 1z.
   - **Fully loaded wafer cost** rests on UNVERIFIED capex-per-wpm rules of thumb.
   - **The Q4-2026 contract level** is not public at chip level. It is anchored on Counterpoint's 1Q/2Q26 RDIMM figures compounded with TrendForce QoQ forecasts, and the Citi $1,586 figure is UNVERIFIED.
   - **The 2023 DDR5 trough** ($3.2/chip) is UNVERIFIED prior knowledge.
   - **The DDR4 4Q26 contract** is assumed at DDR5 parity.
   - **HBM core die size and stack yield** are UNVERIFIED.
"""


def main():
    buf = io.StringIO()
    with redirect_stdout(buf):
        r = report()
    text = buf.getvalue()
    sys.stdout.write(text)
    md = ("# DRAM cost stack: model output\n\n"
          "**Generated by:** `models/dram_cost_stack.py` (agent `p1-model`) · **As of:** %s · "
          "**Inputs:** `research/phase1/cost_inputs.json` (p1-cost) with fallbacks · "
          "**Narrative:** `research/phase1/cost_stack.md` · **Re-run:** `python3 models/dram_cost_stack.py`\n\n"
          "```text\n%s```\n\n%s" % (AS_OF, text, interpretation(r)))
    try:
        OUT_MD.parent.mkdir(parents=True, exist_ok=True)
        OUT_MD.write_text(md, encoding="utf-8")
        print("\nWrote %s" % OUT_MD.relative_to(RV))
    except OSError as exc:
        print("\nWARNING: could not write %s (%s)" % (OUT_MD, exc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
