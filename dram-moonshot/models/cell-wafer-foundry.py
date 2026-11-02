#!/usr/bin/env python3
"""
cell-wafer-foundry.py -- first-principles model for the CELL-WAFER FOUNDRY concept
(dossier key: dos-cell-wafer-foundry, dram-moonshot Stage 3, rank 9).

Concept: litho-light, purely periodic oxide cell wafers (vertical-bitline 3D stacks, no EUV)
hybrid-bonded at 1-2 um pitch to sense/decode periphery wafers from U.S. 22/28 nm logic
foundries, under an open bitline-group electrical bond spec.

What this model computes (pure stdlib; run from dram-moonshot/ with `python3 models/cell-wafer-foundry.py`):
  0. Reference 1-beta DDR5 anchors.
  1. Bond-grid closure: bitline-group mux ratio M forced by bond pitch, by word-line bonds and by the
     area of 28 nm sense amps, iterated self-consistently with the lateral capacitor length (1T1C)
     or with a fixed gain-cell footprint (2T0C-class portfolio cells).
  2. Die density, array efficiency, signal (mV), required Cs, read time, bitline energy.
  3. Bond-link yield with segment repair; particle-void yield (Tong-Gosele); overlay vs wafer bow
     (Stoney); bond-anneal thermal dose vs 85 C drift; bond pad parasitics.
  4. Cost per GB vs DDR5 ($1.48/GB), EUV $ removed, capex per GB/month, and the monolithic
     CMOS-under-array null hypothesis (what the bonded split has to beat).
  5. Sensitivity on the key unknown (bond-link failure probability x bond pitch) and on bow.
  6. Daisy-chain test-vehicle statistics and the GO/NO-GO line.

Every input carries a source URL / repo pointer or "ESTIMATE: basis". Output is printed and written to
research/stage3/cell-wafer-foundry_model_output.md.
"""
import math
import os
import sys

# ============================================================================================
# INPUTS  (value, source)
# ============================================================================================
INPUTS = {
    # ---- 1-beta DDR5 reference ----
    "ddr5_density_gbmm2": (0.447, "A1_scaling_limits.md s1 table: Micron D1b 16Gb 35.83 mm2 (TechInsights teardown via ram-venture cost_stack s3.1)"),
    "ddr5_cost_per_gb": (1.48, "ram-venture models/dram_cost_stack.py ($3.8k 1b wafer -> $1.48/GB)"),
    "ddr5_wafer_cost": (3800.0, "ram-venture models/dram_cost_stack.py (1b wafer)"),
    "ddr5_yield": (0.90, "ESTIMATE: mature DRAM die yield after repair; only used to back out wafer area utilisation"),
    "ddr5_cbl_fF": (35.0, "A1_scaling_limits.md s4 bitline table (512 cells/BL)"),
    "vary_V": (1.05, "models/dram_cell_physics.py INPUTS v_array"),
    "euv_layers_1c": ((5, 7), "A1_scaling_limits.md s0 #6: 5-7 EUV layers at 1c"),
    "euv_cost_per_layer": ((115.0, 165.0, 270.0), "models/dram_cell_physics.py s8 (EUV $/layer lo/base/hi)"),
    "wafer_1c_cost": (4308.0, "models/dram_cell_physics.py s8 ($4,308 1c wafer)"),
    "dram_capex_per_wpm": ((145e3, 157.5e3, 170e3), "A1 s5: greenfield ~$145-170k per wafer-start/month [UNVERIFIED rule of thumb]; Samsung P5 ~$147k/wpm cross-check (capitalandcompute.net)"),
    "wafer_area_mm2": (math.pi * 150.0 ** 2, "geometry: 300 mm wafer"),
    # ---- cell geometry: vertical-bitline (VBL) oxide stack ----
    "p_x_nm": (80.0, "FINAL_CONCEPTS.json: litho-light F ~40 nm -> 2F = 80 nm vertical-bitline pitch along the WL (A3 s2.9 table: 80 nm BL pitch); ArF single exposure or SADP, no EUV"),
    "L_fixed_nm": (200.0, "ESTIMATE: lateral oxide transistor + VBL contact + isolation along the row; A1 base 600 nm = ~400 nm cap + ~200 nm rest"),
    "cap_perim_nm": (150.0, "ESTIMATE: ~45 x 30 nm lateral capacitor cross-section inside an 80 nm-wide, ~60-75 nm-tall tier cell, single-sided"),
    "eot_nm": (0.55, "models/dram_cell_physics.py INPUTS eot_nm (ZrO2 stack, TechInsights/Choe)"),
    "L_gain_nm": (250.0, "ESTIMATE: 2T0C-class gain cell (write + read FET) laid laterally in one tier; footprint 80 x 250 nm = 0.02 um2"),
    "c_tier_fF": (0.08, "ESTIMATE: VBL capacitance per tier crossed; A1 planar 0.06 fF/cell (coupling-dominated) raised for a GAA WL wrap"),
    "c_off_fF": (0.04, "ESTIMATE: off-state bitline-group selector junction+overlap; B3-01 used 0.05 fF per off switch"),
    "c_wire_fF_per_um": (0.15, "B3-01 (ideas_master.json) global bitline 0.15 fF/um"),
    "c_sa_in_fF": (1.5, "B3-01 (ideas_master.json) SA input capacitance"),
    "c_via_stack_fF": (0.3, "ESTIMATE: via stack + redistribution from VBL selector to bond pad"),
    "k_sicn": (5.0, "ESTIMATE: SiCN/SiO2 bond dielectric relative permittivity ~4-5.5"),
    "pad_thick_um": (0.5, "ESTIMATE: bond pad Cu thickness"),
    "dv_cell_mV": (474.0, "FINAL_CONCEPTS.json cell-wafer-foundry: 'Cs = 26 mV x 11 fF/474 mV' (cell swing after droop)"),
    "dv_min_margin_mV": (26.0, "FINAL_CONCEPTS.json: MARGIN STACK sense threshold 26 mV"),
    "dv_min_conv_mV": (50.0, "models/dram_cell_physics.py INPUTS dv_min_mV (conventional SA)"),
    "i_read_uA": (2.0, "ESTIMATE: gain-cell read current; OCTRAM Ion >15 uA (A3 table, Kioxia/Nanya IEDM 2024) derated ~7x for a read FET at low overdrive"),
    "dv_sense_gain_mV": (100.0, "ESTIMATE: bitline swing to resolve a gain-cell read with an offset-cancelled SA"),
    "tiers_base": (64, "ESTIMATE: A1 s6 says 3D DRAM needs 32-192 tiers (SK hynix); 64 = mid case"),
    "die_gbit": (32.0, "ESTIMATE: a 32 Gb die (DDR5 roadmap capacity)"),
    "ecc": (1.0625, "models/dram_cell_physics.py INPUTS ecc_factor (DDR5 on-die ECC)"),
    # ---- periphery wafer (22/28 nm logic) and cell-side overheads ----
    "a_sa_um2": (2.5, "ESTIMATE: ~16-20 T offset-cancelled latch + precharge + column gate at 28 nm with matched (upsized) devices"),
    "a_wld_um2": (3.0, "ESTIMATE: ~3 V word-line driver in 28 nm thick-oxide (2.5/3.3 V) devices"),
    "periph_fixed_mm2": (3.0, "ESTIMATE: I/O, pads, pumps, control, fuses for a DDR5-class die"),
    "wl_len_um": (400.0, "ESTIMATE: per-tier WL segment length limited by WL RC (~10 ns rise) and page size"),
    "predecode": (8, "ESTIMATE: 1-of-8 oxide-TFT WL predecode on the cell wafer (one bond per 8 WLs)"),
    "stair_step_um": (0.5, "ESTIMATE: 3D-NAND-class staircase step per tier, one-sided per WL segment"),
    "periph_fill": (0.85, "ESTIMATE: max fraction of the array footprint the SA + WL-driver periphery may fill (rest hosts fixed periphery/routing)"),
    "cell_edge_frac": (0.08, "ESTIMATE: seal ring, bond keep-out and alignment marks (~3%) + oxide-TFT WL predecode/group-select drivers at the array edge (~5%)"),
    # ---- bonding ----
    "pitch_base_um": (1.5, "FINAL_CONCEPTS.json: 1-2 um bond pitch for VBL stacks"),
    "pad_frac": (0.5, "ESTIMATE: pad diameter = 0.5 x pitch (common hybrid-bond layout)"),
    "overlay_rule": (0.5, "arXiv 2511.05506 (YAP+): keep misalignment within 50% of bottom pad diameter"),
    "p_link_base": (1e-5, "FINAL_CONCEPTS.json key_unknown: <=~1e-5 failures per link required"),
    "p_short_ratio": (0.1, "ESTIMATE: pad-to-pad bridges per link relative to opens (bridges need >pitch/2 misalignment or a Cu particle/extrusion)"),
    "f_global": (0.25, "ESTIMATE: fraction of a signal pad's neighbours that are unswitched global supply pads when power pads are interleaved (no spec rule)"),
    "f_global_spec": (0.0, "ESTIMATE: under the proposed spec rule (signal pads neighbour only signal or domain-switched supply pads) a bridge costs one repair domain, not the die"),
    "repair_domain_groups": (4096, "ESTIMATE: bitline groups per repair domain (one subarray block)"),
    "spare_frac": (0.01, "FINAL_CONCEPTS.json: ~1% segment spares"),
    "E_prime_Pa": (1.63e11, "ESTIMATE: Si plane-strain modulus E/(1-nu^2), E~150 GPa, nu~0.28"),
    "biax_mod_Pa": (1.805e11, "Si(100) biaxial modulus E/(1-nu) ~180.5 GPa (Stoney formula standard value)"),
    "t_wafer_um": (775.0, "SEMI 300 mm wafer thickness"),
    "gamma_J_m2": ((0.1, 0.5, 1.0), "ESTIMATE: room-temperature surface energy of plasma-activated SiO2/SiCN before anneal (0.1) to near-anneal (1.0)"),
    "f_res": (0.10, "ESTIMATE: residual non-linear run-out after bonder scaling compensation (fraction of linear run-out)"),
    "film_t_um": (5.0, "FINAL_CONCEPTS.json key_unknown: ~5 um of stressed films on multi-tier oxide stack"),
    "film_sigma_MPa": ((100.0, 250.0, 500.0), "ESTIMATE: net film stress range for oxide/nitride/W tier stacks"),
    "Ea_eV": ((0.58, 0.72), "B3-20 (ideas_master.json) citing CPB 2015 IGZO recovery/stress barriers"),
    # ---- cost ----
    "periph_wafer_cost": ((1900.0, 2800.0, 3450.0), "ram-venture v4-cost: 28 nm wafer $2,800 (1.9-3.45k), TSMC ~$3.0k (siliconanalysts.com/data/wafer-pricing via snippet)"),
    "prime_wafer_cost": (115.0, "A2_materials_resources.md: prime 300 mm wafer ~$115"),
    "cell_base_cost": (700.0, "ESTIMATE: prime wafer $115 + selector tier + ~4 BEOL routing/redistribution layers + bond layer"),
    "tier_cost": ((20.0, 30.0, 45.0), "A1 s6 scenarios $20/$30/$45 per tier [ESTIMATE, low confidence]"),
    "d2w_extra_cost": (300.0, "ESTIMATE: extra D2W pick-and-place bonder time for ~4,000 x 13 mm2 dies per wafer vs one W2W bond"),
    "periph_capex_per_wpm": ((60e3, 80e3, 100e3), "ESTIMATE: new 28 nm logic capacity per wafer-start/month, only if existing capacity were not available"),
    "bond_cost_pair": (400.0, "ESTIMATE: W2W hybrid bond + pre-bond CMP/clean + thinning + pad reveal per wafer pair"),
    "mono_base_cost": (300.0, "ESTIMATE: routing/via layers to land a cell stack on top of a periphery wafer (CuA)"),
    "d0_periph_cm2": (0.10, "ESTIMATE within ASU ECO-CHIP defect_density 0.05-0.2/cm2 (github.com/ASU-VDA-Lab/ECO-CHIP)"),
    "periph_crit_frac": (0.5, "ESTIMATE: critical-area fraction of periphery not covered by SA/row redundancy"),
    "tier_yield_repaired": (0.998, "A1 s6: per-tier killer-defect probability must reach <=0.2% after repair"),
    "particle_density_cm2": (0.05, "ESTIMATE: >=0.5 um particles per cm2 on a fab-grade pre-bond surface; university-fab surfaces are likely 10-100x worse"),
    "cell_tool_intensity": (0.8, "ESTIMATE: capex per $ of processing for a dep/etch cell line relative to an EUV DRAM line"),
}


def V(k):
    return INPUTS[k][0]


EPS0 = 8.854e-12
KB_EV = 8.617e-5
OUT = []


def p(s=""):
    OUT.append(s)
    print(s)


def hr(t):
    p("")
    p("## " + t)
    p("")


def mid(x):
    return x[1] if isinstance(x, tuple) and len(x) == 3 else x


# ============================================================================================
# Physics helpers
# ============================================================================================
def c_area_fF_per_um2(eot_nm):
    return EPS0 * 3.9 / (eot_nm * 1e-9) * 1e15 / 1e12  # F/m2 -> fF/um2


def bond_pad_cap_fF(pitch_um):
    """Pad-to-4-neighbour coupling (parallel-plate on facing sidewalls) + via stack."""
    d = V("pad_frac") * pitch_um
    gap = pitch_um - d
    side = EPS0 * V("k_sicn") * (d * 1e-6 * V("pad_thick_um") * 1e-6) / (gap * 1e-6)
    return 4 * side * 1e15 * 1.5 + V("c_via_stack_fF")  # x1.5 fringe factor [ESTIMATE]


def wl_bond_density_per_um2(n_tiers, row_pitch_um):
    # one WL per tier per row, segment length wl_len, predecoded on the cell wafer
    return n_tiers / (row_pitch_um * V("wl_len_um") * V("predecode"))


def solve_group(cell, n_tiers, pitch_um, dv_min_mV=None, max_iter=60, a_sa=None):
    """Self-consistent bitline-group closure.
    cell: '1T1C' (lateral capacitor sized to the sense criterion) or 'GAIN' (fixed footprint).
    Returns dict or None if infeasible."""
    px = V("p_x_nm") * 1e-3
    dv_min = dv_min_mV if dv_min_mV is not None else V("dv_min_margin_mV")
    L_cap = 0.4  # um, start
    res = None
    for _ in range(max_iter):
        row = (V("L_fixed_nm") * 1e-3 + L_cap) if cell == "1T1C" else V("L_gain_nm") * 1e-3
        a_fp = px * row  # um2 footprint per vertical bitline (= per cell per tier)
        n_wl = wl_bond_density_per_um2(n_tiers, row)  # WL bonds per um2 of array
        site = 1.0 / pitch_um ** 2
        if n_wl >= site:
            return None
        m_bond = 1.0 / (a_fp * (site - n_wl))
        # periphery area under the array must fit: a_sa/(M a_fp) + a_wld*n_wl <= 1 (fixed periphery handled at die level)
        avail = V("periph_fill") - V("a_wld_um2") * n_wl
        if avail <= 0.05:
            return None
        a_sa_v = V("a_sa_um2") if a_sa is None else a_sa
        m_sa = a_sa_v / (a_fp * avail)
        M = max(1, math.ceil(max(m_bond, m_sa)))
        # global line length: non-destructive cells may cluster; destructive 1T1C must group VBLs in rows
        # not crossed by the active WL -> the group spans M rows.
        L_glob = math.sqrt(M * a_fp) if cell == "GAIN" else M * row
        c_bond = bond_pad_cap_fF(pitch_um)
        cbl = n_tiers * V("c_tier_fF") + (M - 1) * V("c_off_fF") + L_glob * V("c_wire_fF_per_um") + c_bond + V("c_sa_in_fF")
        if cell == "1T1C":
            cs = dv_min * cbl / (V("dv_cell_mV") - dv_min)
            L_new = cs / (c_area_fF_per_um2(V("eot_nm")) * V("cap_perim_nm") * 1e-3)
            res = dict(a_fp=a_fp, row=row, M=M, m_bond=m_bond, m_sa=m_sa, n_wl=n_wl, cbl=cbl, cs=cs, L_cap=L_new, a_sa=a_sa_v,
                       c_bond=c_bond, L_glob=L_glob, limiter="bond" if m_bond >= m_sa else "SA area")
            if abs(L_new - L_cap) < 1e-4:
                break
            L_cap = 0.5 * (L_cap + L_new)
        else:
            t_read_ns = cbl * 1e-15 * V("dv_sense_gain_mV") * 1e-3 / (V("i_read_uA") * 1e-6) * 1e9
            res = dict(a_fp=a_fp, row=row, M=M, m_bond=m_bond, m_sa=m_sa, n_wl=n_wl, cbl=cbl, cs=0.0, L_cap=0.0, a_sa=a_sa_v,
                       c_bond=c_bond, L_glob=L_glob, t_read_ns=t_read_ns, limiter="bond" if m_bond >= m_sa else "SA area")
            break
    return res


def die_model(g, n_tiers):
    bits = V("die_gbit") * 1e9 * V("ecc")
    array_mm2 = bits * g["a_fp"] / n_tiers * 1e-6
    stair = n_tiers * V("stair_step_um") / V("wl_len_um")
    cell_side = array_mm2 * (1 + stair + V("cell_edge_frac"))
    periph_frac = g["a_sa"] / (g["M"] * g["a_fp"]) + V("a_wld_um2") * g["n_wl"]
    periph_side = array_mm2 * periph_frac + V("periph_fixed_mm2")
    die = max(cell_side, periph_side)
    n_sig_bonds = array_mm2 * 1e6 / (g["M"] * g["a_fp"])
    n_wl_bonds = array_mm2 * 1e6 * g["n_wl"]
    return dict(array_mm2=array_mm2, die_mm2=die, eff=array_mm2 / die, dens=V("die_gbit") / die,
                stair=stair, periph_frac=periph_frac, cell_side=cell_side, periph_side=periph_side,
                n_sig=n_sig_bonds, n_wl=n_wl_bonds, die_limiter="cell side" if cell_side >= periph_side else "periphery side")


def poisson_cdf(k, lam):
    s, term = 0.0, math.exp(-lam)
    for i in range(0, k + 1):
        if i > 0:
            term *= lam / i
        s += term
    return min(1.0, s)


def short_yield(n_links, p_link, f_global=None):
    """Bridges onto an unswitched global supply are die-fatal (not repairable)."""
    fg = V("f_global_spec") if f_global is None else f_global
    return math.exp(-n_links * p_link * V("p_short_ratio") * fg)


def link_yield(n_links, p_link, spare_frac=None, G=None):
    G = G or V("repair_domain_groups")
    sf = V("spare_frac") if spare_frac is None else spare_frac
    S = int(math.floor(sf * G))
    lam = G * p_link
    pok = poisson_cdf(S, lam)
    n_dom = n_links / G
    if pok >= 1.0:
        return 1.0
    return math.exp(n_dom * math.log(max(pok, 1e-300)))


def void_radius_mm(h_um, gamma):
    """Tong-Gosele: unbonded radius around a particle of height h (thick-wafer regime, valid when R > 2 t_w)."""
    t = V("t_wafer_um") * 1e-6
    R = (2 * V("E_prime_Pa") * t ** 3 / (3 * gamma)) ** 0.25 * math.sqrt(h_um * 1e-6)
    return R * 1e3


def void_yield(die_mm2, R_mm, d_cm2, w2w=True):
    if w2w:
        a_kill = (math.sqrt(die_mm2) + 2 * R_mm) ** 2 / 100.0
    else:  # D2W: a void cannot extend beyond the die that carries the particle
        a_kill = die_mm2 / 100.0
    return math.exp(-d_cm2 * a_kill)


def runout_um(bow_um, r_mm=150.0):
    """Uncompensated run-out at radius r when a bowed wafer is flattened against a flat one: Delta = b * t / r."""
    return bow_um * V("t_wafer_um") * 1e-6 / (r_mm * 1e-3)


def bow_from_film_um(sigma_MPa, t_um, r_mm=150.0):
    kappa = 6 * sigma_MPa * 1e6 * t_um * 1e-6 / (V("biax_mod_Pa") * (V("t_wafer_um") * 1e-6) ** 2)
    return kappa * (r_mm * 1e-3) ** 2 / 2 * 1e6


def periph_yield(die_mm2):
    return math.exp(-V("d0_periph_cm2") * die_mm2 / 100.0 * V("periph_crit_frac"))


def utilisation():
    gb_per_wafer = V("ddr5_wafer_cost") / V("ddr5_cost_per_gb")
    area_used = gb_per_wafer * 8 / V("ddr5_density_gbmm2")
    return area_used / V("wafer_area_mm2") / V("ddr5_yield"), gb_per_wafer


def cost_per_gb(die, n_tiers, p_link, pitch, tier_cost=None, periph_cost=None, particle=None, d2w=False, f_global=None):
    util, _ = utilisation()
    tc = mid(V("tier_cost")) if tier_cost is None else tier_cost
    pc = mid(V("periph_wafer_cost")) if periph_cost is None else periph_cost
    c_cell = V("cell_base_cost") + n_tiers * tc
    c_pair = c_cell + pc + V("bond_cost_pair")
    y_cell = V("tier_yield_repaired") ** n_tiers
    y_per = periph_yield(die["die_mm2"])
    y_link = link_yield(die["n_sig"] + die["n_wl"], p_link) * short_yield(die["n_sig"] + die["n_wl"], p_link, f_global)
    R = void_radius_mm(0.5, 0.5)
    y_void = void_yield(die["die_mm2"], R, V("particle_density_cm2") if particle is None else particle, w2w=not d2w)
    gb = V("wafer_area_mm2") * util * die["dens"] / 8.0
    if d2w:
        # known-good-die: discard bad halves before bonding; pay each half / its own yield
        good_cost = c_cell / y_cell + pc / y_per + V("bond_cost_pair") + V("d2w_extra_cost")
        y = y_link * y_void
        return (good_cost / (gb * y) if y > 1e-9 else float("inf")), dict(y_cell=y_cell, y_per=y_per, y_link=y_link, y_void=y_void, y=y, c_pair=c_pair)
    y = y_cell * y_per * y_link * y_void
    return (c_pair / (gb * y) if y > 1e-9 else float("inf")), dict(y_cell=y_cell, y_per=y_per, y_link=y_link, y_void=y_void, y=y, c_pair=c_pair)


def ucl95_poisson(k, n):
    """One-sided 95% upper confidence bound on p from k failures in n trials (Poisson, bisection on CDF)."""
    lo, hi = 0.0, max(10.0, 3.0 * (k + 1) + 10 * math.sqrt(k + 1))
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if poisson_cdf(k, m) > 0.05:
            lo = m
        else:
            hi = m
    return hi / n


# ============================================================================================
# Sections
# ============================================================================================
def s0_reference():
    hr("0. Reference anchors (1-beta DDR5)")
    util, gbw = utilisation()
    e_bl = 0.5 * V("ddr5_cbl_fF") * V("vary_V") ** 2
    p(f"- 1b DDR5: {V('ddr5_density_gbmm2')} Gb/mm2, ${V('ddr5_cost_per_gb')}/GB on a ${V('ddr5_wafer_cost'):,.0f} wafer -> {gbw:,.0f} good GB per wafer")
    p(f"- Implied usable-area utilisation (edge, scribe, packing) at {V('ddr5_yield'):.0%} yield: {util:.3f} (reused for bonded dies)")
    p(f"- Bitline energy per sensed bit at Cbl {V('ddr5_cbl_fF'):.0f} fF, VARY {V('vary_V')} V: 0.5*C*V^2 = {e_bl:.1f} fJ")
    lo = V("euv_layers_1c")[0] * V("euv_cost_per_layer")[1]
    hi = V("euv_layers_1c")[1] * V("euv_cost_per_layer")[1]
    p(f"- EUV at 1c: {V('euv_layers_1c')[0]}-{V('euv_layers_1c')[1]} layers x ${V('euv_cost_per_layer')[1]:.0f} = ${lo:,.0f}-{hi:,.0f}/wafer "
      f"({lo / V('wafer_1c_cost') * 100:.0f}-{hi / V('wafer_1c_cost') * 100:.0f}% of a ${V('wafer_1c_cost'):,.0f} 1c wafer). The cell wafer here uses 0 EUV layers; 22/28 nm periphery uses 0.")
    return util, gbw, e_bl


def s1_planar():
    hr("1. Why the first merchant cell wafer must be 3D (planar route check)")
    F = 40.0
    a = 4 * F * F * 1e-6  # um2
    for eff in (0.70, 0.85):
        d = 1.0 / a * 1e6 / 1e9 * eff / V("ecc")
        p(f"- Planar oxide 4F2 at F = {F:.0f} nm, array eff {eff:.2f}: {d:.3f} Gb/mm2 = {d / V('ddr5_density_gbmm2'):.2f}x 1b")
    cbl = 11.0
    cs = V("dv_min_margin_mV") * cbl / (V("dv_cell_mV") - V("dv_min_margin_mV"))
    p(f"- Planar bonded periphery via 8-32:1 array-side mux sees Cbl ~{cbl:.0f} fF; with MARGIN STACK ({V('dv_min_margin_mV'):.0f} mV) Cs >= {cs:.2f} fF (concept text: 0.6 fF)")
    p("- => A litho-light (F~40 nm, no EUV) planar cell wafer gives only ~0.2-0.3x 1b density. The density must come from tiers: the split only")
    p("  pays as a vertical-bitline 3D cell wafer, which is what the rest of this model assumes.")


def s2_closure():
    hr("2. Bond-grid closure: bitline-group mux ratio, Cbl, Cs, die density (vertical-bitline 3D stack)")
    p(f"Die = {V('die_gbit'):.0f} Gb user. MARGIN STACK threshold {V('dv_min_margin_mV'):.0f} mV, cell swing {V('dv_cell_mV'):.0f} mV. "
      f"Cap density at EOT {V('eot_nm')} nm = {c_area_fF_per_um2(V('eot_nm')):.1f} fF/um2. WL predecode 1:{V('predecode')} on the cell wafer, WL segment {V('wl_len_um'):.0f} um. "
      f"SA {V('a_sa_um2')} um2, periphery may fill {V('periph_fill'):.0%} of the array footprint.")
    p("")
    p("| cell | tiers | pitch um | M (bond / SA-area) | limiter | Cbl fF | Cs fF | cap L nm | footprint um2 | read ns | array mm2 | die mm2 | arr eff | Gb/mm2 | x1b |")
    p("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    table = {}
    for cell in ("1T1C", "GAIN"):
        for nt in (16, 32, 64, 128):
            for pitch in (1.0, 1.5, 2.0):
                g = solve_group(cell, nt, pitch)
                if g is None:
                    p(f"| {cell} | {nt} | {pitch} | infeasible (WL bonds exceed sites) | | | | | | | | | | | |")
                    continue
                d = die_model(g, nt)
                table[(cell, nt, pitch)] = (g, d)
                rd = f"{g['t_read_ns']:.2f}" if cell == "GAIN" else "-"
                cs = f"{g['cs']:.2f}" if cell == "1T1C" else "-"
                cl = f"{g['L_cap'] * 1e3:.0f}" if cell == "1T1C" else "-"
                p(f"| {cell} | {nt} | {pitch} | {g['M']} ({g['m_bond']:.0f}/{g['m_sa']:.0f}) | {g['limiter']} | {g['cbl']:.1f} | {cs} | "
                  f"{cl} | {g['a_fp']:.4f} | {rd} | {d['array_mm2']:.1f} | {d['die_mm2']:.1f} | {d['eff']:.2f} | {d['dens']:.2f} | {d['dens'] / V('ddr5_density_gbmm2'):.1f} |")
    p("")
    g, d = table[("1T1C", 64, 1.5)]
    p(f"Base case (1T1C, 64 tiers, 1.5 um): M = {g['M']} ({g['limiter']}-limited), Cbl = {g['cbl']:.1f} fF (bond pad {g['c_bond']:.2f} fF, global line {g['L_glob']:.0f} um "
      f"= {g['L_glob'] * V('c_wire_fF_per_um'):.1f} fF, off selectors {(g['M'] - 1) * V('c_off_fF'):.1f} fF, tiers {64 * V('c_tier_fF'):.1f} fF), "
      f"Cs = {g['cs']:.2f} fF -> lateral cap {g['L_cap'] * 1e3:.0f} nm; die {d['die_mm2']:.1f} mm2 ({d['die_limiter']}-limited), "
      f"array efficiency {d['eff']:.2f}, {d['dens']:.2f} Gb/mm2 = {d['dens'] / V('ddr5_density_gbmm2'):.1f}x 1b.")
    p(f"Staircase overhead {d['stair'] * 100:.0f}%, SA+WL-driver periphery fills {d['periph_frac'] * 100:.0f}% of the array footprint (+{V('periph_fixed_mm2'):.0f} mm2 fixed). "
      f"Signal bonds {d['n_sig']:.2e}, WL bonds {d['n_wl']:.2e} per die.")
    g2, d2 = table[("GAIN", 64, 1.5)]
    p(f"Gain-cell case (64 tiers, 1.5 um): M = {g2['M']}, Cbl = {g2['cbl']:.1f} fF, read time to {V('dv_sense_gain_mV'):.0f} mV at {V('i_read_uA'):.0f} uA = {g2['t_read_ns']:.2f} ns; "
      f"{d2['dens']:.2f} Gb/mm2 = {d2['dens'] / V('ddr5_density_gbmm2'):.1f}x 1b, array eff {d2['eff']:.2f}.")
    p("")
    p("Sensitivity of the base case to the 28 nm SA footprint and to the sense threshold (1T1C, 64 tiers, 1.5 um):")
    p("| SA um2 | dv_min mV | M | limiter | Cbl fF | Cs fF | cap L nm | Gb/mm2 | x1b |")
    p("|---|---|---|---|---|---|---|---|---|")
    for asa in (1.0, 2.5, 5.0):
        for dv in (V("dv_min_margin_mV"), V("dv_min_conv_mV")):
            gg = solve_group("1T1C", 64, 1.5, dv_min_mV=dv, a_sa=asa)
            dd = die_model(gg, 64)
            p(f"| {asa} | {dv:.0f} | {gg['M']} | {gg['limiter']} | {gg['cbl']:.1f} | {gg['cs']:.2f} | {gg['L_cap'] * 1e3:.0f} | {dd['dens']:.2f} | {dd['dens'] / V('ddr5_density_gbmm2'):.1f} |")
    p("")
    m1 = table[("1T1C", 64, 1.0)][0]
    p("Findings:")
    p(f"- At 1.0 um pitch the mux ratio is still {m1['M']} because a ~{V('a_sa_um2')} um2 28 nm sense amp needs that much array area above it")
    p("  (SA-area limit). Finer bonding than ~1.5 um buys nothing until the periphery node shrinks: 1-2 um bonding is matched to 22/28 nm.")
    p("- Destructive-read 1T1C must group vertical bitlines that the active WL does not cross (a row-direction mux), so the global line")
    p("  spans M rows and dominates Cbl. Non-destructive gain cells can cluster any M bitlines under one bond, so their line is ~1-2 um and")
    p("  the read time is ~1 ns. The open spec should favour non-destructive (gain/AND/PIXEL) cells or mandate WL segmentation for 1T1C.")
    p("- Word-line bonds are a first-order bond-site consumer: without on-cell-wafer predecode (1:8 here) they exceed the signal bonds.")
    p("- MARGIN STACK matters: at a conventional 50 mV threshold the base-case Cs roughly doubles (longer lateral capacitor, lower density).")
    return table


def s3_pitch_ceiling(table):
    hr("3. How coarse can the bond pitch get before the concept breaks?")
    p("| pitch um | 1T1C-64: M | Cbl fF | Cs fF | Gb/mm2 | x1b | GAIN-64: M | Cbl fF | read ns | Gb/mm2 |")
    p("|---|---|---|---|---|---|---|---|---|---|")
    ceil_1t1c, ceil_gain = None, None
    for pitch in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
        g = solve_group("1T1C", 64, pitch)
        h = solve_group("GAIN", 64, pitch)
        c1 = c2 = "infeasible"
        if g is not None:
            d = die_model(g, 64)
            if ceil_1t1c is None and (g["cs"] > 2.0 or d["dens"] < 1.5 * V("ddr5_density_gbmm2")):
                ceil_1t1c = pitch
            c1 = f"{g['M']} | {g['cbl']:.1f} | {g['cs']:.2f} | {d['dens']:.2f} | {d['dens'] / V('ddr5_density_gbmm2'):.1f}"
        else:
            ceil_1t1c = ceil_1t1c or pitch
            c1 = "infeasible | | | |"
        if h is not None:
            e = die_model(h, 64)
            if ceil_gain is None and (h["t_read_ns"] > 5.0 or h["cbl"] > 50.0):
                ceil_gain = pitch
            c2 = f"{h['M']} | {h['cbl']:.1f} | {h['t_read_ns']:.2f} | {e['dens']:.2f}"
        else:
            ceil_gain = ceil_gain or pitch
            c2 = "infeasible | | |"
        p(f"| {pitch} | {c1} | {c2} |")
    p("")
    p(f"- 1T1C breaks (Cs > 2 fF or density < 1.5x 1b at 64 tiers) at ~{ceil_1t1c} um pitch.")
    p(f"- Gain cells break (read > 5 ns, Cbl > 50 fF, or WL bonds exhaust the sites) at ~{ceil_gain} um: the WL-bond demand, not the signal,")
    p("  sets their ceiling (a 1:16-1:64 TFT predecode on the cell wafer would lift it).")
    p("- The A3 kill condition 'a floor that forces >2 um' is therefore too strict: the concept tolerates up to ~2-2.5 um, with a density")
    p("  and Cs penalty above 2 um.")
    return ceil_1t1c, ceil_gain


def s4_parasitics_energy(table, e_bl_ref):
    hr("4. Bond parasitics and bitline energy")
    for pitch in (1.0, 1.5, 2.0):
        c = bond_pad_cap_fF(pitch)
        d = V("pad_frac") * pitch
        r = 1.7e-8 * V("pad_thick_um") * 1e-6 / (math.pi * (d * 1e-6 / 2) ** 2) * 2
        p(f"- {pitch} um pitch: pad {d:.2f} um, pad+via capacitance ~{c:.2f} fF, Cu bulk resistance of two pads ~{r * 1e3:.0f} mOhm (+ interface, Kelvin-measured)")
    g, _ = table[("1T1C", 64, 1.5)]
    h, _ = table[("GAIN", 64, 1.5)]
    p(f"- Bond capacitance is {g['c_bond'] / g['cbl'] * 100:.0f}% of the 1T1C Cbl and {h['c_bond'] / h['cbl'] * 100:.0f}% of the gain-cell Cbl at 1.5 um; series R is <0.1 Ohm vs kOhm bitlines.")
    p("  Bond parasitics are NOT the risk; the post-raise 'sense margin vs bond parasitics' step can be emulated on-chip and descoped.")
    for name, gg in (("1T1C-64 @1.5um", g), ("GAIN-64 @1.5um", h)):
        e = 0.5 * gg["cbl"] * V("vary_V") ** 2
        p(f"- {name}: bitline energy 0.5*Cbl*VARY^2 = {e:.1f} fJ per sensed bit vs {e_bl_ref:.1f} fJ in 1b DDR5 ({e_bl_ref / e:.1f}x lower; same ratio for refresh array energy)")


def s5_yield(table):
    hr("5. Yield physics: bond links with repair, shorts, particle voids, overlay vs bow, anneal thermal dose")
    g, d = table[("1T1C", 64, 1.5)]
    n = d["n_sig"] + d["n_wl"]
    p(f"Links per die (1T1C-64 @1.5 um): {n:.2e}. Opens are repaired with {V('spare_frac'):.0%} spare groups per domain of {V('repair_domain_groups')}; "
      f"bridges = {V('p_short_ratio')} x opens; without the spec rule {V('f_global'):.0%} of them land on an unswitched global supply (die-fatal). "
      f"Cost sections assume the spec rule (domain-switched supplies).")
    p("")
    p("| p_link (opens) | dead links/die | open yield, 1% spares | 0.25% spares | no repair | fatal-short yield (global supply adjacent) | with domain power switches |")
    p("|---|---|---|---|---|---|---|")
    for pl in (1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 3e-3, 1e-2):
        p(f"| {pl:.0e} | {n * pl:,.1f} | {link_yield(n, pl):.4f} | {link_yield(n, pl, 0.0025):.4f} | {math.exp(-n * pl):.1e} | {short_yield(n, pl, V('f_global')):.4f} | {short_yield(n, pl):.4f} |")
    cliff = {}
    for sf in (0.01, 0.0025):
        for pl in [10 ** (-7 + 0.05 * i) for i in range(120)]:
            if link_yield(n, pl, sf) < 0.9:
                cliff[sf] = pl
                break
    pl_short = None
    for pl in [10 ** (-9 + 0.05 * i) for i in range(160)]:
        if short_yield(n, pl, V('f_global')) < 0.95:
            pl_short = pl
            break
    p("")
    p(f"- Opens: repair keeps yield >0.9 up to ~{cliff.get(0.01, float('nan')):.0e}/link with 1% spares (~{cliff.get(0.0025, float('nan')):.0e} with 0.25%); without repair a die needs <~1e-8.")
    p(f"- Bridges onto global supplies are the real yield term: at the assumed ratios, die yield falls below 0.95 once opens exceed ~{pl_short:.0e}/link.")
    p("  Spec rule: every signal pad's neighbours are signal pads or domain-switched supplies, so a bridge costs one repair domain, not the die.")
    p("  With that rule, link yield is limited only by spare exhaustion. The experiment must measure opens (daisy chains) AND bridges (combs).")
    p("")
    p("Particle voids (Tong-Gosele thick-wafer formula, 775 um wafers):")
    p("| particle h um | R void mm (gamma 0.1) | (0.5) | (1.0) | W2W die yield @0.05/cm2 | @0.5/cm2 | D2W die yield @0.5/cm2 |")
    p("|---|---|---|---|---|---|---|")
    for h in (0.1, 0.3, 0.5, 1.0):
        rs = [void_radius_mm(h, gm) for gm in V("gamma_J_m2")]
        yw1 = void_yield(d["die_mm2"], rs[1], 0.05)
        yw2 = void_yield(d["die_mm2"], rs[1], 0.5)
        yd = void_yield(d["die_mm2"], rs[1], 0.5, w2w=False)
        p(f"| {h} | {rs[0]:.1f} | {rs[1]:.1f} | {rs[2]:.1f} | {yw1:.3f} | {yw2:.3f} | {yd:.3f} |")
    p("- A 0.5 um particle unbonds a ~2-3 mm radius: in W2W one particle kills several small dies. Fab-grade pre-bond cleanliness")
    p("  (<~0.05 particles/cm2) is mandatory; university-fab coupons must get partner CMP+clean, and a D2W split confines voids to one die.")
    p("  (Formula valid for R > 2 t_w = 1.55 mm; smaller particles fall in the local-deformation regime and are overestimated here.)")
    p("")
    p("Overlay vs wafer bow (Stoney + flattening run-out Delta = b * t / r at r = 150 mm):")
    p("| net film stress MPa (x5 um) | bow um | uncompensated run-out um | residual @f_res 0.10 | @0.25 | allowed @1.0 / 1.5 / 2.0 um pitch |")
    p("|---|---|---|---|---|---|")
    allowed = [V("overlay_rule") * V("pad_frac") * pp for pp in (1.0, 1.5, 2.0)]
    for s in (25.0, 50.0) + V("film_sigma_MPa"):
        b = bow_from_film_um(s, V("film_t_um"))
        ro = runout_um(b)
        p(f"| {s:.0f} | {b:.0f} | {ro:.2f} | {ro * 0.10:.2f} | {ro * 0.25:.2f} | {allowed[0]:.2f} / {allowed[1]:.2f} / {allowed[2]:.2f} |")
    bmax10 = allowed[1] / 0.10 * (150e-3) / (V("t_wafer_um") * 1e-6)
    bmax25 = allowed[1] / 0.25 * (150e-3) / (V("t_wafer_um") * 1e-6)
    p(f"- At 1.5 um pitch (pad {V('pad_frac') * 1.5:.2f} um) the overlay budget is {allowed[1]:.3f} um (50% of pad). With 10% residual after scaling compensation the")
    p(f"  pair tolerates ~{bmax10:.0f} um of bow mismatch; at 25% residual only ~{bmax25:.0f} um. A 5 um film at 100-500 MPa bows ~300-1,600 um")
    p("  (matching the +300/-550 um seen on 3D NAND wafers), so backside stress compensation to <~200 um bow is the process requirement.")
    p("")
    p("Bond-anneal thermal dose expressed as equivalent time at 85 C (Arrhenius):")
    p("| anneal | Ea 0.58 eV | Ea 0.72 eV |")
    p("|---|---|---|")
    doses = {}
    for T, hrs in ((150, 2), (200, 2), (250, 2), (300, 2), (350, 2), (350, 16)):
        cols = []
        for ea in V("Ea_eV"):
            af = math.exp(ea / KB_EV * (1 / 358.15 - 1 / (T + 273.15)))
            yrs = af * hrs / 8766
            doses[(T, hrs, ea)] = yrs
            cols.append(f"{yrs:.2f} yr (AF {af:,.0f})")
        p(f"| {T} C x {hrs} h | {cols[0]} | {cols[1]} |")
    e0, e1 = V("Ea_eV")
    p(f"- 200 C / 2 h = {doses[(200, 2, e0)]:.2f}-{doses[(200, 2, e1)]:.2f} yr at 85 C; 250 C / 2 h = {doses[(250, 2, e0)]:.2f}-{doses[(250, 2, e1)]:.2f} yr; "
      f"350 C / 16 h = {doses[(350, 16, e0)]:.0f}-{doses[(350, 16, e1)]:.0f} yr.")
    p("  If the cell's 85 C drift is pre-characterised, the bond-induced shift is predictable. Keep the anneal <=250 C (Cu/SiCN bonding at")
    p("  180 C has been reported) so the bond consumes <~0.4 yr of the 10-yr drift budget.")


def s6_cost(table, util, gbw):
    hr("6. Cost per GB, EUV removed, capex, and the monolithic null hypothesis")
    p(f"Cell wafer = ${V('cell_base_cost'):.0f} + tiers x $/tier; periphery 28 nm = ${mid(V('periph_wafer_cost')):,.0f}; bond+thin = ${V('bond_cost_pair'):.0f} per pair "
      f"(D2W +${V('d2w_extra_cost'):.0f}); per-tier repaired yield {V('tier_yield_repaired')}; p_link {V('p_link_base'):.0e}; particles {V('particle_density_cm2')}/cm2.")
    p("")
    p("| cell | tiers | pitch | Gb/mm2 | wafer-pair $ | periphery share | Y total | $/GB W2W | x DDR5 | $/GB D2W (KGD) | $/GB @$20/tier | @$45/tier | @$1.9k periphery |")
    p("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    res = {}
    for cell in ("1T1C", "GAIN"):
        for nt in (16, 32, 64, 128):
            key = (cell, nt, 1.5)
            if key not in table:
                continue
            g, d = table[key]
            c, y = cost_per_gb(d, nt, V("p_link_base"), 1.5)
            cd, _ = cost_per_gb(d, nt, V("p_link_base"), 1.5, d2w=True)
            clo, _ = cost_per_gb(d, nt, V("p_link_base"), 1.5, tier_cost=20.0)
            chi, _ = cost_per_gb(d, nt, V("p_link_base"), 1.5, tier_cost=45.0)
            cpl, _ = cost_per_gb(d, nt, V("p_link_base"), 1.5, periph_cost=V("periph_wafer_cost")[0])
            res[key] = (c, y)
            p(f"| {cell} | {nt} | 1.5 | {d['dens']:.2f} | {y['c_pair']:,.0f} | {mid(V('periph_wafer_cost')) / y['c_pair']:.0%} | {y['y']:.3f} | {c:.2f} | {c / V('ddr5_cost_per_gb'):.2f} | {cd:.2f} | {clo:.2f} | {chi:.2f} | {cpl:.2f} |")
    p("")
    for cell in ("1T1C", "GAIN"):
        be = None
        for nt in range(4, 257, 4):
            g = solve_group(cell, nt, 1.5)
            if g is None:
                continue
            d = die_model(g, nt)
            c, _ = cost_per_gb(d, nt, V("p_link_base"), 1.5)
            if c <= V("ddr5_cost_per_gb"):
                be = (nt, c, d["dens"])
                break
        best = None
        for nt in range(8, 257, 8):
            g = solve_group(cell, nt, 1.5)
            if g is None:
                continue
            d = die_model(g, nt)
            c, _ = cost_per_gb(d, nt, V("p_link_base"), 1.5)
            if best is None or c < best[1]:
                best = (nt, c)
        bes = f"cost break-even with 1b DDR5 at {be[0]} tiers (${be[1]:.2f}/GB, {be[2]:.2f} Gb/mm2)" if be else "no break-even up to 256 tiers"
        p(f"- {cell}: {bes}; minimum ${best[1]:.2f}/GB ({best[1] / V('ddr5_cost_per_gb'):.2f}x DDR5) at ~{best[0]} tiers, where {V('tier_yield_repaired')}^N tier yield bites")
    p("- At <=64 tiers the 28 nm periphery wafer is the largest single cost line (~half the pair): a reduced-metal periphery flow is worth")
    p("  as much as ~30 tiers of cell process. These $/GB figures are CONDITIONAL on a portfolio cell reaching the tier count at 0.998")
    p("  repaired tier yield and ~$30/tier -- the cell's risk, not the bond's.")
    p("")
    p("Monolithic CMOS-under-array (oxide cells built directly on the periphery wafer, no bond) is the null hypothesis:")
    extra = V("cell_base_cost") + V("bond_cost_pair") - V("mono_base_cost")
    for nt in (32, 64, 128):
        need = extra / nt
        p(f"- {nt} tiers: the bonded split costs ${extra:.0f}/wafer more (second substrate + bond) -> the cell line must be >= ${need:.1f}/tier cheaper "
          f"than the same tier in a logic foundry's BEOL ({need / mid(V('tier_cost')) * 100:.0f}% of a ${mid(V('tier_cost')):.0f} tier)")
    p("- W2W yield equals monolithic yield (no known-good selection); only D2W/KGD gives a yield advantage. The split's real case is tool")
    p("  specialisation (NAND-class high-AR etch/ALD tools logic fabs lack), parallel cycle time, >400 C or H-rich cell steps the periphery")
    p("  cannot see, and a merchant market -- not physics. This is the honest weak point of the concept and should be priced in.")
    p("")
    g, d = table[("1T1C", 64, 1.5)]
    c, y = res[("1T1C", 64, 1.5)]
    gb_pair = V("wafer_area_mm2") * util * d["dens"] / 8.0 * y["y"]
    c_cell = V("cell_base_cost") + 64 * mid(V("tier_cost"))
    capex_cell_wpm = mid(V("dram_capex_per_wpm")) * c_cell / V("ddr5_wafer_cost") * V("cell_tool_intensity")
    cap_ref = mid(V("dram_capex_per_wpm")) / gbw
    cap_cell = capex_cell_wpm / gb_pair
    cap_per = [x / gb_pair for x in (V("periph_capex_per_wpm")[0], V("periph_capex_per_wpm")[2])]
    p(f"Capex (1T1C-64 @1.5 um): {gb_pair:,.0f} good GB per wafer pair vs {gbw:,.0f} for 1b.")
    p(f"- DRAM greenfield: ${mid(V('dram_capex_per_wpm')) / 1e3:.0f}k/wpm / {gbw:,.0f} GB = ${cap_ref:.0f} per GB/month of capacity")
    p(f"- Cell line (capex scaled to cell-wafer processing $ x {V('cell_tool_intensity')} tool intensity): ${capex_cell_wpm / 1e3:.0f}k/wpm / {gb_pair:,.0f} GB = ${cap_cell:.1f} per GB/month "
      f"({cap_ref / cap_cell:.0f}x less new memory-fab capex, mostly from tier density). Periphery: {1e6 / gb_pair:,.0f} existing 28 nm logic wafers/month per 1M GB/month;"
      f" if that logic capacity had to be built new, add ${cap_per[0]:.1f}-{cap_per[1]:.1f} per GB/month.")
    p(f"- EUV: 0 layers on either wafer vs 5-7 at 1c (${5 * V('euv_cost_per_layer')[1]:,.0f}-{7 * V('euv_cost_per_layer')[1]:,.0f}/wafer avoided).")
    p(f"- Reusable glass carrier (N-36) instead of a prime cell substrate saves at most ~${V('prime_wafer_cost'):.0f}/pair ({V('prime_wafer_cost') / y['c_pair'] * 100:.1f}% of pair cost): a resource win, not a cost win.")
    return res


def s7_sensitivity(table):
    hr("7. Sensitivity on the key unknown: bond-link failure probability x bond pitch (1T1C, 64 tiers)")
    p("Cells: total link yield (repaired opens x fatal bridges) / $/GB. Left block: supply pads adjacent to signal pads (no domain switches);")
    p("right block: spec rule with domain-switched supplies (bridges repairable).")
    p("")
    p("| p_link | 1.0 um | 1.5 um | 2.0 um | 3.0 um | 1.5 um, switched supplies | 3.0 um, switched supplies |")
    p("|---|---|---|---|---|---|---|")
    for pl in (1e-7, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 1e-3, 1e-2):
        row = []
        for pitch, fg in ((1.0, V("f_global")), (1.5, V("f_global")), (2.0, V("f_global")), (3.0, V("f_global")), (1.5, None), (3.0, None)):
            g = solve_group("1T1C", 64, pitch)
            if g is None:
                row.append("infeasible")
                continue
            d = die_model(g, 64)
            c, y = cost_per_gb(d, 64, pl, pitch, f_global=fg)
            cs_ = f"${c:.2f}" if c < 100 else ">$100"
            row.append(f"{y['y_link']:.3f} / {cs_}")
        p(f"| {pl:.0e} | " + " | ".join(row) + " |")
    p("")
    p("Second unknown: particle density on the pre-bond surface (1T1C-64 @1.5 um, W2W vs D2W):")
    p("| particles/cm2 (>=0.5 um) | W2W void yield | W2W $/GB | D2W void yield | D2W $/GB |")
    p("|---|---|---|---|---|")
    g, d = table[("1T1C", 64, 1.5)]
    for dp in (0.01, 0.05, 0.2, 0.5, 2.0):
        c1, y1 = cost_per_gb(d, 64, V("p_link_base"), 1.5, particle=dp)
        c2, y2 = cost_per_gb(d, 64, V("p_link_base"), 1.5, particle=dp, d2w=True)
        p(f"| {dp} | {y1['y_void']:.3f} | ${c1:.2f} | {y2['y_void']:.3f} | ${c2:.2f} |")


def s8_test_vehicle():
    hr("8. Decisive-experiment statistics: daisy chains, combs and Kelvin structures")
    p("| chain length (links) | chain yield @1e-6 | @1e-5 | @1e-4 | best-resolved p range |")
    p("|---|---|---|---|---|")
    for L in (1e3, 1e4, 1e5, 1e6):
        ys = [math.exp(-L * pl) for pl in (1e-6, 1e-5, 1e-4)]
        p(f"| {L:,.0f} | {ys[0]:.3f} | {ys[1]:.3f} | {ys[2]:.3f} | ~{0.1 / L:.0e} to {3 / L:.0e} |")
    p("")
    for n in (3e5, 1e6, 1e7, 3e7):
        kmax = -1
        while ucl95_poisson(kmax + 1, n) <= 1e-5:
            kmax += 1
        txt = f"k <= {kmax}" if kmax >= 0 else "not possible (even k = 0 gives UCL > 1e-5)"
        p(f"- n = {n:.0e} links: claim p_open <= 1e-5 at 95% confidence if failures {txt} (UCL at k=0: {ucl95_poisson(0, n):.1e})")
    n_comb = 3.0 / 1e-7
    p(f"- Bridges: to show p_short <= 1e-7 per adjacent pair with zero shorts needs >= {n_comb:.0e} adjacent pad pairs in comb structures")
    p(f"  ({n_comb * 1.5 ** 2 * 1e-6 / 2:.0f} mm2 of comb at 1.5 um, ~2 pairs per pad).")
    area_1e7 = 1e7 * 1.5 ** 2 * 1e-6
    p(f"- 1e7 links at 1.5 um occupy {area_1e7:.1f} mm2 of bonded area (one field); a 300 mm pair carries ~3e10 sites, so >=1e7 measured")
    p("  links per wafer is a probe-time problem, not an area problem.")
    p("- Design: chains of 1e3/1e4/1e5 links (to resolve 1e-7..1e-3) at 1.0/1.5/2.0 um on the same reticle, Kelvin 4-wire links for the")
    p("  resistance distribution, pad-to-pad combs next to signal and supply pads, electrical overlay verniers at die centre and corners,")
    p("  and IGZO/In2O3 FETs + 1T1C/2T0C cells in the coupon tiers for pre/post-bond Vt and retention.")


def s9_go_nogo(ceilings):
    c1, c2 = ceilings
    hr("9. GO / NO-GO")
    p("GO/NO-GO: GO if an 8-tier (~5 um stressed film) oxide coupon wafer, bonded W2W at <=1.5 um pitch to a periphery-emulator wafer,")
    p("shows: opens <=1e-5 per link (95% UCL over >=1e7 links) with no new opens after 500 thermal cycles; pad-to-pad bridges <=1e-7 per")
    p("adjacent pair (>=3e7 pairs); max overlay <=0.30 um on 100% of dies after backside stress compensation (bow <=~200 um);")
    p(">=95% void-free dies; and post-anneal (<=250 C) oxide Vt shift <=20 mV with 85 C retention change <=2x.")
    p(f"NO-GO for the 1T1C variant if opens >=1e-4 per link at 2.0 um, bridges >=1e-6, or overlay >0.5 um after best compensation (pitch")
    p(f"forced beyond ~{c1} um). Gain-cell variants hold to ~{c2} um. Either way the merchant split pays only if a portfolio cell passes.")
    p("Model margins: with 1% spares, repaired opens keep die yield >0.9 to a few 1e-3/link, so the 1e-5 open bar has >100x headroom for")
    p("random opens; it is kept as a proxy for bridge and reliability tails. Bridges onto global supplies, overlay on bowed wafers and")
    p("particle voids are the binding failure modes.")


def main():
    p("# CELL-WAFER FOUNDRY -- model output")
    p("")
    p("Generated by `models/cell-wafer-foundry.py` (pure stdlib). Every input carries a source or ESTIMATE tag in the INPUTS block.")
    util, gbw, e_bl = s0_reference()
    s1_planar()
    table = s2_closure()
    ceilings = s3_pitch_ceiling(table)
    s4_parasitics_energy(table, e_bl)
    s5_yield(table)
    s6_cost(table, util, gbw)
    s7_sensitivity(table)
    s8_test_vehicle()
    s9_go_nogo(ceilings)
    hr("INPUTS (value | source)")
    for k, (v, src) in INPUTS.items():
        p(f"- `{k}` = {v} | {src}")
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "research", "stage3", "cell-wafer-foundry_model_output.md")
    try:
        with open(out, "w") as f:
            f.write("\n".join(OUT) + "\n")
    except OSError as e:
        print(f"[warn] could not write {out}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
