#!/usr/bin/env python3
"""
and-stack.py -- first-principles model of AND-STACK (Stage 3 dossier `and-stack`, agent dos-and-stack).

AND-STACK: a capacitorless oxide 2T0C gain cell at every tier-hole crossing of a NAND-style stack made
with ONE hole etch. Each tier has a WRITE plate and a SELECT plate. A recessed floating metal ring at the
select level is the storage node. It gates an oxide-semiconductor (IGZO / In2O3) film between two vertical
pillars in the hole (bitline BL and source SL, Macronix-3D-AND style), so every cell reads in parallel
(AND/NOR topology), not through a series string. The write plate gates the film that charges the ring.

Topology closure used here (see notes): during a write the BL and SL pillars of the hole are driven to
the SAME data voltage, so a film that touches both pillars can charge the ring through the write-plate
channel without a read-path short. During a read the SL is grounded and only the selected tier's select
plate is raised; the 63 other select plates sit at a cutoff bias.

RED-TEAM REVISIONS (2026-11-02): the single-film BL = SL closure above is topologically impossible (a ring
contact on a single wall-lining film always abuts the ring's own read channel). The model now describes the
two-film "notched write pocket" redesign; see the RED-TEAM REVISIONS block after INPUTS and section 11.

Run from dram-moonshot/:  python3 models/and-stack.py
Writes research/stage3/and-stack_model_output.md. Pure standard library. Exits 0.
"""

import math
import os
import sys

EPS0 = 8.854e-12
KB = 1.380649e-23
QE = 1.602e-19
T_HOT = 358.0  # 85 C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_MD = os.path.join(ROOT, "research", "stage3", "and-stack_model_output.md")

# --------------------------------------------------------------------------------------------
# INPUTS: (value, basis). Every value carries a source URL or "ESTIMATE: basis".
# --------------------------------------------------------------------------------------------
INPUTS = {
    # ---- reference DRAM (1-beta DDR5) ----
    "d1b_gb_mm2": (0.447, "A1_scaling_limits.md: Micron D1b 16Gb / 35.83 mm2 (TechInsights via ram-venture cost_stack s3.1)"),
    "d1b_cost_model_gb_mm2": (0.438, "ram-venture/models/dram_cost_stack.py (16Gb / 36.5 mm2 die)"),
    "wafer_1b_usd": (3800.0, "ram-venture/models/dram_cost_stack.py wafer_cost_1beta_usd (ESTIMATE there)"),
    "gb_per_wafer_1b": (3069.0, "ram-venture/models/dram_cost_stack.py: GDPW 1705 x yield 0.90 x 2 GB"),
    "gross_die_area_mm2": (1705 * 36.5, "ram-venture/models/dram_cost_stack.py: GDPW 1705 x 36.5 mm2 (300 mm, 3 mm edge, 80 um scribe)"),
    "comp_1b_usd_gb": (1.48, "A1_scaling_limits.md / ram-venture cost stack: component $/GB incl. probe/test/package"),
    # ---- array geometry ----
    "hole_pitch_nm": (150.0, "ESTIMATE: concept card; NAND-class hex channel-hole pitch"),
    "slit_overhead": (0.15, "ESTIMATE: concept card (block slits)"),
    "hole_d_nm": (90.0, "ESTIMATE: NAND-class hole; 90 nm (not 100) leaves a >=20 nm plate web after the ring recess"),
    "tier_pitch_nm": (80.0, "ESTIMATE: concept card, 2 plates x 40 nm (W/Mo + oxide) per tier"),
    "extra_layers_nm": (300.0, "ESTIMATE: hole-top pillar-select gate, dummy and cap layers"),
    "array_eff": (0.70, "ESTIMATE: concept card, bonded periphery (CBA/PUC-style); checked against staircase below"),
    "ecc_parity": (0.10, "ESTIMATE: concept card; ~6% tier-orthogonal RS erasure + ~4% intra-codeword BCH (RAW-BER CONTRACT)"),
    "rows_per_select_group": (2, "ESTIMATE: hole rows per hole-top select group; sets top-BL pitch"),
    "stair_step_um": (0.30, "ESTIMATE: NAND-class staircase step"),
    "stair_lanes": (4, "ESTIMATE: multi-zone (split) staircase, NAND practice"),
    "plate_len_um": (200.0, "ESTIMATE: DRAM-like short plate segment (sub-array) for RC"),
    "plate_rs_ohm_sq": (15.0, "ESTIMATE: ~20-40 nm W/Mo plate (~15-20 uOhm.cm thin film) x2 for hole perforation"),
    # ---- ring (storage node) electrostatics ----
    "ring_h_nm": (18.0, "ESTIMATE: ring height inside a 42 nm select level (6 nm W caps + 6 nm IPD top/bottom)"),
    "ring_t_nm": (10.0, "ESTIMATE: radial ring thickness (TiN/W) in the recess"),
    "ipd_phys_nm": (6.0, "ESTIMATE: Al2O3-rich inter-plate dielectric between select plate and ring"),
    "ipd_eot_nm": (2.5, "ESTIMATE: 6 nm Al2O3/HfO2 laminate, k~9.4"),
    "gox_eot_nm": (3.0, "ESTIMATE: read-gate dielectric between ring and film (6 nm HfO2/SiO2)"),
    "film_nm": (5.0, "ESTIMATE: ALD IGZO / In2O3 channel film"),
    "pillar_w_nm": (22.0, "ESTIMATE: BL and SL metal pillars inside the 68 nm core"),
    "wrap": (1.0, "ESTIMATE: fraction of ring top/bottom faces covered by select metal ('sandwich' select plate); 0 = back face only, Micron FG-NAND-style"),
    "c_par_fF": (0.015, "ESTIMATE: ring to own write plate + fringe to film/pillars, outside the gate area"),
    "c_wp_ring_fF": (0.008, "ESTIMATE: part of c_par: own write plate to ring (sets the write kickback)"),
    "c_nn_fF": (0.002, "ESTIMATE: ring-to-adjacent-ring through the hole core, write plate shields the direct path"),
    "cr_sigma": (0.03, "ESTIMATE: 1-sigma coupling-ratio spread (recess depth / IPD thickness variation across tiers)"),
    # ---- oxide FET ----
    "mu_cm2": (20.0, "ESTIMATE: a-IGZO 10-30 cm2/Vs; ALD In2O3 higher (Purdue VLSI 2024 Imax >160 uA/um, https://engineering.purdue.edu/~yep/Papers/VLSI2024 T4-1_Zehao Lin.pdf)"),
    "vt_read": (0.5, "ESTIMATE: enhancement-mode oxide FET; Purdue EDL 2024 shows Vt ~1 V tunable (https://engineering.purdue.edu/~yep/Papers/EDL_2024_In2O3 600C_Lin.pdf)"),
    "vt_write": (0.5, "ESTIMATE: same film, same process"),
    "ss_mv_dec_85c": (90.0, "ESTIMATE: thin-film oxide FET ~70-80 mV/dec at 25 C scaled by T/300"),
    "i_at_vt_A": (1e-7, "ESTIMATE: constant-current Vt definition, 100 nA x W/L"),
    "v_data_max": (1.0, "ESTIMATE: concept card, 4 levels in <=1 V"),
    "vds_read": (0.1, "ESTIMATE: clamped-BL current-mode (linear region) read"),
    "on_off_req": (1e5, "concept card GO: on/off >=1e5 against the 63-unselected equivalent"),
    "guard_v": (0.10, "ESTIMATE: drift + coupling guard on top of the cutoff requirement"),
    "v_plate_max": (2.5, "ESTIMATE: comfortable plate swing (low-voltage driver class, IPD field < ~3 MV/cm)"),
    "v_wp_on": (2.5, "ESTIMATE: write plate high = V_data_max + Vt + 1 V overdrive"),
    "v_wp_hold": (-1.5, "ESTIMATE: write plate hold, >=0.8 V below Vt referenced to the lowest ring potential"),
    # ---- bitline ----
    "c_bl_wire_fF_um": (0.20, "ESTIMATE: standard local-interconnect capacitance"),
    "l_local_bl_um": (20.0, "ESTIMATE: local BL across ~16 select groups to a bonded sense amp"),
    "n_sel_on_bl": (16, "ESTIMATE: hole-top select devices hanging on one local BL"),
    "c_sel_junction_fF": (0.10, "ESTIMATE"),
    "c_sa_fF": (2.0, "ESTIMATE: sense amp + bond via"),
    "dv_sense_mV": (50.0, "ESTIMATE: comparator resolution per decision incl. offset (MARGIN STACK class)"),
    # ---- level budget (random terms, 1 sigma) ----
    "sig_place_mV": (8.0, "ESTIMATE: write-verify placement resolution"),
    "sig_read_mV": (8.0, "ESTIMATE: RTN + comparator noise referred to ring"),
    "kick_var": (0.05, "ESTIMATE: relative spread of the write-plate kickback"),
    "coupling_det_mV": (30.0, "concept card: neighbour-ring coupling budget at 40 nm tier pitch"),
    "drift_card_mV": (60.0, "concept card: allowed PBTI/H drift over the refresh interval at 85 C"),
    "raw_ber_target": (1e-4, "RAW-BER CONTRACT landing zone (Stage 3); ArchShield-class tolerance https://memlab.ece.gatech.edu/papers/ISCA_2013_1.pdf"),
    # ---- retention / endurance anchors ----
    "imec_95c_s": (200.0, "imec EDL 2025: >200 s at 95 C, >1e12 cycles (https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234)"),
    "sjtu_rt_s": (30000.0, "SJTU AFM 2026 IGO 2T0C >30,000 s, 4 b (https://sigroup.sjtu.edu.cn/files/AdvFunctMater_UltrathinOxide_DRAM_2026.pdf)"),
    "imecas_3b_s": (400.0, "IMECAS + Beijing Super String VLSI 2026: 4 tiers, 3 b/cell, 400 s (https://www.ithome.com/0/966/543.htm)"),
    "endurance_demo": (1e12, "imec EDL 2025 >1e12 cycles (URL above)"),
    "endurance_need_refresh": (3.2e8, "C0 triage C0-1: 1 s refresh for 10 years"),
    "endurance_need_hot": (7e13, "C0 triage C0-1: hot row at 1% duty for 10 years"),
    "verify_pulses": (4, "ESTIMATE: program/verify pulses per 2-bit write"),
    "t_write_ns": (20.0, "ESTIMATE: one write pulse incl. settle (imec <10 ns write)"),
    # ---- energy ----
    "pump_eff": (0.45, "dram_cell_physics.py INPUTS pump_eff (ESTIMATE there)"),
    "periph_overhead": (2.0, "dram_cell_physics.py INPUTS periph_overhead (ESTIMATE there)"),
    "t_ref_ddr5_s": (0.032, "JEDEC 32 ms above 85 C (dram_cell_physics.py)"),
    # ---- cost ----
    "periph_wafer_usd": (2500.0, "ESTIMATE: concept card $2-3k bonded CMOS periphery wafer"),
    "bond_usd": (500.0, "ESTIMATE: concept card W2W hybrid bond (imec 300 nm-pitch W2W, ECTC 2025, via A3)"),
    "array_base_usd": (1000.0, "ESTIMATE: blank Si + hole etch + recesses + ALD films + pillars + staircase + top BL (SADP)"),
    "tier_usd": (30.0, "ESTIMATE: concept card $15-45 per tier (2 plate depositions + share of etch/fill)"),
    "y_periph": (0.95, "ESTIMATE: mature-node logic periphery die yield"),
    "y_bond": (0.97, "ESTIMATE: W2W bond yield at ~1-2 um pitch"),
    "y_hole": (0.97, "ESTIMATE: non-tier array defects (pillar shorts, hole opens) after column repair"),
    "p_tier_die": (0.01, "ESTIMATE: probability a given tier carries a killer defect somewhere in a die (A1 needs <=0.2% WITHOUT erasure coding)"),
    "f_nonconfined": (0.10, "ESTIMATE: share of tier defects that are not confined to one erasure group (plate shorts loading drivers)"),
    "erasure_groups": (64, "ESTIMATE: independent tier-erasure groups per die"),
    "spare_tiers": (2, "ESTIMATE: erasures correctable per codeword (RS(34,32)-class)"),
    "backend_1b_usd_gb": (1.48 - 3800.0 / 3069.0, "derived: 1-beta component $1.48 minus wafer-level $1.238/GB"),
}

# --------------------------------------------------------------------------------------------
# RED-TEAM REVISIONS (owner response resp-and-stack, 2026-11-02).
# Objections: research/redteam/rt_{DEV,PROC,CIRC,IND}.json; responses: research/redteam/responses_and-stack.json.
# Each row: input, old value, new value, objection id(s), reason. The original value is asserted so the
# block fails loudly if the base inputs drift. The pre-red-team design is reproduced by setting
# APPLY_RT_REVISIONS = False (exit 0 either way).
# Redesign summary: the single-film "BL = SL" closure is topologically impossible (RT-PROC-and-stack-01), so the
# cell becomes a TWO-FILM cell: the ring's top face is contacted by a per-hole write film confined in a hole-side
# notch of the write-plate level (notched write pocket), which kills the sandwich select wrap (wrap 1 -> 0). The
# stack becomes SiO2 / doped poly-SiGe select plate (gate-first, Micron-FG-style) / SiO2 / SiN write-plate
# sacrificial layer (replaced from slits by an H-free O2-based ALD Ru fill). Select plates idle LOW (rings parked
# below cutoff) and write plates hold at -3.0 V. Twin pillars need a 110 nm hole at 170 nm pitch.
# --------------------------------------------------------------------------------------------
APPLY_RT_REVISIONS = True
RT_REVISIONS = [
    ("hole_pitch_nm", 150.0, 170.0, "RT-PROC-and-stack-03",
     "two isolated W-core pillars need a ~88 nm core; 110 nm hole + 2x18 nm recess + 24 nm web"),
    ("hole_d_nm", 90.0, 110.0, "RT-PROC-and-stack-03", "core 110-2x(6+5) = 88 nm for two 28 nm pillars"),
    ("pillar_w_nm", 22.0, 28.0, "RT-PROC-and-stack-03 / RT-CIRC-and-stack-04",
     "Macronix-style twin plugs (8-34 layers shown) with a W core; ~10 kOhm per pillar"),
    ("tier_pitch_nm", 80.0, 90.0, "RT-PROC-and-stack-02",
     "per tier SiO2 15 / poly-SiGe select 30 / SiO2 15 / SiN write-plate sacrificial 30 nm (4 layers, 256 at 64 tiers)"),
    ("wrap", 1.0, 0.0, "RT-PROC-and-stack-01 / RT-PROC-and-stack-02",
     "ring top face becomes the write contact, so the W/X/W sandwich select plate is dropped (back face only)"),
    ("ipd_eot_nm", 2.5, 2.0, "RT-PROC-and-stack-01 (consequence)", "1 nm SiO2 + 5 nm HfO2 IPD to recover CR without wrap"),
    ("ss_mv_dec_85c", 90.0, 120.0, "RT-CIRC-and-stack-01 / RT-DEV-and-stack-04",
     "IGZO 2T0C shows 161 mV/dec at 300 K (Frontiers of Physics 2025, rt-CIRC log); 120 central, 160 worst"),
    ("guard_v", 0.10, 0.15, "RT-DEV-and-stack-02",
     "corrected Vt-tail arithmetic (see section 11b) needs little; +50 mV for Vt tail and temperature"),
    ("v_plate_max", 2.5, 3.0, "RT-DEV-and-stack-02", "NAND-class plate drivers on thick-oxide periphery; IPD <=3 MV/cm still enforced"),
    ("cr_sigma", 0.03, 0.045, "RT-PROC-and-stack-05 / RT-CIRC-and-stack-05",
     "within-tier sigma after per-tier trims; tier-to-tier taper is trimmed per plate"),
    ("v_wp_hold", -1.5, -3.0, "RT-CIRC-and-stack-01 / RT-DEV-and-stack-04",
     "deep write-plate hold with idle-low select plates; write FET >=1.9 V below Vt even at the -3.7 sigma tail"),
    ("ecc_parity", 0.10, 0.12, "RT-CIRC-and-stack-02", "+2% in-page reference cells for cross-temperature MLC reads"),
    ("array_eff", 0.70, 0.66, "RT-PROC-and-stack-02 / RT-DEV-and-stack-05",
     "poly-SiGe select plates (~300 ohm/sq) force ~60 um plate segments, roughly doubling the staircase share"),
    ("plate_rs_ohm_sq", 15.0, 300.0, "RT-DEV-and-stack-05 / RT-PROC-and-stack-02",
     "no CVD W in the stack: doped poly-SiGe select plate, H/F driven out at >=800 C before the oxide films"),
    ("plate_len_um", 200.0, 60.0, "RT-DEV-and-stack-05", "keeps select-plate RC ~5 ns with poly plates"),
    ("tier_usd", 30.0, 50.0, "RT-PROC-and-stack-04", "a tier is ~1.5-2 NAND ONON-pair equivalents (rt-PROC: $20-38 per pair)"),
    ("array_base_usd", 1000.0, 2200.0, "RT-PROC-and-stack-04 / RT-PROC-and-stack-01 / RT-PROC-and-stack-03",
     "cell module + notched write pocket + slit Ru replacement + twin sub-hole pillars + bottom select + 2nd SADP level"),
    ("y_hole", 0.97, 0.93, "RT-PROC-and-stack-03", "pillar-pair shorts are hole-level (all 64 tiers); column repair only"),
]
RT_NEW_INPUTS = {
    "ss_write_mv_dec_85c": (120.0, "RED-TEAM RT-CIRC-and-stack-01: write-FET slope, 90-160 mV/dec swept"),
    "sigma_vt_mV": (40.0, "RED-TEAM RT-CIRC-and-stack-01 / RT-DEV-and-stack-02: 30-50 mV per-cell Vt sigma"),
    "dibl_write_V": (0.15, "RED-TEAM RT-DEV-and-stack-04: short (~10 nm) WP-wrapped write segment, DIBL/curvature penalty"),
    "write_L_nm": (10.0, "RED-TEAM: write-film floor segment between read-film contact and ring top (notch geometry)"),
    "wgd_phys_nm": (8.0, "RED-TEAM: separate write-gate dielectric (SiO2/Al2O3) deposited from the slit side"),
    "tempco_vt_mV_K": (-17.0, "RED-TEAM RT-CIRC-and-stack-02: a-IGZO TFT Vt tempco (Chen, IEEE TED 2009, rt-CIRC log)"),
    "tempco_spread": (0.05, "RED-TEAM RT-CIRC-and-stack-02: cell-to-cell tempco spread"),
    "dT_trigger_K": (5.0, "RED-TEAM: on-die sensor forces a refresh of a region when |T - T_write| > 5 K"),
    "rho_w_core_uohm_cm": (35.0, "ESTIMATE: thin W core in a ~20 nm plug (size effect)"),
    "rho_poly_mohm_cm": (1.0, "rt-PROC: doped poly pillar ~1 mOhm.cm"),
    "sa_area_um2": (12.0, "RED-TEAM RT-CIRC-and-stack-03: clamped current-mode 2-b SA + write driver at 28 nm (10-20 um2)"),
    "t_group_drive_ns": (5.0, "ESTIMATE: hole-top select on, drive BL + 2 pillars + ring, select off"),
    "ddr5_GBps_per_GB": (3.2, "DDR5-6400 x8 die (6.4 GB/s) per 2 GB"),
    "incumbent_decline_lo": (0.08, "RED-TEAM RT-IND-and-stack-03: incumbent $/bit decline per year, low"),
    "incumbent_decline_hi": (0.12, "RED-TEAM RT-IND-and-stack-03: incumbent $/bit decline per year, high"),
    "years_to_volume": (6, "RED-TEAM RT-IND-and-stack-03: 2026 -> ~2032 first volume"),
    "deck2_usd": (400.0, "ESTIMATE: second deck hole etch + inter-deck pillar plug for >64 tiers"),
}
if APPLY_RT_REVISIONS:
    for _k, _old, _new, _ids, _why in RT_REVISIONS:
        assert abs(INPUTS[_k][0] - _old) < 1e-9, (_k, INPUTS[_k][0], _old)
        INPUTS[_k] = (_new, f"RED-TEAM {_ids}: {_old:g} -> {_new:g} ({_why}). Pre-red-team basis: {INPUTS[_k][1]}")
INPUTS.update(RT_NEW_INPUTS)


def V(k):
    return INPUTS[k][0]


LINES = []


def out(s=""):
    LINES.append(s)
    print(s)


def h2(t):
    out("")
    out("## " + t)
    out("")


def table(headers, rows):
    out("| " + " | ".join(headers) + " |")
    out("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        out("| " + " | ".join(str(x) for x in r) + " |")


# --------------------------------------------------------------------------------------------
# 1. Geometry and density
# --------------------------------------------------------------------------------------------
def hole_area_um2():
    p = V("hole_pitch_nm") * 1e-3
    return math.sqrt(3) / 2 * p * p * (1 + V("slit_overhead"))


def density_gb_mm2(tiers, bits, eff=None):
    eff = V("array_eff") if eff is None else eff
    cells_mm2 = 1e6 / hole_area_um2()
    return cells_mm2 * tiers * bits * eff / (1 + V("ecc_parity")) / 1e9


def section_density():
    h2("1. Geometry and density (user bits after ECC parity)")
    a = hole_area_um2()
    raw = 1e6 / a / 1e9
    out(f"- Area per hole (one cell per tier): {a:.4f} um2 -> raw {raw:.4f} Gb/mm2 per tier per bit; "
        f"x array eff {V('array_eff')} / (1+{V('ecc_parity')}) = {density_gb_mm2(1, 1):.4f} Gb/mm2 per bit-tier.")
    be1 = V("d1b_gb_mm2") / density_gb_mm2(1, 1)
    out(f"- 1-beta parity ({V('d1b_gb_mm2')} Gb/mm2): {be1:.1f} bit-tiers ({be1:.0f} tiers at 1 b, {be1/2:.1f} at 2 b).")
    # stack, AR, web, staircase, BL pitch
    rows = []
    for n in (16, 32, 64, 96, 128):
        h_um = (n * V("tier_pitch_nm") + V("extra_layers_nm")) / 1000
        ar = h_um * 1000 / V("hole_d_nm")
        rows.append([n, 2 * n, f"{h_um:.2f}", f"{ar:.0f}:1",
                     f"{density_gb_mm2(n,1):.2f} ({density_gb_mm2(n,1)/V('d1b_gb_mm2'):.1f}x)",
                     f"{density_gb_mm2(n,2):.2f} ({density_gb_mm2(n,2)/V('d1b_gb_mm2'):.1f}x)",
                     f"{density_gb_mm2(n,3):.2f} ({density_gb_mm2(n,3)/V('d1b_gb_mm2'):.1f}x)"])
    table(["tiers", "plates", "stack um", "hole AR", "Gb/mm2 1 b (x1b)", "2 b (x1b)", "3 b (x1b)"], rows)
    recess = V("ring_t_nm") + V("ipd_phys_nm") + 2.0  # +2 nm liner
    web = V("hole_pitch_nm") - V("hole_d_nm") - 2 * recess
    out(f"- Plate web left between neighbouring recessed rings: {V('hole_pitch_nm'):.0f} - {V('hole_d_nm'):.0f} - 2x{recess:.0f} = "
        f"**{web:.0f} nm** (flag if <20 nm: plate continuity and ring-to-ring shorts).")
    bl_pitch = V("hole_pitch_nm") / V("rows_per_select_group")
    out(f"- Top bitline pitch with {V('rows_per_select_group')} hole rows per hole-top select group: {bl_pitch:.0f} nm "
        f"(193i single exposure limit ~76-80 nm -> plan SADP; still EUV-free).")
    n64 = 2 * 64 + 4
    stair = n64 * V("stair_step_um") / V("stair_lanes")
    frac = stair / (stair + V("plate_len_um"))
    eff_chk = (1 - frac) * (1 - 0.25)
    out(f"- Staircase for 64 tiers ({n64} contacted layers, {V('stair_step_um')} um steps, {V('stair_lanes')} lanes): "
        f"{stair:.1f} um per {V('plate_len_um'):.0f} um plate = {frac*100:.1f}% area; with 25% for bonds, hole-top selects and "
        f"mat edges, array efficiency ~{eff_chk:.2f} (input {V('array_eff')}).")
    # plate RC
    holes_per_um2 = 1 / a
    c_plate_hole = 0.30e-15  # select plate per hole: IPD to ring (~0.17 fF) + plate-plate (~0.1 fF)
    strip_w = 1.0
    r_per_um = V("plate_rs_ohm_sq") / strip_w
    c_per_um = holes_per_um2 * strip_w * c_plate_hole
    rc = 0.38 * r_per_um * c_per_um * V("plate_len_um") ** 2
    out(f"- Select-plate RC for a {V('plate_len_um'):.0f} um x 1 um strip ({r_per_um:.0f} ohm/um, {c_per_um*1e15:.0f} fF/um): "
        f"**{rc*1e9:.1f} ns** (Elmore 0.38RC). A 1 mm NAND-length plate would be {0.38*r_per_um*c_per_um*1e6*1e9:.0f} ns.")
    return web


# --------------------------------------------------------------------------------------------
# 2. Ring electrostatics: C_SN, coupling ratio, kickback, neighbour coupling
# --------------------------------------------------------------------------------------------
def ring_caps(wrap=None, ipd_eot=None, gox_eot=None, ring_h=None):
    wrap = V("wrap") if wrap is None else wrap
    ipd_eot = V("ipd_eot_nm") if ipd_eot is None else ipd_eot
    gox_eot = V("gox_eot_nm") if gox_eot is None else gox_eot
    h = (V("ring_h_nm") if ring_h is None else ring_h) * 1e-9
    r1 = V("hole_d_nm") / 2 * 1e-9
    r2 = r1 + V("ring_t_nm") * 1e-9
    c_gox = EPS0 * 3.9 / (gox_eot * 1e-9) * 2 * math.pi * r1 * h
    c_back = EPS0 * 3.9 / (ipd_eot * 1e-9) * 2 * math.pi * r2 * h
    c_tb = EPS0 * 3.9 / (ipd_eot * 1e-9) * 2 * math.pi * (r2 ** 2 - r1 ** 2)
    c_ipd = c_back + wrap * c_tb
    c_par = V("c_par_fF") * 1e-15
    c_sn = c_ipd + c_gox + c_par
    return dict(c_gox=c_gox, c_ipd=c_ipd, c_par=c_par, c_sn=c_sn, cr=c_ipd / c_sn)


def section_ring():
    h2("2. Floating-ring storage node: capacitance and select-plate coupling ratio (CR)")
    c = ring_caps()
    out(f"- Base (wrap={V('wrap')}; 1 = sandwich select plate, 0 = back face only): C_ipd {c['c_ipd']*1e15:.3f} fF, C_gate {c['c_gox']*1e15:.3f} fF, "
        f"C_par {c['c_par']*1e15:.3f} fF -> **C_SN {c['c_sn']*1e15:.3f} fF, CR {c['cr']:.2f}**.")
    b = ring_caps(wrap=0.0)
    out(f"- Back-face-only ring (Micron FG-NAND-style recess): C_SN {b['c_sn']*1e15:.3f} fF, CR {b['cr']:.2f}.")
    rows = []
    for w in (0.0, 0.5, 1.0):
        row = [f"wrap {w:.1f}"]
        for e in (2.0, 2.5, 3.5, 5.0):
            cc = ring_caps(wrap=w, ipd_eot=e)
            row.append(f"{cc['cr']:.2f} / {cc['c_sn']*1e15:.2f}")
        rows.append(row)
    out("CR / C_SN (fF) vs IPD EOT (read-gate EOT 3 nm, ring height 18 nm):")
    out("")
    table(["", "IPD EOT 2.0 nm", "2.5 nm", "3.5 nm", "5.0 nm"], rows)
    csn = c["c_sn"]
    kick = V("c_wp_ring_fF") * 1e-15 / csn * (V("v_wp_on") - V("v_wp_hold"))
    nn = V("c_nn_fF") * 1e-15 / csn * V("v_data_max")
    ktc = math.sqrt(KB * T_HOT / csn) * 1e3
    e_lsb2 = csn * V("v_data_max") / 3 / QE
    out("")
    out(f"- Write-plate kickback when the write plate falls {V('v_wp_on')} -> {V('v_wp_hold')} V: {kick*1e3:.0f} mV "
        f"(deterministic, pre-compensated by write-verify; spread {V('kick_var')*100:.0f}% = {kick*V('kick_var')*1e3:.1f} mV).")
    out(f"- Neighbour-ring coupling for a full 1 V swing on the adjacent ring: {nn*1e3:.0f} mV (budget {V('coupling_det_mV'):.0f} mV).")
    out(f"- kTC noise on C_SN at 85 C: {ktc:.1f} mV; one 2-bit level step = {e_lsb2:.0f} electrons "
        f"({V('v_data_max')/3*1e3:.0f} mV).")
    return c


# --------------------------------------------------------------------------------------------
# 3. Select margin: can 63 unselected cells be cut off?
# --------------------------------------------------------------------------------------------
def read_fet_wl():
    r_film = (V("hole_d_nm") / 2 - 6.0 - V("film_nm") / 2)
    arc = 2 * math.pi * r_film - 2 * V("pillar_w_nm")
    l_ch = arc / 2
    w_eff = 2 * V("ring_h_nm")
    return w_eff / l_ch, l_ch


def select_requirements(cr_mean, n_unsel=63):
    wl, _ = read_fet_wl()
    cox = EPS0 * 3.9 / (V("gox_eot_nm") * 1e-9)
    beta = V("mu_cm2") * 1e-4 * cox * wl
    i_on = beta * 1.0 * V("vds_read")  # top stored level at Vov ~1 V, linear region
    i_off_max = i_on / (n_unsel * V("on_off_req"))
    i_vt = V("i_at_vt_A") * wl
    decades = math.log10(i_vt / i_off_max)
    v_ring_cut = V("vt_read") - decades * V("ss_mv_dec_85c") / 1000
    shift = V("v_data_max") - v_ring_cut + V("guard_v")
    cr_min = max(cr_mean - 3 * V("cr_sigma"), 1e-3)
    dv_unsel = shift / cr_min
    v_ipd = (1 - cr_min) * dv_unsel
    e_ipd = v_ipd / (V("ipd_phys_nm") * 1e-7)  # V/cm
    return dict(i_on=i_on, i_off_max=i_off_max, decades=decades, v_ring_cut=v_ring_cut, shift=shift,
                cr_min=cr_min, dv_unsel=dv_unsel, v_ipd=v_ipd, e_ipd=e_ipd)


def section_select(c):
    h2("3. Select margin (KEY UNKNOWN): cutting off 63 unselected cells in the same hole")
    wl, l_ch = read_fet_wl()
    s = select_requirements(c["cr"])
    out(f"- Read FET: two parallel film arcs, W = 2 x {V('ring_h_nm'):.0f} nm, L = {l_ch:.0f} nm -> W/L {wl:.2f}. "
        f"Top-level read current at Vds {V('vds_read')} V, Vov 1 V: **{s['i_on']*1e6:.2f} uA**.")
    out(f"- On/off >= {V('on_off_req'):.0e} against 63 unselected cells -> each unselected cell <= {s['i_off_max']*1e15:.0f} fA "
        f"= {s['decades']:.1f} decades below I(Vt) -> unselected ring must sit <= {s['v_ring_cut']:+.2f} V.")
    out(f"- Highest stored level {V('v_data_max')} V + {V('guard_v')} V guard -> the unselected select plates must pull every ring "
        f"down by **{s['shift']:.2f} V** = CR_min x dV_unsel. This shift is independent of CR; CR sets the plate swing.")
    out(f"- Base CR {c['cr']:.2f} (min {s['cr_min']:.2f} at -3 sigma): dV_unsel = {s['dv_unsel']:.2f} V, IPD sees {s['v_ipd']:.2f} V "
        f"({s['e_ipd']/1e6:.2f} MV/cm physical) during reads.")
    out("")
    out("Sensitivity on the key unknown (CR mean; sigma 0.03):")
    out("")
    rows = []
    for cr in (0.30, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80):
        r = select_requirements(cr)
        ok_swing = r["dv_unsel"] <= V("v_plate_max")
        ok_field = r["e_ipd"] <= 3.0e6
        verdict = "OK" if (ok_swing and ok_field) else ("swing>2.5 V" if not ok_swing else "IPD field")
        if ok_swing and not ok_field:
            verdict = "IPD field"
        rows.append([f"{cr:.2f}", f"{r['cr_min']:.2f}", f"{r['dv_unsel']:.2f}", f"{r['v_ipd']:.2f}",
                     f"{r['e_ipd']/1e6:.1f}", f"{(r['dv_unsel'])/cr:.1f}", verdict])
    table(["CR mean", "CR min", "dV_unsel (V)", "V across IPD (V)", "IPD MV/cm", "MLC plate step / ring step", "verdict"], rows)
    out("")
    cr_ok = next(k / 100 for k in range(30, 95) if select_requirements(k / 100)["dv_unsel"] <= V("v_plate_max")
                 and select_requirements(k / 100)["e_ipd"] <= 3.0e6)
    out(f"- Reading: the AND topology relaxes the card's CR >= 0.6 (inherited from the series-string pass-boost) to "
        f"**CR_mean >= {cr_ok:.2f} with sigma <= {V('cr_sigma')}** for a <= {V('v_plate_max')} V plate swing. Between 0.40 and "
        f"{cr_ok:.2f} the cell still works with 3-3.5 V plate drivers (NAND drivers handle far more); below ~0.40 the IPD field "
        "passes ~3 MV/cm during every read. A low CR costs plate swing, IPD stress and IPD leakage, not cutoff physics.")
    # the write-plate hold bias consequence
    ring_min = 0.0 - s["shift"]
    out(f"- Lowest ring potential with the select plates low = {ring_min:+.2f} V. With write-plate hold {V('v_wp_hold')} V the "
        f"write FET sits {(ring_min + V('vt_write') - V('v_wp_hold'))*1000:.0f} mV below threshold (referenced to the ring as "
        f"source) -> {(ring_min + V('vt_write') - V('v_wp_hold'))*1000/V('ss_write_mv_dec_85c'):.1f} decades at "
        f"{V('ss_write_mv_dec_85c'):.0f} mV/dec (nominal cell; tails and DIBL in section 11a).")
    return s


# --------------------------------------------------------------------------------------------
# 4. Read signal, timing, energy
# --------------------------------------------------------------------------------------------
def c_bitline():
    r1 = 15e-9
    r_out = (V("hole_d_nm") / 2) * 1e-9
    h_pill = (64 * V("tier_pitch_nm") + V("extra_layers_nm")) * 1e-9
    c_coax = 2 * math.pi * EPS0 * 5.0 / math.log(r_out / r1) * h_pill * 0.6  # 60% of perimeter faces plates
    c_pair = math.pi * EPS0 * 4.0 / math.acosh(2.0) * h_pill
    c_pillar = c_coax + c_pair
    c = (c_pillar + V("c_bl_wire_fF_um") * 1e-15 * V("l_local_bl_um") + V("n_sel_on_bl") * V("c_sel_junction_fF") * 1e-15
         + V("c_sa_fF") * 1e-15)
    return c, c_pillar


def section_read(c, s):
    h2("4. Read signal, timing and energy")
    cbl, cp = c_bitline()
    out(f"- Selected-block BL pillar (64 tiers) {cp*1e15:.2f} fF; local BL with hole-top selects and SA: **C_BL {cbl*1e15:.1f} fF** "
        "(unselected blocks' pillars are cut off by the hole-top select).")
    wl, _ = read_fet_wl()
    cox = EPS0 * 3.9 / (V("gox_eot_nm") * 1e-9)
    beta = V("mu_cm2") * 1e-4 * cox * wl
    rows = []
    for bits in (1, 2, 3):
        nlev = 2 ** bits
        step = V("v_data_max") / (nlev - 1)
        di = beta * step * V("vds_read")  # linear-region current step between adjacent levels
        t = cbl * V("dv_sense_mV") * 1e-3 / di
        rows.append([bits, f"{step*1e3:.0f}", f"{di*1e9:.0f}", f"{t*1e9:.1f}", nlev - 1])
    out("Single-plate-level, clamped-BL current-mode MLC read (all levels at one select bias; flash comparators):")
    out("")
    table(["bits/cell", "level step mV", "dI per level nA", "t to resolve 50 mV on C_BL (ns)", "comparators/BL"], rows)
    # energy per read and write
    dvp = select_requirements(c["cr"])["dv_unsel"]  # RED-TEAM: selected plate swings the full dV from idle-low
    e_read = (cbl * V("vds_read") * 0.5 + 0.30e-15 * dvp ** 2) * V("periph_overhead")
    e_bl_w = 2 * cbl * V("v_data_max") ** 2 / 2
    c_wp_hole = V("c_wp_ring_fF") * 1e-15 + 0.06e-15
    e_wp = c_wp_hole * (V("v_wp_on") - V("v_wp_hold")) ** 2 / V("pump_eff")
    e_write = (e_bl_w + e_wp) * V("periph_overhead")
    plate_rc = 0.38 * (V("plate_rs_ohm_sq") / 1.0) * (1 / hole_area_um2() * 0.30e-15) * V("plate_len_um") ** 2
    t2 = cbl * V("dv_sense_mV") * 1e-3 / (beta * V("v_data_max") / 3 * V("vds_read"))
    out("")
    out(f"- Array read latency (2 b): select-plate RC {plate_rc*1e9:.1f} ns + BL integrate {t2*1e9:.1f} ns + ~5 ns comparators/latch "
        f"+ ~5 ns decode = ~{plate_rc*1e9 + t2*1e9 + 10:.0f} ns, inside DRAM's 10-100 ns class. 2 b write = {V('verify_pulses')} x "
        f"({V('t_write_ns'):.0f} ns pulse + verify) = ~{V('verify_pulses')*(V('t_write_ns')+5):.0f} ns.")
    out(f"- Read energy per cell ~{e_read*1e15:.1f} fJ (BL clamp + select plate share, x{V('periph_overhead')} periphery). "
        f"Non-destructive: no restore, so no DDR-style page overfetch on reads.")
    out(f"- Write energy per cell ~{e_write*1e15:.0f} fJ (BL+SL swing {e_bl_w*1e15:.1f} fJ, write plate {e_wp*1e15:.1f} fJ) "
        f"x {V('verify_pulses')} program/verify pulses for 2 b -> ~{e_write*V('verify_pulses')*1e15:.0f} fJ per 2-bit cell.")
    return cbl, e_read, e_write


# --------------------------------------------------------------------------------------------
# 5. MLC level budget -> raw BER
# --------------------------------------------------------------------------------------------
def qfunc(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def raw_ber(bits, drift_mV, c):
    nlev = 2 ** bits
    half = V("v_data_max") / (nlev - 1) / 2 * 1e3
    kick = V("c_wp_ring_fF") * 1e-15 / c["c_sn"] * (V("v_wp_on") - V("v_wp_hold")) * V("kick_var") * 1e3
    ktc = math.sqrt(KB * T_HOT / c["c_sn"]) * 1e3
    sig = math.sqrt(V("sig_place_mV") ** 2 + V("sig_read_mV") ** 2 + kick ** 2 + ktc ** 2)
    margin = half - drift_mV - V("coupling_det_mV")
    if margin <= 0:
        return 0.5, sig, margin
    # inner levels have two neighbours; Gray coding -> ~1 bit error per level error
    p_level = qfunc(margin / sig) * (2 * (nlev - 1) / nlev)
    return p_level / bits, sig, margin


def max_drift_for(bits, target, c):
    lo, hi = 0.0, 500.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if raw_ber(bits, mid, c)[0] <= target:
            lo = mid
        else:
            hi = mid
    return lo


def section_ber(c):
    h2("5. Multi-level budget -> raw BER (feeds the RAW-BER CONTRACT, target 1e-4)")
    rows = []
    for bits in (1, 2, 3):
        b60, sig, m60 = raw_ber(bits, V("drift_card_mV"), c)
        dmax = max_drift_for(bits, V("raw_ber_target"), c)
        rows.append([bits, f"{V('v_data_max')/(2**bits-1)*1e3:.0f}", f"{sig:.1f}",
                     f"{m60:.0f}", f"{b60:.1e}", f"{dmax:.0f}"])
    table(["bits/cell", "level step mV", "random sigma mV", "margin at 60 mV drift + 30 mV coupling",
           "raw BER at card drift", "max drift for BER 1e-4 (mV)"], rows)
    out("")
    out("- 2 b/cell in a 1 V window has room (drift up to the value in the last column). 3 b/cell does not close in a "
        "1 V window with a 30 mV coupling allowance: it needs a ~1.5 V window AND coupling <= 10 mV AND drift <= ~25 mV. "
        "The 3 b rows in section 9 are an upside, not the plan.")
    old = INPUTS["v_data_max"], INPUTS["coupling_det_mV"]
    INPUTS["v_data_max"] = (1.5, old[0][1])
    INPUTS["coupling_det_mV"] = (10.0, old[1][1])
    d3 = max_drift_for(3, V("raw_ber_target"), c)
    INPUTS["v_data_max"], INPUTS["coupling_det_mV"] = old
    out(f"- Check: 3 b in a 1.5 V window with 10 mV coupling tolerates {d3:.0f} mV of drift at raw BER 1e-4.")
    return max_drift_for(2, V("raw_ber_target"), c)


# --------------------------------------------------------------------------------------------
# 6. Retention and refresh
# --------------------------------------------------------------------------------------------
def section_retention(c, dmax2, e_read, e_write):
    h2("6. Retention from node leakage, and refresh energy")
    csn = c["c_sn"]
    rows = []
    for t in (1, 8, 64, 1000):
        r = [f"{t}"]
        for bits, dv in ((1, 0.25), (2, dmax2 / 1000), (2, V("drift_card_mV") / 1000)):
            i = csn * dv / t
            r.append(f"{i*1e21:,.0f}")
        rows.append(r)
    table(["refresh interval s", "1 b, 250 mV loss: max leak zA", f"2 b, {dmax2:.0f} mV (BER-limited): zA",
           "2 b, 60 mV (card): zA"], rows)
    a_ipd = (2 * math.pi * (V("hole_d_nm") / 2 + V("ring_t_nm")) * V("ring_h_nm") +
             2 * math.pi * ((V("hole_d_nm") / 2 + V("ring_t_nm")) ** 2 - (V("hole_d_nm") / 2) ** 2)) * 1e-14  # cm2
    j1 = csn * (V("drift_card_mV") / 1000) / 1.0 / a_ipd
    j64 = j1 / 64
    out("")
    out(f"- Dielectric leakage budget: the ring has {a_ipd*1e10:.2f}e-10 cm2 of IPD. For 2 b at 1 s the whole IPD may leak "
        f"<= {j1:.1e} A/cm2; at 64 s <= {j64:.1e} A/cm2 (85 C, ~0.5-1 V). Low-field Al2O3/SiO2 is plausible; high-k "
        "trap-assisted conduction is the risk.")
    imec_leak = 0.5e-15 * 0.1 / V("imec_95c_s")
    out(f"- Anchor: imec's >200 s at 95 C implies roughly <= {imec_leak*1e21:.0f} zA on a ~0.5 fF node at ~100 mV loss "
        "[ESTIMATE: node C and criterion not published in the snippet]. The 1 s GO bar therefore has ~2 decades of headroom "
        "per cell; the risk is the tail cell and the ring's extra dielectrics.")
    # refresh power
    bits_per_cell = 2
    e_ref_cell = e_read + e_write * V("verify_pulses")
    e_ref_bit = e_ref_cell / bits_per_cell
    try:
        sys.path.insert(0, HERE)
        import dram_cell_physics as dcp  # reuse the A1 model
        e_ddr, _, _ = dcp.refresh_energy_per_bit_fJ()
        src = "dram_cell_physics.refresh_energy_per_bit_fJ()"
    except Exception:  # pragma: no cover
        e_ddr, src = 60.0, "fallback ESTIMATE"
    p_and_1s = e_ref_bit * 8e9 / 1.0
    p_and_64 = e_ref_bit * 8e9 / 64.0
    p_ddr = e_ddr * 1e-15 * 8e9 / V("t_ref_ddr5_s")
    out(f"- Refresh energy per bit: AND-STACK ~{e_ref_bit*1e15:.0f} fJ (read + 4-pulse write-verify) vs DDR5 {e_ddr:.0f} fJ ({src}).")
    out(f"- Refresh power per GB at 85 C: DDR5 at 32 ms {p_ddr*1e3:.1f} mW; AND-STACK at 1 s {p_and_1s*1e3:.2f} mW "
        f"({p_ddr/p_and_1s:.0f}x lower); at 64 s {p_and_64*1e3:.3f} mW ({p_ddr/p_and_64:.0f}x lower).")


# --------------------------------------------------------------------------------------------
# 7. Endurance
# --------------------------------------------------------------------------------------------
def section_endurance():
    h2("7. Endurance budget (channel writes, no charge fluence through an insulator)")
    vp = V("verify_pulses")
    rows = []
    for name, need in (("refresh only, 1 s interval, 10 yr", V("endurance_need_refresh")),
                       ("refresh only, 64 s interval, 10 yr", 10 * 3.15e7 / 64),
                       ("hot row, 1% write duty, 10 yr (C0-1)", V("endurance_need_hot"))):
        pulses = need * vp
        rows.append([name, f"{need:.1e}", f"{pulses:.1e}", f"{V('endurance_demo')/pulses:.2g}x"])
    table(["case", "writes", f"pulses (x{vp} verify)", "margin vs imec 1e12"], rows)
    out("")
    out("- Refresh-driven wear is 3+ decades inside demonstrated endurance. A pathological hot row needs ~300x more "
        "than shown: write-combining/remap in the controller, or a measured >=1e14 (NEO claims 1e14 for its Si cell).")


# --------------------------------------------------------------------------------------------
# 8. Yield with tier-orthogonal erasure codes
# --------------------------------------------------------------------------------------------
def binom_cdf(n, k, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def die_yield(tiers, p_tier=None, spares=None, groups=None, fnc=None):
    p_tier = V("p_tier_die") if p_tier is None else p_tier
    spares = V("spare_tiers") if spares is None else spares
    groups = V("erasure_groups") if groups is None else groups
    fnc = V("f_nonconfined") if fnc is None else fnc
    pg = p_tier * (1 - fnc) / groups
    y_group = binom_cdf(tiers, spares, pg)
    y_nc = math.exp(-p_tier * fnc * tiers)
    return V("y_periph") * V("y_bond") * V("y_hole") * y_nc * y_group ** groups


def section_yield():
    h2("8. Die yield vs per-tier killer-defect rate (tier-orthogonal erasure, 2 spares per codeword)")
    rows = []
    for p in (0.002, 0.01, 0.02, 0.05, 0.10):
        no_ecc = V("y_periph") * V("y_bond") * V("y_hole") * (1 - p) ** 64
        rows.append([f"{p*100:.1f}%", f"{no_ecc:.2f}", f"{die_yield(64, p):.2f}",
                     f"{die_yield(64, p, fnc=0.3):.2f}", f"{die_yield(64, p, fnc=0.0):.2f}"])
    table(["p(tier killer) per die", "64 tiers, no erasure code", f"erasure, {int(V('f_nonconfined')*100)}% non-confined",
           "erasure, 30% non-confined", "erasure, 0% non-confined"], rows)
    out("")
    out("- Erasure coding turns tier yield from a compounding wall (A1: <=0.2% per tier needed) into a parity cost, "
        "provided most defects stay inside one tier and one group. The non-confined share (plate-to-plate shorts that load "
        "a driver) is what the 4-tier stack must measure.")


# --------------------------------------------------------------------------------------------
# 9. Cost per GB
# --------------------------------------------------------------------------------------------
def wafer_cost(tiers, tier_usd=None):
    tier_usd = V("tier_usd") if tier_usd is None else tier_usd
    return V("periph_wafer_usd") + V("bond_usd") + V("array_base_usd") + tiers * tier_usd


def usd_per_gb(tiers, bits, tier_usd=None, p_tier=None):
    gb = V("gross_die_area_mm2") * density_gb_mm2(tiers, bits) / 8 * die_yield(tiers, p_tier)
    w = wafer_cost(tiers, tier_usd) / gb
    d_ratio = V("d1b_cost_model_gb_mm2") / density_gb_mm2(tiers, bits)
    backend = V("backend_1b_usd_gb") * (0.5 + 0.5 * d_ratio)
    return w, w + backend, gb


def section_cost():
    h2("9. Cost per GB vs 1-beta DDR5 (wafer-level $1.24/GB, component $1.48/GB)")
    w1b = V("wafer_1b_usd") / V("gb_per_wafer_1b")
    rows = []
    for tiers, bits in ((16, 2), (32, 1), (32, 2), (48, 2), (64, 1), (64, 2), (64, 3), (96, 2)):
        w, comp, gb = usd_per_gb(tiers, bits)
        rows.append([f"{tiers} x {bits} b", f"{wafer_cost(tiers):,.0f}", f"{die_yield(tiers):.2f}", f"{gb:,.0f}",
                     f"{w:.3f}", f"{w1b/w:.1f}x", f"{comp:.2f}", f"{V('comp_1b_usd_gb')/comp:.1f}x"])
    table(["tiers x bits", "wafer $", "die yield", "GB/wafer", "wafer $/GB", "bits/$ vs 1b (wafer)", "component $/GB",
           "vs $1.48"], rows)
    out("")
    out("Sensitivity of 64 x 2 b component $/GB to $/tier and per-tier defect rate:")
    out("")
    rows = []
    for tu in (15, 30, 45, 80):
        r = [f"${tu}/tier"]
        for p in (0.002, 0.02, 0.10):
            _, comp, _ = usd_per_gb(64, 2, tier_usd=tu, p_tier=p)
            r.append(f"{comp:.2f} ({V('comp_1b_usd_gb')/comp:.1f}x)")
        rows.append(r)
    table(["", "p_tier 0.2%", "p_tier 2%", "p_tier 10%"], rows)
    out("")
    out(f"- Break-even (component) at 1 b: the first tier count with >=1x; at 2 b roughly half that. "
        f"Back-end adder scaled from 1-beta's ${V('backend_1b_usd_gb'):.2f}/GB [ESTIMATE].")
    be_rows = []
    for bits in (1, 2):
        for n in range(4, 200):
            _, comp, _ = usd_per_gb(n, bits)
            if comp <= V("comp_1b_usd_gb"):
                be_rows.append([f"{bits} b", n, f"{density_gb_mm2(n, bits)/V('d1b_gb_mm2'):.2f}x density"])
                break
    table(["bits", "cost break-even tiers", "density at break-even"], be_rows)


# --------------------------------------------------------------------------------------------
# 10. GO / NO-GO
# --------------------------------------------------------------------------------------------
def _with_inputs(over, fn):
    """Evaluate fn() with some INPUTS temporarily overridden (values only)."""
    saved = {k: INPUTS[k] for k in over}
    try:
        for k, v in over.items():
            INPUTS[k] = (v, saved[k][1])
        return fn()
    finally:
        INPUTS.update(saved)


# --------------------------------------------------------------------------------------------
# 11. RED-TEAM checks (owner response resp-and-stack)
# --------------------------------------------------------------------------------------------
def write_fet_tail_leak(hold, ss, ring_min, sigma_mv=None, n_sig=3.72):
    """1e-4-tail write-FET hold leakage (A). Source = ring (lowest node), gate = write plate."""
    sigma_mv = V("sigma_vt_mV") if sigma_mv is None else sigma_mv
    r_mid = (V("hole_d_nm") / 2 + V("ring_t_nm") / 2)
    wl = 2 * math.pi * r_mid / V("write_L_nm")
    i_vt = V("i_at_vt_A") * wl
    vt_eff = V("vt_write") - n_sig * sigma_mv / 1000 - V("dibl_write_V")
    margin = vt_eff - (hold - ring_min)
    return i_vt * 10 ** (-margin / (ss / 1000)), margin, wl


def section_redteam(c, s, dmax2):
    h2("11. RED-TEAM checks (owner response, 2026-11-02)")
    csn = c["c_sn"]
    leak_budget = csn * dmax2 / 1000 / 1.0
    ring_min = -s["shift"]
    # 11a write-FET hold leakage
    out("### 11a. Write-FET hold leakage with idle-low select plates (RT-CIRC-and-stack-01, RT-DEV-and-stack-04)")
    out("")
    _, _, wl = write_fet_tail_leak(V("v_wp_hold"), V("ss_write_mv_dec_85c"), ring_min)
    out(f"- Write FET = write film on the notch floor, W = 2 pi x {V('hole_d_nm')/2 + V('ring_t_nm')/2:.0f} nm, L = "
        f"{V('write_L_nm'):.0f} nm -> W/L {wl:.0f}, I(Vt) {V('i_at_vt_A')*wl*1e6:.1f} uA (a wide, short device: worse than the "
        f"39 nA the dossier used). Tail cell = Vt - 3.72 sigma ({V('sigma_vt_mV'):.0f} mV) - {V('dibl_write_V')} V DIBL. "
        f"Ring parked at {ring_min:+.2f} V (top level, select plates idle low). Budget at 1 s, 2 b: {leak_budget*1e18:.0f} aA.")
    out("")
    rows = []
    for hold in (-1.5, -2.0, -2.5, -3.0):
        r = [f"{hold:+.1f} V"]
        for ss in (90, 120, 160):
            lk, m, _ = write_fet_tail_leak(hold, ss, ring_min)
            r.append(f"{lk*1e18:.3g} aA ({'OK' if lk <= leak_budget else 'FAIL'})")
        rows.append(r)
    table(["WP hold", "SS 90 mV/dec", "SS 120", "SS 160"], rows)
    e_hold = (abs(V("v_wp_hold")) + 0.1) / (V("wgd_phys_nm") * 1e-7) / 1e6
    e_on = V("v_wp_on") / (V("wgd_phys_nm") * 1e-7) / 1e6
    out("")
    out(f"- At the adopted hold {V('v_wp_hold')} V the write-gate dielectric ({V('wgd_phys_nm'):.0f} nm) sees at most "
        f"{abs(V('v_wp_hold'))+0.1:.1f} V ({e_hold:.1f} MV/cm) in hold and {V('v_wp_on')} V ({e_on:.1f} MV/cm) when writing; "
        f"write-plate swing {V('v_wp_on')-V('v_wp_hold'):.1f} V (thick-oxide drivers).")
    # 11b Vt tail of unselected read FETs
    out("")
    out("### 11b. Unselected-cell Vt tails (RT-DEV-and-stack-02)")
    out("")
    wl_r, _ = read_fet_wl()
    cox = EPS0 * 3.9 / (V("gox_eot_nm") * 1e-9)
    di2 = V("mu_cm2") * 1e-4 * cox * wl_r * V("v_data_max") / 3 * V("vds_read")
    rows = []
    for ss in (90, 120, 160):
        for nsig, lab in ((3.72, "1e-4"), (6.36, "1e-10")):
            x = nsig * 50.0 / 1000
            i = s["i_off_max"] * 10 ** (x / (ss / 1000))
            rows.append([ss, lab, f"{x*1000:.0f}", f"{i*1e12:.3g} pA", f"{i/di2*100:.3g}%"])
    table(["SS mV/dec", "cell quantile (sigma_Vt 50 mV)", "Vt shift mV", "leak at nominal cutoff", "of a 2-b level step"], rows)
    out("")
    out(f"- 142 fA x 10^3.5 is ~0.45 nA, not 0.48 uA: the objection's tail currents are 1000x too high. A 1e-10 cell costs "
        f"well under 1% of a {di2*1e9:.0f} nA level step. What does move the cutoff is the slope: at "
        f"{V('ss_mv_dec_85c'):.0f} mV/dec the unselected ring must sit <= {s['v_ring_cut']:+.2f} V, so the pull-down is "
        f"{s['shift']:.2f} V (guard {V('guard_v')} V).")
    # 11c write half-select
    out("")
    out("### 11c. Shared write plate: half-select and the sequential group write (RT-DEV-and-stack-01)")
    out("")
    cbl, cp = c_bitline()
    err = 2 * cp / (2 * cp + csn)
    out(f"- If unselected groups' pillars float at an unknown value, a write pulse pulls each ring {err*100:.0f}% of the way to "
        f"its floating pillars (BL+SL {2*cp*1e15:.2f} fF vs C_SN {csn*1e15:.3f} fF): corruption, as the objection says.")
    bl_pitch = V("hole_pitch_nm") / V("rows_per_select_group")
    n_bl = V("plate_len_um") * 1000 / bl_pitch
    n_g = V("n_sel_on_bl")
    page_cells = n_bl * n_g
    out(f"- Fix adopted: hold write plate k ON and drive the {n_g} groups in turn through the hole-top selects; each driven "
        f"group's ring + pillars then float at their target while the next group is driven. SL pillars float via a bottom "
        f"select. Page = one tier of one block = {n_bl:.0f} BLs x {n_g} groups = {page_cells:,.0f} cells "
        f"({page_cells*2/8/1024:.1f} KiB at 2 b), read into the buffer first (read-modify-write).")
    rows = []
    for mux in (1, 8, 16):
        cyc = n_g * mux * V("t_group_drive_ns") + V("t_write_ns") + n_g * mux * 10.0
        t_page = V("verify_pulses") * cyc
        rows.append([mux, f"{cyc:.0f}", f"{t_page/1000:.1f}", f"{page_cells*2/8/(t_page*1e-9)/1e9:.2f}"])
    table(["SA/driver mux", "ns per pulse cycle (drive + pulse + verify)", "us per page (4 pulses)", "GB/s per block"], rows)
    # 11d SA pitch and bandwidth
    out("")
    out("### 11d. Sense-amp pitch and bandwidth per mm2 (RT-CIRC-and-stack-03)")
    out("")
    fp = V("l_local_bl_um") * bl_pitch / 1000
    mux = math.ceil(V("sa_area_um2") / fp)
    sa_mm2 = 1e6 / fp / mux
    bw_rd = sa_mm2 * 2 / 8 / 20e-9 / 1e9
    need = density_gb_mm2(64, 2) / 8 * V("ddr5_GBps_per_GB")
    out(f"- BL footprint {V('l_local_bl_um'):.0f} um x {bl_pitch:.0f} nm = {fp:.2f} um2 vs SA + driver ~{V('sa_area_um2'):.0f} um2 "
        f"-> {mux}:1 mux. {sa_mm2:,.0f} SAs per mm2 of array, 2 b per ~20 ns -> internal read bandwidth "
        f"~{bw_rd:,.0f} GB/s per mm2.")
    out(f"- DDR5-class need at 64 x 2 b density: {density_gb_mm2(64,2)/8:.2f} GB/mm2 x {V('ddr5_GBps_per_GB')} GB/s per GB = "
        f"{need:.2f} GB/s per mm2 -> {bw_rd/need:,.0f}x headroom. Page width falls {mux}x; latency per access does not.")
    # 11e pillar resistance
    out("")
    out("### 11e. Pillar resistance (RT-CIRC-and-stack-04, RT-PROC-and-stack-03)")
    out("")
    h_pill = (64 * V("tier_pitch_nm") + V("extra_layers_nm")) * 1e-7  # cm
    a_w = math.pi * ((V("pillar_w_nm") - 6) / 2 * 1e-7) ** 2
    a_p = math.pi * (V("pillar_w_nm") / 2 * 1e-7) ** 2
    r_w = V("rho_w_core_uohm_cm") * 1e-6 * h_pill / a_w
    r_p = V("rho_poly_mohm_cm") * 1e-3 * h_pill / a_p
    i_on = s["i_on"]
    rows = []
    for lab, r in (("W core (3 nm TiN liner)", r_w), ("doped poly", r_p)):
        same_end = 2 * r * i_on
        split = r * i_on
        rows.append([lab, f"{r/1e3:.1f}", f"{same_end*1e3:.0f} mV ({same_end/V('vds_read')*100:.0f}%)",
                     f"{split*1e3:.0f} mV ({split/V('vds_read')*100:.0f}%), all tiers"])
    table(["pillar", "kOhm per pillar", "worst tier, BL+SL from top", "BL from top, SL from bottom"], rows)
    out("")
    out("- Contacting BL at the top and SL at the bottom makes the series resistance the same for every tier (one pillar "
        "length), so the loss is a uniform, verify-cancelled offset. Doped-poly pillars are excluded.")
    # 11f cross-temperature
    out("")
    out("### 11f. Cross-temperature MLC (RT-CIRC-and-stack-02)")
    out("")
    rows = []
    for dT in (V("dT_trigger_K"), 10.0, 50.0):
        cm = abs(V("tempco_vt_mV_K")) * dT
        res = cm * V("tempco_spread")
        rows.append([f"{dT:.0f}", f"{cm:.0f}", f"{res:.1f}", "OK" if res <= 10 else ("marginal" if res <= 30 else "FAIL")])
    table(["dT write->read (K)", "common-mode Vt shift (mV, removed by in-page refs)", "residual spread (mV)",
           "vs ~10 mV allowance"], rows)
    out("")
    out(f"- Adopted: in-page reference cells (+2% parity), temperature-tracked select read bias, and a forced refresh of any "
        f"region whose |T - T_write| exceeds {V('dT_trigger_K'):.0f} K. 1 b/cell tolerates the full 50 K with refs.")
    # 11g CR vs taper
    out("")
    out("### 11g. CR versus hole taper and recess depth (RT-PROC-and-stack-05, RT-CIRC-and-stack-05)")
    out("")
    rows = []
    d0 = V("hole_d_nm")
    for f in (1.0, 0.9, 0.8):
        r = [f"{d0*f:.0f} nm ({(1-f)*100:.0f}% taper)"]
        for rt in (7.0, 10.0, 13.0):
            cc = _with_inputs({"hole_d_nm": d0 * f, "ring_t_nm": rt}, lambda: ring_caps())
            r.append(f"{cc['cr']:.3f} / {cc['c_sn']*1e15:.3f}")
        rows.append(r)
    table(["hole CD", "ring 7 nm: CR / C_SN fF", "10 nm", "13 nm"], rows)
    out("")
    out("- CR is a ratio of two coaxial capacitors, so a 20% CD taper moves it only ~0.01-0.02; read W/L and C_SN do scale "
        "with CD and are absorbed by per-cell write-verify plus per-tier reference trims.")
    # 11h IPD read disturb
    out("")
    out("### 11h. Neighbour-read excursions on the IPD (RT-DEV-and-stack-03)")
    out("")
    v_ipd_exc = (1 - c["cr"]) * s["dv_unsel"]
    q_e = (c["c_ipd"] * v_ipd_exc + c["c_gox"] * c["cr"] * s["dv_unsel"]) / QE
    out(f"- Displacement charge per excursion ~{q_e:.0f} e-; trapping 0.1-1% of it is {q_e*0.001*QE/csn*1e3:.1f}-"
        f"{q_e*0.01*QE/csn*1e3:.0f} mV per excursion on C_SN {csn*1e15:.3f} fF.")
    out("- Original bias (select plates idle at read level): every read of any tier swings the 63 other rings, i.e. ~1e7 "
        "excursions per ring per second in a hole read at 10 MHz. Adopted idle-low bias: a ring moves only when its own tier "
        "is read (1/64 of the hole's reads on average); a single-cell read hammer still gives up to 1e7/s, so the GO list "
        "tests own-tier excursions (1e8 within one refresh interval, 1e12 cumulative).")
    # 11i cost rebasing
    out("")
    out("### 11i. Cost re-basing (RT-PROC-and-stack-04, RT-IND-and-stack-03)")
    out("")
    yrs = V("years_to_volume")
    inc_lo = V("comp_1b_usd_gb") * (1 - V("incumbent_decline_hi")) ** yrs
    inc_hi = V("comp_1b_usd_gb") * (1 - V("incumbent_decline_lo")) ** yrs
    rows = []
    cases = [("64 x 2 b revised ($%.0f/tier, $%.0f base)" % (V("tier_usd"), V("array_base_usd")), 64, 2, {}),
             ("64 x 2 b, rt-PROC case ($60/tier, $2,000 base)", 64, 2, {"tier_usd": 60.0, "array_base_usd": 2000.0}),
             ("64 x 2 b, optimistic ($35/tier, $1,600 base)", 64, 2, {"tier_usd": 35.0, "array_base_usd": 1600.0}),
             ("32 x 2 b revised", 32, 2, {}),
             ("96 x 2 b, two decks", 96, 2, {"array_base_usd": V("array_base_usd") + V("deck2_usd")}),
             ("64 x 1 b revised (fallback mode)", 64, 1, {})]
    for lab, n, b, ov in cases:
        _, comp, _ = _with_inputs(ov, lambda: usd_per_gb(n, b)) if ov else usd_per_gb(n, b)
        rows.append([lab, f"{density_gb_mm2(n,b)/V('d1b_gb_mm2'):.1f}x", f"{comp:.2f}", f"{V('comp_1b_usd_gb')/comp:.1f}x",
                     f"{inc_lo/comp:.1f}-{inc_hi/comp:.1f}x"])
    table(["case", "density vs 1-beta", "component $/GB", "bits/$ vs 2026 1-beta ($1.48)",
           f"vs ~{2026+yrs} incumbent (${inc_lo:.2f}-{inc_hi:.2f})"], rows)
    out("")
    out("- The 2032 column holds AND-STACK at its first-product cost while the incumbent rides its curve, as the objection "
        "asks; it ignores incumbent 3D DRAM, which could do better or worse than the 8-12%/yr trend.")
    # 11j bow
    out("")
    out("### 11j. Gate-first metal bow check (RT-PROC-and-stack-02)")
    out("")
    kappa = 6 * 1.0e9 * 2.8e-6 / (180e9 * (775e-6) ** 2)
    out(f"- Stoney, 2.8 um of W at 1 GPa on 775 um Si (M = 180 GPa): bow {kappa*0.15**2/2*1e3:.2f} mm over 300 mm. The objection's "
        "1.7 mm is right, so gate-first metal is dropped: the etched stack is SiO2 / poly-SiGe / SiN (stress-tunable, NAND "
        "practice) and the write-plate metal arrives later from the slits, as NAND's replacement W does.")


def section_go(c, s, dmax2):
    h2("10. GO / NO-GO for the decisive experiment (revised after red team)")
    csn = c["c_sn"]
    leak_1s = csn * dmax2 / 1000 / 1.0
    cr_go = None
    for k in range(30, 90):
        cr = k / 100
        r = select_requirements(cr)
        if r["dv_unsel"] <= V("v_plate_max") and r["e_ipd"] <= 3.0e6:
            cr_go = cr
            break
    out(f"- **GO #1B (vertical closure coupon, month 14; the decisive gate):** on a 2-tier vertical coupon built with the "
        f"two-film notched write pocket, write-then-read works on >=2 tiers with no ring-to-read-channel short, the ring "
        f"holds <= 100 aA at 85 C with the write plate at {V('v_wp_hold')} V and select plates idle low, per-tier CR >= {cr_go:.2f}, "
        "and FIB/TEM shows the notch contact.")
    out(f"- **GO #1A (planar physics, month 9):** CR >= {cr_go:.2f} with within-tier sigma <= {V('cr_sigma')} over >=50 cells "
        f"(dV_unsel <= {V('v_plate_max')} V); each unselected cell <= {s['i_off_max']*1e15:.0f} fA at 85 C with the top level "
        f"stored; write-FET hold leakage 1e-4 tail <= {leak_1s*1e18:.0f} aA at the idle-low bias on >=1e4 devices; read-FET SS "
        f"and Vt(T) from 25 to 110 C; 4 levels in <= 1 V for >= 1 s at 85 C with the 1e-4 cell drifting <= {dmax2:.0f} mV; "
        "cross-temperature 2-b raw BER <= 1e-4 with in-page references at dT +/-10 K (characterised to +/-50 K); "
        "<= 30 mV shift after 1e8 own-tier select excursions inside one refresh interval and after 1e9 neighbour writes; "
        "retention re-measured >= 100 times on >= 1e4 cells (VRT) and read-FET RTN over 10 ns-1 s windows.")
    out(f"- **NO-GO:** no write-then-read closure on the coupon by month 18 (single-etch leg dies; coaxial fallback only), "
        f"CR < 0.40, write-FET tail > 100 aA at {V('v_wp_hold')} V hold, ring tail > 100 aA, or disturb > 1 LSB.")
    out(f"- **Prize if GO (revised):** 64 tiers x 2 b = {density_gb_mm2(64,2):.2f} Gb/mm2 "
        f"({density_gb_mm2(64,2)/V('d1b_gb_mm2'):.1f}x 1-beta), ~${usd_per_gb(64,2)[1]:.2f}/GB component "
        f"({V('comp_1b_usd_gb')/usd_per_gb(64,2)[1]:.1f}x bits/$ vs 2026 1-beta) at 1% per-tier defects.")


def inputs_block():
    h2("INPUTS (value | basis)")
    for k, (v, b) in INPUTS.items():
        vs = f"{v:.4g}" if isinstance(v, float) else str(v)
        out(f"- `{k}` = {vs} | {b}")


def main():
    out("# AND-STACK model output")
    out("")
    out("Generated by `models/and-stack.py` (pure stdlib; agent dos-and-stack, 2026-11-02). "
        "All values are first-principles estimates unless a source is given in the INPUTS block at the end.")
    section_density()
    c = section_ring()
    s = section_select(c)
    cbl, e_read, e_write = section_read(c, s)
    dmax2 = section_ber(c)
    section_retention(c, dmax2, e_read, e_write)
    section_endurance()
    section_yield()
    section_cost()
    section_redteam(c, s, dmax2)
    section_go(c, s, dmax2)
    inputs_block()
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, "w") as f:
        f.write("\n".join(LINES) + "\n")
    print(f"\n[wrote {OUT_MD}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
