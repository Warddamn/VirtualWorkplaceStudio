#!/usr/bin/env python3
"""DD3 - Drop-in Non-Volatile Continuity Modules (anchor C-12, folded C-16).

Unit economics and 36-month monthly P&L for a part-time founder with $40k.
PHASE 5 RED TEAM: inputs revised in the "RED-TEAM REVISIONS (Phase 5)" block below (25 objections from
research/phase5/rt_*.json; responses in research/phase5/responses_nv-continuity-modules.json).
`python3 models/nv-continuity-modules.py --phase4` reproduces the Phase 4 output exactly.
Pure Python 3 stdlib. Run from the repo root:  python3 models/nv-continuity-modules.py

Product lines
  L1 NV-CARD : battery-free PC Card (PCMCIA/JEIDA Type I) "SRAM card" built on Everspin
               MR4A16B 16Mb Toggle MRAM (true async-SRAM timing, U.S.-fabbed Toggle),
               5V-tolerant bus buffers, BVD1/BVD2 strapped "battery good".
               SKUs: 2MB (1 chip) and 4MB (2 chips). Buyers: legacy Fanuc CNC (0/15/16/18/20/21,
               i-series SRAM backup), Fanuc RJ-2/RJ-3 robots, Mitsubishi MELSEC-Q (Q2MEM-xMBS).
  L2 NV-DIP  : battery-free DIP drop-ins for Dallas/Maxim DS1225/DS1230 (FM18W08 F-RAM, 5V)
               and DS1245 (FM28V100 + 5V-tolerant translators). Buyers: industrial controls,
               T&M repair (HP 3458A), arcade/pinball, DMSMS.
  L3 CLOUD   : per-shop subscription (backup-image vault, restore utility, battery-due tracker).
  L4 LTSA    : long-term supply agreement / DMSMS blanket order for a screened, traceable drop-in.
  L5 PLP     : (C-16) MRAM power-loss-protection reference design + design-in services.
               Evaluated as a gated OPTION with expected value, not in the core P&L.

Market scenarios (DRAM price path from models/dram_cost_stack.py ddr5_reference()):
  BASE   : 2026-27 contract prices hold; mild turn in 2028 (-10% over 2028).
  GLUT   : DDR5 -60% from 2028-Q1 (A-05) -> $8.15/GB.
  SEVERE : DDR5 at $2.04/GB from 2028-Q1.
The core lines are priced against batteries and obsolete NVSRAM, not DRAM, so DRAM enters
only through (i) the computed PLP economics and (ii) explicit ESTIMATE multipliers for a
correlated industrial slowdown, component softening and copycat pressure.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CANON = dict(
    cost_component_usd_per_gb=1.48,
    contract_component_usd_per_gb_q4_2026=20.37,
    glut_component_usd_per_gb=8.15,
    severe_glut_component_usd_per_gb=2.04,
    contract_rdimm64_usd_per_user_gb_q4_2026=25.8,
    glut_rdimm64_usd_per_user_gb=10.3,
)
try:
    from dram_cost_stack import ddr5_reference  # noqa: E402
    REF = ddr5_reference()
    REF_SRC = "models/dram_cost_stack.py ddr5_reference() (as_of %s)" % REF.get("as_of", "?")
except Exception as exc:  # pragma: no cover - fallback path
    REF = dict(CANON)
    REF_SRC = "canonical fallback numbers (import failed: %s)" % exc.__class__.__name__


def I(v, src):
    return {"v": v, "src": src}


# ----------------------------------------------------------------------------------------------
# INPUTS - every value carries a source URL or "ESTIMATE: basis"
# ----------------------------------------------------------------------------------------------
INPUTS = {
    # --- founder, timing ---
    "start_cash": I(40000, "ASSUMPTIONS.md A-03 ($40k deployable)"),
    "months": I(36, "MISSION_PROMPT.md founder profile (36-month ceiling)"),
    "founder_salary_monthly_fulltime": I(10000, "ASSUMPTIONS.md A-03 (~$120k/yr loaded)"),
    "fulltime_trigger_op_profit_monthly": I(12000, "ESTIMATE: go full-time only when trailing-3-mo operating profit covers salary + 20% buffer"),
    # --- DRAM reference (imported) ---
    "dram_contract_q4_2026_usd_gb": I(REF["contract_component_usd_per_gb_q4_2026"], REF_SRC),
    "dram_glut_usd_gb": I(REF["glut_component_usd_per_gb"], REF_SRC),
    "dram_severe_usd_gb": I(REF["severe_glut_component_usd_per_gb"], REF_SRC),
    "dram_base_2028_decline": I(0.10, "https://www.tmgm.com/en/analysis/market-insight/micron-dram-supply-tightening (BofA -10% ASP 2028, via 01_LANDSCAPE 1-4b)"),
    # --- component prices ---
    "mr4a16b_usd_qty1": I(46.03, "https://www.digikey.com/en/products/detail/everspin-technologies-inc/MR4A16BYS35/4021237"),
    "mr4a16b_usd_qty1000": I(37.67, "https://www.futureelectronics.com/p/memory--RAM--nvram/mr4a16bcys35r-everspin-technologies-6114651"),
    "mr4a16b_usd_our_qty": I(42.00, "ESTIMATE: 100-500 pcs/yr sits between $37.67 @1k (Future) and $46.03 qty1 (DigiKey)"),
    "mr4a16b_lead_weeks": I(26, "https://www.futureelectronics.com/p/memory--RAM--nvram/mr4a16bcys35r-everspin-technologies-6114651 (20-26 wk)"),
    "fm18w08_usd_qty1": I(12.87, "https://azcus.digikey.com/en/products/detail/infineon-technologies/FM18W08-SG/4090358"),
    "fm18w08_usd_our_qty": I(11.50, "ESTIMATE: ~10% below DigiKey qty-1 $12.87 at 100-pc breaks"),
    "fm28v100_usd_our_qty": I(19.00, "https://www.futureelectronics.com/p/semiconductors--memory--RAM--nvram--fram-mram/fm28v100-tg-infineon-6750863 ($19.38 @2); findchips $17.7-25.9"),
    "mram_1gb_stt_usd": I(102.60, "https://www.lcsc.com/product-image/C20342497.html ($102.60 @500, ~$821/GB)"),
    # --- L1 NV-CARD BOM (per card) ---
    "card_frame_kit_connector_usd": I(12.00, "ESTIMATE: no small-qty price found; ITT StarCard kits exist (https://www.designnews.com/motion-control/itt-interconnect-solutions-snap-on-and-ultrasonic-pcmcia-i-o-card-kits); one 68-pos connector is Last Time Buy"),
    "card_pcb_2mb_usd": I(4.50, "ESTIMATE: 0.8mm 4-layer, 100-pc offshore fab"),
    "card_pcb_4mb_usd": I(5.50, "ESTIMATE: as above, larger"),
    "card_logic_2mb_usd": I(5.00, "ESTIMATE: 3x 74LVC16245-class 5V-tolerant buffers + supervisor + attribute EEPROM + passives"),
    "card_logic_4mb_usd": I(6.00, "ESTIMATE: as above + decode"),
    "card_assembly_usd": I(14.00, "ESTIMATE: U.S. EMS at 100-pc lots; anecdote $415-1,300 per 10 turnkey boards (https://community.sparkfun.com/t/pcb-assembly-service/27265)"),
    "card_assembly_4mb_usd": I(16.00, "ESTIMATE: +1 BGA/TSOP placement"),
    "card_setup_amort_usd": I(4.00, "ESTIMATE: ~$400 stencil/setup per 100-card lot (Screaming Circuits best at 25+: https://pic.hallikainen.org/piclist/2008/a/01/29/165504a.txt)"),
    "card_test_pack_usd": I(4.00, "ESTIMATE: functional test on fixture, label, ESD bag, CoC"),
    "card_shield_usd": I(0.0, "Phase 4: no magnetic shield (neutral default; see RED-TEAM REVISIONS)"),
    # --- L1 prices ---
    "card2_price_direct": I(249.0, "ESTIMATE anchored on Synchrotech 2MB battery card $239.39 (https://www.cdwg.com/product/synchrotech-sram-pcmcia-memory-pc-cards-replaceable-battery-flash-memory/5006798); used 2MB $160-440 eBay; Q2MEM-2MBSN $403.81 (https://www.ebay.de/itm/406086802130)"),
    "card4_price_direct": I(349.0, "ESTIMATE: +$100 for second MRAM die; Memex lists 4MB unavailable (https://memex.ca/?p=596)"),
    "card_reseller_discount": I(0.30, "ESTIMATE: MRO reseller margin 30% (Memex/MRO Electric/DoSupply class)"),
    "card_mix_4mb": I(0.25, "ESTIMATE: Fanuc formats to 4MB max per Memex; most backup jobs fit 1-2MB"),
    # --- L2 NV-DIP BOM and prices ---
    "dip256_cogs_parts_other_usd": I(1.50 + 2.50, "ESTIMATE: PCB $1.50 + machined round pins $2.50 (square pins damage sockets per https://www.pcbway.com/project/shareproject/Dallas_DS1230Y_DS1235YW_NVRAM_FRAM_Replacement_Adapter_79f70ace.html)"),
    "dip256_assembly_test_usd": I(4.00 + 1.50 + 2.00, "ESTIMATE: assembly $4 + setup $1.50 + test/pack $2"),
    "dip1m_cogs_parts_other_usd": I(2.50 + 2.00 + 3.00, "ESTIMATE: 5V-tolerant translators $2.50 + PCB $2 + pins $3"),
    "dip1m_assembly_test_usd": I(5.00 + 1.50 + 2.00, "ESTIMATE: assembly $5 + setup $1.50 + test/pack $2"),
    "dip256_price_direct": I(34.0, "ESTIMATE vs DS1230Y-85 new $35-44 qty1 (https://findchips.com/search/DS1230Y-85?f=dsa) and Glitch Works battery DS1225 drop-in ~$30 (https://tindie.com/products/glitchwrks/glitch-works-gw-1225-1-dallas-ds1225-replacement)"),
    "dip1m_price_direct": I(59.0, "ESTIMATE: DS1245 obsolete/NRND, broker-only (https://www.digipart.com/part/DS1245Y-85); no price found"),
    "dip_reseller_discount": I(0.20, "ESTIMATE: component reseller margin"),
    "dip_mix_1m": I(0.30, "ESTIMATE"),
    # --- channel costs ---
    "ebay_fee_pct": I(0.136, "ESTIMATE: eBay final value fee ~13.6% most categories (not re-verified 2026)"),
    "ebay_fee_fixed": I(0.40, "ESTIMATE: per-order fixed fee"),
    "store_payment_pct": I(0.029, "ESTIMATE: card processing 2.9%"),
    "store_payment_fixed": I(0.30, "ESTIMATE"),
    "cac_store_card_order": I(30.0, "ESTIMATE: niche search terms ('fanuc sram card', 'Q2MEM-2MBS'); ~$1.5 CPC / 5% conv"),
    "cac_store_dip_order": I(6.0, "ESTIMATE: mostly organic (forums, part-number search)"),
    "ship_cost_card": I(9.0, "ESTIMATE: free USPS Priority on direct card orders"),
    "ship_cost_dip": I(5.0, "ESTIMATE: free First-Class on direct DIP orders"),
    "warranty_returns_pct": I(0.03, "ESTIMATE: 3% of revenue (compatibility returns)"),
    "card_channel_mix": I({"ebay": 0.25, "store": 0.35, "reseller": 0.40}, "ESTIMATE: resellers matter because the buyer is a maintenance tech searching MRO catalogs"),
    "dip_channel_mix": I({"ebay": 0.40, "store": 0.40, "reseller": 0.20}, "ESTIMATE"),
    # --- volumes (BASE) ---
    "card_launch_month": I(9, "ESTIMATE: design m1-3, proto/validate m4-6, MRAM lead 20-26 wk ordered m3"),
    "card_ramp_months": I(12, "ESTIMATE"),
    "card_demand_decay_yr": I(0.0, "Phase 4: demand held flat after ramp (neutral default; see RED-TEAM REVISIONS)"),
    "card_units_steady_month": I(40, "ESTIMATE: ~5% of est. global ~10k/yr PC-card SRAM replacement demand (see TAM block)"),
    "dip_launch_month": I(4, "ESTIMATE: FM18W08 in stock (~775 at DigiKey), 8-wk standard lead"),
    "dip_ramp_months": I(9, "ESTIMATE"),
    "dip_units_steady_month": I(50, "ESTIMATE: free open adapters cap the hobby segment; sells on test report + warranty"),
    # --- L3 cloud ---
    "cloud_launch_month": I(15, "ESTIMATE: after cards are in the field"),
    "cloud_price_month": I(29.0, "ESTIMATE: per shop; below DNC/MDC suites"),
    "cloud_attach_rate": I(0.06, "ESTIMATE: 6% of direct card buyers subscribe"),
    "cloud_churn_month": I(0.025, "ESTIMATE: SMB tool churn"),
    "cloud_cogs_month": I(3.0, "ESTIMATE: hosting + support per sub"),
    # --- L4 LTSA / DMSMS ---
    "ltsa_contracts": I([(27, 2000.0), (33, 2000.0)], "ESTIMATE: two $24k/yr blanket orders (start month, $/month); DLA buys 5962 memory by NSN via DIBBS (https://www.highergov.com/nsn/5962012622185/)"),
    "ltsa_gm": I(0.50, "ESTIMATE: screened, traceable lots with CoC"),
    # --- fixed opex, one-time ---
    "opex_tools_month": I(75.0, "ESTIMATE: domain, Shopify-class store, email"),
    "opex_from_launch_month": I(225.0, "ESTIMATE: product liability insurance ~$125 + bookkeeping ~$100"),
    "opex_marketing_dip": I(300.0, "ESTIMATE: ads + samples from DIP launch"),
    "opex_marketing_card": I(300.0, "ESTIMATE: extra ads + trade-forum presence from card launch"),
    "opex_support_retainer": I(0.0, "Phase 4: no paid CNC-service support (neutral default; see RED-TEAM REVISIONS)"),
    "one_time": I({1: 800.0, 2: 1500.0 + 3000.0, 3: 3000.0, 4: 3000.0 + 2500.0, 5: 1500.0},
                  "ESTIMATE: m1 LLC/legal $800; m2 DIP designs $1.5k + card design 1/3; m3 card design 2/3; m4 card design 3/3 + used Fanuc 16i/18i control + Mitsubishi Q CPU + PC-card reader $2.5k; m5 prototype run $1.5k"),
    "inventory_cover_months": I(3, "ESTIMATE: 26-week MRAM lead time forces >= 3 months of stock"),
    "first_lot_cards": I(100, "ESTIMATE: minimum economic EMS lot"),
    "first_lot_dip": I(200, "ESTIMATE"),
    "ltb_connector_sets": I(0, "Phase 4: no connector/frame lifetime buy (neutral default; see RED-TEAM REVISIONS)"),
    "ltb_month": I(0, "Phase 4: n/a"),
    # --- scenario multipliers on the core ---
    "scn_demand_mult": I({"BASE": 1.00, "GLUT": 0.95, "SEVERE": 0.85}, "ESTIMATE: glut correlates with AI/industrial capex slowdown; legacy-MRO demand partly counter-cyclical"),
    "scn_price_mult": I({"BASE": 1.00, "GLUT": 1.00, "SEVERE": 0.90}, "ESTIMATE: SEVERE adds copycat (Shenzhen) price pressure"),
    "scn_cogs_mult": I({"BASE": 1.00, "GLUT": 0.95, "SEVERE": 0.90}, "ESTIMATE: specialty NVM softens a little in a memory downturn"),
    # --- TAM ---
    "fanuc_cnc_cumulative": I(5_000_000, "https://metalworkingnews.info/fanuc-reaches-cnc-production-milestone-of-5-million/ (Feb-2022)"),
    "us_share_installed": I(0.15, "ESTIMATE: U.S. share of Fanuc installed base"),
    "legacy_share": I(0.35, "ESTIMATE: share of Fanuc base on SRAM-card-era controls (0/15/16/18/20/21, i-A)"),
    "legacy_still_running": I(0.50, "ESTIMATE"),
    "machines_per_shop": I(8, "ESTIMATE; >20,000 U.S. job shops (https://www.mmsonline.com/blog/post/capital-spending-survey-projects-5-decline-in-machine-tool-buying-for-2020-but-spending-level-still-above-average)"),
    "card_replacement_years": I(8, "ESTIMATE: battery card life; Memex states >=10-yr rechargeable cell"),
    "other_families_mult": I(1.5, "ESTIMATE: +Mitsubishi Q2MEM, Fanuc robots, Okuma/other, avionics/T&M/synth"),
    "global_over_us_mult": I(4.0, "ESTIMATE"),
    "iseries_share": I(0.0, "Phase 4: i-A folded into legacy_share (neutral default; see RED-TEAM REVISIONS)"),
    "iseries_still_running": I(0.60, "ESTIMATE: i-series controls are younger (1996-2008) than pre-i"),
    "iseries_card_need": I(0.0, "Phase 4: n/a (neutral default)"),
    "sam_over_us_mult": I(4.0, "Phase 4 treated the global market as addressable (SAM = U.S. x 4.0)"),
    "sam_intl_reach": I(0.0, "Phase 4: n/a (neutral default)"),
    # --- C-16 PLP option ---
    "plp_ee_contract_usd": I(45000.0, "card C-16: contract EE ~$30-60k year 1"),
    "plp_eval_boards_usd": I(5000.0, "ESTIMATE"),
    "plp_designin_fee_usd": I(40000.0, "ESTIMATE: package + integration services per OEM design-in"),
    "plp_services_gm": I(0.40, "card C-16 verify_corrections: services ~40% GM years 1-3"),
    "plp_p_designin_by_m36_base": I(0.35, "ESTIMATE: controller vendors/IBM gate PLP; Swissbit PowerSafe, Apacer CorePower own PLP (https://www.electronicsforu.com/news/new-products/swissbit-introduces-powersafe-a-power-loss-protection-system-for-industrial-ssds)"),
    "plp_dram_cache_gb_replaced": I(2.0, "ESTIMATE: DRAM-less design replaces 2GB cache"),
    "plp_mram_mb": I(512, "ESTIMATE: 4x 1Gb STT journal"),
    "plp_supercap_bom_usd": I(12.0, "ESTIMATE: 2-15 tantalum-polymer caps per drive (https://jisaku.com/glossary/storage-ssd-power-loss-protection-tantalum-cap, unverified)"),
    "itc_target_date": I("2027-08-16", "https://www.usitc.gov/sites/default/files/secretary/fed_reg_notices/337/337_1487_notice08262026sgl.pdf"),
}
PHASE4_V = {k: d["v"] for k, d in INPUTS.items()}  # exact Phase 4 inputs, kept for comparison / --phase4

# ==============================================================================================
# RED-TEAM REVISIONS (Phase 5) - agent p5r-nv-continuity-modules, 2026-11-01
# Four adversarial reviewers (VET, VC, HYP, PHY; research/phase5/rt_*.json) attacked DD3.
# Every accepted objection that changes an input is listed here: key, new value, objection id(s),
# basis. The old (Phase 4) value is read from INPUTS above and printed in section [0].
# Run with --phase4 to reproduce the Phase 4 output exactly.
# ==============================================================================================
RT_REVISIONS = [
    # --- market: i-series accepts CF for boot-menu SRAM backup; real need is pre-i ---
    ("legacy_share", 0.15, "RT-VET-DD3-01, RT-VC-DD3-02, RT-HYP-DD3-01",
     "pre-i controls only (16/18-A/B/C, 15, 20/21-B, RJ-2); i-series moved to iseries_* rows; VET estimate ~0.15"),
    ("legacy_still_running", 0.40, "RT-VET-DD3-01, RT-HYP-DD3-02",
     "pre-i controls are 26-38 years old; the 0.50 blend assumed younger i-A units"),
    ("iseries_share", 0.20, "RT-HYP-DD3-01, RT-VC-DD3-02",
     "ESTIMATE: i-A / early i-B / 0i-A/B share of cumulative Fanuc units"),
    ("iseries_card_need", 0.20, "RT-HYP-DD3-01, RT-VET-DD3-01",
     "ESTIMATE: residual SRAM-card need on i-series (normal-mode I/O on 18i-T; CF format NMI on a 16iA, CNCzone 421202); boot backup works on CF"),
    ("other_families_mult", 1.35, "RT-VET-DD3-06",
     "Mitsubishi FA-A-0184 points High-speed Universal QCPU users to SD; SRAM card only for QnH/QnUD file registers"),
    ("global_over_us_mult", 1 / 0.15, "RT-VC-DD3-03",
     "internal consistency: a 15% U.S. share implies global = 6.7x U.S. (information only, not addressable)"),
    ("sam_over_us_mult", 1.10, "RT-VC-DD3-03",
     "core addressable = U.S. + Canada: every named channel is North American"),
    ("sam_intl_reach", 0.15, "RT-VC-DD3-03",
     "partial counter: a plain memory card is very likely EAR99 [ESTIMATE, unconfirmed], so eBay/web can reach ~15% of non-U.S. demand"),
    # --- volume: 40/mo was 16% of (old) U.S. demand and ~36% of revised; product depletes its own market ---
    ("card_units_steady_month", 16, "RT-HYP-DD3-02, RT-VC-DD3-03, RT-VET-DD3-01",
     "~13% of revised North-American SAM (see [3]); a new entrant's share, to be re-set by track A deposits"),
    ("card_demand_decay_yr", 0.10, "RT-HYP-DD3-02, RT-VC-DD3-03",
     "ESTIMATE: ~6%/yr pre-i retirement + ~4%/yr self-depletion (each battery-free card removes an 8-yr replacement)"),
    # --- DIP line: F-RAM /CE-latch trap and cycle time; killed as a leg ---
    ("dip_units_steady_month", 0, "RT-VET-DD3-03, RT-PHY-DD3-02, RT-PHY-DD3-03",
     "DIP leg killed: FM18W08/FM28V100 latch address on /CE fall (130 ns cycle); originals DS1230Y/DS1245Y still in ADI production"),
    ("first_lot_dip", 0, "RT-VET-DD3-03", "no DIP inventory"),
    ("opex_marketing_dip", 150.0, "RT-VET-DD3-03",
     "DIP ads dropped; $150/mo pre-launch card-deposit marketing kept from m4"),
    # --- card hardware: dual-supply translators, byte steering, power-fail gating, shield, connector ---
    ("card_logic_2mb_usd", 9.00, "RT-PHY-DD3-04, RT-PHY-DD3-05",
     "ESTIMATE: 74LVC16T245-class dual-supply translators + mandatory small CPLD (8-bit byte-lane steering, REG#/attribute decode, E/W gating) + supervisor + hold-up cap"),
    ("card_logic_4mb_usd", 10.00, "RT-PHY-DD3-04, RT-PHY-DD3-05", "as above + chip-select decode"),
    ("card_shield_usd", 3.00, "RT-PHY-DD3-01, RT-VET-DD3-02, RT-HYP-DD3-06",
     "ESTIMATE: Ni-Fe/mu-metal foil over the MRAM inside the Type I envelope (or ferritic-steel cover); MR4A16B Hmax_write 8,000 A/m"),
    ("card_frame_kit_connector_usd", 15.00, "RT-HYP-DD3-03, RT-VET-DD3-04",
     "ESTIMATE: no current-production card-side quote found (Hirose IC1K LTB; FCI 90937 obsolete; TE assemblies status unknown); broker/LTB premium"),
    ("ltb_connector_sets", 350, "RT-HYP-DD3-03, RT-VET-DD3-04",
     "funded lifetime buy = modeled BASE card need m11-m36 (288) x 1.2, rounded (see [0b])"),
    ("ltb_month", 9, "RT-HYP-DD3-03, RT-VET-DD3-04", "bought with the first EMS lot"),
    # --- quality, returns, support, insurance ---
    ("warranty_returns_pct", 0.06, "RT-VC-DD3-06, RT-VET-DD3-05, RT-PHY-DD3-06",
     "ESTIMATE: dozens of firmware/option combinations; validation on 3 families, not all; magnet-exposure claims"),
    ("opex_from_launch_month", 350.0, "RT-HYP-DD3-05",
     "product liability $1-2M COI ~$250/mo [ESTIMATE] + bookkeeping $100"),
    ("opex_support_retainer", 150.0, "RT-VC-DD3-06",
     "ESTIMATE: retainer for a CNC field-service technician who handles 'won't format on my 18-B' tickets"),
    ("card_launch_month", 11, "RT-VET-DD3-05, RT-PHY-DD3-06, RT-PHY-DD3-04",
     "pre-i bench + 3-family validation + outside-lab ESD/temp/insertion + rev-B respin before the first 100-card lot"),
    ("one_time", {1: 800.0 + 300.0, 2: 3000.0, 3: 3000.0, 4: 3000.0 + 2500.0, 5: 1500.0,
                  6: 3000.0, 7: 1500.0, 8: 7500.0 + 1500.0},
     "RT-VET-DD3-03, RT-VET-DD3-05, RT-PHY-DD3-06, RT-HYP-DD3-05, RT-PHY-DD3-01",
     "m1 +$300 gaussmeter/test magnets; m2 DIP design $1.5k removed; m4 control budget now buys a pre-i 16-C/18-C/21-B; "
     "m6 +$3k bench time on 2 more families/firmware revs; m7 +$1.5k QMS manual + RMA process; m8 +$7.5k outside-lab "
     "ESD (IEC 61000-4-2), 0-55C, insertion life + $1.5k rev-B respin"),
    # --- recurring line: DMSMS LTSAs nobody found move to the upside case ---
    ("ltsa_contracts", [], "RT-VC-DD3-04",
     "no DLA/NSN demand for DS12xx or PC Card SRAM found (Phase 4 and Phase 5 searches); LTSAs kept only in scale path S2/S4"),
    # --- C-16 PLP option: hold-up energy still needed without an FTL the founder does not own ---
    ("plp_supercap_bom_usd", 4.0, "RT-PHY-DD3-07",
     "ESTIMATE: only ~1/3 of the $12 hold-up BOM is removable; paired-page protection still needs hold-up or an FTL change"),
]
RT_LOG = []
for _key, _new, _ids, _basis in RT_REVISIONS:
    _old = INPUTS[_key]["v"]
    INPUTS[_key] = {"v": _new, "src": "RED-TEAM (Phase 5) %s: was %r. %s. [Phase 4 src: %s]"
                    % (_ids, _old, _basis, INPUTS[_key]["src"])}
    RT_LOG.append((_key, _old, _new, _ids, _basis))
if "--phase4" in sys.argv:
    for _k in INPUTS:
        INPUTS[_k] = {"v": PHASE4_V[_k], "src": INPUTS[_k]["src"]}
V = {k: d["v"] for k, d in INPUTS.items()}
SCENARIOS = ["BASE", "GLUT", "SEVERE"]
MONTH0 = (2026, 11)  # month 1 = 2026-11


def month_label(m):
    y, mo = MONTH0
    idx = (mo - 1) + (m - 1)
    return "%04d-%02d" % (y + idx // 12, idx % 12 + 1)


# ----------------------------------------------------------------------------------------------
# DRAM price path per scenario (only feeds the PLP option and the narrative)
# ----------------------------------------------------------------------------------------------
def dram_price(scn, m):
    p0 = V["dram_contract_q4_2026_usd_gb"]
    if m <= 14:  # through 2027-12
        return p0
    k = min(1.0, (m - 14) / 6.0)  # turn spreads over 2028-H1 (m15..m20)
    if scn == "BASE":
        k = min(1.0, (m - 14) / 12.0)
        return p0 * (1 - V["dram_base_2028_decline"] * k)
    target = V["dram_glut_usd_gb"] if scn == "GLUT" else V["dram_severe_usd_gb"]
    return p0 + (target - p0) * k


# ----------------------------------------------------------------------------------------------
# Unit economics
# ----------------------------------------------------------------------------------------------
def unit_cogs(cogs_mult=1.0):
    mr = V["mr4a16b_usd_our_qty"]
    c2 = (mr + V["card_frame_kit_connector_usd"] + V["card_pcb_2mb_usd"] + V["card_logic_2mb_usd"]
          + V["card_assembly_usd"] + V["card_setup_amort_usd"] + V["card_test_pack_usd"] + V["card_shield_usd"])
    c4 = (2 * mr + V["card_frame_kit_connector_usd"] + V["card_pcb_4mb_usd"] + V["card_logic_4mb_usd"]
          + V["card_assembly_4mb_usd"] + V["card_setup_amort_usd"] + V["card_test_pack_usd"] + V["card_shield_usd"])
    d256 = V["fm18w08_usd_our_qty"] + V["dip256_cogs_parts_other_usd"] + V["dip256_assembly_test_usd"]
    d1m = V["fm28v100_usd_our_qty"] + V["dip1m_cogs_parts_other_usd"] + V["dip1m_assembly_test_usd"]
    return {k: v * cogs_mult for k, v in dict(card2=c2, card4=c4, dip256=d256, dip1m=d1m).items()}


def sku_table(price_mult=1.0, cogs_mult=1.0):
    """Per-SKU realized revenue, variable cost and contribution, blended over channels."""
    cogs = unit_cogs(cogs_mult)
    rows = {}
    spec = {
        "card2": (V["card2_price_direct"], V["card_reseller_discount"], V["card_channel_mix"],
                  V["cac_store_card_order"], V["ship_cost_card"]),
        "card4": (V["card4_price_direct"], V["card_reseller_discount"], V["card_channel_mix"],
                  V["cac_store_card_order"], V["ship_cost_card"]),
        "dip256": (V["dip256_price_direct"], V["dip_reseller_discount"], V["dip_channel_mix"],
                   V["cac_store_dip_order"], V["ship_cost_dip"]),
        "dip1m": (V["dip1m_price_direct"], V["dip_reseller_discount"], V["dip_channel_mix"],
                  V["cac_store_dip_order"], V["ship_cost_dip"]),
    }
    for sku, (p, disc, mix, cac, ship) in spec.items():
        p = p * price_mult
        rev = (mix["ebay"] + mix["store"]) * p + mix["reseller"] * p * (1 - disc)
        fees = (mix["ebay"] * (V["ebay_fee_pct"] * p + V["ebay_fee_fixed"])
                + mix["store"] * (V["store_payment_pct"] * p + V["store_payment_fixed"]))
        acq = mix["store"] * cac
        shipping = (mix["ebay"] + mix["store"]) * ship
        warranty = V["warranty_returns_pct"] * rev
        var = fees + acq + shipping + warranty
        gm = (rev - cogs[sku]) / rev
        contrib = rev - cogs[sku] - var
        rows[sku] = dict(list_price=p, rev=rev, cogs=cogs[sku], gm=gm, var=var, contrib=contrib,
                         contrib_pct=contrib / rev)
    return rows


def ramp(m, launch, months, steady):
    if m < launch:
        return 0.0
    return steady * min(1.0, (m - launch + 1) / float(months))


# ----------------------------------------------------------------------------------------------
# 36-month simulation
# ----------------------------------------------------------------------------------------------
def simulate(scn="BASE", price_mult=1.0, volume_mult=1.0, churn_mult=1.0, cogs_mult=1.0,
             ltsa_on=True, card_launch_shift=0, copycat_month=None, copycat_price_mult=1.0):
    dm = V["scn_demand_mult"][scn] * volume_mult
    pm = V["scn_price_mult"][scn] * price_mult
    cm = V["scn_cogs_mult"][scn] * cogs_mult
    skus_pre = sku_table(pm, cm)
    skus_post = sku_table(pm * copycat_price_mult, cm)  # RED-TEAM: copycat price step (RT-VC-DD3-05)
    skus = skus_pre
    mix4 = V["card_mix_4mb"]
    mix1m = V["dip_mix_1m"]
    card_launch = V["card_launch_month"] + card_launch_shift
    N = V["months"]

    def units(m):
        c = ramp(m, card_launch, V["card_ramp_months"], V["card_units_steady_month"]) * dm
        if m >= card_launch:  # RED-TEAM: installed-base retirement + self-depletion (RT-HYP-DD3-02)
            c *= (1 - V["card_demand_decay_yr"]) ** ((m - card_launch) / 12.0)
        d = ramp(m, V["dip_launch_month"], V["dip_ramp_months"], V["dip_units_steady_month"]) * dm
        return c, d

    def cogs_of(c, d):
        return (c * ((1 - mix4) * skus["card2"]["cogs"] + mix4 * skus["card4"]["cogs"])
                + d * ((1 - mix1m) * skus["dip256"]["cogs"] + mix1m * skus["dip1m"]["cogs"]))

    cash = V["start_cash"]
    subs = 0.0
    fulltime = False
    fulltime_month = None
    inv_value = 0.0
    rows = []
    op_hist = []
    first_card_lot_done = False
    first_dip_lot_done = False
    ltb_pool = 0.0  # RED-TEAM: connector/frame lifetime-buy sets on hand (RT-HYP-DD3-03, RT-VET-DD3-04)
    for m in range(1, N + 1):
        skus = skus_post if (copycat_month is not None and m >= copycat_month) else skus_pre
        c, d = units(m)
        rev_card = c * ((1 - mix4) * skus["card2"]["rev"] + mix4 * skus["card4"]["rev"])
        rev_dip = d * ((1 - mix1m) * skus["dip256"]["rev"] + mix1m * skus["dip1m"]["rev"])
        var_card = c * ((1 - mix4) * skus["card2"]["var"] + mix4 * skus["card4"]["var"])
        var_dip = d * ((1 - mix1m) * skus["dip256"]["var"] + mix1m * skus["dip1m"]["var"])
        cogs_goods = cogs_of(c, d)
        # L3 cloud subscriptions
        if m >= V["cloud_launch_month"]:
            direct_card_buyers = c * (V["card_channel_mix"]["ebay"] + V["card_channel_mix"]["store"])
            subs = subs * (1 - V["cloud_churn_month"] * churn_mult) + direct_card_buyers * V["cloud_attach_rate"]
        rev_cloud = subs * V["cloud_price_month"] * pm
        cogs_cloud = subs * V["cloud_cogs_month"]
        # L4 LTSA
        rev_ltsa = 0.0
        if ltsa_on:
            for start, mrr in V["ltsa_contracts"]:
                if m >= start:
                    rev_ltsa += mrr * dm
        cogs_ltsa = rev_ltsa * (1 - V["ltsa_gm"])
        revenue = rev_card + rev_dip + rev_cloud + rev_ltsa
        cogs = cogs_goods + cogs_cloud + cogs_ltsa
        gross = revenue - cogs
        variable = var_card + var_dip
        fixed = V["opex_tools_month"]
        if m >= V["dip_launch_month"]:
            fixed += V["opex_from_launch_month"] + V["opex_marketing_dip"]
        if m >= card_launch:
            fixed += V["opex_marketing_card"] + V["opex_support_retainer"]
        one_time = V["one_time"].get(m, 0.0)
        op_profit = gross - variable - fixed  # before founder salary and one-time
        op_hist.append(op_profit)
        if not fulltime and len(op_hist) >= 3 and sum(op_hist[-3:]) / 3.0 >= V["fulltime_trigger_op_profit_monthly"]:
            fulltime, fulltime_month = True, m
        salary = V["founder_salary_monthly_fulltime"] if fulltime else 0.0
        net = op_profit - one_time - salary
        # inventory: hold N months of forward cover per line; first lots at minimum economic size
        cover_c = cover_d = 0.0
        for k in range(1, V["inventory_cover_months"] + 1):
            cc, dd = units(m + k)
            cover_c += cogs_of(cc, 0.0)
            cover_d += cogs_of(0.0, dd)
        if not first_card_lot_done and m + V["inventory_cover_months"] >= card_launch:
            cover_c = max(cover_c, cogs_of(V["first_lot_cards"], 0.0))
            first_card_lot_done = True
        if not first_dip_lot_done and m + 1 >= V["dip_launch_month"]:
            cover_d = max(cover_d, cogs_of(0.0, V["first_lot_dip"]))
            first_dip_lot_done = True
        cover = cover_c + cover_d
        target_inv = max(cover, inv_value - cogs_goods)  # never write stock down below what is on hand
        purchases = cogs_goods + (target_inv - inv_value)
        inv_value = target_inv
        cash_flow = net + cogs_goods - purchases  # P&L net, adjusted for inventory build
        # RED-TEAM lifetime buy: pay for all sets up front; connectors consumed from the pool need no
        # new cash (COGS already expenses them). Cover stock still re-buys connectors: slightly conservative.
        ltb_cash = 0.0
        conn_usd = V["card_frame_kit_connector_usd"] * cm
        if V["ltb_connector_sets"] and m == V["ltb_month"]:
            ltb_pool = float(V["ltb_connector_sets"])
            ltb_cash -= ltb_pool * conn_usd
        if ltb_pool > 0 and c > 0:
            used = min(ltb_pool, c)
            ltb_pool -= used
            ltb_cash += used * conn_usd
        cash_flow += ltb_cash
        cash += cash_flow
        rows.append(dict(m=m, label=month_label(m), dram=dram_price(scn, m), cards=c, dips=d, subs=subs,
                         rev_card=rev_card, rev_dip=rev_dip, rev_cloud=rev_cloud, rev_ltsa=rev_ltsa,
                         revenue=revenue, gross=gross, variable=variable, fixed=fixed, one_time=one_time,
                         salary=salary, op_profit=op_profit, net=net, inv=inv_value, cash=cash,
                         recurring_mrr=rev_cloud + rev_ltsa, ltb_pool=ltb_pool))
    return dict(rows=rows, fulltime_month=fulltime_month, skus=skus_pre, scn=scn)


def metrics(sim):
    rows = sim["rows"]
    be = None
    for i, r in enumerate(rows):
        if all(x["net"] >= 0 for x in rows[i:]):
            be = r["m"]
            break
    low = min(rows, key=lambda r: r["cash"])
    out = dict(breakeven=be, cash_low=low["cash"], cash_low_m=low["m"], cash_end=rows[-1]["cash"],
               fulltime=sim["fulltime_month"])
    for m in (12, 18, 24, 36):
        r = rows[m - 1]
        out["runrate_%d" % m] = r["revenue"] * 12
        out["arr_%d" % m] = r["recurring_mrr"] * 12
        out["gm_%d" % m] = (r["gross"] / r["revenue"]) if r["revenue"] else 0.0
    out["rev_total"] = sum(r["revenue"] for r in rows)
    out["net_total"] = sum(r["net"] for r in rows)
    out["first_rev_m"] = next((r["m"] for r in rows if r["revenue"] > 0), None)
    out["cards_total"] = sum(r["cards"] for r in rows)
    out["cards_18"] = sum(r["cards"] for r in rows[:18])
    out["ltb_left"] = rows[-1]["ltb_pool"]
    return out


def run_with(over, scn="BASE", **kw):
    """Run simulate() with some INPUT values temporarily overridden (scale-path variants)."""
    saved = {k: V[k] for k in over}
    try:
        V.update(over)
        sim = simulate(scn, **kw)
        return sim, metrics(sim)
    finally:
        V.update(saved)


# Scale-path variants (Q7). Each override is an ESTIMATE; see notes section 7.
# RED-TEAM: card multipliers are now relative to the current BASE volume (Phase 4 hard-coded 80/60/120
# on a base of 40), and the LTSAs exist only in S2/S4 (RT-VC-DD3-04).
def scale_paths():
    b = V["card_units_steady_month"]
    ltsas = [(24, 2000.0), (27, 2000.0), (30, 4000.0), (33, 4000.0)]
    wl = {"ebay": 0.15, "store": 0.20, "reseller": 0.65}
    s0 = "S0 BASE (direct + 40%% resellers%s)" % (", 2 LTSAs" if V["ltsa_contracts"] else ", no LTSA")
    return [
        (s0, {}),
        ("S1 + white-label in 3-4 MRO catalogs (cards x2, 65% reseller)",
         {"card_units_steady_month": 2 * b, "card_channel_mix": wl}),
        ("S2 + DMSMS/OEM program (4 LTSAs, 2 at $4k/mo) [upside only]", {"ltsa_contracts": ltsas}),
        ("S3 + adjacent form factors (Q2MEM, robots, avionics, synth; cards x1.5)",
         {"card_units_steady_month": 1.5 * b}),
        ("S4 stretch: S1+S2+S3 combined (cards x3), cloud attach 15%",
         {"card_units_steady_month": 3 * b, "card_channel_mix": wl, "ltsa_contracts": ltsas,
          "cloud_attach_rate": 0.15}),
    ]


SCALE_PATHS = scale_paths()


# ----------------------------------------------------------------------------------------------
# TAM and PLP option
# ----------------------------------------------------------------------------------------------
def tam():
    us_base = V["fanuc_cnc_cumulative"] * V["us_share_installed"]
    pre_i = us_base * V["legacy_share"] * V["legacy_still_running"]
    i_res = us_base * V["iseries_share"] * V["iseries_still_running"] * V["iseries_card_need"]  # RED-TEAM
    us_machines = pre_i + i_res
    us_shops = us_machines / V["machines_per_shop"]
    us_cards_yr = us_shops / V["card_replacement_years"] * V["other_families_mult"]
    global_cards_yr = us_cards_yr * V["global_over_us_mult"]
    sam_cards_yr = (us_cards_yr * V["sam_over_us_mult"]
                    + max(0.0, global_cards_yr - us_cards_yr) * V["sam_intl_reach"])
    return dict(us_machines=us_machines, pre_i=pre_i, i_res=i_res, us_shops=us_shops, us_cards_yr=us_cards_yr,
                global_cards_yr=global_cards_yr, sam_cards_yr=sam_cards_yr)


def plp_board(scn_price):
    mram_cost = V["plp_mram_mb"] / 1024.0 * V["mram_1gb_stt_usd"] * 8  # 1Gb = 128MB -> $/GB = 8x
    saving = V["plp_dram_cache_gb_replaced"] * scn_price + V["plp_supercap_bom_usd"]
    return dict(mram_cost=mram_cost, saving=saving, premium=mram_cost - saving, ratio=saving / mram_cost)


def plp_option():
    base_ratio = plp_board(V["dram_contract_q4_2026_usd_gb"])["ratio"]
    out = {}
    for scn, price in (("BASE", V["dram_contract_q4_2026_usd_gb"] * (1 - V["dram_base_2028_decline"])),
                       ("GLUT", V["dram_glut_usd_gb"]), ("SEVERE", V["dram_severe_usd_gb"])):
        b = plp_board(price)
        p = V["plp_p_designin_by_m36_base"] * b["ratio"] / base_ratio
        cost = V["plp_ee_contract_usd"] + V["plp_eval_boards_usd"]
        ev_gp = p * V["plp_designin_fee_usd"] * V["plp_services_gm"]
        designins_to_break_even = cost / (V["plp_designin_fee_usd"] * V["plp_services_gm"])
        out[scn] = dict(price=price, board=b, p=p, cost=cost, ev_gp=ev_gp, ev_net=ev_gp - cost,
                        need=designins_to_break_even)
    return out


# ----------------------------------------------------------------------------------------------
# Printing
# ----------------------------------------------------------------------------------------------
def table(headers, rows):
    w = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    line = "  ".join(str(h).rjust(w[i]) if i else str(h).ljust(w[i]) for i, h in enumerate(headers))
    print(line)
    print("  ".join("-" * x for x in w))
    for r in rows:
        print("  ".join(str(c).rjust(w[i]) if i else str(c).ljust(w[i]) for i, c in enumerate(r)))


def money(x):
    s = "-" if x < 0 else ""
    x = abs(x)
    if x >= 1e6:
        return "%s$%.2fM" % (s, x / 1e6)
    if x >= 1e3:
        return "%s$%.1fk" % (s, x / 1e3)
    return "%s$%.0f" % (s, x)


def pct(x):
    return "%.0f%%" % (100 * x)


def main():
    print("=" * 100)
    print("DD3 nv-continuity-modules - unit economics, 36-month P&L (month 1 = %s)" % month_label(1))
    print("DRAM reference: %s" % REF_SRC)
    print("  Q4-2026 contract $%.2f/GB | glut $%.2f/GB | severe $%.2f/GB | incumbent cost $%.2f/GB"
          % (V["dram_contract_q4_2026_usd_gb"], V["dram_glut_usd_gb"], V["dram_severe_usd_gb"],
             REF.get("cost_component_usd_per_gb", 1.48)))
    print("=" * 100)

    if RT_LOG and "--phase4" not in sys.argv:
        print("\n[0] RED-TEAM REVISIONS (Phase 5): Phase 4 value -> revised value (objection ids)")
        for key, old, new, ids, basis in RT_LOG:
            fo = ("%.4g" % old) if isinstance(old, float) else str(old)
            fn = ("%.4g" % new) if isinstance(new, float) else str(new)
            if len(fo) > 30:
                fo = fo[:27] + "..."
            if len(fn) > 30:
                fn = fn[:27] + "..."
            print("  %-29s %-30s -> %-30s %s" % (key, fo, fn, ids))
        cmp_rows = []
        for label, vv in (("Phase 4", PHASE4_V), ("Phase 5 (red team)", dict(V))):
            for scn in SCENARIOS:
                _, mm = run_with(vv, scn=scn)
                cmp_rows.append([label, scn, money(mm["runrate_18"]), money(mm["runrate_36"]), money(mm["arr_36"]),
                                 mm["breakeven"] or "never", "%s (m%d)" % (money(mm["cash_low"]), mm["cash_low_m"]),
                                 money(mm["net_total"]), mm["fulltime"] or "never", "m%s" % mm["first_rev_m"]])
        print("\n  Headline before / after red team")
        table(["model", "scenario", "run-rate m18", "run-rate m36", "rec. ARR m36", "breakeven m", "cash low",
               "36-mo net", "full-time m", "first rev"], cmp_rows)
        _sim = simulate("BASE")
        _cards = sum(r["cards"] for r in _sim["rows"])
        print("\n[0b] CONNECTOR/FRAME LIFETIME BUY: %d sets at $%.2f = %s in m%d; BASE needs %.0f cards m%d-m36 (x1.2 = %.0f);"
              " %.0f sets left at m36"
              % (V["ltb_connector_sets"], V["card_frame_kit_connector_usd"],
                 money(V["ltb_connector_sets"] * V["card_frame_kit_connector_usd"]), V["ltb_month"], _cards,
                 V["card_launch_month"], 1.2 * _cards, _sim["rows"][-1]["ltb_pool"]))

    print("\n[1] UNIT ECONOMICS PER SKU (BASE; revenue blended over eBay / own store / reseller)")
    sk = sku_table()
    names = dict(card2="NV-CARD 2MB (1x MR4A16B)", card4="NV-CARD 4MB (2x MR4A16B)",
                 dip256="NV-DIP 256Kb (FM18W08) DS1225/1230", dip1m="NV-DIP 1Mb (FM28V100) DS1245")
    if V["dip_units_steady_month"] == 0:  # RED-TEAM: DIP leg killed (RT-VET-DD3-03); rows kept for reference
        names["dip256"] += " [KILLED P5]"
        names["dip1m"] += " [KILLED P5]"
    table(["SKU", "list", "net rev/unit", "COGS", "GM", "fees+CAC+ship+warr", "contrib", "contrib%"],
          [[names[k], money(r["list_price"]), "$%.2f" % r["rev"], "$%.2f" % r["cogs"], pct(r["gm"]),
            "$%.2f" % r["var"], "$%.2f" % r["contrib"], pct(r["contrib_pct"])] for k, r in sk.items()])
    print("  MRAM per 2MB card = $%.2f of $%.2f COGS (%.0f%%); per-bit: MR4A16B $%.0f/GB vs DDR5 contract $%.2f/GB"
          % (V["mr4a16b_usd_our_qty"], sk["card2"]["cogs"], 100 * V["mr4a16b_usd_our_qty"] / sk["card2"]["cogs"],
             V["mr4a16b_usd_our_qty"] / (2.0 / 1024), V["dram_contract_q4_2026_usd_gb"]))
    print("  L3 cloud: $%.0f/shop/mo, COGS $%.0f -> GM %s | L4 LTSA GM %s"
          % (V["cloud_price_month"], V["cloud_cogs_month"],
             pct(1 - V["cloud_cogs_month"] / V["cloud_price_month"]), pct(V["ltsa_gm"])))

    print("\n[2] CUSTOMER-ACQUISITION ASSUMPTIONS")
    table(["line", "channel mix (eBay/store/reseller)", "CAC per store order", "launch m", "steady units/mo"],
          [["NV-CARD", "%d/%d/%d%%" % tuple(int(100 * V["card_channel_mix"][k]) for k in ("ebay", "store", "reseller")),
            money(V["cac_store_card_order"]), V["card_launch_month"], V["card_units_steady_month"]],
           ["NV-DIP", "%d/%d/%d%%" % tuple(int(100 * V["dip_channel_mix"][k]) for k in ("ebay", "store", "reseller")),
            money(V["cac_store_dip_order"]), V["dip_launch_month"], V["dip_units_steady_month"]],
           ["CLOUD", "%.0f%% attach of direct card buyers" % (100 * V["cloud_attach_rate"]),
            "$0 (bundled)", V["cloud_launch_month"], "churn %.1f%%/mo" % (100 * V["cloud_churn_month"])],
           ["LTSA", "direct (DMSMS / OEM)", "founder time",
            ", ".join(str(s_) for s_, _ in V["ltsa_contracts"]) or "none in BASE",
            ("$%.0f/mo each" % V["ltsa_contracts"][0][1]) if V["ltsa_contracts"] else "upside only (S2/S4)"]])

    t = tam()
    print("\n[3] DEMAND SIZING (TAM, ESTIMATE chain)")
    print("  Fanuc cumulative CNCs %s x US %.0f%% x pre-i/CF-rejecting %.0f%% x still running %.0f%% = %s U.S. machines"
          % ("{:,}".format(V["fanuc_cnc_cumulative"]), 100 * V["us_share_installed"], 100 * V["legacy_share"],
             100 * V["legacy_still_running"], "{:,.0f}".format(t["pre_i"])))
    if V["iseries_share"]:
        print("  + i-series residual: x i-A/early-i %.0f%% x running %.0f%% x residual SRAM-card need %.0f%% = %s machine-equivalents"
              % (100 * V["iseries_share"], 100 * V["iseries_still_running"], 100 * V["iseries_card_need"],
                 "{:,.0f}".format(t["i_res"])))
    print("  = %s U.S. machines / %d per shop = %s shops; replacement every %d yrs x %.2f other families = %s cards/yr U.S."
          % ("{:,.0f}".format(t["us_machines"]), V["machines_per_shop"], "{:,.0f}".format(t["us_shops"]),
             V["card_replacement_years"], V["other_families_mult"], "{:,.0f}".format(t["us_cards_yr"])))
    print("  Addressable (SAM) = U.S. x %.2f + %.0f%% of non-U.S. = %s cards/yr; global = U.S. x %.2f = %s cards/yr"
          % (V["sam_over_us_mult"], 100 * V["sam_intl_reach"], "{:,.0f}".format(t["sam_cards_yr"]),
             V["global_over_us_mult"], "{:,.0f}".format(t["global_cards_yr"])))
    print("  Base plan steady state %d cards/mo = %d/yr = %.0f%% of SAM, %.0f%% of U.S., %.0f%% of global demand"
          " (before the %.0f%%/yr decay)"
          % (V["card_units_steady_month"], 12 * V["card_units_steady_month"],
             100 * 12 * V["card_units_steady_month"] / t["sam_cards_yr"],
             100 * 12 * V["card_units_steady_month"] / t["us_cards_yr"],
             100 * 12 * V["card_units_steady_month"] / t["global_cards_yr"], 100 * V["card_demand_decay_yr"]))
    blended_card_rev = (1 - V["card_mix_4mb"]) * sk["card2"]["rev"] + V["card_mix_4mb"] * sk["card4"]["rev"]
    print("  Card market at blended $%.0f/card: SAM %s/yr; U.S. %s/yr; global %s/yr"
          % (blended_card_rev, money(t["sam_cards_yr"] * blended_card_rev), money(t["us_cards_yr"] * blended_card_rev),
             money(t["global_cards_yr"] * blended_card_rev)))

    sims = {s: simulate(s) for s in SCENARIOS}
    mets = {s: metrics(sims[s]) for s in SCENARIOS}

    print("\n[4] MONTHLY P&L AND CASH - BASE (founder part-time, no salary until trigger)")
    hdr = ["m", "month", "cards", "DIPs", "subs", "revenue", "gross", "var+fixed", "one-time", "salary", "net", "inventory", "cash"]
    rws = []
    for r in sims["BASE"]["rows"]:
        rws.append([r["m"], r["label"], "%.0f" % r["cards"], "%.0f" % r["dips"], "%.0f" % r["subs"],
                    money(r["revenue"]), money(r["gross"]), money(r["variable"] + r["fixed"]),
                    money(r["one_time"]), money(r["salary"]), money(r["net"]), money(r["inv"]), money(r["cash"])])
    table(hdr, rws)

    print("\n[4b] CASH CURVE BY SCENARIO (end of quarter; start $%.0fk)" % (V["start_cash"] / 1000))
    qs = list(range(3, V["months"] + 1, 3))
    table(["scenario"] + ["m%d" % q for q in qs],
          [[s] + [money(sims[s]["rows"][q - 1]["cash"]) for q in qs] for s in SCENARIOS])

    print("\n[5] SCENARIO SUMMARY (core lines L1-L4; PLP option excluded - see [7])")
    rows = []
    for s in SCENARIOS:
        mm = mets[s]
        rows.append([s, mm["breakeven"] or "never", "%s (m%d)" % (money(mm["cash_low"]), mm["cash_low_m"]),
                     money(mm["cash_end"]), mm["fulltime"] or "never", money(mm["rev_total"]),
                     money(mm["net_total"]), pct(mm["gm_36"])])
    table(["scenario", "breakeven m", "cash low", "cash m36", "full-time m", "36-mo revenue", "36-mo net", "GM m36"], rows)
    print("  first revenue month (BASE): m%s (%s); cumulative cards m18 / m36: %.0f / %.0f"
          % (mets["BASE"]["first_rev_m"], month_label(mets["BASE"]["first_rev_m"]), mets["BASE"]["cards_18"],
             mets["BASE"]["cards_total"]))
    print("\n  ARR at months 12 / 18 / 24 / 36")
    rows = []
    for s in SCENARIOS:
        mm = mets[s]
        rows.append([s] + [money(mm["runrate_%d" % m]) for m in (12, 18, 24, 36)]
                    + [money(mm["arr_%d" % m]) for m in (12, 18, 24, 36)])
    table(["scenario", "run-rate m12", "m18", "m24", "m36", "recurring ARR m12", "m18", "m24", "m36"], rows)
    print("  run-rate = that month's revenue x 12 (hardware is repeat-purchase, not contracted).")
    print("  recurring ARR = (cloud MRR + LTSA monthly) x 12 = the only contracted/subscription revenue.")
    print("  DRAM $/GB used per scenario at m24: " + ", ".join(
        "%s $%.2f" % (s, sims[s]["rows"][23]["dram"]) for s in SCENARIOS))

    print("\n[6] SENSITIVITY (BASE; one variable at a time, -30% / +30%)")
    srows = []
    cases = [("baseline", {}),
             ("price -30%", dict(price_mult=0.7)), ("price +30%", dict(price_mult=1.3)),
             ("conversion/close -30%", dict(volume_mult=0.7)), ("conversion/close +30%", dict(volume_mult=1.3)),
             ("churn -30%", dict(churn_mult=0.7)), ("churn +30%", dict(churn_mult=1.3)),
             ("COGS -30%", dict(cogs_mult=0.7)), ("COGS +30%", dict(cogs_mult=1.3)),
             ("no LTSA/DMSMS contract", dict(ltsa_on=False)),
             ("card launch +6 mo (MRAM lead/validation slip)", dict(card_launch_shift=6)),
             # RED-TEAM rows (Phase 5)
             ("RT price x0.8 (RT-HYP-DD3-04)", dict(price_mult=0.8)),
             ("RT volume x0.5 (RT-HYP-DD3-02)", dict(volume_mult=0.5)),
             ("RT copycat from m24, price x0.75 (RT-VC-DD3-05)", dict(copycat_month=24, copycat_price_mult=0.75))]
    over_cases = [("RT + 2 LTSAs from m27/m33 (upside, RT-VC-DD3-04)", {"ltsa_contracts": [(27, 2000.0), (33, 2000.0)]}),
                  ("RT no demand decay", {"card_demand_decay_yr": 0.0}),
                  ("RT volume back to Phase 4 (40/mo)", {"card_units_steady_month": 40}),
                  ("RT LTB at MOQ 1,000 sets", {"ltb_connector_sets": 1000}),
                  ("RT no connector LTB (two live sources found)", {"ltb_connector_sets": 0, "card_frame_kit_connector_usd": 12.0}),
                  ("RT DIP line restored as Phase 4 (F-RAM)", {"dip_units_steady_month": 50, "first_lot_dip": 200,
                                                              "opex_marketing_dip": 300.0}),
                  ("RT lean re-plan (partner benches, lab $4k, 50-card lots)",
                   {"one_time": {1: 1100.0, 2: 3000.0, 3: 3000.0, 4: 3000.0, 5: 1500.0, 6: 1500.0, 7: 500.0,
                                 8: 4000.0 + 1500.0}, "first_lot_cards": 50, "card_setup_amort_usd": 8.0}),
                  ("RT demand-validated: 40/mo, price x1.0, LTB 880", {"card_units_steady_month": 40,
                                                                      "ltb_connector_sets": 880})]
    for name, kw in cases:
        mm = metrics(simulate("BASE", **kw))
        srows.append([name, mm["breakeven"] or "never", money(mm["cash_low"]), money(mm["runrate_18"]),
                      money(mm["runrate_36"]), money(mm["arr_36"]), money(mm["net_total"])])
    for name, over in over_cases:
        _, mm = run_with(over)
        srows.append([name, mm["breakeven"] or "never", money(mm["cash_low"]), money(mm["runrate_18"]),
                      money(mm["runrate_36"]), money(mm["arr_36"]), money(mm["net_total"])])
    table(["case", "breakeven m", "cash low", "run-rate m18", "run-rate m36", "rec. ARR m36", "36-mo cum. net"], srows)

    print("\n[6b] SCALE PATH BEYOND THE 'LOW-$100ks' CEILING (BASE market; overrides are ESTIMATES)")
    t_ = tam()
    rows = []
    for name, over in scale_paths():
        sim_, mm = run_with(over)
        cards_yr = 12 * over.get("card_units_steady_month", V["card_units_steady_month"])
        rows.append([name, money(mm["runrate_36"]), money(mm["arr_36"]), money(mm["net_total"]),
                     mm["fulltime"] or "never", "%.0f%%" % (100 * cards_yr / t_["sam_cards_yr"]),
                     "%.0f%%" % (100 * cards_yr / t_["global_cards_yr"])])
    table(["path", "run-rate m36", "rec. ARR m36", "36-mo net", "full-time m", "share of SAM", "share of global"], rows)
    print("  Even the stretch path stays well under $1M/yr; card shares are of steady-state demand before decay.")

    print("\n[7] C-16 PLP OPTION - MRAM journal vs DRAM cache + supercaps (per board) and option value")
    po = plp_option()
    table(["scenario", "DRAM $/GB (2028+)", "MRAM 512MB cost", "DRAM 2GB + caps saved", "MRAM premium/board",
           "p(paid design-in by m36)", "option cost", "EV gross profit", "EV net", "design-ins to break even"],
          [[s, "$%.2f" % o["price"], money(o["board"]["mram_cost"]), money(o["board"]["saving"]),
            money(o["board"]["premium"]), "%.2f" % o["p"], money(o["cost"]), money(o["ev_gp"]),
            money(o["ev_net"]), "%.1f" % o["need"]] for s, o in po.items()])
    print("  MRAM never wins on BOM; the DRAM glut moves the per-board gap by only ~$%.0f-%.0f. Buyers adopt for"
          % (po["GLUT"]["board"]["premium"] - po["BASE"]["board"]["premium"],
             po["SEVERE"]["board"]["premium"] - po["BASE"]["board"]["premium"]))
    print("  reliability (no supercap aging), so the kit's market is set by controller vendors, not price.")
    print("  ITC 337-TA-1487 target date %s: exclusion risk applies to Everspin STT (1Gb, xSPI), not to Toggle MR4A16B."
          % V["itc_target_date"])
    if V["plp_supercap_bom_usd"] < PHASE4_V["plp_supercap_bom_usd"]:
        print("  RED-TEAM (RT-PHY-DD3-07): hold-up energy is still needed for in-flight NAND program/erase (paired pages)")
        print("  unless the FTL changes, and the founder owns no FTL. Only $%.0f of the $%.0f cap BOM is removable."
              % (V["plp_supercap_bom_usd"], PHASE4_V["plp_supercap_bom_usd"]))
        print("  VERDICT: C-16 KILLED (Phase 5). The email interest test is dropped.")
    else:
        print("  VERDICT: negative EV at T0 in every scenario -> defer C-16; run only a zero-cost interest test.")

    print("\n[8] WHAT MUST BE TRUE")
    sk_b = sku_table()
    card_contrib = (1 - V["card_mix_4mb"]) * sk_b["card2"]["contrib"] + V["card_mix_4mb"] * sk_b["card4"]["contrib"]
    dip_contrib = (1 - V["dip_mix_1m"]) * sk_b["dip256"]["contrib"] + V["dip_mix_1m"] * sk_b["dip1m"]["contrib"]
    dip_rev = (1 - V["dip_mix_1m"]) * sk_b["dip256"]["rev"] + V["dip_mix_1m"] * sk_b["dip1m"]["rev"]
    fixed_full = (V["opex_tools_month"] + V["opex_from_launch_month"] + V["opex_marketing_dip"] + V["opex_marketing_card"]
                  + V["opex_support_retainer"])  # RED-TEAM: retainer added (RT-VC-DD3-06)
    r18 = sims["BASE"]["rows"][17]
    print("  Contribution per card $%.0f, per DIP $%.0f; fixed opex at full launch $%.0f/mo."
          % (card_contrib, dip_contrib, fixed_full))
    print("  (a) Part-time breakeven: %.0f cards/mo (or %.0f DIPs/mo) cover fixed opex. BASE at m18 sells %.0f cards + %.0f DIPs."
          % (fixed_full / card_contrib, fixed_full / dip_contrib, r18["cards"], r18["dips"]))
    need_ft = (fixed_full + V["founder_salary_monthly_fulltime"]) / card_contrib
    print("  (b) Founder full-time ($%.0fk/yr): %.0f cards/mo = %.0f%% of addressable (SAM) / %.0f%% of global card demand."
          % (V["founder_salary_monthly_fulltime"] * 12 / 1000, need_ft, 100 * need_ft * 12 / t["sam_cards_yr"],
             100 * need_ft * 12 / t["global_cards_yr"]))
    need_half = 500000 / 12.0 / blended_card_rev
    print("  (c) $0.5M/yr run-rate from cards alone: %.0f cards/mo = %.0f%% of SAM / %.0f%% of global demand."
          % (need_half, 100 * need_half * 12 / t["sam_cards_yr"], 100 * need_half * 12 / t["global_cards_yr"]))
    orders_18 = sum(r["cards"] + r["dips"] for r in sims["BASE"]["rows"][:18])
    be_units = None
    for u_ in range(int(V["card_units_steady_month"]), 400):
        _, mm_ = run_with({"card_units_steady_month": u_})
        if mm_["net_total"] >= 0:
            be_units = u_
            break
    if be_units:
        print("  (f) 36-month cumulative net >= 0 needs %d cards/mo steady (BASE has %d) = %.0f%% of SAM / %.0f%% of U.S. demand."
              % (be_units, V["card_units_steady_month"], 100 * 12 * be_units / t["sam_cards_yr"],
                 100 * 12 * be_units / t["us_cards_yr"]))
    print("  (d) Cumulative orders by m18 in BASE: %.0f units (%.0f cards, %.0f DIPs); reseller accounts needed: >=3 by m12."
          % (orders_18, sum(r["cards"] for r in sims["BASE"]["rows"][:18]),
             sum(r["dips"] for r in sims["BASE"]["rows"][:18])))
    if V["iseries_share"]:
        print("  (e) Status after red team: KILLED in BASE. Reopen only if a $1.2k demand probe gets >=30 full-list deposits"
              " (<=1/3 i-series) AND a reseller LOI >=100 cards/yr at >=$175, or a white-label commitment >=200 cards/yr x 2 yrs.")
        print("      After a reopen, the card line dies if a pre-i Fanuc (16-C/18-C/21-B) rejects it, if a shielded card loses"
              " data at 30 mT or after 60 s on a 0.3 T magnetic base, or if hot removal corrupts non-addressed data.")
    else:
        print("  (e) Kill line: <15 paid pre-orders + <2 reseller LOIs in the 30-day test, or a Fanuc 16i/18i/21i or"
              " Mitsubishi Q CPU rejects the MRAM card (format/read/write).")

    print("\n[9] INPUTS (value | source)")
    for k, d in INPUTS.items():
        v = d["v"]
        vs = str(v) if not isinstance(v, float) else ("%.4g" % v)
        print("  %-36s %-28s | %s" % (k, vs[:28], d["src"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
