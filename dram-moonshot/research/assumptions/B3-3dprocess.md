# Assumptions: B3-3dprocess (Phase B, lens: 3D integration & process innovation)

Agent key `B3-3dprocess`. Written 2026-11-01. These numbers feed `research/models/B3_3dprocess_estimates.py` (stdlib; `python3` exits 0) and the cards in `research/phaseB/B3-3dprocess.json`.

## Network and evidence
- [B3-3dprocess] I used 15 of my 15 WebSearch calls and made no WebFetch calls. Every web fact is a search snippet, logged with "(via search snippet)" — basis: task network rules.
- [B3-3dprocess] Where one snippet summarized several results, I logged the most likely URL and wrote "attribution within result set uncertain" in `supports`. This applies to the CEA-Leti 400 C IEDM 2025 result, the Tom's Hardware CoWoS areas, the Delft grain sizes and the Celestial AI module figures — basis: search summaries did not always tie each fact to one link.
- [B3-3dprocess] Phase A/B URLs reused without re-opening are tagged `[CROSS-REF from <agent> log]` — basis: CONVENTIONS "never invent a URL"; these were logged by A1, A3 and B2.
- [B3-3dprocess] A novelty label of "not found" means "not found in ≤15 searches plus Phase A maps". It does not mean "does not exist" — basis: search budget.

## Reference anchors (reused, not re-derived)
- [B3-3dprocess] 1-beta: 0.447 Gb/mm² die-level, 1,070 nm² cell, F = 13.4 nm, array efficiency 0.51, $3,800/wafer — basis: A1 table 1; ram-venture dram_cost_stack.py.
- [B3-3dprocess] The sense criterion is A1's: ≥50 mV signal after a 15% droop at VARY 1.06 V, so Cs ≥ 0.156·Cbl. Re-deriving it returns 5.45 fF at 35 fF, matching A1's 5.4 fF — basis: A1 §3–4.
- [B3-3dprocess] Pillar capacitance is C = 3.9·ε0·π·d·h/EOT, with d = 21 nm and EOT 0.55 nm, giving 4.14 aF per nm of height — basis: A1 §2.
- [B3-3dprocess] HBM is 3.5 pJ/bit and streaming activation is 0.18 pJ/bit — basis: A1 §7–8.
- [B3-3dprocess] Refresh costs 12 mW per 16 Gb at 64 ms, and retention halves per ~10 °C — basis: A1 §3.
- [B3-3dprocess] Each oxide tier costs 12.5% of a 1-beta wafer ($475); I use $100 for NAND-like single-etch tiers and $200 for interposer tiers as the low end — basis: A2/A3 convention; NAND-style single-etch tiers should be far cheaper than sequential BEOL tiers [judgment].
- [B3-3dprocess] Base wafer cost relative to 1-beta is 0.55 at F = 40 nm and 0.90 at F = 20 nm (A3); I interpolated 0.70 at F = 30 nm — basis: A3 §3.3 plus my interpolation.
- [B3-3dprocess] Array efficiency is 0.70 when sense amps and decoders sit under the array (CMOS-under-array or bonded) — basis: A1 §5 table (PUC 0.70).

## B3-01 MSB-DRAM
- [B3-3dprocess] Bitline load is 0.060 fF per cell, from (35 − 8 fF)/(512 − 64 cells) — basis: A1 bitline table.
- [B3-3dprocess] Global bitline wire is 0.15 fF/µm (pessimistic 0.25). Each off pass-switch junction is 0.05 fF. The bond pad is 1.0 fF (pessimistic 2.0) and the SA input is 1.5 fF (pessimistic 2.0) — basis: typical BEOL wire and junction capacitances [judgment].
- [B3-3dprocess] Along the bitline the WL pitch is 2F, so a 64-cell segment is 1.72 µm long — basis: 6F² = 2F × 3F convention.
- [B3-3dprocess] The stub capacitor saves $150 per cell wafer. The periphery wafer costs $1,800–3,000 (40/28 nm logic) and bonding $200 — basis: [judgment]; the trailing-node logic wafer price is [UNVERIFIED-PK].
- [B3-3dprocess] A ~10-transistor offset-cancelled sense amp fits in 1.1 µm² at 28–40 nm — basis: a 28 nm 6T SRAM bit is ~0.12 µm² [UNVERIFIED-PK].

## B3-02 Carrier-is-memory
- [B3-3dprocess] The logic die is 800 mm², with 60 gross dies per wafer and 50–70% logic yield — basis: reticle-class accelerator [judgment].
- [B3-3dprocess] Removing pads, PHY and TSVs raises DRAM array efficiency from 0.51 to 0.60 — basis: [judgment].
- [B3-3dprocess] Each bond hop is 12 fF at 0.75 V with activity 0.5; on-die movement adds 0.10 pJ/bit (0.5 mm at 0.2 pJ/bit/mm) — basis: A1 wire energies.
- [B3-3dprocess] A blank carrier wafer costs ~$120 — basis: [UNVERIFIED-PK].
- [B3-3dprocess] BSPDN carrier bonding happens after front-side metallization, so the memory wafer never sees FEOL temperatures — basis: SemiEngineering / imec snippets.

## B3-03 Coolant-backed memory
- [B3-3dprocess] The accelerator dissipates 1 kW over 8 cm². The microchannel heat-transfer coefficient h is 5e4–2e5 W/m²K. The memory has 50 µm of Si and 5 µm of BEOL at 3 W/mK — basis: [judgment]; Microsoft reports ~3x better removal than cold plates.
- [B3-3dprocess] Hot spots run at 3–5x the mean flux — basis: [judgment].

## B3-04 Coaxial 4F² 2T0C
- [B3-3dprocess] The storage-node core is 20 nm in diameter and 150 nm tall, with EOT 2 nm — basis: IMECAS 4F² cell has 120 nm channel height and 6 nm IGZO (Tom's Hardware snippet) [judgment].
- [B3-3dprocess] Read current is 10 µA/µm at L = 150 nm and 1 V overdrive — basis: scaled down from CXMT's 60.9 µA/µm at short L (A3).
- [B3-3dprocess] The write-wordline-to-storage-node coupling is 0.005–0.015 fF and the wordline swings 2.5 V — basis: [judgment].
- [B3-3dprocess] The total node leakage range is 10 zA–1 aA — basis: A3 §3.1 infers 7–200 zA from measured cells.

## B3-05 Mirror-VCT
- [B3-3dprocess] The backside VCT plus capacitor module adds 35–45% to the cell-plus-periphery stack cost — basis: [judgment].
- [B3-3dprocess] The overlay budget is ~F/4 — basis: a common DRAM rule of thumb (B2 cites 15–20% of half-pitch).

## B3-06 Dopant-contrast superlattice
- [B3-3dprocess] Boron lattice-contraction coefficient β ≈ 5.2e-24 cm³/atom — basis: [UNVERIFIED-PK] (literature values ~4.5–6.3e-24).
- [B3-3dprocess] The Si–Ge lattice mismatch is 4.18% (Vegard) — basis: [UNVERIFIED-PK].
- [B3-3dprocess] Intrinsic boron diffusion follows D = 0.76·exp(−3.46 eV/kT) cm²/s — basis: textbook [UNVERIFIED-PK].
- [B3-3dprocess] HNA (1:3:8) etches heavily doped Si far faster than intrinsic Si, and anodization porosifies p+ selectively. The ≥100:1 selectivity requirement is mine — basis: MEMS/SOI practice [UNVERIFIED-PK]; my search did not confirm a number.

## B3-07 Graded tier stack
- [B3-3dprocess] The recess rate drops 25% from top to bottom over a 4 µm deck — basis: [ASSUMPTION]; Lam says only that recess "varies" (SemiEngineering), and no number was found.
- [B3-3dprocess] The recess is 600 nm with 60 nm spacing — basis: A1 base 3D footprint (50 × 600 nm).
- [B3-3dprocess] Lateral ALE removes 0.5 nm/cycle — basis: [UNVERIFIED-PK].

## B3-08 Tier decoder
- [B3-3dprocess] Each staircase step is 0.5 µm wide — basis: [UNVERIFIED-PK]; 3D NAND practice.
- [B3-3dprocess] Select gates sit at 0.2 µm pitch with ~2 kΩ each (W ~1 µm oxide TFT); the line capacitance is 50 fF — basis: [judgment].
- [B3-3dprocess] A coarse coding mask costs $5–10 per wafer per layer — basis: [UNVERIFIED-PK]; i-line/KrF cost.

## B3-09 Sandwich stack and B3-22 sequential periphery
- [B3-3dprocess] On a vertical bitline each cell adds 0.08 fF and the wire adds 0.2 fF/µm; the SA input is 0.5 fF — basis: [judgment], scaled from A1/A3.
- [B3-3dprocess] The in-tier MIM capacitor has a ~160 nm effective perimeter at EOT 0.55 nm — basis: a 40 × 40 nm cross-section with both faces counted [judgment].
- [B3-3dprocess] The per-tier footprint with a ~60 nm capacitor is 50 × 200 nm — basis: transistor ~100 nm + capacitor 60 nm + contact 40 nm [judgment].
- [B3-3dprocess] Each tier costs $30–45 (A1 3D range) and each sense layer (Smart Cut plus 400 °C CMOS) $400–700; the base wafer is $2,000 — basis: [judgment]; no vendor price found.
- [B3-3dprocess] The Smart-Cut hydrogen dose is ~5e16 cm⁻² — basis: [UNVERIFIED-PK] (typical 3e16–1e17).
- [B3-3dprocess] Replacing the hybrid-bond pad with a litho via saves ~2 fF (B3-22). A ~10-transistor latch needs 0.2–0.3 µm² at a 28 nm-class rule — basis: [judgment].
- [B3-3dprocess] CEA-Leti 400 °C devices are 2.5 V I/O-class, not dense logic — basis: snippet wording "2.5 V n&p SOI MOSFETs".

## B3-10 Laser single-grain Si
- [B3-3dprocess] 60% of the area lies inside usable grains; floating-body cells take 10F² at F = 40 nm — basis: [judgment]; grain pitch 3–7.5 µm (Delft snippets).
- [B3-3dprocess] SiO2 thermal diffusivity is 8.6e-7 m²/s, the pulse ~100 ns, and p-oxide mobility ~15 cm²/Vs — basis: [UNVERIFIED-PK]; B2-08 cites p-TeSeOx ~15.

## B3-11 Memory interposer
- [B3-3dprocess] The monolithic Si interposer is 2,700 mm² (CoWoS-S-class, ~3.3 reticles) or 4,719 mm² (5.5x); 65% is usable for memory; a wafer yields 16 interposers — basis: TrendForce / Tom's Hardware snippets for 5.5x; 3.3x [UNVERIFIED-PK].
- [B3-3dprocess] A micro-bump hop costs 0.05–0.1 pJ/bit — basis: [judgment].

## B3-12 Photonic periphery
- [B3-3dprocess] Each die has 8 fibers × 16 wavelengths × 32 Gb/s; each ring needs 2–5 mW of tuning — basis: [judgment]; Celestial AI's link energy figures are company claims.
- [B3-3dprocess] GlobalFoundries offers monolithic photonics CMOS in Malta NY — basis: [UNVERIFIED-PK]; no search result mentioned it.

## B3-13/14/15/19 TSV-free stacks
- [B3-3dprocess] Coils sit at 50 µm pitch. TSV keep-out plus TSV/bump yield loss make up 33–50% of the HBM ~3x wafer tax — basis: [ASSUMPTION]; TrendForce gives die +35–45% and yield −20–30% without splitting causes.
- [B3-3dprocess] Sidewall wires sit at 4–8 µm pitch with adaptive patterning; on-die routing to the edge averages 5 mm at 0.05–0.2 pJ/bit/mm — basis: [judgment]; A1 wire energy.
- [B3-3dprocess] The origami membrane is 1.5–3 µm thick with a 0.5% strain limit at folds; the adhesive is 2 µm at k = 0.2 W/mK — basis: [judgment]; the BEOL dielectric strain limit is [UNVERIFIED-PK].
- [B3-3dprocess] An HBM TSV is 6 µm with 5 µm keep-out; a thin-wafer TSV is 1.5 µm with 1 µm keep-out. Die-site yield is 0.90–0.98 after in-die repair — basis: [UNVERIFIED-PK]; WOW snippets give 4–10 µm wafers.

## B3-16 Yield firewall
- [B3-3dprocess] A die has 1,000 blocks; defects are independent per block-tier; die-to-wafer bond yield is 99.5% per group bond — basis: [judgment].

## B3-17 Hydrogen-lean mold
- [B3-3dprocess] Atom density is 8e22 cm⁻³ for PECVD SiN and 9.3e22 for LPCVD SiN, and 6.6e22 for oxide. H content is 20% (PECVD SiN), 4% (LPCVD SiN) and 3% (PECVD TEOS) — basis: [UNVERIFIED-PK].
- [B3-3dprocess] The channel has EOT 3 nm and a 20 mV Vt budget (3 bits), and each hydrogen atom that reaches the channel is one donor — basis: A3 §5-1 (≤~20 mV drift for 3 bits); worst case [judgment].
- [B3-3dprocess] LPCVD rates are 2.5 nm/min (SiN) and 8 nm/min (oxide), with 5 min per gas switch and 150 wafers per batch — basis: [UNVERIFIED-PK].

## B3-18 Bonus tiers
- [B3-3dprocess] 15% of the base die area goes to bonus-tier sense and write-verify circuits — basis: [judgment].

## B3-20 Cold bonding
- [B3-3dprocess] Each sequential bond anneals 2 h at 350 °C. IGZO stress/recovery barriers (0.58–0.72 eV, CPB 2015) are used as a proxy for thermal-only drift — basis: the proxy is a judgment; bias-free thermal drift may follow different kinetics.

## B3-21 Grow-the-hole
- [B3-3dprocess] Each tier adds 30 nm; the selectivity window is ~100 nm per cycle (Saraswat 1984 via US 4,741,928); stray nuclei appear at 0.01–0.1/cm² per layer — basis: the snippet for the window; [judgment] for the nuclei density.

## Judgment calls
- [B3-3dprocess] I killed nothing for business reasons; the rejected ideas in the notes failed on physics or arithmetic, and each carries a revival condition — basis: MISSION framing.
- [B3-3dprocess] Where a card overlaps B1/B2 (B3-04 vs B1-06, B3-18 vs B2-16, B3-09/10/22 vs B2-08), I kept it only when the mechanism or host differs — basis: dedup against sibling lenses.
- [B3-3dprocess] Energy claims for optical (B3-12) and inductive (B3-13) links are stated as parity or worse, not as wins — basis: Celestial AI 3.1 pJ/bit and Shiba 0.7 pJ/bit/hop vs A1's TSV 0.15 pJ/bit/layer.
