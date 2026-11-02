#!/usr/bin/env python3
"""
hot-side-memory.py -- first-principles model for the HOT-SIDE MEMORY dossier (dram-moonshot stage 3).

Concept: oxide (IGZO/ZTO/IGO) 2T0C gain-cell tiers built in the backside-power-delivery (BSPDN) carrier
wafer (8-16 tiers on a trailing-node CMOS wafer, face-to-face hybrid-bonded to the logic front-side BEOL),
plus <=4 tiers inside the logic BEOL. Memory sits at near-junction temperature, so the cell must not care
about heat; defects are binned as capacity.

Owner: dos-hot-side-memory. Written 2026-11-02. Pure standard library. Run from dram-moonshot/:
    python3 models/hot-side-memory.py
Writes research/stage3/hot-side-memory_model_output.md and prints the same text. Exits 0.

Sections
  1  density and capacity (per tier-bit, per die, per GPU, vs 1-beta DDR5 and vs HBM per GPU)
  2  retention and refresh vs temperature (oxide Arrhenius vs Si halving per 10 C)
  3  multi-level margin budget -> allowed cell-to-cell level drift (the KEY UNKNOWN) and refresh interval
  4  SENSITIVITY on the key unknown: drift sigma -> raw BER, bits/cell, GB per die, GB per GPU
  5  energy per bit (read/write) vs HBM, watts and $ saved per GPU
  6  bandwidth, bond count and endurance budget
  7  thermal: memory temperature and the thermal tax of tiers sitting in the BSPDN heat path
  8  yield coupling: logic scrap from memory tiers and bonds
  9  cost per GB of carrier and BEOL tiers vs DDR5 cost and HBM price
  10 GO / NO-GO
"""

import importlib.util
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "research", "stage3", "hot-side-memory_model_output.md"))

KB_EV = 8.617333e-5  # Boltzmann constant, eV/K

# --------------------------------------------------------------------------------------------
# INPUTS: every value carries a source URL or "ESTIMATE: basis"
# --------------------------------------------------------------------------------------------
INPUTS = {
    # ---- cell and array geometry
    "F_nm": (40.0, "ESTIMATE: ArF-immersion single exposure (80 nm pitch), no EUV; concept card (FINAL_CONCEPTS.json)"),
    "cell_F2": (10.0, "ESTIMATE: vertical 2T0C ~8-12F2 per A3_research_frontier.md s2.1; planar is ~24F2"),
    "array_eff_carrier": (0.50, "ESTIMATE: carrier is a CMOS wafer, so SAs/decoders sit under the array (CMOS-under-array); 1-beta DDR5 is 0.51 (A1 model)"),
    "array_eff_beol": (0.30, "ESTIMATE: all-oxide n-only periphery 3-5x Si area; Stage 2 critique of I-02936 gives 25-35%"),
    "ecc_overhead": (36.0 / 32.0, "ESTIMATE: tier-orthogonal RS(36,32) erasure code (I-00729) = 12.5% parity"),
    "die_mm2": (800.0, "ESTIMATE: reticle-class accelerator compute die"),
    "dies_per_gpu": (2, "ESTIMATE: Blackwell/Rubin-class GPUs pair two reticle-sized compute dies [training knowledge]"),
    "d_1beta_Gb_mm2": (0.447, "models/dram_cell_physics.py (16 Gb / 35.83 mm2 Micron D1b); task frame ~0.44"),
    "hbm_GB_per_gpu": (288.0, "https://www.guru3d.com/story/nvidia-details-rubin-gpu-architecture-with-hbm4-nvlink-6-and-336-billion-transistors/ (Rubin 288 GB HBM4, 8 stacks)"),
    "hbm_TBps_per_gpu": (22.0, "https://www.guru3d.com/story/nvidia-details-rubin-gpu-architecture-with-hbm4-nvlink-6-and-336-billion-transistors/ (22 TB/s; 19.2 TB/s per https://pasqualepillitteri.it/news/27545/nvidia-ritira-22-tbs-vera-rubin-hbm4-nvlink-6, unverified)"),
    "tier_thick_um": (0.20, "ESTIMATE: IMECAS vertical 2T0C channel height ~120 nm (Tom's Hardware via B-phase sources) + isolation"),
    # ---- retention and temperature
    "t_ret_95C_s": (200.0, "https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234 (imec EDL 2025: >200 s at 95 C, Lg 40 nm)"),
    "dV_ret_criterion_mV": (100.0, "ESTIMATE: level loss that defines the reported retention time (criterion not in snippet)"),
    "Ea_ret_eV": (0.8, "ESTIMATE: thermally activated oxide off-state/interface leakage; swept 0.5-1.1 eV in sensitivity"),
    "tail_leak_mult": (3.0, "ESTIMATE: 1e-4 tail cell leaks 3x the reported (typical) cell"),
    "si_ret_85C_s": (0.064, "models/dram_cell_physics.py (JEDEC 64 ms; 32 ms above 85 C)"),
    "si_halving_C": (10.0, "models/dram_cell_physics.py (retention halves per ~10 C, GIDL/junction tail)"),
    "C_SN_fF": (0.15, "ESTIMATE: read-transistor gate as storage node at F=40 nm; Stage 2 critique of I-11532 (~0.15 fF node)"),
    # ---- multi-level margin
    "window_mV": (600.0, "ESTIMATE: usable storage-node swing after WWL kickback, inside a <=1 V read range; IMECAS shows 8 levels (3 b) in its window"),
    "sigma_place_mV": (10.0, "ESTIMATE: write-verify placement resolution (NAND ISPP-like)"),
    "sigma_read_mV": (8.0, "ESTIMATE: CDS sense residual; MARGIN STACK budgets <=13 mV"),
    "raw_ber_target": (1e-4, "RAW-BER CONTRACT concept (FINAL_CONCEPTS.md rank 4): BCH t=8 per 512 b absorbs 1e-4"),
    "drift_time_exp": (0.20, "ESTIMATE: BTI-type drift grows ~t^0.1-0.3; 0.2 used"),
    # ---- energy
    "E_hbm_pJ": (3.5, "https://arxiv.org/pdf/2602.18568 (HBM3E 3.44 pJ/b) and https://eu.36kr.com/en/p/4002393085071497 (HBM4 3-4 pJ/b)"),
    "V_array": (0.9, "ESTIMATE: oxide bitline rail"),
    "V_logic": (0.75, "ESTIMATE: logic-side signalling rail"),
    "V_wwl_swing": (2.2, "ESTIMATE: WWL from negative hold (-0.5 V, imec EDL 2025 uses negative hold) to ~1.7 V"),
    "V_rwl_swing": (1.2, "ESTIMATE"),
    "pump_eff": (0.45, "models/dram_cell_physics.py VPP pump efficiency"),
    "cells_per_rbl": (64, "ESTIMATE: short local read bitline (A3 s3.2 sizes 64-cell RBL at ~11 fF)"),
    "c_bl_per_cell_fF": (0.08, "ESTIMATE"),
    "c_bl_fixed_fF": (3.0, "ESTIMATE: SA input + via"),
    "dV_rbl_V": (0.3, "ESTIMATE: current-mode RBL swing for MLC"),
    "cells_per_row": (256, "ESTIMATE: page = 256 cells"),
    "c_wl_per_cell_fF": (0.16, "ESTIMATE: gate + wire per cell"),
    "E_sa_cmp_fJ": (3.0, "ESTIMATE: one latch comparison in carrier CMOS (28-65 nm class)"),
    "E_decode_fJ_bit": (2.0, "ESTIMATE: row/column decode amortized per bit"),
    "L_local_mm": (0.10, "ESTIMATE: subarray-to-bond data line in the tier"),
    "c_wire_pF_mm": (0.20, "ESTIMATE: on-chip wire capacitance"),
    "C_bond_via_fF": (10.0, "ESTIMATE: 1-2 um hybrid-bond pad ~2 fF + 15-level BEOL via stack ~8 fF"),
    "activity": (0.5, "ESTIMATE: data toggle factor"),
    "E_ctrl_fJ_bit": (50.0, "ESTIMATE: logic-side controller + SRAM staging write/read"),
    "L_deliver_near_mm": (1.0, "ESTIMATE: data placed above its consuming SM cluster"),
    "L_deliver_hbm_mm": (8.0, "ESTIMATE: HBM PHY at die edge to consuming SM"),
    "write_verify_iters": (3.0, "ESTIMATE: 2-b write-verify loop"),
    "write_share": (0.20, "ESTIMATE: share of near-tier traffic that is writes (KV append, activations)"),
    "overhead_factor": (2.0, "ESTIMATE: unmodeled periphery/timing/control, as A1 periph_overhead"),
    "hbm_util": (0.60, "ESTIMATE: average HBM bandwidth utilization of a decode-heavy accelerator"),
    "traffic_frac": (0.50, "ESTIMATE: share of HBM traffic served by the near tier (TP weight slice + hot KV); swept 0.2-0.9"),
    "pue": (1.25, "ESTIMATE: liquid-cooled AI hall"),
    "usd_kwh": (0.08, "ESTIMATE: U.S. industrial power"),
    "usd_per_W_dc": (12.0, "ESTIMATE: AI datacenter build cost ~$10-12M per MW of IT load"),
    "years": (5.0, "ESTIMATE: accelerator service life"),
    "E_si_refresh_fJ": (None, "models/dram_cell_physics.py refresh_energy_per_bit_fJ() (~46 fJ), imported at run time"),
    "E_oxide_refresh_fJ": (60.0, "ESTIMATE: gain-cell read + write-verify per refreshed 2-b cell, per bit"),
    # ---- bandwidth / endurance
    "t_cycle_ns": (20.0, "ESTIMATE: 2-b sense 8-15 ns (A3 s3.2) + precharge"),
    "gbps_per_bond": (1.0, "ESTIMATE: ~1 GHz SDR per bond, no PHY"),
    "bond_pitch_um": (1.5, "ESTIMATE: mature W2W; imec shows 300-400 nm (https://www.imec-publications.be/entities/publication/6228fcc8-685e-4e72-83ba-3cb478415500/full)"),
    "endurance_cycles": (1e12, "https://imec-publications.be/entities/publication/948b2190-065d-48d2-a9b9-4f4ecd22c234 (>1e12 cycles, a measured lower bound)"),
    # ---- thermal
    "q_avg_W_mm2": (1.0, "ESTIMATE: concept card (~1 W/mm2 accelerator average)"),
    "q_hot_W_mm2": (10.0, "ESTIMATE: hotspots ~1 kW/cm2 per Stage 2 critique of I-11538"),
    "k_tier_W_mK": (1.4, "ESTIMATE: SiO2-like tier dielectric"),
    "k_cu_W_mK": (400.0, "ESTIMATE: bulk Cu"),
    "via_fill": (0.03, "ESTIMATE: thermal-via area fraction through the tier stack"),
    "front_beol_um": (10.0, "ESTIMATE: logic front-side BEOL between devices and the bond"),
    "k_beol_W_mK": (2.0, "ESTIMATE: low-k + Cu vias, vertical effective"),
    "bspdn_hotspot_penalty_C": (14.0, "https://arxiv.org/pdf/2508.02284v1 (BSPDN hotspots up to ~14 C hotter; attribution uncertain, via snippet)"),
    "Tj_design_C": (105.0, "ESTIMATE: accelerator junction design point"),
    # ---- yield
    "p_kill_tier": (0.001, "ESTIMATE: concept spec <=0.1% logic-killing shorts per tier"),
    "p_kill_bond": (0.001, "ESTIMATE: concept spec <=0.1% per bond"),
    "n_beol_tiers": (4, "concept cap (<=4 BEOL tiers)"),
    "logic_die_usd": (800.0, "ESTIMATE: ~$30k N2/A16-class wafer / ~38 good 800 mm2 dies [training knowledge on N2 wafer price]"),
    # ---- cost
    "carrier_cmos_usd": (1800.0, "ESTIMATE: 65 nm-class foundry CMOS wafer for periphery-under-array"),
    "blank_carrier_usd": (150.0, "ESTIMATE: prime 300 mm Si carrier it replaces"),
    "tier_usd": (300.0, "ESTIMATE: per tier per wafer: ~3 ArFi single-exposure passes + ALD/sputter, etch, CMP"),
    "beol_tier_usd": (450.0, "ESTIMATE: same tier done inside a leading-edge logic fab (higher overhead)"),
    "hybrid_bond_test_usd": (500.0, "ESTIMATE: hybrid-bond (vs fusion) pad CMP/alignment + carrier test"),
    "capacity_yield": (0.90, "ESTIMATE: fraction of bits shipping after fail-soft binning"),
    "ddr5_usd_GB": (1.48, "task frame / ram-venture models/dram_cost_stack.py (1-beta DDR5 component cost)"),
    "hbm3e_usd_GB": (12.0, "https://capitalandcompute.net/memory-prices/hbm/ (HBM3E ~$12/GB contract, Jul 2026)"),
    "hbm4_usd_GB": (16.0, "https://capitalandcompute.net/memory-prices/hbm/ (HBM4 ~$16/GB 2H26)"),
    "wafer_mm": (300.0, "standard"),
}


def V(k):
    return INPUTS[k][0]


LINES = []


def out(s=""):
    LINES.append(s)


def hr(title):
    out("")
    out("## " + title)
    out("")


def table(header, rows):
    out("| " + " | ".join(header) + " |")
    out("|" + "|".join(["---"] * len(header)) + "|")
    for r in rows:
        out("| " + " | ".join(str(x) for x in r) + " |")
    out("")


def qfunc(x):
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def qinv(p):
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if qfunc(mid) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def load_a1():
    """Reuse the phase-A1 model for the Si refresh energy per bit."""
    try:
        spec = importlib.util.spec_from_file_location("dram_cell_physics", os.path.join(HERE, "dram_cell_physics.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        e, _, _ = m.refresh_energy_per_bit_fJ()
        return e, "imported from models/dram_cell_physics.py"
    except Exception as exc:  # pragma: no cover
        return 46.0, f"fallback 46 fJ (import failed: {exc})"


# --------------------------------------------------------------------------------------------
# 1. Density and capacity
# --------------------------------------------------------------------------------------------
def cell_um2():
    return V("cell_F2") * (V("F_nm") * 1e-3) ** 2


def gb_per_mm2_tierbit(eff):
    """User Gb/mm2 per (tier x bit), ECC parity removed."""
    return 1e6 / cell_um2() * eff / V("ecc_overhead") / 1e9


def die_GB(tiers_c, bits_c, tiers_b=0, bits_b=0):
    gc = gb_per_mm2_tierbit(V("array_eff_carrier")) * tiers_c * bits_c * V("die_mm2") / 8
    gb = gb_per_mm2_tierbit(V("array_eff_beol")) * tiers_b * bits_b * V("die_mm2") / 8
    return gc, gb


def section_density():
    hr("1. Density and capacity")
    a = cell_um2()
    out(f"Cell: {V('cell_F2'):.0f}F2 at F = {V('F_nm'):.0f} nm = {a:.4f} um2 "
        f"({1e6/a/1e6:.1f} Mcells/mm2 per tier). ECC parity {100*(V('ecc_overhead')-1):.1f}%.")
    out(f"Per tier-bit: carrier (eff {V('array_eff_carrier'):.2f}) {gb_per_mm2_tierbit(V('array_eff_carrier')):.4f} Gb/mm2; "
        f"BEOL all-oxide periphery (eff {V('array_eff_beol'):.2f}) {gb_per_mm2_tierbit(V('array_eff_beol')):.4f} Gb/mm2; "
        f"1-beta DDR5 = {V('d_1beta_Gb_mm2'):.3f} Gb/mm2.")
    out("")
    rows = []
    configs = [
        ("carrier 8 tiers x 1 b", 8, 1, 0, 0),
        ("carrier 8 tiers x 2 b", 8, 2, 0, 0),
        ("carrier 16 tiers x 1 b", 16, 1, 0, 0),
        ("carrier 16 tiers x 2 b", 16, 2, 0, 0),
        ("BEOL only, 4 tiers x 1 b", 0, 0, 4, 1),
        ("BEOL only, 4 tiers x 2 b", 0, 0, 4, 2),
        ("carrier 16 x 2 b + BEOL 4 x 2 b", 16, 2, 4, 2),
    ]
    res = {}
    for name, tc, bc, tb, bb in configs:
        gc, gb = die_GB(tc, bc, tb, bb)
        g = gc + gb
        dens = g * 8 / V("die_mm2")
        gpu = g * V("dies_per_gpu")
        rows.append((name, f"{dens:.3f}", f"{dens/V('d_1beta_Gb_mm2'):.2f}x", f"{g:.0f}", f"{gpu:.0f}",
                     f"{100*gpu/V('hbm_GB_per_gpu'):.0f}%"))
        res[name] = g
    table(["Configuration", "Gb/mm2 (footprint)", "vs 1-beta", "GB per 800 mm2 die", "GB per 2-die GPU",
           "vs 288 GB HBM/GPU"], rows)
    out("Reading: the carrier tier is a capacity-class near memory (tens of GB per die), not an HBM replacement; "
        "at 16 x 2 b it reaches ~2x 1-beta footprint density because it stacks under a die that exists anyway.")
    return res


# --------------------------------------------------------------------------------------------
# 2. Retention vs temperature
# --------------------------------------------------------------------------------------------
def t_ret_oxide(tc, ea=None, t95=None):
    ea = V("Ea_ret_eV") if ea is None else ea
    t95 = V("t_ret_95C_s") if t95 is None else t95
    return t95 * math.exp(ea / KB_EV * (1 / (tc + 273.15) - 1 / (95 + 273.15)))


def t_ret_si(tc):
    return V("si_ret_85C_s") / 2 ** ((tc - 85) / V("si_halving_C"))


def section_retention():
    hr("2. Retention and refresh vs temperature (1 b, reported-cell basis)")
    rows = []
    for tc in (85, 95, 105, 115, 125):
        to = t_ret_oxide(tc)
        ts = t_ret_si(tc)
        rows.append((tc, f"{ts*1e3:.1f} ms", f"{to:.0f} s", f"{to/ts:,.0f}x",
                     f"{t_ret_oxide(tc, 0.5):.0f} / {t_ret_oxide(tc, 1.1):.0f} s"))
    table(["T (C)", "Si 1T1C refresh", "Oxide 2T0C (Ea 0.8 eV)", "Fewer refreshes", "Oxide at Ea 0.5 / 1.1 eV"], rows)
    i_typ = V("C_SN_fF") * 1e-15 * V("dV_ret_criterion_mV") * 1e-3 / V("t_ret_95C_s")
    out(f"Implied storage-node leakage of the reported cell at 95 C: C_SN x dV / t = {V('C_SN_fF')} fF x "
        f"{V('dV_ret_criterion_mV'):.0f} mV / {V('t_ret_95C_s'):.0f} s = {i_typ*1e21:.0f} zA "
        f"(imec 2020 extracted Ioff 3e-19 A/um, i.e. ~12 zA for a 40 nm wide device).")
    return i_typ


# --------------------------------------------------------------------------------------------
# 3. Multi-level margin budget
# --------------------------------------------------------------------------------------------
def raw_ber(bits, sigma_drift, offset_mV=0.0, window=None):
    window = V("window_mV") if window is None else window
    n = 2 ** bits
    half = window / (n - 1) / 2.0 - offset_mV
    sig = math.sqrt(V("sigma_place_mV") ** 2 + V("sigma_read_mV") ** 2 + sigma_drift ** 2)
    if half <= 0:
        return 0.5
    ser = 2.0 * (n - 1) / n * qfunc(half / sig)
    return ser / bits


def allowed_sigma_drift(bits, window=None, offset_mV=0.0):
    window = V("window_mV") if window is None else window
    n = 2 ** bits
    k = qinv(V("raw_ber_target") * bits * n / (2.0 * (n - 1)))
    half = window / (n - 1) / 2.0 - offset_mV
    s_tot = half / k
    rest = s_tot ** 2 - V("sigma_place_mV") ** 2 - V("sigma_read_mV") ** 2
    return math.sqrt(rest) if rest > 0 else 0.0, k


def droop_rate_tail_mV_s(tc):
    """Tail-cell storage-node droop rate at temperature tc (mV/s)."""
    return V("tail_leak_mult") * V("dV_ret_criterion_mV") / t_ret_oxide(tc)


def refresh_interval(bits, sigma_1s, tc):
    """Longest hold time t (s) at which raw BER <= target, with sigma growing ~t^n and tail droop offset."""
    lo, hi = 1e-3, 1e6
    if raw_ber(bits, sigma_1s * (lo ** V("drift_time_exp")), droop_rate_tail_mV_s(tc) * lo) > V("raw_ber_target"):
        return 0.0
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        b = raw_ber(bits, sigma_1s * (mid ** V("drift_time_exp")), droop_rate_tail_mV_s(tc) * mid)
        if b <= V("raw_ber_target"):
            lo = mid
        else:
            hi = mid
    return lo


def section_margin():
    hr("3. Multi-level margin budget: what drift the cell may have (raw BER 1e-4, ECC downstream)")
    out(f"Window {V('window_mV'):.0f} mV; write-verify placement sigma {V('sigma_place_mV'):.0f} mV; "
        f"sense residual sigma {V('sigma_read_mV'):.0f} mV; raw BER target {V('raw_ber_target'):.0e}.")
    out("")
    rows = []
    allowed = {}
    for b in (1, 2, 3):
        for w in (400.0, 600.0, 800.0):
            s, k = allowed_sigma_drift(b, window=w)
            if w == V("window_mV"):
                allowed[b] = s
            rows.append((b, f"{w:.0f}", f"{w/(2**b-1):.0f}", f"{k:.2f}", f"{s:.1f}"))
    table(["bits/cell", "window (mV)", "level spacing (mV)", "Q needed", "allowed drift sigma (mV)"], rows)
    out(f"At the base window the cell may drift (cell-to-cell sigma, after reference tracking of common-mode) "
        f"<= {allowed[1]:.0f} mV for 1 b, <= {allowed[2]:.0f} mV for 2 b, <= {allowed[3]:.0f} mV for 3 b. "
        "This reproduces the concept card's <=20-30 mV (2 b) spec and shows 1 b is far more forgiving.")
    out("")
    rows = []
    for tc in (105, 125):
        for b, s1 in ((1, 40.0), (2, 15.0), (2, 20.0), (3, 6.0)):
            t = refresh_interval(b, s1, tc)
            rows.append((tc, b, f"{s1:.0f}", f"{droop_rate_tail_mV_s(tc):.2f}", f"{t:,.1f} s" if t > 0 else "fails at 1 ms"))
    table(["T (C)", "bits", "drift sigma at 1 s (mV)", "tail droop (mV/s)", "refresh interval (BER<=1e-4)"], rows)
    out(f"Drift grows as t^{V('drift_time_exp')}; the tail cell leaks {V('tail_leak_mult'):.0f}x the reported cell. "
        "Refresh every few seconds to minutes is still >1,000x rarer than Si at the same temperature.")
    lk = {}
    for b in (1, 2):
        s_all, _ = allowed_sigma_drift(b)
        for t in (1.0, 10.0):
            budget_mV = 0.5 * (V("window_mV") / (2 ** b - 1) / 2.0)  # give half the half-spacing to droop
            lk[(b, t)] = V("C_SN_fF") * 1e-15 * budget_mV * 1e-3 / t
    out(f"Leakage ceiling for the 1e-4 tail cell (half the half-spacing given to droop, C_SN {V('C_SN_fF')} fF): "
        f"1 b: {lk[(1,1.0)]*1e18:.1f} aA (1 s), {lk[(1,10.0)]*1e18:.2f} aA (10 s); "
        f"2 b: {lk[(2,1.0)]*1e18:.1f} aA (1 s), {lk[(2,10.0)]*1e18:.2f} aA (10 s).")
    return allowed


# --------------------------------------------------------------------------------------------
# 4. Sensitivity on the key unknown
# --------------------------------------------------------------------------------------------
def section_sensitivity(allowed):
    hr("4. SENSITIVITY on the key unknown: post-sequence level drift sigma over 1 s at 105 C")
    rows = []
    for s in (5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100):
        b1, b2, b3 = raw_ber(1, s), raw_ber(2, s), raw_ber(3, s)
        bmax = 0
        for b in (1, 2, 3):
            if raw_ber(b, s) <= V("raw_ber_target"):
                bmax = b
        if bmax:
            gc, _ = die_GB(16, bmax)
            gc8, _ = die_GB(8, bmax)
            cap = f"{gc8:.0f} / {gc:.0f}"
            gpu = f"{gc*V('dies_per_gpu'):.0f}"
        else:
            cap, gpu = "0 (NO-GO)", "0"
        rows.append((s, f"{b1:.1e}", f"{b2:.1e}", f"{b3:.1e}", bmax, cap, gpu))
    table(["drift sigma (mV)", "raw BER 1 b", "raw BER 2 b", "raw BER 3 b", "max bits/cell",
           "GB/die (8 / 16 carrier tiers)", "GB/GPU (16 tiers)"], rows)
    out(f"Thresholds at a {V('window_mV'):.0f} mV window: 3 b needs <= {allowed[3]:.0f} mV, 2 b <= {allowed[2]:.0f} mV, "
        f"1 b <= {allowed[1]:.0f} mV. The energy win does not depend on bits/cell; capacity does.")
    out("")
    rows = []
    for w in (300.0, 400.0, 600.0, 800.0):
        s2, _ = allowed_sigma_drift(2, window=w)
        s1, _ = allowed_sigma_drift(1, window=w)
        rows.append((f"{w:.0f}", f"{s1:.0f}", f"{s2:.0f}"))
    table(["window (mV)", "allowed sigma 1 b (mV)", "allowed sigma 2 b (mV)"], rows)
    out("Second unknown: the usable window after kickback and PBTI. Below ~400 mV, 2 b needs drift under ~15 mV.")


# --------------------------------------------------------------------------------------------
# 5. Energy
# --------------------------------------------------------------------------------------------
def near_energy():
    c_rbl = V("cells_per_rbl") * V("c_bl_per_cell_fF") + V("c_bl_fixed_fF")  # fF
    bits = 2
    e_rbl_cell = c_rbl * V("V_array") * V("dV_rbl_V")  # fJ per cell read
    e_sa_cell = (2 ** bits - 1) * V("E_sa_cmp_fJ")
    c_wl = V("cells_per_row") * V("c_wl_per_cell_fF")
    e_rwl_cell = c_wl * V("V_rwl_swing") ** 2 / V("cells_per_row")
    e_cell_read_bit = (e_rbl_cell + e_sa_cell + e_rwl_cell) / bits
    e_local = V("activity") * V("L_local_mm") * V("c_wire_pF_mm") * 1e3 * V("V_array") ** 2
    e_bond = V("activity") * V("C_bond_via_fF") * V("V_logic") ** 2
    e_read_port = (e_cell_read_bit + V("E_decode_fJ_bit") + e_local + e_bond) * V("overhead_factor") + V("E_ctrl_fJ_bit")
    # write: WBL full swing + WWL pumped, repeated per verify iteration with a verify read
    e_wbl = c_rbl * V("V_array") ** 2
    e_wwl = c_wl * V("V_wwl_swing") ** 2 / V("pump_eff") / V("cells_per_row")
    e_write_cell = V("write_verify_iters") * (e_wbl + e_wwl + e_rbl_cell + e_sa_cell)
    e_write_port = (e_write_cell / bits + V("E_decode_fJ_bit") + e_local + e_bond) * V("overhead_factor") + V("E_ctrl_fJ_bit")
    e_mix_port = (1 - V("write_share")) * e_read_port + V("write_share") * e_write_port
    e_wire_mm = V("activity") * V("c_wire_pF_mm") * 1e3 * V("V_logic") ** 2  # fJ/bit/mm
    return dict(c_rbl=c_rbl, e_cell_read_bit=e_cell_read_bit, e_local=e_local, e_bond=e_bond,
                e_read_port=e_read_port, e_write_port=e_write_port, e_mix_port=e_mix_port, e_wire_mm=e_wire_mm)


def section_energy(si_refresh_fJ, si_src, cap_GB):
    hr("5. Energy per bit and watts saved")
    e = near_energy()
    out(f"Read bitline {e['c_rbl']:.1f} fF; cell+SA+RWL per bit {e['e_cell_read_bit']:.1f} fJ; local data line "
        f"{e['e_local']:.1f} fJ; bond+via stack {e['e_bond']:.1f} fJ; x{V('overhead_factor'):.0f} unmodeled periphery; "
        f"+{V('E_ctrl_fJ_bit'):.0f} fJ logic-side controller/SRAM.")
    out("")
    near_port = e["e_mix_port"] / 1e3
    near_deliv = near_port + e["e_wire_mm"] * V("L_deliver_near_mm") / 1e3
    hbm_port = V("E_hbm_pJ")
    hbm_deliv = hbm_port + e["e_wire_mm"] * V("L_deliver_hbm_mm") / 1e3
    rows = [
        ("near tier read, to controller port", f"{e['e_read_port']/1e3:.3f}"),
        ("near tier 2-b write-verify, to port", f"{e['e_write_port']/1e3:.3f}"),
        (f"near tier mix ({100*V('write_share'):.0f}% writes), to port", f"{near_port:.3f}"),
        (f"near tier delivered to SM ({V('L_deliver_near_mm'):.0f} mm)", f"{near_deliv:.3f}"),
        ("concept card claim", "0.3"),
        ("HBM3E/HBM4, to PHY/controller", f"{hbm_port:.2f}"),
        (f"HBM delivered to SM (+{V('L_deliver_hbm_mm'):.0f} mm NoC)", f"{hbm_deliv:.2f}"),
    ]
    table(["Path", "pJ/bit"], rows)
    out(f"Ratio at the port: {hbm_port/near_port:.0f}x (model) / {hbm_port/0.3:.0f}x (card's 0.3 pJ/b). "
        f"Delivered: {hbm_deliv/near_deliv:.0f}x.")
    out("")
    # watts saved
    use = max(near_deliv, 0.3)  # conservative: never better than the card's claim
    rows = []
    for bw in (V("hbm_TBps_per_gpu"), 19.2, 8.0):
        for f in (0.2, V("traffic_frac"), 0.9):
            bits_s = bw * 1e12 * 8 * V("hbm_util") * f
            w = bits_s * (hbm_deliv - use) * 1e-12
            kwh = w * 8766 * V("years") * V("pue") / 1e3
            rows.append((f"{bw:.1f}", f"{f:.1f}", f"{w:.0f}", f"{kwh:,.0f}", f"${kwh*V('usd_kwh'):,.0f}",
                         f"${w*V('usd_per_W_dc'):,.0f}"))
    table(["HBM TB/s", "traffic share on near tier", "W saved/GPU", f"kWh over {V('years'):.0f} yr (PUE)",
           "electricity $", "DC capex freed ($/W)"], rows)
    full = V("hbm_TBps_per_gpu") * 1e12 * 8 * (V("E_hbm_pJ") - 0.3) * 1e-12
    out(f"Card framing (100% of traffic at full 22 TB/s, port to port 3.5 -> 0.3 pJ/b): {full:.0f} W per GPU. "
        f"The utilization- and share-weighted figure above is the honest one; delivered-energy accounting "
        f"uses max(model, 0.3 pJ/b) = {use:.2f} pJ/b for the near tier.")
    out("")
    # refresh
    bits = cap_GB * 8e9
    rows = []
    for tc in (105, 125):
        p_si = bits * si_refresh_fJ * 1e-15 / t_ret_si(tc)
        t_ox = refresh_interval(2, 15.0, tc)
        p_ox = bits * V("E_oxide_refresh_fJ") * 1e-15 / t_ox if t_ox > 0 else float("inf")
        rows.append((tc, f"{t_ret_si(tc)*1e3:.0f} ms", f"{p_si:.2f} W", f"{t_ox:.1f} s", f"{p_ox*1e3:.2f} mW"))
    table([f"T (C), {cap_GB:.0f} GB", "Si refresh period", "Si refresh power", "oxide 2-b interval (15 mV)",
           "oxide refresh power"], rows)
    out(f"Si refresh energy per bit {si_refresh_fJ:.0f} fJ ({si_src}). Refresh watts are small either way; "
        "what Si loses at 105-125 C is availability (tRFC/tREFI) and the retention tail, not power.")
    return near_port, near_deliv, hbm_deliv


# --------------------------------------------------------------------------------------------
# 6. Bandwidth, bonds, endurance
# --------------------------------------------------------------------------------------------
def section_bandwidth(near_port, cap_GB):
    hr("6. Bandwidth, bond count, endurance")
    bw_near = V("traffic_frac") * V("hbm_TBps_per_gpu") * 1e12 * 8 / V("dies_per_gpu")  # b/s per die at peak
    sub_cells = 64 * V("cells_per_row")
    sub_bits_per_cycle = V("cells_per_row") * 2
    sub_rate = sub_bits_per_cycle / (V("t_cycle_ns") * 1e-9)
    n_active = bw_near / sub_rate
    sub_area_um2 = sub_cells * cell_um2() / V("array_eff_carrier")
    n_sub_tier = V("die_mm2") * 1e6 / sub_area_um2
    bonds_needed = bw_near / (V("gbps_per_bond") * 1e9)
    bonds_mm2 = 1e6 / V("bond_pitch_um") ** 2
    p_density = bw_near * near_port * 1e-12 / V("die_mm2")
    rows = [
        ("peak near-tier bandwidth per die", f"{bw_near/8/1e12:.1f} TB/s"),
        ("subarray (64 x 256 cells, 2 b) rate", f"{sub_rate/1e9:.1f} Gb/s"),
        ("concurrently active subarrays", f"{n_active:,.0f}"),
        ("subarrays per tier per die", f"{n_sub_tier:,.0f}"),
        ("active fraction of ONE tier", f"{100*n_active/n_sub_tier:.2f}%"),
        ("signal bonds needed (1 Gb/s each)", f"{bonds_needed:,.0f}"),
        (f"bond area at {V('bond_pitch_um')} um pitch", f"{bonds_needed/bonds_mm2:.2f} mm2 of {V('die_mm2'):.0f}"),
        ("near-tier access power density", f"{p_density*1e3:.0f} mW/mm2"),
    ]
    table(["Quantity", "Value"], rows)
    # endurance
    wr_bps = bw_near * V("write_share")
    bits_die = cap_GB * 8e9
    writes_per_cell_s = wr_bps / bits_die
    life = writes_per_cell_s * 8766 * 3600 * V("years")
    t_hot = V("endurance_cycles") * V("t_cycle_ns") * 1e-9
    out(f"Endurance: average {writes_per_cell_s:.1f} writes/cell/s -> {life:.1e} writes in {V('years'):.0f} yr "
        f"vs >= {V('endurance_cycles'):.0e} measured ({V('endurance_cycles')/life:,.0f}x headroom). A single row "
        f"rewritten every {V('t_cycle_ns'):.0f} ns would reach 1e12 in {t_hot/3600:.1f} h, so per-row write "
        "throttling or hot-buffer placement in SRAM is required; transistor-written cells have no known "
        "insulator wear-out, but BTI from write pulses accumulates.")
    out(f"Latency: no PHY or SerDes; a ~{V('t_cycle_ns'):.0f} ns array cycle plus ~5-10 ns of bond/controller "
        "puts near-tier access at ~30-40 ns vs ~100+ ns for HBM [ESTIMATE].")


# --------------------------------------------------------------------------------------------
# 7. Thermal
# --------------------------------------------------------------------------------------------
def section_thermal():
    hr("7. Thermal: where the memory sits and what it costs the logic")
    t_c = 16 * V("tier_thick_um") * 1e-6
    t_b = V("n_beol_tiers") * V("tier_thick_um") * 1e-6
    k_eff = (1 - V("via_fill")) * V("k_tier_W_mK") + V("via_fill") * V("k_cu_W_mK")
    rows = []
    for name, t in (("16 carrier tiers", t_c), ("4 BEOL tiers", t_b)):
        for q in (V("q_avg_W_mm2"), V("q_hot_W_mm2")):
            dt0 = q * 1e6 * t / V("k_tier_W_mK")
            dt1 = q * 1e6 * t / k_eff
            rows.append((name, f"{t*1e6:.1f}", f"{q:.0f}", f"{dt0:.1f}", f"{dt1:.1f}"))
    table(["Stack in heat path", "thickness (um)", "flux (W/mm2)", "dT no thermal vias (K)",
           f"dT with {100*V('via_fill'):.0f}% Cu vias (K)"], rows)
    dt_beol = V("q_avg_W_mm2") * 1e6 * V("front_beol_um") * 1e-6 / V("k_beol_W_mK")
    out(f"In BSPDN the heat sink sits on the carrier, so all logic heat crosses the front BEOL, the bond and the "
        f"carrier tiers. Memory runs ~{dt_beol:.0f} K below junction on average (front BEOL {V('front_beol_um'):.0f} um "
        f"at k {V('k_beol_W_mK')} W/mK): ~{V('Tj_design_C')-dt_beol:.0f} C at a {V('Tj_design_C'):.0f} C design Tj, and "
        f"up to ~{V('Tj_design_C')+V('bspdn_hotspot_penalty_C')-dt_beol:.0f} C over BSPDN hotspots "
        f"(+{V('bspdn_hotspot_penalty_C'):.0f} C). Test at 105 and 125 C.")
    out("NEW RED FLAG: an unvia'd 16-tier oxide stack adds ~20 K over 10 W/mm2 hotspots. Fix: ~3% Cu/W thermal-via "
        "fill (or high-k dielectrics such as AlN between tiers), or keep tiers off hotspot regions and bin that area out.")


# --------------------------------------------------------------------------------------------
# 8. Yield coupling
# --------------------------------------------------------------------------------------------
def section_yield():
    hr("8. Yield coupling: logic scrapped by memory")
    rows = []
    for p in (0.0003, 0.001, 0.003, 0.01):
        for nb in (0, 4, 16):
            y = (1 - p) ** nb * (1 - p) * (1 - p)  # BEOL tiers x bond x carrier shorts across the bond
            loss = 1 - y
            rows.append((f"{100*p:.2f}%", nb, f"{100*loss:.2f}%", f"${loss*V('logic_die_usd'):.0f}"))
    table(["kill prob per tier/bond", "BEOL tiers", "logic scrapped", "$ per logic die"], rows)
    y16 = 0.99 ** 16
    out(f"Reference: 16 monolithic tiers at 99% unrepairable yield scrap {100*(1-y16):.0f}% of logic; with fail-soft "
        "binning only logic-killing shorts count, and the carrier/BEOL split caps the BEOL count at 4.")


# --------------------------------------------------------------------------------------------
# 9. Cost per GB
# --------------------------------------------------------------------------------------------
def dies_per_wafer(a_mm2):
    d = V("wafer_mm")
    return int(math.pi * (d / 2) ** 2 / a_mm2 - math.pi * d / math.sqrt(2 * a_mm2))


def section_cost():
    hr("9. Cost per GB (incremental over a blank BSPDN carrier) vs DDR5 cost and HBM price")
    dpw = dies_per_wafer(V("die_mm2"))
    rows = []
    for tiers in (8, 16):
        for bits in (1, 2):
            gc, _ = die_GB(tiers, bits)
            cost = V("carrier_cmos_usd") + tiers * V("tier_usd") + V("hybrid_bond_test_usd") - V("blank_carrier_usd")
            gbw = dpw * gc * V("capacity_yield")
            rows.append((f"carrier {tiers} x {bits} b", f"${cost:,.0f}", f"{gc*V('capacity_yield'):.0f}",
                         f"{gbw:,.0f}", f"${cost/gbw:.2f}", f"{cost/gbw/V('ddr5_usd_GB'):.1f}x",
                         f"{V('hbm4_usd_GB')/(cost/gbw):.0f}x cheaper"))
    for bits in (1, 2):
        _, gb = die_GB(0, 0, 4, bits)
        cost = 4 * V("beol_tier_usd")
        gbw = dpw * gb * V("capacity_yield")
        rows.append((f"BEOL 4 x {bits} b", f"${cost:,.0f}", f"{gb*V('capacity_yield'):.0f}", f"{gbw:,.0f}",
                     f"${cost/gbw:.2f}", f"{cost/gbw/V('ddr5_usd_GB'):.1f}x", f"{V('hbm4_usd_GB')/(cost/gbw):.0f}x cheaper"))
    table(["Option", "added $/wafer", "GB/die shipped", "GB/wafer", "$/GB", "vs DDR5 cost $1.48", "vs HBM4 ~$16/GB"], rows)
    out(f"{dpw} gross 800 mm2 sites per 300 mm wafer. Costs are fab-cost estimates, HBM figures are prices; the point "
        "is order of magnitude: near-tier bits cost DDR5-like dollars and sit an order below HBM price.")


# --------------------------------------------------------------------------------------------
# 10. GO / NO-GO
# --------------------------------------------------------------------------------------------
def section_go(allowed):
    hr("10. GO / NO-GO for the decisive experiment")
    out("Measured on >=64 kb oxide 2T0C arrays after the FULL sequence (<=400 C tiers, 350-400 C bond anneal, thinning, "
        "400 C backside-metal + forming-gas emulation), at 105 C and 125 C:")
    out("")
    s2_400, _ = allowed_sigma_drift(2, window=400.0)
    s1_400, _ = allowed_sigma_drift(1, window=400.0)
    out(f"- **GO (2 b/cell):** cell-to-cell level drift sigma over a 1 s hold at 105 C <= {allowed[2]:.0f} mV "
        f"(raw BER <= 1e-4 in a measured >= {V('window_mV'):.0f} mV window; <= {s2_400:.0f} mV if the window is only "
        f"400 mV), which is the same as a >= 1 s 2-b refresh interval with tail droop included, AND 1e-4-tail retention >= 1 s at 125 C, AND logic "
        "ring-oscillator shift <= 1% with Vt shift <= 10 mV, AND logic-killing shorts <= 0.1% per tier and per bond.")
    out(f"- **GO at 1 b (capacity halves, energy win intact):** drift sigma {allowed[2]:.0f}-{allowed[1]:.0f} mV "
        f"({s2_400:.0f}-{s1_400:.0f} mV at a 400 mV window).")
    out(f"- **NO-GO:** drift sigma > {allowed[1]:.0f} mV ({s1_400:.0f} mV at a 400 mV window) at 1 b, OR 1e-4-tail retention < 1 s at 105 C, OR ring-oscillator "
        "shift > 1% that H-lean/In-poor process changes cannot recover. Revival: an H-blocking liner plus In-poor/IGO "
        "channel that restores <=25 mV, or a Ga-free ZTO/In2O3 channel that passes.")


def main():
    si_e, si_src = load_a1()
    INPUTS["E_si_refresh_fJ"] = (si_e, INPUTS["E_si_refresh_fJ"][1])
    out("# HOT-SIDE MEMORY: model output")
    out("")
    out("Generated by `models/hot-side-memory.py` (pure stdlib). Every input is listed in the INPUTS block of the "
        "script with a source URL or an ESTIMATE basis. Agent key: dos-hot-side-memory. 2026-11-02.")
    res = section_density()
    section_retention()
    allowed = section_margin()
    section_sensitivity(allowed)
    cap = res["carrier 16 tiers x 2 b"]
    near_port, near_deliv, hbm_deliv = section_energy(si_e, si_src, cap)
    section_bandwidth(near_port, cap)
    section_thermal()
    section_yield()
    section_cost()
    section_go(allowed)
    hr("Headline")
    g8_1, _ = die_GB(8, 1)
    g16_2, _ = die_GB(16, 2)
    w = V("hbm_TBps_per_gpu") * 1e12 * 8 * V("hbm_util") * V("traffic_frac") * (hbm_deliv - max(near_deliv, 0.3)) * 1e-12
    out(f"- Capacity: {g8_1:.0f}-{g16_2:.0f} GB per 800 mm2 die (8 x 1 b to 16 x 2 b carrier tiers), "
        f"{2*g8_1:.0f}-{2*g16_2:.0f} GB per 2-die GPU vs 288 GB HBM4.")
    out(f"- Energy: {near_port:.2f} pJ/b at the port ({near_deliv:.2f} delivered) vs {V('E_hbm_pJ')} pJ/b HBM: "
        f"~{V('E_hbm_pJ')/max(near_port,0.3):.0f}x at the card's conservative 0.3 pJ/b; ~{w:.0f} W per GPU at "
        f"{100*V('hbm_util'):.0f}% utilization and {100*V('traffic_frac'):.0f}% of traffic on the near tier.")
    out(f"- Refresh at 105 C: oxide ~{t_ret_oxide(105):.0f} s (1 b) vs Si {t_ret_si(105)*1e3:.0f} ms = "
        f"{t_ret_oxide(105)/t_ret_si(105):,.0f}x fewer refreshes.")
    out(f"- Key threshold: drift sigma <= {allowed[2]:.0f} mV (2 b) / <= {allowed[1]:.0f} mV (1 b) over 1 s at 105 C, "
        "after the post-bond thermal/hydrogen sequence.")
    hr("Appendix: INPUTS (value, source or ESTIMATE basis)")
    rows = []
    for k, (v, src) in INPUTS.items():
        vs = f"{v:.4g}" if isinstance(v, float) else str(v)
        rows.append((k, vs, src.replace("|", "/")))
    table(["Input", "Value", "Source / basis"], rows)
    text = "\n".join(LINES) + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(text)
    print(text)
    print(f"[written to {OUT}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
