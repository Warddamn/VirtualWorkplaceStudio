#!/usr/bin/env python3
"""
leakage_tail.py -- analysis for home-lab experiment E4, "The DRAM cell is an electrometer".

What it does
------------
You measure transistor off-leakage with the charge-decay method: a storage node (the
transistor's drain + a small film capacitor + an electrometer op-amp input) is charged,
the transistor is turned off, and the node voltage is logged while leakage drains it.
The physics is one line, charge conservation on an isolated node:

        I_leak = -C_node * dV/dt

This script turns a CSV of (device, temperature, time, voltage) logs into:
  1. a robust slope (Theil-Sen) and an ordinary least-squares slope with its standard error,
     per device and temperature, then a leakage current;
  2. blank subtraction (a run with no device = the bench's own floor, mostly op-amp bias current);
  3. the leakage DISTRIBUTION at each temperature: empirical quantiles with two kinds of
     95% confidence interval (distribution-free order-statistic CI and bootstrap CI), a
     lognormal fit, and a lognormality check (probability-plot correlation);
  4. an Arrhenius activation energy Ea per device (from 3-4 temperatures) and its spread;
  5. the sample-size arithmetic for tail quantiles (why a 1e-4 quantile needs ~3e4-1e5 devices).

It is a rehearsal of the dram-moonshot study's "Oxide Tail Spec" statistics: same method and
the same statistics, on cheap silicon MOSFETs instead of 0.01 um^2 oxide transistors.

Input CSV
---------
Required columns (header names are case-insensitive; aliases accepted):
    device        any string; use "BLANK" (or --blank-name) for the no-device floor run
    temperature   setpoint or measured block temperature, deg C   (alias: temperature_C, temp_C)
    time          seconds since the transistor was turned off       (alias: time_s, t)
    voltage       node voltage in volts                             (alias: voltage_V, v)
Optional columns:
    run           repeat index if one device is measured more than once at one temperature
    cap_pf        node capacitance for that row in pF (the firmware writes CAP_PF here).
                  --cap-pf, when given, OVERRIDES this column for every record.
    temp_meas_C   logged block temperature for that row (used with --cap-tempco-ppm)

Valid-range rule (why a "quiet" trace can mean a LEAKY device)
----------------------------------------------------------------
The buffer is linear only between ~0.45 V and the ADS1115 full scale (2.048 V). A node that
leaves that window, or falls more than 0.5 V, is no longer measuring the current. Each record
is therefore cut at its first out-of-range point:
    ok         never left the window: normal fit
    truncated  left the window, but >= 30 in-range points remain after --skip-s: fit those
    drained    fewer than 30 points remain: the device leaked MORE than the node could hold.
               Its current is reported as a LOWER BOUND, I_lb = C * (V_start - V_limit) / t_out,
               and it is never called "below floor" (right-censored: at least this leaky)
    invalid    the node was already outside the window at the first sample (e.g. a BLANK
               whose node was never written): the record is dropped with a warning

Usage
-----
    python3 leakage_tail.py --selftest [--workdir DIR]        # synthetic data, checks recovery
    python3 leakage_tail.py --expected                       # first-principles numbers for E4
    python3 leakage_tail.py --csv my_log.csv --skip-s 60 [--json out.json]
    python3 leakage_tail.py --csv my_log.csv --cap-pf 10230  # override the cap_pf column
    python3 leakage_tail.py --plan 2e-13 --window-s 600      # pick a capacitor for a current
    python3 leakage_tail.py --plan 1e-10 --cap-pf 47000      # longest window for this C

Dependencies: Python 3.9+ standard library + numpy. No scipy, no matplotlib.
Author: dram-moonshot home-lab track T2. Written 2026-11-03. Exit code 0 = success.
"""

import argparse
import csv
import json
import math
import os
import sys
import tempfile
from statistics import NormalDist

import numpy as np

KB_EV = 8.617333262e-5          # Boltzmann constant, eV/K
KB_J = 1.380649e-23             # Boltzmann constant, J/K
Q_E = 1.602176634e-19           # elementary charge, C
ZERO_C = 273.15

# Valid node window (must match V_MIN / V_MAX / DROOP_MAX_V in e4_pico_leakage_bench.py)
V_LO = 0.45                     # below this the single-supply buffer is near its output rail
V_HI = 2.04                     # ADS1115 +/-2.048 V full scale clips at 2.0479 V
DROOP_MAX = 0.50                # leakage depends on bias: stop trusting the slope after 0.5 V
N_MIN_FIT = 30                  # fewer in-range points than this -> "drained" (lower bound)
DROOP_BELOW_FLOOR = 0.30        # a run may be called "below floor" only if it drooped < 0.3 V

# ---------------------------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------------------------
ALIASES = {
    "device": ("device", "dut", "device_id"),
    "temperature": ("temperature", "temperature_c", "temp_c", "temp", "t_c"),
    "time": ("time", "time_s", "t", "seconds"),
    "voltage": ("voltage", "voltage_v", "v", "v_node"),
    "run": ("run", "rep", "repeat"),
    "cap_pf": ("cap_pf", "c_pf", "cnode_pf"),
    "temp_meas_C": ("temp_meas_c", "t_meas_c", "block_c"),
}


def _map_header(header):
    low = [h.strip().lower() for h in header]
    out = {}
    for key, names in ALIASES.items():
        for n in names:
            if n in low:
                out[key] = low.index(n)
                break
    missing = [k for k in ("device", "temperature", "time", "voltage") if k not in out]
    if missing:
        raise ValueError(f"CSV is missing required column(s): {missing}. Header was: {header}")
    return out


def load_csv(path):
    """Return dict keyed by (device, temperature_C, run) -> dict of numpy arrays."""
    recs = {}
    with open(path, newline="") as fh:
        # The Pico firmware prints '#' status lines; concatenated logs repeat the header.
        lines = [ln for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
    rd = csv.reader(lines)
    header = next(rd)
    col = _map_header(header)
    for row in rd:
        if not row:
            continue
        try:
            float(row[col["time"]])
        except (ValueError, IndexError):
            continue                     # a repeated header or a malformed line
        dev = row[col["device"]].strip()
        temp = round(float(row[col["temperature"]]), 1)
        run = row[col["run"]].strip() if "run" in col else "0"
        key = (dev, temp, run)
        r = recs.setdefault(key, {"t": [], "v": [], "cap_pf": [], "tm": []})
        r["t"].append(float(row[col["time"]]))
        r["v"].append(float(row[col["voltage"]]))
        r["cap_pf"].append(float(row[col["cap_pf"]]) if "cap_pf" in col and row[col["cap_pf"]] else math.nan)
        r["tm"].append(float(row[col["temp_meas_C"]]) if "temp_meas_C" in col and row[col["temp_meas_C"]] else math.nan)
    for r in recs.values():
        order = np.argsort(r["t"])
        for k in ("t", "v", "cap_pf", "tm"):
            r[k] = np.asarray(r[k], dtype=float)[order]
    return recs


# ---------------------------------------------------------------------------------------------
# Slope fitting
# ---------------------------------------------------------------------------------------------
def theil_sen(t, v, max_points=400):
    """Median of pairwise slopes (robust to spikes, RTN steps and a few bad points)."""
    n = len(t)
    if n < 3:
        raise ValueError("need >= 3 points for a slope")
    if n > max_points:
        idx = np.linspace(0, n - 1, max_points).round().astype(int)
        t, v = t[idx], v[idx]
    i, j = np.triu_indices(len(t), k=1)
    dt = t[j] - t[i]
    ok = dt > 0
    slopes = (v[j] - v[i])[ok] / dt[ok]
    m = float(np.median(slopes))
    b = float(np.median(v - m * t))
    return m, b


def ols(t, v):
    """Least-squares slope, intercept, slope standard error, residual std."""
    n = len(t)
    tm, vm = t.mean(), v.mean()
    stt = float(np.sum((t - tm) ** 2))
    m = float(np.sum((t - tm) * (v - vm)) / stt)
    b = vm - m * tm
    resid = v - (m * t + b)
    s = float(np.sqrt(np.sum(resid ** 2) / max(n - 2, 1)))
    se = s / math.sqrt(stt)
    return m, b, se, s


def _record_cap_pf(rec, cap_pf_default, cap_override):
    cap_col = rec["cap_pf"]
    col = float(np.nanmedian(cap_col)) if np.isfinite(cap_col).any() else None
    if cap_override is not None:
        return float(cap_override), col
    return (col if col is not None else float(cap_pf_default)), col


def fit_record(rec, cap_pf_default, skip_s=60.0, cap_tempco_ppm=None, cap_override=None):
    """Fit one decay record. Returns a dict with slope, current (A) and a status.

    Sign convention: I_leak > 0 means charge is LEAVING the node (node voltage falling for a
    positive node). I_leak = -C * dV/dt.

    status: "ok", "truncated", "drained" (I_lb_A is a LOWER bound) or "invalid" (see module doc).
    """
    t_all, v_all = rec["t"], rec["v"]
    cap_pf, cap_col = _record_cap_pf(rec, cap_pf_default, cap_override)
    C = cap_pf * 1e-12
    base = {"cap_pf": cap_pf, "cap_pf_column": cap_col, "n_raw": int(len(t_all)),
            "v_first": float(v_all[0]) if len(v_all) else float("nan")}

    # 1) valid-range cut: the record is trusted only up to its first out-of-range point
    v_ref = float(v_all[0])
    if not (V_LO < v_ref < V_HI):
        return dict(base, status="invalid",
                    reason=f"first sample {v_ref:.3f} V is outside {V_LO}-{V_HI} V (node never written, or railed)")
    ok_all = (v_all > V_LO) & (v_all < V_HI) & (v_all > v_ref - DROOP_MAX)
    bad = np.nonzero(~ok_all)[0]
    first_bad = int(bad[0]) if len(bad) else len(t_all)
    left_range = first_bad < len(t_all)

    sel = np.zeros(len(t_all), dtype=bool)
    sel[:first_bad] = True
    sel &= t_all >= (t_all[0] + skip_s)
    if sel.sum() < N_MIN_FIT:
        if left_range:
            # Drained (or rose out of range) before enough points: report a bound, not a fit.
            dt = float(t_all[first_bad] - t_all[0])
            if v_all[first_bad] >= V_HI:
                I_b = -C * (V_HI - v_ref) / dt          # node ROSE: charge flowing IN, at least this much
            else:
                v_lim = max(V_LO, v_ref - DROOP_MAX)
                I_b = C * (v_ref - v_lim) / dt          # node fell past the limit within dt
            return dict(base, status="drained", I_lb_A=I_b, t_out_s=dt,
                        v_out=float(v_all[first_bad]),
                        reason=f"node left the valid window after {dt:.0f} s: current is a LOWER bound")
        # simply a short record that stayed in range: use every in-range point, ignore skip_s
        sel = np.zeros(len(t_all), dtype=bool)
        sel[:first_bad] = True
        if sel.sum() < 10:
            return dict(base, status="invalid", reason=f"only {int(sel.sum())} points")
    t, v = t_all[sel], v_all[sel]
    tm = rec["tm"][sel]
    tempco_applied = False
    if cap_tempco_ppm is not None and np.isfinite(tm).all():
        # Charge Q is fixed; C(T) = C0 (1 + a dT)  ->  V(T) = Q / C(T). Undo it.
        a = cap_tempco_ppm * 1e-6
        v = v * (1.0 + a * (tm - tm.mean()))
        tempco_applied = True
    m_ts, b_ts = theil_sen(t, v)
    m_ols, b_ols, se, s = ols(t, v)
    half = len(t) // 2
    curv = None
    if half >= 5:
        m1, _ = theil_sen(t[:half], v[:half])
        m2, _ = theil_sen(t[half:], v[half:])
        if abs(m_ts) > 0:
            curv = (m2 - m1) / abs(m_ts)  # >0: decay slowing (bias-dependent leak or DA tail)
    return {
        **base,
        "status": "truncated" if left_range else "ok",
        "t_out_s": float(t_all[first_bad] - t_all[0]) if left_range else None,
        "n_points": int(len(t)),
        "window_s": float(t[-1] - t[0]),
        "v_start": float(v[0]), "v_end": float(v[-1]),
        "dv_total": float(v[-1] - v[0]),
        "droop_total_V": float(v_ref - v_all[first_bad - 1]),
        "slope_ts_V_per_s": m_ts,
        "slope_ols_V_per_s": m_ols,
        "slope_se_V_per_s": se,
        "resid_std_V": s,
        "I_ts_A": -C * m_ts,
        "I_ols_A": -C * m_ols,
        "I_se_A": C * se,
        "curvature": curv,
        "tempco_corrected": tempco_applied,
    }


# ---------------------------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------------------------
def binom_cdf_array(n, p):
    """P(X <= k) for k = 0..n, X ~ Binomial(n, p). Stable log-space, numpy only."""
    k = np.arange(n + 1)
    lg = np.array([math.lgamma(x + 1) for x in range(n + 1)])
    logpmf = lg[n] - lg - lg[::-1] + k * math.log(p) + (n - k) * math.log1p(-p)
    pmf = np.exp(logpmf - logpmf.max())
    pmf /= pmf.sum()
    return np.cumsum(pmf)


def order_stat_ci(n, p, conf=0.95):
    """Distribution-free CI for the p-quantile from order statistics.

    Returns (lo_rank, hi_rank) as 1-based ranks into the sorted sample, with None where the
    bound falls outside the sample (lo: below the minimum; hi: above the maximum).
    Coverage: P(x_(lo) <= xi_p <= x_(hi)) = F(hi-1) - F(lo-1) >= conf (F = binomial CDF).
    """
    a = (1.0 - conf) / 2.0
    F = binom_cdf_array(n, p)            # F[k] = P(X <= k)
    lo = None
    for r in range(n, 0, -1):            # largest r with P(X <= r-1) <= a
        if F[r - 1] <= a:
            lo = r
            break
    hi = None
    for r in range(1, n + 1):            # smallest r with P(X <= r-1) >= 1-a
        if F[r - 1] >= 1.0 - a:
            hi = r
            break
    return lo, hi


def bootstrap_quantile_ci(x, p, B=2000, conf=0.95, rng=None):
    rng = rng or np.random.default_rng(1)
    x = np.asarray(x)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    qs = np.quantile(x[idx], p, axis=1)
    a = (1 - conf) / 2
    return float(np.quantile(qs, a)), float(np.quantile(qs, 1 - a))


def lognormal_fit(x):
    lx = np.log(np.asarray(x))
    mu = float(lx.mean())
    sd = float(lx.std(ddof=1))
    q75, q25 = np.quantile(lx, [0.75, 0.25])
    sd_robust = float((q75 - q25) / 1.349)
    return mu, sd, sd_robust


def ppcc(x):
    """Probability-plot correlation of ln(x) vs normal scores (1.0 = perfectly lognormal)."""
    lx = np.sort(np.log(np.asarray(x)))
    n = len(lx)
    nd = NormalDist()
    z = np.array([nd.inv_cdf((i - 0.375) / (n + 0.25)) for i in range(1, n + 1)])  # Blom
    return float(np.corrcoef(lx, z)[0, 1])


def ppcc_critical(n, alpha=0.05, sims=400, rng=None):
    """Monte-Carlo lower critical value of PPCC for a true lognormal sample of size n."""
    rng = rng or np.random.default_rng(7)
    vals = [ppcc(np.exp(rng.standard_normal(n))) for _ in range(sims)]
    return float(np.quantile(vals, alpha))


def arrhenius_fit(temps_C, currents_A):
    """ln I = ln I0 - Ea / (k T). Returns Ea (eV), ln I0, R^2."""
    T = np.asarray(temps_C, dtype=float) + ZERO_C
    I = np.asarray(currents_A, dtype=float)
    x = 1.0 / (KB_EV * T)
    y = np.log(I)
    A = np.vstack([x, np.ones_like(x)]).T
    (m, c), *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = m * x + c
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(-m), float(c), r2


def arrhenius_factor(Ea_eV, T1_C, T2_C):
    T1, T2 = T1_C + ZERO_C, T2_C + ZERO_C
    return math.exp(Ea_eV / KB_EV * (1 / T1 - 1 / T2))


def n_to_see_tail(p, conf=0.95):
    """Smallest n with P(at least one sample beyond the p-upper-quantile) >= conf."""
    return math.ceil(math.log(1 - conf) / math.log1p(-p))


def n_for_upper_ci(p, conf=0.95):
    """Smallest n for which a distribution-free two-sided CI for the (1-p) quantile has an
    upper bound inside the sample (i.e. you can bound the tail from data alone)."""
    lo, hi = 10, 10
    # find a bracket
    while True:
        _, h = order_stat_ci(hi, 1 - p, conf)
        if h is not None:
            break
        lo, hi = hi, hi * 2
        if hi > 5_000_000:
            return None
    while hi - lo > 1:
        mid = (lo + hi) // 2
        _, h = order_stat_ci(mid, 1 - p, conf)
        if h is None:
            lo = mid
        else:
            hi = mid
    return hi


E6 = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8]


def snap_e6(x):
    dec = 10 ** math.floor(math.log10(x))
    best = min((abs(math.log(x / (m * dec))), m * dec) for m in E6 + [10.0])
    return best[1]


def plan_capacitor(I_A, window_s, dv_target_V=0.1, c_min_pf=100.0, c_max_pf=100_000.0):
    """C so the node drops ~dv_target in the window: C = I t / dV, snapped to E6, clamped."""
    c_pf = I_A * window_s / dv_target_V * 1e12
    c_pf = min(max(c_pf, c_min_pf), c_max_pf)
    c_pf = snap_e6(c_pf)
    dv = I_A * window_s / (c_pf * 1e-12)
    return c_pf, dv


# ---------------------------------------------------------------------------------------------
# Analysis pipeline
# ---------------------------------------------------------------------------------------------
QUANTS_DEFAULT = (0.1, 0.5, 0.9, 0.99)


def analyze(recs, cap_pf=470.0, skip_s=60.0, blank_name="BLANK", quantiles=QUANTS_DEFAULT,
            boot=2000, cap_tempco_ppm=None, floor_sigma=3.0, verbose=True, seed=1, cap_override=None):
    rng = np.random.default_rng(seed)
    fits = {}
    for key, rec in recs.items():
        fits[key] = fit_record(rec, cap_pf, skip_s=skip_s, cap_tempco_ppm=cap_tempco_ppm,
                               cap_override=cap_override)
    warnings = []
    if cap_override is not None:
        n_diff = sum(1 for f in fits.values() if f["cap_pf_column"] is not None
                     and abs(f["cap_pf_column"] / cap_override - 1) > 0.01)
        if n_diff:
            warnings.append(f"--cap-pf {cap_override:g} overrides a cap_pf column that differs by > 1% in "
                            f"{n_diff} record(s). Intended? (Set CAP_PF in the firmware instead.)")
    for (dev, T, run), f in sorted(fits.items()):
        if f["status"] == "invalid":
            warnings.append(f"INVALID record dropped: {dev} at {T} C run {run}: {f['reason']}")

    # Blank (floor) per temperature: mean over usable blank runs at that temperature
    blanks = {}
    for (dev, T, run), f in fits.items():
        if dev.upper() == blank_name.upper():
            if f["status"] in ("ok", "truncated"):
                blanks.setdefault(T, []).append(f["I_ts_A"])
            elif f["status"] == "drained":
                warnings.append(f"BLANK at {T} C run {run} DRAINED: the bench itself leaks >= {fmtA(f['I_lb_A'])}."
                                " Not used as a floor. Fix the bench (section 11).")
    blank_I = {T: float(np.mean(v)) for T, v in blanks.items()}
    blank_sd = {T: (float(np.std(v, ddof=1)) if len(v) > 1 else float("nan")) for T, v in blanks.items()}

    # Per device & temperature current (average over usable runs), blank-subtracted
    per = {}
    for (dev, T, run), f in fits.items():
        if dev.upper() == blank_name.upper() or f["status"] == "invalid":
            continue
        per.setdefault((dev, T), []).append(f)
    devices = sorted({d for d, _ in per})
    temps = sorted({T for _, T in per})
    for T in temps:
        if len(blanks.get(T, [])) < 2:
            warnings.append(f"T = {T} C: {len(blanks.get(T, []))} usable BLANK run(s): floor not established"
                            " (need >= 2 that agree)")
    table = {}
    for (dev, T), fl in per.items():
        good = [f for f in fl if f["status"] in ("ok", "truncated")]
        b = blank_I.get(T, 0.0)
        bsd = blank_sd.get(T, float("nan"))
        if good:
            I_raw = float(np.mean([f["I_ts_A"] for f in good]))
            I_se = float(np.sqrt(np.sum([f["I_se_A"] ** 2 for f in good])) / len(good))
            I = I_raw - b
            floor = max(floor_sigma * I_se, floor_sigma * bsd if math.isfinite(bsd) else 0.0,
                        0.5 * abs(b) if b else 0.0, 1e-18)
            # Only a quiet run that never left the window may be called "below floor"
            quiet = all(f["status"] == "ok" and f["droop_total_V"] < DROOP_BELOW_FLOOR for f in good)
            table[(dev, T)] = {"I_raw_A": I_raw, "I_A": I, "I_se_A": I_se, "floor_A": floor,
                               "below_floor": bool(I <= floor and quiet), "censored": False,
                               "status": "truncated" if any(f["status"] == "truncated" for f in good) else "ok",
                               "runs": len(good), "cap_pf": good[0]["cap_pf"], "dv_total": good[0]["dv_total"],
                               "curvature": good[0]["curvature"]}
        else:   # every run drained: right-censored, current is AT LEAST the bound
            I_lb = float(max(f["I_lb_A"] for f in fl))
            table[(dev, T)] = {"I_raw_A": I_lb, "I_A": I_lb - b, "I_se_A": float("nan"), "floor_A": float("nan"),
                               "below_floor": False, "censored": True, "status": "drained",
                               "runs": len(fl), "cap_pf": fl[0]["cap_pf"], "dv_total": None, "curvature": None}

    results = {"blank_I_A": blank_I, "blank_sd_A": blank_sd, "temperatures_C": temps,
               "n_devices": len(devices), "per_temperature": {}, "arrhenius": {}, "records": {},
               "warnings": warnings}
    for (dev, T), r in table.items():
        results["records"][f"{dev}@{T}"] = r

    nd = NormalDist()
    for T in temps:
        keys = [(d, T) for d in devices if (d, T) in table]
        vals = np.array([table[k]["I_A"] for k in keys])
        below = np.array([table[k]["below_floor"] for k in keys])
        cens = np.array([table[k]["censored"] for k in keys])
        trunc = np.array([table[k]["status"] == "truncated" for k in keys])
        floors = np.array([table[k]["floor_A"] for k in keys])
        n = len(vals)
        # Left-censoring: values below the bench floor are replaced by the floor. This biases
        # LOW quantiles only. Right-censoring: drained devices enter at their LOWER bound, so every
        # quantile (and every upper CI limit) is then a LOWER bound on the true value.
        x = np.where(below, floors, vals)
        x = np.maximum(x, 1e-21)
        xs = np.sort(x)
        qrows = []
        for p in quantiles:
            q = float(np.quantile(x, p))
            lo, hi = order_stat_ci(n, p)
            os_lo = float(xs[lo - 1]) if lo else None
            os_hi = float(xs[hi - 1]) if hi else None
            if n * min(p, 1 - p) < 5:
                b_lo = b_hi = None            # a bootstrap CI cannot reach beyond the sample extremes
            else:
                b_lo, b_hi = bootstrap_quantile_ci(x, p, B=boot, rng=rng)
            qrows.append({"p": p, "q_A": q, "os_ci": [os_lo, os_hi], "boot_ci": [b_lo, b_hi]})
        # drained devices enter at their lower bound: dropping them would shrink sigma_ln
        mu, sd, sd_rob = lognormal_fit(x[~below] if (~below).sum() >= 5 else x)
        pc = ppcc(x)
        pc_crit = ppcc_critical(n, rng=np.random.default_rng(11))
        # Lognormal extrapolation to the 1e-4 upper tail (MODEL, not data)
        z4 = nd.inv_cdf(1 - 1e-4)
        q4 = math.exp(mu + sd * z4)
        bs = []
        for _ in range(min(boot, 1000)):
            s = x[rng.integers(0, n, n)]
            m_, s_, _ = lognormal_fit(s)
            bs.append(math.exp(m_ + s_ * z4))
        q4_ci = [float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))]
        results["per_temperature"][T] = {
            "n": n, "n_below_floor": int(below.sum()), "n_drained_lower_bound": int(cens.sum()),
            "n_truncated": int(trunc.sum()), "quantiles": qrows,
            "lognormal_mu_ln": mu, "lognormal_sigma_ln": sd, "sigma_ln_robust": sd_rob,
            "median_A": float(np.median(x)), "ppcc": pc, "ppcc_crit_5pct": pc_crit,
            "lognormal_rejected": bool(pc < pc_crit),
            "q_1e-4_lognormal_extrapolation_A": q4, "q_1e-4_extrap_CI_A": q4_ci,
            "tail_ratio_q99_over_median": float(np.quantile(x, 0.99) / np.median(x)) if n >= 2 else None,
        }

    # Arrhenius per device (needs >= 3 temperatures with measured, above-floor, uncensored currents)
    eas = {}
    for d in devices:
        pts = [(T, table[(d, T)]["I_A"]) for T in temps
               if (d, T) in table and not table[(d, T)]["below_floor"] and not table[(d, T)]["censored"]
               and table[(d, T)]["I_A"] > 0]
        if len(pts) >= 3:
            Ea, lnI0, r2 = arrhenius_fit([p[0] for p in pts], [p[1] for p in pts])
            eas[d] = {"Ea_eV": Ea, "r2": r2, "n_T": len(pts)}
    if eas:
        e = np.array([v["Ea_eV"] for v in eas.values()])
        bs = [float(np.median(e[rng.integers(0, len(e), len(e))])) for _ in range(boot)]
        # pooled: Arrhenius of the per-temperature median currents
        med_T = [results["per_temperature"][T]["median_A"] for T in temps]
        pooled = arrhenius_fit(temps, med_T) if len(temps) >= 2 else (float("nan"), 0, float("nan"))
        results["arrhenius"] = {
            "n_devices_fitted": len(eas), "Ea_median_eV": float(np.median(e)),
            "Ea_median_CI_eV": [float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))],
            "Ea_IQR_eV": [float(np.quantile(e, 0.25)), float(np.quantile(e, 0.75))],
            "Ea_min_eV": float(e.min()), "Ea_max_eV": float(e.max()),
            "Ea_pooled_medians_eV": pooled[0], "pooled_r2": pooled[2],
            "per_device": eas,
        }
    if verbose:
        print_report(results)
    return results


def fmtA(x):
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "   n/a  "
    a = abs(x)
    for unit, s in (("pA", 1e-12), ("fA", 1e-15), ("aA", 1e-18), ("zA", 1e-21)):
        if a >= s or unit == "zA":
            return f"{x / s:8.3g} {unit}"
    return f"{x:.3g} A"


def print_report(res):
    print("=" * 92)
    print("E4 LEAKAGE-TAIL REPORT (charge-decay method, I = -C dV/dt)")
    print("=" * 92)
    print(f"devices: {res['n_devices']}   temperatures (C): {res['temperatures_C']}")
    if res["blank_I_A"]:
        for T, b in res["blank_I_A"].items():
            print(f"bench floor (blank) at {T:5.1f} C: {fmtA(b)}  (sd between blank runs: {fmtA(res['blank_sd_A'][T])})")
    else:
        print("no BLANK runs found: currents are NOT floor-corrected (op-amp bias current included)")
    for w in res.get("warnings", []):
        print(f"WARNING: {w}")
    for T, r in res["per_temperature"].items():
        print("-" * 92)
        print(f"T = {T} C   n = {r['n']}   below floor: {r['n_below_floor']}   median = {fmtA(r['median_A'])}"
              f"   truncated fits: {r['n_truncated']}")
        if r["n_drained_lower_bound"]:
            print(f"  {r['n_drained_lower_bound']} run(s) DRAINED: the node could not hold these devices, so their"
                  " currents are LOWER bounds.")
            print("  Every quantile and upper CI limit below is then a LOWER bound too. Re-measure those devices"
                  " with a 10x larger C_s (or a shorter window).")
        print(f"  lognormal: sigma_ln = {r['lognormal_sigma_ln']:.2f} (robust {r['sigma_ln_robust']:.2f}),"
              f" PPCC = {r['ppcc']:.4f} (5% critical {r['ppcc_crit_5pct']:.4f})"
              f" -> {'NOT lognormal (heavier or odd tail)' if r['lognormal_rejected'] else 'consistent with lognormal'}")
        print(f"  {'quantile':>9s} {'value':>12s} {'order-stat 95% CI':>30s} {'bootstrap 95% CI':>28s}")
        foot = False
        for q in r["quantiles"]:
            lo, hi = q["os_ci"]
            os_s = f"[{fmtA(lo) if lo is not None else ' <min   '}, {fmtA(hi) if hi is not None else ' >max   '}]"
            mark = ""
            if q["boot_ci"][0] is None:
                mark, foot = " *", True
            print(f"  {q['p']:9.4g} {fmtA(q['q_A']):>12s} {os_s:>30s} [{fmtA(q['boot_ci'][0])}, {fmtA(q['boot_ci'][1])}]{mark}")
        if foot:
            print("  * bootstrap CI not valid this far into the tail (n x tail fraction < 5): it can never"
                  " exceed the sample maximum. Trust the order-statistic column.")
        print(f"  1e-4 upper quantile by LOGNORMAL EXTRAPOLATION (model, not data): {fmtA(r['q_1e-4_lognormal_extrapolation_A'])}"
              f"  95% CI [{fmtA(r['q_1e-4_extrap_CI_A'][0])}, {fmtA(r['q_1e-4_extrap_CI_A'][1])}]"
              + ("  (drained runs present: treat as a LOWER bound)" if r["n_drained_lower_bound"] else ""))
    a = res.get("arrhenius")
    print("-" * 92)
    if a:
        print(f"Arrhenius: {a['n_devices_fitted']} devices with >=3 temperatures. Ea median = {a['Ea_median_eV']:.3f} eV"
              f" (95% CI {a['Ea_median_CI_eV'][0]:.3f}-{a['Ea_median_CI_eV'][1]:.3f}),"
              f" IQR {a['Ea_IQR_eV'][0]:.3f}-{a['Ea_IQR_eV'][1]:.3f}, range {a['Ea_min_eV']:.3f}-{a['Ea_max_eV']:.3f}")
        print(f"  pooled fit of per-temperature medians: Ea = {a['Ea_pooled_medians_eV']:.3f} eV, R^2 = {a['pooled_r2']:.4f}")
        print("  reading guide: ~0.56 eV = silicon generation current (Eg/2); ~1.1 eV = diffusion current (Eg);"
              " <0.4 eV = tunnelling, surface or fixture leakage")
    else:
        print("Arrhenius: not enough temperatures (need >= 3 per device above the floor)")
    print("-" * 92)
    print("Sample size for the tail (distribution-free, 95% confidence):")
    print_sample_size_table()


def print_sample_size_table(ps=(1e-1, 1e-2, 1e-3, 1e-4, 2e-5)):
    print(f"  {'tail p':>8s} {'n to see >=1 beyond q (95%)':>28s} {'n for data-only upper CI':>26s} {'n for ~10 exceedances':>22s}")
    for p in ps:
        n1 = n_to_see_tail(p)
        n2 = n_for_upper_ci(p) if p >= 1e-4 else math.ceil(3.689 / p)  # see note
        n3 = math.ceil(10 / p)
        print(f"  {p:8.0e} {n1:28,d} {n2:26,d} {n3:22,d}")
    print("  (for p < 1e-4 the middle column uses the asymptote ~3.69/p to keep run time short)")


# ---------------------------------------------------------------------------------------------
# First-principles expected numbers for the E4 write-up
# ---------------------------------------------------------------------------------------------
def expected():
    print("=" * 92)
    print("E4 FIRST-PRINCIPLES NUMBERS (all [ESTIMATE] unless the input is tagged)")
    print("=" * 92)
    print("\n1) Charge conservation: I = C dV/dt.  The same current gives a 'loud' signal on a tiny node.")
    cases = [("imec-class 2T0C cell, typical (study: 75 zA on 0.15 fF)", 0.15e-15, 75e-21),
             ("hot-side 1e-4 tail ceiling, 1 b at 1 s (22.5 aA on 0.15 fF)", 0.15e-15, 22.5e-18),
             ("home bench, 100 pF node, 1 fA", 100e-12, 1e-15),
             ("home bench, 10 nF node, 1 pA (typical 2N7000)", 10e-9, 1e-12),
             ("home bench, 470 pF node, 1 pA (C too small: drains)", 470e-12, 1e-12),
             ("home bench, 100 nF node, 100 pA (hot)", 100e-9, 100e-12)]
    print(f"  {'case':62s} {'dV/dt':>14s} {'time for 10 mV':>16s} {'0.9 V -> 0.45 V':>16s}")
    for name, C, I in cases:
        s = I / C
        print(f"  {name:62s} {s*1e6:10.3g} uV/s {0.01/s:13.3g} s {0.45/s:13.3g} s")
    print("  -> a 0.15 fF cell turns 75 zA into ~0.5 mV/s. The cell IS the electrometer: small C is the trick.")
    print("  -> but the bench node must also HOLD the current for the whole window: C_s >= I x T / 0.3 V.")
    print("     A 1 pA device empties a 470 pF node in ~210 s, so a 1,800 s record would be mostly a flat rail.")

    print("\n2) Noise-limited current resolution of a straight-line fit (ADS1115, +/-2.048 V range):")
    lsb = 4.096 / 65536
    sig_v = lsb  # ~1 LSB rms at 8 SPS, averaged to 1 sample/s  [ESTIMATE]
    print(f"  ADC LSB = {lsb*1e6:.1f} uV; assumed rms noise per 1-s sample = {sig_v*1e6:.1f} uV")
    print(f"  sigma_slope = sigma_v * sqrt(12/N) / T   (N points evenly over T seconds)")
    print(f"  {'C node':>8s} {'window':>8s} {'sigma_I (1 sigma)':>18s}")
    for C in (100e-12, 470e-12, 1e-9, 10e-9):
        for T in (300, 600, 1800):
            N = T
            s = sig_v * math.sqrt(12 / N) / T
            print(f"  {C*1e12:6.0f}pF {T:7d}s {fmtA(C*s):>18s}")
    print("  -> noise is NOT the limit; op-amp bias current, capacitor insulation, dielectric absorption,")
    print("     humidity and temperature drift are. Plan on ~1-10 fA after blank subtraction with an air or PTFE")
    print("     capacitor, and 10-100 fA with a boxed film capacitor until your blank shows otherwise.")
    print("  Capacitor insulation: WIMA FKP 2 guarantees >= 5e5 MOhm at 20 C [REPORTED, retailer copies of the")
    print(f"  WIMA data] -> <= {0.9/5e11*1e12:.1f} pA at 0.9 V. Real film leakage is usually far lower; your blank measures it.")
    print("  Temperature drift on a big C: polypropylene ~ -200 ppm/K on a ~1 V node is ~200 uV/K. On 10 nF a")
    print("  20 fA blank moves only 3.6 uV in 1,800 s, so measure the fA floor on 470 pF, not on 10 nF.")

    print("\n3) kT/C noise on the node (one-time, frozen at switch-off):")
    for C in (0.15e-15, 100e-12, 1e-9):
        print(f"  C = {C*1e12:10.4g} pF: sqrt(kT/C) at 300 K = {math.sqrt(KB_J*300/C)*1e6:10.3g} uV")

    print("\n4) Dielectric absorption (DA) looks like a fake current: I_DA(t) ~ C*DA*dV_step/(ln(1000)*t)  [crude model]")
    print("   DA values: polypropylene 0.05-0.10%, C0G/NP0 ~0.6%, X7R ~2.5% [REPORTED, WIMA table]")
    print(f"  {'dielectric':>14s} {'DA':>6s} {'no soak: 1 V step, t=60 s':>28s} {'soaked: 0.1 V kickback, t=300 s':>34s}")
    for name, da in (("polypropylene", 0.0005), ("C0G/NP0", 0.006), ("X7R", 0.025)):
        C = 100e-12
        a = C * da * 1.0 / (math.log(1000) * 60)
        b = C * da * 0.1 / (math.log(1000) * 300)
        print(f"  {name:>14s} {da*100:5.2f}% {fmtA(a):>28s} {fmtA(b):>34s}")
    print("  -> use polypropylene or PTFE, and SOAK the node at its start voltage before switching off.")

    print("\n5) Kickback when the DUT switches off: dV = -[Cgd*(V_node + Vth) + Cds*V_WBL] / C_node")
    print("   Only the part of the 9 V gate swing below V_node + Vth (~2-4 V) couples: above it the channel is")
    print("   still on and the 6.9 kOhm bit line holds the node. Then the bit line steps 1.03 V -> 0 V through Cds.")
    print("   Cgd ~5 pF (2N7000 Crss 4 typ / 5 max at 25 V [DATASHEET], larger near 1 V);")
    print("   Cds ~10-50 pF near 1 V [ESTIMATE: Coss 11 typ / 25 max at 25 V, x2-4 for a junction at ~1 V].")
    print(f"  {'C_node':>8s} {'gate term':>20s} {'bit-line term':>22s} {'total':>22s}")
    for cn in (470e-12, 1e-9, 10e-9, 47e-9):
        g = (-5e-12 * 4 / cn, -5e-12 * 2 / cn)
        d = (-50e-12 * 1.03 / cn, -10e-12 * 1.03 / cn)
        print(f"  {cn*1e12:6.0f}pF {g[0]*1e3:8.1f} to {g[1]*1e3:5.1f} mV {d[0]*1e3:9.1f} to {d[1]*1e3:5.1f} mV"
              f" {(g[0]+d[0])*1e3:9.1f} to {(g[1]+d[1])*1e3:5.1f} mV")
    print("  -> a bigger C_s is the cure; the gate voltage matters little. (2T0C papers see the same coupling.)")

    print("\n6) Arrhenius scaling, I ~ exp(-Ea/kT):")
    print(f"  {'Ea (eV)':>8s} {'x per +10 K near 25 C':>22s} {'x from 25 to 85 C':>18s}  meaning")
    for Ea, m in ((0.56, "Si generation current, ~Eg/2"), (0.8, "study's IGZO planning value"),
                  (1.12, "Si diffusion current, ~Eg")):
        print(f"  {Ea:8.2f} {arrhenius_factor(Ea, 25, 35):22.2f} {arrhenius_factor(Ea, 25, 85):18.0f}  {m}")
    print("  Temperature stability: dlnI/dT = Ea/(kT^2) = "
          f"{0.6/(KB_EV*298.15**2)*100:.1f} %/K at 0.6 eV -> hold the block within +/-0.2 K.")

    print("\n7) Capacitor plan for a 600 s window and ~100 mV droop (E6 values, 100 pF-100 nF):")
    print(f"  {'I at 25 C':>10s} | " + " | ".join(f"{T:>3d} C (Ea 0.6): C, droop" for T in (25, 45, 65, 85)))
    for I25 in (1e-15, 1e-14, 1e-13, 1e-12, 1e-11):
        cells = []
        for T in (25, 45, 65, 85):
            I = I25 * arrhenius_factor(0.6, 25, T)
            c, dv = plan_capacitor(I, 600)
            cells.append(f"{c:8.0f} pF,{dv*1e3:7.1f} mV")
        print(f"  {fmtA(I25):>10s} | " + " | ".join(f"{c:>23s}" for c in cells))
    print("  If droop at 100 pF is < 1 mV, lengthen the window (1800 s) or accept a floor-limited result.")
    print("\n7b) Minimum C_s so a device stays inside the 0.3 V droop limit: C_s >= I x T / 0.3 V")
    print(f"  {'I':>10s} {'T = 120 s':>12s} {'T = 600 s':>12s} {'T = 1,800 s':>12s}")
    for I in (1e-13, 1e-12, 1e-11, 1e-10):
        print(f"  {fmtA(I):>10s} " + " ".join(f"{I*T/0.3*1e12/1e3:9.2f} nF" for T in (120, 600, 1800)))
    print("  For a POPULATION, size C_s so the MEDIAN droops ~30 mV: then a device 10x leakier still stays")
    print("  under 0.3 V. 2N7000s at 25 C (median 0.1-10 pA, 600 s): about 2.2-100 nF; 10 nF is a good start.")

    print("\n8) Sample size: why the Oxide Tail Spec needs >=1e5 cells per split")
    print_sample_size_table()
    print(f"  With n = 100 devices the highest quantile you can bound from data alone (two-sided 95%) is")
    print(f"  q = 0.025^(1/n) = {0.025**(1/100):.3f}. The 1e-4 quantile from 100 devices is a lognormal")
    print("  EXTRAPOLATION: it is only as good as the lognormal assumption.")

    print("\n9) Calibration currents:")
    for R, V in ((10e9, 0.1), (10e9, 0.01), (10e9, 0.001), (100e9, 0.001)):
        print(f"  {V*1e3:6.1f} mV across {R/1e9:5.0f} GOhm -> {fmtA(V/R)}")
    for Cinj, ramp in ((10e-12, 1e-4), (10e-12, 1e-3), (1e-12, 1e-3)):
        print(f"  ramp {ramp*1e3:5.2f} mV/s through {Cinj*1e12:4.0f} pF injector -> {fmtA(Cinj*ramp)}")
    print()


# ---------------------------------------------------------------------------------------------
# Self-test on synthetic data
# ---------------------------------------------------------------------------------------------
def synth_dataset(path, n_dev=120, temps=(25, 45, 65, 85), seed=42, I25_median=0.5e-12,
                  sigma_ln=0.9, Ea_mean=0.70, Ea_sd=0.05, n_outliers=3, bias_A=3e-15):
    rng = np.random.default_rng(seed)
    lnI = np.log(I25_median) + sigma_ln * rng.standard_normal(n_dev)
    lnI[:n_outliers] += math.log(50.0)       # a small "tail population" (e.g. damaged junctions)
    Ea = np.clip(Ea_mean + Ea_sd * rng.standard_normal(n_dev), 0.4, 1.2)
    truth = {}
    lsb = 4.096 / 65536
    rows = []

    def record(dev, T, I_dev):
        window = 600 if T == 25 else 300
        I_tot = I_dev + bias_A
        c_pf, _ = plan_capacitor(max(I_tot, 1e-16), window)
        C = c_pf * 1e-12
        t = np.arange(0, 60 + window + 1, 1.0)
        v0 = 1.0 - 0.1                       # 1.0 V written, ~0.1 V kickback
        v = v0 - I_tot / C * t
        v += 2e-3 * np.exp(-t / 20.0)        # settling / DA relaxation in the first minute
        v += lsb * rng.standard_normal(len(t))
        spikes = rng.random(len(t)) < 0.005
        v[spikes] += rng.choice([-1, 1], spikes.sum()) * 1e-3
        v = np.round(v / lsb) * lsb          # ADC quantisation
        for ti, vi in zip(t, v):
            rows.append((dev, T, f"{ti:.1f}", f"{vi:.7f}", f"{c_pf:.0f}"))

    for T in temps:
        record("BLANK", T, 0.0)
        for i in range(n_dev):
            I = math.exp(lnI[i]) * arrhenius_factor(Ea[i], 25, T)
            dev = f"Q{i+1:03d}"
            truth[(dev, float(T))] = I
            record(dev, T, I)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["device", "temperature", "time", "voltage", "cap_pf"])
        w.writerows(rows)
    return truth, {f"Q{i+1:03d}": float(Ea[i]) for i in range(n_dev)}


def selftest(workdir=None):
    ok = True
    print("SELFTEST 1: order-statistic CI for the median of n=100 should be ranks (40, 61)")
    lo, hi = order_stat_ci(100, 0.5)
    print(f"  got ({lo}, {hi})")
    ok &= (lo, hi) == (40, 61)

    print("SELFTEST 2: n to see the 1e-4 tail at 95% = ceil(ln 0.05 / ln(1-1e-4)) = 29,956")
    n = n_to_see_tail(1e-4)
    print(f"  got {n:,d}")
    ok &= n == 29956

    print("SELFTEST 3: Arrhenius fit recovers Ea = 0.70 eV exactly on noiseless points")
    Ts = [25, 45, 65, 85]
    Is = [1e-13 * arrhenius_factor(0.70, 25, T) for T in Ts]
    Ea, _, r2 = arrhenius_fit(Ts, Is)
    print(f"  got Ea = {Ea:.4f} eV, R^2 = {r2:.6f}")
    ok &= abs(Ea - 0.70) < 1e-6

    print("SELFTEST 4: synthetic bench data (120 devices x 4 temperatures + blanks, lognormal, 3 tail outliers)")
    workdir = workdir or tempfile.mkdtemp(prefix="T2_leakage_")
    os.makedirs(workdir, exist_ok=True)
    path = os.path.join(workdir, "T2_leakage_synthetic.csv")
    truth, Ea_true = synth_dataset(path)
    print(f"  wrote {path}")
    recs = load_csv(path)
    res = analyze(recs, cap_pf=470, skip_s=60, boot=600, verbose=True)

    # per-record current recovery (well above floor)
    errs = []
    for (dev, T), I in truth.items():
        r = res["records"][f"{dev}@{T}"]
        if I > 100e-15:
            errs.append(abs(r["I_A"] / I - 1))
    med_err = float(np.median(errs))
    p95_err = float(np.quantile(errs, 0.95))
    print(f"  per-record current error (I_true > 100 fA): median {med_err*100:.2f}%, 95th pct {p95_err*100:.2f}%")
    ok &= med_err < 0.03

    for T in (25.0, 85.0):
        true_vals = np.array([I for (d, t), I in truth.items() if t == T])
        est_med = res["per_temperature"][T]["median_A"]
        true_med = float(np.median(true_vals))
        e = abs(est_med / true_med - 1)
        print(f"  T={T}: median estimated {fmtA(est_med)} vs true {fmtA(true_med)} ({e*100:.1f}% error)")
        ok &= e < 0.10
        q90 = [q for q in res["per_temperature"][T]["quantiles"] if q["p"] == 0.9][0]
        tq90 = float(np.quantile(true_vals, 0.9))
        e90 = abs(q90["q_A"] / tq90 - 1)
        print(f"  T={T}: q0.9 estimated {fmtA(q90['q_A'])} vs true {fmtA(tq90)} ({e90*100:.1f}% error)")
        ok &= e90 < 0.10
    rob = res["per_temperature"][25.0]["sigma_ln_robust"]
    true25 = np.array([I for (d, t), I in truth.items() if t == 25.0])
    rob_true = lognormal_fit(true25)[2]
    print(f"  robust sigma_ln at 25 C = {rob:.3f} vs {rob_true:.3f} for the true currents of the same"
          f" 120 devices (population value 0.9; n=120 sampling scatter is ~+/-0.1)")
    ok &= abs(rob - rob_true) < 0.03
    flagged = res["per_temperature"][25.0]["lognormal_rejected"]
    print(f"  heavy-tail check: 3 of 120 devices were made 50x leakier -> lognormal rejected = {flagged}")
    ok &= flagged
    ea_med_true = float(np.median(list(Ea_true.values())))
    ea_med = res["arrhenius"]["Ea_median_eV"]
    print(f"  Ea median estimated {ea_med:.3f} eV vs true sample median {ea_med_true:.3f} eV")
    ok &= abs(ea_med - ea_med_true) < 0.03
    q99 = [q for q in res["per_temperature"][25.0]["quantiles"] if q["p"] == 0.99][0]
    print(f"  q0.99 bootstrap CI suppressed at n = 120 (n x 0.01 < 5): {q99['boot_ci'] == [None, None]}")
    ok &= q99["boot_ci"] == [None, None]

    print("SELFTEST 5: the node-range rule. A fixed 470 pF node, 1,800 s, buffer clamped near 0 V, ADC clips at"
          " 2.048 V")
    ok &= selftest_range_rule()

    print("SELFTEST 6: --cap-pf overrides the cap_pf column")
    rec = synth_record(1e-13, 470e-12, 600, np.random.default_rng(3))
    f_col = fit_record(rec, 470.0)
    f_ovr = fit_record(rec, 470.0, cap_override=500.0)
    ratio = f_ovr["I_ts_A"] / f_col["I_ts_A"]
    print(f"  I(override 500 pF) / I(column 470 pF) = {ratio:.4f} (expect {500/470:.4f})")
    ok &= abs(ratio - 500 / 470) < 1e-9
    print("SELFTEST", "PASS" if ok else "FAIL")
    return ok


def synth_record(I_A, C_F, window_s, rng, v0=0.9, dev="X", cap_col_pf=None):
    """One decay record as the real bench would log it: settling bump, 1-LSB noise, the buffer's
    output clamped near 0 V, the ADS1115 clipped at 2.0479 V, then quantised."""
    lsb = 4.096 / 65536
    t = np.arange(0, window_s + 1, 1.0)
    v = v0 - I_A / C_F * t + 2e-3 * np.exp(-t / 20.0) + lsb * rng.standard_normal(len(t))
    v = np.clip(v, 0.004, 2.0479)
    v = np.round(v / lsb) * lsb
    cap = np.full(len(t), (cap_col_pf if cap_col_pf is not None else C_F * 1e12))
    return {"t": t, "v": v, "cap_pf": cap, "tm": np.full(len(t), math.nan), "dev": dev}


def selftest_range_rule():
    ok = True
    rng = np.random.default_rng(9)
    recs = {}
    cases = {"P1pA": 1e-12, "P10pA": 1e-11, "Plow": 2e-15 + 3e-15}   # every run also carries the 3 fA bench
    for name, I in cases.items():
        recs[(name, 25.0, "0")] = synth_record(I, 470e-12, 1800, rng)
    # three good blanks (+3 fA) and one whose node was never written (starts at 2.6 V -> ADC reads 2.0479 V)
    for k in range(3):
        recs[("BLANK", 25.0, str(k))] = synth_record(3e-15, 470e-12, 1800, rng)
    recs[("BLANK", 25.0, "railed")] = synth_record(15e-15, 470e-12, 1800, rng, v0=2.6)
    res = analyze(recs, cap_pf=470.0, skip_s=60.0, boot=200, verbose=False)
    r1 = res["records"]["P1pA@25.0"]
    r10 = res["records"]["P10pA@25.0"]
    rlo = res["records"]["Plow@25.0"]
    print(f"  1 pA device : status {r1['status']:9s} I = {fmtA(r1['I_A'])} (true 1 pA), below floor = {r1['below_floor']}")
    print(f"  10 pA device: status {r10['status']:9s} I >= {fmtA(r10['I_A'])} (true 10 pA), below floor = {r10['below_floor']}")
    print(f"  2 fA device : status {rlo['status']:9s} I = {fmtA(rlo['I_A'])} (true 2 fA after the 3 fA blank)")
    ok &= r1["status"] in ("truncated", "drained") and r1["I_A"] >= 0.5e-12 and not r1["below_floor"]
    ok &= r1["status"] != "truncated" or abs(r1["I_A"] / 1e-12 - 1) < 0.10
    ok &= r10["status"] == "drained" and r10["censored"] and 0.5e-12 <= r10["I_A"] <= 1e-11 and not r10["below_floor"]
    ok &= rlo["status"] == "ok" and abs(rlo["I_A"] - 2e-15) < 1e-15
    railed_dropped = any("INVALID" in w and "railed" in w for w in res["warnings"])
    print(f"  blank whose node started at 2.6 V (ADC clipped): dropped as INVALID = {railed_dropped};"
          f" floor from the 3 good blanks = {fmtA(res['blank_I_A'][25.0])} (true 3 fA)")
    ok &= railed_dropped and abs(res["blank_I_A"][25.0] - 3e-15) < 1e-15
    nd = res["per_temperature"][25.0]["n_drained_lower_bound"]
    print(f"  drained (lower-bound) devices counted at 25 C: {nd} (expect 1)")
    ok &= nd == 1
    # the old behaviour this replaces: a plain fit over the whole clamped trace
    t, v = recs[("P10pA", 25.0, "0")]["t"], recs[("P10pA", 25.0, "0")]["v"]
    m_naive, _ = theil_sen(t[t >= 60], v[t >= 60])
    print(f"  (a naive fit of the clamped 10 pA trace would report {fmtA(-470e-12 * m_naive + 0.0)}: a 'perfect' device)")
    return ok


# ---------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", help="log CSV: device,temperature,time,voltage[,run,cap_pf,temp_meas_C]")
    ap.add_argument("--cap-pf", type=float, default=None,
                    help="node capacitance in pF. Given: OVERRIDES the cap_pf column for every record. "
                         "Not given: the cap_pf column is used (470 pF if there is no column). With --plan: "
                         "prints the longest window this C can hold.")
    ap.add_argument("--skip-s", type=float, default=60.0, help="seconds to skip after switch-off (settling)")
    ap.add_argument("--blank-name", default="BLANK")
    ap.add_argument("--quantiles", default="0.1,0.5,0.9,0.99")
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--cap-tempco-ppm", type=float, default=None,
                    help="capacitor tempco in ppm/K (polypropylene is roughly -200 to -250); needs temp_meas_C")
    ap.add_argument("--json", help="write results to this JSON file")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--workdir", help="where --selftest writes its synthetic CSV")
    ap.add_argument("--expected", action="store_true", help="print first-principles numbers for E4")
    ap.add_argument("--plan", type=float, help="expected current (A): suggest a capacitor")
    ap.add_argument("--window-s", type=float, default=600.0)
    a = ap.parse_args(argv)

    if a.selftest:
        return 0 if selftest(a.workdir) else 1
    if a.expected:
        expected()
        return 0
    if a.plan:
        I, W = a.plan, a.window_s
        c, dv = plan_capacitor(I, W)
        print(f"For I = {fmtA(I)} over {W:.0f} s:")
        print(f"  one device      : C = {c:.0f} pF -> droop {dv*1e3:.1f} mV (target ~100 mV)")
        cp, dvp = plan_capacitor(I, W, dv_target_V=0.03)
        print(f"  a POPULATION with this median: C = {cp:.0f} pF -> median droop {dvp*1e3:.1f} mV;"
              f" a device 10x leakier droops {10*dvp*1e3:.0f} mV {'(OK, < 300 mV)' if 10*dvp < 0.3 else '(too much: shorten the window)'}")
        print(f"  minimum C for this current to stay inside the 0.3 V droop limit: {I*W/0.3*1e12:.0f} pF")
        if a.cap_pf:
            t03 = 0.3 * a.cap_pf * 1e-12 / I
            print(f"  with C = {a.cap_pf:.0f} pF this current droops 0.3 V after {t03:.0f} s: set RECORD_S <= "
                  f"{min(t03, 1800):.0f}" + (" and use --skip-s 10 (record < 120 s)" if t03 < 120 else ""))
        return 0
    if not a.csv:
        ap.print_help()
        return 0
    recs = load_csv(a.csv)
    qs = tuple(float(x) for x in a.quantiles.split(","))
    res = analyze(recs, cap_pf=470.0, skip_s=a.skip_s, blank_name=a.blank_name, quantiles=qs,
                  boot=a.boot, cap_tempco_ppm=a.cap_tempco_ppm, cap_override=a.cap_pf)
    if a.json:
        def conv(o):
            if isinstance(o, dict):
                return {str(k): conv(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [conv(v) for v in o]
            if isinstance(o, (np.floating, np.integer)):
                return o.item()
            return o
        with open(a.json, "w") as fh:
            json.dump(conv(res), fh, indent=1)
        print(f"wrote {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
