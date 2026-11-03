#!/usr/bin/env python3
"""
expected_numbers.py -- first-principles predictions for E7 (home-made oxide transistor)
and E8 (home-made oxide gain-cell memory). Track T4, dram-moonshot home lab.

Run:  python3 expected_numbers.py            (prints every table; exit 0)
      python3 expected_numbers.py --json out.json   (also dumps the numbers)

Pure standard library + numpy. Every input below carries an evidence tag:
  [REPORTED]  literature or vendor number (see the E7/E8 Sources sections)
  [DATASHEET] vendor datasheet value
  [ESTIMATE]  our planning assumption or arithmetic
  [UNVERIFIED] could not be confirmed this session
Change the PLAN dict to match YOUR device once you have measured it.
"""

import json
import math
import sys

import numpy as np

Q = 1.602176634e-19      # C, elementary charge
KB = 1.380649e-23        # J/K
KB_EV = 8.617333262e-5   # eV/K
EPS0 = 8.8541878128e-12  # F/m
H_PLANCK = 6.62607015e-34
M0 = 9.1093837015e-31    # kg

# ------------------------------------------------------------------------------------------
# Planning inputs (edit these after you measure)
# ------------------------------------------------------------------------------------------
PLAN = {
    # Gate stack
    "tox_nm": 300.0,          # thermal SiO2 on p++ Si (Ossila Pt chips and MTI wafers) [REPORTED]
    "eps_sio2": 3.9,          # [REPORTED, textbook]
    # Route A: Ossila Pt test chip, one channel  (W 1 mm, L 2-10 um) [REPORTED]
    "A_W_um": 1000.0, "A_L_um": 10.0,
    # Route B: bare wafer + silver-paint top contacts over a wire mask [ESTIMATE]
    "B_W_um": 3000.0, "B_L_um": 100.0,
    # Home ZnO film (aqueous zinc-ammine, 300 C hot plate) [ESTIMATE from REPORTED 0.9-5 cm2/Vs]
    "mu_cm2Vs": 0.3,
    "vth_V": 8.0,             # [ESTIMATE] enhancement mode on 300 nm SiO2
    "ss_V_per_dec": 1.0,      # [ESTIMATE] trap-rich film on thick oxide
    "ioff_floor_A": 1e-12,    # [ESTIMATE] DIY rig floor (100 Mohm TIA, guarded)
    # E8 storage node
    "c_store_F": 10e-9,       # added C0G / polypropylene capacitor [ESTIMATE choice]
    "c_read_gate_F": 50e-12,  # 2N7000 input capacitance, 40-60 pF per distributors [UNVERIFIED]
    "c_wiring_F": 10e-12,     # air-wired node [ESTIMATE]
    "sn_pad_area_mm2": 1.0,   # storage-side electrode area over the back gate [ESTIMATE]
    "wwl_high_V": 27.5,       # write word line high (<= 30 V rule)
    "v_one_V": 3.0,           # stored "1" (re-picked from calibration in practice)
    "dv_retention_V": 0.1,    # retention criterion: time to lose 100 mV
    # Leakage planning values for E8 (E2 measures the silicon side for real)
    "I_ox_25C_A": 1e-12, "Ea_ox_eV": 0.35,   # [ESTIMATE] floor/trap-limited home TFT
    "I_si_25C_A": 1e-11, "Ea_si_lo_eV": 0.56, "Ea_si_hi_eV": 1.12,  # [ESTIMATE] junction-limited
}

TEMPS_C = [25.0, 45.0, 65.0]
OUT = {}


def hr(title):
    print("\n" + "=" * 92)
    print(title)
    print("=" * 92)


def cox_F_per_cm2(tox_nm, eps_r=3.9):
    return eps_r * EPS0 / (tox_nm * 1e-9) / 1e4   # F/m2 -> F/cm2


def kT_eV(tc):
    return KB_EV * (tc + 273.15)


# ------------------------------------------------------------------------------------------
# E7 section 1: gate capacitor and channel charge (Gauss's law)
# ------------------------------------------------------------------------------------------
def s1_gate():
    hr("E7-1  Gate capacitance and induced electrons (Gauss's law, Q = Cox * (Vg - Vth))")
    rows = []
    for t in (100.0, 230.0, 300.0):
        c = cox_F_per_cm2(t)
        n20 = c * 20.0 / Q
        rows.append((t, c, n20))
        print(f"SiO2 {t:5.0f} nm: Cox = {c*1e9:6.2f} nF/cm2 ; at Vg-Vth = 20 V -> {n20:.2e} electrons/cm2")
    OUT["cox_nF_cm2"] = {f"{int(t)}nm": round(c * 1e9, 3) for t, c, _ in rows}
    print("Lesson: thinner oxide = same charge at lower voltage. 300 nm needs ~3x the volts of 100 nm.")


# ------------------------------------------------------------------------------------------
# E7 section 2: why wide-bandgap oxides leak so little (Boltzmann statistics)
# ------------------------------------------------------------------------------------------
def nc_nv(m_eff):
    """Effective density of states at 300 K, cm^-3, for effective mass m_eff (units of m0)."""
    T = 300.0
    return 2.0 * (2 * math.pi * m_eff * M0 * KB * T / H_PLANCK ** 2) ** 1.5 / 1e6


def s2_bandgap():
    hr("E7-2  Intrinsic carrier density n_i = sqrt(Nc*Nv)*exp(-Eg/2kT) and generation leakage")
    mats = [
        # name, Eg eV, me*, mh*  (textbook values [REPORTED, textbook]; IGZO masses [UNVERIFIED])
        ("Si", 1.12, 1.08, 0.81),
        ("ZnO", 3.37, 0.28, 0.59),
        ("a-IGZO (Eg~3.1)", 3.1, 0.34, 1.0),
    ]
    tau_s, wdep_cm = 1e-6, 1e-4   # generation lifetime 1 us, depletion width 1 um [ESTIMATE]
    res = {}
    print(f"{'material':18s} {'Eg eV':>6s} {'n_i cm^-3':>11s} {'J_gen A/cm2':>12s} {'Ea_gen eV':>9s} {'Ea_diff eV':>10s}")
    for name, eg, me, mh in mats:
        ni = math.sqrt(nc_nv(me) * nc_nv(mh)) * math.exp(-eg / (2 * kT_eV(26.85)))
        jgen = Q * ni * wdep_cm / (2 * tau_s)
        res[name] = (ni, jgen)
        print(f"{name:18s} {eg:6.2f} {ni:11.2e} {jgen:12.2e} {eg/2:9.2f} {eg:10.2f}")
    ratio = res["Si"][0] / res["ZnO"][0]
    print(f"\nn_i(Si)/n_i(ZnO) = {ratio:.1e}. A silicon p-n junction has a thermal-generation floor;")
    print("an oxide TFT has no p-n junction and its intrinsic floor is ~1e19x lower, so its off-current")
    print("is set by gate bias (subthreshold), defects and leakage paths -- engineering, not physics.")
    print("That is exactly why the study's biggest unknown is the DEFECT TAIL, not the median.")
    # Silicon generation leakage of a 1 mm2 junction for scale
    print(f"Silicon junction, 1 mm2, J_gen above: {res['Si'][1]*1e-2:.1e} A at 27 C (doubles every ~8-10 C).")
    OUT["ni"] = {k: v[0] for k, v in res.items()}
    OUT["ni_ratio_si_over_zno"] = ratio


def s3_subthreshold():
    hr("E7-3  Subthreshold swing SS = ln(10)*(kT/q)*(1 + C_traps/Cox)  (Boltzmann limit)")
    for tc in TEMPS_C:
        print(f"Ideal SS at {tc:4.0f} C = {math.log(10)*kT_eV(tc)*1000:5.1f} mV/decade")
    cox = cox_F_per_cm2(PLAN["tox_nm"])
    print("\nTrap density implied by a measured SS on 300 nm SiO2 (Dit = (SS/SS_ideal - 1)*Cox/q):")
    for ss in (0.3, 0.5, 1.0, 2.0):
        dit = (ss / (math.log(10) * kT_eV(25)) - 1) * cox / Q
        print(f"  SS {ss:3.1f} V/dec -> Dit ~ {dit:.1e} states/(cm2 eV)")
    OUT["ss_ideal_mV_dec"] = {f"{int(t)}C": round(math.log(10) * kT_eV(t) * 1000, 2) for t in TEMPS_C}


def s4_depletion():
    hr("E7-4  Can the gate turn the film off?  Charge balance q*Nd*t = Cox*dV")
    cox = cox_F_per_cm2(PLAN["tox_nm"])
    print(f"Cox = {cox*1e9:.2f} nF/cm2 (300 nm). Volts needed to sweep ALL free electrons out of the film:")
    print(f"{'Nd (cm^-3)':>11s}" + "".join(f"{t:>9.0f} nm" for t in (5, 10, 20, 40)))
    table = {}
    for nd in (1e16, 1e17, 1e18, 1e19):
        vals = [Q * nd * t * 1e-7 / cox for t in (5, 10, 20, 40)]
        table[f"{nd:.0e}"] = vals
        print(f"{nd:11.0e}" + "".join(f"{v:10.1f} V" for v in vals))
    print("ZnO films are ~1e16-1e17 (easy to turn off). Undoped In2O3 can be ~1e18-1e19, so it must be")
    print("ultrathin (<~10 nm) or alloyed with Ga/Zn -- the same reason industry uses IGZO, not In2O3.")
    print("No holes form in the oxide (n_i is tiny), so the film can sit in deep depletion indefinitely.")
    OUT["depletion_V"] = table


def s5_film():
    hr("E7-5  Film thickness from spin coating (mass balance)")
    # ZnO: M = 81.38 g/mol, rho = 5.61 g/cm3 [REPORTED textbook]; In2O3: 277.64 g/mol, 7.18 g/cm3
    for name, M, rho, per in (("ZnO", 81.38, 5.61, 1), ("In2O3", 277.64, 7.18, 2)):
        vm = M / rho  # cm3 per mol of oxide formula unit
        for wet_um in (1.0, 3.0):
            for conc in (0.1, 0.2):
                t_nm = wet_um * 1e-4 * conc * 1e-3 / per * vm * 1e7
                print(f"{name:6s} {conc:.1f} M, wet film {wet_um:.0f} um -> ~{t_nm:4.1f} nm dense oxide per coat")
    print("Water inks give a few nm per coat at 3000 rpm [ESTIMATE]; 2-4 coats -> 10-20 nm ZnO.")


def precursor_masses():
    hr("E7-6  Precursor masses for 10 mL of 0.1 M ink")
    rows = [
        ("ZnO powder (dissolve in 28-30% NH3(aq))", 81.38),
        ("Zn(NO3)2.6H2O (for IZO/IGZO)", 297.49),
        ("In(NO3)3, anhydrous basis (scale by label MW)", 300.83),
        ("Ga(NO3)3, anhydrous basis (scale by label MW)", 255.74),
    ]
    for name, mw in rows:
        print(f"{name:48s} MW {mw:7.2f} g/mol -> {0.1*0.010*mw*1000:6.1f} mg")
    nh3 = 0.28 * 898.0 / 17.031
    print(f"28 wt% ammonia (density ~0.898 g/mL) = {nh3:.1f} M NH3 -> 150x excess over 0.1 M Zn [ESTIMATE].")
    print("Hydrated salts: always use the molecular weight printed on YOUR bottle.")


def s7_currents():
    hr("E7-7  Expected drain currents (square law, saturation) and the rig ranges you need")
    cox = cox_F_per_cm2(PLAN["tox_nm"])
    mu = PLAN["mu_cm2Vs"]
    vth = PLAN["vth_V"]
    out = {}
    for route in ("A", "B"):
        W, L = PLAN[f"{route}_W_um"], PLAN[f"{route}_L_um"]
        k = 0.5 * mu * cox * W / L         # A/V^2
        for vg in (15.0, 20.0, 25.5):        # 25.5 V = rig maximum (28 V node - 2.5 V VREF)
            idsat = k * (vg - vth) ** 2
            print(f"Route {route} (W/L={W/L:5.0f}) Vgs={vg:4.1f} V -> Id_sat ~ {idsat*1e6:7.2f} uA")
        ion = k * (25.5 - vth) ** 2
        # current exactly at Vth from subthreshold/strong-inversion matching (EKV-like): (n*phi)^2
        nphi = PLAN["ss_V_per_dec"] / math.log(10)
        i_vth = k * (2 * nphi) ** 2 * math.log(2) ** 2
        out[route] = {"Ion_A": ion, "I_at_Vth_A": i_vth,
                      "on_off_at_floor": ion / PLAN["ioff_floor_A"]}
        print(f"  current near Vth ~ {i_vth:.1e} A ; on/off limited by 1 pA floor ~ {ion/PLAN['ioff_floor_A']:.1e}")
        # subthreshold-predicted channel current at hold biases
        for vgs in (0.0, -2.0):
            ich = i_vth * 10 ** ((vgs - vth) / PLAN["ss_V_per_dec"])
            print(f"  channel current predicted at Vgs={vgs:+.0f} V: {ich:.1e} A  (measured value will be the floor)")
        # write time constant in E8: R_on in linear region at Vgs = WWL - V1
        vgs_w = PLAN["wwl_high_V"] - PLAN["v_one_V"]
        ron = 1.0 / (mu * cox * W / L * (vgs_w - vth))
        ctot = PLAN["c_store_F"] + PLAN["c_read_gate_F"] + PLAN["c_wiring_F"]
        print(f"  E8 write: R_on ~ {ron/1e3:.0f} kohm -> tau = R_on*C_SN ~ {ron*ctot*1e3:.1f} ms (write pulse >= 10 tau)")
        out[route]["R_on_ohm"] = ron
        out[route]["tau_write_s"] = ron * ctot
    OUT["currents"] = out
    print("\nDIY transimpedance ranges (ADS1115 +/-2.048 V, 62.5 uV LSB; +/-0.256 V PGA -> 7.8 uV LSB):")
    for rf in (1e4, 1e6, 1e8):
        fs = 2.0 / rf
        lsb = 62.5e-6 / rf
        lsb_hi = 7.8125e-6 / rf
        jn = math.sqrt(4 * KB * 298.15 * 10.0 / rf)
        print(f"  Rf {rf:8.0e} ohm: full scale {fs:.1e} A, LSB {lsb:.1e} A (best {lsb_hi:.1e} A), "
              f"Johnson noise (10 Hz) {jn:.1e} A rms")
    print("Needed span: ~1e-4 A on to ~1e-12 A off = 8 decades -> three ranges + E4 bench below 1 pA.")


# ------------------------------------------------------------------------------------------
# E8 sections
# ------------------------------------------------------------------------------------------
def e8_node():
    hr("E8-1  Storage node, kickback (charge conservation) and retention t = C*dV/I")
    cox = cox_F_per_cm2(PLAN["tox_nm"])
    c_ov = cox * PLAN["sn_pad_area_mm2"] * 1e-2     # mm2 -> cm2
    c_tot = PLAN["c_store_F"] + PLAN["c_read_gate_F"] + PLAN["c_wiring_F"] + c_ov
    fast = PLAN["wwl_high_V"] * c_ov / c_tot
    slow = (PLAN["v_one_V"] + PLAN["vth_V"]) * c_ov / c_tot
    print(f"Storage-side pad over back gate: {PLAN['sn_pad_area_mm2']} mm2 -> C_ov = {c_ov*1e12:.0f} pF")
    print(f"C_SN total = {c_tot*1e9:.2f} nF (10 nF added + read gate + wiring + C_ov)")
    print(f"Kickback when WWL falls: fast edge {fast*1000:.0f} mV ; slow edge (after switch-off only) {slow*1000:.0f} mV")
    for cs in (1e-9, 10e-9, 47e-9):
        ct = cs + PLAN["c_read_gate_F"] + PLAN["c_wiring_F"] + c_ov
        print(f"  with C_store {cs*1e9:4.0f} nF: fast-edge kick {PLAN['wwl_high_V']*c_ov/ct:5.2f} V")
    print("Lesson: the gate overlap that every back-gated TFT has is a coupling capacitor. Real 2T0C cells")
    print("fight the same kickback; here you beat it with a big C_store and a small storage-side pad.")
    OUT["c_sn_F"] = c_tot
    OUT["kick_fast_V"] = fast
    OUT["kick_slow_V"] = slow
    return c_tot


def arrh(i25, ea, tc):
    return i25 * math.exp(-ea / KB_EV * (1 / (tc + 273.15) - 1 / 298.15))


def e8_retention(c_tot):
    hr("E8-2  Expected retention, oxide switch vs silicon switch (Arrhenius I = I0*exp(-Ea/kT))")
    dv = PLAN["dv_retention_V"]
    print(f"Retention = time to lose {dv*1000:.0f} mV on C_SN = {c_tot*1e9:.2f} nF.")
    print(f"{'T (C)':>6s} {'I_oxide':>10s} {'t_oxide':>10s} {'I_Si(Ea .56)':>13s} {'t_Si':>9s} "
          f"{'I_Si(Ea 1.12)':>14s} {'t_Si':>9s} {'ratio (.56/1.12)':>17s}")
    rows = {}
    for tc in TEMPS_C:
        iox = arrh(PLAN["I_ox_25C_A"], PLAN["Ea_ox_eV"], tc)
        isl = arrh(PLAN["I_si_25C_A"], PLAN["Ea_si_lo_eV"], tc)
        ish = arrh(PLAN["I_si_25C_A"], PLAN["Ea_si_hi_eV"], tc)
        tox, tsl, tsh = c_tot * dv / iox, c_tot * dv / isl, c_tot * dv / ish
        rows[tc] = dict(I_ox=iox, t_ox=tox, I_si_lo=isl, t_si_lo=tsl, I_si_hi=ish, t_si_hi=tsh)
        print(f"{tc:6.0f} {iox:10.1e} {tox:9.0f}s {isl:13.1e} {tsl:8.1f}s {ish:14.1e} {tsh:8.1f}s "
              f"{tox/tsl:8.0f} / {tox/tsh:<6.0f}")
    g_lo = (rows[65]["t_ox"] / rows[65]["t_si_lo"]) / (rows[25]["t_ox"] / rows[25]["t_si_lo"])
    g_hi = (rows[65]["t_ox"] / rows[65]["t_si_hi"]) / (rows[25]["t_ox"] / rows[25]["t_si_hi"])
    print(f"\nAdvantage growth 25 -> 65 C: x{g_lo:.1f} (Si Ea 0.56) to x{g_hi:.0f} (Si Ea 1.12).")
    print("Prediction: the oxide cell's lead widens as it gets hotter IF the oxide leakage has a lower")
    print("activation energy than the silicon junction. If both have Ea ~0.8 eV (as the study assumed for")
    print("imec cells), the ratio stays flat and the win is the absolute level. E8 measures which.")
    # crossover temperature if oxide Ea were higher than Si's (what-if)
    ea_ox_hi = 1.3
    # solve i_ox(T) = i_si(T) with Si Ea 0.56: ln(iox25/isi25) = (Ea_ox - Ea_si)/k*(1/T - 1/298)
    lnr = math.log(PLAN["I_ox_25C_A"] / PLAN["I_si_25C_A"])
    inv_t = 1 / 298.15 + lnr * KB_EV / (ea_ox_hi - PLAN["Ea_si_lo_eV"])
    print(f"What-if: oxide Ea {ea_ox_hi} eV vs Si 0.56 eV -> lines cross at {1/inv_t-273.15:.0f} C.")
    OUT["retention"] = {str(int(k)): v for k, v in rows.items()}
    OUT["advantage_growth_25_to_65"] = [g_lo, g_hi]
    # droop-rate comparison with imec (study dossier: 0.15 fF, 75 zA)
    home = PLAN["I_ox_25C_A"] / c_tot
    imec = 75e-21 / 0.15e-15
    print(f"\nDroop rate I/C: home cell {home:.1e} V/s vs imec 2T0C (75 zA on 0.15 fF) {imec:.1e} V/s.")
    print("Similar droop rates, for opposite reasons: the home cell leaks ~1e7x more charge but stores")
    print("~7e7x more. That is why a home retention time says nothing direct about scaled devices.")
    OUT["droop_V_per_s"] = {"home": home, "imec_from_dossier": imec}


def e8_hold_bias():
    hr("E8-3  Hold-bias test: subthreshold says leakage falls 10x per SS volts of more-negative hold")
    i_vth = OUT["currents"]["A"]["I_at_Vth_A"]
    for vgs in (4.0, 2.0, 0.0, -2.0):
        ich = i_vth * 10 ** ((vgs - PLAN["vth_V"]) / PLAN["ss_V_per_dec"])
        seen = max(ich, PLAN["ioff_floor_A"])
        print(f"Vgs(hold) {vgs:+4.1f} V: channel {ich:.1e} A -> you will see ~{seen:.1e} A")
    print("Silicon switch (Vth ~2 V): below Vgs ~0.5 V the junction floor dominates, so making the hold")
    print("more negative does NOT help (it can hurt via GIDL). The oxide switch keeps improving until a floor.")


def e8_rtn_and_tails():
    hr("E8-4  What a home device cannot see: single-trap RTN and 1e-4 tails")
    cox_home = cox_F_per_cm2(PLAN["tox_nm"]) * 1e4        # F/m2
    a_home = PLAN["A_W_um"] * PLAN["A_L_um"] * 1e-12        # m2
    dvt_home = Q / (cox_home * a_home)
    cox_scaled = 3.9 * EPS0 / 4e-9                          # EOT 4 nm (dossier)
    dvt_scaled = Q / (cox_scaled * 0.01e-12)
    print(f"One trapped electron shifts Vt by q/(Cox*A): home TFT ({a_home*1e12:.0f} um2) {dvt_home*1e6:.2f} uV;")
    print(f"scaled cell (0.01 um2, EOT 4 nm) {dvt_scaled*1e3:.2f} mV -> {dvt_scaled/dvt_home:.0e}x larger.")
    print("So RTN that matters at 0.01 um2 is invisible at home. Do not claim RTN results from E7/E8.")
    print("\nTail statistics: to see a quantile q you need ~10 devices beyond it -> N >= 10/q.")
    for n in (4, 20, 100, 1e4, 1e5):
        print(f"  N = {n:>8.0f} devices -> smallest trustworthy quantile ~ {min(10/n, 0.5):.0e}")
    print("The study's pass lines live at 1e-4 to 2e-5 -> N >= 1e5-5e5 cells: a nanofab array, not a home bench.")
    OUT["rtn_dvt_home_V"] = dvt_home
    OUT["rtn_dvt_scaled_V"] = dvt_scaled


def bom():
    hr("Bill of materials totals (approx USD, Nov 2026; see the parts tables for tags and sources)")
    e7_core = {
        "MTI 100 mm p++ Si / 300 nm SiO2 wafer": 110, "diamond scribe": 12,
        "ZnO 99.999% 25 g (cheaper 99.9% grades ~40)": 181, "ammonium hydroxide 28-30% 500 mL": 50,
        "syringe filters + syringes": 25, "glass vials, PTFE caps": 15, "silver conductive paint": 25,
        "fine wire for channel mask": 10, "digital ceramic hot plate (<=380-400 C)": 290,
        "K-type thermocouple meter + Al block": 30, "DIY spin coater parts": 80, "0.001 g scale": 30,
        "USB microscope": 40, "PPE: splash goggles, nitrile gloves, lab coat": 55,
    }
    rig = {
        "Raspberry Pi Pico 2": 5, "ADS1115 breakout": 15, "LMC6482 x2": 8, "LM358 x2": 2,
        "LM4040-2.5 ref": 1, "reed relays x3": 10, "precision resistors incl. 100 Mohm": 12,
        "PTFE standoffs": 5, "0-30 V bench supply": 65, "metal tin (dark + shield) + silica gel": 15,
        "multimeter": 30, "perfboard, wire, BNC": 20,
    }
    e8 = {
        "2N7000 x10": 4, "C0G/polypropylene 10 nF x6": 6, "heater resistor + MOSFET + NTC + fuse": 15,
        "aluminum block": 5, "12 V adapter": 10, "extra chips/wafer pieces for 4-6 TFTs": 0,
    }
    indium = {"indium nitrate 99.99% 10 g": 163, "zinc nitrate hexahydrate 100 g": 40,
              "gallium nitrate hydrate (optional)": 150}
    for name, d in (("E7 materials + process tools", e7_core), ("T4 mini-SMU rig", rig),
                    ("E8 add-on", e8), ("Optional IZO/IGZO upgrade", indium)):
        print(f"{name:32s} ~${sum(d.values()):,}")
    tot = sum(e7_core.values()) + sum(rig.values()) + sum(e8.values())
    print(f"{'E7 + rig + E8 (no indium)':32s} ~${tot:,}  (about ${tot - 290 - 80:,} if a makerspace lends hot plate + spin coater)")
    OUT["bom_usd"] = {"e7": sum(e7_core.values()), "rig": sum(rig.values()), "e8": sum(e8.values()),
                      "indium_upgrade": sum(indium.values()), "total_no_indium": tot}


def main(argv):
    s1_gate()
    s2_bandgap()
    s3_subthreshold()
    s4_depletion()
    s5_film()
    precursor_masses()
    s7_currents()
    c_tot = e8_node()
    e8_retention(c_tot)
    e8_hold_bias()
    e8_rtn_and_tails()
    bom()
    if "--json" in argv:
        path = argv[argv.index("--json") + 1]
        with open(path, "w") as f:
            json.dump(OUT, f, indent=1, default=float)
        print(f"\nwrote {path}")
    # sanity checks so a broken edit fails loudly
    assert abs(OUT["cox_nF_cm2"]["300nm"] - 11.51) < 0.05
    assert OUT["ni_ratio_si_over_zno"] > 1e15
    assert np.isfinite(OUT["c_sn_F"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
