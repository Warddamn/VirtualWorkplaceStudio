"""Library commands: demo, add, process, sessions, show, day, search, ask, delete, config."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from ..config import default_config_text
from ..models import CLIP_STAGES, SESSION_STAGES, Session
from ..timeutil import fmt_clock, fmt_duration, local_date, now_ts, parse_day
from .common import EXIT_ERROR, CliError, Context, progress_printer


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("demo", help="generate a sample clip and run the whole pipeline on it")
    p.add_argument("--keep", action="store_true", help="keep the demo session in the library afterwards")
    p.set_defaults(func=cmd_demo)

    p = sub.add_parser("add", help="add video/audio files to the library and write notes for them")
    p.add_argument("files", nargs="+", metavar="FILE")
    p.add_argument("--no-process", action="store_true", help="only add; run `vnote process` later")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("process", help="(re)run the pipeline for sessions that are not finished")
    p.add_argument("session", nargs="?", default="pending", help="session id / prefix / 'latest' / 'all' (default: unfinished ones)")
    p.add_argument(
        "--force", action="append", default=[], metavar="STAGE",
        help=f"redo a stage and what depends on it ({', '.join(CLIP_STAGES + SESSION_STAGES)}); repeatable",
    )  # fmt: skip
    p.set_defaults(func=cmd_process)

    p = sub.add_parser("sessions", help="list sessions")
    p.add_argument("-n", "--limit", type=int, default=20)
    p.add_argument("--day", help="only this day (YYYY-MM-DD, today, yesterday)")
    p.set_defaults(func=cmd_sessions)

    p = sub.add_parser("show", help="show the note of a session")
    p.add_argument("session", nargs="?", default="latest")
    p.add_argument("--open", action="store_true", help="open the Markdown note in the default app")
    p.add_argument("--transcript", action="store_true", help="print the full transcript too")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("day", help="digest of a day (default: today)")
    p.add_argument("date", nargs="?", default="today", help="YYYY-MM-DD, today or yesterday")
    p.add_argument("--open", action="store_true", help="open the Markdown note in the default app")
    p.set_defaults(func=cmd_day)

    p = sub.add_parser("search", help="search speech, on-screen text, captions and notes")
    p.add_argument("query", nargs="+")
    p.add_argument("-n", "--limit", type=int, default=15)
    p.add_argument("--day", help="only this day (YYYY-MM-DD, today, yesterday)")
    p.add_argument("--kind", action="append", choices=["utterance", "ocr", "caption", "moment", "session"])
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("ask", help="ask a question about what was recorded")
    p.add_argument("question", nargs="+")
    p.add_argument("--sources", action="store_true", help="list the evidence the answer was built from")
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("delete", help="delete a session: its media, keyframes, note and index entries")
    p.add_argument("session")
    p.add_argument("-y", "--yes", action="store_true", help="do not ask for confirmation")
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("config", help="show settings, or create/edit config.toml")
    p.add_argument("--init", action="store_true", help="write a commented config.toml with every default")
    p.add_argument("--path", action="store_true", help="print the path of config.toml")
    p.set_defaults(func=cmd_config)


# -- helpers -------------------------------------------------------------------


def open_in_default_app(path: Path) -> bool:
    """Open a file with the desktop's default application. Returns False if that is not possible."""
    opener = "open" if sys.platform == "darwin" else shutil.which("xdg-open")
    if not opener:
        return False
    try:
        subprocess.Popen([opener, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except OSError:
        return False


def process_sessions(ctx: Context, sessions: list[Session], *, force: list[str] | None = None) -> list[Session]:
    """Run the pipeline for each session, printing progress. Returns the refreshed sessions."""
    from ..pipeline import Pipeline

    done: list[Session] = []
    for session in sessions:
        clips = ctx.store.list_clips(session.id)
        minutes = sum(c.duration for c in clips) / 60
        label = f"{fmt_clock(session.started_ts, '%a %d %b %H:%M')}"
        ctx.out.heading(f"Session {session.id}  ({label}, {len(clips)} clip(s){f', {minutes:.0f} min' if minutes else ''})")
        with Pipeline(ctx.settings, ctx.store, progress=progress_printer(ctx.out)) as pipeline:
            try:
                result = pipeline.process_session(session.id, force=force or ())
            except ValueError as exc:
                raise CliError(str(exc)) from exc
            for kind, reason in pipeline.unavailable().items():
                ctx.out.warn(f"{_KIND_LABELS.get(kind, kind)} skipped: {reason}")
        done.append(result)
        report_session(ctx, result)
    return done


_KIND_LABELS = {"asr": "Speech-to-text", "ocr": "Text recognition", "vision": "Frame descriptions", "llm": "LLM summary"}


def report_session(ctx: Context, session: Session) -> None:
    out = ctx.out
    errors = [
        (clip.id, stage, info.get("message", ""))
        for clip in ctx.store.list_clips(session.id)
        for stage, info in clip.stages.items()
        if info.get("status") == "error"
    ]
    for clip_id, stage, message in errors:
        out.warn(f"clip {clip_id}: {stage} failed: {message}")
    if session.note_path:
        out.ok(f"{session.title or 'Note'}  →  {ctx.settings.abs(session.note_path)}")
    if session.note and session.note.llm_backend == "extractive":
        out.info("  (summary built without an LLM: excerpts only. `vnote doctor` shows how to enable one.)")


def print_note(ctx: Context, session: Session, *, transcript: bool = False) -> None:
    out = ctx.out
    note = session.note
    span = fmt_clock(session.started_ts, "%a %d %b %Y  %H:%M")
    if session.ended_ts:
        span += f"–{fmt_clock(session.ended_ts)}  ({fmt_duration(session.ended_ts - session.started_ts)})"
    out.heading(note.title if note and note.title else session.title or f"Session {session.id}")
    out.info(f"{span}   [{session.id}]  status: {session.status}")
    if note is None:
        out.line("")
        out.line("Not summarised yet. Run `vnote process`.")
        return

    def section(title: str, items: list[str]) -> None:
        if items:
            out.line("")
            out.heading(title)
            for item in items:
                out.para(f"• {item}", indent=2)

    if note.summary:
        out.line("")
        out.para(note.summary)
    section("Key points", note.key_points)
    actions = []
    for a in note.action_items:
        extra = ", ".join(x for x in (a.owner, f"due {a.due}" if a.due else "") if x)
        when = f" [{fmt_clock(a.ts)}]" if a.ts else ""
        actions.append(f"{a.text}{f' ({extra})' if extra else ''}{when}")
    section("Action items", actions)
    section("Decisions", note.decisions)
    section("Open questions", note.open_questions)
    section("Captured text", note.captured_text)
    moments = ctx.store.list_moments(session.id)
    shown = [m for m in moments if m.salience != "background"]
    if shown:
        out.line("")
        out.heading("Timeline")
        for m in shown:
            mark = "★ " if m.salience == "highlight" else ""
            out.line(f"  {fmt_clock(m.ts0)}–{fmt_clock(m.ts1)}  {mark}{out.style(m.title or 'Untitled', 'bold')}")
            if m.summary:
                out.para(m.summary, indent=15)
        hidden = len(moments) - len(shown)
        if hidden:
            out.info(f"  (+ {hidden} quiet stretch(es), see the Markdown note)")
    if transcript:
        out.line("")
        out.heading("Transcript")
        for u in ctx.store.list_utterances(session_id=session.id):
            out.para(f"{fmt_clock(u.ts0, '%H:%M:%S')}  {u.text}", indent=2)
    if session.note_path:
        out.line("")
        out.info(f"Markdown note: {ctx.settings.abs(session.note_path)}")


# -- commands ------------------------------------------------------------------


def cmd_demo(ctx: Context, args: argparse.Namespace) -> int:
    from ..capture.importer import import_file
    from ..demo import make_demo_video

    out = ctx.out
    ctx.settings.ensure_dirs()
    out.line("Rendering a sample clip (a desk, a whiteboard, a door sign, a walk, a car park)…")
    clip_path = ctx.settings.cache_dir / "demo" / "videonotes-demo.mp4"
    info = make_demo_video(clip_path)
    if not info.has_speech:
        out.warn("No speech synthesiser found, so the sample has no voice track (on-screen text still works).")
    if not info.has_text:
        out.warn("This ffmpeg has no drawtext filter, so the sample has no on-screen text.")
    session = import_file(ctx.settings, ctx.store, clip_path, start_ts=now_ts() - info.duration)
    try:
        (result,) = process_sessions(ctx, [session])
    finally:
        clip_path.unlink(missing_ok=True)
    out.line("")
    print_note(ctx, ctx.store.get_session(result.id) or result)
    out.line("")
    if args.keep:
        out.info(f"Kept as session {result.id}. Remove it with `vnote delete {result.id}`.")
    else:
        delete_session_files(ctx, result)
        out.info("Demo session removed again (use --keep to keep it).")
    return 0


def cmd_add(ctx: Context, args: argparse.Namespace) -> int:
    from ..capture.importer import import_file

    sessions: list[Session] = []
    for name in args.files:
        path = Path(name).expanduser()
        if not path.is_file():
            raise CliError(f"No such file: {path}")
        session = import_file(ctx.settings, ctx.store, path)
        ctx.out.ok(f"Added {path.name} as session {session.id}")
        sessions.append(session)
    if not args.no_process:
        process_sessions(ctx, sessions)
    return 0


def cmd_process(ctx: Context, args: argparse.Namespace) -> int:
    if args.session == "all":
        sessions = ctx.store.list_sessions()
    elif args.session == "pending":
        sessions = [s for s in ctx.store.list_sessions() if s.status != "ready" or s.note is None]
        if not sessions and args.force:
            raise CliError("Nothing is pending. Name a session (or 'all') to use --force.")
    else:
        sessions = [ctx.require_session(args.session)]
    if not sessions:
        ctx.out.ok("Everything is up to date.")
        return 0
    sessions.sort(key=lambda s: s.started_ts)
    done = process_sessions(ctx, sessions, force=args.force)
    return EXIT_ERROR if any(s.status == "error" for s in done) else 0


def cmd_sessions(ctx: Context, args: argparse.Namespace) -> int:
    from ..timeutil import day_bounds

    since = until = None
    if args.day:
        try:
            since, until = day_bounds(parse_day(args.day))
        except ValueError as exc:
            raise CliError(f"Not a date: {args.day!r} (use YYYY-MM-DD, today or yesterday)") from exc
    sessions = ctx.store.list_sessions(since_ts=since, until_ts=until, limit=args.limit)
    if not sessions:
        ctx.out.line("No sessions yet. Try `vnote demo`, `vnote import` or `vnote add FILE`.")
        return 0
    rows = []
    for s in sessions:
        length = fmt_duration(s.ended_ts - s.started_ts) if s.ended_ts else "-"
        rows.append([s.id, fmt_clock(s.started_ts, "%a %d %b %H:%M"), length, s.kind, s.status, s.title or "(untitled)"])
    ctx.out.table(rows, header=["ID", "STARTED", "LENGTH", "SOURCE", "STATUS", "TITLE"])
    return 0


def cmd_show(ctx: Context, args: argparse.Namespace) -> int:
    session = ctx.require_session(args.session)
    print_note(ctx, session, transcript=args.transcript)
    if args.open:
        if not session.note_path:
            raise CliError("This session has no Markdown note yet.", hint="Run `vnote process` first.")
        if not open_in_default_app(ctx.settings.abs(session.note_path)):
            ctx.out.warn("Could not open the note automatically; open the path above yourself.")
    return 0


def cmd_day(ctx: Context, args: argparse.Namespace) -> int:
    from ..pipeline import Pipeline

    try:
        date = parse_day(args.date)
    except ValueError as exc:
        raise CliError(f"Not a date: {args.date!r} (use YYYY-MM-DD, today or yesterday)") from exc
    out = ctx.out
    with Pipeline(ctx.settings, ctx.store) as pipeline:
        path = pipeline.build_day(date)
    digest = ctx.store.get_day(date)
    if digest is None:
        out.line(f"Nothing recorded on {date}.")
        return 0
    out.heading(f"{date} — {digest.headline}" if digest.headline else date)
    if digest.summary:
        out.line("")
        out.para(digest.summary)
    if digest.highlights:
        out.line("")
        out.heading("Highlights")
        for item in digest.highlights:
            out.para(f"• {item}", indent=2)
    if digest.action_items:
        out.line("")
        out.heading("Action items")
        for a in digest.action_items:
            extra = ", ".join(x for x in (a.owner, f"due {a.due}" if a.due else "") if x)
            out.para(f"☐ {a.text}{f' ({extra})' if extra else ''}", indent=2)
    out.line("")
    out.heading("Sessions")
    for sid in digest.session_ids:
        s = ctx.store.get_session(sid)
        if s:
            out.line(f"  {fmt_clock(s.started_ts)}  {s.title or '(untitled)'}  [{s.id}]")
    out.line("")
    out.info(f"Markdown note: {path}")
    if args.open and not open_in_default_app(path):
        out.warn("Could not open the note automatically; open the path above yourself.")
    return 0


def cmd_search(ctx: Context, args: argparse.Namespace) -> int:
    from ..search import search

    try:
        day = parse_day(args.day) if args.day else None
    except ValueError as exc:
        raise CliError(f"Not a date: {args.day!r} (use YYYY-MM-DD, today or yesterday)") from exc
    query = " ".join(args.query)
    hits = search(ctx.store, query, limit=args.limit, kinds=args.kind, day=day)
    if not hits:
        ctx.out.line("No matches.")
        return 0
    labels = {"utterance": "said", "ocr": "seen (text)", "caption": "seen", "moment": "moment", "session": "note"}
    for hit in hits:
        when = fmt_clock(hit.ts, "%a %d %b %H:%M") if hit.ts else "-"
        head = f"{when}  {labels.get(hit.kind, hit.kind)}"
        ctx.out.line(f"{ctx.out.style(head, 'cyan')}  {ctx.out.style('[' + hit.session_id + ']', 'dim')}")
        ctx.out.para(" ".join(hit.snippet.split()), indent=4)
    return 0


def cmd_ask(ctx: Context, args: argparse.Namespace) -> int:
    from ..search import ask

    question = " ".join(args.question)
    answer = ask(ctx.settings, ctx.store, question)
    out = ctx.out
    out.para(answer.text or "Nothing in the library answers that.")
    if answer.llm_backend == "extractive" and answer.sources:
        out.line("")
        out.info("(No LLM available: these are the closest excerpts, not a written answer.)")
    if args.sources and answer.sources:
        out.line("")
        out.heading("Evidence")
        for e in answer.sources:
            when = fmt_clock(e.ts, "%a %d %b %H:%M") if e.ts else "-"
            out.line(f"  {out.style(when, 'cyan')}  {e.kind}  {out.style('[' + e.session_id + ']', 'dim')}")
            out.para(" ".join(e.text.split())[:400], indent=6)
    return 0


def delete_session_files(ctx: Context, session: Session) -> None:
    """Remove a session and everything derived from it. Media outside the library is never touched."""
    settings = ctx.settings
    targets = [
        settings.media_dir / session.id,
        settings.frames_dir / session.id,
        settings.cache_dir / session.id,
        settings.vault_dir / "assets" / session.id,
    ]
    for target in targets:
        shutil.rmtree(target, ignore_errors=True)
    if session.note_path:
        settings.abs(session.note_path).unlink(missing_ok=True)
    ctx.store.delete_session(session.id)
    try:
        from ..notes.render import render_day_note

        render_day_note(settings, ctx.store, local_date(session.started_ts))
    except Exception:  # the day note is a convenience; deletion already succeeded
        pass


def cmd_delete(ctx: Context, args: argparse.Namespace) -> int:
    session = ctx.require_session(args.session)
    label = f"{session.id}  {fmt_clock(session.started_ts, '%a %d %b %H:%M')}  {session.title or '(untitled)'}"
    if not args.yes:
        if not sys.stdin.isatty():
            raise CliError("Refusing to delete without confirmation.", hint="Add --yes to confirm.")
        reply = input(f"Delete session {label} with its media copies, keyframes and note? [y/N] ")
        if reply.strip().lower() not in ("y", "yes"):
            ctx.out.line("Nothing deleted.")
            return 0
    delete_session_files(ctx, session)
    ctx.out.ok(f"Deleted {label}")
    return 0


def cmd_config(ctx: Context, args: argparse.Namespace) -> int:
    path = ctx.settings.config_path
    if args.path:
        ctx.out.line(str(path))
        return 0
    if args.init:
        if path.exists():
            raise CliError(f"{path} already exists; edit it, or delete it first.")
        ctx.settings.ensure_dirs()
        path.write_text(default_config_text(), encoding="utf-8")
        ctx.out.ok(f"Wrote {path}")
        return 0
    ctx.out.info(f"# {path}{'' if path.exists() else '  (not created yet: `vnote config --init`)'}")
    ctx.out.info(f"# library: {ctx.settings.home}")
    for section, values in ctx.settings.to_dict().items():
        if not isinstance(values, dict):
            continue
        ctx.out.line("")
        ctx.out.heading(f"[{'import' if section == 'imports' else section}]")
        for key, value in values.items():
            ctx.out.line(f"{key} = {value!r}")
    return 0
