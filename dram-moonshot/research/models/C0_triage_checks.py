#!/usr/bin/env python3
"""C0 physics triage checks (lead device physicist, 2026-11-01).

First-principles arithmetic behind the triage verdicts in
research/phaseB/ideas_master.json and TRIAGE.md. Stdlib only; python3 exits 0.
Every result is an [ESTIMATE]; inputs are labelled where they are assumptions.
"""
import math

k_B = 1.380649e-23      # J/K
q = 1.602176634e-19     # C
eps0 = 8.8541878128e-12  # F/m
kT300 = k_B * 300 / q   # eV
kT358 = k_B * 358 / q   # eV (85 C)


def hdr(s):
    print("\n== " + s + " ==")


# ---------------------------------------------------------------- endurance bar
hdr("C0-1 Endurance a DRAM-class cell must survive (10 years)")
ten_yr = 10 * 365.25 * 24 * 3600
for label, period in [("refresh 64 ms", 0.064), ("refresh 1 s", 1.0),
                      ("hot row at tRC 46 ns, 100% duty", 46e-9),
                      ("hot row at 1% duty", 46e-9 / 0.01)]:
    print(f"  {label:34s}: {ten_yr / period:9.2e} cycles")

# ---------------------------------------------------------------- charge fluence
hdr("C0-2 Charge-fluence rule (B5 rule 1) applied to tunnelling contacts")
# B5-07 'soft-landing' revival: ~1 fC per write through a ~10 nm^2 contact coating
for Q_fC, A_nm2 in [(1.0, 10.0), (1.0, 100.0), (0.93, 400.0)]:
    flu = Q_fC * 1e-15 / (A_nm2 * 1e-14)  # C/cm^2 per write
    lo, hi = 1.0 / flu, 100.0 / flu          # amorphous Q_BD 1-100 C/cm^2
    print(f"  {Q_fC} fC through {A_nm2:5.0f} nm^2: {flu:8.2e} C/cm2/write -> "
          f"{lo:8.1e}-{hi:8.1e} writes at Q_BD 1-100 C/cm2")

# ---------------------------------------------------------------- B1-09 FN
hdr("C0-3 B1-09 nanogap: Fowler-Nordheim write time (Schottky-Nordheim corrected)")


def fn_J(phi_eV, F_Vnm):
    """FN current density, A/cm^2, with the simple v(f) image-charge correction."""
    F = F_Vnm * 1e9
    f = 1.439964 * F_Vnm / phi_eV ** 2      # eV nm / eV^2 * V/nm -> dimensionless
    v = 1 - f + (f / 6.0) * math.log(f)
    a = 1.541434e-6                          # A eV V^-2
    b = 6.830890                             # eV^-3/2 V nm^-1
    J = a * F ** 2 / phi_eV * math.exp(-v * b * phi_eV ** 1.5 / F_Vnm)  # A/m^2
    return J * 1e-4


area_cm2 = (20e-7) ** 2
for phi in (4.5, 2.7):
    for gap in (2.5, 3.0):
        for V in (6.0, 8.0):
            J = fn_J(phi, V / gap)
            I = J * area_cm2
            t01 = 0.1e-15 / I
            print(f"  phi {phi} eV gap {gap} nm V {V} V: J {J:9.2e} A/cm2, "
                  f"I {I:8.2e} A, t(0.1 fC) {t01:8.2e} s")

# ---------------------------------------------------------------- B1-06 Schottky
hdr("C0-4 B1-06 vertical SFG: reverse thermionic leakage of the write diode at 85 C")
A_star = 41.0  # A cm^-2 K^-2 for m* ~0.34 m0 (IGZO-class) [ASSUMPTION]
for phi in (0.8, 0.9, 0.95, 1.0, 1.1):
    J = A_star * 358 ** 2 * math.exp(-phi / kT358)
    I = J * area_cm2
    t = 0.2e-15 * 0.2 / I  # 0.2 fF floating gate, 0.2 V droop budget
    print(f"  phi_B {phi:4.2f} eV: I {I:8.2e} A -> retention {t:9.2e} s")

# ---------------------------------------------------------------- B1-19 NbO2
hdr("C0-5 B1-19 NbO2 local sense: heat-capacity floor per decision vs bitline energy")
cv = 3.0e6  # J m^-3 K^-1 volumetric heat capacity, oxide-typical [ASSUMPTION]
dT = 1080 - 358  # NbO2 IMT ~1080 K, ambient 85 C
for side_nm in (10, 20):
    E = cv * (side_nm * 1e-9) ** 3 * dT
    print(f"  {side_nm} nm cube heated by {dT} K: {E * 1e15:6.2f} fJ (zero-loss floor)")
for C_fF, V in [(8.0, 0.4), (35.0, 1.06)]:
    print(f"  bitline C*V^2 at {C_fF} fF, {V} V: {C_fF * V * V:6.2f} fJ")
# thermal noise of the switching volume (sets a floor on threshold noise)
C_th = cv * (10e-9) ** 3
print(f"  dT_rms of a 10 nm cube: {math.sqrt(k_B * 358 ** 2 / C_th):5.2f} K")

# ---------------------------------------------------------------- B5-03 deep levels
hdr("C0-6 B5-03 deep-level bit: emission time vs level depth")
for E in (0.56, 1.0, 1.3):
    for T, kt in ((300, kT300), (358, kT358)):
        for pre in (1e12, 1e13):
            tau = 1.0 / (pre * math.exp(-E / kt))
            print(f"  E {E:4.2f} eV T {T} K prefactor {pre:.0e}: tau {tau:9.2e} s")
print("  Si gap 1.12 eV caps any level at <=0.56 eV from the nearer band edge.")

# ---------------------------------------------------------------- B5-04 pinned well
hdr("C0-7 B5-04 Jot-RAM: doping needed to fully deplete (pin) a 40 nm-wide well")
eps_si = 11.7 * eps0 * 1e-2  # F/cm
w = 40e-7  # cm
for Vpin in (0.5, 1.0):
    N = Vpin * 8 * eps_si / (q * w ** 2)
    Emax = q * N * (w / 2) / eps_si
    print(f"  V_pin {Vpin} V: N_D {N:8.2e} cm-3, peak field {Emax:8.2e} V/cm "
          f"(Si band-to-band tunnelling onset ~5e5-1e6 V/cm)")

# ---------------------------------------------------------------- B5-12 skyrmion
hdr("C0-8 B5-12 skyrmion clock: drive energy per step needed for a low shift-error rate")
for dE in (5, 10, 20, 27.6, 30):
    print(f"  {dE:5.1f} kT per step -> back-hop probability {math.exp(-dE):8.2e}")
print(f"  1e-12 per shift needs {math.log(1e12):.1f} kT; at 5 kT for xi=100 fJ/Vm "
      f"the coefficient must rise ~{math.log(1e12) / 5:.1f}x at equal field")

# ---------------------------------------------------------------- B5-01 ring-down
hdr("C0-9 B5-01 Click-RAM: ring-down after snap-through")
for Q in (10, 100, 1000):
    for f0 in (2e9, 5e9, 15e9):
        tau = Q / (math.pi * f0)
        print(f"  Q {Q:5d} f0 {f0 / 1e9:4.0f} GHz: amplitude tau {tau * 1e9:7.2f} ns, "
              f"5 tau {5 * tau * 1e9:7.1f} ns")

# ---------------------------------------------------------------- B4-17 rate-distortion
hdr("C0-10 B4-17 procedural weights: rate-distortion bound for i.i.d. Gaussian weights")
gran = 0.5 * math.log2(math.pi * math.e / 6)         # entropy-coded uniform scalar gap
fixed = 0.5 * math.log2(math.sqrt(3) * math.pi / 2)  # optimal fixed-rate scalar gap
print(f"  gap of entropy-coded scalar quantiser to R(D): {gran:.3f} bit/weight")
print(f"  gap of optimal fixed-rate scalar (Lloyd-Max, high rate): {fixed:.3f} bit/weight")
print(f"  max storage ratio vs 4-bit entropy-coded scalar: {4 / (4 - gran):.3f}x")
print(f"  max storage ratio vs 4-bit optimal fixed-rate scalar: {4 / (4 - fixed):.3f}x")
print("  a 1.33x claim (3 vs 4 bits at equal distortion) needs inter-weight structure")

# ---------------------------------------------------------------- B1-04 kTC
hdr("C0-11 B1-04 charge-transfer pre-sense: bitline kTC noise vs signal charge")
for Cbl_fF in (35.0,):
    n_rms = math.sqrt(k_B * 358 * Cbl_fF * 1e-15) / q
    for Cs, dV in ((0.5, 0.5), (0.25, 0.5)):
        sig = Cs * 1e-15 * dV / q
        print(f"  Cbl {Cbl_fF} fF kTC {n_rms:5.0f} e- rms; Cs {Cs} fF x {dV} V = "
              f"{sig:6.0f} e- -> {sig / n_rms:5.1f} sigma")

# ---------------------------------------------------------------- B3-13/B5-18 relays
hdr("C0-12 B3-13 + B5-18 inductive relays: energy per bit vs stack height")
for N in (4, 8, 12, 16):
    avg = 0.7 * (N + 1) / 2
    print(f"  {N:2d}-high: average {avg:5.2f} pJ/b, worst {0.7 * N:5.2f} pJ/b "
          f"(HBM TSV path ~3.5 pJ/b incl. interposer)")

# ---------------------------------------------------------------- B3-15 fold
hdr("C0-13 B3-15 origami stack: fold radius and polymer thermal resistance")
for t_um, eps_allow in ((5.0, 0.005), (2.0, 0.03)):
    R = t_um / (2 * eps_allow)
    print(f"  membrane/hinge {t_um} um at {eps_allow * 100:.1f}% strain: R {R:6.0f} um, "
          f"layer pitch {2 * R:6.0f} um")
R_th = 16 * 10e-6 / (0.2 * 1e-4)
print(f"  16 x 10 um polyimide (0.2 W/mK) over 100 mm2: {R_th:5.1f} K/W "
      f"-> {R_th * 3:4.0f} K at 3 W, {R_th * 15:4.0f} K at 15 W")

# ---------------------------------------------------------------- cooling
hdr("C0-14 B3-03 + B4-13 cool memory: Arrhenius retention gain 85 C -> 35 C")
for Ea in (0.25, 0.4, 0.55):
    g = math.exp(Ea / (k_B / q) * (1 / 308.15 - 1 / 358.15))
    print(f"  Ea {Ea} eV: x{g:5.1f}")

print("\nC0 triage checks done.")
