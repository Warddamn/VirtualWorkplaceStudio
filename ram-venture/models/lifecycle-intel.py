#!/usr/bin/env python3
"""DD2 "Memory Lifecycle & Cost Intelligence for OEMs" -- unit economics and 36-month P&L.

Bundle: anchor C-80 (memory exposure + buy/hold/EOL alerts SaaS), folded C-29 (EOL NVM cross-reference,
a feature), C-61 (LTB-sizing software + LTB studies; the physical vault is NOT modelled), C-72 (pooled
forecast portal, a free feature; no co-op revenue), C-86 (Memory Cost Escalation Index licences).

Run from the repo root:  python3 models/lifecycle-intel.py
Pure stdlib. Exits 0. Every input carries a source URL or "ESTIMATE: basis".
Agent key: p4-lifecycle-intel. As of 2026-11-01. Month 1 of the model = 2026-12.
"""
import contextlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ----------------------------------------------------------------------------------------------
# DDR5 reference deck (canonical; import from models/dram_cost_stack.py, fall back if that fails)
# ----------------------------------------------------------------------------------------------
CANONICAL_FALLBACK = dict(
    cost_component_usd_per_gb=1.48, contract_component_usd_per_gb_q4_2026=20.37,
    glut_component_usd_per_gb=8.15, severe_glut_component_usd_per_gb=2.04,
    contract_rdimm64_usd_per_user_gb_q4_2026=25.8, glut_rdimm64_usd_per_user_gb=10.3,
)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        from dram_cost_stack import ddr5_reference  # noqa: E402
        REF = ddr5_reference()
    REF_SRC = "models/dram_cost_stack.py ddr5_reference()"
except Exception as exc:  # pragma: no cover - fallback path
    REF = dict(CANONICAL_FALLBACK)
    REF_SRC = "canonical fallback numbers (import failed: %s)" % exc

P_Q4_2026 = REF["contract_component_usd_per_gb_q4_2026"]   # $/GB DDR5 contract, Q4-2026
P_GLUT = REF["glut_component_usd_per_gb"]                  # $/GB, A-05 glut (-60%)
P_SEVERE = REF["severe_glut_component_usd_per_gb"]         # $/GB, severe glut

# ----------------------------------------------------------------------------------------------
# INPUTS  (value, source).  Every number used below comes from this block.
# ----------------------------------------------------------------------------------------------
INPUTS = {
    # --- timeline -------------------------------------------------------------------------------
    "months": (36, "ESTIMATE: mission 36-month hard ceiling for PRIMARY"),
    "start_year": (2026, "ESTIMATE: model month 1 = 2026-12, after a November kill experiment"),
    "start_month": (12, "ESTIMATE: model month 1 = December 2026 (kill experiment runs in November 2026)"),
    "saas_launch_month": (5, "ESTIMATE: ~4 months x ~60 founder h/month to an MVP on DigiKey/Nexar APIs; C-80 card says 4-8 months"),
    "design_partner_until": (10, "ESTIMATE: first paying cohort gets ~40% off through month 10 (design-partner pricing)"),
    "design_partner_arpa_factor": (0.60, "ESTIMATE: 40% design-partner discount"),
    "index_methodology_month": (9, "ESTIMATE: methodology + back-filled history from contributed PO data published month 9 (C-86 card: 9-15 months)"),
    "index_first_sale_month": (12, "ESTIMATE: first licence 3 months after methodology; C-86 audit says both parties' legal teams must accept"),
    # --- founder & capital ----------------------------------------------------------------------
    "founder_cash": (40_000.0, "ESTIMATE: ASSUMPTIONS A-03 ($40k deployable)"),
    "founder_salary_ft": (10_000.0, "ESTIMATE: ASSUMPTIONS A-03 (~$120k/yr loaded once revenue supports it)"),
    "hire_trigger_mrr": (45_000.0, "ESTIMATE: add a sales/CS hire once MRR covers it ~5x"),
    "hire_cost": (9_000.0, "ESTIMATE: ~$108k/yr loaded sales/CS hire"),
    "hire_capacity_mult": (1.6, "ESTIMATE: second seller adds ~60% pipeline capacity"),
    # --- pricing ----------------------------------------------------------------------------------
    "team_price": (249.0, "ESTIMATE: at SiliconExpert BOM Manager Essentials $250/mo (1 user, 1 BOM <=500 parts) https://www.siliconexpert.com/products/bom-manager/"),
    "pro_price": (649.0, "ESTIMATE: multi-BOM/EMS tier; ~$7.8k/yr vs Accuris $6,000 ACV minimum https://accuristech.com/accuris-price-match-offer-terms/"),
    "pro_mix": (0.25, "ESTIMATE: 1 in 4 accounts need multi-BOM / LTB-inventory module"),
    "contributor_share": (0.40, "ESTIMATE: share of accounts that contribute anonymised memory PO prices to the index panel"),
    "contributor_discount": (0.10, "ESTIMATE: 10% discount for contributing PO data (Lytica-style transaction data https://www.cengn.ca/wp-content/uploads/2020/06/Lytica-Success-Story.pdf)"),
    "index_std_price": (6_000.0, "ESTIMATE: E-02 model (research/phase2/E_notes.md s.11); below DRAMeXchange Gold $11k/yr https://giikorea.co.kr/annual/tdf225654-dramexchange-membership.html"),
    "index_ent_price": (24_000.0, "ESTIMATE: E-02 model; redistribution/API tier, below DRAMeXchange DRAM&NAND Platinum $30k"),
    "index_ent_mix": (0.15, "ESTIMATE: E-02 assumed 5 of 35 licences enterprise"),
    "ltb_study_price": (3_500.0, "ESTIMATE: 1.5-2 analyst-days; LTB order window is 6 months from PDN (https://www.maxlinear.com/support/quality/policy-and-procedure)"),
    # --- COGS -------------------------------------------------------------------------------------
    "saas_hosting_per_acct": (10.0, "ESTIMATE: cloud compute/storage per account-month"),
    "saas_data_per_acct": (12.0, "ESTIMATE: marginal API/data volume per account-month"),
    "support_h_per_acct": (0.5, "ESTIMATE: onboarding + alert triage hours per account-month"),
    "support_rate": (60.0, "ESTIMATE: U.S. contractor support rate $/h (cash cost even while founder is part-time)"),
    "payment_fee": (0.03, "ESTIMATE: card processing ~2.9% + $0.30"),
    "index_support_h": (1.0, "ESTIMATE: hours per licence-month (methodology questions, audit packs)"),
    "ltb_cogs_share": (0.30, "ESTIMATE: contractor analyst time + data pulls per LTB study"),
    "fixed_hosting": (150.0, "ESTIMATE: base infra from launch"),
    "nexar_standard": (300.0, "ESTIMATE: price unpublished; Standard tier = 2,000 matched parts/mo https://nexar.com/compare-plans"),
    "nexar_pro": (1_000.0, "ESTIMATE: price unpublished; Pro tier = 15,000 matched parts/mo https://nexar.com/compare-plans"),
    "nexar_pro_trigger_accts": (60, "ESTIMATE: ~250 memory MPNs per account refreshed monthly exceeds 2,000 matched parts at ~8+ accounts with caching; switch tier at 60"),
    "display_licence": (1_000.0, "ESTIMATE: commercial display/redistribution licence; Octopart terms bar historical-trend use and >24h caching https://octopart.com/api/legal"),
    "display_licence_from": (12, "ESTIMATE: needed once in-app price display scales"),
    "dramx_silver_yr": (5_000.0, "https://giikorea.co.kr/annual/tdf225654-dramexchange-membership.html (Silver $5,000/yr; internal benchmarking only, not redistributable)"),
    # --- opex -------------------------------------------------------------------------------------
    "tools": (250.0, "ESTIMATE: dev tools, CRM, email, domain"),
    "marketing_pre": (300.0, "ESTIMATE: newsletter + free public memory surcharge reference page"),
    "marketing_post": (900.0, "ESTIMATE: content, LinkedIn, association memberships (AdvaMed/IPC/SMTA chapters)"),
    "cost_per_trial": (35.0, "ESTIMATE: blended paid+organic cost per qualified trial (B2B CPL $30-150, mostly organic here)"),
    "founder_sales_h_per_trial": (1.0, "ESTIMATE: demo + follow-up per qualified trial (imputed, not cash while part-time)"),
    "founder_h_value": (75.0, "ESTIMATE: imputed value of founder sales hour for fully loaded CAC"),
    "insurance": (150.0, "ESTIMATE: E&O/cyber ~$1.8k/yr from launch"),
    "accounting": (100.0, "ESTIMATE: bookkeeping/bank"),
    "legal_onetime": (7_000.0, "ESTIMATE: gov-contracts attorney reviews index methodology, EPA clause kit (FAR 16.203-1/52.216-4) and API licences"),
    "legal_month": (8, "ESTIMATE: before index methodology is published"),
    "travel": (2_500.0, "ESTIMATE: one trade show per year (months 10, 22, 34)"),
    # --- acquisition ------------------------------------------------------------------------------
    "trials_at_launch": (6.0, "ESTIMATE: founder network + day-job peers + free exposure scan"),
    "trials_growth": (2.0, "ESTIMATE: +2 qualified trials/month/month as content compounds"),
    "trials_cap_pt": (25.0, "ESTIMATE: part-time (15 h/wk) can run ~25 trials/month"),
    "trials_cap_ft": (60.0, "ESTIMATE: full-time founder ~60 trials/month"),
    "trial_conversion": (0.12, "ESTIMATE: B2B opt-in trial->paid 10-25%; low end because memory-only scope vs SiliconExpert's all-parts $250 tier"),
    "lifecycle_floor": (0.40, "ESTIMATE: share of demand driven by EOL/lifecycle (price-insensitive); AdvaMed: 63% of medtech report allocation/scarcity https://www.advamed.org/2026/08/17/memory-chip-shortages-implications-for-medtech-innovation-and-patient-care/"),
    "churn_base": (0.020, "ESTIMATE: SMB B2B SaaS 2-3%/month"),
    "churn_glut_extra": (0.08, "ESTIMATE: price-motivated accounts churn up to +8%/month when DDR5 is at 0% of peak (C-80 audit: buy/hold alerts worthless in glut)"),
    "index_rate": (0.60, "ESTIMATE: new index licences/month at full volatility, part-time (E-02: 35 licences over ~3 years)"),
    "index_floor": (0.35, "ESTIMATE: residual demand when prices are flat (multi-year EPA clauses still needed after a 6x shock)"),
    "vol_ref": (0.15, "ESTIMATE: a 15% move in 3 months saturates index demand (Lewis Silkin 2026-05: clauses built for 3-5%/yr)"),
    "index_churn": (0.008, "ESTIMATE: licences embedded in multi-year contracts rarely churn"),
    "index_churn_flat": (0.015, "ESTIMATE: renewal churn when 3-month move <2% after month 24"),
    "ltb_attach": (0.015, "ESTIMATE: share of active accounts ordering an LTB study per month"),
    "ltb_inbound": (0.30, "ESTIMATE: non-subscriber LTB studies/month after launch"),
    "ltb_cap_pt": (2.0, "ESTIMATE: part-time capacity, studies/month"),
    "ltb_cap_ft": (4.0, "ESTIMATE: full-time capacity, studies/month"),
    "eol_mult_glut": (1.25, "ESTIMATE: makers exit legacy lines faster in downturns (2023: Nanya/Winbond legacy pressure https://apps.digitimes.com/news/a20230222PD222/dram-nanya.html)"),
    "eol_mult_severe": (1.40, "ESTIMATE: deeper trough -> more EOL/PDN notices"),
    "ft_capacity_index_mult": (1.5, "ESTIMATE: full-time founder closes 50% more index licences"),
    # --- price path (multipliers on the Q4-2026 DDR5 contract price) ------------------------------
    "q_2027": ((1.04, 1.06, 1.07, 1.07), "ESTIMATE: server DRAM contract keeps rising through 2H27 with narrowing increases https://finance.technews.tw/2026/07/09/long-term-agreements-price-cap-3q26-server-dram-contract-price-estimated-13-18-qoq-increase/"),
    "base_end_2028": (0.85, "ESTIMATE: BASE turn in 2028, BofA -10% ASP (01_LANDSCAPE s.1 row 4b); -15% by Dec-2028"),
    "base_end_2029": (0.80, "ESTIMATE: BASE soft 2029"),
    "tam_us_smb_oems": (6_000, "ESTIMATE: U.S. hardware OEMs/EMS with $1-50M BOM spend and memory in BOM (NAICS 334 + 3345 + 3391 firms with ~20-500 staff); unsourced order-of-magnitude"),
}
P = {k: v[0] for k, v in INPUTS.items()}

SCENARIOS = ("BASE", "GLUT", "SEVERE")
SCEN_END_2028 = {"BASE": P["base_end_2028"], "GLUT": P_GLUT / P_Q4_2026, "SEVERE": P_SEVERE / P_Q4_2026}
SCEN_END_2029 = {"BASE": P["base_end_2029"], "GLUT": P_GLUT / P_Q4_2026, "SEVERE": P_SEVERE / P_Q4_2026}
EOL_MULT = {"BASE": 1.0, "GLUT": P["eol_mult_glut"], "SEVERE": P["eol_mult_severe"]}


# ----------------------------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------------------------
def cal(m):
    """model month (1-based) -> (year, month)"""
    idx = (P["start_year"] * 12 + P["start_month"] - 1) + (m - 1)
    return idx // 12, idx % 12 + 1


def label(m):
    y, mo = cal(m)
    return "%d-%02d" % (y, mo)


def price_mult(m, scen):
    """DDR5 contract price as a multiple of Q4-2026, piecewise linear by month."""
    y, mo = cal(m)
    if y <= 2026:
        return 1.0
    if y == 2027:
        return P["q_2027"][(mo - 1) // 3]
    peak = P["q_2027"][3]
    if y == 2028:
        t = mo / 12.0
        return peak + (SCEN_END_2028[scen] - peak) * t
    t = min(1.0, (mo + 12 * (y - 2029)) / 12.0)
    return SCEN_END_2028[scen] + (SCEN_END_2029[scen] - SCEN_END_2028[scen]) * t


def table(headers, rows, align=None):
    rows = [["" if v is None else str(v) for v in r] for r in rows]
    w = [max(len(str(h)), *(len(r[i]) for r in rows)) if rows else len(str(h)) for i, h in enumerate(headers)]
    align = align or ["l"] + ["r"] * (len(headers) - 1)
    fmt = lambda cells: "  ".join(c.ljust(w[i]) if align[i] == "l" else c.rjust(w[i]) for i, c in enumerate(cells)).rstrip()
    print("\n".join([fmt([str(h) for h in headers]), "  ".join("-" * x for x in w)] + [fmt(r) for r in rows]))


def section(t):
    print("\n" + "=" * 104 + "\n" + t + "\n" + "=" * 104)


def k(x):
    return "%.0fk" % (x / 1000.0) if abs(x) >= 1000 else "%.0f" % x


def money(x):
    return "-$%s" % format(-x, ",.0f") if x < 0 else "$%s" % format(x, ",.0f")


def pct(x):
    return "%.0f%%" % (100.0 * x)


# ----------------------------------------------------------------------------------------------
# Simulation
# ----------------------------------------------------------------------------------------------
def simulate(scen, price_m=1.0, conv_m=1.0, churn_m=1.0, cogs_m=1.0, trial_m=1.0):
    team, pro = P["team_price"] * price_m, P["pro_price"] * price_m
    arpa_list = (1 - P["pro_mix"]) * team + P["pro_mix"] * pro
    arpa_net = arpa_list * (1 - P["contributor_share"] * P["contributor_discount"])
    idx_annual = ((1 - P["index_ent_mix"]) * P["index_std_price"] + P["index_ent_mix"] * P["index_ent_price"]) * price_m
    ltb_price = P["ltb_study_price"] * price_m
    var_saas = (P["saas_hosting_per_acct"] + P["saas_data_per_acct"] + P["support_h_per_acct"] * P["support_rate"]) * cogs_m
    var_idx = P["index_support_h"] * P["support_rate"] * cogs_m

    acc_L = acc_P = lic = 0.0
    cash = P["founder_cash"]
    ft = hired = False
    ft_month = hire_month = None
    hist = []
    adds_total = mkt_spend_total = 0.0
    for m in range(1, P["months"] + 1):
        pm = price_mult(m, scen)
        prev = price_mult(m - 3, scen) if m > 3 else 1.0
        U = max(0.1, min(1.0, pm))                       # shortage urgency (1 = at/above 2026 peak)
        V = abs(pm / prev - 1.0)                          # 3-month price move
        cap_mult = (P["hire_capacity_mult"] if hired else 1.0)
        # --- SaaS acquisition and churn
        trials = 0.0
        if m >= P["saas_launch_month"]:
            cap = (P["trials_cap_ft"] if ft else P["trials_cap_pt"]) * cap_mult
            raw = min(cap, P["trials_at_launch"] + P["trials_growth"] * (m - P["saas_launch_month"]))
            trials = raw * trial_m
        conv = P["trial_conversion"] * conv_m
        new_L = trials * conv * P["lifecycle_floor"]
        new_P = trials * conv * (1 - P["lifecycle_floor"]) * U
        ch_L = P["churn_base"] * churn_m
        ch_P = min(0.5, (P["churn_base"] + P["churn_glut_extra"] * (1 - U)) * churn_m)
        acc_L = acc_L * (1 - ch_L) + new_L
        acc_P = acc_P * (1 - ch_P) + new_P
        accts = acc_L + acc_P
        adds_total += new_L + new_P
        # --- index licences
        new_lic = 0.0
        if m >= P["index_first_sale_month"]:
            vol_term = P["index_floor"] + (1 - P["index_floor"]) * min(1.0, V / P["vol_ref"])
            new_lic = P["index_rate"] * conv_m * vol_term * (P["ft_capacity_index_mult"] if ft else 1.0) * cap_mult
        ich = (P["index_churn_flat"] if (m > 24 and V < 0.02) else P["index_churn"]) * churn_m
        lic = lic * (1 - ich) + new_lic
        # --- LTB studies (EOL-driven)
        ltb = 0.0
        if m >= P["saas_launch_month"]:
            y, _ = cal(m)
            eolm = EOL_MULT[scen] if y >= 2028 else 1.0
            ltb = min((P["ltb_cap_ft"] if ft else P["ltb_cap_pt"]) * cap_mult,
                      (P["ltb_attach"] * accts + P["ltb_inbound"]) * eolm)
        # --- revenue
        dp = P["design_partner_arpa_factor"] if m <= P["design_partner_until"] else 1.0
        rev_saas = accts * arpa_net * dp
        rev_idx = lic * idx_annual / 12.0
        rev_ltb = ltb * ltb_price
        rev = rev_saas + rev_idx + rev_ltb
        mrr = rev_saas + rev_idx
        # --- COGS
        fixed = 0.0
        if m >= P["saas_launch_month"]:
            fixed += P["fixed_hosting"] + (P["nexar_pro"] if accts >= P["nexar_pro_trigger_accts"] else P["nexar_standard"])
        if m >= P["display_licence_from"]:
            fixed += P["display_licence"]
        if m >= P["index_methodology_month"]:
            fixed += P["dramx_silver_yr"] / 12.0
        fixed *= cogs_m
        cogs = accts * var_saas + lic * var_idx + rev_ltb * P["ltb_cogs_share"] * cogs_m + rev * P["payment_fee"] + fixed
        gp = rev - cogs
        # --- opex
        mkt = (P["marketing_post"] if m >= P["saas_launch_month"] else P["marketing_pre"]) + trials * P["cost_per_trial"]
        mkt_spend_total += mkt if m >= P["saas_launch_month"] else 0.0
        opex_ns = P["tools"] + mkt + P["accounting"] + (P["insurance"] if m >= P["saas_launch_month"] else 0.0)
        opex_ns += P["legal_onetime"] if m == P["legal_month"] else 0.0
        opex_ns += P["travel"] if m in (10, 22, 34) else 0.0
        salary = (P["founder_salary_ft"] if ft else 0.0) + (P["hire_cost"] if hired else 0.0)
        net = gp - opex_ns - salary
        cash += net
        hist.append(dict(m=m, lab=label(m), pm=pm, U=U, V=V, trials=trials, accts=accts, acc_P=acc_P, acc_L=acc_L,
                         lic=lic, ltb=ltb, rev=rev, rev_saas=rev_saas, rev_idx=rev_idx, rev_ltb=rev_ltb, mrr=mrr,
                         cogs=cogs, fixed=fixed, gp=gp, opex=opex_ns, salary=salary, net=net, cash=cash,
                         ft=ft, hired=hired, sal_cover=gp - opex_ns - P["founder_salary_ft"]))
        # --- state transitions (take effect next month)
        if not ft and m >= 3:
            last3 = hist[-3:]
            if sum(h["gp"] - h["opex"] for h in last3) / 3.0 >= P["founder_salary_ft"]:
                ft, ft_month = True, m + 1
        if ft and not hired and mrr >= P["hire_trigger_mrr"]:
            hired, hire_month = True, m + 1
    cac = mkt_spend_total / adds_total if adds_total else float("nan")
    return dict(hist=hist, ft_month=ft_month, hire_month=hire_month, arpa_list=arpa_list, arpa_net=arpa_net,
                idx_annual=idx_annual, ltb_price=ltb_price, var_saas=var_saas, var_idx=var_idx, cac=cac)


def sustained_first(hist, key, n=3):
    for i in range(len(hist) - n + 1):
        if all(hist[j][key] >= 0 for j in range(i, i + n)):
            return hist[i]["m"]
    return None


def summarize(r):
    h = r["hist"]
    low = min(h, key=lambda x: x["cash"])
    arr = {mm: 12 * h[mm - 1]["mrr"] for mm in (12, 18, 24, 36)}
    return dict(be_net=sustained_first(h, "net"), be_sal=sustained_first(h, "sal_cover"),
                low=low["cash"], low_m=low["m"], arr=arr, ft=r["ft_month"], hire=r["hire_month"],
                acc18=h[17]["accts"], acc36=h[35]["accts"], lic18=h[17]["lic"], lic36=h[35]["lic"],
                cash36=h[35]["cash"])


def fm(x):
    return "never" if x is None else "m%d (%s)" % (x, label(x))


# ----------------------------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------------------------
def main():
    print("DD2 lifecycle-intel unit-economics model  |  as of 2026-11-01  |  model month 1 = %s" % label(1))
    print("DDR5 reference source: %s" % REF_SRC)
    print("  incumbent cost $%.2f/GB | Q4-2026 contract $%.2f/GB | glut $%.2f/GB | severe $%.2f/GB | 64GB RDIMM $%.1f/user-GB (glut $%.1f)"
          % (REF["cost_component_usd_per_gb"], P_Q4_2026, P_GLUT, P_SEVERE,
             REF["contract_rdimm64_usd_per_user_gb_q4_2026"], REF["glut_rdimm64_usd_per_user_gb"]))

    section("1. INPUTS (value | source or ESTIMATE basis)")
    rows = []
    for key, (v, src) in INPUTS.items():
        vs = ",".join("%g" % x for x in v) if isinstance(v, tuple) else ("%g" % v if isinstance(v, (int, float)) else str(v))
        rows.append([key, vs, src])
    table(["input", "value", "source / basis"], rows, ["l", "r", "l"])

    section("2. DDR5 contract price path by scenario ($/GB, quarter-end) and what drives demand")
    rows = []
    for m in range(1, 37):
        if cal(m)[1] in (3, 6, 9, 12):
            rows.append([label(m)] + ["%.2f" % (P_Q4_2026 * price_mult(m, s)) for s in SCENARIOS])
    table(["quarter-end", "BASE", "GLUT", "SEVERE"], rows)
    print("Urgency U = price/Q4-2026 (clipped 0.1-1) scales price-motivated sign-ups and churn; 3-month |move| drives index sales.")

    runs = {s: simulate(s) for s in SCENARIOS}
    sums = {s: summarize(runs[s]) for s in SCENARIOS}
    b = runs["BASE"]

    section("3. Unit economics per product line (list prices; variable COGS; BASE)")
    rows = []
    for name, price_mo, var in (("SaaS Team ($/acct-mo)", P["team_price"], b["var_saas"]),
                                ("SaaS Pro ($/acct-mo)", P["pro_price"], b["var_saas"] * 1.5),
                                ("SaaS blended net ($/acct-mo)", b["arpa_net"], b["var_saas"] + P["pro_mix"] * 0.5 * b["var_saas"]),
                                ("Index Standard ($/licence-mo)", P["index_std_price"] / 12, b["var_idx"]),
                                ("Index Enterprise ($/licence-mo)", P["index_ent_price"] / 12, b["var_idx"] * 2),
                                ("LTB study ($/study)", P["ltb_study_price"], P["ltb_study_price"] * P["ltb_cogs_share"])):
        varc = var + price_mo * P["payment_fee"]
        rows.append([name, "%.0f" % price_mo, "%.0f" % varc, pct(1 - varc / price_mo)])
    table(["line", "price", "var COGS", "contribution margin"], rows)
    print("Note: the Pro row assumes 1.5x support load and the blended row includes it; the simulation uses one support load for all accounts (small optimism, ~1 pt GM).")
    h = b["hist"]
    life = 1.0 / P["churn_base"]
    cm = b["arpa_net"] - b["var_saas"] - b["arpa_net"] * P["payment_fee"]
    print("SaaS CAC (marketing + paid trials, founder time excluded) = %s per account; lifetime ~%.0f months at base churn;"
          % (money(b["cac"]), life))
    print("  LTV = %s; LTV/CAC = %.1f; CAC payback = %.1f months" % (money(cm * life), cm * life / b["cac"], b["cac"] / cm))
    cac_full = b["cac"] + P["founder_sales_h_per_trial"] * P["founder_h_value"] / P["trial_conversion"]
    print("Fully loaded CAC (adds %.0f founder h/trial at $%.0f/h imputed) = %s; LTV/CAC = %.1f; payback = %.1f months"
          % (P["founder_sales_h_per_trial"], P["founder_h_value"], money(cac_full), cm * life / cac_full, cac_full / cm))
    print("Index licence: no paid acquisition modelled; each sale needs both contract parties' legal/procurement sign-off (C-86 audit).")
    rows = []
    for mm in (12, 18, 24, 36):
        x = h[mm - 1]
        rows.append([label(mm), money(x["rev"]), money(x["cogs"]), money(x["fixed"]), pct(x["gp"] / x["rev"]) if x["rev"] else "n/a"])
    table(["BASE month", "revenue/mo", "COGS/mo", "of which fixed data/infra", "blended GM"], rows)

    section("4. BASE monthly P&L and cash (USD; founder unpaid until full-time switch)")
    rows = []
    for x in h:
        rows.append([x["m"], x["lab"], "%.2f" % (P_Q4_2026 * x["pm"]), "%.0f" % x["trials"], "%.1f" % x["accts"], "%.1f" % x["lic"],
                     "%.1f" % x["ltb"], k(x["rev"]), k(x["cogs"]), k(x["gp"]), k(x["opex"]), k(x["salary"]), k(x["net"]),
                     money(x["cash"]), "FT" if x["ft"] else "PT"])
    table(["m", "month", "$/GB", "trials", "accts", "idx lic", "LTB", "rev", "COGS", "GP", "opex", "salary", "net", "cash", "mode"], rows)

    section("5. GLUT and SEVERE monthly cash and MRR (side by side with BASE)")
    rows = []
    for i in range(36):
        rows.append([i + 1, label(i + 1)] + [money(runs[s]["hist"][i]["cash"]) for s in SCENARIOS]
                    + [k(runs[s]["hist"][i]["mrr"]) for s in SCENARIOS])
    table(["m", "month", "cash BASE", "cash GLUT", "cash SEVERE", "MRR BASE", "MRR GLUT", "MRR SEVERE"], rows)

    section("6. Scenario summary")
    rows = []
    for s in SCENARIOS:
        z = sums[s]
        rows.append([s, fm(z["be_net"]), fm(z["be_sal"]), fm(z["ft"]), "%s @ m%d" % (money(z["low"]), z["low_m"]),
                     money(z["arr"][12]), money(z["arr"][18]), money(z["arr"][24]), money(z["arr"][36]), money(z["cash36"])])
    table(["scenario", "breakeven (founder unpaid)", "covers $10k/mo salary", "full-time from", "cash low point",
           "ARR m12", "ARR m18", "ARR m24", "ARR m36", "cash m36"], rows)
    rows = []
    for s in SCENARIOS:
        z, x = sums[s], runs[s]["hist"][35]
        mix = (x["acc_P"] * runs[s]["arpa_net"], x["acc_L"] * runs[s]["arpa_net"], x["rev_idx"], x["rev_ltb"])
        tot = sum(mix) or 1.0
        rows.append([s, "%.0f" % z["acc18"], "%.0f" % z["acc36"], "%.1f" % z["lic18"], "%.1f" % z["lic36"]]
                    + [pct(v / tot) for v in mix])
    table(["scenario", "accts m18", "accts m36", "licences m18", "licences m36", "m36 rev: price-driven SaaS",
           "lifecycle SaaS", "index", "LTB studies"], rows)
    print("ARR = 12 x (SaaS + index MRR); one-off LTB study revenue is excluded from ARR but included in P&L/cash.")
    print("\nGlut behaviour by module: monthly revenue at m36 (%s) and change vs BASE" % label(36))
    rows = []
    xb = runs["BASE"]["hist"][35]
    lines = (("buy/hold + allocation alerts (price-motivated SaaS)", lambda r, x: x["acc_P"] * r["arpa_net"]),
             ("EOL/lifecycle + NVM cross-ref + LTB sizer (lifecycle SaaS)", lambda r, x: x["acc_L"] * r["arpa_net"]),
             ("Memory Cost Escalation Index licences", lambda r, x: x["rev_idx"]),
             ("LTB studies (one-off)", lambda r, x: x["rev_ltb"]))
    for nm, f in lines:
        vb = f(runs["BASE"], xb)
        row = [nm]
        for s in SCENARIOS:
            v = f(runs[s], runs[s]["hist"][35])
            row.append(money(v) + ("" if s == "BASE" else " (%+.0f%%)" % (100 * (v / vb - 1) if vb else 0)))
        rows.append(row)
    table(["module", "BASE", "GLUT", "SEVERE"], rows)

    section("7. Sensitivity (each input x0.7 and x1.3; all else BASE/GLUT)")
    for s in ("BASE", "GLUT"):
        print("\n-- %s --" % s)
        rows = []
        z0 = sums[s]
        rows.append(["(base case)", "", money(z0["arr"][18]), money(z0["arr"][36]), fm(z0["be_sal"]), money(z0["low"])])
        for nm, kw in (("price (all lines)", "price_m"), ("conversion/close rate", "conv_m"), ("churn", "churn_m"), ("COGS", "cogs_m")):
            for mult in (0.7, 1.3):
                z = summarize(simulate(s, **{kw: mult}))
                rows.append([nm, "x%.1f" % mult, money(z["arr"][18]), money(z["arr"][36]), fm(z["be_sal"]), money(z["low"])])
        table(["driver", "mult", "ARR m18", "ARR m36", "covers $10k/mo salary", "cash low"], rows)

    section("8. What must be true")
    arpa_yr = 12 * b["arpa_net"]
    # salary-coverage requirement at steady state (no index): N*(arpa*(1-fee) - var) >= salary + fixed + opex
    fixed_ss = P["fixed_hosting"] + P["nexar_standard"] + P["display_licence"] + P["dramx_silver_yr"] / 12
    opex_ss = P["tools"] + P["marketing_post"] + P["accounting"] + P["insurance"] + P["trials_cap_pt"] * P["cost_per_trial"]
    need_sal = (P["founder_salary_ft"] + fixed_ss + opex_ss) / (b["arpa_net"] * (1 - P["payment_fee"]) - b["var_saas"])
    print("Blended net ARPA = %s/mo (%s/yr). Index blended licence = %s/yr." % (money(b["arpa_net"]), money(arpa_yr), money(b["idx_annual"])))
    print("To pay the founder $10k/mo from SaaS alone: >= %.0f paying accounts (or ~%.0f accounts + 10 index licences)."
          % (need_sal, need_sal - 10 * (b["idx_annual"] / 12 - b["var_idx"]) / (b["arpa_net"] * (1 - P["payment_fee"]) - b["var_saas"])))
    print("WHAT MUST BE TRUE for a full-time founder by m18 (%s): >= %.0f paying accounts (or ~%.0f + 10 licences) by then;"
          % (label(18), need_sal, need_sal - 10 * (b["idx_annual"] / 12 - b["var_idx"]) / (b["arpa_net"] * (1 - P["payment_fee"]) - b["var_saas"])))
    print("   modelled BASE at m18 = %.0f accounts + %.1f licences -> founder %s (full-time switch %s)." % (
        sums["BASE"]["acc18"], sums["BASE"]["lic18"],
        "can go full-time" if (sums["BASE"]["ft"] or 99) <= 18 else "still part-time", fm(sums["BASE"]["ft"])))
    print("   Kill-experiment gate implied: >= 5 paid deposits from 25 qualified conversations (20%) supports the 12% trial conversion.")
    for target in (1_000_000, 2_000_000):
        lo, hi = 0.5, 40.0
        for _ in range(40):
            mid = (lo + hi) / 2
            z = summarize(simulate("BASE", trial_m=mid, conv_m=1.0))
            if z["arr"][36] >= target:
                hi = mid
            else:
                lo = mid
        z = summarize(simulate("BASE", trial_m=hi))
        zg = summarize(simulate("GLUT", trial_m=hi))
        print("ARR %s by m36 (BASE) needs SaaS trial inflow x%.1f the modelled level (~%.0f qualified trials/month part-time, ~%.0f full-time),"
              % (money(target), hi, hi * P["trials_cap_pt"], hi * P["trials_cap_ft"]))
        print("   i.e. ~%.0f paying accounts + %.0f licences by m18 and ~%.0f accounts by m36 = %.1f%% of an estimated %d U.S. SMB OEMs;"
              % (z["acc18"], z["lic18"], z["acc36"], 100 * z["acc36"] / P["tam_us_smb_oems"], P["tam_us_smb_oems"]))
        print("   the same funnel under GLUT reaches %s ARR at m36." % money(zg["arr"][36]))
    print("Pure-SaaS accounts for $1M ARR: %.0f; for $2M ARR: %.0f (at %s/yr)." % (1e6 / arpa_yr, 2e6 / arpa_yr, money(arpa_yr)))
    print("Pure-index licences for $1M ARR: %.0f (at %s/yr) -- vs DRAMeXchange's paid tiers $5k-55k/yr." % (1e6 / b["idx_annual"], money(b["idx_annual"])))

    section("9. Headline")
    for s in SCENARIOS:
        z = sums[s]
        hh = runs[s]["hist"]
        print("%-6s GM m18 %s, m36 %s | breakeven (unpaid) %s | covers $10k salary %s | cash low %s (m%d) | ARR m18 %s | ARR m36 %s"
              % (s, pct(hh[17]["gp"] / hh[17]["rev"]), pct(hh[35]["gp"] / hh[35]["rev"]), fm(z["be_net"]), fm(z["be_sal"]),
                 money(z["low"]), z["low_m"], money(z["arr"][18]), money(z["arr"][36])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
