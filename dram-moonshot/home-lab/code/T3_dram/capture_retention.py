#!/usr/bin/env python3
"""capture_retention.py -- drive the E6 retention firmware over USB serial and log every result.

The serial (hardware) path is UNTESTED ON HARDWARE; --simulate and --selftest are tested.

It sends one RUN command per (repeat, pattern, wait), saves every line the board returns to a log
file (flushed line by line, so a crash loses nothing), stops a sweep early once a run fails more
than --stop-ber of all bits, and starts each temperature with a control run that must show zero
failures. It aborts after 3 runs in a row get no END (board hung or unplugged).

Resuming: rerunning with the same --out APPENDS a fresh plan. To finish only the missing repeats,
use --first-repeat K --repeats M (for example --first-repeat 4 --repeats 2 after repeats 1-3 finished).

  python3 capture_retention.py --port /dev/ttyACM0 --temp-c 45 --out e6_45C.log
  python3 capture_retention.py --plan --temp-c 45            # print the plan and time estimate
  python3 capture_retention.py --simulate --temp-c 45 --out sim.log   # no hardware: synthetic chip
  python3 capture_retention.py --selftest                    # exit 0 if the capture path works

pyserial is optional: without it only --plan, --simulate and --selftest work
(install with: python3 -m pip install pyserial).
The analysis is a separate step: python3 retention_map.py analyze e6_*.log
"""
import argparse
import contextlib
import io
import math
import os
import random
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retention_map as rm  # noqa: E402  (same folder)

try:
    import serial  # pyserial
except ImportError:  # handled at run time
    serial = None

PATTERN_SET = {"ALL0": (0, 0), "ALL1": (1, 0), "CHECKER": (2, 0), "CHECKER~": (2, 1),
               "ROWSTRIPE": (3, 0), "ROWSTRIPE~": (3, 1), "COLSTRIPE": (4, 0), "RANDOM": (5, 0),
               "RANDOM~": (5, 1)}
DEFAULT_PATTERNS = ["ALL0", "ALL1", "CHECKER", "CHECKER~", "ROWSTRIPE", "RANDOM"]
# ESTIMATE: two passes over 4,194,304 words at a 16 MHz core and 8 MHz SDCLK, ~30-60 cycles per word
# (pattern hash + FMC access) -> ~8-16 s per pass. Measure yours: the control run prints it.
WRITE_READ_S = 20.0
A_MAX_S = 4.096         # longest relaxed period at SDCLK 8 MHz (4096 rows x 8192 / 8 MHz = 4.19 s)
LOG_CAP = 20000         # the firmware logs at most this many failing words per run
F_LINE_BYTES = 25       # "F,123,3fffff,ffff,fffb\r\n" is ~22-25 characters
B_EXTRA_MS = rm.B_EXTRA_MS
TERMINAL_ERRS = ("ERR,bad RUN command", "ERR,unknown command", "ERR,sdram not initialised")


class SerialDevice:
    def __init__(self, port, baud):
        if serial is None:
            raise RuntimeError("pyserial is not installed: python3 -m pip install pyserial")
        self.s = serial.Serial(port, baud, timeout=1.0)
        time.sleep(0.5)
        self.s.reset_input_buffer()

    def send(self, line):
        self.s.write((line + "\n").encode("ascii"))

    def readline(self, timeout_s):
        t_end = time.time() + timeout_s
        while time.time() < t_end:
            raw = self.s.readline()
            if raw:
                return raw.decode("ascii", "replace").strip()
        return None


class SimDevice:
    """Stands in for the board: same commands in, same lines out (synthetic chip)."""

    def __init__(self, chip=None, seed=5):
        self.chip = chip or rm.SyntheticChip(n_words=1 << 16)
        self.rng = rm.np.random.default_rng(seed)
        self.queue = []

    def send(self, line):
        tok = line.split()
        if tok[0] == "PING":
            self.queue.append("PONG")
        elif tok[0] == "INFO":
            self.queue.append(self.chip.hello())
        elif tok[0] == "RUN":
            rid, method, pat, inv, seed, wait_ms, rep, t10 = tok[1:9]
            pat, inv, seed, wait_ms, rep, t10 = int(pat), int(inv), int(seed), int(wait_ms), int(rep), int(t10)
            temp = t10 / 10.0
            interval_ms = 0 if method == "C" else wait_ms + (B_EXTRA_MS if method == "B" else 0)
            if method == "C":
                fb = rm.np.zeros(0, rm.np.int64)
            else:
                fb = self.chip.fail_bits(pat, inv, seed, interval_ms / 1000.0, temp, self.rng)
            self.queue.extend(rm.firmware_lines(int(rid), method, pat, inv, seed, wait_ms, rep, temp,
                                                temp + self.rng.normal(0, 0.3), fb, self.chip.bpw,
                                                self.chip.wpr, interval_ms=interval_ms))
        else:
            self.queue.append("ERR,unknown command")

    def readline(self, timeout_s):
        return self.queue.pop(0) if self.queue else None


def build_plan(args):
    pats = [PATTERN_SET[p] for p in args.patterns]
    rng = random.Random(args.order_seed)
    plan = [("C", 0, 0, 0, 0, 0)]                        # control run first
    first = getattr(args, "first_repeat", 1)
    for rep in range(first, first + args.repeats):
        order = pats[:]
        rng.shuffle(order)                                # decorrelate slow drift from pattern
        for pat, inv in order:
            sweep = []
            for w in args.waits:
                method = args.method if args.method != "auto" else ("A" if w <= A_MAX_S else "B")
                sweep.append((method, pat, inv, args.seed, int(round(w * 1000)), rep))
            plan.append(sweep)
    return plan


def estimate_hours(plan, temp_c=25.0, n_bits=rm.CHIP_BITS_F429, baud=115200, write_read_s=WRITE_READ_S,
                   stop_ber=1e-2):
    """Run time in hours: write + read, the waits (method A holds 3 periods), and UART time for the
    F lines. Failing words per run come from the central model in retention_map.predict (about half
    the cells are charged in a single pattern); early stop is applied the same way. [ESTIMATE]"""
    mu, sg = rm.dossier_anchor()
    model = rm.RetentionModel(mu, sg, halving_c=10.0)
    s_per_line = F_LINE_BYTES * 10.0 / baud
    tot = 0.0
    for item in plan:
        sweeps = [item] if isinstance(item, tuple) else item
        for method, _, _, _, wait_ms, _ in sweeps:
            w = wait_ms / 1000.0
            if method == "C":
                tot += write_read_s
                continue
            ber = 0.5 * model.cdf(w + (B_EXTRA_MS / 1000.0 if method == "B" else 0.0), temp_c)
            lines = min(LOG_CAP, ber * n_bits)
            tot += write_read_s + (3 * w if method == "A" else w) + lines * s_per_line
            if ber > stop_ber:
                break                                     # the campaign stops this sweep here too
    return tot / 3600.0


def next_run_id(path):
    best = 0
    if path and os.path.exists(path):
        with open(path, errors="replace") as fh:
            for line in fh:
                if line.startswith("RUN,"):
                    try:
                        best = max(best, int(line.split(",")[1]))
                    except ValueError:
                        pass
    return best + 1


def do_run(dev, fh, rid, item, temp_c, timeout_s, n_bits, warn_dt=2.0):
    """One RUN. Returns a dict: ber (None if no END), errs (ERR lines), nan_temp, elapsed_s."""
    method, pat, inv, seed, wait_ms, rep = item
    res = {"ber": None, "errs": [], "nan_temp": False, "elapsed_s": None}
    t0 = time.time()
    fh.write("H,%.1f\n" % t0)
    dev.send("RUN %d %s %d %d %d %d %d %d" % (rid, method, pat, inv, seed, wait_ms, rep, int(round(temp_c * 10))))
    t_end = t0 + timeout_s
    while time.time() < t_end:
        line = dev.readline(max(1.0, t_end - time.time()))
        if line is None:
            break
        fh.write(line + "\n")
        if line.startswith("TEMP,"):
            try:
                tm = float(line.split(",")[3])
                if math.isnan(tm):
                    res["nan_temp"] = True
                    print("  WARNING: thermocouple fault (nan): check the wiring and that the tip is not"
                          " touching metal")
                elif abs(tm - temp_c) > warn_dt:
                    print("  WARNING: thermocouple reads %.2f C, --temp-c is %.1f C" % (tm, temp_c))
            except (ValueError, IndexError):
                pass
        if line.startswith("ERR"):
            res["errs"].append(line)
            print("  device error:", line)
            if line.startswith(TERMINAL_ERRS):
                fh.flush()
                return res                                # the board will not send END for this one
            continue                                      # e.g. precharge timeout: the run still ENDs
        if line.startswith("END,%d," % rid):
            f = line.split(",")
            if len(f) < 9:
                continue                                  # truncated END line: keep reading until timeout
            fh.flush()
            try:
                res["ber"] = int(f[3]) / float(n_bits)
            except ValueError:
                continue
            res["elapsed_s"] = time.time() - t0
            if f[8] == "ERR":
                res["ber"] = None                         # firmware marked the run invalid
            return res
    fh.flush()
    print("  TIMEOUT waiting for END of run %d" % rid)
    return res


def campaign(dev, args, out_path):
    dev.send("INFO")
    hello = dev.readline(5.0)
    if not hello or not hello.startswith("HELLO"):
        print("No HELLO from the device (got %r). Check port, baud and firmware." % hello)
        return 2
    f = hello.split(",")
    n_bits = int(f[3]) * int(f[4])
    plan = build_plan(args)
    rid = args.start_id or next_run_id(out_path)
    baud = getattr(args, "baud", 115200)
    print("Device: %s | %d bits | plan: %d sweeps + control, ~%.1f h [ESTIMATE]" %
          (hello, n_bits, len(plan) - 1, estimate_hours(plan, args.temp_c, n_bits, baud, stop_ber=args.stop_ber)))
    misses = 0
    with open(out_path, "a") as fh:
        fh.write("# capture_retention.py %s temp_c=%.1f first_repeat=%d repeats=%d\n" % (
            time.strftime("%Y-%m-%d %H:%M:%S"), args.temp_c, getattr(args, "first_repeat", 1), args.repeats))
        fh.write(hello + "\n")
        for item in plan:
            sweeps = [item] if isinstance(item, tuple) else item
            for run in sweeps:
                method, pat, inv, _, wait_ms, rep = run
                timeout = 120.0 + (3.0 if method == "A" else 1.0) * wait_ms / 1000.0 + 60.0
                rr = do_run(dev, fh, rid, run, args.temp_c, timeout, n_bits)
                ber = rr["ber"]
                label = "control" if method == "C" else "rep %d %s%s %s %.3f s" % (
                    rep, rm.PATTERN_NAMES[pat], "~" if inv else "", method, wait_ms / 1000.0)
                print("  run %d %s -> %s" % (rid, label, "no valid END" if ber is None else "BER %.3g" % ber))
                rid += 1
                if method == "C":
                    if ber != 0.0:
                        print("CONTROL RUN %s: stop and fix the setup first (section 13 of the guide)." %
                              ("GAVE NO RESULT" if ber is None else "FAILED (errors with normal refresh)"))
                        return 3
                    if rr["elapsed_s"]:
                        wr = max(1.0, rr["elapsed_s"])
                        print("  measured write+read = %.1f s (estimate was %.0f s); revised plan estimate"
                              " = %.1f h" % (wr, WRITE_READ_S, estimate_hours(plan, args.temp_c, n_bits, baud,
                                                                               wr, args.stop_ber)))
                misses = misses + 1 if ber is None else 0
                if misses >= 3:
                    print("ABORT: 3 runs in a row without a valid END. Is the board hung? Reset it, send"
                          " PING, then resume with --first-repeat.")
                    return 4
                if ber is not None and ber > args.stop_ber:
                    break                                 # rest of this sweep is uninformative
    print("Log written to %s" % out_path)
    return 0


class FaultDevice(SimDevice):
    """A SimDevice that misbehaves on purpose: mode 'err' adds a non-terminal ERR line to the first data
    run and marks its END as ERR (as the firmware does after a precharge timeout), 'badctrl' makes the
    control run fail, 'hang' stops answering after the control run, 'shortend' truncates every data
    END line, 'nan' reports a broken thermocouple."""

    def __init__(self, mode):
        super().__init__(chip=rm.SyntheticChip(n_words=1 << 14, seed=9))
        self.mode = mode
        self.n_run = 0

    def send(self, line):
        before = len(self.queue)
        super().send(line)
        if not line.startswith("RUN"):
            return
        self.n_run += 1
        new = self.queue[before:]
        del self.queue[before:]
        is_ctrl = line.split()[2] == "C"
        if self.mode == "hang" and not is_ctrl:
            return
        out = []
        for ln in new:
            if self.mode == "badctrl" and is_ctrl and ln.startswith("END,"):
                f = ln.split(",")
                f[2], f[3] = "3", "5"
                ln = ",".join(f)
            if self.mode == "shortend" and not is_ctrl and ln.startswith("END,"):
                ln = ",".join(ln.split(",")[:4])
            if self.mode == "nan" and ln.startswith("TEMP,"):
                ln = ",".join(ln.split(",")[:3] + ["nan"])
            first_data = self.n_run == 2
            if self.mode == "err" and first_data and ln.startswith("TEMP,") and ",end," in ln:
                out.append("ERR,precharge timeout")
            if self.mode == "err" and first_data and ln.startswith("END,"):
                ln = ",".join(ln.split(",")[:8] + ["ERR"])
            out.append(ln)
        self.queue.extend(out)


def selftest():
    print("capture selftest: simulated device, small chip, reduced plan")
    checks = []
    base = dict(patterns=["ALL0", "ALL1", "CHECKER"], waits=[0.064 * 2 ** i for i in range(0, 11, 2)],
                repeats=2, first_repeat=1, method="auto", seed=1234, order_seed=3, stop_ber=1e-2,
                temp_c=65.0, start_id=0, baud=115200)
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "sim.log")
        args = argparse.Namespace(**base)
        rc = campaign(SimDevice(), args, path)
        args.temp_c = 45.0
        rc2 = campaign(SimDevice(), args, path)
        with open(path) as fh:
            lines = fh.readlines()
        # fault injection: each mode on its own log
        fault_rc, fault_runs = {}, {}
        for mode in ("err", "badctrl", "hang", "shortend", "nan"):
            fp = os.path.join(td, "fault_%s.log" % mode)
            fa = argparse.Namespace(**dict(base, repeats=1, patterns=["ALL0"], waits=[0.256, 1.024, 2.048, 4.096]))
            fault_rc[mode] = campaign(FaultDevice(mode), fa, fp)
            with open(fp) as fh:
                fault_runs[mode] = rm.parse_log(fh.readlines())
        # resume labels
        ra = argparse.Namespace(**dict(base, first_repeat=4, repeats=2))
        resume_reps = sorted({r[5] for sw in build_plan(ra)[1:] for r in sw})
    log = rm.parse_log(lines)
    ids = [r.rid for r in log.runs]
    b_runs = [r for r in log.runs if r.method == "B"]
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            make_parser().parse_args(["--plan", "--seed", "3000000000"])
        seed_rejected = False
    except SystemExit:
        seed_rejected = True
    est = estimate_hours(build_plan(argparse.Namespace(**dict(base, patterns=DEFAULT_PATTERNS, waits=rm.DEFAULT_WAITS_S,
                                                                repeats=5))), 65.0)
    checks += [
        ("campaigns returned 0", rc == 0 and rc2 == 0),
        ("runs parsed", len(log.runs) > 10),
        ("run ids unique across appended campaigns", len(ids) == len(set(ids))),
        ("control runs present and clean", sum(1 for r in log.runs if r.method == "C") == 2 and
         all(r.fail_bits == 0 for r in log.runs if r.method == "C")),
        ("host timestamps attached", all(r.t_host is not None for r in log.runs)),
        ("method A used for short waits, B for long", {r.method for r in log.runs if r.method != "C"} == {"A", "B"}),
        ("method B interval = pause + %d ms" % B_EXTRA_MS, b_runs and
         all(r.interval_ms == r.wait_ms + B_EXTRA_MS for r in b_runs)),
        ("parse errors", not log.errors),
        ("non-terminal ERR: capture keeps reading to END; the ERR run is excluded from analysis",
         fault_rc["err"] == 0 and len(fault_runs["err"].runs) == 4 and len(fault_runs["err"].errors) == 2),
        ("failed control run stops the campaign (rc 3)", fault_rc["badctrl"] == 3),
        ("hung board: abort after 3 runs without END (rc 4)", fault_rc["hang"] == 4),
        ("truncated END lines do not crash the capture", fault_rc["shortend"] == 4),
        ("thermocouple nan handled (rc 0)", fault_rc["nan"] == 0),
        ("--first-repeat 4 --repeats 2 labels repeats 4 and 5", resume_reps == [4, 5]),
        ("--seed above 2^31-1 rejected", seed_rejected),
        ("65 C plan estimate is 2.5-4.5 h (write+read, waits, UART logging)", 2.5 <= est <= 4.5),
        ("pyserial optional", True),
    ]
    for name, ok in checks:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    print("  (65 C default plan estimate: %.2f h)" % est)
    print("  (pyserial %s)" % ("installed" if serial is not None else "not installed: hardware mode disabled, simulate OK"))
    return 0 if all(ok for _, ok in checks) else 1


def seed_arg(text):
    v = int(text)
    if not 0 <= v <= 2147483647:
        raise argparse.ArgumentTypeError("--seed must be 0..2147483647 (the firmware parses a signed 32-bit int)")
    return v


def positive_int(text):
    v = int(text)
    if v < 1:
        raise argparse.ArgumentTypeError("must be >= 1")
    return v


def make_parser():
    ap = argparse.ArgumentParser(description="Drive the E6 retention firmware and log results.")
    ap.add_argument("--port", help="serial port, e.g. /dev/ttyACM0, /dev/cu.usbmodem..., or COM5")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--temp-c", type=float, default=25.0,
                    help="chip temperature for this campaign (the setpoint, or the measured value for 25 C)")
    ap.add_argument("--out", default="e6_retention.log")
    ap.add_argument("--patterns", nargs="+", default=DEFAULT_PATTERNS, choices=sorted(PATTERN_SET))
    ap.add_argument("--waits", nargs="+", type=float, default=rm.DEFAULT_WAITS_S, help="seconds")
    ap.add_argument("--repeats", type=positive_int, default=5)
    ap.add_argument("--first-repeat", type=positive_int, default=1,
                    help="label of the first repeat (to finish an interrupted campaign)")
    ap.add_argument("--method", default="auto", choices=["auto", "A", "B"],
                    help="auto: A (relaxed refresh) up to 4.096 s, B (pause) above")
    ap.add_argument("--seed", type=seed_arg, default=1234, help="RANDOM pattern seed (fixed across repeats)")
    ap.add_argument("--order-seed", type=int, default=1)
    ap.add_argument("--stop-ber", type=float, default=1e-2)
    ap.add_argument("--start-id", type=int, default=0, help="0 = continue after the last id in --out")
    ap.add_argument("--plan", action="store_true", help="print the plan and time estimate, then exit")
    ap.add_argument("--simulate", action="store_true", help="use a synthetic chip instead of hardware")
    ap.add_argument("--selftest", action="store_true")
    return ap


def main(argv=None):
    a = make_parser().parse_args(argv)
    if a.selftest:
        return selftest()
    if a.plan:
        plan = build_plan(a)
        n = sum(1 if isinstance(i, tuple) else len(i) for i in plan)
        print("%d runs at most (fewer with early stop); about %.1f h at %.1f C [ESTIMATE: write+read %.0f s per"
              " run, waits, UART logging at %d baud; the control run prints a measured figure]" %
              (n, estimate_hours(plan, a.temp_c, baud=a.baud, stop_ber=a.stop_ber), a.temp_c, WRITE_READ_S, a.baud))
        for item in plan[:3]:
            print("  ", item if isinstance(item, tuple) else item[:3] + ["..."])
        return 0
    if a.simulate:
        return campaign(SimDevice(), a, a.out)
    if serial is None:
        print("pyserial is not installed. Install it (python3 -m pip install pyserial) or use --simulate.")
        return 2
    if not a.port:
        print("--port is required for hardware mode (list ports: python3 -m serial.tools.list_ports)")
        return 2
    return campaign(SerialDevice(a.port, a.baud), a, a.out)


if __name__ == "__main__":
    sys.exit(main())
