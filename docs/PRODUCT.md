# Product Vision — What Makes This Worth $19.99/month

## The feeling we're selling

Nobody pays for "AI music generation." People pay for the chills — the moment a song
they already love comes back transformed and it *works*, the way the PS22 chorus made
Lisztomania feel brand new. Every premium feature below exists to make that moment
(a) happen reliably, (b) feel personal, and (c) be shareable. If a feature doesn't
serve one of those three, it's cut.

The subscription logic: a $19.99 subscriber isn't buying credits, they're buying
**reliability of the magic**. One bad generation kills trust faster than ten good ones
build it. So the deepest premium investment is quality machinery, not feature count.

## The five pillars

### 1. It sounds great *every time* — Takes
Never show the user one roll of the dice. Every cover generates **multiple takes**
(2 on Plus, 4 on Studio), auto-ranked, presented as "Take A / Take B / …" with instant
switching in the player. The user picks the keeper; the rest stay available. This is
the single highest-leverage quality feature and it's pure product engineering — no
model improvements needed.

### 2. Any style, dialed in — Style Studio
- Paste a YouTube link or type "like the kids-choir cover of Lisztomania" → the app
  builds a rich, **editable** style card (instrumentation, mood, tempo feel, vocal
  character) — metadata + LLM only, never audio ripping.
- **Intensity slider**: subtle reinterpretation ↔ total transformation.
- **Save your styles**: a personal style library ("My rainy-day choir", "Grandpa's
  swing band") reusable on any song.
- Curated seasonal/occasion **style packs** (Christmas choir, wedding strings,
  Halloween organ, lullaby music box).

### 3. Refine like talking to a producer — the Refine loop
After hearing a cover: "more choir, less piano", "slower and sadder", "make the chorus
bigger". An LLM merges the note into the style prompt and re-renders as a new linked
version; the version history reads like a session with a producer. Iteration is where
delight compounds — a one-shot tool feels like a slot machine, a refinable one feels
like an instrument.

### 4. Personal, not just popular — Your Voice & Moments
- **Sing it yourself**: record a voice memo of you (or your kid) singing anything —
  get back a full produced arrangement built around *your* melody. Legally the
  cleanest feature we have and emotionally the strongest ("my daughter's song, with an
  orchestra").
- **Moments**: occasion framing on the create screen — "for a birthday", "first
  dance, but as a lullaby", "graduation anthem version". Same engine, different
  entry point; this is what makes non-musicians cry and subscribe.

### 5. Built to share — without legal landmines
Beautiful cover cards (art + waveform + style name), 30-second preview clips, share
sheet for the audio you have rights to. Sharing of covers of commercial songs stays
personal/in-app until Stage-3 licensing (see FEASIBILITY.md); user-owned and
public-domain covers export freely.

## Studio-tier extras (the musician's reasons to pay)
- **Stems** of the cover (vocals / accompaniment) for remixing.
- **Karaoke / instrumental version** of any cover, one tap.
- HQ audio, priority queue, generous fair-use quota.

## Tiers

| | Free | Plus $7.99 | Studio $19.99 |
|---|---|---|---|
| Covers / month | 3 | 30 | 200 (fair use) |
| Takes per cover | 1 | 2 | 4, auto-ranked |
| Style Studio (link/name → style) | preview only | ✅ | ✅ |
| Saved styles | — | 5 | unlimited |
| Refine loop | — | 3/cover | unlimited |
| Instrumental + stems | — | — | ✅ |
| Queue | standard | standard | priority |

## v0.2 scope (buildable now, on top of the MVP)

Backend:
- Multi-take generation: N takes per job (engine-abstracted), stored as `takes` with
  rank order; `POST /covers/:id/pick` to set the keeper.
- `POST /covers/:id/refine` — note text → LLM-merged style prompt → child job linked
  by `parentJobId` (version chain).
- Saved styles CRUD per device: `GET/POST/DELETE /custom-styles`.
- `instrumental: boolean` option on cover creation (prompt-engineered variant).
- Tier/quota config per device (`tier` on devices; quotas enforced; no billing yet —
  a `POST /devices/:id/tier` dev endpoint stands in for the app-store purchase).
- Waveform peaks (`GET /covers/:id/peaks`) computed from the output WAV/MP3 for the
  player's scrubber.

Mobile:
- Take picker in the Player (A/B/C/D chips, instant switch, "keep this one").
- Refine sheet on the Player (note input + version history list).
- Style Studio screen: reference input → editable style card → save to My Styles;
  My Styles rail on Create.
- Moments row on Create (occasion chips that pre-fill style guidance).
- Player upgrades: waveform scrubber, favorite, instrumental toggle (creates variant),
  share sheet.
- Library: favorites filter, version chains grouped, search.
- Onboarding: 3 screens + a bundled demo cover so the first play is instant magic.
- Paywall screen (tier comparison, stubbed purchase → dev tier switch).

Explicitly deferred: real billing (RevenueCat), accounts/cloud sync (device-scoped for
now), social feed/community styles, video export, section-level repaint (engine-gated),
Stage-3 commercial catalog licensing.
