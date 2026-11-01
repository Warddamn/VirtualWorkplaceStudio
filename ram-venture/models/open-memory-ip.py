#!/usr/bin/env python3
"""DD5 - U.S. Open Memory IP: unit economics, 36-month P&L and cash curve.

Deep dive DD5 (anchor C-33, folded C-32 and C-22), agent key p4-open-memory-ip, as of 2026-11-01.

The bootstrapped business modeled month by month is the T0 wedge (C-33): a software-first memory
compiler service for U.S. open-PDK tapeouts (SkyWater sky130 via ChipFoundry / Cadence MPW, GF180MCU
via wafer.space / GF university shuttles). It has three product lines:
  A. Subscription: hosted macro generator + characterized macro library + CI regression
  B. Per-tapeout integration / sign-off service
  C. Silicon-characterized macro license with warranty (commercial / SBIR / DoD teams)
The T2 climb (C-32 gain-cell eDRAM macros, C-22 ReRAM secure-NVM on SkyWater S130) is NOT bootstrappable.
It is modeled as a separately printed funding path and overlay, never mixed into bootstrap revenue
(grants are funding, not revenue: ASSUMPTIONS A-04).

Pure Python 3 stdlib. Run from the repo root:  python3 models/open-memory-ip.py
Writes nothing; research/phase4/open-memory-ip_model_output.md holds a captured copy of stdout.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ---------------------------------------------------------------------------------------------
# DDR5 reference deck (canonical, models/dram_cost_stack.py; fallback = canonical numbers in the brief)
# ---------------------------------------------------------------------------------------------
FALLBACK_REF = dict(
    cost_component_usd_per_gb=1.48, contract_component_usd_per_gb_q4_2026=20.37,
    glut_component_usd_per_gb=8.15, severe_glut_component_usd_per_gb=2.04,
    contract_rdimm64_usd_per_user_gb_q4_2026=25.8, glut_rdimm64_usd_per_user_gb=10.3,
)
try:
    from dram_cost_stack import ddr5_reference  # noqa: E402
    REF = ddr5_reference()
    REF_SRC = "models/dram_cost_stack.py ddr5_reference()"
except Exception as exc:  # pragma: no cover - fallback path
    REF = dict(FALLBACK_REF)
    REF_SRC = "FALLBACK canonical numbers (import failed: %s)" % exc.__class__.__name__

# ---------------------------------------------------------------------------------------------
# INPUTS - every value carries a source URL or "ESTIMATE: basis"
# ---------------------------------------------------------------------------------------------
INPUTS = {}


def inp(name, value, src):
    INPUTS[name] = (value, src)
    return value


# --- Founder, timeline (ASSUMPTIONS.md) ---
START_CASH = inp("start_cash", 40_000, "ASSUMPTIONS.md A-03 ($40k deployable)")
MONTHS = inp("months", 36, "Mission: 36-month hard ceiling for PRIMARY (ASSUMPTIONS A-12)")
START_LABEL = inp("month1", (2026, 12), "ESTIMATE: month 1 = Dec-2026 (study date 2026-11-01)")
FOUNDER_FT_SALARY = inp("founder_ft_salary_month", 10_000, "ASSUMPTIONS.md A-03 (~$120k/yr loaded once revenue covers it)")
FT_CASH_BUFFER = inp("ft_cash_buffer", 25_000, "ESTIMATE: founder quits day job only with >=$25k cash on hand")
GLUT_START_MONTH = inp("glut_start_month", 14, "ASSUMPTIONS A-05 glut from 2028-Q1; month 14 = Jan-2028")

# --- Market evidence (projects per year that could buy) ---
TT_PROJECTS_2026 = inp("tinytapeout_projects_2026_sky_ihp_gf", 289 + 275 + 283 + 52,
                       "https://github.com/TinyTapeout/tinytapeout-sky-26a (289), -sky-26b (275), -ihp-26a (283), -gf-0p2 (52): git tree counts 2026-11-01; tiles are a funnel, not macro buyers")
WS_SLOTS_PER_RUN = inp("wafer_space_slots_per_run", 54, "https://github.com/wafer-space/ws-run2 (G802: 54 slots; Run 1 G801: 40)")
WS_RUNS_PER_YEAR = inp("wafer_space_runs_per_year", 2, "ESTIMATE: Run 1 wafers May-2026, Run 2 Jul-2026 tapeout, Run 3 'coming soon' (crowdsupply.com/wafer-space)")
CF_PROJECTS_PER_YEAR = inp("chipfoundry_sky130_projects_per_year", 60,
                           "ESTIMATE: 2-3 ChipFoundry shuttles/yr at >=50% fill (eeNews) ~20-30 paid slots; Efabless chipIgnite did 80 commercial designs + 50 universities over ~3 yrs (eejournal)")
CADENCE_PROJECTS_PER_YEAR = inp("cadence_sky130_mpw_projects_per_year", 30,
                                "ESTIMATE: Cadence SKY130 aggregation, $10-12k/block, 'multiple runs per year' (skywatertechnology.com Cadence MPW page, via snippet)")
GF_UNIV_PROJECTS_PER_YEAR = inp("gf_university_pilot_projects_per_year", 40,
                                "https://news.synopsys.com/2025-09-04-Synopsys-and-GlobalFoundries-Establish-Pilot-Program-to-Bring-Chip-Design-and-Manufacturing-to-University-Classrooms (40 universities, GF180MCU)")
OTHER_US_ACAD_PROJECTS = inp("mosis2_commons_other_projects_per_year", 60,
                             "ESTIMATE: MOSIS 2.0 (>35 MPW shuttles, isi.edu 2026) + Microelectronics Commons hubs (>61,000 chips, nstxl.org 2026-03) full-chip projects on U.S. trailing nodes")
MEMORY_NEED_SHARE = inp("share_projects_needing_memory_beyond_free_macros", 0.30,
                        "ESTIMATE: wafer.space Run 2 listing - ~10 of 51 projects mention SRAM/RAM (git README 2026-10-17); full SoCs need >4KB (sky130) / >1KB (GF180) which no free macro covers")
WTP_SHARE = inp("share_of_those_that_pay", 0.40, "ESTIMATE: hobby/student projects use free OpenRAM/OCD/DFFRAM; funded labs, startups, SBIR teams pay to de-risk a $7-15k slot")
GROUP_CYCLES = inp("avg_active_years_per_paying_group", 2.0, "ESTIMATE: labs/startups tape out repeatedly over a 2-3 yr grant/funding cycle")
ACAD_SHARE = inp("academic_share_of_accounts", 0.60, "ESTIMATE: wafer.space/TT listings dominated by universities and hobbyists; commercial minority")

# --- Pricing (BASE, per unit) ---
P_SUB_ACAD = inp("price_sub_academic_month", 200, "ESTIMATE: $2.4k/yr, <25% of one $7-15k shuttle slot (ChipFoundry $15k/100 chips; wafer.space ~$7k/1,000 dies)")
P_SUB_COM = inp("price_sub_commercial_month", 800, "ESTIMATE: $9.6k/yr, < one contract-engineer week; far below commercial compiler licences (Virage 0.18um from $300k list, 2001: designworldonline.com)")
P_SVC_ACAD = inp("price_tapeout_service_academic", 3_000, "ESTIMATE: ~20-40% of a $7.5-15k MPW slot")
P_SVC_COM = inp("price_tapeout_service_commercial", 10_000, "ESTIMATE: ~65-100% of a $10-15k MPW slot; buyer is de-risking the whole tapeout")
P_LIC = inp("price_characterized_macro_license", 20_000, "ESTIMATE: per design, 12-mo support + warranty; anchors: Weebit first-ever eNVM licence ~US$0.1M (MST Access), foundry-sponsored compilers free to NDA-PDK customers (Artisan model, design-reuse.com)")

# --- COGS per unit ---
CONTRACT_RATE = inp("contract_vlsi_rate_per_hour", 125, "ESTIMATE: U.S. freelance analog/memory layout & characterization engineer")
HOST_PER_ACCT = inp("hosting_per_account_month", 15, "ESTIMATE: cloud CPU for OpenRAM/ngspice/Xyce runs per active account")
SUP_H_ACAD = inp("support_hours_academic_month", 0.3, "ESTIMATE")
SUP_H_COM = inp("support_hours_commercial_month", 0.5, "ESTIMATE")
SVC_H_ACAD = inp("service_contract_hours_academic", 12, "ESTIMATE: macro generation + DRC/LVS + integration review")
SVC_H_COM = inp("service_contract_hours_commercial", 30, "ESTIMATE: custom configuration + timing sign-off + integration")
SVC_COMPUTE = inp("service_compute_per_job", 100, "ESTIMATE")
LIC_H = inp("license_contract_hours", 30, "ESTIMATE: delivery, PVT corner check, 12-mo support")
LIC_WARRANTY = inp("license_warranty_reserve_share", 0.10, "ESTIMATE: reserve for re-spin support")
PAY_FEE = inp("payment_processing_share", 0.03, "ESTIMATE: card/ACH + invoicing")

# --- Customer acquisition (BASE) ---
OUTREACH_PT = inp("outreach_contacts_month_parttime", 30, "ESTIMATE: ~4 h/week of the founder's 15 h (A-03)")
OUTREACH_FT = inp("outreach_contacts_month_fulltime", 60, "ESTIMATE")
REPLY_RATE = inp("reply_rate", 0.25, "ESTIMATE: warm, named technical outreach to public tapeout teams (wafer.space/TT repos list owners)")
CLOSE_RATE = inp("close_rate_of_replies", 0.15, "ESTIMATE: no paid demand found yet (C-33 verify: WTP STILL-UNVERIFIED) - the kill experiment measures this")
INBOUND_START = inp("inbound_start_month", 4, "ESTIMATE: after public launch of macro library on GitHub/PyPI")
INBOUND_RAMP = inp("inbound_accounts_added_per_month_per_month", 0.06, "ESTIMATE")
INBOUND_MAX = inp("inbound_accounts_max_per_month", 1.2, "ESTIMATE")
SUB_ATTACH = inp("subscription_attach_rate", 0.70, "ESTIMATE")
FIRST_SVC_ACAD = inp("first_tapeout_service_prob_academic", 0.5, "ESTIMATE")
FIRST_SVC_COM = inp("first_tapeout_service_prob_commercial", 0.6, "ESTIMATE")
TAPEOUTS_YR_ACAD = inp("tapeouts_per_year_academic_group", 1.0, "ESTIMATE: course/lab cadence")
TAPEOUTS_YR_COM = inp("tapeouts_per_year_commercial", 1.5, "ESTIMATE: 1-2 MPW spins per year")
REPEAT_SVC_ATTACH = inp("repeat_service_attach", 0.5, "ESTIMATE")
LIC_RATE_COM_YR = inp("licenses_per_commercial_account_year", 0.25, "ESTIMATE")
LIC_DOD_MONTH = inp("dod_sbir_license_channel_per_month", 0.08, "ESTIMATE: ~1/yr; precedent Sandia licensed Mobile Semiconductor 180nm compilers (design-reuse.com)")
CHURN_ACAD = inp("churn_academic_month", 0.03, "ESTIMATE: students graduate, grants end")
CHURN_COM = inp("churn_commercial_month", 0.025, "ESTIMATE: startups die or move to NDA PDK + foundry compiler")
SERVICES_START = inp("services_start_month", 4, "ESTIMATE: simulated (pre-silicon) macros sellable after 3 months of build-out, timed to the next ChipFoundry/wafer.space deadline")
GF180_CHAR_DONE = inp("gf180_characterized_month", 10, "ESTIMATE: wafer.space slot m4 + ~12 wk fab (Run 1: 12 weeks at GF) + packaging/test")
SKY130_CHAR_DONE = inp("sky130_characterized_month", 13, "ESTIMATE: ChipFoundry slot m7 + ~6-month SkyWater turn (Cadence MPW: Jan submit -> Jul die)")

# --- Operating costs ---
OPEX_FIXED = inp("opex_fixed_month", 600, "ESTIMATE: hosting base $150 + software/domain $100 + accounting/legal $350")
EO_INSURANCE = inp("e_and_o_insurance_month_after_first_license", 250, "ESTIMATE")
MKT_PT = inp("marketing_travel_month_parttime", 250, "ESTIMATE: FSiC/ORConf-type community events remote; small ads")
MKT_FT = inp("marketing_travel_month_fulltime", 1_000, "ESTIMATE: DAC/GOMACTech travel, hub events")
ONE_TIME = inp("one_time_spends", {
    1: ("company formation + templates", 1_000),
    2: ("contract VLSI build-out 20h", 2_500),
    3: ("contract VLSI build-out 40h", 5_000),
    4: ("wafer.space GF180 half slot (test macros)", 3_750),
    7: ("ChipFoundry sky130 slot (test macros)", 15_000),
    9: ("test bench: FPGA carrier + PCB + bench time", 4_000),
    10: ("GF180 characterization contractor 40h", 5_000),
    13: ("sky130 characterization contractor 40h", 5_000),
    16: ("wafer.space GF180 full slot: 8-32KB macros", 7_250),
    19: ("ChipFoundry sky130 slot: 16-64KB macros", 15_000),
    24: ("characterization contractor 40h", 5_000),
}, "ESTIMATE; slot prices: ChipFoundry ~$15k/100 chips (eeNews), wafer.space ~$7-7.5k per full slot/1,000 dies (crowdsupply Run 2), half slot = 1/2")

# --- Scenario links to the DDR5 deck ---
DEMAND_ELASTICITY = inp("commercial_demand_elasticity_to_ddr5_drop", 0.33,
                        "ESTIMATE: on-chip macros are priced per design, not per GB; a DRAM glut hits startup/tapeout budgets only through the semiconductor cycle - assume 1/3 pass-through")
PRICE_ELASTICITY = inp("commercial_price_elasticity_to_ddr5_drop", 0.15, "ESTIMATE")
CHURN_ELASTICITY = inp("commercial_churn_elasticity_to_ddr5_drop", 0.50, "ESTIMATE")
BASE_2028_DROP = inp("base_2028_ddr5_asp_drop", 0.10, "01_LANDSCAPE.md s1 row 4b (BofA -10% ASP 2028, REPORTED)")

# --- Technical context inputs (gain cell, SRAM density, $/GB) ---
SKY130_BITCELL_UM2 = inp("sky130_6t_bitcell_um2", 1.896, "https://github.com/google/skywater-pdk-libs-sky130_fd_bd_sram (1.200 x 1.580 um, VERIFIED)")
SKY130_1KB_MM2 = inp("sky130_openram_1kb_macro_mm2", 0.47978 * 0.3975, "https://github.com/efabless/sky130_sram_macros (32x256 LEF 479.78 x 397.5 um)")
SKY130_2KB_MM2 = inp("sky130_openram_2kb_macro_mm2", 0.6831 * 0.41654, "https://github.com/VLSIDA/sky130_sram_macros (683.1 x 416.54 um)")
GF180_OCD_1KB_MM2 = inp("gf180_ocd_1kb_macro_mm2", 0.3013 * 0.51581, "https://github.com/RTimothyEdwards/gf180mcu_ocd_ip_sram (1024x8 LEF 301.3 x 515.81 um)")
GF180_GF_512B_MM2 = inp("gf180_gf_512b_macro_mm2", 0.43186 * 0.48488, "https://github.com/google/globalfoundries-pdk-ip-gf180mcu_fd_ip_sram (512x8 LEF)")
LARGE_MACRO_ARRAY_EFF = inp("large_macro_array_efficiency", 0.60, "ESTIMATE: banked 32-64KB macro; typical commercial compiler 0.6-0.75")
GC_AREA_SAVING_SILICON = inp("gain_cell_bitcell_area_saving_65nm_silicon", (0.20, 0.30),
                             "https://cris.biu.ac.il/en/publications/4t-gain-cell-providing-unlimited-availability-through-hidden-refr/ (Teman group 16-kbit 65nm macros: up to 20% (2021) / 30% (2024) vs SRAM)")
GC_AREA_SAVING_CLAIM = inp("gain_cell_area_saving_vendor_claim", (0.40, 0.50),
                           "https://silicon-saxony.de/en/globalfoundries-and-raaam-memory-technologies-development-of-next-generation-gcram-technology-and-a-test-chip-on-the-fdx-platform/ (~40%); OpenGCRAM citing RAAAM up to 50% (arxiv 2507.10849)")
SRAM_130_USD_GB = inp("sram_silicon_sky130_usd_per_gb", 1_330, "01_LANDSCAPE.md s4.4 (cost_stack.md s8.5, ESTIMATE)")

# --- T2 path inputs (printed separately; not in bootstrap P&L) ---
STTR_P1 = inp("sttr_phase1_usd", 305_000, "NSF 26-510 Phase I up to $305k (grantedai.com summary; 01_LANDSCAPE s7: NSF Phase I $305k)")
STTR_P1_AWARD_MONTH = inp("sttr_phase1_award_month", 15, "ESTIMATE: submit m6-m9 with university PI, ~6-month review")
STTR_UNIV_SHARE = inp("sttr_min_research_institution_share", 0.30, "STTR rule: >=30% to the research institution (SBA policy, UNVERIFIED this session)")
STTR_FEE = inp("sttr_allowed_fee_share", 0.07, "ESTIMATE: typical 7% fee on SBIR/STTR awards")
STTR_P2 = inp("sttr_phase2_usd", 1_500_000, "ESTIMATE within ~$2.15M Phase II guideline (01_LANDSCAPE s7)")
STTR_P2_AWARD_MONTH = inp("sttr_phase2_award_month", 30, "ESTIMATE: Phase I 12 mo + ~3-mo review")
GC_EVAL_LICENSE = inp("gain_cell_eval_license_usd", 75_000, "ESTIMATE: below Weebit first-ever ~US$0.1M fee (MST Access) - a zero-heritage entrant")
GC_EVAL_MONTHS = inp("gain_cell_eval_license_months", (34,), "ESTIMATE: one eval licence after sky130 gain-cell silicon (m21-m27) and characterization; buyer = a trusted-ASIC team on SkyWater")
SEED_USD = inp("seed_round_usd", 2_500_000, "ESTIMATE: T2 seed for a memory-IP startup; conditional on wedge traction + gain-cell silicon")
SEED_MONTH = inp("seed_round_month", 28, "ESTIMATE")
FREE_SHOCK = inp("free_bundle_shock", dict(month=18, close=0.5, churn=2.0, sub_price=0.8, lic=0.5), "ESTIMATE: ChipFoundry/Cadence/UCSC/OCD ship free characterized >=16KB macros (C-33 fatal flaw); halves close rate and licences, doubles churn, -20% sub price")
RERAM_MPW_BLOCK = inp("cadence_sky130_reram_block_usd", 12_000, "https://www.skywatertechnology.com/lowering-barriers-to-silicon-cadence-launches-mpw-aggregation-service-for-sky130/ ($10-12k; upper end = ReRAM option, via snippet)")
WEEBIT_FIRST_FEE = inp("weebit_first_ever_license_fee_usd", 100_000, "MST Access report via 01_LANDSCAPE s9 (~US$0.1M first-ever licence; fabless-startup fee unknown)")
MASK_SET_130 = inp("s130_production_mask_set_usd", 550_000, "01_LANDSCAPE s6 (130nm full mask set $500-600k, AnySilicon)")
QUAL_LOTS = inp("jedec_qual_and_packaging_usd", 400_000, "C-22 verify_corrections (~$0.3-0.5M)")
COFOUNDER_LOADED = inp("circuit_cofounder_loaded_year", 220_000, "ESTIMATE: U.S. memory/mixed-signal designer, loaded")

# ---------------------------------------------------------------------------------------------
# Derived market sizing
# ---------------------------------------------------------------------------------------------
FULLCHIP_PROJECTS_YR = (WS_SLOTS_PER_RUN * WS_RUNS_PER_YEAR + CF_PROJECTS_PER_YEAR + CADENCE_PROJECTS_PER_YEAR
                        + GF_UNIV_PROJECTS_PER_YEAR + OTHER_US_ACAD_PROJECTS)
PAYING_PROJECTS_YR = FULLCHIP_PROJECTS_YR * MEMORY_NEED_SHARE * WTP_SHARE
CAP_TOTAL = PAYING_PROJECTS_YR * GROUP_CYCLES
CAP_ACAD = CAP_TOTAL * ACAD_SHARE
CAP_COM = CAP_TOTAL * (1 - ACAD_SHARE)

SCEN_DROP = {
    "BASE": BASE_2028_DROP,
    "GLUT": 1 - REF["glut_component_usd_per_gb"] / REF["contract_component_usd_per_gb_q4_2026"],
    "SEVERE": 1 - REF["severe_glut_component_usd_per_gb"] / REF["contract_component_usd_per_gb_q4_2026"],
}
SCEN_DDR5 = {
    "BASE": REF["contract_component_usd_per_gb_q4_2026"] * (1 - BASE_2028_DROP),
    "GLUT": REF["glut_component_usd_per_gb"],
    "SEVERE": REF["severe_glut_component_usd_per_gb"],
}


def month_label(m):
    y, mo = START_LABEL
    idx = (mo - 1) + (m - 1)
    return "%d-%02d" % (y + idx // 12, idx % 12 + 1)


# ---------------------------------------------------------------------------------------------
# Unit economics per product line
# ---------------------------------------------------------------------------------------------
def unit_econ(price_mult=1.0, cogs_mult=1.0, com_price_mult=1.0):
    pa, pc = P_SUB_ACAD * price_mult, P_SUB_COM * price_mult * com_price_mult
    sa, sc = P_SVC_ACAD * price_mult, P_SVC_COM * price_mult * com_price_mult
    lic = P_LIC * price_mult * com_price_mult
    rows = {
        "A1 Sub academic (/mo)": (pa, cogs_mult * (HOST_PER_ACCT + SUP_H_ACAD * CONTRACT_RATE) + PAY_FEE * pa),
        "A2 Sub commercial (/mo)": (pc, cogs_mult * (HOST_PER_ACCT + SUP_H_COM * CONTRACT_RATE) + PAY_FEE * pc),
        "B1 Tapeout svc academic": (sa, cogs_mult * (SVC_H_ACAD * CONTRACT_RATE + SVC_COMPUTE) + PAY_FEE * sa),
        "B2 Tapeout svc commercial": (sc, cogs_mult * (SVC_H_COM * CONTRACT_RATE + SVC_COMPUTE) + PAY_FEE * sc),
        "C  Characterized license": (lic, cogs_mult * (LIC_H * CONTRACT_RATE + LIC_WARRANTY * lic) + PAY_FEE * lic),
    }
    return rows


# ---------------------------------------------------------------------------------------------
# Monthly simulation
# ---------------------------------------------------------------------------------------------
def simulate(scen="BASE", price_mult=1.0, close_mult=1.0, churn_mult=1.0, cogs_mult=1.0, t2_overlay=False,
             free_shock=False):
    drop = SCEN_DROP[scen]
    base_close, base_churn = close_mult, churn_mult
    cash = START_CASH
    acad = com = 0.0
    full_time = False
    first_license_month = None
    rows = []
    for m in range(1, MONTHS + 1):
        in_glut = m >= GLUT_START_MONTH
        d_mult = (1 - DEMAND_ELASTICITY * drop) if in_glut else 1.0
        p_mult_c = (1 - PRICE_ELASTICITY * drop) if in_glut else 1.0
        ch_mult_c = (1 + CHURN_ELASTICITY * drop) if in_glut else 1.0
        shock = free_shock and m >= FREE_SHOCK["month"]
        close_mult = base_close * (FREE_SHOCK["close"] if shock else 1.0)
        churn_mult = base_churn * (FREE_SHOCK["churn"] if shock else 1.0)
        ue = unit_econ(price_mult, cogs_mult, p_mult_c)
        if shock:
            for k in ("A1 Sub academic (/mo)", "A2 Sub commercial (/mo)"):
                pr, co = ue[k]
                ue[k] = (pr * FREE_SHOCK["sub_price"], co - PAY_FEE * pr * (1 - FREE_SHOCK["sub_price"]))

        # --- acquisition ---
        contacts = OUTREACH_FT if full_time else OUTREACH_PT
        outbound = contacts * REPLY_RATE * CLOSE_RATE * close_mult if m >= 2 else 0.0
        inbound = min(INBOUND_MAX, INBOUND_RAMP * (m - INBOUND_START + 1)) * close_mult if m >= INBOUND_START else 0.0
        new_accts = (outbound + inbound) if m >= SERVICES_START else 0.0
        new_acad = new_accts * ACAD_SHARE * max(0.0, 1 - acad / CAP_ACAD)
        new_com = new_accts * (1 - ACAD_SHARE) * d_mult * max(0.0, 1 - com / CAP_COM)

        # --- churn then adds (subscriptions) ---
        acad = acad * (1 - CHURN_ACAD * churn_mult) + new_acad * SUB_ATTACH
        com = com * (1 - CHURN_COM * churn_mult * ch_mult_c) + new_com * SUB_ATTACH

        # --- services and licenses ---
        svc_a = new_acad * FIRST_SVC_ACAD + acad * TAPEOUTS_YR_ACAD / 12 * REPEAT_SVC_ATTACH
        svc_c = new_com * FIRST_SVC_COM + com * TAPEOUTS_YR_COM / 12 * REPEAT_SVC_ATTACH
        lic = 0.0
        if m >= SKY130_CHAR_DONE:
            lic = com * LIC_RATE_COM_YR / 12 + LIC_DOD_MONTH * d_mult
        elif m >= GF180_CHAR_DONE:
            lic = (com * LIC_RATE_COM_YR / 12) * 0.5  # GF180-only library: half the demand [ESTIMATE]
        if shock:
            lic *= FREE_SHOCK["lic"]
        if lic > 0 and first_license_month is None:
            first_license_month = m

        # --- revenue / COGS ---
        lines = {
            "A": (acad * ue["A1 Sub academic (/mo)"][0] + com * ue["A2 Sub commercial (/mo)"][0],
                  acad * ue["A1 Sub academic (/mo)"][1] + com * ue["A2 Sub commercial (/mo)"][1]),
            "B": (svc_a * ue["B1 Tapeout svc academic"][0] + svc_c * ue["B2 Tapeout svc commercial"][0],
                  svc_a * ue["B1 Tapeout svc academic"][1] + svc_c * ue["B2 Tapeout svc commercial"][1]),
            "C": (lic * ue["C  Characterized license"][0], lic * ue["C  Characterized license"][1]),
        }
        t2_rev = 0.0
        t2_cash = 0.0
        if t2_overlay:
            if m in GC_EVAL_MONTHS:
                t2_rev = GC_EVAL_LICENSE * price_mult
            if m == STTR_P1_AWARD_MONTH:
                t2_cash += STTR_P1 * STTR_FEE  # only the fee is free cash; the rest is spent on R&D
            if m == STTR_P2_AWARD_MONTH:
                t2_cash += STTR_P2 * STTR_FEE
            if m == 18:
                t2_cash -= RERAM_MPW_BLOCK  # ReRAM probe block paid from company cash
            if m == SEED_MONTH:
                t2_cash += SEED_USD
            if m >= SEED_MONTH + 2:
                t2_cash -= COFOUNDER_LOADED / 12
            if m == SEED_MONTH + 2:
                t2_cash -= WEEBIT_FIRST_FEE
        rev = sum(v[0] for v in lines.values()) + t2_rev
        cogs = sum(v[1] for v in lines.values()) + (0.25 * t2_rev)
        gp = rev - cogs

        # --- opex ---
        opex = OPEX_FIXED + (MKT_FT if full_time else MKT_PT)
        if first_license_month is not None and m >= first_license_month:
            opex += EO_INSURANCE
        one_time = ONE_TIME[m][1] if m in ONE_TIME else 0.0
        salary = FOUNDER_FT_SALARY if full_time else 0.0
        net = gp - opex - one_time - salary + t2_cash
        cash += net
        rows.append(dict(m=m, label=month_label(m), acad=acad, com=com, new=new_acad + new_com,
                         svc=svc_a + svc_c, lic=lic, revA=lines["A"][0], revB=lines["B"][0], revC=lines["C"][0],
                         t2=t2_rev, rev=rev, cogs=cogs, gp=gp, opex=opex, one_time=one_time, salary=salary,
                         t2_cash=t2_cash, net=net, cash=cash, ft=full_time,
                         mrr_sub=lines["A"][0], outbound=outbound, inbound=inbound))

        # --- full-time switch for next month: trailing-3 GP covers salary + FT opex and cash buffer ---
        if not full_time and m >= 3:
            gp3 = sum(r["gp"] for r in rows[-3:]) / 3
            if gp3 >= FOUNDER_FT_SALARY + OPEX_FIXED + MKT_FT + EO_INSURANCE and cash >= FT_CASH_BUFFER:
                full_time = True
    return rows


def summarize(rows):
    cash_low = min(rows, key=lambda r: r["cash"])
    be = None
    for i in range(len(rows) - 2):
        if all(rows[j]["net"] >= 0 for j in range(i, len(rows))) or all(rows[j]["net"] >= 0 for j in range(i, i + 3)):
            if rows[i]["rev"] > 0:
                be = rows[i]["m"]
                break
    ft = next((r["m"] for r in rows if r["ft"]), None)
    first_rev = next((r["m"] for r in rows if r["rev"] > 0), None)
    fte_be = next((r["m"] for r in rows if r["gp"] >= FOUNDER_FT_SALARY + OPEX_FIXED + MKT_FT + EO_INSURANCE), None)

    def arr(m):
        r = rows[m - 1]
        run = sum(x["rev"] for x in rows[max(0, m - 3):m]) / min(3, m) * 12
        return r["mrr_sub"] * 12, run
    return dict(cash_low=cash_low["cash"], cash_low_m=cash_low["m"], breakeven=be, ft=ft, first_rev=first_rev,
                fte_be=fte_be, arr={m: arr(m) for m in (12, 18, 24, 36)}, end_cash=rows[-1]["cash"],
                rev36=sum(r["rev"] for r in rows), gp36=sum(r["gp"] for r in rows),
                accts36=(rows[-1]["acad"], rows[-1]["com"]))


def money(x):
    return ("-$%sk" % format(abs(x) / 1000, ",.1f")) if x < 0 else ("$%sk" % format(x / 1000, ",.1f"))


def mo(x):
    return "never" if x is None else "m%d (%s)" % (x, month_label(x))


# ---------------------------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------------------------
def main():
    W = 108
    print("=" * W)
    print("DD5 U.S. OPEN MEMORY IP - unit economics & 36-month P&L (models/open-memory-ip.py, as of 2026-11-01)")
    print("=" * W)
    print("DDR5 reference source: %s" % REF_SRC)
    print("  incumbent cost $%.2f/GB | Q4-26 contract $%.2f/GB | glut $%.2f/GB | severe $%.2f/GB" % (
        REF["cost_component_usd_per_gb"], REF["contract_component_usd_per_gb_q4_2026"],
        REF["glut_component_usd_per_gb"], REF["severe_glut_component_usd_per_gb"]))

    # --- 1. technical context ---
    print("\n1. WHY THE AXIS IS NOT $/GB (density and $/GB context)")
    bit_kb = 1e6 / SKY130_BITCELL_UM2 / 1000  # kbit/mm2 at 100% array efficiency
    d1 = 8192 / SKY130_1KB_MM2 / 1000
    d2 = 16384 / SKY130_2KB_MM2 / 1000
    dbig = bit_kb * LARGE_MACRO_ARRAY_EFF
    g1 = 8192 / GF180_OCD_1KB_MM2 / 1000
    g5 = 4096 / GF180_GF_512B_MM2 / 1000
    print("  sky130 6T bitcell limit                    %7.1f kbit/mm2  (1.896 um2 cell)" % bit_kb)
    print("  sky130 OpenRAM 1KB / 2KB macros (largest)  %7.1f / %5.1f kbit/mm2" % (d1, d2))
    print("  sky130 banked 32-64KB macro @%.0f%% array eff %7.1f kbit/mm2  -> %.1fx the 2KB macro (compiler work, no new cell)" % (
        LARGE_MACRO_ARRAY_EFF * 100, dbig, dbig / d2))
    print("  GF180 open macros: GF 512B / OCD 1KB       %7.1f / %5.1f kbit/mm2 (largest free GF180 macro = 1KB)" % (g5, g1))
    lo, hi = GC_AREA_SAVING_SILICON
    clo, chi = GC_AREA_SAVING_CLAIM
    print("  Gain-cell density vs 6T: silicon (65nm, Teman) %.2f-%.2fx; vendor claims (RAAAM/GF) %.2f-%.2fx -> NOT the 2-4x in the hypothesis" % (
        1 / (1 - lo), 1 / (1 - hi), 1 / (1 - clo), 1 / (1 - chi)))
    print("  sky130 SRAM silicon ~$%d/GB vs DDR5: %s" % (SRAM_130_USD_GB, " | ".join(
        "%s $%.2f/GB -> %.0fx" % (s, SCEN_DDR5[s], SRAM_130_USD_GB / SCEN_DDR5[s]) for s in ("BASE", "GLUT", "SEVERE"))))
    print("  => macros are priced per design/tapeout, not per GB; the DDR5 cycle touches this only via design-start budgets.")

    # --- 2. market sizing ---
    print("\n2. MARKET SIZING (projects per year on U.S.-fab open/academic shuttles)")
    print("  Tiny Tapeout 2026 tiles (funnel only, not macro buyers): %d" % TT_PROJECTS_2026)
    print("  wafer.space %d x %d + ChipFoundry %d + Cadence MPW %d + GF univ pilot %d + MOSIS2/Commons/other %d = %d full-chip projects/yr" % (
        WS_SLOTS_PER_RUN, WS_RUNS_PER_YEAR, CF_PROJECTS_PER_YEAR, CADENCE_PROJECTS_PER_YEAR, GF_UNIV_PROJECTS_PER_YEAR,
        OTHER_US_ACAD_PROJECTS, FULLCHIP_PROJECTS_YR))
    print("  x need memory beyond free macros %.0f%% x willing to pay %.0f%% = %.0f paying projects/yr" % (
        MEMORY_NEED_SHARE * 100, WTP_SHARE * 100, PAYING_PROJECTS_YR))
    print("  active-account cap (x %.1f yr groups): academic %.0f, commercial %.0f" % (GROUP_CYCLES, CAP_ACAD, CAP_COM))
    ue0 = unit_econ()
    sam = (CAP_ACAD * ue0["A1 Sub academic (/mo)"][0] * 12 + CAP_COM * ue0["A2 Sub commercial (/mo)"][0] * 12
           + PAYING_PROJECTS_YR * (ACAD_SHARE * P_SVC_ACAD + (1 - ACAD_SHARE) * P_SVC_COM)
           + CAP_COM * LIC_RATE_COM_YR * P_LIC + LIC_DOD_MONTH * 12 * P_LIC)
    print("  => serviceable revenue ceiling of the wedge at full share: %s/yr (subscriptions + services + licenses)" % money(sam))

    # --- 3. unit economics ---
    print("\n3. UNIT ECONOMICS PER PRODUCT LINE (BASE prices)")
    print("  %-28s %10s %10s %8s" % ("Product line", "Price", "COGS", "GM"))
    for k, (p, c) in ue0.items():
        print("  %-28s %10s %10s %7.0f%%" % (k, "$%s" % format(p, ",.0f"), "$%s" % format(c, ",.0f"), 100 * (p - c) / p))
    gpa = ue0["A1 Sub academic (/mo)"][0] - ue0["A1 Sub academic (/mo)"][1]
    gpc = ue0["A2 Sub commercial (/mo)"][0] - ue0["A2 Sub commercial (/mo)"][1]
    ltv_a = gpa / CHURN_ACAD + FIRST_SVC_ACAD * (ue0["B1 Tapeout svc academic"][0] - ue0["B1 Tapeout svc academic"][1])
    ltv_c = gpc / CHURN_COM + FIRST_SVC_COM * (ue0["B2 Tapeout svc commercial"][0] - ue0["B2 Tapeout svc commercial"][1])
    new_pt = OUTREACH_PT * REPLY_RATE * CLOSE_RATE
    cac_cash = MKT_PT / new_pt
    cac_loaded = (MKT_PT + 16 * 75) / new_pt
    print("  Lifetime GP: academic sub %s (life %.0f mo) | commercial sub %s (life %.0f mo), incl. first tapeout service" % (
        money(ltv_a), 1 / CHURN_ACAD, money(ltv_c), 1 / CHURN_COM))
    print("  Acquisition: %d contacts/mo x %.0f%% reply x %.0f%% close = %.2f outbound accounts/mo part-time (+ inbound ramp to %.1f/mo)" % (
        OUTREACH_PT, REPLY_RATE * 100, CLOSE_RATE * 100, new_pt, INBOUND_MAX))
    print("  CAC: cash %s/account; loaded with 16 founder h/mo @ $75/h = %s/account -> LTV/CAC (blended %.0f%% acad) %.1fx" % (
        money(cac_cash), money(cac_loaded), ACAD_SHARE * 100,
        (ACAD_SHARE * ltv_a + (1 - ACAD_SHARE) * ltv_c) / cac_loaded))

    # --- 4. scenarios ---
    res = {}
    print("\n4. SCENARIOS (bootstrap wedge only; month 1 = %s; glut from m%d = %s)" % (
        month_label(1), GLUT_START_MONTH, month_label(GLUT_START_MONTH)))
    for s in ("BASE", "GLUT", "SEVERE"):
        print("  %-6s DDR5 drop %.0f%% -> commercial demand x%.2f, commercial price x%.2f, commercial churn x%.2f" % (
            s, SCEN_DROP[s] * 100, 1 - DEMAND_ELASTICITY * SCEN_DROP[s], 1 - PRICE_ELASTICITY * SCEN_DROP[s],
            1 + CHURN_ELASTICITY * SCEN_DROP[s]))
    for s in ("BASE", "GLUT", "SEVERE"):
        rows = simulate(s)
        res[s] = (rows, summarize(rows))

    rows = res["BASE"][0]
    print("\n5. MONTHLY P&L AND CASH - BASE (accounts are expected values)")
    hdr = "  %-4s %-7s %5s %5s %5s %5s %8s %8s %8s %8s %8s %7s %8s %9s %3s" % (
        "m", "month", "acad", "com", "svc", "lic", "rev A", "rev B", "rev C", "revenue", "GP", "opex", "one-time", "cash", "FT")
    print(hdr)
    for r in rows:
        print("  %-4d %-7s %5.1f %5.1f %5.2f %5.2f %8s %8s %8s %8s %8s %7s %8s %9s %3s" % (
            r["m"], r["label"], r["acad"], r["com"], r["svc"], r["lic"], money(r["revA"]), money(r["revB"]), money(r["revC"]),
            money(r["rev"]), money(r["gp"]), money(r["opex"] + r["salary"]), money(r["one_time"]), money(r["cash"]),
            "Y" if r["ft"] else "-"))

    print("\n6. SCENARIO SUMMARY")
    print("  %-7s %9s %10s %16s %16s %14s %10s %10s %10s %10s %10s" % (
        "scen", "1st rev", "cash low", "3-mo CF+ from", "founder FT", "GM (36 mo)", "ARR m12", "ARR m18", "ARR m24", "ARR m36", "end cash"))
    for s in ("BASE", "GLUT", "SEVERE"):
        sm = res[s][1]
        print("  %-7s %9s %10s %16s %16s %13.0f%% %10s %10s %10s %10s %10s" % (
            s, "m%d" % sm["first_rev"], "%s@m%d" % (money(sm["cash_low"]), sm["cash_low_m"]), mo(sm["breakeven"]), mo(sm["ft"]),
            100 * sm["gp36"] / sm["rev36"], money(sm["arr"][12][0]), money(sm["arr"][18][0]), money(sm["arr"][24][0]),
            money(sm["arr"][36][0]), money(sm["end_cash"])))
    print("  ARR = subscription MRR x 12 (recurring only). Revenue run-rate (last 3 months x 4) incl. services/licenses:")
    for s in ("BASE", "GLUT", "SEVERE"):
        sm = res[s][1]
        print("  %-7s run-rate m12 %s | m18 %s | m24 %s | m36 %s | 36-mo revenue %s | accounts at m36: %.0f acad + %.0f com" % (
            s, money(sm["arr"][12][1]), money(sm["arr"][18][1]), money(sm["arr"][24][1]), money(sm["arr"][36][1]),
            money(sm["rev36"]), sm["accts36"][0], sm["accts36"][1]))

    # --- 7. sensitivity ---
    print("\n7. SENSITIVITY (BASE scenario, one input at a time)")
    print("  %-22s %12s %16s %16s %10s %10s %10s" % ("case", "cash low", "3-mo CF+ from", "founder FT", "ARR m18", "ARR m36", "rev m36 RR"))
    cases = [("base", {})]
    for lab, key in (("price", "price_mult"), ("close rate", "close_mult"), ("churn", "churn_mult"), ("COGS", "cogs_mult")):
        for f in (0.7, 1.3):
            cases.append(("%s x%.1f" % (lab, f), {key: f}))
    for lab, kw in cases:
        sm = summarize(simulate("BASE", **kw))
        print("  %-22s %12s %16s %16s %10s %10s %10s" % (lab, money(sm["cash_low"]), mo(sm["breakeven"]), mo(sm["ft"]),
                                                      money(sm["arr"][18][0]), money(sm["arr"][36][0]), money(sm["arr"][36][1])))
    for lab, sc in (("FREE-BUNDLE shock m18", "BASE"), ("GLUT + free shock", "GLUT")):
        sm = summarize(simulate(sc, free_shock=True))
        print("  %-22s %12s %16s %16s %10s %10s %10s" % (lab, money(sm["cash_low"]), mo(sm["breakeven"]), mo(sm["ft"]),
                                                      money(sm["arr"][18][0]), money(sm["arr"][36][0]), money(sm["arr"][36][1])))
    worst = summarize(simulate("SEVERE", price_mult=0.7, close_mult=0.7, churn_mult=1.3, cogs_mult=1.3))
    print("  %-22s %12s %16s %16s %10s %10s %10s" % ("SEVERE + all adverse", money(worst["cash_low"]), mo(worst["breakeven"]),
                                                  mo(worst["ft"]), money(worst["arr"][18][0]), money(worst["arr"][36][0]),
                                                  money(worst["arr"][36][1])))

    # --- 8. what must be true ---
    print("\n8. WHAT MUST BE TRUE")
    need_gp = FOUNDER_FT_SALARY + OPEX_FIXED + MKT_FT + EO_INSURANCE
    gp_svc_c = ue0["B2 Tapeout svc commercial"][0] - ue0["B2 Tapeout svc commercial"][1]
    gp_svc_a = ue0["B1 Tapeout svc academic"][0] - ue0["B1 Tapeout svc academic"][1]
    gp_lic = ue0["C  Characterized license"][0] - ue0["C  Characterized license"][1]
    # monthly GP per "account bundle" at the base mix: subscription + repeat services + licenses
    per_a = gpa + TAPEOUTS_YR_ACAD / 12 * REPEAT_SVC_ATTACH * gp_svc_a
    per_c = gpc + TAPEOUTS_YR_COM / 12 * REPEAT_SVC_ATTACH * gp_svc_c + LIC_RATE_COM_YR / 12 * gp_lic
    blended = ACAD_SHARE * per_a + (1 - ACAD_SHARE) * per_c
    need_accts = need_gp / blended
    b18 = rows[17]
    print("  To pay the founder full-time ($%sk/mo) + FT opex from gross profit needs %s GP/month." % (
        format(FOUNDER_FT_SALARY / 1000, ".0f"), money(need_gp)))
    print("  At the base mix one active account yields %s GP/mo (academic %s, commercial %s)." % (money(blended), money(per_a), money(per_c)))
    print("  => ~%.0f active paying accounts (~%.0f academic + %.0f commercial) by month 18; model has %.1f + %.1f = %.1f at m18." % (
        need_accts, need_accts * ACAD_SHARE, need_accts * (1 - ACAD_SHARE), b18["acad"], b18["com"], b18["acad"] + b18["com"]))
    print("  => that is %.0f%% of the whole wedge cap (%.0f accounts) - i.e. near-total share of a tiny market." % (
        100 * need_accts / CAP_TOTAL, CAP_TOTAL))
    print("  Equivalently (no subscriptions): %.1f commercial tapeout services/mo or %.1f licenses/mo." % (
        need_gp / gp_svc_c, need_gp / gp_lic))
    print("  Kill line for the 30-day experiment: >=3 paid pre-orders (>=$2k each) or >=$15k in signed LOIs from the outreach list.")

    # --- 9. T2 path ---
    print("\n9. PATH TO T2 (gain-cell + ReRAM macros) - funding, not revenue (A-04)")
    t2 = [
        ("m6-m9", "STTR Phase I proposal with university PI (e.g. UCSC OpenRAM / Stanford OpenGCRAM group)", 0, "founder time"),
        ("m%d" % STTR_P1_AWARD_MONTH, "STTR Phase I award: sky130 gain-cell macro + test chip", STTR_P1, "NSF/DoD STTR"),
        ("m15-m21", "  of which >=%.0f%% to university; 2 ChipFoundry sky130 spins" % (STTR_UNIV_SHARE * 100), 2 * 15_000, "inside Phase I"),
        ("m18", "ReRAM probe: Cadence SKY130 MPW block with Weebit ReRAM option", RERAM_MPW_BLOCK, "Phase I / cash"),
        ("m18-m24", "Weebit evaluation/licence (first-ever fee anchor; startup fee unknown)", WEEBIT_FIRST_FEE, "seed or Phase II"),
        ("m%d" % STTR_P2_AWARD_MONTH, "STTR Phase II: characterization, compiler, reliability", STTR_P2, "NSF/DoD STTR"),
        ("m27-m30", "Seed round, conditional on >=$250k ARR wedge + gain-cell silicon", 2_500_000, "VC / strategic (SkyWater/IonQ?)"),
        ("m30-m48", "Full-time circuit cofounder (2 yrs loaded)", 2 * COFOUNDER_LOADED, "seed"),
        ("m36-m54", "ReRAM secure-NVM chiplet: S130 mask set + JEDEC qual + packaging", MASK_SET_130 + QUAL_LOTS, "seed / Phase II / DoD"),
    ]
    for when, what, usd, who in t2:
        print("  %-8s %-82s %10s  %s" % (when, what, money(usd) if usd else "-", who))
    tot = STTR_P1 + STTR_P2 + 2_500_000
    print("  Total external capital to reach a qualified macro: ~%s (T2). Product revenue from gain-cell/ReRAM before m36: at most %d gain-cell eval licence(s)." % (
        money(tot), len(GC_EVAL_MONTHS)))
    ov = summarize(simulate("BASE", t2_overlay=True))
    print("  BASE + T2 overlay (STTR fees, ReRAM MPW block, %d gain-cell eval licence @ %s, seed %s at m%d, cofounder + Weebit fee):" % (
        len(GC_EVAL_MONTHS), money(GC_EVAL_LICENSE), money(SEED_USD), SEED_MONTH))
    print("    36-mo revenue %s (wedge %s + T2 %s) | end cash %s, of which seed %s -> operating cash excl. seed %s (vs BASE wedge %s)." % (
        money(ov["rev36"]), money(ov["rev36"] - GC_EVAL_LICENSE * len(GC_EVAL_MONTHS)), money(GC_EVAL_LICENSE * len(GC_EVAL_MONTHS)),
        money(ov["end_cash"]), money(SEED_USD), money(ov["end_cash"] - SEED_USD),
        money(summarize(simulate("BASE"))["end_cash"])))

    # --- 10. headline ---
    b = res["BASE"][1]
    g = res["GLUT"][1]
    sv = res["SEVERE"][1]
    print("\n10. HEADLINE")
    print("  36-mo gross margin %.0f%% (base). Cash-flow breakeven (first of 3 cash-positive months) %s; founder can go full-time %s." % (
        100 * b["gp36"] / b["rev36"], mo(b["breakeven"]), mo(b["ft"])))
    print("  Recurring ARR m18 / m36: BASE %s / %s | GLUT %s / %s | SEVERE %s / %s" % (
        money(b["arr"][18][0]), money(b["arr"][36][0]), money(g["arr"][18][0]), money(g["arr"][36][0]),
        money(sv["arr"][18][0]), money(sv["arr"][36][0])))
    print("  Revenue run-rate m18 / m36: BASE %s / %s | GLUT %s / %s | SEVERE %s / %s" % (
        money(b["arr"][18][1]), money(b["arr"][36][1]), money(g["arr"][18][1]), money(g["arr"][36][1]),
        money(sv["arr"][18][1]), money(sv["arr"][36][1])))
    print("  Cash low point BASE %s at m%d (starting from %s)." % (money(b["cash_low"]), b["cash_low_m"], money(START_CASH)))

    print("\nINPUTS (value | source)")
    for k, (v, src) in INPUTS.items():
        if isinstance(v, dict) and all(isinstance(x, tuple) for x in v.values()):
            v = "; ".join("m%d %s $%s" % (m, d, format(c, ",")) for m, (d, c) in v.items())
        print("  %-52s %s | %s" % (k, v, src))
    return 0


if __name__ == "__main__":
    sys.exit(main())
