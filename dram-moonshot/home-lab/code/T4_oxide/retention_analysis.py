#!/usr/bin/env python3
"""
retention_analysis.py -- turn E8 gain-cell decay logs into leakage currents, retention times and
activation energies. Track T4, dram-moonshot home lab. Python 3 + numpy only.

Physics
  charge on the storage node (SN):  Q = C_SN * V      ->  leakage  I = -C_SN * dV/dt
  retention to lose dV:             t_ret = C_SN * dV / I
  temperature:                      I(T) = I0 * exp(-Ea / kT)   (Arrhenius; fit ln I vs 1/kT)
  floor subtraction:                I_switch = I_cell - I_dummy  (dummy cell = same node, no channel)

Inputs
  Run CSV (one hold experiment): header with  t_s  and either  v_sn  (volts, e.g. from an
  electrometer buffer, see E4) or  i_read  (amps through the read transistor). pico_gaincell.py
  writes t_s,i_read_A,... ; the column name i_read_a is accepted too.
  Calibration CSV (needed with i_read): columns v_sn,i_read  -- made by pico_gaincell.py
  'calibrate': it writes known voltages through the switch and records the read current.

Usage
  python3 retention_analysis.py run hold_25C.csv --c-sn 10.18e-9 [--calib cal.csv] [--dv 0.1] [--t0 5]
  python3 retention_analysis.py compare --c-sn 10.18e-9 [--calib cal.csv] \
        --run oxide:25:ox25.csv --run oxide:45:ox45.csv --run oxide:65:ox65.csv \
        --run si:25:si25.csv   --run si:45:si45.csv   --run si:65:si65.csv \
        --run dummy:25:d25.csv --run dummy:65:d65.csv  [--floor-label dummy] [--json out.json]
  python3 retention_analysis.py --selftest     (synthetic decays; exit 0 on pass)
"""

import argparse
import json
import math
import os
import sys
import tempfile

import numpy as np

KB_EV = 8.617333262e-5


def load_cols(path):
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.lstrip().startswith("#")]
    header = [h.strip().lower() for h in lines[0].split(",")]
    cols = {h: [] for h in header}
    for ln in lines[1:]:
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) != len(header):
            continue
        for h, p in zip(header, parts):
            cols[h].append(p)
    out = {}
    for h, v in cols.items():
        try:
            out[h] = np.array([float(x) for x in v])
        except ValueError:
            out[h] = np.array(v)
    return out


def calib_from_csv(path):
    """Read v_sn,i_read pairs; keep only the part where current rises monotonically with voltage
    and sits well above the noise floor (the bottom of a calibration is just noise)."""
    c = load_cols(path)
    i = np.abs(c["i_read"] if "i_read" in c else c["i_read_a"])
    v = c["v_sn"]
    o = np.argsort(v)
    v, i = v[o], i[o]
    floor = 10 * float(np.min(i[i > 0])) if np.any(i > 0) else 1e-30
    keep_v, keep_i = [], []
    for vv, ii in zip(v, i):
        if ii > floor and (not keep_i or ii > 1.02 * keep_i[-1]):
            keep_v.append(vv)
            keep_i.append(ii)
    if len(keep_v) < 3:
        raise ValueError(f"{path}: calibration has fewer than 3 usable points")
    return np.log10(np.array(keep_i)), np.array(keep_v)


def to_vsn(d, calib):
    if "v_sn" in d:
        return d["v_sn"].astype(float)
    key = "i_read" if "i_read" in d else ("i_read_a" if "i_read_a" in d else None)
    if key is None:
        raise ValueError("run CSV needs v_sn or i_read column")
    if calib is None:
        raise ValueError("i_read data needs --calib (v_sn vs i_read table)")
    li, v = calib
    x = np.log10(np.clip(np.abs(d[key]), 1e-30, None))
    if np.any(x < li[0]) or np.any(x > li[-1]):
        sys.stderr.write("warning: read current outside calibration range; values clipped\n")
    return np.interp(x, li, v)


def linfit(x, y):
    a = np.vstack([x, np.ones_like(x)]).T
    (m, b), *_ = np.linalg.lstsq(a, y, rcond=None)
    return float(m), float(b)


def analyze_run(t, v, c_sn, dv=0.1, t0=None, v_fail=None):
    """Leakage and retention of one hold experiment."""
    t = np.asarray(t, float)
    v = np.asarray(v, float)
    if t0 is None:
        t0 = t[min(2, len(t) - 1)]          # skip the first samples (kickback, settling)
    sel = t >= t0
    t, v = t[sel] - t0, v[sel]
    n = len(t)
    if n < 6:
        raise ValueError("need at least 6 samples after t0")
    v0 = float(np.median(v[:3]))
    w = max(5, n // 10)
    slopes, centers, vcen = [], [], []
    for s in range(0, n - w + 1, max(1, w // 2)):
        m, _ = linfit(t[s:s + w], v[s:s + w])
        slopes.append(m)
        centers.append(float(np.mean(t[s:s + w])))
        vcen.append(float(np.mean(v[s:s + w])))
    slopes = np.array(slopes)
    i_win = -c_sn * slopes
    # initial leakage: one straight-line fit over every sample in the first 10% of droop
    # (uses all points for slow decays; stays early for fast ones; bias <= ~5% for exponential decay)
    below = np.where(v < v0 - 0.1 * abs(v0))[0]
    k_end = int(below[0]) if len(below) else n
    warn = None
    if k_end < 3:
        k_end = 3
        warn = "decay faster than the sampling: log faster (use log-spaced sample times)"
    m0, _ = linfit(t[:k_end], v[:k_end])
    i_init = -c_sn * m0
    rep = {"v0_V": v0, "I_initial_A": i_init, "I_median_A": float(np.median(i_win)),
           "droop_V_per_s": -m0, "duration_s": float(t[-1]), "n_fit_points": k_end,
           "I_vs_V": [(round(a, 4), float(b)) for a, b in zip(vcen, i_win)]}
    target = v0 - dv
    hit = np.where(v <= target)[0]
    if len(hit):
        k = hit[0]
        if k == 0:
            rep["t_dv_s"] = float(t[0])
        else:
            rep["t_dv_s"] = float(t[k - 1] + (target - v[k - 1]) * (t[k] - t[k - 1]) / (v[k] - v[k - 1]))
        rep["t_dv_extrapolated"] = False
    else:
        rep["t_dv_s"] = c_sn * dv / i_init if i_init > 0 else float("inf")
        rep["t_dv_extrapolated"] = True
    if v_fail is not None:
        hit = np.where(v <= v_fail)[0]
        rep["t_fail_s"] = float(t[hit[0]]) if len(hit) else None
    rep["dv_V"] = dv
    if warn:
        rep["warning"] = warn
    return rep


def arrhenius(temps_c, currents):
    """Fit ln I = ln I0 - Ea/kT. Returns Ea (eV), I at 25 C, R^2."""
    x = 1.0 / (KB_EV * (np.asarray(temps_c, float) + 273.15))
    y = np.log(np.asarray(currents, float))
    m, b = linfit(x, y)
    pred = m * x + b
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2)) or 1e-30
    i25 = math.exp(m / (KB_EV * 298.15) + b)
    return -m, i25, 1 - ss_res / ss_tot


def crossover_c(ea1, i25_1, ea2, i25_2):
    """Temperature where two Arrhenius lines cross, or None (parallel or outside -50..300 C)."""
    if abs(ea1 - ea2) < 1e-6:
        return None
    inv_t = 1 / 298.15 + KB_EV * math.log(i25_1 / i25_2) / (ea1 - ea2)
    if inv_t <= 0:
        return None
    tc = 1 / inv_t - 273.15
    return tc if -50 < tc < 300 else None


def compare(runs, c_sn, calib, dv, t0, floor_label):
    res = {}
    for label, tc, path in runs:
        d = load_cols(path)
        v = to_vsn(d, calib)
        r = analyze_run(d["t_s"], v, c_sn, dv, t0)
        res.setdefault(label, {})[tc] = r
    out = {"per_run": {lab: {str(k): {kk: vv for kk, vv in r.items() if kk != "I_vs_V"}
                             for k, r in v.items()} for lab, v in res.items()},
           "labels": {}, "warnings": []}
    floor = res.get(floor_label, {})
    for lab, byt in res.items():
        temps = sorted(byt)
        cur = [byt[t]["I_initial_A"] for t in temps]
        entry = {"temps_C": temps, "I_cell_A": cur}
        if lab != floor_label and floor:
            sub = []
            for t, i in zip(temps, cur):
                if t in floor:
                    fi = floor[t]["I_initial_A"]
                    if i < 3 * fi:
                        out["warnings"].append(f"{lab} at {t} C: cell leakage {i:.2e} A < 3x dummy floor "
                                               f"{fi:.2e} A -> you are measuring the setup, not the switch")
                    sub.append(max(i - fi, 1e-30))
                else:
                    sub.append(i)
            entry["I_switch_A"] = sub
        if len(temps) >= 2 and all(c > 0 for c in cur):
            ea, i25, r2 = arrhenius(temps, entry.get("I_switch_A", cur))
            entry.update(Ea_eV=ea, I25_A=i25, R2=r2)
        entry["t_dv_s"] = [byt[t]["t_dv_s"] for t in temps]
        out["labels"][lab] = entry
    labs = [l for l in out["labels"] if l != floor_label and "Ea_eV" in out["labels"][l]]
    pairs = []
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            a, b = out["labels"][labs[i]], out["labels"][labs[j]]
            common = sorted(set(a["temps_C"]) & set(b["temps_C"]))
            ratio = {}
            for t in common:
                ta = a["t_dv_s"][a["temps_C"].index(t)]
                tb = b["t_dv_s"][b["temps_C"].index(t)]
                ratio[t] = ta / tb
            growth = ratio[common[-1]] / ratio[common[0]] if len(common) >= 2 else None
            pairs.append({"a": labs[i], "b": labs[j], "retention_ratio_a_over_b": ratio,
                          "ratio_growth_low_to_high_T": growth,
                          "dEa_b_minus_a_eV": b["Ea_eV"] - a["Ea_eV"],
                          "crossover_C": crossover_c(a["Ea_eV"], a["I25_A"], b["Ea_eV"], b["I25_A"])})
    out["pairs"] = pairs
    return out


# ------------------------------------------------------------------------------------------
# selftest
# ------------------------------------------------------------------------------------------
def synth_run(path, c_sn, i_leak, rng, calib_fn=None, dur=2000.0, v0=3.0, kick=0.3):
    tau = c_sn * v0 / i_leak                       # ohmic-like leak toward 0 V
    dur = min(dur, 2.0 * tau)
    t = np.concatenate([[0.0], np.geomspace(0.5, dur, 160)])   # log-spaced, as pico_gaincell logs
    v = v0 * np.exp(-t / tau)
    v[:2] += kick * np.array([1.0, 0.2])           # settling transient the analysis must skip
    if calib_fn is None:
        v = v + 2e-5 * rng.standard_normal(len(v))
        with open(path, "w") as f:
            f.write("t_s,v_sn\n" + "".join(f"{a:.3f},{b:.7f}\n" for a, b in zip(t, v)))
    else:
        i = calib_fn(v) * (1 + 0.003 * rng.standard_normal(len(v)))
        with open(path, "w") as f:
            f.write("t_s,i_read_A,temp_c\n" + "".join(f"{a:.3f},{b:.6e},25\n" for a, b in zip(t, i)))


def selftest():
    rng = np.random.default_rng(11)
    tmp = tempfile.mkdtemp(prefix="T4_ret_selftest_")
    c_sn = 10.18e-9
    ok = True

    def arr(i25, ea, tc):
        return i25 * math.exp(-ea / KB_EV * (1 / (tc + 273.15) - 1 / 298.15))

    # read transistor in subthreshold: 100 mV/decade, 1 nA at 1.0 V
    def read_fn(v):
        return 1e-9 * 10 ** ((v - 1.0) / 0.1)

    cal = os.path.join(tmp, "cal.csv")
    vv = np.linspace(0.0, 3.6, 37)
    with open(cal, "w") as f:
        f.write("v_sn,i_read\n" + "".join(f"{a:.4f},{read_fn(a):.6e}\n" for a in vv))
    truth = {"oxide": (1e-12, 0.35), "si": (1e-11, 0.80), "dummy": (1e-13, 0.10)}
    runs = []
    for lab, (i25, ea) in truth.items():
        for tc in (25.0, 45.0, 65.0):
            leak = arr(i25, ea, tc)
            if lab != "dummy":
                leak += arr(*truth["dummy"], tc)      # a real cell includes the setup floor
            p = os.path.join(tmp, f"{lab}_{int(tc)}.csv")
            synth_run(p, c_sn, leak, rng, calib_fn=read_fn)
            runs.append((lab, tc, p))
    out = compare(runs, c_sn, calib_from_csv(cal), 0.1, None, "dummy")
    for lab in ("oxide", "si"):
        e = out["labels"][lab]
        i25, ea = truth[lab]
        good_ea = abs(e["Ea_eV"] - ea) < 0.05
        good_i = abs(e["I25_A"] / i25 - 1) < 0.15
        print(f"  {'ok  ' if good_ea else 'FAIL'} {lab:6s} Ea  got {e['Ea_eV']:.3f} eV  true {ea}")
        print(f"  {'ok  ' if good_i else 'FAIL'} {lab:6s} I25 got {e['I25_A']:.3e} A  true {i25:.1e}")
        ok &= good_ea and good_i
    pr = out["pairs"][0]
    g = pr["ratio_growth_low_to_high_T"]
    exp_g = math.exp((0.80 - 0.35) / KB_EV * (1 / 298.15 - 1 / 338.15))
    good_g = g is not None and abs(g / exp_g - 1) < 0.3
    print(f"  {'ok  ' if good_g else 'FAIL'} retention-ratio growth 25->65 C got {g:.2f}, expected ~{exp_g:.2f}")
    ok &= good_g
    x = crossover_c(1.3, 1e-12, 0.56, 1e-11)
    good_x = x is not None and 45 < x < 60
    print(f"  {'ok  ' if good_x else 'FAIL'} crossover (Ea 1.3 vs 0.56 eV, 10x apart at 25 C) = {x:.1f} C")
    ok &= good_x
    # direct-voltage path + extrapolation flag
    p = os.path.join(tmp, "direct.csv")
    synth_run(p, c_sn, 1e-14, rng, dur=600.0)
    d = load_cols(p)
    r = analyze_run(d["t_s"], d["v_sn"], c_sn, 0.1)
    good_d = r["t_dv_extrapolated"] and abs(r["I_initial_A"] / 1e-14 - 1) < 0.3
    print(f"  {'ok  ' if good_d else 'FAIL'} tiny leak (1e-14 A): I={r['I_initial_A']:.2e} A, "
          f"t_dv={r['t_dv_s']:.3g} s extrapolated={r['t_dv_extrapolated']}")
    ok &= good_d
    print(f"Selftest files in {tmp}")
    print("SELFTEST PASS" if ok else "SELFTEST FAIL")
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("run")
    p1.add_argument("csv")
    p2 = sub.add_parser("compare")
    p2.add_argument("--run", action="append", required=True, help="label:tempC:file.csv")
    p2.add_argument("--floor-label", default="dummy")
    for p in (p1, p2):
        p.add_argument("--c-sn", type=float, required=True, help="storage-node capacitance, F")
        p.add_argument("--calib", default=None)
        p.add_argument("--dv", type=float, default=0.1)
        p.add_argument("--t0", type=float, default=None, help="ignore samples before this time, s")
        p.add_argument("--json", default=None)
    p1.add_argument("--v-fail", type=float, default=None)
    a = ap.parse_args(argv)
    calib = calib_from_csv(a.calib) if a.calib else None
    if a.cmd == "run":
        d = load_cols(a.csv)
        rep = analyze_run(d["t_s"], to_vsn(d, calib), a.c_sn, a.dv, a.t0, a.v_fail)
        for k, v in rep.items():
            if k != "I_vs_V":
                print(f"  {k:20s} {v:.4g}" if isinstance(v, float) else f"  {k:20s} {v}")
    else:
        runs = []
        for s in a.run:
            lab, tc, path = s.split(":", 2)
            runs.append((lab, float(tc), path))
        rep = compare(runs, a.c_sn, calib, a.dv, a.t0, a.floor_label)
        for lab, e in rep["labels"].items():
            line = f"{lab:8s} T={e['temps_C']} I_cell={['%.2e' % x for x in e['I_cell_A']]}"
            if "Ea_eV" in e:
                line += f"  Ea={e['Ea_eV']:.2f} eV  I25={e['I25_A']:.2e} A  R2={e['R2']:.3f}"
            print(line)
        for pr in rep["pairs"]:
            print(f"{pr['a']} vs {pr['b']}: retention ratio {pr['retention_ratio_a_over_b']}, growth "
                  f"{pr['ratio_growth_low_to_high_T']}, crossover {pr['crossover_C']}")
        for w in rep["warnings"]:
            print("WARNING:", w)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(rep, f, indent=1, default=float)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
