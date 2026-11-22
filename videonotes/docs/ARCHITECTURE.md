# videonotes — architecture contract

videonotes turns footage from a worn action camera (DJI Osmo Action 4 / 5 Pro) into
searchable notes on a 16 GB Mac, locally. This document is the contract every module is
built against: who owns which file, the exact public functions, and the rules that keep
the pieces interchangeable.

## 1. The idea in one picture

```
 CAPTURE (3 ways in)                      PIPELINE (per clip)                         NOTES
 ───────────────────                      ───────────────────                         ─────
 USB webcam mode ─┐                       probe      duration, size, start time
   (live, ffmpeg  │   60 s segments       extract    16 kHz WAV  +  sparse keyframes  moments  (segment)
    avfoundation) ├─►  = "clips"  ───────► transcribe speech → utterances             summaries (LLM or
 Wi-Fi RTMP push ─┤                       ocr        text on keyframes                 extractive)
   (camera told   │                       caption    what the wearer is looking at    Markdown vault
    over BLE)     │                                  (budgeted, most novel frames)    SQLite FTS search
 SD card / USB ───┘   .LRF proxies                                                    ask-your-day
   import             = "clips"           then per session: segment → summarize → render
```

Everything after capture is the same code path: a **clip** is just a media file with a known
wall-clock start time. Live capture produces clips by cutting the stream into fixed
segments; import produces clips from the camera's files (preferring DJI's low-res `.LRF`
proxy so 4K never has to be decoded).

### Why it is cheap enough for a laptop

1. **Never analyse full-rate, full-size video.** One ffmpeg pass decodes at 2 fps / 320 px
   grayscale into a pipe; numpy picks a handful of sharp, novel frames; only those are
   extracted at readable size. A minute of video becomes ~2–8 JPEGs.
2. **Audio carries most of the meaning.** Speech-to-text runs on 16 kHz mono with silence
   skipped; it is the bulk of a note. Video adds what audio cannot: text in view
   (whiteboards, slides, screens, signs), where you were, what you were doing.
3. **Cheap perception first.** OCR runs on every keyframe (fast, on-device). The expensive
   vision-language caption runs only on a budgeted subset (most novel frames).
4. **One heavy model in RAM at a time.** Stages run stage-by-stage over all pending clips;
   each backend is `close()`d before the next loads.
5. **Idempotent, resumable stages.** Every stage records `done` per clip in SQLite, so a
   crash or Ctrl-C loses at most one clip-stage and re-runs are free.

## 2. Conventions (binding on every module)

* Python ≥ 3.11, `src/` layout, package `videonotes`, CLI `vnote`.
* **Time**: `ts` = UNIX epoch seconds UTC (float); `t` = seconds from clip start;
  `ts = clip.start_ts + t`. Local time only at the presentation edge (`timeutil`).
* **Paths in the DB** are relative to home (`Settings.rel()` / `Settings.abs()`).
* **Core dependency is numpy only.** Everything else (mlx, onnxruntime, pyobjc, bleak,
  anthropic, …) is optional, imported lazily *inside functions*, and its absence produces a
  `BackendUnavailable` with an exact install command — never an `ImportError` at import time.
* **ffmpeg** is only ever invoked through `videonotes.media.ffmpeg` (`run`, `base_cmd`, `probe`).
* **No network by default.** Cloud backends are used only when explicitly selected in
  config (`backend = "anthropic"`); `auto` never picks one.
* **Errors**: raise the typed exceptions (`FFmpegError`, `BackendUnavailable`, `BackendError`,
  or a module-specific subclass of `RuntimeError`) with a message a non-expert can act on.
  The pipeline catches per clip-stage, records `error`, and carries on.
* **Logging**: `logging.getLogger("videonotes.<module>")`; no `print` outside `cli.py`.
* **Tests**: pytest, under `tests/`, runnable on Linux CI without a Mac, camera, GPU or
  network. macOS-only code paths are unit-tested by mocking the OS boundary (command
  builders are pure functions that return argv lists; parsers take captured text).
  Shared fixtures in `tests/conftest.py`: `settings`, `store`, `demo_video` (synthetic clip
  with known speech + on-screen text, see `videonotes.demo.DEMO_SCENES`), and
  `tests/fake_ollama.py::FakeOllama`.
* Style: type hints everywhere, `from __future__ import annotations`, line length 110.

## 3. Spine (already written — do not change signatures; extend only by adding)

| File | What it provides |
|---|---|
| `models.py` | `Session`, `Clip`, `Keyframe`, `Utterance`, `Moment`, `SessionNote`, `ActionItem`, `DayDigest`, `SearchHit`, stage name tuples |
| `config.py` | `Settings` (+ section dataclasses), `load_settings`, layout properties, `rel`/`abs`, `is_macos`, `is_apple_silicon`, `DJI_DEVICE_HINTS` |
| `store.py` | `Store` — all SQL: sessions, clips (+ stage status), keyframes, utterances, moments, days, FTS `search()` |
| `timeutil.py` | ids, local-day bounds, formatting, `slugify` |
| `media/ffmpeg.py` | `ffmpeg_bin`, `run`, `base_cmd`, `probe -> MediaInfo`, `has_encoder/has_filter/has_hwaccel/has_input_format`, `FFmpegError` |
| `backends/base.py` | Protocols `Transcriber`, `OcrEngine`, `Captioner`, `LLM`; `TranscriptSegment`, `OcrLine`, `OcrResult`; `BackendUnavailable`, `BackendError` |
| `backends/jsonutil.py` | `extract_json`, `coerce_to_schema`, `schema_prompt` |
| `backends/ollama_client.py` | `OllamaClient` (`is_running`, `list_models`, `first_available`, `chat`, `unload`) |
| `backends/anthropic_client.py` | `ClaudeClient.complete(...)`, `DEFAULT_MODEL` |
| `demo.py` | `make_demo_video`, `DEMO_SCENES` |

## 4. Components and their public surface

Each component owns its files exclusively. Functions listed here are the contract; private
helpers are free-form.

### 4.1 `media/audio.py`, `media/keyframes.py` — media analysis

```python
# media/audio.py
class NoAudioError(FFmpegError): ...
def extract_audio(src: Path, dst_wav: Path, *, start: float | None = None,
                  duration: float | None = None) -> float
    """Write 16 kHz mono 16-bit PCM WAV; return its duration (s). NoAudioError if src has no audio."""
def read_wav(path: Path) -> np.ndarray            # float32 mono in [-1, 1], 16 kHz
def write_wav(path: Path, samples: np.ndarray, rate: int = 16000) -> None
@dataclass
class SpeechSpan: t0: float; t1: float
def detect_speech(samples: np.ndarray, rate: int = 16000, *, min_speech_s: float = 0.25,
                  min_silence_s: float = 0.6, pad_s: float = 0.25) -> list[SpeechSpan]
    """Energy/spectral VAD in numpy. Conservative: prefers false positives over dropped speech."""
def speech_ratio(spans: list[SpeechSpan], duration: float) -> float

# media/keyframes.py
@dataclass
class FrameCandidate: t: float; sharpness: float; novelty: float; reason: str
def select_keyframes(src: Path, cfg: FrameSettings, *, duration: float | None = None,
                     hwaccel: bool = True) -> list[FrameCandidate]
    """Single low-res decode pass; returns chosen times in ascending order."""
def extract_frames(src: Path, times: list[float], out_dir: Path, *, width: int = 1280,
                   quality: int = 3, prefix: str = "kf") -> list[Path]
    """One JPEG per requested time (same order). Never upscales. Accurate seeking."""
```

### 4.2 `backends/asr.py` — speech to text

```python
def make_transcriber(settings: Settings) -> Transcriber | None
    """None when asr.backend == 'none', or when 'auto' finds nothing usable.
    Raises BackendUnavailable when an explicitly chosen backend cannot run."""
def asr_status(settings: Settings) -> list[BackendStatus]      # for `vnote doctor`
```

`BackendStatus` (defined in `backends/status.py`, spine):
`name: str, available: bool, detail: str, selected: bool` — `detail` is the install/start
instruction when unavailable, or the resolved model when available.

Every factory follows the same rule: explicit backend → use it or raise
`BackendUnavailable`; `auto` → first available in the documented preference order, else
`None` (the pipeline records the stage as `skipped` with the reason and continues).

### 4.3 `backends/ocr.py`, `backends/vision.py` — reading and describing frames

```python
def make_ocr(settings: Settings) -> OcrEngine | None
def ocr_status(settings: Settings) -> list[BackendStatus]
def clean_ocr_text(result: OcrResult, *, min_confidence: float, min_chars: int) -> str
    """Drop low-confidence / junk lines; normalise whitespace."""

def make_captioner(settings: Settings) -> Captioner | None
def vision_status(settings: Settings) -> list[BackendStatus]
CAPTION_PROMPT: str      # the shared instruction every captioner backend uses
```

### 4.4 `backends/llm.py` — text LLM

```python
def make_llm(settings: Settings) -> LLM | None      # None => callers use extractive fallbacks
def llm_status(settings: Settings) -> list[BackendStatus]
```

### 4.5 `notes/` — from perception to notes

```python
# notes/moments.py
def segment_moments(session: Session, utterances: list[Utterance], keyframes: list[Keyframe],
                    cfg: NotesSettings) -> list[Moment]
    """Split a session into moments at long speech pauses and strong visual changes,
    honouring moment_min_seconds / moment_max_seconds. Deterministic; no LLM."""

# notes/summarize.py
def moment_context(moment: Moment, utterances: list[Utterance], keyframes: list[Keyframe],
                   *, max_chars: int = 6000) -> str
    """The fused evidence for one moment: timestamped speech, on-screen text, captions."""
def summarize_moments(llm: LLM | None, session: Session, moments: list[Moment],
                      utterances: list[Utterance], keyframes: list[Keyframe]) -> list[Moment]
    """Fill title / summary / tags of each moment (LLM, or extractive when llm is None)."""
def summarize_session(llm: LLM | None, session: Session, moments: list[Moment],
                      utterances: list[Utterance], keyframes: list[Keyframe]) -> SessionNote
def summarize_day(llm: LLM | None, date: str, sessions: list[Session]) -> DayDigest
def answer_question(llm: LLM | None, question: str, evidence: list[Evidence]) -> Answer

# notes/render.py
def render_session_note(settings: Settings, store: Store, session_id: str) -> Path
    """Write <vault>/sessions/<date> <time> <title>.md (+ copies of embedded keyframes
    under <vault>/assets/<session_id>/). Returns the Markdown path. Re-rendering a session
    replaces its previous file even if the title changed."""
def render_day_note(settings: Settings, store: Store, date: str) -> Path
```

Summaries must never invent: every prompt instructs the model to use only the supplied
evidence, and extractive fallbacks only quote. A `SessionNote` records which backend wrote
it in `llm_backend`.

### 4.6 `capture/` — getting media in

```python
# capture/devices.py
@dataclass
class CaptureDevice: index: int; name: str; kind: str      # kind: "video" | "audio"
def parse_avfoundation_devices(stderr_text: str) -> list[CaptureDevice]
def list_devices() -> list[CaptureDevice]                   # macOS only; [] elsewhere
def pick_device(devices: list[CaptureDevice], kind: str, wanted: str) -> CaptureDevice | None

# capture/live.py
@dataclass
class Segment: path: Path; start_ts: float; duration: float
def webcam_command(settings: Settings, video: CaptureDevice, audio: CaptureDevice | None,
                   out_dir: Path) -> list[str]
def rtmp_listen_command(settings: Settings, out_dir: Path) -> list[str]
class SegmentRecorder:
    """Runs one ffmpeg process that writes fixed-length segments and reports each
    segment once it is complete (i.e. once ffmpeg has moved on to the next file)."""
    def __init__(self, command: list[str], out_dir: Path, *, segment_seconds: int): ...
    def start(self) -> None
    def poll(self) -> list[Segment]        # newly completed segments, oldest first
    def stop(self) -> list[Segment]        # terminate ffmpeg cleanly; return the final segments
    @property
    def running(self) -> bool
    def last_error(self) -> str

# capture/importer.py
@dataclass
class CardClip:
    original: Path; proxy: Path | None; start_ts: float; size: int; index: int | None
def find_camera_volumes() -> list[Path]
def scan_card(root: Path) -> list[CardClip]
def group_into_sessions(clips: list[CardClip], gap_seconds: float) -> list[list[CardClip]]
def clip_fingerprint(path: Path) -> str
def import_clips(settings: Settings, store: Store, clips: list[CardClip], *, source: str,
                 kind: str = "import") -> list[Session]
    """Create sessions + clips (copying media per imports.copy_media); skips known fingerprints."""
def import_file(settings: Settings, store: Store, path: Path, *, start_ts: float | None = None) -> Session
```

### 4.7 `dji/` — camera control over Bluetooth LE

```python
# dji/rsdk.py     official "DJI R SDK" framing (record start/stop, status, mode, sleep)
# dji/duml.py     reverse-engineered framing used to join Wi-Fi + start RTMP livestream
# dji/camera.py   high-level async API on top of bleak
@dataclass
class FoundCamera: address: str; name: str; rssi: int | None; model: str | None
async def scan(timeout: float = 8.0, name_filter: str = "") -> list[FoundCamera]
class OsmoCamera:
    def __init__(self, address: str, *, model: str = "auto"): ...
    async def connect(self) -> None
    async def disconnect(self) -> None
    async def pair(self) -> None
    async def start_recording(self) -> None
    async def stop_recording(self) -> None
    async def status(self) -> CameraStatus
    async def start_livestream(self, *, ssid: str, password: str, rtmp_url: str,
                               resolution: str, bitrate_kbps: int, fps: int) -> None
    async def stop_livestream(self) -> None
```

Protocol encoders/decoders are pure functions with byte-exact tests against vectors taken
from the reference implementations. Nothing in `dji/` could be tested on hardware when it
was written; `camera.py` therefore logs every frame sent/received at DEBUG level.

### 4.8 `pipeline.py`, `search.py`, `cli.py`, `web/` — orchestration and UI

```python
# pipeline.py
class Pipeline:
    def __init__(self, settings: Settings, store: Store, *, progress: Progress | None = None): ...
    def process_session(self, session_id: str, *, force: Iterable[str] = ()) -> Session
        """Run every pending clip stage (stage-major, one model loaded at a time), then
        segment → summarize → render. Safe to call repeatedly."""
    def process_clip_light(self, clip_id: int) -> None
        """Live mode: probe + extract + transcribe + ocr for one fresh segment."""
    def finalize_session(self, session_id: str) -> Session
    def build_day(self, date: str) -> Path
    def close(self) -> None

# search.py
def search(store: Store, query: str, **filters) -> list[SearchHit]
def ask(settings: Settings, store: Store, question: str, *, llm: LLM | None = None) -> Answer
```

CLI (`vnote …`): `doctor`, `init`, `demo`, `devices`, `live`, `wireless`, `import`, `add`,
`process`, `sessions`, `show`, `day`, `search`, `ask`, `camera scan|pair|record|status`,
`web`, `config`.

## 5. Notes model

* **Session** — one live run, or imported clips recorded close together.
* **Moment** — a coherent span inside a session (a conversation, a task, a place).
* **SessionNote** — title, summary, key points, action items (owner / due only if stated),
  decisions, open questions, people, places, captured text, tags.
* **DayDigest** — headline, summary, highlights, merged action items for a local calendar day.

The Markdown vault (`<home>/notes`, Obsidian-compatible):

```
notes/
  days/2026-11-22.md
  sessions/2026-11-22 1432 Planning meeting.md
  assets/<session_id>/kf_000123.jpg
```
