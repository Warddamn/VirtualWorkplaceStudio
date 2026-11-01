## Summary

**Bottom line.** Two red-team rounds raised 186 objections against seven deep dives, and none was refuted. Five deep dives were killed and two were cut to part-time side lines. No surviving plan pays the founder a salary within 36 months in any price scenario. So the Phase 6 picks are side businesses, not ventures (`research/phase6/decision.json`).

### What was attacked, and by whom

Four adversarial personas attacked every deep dive independently: **VET**, a 30-year DRAM process veteran; **VC**, a semiconductor VC who lost money on Z-RAM, T-RAM, Nantero and Crossbar; **HYP**, a top-5-cloud memory procurement lead; and **PHY**, a condensed-matter physicist.

- **Round 1** covered DD1–DD5 and raised 127 objections.
- **Round 2** covered DD6–DD7 and raised 59. It was run because round 1 left no PRIMARY or MOONSHOT candidate (`03_SCORING.md` §9).

Of the 186, 11 were FATAL, 112 MAJOR and 63 MINOR. Dispositions: 0 refuted, 42 mitigated, 111 downgraded, 33 killed (Scoreboard below).

### Outcome

| Deep dive | Final status | Revised m36 BASE ARR | Founder full-time within 36 months? | Decisive objection |
|---|---|---|---|---|
| DD1 Provenance & recert | KILLED | $58,335 | Never (m32 only if two long-shot tracks both pass) | RT-HYP-DD1-01: the module maker already knows its die source and may self-certify for free |
| DD2 Lifecycle intelligence | DOWNGRADED; now PRIMARY | $149,629 | Never (needs ≥14.7% trial conversion; modelled 10%) | RT-VC-DD2-01: the panel reaches 14.2 of the 15 contributors needed, so the index, the bundle's moat, is never published |
| DD3 NV continuity cards | KILLED | $39,890 run-rate ($2.7k recurring) | Never | RT-HYP-DD3-01: i-series controls already back up to a $20 CF card; without them and the unfound DMSMS orders, demand is ~2,591 cards/yr |
| DD4 Memory efficiency | KILLED | $7,098 | Never | RT-VC-DD4-01: no kill-test result changes the ceiling; real on-call costs $2.9–3.4k/month against a $1.66/node fee |
| DD5 Open memory IP | DOWNGRADED; now FALLBACK | $65,678 recurring ($164.1k run-rate) | Never (only the combined-upside case, at m22) | RT-VC-DD5-01: half the 298-project market was the author's estimate; ceiling $747k → $424k/yr (RT-VC-DD5-02 killed the T2 legs) |
| DD6 Private MoE appliance | KILLED | $63,873 | Never (needs a 21% close rate) | RT-VET-DD6-01: four users touch 3.88× one user's expert bytes, so the L box serves 1–2 users, not 4 |
| DD7 Legacy DRAM die bank | KILLED | $8,606 (residual rep line) | Never | RT-VET-DD7-01: banking die costs the OEM 2.9–5.4× a packaged last-time buy |

Sources: `research/phase5/responses_*.json`; `models/lifecycle-intel.py` and `models/open-memory-ip.py`, re-run 2026-11-01 with exit 0.

### Failure modes that recurred

1. **The buyer already had the asset for free.** Module makers hold die-source invoices and can read package top marks (DD1). MCM makers bank their own die, and Micross sells the same bundle direct (DD7). Proxmox already runs KSM (DD4). Fanuc i-series controls take a $20 CF card (DD3).
2. **A free or cheaper substitute was already in the channel.**
   - Distributors and Octopart give away the lifecycle data DD2 charges $249/month for (HYP and VC verdicts).
   - Free OpenRAM code keeps improving, and its authors are DD5's likely contractors (VC verdict; RT-HYP-DD5-04).
   - A $44.6k two-node Mac Studio cluster matches the single-stream speed of DD6's $78,708 L box, per published runs (RT-HYP-DD6-03).
3. **The models hid capacity limits.**
   - DD6's revenue never read the box's capacity (VET verdict).
   - DD2 sold index licences whatever the panel size (RT-HYP-DD2-01).
   - DD4's $750/month of 24/7 on-call buys about 4 contractor hours (RT-VET-DD4-04).
   - Part-time hours cap DD2 at ~20 trials a month (RT-VC-DD2-06). DD5 can reach only 19 new teams a month, because no more exist (RT-HYP-DD5-01).
4. **Demand inputs were estimates.**
   - DD5: 150 of the 298 projects a year (RT-VC-DD5-01).
   - DD3: two DMSMS orders nobody found, which carried $48k of the $56.2k m36 recurring ARR (RT-VC-DD3-04).
   - DD2: a 6,000-OEM market, now 3,000 and still an estimate (RT-VC-DD2-04).
   - DD1: an unmeasured 7%→10% close-rate lift (RT-VC-DD1-02).
5. **Regulated buyers will not take a part-time founder on trust.**
   - Their supplier onboarding is hard for a part-time single-member LLC to pass (DD6 revised verdict).
   - Vendor approval needs a named on-call rotation (RT-HYP-DD4-04).
   - Defense work needs NIST SP 800-171 or AS9120B, ~$35k each (DD7).
   - The day job adds an IP-assignment risk, which became DD2's K0 gate (RT-VC-DD2-05).

### What the red team got wrong or could not test

- **Evidence on both sides is snippet-grade.** Deep-dive web facts are [REPORTED] at best (`lifecycle-intel.md` header). Some objections cite a datasheet "as I recall it; verify" (RT-VET-DD3-03) or [UNVERIFIED-training] figures (RT-HYP-DD3-06).
- **It replaced estimates with smaller estimates.** Neither side has a deposit, PO or paid pilot (`decision.json`, biggest_unknown). Cutting conversion from 12% to 10%, or OEMs from 6,000 to 3,000, is more cautious, not better evidenced. The kill tests are the first real demand data.
- **Some objections overstated their case.** DD6 needs ~461 GB/s on routed-only bytes, not ~620 GB/s, though the verdict holds (RT-VET-DD6-01). DD5 recorded two factual corrections: Cadence did offer a ReRAM option in 2026 (RT-VET-DD5-05), and a 6-month slip on the Phase 4 inputs still paid the founder at m21 (RT-VC-DD5-04).
- **Zero refutations out of 186 is a warning sign.** The same study wrote the deep dives and the responses, so concessions may have come too easily. Re-running each concession in a model reduces that risk but does not remove it.
- **No persona was a buyer of either survivor.** None is an SMB-OEM purchaser (DD2) or a university tapeout team (DD5).
- **Some physics was never tested.** No one has measured DD6's throughput on the exact box, tested DD3's magnetic immunity above 8,000 A/m, or silicon-verified a 16 KB-plus sky130 macro (DD5).
- **Eleven surviving concepts were never deep-dived or red-teamed** (`SUMMARY_TABLE.md`). They include C-36, which the integrity judge calls "alive only because it was never red-teamed."

### How the outcome changed the decision

Round 1 killed DD1, DD3 and DD4 and cut DD2 and DD5 to side lines. The study then ran round 2 on the strongest untested survivors (`03_SCORING.md` §9). DD6, the best-fit hardware concept and, per the round-2 selection, the only one a glut helps (its deep dive found the gain small: GLUT m36 ARR $66,969 vs BASE $63,873), was the PRIMARY candidate; DD7, the strongest T2+ path, was the MOONSHOT candidate. Round 2 killed both: DD6 nets −$29,411 over 36 months and needs a $25k bridge, and DD7's Plan B returns 0.29× on $11.49M.

The three judges then reached the same picks independently (`research/phase6/judge_*.json`):

- **PRIMARY: DD2, SaaS only.** It has the cheapest decisive test (~$1,950 planned over 29 days, ~$2,950 if the deferred $1,000 consult is spent; `decision.json` PRIMARY.spend) and 57% gross margin by m36, and its lifecycle module holds flat at $5,774/month in the glut. If K0, K1 or K6 fails, the PRIMARY becomes NONE.
- **FALLBACK: DD5, the wedge only, run after DD2 rather than alongside it.** Its buyers do not overlap with DD2's. If it passes its test, it is the only survivor that ends 36 months above its starting $40k in all three price scenarios.
- **MOONSHOT: none qualifies.** The killed index (C-86) is kept as a ~$0 option inside DD2's test.

The response files' "not a PRIMARY" and "not FALLBACK" lines predate round 2; the picks do not upgrade either concept.
