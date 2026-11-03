#!/usr/bin/env python3
"""
ccd_cte.py -- analysis for home-lab experiment E5, "A charge river in a chip".

A bucket-brigade device (BBD) audio delay chip is a chain of MOS capacitors and switches that
passes charge packets from stage to stage on a two-phase clock. It is a "charge river" memory:
the bit is a packet that moves. This script measures how much of each packet is left behind
per transfer, using the same methods astronomers use on CCD cameras.

Physics (first principles)
--------------------------
Each transfer moves a fraction (1 - eps) of the packet forward and leaves eps behind; the
left-behind charge joins the NEXT packet. CTE = 1 - eps is the charge transfer efficiency.
After N transfers, a single injected packet is spread over the output samples k = 0, 1, 2, ...
as a negative-binomial distribution (charge is conserved, only delayed):

        h_k = C(N+k-1, k) * (1-eps)^N * eps^k

so   h_0 / sum(h) = (1-eps)^N ~ exp(-N eps)      (packet "survival")
     h_1 / h_0    = N eps                          (first trailing sample, "EPER"-style)
     |H(f)| = exp(-N eps (1 - cos(2 pi f / f_clk)))  (frequency response; -2 N eps nepers at Nyquist)

Your readout (output buffer, filters, scope bandwidth) adds its own smear r that does NOT grow
with N:  h_1/h_0 = eps * N + r.  Because r >= 0 for a low-pass readout, ONE chip already gives an
honest upper bound:  eps <= (h_1/h_0) / N  (valid when lead/main ~ 0 and no trailing sample is
negative). If two lengths share an IDENTICAL readout, the slope of h_1/h_0 against N is eps.
A series chain (two V3207s) adds a chip-to-chip interface smear r_if that one chip lacks, so its
slope is eps + r_if / 1024: again an upper bound, not a clean separation. A V3205SD is a
different chip with a different output stage: treat it as a separate chip, not a third length.

Retention (--retention): a CSV of hold_s,index,value (analog level of every bucket after the
clock was stopped for hold_s). The script splits the change since the shortest hold into a
common-mode drift (all '1' buckets, all '0' buckets) and a per-bucket residual; the residual is
the weak-bucket tail, I_excess = C_b * residual / hold.

Input formats
-------------
--samples CSV : one ADC/scope value per clock period, synchronised to the clock.
                columns: run, n_stages, f_clk_hz, index, value
                (optional: rep). Use --fold-period P if the pulse repeats every P samples
                (the companion MicroPython injects one pulse every 32 samples).
--scope CSV   : raw waveform, columns time_s, voltage[, clock]. With a clock column the script
                finds rising edges and samples at --phase of each period; without it you must
                give --fclk and --t0 (time of one rising clock edge). Give --nstages too.

Usage
-----
    python3 ccd_cte.py --selftest [--workdir DIR]
    python3 ccd_cte.py --expected
    python3 ccd_cte.py --samples runs.csv --fold-period 32 [--skip 1100]
    python3 ccd_cte.py --scope capture.csv --nstages 1024 --phase 0.25 --fold-period 32
    python3 ccd_cte.py --retention ret.csv [--cb-pf 1.4] [--adc-scale 1.682]

Dependencies: Python 3.9+ standard library + numpy. Exit 0 = success.
Author: dram-moonshot home-lab track T2. Written 2026-11-03.
"""

import argparse
import csv
import math
import os
import sys
import tempfile
from collections import defaultdict

import numpy as np

Q_E = 1.602176634e-19
KB_J = 1.380649e-23
KB_EV = 8.617333262e-5


# ---------------------------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------------------------
def nb_impulse(N, eps, K):
    """h_k for k = 0..K: fraction of one packet found k samples late after N transfers."""
    k = np.arange(K + 1, dtype=float)
    if eps <= 0:
        h = np.zeros(K + 1)
        h[0] = 1.0
        return h
    logh = (np.array([math.lgamma(N + x) for x in k]) - np.array([math.lgamma(x + 1) for x in k])
            - math.lgamma(N) + N * math.log1p(-eps) + k * math.log(eps))
    return np.exp(logh)


def readout_kernel(r):
    """Area-conserving two-tap readout smear: fraction r/(1+r) arrives one sample late."""
    return np.array([1.0, r]) / (1.0 + r)


# ---------------------------------------------------------------------------------------------
# Extraction from one run
# ---------------------------------------------------------------------------------------------
def fold(values, period, skip=0):
    v = np.asarray(values, dtype=float)[skip:]
    reps = len(v) // period
    if reps < 1:
        raise ValueError("not enough samples to fold")
    m = v[: reps * period].reshape(reps, period)
    return m.mean(axis=0), m.std(axis=0, ddof=1) / math.sqrt(reps) if reps > 1 else np.zeros(period), reps


def extract(values, n_stages, fold_period=None, skip=0, K=8, pre=8, se=None):
    """Return the measured impulse response h_k (k=-1..K) and three eps estimates."""
    if fold_period:
        mean, se_arr, reps = fold(values, fold_period, skip)
    else:
        mean = np.asarray(values, dtype=float)[skip:]
        se_arr, reps = None, 1
    P = len(mean)
    med = float(np.median(mean))
    dev = mean - med
    k0 = int(np.argmax(np.abs(dev)))
    sign = 1.0 if dev[k0] > 0 else -1.0
    base_idx = [(k0 - j) % P for j in range(2, 2 + pre)]
    if not fold_period:
        base_idx = [i for i in range(max(0, k0 - 2 - pre), max(0, k0 - 1))]
        if len(base_idx) < 3:
            raise ValueError("pulse too close to start of record for a baseline")
    baseline = float(np.median(mean[base_idx]))
    noise = float(np.std(mean[base_idx], ddof=1)) if len(base_idx) > 2 else float("nan")
    idx = [(k0 + k) % P for k in range(-1, K + 1)]
    h = sign * (mean[idx] - baseline)          # h[0] is k = -1 (lead), h[1] is k = 0 ...
    lead, main, trail = h[0], h[1], h[2:]
    total = main + trail.sum()
    r1 = trail[0] / main
    eps_r1 = r1 / n_stages
    eps_area = 1.0 - (main / total) ** (1.0 / n_stages)
    # Negative-binomial shape fit with a free readout tap (grid search, LS amplitude)
    eps_fit, r_fit = fit_nb_readout(np.concatenate([[main], trail]), n_stages)
    # simple uncertainty on r1 from baseline noise
    s = noise if math.isfinite(noise) else 0.0
    r1_se = math.sqrt((s / main) ** 2 + (r1 * s / main) ** 2) if main != 0 else float("nan")
    trail_min = float(np.min(trail[:3]) / main) if main != 0 else float("nan")
    tol = max(0.01, 3 * s / abs(main)) if main != 0 else 0.01
    bound_ok = bool(abs(lead / main) <= tol and trail_min >= -tol) if main != 0 else False
    return {"k0": k0, "sign": sign, "baseline": baseline, "noise_per_avg_sample": noise, "reps": reps,
            "trail_min_over_main": trail_min, "one_chip_bound_valid": bound_ok,
            "amplitude": main, "lead_over_main": lead / main, "h": (np.concatenate([[main], trail]) / main).tolist(),
            "r1": r1, "r1_se": r1_se, "eps_r1": eps_r1, "eps_area": eps_area,
            "eps_fit": eps_fit, "r_fit": r_fit, "survival": main / total}


def fit_nb_readout(h, N, eps_grid=None, r_grid=None):
    K = len(h) - 1
    eps_grid = eps_grid if eps_grid is not None else np.logspace(-7, -1.3, 260)
    r_grid = r_grid if r_grid is not None else np.linspace(0.0, 0.3, 61)
    best = (float("inf"), None, None)
    for e in eps_grid:
        base = nb_impulse(N, e, K + 1)
        for r in r_grid:
            y = np.convolve(base, readout_kernel(r))[: K + 1]
            a = float(np.dot(y, h) / np.dot(y, y))
            res = float(np.sum((h - a * y) ** 2))
            if res < best[0]:
                best = (res, float(e), float(r))
    return best[1], best[2]


def multi_length(results):
    """results: list of (N, r1, -ln survival). Linear fits vs N -> eps (slope), readout (intercept)."""
    N = np.array([x[0] for x in results], dtype=float)
    if len(set(N)) < 2:
        return None
    r1 = np.array([x[1] for x in results])
    ls = np.array([x[2] for x in results])
    m1, c1 = np.polyfit(N, r1, 1)
    m2, c2 = np.polyfit(N, ls, 1)
    return {"eps_from_trail_slope": float(m1), "readout_trail_intercept": float(c1),
            "eps_from_survival_slope": float(1 - math.exp(-m2)), "readout_survival_intercept": float(c2),
            "n_lengths": int(len(set(N)))}


# ---------------------------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------------------------
def load_samples(path):
    runs = defaultdict(lambda: {"N": None, "f": None, "idx": [], "val": []})
    with open(path, newline="") as fh:
        # skip the firmware's '#' status lines
        lines = [ln for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
    rd = csv.DictReader(lines)
    for row in rd:
        row = {k.strip().lower(): v for k, v in row.items() if k is not None}
        try:
            float(row.get("value", ""))
        except (TypeError, ValueError):
            continue                     # repeated header or malformed line
        key = row.get("run", "0")
        r = runs[key]
        r["N"] = int(float(row["n_stages"]))
        r["f"] = float(row["f_clk_hz"])
        r["idx"].append(int(float(row["index"])))
        r["val"].append(float(row["value"]))
    out = {}
    for k, r in runs.items():
        o = np.argsort(r["idx"])
        out[k] = {"N": r["N"], "f": r["f"], "val": np.asarray(r["val"])[o]}
    return out


def load_scope(path):
    t, v, c = [], [], []
    with open(path, newline="") as fh:
        lines = [ln for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
    rd = csv.reader(lines)
    header = [h.strip().lower() for h in next(rd)]
    it = header.index("time_s") if "time_s" in header else 0
    iv = header.index("voltage") if "voltage" in header else 1
    ic = header.index("clock") if "clock" in header else None
    for row in rd:
        if not row:
            continue
        try:
            float(row[it])
        except (ValueError, IndexError):
            continue
        t.append(float(row[it]))
        v.append(float(row[iv]))
        if ic is not None:
            c.append(float(row[ic]))
    return np.asarray(t), np.asarray(v), (np.asarray(c) if c else None)


def resample_scope(t, v, clock=None, fclk=None, t0=None, phase=0.25):
    """One value per clock period, taken at `phase` (0-1) after each rising clock edge."""
    if clock is not None:
        thr = 0.5 * (clock.min() + clock.max())
        hi = clock > thr
        edges_i = np.nonzero(~hi[:-1] & hi[1:])[0]
        # linear interpolation of the crossing time
        te = t[edges_i] + (thr - clock[edges_i]) / (clock[edges_i + 1] - clock[edges_i]) * (t[edges_i + 1] - t[edges_i])
        period = float(np.median(np.diff(te)))
    else:
        if fclk is None or t0 is None:
            raise ValueError("scope data without a clock column needs --fclk and --t0")
        period = 1.0 / fclk
        n0 = math.ceil((t[0] - t0) / period)
        n1 = math.floor((t[-1] - t0) / period) - 1
        te = t0 + period * np.arange(n0, n1 + 1)
    ts = te + phase * period
    ts = ts[ts < t[-1]]
    return np.interp(ts, t, v), 1.0 / period


# ---------------------------------------------------------------------------------------------
# Stopped-clock retention (analog levels)
# ---------------------------------------------------------------------------------------------
ADC_SCALE_DEFAULT = 37.0 / 22.0     # 15 kOhm over 22 kOhm divider: real OUT volts = ADC volts x 37/22
CB_PF_DEFAULT = 700.0 / 512         # <= 1.37 pF per bucket if C_clk <= 700 pF (upper bound)


def load_retention(path):
    data = defaultdict(dict)
    with open(path, newline="") as fh:
        lines = [ln for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
    rd = csv.DictReader(lines)
    for row in rd:
        row = {k.strip().lower(): v for k, v in row.items() if k is not None}
        try:
            h = float(row["hold_s"])
            i = int(float(row["index"]))
            v = float(row["value"])
        except (KeyError, TypeError, ValueError):
            continue                    # repeated header or malformed line
        data[h][i] = v
    holds = sorted(data)
    L = min(len(data[h]) for h in holds)
    return holds, {h: np.array([data[h][i] for i in sorted(data[h])[:L]]) for h in holds}


def analyze_retention(holds, vals, cb_pf=CB_PF_DEFAULT, adc_scale=ADC_SCALE_DEFAULT, verbose=True):
    """Split dV(hold) into a common-mode drift per written value and a per-bucket residual."""
    if len(holds) < 3:
        raise ValueError("need the reference hold plus >= 2 longer holds")
    ref = holds[0]
    v0 = vals[ref] * adc_scale
    lo, hi = np.quantile(v0, [0.1, 0.9])
    ones = v0 > 0.5 * (lo + hi)          # written value from the shortest hold
    later = holds[1:]
    dt = np.array([h - ref for h in later])
    cm1, cm0, resid = [], [], []
    for h in later:
        dv = vals[h] * adc_scale - v0
        c1 = float(np.median(dv[ones]))
        c0 = float(np.median(dv[~ones]))
        cm1.append(c1)
        cm0.append(c0)
        resid.append(dv - np.where(ones, c1, c0))
    resid = np.array(resid)              # shape (n_holds, L)
    # per-bucket excess leak: residual grows linearly with hold time -> fit through the origin
    slope = (dt[:, None] * resid).sum(axis=0) / float((dt ** 2).sum())
    I_ex = -cb_pf * 1e-12 * slope        # > 0: this bucket's voltage FELL faster than its group's
    # common mode = log-time drift (subthreshold transfer) + linear-in-time leak of a TYPICAL bucket
    A = np.vstack([np.log10(np.array(later) / ref), dt, np.ones_like(dt)]).T
    (s1, k1, _), *_ = np.linalg.lstsq(A, np.array(cm1), rcond=None)
    (s0, k0, _), *_ = np.linalg.lstsq(A, np.array(cm0), rcond=None)
    s1, s0, k1, k0 = float(s1), float(s0), float(k1), float(k0)
    order = np.argsort(-np.abs(I_ex))
    out = {"holds_s": later, "cm_ones_V": cm1, "cm_zeros_V": cm0,
           "cm_ones_V_per_decade": s1, "cm_zeros_V_per_decade": s0,
           "I_typical_ones_A": -cb_pf * 1e-12 * k1, "I_typical_zeros_A": -cb_pf * 1e-12 * k0,
           "I_excess_A": I_ex, "weakest": [int(i) for i in order[:5]], "n_ones": int(ones.sum()),
           "L": int(len(v0)), "cb_pf": cb_pf}
    if verbose:
        print("=" * 96)
        print("E5 STOPPED-CLOCK RETENTION (analog levels; real volts = ADC volts x %.3f)" % adc_scale)
        print("=" * 96)
        print(f"buckets: {out['L']}  ('1' written: {out['n_ones']})   reference hold: {ref} s   C_b = {cb_pf:.2f} pF")
        print(f"  {'hold (s)':>9s} {'common mode, 1s':>16s} {'common mode, 0s':>16s} {'resid spread (sd)':>18s}")
        for h, a, b, r in zip(later, cm1, cm0, resid):
            print(f"  {h:9.3g} {a*1e3:13.1f} mV {b*1e3:13.1f} mV {np.std(r)*1e3:15.2f} mV")
        print(f"  common mode = a x log10(hold) + b x hold: a = {s1*1e3:.1f} mV/decade ('1's), {s0*1e3:.1f} mV/decade ('0's);")
        print(f"  b gives the TYPICAL bucket's leak: {I_ex_fmt(out['I_typical_ones_A'])} ('1's),"
              f" {I_ex_fmt(out['I_typical_zeros_A'])} ('0's)")
        print("  -> a steady mV-per-decade drift of everything is subthreshold transfer / shared leakage, NOT weak")
        print("     buckets. With a fixed comparator threshold it makes a one-direction error cliff.")
        q = np.quantile(I_ex, [0.5, 0.9, 0.99])
        print(f"  per-bucket EXCESS leak I = C_b x residual / hold (within the output-stage gain, ~2x):")
        print(f"    median {I_ex_fmt(q[0])}, q0.9 {I_ex_fmt(q[1])}, q0.99 {I_ex_fmt(q[2])}, max {I_ex_fmt(I_ex.max())}")
        print("    weakest buckets (index: excess leak): " +
              ", ".join(f"{i}: {I_ex_fmt(I_ex[i])}" for i in out["weakest"]))
        print("  This residual is the weak-bucket tail: feed its values to E4's statistics if you like.")
    return out


def I_ex_fmt(x):
    a = abs(x)
    for unit, s in (("pA", 1e-12), ("fA", 1e-15), ("aA", 1e-18)):
        if a >= s or unit == "aA":
            return f"{x / s:.3g} {unit}"
    return f"{x:.3g} A"


# ---------------------------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------------------------
def report(runs_results, multi):
    print("=" * 96)
    print("E5 CHARGE-TRANSFER REPORT (negative-binomial deferred-charge model)")
    print("=" * 96)
    print(f"{'run':>8s} {'N':>6s} {'f_clk':>9s} {'reps':>5s} {'amp':>9s} {'lead/main':>10s} {'h1/h0':>9s}"
          f" {'eps<=h1/h0/N':>12s} {'bound':>6s} {'eps(area)':>11s} {'eps(fit)':>10s} {'r(fit)':>7s} {'CTE(fit)':>10s}")
    for name, N, f, r in runs_results:
        print(f"{name:>8s} {N:6d} {f:9.0f} {r['reps']:5d} {r['amplitude']*1e3:7.1f}mV {r['lead_over_main']:10.4f}"
              f" {r['r1']:9.4f} {r['eps_r1']:12.3e} {'OK' if r['one_chip_bound_valid'] else 'CHECK':>6s}"
              f" {r['eps_area']:11.3e} {r['eps_fit']:10.3e} {r['r_fit']:7.3f} {1-r['eps_fit']:10.6f}")
    print("  lead/main should be ~0. If not, your sampling phase is wrong or the readout rings.")
    print("  eps <= (h1/h0)/N is an UPPER BOUND on eps from one chip: readout smear only ADDS to h1/h0. It holds")
    print("  when lead/main ~ 0 and no trailing sample is negative ('bound OK'). eps(area) also includes smear.")
    for f, m in multi.items():
        if m is None:
            print(f"f_clk = {f:.0f} Hz: one length only -> quote the one-chip bound eps <= (h1/h0)/N above")
            continue
        print(f"f_clk = {f:.0f} Hz, {m['n_lengths']} lengths: slope = {m['eps_from_trail_slope']:.3e} (trail),"
              f" {m['eps_from_survival_slope']:.3e} (survival); intercept = {m['readout_trail_intercept']:.4f}")
        print("   The multi-length slope equals eps only if every length has the SAME readout. A series chain adds a")
        print("   chip-to-chip interface smear r_if, so the slope is eps + r_if/N_chip: an UPPER bound on eps.")
        e = m["eps_from_trail_slope"]
        print(f"   -> CTE >= {1-e:.6f}. Charge-river GO needs >= 0.9970 (DFE); STRONG GO >= 0.999 (study dossier).")


# ---------------------------------------------------------------------------------------------
# First-principles expectations
# ---------------------------------------------------------------------------------------------
def qfunc(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def expected():
    print("=" * 96)
    print("E5 FIRST-PRINCIPLES NUMBERS (all [ESTIMATE] unless the input is tagged)")
    print("=" * 96)
    print("\n1) What a given per-transfer loss eps does to a single packet after N transfers")
    print(f"  {'eps':>8s} {'CTE':>9s} | " + " | ".join(f"N={N}: surv, h1/h0, Nyq dB" for N in (1024, 2048, 4096)))
    for eps in (3e-5, 1e-4, 3e-4, 1e-3):
        cells = []
        for N in (1024, 2048, 4096):
            s = (1 - eps) ** N
            nyq_db = 20 * math.log10(math.exp(-2 * N * eps))
            cells.append(f"{s:5.3f}, {N*eps:5.3f}, {nyq_db:6.2f}")
        print(f"  {eps:8.0e} {1-eps:9.5f} | " + " | ".join(f"{c:>24s}" for c in cells))
    print("  Audio BBDs pass usable treble to near f_clk/3 at 1024-4096 stages, which suggests eps of order")
    print("  1e-4 or below [ESTIMATE; no per-stage figure was verified]. Your measurement replaces this guess.")

    print("\n2) The study's charge-river bar (dossiers/charge-river.md):")
    for name, cte, n in (("GO floor with DFE", 0.9970, 98), ("STRONG GO", 0.999, 98),
                         ("one-way 64-stage fallback", 0.9987, 194), ("imec '>98%' read as PER transfer", 0.98, 98)):
        print(f"  {name:36s} CTE {cte:.4f} over {n:3d} transfers -> packet survival {cte**n:.3f}")
    print(f"  worst string (k_ws = 1.5) at 0.997: (1 - 1.5*0.003)^98 = {(1-0.0045)**98:.3f} (dossier: ~65%)")
    print(f"  imec '>98%' read as END-TO-END over 142 bits x 4 phases = 568 transfers -> eps <= {1-0.98**(1/568):.1e}"
          f" per transfer (dossier: 0.99996)")
    print("  A home BBD at eps ~1e-4 would beat the GO bar by ~30x: crystalline-silicon charge transfer is not")
    print("  the hard part. The open question is deposited OXIDE channels with traps, at 50 MHz, with 313 e-.")

    print("\n3) How big is a BBD bucket? (from the clock-pin capacitance)")
    c_clk = 700e-12   # MN3007 clock input capacitance, max [REPORTED, Xvive listing]; V3207: not found
    cb = c_clk / 512
    print(f"  V3207 clock input capacitance: NOT FOUND [UNVERIFIED]. The 15 V MN3007 is <= 700 pF [REPORTED]")
    print(f"  -> <= {cb*1e12:.2f} pF per bucket over 512 buckets per phase: an UPPER bound for the V3207.")
    print("  Measure C_clk yourself (step 18); bucket ~ C_clk/512 (still an upper bound: the line also drives gates).")
    print(f"  {'C_clk':>8s} {'bucket':>9s} {'packet at 0.3 V':>16s} {'kT/C noise (300 K)':>22s}")
    for cc in (700e-12, 300e-12, 150e-12, 51.2e-12):
        b = cc / 512
        print(f"  {cc*1e12:6.0f}pF {b*1e12:7.2f}pF {b*0.3/Q_E:13,.0f} e- {math.sqrt(KB_J*300/b)*1e6:8.0f} uV ="
              f" {math.sqrt(KB_J*300*b)/Q_E:4.0f} e-")
    c313 = (313 * Q_E) ** 2 / (KB_J * 300)
    print(f"  kT/C noise equals the whole 313-electron charge-river packet when the bucket is {c313*1e12:.2f} pF.")
    print("  Either way the home packet is >= ~190,000 electrons (600x the study's): a BBD cannot test few-electron")
    print("  physics. charge-river packet: ~313 e-; imec vertical IGZO CCD: 'a few thousand' [REPORTED in dossier]")

    print("\n4) Stopped-clock retention: a BBD bucket is a DRAM-like capacitor + switch")
    # Assume the 10 kHz minimum clock keeps leakage drift below ~10 mV over the 51.2 ms delay
    t_delay = 1024 / (2 * 10e3)
    i_max = cb * 0.010 / t_delay
    print(f"  Datasheet minimum clock 10 kHz -> 51.2 ms delay [DATASHEET V3207]. If designers allow <= 10 mV of")
    print(f"  leakage drift in that time, bucket leakage <= {i_max*1e15:.0f} fA [ESTIMATE].")
    for I in (i_max, 30e-15, 3e-15):
        t25 = cb * 0.150 / I
        f60 = math.exp(0.6 / KB_EV * (1 / 298.15 - 1 / 333.15))
        print(f"  leak {I*1e15:6.0f} fA, 150 mV margin: retention {t25:7.2f} s at 25 C, {t25/f60:7.3f} s at 60 C (Ea 0.6 eV)")
    print("  (The 0.77 s bound does not depend on the bucket size: C_b cancels. The 30 fA and 3 fA rows assume")
    print(f"  {cb*1e12:.2f} pF and scale with C_b.)")
    print("  This t = C dV / I counts junction leakage only. A stopped BBD also drifts in COMMON MODE: the transfer")
    print("  transistors on the frozen phase sit at their source-follower cutoff and keep conducting slightly")
    print("  (subthreshold), so every bucket moves together, roughly in proportion to log(hold time) [ESTIMATE].")
    print("  With a fixed comparator threshold that shows up as a one-direction error CLIFF, not a weak-cell tail.")
    print("  -> expect retention of order 0.1-100 s at room temperature: the same 'seconds' scale as DRAM cells.")

    print("\n5) Energy: moving charge costs C V^2 per clock edge pair")
    print("  Values below assume C_clk = 700 pF (MN3007 max): they are UPPER bounds; scale linearly with your C_clk.")
    for v, c, f, name in ((5.0, 700e-12, 10e3, "V3207-class at 5 V (C assumed = MN3007 max)"),
                          (15.0, 700e-12, 10e3, "MN3007 at 15 V")):
        p = 2 * c * v * v * f
        e_cycle = 2 * c * v * v
        per_transfer = e_cycle / 1024          # 512 packets x 2 stages per cycle
        print(f"  {name:44s}: clock power {p*1e3:5.2f} mW at {f/1e3:.0f} kHz,"
              f" {p/512*1e6:5.2f} uW per stored bit, {per_transfer*1e12:5.1f} pJ per packet-transfer")
    dram = 46e-15 / 0.064
    print(f"  DRAM refresh: 46 fJ/bit per 64 ms [study, charge-river dossier] = {dram*1e12:.2f} pW per stored bit")
    print(f"  charge-river design: 45 fJ per bit read over 98 transfers = {45e-15/98*1e15:.2f} fJ per transfer")
    print(f"  -> a BBD loop spends ~{(2*700e-12*25*10e3/512)/dram:.0e}x DRAM's standby power per bit; per transfer it is")
    print(f"     ~{(2*700e-12*25/1024)/(45e-15/98):.0e}x the charge-river target. Energy scales with C V^2: fF buckets, ~1 V.")

    print("\n6) Delay-line memory: with and without regeneration")
    for N, eps in ((1024, 1e-4), (4096, 1e-4), (1024, 1e-3)):
        laps = math.log(2) / (-N * math.log1p(-eps))
        print(f"  N={N}, eps={eps:.0e}: analog recirculation (no regeneration) closes the worst-case eye after"
              f" ~{laps:.1f} laps = {laps*N/2/10e3:.2f} s at 10 kHz")
    print("  (worst-case eye = 2*(1-eps)^(N*laps) - 1; any loop-gain error g != 1 makes it worse, as g^laps)")
    A, sigma = 0.3, 0.001
    for N, eps in ((1024, 1e-4), (4096, 1e-4)):
        h0 = (1 - eps) ** N
        eye = A * (2 * h0 - 1)
        p = qfunc(eye / 2 / sigma)
        ptxt = f"{p:.1e}" if p > 0 else "< 1e-300"
        print(f"  WITH regeneration, N={N}: one-pass eye {eye*1e3:.0f} mV, noise {sigma*1e3:.0f} mV rms -> Gaussian BER {ptxt}"
              " (i.e. ~0: errors will come from glitches, timing and drift, not from thermal noise)")
    print("  EDSAC (1949) stored 576 bits per mercury tank, 32 tanks, kept alive the same way [REPORTED].")
    print("  One V3207 loop stores 512 bits; at 10 kHz a lap takes 51.2 ms.")
    print()


# ---------------------------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------------------------
def synth_stream(N, eps, r_ro, f, rng, A=0.3, base=2.5, sigma=1e-3, period=32, reps=64, fill=None):
    """Sampled output stream: one pulse every `period` samples, convolved with BBD + readout."""
    fill = N // 2 if fill is None else fill
    n = fill + period * reps
    x = np.zeros(n + 64)
    x[np.arange(0, n + 64, period)] = A
    h = nb_impulse(N, eps, 40)
    y = np.convolve(x, h)[: len(x)]
    y = np.convolve(y, readout_kernel(r_ro))[: len(x)]
    y = base + y[:n] + sigma * rng.standard_normal(n)
    return y


def synth_retention(path, rng, L=512, cb=1.37e-12, scale=ADC_SCALE_DEFAULT):
    """hold_s,index,value file as mode 'retention_analog' prints it (ADC volts, 12-bit steps)."""
    bits = rng.integers(0, 2, L)
    v_real = np.where(bits == 1, 2.58, 2.25) + 0.005 * rng.standard_normal(L)   # fixed pattern per bucket
    I = np.exp(np.log(0.2e-15) + 0.7 * rng.standard_normal(L))     # 0.2 fA x 100 s / 1.37 pF = 15 mV
    weak = [int(i) for i in rng.choice(L, 3, replace=False)]
    I[weak] = 2e-15                                                # weak buckets: 146 mV in 100 s
    holds = (0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30, 100)
    lsb = 3.3 / 4096
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["hold_s", "index", "value"])
        for h in holds:
            dec = math.log10(h / 0.01)
            cm = np.where(bits == 1, -0.025, -0.020) * dec
            v = v_real + cm - I * (h - 0.01) / cb + 0.001 * rng.standard_normal(L)
            adc = np.round(v / scale / lsb) * lsb
            for i in range(L):
                w.writerow([f"{h:.3f}", i, f"{adc[i]:.6f}"])
    return weak


def selftest(workdir=None):
    ok = True
    rng = np.random.default_rng(5)
    print("SELFTEST 1: negative-binomial model sums to 1 and has h1/h0 = N eps")
    h = nb_impulse(1024, 1e-4, 60)
    print(f"  sum = {h.sum():.6f}, h1/h0 = {h[1]/h[0]:.6f} (expect 0.102400)")
    ok &= abs(h.sum() - 1) < 1e-6 and abs(h[1] / h[0] - 0.1024) < 1e-9

    print("SELFTEST 2: shape fit recovers eps on a noiseless impulse (N=2048, eps=2e-4, readout r=0.05)")
    hh = np.convolve(nb_impulse(2048, 2e-4, 12), readout_kernel(0.05))[:9]
    e, r = fit_nb_readout(hh / hh[0], 2048)
    print(f"  fit eps = {e:.3e}, r = {r:.3f}")
    ok &= abs(e / 2e-4 - 1) < 0.05 and abs(r - 0.05) < 0.006

    print("SELFTEST 3: synthetic sampled runs, eps_true = 1.0e-4, readout smear 0.03, 1 mV noise, 64 reps")
    workdir = workdir or tempfile.mkdtemp(prefix="T2_cte_")
    os.makedirs(workdir, exist_ok=True)
    path = os.path.join(workdir, "T2_cte_synthetic_samples.csv")
    eps_true, r_true = 1.0e-4, 0.03
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["run", "n_stages", "f_clk_hz", "index", "value"])
        for name, N, f, eps in (("A1024", 1024, 10e3, eps_true), ("B2048", 2048, 10e3, eps_true),
                                ("C4096", 4096, 10e3, eps_true),
                                ("D1024_50k", 1024, 50e3, 3e-4), ("E2048_50k", 2048, 50e3, 3e-4)):
            y = synth_stream(N, eps, r_true, f, rng)
            for i, val in enumerate(y):
                w.writerow([name, N, int(f), i, f"{val:.6f}"])
    print(f"  wrote {path}")
    res = run_samples(path, fold_period=32, skip=None)
    m10 = res[10000.0]
    print(f"  multi-length eps at 10 kHz = {m10['eps_from_trail_slope']:.3e} (true {eps_true:.1e})")
    ok &= abs(m10["eps_from_trail_slope"] / eps_true - 1) < 0.15
    ok &= abs(m10["readout_trail_intercept"] - r_true) < 0.01
    m50 = res[50000.0]
    print(f"  multi-length eps at 50 kHz = {m50['eps_from_trail_slope']:.3e} (true 3.0e-04)")
    ok &= abs(m50["eps_from_trail_slope"] / 3e-4 - 1) < 0.15

    print("SELFTEST 4: scope-format waveform (50 points/period, clock column, edge spikes) -> resample -> same answer")
    N, f = 1024, 10e3
    y = synth_stream(N, eps_true, r_true, f, rng, reps=48)
    spp = 50
    period = 1 / f
    t = np.arange(len(y) * spp) * (period / spp)
    j = np.arange(len(t)) // spp
    ph = (np.arange(len(t)) % spp) / spp
    v = y[j] + 0.004 * np.exp(-ph / 0.03) + 0.004 * np.exp(-np.clip(ph - 0.5, 0, None) / 0.03) * (ph >= 0.5)
    v += 0.0005 * rng.standard_normal(len(t))
    clk = np.where(ph < 0.5, 3.3, 0.0)
    clk = np.roll(clk, -1)          # rising edge one point before each period starts
    spath = os.path.join(workdir, "T2_cte_synthetic_scope.csv")
    with open(spath, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["time_s", "voltage", "clock"])
        for row in zip(t, v, clk):
            w.writerow([f"{row[0]:.8e}", f"{row[1]:.6f}", f"{row[2]:.2f}"])
    tt, vv, cc = load_scope(spath)
    vals, f_est = resample_scope(tt, vv, clock=cc, phase=0.25)
    r = extract(vals, N, fold_period=32, skip=N // 2 + 8)
    direct = extract(y, N, fold_period=32, skip=N // 2)
    print(f"  clock recovered {f_est:.1f} Hz; h1/h0 scope {r['r1']:.4f} vs direct samples {direct['r1']:.4f}"
          f" (true N eps + r = {N*eps_true + r_true:.4f})")
    ok &= abs(r["r1"] - (N * eps_true + r_true)) < 0.01 and abs(f_est - f) < 1

    print("SELFTEST 5: loop arithmetic, laps to close the eye without regeneration = ln2 / (N eps)")
    laps = math.log(2) / (-1024 * math.log1p(-1e-4))
    print(f"  N=1024, eps=1e-4: {laps:.2f} laps")
    ok &= abs(laps - 6.77) < 0.02

    print("SELFTEST 6: stopped-clock retention: -25/-20 mV/decade common-mode drift, typical leak 0.2 fA,"
          " 3 weak buckets at 2 fA")
    rpath = os.path.join(workdir, "T2_retention_synthetic.csv")
    weak_true = synth_retention(rpath, rng)
    holds, vals = load_retention(rpath)
    rr = analyze_retention(holds, vals, cb_pf=1.37, verbose=True)
    print(f"  common mode recovered: {rr['cm_ones_V_per_decade']*1e3:.1f} / {rr['cm_zeros_V_per_decade']*1e3:.1f}"
          f" mV/decade (true -25 / -20); weakest 3 = {sorted(rr['weakest'][:3])} (true {sorted(weak_true)})")
    ok &= abs(rr["cm_ones_V_per_decade"] / -0.025 - 1) < 0.1 and abs(rr["cm_zeros_V_per_decade"] / -0.020 - 1) < 0.1
    ok &= sorted(rr["weakest"][:3]) == sorted(weak_true)
    print(f"  weak-bucket excess leak: {', '.join(I_ex_fmt(rr['I_excess_A'][i]) for i in weak_true)}"
          f" (true 2 fA minus the group median ~0.2 fA)")
    ok &= all(abs(rr["I_excess_A"][i] / 1.8e-15 - 1) < 0.15 for i in weak_true)
    print("SELFTEST", "PASS" if ok else "FAIL")
    return ok


def run_samples(path, fold_period=None, skip=None, K=8, verbose=True):
    runs = load_samples(path)
    rows, by_f = [], defaultdict(list)
    for name, r in sorted(runs.items()):
        sk = (r["N"] // 2 + 8) if skip is None else skip
        res = extract(r["val"], r["N"], fold_period=fold_period, skip=sk, K=K)
        rows.append((name, r["N"], r["f"], res))
        by_f[r["f"]].append((r["N"], res["r1"], -math.log(res["survival"])))
    multi = {f: multi_length(v) for f, v in by_f.items()}
    if verbose:
        report(rows, multi)
    return multi


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--samples", help="CSV: run,n_stages,f_clk_hz,index,value")
    ap.add_argument("--scope", help="CSV: time_s,voltage[,clock]")
    ap.add_argument("--nstages", type=int, help="stages for --scope data")
    ap.add_argument("--fclk", type=float, help="clock frequency for --scope data without a clock column")
    ap.add_argument("--t0", type=float, help="time of one rising clock edge (--scope without clock column)")
    ap.add_argument("--phase", type=float, default=0.25, help="sampling point within each clock period (0-1)")
    ap.add_argument("--fold-period", type=int, default=None, help="pulse repeat period in samples (e.g. 32)")
    ap.add_argument("--skip", type=int, default=None, help="samples to drop at the start (default N/2+8: line fill)")
    ap.add_argument("--trail", type=int, default=8, help="trailing samples to analyse")
    ap.add_argument("--retention", help="CSV: hold_s,index,value (firmware mode retention_analog)")
    ap.add_argument("--cb-pf", type=float, default=CB_PF_DEFAULT,
                    help="bucket capacitance in pF (default 700/512 = 1.37, an upper bound; use C_clk/512)")
    ap.add_argument("--adc-scale", type=float, default=ADC_SCALE_DEFAULT,
                    help="real OUT volts per ADC volt (15k/22k divider: 37/22 = 1.682)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--workdir")
    ap.add_argument("--expected", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return 0 if selftest(a.workdir) else 1
    if a.expected:
        expected()
        return 0
    if a.samples:
        run_samples(a.samples, fold_period=a.fold_period, skip=a.skip, K=a.trail)
        return 0
    if a.retention:
        holds, vals = load_retention(a.retention)
        analyze_retention(holds, vals, cb_pf=a.cb_pf, adc_scale=a.adc_scale)
        return 0
    if a.scope:
        if not a.nstages:
            ap.error("--scope needs --nstages")
        t, v, c = load_scope(a.scope)
        vals, f = resample_scope(t, v, clock=c, fclk=a.fclk, t0=a.t0, phase=a.phase)
        sk = a.skip if a.skip is not None else 0
        r = extract(vals, a.nstages, fold_period=a.fold_period, skip=sk, K=a.trail)
        report([("scope", a.nstages, f, r)], {f: None})
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
