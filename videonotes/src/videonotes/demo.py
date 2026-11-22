"""Synthetic sample footage, so the whole pipeline can be tried without a camera.

``vnote demo`` builds a ~80 second clip that mimics what matters in real
wearable footage: several distinct scenes, a "whiteboard" and a "door sign"
with readable text, spoken notes-to-self, and a silent stretch.  It is also
the shared fixture for the test-suite.

Speech uses the macOS ``say`` command when available, otherwise ffmpeg's
``flite`` filter if this ffmpeg has it, otherwise the clip is silent (and
``DemoInfo.has_speech`` is False).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .media import ffmpeg as ff


@dataclass
class DemoScene:
    name: str
    duration: float
    background: str  # an ffmpeg lavfi video source without size/rate/duration
    lines: list[str] = field(default_factory=list)  # text drawn on screen
    speech: str = ""  # words spoken during the scene
    text_color: str = "black"
    t0: float = 0.0  # filled in by make_demo_video


#: What the demo "day" contains. Tests assert that the pipeline recovers these.
DEMO_SCENES: list[DemoScene] = [
    DemoScene(
        name="desk",
        duration=18,
        background="testsrc2",
        speech="Okay, quick note to self. Remember to email the quarterly budget to Sarah before Friday.",
    ),
    DemoScene(
        name="whiteboard",
        duration=24,
        background="color=c=0xF4F4F0",
        lines=["Launch plan Q3", "Ship Falcon beta by June 14", "Action: call vendor about sensors"],
        speech=(
            "This is the whiteboard from the planning meeting. "
            "We decided to ship the Falcon beta on June fourteenth. "
            "I need to call the vendor about the sensors."
        ),
    ),
    DemoScene(
        name="door-sign",
        duration=16,
        background="color=c=0x1E3A5F",
        lines=["Room 4B", "Design Review 3 PM"],
        text_color="white",
        speech="The design review is in room four B at three P M.",
    ),
    DemoScene(name="walking", duration=14, background="mandelbrot"),
    DemoScene(
        name="parking",
        duration=10,
        background="color=c=0x3B3B3B",
        lines=["LEVEL 2", "ROW G 27"],
        text_color="yellow",
        speech="I parked the car on level two, row G.",
    ),
]

_FONT_CANDIDATES = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
)


@dataclass
class DemoInfo:
    path: Path
    duration: float
    scenes: list[DemoScene]
    has_speech: bool
    has_text: bool


def _speech_engine() -> str | None:
    if sys.platform == "darwin" and shutil.which("say"):
        return "say"
    if ff.has_filter("flite"):
        return "flite"
    return None


def _synthesise(text: str, out_wav: Path, engine: str, workdir: Path) -> bool:
    """Write ``text`` as a 16 kHz mono WAV. Returns False if synthesis failed."""
    try:
        if engine == "say":
            aiff = workdir / (out_wav.stem + ".aiff")
            subprocess.run(["say", "-o", str(aiff), text], check=True, capture_output=True, timeout=120)
            ff.run(["-i", str(aiff), "-ar", "16000", "-ac", "1", str(out_wav)], timeout=120)
        else:
            textfile = workdir / (out_wav.stem + ".txt")
            textfile.write_text(text, encoding="utf-8")
            ff.run(
                ["-f", "lavfi", "-i", f"flite=textfile={_esc(textfile)}:voice=slt", "-ar", "16000", "-ac", "1", str(out_wav)],
                timeout=120,
            )  # fmt: skip
    except (ff.FFmpegError, OSError, subprocess.SubprocessError):
        return False
    return out_wav.is_file() and out_wav.stat().st_size > 1000


def _esc(path: Path) -> str:
    """Escape a path for use inside an ffmpeg filter argument."""
    return str(path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace(",", "\\,")


def make_demo_video(
    out: str | Path,
    *,
    size: str = "1280x720",
    fps: int = 30,
    scenes: list[DemoScene] | None = None,
    speech: bool = True,
    creation_time: str | None = None,
) -> DemoInfo:
    """Render the demo clip to ``out`` (H.264 + AAC MP4)."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    scenes = [DemoScene(**{**s.__dict__}) for s in (scenes or DEMO_SCENES)]
    engine = _speech_engine() if speech else None
    can_text = ff.has_filter("drawtext")
    font = next((f for f in _FONT_CANDIDATES if Path(f).is_file()), None)
    width, height = (int(x) for x in size.split("x"))
    spoke = False
    drew = False

    with tempfile.TemporaryDirectory(prefix="videonotes-demo-") as tmp:
        work = Path(tmp)
        parts: list[Path] = []
        t = 0.0
        for i, scene in enumerate(scenes):
            scene.t0 = t
            t += scene.duration
            # no duration here (not every lavfi source has one): the output -t below bounds the scene
            video = f"{scene.background}{':' if '=' in scene.background else '='}s={size}:r={fps}"
            filters = ["noise=alls=6:allf=t"]
            if scene.lines and can_text:
                font_size = max(18, height // 11)
                for j, line in enumerate(scene.lines):
                    textfile = work / f"s{i}_l{j}.txt"
                    textfile.write_text(line, encoding="utf-8")
                    spec = (
                        f"drawtext=textfile={_esc(textfile)}:fontsize={font_size}:fontcolor={scene.text_color}"
                        f":x={width // 12}:y={height // 6 + j * int(font_size * 1.6)}"
                    )
                    if font:
                        spec += f":fontfile={_esc(Path(font))}"
                    filters.append(spec)
                drew = True
            filters.append("format=yuv420p")
            args = ["-f", "lavfi", "-i", video]
            wav = work / f"s{i}.wav"
            if scene.speech and engine and _synthesise(scene.speech, wav, engine, work):
                # start speaking one second into the scene; pad with silence to the scene length
                args += ["-i", str(wav), "-af", "adelay=1000:all=1,apad"]
                spoke = True
            else:
                args += ["-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono"]
            part = work / f"part{i}.mp4"
            args += [
                "-vf", ",".join(filters), "-t", f"{scene.duration}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-g", str(fps * 2),
                "-c:a", "aac", "-ar", "48000", "-ac", "1", "-b:a", "64k", str(part),
            ]  # fmt: skip
            ff.run(args, timeout=600)
            parts.append(part)

        listing = work / "parts.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
        args = ["-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy"]
        if creation_time:
            args += ["-metadata", f"creation_time={creation_time}"]
        args += ["-movflags", "+faststart", str(out)]
        ff.run(args, timeout=600)

    return DemoInfo(path=out, duration=t, scenes=scenes, has_speech=spoke, has_text=drew)
