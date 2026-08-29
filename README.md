# Style-Transfer Cover App

Concept: pick a song you love, point at a style reference (a YouTube link or just a
name — "the PS22 kids-choir cover of Lisztomania"), and get a full cover of your song
in that style: same melody and lyrics, new arrangement and vocals.

Current status: **feasibility research complete.** See [FEASIBILITY.md](FEASIBILITY.md)
for the full report — engine landscape, API access, legal constraints, phone-app
architecture, unit economics, and a staged roadmap.

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
