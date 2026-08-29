# Backend — cover app API server

Node 20+ / TypeScript / Fastify 4 / SQLite (better-sqlite3). Implements the contract in
`docs/ARCHITECTURE.md`: job queue + engine adapters + style-prompt builder + credits.

## Run

```bash
cd backend
npm install
npm run dev        # tsx watch, port 3000 (PORT env to change)
# or
npm run build && npm start
```

Zero config needed: the default **mock** engine waits ~5s and synthesizes an
audible ~8s WAV melody, so the whole app runs end-to-end without API keys.
Copy `.env.example` to `.env` for the real engines / LLM style prompts.

```bash
npm run typecheck  # tsc --noEmit
npm test           # node:test — job lifecycle, style-prompt fallback, credits/402
```

Storage lives in `backend/data/` (gitignored): `app.db`, `uploads/`, `outputs/`.
Jobs survive restarts — `queued`/`processing` rows are re-queued on boot.

## Endpoints

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | `{ ok, engine }` |
| GET | `/styles` | the 8 shared style presets |
| POST | `/style-prompts` | `{ reference }` → `{ stylePrompt, source: 'llm'\|'fallback', metadata? }` |
| POST | `/covers` | multipart: `audio` (mp3/m4a/wav ≤50MB), `deviceId`, `songName`, `styleId` **or** `customStylePrompt`; `402` at 0 credits |
| GET | `/covers/:id` | job status |
| GET | `/covers?deviceId=` | device's jobs, newest first |
| GET | `/covers/:id/audio` | streams the finished audio |
| POST | `/devices` | upsert `{ deviceId, expoPushToken? }` (10 default credits) |
| GET | `/devices/:deviceId` | `{ device: { deviceId, credits } }` |

Credits decrement **only on success**; a completed job fires an Expo push when the
device registered a token. Artist-voice style prompts ("voice of X", "sounds like
<Name>") are refused with `400` — style prompts describe genre/instrumentation/vibe.
Pasted YouTube links are resolved to **metadata only** (public oEmbed); the app never
downloads audio from streaming services.

## ⚠️ VERIFY ENGINE FIELD NAMES BEFORE SPENDING MONEY

replicate.com and fal.ai were **unreachable from the build environment**, so the
input field names for the two real engines are **best-effort guesses**, isolated in
one constants object per adapter:

- `src/engines/minimaxReplicate.ts` → `REPLICATE_MINIMAX.INPUT_FIELDS`
  — verify against the live schema at <https://replicate.com/minimax/music-cover>
  (API tab → input schema). Also confirm the Files API upload flow and the output
  shape handled in `extractOutputUrl`.
- `src/engines/aceStepFal.ts` → `FAL_ACESTEP` (`queueUrl` + `INPUT_FIELDS`)
  — verify against <https://fal.ai/models/fal-ai/ace-step/audio-to-audio>
  (API docs → input schema). `audio_cover_strength` defaults to 0.5 per
  `docs/FEASIBILITY.md`.

Each mismatch is a one-line fix in those constants. Run one ~$0.15 job per engine
end-to-end before wiring anything user-facing (see `test-kit/` for the validation
harness and pass bar).

## Style-prompt LLM

`POST /style-prompts` uses `@anthropic-ai/sdk` with the cheapest Haiku-tier model
(`claude-haiku-4-5`) when `ANTHROPIC_API_KEY` is set. When unset (or on any API
failure) it falls back to a deterministic keyword match against the preset table,
then a generic template — the response's `source` field says which path ran.
