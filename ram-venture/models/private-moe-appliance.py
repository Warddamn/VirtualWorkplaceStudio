#!/usr/bin/env python3
"""DD6 -- Private MoE Inference Appliance (DRAM instead of HBM): unit-economics model.

Agent key: p4-private-moe-appliance.  As of 2026-11-01.  Pure Python 3 stdlib.
Run:  cd ram-venture && python3 models/private-moe-appliance.py
      (prints every table, writes research/phase4/private-moe-appliance_model_output.md, exits 0)

The concept (C-48): a U.S.-integrated on-prem inference box that keeps the expert weights of an
open-weight mixture-of-experts model (Kimi-K2.5 ~1T, DeepSeek V3/V4, GLM-5.x, MiniMax-M2/M3, and the
U.S.-origin Inkling 975B / Nemotron 3 Ultra 550B) resident in DDR5 on a single-socket EPYC 9005 (or
Xeon 6) server, with one GPU doing attention, shared experts and long-prompt prefill
(KTransformers / SGLang / llama.cpp hybrid inference). Sold to regulated small/mid organizations as:

  Line 1  Hardware appliance, two SKUs, build-to-order with a deposit:
            L "Team-1T": 1S EPYC 9005 48C, 768 GB DDR5 (12 x 64GB), 1x RTX PRO 6000 96GB.
                         Runs 1T-class MoE at native INT4 (Kimi-K2.5 needs >=600 GB RAM + 48 GB VRAM).
            S "Team-S":  1S EPYC 9005 32C, 384 GB DDR5 (12 x 32GB), 1x RTX 5090 32GB.
                         Runs 200-300B-class MoE (DeepSeek-V4-Flash needs >=200 GB + one RTX 5090).
  Line 2  Annual support + model-update subscription per box (the recurring line), billed yearly
          in advance, mandatory in year 1.
  Line 3  One-time setup/integration fee (RAG connectors, SSO, SSP/boundary documentation).

Each scenario simulates 36 months, Nov-2026 (m1) to Oct-2029 (m36), from the founder's $40k
(ASSUMPTIONS A-03). The founder starts part-time at ~65 h/month and goes full-time only when the
trailing 3-month operating profit covers a $10k/month loaded salary and post-tax cash >= $30k.
Founder hours are a hard budget: builds and support that do not fit go to a contractor at a cash
rate; sales conversations get what is left. If cash would fall below a $5k floor, the model draws
external capital in $25k tranches and reports it explicitly.

Scenarios (2028-Q1 = m15 = Jan-2028):
  BASE    DDR5 RDIMM at the Q4-2026 contract deck to Dec-2027, then -30% linear across 2028.
          GPU street prices hold to Dec-2027, then -30% linear across 2028.
  GLUT    DDR5 -60% from 2028-Q1 (A-05; ddr5_reference glut deck). GPUs fall to 55% (GDDR7 normalizes).
  SEVERE  DDR5 component at $2.04/GB from 2028-Q1 (ddr5_reference severe deck). GPUs fall to 50%.
Hardware is priced cost-plus at order time, so a glut lowers the box price (and GP dollars per box)
but raises unit demand a little (elasticity input). The subscription is priced per box, not as a
share of hardware, so recurring revenue does not deflate with DRAM.

The model works in expected values: customers and boxes can be fractional. Read it as a central
case, not a forecast. Every INPUTS entry carries a source URL or "ESTIMATE: basis". "(snippet)"
means the number was seen only in a search-result snippet; full log:
research/sources/p4-private-moe-appliance.jsonl. Assumptions: research/assumptions/p4-private-moe-appliance.md.

PHASE 5 (agent p5r-private-moe-appliance, 2026-11-01): the "RED-TEAM REVISIONS (Phase 5)" block below the
INPUTS changes inputs and adds mechanics, each tagged old -> new with its objection id from
research/phase5/rt2_*.json. run_with(P_PHASE4, scen) reproduces the Phase 4 numbers exactly. New mechanics:
a bandwidth-based capacity model (distinct experts per batch step / effective DRAM bandwidth) with a VRAM/KV
check; a subscription price capped by named users; a demand response to price RISES versus the Phase-4 price
card; a VAR-paper fee on direct deals; quote-to-purchase cost drift; a spare-parts pool held as inventory;
and new honesty metrics (renewal-tested ARR, customer cash held, founder economic profit).
Responses: research/phase5/responses_private-moe-appliance.json.
"""
import io
import math
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

AS_OF = "2026-11-01"
HERE = Path(__file__).resolve().parent
RV = HERE.parent
OUT_MD = RV / "research" / "phase4" / "private-moe-appliance_model_output.md"

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
    REF_SOURCE = "canonical fallback numbers from the DD6 task spec (import failed: %r)" % (exc,)

MODULE_TO_COMPONENT = REF["contract_rdimm64_usd_per_user_gb_q4_2026"] / REF["contract_component_usd_per_gb_q4_2026"]
RDIMM_NOW = REF["contract_rdimm64_usd_per_user_gb_q4_2026"]
RDIMM_GLUT = REF["glut_rdimm64_usd_per_user_gb"]
RDIMM_SEVERE = REF["severe_glut_component_usd_per_gb"] * MODULE_TO_COMPONENT

# ----------------------------------------------------------------------------------------------
# INPUTS: name -> (value, source).  Source = URL or "ESTIMATE: basis".
# ----------------------------------------------------------------------------------------------
_KT_R1 = "https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/DeepseekR1_V3_tutorial.md"
_KT_BAL = "https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/balance-serve.md"
_KT_MM = "https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/MiniMax-M2.1-Tutorial.md"
_KT_KN = "https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/kt-kernel/Kimi-K2-Thinking-Native.md"
_KT_K25 = "https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/Kimi-K2.5.md"
_KT_V4F = "https://github.com/kvcache-ai/ktransformers/blob/main/doc/en/DeepSeek-V4-Flash.md"
_PRO6K = "https://tech-insider.org/nvidia-rtx-pro-6000-blackwell-price-2026/ (snippet: $16,000 NVIDIA US store, Sep-2026); https://gpuprix.com/us/gpus/rtx-pro-6000-blackwell (snippet: US low $17,987, 2026-10-22)"
_5090 = "https://tech-insider.org/rtx-5090-shortage-price-surge-2026/ (snippet: Micro Center $4,299-5,300; online $8.5-10k, Oct-2026); https://www.guru3d.com/story/geforce-rtx-5090-street-prices-in-eu-now-exceed/ (EUR >5,000)"
_SMCI = "https://www.sec.gov/Archives/edgar/data/0001375365/000137536526000022/smci-20260630.htm (snippet: FY26 GAAP GM 10.8%)"
_C48 = "research/phase2/concepts_master.json C-48 card (22% hardware GM in the card's own BOM model)"
_LEMONY = "https://techcrunch.com/2025/06/11/uptime-industries-wants-to-boost-localized-ai-usage-with-an-ai-in-a-box-called-lemony-ai (snippet: $499/month for up to 5 users)"
_MSPAI = "https://www.firstfocus.com.au/insights/mid-sized-business-budget-for-ai/ (snippet: AI add-on $25-75/user/month; MSP-led AI $100-300/user/month)"
_IBL = "https://ibl.ai/blog/private-ai-pricing.md (snippet: managed private AI $12-20/user/month at 100 users)"
_RT = "05_REDTEAM.md RT-VC-DD1-07 (30% tax provision with loss carry-forward)"

INPUTS = {
    # --- Founder and company (ASSUMPTIONS.md A-03) ---
    "founder_capital": (40_000.0, "ASSUMPTIONS.md A-03: $40k deployable"),
    "founder_hours_pt": (65.0, "ASSUMPTIONS.md A-03: ~15 h/week = ~65 h/month part-time"),
    "founder_hours_ft": (170.0, "ESTIMATE: full-time month of ~40 h/week"),
    "founder_salary_ft": (10_000.0, "ASSUMPTIONS.md A-03: ~$120k/yr loaded once full-time"),
    "ft_trigger_cash": (30_000.0, "ESTIMATE: three months of salary as buffer before quitting the day job"),
    "tax_rate": (0.30, _RT),
    "cash_floor": (5_000.0, "ESTIMATE: minimum operating cash before external capital is drawn"),
    "ext_tranche": (25_000.0, "ESTIMATE: angel note / SBA Express line tranche size"),

    # --- DRAM (ddr5_reference, live import) ---
    "dram_now_per_user_gb": (RDIMM_NOW, "models/dram_cost_stack.py ddr5_reference(): 64GB RDIMM Q4-2026 contract per user-GB"),
    "dram_glut_per_user_gb": (RDIMM_GLUT, "models/dram_cost_stack.py ddr5_reference(): glut (-60%, A-05) per RDIMM user-GB"),
    "dram_severe_per_user_gb": (RDIMM_SEVERE, "models/dram_cost_stack.py ddr5_reference(): severe component $2.04/GB x RDIMM/component ratio"),
    "dram_small_buyer_premium": (1.15, "ESTIMATE: a small integrator pays between contract ($25.8/GB) and street (~$32/GB, ServNet DDR5 tracker Aug-2026 via C-48 card, https://www.servnetuk.com/research/ddr5-server-memory-price-tracker-2026)"),
    "base_turn_depth": (0.30, "ESTIMATE: BASE drifts -30% across 2028 (same BASE shape as DD4, 05_REDTEAM.md RT-HYP-DD4 response)"),

    # --- SKU L 'Team-1T' bill of materials ---
    "L_dram_gb": (768.0, "ESTIMATE: 12 channels x 64GB RDIMM (1 DPC); Kimi-K2.5 needs >=600 GB RAM, " + _KT_K25),
    "L_cpu": (5_500.0, "ESTIMATE: EPYC 9005 48C (9455-class) ~$5.4k 1k-unit list recalled from training [UNVERIFIED]; cross-check Xeon 6747P 48C MSRP $6,497 / Newegg $8,731 (snippet, https://www.newegg.com/p/N82E16819118613)"),
    "L_gpu": (16_000.0, _PRO6K),
    "L_platform": (4_500.0, "ESTIMATE: SP5 board ~$1.0k, 4U/tower chassis + 2 kW PSU ~$1.4k, 2x4TB enterprise NVMe ~$1.6k at ~3x 2026 NAND (01_LANDSCAPE s0), cooling/cables ~$0.5k"),
    # --- SKU S 'Team-S' bill of materials ---
    "S_dram_gb": (384.0, "ESTIMATE: 12 x 32GB RDIMM; DeepSeek-V4-Flash needs >=200 GB RAM, " + _KT_V4F),
    "S_cpu": (3_700.0, "ESTIMATE: EPYC 9355 32C ~$3.7k list recalled from training [UNVERIFIED]; the 9355 is the CPU in KTransformers' own benchmark table, " + _KT_MM),
    "S_gpu": (5_000.0, _5090),
    "S_platform": (3_800.0, "ESTIMATE: as L with a smaller PSU and 2x2TB NVMe"),
    "mix_L": (0.50, "ESTIMATE: half the orders want 1T-class models (or U.S.-origin Inkling 975B), half the 200-300B tier"),
    "ship_per_box": (400.0, "ESTIMATE: freight + insurance for a ~35 kg server, East Coast regional"),

    # --- GPU price paths (the GDDR7 shortage doubled RTX PRO 6000 street prices in 2026) ---
    "gpu_base_turn": (0.30, "ESTIMATE: BASE GPU street -30% across 2028 toward the $8.6k launch MSRP (tech-insider snippet)"),
    "gpu_glut_factor": (0.55, "ESTIMATE: GLUT GPU at 55% of Oct-2026 street from 2028-Q1 = ~launch MSRP ($8,565 RTX PRO 6000, 2025-03)"),
    "gpu_severe_factor": (0.50, "ESTIMATE: SEVERE GPU at 50% of Oct-2026 street from 2028-Q1"),

    # --- Pricing ---
    "hw_gm": (0.22, _C48 + "; scale integrator floor: " + _SMCI + ", FQ4-26 17.5%"),
    "setup_fee": (4_000.0, "ESTIMATE: ~24 h of RAG/SSO/SSP integration at ~$165/h; below the $5-25k per-client private-AI install range in https://betonai.net/how-to-build-a-5k-20k-month-private-ai-installation-business-in-2026-the-privacy-first-gold-rush-complete-setup-pricing-and-client-acquisition-guide/ (snippet, weak)"),
    "sub_L_month": (1_250.0, "ESTIMATE: ~25 named users x $50/user/month; anchors " + _LEMONY + "; " + _MSPAI + "; " + _IBL),
    "sub_S_month": (650.0, "ESTIMATE: Lemony $499/month for 5 users (TechCrunch snippet) plus server-class support; ~40 users x $16"),
    "sub_churn_annual": (0.20, "ESTIMATE: 1 in 5 boxes drop support at each anniversary and self-maintain the open-source stack (DD4 red team: buyers cancel once the purchase decision has passed)"),
    "partner_hw_commission": (0.10, "ESTIMATE: MSP/RPO reseller margin on hardware"),
    "partner_sub_commission": (0.15, "ESTIMATE: MSP/RPO share of subscription billings"),
    "glut_elasticity": (0.30, "ESTIMATE: units rise 0.3% per 1% fall in box price; Macs, DGX and GPU servers get cheaper in a glut too, so net elasticity is small"),

    # --- Cash terms ---
    "deposit_pct": (0.50, "C-48 card: build-to-order with 50% deposits; balance at delivery (order month + 1)"),

    # --- Costs of goods and support ---
    "warranty_reserve_pct": (0.02, "ESTIMATE: RMA labor/shipping/loaners beyond the OEM 3-year parts warranty, 2% of hardware revenue"),
    "parts_reserve_pct_yr": (0.03, "ESTIMATE: advance-replacement / spares reserve, 3% of box hardware cost per year while under subscription"),
    "tooling_per_box_month": (25.0, "ESTIMATE: monitoring, update repository, ticketing per box"),
    "support_h_per_box_month": (2.0, "ESTIMATE: patching, monitoring triage, quarterly model refresh per box (business-hours SLA; no 24/7 on-call, see DD4 red team)"),
    "contractor_rate": (85.0, "ESTIMATE: Linux/GPU contract technician, East Coast"),
    "shadow_rate": (85.0, "ESTIMATE: founder labor valued at the contractor rate for unit economics only"),
    "build_h_per_box": (12.0, "ESTIMATE: assembly 3 h, 48 h unattended burn-in (memtest/GPU), OS + FIPS mode + SGLang/KTransformers + model load + benchmark 9 h"),
    "install_h_per_box": (8.0, "ESTIMATE: on-site install incl. regional travel"),
    "setup_h_per_box": (16.0, "ESTIMATE: RAG connectors, SSO, boundary/SSP inserts (paid by the setup fee)"),
    "fleet_fixed_h": (12.0, "ESTIMATE: re-quantize/test new model releases, image builds, release notes per month once a fleet exists"),
    "admin_h": (8.0, "ESTIMATE: bookkeeping, quoting, procurement"),
    "h_per_conversation": (3.0, "ESTIMATE: research, discovery call, follow-up, proposal per qualified conversation"),
    "min_sales_share": (0.20, "ESTIMATE: founder keeps >=20% of hours for selling; builds/support beyond that go to a contractor"),
    "field_tech_cost": (7_500.0, "ESTIMATE: ~$65k salary + 15% load"),
    "field_tech_hours": (150.0, "ESTIMATE: productive hours per month"),
    "field_tech_fleet_trigger": (30.0, "ESTIMATE: hire a field tech once >=30 boxes are under subscription and the founder is full-time"),

    # --- Acquisition ---
    "demo_ready_month": (3.0, "ESTIMATE: rented-host demo + published benchmark by m3"),
    "conv_target_pt": (5.0, "ESTIMATE: qualified conversations per month a 15 h/week founder can source (outbound to MSPs/RPOs, legal IT, DIB subs)"),
    "conv_target_ft": (14.0, "ESTIMATE: full-time founder"),
    "channel_start_month": (13.0, "ESTIMATE: first MSP/RPO reseller signed after ~4 reference installs"),
    "channel_conv_month": (3.0, "ESTIMATE: qualified conversations per month from channel partners (1 founder hour each)"),
    "conversion": (0.08, "ESTIMATE: qualified conversation -> order; B2B hardware with 3-6 month security review (C-48 verify_corrections)"),
    "sales_cycle_m": (4.0, "C-48 verify_corrections: regulated buyers run 3-6 month security and procurement reviews"),
    "expansion_rate": (0.15, "ESTIMATE: share of customers who order a second box 12 months after the first"),

    # --- Fixed opex ---
    "demo_rent_month": (1_200.0, "ESTIMATE: bare-metal 768GB+ RAM / 1-GPU host rental for demos m2-m9 (availability not confirmed: open gap)"),
    "demo_rent_until": (9.0, "ESTIMATE: rent until an own demo box is bought"),
    "demo_buy_month": (10.0, "ESTIMATE: buy an S-class demo box (at BOM) in the first month >= m10 in which cash stays >= $15k after the purchase; rent until then"),
    "demo_buy_cash_buffer": (15_000.0, "ESTIMATE: founder policy, keep $15k after buying the demo box"),
    "oncall_month": (0.0, "ESTIMATE: BASE sells a business-hours, next-business-day SLA; a 24/7 on-call retainer (~$2,500/month, 05_REDTEAM.md DD4) is tested as a sensitivity"),
    "bench_capex": (2_500.0, "ESTIMATE: ESD bench, tools, UPS, switch, burn-in rack (m2)"),
    "legal_setup": (3_000.0, "ESTIMATE: MSA, warranty/subscription terms, export/ITAR handling language (m1)"),
    "esp_compliance_setup": (8_000.0, "ESTIMATE: own support-process SSP, escorted-remote-session tooling, gap review so a CMMC customer can include us as an External Service Provider (m9)"),
    "esp_compliance_month": (400.0, "ESTIMATE: ongoing ESP compliance upkeep from m9"),
    "insurance_month": (500.0, "ESTIMATE: GL + E&O + cyber from m6 (DD4 used $400 E&O alone)"),
    "software_month": (150.0, "ESTIMATE: website, CRM, repo hosting, benchmark storage"),
    "legal_acct_month": (300.0, "ESTIMATE: bookkeeping and occasional contract review"),
    "marketing_pt": (600.0, "ESTIMATE: content, benchmark publishing, one regional event per quarter"),
    "marketing_ft": (1_500.0, "ESTIMATE: adds CMMC Con / legal-tech conference presence"),

    # --- Performance inputs (evidence -> capacity) ---
    "L_single_tps": (17.0, "ESTIMATE: KTransformers DeepSeek-R1 8.73 tok/s on 1S Xeon 6454S 8ch DDR5-4800 (" + _KT_R1 + ") x2.0 bandwidth (12ch DDR5-6400) x37/32 active params = 20.2, derated 0.85 for EPYC/1-GPU; cross-check MiniMax-M2.1 32 tok/s on 2S EPYC 9355 + 1x RTX 5090 at ~0.8x Kimi bytes/token (" + _KT_MM + ")"),
    "S_single_tps": (25.0, "ESTIMATE: MiniMax-M2.1 32.1 tok/s on 2S EPYC 9355 + 1x RTX 5090 (" + _KT_MM + ") / 1.29 dual-socket gain (" + _KT_R1 + ")"),
    "conc_exponent": (0.62, "ESTIMATE: fits KTransformers +130% aggregate at 4-way concurrency (" + _KT_BAL + ")"),
    "conc_saturation": (2.4, "ESTIMATE: Xeon 6 + MRDIMM-8800 aggregate 17 -> 40 tok/s (2.35x) with concurrency, GPU-bound after (" + _KT_BAL + ")"),
    "min_user_tps": (10.0, "ESTIMATE: acceptable streaming speed for chat/RAG per user"),
    "peak_active_share": (0.15, "ESTIMATE: share of named users generating at the same moment at peak"),
    "L_prefill_2k": (106.0, "ESTIMATE: Kimi-K2-Thinking native 53 tok/s at 2k on 1x 48GB GPU, PCIe 4.0 (" + _KT_KN + ") x2 for PCIe 5.0 layerwise weight streaming"),
    "L_prefill_8k": (368.0, "ESTIMATE: same source, 184 tok/s at 8k x2"),
    "S_prefill_2k": (408.0, "MiniMax-M2.1, 1x RTX 5090 + 2x EPYC 9355, PCIe 5.0, 2k prompt (" + _KT_MM + ")"),
    "S_prefill_8k": (1_196.0, "MiniMax-M2.1, same config, 8k prompt (" + _KT_MM + ")"),

    # --- Substitutes (per named user per month over 36 months) ---
    "mac512_price": (22_299.0, "https://www.ithinkdiff.com/512gb-mac-studio-m5-ultra-price-22299/ (snippet, 2026-10): Mac Studio M5 Ultra 512GB"),
    "mac512_users": (5.0, "ESTIMATE: single-stream oriented (llama.cpp/MLX), M3 Ultra Kimi-K2.5 5-15 tok/s (https://developer.tenten.co/how-to-run-kimi-k25-locally-on-mac-studio-m3-ultra-with-512gb, snippet); 1T models only at ~3-bit in 512 GB"),
    "dgx_station_price": (90_000.0, "https://www.servethehome.com/nvidia-dgx-station-systems-available-at-last-gb300-gb200-workstations-for-your-desktop (snippet: from $87,411.50); Exxact $94,930 (Tom's Hardware snippet)"),
    "dgx_station_users": (80.0, "ESTIMATE: 288 GB HBM3e + 496 GB LPDDR5X (Wccftech snippet: 748 GB coherent); a 1T INT4 model (~600 GB) spills experts to LPDDR5X over NVLink-C2C, so ~3x the L box users, not 10x"),
    "copilot_gcch_user_month": (35.0, "ESTIMATE [UNVERIFIED-training]: M365 Copilot list ~$30/user/month commercial; GCC High GA Dec-2025 (https://www.daymarksi.com/blog/microsoft-365-copilot-in-gcc-high-what-dib-subcontractors-need-to-know-about-deploying-ai-without-breaking-cmmc, snippet), GCC High price not found"),
    "managed_private_user_month": (16.0, _IBL),
    "legal_seat_user_month": (104.0, "https://spellbook.com/learn/legal-ai-tool-pricing (snippet: CoCounsel $104-639/user/month; Spellbook $100-300)"),
}

# ----------------------------------------------------------------------------------------------
# RED-TEAM REVISIONS (Phase 5) -- agent p5r-private-moe-appliance, 2026-11-01
# Objections: research/phase5/rt2_{VET,VC,HYP,PHY}.json (dd == "DD6"). Each entry: old -> new, objection id.
# Step 1 adds NEW mechanic inputs at Phase-4-neutral values (so Phase 4 still reproduces).
# Step 2 (REVISIONS) overrides old and new inputs with the post-red-team values.
# ----------------------------------------------------------------------------------------------
_RT = "research/phase5/rt2_*.json"
NEW_INPUTS = {
    # DRAM premium path: the small-buyer premium is a shortage premium; it unwinds across the 2028 turn
    "dram_premium_post_turn": (1.15, "ESTIMATE: small-buyer premium over contract once supply loosens (2028 turn); Phase 4 used 1.15 throughout"),
    # demand response to price RISES vs the Phase-4 price card (Phase 4: none)
    "elast_up": (0.0, "ESTIMATE: units fall elast_up % per 1% the box price sits above the Phase-4 price card"),
    "ref_mode": (0.0, "0 = elasticity reference is this run's own m1 price (Phase 4); 1 = the fixed Phase-4 price card"),
    # VAR / MSP paper on founder-sourced deals (Phase 4: none)
    "paper_share": (0.0, "ESTIMATE: share of founder-sourced orders that must be placed on a VAR/MSP contract vehicle"),
    "paper_fee": (0.0, "ESTIMATE: fee to the VAR carrying the paper, share of hardware revenue"),
    # quote-to-purchase cost drift absorbed by the integrator (Phase 4: none)
    "quote_drift": (0.0, "ESTIMATE: expected BOM drift between the approved quote and parts purchase that the integrator absorbs"),
    # spare-parts pool held as inventory (Phase 4: none)
    "spare_kit_boxes": (0.0, "ESTIMATE: one spare RDIMM (SKU-mix sized) per this many boxes under subscription; 0 = off"),
    "loaner_gpu_trigger": (0.0, "ESTIMATE: buy one 48 GB loaner GPU once this many boxes are under subscription; 0 = off"),
    # subscription capped by what the box can serve (Phase 4: no cap)
    "sub_user_cap": (0.0, "ESTIMATE: $/named user/month ceiling on a box subscription; 0 = off"),
    # capacity model switch and bandwidth-model inputs
    "capacity_model": ("phase4", "'phase4' = conc_exponent/conc_saturation fit; 'bandwidth' = distinct-expert bytes / effective DRAM bandwidth"),
    "bw_peak_gbs": (576.0, "AMD EPYC 9005 architecture guide 58462 (via RT-VET-DD6-01): 12 ch x DDR5-6000 platform max x 8 B = 576 GB/s; 6400 only on some validated boards [REPORTED via red team]"),
    "bw_eff": (0.50, "ESTIMATE: share of peak an expert-streaming engine sustains; P1 (8.73 tok/s, ~12.2 GB routed/token, 307 GB/s peak) implies >=0.35 with zero overhead, ~0.47 with ~30 ms fixed time; STREAM-class ~0.8 is not reachable while also syncing a GPU every layer"),
    "experts_active": (8.0, "Kimi-K2.x and MiniMax-M2 route 8 experts per token per MoE layer (public configs, via RT-PHY-DD6-01)"),
    "L_experts": (384.0, "Kimi-K2.5: 384 routed experts per MoE layer (" + _KT_K25 + ")"),
    "S_experts": (256.0, "MiniMax-M2.x: 256 routed experts per MoE layer (public config, via RT-PHY-DD6-01)"),
    "L_routed_gb": (11.9, "RT-PHY-DD6-01 config arithmetic: 8 x 3x7168x2048 params x 60 MoE layers = 21.1B routed params/token at ~4.5 bits (INT4, group 32)"),
    "S_routed_gb": (7.0, "RT-PHY-DD6-01: MiniMax-M2 8 x 3x3072x1536 x 62 layers = 7.0B routed params/token at FP8"),
    "L_tfix_ms": (20.0, "ESTIMATE: per-step fixed time (GPU attention/shared experts, PCIe sync, launches) for 61-layer Kimi on kt-kernel+SGLang"),
    "S_tfix_ms": (18.0, "ESTIMATE: calibrated so P2 (2S EPYC 9355 + 5090, 32.1 tok/s = 31 ms/step) is reproduced at ~0.5 x 1,152 GB/s"),
    "L_vram_gb": (96.0, "RTX PRO 6000 Blackwell 96 GB"),
    "S_vram_gb": (32.0, "Phase 4 S GPU: GeForce RTX 5090 32 GB"),
    "L_vram_fixed_gb": (44.0, "ESTIMATE (RT-PHY-DD6-03 method): ~11.5B non-routed params ~23 GB + 19 GB layerwise-prefill double buffer + 2 GB workspace"),
    "S_vram_fixed_gb": (13.2, "RT-PHY-DD6-03: ~4 GB non-expert FP8 + 7.2 GB layer double buffer + 2 GB workspace"),
    "L_kv_kb_per_tok": (70.0, "RT-PHY-DD6-03: Kimi MLA KV ~70 KB/token"),
    "S_kv_kb_per_tok": (124.0, "RT-PHY-DD6-03: MiniMax-M2 GQA 8 KV heads x 128 x 62 layers at FP8 = 124 KB/token"),
    "design_ctx_tokens": (32_000.0, "ESTIMATE: RAG design context per active user (the S box's own 32k benchmark, P2); RT-PHY-DD6-03, RT-VC-DD6-11"),
}
for _k, _v in NEW_INPUTS.items():
    INPUTS[_k] = _v

# name -> (new value, "old -> new; objection id(s); basis")
REVISIONS = {
    "dram_small_buyer_premium": (1.65, "1.15 -> 1.65 pre-turn ($29.65 -> $42.5 per user-GB; 64 GB RDIMM $1,898 -> $2,722); RT-VET-DD6-02. Basis: doc's own street $32/GB (Aug-26) x ServerMonkey +35% Aug-Oct (reviewer-cited) = $43; Origin Storage 64GB-6400 GBP 2,516 special (~$52/GB, avoira.com snippet); Fusion $46-58/GB (reviewer-cited, not confirmed). Unwinds to 1.15 across 2028 (dram_premium_post_turn)"),
    "S_gpu": (8_216.0, "$5,000 GeForce RTX 5090 (Micro Center retail) -> $8,216 RTX PRO 5000 Blackwell 48GB via SHI (MSRP $8,999); RT-VET-DD6-03, RT-HYP-DD6-09 (GeForce 'no datacenter deployment' licence, consumer warranty, retail not an authorized distributor), RT-PHY-DD6-03 (48 GB fixes the KV ceiling)"),
    "S_vram_gb": (48.0, "32 -> 48 GB (RTX PRO 5000 Blackwell); RT-PHY-DD6-03"),
    "mix_L": (0.0, "0.50 -> 0.00 in BASE: the L SKU is not quoted until a socket-pinned Track B run shows >=10 tok/s per user at >=2 concurrent; bandwidth arithmetic gives 1-2 users (7-13 named); RT-VET-DD6-01 (FATAL), RT-PHY-DD6-01/02, RT-HYP-DD6-04/05, RT-VC-DD6-07/08/09/11, RT-HYP-DD6-03. Re-admission tested as a sensitivity"),
    "L_dram_gb": (832.0, "768 -> 832 GB bought (13 x 64 GB: 12 installed + 1 on-site cold spare; a 10-DIMM fallback is below the 650 GB floor); RT-PHY-DD6-05"),
    "capacity_model": ("bandwidth", "'phase4' -> 'bandwidth': conc_saturation 2.4 was measured on a ~845 GB/s Xeon 6 MRDIMM socket; per-step bytes now scale with distinct experts touched; RT-VET-DD6-01, RT-PHY-DD6-01, RT-PHY-DD6-02"),
    "sub_user_cap": (50.0, "off -> $50/named user/month (the Phase-4 anchor: ~25 users x $50 = $1,250); an L box serving ~13 named users bills <= ~$667; RT-VET-DD6-01 (simulate() never read capacity)"),
    "conversion": (0.06, "0.08 -> 0.06: unmeasured close rate for a new single-member LLC (supplier onboarding, SOC 2/COI/financials gates); CMMC Phase 2 suspended 2026-07-13 removes urgency; RT-VC-DD6-02, RT-HYP-DD6-01, RT-HYP-DD6-08"),
    "sales_cycle_m": (7.0, "4 -> 7 months: discovery -> 60-day paid pilot -> 3-6 month security review -> PO, as section 4 prescribes; RT-HYP-DD6-02"),
    "paper_share": (0.5, "0 -> 0.5 of founder-sourced orders placed on a VAR/MSP contract vehicle (CDW-G/SHI/Carahsoft-class or the partner's paper); RT-HYP-DD6-01"),
    "paper_fee": (0.05, "0 -> 5% of hardware to the VAR carrying the paper; RT-HYP-DD6-01"),
    "insurance_month": (900.0, "$500 -> $900/month: $1-2M cyber/E&O + GL + product liability limits a regulated buyer's COI demands (cf. RT-HYP-DD1-08); RT-HYP-DD6-01"),
    "partner_hw_commission": (0.15, "0.10 -> 0.15: at 10% the MSP earns less than building the box itself; RT-VC-DD6-06"),
    "partner_sub_commission": (0.20, "0.15 -> 0.20; RT-VC-DD6-06"),
    "channel_conv_month": (2.0, "3 -> 2 conversations/month: the partners are also competitors (Petronella) and the CMMC rush is paused; RT-VC-DD6-06, RT-HYP-DD6-08"),
    "sub_churn_annual": (0.30, "0.20 -> 0.30: an air-gapped box's patches and model refreshes are work the customer's own MSP can do; RT-VC-DD6-04"),
    "oncall_month": (500.0, "$0 -> $500/month business-hours backup-technician retainer from first delivery (U.S. person, named); RT-VC-DD6-03, RT-HYP-DD6-06"),
    "h_per_conversation": (4.0, "3 -> 4 h: adds security questionnaires, SSP inserts and pilot support; RT-VC-DD6-03"),
    "parts_reserve_pct_yr": (0.04, "0.03 -> 0.04 of box cost per year (GPU field failures ~3%/yr at a third of the Llama-3 training rate); RT-HYP-DD6-06"),
    "spare_kit_boxes": (5.0, "off -> one spare RDIMM per 5 boxes under subscription, held as inventory; RT-VET-DD6-06, RT-PHY-DD6-05"),
    "loaner_gpu_trigger": (5.0, "off -> one 48 GB loaner GPU (RTX PRO 5000) once 5 boxes are under subscription; it runs either SKU degraded; RT-HYP-DD6-06"),
    "elast_up": (0.5, "0 -> 0.5: units fall 0.5% per 1% the box price sits above the Phase-4 card (low end of the reviewer range -0.5..-1.0: OEM servers inflate with the same DRAM, Apple/NVIDIA unified-memory prices and cloud seats do not); RT-VC-DD6-01, RT-VET-DD6-02"),
    "ref_mode": (1.0, "0 -> 1: elasticity measured against the fixed Phase-4 price card ($62,525 L / $30,622 S) on which the close rate was assumed; RT-VC-DD6-01"),
    "quote_drift": (0.03, "0 -> 3% of BOM absorbed between approved quote and purchase (index clause covers the rest; quotes now 30 days with a DRAM/GPU index adjuster); RT-HYP-DD6-07"),
    "install_h_per_box": (12.0, "8 -> 12 h: electrical/thermal survey, dedicated 20 A circuit or rack placement, DIMM-temperature check; RT-PHY-DD6-04"),
}
P_PHASE4 = {name: INPUTS[name][0] for name in REVISIONS}   # run_with(P_PHASE4, scen) reproduces Phase 4
for _k, (_v, _why) in REVISIONS.items():
    INPUTS[_k] = (_v, INPUTS[_k][1] + " || RED-TEAM (Phase 5): " + _why)


_OVR = {}


def I(name):
    if name in _OVR:
        return _OVR[name]
    return INPUTS[name][0]


def run_with(overrides, scen, **kw):
    """simulate() with temporary INPUTS overrides (used for sensitivity rows)."""
    _OVR.clear()
    _OVR.update(overrides)
    try:
        return simulate(scen, **kw)
    finally:
        _OVR.clear()


MONTHS = 36
START_YEAR, START_MONTH = 2026, 11
TURN_MONTH = 15  # Jan-2028 = 2028-Q1


def month_label(m):
    idx = START_MONTH - 1 + (m - 1)
    return "%d-%02d" % (START_YEAR + idx // 12, idx % 12 + 1)


# ----------------------------------------------------------------------------------------------
# Price paths
# ----------------------------------------------------------------------------------------------
def dram_price(m, scen):
    """$/user-GB the integrator pays in month m (contract deck x small-buyer premium)."""
    now = I("dram_now_per_user_gb")
    if scen == "BASE":
        if m < TURN_MONTH:
            p = now
        else:
            frac = min(1.0, (m - TURN_MONTH + 1) / 12.0)
            p = now * (1.0 - I("base_turn_depth") * frac)
    elif scen == "GLUT":
        p = now if m < TURN_MONTH else I("dram_glut_per_user_gb")
    elif scen == "SEVERE":
        p = now if m < TURN_MONTH else I("dram_severe_per_user_gb")
    else:
        raise ValueError(scen)
    return p * dram_premium(m, scen)


def dram_premium(m, scen):
    """Small-buyer premium over contract: a shortage premium that unwinds across the 2028 turn (Phase 5)."""
    pre, post = I("dram_small_buyer_premium"), I("dram_premium_post_turn")
    if m < TURN_MONTH:
        return pre
    if scen == "BASE":
        frac = min(1.0, (m - TURN_MONTH + 1) / 12.0)
        return pre + (post - pre) * frac
    return post


def gpu_factor(m, scen):
    if m < TURN_MONTH:
        return 1.0
    if scen == "BASE":
        frac = min(1.0, (m - TURN_MONTH + 1) / 12.0)
        return 1.0 - I("gpu_base_turn") * frac
    if scen == "GLUT":
        return I("gpu_glut_factor")
    return I("gpu_severe_factor")


def bom(sku, m, scen, cogs_mult=1.0):
    d = dram_price(m, scen) * I(sku + "_dram_gb")
    g = I(sku + "_gpu") * gpu_factor(m, scen)
    c = I(sku + "_cpu")
    p = I(sku + "_platform")
    tot = (d + g + c + p) * cogs_mult
    return dict(dram=d * cogs_mult, gpu=g * cogs_mult, cpu=c * cogs_mult, platform=p * cogs_mult, total=tot)


def hw_price(sku, m, scen, gm):
    return bom(sku, m, scen)["total"] / (1.0 - gm)


# ----------------------------------------------------------------------------------------------
# Performance / capacity (from the KTransformers evidence)
# ----------------------------------------------------------------------------------------------
def per_user_tps(single, c):
    agg = single * min(c ** I("conc_exponent"), I("conc_saturation"))
    return agg / c


def capacity_phase4(sku):
    single = I(sku + "_single_tps")
    cstar = 1
    for c in range(1, 65):
        if per_user_tps(single, c) >= I("min_user_tps"):
            cstar = c
    users = cstar / I("peak_active_share")
    return dict(single=single, cstar=cstar, users=users,
                ttft2k=2048.0 / I(sku + "_prefill_2k"), ttft8k=8192.0 / I(sku + "_prefill_8k"))


def distinct_mult(c, n_exp, k):
    """Expected distinct routed experts per layer for c independent tokens, as a multiple of one token's k."""
    return (n_exp / k) * (1.0 - (1.0 - k / n_exp) ** c)


def bw_user_tps(sku, c, bw=None, eff=None, tfix=None, routed=None):
    """Per-user decode tok/s at c concurrent streams: step = t_fix + distinct-expert bytes / effective bandwidth
    (RT-VET-DD6-01, RT-PHY-DD6-01). Uniform independent routing; routing skew would lower distinct_mult a little."""
    bw = I("bw_peak_gbs") if bw is None else bw
    eff = I("bw_eff") if eff is None else eff
    tfix = I(sku + "_tfix_ms") if tfix is None else tfix
    routed = I(sku + "_routed_gb") if routed is None else routed
    d = distinct_mult(c, I(sku + "_experts"), I("experts_active"))
    step_ms = tfix + 1000.0 * d * routed / (bw * eff)
    return 1000.0 / step_ms


def kv_max_users(sku):
    free_gb = I(sku + "_vram_gb") - I(sku + "_vram_fixed_gb")
    per_user_gb = I("design_ctx_tokens") * I(sku + "_kv_kb_per_tok") / 1e6
    return max(0, int(free_gb / per_user_gb)) if per_user_gb > 0 else 64


def capacity_bandwidth(sku, **kw):
    single = bw_user_tps(sku, 1, **kw)
    cstar = 1
    for c in range(1, 65):
        if bw_user_tps(sku, c, **kw) >= I("min_user_tps"):
            cstar = c
    kvmax = kv_max_users(sku)
    cstar = max(1, min(cstar, kvmax))
    users = cstar / I("peak_active_share")
    return dict(single=single, cstar=cstar, users=users, kvmax=kvmax,
                ttft2k=2048.0 / I(sku + "_prefill_2k"), ttft8k=8192.0 / I(sku + "_prefill_8k"))


def capacity(sku):
    if I("capacity_model") == "bandwidth":
        return capacity_bandwidth(sku)
    return capacity_phase4(sku)


def sub_price(sku):
    """List subscription, capped at sub_user_cap x named users when the cap is on (Phase 5)."""
    lst = I("sub_%s_month" % sku)
    cap = I("sub_user_cap")
    if cap > 0:
        return min(lst, cap * capacity(sku)["users"])
    return lst


# ----------------------------------------------------------------------------------------------
# Simulation
# ----------------------------------------------------------------------------------------------
def _phase4_card():
    """Phase-4 price card (BASE, m1, 22% GM, Phase-4 inputs): the price the 8% close rate was assumed at."""
    saved = dict(_OVR)
    _OVR.clear()
    _OVR.update(P_PHASE4)
    try:
        return {s: hw_price(s, 1, "BASE", I("hw_gm")) for s in "LS"}
    finally:
        _OVR.clear()
        _OVR.update(saved)


REF_CARD = _phase4_card()

DEFAULTS = dict(price_mult=1.0, conv_mult=1.0, churn_mult=1.0, cogs_mult=1.0, sub_price_mult=None,
                gm=None)


def simulate(scen, months=MONTHS, **kw):
    o = dict(DEFAULTS)
    o.update(kw)
    gm = I("hw_gm") * o["price_mult"] if o["gm"] is None else o["gm"]
    sub_mult = o["price_mult"] if o["sub_price_mult"] is None else o["sub_price_mult"]
    conv_rate = I("conversion") * o["conv_mult"]
    churn = min(0.95, I("sub_churn_annual") * o["churn_mult"])
    cm = o["cogs_mult"]
    sub_month = {"L": sub_price("L") * sub_mult, "S": sub_price("S") * sub_mult}
    setup_fee = I("setup_fee") * sub_mult
    mixw = {"L": I("mix_L"), "S": 1.0 - I("mix_L")}
    if I("ref_mode") >= 1:
        base_box_price = sum(mixw[s] * REF_CARD[s] for s in "LS")
    else:
        base_box_price = sum(mixw[s] * hw_price(s, 1, scen, gm) for s in "LS")
    spare_kits = 0
    spare_inv = 0.0
    loaner_bought = False
    cum_sub_billed = 0.0
    cum_sub_rev = 0.0
    pt_months = 0
    sub_gp_24 = 0.0
    hw_gp_24 = 0.0

    cash = I("founder_capital")
    ext_cap = 0.0
    full_time = False
    ft_month = None
    field_techs = 0
    conv_hist = {}          # month -> (direct conversations, channel conversations)
    orders = {}             # month -> dict(units, channel_units, price/bom per sku)
    cohorts = []            # (delivery_month, units_by_sku, channel_share)
    cust_hist = {}          # month -> customers acquired (orders placed)
    cum_taxable = 0.0
    taxed = 0.0
    rows = []
    op_hist = []
    hours_short_total = 0.0
    demo_bought = False

    for m in range(1, months + 1):
        avail = I("founder_hours_ft") if full_time else I("founder_hours_pt")

        # ---- active subscription fleet (start of month) ----
        active = {"L": 0.0, "S": 0.0}
        active_ch = 0.0
        sub_cash_in = 0.0
        sub_cash_partner = 0.0
        for (dm, units, chs) in cohorts:
            if m < dm:
                continue
            age = m - dm
            surv = (1.0 - churn) ** (age // 12)
            for s in "LS":
                active[s] += units[s] * surv
                active_ch += units[s] * surv * chs
            if age % 12 == 0:  # annual billing in advance at delivery and each anniversary
                bill = sum(units[s] * surv * sub_month[s] * 12.0 for s in "LS")
                sub_cash_in += bill
                sub_cash_partner += bill * chs * I("partner_sub_commission")
        fleet = active["L"] + active["S"]

        # ---- deliveries this month = orders placed last month ----
        od = orders.get(m - 1)
        deliv_units = {"L": 0.0, "S": 0.0}
        hw_rev = 0.0
        hw_bom_deliv = 0.0
        hw_balance_cash = 0.0
        partner_hw = 0.0
        deliv_ch_share = 0.0
        if od:
            for s in "LS":
                deliv_units[s] = od["units"][s]
                hw_rev += od["units"][s] * od["price"][s]
                hw_bom_deliv += od["units"][s] * od["bom"][s]
            hw_balance_cash = hw_rev * (1.0 - I("deposit_pct"))
            deliv_ch_share = od["ch_share"]
            partner_hw = hw_rev * (deliv_ch_share * I("partner_hw_commission")
                                   + (1.0 - deliv_ch_share) * I("paper_share") * I("paper_fee"))
            if deliv_units["L"] + deliv_units["S"] > 0:
                cohorts.append((m, dict(deliv_units), deliv_ch_share))
                # first-year subscription billed at delivery: count it now (cohort age 0 this month)
                bill = sum(deliv_units[s] * sub_month[s] * 12.0 for s in "LS")
                sub_cash_in += bill
                sub_cash_partner += bill * deliv_ch_share * I("partner_sub_commission")
                for s in "LS":
                    active[s] += deliv_units[s]
                active_ch += (deliv_units["L"] + deliv_units["S"]) * deliv_ch_share
                fleet = active["L"] + active["S"]
        n_deliv = deliv_units["L"] + deliv_units["S"]
        setup_rev = n_deliv * setup_fee

        # ---- founder hours ----
        fixed_h = I("admin_h") + (I("fleet_fixed_h") if (fleet > 0 or m >= I("demo_ready_month")) else 13.0)
        support_h = fleet * I("support_h_per_box_month")
        build_h = n_deliv * (I("build_h_per_box") + I("install_h_per_box") + I("setup_h_per_box"))
        tech_h = field_techs * I("field_tech_hours")
        ops_h = support_h + build_h
        ops_by_tech = min(ops_h, tech_h)
        ops_left = ops_h - ops_by_tech
        founder_ops_cap = max(0.0, avail - fixed_h - avail * I("min_sales_share"))
        founder_ops = min(ops_left, founder_ops_cap)
        contractor_h = ops_left - founder_ops
        sales_h = max(0.0, avail - fixed_h - founder_ops)

        # ---- sales conversations and orders ----
        direct = 0.0
        channel = 0.0
        if m >= I("demo_ready_month"):
            target = I("conv_target_ft") if full_time else I("conv_target_pt")
            direct = min(target, sales_h / I("h_per_conversation"))
            if m >= I("channel_start_month"):
                channel = I("channel_conv_month")
                direct = min(direct, max(0.0, (sales_h - channel * 1.0) / I("h_per_conversation")))
        conv_hist[m] = (direct, channel)
        lag = int(I("sales_cycle_m"))
        new_orders = 0.0
        ch_orders = 0.0
        if (m - lag) in conv_hist:
            d0, c0 = conv_hist[m - lag]
            box_price_now = sum(mixw[s] * hw_price(s, m, scen, gm) for s in "LS")
            ratio = box_price_now / base_box_price
            elast = 1.0 + I("glut_elasticity") * max(0.0, 1.0 - ratio) - I("elast_up") * max(0.0, ratio - 1.0)
            elast = max(0.1, elast)
            new_orders = (d0 + c0) * conv_rate * elast
            ch_orders = c0 * conv_rate * elast
        expansion = cust_hist.get(m - 12, 0.0) * I("expansion_rate")
        cust_hist[m] = new_orders
        tot_orders = new_orders + expansion
        ch_share = (ch_orders / tot_orders) if tot_orders > 0 else 0.0
        order_cash_out = 0.0
        deposit_cash = 0.0
        if tot_orders > 0:
            units = {s: tot_orders * mixw[s] for s in "LS"}
            price = {s: hw_price(s, m, scen, gm) for s in "LS"}
            b = {s: bom(s, m, scen, cm)["total"] * (1.0 + I("quote_drift")) for s in "LS"}
            orders[m] = dict(units=units, price=price, bom=b, ch_share=ch_share)
            order_cash_out = sum(units[s] * b[s] for s in "LS")      # parts bought on order
            deposit_cash = sum(units[s] * price[s] for s in "LS") * I("deposit_pct")

        # ---- P&L (recognized) ----
        sub_rev = sum(active[s] * sub_month[s] for s in "LS")
        revenue = hw_rev + setup_rev + sub_rev
        warranty = hw_rev * I("warranty_reserve_pct")
        ship = n_deliv * I("ship_per_box")
        parts_res = sum(active[s] * bom(s, 1, scen, cm)["total"] for s in "LS") * I("parts_reserve_pct_yr") / 12.0
        tooling = fleet * I("tooling_per_box_month") * cm
        contractor = contractor_h * I("contractor_rate")
        partner = partner_hw + sum(active[s] * sub_month[s] for s in "LS") * (active_ch / fleet if fleet else 0.0) * I("partner_sub_commission")
        cogs = hw_bom_deliv + warranty + ship + parts_res + tooling + contractor + partner
        gp = revenue - cogs

        opex = I("software_month") + I("legal_acct_month")
        opex += I("marketing_ft") if full_time else I("marketing_pt")
        if m >= 6:
            opex += I("insurance_month")
        if m >= 2 and not demo_bought:
            opex += I("demo_rent_month")
        if fleet > 0:
            opex += I("oncall_month")
        if m >= 9:
            opex += I("esp_compliance_month")
        one_time = 0.0
        if m == 1:
            one_time += I("legal_setup")
        if m == 2:
            one_time += I("bench_capex")
        if m == 9:
            one_time += I("esp_compliance_setup")
        if (not demo_bought) and m >= int(I("demo_buy_month")):
            demo_cost = bom("S", m, scen, cm)["total"]
            if cash - demo_cost >= I("demo_buy_cash_buffer"):
                one_time += demo_cost
                demo_bought = True
        salary = I("founder_salary_ft") if full_time else 0.0
        tech_cost = field_techs * I("field_tech_cost")
        ebitda = gp - opex - one_time - salary - tech_cost

        # ---- tax (30% on positive cumulative taxable income, loss carry-forward) ----
        cum_taxable += ebitda
        tax = 0.0
        if cum_taxable > taxed:
            tax = (cum_taxable - taxed) * I("tax_rate")
            taxed = cum_taxable
        net = ebitda - tax

        # ---- spare-parts pool held as inventory (Phase 5; RT-VET-DD6-06, RT-HYP-DD6-06, RT-PHY-DD6-05) ----
        spare_cash = 0.0
        if I("spare_kit_boxes") > 0 and fleet > 0:
            need = int(math.ceil(fleet / I("spare_kit_boxes") - 1e-9))
            if need > spare_kits:
                kit_val = (mixw["L"] * 64.0 + mixw["S"] * 32.0) * dram_price(m, scen)
                spare_cash += (need - spare_kits) * kit_val
                spare_kits = need
        if I("loaner_gpu_trigger") > 0 and (not loaner_bought) and fleet >= I("loaner_gpu_trigger"):
            spare_cash += I("S_gpu") * gpu_factor(m, scen)
            loaner_bought = True
        spare_inv += spare_cash

        # ---- honesty metrics (Phase 5; RT-VC-DD6-04, RT-VC-DD6-05) ----
        cum_sub_billed += sub_cash_in
        cum_sub_rev += sub_rev
        if not full_time:
            pt_months += 1
        if 13 <= m <= 24:
            sub_part = sum(active[s] * sub_month[s] for s in "LS") * (active_ch / fleet if fleet else 0.0) * I("partner_sub_commission")
            sub_gp_24 += (sub_rev - parts_res - tooling - sub_part - (I("oncall_month") if fleet > 0 else 0.0)
                          - support_h * I("shadow_rate"))
            hw_gp_24 += (hw_rev + setup_rev - hw_bom_deliv - warranty - ship - partner_hw
                         - build_h * I("shadow_rate"))
        arr_renewal_tested = 0.0
        for (dm, units, chs) in cohorts:
            if m - dm >= 12:
                surv = (1.0 - churn) ** ((m - dm) // 12)
                arr_renewal_tested += sum(units[s] * surv * sub_month[s] * 12.0 for s in "LS")

        # ---- cash ----
        cash_in = deposit_cash + hw_balance_cash + setup_rev + sub_cash_in
        cash_out = (order_cash_out + warranty + ship + parts_res + tooling + contractor + partner_hw
                    + sub_cash_partner + opex + one_time + salary + tech_cost + tax + spare_cash)
        cash += cash_in - cash_out
        drawn = 0.0
        if cash < I("cash_floor"):
            need = I("cash_floor") - cash
            drawn = math.ceil(need / I("ext_tranche")) * I("ext_tranche")
            cash += drawn
            ext_cap += drawn

        arr = sum(active[s] * sub_month[s] for s in "LS") * 12.0
        op_profit = gp - opex  # recurring operating profit before founder salary and one-offs
        op_hist.append(op_profit)
        hours_short_total += contractor_h
        rows.append(dict(m=m, label=month_label(m), ft=full_time, op_profit=op_profit, conv=direct + channel, orders=tot_orders,
                         deliv=n_deliv, fleet=fleet, hw_rev=hw_rev, setup_rev=setup_rev, sub_rev=sub_rev,
                         revenue=revenue, cogs=cogs, gp=gp, opex=opex + one_time + tech_cost, salary=salary,
                         ebitda=ebitda, tax=tax, net=net, cash=cash, drawn=drawn, arr=arr,
                         contractor_h=contractor_h, sales_h=sales_h, techs=field_techs,
                         box_price=sum(mixw[s] * hw_price(s, m, scen, gm) for s in "LS"),
                         arr_rt=arr_renewal_tested, spare_inv=spare_inv, deposit_in=deposit_cash,
                         deferred=cum_sub_billed - cum_sub_rev))

        # ---- state transitions for next month ----
        if not full_time and m >= 3:
            trail = sum(op_hist[-3:]) / min(3, len(op_hist))
            if trail >= I("founder_salary_ft") and cash >= I("ft_trigger_cash"):
                full_time = True
                ft_month = m + 1
        if full_time and fleet >= I("field_tech_fleet_trigger") * (field_techs + 1):
            field_techs += 1

    res = summarize(rows, ext_cap, ft_month, scen)
    last = rows[-1]
    res["arr_rt36"] = last["arr_rt"]
    res["spare_inv"] = last["spare_inv"]
    res["customer_cash"] = last["deferred"] + last["deposit_in"]
    res["unpaid_hours"] = pt_months * I("founder_hours_pt")
    res["econ_profit"] = res["cum_net"] - res["unpaid_hours"] * I("shadow_rate")
    res["sub_gp_share_y2"] = (sub_gp_24 / (sub_gp_24 + hw_gp_24)) if (sub_gp_24 + hw_gp_24) > 0 else None
    return res


def summarize(rows, ext_cap, ft_month, scen):
    cash_low = min(r["cash"] - r["drawn"] for r in rows)
    cash_low_m = min(rows, key=lambda r: r["cash"] - r["drawn"])["m"]
    be = None
    for i, r in enumerate(rows):
        if i + 3 <= len(rows) and all(x["ebitda"] >= 0 for x in rows[i:i + 3]) and all(x["ebitda"] >= -1 for x in rows[i:]):
            be = r["m"]
            break
    sal_be = None
    for i, r in enumerate(rows):
        if i + 3 <= len(rows) and all(x["op_profit"] - I("founder_salary_ft") >= 0 for x in rows[i:i + 3]):
            sal_be = r["m"]
            break
    first_rev = next((r["m"] for r in rows if r["revenue"] > 0 or r["drawn"] < 0), None)
    first_cash = None
    for r in rows:
        if r["orders"] > 0:
            first_cash = r["m"]
            break
    arr = {k: rows[k - 1]["arr"] for k in (12, 18, 24, 36, 48, 60) if k <= len(rows)}
    cum_net = sum(r["net"] for r in rows)
    salary_paid = sum(r["salary"] for r in rows)
    boxes = sum(r["deliv"] for r in rows)
    return dict(scen=scen, rows=rows, ext_cap=ext_cap, ft_month=ft_month, cash_low=cash_low, sal_be=sal_be,
                cash_low_m=cash_low_m, breakeven=be, first_rev=first_rev, first_cash=first_cash,
                arr=arr, cum_net=cum_net, salary_paid=salary_paid, boxes=boxes,
                end_cash=rows[-1]["cash"], rev36=sum(r["revenue"] for r in rows),
                tax=sum(r["tax"] for r in rows), fleet36=rows[-1]["fleet"])


# ----------------------------------------------------------------------------------------------
# Unit economics
# ----------------------------------------------------------------------------------------------
def unit_economics(sku, m, scen):
    b = bom(sku, m, scen)
    gm = I("hw_gm")
    price = b["total"] / (1.0 - gm)
    hw_gp = price - b["total"] * (1.0 + I("quote_drift")) - price * I("warranty_reserve_pct") - I("ship_per_box")
    labor_one = (I("build_h_per_box") + I("install_h_per_box") + I("setup_h_per_box")) * I("shadow_rate")
    setup_gp = I("setup_fee") - I("setup_h_per_box") * I("shadow_rate")
    sub_m = sub_price(sku)
    sub_cost_m = (I("support_h_per_box_month") * I("shadow_rate") + I("tooling_per_box_month")
                  + bom(sku, 1, scen)["total"] * I("parts_reserve_pct_yr") / 12.0)
    sub_gm = 1.0 - sub_cost_m / sub_m
    churn = I("sub_churn_annual")
    yrs = 1.0 + (1.0 - churn) + (1.0 - churn) ** 2      # expected subscription years in a 3-year window
    ltv3 = hw_gp - (I("build_h_per_box") + I("install_h_per_box")) * I("shadow_rate") + setup_gp + yrs * 12 * (sub_m - sub_cost_m)
    cac = (1.0 / I("conversion")) * I("h_per_conversation") * I("shadow_rate") + 2_000.0  # + marketing allocation
    return dict(sku=sku, m=m, scen=scen, bom=b, price=price, hw_gp=hw_gp, hw_gm=hw_gp / price,
                labor_one=labor_one, setup_gp=setup_gp, sub_m=sub_m, sub_cost_m=sub_cost_m, sub_gm=sub_gm,
                ltv3=ltv3, cac=cac, recurring_share=yrs * 12 * sub_m / (price + I("setup_fee") + yrs * 12 * sub_m))


# ----------------------------------------------------------------------------------------------
# Printing helpers (ASCII only)
# ----------------------------------------------------------------------------------------------
def table(headers, rows, align=None):
    cols = len(headers)
    w = [len(str(h)) for h in headers]
    for r in rows:
        for i in range(cols):
            w[i] = max(w[i], len(str(r[i])))
    align = align or (["l"] + ["r"] * (cols - 1))

    def fmt(r):
        out = []
        for i in range(cols):
            s = str(r[i])
            out.append(s.ljust(w[i]) if align[i] == "l" else s.rjust(w[i]))
        return "| " + " | ".join(out) + " |"
    lines = [fmt(headers), "|" + "|".join("-" * (x + 2) for x in w) + "|"]
    lines += [fmt(r) for r in rows]
    print("\n".join(lines))


def usd(x):
    if x is None:
        return "-"
    neg = x < 0
    s = "${:,.0f}".format(abs(x))
    return "-" + s if neg else s


def k(x):
    if x is None:
        return "-"
    return ("-" if x < 0 else "") + "${:,.1f}k".format(abs(x) / 1000.0)


def mo(m):
    return "never" if m is None else "m%d (%s)" % (m, month_label(m))


# ----------------------------------------------------------------------------------------------
# What-must-be-true solver
# ----------------------------------------------------------------------------------------------
def solve_mult(scen, key, target_fn, lo=0.2, hi=6.0, iters=40):
    """Smallest multiplier on `key` such that target_fn(summary) is True (assumes monotone)."""
    if not target_fn(simulate(scen, **{key: hi})):
        return None
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if target_fn(simulate(scen, **{key: mid})):
            hi = mid
        else:
            lo = mid
    return hi


# ----------------------------------------------------------------------------------------------
# Main report
# ----------------------------------------------------------------------------------------------
def _row(lab, s):
    return [lab, usd(s["arr"][18]), usd(s["arr"][36]), usd(s["cum_net"]), "%s at m%d" % (usd(s["cash_low"]), s["cash_low_m"]),
            usd(s["ext_cap"]), mo(s["ft_month"])]


def report():
    print("DD6 -- Private MoE Inference Appliance (DRAM instead of HBM) -- unit-economics model")
    print("As of %s.  DDR5 deck: %s" % (AS_OF, REF_SOURCE))
    print("RDIMM $/user-GB: Q4-26 contract %.2f | glut %.2f | severe %.2f | small-buyer premium x%.2f pre-turn, x%.2f after the 2028 turn"
          % (RDIMM_NOW, RDIMM_GLUT, RDIMM_SEVERE, I("dram_small_buyer_premium"), I("dram_premium_post_turn")))
    print("Months: m1 = %s ... m36 = %s; 2028-Q1 turn = m%d (%s)." % (month_label(1), month_label(36), TURN_MONTH, month_label(TURN_MONTH)))
    print()

    # 0. Red-team revisions
    print("== 0. RED-TEAM REVISIONS (Phase 5): inputs changed, old -> new, objection ids ==")
    rws = []
    for name, (new, why) in REVISIONS.items():
        old = P_PHASE4[name]
        ids = []
        for tok in re.findall(r"RT-[A-Z]+-DD6-\d+(?:/\d+)*", why):
            if tok not in ids:
                ids.append(tok)
        rws.append([name, str(old), str(new), ", ".join(ids)])
    table(["Input", "Phase 4", "Phase 5", "Objection id(s)"], rws, ["l", "r", "r", "l"])
    p4 = {sc: run_with(dict(P_PHASE4), sc) for sc in ("BASE", "GLUT", "SEVERE")}
    rv = {sc: simulate(sc) for sc in ("BASE", "GLUT", "SEVERE")}
    print()
    print("Headline, Phase 4 inputs (reproduced exactly by run_with(P_PHASE4)) vs Phase 5 inputs:")
    hdr = ["Metric", "P4 BASE", "P5 BASE", "P4 GLUT", "P5 GLUT", "P4 SEVERE", "P5 SEVERE"]
    rws = []
    for lab, f in (("ARR m18", lambda r: usd(r["arr"][18])), ("ARR m36", lambda r: usd(r["arr"][36])),
                   ("36-mo net after tax", lambda r: usd(r["cum_net"])), ("Founder full-time", lambda r: mo(r["ft_month"])),
                   ("Salary-incl. breakeven", lambda r: mo(r["sal_be"])), ("Breakeven as run", lambda r: mo(r["breakeven"])),
                   ("First order", lambda r: mo(r["first_cash"])), ("External capital", lambda r: usd(r["ext_cap"])),
                   ("Boxes delivered", lambda r: "%.1f" % r["boxes"])):
        row = [lab]
        for sc in ("BASE", "GLUT", "SEVERE"):
            row += [f(p4[sc]), f(rv[sc])]
        rws.append(row)
    table(hdr, rws)
    print()

    # 1. BOM
    print("== 1. Bill of materials and box price (hardware GM target %.0f%%) ==" % (I("hw_gm") * 100))
    hdr = ["SKU / scenario / month", "DRAM", "GPU", "CPU", "Platform", "BOM", "Box price", "DRAM share"]
    rws = []
    for sku in "LS":
        for scen, m in (("BASE", 1), ("BASE", 27), ("GLUT", 15), ("SEVERE", 15)):
            b = bom(sku, m, scen)
            p = b["total"] / (1 - I("hw_gm"))
            rws.append(["%s %s %s" % (sku, scen, month_label(m)), usd(b["dram"]), usd(b["gpu"]), usd(b["cpu"]),
                        usd(b["platform"]), usd(b["total"]), usd(p), "%.0f%%" % (100 * b["dram"] / b["total"])])
    table(hdr, rws)
    print("Phase-4 price card (elasticity reference, RT-VC-DD6-01): L %s, S %s. Phase 5: L buys %.0f GB (12 + 1 on-site spare"
          % (usd(REF_CARD["L"]), usd(REF_CARD["S"]), I("L_dram_gb")))
    print("RDIMM, RT-PHY-DD6-05); S uses an RTX PRO 5000 Blackwell 48GB at %s via SHI (RT-VET-DD6-03, RT-HYP-DD6-09)." % usd(I("S_gpu")))
    print("A 2-socket L (24 x 32 GB, second CPU + board ~+$6.5k BOM) would quote ~%s (RT-PHY-DD6-02)."
          % usd((bom("L", 1, "BASE")["total"] + 6_500.0) / (1 - I("hw_gm"))))
    print()

    # 2. Performance and capacity
    print("== 2. Performance -> capacity (Phase 5 bandwidth model; ESTIMATES until a socket-pinned Track B run) ==")
    print("step time = t_fix + distinct-expert multiple(c) x routed GB/token / (peak GB/s x efficiency); 10 tok/s/user floor;")
    print("named users = max concurrent / %.2f peak-active share; concurrency also capped by GPU KV memory at %.0fk-token contexts."
          % (I("peak_active_share"), I("design_ctx_tokens") / 1000))
    hdr = ["Configuration", "1-stream", "@2", "@3", "@4", "@8", "max conc", "named users", "KV max @ctx"]
    rws = []
    variants = [
        ("L 1S Kimi-K2.5 INT4, DDR5-6000, eff 0.50 (P5)", "L", {}),
        ("L 1S, eff 0.55", "L", dict(eff=0.55)),
        ("L 1S, DDR5-6400 board (614 GB/s)", "L", dict(bw=614.4)),
        ("L 2S 24x32GB, NUMA-TP, eff 0.45, t_fix 22", "L", dict(bw=1152.0, eff=0.45, tfix=22.0)),
        ("L 1S Inkling 975B-A41B (routed x41/32)", "L", dict(routed=I("L_routed_gb") * 41 / 32)),
        ("L 1S Nemotron 3 Ultra 550B-A55B (x55/32)", "L", dict(routed=I("L_routed_gb") * 55 / 32)),
        ("S 1S MiniMax-M2.x FP8, PRO 5000 48GB (P5)", "S", {}),
        ("S 1S MiniMax-M2.x INT4 experts (unmeasured)", "S", dict(routed=I("S_routed_gb") * 4.5 / 8)),
    ]
    for lab, sku, kw in variants:
        c = capacity_bandwidth(sku, **kw)
        rws.append([lab, "%.1f" % c["single"]] + ["%.1f" % bw_user_tps(sku, n, **kw) for n in (2, 3, 4, 8)]
                   + [c["cstar"], "%.1f" % c["users"], c["kvmax"]])
    table(hdr, rws)
    saved_vram = _OVR.get("S_vram_gb")
    _OVR["S_vram_gb"] = 32.0
    kv5090 = kv_max_users("S")
    if saved_vram is None:
        _OVR.pop("S_vram_gb")
    else:
        _OVR["S_vram_gb"] = saved_vram
    print("Phase-4 S GPU (RTX 5090 32 GB) holds only %d users' KV at %.0fk tokens (RT-PHY-DD6-03)." % (kv5090, I("design_ctx_tokens") / 1000))
    print("Phase-4 fit for reference (conc_exponent %.2f, saturation %.1f measured on a ~845 GB/s Xeon 6 MRDIMM socket):"
          % (I("conc_exponent"), I("conc_saturation")))
    for sku in "LS":
        c = capacity_phase4(sku)
        print("  %s: %.1f tok/s single, %d concurrent, %.0f named users (superseded)" % (sku, c["single"], c["cstar"], c["users"]))
    print("TTFT (idle box): L %.0f s at 2k, %.0f s at 8k, ~%.0f s at 32k, ~%.0f s at 64k (8k prefill rate; queues under load,"
          % (capacity("L")["ttft2k"], capacity("L")["ttft8k"], 32768 / I("L_prefill_8k"), 65536 / I("L_prefill_8k")))
    print("RT-HYP-DD6-05, RT-VC-DD6-11). S %.0f s at 2k, %.0f s at 8k, ~13 s at 32k (P2: 2,540 tok/s at 32k on 2S)."
          % (capacity("S")["ttft2k"], capacity("S")["ttft8k"]))
    print("Mac cluster check (RT-HYP-DD6-03, RT-VC-DD6-09): 2x M3 Ultra ran Kimi K2 Thinking at ~15 tok/s (Hardware Corner snippet);")
    print("4x M3 Ultra 28.3 tok/s, ~2 s TTFT, <500 W (Geerling; Creative Strategies). 2x M5 Ultra 512GB = %s."
          % usd(2 * I("mac512_price")))
    print()

    # 3. Unit economics
    print("== 3. Unit economics per box (founder labor at $%.0f/h shadow rate; 3-year window) ==" % I("shadow_rate"))
    hdr = ["SKU / scenario / month", "Box price", "HW GP", "HW GM", "Sub $/mo", "Sub cost/mo", "Sub GM", "3-yr GP/customer", "CAC", "Recurring share"]
    rws = []
    for sku in "LS":
        for scen, m in (("BASE", 1), ("GLUT", 15), ("SEVERE", 15)):
            u = unit_economics(sku, m, scen)
            rws.append(["%s %s %s" % (sku, scen, month_label(m)), usd(u["price"]), usd(u["hw_gp"]), "%.0f%%" % (100 * u["hw_gm"]),
                        usd(u["sub_m"]), usd(u["sub_cost_m"]), "%.0f%%" % (100 * u["sub_gm"]), usd(u["ltv3"]), usd(u["cac"]),
                        "%.0f%%" % (100 * u["recurring_share"])])
    table(hdr, rws)
    print("CAC = (1/conversion) x %.0f h per qualified conversation x shadow rate + $2,000 marketing allocation." % I("h_per_conversation"))
    print("HW GP is after %.0f%% quote-to-purchase drift, warranty and freight, before partner/VAR fees. L subscription is capped at"
          % (100 * I("quote_drift")))
    print("$%.0f x named users (RT-VET-DD6-01)." % I("sub_user_cap"))
    print()

    # 4. Substitutes per named user
    print("== 4. Cost per named user per month over 36 months vs substitutes (ESTIMATE capacities) ==")
    cL, cS = capacity("L"), capacity("S")
    uL, uS = unit_economics("L", 1, "BASE"), unit_economics("S", 1, "BASE")
    cL55 = capacity_bandwidth("L", eff=0.55)
    subL55 = min(I("sub_L_month"), I("sub_user_cap") * cL55["users"])
    subs = [
        ("This venture L box + subscription", (uL["price"] + I("setup_fee") + 36 * uL["sub_m"]) / (36 * cL["users"]), "%.1f users; 1T at INT4 (eff 0.50)" % cL["users"]),
        ("  same, eff 0.55 (2 concurrent)", (uL["price"] + I("setup_fee") + 36 * subL55) / (36 * cL55["users"]), "%.1f users" % cL55["users"]),
        ("This venture S box + subscription", (uS["price"] + I("setup_fee") + 36 * uS["sub_m"]) / (36 * cS["users"]), "%.0f users; 200-300B MoE" % cS["users"]),
        ("Mac Studio M5 Ultra 512GB (self-run)", I("mac512_price") / (36 * I("mac512_users")), "%.0f users; 1T only ~3-bit; no support" % I("mac512_users")),
        ("2x Mac Studio M5 Ultra RDMA cluster", 2 * I("mac512_price") / (36 * 6.7), "~6.7 users (1 at >=10 tok/s, as L); 1T INT4; ~2 s TTFT"),
        ("NVIDIA DGX Station GB300 (self-run)", I("dgx_station_price") / (36 * I("dgx_station_users")), "%.0f users; no support" % I("dgx_station_users")),
        ("M365 Copilot in GCC High (cloud)", I("copilot_gcch_user_month"), "price [UNVERIFIED]; CUI-eligible"),
        ("Managed private AI (MSP, cloud/colo)", I("managed_private_user_month"), "at 100 users"),
        ("Legal per-seat AI (CoCounsel entry)", I("legal_seat_user_month"), "cloud, $104-639"),
    ]
    table(["Option", "$/user/month", "Basis"], [[a, usd(b), c] for a, b, c in subs], ["l", "r", "l"])
    print()

    # 5. Scenarios
    results = rv
    print("== 5. Scenario summary (36 months from $40k; expected values; Phase 5 inputs) ==")
    hdr = ["Metric", "BASE", "GLUT", "SEVERE"]
    R = results
    rws = [
        ["First order (deposit) month", mo(R["BASE"]["first_cash"]), mo(R["GLUT"]["first_cash"]), mo(R["SEVERE"]["first_cash"])],
        ["Founder full-time from", mo(R["BASE"]["ft_month"]), mo(R["GLUT"]["ft_month"]), mo(R["SEVERE"]["ft_month"])],
        ["Breakeven as run (EBITDA>=0 from here)", mo(R["BASE"]["breakeven"]), mo(R["GLUT"]["breakeven"]), mo(R["SEVERE"]["breakeven"])],
        ["Salary-incl. breakeven (GP-opex>=$10k x3)", mo(R["BASE"]["sal_be"]), mo(R["GLUT"]["sal_be"]), mo(R["SEVERE"]["sal_be"])],
        ["Cash low (pre-draw)", "%s at m%d" % (usd(R["BASE"]["cash_low"]), R["BASE"]["cash_low_m"]),
         "%s at m%d" % (usd(R["GLUT"]["cash_low"]), R["GLUT"]["cash_low_m"]), "%s at m%d" % (usd(R["SEVERE"]["cash_low"]), R["SEVERE"]["cash_low_m"])],
        ["External capital drawn", usd(R["BASE"]["ext_cap"]), usd(R["GLUT"]["ext_cap"]), usd(R["SEVERE"]["ext_cap"])],
        ["Boxes delivered (36 mo)", "%.1f" % R["BASE"]["boxes"], "%.1f" % R["GLUT"]["boxes"], "%.1f" % R["SEVERE"]["boxes"]],
        ["Boxes under subscription m36", "%.1f" % R["BASE"]["fleet36"], "%.1f" % R["GLUT"]["fleet36"], "%.1f" % R["SEVERE"]["fleet36"]],
    ]
    for kk in (12, 18, 24, 36):
        rws.append(["Recurring ARR m%d" % kk, usd(R["BASE"]["arr"][kk]), usd(R["GLUT"]["arr"][kk]), usd(R["SEVERE"]["arr"][kk])])
    rws += [
        ["  of which renewal-tested (delivered <=m24)", usd(R["BASE"]["arr_rt36"]), usd(R["GLUT"]["arr_rt36"]), usd(R["SEVERE"]["arr_rt36"])],
        ["36-mo revenue", usd(R["BASE"]["rev36"]), usd(R["GLUT"]["rev36"]), usd(R["SEVERE"]["rev36"])],
        ["36-mo net after tax", usd(R["BASE"]["cum_net"]), usd(R["GLUT"]["cum_net"]), usd(R["SEVERE"]["cum_net"])],
        ["Tax provisioned", usd(R["BASE"]["tax"]), usd(R["GLUT"]["tax"]), usd(R["SEVERE"]["tax"])],
        ["Founder salary paid", usd(R["BASE"]["salary_paid"]), usd(R["GLUT"]["salary_paid"]), usd(R["SEVERE"]["salary_paid"])],
        ["Cash at m36 (incl. ext. capital)", usd(R["BASE"]["end_cash"]), usd(R["GLUT"]["end_cash"]), usd(R["SEVERE"]["end_cash"])],
        ["  of which customers' money (prepaid subs + deposits)", usd(R["BASE"]["customer_cash"]), usd(R["GLUT"]["customer_cash"]), usd(R["SEVERE"]["customer_cash"])],
        ["Spare-parts inventory held m36", usd(R["BASE"]["spare_inv"]), usd(R["GLUT"]["spare_inv"]), usd(R["SEVERE"]["spare_inv"])],
        ["Unpaid founder hours (part-time months x %.0f h)" % I("founder_hours_pt"), "%.0f" % R["BASE"]["unpaid_hours"], "%.0f" % R["GLUT"]["unpaid_hours"], "%.0f" % R["SEVERE"]["unpaid_hours"]],
        ["Founder economic profit (net - unpaid h x $%.0f)" % I("shadow_rate"), usd(R["BASE"]["econ_profit"]), usd(R["GLUT"]["econ_profit"]), usd(R["SEVERE"]["econ_profit"])],
        ["Subscription share of labor-valued GP, m13-m24", "%.0f%%" % (100 * (R["BASE"]["sub_gp_share_y2"] or 0)), "%.0f%%" % (100 * (R["GLUT"]["sub_gp_share_y2"] or 0)), "%.0f%%" % (100 * (R["SEVERE"]["sub_gp_share_y2"] or 0))],
    ]
    table(hdr, rws)
    rb = R["BASE"]["rows"]
    first = R["BASE"]["first_cash"]
    lead = "L" if I("mix_L") >= 0.5 else "S"
    pre = rb[first - 2]["cash"] if first and first >= 2 else I("founder_capital")
    gap = bom(lead, first or 1, "BASE")["total"] * (1 + I("quote_drift")) - hw_price(lead, first or 1, "BASE", I("hw_gm")) * I("deposit_pct")
    print("Lumpiness check (expected values hide whole boxes): cash before the first order is %s; one whole %s order"
          % (usd(pre), lead))
    print("needs %s of parts working capital beyond its 50%% deposit -> cash %s; two in one month -> %s."
          % (usd(gap), usd(pre - gap), usd(pre - 2 * gap)))
    print("The ESP set-up ($8k at m9) lands before the first order (m%s), so BASE draws a $25k tranche at m9: the bridge is"
          % (first if first else "-"))
    print("no longer optional.")
    print()

    # 6. Monthly P&L
    for scen in ("BASE", "GLUT", "SEVERE"):
        rr = results[scen]["rows"]
        print("== 6%s. Monthly P&L and cash -- %s ==" % ({"BASE": "a", "GLUT": "b", "SEVERE": "c"}[scen], scen))
        hdr = ["m", "Month", "FT", "Conv", "Orders", "Deliv", "Fleet", "HW rev", "Sub rev", "Setup", "GP", "Opex+sal", "EBITDA", "Tax", "Cash", "Drawn", "ARR", "Contr h"]
        rws = []
        for r in rr:
            if scen != "BASE" and r["m"] % 3 != 0:
                continue
            rws.append([r["m"], r["label"], "Y" if r["ft"] else "-", "%.1f" % r["conv"], "%.2f" % r["orders"], "%.2f" % r["deliv"],
                        "%.1f" % r["fleet"], k(r["hw_rev"]), k(r["sub_rev"]), k(r["setup_rev"]), k(r["gp"]),
                        k(r["opex"] + r["salary"]), k(r["ebitda"]), k(r["tax"]), k(r["cash"]), k(r["drawn"]), k(r["arr"]),
                        "%.0f" % r["contractor_h"]])
        table(hdr, rws)
        if scen != "BASE":
            print("(quarter-end months shown; every month is simulated)")
        print()

    # 7. Sensitivity
    print("== 7. Sensitivity (BASE, Phase 5 inputs; one lever at a time unless stated) ==")
    print("price = hardware GM target, subscription and setup prices x(1+/-0.3), now with demand response (elast_up %.1f);"
          % I("elast_up"))
    print("COGS = BOM and subscription costs x(1+/-0.3) with prices fixed at the quote (a spike after quoting).")
    hdr = ["Lever", "ARR m18", "ARR m36", "36-mo net", "Cash low", "Ext. capital", "Full-time"]
    rws = [_row("BASE (Phase 5)", results["BASE"]), _row("Phase 4 inputs reproduced", p4["BASE"])]
    for lab, kw in (("price -30%", dict(price_mult=0.7)), ("price +30%", dict(price_mult=1.3)),
                    ("conversion -30%", dict(conv_mult=0.7)), ("conversion +30%", dict(conv_mult=1.3)),
                    ("churn -30%", dict(churn_mult=0.7)), ("churn +30%", dict(churn_mult=1.3)),
                    ("COGS -30%", dict(cogs_mult=0.7)), ("COGS +30%", dict(cogs_mult=1.3)),
                    ("all three adverse (conv/churn/price)", dict(conv_mult=0.7, churn_mult=1.3, price_mult=0.7))):
        rws.append(_row(lab, simulate("BASE", **kw)))
    for lab, ov, sc in (
            ("KILL-TEST PASS: conv 0.08, cycle 6, channel 3/mo", {"conversion": 0.08, "sales_cycle_m": 6.0, "channel_conv_month": 3.0}, "BASE"),
            ("  same + L re-admitted (mix 0.25, eff 0.55)", {"conversion": 0.08, "sales_cycle_m": 6.0, "channel_conv_month": 3.0, "mix_L": 0.25, "bw_eff": 0.55}, "BASE"),
            ("L re-admitted alone (mix 0.25, eff 0.55)", {"mix_L": 0.25, "bw_eff": 0.55}, "BASE"),
            ("conversion 0.08 (Phase 4)", {"conversion": 0.08}, "BASE"),
            ("conversion 0.12", {"conversion": 0.12}, "BASE"),
            ("sales cycle 4 (Phase 4)", {"sales_cycle_m": 4.0}, "BASE"),
            ("sales cycle 9", {"sales_cycle_m": 9.0}, "BASE"),
            ("DRAM premium 1.15 (Phase 4, $29.65/GB)", {"dram_small_buyer_premium": 1.15}, "BASE"),
            ("DRAM premium 2.0 (Fusion ~$52/GB)", {"dram_small_buyer_premium": 2.0}, "BASE"),
            ("elast_up 0 (no response to price rises)", {"elast_up": 0.0}, "BASE"),
            ("elast_up 1.0", {"elast_up": 1.0}, "BASE"),
            ("no MSP/RPO channel", {"channel_conv_month": 0.0}, "BASE"),
            ("founder 55 h/month", {"founder_hours_pt": 55.0}, "BASE"),
            ("founder 45 h/month", {"founder_hours_pt": 45.0}, "BASE"),
            ("no backup retainer", {"oncall_month": 0.0}, "BASE"),
            ("24/7 on-call retainer $2.5k/mo", {"oncall_month": 2_500.0}, "BASE"),
            ("subscription price x2 ($1,300 S)", {"sub_S_month": 1_300.0, "sub_L_month": 2_500.0}, "BASE"),
            ("deposit 70%", {"deposit_pct": 0.70}, "BASE"),
            ("GLUT with glut elasticity 1.0", {"glut_elasticity": 1.0}, "GLUT")):
        rws.append(_row(lab, run_with(ov, sc)))
    table(hdr, rws)
    print()

    # 8. What must be true
    print("== 8. What must be true (Phase 5 inputs) ==")
    m1 = solve_mult("BASE", "conv_mult", lambda r: r["arr"][36] >= 1_000_000)
    m2 = solve_mult("BASE", "conv_mult", lambda r: r["ft_month"] is not None and r["ft_month"] <= 36)
    m2b = solve_mult("BASE", "conv_mult", lambda r: r["ft_month"] is not None and r["ft_month"] <= 30)
    m5 = solve_mult("BASE", "conv_mult", lambda r: r["cum_net"] >= 0)
    m4 = solve_mult("BASE", "sub_price_mult", lambda r: r["ft_month"] is not None and r["ft_month"] <= 36)
    print("Conversion needed for founder full-time by m36: %s"
          % ("x%.2f = %.1f%% of qualified conversations" % (m2, 100 * m2 * I("conversion")) if m2 else "not reachable at <=6x"))
    print("Conversion needed for founder full-time by m30: %s"
          % ("x%.2f = %.1f%%" % (m2b, 100 * m2b * I("conversion")) if m2b else "not reachable at <=6x"))
    print("Conversion needed for a non-negative 36-month net: %s"
          % ("x%.2f = %.1f%%" % (m5, 100 * m5 * I("conversion")) if m5 else "not reachable at <=6x"))
    print("Conversion needed for $1M recurring ARR at m36: %s"
          % ("x%.2f = %.1f%%" % (m1, 100 * m1 * I("conversion")) if m1 else "not reachable at <=6x"))
    print("Price multiple (HW GM, subscription, setup; with demand response) needed for full-time by m36: %s"
          % ("x%.2f" % m4 if m4 else "not reachable at <=6x"))
    ext = simulate("BASE", months=60)
    print("Ceiling check (BASE run on to m60, same funnel): recurring ARR m48 %s, m60 %s; full-time %s; 60-month net %s."
          % (usd(ext["arr"][48]), usd(ext["arr"][60]), mo(ext["ft_month"]), usd(ext["cum_net"])))
    b = results["BASE"]
    print()
    print("WHAT MUST BE TRUE (Phase 5): ~%.0f%% of qualified regulated buyers must buy a ~$%sk S box (priced %.0f%% above the"
          % (100 * I("conversion"), int(unit_economics("S", 1, "BASE")["price"] / 1000), 100 * (hw_price("S", 1, "BASE", I("hw_gm")) / REF_CARD["S"] - 1)))
    print("Phase-4 card) within ~%d months of a demo, keep paying $%.0f/month (churn <=%.0f%%/yr), and the founder must still"
          % (int(I("sales_cycle_m")), I("sub_S_month"), 100 * I("sub_churn_annual")))
    print("source ~%.0f conversations a month while delivering. Then BASE reaches %s ARR at m36 (%s at m18), never pays the"
          % (I("conv_target_pt"), usd(b["arr"][36]), usd(b["arr"][18])))
    print("founder a salary, and nets %s over 36 months. Full-time by m36 needs a %.0f%% close rate."
          % (usd(b["cum_net"]), 100 * (m2 or 0) * I("conversion")))
    return results


def main():
    buf = io.StringIO()
    with redirect_stdout(buf):
        report()
    out = buf.getvalue()
    sys.stdout.write(out)
    try:
        OUT_MD.parent.mkdir(parents=True, exist_ok=True)
        OUT_MD.write_text(
            "# DD6 -- Private MoE Inference Appliance: model output\n\n"
            "Generated by `python3 models/private-moe-appliance.py` (agent p4-private-moe-appliance, %s; Phase 5 red-team revisions by p5r-private-moe-appliance). "
            "Inputs and sources: the INPUTS block and the RED-TEAM REVISIONS (Phase 5) block in the model; notes: `research/phase4/private-moe-appliance_notes.md`; responses: `research/phase5/responses_private-moe-appliance.json`.\n\n"
            "```\n%s```\n" % (AS_OF, out))
    except OSError as exc:  # pragma: no cover
        sys.stderr.write("could not write %s: %r\n" % (OUT_MD, exc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
