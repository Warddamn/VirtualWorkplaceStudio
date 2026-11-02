#!/usr/bin/env python3
"""
A3_frontier_estimates.py -- first-principles cross-checks for the 2022-2026 research-frontier map
(dram-moonshot phase A3). Owner: A3-frontier. Written 2026-11-01. Pure standard library.

Used by research/phaseA/A3_research_frontier.md. Every input is tagged:
  [REPORTED]  number from a paper/press item logged in research/sources/A3-frontier.jsonl
  [A1]        reused from models/dram_cell_physics.py / A1_scaling_limits.md (sibling agent)
  [ESTIMATE]  my assumption, logged in research/assumptions/A3-frontier.md

Sections:
  1. Oxide 2T0C storage node: Ioff-limited retention vs measured retention (what really limits it)
  2. Read speed of an oxide gain cell (is IGZO "too slow" for DRAM-class 10-100 ns?)
  3. Density and bits-per-wafer-$ of multi-level, multi-tier gain cells vs 1-beta 6F2 1T1C
  4. Ferroelectric 2T-nC stack: footprint per bit, switched charge vs DRAM cell charge, endurance need
  5. VCMA-MRAM write energy vs DRAM refresh/activate energy
  6. Cryogenic (77 K) DRAM: does the refrigerator eat the refresh savings?
  7. Hybrid-bond pitch needed for one bond per bitline segment (disaggregated cell wafer)
  8. PIM: internal-bandwidth ratio vs measured LLM speedup (Amdahl check)
"""

import math

EPS0 = 8.854e-12
Q_E = 1.602e-19

# ---------------------------------------------------------------------------------------------
# Shared anchors
# ---------------------------------------------------------------------------------------------
CELL_1B_UM2 = 0.00107        # [A1] 1-beta 6F2 cell area (~1,070 nm^2), A1-scaling estimate
ARRAY_EFF = 0.508            # [A1] array efficiency used to calibrate 1-beta die density
DRAM_CELL_CHARGE_E = 17800   # [A1] ~charge per DRAM bit (Cs*V), electrons
DRAM_REFRESH_FJ_PER_BIT = 46 # [A1] refresh energy per bit per refresh event


def hr(t):
    print("\n" + "=" * 92)
    print(t)
    print("=" * 92)


# ---------------------------------------------------------------------------------------------
# 1. Retention: Ioff-limited vs measured
# ---------------------------------------------------------------------------------------------
def retention_s(c_sn_fF, dv_mV, i_leak_A):
    return (c_sn_fF * 1e-15) * (dv_mV * 1e-3) / i_leak_A


def section_retention():
    hr("1. Oxide gain cell: channel-leakage-limited retention vs measured")
    cases = [
        # label, I_leak (A)
        ("imec IEDM2020 extracted 3e-19 A/um x W=50 nm", 3e-19 * 0.05),   # [REPORTED] x [ESTIMATE W]
        ("Kioxia OCTRAM / 3D OCTRAM upper bound <1 aA/cell", 1e-18),      # [REPORTED]
        ("Si BCAT 6-sigma tail (A1: <=13 fA for 64 ms)", 13e-15),         # [A1]
    ]
    c_sn = 1.0   # fF storage node (read-transistor gate + parasitic) [ESTIMATE 0.5-2 fF]
    print(f"Storage node C_SN = {c_sn} fF; tolerated droop: 1-bit 200 mV, 3-bit (1 V window/8 levels/2) 62 mV")
    for lab, i in cases:
        t1 = retention_s(c_sn, 200, i)
        t3 = retention_s(c_sn, 62, i)
        print(f"  {lab:58s} I={i:8.1e} A  t(1b)={t1:10.3g} s  t(3b)={t3:10.3g} s")
    measured = {"imec IEDM2020": 400, "imec IEDM2021": 1e3, "imec EDL2025 @95C": 200,
                "IMECAS VLSI2026 3b/cell": 400, "SJTU AFM2026 IGO+HfO2 pass.": 3e4,
                "MoS2 2T0C ACS Nano 2025": 1e3, "Si-MoS2 NatComm 2024": 6e3}
    print("  Measured (REPORTED):", ", ".join(f"{k} {v:g} s" for k, v in measured.items()))
    print("  Total storage-node leakage needed (C_SN=1 fF) for a target retention:")
    for target in (1e3, 1e4, 1e5, 1e6):
        i1 = c_sn * 1e-15 * 0.2 / target
        i3 = c_sn * 1e-15 * 0.062 / target
        print(f"    t={target:8.0e} s ({target/86400:6.2f} days): I_total <= {i1:8.1e} A (1-bit), {i3:8.1e} A (3-bit)")
    print("  -> 1 aA total leakage gives only ~200 s at 1 fF/200 mV, so the 1e3-3e4 s results already imply")
    print("     ~7-200 zA TOTAL node leakage (at 1 fF) (channel + gate stack + passivation + trap emission). SJTU's 100x")
    print("     gain from HfO2 passivation alone says surfaces/interfaces, not the channel bandgap, set retention.")
    print("     Reaching 1e5-1e6 s ('days', refresh-free in practice) is a materials/interface problem: white space.")


# ---------------------------------------------------------------------------------------------
# 2. Read speed
# ---------------------------------------------------------------------------------------------
def section_read_speed():
    hr("2. Gain-cell read time on a read bitline (RBL)")
    i_per_um = 60.9e-6   # [REPORTED] CXMT IEDM 2025 IGZO select transistor, A/um
    for w_nm in (20, 40):
        for cells in (64, 256):
            c_rbl = cells * 0.1e-15 + 5e-15    # [ESTIMATE] 0.1 fF/cell + 5 fF fixed
            i_rd = i_per_um * w_nm * 1e-3 * 0.5  # 50% of Ion at read bias [ESTIMATE]
            t = c_rbl * 0.1 / i_rd               # 100 mV development
            print(f"  W={w_nm:3d} nm, {cells:3d} cells/RBL: C_RBL={c_rbl*1e15:5.1f} fF, I_read={i_rd*1e6:4.2f} uA,"
                  f" t(100 mV)={t*1e9:5.2f} ns; 3-bit (8x finer) ~{8*t*1e9:5.1f} ns")
    print("  -> Even amorphous-oxide read currents develop a sense signal in ~1 ns (1-bit) or ~5-15 ns (3-bit):")
    print("     oxide mobility is NOT a blocker at DRAM-class 10-100 ns; it is a blocker only at SRAM/L2 speeds.")


# ---------------------------------------------------------------------------------------------
# 3. Density and bits per wafer-$
# ---------------------------------------------------------------------------------------------
def section_density():
    hr("3. Multi-level x multi-tier oxide gain cell vs 1-beta 6F2 (cell-level, same array efficiency)")
    ref_bits_per_um2 = 1 / CELL_1B_UM2
    print(f"  1-beta reference: {CELL_1B_UM2*1e6:.0f} nm^2/cell -> {ref_bits_per_um2*ARRAY_EFF*1e-3:.3f} Gb/mm^2 die-level"
          " (array eff 0.508)")
    # wafer-cost model: base (relative to 1-beta wafer) + per-tier adder as fraction of base
    tier_add = 0.125   # [ESTIMATE, same as A2] each extra tier adds 12.5% of base wafer cost
    designs = [
        # label, F (nm), F^2 per cell footprint, base wafer cost vs 1-beta
        ("vertical-channel 2T0C, F=20 nm (SAQP-class litho)", 20, 10, 0.90),
        ("vertical-channel 2T0C, F=40 nm (single-exposure ArFi)", 40, 10, 0.55),
        ("planar 2T0C, F=40 nm", 40, 24, 0.55),
    ]
    print(f"  {'design':52s} {'b':>2s} {'N':>3s} {'um2/bit':>9s} {'Gb/mm2':>7s} {'xDensity':>8s} {'xBits/$':>8s}")
    for lab, f, nf2, base in designs:
        a_cell = nf2 * (f * 1e-3) ** 2
        for b in (1, 2, 3):
            for n in (1, 4, 8, 16):
                a_bit = a_cell / (b * n)
                gbmm2 = ARRAY_EFF / a_bit * 1e-3
                xden = CELL_1B_UM2 / a_bit
                cost = base * (1 + tier_add * (n - 1))
                xbits_per_dollar = xden / cost
                if (b, n) in ((1, 1), (2, 4), (3, 4), (2, 8), (3, 8), (3, 16)):
                    print(f"  {lab:52s} {b:2d} {n:3d} {a_bit:9.5f} {gbmm2:7.3f} {xden:8.2f} {xbits_per_dollar:8.2f}")
    # break-even b*N for each design at equal density
    for lab, f, nf2, base in designs:
        a_cell = nf2 * (f * 1e-3) ** 2
        print(f"  break-even b*N for density parity: {lab}: {a_cell / CELL_1B_UM2:.1f}")


# ---------------------------------------------------------------------------------------------
# 4. Ferroelectric 2T-nC
# ---------------------------------------------------------------------------------------------
def section_2tnc():
    hr("4. Ferroelectric 2T-nC stack (one gain-transistor pair, n stacked MFM capacitors)")
    f = 20
    a_2t = 2 * 8 * (f * 1e-3) ** 2 * 1.5     # [ESTIMATE] two 8F2 transistors + 50% routing
    for n in (8, 16, 32, 64, 128):
        a_bit = a_2t / n
        print(f"  n={n:3d}: footprint/bit={a_bit:.5f} um^2 -> {CELL_1B_UM2/a_bit:5.2f}x 1-beta density"
              f" ({ARRAY_EFF/a_bit*1e-3:5.2f} Gb/mm2 at 0.508 eff)")
    pr = 20e-6       # C/cm^2 remanent polarization, HZO [ESTIMATE 15-25]
    d_pillar = 40e-7 # cm (40 nm pillar)
    for t_layer_nm in (20, 40):
        a_cap = math.pi * d_pillar * t_layer_nm * 1e-7   # cylinder wall area, cm^2
        q = 2 * pr * a_cap
        print(f"  MFM cap on 40 nm pillar, {t_layer_nm} nm tall: A={a_cap*1e14:.0f} nm^2, 2Pr*A={q*1e15:.2f} fC"
              f" = {q/Q_E:,.0f} e- (DRAM bit ~{DRAM_CELL_CHARGE_E:,} e-)")
    yrs = 5 * 365.25 * 24 * 3600
    for label, period in (("hot row every tRC=46 ns", 46e-9), ("1 write/us", 1e-6),
                          ("1 write/ms", 1e-3), ("1 write/s", 1.0)):
        print(f"  endurance needed over 5 yr, {label:24s}: {yrs/period:9.2e} cycles")
    print("  Reported: HZO 1Mb 1T1C 1e11 (IEDM 2023); Micron 32Gb NVDRAM 1e15 (press). Destructive read means")
    print("  reads also consume endurance; DRAM-class without wear-levelling needs ~1e15-1e16.")


# ---------------------------------------------------------------------------------------------
# 5. VCMA energy
# ---------------------------------------------------------------------------------------------
def section_vcma():
    hr("5. VCMA-MRAM write energy (capacitive charging of the MTJ) vs DRAM")
    k, t_mgo, d = 9.0, 1.2e-9, 50e-9     # [ESTIMATE] MgO k, thickness, MTJ diameter
    c = EPS0 * k * math.pi * (d / 2) ** 2 / t_mgo
    for v in (0.5, 1.0, 1.5):
        print(f"  MTJ C={c*1e15:.3f} fF at {v} V: device CV^2={c*v*v*1e15:.3f} fJ; with 1-5 fF line ->"
              f" {(c+1e-15)*v*v*1e15:.2f}-{(c+5e-15)*v*v*1e15:.2f} fJ")
    print(f"  Reported: imec 2020 20 fJ @1.1 GHz, >1e10 cycles; Spintec 6 fJ @0.5 ns. DRAM refresh alone"
          f" ~{DRAM_REFRESH_FJ_PER_BIT} fJ/bit per event (A1) -> VCMA is non-volatile AND cheaper per write.")


# ---------------------------------------------------------------------------------------------
# 6. Cryogenic DRAM
# ---------------------------------------------------------------------------------------------
def section_cryo():
    hr("6. 77 K DRAM: refrigeration overhead")
    t_c, t_h = 77.0, 300.0
    cop_carnot = t_c / (t_h - t_c)
    for frac in (0.15, 0.30):
        cop = cop_carnot * frac
        print(f"  COP Carnot={cop_carnot:.3f}; at {frac:.0%} of Carnot COP={cop:.3f} -> {1/cop:5.1f} W wall per W removed")
    rdimm_active, rdimm_refresh = 12.0, 0.75   # [A1] W
    for cold_power_frac in (0.3, 0.5):
        p_cold = rdimm_active * cold_power_frac
        wall = p_cold * (1 + 1 / (cop_carnot * 0.30))
        print(f"  RDIMM 12 W -> {p_cold:.1f} W at 77 K (assume {cold_power_frac:.0%}) -> {wall:5.1f} W at the wall"
              f" vs 12 W warm (refresh share only ~{rdimm_refresh} W)")
    print("  -> Cold DRAM is net-energy-negative unless the cooling is already paid for (quantum / superconducting).")


# ---------------------------------------------------------------------------------------------
# 7. Hybrid bonding for a disaggregated cell wafer
# ---------------------------------------------------------------------------------------------
def section_bonding():
    hr("7. Bonds needed for one bond per bitline segment (cell wafer bonded to foundry periphery wafer)")
    for bl_pitch, cell_pitch, cells in ((40, 40, 128), (80, 120, 128), (80, 120, 256), (64, 64, 64)):
        seg_area_um2 = (bl_pitch * 1e-3) * (cell_pitch * 1e-3 * cells)
        bonds_per_mm2 = 1e6 / seg_area_um2
        pitch_um = math.sqrt(1e6 / bonds_per_mm2)
        print(f"  BL pitch {bl_pitch} nm, cell pitch {cell_pitch} nm, {cells} cells/segment: {bonds_per_mm2/1e6:5.2f} M bonds/mm2"
              f" -> square bond pitch <= {pitch_um:4.2f} um")
    print("  Reported: imec W2W hybrid bonding at 300 nm pitch (ECTC 2025) = 11.1 M bonds/mm2.")
    print("  -> At litho-light oxide-cell pitches (80-120 nm) one bond per 128-256-cell segment needs only ~1-2 um pitch;")
    print("     a vertical-bitline 3D stack needs one bond per vertical BL group, not per tier.")


# ---------------------------------------------------------------------------------------------
# 8. PIM Amdahl check
# ---------------------------------------------------------------------------------------------
def section_pim():
    hr("8. LPDDR5X-PIM: internal bandwidth ratio vs measured speedup")
    bw_ratio = 614 / 76.8     # [REPORTED] Samsung Hot Chips 2026
    measured = 3.01           # [REPORTED] throughput, Llama-3.1-8B
    # Amdahl: speedup = 1/((1-p) + p/bw_ratio) -> solve p
    p = (1 - 1 / measured) / (1 - 1 / bw_ratio)
    print(f"  bandwidth ratio {bw_ratio:.1f}x; measured {measured}x -> implied PIM-accelerable fraction p={p:.2f}")
    print("  -> ~76% of the workload time was bandwidth-bound and offloadable; the remaining serial part caps gains.")


def main():
    section_retention()
    section_read_speed()
    section_density()
    section_2tnc()
    section_vcma()
    section_cryo()
    section_bonding()
    section_pim()


if __name__ == "__main__":
    main()
