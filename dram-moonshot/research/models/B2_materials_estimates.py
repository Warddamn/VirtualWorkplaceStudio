#!/usr/bin/env python3
"""B2 (Phase B, lens: NEW MATERIALS & LOW-RESOURCE FABRICATION) first-principles estimates.

Agent key: B2-materials. Written 2026-11-01. Standard library only; `python3` must exit 0.

Every number here is an [ESTIMATE] unless the comment names a source. Inputs that are
judgement calls are logged in research/assumptions/B2-materials.md. Reference anchors are
reused (not re-derived) from:
  - ram-venture/models/dram_cost_stack.py: 1-beta DDR5 $3,800 wafer, 36.5 mm2 16Gb die,
    $1.48/GB, 0.447 Gb/mm2 die-level (teardown).
  - dram-moonshot/research/phaseA/A1_scaling_limits.md: Cs formula, 1-beta pillar
    (21 nm x 1.3 um, EOT 0.55 nm -> ~5.4 fF), leakage budgets 13 fA / 0.84 fA / 0.084 fA,
    bitline table (64 cells -> 8 fF; 512 cells -> 35 fF), EUV $165/wafer/layer.
  - dram-moonshot/research/phaseA/A3_research_frontier.md: vertical 2T0C 10F2,
    array efficiency 0.508, tier cost 12.5% of base wafer, read-BL 0.1 fF/cell + 5 fF.
  - dram-moonshot/research/phaseA/A2_materials_resources.md: fleet 22.2M wafers/yr,
    3.3 m2 capacitor area per wafer, Ge/Ru/Hf/Sc fleet exposure.

Each section is labelled with the idea-card id (B2-xx) it supports.
"""

import math

EPS0 = 8.854e-12          # F/m
Q_E = 1.602e-19           # C
FARADAY = 96485.0         # C/mol

# ---- reference anchors (reused) ----
REF_DENSITY = 0.447       # Gb/mm2 die-level, Micron D1b teardown (A1 table 1)
REF_COST_GB = 1.48        # $/GB, dram_cost_stack.py
REF_WAFER = 3800.0        # $ per 1-beta wafer
WAFER_1C = 4300.0         # $ per 1c wafer (A1)
EUV_LAYER = 165.0         # $/wafer/layer (ram-venture, via A1 sec 5)
FLEET_WAFERS = 22.2e6     # DRAM wafers/yr (A2)
CAP_AREA_M2 = 3.3         # capacitor dielectric area per wafer (A2 model sec 1)
WAFER_AREA_M2 = math.pi * 0.15 ** 2
USABLE_MM2 = 60334.0      # usable mm2 on a 300 mm wafer (ram-venture device_cost_compare)
LEAK_64MS_FA = 13.0       # A1 sec 3
LEAK_1S_FA = 0.84
LEAK_10S_FA = 0.084


def cs_fF(d_nm, h_um, eot_nm):
    """Cylinder (pillar) capacitance, A1 convention: C = 3.9*eps0*pi*d*h/EOT. Returns fF."""
    return 3.9 * EPS0 * math.pi * d_nm * 1e-9 * h_um * 1e-6 / (eot_nm * 1e-9) * 1e15


def h_for_cs_um(cs_target_fF, d_nm, eot_nm):
    return cs_target_fF * 1e-15 * eot_nm * 1e-9 / (3.9 * EPS0 * math.pi * d_nm * 1e-9) * 1e6


def eot_nm(k, t_nm):
    return t_nm * 3.9 / k


def density_gb_mm2(F_nm, cell_F2, eff, bits=1, tiers=1):
    cell_nm2 = cell_F2 * F_nm ** 2
    return 1e12 / cell_nm2 * eff * bits * tiers / 1e9


def hr(title):
    print("\n" + "=" * 100 + "\n" + title + "\n" + "=" * 100)


def main():
    print("B2-materials first-principles estimates (agent B2-materials, 2026-11-01). All [ESTIMATE].")

    # ------------------------------------------------------------------ reference
    hr("REF  1-beta pillar capacitor check against A1")
    ref = cs_fF(21, 1.3, 0.55)
    print(f"1-beta pillar 21 nm x 1.3 um, EOT 0.55 nm -> Cs = {ref:.2f} fF (A1: ~5.4 fF)")

    # ------------------------------------------------------------------ B2-01 AAO
    hr("B2-01  Anodic-alumina (AAO) self-ordered capacitor mold")
    F = 20.0
    pitch = 2 * F                       # 4F2 square lattice, 40 nm pitch (AAO demonstrated interval 40-500 nm)
    pore = 26.0                         # nm after pore widening
    porosity = (math.pi / 4 * pore ** 2) / pitch ** 2
    d_eff = pore - 2 * 3.0 - 5.0        # TiN 3 nm liner, then mid-plane of a ~5 nm ZrO2-class film
    for h in (1.3, 2.0, 2.5, 3.0):
        print(f"  cup-in-pore d_eff {d_eff:.0f} nm, h {h:.1f} um, EOT 0.55 -> Cs = {cs_fF(d_eff, h, 0.55):.2f} fF"
              f"  (pore AR {h * 1000 / pore:.0f}:1)")
    for eff in (0.51, 0.70):
        print(f"  4F2 at F=20 nm, array eff {eff:.2f}: {density_gb_mm2(F, 4, eff):.3f} Gb/mm2"
              f" = {density_gb_mm2(F, 4, eff) / REF_DENSITY:.2f}x 1-beta")
    # anodization charge & energy per wafer for a 2.5 um AAO film
    t_aao = 2.5e-6
    vol_cm3 = WAFER_AREA_M2 * t_aao * 1e6 * (1 - porosity)
    mass_al2o3 = vol_cm3 * 3.0                     # g, porous-AAO skeletal density ~3.0 g/cm3 [ASSUMPTION]
    mol_al = 2 * mass_al2o3 / 101.96
    charge = 3 * mol_al * FARADAY
    energy_kwh = charge * 15.0 / 3.6e6             # 15 V mild anodization
    print(f"  porosity {porosity:.2f}; Al consumed {mol_al * 26.98:.2f} g/wafer; anodization charge {charge:.0f} C;"
          f" energy at 15 V = {energy_kwh * 1000:.1f} Wh/wafer (vs ~1,300 kWh/wafer total fab, A2)")

    # ------------------------------------------------------------------ B2-02 rutile TiO2 on SnO2
    hr("B2-02  SnO2-templated rutile TiO2 (Ru-free) short-stub capacitor")
    for k, t in ((68, 7.0), (80, 7.0), (100, 7.0)):
        e = eot_nm(k, t)
        print(f"  k={k}, t={t} nm -> EOT {e:.3f} nm; h for 5.4 fF at d=21 nm: {h_for_cs_um(5.4, 21, e):.2f} um;"
              f" h for 2.0 fF: {h_for_cs_um(2.0, 21, e):.2f} um")
    e68 = eot_nm(68, 7.0)
    h68 = h_for_cs_um(5.4, 21, e68)
    area_cm2 = math.pi * 21e-7 * h68 * 1e-4
    for j in (1e-8, 1e-7, 1e-6, 1e-5):
        i_fa = j * area_cm2 * 1e15
        print(f"  dielectric J={j:.0e} A/cm2 over {area_cm2:.2e} cm2 -> {i_fa:.4f} fA per cell"
              f" (budgets: 64 ms {LEAK_64MS_FA} fA, 1 s {LEAK_1S_FA} fA, 10 s {LEAK_10S_FA} fA)")
    # Sn demand for 5 nm doped-SnO2 bottom electrodes on the shorter stub area
    cap_area = CAP_AREA_M2 * h68 / 1.3
    sno2_g = cap_area * 5e-9 * 1e6 * 6.95          # g SnO2 in film
    sn_g_consumed = sno2_g * (118.71 / 150.71) / 0.15   # 15% ALD precursor utilization [ASSUMPTION, A2 convention]
    fleet_t = sn_g_consumed * FLEET_WAFERS / 1e6
    print(f"  Sn consumed {sn_g_consumed:.2f} g/wafer -> fleet {fleet_t:.0f} t/yr vs ~300 kt/yr world tin"
          f" = {fleet_t / 3e5 * 100:.3f}% [world tin UNVERIFIED-PK]")

    # ------------------------------------------------------------------ B2-03 Hf-free MPB
    hr("B2-03  Hf-free Zr-based MPB / superlattice super-k")
    for k, t in ((40, 5.6), (56, 5.9), (62, 5.9)):
        e = eot_nm(k, t)
        print(f"  k={k}, t={t} nm -> EOT {e:.3f} nm; h for 5.4 fF at d=21: {h_for_cs_um(5.4, 21, e):.2f} um"
              f" (AR {h_for_cs_um(5.4, 21, e) * 1000 / 21:.0f})")

    # ------------------------------------------------------------------ B2-04 capacitor-first perovskite
    hr("B2-04  Capacitor-first inverted flow, perovskite (Ba,Sr)TiO3 crystallized before any transistor")
    for k, t in ((100, 10.0), (150, 10.0), (250, 12.0)):
        e = eot_nm(k, t)
        print(f"  k={k}, t={t} nm -> EOT {e:.3f} nm; Cs at d=22 nm: h=0.3 um {cs_fF(22, 0.3, e):.2f} fF,"
              f" h=0.5 um {cs_fF(22, 0.5, e):.2f} fF, h=1.0 um {cs_fF(22, 1.0, e):.2f} fF")

    # ------------------------------------------------------------------ B2-05 solid-state ionic EDL capacitor
    hr("B2-05  Solid-state proton double-layer (EDL) nano-capacitor [SPECULATIVE]")
    c_zro2 = 3.9 * EPS0 / 0.55e-9 * 1e2      # uF/cm2 (F/m2 * 1e6 uF/F / 1e4 cm2/m2 = *1e2)
    print(f"  ZrO2-class EOT 0.55 nm areal capacitance = {c_zro2:.2f} uF/cm2")
    for c_sp in (10.0, 20.0, 100.0):
        a_cm2 = 5.4e-15 / (c_sp * 1e-6)
        h_um = a_cm2 * 1e-4 / (math.pi * 21e-9) * 1e6
        print(f"  specific C {c_sp:.0f} uF/cm2 -> h for 5.4 fF at d=21 nm = {h_um:.2f} um")
    a_cm2 = 5.4e-15 / 20e-6
    for sigma in (1e-5, 1e-4, 1e-3):
        r = 5e-7 / (sigma * a_cm2)                  # 5 nm electrolyte
        print(f"  sigma {sigma:.0e} S/cm, 5 nm electrolyte -> R_ion {r:.2e} ohm, RC with 5.4 fF = {r * 5.4e-15 * 1e9:.1f} ns")

    # ------------------------------------------------------------------ B2-06 AlBN flat ferroelectric
    hr("B2-06  AlBN (Sc-free, Hf-free) flat ferroelectric capacitor")
    for pr in (25.0, 130.0):
        for side in (20.0, 40.0):
            q = 2 * pr * 1e-6 * (side * 1e-7) ** 2
            print(f"  2Pr with Pr={pr:.0f} uC/cm2, {side:.0f}x{side:.0f} nm planar -> {q * 1e15:.2f} fC = {q / Q_E:,.0f} e-"
                  f" (1-beta bit ~17,800 e-)")
    for ec in (5.4, 3.0):
        for t in (5.0, 10.0):
            print(f"  Ec {ec} MV/cm x t {t} nm -> coercive voltage {ec * t / 10:.1f} V")
    print(f"  endurance gap: demonstrated >1e6 vs DRAM-class ~3.4e15 (A3) = {3.4e15 / 1e6:.1e}x;"
          f" vs write-light tier 1.6e11 = {1.6e11 / 1e6:.1e}x")

    # ------------------------------------------------------------------ B2-07 Ga-free channel read speed
    hr("B2-07  Ga-free / In-lean channel (ZTO, SnO2, ITZO) read speed")
    for n_cells in (64, 256):
        c_rbl = (0.1 * n_cells + 5.0) * 1e-15
        for i_ua in (0.2, 0.6):
            t = c_rbl * 0.1 / (i_ua * 1e-6)
            print(f"  RBL {n_cells} cells ({c_rbl * 1e15:.1f} fF), read current {i_ua} uA -> 100 mV in {t * 1e9:.1f} ns;"
                  f" 3-bit (x8) {8 * t * 1e9:.0f} ns")

    # ------------------------------------------------------------------ B2-08 in-tier oxide CMOS sense amps
    hr("B2-08  Complementary oxide (n-IGZO/ZTO + p-TeSeOx/SnO) sense amps inside the memory tier")
    # reuse A1 bitline table: 512 cells 35 fF at VARY 1.0 V; 64 cells 8 fF at VARY 0.4 V
    e512 = 35e-15 * 1.0 ** 2 / 2
    e64 = 8e-15 * 0.4 ** 2 / 2
    print(f"  BL CV2/2: 512-cell 35 fF @1.0 V = {e512 * 1e15:.1f} fJ; 64-cell 8 fF @0.4 V = {e64 * 1e15:.2f} fJ;"
          f" ratio {e512 / e64:.0f}x")
    cell_nm2 = 4 * 20 ** 2
    seg_um2 = 64 * cell_nm2 / 1e6
    print(f"  64-cell BL segment at 4F2 F=20 nm covers {seg_um2:.3f} um2; an open-BL SA serving 2 segments gets"
          f" {2 * seg_um2:.3f} um2 per tier it sits under")
    for tiers in (4, 8, 16):
        print(f"    if the SA tier serves a vertical stack of {tiers} memory tiers: {2 * seg_um2 * tiers:.2f} um2 per SA")
    sigma_vt = 0.04
    print(f"  oxide TFT sigma(Vt) ~{sigma_vt * 1000:.0f} mV [ASSUMPTION] -> 6-sigma SA offset ~{6 * sigma_vt * 1.414 * 1000:.0f} mV"
          f" without offset cancellation vs 215 mV fresh signal at 64 cells (A1)")

    # ------------------------------------------------------------------ B2-09 Ge-free NAND-line 3D
    hr("B2-09  Ge-free, NAND-line 3D oxide gain cell (oxide/nitride mold, channel replacement)")
    for F_, b, n in ((40, 1, 16), (40, 3, 16), (40, 3, 32), (30, 2, 32)):
        d = density_gb_mm2(F_, 10, 0.508, b, n)
        print(f"  vertical 2T0C 10F2, F={F_} nm, {b} b x {n} tiers: {d:.2f} Gb/mm2 = {d / REF_DENSITY:.1f}x 1-beta")
    print("  Ge avoided at fleet scale (A2 sec 4): 9-53 t/yr = 6-38% of refined world Ge")

    # ------------------------------------------------------------------ B2-10 fluorine-free carbon mold
    hr("B2-10  Fluorine-free carbon mold (O2/COS etch of amorphous carbon; thermal-O2 recess)")
    # areal density of holes per wafer etched in fluorocarbon chemistry today: capacitor + contacts.
    holes_per_mm2 = 1e12 / 1070.0      # one capacitor hole per 1-beta cell (nm2 per mm2)
    print(f"  capacitor holes per mm2 at 1-beta ~{holes_per_mm2:.2e}; per wafer ~{holes_per_mm2 * USABLE_MM2:.2e}"
          " -- every one is a C4F6/C4F8-class HAR etch today")
    c_mold_mass = WAFER_AREA_M2 * 1.3e-6 * 1e6 * 1.8   # g of a-C (1.8 g/cm3) for a 1.3 um mold
    print(f"  a 1.3 um amorphous-carbon mold is {c_mold_mass:.2f} g C/wafer, burned to CO2 = {c_mold_mass * 44 / 12:.2f} g CO2"
          " (vs fluorocarbon GWP 100s-1000s x per kg; no PFAS)")

    # ------------------------------------------------------------------ B2-11/12/13/14 patterning
    hr("B2-11..14  Patterning substitutions: value of removing EUV or SAQP layers")
    for n in (1, 2, 3):
        print(f"  {n} EUV layer(s) removed: ${n * EUV_LAYER:.0f}/wafer = {n * EUV_LAYER / WAFER_1C * 100:.1f}% of a $4.3k 1c wafer"
              " (before netting replacement-step cost)")
    for n_imm in (1.44,):
        for s in (0.93, 0.97):
            hp = 193.0 / (4 * n_imm * s)
            print(f"  B2-13 two-beam water-immersion interference: hp = 193/(4*{n_imm}*{s}) = {hp:.1f} nm;"
                  f" crossed exposures -> {2 * hp:.0f} nm-pitch posts; +SADP -> {hp:.0f} nm pitch (4F2 F={hp / 2:.1f} nm)")
    # DSA: PS-b-PMMA cylinder L0 vs DRAM capacitor lattice
    print("  B2-11 DSA: PS-b-PMMA hex cylinders L0 ~28-40 nm [UNVERIFIED-PK; imec 37 nm pitch BCP in BACUS 2014]"
          " vs 1-beta honeycomb 35 nm / 1c 32 nm (A1) -> native match; 3x-4x density multiplication from an"
          " ArFi guide at ~70-105 nm pitch")

    # ------------------------------------------------------------------ B2-15 defect tolerance
    hr("B2-15  Defect-tolerant array: random cell-defect fraction p vs ECC strength (16 Gb die)")
    bits = 17.2e9
    for p in (1e-6, 1e-5, 1e-4):
        words = bits / 128
        p2 = math.comb(136, 2) * p ** 2      # SECDED (136,128) fails at >=2
        p3 = math.comb(144, 3) * p ** 3      # BCH t=2 (144,128) fails at >=3
        print(f"  p={p:.0e}: defective cells {p * bits:,.0f}; SECDED failing words {p2 * words:,.0f};"
              f" BCH t=2 failing words {p3 * words:,.1f}")
    print("  -> BCH t=2 (12.5% check bits vs 6.25% for SECDED) plus a few-hundred-word remap CAM tolerates p=1e-4,"
          " i.e. ~100x the random-defect fraction, before soft-error budget")

    # ------------------------------------------------------------------ B2-16 monolithic BEOL memory on logic
    hr("B2-16  Monolithic BEOL main memory inside the logic die's metal stack")
    for b, n in ((3, 8), (3, 16)):
        d = density_gb_mm2(40, 10, 0.508, b, n)
        cap_gb = d * 800 / 8
        tier_cost = 500.0
        cost_gb = n * tier_cost / (d * USABLE_MM2 / 8 * 0.8)
        print(f"  F=40 nm 10F2 {b} b x {n} tiers: {d:.2f} Gb/mm2 -> {cap_gb:.0f} GB over an 800 mm2 die;"
              f" added cost at ${tier_cost:.0f}/tier/wafer, 80% yield = ${cost_gb:.2f}/GB")
    for bw_tbs in (8, 16):
        saved = (3.5 - 0.2) * 1e-12 * bw_tbs * 1e12 * 8
        print(f"  at {bw_tbs} TB/s, 3.5 -> 0.2 pJ/bit saves {saved:.0f} W per accelerator")

    # ------------------------------------------------------------------ B2-17 glass carrier mini-line
    hr("B2-17  BEOL-only cell mini-line on reusable glass carriers, bonded to trailing-node periphery")
    print("  wafers per memory wafer-equivalent: PUC today = 2 prime Si (cell + periphery);"
          " reusable carrier = 1 prime Si + carrier/N_reuse")
    for reuse in (10, 50):
        print(f"    carrier reused {reuse}x -> {1 + 1 / reuse:.2f} wafer-equivalents (vs 2.0): prime-Si/HPQ demand"
              f" -{(1 - (1 + 1 / reuse) / 2) * 100:.0f}% for the cell side")
    for capex in (145e3, 170e3):
        print(f"  DRAM greenfield ${capex / 1e3:.0f}k/wpm (A1) vs BEOL-only line assumed 30-40% of it"
              f" -> ${capex * 0.3 / 1e3:.0f}-{capex * 0.4 / 1e3:.0f}k/wpm [ASSUMPTION]")

    # ------------------------------------------------------------------ B2-18 trailing-node reuse
    hr("B2-18  Trailing-node (65-90 nm) fab reuse: CMOS-under-array deep-tier MLC oxide memory")
    for F_ in (65.0, 90.0):
        bn = REF_DENSITY / density_gb_mm2(F_, 10, 0.508)
        bn_cua = REF_DENSITY / density_gb_mm2(F_, 10, 0.70)
        print(f"  F={F_:.0f} nm vertical 10F2: break-even bits x tiers = {bn:.1f} (eff 0.508), {bn_cua:.1f} (CuA eff 0.70)")
    base = 1300.0                       # depreciated-line wafer, ram-venture DDR4 1y row
    for tier in (80.0, 162.5):          # $80 = depreciated-tool judgement; $162.5 = A2/A3 convention (12.5% of base)
        for b, n in ((3, 16), (3, 24), (4, 16)):
            d = density_gb_mm2(65, 10, 0.70, b, n)
            wafer = base + n * tier
            bits_per_dollar = (d / REF_DENSITY) * (REF_WAFER / wafer)
            print(f"  tier ${tier:.0f}: F=65 nm, CuA eff 0.70, {b} b x {n} tiers: {d:.2f} Gb/mm2 ({d / REF_DENSITY:.2f}x);"
                  f" wafer ${wafer:.0f} -> {bits_per_dollar:.2f}x 1-beta bits/$ (before yield)")

    # ------------------------------------------------------------------ B2-19 panel-level
    hr("B2-19  Panel-level 3D oxide memory [SPECULATIVE]")
    gen35 = 0.62 * 0.75
    print(f"  Gen 3.5 panel 620x750 mm = {gen35:.3f} m2 = {gen35 / WAFER_AREA_M2:.1f}x a 300 mm wafer")
    for F_, b, n in ((100, 3, 64), (100, 2, 128), (50, 3, 64)):
        d = density_gb_mm2(F_, 10, 0.5, b, n)
        tb = d * gen35 * 1e6 * 0.8 / 8 / 1000
        print(f"  F={F_} nm 10F2 {b} b x {n} tiers: {d:.2f} Gb/mm2 ({d / REF_DENSITY:.1f}x); usable 80% -> {tb:.0f} TB per panel")

    # ------------------------------------------------------------------ B2-20 self-assembled tiers
    hr("B2-20  Self-assembled tier stack: parallel BCP lamellae + sequential infiltration synthesis [SPECULATIVE]")
    for L0 in (25.0, 40.0):
        for film in (1.0, 2.0):
            print(f"  L0 {L0:.0f} nm, film {film:.1f} um -> {film * 1000 / L0:.0f} periods (tiers) from one coat")
    print("  tier-thickness tolerance target ~+/-1 nm (4% of 25 nm); BCP L0 scales with N^(2/3) so"
          " molecular-weight dispersity sets the floor [UNVERIFIED-PK]")
    print("\nDone.")


if __name__ == "__main__":
    main()
