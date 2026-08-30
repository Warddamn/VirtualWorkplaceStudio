# Style-Transfer Cover App

Concept: pick a song you love, point at a style reference (a YouTube link or just a
name — "the PS22 kids-choir cover of Lisztomania"), and get a full cover of your song
in that style: same melody and lyrics, new arrangement and vocals.

## Quick preview — the live site on localhost:5555

```
./preview.sh
```

then open **http://localhost:5555** — one command builds the web version of the app
and serves UI + API together on one port (mock engine, zero configuration, works
offline). First run installs dependencies and builds; later runs start in seconds.
`REBUILD=1 ./preview.sh` forces a fresh web build; `PORT=8080 ./preview.sh` changes
the port.

Current status: **v0.2 app built** (backend + Expo app + engine test kit) with the
premium feature set — multi-take covers, refine loop, Style Studio, tiers. See
[FEASIBILITY.md](FEASIBILITY.md) for the research — engine landscape, API access,
legal constraints, unit economics, and the staged roadmap — and
[docs/PRODUCT.md](docs/PRODUCT.md) for the product vision.

The short version:

- **Feasible.** Full-arrangement style transfer is a shipped capability (Suno Covers,
  MiniMax Music Cover API, open-source ACE-Step). The gap in the market is legal, not
  technical.
- **Partially API-gated.** The best engine (Suno) is invite-only; a legitimate v1 stack
  exists today via MiniMax's cover API on resellers (~$0.15/cover) with ACE-Step as
  self-hosted fallback.
- **One hard legal rule:** never extract audio from YouTube links — use link metadata to
  build a text style prompt instead.
- **Next step:** a ~$2 listening test of the candidate engines (spec in the report)
  before writing any product code.
