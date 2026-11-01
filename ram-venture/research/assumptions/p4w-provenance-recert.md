# Assumptions: p4w-provenance-recert (DD1 deep-dive writer), 2026-11-01

All model inputs are the research agent's (`research/assumptions/p4-provenance-recert.md`; INPUTS in `models/provenance-recert.py`). No WebSearch was used. Every URL in `04_DEEPDIVES/provenance-recert.md` was checked against `research/sources/*.jsonl`, so no new sources were logged. The judgment calls below are mine.

- [p4w-provenance-recert] Verdicts are POSSIBLE yes / PROFITABLE marginal / DOABLE yes — basis: m§3–m§6. 85% of BASE revenue is 15%-GM recert, ARR at m36 is $434–446k across decks, and CleanBOM close rate, churn and the ITAD buy fraction are all unmeasured.
- [p4w-provenance-recert] Variant runs (early turn `turn_month=12`; `buy_frac=0.75` in GLUT; CleanBOM close = 0; `_cb_delay=6` in GLUT; `_close_mult=0.7` with the slip) use `simulate()`/`metrics()` from the unmodified model — basis: these stress combinations are not printed by the model. The reproduction command is in §2.6 of the deep dive.
- [p4w-provenance-recert] Full-time gate adds ">= 5 paying CleanBOM subscribers" to the model's EBITDA >= $12k and cash >= $25k trigger. The model does not include this condition — basis: in the GLUT + 6-month FAR-slip variant the founder quits in Dec-27 and is back at the day job by Feb-28.
- [p4w-provenance-recert] Kill track C requires at least one of the three commitments to be cash (a $900 pack or a prepaid pilot) — basis: an LOI costs the buyer nothing.
- [p4w-provenance-recert] Kill track B passes only if the die source is identified on at least 3 of 4 samples. Its cost ($600/sample) and time (15 business days) lines are carried from the notes §9.
- [p4w-provenance-recert] Intermediate kill lines are my settings, set at or just below the model path (m§2 BASE): m6 trailing recert contribution 12% (model 15%) and 150 modules (model 155); m12 at least 1 subscriber plus 3 packs (model 1.5 subscribers); m18 at least 7 subscribers (model 7.5; must-be-true 10).
- [p4w-provenance-recert] Glut stop-line of a 32GB DDR4 at ~$69 = $125 x 0.55. This is the index at which GLUT lot buying collapses in m§2 (Sep-28).
- [p4w-provenance-recert] PMem buying continues past 2027-09-30 only if trailing contribution from non-VMware buyers is at least 20% — basis: m§1b today GM is 23%; vSphere 8 EoGS is 2027-10-11.
- [p4w-provenance-recert] A US8468422 FTO read costs ~$1–2k — basis: judgment for a single-patent attorney read; not sourced.
- [p4w-provenance-recert] The federal channel advisor is commission-only, so the model carries no fixed cost for the role — basis: keeps the T0 budget intact; not sourced.
- [p4w-provenance-recert] The CleanBOM glut-demand sign is treated as ambiguous. Cheaper Korean and U.S. bits could pull OEMs off CXMT and shrink demand; cheaper CXMT bits could gain share and grow it. The model holds demand flat — basis: Phase 3 scorers argued only the "raises demand" side.
