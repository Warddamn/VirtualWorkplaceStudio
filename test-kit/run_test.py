#!/usr/bin/env python3
"""Engine validation kit — the "$2 listening test" from docs/FEASIBILITY.md.

For every audio file you drop into ./songs/ and every selected style preset in
./prompts.json, this script generates a cover via:

  * Replicate `minimax/music-cover`            (env REPLICATE_API_TOKEN)
  * optionally fal.ai ACE-Step audio-to-audio  (env FAL_KEY), sweeping
    audio_cover_strength over 0.3 / 0.5 / 0.7

Outputs land in ./outputs/<random-id>.mp3 so they can be graded BLIND:
  * outputs/manifest.csv  — the answer key (id -> song, engine, style, strength)
  * outputs/grading.csv   — one empty scoring row per successful output

The script never spends money without printing a cost estimate and asking for
confirmation first, and it degrades gracefully: with zero API keys it explains
exactly what is missing instead of crashing. Per-item failures are recorded and
the run keeps going.

Usage examples:
    python3 run_test.py --engine minimax
    python3 run_test.py --engine both --styles kids-choir,gospel-choir --limit 6
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import secrets
import sys
import time
from pathlib import Path

# ============================================================================
# ENGINE INPUT SCHEMAS — BEST EFFORT. VERIFY BEFORE SPENDING REAL MONEY.
#
# replicate.com and fal.ai were UNREACHABLE from the environment where this
# script was written, so the model ids, input field names, and output shapes
# below could not be checked against the live schemas. They follow the shapes
# documented in docs/FEASIBILITY.md (reference audio + text style prompt,
# 10-300 chars; ACE-Step audio-to-audio with an audio_cover_strength slider).
#
# Before your first paid run, open:
#   https://replicate.com/minimax/music-cover        (API tab -> input schema)
#   https://fal.ai/models/fal-ai/ace-step/audio-to-audio  (API docs)
# and fix the constants below if they differ. Everything schema-shaped lives
# in this one block on purpose — nothing else in the file should need edits.
# ============================================================================

MINIMAX_MODEL = "minimax/music-cover"
MINIMAX_FIELD_AUDIO = "audio_url"     # the user's source song (public MP3/WAV URL; must contain vocals)
MINIMAX_FIELD_PROMPT = "prompt"       # text style prompt (model allows up to 2,000 chars)
# ^ cross-checked 2026-08-30 against replicate.com/minimax/music-cover, runware.ai
#   and aimlapi.com docs (all agree) — still glance at the live model page first.

ACESTEP_ENDPOINT = "fal-ai/ace-step/audio-to-audio"
ACESTEP_FIELD_AUDIO_URL = "audio_url"          # URL of the uploaded source song
ACESTEP_FIELD_PROMPT = "prompt"                # text style prompt
ACESTEP_FIELD_STRENGTH = "audio_cover_strength"  # 0..1, how far from the original

# ============================================================================

KIT_DIR = Path(__file__).resolve().parent
SONGS_DIR = KIT_DIR / "songs"
OUTPUTS_DIR = KIT_DIR / "outputs"
PROMPTS_PATH = KIT_DIR / "prompts.json"
MANIFEST_PATH = OUTPUTS_DIR / "manifest.csv"
GRADING_PATH = OUTPUTS_DIR / "grading.csv"

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac", ".aiff"}

# Cost model (see README.md for the math). Estimates, not quotes.
MINIMAX_COST_PER_COVER = 0.15   # ~$0.15/cover via Replicate (FEASIBILITY.md)
ACESTEP_EST_COST_PER_RUN = 0.05  # rough: fal bills by compute time (~$0.0002/s)

ACESTEP_STRENGTHS = (0.3, 0.5, 0.7)
MAX_PROMPT_CHARS = 300

MANIFEST_COLUMNS = ["id", "song", "engine", "style", "strength", "status", "error"]
GRADING_COLUMNS = [
    "id",
    "melody_recognizable_10s",
    "lyrics_correct_pct",
    "style_achieved_1_5",
    "artifacts_1_5",
    "would_pay",
]


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------

def die(message: str, code: int = 2) -> "NoReturn":  # noqa: F821 (py3.10 friendly)
    print(f"\nerror: {message}", file=sys.stderr)
    sys.exit(code)


def load_styles() -> list[dict]:
    """Load and sanity-check prompts.json."""
    try:
        data = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"prompts.json not found at {PROMPTS_PATH}")
    except json.JSONDecodeError as exc:
        die(f"prompts.json is not valid JSON: {exc}")
    styles = data.get("styles")
    if not isinstance(styles, list) or not styles:
        die("prompts.json must contain a non-empty 'styles' array")
    for style in styles:
        for field in ("id", "name", "stylePrompt"):
            if not style.get(field):
                die(f"style entry {style!r} is missing required field '{field}'")
        if len(style["stylePrompt"]) > MAX_PROMPT_CHARS:
            print(
                f"warning: stylePrompt for '{style['id']}' exceeds "
                f"{MAX_PROMPT_CHARS} chars; truncating for the engine call."
            )
            style["stylePrompt"] = style["stylePrompt"][:MAX_PROMPT_CHARS]
    return styles


def discover_songs() -> list[Path]:
    if not SONGS_DIR.is_dir():
        return []
    return sorted(
        p
        for p in SONGS_DIR.iterdir()
        if p.is_file()
        and not p.name.startswith(".")
        and p.suffix.lower() in AUDIO_EXTENSIONS
    )


def existing_output_ids() -> set[str]:
    """Ids already used in outputs/ or manifest.csv, to avoid collisions."""
    ids: set[str] = set()
    if OUTPUTS_DIR.is_dir():
        ids.update(p.stem for p in OUTPUTS_DIR.iterdir() if p.is_file())
    if MANIFEST_PATH.is_file():
        with MANIFEST_PATH.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row.get("id"):
                    ids.add(row["id"])
    return ids


def new_output_id(taken: set[str]) -> str:
    while True:
        candidate = secrets.token_hex(4)  # 8 hex chars, meaningless on purpose
        if candidate not in taken:
            taken.add(candidate)
            return candidate


def append_csv_row(path: Path, columns: list[str], row: dict) -> None:
    """Append one row, writing the header first if the file is new/empty."""
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.is_file() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        if is_new:
            writer.writeheader()
        writer.writerow({col: row.get(col, "") for col in columns})


def download_url(url: str) -> bytes:
    try:
        import requests  # lazy: only needed when actually fetching results
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            "the 'requests' package is required to download engine output — "
            "run: pip install -r requirements.txt"
        ) from exc
    response = requests.get(url, timeout=600)
    response.raise_for_status()
    return response.content


def _collect_urls(value: object, urls: list[str]) -> None:
    if isinstance(value, str):
        if value.startswith(("http://", "https://")):
            urls.append(value)
    elif isinstance(value, dict):
        # Conventional keys first so they rank ahead of incidental URLs.
        for key in ("audio", "audio_url", "audio_file", "url", "output"):
            if key in value:
                _collect_urls(value[key], urls)
        for key, nested in value.items():
            if key not in ("audio", "audio_url", "audio_file", "url", "output"):
                _collect_urls(nested, urls)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _collect_urls(item, urls)


def find_audio_url(value: object) -> str | None:
    """Best-effort search for an audio URL inside an engine's response object.

    A URL whose path has an audio extension always wins over one without —
    otherwise a schema mismatch could silently hand us a status/request URL
    and we'd save an HTML page as a plausible-looking "cover".
    """
    urls: list[str] = []
    _collect_urls(value, urls)
    for url in urls:
        if Path(url.split("?", 1)[0]).suffix.lower() in AUDIO_EXTENSIONS:
            return url
    return urls[0] if urls else None


def resolve_output_bytes(output: object) -> bytes:
    """Turn whatever an engine client returned into raw audio bytes."""
    if isinstance(output, bytes):
        return output
    if hasattr(output, "read"):  # e.g. replicate's FileOutput
        data = output.read()  # type: ignore[union-attr]
        return data if isinstance(data, bytes) else bytes(data)
    if isinstance(output, (list, tuple)) and output:
        return resolve_output_bytes(output[0])
    url = find_audio_url(output)
    if url:
        return download_url(url)
    raise RuntimeError(f"could not locate audio in engine output: {output!r:.200}")


def guess_extension(output: object) -> str:
    """Keep the contract's .mp3 default, but respect an obvious other format."""
    url = find_audio_url(output) or ""
    suffix = Path(url.split("?", 1)[0]).suffix.lower()
    return suffix if suffix in AUDIO_EXTENSIONS else ".mp3"


# ---------------------------------------------------------------------------
# Engines (lazy imports: the kit must run its no-key preflight without any of
# these packages installed)
# ---------------------------------------------------------------------------

def run_minimax(song_path: Path, style_prompt: str) -> tuple[bytes, str]:
    """One cover via Replicate minimax/music-cover. Returns (bytes, extension)."""
    try:
        import replicate  # lazy
    except ImportError as exc:
        raise RuntimeError(
            "the 'replicate' package is not installed — "
            "run: pip install -r requirements.txt"
        ) from exc
    with song_path.open("rb") as audio_file:
        output = replicate.run(
            MINIMAX_MODEL,
            input={
                MINIMAX_FIELD_AUDIO: audio_file,
                MINIMAX_FIELD_PROMPT: style_prompt,
            },
        )
    return resolve_output_bytes(output), guess_extension(output)


def run_acestep(song_path: Path, style_prompt: str, strength: float) -> tuple[bytes, str]:
    """One cover via fal.ai ACE-Step audio-to-audio. Returns (bytes, extension)."""
    try:
        import fal_client  # lazy
    except ImportError as exc:
        raise RuntimeError(
            "the 'fal-client' package is not installed — "
            "run: pip install fal-client (it is optional in requirements.txt)"
        ) from exc
    audio_url = fal_client.upload_file(str(song_path))
    result = fal_client.subscribe(
        ACESTEP_ENDPOINT,
        arguments={
            ACESTEP_FIELD_AUDIO_URL: audio_url,
            ACESTEP_FIELD_PROMPT: style_prompt,
            ACESTEP_FIELD_STRENGTH: strength,
        },
    )
    return resolve_output_bytes(result), guess_extension(result)


# ---------------------------------------------------------------------------
# Planning
# ---------------------------------------------------------------------------

def build_plan(
    songs: list[Path], styles: list[dict], engines: list[str], limit: int | None
) -> list[dict]:
    """One dict per paid generation, in a stable, human-predictable order."""
    plan: list[dict] = []
    for song in songs:
        for style in styles:
            if "minimax" in engines:
                plan.append(
                    {
                        "song": song,
                        "style": style,
                        "engine": "minimax",
                        "strength": None,
                        "est_cost": MINIMAX_COST_PER_COVER,
                    }
                )
            if "acestep" in engines:
                for strength in ACESTEP_STRENGTHS:
                    plan.append(
                        {
                            "song": song,
                            "style": style,
                            "engine": "acestep",
                            "strength": strength,
                            "est_cost": ACESTEP_EST_COST_PER_RUN,
                        }
                    )
    if limit is not None:
        plan = plan[:limit]
    return plan


def describe_item(item: dict) -> str:
    label = f"{item['song'].name} × {item['style']['id']} via {item['engine']}"
    if item["strength"] is not None:
        label += f" (strength {item['strength']})"
    return label


def preflight(engines: list[str], songs: list[Path]) -> list[str]:
    """Return a list of human-readable problems; empty means good to go."""
    problems: list[str] = []
    if not songs:
        problems.append(
            f"No audio files found in {SONGS_DIR}/ — drop in a few songs you "
            f"legally own (extensions: {', '.join(sorted(AUDIO_EXTENSIONS))}). "
            "Short vocal songs (1-3 min) keep the test cheap."
        )
    if "minimax" in engines and not os.environ.get("REPLICATE_API_TOKEN"):
        problems.append(
            "REPLICATE_API_TOKEN is not set (needed for --engine minimax/both). "
            "Create a token at replicate.com -> account -> API tokens, then:\n"
            "      export REPLICATE_API_TOKEN=r8_..."
        )
    if "acestep" in engines and not os.environ.get("FAL_KEY"):
        problems.append(
            "FAL_KEY is not set (needed for --engine acestep/both). "
            "Create a key at fal.ai -> dashboard -> keys, then:\n"
            "      export FAL_KEY=..."
        )

    # Catch missing packages here rather than as N identical failures after
    # the user has already confirmed the spend.
    import importlib.util

    needed_packages = {"requests": "downloading engine output"}
    if "minimax" in engines:
        needed_packages["replicate"] = "--engine minimax/both"
    if "acestep" in engines:
        needed_packages["fal_client"] = "--engine acestep/both"
    missing = [name for name in needed_packages if importlib.util.find_spec(name) is None]
    if missing:
        problems.append(
            "Missing Python package(s): "
            + ", ".join(f"'{name}' ({needed_packages[name]})" for name in missing)
            + " — run: pip install -r requirements.txt"
        )
    return problems


def confirm_spend(plan: list[dict], assume_yes: bool) -> bool:
    total = sum(item["est_cost"] for item in plan)
    by_engine: dict[str, tuple[int, float]] = {}
    for item in plan:
        count, cost = by_engine.get(item["engine"], (0, 0.0))
        by_engine[item["engine"]] = (count + 1, cost + item["est_cost"])

    print("\nPlanned generations:")
    for engine, (count, cost) in sorted(by_engine.items()):
        print(f"  {engine:8s} {count:3d} runs  ≈ ${cost:.2f}")
    print(f"  {'total':8s} {len(plan):3d} runs  ≈ ${total:.2f}")
    print(
        "  (estimates: minimax ≈ $%.2f/cover; ACE-Step on fal is metered by "
        "compute time, ≈ $%.2f/run assumed — see README.md)"
        % (MINIMAX_COST_PER_COVER, ACESTEP_EST_COST_PER_RUN)
    )

    if assume_yes:
        print("\n--yes given: skipping confirmation.")
        return True
    try:
        answer = input(f"\nSpend ≈ ${total:.2f} and start? [y/N] ")
    except EOFError:
        print("\nNo interactive terminal detected — re-run with --yes to confirm.")
        return False
    return answer.strip().lower() in ("y", "yes")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="run_test.py",
        description=(
            "Generate blind-graded style-transfer covers of the songs in "
            "./songs/ using MiniMax music-cover (Replicate) and optionally "
            "ACE-Step audio-to-audio (fal.ai)."
        ),
        epilog=(
            "examples:\n"
            "  python3 run_test.py --engine minimax\n"
            "  python3 run_test.py --engine both --styles kids-choir,bossa-nova\n"
            "  python3 run_test.py --engine acestep --limit 6 --yes\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--engine",
        choices=("minimax", "acestep", "both"),
        default="minimax",
        help="which engine(s) to test (default: minimax)",
    )
    parser.add_argument(
        "--styles",
        default="all",
        metavar="ID[,ID...]",
        help="comma-separated style ids from prompts.json (default: all)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="cap the total number of paid generations (spend control)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="skip the cost confirmation prompt (for non-interactive runs)",
    )
    return parser.parse_args(argv)


def select_styles(all_styles: list[dict], spec: str) -> list[dict]:
    if spec.strip().lower() in ("", "all"):
        return all_styles
    by_id = {style["id"]: style for style in all_styles}
    selected: list[dict] = []
    for raw in spec.split(","):
        style_id = raw.strip()
        if not style_id:
            continue
        if style_id not in by_id:
            die(
                f"unknown style id '{style_id}'. "
                f"Valid ids: {', '.join(by_id)}"
            )
        if by_id[style_id] not in selected:
            selected.append(by_id[style_id])
    if not selected:
        die("--styles selected no styles")
    return selected


def run_plan(plan: list[dict]) -> tuple[int, int]:
    """Execute the plan item by item. Returns (succeeded, failed)."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    taken_ids = existing_output_ids()
    succeeded = failed = 0

    for index, item in enumerate(plan, start=1):
        label = describe_item(item)
        print(f"\n[{index}/{len(plan)}] {label}")
        output_id = new_output_id(taken_ids)
        started = time.monotonic()
        try:
            if item["engine"] == "minimax":
                audio, extension = run_minimax(
                    item["song"], item["style"]["stylePrompt"]
                )
            else:
                audio, extension = run_acestep(
                    item["song"], item["style"]["stylePrompt"], item["strength"]
                )
            output_path = OUTPUTS_DIR / f"{output_id}{extension}"
            output_path.write_bytes(audio)
        except KeyboardInterrupt:
            print("\nInterrupted — results so far are already in the CSVs.")
            raise
        except Exception as exc:  # per-item isolation: record and keep going
            failed += 1
            elapsed = time.monotonic() - started
            error_text = f"{type(exc).__name__}: {exc}"
            print(f"    FAILED after {elapsed:.0f}s — {error_text}")
            append_csv_row(
                MANIFEST_PATH,
                MANIFEST_COLUMNS,
                {
                    "id": output_id,
                    "song": item["song"].name,
                    "engine": item["engine"],
                    "style": item["style"]["id"],
                    "strength": "" if item["strength"] is None else item["strength"],
                    "status": "failed",
                    "error": error_text[:500],
                },
            )
            continue

        succeeded += 1
        elapsed = time.monotonic() - started
        print(f"    ok in {elapsed:.0f}s -> {output_path.relative_to(KIT_DIR)}")
        append_csv_row(
            MANIFEST_PATH,
            MANIFEST_COLUMNS,
            {
                "id": output_id,
                "song": item["song"].name,
                "engine": item["engine"],
                "style": item["style"]["id"],
                "strength": "" if item["strength"] is None else item["strength"],
                "status": "succeeded",
                "error": "",
            },
        )
        append_csv_row(GRADING_PATH, GRADING_COLUMNS, {"id": output_id})

    shuffle_grading_rows()
    return succeeded, failed


def shuffle_grading_rows() -> None:
    """Rewrite grading.csv ordered by random id, not generation order.

    The plan order is deterministic (songs × styles × engines), so rows appended
    in run order would let a grader reconstruct each item's style from its row
    position alone. Sorting by the random hex id breaks that correlation; graders
    should also open files by id, not by file creation time.
    """
    if not GRADING_PATH.exists():
        return
    with GRADING_PATH.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    rows.sort(key=lambda row: row.get("id", ""))
    with GRADING_PATH.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=GRADING_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.limit is not None and args.limit < 1:
        die("--limit must be at least 1")

    engines = ["minimax", "acestep"] if args.engine == "both" else [args.engine]
    all_styles = load_styles()
    styles = select_styles(all_styles, args.styles)
    songs = discover_songs()

    problems = preflight(engines, songs)
    if problems:
        print("Cannot start yet — the following need fixing first:\n")
        for number, problem in enumerate(problems, start=1):
            print(f"  {number}. {problem}\n")
        print(
            "Nothing was run and nothing was spent. Fix the above and re-run, "
            "e.g.:  python3 run_test.py --engine minimax --styles kids-choir"
        )
        return 2

    plan = build_plan(songs, styles, engines, args.limit)
    print(
        f"Songs: {len(songs)}  ·  Styles: {len(styles)} "
        f"({', '.join(s['id'] for s in styles)})  ·  "
        f"Engines: {', '.join(engines)}"
        + (f"  ·  Limit: {args.limit}" if args.limit is not None else "")
    )
    if not plan:
        die("nothing to do (empty plan)")

    if not confirm_spend(plan, args.yes):
        print("Aborted — nothing was spent.")
        return 1

    try:
        succeeded, failed = run_plan(plan)
    except KeyboardInterrupt:
        return 130

    print(
        f"\nDone: {succeeded} succeeded, {failed} failed "
        f"(details in {MANIFEST_PATH.relative_to(KIT_DIR)})."
    )
    if succeeded:
        print(
            f"Next: have listeners grade blind using "
            f"{GRADING_PATH.relative_to(KIT_DIR)} — see README.md for the "
            "pass bar. Keep manifest.csv away from graders until scores are in."
        )
    return 0 if succeeded or not plan else 1


if __name__ == "__main__":
    sys.exit(main())
