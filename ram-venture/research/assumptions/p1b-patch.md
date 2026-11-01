# Assumptions: p1b-patch (2026-11-01)

- [p1b-patch] Phase 1b tally (113 items: 56 confirmed, 28 corrected, 1 refuted, 23 still unverified, 5 new) counts one verdict per verifier-log row. Mixed labels go to the main verdict: "CONFIRMED + CORRECTED" → corrected; "CONFIRMED (X); STILL-UNVERIFIED (Y)" → confirmed; v4 5d "STILL-UNVERIFIED (published); derived CORRECTED" → still unverified; v4 2f "CLARIFIED" → corrected; v3 1d "PASSED" → confirmed — basis: verify_v1..v4 change tables.
- [p1b-patch] Treated the §5949 "reasonable inquiry" standard as moving O1's core product from die-level lab screening to attestation and BOM-traceability workflow, with lab screening as an add-on — basis: verify_v1-policy.md items 1d–1f and note 1.
- [p1b-patch] Moved Weebit-on-S130 entry from T0 to T1 — basis: verify_v2-fabs-ip.md items 1b–1d, 1i and notes 2–3. The fabless-startup fee is unknown, and existing licensees paid an estimated $0.1–2.6M upfront.
- [p1b-patch] Adopted v4-cost's re-run deck as canonical: cost $1.48/GB, contract $20.37/GB, glut $8.15/GB, RDIMM $25.78/$10.31 per user-GB — basis: models/dram_cost_stack.py re-run 2026-11-01, exit 0, output identical to cost_stack_output.md.
- [p1b-patch] Kept the market.md "85–90% fall to the 2023 floor" and added ~92% on the 1b contract deck, i.e. $1.60 / $20.37 — basis: arithmetic.
