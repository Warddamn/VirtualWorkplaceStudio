# Engine validation kit — the "$2 listening test"

Standalone Python kit that answers the single go/no-go question from
`docs/FEASIBILITY.md`: **do today's hosted cover engines produce style-transfer
covers good enough that someone would pay for them — especially the kids-choir
case?** Every quality claim in the feasibility report is secondhand; this kit
produces the first-hand evidence, blind-gradable, for a couple of dollars.

It runs your own legally-owned test songs through:

- **MiniMax `minimax/music-cover`** via Replicate — the intended launch engine
- **ACE-Step audio-to-audio** via fal.ai (optional) — the open-source fallback,
  swept across `audio_cover_strength` 0.3 / 0.5 / 0.7 (its known-flaky knob)

across the 8 preset style prompts the app will ship (see `prompts.json`,
kids-choir first because it is the one unsolved sub-problem).

## Cost math

| Engine | Unit cost (est.) | Runs per song × style | Cost per song × style |
|---|---|---|---|
| MiniMax via Replicate | ~$0.15 / cover | 1 | ~$0.15 |
| ACE-Step via fal.ai | metered by compute time (~$0.0002/s); assume ~$0.05 / run | 3 (strength sweep) | ~$0.15 |

Worked examples:

- Focused first pass — 2 songs × 3 styles, MiniMax only:
  2 × 3 × $0.15 ≈ **$0.90**
- The full feasibility-report test — 2 songs × all 8 styles, MiniMax only:
  2 × 8 × $0.15 ≈ **$2.40**
- Both engines, 1 song × all 8 styles:
  8 × ($0.15 + 3 × $0.05) ≈ **$2.40**

These are estimates, not quotes — the script prints its own estimate for your
exact plan and **asks for confirmation before spending anything**. Use
`--limit N` as a hard cap on the number of paid generations.

## Setup

Python 3.10+.

```bash
cd test-kit
pip install -r requirements.txt        # fal-client is optional (see file)

export REPLICATE_API_TOKEN=r8_...      # replicate.com -> account -> API tokens
export FAL_KEY=...                     # fal.ai -> dashboard -> keys (only for acestep)
```

Drop 2–3 audio files you **legally own** into `songs/` (mp3/wav/m4a/flac/ogg —
short vocal songs of 1–3 minutes keep the test cheap). Per the feasibility
report, a good spread is: a clear vocal song, one non-English song, and one
dense mix to stress the lyric extraction.

With **zero API keys set the script still runs**: it explains exactly what is
missing and exits without spending or crashing — safe to try immediately.

## Run

```bash
python3 run_test.py --engine minimax                       # launch-engine test
python3 run_test.py --engine both --styles kids-choir,gospel-choir
python3 run_test.py --engine acestep --limit 6             # cap spend at 6 runs
python3 run_test.py --help
```

Flags: `--engine minimax|acestep|both` (default `minimax`), `--styles` as a
comma-separated list of ids from `prompts.json` (default all 8), `--limit N` to
cap total paid generations, `--yes` to skip the confirmation prompt in
non-interactive runs.

Failures are handled per item: one bad generation is recorded in the manifest
with its error and the run continues.

## Blind grading

Each output is saved as `outputs/<random-id>.mp3` — the filename deliberately
reveals nothing. Two CSVs are written alongside:

- `outputs/manifest.csv` — the **answer key**: id → song, engine, style,
  strength, status, error. Keep this away from graders until scoring is done.
- `outputs/grading.csv` — one row per successful output with empty cells to
  fill in: `melody_recognizable_10s` (yes/no within 10 seconds),
  `lyrics_correct_pct` (0–100), `style_achieved_1_5`, `artifacts_1_5`,
  `would_pay` (yes/no).

Have ~5 listeners play the files in shuffled order and fill in `grading.csv`.
Ideally the person who ran the script is not a grader (the console log shows
the mapping). Afterwards join `grading.csv` to `manifest.csv` on `id` to see
scores per engine/style/strength.

## The pass bar

From `docs/FEASIBILITY.md`:

- **≥ 3 of 5 listeners recognize the song AND can name the style**, and
- **lyric errors < 10%** (i.e. `lyrics_correct_pct` ≥ 90).

If MiniMax clears the bar → build Stage 1 of the app now. If it fails → the
project is effectively gated on Suno partner access or the 2026 licensed
platforms; prototype on ACE-Step and wait.

## Caveat: verify the engine input schemas first

replicate.com and fal.ai were unreachable from the environment where this kit
was written, so the model ids, input field names, and output shapes are
best-effort per the feasibility report. They are isolated in ONE clearly
marked block at the top of `run_test.py`. Before your first paid run, check
them against the live pages:

- https://replicate.com/minimax/music-cover (API tab → input schema)
- https://fal.ai/models/fal-ai/ace-step/audio-to-audio (API docs)

Also confirm on the Replicate page that a **fresh** account can still invoke
`minimax/music-cover` at all — the upstream MiniMax music API is on a
wind-down, which is exactly why this test exists.
