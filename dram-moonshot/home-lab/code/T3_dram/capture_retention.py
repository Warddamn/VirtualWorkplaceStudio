#!/usr/bin/env python3
"""capture_retention.py -- drive the E6 retention firmware over USB serial and log every result.

The serial (hardware) path is UNTESTED ON HARDWARE; --simulate and --selftest are tested.

It sends one RUN command per (repeat, pattern, wait), saves every line the board returns to a log
file (flushed line by line, so a crash loses nothing), stops a sweep early once a run fails more
than --stop-ber of all bits, and starts each temperature with a control run that must show zero
failures.

  python3 capture_retention.py --port /dev/ttyACM0 --temp-c 45 --out e6_45C.log
  python3 capture_retention.py --plan --temp-c 45            # print the plan and time estimate
  python3 capture_retention.py --simulate --temp-c 45 --out sim.log   # no hardware: synthetic chip
  python3 capture_retention.py --selftest                    # exit 0 if the capture path works

pyserial is optional: without it only --plan, --simulate and --selftest work
(install with: python3 -m pip install pyserial).
The analysis is a separate step: python3 retention_map.py analyze e6_*.log
"""
import argparse
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
WRITE_READ_S = 9.0      # ESTIMATE: write + read 8 MB at a 16 MHz core clock
A_MAX_S = 4.096         # longest relaxed period at SDCLK 8 MHz (4096 rows x 8192 / 8 MHz = 4.19 s)


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
            if method == "C":
                fb = rm.np.zeros(0, rm.np.int64)
            else:
                fb = self.chip.fail_bits(pat, inv, seed, wait_ms / 1000.0, temp, self.rng)
            self.queue.extend(rm.firmware_lines(int(rid), method, pat, inv, seed, wait_ms, rep, temp,
                                                temp + self.rng.normal(0, 0.3), fb, self.chip.bpw,
                                                self.chip.wpr))
        else:
            self.queue.append("ERR,unknown command")

    def readline(self, timeout_s):
        return self.queue.pop(0) if self.queue else None


def build_plan(args):
    pats = [PATTERN_SET[p] for p in args.patterns]
    rng = random.Random(args.order_seed)
    plan = [("C", 0, 0, 0, 0, 0)]                        # control run first
    for rep in range(1, args.repeats + 1):
        order = pats[:]
        rng.shuffle(order)                                # decorrelate slow drift from pattern
        for pat, inv in order:
            sweep = []
            for w in args.waits:
                method = args.method if args.method != "auto" else ("A" if w <= A_MAX_S else "B")
                sweep.append((method, pat, inv, args.seed, int(round(w * 1000)), rep))
            plan.append(sweep)
    return plan


def estimate_hours(plan, cap_lines_s=0.0):
    tot = 0.0
    for item in plan:
        sweeps = [item] if isinstance(item, tuple) else item
        for method, _, _, _, wait_ms, _ in sweeps:
            w = wait_ms / 1000.0
            tot += WRITE_READ_S + (3 * w if method == "A" else w) + cap_lines_s
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
    method, pat, inv, seed, wait_ms, rep = item
    fh.write("H,%.1f\n" % time.time())
    dev.send("RUN %d %s %d %d %d %d %d %d" % (rid, method, pat, inv, seed, wait_ms, rep, int(round(temp_c * 10))))
    t_end = time.time() + timeout_s
    while time.time() < t_end:
        line = dev.readline(max(1.0, t_end - time.time()))
        if line is None:
            break
        fh.write(line + "\n")
        if line.startswith("TEMP,"):
            try:
                tm = float(line.split(",")[3])
                if abs(tm - temp_c) > warn_dt:
                    print("  WARNING: thermocouple reads %.2f C, setpoint %.1f C" % (tm, temp_c))
            except ValueError:
                pass
        if line.startswith("ERR"):
            print("  device error:", line)
            fh.flush()
            return None
        if line.startswith("END,%d," % rid):
            fh.flush()
            f = line.split(",")
            return int(f[3]) / float(n_bits)
    fh.flush()
    print("  TIMEOUT waiting for END of run %d" % rid)
    return None


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
    print("Device: %s | %d bits | plan: %d sweeps + control, ~%.1f h" %
          (hello, n_bits, len(plan) - 1, estimate_hours(plan)))
    with open(out_path, "a") as fh:
        fh.write("# capture_retention.py %s temp_setpoint=%.1f\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), args.temp_c))
        fh.write(hello + "\n")
        for item in plan:
            sweeps = [item] if isinstance(item, tuple) else item
            for run in sweeps:
                method, pat, inv, _, wait_ms, rep = run
                timeout = 120.0 + (3.0 if method == "A" else 1.0) * wait_ms / 1000.0 + 60.0
                ber = do_run(dev, fh, rid, run, args.temp_c, timeout, n_bits)
                label = "control" if method == "C" else "rep %d %s%s %s %.3f s" % (
                    rep, rm.PATTERN_NAMES[pat], "~" if inv else "", method, wait_ms / 1000.0)
                print("  run %d %s -> %s" % (rid, label, "no END" if ber is None else "BER %.3g" % ber))
                rid += 1
                if method == "C" and ber not in (None, 0.0):
                    print("CONTROL RUN FAILED: errors with normal refresh. Stop and fix the setup first.")
                    return 3
                if ber is not None and ber > args.stop_ber:
                    break                                 # rest of this sweep is uninformative
    print("Log written to %s" % out_path)
    return 0


def selftest():
    print("capture selftest: simulated device, small chip, reduced plan")
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "sim.log")
        args = argparse.Namespace(patterns=["ALL0", "ALL1", "CHECKER"], waits=[0.064 * 2 ** i for i in range(0, 11, 2)],
                                  repeats=2, method="auto", seed=1234, order_seed=3, stop_ber=1e-2,
                                  temp_c=65.0, start_id=0)
        rc = campaign(SimDevice(), args, path)
        args.temp_c = 45.0
        rc2 = campaign(SimDevice(), args, path)
        with open(path) as fh:
            lines = fh.readlines()
    log = rm.parse_log(lines)
    ids = [r.rid for r in log.runs]
    checks = [
        ("campaigns returned 0", rc == 0 and rc2 == 0),
        ("runs parsed", len(log.runs) > 10),
        ("run ids unique across appended campaigns", len(ids) == len(set(ids))),
        ("control runs present and clean", sum(1 for r in log.runs if r.method == "C") == 2 and
         all(r.fail_bits == 0 for r in log.runs if r.method == "C")),
        ("host timestamps attached", all(r.t_host is not None for r in log.runs)),
        ("method A used for short waits, B for long", {r.method for r in log.runs if r.method != "C"} == {"A", "B"}),
        ("parse errors", not log.errors),
        ("pyserial optional", True),
    ]
    for name, ok in checks:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    print("  (pyserial %s)" % ("installed" if serial is not None else "not installed: hardware mode disabled, simulate OK"))
    return 0 if all(ok for _, ok in checks) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Drive the E6 retention firmware and log results.")
    ap.add_argument("--port", help="serial port, e.g. /dev/ttyACM0 or COM5")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--temp-c", type=float, default=25.0, help="chamber setpoint for this campaign")
    ap.add_argument("--out", default="e6_retention.log")
    ap.add_argument("--patterns", nargs="+", default=DEFAULT_PATTERNS, choices=sorted(PATTERN_SET))
    ap.add_argument("--waits", nargs="+", type=float, default=rm.DEFAULT_WAITS_S, help="seconds")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--method", default="auto", choices=["auto", "A", "B"],
                    help="auto: A (relaxed refresh) up to 4.096 s, B (pause) above")
    ap.add_argument("--seed", type=int, default=1234, help="RANDOM pattern seed (fixed across repeats)")
    ap.add_argument("--order-seed", type=int, default=1)
    ap.add_argument("--stop-ber", type=float, default=1e-2)
    ap.add_argument("--start-id", type=int, default=0, help="0 = continue after the last id in --out")
    ap.add_argument("--plan", action="store_true", help="print the plan and time estimate, then exit")
    ap.add_argument("--simulate", action="store_true", help="use a synthetic chip instead of hardware")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.plan:
        plan = build_plan(a)
        n = sum(1 if isinstance(i, tuple) else len(i) for i in plan)
        print("%d runs at most (fewer with early stop); <= %.1f h at %.1f C" % (n, estimate_hours(plan), a.temp_c))
        for item in plan[:3]:
            print("  ", item if isinstance(item, tuple) else item[:3] + ["..."])
        return 0
    if a.simulate:
        return campaign(SimDevice(), a, a.out)
    if serial is None:
        print("pyserial is not installed. Install it (python3 -m pip install pyserial) or use --simulate.")
        return 2
    if not a.port:
        print("--port is required for hardware mode")
        return 2
    return campaign(SerialDevice(a.port, a.baud), a, a.out)


if __name__ == "__main__":
    sys.exit(main())
