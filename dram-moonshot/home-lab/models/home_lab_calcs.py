#!/usr/bin/env python3
"""
home_lab_calcs.py -- first-principles numbers behind home-lab/FIRST_PRINCIPLES.md (track T5).

Every number in FIRST_PRINCIPLES.md comes from this script. Other home-lab guides cite it as
"home_lab_calcs.py section N". Each section prints the same law twice: once at CHIP scale
(numbers from the dram-moonshot study) and once at BENCH scale (parts you can buy).

Owner: track T5 (dram-moonshot home-lab). Written 2026-11-03. Python 3 standard library + numpy only.

Usage (from any folder):
  python3 home_lab_calcs.py               # print every section
  python3 home_lab_calcs.py --section 14  # print one section (0-15)
  python3 home_lab_calcs.py --selftest    # check formulas against known values and run the
                                          # tail-statistics and retention-fit pipeline on SYNTHETIC data
Exit code 0 on success. Nothing is written to disk.

Evidence tags used in the printout:
  [DATASHEET]  a manufacturer datasheet value
  [REPORTED]   a paper, press release or study file (search snippets count; see FIRST_PRINCIPLES.md Sources)
  [ESTIMATE]   our own arithmetic or an assumed bench value
  [UNVERIFIED] a textbook or prior-knowledge value not re-checked this session
  [STUDY]      a number from the dram-moonshot study models (models/*.py), itself [MODEL]/[ESTIMATE]
"""

import argparse
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True  # do not leave __pycache__ files in the study's models/ folder

# --------------------------------------------------------------------------------------------
# Link to the study's shared cell-physics model, so overlapping numbers are identical.
# --------------------------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
STUDY_MODELS = os.path.normpath(os.path.join(HERE, "..", "..", "models"))
try:
    sys.path.insert(0, STUDY_MODELS)
    import dram_cell_physics as dcp  # noqa: E402

    _I = dcp.INPUTS
    _d_cx = _I["user_gbit"] / _I["die_cxmt_g4_mm2"]
    _d_1b = _I["user_gbit"] / _I["die_1b_mm2"]
    _cell_1b = _I["cell_cxmt_g4_um2"] * _d_cx / _d_1b
    CS_1B_FF = dcp.cap_pillar_fF(dcp.hex_pitch_nm(_cell_1b) - _I["cap_gap_nm"], _I["cap_height_nm"], _I["eot_nm"])
    CBL_FF = dcp.c_bitline_fF(_I["cells_per_bl"])
    V_ARRAY = _I["v_array"]
    E_REFRESH_FJ = dcp.refresh_energy_per_bit_fJ()[0]
    T_REF_S = _I["t_ref_s"]
    DV_MIN_MV = _I["dv_min_mV"]
    DIE_BITS = _I["user_gbit"] * _I["ecc_factor"] * 1e9
    STUDY_LINK = "models/dram_cell_physics.py (imported live)"
    CBL_128_FF = dcp.c_bitline_fF(128)
except Exception:  # pragma: no cover - fallback if this file is moved out of the study tree
    CS_1B_FF, CBL_FF, V_ARRAY, E_REFRESH_FJ = 5.42, 34.72, 1.05, 45.9
    T_REF_S, DV_MIN_MV, DIE_BITS = 0.064, 50.0, 16 * 1.0625e9
    STUDY_LINK = "fallback copies of models/dram_cell_physics.py outputs (2026-11-01 run)"
    CBL_128_FF = 11.68

# --------------------------------------------------------------------------------------------
# CONSTANTS: name -> (value, unit, source, tag)
# --------------------------------------------------------------------------------------------
CONST = {
    "k_B": (1.380649e-23, "J/K", "SI exact value (BIPM SI Brochure, 9th ed., 2019)", "[REPORTED]"),
    "k_B_eV": (8.617333262e-5, "eV/K", "k_B / e, SI exact values (BIPM SI Brochure)", "[REPORTED]"),
    "q": (1.602176634e-19, "C", "SI exact value (BIPM SI Brochure)", "[REPORTED]"),
    "eps0": (8.8541878128e-12, "F/m", "CODATA 2018 recommended value", "[UNVERIFIED]"),
    "h": (6.62607015e-34, "J s", "SI exact value (BIPM SI Brochure)", "[REPORTED]"),
    "m0": (9.1093837015e-31, "kg", "CODATA 2018 electron mass", "[UNVERIFIED]"),
    "c": (299792458.0, "m/s", "SI exact value", "[REPORTED]"),
}
KB = CONST["k_B"][0]
KB_EV = CONST["k_B_eV"][0]
QE = CONST["q"][0]
EPS0 = CONST["eps0"][0]
HPL = CONST["h"][0]
M0 = CONST["m0"][0]
C_LIGHT = CONST["c"][0]

T_ROOM = 298.15   # 25 C
T_300 = 300.0
T_85 = 358.15     # 85 C, DRAM's standard hot corner
T_105 = 378.15
T_125 = 398.15

# Activation energy implied by the industry rule of thumb 'retention halves every 10 C', at 85 C [ESTIMATE].
# (JEDEC itself only doubles the refresh rate above 85 C; the 10 C rule is not a JEDEC rule.)
EA_10C_RULE = math.log(2) * 8.617333262e-5 / (1 / 358.15 - 1 / 368.15)

# Semiconductor inputs: name -> (Eg eV, Nc cm^-3 at 300 K, Nv cm^-3 at 300 K, source, tag)
SEMIS = {
    "Si": (1.12, 2.86e19, 2.66e19, "Sze & Ng, Physics of Semiconductor Devices, 3rd ed. (2007), App. G", "[UNVERIFIED]"),
    "a-IGZO (3.05 eV)": (3.05, None, None, "optical gap ~3.05 eV, U. Michigan a-IGZO TFT photosensitivity paper", "[REPORTED]"),
    "IGZO (3.2 eV)": (3.2, None, None, "mid-range of quoted IGZO gaps (3.0-3.5 eV); 3.13 eV used as a reference in arXiv 1812.11333", "[REPORTED]"),
    "ZnO (3.37 eV)": (3.37, None, None, "textbook ZnO room-temperature gap", "[UNVERIFIED]"),
    "wide oxide (3.5 eV)": (3.5, None, None, "upper end of the task's 3.0-3.5 eV range", "[ESTIMATE]"),
}
OXIDE_ME = (0.2, 0.34)          # electron effective mass range, m*/m0 [REPORTED via snippets: 0.20 computed a-IGZO, ~0.33 c-IGZO]
OXIDE_NV_RANGE = (1e19, 1e21)   # valence-band effective density, cm^-3 [ESTIMATE: holes are localized; wide bound]

# Hot-side local read bitline: 64 cells x 0.08 fF + 3 fF (models/hot-side-memory.py near_energy) [STUDY]
RBL_HOT_FF = 64 * 0.08 + 3.0

# Study numbers (dram-moonshot). [STUDY]
STUDY = {
    "Cs_1b_fF": (CS_1B_FF, STUDY_LINK + ", section 2 (1-beta pillar capacitor)"),
    "Cbl_fF": (CBL_FF, STUDY_LINK + ", 512 cells per bitline"),
    "V_array": (V_ARRAY, STUDY_LINK + ", VARY"),
    "E_refresh_fJ": (E_REFRESH_FJ, STUDY_LINK + ", section 5"),
    "t_ref_s": (T_REF_S, "JEDEC 64 ms window, via " + STUDY_LINK),
    "die_bits": (DIE_BITS, "16 Gb die incl. on-die ECC bits, via " + STUDY_LINK),
    "C_SN_fF": (0.15, "models/hot-side-memory.py C_SN_fF (oxide 2T0C storage node at F=40 nm) [ESTIMATE]"),
    "window_mV": (600.0, "models/hot-side-memory.py window_mV [ESTIMATE]"),
    "c_wire_pF_mm": (0.20, "models/hot-side-memory.py c_wire_pF_mm [ESTIMATE]"),
    "C_bond_via_fF": (10.0, "models/hot-side-memory.py C_bond_via_fF [ESTIMATE]"),
    "V_logic": (0.75, "models/hot-side-memory.py V_logic [ESTIMATE]"),
    "E_hbm_delivered_pJ": (3.95, "research/stage3/hot-side-memory_model_output.md [MODEL]"),
    "E_near_delivered_pJ": (0.37, "research/stage3/hot-side-memory_model_output.md [MODEL]"),
    "E_hbm_port_pJ": (3.5, "models/hot-side-memory.py E_hbm_pJ (HBM3E 3.44 pJ/b, arXiv 2602.18568) [REPORTED]"),
    "E_ddr5_host_pJ": (15.0, STUDY_LINK + ", section 8 'DDR5 host @15 pJ/b' [ESTIMATE]"),
    "imec_2T0C_ret_s_95C": (200.0, "imec 40 nm IGZO 2T0C, EDL 2025: >200 s at 95 C [REPORTED]"),
    "Ea_oxide_eV": (0.8, "dossiers/hot-side-memory.md Arrhenius extrapolation Ea = 0.8 eV [ESTIMATE]"),
    "ber64_85C": (3.6e-9, "models/raw-ber-contract.py ret_anchor_ber_64ms (RAIDR-era tail, 85 C derate) [ESTIMATE]"),
    "ber32_85C": (1.1e-10, "models/raw-ber-contract.py ret_anchor_ber_32ms [ESTIMATE]"),
    "rtn_eta_mV": (2.8, "dossiers/charge-river.md section 2.3: unscreened RTN mean amplitude eta = 2.8 mV [ESTIMATE]"),
    "ccd_k_ws": (1.5, "dossiers/charge-river.md section 2.3 worst-string factor [ESTIMATE]"),
    "ccd_transfers": (98, "dossiers/charge-river.md section 2.3 transfers per segment"),
    "ccd_survival": (0.65, "dossiers/charge-river.md: ~65% worst-string survival gives a 6.1-sigma eye [ESTIMATE]"),
}

# Bench reference values. These are REFERENCE choices so every guide shares one baseline. [ESTIMATE]
BENCH = {
    "Cs_F": 1e-9,          # 1 nF C0G/NP0 storage capacitor (low leakage, low dielectric absorption)
    "Cbl_F": 6.8e-9,       # 6.8 nF "bitline" capacitor: Cbl/Cs = 6.8, close to the 1-beta chip's 6.4
    "V": 3.3,              # USB / microcontroller logic rail
    "Cnode_E4_F": (10e-12, 100e-12, 1e-9),  # floating-node sizes for the femtoamp bench
    "adc_res_V": (1e-3, 100e-6),            # 1 mV: external ADC/DMM with its own reference; 100 uV: 16-bit
                                            # external ADC with care. Drift, not resolution, sets the floor.
    "leak_cases_A": (1e-9, 10e-12, 20e-15, 1e-15),
    "ada4530_ib_max_A": 20e-15,  # ADA4530-1 input bias, max, -40..85 C [DATASHEET]
    "ada4530_ib_typ_A": 1e-15,   # "<1 fA typical at 25 C" [DATASHEET]
    "dram64_cells": 2 ** 26,     # 64 Mbit SDR SDRAM (e.g., Alliance AS4C4M16SA) = 67,108,864 cells
    "dram64_price_usd": 3.95,    # DigiKey qty 1, AS4C4M16SA-6TCN, approx Nov 2026 [REPORTED via snippet];
                                 # Findchips $4.33, RS GBP 4.97 at qty 1 (reviewer search) -> "~$4-5"
    "dev_board_usd": (30, 65),   # STM32F429I-DISC1 (SDRAM already fitted): EUR 26.23 ex-VAT DigiKey IT .. $62.99
                                 # Waveshare, approx Nov 2026 [REPORTED via snippets]
    "ada4530_supply_V": (4.5, 16.0),  # ADA4530-1 supply range; will NOT run from 3.3 V [DATASHEET]
}


# --------------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------------
_PREFIX = [(1e12, "T"), (1e9, "G"), (1e6, "M"), (1e3, "k"), (1.0, ""), (1e-3, "m"), (1e-6, "u"),
           (1e-9, "n"), (1e-12, "p"), (1e-15, "f"), (1e-18, "a"), (1e-21, "z"), (1e-24, "y")]


def si(x, unit="", digits=3):
    """Format with an SI prefix: si(1.3e-14, 'A') -> '13.0 fA'."""
    if x == 0 or not math.isfinite(x):
        return f"{x} {unit}"
    ax = abs(x)
    for scale, p in _PREFIX:
        if ax >= scale * 0.9995:
            return f"{x / scale:.{digits}g} {p}{unit}"
    return f"{x:.{digits}e} {unit}"


def hr(n, title):
    print("\n" + "=" * 100)
    print(f"SECTION {n}. {title}")
    print("=" * 100)


def table(headers, rows):
    w = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    print("  ".join(str(h).ljust(w[i]) for i, h in enumerate(headers)))
    print("  ".join("-" * w[i] for i in range(len(headers))))
    for r in rows:
        print("  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))


def q_upper(z):
    """Upper-tail probability of a standard normal, Q(z) = P(Z > z)."""
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def z_upper(p):
    """Inverse of q_upper by bisection: the z with P(Z > z) = p (0 < p < 1)."""
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if q_upper(mid) > p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def kT_eV(T):
    return KB_EV * T


def arrhenius_factor(Ea_eV, T_from, T_to):
    """Rate multiplier when going from T_from to T_to (rate ~ exp(-Ea/kT))."""
    return math.exp(Ea_eV / KB_EV * (1.0 / T_from - 1.0 / T_to))


def doubling_interval_C(Ea_eV, T):
    """Temperature rise (K) that doubles an Arrhenius rate near T. Exact solution of AF = 2."""
    # 1/T - 1/(T+d) = ln2 * k / Ea  ->  d = T^2 x / (1 - T x), x = ln2 k / Ea
    x = math.log(2.0) * KB_EV / Ea_eV
    return T * T * x / (1.0 - T * x)


def nc_from_mass(m_rel, T):
    """Effective density of states, cm^-3: Nc = 2 (2 pi m* k T / h^2)^1.5."""
    m = m_rel * M0
    return 2.0 * (2.0 * math.pi * m * KB * T / HPL ** 2) ** 1.5 / 1e6


def si_gap(T):
    """Varshni fit for Si band gap (eV): 1.17 - 4.73e-4 T^2/(T+636) [UNVERIFIED textbook]."""
    return 1.17 - 4.73e-4 * T * T / (T + 636.0)


def ni_cm3(Eg, Nc300, Nv300, T):
    """Intrinsic carrier density ni = sqrt(Nc Nv) exp(-Eg / 2kT), Nc,Nv ~ T^1.5."""
    s = (T / 300.0) ** 1.5
    return math.sqrt(Nc300 * s * Nv300 * s) * math.exp(-Eg / (2.0 * kT_eV(T)))


def ktc_V(C, T):
    return math.sqrt(KB * T / C)


def poisson_cdf(k, lam):
    """P(X <= k) for X ~ Poisson(lam); vectorized sum in log space (k up to ~1e6)."""
    if k < 0:
        return 0.0
    i = np.arange(0, int(k) + 1, dtype=float)
    log_fact = np.concatenate(([0.0], np.cumsum(np.log(np.arange(1, int(k) + 1, dtype=float)))))
    logpmf = -lam + i * math.log(lam) - log_fact
    return float(min(1.0, np.exp(logpmf).sum()))


def quantile_ci_ranks(N, p, conf=0.95):
    """Distribution-free CI for the p-quantile from N samples: ranks (r, s) such that the true quantile
    lies between the r-th and s-th smallest values with probability >= conf. Uses the Poisson
    approximation to Binomial(N, p), excellent for p <= 1e-3. Returns (r, s, achieved coverage)."""
    lam = N * p
    a = (1.0 - conf) / 2.0
    # r = largest r with P(K < r) = P(K <= r-1) <= a
    r = 0
    while poisson_cdf(r, lam) <= a:
        r += 1
    # now P(K <= r) > a, so P(K <= r-1) <= a  -> rank r (1-based) is the lower bound
    # s = smallest s with P(K >= s) = 1 - P(K <= s-1) <= a
    s = max(r + 1, int(lam))
    while 1.0 - poisson_cdf(s - 1, lam) > a:
        s += 1
    cov = poisson_cdf(s - 1, lam) - (poisson_cdf(r - 1, lam) if r >= 1 else 0.0)
    return r, s, cov


def garwood(k, conf=0.95):
    """Exact Poisson CI for an observed count k (bisection)."""
    a = (1.0 - conf) / 2.0

    def solve(f, lo, hi):
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if f(mid):
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    lower = 0.0 if k == 0 else solve(lambda lam: 1.0 - poisson_cdf(k - 1, lam) < a, 0.0, k + 10 * math.sqrt(k) + 10)
    upper = solve(lambda lam: poisson_cdf(k, lam) > a, 0.0, k + 20 * math.sqrt(k + 1) + 20)
    return lower, upper


def binom_tail_ge(n, p, k):
    """P(X >= k) for X ~ Binomial(n, p), summed directly over the upper tail (no 1 - sum cancellation),
    so it stays accurate at tiny p (e.g. ~1e-25 at BER 1e-14). Terms beyond the window are negligible."""
    if k <= 0:
        return 1.0
    if k > n or p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    lp, lq = math.log(p), math.log1p(-p)
    top = min(n, max(k + 80, int(n * p + 12 * math.sqrt(n * p * (1 - p)) + 12)))
    c = math.lgamma(n + 1)
    return min(1.0, sum(math.exp(c - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * lp + (n - i) * lq)
                        for i in range(k, top + 1)))


# Retention tail model at 85 C (lognormal in ln t), from raw-ber-contract.py anchors
def retention_model_85C():
    z1 = z_upper(STUDY["ber64_85C"][0])
    z2 = z_upper(STUDY["ber32_85C"][0])
    sigma = (math.log(0.064) - math.log(0.032)) / (z2 - z1)
    mu = math.log(0.064) + sigma * z1
    return mu, sigma


def fail_fraction(t_s, mu, sigma, AF=1.0):
    """Fraction of cells (tested in their charged state) that fail when left t_s unrefreshed.
    AF = retention stretch factor relative to 85 C (AF > 1 when colder)."""
    return q_upper((mu - math.log(t_s / AF)) / sigma)


def time_for_fraction(frac, mu, sigma, AF=1.0):
    return AF * math.exp(mu - sigma * z_upper(frac))


# --------------------------------------------------------------------------------------------
# SECTION 0: constants
# --------------------------------------------------------------------------------------------
def s0():
    hr(0, "CONSTANTS AND SOURCES")
    table(["name", "value", "unit", "tag", "source"],
          [(k, f"{v[0]:.10g}", v[1], v[3], v[2]) for k, v in CONST.items()])
    print()
    table(["semiconductor", "Eg (eV)", "tag", "source"], [(k, v[0], v[4], v[3]) for k, v in SEMIS.items()])
    print(f"Oxide electron effective mass m*/m0 = {OXIDE_ME[0]}-{OXIDE_ME[1]} [REPORTED via snippets]; "
          f"oxide Nv bounded {OXIDE_NV_RANGE[0]:.0e}-{OXIDE_NV_RANGE[1]:.0e} cm^-3 [ESTIMATE]")
    print()
    table(["study number [STUDY]", "value", "source"], [(k, f"{v[0]:.4g}", v[1]) for k, v in STUDY.items()])
    print()
    table(["bench reference [ESTIMATE unless noted]", "value"], [(k, str(v)) for k, v in BENCH.items()])
    print(f"\nkT at 25 C = {kT_eV(T_ROOM)*1e3:.2f} meV; at 85 C = {kT_eV(T_85)*1e3:.2f} meV; at 125 C = {kT_eV(T_125)*1e3:.2f} meV")


# --------------------------------------------------------------------------------------------
# SECTION 1: what a bit needs
# --------------------------------------------------------------------------------------------
def s1():
    hr(1, "WHAT A BIT PHYSICALLY NEEDS")
    print("(a) Hold time vs barrier (single-particle bits such as a magnet): Delta = Eb/kT >= ln(f0 * t * N / P),")
    print("    P = allowed expected number of failures (0.5 here, i.e. ~40% chance of any failure).")
    rows = []
    for name, f0, t, N, P in (("one MRAM-type bit, 10 years, P = 0.5", 1e9, 10 * 3.156e7, 1, 0.5),
                              ("1 Gbit MRAM-type array, 10 years, 0.5 expected failures", 1e9, 10 * 3.156e7, 1e9, 0.5)):
        d = math.log(f0 * t * N / P)
        rows.append((name, f"{f0:.0e} Hz", f"{d:.1f}", f"{d*kT_eV(T_85):.2f} eV at 85 C"))
    table(["case", "attempt rate f0", "Delta = Eb/kT", "barrier"], rows)
    print("  -> the familiar 'Delta >= ~60' rule for 10-year magnetic bits [ESTIMATE; f0 = 1 GHz assumed].")
    print("\n(b) Charge bits: how many electrons is a bit?")
    rows = []
    for name, C, V in (("1-beta DRAM cell, signal charge C*VARY/2", CS_1B_FF * 1e-15, V_ARRAY / 2),
                       ("oxide gain-cell storage node, 600 mV window", 0.15e-15, 0.6),
                       ("bench 1 nF cell at 3.3 V", BENCH["Cs_F"], BENCH["V"])):
        rows.append((name, si(C, "F"), f"{V:.3g} V", f"{C*V/QE:,.0f}", si(QE / C, "V")))
    table(["storage", "C", "V", "electrons", "volts per electron"], rows)
    print("\n(c) Endurance needed: how many write/restore events does a cell see?")
    rows = [("refresh only, 64 ms, 7 years", 7 * 3.156e7 / 0.064),
            ("hot cache line written every 100 ns, 3 years", 3 * 3.156e7 / 100e-9),
            ("hot line written every 10 ns, 1 year", 3.156e7 / 10e-9)]
    table(["use", "events"], [(a, f"{b:.2e}") for a, b in rows])
    print("  -> 1e15+ writes is the bar a working-memory cell must clear [ESTIMATE]. Moving charge wears nothing;")
    print("     moving atoms (filaments, phase change) or tunnelling through oxide (flash) does.")


# --------------------------------------------------------------------------------------------
# SECTION 2: Q = C V
# --------------------------------------------------------------------------------------------
def s2():
    hr(2, "Q = C * V  (charge stored)")
    rows = []
    for scale, C, V in (("CHIP 1-beta cell, full VARY", CS_1B_FF * 1e-15, V_ARRAY),
                        ("CHIP 1-beta cell, signal half (VARY/2)", CS_1B_FF * 1e-15, V_ARRAY / 2),
                        ("CHIP oxide gain-cell node (0.15 fF, 0.6 V)", 0.15e-15, 0.6),
                        ("BENCH 1 nF cell at 3.3 V", BENCH["Cs_F"], BENCH["V"]),
                        ("BENCH 100 pF node at 3.3 V", 100e-12, BENCH["V"])):
        Q = C * V
        rows.append((scale, si(C, "F"), f"{V:.3g} V", si(Q, "C"), f"{Q/QE:.3g}"))
    table(["scale", "C", "V", "Q", "electrons"], rows)
    print(f"Bench/chip charge ratio (1 nF @3.3 V vs 1-beta cell @VARY): "
          f"{BENCH['Cs_F']*BENCH['V']/(CS_1B_FF*1e-15*V_ARRAY):.2e}x")


# --------------------------------------------------------------------------------------------
# SECTION 3: retention t = C dV / I, and its inverse I = C dV/dt
# --------------------------------------------------------------------------------------------
def droop_allowed_V():
    """Allowed droop of a stored '1' at end of retention for the 1-beta cell (as dram_cell_physics s3)."""
    vpre = V_ARRAY / 2
    v1min = vpre + DV_MIN_MV / 1e3 * (CS_1B_FF + CBL_FF) / CS_1B_FF
    return V_ARRAY - v1min


def s3():
    hr(3, "RETENTION  t = C * dV / I_leak   and the inverse  I = C * dV/dt  (the floating-node method)")
    droop = droop_allowed_V()
    print(f"CHIP: 1-beta cell Cs = {CS_1B_FF:.2f} fF, allowed droop {droop*1e3:.0f} mV "
          f"(keeps a {DV_MIN_MV:.0f} mV sense signal) [STUDY]")
    rows = []
    for t in (0.032, 0.064, 1.0, 10.0, 3600.0):
        rows.append((si(t, "s"), si(CS_1B_FF * 1e-15 * droop / t, "A")))
    table(["retention target", "max tail-cell leakage"], rows)
    print("\nCHIP: oxide gain-cell node 0.15 fF, allowed droop 100 mV [STUDY C_SN; droop ESTIMATE]")
    rows = []
    for t in (1.0, 3.6, 200.0, 3600.0):
        rows.append((si(t, "s"), si(0.15e-15 * 0.1 / t, "A")))
    table(["retention target", "max leakage"], rows)
    print("\nBENCH: 1 nF cell, 0.5 V allowed droop (3.3 V '1' read against a 1.65 V reference with margin)")
    rows = []
    for I in BENCH["leak_cases_A"]:
        t = BENCH["Cs_F"] * 0.5 / I
        rows.append((si(I, "A"), si(t, "s"), f"{t/3600:.3g} h"))
    table(["leakage", "retention", "hours"], rows)
    print("\nBENCH: smallest leakage you can resolve from droop, I_min = C * dV_res / t_obs [ESTIMATE]")
    rows = []
    for C in BENCH["Cnode_E4_F"]:
        for dv in BENCH["adc_res_V"]:
            for t_obs in (60.0, 3600.0, 86400.0):
                rows.append((si(C, "F"), si(dv, "V"), si(t_obs, "s"), si(C * dv / t_obs, "A")))
    table(["node C", "voltage resolution", "observe for", "I_min (ideal)"], rows)
    print(f"Real floor: the buffer's input bias current lands on the node. ADA4530-1: <= {si(BENCH['ada4530_ib_max_A'],'A')} max "
          f"(-40..85 C), ~{si(BENCH['ada4530_ib_typ_A'],'A')} typ at 25 C [DATASHEET]. Subtract it with a 'blank' run.")
    print("Worked example: 100 pF node drooping 1 mV per hour -> I = 100e-12 * 1e-3 / 3600 = "
          f"{si(100e-12*1e-3/3600,'A')}  (the arithmetic, NOT a home result)")
    ib, cn = BENCH["ada4530_ib_typ_A"], 100e-12
    print(f"  But the buffer's own ~{si(ib,'A')} typical bias moves that node {si(ib*3600/cn,'V')} per hour "
          f"({ib/(cn*1e-3/3600):.0f}x the example); at the {si(BENCH['ada4530_ib_max_A'],'A')} max it is "
          f"{si(BENCH['ada4530_ib_max_A']*3600/cn,'V')} per hour.")
    dbl = 40.0 / math.log2(250e-15 / 20e-15)
    print(f"  Datasheet maxima 20 fA (85 C) -> 250 fA (125 C) imply the bias doubles every ~{dbl:.0f} C, so +-1 C of room "
          f"drift moves it ~{(2**(1/dbl)-1)*100:.0f}% [ESTIMATE]. Blank subtraction to 27.8 aA would need it steady to "
          f"~{27.8e-18/ib*100:.0f}%.")
    print(f"  ADA4530-1 supply: {BENCH['ada4530_supply_V'][0]}-{BENCH['ada4530_supply_V'][1]:.0f} V [DATASHEET]: "
          "it will not run from the 3.3 V rail.")
    print("Realistic home floors [ESTIMATE]: solderless breadboard pA-nA; clean hand-wired node in air or on PTFE")
    print("  standoffs with the guard used ~10-100 fA; ADA4530-1 eval board in a shielded box ~1-20 fA; best case with")
    print("  blank subtraction and temperature held to +-0.5 C ~0.1-1 fA. Attoamps are out of reach at home.")
    print(f"  For scale: 10 fA on 100 pF droops {si(10e-15*3600/100e-12,'V')} per hour.")
    print("Capacitor insulation resistance (C0G datasheet minimums ~10-100 Gohm [UNVERIFIED typical spec]) allows up to "
          f"{si(3.3/100e9,'A')}-{si(3.3/10e9,'A')} at 3.3 V: measure YOUR part in the blank.")


# --------------------------------------------------------------------------------------------
# SECTION 4: charge sharing
# --------------------------------------------------------------------------------------------
def sense(cs, cbl, v):
    return (v / 2) * cs / (cs + cbl)


def s4():
    hr(4, "CHARGE-SHARING SENSE SIGNAL  dV = (V/2) * Cs / (Cs + Cbl)")
    rows = []
    for name, cs, cbl, v in (("CHIP 1-beta, 512 cells/BL", CS_1B_FF, CBL_FF, V_ARRAY),
                             ("CHIP 1-beta, 128 cells/BL", CS_1B_FF, CBL_128_FF, V_ARRAY),
                             ("CHIP 1 fF cell, 512 cells/BL", 1.0, CBL_FF, V_ARRAY),
                             ("BENCH 1 nF cell, 6.8 nF 'bitline'", 1.0, 6.8, BENCH["V"]),
                             ("BENCH 1 nF cell, 1 m RG-58 coax (~97 pF) + 10 pF probe", 1.0, 0.107, BENCH["V"]),
                             ("BENCH 1 nF cell, 100 nF 'long bitline'", 1.0, 100.0, BENCH["V"])):
        dv = sense(cs, cbl, v)
        rows.append((name, f"{cbl/cs:.2f}", si(dv, "V")))
    table(["case (C values in the same unit)", "Cbl/Cs", "signal"], rows)
    print("Same law, both scales: the signal depends only on the RATIO Cbl/Cs and on V.")
    print("A 1-beta chip and a 1 nF/6.8 nF bench cell have nearly the same ratio (6.4 vs 6.8), so the bench")
    print(f"signal is ~{sense(1, 6.8, BENCH['V'])/sense(CS_1B_FF, CBL_FF, V_ARRAY):.1f}x the chip's only because 3.3 V > 1.05 V.")
    print("\nBENCH pitfalls [ESTIMATE]:")
    r = 6.8
    print(f"  two unmeasured +-5% capacitors -> Cbl/Cs uncertain by +-{math.hypot(5, 5):.1f}%, signal by "
          f"+-{math.hypot(5, 5)*r/(1+r):.1f}%: measure both parts")
    for vt in (0.8, 2.1, 3.0):  # 2N7000 V_GS(th) range and a typical value [DATASHEET range, UNVERIFIED]
        vc = BENCH["V"] - vt
        sig = (vc - BENCH["V"] / 2) / (1 + r)
        print(f"  N-MOSFET gate driven from a 3.3 V pin, Vt {vt} V: cell stores {vc:.1f} V -> signal {sig*1e3:+.0f} mV "
              f"({'reads as 0!' if sig < 0 else 'weak 1'}) vs +{sense(1, r, BENCH['V'])*1e3:.0f} mV ideal")
    qinj = 20e-12 * 5.0
    print(f"  switch charge injection ~20 pF x 5 V = {si(qinj,'C')}; if 10-50% lands on 1 nF: "
          f"{si(0.1*qinj/1e-9,'V')}-{si(0.5*qinj/1e-9,'V')} (cancel with (V1 - V0)/2)")
    print(f"  an MCU pin leaking 1 nA empties 0.5 V from 1 nF in {si(1e-9*0.5/1e-9,'s')}")


# --------------------------------------------------------------------------------------------
# SECTION 5: energy and refresh power
# --------------------------------------------------------------------------------------------
def s5():
    hr(5, "ENERGY  E_supply = C*V^2 per charge-up (1/2 stored, 1/2 lost in the switch)  and REFRESH POWER")
    rows = []
    for name, C, V in (("CHIP 1-beta cell", CS_1B_FF * 1e-15, V_ARRAY),
                       ("CHIP 512-cell bitline", CBL_FF * 1e-15, V_ARRAY),
                       ("CHIP oxide gain-cell node", 0.15e-15, 0.6),
                       ("BENCH 1 nF cell", BENCH["Cs_F"], BENCH["V"]),
                       ("BENCH 6.8 nF bitline", BENCH["Cbl_F"], BENCH["V"])):
        rows.append((name, si(C * V * V, "J"), si(0.5 * C * V * V, "J")))
    table(["element", "C*V^2 from supply", "1/2 C V^2 stored"], rows)
    print(f"\nCHIP refresh: E per refreshed bit = {E_REFRESH_FJ:.0f} fJ (bitline + wordline x2 periphery) [STUDY]")
    for t in (0.064, 0.032):
        p = DIE_BITS * E_REFRESH_FJ * 1e-15 / t
        print(f"  P_refresh = bits x E / t_ref = {DIE_BITS:.2e} x {E_REFRESH_FJ:.0f} fJ / {t*1e3:.0f} ms = {si(p,'W')} per 16 Gb die")
    e_b = (BENCH["Cs_F"] + BENCH["Cbl_F"]) * BENCH["V"] ** 2
    print(f"BENCH refresh: 8 cells x (Cs+Cbl) V^2 = 8 x {si(e_b,'J')} every 10 s = {si(8*e_b/10,'W')}")
    print("  -> on the bench the microcontroller (~0.1 W) dwarfs the array; on a chip the array IS the cost.")
    print(f"Refresh energy saved if the interval grows k-fold: P scales as 1/k (e.g. 9x interval -> "
          f"{si(DIE_BITS*E_REFRESH_FJ*1e-15/0.032/9,'W')} per die at the 32 ms baseline).")


# --------------------------------------------------------------------------------------------
# SECTION 6: kT/C
# --------------------------------------------------------------------------------------------
def cmin_ktc(margin_V, z, T):
    return KB * T * (z / margin_V) ** 2


def s6():
    hr(6, "THERMAL (kT/C) NOISE  sigma_V = sqrt(kT/C)  and the minimum capacitance it implies")
    rows = []
    for name, C, T in (("CHIP 512-cell bitline, 85 C", CBL_FF * 1e-15, T_85),
                       ("CHIP 1-beta cell, 85 C", CS_1B_FF * 1e-15, T_85),
                       ("CHIP oxide gain-cell node, 105 C", 0.15e-15, T_105),
                       ("BENCH 10 pF probe node, 25 C", 10e-12, T_ROOM),
                       ("BENCH 1 nF cell, 25 C", 1e-9, T_ROOM)):
        rows.append((name, si(C, "F"), si(ktc_V(C, T), "V")))
    table(["node", "C", "sigma (rms)"], rows)
    print("\nMinimum C so that kT/C alone gives error probability P per read: C_min = kT (z/M)^2, M = half the gap")
    rows = []
    for M in (0.010, 0.050, 0.100):
        for P in (1e-15, 1e-4):
            z = z_upper(P)
            rows.append((si(M, "V"), f"{P:.0e}", f"{z:.2f}", si(cmin_ktc(M, z, T_85), "F")))
    table(["margin M", "error prob P", "z", "C_min at 85 C"], rows)
    print("-> ~0.1 fF is the thermodynamic floor for a 50 mV margin; today's 5 fF cell is 40x above it.")
    print("   Accepting P = 1e-4 behind ECC lowers the floor ~4.5x (the raw-ber idea seen through kT/C).")


# --------------------------------------------------------------------------------------------
# SECTION 7: Arrhenius
# --------------------------------------------------------------------------------------------
def s7():
    hr(7, "ARRHENIUS  I ~ exp(-Ea/kT): how fast leakage rises with temperature")
    eas = (("DRAM tail cells (patent data)", 0.35), ("Si generation ~Eg/2", 0.56),
           ("DRAM main cells (patent data)", 0.6), ("rule of thumb 'halves per 10 C', at 85 C", None),
           ("oxide 2T0C extrapolation", 0.8), ("Si diffusion ~Eg", 1.12))
    rows = []
    for name, ea in eas:
        if ea is None:
            ea = EA_10C_RULE
        rows.append((name, f"{ea:.2f}", f"{doubling_interval_C(ea, T_ROOM):.1f}", f"{doubling_interval_C(ea, T_85):.1f}",
                     f"{arrhenius_factor(ea, T_ROOM, T_85):.3g}x", f"{arrhenius_factor(ea, T_ROOM, 338.15):.3g}x"))
    table(["mechanism", "Ea eV", "doubles every (K) near 25 C", "near 85 C", "25->85 C", "25->65 C (bench)"], rows)
    print("\nCHIP: what a 64 ms worst cell at 85 C becomes at 25 C (retention stretches by the same factor):")
    rows = []
    for ea in (0.35, 0.6, round(EA_10C_RULE, 2)):
        rows.append((f"{ea}", si(0.064 * arrhenius_factor(ea, T_ROOM, T_85), "s")))
    table(["Ea eV", "worst-cell retention at 25 C (>=)"], rows)
    span = 1 / T_ROOM - 1 / 338.15
    print(f"\nBENCH: a 10 K error in the DUT's true temperature at the hot end of a 25->65 C fit shifts Ea by "
          f"{(1/338.15 - 1/348.15)/span:.0%}-{(1/328.15 - 1/338.15)/span:.0%} [ESTIMATE]: log the DUT's own temperature.")
    print("\nCHIP oxide: imec 2T0C >200 s at 95 C, extrapolated [STUDY Ea 0.8 eV; range 0.5-1.1]:")
    rows = []
    for Tc in (25, 85, 105, 125):
        T = Tc + 273.15
        vals = [200.0 / arrhenius_factor(ea, 368.15, T) for ea in (0.5, 0.8, 1.1)]
        rows.append((f"{Tc} C", si(vals[0], "s"), si(vals[1], "s"), si(vals[2], "s")))
    table(["temperature", "Ea 0.5", "Ea 0.8", "Ea 1.1"], rows)


# --------------------------------------------------------------------------------------------
# SECTION 8: band gap, intrinsic carriers, subthreshold, and why tails are lognormal
# --------------------------------------------------------------------------------------------
def s8():
    hr(8, "BAND GAP -> INTRINSIC CARRIERS  ni = sqrt(Nc*Nv) * exp(-Eg/2kT)  (the root of the BEST BET)")
    si_eg = SEMIS["Si"]
    rows = []
    ni_si = {}
    for T in (T_300, T_85, T_125):
        ni_si[T] = ni_cm3(si_gap(T), si_eg[1], si_eg[2], T)
        rows.append(("Si (Varshni Eg)", f"{T-273.15:.0f} C", f"{si_gap(T):.3f}", f"{ni_si[T]:.3g}", "1",
                     f"{1/ni_si[T]*1e12:.3g} um^3"))
    for name in ("a-IGZO (3.05 eV)", "IGZO (3.2 eV)", "ZnO (3.37 eV)", "wide oxide (3.5 eV)"):
        Eg = SEMIS[name][0]
        for T in (T_300, T_85, T_125):
            lo = ni_cm3(Eg, nc_from_mass(OXIDE_ME[0], 300.0), OXIDE_NV_RANGE[0], T)
            hi = ni_cm3(Eg, nc_from_mass(OXIDE_ME[1], 300.0), OXIDE_NV_RANGE[1], T)
            mid = math.sqrt(lo * hi)
            rows.append((name, f"{T-273.15:.0f} C", f"{Eg:.2f}", f"{lo:.2g} .. {hi:.2g}", f"{mid/ni_si[T]:.1e}",
                         f"{1/mid*1e-6:.3g} m^3"))
    table(["material", "T", "Eg eV", "ni cm^-3", "ni / ni(Si)", "volume holding ONE intrinsic carrier"], rows)
    print(f"Check: textbook ni(Si, 300 K) ~ 1.0e10 cm^-3 (9.65e9 in Altermatt 2003) [UNVERIFIED]; formula gives {ni_si[T_300]:.3g}.")
    print(f"Oxide Nc from m* = {OXIDE_ME[0]}-{OXIDE_ME[1]} m0: {nc_from_mass(OXIDE_ME[0],300):.2g}-"
          f"{nc_from_mass(OXIDE_ME[1],300):.2g} cm^-3 at 300 K [ESTIMATE].")
    print("\nIntrinsic (SRH generation) leakage floor of a small depleted volume: I = q * ni * Vol / tau_g [ESTIMATE]")
    vol = (40e-7) ** 2 * 10e-7  # 40 nm x 40 nm x 10 nm in cm^3
    rows = []
    for name, ni in (("Si 85 C", ni_si[T_85]),
                     ("IGZO 3.05 eV 85 C (mid)", math.sqrt(ni_cm3(3.05, nc_from_mass(0.2, 300), 1e19, T_85) *
                                                          ni_cm3(3.05, nc_from_mass(0.34, 300), 1e21, T_85)))):
        for tau in (1e-6, 1e-3):
            rows.append((name, si(tau, "s"), si(QE * ni * vol / tau, "A")))
    table(["material", "generation lifetime", "floor for a 40x40x10 nm volume"], rows)
    print("-> In silicon the floor sits near measurable levels and traps/GIDL lift it to fA in the tail.")
    print("   In a 3+ eV oxide the intrinsic floor is ~1e-30 A or lower: it is NOT the limit. Defects, hydrogen,")
    print("   the gate dielectric and the subthreshold tail set real leakage (measured: <1 aA Kioxia, <=200 zA SEL,")
    print("   135 yA/um at 85 C in JJAP 51, 021201) [REPORTED]. That is why the study's unknown is the defect TAIL.")
    print("\nSubthreshold floor: SS_min = ln(10) kT/q:")
    for T in (T_300, T_85, T_125):
        print(f"  {T-273.15:5.0f} C: {math.log(10)*kT_eV(T)*1e3:5.1f} mV/decade")
    print("\nOff-current at hold bias: I_off = I(Vt) * 10^(-(Vt - V_hold)/SS), with I(Vt) = 100 nA [ESTIMATE]")
    rows = []
    for dv in (0.6, 0.8, 1.0, 1.2):
        rows.append((f"{dv:.1f} V", *(si(100e-9 * 10 ** (-dv * 1e3 / ss), "A") for ss in (72, 100, 150))))
    table(["Vt - V_hold", "SS 72 mV/dec", "SS 100", "SS 150"], rows)
    print("-> a 0.2 V more negative hold buys ~2 decades at SS 100 (the study's -0.5 vs -0.7 V hold split).")
    print("\nWhy leakage tails are lognormal: Vt is ~Gaussian, leakage is exponential in Vt, so")
    print("  sigma_log10(I) = sigma_Vt / SS;   tail multiplier at quantile z = 10^(z * sigma_Vt / SS)")
    rows = []
    for svt in (0.03, 0.05, 0.08):
        for ss in (0.072, 0.100, 0.150):
            s_dec = svt / ss
            rows.append((f"{svt*1e3:.0f} mV", f"{ss*1e3:.0f}", f"{s_dec:.2f}", f"{10**(z_upper(1e-4)*s_dec):.3g}x",
                         f"{10**(z_upper(1/DIE_BITS)*s_dec):.3g}x"))
    table(["sigma_Vt", "SS mV/dec", "sigma (decades)", "1e-4 tail / median", "worst of 1.7e10 / median"], rows)


# --------------------------------------------------------------------------------------------
# SECTION 9: gain cell
# --------------------------------------------------------------------------------------------
def s9():
    hr(9, "GAIN CELL: read through a transistor instead of dumping charge on a bitline")
    C, W = 0.15e-15, 0.6
    print(f"CHIP oxide 2T0C node {si(C,'F')}: {C*W/QE:.0f} electrons across a {W*1e3:.0f} mV window, "
          f"{si(QE/C,'V')} per electron [STUDY C_SN]")
    print(f"  charge sharing onto even the study's short 64-cell read bitline ({RBL_HOT_FF:.1f} fF), precharged mid-window, "
          f"would give only {si(sense(C, RBL_HOT_FF*1e-15, W), 'V')}")
    print(f"  ({si(sense(C, RBL_HOT_FF*1e-15, 2*W), 'V')} even with the bitline precharged to one end of the window): "
          "too small. Hence: do not share charge, sense current.")
    for i_rd, t_rd in ((1e-6, 10e-9), (10e-6, 5e-9)):
        q_rd = i_rd * t_rd
        print(f"  read {si(i_rd,'A')} for {si(t_rd,'s')} moves {si(q_rd,'C')} = {q_rd/(C*W):.0f}x the stored charge, "
              "and the stored charge is untouched (non-destructive) [ESTIMATE]")
    print(f"  retention budget, 100 mV droop: 1 s needs <= {si(C*0.1/1,'A')}; the study's 1e-4-tail kill line "
          f"(>= 1 s at 105 C) is a <= {si(C*0.1,'A')} tail-leakage spec at 105 C [ESTIMATE]")
    Cb, Vb, ib, tb = 150e-12, 3.0, 1e-3, 1e-3
    print(f"BENCH gain cell: node {si(Cb,'F')} (100 pF C0G + ~50 pF gate and wiring), {Vb} V -> {si(Cb*Vb,'C')} stored;")
    print(f"  read {si(ib,'A')} for {si(tb,'s')} = {si(ib*tb,'C')} -> charge gain ~{ib*tb/(Cb*Vb):.0f}x [ESTIMATE]")
    print("  Note: 'charge gain' = I_read * t_read / Q_stored grows in proportion to the read time you choose, so it")
    print("  is not a property of the cell. Always quote it together with the read time.")


# --------------------------------------------------------------------------------------------
# SECTION 10: wire energy
# --------------------------------------------------------------------------------------------
def coax_c_per_m(d_inner_mm, d_outer_mm, er):
    return 2 * math.pi * EPS0 * er / math.log(d_outer_mm / d_inner_mm)


def twin_c_per_m(d_mm, spacing_mm, er=1.0):
    return math.pi * EPS0 * er / math.acosh(spacing_mm / d_mm)


def microstrip_c_per_m(z0, eeff):
    return math.sqrt(eeff) / (C_LIGHT * z0)


def s10():
    hr(10, "THE PRICE OF DISTANCE: E_bit = alpha * C_wire * V^2, with C_wire ~ 10-200 pF per metre at EVERY scale")
    c_coax = coax_c_per_m(0.81, 2.95, 2.25)
    c_twin = twin_c_per_m(0.64, 2.5, 1.0)
    c_ms = microstrip_c_per_m(50.0, 3.3)
    c_chip = STUDY["c_wire_pF_mm"][0] * 1e-12 * 1e3
    rows = [("on-chip wire (study value; 0.1-0.25 fF/um reported)", c_chip),
            ("50-ohm PCB microstrip, eps_eff 3.3", c_ms),
            ("RG-58-like coax (0.81/2.95 mm, PE er 2.25)", c_coax),
            ("two 22 AWG jumper wires 2.5 mm apart, in air", c_twin)]
    table(["wire", "pF per m", "fF per um"], [(n, f"{c*1e12:.0f}", f"{c*1e12/1e6*1e3:.3f}") for n, c in rows])
    print("Why: C per length = 2*pi*eps / ln(outer/inner). Only the RATIO of sizes enters, and only via a log,")
    print("so a nanometre wire and a millimetre cable carry about the same pF per metre. Energy per bit is set by")
    print("LENGTH x V^2. To save energy you must shorten the wire or lower the swing. That is HOT-SIDE MEMORY.")
    print("\nalpha: random data charges the wire on 1/4 of bits (0->1), so alpha = 0.25 per C*V^2.")
    print("The study's hot-side model uses alpha = 0.5 (conservative; ratios unaffected).")
    rows = []
    a = 0.25
    for name, C, V in (("hybrid bond + via stack (10 fF), 0.75 V", 10e-15, 0.75),
                       ("on-chip 1 mm, 0.75 V", c_chip * 1e-3, 0.75),
                       ("on-chip 8 mm (HBM PHY to compute core), 0.75 V", c_chip * 8e-3, 0.75),
                       ("PCB 10 cm + 2 x 2 pF pads (DDR-like), 1.1 V", c_ms * 0.1 + 4e-12, 1.1),
                       ("BENCH 10 cm jumper pair, 3.3 V", c_twin * 0.1, 3.3),
                       ("BENCH 1 m coax, 3.3 V", c_coax * 1.0, 3.3),
                       ("BENCH 10 m coax, 3.3 V", c_coax * 10.0, 3.3)):
        rows.append((name, si(C, "F"), si(a * C * V * V, "J")))
    table(["path", "C", "wire energy per bit (alpha 0.25)"], rows)
    print(f"\nStudy result [STUDY]: near-tier {STUDY['E_near_delivered_pJ'][0]} pJ/bit vs HBM "
          f"{STUDY['E_hbm_delivered_pJ'][0]} pJ/bit delivered = {STUDY['E_hbm_delivered_pJ'][0]/STUDY['E_near_delivered_pJ'][0]:.1f}x; "
          f"DDR5 host ~{STUDY['E_ddr5_host_pJ'][0]:.0f} pJ/bit. Wires plus their drivers, termination and pads make the gap.")
    print("\nBENCH prediction for E3: a square wave at f into wire C draws extra supply current dI = f * C * V")
    rows = []
    for name, C in (("1 m coax", c_coax), ("10 m coax", 10 * c_coax), ("10 cm jumper pair", 0.1 * c_twin)):
        for f in (100e3, 1e6):
            rows.append((name, si(f, "Hz"), si(f * C * 3.3, "A"), si(f * C * 3.3 * 3.3, "W")))
    table(["load", "f", "extra supply current at 3.3 V", "extra power"], rows)
    print("(add ~10-15 pF for the scope probe and pin; measure with and without the wire and subtract) [ESTIMATE]")
    print("\nValidity of dI = f*C*V: the wire must fully charge every half period, i.e. 5*R_source*C (or ~3-5 round trips")
    print("for long coax) must be well under 1/(2f). With a 100 ohm series resistor [ESTIMATE]:")
    rows = []
    for name, length, f in (("1 m coax", 1.0, 1e6), ("10 m coax", 10.0, 1e6), ("10 m coax", 10.0, 100e3)):
        C = c_coax * length
        rt = 2 * length / (0.66 * C_LIGHT)  # round trip, PE velocity factor ~0.66 [UNVERIFIED typical]
        settle = max(5 * 100.0 * C, 5 * rt)
        rows.append((name, si(f, "Hz"), si(5 * 100.0 * C, "s"), si(rt, "s"), si(1 / (2 * f), "s"),
                     "OK" if settle < 0.2 / (2 * f) else ("marginal" if settle < 1 / (2 * f) else "too fast")))
    table(["load", "f", "5*R*C (R = 100 ohm)", "round trip", "half period", "verdict"], rows)
    print("-> Use 1 MHz for 1 m but 100 kHz for 10 m.")
    print(f"Peak drive current ~3.3 V / (100 + 50 + ~20 ohm) = {si(3.3/170,'A')}: use a 74AC04-type buffer (24 mA), not")
    print("an MCU pin (RP2040 drive settings are 2-12 mA). Measure only the buffer chip's supply current: a meter in")
    print(f"the mA range, or a 10 ohm shunt ({si(1e6*c_coax*3.3*10,'V')} at 1 m, 1 MHz), with a 10 uF + 100 nF bypass on the chip")
    print("side of the meter. Leave the far end OPEN: a 50 ohm terminator draws ~33 mA and swamps the effect.")
    print("Measure first with no cable and subtract that baseline. A typical USB power meter (~1 mA resolution) cannot see this.")


# --------------------------------------------------------------------------------------------
# SECTION 11: charge transfer
# --------------------------------------------------------------------------------------------
def s11():
    hr(11, "CHARGE TRANSFER (CCD / bucket brigade): an ISOLATED packet's main peak keeps CTE^N")
    print("Fraction of an isolated packet still in its own bucket after N transfers (the rest trails behind it):")
    ctes = (0.98, 0.99, 0.997, 0.999, 0.9999, 0.99999)
    ns = (32, 98, 568, 1024)
    table(["CTE"] + [f"N={n}" for n in ns], [(f"{c}", *(f"{c**n:.3g}" for n in ns)) for c in ctes])
    k = STUDY["ccd_k_ws"][0]
    n = STUDY["ccd_transfers"][0]
    h = STUDY["ccd_survival"][0]
    floor = 1 - (1 - h ** (1 / n)) / k
    print(f"\nCHIP: study floor for {n}-transfer segments, worst-string factor {k}, {h:.0%} survival -> CTE >= {floor:.4f} [STUDY]")
    print(f"imec 'CTE > 98%' ambiguity: per transfer -> {0.98**98:.1%} left after 98 transfers (fails);")
    print(f"  end-to-end over 142 bits x 4 phases = 568 transfers -> per-transfer {0.98**(1/568):.6f} (passes easily)")
    print("\nBENCH (E5): charge left behind is NOT lost; it joins the next packet. So for a continuous signal the")
    print("inefficiency eps = 1 - CTE does not lower the gain at low frequency. It smears the signal and cuts treble:")
    print("  |H(f)| = exp[-N eps (1 - cos(2 pi f / f_s))],  f_s = clock (sample) rate [UNVERIFIED textbook; Sequin &")
    print("  Tompsett 1975]. Exact DC gain 1. A BBD's low-frequency gain is set by its input/output followers and bias,")
    print("  not by CTE. Do NOT infer CTE from low-frequency insertion loss.")
    print(f"  Example: 1 kHz tone, f_s = 100 kHz, CTE 0.9999, N = 1024 loses only "
          f"{8.686*1024*1e-4*(1-math.cos(2*math.pi*0.01)):.4f} dB.")
    print("\nMethod 1 (best): isolated pulse. One clock-wide pulse, synchronised to the clock, with empty samples")
    print("around it. First trailing sample / main sample = N * eps (exact for the simple transfer model).")
    rows = []
    for cte in (0.999, 0.9999, 0.99999):
        rows.append((f"{cte}", *(f"{N*(1-cte):.3g}" for N in (512, 1024, 4096))))
    table(["CTE", "pulse trailing/main, N=512", "N=1024", "N=4096"], rows)
    print("  -> Over 1,024 transfers a 10% trailing sample means CTE ~0.9999; a 1% trailing sample means ~0.99999.")
    print("  The output stage adds its own smear: E5 separates it by comparing two chain lengths (slope = eps).")
    sinc4 = -20 * math.log10(math.sin(math.pi / 4) / (math.pi / 4))
    print(f"\nMethod 2: tone at f_s/4 vs a slow tone (f <= f_s/100). The sample-and-hold sinc alone costs "
          f"-20 log10(sin(pi/4)/(pi/4)) = {sinc4:.2f} dB at f_s/4;")
    print("  divide it out, and divide out your output filter (measure the filter alone). The remaining extra loss")
    print("  L dB = 8.686 * N * eps (since 1 - cos(pi/2) = 1), so eps = L / (8.686 N).")
    rows = []
    for L in (0.5, 0.89, 3.0, 8.9):
        rows.append((f"{L} dB", *(f"{1 - L/(20*math.log10(math.e)*N):.6f}" for N in (512, 1024, 4096))))
    table(["extra loss at f_s/4 after sinc and filter correction", "CTE, N=512", "N=1024", "N=4096"], rows)
    print("  Not at f_s/2: a tone exactly at half the clock rate is sampled with a phase-dependent amplitude, and the")
    print(f"  sinc there is {-20*math.log10(math.sin(math.pi/2)/(math.pi/2)):.2f} dB, so f_s/4 is the cleaner point.")
    print(f"Inverse (isolated packet): its main peak keeps CTE^N: CTE 0.9999 over 1024 transfers keeps "
          f"{0.9999**1024:.1%} in the main sample; CTE 0.999 keeps {0.999**1024:.1%}.")


# --------------------------------------------------------------------------------------------
# SECTION 12: Landauer
# --------------------------------------------------------------------------------------------
def s12():
    hr(12, "THE PHYSICAL FLOOR: Landauer kT*ln2 per erased bit")
    for T in (T_300, T_85):
        print(f"kT ln2 at {T-273.15:.0f} C = {si(KB*T*math.log(2),'J')} = {kT_eV(T)*math.log(2)*1e3:.1f} meV")
    L = KB * T_300 * math.log(2)
    rows = []
    for name, e in (("1-beta cell stored energy 1/2 C V^2", 0.5 * CS_1B_FF * 1e-15 * V_ARRAY ** 2),
                    ("DRAM refresh per bit [STUDY]", E_REFRESH_FJ * 1e-15),
                    ("oxide gain-cell node 1/2 C V^2", 0.5 * 0.15e-15 * 0.6 ** 2),
                    ("HOT-SIDE near tier delivered [STUDY]", STUDY["E_near_delivered_pJ"][0] * 1e-12),
                    ("HBM delivered [STUDY]", STUDY["E_hbm_delivered_pJ"][0] * 1e-12),
                    ("DDR5 host [STUDY]", STUDY["E_ddr5_host_pJ"][0] * 1e-12),
                    ("BENCH 1 nF cell 1/2 C V^2", 0.5 * BENCH["Cs_F"] * BENCH["V"] ** 2)):
        rows.append((name, si(e, "J"), f"{e/L:.2e}"))
    table(["operation", "energy", "x Landauer (300 K)"], rows)
    print("-> 4-9 orders of magnitude of headroom. Physics is not the wall; wires, voltage and periphery are.")
    print("   The headroom shows a ~10x gain from geometry breaks no physical law; it does not show the gain is easy.")


# --------------------------------------------------------------------------------------------
# SECTION 13: RTN
# --------------------------------------------------------------------------------------------
def s13():
    hr(13, "RANDOM TELEGRAPH NOISE: one trapped electron shifts Vt by ~ q / (Cox * W * L)")
    rows = []
    for name, W, L, eot in (("oxide cell read FET 40x40 nm, EOT 3 nm", 40e-9, 40e-9, 3e-9),
                            ("oxide FET 100x100 nm, EOT 5 nm", 100e-9, 100e-9, 5e-9),
                            ("Si DRAM periphery 30x30 nm, EOT 1 nm", 30e-9, 30e-9, 1e-9),
                            ("BENCH discrete MOSFET ~1 mm^2 gate, 50 nm oxide", 1e-3, 1e-3, 50e-9)):
        cox = 3.9 * EPS0 / eot
        rows.append((name, si(cox * W * L, "F"), si(QE / (cox * W * L), "V")))
    table(["device", "gate C", "dVt per trapped electron (charge-sheet)"], rows)
    print("Percolation through a few weak spots makes real steps several times larger; amplitudes follow an")
    print("exponential distribution: P(A > a) = Nt * exp(-a/eta)  ->  the p-quantile a_p = eta * ln(Nt / p)")
    eta = STUDY["rtn_eta_mV"][0]
    rows = []
    for e in (eta, 5.0, 10.0, 15.0):
        rows.append((f"{e} mV", *(f"{e*math.log(nt/1e-4):.0f} mV" for nt in (0.3, 1.0, 3.0))))
    table(["eta (mean step)", "1e-4 quantile, Nt=0.3", "Nt=1", "Nt=3"], rows)
    need = 100.0 / math.log(1 / 1e-4)
    print(f"Study kill line: RTN 1e-4 quantile <= 100 mV -> fails if eta > ~{need:.1f} mV (Nt = 1) [ESTIMATE]")
    print("The median device sees ~eta; the 1e-4 device sees ~9x eta. Refresh and margins are set by the tail.")


# --------------------------------------------------------------------------------------------
# SECTION 14: statistics of tails
# --------------------------------------------------------------------------------------------
def s14():
    hr(14, "STATISTICS OF TAILS: how many samples a 1e-4 quantile needs, and why a DRAM chip is the cheapest tool")
    print("Count of samples below the true p-quantile: K ~ Binomial(N, p) ~ Poisson(N p). Relative error ~ 1/sqrt(Np).")
    rows = []
    for p in (1e-4, 2e-5):
        for N in (1e3, 1e4, 1e5, 1e6, float(BENCH["dram64_cells"])):
            lam = N * p
            if lam < 1:
                rows.append((f"{p:.0e}", f"{N:.2e}", f"{lam:.2f}", "-", "-", "cannot estimate; at best an upper bound"))
                continue
            r, s, cov = quantile_ci_ranks(N, p)
            sd = 0.5  # decades, lognormal leakage example
            lvl_hi = s / N
            f_lo = 10 ** (sd * (z_upper(lvl_hi) - z_upper(p)))
            if r == 0:  # no lower order statistic qualifies: one-sided interval only
                rows.append((f"{p:.0e}", f"{N:.2e}", f"{lam:.1f}", f"none..{s}", f"0..{lvl_hi:.2g}",
                             f"x{f_lo:.2f} .. unbounded"))
                continue
            lvl_lo = r / N
            f_hi = 10 ** (sd * (z_upper(lvl_lo) - z_upper(p)))
            rows.append((f"{p:.0e}", f"{N:.2e}", f"{lam:.1f}", f"{r}..{s}", f"{lvl_lo:.2g}..{lvl_hi:.2g}",
                         f"x{f_lo:.2f} .. x{f_hi:.2f}"))
    table(["p", "N samples", "expected tail count Np", "95% CI ranks", "true level lies in",
           "value factor (lognormal, 0.5 dec)"], rows)
    print("\nRule of three: to show the p-quantile is above a pass line with 95% confidence and ZERO failures,")
    for p in (1e-4, 2e-5, 1e-6):
        print(f"  p = {p:.0e}: N >= -ln(0.05)/p = {-math.log(0.05)/p:,.0f}")
    print("For a usable estimate (not just a bound), aim for Np >= 10-30 -> N = 1e5-3e5 at 1e-4, 5e5-1.5e6 at 2e-5.")
    n = BENCH["dram64_cells"]
    print(f"\nA 64 Mbit DRAM chip = {n:,} cells for ~$4-5 (DigiKey ${BENCH['dram64_price_usd']:.2f} qty 1) -> "
          f"${BENCH['dram64_price_usd']/n:.1e} per cell [REPORTED price]")
    print(f"  With the board that drives it (e.g. STM32F429I-DISC1, SDRAM already fitted): ~${BENCH['dev_board_usd'][0]}-"
          f"{BENCH['dev_board_usd'][1]} [REPORTED price]")
    for p in (1e-4, 1e-5, 1e-6, 1e-7):
        lo, hi = garwood(n * p)
        print(f"  p = {p:.0e}: {n*p:,.0f} tail cells per pass; 95% Poisson range on the count {lo:,.0f}-{hi:,.0f}")
    print("Probe-station comparison: 1e5 single transistors at ~10 s each = "
          f"{1e5*10/86400:.1f} days of stepping [ESTIMATE]; one DRAM chip pass reads 6.7e7 cells in seconds.")
    for rate in (1e6, 20e6):
        print(f"  reading 8 MB at {si(rate,'B/s')}: {8*2**20/rate:.2f} s per pass")
    print("CAUTION (timing trap): a 1 MB/s pass (8.4 s) is longer than the 0.5-5 s waits and the expected first failure.")
    print("  Every access to a row also refreshes it, so rows read later have waited longer. Either write and read rows")
    print("  in the same order at the same speed (each row then waits the same start-to-start time, at least one pass),")
    print("  or restart every row at once with a burst of 4,096 AUTO REFRESH commands (< 1 ms) and log each row's read")
    print("  time, or read only a slice of rows per trial, or relax the controller's own refresh timer (E6 method A).")
    print("  Use a fast interface (>= 20 MB/s: 0.42 s per pass) and fit with per-row waits (fit_retention_from_counts")
    print("  t_offset=...). Close every row within the datasheet tRAS(max), ~100-120 us for SDR SDRAM [UNVERIFIED for")
    print("  your part]: bit-banging a 512-byte row at 1 MB/s keeps it open ~0.5 ms, which is too long.")
    # Predicted retention failures for the home E6 experiment
    mu, sg = retention_model_85C()
    print(f"\nPRIOR for E6 (order of magnitude only): lognormal retention tail fitted to the study's 85 C anchors "
          f"(BER 3.6e-9 @64 ms, 1.1e-10 @32 ms): sigma_ln = {sg:.2f} [STUDY/ESTIMATE].")
    print("Applied to a 64 Mbit chip, every cell tested once in its charged state (all-0s pass + all-1s pass):")
    rows = []
    for Tc in (25, 45):
        for ea in (0.35, 0.6):
            AF = arrhenius_factor(ea, Tc + 273.15, T_85)
            t1 = time_for_fraction(1.0 / n, mu, sg, AF)
            row = [f"{Tc} C", f"{ea}", si(t1, "s")]
            for t in (1.0, 10.0, 60.0):
                row.append(f"{n*fail_fraction(t, mu, sg, AF):.3g}")
            rows.append(tuple(row))
    table(["chip T", "Ea eV", "first failure (expected count 1)", "fails after 1 s", "10 s", "60 s"], rows)
    print("Treat this as a prior to be overturned: the anchors come from server DIMMs, not your chip.")
    # raw-ber at home: interval extension with ECC
    print("\nRAW-BER AT HOME: how much longer can the chip go unrefreshed if a code fixes the weak bits?")
    print("(iid errors assumed; expected uncorrectable codewords per full-chip pass <= 0.01)")
    rows = []
    max_ber = {}
    codes = (("no code", 1, 0, 1), ("SECDED Hamming(72,64)", 72, 1, 64), ("BCH t=8 per 512 b (study)", 592, 8, 512))
    for Tc, ea in ((25, 0.35), (25, 0.6)):
        AF = arrhenius_factor(ea, Tc + 273.15, T_85)
        base = None
        for name, nbits, t_corr, data in codes:
            words = n / nbits  # physical cells per codeword in a home analysis (check bits use cells too)
            # find largest BER with words * P(>t errors) <= 0.01, by bisection in log space
            lo, hi = -14.0, -1.0
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                ber = 10 ** mid
                pu = binom_tail_ge(nbits, ber, t_corr + 1)
                if words * pu <= 0.01:
                    lo = mid
                else:
                    hi = mid
            ber = 10 ** lo
            max_ber[name] = ber
            t = time_for_fraction(ber, mu, sg, AF)
            base = base or t
            rows.append((f"{Tc} C / Ea {ea}", name, f"{ber:.2e}", si(t, "s"), f"{t/base:.1f}x"))
    table(["condition", "code", "max raw BER", "max unrefreshed time", "vs no code"], rows)
    # sensitivity: the stretch depends only on sigma_ln
    zs = [z_upper(max_ber[c[0]]) for c in codes]
    dz = [zs[0] - z for z in zs]
    print(f"\nThe stretch = exp(sigma_ln * dz), with dz = {dz[1]:.2f} (SECDED) and {dz[2]:.2f} (BCH-8): it depends ONLY on")
    print("the spread sigma_ln of your chip's retention distribution, not on temperature or Ea. Sensitivity [ESTIMATE]:")
    srows = []
    for sl in (0.5, 1.0, sg, 2.0):
        srows.append((f"{sl:.2f}" + (" (prior)" if sl == sg else ""), "1.0x",
                      f"{math.exp(sl*dz[1]):.1f}x", f"{math.exp(sl*dz[2]):.0f}x"))
    table(["sigma_ln", "no code", "SECDED(72,64)", "BCH t=8 / 512 b"], srows)
    print("-> Measuring sigma_ln is E6's real result; the prior's 8x / 57x are not predictions.")
    print("-> The FASTEST PROOF's mechanism at home: a code turns the 1-in-67-million weakest cell into a")
    print("   non-event, and the interval is set by a much higher quantile of the same distribution.")


# --------------------------------------------------------------------------------------------
# SECTION 15: summary
# --------------------------------------------------------------------------------------------
def s15():
    hr(15, "SUMMARY: SAME LAW, TWO SCALES")
    droop = droop_allowed_V()
    c_coax = coax_c_per_m(0.81, 2.95, 2.25)
    rows = [
        ("Q = C V", f"{CS_1B_FF*1e-15*V_ARRAY/2/QE:,.0f} e- signal (1-beta)", f"{BENCH['Cs_F']*BENCH['V']/QE:.2e} e- (1 nF, 3.3 V)", "E1"),
        ("t = C dV / I", f"64 ms needs <= {si(CS_1B_FF*1e-15*droop/0.064,'A')}", f"1 nF, 0.5 V, 10 pA -> {si(1e-9*0.5/10e-12,'s')}", "E1, E4"),
        ("I = C dV/dt", "how aA oxide leakage is measured",
         f"100 pF, 1 mV/h -> {si(100e-12*1e-3/3600,'A')} (arithmetic); home floor ~10 fA, 0.1-1 fA at best", "E4, E7, E8"),
        ("dV = (V/2) Cs/(Cs+Cbl)", f"{si(sense(CS_1B_FF, CBL_FF, V_ARRAY),'V')}", f"{si(sense(1, 6.8, 3.3),'V')} (1 nF / 6.8 nF)", "E1"),
        ("E = C V^2", f"bitline {si(CBL_FF*1e-15*V_ARRAY**2,'J')}", f"6.8 nF: {si(6.8e-9*3.3**2,'J')}", "E1, E3"),
        ("P_ref = N E / t", f"{si(DIE_BITS*E_REFRESH_FJ*1e-15/0.064,'W')} per die at 64 ms", f"{si(8*7.8e-9*3.3**2/10,'W')} for 8 cells at 10 s", "E1, E6"),
        ("sqrt(kT/C)", f"{si(ktc_V(CBL_FF*1e-15,T_85),'V')} on a bitline", f"{si(ktc_V(1e-9,T_ROOM),'V')} on 1 nF", "(theory)"),
        ("Arrhenius", f"x2 per ~10-23 C near 85 C (Ea {EA_10C_RULE:.2f}-0.35 eV)", f"25->65 C: x{arrhenius_factor(0.56,T_ROOM,338.15):.0f} (Ea 0.56)", "E4, E6"),
        ("ni ~ exp(-Eg/2kT)", "IGZO ni = 1e-14..1e-18 x Si (27-85 C)", "home ZnO TFT will leak far above its ni floor", "E7, E8"),
        ("E_wire = a C V^2", "0.37 vs 3.95 pJ/bit [STUDY]", f"1 m coax @1 MHz: +{si(1e6*c_coax*3.3,'A')}", "E3"),
        ("CTE^N (isolated packet)", "needs CTE >= 0.997 over 98 transfers",
         "pulse: 10% trailing over 1024 -> CTE 0.9999 (or 0.89 dB extra at f_s/4)", "E5"),
        ("Landauer kT ln2", f"refresh {E_REFRESH_FJ*1e-15/(KB*T_300*math.log(2)):.1e}x above", "bench cell ~1e12x above", "(theory)"),
        ("RTN ~ q/(Cox W L)", f"{si(QE/(3.9*EPS0/3e-9*1.6e-15),'V')} per electron (40 nm)", "unmeasurable on a power MOSFET", "E4 (popcorn noise), E8"),
        ("tail statistics", "1e-4 quantile needs N >= ~1e5", "64 Mbit chip = 6.7e7 cells: ~$4 chip, ~$30-65 on a board",
         "E4, E6"),
    ]
    table(["law", "chip scale", "bench scale", "home experiment"], rows)


SECTIONS = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]


# --------------------------------------------------------------------------------------------
# SELFTEST
# --------------------------------------------------------------------------------------------
_SQRT2 = math.sqrt(2.0)
_LN_SQRT_2PI = 0.5 * math.log(2.0 * math.pi)


def _log_erfc_pos(x):
    """ln erfc(x) for x >= 0, vectorized. Numerical Recipes 'erfcc' Chebyshev fit, fractional error < 1.2e-7
    everywhere [UNVERIFIED textbook], written in log form so deep tails do not underflow."""
    t = 1.0 / (1.0 + 0.5 * x)
    poly = (-1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (
        0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))))
    return np.log(t) - x * x + poly


def log_norm_cdf(eta):
    """ln Phi(eta) for a numpy array, accurate in both tails (Phi = 0.5 erfc(-eta/sqrt2))."""
    eta = np.asarray(eta, float)
    x = -eta / _SQRT2
    out = np.empty_like(eta)
    pos = x >= 0
    out[pos] = math.log(0.5) + _log_erfc_pos(x[pos])
    out[~pos] = np.log1p(-0.5 * np.exp(_log_erfc_pos(-x[~pos])))  # Phi = 1 - 0.5 erfc(|x|)
    return out


def fit_retention_from_counts(times, fails, n_cells, t_offset=None, return_se=False):
    """Analysis pipeline for E6: fit a lognormal retention tail F(t) = Phi((ln t - mu)/sigma) to fail counts.

    Each element is one 'bin': a group of cells that all waited the same time.
      times    : nominal wait per bin (s)
      fails    : failing cells per bin
      n_cells  : cells per bin (scalar or array)
      t_offset : optional extra wait per bin (s), e.g. how long after the nominal wait each row was read.
                 The fit uses the TRUE wait times + t_offset. Pass per-row bins to remove the timing trap.
    Binomial maximum likelihood (probit link), solved by Fisher scoring with step halving. Bins with zero
    failures count too. A 3-failure bin no longer weighs as much as a 144,000-failure bin.
    Returns (mu, sigma) in ln-seconds, or (mu, sigma, se_sigma) with return_se=True."""
    t = np.asarray(times, float).ravel()
    k = np.asarray(fails, float).ravel()
    n = np.broadcast_to(np.asarray(n_cells, float), t.shape).astype(float)
    if t_offset is not None:
        t = t + np.broadcast_to(np.asarray(t_offset, float), t.shape)
    if np.any(t <= 0) or np.any(k < 0) or np.any(k > n):
        raise ValueError("need positive wait times and 0 <= fails <= n_cells")
    x = np.log(t)
    # start: unweighted probit least squares on ~12 pooled groups (sorted by wait) with >= 3 failures
    order = np.argsort(x)
    groups = np.array_split(order, min(12, len(order)))
    gx, gz = [], []
    for g in groups:
        kk, nn = k[g].sum(), n[g].sum()
        if 3 <= kk <= nn - 3:
            gx.append(np.average(x[g], weights=n[g]))
            gz.append(-z_upper(kk / nn))
    if len(gx) < 2:
        raise ValueError("need at least two (pooled) wait times with >= 3 failures")
    b, a = np.polyfit(gx, gz, 1)  # eta = a + b ln t, b = 1/sigma
    if b <= 0:
        raise ValueError("fail fraction does not rise with wait time; check the data")

    def loglik(a_, b_):
        eta = a_ + b_ * x
        return float(np.sum(k * log_norm_cdf(eta) + (n - k) * log_norm_cdf(-eta)))

    ll = loglik(a, b)
    info = None
    for _ in range(100):
        eta = a + b * x
        lF, lS = log_norm_cdf(eta), log_norm_cdf(-eta)
        lphi = -0.5 * eta * eta - _LN_SQRT_2PI
        r = np.exp(lphi - lF - lS)                    # phi / (F (1 - F)), overflow-safe
        F = np.exp(lF)
        u = (k - n * F) * r                           # d loglik / d eta
        w = n * np.exp(lphi) * r                      # Fisher information per unit eta
        U = np.array([u.sum(), (u * x).sum()])
        info = np.array([[w.sum(), (w * x).sum()], [(w * x).sum(), (w * x * x).sum()]])
        step = np.linalg.solve(info, U)
        lam = 1.0
        while lam > 1e-6:
            a_new, b_new = a + lam * step[0], b + lam * step[1]
            if b_new > 0:
                ll_new = loglik(a_new, b_new)
                if ll_new >= ll - 1e-9:
                    break
            lam *= 0.5
        a, b, ll = a_new, b_new, ll_new
        if abs(lam * step[1]) < 1e-10 * abs(b) and abs(lam * step[0]) < 1e-10 * (1 + abs(a)):
            break
    sigma = 1.0 / b
    mu = -a * sigma
    if not return_se:
        return mu, sigma
    cov = np.linalg.inv(info)
    return mu, sigma, math.sqrt(cov[1, 1]) / b ** 2  # se(sigma) = se(b) / b^2


def per_row_bins(t_nominal, n_rows, pass_time_s, cells_per_row):
    """Bins for a 'refresh-burst then read sequentially' run: row i is read t_nominal + i*pass_time/n_rows after
    the burst. Returns (times, t_offset, n_cells) arrays for fit_retention_from_counts."""
    off = np.arange(n_rows) * (pass_time_s / n_rows)
    return np.full(n_rows, float(t_nominal)), off, np.full(n_rows, float(cells_per_row))


def _norm_cdf_np(eta):
    return np.exp(log_norm_cdf(eta))


def selftest():
    print("SELFTEST: formulas vs known values, then synthetic-data runs of the statistics and fitting pipelines")
    checks = []

    def check(name, value, lo, hi):
        ok = lo <= value <= hi
        checks.append(ok)
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value:.6g} (expected {lo:.6g} .. {hi:.6g})")

    check("1-beta signal electrons (study prints 17,768)", CS_1B_FF * 1e-15 * V_ARRAY / 2 / QE, 17500, 18000)
    check("bitline kT/C at 85 C, mV (study prints 0.38)", ktc_V(CBL_FF * 1e-15, T_85) * 1e3, 0.37, 0.39)
    check("fresh sense signal, mV (study prints 70.9)", sense(CS_1B_FF, CBL_FF, V_ARRAY) * 1e3, 70.5, 71.3)
    check("64 ms tail leakage, fA (study prints 13.1)", CS_1B_FF * 1e-15 * droop_allowed_V() / 0.064 * 1e15, 13.0, 13.25)
    check("Landauer at 300 K, zJ", KB * 300 * math.log(2) * 1e21, 2.86, 2.88)
    check("Si ni at 300 K / 1e10", ni_cm3(si_gap(300.0), 2.86e19, 2.66e19, 300.0) / 1e10, 0.5, 2.0)
    check("Nc for m*=1 at 300 K / 2.5e19", nc_from_mass(1.0, 300.0) / 2.5e19, 0.98, 1.02)
    check("coax C, pF/m (datasheets ~100)", coax_c_per_m(0.81, 2.95, 2.25) * 1e12, 90, 105)
    check("imec 200 s @95 C -> 105 C, s (dossier says 103)", 200.0 / arrhenius_factor(0.8, 368.15, 378.15), 100, 106)
    check("CCD CTE floor (dossier says 0.997)", 1 - (1 - 0.65 ** (1 / 98)) / 1.5, 0.9965, 0.9975)
    check("SS floor at 300 K, mV/dec", math.log(10) * kT_eV(300.0) * 1e3, 59.4, 59.8)
    check("z_upper(1e-4)", z_upper(1e-4), 3.718, 3.721)
    check("doubling interval for the '10 C rule' Ea at 85 C, K", doubling_interval_C(EA_10C_RULE, T_85), 9.99, 10.01)
    lo, hi = garwood(10)
    check("Garwood lower for k=10 (tables: 4.795)", lo, 4.78, 4.81)
    check("Garwood upper for k=10 (tables: 18.39)", hi, 18.37, 18.41)

    # Monte Carlo coverage of the order-statistic CI on SYNTHETIC lognormal retention data
    rng = np.random.default_rng(20261103)
    N, p, trials = 100_000, 1e-4, 300
    r, s, cov_theory = quantile_ci_ranks(N, p)
    mu, sig = 0.0, 1.2
    true_q = math.exp(mu - sig * z_upper(p))
    hits = 0
    for _ in range(trials):
        x = rng.lognormal(mu, sig, N)
        part = np.partition(x, [r - 1, s - 1])
        if part[r - 1] <= true_q <= part[s - 1]:
            hits += 1
    print(f"  Monte Carlo: N={N:,}, p={p:g}, ranks {r}..{s}, theory coverage {cov_theory:.3f}")
    check("simulated CI coverage", hits / trials, 0.92, 0.995)

    # The vectorized log-CDF used by the fit, against math.erfc
    etas = np.array([-12.0, -8.0, -5.0, -2.0, 0.0, 1.5, 4.0])
    exact = np.array([math.log(0.5 * math.erfc(-e / _SQRT2)) for e in etas])
    check("log Phi(eta) max relative error vs math.erfc (eta -12..4)",
          float(np.max(np.abs((log_norm_cdf(etas) - exact) / np.maximum(1e-300, np.abs(exact)))) +
                np.max(np.abs(np.expm1(log_norm_cdf(etas) - exact)))), 0.0, 1e-6)
    check("binom_tail_ge(72, 1e-14, 2) ~ C(72,2)*1e-28 = 2.556e-25", binom_tail_ge(72, 1e-14, 2) / 2.556e-25, 0.999, 1.001)

    # Synthetic E6 run: draw fail counts for a 64 Mbit chip from a known tail, then refit it
    mu_t, sg_t = retention_model_85C()
    AF = arrhenius_factor(0.6, T_ROOM, T_85)
    n = BENCH["dram64_cells"]
    times = [0.5, 1, 2, 5, 10, 20, 40, 60, 120]
    fails = [int(rng.binomial(n, fail_fraction(t, mu_t, sg_t, AF))) for t in times]
    print(f"  synthetic E6 ladder, equal waits (25 C, Ea 0.6): {dict(zip(times, fails))}")
    mu_f, sg_f = fit_retention_from_counts(times, fails, n)
    check("refit sigma_ln / true (one seed)", sg_f / sg_t, 0.9, 1.1)
    check("refit median shift |d mu| (ln units)", abs((mu_f - math.log(AF)) - mu_t), 0.0, 0.3)

    # Spread of the fit over many synthetic chips (the guide quotes this, not one lucky seed)
    ratios = []
    for _ in range(300):
        fk = [int(rng.binomial(n, fail_fraction(t, mu_t, sg_t, AF))) for t in times]
        ratios.append(fit_retention_from_counts(times, fk, n)[1] / sg_t)
    ratios = np.array(ratios)
    within5 = float(np.mean(np.abs(ratios - 1) <= 0.05))
    print(f"  300 synthetic chips: sigma ratio mean {ratios.mean():.3f}, sd {ratios.std():.3f}, 5-95% "
          f"{np.quantile(ratios, 0.05):.3f}-{np.quantile(ratios, 0.95):.3f}, within 5%: {within5:.0%}")
    check("fraction of synthetic chips with sigma within 5%", within5, 0.85, 1.0)

    # Timing trap: refresh burst, then a slow sequential read (1 MB/s, 8.4 s per pass) of 16,384 rows x 4,096 cells.
    rows_n, cells_row, pass_s = 16384, 4096, 8 * 2 ** 20 / 1e6
    all_t, all_off, all_n, all_k, naive_k = [], [], [], [], []
    for t in times:
        tt, off, nn = per_row_bins(t, rows_n, pass_s, cells_row)
        pf = _norm_cdf_np((np.log((tt + off) / AF) - mu_t) / sg_t)
        kk = rng.binomial(cells_row, pf)
        all_t.append(tt), all_off.append(off), all_n.append(nn), all_k.append(kk)
        naive_k.append(int(kk.sum()))
    print(f"  synthetic slow-read ladder (every row read after t + up to {pass_s:.1f} s): {dict(zip(times, naive_k))}")
    mu_n, sg_n = fit_retention_from_counts(times, naive_k, n)
    mu_r, sg_r, se_r = fit_retention_from_counts(np.concatenate(all_t), np.concatenate(all_k), np.concatenate(all_n),
                                                 t_offset=np.concatenate(all_off), return_se=True)
    for t, kk in zip(times[:4], naive_k[:4]):
        exp_eq = n * fail_fraction(t, mu_t, sg_t, AF)
        print(f"    rung t = {t:>4} s: slow read logged {kk:>4} failures; a true {t} s wait expects {exp_eq:.3g}")
    print(f"  naive fit (assumes every cell waited exactly t): sigma ratio {sg_n/sg_t:.2f}  <- the timing trap "
          "(short rungs are wrong by orders of magnitude; ML weighting hides part of it)")
    print(f"  per-row fit (t_offset = each row's read time):  sigma ratio {sg_r/sg_t:.3f} +- {se_r/sg_t:.3f}")
    check("per-row fit sigma_ln / true under a slow read", sg_r / sg_t, 0.9, 1.1)
    check("per-row fit median shift |d mu| (ln units)", abs((mu_r - math.log(AF)) - mu_t), 0.0, 0.3)

    ok = all(checks)
    print(f"\nSELFTEST {'PASS' if ok else 'FAIL'}: {sum(checks)}/{len(checks)} checks")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--section", type=int, choices=range(len(SECTIONS)), help="print one section only")
    ap.add_argument("--selftest", action="store_true", help="run checks and synthetic-data pipelines")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.section is not None:
        SECTIONS[a.section]()
    else:
        print("home_lab_calcs.py -- first-principles numbers for home-lab/FIRST_PRINCIPLES.md")
        print(f"Study link: {STUDY_LINK}")
        for f in SECTIONS:
            f()
        print("\nDONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
