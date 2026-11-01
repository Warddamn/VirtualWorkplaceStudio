# p5-VC assumptions (Phase 5 red team, VC persona, 2026-11-01)

- [p5-VC] DD1 CleanBOM addressable buyers that cannot rely on an upstream certification ≈ 20–40 compatible-module/white-box builders plus a few hundred SEWP/GSA resellers; 40 × $30k + 300 × $9k ≈ $3.9M at 100% share — basis: DD1 §3 buyer list and $750/$2,500 tiers; no census of these firms exists in the repo.
- [p5-VC] DD1 working-capital gap at m10 ≈ $40k B2B receivables (net-30 on ~55% B2B share of $82.3k recert revenue) + $20–30k held eBay payouts — basis: models/provenance-recert.py BASE m10 row; eBay new-seller hold ~14–30 days and ~10 item/$500 limits (snippets logged in p5-VC.jsonl).
- [p5-VC] Combined income + self-employment tax on pass-through EBITDA ≈ 25–35% — basis: general U.S. pass-through rates; none of the five models provisions tax.
- [p5-VC] DD2 price-driven module removal would cut BASE m36 ARR toward ~$250k — basis: 39% price-driven share of m36 revenue in models/lifecycle-intel.py §6 applied to $421,548.
- [p5-VC] DD3 i-series Fanuc controls (0i/16i/18i/21i) accept CF-in-PCMCIA for SRAM backup; pre-i controls are the ones needing true SRAM cards — basis: IMD 0i-Mate CF backup procedure and Memex 16/18-B/C manual (snippets); not confirmed against a Fanuc maintenance manual.
- [p5-VC] DD4 credible 1-hour-response kernel on-call costs "several thousand $/month" — basis: judgment; $750/month buys ~4 h at the model's $175/h.
- [p5-VC] DD5: 204 of 298 funnel projects rest on estimates (150 pure ESTIMATE rows + 54 from an estimated second wafer.space run/yr) — basis: models/open-memory-ip.py INPUTS.
