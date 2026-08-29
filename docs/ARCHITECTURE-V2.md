# v0.2 Architecture Contract — Premium Features

Extends `docs/ARCHITECTURE.md` (still binding where not amended here) with the v0.2
scope from `docs/PRODUCT.md`. Same hard rules: no audio extraction from YouTube (links
resolve to oEmbed **metadata only**), no artist-voice imitation.

## Backend changes (`/backend`)

### Tiers replace raw credits

`devices` gains `tier TEXT NOT NULL DEFAULT 'free'` (`free|plus|studio`). Monthly
quota is enforced by counting the device's jobs created in the current calendar month
(UTC), **excluding** jobs with status `failed` (failed covers don't consume quota;
refinements DO count — they are generations).

| tier | monthly covers | takes per cover (max) |
|---|---|---|
| free | 3 | 1 |
| plus | 30 | 2 |
| studio | 200 | 4 |

- Device API shape becomes `{ deviceId, tier, monthlyQuota, usedThisMonth, remaining }`
  (drop `credits` from responses; keep the column for migration compat, unused).
  Update existing tests accordingly — the full MVP suite must still pass otherwise.
- `POST /covers` returns **402** `{ error }` when `remaining <= activeJobs` (the
  reservation logic from v1, now against quota).
- `POST /devices/:deviceId/tier` body `{ tier }` → updated device. Dev-stub for the
  future app-store purchase; a comment must say so.

### Takes (multi-candidate generation)

- New table `takes`: `job_id`, `idx` (0-based), `status` (`pending|succeeded|failed`),
  `output_path`, `error`. A job requests `takesRequested` (1..tier max, default =
  tier max, clamped) and runs its takes sequentially in one queue slot; the job is
  `succeeded` when ≥1 take succeeded (failed takes are tolerated), `failed` only when
  all fail.
- `POST /covers` gains optional multipart fields: `takes` (int), `instrumental`
  (`"true"|"false"` — when true, append ", instrumental only, no vocals" to the style
  prompt server-side), `parentJobId` (internal use by refine; reject unknown ids).
- Job API shape gains: `takes: [{ idx, status }]`, `selectedTake: number` (default 0,
  the first succeeded take), `takesRequested`, `instrumental: boolean`,
  `parentJobId: string|null`, `refineNote: string|null`.
- `GET /covers/:id/audio?take=N` streams take N (default `selectedTake`). Keep Range +
  Content-Disposition behavior; filename gains ` (take N+1)` when N != selectedTake.
- `POST /covers/:id/pick` body `{ take }` → sets `selectedTake` (must be a succeeded
  take) → `{ job }`.

### Refine

`POST /covers/:id/refine` body `{ note }` (1..300 chars, denylist-checked):
- Source job must be `succeeded`. Builds a new style prompt by merging the source
  job's prompt with the note — via Anthropic when `ANTHROPIC_API_KEY` is set (same
  model/constraints as buildStylePrompt; result ≤300 chars, denylist-checked), else a
  deterministic fallback: `"<source prompt>, <note>"` truncated to 300.
- Creates a child job (same input audio file, `parentJobId` = source, `refineNote` =
  note, same instrumental flag, takes = tier max) through the normal quota check and
  queue. → `201 { job }`.

### Saved custom styles

New table `custom_styles`: `id` (uuid), `device_id`, `name` (≤60), `emoji` (≤8),
`style_prompt` (≤300, denylist-checked), `created_at`.
- `GET /custom-styles?deviceId=` → `{ styles: [...] }` (newest first, camelCased)
- `POST /custom-styles` body `{ deviceId, name, emoji?, stylePrompt }` → `201 { style }`
  (cap 50 per device → 400 beyond)
- `DELETE /custom-styles/:id?deviceId=` → `{ ok: true }` (404 if not that device's)
- `POST /covers` gains optional `customStyleId` as a third mutually-exclusive style
  source (`styleId` | `customStylePrompt` | `customStyleId`).

### Song identification from a link (metadata only)

`POST /song-metadata` body `{ url }` (must be a YouTube/youtu.be URL → 400 otherwise):
fetch `https://www.youtube.com/oembed?url=...&format=json` server-side, → 
`{ title, author }` or 502 `{ error }` when the lookup fails. No audio is ever
fetched — this endpoint exists so the app can prefill the song name and tell the user
"now pick your own audio file of this song". Reuse/refactor the oEmbed helper already
in stylePrompt.ts.

### Waveform peaks

`GET /covers/:id/peaks?take=N` → `{ peaks: number[] }` — ~120 buckets of 0..1 RMS
computed by parsing the output WAV (16-bit PCM; use the existing WAV knowledge from
the mock engine). For non-WAV outputs return 200 `{ peaks: [] }` and let the client
fall back to a plain progress bar.

### Tests

Keep the whole suite green. Add coverage: takes lifecycle (multi-take job with a
partially failing engine → succeeded with failed take recorded), pick, refine
(fallback path: merged prompt + parent linkage + quota consumption), quota 402 at
tier limit and after tier upgrade, custom styles CRUD + use in a cover, peaks on a
mock output, song-metadata URL validation (reject non-YouTube without network).
The mock engine gains an env knob `MOCK_ENGINE_FAIL_TAKES` (comma list of take idxs
to fail) for tests.

## Mobile changes (`/mobile`)

All screens keep passing `npx tsc --noEmit`. API client mirrors the new shapes.

- **Create**: Moments chip row (Birthday 🎂, Lullaby 🌙, Wedding 💍, Holiday 🎄,
  Graduation 🎓 — each appends a phrase to the style guidance, bundled client-side);
  "Identify from a link" field → `POST /song-metadata` → prefills song name + shows
  the note "Now pick your own audio file of this song — the app never downloads from
  YouTube"; My Styles rail (from `GET /custom-styles`) after the preset gallery; a
  "Save style" button beside a successful custom preview (name + emoji dialog);
  takes selector (1..tier max) and Instrumental toggle; quota display
  (`remaining/monthlyQuota` + tier badge).
- **Player**: take chips (Take A/B/C/D from `takes`, disabled when failed), switching
  swaps the audio source (`?take=N`); "Keep this take" → `POST /pick`; Refine sheet
  (note input, submit → navigate to the new job's player); version chain strip when
  `parentJobId` or children exist ("v1 → v2 → v3" navigation); waveform scrubber from
  `/peaks` (SVG-free: a row of Views with heights; plain slider fallback when peaks
  empty); share button unchanged.
- **Library**: group refinement chains under the newest version (expandable);
  favorites star stored in AsyncStorage; search box filtering by song name/style;
  filter chips (All / Ready / Favorites).
- **Paywall** (`/upgrade`): tier comparison from PRODUCT.md, current tier highlighted,
  "Switch (dev)" buttons calling the tier dev endpoint with a visible "developer
  stub — real purchases come with App Store billing" note. Entry points: quota-empty
  402 errors and a Settings row.
- **Onboarding**: first-launch overlay (3 cards: pick a song you own → choose any
  style → takes & refine), dismissed state persisted; ship a small bundled demo WAV
  asset (generate one ~5s melody file into `assets/demo-cover.wav` during the build,
  committed) playable from the overlay's last card so the first sound is instant.
- **Settings**: tier + quota display, link to Paywall.

## Out of scope (unchanged from PRODUCT.md)

Real billing, accounts/sync, social/community, video export, section repaint,
commercial-catalog licensing.
