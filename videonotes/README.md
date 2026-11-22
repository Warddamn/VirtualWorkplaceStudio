# videonotes

Video note-taking for a body-worn action camera: the video equivalent of the audio "AI pendants"
(Limitless, Bee, Omi, Plaud). Wear a **DJI Osmo Action 4 or Osmo Action 5 Pro**, and your Mac turns
the footage into searchable notes: what was said, what was written on whiteboards, slides, signs and
screens, decisions, action items, and a digest of the day.

Everything runs **locally on the Mac** (built for 16 GB of RAM). Nothing leaves the laptop unless you
explicitly configure a cloud model.

```
 three ways in                         per clip                              out
 ─────────────                         ────────                              ───
 SD card / USB import  ─┐              speech → text (silence skipped)       Markdown notes per session
 USB webcam, live       ├─► clips ──►  a few sharp, new frames per minute ►  + a digest per day
 Wi-Fi, live (via BLE)  ─┘             text read off those frames (OCR)      full-text search
                                       short descriptions of some frames     "ask your day"
                                                                             local web viewer
```

What video adds over an audio pendant: it reads the whiteboard, slide, sign or screen in front of you
(audio can't), it shows *where* you were and *what* you were doing, and every note embeds the frames
it rests on so you can check it.

> **Status: v0.1, built and tested without the hardware.** Everything runs and is tested on a Linux
> machine with synthetic footage (about 2,000 automated tests, plus an end-to-end run of the whole
> pipeline). Nothing has yet touched a real DJI camera or a Mac. The camera protocols were
> implemented byte-for-byte from DJI's own sample code and from open-source projects that reverse
> engineered the livestream setup, but expect to adjust details on first contact. The
> [first hour with the camera](#first-hour-with-the-real-camera) section is the checklist for that.

---

## Install (once)

You need a Mac with macOS 14 or newer. Apple Silicon (M1 or later) is the main target; Intel Macs
work with slower, CPU-only models.

```sh
# 1. Tools: Homebrew from https://brew.sh first, then
brew install uv ffmpeg

# 2. The local model server, for frame descriptions and written summaries (optional but recommended)
brew install ollama            # or download the app from https://ollama.com
ollama serve &                 # or just open the Ollama app
ollama pull qwen3-vl:4b-instruct   # describes frames (~3.3 GB). If that tag is missing: qwen3-vl:4b
ollama pull qwen3:4b               # writes summaries (~2.6 GB)

# 3. videonotes itself
git clone https://github.com/warddamn/VirtualWorkplaceStudio.git
cd VirtualWorkplaceStudio/videonotes
uv venv --python 3.12
uv pip install -e '.[mac]'     # picks the right speech model for Apple Silicon vs Intel
source .venv/bin/activate

# 4. Set up the library (~/VideoNotes) and check everything
vnote init
vnote demo                     # runs the whole pipeline on a generated sample clip
```

`vnote init` / `vnote doctor` list every component, mark what is in use, and print the exact command
for anything missing. The first transcription downloads the speech model (about 1.3 GB on Apple
Silicon) once.

Without Ollama everything still works: notes are then built from quotes of what was said and shown
("extractive") instead of being written by a language model, and frames are read (OCR) but not
described.

**Permissions.** macOS asks the *terminal app* (Terminal, iTerm, VS Code …) for access, not
videonotes. Allow **Camera** and **Microphone** for `vnote live`, **Bluetooth** for `vnote camera` and
`vnote wireless`, and **Removable Volumes** for `vnote import`. If you clicked "Don't Allow", fix it
in System Settings → Privacy & Security.

---

## Using it

### 1. Record on the camera, import later (the main way)

Record as usual. Afterwards plug the camera into the Mac with USB-C and choose the **file transfer**
option on its screen (or put the microSD card in a reader), then:

```sh
vnote import --dry-run         # what is new on the card
vnote import                   # copy, process, write notes
```

Import never writes to or deletes anything on the card. It copies the camera's low-resolution
**.LRF proxy** files (about 10 % of the size), analyses those, and cuts the stills it keeps from the
full-quality originals while the card is still connected, because a proxy is too blurry to read a
whiteboard. **Keep the camera connected until "Extracting audio and keyframes" has finished.**
Clips recorded close together become one session. `vnote import /some/folder` and
`vnote add file.mp4` work for any video, from any camera.

### 2. Live over USB (at a desk)

Plug the camera in and choose **Webcam** on its screen.

```sh
vnote devices                  # the camera should be marked "← camera"
vnote live                     # speech and on-screen text appear as you go; Ctrl-C finishes
```

Video is cut into 60-second segments that are processed while you record. When you stop, the
frames get described and the summary is written. The Osmo Action 4 sends its microphone over USB;
the Action 5 Pro does so from firmware 01.01.05.20. Without a camera microphone, the Mac's
microphone is used (`--audio default` forces it, `--audio none` records video only).

### 3. Live over Wi-Fi (camera worn, Mac nearby)

The Mac tells the camera over Bluetooth to join your Wi-Fi network and stream to it:

```sh
vnote camera pair              # once: confirm the prompt on the camera's screen
vnote wireless --ssid "Your Wi-Fi"     # asks for the Wi-Fi password; Ctrl-C finishes
```

If Bluetooth setup gives you trouble, `vnote wireless --manual` only listens, and you start the RTMP
livestream yourself in the DJI Mimo app with the address `vnote` prints. Allow incoming connections
if macOS asks.

### Camera control

```sh
vnote camera scan              # which DJI cameras are nearby, and which model
vnote camera status            # mode, recording, battery, card space
vnote camera record start      # … stop
```

### Reading your notes

```sh
vnote day                      # today's digest (or: vnote day yesterday / 2026-11-22)
vnote sessions                 # list
vnote show                     # the latest session (or an id / id prefix); --open opens the Markdown
vnote search whiteboard falcon # speech, on-screen text, descriptions, notes
vnote ask "where did I park?"  # answers from the evidence, and shows it with --sources
vnote web                      # browse everything at http://127.0.0.1:8765 (local only)
```

Notes are plain Markdown in `~/VideoNotes/notes` (an Obsidian-compatible folder: point
`notes.vault` in the config at your own vault if you like):

```
notes/days/2026-11-22.md
notes/sessions/2026-11-22 1432 Planning meeting.md     ← with the frames it rests on
notes/assets/<session>/kf_….jpg
```

A session note has a summary, key points, action items (as checkboxes; owners and due dates only if
they were actually said or shown), decisions, open questions, the text captured from surfaces, and a
timeline of moments with their frames and transcript. Quiet stretches (walking, waiting) are
collapsed. Ticking an action item in the Markdown survives re-processing.

### Housekeeping

```sh
vnote process                  # finish anything interrupted (everything is resumable)
vnote process latest --force summarize   # redo one stage, e.g. after installing Ollama
vnote delete <session>         # removes its media copies, frames, note and search entries
vnote config --init            # writes ~/VideoNotes/config.toml with every setting explained
vnote --set vision.backend=none import   # any setting can be overridden for one run
```

---

## Recommended camera settings ("video pendant")

From the research behind this project; none of it has been tried on your camera yet.

| Setting | Value | Why |
|---|---|---|
| Mode / resolution | Video, **1080p, 24 or 30 fps** | lowest option; the rated battery life assumes it |
| Codec | HEVC (H.264 on an older Intel Mac) | smaller files; the proxy is H.264 either way |
| Colour | Normal 8-bit (no D-Log / HLG / 10-bit) | cheaper to decode, natural colours for the models |
| FOV | **Standard (Dewarp)** when reading text matters, Wide for context | straight lines are easier to read |
| Stabilisation | RockSteady (not RockSteady+ / Horizon) | less crop |
| Screen off when recording | 3 s | battery and heat |
| Wi-Fi | off while worn (unless using `vnote wireless`) | battery |
| Loop recording / Pre-Rec | off | so nothing is overwritten before import |
| Clock | sync once with DJI Mimo | file names carry the camera's local time |

Expect about **2.5 h (Action 4) / 4 h (Action 5 Pro) per battery** at 1080p and roughly
**10–20 GB per hour** on the card. All-day capture needs spare batteries or USB power. For
documents, a still photo beats any video frame: photos on the card are imported too and read at full
resolution.

---

## Choosing models

`auto` picks the best thing that is installed. What it resolves to:

| Job | Apple Silicon | Intel Mac | Without extras |
|---|---|---|---|
| Speech → text | Parakeet TDT 0.6B v3 (MLX) | faster-whisper `small` (int8) | sherpa-onnx Parakeet (CPU) |
| Text in frames | Apple Vision (on-device) | Apple Vision | RapidOCR (CPU) |
| Frame descriptions | Ollama `qwen3-vl:4b-instruct` | Ollama, or off | off |
| Summaries / ask | Ollama `qwen3:4b` | Ollama `qwen3:4b` (slow on CPU) | extractive quotes |

Only one model is in memory at a time: the pipeline runs speech for all clips, then OCR, then
descriptions, then summaries, unloading in between, so a 16 GB Mac stays usable. Frame descriptions
are the slow part (seconds per frame), so they are budgeted to the most novel frames
(`vision.max_per_minute`, default 2). Rough estimate for a heavy day (8 h recorded, 2 h of speech) on
a base M-series chip: under an hour of processing, most of it frame descriptions. These numbers are
extrapolations to be confirmed on your Mac.

**Cloud (opt-in only).** `pip install 'videonotes[cloud]'`, set `ANTHROPIC_API_KEY`, and set
`backend = "anthropic"` under `[vision]` and/or `[llm]` in `config.toml` to use Claude. `auto` never
picks a cloud backend: frames and transcripts of your day stay local unless you say otherwise.

---

## First hour with the real camera

Nothing below could be tested without the hardware. Run these in order and note what happens; each
step exercises one untested assumption.

1. `vnote camera scan`: tells you whether you have an **Action 4 or Action 5 Pro** (from the
   Bluetooth advertisement). If nothing is found, check the Bluetooth permission for your terminal
   app and that the camera is awake.
2. Plug in, choose **file transfer**, run `vnote doctor`: the card should be listed under Camera.
   Then `vnote import --dry-run`. If the card is not found, the camera may not mount as a plain disk:
   use a card reader, or `vnote import /Volumes/<name>`.
3. `vnote import` on one short clip. Check the note, and whether the speech came through (the
   research could not establish whether the proxy files carry audio; the pipeline falls back to the
   original for sound).
4. Choose **Webcam**, then `vnote devices` and `vnote live --minutes 2`. If capture fails, try
   `--set capture.video_size=1280x720` or `--set capture.framerate=25`.
5. `vnote camera pair` and `vnote camera status`, then `vnote camera record start` / `stop`.
6. `vnote wireless --ssid "…" --minutes 2`. If the camera does not start streaming, run it again with
   `-vv` (every Bluetooth frame sent and received is logged), and try `vnote wireless --manual`
   with the DJI Mimo app to separate a Bluetooth problem from a network one.

Known limits:

- A Mac cannot wake a sleeping camera over Bluetooth (DJI's wake-up packet can't be sent by
  macOS), so videonotes never puts the camera to sleep.
- The camera sends no confirmation that its stream reached the Mac; arriving video is the proof.
- The keyframe sensitivity (`frames.novelty_threshold`, default 0.25) was tuned on synthetic
  footage. If notes have too many near-identical frames while you walk, raise it; if a new line on a
  whiteboard is missed, lower it.

---

## Privacy and recording other people

You are recording other people, which is legal in some places and situations and not in others.
In the US, audio recording needs the consent of every party in about a dozen states; video of people
in private spaces is restricted almost everywhere; in the EU the household exemption is read
narrowly; and many workplaces forbid recording. This is orientation, not legal advice. Tell people
you are recording, keep the camera visible, and turn it off where recording is not appropriate.

videonotes helps by keeping everything local, never writing to the camera's card, letting you
choose what media is kept (`import.copy_media = "proxy" | "original" | "none"`), and deleting a
session and everything derived from it with one command.

---

## For developers

```sh
uv pip install -e '.[dev]'
pytest                          # ~2,000 tests, about 2-3 minutes, no network, no camera, no Mac needed
ruff check src tests
```

`docs/ARCHITECTURE.md` is the design contract: data model and time conventions, the stage-major
pipeline, and the interfaces each component implements. Components:

| Package | What |
|---|---|
| `capture/` | device discovery, live segment recording (USB and RTMP), card import |
| `media/` | ffmpeg helper, audio and speech detection, keyframe selection |
| `backends/` | speech-to-text, OCR, frame descriptions, LLMs (local and opt-in cloud) |
| `notes/` | moments, summaries, Markdown rendering |
| `dji/` | Bluetooth LE: DJI's official R SDK (record, status) and the livestream setup protocol |
| `pipeline.py`, `store.py`, `search.py` | orchestration, the SQLite library with full-text search, ask |
| `cli/`, `web/` | the `vnote` command and the local web viewer |
