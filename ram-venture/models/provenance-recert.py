#!/usr/bin/env python3
"""
models/provenance-recert.py -- DD1 "Provenance & Recertified Memory" (agent p4-provenance-recert, 2026-11-01)

Unit economics and a 36-month monthly P&L / cash curve for the bundle:
  C-62  ProvenRAM recert   : buy decommissioned DDR4/DDR5 RDIMM lots, test, grade, serialize, resell (cash engine)
  C-26  Optane PMem salvage: a SKU of the recert line (sunsets with vSphere 8, 2027-10-11)
  C-64  CleanBOM-5949      : provenance subscription + per-SKU evidence packs + die-ID lab pass-through
  C-85  DIMM-health        : rasdaemon/EDAC predictive replacement subscription, spares drawn from recert stock

Scenarios: BASE (2026-27 prices hold, soft turn in 2028), GLUT (A-05: -60% over 2028), SEVERE ($2.04/GB deck).
Pure Python 3 stdlib. Run from the repo root:  python3 models/provenance-recert.py   (exits 0)
Every INPUT carries a source URL or "ESTIMATE: basis". Snippet-grade sources are listed in
research/sources/p4-provenance-recert.jsonl; judgment calls in research/assumptions/p4-provenance-recert.md.
"""
import contextlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ----------------------------------------------------------------------------------------------
# DDR5 reference deck (canonical numbers from models/dram_cost_stack.py; fallback if import fails)
# ----------------------------------------------------------------------------------------------
CANONICAL = {
    "cost_component_usd_per_gb": 1.48,
    "contract_component_usd_per_gb_q4_2026": 20.37,
    "glut_component_usd_per_gb": 8.15,
    "severe_glut_component_usd_per_gb": 2.04,
    "contract_rdimm64_usd_per_user_gb_q4_2026": 25.8,
    "glut_rdimm64_usd_per_user_gb": 10.3,
}


def load_ref():
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            from dram_cost_stack import ddr5_reference  # noqa: E402
            ref = ddr5_reference()
        for k, v in CANONICAL.items():
            ref.setdefault(k, v)
        return ref, "models/dram_cost_stack.py ddr5_reference() (live import)"
    except Exception as exc:  # pragma: no cover - fallback path
        return dict(CANONICAL), "canonical fallback numbers (import failed: %s)" % exc.__class__.__name__


REF, REF_SRC = load_ref()
CONTRACT = REF["contract_component_usd_per_gb_q4_2026"]
GLUT_RATIO = REF["glut_component_usd_per_gb"] / CONTRACT        # ~0.40
SEVERE_RATIO = REF["severe_glut_component_usd_per_gb"] / CONTRACT  # ~0.10
NEW_RDIMM64_PER_GB = REF["contract_rdimm64_usd_per_user_gb_q4_2026"]

# ----------------------------------------------------------------------------------------------
# INPUTS  (value, source).  "ESTIMATE: ..." = my assumption with its basis.
# ----------------------------------------------------------------------------------------------
AMC = "https://www.amcompute.com/appraisals/"
INPUTS = {
    # --- founder, cash, timeline -----------------------------------------------------------------
    "start_cash": (40_000, "ASSUMPTIONS.md A-03: $40k deployable"),
    "months": (36, "Mission: 36-month hard ceiling; month 1 = Nov-2026, month 36 = Oct-2029"),
    "reserve_cash": (5_000, "ESTIMATE: minimum cash buffer kept before buying inventory"),
    "turn_month": (15, "01_LANDSCAPE §0 item 4: downturn most likely begins 2028 -> month 15 = Jan-2028"),
    # --- price paths ------------------------------------------------------------------------------
    "base_2028_decline": (0.10, "01_LANDSCAPE §1 row 4b: BofA -10% DRAM ASP in 2028 (TMGM/Baird; KuCoin)"),
    "base_2029_decline": (0.10, "ESTIMATE: continued soft decline Jan-Oct 2029 in BASE"),
    "glut_ramp_months": (12, "01_LANDSCAPE §1 row 4a: 2018-19 8GB module -62.5% in ~4 quarters"),
    "used_floor_per_gb": (1.00, "research/phase2/C_notes.md App. A '2023-like $1/GB' used RDIMM trough (ESTIMATE)"),
    # --- recert SKUs (realized used resale, 12 months to Aug-2026) -------------------------------------
    "ddr4_32_price": (125.0, AMC + "ddr4-32gb-rdimm  ($100-150 midpoint; via search snippet)"),
    "ddr4_64_price": (310.0, AMC + "ddr4-64gb-rdimm  ($250-370 midpoint; via search snippet)"),
    "ddr5_64_price": (1045.0, AMC + "ddr5-64gb-rdimm  ($890-1,200 midpoint; via search snippet)"),
    "mix_ddr4_32": (0.60, "ESTIMATE: DDR4 dominates 2026 decommission flow (C_notes §6)"),
    "mix_ddr4_64": (0.30, "ESTIMATE: as above"),
    "mix_ddr5_64": (0.10, "ESTIMATE: used DDR5 supply thin (01_LANDSCAPE 1b item 4)"),
    "buy_frac": (0.65, "ESTIMATE: 01_LANDSCAPE O3 uses 0.60 and flags it optimistic (Iron Mountain ALM keeps the "
                       "repricing, MarketBeat Q2-26); PCSP lot of 24x32GB listed ~$140/module ~= resale"),
    "b2b_price_factor": (0.88, "ESTIMATE: TPM/refurbisher volume buyers pay below single-unit eBay realized"),
    "ebay_fee_pct": (0.136, "https://litcommerce.com/ebay-fee-calculator/ (13.6% Selected Computer Hardware; "
                            "10.9% elsewhere -> conservative)"),
    "ebay_fee_per_order": (0.40, "https://litcommerce.com/ebay-fee-calculator/ ($0.30-0.40 per order)"),
    "b2b_fee_pct": (0.03, "research/phase2/C_notes.md App. A (payment processing)"),
    "ship_ebay": (5.0, "research/phase2/C_notes.md App. A"),
    "ship_b2b": (1.5, "research/phase2/C_notes.md App. A"),
    "ebay_share_start": (0.70, "ESTIMATE: eBay first, B2B accounts take months"),
    "ebay_share_m12": (0.40, "ESTIMATE: 3-5 B2B accounts (xByte, TechMikeNY, PCSP, TPM spares desks) by month 12"),
    "fail_rate": (0.03, "research/phase2/C_notes.md App. A (test fallout written off)"),
    "return_rate": (0.02, "research/phase2/C_notes.md App. A; 1-yr warranty (channel norm 90 d to lifetime: "
                          "Reboot IT, Rimlance listings)"),
    "consumables": (1.0, "ESTIMATE: ESD bag, serialized label, box per module"),
    "minutes_per_module": (12.0, "ESTIMATE: C_notes 6 min test + receive/SPD-log/label/photo/list/pack"),
    "tech_rate": (25.0, "ESTIMATE: East Coast part-time technician, loaded $/h"),
    "founder_ops_hours_pt": (35.0, "ESTIMATE: ~8 of A-03's 15 h/week on ops"),
    "founder_ops_hours_ft": (60.0, "ESTIMATE: full-time founder's ops share"),
    "recert_start": (2, "ESTIMATE: first ITAD lot bought month 2, sold month 3 (C-62 card: 2-4 months)"),
    "units_step": (40, "ESTIMATE: +40 modules/month ramp"),
    "units_cap_pt": (400, "ESTIMATE: channel absorption part-time (eBay + 3-5 B2B accounts)"),
    "units_cap_ft": (600, "ESTIMATE: channel absorption full-time (~$150k/mo of ITAD lots to source)"),
    "glut_volume_floor": (0.50, "ESTIMATE: used-RDIMM channel volume falls to 50% of cap at the glut price "
                                "(new DDR5 servers become the cheaper upgrade); linear in the price index"),
    "min_margin_to_buy": (0.05, "ESTIMATE: stop buying when expected contribution < 5% of price"),
    "maintenance_buy_frac": (0.10, "ESTIMATE: keep a trickle for spares/library when buying stops"),
    "space_trigger_units": (250, "ESTIMATE: garage -> flex space above 250 modules/month"),
    # --- Optane PMem SKU (C-26) --------------------------------------------------------------------
    "pmem_price": (200.0, "ESTIMATE from listings: new 128GB PMem 200 ~US$290 (ebay.de/itm/204762258263, undated); "
                          "C-26 card $65-380 used 128GB; 2019 list $695 (Tom's Hardware)"),
    "pmem_buy_frac": (0.55, "ESTIMATE: C-26 card 20-35% GM"),
    "pmem_units": (25, "ESTIMATE: ~10% of the >=200/month market the C-26 kill test asks for"),
    "pmem_start": (3, "ESTIMATE"),
    "pmem_post_vmware": (0.40, "Broadcom KB 459135 (vSphere 8 EoGS 2027-10-11) + KB 326910 (VCF 9 drops PMem)"),
    "pmem_vmware_month": (13, "vSphere 8 EoGS 2027-10-11 -> from month 13 (Nov-2027)"),
    # --- CleanBOM-5949 (C-64) --------------------------------------------------------------------
    "cb_launch": (10, "ESTIMATE: Aug-2027; C-64 verify: buyers wait for final FAR rule (proposed 2026-02-17, "
                      "federalregister.gov 2026-03065); Sec.805 indirect ban 2027-06-30 (Crowell)"),
    "cb_conv_pt": (5.0, "ESTIMATE: qualified conversations/month, part-time founder"),
    "cb_conv_ft": (12.0, "ESTIMATE: qualified conversations/month, full-time founder"),
    "cb_close_bundle": (0.10, "ESTIMATE: untested; 01_LANDSCAPE O1 kill threshold is 3 of 10 'would pay'"),
    "cb_close_standalone": (0.07, "ESTIMATE: thinner die-source evidence without recert flow (the bundle hypothesis)"),
    "cb_lo_price": (750.0, "ESTIMATE: integrator/reseller tier; below SiliconExpert-class ACV (Accuris offer "
                           "floor $6k/yr, accuristech.com/siliconexpert-offer-terms)"),
    "cb_hi_price": (2500.0, "ESTIMATE: module maker/ODM die-source tier; C-64 card $1.5-12k/mo cut for safe harbor"),
    "cb_hi_share": (0.35, "ESTIMATE: share of customers on the high tier"),
    "cb_churn": (0.02, "ESTIMATE: SMB B2B SaaS monthly churn"),
    "cb_pack_rate": (0.15, "ESTIMATE: share of conversations buying a one-off evidence pack"),
    "cb_pack_price": (900.0, "ESTIMATE: per-SKU-family attestation + SPD scan + cross-reference report"),
    "cb_samples_per_sub": (0.4, "ESTIMATE: die-ID samples ordered per subscriber-month"),
    "lab_cost": (400.0, "ESTIMATE: X-ray+decap+die photo; blog ranges $50-500/component, SEM $150-500/sample "
                        "(industrialmonitordirect.com, weak); 26 ANAB AS6171 labs (blog.ansi.org)"),
    "lab_markup": (1.6, "ESTIMATE: handling + interpretation"),
    "cb_sw_cogs_pct": (0.12, "ESTIMATE: hosting, data, support as % of software revenue"),
    "lib_samples_early": (3.0, "ESTIMATE: die-source library samples/month, months 4-18"),
    "lib_samples_late": (1.0, "ESTIMATE: library upkeep samples/month after month 18"),
    "lib_module_cost": (150.0, "ESTIMATE: standalone must buy each sample module (bundle gets it from recert)"),
    # --- DIMM-health (C-85) ----------------------------------------------------------------------
    "dh_launch": (12, "ESTIMATE: Oct-2027 (agent + console build, C-85 verify: 6-12 months part-time)"),
    "dh_new_pt": (0.15, "ESTIMATE: new customers/month part-time (slow university/colo procurement)"),
    "dh_new_ft": (0.35, "ESTIMATE: new customers/month full-time"),
    "dh_dimms": (1200, "ESTIMATE: 100 out-of-warranty servers x 12 DIMMs (card used 2,400)"),
    "dh_price": (0.60, "ESTIMATE: below card $0.75 because Lenovo MPFA (lenovopress.lenovo.com/lp2326), Intel MFP "
                       "in AMI/Insyde BMC, Park Place ParkView already predict DIMM failures"),
    "dh_repl_rate": (0.015, "C-85 card ESTIMATE; Google 'DRAM errors in the wild' ~8% DIMMs/yr see errors"),
    "dh_ship": (18.0, "C-85 card (E_notes §10)"),
    "dh_host": (0.05, "C-85 card: hosting/support $/DIMM-month"),
    "dh_pool_frac": (0.02, "C-85 card: spares pool as % of covered DIMMs"),
    "dh_carry": (0.20, "C-85 card: carrying + obsolescence per year on pool"),
    "dh_churn": (0.015, "ESTIMATE: monthly churn"),
    "dh_churn_glut": (0.035, "ESTIMATE: churn after Jan-2028 in GLUT/SEVERE (cheap DDR5 refresh, C-85 verify)"),
    "dh_swap_hours": (0.5, "ESTIMATE: pick, label, ship per swap"),
    # --- opex, capex, people ------------------------------------------------------------------------
    "opex_tools": (150.0, "ESTIMATE: hosting, eBay store, label software"),
    "opex_tools_cb": (350.0, "ESTIMATE: added SaaS hosting/monitoring once CleanBOM live"),
    "opex_insurance": (200.0, "ESTIMATE: GL + product liability"),
    "opex_eo": (400.0, "ESTIMATE: E&O for attestations (False Claims Act-adjacent exposure, C-64 scorers)"),
    "opex_books": (150.0, "ESTIMATE: bookkeeping"),
    "opex_marketing": (300.0, "ESTIMATE: listings promotion, samples"),
    "opex_space": (1500.0, "ESTIMATE: East Coast flex space"),
    "legal_setup": (2500.0, "ESTIMATE: LLC, terms, 'used/recertified' disclosure (18 USC 2320, C_notes §6)"),
    "legal_cb": (6000.0, "ESTIMATE: attestation templates, liability caps, before CleanBOM launch"),
    "cb_launch_marketing": (3000.0, "ESTIMATE: federal-reseller events / SEWP vendor days"),
    "cert_iso": (10000.0, "ESTIMATE: ISO 9001/AS6081 readiness; AS9120 proxy $6-12k (amtivo.com); NQA sole "
                          "AS6081 CB (nqa.com)"),
    "cert_iso_month": (15, "ESTIMATE"),
    "cert_surv": (3000.0, "ESTIMATE: surveillance audit month 27"),
    "capex_m1": (4200.0, "ESTIMATE: 2 used Gen10 DDR4 servers w/o memory + ESD bench + label printer"),
    "capex_ddr5": (4000.0, "ESTIMATE: used DDR5 (Sapphire Rapids) test platform, month 6"),
    "capex_cb_only": (1500.0, "ESTIMATE: SPD scan rig for a standalone CleanBOM"),
    "founder_salary": (10000.0, "ASSUMPTIONS.md A-03: ~$120k/yr loaded once revenue covers it"),
    "ft_trigger_ebitda": (12000.0, "ESTIMATE: trailing-3-month EBITDA (pre-salary) to quit the day job"),
    "ft_trigger_cash": (25000.0, "ESTIMATE: cash needed to go full-time"),
    "ft_revert_cash": (8000.0, "ESTIMATE: back to the day job below this cash"),
    "founder_hour_value": (75.0, "ESTIMATE: imputed founder time for CAC only (never cash)"),
    "hours_per_conversation": (3.0, "ESTIMATE: prospecting + call + follow-up"),
}
P0 = {k: v[0] for k, v in INPUTS.items()}
M = P0["months"]
SCENARIOS = ("BASE", "GLUT", "SEVERE")
ALL_LINES = ("recert", "pmem", "cb", "dh")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def label(m):
    z = 10 + m - 1                       # month 1 = Nov-2026
    return "%s-%02d" % (MONTHS[z % 12], (2026 + z // 12) % 100)


def skus(p):
    return [("DDR4 32GB", 32, p["ddr4_32_price"], p["mix_ddr4_32"]),
            ("DDR4 64GB", 64, p["ddr4_64_price"], p["mix_ddr4_64"]),
            ("DDR5 64GB", 64, p["ddr5_64_price"], p["mix_ddr5_64"])]


# ----------------------------------------------------------------------------------------------
# Price index for used modules by scenario (1.0 = trailing-12-month realized resale)
# ----------------------------------------------------------------------------------------------
def price_index(scn, m, p):
    t = p["turn_month"]
    if m < t:
        return 1.0
    if scn == "BASE":
        if m <= t + 11:
            return 1.0 - p["base_2028_decline"] * (m - t + 1) / 12.0
        return (1.0 - p["base_2028_decline"]) - p["base_2029_decline"] * (m - t - 11) / 10.0
    target = GLUT_RATIO if scn == "GLUT" else SEVERE_RATIO
    k = min(1.0, (m - t + 1) / float(p["glut_ramp_months"]))
    return 1.0 - (1.0 - target) * k


def sku_price(p, base_price, gb, idx):
    return max(base_price * idx * p.get("_recert_price_mult", 1.0), p["used_floor_per_gb"] * gb)


def ebay_share(p, m):
    if m >= 12:
        return p["ebay_share_m12"]
    return p["ebay_share_start"] + (p["ebay_share_m12"] - p["ebay_share_start"]) * (m - 1) / 11.0


def recert_unit(p, idx_sell, idx_buy, es):
    """Per GOOD module sold: revenue, buy (incl. fallout), fees, ship, consumables, returns, labor, contribution."""
    cm = p.get("_cogs_mult", 1.0)
    rev = buy = fees = ship = 0.0
    for _, gb, base, share in skus(p):
        ps = sku_price(p, base, gb, idx_sell)
        pb = sku_price(p, base, gb, idx_buy)
        r_e, r_b = ps, ps * p["b2b_price_factor"]
        rev += share * (es * r_e + (1 - es) * r_b)
        fees += share * (es * (r_e * p["ebay_fee_pct"] * cm + p["ebay_fee_per_order"])
                         + (1 - es) * r_b * p["b2b_fee_pct"] * cm)
        ship += share * (es * p["ship_ebay"] + (1 - es) * p["ship_b2b"])
        buy += share * p["buy_frac"] * cm * pb
    buy_good = buy / (1 - p["fail_rate"])            # fallout cost carried by good units
    ret = rev * p["return_rate"]
    labor = p["minutes_per_module"] / 60.0 * p["tech_rate"] / (1 - p["fail_rate"])
    cons = p["consumables"]
    contrib = rev - buy_good - fees - ship - ret - cons - labor
    return dict(rev=rev, buy=buy_good, buy_raw=buy, fees=fees, ship=ship, ret=ret, cons=cons, labor=labor,
                contrib=contrib, gm=contrib / rev if rev else 0.0)


def pmem_unit(p, idx):
    cm = p.get("_cogs_mult", 1.0)
    price = p["pmem_price"] * idx * p.get("_recert_price_mult", 1.0)
    buy = p["pmem_buy_frac"] * cm * price
    fees = price * p["ebay_fee_pct"] * cm + p["ebay_fee_per_order"]
    labor = 15.0 / 60.0 * p["tech_rate"]
    c = price - buy - fees - p["ship_ebay"] - price * p["return_rate"] - p["consumables"] - labor
    return dict(rev=price, buy=buy, fees=fees, labor=labor, contrib=c, gm=c / price if price else 0.0)


def spare_cost(p, idx, bundled):
    """Cost of one tested 32GB DDR4 spare for the DIMM-health pool."""
    cm = p.get("_cogs_mult", 1.0)
    px = sku_price(p, p["ddr4_32_price"], 32, idx)
    if bundled:   # pulled from recert stock at buy cost + test labor
        return p["buy_frac"] * cm * px / (1 - p["fail_rate"]) + p["minutes_per_module"] / 60.0 * p["tech_rate"]
    return px * 1.0 + p["ship_ebay"]   # standalone buys spares retail


def cb_arpa(p):
    sp = p.get("_saas_price_mult", 1.0)
    return sp * ((1 - p["cb_hi_share"]) * p["cb_lo_price"] + p["cb_hi_share"] * p["cb_hi_price"])


# ----------------------------------------------------------------------------------------------
# Monthly simulation
# ----------------------------------------------------------------------------------------------
def simulate(scn, p, lines=ALL_LINES):
    cm = p.get("_cogs_mult", 1.0)
    sp = p.get("_saas_price_mult", 1.0)
    close_mult = p.get("_close_mult", 1.0)
    churn_mult = p.get("_churn_mult", 1.0)
    cb_launch = p["cb_launch"] + p.get("_cb_delay", 0)
    bundled = "recert" in lines
    cash = float(p["start_cash"])
    ft = False
    inv_units, inv_cost, inv_idx = 0.0, 0.0, 1.0
    cb_lo = cb_hi = 0.0
    dh = 0.0
    pool_units = 0.0
    lib_n = 0.0
    rows, pre_hist = [], []
    for m in range(1, M + 1):
        idx = price_index(scn, m, p)
        idx_prev = price_index(scn, m - 1, p) if m > 1 else 1.0
        es = ebay_share(p, m)
        hours = 0.0
        rev = {"recert": 0.0, "pmem": 0.0, "cb": 0.0, "dh": 0.0}
        cogs = {"recert": 0.0, "pmem": 0.0, "cb": 0.0, "dh": 0.0}
        cash_in = cash_out = 0.0
        # ---- recert: sell last month's purchases ------------------------------------------------
        units_sold = 0.0
        if inv_units > 0:
            u = recert_unit(p, idx, inv_idx, es)
            good = inv_units * (1 - p["fail_rate"])
            units_sold = good
            rev["recert"] = good * u["rev"]
            var_cash = good * (u["fees"] + u["ship"] + u["ret"] + u["cons"])
            cogs["recert"] = inv_cost + var_cash
            cash_in += rev["recert"]
            cash_out += var_cash
        # ---- PMem SKU (bought and sold within the month) ----------------------------------------
        pm_units = 0.0
        if "pmem" in lines and m >= p["pmem_start"]:
            pu = pmem_unit(p, idx)
            pm_units = p["pmem_units"] * (p["pmem_post_vmware"] if m >= p["pmem_vmware_month"] else 1.0)
            if pu["gm"] < p["min_margin_to_buy"]:
                pm_units *= p["maintenance_buy_frac"]
            rev["pmem"] = pm_units * pu["rev"]
            pm_cash = pm_units * (pu["buy"] + pu["fees"] + p["ship_ebay"] + pu["rev"] * p["return_rate"]
                                  + p["consumables"])
            cogs["pmem"] = pm_cash
            cash_in += rev["pmem"]
            cash_out += pm_cash
            hours += pm_units * 15.0 / 60.0
        # ---- CleanBOM ---------------------------------------------------------------------------
        lib_cost = 0.0
        cb_conv = 0.0
        cb_new = 0.0
        if "cb" in lines:
            if m >= 4:
                n = p["lib_samples_early"] if m <= 18 else p["lib_samples_late"]
                lib_cost = n * p["lab_cost"] * cm + (0.0 if (bundled and not p.get("_no_lift")) else n * p["lib_module_cost"])
                lib_n += n
            if m >= cb_launch:
                cb_conv = p["cb_conv_ft"] if ft else p["cb_conv_pt"]
                close = (p["cb_close_bundle"] if (bundled and not p.get("_no_lift")) else p["cb_close_standalone"]) \
                    * close_mult
                cb_new = cb_conv * close
                ch = min(0.99, p["cb_churn"] * churn_mult)
                cb_lo = cb_lo * (1 - ch) + cb_new * (1 - p["cb_hi_share"])
                cb_hi = cb_hi * (1 - ch) + cb_new * p["cb_hi_share"]
                mrr = sp * (cb_lo * p["cb_lo_price"] + cb_hi * p["cb_hi_price"])
                packs = cb_conv * p["cb_pack_rate"] * p["cb_pack_price"] * sp
                nsamp = (cb_lo + cb_hi) * p["cb_samples_per_sub"]
                lab_rev = nsamp * p["lab_cost"] * p["lab_markup"]
                lab_cogs = nsamp * p["lab_cost"] * cm
                rev["cb"] = mrr + packs + lab_rev
                cogs["cb"] = lab_cogs + p["cb_sw_cogs_pct"] * cm * (mrr + packs)
                cash_in += rev["cb"]
                cash_out += cogs["cb"]
        cb_mrr = sp * (cb_lo * p["cb_lo_price"] + cb_hi * p["cb_hi_price"])
        # ---- DIMM-health ------------------------------------------------------------------------
        swaps = 0.0
        if "dh" in lines and m >= p["dh_launch"]:
            ch = p["dh_churn_glut"] if (scn != "BASE" and m >= p["turn_month"]) else p["dh_churn"]
            ch = min(0.99, ch * churn_mult)
            dh = dh * (1 - ch) + (p["dh_new_ft"] if ft else p["dh_new_pt"]) * close_mult
            dimms = dh * p["dh_dimms"]
            rev["dh"] = dimms * p["dh_price"] * sp
            sc = spare_cost(p, idx, bundled)
            swaps = dimms * p["dh_repl_rate"] / 12.0
            cogs["dh"] = swaps * (sc + p["dh_ship"]) + dimms * p["dh_host"] * cm \
                + pool_units * sc * p["dh_carry"] / 12.0
            target_pool = dimms * p["dh_pool_frac"]
            cash_out += (target_pool - pool_units) * sc       # pool top-up (or release)
            pool_units = target_pool
            cash_in += rev["dh"]
            cash_out += cogs["dh"]
            hours += swaps * p["dh_swap_hours"]
        dh_mrr = dh * p["dh_dimms"] * p["dh_price"] * sp
        # ---- opex -------------------------------------------------------------------------------
        cb_live = "cb" in lines and m >= cb_launch
        phys = any(x in lines for x in ("recert", "pmem", "dh"))
        opex = p["opex_tools"] + p["opex_insurance"] + p["opex_books"] + p["opex_marketing"]
        if cb_live:
            opex += p["opex_tools_cb"] + p["opex_eo"]
        if phys and (inv_units > p["space_trigger_units"] or ft):
            opex += p["opex_space"]
        if m == 1:
            opex += p["legal_setup"]
        if "cb" in lines and m == cb_launch - 1:
            opex += p["legal_cb"]
        if "cb" in lines and m == cb_launch:
            opex += p["cb_launch_marketing"]
        if m == p["cert_iso_month"]:
            opex += p["cert_iso"]
        if m == 27:
            opex += p["cert_surv"]
        opex += lib_cost
        capex = 0.0
        if m == 1:
            capex += p["capex_m1"] if phys else p["capex_cb_only"]
        if m == 6 and "recert" in lines:
            capex += p["capex_ddr5"]
        # ---- labor: founder hours first, technician beyond ----------------------------------------
        hours += inv_units * p["minutes_per_module"] / 60.0     # modules tested this month = last buy
        founder_h = p["founder_ops_hours_ft"] if ft else p["founder_ops_hours_pt"]
        tech = max(0.0, hours - founder_h) * p["tech_rate"]
        salary = p["founder_salary"] if ft else 0.0
        revenue = sum(rev.values())
        gp = revenue - sum(cogs.values()) - tech
        ebitda_pre = gp - opex
        ebitda = ebitda_pre - salary
        cash += cash_in - cash_out - tech - opex - salary - capex
        # ---- recert purchase for next month (capital- and margin-limited) -------------------------
        buy_units, buy_cost = 0.0, 0.0
        if "recert" in lines and m >= p["recert_start"]:
            cap = p["units_cap_ft"] if ft else p["units_cap_pt"]
            dfac = p["glut_volume_floor"] + (1 - p["glut_volume_floor"]) * \
                max(0.0, min(1.0, (idx - GLUT_RATIO) / (1 - GLUT_RATIO)))
            cap *= dfac
            target = min(cap, p["units_step"] * (m - p["recert_start"] + 1))
            trend = idx / idx_prev if idx_prev > 0 else 1.0
            exp = recert_unit(p, max(0.0, idx * trend), idx, ebay_share(p, m + 1))
            if exp["gm"] < p["min_margin_to_buy"]:
                target *= p["maintenance_buy_frac"]
            unit_buy = recert_unit(p, idx, idx, es)["buy_raw"]
            afford = max(0.0, (cash - p["reserve_cash"]) / unit_buy) if unit_buy > 0 else 0.0
            buy_units = min(target, afford)
            buy_cost = buy_units * unit_buy
            cash -= buy_cost
        inv_units, inv_cost, inv_idx = buy_units, buy_cost, idx
        # ---- founder full-time switch --------------------------------------------------------------
        pre_hist.append(ebitda_pre)
        ft_this = ft
        if not ft and not p.get("_never_ft") and len(pre_hist) >= 3 and sum(pre_hist[-3:]) / 3.0 >= p["ft_trigger_ebitda"] \
                and cash >= p["ft_trigger_cash"]:
            ft = True
        elif ft and cash < p["ft_revert_cash"]:
            ft = False
        rows.append(dict(m=m, label=label(m), idx=idx, units=units_sold, pmem=pm_units,
                         rev_recert=rev["recert"] + rev["pmem"], rev_cb=rev["cb"], rev_dh=rev["dh"],
                         revenue=revenue, gp=gp, opex=opex, salary=salary, ebitda=ebitda, ebitda_pre=ebitda_pre,
                         cash=cash, cb_subs=cb_lo + cb_hi, dh_custs=dh, mrr=cb_mrr + dh_mrr, cb_mrr=cb_mrr,
                         dh_mrr=dh_mrr, ft=ft_this, lib=lib_n, cb_conv=cb_conv, cb_new=cb_new, inv=buy_cost,
                         pool=pool_units * spare_cost(p, idx, bundled), net=cash + buy_cost,
                         gp_recert=rev["recert"] + rev["pmem"] - cogs["recert"] - cogs["pmem"] - tech,
                         gp_cb=rev["cb"] - cogs["cb"], gp_dh=rev["dh"] - cogs["dh"]))
    return rows


def metrics(rows):
    be = None
    for i in range(len(rows) - 2):
        if all(r["ebitda"] >= 0 for r in rows[i:i + 3]):
            be = rows[i]["m"]
            break
    be_sal = None   # breakeven if the founder were paid market salary every month
    for i in range(len(rows) - 2):
        if all(r["ebitda_pre"] - P0["founder_salary"] >= 0 for r in rows[i:i + 3]):
            be_sal = rows[i]["m"]
            break
    low = min(rows, key=lambda r: r["cash"])
    low_net = min(rows, key=lambda r: r["net"])
    ft_m = next((r["m"] for r in rows if r["ft"]), None)
    arr = {k: rows[k - 1]["mrr"] * 12 for k in (12, 18, 24, 36)}
    run = {k: rows[k - 1]["revenue"] * 12 for k in (12, 18, 24, 36)}
    return dict(be=be, be_sal=be_sal, low=low["cash"], low_m=low["m"], ft_m=ft_m, arr=arr, run=run,
                low_net=low_net["net"], low_net_m=low_net["m"], inv36=rows[-1]["inv"], net36=rows[-1]["net"],
                cash36=rows[-1]["cash"], cum_ebitda=sum(r["ebitda"] for r in rows), subs18=rows[17]["cb_subs"], subs36=rows[-1]["cb_subs"],
                dh18=rows[17]["dh_custs"], dh36=rows[-1]["dh_custs"], ft_months=sum(1 for r in rows if r["ft"]),
                rev_total=sum(r["revenue"] for r in rows))


# ----------------------------------------------------------------------------------------------
# Printing helpers (ASCII)
# ----------------------------------------------------------------------------------------------
def table(headers, rows, align=None):
    rows = [["" if v is None else str(v) for v in r] for r in rows]
    w = [max(len(str(h)), *(len(r[i]) for r in rows)) if rows else len(str(h)) for i, h in enumerate(headers)]
    align = align or ["l"] + ["r"] * (len(headers) - 1)
    fmt = lambda cells: "  ".join(c.ljust(w[i]) if align[i] == "l" else c.rjust(w[i]) for i, c in enumerate(cells))
    print("\n".join([fmt([str(h) for h in headers]), "  ".join("-" * x for x in w)] + [fmt(r) for r in rows]))


def section(t):
    print("\n" + "=" * 104 + "\n" + t + "\n" + "=" * 104)


def k(x):
    return "%.1fk" % (x / 1000.0)


def usd(x):
    return "$%s" % format(int(round(x)), ",")


def pct(x):
    return "%.0f%%" % (100 * x)


def mo(m):
    return "never" if m is None else "m%d (%s)" % (m, label(m))


# ----------------------------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------------------------
def main():
    p = dict(P0)
    print("DD1 Provenance & Recertified Memory -- unit economics and 36-month P&L (models/provenance-recert.py)")
    print("As of 2026-11-01. Month 1 = Nov-26, month 36 = Oct-29. DDR5 deck: %s" % REF_SRC)
    print("  DDR5 component cost $%.2f/GB | Q4-26 contract $%.2f/GB | glut $%.2f/GB (x%.2f) | severe $%.2f/GB (x%.2f)"
          % (REF["cost_component_usd_per_gb"], CONTRACT, REF["glut_component_usd_per_gb"], GLUT_RATIO,
             REF["severe_glut_component_usd_per_gb"], SEVERE_RATIO))
    used_ddr5_gb = p["ddr5_64_price"] / 64.0
    print("  New 64GB DDR5 RDIMM contract $%.2f/user-GB; used 64GB DDR5 resale $%.2f/GB = %.0f%% of new "
          "(amcompute 55-74%% band check)" % (NEW_RDIMM64_PER_GB, used_ddr5_gb, 100 * used_ddr5_gb / NEW_RDIMM64_PER_GB))
    print("  Used resale index applied to all recert SKUs, PMem and spares; CleanBOM demand is statutory (same in all).")
    print("  INPUTS: %d values, each with a source or 'ESTIMATE: basis' (see the INPUTS dict in this file)." % len(INPUTS))

    # ---------------- 1. unit economics per line ----------------
    section("1. UNIT ECONOMICS PER PRODUCT LINE (per unit, at each price deck; steady state, no inventory lag)")
    decks = [("Today (BASE 2026-27)", 1.0), ("GLUT (x%.2f)" % GLUT_RATIO, GLUT_RATIO),
             ("SEVERE (x%.2f)" % SEVERE_RATIO, SEVERE_RATIO)]
    print("\n1a. Recert RDIMM (mix 60%% 32GB DDR4 / 30%% 64GB DDR4 / 10%% 64GB DDR5), per good module; "
          "buy at %.0f%% of realized resale" % (100 * p["buy_frac"]))
    rows = []
    for name, idx in decks:
        for ch, es in (("eBay", 1.0), ("B2B", 0.0), ("mix m12", p["ebay_share_m12"])):
            u = recert_unit(p, idx, idx, es)
            rows.append([name if ch == "eBay" else "", ch, usd(u["rev"]), usd(u["buy"]), usd(u["fees"] + u["ship"]),
                         usd(u["ret"] + u["cons"] + u["labor"]), usd(u["contrib"]), pct(u["gm"])])
    table(["Deck", "Channel", "Price", "Buy+fallout", "Fees+ship", "Ret+cons+labor", "Contrib", "GM"], rows,
          ["l", "l"] + ["r"] * 6)
    print("  Per SKU, today, mixed channel:")
    rows = []
    for nm, gb, base, share in skus(p):
        q = dict(p)
        q.update({"mix_ddr4_32": 0, "mix_ddr4_64": 0, "mix_ddr5_64": 0})
        q[{"DDR4 32GB": "mix_ddr4_32", "DDR4 64GB": "mix_ddr4_64", "DDR5 64GB": "mix_ddr5_64"}[nm]] = 1.0
        u = recert_unit(q, 1.0, 1.0, p["ebay_share_m12"])
        rows.append([nm, "$%.2f/GB" % (base / gb), usd(u["rev"]), usd(u["buy_raw"]), usd(u["contrib"]), pct(u["gm"]),
                     usd(u["buy_raw"])])
    table(["SKU", "Resale/GB", "Avg price", "Buy", "Contrib", "GM", "Cash tied/unit"], rows)
    # inventory-lag loss in a falling month
    u_lag = recert_unit(p, 1.0 - (1 - GLUT_RATIO) / 12.0, 1.0, p["ebay_share_m12"])
    print("  Inventory lag: buying at today's price and selling one GLUT month later (-%.0f%%/month) gives %s "
          "contribution per module (%s)." % (100 * (1 - GLUT_RATIO) / 12, usd(u_lag["contrib"]), pct(u_lag["gm"])))

    print("\n1b. Optane PMem 128GB (C-26 SKU), eBay only")
    table(["Deck", "Price", "Buy", "Fees", "Labor", "Contrib", "GM"],
          [[n, usd(pmem_unit(p, i)["rev"]), usd(pmem_unit(p, i)["buy"]), usd(pmem_unit(p, i)["fees"]),
            usd(pmem_unit(p, i)["labor"]), usd(pmem_unit(p, i)["contrib"]), pct(pmem_unit(p, i)["gm"])]
           for n, i in decks])

    print("\n1c. CleanBOM-5949 per subscriber-month (blended %d%% $%d / %d%% $%d) -- same in every deck"
          % (100 * (1 - p["cb_hi_share"]), p["cb_lo_price"], 100 * p["cb_hi_share"], p["cb_hi_price"]))
    arpa = cb_arpa(p)
    lab_rev = p["cb_samples_per_sub"] * p["lab_cost"] * p["lab_markup"]
    lab_c = p["cb_samples_per_sub"] * p["lab_cost"]
    sw_c = p["cb_sw_cogs_pct"] * arpa
    cb_gm = (arpa + lab_rev - lab_c - sw_c) / (arpa + lab_rev)
    table(["Item", "$/month"], [["Subscription ARPA", usd(arpa)], ["Lab pass-through revenue", usd(lab_rev)],
                                ["Lab cost", usd(-lab_c)], ["Software COGS (12%)", usd(-sw_c)],
                                ["Gross profit", usd(arpa + lab_rev - lab_c - sw_c)], ["GM", pct(cb_gm)]])
    print("  One-off evidence pack: $%d at ~%s GM (software cost only)." % (p["cb_pack_price"],
                                                                        pct(1 - p["cb_sw_cogs_pct"])))

    print("\n1d. DIMM-health per customer-year (%d DIMMs at $%.2f/DIMM-month)" % (p["dh_dimms"], p["dh_price"]))
    rows = []
    for n, i in decks:
        for bundled in (True, False):
            sc = spare_cost(p, i, bundled)
            dimms = p["dh_dimms"]
            r = dimms * p["dh_price"] * 12
            c = dimms * p["dh_repl_rate"] * (sc + p["dh_ship"]) + dimms * p["dh_host"] * 12 \
                + dimms * p["dh_pool_frac"] * sc * p["dh_carry"]
            diy = dimms * p["dh_repl_rate"] * (sc + p["dh_ship"])
            rows.append([n if bundled else "", "bundle" if bundled else "standalone", usd(r), usd(c), pct((r - c) / r),
                         usd(sc), usd(dimms * p["dh_pool_frac"] * sc), "%.1fx" % (r / diy)])
    table(["Deck", "Spares from", "Revenue/yr", "COGS/yr", "GM", "Spare cost", "Pool capital", "Fee/DIY spares"],
          rows, ["l", "l"] + ["r"] * 6)

    print("\n1e. Customer acquisition (founder time imputed at $%d/h, %d h per conversation; marketing $%d/mo)"
          % (p["founder_hour_value"], p["hours_per_conversation"], p["opex_marketing"]))
    cac_cb = p["hours_per_conversation"] * p["founder_hour_value"] / p["cb_close_bundle"] \
        + p["opex_marketing"] / max(1e-9, p["cb_conv_pt"] * p["cb_close_bundle"]) * 0.5
    ltv_cb = (arpa + lab_rev - lab_c - sw_c) / p["cb_churn"]
    dh_gp_m = p["dh_dimms"] * p["dh_price"] - (p["dh_dimms"] * p["dh_repl_rate"] / 12 * (spare_cost(p, 1.0, True)
                                                                                      + p["dh_ship"])
                                                + p["dh_dimms"] * p["dh_host"])
    cac_dh = 20 * p["hours_per_conversation"] * p["founder_hour_value"]   # ~20 conversations per signed fleet
    ltv_dh = dh_gp_m / p["dh_churn"]
    table(["Line", "Close/conv", "CAC", "Gross profit/mo", "Churn/mo", "LTV", "LTV/CAC", "Payback (mo)"],
          [["CleanBOM", pct(p["cb_close_bundle"]), usd(cac_cb), usd(arpa + lab_rev - lab_c - sw_c),
            pct(p["cb_churn"]), usd(ltv_cb), "%.0fx" % (ltv_cb / cac_cb), "%.1f" % (cac_cb / (arpa + lab_rev - lab_c - sw_c))],
           ["DIMM-health", "~5%", usd(cac_dh), usd(dh_gp_m), "%.1f%%" % (100 * p["dh_churn"]), usd(ltv_dh),
            "%.0fx" % (ltv_dh / cac_dh), "%.1f" % (cac_dh / dh_gp_m)],
           ["Recert B2B", "n/a", "in fees", "per module", "n/a", "n/a", "n/a", "n/a"]])
    print("  LTV/CAC looks high only because the close rate and churn are untested; the kill experiment measures them.")

    # ---------------- 2. monthly P&L per scenario ----------------
    results = {}
    for scn in SCENARIOS:
        rows = simulate(scn, p)
        results[scn] = rows
        section("2. MONTHLY P&L AND CASH, %s scenario (all four lines; $; FT = founder full-time)" % scn)
        out = []
        for r in rows:
            out.append([r["label"], "%.2f" % r["idx"], "%d" % round(r["units"]), k(r["rev_recert"]), k(r["rev_cb"]),
                        k(r["rev_dh"]), k(r["revenue"]), k(r["gp"]), k(r["opex"]), k(r["salary"]), k(r["ebitda"]),
                        k(r["cash"]), k(r["inv"]), "%.1f" % r["cb_subs"], "%.1f" % r["dh_custs"], k(r["mrr"] * 12),
                        "FT" if r["ft"] else ""])
        table(["Month", "Idx", "Mods", "Recert+PMem", "CleanBOM", "DIMM-h", "Revenue", "GP", "Opex", "Salary",
               "EBITDA", "Cash", "Inv buy", "CB subs", "DH cust", "ARR", ""], out)
        print("  Mods = good recert modules sold. Inv buy = lots bought this month for next month (cash already out).")

    # ---------------- 3. scenario summary ----------------
    section("3. SCENARIO SUMMARY (bundle, all four lines)")
    out = []
    for scn in SCENARIOS:
        mt = metrics(results[scn])
        out.append([scn, mo(mt["be"]), mo(mt["be_sal"]), "%s @m%d" % (usd(mt["low"]), mt["low_m"]),
                    "%s @m%d" % (usd(mt["low_net"]), mt["low_net_m"]),
                    usd(mt["arr"][12]), usd(mt["arr"][18]), usd(mt["arr"][24]), usd(mt["arr"][36]),
                    usd(mt["run"][18]), usd(mt["run"][36]), usd(mt["cash36"]), usd(mt["inv36"]), mo(mt["ft_m"])])
    table(["Scenario", "Breakeven (actual)", "Breakeven @$10k salary", "Cash low", "Cash+inv low", "ARR m12",
           "ARR m18", "ARR m24", "ARR m36", "Run-rate m18", "Run-rate m36", "Cash m36", "Inventory m36",
           "Founder FT from"], out)
    print("  Cash low sits on the $5k reserve by design: the operator buys inventory down to the reserve, so working")
    print("  capital, not losses, is what binds in year 1. 'Cash+inv low' adds back the lots bought that month.")
    print("  ARR = recurring only (CleanBOM subscriptions + DIMM-health) x 12. Run-rate = all revenue in that month x 12.")
    print("  'Breakeven (actual)' = first of 3 straight months with EBITDA >= 0 as actually incurred (founder unpaid")
    print("  until the full-time trigger). 'Breakeven @$10k salary' charges a market founder salary every month.")
    for scn in SCENARIOS:
        rr = results[scn]
        rec = sum(r["rev_recert"] for r in rr)
        print("  %-6s cumulative revenue %s: recert+PMem %s (%s), CleanBOM %s, DIMM-health %s; recert modules sold %s"
              % (scn, usd(sum(r["revenue"] for r in rr)), usd(rec), pct(rec / max(1, sum(r["revenue"] for r in rr))),
                 usd(sum(r["rev_cb"] for r in rr)), usd(sum(r["rev_dh"] for r in rr)),
                 format(int(sum(r["units"] for r in rr)), ",")))
    print("  Gross margin over 36 months (GP / revenue; recert GP is after technician labor):")
    for scn in SCENARIOS:
        rr = results[scn]
        def g(a, b):
            ra = sum(r[a] for r in rr)
            return pct(sum(r[b] for r in rr) / ra) if ra else "n/a"
        print("  %-6s blended %s | recert+PMem %s | CleanBOM %s | DIMM-health %s"
              % (scn, g("revenue", "gp"), g("rev_recert", "gp_recert"), g("rev_cb", "gp_cb"), g("rev_dh", "gp_dh")))
    lib = results["BASE"][-1]["lib"]
    print("  Die-source library by m36: %d lab-confirmed module part numbers (X-ray+decap), plus SPD records on every"
          " recert module." % lib)

    # ---------------- 4. whole vs parts ----------------
    section("4. IS THE WHOLE BETTER THAN ITS PARTS?  (same founder, same $40k, run line-by-line)")
    configs = [("Bundle (all four)", ALL_LINES, {}), ("Recert + PMem only", ("recert", "pmem"), {}),
               ("CleanBOM standalone", ("cb",), {}), ("DIMM-health standalone", ("dh",), {}),
               ("Recert + CleanBOM", ("recert", "pmem", "cb"), {}),
               ("Bundle, no evidence lift", ALL_LINES, {"_no_lift": True}),
               ("Bundle, founder never FT", ALL_LINES, {"_never_ft": True})]
    out = []
    for scn in SCENARIOS:
        for name, ln, ov in configs:
            q = dict(p)
            q.update(ov)
            mt = metrics(simulate(scn, q, ln))
            out.append([scn if name.startswith("Bundle") else "", name, "%s @m%d" % (usd(mt["low"]), mt["low_m"]),
                        mo(mt["be"]), usd(mt["arr"][18]), usd(mt["arr"][36]), usd(mt["run"][36]), usd(mt["cash36"]),
                        usd(mt["cum_ebitda"]), "%d" % mt["ft_months"]])
    table(["Scenario", "Configuration", "Cash low", "Breakeven", "ARR m18", "ARR m36", "Run-rate m36", "Cash m36",
           "Cum EBITDA", "FT months"], out, ["l", "l"] + ["r"] * 8)
    print("  Standalone CleanBOM pays for each library sample module and closes at %.0f%% vs %.0f%% (the bundle"
          % (100 * p["cb_close_standalone"], 100 * p["cb_close_bundle"]))
    print("  hypothesis, untested). Standalone DIMM-health buys spares at resale, not recert buy cost.")
    print("  'No evidence lift' keeps the recert cash but gives CleanBOM the standalone close rate and sample cost:")
    print("  the gap to the full bundle is what the die-source library is worth; the gap to 'founder never FT' is")
    print("  what recert cash (buying founder time) is worth.")

    # ---------------- 5. sensitivity ----------------
    section("5. SENSITIVITY (BASE scenario, bundle; one input moved at a time)")
    base_mt = metrics(results["BASE"])
    tests = [("Recert resale price", "_recert_price_mult"), ("SaaS / subscription price", "_saas_price_mult"),
             ("Close rate (CB + DH)", "_close_mult"), ("Churn (CB + DH)", "_churn_mult"),
             ("COGS (buy %, fees, lab, hosting)", "_cogs_mult")]
    out = [["Base case", "--", mo(base_mt["be"]), usd(base_mt["low"]), usd(base_mt["arr"][18]),
            usd(base_mt["arr"][36]), usd(base_mt["cash36"]), usd(base_mt["cum_ebitda"])]]
    for name, key in tests:
        for mult in (0.7, 1.3):
            q = dict(p)
            q[key] = mult
            mt = metrics(simulate("BASE", q))
            out.append([name, "%+d%%" % round(100 * (mult - 1)), mo(mt["be"]), usd(mt["low"]), usd(mt["arr"][18]),
                        usd(mt["arr"][36]), usd(mt["cash36"]), usd(mt["cum_ebitda"])])
    for name, key, val in (("Final FAR rule slips 6 mo (CB launch m16)", "_cb_delay", 6),
                           ("Founder stays part-time all 36 months", "_never_ft", True)):
        q = dict(p)
        q[key] = val
        mt = metrics(simulate("BASE", q))
        out.append([name, "+6 mo" if key == "_cb_delay" else "PT", mo(mt["be"]), usd(mt["low"]), usd(mt["arr"][18]), usd(mt["arr"][36]),
                    usd(mt["cash36"]), usd(mt["cum_ebitda"])])
    for bf in (0.55, 0.75):
        q = dict(p)
        q["buy_frac"] = bf
        mt = metrics(simulate("BASE", q))
        out.append(["ITAD buy fraction = %.2f" % bf, "abs", mo(mt["be"]), usd(mt["low"]), usd(mt["arr"][18]),
                    usd(mt["arr"][36]), usd(mt["cash36"]), usd(mt["cum_ebitda"])])
    table(["Input", "Move", "Breakeven", "Cash low", "ARR m18", "ARR m36", "Cash m36", "Cum EBITDA"], out,
          ["l", "l"] + ["r"] * 6)
    print("  Glut and severe sensitivities: see sections 3-4 (CleanBOM is price-independent; recert is not).")

    # ---------------- 6. what must be true ----------------
    section("6. WHAT MUST BE TRUE")
    # (a) breakeven buy fraction
    def contrib_at(bf, es):
        q = dict(p)
        q["buy_frac"] = bf
        return recert_unit(q, 1.0, 1.0, es)["contrib"]
    def solve(es):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if contrib_at(mid, es) > 0:
                lo = mid
            else:
                hi = mid
        return lo
    print("a) Recert: lots must cost less than %.0f%% (eBay) / %.0f%% (B2B) / %.0f%% (m12 mix) of realized resale for any"
          % (100 * solve(1.0), 100 * solve(0.0), 100 * solve(p["ebay_share_m12"])))
    print("   contribution at today's prices; at the modeled %.0f%% the mixed-channel margin is %s per module (%s)."
          % (100 * p["buy_frac"], usd(recert_unit(p, 1, 1, p["ebay_share_m12"])["contrib"]),
             pct(recert_unit(p, 1, 1, p["ebay_share_m12"])["gm"])))
    u = recert_unit(p, 1.0, 1.0, p["ebay_share_m12"])
    fixed18 = p["opex_tools"] + p["opex_tools_cb"] + p["opex_insurance"] + p["opex_eo"] + p["opex_books"] \
        + p["opex_marketing"] + p["opex_space"] + p["lib_samples_late"] * p["lab_cost"]
    print("b) Recert alone covers a $10k/mo founder salary + ~%s fixed opex at %d good modules/month at today's prices"
          % (usd(fixed18), (p["founder_salary"] + fixed18) / max(1e-9, u["contrib"])))
    print("   (needs ~%s of inventory cash per month at %.0f%% buy) -- and only until the 2028 turn."
          % (usd((p["founder_salary"] + fixed18) / u["contrib"] * u["buy_raw"]), 100 * p["buy_frac"]))
    gp_sub = arpa + lab_rev - lab_c - sw_c
    n_need = (p["founder_salary"] + fixed18) / gp_sub
    print("c) For the business to survive the glut on recurring revenue alone, CleanBOM needs ~%.0f paying subscribers"
          " (at %s GP/sub-month)" % (n_need, usd(gp_sub)))
    print("   by the 2028 turn (month 15-18). Modeled BASE: %.1f subscribers at m18, %.1f at m36."
          % (results["BASE"][17]["cb_subs"], results["BASE"][-1]["cb_subs"]))
    surv = sum((1 - p["cb_churn"]) ** (18 - mm) for mm in range(p["cb_launch"], 19))
    close_need = n_need / (p["cb_conv_pt"] * surv)
    conv_need = n_need / (p["cb_close_bundle"] * surv)
    print("   Getting there by m18 from a m%d launch needs a %.0f%% close rate at %d conversations/month, or %.0f"
          " conversations/month at a %.0f%% close." % (p["cb_launch"], 100 * close_need, p["cb_conv_pt"], conv_need,
                                                     100 * p["cb_close_bundle"]))
    print("d) Equivalently: by month 18 the founder needs ~%.0f signed provenance customers (e.g. %.0f module makers at"
          " $%d + %.0f integrators at $%d)." % (n_need, n_need * p["cb_hi_share"], p["cb_hi_price"],
                                                n_need * (1 - p["cb_hi_share"]), p["cb_lo_price"]))
    print("e) DIMM-health must sell at %.1fx the buyer's DIY spares cost against free OEM/BMC prediction (Lenovo MPFA,"
          % (p["dh_dimms"] * p["dh_price"] * 12 / (p["dh_dimms"] * p["dh_repl_rate"] * (spare_cost(p, 1, True) + p["dh_ship"]))))
    print("   Intel MFP) and ParkView-bundled TPM: it must be sold as a wholesale feed + spares to TPMs/MSPs, or dropped.")
    print("f) $1M ARR at m36 would need ~%.0f CleanBOM subscribers at the blended ARPA; the model reaches %.1f."
          % (1e6 / 12 / arpa, results["BASE"][-1]["cb_subs"]))

    # ---------------- 7. glut behavior per line ----------------
    section("7. GLUT BEHAVIOR PER LINE (steady-state unit margin and modeled revenue in the last 12 months)")
    out = []
    for scn in SCENARIOS:
        rr = results[scn][-12:]
        i = price_index(scn, M, p)
        out.append([scn, "%.2f" % i, pct(recert_unit(p, i, i, p["ebay_share_m12"])["gm"]), pct(pmem_unit(p, i)["gm"]),
                    pct(cb_gm), usd(sum(r["rev_recert"] for r in rr)), usd(sum(r["rev_cb"] for r in rr)),
                    usd(sum(r["rev_dh"] for r in rr)), "%.1f" % rr[-1]["dh_custs"]])
    table(["Scenario", "Idx m36", "Recert GM", "PMem GM", "CleanBOM GM", "Recert rev (last 12m)", "CB rev (last 12m)",
           "DH rev (last 12m)", "DH cust m36"], out)
    print("  Recert dies as a profit line in GLUT/SEVERE (buying stops; trickle kept for spares/library). PMem dies on")
    print("  2027-10-11 (VMware) regardless. CleanBOM is unaffected by price. DIMM-health margin rises (cheap spares) but")
    print("  customers churn faster once DDR5 refresh is cheap.")
    print("\nDone. exit 0")


if __name__ == "__main__":
    main()
    sys.exit(0)
