# Assumptions — p3-audit-07 (Phase 3 kill pass, batch 07: C-44..C-50)

- [p3-audit-07] A retired DDR4 RDIMM's opportunity cost is its used-module resale value ($4-11/GB in 4Q26, from amcompute $250-370 per 64GB and PCSP $2,300-5,500 per 512 GB), not DDR4 chip spot ($21-44/GB) — basis: x4 RDIMMs cannot be sold as consumer chips; 01_LANDSCAPE 10.4 #4 bars chip spot as a base case.
- [p3-audit-07] Glut recovered-DDR4 value is $0.5-1.5/GB and severe-trough value $0.3-0.8/GB — basis: 01_LANDSCAPE 5.2 (us_backend.md 6.5 estimate) plus the 2023 DDR4 chip floor of $1.30.
- [p3-audit-07] The small-vendor CXL card costs $2.34/GB (~$1.8k for 12x64GB) — basis: branch B model, not re-derived.
- [p3-audit-07] A Pond-scale pod is 8 dual-socket servers with 1.5 TB each (12 TB); a 7-9% gross saving is valued at the canonical $20.31 (4Q26) and $8.12 (glut) RDIMM decks — basis: Pond 16-socket result; 01_LANDSCAPE 4.3.
- [p3-audit-07] KTransformers decode scales roughly linearly with socket memory bandwidth (307 -> 614 GB/s) and inversely with active parameters (37B -> 32B) — basis: memory-bound MoE decode; measured R1 numbers in the KTransformers tutorial. Result ~20 tok/s (1 socket) and ~26 tok/s (2 sockets), vs the card's 23/46 roofline.
- [p3-audit-07] Gen5 enterprise SSD sequential read is ~12 GB/s — basis: branch B's own 1.79 s to reload 20 GiB; so 8 SSDs roughly match 2x400G RDMA (~100 GB/s).
- [p3-audit-07] R4 compares a card against every alternative its named buyer can actually get, including free software already in the buyer's stack (the same test batch 11 applied to C-77). An identical competitor product alone is scored as competition, not killed under R4.
- [p3-audit-07] EPYC 9005 supports up to ~6 TB per socket at 2 DPC — basis: training knowledge [UNVERIFIED-T]; no search spent.
