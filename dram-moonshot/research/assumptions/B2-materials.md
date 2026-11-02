# Assumptions: B2-materials (Phase B, lens: new materials & low-resource fabrication)

Agent key `B2-materials`. Written 2026-11-01. These feed `research/models/B2_materials_estimates.py` and `research/phaseB/B2-materials.json`.

## Network and evidence
- [B2-materials] I used 15 of my 15 WebSearch calls and no WebFetch. Every web fact comes from a search snippet and is tagged "(via search snippet)" in `research/sources/B2-materials.jsonl` (47 entries). Basis: the task's network rules.
- [B2-materials] Evidence entries tagged `[CROSS-REF]` in the JSON (Kioxia OCTRAM and 3D OCTRAM, IMECAS 3 b/cell, imec 300 nm W2W bonding, Samsung 4F² VCT, TechInsights Cs, ECS SrTiO3, SK hynix 56.1% yield) come from the Phase A logs (A1-scaling, A3-frontier). I did not re-open them, so they are not in my source log. Basis: MISSION rule 4, reuse rather than redo.
- [B2-materials] Where a search summary gave several candidate URLs for one fact, I picked the most likely one and wrote the attribution uncertainty into the `shows` field: the Masuda 40–500 nm interval (MRS-J vs ECS MA-201), the doped-SnO2 patent (US 2023/0102906 vs US 12,356,643), and the IDW 2025 Te-oxide CMOS abstract (AMD2-04 vs AMD1-01). Basis: never invent a citation.
- [B2-materials] Prior-knowledge facts with no URL are tagged [UNVERIFIED-PK]: OCTRAM's transistor-over-capacitor order; SIS invented at Argonne; DSA-made imprint masters in bit-patterned media; Canon NIL R&D in Austin TX; fluorinated NIL release layers; world tin output ~300 kt/yr; Nb ~90% Brazilian; a-C hardmasks etched with O2/COS in 3D NAND; perovskite BST DRAM programs abandoned in the 2000s; 300 mm CTE-matched glass carriers commercially available.

## Model inputs
- [B2-materials] Reference anchors are reused unchanged: 1-beta die 0.447 Gb/mm², $3,800 wafer, $1.48/GB, 1c wafer $4,300, EUV $165/wafer/layer, fleet 22.2M wafers/yr, 3.3 m² capacitor area per wafer. Basis: ram-venture `dram_cost_stack.py` and A1/A2.
- [B2-materials] Capacitance uses A1's cylinder formula C = 3.9·ε0·π·d·h/EOT. It reproduces A1's 5.4 fF for the 1-beta pillar (5.38 fF). Basis: consistency with A1.
- [B2-materials] AAO cup capacitor: pore 26 nm at 40 nm pitch, 3 nm TiN liner, ~5 nm dielectric, mid-plane diameter 15 nm, EOT 0.55 nm. Basis: geometry judgment. Porous-AAO skeletal density 3.0 g/cm³; anodization at 15 V; 3 e⁻ per Al.
- [B2-materials] A 40 nm AAO interval is reachable with imprint pretexturing. Basis: snippet says "typically 40–500 nm". The 32–35 nm 1-beta/1c pitches are treated as unproven.
- [B2-materials] Rutile TiO2 is 7 nm thick with k 68 (Gordon 2010), 80 or 100 (patent range 60–100). Doped SnO2 electrode 5 nm, density 6.95 g/cm³, 15% ALD precursor utilization (A2 convention).
- [B2-materials] Dielectric leakage budget is evaluated at the stored bias over the capacitor's sidewall area and compared to A1's tail-cell budgets (13 fA, 0.84 fA, 0.084 fA). Basis: A1 §3. This ignores local thin-spot tails, which would tighten the spec.
- [B2-materials] Hf-free MPB card uses k 56 at 5.9 nm (KAIST bilayer value, which contains Hf) as the *target* for a Zr-only stack. Basis: no Hf-free MPB number was found; the 2026 overestimate caveat is carried into the card.
- [B2-materials] Perovskite k 100–250 at 10–12 nm, pillar d = 22 nm at 40 nm pitch. Basis: judgment within thin-film BST/STO ranges [UNVERIFIED-PK].
- [B2-materials] EDL specific capacitance 10–20 µF/cm² (double layer) and ~100 µF/cm² (pseudocapacitive); electrolyte 5 nm; ionic conductivity 1e-5 to 1e-3 S/cm. Basis: textbook ranges [UNVERIFIED-PK]; MIT's ns proton motion was at ~1 V/nm, far above storage fields.
- [B2-materials] AlBN: Pr 130 µC/cm², Ec 5.4 or 3.0 MV/cm (snippets); sub-5 nm switching is unproven.
- [B2-materials] Read bitline 0.1 fF/cell + 5 fF; ZTO read current 0.2 µA (~1/3 of IGZO), IGZO 0.6 µA; 3-bit sensing 8× the 1-bit time. Basis: A3 conventions, ZTO derating is my judgment.
- [B2-materials] Oxide TFT σ(Vt) = 40 mV for a minimum-size SA pair. Basis: judgment for amorphous-oxide TFTs at ~100 nm; it drives the conclusion that offset cancellation is mandatory.
- [B2-materials] Vertical 2T0C footprint 10F², array efficiency 0.508 (A3) or 0.70 with CMOS-under-array or periphery-under-cell (A1).
- [B2-materials] Memory-on-logic tier cost $500/tier/wafer and 80% memory yield. Basis: ~12.5% of a DRAM wafer (A2/A3 convention) applied as an absolute cost on a logic line; logic-line overheads could raise it.
- [B2-materials] Trailing-node line: base wafer $1,300 (ram-venture depreciated DDR4 line), tier cost $80 (depreciated tools, my judgment) or $162.5 (A2/A3 12.5% convention). Both are reported.
- [B2-materials] BEOL-only cell line capex = 30–40% of a DRAM greenfield ($145–170k/wpm). Basis: judgment that furnaces, implant, epi, EUV and most immersion litho are absent; this is the weakest number in B2-17.
- [B2-materials] Reusable glass carrier: 10–50 reuses. Basis: judgment from temporary-bonding practice [UNVERIFIED-PK].
- [B2-materials] Defect-tolerance calc assumes independent random cell defects, SECDED (136,128) and BCH t=2 (144,128) on 128-bit words, 17.2e9 physical bits per 16 Gb die. Basis: standard binomial approximation; clustered defects are handled by sparing, not ECC.
- [B2-materials] Panel: Gen 3.5 = 620×750 mm, 80% usable, F = 50–100 nm imprint. Basis: WGP imprint at 100–200 nm pitch; sub-100 nm panel imprint was not found.
- [B2-materials] BCP lamellae L0 25–40 nm, 1–2 µm films. Basis: typical PS-b-PMMA ranges [UNVERIFIED-PK].
- [B2-materials] Interface energy for memory-on-logic: 3.5 pJ/bit (HBM, A1) → 0.2 pJ/bit (≤1 mm wire, A1 floor table).

## Judgment calls
- [B2-materials] Ideas are judged on physics only (MISSION). Cards with large endurance or tool gaps (B2-06 AlBN, B2-19 panel, B2-20 BCP tiers, B2-05 EDL) are kept with their show-stoppers stated, not killed, because no law of physics forbids them.
- [B2-materials] I wrote a model file (`research/models/B2_materials_estimates.py`) in addition to the files named in the task, following MISSION rule 2 ("put reusable estimates in Python under models/"). It touches no other agent's file.
- [B2-materials] "Most exciting" ranking weighs size of step change × physics plausibility × small-team provability: B2-16, B2-01, B2-18 (with B2-13 as runner-up).
