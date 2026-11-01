# Assumptions — p3-writer (03_SCORING.md)

- [p3-writer] Kill-rule definitions in 03_SCORING.md §1.1 are reconstructed from how the 14 auditors applied them, because no file defines them in one place — basis: research/phase3/verify/*.json, research/assumptions/p3-audit-*.md.
- [p3-writer] Kill reasons in §2 are condensed from `kill_reason` in concepts_master.json; numbers keep the deck the auditor used ($15.99 / $6.40 / $1.64 per GB), not the live device-model deck — basis: concepts_master.json; device_cost_output.md §5.
- [p3-writer] Concept names in the §2 register drop editorial suffixes such as "(tempting, dead)"; short names are used in §4–§7 tables for width — basis: readability only; ids are unchanged.
- [p3-writer] Per-criterion justifications in §4.1 are condensed from the scores.csv `*_why` text, and the founder is referred to as they/them even where the source text says "he" — basis: task instruction.
- [p3-writer] The "side/feature/lifestyle/SKU/gig/lead-gen/not a venture" flag in §6 is a regex over all three lenses' `one_line_view` text; 12 of the top 15 match — basis: research/phase3/scores_raw/*.json.
- [p3-writer] The 5-year revenue-ceiling bands in §6 are my own estimates, not scores. They are built from card pricing and customer counts (C-64 $1.5–12k/month × 37 customers; C-86 $0.3M ARR; C-80 ~$24k MRR; C-85 25 × $21.6k; C-74 $500–2k/month per 50–200 nodes) and from scorer ceilings (C-12 "low $100ks/yr"; C-33 "<$0.5-1M ARR") — basis: concepts_master.json, scores_raw one_line_view, verify batch_02.
- [p3-writer] C-75 services ceiling assumes ~6–12 engagements per year at $15–40k for a part-time founder — basis: C-75 card ttr text ($15–40k engagement); capacity is my judgment.
- [p3-writer] C-48 revenue band assumes 20–50 boxes per year at ~$25–45k each — basis: the card's DRAM BOM of $15.6–31.2k per box plus CPU/GPU; volume is my judgment.
- [p3-writer] The "commodity software" and "ideal T2 device" profiles in §5 are hypothetical, used only to show the structural bias of the weights — basis: arithmetic with models/scoring.py `weighted()`.
- [p3-writer] The coverage proof uses the union of the three top-10 lists (11 ids), which is stricter than selection.json's wording — basis: scores.csv ranks.
- [p3-writer] All URLs cited in 03_SCORING.md come from auditors' `new_evidence` entries and are [REPORTED] (search snippets), except the VLSIDA GitHub repository, which an auditor opened via git — basis: research/phase3/verify/*.json; logged in research/sources/p3-writer.jsonl.
