# Concept card JSON schema (Phase 2)

Each ideation agent writes `$RV/research/phase2/<branch-key>.json`:

```json
{
  "branch_key": "A1",
  "branch": "A",
  "scope": "short description of the sub-space covered",
  "cards": [
    {
      "tmp_id": "A1-01",
      "name": "Short distinctive name",
      "branch": "A|B|C|D|E",
      "subbranch": "e.g. Oxide-semiconductor DRAM",
      "materials_sense": "a-material|b-process|c-capital|none|mixed:a+c   (mission rule 5: which kind of 'cheaper' this exploits)",
      "what_it_is": "2 sentences, concrete: named material, process, fab/line or partner, product form factor.",
      "why_it_could_work": "the mechanism or the arbitrage, with numbers where possible",
      "evidence": [
        {"title": "...", "url": "https://...", "type": "peer-reviewed|conference|patent|industry|company|government|news", "date": "YYYY[-MM]", "shows": "what it demonstrates and at what scale"}
      ],
      "trl": 1,
      "capital_tier": "T0|T1|T2|T3|T4",
      "time_to_first_revenue_months": 18,
      "time_to_first_revenue_text": "e.g. 12-18 months (pilot module sales to X)",
      "gross_margin_estimate": "e.g. 35-50%",
      "gross_margin_mid_pct": 42,
      "us_manufacturability": "where, with whom, at what node/line — named facility",
      "who_is_already_doing_this": "named companies / labs",
      "wins_axis": "the axis it wins on, e.g. standby W/GB",
      "buyer": "the named workload or buyer type that pays for that axis",
      "survives_glut": "yes|no|partially",
      "glut_reason": "why, given DDR5 falls 60% in 2028-29",
      "fatal_flaw": "the single most likely killer",
      "rule1_status": "SUPPORTED|UNSUPPORTED",
      "business_model_lenses": "which of: fabless->foundry, IP licensing, module/appliance, recert/brokerage, SaaS, data product, defense-first, university/lab patent license",
      "founder_fit_note": "one line: can a software builder with <$50k and a day job start this?",
      "possible": "yes|marginal|no — one line",
      "profitable": "yes|marginal|no — one line",
      "doable_by_founder": "yes|marginal|no — one line"
    }
  ]
}
```

Rules:
- At least **10 cards** per branch. Every card names a concrete material/process, a fab/line or partner, a buyer, and at least one source URL.
- A card may honestly carry `rule1_status: UNSUPPORTED`. Include tempting-but-dead ideas so the kill is recorded with a reason; it will be killed in Phase 3.
- No two cards in your file may be the same idea under different names.
- Validate the file with `python3 -c "import json;json.load(open('<path>'))"` before you finish.
