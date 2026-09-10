# Cover App — project context

Style-transfer cover app: pick a song, point at a style reference, get a full cover in that
style. Same melody and lyrics, new arrangement and vocals.

## Layout

| Path | What |
|---|---|
| `backend/` | Node 20 / TypeScript / Fastify 4 / SQLite. Job queue, engine adapters, tiers. |
| `mobile/` | Expo app. `app/` routes, `components/`, `lib/`. |
| `test-kit/` | Standalone Python engine-validation kit. The "$2 listening test". |
| `docs/` | Architecture contracts and strategy. `ARCHITECTURE.md` is v1, `ARCHITECTURE-V2.md` amends it. |

## Commands

```bash
cd backend && npm run dev         # tsx watch, port 3000
cd backend && npm run typecheck   # tsc --noEmit
cd backend && npm test            # node:test
./preview.sh                      # full app on localhost:5555, mock engine, no keys needed
```

Storage lives in `backend/data/` and is gitignored. Jobs survive restarts.

## Two hard rules, do not violate

1. **Never extract audio from a YouTube link.** Links resolve to oEmbed **metadata only**,
   which an LLM turns into a text style prompt. This is killed three separate ways: YouTube
   ToS, live DMCA §1201 claims, and App Store Guideline 5.2.3.
2. **Never imitate a named artist's voice.** Styles describe instrumentation, mood, tempo
   feel, and vocal character. Not a person.

## Engine adapters

`backend/src/engines/` — `mock` (default, no keys, synthesizes an 8s WAV), `minimaxReplicate`
(intended launch engine, ~$0.15/cover), `aceStepFal` (open-source fallback, quality risk).
The abstraction layer exists because MiniMax's own API is being sunset; treat the supply
chain as fragile and keep adapters swappable.

## Tiers

`free` 3 covers/month 1 take · `plus` 30/2 · `studio` 200/4. Quota counts non-failed jobs in
the current UTC month. Failed covers do not consume quota; refinements do.

## Open question that gates everything

`FEASIBILITY.md` says every quality claim in it is secondhand. The listening test in
`test-kit/` has never been run. Until it is, "does the output clear the I-would-pay-for-this
bar" is unanswered, and it is the go/no-go for the whole product.

## Working style

- Run `npm run typecheck` and `npm test` in `backend/` before saying a change works.
- Prefer editing the engine abstraction over special-casing one provider.
- Agent fleet conventions live in `docs/CHEAP-BUILD-RUNBOOK.md`. Workers are cheap, narrow,
  and read-mostly. One writer per project at a time.
