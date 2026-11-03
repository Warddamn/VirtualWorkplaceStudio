#!/usr/bin/env python3
"""
iv_analysis.py -- extract transistor parameters from home-made oxide TFT (thin-film transistor)
curves. Track T4 (E7/E8), dram-moonshot home lab. Python 3 + numpy only.

What it extracts
  Transfer curve (Id vs Vg at fixed Vd):
    Ion, Ioff, on/off ratio, turn-on voltage Von, subthreshold swing SS (V/decade),
    threshold voltage Vth and saturation mobility (sqrt(Id) method)  or  linear mobility
    (max transconductance, ELR method), hysteresis (forward vs reverse sweep), trap density
    implied by SS, off-current per um of width, gate-leakage sanity check (needs --gleak: the
    rig has one ammeter on the source, so gate current is measured in a separate gleak.csv run).
  Output curves (Id vs Vd at several Vg): saturation quality and a contact-barrier warning
    (S-shaped start = Schottky-like contacts).

Physics used (gradual-channel / square law):
  saturation  Id = (W/2L) * mu * Cox * (Vg - Vth)^2   ->  mu_sat = 2 L m^2 / (W Cox),  m = d sqrt(Id)/dVg
  linear      Id = (W/L)  * mu * Cox * (Vg - Vth - Vd/2) * Vd  ->  mu_lin = L gm_max / (W Cox Vd)
  subthreshold SS = dVg / dlog10(Id) >= ln(10) kT/q (59.2 mV/dec at 25 C)

Input: CSV with a header row. Recognised column names (case-insensitive):
  vg | vgs   gate-source voltage (V)        vd | vds   drain-source voltage (V)
  id | ids   drain current (A)              ig | igs   gate current (A, optional)
  dir        'f'/'r' sweep direction (optional; otherwise split at the maximum Vg)
Lines starting with '#' are ignored. pico_smu.py writes this format (extra columns such as mode,
range and t_s are ignored). A gate-leakage file from pico_smu.py 'gleak' has vgs and ig columns
(no id); pass it with --gleak, not as the main CSV.

Usage
  python3 iv_analysis.py transfer my_transfer.csv --W 1000 --L 10 --tox-nm 300 [--vd 20]
          [--gleak gleak.csv] [--regime auto|sat|lin] [--voff 0] [--json out.json] [--svg out.svg]
  python3 iv_analysis.py output my_output.csv --W 1000 --L 10
  python3 iv_analysis.py --selftest        (synthetic TFT curves; exit 0 on pass)
"""

import argparse
import json
import math
import os
import sys
import tempfile

import numpy as np

Q = 1.602176634e-19
KB_EV = 8.617333262e-5
EPS0 = 8.8541878128e-12

ALIASES = {
    "vg": ("vg", "vgs", "v_g", "vgate"),
    "vd": ("vd", "vds", "v_d", "vdrain"),
    "id": ("id", "ids", "i_d", "idrain"),
    "ig": ("ig", "igs", "i_g", "igate"),
    "dir": ("dir", "direction", "sweep"),
}


# ------------------------------------------------------------------------------------------
# I/O
# ------------------------------------------------------------------------------------------
def load_csv(path):
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.lstrip().startswith("#")]
    if not lines:
        raise ValueError(f"{path}: no data")
    header = [h.strip().lower() for h in lines[0].split(",")]
    cols = {}
    for key, names in ALIASES.items():
        for n in names:
            if n in header:
                cols[key] = header.index(n)
                break
    if "vg" not in cols or "id" not in cols:
        hint = ""
        if "vg" in cols and "ig" in cols:
            hint = (" -- this looks like a gate-leakage (gleak) file: pass it with --gleak next to a "
                    "transfer CSV, e.g. transfer transfer_sat.csv --gleak gleak.csv")
        raise ValueError(f"{path}: need at least vg and id columns, got {header}{hint}")
    data = {k: [] for k in cols}
    for ln in lines[1:]:
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) < len(header):
            continue
        for k, i in cols.items():
            data[k].append(parts[i])
    out = {}
    for k, v in data.items():
        if k == "dir":
            out[k] = np.array([s[:1].lower() for s in v])
        else:
            out[k] = np.array([float(s) for s in v])
    return out


def load_gleak(path):
    """Gate-leakage file (pico_smu.py 'gleak': mode,dir,vgs,vds,ig,range,t_s). Returns vg, |ig|
    sorted by vg, averaging repeated gate voltages."""
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.lstrip().startswith("#")]
    if not lines:
        raise ValueError(f"{path}: no data")
    header = [h.strip().lower() for h in lines[0].split(",")]
    iv = next((header.index(n) for n in ALIASES["vg"] if n in header), None)
    ii = next((header.index(n) for n in ALIASES["ig"] if n in header), None)
    if iv is None or ii is None:
        raise ValueError(f"{path}: a gleak file needs vg (or vgs) and ig columns, got {header}")
    vg, ig = [], []
    for ln in lines[1:]:
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) < len(header):
            continue
        vg.append(float(parts[iv]))
        ig.append(abs(float(parts[ii])))
    vg, ig = np.array(vg), np.array(ig)
    ux = np.unique(np.round(vg, 3))
    um = np.array([ig[np.round(vg, 3) == x].mean() for x in ux])
    if len(ux) < 2:
        raise ValueError(f"{path}: need at least two gate voltages")
    return {"vg": ux, "ig": um}


def attach_gleak(d, g):
    """Put the gate current from a gleak run onto the transfer curve's Vg grid (|ig|)."""
    d = dict(d)
    d["ig"] = np.interp(d["vg"], g["vg"], g["ig"])
    return d


def write_csv(path, d, keys):
    with open(path, "w") as f:
        f.write(",".join(keys) + "\n")
        n = len(d[keys[0]])
        for i in range(n):
            row = []
            for k in keys:
                val = d[k][i]
                row.append(val if isinstance(val, str) else f"{val:.6e}")
            f.write(",".join(row) + "\n")


def cox_F_cm2(tox_nm, eps_r):
    return eps_r * EPS0 / (tox_nm * 1e-9) / 1e4


# ------------------------------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------------------------------
def split_sweeps(d):
    vg = d["vg"]
    if "dir" in d:
        f = d["dir"] == "f"
        r = d["dir"] == "r"
        return np.where(f)[0], np.where(r)[0]
    imax = int(np.argmax(vg))
    fwd = np.arange(0, imax + 1)
    rev = np.arange(imax, len(vg)) if len(vg) - imax >= 4 else np.array([], dtype=int)
    return fwd, rev


def linfit(x, y):
    a = np.vstack([x, np.ones_like(x)]).T
    (m, b), *_ = np.linalg.lstsq(a, y, rcond=None)
    return float(m), float(b)


def crossing(x, y, level, rising=True):
    """First x where y crosses level (linear interpolation). y is assumed ordered along x."""
    for i in range(len(y) - 1):
        y0, y1 = y[i], y[i + 1]
        if rising and y0 < level <= y1 or (not rising) and y0 >= level > y1:
            if y1 == y0:
                return float(x[i])
            return float(x[i] + (level - y0) * (x[i + 1] - x[i]) / (y1 - y0))
    return None


def subthreshold_swing(vg, i, ilo, ihi):
    """Minimum V/decade from least-squares fits over sliding one-decade windows."""
    lg = np.log10(np.clip(i, 1e-30, None))
    best = None
    n = len(vg)
    for s in range(n):
        if not (ilo < i[s] < ihi):
            continue
        for e in range(s + 2, n):
            if i[e] >= ihi:
                break
            if lg[e] - lg[s] >= 1.0:
                m, _ = linfit(lg[s:e + 1], vg[s:e + 1])   # V per decade
                if m > 0 and (best is None or m < best):
                    best = m
                break
    return best


# ------------------------------------------------------------------------------------------
# transfer analysis
# ------------------------------------------------------------------------------------------
def analyze_transfer(d, W_um, L_um, tox_nm=300.0, eps_r=3.9, vd=None, regime="auto",
                     voff=None, temp_c=25.0):
    rep = {"warnings": []}
    cox = cox_F_cm2(tox_nm, eps_r)
    fwd, rev = split_sweeps(d)
    vg_f = d["vg"][fwd]
    order = np.argsort(vg_f, kind="stable")
    vg_f = vg_f[order]
    i_f = np.abs(d["id"][fwd])[order]
    if vd is None:
        vd = float(np.median(np.abs(d["vd"][fwd]))) if "vd" in d else None
    if vd is None:
        raise ValueError("drain voltage unknown: add a vd column or pass --vd")
    rep["vd_V"] = vd
    ion = float(np.max(i_f))
    if voff is not None:
        ioff = float(10 ** np.interp(voff, vg_f, np.log10(np.clip(i_f, 1e-30, None))))
    else:
        k = max(3, len(i_f) // 10)
        ioff = float(np.median(np.sort(i_f)[:k]))
    rep.update(Ion_A=ion, Ioff_A=ioff, on_off=ion / max(ioff, 1e-30),
               Ioff_per_um_A=ioff / W_um, Cox_F_cm2=cox)
    # turn-on voltage: first Vg where I > 10*Ioff and the next two points too
    von = None
    for j in range(len(i_f) - 2):
        if i_f[j] > 10 * ioff and i_f[j + 1] > 10 * ioff and i_f[j + 2] > 10 * ioff:
            von = float(vg_f[j])
            break
    rep["Von_V"] = von
    ss = subthreshold_swing(vg_f, i_f, 3 * ioff, 0.3 * ion)
    rep["SS_V_per_dec"] = ss
    if ss is not None:
        ss_ideal = math.log(10) * KB_EV * (temp_c + 273.15)
        rep["Dit_cm2_eV"] = max(0.0, (ss / ss_ideal - 1) * cox / Q)
    # regime
    if regime == "auto":
        span = float(vg_f[-1] - (von if von is not None else vg_f[0]))
        regime = "sat" if vd >= 0.5 * span else "lin"
    rep["regime"] = regime
    if regime == "sat":
        sq = np.sqrt(i_f)
        top = sq.max()
        sel = np.where((sq > 0.2 * top) & (sq < 0.95 * top))[0]
        if len(sel) < 4:
            sel = np.where(sq > 0.1 * top)[0]
        dv = float(np.median(np.diff(vg_f))) if len(vg_f) > 1 else 1.0
        w = max(4, len(sel) // 3, int(round(4.0 / max(dv, 1e-6))))   # >= ~4 V wide: averages noise
        w = min(w, len(sel))
        best = None
        for s in range(0, len(sel) - w + 1):
            idx = sel[s:s + w]
            m, b = linfit(vg_f[idx], sq[idx])
            if best is None or m > best[0]:
                best = (m, b, idx)
        m, b, idx = best
        vth = -b / m
        mu = 2 * L_um * m * m / (W_um * cox)
        rep.update(Vth_V=vth, mu_cm2_Vs=mu, fit_window_V=[float(vg_f[idx[0]]), float(vg_f[idx[-1]])])
        if vd < vg_f[idx[-1]] - vth:
            rep["warnings"].append(
                f"Vd={vd:.2f} V < Vg-Vth={vg_f[idx[-1]] - vth:.2f} V at the top of the fit: not fully "
                "saturated; mobility is underestimated. Raise Vd or use --regime lin with small Vd.")
    else:
        # transconductance from straight-line fits over >= ~5 V windows (point derivatives are noisy)
        dv = float(np.median(np.diff(vg_f))) if len(vg_f) > 1 else 1.0
        w = max(5, int(round(5.0 / max(dv, 1e-6))))
        w = min(w, len(vg_f))
        best = None
        for s in range(0, len(vg_f) - w + 1):
            m, b = linfit(vg_f[s:s + w], i_f[s:s + w])
            if best is None or m > best[0]:
                best = (m, b)
        gmax, b = best
        vth = float(-b / gmax - vd / 2)          # extrapolation in the linear region (ELR)
        mu = L_um * gmax / (W_um * cox * vd)
        rep.update(Vth_V=vth, mu_cm2_Vs=mu, gm_max_S=gmax)
    # hysteresis
    if len(rev) >= 4:
        vg_r = d["vg"][rev]
        i_r = np.abs(d["id"][rev])
        iref = math.sqrt(ion * max(ioff, 1e-30))
        lf = np.log10(np.clip(i_f, 1e-30, None))
        v_f = crossing(vg_f, lf, math.log10(iref), rising=True)
        o = np.argsort(vg_r)[::-1]            # reverse sweep runs from high Vg down
        v_r = crossing(vg_r[o], np.log10(np.clip(i_r[o], 1e-30, None)), math.log10(iref), rising=False)
        if v_f is not None and v_r is not None:
            rep["hysteresis_V"] = v_r - v_f
            rep["hysteresis_at_A"] = iref
    # gate leakage sanity check
    if "ig" in d:
        ig_f = np.abs(d["ig"][fwd])[order]
        off_region = i_f < 3 * ioff
        ig_off = float(np.max(ig_f[off_region])) if off_region.any() else float(np.max(ig_f))
        ig_max = float(np.max(ig_f))
        rep.update(Ig_off_region_A=ig_off, Ig_max_A=ig_max)
        if ig_off > 0.3 * ioff:
            rep["warnings"].append(
                f"Gate current in the off region ({ig_off:.1e} A) is comparable to Ioff ({ioff:.1e} A): "
                "your 'off-current' may be gate leakage. Check oxide damage, scratches, probe punch-through.")
        if ig_max > 0.01 * ion:
            rep["warnings"].append(f"Gate current {ig_max:.1e} A exceeds 1% of Ion: leaky gate oxide.")
    else:
        rep["warnings"].append("Gate leakage NOT checked: no ig data. Run pico_smu 'gleak' and pass "
                               "the file with --gleak gleak.csv (required for the PASS grade).")
    if rep.get("mu_cm2_Vs", 0) > 10:
        rep["warnings"].append("Mobility > 10 cm2/Vs for a home ZnO film is suspicious: unisolated film "
                               "makes the real width larger than W (fringe current). Scribe a moat and re-measure.")
    return rep


# ------------------------------------------------------------------------------------------
# output-curve analysis
# ------------------------------------------------------------------------------------------
def analyze_output(d, W_um, L_um):
    if "vd" not in d:
        raise ValueError("output analysis needs a vd column")
    vgs = np.round(d["vg"], 2)
    rep = {"curves": [], "warnings": []}
    for v in sorted(set(vgs.tolist())):
        sel = vgs == v
        vd = np.abs(d["vd"][sel])
        i = np.abs(d["id"][sel])
        o = np.argsort(vd)
        vd, i = vd[o], i[o]
        if len(vd) < 8 or vd.max() <= 0:
            continue
        vmax = vd.max()
        lo = (vd > 0) & (vd <= 0.1 * vmax)
        mid = (vd > 0.1 * vmax) & (vd <= 0.3 * vmax)
        hi = vd >= 0.8 * vmax
        s0 = linfit(vd[lo], i[lo])[0] if lo.sum() >= 2 else float("nan")
        s1 = linfit(vd[mid], i[mid])[0] if mid.sum() >= 2 else float("nan")
        gout = linfit(vd[hi], i[hi])[0] if hi.sum() >= 2 else float("nan")
        imax = float(i[-1])
        sat_quality = gout * vmax / imax if imax > 0 else float("nan")
        # ideal TFT: conductance is highest at Vd -> 0 (s0 > s1). A rising start means a barrier.
        barrier = bool(np.isfinite(s0) and np.isfinite(s1) and s1 > 0 and s0 < 0.85 * s1)
        rep["curves"].append(dict(vg=v, Id_at_vdmax_A=imax, slope_start_S=s0, slope_early_S=s1,
                                  gout_S=gout, rel_output_conductance=sat_quality,
                                  contact_barrier=barrier))
        if barrier:
            rep["warnings"].append(f"Vg={v:g} V: current starts superlinearly (S-shape) -> contact barrier "
                                   "likely (Schottky-like source/drain). Try Al/In/ITO contacts or a longer anneal.")
    return rep


# ------------------------------------------------------------------------------------------
# tiny SVG plotter (no matplotlib needed)
# ------------------------------------------------------------------------------------------
def svg_plot(series, path, title, xlabel, ylabel, logy=False):
    """series: list of (label, x array, y array). Writes a self-contained SVG file."""
    Wpx, Hpx, ml, mr, mt, mb = 640, 420, 70, 20, 30, 50
    xs = np.concatenate([s[1] for s in series])
    ys = np.concatenate([s[2] for s in series])
    if logy:
        ys = np.log10(np.clip(np.abs(ys), 1e-16, None))
    x0, x1 = float(xs.min()), float(xs.max())
    y0, y1 = float(ys.min()), float(ys.max())
    if y1 == y0:
        y1 = y0 + 1
    if logy:
        y0, y1 = math.floor(y0), math.ceil(y1)

    def px(x):
        return ml + (x - x0) / (x1 - x0) * (Wpx - ml - mr)

    def py(y):
        return Hpx - mb - (y - y0) / (y1 - y0) * (Hpx - mt - mb)

    colors = ["#1f5fa8", "#c2410c", "#15803d", "#7e22ce", "#a16207", "#0e7490"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wpx}" height="{Hpx}" font-family="sans-serif" font-size="12">',
           f'<rect width="{Wpx}" height="{Hpx}" fill="white"/>',
           f'<text x="{Wpx/2}" y="18" text-anchor="middle" font-size="14">{title}</text>',
           f'<line x1="{ml}" y1="{Hpx-mb}" x2="{Wpx-mr}" y2="{Hpx-mb}" stroke="black"/>',
           f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{Hpx-mb}" stroke="black"/>',
           f'<text x="{Wpx/2}" y="{Hpx-12}" text-anchor="middle">{xlabel}</text>',
           f'<text x="16" y="{Hpx/2}" text-anchor="middle" transform="rotate(-90 16 {Hpx/2})">{ylabel}</text>']
    for k in range(6):
        xv = x0 + k * (x1 - x0) / 5
        out.append(f'<text x="{px(xv):.1f}" y="{Hpx-mb+16}" text-anchor="middle">{xv:.3g}</text>')
    yt = range(int(y0), int(y1) + 1) if logy else [y0 + k * (y1 - y0) / 5 for k in range(6)]
    for yv in yt:
        lab = f"1e{int(yv)}" if logy else f"{yv:.3g}"
        out.append(f'<text x="{ml-6}" y="{py(yv)+4:.1f}" text-anchor="end">{lab}</text>')
        out.append(f'<line x1="{ml}" y1="{py(yv):.1f}" x2="{Wpx-mr}" y2="{py(yv):.1f}" stroke="#ddd"/>')
    for n, (label, x, y) in enumerate(series):
        yy = np.log10(np.clip(np.abs(y), 1e-16, None)) if logy else y
        pts = " ".join(f"{px(a):.1f},{py(b):.1f}" for a, b in zip(x, yy))
        c = colors[n % len(colors)]
        out.append(f'<polyline fill="none" stroke="{c}" stroke-width="1.5" points="{pts}"/>')
        out.append(f'<text x="{Wpx-mr-5}" y="{mt+15+15*n}" text-anchor="end" fill="{c}">{label}</text>')
    out.append("</svg>")
    with open(path, "w") as f:
        f.write("\n".join(out))


# ------------------------------------------------------------------------------------------
# synthetic TFT (used by --selftest and by pico_smu.py --sim)
# ------------------------------------------------------------------------------------------
def tft_current(vg, vd, mu=0.5, vth=6.0, ss=0.8, W_um=1000.0, L_um=10.0, tox_nm=300.0,
                eps_r=3.9, floor=2e-12, schottky_v0=0.0):
    """Smooth subthreshold-to-square-law model (EKV-style interpolation). Returns |Id| in A."""
    cox = cox_F_cm2(tox_nm, eps_r)
    k = 0.5 * mu * cox * W_um / L_um
    m = 2.0 * ss / math.log(10)

    def G(u):
        return m * np.logaddexp(0.0, u / m)

    vg = np.asarray(vg, dtype=float)
    vd = np.asarray(vd, dtype=float)
    i = k * (G(vg - vth) ** 2 - G(vg - vth - vd) ** 2)
    if schottky_v0 > 0:
        i = i * vd ** 2 / (vd ** 2 + schottky_v0 ** 2)
    return np.abs(i) + floor


def synth_transfer(vd, mu, vth, ss, floor, hyst, W_um, L_um, rng, ig=None):
    up = np.arange(-2.5, 27.5001, 0.25)
    dn = up[::-1][1:]
    vg = np.concatenate([up, dn])
    th = np.concatenate([np.full(len(up), vth), np.full(len(dn), vth + hyst)])
    i = np.array([tft_current(a, vd, mu, t, ss, W_um, L_um, floor=floor) for a, t in zip(vg, th)])
    i = i * (1 + 0.01 * rng.standard_normal(len(i))) + 2e-13 * rng.standard_normal(len(i))
    d = {"vg": vg, "vd": np.full(len(vg), vd), "id": i,
         "dir": np.array(["f"] * len(up) + ["r"] * len(dn))}
    if ig is not None:
        d["ig"] = np.full(len(vg), ig) * (1 + 0.05 * rng.standard_normal(len(vg)))
    return d


def selftest():
    rng = np.random.default_rng(7)
    W, L = 1000.0, 10.0
    true = dict(mu=0.5, vth=6.0, ss=0.8, floor=2e-12, hyst=1.5)
    ok = True
    tmp = tempfile.mkdtemp(prefix="T4_iv_selftest_")

    def check(name, got, want, tol, rel=True):
        nonlocal ok
        if got is None:
            print(f"  FAIL {name}: not extracted")
            ok = False
            return
        err = abs(got - want) / abs(want) if rel else abs(got - want)
        flag = "ok  " if err <= tol else "FAIL"
        if err > tol:
            ok = False
        print(f"  {flag} {name:22s} got {got:10.4g}  true {want:10.4g}  (tol {tol}{' rel' if rel else ' abs'})")

    print("Selftest 1: saturation transfer (Vd = 20 V), forward + reverse sweep, CSV round trip")
    d = synth_transfer(20.0, true["mu"], true["vth"], true["ss"], true["floor"], true["hyst"], W, L, rng)
    p = os.path.join(tmp, "sat.csv")
    write_csv(p, d, ["dir", "vg", "vd", "id"])
    d2 = load_csv(p)
    r = analyze_transfer(d2, W, L, 300.0)
    check("mu_sat cm2/Vs", r["mu_cm2_Vs"], true["mu"], 0.15)
    check("Vth V", r["Vth_V"], true["vth"], 0.8, rel=False)
    check("SS V/dec", r["SS_V_per_dec"], true["ss"], 0.2)
    check("Ioff A", r["Ioff_A"], true["floor"], 0.5)
    check("hysteresis V", r.get("hysteresis_V"), true["hyst"], 0.4, rel=False)
    if r["regime"] != "sat":
        print("  FAIL regime detection")
        ok = False
    svg = os.path.join(tmp, "sat.svg")
    f, _ = split_sweeps(d2)
    svg_plot([("forward", d2["vg"][f], d2["id"][f])], svg, "selftest transfer", "Vg (V)", "Id (A)", logy=True)
    if not os.path.getsize(svg) > 500:
        ok = False

    print("Selftest 2: linear transfer (Vd = 0.5 V)")
    d = synth_transfer(0.5, true["mu"], true["vth"], true["ss"], true["floor"], 0.0, W, L, rng)
    r = analyze_transfer(d, W, L, 300.0)
    check("mu_lin cm2/Vs", r["mu_cm2_Vs"], true["mu"], 0.2)
    check("Vth_lin V", r["Vth_V"], true["vth"], 1.5, rel=False)   # ELR is noise-sensitive
    if r["regime"] != "lin":
        print("  FAIL regime detection (lin)")
        ok = False

    print("Selftest 3: gate-leakage flag")
    d = synth_transfer(20.0, 0.5, 6.0, 0.8, 2e-12, 0.0, W, L, rng, ig=5e-12)
    r = analyze_transfer(d, W, L, 300.0)
    flagged = any("gate leakage" in w for w in r["warnings"])
    print(f"  {'ok  ' if flagged else 'FAIL'} leaky gate flagged")
    ok &= flagged
    d = synth_transfer(20.0, 0.5, 6.0, 0.8, 2e-12, 0.0, W, L, rng, ig=1e-14)
    r = analyze_transfer(d, W, L, 300.0)
    clean = not any("gate leakage" in w for w in r["warnings"])
    print(f"  {'ok  ' if clean else 'FAIL'} clean gate not flagged")
    ok &= clean

    print("Selftest 4: --gleak path with pico_smu-format files (transfer has no ig column)")
    d = synth_transfer(17.5, 0.5, 6.0, 0.8, 2e-12, 0.0, W, L, rng)
    pt = os.path.join(tmp, "transfer_sat.csv")
    with open(pt, "w") as f:
        f.write("# transfer sweep (pico_smu format)\nmode,dir,vgs,vds,id,range,t_s\n")
        for k in range(len(d["vg"])):
            f.write(f"transfer,{d['dir'][k]},{d['vg'][k]:.4f},{d['vd'][k]:.4f},{d['id'][k]:.6e},hi,{k*0.4:.2f}\n")
    dt = load_csv(pt)
    r = analyze_transfer(dt, W, L, 300.0)
    nocheck = any("NOT checked" in w for w in r["warnings"])
    print(f"  {'ok  ' if nocheck else 'FAIL'} missing gate-leakage data is reported")
    ok &= nocheck
    for ig_level, want in ((5e-12, True), (1e-14, False)):
        pg = os.path.join(tmp, f"gleak_{ig_level:.0e}.csv")
        with open(pg, "w") as f:
            f.write("# gate leakage (pico_smu format)\nmode,dir,vgs,vds,ig,range,t_s\n")
            for k, vg in enumerate(np.arange(-2.5, 24.51, 1.0)):
                ig = -ig_level * (1 + 0.05 * rng.standard_normal())
                f.write(f"gleak,f,{vg:.4f},0.0000,{ig:.6e},hi,{2*k:.2f}\n")
        try:
            load_csv(pg)
            print("  FAIL gleak file accepted as a transfer file")
            ok = False
        except ValueError as e:
            good_msg = "--gleak" in str(e)
            print(f"  {'ok  ' if good_msg else 'FAIL'} gleak file as main CSV gives a hint, not a crash")
            ok &= good_msg
        r = analyze_transfer(attach_gleak(dt, load_gleak(pg)), W, L, 300.0)
        got = any("gate leakage" in w for w in r["warnings"])
        good = got == want
        print(f"  {'ok  ' if good else 'FAIL'} --gleak with |ig| {ig_level:.0e} A: flagged={got} (expected {want})")
        ok &= good

    print("Selftest 5: output curves, ideal vs Schottky-like contacts")
    for v0, want in ((0.0, False), (1.5, True)):
        vgl, vdl, il = [], [], []
        for vg in (10.0, 15.0, 20.0, 25.0):
            vds = np.linspace(0, 20, 81)
            i = tft_current(vg, vds, schottky_v0=v0) * (1 + 0.01 * rng.standard_normal(len(vds)))
            vgl += [vg] * len(vds)
            vdl += list(vds)
            il += list(i)
        r = analyze_output({"vg": np.array(vgl), "vd": np.array(vdl), "id": np.array(il)}, W, L)
        got = any(c["contact_barrier"] for c in r["curves"])
        good = got == want
        print(f"  {'ok  ' if good else 'FAIL'} schottky_v0={v0}: barrier flagged={got} (expected {want})")
        ok &= good
    print(f"\nSelftest files in {tmp}")
    print("SELFTEST PASS" if ok else "SELFTEST FAIL")
    return 0 if ok else 1


# ------------------------------------------------------------------------------------------
def fmt(rep):
    lines = []
    for k, v in rep.items():
        if k in ("warnings", "curves"):
            continue
        if isinstance(v, float):
            lines.append(f"  {k:22s} {v:.4g}")
        else:
            lines.append(f"  {k:22s} {v}")
    for c in rep.get("curves", []):
        lines.append("  Vg={vg:g} V: Id(Vdmax)={Id_at_vdmax_A:.3g} A, rel. output conductance={rel_output_conductance:.3g}, "
                     "contact barrier={contact_barrier}".format(**c))
    for w in rep.get("warnings", []):
        lines.append(f"  WARNING: {w}")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["transfer", "output"])
    ap.add_argument("csv")
    ap.add_argument("--W", type=float, default=1000.0, help="channel width, um")
    ap.add_argument("--L", type=float, default=10.0, help="channel length, um")
    ap.add_argument("--tox-nm", type=float, default=300.0)
    ap.add_argument("--eps", type=float, default=3.9)
    ap.add_argument("--vd", type=float, default=None)
    ap.add_argument("--voff", type=float, default=None, help="report Ioff at this Vg instead of the floor")
    ap.add_argument("--regime", choices=["auto", "sat", "lin"], default="auto")
    ap.add_argument("--temp-c", type=float, default=25.0)
    ap.add_argument("--gleak", default=None, help="gate-leakage CSV from pico_smu 'gleak' (vgs, ig)")
    ap.add_argument("--json", default=None)
    ap.add_argument("--svg", default=None)
    a = ap.parse_args(argv)
    try:
        d = load_csv(a.csv)
    except ValueError as e:
        print(f"ERROR: {e}")
        return 2
    if a.gleak:
        if a.mode != "transfer":
            print("ERROR: --gleak only applies to transfer analysis")
            return 2
        d = attach_gleak(d, load_gleak(a.gleak))
    if a.mode == "transfer":
        rep = analyze_transfer(d, a.W, a.L, a.tox_nm, a.eps, a.vd, a.regime, a.voff, a.temp_c)
        if a.svg:
            f, r = split_sweeps(d)
            ser = [("forward", d["vg"][f], d["id"][f])]
            if len(r):
                ser.append(("reverse", d["vg"][r], d["id"][r]))
            svg_plot(ser, a.svg, os.path.basename(a.csv), "Vgs (V)", "|Id| (A)", logy=True)
    else:
        rep = analyze_output(d, a.W, a.L)
        if a.svg:
            vgs = np.round(d["vg"], 2)
            ser = [(f"Vg={v:g}", d["vd"][vgs == v], np.abs(d["id"][vgs == v])) for v in sorted(set(vgs.tolist()))]
            svg_plot(ser, a.svg, os.path.basename(a.csv), "Vds (V)", "|Id| (A)")
    print(f"{a.mode} analysis of {a.csv}  (W={a.W} um, L={a.L} um, tox={a.tox_nm} nm)")
    print(fmt(rep))
    if a.mode == "transfer":
        print("  NOTE: Ioff_A is the lowest current in the sweep. If it is within ~3x of the scatter of your floor"
              " test (floor.csv, E7 step 3), it measures your setup, not the channel; the planning channel"
              " off-current is ~1e-16 A (E7 section 1.4).")
    if a.json:
        with open(a.json, "w") as f:
            json.dump(rep, f, indent=1, default=float)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
