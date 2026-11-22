"""SQLite library: sessions, clips, keyframes, utterances, moments, notes, search.

One file (``<home>/library.db``), WAL mode, FTS5 for full-text search.  Every
other component talks to the library through :class:`Store`; nothing else
writes SQL.

Thread-safety: a ``Store`` owns one connection guarded by a lock, so one
instance can be shared by the capture thread, the processing thread and the
local web UI.
"""

from __future__ import annotations

import json
import re
import sqlite3
import threading
import time
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .models import (
    Clip,
    DayDigest,
    Keyframe,
    Moment,
    SearchHit,
    Session,
    SessionNote,
    Utterance,
)

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS sessions (
    id          TEXT PRIMARY KEY,
    kind        TEXT NOT NULL,
    source      TEXT NOT NULL DEFAULT '',
    title       TEXT NOT NULL DEFAULT '',
    started_ts  REAL NOT NULL,
    ended_ts    REAL,
    status      TEXT NOT NULL DEFAULT 'open',
    note_json   TEXT,
    note_path   TEXT,
    created_ts  REAL NOT NULL,
    updated_ts  REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_started ON sessions(started_ts);

CREATE TABLE IF NOT EXISTS clips (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    path          TEXT NOT NULL,
    original_path TEXT,
    fingerprint   TEXT NOT NULL UNIQUE,
    start_ts      REAL NOT NULL,
    duration      REAL NOT NULL DEFAULT 0,
    width         INTEGER,
    height        INTEGER,
    fps           REAL,
    has_audio     INTEGER NOT NULL DEFAULT 1,
    has_video     INTEGER NOT NULL DEFAULT 1,
    stages        TEXT NOT NULL DEFAULT '{}',
    created_ts    REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS clips_session ON clips(session_id, start_ts);

CREATE TABLE IF NOT EXISTS keyframes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    clip_id         INTEGER NOT NULL REFERENCES clips(id) ON DELETE CASCADE,
    session_id      TEXT NOT NULL,
    t               REAL NOT NULL,
    ts              REAL NOT NULL,
    path            TEXT NOT NULL,
    sharpness       REAL NOT NULL DEFAULT 0,
    novelty         REAL NOT NULL DEFAULT 0,
    reason          TEXT NOT NULL DEFAULT '',
    ocr_text        TEXT,
    ocr_backend     TEXT,
    caption         TEXT,
    caption_backend TEXT
);
CREATE INDEX IF NOT EXISTS keyframes_session ON keyframes(session_id, ts);
CREATE INDEX IF NOT EXISTS keyframes_clip ON keyframes(clip_id, t);

CREATE TABLE IF NOT EXISTS utterances (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    clip_id    INTEGER NOT NULL REFERENCES clips(id) ON DELETE CASCADE,
    session_id TEXT NOT NULL,
    t0         REAL NOT NULL,
    t1         REAL NOT NULL,
    ts0        REAL NOT NULL,
    ts1        REAL NOT NULL,
    text       TEXT NOT NULL,
    speaker    TEXT,
    backend    TEXT
);
CREATE INDEX IF NOT EXISTS utterances_session ON utterances(session_id, ts0);
CREATE INDEX IF NOT EXISTS utterances_clip ON utterances(clip_id, t0);

CREATE TABLE IF NOT EXISTS moments (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    idx           INTEGER NOT NULL,
    ts0           REAL NOT NULL,
    ts1           REAL NOT NULL,
    title         TEXT NOT NULL DEFAULT '',
    summary       TEXT NOT NULL DEFAULT '',
    tags          TEXT NOT NULL DEFAULT '[]',
    kind          TEXT NOT NULL DEFAULT '',
    salience      TEXT NOT NULL DEFAULT 'normal',
    keyframe_ids  TEXT NOT NULL DEFAULT '[]',
    utterance_ids TEXT NOT NULL DEFAULT '[]'
);
CREATE INDEX IF NOT EXISTS moments_session ON moments(session_id, idx);

CREATE TABLE IF NOT EXISTS days (
    date        TEXT PRIMARY KEY,
    digest_json TEXT NOT NULL,
    note_path   TEXT,
    updated_ts  REAL NOT NULL
);

-- Search documents live in a plain (indexed) table so they can be replaced cheaply;
-- the FTS5 index is an external-content table kept in step by triggers.
CREATE TABLE IF NOT EXISTS search (
    id         INTEGER PRIMARY KEY,
    text       TEXT NOT NULL,
    kind       TEXT NOT NULL,
    ref_id     TEXT NOT NULL,
    session_id TEXT NOT NULL,
    ts         REAL
);
CREATE INDEX IF NOT EXISTS search_ref ON search(kind, ref_id);
CREATE INDEX IF NOT EXISTS search_session ON search(session_id, kind);

CREATE VIRTUAL TABLE IF NOT EXISTS search_fts USING fts5(
    text,
    content = 'search',
    content_rowid = 'id',
    tokenize = 'porter unicode61 remove_diacritics 2'
);
CREATE TRIGGER IF NOT EXISTS search_ai AFTER INSERT ON search BEGIN
    INSERT INTO search_fts(rowid, text) VALUES (new.id, new.text);
END;
CREATE TRIGGER IF NOT EXISTS search_ad AFTER DELETE ON search BEGIN
    INSERT INTO search_fts(search_fts, rowid, text) VALUES ('delete', old.id, old.text);
END;
CREATE TRIGGER IF NOT EXISTS search_au AFTER UPDATE ON search BEGIN
    INSERT INTO search_fts(search_fts, rowid, text) VALUES ('delete', old.id, old.text);
    INSERT INTO search_fts(rowid, text) VALUES (new.id, new.text);
END;
"""

SEARCH_KINDS = ("utterance", "ocr", "caption", "moment", "session")


def _now() -> float:
    return time.time()


def fts_query(text: str) -> str:
    """Turn free user text into a safe FTS5 query.

    Every word becomes a quoted prefix term and terms are OR-ed, so natural
    questions ("where did I leave my keys") match without FTS syntax errors;
    bm25 ranking then favours rows containing more of the words.
    """
    words = re.findall(r"[\w']+", text.lower(), flags=re.UNICODE)
    words = [w.strip("'") for w in words]
    words = [w for w in words if w and w not in _STOPWORDS]
    if not words:
        words = [w.strip("'") for w in re.findall(r"[\w']+", text.lower()) if w.strip("'")]
    seen: list[str] = []
    for w in words:
        if w not in seen:
            seen.append(w)
    return " OR ".join(f'"{w}"*' for w in seen[:24])


_STOPWORDS = frozenset(
    """a an and are as at be but by did do does for from had has have how i if in is it its me my
    of on or so that the their them then there these they this to was we were what when where which
    who why will with you your""".split()
)


class Store:
    """The videonotes library database."""

    def __init__(self, db_path: str | Path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._db = sqlite3.connect(str(self.path), check_same_thread=False, isolation_level=None)
        self._db.row_factory = sqlite3.Row
        with self._lock:
            self._db.execute("PRAGMA journal_mode=WAL")
            self._db.execute("PRAGMA synchronous=NORMAL")
            self._db.execute("PRAGMA foreign_keys=ON")
            self._db.execute("PRAGMA busy_timeout=10000")
            self._db.executescript(_SCHEMA)
            row = self._db.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
            if row is None:
                self._db.execute(
                    "INSERT INTO meta(key, value) VALUES('schema_version', ?)", (str(SCHEMA_VERSION),)
                )
            elif int(row["value"]) > SCHEMA_VERSION:
                raise RuntimeError(
                    f"{self.path} was created by a newer videonotes (schema {row['value']}); "
                    f"this version understands schema {SCHEMA_VERSION}. Please upgrade."
                )

    # -- plumbing ---------------------------------------------------------

    def close(self) -> None:
        with self._lock:
            self._db.close()

    def __enter__(self) -> Store:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        """Run several statements atomically."""
        with self._lock:
            self._db.execute("BEGIN IMMEDIATE")
            try:
                yield self._db
            except BaseException:
                self._db.execute("ROLLBACK")
                raise
            else:
                self._db.execute("COMMIT")

    def _all(self, sql: str, args: Iterable[Any] = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self._db.execute(sql, tuple(args)).fetchall()

    def _one(self, sql: str, args: Iterable[Any] = ()) -> sqlite3.Row | None:
        with self._lock:
            return self._db.execute(sql, tuple(args)).fetchone()

    def _exec(self, sql: str, args: Iterable[Any] = ()) -> sqlite3.Cursor:
        with self._lock:
            return self._db.execute(sql, tuple(args))

    # -- meta -------------------------------------------------------------

    def get_meta(self, key: str, default: str | None = None) -> str | None:
        row = self._one("SELECT value FROM meta WHERE key=?", (key,))
        return row["value"] if row else default

    def set_meta(self, key: str, value: str) -> None:
        self._exec(
            "INSERT INTO meta(key, value) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )

    # -- sessions ---------------------------------------------------------

    @staticmethod
    def _session(row: sqlite3.Row) -> Session:
        note = SessionNote.from_dict(json.loads(row["note_json"])) if row["note_json"] else None
        return Session(
            id=row["id"],
            kind=row["kind"],
            source=row["source"],
            title=row["title"],
            started_ts=row["started_ts"],
            ended_ts=row["ended_ts"],
            status=row["status"],
            note=note,
            note_path=row["note_path"],
            created_ts=row["created_ts"],
            updated_ts=row["updated_ts"],
        )

    def create_session(self, session: Session) -> Session:
        now = _now()
        session.created_ts = session.created_ts or now
        session.updated_ts = now
        self._exec(
            "INSERT INTO sessions(id, kind, source, title, started_ts, ended_ts, status, "
            "note_json, note_path, created_ts, updated_ts) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (
                session.id,
                session.kind,
                session.source,
                session.title,
                session.started_ts,
                session.ended_ts,
                session.status,
                json.dumps(session.note.to_dict()) if session.note else None,
                session.note_path,
                session.created_ts,
                session.updated_ts,
            ),
        )
        return session

    def get_session(self, session_id: str) -> Session | None:
        row = self._one("SELECT * FROM sessions WHERE id=?", (session_id,))
        return self._session(row) if row else None

    def find_session(self, prefix: str) -> Session | None:
        """Resolve a full id, a unique id prefix, or 'latest'/'last'."""
        if prefix in ("latest", "last"):
            row = self._one("SELECT * FROM sessions ORDER BY started_ts DESC LIMIT 1")
            return self._session(row) if row else None
        exact = self.get_session(prefix)
        if exact:
            return exact
        like = prefix.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        rows = self._all("SELECT * FROM sessions WHERE id LIKE ? ESCAPE '\\' LIMIT 2", (like,))
        return self._session(rows[0]) if len(rows) == 1 else None

    def list_sessions(
        self, *, since_ts: float | None = None, until_ts: float | None = None, limit: int | None = None
    ) -> list[Session]:
        sql = "SELECT * FROM sessions WHERE 1=1"
        args: list[Any] = []
        if since_ts is not None:
            sql += " AND started_ts >= ?"
            args.append(since_ts)
        if until_ts is not None:
            sql += " AND started_ts < ?"
            args.append(until_ts)
        sql += " ORDER BY started_ts DESC"
        if limit:
            sql += " LIMIT ?"
            args.append(limit)
        return [self._session(r) for r in self._all(sql, args)]

    def update_session(self, session_id: str, **fields: Any) -> None:
        """Update columns of a session. ``note=`` accepts a SessionNote (or None)."""
        allowed = {"kind", "source", "title", "started_ts", "ended_ts", "status", "note_path"}
        sets: list[str] = []
        args: list[Any] = []
        for key, value in fields.items():
            if key == "note":
                sets.append("note_json=?")
                args.append(json.dumps(value.to_dict()) if value is not None else None)
            elif key in allowed:
                sets.append(f"{key}=?")
                args.append(value)
            else:
                raise KeyError(f"unknown session field: {key}")
        sets.append("updated_ts=?")
        args.append(_now())
        args.append(session_id)
        self._exec(f"UPDATE sessions SET {', '.join(sets)} WHERE id=?", args)
        if "note" in fields:
            self._index_session(session_id)

    def delete_session(self, session_id: str) -> None:
        with self.tx() as db:
            db.execute("DELETE FROM search WHERE session_id=?", (session_id,))
            db.execute("DELETE FROM sessions WHERE id=?", (session_id,))

    def session_bounds(self, session_id: str) -> tuple[float, float] | None:
        row = self._one(
            "SELECT MIN(start_ts) AS a, MAX(start_ts + duration) AS b FROM clips WHERE session_id=?",
            (session_id,),
        )
        if not row or row["a"] is None:
            return None
        return float(row["a"]), float(row["b"])

    # -- clips ------------------------------------------------------------

    @staticmethod
    def _clip(row: sqlite3.Row) -> Clip:
        return Clip(
            id=row["id"],
            session_id=row["session_id"],
            path=row["path"],
            original_path=row["original_path"],
            fingerprint=row["fingerprint"],
            start_ts=row["start_ts"],
            duration=row["duration"],
            width=row["width"],
            height=row["height"],
            fps=row["fps"],
            has_audio=bool(row["has_audio"]),
            has_video=bool(row["has_video"]),
            stages=json.loads(row["stages"] or "{}"),
            created_ts=row["created_ts"],
        )

    def add_clip(self, clip: Clip) -> Clip:
        """Insert a clip. Raises ``sqlite3.IntegrityError`` if the fingerprint exists."""
        clip.created_ts = clip.created_ts or _now()
        cur = self._exec(
            "INSERT INTO clips(session_id, path, original_path, fingerprint, start_ts, duration, "
            "width, height, fps, has_audio, has_video, stages, created_ts) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                clip.session_id,
                clip.path,
                clip.original_path,
                clip.fingerprint,
                clip.start_ts,
                clip.duration,
                clip.width,
                clip.height,
                clip.fps,
                int(clip.has_audio),
                int(clip.has_video),
                json.dumps(clip.stages),
                clip.created_ts,
            ),
        )
        clip.id = int(cur.lastrowid)
        return clip

    def get_clip(self, clip_id: int) -> Clip | None:
        row = self._one("SELECT * FROM clips WHERE id=?", (clip_id,))
        return self._clip(row) if row else None

    def clip_by_fingerprint(self, fingerprint: str) -> Clip | None:
        row = self._one("SELECT * FROM clips WHERE fingerprint=?", (fingerprint,))
        return self._clip(row) if row else None

    def list_clips(self, session_id: str) -> list[Clip]:
        return [
            self._clip(r)
            for r in self._all("SELECT * FROM clips WHERE session_id=? ORDER BY start_ts, id", (session_id,))
        ]

    def update_clip(self, clip_id: int, **fields: Any) -> None:
        allowed = {
            "path", "original_path", "start_ts", "duration", "width", "height", "fps",
            "has_audio", "has_video",
        }  # fmt: skip
        sets, args = [], []
        for key, value in fields.items():
            if key not in allowed:
                raise KeyError(f"unknown clip field: {key}")
            sets.append(f"{key}=?")
            args.append(int(value) if key in ("has_audio", "has_video") else value)
        if not sets:
            return
        args.append(clip_id)
        self._exec(f"UPDATE clips SET {', '.join(sets)} WHERE id=?", args)

    def set_clip_stage(self, clip_id: int, stage: str, status: str, **detail: Any) -> None:
        """Record the outcome of one pipeline stage (status: done | error | skipped)."""
        with self.tx() as db:
            row = db.execute("SELECT stages FROM clips WHERE id=?", (clip_id,)).fetchone()
            if row is None:
                raise KeyError(f"no clip {clip_id}")
            stages = json.loads(row["stages"] or "{}")
            stages[stage] = {"status": status, "ts": _now(), **detail}
            db.execute("UPDATE clips SET stages=? WHERE id=?", (json.dumps(stages), clip_id))

    def clear_clip_stage(self, clip_id: int, stage: str) -> None:
        with self.tx() as db:
            row = db.execute("SELECT stages FROM clips WHERE id=?", (clip_id,)).fetchone()
            if row is None:
                return
            stages = json.loads(row["stages"] or "{}")
            stages.pop(stage, None)
            db.execute("UPDATE clips SET stages=? WHERE id=?", (json.dumps(stages), clip_id))

    # -- keyframes --------------------------------------------------------

    @staticmethod
    def _keyframe(row: sqlite3.Row) -> Keyframe:
        return Keyframe(
            id=row["id"],
            clip_id=row["clip_id"],
            session_id=row["session_id"],
            t=row["t"],
            ts=row["ts"],
            path=row["path"],
            sharpness=row["sharpness"],
            novelty=row["novelty"],
            reason=row["reason"],
            ocr_text=row["ocr_text"],
            ocr_backend=row["ocr_backend"],
            caption=row["caption"],
            caption_backend=row["caption_backend"],
        )

    def replace_keyframes(self, clip_id: int, keyframes: list[Keyframe]) -> list[Keyframe]:
        """Replace every keyframe of a clip (the extract stage is re-runnable)."""
        with self.tx() as db:
            old = [r["id"] for r in db.execute("SELECT id FROM keyframes WHERE clip_id=?", (clip_id,))]
            for kid in old:
                db.execute(
                    "DELETE FROM search WHERE kind IN ('ocr','caption') AND ref_id=?", (str(kid),)
                )
            db.execute("DELETE FROM keyframes WHERE clip_id=?", (clip_id,))
            for kf in keyframes:
                cur = db.execute(
                    "INSERT INTO keyframes(clip_id, session_id, t, ts, path, sharpness, novelty, reason, "
                    "ocr_text, ocr_backend, caption, caption_backend) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        clip_id, kf.session_id, kf.t, kf.ts, kf.path, kf.sharpness, kf.novelty,
                        kf.reason, kf.ocr_text, kf.ocr_backend, kf.caption, kf.caption_backend,
                    ),  # fmt: skip
                )
                kf.id = int(cur.lastrowid)
                kf.clip_id = clip_id
                if kf.ocr_text:
                    self._index(db, "ocr", str(kf.id), kf.session_id, kf.ts, kf.ocr_text)
                if kf.caption:
                    self._index(db, "caption", str(kf.id), kf.session_id, kf.ts, kf.caption)
        return keyframes

    def get_keyframe(self, keyframe_id: int) -> Keyframe | None:
        row = self._one("SELECT * FROM keyframes WHERE id=?", (keyframe_id,))
        return self._keyframe(row) if row else None

    def list_keyframes(
        self,
        *,
        session_id: str | None = None,
        clip_id: int | None = None,
        ts0: float | None = None,
        ts1: float | None = None,
    ) -> list[Keyframe]:
        sql, args = "SELECT * FROM keyframes WHERE 1=1", []
        if session_id is not None:
            sql += " AND session_id=?"
            args.append(session_id)
        if clip_id is not None:
            sql += " AND clip_id=?"
            args.append(clip_id)
        if ts0 is not None:
            sql += " AND ts >= ?"
            args.append(ts0)
        if ts1 is not None:
            sql += " AND ts < ?"
            args.append(ts1)
        sql += " ORDER BY ts, id"
        return [self._keyframe(r) for r in self._all(sql, args)]

    def set_keyframe_ocr(self, keyframe_id: int, text: str, backend: str) -> None:
        with self.tx() as db:
            row = db.execute("SELECT session_id, ts FROM keyframes WHERE id=?", (keyframe_id,)).fetchone()
            if row is None:
                raise KeyError(f"no keyframe {keyframe_id}")
            db.execute(
                "UPDATE keyframes SET ocr_text=?, ocr_backend=? WHERE id=?", (text, backend, keyframe_id)
            )
            db.execute("DELETE FROM search WHERE kind='ocr' AND ref_id=?", (str(keyframe_id),))
            if text.strip():
                self._index(db, "ocr", str(keyframe_id), row["session_id"], row["ts"], text)

    def set_keyframe_caption(self, keyframe_id: int, caption: str, backend: str) -> None:
        with self.tx() as db:
            row = db.execute("SELECT session_id, ts FROM keyframes WHERE id=?", (keyframe_id,)).fetchone()
            if row is None:
                raise KeyError(f"no keyframe {keyframe_id}")
            db.execute(
                "UPDATE keyframes SET caption=?, caption_backend=? WHERE id=?",
                (caption, backend, keyframe_id),
            )
            db.execute("DELETE FROM search WHERE kind='caption' AND ref_id=?", (str(keyframe_id),))
            if caption.strip():
                self._index(db, "caption", str(keyframe_id), row["session_id"], row["ts"], caption)

    def reset_keyframe(self, keyframe_id: int, *, ocr: bool = False, caption: bool = False) -> None:
        """Forget OCR text and/or caption of a keyframe so that stage runs again for it."""
        with self.tx() as db:
            if ocr:
                db.execute("UPDATE keyframes SET ocr_text=NULL, ocr_backend=NULL WHERE id=?", (keyframe_id,))
                db.execute("DELETE FROM search WHERE kind='ocr' AND ref_id=?", (str(keyframe_id),))
            if caption:
                db.execute("UPDATE keyframes SET caption=NULL, caption_backend=NULL WHERE id=?", (keyframe_id,))
                db.execute("DELETE FROM search WHERE kind='caption' AND ref_id=?", (str(keyframe_id),))

    # -- utterances -------------------------------------------------------

    @staticmethod
    def _utterance(row: sqlite3.Row) -> Utterance:
        return Utterance(
            id=row["id"],
            clip_id=row["clip_id"],
            session_id=row["session_id"],
            t0=row["t0"],
            t1=row["t1"],
            ts0=row["ts0"],
            ts1=row["ts1"],
            text=row["text"],
            speaker=row["speaker"],
            backend=row["backend"],
        )

    def replace_utterances(self, clip_id: int, utterances: list[Utterance]) -> list[Utterance]:
        with self.tx() as db:
            old = [r["id"] for r in db.execute("SELECT id FROM utterances WHERE clip_id=?", (clip_id,))]
            for uid in old:
                db.execute("DELETE FROM search WHERE kind='utterance' AND ref_id=?", (str(uid),))
            db.execute("DELETE FROM utterances WHERE clip_id=?", (clip_id,))
            for u in utterances:
                cur = db.execute(
                    "INSERT INTO utterances(clip_id, session_id, t0, t1, ts0, ts1, text, speaker, backend) "
                    "VALUES(?,?,?,?,?,?,?,?,?)",
                    (clip_id, u.session_id, u.t0, u.t1, u.ts0, u.ts1, u.text, u.speaker, u.backend),
                )
                u.id = int(cur.lastrowid)
                u.clip_id = clip_id
                if u.text.strip():
                    self._index(db, "utterance", str(u.id), u.session_id, u.ts0, u.text)
        return utterances

    def list_utterances(
        self,
        *,
        session_id: str | None = None,
        clip_id: int | None = None,
        ts0: float | None = None,
        ts1: float | None = None,
    ) -> list[Utterance]:
        sql, args = "SELECT * FROM utterances WHERE 1=1", []
        if session_id is not None:
            sql += " AND session_id=?"
            args.append(session_id)
        if clip_id is not None:
            sql += " AND clip_id=?"
            args.append(clip_id)
        if ts0 is not None:
            sql += " AND ts1 > ?"
            args.append(ts0)
        if ts1 is not None:
            sql += " AND ts0 < ?"
            args.append(ts1)
        sql += " ORDER BY ts0, id"
        return [self._utterance(r) for r in self._all(sql, args)]

    # -- moments ----------------------------------------------------------

    @staticmethod
    def _moment(row: sqlite3.Row) -> Moment:
        return Moment(
            id=row["id"],
            session_id=row["session_id"],
            idx=row["idx"],
            ts0=row["ts0"],
            ts1=row["ts1"],
            title=row["title"],
            summary=row["summary"],
            tags=json.loads(row["tags"] or "[]"),
            kind=row["kind"],
            salience=row["salience"],
            keyframe_ids=json.loads(row["keyframe_ids"] or "[]"),
            utterance_ids=json.loads(row["utterance_ids"] or "[]"),
        )

    def replace_moments(self, session_id: str, moments: list[Moment]) -> list[Moment]:
        with self.tx() as db:
            db.execute("DELETE FROM search WHERE kind='moment' AND session_id=?", (session_id,))
            db.execute("DELETE FROM moments WHERE session_id=?", (session_id,))
            for m in moments:
                cur = db.execute(
                    "INSERT INTO moments(session_id, idx, ts0, ts1, title, summary, tags, kind, salience, "
                    "keyframe_ids, utterance_ids) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        session_id, m.idx, m.ts0, m.ts1, m.title, m.summary, json.dumps(m.tags),
                        m.kind, m.salience or "normal", json.dumps(m.keyframe_ids), json.dumps(m.utterance_ids),
                    ),  # fmt: skip
                )
                m.id = int(cur.lastrowid)
                m.session_id = session_id
                text = " — ".join(x for x in (m.title, m.summary, " ".join(m.tags)) if x)
                if text.strip():
                    self._index(db, "moment", str(m.id), session_id, m.ts0, text)
        return moments

    def update_moment(
        self,
        moment_id: int,
        *,
        title: str,
        summary: str,
        tags: list[str],
        kind: str | None = None,
        salience: str | None = None,
    ) -> None:
        """Store a moment's summary. ``kind`` / ``salience`` are left unchanged when None."""
        with self.tx() as db:
            row = db.execute("SELECT session_id, ts0 FROM moments WHERE id=?", (moment_id,)).fetchone()
            if row is None:
                raise KeyError(f"no moment {moment_id}")
            db.execute(
                "UPDATE moments SET title=?, summary=?, tags=?, kind=COALESCE(?, kind), "
                "salience=COALESCE(?, salience) WHERE id=?",
                (title, summary, json.dumps(tags), kind, salience, moment_id),
            )
            db.execute("DELETE FROM search WHERE kind='moment' AND ref_id=?", (str(moment_id),))
            text = " — ".join(x for x in (title, summary, " ".join(tags)) if x)
            if text.strip():
                self._index(db, "moment", str(moment_id), row["session_id"], row["ts0"], text)

    def list_moments(self, session_id: str) -> list[Moment]:
        return [
            self._moment(r)
            for r in self._all("SELECT * FROM moments WHERE session_id=? ORDER BY idx", (session_id,))
        ]

    def get_moment(self, moment_id: int) -> Moment | None:
        row = self._one("SELECT * FROM moments WHERE id=?", (moment_id,))
        return self._moment(row) if row else None

    # -- days -------------------------------------------------------------

    def save_day(self, digest: DayDigest, note_path: str | None = None) -> None:
        self._exec(
            "INSERT INTO days(date, digest_json, note_path, updated_ts) VALUES(?,?,?,?) "
            "ON CONFLICT(date) DO UPDATE SET digest_json=excluded.digest_json, "
            "note_path=excluded.note_path, updated_ts=excluded.updated_ts",
            (digest.date, json.dumps(digest.to_dict()), note_path, _now()),
        )

    def get_day(self, date: str) -> DayDigest | None:
        row = self._one("SELECT digest_json FROM days WHERE date=?", (date,))
        return DayDigest.from_dict(json.loads(row["digest_json"])) if row else None

    # -- search -----------------------------------------------------------

    @staticmethod
    def _index(db: sqlite3.Connection, kind: str, ref_id: str, session_id: str, ts: float | None, text: str) -> None:
        db.execute(
            "INSERT INTO search(text, kind, ref_id, session_id, ts) VALUES(?,?,?,?,?)",
            (text, kind, ref_id, session_id, ts),
        )

    def _index_session(self, session_id: str) -> None:
        with self.tx() as db:
            db.execute("DELETE FROM search WHERE kind='session' AND session_id=?", (session_id,))
            row = db.execute(
                "SELECT title, note_json, started_ts FROM sessions WHERE id=?", (session_id,)
            ).fetchone()
            if row is None or not row["note_json"]:
                return
            note = SessionNote.from_dict(json.loads(row["note_json"]))
            parts = [note.title or row["title"], note.summary, *note.key_points, *note.decisions]
            parts += [a.text for a in note.action_items] + note.open_questions + note.tags
            text = "\n".join(p for p in parts if p)
            if text.strip():
                self._index(db, "session", session_id, session_id, row["started_ts"], text)

    def search(
        self,
        query: str,
        *,
        limit: int = 20,
        kinds: Iterable[str] | None = None,
        session_id: str | None = None,
        since_ts: float | None = None,
        until_ts: float | None = None,
    ) -> list[SearchHit]:
        """Full-text search over transcripts, on-screen text, captions and notes."""
        match = fts_query(query)
        if not match:
            return []
        sql = (
            "SELECT s.text, s.kind, s.ref_id, s.session_id, s.ts, "
            "snippet(search_fts, 0, '[', ']', ' … ', 18) AS snip, bm25(search_fts) AS rank "
            "FROM search_fts JOIN search s ON s.id = search_fts.rowid WHERE search_fts MATCH ?"
        )
        args: list[Any] = [match]
        kinds = list(kinds) if kinds else None
        if kinds:
            sql += f" AND s.kind IN ({','.join('?' * len(kinds))})"
            args += kinds
        if session_id:
            sql += " AND s.session_id=?"
            args.append(session_id)
        if since_ts is not None:
            sql += " AND s.ts >= ?"
            args.append(since_ts)
        if until_ts is not None:
            sql += " AND s.ts < ?"
            args.append(until_ts)
        sql += " ORDER BY rank LIMIT ?"
        args.append(limit)
        hits = []
        for r in self._all(sql, args):
            ts = r["ts"]
            hits.append(
                SearchHit(
                    kind=r["kind"],
                    ref_id=str(r["ref_id"]),
                    session_id=r["session_id"],
                    ts=float(ts) if ts is not None else None,
                    text=r["text"],
                    snippet=r["snip"],
                    score=-float(r["rank"]),
                )
            )
        return hits

    # -- stats ------------------------------------------------------------

    def stats(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for table in ("sessions", "clips", "keyframes", "utterances", "moments"):
            out[table] = self._one(f"SELECT COUNT(*) AS n FROM {table}")["n"]
        out["media_seconds"] = self._one("SELECT COALESCE(SUM(duration), 0) AS s FROM clips")["s"]
        return out
