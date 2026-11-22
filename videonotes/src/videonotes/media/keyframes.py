"""Sparse keyframe selection and still-frame extraction.

A worn camera produces hours of video in which very little changes.  This
module finds the handful of frames worth keeping, in two cheap steps:

1. :func:`select_keyframes` runs **one** ffmpeg process that decodes the file
   once and pipes a few tiny grayscale frames per second to Python.  Each
   piped frame is a vertical stack of

   * a point-sampled copy of the picture (a third of the native size), used
     for the focus measure: nearest-neighbour sampling keeps native-resolution
     detail, so motion blur that is invisible at thumbnail size still shows;
   * an area-averaged thumbnail (``cfg.analysis_width`` wide), used to decide
     whether the picture shows something new.

   A small streaming state machine then keeps: a frame near the start
   (``"first"``), the sharpest frame shortly after the picture changed and came
   to rest (``"scene"`` for a cut-like change, ``"novel"`` for a gradual one),
   and a keep-alive frame when nothing changed for ``cfg.max_gap_s``
   (``"interval"``).  Memory use does not grow with the length of the file.

2. :func:`extract_frames` cuts full-quality JPEGs for just those times, with a
   few frame-accurate seeks per ffmpeg process and several processes at once.

Novelty is the share of image tiles whose brightness changed, measured after
cancelling what a body-worn camera does all the time without showing anything
new: small translations (shake, sway: phase correlation) and global brightness
changes (auto-exposure, flicker: offset and gain compensation).

The measures and thresholds come from the frame-selection research for this
project (synthetic "day in the life" footage with ground truth).  They are
module constants below; the user-facing knobs are :class:`~videonotes.config.FrameSettings`.
"""

from __future__ import annotations

import io
import logging
import math
import os
import queue
import re
import select
import shutil
import subprocess
import threading
import time
import uuid
from collections import deque
from collections.abc import Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..config import FrameSettings, is_macos
from . import ffmpeg as ff

log = logging.getLogger("videonotes.keyframes")

#: Every value :attr:`FrameCandidate.reason` can take.
REASONS = ("first", "scene", "novel", "interval")

# -- novelty measure (thumbnail tiles) ---------------------------------------------
_TILES_ACROSS = 20  # tile grid: 16 px tiles on a 320 px thumbnail
_TILE_DELTA = 10.0  # a tile "changed" when its mean moved by more than this (0..255) ...
_MAX_OFFSET = 64.0  # ... after removing a global brightness change of at most this much
_MAX_GAIN = 1.5  # ... and a global contrast / exposure gain of at most this factor
_MAX_SHIFT = 0.30  # largest translation cancelled, as a fraction of width / height
_MIN_PEAK = 0.03  # phase-correlation peak below this = the two pictures are unrelated
#: novelty = (share of changed tiles) ** gamma.  Chosen so that the operating point the
#: research tuned (2.5 % of tiles changed) maps to 0.20.  The default ``novelty_threshold``
#: is 0.25 (about 4.2 % of tiles): residual camera shake and exposure flicker measured up to
#: about 0.23 (3.3 %) after translation/gain cancelling, while one new line of writing on a
#: whiteboard is typically 4-5 %.  Tune it on real footage (``frames.novelty_threshold``).
_NOVELTY_GAMMA = 0.4363
_SCENE_NOVELTY = 0.55  # >= 25 % of tiles changed between consecutive samples: a cut-like change
_STILL_NOVELTY = 0.134  # <= 1 % of tiles: the picture is holding still
_LOCAL_NOVELTY = 0.37  # <= 10 % of tiles: something moves inside an otherwise fixed view
_STILL_SHIFT = 0.06  # the picture slid by more than this share of its size between samples: panning

# -- pacing -----------------------------------------------------------------------
_SETTLE_S = 1.0  # new content must hold still this long before a frame is taken
_MOTION_GAP_S = 10.0  # picture changing continuously (walking): one frame per this many seconds
_LOCAL_GAP_S = 30.0  # something keeps moving in a fixed view: one frame per this many seconds
_REVISIT_REFS = 3  # looking back at one of the last few keyframes' views is not new ...
_REVISIT_MATCH = 0.6  # ... if it matches that keyframe this much more closely than the threshold asks
_INTERVAL_POOL_MAX_S = 15.0  # a keep-alive frame is the sharpest of at most this many seconds
_NEAR_TIE = 1.05  # sharpness within 5 % counts as equal
_FIRST_NEAR_TIE = 1.10  # "first" prefers the earliest frame unless a later one is clearly sharper

# -- unusable frames --------------------------------------------------------------
_DARK_LEVEL = 32  # practically no pixel brighter than this: lens covered / pocket / night
_BRIGHT_LEVEL = 224  # practically no pixel darker than this: blown out
_FLAT_RANGE = 12  # practically no contrast at all: featureless
_TAIL_FRACTION = 0.001  # "practically no pixel" = fewer than this share of the pixels
_BLUR_RATIO = 0.25  # focus measure below this share of recent frames' best = motion-blurred
_BLUR_MEMORY_S = 6.0
_SHARPER_RATIO = 1.0 / _BLUR_RATIO  # the view got this much sharper than its keyframe: take another

# -- analysis stream --------------------------------------------------------------
_MIN_ANALYSIS_WIDTH = 16
_MAX_ANALYSIS_WIDTH = 1920
_MIN_ANALYSIS_FPS = 0.05
_MAX_ANALYSIS_FPS = 30.0
_SHARP_SCALE = 1.0 / 3.0  # the focus frame is the picture point-sampled to this share of its size
_MAX_SHARP_WIDTH = 960  # ... but never wider than this (bounds the cost for 4K)
_STALL_TIMEOUT_S = 180.0  # ffmpeg produced nothing for this long: treat as hung
_EXIT_GRACE_S = 30.0  # how long ffmpeg may take to exit after its last frame
_STDERR_TAIL_LINES = 40

# -- extraction -------------------------------------------------------------------
_SEEK_BATCH = 6  # timestamps per ffmpeg process
_EXTRACT_JOBS = 4  # concurrent ffmpeg processes
_SEEK_THREADS = 2  # decoder threads per seek (many short decodes run side by side)
_BATCH_TIMEOUT_S = 180.0  # plus _PER_SEEK_TIMEOUT_S per timestamp in the batch
_PER_SEEK_TIMEOUT_S = 45.0
_TAIL_WINDOWS_S = (2.0, 30.0)  # how far before the end to look for the last frame
_FULL_DECODE_LIMIT_S = 900.0  # decode a whole file to find its last frame only if shorter


@dataclass
class FrameCandidate:
    """One selected moment of a clip.

    ``t`` is the frame's presentation time in seconds from the start of the
    source file (the time :func:`extract_frames` expects).  ``sharpness`` is a
    focus measure (variance of the Laplacian; comparable between frames of the
    same clip, higher is sharper), ``novelty`` is 0..1 against the keyframes
    selected before it, and ``reason`` is one of :data:`REASONS`.
    """

    t: float
    sharpness: float
    novelty: float
    reason: str


# =====================================================================================
# Settings -> clamped parameters
# =====================================================================================


def _number(value: object, default: float) -> float:
    try:
        out = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


@dataclass(frozen=True)
class _Params:
    """:class:`FrameSettings` with every value made safe to compute with."""

    fps: float
    width: int
    threshold: float
    window_s: float
    min_gap_s: float
    max_gap_s: float  # math.inf = no keep-alive frames
    max_per_minute: float  # 0 = no budget

    @property
    def period(self) -> float:
        return 1.0 / self.fps

    @classmethod
    def from_settings(cls, cfg: FrameSettings) -> _Params:
        """Clamp user settings.  Zero or negative values mean, per field: ``analysis_fps`` /
        ``analysis_width`` -> the built-in default; ``max_gap_s`` -> no keep-alive frames;
        ``max_per_minute`` -> no budget; the rest -> 0."""
        defaults = FrameSettings()
        fps = _number(getattr(cfg, "analysis_fps", None), defaults.analysis_fps)
        if fps <= 0:
            fps = defaults.analysis_fps
        fps = min(max(fps, _MIN_ANALYSIS_FPS), _MAX_ANALYSIS_FPS)
        width = int(_number(getattr(cfg, "analysis_width", None), defaults.analysis_width))
        if width <= 0:
            width = defaults.analysis_width
        width = min(max(width, _MIN_ANALYSIS_WIDTH), _MAX_ANALYSIS_WIDTH)
        threshold = _number(getattr(cfg, "novelty_threshold", None), defaults.novelty_threshold)
        threshold = min(max(threshold, 0.01), 1.0)
        window = max(0.0, _number(getattr(cfg, "sharpness_window_s", None), defaults.sharpness_window_s))
        min_gap = max(0.0, _number(getattr(cfg, "min_gap_s", None), defaults.min_gap_s))
        max_gap = _number(getattr(cfg, "max_gap_s", None), defaults.max_gap_s)
        budget = max(0.0, _number(getattr(cfg, "max_per_minute", None), defaults.max_per_minute))
        if max_gap > 0:
            # Keep-alive frames cannot come faster than the minimum spacing or the budget allow.
            max_gap = max(max_gap, min_gap + 1.0 / fps, 60.0 / budget if budget > 0 else 0.0)
        else:
            max_gap = math.inf
        return cls(fps, width, threshold, window, min_gap, max_gap, budget)


# =====================================================================================
# Per-frame measures
# =====================================================================================


def sharpness(image: np.ndarray) -> float:
    """Variance of the 4-neighbour Laplacian of a grayscale image (higher = sharper)."""
    if image.ndim != 2 or image.shape[0] < 3 or image.shape[1] < 3:
        return 0.0
    g = image.astype(np.float32)
    lap = 4.0 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(lap.var())


def is_usable(gray: np.ndarray) -> bool:
    """False for frames nobody would want as a still: near-black, blown out or featureless."""
    if gray.size == 0:
        return False
    hist = np.bincount(gray.reshape(-1), minlength=256)
    cum = np.cumsum(hist)
    tail = max(1.0, _TAIL_FRACTION * gray.size)
    low = int(np.searchsorted(cum, tail, side="left"))  # ~0.1st percentile
    high = int(np.searchsorted(cum, gray.size - tail, side="right"))  # ~99.9th percentile
    high = min(high, 255)
    return not (high < _DARK_LEVEL or low > _BRIGHT_LEVEL or high - low < _FLAT_RANGE)


def _tile_means(gray: np.ndarray, tile: int) -> np.ndarray:
    rows, cols = gray.shape[0] // tile, gray.shape[1] // tile
    return gray[: rows * tile, : cols * tile].reshape(rows, tile, cols, tile).mean(axis=(1, 3))


def _changed_fraction(a: np.ndarray, b: np.ndarray) -> float:
    """Share of tiles whose mean differs between two tile grids once a global exposure change
    is cancelled: first a plain brightness offset, then (if tiles still differ) the best
    gain-and-offset through the tiles that the offset alone already explains.  Tiles pushed
    into clipping by the exposure change (blown highlights, crushed blacks) are not counted.

    Both corrections are bounded (``_MAX_OFFSET``, ``_MAX_GAIN``), so the lights going out,
    or a white wall followed by a dark one, still count as a change.
    """
    if a.size == 0:
        return 0.0
    diff = b - a
    offset = min(max(float(np.median(diff)), -_MAX_OFFSET), _MAX_OFFSET)
    residual = np.abs(diff - offset)
    changed = int(np.count_nonzero(residual > _TILE_DELTA))
    if changed == 0:
        return 0.0
    gain = 1.0
    inliers = residual <= 2.0 * _TILE_DELTA
    if int(np.count_nonzero(inliers)) >= max(8, a.size // 4):
        ai, bi = a[inliers], b[inliers]
        spread = float(ai.var())
        if spread > 16.0:
            gain = float(((ai - ai.mean()) * (bi - bi.mean())).mean()) / spread
            gain = min(max(gain, 1.0 / _MAX_GAIN), _MAX_GAIN)
            offset = float(np.median(b - gain * a))
            middle = float(np.median(a))
            shift = min(max((gain - 1.0) * middle + offset, -_MAX_OFFSET), _MAX_OFFSET)  # brightness change mid-scale
            offset = shift - (gain - 1.0) * middle
    # What each picture predicts for the other, within what a pixel can hold.
    forward = np.abs(b - np.clip(gain * a + offset, 0.0, 255.0))
    backward = np.abs(a - np.clip((b - offset) / gain, 0.0, 255.0)) * gain
    fitted = np.minimum(forward, backward) / math.sqrt(gain)
    return min(changed, int(np.count_nonzero(fitted > _TILE_DELTA))) / a.size


class _Frame:
    """What the selector remembers about one analysed frame."""

    __slots__ = ("t", "sharp", "gray", "usable", "blurred", "nov", "tiles", "spec")

    def __init__(self, t: float, sharp: float, gray: np.ndarray, usable: bool):
        self.t = t
        self.sharp = sharp
        self.gray = gray  # uint8 thumbnail, owned by this object
        self.usable = usable
        self.blurred = False  # much less sharp than the frames just before it
        self.nov = 0.0
        self.tiles: np.ndarray | None = None
        self.spec: np.ndarray | None = None

    @property
    def rank(self) -> int:
        """2 = good still, 1 = motion-blurred, 0 = unusable exposure."""
        return 0 if not self.usable else (1 if self.blurred else 2)

    def better_than(self, other: _Frame | None, tie: float = 1.0) -> bool:
        """True if this frame is the better still (``tie`` > 1 demands a clear margin)."""
        if other is None:
            return True
        if self.rank != other.rank:
            return self.rank > other.rank
        return self.sharp > other.sharp * tie


class _Comparer:
    """Novelty between two thumbnails of one fixed size."""

    def __init__(self, shape: tuple[int, int]):
        self.h, self.w = shape
        self.tile = max(1, min(round(self.w / _TILES_ACROSS), self.h, self.w))
        window = np.hanning(self.h)[:, None] * np.hanning(self.w)[None, :]
        self.window = window.astype(np.float32)
        self.can_align = self.h >= 8 and self.w >= 8

    def _tiles(self, f: _Frame) -> np.ndarray:
        if f.tiles is None:
            f.tiles = _tile_means(f.gray, self.tile)
        return f.tiles

    def _spec(self, f: _Frame) -> np.ndarray:
        if f.spec is None:
            g = f.gray.astype(np.float32)
            g -= float(g.mean())
            f.spec = np.fft.rfft2(g * self.window).astype(np.complex64)
        return f.spec

    def _shift(self, a: _Frame, b: _Frame) -> tuple[int, int, float]:
        """Translation (dx, dy) with b(y, x) ~= a(y - dy, x - dx), and the correlation peak."""
        cross = self._spec(b) * np.conj(self._spec(a))
        cross /= np.abs(cross) + 1e-6
        corr = np.fft.irfft2(cross, s=(self.h, self.w))
        k = int(np.argmax(corr))
        dy, dx = divmod(k, self.w)
        peak = float(corr.flat[k])
        if dy > self.h // 2:
            dy -= self.h
        if dx > self.w // 2:
            dx -= self.w
        return dx, dy, peak

    def novelty(self, a: _Frame, b: _Frame, *, enough_below: float = 0.0) -> float:
        """0..1: how much of ``b`` is not in ``a`` (see :meth:`compare`)."""
        return self.compare(a, b, enough_below=enough_below)[0]

    def compare(self, a: _Frame, b: _Frame, *, enough_below: float = 0.0) -> tuple[float, float]:
        """``(novelty, shift)``: how much of ``b`` is not in ``a`` (0..1), and how far the picture
        slid between them when a translation was cancelled to get that score (as a share of the
        picture size, 0 when none was).

        The translation search is skipped when the plain comparison already scores below
        ``enough_below`` (aligning can only lower the score, and the caller does not care).
        """
        frac = _changed_fraction(self._tiles(a), self._tiles(b))
        if frac <= 0.0:
            return 0.0, 0.0
        score = frac**_NOVELTY_GAMMA
        if score < enough_below or not self.can_align:
            return score, 0.0
        dx, dy, peak = self._shift(a, b)
        if (dx, dy) == (0, 0) or peak < _MIN_PEAK:
            return score, 0.0
        if abs(dx) > _MAX_SHIFT * self.w or abs(dy) > _MAX_SHIFT * self.h:
            return score, 0.0
        ya, yb = (0, dy) if dy >= 0 else (-dy, 0)
        xa, xb = (0, dx) if dx >= 0 else (-dx, 0)
        hh, ww = self.h - abs(dy), self.w - abs(dx)
        if hh < 2 * self.tile or ww < 2 * self.tile:
            return score, 0.0
        aligned = _changed_fraction(
            _tile_means(a.gray[ya : ya + hh, xa : xa + ww], self.tile),
            _tile_means(b.gray[yb : yb + hh, xb : xb + ww], self.tile),
        ) ** _NOVELTY_GAMMA
        if aligned >= score:
            return score, 0.0
        return aligned, max(abs(dx) / self.w, abs(dy) / self.h)


# =====================================================================================
# Streaming selector
# =====================================================================================


class _Pending:
    """A change that has been noticed but not yet turned into a keyframe."""

    __slots__ = ("kind", "start", "abrupt", "run_start", "settled", "window_end", "best", "fallback", "n", "nov_sum")

    def __init__(self, kind: str, start: float, abrupt: bool = False):
        self.kind = kind  # "change" | "sharper"
        self.start = start
        self.abrupt = abrupt
        self.run_start: float | None = None  # when the current still run began
        self.settled = False
        self.window_end = math.inf
        self.best: _Frame | None = None  # best frame of the still run
        self.fallback: _Frame | None = None  # best frame since the change, still or not
        self.n = 0
        self.nov_sum = 0.0


class _Selector:
    """Online keyframe selector: ``push`` analysed frames in time order, then ``finish``.

    Memory is bounded: the last few selected frames, the previous frame, at most one
    candidate per pending change and a short pool of keep-alive candidates.
    """

    def __init__(self, params: _Params):
        self.p = params
        self.selected: list[FrameCandidate] = []
        self.n_frames = 0
        self.n_out_of_order = 0
        self.t_first: float | None = None
        self.t_last: float | None = None
        self._cmp: _Comparer | None = None
        self._started = False  # "first" has been emitted
        self._first_best: _Frame | None = None
        self._last_t = -math.inf  # time of the last selected frame
        self._refs: deque[_Frame] = deque(maxlen=1 + _REVISIT_REFS)
        self._match: _Frame | None = None  # the reference the current frame looks like, if any
        self._prev: _Frame | None = None  # previous usable frame
        self._pending: _Pending | None = None
        self._sharp_hist: deque[tuple[float, float]] = deque()
        self._pool: deque[_Frame] = deque()
        self._pool_s = (
            min(max(params.window_s, params.max_gap_s / 4.0), _INTERVAL_POOL_MAX_S)
            if math.isfinite(params.max_gap_s)
            else 0.0
        )
        self._pool_cap = 256
        motion_gap = max(_MOTION_GAP_S, params.min_gap_s)
        if params.max_per_minute > 0:
            motion_gap = max(motion_gap, 60.0 / params.max_per_minute)
        self._motion_gap = motion_gap
        self._local_gap = max(_LOCAL_GAP_S, motion_gap)

    # -- input ---------------------------------------------------------------------

    def push(self, t: float, gray: np.ndarray, sharp: float, usable: bool | None = None) -> None:
        """Feed one analysed frame (``gray``: uint8 thumbnail the selector may keep)."""
        if not math.isfinite(t) or (self.t_last is not None and t <= self.t_last):
            self.n_out_of_order += 1
            return
        if self._cmp is None:
            self._cmp = _Comparer((int(gray.shape[0]), int(gray.shape[1])))
        elif gray.shape != (self._cmp.h, self._cmp.w):
            raise ValueError(f"analysis frame size changed from {(self._cmp.h, self._cmp.w)} to {gray.shape}")
        if self.t_first is None:
            self.t_first = t
        self.t_last = t
        self.n_frames += 1
        frame = _Frame(t, float(sharp) if math.isfinite(sharp) else 0.0, gray, is_usable(gray) if usable is None else usable)
        self._flag_blur(frame)
        self._pool_add(frame)
        if not self._started:
            in_window = t - self.t_first <= self.p.window_s + 1e-6
            if in_window and frame.better_than(self._first_best, _FIRST_NEAR_TIE):
                self._first_best = frame
            if in_window and t - self.t_first < self.p.window_s - 1e-6:
                return
            self._emit_first()
            if self._refs and frame is self._refs[-1]:
                return
        self._step(frame)

    def finish(self) -> list[FrameCandidate]:
        """End of stream: flush what is pending and return the selection in time order."""
        if not self._started:
            self._emit_first()
        pend, self._pending = self._pending, None
        if pend is not None:
            pick = pend.best or pend.fallback
            if pick is not None:
                self._select(pick, self._reason(pend), pick.nov)
        self.selected.sort(key=lambda c: c.t)
        return self.selected

    # -- internals -----------------------------------------------------------------

    def _emit_first(self) -> None:
        self._started = True
        if self._first_best is not None:
            self._select(self._first_best, "first", 1.0)
            self._first_best = None

    def _select(self, frame: _Frame, reason: str, novelty: float) -> None:
        self.selected.append(FrameCandidate(frame.t, frame.sharp, min(1.0, max(0.0, novelty)), reason))
        self._last_t = frame.t
        self._refs.append(frame)
        self._pending = None

    @staticmethod
    def _reason(pend: _Pending) -> str:
        if pend.kind == "sharper":
            return "interval"
        return "scene" if pend.abrupt and pend.best is not None else "novel"

    def _eligible(self, frame: _Frame) -> bool:
        return frame.t >= self._last_t + self.p.min_gap_s - 1e-6

    def _flag_blur(self, frame: _Frame) -> None:
        hist = self._sharp_hist
        while hist and hist[0][0] < frame.t - _BLUR_MEMORY_S:
            hist.popleft()
        if not frame.usable:
            return
        if hist and frame.sharp < _BLUR_RATIO * max(s for _, s in hist):
            frame.blurred = True
        hist.append((frame.t, frame.sharp))
        if len(hist) > 512:
            hist.popleft()

    def _pool_add(self, frame: _Frame) -> None:
        """Keep-alive candidates: a sliding-window maximum over the last ``_pool_s`` seconds
        (an older frame survives only while it is clearly better than every later one)."""
        if self._pool_s <= 0.0 and math.isinf(self.p.max_gap_s):
            return
        pool = self._pool
        while pool and not pool[-1].better_than(frame, _NEAR_TIE):
            pool.pop()
        pool.append(frame)
        while pool[0].t < frame.t - self._pool_s - 1e-6 or len(pool) > self._pool_cap:
            pool.popleft()

    def _novelty(self, frame: _Frame) -> float:
        """Novelty against the last selected frame.  A frame that is new by that measure but
        a close match of one of the few keyframes before it (while those are recent) is a
        glance back at something already captured, and scores as that match instead.
        Remembers in ``_match`` which keyframe the frame looks like, if any."""
        assert self._cmp is not None
        thr = self.p.threshold
        self._match = None
        if not self._refs:
            return 1.0
        last = self._refs[-1]
        nov = self._cmp.novelty(last, frame, enough_below=thr) if last.usable else 1.0
        if nov < thr:
            self._match = last
            return nov
        close = _REVISIT_MATCH * thr
        for ref in list(self._refs)[-2::-1]:
            if frame.t - ref.t > self.p.max_gap_s:
                break
            if ref.usable and (seen := self._cmp.novelty(ref, frame, enough_below=close)) < close:
                self._match = ref
                return seen
        return nov

    def _motion(self, frame: _Frame) -> tuple[float, float]:
        """Change since the previous usable frame: ``(novelty, slide)``."""
        if self._prev is None or self._cmp is None:
            return 1.0, 0.0
        return self._cmp.compare(self._prev, frame, enough_below=_STILL_NOVELTY)

    def _new_scene(self, frame: _Frame) -> None:
        """Focus measures of different scenes do not compare: restart the blur history
        with the frame that opened the new one."""
        self._sharp_hist.clear()
        self._sharp_hist.append((frame.t, frame.sharp))

    def _step(self, frame: _Frame) -> None:
        if frame.usable:
            frame.nov = self._novelty(frame)
            self._advance(frame)
            old, self._prev = self._prev, frame
            if old is not None and not any(old is ref for ref in self._refs):
                old.spec = None  # only the previous frame and the references keep a spectrum
        if frame.t - self._last_t >= self.p.max_gap_s - 0.5 * self.p.period:
            self._keep_alive()

    def _advance(self, frame: _Frame) -> None:
        """Drive the change -> settle -> pick state machine with one usable frame."""
        p = self.p
        pend = self._pending
        novel = frame.nov >= p.threshold
        if pend is None:
            if novel:
                motion, _ = self._motion(frame)
                abrupt = motion >= _SCENE_NOVELTY and frame.nov >= _SCENE_NOVELTY
                self._pending = _Pending("change", frame.t, abrupt)
                if abrupt:
                    self._new_scene(frame)
            elif self._eligible(frame) and frame.rank == 2 and self._much_sharper_than_its_keyframe(frame):
                pend = self._pending = _Pending("sharper", frame.t)
                pend.best = frame
                pend.window_end = frame.t + p.window_s
                if p.window_s <= 0.0:
                    self._select(frame, "interval", frame.nov)
            return

        if pend.kind == "sharper":
            assert pend.best is not None
            if novel:  # the view changed while we were collecting: keep what we have, start over
                self._select(pend.best, "interval", pend.best.nov)
                self._restart(frame)
                return
            if frame.rank == 2 and frame.better_than(pend.best):
                pend.best = frame
            if frame.t >= pend.window_end - 1e-6:
                self._select(pend.best, "interval", pend.best.nov)
            return

        if not novel:  # back to a view we already have
            if pend.settled and pend.best is not None:
                self._select(pend.best, self._reason(pend), pend.best.nov)
                self._restart(frame)
            else:
                self._pending = None
            return

        motion, slide = self._motion(frame)
        eligible = self._eligible(frame)
        pend.n += 1
        pend.nov_sum += frame.nov
        if eligible and frame.better_than(pend.fallback):
            pend.fallback = frame
        if motion >= _SCENE_NOVELTY and frame.nov >= _SCENE_NOVELTY:  # another cut
            if pend.settled and pend.best is not None:
                self._select(pend.best, self._reason(pend), pend.best.nov)
                self._restart(frame)
                return
            pend.abrupt = True
            pend.settled, pend.run_start, pend.best = False, None, None
            self._new_scene(frame)
        elif motion < max(_STILL_NOVELTY, min(_LOCAL_NOVELTY, 0.5 * frame.nov)) and slide <= _STILL_SHIFT:
            # Holding still (shake and sway allowed, panning not).
            if pend.run_start is None:
                pend.run_start = self._prev.t if self._prev is not None else frame.t
            if eligible and frame.better_than(pend.best):
                overdue = pend.settled and frame.t > pend.window_end
                if overdue and frame.rank == 2 and (pend.best is None or pend.best.rank < 2):
                    pend.window_end = frame.t + p.window_s  # first good frame after a smeared stretch
                pend.best = frame
            if not pend.settled and frame.t - pend.run_start >= _SETTLE_S - 0.5 * p.period:
                pend.settled = True
                pend.window_end = max(frame.t, self._last_t + p.min_gap_s) + p.window_s
        elif pend.settled and pend.best is not None:  # the settled view moves on: take what we have
            self._select(pend.best, self._reason(pend), pend.best.nov)
            return
        else:
            pend.settled, pend.run_start, pend.best = False, None, None

        if pend.settled and pend.best is not None and pend.best.rank == 2 and frame.t >= pend.window_end - 1e-6:
            self._select(pend.best, self._reason(pend), pend.best.nov)
            return
        # Never coming to rest (walking, something moving in view), or only blurred frames
        # so far: do not wait for ever.
        big = pend.nov_sum / pend.n >= _SCENE_NOVELTY
        if frame.t - pend.start >= (self._motion_gap if big else self._local_gap):
            pick = pend.best or pend.fallback
            if pick is not None:
                self._select(pick, self._reason(pend), pick.nov)

    def _restart(self, frame: _Frame) -> None:
        """A keyframe was just taken while ``frame`` was being looked at: judge it afresh."""
        frame.nov = self._novelty(frame)
        self._advance(frame)

    def _much_sharper_than_its_keyframe(self, frame: _Frame) -> bool:
        ref = self._match
        return ref is not None and ref.usable and frame.sharp > _SHARPER_RATIO * max(ref.sharp, 1e-6)

    def _keep_alive(self) -> None:
        """Nothing was selected for ``max_gap_s``: take the best frame we can offer."""
        pend = self._pending
        if pend is not None:
            pick = pend.best or pend.fallback
            if pick is not None:
                self._select(pick, self._reason(pend), pick.nov)
                return
        for frame in self._pool:
            if self._eligible(frame):
                self._select(frame, "interval", frame.nov)
                return


def _apply_budget(
    cands: list[FrameCandidate], duration: float, params: _Params, *, start: float = 0.0
) -> list[FrameCandidate]:
    """Enforce ``min_gap_s`` and the ``max_per_minute`` budget on a time-sorted selection.

    ``duration`` is the length of video the selection covers, beginning at ``start``.
    Over budget, the least novel frames go first, but a frame whose removal would open a gap
    longer than ``max_gap_s`` is spared.  Only if the budget cannot be met that way do the
    most novel frames simply win.  The ``"first"`` frame always stays.
    """
    cands = sorted(cands, key=lambda c: c.t)
    spaced: list[FrameCandidate] = []
    for cand in cands:
        if spaced and cand.t - spaced[-1].t < params.min_gap_s - 1e-6:
            keep_new = spaced[-1].reason != "first" and (cand.reason == "first" or cand.novelty > spaced[-1].novelty)
            if keep_new:
                spaced[-1] = cand
            continue
        spaced.append(cand)
    if params.max_per_minute <= 0 or not spaced:
        return spaced
    limit = max(1, math.ceil(params.max_per_minute * max(duration, 0.0) / 60.0 - 1e-9))
    excess = len(spaced) - limit
    if excess <= 0:
        return spaced

    n = len(spaced)
    prev = list(range(-1, n - 1))
    nxt = list(range(1, n + 1))
    alive = [True] * n
    end_t = max(start + duration, spaced[-1].t)
    by_novelty = sorted((i for i in range(n) if spaced[i].reason != "first"), key=lambda i: (spaced[i].novelty, -spaced[i].t))
    for i in by_novelty:
        if excess <= 0:
            break
        before = spaced[prev[i]].t if prev[i] >= 0 else start
        after = spaced[nxt[i]].t if nxt[i] < n else end_t
        if after - before > params.max_gap_s + 1e-6:
            continue  # gaps only ever grow, so this frame stays protected for the rest of the pass
        alive[i] = False
        if prev[i] >= 0:
            nxt[prev[i]] = nxt[i]
        if nxt[i] < n:
            prev[nxt[i]] = prev[i]
        excess -= 1
    if excess > 0:  # holes are unavoidable: keep "first" and the most novel of the rest
        firsts = sum(1 for c in spaced if c.reason == "first")
        keep = set(by_novelty[len(by_novelty) - max(0, limit - firsts) :]) if limit > firsts else set()
        alive = [spaced[i].reason == "first" or i in keep for i in range(n)]
    return [c for i, c in enumerate(spaced) if alive[i]]


# =====================================================================================
# Analysis stream (the ffmpeg boundary of select_keyframes)
# =====================================================================================


@dataclass(frozen=True)
class AnalysisGeometry:
    """Sizes of the two pictures stacked in each piped frame (focus frame on top)."""

    width: int  # thumbnail (novelty)
    height: int
    sharp_width: int  # point-sampled focus frame
    sharp_height: int

    @property
    def frame_bytes(self) -> int:
        return self.sharp_width * (self.sharp_height + self.height)


def _even(value: float, minimum: int = 2) -> int:
    """Nearest even integer, at least ``minimum``."""
    return max(minimum, int(round(value / 2.0)) * 2)


def _even_floor(value: float, minimum: int = 2) -> int:
    """Largest even integer not above ``value``, at least ``minimum``."""
    return max(minimum, int(value) // 2 * 2)


def display_size(info: ff.MediaInfo) -> tuple[int, int] | None:
    """Picture size as shown (rotation metadata applied), or None when the probe has none."""
    if not info.width or not info.height or info.width <= 0 or info.height <= 0:
        return None
    if info.rotation % 180 == 90:
        return int(info.height), int(info.width)
    return int(info.width), int(info.height)


def analysis_geometry(size: tuple[int, int] | None, analysis_width: int) -> AnalysisGeometry:
    """Thumbnail and focus-frame sizes for a source of the given displayed ``size``.

    Widths and heights are even; the thumbnail is never wider than the source (down to a
    floor of 16 px) and keeps its aspect ratio.  An unknown size is assumed to be 16:9.
    """
    src_w, src_h = size if size else (1920, 1080)
    width = min(max(int(analysis_width), _MIN_ANALYSIS_WIDTH), _MAX_ANALYSIS_WIDTH)
    width = _even_floor(min(width, src_w), _MIN_ANALYSIS_WIDTH)
    height = min(_even(width * src_h / src_w), 8 * width)
    sharp_w = min(src_w, max(width, int(src_w * _SHARP_SCALE)), max(width, _MAX_SHARP_WIDTH))
    sharp_w = max(width, _even_floor(sharp_w))
    sharp_h = min(_even(sharp_w * src_h / src_w), 8 * sharp_w)
    return AnalysisGeometry(width, height, sharp_w, sharp_h)


def analysis_command(
    src: str | Path,
    geometry: AnalysisGeometry,
    *,
    analysis_fps: float,
    source_fps: float | None = None,
    hwaccel: str | None = None,
) -> list[str]:
    """The argv of the analysis pass.

    Per kept frame ffmpeg writes one raw gray picture on stdout (focus frame stacked on the
    thumbnail) and one ``showinfo`` line with the frame's original timestamp on stderr.
    ``select`` does the decimation rather than the ``fps`` filter because it keeps the
    source timestamps (``fps`` re-stamps frames, and a later seek would land elsewhere).
    """
    g = geometry
    period = 1.0 / analysis_fps
    fps = source_fps if source_fps and math.isfinite(source_fps) and source_fps > 0 else 30.0
    slack = min(0.5 / fps, period / 4.0)  # so "every 15th frame" survives timestamp jitter
    keep = f"isnan(prev_selected_t)+gte(t-prev_selected_t,{period - slack:.6f})+lt(t,prev_selected_t)"
    graph = (
        f"[0:V:0]select='{keep}',showinfo=checksum=0,format=gray,split=2[a][b];"
        f"[a]scale={g.width}:{g.height}:flags=area,pad={g.sharp_width}:{g.height}[lo];"
        f"[b]scale={g.sharp_width}:{g.sharp_height}:flags=neighbor[hi];"
        "[hi][lo]vstack[out]"
    )
    cmd = ff.base_cmd(loglevel="level+info") + ["-nostats"]
    if hwaccel:
        cmd += ["-hwaccel", hwaccel]
    cmd += ["-i", _input_path(src), "-an", "-sn", "-dn", "-filter_complex", graph, "-map", "[out]"]
    cmd += ["-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"]
    return cmd


def _input_path(path: str | Path) -> str:
    """Absolute path, so ffmpeg can never mistake a file name for a protocol or an option."""
    return os.path.abspath(os.fspath(path))


_SHOWINFO_FRAME = re.compile(r"\bn:\s*\d+\s+pts:\s*(\S+)\s+pts_time:\s*(\S+)")
_SHOWINFO_TIMEBASE = re.compile(r"config in time_base:\s*(\d+)/(\d+)")
_ERROR_LINE = re.compile(r"\[(?:error|fatal|panic)\]")
_LEVEL_TAG = re.compile(r"\[(?:info|warning|error|fatal|panic|verbose|debug)\]\s?")


def parse_showinfo(line: str) -> tuple[int | None, float | None] | None:
    """``(pts, pts_time)`` of a ``showinfo`` frame line, or None for any other line."""
    m = _SHOWINFO_FRAME.search(line)
    if not m:
        return None
    try:
        pts: int | None = int(m[1])
    except ValueError:
        pts = None
    try:
        seconds: float | None = float(m[2])
        if not math.isfinite(seconds):
            seconds = None
    except ValueError:
        seconds = None
    return pts, seconds


def parse_timebase(line: str) -> float | None:
    """Seconds per timestamp tick from showinfo's ``config in time_base: 1/15360`` line."""
    m = _SHOWINFO_TIMEBASE.search(line)
    if not m or int(m[2]) == 0 or int(m[1]) == 0:
        return None
    return int(m[1]) / int(m[2])


class _FrameStream:
    """One running analysis process: iterate to get ``(t, frame_bytes)`` pairs.

    Use as a context manager; leaving the block always terminates and reaps the process,
    whatever happened inside (normal end, exception, Ctrl-C).
    """

    def __init__(self, cmd: Sequence[str], frame_bytes: int, *, period: float, stall_timeout: float | None = None):
        self._cmd = list(cmd)
        self._buf = bytearray(frame_bytes)
        self._period = period
        self._stall_timeout = _STALL_TIMEOUT_S if stall_timeout is None else stall_timeout
        self._proc: subprocess.Popen[bytes] | None = None
        self._thread: threading.Thread | None = None
        self._stamps: queue.SimpleQueue[tuple[int | None, float | None]] = queue.SimpleQueue()
        self._stderr_done = threading.Event()
        self._timebase: float | None = None
        self._tail: deque[str] = deque(maxlen=_STDERR_TAIL_LINES)
        self._errors: deque[str] = deque(maxlen=12)
        self._eof = False
        self._last_t: float | None = None
        self.frames = 0
        self.guessed_times = 0
        self.returncode: int | None = None

    def __enter__(self) -> _FrameStream:
        try:
            self._proc = subprocess.Popen(
                self._cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0
            )
        except OSError as exc:
            raise ff.FFmpegError(f"could not start ffmpeg ({exc}).\n{ff.INSTALL_HINT}") from exc
        self._thread = threading.Thread(target=self._drain_stderr, name="videonotes-ffmpeg-stderr", daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _drain_stderr(self) -> None:
        assert self._proc is not None and self._proc.stderr is not None
        try:
            for raw in io.BufferedReader(self._proc.stderr, 1 << 16):  # type: ignore[arg-type]
                line = raw[:4000].decode("utf-8", "replace").rstrip()
                stamp = parse_showinfo(line)
                if stamp is not None:
                    self._stamps.put(stamp)
                    continue
                if "showinfo" in line[:60]:
                    if self._timebase is None:
                        self._timebase = parse_timebase(line)
                    continue  # per-frame side-data chatter
                if not line:
                    continue
                self._tail.append(line)
                if _ERROR_LINE.search(line):
                    self._errors.append(line)
        except (OSError, ValueError):
            pass  # pipe closed underneath us while shutting down
        finally:
            self._stderr_done.set()

    def _fill(self) -> bool:
        """Read exactly one frame into the buffer. False at end of stream."""
        assert self._proc is not None and self._proc.stdout is not None
        out = self._proc.stdout
        view = memoryview(self._buf)
        got = 0
        while got < len(view):
            try:
                ready, _, _ = select.select([out], [], [], self._stall_timeout)
            except (OSError, ValueError):
                ready = [out]  # select() unusable on this pipe: fall back to a blocking read
            if not ready:
                raise ff.FFmpegError(
                    f"ffmpeg produced no video for {self._stall_timeout:.0f} seconds and was stopped. "
                    "The file may be damaged, or the disk it is on stopped responding; "
                    "check that the drive or card is still connected and try again."
                )
            n = out.readinto(view[got:])
            if not n:
                if got:
                    log.debug("analysis stream ended inside a frame (%d of %d bytes)", got, len(view))
                self._eof = True
                return False
            got += n
        return True

    def _next_time(self) -> float:
        stamp: tuple[int | None, float | None] | None = None
        waited = 0.0
        while True:
            try:
                stamp = self._stamps.get(timeout=0.25)
                break
            except queue.Empty:
                waited += 0.25
                if (self._stderr_done.is_set() and self._stamps.empty()) or waited >= 20.0:
                    break
        t: float | None = None
        if stamp is not None:
            pts, seconds = stamp
            # The integer timestamp is exact; older ffmpeg prints pts_time with 6 significant
            # digits only, which is too coarse late in a long recording.
            t = pts * self._timebase if pts is not None and self._timebase else seconds
        if t is None:
            self.guessed_times += 1
            t = 0.0 if self._last_t is None else self._last_t + self._period
        self._last_t = t
        return t

    def __iter__(self) -> Iterator[tuple[float, bytearray]]:
        while self._fill():
            t = self._next_time()
            self.frames += 1
            yield t, self._buf

    def close(self) -> None:
        proc = self._proc
        if proc is None:
            return
        self._proc = None
        try:
            if proc.poll() is None and self._eof:
                try:  # finished normally: give it a moment to write its trailer and leave
                    proc.wait(timeout=_EXIT_GRACE_S)
                except subprocess.TimeoutExpired:
                    pass
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
        finally:
            if proc.poll() is None:
                proc.kill()
            proc.wait()
            self.returncode = proc.returncode
            if self._thread is not None:
                self._thread.join(timeout=5)
            for pipe in (proc.stdout, proc.stderr):
                try:
                    if pipe is not None:
                        pipe.close()
                except OSError:
                    pass

    def error_text(self) -> str:
        """ffmpeg's own explanation: its error lines, else the end of what it printed."""
        lines = list(self._errors) or list(self._tail)[-8:]
        return "\n".join(_LEVEL_TAG.sub("", line) for line in lines)


@dataclass
class _Analysis:
    candidates: list[FrameCandidate]
    frames: int
    t_first: float | None
    t_last: float | None
    returncode: int | None
    error: str


def _analyse(cmd: Sequence[str], geometry: AnalysisGeometry, params: _Params) -> _Analysis:
    """Run one analysis pass and select as the frames arrive."""
    selector = _Selector(params)
    g = geometry
    with _FrameStream(cmd, g.frame_bytes, period=params.period) as stream:
        for t, buf in stream:
            stacked = np.frombuffer(buf, dtype=np.uint8).reshape(g.sharp_height + g.height, g.sharp_width)
            thumb = stacked[g.sharp_height :, : g.width].copy()
            selector.push(t, thumb, sharpness(stacked[: g.sharp_height]))
    if stream.guessed_times:
        log.warning("%d frame(s) arrived without a timestamp; their times were estimated", stream.guessed_times)
    if selector.n_out_of_order:
        log.warning("%d frame(s) with timestamps going backwards were ignored", selector.n_out_of_order)
    return _Analysis(
        selector.finish(), selector.n_frames, selector.t_first, selector.t_last, stream.returncode, stream.error_text()
    )


_HINTS = (
    ("moov atom not found", "The recording looks incomplete: the camera probably lost power or was "
     "switched off before it finished writing the file."),
    ("invalid data found", "The file is damaged or not a video (if it is still being copied, wait and retry)."),
    ("unrecognized option 'fps_mode'", "This ffmpeg is too old (5.1 or newer is needed). Update it with:  brew upgrade ffmpeg"),
    ("no such file or directory", "The file is gone; if it lives on the camera or an SD card, reconnect it."),
    ("input/output error", "The disk stopped responding; check that the drive or card is still connected."),
    ("permission denied", "videonotes is not allowed to read this file; check its permissions."),
)  # fmt: skip


def _explain(name: str, what: str, error: str, returncode: int | None) -> ff.FFmpegError:
    hint = next((text for needle, text in _HINTS if needle in error.lower()), "")
    code = f" (exit {returncode})" if returncode not in (None, 0) else ""
    message = f"{what} {name}{code}."
    if hint:
        message += f" {hint}"
    if error:
        message += f"\nffmpeg said:\n{error}"
    return ff.FFmpegError(message, returncode=returncode, stderr=error)


def select_keyframes(
    src: str | Path,
    cfg: FrameSettings,
    *,
    duration: float | None = None,
    hwaccel: bool = True,
) -> list[FrameCandidate]:
    """Choose a sparse set of sharp, non-redundant frames from ``src``.

    One low-resolution decode pass (``cfg.analysis_fps`` frames per second,
    ``cfg.analysis_width`` pixels wide), consumed as a stream.  Returns the chosen times in
    ascending order; see :data:`REASONS` for why a frame can be chosen:

    * ``"first"`` — the sharpest usable frame of the first ``cfg.sharpness_window_s``;
    * ``"scene"`` / ``"novel"`` — the picture differs from the recent keyframes by more than
      ``cfg.novelty_threshold`` (cut-like / gradual).  The frame taken is not the transition
      itself but the sharpest one within ``cfg.sharpness_window_s`` after the picture came
      to rest (or the sharpest of the stretch when it never does, e.g. while walking);
    * ``"interval"`` — nothing was selected for ``cfg.max_gap_s`` (the sharpest of the most
      recent stretch), or the view has become much sharper than the keyframe held for it.

    Frames are at least ``cfg.min_gap_s`` apart and number at most ``cfg.max_per_minute`` per
    minute of video on average (over budget the most novel stay, and ``"first"`` always).
    Near-black, blown-out and featureless frames, and frames far blurrier than their
    neighbours, are only ever used when a ``"first"`` / ``"interval"`` frame is due and
    nothing better exists.

    ``duration`` is the caller's idea of the clip length; it is used for a sanity warning
    only, because container durations are sometimes wrong: selection relies on the
    timestamps actually decoded.  With ``hwaccel`` (macOS, VideoToolbox available) decoding
    is tried on the GPU first and silently repeated in software if that fails.

    Returns ``[]`` for a file without a video stream.  Raises
    :class:`~videonotes.media.ffmpeg.FFmpegError` when the file cannot be read at all; a
    recording that is damaged part-way yields the keyframes up to the damage.
    """
    src = Path(src)
    info = ff.probe(src)
    if not info.has_video:
        return []
    params = _Params.from_settings(cfg)
    geometry = analysis_geometry(display_size(info), params.width)

    accels: list[str | None] = []
    if hwaccel and is_macos() and ff.has_hwaccel("videotoolbox"):
        accels.append("videotoolbox")
    accels.append(None)

    result: _Analysis | None = None
    started = time.monotonic()
    for accel in accels:
        cmd = analysis_command(src, geometry, analysis_fps=params.fps, source_fps=info.fps, hwaccel=accel)
        last = accel is None
        try:
            result = _analyse(cmd, geometry, params)
        except ff.FFmpegError as exc:
            if last:
                raise
            log.info("hardware decoding of %s failed (%s); retrying in software", src.name, exc)
            continue
        if last or (result.frames > 0 and result.returncode == 0):
            break
        log.info(
            "hardware decoding of %s gave %d frame(s), exit %s; retrying in software",
            src.name, result.frames, result.returncode,
        )  # fmt: skip
    assert result is not None

    if result.frames == 0:
        if result.returncode not in (None, 0):
            raise _explain(src.name, "Could not read video frames from", result.error, result.returncode)
        log.warning("%s has a video stream but no decodable frames", src.name)
        return []
    assert result.t_first is not None and result.t_last is not None
    if result.returncode not in (None, 0):
        log.warning(
            "%s could only be read up to %.1f s (ffmpeg exit %s); keeping the keyframes found so far.\n%s",
            src.name, result.t_last, result.returncode, result.error,
        )  # fmt: skip
    elif duration and math.isfinite(duration) and duration - result.t_last > max(10.0, 0.2 * duration):
        log.warning("%s: expected %.0f s of video but the frames end at %.1f s", src.name, duration, result.t_last)

    seen = result.t_last - result.t_first + params.period
    chosen = _apply_budget(result.candidates, seen, params, start=result.t_first)
    log.debug(
        "%s: %d analysis frames (%.1f s of video) in %.1f s -> %d keyframes",
        src.name, result.frames, seen, time.monotonic() - started, len(chosen),
    )  # fmt: skip
    return chosen


# =====================================================================================
# Extraction
# =====================================================================================


def frame_filename(t: float, prefix: str = "kf") -> str:
    """``<prefix>_<milliseconds, 9 digits>.jpg`` for a time in seconds (negative times are 0)."""
    return f"{prefix}_{max(0, int(round(t * 1000.0))):09d}.jpg"


@dataclass(frozen=True)
class _Shot:
    """One JPEG to produce."""

    t: float  # requested time (>= 0)
    seek: float  # where ffmpeg is told to seek (<= 0: do not seek, take the first frame)
    tmp: Path
    final: Path


def extract_command(src: str | Path, shots: Sequence[_Shot], *, scale: str | None, quality: int) -> list[str]:
    """Arguments (for :func:`videonotes.media.ffmpeg.run`) that write one JPEG per shot.

    Each shot is its own input, opened with ``-ss`` in front of ``-i``: ffmpeg jumps to the
    key frame before the time, decodes forward and outputs the first frame at or after it.
    """
    path = _input_path(src)
    args: list[str] = []
    for shot in shots:
        if shot.seek > 0:
            args += ["-ss", f"{shot.seek:.6f}"]
        args += ["-threads", str(_SEEK_THREADS), "-i", path]
    for k, shot in enumerate(shots):
        args += ["-map", f"{k}:V:0", "-an", "-sn", "-dn", "-frames:v", "1"]
        if scale:
            args += ["-vf", scale]
        args += ["-q:v", str(quality), "-f", "image2", "-c:v", "mjpeg", "-update", "1", str(shot.tmp)]
    return args


def _scale_filter(size: tuple[int, int] | None, width: int) -> str | None:
    """Downscale to ``width`` when the picture is wider; never upscale."""
    if width <= 0:
        return None
    if size is None:  # unknown source size: let ffmpeg decide per frame
        return f"scale=w='min(iw,{width})':h=-2:flags=bicubic"
    if size[0] <= width:
        return None
    return f"scale={width}:-2:flags=bicubic"


def _valid_jpeg(path: Path) -> bool:
    """A complete JPEG file (start and end markers present)."""
    try:
        size = path.stat().st_size
        if size < 100:
            return False
        with path.open("rb") as fh:
            head = fh.read(2)
            fh.seek(-2, os.SEEK_END)
            return head == b"\xff\xd8" and fh.read(2) == b"\xff\xd9"
    except OSError:
        return False


def _discard(paths: Sequence[Path]) -> None:
    for path in paths:
        try:
            path.unlink()
        except OSError:
            pass


def extract_frames(
    src: str | Path,
    times: list[float],
    out_dir: str | Path,
    *,
    width: int = 1280,
    quality: int = 3,
    prefix: str = "kf",
) -> list[Path]:
    """Write one JPEG per requested time; returns their paths in the order of ``times``.

    Files are named ``<prefix>_<milliseconds zero-padded to 9 digits>.jpg`` inside
    ``out_dir`` (created if needed).  Equal times (to the millisecond) share one file.

    * **Accuracy** — the image is the first frame at or after ``t`` minus half a frame, i.e.
      the frame being shown at ``t``, within one source frame (exactly the analysed frame
      for times that come from :func:`select_keyframes`).
    * **Size** — ``width`` is a maximum: wider pictures are scaled down (aspect kept), narrower
      ones are left alone.  ``quality`` is ffmpeg's ``-q:v`` (2 best … 31 worst).
    * **Past the end** — a time after the last frame yields the last decodable frame.

    Raises :class:`~videonotes.media.ffmpeg.FFmpegError` unless every requested time got its
    own freshly written image (so a failed batch can never hand back a wrong or stale
    picture), and ``ValueError`` for a time that is not a finite number.
    """
    src, out_dir = Path(src), Path(out_dir)
    times = [float(t) for t in times]
    if not times:
        return []
    for t in times:
        if not math.isfinite(t):
            raise ValueError(f"extract_frames: {t!r} is not a valid time")
    if os.sep in prefix or (os.altsep and os.altsep in prefix):
        raise ValueError(f"extract_frames: prefix {prefix!r} must not contain a path separator")
    info = ff.probe(src)
    if not info.has_video:
        raise ff.FFmpegError(f"{src.name} has no video, so no frames can be taken from it")
    quality = min(max(int(quality), 2), 31)
    scale = _scale_filter(display_size(info), int(width))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_dir = out_dir.resolve()

    fps = info.fps if info.fps and math.isfinite(info.fps) and info.fps > 0 else 30.0
    half_frame = 0.5 / fps
    token = f"{os.getpid()}-{uuid.uuid4().hex[:8]}"
    shots: dict[str, _Shot] = {}
    for t in times:
        name = frame_filename(t, prefix)
        if name not in shots:
            t = max(0.0, t)
            shots[name] = _Shot(t, t - half_frame, out_dir / f".{name}.{token}.part.jpg", out_dir / name)

    temps = [shot.tmp for shot in shots.values()]
    last_tmp = out_dir / f".{prefix}_last.{token}.part.jpg"
    try:
        missing = _run_batches(src, list(shots.values()), scale, quality)
        if missing:
            _fill_in(src, info, missing, last_tmp, scale, quality, total=len(shots))
        for shot in shots.values():
            os.replace(shot.tmp, shot.final)
    finally:
        _discard([*temps, last_tmp])
    return [out_dir / frame_filename(t, prefix) for t in times]


def _run_batches(src: Path, shots: list[_Shot], scale: str | None, quality: int) -> list[_Shot]:
    """Seek-extract all shots, a few per ffmpeg process and a few processes at a time.
    Returns the shots that did not get an image."""
    shots = sorted(shots, key=lambda s: s.t)
    batches = [shots[i : i + _SEEK_BATCH] for i in range(0, len(shots), _SEEK_BATCH)]

    def work(batch: list[_Shot]) -> list[_Shot]:
        timeout = _BATCH_TIMEOUT_S + _PER_SEEK_TIMEOUT_S * len(batch)
        try:
            proc = ff.run(extract_command(src, batch, scale=scale, quality=quality), timeout=timeout, check=False)
        except ff.FFmpegError as exc:  # timed out
            log.warning("extracting %d frame(s) from %s: %s", len(batch), src.name, exc)
            _discard([s.tmp for s in batch])
            return batch
        if proc.returncode != 0:
            # One bad seek fails the whole process; trust none of its files and redo each alone.
            _discard([s.tmp for s in batch])
            return batch
        return [s for s in batch if not _valid_jpeg(s.tmp)]

    missing: list[_Shot] = []
    workers = max(1, min(_EXTRACT_JOBS, len(batches), os.cpu_count() or 1))
    pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="videonotes-extract")
    try:
        for result in pool.map(work, batches):
            missing += result
    except BaseException:
        pool.shutdown(wait=True, cancel_futures=True)  # no ffmpeg left behind on Ctrl-C
        raise
    pool.shutdown(wait=True)
    return missing


_NO_FRAME = re.compile(r"output file is empty|nothing was (?:encoded|written)|does not contain any stream", re.I)


def _fill_in(
    src: Path, info: ff.MediaInfo, missing: list[_Shot], last_tmp: Path, scale: str | None, quality: int, *, total: int
) -> None:
    """Second chance for shots a batch did not produce: each alone, then (for times with no
    frame at or after them) the last decodable frame of the file."""
    fps = info.fps if info.fps and info.fps > 0 else 30.0
    past_end: list[_Shot] = []
    failures: list[tuple[_Shot, str]] = []
    for shot in sorted(missing, key=lambda s: s.t):
        _discard([shot.tmp])
        try:
            proc = ff.run(
                extract_command(src, [shot], scale=scale, quality=quality),
                timeout=_BATCH_TIMEOUT_S + _PER_SEEK_TIMEOUT_S, check=False,
            )  # fmt: skip
        except ff.FFmpegError as exc:
            failures.append((shot, str(exc)))
            continue
        if proc.returncode == 0 and _valid_jpeg(shot.tmp):
            continue
        _discard([shot.tmp])
        beyond = info.duration > 0 and shot.t >= info.duration - 2.0 / fps
        if proc.returncode == 0 or beyond or _NO_FRAME.search(proc.stderr or ""):
            past_end.append(shot)  # ffmpeg ran fine but found no frame at or after this time
        else:
            tail = "\n".join((proc.stderr or "").strip().splitlines()[-6:])
            failures.append((shot, tail))

    if past_end and not failures:
        try:
            _last_frame(src, info, last_tmp, scale, quality)
        except ff.FFmpegError as exc:
            failures = [(shot, str(exc)) for shot in past_end]
            past_end = []
        else:
            for shot in past_end:
                shutil.copyfile(last_tmp, shot.tmp)
            log.info(
                "%s: %d time(s) from %.3f s on are past the last frame; used the last frame instead",
                src.name, len(past_end), min(s.t for s in past_end),
            )  # fmt: skip
    if failures:
        shot, text = failures[0]
        worked = total - len(failures) - len(past_end)
        raise _explain(
            src.name,
            f"Could not take {len(failures)} of {total} still frame(s) (first failure at {shot.t:.3f} s; "
            f"{worked} worked) from",
            text,
            None,
        )


def _last_frame(src: Path, info: ff.MediaInfo, dst: Path, scale: str | None, quality: int) -> None:
    """Write the last decodable frame of ``src`` to ``dst``.

    ffmpeg overwrites one image with every frame it decodes (``-update 1``), so whatever is
    left when it stops is the last frame.  Only the tail of the file is decoded when that
    is enough.
    """
    path = _input_path(src)
    out = ["-map", "0:V:0", "-an", "-sn", "-dn"]
    if scale:
        out += ["-vf", scale]
    out += ["-fps_mode", "passthrough", "-q:v", str(quality), "-f", "image2", "-c:v", "mjpeg", "-update", "1", str(dst)]
    attempts: list[list[str]] = []
    if info.duration > max(_TAIL_WINDOWS_S):
        attempts += [["-sseof", f"-{window:g}", "-i", path] for window in _TAIL_WINDOWS_S]
    if info.duration <= _FULL_DECODE_LIMIT_S:
        attempts.append(["-i", path])
    error = ""
    for head in attempts:
        _discard([dst])
        try:
            proc = ff.run(head + out, timeout=_BATCH_TIMEOUT_S + 2.0 * min(max(info.duration, 0.0), _FULL_DECODE_LIMIT_S), check=False)
        except ff.FFmpegError as exc:
            error = str(exc)
            continue
        if proc.returncode == 0 and _valid_jpeg(dst):
            return
        error = "\n".join((proc.stderr or "").strip().splitlines()[-6:])
    _discard([dst])
    raise _explain(src.name, "Could not find a last frame in", error, None)
