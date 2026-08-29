# MVP Architecture Contract

This document is the source of truth for the MVP build. Every component must follow it
so the pieces integrate. Repo layout:

```
/test-kit/    Engine validation kit (Python)         — standalone, no app dependencies
/backend/     API server (Node 20+, TypeScript)      — job queue + engine adapters
/mobile/      Phone app (Expo / React Native, TS)    — thin client for the backend
/docs/        This contract + FEASIBILITY.md context
```

Hard rules for all components:
- The app NEVER downloads/extracts audio from YouTube or any streaming service. A pasted
  link may only be resolved to **metadata** (YouTube oEmbed: `https://www.youtube.com/oembed?url=<link>&format=json`,
  no API key needed) and turned into a *text* style prompt.
- Users supply audio only as local files they own (upload / in-app recording).
- No named-artist voice imitation: style prompts must describe genre/instrumentation/
  vibe, never "in the voice of <artist>". Backend strips/refuses artist-voice requests
  (maintain a simple denylist check: prompt patterns like "voice of", "sounds like <Name>").

## Shared: style presets

Both backend and mobile ship this list (backend is authoritative via `GET /styles`;
mobile bundles it as fallback). Fields: `id`, `name`, `emoji`, `description`,
`stylePrompt` (the engineered prompt sent to the engine, ≤300 chars).

| id | name | stylePrompt (essence) |
|---|---|---|
| kids-choir | Kids Choir | children's choir, school assembly, piano accompaniment, joyful, live room, group of young voices singing in unison and simple harmony |
| bossa-nova | Bossa Nova | bossa nova, nylon guitar, soft brushed drums, warm intimate vocals, Rio café feel |
| synthwave-80s | 80s Synthwave | 80s synthwave, analog synths, gated reverb drums, neon retro-futuristic mood |
| swing-trio | Swing Jazz Trio | swing jazz trio, upright bass, brushed kit, jazz piano, crooner-style delivery |
| campfire-folk | Campfire Folk | acoustic folk, fingerpicked guitar, warm group harmonies, intimate campfire feel |
| gospel-choir | Gospel Choir | gospel choir, hammond organ, claps, powerful massed voices, uplifting church energy |
| heavy-metal | Heavy Metal | heavy metal, distorted guitars, double-kick drums, aggressive powerful vocals |
| lofi-chill | Lo-fi Chill | lo-fi chillhop, dusty drums, mellow keys, relaxed hazy vocals, bedroom-producer feel |

## Backend (`/backend`)

Stack: Node 20+, TypeScript (strict), Fastify 4, `@fastify/multipart`, `@fastify/cors`,
`better-sqlite3`, `zod`, `expo-server-sdk` (push), `@anthropic-ai/sdk` (style prompts).
Scripts in package.json: `dev` (tsx watch), `build` (tsc), `start`, `typecheck`
(tsc --noEmit), `test` (node --test on compiled or via tsx). Keep tests light but real:
job lifecycle with mock engine, style-prompt fallback, credits.

Storage: `backend/data/` (gitignored) — `app.db` (SQLite), `uploads/`, `outputs/`.
Port: `PORT` env, default **3000**. All responses JSON unless noted.

### Data model (SQLite)

- `jobs`: id (uuid), device_id, song_name, style_id (nullable), style_prompt,
  status (`queued|processing|succeeded|failed`), engine, input_path, output_path
  (nullable), error (nullable), created_at, updated_at
- `devices`: device_id (pk), expo_push_token (nullable), credits (int, default 10),
  created_at

### Engine adapter interface

```ts
export interface CoverEngine {
  readonly name: string;                 // 'mock' | 'minimax' | 'acestep'
  generateCover(req: {
    inputAudioPath: string;              // local file path of user's song
    stylePrompt: string;                 // ≤300 chars
  }): Promise<{ outputAudioPath: string }>;  // local file path of result
}
```

Selected by env `ENGINE` (default `mock`).

- **MockEngine** (default, zero config): waits ~5s, then synthesizes a valid 16-bit PCM
  WAV (~8s, a simple sine-wave melody — a few notes so it's audibly "a song") written
  with no external deps, and returns it. This makes the whole app runnable end-to-end
  with no API keys.
- **MinimaxReplicateEngine**: calls Replicate's HTTP API (`REPLICATE_API_TOKEN`) for
  model `minimax/music-cover` — upload the input audio (Replicate files API or data URI),
  pass the style prompt, poll the prediction, download output. NOTE: replicate.com is
  unreachable from this build environment, so exact input field names could not be
  verified — implement best-effort per docs/FEASIBILITY.md (reference audio + text
  prompt, 10–300 chars), isolate field names in one constants object, and put a loud
  comment + README note telling the operator to verify against the live model page.
- **AceStepFalEngine**: same posture against fal.ai (`FAL_KEY`), endpoint family
  `fal-ai/ace-step/audio-to-audio` with `audio_cover_strength` ~0.5.

Failures must mark the job `failed` with a human-readable `error`, never crash the queue.

### Job queue

In-process worker (no Redis): a simple FIFO drained by N=2 concurrent workers; jobs
survive restarts by re-queuing `queued`/`processing` rows on boot. On completion:
decrement device credits (only on success), send Expo push if the device registered a
token ("Your <style> cover of <song> is ready 🎶").

### Style prompt builder

`buildStylePrompt(reference: string)`:
1. If reference matches a YouTube URL → fetch oEmbed metadata (title + author_name).
2. Compose an LLM request (Anthropic SDK) that turns the reference text/metadata into a
   ≤300-char instrumentation/genre/mood style prompt (never artist-voice imitation —
   include that constraint in the system prompt). Use the current cheapest Haiku-tier
   model — load the `claude-api` skill to get the current model id before writing this.
3. If `ANTHROPIC_API_KEY` is unset or the call fails → deterministic fallback: keyword
   match against the preset table (e.g. contains "choir" → kids-choir prompt), else a
   generic template built from the reference text. Response says which path was used.

### Endpoints

- `GET /health` → `{ ok: true, engine: string }`
- `GET /styles` → `{ styles: StylePreset[] }`
- `POST /style-prompts` body `{ reference: string }` →
  `{ stylePrompt: string, source: 'llm' | 'fallback', metadata?: { title, author } }`
- `POST /covers` — multipart: `audio` (file, mp3/m4a/wav, ≤50MB), fields `deviceId`,
  `songName`, and either `styleId` or `customStylePrompt`. 402 if credits ≤ 0.
  → `{ job: Job }` (Job mirrors the jobs row, camelCased, without paths)
- `GET /covers/:id` → `{ job: Job }`
- `GET /covers?deviceId=` → `{ jobs: Job[] }` (newest first)
- `GET /covers/:id/audio` → streams the output file (Content-Type audio/wav or audio/mpeg)
- `POST /devices` body `{ deviceId, expoPushToken? }` → upsert → `{ device: { deviceId, credits } }`
- `GET /devices/:deviceId` → `{ device: { deviceId, credits } }`

Validation with zod; unknown routes 404 JSON; errors `{ error: string }`.

## Mobile (`/mobile`)

Stack: Expo (current SDK, TypeScript template), `expo-router`, `expo-document-picker`
(pick audio file), `expo-av` (playback), `expo-notifications` + `expo-device` (push),
`@react-native-async-storage/async-storage`. Must pass `npx tsc --noEmit`.

Config: `EXPO_PUBLIC_API_URL` (default `http://localhost:3000`); also editable in a
Settings screen (persisted). On first launch generate a `deviceId` (uuid), persist it,
`POST /devices` (with Expo push token when permission granted — degrade gracefully in
Expo Go / simulator).

Screens (expo-router):
- **Create** (`/`): pick an audio file → shows file name; style gallery grid (from
  `GET /styles`, bundled fallback) with emoji cards; an optional "or describe / paste a
  link" text field with a "Preview style" button calling `POST /style-prompts` and
  showing the generated prompt; big "Make my cover" button → `POST /covers` → navigate
  to Library. Show remaining credits.
- **Library** (`/library`): job list with status chips (queued/processing spinner /
  ready / failed), poll every 3s while any job is active; tap a ready job → Player.
- **Player** (`/cover/[id]`): song name, style, play/pause via expo-av streaming
  `GET /covers/:id/audio`, share-sheet button for the downloaded file.
- **Settings** (`/settings`): backend URL, device id display, credits.

Design: clean dark theme, one accent color, emoji-forward style cards. No pixel-perfect
ambitions — solid, obviously-navigable MVP.

## Test kit (`/test-kit`)

Python 3.10+, standalone. Files:
- `README.md` — what this proves, cost (~$0.15/cover), how to run, the pass bar
  (≥3/5 listeners recognize the song AND name the style; lyric errors <10%).
- `requirements.txt` — `replicate`, `fal-client` (optional), `requests`.
- `prompts.json` — the 8 preset style prompts above (kids-choir first).
- `run_test.py` — for each audio file in `songs/` × each selected prompt: run
  `minimax/music-cover` on Replicate (`REPLICATE_API_TOKEN`) and optionally ACE-Step
  audio-to-audio on fal (`FAL_KEY`, strength sweep 0.3/0.5/0.7). Save to
  `outputs/<random-id>.mp3` with the mapping written to `outputs/manifest.csv`
  (id → song, engine, style) so grading can be done blind; also emit `grading.csv`
  (id, melody_recognizable_10s, lyrics_correct_pct, style_achieved_1_5,
  artifacts_1_5, would_pay) with empty cells to fill in.
  CLI: `--engine minimax|acestep|both`, `--styles kids-choir,...` (default all),
  `--limit N` to cap spend; print a cost estimate and ask for confirmation before
  spending. Handle failures per-item and keep going.
- `songs/.gitkeep` — user drops their own legally-owned test files here.

Field-name caveat: replicate.com/fal.ai are unreachable from the build environment, so
input schemas are best-effort — isolate them at the top of `run_test.py` with a comment
pointing at the live model pages.

## Git hygiene

Root `.gitignore` covers: `node_modules/`, `backend/data/`, `mobile/.expo/`, `dist/`,
`build/`, `__pycache__/`, `.env*`, `test-kit/outputs/`, `test-kit/songs/*` (keep
`.gitkeep`), `*.log`. Builders do not run git commands; integration commits happen at
the end from the orchestrating session.
