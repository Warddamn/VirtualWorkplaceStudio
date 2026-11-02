#!/usr/bin/env python3
"""B3 (Phase B, lens: 3D INTEGRATION & PROCESS INNOVATION) first-principles estimates.

Agent key: B3-3dprocess. Written 2026-11-01. Standard library only; `python3` must exit 0.

Every number printed here is an [ESTIMATE] unless the comment names a source. Judgement
calls are logged in research/assumptions/B3-3dprocess.md. Anchors reused (not re-derived):
  - ram-venture/models/dram_cost_stack.py: 1-beta DDR5 wafer $3,800, 16Gb die 36.5 mm2,
    0.447 Gb/mm2 die-level (teardown), $1.48/GB.
  - phaseA/A1_scaling_limits.md: pillar Cs formula and 1-beta pillar (21 nm, EOT 0.55 nm),
    bitline table (64 cells -> 8 fF, 512 -> 35 fF), sense criterion (50 mV after 15% droop),
    refresh 46 fJ/bit and 12 mW per 16Gb die at 64 ms, retention halves per ~10 C,
    HBM ~3.5 pJ/bit, 3D tier-yield arithmetic.
  - phaseA/A3_research_frontier.md: vertical 2T0C 10F2, array efficiency 0.508,
    tier cost = 12.5% of the base wafer, oxide read-current numbers.
Sections are labelled with the idea-card id (B3-xx) they support.
"""

import math

EPS0 = 8.854e-12
Q_E = 1.602e-19
K_B_EV = 8.617e-5

REF_DENSITY = 0.447          # Gb/mm2 die-level, 1-beta (A1 table 1)
REF_WAFER = 3800.0           # $ per 1-beta wafer (dram_cost_stack.py)
REF_CELL_NM2 = 1070.0        # 1-beta 6F2 cell (A1)
REF_ARRAY_EFF = 0.51         # A1
F_1B = 13.4                  # nm (A1)
WAFER_MM2 = math.pi * 150.0 ** 2
TIER_COST_A3 = 0.125 * REF_WAFER   # $475/tier, A2/A3 convention (each tier ~12.5% of a wafer)
HBM_PJ = 3.5                 # pJ/bit (A1 sec 7-8)
REFRESH_MW_PER_16GB_64MS = 12.0    # A1 sec 3


def hr(t):
    print("\n" + "=" * 96)
    print(t)
    print("=" * 96)


def pillar_cs_fF(d_nm, h_nm, eot_nm):
    """A1 convention: C = 3.9*eps0*pi*d*h/EOT (fF)."""
    return 3.9 * EPS0 * math.pi * d_nm * 1e-9 * h_nm * 1e-9 / (eot_nm * 1e-9) * 1e15


def cs_needed_fF(cbl_fF, vary=1.06, droop=0.15, sig_mV=50.0):
    """A1 sense criterion: (VARY/2 - droop*VARY) * Cs/(Cs+Cbl) >= 50 mV after 15% droop."""
    a = (vary / 2.0 - droop * vary) * 1000.0
    r = sig_mV / a                       # Cs/(Cs+Cbl) >= r
    return r * cbl_fF / (1.0 - r)


def vary_min(cs, cbl, droop=0.15, sig_mV=50.0):
    return sig_mV / 1000.0 / ((0.5 - droop) * cs / (cs + cbl))


def dens(cell_nm2, eff, bits=1, tiers=1):
    return 1e12 / cell_nm2 * eff * bits * tiers / 1e9


def binom_at_most(n, p, k):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def arrhenius(ea_ev, t1_c, t2_c):
    return math.exp(ea_ev / K_B_EV * (1.0 / (t1_c + 273.15) - 1.0 / (t2_c + 273.15)))


# --------------------------------------------------------------------------------------
def b3_01_msb():
    hr("B3-01  Muxed short-bitline (hierarchical) 1T1C with sense amps bonded under the array")
    c_cell = (35.0 - 8.0) / (512 - 64)          # fF per cell on the BL, from A1's 512/64 table
    local = 64 * c_cell + 0.10                  # 64-cell local BL + mux junction
    seg_len_um = 64 * 2 * F_1B / 1000.0         # WL pitch 2F along the BL
    for label, wire_ff_um, bond_ff, sa_ff in [("base", 0.15, 1.0, 1.5), ("pessimistic", 0.25, 2.0, 2.0)]:
        glob = 8 * seg_len_um * wire_ff_um + 8 * 0.05 + bond_ff + sa_ff
        cbl = local + glob
        cs = cs_needed_fF(cbl)
        h = cs / pillar_cs_fF(21, 1, 0.55)
        print(f"  {label:11s}: local BL {local:4.2f} fF + global {glob:4.2f} fF = Cbl_eff {cbl:5.2f} fF ->"
              f" Cs_min {cs:4.2f} fF -> pillar height {h:4.0f} nm (vs 1,300 nm; AR {h/21:4.1f} vs 62)")
    cbl = local + 8 * seg_len_um * 0.15 + 0.4 + 1.0 + 1.5
    print(f"  check vs today: Cs_min at 35 fF = {cs_needed_fF(35):.2f} fF (A1 says 5.4 fF)")
    e_today = 35e-15 * 1.06 ** 2 / 2 * 1e15
    e_stub = cbl * 1e-15 * 1.06 ** 2 / 2 * 1e15
    vmin = vary_min(5.4, cbl)
    e_lowv = cbl * 1e-15 * max(vmin, 0.45) ** 2 / 2 * 1e15
    print(f"  BL CV^2/2 per sensed bit: today {e_today:4.1f} fJ; MSB stub-cap at 1.06 V {e_stub:4.1f} fJ"
          f" ({e_today/e_stub:3.1f}x); MSB keeping 5.4 fF cap, VARY>= {vmin:4.2f} V -> {e_lowv:4.2f} fJ ({e_today/e_lowv:3.0f}x)")
    for m in (8, 16):
        a = m * 64 * REF_CELL_NM2 / 1e6
        print(f"  {m:2d}:1 mux: {a:5.3f} um^2 per bond -> bond pitch {math.sqrt(a):4.2f} um; SA budget (2 nodes/SA)"
              f" {2*a:4.2f} um^2")
    d = REF_DENSITY * 0.70 / REF_ARRAY_EFF
    print(f"  array efficiency 0.51 -> 0.70 (SA/decoders under): {d:4.3f} Gb/mm2 = {d/REF_DENSITY:4.2f}x 1-beta")
    for peri in (1800.0, 3000.0):
        cost = REF_WAFER - 150.0 + peri + 200.0
        print(f"  cost: cell wafer $3,650 + periphery ${peri:,.0f} + bond $200 = ${cost:,.0f} -> $/bit"
              f" {cost/REF_WAFER/(d/REF_DENSITY):4.2f}x 1-beta")


def b3_02_carrier():
    hr("B3-02  Carrier-is-memory: the bonded carrier of a backside-power logic wafer is a DRAM wafer")
    die = 800.0
    for label, d in [("1-beta DRAM, I/O removed (eff 0.60)", REF_DENSITY * 0.60 / 0.51),
                     ("1-beta DRAM as-is", REF_DENSITY)]:
        gb = die * d / 8
        print(f"  {label:38s}: {d:4.3f} Gb/mm2 x {die:.0f} mm2 = {gb:5.1f} GB per accelerator")
    e_bond = 12e-15 * 0.75 ** 2 * 0.5 * 1e12    # pJ/bit: 12 fF pad+wire, 0.75 V, activity 0.5
    e_total = e_bond + 0.1 + 0.18               # + 0.5 mm on-die move + streaming activation (A1)
    print(f"  interface energy: bond hop {e_bond:5.3f} pJ/bit + on-die 0.10 + activation 0.18 = {e_total:4.2f} pJ/bit"
          f" vs HBM {HBM_PJ} ({HBM_PJ/e_total:3.0f}x lower)")
    for tbs in (8, 16):
        bits = tbs * 8e12
        print(f"  at {tbs:2d} TB/s: HBM {bits*HBM_PJ*1e-12:5.0f} W vs bonded {bits*e_total*1e-12:4.0f} W")
    bonds = 1e6 * 0.02 * die
    print(f"  1 um pitch = 1e6 bonds/mm2; 2% as data lanes at 2 Gb/s = {bonds*2e9/8e12:,.0f} TB/s ceiling (array/power bound first)")
    gross = 60
    for yl in (0.5, 0.7):
        per = (REF_WAFER - 120) / gross / yl
        print(f"  memory cost per good accelerator (logic yield {yl:.0%}): ${per:5.0f} -> ${per/52.6:4.2f}/GB")
    gbit = die * REF_DENSITY * 0.60 / 0.51
    for ms, t in ((64, 85), (16, 105)):
        print(f"  refresh at {t} C ({ms} ms): {gbit/16*REFRESH_MW_PER_16GB_64MS*64/ms/1000:4.2f} W for the whole layer")
    wse = WAFER_MM2 * 0.85 * REF_DENSITY * 0.60 / 0.51 / 8 / 1000
    print(f"  wafer-scale version (300 mm memory wafer under a wafer-scale engine, 85% usable): {wse:4.1f} TB")


def b3_03_coolant():
    hr("B3-03  Coolant-backed memory wafer: microchannels etched in the memory wafer's back")
    q = 1000.0 / 8e-4          # W/m2 (1 kW over 8 cm2)
    for h in (5e4, 1e5, 2e5):
        dt_conv = q / h
        dt_si = q * 50e-6 / 148.0
        dt_beol = q * 5e-6 / 3.0
        mem = dt_conv + dt_si + dt_beol
        print(f"  h={h:7.0e} W/m2K: memory {mem:5.1f} K above coolant (conv {dt_conv:4.1f}, Si {dt_si:3.1f},"
              f" BEOL {dt_beol:3.1f}); logic ~{mem + q*10e-6/3.0:4.1f} K")
    for tm in (45, 55, 65):
        gain = 2 ** ((85 - tm) / 10.0)
        print(f"  memory at {tm} C: retention x{gain:4.1f} vs 85 C spec -> refresh {64*gain:6.0f} ms;"
              f" refresh busy 7.6% -> {7.6/gain:4.2f}%")


def b3_04_coax():
    hr("B3-04  Coaxial 4F2 2T0C: storage-node core gates a read-channel shell; write FET stacked above")
    for F in (20, 30, 40, 65):
        d1 = dens(4 * F * F, 0.70)
        d10 = dens(10 * F * F, 0.508)
        print(f"  F={F:2d} nm: 4F2 coax {d1:5.3f} Gb/mm2 per tier-bit (eff 0.70); break-even bxN {REF_DENSITY/d1:4.1f}"
              f" | same eff 0.508: {REF_DENSITY/dens(4*F*F,0.508):4.1f} | A3 10F2: {REF_DENSITY/d10:4.1f}")
    rows = [(40, 2, 8, 0.55), (40, 1, 8, 0.55), (30, 2, 4, 0.70), (20, 1, 2, 0.90)]
    for F, b, n, base in rows:
        d = dens(4 * F * F, 0.70, b, n)
        cost = REF_WAFER * base + n * TIER_COST_A3
        print(f"  F={F} {b}b x {n} tiers: {d:5.2f} Gb/mm2 = {d/REF_DENSITY:4.2f}x; wafer ${cost:,.0f} ->"
              f" bits/$ {d/REF_DENSITY*REF_WAFER/cost:4.2f}x")
    c = pillar_cs_fF(20, 150, 2.0)
    print(f"  C_SN (core 20 nm x 150 nm, EOT 2 nm) = {c:5.3f} fF = {c*1e-15/Q_E:,.0f} e/V")
    for i in (1e-20, 1e-19, 1e-18):
        print(f"    total leakage {i:6.0e} A: retention (200 mV) {c*1e-15*0.2/i:8.0f} s; (50 mV, 2b) {c*1e-15*0.05/i:7.0f} s")
    i_rd = math.pi * 30e-3 * 10.0      # uA: perimeter 30*pi nm, 10 uA/um at L=150 nm
    print(f"  read current ~{i_rd:4.2f} uA -> 100 mV on 9 fF in {9e-15*0.1/(i_rd*1e-6)*1e9:4.2f} ns")
    for cc in (0.005, 0.015):
        print(f"  WWL kickback, Cc={cc} fF, 2.5 V swing: {2.5*cc/(cc+c)*1000:4.0f} mV")


def b3_05_mirror():
    hr("B3-05  Mirror-VCT: 4F2 oxide VCT cells above AND below one shared bitline plane")
    for F in (20.0, 14.7):
        one = dens(4 * F * F, 0.70)
        print(f"  F={F:4.1f} nm: one side {one:4.2f} Gb/mm2; mirrored {2*one:4.2f} Gb/mm2 = {2*one/REF_DENSITY:4.2f}x 1-beta;"
              f" backside overlay budget ~F/4 = {F/4:3.1f} nm")
    for extra in (0.35, 0.45):
        print(f"  if the backside module adds {extra:.0%} to the cell+periphery stack: bits/$ vs one-sided VCT"
              f" {2/(1+extra):4.2f}x")


def b3_06_dopant():
    hr("B3-06  Ge-free dopant-contrast superlattice (Si / Si:B[:C]) for 3D Si DRAM")
    eps_sige = 0.20 * 0.0418
    beta_b = 5.2e-24
    for nb in (1e20, 3e20):
        e = beta_b * nb
        ge_comp = e / 0.0418
        print(f"  B={nb:.0e}: misfit {e*100:5.3f}% vs Si0.8Ge0.2 {eps_sige*100:4.2f}% -> strain energy x{(e/eps_sige)**2:6.4f};"
              f" Ge to null it {ge_comp*100:4.2f}% ({0.20/ge_comp:4.0f}x less Ge)")
    for tc, t in ((650, 3.6e4), (1000, 10)):
        kT = K_B_EV * (tc + 273.15)
        D = 0.76 * math.exp(-3.46 / kT)
        print(f"  B diffusion at {tc} C for {t:.0e} s: sqrt(Dt) = {math.sqrt(D*t)*1e7:4.2f} nm")


def b3_07_graded():
    hr("B3-07  Etch-compensated graded tier stack (uniform lateral recess)")
    for h_um, spread in ((4.0, 0.25),):
        lam = h_um / math.acosh(1 / (1 - spread))
        print(f"  calibrate: {spread:.0%} bottom/top recess-rate drop over {h_um} um -> depletion length {lam:4.2f} um")
        for H in (4.0, 8.0, 12.0):
            ratio = 1 / math.cosh(H / lam)
            print(f"    deck height {H:4.1f} um ({int(H/0.06)} tiers at 60 nm): bottom rate {ratio:4.2f}x top ->"
                  f" grading range needed {1/ratio:4.2f}x")
    L = 600.0
    for s in (0.25, 0.05):
        pitch = L * (1 + s / 2) + 60
        print(f"  recess spread +-{s/2:.1%}: cell pitch along recess {pitch:4.0f} nm; worst-case Cs {1-s/2:4.3f}x nominal")
    print(f"  footprint saving 25%->5% spread: {1-(L*1.025+60)/(L*1.125+60):.1%}")
    print(f"  lateral ALE trim: 20 nm at 0.5 nm/cycle = 40 cycles; full 600 nm = 1,200 cycles (too slow alone)")


def b3_08_decoder():
    hr("B3-08  Vt-coded in-stack tier decoder replaces the staircase")
    for N in (32, 64, 128):
        k = math.ceil(math.log2(N))
        stair = N * 0.5
        dec = 2 * k * 0.2 + 0.3
        for wl_cells in (128, 512):
            line = wl_cells * 0.05
            print(f"  N={N:3d}: staircase {stair:5.1f} um vs decoder {dec:4.1f} um ({stair/dec:4.1f}x);"
                  f" line of {wl_cells} cells ({line:4.1f} um): overhead {stair/(stair+line):4.0%} -> {dec/(dec+line):4.0%}")
    r_gate = 2.0e3
    print(f"  12 series select gates at ~{r_gate/1e3:.0f} kOhm (W~1 um) x 50 fF line = {12*r_gate*50e-15*1e9:3.1f} ns RC")


def b3_09_sandwich():
    hr("B3-09  Smart-Cut c-Si sense layers every 16 oxide tiers (sandwich stack)")
    for mux in (1, 30):
        cbl = 16 * 0.08 + 1.0 * 0.2 + 0.5 + (mux * 0.05 + mux * 0.05 * 0.2 if mux > 1 else 0)
        cs = cs_needed_fF(cbl)
        per_nm = 3.9 * EPS0 * 160e-9 / 0.55e-9 * 1e15 * 1e-9    # fF per nm of lateral length
        print(f"  {mux:2d}:1 mux: vertical BL Cbl {cbl:4.2f} fF -> Cs_min {cs:4.2f} fF -> in-tier cap length"
              f" {cs/per_nm:4.0f} nm (vs A1 base 600 nm)")
    a_tier = 0.050 * 0.200
    d_t = dens(a_tier * 1e6, 0.70)
    print(f"  per-tier footprint 50 x 200 nm -> {d_t:5.3f} Gb/mm2/tier; 64 tiers {64*d_t:4.2f} Gb/mm2 ({64*d_t/REF_DENSITY:3.0f}x)")
    for tier_cost, sa_layer in ((30, 400), (45, 700)):
        cost = 2000 + 64 * tier_cost + 4 * sa_layer
        print(f"  cost: base $2,000 + 64 x ${tier_cost} + 4 SA layers x ${sa_layer} = ${cost:,} ->"
              f" bits/$ {64*d_t/REF_DENSITY*REF_WAFER/cost:4.1f}x (before yield)")
    h_dose = 5e16
    print(f"  Smart-Cut H dose ~{h_dose:.0e} cm^-2 vs MLC donor budget 1.4e11 cm^-2: barrier must stop {1-1.4e11/h_dose:.6%}")


def b3_10_ela():
    hr("B3-10  Sputtered (H-free) Si + excimer-laser single-grain tiers: in-stack CMOS / floating-body cells")
    usable = 0.6
    d_t = dens(10 * 40 * 40, 0.70) * usable
    print(f"  floating-body 10F2 at F=40, grain-usable 60%: {d_t:5.3f} Gb/mm2/tier; parity at {REF_DENSITY/d_t:4.1f} tiers")
    L = math.sqrt(8.6e-7 * 100e-9)
    print(f"  thermal diffusion length in SiO2 for a 100 ns pulse: {L*1e6:4.2f} um -> isolation ~0.5-1 um per tier")
    print(f"  p-FET mobility single-grain Si 121-250 cm2/Vs vs p-oxide ~15 -> drive x{121/15:3.0f}-{250/15:3.0f}")


def b3_11_interposer():
    hr("B3-11  Memory interposer: oxide gain-cell tiers built into a Si interposer")
    for area in (2700.0, 4719.0):
        a = area * 0.65
        lo = a * dens(10 * 65 * 65, 0.508, 1, 8) / 8
        hi = a * dens(4 * 65 * 65, 0.70, 2, 8) / 8
        print(f"  interposer {area:5.0f} mm2 (65% usable): 10F2 1b x 8 -> {lo:5.1f} GB; coax 4F2 2b x 8 -> {hi:5.1f} GB")
    for tier in (200.0, 475.0):
        per = 8 * tier / 16
        print(f"  8 tiers at ${tier:.0f}/tier, 16 interposers/wafer: +${per:4.0f} per interposer")
    print(f"  energy: microbump ~0.05-0.1 + activation 0.18 + on-die 0.05 -> ~0.3 pJ/bit vs HBM {HBM_PJ}")


def b3_12_photonic():
    hr("B3-12  Photonic periphery wafer: DRAM cell wafer bonded to a monolithic photonics-CMOS periphery")
    link = 2.4 + 0.7
    print(f"  link (Celestial AI, HC2025, company): {link:3.1f} pJ/bit + array 0.3 = {link+0.3:3.1f} vs HBM {HBM_PJ}")
    rings = 8 * 16 * 2
    for mw in (2.0, 5.0):
        print(f"  {rings} rings x {mw} mW tuning at 4 Tb/s per die = {rings*mw/1000:4.2f} W = {rings*mw*1e-3/4e12*1e12:4.2f} pJ/bit")
    print("  per-die bandwidth 4 Tb/s = 500 GB/s (vs HBM4 ~2 TB/s shared by 12-16 dies)")


def b3_13_coil():
    hr("B3-13  Coil-stacked HBM (inductive links, wire-bonded power, no TSVs)")
    coil = 50e-6
    n = 2048
    print(f"  {n} coils at {coil*1e6:.0f} um pitch = {n*coil*coil*1e6:4.1f} mm2 (placed over the array in top metal)")
    print(f"  energy: coil 0.7 pJ/bit/hop (Shiba 2022, SRAM) vs TSV ~0.15 pJ/bit/layer (A1) -> energy is WORSE")
    for recov in (0.33, 0.5):
        tax = 3.0
        print(f"  if TSV keep-out + TSV/bump yield are {recov:.0%} of the HBM 3x tax: tax -> {tax-(tax-1)*recov:3.2f}x;"
              f" bits/wafer +{tax/(tax-(tax-1)*recov)-1:.0%}")


def b3_14_sidewall():
    hr("B3-14  Sidewall-wired DRAM cube with adaptive (die-position-corrected) patterning")
    for pitch in (4.0, 8.0):
        print(f"  edge 10 mm at {pitch} um pitch: {10000/pitch:5.0f} wires per edge")
    c = 0.2 * 16 * 50
    print(f"  vertical side wire 16 x 50 um, {c:.0f} fF: {c*1e-15*0.4**2*1e12:5.3f} pJ/bit at 0.4 V swing")
    for e_mm in (0.2, 0.05):
        print(f"  extra on-die route to the edge, 5 mm avg at {e_mm} pJ/bit/mm: +{5*e_mm:4.2f} pJ/bit")
    r = 1.7e-8 * 0.8e-3 / (10e-6 * 200e-6)
    print(f"  plated side power rail 10 um x 200 um x 0.8 mm: {r*1000:4.1f} mOhm")


def b3_15_origami():
    hr("B3-15  Origami membrane stack [SPECULATIVE]")
    for t_um, eps in ((3.0, 0.005), (1.5, 0.005)):
        R = t_um * 1e-6 / (2 * eps)
        fold = math.pi * R * 1000
        print(f"  membrane {t_um} um, strain limit {eps:.1%}: R {R*1e6:4.0f} um, fold {fold:4.2f} mm -> loss per 10 mm layer"
              f" {fold/(10+fold):4.1%}")
    r_layer = 2e-6 / 0.2
    print(f"  16 adhesive layers (2 um, k 0.2): {16*r_layer*1e4:4.2f} K cm2/W (bumpless WOW 0.46, conventional 1.54)")
    print(f"  wires across one 10 mm fold at 1 um pitch x 2 metals: {2*10000:,}")


def b3_16_spares():
    hr("B3-16  Spare tiers + tested tier groups (yield firewall for 64 tiers)")
    for p in (0.01, 0.005, 0.002):
        row = [f"s={s}: {binom_at_most(64+s, p, s):6.4f}" for s in (0, 1, 2, 4)]
        print(f"  per block-tier defect p={p}: block survival " + ", ".join(row))
    blocks = 1000
    for p in (0.01, 0.005):
        for s in (2, 4):
            pb = binom_at_most(64 + s, p, s)
            print(f"    die with {blocks} blocks, p={p}, s={s}: die yield {pb**blocks:6.3f} (overhead {s/64:.1%})")
    yg = 0.99 ** 8
    print(f"  tested groups: 8 groups x 8 tiers at 0.99/tier -> group yield {yg:5.3f}; 7 bonds at 99.5% -> {0.995**7:5.3f}"
          f" vs monolithic 0.99^64 = {0.99**64:5.3f}")


def b3_17_hydrogen():
    hr("B3-17  Hydrogen-lean batch-furnace mold for oxide 3D stacks")
    cox = 3.9 * EPS0 / 3e-9 * 1e-4          # F/cm2 at EOT 3 nm
    n_allow = 0.020 * cox / Q_E
    print(f"  C_ox (EOT 3 nm) {cox*1e6:4.2f} uF/cm2 -> 20 mV MLC budget = {n_allow:5.2e} donors/cm2")
    for lab, dens_at, hfrac in (("PECVD SiN 20% H", 8.0e22, 0.20), ("LPCVD SiN 4% H", 9.3e22, 0.04),
                                ("PECVD TEOS SiO2 3% H", 6.6e22, 0.03)):
        h = dens_at * hfrac * 30e-7
        print(f"  30 nm {lab:22s}: {h:5.2e} H/cm2 -> tolerable fraction reaching channel {n_allow/h:7.1e}")
    sin_min = 64 * 30 / 2.5
    ox_min = 64 * 30 / 8.0
    sw = 64 * 2 * 5
    tot = sin_min + ox_min + sw
    print(f"  batch furnace, 64 pairs, 150 wafers: {tot/60:4.1f} h per batch -> {tot/150:4.1f} min per wafer")


def b3_18_bonus():
    hr("B3-18  BEOL bonus tiers on a conventional DRAM die")
    die = 36.5
    base = 16.0 * 0.85
    opts = [("A3 10F2 vertical 2T0C, 1b x 8", dens(10 * 1600, 0.508, 1, 8)),
            ("coax 4F2 (B3-04), 1b x 8", dens(4 * 1600, 0.70, 1, 8)),
            ("coax 4F2 (B3-04), 2b x 8", dens(4 * 1600, 0.70, 2, 8))]
    for lab, d in opts:
        tot = base + d * die
        for tier in (100.0, 475.0):
            cost = REF_WAFER + 8 * tier
            print(f"  {lab:32s} tier ${tier:3.0f}: {tot:5.1f} Gb/die ({tot/16:4.2f}x), bits/$ {tot/16*REF_WAFER/cost:4.2f}x")


def b3_19_wow():
    hr("B3-19  Bumpless ultra-thin wafer-on-wafer DRAM with spare layers")
    a_hbm = (6 + 2 * 5) ** 2
    a_thin = (1.5 + 2 * 1) ** 2
    print(f"  TSV+keep-out area: HBM-class {a_hbm} um2 vs thin-wafer {a_thin:.1f} um2 ({a_hbm/a_thin:3.0f}x less)")
    for n in (16, 64):
        print(f"  {n} layers x 10 um = {n*10} um stack (vs JEDEC 775 um package)")
    for y in (0.90, 0.95, 0.98):
        r16 = binom_at_most(18, 1 - y, 2)
        r64 = binom_at_most(72, 1 - y, 8)
        print(f"  die-site yield {y}: >=16 of 18 good {r16:5.3f}; >=64 of 72 good {r64:5.3f}; no spares 16 {y**16:5.3f}")


def b3_20_cold():
    hr("B3-20  Room-temperature surface-activated hybrid bonding for oxide-cell stacks")
    for g in (4, 8):
        print(f"  {g} sequential bonds x 2 h at 350 C: first layer sees {2*g} h at 350 C; RT-SAB: 0 h")
    print(f"  IGZO recovery/stress kinetics ~0.58-0.72 eV: 350 C vs 85 C acceleration "
          f"{arrhenius(0.58, 85, 350):6.0f}-{arrhenius(0.72, 85, 350):6.0f}x -> 16 h at 350 C ~ "
          f"{16*arrhenius(0.58,85,350)/8760:4.1f}-{16*arrhenius(0.72,85,350)/8760:5.1f} years at 85 C")


def b3_21_grow():
    hr("B3-21  Grow-the-hole: bottom-up dual area-selective deposition instead of a HAR etch [SPECULATIVE]")
    for tiers in (64, 128):
        h = tiers * 0.06
        print(f"  {tiers} tiers x 60 nm = {h:4.2f} um; 100 nm holes -> AR {h/0.1:4.0f} with zero plasma etch")
    print("  selective W window ~100 nm per cycle (Saraswat 1984 via patent) vs 30 nm increment per layer -> 3x margin")
    for d in (0.1, 0.01):
        print(f"  stray W nuclei {d}/cm2 per layer x 128 layers -> {d*128:5.2f} shorts/cm2 before etch-back")


def b3_22_seqperi():
    hr("B3-22  Sequential periphery-over-cell for Si DRAM (Smart-Cut c-Si + 400 C CMOS on the finished array)")
    for cells in (64, 128):
        cbl = {64: 8.0, 128: 12.0}[cells] - 2.0
        cs = cs_needed_fF(cbl)
        h = cs / pillar_cs_fF(21, 1, 0.55)
        sa = 2 * cells * REF_CELL_NM2 / 1e6
        print(f"  {cells} cells/BL, litho via (no bond pad, -2 fF): Cbl {cbl:4.1f} fF -> Cs {cs:4.2f} fF ->"
              f" cap {h:4.0f} nm; SA area budget {sa:4.3f} um^2 (open BL, 2 segments)")
    print("  via pitch: litho-aligned through ~0.5-1 um of transferred layer, ~100-200 nm vias, overlay ~5-10 nm"
          " (vs hybrid bond >=300-400 nm pitch, ~50-100 nm overlay)")


def main():
    for f in (b3_01_msb, b3_02_carrier, b3_03_coolant, b3_04_coax, b3_05_mirror, b3_06_dopant, b3_07_graded,
              b3_08_decoder, b3_09_sandwich, b3_10_ela, b3_11_interposer, b3_12_photonic, b3_13_coil,
              b3_14_sidewall, b3_15_origami, b3_16_spares, b3_17_hydrogen, b3_18_bonus, b3_19_wow,
              b3_20_cold, b3_21_grow, b3_22_seqperi):
        f()
    hr("Rejected-idea arithmetic")
    print(f"  anneal-reset of IGZO drift: 0.58 eV -> 85->250 C x{arrhenius(0.58,85,250):4.0f}; 85->150 C x{arrhenius(0.58,85,150):3.0f}")
    r_ox = 2e-6 / (1.4 * 2.5e-9)
    print(f"  block heater (50x50 um on 2 um SiO2): R {r_ox:4.0f} K/W -> {250/r_ox:4.2f} W per block for 250 K")
    c = 3.9 * 20 / 3.9 * EPS0 * (0.3e-6) ** 2 / 5e-9 * 1e15
    print(f"  bond-interface capacitor 0.3 x 0.3 um, 5 nm HfO2: {c:3.1f} fF but cell >= bond pitch^2 = 0.09 um2 (84x 1-beta)")


if __name__ == "__main__":
    main()
