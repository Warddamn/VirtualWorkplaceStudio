"""The processing pipeline: clips in, notes out.

Stage order per clip::

    probe -> extract (16 kHz audio + sparse keyframes) -> transcribe -> ocr -> caption

then per session::

    segment (moments) -> summarize -> render (Markdown) -> day digest

Design rules (see docs/ARCHITECTURE.md):

* **Stage-major.**  Each stage runs over every pending clip before the next
  stage starts, and its model is closed before the next one loads, so a
  16 GB machine never holds two heavy models.
* **Idempotent and resumable.**  A stage that finished for a clip is recorded
  in the library and skipped next time; an interrupted run just continues.
* **Degrade, don't die.**  A missing backend marks its stage *skipped* (with
  the reason, shown by ``vnote doctor`` / ``vnote show``) and the rest still
  runs; a clip that fails a stage is recorded as *error* and the others
  carry on.  Skipped and failed stages are retried on the next run.
"""

from __future__ import annotations

import hashlib
import logging
import math
import shutil
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any, Protocol

from .backends.base import BackendUnavailable
from .config import Settings
from .models import CLIP_STAGES, SESSION_STAGES, Clip, Keyframe, Session, Utterance
from .store import Store

log = logging.getLogger("videonotes.pipeline")

#: Which later clip stages become stale when a stage is re-run.
_DOWNSTREAM = {
    "probe": ("extract", "transcribe", "ocr", "caption"),
    "extract": ("transcribe", "ocr", "caption"),
    "transcribe": (),
    "ocr": (),
    "caption": (),
}


class Progress(Protocol):
    """Receives pipeline events; the CLI turns them into progress output."""

    def __call__(self, event: str, **info: Any) -> None: ...


def _no_progress(event: str, **info: Any) -> None:
    return None


class Pipeline:
    """Runs pipeline stages against one library.

    Backends are created lazily through the ``make_*`` factories and can be
    replaced for tests via the ``factories`` argument, a mapping with any of the
    keys ``"asr"``, ``"ocr"``, ``"vision"``, ``"llm"`` to zero-argument callables.
    """

    def __init__(
        self,
        settings: Settings,
        store: Store,
        *,
        progress: Progress | None = None,
        factories: dict[str, Callable[[], Any]] | None = None,
    ):
        self.settings = settings
        self.store = store
        self.progress: Progress = progress or _no_progress
        self._factories = dict(factories or {})
        self._backends: dict[str, Any] = {}
        self._unavailable: dict[str, str] = {}
        settings.ensure_dirs()

    # -- backend lifecycle -----------------------------------------------------

    def _default_factory(self, kind: str) -> Callable[[], Any]:
        if kind == "asr":
            from .backends.asr import make_transcriber

            return lambda: make_transcriber(self.settings)
        if kind == "ocr":
            from .backends.ocr import make_ocr

            return lambda: make_ocr(self.settings)
        if kind == "vision":
            from .backends.vision import make_captioner

            return lambda: make_captioner(self.settings)
        if kind == "llm":
            from .backends.llm import make_llm

            return lambda: make_llm(self.settings)
        raise KeyError(kind)

    def _backend(self, kind: str) -> Any | None:
        """The backend of one kind, created on first use. None when there is none."""
        if kind in self._backends:
            return self._backends[kind]
        if kind in self._unavailable:
            return None
        factory = self._factories.get(kind) or self._default_factory(kind)
        try:
            backend = factory()
        except BackendUnavailable as exc:
            self._unavailable[kind] = str(exc)
            log.warning("%s backend unavailable: %s", kind, exc)
            return None
        if backend is None:
            configured = getattr(getattr(self.settings, kind), "backend", "auto")
            self._unavailable[kind] = (
                "turned off in config" if configured == "none" else "no backend available (run `vnote doctor`)"
            )
            return None
        self._backends[kind] = backend
        return backend

    def _release(self, kind: str) -> None:
        backend = self._backends.pop(kind, None)
        if backend is not None:
            try:
                backend.close()
            except Exception:  # a failing close must never break a run
                log.exception("closing %s backend failed", kind)

    def close(self) -> None:
        for kind in list(self._backends):
            self._release(kind)

    def __enter__(self) -> Pipeline:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- paths -------------------------------------------------------------------

    def _wav_path(self, clip: Clip) -> Path:
        return self.settings.cache_dir / clip.session_id / f"clip{clip.id:06d}.wav"

    def _frames_dir(self, clip: Clip) -> Path:
        return self.settings.frames_dir / clip.session_id / f"clip{clip.id:06d}"

    def _media_path(self, clip: Clip) -> Path:
        return self.settings.abs(clip.path)

    # -- clip stages -------------------------------------------------------------

    def _stage_probe(self, clip: Clip) -> dict[str, Any]:
        from .media import ffmpeg as ff

        info = ff.probe(self._media_path(clip))
        has_audio = info.has_audio
        if not has_audio:
            # A low-res proxy may be video-only while the full-quality original has the sound.
            original = self._original_path(clip)
            if original is not None:
                try:
                    has_audio = ff.probe(original).has_audio
                except ff.FFmpegError:
                    has_audio = False
        if not (info.has_video or has_audio):
            raise ff.FFmpegError(f"{self._media_path(clip).name} has neither video nor audio")
        self.store.update_clip(
            clip.id,
            duration=info.duration,
            width=info.width,
            height=info.height,
            fps=info.fps,
            has_audio=has_audio,
            has_video=info.has_video,
        )
        return {"duration": round(info.duration, 2)}

    def _stage_extract(self, clip: Clip) -> dict[str, Any]:
        from .media import keyframes as kfm

        src = self._media_path(clip)
        detail: dict[str, Any] = {"audio": False, "keyframes": 0}
        if clip.has_audio:
            detail["audio"] = self._extract_wav(clip)
            if not detail["audio"]:
                self.store.update_clip(clip.id, has_audio=False)
        keyframes: list[Keyframe] = []
        if clip.has_video:
            candidates = kfm.select_keyframes(src, self.settings.frames, duration=clip.duration or None)
            out_dir = self._frames_dir(clip)
            if out_dir.exists():
                shutil.rmtree(out_dir, ignore_errors=True)
            if candidates:
                paths = kfm.extract_frames(
                    self._frame_source(clip),
                    [c.t for c in candidates],
                    out_dir,
                    width=self.settings.frames.jpeg_width,
                    quality=self.settings.frames.jpeg_quality,
                )
                for cand, path in zip(candidates, paths, strict=True):
                    keyframes.append(
                        Keyframe(
                            clip_id=clip.id,
                            session_id=clip.session_id,
                            t=cand.t,
                            ts=clip.start_ts + cand.t,
                            path=self.settings.rel(path),
                            sharpness=cand.sharpness,
                            novelty=cand.novelty,
                            reason=cand.reason,
                        )
                    )
        self.store.replace_keyframes(clip.id, keyframes)
        detail["keyframes"] = len(keyframes)
        return detail

    def _original_path(self, clip: Clip) -> Path | None:
        """The full-quality original of a clip, when there is one and it is still reachable
        (it usually lives on the camera's card, which may have been unplugged since)."""
        if not clip.original_path:
            return None
        original = self.settings.abs(clip.original_path)
        try:
            if original.is_file() and original != self._media_path(clip):
                return original
        except OSError:
            pass
        return None

    def _frame_source(self, clip: Clip) -> Path:
        """File to cut stills from: the original when reachable (text on a whiteboard is far
        more legible in the full-resolution file than in the proxy), else the analysed file."""
        return self._original_path(clip) or self._media_path(clip)

    def _extract_wav(self, clip: Clip) -> bool:
        """Write the clip's 16 kHz WAV, from the analysed file or else from the original."""
        from .media import audio as au

        sources = [self._media_path(clip)]
        original = self._original_path(clip)
        if original is not None:
            sources.append(original)
        for source in sources:
            try:
                au.extract_audio(source, self._wav_path(clip))
                return True
            except au.NoAudioError:
                continue
        return False

    def _stage_transcribe(self, clip: Clip) -> dict[str, Any]:
        if not clip.has_audio:
            self.store.replace_utterances(clip.id, [])
            return {"utterances": 0, "note": "no audio track"}
        transcriber = self._backend("asr")
        if transcriber is None:
            raise _Skip(self._unavailable.get("asr", "no speech-to-text backend"))
        wav = self._wav_path(clip)
        if not wav.is_file() and not self._extract_wav(clip):
            self.store.replace_utterances(clip.id, [])
            return {"utterances": 0, "note": "no audio track"}
        language = self.settings.asr.language
        segments = transcriber.transcribe(wav, language=None if language in ("", "auto") else language)
        utterances = [
            Utterance(
                clip_id=clip.id,
                session_id=clip.session_id,
                t0=float(seg.t0),
                t1=float(max(seg.t1, seg.t0)),
                ts0=clip.start_ts + float(seg.t0),
                ts1=clip.start_ts + float(max(seg.t1, seg.t0)),
                text=seg.text.strip(),
                speaker=seg.speaker,
                backend=transcriber.name,
            )
            for seg in segments
            if seg.text and seg.text.strip()
        ]
        utterances.sort(key=lambda u: (u.t0, u.t1))
        self.store.replace_utterances(clip.id, utterances)
        wav.unlink(missing_ok=True)
        return {"utterances": len(utterances), "backend": transcriber.name}

    def _stage_ocr(self, clip: Clip) -> dict[str, Any]:
        keyframes = self.store.list_keyframes(clip_id=clip.id)
        pending = [k for k in keyframes if k.ocr_text is None]
        if not pending:
            return {"frames": 0}
        engine = self._backend("ocr")
        if engine is None:
            raise _Skip(self._unavailable.get("ocr", "no OCR backend"))
        from .backends.ocr import clean_ocr_text

        cfg = self.settings.ocr
        with_text = 0
        for kf in pending:
            try:
                result = engine.read(self.settings.abs(kf.path))
                text = clean_ocr_text(result, min_confidence=cfg.min_confidence, min_chars=cfg.min_chars)
            except BackendUnavailable:
                raise
            except Exception as exc:  # one unreadable frame must not sink the clip
                log.warning("OCR failed on %s: %s", kf.path, exc)
                text = ""
            self.store.set_keyframe_ocr(kf.id, text, engine.name)
            with_text += bool(text)
        return {"frames": len(pending), "with_text": with_text, "backend": engine.name}

    def _stage_caption(self, clip: Clip) -> dict[str, Any]:
        keyframes = self.store.list_keyframes(clip_id=clip.id)
        chosen = choose_frames_to_caption(keyframes, clip.duration, self.settings.vision.max_per_minute)
        pending = [k for k in chosen if k.caption is None]
        if not pending:
            return {"frames": 0}
        captioner = self._backend("vision")
        if captioner is None:
            raise _Skip(self._unavailable.get("vision", "no captioning backend"))
        done = 0
        for kf in pending:
            try:
                caption = captioner.caption(self.settings.abs(kf.path), context=(kf.ocr_text or "")[:600])
            except BackendUnavailable:
                raise
            except Exception as exc:
                log.warning("captioning failed on %s: %s", kf.path, exc)
                continue  # leave caption None so a later run retries this frame
            self.store.set_keyframe_caption(kf.id, caption.strip(), captioner.name)
            done += 1
        return {"frames": done, "backend": captioner.name}

    _RUNNERS = {
        "probe": _stage_probe,
        "extract": _stage_extract,
        "transcribe": _stage_transcribe,
        "ocr": _stage_ocr,
        "caption": _stage_caption,
    }
    _STAGE_BACKEND = {"transcribe": "asr", "ocr": "ocr", "caption": "vision"}

    def _run_clip_stage(self, clip_id: int, stage: str) -> str:
        """Run one stage for one clip. Returns the recorded status."""
        clip = self.store.get_clip(clip_id)
        if clip is None:
            return "error"
        if clip.stage_done(stage):
            return "done"
        if stage != "probe" and not clip.stage_done("probe"):
            return "blocked"
        if stage in ("transcribe", "ocr", "caption") and not clip.stage_done("extract"):
            return "blocked"
        try:
            detail = self._RUNNERS[stage](self, clip)
        except _Skip as skip:
            self.store.set_clip_stage(clip_id, stage, "skipped", reason=str(skip))
            return "skipped"
        except BackendUnavailable as exc:
            kind = self._STAGE_BACKEND.get(stage)
            if kind:  # the backend died mid-run (e.g. model server stopped): stop using it
                self._release(kind)
                self._unavailable[kind] = str(exc)
            self.store.set_clip_stage(clip_id, stage, "skipped", reason=str(exc))
            return "skipped"
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            log.exception("stage %s failed for clip %s", stage, clip_id)
            self.store.set_clip_stage(clip_id, stage, "error", message=_short(exc))
            return "error"
        self.store.set_clip_stage(clip_id, stage, "done", **detail)
        return "done"

    def _force(self, session_id: str, stages: Iterable[str]) -> set[str]:
        """Clear recorded results so the given stages (and what depends on them) run again."""
        wanted = set(stages)
        unknown = wanted - set(CLIP_STAGES) - set(SESSION_STAGES)
        if unknown:
            raise ValueError(f"unknown stage(s): {', '.join(sorted(unknown))}")
        clear: set[str] = set()
        for stage in wanted & set(CLIP_STAGES):
            clear.add(stage)
            clear.update(_DOWNSTREAM[stage])
        for clip in self.store.list_clips(session_id):
            for stage in clear:
                self.store.clear_clip_stage(clip.id, stage)
            if "ocr" in clear or "caption" in clear:
                for kf in self.store.list_keyframes(clip_id=clip.id):
                    if "ocr" in clear and kf.ocr_text is not None and "extract" not in clear:
                        self.store.reset_keyframe(kf.id, ocr=True)
                    if "caption" in clear and kf.caption is not None and "extract" not in clear:
                        self.store.reset_keyframe(kf.id, caption=True)
        return wanted

    # -- public: batch processing --------------------------------------------------

    def process_session(self, session_id: str, *, force: Iterable[str] = ()) -> Session:
        """Bring one session fully up to date. Safe to call repeatedly."""
        session = self._require(session_id)
        forced = self._force(session_id, force)
        self.store.update_session(session_id, status="processing")
        try:
            for stage in CLIP_STAGES:
                clips = [c for c in self.store.list_clips(session_id) if not c.stage_done(stage)]
                if not clips:
                    continue
                self.progress("stage_start", stage=stage, total=len(clips), session_id=session_id)
                for i, clip in enumerate(clips, 1):
                    status = self._run_clip_stage(clip.id, stage)
                    self.progress(
                        "clip_stage", stage=stage, clip_id=clip.id, index=i, total=len(clips), status=status
                    )
                kind = self._STAGE_BACKEND.get(stage)
                if kind:
                    self._release(kind)  # one heavy model in memory at a time
            return self._finish(session, forced)
        except BaseException:
            self.store.update_session(session_id, status="error" if self._has_errors(session_id) else "open")
            raise
        finally:
            self.close()

    # -- public: live capture --------------------------------------------------------

    def process_clip_light(self, clip_id: int) -> dict[str, str]:
        """Live mode: cheap stages for one fresh segment, keeping models loaded between calls.

        Captioning and summarising are left to :meth:`finalize_session`.
        """
        statuses = {}
        for stage in ("probe", "extract", "transcribe", "ocr"):
            statuses[stage] = self._run_clip_stage(clip_id, stage)
            self.progress("clip_stage", stage=stage, clip_id=clip_id, index=1, total=1, status=statuses[stage])
        return statuses

    def finalize_session(self, session_id: str) -> Session:
        """Finish a session after live capture: remaining clip stages, then notes."""
        self._release("asr")
        self._release("ocr")
        return self.process_session(session_id)

    # -- session stages ------------------------------------------------------------------

    def _finish(self, session: Session, forced: set[str]) -> Session:
        from .notes.moments import segment_moments
        from .notes.render import render_session_note
        from .notes.summarize import summarize_moments, summarize_session

        sid = session.id
        bounds = self.store.session_bounds(sid)
        if bounds:
            self.store.update_session(sid, started_ts=bounds[0], ended_ts=bounds[1])
            session = self._require(sid)
        utterances = self.store.list_utterances(session_id=sid)
        keyframes = self.store.list_keyframes(session_id=sid)

        fingerprint = _evidence_fingerprint(utterances, keyframes, self.settings)
        previous = self.store.get_meta(f"summary:{sid}")
        fresh = session.note is not None and previous == fingerprint and not (forced & {"segment", "summarize"})
        if not fresh:
            self.progress("session_stage", stage="segment", session_id=sid)
            moments = segment_moments(session, utterances, keyframes, self.settings.notes)
            moments = self.store.replace_moments(sid, moments)

            self.progress("session_stage", stage="summarize", session_id=sid)
            llm = self._backend("llm")
            try:
                moments = summarize_moments(llm, session, moments, utterances, keyframes)
                for m in moments:
                    self.store.update_moment(
                        m.id, title=m.title, summary=m.summary, tags=m.tags, kind=m.kind, salience=m.salience
                    )
                note = summarize_session(llm, session, moments, utterances, keyframes)
            finally:
                self._release("llm")
            self.store.update_session(sid, note=note, title=note.title or session.title)
            self.store.set_meta(f"summary:{sid}", fingerprint)

        self.progress("session_stage", stage="render", session_id=sid)
        render_session_note(self.settings, self.store, sid)
        self.store.update_session(sid, status="error" if self._has_errors(sid) else "ready")
        session = self._require(sid)
        try:
            from .timeutil import local_date

            self.build_day(local_date(session.started_ts))
        except Exception:  # the day note is a convenience; never fail the session over it
            log.exception("building the day note failed")
        return self._require(sid)

    def build_day(self, date: str) -> Path:
        """(Re)build the digest and Markdown note for one local calendar day."""
        from .notes.render import render_day_note
        from .notes.summarize import summarize_day
        from .timeutil import day_bounds

        start, end = day_bounds(date)
        sessions = [s for s in self.store.list_sessions(since_ts=start, until_ts=end) if s.note is not None]
        sessions.sort(key=lambda s: s.started_ts)
        if sessions:
            self.progress("session_stage", stage="day", session_id=date)
            llm = self._backend("llm")
            try:
                digest = summarize_day(llm, date, sessions)
            finally:
                self._release("llm")
            digest.date = date
            digest.session_ids = [s.id for s in sessions]
            self.store.save_day(digest)
        return render_day_note(self.settings, self.store, date)

    # -- helpers -----------------------------------------------------------------------------

    def _require(self, session_id: str) -> Session:
        session = self.store.get_session(session_id)
        if session is None:
            raise KeyError(f"no such session: {session_id}")
        return session

    def _has_errors(self, session_id: str) -> bool:
        return any(
            info.get("status") == "error" for clip in self.store.list_clips(session_id) for info in clip.stages.values()
        )

    def unavailable(self) -> dict[str, str]:
        """Backends that could not be used in this run, with the reason."""
        return dict(self._unavailable)


class _Skip(Exception):
    """A stage cannot run for lack of a backend."""


def _short(exc: BaseException, limit: int = 400) -> str:
    text = f"{type(exc).__name__}: {exc}".strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def choose_frames_to_caption(keyframes: list[Keyframe], duration: float, max_per_minute: float) -> list[Keyframe]:
    """Pick which keyframes of a clip are worth a (slow) caption.

    Budget = ``max_per_minute`` per minute of clip (at least one).  The most
    novel frames win, but picks are spread out: a frame is skipped while a
    better one within the same slice of the clip is already chosen.
    Frames that already have a caption always count towards the budget.
    """
    if not keyframes or max_per_minute <= 0:
        return []
    minutes = max(duration, 1.0) / 60.0
    budget = max(1, math.ceil(minutes * max_per_minute))
    if len(keyframes) <= budget:
        return sorted(keyframes, key=lambda k: k.t)
    slice_len = max(duration, 1.0) / budget
    best: dict[int, Keyframe] = {}
    for kf in keyframes:
        slot = min(budget - 1, int(kf.t // slice_len))
        score = (kf.caption is not None, kf.reason in ("first", "scene"), kf.novelty, kf.sharpness)
        current = best.get(slot)
        if current is None or score > (
            current.caption is not None,
            current.reason in ("first", "scene"),
            current.novelty,
            current.sharpness,
        ):
            best[slot] = kf
    return sorted(best.values(), key=lambda k: k.t)


def _evidence_fingerprint(utterances: list[Utterance], keyframes: list[Keyframe], settings: Settings) -> str:
    """Changes whenever what a summary is built from changes."""
    h = hashlib.sha256()
    for u in utterances:
        h.update(f"u|{u.ts0:.2f}|{u.text}\n".encode())
    for k in keyframes:
        h.update(f"k|{k.ts:.2f}|{k.ocr_text or ''}|{k.caption or ''}\n".encode())
    n = settings.notes
    h.update(f"cfg|{n.moment_gap_seconds}|{n.moment_min_seconds}|{n.moment_max_seconds}".encode())
    h.update(f"llm|{settings.llm.backend}|{settings.llm.model}".encode())
    return h.hexdigest()
