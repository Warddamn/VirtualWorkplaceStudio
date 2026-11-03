#!/usr/bin/env python3
"""
analyze_t1.py -- turn the CSV logs from the T1 Pico scripts into the numbers each guide asks for.

Runs on a PC with Python 3 + numpy (no scipy, no matplotlib). Written 2026-11-03 for the DRAM Moonshot home lab.

    python3 analyze_t1.py --selftest                 # synthetic data for every analysis; exit 0 on pass
    python3 analyze_t1.py share e1_share.csv         # E1 charge sharing: measured vs predicted dV, fitted strays
    python3 analyze_t1.py destructive e1_destr.csv   # E1 destructive read: signal ratio per read
    python3 analyze_t1.py decay e1_peek.csv --c-pf 1000            # leakage from a decay curve (E1 peek)
    python3 analyze_t1.py decay e2_ret.csv --c-pf 230 --col v_out  # E2: one result per cell
    python3 analyze_t1.py decay e2_ret.csv --c-pf 230 --col v_out --drop-mv 550   # + 1-bit hold time
    python3 analyze_t1.py float e1_float.csv         # E1: leakage on the floating bitline (GPIOs, comparator)
    python3 analyze_t1.py retmap e1_retmap.csv       # E1 16-cell retention distribution, tails, ECC gain
    python3 analyze_t1.py ecc e1_ecc.csv             # E1: ECC refresh extension (decoder limit / first raw error)
    python3 analyze_t1.py temp cold.csv room.csv warm.csv          # E1 retmap files: retention vs temperature -> Ea
    python3 analyze_t1.py temp --decay --c-pf 230 --col v_out c.csv r.csv w.csv   # E2: leakage vs T -> Ea per cell
    python3 analyze_t1.py kick e2_ret.csv            # E2: gate kick and WBL-park step per cell
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


def analyze_decay(rows, c_pf, col="v_sn", window_mv=100.0, drop_mv=None, quiet=False):
    """Leakage from the initial slope (first `window_mv` of droop). For E2 rows, one result per cell.
    drop_mv: also report the time to fall that far (e.g. 550 = the 1-bit hold time in E2)."""
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
        tx = time_to_drop(t, v, drop_mv / 1e3, v_start) if drop_mv else float("nan")
        results[cell] = dict(slope=m, i_leak=i_leak, r2=r2, t100=t100, t200=t200, tx=tx, v0=v0,
                             too_fast=too_fast, started_low=False)
    # A cell that already lost its charge before the first sample shows a flat line near 0 V: that is the
    # LEAKIEST cell, not the best one. Flag cells that start far below the others.
    v0_max = max((r["v0"] for r in results.values()), default=0.0)
    for cell, r in results.items():
        if len(results) > 1 and v0_max > 0.2 and r["v0"] < 0.5 * v0_max:
            r["started_low"] = True
    if not quiet:
        for cell, r in sorted(results.items()):
            if r["started_low"]:
                print("cell %-2s WARNING: starts at %.2f V, far below the other cells (%.2f V): it lost its charge "
                      "before the first sample. Its leakage is above ~C x 0.1 V / 0.1 s = %.3g pA ('retention' mode "
                      "samples first ~0.1 s after switch-off). Use 'fast' mode; do not read its flat line as low "
                      "leakage." % (cell, r["v0"], v0_max, c_pf * 1e-12 * 0.1 / 0.1 * 1e12))
            elif r["too_fast"]:
                print("cell %-2s WARNING: fewer than 5 samples inside the first %g mV of droop; the cell decays faster "
                      "than you sample. Re-run with the firmware's 'fast' mode." % (cell, window_mv))
            extra = ("  t(-%g mV) = %.4g s" % (drop_mv, r["tx"])) if drop_mv else ""
            print("cell %-2s start %.3f V  slope %+.3g mV/s  (R^2 %.3f)  -> leakage I = C*dV/dt = %.3g pA "
                  "(C = %g pF)  t(-100 mV) = %.4g s  t(-200 mV) = %.4g s%s"
                  % (cell, r["v0"], r["slope"] * 1e3, r["r2"], r["i_leak"] * 1e12, c_pf, r["t100"], r["t200"], extra))
        if results:
            print("Note: in E2 the follower output tracks Vsn with gain ~1; use the 'transfer' calibration if not. "
                  "'nan' times mean the curve never fell that far: the run was too short.")
    return results


def analyze_float(rows, quiet=False):
    """E1 float test: drift of the floating bitline (wordline closed) -> leakage = Cbl * drift / dt."""
    sel = [r for r in rows if r.get("mode") == "float"]
    if not sel:
        print("no float rows")
        return None
    dv = np.array([fnum(r["dv"]) for r in sel])
    dt = np.array([fnum(r["wait_s"]) for r in sel])
    cbl = fnum(sel[0]["cbl_nF"]) * 1e-9
    drift = float(np.mean(dv))
    i_leak = cbl * drift / float(np.mean(dt))
    if not quiet:
        print("Float test (%d repeats): drift %+.3f mV (sd %.3f mV) in %.2f ms -> bitline leakage %+.3g nA "
              "(Cbl %.3g nF). Pass: |drift| < 0.5 mV. %s"
              % (len(sel), drift * 1e3, float(np.std(dv)) * 1e3, float(np.mean(dt)) * 1e3, i_leak * 1e9, cbl * 1e9,
                 "PASS" if abs(drift) < 0.5e-3 else "FAIL: check GPIO pulls, the comparator input and the follower"))
    return dict(drift=drift, i_leak=i_leak)


def analyze_kick(rows, quiet=False):
    """E2: gate kick = Vout 2 ms after switch-off (WBL still at the write level) - Vout with the switch on;
    park step = Vout after WBL parks - Vout before it parks (only in 'retention' logs, which wait for WBL)."""
    out = {}
    for cell in sorted(set(r.get("cell") for r in rows if r.get("mode", "").startswith("kick_"))):
        def med(mode):
            v = [fnum(r["v_out"]) for r in rows if r.get("cell") == cell and r.get("mode") == mode]
            return float(np.median(v)) if v else float("nan")
        b, a, p = med("kick_before"), med("kick_after"), med("kick_park")
        out[cell] = dict(gate_mV=(a - b) * 1e3, park_mV=(p - a) * 1e3)
        if not quiet:
            print("cell %-2s Vout on %.3f V -> off %.3f V: gate kick %+.1f mV%s" % (
                cell, b, a, (a - b) * 1e3,
                ("; WBL park step %+.1f mV (Vout %.3f V)" % ((p - a) * 1e3, p)) if p == p else ""))
    if not quiet:
        if out:
            print("Compare with E2 section 2.4 (follower gain ~0.98). Negative = the node was pushed down.")
        else:
            print("no kick rows (they come from 'retention' and 'fast' runs of the updated firmware)")
    return out


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


def transition(obs):
    """obs = [(wait, failed)]. Threshold = geometric mean of the last passing wait and the first failing wait
    above it (the same rule per_cell_retention uses)."""
    passes = [w for w, f in obs if not f]
    fails = [w for w, f in obs if f]
    last_pass = max(passes) if passes else None
    first_fail = min([w for w in fails if last_pass is None or w > last_pass], default=None)
    if first_fail is None:
        return float("nan")
    if last_pass is None:
        return first_fail
    return math.sqrt(last_pass * first_fail)


def analyze_ecc(rows, quiet=False):
    """E1 ECC demo: first raw error vs the point where the decoder can no longer fix the word."""
    sel = [r for r in rows if r.get("mode") == "ecc"]
    if not sel:
        print("no ecc rows")
        return None
    w = [fnum(r["wait_s"]) for r in sel]
    raw = [fnum(r["raw_errors"]) >= 1 for r in sel]
    bad = [int(fnum(r["status"])) == 2 or int(fnum(r["data_ok"])) == 0 for r in sel]
    t_raw = transition(list(zip(w, raw)))
    t_bad = transition(list(zip(w, bad)))
    ratio = t_bad / t_raw if t_raw > 0 else float("nan")
    if not quiet:
        print("ECC demo: first raw error at ~%.4g s; decoder gives up (status 2 or wrong data) at ~%.4g s"
              % (t_raw, t_bad))
        print("ECC refresh extension = %.2fx (E1 section 2.7 expects ~1.1-1.4x for 16 lognormal cells)" % ratio)
        ws = sorted(set(w))
        steps = [y / x - 1 for x, y in zip(ws, ws[1:]) if x > 0]
        if any(r for wi, r in zip(w, raw) if wi == ws[0]):
            print("WARNING: raw errors already at the shortest wait (%.3g s): lower RET_MIN_S and repeat" % ws[0])
        print("Waits tested: %d, finest step %.1f%% (the fine pass uses 5%%; if the finest step is ~78%%, the fine "
              "pass did not run and the ratio is not resolved)" % (len(ws), 100 * min(steps) if steps else float("nan")))
    return dict(t_raw=t_raw, t_bad=t_bad, ratio=ratio)


def analyze_temp_decay(paths, c_pf, col="v_out", quiet=False):
    """E2: leakage per cell from each file's decay, then ln(I) vs 1/kT per cell -> Ea."""
    per_cell = {}
    temps = []
    for p in paths:
        rows = read_rows(p)
        tc = [fnum(r.get("temp_c")) for r in rows if np.isfinite(fnum(r.get("temp_c")))]
        if not tc:
            print("%s: no temperature readings; skipped" % os.path.basename(p))
            continue
        t_mean = float(np.mean(tc))
        temps.append(t_mean)
        for cell, r in analyze_decay(rows, c_pf, col=col, quiet=True).items():
            if r["i_leak"] > 0 and not r["started_low"] and not r["too_fast"]:
                per_cell.setdefault(cell, []).append((t_mean, r["i_leak"], os.path.basename(p)))
    out = {}
    for cell, pts in sorted(per_cell.items()):
        if len(pts) < 2:
            if not quiet:
                print("cell %s: fewer than 2 usable temperatures" % cell)
            continue
        x = np.array([1.0 / (KB_EV * (tc + 273.15)) for tc, _, _ in pts])
        y = np.log([i for _, i, _ in pts])
        m, b, r2 = fit_line(x, y)        # ln I = b - Ea/(kT)
        ea = -m
        out[cell] = ea
        if not quiet:
            for tc, i, name in pts:
                print("  cell %s %6.1f C  leakage %.3g pA  (%s)" % (cell, tc, i * 1e12, name))
            print("cell %s: Ea = %.3f eV (R^2 %.3f): leakage doubles every %.1f C near 22 C"
                  % (cell, ea, r2, (KB_EV * 295.15 ** 2 * math.log(2)) / ea if ea > 0 else float("nan")))
    if not quiet and out:
        print("Compare: silicon depletion generation ~0.6 eV; Ea < 0.3 eV suggests surface, humidity or "
              "dielectric leakage, not the switch.")
    return out


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
            vals = [fnum(r.get("retention_s")) for r in rows if "retention_s" in r]
            ret = float(np.median(vals)) if vals else float("nan")
        if not (np.isfinite(ret) and ret > 0):
            print("%s: no retention values (this command reads E1 'retmap' files; for E2 decay files use "
                  "'temp --decay --c-pf 230 --col v_out')" % os.path.basename(p))
            return None
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


def log_schedule(t_min_s, t_max_s, per_decade=4):
    """Copy of t1_common.log_schedule (the firmware's coarse waits)."""
    out, k = [], 0
    while True:
        t = t_min_s * 10 ** (k / per_decade)
        if t > t_max_s * 1.0001:
            break
        out.append(round(t, 3))
        k += 1
    return out


def sim_retmap(true_ret, ret_min=1.0, ret_max=3600.0, fine_step=1.05, stop_cells=16, fine=True):
    """Replica of e1_array_4x4.mode_retmap's schedule (coarse 4 per decade, then 5% steps) on ideal cells."""
    rows = []

    def once(w):
        got = [1 if r > w else 0 for r in true_ret]
        for i in range(16):
            rows.append(["E1B", "retmap", 0, 22.0, w, i // 4, i % 4, 1, got[i]])
        return 16 - sum(got)

    first_fail = all_fail = None
    for w in log_schedule(ret_min, ret_max, 4):
        n = once(w)
        if n and first_fail is None:
            first_fail = w
        if n == 16:
            all_fail = w
            break
    if first_fail is None or not fine:
        return rows
    w = first_fail / 10 ** 0.25
    w_end = min(ret_max, all_fail * 1.2) if all_fail else ret_max
    while True:
        w = round(w * fine_step, 3)
        if w > w_end:
            break
        if once(w) >= stop_cells:
            break
    return rows


def sim_ecc(true_ret, hamming16, data=0x7FF, ret_min=1.0, ret_max=3600.0, fine_step=1.05):
    """Replica of e1_array_4x4.mode_ecc on ideal cells: a stored 1 reads 0 once the wait exceeds its retention."""
    cw = hamming16.encode(data)
    rows = []

    def once(w):
        got = [0 if (cw[i] == 1 and true_ret[i] <= w) else cw[i] for i in range(16)]
        d, status, pos = hamming16.decode(got)
        raw = sum(1 for i in range(16) if got[i] != cw[i])
        ok = 1 if d == data else 0
        rows.append(["E1B", "ecc", 0, 22.0, w, raw, status, pos, ok])
        return raw, (status == hamming16.DETECTED or not ok)

    first_raw = first_bad = None
    for w in log_schedule(ret_min, ret_max, 4):
        raw, bad = once(w)
        if raw and first_raw is None:
            first_raw = w
        if bad:
            first_bad = w
            break
    if first_raw is None:
        return rows
    w = first_raw / 10 ** 0.25
    w_end = min(ret_max, first_bad * 1.2) if first_bad else ret_max
    while True:
        w = round(w * fine_step, 3)
        if w > w_end:
            break
        if once(w)[1]:
            break
    return rows


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
    # a cell that is already empty at the first sample must be flagged, not reported as 'low leakage'
    rows_low = [r for r in rows if r[5] != "C"] + [["E2", "retention", i * 1.0, 22.0, "syn", "C",
                                                     0.03 + rng.normal(0, 0.0005)] for i in range(200)]
    p3 = os.path.join(d, "decay_low.csv")
    write_csv(p3, hdr2, rows_low)
    rl = analyze_decay(read_rows(p3), c_pf, col="v_out", quiet=True)
    check("decay: cell that starts empty is flagged (and full cells are not)",
          rl["C"]["started_low"] and not rl["A"]["started_low"])
    tx = analyze_decay(read_rows(p), c_pf, col="v_out", drop_mv=550, quiet=True)["A"]["tx"]
    check("decay --drop-mv 550: %.1f s (true %.1f)" % (tx, 0.55 * c_pf * 1e-12 / leaks["A"]),
          abs(tx / (0.55 * c_pf * 1e-12 / leaks["A"]) - 1) < 0.03)

    # 4. retention map (16 cells lognormal), using the firmware's own schedule (coarse 4/decade + fine 5%)
    hdr3 = ["exp", "mode", "t_s", "temp_c", "wait_s", "row", "col", "stored_bit", "read_bit"]
    true_ret = np.exp(rng.normal(math.log(100.0), 0.5, 16))
    rows = sim_retmap(true_ret)
    p = os.path.join(d, "retmap.csv")
    write_csv(p, hdr3, rows)
    rm = analyze_retmap(read_rows(p), quiet=True)
    true_sorted = np.sort(true_ret)
    check("retmap: median %.1f s (true %.1f)" % (rm["median"], float(np.exp(np.mean(np.log(true_ret))))),
          abs(math.log(rm["median"] / float(np.exp(np.mean(np.log(true_ret)))))) < 0.15)
    check("retmap: weakest %.1f s (true %.1f)" % (rm["weakest"], true_sorted[0]),
          abs(math.log(rm["weakest"] / true_sorted[0])) < 0.06)

    # 4b. can the firmware schedule resolve the ECC gain (2nd weakest / weakest, expected 1.1-1.4x)?
    for sig in (0.3, 0.5):
        meas_f, meas_c, true_r = [], [], []
        for _ in range(300):
            tr = np.exp(rng.normal(math.log(100.0), sig, 16))
            ts = np.sort(tr)
            true_r.append(ts[1] / ts[0])
            for fine, store in ((True, meas_f), (False, meas_c)):
                vals = sorted(v for v, _ in per_cell_retention(
                    [dict(zip(hdr3, map(str, r))) for r in sim_retmap(tr, fine=fine)]).values())
                store.append(vals[1] / vals[0])
        mf, mc, mt = float(np.median(meas_f)), float(np.median(meas_c)), float(np.median(true_r))
        check("retmap sigma %.1f: ECC gain with the fine pass %.3f vs true %.3f (coarse 1.78x steps alone: %.3f)"
              % (sig, mf, mt, mc), abs(mf - mt) < 0.04)

    # 4c. the ECC mode itself (codeword of 16 ones, decoder from hamming16)
    hdr_e = ["exp", "mode", "t_s", "temp_c", "wait_s", "raw_errors", "status", "corrected_pos", "data_ok"]
    tr = np.exp(rng.normal(math.log(100.0), 0.4, 16))
    p = os.path.join(d, "ecc.csv")
    write_csv(p, hdr_e, sim_ecc(tr, hamming16))
    ec = analyze_ecc(read_rows(p), quiet=True)
    ts = np.sort(tr)
    check("ecc: extension %.3f (true 2nd/1st %.3f)" % (ec["ratio"], ts[1] / ts[0]),
          abs(ec["ratio"] / (ts[1] / ts[0]) - 1) < 0.06)

    # 4d. float test and kick rows
    rows = [["E1A", "float", k, 22.0, 1.0, 4.7, 0.0055, k, -1, 1.65, 1.65 + 0.0002 + rng.normal(0, 0.00005),
             0, -1, -1, 1.65] for k in range(20)]
    for r in rows:
        r[11] = r[10] - r[9]
    p = os.path.join(d, "float.csv")
    write_csv(p, hdr, rows)
    fl = analyze_float(read_rows(p), quiet=True)
    check("float: leakage %.3g nA (true %.3g)" % (fl["i_leak"] * 1e9, 4.7e-9 * 0.0002 / 0.0055 * 1e9),
          abs(fl["i_leak"] / (4.7e-9 * 0.0002 / 0.0055) - 1) < 0.1)
    rows = []
    for cell, kg, kp in (("A", -0.191, -0.150), ("B", -0.039, -0.010)):
        for mode, v in (("kick_before", 1.10), ("kick_after", 1.10 + kg), ("kick_park", 1.10 + kg + kp)):
            rows.append(["E2", mode, 0, 22.0, "syn", cell, v + rng.normal(0, 0.0005)])
    p = os.path.join(d, "kick.csv")
    write_csv(p, ["exp", "mode", "t_s", "temp_c", "label", "cell", "v_out"], rows)
    kk = analyze_kick(read_rows(p), quiet=True)
    check("kick: cell A gate %.0f mV (true -191), park %.0f mV (true -150)" % (kk["A"]["gate_mV"], kk["A"]["park_mV"]),
          abs(kk["A"]["gate_mV"] + 191) < 5 and abs(kk["A"]["park_mV"] + 150) < 5)

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
    # E2 files: 'temp' alone must refuse (no silent NaN); 'temp --decay' fits Ea per cell
    paths2 = []
    for tc in (4.0, 22.0, 45.0):
        tk = tc + 273.15
        rr = []
        for i in range(600):
            for cell, i22 in (("A", 0.5e-12), ("B", 0.1e-12)):
                il = i22 * math.exp(-ea_true / KB_EV * (1 / tk - 1 / 295.15))
                rr.append(["E2", "retention", i * 1.0, tc + rng.normal(0, 0.1), "syn", cell,
                           1.10 - il / (230e-12) * i + rng.normal(0, 0.0003)])
        pp = os.path.join(d, "e2temp_%d.csv" % int(tc))
        write_csv(pp, hdr2, rr)
        paths2.append(pp)
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        refused = analyze_temp(paths2, quiet=True) is None
    check("temp on E2 decay files refuses instead of printing NaN", refused)
    ed = analyze_temp_decay(paths2, 230.0, col="v_out", quiet=True)
    check("temp --decay: Ea A %.3f, B %.3f eV (true 0.6)" % (ed["A"], ed["B"]),
          abs(ed["A"] - ea_true) < 0.05 and abs(ed["B"] - ea_true) < 0.08)

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
    s.add_argument("--drop-mv", type=float, default=None, help="also report t(-X mV), e.g. 550 = E2 1-bit hold")
    s = sub.add_parser("float"); s.add_argument("csv")
    s = sub.add_parser("retmap"); s.add_argument("csv")
    s = sub.add_parser("ecc"); s.add_argument("csv")
    s = sub.add_parser("kick"); s.add_argument("csv")
    s = sub.add_parser("temp"); s.add_argument("csv", nargs="+")
    s.add_argument("--decay", action="store_true", help="E2 decay files: fit leakage vs T per cell")
    s.add_argument("--c-pf", type=float, default=230.0); s.add_argument("--col", default="v_out")
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
        analyze_decay(read_rows(args.csv), args.c_pf, col=args.col, window_mv=args.window_mv, drop_mv=args.drop_mv)
    elif args.cmd == "float":
        analyze_float(read_rows(args.csv))
    elif args.cmd == "retmap":
        analyze_retmap(read_rows(args.csv))
    elif args.cmd == "ecc":
        analyze_ecc(read_rows(args.csv))
    elif args.cmd == "kick":
        analyze_kick(read_rows(args.csv))
    elif args.cmd == "temp":
        if args.decay:
            analyze_temp_decay(args.csv, args.c_pf, col=args.col)
        else:
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
