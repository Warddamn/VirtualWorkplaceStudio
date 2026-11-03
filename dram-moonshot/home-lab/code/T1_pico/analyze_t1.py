#!/usr/bin/env python3
"""
analyze_t1.py -- turn the CSV logs from the T1 Pico scripts into the numbers each guide asks for.

Runs on a PC with Python 3 + numpy (no scipy, no matplotlib). Written 2026-11-03 for the DRAM Moonshot home lab.

    python3 analyze_t1.py --selftest                 # synthetic data for every analysis; exit 0 on pass
    python3 analyze_t1.py share e1_share.csv         # E1 charge sharing: measured vs predicted dV, fitted strays
    python3 analyze_t1.py destructive e1_destr.csv   # E1 destructive read: signal ratio per read
    python3 analyze_t1.py decay e1_peek.csv --c-pf 1000            # leakage from a decay curve (E1 peek)
    python3 analyze_t1.py decay e2_ret.csv --c-pf 110 --col v_out  # E2: one result per cell
    python3 analyze_t1.py retmap e1_retmap.csv       # E1 16-cell retention distribution, tails, ECC gain
    python3 analyze_t1.py temp cold.csv room.csv warm.csv          # retention vs temperature -> Ea
    python3 analyze_t1.py energy e3_sweep.csv        # E3: C from slope of I vs f; energy per cycle
    python3 analyze_t1.py mlc e2_mlc.csv             # E2: 2-bit level errors vs hold time
    python3 analyze_t1.py transfer e2_transfer.csv   # E2: read-FET threshold and follower gain per cell

Input: the CSV printed by the Pico scripts (lines starting with '#' and prompt echoes are ignored; a line that
starts with 'exp,' starts a new header block).
"""

import argparse
import math
import os
import sys
import tempfile

import numpy as np

KB_EV = 8.617333e-5
KNOWN_EXP = ("E1A", "E1B", "E2", "E3")


# --------------------------------------------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------------------------------------------
def read_rows(path):
    rows = []
    header = None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if parts[0] == "exp":
                header = parts
                continue
            if header is None or len(parts) != len(header) or parts[0] not in KNOWN_EXP:
                continue          # prompt echoes, partial lines, noise
            rows.append(dict(zip(header, parts)))
    return rows


def fnum(x, default=float("nan")):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


# --------------------------------------------------------------------------------------------------------------
# Analyses
# --------------------------------------------------------------------------------------------------------------
def share_model(v_write, v_pre, cs, cbl):
    return (v_write - v_pre) * cs / (cs + cbl)


def analyze_share(rows, v_write=3.3, quiet=False):
    sel = [r for r in rows if r.get("mode") == "share"]
    groups = {}
    for r in sel:
        key = (fnum(r["cs_nF"]), fnum(r["cbl_nF"]), int(fnum(r["stored_bit"])))
        groups.setdefault(key, []).append(r)
    keys = sorted(groups)
    meas = []
    for k in keys:
        g = groups[k]
        dv = np.array([fnum(r["dv"]) for r in g])
        vpre = np.array([fnum(r["v_pre"]) for r in g])
        meas.append((k, float(np.mean(dv)), float(np.std(dv)), float(np.mean(vpre)),
                     float(np.mean([fnum(r["sa_bit"]) == k[2] for r in g]))))
    # fit one stray capacitance (pF) shared by all points, by grid search on squared error
    best = (float("inf"), 0.0)
    for cx_pf in np.arange(0.0, 300.0, 0.5):
        err = 0.0
        for (cs, cbl, bit), dv, _, vpre, _ in meas:
            pred = share_model(v_write if bit else 0.0, vpre, cs, cbl + cx_pf / 1e3)
            err += (dv - pred) ** 2
        best = min(best, (err, float(cx_pf)))
    cx = best[1]
    out = []
    if not quiet:
        print("Charge sharing: dV = (Vcell - Vpre) * Cs / (Cs + Cbl + Cstray); fitted Cstray = %.1f pF" % cx)
        print("%6s %7s %4s %10s %8s %12s %12s %9s %8s" % ("Cs nF", "Cbl nF", "bit", "dV mV", "sd mV",
                                                         "pred(0) mV", "pred(fit) mV", "meas/pred", "SA ok"))
    for (cs, cbl, bit), dv, sd, vpre, ok in meas:
        p0 = share_model(v_write if bit else 0.0, vpre, cs, cbl)
        p1 = share_model(v_write if bit else 0.0, vpre, cs, cbl + cx / 1e3)
        out.append((cs, cbl, bit, dv, p1))
        if not quiet:
            print("%6.2f %7.2f %4d %10.1f %8.1f %12.1f %12.1f %9.3f %7.0f%%" % (cs, cbl, bit, dv * 1e3, sd * 1e3,
                                                                                p0 * 1e3, p1 * 1e3, dv / p1, ok * 100))
    return cx, out


def analyze_destructive(rows, quiet=False):
    sel = [r for r in rows if r.get("mode") == "destructive"]
    sel.sort(key=lambda r: int(fnum(r["read_idx"])))
    dvs = [fnum(r["dv"]) for r in sel]
    ratios = [dvs[i + 1] / dvs[i] for i in range(len(dvs) - 1) if dvs[i] != 0]
    if sel and not quiet:
        cs, cbl = fnum(sel[0]["cs_nF"]), fnum(sel[0]["cbl_nF"])
        print("Destructive read, Cs %.2f nF, Cbl %.2f nF: predicted ratio Cs/(Cs+Cbl) = %.3f (strays lower it)"
              % (cs, cbl, cs / (cs + cbl)))
        for i, dv in enumerate(dvs):
            print("  read %d: dV = %+.1f mV%s" % (i + 1, dv * 1e3, ("   ratio to previous %.3f" % ratios[i - 1])
                                                if i > 0 else ""))
    return ratios


def fit_line(x, y):
    a = np.vstack([x, np.ones_like(x)]).T
    (m, b), *_ = np.linalg.lstsq(a, y, rcond=None)
    resid = y - (m * x + b)
    ss = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - float(np.sum(resid ** 2)) / ss if ss > 0 else 1.0
    return float(m), float(b), r2


def time_to_drop(t, v, dv, v_start):
    """First time the (lightly smoothed) curve is dv below v_start; linear interpolation, time measured from t[0]."""
    if len(v) < 3:
        return float("nan")
    k = 3
    vs = np.convolve(v, np.ones(k) / k, mode="valid")
    ts = t[1:-1] if len(t) >= 3 else t
    v0 = v_start
    idx = np.nonzero(vs <= v0 - dv)[0]
    if len(idx) == 0:
        return float("nan")
    i = idx[0]
    if i == 0:
        return float(ts[0] - t[0])
    f = (v0 - dv - vs[i - 1]) / (vs[i] - vs[i - 1])
    return float(ts[i - 1] + f * (ts[i] - ts[i - 1]) - t[0])


def analyze_decay(rows, c_pf, col="v_sn", window_mv=100.0, quiet=False):
    """Leakage from the initial slope (first `window_mv` of droop). For E2 rows, one result per cell."""
    results = {}
    cells = sorted(set(r.get("cell", "-") for r in rows if col in r and r.get("mode") in ("peek", "retention")))
    for cell in cells:
        sel = [r for r in rows if r.get("cell", "-") == cell and r.get("mode") in ("peek", "retention")]
        t = np.array([fnum(r["t_s"]) for r in sel])
        v = np.array([fnum(r[col]) for r in sel])
        ok = np.isfinite(t) & np.isfinite(v)
        t, v = t[ok], v[ok]
        if len(t) < 5:
            continue
        v0 = np.median(v[:5])
        win = v >= v0 - window_mv / 1e3
        # keep only the first contiguous stretch inside the window
        last = int(np.argmin(win)) if not win.all() else len(win)
        too_fast = last < 5
        last = max(last, 5)
        m, b, r2 = fit_line(t[:last], v[:last])
        i_leak = -m * c_pf * 1e-12
        v_start = m * t[0] + b          # start value from the fit, robust to noise
        t100 = time_to_drop(t, v, 0.100, v_start)
        t200 = time_to_drop(t, v, 0.200, v_start)
        results[cell] = dict(slope=m, i_leak=i_leak, r2=r2, t100=t100, t200=t200, v0=v0, too_fast=too_fast)
        if not quiet and too_fast:
            print("cell %-2s WARNING: fewer than 5 samples inside the first %g mV of droop; the cell decays faster "
                  "than you sample. Re-run with the firmware's 'fast' mode." % (cell, window_mv))
        if not quiet:
            print("cell %-2s start %.3f V  slope %+.3g mV/s  (R^2 %.3f)  -> leakage I = C*dV/dt = %.3g pA "
                  "(C = %g pF)  t(-100 mV) = %.4g s  t(-200 mV) = %.4g s"
                  % (cell, v0, m * 1e3, r2, i_leak * 1e12, c_pf, t100, t200))
    if not quiet and results:
        print("Note: in E2 the follower output tracks Vsn with gain ~1; use the 'transfer' calibration if not.")
    return results


def per_cell_retention(rows):
    sel = [r for r in rows if r.get("mode") == "retmap"]
    cells = {}
    for r in sel:
        key = (int(fnum(r["row"])), int(fnum(r["col"])))
        cells.setdefault(key, []).append((fnum(r["wait_s"]), int(fnum(r["read_bit"]))))
    waits_all = sorted(set(fnum(r["wait_s"]) for r in sel))
    out = {}
    for key, obs in cells.items():
        obs.sort()
        passes = [w for w, b in obs if b == 1]
        fails = [w for w, b in obs if b == 0]
        last_pass = max(passes) if passes else None
        first_fail = min([w for w in fails if last_pass is None or w > last_pass], default=None)
        if first_fail is None:
            out[key] = (waits_all[-1], "censored_high")
        elif last_pass is None:
            out[key] = (waits_all[0], "censored_low")
        else:
            out[key] = (math.sqrt(last_pass * first_fail), "ok")
    return out


def lognormal_tail(ret, rng, n_boot=4000):
    x = np.log(np.asarray(ret))
    mu, s = float(np.mean(x)), float(np.std(x, ddof=1))
    z4 = -3.719016
    q4 = math.exp(mu + z4 * s)
    boots = []
    n = len(x)
    for _ in range(n_boot):
        sample = rng.normal(mu, s, n)
        boots.append(math.exp(np.mean(sample) + z4 * np.std(sample, ddof=1)))
    lo, hi = np.percentile(boots, [5, 95])
    return mu, s, q4, float(lo), float(hi)


def analyze_retmap(rows, quiet=False, seed=7):
    cells = per_cell_retention(rows)
    if not cells:
        print("no retmap rows")
        return None
    vals = sorted(v for v, _ in cells.values())
    flags = [f for _, f in cells.values()]
    rng = np.random.default_rng(seed)
    mu, s, q4, lo, hi = lognormal_tail(vals, rng)
    ratio = vals[1] / vals[0] if len(vals) > 1 and vals[0] > 0 else float("nan")
    if not quiet:
        print("Per-cell retention (s), row x col:")
        for r in range(4):
            print("   " + "  ".join("%9.4g" % cells.get((r, c), (float("nan"), ""))[0] for c in range(4)))
        print("censored (never failed / failed at first wait): %d / %d of %d"
              % (flags.count("censored_high"), flags.count("censored_low"), len(flags)))
        print("median %.4g s, weakest %.4g s, 2nd weakest %.4g s, strongest %.4g s"
              % (math.exp(mu), vals[0], vals[1], vals[-1]))
        print("lognormal fit: sigma(ln t) = %.2f -> 1e-4 quantile %.4g s (90%% band %.4g-%.4g s, assumes the "
              "shape holds)" % (s, q4, lo, hi))
        print("ECC refresh extension (2nd weakest / weakest): %.2fx  [raw-ber-contract in miniature]" % ratio)
    return dict(median=math.exp(mu), sigma=s, weakest=vals[0], second=vals[1], ratio=ratio, q4=q4)


def analyze_temp(paths, quiet=False):
    pts = []
    for p in paths:
        rows = read_rows(p)
        temps = [fnum(r.get("temp_c")) for r in rows if np.isfinite(fnum(r.get("temp_c")))]
        if not temps:
            continue
        if any(r.get("mode") == "retmap" for r in rows):
            ret = float(np.median([v for v, _ in per_cell_retention(rows).values()]))
        else:
            ret = float(np.median([fnum(r.get("retention_s")) for r in rows if "retention_s" in r]))
        pts.append((float(np.mean(temps)), ret, p))
    if len(pts) < 2:
        print("need >= 2 files with temperatures")
        return None
    t_k = np.array([p[0] + 273.15 for p in pts])
    ln_r = np.log([p[1] for p in pts])
    m, b, r2 = fit_line(1.0 / (KB_EV * t_k), ln_r)     # ln t = b + Ea/(kT)
    ea = m
    dbl = (KB_EV * (295.15 ** 2) * math.log(2)) / ea if ea > 0 else float("nan")
    if not quiet:
        for tc, ret, p in pts:
            print("  %6.1f C  median retention %.4g s   (%s)" % (tc, ret, os.path.basename(p)))
        print("Arrhenius fit: Ea = %.3f eV (R^2 %.3f) -> retention halves every %.1f C near 22 C" % (ea, r2, dbl))
        print("Compare: silicon depletion generation ~0.6 eV (halves every ~9 C); diffusion ~1.1 eV (~4-5 C); "
              "Ea < 0.3 eV suggests surface/humidity or dielectric leakage, not the transistor.")
    return ea


def analyze_energy(rows, r_shunt=100.0, use_dmm=False, quiet=False):
    sel = [r for r in rows if r.get("mode") == "sweep"]
    labels = []
    for r in sel:
        if r["label"] not in labels:
            labels.append(r["label"])
    fits = {}
    for lab in labels:
        g = [r for r in sel if r["label"] == lab]
        f = np.array([fnum(r["f_hz"]) for r in g])
        if use_dmm:
            i = np.array([fnum(r["dmm_mV"]) / 1e3 / r_shunt for r in g])
        else:
            i = np.array([fnum(r["i_a"]) for r in g])
        v = np.array([fnum(r["v_eff"]) for r in g])
        ok = (f > 0) & np.isfinite(i)
        if ok.sum() < 2:
            continue
        m, b, r2 = fit_line(f[ok], i[ok])
        veff = float(np.mean(v[ok]))
        fits[lab] = dict(c_tot=m / veff, i0=b, r2=r2, v=veff, c_nom=fnum(g[0]["c_nom_pF"]) * 1e-12)
    base = fits.get("open", {}).get("c_tot", 0.0)
    if not quiet:
        print("E3: I = I0 + C*V*f.  Baseline (label 'open') C = %.1f pF is subtracted." % (base * 1e12))
        print("%-14s %9s %9s %10s %8s %12s %14s" % ("load", "C_tot pF", "C_load pF", "nominal pF", "R^2",
                                                    "meas/nominal", "E/cycle C*V^2"))
    out = {}
    for lab, d in fits.items():
        c_load = d["c_tot"] - base
        out[lab] = c_load
        ratio = c_load / d["c_nom"] if d["c_nom"] > 0 else float("nan")
        if not quiet:
            print("%-14s %9.1f %9.1f %10.1f %8.4f %12.3f %12.4g J" % (lab, d["c_tot"] * 1e12, c_load * 1e12,
                                                                      d["c_nom"] * 1e12, d["r2"], ratio,
                                                                      c_load * d["v"] ** 2))
    return out


def analyze_transfer(rows, quiet=False, v_on=0.05):
    """E2 calibration: per cell, fit Vout = gain * (Vwbl - Vth_eff) on the points where Vout > v_on."""
    sel = [r for r in rows if r.get("mode") == "transfer"]
    out = {}
    for cell in sorted(set(r["cell"] for r in sel)):
        g = [r for r in sel if r["cell"] == cell]
        x = np.array([fnum(r["v_wbl"]) for r in g])
        y = np.array([fnum(r["v_out"]) for r in g])
        ok = y > v_on
        if ok.sum() < 3:
            if not quiet:
                print("cell %s: output never rises above %.2f V: read FET Vth too high, or the switch never opens"
                      % (cell, v_on))
            continue
        m, b, r2 = fit_line(x[ok], y[ok])
        vth = -b / m if m != 0 else float("nan")
        out[cell] = dict(gain=m, vth=vth, r2=r2)
        if not quiet:
            print("cell %s: Vout = %.3f x (Vwbl - %.3f V)  (R^2 %.4f); storage-node voltage = %.3f + Vout / %.3f"
                  % (cell, m, vth, r2, vth, m))
    return out


def analyze_mlc(rows, quiet=False):
    sel = [r for r in rows if r.get("mode") == "mlc"]
    if not sel:
        print("no mlc rows")
        return None
    targets = sorted(set(fnum(r["target_v"]) for r in sel))
    th = [(targets[i] + targets[i + 1]) / 2 for i in range(len(targets) - 1)]

    def classify(v):
        return sum(1 for x in th if v > x)

    bins = [0, 1, 3, 10, 30, 100, 300, 1000, 3000]
    if not quiet:
        print("Levels %s V, thresholds %s V" % (", ".join("%.3f" % t for t in targets),
                                                ", ".join("%.3f" % t for t in th)))
        print("%12s %10s %8s" % ("hold (s)", "samples", "errors"))
    res = []
    for lo, hi in zip(bins[:-1], bins[1:]):
        g = [r for r in sel if lo <= fnum(r["t_s"]) < hi]
        if not g:
            continue
        err = sum(1 for r in g if classify(fnum(r["v_out"])) != int(fnum(r["level"])))
        res.append((lo, hi, len(g), err))
        if not quiet:
            print("%5g-%-6g %10d %8d  (%.2g)" % (lo, hi, len(g), err, err / len(g)))
    return res


# --------------------------------------------------------------------------------------------------------------
# Self-test on synthetic data
# --------------------------------------------------------------------------------------------------------------
def write_csv(path, header, rows, extra_lines=()):
    with open(path, "w") as f:
        f.write("# synthetic data\n")
        for x in extra_lines:
            f.write(x + "\n")
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")


def selftest():
    rng = np.random.default_rng(2026)
    d = tempfile.mkdtemp(prefix="t1_selftest_")
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + name)
        ok = ok and cond

    # hamming16 module (shared with the Pico)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import hamming16
    check("hamming16 corrects all single errors, detects all double errors", hamming16.self_check())

    # 1. charge sharing
    hdr = ["exp", "mode", "t_s", "temp_c", "cs_nF", "cbl_nF", "wait_s", "read_idx", "stored_bit", "v_pre",
           "v_after", "dv", "sa_bit", "adc_bit", "v_ref"]
    rows = []
    cx_true = 0.030  # nF
    for cbl in (1.0, 2.2, 4.7, 10.0, 22.0):
        for bit in (1, 0):
            for k in range(10):
                vpre = 1.65 + rng.normal(0, 0.003)
                dv = share_model(3.3 if bit else 0.0, vpre, 1.0, cbl + cx_true) + rng.normal(0, 0.002)
                rows.append(["E1A", "share", k, 22.0, 1.0, cbl, 0, k, bit, vpre, vpre + dv, dv, bit, bit, 1.65])
    p = os.path.join(d, "share.csv")
    write_csv(p, hdr, rows, extra_lines=["Cbl fitted now in nF (blank = stop): 4.7, prompt echo with, commas"])
    cx, _ = analyze_share(read_rows(p), quiet=True)
    check("share: fitted stray %.1f pF (true 30)" % cx, abs(cx - 30.0) < 10.0)

    # 2. destructive
    rows = []
    v = 3.3
    for k in range(4):
        dv = share_model(v, 1.65, 1.0, 4.73)
        rows.append(["E1A", "destructive", k, 22.0, 1.0, 4.7, 0, k, 1, 1.65, 1.65 + dv, dv, 1, 1, 1.65])
        v = 1.65 + dv
    p = os.path.join(d, "destr.csv")
    write_csv(p, hdr, rows)
    ratios = analyze_destructive(read_rows(p), quiet=True)
    check("destructive: ratio %.3f = Cs/(Cs+Cbl) 0.175" % ratios[0], abs(ratios[0] - 1.0 / 5.73) < 0.005)

    # 3. decay (E2 long format, three cells)
    hdr2 = ["exp", "mode", "t_s", "temp_c", "label", "cell", "v_out"]
    rows = []
    c_pf = 110.0
    leaks = {"A": 0.5e-12, "B": 0.1e-12, "C": 0.02e-12}
    for i in range(1200):
        t = i * 1.0
        for cell, il in leaks.items():
            vv = 1.10 - il / (c_pf * 1e-12) * t + rng.normal(0, 0.0005)
            rows.append(["E2", "retention", t, 22.0, "synthetic", cell, max(vv, 0.0)])
    p = os.path.join(d, "decay.csv")
    write_csv(p, hdr2, rows)
    res = analyze_decay(read_rows(p), c_pf, col="v_out", quiet=True)
    for cell, il in leaks.items():
        got = res[cell]["i_leak"]
        check("decay cell %s: leakage %.3g pA (true %.3g)" % (cell, got * 1e12, il * 1e12), abs(got / il - 1) < 0.1)
    t100 = res["A"]["t100"]
    t100_true = 0.1 * c_pf * 1e-12 / leaks["A"]
    check("decay: t(-100 mV) %.1f s (true %.1f)" % (t100, t100_true), abs(t100 - t100_true) < 3.0)
    # a cell that decays faster than the sample rate must be flagged, not silently mis-measured
    rows_fast = [["E2", "retention", float(i), 22.0, "syn", "F", max(1.1 - 0.45 * i, 0.0)] for i in range(30)]
    p2 = os.path.join(d, "decay_fast.csv")
    write_csv(p2, hdr2, rows_fast)
    check("decay: too-fast cell is flagged", analyze_decay(read_rows(p2), c_pf, col="v_out", quiet=True)["F"]["too_fast"])

    # 4. retention map (16 cells lognormal)
    hdr3 = ["exp", "mode", "t_s", "temp_c", "wait_s", "row", "col", "stored_bit", "read_bit"]
    true_ret = np.exp(rng.normal(math.log(100.0), 0.5, 16))
    waits = [round(1.0 * 10 ** (k / 8), 3) for k in range(0, 33)]   # 1 .. 10000 s, 8 per decade
    rows = []
    for w in waits:
        for i in range(16):
            rows.append(["E1B", "retmap", 0, 22.0, w, i // 4, i % 4, 1, 1 if true_ret[i] > w else 0])
    p = os.path.join(d, "retmap.csv")
    write_csv(p, hdr3, rows)
    rm = analyze_retmap(read_rows(p), quiet=True)
    true_sorted = np.sort(true_ret)
    check("retmap: median %.1f s (true %.1f)" % (rm["median"], float(np.exp(np.mean(np.log(true_ret))))),
          abs(math.log(rm["median"] / float(np.exp(np.mean(np.log(true_ret)))))) < 0.15)
    check("retmap: weakest %.1f s (true %.1f)" % (rm["weakest"], true_sorted[0]),
          abs(math.log(rm["weakest"] / true_sorted[0])) < 0.2)

    # 5. temperature (three files)
    paths = []
    ea_true = 0.6
    for tc in (4.0, 22.0, 45.0):
        tk = tc + 273.15
        med = 100.0 * math.exp(ea_true / KB_EV * (1 / tk - 1 / 295.15))
        rr = []
        ret = med * np.exp(rng.normal(0, 0.3, 16))
        for w in [round(0.1 * 10 ** (k / 10), 4) for k in range(0, 51)]:
            for i in range(16):
                rr.append(["E1B", "retmap", 0, tc + rng.normal(0, 0.2), w, i // 4, i % 4, 1, 1 if ret[i] > w else 0])
        pp = os.path.join(d, "temp_%d.csv" % int(tc))
        write_csv(pp, hdr3, rr)
        paths.append(pp)
    ea = analyze_temp(paths, quiet=True)
    check("temp: Ea %.3f eV (true 0.6)" % ea, abs(ea - ea_true) < 0.12)

    # 6. energy
    hdr4 = ["exp", "mode", "label", "c_nom_pF", "f_hz", "v_shunt", "i_a", "v_eff", "dmm_mV"]
    rows = []
    internal = 15e-12
    for lab, c in (("open", 0.0), ("100pF", 100e-12), ("1m_RG58", 101e-12), ("3m_RG58", 303e-12),
                   ("1nF", 1e-9)):
        for f in (0, 100e3, 250e3, 500e3, 1e6):
            if lab == "1nF" and f > 250e3:
                continue
            i = 0.2e-3 + (c + internal) * 3.25 * f + rng.normal(0, 0.5e-6)
            rows.append(["E3", "sweep", lab, c * 1e12, f, i * 100, i, 3.25, ""])
    p = os.path.join(d, "energy.csv")
    write_csv(p, hdr4, rows)
    en = analyze_energy(read_rows(p), quiet=True)
    for lab, c in (("100pF", 100e-12), ("3m_RG58", 303e-12), ("1nF", 1e-9)):
        check("energy: %s C_load %.1f pF (true %.1f)" % (lab, en[lab] * 1e12, c * 1e12), abs(en[lab] - c) < 5e-12)

    # 7. MLC
    hdr5 = ["exp", "mode", "label", "t_s", "trial", "level", "target_v", "v_out"]
    rows = []
    targets = (0.15, 0.45, 0.75, 1.05)
    for trial in range(3):
        for lev, tv in enumerate(targets):
            for t in range(0, 300, 2):
                rows.append(["E2", "mlc", "syn", t, trial, lev, tv, tv - 0.0006 * t + rng.normal(0, 0.002)])
    p = os.path.join(d, "mlc.csv")
    write_csv(p, hdr5, rows)
    res = analyze_mlc(read_rows(p), quiet=True)
    early = [e for lo, hi, n, e in res if hi <= 100]
    late = [e for lo, hi, n, e in res if lo >= 300 or (lo >= 100 and hi <= 300)]
    check("mlc: no errors before 100 s, errors once drift > half-spacing (150 mV at 250 s)",
          sum(early) == 0 and sum(late) > 0)

    # 8. transfer calibration
    hdr6 = ["exp", "mode", "label", "v_wbl", "cell", "v_out"]
    rows = []
    for cell, vth, gain in (("A", 2.05, 0.97), ("B", 1.80, 0.98)):
        for k in range(67):
            vw = 0.05 * k
            rows.append(["E2", "transfer", "syn", vw, cell, max(gain * (vw - vth), 0.0) + rng.normal(0, 0.001)])
    p = os.path.join(d, "transfer.csv")
    write_csv(p, hdr6, rows)
    tr = analyze_transfer(read_rows(p), quiet=True)
    check("transfer: cell A Vth %.3f V gain %.3f (true 2.05 / 0.97)" % (tr["A"]["vth"], tr["A"]["gain"]),
          abs(tr["A"]["vth"] - 2.05) < 0.03 and abs(tr["A"]["gain"] - 0.97) < 0.02)

    print("SELFTEST " + ("PASSED" if ok else "FAILED") + "  (scratch files in %s)" % d)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Analyze T1 bench logs (E1, E2, E3).")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("share"); s.add_argument("csv"); s.add_argument("--v-write", type=float, default=3.3)
    s = sub.add_parser("destructive"); s.add_argument("csv")
    s = sub.add_parser("decay"); s.add_argument("csv"); s.add_argument("--c-pf", type=float, required=True)
    s.add_argument("--col", default="v_sn"); s.add_argument("--window-mv", type=float, default=100.0)
    s = sub.add_parser("retmap"); s.add_argument("csv")
    s = sub.add_parser("temp"); s.add_argument("csv", nargs="+")
    s = sub.add_parser("energy"); s.add_argument("csv"); s.add_argument("--r-shunt", type=float, default=100.0)
    s.add_argument("--use-dmm", action="store_true")
    s = sub.add_parser("mlc"); s.add_argument("csv")
    s = sub.add_parser("transfer"); s.add_argument("csv")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.cmd == "share":
        analyze_share(read_rows(args.csv), v_write=args.v_write)
    elif args.cmd == "destructive":
        analyze_destructive(read_rows(args.csv))
    elif args.cmd == "decay":
        analyze_decay(read_rows(args.csv), args.c_pf, col=args.col, window_mv=args.window_mv)
    elif args.cmd == "retmap":
        analyze_retmap(read_rows(args.csv))
    elif args.cmd == "temp":
        analyze_temp(args.csv)
    elif args.cmd == "energy":
        analyze_energy(read_rows(args.csv), r_shunt=args.r_shunt, use_dmm=args.use_dmm)
    elif args.cmd == "mlc":
        analyze_mlc(read_rows(args.csv))
    elif args.cmd == "transfer":
        analyze_transfer(read_rows(args.csv))
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
