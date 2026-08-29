# Backend — cover app API server

Node 20+ / TypeScript / Fastify 4 / SQLite (better-sqlite3). Implements the contracts in
`docs/ARCHITECTURE.md` (MVP) and `docs/ARCHITECTURE-V2.md` (premium features): job queue +
engine adapters + style-prompt builder + tiers/quotas, multi-take generation, refine loop,
saved custom styles, song-metadata lookup and waveform peaks.

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
npm test           # node:test — lifecycle, takes, refine, quota/402, custom styles,
                   #             peaks, song-metadata validation, v1->v2 migration
```

Storage lives in `backend/data/` (gitignored): `app.db`, `uploads/`, `outputs/`.
Jobs survive restarts — `queued`/`processing` rows are re-queued on boot.

## Tiers & quotas

Devices carry a `tier` (`free|plus|studio`; default free). Monthly quota counts the
device's jobs created in the current UTC calendar month, **excluding failed jobs**
(failed covers don't consume quota; refinements do). Queued/processing jobs already
hold a quota slot, so rapid submissions can't overdraw it. The legacy `credits`
column is kept for migration compat but unused.

| tier | covers/month | takes per cover (max) |
|---|---|---|
| free | 3 | 1 |
| plus | 30 | 2 |
| studio | 200 | 4 |

## Endpoints

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | `{ ok, engine }` |
| GET | `/styles` | the 8 shared style presets |
| POST | `/style-prompts` | `{ reference }` → `{ stylePrompt, source: 'llm'\|'fallback', metadata? }` |
| POST | `/song-metadata` | `{ url }` (YouTube only) → `{ title, author }` via oEmbed — **metadata only, never audio** |
| POST | `/covers` | multipart: `audio` (mp3/m4a/wav ≤50MB), `deviceId`, `songName`, exactly one of `styleId` / `customStylePrompt` / `customStyleId`; optional `takes` (1..tier max, default max), `instrumental` (`"true"` appends ", instrumental only, no vocals"), `parentJobId` (internal); `402` when the monthly quota is spent |
| GET | `/covers/:id` | job status incl. `takes: [{ idx, status }]`, `selectedTake`, `parentJobId`, `refineNote` |
| GET | `/covers?deviceId=` | device's jobs, newest first |
| GET | `/covers/:id/audio?take=N` | streams take N (default: selected take); Range/206 supported; non-selected takes get " (take N+1)" in the filename |
| GET | `/covers/:id/peaks?take=N` | `{ peaks: number[] }` — ~120 buckets of 0..1 RMS from the WAV output; `[]` for non-WAV outputs |
| POST | `/covers/:id/pick` | `{ take }` (must be a succeeded take) → sets the keeper → `{ job }` |
| POST | `/covers/:id/refine` | `{ note }` (1–300 chars) → LLM-merged (or deterministic `"<prompt>, <note>"`) style prompt → child job with `parentJobId`; normal quota check → `201 { job }` |
| GET | `/custom-styles?deviceId=` | saved styles, newest first |
| POST | `/custom-styles` | `{ deviceId, name ≤60, emoji? ≤8, stylePrompt ≤300 }` → `201 { style }` (cap 50/device) |
| DELETE | `/custom-styles/:id?deviceId=` | `{ ok: true }`; 404 if not that device's |
| POST | `/devices` | upsert `{ deviceId, expoPushToken? }` |
| GET | `/devices/:deviceId` | `{ device: { deviceId, tier, monthlyQuota, usedThisMonth, remaining } }` |
| POST | `/devices/:deviceId/tier` | `{ tier }` → updated device — **dev stub** standing in for app-store billing |

A cover job runs its takes **sequentially in one queue slot**: the job succeeds when
≥1 take succeeds (failed takes stay recorded and selectable-around), and fails only
when all takes fail. A completed job fires an Expo push when the device registered a
token. Artist-voice style prompts ("voice of X", "sounds like <Name>") are refused
with `400` — style prompts describe genre/instrumentation/vibe. Pasted YouTube links
are resolved to **metadata only** (public oEmbed); the app never downloads audio from
streaming services.

Test knob: `MOCK_ENGINE_FAIL_TAKES` (comma list of take indexes, e.g. `0,2`) makes
the mock engine fail those takes — used by the test suite to exercise partial-failure
jobs.

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

`POST /style-prompts` and the refine merge use `@anthropic-ai/sdk` with the cheapest
Haiku-tier model (`claude-haiku-4-5`) when `ANTHROPIC_API_KEY` is set. When unset (or
on any API failure) they fall back deterministically — style prompts to a keyword
match against the preset table then a generic template (the response's `source` field
says which path ran), refine to `"<source prompt>, <note>"` truncated to 300 chars.
Either way the result is denylist-checked before it reaches an engine.
