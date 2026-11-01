#!/usr/bin/env python3
"""A2 resource-intensity model for DRAM (agent A2-resources, NEW DRAM study, as of 2026-11-01).

What it does
  Per 300mm wafer and per GB of 1-beta DDR5: electricity, water, silicon, and the mass of the
  "interesting" elements (Hf, Zr, W, Cu, and hypothetical Ru, Ge, In, Ga, Sc for new cell concepts).
  It scales those to the whole DRAM fleet, compares them with world supply, and gives each one's share
  of wafer cost. It also compares embodied (fab) electricity with use-phase electricity per GB.

Conventions
  Every input is (base, low, high, tag, basis). Tags follow ram-venture/research/CONVENTIONS.md:
  [ESTIMATE] = my arithmetic/assumption; [REPORTED] = search-snippet source (see
  research/sources/A2-resources.jsonl); [UNVERIFIED-PK] = prior knowledge, no URL.
  DDR5 anchors are reused from ram-venture/models/dram_cost_stack.py (1-beta 16Gb die 36.5 mm^2,
  1,534 good dies/wafer, $3,800 wafer, $1.48/GB).

Run: python3 dram-moonshot/research/models/A2_resource_intensity.py   (stdlib only; exits 0)
"""
import math

# ----------------------------------------------------------------------------------------------
# 1. Anchors reused from ram-venture (do not redo)
# ----------------------------------------------------------------------------------------------
WAFER_AREA_CM2 = math.pi * 15.0 ** 2          # 706.9 cm^2, 300mm wafer
GOOD_DIES_1B = 1534                           # dram_cost_stack.py, DDR5 16Gb 1-beta, yield 0.90
GB_PER_DIE = 2.0                              # 16Gb
GB_PER_WAFER_1B = GOOD_DIES_1B * GB_PER_DIE   # 3,068 GB
WAFER_COST_1B = 3800.0                        # $ fully loaded, dram_cost_stack.py base
COST_PER_GB_1B = 1.48                         # $/GB, dram_cost_stack.py base
CELL_AREA_UM2 = 1.0 / (0.447e9 / 1e6) * 0.60  # chip-level 0.447 Gb/mm^2 x 0.60 array eff -> ~1.34e-3 um^2/bit

# ----------------------------------------------------------------------------------------------
# 2. Inputs (base, low, high, tag, basis)
# ----------------------------------------------------------------------------------------------
P = {
    # fleet
    "fleet_wpm": (1.85e6, 1.7e6, 2.0e6, "[ESTIMATE]",
                  "2023 1.7M wpm (ram-venture cost_inputs, UNVERIFIED-PK) + ~4%/yr additions to 2026"),
    # energy
    "kwh_per_wafer": (1300.0, 900.0, 2000.0, "[ESTIMATE]",
                      "Micron company-wide 11 TWh/yr (2023 SR, REPORTED) / ~7.2-8.4M wafers/yr (DRAM 0.35M + NAND "
                      "0.25-0.35M wpm, UNVERIFIED-PK) = 1,310-1,530; Silicon Analysts 800-1,500 kWh/wafer advanced logic (REPORTED)"),
    "usd_per_kwh": (0.10, 0.06, 0.14, "[UNVERIFIED-PK]", "industrial tariffs: Idaho ~0.06, Taiwan ~0.10, Korea ~0.13"),
    "grid_kgco2_per_kwh": (0.45, 0.30, 0.50, "[UNVERIFIED-PK]", "Korea/Taiwan grid intensity"),
    # EUV
    "euv_gwh_per_tool_yr": (10.2, 5.6, 12.2, "[REPORTED]",
                            "TechInsights up to 10.2 GWh/yr; SPIE 2008 640 kW@100 wph = 5.6 GWh; Bits&Chips 12.2 GWh high-NA"),
    "euv_exposures_per_tool_yr": (0.91e6, 0.7e6, 1.1e6, "[ESTIMATE]", "ram-venture cost_stack.md 2.4: 80% uptime x 130 wph"),
    "euv_layers_dram": (6, 0, 7, "[REPORTED]", "SK hynix 1c 6 layers (TechNews 2025-08); Micron 1-beta 0; CXMT 0"),
    "tin_droplet_um": (27.0, 20.0, 30.0, "[UNVERIFIED-PK]", "LPP source droplet diameter"),
    "tin_droplet_hz": (50000.0, 50000.0, 80000.0, "[REPORTED]", "TechInsights: 50,000 droplets/s"),
    # water
    "m3_water_per_wafer": (8.0, 5.0, 25.0, "[ESTIMATE]",
                           "rule of thumb ~2,200 gal (8.3 m3) incl. ~1,500 gal UPW per 300mm wafer (UNVERIFIED-PK); "
                           "Micron Clay 48 MGD (182k m3/d, REPORTED) / assumed 4 fabs x 60-150k wpm gives 12-25 m3"),
    "usd_per_m3_water": (2.0, 1.0, 4.0, "[UNVERIFIED-PK]", "intake + UPW + wastewater treatment, ex-capex"),
    # silicon
    "wafer_thickness_um": (775.0, 775.0, 775.0, "[UNVERIFIED-PK]", "SEMI M1 300mm"),
    "poly_per_wafer_factor": (2.0, 1.7, 2.5, "[UNVERIFIED-PK]", "crystal top/tail, kerf, polish losses"),
    "prime_wafer_usd": (115.0, 100.0, 140.0, "[ESTIMATE]", "ram-venture cost_inputs $100-130; +May-2026 hikes (REPORTED)"),
    # capacitor geometry (1-beta pillar capacitor)
    "cap_diam_nm": (28.0, 24.0, 35.0, "[UNVERIFIED-PK]", "1b-class storage node outer diameter"),
    "cap_height_um": (1.4, 1.1, 1.8, "[UNVERIFIED-PK]", "storage node height (AR ~50)"),
    "array_frac_of_wafer": (0.51, 0.45, 0.55, "[ESTIMATE]", "0.85 die area x 0.60 array efficiency"),
    "cap_dielectric_nm": (6.0, 5.0, 8.0, "[UNVERIFIED-PK]", "ZrO2/Al2O3/ZrO2 stack"),
    "hzo_fe_nm": (10.0, 8.0, 12.0, "[UNVERIFIED-PK]", "HZO ferroelectric capacitor film (FeRAM/NVDRAM-class)"),
    "electrode_nm": (5.0, 3.0, 8.0, "[UNVERIFIED-PK]", "per electrode, TiN today; Ru hypothetical"),
    "ald_util": (0.10, 0.05, 0.30, "[UNVERIFIED-PK]", "ALD precursor utilization into film (rest to walls/exhaust)"),
    # W, Cu
    "w_deposited_g": (2.0, 1.0, 4.0, "[ESTIMATE]",
                      "~4 W levels (buried WL, BL/SN contacts, landing pad, periphery contact) x ~0.4 um blanket-equivalent"),
    "wf6_util": (0.30, 0.20, 0.50, "[UNVERIFIED-PK]", "CVD W WF6 utilization"),
    "cu_g": (2.0, 1.0, 4.0, "[ESTIMATE]", "3 periphery Cu levels x ~1 um plated overburden"),
    # 3D DRAM Si/SiGe superlattice (hypothetical scale-up)
    "sige_pairs": (100, 32, 200, "[ESTIMATE]", "3D DRAM epitaxial Si/SiGe stack layer pairs"),
    "sige_nm": (10.0, 8.0, 20.0, "[ESTIMATE]", "SiGe sacrificial layer thickness"),
    "ge_atfrac": (0.20, 0.15, 0.30, "[ESTIMATE]", "Ge atomic fraction in SiGe"),
    "geh4_util": (0.20, 0.10, 0.40, "[UNVERIFIED-PK]", "epi germane utilization"),
    # IGZO and AlScN (hypothetical)
    "igzo_nm": (10.0, 5.0, 15.0, "[ESTIMATE]", "oxide channel thickness"),
    "igzo_area_factor": (5.0, 1.0, 40.0, "[ESTIMATE]", "blanket area / wafer area (1 = planar, 40 = many 3D tiers)"),
    "sputter_util": (0.30, 0.15, 0.40, "[UNVERIFIED-PK]", "target utilization"),
    "alscn_nm": (10.0, 10.0, 45.0, "[ESTIMATE]", "AlScN ferroelectric thickness"),
    # world supply (t/yr)
    "world_w_t": (85000.0, 80000.0, 90000.0, "[REPORTED]", "~85 kt, China ~80% (Oregon Group 2026, via snippet)"),
    "world_hf_t": (80.0, 60.0, 100.0, "[UNVERIFIED-PK]", "separated Hf metal/oxide; nuclear-Zr by-product"),
    "world_zircon_t": (1.5e6, 1.2e6, 1.7e6, "[UNVERIFIED-PK]", "zircon concentrate"),
    "world_ru_t": (35.0, 30.0, 40.0, "[UNVERIFIED-PK]", "PGM by-product, South Africa dominant"),
    "world_ge_t": (140.0, 120.0, 220.0, "[UNVERIFIED-PK]", "refined Ge, China ~2/3"),
    "world_in_t": (1050.0, 950.0, 1100.0, "[UNVERIFIED-PK]", "refined In, China ~60-70%"),
    "world_ga_t": (760.0, 600.0, 1000.0, "[UNVERIFIED-PK]", "primary Ga, China ~98%"),
    "world_sc_t": (20.0, 10.0, 30.0, "[UNVERIFIED-PK]", "Sc metal-equivalent (~30 t Sc2O3)"),
    "world_cu_t": (23e6, 22e6, 24e6, "[UNVERIFIED-PK]", "mine copper"),
    "world_semi_poly_t": (45000.0, 40000.0, 55000.0, "[UNVERIFIED-PK]", "semiconductor-grade polysilicon"),
    "world_sn_t": (300000.0, 280000.0, 380000.0, "[UNVERIFIED-PK]", "refined tin"),
    # prices ($/kg)
    "price_hf": (12000.0, 5000.0, 13115.0, "[REPORTED]", "SMM ~$5k -> $13.1k/kg Nov-25 to Apr-26; IMARC ~$12k Q2-26"),
    "price_w": (400.0, 50.0, 420.0, "[ESTIMATE]", "APT $3,185/mtu (Oregon Group 2026) = $318/kg WO3 -> ~$400/kg W"),
    "price_ru": (56210.0, 17980.0, 56210.0, "[REPORTED]", "$56.21/g Mar-2026 vs $17.98/g Mar-2025 (via snippet)"),
    "price_ge": (3000.0, 1500.0, 5000.0, "[UNVERIFIED-PK]", "Ge metal after 2023-25 China controls"),
    "price_cu": (10.0, 8.0, 20.0, "[UNVERIFIED-PK]", "copper; sensitivity to 2x"),
    # use phase
    "use_w_per_gb": (0.15, 0.10, 0.25, "[UNVERIFIED-PK]", "server DDR5 RDIMM ~8-12 W per 64GB average"),
    "life_years": (5.0, 4.0, 7.0, "[ESTIMATE]", "server memory service life"),
}


def v(k, which=0):
    return P[k][which]


def fmt(x, nd=2):
    if x == 0:
        return "0"
    if abs(x) >= 1e5 or abs(x) < 1e-3:
        return f"{x:.2e}"
    return f"{x:,.{nd}f}"


# ----------------------------------------------------------------------------------------------
# 3. Calculations
# ----------------------------------------------------------------------------------------------
def cap_area_m2(w=0):
    """Capacitor dielectric area per wafer (m^2): array region x enhancement + rest x 1."""
    lateral_um2 = math.pi * (v("cap_diam_nm", w) / 1000.0) * v("cap_height_um", w)
    enh = lateral_um2 / CELL_AREA_UM2
    af = v("array_frac_of_wafer", w)
    return WAFER_AREA_CM2 / 1e4 * (af * enh + (1 - af)), enh


def film_mass_g(area_m2, nm, rho):
    return area_m2 * 1e4 * nm * 1e-7 * rho


def run():
    out = {}
    fleet_wafers = v("fleet_wpm") * 12
    out["fleet_wafers_yr"] = fleet_wafers

    # energy
    kwh = v("kwh_per_wafer")
    out["kwh_per_gb"] = kwh / GB_PER_WAFER_1B
    out["kwh_per_gb_lo"] = v("kwh_per_wafer", 1) / GB_PER_WAFER_1B
    out["kwh_per_gb_hi"] = v("kwh_per_wafer", 2) / GB_PER_WAFER_1B
    out["elec_usd_per_wafer"] = kwh * v("usd_per_kwh")
    out["elec_share_wafer_cost"] = out["elec_usd_per_wafer"] / WAFER_COST_1B
    out["fleet_twh"] = fleet_wafers * kwh / 1e9
    out["gco2_per_gb_elec"] = out["kwh_per_gb"] * v("grid_kgco2_per_kwh") * 1000
    # EUV
    kwh_per_exposure = v("euv_gwh_per_tool_yr") * 1e6 / v("euv_exposures_per_tool_yr")
    out["euv_kwh_per_exposure"] = kwh_per_exposure
    out["euv_kwh_per_wafer_6L"] = kwh_per_exposure * v("euv_layers_dram")
    out["euv_share_of_wafer_kwh"] = out["euv_kwh_per_wafer_6L"] / kwh
    r_cm = v("tin_droplet_um") / 2 * 1e-4
    sn_g_s = 4 / 3 * math.pi * r_cm ** 3 * 7.3 * v("tin_droplet_hz")
    out["tin_kg_per_tool_yr"] = sn_g_s * 3600 * 24 * 365 * 0.8 / 1000
    # use phase
    out["use_kwh_per_gb_life"] = v("use_w_per_gb") * 8760 * v("life_years") / 1000
    out["use_over_embodied"] = out["use_kwh_per_gb_life"] / out["kwh_per_gb"]

    # water
    out["l_water_per_gb"] = v("m3_water_per_wafer") * 1000 / GB_PER_WAFER_1B
    out["water_usd_per_wafer"] = v("m3_water_per_wafer") * v("usd_per_m3_water")
    out["fleet_water_mm3_yr"] = fleet_wafers * v("m3_water_per_wafer") / 1e6

    # silicon
    si_g = WAFER_AREA_CM2 * v("wafer_thickness_um") * 1e-4 * 2.329
    out["si_g_per_wafer"] = si_g
    out["si_mg_per_gb"] = si_g * 1000 / GB_PER_WAFER_1B
    out["fleet_poly_t"] = fleet_wafers * si_g * v("poly_per_wafer_factor") / 1e6
    out["fleet_poly_share"] = out["fleet_poly_t"] / v("world_semi_poly_t")
    out["wafer_share_wafer_cost"] = v("prime_wafer_usd") / WAFER_COST_1B

    # capacitor films
    area, enh = cap_area_m2()
    out["cap_area_m2"], out["cap_enh"] = area, enh
    zro2 = film_mass_g(area, v("cap_dielectric_nm"), 5.68)
    out["zr_dep_g"] = zro2 * 91.22 / 123.22
    hzo = film_mass_g(area, v("hzo_fe_nm"), 8.3)
    hf_frac = 0.5 * 178.49 / (0.5 * 178.49 + 0.5 * 91.22 + 32.0)
    out["hf_dep_g_hzo"] = hzo * hf_frac

    def element_row(name, dep_g, util, world_t, price):
        cons_g = dep_g / util
        return dict(name=name, dep_g=dep_g, cons_g=cons_g,
                    fleet_t=fleet_wafers * cons_g / 1e6,
                    share=fleet_wafers * cons_g / 1e6 / world_t if world_t else float("nan"),
                    usd_wafer=cons_g / 1000 * price if price else float("nan"))

    rows = []
    rows.append(element_row("Zr (ZrO2 cap dielectric, today)", out["zr_dep_g"], v("ald_util"),
                            v("world_zircon_t") * 0.49, None))
    rows.append(element_row("Hf (HZO 10nm FE capacitor, hypothetical all-fleet)", out["hf_dep_g_hzo"], v("ald_util"),
                            v("world_hf_t"), v("price_hf")))
    rows.append(element_row("Hf (same, 30% ALD utilization)", out["hf_dep_g_hzo"], 0.30, v("world_hf_t"), v("price_hf")))
    rows.append(element_row("W (word lines, contacts, today)", v("w_deposited_g"), v("wf6_util"), v("world_w_t"),
                            v("price_w")))
    rows.append(element_row("Cu (periphery BEOL, today)", v("cu_g"), 1.0, v("world_cu_t"), v("price_cu")))
    ru_dep = film_mass_g(area, 2 * v("electrode_nm"), 12.45)
    rows.append(element_row("Ru (2 cap electrodes, hypothetical)", ru_dep, 0.15, v("world_ru_t"), v("price_ru")))
    rows.append(element_row("Ru (same, 100% recovery/utilization)", ru_dep, 1.0, v("world_ru_t"), v("price_ru")))
    x = v("ge_atfrac")
    rho_sige = 2.329 + (5.323 - 2.329) * x
    ge_mfrac = x * 72.63 / (x * 72.63 + (1 - x) * 28.09)
    sige = WAFER_AREA_CM2 * v("sige_pairs") * v("sige_nm") * 1e-7 * rho_sige
    rows.append(element_row("Ge (3D DRAM Si/SiGe 100 pairs, hypothetical)", sige * ge_mfrac, v("geh4_util"),
                            v("world_ge_t"), v("price_ge")))
    sige_hi = WAFER_AREA_CM2 * 200 * 10 * 1e-7 * (2.329 + (5.323 - 2.329) * 0.30)
    ge_hi_frac = 0.30 * 72.63 / (0.30 * 72.63 + 0.70 * 28.09)
    rows.append(element_row("Ge (200 pairs, 30% Ge, 10% util)", sige_hi * ge_hi_frac, 0.10, v("world_ge_t"),
                            v("price_ge")))
    igzo = WAFER_AREA_CM2 * v("igzo_area_factor") * v("igzo_nm") * 1e-7 * 6.1
    m_igzo = 114.82 + 69.72 + 65.38 + 64.0
    rows.append(element_row("In (IGZO channel, area x5)", igzo * 114.82 / m_igzo, v("sputter_util"), v("world_in_t"), None))
    rows.append(element_row("Ga (IGZO channel, area x5)", igzo * 69.72 / m_igzo, v("sputter_util"), v("world_ga_t"), None))
    igzo40 = WAFER_AREA_CM2 * 40 * v("igzo_nm") * 1e-7 * 6.1
    rows.append(element_row("Ga (IGZO, 40x area: many 3D tiers)", igzo40 * 69.72 / m_igzo, v("sputter_util"),
                            v("world_ga_t"), None))
    m_alscn = 0.7 * 26.98 + 0.3 * 44.96 + 14.01
    alscn3d = film_mass_g(area, v("alscn_nm"), 3.5)
    rows.append(element_row("Sc (AlScN 10nm on 3D capacitor area)", alscn3d * 0.3 * 44.96 / m_alscn, v("sputter_util"),
                            v("world_sc_t"), None))
    alscn_pl = WAFER_AREA_CM2 * v("alscn_nm") * 1e-7 * 3.5
    rows.append(element_row("Sc (AlScN 10nm planar crossbar)", alscn_pl * 0.3 * 44.96 / m_alscn, v("sputter_util"),
                            v("world_sc_t"), None))
    out["rows"] = rows
    # fleet tin for EUV (assume ~300 DRAM+logic EUV tools installed by 2026)
    out["tin_fleet_t"] = out["tin_kg_per_tool_yr"] * 300 / 1000
    out["tin_share"] = out["tin_fleet_t"] / v("world_sn_t")
    return out


def main():
    o = run()
    print("A2 RESOURCE-INTENSITY MODEL  (agent A2-resources, as of 2026-11-01; all [ESTIMATE] unless tagged)")
    print(f"Anchor: DDR5 16Gb 1-beta, {GOOD_DIES_1B} good dies/wafer = {GB_PER_WAFER_1B:,.0f} GB/wafer; "
          f"wafer ${WAFER_COST_1B:,.0f}; ${COST_PER_GB_1B}/GB (ram-venture/models/dram_cost_stack.py)")
    print(f"Fleet: {o['fleet_wafers_yr']/1e6:.1f}M DRAM wafers/yr")
    print("\n-- ENERGY --")
    print(f"Fab electricity: {v('kwh_per_wafer'):,.0f} kWh/wafer ({v('kwh_per_wafer',1):,.0f}-{v('kwh_per_wafer',2):,.0f}) "
          f"-> {o['kwh_per_gb']:.2f} kWh/GB ({o['kwh_per_gb_lo']:.2f}-{o['kwh_per_gb_hi']:.2f})")
    print(f"Electricity cost: ${o['elec_usd_per_wafer']:.0f}/wafer = {o['elec_share_wafer_cost']*100:.1f}% of wafer cost; "
          f"${o['elec_usd_per_wafer']/GB_PER_WAFER_1B:.3f}/GB")
    print(f"Fleet DRAM fab electricity: {o['fleet_twh']:.0f} TWh/yr (world electricity ~30,000 TWh -> "
          f"{o['fleet_twh']/30000*100:.2f}%)")
    print(f"Electricity CO2: {o['gco2_per_gb_elec']:.0f} gCO2/GB (literature embodied 63-65 gCO2e/GB -> see note)")
    print(f"EUV: {o['euv_kwh_per_exposure']:.1f} kWh/exposure; 6 EUV layers = {o['euv_kwh_per_wafer_6L']:.0f} kWh/wafer "
          f"= {o['euv_share_of_wafer_kwh']*100:.0f}% of wafer kWh")
    print(f"EUV tin: {o['tin_kg_per_tool_yr']:.0f} kg Sn/tool-yr (droplets, before recovery); 300 tools = "
          f"{o['tin_fleet_t']:.0f} t = {o['tin_share']*100:.3f}% of world tin")
    print(f"Use phase: {o['use_kwh_per_gb_life']:.1f} kWh/GB over {v('life_years'):.0f} yr at {v('use_w_per_gb')} W/GB "
          f"= {o['use_over_embodied']:.0f}x embodied fab electricity")
    print("\n-- WATER / SILICON --")
    print(f"Water: {v('m3_water_per_wafer'):.0f} m3/wafer ({v('m3_water_per_wafer',1):.0f}-{v('m3_water_per_wafer',2):.0f}) "
          f"-> {o['l_water_per_gb']:.1f} L/GB; ${o['water_usd_per_wafer']:.0f}/wafer "
          f"({o['water_usd_per_wafer']/WAFER_COST_1B*100:.1f}%); fleet {o['fleet_water_mm3_yr']:.0f} Mm3/yr gross")
    print(f"Silicon: {o['si_g_per_wafer']:.0f} g/wafer = {o['si_mg_per_gb']:.0f} mg Si/GB; fleet poly "
          f"{o['fleet_poly_t']:,.0f} t = {o['fleet_poly_share']*100:.0f}% of semi-grade poly; prime wafer "
          f"{o['wafer_share_wafer_cost']*100:.1f}% of wafer cost")
    print("\n-- CAPACITOR FILM AREA --")
    print(f"Pillar capacitor surface enhancement in array: {o['cap_enh']:.0f}x; dielectric area/wafer "
          f"{o['cap_area_m2']:.1f} m2 (wafer = 0.071 m2)")
    print("\n-- ELEMENTS: per wafer, fleet total vs world supply, cost share --")
    print(f"{'element / use':52s} {'dep g/wf':>9s} {'cons g/wf':>9s} {'fleet t/yr':>10s} {'% world':>8s} {'$/wafer':>8s} {'% wafer$':>8s}")
    for r in o["rows"]:
        usd = r["usd_wafer"]
        usd_s = "-" if usd != usd else f"{usd:,.1f}"
        pct_s = "-" if usd != usd else f"{usd / WAFER_COST_1B * 100:.2f}"
        print(f"{r['name']:52s} {fmt(r['dep_g'],3):>9s} {fmt(r['cons_g'],3):>9s} {fmt(r['fleet_t'],1):>10s} "
              f"{r['share']*100:8.2f} {usd_s:>8s} {pct_s:>8s}")
    print("\nNotes: 'dep' = mass left in the film; 'cons' = mass consumed incl. precursor/target waste. Hypothetical rows")
    print("assume the ENTIRE DRAM fleet adopts that cell; they bound the resource exposure of new concepts, not today's use.")


if __name__ == "__main__":
    main()
