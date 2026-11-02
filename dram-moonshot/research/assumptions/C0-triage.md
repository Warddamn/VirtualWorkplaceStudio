# C0 triage: assumptions and judgment calls

Agent key: `C0-triage` (lead device physicist). Written 2026-11-01. Arithmetic: `research/models/C0_triage_checks.py` (python3 exits 0). Web: 5 of 5 searches used, no fetches. Every web fact is a search snippet.

## Verdict rules
- [C0-triage] **ALIVE** means every physical effect the idea needs has been shown somewhere, at or within about 10x of the needed size. What remains is integration, yield, uniformity, or measuring a parameter that theory gives no reason to fear. — basis: MISSION.md says kill only on physics; this keeps engineering risk out of the verdict.
- [C0-triage] **ALIVE-SPECULATIVE** means at least one needed effect is either contested in the literature or not shown within about 100x of the needed size. The triage_reason names that effect, and revival_condition gives the measurement that would promote the idea to ALIVE. — basis: the task asks us to "say exactly which".
- [C0-triage] **DEAD-PHYSICS** is used only when the main claim breaks a physical bound, or hits a known show-stopper with no plausible way around it. When only part of an idea fails, the idea is not killed: the failing sub-claim or variant is listed under `dead_subclaims`. — basis: the founder's framing (persistence, re-scoping) and the instruction to be fair to bold ideas.
- [C0-triage] For ALIVE ideas, `revival_condition` holds a **kill test** instead: the measurement that would demote the idea. That makes the field useful for Phase C. — basis: judgment call.
- [C0-triage] Business, market, time-to-revenue and founder fit were ignored throughout. — basis: MISSION.md.

## Merge rules
- [C0-triage] Merged only when the core mechanism and the target are the same. Cards that share a goal but use a different mechanism (for example the short-bitline family B1-04/B3-01/B3-09/B3-22/B2-08/B5-09/B5-10/B1-19) stay separate, tagged with a shared `family`. — basis: Phase C needs to compare alternative mechanisms one against another.
- [C0-triage] Four merges, 101 cards to 97 ideas:
  - B4-14 into B3-12: the same photonic periphery wafer.
  - B5-18 into B3-13: the same inductive-coupling stack. B5-18's reach arithmetic is kept as the physics constraint.
  - B4-13 into B3-03: the same retention-from-cooling physics, with two placements.
  - B2-06 into B1-11: B2-06's own mechanism reads the FE capacitor capacitively through a 2T gain cell, which is B1-11's cell built in AlBN.
- [C0-triage] The primary card keeps all of its original fields. Each absorbed card is kept whole under `absorbed_cards`.

## Physics numbers assumed (all [ESTIMATE] unless cited)
- [C0-triage] **Endurance bar for DRAM-class duty:** 3.2e8 cycles (1 s refresh, 10 years) to 6.9e13 (hot row at 1% duty), and 6.9e15 for a row hammered continuously at tRC = 46 ns. — basis: C0-1.
- [C0-triage] **Amorphous dielectric charge-to-breakdown:** Q_BD = 1–100 C/cm². — basis: B5 notes, rule 1. For ultrathin oxides at low field it can be higher, which is why B1-10 is ALIVE-SPECULATIVE and not dead.
- [C0-triage] **Fowler–Nordheim emission:** standard constants a = 1.5414e-6 A·eV/V² and b = 6.8309 eV^-3/2·V/nm, with the simple Schottky–Nordheim v(f) correction. Emitter work function 4.5 eV for TiN and 2.7 eV for the card's low-work-function case. Emitter area (20 nm)². — basis: textbook FN; C0-3.
- [C0-triage] **Oxide Schottky diode:** Richardson constant A* = 41 A/cm²K² (m* ≈ 0.34 m0, IGZO-class). Floating gate 0.2 fF with a 0.2 V droop budget. — basis: B1-06 card scale; C0-4.
- [C0-triage] **NbO2 switching element:** volumetric heat capacity 3e6 J/m³K. IMT at ~1,080 K. — basis: oxide-typical value; NbO2 transition temperature [UNVERIFIED-PK].
- [C0-triage] **Deep-level emission:** attempt prefactor 1e12–1e13 s⁻¹. — basis: typical σ·v_th·N_c; C0-6.
- [C0-triage] **Pinned well (B5-04):** full depletion of a 40 nm slab needs N = 8εV_pin/(q w²). Si band-to-band tunnelling turns on at ~0.5–1 MV/cm. — basis: depletion approximation; onset field [UNVERIFIED-PK].
- [C0-triage] **Skyrmion shift-error (B5-12):** a thermal back-hop occurs with probability exp(-ΔE/kT). A 1e-12 shift error needs ΔE ≈ 27.6 kT. — basis: C0-8.
- [C0-triage] **Ring-down of a snapped ribbon (B5-01):** amplitude decays with τ = Q/(πf0). Q of 10–1,000 is assumed for nm ribbons. — basis: C0-9; the Q range is [UNVERIFIED-PK].
- [C0-triage] **Rate-distortion (B4-17):** high-rate gaps to R(D) for a Gaussian source are 0.254 b for an entropy-coded uniform scalar quantizer and 0.722 b for an optimal fixed-rate scalar quantizer. LLM weights are treated as roughly i.i.d. Gaussian. — basis: standard quantization theory; C0-10.
- [C0-triage] **Bitline kTC noise:** 35 fF at 358 K gives ~82 e⁻ rms. — basis: C0-11.
- [C0-triage] **Inductive relay energy:** 0.7 pJ/b per hop (the B3-13 figure). HBM path ~3.5 pJ/b. — basis: C0-12.
- [C0-triage] **Fold mechanics (B3-15):**
  - Brittle BEOL tolerates 0.5% strain. A polymer hinge with neutral-plane Cu tolerates 3%.
  - Polyimide conducts 0.2 W/mK.
  - basis: thin-film mechanics [UNVERIFIED-PK]; C0-13.
- [C0-triage] **Boron lattice contraction in Si:** ~5.2e-24 cm³ per atom, used to check B3-06's misfit numbers. — basis: [UNVERIFIED-PK].
- [C0-triage] **AFE ZrO2 endurance:** best seen this session is ~5e9 field cycles for tetragonal-phase ZrO2 (JMCC 2024 supplement) and ~1e8 for a confined 12 nm AFE film (NTU 2026). No 1e11 report was found. — basis: search snippets in `sources/C0-triage.jsonl`.
- [C0-triage] **Wurtzite FE endurance:** best seen is >1e10 cycles in sub-50 nm AlScN (Cho et al., arXiv 2025 preprint). It raises the earlier ~1e6–1e7 benchmark and narrows the gap for the AlBN variant of N-11. — basis: search snippet.
- [C0-triage] **Oxide-semiconductor CCD transfer efficiency:** no published data found. Treated as the open, decisive measurement for B1-08 and, more weakly, B1-03. — basis: negative search result.
- [C0-triage] **Crystalline-barrier lifetime at ~1e11 C/cm²:** no RTD lifetime-versus-current-density data found. B5's premise that crystalline barriers survive DRAM-class fluence stays [UNVERIFIED]. That is why B5-05, B5-06 and B1-20 are ALIVE-SPECULATIVE. — basis: negative search result.
- [C0-triage] **Cylindrical-wire domain walls:** >600 m/s (STT) and ~1 km/s between modulation sites are reported, but with stochastic pinning and with STT, Oersted and Joule effects entangled. Experiments are in wires wider than B5-02's 20 nm [UNVERIFIED-PK on exact diameters]. — basis: search snippets.

## Cross-lens adjudications (judgment calls)
- [C0-triage] **B1 killed the "protonic nano-supercapacitor stub" as thermodynamically contradictory.** I overrule that for B2-05's double-layer version. The contradiction applies to storing information in ion position. An EDL capacitor stores electronic charge on blocking electrodes, and electronic/faradaic leakage sets its retention, not ion mobility. B2-05's pseudocapacitive skin is still dead on faradaic endurance.
- [C0-triage] **B1 killed a pinned-diode storage node** (too few electrons at 30 nm, planar). B5-04's vertical well answers the full-well objection. A new objection, needing ≥1.6e18 cm⁻³ doping at 0.5–1 MV/cm, makes it ALIVE-SPECULATIVE, not dead.
- [C0-triage] **B2 rejected DNA templates on defect rate.** B5-11 is kept ALIVE-SPECULATIVE, because proofreading assembly is not ruled out by physics.
- [C0-triage] **B1 parked the vertical racetrack.** B5-02 is kept ALIVE-SPECULATIVE, because 2019–2023 cylindrical-wire data show fast Bloch-point wall motion.
- [C0-triage] **B3-13 claims 12–16-high inductive stacks; B5-18 says 16-high fails.** Both are right about different things. Direct links fail on coil area. Relayed links work but cost ~6 pJ/b on average at 16-high, so the idea is energy-negative above ~8-high.
- [C0-triage] **B1 killed a passive parallel-FE capacitance canceller.** B5-09's active negative-impedance converter is a different, legitimate circuit (an amplifier), so it is ALIVE.
- [C0-triage] **Cryogenic cards (B5-14 to B5-17) are judged inside their stated scope,** which is cold compute. A3's kill for warm data centres was on system energy, which is not a device-physics verdict.
