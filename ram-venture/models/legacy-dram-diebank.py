#!/usr/bin/env python3
"""
DD7 - Authorized-Aftermarket Legacy DRAM Die Bank (+ hi-rel MCMs)
Anchor C-91 (title-taking authorized-aftermarket die bank), folded C-65 (hi-rel x72 ECC DDR4 MCM).
Agent: p4-legacy-dram-diebank. As of 2026-11-01. Pure Python 3 stdlib.

Run from the ram-venture root:   python3 models/legacy-dram-diebank.py

Three plans are modelled, each under BASE / GLUT (DDR5 -60% from 2028-Q1) / SEVERE ($2.04/GB):

  Plan A  "Bootstrap wedge" (T0, founder's $40k, no outside money):
          L1 managed die-bank programs (consignment vault at a Micross-type site; the OEM owns the die)
          L2 channel (rep) commissions on a long-lifecycle DRAM OCM's parts
  Plan B  "Staged moonshot" (T2, gated outside capital, explicit):
          Plan A lines + Stage-1 $1.5M at m18 -> quality system + title-taking bank #1 (L3)
                       + Stage-2 $4.0M at m30 -> hi-rel x72 ECC DDR4 MCM (L4) drawing die from the bank
          Simulated for 120 months: the 36-month P&L is the first 36 rows; the 10-year view is the moonshot ceiling.
  Plan C  "Buy a small licensed aftermarket manufacturer / test house" (acquisition arithmetic only)

Every INPUT carries a source URL or "ESTIMATE: basis". Sources: research/sources/p4-legacy-dram-diebank.jsonl.
Assumptions: research/assumptions/p4-legacy-dram-diebank.md. Notes: research/phase4/legacy-dram-diebank_notes.md.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ----------------------------------------------------------------------------------------------
# 0. Canonical DDR reference (import; fall back to the canonical numbers if the import fails)
# ----------------------------------------------------------------------------------------------
_CANON = dict(contract_component_usd_per_gb_q4_2026=20.37, glut_component_usd_per_gb=8.15,
              severe_glut_component_usd_per_gb=2.04, contract_rdimm64_usd_per_user_gb_q4_2026=25.8,
              glut_rdimm64_usd_per_user_gb=10.3, cost_component_usd_per_gb=1.48,
              trough_2023_ddr4_usd_per_gb=1.30, ddr4_depreciated_cost_usd_per_gb=1.284)
try:
    from dram_cost_stack import ddr5_reference  # noqa: E402
    REF = ddr5_reference()
    REF_SRC = "models/dram_cost_stack.py ddr5_reference() (imported)"
except Exception as exc:  # pragma: no cover - fallback path
    REF = dict(_CANON)
    REF_SRC = "canonical fallback (import failed: %s)" % exc

P0 = REF["contract_component_usd_per_gb_q4_2026"]
P_GLUT = REF["glut_component_usd_per_gb"]
P_SEVERE = REF["severe_glut_component_usd_per_gb"]

# ----------------------------------------------------------------------------------------------
# 1. INPUTS  (name: (value, source))
# ----------------------------------------------------------------------------------------------
INPUTS = {
    # --- timeline & market ---
    "start_month_label": ("2026-11", "Task spec: as of 2026-11-01; m1 = 2026-11"),
    "glut_start_month": (15, "ASSUMPTIONS A-05: glut from 2028-Q1 = m15"),
    "p0_legacy_usd_gb": (P0, REF_SRC + ": Q4-2026 contract; legacy DDR4 at parity per 01_LANDSCAPE.md 10.4 #4"),
    "p_glut_usd_gb": (P_GLUT, REF_SRC + ": glut deck (-60%)"),
    "p_severe_usd_gb": (P_SEVERE, REF_SRC + ": severe deck ($2.04)"),
    "base_decline": (0.35, "ESTIMATE: legacy -35% m15->m26 in BASE; DDR4 collapses first (01_LANDSCAPE 3.3); BofA -10% blended ASP 2028 (01_LANDSCAPE 1 row 4b) is the floor"),
    "base_decline_end_month": (26, "ESTIMATE: decline spread over 2028 (house call: turn 2028)"),
    "glut_ramp_end_month": (17, "ESTIMATE: glut reached in two quarters (2018-19 analog: -62.5% in ~4 quarters, 01_LANDSCAPE 1 row 4a)"),
    "severe_ramp_end_month": (20, "ESTIMATE: severe trough reached in ~6 quarters"),
    "long_run_usd_gb": (3.00, "ESTIMATE: ~2.3x 2023 DDR4 trough $%.2f and depreciated DDR4 cost $%.3f/GB (models/dram_cost_stack.py) = ~57%% cycle-average maker GM" % (REF["trough_2023_ddr4_usd_per_gb"], REF["ddr4_depreciated_cost_usd_per_gb"])),
    "long_run_reached_month": (60, "ESTIMATE: price normalises over 2030-31"),
    "demand_mult": ({"BASE": 1.0, "GLUT": 0.75, "SEVERE": 0.60}, "ESTIMATE: fewer LTBs when supply is abundant, partly offset by more EOL notices (Z2Data 2026 https://www.z2data.com/insights/how-chip-obsolescence-is-making-dmsms-worseand-where-we-re-headed-in-2027)"),
    "base_demand_mult_after_m27": (0.90, "ESTIMATE: shortage pain fades in BASE as prices fall"),
    # --- founder ---
    "founder_cash": (40000.0, "ASSUMPTIONS A-03: $40k deployable"),
    "hours_pt": (65.0, "ASSUMPTIONS A-03: ~15 h/week"),
    "hours_ft": (170.0, "ESTIMATE: full-time month"),
    "ops_hire_hours": (80.0, "ESTIMATE: quality/ops manager absorbs ~half of program service after Stage-1"),
    "ft_salary_loaded": (11000.0, "ESTIMATE: $10k/month salary + 10% burden (round-1 convention)"),
    "ft_trigger_contrib": (10000.0, "ESTIMATE: trailing-3-month contribution must replace salary"),
    "ft_trigger_cash": (30000.0, "ESTIMATE: cash floor before quitting the day job"),
    "tax_rate": (0.30, "ESTIMATE: pass-through federal+state+SE; red team RT-VC-DD1-07"),
    # --- L1 managed die-bank program (consignment; OEM owns die) ---
    "conv_pt": (4.0, "ESTIMATE: 15 h/month prospecting at ~4 h per qualified DMSMS/OEM conversation"),
    "ft_mult": (2.5, "ESTIMATE: 37.5 h/month prospecting full-time"),
    "ramp_months": (6, "ESTIMATE: credibility ramp; m1 is spent on the kill experiment, full funnel from m6"),
    "prospect_hours_pt": (15.0, "ESTIMATE: see conv_pt"),
    "p_study": (0.10, "ESTIMATE: below DD2's attacked 12% trial conversion (RT-VC-DD2-06)"),
    "p_program": (0.35, "ESTIMATE: study -> managed program; Micross sells the vault direct (https://www.micross.com/sustainment-solutions/program-sustainment-management/long-term-die-and-wafer-storage)"),
    "study_price": (4000.0, "ESTIMATE: DD2 priced LTB studies at $3,500 (04_DEEPDIVES/lifecycle-intel) plus program setup"),
    "study_cost": (300.0, "ESTIMATE: paid part/lifecycle data per study"),
    "study_hours": (10.0, "ESTIMATE"),
    "program_fee": (750.0, "ESTIMATE: below an OEM buyer's in-house time; SiliconExpert software alone is $250/month (DD2)"),
    "program_direct_cost": (60.0, "ESTIMATE: documentation, shipping coordination, insurance rider"),
    "program_hours": (2.0, "ESTIMATE"),
    "program_churn": (0.01, "ESTIMATE: programs run for the bank's life; OEM may internalise or deal direct with Micross"),
    "agency_fee_pct": (0.04, "ESTIMATE: procurement agency fee on LTB die value"),
    "ltb_die_per_program": (4000.0, "ESTIMATE: life-of-need buy for one part family at a mid-size OEM"),
    "gb_per_die_l1": (0.75, "ESTIMATE: blend of DDR3 4Gb (0.5 GB) and DDR4 8Gb (1 GB)"),
    "kgd_factor": (0.85, "ESTIMATE: KGD price / packaged $/GB; no quote (ESMT KGD at Suntsu is RFQ-only, https://suntsu.com/product/integrated-circuits/memory/kgd-256mbx16-ddr4-1-2v/)"),
    "pull_units_per_program": (80.0, "ESTIMATE: 4,000 die drawn over ~4 years"),
    "pull_margin_unit": (1.00, "ESTIMATE: ~10% coordination margin on ~$10 OSAT package+test"),
    # --- L2 channel commissions ---
    "rep_start_month": (9, "ESTIMATE: Intelligent Memory signed Sourceability/Flip in 2026 (https://evertiq.com/design/2026-10-06-intelligent-memory-signs-sourceability-as-global-distributor); a new U.S. rep needs ~6-9 months"),
    "acct_rate_pt": (0.30, "ESTIMATE: new rep accounts/month part-time"),
    "acct_purchase_yr": (40000.0, "ESTIMATE: long-lifecycle DRAM bought per mid-size OEM account at 2026 prices; scales with legacy price"),
    "commission": (0.05, "ESTIMATE: typical component rep commission; unsourced"),
    "acct_churn": (0.015, "ESTIMATE"),
    "acct_hours": (0.5, "ESTIMATE"),
    # --- part-time fixed costs ---
    "fixed_pt": (680.0, "ESTIMATE: CRM/Sales Navigator ~$100, E&O ~$110 (Insureon via sources/p5r-memory-efficiency.jsonl), accounting $100, web $20, travel accrual $350"),
    "conference_cost": (2500.0, "ESTIMATE: one DMSMS-conference trip per year"),
    "conference_months": ([10, 22, 34, 46, 58, 70, 82, 94, 106, 118], "ESTIMATE: annual; real conference dates not checked"),
    "oneoff_m1": (8500.0, "ESTIMATE: kill experiment $6,000 + LLC and rep-agreement legal $2,500"),
    # --- Plan B capital & staff ---
    "raise1_month": (18, "ESTIMATE: gate = OCM letter + >=3 locked-die LOIs by m15, close by m18"),
    "raise1_amt": (1500000.0, "ESTIMATE: seed for quality system + bank #1; no investor conversation"),
    "raise2_month": (30, "ESTIMATE: gate = >=1 MCM evaluation LOI"),
    "raise2_amt": (4000000.0, "ESTIMATE: MCM NRE + team (C-65 card: $2-4M before revenue)"),
    "cash_reserve": (50000.0, "ESTIMATE: bridge equity injected below this (Plan B only); reported as extra external capital"),
    "qa_mgr": (11000.0, "ESTIMATE: quality/ops manager loaded, m19+ (AS9120B/AS6081/AS6496 programme)"),
    "test_contractor": (6000.0, "ESTIMATE: memory test engineering contractor m19-m30"),
    "mcm_engineers": (36000.0, "ESTIMATE: 2 package/SI engineers loaded, m30+"),
    "bd_hire": (16000.0, "ESTIMATE: defense BD loaded, m31+"),
    "ops_tech": (8000.0, "ESTIMATE: ops tech for bank pulls, m38+"),
    "scale_hires_m60": (30000.0, "ESTIMATE: second BD + production/quality engineer, m60+"),
    "overhead_b": (4000.0, "ESTIMATE: office, software, legal, accounting from m18"),
    "insurance_b": (1500.0, "ESTIMATE: product liability/aerospace cover from m20"),
    "itar_month": (250.0, "ESTIMATE: DDTC registration ~$3k/yr (prior knowledge, not verified this session) from m30"),
    "as9120_cert": (35000.0, "ESTIMATE: AS9120B certification spread m21-m25"),
    "as9120_surv_yr": (8000.0, "ESTIMATE: surveillance audits from m33"),
    # --- L3 title-taking bank ---
    "bank_months": ([20, 44, 68], "ESTIMATE: bank #1 two months after Stage-1, then every two years"),
    "bank_wafers": (10, "ESTIMATE: 10 x 300mm wafers per bank (C-91 card used ~$600k for ~30 wafers)"),
    "good_die_per_wafer": (1251, "ESTIMATE (research/phase1/us_backend.md 4.2): DDR4 8Gb 45 mm2, 85% yield, ~1,251 good die/300mm wafer"),
    "gb_per_die_bank": (1.0, "Definition: JEDEC DDR4 8Gb die = 1 GB"),
    "wafer_factor": (0.75, "ESTIMATE: wafer-level die price / packaged $/GB (wafer < KGD < packaged); no OCM quote"),
    "bank_nre_first": (120000.0, "ESTIMATE: FBGA package qual + memory-ATE test program + JEDEC qual lot at a U.S. OSAT; QP Technologies publishes no pricing (https://anysilicon.com/vendors/qp-technologies/)"),
    "bank_nre_next": (40000.0, "ESTIMATE: same package family, new die revision"),
    "storage_pct_yr": (0.03, "ESTIMATE: Micross carrying-fee model, no rates published (https://www.micross.com/sustainment-solutions/program-sustainment-management/long-term-die-and-wafer-storage); E-07 used 1.5%"),
    "storage_min_yr": (5000.0, "ESTIMATE: minimum vault fee per bank"),
    "reprobe_unit": (1.50, "ESTIMATE: wafer re-probe of aged die at pull (GEIA-STD-0003B LTS practice, https://saemobilus.sae.org/standards/geiastd0003b-long-term-storage-lts-electronic-devices)"),
    "pack_unit": (6.00, "ESTIMATE: U.S. low-volume FBGA assembly; Asian volume <$1; no quote"),
    "test_unit": (4.00, "ESTIMATE: at-speed DDR4 test at a U.S. test house; no quote"),
    "pull_yield": (0.95, "ESTIMATE: aged-die pull yield; Rochester found packaged parts functional after up to 17 years (https://www.digikey.com/en/blog/testing-confirms-that-component-reliability-remains-with-proper-long-term-storage)"),
    "aftermarket_mult": (2.5, "ESTIMATE: centre-low of the 1.5-5x authorized-aftermarket range (research/phase1/us_backend.md 5.3, itself an estimate); JEDEC DRAM is substitutable (DSPO 2024 case mix)"),
    "mult_compress": ({"BASE": 1.0, "GLUT": 0.9, "SEVERE": 0.8}, "ESTIMATE: broker market and cheap substitutes cap aftermarket pricing in a glut"),
    "sell_lag_months": (18, "ESTIMATE: banked die sell only after OCM and distributor stock runs out (C-91 card: years 3-8)"),
    "sell_rate_yr": ({"BASE": 0.15, "GLUT": 0.11, "SEVERE": 0.08}, "ESTIMATE: E-07 base 15%/yr (research/phase2/E_notes.md 5); substitutes shrink the locked-buyer pool in a glut"),
    "bank_min_gm": (0.20, "ESTIMATE: rational-operator rule; a bank is bought only if projected unit GM at purchase >= 20%"),
    "locked_floor_unit": (0.0, "ESTIMATE: price floor per part from locked buyers' requalification avoidance; OFF in all scenarios (no evidence); shown as a what-if"),
    # --- L4 hi-rel MCM ---
    "mcm_nre_total": (1400000.0, "ESTIMATE: substrate+SI/PI+package tooling+test program+MIL-STD-883-style qual+SEL/TID test; C-65 card $2-4M incl. staff"),
    "mcm_nre_months": (18, "ESTIMATE (C-65 card): SI/PI 6-9 months + qualification 6-12 months"),
    "mcm_eval_units": (100, "ESTIMATE: evaluation lot"),
    "mcm_eval_price": (1200.0, "ESTIMATE"),
    "mcm_designin_start_lag": (30, "ESTIMATE: first production design-in 30 months after Stage-2 (C-65 card 30-42 months to first revenue)"),
    "mcm_designins_yr": (2.0, "ESTIMATE: design-ins per year for a no-heritage entrant"),
    "mcm_designin_mult": ({"BASE": 1.0, "GLUT": 0.85, "SEVERE": 0.70}, "ESTIMATE: cost-sensitive NewSpace end reverts to upscreened COTS DDR4 in a glut (founder_3/veteran_3 scores)"),
    "mcm_units_yr_per_designin": (300.0, "ESTIMATE: NewSpace/rugged program volume; Mercury's $8.2M memory order (https://intelligencecommunitynews.com/mercury-systems-receives-8-2m-order-for-swap-optimized-memory-for-c2i-application/) shows larger programs exist"),
    "mcm_program_life_months": (96, "ESTIMATE: 8-year production life"),
    "mcm_attrition": (0.005, "ESTIMATE: monthly program cancellation/attrition"),
    "mcm_asp": (900.0, "ESTIMATE: entrant at the low end of the C-65 card's $800-3,000; no public price (Avnet lists Teledyne DDR4T as RFQ, https://www.avnet.com/americas/manufacturers/m/c/teledyne-e2v/memory)"),
    "mcm_die_per_unit": (9, "Design fact (C-65 card): 9 x 8Gb x8 KGD for an 8GB x72 ECC part"),
    "mcm_substrate": (60.0, "ESTIMATE"),
    "mcm_assembly": (80.0, "ESTIMATE: U.S. hi-rel OSAT"),
    "mcm_screen": (150.0, "ESTIMATE: burn-in + temperature screening + at-speed test (Mercury datasheet: 100% burn-in, https://www.mrcy.com/siteassets/product-datasheets/ddr/high-density-secure-memory-16gb-ddr4-builtsecure.pdf)"),
    "mcm_yield": (0.91, "ESTIMATE (veteran_3 score, research/phase3/scores_raw/veteran_3.json): 99% KGD -> ~91% module"),
    "var_opex_hw_pct": (0.20, "ESTIMATE: variable opex on bank+MCM revenue: defense reps ~5-7%, warranty/RMA ~2%, production/quality/logistics scaling ~10%"),
    "ev_rev_multiple": (1.5, "ESTIMATE: sub-scale hi-rel component business; no transaction multiple found"),
    # --- Plan C acquisition ---
    "acq_staff": (30, "Resurgent ~30 employees (https://www.businesswire.com/news/home/20230221005100/en)"),
    "acq_rev_per_emp": (200000.0, "ESTIMATE: small specialty electronics manufacturer"),
    "acq_ebitda_margin": ({"BASE": 0.15, "GLUT": 0.10, "SEVERE": 0.06}, "ESTIMATE"),
    "acq_multiple": (5.0, "ESTIMATE: EBITDA multiple for a sub-$1M-EBITDA niche manufacturer"),
    "sba_share": (0.80, "ESTIMATE: SBA 7(a) structure; program cap $5M (prior knowledge, not verified this session)"),
    "sba_rate": (0.105, "ESTIMATE: prime + spread"),
    "sba_years": (10, "ESTIMATE: 7(a) business-acquisition term"),
    "seller_note_share": (0.10, "ESTIMATE"),
    "equity_share": (0.10, "ESTIMATE: equity injection"),
    # --- inputs added in Phase 5 (neutral Phase 4 values here; revised below) ---
    "l1_enabled": (1.0, "Phase 4: L1 managed die-bank programs on"),
    "burnin_hotcold_unit": (0.0, "Phase 4: no burn-in or hot/cold insertion in the L3 pull stack"),
    "surveillance_yr": (0.0, "Phase 4: no periodic sample-assembly surveillance of stored lots"),
    "pull_whole_wafer": (False, "Phase 4: pull cost booked per die sold"),
    "pull_cap_to_ltb": (False, "Phase 4: program_unit bills pulls for the whole program life"),
    "mcm_lot_requal_yr": (0.0, "Phase 4: radiation/temperature data treated as one-time NRE"),
    "planA_extra_oneoff": ({}, "variant hook: {month: $} extra Plan A one-off costs (0 in BASE)"),
    "planA_extra_month": (0.0, "variant hook: extra Plan A monthly fixed cost (0 in BASE)"),
    "planA_extra_start": (1, "variant hook: first month of planA_extra_month"),
}

# ----------------------------------------------------------------------------------------------
# RED-TEAM REVISIONS (Phase 5) -- owner p5r-legacy-dram-diebank, 2026-11-01
# Objections: research/phase5/rt2_{VET,VC,HYP,PHY}.json (dd = DD7); responses:
# research/phase5/responses_legacy-dram-diebank.json. INPUTS_P4 keeps the Phase 4 inputs so model
# section 10 reproduces the Phase 4 output exactly; every line below is old -> new, objection id.
# ----------------------------------------------------------------------------------------------
INPUTS_P4 = copy.deepcopy(INPUTS)
RT_REVISIONS = {
    # L1 killed (three FATALs): banking bare die costs a board OEM 3-5x the die it saves (model section 10a);
    # board OEMs qualify packaged part numbers, and Micross sells the whole bundle direct (EDSP).
    "l1_enabled": (0.0, "1 -> 0; RT-HYP-DD7-01, RT-VC-DD7-01, RT-VET-DD7-01 (L1 KILLED); RT-VC-DD7-02, RT-VET-DD7-02"),
    "p_program": (0.10, "0.35 -> 0.10; RT-VC-DD7-02: Micross EDSP sells LTB procurement + N2 storage + pulls direct "
                        "(https://www.micross.com/products-and-services/eol-dmsms-sustainment/original-qualified-product/eol-die-sustainment-program-edsp); only used in what-ifs, L1 is off"),
    "pull_cap_to_ltb": (True, "False -> True; RT-VC-DD7-01: a 4,000-die program cannot bill 8,000 pulls (Phase 4 bug in program_unit)"),
    "oneoff_m1": (3900.0, "8,500 -> 3,900; kill test withdrawn (concept killed; RT-VC-DD7-03, RT-VET-DD7-07); "
                          "+$500 employment-agreement review (RT-HYP-DD7-06) + $900 rep-agreement review + $2,500 LLC/rep legal"),
    # L3 bank
    "burnin_hotcold_unit": (10.0, "0 -> 10 $/die; RT-VET-DD7-03: hot/cold at-speed insertions + burn-in, low end of $10-20 [ESTIMATE]"),
    "pull_yield": (0.90, "0.95 -> 0.90; RT-PHY-DD7-03: no published bondability/yield data for bare DRAM die after >=10 yr in N2"),
    "surveillance_yr": (5000.0, "0 -> 5,000 $/bank/yr; RT-PHY-DD7-03: annual sample assembly + test + bond pull/shear [ESTIMATE]"),
    "pull_whole_wafer": (True, "False -> True; RT-PHY-DD7-04: thinning/saw are whole-wafer steps, so a wafer is packaged when opened"),
    "aftermarket_mult": (2.0, "2.5 -> 2.0; RT-HYP-DD7-04: recovered hyperscaler DDR4 (2028-30) caps non-DFARS buyers near 1.5x; "
                              "50/50 blend with 2.5x DFARS-bound buyers [ESTIMATE]"),
    "good_die_per_wafer": (736, "1,251 -> 736; RT-PHY-DD7-05: legacy-OCM 8Gb die ~75 mm2 (60-90 mm2 range), 300 mm, 85% yield [ESTIMATE]"),
    "bank_wafers": (17, "10 -> 17; RT-PHY-DD7-05: keeps the bank at ~12,500 die on the larger die"),
    # L4 MCM
    "mcm_substrate": (90.0, "60 -> 90; RT-PHY-DD7-01: nine 8Gb die (~405-675 mm2) do not fit 15x20 mm side by side; stacked/RDL build [ESTIMATE]"),
    "mcm_assembly": (160.0, "80 -> 160; RT-PHY-DD7-01: two-high stack, thinning, RDL/face-down window per die [ESTIMATE]"),
    "mcm_yield": (0.76, "0.91 -> 0.76; RT-VET-DD7-04 + RT-PHY-DD7-02: 3% per-die fallout at a 125 C screen/bin on unburned "
                        "distributor KGD, 0.97^9 = 0.76 [ESTIMATE]"),
    "mcm_nre_total": (1600000.0, "1.4M -> 1.6M; RT-VET-DD7-06: build at a QML-38534 line (audit, line qualification, "
                                 "competitor margin) [ESTIMATE]"),
    "mcm_lot_requal_yr": (75000.0, "0 -> 75,000 $/yr from first production; RT-VET-DD7-04: TID/SEL/hot-retention data repeated per "
                                   "die revision and wafer lot (no revision lock on distributor KGD) [ESTIMATE]"),
}
for _name, (_val, _why) in RT_REVISIONS.items():
    INPUTS[_name] = (_val, "RED-TEAM REVISION: " + _why)


def v(name):
    return INPUTS[name][0]


MONTHS_A = 36
MONTHS_B = 120
SCENS = ["BASE", "GLUT", "SEVERE"]


def mlabel(m):
    y, mo = 2026, 11 + (m - 1)
    y += (mo - 1) // 12
    mo = (mo - 1) % 12 + 1
    return "%04d-%02d" % (y, mo)


# ----------------------------------------------------------------------------------------------
# 2. Price path (legacy DDR4 packaged $/GB) and demand multiplier
# ----------------------------------------------------------------------------------------------
def legacy_price(m, scen, P=None):
    P = P or INPUTS
    p0 = P["p0_legacy_usd_gb"][0]
    gs = P["glut_start_month"][0]

    def p_at(mm):
        if mm < gs:
            return p0
        if scen == "BASE":
            end = P["base_decline_end_month"][0]
            tgt = p0 * (1 - P["base_decline"][0])
        elif scen == "GLUT":
            end, tgt = P["glut_ramp_end_month"][0], P["p_glut_usd_gb"][0]
        else:
            end, tgt = P["severe_ramp_end_month"][0], P["p_severe_usd_gb"][0]
        if mm >= end:
            return tgt
        f = (mm - gs + 1) / float(end - gs + 1)
        return p0 + (tgt - p0) * f

    if m <= 36:
        return p_at(m)
    p36 = p_at(36)
    lr, lrm = P["long_run_usd_gb"][0], P["long_run_reached_month"][0]
    if m >= lrm:
        return lr
    return p36 + (lr - p36) * (m - 36) / float(lrm - 36)


def demand_mult(m, scen, P=None):
    P = P or INPUTS
    if m < P["glut_start_month"][0]:
        return 1.0
    if scen == "BASE":
        return P["base_demand_mult_after_m27"][0] if m >= 27 else 1.0
    return P["demand_mult"][0][scen]


# ----------------------------------------------------------------------------------------------
# 3. Simulation
# ----------------------------------------------------------------------------------------------
def pull_cost(P=None):
    """Per-die pull cost before the die itself: re-probe + package + test (+ Phase 5 burn-in/hot-cold)."""
    P = P or INPUTS
    return (P["reprobe_unit"][0] + P["pack_unit"][0] + P["test_unit"][0] + P["burnin_hotcold_unit"][0])


def pull_charge(b, units_die, P=None):
    """Pull cost booked when `units_die` are drawn from bank b. Phase 4: per die drawn. Phase 5
    (pull_whole_wafer, RT-PHY-DD7-04): thinning and saw are whole-wafer steps, so each wafer is packaged
    when it is opened and the whole wafer's pull cost is booked then."""
    P = P or INPUTS
    if not P["pull_whole_wafer"][0]:
        return units_die * pull_cost(P)
    gdpw = P["good_die_per_wafer"][0]
    b["drawn"] = b.get("drawn", 0.0) + units_die
    cost = 0.0
    while b["drawn"] > b.get("opened", 0.0) + 1e-9 and b.get("opened", 0.0) < b["die0"]:
        n = min(gdpw, b["die0"] - b.get("opened", 0.0))
        b["opened"] = b.get("opened", 0.0) + n
        cost += n * pull_cost(P)
    return cost


def simulate(scen, plan="A", months=MONTHS_A, P=None):
    """Monthly simulation. plan 'A' = bootstrap wedge; 'B' = staged moonshot (gated raises)."""
    P = P or INPUTS
    g = lambda k: P[k][0]  # noqa: E731
    cash = g("founder_cash")
    ft = False
    programs = accounts = 0.0
    studies_prev = 0.0
    ar1 = 0.0          # services, 1-month lag
    ar2 = [0.0, 0.0]   # commissions + hardware, 2-month lag
    nol = 0.0          # loss carry-forward
    ext_capital = 0.0
    bridges = 0.0
    banks = []         # dicts: month, die0, die_left, basis_per_die, anchor_price
    skipped = []       # bank months skipped by the rational-operator rule
    mcm_cohorts = []   # (start_month, units_per_month)
    mcm_nre_left = 0.0
    contrib_hist = []
    rows = []
    for m in range(1, months + 1):
        price = legacy_price(m, scen, P)
        dm = demand_mult(m, scen, P)
        rev = dict(study=0.0, prog=0.0, agency=0.0, pull=0.0, comm=0.0, bank=0.0, mcm=0.0)
        cogs = 0.0
        opex = 0.0
        capex_inv = 0.0  # inventory purchases (cash, capitalised)
        equity_in = 0.0

        # ---- Plan B gated raises and full-time switch ----
        if plan == "B" and m == g("raise1_month"):
            equity_in += g("raise1_amt")
            ft = True
        if plan == "B" and m == g("raise2_month"):
            equity_in += g("raise2_amt")
            mcm_nre_left = g("mcm_nre_total")

        # ---- capacity ----
        hours = g("hours_ft") if ft else g("hours_pt")
        if plan == "B" and m > g("raise1_month"):
            hours += g("ops_hire_hours")
        prospect_h = g("prospect_hours_pt") * (g("ft_mult") if ft else 1.0)

        # ---- L1 managed die-bank programs ----
        ramp = min(1.0, m / float(g("ramp_months")))
        conv = g("conv_pt") * (g("ft_mult") if ft else 1.0) * dm * ramp * g("l1_enabled")  # Phase 5: L1 killed
        studies = conv * g("p_study")
        new_prog = studies_prev * g("p_program")
        studies_prev = studies
        programs = programs * (1 - g("program_churn")) + new_prog
        # ---- L2 channel accounts ----
        new_acct = 0.0
        if m >= g("rep_start_month"):
            new_acct = g("acct_rate_pt") * (g("ft_mult") if ft else 1.0) * dm
        accounts = accounts * (1 - g("acct_churn")) + new_acct
        # capacity cap on programs
        free_h = hours - prospect_h - studies * g("study_hours") - accounts * g("acct_hours")
        cap_prog = max(0.0, free_h / g("program_hours"))
        if programs > cap_prog:
            lost = programs - cap_prog
            new_prog = max(0.0, new_prog - lost)
            programs = cap_prog
        rev["study"] = studies * g("study_price")
        rev["prog"] = programs * g("program_fee")
        rev["agency"] = new_prog * g("agency_fee_pct") * g("ltb_die_per_program") * g("gb_per_die_l1") * g("kgd_factor") * price
        rev["pull"] = programs * g("pull_units_per_program") * g("pull_margin_unit")
        rev["comm"] = accounts * g("acct_purchase_yr") / 12.0 * (price / g("p0_legacy_usd_gb")) * g("commission")
        cogs += studies * g("study_cost") + programs * g("program_direct_cost")

        # ---- fixed costs (part-time base) ----
        opex += g("fixed_pt")
        if m in g("conference_months"):
            opex += g("conference_cost")
        if m == 1:
            opex += g("oneoff_m1")
        opex += g("planA_extra_oneoff").get(m, 0.0)          # Phase 5 variant hook (0 in BASE)
        if m >= g("planA_extra_start"):
            opex += g("planA_extra_month")                   # Phase 5 variant hook (0 in BASE)

        # ---- Plan B: staff, quality, bank, MCM ----
        if plan == "B":
            r1, r2 = g("raise1_month"), g("raise2_month")
            if m >= r1:
                opex += g("overhead_b")
            if m > r1:
                opex += g("qa_mgr")
            if r1 < m <= r2:
                opex += g("test_contractor")
            if m >= r1 + 2:
                opex += g("insurance_b")
            if r1 + 3 <= m <= r1 + 7:
                opex += g("as9120_cert") / 5.0
            if m >= r1 + 15:
                opex += g("as9120_surv_yr") / 12.0
            if m >= r2:
                opex += g("mcm_engineers") + g("itar_month")
            if m >= r2 + 1:
                opex += g("bd_hire")
            if m >= 38:
                opex += g("ops_tech")
            if m >= 60:
                opex += g("scale_hires_m60")
            # bank purchases + NRE
            for i, bm in enumerate(g("bank_months")):
                if m == bm:
                    die0 = g("bank_wafers") * g("good_die_per_wafer")
                    per_die = g("wafer_factor") * price * g("gb_per_die_bank")
                    unit_p = max(g("aftermarket_mult") * g("mult_compress")[scen] * price * g("gb_per_die_bank"),
                                 g("locked_floor_unit"))
                    unit_c = (per_die + pull_cost(P)) / g("pull_yield")
                    if (unit_p - unit_c) / unit_p >= g("bank_min_gm"):
                        capex_inv += die0 * per_die
                        banks.append(dict(month=bm, die0=die0, left=float(die0), basis=per_die,
                                          anchor=price * g("gb_per_die_bank"), opened=0.0,
                                          nre=g("bank_nre_first") if not banks else g("bank_nre_next")))
                    else:
                        skipped.append(bm)
            for b in banks:
                nre_months = 6 if b["nre"] >= 100000 else 3
                if b["month"] <= m < b["month"] + nre_months:
                    opex += b["nre"] / nre_months
                if m > b["month"] and b["left"] > 0:
                    opex += max(g("storage_pct_yr") * b["left"] * b["basis"], g("storage_min_yr")) / 12.0
                    opex += g("surveillance_yr") / 12.0      # Phase 5 (RT-PHY-DD7-03)
            # bank aftermarket sales (first call on banked die)
            for b in banks:
                if m >= b["month"] + g("sell_lag_months") and b["left"] > 0:
                    units_die = min(b["left"], b["die0"] * g("sell_rate_yr")[scen] / 12.0)
                    good = units_die * g("pull_yield")
                    b["left"] -= units_die
                    price_unit = max(g("aftermarket_mult") * g("mult_compress")[scen] * b["anchor"], g("locked_floor_unit"))
                    rev["bank"] += good * price_unit
                    cogs += units_die * b["basis"] + pull_charge(b, units_die, P)
            # MCM NRE
            if mcm_nre_left > 0:
                spend = min(mcm_nre_left, g("mcm_nre_total") / g("mcm_nre_months"))
                opex += spend
                mcm_nre_left -= spend
            # MCM demand: evaluation lot then design-in cohorts
            mcm_units = 0.0
            if m == r2 + g("mcm_nre_months"):
                mcm_units_eval = g("mcm_eval_units")
                rev["mcm"] += mcm_units_eval * g("mcm_eval_price")
                mcm_units += mcm_units_eval
            if m >= r2 + g("mcm_designin_start_lag"):
                rate = g("mcm_designins_yr") / 12.0 * g("mcm_designin_mult")[scen]
                mcm_cohorts.append([m, rate * g("mcm_units_yr_per_designin") / 12.0])
            prod_units = 0.0
            for c in mcm_cohorts:
                if m - c[0] < g("mcm_program_life_months"):
                    c[1] *= (1 - g("mcm_attrition"))
                    prod_units += c[1]
            rev["mcm"] += prod_units * g("mcm_asp")
            mcm_units += prod_units
            if m >= r2 + g("mcm_nre_months"):
                opex += g("mcm_lot_requal_yr") / 12.0        # Phase 5 (RT-VET-DD7-04)
            if mcm_units > 0:
                die_need = mcm_units * g("mcm_die_per_unit") / g("mcm_yield")
                die_cost = 0.0
                mkt = g("kgd_factor") * price * g("gb_per_die_bank")
                for b in banks:  # draw oldest bank first, only when banked die is cheaper than market KGD
                    if die_need <= 0:
                        break
                    if m > b["month"] and b["left"] > 0 and b["basis"] <= mkt:
                        take = min(die_need, b["left"])
                        b["left"] -= take
                        die_cost += take * b["basis"]
                        die_need -= take
                if die_need > 0:
                    die_cost += die_need * mkt
                fixed = mcm_units * (g("mcm_substrate") + g("mcm_assembly") + g("mcm_screen")) / g("mcm_yield")
                cogs += die_cost + fixed

        if plan == "B":
            opex += g("var_opex_hw_pct") * (rev["bank"] + rev["mcm"])
        # ---- founder pay ----
        if ft:
            opex += g("ft_salary_loaded")

        revenue = sum(rev.values())
        ebitda = revenue - cogs - opex
        # write-off of unsold bank die at the horizon end
        writeoff = 0.0
        if plan == "B" and m == months:
            for b in banks:
                writeoff += b["left"] * b["basis"]
        taxable = ebitda - writeoff
        tax = 0.0
        if taxable > 0:
            use = min(nol, taxable)
            nol -= use
            tax = (taxable - use) * g("tax_rate")
        else:
            nol += -taxable

        # ---- cash: collections with lags ----
        services = rev["study"] + rev["prog"] + rev["agency"] + rev["pull"]
        lagged2 = rev["comm"] + rev["bank"] + rev["mcm"]
        collected = ar1 + ar2[0]
        ar1 = services
        ar2 = [ar2[1], lagged2]
        cash += collected - cogs - opex - tax - capex_inv + equity_in
        ext_capital += equity_in
        bridge = 0.0
        if plan == "B" and m >= g("raise1_month") and cash < g("cash_reserve"):
            bridge = g("cash_reserve") - cash
            cash += bridge
            bridges += bridge
            ext_capital += bridge

        contrib = revenue - cogs - (opex - (g("ft_salary_loaded") if ft else 0.0))
        contrib_hist.append(contrib)
        # Plan A full-time trigger (evaluated at month end, effective next month)
        if plan == "A" and not ft and len(contrib_hist) >= 3:
            if sum(contrib_hist[-3:]) / 3.0 >= g("ft_trigger_contrib") and cash >= g("ft_trigger_cash"):
                ft = True
                ft_from = m + 1  # noqa: F841
        recurring = rev["prog"] + rev["comm"]
        rows.append(dict(m=m, label=mlabel(m), price=price, programs=programs, accounts=accounts,
                         rev=revenue, rev_parts=dict(rev), cogs=cogs, opex=opex, ebitda=ebitda,
                         tax=tax, inv=capex_inv, equity=equity_in, bridge=bridge, cash=cash, ft=ft,
                         recurring_arr=12 * recurring, runrate=12 * revenue,
                         bank_die_left=sum(b["left"] for b in banks), writeoff=writeoff))
    return dict(rows=rows, ext_capital=ext_capital, bridges=bridges, banks=banks, skipped=skipped)


def metrics(res, horizon=36, start=1):
    rows = res["rows"][:horizon]
    low = min(rows, key=lambda r: r["cash"])
    be = None
    for i, r in enumerate(rows):
        if r["m"] < start:
            continue
        if i + 3 <= len(rows) and all(x["ebitda"] >= 0 for x in rows[i:i + 3]):
            be = r["m"]
            break
    ft_m = next((r["m"] for r in rows if r["ft"]), None)
    out = dict(cash_low=low["cash"], cash_low_m=low["m"], breakeven=be, ft_month=ft_m,
               cash_end=rows[-1]["cash"])
    for mm in (12, 18, 24, 36):
        if mm <= horizon:
            out["arr_%d" % mm] = rows[mm - 1]["recurring_arr"]
            out["run_%d" % mm] = rows[mm - 1]["runrate"]
    out["ext_by_h"] = sum(r["equity"] + r["bridge"] for r in rows)
    out["rev_cum"] = sum(r["rev"] for r in rows)
    return out


def irr(cfs, lo=-0.99, hi=10.0):
    def npv(r):
        return sum(cf / (1 + r) ** i for i, cf in enumerate(cfs))
    f_lo, f_hi = npv(lo), npv(hi)
    if f_lo * f_hi > 0:
        # Phase 5: a tiny negative tail (storage on the last few die) can flip the sign at r -> -0.99 and hide the
        # economically meaningful root; scan monthly rates from -0.6 to 1.0 and keep the sign change nearest 0.
        grid = [-0.6 + 0.002 * i for i in range(801)]
        vals = [npv(r) for r in grid]
        brackets = [(grid[i], grid[i + 1]) for i in range(800) if vals[i] * vals[i + 1] <= 0]
        if not brackets:
            return None
        lo, hi = min(brackets, key=lambda br: abs(br[0]))
        f_lo, f_hi = npv(lo), npv(hi)
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = npv(mid)
        if f_lo * f_mid <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


# ----------------------------------------------------------------------------------------------
# 4. Unit economics per line
# ----------------------------------------------------------------------------------------------
def bank_standalone(scen, buy_month=20, P=None, months=120):
    """Monthly cash flows of one bank alone (purchase, NRE, storage, pulls, sales), IRR annualised."""
    P = P or INPUTS
    g = lambda k: P[k][0]  # noqa: E731
    price = legacy_price(buy_month, scen, P)
    die0 = g("bank_wafers") * g("good_die_per_wafer")
    basis = g("wafer_factor") * price * g("gb_per_die_bank")
    anchor = price * g("gb_per_die_bank")
    left = float(die0)
    bk = dict(die0=die0, opened=0.0, drawn=0.0)   # wafer-opening state (Phase 5, RT-PHY-DD7-04)
    cfs = [-(die0 * basis + g("bank_nre_first"))]
    units_sold = 0.0
    rev_tot = cost_tot = 0.0
    for k in range(1, months - buy_month + 1):
        cf = -max(g("storage_pct_yr") * left * basis, g("storage_min_yr")) / 12.0 if left > 0 else 0.0
        if left > 0:
            cf -= g("surveillance_yr") / 12.0          # Phase 5 (RT-PHY-DD7-03); 0 in Phase 4
        if k >= g("sell_lag_months") and left > 0:
            u = min(left, die0 * g("sell_rate_yr")[scen] / 12.0)
            left -= u
            good = u * g("pull_yield")
            r = good * max(g("aftermarket_mult") * g("mult_compress")[scen] * anchor, g("locked_floor_unit"))
            c = pull_charge(bk, u, P)
            cf += r - c
            rev_tot += r
            cost_tot += c + u * basis
            units_sold += good
        cfs.append(cf)
    r_m = irr(cfs)
    irr_a = (1 + r_m) ** 12 - 1 if r_m is not None else None
    unit_price = max(g("aftermarket_mult") * g("mult_compress")[scen] * anchor, g("locked_floor_unit"))
    unit_cost = (basis + pull_cost(P)) / g("pull_yield")
    return dict(price_gb=price, basis=basis, die0=die0, outlay=die0 * basis + g("bank_nre_first"),
                unit_price=unit_price, unit_cost=unit_cost, unit_gm=(unit_price - unit_cost) / unit_price,
                irr=irr_a, sold=units_sold, left=left, rev=rev_tot, multiple=sum(c for c in cfs[1:]) / -cfs[0])


def mcm_unit(scen, m, P=None, die_basis=None):
    P = P or INPUTS
    g = lambda k: P[k][0]  # noqa: E731
    price = legacy_price(m, scen, P)
    die = die_basis if die_basis is not None else g("kgd_factor") * price * g("gb_per_die_bank")
    cost = (g("mcm_die_per_unit") * die + g("mcm_substrate") + g("mcm_assembly") + g("mcm_screen")) / g("mcm_yield")
    return dict(die=die, cost=cost, gm=(g("mcm_asp") - cost) / g("mcm_asp"))


def program_unit(P=None):
    P = P or INPUTS
    g = lambda k: P[k][0]  # noqa: E731
    life = 1.0 / g("program_churn")
    pulls = g("pull_units_per_program")
    if g("pull_cap_to_ltb"):   # Phase 5 (RT-VC-DD7-01): a 4,000-die program cannot bill pulls for 100 months
        pulls = min(pulls * life, g("ltb_die_per_program")) / life
    m_gp = g("program_fee") - g("program_direct_cost") + pulls * g("pull_margin_unit")
    agency = g("agency_fee_pct") * g("ltb_die_per_program") * g("gb_per_die_l1") * g("kgd_factor") * g("p0_legacy_usd_gb")
    conv_per_prog = 1.0 / (g("p_study") * g("p_program"))
    hours = conv_per_prog * (g("prospect_hours_pt") / g("conv_pt")) + (1 / g("p_program")) * g("study_hours")
    return dict(monthly_gp=m_gp, agency=agency, life_months=life, ltv=m_gp * life + agency, conv=conv_per_prog,
                cac_hours=hours, study_rev_per_prog=g("study_price") / g("p_program"))


# ----------------------------------------------------------------------------------------------
# 5. Plan C acquisition arithmetic
# ----------------------------------------------------------------------------------------------
def acquisition(scen, P=None):
    P = P or INPUTS
    g = lambda k: P[k][0]  # noqa: E731
    rev = g("acq_staff") * g("acq_rev_per_emp")
    base_ebitda = rev * g("acq_ebitda_margin")["BASE"]
    price = base_ebitda * g("acq_multiple")  # bought at BASE earnings
    ebitda = rev * (0.85 if scen == "GLUT" else 0.75 if scen == "SEVERE" else 1.0) * g("acq_ebitda_margin")[scen]
    loan = price * g("sba_share")
    r, n = g("sba_rate"), g("sba_years")
    pay = loan * r / (1 - (1 + r) ** -n)
    return dict(rev=rev, price=price, ebitda=ebitda, loan=loan, pay=pay, dscr=ebitda / pay,
                equity=price * g("equity_share"), seller=price * g("seller_note_share"),
                outside_equity=max(0.0, price * g("equity_share") - g("founder_cash")))


# ----------------------------------------------------------------------------------------------
# 6. Printing helpers (ASCII only)
# ----------------------------------------------------------------------------------------------
def k(x):
    if x is None:
        return "n/a"
    if abs(x) >= 1e6:
        return "%.2fM" % (x / 1e6)
    if abs(x) >= 1e3:
        return "%.1fk" % (x / 1e3)
    return "%.0f" % x


def pct(x):
    return "n/a" if x is None else "%.1f%%" % (100 * x)


def table(headers, rows):
    w = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    line = "  ".join(str(h).rjust(w[i]) for i, h in enumerate(headers))
    print(line)
    print("  ".join("-" * w[i] for i in range(len(headers))))
    for r in rows:
        print("  ".join(str(c).rjust(w[i]) for i, c in enumerate(r)))


def hdr(t):
    print()
    print("=" * 100)
    print(t)
    print("=" * 100)


def monthly_table(res, n=36):
    rows = []
    for r in res["rows"][:n]:
        p = r["rev_parts"]
        rows.append([r["m"], r["label"], "%.2f" % r["price"], "%.1f" % r["programs"], "%.1f" % r["accounts"],
                     k(p["study"] + p["agency"]), k(p["prog"] + p["pull"]), k(p["comm"]), k(p["bank"] + p["mcm"]),
                     k(r["rev"]), k(r["cogs"]), k(r["opex"]), k(r["ebitda"]), k(r["tax"]), k(r["inv"]),
                     k(r["equity"] + r["bridge"]), k(r["cash"]), "FT" if r["ft"] else "PT",
                     k(r["recurring_arr"])])
    table(["m", "month", "$/GB", "progs", "accts", "one-off", "prog+pull", "comm", "bank+MCM", "revenue",
           "COGS", "opex", "EBITDA", "tax", "invent", "ext.cap", "cash", "fdr", "rec.ARR"], rows)



# ----------------------------------------------------------------------------------------------
# 6b. Phase 5 red-team helpers
# ----------------------------------------------------------------------------------------------
def P_with(base, **ov):
    """Deep copy of an INPUTS-style dict with values overridden (source text marked as a variant)."""
    P = copy.deepcopy(base)
    for name, val in ov.items():
        P[name] = (val, "Phase 5 variant")
    return P


def P_pull_total(base, total):
    """Set the all-in per-die pull cost (re-probe + package + test + burn-in/hot-cold) to `total`."""
    rest = base["reprobe_unit"][0] + base["pack_unit"][0] + base["test_unit"][0]
    return P_with(base, burnin_hotcold_unit=total - rest)


def bank_irr_str(b):
    if b["irr"] is not None:
        return pct(b["irr"])
    return "n/a (cash mult %.2fx)" % b["multiple"]


def pull_breakeven(P, scen="BASE", buy_month=20):
    """All-in pull cost per die at which unit GM = 0 and at which the 10-year cash multiple = 1 (IRR = 0)."""
    g = lambda kk: P[kk][0]  # noqa: E731
    price = legacy_price(buy_month, scen, P)
    unit_p = max(g("aftermarket_mult") * g("mult_compress")[scen] * price * g("gb_per_die_bank"), g("locked_floor_unit"))
    basis = g("wafer_factor") * price * g("gb_per_die_bank")
    gm0 = unit_p * g("pull_yield") - basis
    lo, hi = -50.0, 200.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if bank_standalone(scen, buy_month, P_pull_total(P, mid))["multiple"] > 1.0:
            lo = mid
        else:
            hi = mid
    return dict(gm0=gm0, irr0=(lo + hi) / 2)


def l1_buyer_cost(P):
    """What one L1 managed program costs the OEM against buying packaged parts and dry-storing them."""
    g = lambda kk: P[kk][0]  # noqa: E731
    gb = g("ltb_die_per_program") * g("gb_per_die_l1")
    die_val = gb * g("kgd_factor") * g("p0_legacy_usd_gb")
    pkg_val = gb * g("p0_legacy_usd_gb")
    n = g("ltb_die_per_program")
    out = []
    for life, lab in ((n / g("pull_units_per_program"), "die exhausted (80/month)"),
                      (1.0 / g("program_churn"), "model program life")):
        founder = g("program_fee") * life + g("agency_fee_pct") * die_val + g("study_price") + n * g("pull_margin_unit")
        osat_lo = n * 10.0
        osat_hi = n * (g("reprobe_unit") + g("pack_unit") + g("test_unit")) / g("pull_yield")
        stor_lo = g("storage_pct_yr") * die_val * life / 12.0
        stor_hi = max(g("storage_pct_yr") * die_val, g("storage_min_yr")) * life / 12.0
        lo = die_val + founder + osat_lo + stor_lo + g("bank_nre_next")
        hi = die_val + founder + osat_hi + stor_hi + g("bank_nre_first")
        out.append(dict(label=lab, life=life, founder=founder, lo=lo, hi=hi))
    packaged = pkg_val + 3000.0  # ESTIMATE: dry-pack / N2 cabinet at the CM over the program life
    return dict(die_val=die_val, pkg_val=pkg_val, packaged=packaged, rows=out)


def dd6_hours_check():
    """RT-VC-DD7-03: DD6 BASE with founder hours diverted to DD7 (imports models/private-moe-appliance.py)."""
    try:
        import importlib.util
        import io
        import contextlib
        spec = importlib.util.spec_from_file_location("dd6_model", os.path.join(HERE, "private-moe-appliance.py"))
        mod = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)
            out = []
            for h in (65.0, 55.0, 45.0):
                r = mod.run_with({"founder_hours_pt": h}, "BASE")
                out.append((h, r["ft_month"], r["arr"][36]))
        return out
    except Exception as exc:  # pragma: no cover
        return "DD6 model import failed: %s" % exc


def redteam_section():
    hdr("10. RED-TEAM REVISIONS (Phase 5): reproduction of Phase 4, reviewer variants, revised result")
    P4 = INPUTS_P4
    print("10a. Reproduction on Phase 4 inputs (must match the Phase 4 output):")
    rA = {s_: metrics(simulate(s_, "A", 36, P4)) for s_ in SCENS}
    b4 = bank_standalone("BASE", P=P4)
    print("   Plan A m36 recurring ARR BASE/GLUT/SEVERE $%s / $%s / $%s; cash low $%s at m%d"
          % (k(rA["BASE"]["arr_36"]), k(rA["GLUT"]["arr_36"]), k(rA["SEVERE"]["arr_36"]), k(rA["BASE"]["cash_low"]),
             rA["BASE"]["cash_low_m"]))
    print("   Bank m20 BASE: unit GM %s, IRR %s, cash multiple %.2fx | MCM GM m1/m36/m60: %s / %s / %s"
          % (pct(b4["unit_gm"]), pct(b4["irr"]), b4["multiple"], pct(mcm_unit("BASE", 1, P4)["gm"]),
             pct(mcm_unit("BASE", 36, P4)["gm"]), pct(mcm_unit("BASE", 60, P4)["gm"])))
    rb4 = simulate("BASE", "B", MONTHS_B, P4)
    ev4 = P4["ev_rev_multiple"][0] * sum(r["rev"] for r in rb4["rows"][108:120])
    print("   Plan B BASE EV/capital %.2fx on $%s" % (ev4 / rb4["ext_capital"], k(rb4["ext_capital"])))

    print()
    print("10b. L1 buyer economics (RT-HYP-DD7-01, RT-VC-DD7-01, RT-VET-DD7-01), one 4,000-die program at 2026 prices:")
    lb = l1_buyer_cost(P4)
    print("   die value (KGD) $%s | same parts packaged $%s | packaged LTB + dry storage $%s [ESTIMATE +$3k]"
          % (k(lb["die_val"]), k(lb["pkg_val"]), k(lb["packaged"])))
    rows = []
    for r in lb["rows"]:
        rows.append([r["label"], "%.0f" % r["life"], k(r["founder"]), k(r["lo"]), k(r["hi"]),
                     "%.1f-%.1fx" % (r["lo"] / lb["packaged"], r["hi"] / lb["packaged"])])
    table(["life basis", "months", "billed by founder", "OEM total low", "OEM total high", "vs packaged LTB"], rows)
    print("   OEM total = die + founder billing (fees, 4%% agency, study, $1/pull) + U.S. package/test ($10-12.11/die)"
          " + vault (3%%/yr, or $5k/yr minimum) + package/test set-up ($40k-120k). A board OEM also gets a new part"
          " number (RT-VET-DD7-02). Phase 4 program_unit billed %.0f pulls from a %d-die program (bug, fixed)."
          % (P4["pull_units_per_program"][0] / P4["program_churn"][0], P4["ltb_die_per_program"][0]))
    pu4, pu5 = program_unit(P4), program_unit(INPUTS)
    print("   program lifetime gross profit: Phase 4 $%s -> pull cap + p_program 0.10: $%s; conversations per program"
          " %.1f -> %.1f (~%.0f -> ~%.0f founder hours)"
          % (k(pu4["ltv"]), k(pu5["ltv"]), pu4["conv"], pu5["conv"], pu4["cac_hours"], pu5["cac_hours"]))

    print()
    print("10c. Plan A variants on Phase 4 inputs (L1 still on), BASE:")
    as9120 = {mm: 7000.0 for mm in range(2, 7)}
    var = [
        ("Phase 4 as published", {}),
        ("RT-VC-DD7-02 p_program 0.35 -> 0.10", dict(p_program=0.10)),
        ("RT-HYP-DD7-02 NIST 800-171/CUI: +$35k at m6, +$500/mo from m6",
         dict(planA_extra_oneoff={6: 35000.0}, planA_extra_month=500.0, planA_extra_start=6)),
        ("RT-HYP-DD7-03 AS9120B in year 1: $35k m2-m6, $8k/yr from m14",
         dict(planA_extra_oneoff=as9120, planA_extra_month=8000.0 / 12, planA_extra_start=14)),
        ("HYP-02 + HYP-03 together",
         dict(planA_extra_oneoff=dict(list(as9120.items()) + [(6, 35000.0 + 7000.0)]), planA_extra_month=500.0 + 8000.0 / 12,
              planA_extra_start=6)),
    ]
    rows = []
    for lab, ov in var:
        res = simulate("BASE", "A", 36, P_with(P4, **ov))
        mt = metrics(res)
        below = next((r["m"] for r in res["rows"] if r["cash"] < 20000), None)
        rows.append([lab, k(mt["arr_36"]), k(mt["cash_low"]), mt["cash_low_m"], below or "never"])
    table(["variant", "m36 rec.ARR", "cash low", "at m", "cash < $20k floor (kill #8)"], rows)

    print()
    print("10d. L3 bank #1 (bought m20, BASE), one change at a time on Phase 4 inputs, then all Phase 5 revisions:")
    var = [
        ("Phase 4", P4),
        ("RT-HYP-DD7-04 aftermarket 1.5x", P_with(P4, aftermarket_mult=1.5)),
        ("RT-HYP-DD7-04 aftermarket 2.0x (blend)", P_with(P4, aftermarket_mult=2.0)),
        ("RT-PHY-DD7-03 pull yield 0.90", P_with(P4, pull_yield=0.90)),
        ("RT-PHY-DD7-03 pull yield 0.85", P_with(P4, pull_yield=0.85)),
        ("RT-PHY-DD7-03 pull yield 0.80", P_with(P4, pull_yield=0.80)),
        ("RT-PHY-DD7-03 +$5k/yr surveillance", P_with(P4, surveillance_yr=5000.0)),
        ("RT-PHY-DD7-04 whole-wafer opening", P_with(P4, pull_whole_wafer=True)),
        ("RT-VET-DD7-03 pull $15.00 (old C1 pass line)", P_pull_total(P4, 15.0)),
        ("RT-VET-DD7-03 pull $21.50", P_pull_total(P4, 21.5)),
        ("RT-VET-DD7-03 pull $30.00", P_pull_total(P4, 30.0)),
        ("RT-PHY-DD7-05 736 die/wafer x 17 wafers", P_with(P4, good_die_per_wafer=736, bank_wafers=17)),
        ("ALL Phase 5 revisions (revised BASE)", INPUTS),
    ]
    rows = []
    for lab, P in var:
        b = bank_standalone("BASE", P=P)
        rows.append([lab, "%.2f" % b["unit_price"], "%.2f" % b["unit_cost"], pct(b["unit_gm"]),
                     ">=20%" if b["unit_gm"] >= INPUTS["bank_min_gm"][0] else "NO BUY", bank_irr_str(b),
                     "%.2fx" % b["multiple"]])
    table(["variant", "sale/unit", "cost/unit", "unit GM", "buy rule", "10y IRR", "cash mult"], rows)
    be4, be5 = pull_breakeven(P4), pull_breakeven(INPUTS)
    print("   all-in pull cost per die at break-even: Phase 4 inputs unit GM 0 at $%.2f, IRR 0 at $%.2f; revised inputs"
          " unit GM 0 at $%.2f, IRR 0 at $%.2f (Phase 4 C1 pass line was $15)."
          % (be4["gm0"], be4["irr0"], be5["gm0"], be5["irr0"]))
    for s_ in SCENS:
        b = bank_standalone(s_, P=INPUTS)
        print("   revised %s: unit GM %s, IRR %s" % (s_, pct(b["unit_gm"]), bank_irr_str(b)))

    print()
    print("10e. L4 MCM unit GM at $900 ASP, BASE m1 / m36 / m60:")
    var = [
        ("Phase 4 (side by side, 91% yield)", P4),
        ("RT-PHY-DD7-01 stacked/RDL $90 + $160", P_with(P4, mcm_substrate=90.0, mcm_assembly=160.0)),
        ("RT-PHY-DD7-01 stacked/RDL at 85% yield", P_with(P4, mcm_substrate=90.0, mcm_assembly=160.0, mcm_yield=0.85)),
        ("RT-VET-DD7-04 module yield 0.76 (3%/die)", P_with(P4, mcm_yield=0.97 ** 9)),
        ("RT-VET-DD7-04 module yield 0.63 (5%/die)", P_with(P4, mcm_yield=0.95 ** 9)),
        ("RT-VET-DD7-04 0.76 + KGD at parity", P_with(P4, mcm_yield=0.97 ** 9, kgd_factor=1.0)),
        ("RT-PHY-DD7-02 125C bin 98%/die (0.834)", P_with(P4, mcm_yield=0.98 ** 9)),
        ("RT-PHY-DD7-02 125C bin 95%/die (0.630)", P_with(P4, mcm_yield=0.95 ** 9)),
        ("RT-PHY-DD7-02 125C bin 90%/die (0.387)", P_with(P4, mcm_yield=0.90 ** 9)),
        ("ALL Phase 5 revisions (revised BASE)", INPUTS),
    ]
    rows = []
    for lab, P in var:
        u = [mcm_unit("BASE", mm, P) for mm in (1, 36, 60)]
        rows.append([lab, "%.3f" % P["mcm_yield"][0], " / ".join("%.0f" % x["cost"] for x in u),
                     " / ".join(pct(x["gm"]) for x in u)])
    table(["variant", "module yield", "unit cost m1/m36/m60", "GM m1/m36/m60"], rows)
    trfc = 0.350
    print("   RT-PHY-DD7-02 refresh tax (8Gb tRFC1 = 350 ns): JEDEC 2x per 10 C beyond 95 C (3.9 us) ->"
          " 105 C %.0f%%, 115 C %.0f%%, 125 C %.0f%% of device time"
          % tuple(100 * trfc / (3.9 / 2 ** ((t - 95) / 10.0)) for t in (105, 115, 125)))
    kb = 8.617e-5
    for ea in (0.5, 0.6):
        f = 2.718281828 ** (ea / kb * (1 / 358.15 - 1 / 398.15))
        print("   Arrhenius Ea %.1f eV from 85 C (7.8 us): 125 C tREFI %.2f us -> refresh tax %.0f%%"
              % (ea, 7.8 / f, 100 * trfc / (7.8 / f)))

    print()
    print("10f. RT-PHY-DD7-05 die size: wafers for a 12,510-die bank and silicon area of a nine-die MCM:")
    rows = []
    for area in (45.0, 60.0, 75.0, 90.0):
        gross = 3.14159265 * 150 ** 2 / area - 3.14159265 * 300 / (2 * area) ** 0.5
        good = 0.85 * gross
        rows.append(["%.0f mm2" % area, "%.0f" % gross, "%.0f" % good, "%.1f" % (12510 / good), "%.0f mm2" % (9 * area),
                     "%.0f%%" % (100 * 9 * area / 300.0)])
    table(["8Gb die", "gross/wafer", "good (85%)", "wafers for 12,510", "9-die silicon", "of 15x20 mm"], rows)

    print()
    print("10g. Plan B 10-year view and the BULL what-if (RT-VC-DD7-06):")
    rows = []
    for lab, P in (("Phase 4", P4), ("revised", INPUTS)):
        for s_ in SCENS:
            rb = simulate(s_, "B", MONTHS_B, P)
            r10 = sum(r["rev"] for r in rb["rows"][108:120])
            rows.append([lab, s_, k(r10), k(rb["ext_capital"]), "%.2fx" % (P["ev_rev_multiple"][0] * r10 / rb["ext_capital"]),
                         ",".join(str(b["month"]) for b in rb["banks"]) or "none"])
    table(["inputs", "scen", "y10 revenue", "ext. capital", "EV/capital", "banks bought"], rows)
    for lab, P in (("Phase 4", P4), ("revised", INPUTS)):
        Pb = P_with(P, mcm_designins_yr=4.0, mcm_units_yr_per_designin=1000.0, mcm_asp=1500.0, aftermarket_mult=4.0,
                    mcm_designin_start_lag=24)
        rb = simulate("BASE", "B", MONTHS_B, Pb)
        r10 = sum(r["rev"] for r in rb["rows"][108:120])
        mult = P["ev_rev_multiple"][0] * r10 / rb["ext_capital"]
        print("   BULL %s: y10 revenue $%s, capital $%s, EV/capital %.2fx = %.1f%%/yr gross over 10 years if all capital"
              " went in at t0 (before dilution, option pool and a co-founder's equity)"
              % (lab, k(r10), k(rb["ext_capital"]), mult, 100 * (mult ** 0.1 - 1)))

    print()
    print("10h. RT-VC-DD7-03 founder hours: DD6 BASE with DD7 hours carved out of the 65 h/month:")
    d6 = dd6_hours_check()
    if isinstance(d6, str):
        print("   " + d6)
    else:
        for h, ftm, a36 in d6:
            print("   DD6 founder_hours_pt %.0f: full-time %s, m36 ARR $%s" % (h, ("m%d" % ftm) if ftm else "never", k(a36)))

    print()
    print("10i. RT-VC-DD7-05 / RT-HYP-DD7-07 fee pool (what the founder could bill), not die value:")
    lon = 1268 * 0.10
    prog_arr = 12 * INPUTS_P4["program_fee"][0]
    print("   ~%.0f memory life-of-need cases/yr (unsourced 10%% share) x $%s program ARR = $%s/yr of new ARR at 100%%"
          " national share, plus 4%% agency on $50-200k = $%s-%s/yr one-off; at a 3-5%% share: $%s-%s of new ARR/yr"
          % (lon, k(prog_arr), k(lon * prog_arr), k(lon * 0.04 * 50e3), k(lon * 0.04 * 200e3),
             k(0.03 * lon * prog_arr), k(0.05 * lon * prog_arr)))

    print()
    print("10j. Residual Plan A = L2 rep commissions only (RT-VC-DD7-08), revised inputs:")
    var = [
        ("revised BASE (5%, 0.30 accts/mo, $680/mo fixed)", INPUTS),
        ("commission 3%", P_with(INPUTS, commission=0.03)),
        ("account rate 0.20/mo", P_with(INPUTS, acct_rate_pt=0.20)),
        ("lean: fixed $300/mo, no conference", P_with(INPUTS, fixed_pt=300.0, conference_cost=0.0)),
    ]
    rows = []
    for lab, P in var:
        for s_ in SCENS:
            res = simulate(s_, "A", 36, P)
            mt = metrics(res)
            below = next((r["m"] for r in res["rows"] if r["cash"] < 20000), None)
            rows.append([lab if s_ == "BASE" else "", s_, k(mt["arr_18"]), k(mt["arr_36"]), mt["breakeven"] or "none",
                         mt["ft_month"] or "never", k(mt["cash_low"]), mt["cash_low_m"], below or "never"])
    table(["variant", "scen", "rec.ARR m18", "m36", "breakeven m", "FT", "cash low", "at m", "cash < $20k"], rows)
    p_rep = 0.25
    a36 = metrics(simulate("BASE", "A", 36, INPUTS))["arr_36"]
    print("   probability-weighted BASE m36 ARR at p(rep offer) = %.2f [ESTIMATE: Intelligent Memory chose scaled"
          " distributors in 2026] = $%s" % (p_rep, k(p_rep * a36)))

    print()
    print("10k. Plan C (RT-VC-DD7-07): DSCR unchanged (1.50 / 0.85 / 0.45); dropped as not executable by this founder"
          " (full-time, personal guarantee on ~$3.6M, $410k outside equity, no named target).")


# ----------------------------------------------------------------------------------------------
# 7. Main
# ----------------------------------------------------------------------------------------------
def main():
    print("DD7 legacy-dram-diebank model | as of 2026-11-01 | reference: %s" % REF_SRC)
    print("DDR5 reference: contract $%.2f/GB, glut $%.2f/GB, severe $%.2f/GB, incumbent cost $%.2f/GB, "
          "64GB RDIMM $%.1f/user-GB (glut $%.1f)" % (P0, P_GLUT, P_SEVERE, REF["cost_component_usd_per_gb"],
                                                     REF["contract_rdimm64_usd_per_user_gb_q4_2026"],
                                                     REF["glut_rdimm64_usd_per_user_gb"]))

    hdr("1. INPUTS (value | source)")
    for name, (val, src) in INPUTS.items():
        sval = val if not isinstance(val, float) else ("%.4g" % val)
        print("%-28s %-34s | %s" % (name, str(sval)[:34], src))

    hdr("2. Legacy DDR4 price path used by every line ($/GB packaged)")
    rows = []
    for m in (1, 12, 15, 17, 18, 20, 24, 26, 30, 36, 48, 60, 120):
        rows.append([m, mlabel(m)] + ["%.2f" % legacy_price(m, s) for s in SCENS])
    table(["m", "month"] + SCENS, rows)

    hdr("3. Unit economics per product line")
    pu = program_unit()
    print("L1 managed die-bank program (consignment vault; OEM owns die; founder = program manager)"
          " -- KILLED in Phase 5 (RT-HYP/VC/VET-DD7-01); unit economics shown as a what-if on revised inputs")
    print("   monthly gross profit/program $%.0f | agency fee at start $%.0f (2026 price) | expected life %.0f months"
          % (pu["monthly_gp"], pu["agency"], pu["life_months"]))
    print("   lifetime gross profit/program $%s + study revenue per program won $%s"
          % (k(pu["ltv"]), k(pu["study_rev_per_prog"])))
    print("   acquisition: %.1f qualified conversations per program = ~%.0f founder hours (CAC in time, not cash)"
          % (pu["conv"], pu["cac_hours"]))
    print("L2 channel commission per account: $%.0f/yr at 2026 prices; $%.0f/yr at the $%.2f long-run price"
          % (v("acct_purchase_yr") * v("commission"), v("acct_purchase_yr") * v("commission") * v("long_run_usd_gb") / P0,
             v("long_run_usd_gb")))
    print()
    print("L3 title-taking bank (one bank = %d wafers x %d good die = %d DDR4 8Gb die), bought at m20, sold from m38:"
          % (v("bank_wafers"), v("good_die_per_wafer"), v("bank_wafers") * v("good_die_per_wafer")))
    rows = []
    for s in SCENS:
        b = bank_standalone(s)
        rows.append([s, "%.2f" % b["price_gb"], "%.2f" % b["basis"], k(b["outlay"]), "%.2f" % b["unit_price"],
                     "%.2f" % b["unit_cost"], pct(b["unit_gm"]), pct(b["irr"]), "%.2fx" % b["multiple"],
                     k(b["sold"]), k(b["left"])])
    table(["scen", "$/GB@buy", "die basis", "outlay", "sale/unit", "cost/unit", "unit GM", "10y IRR",
           "cash mult", "units sold", "die left"], rows)
    print("   (sale/unit = %.1fx the packaged part price at EOL, compressed in a glut; cost/unit = die basis + re-probe"
          " + U.S. package + test, / pull yield)" % v("aftermarket_mult"))
    b2 = copy.deepcopy(INPUTS)
    rows = []
    for anchor_m, lab in ((1, "bought at 2026 peak (m1)"), (20, "bought m20"), (60, "bought at long-run (m60)")):
        for s in ("BASE",):
            b = bank_standalone(s, buy_month=anchor_m, P=b2, months=anchor_m + 100)
            rows.append([lab, "%.2f" % b["price_gb"], "%.2f" % b["unit_price"], "%.2f" % b["unit_cost"],
                         pct(b["unit_gm"]), pct(b["irr"])])
    P_scale = copy.deepcopy(INPUTS)
    for nn, val in (("reprobe_unit", 0.5), ("pack_unit", 1.0), ("test_unit", 0.5)):
        P_scale[nn] = (val, "what-if: Rochester-scale in-house assembly/test")
    b = bank_standalone("BASE", buy_month=60, P=P_scale, months=160)
    rows.append(["m60, pull $2/die (Rochester-scale), incl. $120k NRE", "%.2f" % b["price_gb"], "%.2f" % b["unit_price"],
                 "%.2f" % b["unit_cost"], pct(b["unit_gm"]), pct(b["irr"])])
    P_floor = copy.deepcopy(INPUTS)
    P_floor["locked_floor_unit"] = (20.0, "what-if")
    b = bank_standalone("BASE", buy_month=60, P=P_floor, months=160)
    rows.append(["m60, $20 locked-buyer floor, incl. $120k NRE", "%.2f" % b["price_gb"], "%.2f" % b["unit_price"],
                 "%.2f" % b["unit_cost"], pct(b["unit_gm"]), pct(b["irr"])])
    print("   Timing and scale check (BASE sell-through, price anchored at purchase):")
    table(["purchase", "$/GB", "sale/unit", "cost/unit", "unit GM", "IRR"], rows)
    print()
    print("L4 hi-rel x72 ECC DDR4 MCM (9 die + substrate + assembly + screening, / %.0f%% module yield), ASP $%.0f:"
          % (100 * v("mcm_yield"), v("mcm_asp")))
    rows = []
    for s in SCENS:
        for m in (1, 36, 60):
            u = mcm_unit(s, m)
            rows.append([s, m, mlabel(m), "%.2f" % u["die"], "%.0f" % u["cost"], pct(u["gm"])])
    table(["scen", "m", "month", "die $", "unit cost", "GM @ASP"], rows)
    u = mcm_unit("BASE", 60)
    gp_designin = (v("mcm_asp") - u["cost"]) * v("mcm_units_yr_per_designin") * v("mcm_program_life_months") / 12.0
    print("   gross profit per design-in over %d months (no attrition, long-run die): $%s -> NRE $%s needs %.1f design-ins"
          % (v("mcm_program_life_months"), k(gp_designin), k(v("mcm_nre_total")), v("mcm_nre_total") / gp_designin))

    # ---------------- Plan A ----------------
    hdr("4. PLAN A - bootstrap wedge, founder's $40k, part-time. Phase 5: L1 KILLED, so the residual is L2 rep commissions only")
    resA = {s: simulate(s, "A", MONTHS_A) for s in SCENS}
    print("Monthly P&L and cash, BASE (one-off = studies + agency fees; prog+pull = program fees + pull margin;"
          " comm = channel commissions):")
    monthly_table(resA["BASE"])
    print()
    rows = []
    for s in SCENS:
        mt = metrics(resA[s])
        rows.append([s, k(mt["arr_12"]), k(mt["arr_18"]), k(mt["arr_24"]), k(mt["arr_36"]), k(mt["run_36"]),
                     mt["breakeven"] or "none", mt["ft_month"] or "never", k(mt["cash_low"]), mt["cash_low_m"],
                     k(mt["cash_end"]), k(mt["rev_cum"])])
    table(["scen", "recARR m12", "m18", "m24", "m36", "run-rate m36", "breakeven m", "FT month", "cash low",
           "at m", "cash m36", "cum rev"], rows)
    print("   breakeven = first month EBITDA >= 0 for 3 straight months (part-time: no founder pay, so it is early and"
          " means little); FT month = when the wedge can pay the founder $10k/month.")
    for s in SCENS:
        r36 = resA[s]["rows"][35]
        print("   %s m36 mix: programs %.1f, accounts %.1f, recurring ARR $%s of which commissions $%s"
              % (s, r36["programs"], r36["accounts"], k(r36["recurring_arr"]), k(12 * r36["rev_parts"]["comm"])))

    # ---------------- Plan B ----------------
    hdr("5. PLAN B - staged moonshot (gated outside capital): Stage-1 $1.5M at m18, Stage-2 $4.0M at m30")
    resB = {s: simulate(s, "B", MONTHS_B) for s in SCENS}
    print("Monthly P&L and cash, BASE, m1-m36 (ext.cap = equity raises + automatic bridges to keep $50k):")
    monthly_table(resB["BASE"], 36)
    print()
    rows = []
    for s in SCENS:
        mt = metrics(resB[s], 36, start=v("raise1_month"))
        low_pre = min(resB[s]["rows"][:35], key=lambda r: r["cash"] - r["equity"] - r["bridge"])
        rows.append([s, k(mt["arr_12"]), k(mt["arr_18"]), k(mt["arr_24"]), k(mt["arr_36"]), k(mt["run_36"]),
                     mt["breakeven"] or "none", k(mt["cash_low"]), mt["cash_low_m"], k(mt["ext_by_h"]),
                     k(mt["rev_cum"]), k(mt["cash_end"])])
    table(["scen", "recARR m12", "m18", "m24", "m36", "run-rate m36", "post-raise BE", "cash low", "at m",
           "ext.capital by m36", "cum rev m36", "cash m36"], rows)
    print("   Cash low is the founder-funded phase (before Stage-1); after the raises the plan burns outside money and"
          " has no breakeven inside 36 months. ARR here = program fees + commissions only (bank and MCM have no"
          " revenue before m36).")
    for s in SCENS:
        bb = resB[s]
        print("   %s banks bought at m%s; skipped by the >=%.0f%% unit-GM rule at m%s"
              % (s, ",".join(str(b["month"]) for b in bb["banks"]) or "-", 100 * v("bank_min_gm"),
                 ",".join(str(x) for x in bb["skipped"]) or "-"))

    hdr("6. PLAN B 10-year ceiling view (the MOONSHOT test; no horizon limit)")
    rows = []
    for s in SCENS:
        R = resB[s]["rows"]
        for y in range(1, 11):
            ys = R[(y - 1) * 12:y * 12]
            rev = sum(r["rev"] for r in ys)
            bank = sum(r["rev_parts"]["bank"] for r in ys)
            mcm = sum(r["rev_parts"]["mcm"] for r in ys)
            ebitda = sum(r["ebitda"] for r in ys)
            ext = sum(r["equity"] + r["bridge"] for r in ys)
            if y in (1, 2, 3, 4, 5, 6, 8, 10):
                rows.append([s, y, k(rev), k(bank), k(mcm), k(ebitda), k(ext), k(ys[-1]["cash"])])
    table(["scen", "year", "revenue", "bank rev", "MCM rev", "EBITDA", "ext.cap in yr", "cash yr-end"], rows)
    print()
    rows = []
    summary_b = {}
    for s in SCENS:
        R = resB[s]["rows"]
        y10 = R[108:120]
        rev10 = sum(r["rev"] for r in y10)
        ebitda10 = sum(r["ebitda"] for r in y10)
        ev = v("ev_rev_multiple") * rev10
        ext = resB[s]["ext_capital"]
        wo = R[-1]["writeoff"]
        first_pos = next((y for y in range(3, 11) if sum(r["ebitda"] for r in R[(y - 1) * 12:y * 12]) > 0), None)
        be120 = metrics(resB[s], MONTHS_B, start=v("raise1_month"))["breakeven"]
        summary_b[s] = dict(rev10=rev10, ext=ext, ev=ev, be=be120)
        rows.append([s, k(rev10), k(ebitda10), first_pos or "never", be120 or "none", k(ext),
                     k(resB[s]["bridges"]), k(ev), "%.2fx" % (ev / ext), k(wo)])
    table(["scen", "y10 revenue", "y10 EBITDA", "1st EBITDA+ yr (y3+)", "post-raise BE month", "total ext.capital",
           "of which bridges", "EV @1.5x rev", "EV / capital", "die written off"], rows)
    # bull stretch: what it would take
    P_bull = copy.deepcopy(INPUTS)
    for nn, val in (("mcm_designins_yr", 4.0), ("mcm_units_yr_per_designin", 1000.0), ("mcm_asp", 1500.0),
                    ("aftermarket_mult", 4.0), ("mcm_designin_start_lag", 24)):
        P_bull[nn] = (val, "BULL what-if")
    rb = simulate("BASE", "B", MONTHS_B, P_bull)
    rev10b = sum(r["rev"] for r in rb["rows"][108:120])
    eb10b = sum(r["ebitda"] for r in rb["rows"][108:120])
    print("   BULL what-if (BASE prices; 4 design-ins/yr x 1,000 units at $1,500, first at m54; aftermarket 4.0x):"
          " y10 revenue $%s, y10 EBITDA $%s, external capital $%s, EV/capital %.2fx (at 1.5x revenue)."
          % (k(rev10b), k(eb10b), k(rb["ext_capital"]), v("ev_rev_multiple") * rev10b / rb["ext_capital"]))
    print()
    print("   What the MCM line must achieve (BASE prices, ASP $%.0f): EV/capital at 1.5x y10 revenue [y10 revenue]"
          % v("mcm_asp"))
    grid_rows = []
    grid = {}
    for dpy in (2.0, 4.0, 6.0):
        row = ["%.0f design-ins/yr" % dpy]
        for upy in (300.0, 600.0, 1000.0):
            Pg = copy.deepcopy(INPUTS)
            Pg["mcm_designins_yr"] = (dpy, "grid")
            Pg["mcm_units_yr_per_designin"] = (upy, "grid")
            rg = simulate("BASE", "B", MONTHS_B, Pg)
            r10 = sum(r["rev"] for r in rg["rows"][108:120])
            ratio = v("ev_rev_multiple") * r10 / rg["ext_capital"]
            grid[(dpy, upy)] = ratio
            row.append("%.2fx [%s]" % (ratio, k(r10)))
        grid_rows.append(row)
    table(["", "300 units/yr each", "600 units/yr each", "1,000 units/yr each"], grid_rows)
    print("   Ceiling check: Rochester Electronics (70+ OCMs, >20,000 device types, >10B die) is estimated at"
          " $200-500M revenue by data aggregators (private; see notes). This plan's year-10 revenue is the honest"
          " DRAM-only ceiling for a new entrant.")
    dsp_cases = 4143 + 2809 + 24 + 1268
    mem_share = 0.10
    lon = 1268 * mem_share
    print("   DMSMS sanity check: DSPO 2024 case mix (no-issue 4,143 + simple substitute 2,809 + complex 24 +"
          " life-of-need buy 1,268 = %d cases, redesign excluded); if ~%.0f%% are memory, ~%.0f memory life-of-need"
          " buys/yr; at $50-200k each = $%s-%s/yr of DMSMS-tracked demand [ESTIMATE]."
          % (dsp_cases, 100 * mem_share, lon, k(lon * 50e3), k(lon * 200e3)))

    # ---------------- Plan C ----------------
    hdr("7. PLAN C - acquire a small licensed aftermarket manufacturer / test house (Resurgent-like, ~30 staff)")
    rows = []
    for s in SCENS:
        a = acquisition(s)
        rows.append([s, k(a["rev"]), k(a["price"]), k(a["ebitda"]), k(a["loan"]), k(a["pay"]), "%.2f" % a["dscr"],
                     k(a["equity"]), k(a["seller"]), k(a["outside_equity"])])
    table(["scen", "revenue", "price", "EBITDA", "SBA loan", "debt svc/yr", "DSCR", "equity", "seller note",
           "outside equity"], rows)
    print("   Lenders typically want DSCR >= ~1.25 [ESTIMATE]. The founder must run it full-time (day job ends), and"
          " OCM licences may carry change-of-control clauses (not checked).")

    # ---------------- Sensitivity ----------------
    hdr("8. Sensitivity (+/-30%)")
    print("Plan A, BASE, m36 recurring ARR / m36 cash / FT month:")
    knobs_A = {
        "price (fee, study, commission)": ["program_fee", "study_price", "commission"],
        "conversion (p_study)": ["p_study"],
        "churn (program + account)": ["program_churn", "acct_churn"],
        "COGS (direct + fixed costs)": ["program_direct_cost", "study_cost", "fixed_pt"],
    }
    base_mt = metrics(simulate("BASE", "A", 36))
    rows = [["baseline", k(base_mt["arr_36"]), k(base_mt["cash_end"]), base_mt["ft_month"] or "never", "", "", ""]]
    for lab, names in knobs_A.items():
        out = []
        for f in (0.7, 1.3):
            P = copy.deepcopy(INPUTS)
            for n in names:
                P[n] = (P[n][0] * f, P[n][1])
            mt = metrics(simulate("BASE", "A", 36, P))
            out.append(mt)
        rows.append([lab, k(out[0]["arr_36"]), k(out[0]["cash_end"]), out[0]["ft_month"] or "never",
                     k(out[1]["arr_36"]), k(out[1]["cash_end"]), out[1]["ft_month"] or "never"])
    table(["knob", "-30% ARR", "-30% cash", "-30% FT", "+30% ARR", "+30% cash", "+30% FT"], rows)
    print()
    print("Plan B, BASE, 10-year: y10 revenue / total external capital / EV-to-capital:")
    knobs_B = {
        "price (aftermarket mult, MCM ASP)": ["aftermarket_mult", "mcm_asp"],
        "conversion (design-ins, sell-through)": ["mcm_designins_yr", "sell_rate_yr"],
        "churn (MCM attrition, programs)": ["mcm_attrition", "program_churn", "acct_churn"],
        "COGS (die, pack/test, MCM build)": ["wafer_factor", "kgd_factor", "pack_unit", "test_unit",
                                            "mcm_substrate", "mcm_assembly", "mcm_screen"],
    }

    def b_summary(P):
        res = simulate("BASE", "B", MONTHS_B, P)
        rev10 = sum(r["rev"] for r in res["rows"][108:120])
        ev = P["ev_rev_multiple"][0] * rev10
        return rev10, res["ext_capital"], ev / res["ext_capital"]

    r0 = b_summary(INPUTS)
    rows = [["baseline", k(r0[0]), k(r0[1]), "%.2fx" % r0[2], "", "", ""]]
    for lab, names in knobs_B.items():
        out = []
        for f in (0.7, 1.3):
            P = copy.deepcopy(INPUTS)
            for n in names:
                val = P[n][0]
                if isinstance(val, dict):
                    val = {kk: vv * f for kk, vv in val.items()}
                else:
                    val = val * f
                P[n] = (val, P[n][1])
            out.append(b_summary(P))
        rows.append([lab, k(out[0][0]), k(out[0][1]), "%.2fx" % out[0][2], k(out[1][0]), k(out[1][1]),
                     "%.2fx" % out[1][2]])
    table(["knob", "-30% y10 rev", "-30% capital", "-30% EV/cap", "+30% y10 rev", "+30% capital", "+30% EV/cap"], rows)
    print()
    print("Bank #1 standalone IRR, BASE, one knob at a time (+/-30%):")
    rows = []
    for lab, n in (("aftermarket mult", "aftermarket_mult"), ("sell-through rate", "sell_rate_yr"),
                   ("die cost (wafer factor)", "wafer_factor"), ("U.S. pack+test", None)):
        out = []
        for f in (0.7, 1.3):
            P = copy.deepcopy(INPUTS)
            if n is None:
                for nn in ("pack_unit", "test_unit", "reprobe_unit"):
                    P[nn] = (P[nn][0] * f, P[nn][1])
            else:
                val = P[n][0]
                P[n] = ({kk: vv * f for kk, vv in val.items()} if isinstance(val, dict) else val * f, P[n][1])
            out.append(bank_standalone("BASE", P=P)["irr"])
        rows.append([lab, pct(out[0]), pct(out[1])])
    table(["knob", "-30%", "+30%"], rows)

    # ---------------- What must be true ----------------
    hdr("9. WHAT MUST BE TRUE")
    mA = metrics(resA["BASE"])
    print("Plan A (what the founder can do now) reaches $%s recurring ARR at m36 in BASE (GLUT $%s, SEVERE $%s) and"
          % (k(mA["arr_36"]), k(metrics(resA["GLUT"])["arr_36"]), k(metrics(resA["SEVERE"])["arr_36"])))
    print("  %s pays the founder; it is not a venture." % ("never" if mA["ft_month"] is None else "only from m%d" % mA["ft_month"]))
    sb = summary_b["BASE"]
    print("Plan B needs $%s of outside capital (BASE) for $%s of year-10 revenue (EV ~$%s, %.2fx capital); GLUT %.2fx,"
          " SEVERE %.2fx." % (k(sb["ext"]), k(sb["rev10"]), k(sb["ev"]), sb["ev"] / sb["ext"],
                              summary_b["GLUT"]["ev"] / summary_b["GLUT"]["ext"],
                              summary_b["SEVERE"]["ev"] / summary_b["SEVERE"]["ext"]))
    print("PHASE 5 RED TEAM: KILLED. L1 (managed die-bank programs) has no rational buyer: banking bare die costs a"
          " board OEM several times the die it saves (section 10b), and board OEMs qualify packaged part numbers."
          " L3 (title-taking bank) is not bought in any scenario once burn-in/hot-cold test, bare-die storage yield,"
          " whole-wafer pulls and a blended 2.0x multiple are carried (section 10d). L4 (MCM) needs a stacked/RDL build,"
          " a 125 C bin and per-lot requalification; Plan B returns %.2fx capital in BASE and needs ~$%.0fM. Plan C is not"
          " executable by this founder. The residual (L2 rep commissions) is not this concept and does not cover its"
          " own fixed costs." % (sb["ev"] / sb["ext"], sb["ext"] / 1e6))
    print("WHAT WOULD HAVE TO BE TRUE TO REOPEN: (1) an OCM states in writing it would grant authorized-aftermarket"
          " rights (die + test-program transfer + marking) on a named EOL DDR3/DDR4 part to a new U.S. entity; (2) >=3"
          " die-consuming hybrid/SiP/MCM makers without their own vault would accept re-packaged or banked die and pay a"
          " third party; (3) a written U.S. OSAT quote for window-BGA assembly + 3-temperature test + burn-in at <=$%.2f/die"
          " all-in (the revised unit-GM break-even at m20 BASE, section 10d); (4) a hi-rel co-founder who brings an"
          " existing MCM design-in." % pull_breakeven(INPUTS)["gm0"])
    redteam_section()


if __name__ == "__main__":
    main()
