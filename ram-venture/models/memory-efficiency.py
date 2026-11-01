#!/usr/bin/env python3
"""DD4 -- Memory Efficiency for On-Prem & Self-Hosted Fleets: unit-economics model.

Agent key: p4-memory-efficiency.  As of 2026-11-01.  Pure Python 3 stdlib.
Phase 5 red-team revisions: agent p5r-memory-efficiency, 2026-11-01. See the "RED-TEAM REVISIONS (Phase 5)"
block below INPUTS. Set APPLY_RED_TEAM = False to reproduce the Phase 4 numbers exactly.
Run:  cd ram-venture && python3 models/memory-efficiency.py
      (prints every table, writes research/phase4/memory-efficiency_model_output.md, exits 0)

The bundle has three product lines, run as one part-time company:
  C-73  Cloud memory FinOps audit. A fixed-fee report plus a small monitoring subscription. AWS list
        prices did not move in 2026, so this line ignores DRAM prices. Its job is cash and leads.
  C-74  On-prem "memory reclaim autopilot". A per-node agent tunes zswap/zram, PSI-driven proactive
        reclaim (Senpai/TMO-style) and DAMON_RECLAIM under SLO guardrails. Price = a share of the
        DRAM purchase it defers, capped at a list price. Its value moves with the DRAM price.
  C-75  KV-cache tier integration (LMCache / NVIDIA Dynamo KVBM / SGLang HiCache / Mooncake) for
        self-hosted LLM teams. A one-time engagement plus a monitoring/upgrade retainer. Its value is
        GPU-hours avoided, so it ignores DRAM prices, but the open-source stack is commoditizing it.

Each scenario simulates 36 months, Nov-2026 to Oct-2029, from the founder's $40k (A-03). The founder
starts part-time at 15 h/week and goes full-time only once the gross profit left after non-salary
opex covers a $10k/month loaded salary.

The model works in expected values: customers can be fractional. Read it as a central case, not a
forecast. Every INPUTS entry carries a source URL or "ESTIMATE: basis". "(snippet)" means the number
was seen only in a search-result snippet; the full log is research/sources/p4-memory-efficiency.jsonl.
"""
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

AS_OF = "2026-11-01"
HERE = Path(__file__).resolve().parent
RV = HERE.parent
OUT_MD = RV / "research" / "phase4" / "memory-efficiency_model_output.md"

# ----------------------------------------------------------------------------------------------
# DDR5 reference deck: live import from the Phase-1 cost stack, with the canonical numbers as fallback
# ----------------------------------------------------------------------------------------------
FALLBACK_REF = {
    "cost_component_usd_per_gb": 1.48,
    "contract_component_usd_per_gb_q4_2026": 20.37,
    "contract_rdimm64_usd_per_user_gb_q4_2026": 25.8,
    "glut_component_usd_per_gb": 8.15,
    "glut_rdimm64_usd_per_user_gb": 10.3,
    "severe_glut_component_usd_per_gb": 2.04,
}
sys.path.insert(0, str(HERE))
try:
    with redirect_stdout(io.StringIO()):
        from dram_cost_stack import ddr5_reference  # noqa: E402
        REF = ddr5_reference()
    REF_SOURCE = "models/dram_cost_stack.py ddr5_reference() (live import)"
except Exception as exc:  # pragma: no cover - fallback path
    REF = dict(FALLBACK_REF)
    REF_SOURCE = "canonical fallback numbers from the DD4 task spec (import failed: %r)" % (exc,)

MODULE_TO_COMPONENT = REF["contract_rdimm64_usd_per_user_gb_q4_2026"] / REF["contract_component_usd_per_gb_q4_2026"]

# ----------------------------------------------------------------------------------------------
# INPUTS: name -> (value, source).  Source = URL or "ESTIMATE: basis".
# ----------------------------------------------------------------------------------------------
_TMO = "https://par.nsf.gov/servlets/purl/10332477"
_GOOG = "https://lpc.events/event/4/contributions/561/attachments/363/596/Persistent_Memory_as_Memory.pdf"
_AMC4 = "https://www.amcompute.com/appraisals/ddr4-64gb-rdimm"
_PROS = "https://www.usage.ai/blogs/finops/tools/prosperops-pricing/"
_CAST = "https://www.costbench.com/software/cloud-cost-management/cast-ai/"
_KUBE = "https://costbench.com/software/cloud-cost-management/kubecost/"
_DDOG = "https://costbench.com/compare/datadog-vs-new-relic/"
_C74 = "research/phase2/concepts_master.json C-74 card + research/phase3/verify/batch_11.json"
_C75 = "research/phase2/concepts_master.json C-75 card + research/phase3/verify/batch_11.json"
_C73 = "research/phase2/concepts_master.json C-73 card + research/phase3/verify/batch_11.json"

INPUTS = {
    # --- Founder and company (ASSUMPTIONS.md A-03) ---
    "founder_capital": (40_000.0, "ASSUMPTIONS.md A-03: $40k deployable"),
    "founder_hours_pt": (65.0, "ASSUMPTIONS.md A-03: ~15 h/week = ~65 h/month part-time"),
    "founder_hours_ft": (170.0, "ESTIMATE: full-time month of ~40 h/week"),
    "founder_salary_ft": (10_000.0, "ASSUMPTIONS.md A-03: ~$120k/yr loaded once full-time"),
    "founder_labor_rate": (75.0, "ESTIMATE: imputed $/h used only for the labor-loaded gross-margin view"),

    # --- DRAM value deck ($/GB) ---
    "rdimm_peak_usd_gb": (REF["contract_rdimm64_usd_per_user_gb_q4_2026"],
                          REF_SOURCE + ": 64GB DDR5 RDIMM contract per user-GB, Q4-2026"),
    "rdimm_glut_usd_gb": (REF["glut_rdimm64_usd_per_user_gb"], REF_SOURCE + ": A-05 glut (-60%) per user-GB"),
    "rdimm_severe_usd_gb": (REF["severe_glut_component_usd_per_gb"] * MODULE_TO_COMPONENT,
                            "ESTIMATE: severe component $/GB (ddr5_reference) x RDIMM/component ratio %.3f"
                            % MODULE_TO_COMPONENT),
    "ddr4_used_usd_gb": (4.45, _AMC4 + " (snippet): used 64GB DDR4 RDIMM $250-370; landscape 1b $3.1-5.8/GB; midpoint"),
    "ddr4_trough_usd_gb": (1.30, "01_LANDSCAPE.md §1 row 4a: DDR4 8Gb fixed-price trough $1.30 (Sep-2023, KED Global)"),
    "base_turn_pct": (0.30, "ESTIMATE: BASE turn in 2028 sits between BofA -10% 2028 ASP and the A-05 -60% glut (01_LANDSCAPE §1 4b)"),
    "glut_ddr4_turn_pct": (0.50, "ESTIMATE: A-05 says legacy DDR4 falls less in % than DDR5 and stays above the 2023 trough"),
    "turn_start": ((2028, 1), "01_LANDSCAPE.md F2 (downturn most likely begins 2028) + task spec (GLUT from 2028-Q1)"),
    "turn_ramp_months": (12, "https://press.trendforce.com/node/view/3173.html: 2018-19 analog, -62.5% in ~4 quarters (via 01_LANDSCAPE §1 4a)"),

    # --- C-74 reclaim autopilot: technical value ---
    "node_gb": (512.0, "ESTIMATE: C-74 reference fleet node (200 x 512GB) in " + _C74),
    "reclaim_frac": (0.10, "ESTIMATE: share of installed RAM freed. Google zswap ~5% of fleet RAM (" + _GOOG +
                     ", snippet); Meta TMO 20-32% (" + _TMO + ", snippet); DAMON_RECLAIM lab 32-40% (LKML RFC)"),
    "ddr5_share": (0.60, "ESTIMATE: targeting rule (sell to operators buying DDR5 servers in 2026-27); the other 40% of node-GB is DDR4 valued at used prices (p3-audit-11 C-74 correction)"),
    "contract_months": (36, "ESTIMATE: 3-year term spreads the one-time deferred-DRAM value"),
    "value_realization": (1.0, "Phase 4: linear GB x $/GB value treated as fully avoided DRAM (revised in RED-TEAM block)"),
    "acq_stop_price_frac": (0.0, "Phase 4: kill criterion 9 (stop new C-74 acquisition below 60% of peak) not wired into the model"),
    "acq_stop_max_cust": (8.0, "04_DEEPDIVES/memory-efficiency.md §11 kill 9: the stop applies only before 8 C-74 customers"),
    "contract_lag_months": (6, "ESTIMATE: annual contracts reprice at renewal, so the fee lags the DRAM price by ~6 months on average"),
    "savings_share": (0.30, _PROS + " (snippet): ProsperOps ~30-35% of realized savings; Zesty 25% (https://www.usage.ai/?p=6180)"),
    "list_price_node_month": (10.0, "ESTIMATE: C-74 card $500-2k/mo for 50-200 nodes; cf. Datadog infra $15/host/mo (" + _DDOG +
                              "), Kubecost $449/100 nodes (" + _KUBE + "), CAST AI $5/vCPU/mo (" + _CAST + ")"),
    "nodes_per_customer": (80.0, "ESTIMATE: mid of the C-74 card's 50-200-node pilot range"),
    "node_expansion_pm": (0.005, "ESTIMATE: +6%/yr fleet growth at existing customers"),
    "hosting_per_node": (0.25, "ESTIMATE: control-plane hosting + metrics storage $/node/month"),
    "support_pct": (0.10, "ESTIMATE: contractor support time as a share of C-74 subscription revenue (" + _C74 + ": incident/on-call cost)"),
    "oncall_small": (750.0, "ESTIMATE: kernel-savvy on-call retainer $/month with 1-5 customers"),
    "oncall_large": (2_000.0, "ESTIMATE: on-call retainer $/month with 6+ customers"),
    "oncall_threshold": (6.0, "ESTIMATE: customer count at which on-call moves to the larger retainer"),
    "pilot_fee": (2_000.0, "ESTIMATE: paid 60-day pilot fee; C-74 card says paid pilot after the volunteer-host test"),
    "pilot_cost": (2_100.0, "ESTIMATE: 12 h kernel contractor x $175/h per pilot (" + _C74 + ": $150-200/h)"),
    "scan_cost": (200.0, "ESTIMATE: 1 h contractor + hosting per free 14-day cold-memory scan (booked as sales & marketing opex)"),
    "c74_build_cost": (17_500.0, "ESTIMATE: 100 h kernel contractor x $175/h (" + _C74 + " said ~300 h; scoped to an MVP to fit $40k)"),
    "c74_build_months": ((2, 5), "ESTIMATE: build spread over months 2-5"),
    "c74_sell_start": (5, "ESTIMATE: outreach starts when the read-only scanner is ready (month 5)"),
    "c74_agent_ready": (6, "ESTIMATE: guarded agent ready for paid pilots in month 6"),
    "test_infra_pm": (250.0, "ESTIMATE: rented bare-metal test hosts $/month from month 2"),
    "soc2_cost": (12_000.0, "ESTIMATE: SOC 2 Type I readiness + audit for a small vendor"),
    "soc2_trigger_customers": (5.0, "ESTIMATE: buyers start asking for SOC 2 at ~5 C-74 customers"),

    # --- C-74 funnel ---
    "touches_pt": (40.0, "ESTIMATE: targeted outbound touches/month part-time (~10 h)"),
    "touches_ft": (120.0, "ESTIMATE: outbound touches/month full-time"),
    "hours_per_touch": (0.25, "ESTIMATE: research + personalised message"),
    "reply_rate": (0.08, "ESTIMATE: B2B infra outbound reply-to-conversation rate"),
    "inbound_max": (4.0, "ESTIMATE: inbound conversations/month from an open-source cold-memory scanner + write-ups"),
    "inbound_ramp": ((9, 15), "ESTIMATE: inbound ramps from month 9 to month 15"),
    "conv_to_scan": (0.35, "ESTIMATE: conversation -> free 14-day read-only scan"),
    "scan_to_pilot": (0.40, "ESTIMATE: scan -> paid pilot"),
    "pilot_to_sub": (0.60, "ESTIMATE: paid pilot -> subscription (conservative ops buyers; one incident ends it)"),
    "pain_floor": (0.40, "ESTIMATE: share of conversion left with zero DRAM pain (density/SLO value); scaled by RDIMM price/peak"),
    "c74_churn_pm": (0.015, "ESTIMATE: 1.5%/month base logo churn"),
    "c74_glut_churn_uplift": (0.020, "ESTIMATE: extra churn x (1 - price/peak): once RAM is cheap again, buyers just buy RAM (" + _C74 + " glut_reason)"),

    # --- C-73 cloud audit (lead magnet / cash bridge) ---
    "c73_price": (3_000.0, "ESTIMATE: low end of the card's $3-8k fixed-fee audit (" + _C73 + ")"),
    "c73_cogs": (150.0, "ESTIMATE: tooling/cloud cost per audit"),
    "c73_hours": (14.0, "ESTIMATE: founder hours per audit"),
    "c73_rate_pt": (0.33, "ESTIMATE: ~1 audit/quarter from the founder's network, part-time (network is manufacturing, not SaaS)"),
    "c73_rate_ft": (1.0, "ESTIMATE: audits/month full-time"),
    "c73_start": (5, "ESTIMATE: first audit in month 5 -- p3-audit-11 corrected C-73 to 4-8 months to a first audit (" + _C73 + ")"),
    "c73_to_monitor": (0.10, "ESTIMATE: audit -> $250/mo monitoring; scorers say no shortage pain in cloud (AWS list prices unchanged)"),
    "c73_monitor_price": (250.0, _C73 + ": ~$270/mo fee per $40k-bill customer (D d_calcs.py)"),
    "c73_monitor_cogs": (25.0, "ESTIMATE: hosting per monitoring account"),
    "c73_monitor_churn": (0.06, "ESTIMATE: report-only product churns once savings are booked (" + _C73 + " fatal_flaw)"),
    "c73_to_c74_convs": (0.25, "ESTIMATE: C-74 conversations generated per cloud audit (hybrid/colo referrals)"),

    # --- C-75 KV-cache integration ---
    "c75_enabled": (1, "ESTIMATE: the line is on in the base bundle"),
    "c75_benchmark_cost": (6_000.0, "ESTIMATE: ~$3k rented 8xH100 hours + ~$3k inference contractor (" + _C75 + " said $5-15k)"),
    "c75_benchmark_months": ((6, 7), "ESTIMATE: public benchmark published months 6-7"),
    "c75_start": (9, "ESTIMATE: first engagement possible after the benchmark and a discounted reference"),
    "c75_deal_rate_pt": (0.15, "ESTIMATE: engagements/month part-time (~1 every 7 months)"),
    "c75_deal_rate_ft": (0.35, "ESTIMATE: engagements/month full-time"),
    "c75_decay_floor": (0.30, "ESTIMATE: deal flow falls to 30% by month 24 -- Red Hat AI 3.5 ships CPU KV offload GA (2026-09-09, https://aicybr.com/blog/red-hat-ai-3-5-enterprise-inference-agents), Tensormesh Platform launched 2026-10-15 (https://www.hpcwire.com/aiwire/2026/10/15/tensormesh-targets-redundant-llm-computation-with-enterprise-caching-platform/)"),
    "c75_decay_month": (24, "ESTIMATE: month by which the decay floor is reached"),
    "c75_glut_factor": (0.80, "ESTIMATE: a DRAM glut implies an AI-capex slowdown that thins self-hosted LLM projects (01_LANDSCAPE §10.4 #11 via founder_3 scorer)"),
    "c75_price": (25_000.0, _C75 + ": $15-40k integration engagement (midpoint-ish)"),
    "c75_cogs": (10_000.0, "ESTIMATE: 45 h inference contractor x $200/h + $1k GPU time per engagement"),
    "c75_hours": (40.0, "ESTIMATE: founder hours per engagement"),
    "c75_to_retainer": (0.60, "ESTIMATE: engagement -> monitoring/upgrade retainer"),
    "c75_retainer_price": (1_500.0, "ESTIMATE: keep up with vLLM/LMCache releases (65 LMCache PyPI releases May-2025..Oct-2026, D notes)"),
    "c75_retainer_cogs_pct": (0.30, "ESTIMATE: contractor upkeep share of retainer"),
    "c75_retainer_churn": (0.04, "ESTIMATE: 4%/month as defaults absorb the integration (Tensormesh/NVIDIA/Red Hat)"),

    # --- Opex and founder-hour budget ---
    "legal_setup": (1_500.0, "ESTIMATE: LLC, contracts, MSA template (month 1)"),
    "tools_pm": (300.0, "ESTIMATE: SaaS tools, CRM, domain, accounting"),
    "marketing_pt": (250.0, "ESTIMATE: part-time marketing/events $/month"),
    "marketing_ft": (1_000.0, "ESTIMATE: full-time marketing/events $/month"),
    "insurance_pm": (200.0, "ESTIMATE: tech E&O + cyber $/month from first pilot (agent changes production memory)"),
    "dev_hours_early": (25.0, "ESTIMATE: founder product hours/month, months 1-12"),
    "dev_hours_late": (15.0, "ESTIMATE: founder product hours/month after month 12"),
    "hours_per_c74_customer": (0.5, "ESTIMATE: founder account hours/customer/month"),
    "hours_per_scan": (3.0, "ESTIMATE: founder hours per free scan"),
    "hours_per_pilot_month": (5.0, "ESTIMATE: founder hours per pilot per month (2-month pilot)"),
    "hours_per_retainer": (3.0, "ESTIMATE: founder hours per C-75 retainer per month"),

    # --- Sensitivity multipliers (1.0 = base) ---
    "price_mult": (1.0, "ESTIMATE: sensitivity multiplier on all prices"),
    "conv_mult": (1.0, "ESTIMATE: sensitivity multiplier on conversion/close rates"),
    "churn_mult": (1.0, "ESTIMATE: sensitivity multiplier on all churn rates"),
    "cogs_mult": (1.0, "ESTIMATE: sensitivity multiplier on all COGS items"),
}

# ----------------------------------------------------------------------------------------------
# RED-TEAM REVISIONS (Phase 5) -- agent p5r-memory-efficiency, 2026-11-01
# Four adversarial reviewers (VET, VC, HYP, PHY; research/phase5/rt_*.json) attacked DD4. Every accepted
# objection that changes an input is applied here, on top of INPUTS. The Phase 4 values stay in INPUTS
# for audit. Format: input -> (old, new, objection ids, basis). Responses in full:
# research/phase5/responses_memory-efficiency.json.
# ----------------------------------------------------------------------------------------------
APPLY_RED_TEAM = True
RED_TEAM_REVISIONS = {
    "reclaim_frac": (0.10, 0.06, "RT-HYP-DD4-02, RT-VC-DD4-03, RT-VET-DD4-02; also RT-PHY-DD4-04, RT-PHY-DD4-05",
                     "ESTIMATE: incremental reclaim over a STOCK Proxmox baseline (KSM on via ksmtuned at ~80% host RAM, "
                     "ballooning on), so the dedup slice is no longer ours; zswap + proactive reclaim only, zswap-only "
                     "(no SSD writeback) on boot media; hugepage/SEV/TDX hosts reclaim ~0. Google fleet zswap ~5% "
                     "(" + _GOOG + "); HYP's own run used 6%"),
    "savings_share": (0.30, 0.20, "RT-HYP-DD4-01",
                      "ESTIMATE: on-prem 'DIMMs not bought' is a counterfactual, not an invoice line like ProsperOps/"
                      "Zesty; procurement negotiates it toward a per-node licence benchmarked against Ubuntu Pro/RHEL "
                      "support (which includes tuned). HYP's number"),
    "value_realization": (1.0, 0.75, "RT-VC-DD4-02 (with RT-PHY-DD4-01, RT-VET-DD4-01 on the mean)",
                          "ESTIMATE: 36 months of freed capacity is worth its rental equivalent, not the full purchase: "
                          "P0 - PV(residual of 3-yr-old DIMMs) = 68% (flat prices) to 78% (BASE -30% turn) of P0 at 8%/yr "
                          "and 40% residual. VC's pure-deferral formula P0 - PV(P36) gives 44% in BASE but ignores the "
                          "extra life of later-bought DIMMs. DIMM-step quantization is mean-neutral across buyers "
                          "(E[saving] = P(cross) x step = r x S) so it moves conversion (pilot_to_sub), not this factor"),
    "ddr5_share": (0.60, 0.40, "RT-HYP-DD4-06, RT-VET-DD4-05",
                   "ESTIMATE: SMB MSP fleets on 4-6-yr refresh were still mostly DDR4 in late 2026 (DDR5 server platforms "
                   "only since late 2022/2023); VMware->Proxmox migrations often reuse existing hosts; shortage buyers "
                   "bought refurbished DDR4 in 2026. Between the reviewers' 0.30 and Phase 4's unsourced 0.60"),
    "oncall_small": (750.0, 2_500.0, "RT-HYP-DD4-04, RT-VC-DD4-04, RT-VET-DD4-04",
                     "ESTIMATE: a named 24/7 rotation with a 1-2 h response SLA; $750 bought ~4.3 contractor hours. "
                     "Midpoint of HYP's $2,000 and VET's ~$3,000 (~15 reserved h + availability premium)"),
    "oncall_large": (2_000.0, 3_000.0, "RT-VET-DD4-04", "ESTIMATE: VET's $3,000 retainer at 6+ customers"),
    "insurance_pm": (200.0, 400.0, "RT-HYP-DD4-04",
                     "ESTIMATE: tech E&O with limits that cover production-impact claims. Small-tech E&O averages "
                     "$67-110/mo (Insureon, https://www.insureon.com/small-business-insurance/errors-omissions/buy-for-less, "
                     "snippet); startup median $3,700/yr = $308/mo (Vouch via QuoteSweep, "
                     "https://www.quotesweep.com/blog/tech-startup-insurance-cost, snippet); x1.3 for higher limits. "
                     "HYP's $600 treated as the upper bound"),
    "scan_to_pilot": (0.40, 0.30, "RT-VC-DD4-05, RT-PHY-DD4-03, RT-VET-DD4-03",
                      "ESTIMATE: the competitor is the in-house admin with free upstream features; shops with no "
                      "kernel team are the least willing to let an outside agent touch production memory; HPC "
                      "rows (4 of the first ten, 15 of 60 targets) removed as physically mismatched"),
    "pilot_to_sub": (0.60, 0.40, "RT-PHY-DD4-01, RT-VET-DD4-01, RT-HYP-DD4-01",
                     "ESTIMATE: a pilot converts only where measured reclaim visibly changes a 2027 PO (fewer whole "
                     "nodes on memory-bound VM hosts, or a DIMM step). At 6% reclaim the DIMM-step crossing "
                     "probability is P ~ 0.06 x S/(dS) = 12-18% (PHY's formula), so ~1/3 of pilots show no PO delta"),
    "soc2_trigger_customers": (5.0, 2.0, "RT-VC-DD4-05",
                               "ESTIMATE: buyers ask for SOC 2 before an outside agent changes production memory"),
    "acq_stop_price_frac": (0.0, 0.60, "RT-HYP-DD4-05",
                            "§11 kill criterion 9 wired into the model: stop new C-74 acquisition once 64GB DDR5 RDIMM "
                            "is >40% below the 4Q26 peak and there are fewer than 8 C-74 customers (fires in GLUT/SEVERE, "
                            "not in BASE where the turn is -30%)"),
    "c75_enabled": (1, 0, "RT-HYP-DD4-04, RT-PHY-DD4-07",
                    "the DD's own recommendation is to drop C-75 apart from opportunistic consulting, so the headline "
                    "must not count it; PHY adds that host-DRAM KV tiers are bandwidth/NUMA-bound (sizing risk)"),
    "c73_rate_pt": (0.33, 0.17, "RT-VC-DD4-06",
                    "ESTIMATE: ~2 audits/yr; the founder's network is manufacturing, not cloud SaaS, and EC2 memory "
                    "prices did not move (no tailwind)"),
}
for _k, (_old, _new, _ids, _basis) in RED_TEAM_REVISIONS.items():
    assert _k in INPUTS, _k
    assert INPUTS[_k][0] == _old, (_k, INPUTS[_k][0], _old)

SCENARIOS = ("BASE", "GLUT", "SEVERE")
SCEN_DESC = {
    "BASE": "2026-27 prices hold; turn in 2028 (-30% over 2028, then flat)",
    "GLUT": "A-05: DDR5 -60% from 2028-Q1 (ramp over 2028 to the $10.3/user-GB glut line)",
    "SEVERE": "ramp over 2028 to the severe line ($2.04/GB component = $%.2f/user-GB RDIMM)" % INPUTS["rdimm_severe_usd_gb"][0],
}
MONTHS = 36


def base_params(overrides=None, red_team=None):
    p = {k: v[0] for k, v in INPUTS.items()}
    if APPLY_RED_TEAM if red_team is None else red_team:
        p.update({k: v[1] for k, v in RED_TEAM_REVISIONS.items()})
    if overrides:
        for k in overrides:
            if k not in p:
                raise KeyError("unknown override %s" % k)
        p.update(overrides)
    return p


# ----------------------------------------------------------------------------------------------
# Calendar and price paths
# ----------------------------------------------------------------------------------------------
def cal(m):
    t = 2026 * 12 + 10 + (m - 1)  # month 1 = Nov-2026
    return t // 12, t % 12 + 1


def label(m):
    y, mo = cal(m)
    return "%d-%02d" % (y, mo)


def dram_prices(m, scen, p):
    """(64GB DDR5 RDIMM $/user-GB, used DDR4 RDIMM $/GB) in month m under a scenario."""
    peak, d4 = p["rdimm_peak_usd_gb"], p["ddr4_used_usd_gb"]
    if scen == "BASE":
        t5, t4 = peak * (1 - p["base_turn_pct"]), d4 * (1 - p["base_turn_pct"])
    elif scen == "GLUT":
        t5 = p["rdimm_glut_usd_gb"]
        t4 = max(p["ddr4_trough_usd_gb"], d4 * (1 - p["glut_ddr4_turn_pct"]))
    elif scen == "SEVERE":
        t5, t4 = p["rdimm_severe_usd_gb"], p["ddr4_trough_usd_gb"]
    else:
        raise ValueError(scen)
    y, mo = cal(m)
    ty, tm = p["turn_start"]
    k = (y * 12 + mo) - (ty * 12 + tm)
    if k < 0:
        return peak, d4
    f = min(1.0, (k + 1) / p["turn_ramp_months"])
    return peak - (peak - t5) * f, d4 - (d4 - t4) * f


def node_value(m, scen, p):
    """Realized DRAM value ($) of reclaiming memory on one node in month m (linear GB x $/GB x realization)."""
    r5, r4 = dram_prices(m, scen, p)
    blended = p["ddr5_share"] * r5 + (1 - p["ddr5_share"]) * r4
    return p["node_gb"] * p["reclaim_frac"] * blended * p["value_realization"]


def fee_per_node(m, scen, p):
    """C-74 price $/node/month: savings share of deferred value over the term, capped at list."""
    mm = max(1, m - int(p["contract_lag_months"]))
    cap = node_value(mm, scen, p) / p["contract_months"] * p["savings_share"]
    return min(p["list_price_node_month"], cap) * p["price_mult"]


# ----------------------------------------------------------------------------------------------
# Simulation
# ----------------------------------------------------------------------------------------------
def simulate(scen, overrides=None, red_team=None):
    p = base_params(overrides, red_team)
    cm, km, um, gm_ = p["conv_mult"], p["churn_mult"], p["cogs_mult"], p["price_mult"]
    cash = p["founder_capital"]
    ft = False
    ft_month = None
    c74_cust = c74_nodes = c74_cum_new = 0.0
    scans, pilots, deals = {}, {}, {}
    c73_mon = 0.0
    c75_ret = 0.0
    soc2_done = False
    acq_stopped, acq_stop_m = False, None  # §11 kill criterion 9 (RED-TEAM: RT-HYP-DD4-05)
    hist_op = []  # gross profit - non-salary opex, for the full-time rule
    rows = []
    for m in range(1, MONTHS + 1):
        r5, r4 = dram_prices(m, scen, p)
        price_ratio = r5 / p["rdimm_peak_usd_gb"]
        pain = p["pain_floor"] + (1 - p["pain_floor"]) * price_ratio
        fee = fee_per_node(m, scen, p)
        cap_h = p["founder_hours_ft"] if ft else p["founder_hours_pt"]
        if (not acq_stopped and p["acq_stop_price_frac"] > 0 and price_ratio < p["acq_stop_price_frac"]
                and c74_cust < p["acq_stop_max_cust"]):
            acq_stopped, acq_stop_m = True, m
        selling = m >= p["c74_sell_start"] and not acq_stopped

        # --- C-74 base: churn, expansion, new customers from pilots two months ago ---
        churn = min(0.95, (p["c74_churn_pm"] + p["c74_glut_churn_uplift"] * max(0.0, 1 - price_ratio)) * km)
        lost = c74_cust * churn
        c74_nodes *= (1 - churn) * (1 + p["node_expansion_pm"])
        c74_cust -= lost
        new_c74 = pilots.get(m - 2, 0.0) * min(1.0, p["pilot_to_sub"] * cm)
        c74_cust += new_c74
        c74_cum_new += new_c74
        c74_nodes += new_c74 * p["nodes_per_customer"]

        # --- C-73 audits and monitoring ---
        audits = 0.0
        if m >= p["c73_start"]:
            audits = p["c73_rate_ft"] if ft else p["c73_rate_pt"]
        c73_mon = c73_mon * (1 - min(0.95, p["c73_monitor_churn"] * km)) + audits * min(1.0, p["c73_to_monitor"] * cm)

        # --- C-75 engagements and retainers ---
        c75_new = 0.0
        if p["c75_enabled"] and m >= p["c75_start"]:
            rate = p["c75_deal_rate_ft"] if ft else p["c75_deal_rate_pt"]
            decay = max(p["c75_decay_floor"], 1 - (1 - p["c75_decay_floor"]) * (m - 1) / (p["c75_decay_month"] - 1))
            sf = p["c75_glut_factor"] if (scen != "BASE" and price_ratio < 0.999) else 1.0
            c75_new = rate * decay * sf * cm
        deals[m] = c75_new
        c75_ret = c75_ret * (1 - min(0.95, p["c75_retainer_churn"] * km)) + deals.get(m - 2, 0.0) * min(1.0, p["c75_to_retainer"] * cm)

        # --- founder hours: committed work first, outreach fills what is left ---
        active_pilots = pilots.get(m - 1, 0.0) + pilots.get(m - 2, 0.0)
        committed = ((p["dev_hours_early"] if m <= 12 else p["dev_hours_late"])
                     + audits * p["c73_hours"]
                     + (deals.get(m, 0.0) + deals.get(m - 1, 0.0)) * p["c75_hours"] / 2
                     + c75_ret * p["hours_per_retainer"]
                     + c74_cust * p["hours_per_c74_customer"]
                     + active_pilots * p["hours_per_pilot_month"]
                     + scans.get(m - 1, 0.0) * p["hours_per_scan"])
        touches = 0.0
        if selling:
            target = p["touches_ft"] if ft else p["touches_pt"]
            touches = min(target, max(0.0, (cap_h - committed) / p["hours_per_touch"]))
        hours_used = committed + touches * p["hours_per_touch"]

        # --- C-74 funnel ---
        a, b = p["inbound_ramp"]
        inbound = 0.0 if m < a else p["inbound_max"] * min(1.0, (m - a + 1) / (b - a + 1))
        convs = touches * p["reply_rate"] + (inbound + audits * p["c73_to_c74_convs"] if selling else 0.0)
        scans[m] = convs * min(1.0, p["conv_to_scan"] * cm) * pain
        pilots[m] = scans.get(m - 1, 0.0) * min(1.0, p["scan_to_pilot"] * cm) if m >= p["c74_agent_ready"] else 0.0
        if m == p["c74_agent_ready"]:  # scans that waited for the agent convert now
            pilots[m] = sum(v for k, v in scans.items() if k < m) * min(1.0, p["scan_to_pilot"] * cm)

        # --- revenue ---
        rev_c73 = audits * p["c73_price"] * gm_ + c73_mon * p["c73_monitor_price"] * gm_
        rev_c74_sub = c74_nodes * fee
        rev_c74 = rev_c74_sub + pilots[m] * p["pilot_fee"] * gm_
        rev_c75_ret = c75_ret * p["c75_retainer_price"] * gm_
        rev_c75 = (deals.get(m, 0.0) + deals.get(m - 1, 0.0)) / 2 * p["c75_price"] * gm_ + rev_c75_ret
        rev = rev_c73 + rev_c74 + rev_c75
        mrr = c73_mon * p["c73_monitor_price"] * gm_ + rev_c74_sub + rev_c75_ret

        # --- COGS ---
        cogs_c73 = (audits * p["c73_cogs"] + c73_mon * p["c73_monitor_cogs"]) * um
        oncall = 0.0
        if c74_cust > 0.05:
            oncall = p["oncall_large"] if c74_cust >= p["oncall_threshold"] else p["oncall_small"]
        cogs_c74_sub = (c74_nodes * p["hosting_per_node"] + p["support_pct"] * rev_c74_sub + oncall) * um
        cogs_c74_pil = pilots[m] * p["pilot_cost"] * um
        cogs_c74 = cogs_c74_sub + cogs_c74_pil
        cogs_c75 = ((deals.get(m, 0.0) + deals.get(m - 1, 0.0)) / 2 * p["c75_cogs"]
                    + p["c75_retainer_cogs_pct"] * rev_c75_ret) * um
        cogs = cogs_c73 + cogs_c74 + cogs_c75
        gp = rev - cogs

        # --- opex ---
        opex_ns = p["tools_pm"] + (p["marketing_ft"] if ft else p["marketing_pt"]) + scans[m] * p["scan_cost"]
        if m == 1:
            opex_ns += p["legal_setup"]
        b0, b1 = p["c74_build_months"]
        if b0 <= m <= b1:
            opex_ns += p["c74_build_cost"] / (b1 - b0 + 1)
        if m >= 2:
            opex_ns += p["test_infra_pm"]
        if m >= p["c74_agent_ready"]:
            opex_ns += p["insurance_pm"]
        s0, s1 = p["c75_benchmark_months"]
        if p["c75_enabled"] and s0 <= m <= s1:
            opex_ns += p["c75_benchmark_cost"] / (s1 - s0 + 1)
        if not soc2_done and c74_cum_new >= p["soc2_trigger_customers"]:
            opex_ns += p["soc2_cost"]
            soc2_done = True
        salary = p["founder_salary_ft"] if ft else 0.0
        opex = opex_ns + salary
        net = gp - opex
        cash += net
        hist_op.append(gp - opex_ns)

        rows.append(dict(
            m=m, date=label(m), ft=ft, r5=r5, r4=r4, fee=fee, nodeval=node_value(m, scen, p), pain=pain,
            c74_cust=c74_cust, c74_nodes=c74_nodes, new_c74=new_c74, scans=scans[m], pilots=pilots[m],
            touches=touches, hours=hours_used, cap=cap_h, audits=audits, c73_mon=c73_mon,
            c75_deals=c75_new, c75_ret=c75_ret,
            rev_c73=rev_c73, rev_c74=rev_c74, rev_c75=rev_c75, rev=rev, rev_c74sub=rev_c74_sub,
            rev_c74pil=rev_c74 - rev_c74_sub, cogs_c74sub=cogs_c74_sub, cogs_c74pil=cogs_c74_pil,
            cogs_c73=cogs_c73, cogs_c74=cogs_c74, cogs_c75=cogs_c75, cogs=cogs, gp=gp,
            opex=opex, salary=salary, net=net, cash=cash, mrr=mrr, arr=12 * mrr,
        ))
        # full-time switch for next month (A-03): gross profit after non-salary opex covers the salary
        if not ft and len(hist_op) >= 3 and sum(hist_op[-3:]) / 3 >= p["founder_salary_ft"]:
            ft = True
            ft_month = m + 1
    summ = summarize(rows, ft_month)
    summ["acq_stop_m"] = acq_stop_m
    return dict(rows=rows, p=p, scen=scen, ft_month=ft_month, summary=summ)


def summarize(rows, ft_month):
    rev = sum(r["rev"] for r in rows)
    cogs = sum(r["cogs"] for r in rows)
    line = {}
    for k in ("c73", "c74", "c75", "c74sub", "c74pil"):
        rv = sum(r["rev_" + k] for r in rows)
        cg = sum(r["cogs_" + k] for r in rows)
        line[k] = (rv, cg, (rv - cg) / rv if rv > 0 else None)
    nets = [r["net"] for r in rows]
    be = None
    for i in range(2, len(rows)):
        if sum(nets[i - 2:i + 1]) >= 0 and rows[i]["rev"] > 0:
            be = rows[i]["m"]
            break
    sustained = None
    for i in range(2, len(rows)):
        if all(sum(nets[j - 2:j + 1]) >= 0 for j in range(i, len(rows))):
            sustained = rows[i]["m"]
            break
    low = min(rows, key=lambda r: r["cash"])
    arr = {m: rows[m - 1]["arr"] for m in (12, 18, 24, 36)}
    cust = {m: rows[m - 1]["c74_cust"] for m in (12, 18, 24, 36)}
    first_rev = next((r["m"] for r in rows if r["rev"] > 1), None)
    first_rec = next((r["m"] for r in rows if r["mrr"] > 1), None)
    over = [r["m"] for r in rows if r["hours"] > r["cap"] * 1.001]
    return dict(rev=rev, cogs=cogs, gm=(rev - cogs) / rev if rev else None, line=line, be=be, be_sustained=sustained,
                cash_low=low["cash"], cash_low_m=low["m"], cash_end=rows[-1]["cash"], arr=arr, cust=cust,
                ft_month=ft_month, first_rev=first_rev, first_rec=first_rec, over_capacity=over)


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
    print("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


def usd(x, d=0):
    if x is None:
        return "n/a"
    s = "-" if x < 0 else ""
    return s + "$" + format(abs(x), ",.%df" % d)


def k(x):
    return "n/a" if x is None else ("%s$%.1fk" % ("-" if x < 0 else "", abs(x) / 1000))


def pct(x):
    return "n/a" if x is None else "%.0f%%" % (100 * x)


def mo(m):
    return "never" if m is None else "M%d (%s)" % (m, label(m))


# ----------------------------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------------------------
def report():
    p = base_params()
    print("DD4 Memory Efficiency (C-73 + C-74 + C-75) -- unit-economics model, as of %s" % AS_OF)
    print("DDR5 reference deck: %s" % REF_SOURCE)
    print("Month 1 = 2026-11; month 36 = %s. Expected-value model (fractional customers)." % label(MONTHS))
    print("RED-TEAM REVISIONS (Phase 5) applied: %s. Every table below uses the revised inputs unless it says"
          " 'Phase 4'." % ("YES" if APPLY_RED_TEAM else "NO (Phase 4 reproduction)"))

    section("0. RED-TEAM REVISIONS (Phase 5): changed inputs and their effect on the headline")
    table(["Input", "Phase 4", "Phase 5", "Objection ids"],
          [[kk, v[0], v[1], v[2][:70]] for kk, v in RED_TEAM_REVISIONS.items()], ["l", "r", "r", "l"])
    print("\nBases for each change are in the RED_TEAM_REVISIONS block of models/memory-efficiency.py.")
    rows = []
    for scen in SCENARIOS:
        for tag, rt in (("Phase 4", False), ("Phase 5", True)):
            s0 = simulate(scen, red_team=rt)["summary"]
            rows.append([scen, tag, "%.2f" % simulate(scen, red_team=rt)["rows"][0]["fee"], k(s0["arr"][18]),
                         k(s0["arr"][36]), "%.1f" % s0["cust"][36], "%s @M%d" % (k(s0["cash_low"]), s0["cash_low_m"]),
                         k(s0["cash_end"]), mo(s0["be"]), mo(s0["ft_month"])])
    table(["Scenario", "Inputs", "Fee M1 $/node", "ARR M18", "ARR M36", "C74 cust M36", "Cash low", "Cash M36",
           "Breakeven", "Founder FT"], rows)
    print("\nOne change at a time (BASE, Phase 4 inputs plus only that red-team change):")
    rows = []
    for kk, v in RED_TEAM_REVISIONS.items():
        s1 = simulate("BASE", {kk: v[1]}, red_team=False)["summary"]
        rows.append([kk, "%s -> %s" % (v[0], v[1]), k(s1["arr"][36]), k(s1["cash_low"]), k(s1["cash_end"]),
                     pct(s1["line"]["c74sub"][2])])
    table(["Changed input", "Old -> new", "ARR M36", "Cash low", "Cash M36", "C-74 sub GM"], rows)

    section("1. Key inputs (full list with sources in the INPUTS block of models/memory-efficiency.py)")
    keys = ["founder_capital", "rdimm_peak_usd_gb", "rdimm_glut_usd_gb", "rdimm_severe_usd_gb", "ddr4_used_usd_gb",
            "node_gb", "reclaim_frac", "ddr5_share", "savings_share", "list_price_node_month", "nodes_per_customer",
            "touches_pt", "reply_rate", "conv_to_scan", "scan_to_pilot", "pilot_to_sub", "c74_churn_pm",
            "c73_price", "c73_rate_pt", "c73_to_monitor", "c75_enabled", "c75_price", "c75_deal_rate_pt",
            "c75_retainer_price", "founder_salary_ft", "value_realization", "oncall_small", "oncall_large",
            "insurance_pm", "soc2_trigger_customers", "acq_stop_price_frac"]
    table(["Input", "Value", "Source (truncated; RED-TEAM = revised in Phase 5)"],
          [[kk, ("%.4g" % p[kk]) if isinstance(p[kk], float) else p[kk],
            ("RED-TEAM (was %s): %s" % (RED_TEAM_REVISIONS[kk][0], RED_TEAM_REVISIONS[kk][2]) if
             (APPLY_RED_TEAM and kk in RED_TEAM_REVISIONS) else INPUTS[kk][1])[:92]] for kk in keys], ["l", "r", "l"])

    section("2. Glut effect: what one GB and one node of reclaimed DRAM is worth (C-74 value driver)")
    rows = []
    for scen in SCENARIOS:
        for m in (1, 15, 18, 24, 36):
            r5, r4 = dram_prices(m, scen, p)
            nv = node_value(m, scen, p)
            fee = min(p["list_price_node_month"], nv / p["contract_months"] * p["savings_share"])
            rows.append([scen, label(m), "%.2f" % r5, "%.2f" % r4, usd(nv), "%.2f" % fee,
                         usd(fee * p["nodes_per_customer"]), "%.1fx" % (nv / (fee * p["contract_months"]))])
    table(["Scenario", "Month", "DDR5 RDIMM $/GB", "Used DDR4 $/GB", "Realized $/node", "Fee $/node/mo (no lag)",
           "MRR per 80-node cust", "Customer ROI (3 yr)"], rows)
    gb_saved = p["node_gb"] * p["reclaim_frac"]
    print("\nPer node: %.0f GB installed x %.0f%% reclaimed = %.1f GB freed; DDR5 share of node-GB %.0f%%; value"
          " realization %.0f%% (rental-equivalent of 36 months of freed capacity, RT-VC-DD4-02)."
          % (p["node_gb"], 100 * p["reclaim_frac"], gb_saved, 100 * p["ddr5_share"], 100 * p["value_realization"]))
    print("At list $%.0f/node/mo the fee would equal %.0f%% of peak deferred value over 36 months; the model charges the"
          % (p["list_price_node_month"], 100 * p["list_price_node_month"] * 36 / node_value(1, "BASE", p)))
    print("lower of list and a %.0f%% savings share (ProsperOps/Zesty-style take rate)." % (100 * p["savings_share"]))
    print("A pure DDR4 fleet node is worth only %s at the peak (%.1f GB x $%.2f x %.2f): DDR4 fleets cannot pay."
          % (usd(gb_saved * p["ddr4_used_usd_gb"] * p["value_realization"]), gb_saved, p["ddr4_used_usd_gb"],
             p["value_realization"]))
    pure5 = gb_saved * p["rdimm_peak_usd_gb"] * p["value_realization"]
    print("A pure DDR5 node is worth %s at the peak -> fee $%.2f/node/mo at a %.0f%% share (the best case for the"
          " kill test's $5 bar)." % (usd(pure5), pure5 / p["contract_months"] * p["savings_share"], 100 * p["savings_share"]))

    section("3. Unit economics per product line (BASE, steady state)")
    res = {s: simulate(s) for s in SCENARIOS}
    rb = res["BASE"]["rows"]
    fee12 = rb[11]["fee"]
    arpa = fee12 * p["nodes_per_customer"]
    var_cogs = p["nodes_per_customer"] * p["hosting_per_node"] + p["support_pct"] * arpa
    c24 = rb[23]["c74_cust"]  # on-call retainer actually paid at month 24, spread over that month's customers
    oncall_alloc = (p["oncall_large"] if c24 >= p["oncall_threshold"] else p["oncall_small"]) / max(1.0, c24)
    funnel = p["reply_rate"] * p["conv_to_scan"] * p["scan_to_pilot"] * p["pilot_to_sub"]
    touches_per_cust = 1 / funnel
    scans_per_cust = 1 / (p["scan_to_pilot"] * p["pilot_to_sub"])
    pilots_per_cust = 1 / p["pilot_to_sub"]
    cac_cash = scans_per_cust * p["scan_cost"] + pilots_per_cust * (p["pilot_cost"] - p["pilot_fee"])
    cac_hours = touches_per_cust * p["hours_per_touch"] + scans_per_cust * p["hours_per_scan"] + pilots_per_cust * 2 * p["hours_per_pilot_month"]
    gm74_var = (arpa - var_cogs) / arpa
    gm74_loaded = (arpa - var_cogs - oncall_alloc) / arpa
    life = 1 / p["c74_churn_pm"]
    rows = [
        ["C-74 reclaim subscription (80 nodes)", usd(arpa) + "/mo", usd(var_cogs) + "/mo var + " + usd(oncall_alloc) + " on-call",
         pct(gm74_var) + " var / " + pct(gm74_loaded) + " loaded", usd(cac_cash) + " + %.0f h" % cac_hours,
         ("%.1f mo" % ((cac_cash + cac_hours * p["founder_labor_rate"]) / (arpa * gm74_loaded))) if gm74_loaded > 0
         else "never (loaded GM<0)",
         usd(arpa * gm74_loaded * life)],
        ["C-73 cloud audit (one-time)", usd(p["c73_price"]), usd(p["c73_cogs"]) + " + %.0f h" % p["c73_hours"],
         pct((p["c73_price"] - p["c73_cogs"]) / p["c73_price"]) + " cash / " +
         pct((p["c73_price"] - p["c73_cogs"] - p["c73_hours"] * p["founder_labor_rate"]) / p["c73_price"]) + " labor-loaded",
         "network (0 cash)", "n/a", usd(p["c73_price"] - p["c73_cogs"])],
        ["C-73 monitoring subscription", usd(p["c73_monitor_price"]) + "/mo", usd(p["c73_monitor_cogs"]) + "/mo",
         pct(1 - p["c73_monitor_cogs"] / p["c73_monitor_price"]), "%.0f audits per sub" % (1 / p["c73_to_monitor"]), "n/a",
         usd((p["c73_monitor_price"] - p["c73_monitor_cogs"]) / p["c73_monitor_churn"])],
        ["C-75 KV-cache integration engagement", usd(p["c75_price"]), usd(p["c75_cogs"]) + " + %.0f h" % p["c75_hours"],
         pct((p["c75_price"] - p["c75_cogs"]) / p["c75_price"]) + " cash / " +
         pct((p["c75_price"] - p["c75_cogs"] - p["c75_hours"] * p["founder_labor_rate"]) / p["c75_price"]) + " labor-loaded",
         usd(p["c75_benchmark_cost"]) + " benchmark (once)", "n/a", usd(p["c75_price"] - p["c75_cogs"])],
        ["C-75 retainer", usd(p["c75_retainer_price"]) + "/mo", pct(p["c75_retainer_cogs_pct"]) + " of rev",
         pct(1 - p["c75_retainer_cogs_pct"]), "from engagement", "n/a",
         usd(p["c75_retainer_price"] * (1 - p["c75_retainer_cogs_pct"]) / p["c75_retainer_churn"])],
    ]
    table(["Line", "Price", "COGS", "Gross margin", "CAC (cash + founder h)", "Payback", "LTV (GP)"], rows,
          ["l", "r", "l", "l", "l", "r", "r"])
    print("\nC-74 funnel: %.0f outbound touches -> 1 customer (reply %.0f%% x scan %.0f%% x pilot %.0f%% x close %.0f%% = %.2f%%),"
          % (touches_per_cust, 100 * p["reply_rate"], 100 * p["conv_to_scan"], 100 * p["scan_to_pilot"],
             100 * p["pilot_to_sub"], 100 * funnel))
    print("before the DRAM-pain multiplier (%.1f at peak; %.2f at the glut line; %.2f at the severe line)."
          % (1.0, p["pain_floor"] + (1 - p["pain_floor"]) * p["rdimm_glut_usd_gb"] / p["rdimm_peak_usd_gb"],
             p["pain_floor"] + (1 - p["pain_floor"]) * p["rdimm_severe_usd_gb"] / p["rdimm_peak_usd_gb"]))
    print("Part-time capacity = %.0f touches/mo + inbound ramp to %.0f conversations/mo (months %d-%d) -> ~%.2f new C-74 customers/mo at peak."
          % (p["touches_pt"], p["inbound_max"], p["inbound_ramp"][0], p["inbound_ramp"][1],
             (p["touches_pt"] * p["reply_rate"] + p["inbound_max"]) * p["conv_to_scan"] * p["scan_to_pilot"] * p["pilot_to_sub"]))
    print("C-74 fee in BASE month 12: $%.2f/node/mo (savings-share capped; list $%.0f)." % (fee12, p["list_price_node_month"]))

    for scen in SCENARIOS:
        section("4%s. Monthly P&L and cash, %s -- %s" % ("abc"[SCENARIOS.index(scen)], scen, SCEN_DESC[scen]))
        rws = []
        for r in res[scen]["rows"]:
            rws.append([r["m"], r["date"], "FT" if r["ft"] else "PT", "%.1f" % r["r5"], "%.2f" % r["fee"],
                        "%.2f" % r["c74_cust"], "%.0f" % r["c74_nodes"], "%.2f" % r["c75_ret"],
                        "%.0f" % r["rev_c73"], "%.0f" % r["rev_c74"], "%.0f" % r["rev_c75"], "%.0f" % r["rev"],
                        "%.0f" % r["cogs"], "%.0f" % r["gp"], "%.0f" % r["opex"], "%.0f" % r["net"],
                        "%.0f" % r["cash"], "%.0f" % r["arr"], "%.0f%%" % (100 * r["hours"] / r["cap"])])
        table(["M", "Date", "PT/FT", "DDR5$/GB", "Fee$/node", "C74cust", "Nodes", "C75ret", "RevC73", "RevC74",
               "RevC75", "Revenue", "COGS", "GrossProf", "Opex", "Net", "Cash", "ARR", "FounderHrs"], rws)

    section("5. Scenario summary (36 months, from $40k founder capital)")
    rows = []
    for scen in SCENARIOS:
        s = res[scen]["summary"]
        rows.append([scen, k(s["rev"]), pct(s["gm"]), pct(s["line"]["c73"][2]), pct(s["line"]["c74sub"][2]),
                     pct(s["line"]["c74pil"][2]), pct(s["line"]["c75"][2]), mo(s["first_rev"]), mo(s["be"]),
                     mo(s["be_sustained"]), "%s @M%d" % (k(s["cash_low"]), s["cash_low_m"]), k(s["cash_end"]),
                     mo(s["ft_month"])])
    table(["Scenario", "Rev 36mo", "GM", "GM C73", "GM C74 sub", "GM C74 pilots", "GM C75", "First revenue",
           "Breakeven (3-mo net>=0)",
           "Sustained BE", "Cash low", "Cash M36", "Founder full-time"], rows)
    print()
    rows = []
    for scen in SCENARIOS:
        s = res[scen]["summary"]
        rows.append([scen] + [k(s["arr"][m]) for m in (12, 18, 24, 36)] + ["%.1f" % s["cust"][m] for m in (12, 18, 24, 36)])
    table(["Scenario", "ARR M12", "ARR M18", "ARR M24", "ARR M36", "C74 cust M12", "M18", "M24", "M36"], rows)
    print("\nARR = 12 x recurring MRR (C-74 subscriptions + C-73 monitoring + C-75 retainers); audits, pilots and")
    print("engagements are one-time and excluded. Breakeven = first month the trailing-3-month net cash flow is >= 0")
    print("(founder unpaid while part-time). Sustained BE = that holds through month 36.")
    for scen in SCENARIOS:
        oc = res[scen]["summary"]["over_capacity"]
        if oc:
            print("WARNING %s: founder hours exceed capacity in months %s" % (scen, oc))

    section("6. Sensitivity (+/-30%) -- ARR M18 / ARR M36 / breakeven / cash low")
    tests = [("Base case", {}),
             ("Price -30%", {"price_mult": 0.7}), ("Price +30%", {"price_mult": 1.3}),
             ("Conversion/close -30%", {"conv_mult": 0.7}), ("Conversion/close +30%", {"conv_mult": 1.3}),
             ("Churn -30%", {"churn_mult": 0.7}), ("Churn +30%", {"churn_mult": 1.3}),
             ("COGS -30%", {"cogs_mult": 0.7}), ("COGS +30%", {"cogs_mult": 1.3}),
             ("Reclaim 5% (Google zswap-like)", {"reclaim_frac": 0.05}),
             ("Reclaim 20% (low end of Meta TMO)", {"reclaim_frac": 0.20}),
             ("DDR5 share 100% of node-GB", {"ddr5_share": 1.0}),
             ("Node 1 TB (virtualization hosts)", {"node_gb": 1024.0}),
             ("Drop C-75 line", {"c75_enabled": 0}),
             ("RT: C-75 back on (gate passes)", {"c75_enabled": 1}),
             ("RT: C-73 zero (C-74 standalone)", {"c73_rate_pt": 0.0, "c73_rate_ft": 0.0}),
             ("RT: reclaim 10% incremental (kill-test PASS bar)", {"reclaim_frac": 0.10}),
             ("RT: kill-test best case (reclaim 10%, DDR5 60%)", {"reclaim_frac": 0.10, "ddr5_share": 0.60}),
             ("RT: savings share back to 30%", {"savings_share": 0.30}),
             ("RT: on-call/E&O back to Phase 4 ($750/$2k/$200)",
              {"oncall_small": 750.0, "oncall_large": 2_000.0, "insurance_pm": 200.0}),
             ("RT: conversion back to Phase 4 (0.40/0.60)", {"scan_to_pilot": 0.40, "pilot_to_sub": 0.60}),
             ("Everything +30% (price, conv, churn-30%, COGS-30%)",
              {"price_mult": 1.3, "conv_mult": 1.3, "churn_mult": 0.7, "cogs_mult": 0.7})]
    for scen in ("BASE", "GLUT", "SEVERE"):
        print("\n%s:" % scen)
        rows = []
        for name, ov in tests:
            s = simulate(scen, ov)["summary"]
            rows.append([name, k(s["arr"][18]), k(s["arr"][36]), mo(s["be"]), "%s @M%d" % (k(s["cash_low"]), s["cash_low_m"]),
                         k(s["cash_end"]), mo(s["ft_month"])])
        table(["Case", "ARR M18", "ARR M36", "Breakeven", "Cash low", "Cash M36", "Founder FT"], rows)

    section("7. What must be true")
    s = res["BASE"]["summary"]
    r18 = rb[17]
    fee18 = r18["fee"]
    opex_ft = p["tools_pm"] + p["marketing_ft"] + p["test_infra_pm"] + p["insurance_pm"]
    gm_c74 = gm74_var
    mrr_need = (p["founder_salary_ft"] + opex_ft + p["oncall_large"]) / gm_c74
    nodes_need = mrr_need / fee18
    cust_need = nodes_need / p["nodes_per_customer"]
    print("To pay the founder full-time ($%.0fk/mo loaded) from C-74 alone by month 18 (BASE fee $%.2f/node/mo):"
          % (p["founder_salary_ft"] / 1000, fee18))
    print("  needed MRR ~ %s -> %s nodes -> %.0f customers at %.0f nodes each." % (usd(mrr_need), format(int(nodes_need), ","),
                                                                              cust_need, p["nodes_per_customer"]))
    print("  model delivers by month 18: %.1f customers, %.0f nodes, total ARR %s (shortfall ~%.0fx)."
          % (r18["c74_cust"], r18["c74_nodes"], k(r18["arr"]), cust_need / max(0.01, r18["c74_cust"])))
    need_conv_rate = cust_need / 11.0  # selling months 8..18
    print("  i.e. ~%.1f new customers/month from month 8 vs ~%.2f/month the part-time funnel produces."
          % (need_conv_rate, s["cust"][18] / 11.0))
    for scen in ("GLUT", "SEVERE"):
        rr = res[scen]["rows"][35]
        need36 = (p["founder_salary_ft"] + opex_ft + p["oncall_large"]) / gm_c74 / max(0.01, rr["fee"])
        print("  %s month-36 fee $%.2f/node/mo -> %s nodes (~%.0f customers) to carry one salary."
              % (scen, rr["fee"], format(int(need36), ","), need36 / p["nodes_per_customer"]))
    # RT-VC-DD4-01: what a channel partner would have to bring to change the ceiling
    print("\nChannel test (RT-VC-DD4-01): pure-DDR5 VM-host nodes a reseller/MSP partner must bring to carry one salary"
          "\n  plus fixed ops (on-call $%.0f + E&O $%.0f + tools/marketing), at a %.0f%% channel revenue share:"
          % (p["oncall_large"], p["insurance_pm"], 100 * 0.25))
    for rf in (p["reclaim_frac"], 0.10):
        pv = dict(p, ddr5_share=1.0, reclaim_frac=rf)
        f1 = min(pv["list_price_node_month"], node_value(1, "BASE", pv) / pv["contract_months"] * pv["savings_share"])
        net_node = f1 * (1 - 0.25) - pv["hosting_per_node"] - pv["support_pct"] * f1
        need_n = (p["founder_salary_ft"] + opex_ft + p["oncall_large"]) / max(0.01, net_node)
        print("  reclaim %2.0f%%: fee $%.2f/node/mo at the peak -> %s nodes (BASE peak price; ~%.0f%% more at the M36"
              " BASE price)" % (100 * rf, f1, format(int(round(need_n, -2)), ","), 100 * (1 / (1 - p["base_turn_pct"]) - 1)))
    print("Also true or fatal: (a) >=10% of installed RAM reclaimable with no p99/OOM regression on a stranger's fleet;"
          "\n  (b) target fleets are mostly DDR5 and still buying in 2027; (c) one swap incident does not end the company;"
          "\n  (d) the buyer pays for tuning free upstream features (zswap, PSI, DAMON) instead of doing it in-house.")

    section("8. Verdict lines")
    for scen in SCENARIOS:
        s = res[scen]["summary"]
        neg = next((r["m"] for r in res[scen]["rows"] if r["cash"] < 0), None)
        print("%-6s GM %s | breakeven %s | cash low %s | ARR M18 %s | ARR M36 %s | founder full-time %s | cash < $0 from %s"
              " | C-74 acquisition stopped %s"
              % (scen, pct(s["gm"]), mo(s["be"]), k(s["cash_low"]), k(s["arr"][18]), k(s["arr"][36]), mo(s["ft_month"]),
                 mo(neg), mo(s.get("acq_stop_m"))))
    return res


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            st.write(s)

    def flush(self):
        for st in self.streams:
            st.flush()


def main():
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = Tee(old, buf)
    try:
        report()
    finally:
        sys.stdout = old
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(
        "# DD4 memory-efficiency model output\n\n"
        "Generated by `python3 models/memory-efficiency.py` (agent `p4-memory-efficiency`, as of %s; "
        "RED-TEAM REVISIONS (Phase 5) by `p5r-memory-efficiency` applied). "
        "Do not edit by hand; re-run the model.\n\n```\n%s```\n" % (AS_OF, buf.getvalue()))
    print("\n[wrote %s]" % OUT_MD.relative_to(RV))
    return 0


if __name__ == "__main__":
    sys.exit(main())
