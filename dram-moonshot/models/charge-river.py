#!/usr/bin/env python3
"""
charge-river.py -- first-principles model for the CHARGE-RIVER dossier (dram-moonshot, rank 7).

Owner: dos-charge-river. Written 2026-11-02. Pure standard library. Run from dram-moonshot/:
    python3 models/charge-river.py
Writes research/stage3/charge-river_model_output.md and prints the same text.

CHARGE-RIVER = vertical oxide CCD strings (no transistor or capacitor per bit) in a 3D-NAND-like
plate stack, read at BOTH ends (two 32-stage segments per hole), with fat zero, a buried oxide
heterochannel, decision-feedback (DFE) correction of deferred charge, and a drum-style placement
compiler that schedules LLM weight/KV traffic so packets arrive just in time.

Sections
  1. Geometry, packet size, signal and noise (electrons, mV)
  2. Density (Gb/mm^2) vs 1-beta DDR5
  3. Reliability target: decisions per second x ECC -> required raw BER per segment read
  4. CTE -> BER (binomial partition noise + deferred-charge eye, with/without DFE) -> minimum CTE
  5. Trap kinetics: what imec's 6.25 MHz point predicts at a 50 MHz stage clock, 25 and 85 C
  6. KEY-UNKNOWN SENSITIVITY: CTE -> allowed segment length -> bits/hole -> density and $/GB
  7. Latency and schedulability (lead-time model of LLM decode traffic)
  8. Bandwidth and energy per bit; scrub ("refresh") power vs DDR5
  9. Retention and endurance budgets
 10. Plate RC (clock distribution)
 11. Cost per bit vs $1.48/GB DDR5 (and NAND price cross-check)
 12. GO / NO-GO
 13. Seed budget;  14. RED-TEAM REVISIONS summary
Every input carries a source URL / in-study file, or "ESTIMATE: basis".

RED-TEAM REVISIONS (2026-11-02): see the RT_REVISIONS block after INPUTS. Key changes: segments are injected at the
bottom and sensed at the top (no return path existed); 2-row clock strips with replacement-metal slits; staircase,
spares, joint-tier and per-plate cost added; RTN tail (4b), buried-channel electrostatics (5a), gap barriers (5b),
regeneration topology (4c), like-for-like energy (8). New sections are marked RED-TEAM.
"""

import math
import os

Q_E = 1.602176634e-19      # C
K_B_EV = 8.617333e-5       # eV/K
EPS0 = 8.8541878128e-12    # F/m

IMEC_IEDM24 = "https://imec-publications.be/handle/20.500.12860/59420"
IMEC_IMW26 = ("https://www.eejournal.com/industry_news/imec-demonstrates-the-first-3d-implementation-"
              "of-a-charge-coupled-device-for-ai-memory-applications/")
LSST_DFE = ("https://spiedigitallibrary.org/journals/Journal-of-Astronomical-Telescopes-Instruments-and-Systems/"
            "volume-7/issue-04/048002/Characterization-and-correction-of-serial-deferred-charge-in-LSST-camera/"
            "10.1117/1.JATIS.7.4.048002.full")
OXIDE_TRANSIENT = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5605542/"
HETERO_REVIEW = "https://scholarx.skku.edu/item/fde13622-0afc-4041-b0c9-2bc148ffea51"

# =============================================================================================
# INPUTS  (value, source URL / in-study file, or "ESTIMATE: basis")
# =============================================================================================
INPUTS = {
    # ---- reference points --------------------------------------------------------------------
    "d1b_gb_mm2": (0.447, "REPORTED: research/phaseA/A1_scaling_limits.md (Micron D1b 16Gb, 35.83 mm2 teardown via ram-venture cost_stack s3.1)"),
    "ddr5_usd_gb": (1.48, "ram-venture/models/dram_cost_stack.py (1-beta wafer $3.8k -> $1.48/GB)"),
    "wafer_1b_usd": (3800.0, "ram-venture/models/dram_cost_stack.py wafer_cost_1beta_usd"),
    "nand_tlc_usd_gb": (0.09, "ram-venture/models/device_cost_compare.py 'NAND TLC 2026 PRICE' row (price, not cost)"),
    "nand_bits_per_hole": (600, "ESTIMATE: ~200-layer TLC NAND = 200 cells x 3 b per channel hole [training knowledge]"),
    "hbm3_pj_bit": (3.44, "research/phaseA/A1_scaling_limits.md (RPU https://arxiv.org/pdf/2602.18568)"),
    "ddr5_refresh_fj_bit": (46.0, "research/phaseA/A1_scaling_limits.md / models/dram_cell_physics.py refresh energy"),
    "ddr5_tref_s": (0.064, "JEDEC 64 ms (A1 INPUTS t_ref_s)"),
    # ---- imec prior art (the only oxide CCD data that exists) --------------------------------
    "imec_cte": (0.98, IMEC_IEDM24 + " (CTE >98%; per-transfer vs end-to-end NOT stated in snippet)"),
    "imec_clock_hz": (6.25e6, IMEC_IEDM24 + " (>6.25 MHz transfer speed)"),
    "imec_phases": (4, IMEC_IEDM24 + " (planar 4-phase)"),
    "imec_bits": (142, IMEC_IEDM24 + " (142-bit register)"),
    "imec_retention_s": (200.0, IMEC_IEDM24 + " (>200 s)"),
    "imec_endurance": (1e10, IMEC_IEDM24 + " (>1e10 cycles, no degradation)"),
    "imec_3d_clock_hz": (4e6, IMEC_IMW26 + " (3-word-line vertical IGZO CCD, >4 MHz, 'a few thousand' e-/packet)"),
    # ---- CHARGE-RIVER geometry ---------------------------------------------------------------
    "n_plates": (200, "ESTIMATE: concept spec; 3D NAND production stacks exceed 200 word-line layers [training knowledge]"),
    "plate_pitch_nm": (40.0, "ESTIMATE: concept spec = 25 nm W plate + 15 nm SiO2; 3D NAND tier pitch ~40-50 nm [training knowledge]"),
    "plate_thk_nm": (25.0, "ESTIMATE: gate length per plate (see plate_pitch_nm)"),
    "plate_iso_nm": (15.0, "ESTIMATE: inter-plate SiO2 (see plate_pitch_nm)"),
    "phases": (3, "ESTIMATE: 3-phase clocking, 3 plates per stored bit (concept spec)"),
    "segments": (2, "ESTIMATE: sense node at BOTH ends of each hole (bonded CMOS below + top metal), so each segment is <=32 stages (chief's spec)"),
    "overhead_plates": (6, "ESTIMATE: input gate, output gate, reset/transfer plates at the two ends"),
    "hole_cell_um2": (0.02, "ESTIMATE: concept spec, ~141 nm hole pitch (3D NAND-class)"),
    "hole_d_nm": (100.0, "ESTIMATE: 3D NAND-class channel hole at ~141 nm pitch"),
    "diel_phys_nm": (6.0, "ESTIMATE: gate dielectric physical thickness (SiO2/Al2O3)"),
    "eot_nm": (5.0, "ESTIMATE: gate dielectric EOT; thick enough for ~3 V clocks without charge trapping"),
    "slit_nm": (60.0, "ESTIMATE: isolation slit between row clock groups (plates are not replaced through it)"),
    "holes_per_row": (1, "ESTIMATE: one-hole-wide clock group, each hole on its own column line (critic: per-row slits)"),
    "periph_eff": (0.75, "ESTIMATE: column SAs/regenerators, clock drivers, straps; CMOS bonded under the array"),
    # ---- charge, signal, noise ---------------------------------------------------------------
    "dv_well": (1.5, "ESTIMATE: storage-barrier potential difference that holds the packet"),
    "signal_fill": (0.70, "ESTIMATE: operate at 70% of full well"),
    "fat_zero_frac": (0.15, "ESTIMATE: fat zero = 15% of signal (1970s surface-channel CCD practice [training knowledge])"),
    "c_fd_fF": (0.30, "ESTIMATE: floating diffusion + oxide source-follower gate at a 141 nm hole top"),
    "sigma_read_e": (8.0, "ESTIMATE: 3 mV rms post-CDS oxide SF at 0.3 fF (5.6 e-) + coupling 4 e- + residual offset 2 e- (PIXEL-STACK budget ~4 mV rms)"),
    "sigma_fz_e": (3.0, "ESTIMATE: fill-and-spill fat-zero injection noise"),
    "k_ws": (1.5, "ESTIMATE: worst-string multiplier on deferral (Poisson trap count + process spread over ~1e8 strings)"),
    "kappa": (0.10, "ESTIMATE: DFE residual = 10% of deferred charge; basis: LSST shows deferred charge is largely modelable " + LSST_DFE),
    "dfe_on": (True, "design choice (concept)"),
    # ---- reliability target ------------------------------------------------------------------
    "die_gbit": (16.0, "ESTIMATE: compare at a 16 Gb die (DDR5 reference die)"),
    "laps_per_s": (30.0, "ESTIMATE: decode 20-50 tok/s per user; each weight/KV bit read once per decode step"),
    "t_scrub_s": (20.0, "ESTIMATE: imec >200 s retention / 10x margin (" + IMEC_IEDM24 + ")"),
    "ecc_data_bits": (512, "ESTIMATE: BCH codeword over 512 data bits read from 512 parallel column SAs"),
    "ecc_t": (2, "ESTIMATE: BCH t=2 (20 parity bits, 3.9%)"),
    "ecc_parity_bits": (20, "ESTIMATE: t x ceil(log2(532)) = 2 x 10"),
    "fit_target": (10.0, "ESTIMATE: uncorrectable errors per 1e9 device-hours per die (DRAM-class)"),
    "continuous_laps_per_s": (1.5625e6, "derived: 50 MHz / 32 stages if strings circulated continuously (the 'refresh by circulation' framing)"),
    # ---- clocking / latency -------------------------------------------------------------------
    "f_stage_hz": (50e6, "concept go spec: 50 MHz STAGE clock = 150 M transfers/s (research/stage3/FINAL_CONCEPTS.md arbitration #5)"),
    "lap_stages": (32, "concept go spec (regenerate every <=32 stages)"),
    "t_hit_ns": (15.0, "ESTIMATE: SRAM front buffer + controller latency for a scheduled (pre-staged) access"),
    "l_avg_ns": (40.0, "concept target: ~40 ns average effective latency"),
    # ---- trap kinetics (frequency / temperature transfer of imec's point) ---------------------
    "sigma_cap_cm2": (1e-15, "ESTIMATE: neutral acceptor-like trap capture cross-section (SRH; " + OXIDE_TRANSIENT + " shows us-scale transients)"),
    "m_eff": (0.30, "ESTIMATE: a-IGZO electron effective mass ~0.3 m0 [training knowledge]"),
    "nc_cm3": (5e18, "ESTIMATE: a-IGZO conduction-band effective DOS ~5e18 cm^-3 [training knowledge]"),
    "f_it": (0.6, "ESTIMATE: share of imec surface-channel loss from gate-dielectric interface traps"),
    "eta_buried": (0.9, "ESTIMATE: share of interface-trap loss removed by a buried heterochannel (band offset; " + HETERO_REVIEW + ")"),
    "eta_fz": (0.4, "ESTIMATE: residual loss with fat zero (traps below the fat-zero quasi-Fermi level stay full)"),
    # ---- energy -------------------------------------------------------------------------------
    "v_clk": (3.0, "ESTIMATE: CCD clock swing for an accumulation-mode oxide channel"),
    "eta_rec": (0.5, "ESTIMATE: resonant/charge-recycling clock drivers recover 50% of CV^2"),
    "rows_per_col": (512, "ESTIMATE: holes sharing one column line"),
    "c_col_per_hole_fF": (0.08, "ESTIMATE: column-line capacitance per hole at 141 nm pitch"),
    "c_col_fixed_fF": (10.0, "ESTIMATE: SA input + via"),
    "v_col_swing": (0.15, "ESTIMATE: source-follower column swing"),
    "vdd": (1.0, "ESTIMATE: periphery supply"),
    "e_sa_fj": (10.0, "ESTIMATE: SA latch + regenerated-packet re-injection"),
    "e_sf_fj": (5.0, "ESTIMATE: 1 uA SF bias for 5 ns at 1 V"),
    "e_dfe_fj": (5.0, "ESTIMATE: DFE subtract/compare per bit in 28-40 nm CMOS"),
    "rho_w_ohm_m": (15e-8, "ESTIMATE: thin-film W resistivity ~15 uOhm.cm"),
    # ---- LLM workload (dense 70B-class decode) ------------------------------------------------
    "params": (70e9, "ESTIMATE: Llama-3-70B-class model [training knowledge]"),
    "bytes_per_param": (1.0, "ESTIMATE: FP8 weights"),
    "kv_bytes_per_token": (80 * 8 * 128 * 2 * 1, "ESTIMATE: 80 layers x 8 KV heads x 128 dim x (K,V) x 1 B (GQA, FP8) [training knowledge]"),
    "batch": (32, "ESTIMATE: serving batch"),
    "context": (8192, "ESTIMATE: tokens of context per sequence"),
    "random_share_dense": (0.005, "ESTIMATE: unpredictable bytes in dense decode (batch churn, page tables, sampling)"),
    "random_share_moe": (0.02, "ESTIMATE: unpredictable bytes with MoE + sparse attention"),
    "expert_share_moe": (0.8, "ESTIMATE: share of weight bytes that are routed experts"),
    "expert_lead_med_us": (10.0, "ESTIMATE: router decision -> expert matmul lead time (one layer of decode compute)"),
    "sparse_kv_share": (0.5, "ESTIMATE: share of KV reads chosen by top-k / sparse attention"),
    "sparse_kv_lead_med_us": (3.0, "ESTIMATE: score computation -> KV gather lead time"),
    "lead_sigma_ln": (1.0, "ESTIMATE: lognormal spread of lead times"),
    # ---- wafer cost ---------------------------------------------------------------------------
    "array_base_usd": (1200.0, "ESTIMATE: hole etch, ALD dielectric + oxide channel, top 2T readout tier, 3-4 metals"),
    "per_plate_usd": (10.0, "ESTIMATE: W/SiO2 pair deposition share incl. tool depreciation (no staircase: 3-6 clock contacts)"),
    "cmos_wafer_usd": (1800.0, "ESTIMATE: 28-40 nm-class periphery wafer (SAs, DFE, clock drivers)"),
    "bond_usd": (300.0, "ESTIMATE: wafer-to-wafer hybrid bonding"),
    "yield_rel": (0.8, "ESTIMATE: die yield relative to mature 1-beta (new 3D stack, bonded)"),
}

# =============================================================================================
# RED-TEAM REVISIONS (2026-11-02, owner response to research/redteam/rt_{DEV,PROC,CIRC,IND}.json;
# responses in research/redteam/responses_charge-river.json). Objections are answered, never deleted.
# Format: key, old -> new, objection id(s), reason.  New keys have old = None.
# =============================================================================================
RT_REVISIONS = [
    ("holes_per_row", 1, 2, "RT-PROC-charge-river-01/-02, RT-CIRC-charge-river-01",
     "2-row clock strips with NAND-style staggered holes and column lines at half the hole pitch (SADP): each hole of a strip "
     "has its own column line, so both rows are read at once (no extra cycling) and slits are amortised over 2 rows"),
    ("slit_nm", 60.0, 100.0, "RT-PROC-charge-river-01",
     "gate-first 5 um W stack bows a 300 mm wafer ~3 mm (Stoney) and a 60 nm slit in metal is AR ~130; adopt NAND's ONON + "
     "replacement-W flow (slits >=100 nm), channel-LAST so WF6/H2 never touches the oxide channel"),
    ("per_plate_usd", 10.0, 25.0, "RT-PROC-charge-river-04",
     "NAND per-layer economics ($20-38 per ONON pair, rt-PROC from Choe/TechInsights 10-15% gain 64->96 layers); range $12-35 carried"),
    ("array_base_usd", 1200.0, 1500.0, "RT-CIRC-charge-river-01",
     "top FD/RST/SF/SEL oxide-TFT tier (one set per 2 holes) and bottom per-column injection lines now priced"),
    ("c_fd_fF", 0.30, 0.40, "RT-CIRC-charge-river-01, RT-PROC-charge-river-03",
     "floating diffusion shared by 2 holes on one column line (adjacent strips, never read together): 2 contacts + 0.4 um "
     "strip + bootstrapped SF gate + RST overlap; I-12302-style local strip with a local gain FET, column line clamped"),
    ("sigma_read_e", 8.0, 10.0, "RT-CIRC-charge-river-01, RT-PROC-charge-river-03",
     "3 mV rms at 0.40 fF = 7.5 e- + coupling 4 e- + offset 2 e- = 8.7 e-, rounded up; Gaussian part only (RTN tail is now "
     "a separate term, section 4b)"),
    ("eta_buried", 0.9, 0.5, "RT-DEV-charge-river-01",
     "a 4.5e12 cm^-2 packet consumes most of a 0.3 eV offset (E_F +36 meV, ~0.17 V across a 2.5 nm cap): interface-loss "
     "removal cut to 50% until a ->=0.5 eV offset is measured (section 5a)"),
    ("eta_rec", 0.5, 0.33, "RT-CIRC-charge-river-03",
     "no on-chip LC at 50 MHz (uH inductors); 3-phase charge sharing / 3-step stepwise charging recovers ~1/3 realistically"),
    ("topology", None, "joint", "RT-CIRC-charge-river-02, RT-PROC-charge-river-03",
     "a straight hole has no return path: every segment now injects at its BOTTOM (fill-and-spill from a per-column line, no "
     "per-hole TFT) and is sensed at its TOP; decisions return through the CMOS. 'joint' = two 100-plate decks with a "
     "[SPECULATIVE] regenerator tier at the deck joint (keeps 2 x 32 stages, 98 transfers); fallback 'oneway' = one 64-stage "
     "string, 194 transfers, no new tier"),
    ("joint_tier_usd", None, 500.0, "RT-CIRC-charge-river-02",
     "ESTIMATE: deck-joint tier = oxide-TFT sense set for the lower deck + injection nodes for the upper deck + 2 line levels + TAV landings"),
    ("joint_tav_eff", None, 0.96, "RT-CIRC-charge-river-02",
     "ESTIMATE: area for through-array vias carrying joint-tier column/injection lines down to the CMOS (NAND bit-line TAV class)"),
    ("stair_step_um", None, 0.30, "RT-PROC-charge-river-02",
     "every buried plate needs its own contact step: ~0.3 um per step (rt-PROC)"),
    ("strip_len_um", None, 150.0, "RT-PROC-charge-river-02",
     "ESTIMATE: driven strip length per staircase; plate RC allows ~100-200 um at a 50 MHz stage clock (section 10)"),
    ("spare_frac", None, 0.03, "RT-DEV-charge-river-05, RT-CIRC-charge-river-04, RT-DEV-charge-river-02",
     "ESTIMATE: spare strings (screened at k_ws x median, NAND bad-block style) ~2% + spare sense nodes (RTN screen) ~1%"),
    ("rtn_eta_mV", None, 2.8, "RT-CIRC-charge-river-04, RT-DEV-charge-river-02",
     "mean exponential RTN step of a ~0.01 um^2 oxide SF; reviewers' range 1.4-4.2 mV (q/(Cox W L))"),
    ("rtn_p_fast", None, 0.20, "RT-DEV-charge-river-02", "share of SFs carrying a trap with tau near the 2-5 ns CDS interval (rt-DEV)"),
    ("rtn_p_switch", None, 0.25, "RT-DEV-charge-river-02", "ESTIMATE: probability such a trap switches between the two CDS samples"),
    ("io_pj_bit", None, 1.0, "RT-CIRC-charge-river-03",
     "ESTIMATE: HBM-class PHY + TSV/interposer I/O energy, added so the comparison with HBM3 3.44 pJ/bit is like for like"),
    ("dEc_eV", None, 0.30, "RT-DEV-charge-river-01",
     "dossier's original core/cap offset spec; measured IGZO/beta-Ga2O3 0.71+-0.1 eV (NYCU XPS), high-In IGZO/IGZO ~0.4 eV (search snippets)"),
    ("t_cap_nm", None, 2.5, "RT-DEV-charge-river-01", "ESTIMATE: cap between core and gate dielectric (rt-DEV: 2-3 nm)"),
    ("eps_cap", None, 12.0, "RT-DEV-charge-river-01", "ESTIMATE: relative permittivity of an amorphous oxide cap"),
    ("e0_sub_eV", None, 0.05, "RT-DEV-charge-river-01", "ESTIMATE: ground-subband energy of a ~5 nm core under the packet's field"),
]
for _k, _old, _new, _ids, _why in RT_REVISIONS:
    _src = INPUTS[_k][1] + " | " if _k in INPUTS else ""
    INPUTS[_k] = (_new, _src + "RED-TEAM: %s -> %s (%s): %s" % (_old, _new, _ids, _why))


def V(key):
    return INPUTS[key][0]


OUT = []


def p(line=""):
    OUT.append(line)


def table(header, rows):
    p("| " + " | ".join(header) + " |")
    p("|" + "|".join(["---"] * len(header)) + "|")
    for r in rows:
        p("| " + " | ".join(str(x) for x in r) + " |")
    p()


def qfunc(x):
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def qinv(pv):
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if qfunc(mid) > pv:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# =============================================================================================
# 1. Geometry, packet, signal, noise
# =============================================================================================
def packet():
    d_ch = (V("hole_d_nm") - 2 * V("diel_phys_nm")) * 1e-9
    L = V("plate_thk_nm") * 1e-9
    cox = 3.9 * EPS0 / (V("eot_nm") * 1e-9)            # F/m^2
    c_gate = cox * math.pi * d_ch * L                     # F
    full_well = c_gate * V("dv_well") / Q_E
    n_s = V("signal_fill") * full_well
    n_fz = V("fat_zero_frac") * n_s
    cg_uv = Q_E / (V("c_fd_fF") * 1e-15) * 1e6            # uV per electron
    n_sheet = cox * V("dv_well") * V("signal_fill") / Q_E / 1e4   # cm^-2
    return dict(d_ch_nm=d_ch * 1e9, cox=cox, c_gate_fF=c_gate * 1e15, full_well=full_well,
                n_s=n_s, n_fz=n_fz, cg_uv=cg_uv, sig_mV=n_s * cg_uv / 1000,
                noise_mV=V("sigma_read_e") * cg_uv / 1000, n_sheet=n_sheet)


# =============================================================================================
# 2. Density
# =============================================================================================
def stages_from_plates(n_plates):
    return int((n_plates - V("overhead_plates")) // (V("segments") * V("phases")))


def plates_for_stages(stages):
    return V("segments") * V("phases") * stages + V("overhead_plates")


def array_eff():
    pitch = math.sqrt(V("hole_cell_um2")) * 1000.0          # nm
    k = V("holes_per_row")
    slit_eff = k * pitch / (k * pitch + V("slit_nm"))
    return slit_eff, slit_eff * V("periph_eff"), pitch


def ecc_rate():
    return V("ecc_data_bits") / (V("ecc_data_bits") + V("ecc_parity_bits"))


def stair_eff(n_plates, strip_um=None, step_um=None):
    # RED-TEAM (RT-PROC-charge-river-02): every buried plate needs a contact step at each driven strip end
    strip_um = V("strip_len_um") if strip_um is None else strip_um
    step_um = V("stair_step_um") if step_um is None else step_um
    s = n_plates * step_um
    return strip_um / (strip_um + s)


def topo_eff(topology=None):
    topology = V("topology") if topology is None else topology
    return V("joint_tav_eff") if topology == "joint" else 1.0


def density_gb_mm2(bits_per_hole, n_plates=None, topology=None, stair=None):
    # RED-TEAM: x staircase efficiency x (1 - spares) x joint-tier TAV efficiency (was slit x periphery x ECC only)
    n_plates = V("n_plates") if n_plates is None else n_plates
    _, eff, _ = array_eff()
    holes_mm2 = 1e6 / V("hole_cell_um2")
    st = stair_eff(n_plates) if stair is None else stair
    return bits_per_hole * holes_mm2 * eff * st * (1 - V("spare_frac")) * topo_eff(topology) * ecc_rate() / 1e9


def density_original(bits_per_hole):
    # the pre-red-team formula, kept for the old -> new comparison (slit 60 nm, 1-row strips)
    pitch = math.sqrt(V("hole_cell_um2")) * 1000.0
    slit_eff = pitch / (pitch + 60.0)
    return bits_per_hole * 1e6 / V("hole_cell_um2") * slit_eff * V("periph_eff") * ecc_rate() / 1e9


# =============================================================================================
# 3. Reliability target
# =============================================================================================
def p_required(decisions_per_bit_s, t=None, n_data=None, parity=None):
    t = V("ecc_t") if t is None else t
    n_data = V("ecc_data_bits") if n_data is None else n_data
    parity = V("ecc_parity_bits") if parity is None else parity
    n = n_data + parity
    codewords = V("die_gbit") * 1e9 / n_data
    events_s = codewords * decisions_per_bit_s
    allowed = V("fit_target") / (1e9 * 3600.0) / events_s
    return (allowed / math.comb(n, t + 1)) ** (1.0 / (t + 1))


# =============================================================================================
# 4. CTE -> BER
# =============================================================================================
def ber_segment(cte, n_t, n_s, dfe=True, kappa=None, k_ws=None, sig_r=None):
    kappa = V("kappa") if kappa is None else kappa
    k_ws = V("k_ws") if k_ws is None else k_ws
    sig_r = V("sigma_read_e") if sig_r is None else sig_r
    eps = min(1.0, k_ws * (1.0 - cte))
    h0 = (1.0 - eps) ** n_t
    tail = (1.0 - h0) * n_s                  # deferred charge a '0' collects after a long run of '1's
    base = sig_r ** 2 + V("sigma_fz_e") ** 2
    part = n_s * h0 * (1.0 - h0)             # binomial partition noise of the '1' packet
    if dfe:
        # history-aware threshold; worst history = all ones (largest tail, Poisson noise on both levels)
        sep = h0 * n_s - 2.0 * kappa * tail
        s1 = math.sqrt(base + part + tail)
        s0 = math.sqrt(base + tail)
    else:
        # fixed threshold; worst '1' follows zeros, worst '0' follows ones
        sep = h0 * n_s - tail
        s1 = math.sqrt(base + part)
        s0 = math.sqrt(base + tail)
    if sep <= 0:
        return 0.5, h0
    return qfunc(sep / (s0 + s1)), h0


def cte_min(n_t, n_s, p_req, dfe=True, **kw):
    lo, hi = 0.80, 1.0 - 1e-9
    if ber_segment(hi, n_t, n_s, dfe, **kw)[0] > p_req:
        return None
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if ber_segment(mid, n_t, n_s, dfe, **kw)[0] <= p_req:
            hi = mid
        else:
            lo = mid
    return hi


# ---- RED-TEAM (RT-CIRC-charge-river-04, RT-DEV-charge-river-02): RTN tail of the oxide source followers ----
def eye_parts(cte, n_t, n_s, k_ws=None, kappa=None, sig_r=None):
    kappa = V("kappa") if kappa is None else kappa
    k_ws = V("k_ws") if k_ws is None else k_ws
    sig_r = V("sigma_read_e") if sig_r is None else sig_r
    eps = min(1.0, k_ws * (1.0 - cte))
    h0 = (1.0 - eps) ** n_t
    tail = (1.0 - h0) * n_s
    base = sig_r ** 2 + V("sigma_fz_e") ** 2
    sep = h0 * n_s - 2.0 * kappa * tail
    s1 = math.sqrt(base + n_s * h0 * (1.0 - h0) + tail)
    s0 = math.sqrt(base + tail)
    return sep, s0, s1


def ber_rtn(cte, n_t, n_s, eta_e, screen_e=None, p_fast=None, p_sw=None, **kw):
    """Die-average BER with DFE when a share p_fast of sense nodes carries one fast trap whose step A ~ Exp(eta_e)
    switches between the CDS samples with probability p_sw. Nodes with A > screen_e are spared (mapped out)."""
    p_fast = V("rtn_p_fast") if p_fast is None else p_fast
    p_sw = V("rtn_p_switch") if p_sw is None else p_sw
    sep, s0, s1 = eye_parts(cte, n_t, n_s, **kw)
    if sep <= 0:
        return 0.5
    d1 = sep * s1 / (s0 + s1)
    d0 = sep * s0 / (s0 + s1)

    def err(a):
        return 0.25 * (qfunc((d1 - a) / s1) + qfunc((d1 + a) / s1) + qfunc((d0 - a) / s0) + qfunc((d0 + a) / s0))

    e0 = err(0.0)
    a_max = 40.0 * eta_e if screen_e is None else screen_e
    n = 400
    acc, norm = 0.0, 0.0
    for i in range(n):
        a = (i + 0.5) * a_max / n
        w = math.exp(-a / eta_e)
        acc += w * ((1 - p_sw) * e0 + p_sw * err(a))
        norm += w
    return (1 - p_fast) * e0 + p_fast * acc / norm


def cte_min_rtn(n_t, n_s, p_req, eta_e, screen_e=None, **kw):
    lo, hi = 0.80, 1.0 - 1e-9
    if ber_rtn(hi, n_t, n_s, eta_e, screen_e, **kw) > p_req:
        return None
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if ber_rtn(mid, n_t, n_s, eta_e, screen_e, **kw) <= p_req:
            hi = mid
        else:
            lo = mid
    return hi


# ---- RED-TEAM (RT-DEV-charge-river-01): is a 4.5e12 cm^-2 packet still buried? ----
def buried_margin(n_sheet_cm2, dEc, t_cap_nm, eps_cap=None, e0=None, temp_k=358.0):
    eps_cap = V("eps_cap") if eps_cap is None else eps_cap
    e0 = V("e0_sub_eV") if e0 is None else e0
    g2d = V("m_eff") * 9.1093837e-31 / (math.pi * 1.054571817e-34 ** 2) * Q_E * 1e-4   # states / (eV cm^2)
    ef = n_sheet_cm2 / g2d                                                                  # eV above subband
    v_cap = Q_E * n_sheet_cm2 * 1e4 * t_cap_nm * 1e-9 / (eps_cap * EPS0)                    # V across the cap
    delta = dEc - v_cap - e0 - ef
    kt = K_B_EV * temp_k
    f_if = min(1.0, math.exp(-delta / kt))
    return dict(ef=ef, v_cap=v_cap, delta=delta, d_kt=delta / kt, f_if=f_if, eta_b=1 - f_if)


# ---- RED-TEAM (RT-DEV-charge-river-04): inter-plate gap barrier / pocket ----
def gap_strand(dv_ev, temp_k, t_dwell_s, f0=0.1, gap_nm=None):
    gap_nm = V("plate_iso_nm") if gap_nm is None else gap_nm
    d_cm2_s = 10.0 * K_B_EV * temp_k                    # Einstein, mu = 10 cm^2/Vs
    tau_diff = ((V("plate_thk_nm") + gap_nm) * 1e-7) ** 2 / d_cm2_s
    tau_b = tau_diff * math.exp(dv_ev / (K_B_EV * temp_k))
    return tau_b, f0 * math.exp(-t_dwell_s / tau_b)


def max_transfers(cte, n_s, p_req, dfe=True, cap=10000, **kw):
    best = 0
    for n_t in range(1, cap + 1):
        if ber_segment(cte, n_t, n_s, dfe, **kw)[0] <= p_req:
            best = n_t
        else:
            break
    return best


# =============================================================================================
# 5. Trap kinetics transfer of imec's point
# =============================================================================================
def nu0():
    v_th = math.sqrt(3 * 1.380649e-23 * 300.0 / (V("m_eff") * 9.1093837e-31)) * 100.0   # cm/s
    return V("sigma_cap_cm2") * v_th * V("nc_cm3"), v_th


def e_window(t_dwell_s, temp_k):
    return K_B_EV * temp_k * math.log(nu0()[0] * t_dwell_s)


def eps_transfer(f_stage, temp_k, phases, w_ev, f_tail, eps0, improvements=1.0):
    t_d0 = 1.0 / (V("imec_phases") * V("imec_clock_hz"))
    e0 = e_window(t_d0, 300.0)
    e = e_window(1.0 / (phases * f_stage), temp_k)
    g_rel = f_tail * math.exp(-(e - e0) / w_ev) + (1.0 - f_tail)
    return eps0 * g_rel * (temp_k / 300.0) * improvements


# =============================================================================================
# 6-11 helpers
# =============================================================================================
def good_area_mm2():
    # calibrated so 1-beta reproduces ram-venture: $3.8k wafer -> $1.48/GB at 0.447 Gb/mm2
    return V("wafer_1b_usd") / V("ddr5_usd_gb") * 8.0 / V("d1b_gb_mm2")


def wafer_cost(n_plates, topology=None, per_plate=None):
    topology = V("topology") if topology is None else topology
    per_plate = V("per_plate_usd") if per_plate is None else per_plate
    joint = V("joint_tier_usd") if topology == "joint" else 0.0      # RED-TEAM RT-CIRC-charge-river-02
    return V("array_base_usd") + joint + per_plate * n_plates + V("cmos_wafer_usd") + V("bond_usd")


def usd_per_gb(dens, n_plates, topology=None, per_plate=None, yld=None):
    yld = V("yield_rel") if yld is None else yld
    return wafer_cost(n_plates, topology, per_plate) / (dens * good_area_mm2() * yld / 8.0)


def lognorm_sf(t, med, sig):
    if t <= 0:
        return 1.0
    return 0.5 * math.erfc((math.log(t) - math.log(med)) / (sig * math.sqrt(2.0)))


def main():
    pk = packet()
    n_s = pk["n_s"]
    stages = min(stages_from_plates(V("n_plates")), V("lap_stages"))
    bits_hole = V("segments") * stages
    n_t = V("phases") * stages + 2          # + transfer into the output node and input injection
    slit_eff, eff, pitch = array_eff()
    dens = density_gb_mm2(bits_hole)

    p("# CHARGE-RIVER model output")
    p()
    p("Generated by `models/charge-river.py` (pure stdlib). Agent `dos-charge-river`, 2026-11-02. "
      "Every input is listed in section 0 with its source or `ESTIMATE: basis`.")
    p()

    # ---------------------------------------------------------------- 0 inputs
    p("## 0. Inputs")
    p()
    rows = []
    for k, (v, src) in INPUTS.items():
        vs = ("%.4g" % v) if isinstance(v, float) else str(v)
        rows.append(["`%s`" % k, vs, src.replace("|", "/")])
    table(["key", "value", "source / basis"], rows)

    # ---------------------------------------------------------------- 1 packet
    p("## 1. Geometry, packet, signal and noise")
    p()
    table(["quantity", "value", "arithmetic"], [
        ["channel diameter at gate", "%.0f nm" % pk["d_ch_nm"], "hole %.0f - 2 x %.0f nm dielectric" % (V("hole_d_nm"), V("diel_phys_nm"))],
        ["Cox", "%.2f fF/um^2" % (pk["cox"] * 1e3), "3.9 eps0 / EOT %.0f nm" % V("eot_nm")],
        ["gate capacitance per plate per hole", "%.3f fF" % pk["c_gate_fF"], "Cox x pi d x L(%.0f nm)" % V("plate_thk_nm")],
        ["full well", "%.0f e-" % pk["full_well"], "C x %.1f V / q" % V("dv_well")],
        ["signal packet N_s", "%.0f e-" % n_s, "%.0f%% of full well" % (100 * V("signal_fill"))],
        ["fat zero", "%.0f e-" % pk["n_fz"], "%.0f%% of N_s" % (100 * V("fat_zero_frac"))],
        ["sheet charge of a '1'", "%.2e cm^-2" % pk["n_sheet"], "sets traps-per-electron ratio (area-independent)"],
        ["FD conversion gain", "%.0f uV/e-" % pk["cg_uv"], "q / %.2f fF" % V("c_fd_fF")],
        ["signal at FD", "%.0f mV" % pk["sig_mV"], "N_s x CG"],
        ["read noise", "%.1f e- = %.1f mV rms" % (V("sigma_read_e"), pk["noise_mV"]), "ESTIMATE (post-CDS)"],
        ["raw SNR (no transfer loss)", "%.0f : 1" % (n_s / V("sigma_read_e")), "N_s / sigma"],
    ])
    p("imec's 3D device holds 'a few thousand' electrons per packet with larger features ([EE Journal](%s)). "
      "At 40 nm plates the packet is ~%.0f e-, so CHARGE-RIVER is a few-hundred-electron CCD: "
      "transfer loss, not read noise, sets the margin." % (IMEC_IMW26, n_s))
    p()

    # ---------------------------------------------------------------- 2 density
    p("## 2. Density vs 1-beta DDR5")
    p()
    table(["quantity", "value", "arithmetic"], [
        ["plates", V("n_plates"), "stack height %.1f um, hole AR %.0f" % (V("n_plates") * V("plate_pitch_nm") / 1000,
                                                                       V("n_plates") * V("plate_pitch_nm") / V("hole_d_nm"))],
        ["stages per segment", stages, "floor((%d - %d) / (%d segments x %d phases)), capped at %d" % (
            V("n_plates"), V("overhead_plates"), V("segments"), V("phases"), V("lap_stages"))],
        ["bits per hole", bits_hole, "%d segments x %d" % (V("segments"), stages)],
        ["transfers per segment read", n_t, "%d x %d + 2" % (V("phases"), stages)],
        ["hole pitch", "%.0f nm" % pitch, "sqrt(%.3f um^2)" % V("hole_cell_um2")],
        ["slit efficiency", "%.2f" % slit_eff, "%d x %.0f / (%d x %.0f + %.0f)" % (V("holes_per_row"), pitch, V("holes_per_row"), pitch, V("slit_nm"))],
        ["array efficiency", "%.2f" % eff, "slit x periphery %.2f" % V("periph_eff")],
        ["staircase efficiency (RED-TEAM, RT-PROC-02)", "%.3f" % stair_eff(V("n_plates")), "%.0f um strip / (%.0f um + %d plates x %.2f um)" % (
            V("strip_len_um"), V("strip_len_um"), V("n_plates"), V("stair_step_um"))],
        ["spares (RED-TEAM, RT-DEV-05 / RT-CIRC-04)", "%.2f" % (1 - V("spare_frac")), "1 - %.2f spare strings + sense nodes" % V("spare_frac")],
        ["joint-tier TAV efficiency (RED-TEAM, RT-CIRC-02)", "%.2f" % topo_eff(), "topology = %s" % V("topology")],
        ["ECC rate", "%.3f" % ecc_rate(), "512 / 532"],
        ["**user density**", "**%.2f Gb/mm^2**" % dens, "bits/hole / hole area x all efficiencies x ECC rate"],
        ["**vs 1-beta (0.447)**", "**%.2fx**" % (dens / V("d1b_gb_mm2")), "pre-red-team: %.2f Gb/mm^2 (%.2fx)" % (
            density_original(bits_hole), density_original(bits_hole) / V("d1b_gb_mm2"))],
        ["16 Gb die area (array efficiency included)", "%.1f mm^2" % (V("die_gbit") / dens), "vs 35.8 mm^2 for 1-beta 16 Gb"],
    ])
    p("RED-TEAM (RT-CIRC-charge-river-02): the %d bits per hole are now two 32-stage segments, each injected at its bottom and "
      "sensed at its top, with a [SPECULATIVE] regenerator tier at the joint of two 100-plate decks. Without that tier the "
      "same 64 bits need one 64-stage string (194 transfers; section 4c)." % bits_hole)
    p()

    # ---------------------------------------------------------------- 3 reliability
    p("## 3. Reliability target (raw BER per segment read)")
    p()
    dec_rate = V("laps_per_s") + 1.0 / V("t_scrub_s")
    p_req = p_required(dec_rate)
    rows = []
    for label, rate in [("park-and-shift (decode reads, %.0f laps/s + scrub)" % V("laps_per_s"), dec_rate),
                        ("scrub only (cold data)", 1.0 / V("t_scrub_s")),
                        ("continuous circulation at 50 MHz", V("continuous_laps_per_s"))]:
        for t, nd, par in [(1, 64, 8), (2, 512, 20), (4, 512, 40)]:
            pr = p_required(rate, t, nd, par)
            rows.append([label, "t=%d over %d b" % (t, nd), "%.2e" % pr, "%.2f" % qinv(pr)])
    table(["operating mode", "ECC", "max raw BER per decision", "Q (sigma)"], rows)
    p("**Design point:** %.1f decisions per bit per second, BCH t=2 over 512 b, %.0f FIT per 16 Gb die -> raw BER <= **%.1e** "
      "per segment read (Q = %.2f sigma)." % (dec_rate, V("fit_target"), p_req, qinv(p_req)))
    p()
    p("**Finding: do not circulate continuously.** 'Regeneration replaces refresh' is only safe if packets are PARKED "
      "between accesses (imec shows >200 s retention) and lapped on demand plus a scrub every ~%.0f s. Continuous "
      "circulation makes ~1.6e6 decisions per bit per second, about 50,000x more than the design point, and tightens the raw-BER "
      "requirement ~%.0fx (it also burns the endurance budget, section 9)." % (V("t_scrub_s"),
                                                                      p_req / p_required(V("continuous_laps_per_s"))))
    p()

    # ---------------------------------------------------------------- 4 CTE -> BER
    p("## 4. Charge-transfer efficiency -> BER -> minimum CTE")
    p()
    p("Model: per-transfer deferral eps = k_ws x (1 - CTE); after n_t transfers a '1' keeps h0 = (1-eps)^n_t and "
      "the rest trails into later packets. The noise is read noise plus fat-zero noise, plus binomial partition noise "
      "N_s h0 (1-h0) and Poisson noise on the deferred charge. Partition noise is physics that no correction removes. Without DFE the threshold is fixed: the "
      "worst '1' follows zeros and the worst '0' follows ones, so the eye is (2 h0 - 1) N_s. With DFE the threshold "
      "follows the decided history, and the eye is h0 N_s - 2 kappa x tail (LSST-style deferred-charge correction, "
      "[Snyder 2021](%s))." % LSST_DFE)
    p()
    rows = []
    for nt in (50, n_t, 2 * (n_t - 2) + 2):
        for ns in (150, n_s, 600, 3000):
            c0 = cte_min(nt, ns, p_req, dfe=False)
            c1 = cte_min(nt, ns, p_req, dfe=True)
            rows.append([nt, "%.0f" % ns, "%.5f" % c0 if c0 else "n/a", "%.5f" % c1 if c1 else "n/a",
                         "%.1e" % (1 - c1) if c1 else "n/a"])
    table(["transfers per segment", "N_s (e-)", "min CTE, no DFE", "min CTE, DFE", "max deferral/transfer (DFE)"], rows)
    c_nodfe = cte_min(n_t, n_s, p_req, dfe=False)
    c_dfe = cte_min(n_t, n_s, p_req, dfe=True)
    _, h0_req = ber_segment(c_dfe, n_t, n_s, True)
    p("**Base case (%d transfers, %.0f e-, k_ws %.1f, kappa %.2f):** minimum median CTE = **%.4f with DFE** (a '1' may lose "
      "%.0f%% of its charge in the worst string) and **%.4f without DFE**." % (
          n_t, n_s, V("k_ws"), V("kappa"), c_dfe, 100 * (1 - h0_req), c_nodfe))
    p()
    p("Compare the chief's packet-survival framing: 0.98^96 = %.1f%%, 0.999^96 = %.1f%%, 0.999^192 = %.1f%%. "
      "A regenerated binary packet does not need 91%% survival. It needs an eye that clears ~%.1f sigma, which the base "
      "case reaches at ~%.0f%% survival. The chief's 0.999 is a comfortable spec; the physics floor is ~%.4f." % (
          100 * 0.98 ** 96, 100 * 0.999 ** 96, 100 * 0.999 ** 192, qinv(p_req), 100 * h0_req, c_dfe))
    p()
    rows = []
    for sr in (4, 8, 15, 30):
        for kws in (1.0, 1.5, 3.0):
            for kap in (0.05, 0.1, 0.3):
                c = cte_min(n_t, n_s, p_req, dfe=True, k_ws=kws, kappa=kap, sig_r=sr)
                rows.append([sr, kws, kap, "%.4f" % c if c else "n/a"])
    p("Sensitivity of the DFE threshold to read noise, worst-string factor and DFE residual (%d transfers, %.0f e-):" % (n_t, n_s))
    p()
    table(["read noise (e-)", "k_ws", "kappa", "min CTE (DFE)"], rows)

    # ---------------------------------------------------------------- 4b RTN (RED-TEAM)
    p("## 4b. RED-TEAM: RTN tail of ~1e6 oxide source followers (RT-CIRC-charge-river-04, RT-DEV-charge-river-02)")
    p()
    p("A Gaussian read-noise term hides the 6-sigma tail. Model: a share p_fast = %.2f of sense nodes carries one trap with tau "
      "near the CDS interval; its step A is exponential with mean eta; it switches between the two CDS samples with "
      "probability %.2f. The die-average raw BER must still meet %.1e. 'Screen' = nodes whose measured step exceeds the "
      "threshold are mapped out (spare fraction = p_fast x exp(-T/eta)). Conversion gain %.0f uV/e-." % (
          V("rtn_p_fast"), V("rtn_p_switch"), p_req, pk["cg_uv"]))
    p()
    rows = []
    rtn_base = None
    for eta_mv in (1.4, 2.8, 4.2):
        eta_e = eta_mv * 1000.0 / pk["cg_uv"]
        for scr in (None, 60.0, 40.0, 25.0):
            c = cte_min_rtn(n_t, n_s, p_req, eta_e, scr)
            spare = 0.0 if scr is None else V("rtn_p_fast") * math.exp(-scr / eta_e)
            rows.append(["%.1f mV (%.1f e-)" % (eta_mv, eta_e), "none" if scr is None else "%.0f e-" % scr,
                         "%.4f" % c if c else "FAILS at any CTE", "%.2g%%" % (100 * spare),
                         "%.0f e-" % (eta_e * math.log(V("rtn_p_fast") * V("rtn_p_switch") / 1e-9))])
            if abs(eta_mv - V("rtn_eta_mV")) < 1e-9 and scr == 25.0:
                rtn_base = (c, spare, eta_e)
    table(["mean RTN step eta", "screen threshold", "min CTE (DFE) incl. RTN", "nodes spared", "unscreened 1e-9 per-read step quantile"], rows)
    sep_b, s0_b, s1_b = eye_parts(c_dfe, n_t, n_s)
    p("**Finding.** At the Gaussian floor the eye is %.0f e- wide (half-width ~%.0f e-). The reviewers are right that a "
      "Gaussian 8-10 e- term hides the tail: unscreened, eta = 2.8 mV moves the floor to ~0.9993 and 4.2 mV fails at any "
      "CTE. Screening nodes whose measured between-sample step exceeds ~25 e- (0.6%% of nodes spared at 2.8 mV, 1.8%% at "
      "4.2 mV; each spare costs only the 2 holes on that FD) brings the floor back to ~0.9975, within ~3e-4 of the "
      "Gaussian value. This only holds if the screen sees the traps: the decisive experiment must measure the step "
      "distribution AT the 2-5 ns CDS interval on >= 1e4 nodes, and the scrub must re-screen in the field because traps "
      "activate over life. Insurance (I-12627 principle): two independent SFs on each FD, averaged, with a disagreement "
      "flag that re-samples the still-held FD. An undetected large step then needs both SFs to step together: the event "
      "probability per read falls from p_fast x p_switch = %.0e to ~%.0e and the amplitude tail exp(-A/eta) enters "
      "squared, if trap sites are independent (hydrogen clusters could correlate them). It costs one TFT per FD, so it "
      "needs a second TFT sub-layer and is held as a later option." % (
          sep_b, sep_b / 2, V("rtn_p_fast") * V("rtn_p_switch"), (V("rtn_p_fast") * V("rtn_p_switch")) ** 2))
    p()

    # ---------------------------------------------------------------- 4c topology (RED-TEAM)
    p("## 4c. RED-TEAM: regeneration topology (RT-CIRC-charge-river-02, RT-PROC-charge-river-03)")
    p()
    p("Readout at a segment end is destructive and a straight hole has no return path, so the original 'sense and re-inject "
      "at each end' scheme was not physical. Every segment must be injected at one end and sensed at the other, with the "
      "decided bit carried back through the CMOS. Fill-and-spill (potential-equilibration) injection from a per-column line "
      "needs no per-hole TFT and is insensitive to the line's capacitance, so it can sit at the hole bottom; the low-noise "
      "floating diffusion sits only where a TFT tier can be built (hole top, or a deck joint).")
    p()
    rows = []
    topo_rows = []
    for label, topo, segs, st, npl, ntr in [
            ("original claim (2 x 32, sense+inject at both ends) [not physical]", "orig", 2, 32, 200, 98),
            ("joint: 2 decks x 100 plates, regenerator tier at joint [SPECULATIVE]", "joint", 2, 32, 200, 98),
            ("oneway: one 64-stage string, inject bottom, sense top", "oneway", 1, 64, 200, 194),
            ("oneway-100: 100-plate stack, one 32-stage string", "oneway", 1, 32, 100, 98),
            ("LIFO: bidirectional at each end (worst bit in+out)", "oneway", 2, 32, 200, 194)]:
        bh = segs * st
        floor = cte_min(ntr, n_s, p_req, True)
        floor_r = cte_min_rtn(ntr, n_s, p_req, rtn_base[2], 25.0) if rtn_base else None
        if topo == "orig":
            d = density_original(bh)
            c = (V("array_base_usd") - 300 + 10.0 * npl + V("cmos_wafer_usd") + V("bond_usd")) / (d * good_area_mm2() * V("yield_rel") / 8.0)
        else:
            d = density_gb_mm2(bh, npl, topo)
            c = usd_per_gb(d, npl, topo)
        lap_st = st
        lap_us = lap_st / V("f_stage_hz") * 1e6
        s_req = 1 - (V("l_avg_ns") - V("t_hit_ns")) * 1e-9 / (lap_us * 1e-6 / 2)
        laps_mult = 2 if label.startswith("LIFO") else 1
        cyc = lap_st * laps_mult * V("laps_per_s") * 3.15e7 * 5
        rows.append([label, bh, ntr, "%.4f / %.4f" % (floor, floor_r if floor_r else float('nan')),
                     "%.2f (%.1fx)" % (d, d / V("d1b_gb_mm2")), "$%.2f (%.2fx)" % (c, V("ddr5_usd_gb") / c),
                     "%.2f us / %.1f%%" % (lap_us * laps_mult, 100 * (1 - (V("l_avg_ns") - V("t_hit_ns")) * 1e-9 / (lap_us * laps_mult * 1e-6 / 2))),
                     "%.1e" % cyc])
        topo_rows.append((label, d, c, floor))
    table(["topology", "bits/hole", "transfers per read (worst bit)", "min CTE: Gaussian / incl. RTN (eta 2.8 mV, 25 e- screen)",
           "user Gb/mm^2 (x1b)", "$/GB (x cheaper than DDR5)", "lap / s needed for 40 ns", "plate cycles, 5 yr"], rows)
    p("**Finding.** The joint-regenerator design keeps 64 bits/hole at the old ~0.997 floor but adds a never-built TFT tier "
      "between decks (+$%.0f/wafer). Without it, 64 bits/hole need a one-way 64-stage string whose floor is ~0.9985 (2x less "
      "deferral allowed), a 1.28 us lap (s >= 96%%) and 3e11 plate cycles. A bidirectional (LIFO) scheme is strictly worse "
      "(same 194-transfer worst bit, a bottom sense node, a 32-bit buffer per node and 2x cycles). Cutting to a 100-plate "
      "stack keeps the 0.997 floor but halves bits/hole and loses to DDR5 on cost." % V("joint_tier_usd"))
    p()

    # ---------------------------------------------------------------- 5 trap kinetics
    p("## 5. Trap kinetics: carrying imec's 6.25 MHz point to a 50 MHz stage clock")
    p()
    nu, vth = nu0()
    t_d0 = 1.0 / (V("imec_phases") * V("imec_clock_hz"))
    t_d50 = 1.0 / (V("phases") * V("f_stage_hz"))
    p("Transport is not the limit. Drift across a %.0f nm gate at 10 cm^2/Vs and 1 V takes ~%.1e s, and diffusion "
      "takes ~%.1e s, both far below the %.1f ns dwell at 50 MHz. Loss comes from traps that capture "
      "electrons while the packet sits and emit them after it has moved two gates on. With SRH emission tau_e = "
      "exp(E/kT) / nu0, nu0 = sigma v_th N_c = %.1e /s (v_th %.1e cm/s), the gates that lose charge are those with "
      "tau_e near the dwell time, i.e. trap depth E_w = kT ln(nu0 t_dwell)." % (
          V("plate_thk_nm"), (V("plate_thk_nm") * 1e-7) ** 2 / (10 * 1.0), (V("plate_thk_nm") * 1e-7) ** 2 / (10 * 0.0257),
          t_d50 * 1e9, nu, vth))
    p()
    rows = []
    for label, f, ph, tk in [("imec planar, 6.25 MHz, 4-phase, 25 C", V("imec_clock_hz"), 4, 300.0),
                             ("CR 50 MHz stage, 3-phase, 85 C", V("f_stage_hz"), 3, 358.0),
                             ("CR 50 MHz stage, 3-phase, 25 C", V("f_stage_hz"), 3, 300.0),
                             ("CR 200 MHz stage, 3-phase, 25 C", 200e6, 3, 300.0),
                             ("CR 6.25 MHz stage, 3-phase, 85 C", 6.25e6, 3, 358.0)]:
        td = 1.0 / (ph * f)
        rows.append([label, "%.2f ns" % (td * 1e9), "%.3f eV" % e_window(td, tk)])
    table(["condition", "gate dwell", "trap depth probed E_w"], rows)
    p("**Finding: the hard corner is fast and COOL, not hot.** At 85 C a 50 MHz stage clock probes traps only "
      "~%.0f meV shallower than imec's 6.25 MHz room-temperature point, because heat speeds emission. At 25 C it probes ~%.0f meV "
      "shallower, into the denser band tail. The experiment must therefore report CTE at 25 C as well as 85 C." % (
          1000 * (e_window(t_d0, 300) - e_window(t_d50, 358)), 1000 * (e_window(t_d0, 300) - e_window(t_d50, 300))))
    p()
    imp = (1 - V("f_it") * V("eta_buried")) * V("eta_fz")
    rows = []
    for interp, eps0 in [("imec 98% = PER TRANSFER", 1 - V("imec_cte")),
                         ("imec 98% = END-TO-END (142 b x 4 ph)", 1 - V("imec_cte") ** (1.0 / (V("imec_bits") * V("imec_phases"))))]:
        for w in (0.015, 0.030, 0.060):
            for ft in (0.25, 1.0):
                e85 = eps_transfer(V("f_stage_hz"), 358.0, 3, w, ft, eps0)
                e25 = eps_transfer(V("f_stage_hz"), 300.0, 3, w, ft, eps0)
                e25i = eps_transfer(V("f_stage_hz"), 300.0, 3, w, ft, eps0, imp)
                worst = max(eps_transfer(V("f_stage_hz"), 358.0, 3, w, ft, eps0, imp), e25i)
                verdict = "GO" if 1 - worst >= c_dfe else ("marginal" if 1 - worst >= 0.99 else "NO-GO")
                rows.append([interp, "%.0f" % (w * 1000), "%.2f" % ft, "%.4f" % (1 - e85), "%.4f" % (1 - e25),
                             "%.4f" % (1 - e25i), verdict])
    table(["imec reading", "tail slope W (meV)", "tail share of loss", "CTE surface 85C", "CTE surface 25C",
           "CTE buried+fat-zero 25C", "verdict: worst of 25/85 C (improved) vs floor %.4f" % c_dfe], rows)
    p("Improvement factor assumed for buried heterochannel + fat zero: (1 - %.1f x %.1f) x %.1f = %.2f "
      "(ESTIMATE; no oxide buried-channel CCD has been measured). The model splits on how imec's '>98%%' is defined. Read per transfer, "
      "CHARGE-RIVER needs a ~%.0fx cut in deferral, which the buried channel and fat zero only reach if most of "
      "imec's loss is interface-trap loss. Read end-to-end (per transfer 0.99996), the device clears the floor "
      "with ~%.0fx margin today. **Buying the IEDM 2024 paper (~$35) is the cheapest experiment in the dossier.**" % (
          V("f_it"), V("eta_buried"), V("eta_fz"), imp, (1 - V("imec_cte")) / (1 - c_dfe),
          (1 - c_dfe) / (1 - V("imec_cte") ** (1.0 / (V("imec_bits") * V("imec_phases"))))))
    p()

    p("RED-TEAM (RT-IND-charge-river-03): a search on 2026-11-02 found the IEDM 2024 record (paper 37-6, Kishore et al., "
      "DOI 10.1109/iedm50854.2024.10873539) still says only 'CTE >98%' and adds 'multilevel capability'. The definition is "
      "still unread; the $35 purchase stays task 1 of month 0 and both readings are carried.")
    p()

    # ---------------------------------------------------------------- 5a buried electrostatics (RED-TEAM)
    p("## 5a. RED-TEAM: does a 4.5e12 cm^-2 packet stay buried? (RT-DEV-charge-river-01)")
    p()
    p("Margin of the cap conduction band above the packet's Fermi level at the gate-dielectric interface: Delta = dEc - "
      "q n t_cap / eps_cap - E0 - n / g2D (m* %.2f). The share of interface-trap loss left is approximated as exp(-Delta/kT) "
      "(optimistic: ignores wavefunction penetration and tunnelling to border traps). 85 C." % V("m_eff"))
    p()
    rows = []
    for dec in (0.30, 0.40, 0.50, 0.70):
        for tc in (2.0, 2.5, 3.0):
            for ns_cm2 in (4.5e12, 2.5e12):
                bm = buried_margin(ns_cm2, dec, tc)
                rows.append(["%.2f" % dec, "%.1f" % tc, "%.1e" % ns_cm2, "%.0f" % (1000 * bm["ef"]), "%.0f" % (1000 * bm["v_cap"]),
                             "%.0f meV (%.1f kT)" % (1000 * bm["delta"], bm["d_kt"]), "%.2f" % bm["eta_b"]])
    table(["dEc (eV)", "cap (nm)", "sheet charge (cm^-2)", "E_F above subband (meV)", "drop across cap (mV)", "Delta",
           "interface-loss removal (est.)"], rows)
    bm0 = buried_margin(pk["n_sheet"], V("dEc_eV"), V("t_cap_nm"))
    p("**Finding.** At the dossier's spec (0.30 eV, 2.5 nm cap, full fill) Delta is only %.1f kT, so the top of each '1' packet "
      "does reach the cap interface, as RT-DEV says. Small composition swings (+-0.05 eV, RT-DEV-03 / RT-PROC-06) move the "
      "removal between ~0.3 and ~0.9, so the model now carries eta_buried = %.1f, not 0.9. The redesign spec is dEc >= 0.5 eV "
      "with a <= 2.5 nm cap (Delta >= ~6 kT at full fill). That offset exists in the literature for IGZO on Ga2O3 "
      "(0.71 +- 0.1 eV, crystalline beta-Ga2O3, XPS) but has not been measured for ALD amorphous stacks, and a Ga-rich cap "
      "conflicts with the Ga-free goal (ZTO/ITZO caps must be measured). Reaching dEc >= 0.5 eV at <= 3e12 cm^-2 is the "
      "fallback (smaller packets cost CTE floor: 150 e- needs ~0.999)." % (bm0["d_kt"], V("eta_buried")))
    p()

    # ---------------------------------------------------------------- 5b gap barrier (RED-TEAM)
    p("## 5b. RED-TEAM: inter-plate gap barriers and pockets (RT-DEV-charge-river-04, RT-PROC-charge-river-05)")
    p()
    t_dw = 1.0 / (V("phases") * V("f_stage_hz"))
    budget_eps = 0.2 * (1 - c_dfe) / V("k_ws")
    rows = []
    for dv_kt in (0.5, 1, 2, 3, 4, 5, 6):
        for tk in (300.0, 358.0):
            tau_b, fs = gap_strand(dv_kt * K_B_EV * tk, tk, t_dw)
            rows.append(["%.1f kT (%.0f mV)" % (dv_kt, 1000 * dv_kt * K_B_EV * tk), "%.0f C" % (tk - 273), "%.3f ns" % (tau_b * 1e9),
                         "%.1e" % fs, "OK" if fs <= budget_eps else "strands charge"])
    table(["static barrier in the gap", "T", "escape time over barrier", "stranded fraction after %.2f ns dwell (10%% left behind)" % (t_dw * 1e9),
           "vs 20%% of the deferral budget (%.1e)" % budget_eps], rows)
    c_gap = pk["cox"] * math.pi * pk["d_ch_nm"] * 1e-9 * V("plate_iso_nm") * 1e-9 * 0.5
    p("**Finding.** A static barrier in the 15 nm gap is tolerable up to ~2.5-3 kT (~65-90 mV) at a 6.7 ns dwell, so RT-DEV's "
      "< 0.5 kT criterion is stricter than the transport needs. A static pocket is neutralised by the fat zero (%.0f e-) as "
      "long as its capacity is below it: with ~%.3f fF of gap coupling (half of Cox over the gap) that is a pocket up to ~%.0f mV deep. Signal-dependent "
      "pockets are not neutralised and only electrostatics plus measurement can bound them, so a 2D/3D gap solve is a month-2 "
      "deliverable, planar CTE is measured against gap width, and run 1 adds overlapping two-level gates as the "
      "process-clean reference (RT-PROC-05). The vertical gap is set by a deposited oxide, not e-beam lithography, so it is "
      "more uniform than the planar proxy." % (pk["n_fz"], c_gap * 1e15, pk["n_fz"] * Q_E / c_gap * 1000))
    p()

    # ---------------------------------------------------------------- 6 sensitivity key unknown
    p("## 6. KEY-UNKNOWN SENSITIVITY: CTE -> segment length -> density and $/GB")
    p()
    p("For each median per-transfer CTE: the longest segment whose worst-string BER meets %.1e with DFE, the plates that "
      "segment needs (two segments per hole), user density and $/GB. Fewer plates make the wafer cheaper, but density "
      "falls faster." % p_req)
    p()
    rows = []
    max_st = stages_from_plates(V("n_plates"))
    for cte in (0.98, 0.99, 0.995, 0.996, 0.997, 0.998, 0.999, 0.9995, 0.9999):
        nt_max = max_transfers(cte, n_s, p_req, True, cap=3 * max_st + 2)
        st = max(0, min(max_st, (nt_max - 2) // V("phases")))
        bh = V("segments") * st
        if bh == 0:
            rows.append(["%.4f" % cte, nt_max, 0, "-", "-", "-", "-", "DEAD"])
            continue
        npl = plates_for_stages(st)
        d = density_gb_mm2(bh, npl)
        c = usd_per_gb(d, npl)
        # RED-TEAM fallback: one-way string (no joint tier), up to 64 stages in the same 200 plates
        st1 = max(0, min(2 * max_st, (nt_max - 2) // V("phases")))
        if st1 > 0:
            npl1 = V("phases") * st1 + V("overhead_plates")
            d1 = density_gb_mm2(st1, npl1, "oneway")
            c1 = usd_per_gb(d1, npl1, "oneway")
            ow = "%d b, %.2f (%.1fx), $%.2f" % (st1, d1, d1 / V("d1b_gb_mm2"), c1)
        else:
            ow = "-"
        verdict = "GO" if d / V("d1b_gb_mm2") >= 2.5 else ("weak" if d / V("d1b_gb_mm2") >= 1.5 else "NO-GO")
        rows.append(["%.4f" % cte, nt_max, st, bh, npl, "%.2f (%.1fx)" % (d, d / V("d1b_gb_mm2")),
                     "$%.2f (%.2fx)" % (c, V("ddr5_usd_gb") / c), ow, verdict])
    table(["median CTE", "max transfers/segment", "stages/segment", "bits/hole", "plates", "joint: user Gb/mm^2 (x1b)",
           "joint: $/GB (x cheaper than $1.48)", "oneway fallback: bits/hole, Gb/mm^2, $/GB", "verdict (density)"], rows)
    p("RED-TEAM: verdict thresholds now key on density (GO >= 2.5x, weak >= 1.5x) because cost per bit no longer beats DDR5 "
      "materially at $%.0f/plate (section 11). The 'joint' columns assume the [SPECULATIVE] deck-joint regenerator tier "
      "(two regenerated 32-stage segments); the one-way fallback needs CTE >= ~0.9985 for the full 64 bits." % V("per_plate_usd"))
    p()

    # ---------------------------------------------------------------- 7 latency & schedulability
    p("## 7. Latency and schedulability")
    p()
    p("Effective latency = t_hit + (1 - s) x T_lap / 2, where s is the share of bytes whose address is known at least "
      "one lap ahead. Required s for a %.0f ns average with t_hit = %.0f ns:" % (V("l_avg_ns"), V("t_hit_ns")))
    p()
    w_bytes = V("params") * V("bytes_per_param")
    kv_bytes = V("kv_bytes_per_token") * V("context") * V("batch")
    total = w_bytes + kv_bytes
    rows = []
    for f in (4e6, 6.25e6, 25e6, 50e6, 100e6, 200e6):
        t_lap = V("lap_stages") / f
        s_req = 1 - (V("l_avg_ns") - V("t_hit_ns")) * 1e-9 / (t_lap / 2)
        # dense
        s_dense = 1 - V("random_share_dense")
        # MoE + sparse attention
        wsh = w_bytes / total
        ksh = kv_bytes / total
        r = V("random_share_moe")
        sched_w = (1 - V("expert_share_moe")) + V("expert_share_moe") * lognorm_sf(t_lap * 1e6, V("expert_lead_med_us"), V("lead_sigma_ln"))
        sched_k = (1 - V("sparse_kv_share")) + V("sparse_kv_share") * lognorm_sf(t_lap * 1e6, V("sparse_kv_lead_med_us"), V("lead_sigma_ln"))
        s_moe = (1 - r) * (wsh * sched_w + ksh * sched_k)
        l_dense = V("t_hit_ns") + (1 - s_dense) * t_lap / 2 * 1e9
        l_moe = V("t_hit_ns") + (1 - s_moe) * t_lap / 2 * 1e9
        rows.append(["%.2f MHz" % (f / 1e6), "%.2f us" % (t_lap * 1e6), "%.1f%%" % (100 * max(0, s_req)),
                     "%.1f%% -> %.0f ns" % (100 * s_dense, l_dense), "%.1f%% -> %.0f ns" % (100 * s_moe, l_moe)])
    table(["stage clock", "32-stage lap", "s needed for 40 ns", "dense 70B decode: s -> avg latency",
           "MoE + sparse attention: s -> avg latency"], rows)
    t_lap64 = 64 / V("f_stage_hz")
    wsh_, ksh_ = w_bytes / total, kv_bytes / total
    sw64 = (1 - V("expert_share_moe")) + V("expert_share_moe") * lognorm_sf(t_lap64 * 1e6, V("expert_lead_med_us"), V("lead_sigma_ln"))
    sk64 = (1 - V("sparse_kv_share")) + V("sparse_kv_share") * lognorm_sf(t_lap64 * 1e6, V("sparse_kv_lead_med_us"), V("lead_sigma_ln"))
    s_moe64 = (1 - V("random_share_moe")) * (wsh_ * sw64 + ksh_ * sk64)
    p("RED-TEAM (RT-CIRC-charge-river-02): the joint topology keeps the 32-stage lap above. The one-way 64-stage fallback "
      "has a %.2f us lap at 50 MHz: s >= %.1f%% is needed for 40 ns; dense decode gives %.0f ns and MoE + sparse attention "
      "%.0f ns (s = %.1f%%)." % (t_lap64 * 1e6, 100 * (1 - 25e-9 / (t_lap64 / 2)),
                                  V("t_hit_ns") + V("random_share_dense") * t_lap64 / 2 * 1e9,
                                  V("t_hit_ns") + (1 - s_moe64) * t_lap64 / 2 * 1e9, 100 * s_moe64))
    p()
    p("Workload per decode step (dense 70B FP8, batch %d, %d context): weights %.0f GB + KV %.1f GB, all in a fixed or "
      "append-then-scan order. **Finding:** an access only has to be known ONE LAP ahead (0.64 us at 50 MHz), and "
      "a decode layer takes tens of microseconds, so most routed-expert and top-k KV reads are schedulable at 50 MHz. "
      "With a %.1f%% random floor (dense decode), even imec's 4-6 MHz clock meets 40 ns. With MoE + sparse attention "
      "(%.0f%% random floor, microsecond lead times), 4-6 MHz gives 0.7-1.5 us averages while 50 MHz gives ~26 ns. That is the "
      "real case for the 50 MHz clock. The trace-driven simulator must measure the random floor and the lead-time "
      "distribution." % (V("batch"), V("context"), w_bytes / 1e9, kv_bytes / 1e9, 100 * V("random_share_dense"),
                         100 * V("random_share_moe")))
    p()

    # ---------------------------------------------------------------- 8 bandwidth & energy
    p("## 8. Bandwidth and energy")
    p()
    # plate capacitance per hole (gate + both neighbours)
    plate_area_um2 = V("hole_cell_um2") - math.pi * (V("hole_d_nm") / 2000.0) ** 2
    c_pp = 3.9 * EPS0 / (V("plate_iso_nm") * 1e-9) * plate_area_um2 * 1e-12 * 1e15     # fF
    c_plate = pk["c_gate_fF"] + 2 * c_pp
    act_plates = plates_for_stages(stages) - V("overhead_plates")
    e_stage = act_plates * c_plate * 1e-15 * V("v_clk") ** 2                              # J per stage per hole
    e_shift_bit = e_stage / V("segments") * (1 - V("eta_rec")) * 1e15                     # fJ/bit
    e_shift_bit_cv2 = e_stage / V("segments") * 1e15
    c_col = V("rows_per_col") * V("c_col_per_hole_fF") + V("c_col_fixed_fF")
    e_col = c_col * V("v_col_swing") * V("vdd")                                           # fJ
    e_sense = e_col + V("e_sa_fj") + V("e_sf_fj") + V("e_dfe_fj")
    e_bit = e_shift_bit + e_sense
    holes_die = V("die_gbit") * 1e9 / ecc_rate() / bits_hole
    sub_holes = V("rows_per_col") * V("rows_per_col")
    n_sa = holes_die / sub_holes * V("rows_per_col") * V("segments")
    bw_peak_tbs = n_sa * V("f_stage_hz") / 8 / 1e12
    steps_s = V("laps_per_s")
    demand_tbs = total * steps_s / 1e12
    dies = total / (V("die_gbit") / 8 * 1e9)
    table(["quantity", "value", "arithmetic"], [
        ["plate-to-plate C per hole (each side)", "%.3f fF" % c_pp, "3.9 eps0/%.0f nm x %.4f um^2" % (V("plate_iso_nm"), plate_area_um2)],
        ["switched C per plate per hole", "%.3f fF" % c_plate, "gate + 2 x plate-plate"],
        ["shift energy per bit (CV^2)", "%.0f fJ" % e_shift_bit_cv2, "%d plates x C x %.1f V^2 / %d bits per stage" % (act_plates, V("v_clk"), V("segments"))],
        ["shift energy per bit (recycled)", "%.0f fJ" % e_shift_bit, "x (1 - %.2f)" % V("eta_rec")],
        ["column + SA + SF + DFE", "%.0f fJ" % e_sense, "C_col %.0f fF x %.2f V x %.1f V + %.0f + %.0f + %.0f" % (
            c_col, V("v_col_swing"), V("vdd"), V("e_sa_fj"), V("e_sf_fj"), V("e_dfe_fj"))],
        ["**core energy per bit read**", "**%.0f fJ (%.2f pJ)**" % (e_bit, e_bit / 1000), "vs HBM3 %.2f pJ/bit total incl. I/O" % V("hbm3_pj_bit")],
        ["sense nodes per 16 Gb die", "%.2e" % n_sa, "%d SAs x %d ends per %d-hole subarray" % (V("rows_per_col"), V("segments"), sub_holes)],
        ["peak bandwidth per die at 50 MHz", "%.1f TB/s" % bw_peak_tbs, "all subarrays streaming"],
        ["power at peak", "%.1f W" % (bw_peak_tbs * 8e12 * e_bit * 1e-15), "core only"],
        ["70B decode demand at %.0f steps/s" % steps_s, "%.1f TB/s over %.0f dies" % (demand_tbs, dies), "%.0f GB per step" % (total / 1e9)],
        ["per-die demand", "%.0f GB/s = %.1f%% of peak" % (demand_tbs * 1e3 / dies, 100 * demand_tbs / dies / bw_peak_tbs), ""],
    ])
    scrub_w = V("die_gbit") * 1e9 / ecc_rate() * e_bit * 1e-15 / V("t_scrub_s")
    ref_w = V("die_gbit") * 1e9 * V("ddr5_refresh_fj_bit") * 1e-15 / V("ddr5_tref_s")
    p("**Refresh:** scrubbing every %.0f s costs %.3f mW per 16 Gb die, against DDR5's %.1f mW (46 fJ/bit every 64 ms): "
      "~%.0fx lower. Read energy is DRAM-like (~0.1 pJ/bit core), so the system energy win comes from refresh and from "
      "placing the tier near compute, not from the array." % (V("t_scrub_s"), scrub_w * 1e3, ref_w * 1e3, ref_w / scrub_w))
    p()
    # RED-TEAM (RT-CIRC-charge-river-03): like-for-like energy per USEFUL bit, with I/O and a realistic clock-recovery figure
    strip_holes = V("strip_len_um") * 1000.0 / pitch * V("holes_per_row")
    lap_e_strip = strip_holes * stages * e_stage * (1 - V("eta_rec"))                     # J to lap one clock strip
    e_rand_useful = (lap_e_strip / 512 + e_sense * 1e-15) * 1e12                          # pJ per useful bit, 64 B access
    e_stream = e_bit / 1000 + V("io_pj_bit")
    e_rand = e_rand_useful + V("io_pj_bit")
    rows = []
    for lab, rshare in [("dense decode", V("random_share_dense")), ("MoE + sparse attention", V("random_share_moe"))]:
        mix = (1 - rshare) * e_stream + rshare * e_rand
        rows.append([lab, "%.1f%%" % (100 * rshare), "%.2f pJ" % mix, "%.1fx" % (V("hbm3_pj_bit") / mix)])
    p("**RED-TEAM energy per useful bit (RT-CIRC-charge-river-03).** Clock recovery is now %.0f%% (3-phase charge sharing / "
      "stepwise charging; on-chip LC is not feasible at 50 MHz) and an HBM-class I/O cost of %.1f pJ/bit is added. A clock "
      "strip (%.0f um, %d rows) holds %.0f holes, so a random 64 B access that laps one strip for 512 useful bits costs "
      "%.1f pJ per useful bit plus I/O (worse than a DRAM row activation for 64 B). Streaming costs %.2f pJ/bit incl. I/O." % (
          100 * V("eta_rec"), V("io_pj_bit"), V("strip_len_um"), V("holes_per_row"), strip_holes, e_rand_useful, e_stream))
    p()
    table(["workload", "random (unscheduled) share", "energy per useful bit incl. I/O", "vs HBM3 3.44 pJ/bit"], rows)
    p("The like-for-like energy step is ~2-3x per streamed bit, not the ~48x a 0.07 pJ core vs 3.44 pJ total comparison "
      "suggests. The ~%.0fx refresh/standby saving stands." % (ref_w / scrub_w))
    p()

    # ---------------------------------------------------------------- 9 retention & endurance
    p("## 9. Retention and endurance budgets")
    p()
    kt85 = K_B_EV * 358.0
    ni = math.sqrt(5e18 * 5e19) * math.exp(-3.1 / (2 * kt85))
    vol_cm3 = math.pi * pk["d_ch_nm"] * 1e-7 * V("plate_thk_nm") * 1e-7 * 8e-7
    gen_e_s = ni / 1e-6 * vol_cm3
    allowed_loss = 0.10 * n_s
    i_leak_aa = allowed_loss / V("t_scrub_s") * Q_E * 1e18
    cyc_park = V("lap_stages") * V("laps_per_s") * 3.15e7 * 5
    cyc_cont = V("f_stage_hz") * 3.15e7 * 5
    table(["quantity", "value", "arithmetic"], [
        ["IGZO intrinsic density at 85 C", "%.1e cm^-3" % ni, "sqrt(NcNv) exp(-3.1 eV / 2kT) (ESTIMATE Nc 5e18, Nv 5e19)"],
        ["thermal generation per well", "%.1e e-/s" % gen_e_s, "n_i / 1 us x channel volume (8 nm film)"],
        ["allowed loss between scrubs", "%.0f e- (10%% of N_s)" % allowed_loss, "ESTIMATE"],
        ["max well leakage for %.0f s scrub" % V("t_scrub_s"), "%.2f aA" % i_leak_aa, "comparable to IGZO Ioff <1 aA (A1: OCTRAM)"],
        ["imec retention", ">%.0f s" % V("imec_retention_s"), "planar, (%s)" % IMEC_IEDM24],
        ["plate cycles, 5 yr, park-and-shift", "%.1e" % cyc_park, "%d stages x %.0f laps/s x 5 yr" % (V("lap_stages"), V("laps_per_s"))],
        ["plate cycles, 5 yr, continuous", "%.1e" % cyc_cont, "50 MHz x 5 yr"],
        ["imec demonstrated", ">%.0e" % V("imec_endurance"), "lower bound, no degradation"],
        ["gap to demonstrate (park-and-shift)", "%.0fx" % (cyc_park / V("imec_endurance")), "need a >=1e12 cycle test at 85 C"],
    ])
    p("Silicon CCD memories died partly on dark current; IGZO generation is ~%.0e e-/s per well, effectively zero. "
      "Retention is set by inter-well barrier and gate leakage, the same aA class that IGZO 2T0C cells already show." % gen_e_s)
    p()

    # ---------------------------------------------------------------- 10 plate RC
    p("## 10. Plate RC (clock distribution)")
    p()
    # RED-TEAM: metal left beside the holes and capacitance both scale with strip width (holes_per_row), so RC/um^2 does not
    w_metal_nm = V("holes_per_row") * (pitch - V("hole_d_nm"))
    r_um = V("rho_w_ohm_m") / (V("plate_thk_nm") * 1e-9 * w_metal_nm * 1e-9) * 1e-6       # ohm/um
    c_um = c_plate * V("holes_per_row") / pitch * 1000.0                                   # fF/um
    rows = []
    for f in (6.25e6, 50e6, 200e6):
        t_phase = 1.0 / (3 * f)
        # settle 5 tau within 30% of phase time, distributed tau ~0.38 RC
        rc_max = 0.3 * t_phase / 5 / 0.38
        l_max = math.sqrt(rc_max / (r_um * c_um * 1e-15))
        rows.append(["%.2f MHz" % (f / 1e6), "%.2f ns" % (t_phase * 1e9), "%.0f um" % l_max])
    p("%d-hole-wide clock strip (RED-TEAM: was 1): W left beside the holes = %.0f nm, r = %.0f ohm/um, c = %.2f fF/um." % (
        V("holes_per_row"), w_metal_nm, r_um, c_um))
    p()
    table(["stage clock", "phase time", "max plate length between straps/drivers"], rows)
    p("Clocking at 50 MHz needs a strap or driver every ~0.1 mm of row, which is routine on a bonded CMOS wafer. "
      "This is NOT the 5 mm word-plane RC (~160 ns) problem the critics raised, because CHARGE-RIVER's clock rows are short.")
    p()
    p("**RED-TEAM correction (RT-PROC-charge-river-02).** A buried plate cannot be 'strapped': each driven strip end needs a "
      "staircase with one step per plate. The strip length is set by RC (above; a laxer 3-tau-in-50% settle gives ~1.65x "
      "longer), and RC per um^2 is independent of strip width, so wider strips do not help. Staircase efficiency:")
    p()
    rows = []
    for npl_ in (100, 200, 300):
        rows.append([npl_, "%.0f um" % (npl_ * V("stair_step_um"))] +
                    ["%.2f" % stair_eff(npl_, L) for L in (100.0, 150.0, 200.0)] + ["%.2f" % stair_eff(npl_, 150.0, 0.015)])
    table(["plates", "staircase length", "eff, 100 um strip", "eff, 150 um strip (base)", "eff, 200 um strip",
           "[SPECULATIVE] 3-trench selective-recess phase contacts (~3 um/end)"], rows)
    p("At 200 plates the staircase costs ~%.0f%% of array area (rt-PROC: 23-38%%). Per-row slits cannot simply be dropped: "
      "shared plates would multiply park-and-shift cycles. The base design widens strips to 2 rows only to amortise the "
      "wider replacement-metal slits, not to save staircase. A staircase-free contact (three sacrificial plate materials, "
      "each phase contacted through its own trench after selectively recessing the other two) would recover it, but no "
      "such process exists [SPECULATIVE]." % (100 * (1 - stair_eff(V("n_plates")))))
    p()

    # ---------------------------------------------------------------- 11 cost
    p("## 11. Cost per bit vs DDR5 ($1.48/GB)")
    p()
    npl = plates_for_stages(stages)
    c_cr = usd_per_gb(dens, npl)
    nand_xcheck = V("nand_tlc_usd_gb") * V("nand_bits_per_hole") / bits_hole
    table(["quantity", "value", "arithmetic"], [
        ["effective good area per wafer", "%.0f mm^2" % good_area_mm2(), "calibrated: $3.8k / $1.48 x 8 / 0.447"],
        ["CHARGE-RIVER wafer (array + joint tier + plates + CMOS + bond/CuA)", "$%.0f" % wafer_cost(npl), "%.0f + %.0f + %d x %.0f + %.0f + %.0f" % (
            V("array_base_usd"), V("joint_tier_usd") if V("topology") == "joint" else 0.0, npl, V("per_plate_usd"),
            V("cmos_wafer_usd"), V("bond_usd"))],
        ["**$/GB**", "**$%.2f (%.2fx vs DDR5; >1 = cheaper)**" % (c_cr, V("ddr5_usd_gb") / c_cr), "wafer / (density x area x yield %.1f / 8)" % V("yield_rel")],
        ["NAND-price cross-check", "~$%.2f/GB" % nand_xcheck, "$0.09/GB TLC x %d b per NAND hole / %d b per CR hole (price, incl. margin; NAND spreads its staircase over 9x more bits per plate-hole, so this is not a CR cost floor)" % (
            V("nand_bits_per_hole"), bits_hole)],
    ])
    rows = []
    for wm in (0.7, 1.0, 1.3):
        for y in (0.5, 0.8, 0.95):
            c = wafer_cost(npl) * wm / (dens * good_area_mm2() * y / 8.0)
            rows.append(["x%.1f" % wm, "%.2f" % y, "$%.2f" % c, "%.1fx" % (V("ddr5_usd_gb") / c)])
    table(["wafer cost", "rel. yield", "$/GB", "vs DDR5"], rows)
    p("The cost step is ~2x, not 10x: a CCD hole stores %d bits where a TLC NAND hole stores ~%d, so CHARGE-RIVER "
      "inherits NAND's process but not its bits per hole." % (bits_hole, V("nand_bits_per_hole")))
    p()
    p("**RED-TEAM cost sensitivity (RT-PROC-charge-river-04, RT-IND-charge-river-02, RT-PROC-charge-river-02).** $/GB at "
      "yield %.1f for per-plate cost x staircase x topology:" % V("yield_rel"))
    p()
    rows = []
    for pp in (10.0, 15.0, 25.0, 35.0):
        row = ["$%.0f" % pp]
        for topo, bh_, npl_, stair_ in [("joint", 64, 200, None), ("oneway", 64, 200, None), ("joint", 64, 200, stair_eff(200, 150.0, 0.015))]:
            d_ = density_gb_mm2(bh_, npl_, topo, stair_)
            c_ = usd_per_gb(d_, npl_, topo, pp)
            row.append("$%.2f (%.2fx)" % (c_, V("ddr5_usd_gb") / c_))
        rows.append(row)
    table(["per plate pair", "joint (base)", "oneway fallback (needs CTE ~0.9985)", "joint + [SPECULATIVE] staircase-free contacts"], rows)
    d_base = density_gb_mm2(bits_hole, npl)
    p("**Finding: the cost leg does not survive.** At $%.0f per plate (rt-PROC's NAND-derived $20-38, range $12-35 carried) "
      "plus the staircase, the joint tier and spares, CHARGE-RIVER costs $%.2f/GB, %.2fx DDR5's $1.48: parity, not a step. "
      "Even at yield 0.95 it is $%.2f/GB. It beats DDR5 by >= 1.4x only with per-plate cost <= ~$15 AND staircase-free "
      "contacts, both unproven. The density step (%.1fx 1-beta) and the refresh/standby step remain." % (
          V("per_plate_usd"), usd_per_gb(d_base, npl), V("ddr5_usd_gb") / usd_per_gb(d_base, npl),
          usd_per_gb(d_base, npl, yld=0.95), d_base / V("d1b_gb_mm2")))
    p()

    # ---------------------------------------------------------------- 12 GO / NO-GO
    p("## 12. GO / NO-GO")
    p()
    # NO-GO bound: CTE where density falls below 1.5x
    nogo = None
    for i in range(0, 2001):
        cte = 0.98 + i * 0.00001
        nt_max = max_transfers(cte, n_s, p_req, True, cap=3 * max_st + 2)
        st = max(0, min(max_st, (nt_max - 2) // V("phases")))
        if st > 0 and density_gb_mm2(V("segments") * st, plates_for_stages(st)) / V("d1b_gb_mm2") >= 1.5:
            nogo = cte
            break
    nogo_cost = None
    if nogo:
        st_n = max(0, min(max_st, (max_transfers(nogo, n_s, p_req, True, cap=3 * max_st + 2) - 2) // V("phases")))
        nogo_cost = usd_per_gb(density_gb_mm2(V("segments") * st_n, plates_for_stages(st_n)), plates_for_stages(st_n))
    p("**GO/NO-GO:** GO if planar test CCDs (sheet charge ~%.1e cm^-2, i.e. <= %.0f e- per 40 nm-plate packet; worst-case 1-after-0s pattern) "
      "show a median per-transfer CTE >= **%.4f with DFE** (deferral <= %.1e per transfer) at a >= 50 MHz STAGE clock "
      "(>= 150 M transfers/s) at BOTH 25 C and 85 C, and a 98-transfer loop with FPGA regeneration logs raw BER <= %.0e. "
      "The chief's 0.999 spec is the STRONG-GO line: it buys 64-stage segments or 3x the worst-string spread. "
      "NO-GO if every channel variant stays below CTE %.4f at >= 50 M transfers/s, where density drops under 1.5x 1-beta "
      "and cost rises to ~$%.2f/GB, worse than DDR5. System half: GO if trace replay shows >= %.0f%% of bytes known >= one lap (0.64 us) ahead." % (
          pk["n_sheet"], pk["full_well"], c_dfe, 1 - c_dfe, p_req, nogo if nogo else float('nan'), nogo_cost if nogo_cost else float('nan'),
          100 * (1 - (V("l_avg_ns") - V("t_hit_ns")) * 1e-9 / (V("lap_stages") / V("f_stage_hz") / 2))))
    p()
    p("Headline: %.2f Gb/mm^2 user (%.1fx 1-beta), ~$%.2f/GB (%.2fx vs DDR5; >1 = cheaper), %.0f e- packets (%.0f mV at the FD, %.0f e- noise), "
      "~%.2f pJ/bit core read, scrub power ~%.0fx below DDR5 refresh, and a minimum CTE of %.4f (DFE) / %.4f (no DFE) at %d transfers." % (
          dens, dens / V("d1b_gb_mm2"), c_cr, V("ddr5_usd_gb") / c_cr, n_s, pk["sig_mV"], V("sigma_read_e"),
          e_bit / 1000, ref_w / scrub_w, c_dfe, c_nodfe, n_t))
    p()
    c_ow = cte_min(194, n_s, p_req, True)
    c_rtn = rtn_base[0] if rtn_base else float('nan')
    p("**RED-TEAM GO/NO-GO additions.** (1) GO line for the base (joint) topology stays at median CTE >= %.4f (DFE, Gaussian); "
      "with the RTN tail at eta 2.8 mV and a 25 e- screen it is %.4f. Without the joint tier (one-way 64-stage fallback) "
      "the GO line is %.4f, i.e. the old STRONG-GO region. (2) Sense-node RTN: measured 1e-9 per-read step quantile "
      "<= 30 e- after sparing <= 2%% of >= 1e4 nodes, at the real 2-5 ns CDS interval. (3) Buried vs surface deferral >= 3x "
      "at matched 4.5e12 cm^-2 on the overlapping-gate reference, with an XPS-measured dEc >= 0.5 eV. (4) Density GO is "
      ">= 2.5x 1-beta; the cost claim is withdrawn (section 11)." % (c_dfe, c_rtn, c_ow))
    p()

    # ---------------------------------------------------------------- 13 budget roll-up
    p("## 13. Seed budget roll-up (CHARGE-RIVER standalone, 24 months)")
    p()
    # RED-TEAM revised budget (old total $990k): adds overlapping-gate reference level (RT-PROC-05), RTN node array at the real
    # CDS interval (RT-CIRC-04, RT-DEV-02), ALD composition-vs-depth + XPS offsets (RT-DEV-01/-03, RT-PROC-06), a 12-plate
    # vertical coupon (RT-IND-04, RT-DEV-04), professional FTO (RT-IND-01) and per-plate cost check (RT-PROC-04); run 2 merged
    # into the vertical-coupon run, contingency cut.
    budget = [
        ("Founder salaries, 2 x 24 months lean, incl. payroll tax", 330e3, "ESTIMATE"),
        ("CCD/device advisor (ex-Lincoln/LBNL/Teledyne-class), ~10% time", 40e3, "ESTIMATE"),
        ("University nanofab fees: ~1,200 h blended ~$140/h (was 1,400 h; run 2 merged with coupon run)", 170e3, "Penn 2025 industry: door $66-77/h, tools $0-495/h, staff $150/h (https://www.nano.upenn.edu/resources/fee-structure)"),
        ("E-beam lithography for 25-50 nm gates/gaps and coupon contacts, ~140 h", 35e3, "ESTIMATE: ~$250/h industry e-beam"),
        ("Wafers, ALD precursors, oxide targets, masks (+ overlapping-gate level, composition corners)", 50e3, "ESTIMATE; RED-TEAM RT-PROC-05, RT-PROC-06"),
        ("National-lab user time (Argonne CNM ALD/XPS band offsets, LBNL TEM/EDX of high-AR coupons)", 25e3, "ESTIMATE; RED-TEAM RT-DEV-01, RT-DEV-03"),
        ("High-aspect-ratio conformality test chips for multi-cation ALD (AR 40-80 equivalent)", 5e3, "ESTIMATE [UNVERIFIED vendor pricing]; RED-TEAM RT-PROC-06"),
        ("12-plate vertical CCD coupon (W or Mo/SiO2 stack, ~250 nm holes, buried heterochannel)", 50e3, "ESTIMATE; RED-TEAM RT-IND-04, RT-DEV-04"),
        ("RTN node array: >=1e4 oxide FD-SF cells with on-die oxide sample-and-hold at 2-5 ns CDS", 15e3, "ESTIMATE; RED-TEAM RT-CIRC-04, RT-DEV-02"),
        ("Test hardware: >=200 MHz 4-ch pattern gen (used), charge amp + digitizer, FPGA, hot/cold chuck access", 85e3, "ESTIMATE"),
        ("sky130 readout/regenerator/DFE test chip (ChipFoundry slot)", 15e3, "~$15k per 100 chips (https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/)"),
        ("Packaging, PCBs, wire bonding", 12e3, "ESTIMATE"),
        ("Trace-driven SOAP simulator: GPU time for vLLM/SGLang trace capture", 12e3, "ESTIMATE (software written by the founders)"),
        ("Per-plate cost check (NAND reverse-costing report or ex-NAND cost engineer)", 5e3, "ESTIMATE; RED-TEAM RT-PROC-04"),
        ("IP: 3 US provisionals + 1 PCT", 40e3, "ESTIMATE"),
        ("Professional FTO/patentability search on imec / SEL oxide-CCD filings, before provisionals", 20e3, "ESTIMATE; RED-TEAM RT-IND-01"),
        ("Legal, accounting, insurance", 28e3, "ESTIMATE"),
        ("Travel (IEDM, IMW, imec/Lincoln visits)", 12e3, "ESTIMATE"),
        ("Contingency", 45e3, "~5% of the above (cut from $80k)"),
    ]
    tot = sum(b[1] for b in budget)
    table(["item", "USD", "basis"], [[b[0], "$%.0fk" % (b[1] / 1e3), b[2]] for b in budget] + [["**TOTAL**", "**$%.0fk**" % (tot / 1e3), "must be < $1,000k: %s" % ("OK" if tot < 1e6 else "OVER")]])

    # ---------------------------------------------------------------- 14 RED-TEAM summary
    p("## 14. RED-TEAM REVISIONS (old -> new, objection id)")
    p()
    table(["input", "old", "new", "objection(s)"], [["`%s`" % k, str(o), str(n), ids] for k, o, n, ids, _ in RT_REVISIONS])
    d_old = density_original(64)
    c_old = (1200.0 + 10.0 * 198 + 1800.0 + 300.0) / (d_old * good_area_mm2() * V("yield_rel") / 8.0)
    c_ow = cte_min(194, n_s, p_req, True)
    table(["headline", "pre-red-team", "post-red-team (joint, base)", "post-red-team (one-way fallback)"], [
        ["user density", "%.2f Gb/mm^2 (%.1fx)" % (d_old, d_old / V("d1b_gb_mm2")), "%.2f Gb/mm^2 (%.1fx)" % (dens, dens / V("d1b_gb_mm2")),
         "%.2f Gb/mm^2 (%.1fx)" % (density_gb_mm2(64, 200, "oneway"), density_gb_mm2(64, 200, "oneway") / V("d1b_gb_mm2"))],
        ["$/GB (x vs DDR5)", "$%.2f (%.2fx)" % (c_old, V("ddr5_usd_gb") / c_old), "$%.2f (%.2fx)" % (c_cr, V("ddr5_usd_gb") / c_cr),
         "$%.2f (%.2fx)" % (usd_per_gb(density_gb_mm2(64, 200, "oneway"), 200, "oneway"),
                            V("ddr5_usd_gb") / usd_per_gb(density_gb_mm2(64, 200, "oneway"), 200, "oneway"))],
        ["min median CTE (DFE)", "0.9970 (8 e-, 98 transfers)", "%.4f Gaussian / %.4f incl. RTN screen" % (c_dfe, rtn_base[0] if rtn_base else float('nan')),
         "%.4f (194 transfers)" % c_ow],
        ["buried + fat-zero deferral factor", "0.18", "%.2f" % ((1 - V("f_it") * V("eta_buried")) * V("eta_fz")), "same"],
        ["energy per useful bit vs HBM3", "0.072 pJ core (no I/O)", "%.2f pJ streaming, %.2f-%.2f pJ with 0.5-2%% random, incl. I/O (~%.1f-%.1fx better)" % (
            e_stream, (1 - V("random_share_dense")) * e_stream + V("random_share_dense") * e_rand,
            (1 - V("random_share_moe")) * e_stream + V("random_share_moe") * e_rand,
            V("hbm3_pj_bit") / ((1 - V("random_share_moe")) * e_stream + V("random_share_moe") * e_rand), V("hbm3_pj_bit") / e_stream), "same"],
        ["refresh/scrub power vs DDR5", "~191x lower", "~%.0fx lower" % (ref_w / scrub_w), "same"],
        ["seed budget", "$990k", "$%.0fk" % (tot / 1e3), "same"],
    ])
    p("Model exits 0. Responses to all 19 objections: research/redteam/responses_charge-river.json.")
    p()

    text = "\n".join(OUT)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(root, "research", "stage3", "charge-river_model_output.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(text + "\n")
    print(text)
    print("\n[wrote %s]" % out_path)


if __name__ == "__main__":
    main()
