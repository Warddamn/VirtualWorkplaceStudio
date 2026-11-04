#!/usr/bin/env python3
"""
retention_fit.py -- fit REAL public DRAM retention data, then re-run the raw-ber-contract refresh model with it.

Data (not stored in this repository; fetch it with fetch_data.py):
  CMU-SAFARI DRAM-Voltage-Study, characterization_results/retention_time_profile.csv
  https://github.com/CMU-SAFARI/DRAM-Voltage-Study (commit b2089c3c7c2aac1d0936b4cfc572a675f5fd73f4)
  31 DDR3L SO-DIMMs from 3 vendors, 2 GB each (4 x 4Gb chips), tested on an FPGA (SoftMC) at 20 and 70 C
  ambient, 1.15/1.2/1.35 V, refresh intervals 64-2048 ms. One row = one test: bit-error counts per bank.

What it computes:
  1. Fleet-mean retention bit error rate (BER) per temperature / voltage / interval, with bootstrap CIs.
  2. Per-DIMM lognormal tail fit at 70 C: sigma_ln of log retention time, median, local slope.
  3. Activation energy (Ea) of the weak tail from the 20 C vs 70 C time shift at matched BER, per DIMM and pooled.
  4. Test-to-test variability of the counts (an upper bound on VRT + pattern + setup noise; cell addresses are
     not in the data, so the VRT cell fraction itself cannot be measured).
  5. Bank-level uniformity (are errors spread evenly over the 8 banks?).
  6. Comparison against the BER the raw-ber-contract model assumes, and a re-run of the model's safe-interval
     calculation (models/raw-ber-contract.py: lognormal_params L664, ber_ret L672, p_max_interval L685,
     refresh_numbers L701, max_p_rs L615, max_p_rs_ondie L917, the section 10.1 case table L1007-1021)
     with the fitted parameters swapped in.

Run (stdlib + numpy):
  python3 -I research/realdata/retention_fit.py --csv /path/to/retention_time_profile.csv
  python3 -I research/realdata/retention_fit.py --selftest
Writes research/realdata/retention_fit_summary.json and research/realdata/retention_per_dimm.csv
(derived numbers only; no raw rows). Exit 0 on success.

Conventions:
  * "BER" here means random-data-equivalent BER = mean errors per test / bits. The tests alternate data
    patterns (about half the trials at long intervals show exactly 0 errors, the inverse pattern), so the mean
    over trials approximates random data, where about half the cells are charged. This matches the model's
    ber_ret(), which multiplies the cell failure fraction by data_pattern_factor = 0.5 [ESTIMATE].
  * F(t) is the cell failure fraction (all cells charged) = 2 x BER.
  * Temperatures are the reported ambient values; chip temperature may be a few C higher [UNVERIFIED].
"""

import argparse
import csv
import importlib.util
import json
import math
import os
import random
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))  # dram-moonshot/
MODEL_PATH = os.path.join(ROOT, "models", "raw-ber-contract.py")

BITS_PER_DIMM = 2 * 2 ** 30 * 8  # 2 GB DIMM = 4 x 4Gb chips [REPORTED: arXiv 1705.10292 via search snippet]
BITS_PER_BANK = BITS_PER_DIMM // 8  # DDR3: 8 banks
DATA_FACTOR = 0.5  # mean over pattern + inverse = random data (half the cells charged) [ESTIMATE]
K_B = 8.617333262e-5  # eV/K
C2K = 273.15
REQUIRED = ["dimm_name", "vendor", "vdd", "temperature(C)", "refresh_interval(ms)"] + \
           [f"bank{i}_bit_err_count" for i in range(8)] + ["total_dimm_bit_err_count"]
NOMINAL_V = 1.35  # DDR3L nominal VDD


# ------------------------------------------------------------------------------------------------
# Math
# ------------------------------------------------------------------------------------------------
def erfc_np(x):
    """Complementary error function, vectorised (Numerical Recipes erfcc; fractional error < 1.2e-7 for all x),
    so tails down to 1e-15 keep their relative precision."""
    x = np.asarray(x, dtype=float)
    z = np.abs(x)
    t = 1.0 / (1.0 + 0.5 * z)
    ans = t * np.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (
        -0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))))
    return np.where(x >= 0, ans, 2.0 - ans)


def norm_sf(z):
    return 0.5 * erfc_np(np.asarray(z) / math.sqrt(2.0))


def F_logn(t, mu, s):
    """Cell failure fraction by time t (s) for log-retention ~ Normal(mu, s)."""
    return norm_sf((mu - np.log(t)) / s)


def norm_ppf_upper(p):
    """z with Q(z) = p (p < 0.5), by bisection on math.erfc."""
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 0.5 * math.erfc(mid / math.sqrt(2)) > p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def arrhenius(ea_ev, t_cold_c, t_hot_c):
    """Retention-time ratio t(cold)/t(hot) for leakage ~ exp(-Ea/kT)."""
    return math.exp(ea_ev / K_B * (1.0 / (t_cold_c + C2K) - 1.0 / (t_hot_c + C2K)))


def ea_from_ratio(ratio, t_cold_c, t_hot_c):
    return K_B * math.log(ratio) / (1.0 / (t_cold_c + C2K) - 1.0 / (t_hot_c + C2K))


def poisson_ll(k, lam):
    lam = np.maximum(lam, 1e-300)
    return np.sum(k * np.log(lam) - lam, axis=-1)


# ------------------------------------------------------------------------------------------------
# Data loading
# ------------------------------------------------------------------------------------------------
def load_csv(path):
    with open(path, newline="") as f:
        rd = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (rd.fieldnames or [])]
        if missing:
            raise ValueError(f"missing columns: {missing}")
        recs = []
        for r in rd:
            try:
                banks = [float(r[f"bank{i}_bit_err_count"]) for i in range(8)]
                rec = dict(dimm=r["dimm_name"].strip(), vendor=r["vendor"].strip(), vdd=float(r["vdd"]),
                           T=float(r["temperature(C)"]), iv=int(float(r["refresh_interval(ms)"])),
                           banks=banks, total=float(r["total_dimm_bit_err_count"]))
            except (ValueError, KeyError):
                continue
            recs.append(rec)
    return recs


def group(recs, named_only=True):
    g = {}
    for r in recs:
        if named_only and not r["dimm"]:
            continue
        g.setdefault((r["dimm"], r["T"], r["vdd"], r["iv"]), []).append(r)
    return g


def group_stats(rows):
    c = np.array([r["total"] for r in rows])
    nz = c[c > 0]
    uniq = len({tuple(r["banks"]) for r in rows})
    return dict(n=len(c), unique_rows=uniq, mean=float(c.mean()), frac_zero=float(np.mean(c == 0)),
                mean_nonzero=float(nz.mean()) if len(nz) else 0.0,
                median_nonzero=float(np.median(nz)) if len(nz) else 0.0,
                cv_nonzero=float(nz.std(ddof=1) / nz.mean()) if len(nz) >= 2 and nz.mean() > 0 else None,
                maxmin_nonzero=float(nz.max() / nz.min()) if len(nz) >= 2 else None,
                bank_mean=[float(np.mean([r["banks"][i] for r in rows])) for i in range(8)])


def dimm_curves(G, mode="mean"):
    """{dimm: {(T, vdd): {iv_ms: BER}}}, BER = count / bits.
    mode "mean":   mean over tests = random-data equivalent (pattern + inverse average) [central]
    mode "robust": 0.5 x median of nonzero tests (one pattern of a pattern/inverse pair; outlier-resistant)
    mode "worst":  mean of nonzero tests read as if it were random data (2x pessimistic when half the tests are 0)
    mode "max":    the single worst test read as if it were random data (bound for data-pattern dependence)"""
    out = {}
    for (d, T, v, iv), rows in G.items():
        st = group_stats(rows)
        val = st["mean"]
        if st["frac_zero"] <= 0.9:  # in the low-count regime (mostly zero tests) every mode uses the mean
            if mode == "robust":
                val = DATA_FACTOR * st["median_nonzero"]
            elif mode == "worst":
                val = st["mean_nonzero"]
            elif mode == "max":
                val = max(r["total"] for r in rows)
        out.setdefault(d, {}).setdefault((T, v), {})[iv] = val / BITS_PER_DIMM
    return out


# ------------------------------------------------------------------------------------------------
# Fits
# ------------------------------------------------------------------------------------------------
MU_GRID = np.linspace(math.log(0.3), math.log(1e7), 140)
S_GRID = np.linspace(0.08, 4.0, 120)


def fit_lognormal(t_s, ber, bits=BITS_PER_DIMM):
    """Poisson pseudo-likelihood fit of BER(t) = DATA_FACTOR * F_logn(t; mu, s), using the per-test mean count as
    the count (one-test equivalent, so the CI is not overstated by repeated tests of the same cells).
    Returns (mu, s) at the test temperature, plus the log-likelihood."""
    t = np.asarray(t_s, float)
    k = np.asarray(ber, float) * bits
    mu_g, s_g = MU_GRID, S_GRID
    best = None
    for _ in range(3):
        M, S = np.meshgrid(mu_g, s_g, indexing="ij")
        lam = bits * DATA_FACTOR * F_logn(t[None, None, :], M[..., None], S[..., None])
        ll = poisson_ll(k[None, None, :], lam)
        i, j = np.unravel_index(np.argmax(ll), ll.shape)
        best = (float(mu_g[i]), float(s_g[j]), float(ll[i, j]))
        dmu = (mu_g[1] - mu_g[0]) * 3
        ds = (s_g[1] - s_g[0]) * 3
        mu_g = np.linspace(best[0] - dmu, best[0] + dmu, 41)
        s_g = np.linspace(max(0.03, best[1] - ds), best[1] + ds, 41)
    return best


def local_slope_logn(t, mu, s, dt=1.01):
    return math.log(float(F_logn(t * dt, mu, s)) / float(F_logn(t, mu, s))) / math.log(dt)


def interp_time_for_ber(curve, target):
    """Log-log interpolation of the time at which a measured BER curve {iv_ms: ber} reaches target.
    Returns (t_s, flag) with flag 'interp', 'extrap_low' or None if the curve never gets there."""
    pts = sorted((iv / 1000.0, b) for iv, b in curve.items() if b > 0)
    if len(pts) < 2:
        return None, None
    for (t1, b1), (t2, b2) in zip(pts, pts[1:]):
        if b1 <= target <= b2 and b2 > b1:
            x = math.log(t1) + (math.log(target) - math.log(b1)) * (math.log(t2) - math.log(t1)) / (math.log(b2) - math.log(b1))
            return math.exp(x), "interp"
    (t1, b1), (t2, b2) = pts[0], pts[1]
    if target < b1 and b2 > b1:
        k = (math.log(b2) - math.log(b1)) / (math.log(t2) - math.log(t1))
        return t1 * (target / b1) ** (1.0 / k), "extrap_low"
    return None, None


def ea_matched(c20, c70, iv_ref=2048, min_count=3.0):
    """Ea of the weakest cells from the 20 -> 70 C time shift at matched BER.
    Uses the 20 C BER at iv_ref; returns (Ea, kind) with kind 'point' or 'lower_bound' (20 C had < min_count
    errors per test, so only a bound on the shift)."""
    b20 = c20.get(iv_ref, 0.0)
    if b20 * BITS_PER_DIMM >= min_count:
        t70, flag = interp_time_for_ber(c70, b20)
        if t70 is None:
            return None, None
        return ea_from_ratio((iv_ref / 1000.0) / t70, 20.0, 70.0), "point" if flag == "interp" else "point_extrap"
    bound = min_count / BITS_PER_DIMM
    t70, flag = interp_time_for_ber(c70, bound)
    if t70 is None or t70 >= iv_ref / 1000.0:
        return None, None
    return ea_from_ratio((iv_ref / 1000.0) / t70, 20.0, 70.0), "lower_bound"


def fleet_mean(curves, keys, T, v):
    """Mean BER over DIMMs (each DIMM weighted equally) at each interval."""
    ivs = sorted({iv for d in keys for iv in curves[d].get((T, v), {})})
    res = {}
    for iv in ivs:
        vals = [curves[d][(T, v)][iv] for d in keys if iv in curves[d].get((T, v), {})]
        if vals:
            res[iv] = float(np.mean(vals))
    return res


# ------------------------------------------------------------------------------------------------
# Model re-run
# ------------------------------------------------------------------------------------------------
def load_model():
    spec = importlib.util.spec_from_file_location("raw_ber_contract_model", MODEL_PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)  # main() is guarded by __name__, so nothing is printed or written
    return m


def code_limits(m):
    V = m.V
    tgt = V("ue_budget_per_module_yr") / (V("avg_bw_GBps") * 1e9 / 64 * 3.156e7)  # = model section_target()
    return dict(tgt=tgt,
                ddr4_rs8=m.max_p_rs(tgt), ddr4_rs8_degraded=m.max_p_rs(tgt, erased=8),
                ddr5_rs8_sec=m.max_p_rs_ondie(tgt), ddr5_rs8_sec_degraded=m.max_p_rs_ondie(tgt, erased=True),
                ddr4_bch12=m.max_p_hard(int(V("rdimm_sideband_bits")) // int(V("bch_m_line")),
                                        int(V("line_data_bits")), int(V("bch_m_line")), tgt))


class SwappedRetention:
    """Context manager: replace the model's retention tail with a fitted one at 85 C.
    kind 'logn': lognormal (mu85, s); kind 'pow': power law BER = b0 * (t/t0)^k (tangent, pessimistic)."""

    def __init__(self, m, kind, **p):
        self.m, self.kind, self.p = m, kind, p

    def __enter__(self):
        self.orig_ln, self.orig_ber = self.m.lognormal_params, self.m.ber_ret
        m, p, kind = self.m, self.p, self.kind
        if kind == "logn":
            m.lognormal_params = lambda: (p["mu85"], p["s"])
        else:
            def ber_pow(P, model, temp_scale=1.0):
                Pe = P / temp_scale
                return min(p["f0"] * (Pe / p["t0"]) ** p["k"], 0.5) * m.V("data_pattern_factor")
            m.ber_ret = ber_pow
        return self

    def __exit__(self, *a):
        self.m.lognormal_params, self.m.ber_ret = self.orig_ln, self.orig_ber


EA_MODEL = None  # set in analyse(): the model's own x4-per-20-C rule = 0.72 eV between 65 and 85 C


def temp_scales(ea_hot, ea_cool):
    """temp_scale values (the model's ber_ret argument; >1 = cooler, longer retention) relative to a tail that
    was moved from the 70 C data to 85 C with ea_hot. Temperatures below 70 C use ea_cool (the tail Ea
    measured between 20 and 70 C), so nothing below 70 C borrows the hot-side assumption."""
    a = arrhenius(ea_hot, 70, 85)
    return {"85": 1.0, "70": a, "65": a * arrhenius(ea_cool, 65, 70), "45": a * arrhenius(ea_cool, 45, 70)}


CASES = [("DDR4 / RS-8 chipkill", "ddr4_rs8", 1.0, 0.064),
         ("DDR4 / RS-8 degraded (chip dead)", "ddr4_rs8_degraded", 1.0, 0.064),
         ("DDR4 / BCH-12 (no chipkill)", "ddr4_bch12", 1.0, 0.064),
         ("DDR5 / RS-8 behind SEC, x0.5 derate", "ddr5_rs8_sec", 0.5, 0.032),
         ("DDR5 / RS-8 behind SEC, no derate", "ddr5_rs8_sec", 1.0, 0.032),
         ("DDR5 / RS-8 degraded, x0.5 derate", "ddr5_rs8_sec_degraded", 0.5, 0.032)]


def safe_intervals(m, lim, ts, vrt=None, scrub_h=None):
    """Mirror of the model's section 10.1 case table (L1007-1021): safe interval per part/code at each
    temperature in ts ({label: temp_scale}); scale 0.5 is the model's DDR5 retention derate (L138)."""
    res = {}
    for name, key, scale, win in CASES:
        row = {"window_s": win}
        for T, t in ts.items():
            i = m.p_max_interval("logn", lim[key], t * scale, vrt, scrub_h)
            row[f"i{T}_s"] = i
            row[f"cut{T}"] = i / win
        res[name] = row
    return res


def measured_bound(curve70, plim, mult, scale):
    """Largest MEASURED interval at 70 C whose BER x (1 + VRT growth x scrub) fits the code limit: no
    extrapolation in BER. For a derated part (scale 0.5) the bound is scale x that interval. Returns s or 0."""
    ok = [iv / 1000.0 for iv, b in curve70.items() if b * mult <= plim]
    return scale * max(ok) if ok else 0.0


def energy_cut(m, interval_s, window_s=0.032):
    base = m.refresh_numbers(window_s)[0]
    pr, ps, _ = m.refresh_numbers(min(interval_s, 4.0))
    return base / (pr + ps)


# ------------------------------------------------------------------------------------------------
# Analysis
# ------------------------------------------------------------------------------------------------
def analyse(recs, n_boot=400, seed=1, quiet=False):
    rng = np.random.default_rng(seed)
    say = (lambda *a: None) if quiet else print
    G = group(recs)
    curves = dimm_curves(G)
    rcurves = dimm_curves(G, "robust")
    wcurves = dimm_curves(G, "worst")
    mcurves = dimm_curves(G, "max")
    dimms = sorted(curves)
    vendors = {}
    for r in recs:
        if r["dimm"]:
            vendors[r["dimm"]] = r["vendor"]
    S = dict(n_rows=len(recs), n_rows_unnamed=sum(1 for r in recs if not r["dimm"]), n_dimms=len(dimms),
             vendors={v: sum(1 for d in dimms if vendors[d] == v) for v in sorted(set(vendors.values()))},
             bits_per_dimm=BITS_PER_DIMM)
    raw_rows = [tuple([r["dimm"], r["T"], r["vdd"], r["iv"]] + r["banks"]) for r in recs]
    nz_rows = [x for x, r in zip(raw_rows, recs) if r["total"] > 0]
    S["duplicate_share_nonzero_rows"] = 1 - len(set(nz_rows)) / max(1, len(nz_rows))
    temps = sorted({k[1] for k in G})
    volts = sorted({k[2] for k in G})
    ivs = sorted({k[3] for k in G})

    # 1. fleet-mean BER with bootstrap over DIMMs
    fleet = []
    for T in temps:
        for v in volts:
            keys = [d for d in dimms if (T, v) in curves[d]]
            if not keys:
                continue
            fm = fleet_mean(curves, keys, T, v)
            for iv in ivs:
                vals = np.array([curves[d][(T, v)][iv] for d in keys if iv in curves[d][(T, v)]])
                if len(vals) == 0:
                    continue
                bs = [float(np.mean(rng.choice(vals, len(vals)))) for _ in range(n_boot)]
                zero_dimms = int(np.sum(vals == 0))
                fleet.append(dict(T_C=T, vdd=v, interval_ms=iv, n_dimms=len(vals), ber_mean=fm.get(iv, 0.0),
                                  ber_ci95=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                                  ber_max_dimm=float(vals.max()), dimms_with_zero=zero_dimms,
                                  ber_upper95_if_all_zero=(3.0 / (BITS_PER_DIMM * len(vals))) if zero_dimms == len(vals) else None))
    S["fleet_ber"] = fleet

    # 2. per-DIMM lognormal fits at 70 C, nominal V
    per = []
    for d in dimms:
        c70 = curves[d].get((70.0, NOMINAL_V), {})
        c20 = curves[d].get((20.0, NOMINAL_V), {})
        row = dict(dimm=d, vendor=vendors[d])
        if c70 and sum(1 for b in c70.values() if b * BITS_PER_DIMM >= 1) >= 2:
            t = sorted(c70)
            mu, s, ll = fit_lognormal([x / 1000 for x in t], [c70[x] for x in t])
            row.update(mu70=mu, s_ln=s, median70_s=math.exp(mu), slope_2s=local_slope_logn(2.0, mu, s),
                       ber70_2048=c70.get(2048), ber70_1024=c70.get(1024))
        ea, kind = ea_matched(c20, c70) if (c20 and c70) else (None, None)
        row.update(ea_ev=ea, ea_kind=kind, ber20_2048=c20.get(2048) if c20 else None)
        per.append(row)
    S["per_dimm"] = per

    fitted = [r for r in per if "s_ln" in r]
    if not fitted:
        raise ValueError("no DIMM has >=2 intervals with errors at 70 C; nothing to fit")
    sl = np.array([r["s_ln"] for r in fitted])
    S["per_dimm_sigma_ln"] = dict(n=len(sl), median=float(np.median(sl)), p10=float(np.percentile(sl, 10)),
                                  p90=float(np.percentile(sl, 90)), min=float(sl.min()), max=float(sl.max()))
    eas = [r["ea_ev"] for r in per if r["ea_kind"] in ("point", "point_extrap")]
    eab = [r["ea_ev"] for r in per if r["ea_kind"] == "lower_bound"]
    S["per_dimm_ea"] = dict(n_point=len(eas), point_values=sorted(round(x, 3) for x in eas),
                            n_lower_bound=len(eab), lower_bounds=sorted(round(x, 3) for x in eab),
                            median_point=float(np.median(eas)) if eas else None)

    # 3. pooled fits (fleet mean) with bootstrap over DIMMs
    keys70 = [d for d in dimms if (70.0, NOMINAL_V) in curves[d]]
    keysboth = [d for d in keys70 if (20.0, NOMINAL_V) in curves[d]]

    def pooled(keyset, cv=curves):
        c70 = fleet_mean(cv, keyset, 70.0, NOMINAL_V)
        c20 = fleet_mean(cv, keyset, 20.0, NOMINAL_V)
        t = sorted(c70)
        mu, s, _ = fit_lognormal([x / 1000 for x in t], [c70[x] for x in t])
        ea, kind = ea_matched(c20, c70)
        ea1, kind1 = ea_matched(c20, c70, iv_ref=1536)
        # tangent power law through the two longest intervals at 70 C (pessimistic extrapolation)
        tt = [x for x in t if c70[x] > 0][-2:]
        kpow = math.log(c70[tt[1]] / c70[tt[0]]) / math.log(tt[1] / tt[0])
        return dict(mu70=mu, s_ln=s, ea=ea, ea_kind=kind, ea_1536=ea1, k_pow=kpow, t_top=tt[1] / 1000,
                    ber_top=c70[tt[1]], c70=c70, c20=c20)

    P = pooled(keysboth)
    PR = pooled(keysboth, rcurves)
    boots = []
    for _ in range(n_boot):
        ks = list(rng.choice(keysboth, len(keysboth)))
        try:
            boots.append(pooled(ks))
        except Exception:
            continue

    def ci(name):
        v = np.array([b[name] for b in boots if b.get(name) is not None])
        return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) else None

    S["pooled"] = dict(n_dimms=len(keysboth), mu70=P["mu70"], median70_s=math.exp(P["mu70"]), s_ln=P["s_ln"],
                       s_ln_ci95=ci("s_ln"), ea_ev=P["ea"], ea_kind=P["ea_kind"], ea_ci95=ci("ea"),
                       ea_ev_at_1536ms=P["ea_1536"], k_pow_top=P["k_pow"], k_pow_ci95=ci("k_pow"),
                       slope_2s_logn=local_slope_logn(2.0, P["mu70"], P["s_ln"]),
                       robust_estimator=dict(s_ln=PR["s_ln"], mu70=PR["mu70"], ea_ev=PR["ea"], k_pow_top=PR["k_pow"]))
    # C2 review additions: how much one module drives the fleet Ea, the BER level at which Ea is measured, and the
    # local lognormal width between adjacent measured intervals (does the tail widen or narrow with t?)
    c20 = P["c20"].get(2048, 0.0)
    top20 = max(keysboth, key=lambda d: curves[d][(20.0, NOMINAL_V)].get(2048, 0.0))
    share20 = curves[top20][(20.0, NOMINAL_V)].get(2048, 0.0) / len(keysboth) / c20 if c20 > 0 else None
    P_lo = pooled([d for d in keysboth if d != top20])
    loc = {}
    ts_nz = [t for t in sorted(P["c70"]) if P["c70"][t] > 0]
    for t1, t2 in zip(ts_nz, ts_nz[1:]):
        z1 = -norm_ppf_upper(2 * P["c70"][t1])
        z2 = -norm_ppf_upper(2 * P["c70"][t2])
        loc[f"{t1}-{t2}ms"] = math.log(t2 / t1) / (z2 - z1)
    S["pooled"].update(ea_matched_ber=c20, ea_top_dimm_20C=top20, ea_top_dimm_share_of_20C_mean=share20,
                       ea_ev_without_top_dimm=P_lo["ea"], s_ln_local_between_intervals=loc)

    # 4. test-to-test variability (VRT + DPD + setup upper bound)
    cvs, mm, shifts = [], [], 0
    for (d, T, v, iv), rows in G.items():
        st = group_stats(rows)
        nzc = [r["total"] for r in rows if r["total"] > 0]
        if len(nzc) >= 4 and st["median_nonzero"] >= 50:
            cvs.append(st["cv_nonzero"])
            mm.append(st["maxmin_nonzero"])
            if st["maxmin_nonzero"] > 3:
                shifts += 1
    cvs, mm = np.array(cvs), np.array(mm)
    shift_dimms, elig_dimms = set(), set()
    for (d, T, v, iv), rows in G.items():
        st = group_stats(rows)
        if sum(1 for r in rows if r["total"] > 0) >= 4 and st["median_nonzero"] >= 50:
            elig_dimms.add(d)
            if st["maxmin_nonzero"] > 3:
                shift_dimms.add(d)
    S["variability"] = dict(n_groups=len(cvs), cv_median=float(np.median(cvs)), cv_p90=float(np.percentile(cvs, 90)),
                            maxmin_median=float(np.median(mm)), groups_maxmin_gt3=int(shifts),
                            share_groups_maxmin_gt3=float(shifts / len(cvs)),
                            dimms_eligible=len(elig_dimms), dimms_with_maxmin_gt3=sorted(shift_dimms))

    # 5. bank uniformity at 70 C / 2048 ms / nominal V. One-test-equivalent = the mean of the NONZERO tests, i.e.
    # one charged-pattern test, whose bank counts are Poisson counts of distinct weak cells. (C2 review fix: the
    # mean over all tests halves every count, because half the tests are the zero inverse pattern, and so halves
    # chi2; that hid most of the imbalance.)
    bank_rows = []
    for d in dimms:
        rows = G.get((d, 70.0, NOMINAL_V, 2048))
        if not rows:
            continue
        nzr = [r for r in rows if r["total"] > 0] or rows
        bm = np.mean([r["banks"] for r in nzr], axis=0)
        tot = bm.sum()
        if tot < 40:
            continue
        exp = tot / 8
        chi2 = float(np.sum((bm - exp) ** 2 / exp))
        bank_rows.append(dict(dimm=d, total=float(tot), top_bank_share=float(bm.max() / tot), chi2_7df=chi2))
    chis = np.array([b["chi2_7df"] for b in bank_rows])
    tops = np.array([b["top_bank_share"] for b in bank_rows])
    S["banks"] = dict(n_dimms=len(bank_rows), top_bank_share_median=float(np.median(tops)),
                      top_bank_share_max=float(tops.max()), dimms_chi2_gt_24_3=int(np.sum(chis > 24.3)),
                      note="chi2 > 24.3 is p < 0.001 at 7 dof (one charged test = mean of the nonzero tests); "
                           "expected top share for uniform banks with these counts is ~0.13-0.15")

    # 6. model comparison and re-run
    global EA_MODEL
    m = load_model()
    lim = code_limits(m)
    EA_MODEL = ea_from_ratio(4, 65, 85)
    S["code_limits"] = lim
    ts70 = 4 ** 0.75  # the model's own temperature rule: x4 retention per 20 C, so 85 -> 70 C = x2.83
    comp = []
    for iv in sorted(P["c70"]):
        t = iv / 1000
        comp.append(dict(interval_ms=iv, measured_ber70=P["c70"][iv], measured_ci95=next(
            (r["ber_ci95"] for r in fleet if r["T_C"] == 70.0 and r["vdd"] == NOMINAL_V and r["interval_ms"] == iv), None),
                         model_logn=m.ber_ret(t, "logn", ts70), model_pow3=m.ber_ret(t, "pow3", ts70),
                         model_pow5=m.ber_ret(t, "pow5", ts70)))
    S["model_vs_measured_70C"] = comp
    mu_m, s_m = m.lognormal_params()
    S["model_tail"] = dict(mu85=mu_m, s_ln=s_m, median85_s=math.exp(mu_m), median70_s=math.exp(mu_m) * ts70,
                           implied_ea_85_65=EA_MODEL, implied_ea_65_45=ea_from_ratio(4, 45, 65))
    model_iv = safe_intervals(m, lim, {"85": 1.0, "70": ts70, "65": 4.0, "45": 16.0})
    S["model_intervals_original"] = model_iv

    def rerun(mu70, s_ln, ea_hot, ea_cool, kind="logn", pw=None, vrt=None):
        ts = temp_scales(ea_hot, ea_cool)
        if kind == "logn":
            sw = SwappedRetention(m, "logn", mu85=mu70 - math.log(arrhenius(ea_hot, 70, 85)), s=s_ln)
        else:
            sw = SwappedRetention(m, "pow", f0=pw["f0"], t0=pw["t0"] / arrhenius(ea_hot, 70, 85), k=pw["k"])
        with sw:
            return safe_intervals(m, lim, ts, vrt)

    pw = dict(f0=2 * P["ber_top"], t0=P["t_top"], k=P["k_pow"])  # cell failure fraction at the longest interval
    reruns = {
        "A optimistic: lognormal fit, fitted Ea both ways": rerun(P["mu70"], P["s_ln"], P["ea"], P["ea"]),
        "B central: lognormal fit, model Ea 0.72 eV above 70 C, fitted Ea below": rerun(P["mu70"], P["s_ln"], EA_MODEL, P["ea"]),
        "C pessimistic: power-law tangent, model Ea above 70 C, fitted Ea below": rerun(P["mu70"], P["s_ln"], EA_MODEL, P["ea"], "pow", pw),
    }
    PW = pooled(keysboth, wcurves)
    reruns["D worst-pattern BER (2x), lognormal, model Ea above 70 C"] = rerun(PW["mu70"], PW["s_ln"], EA_MODEL, P["ea"])
    PM = pooled(keysboth, mcurves)
    reruns["E single worst test as random data, lognormal, model Ea above 70 C"] = rerun(PM["mu70"], PM["s_ln"], EA_MODEL, P["ea"])
    S["rerun"] = reruns
    S["pooled_worst_pattern"] = dict(mu70=PW["mu70"], s_ln=PW["s_ln"], ea=PW["ea"])
    S["pooled_max_test"] = dict(mu70=PM["mu70"], s_ln=PM["s_ln"], ea=PM["ea"], ber70=PM["c70"])

    # bootstrap CIs (resampling DIMMs) for the central case B and the optimistic case A
    cb = {"A_ddr5_85": [], "A_ddr4_85": [], "B_ddr5_85": [], "B_ddr4_85": [], "B_ddr5_70": [], "B_ddr4_70": []}
    for bb in boots[: min(len(boots), 200)]:
        if bb.get("ea") is None:
            continue
        for tag, eh in (("A", bb["ea"]), ("B", EA_MODEL)):
            with SwappedRetention(m, "logn", mu85=bb["mu70"] - math.log(arrhenius(eh, 70, 85)), s=bb["s_ln"]):
                cb[f"{tag}_ddr5_85"].append(m.p_max_interval("logn", lim["ddr5_rs8_sec"], 0.5))
                cb[f"{tag}_ddr4_85"].append(m.p_max_interval("logn", lim["ddr4_rs8"], 1.0))
                if tag == "B":
                    a70 = arrhenius(eh, 70, 85)
                    cb["B_ddr5_70"].append(m.p_max_interval("logn", lim["ddr5_rs8_sec"], 0.5 * a70))
                    cb["B_ddr4_70"].append(m.p_max_interval("logn", lim["ddr4_rs8"], a70))
    S["rerun_boot_ci95_s"] = {k: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] for k, v in cb.items() if v}

    # measurement bounds with no BER extrapolation (70 C data; 85 C needs only the temperature step)
    mult = 1 + m.V("vrt_growth_per_day") * m.V("scrub_interval_h") / 24.0
    worst_c70 = {}
    for d in keys70:
        for iv, bv in curves[d][(70.0, NOMINAL_V)].items():
            worst_c70[iv] = max(worst_c70.get(iv, 0.0), bv)
    mb = {}
    for name, key, scale, win in CASES:
        for lab, cv in (("fleet", P["c70"]), ("worst_dimm", worst_c70)):
            b70 = measured_bound(cv, lim[key], mult, scale)
            mb[f"{name} | {lab}"] = dict(i70_s=b70, cut70=b70 / win, i85_s_modelEa=b70 / arrhenius(EA_MODEL, 70, 85),
                                         cut85_modelEa=b70 / arrhenius(EA_MODEL, 70, 85) / win,
                                         i85_s_fittedEa=b70 / arrhenius(P["ea"], 70, 85))
    S["measured_bounds"] = mb
    S["worst_dimm_curve70"] = worst_c70

    # per-DIMM safe intervals: central case B (model Ea above 70 C)
    for r in per:
        if "s_ln" not in r:
            continue
        a85 = arrhenius(EA_MODEL, 70, 85)
        with SwappedRetention(m, "logn", mu85=r["mu70"] - math.log(a85), s=r["s_ln"]):
            r["ddr4_rs8_i85_s"] = m.p_max_interval("logn", lim["ddr4_rs8"], 1.0)
            r["ddr4_rs8_i70_s"] = m.p_max_interval("logn", lim["ddr4_rs8"], a85)
            r["ddr5_rs8_i85_s"] = m.p_max_interval("logn", lim["ddr5_rs8_sec"], 0.5)
            r["ddr5_rs8_i70_s"] = m.p_max_interval("logn", lim["ddr5_rs8_sec"], 0.5 * a85)
    pdv = [r for r in per if "ddr4_rs8_i85_s" in r]

    def dist(key, win):
        v = np.array([r[key] for r in pdv])
        return dict(min=float(v.min()), p10=float(np.percentile(v, 10)), median=float(np.median(v)),
                    min_cut=float(v.min() / win), p10_cut=float(np.percentile(v, 10) / win),
                    median_cut=float(np.median(v) / win))
    S["per_dimm_intervals_caseB"] = dict(n=len(pdv), ddr4_85=dist("ddr4_rs8_i85_s", 0.064), ddr4_70=dist("ddr4_rs8_i70_s", 0.064),
                                         ddr5_85=dist("ddr5_rs8_i85_s", 0.032), ddr5_70=dist("ddr5_rs8_i70_s", 0.032))
    # C2 review addition: fleet refresh-energy cut, DDR5 85 C, case B. A per-module servo runs each module at its own
    # interval (fleet power = mean over modules); one fixed fleet interval must suit the worst module.
    base = m.refresh_numbers(0.032)[0]
    pw5 = [sum(m.refresh_numbers(min(r["ddr5_rs8_i85_s"], 4.0))[:2]) for r in pdv]
    S["fleet_energy_cut_ddr5_85_caseB"] = dict(per_module_servo=float(base / np.mean(pw5)),
                                              fixed_interval_worst_module=float(base / max(pw5)))

    # VRT sensitivity (the data cannot measure the growth rate g): case B at g = 1, 100, 700 per day, 1 h scrub
    vs = {}
    for g in (1.0, 100.0, 700.0):
        rr = rerun(P["mu70"], P["s_ln"], EA_MODEL, P["ea"], vrt=g)
        vs[f"g={g:g}/day"] = {k: rr[k] for k in ("DDR4 / RS-8 chipkill", "DDR5 / RS-8 behind SEC, x0.5 derate")}
    S["vrt_sensitivity_caseB"] = vs
    S["energy_cut_ddr5_85"] = {k: energy_cut(m, v["DDR5 / RS-8 behind SEC, x0.5 derate"]["i85_s"]) for k, v in reruns.items()}
    S["energy_cut_ddr5_85"]["model original"] = energy_cut(m, model_iv["DDR5 / RS-8 behind SEC, x0.5 derate"]["i85_s"])
    S["extrapolation_gap"] = dict(highest_fleet_ber_measured=max(P["c70"].values()),
                                  highest_single_dimm_ber=max(worst_c70.values()),
                                  ddr5_limit=lim["ddr5_rs8_sec"], ddr4_limit=lim["ddr4_rs8"],
                                  decades_fleet_to_ddr5_limit=math.log10(lim["ddr5_rs8_sec"] / max(P["c70"].values())),
                                  decades_fleet_to_ddr4_limit=math.log10(lim["ddr4_rs8"] / max(P["c70"].values())))
    say(f"pooled sigma_ln {P['s_ln']:.3f}, Ea {P['ea']:.3f} eV ({P['ea_kind']}), k_pow {P['k_pow']:.2f}")
    return S


def write_outputs(S, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    js = os.path.join(out_dir, "retention_fit_summary.json")
    with open(js, "w") as f:
        json.dump(S, f, indent=1, default=float)
    cols = ["dimm", "vendor", "s_ln", "median70_s", "slope_2s", "ber70_1024", "ber70_2048", "ber20_2048",
            "ea_ev", "ea_kind", "ddr4_rs8_i85_s", "ddr4_rs8_i70_s", "ddr5_rs8_i85_s", "ddr5_rs8_i70_s"]
    pc = os.path.join(out_dir, "retention_per_dimm.csv")
    with open(pc, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in S["per_dimm"]:
            w.writerow([("" if r.get(c) is None else (f"{r[c]:.4g}" if isinstance(r.get(c), float) else r[c])) for c in cols])
    return js, pc


def print_report(S):
    P = S["pooled"]
    print(f"rows {S['n_rows']} ({S['n_rows_unnamed']} unnamed, excluded), DIMMs {S['n_dimms']} {S['vendors']}, "
          f"duplicate share of nonzero rows {S['duplicate_share_nonzero_rows']:.2f}")
    print("Fleet-mean BER (random-data equivalent), nominal 1.35 V:")
    for r in S["fleet_ber"]:
        if r["vdd"] == NOMINAL_V:
            ub = f" (all zero; <{r['ber_upper95_if_all_zero']:.1e})" if r["ber_upper95_if_all_zero"] else ""
            print(f"  {r['T_C']:.0f} C {r['interval_ms']:5d} ms  {r['ber_mean']:.2e}  CI {r['ber_ci95'][0]:.1e}-"
                  f"{r['ber_ci95'][1]:.1e}  max DIMM {r['ber_max_dimm']:.1e}{ub}")
    print(f"Pooled (n={P['n_dimms']}): sigma_ln {P['s_ln']:.3f} CI {P['s_ln_ci95']}, median70 {P['median70_s']:.3g} s, "
          f"Ea {P['ea_ev']:.3f} eV CI {P['ea_ci95']}, k_pow {P['k_pow_top']:.2f} CI {P['k_pow_ci95']}")
    print(f"Ea matched at BER {P['ea_matched_ber']:.1e}; {P['ea_top_dimm_20C']} holds {P['ea_top_dimm_share_of_20C_mean']:.0%} "
          f"of the 20 C mean; Ea without it {P['ea_ev_without_top_dimm']:.3f} eV; local sigma_ln "
          + ", ".join(f"{k} {v:.2f}" for k, v in P["s_ln_local_between_intervals"].items()))
    print(f"Per-DIMM sigma_ln {S['per_dimm_sigma_ln']}")
    print(f"Per-DIMM Ea {S['per_dimm_ea']}")
    print(f"Variability {S['variability']}")
    print(f"Banks {S['banks']}")
    print("Model vs measured BER at 70 C:")
    for c in S["model_vs_measured_70C"]:
        r = c["model_logn"] / c["measured_ber70"] if c["measured_ber70"] > 0 else float("inf")
        print(f"  {c['interval_ms']:5d} ms measured {c['measured_ber70']:.2e}  model logn {c['model_logn']:.2e} "
              f"(x{r:.3g})  pow3 {c['model_pow3']:.2e}  pow5 {c['model_pow5']:.2e}")
    print("Safe intervals (s) and cut vs the part's own window, at 85 / 70 / 65 C:")
    for lab, block in [("MODEL ORIGINAL", S["model_intervals_original"])] + list(S["rerun"].items()):
        print(" ", lab)
        for k, v in block.items():
            print(f"    {k:40s} 85C {v['i85_s']:.3f} ({v['cut85']:.1f}x)  70C {v['i70_s']:.3f} ({v['cut70']:.1f}x)  "
                  f"65C {v['i65_s']:.3f} ({v['cut65']:.1f}x)  45C {v['i45_s']:.3f}")
    print(f"Bootstrap CIs (s): {S['rerun_boot_ci95_s']}")
    print("Measured bounds (no BER extrapolation):")
    for k, v in S["measured_bounds"].items():
        print(f"    {k:55s} 70C {v['i70_s']:.3f} s ({v['cut70']:.1f}x)  85C(model Ea) {v['i85_s_modelEa']:.3f} s ({v['cut85_modelEa']:.1f}x)")
    print(f"Per-DIMM intervals, case B: {S['per_dimm_intervals_caseB']}")
    print(f"VRT sensitivity, case B: " + "; ".join(f"{g}: DDR4 85C {v['DDR4 / RS-8 chipkill']['i85_s']:.2f} s, DDR5 85C "
          f"{v['DDR5 / RS-8 behind SEC, x0.5 derate']['i85_s']:.2f} s, DDR5 70C {v['DDR5 / RS-8 behind SEC, x0.5 derate']['i70_s']:.2f} s"
          for g, v in S["vrt_sensitivity_caseB"].items()))
    print("Energy cut DDR5 85 C vs 32 ms: " + "; ".join(f"{k[:1]} {v:.1f}x" for k, v in S["energy_cut_ddr5_85"].items()))
    fe = S["fleet_energy_cut_ddr5_85_caseB"]
    print(f"Fleet energy cut DDR5 85 C, case B: per-module servo {fe['per_module_servo']:.1f}x; one fixed interval "
          f"(worst module) {fe['fixed_interval_worst_module']:.1f}x")
    print(f"Extrapolation gap {S['extrapolation_gap']}")


# ------------------------------------------------------------------------------------------------
# Self-test on synthetic data
# ------------------------------------------------------------------------------------------------
def synth_csv(path, n_dimms=12, sigma=1.0, med70=150.0, ea=0.30, seed=7):
    """Synthetic SAFARI-format file: lognormal tails, Arrhenius shift, pattern/inverse trials (inverse = 0 errors),
    exact duplicate blocks (as in the real file)."""
    rnd = random.Random(seed)
    mu70 = math.log(med70)
    rows = []
    for i in range(n_dimms):
        d = f"S{i+1}"
        dm = mu70 + rnd.gauss(0, 0.15)
        for T in (20, 70):
            muT = dm + math.log(arrhenius(ea, T, 70))
            for v in (1.35, 1.2):
                for iv in (64, 128, 256, 512, 1024, 1536, 2048):
                    F = float(F_logn(iv / 1000.0, muT, sigma))
                    block = []
                    for trial in range(6):
                        charged = trial % 2 == 0
                        lam = F * BITS_PER_DIMM / 8 if charged else 0.0
                        banks = [float(np.random.default_rng(rnd.randrange(1 << 30)).poisson(lam)) for _ in range(8)]
                        block.append([d, "S", v, T, iv] + banks + [sum(banks)])
                    rows += block + block  # duplicate the block
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(REQUIRED)
        w.writerows(rows)


def selftest():
    ok = True
    for x in (-3.0, -0.5, 0.0, 0.7, 2.5, 5.0, 7.5):
        rel = abs(float(erfc_np(x)) - math.erfc(x)) / math.erfc(x)
        if rel > 2e-7:
            print(f"FAIL erfc at {x}: rel err {rel:.1e}")
            ok = False
    z = norm_ppf_upper(1e-9)
    if abs(0.5 * math.erfc(z / math.sqrt(2)) / 1e-9 - 1) > 1e-6:
        print("FAIL norm_ppf_upper")
        ok = False
    if abs(ea_from_ratio(arrhenius(0.6, 25, 65), 25, 65) - 0.6) > 1e-9:
        print("FAIL arrhenius round trip")
        ok = False
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "synthetic.csv")
        sig, ea = 1.0, 0.30
        synth_csv(p, sigma=sig, ea=ea)
        S = analyse(load_csv(p), n_boot=40, quiet=True)
        P = S["pooled"]
        print(f"selftest: true sigma {sig}, fitted {P['s_ln']:.3f}; true Ea {ea}, fitted {P['ea_ev']:.3f} "
              f"({P['ea_kind']}); duplicate share {S['duplicate_share_nonzero_rows']:.2f}")
        if abs(P["s_ln"] - sig) / sig > 0.2:
            print("FAIL sigma recovery")
            ok = False
        if P["ea_ev"] is None or abs(P["ea_ev"] - ea) > 0.08:
            print("FAIL Ea recovery")
            ok = False
        if S["banks"]["dimms_chi2_gt_24_3"] != 0:
            print(f"FAIL bank uniformity: synthetic banks are uniform but {S['banks']['dimms_chi2_gt_24_3']} flagged")
            ok = False
        if not (P["ea_ev_without_top_dimm"] and abs(P["ea_ev_without_top_dimm"] - ea) < 0.1
                and S["fleet_energy_cut_ddr5_85_caseB"]["per_module_servo"] > 1):
            print("FAIL C2 additions (Ea without top module / fleet energy cut)")
            ok = False
        h = S["rerun"]
        k = next(iter(h))
        if not all(math.isfinite(v["i85_s"]) and v["i85_s"] > 0 for v in h[k].values()):
            print("FAIL model re-run")
            ok = False
        # model must be restored after the context managers
        m = load_model()
        lim = code_limits(m)
        i0 = m.p_max_interval("logn", lim["ddr5_rs8_sec"], 0.5)
        if abs(i0 - 0.285) > 0.01:
            print(f"FAIL model baseline DDR5 interval {i0:.3f} (expected 0.285 s, dossier 2.5)")
            ok = False
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--csv", help="path to retention_time_profile.csv (see fetch_data.py)")
    ap.add_argument("--out-dir", default=HERE)
    ap.add_argument("--boot", type=int, default=400)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.csv:
        ap.error("--csv is required (or --selftest)")
    S = analyse(load_csv(a.csv), n_boot=a.boot)
    print_report(S)
    js, pc = write_outputs(S, a.out_dir)
    print(f"[wrote {js}]\n[wrote {pc}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
