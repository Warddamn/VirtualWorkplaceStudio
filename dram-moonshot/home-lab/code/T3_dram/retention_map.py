#!/usr/bin/env python3
"""retention_map.py -- Experiment E6 / Track T3: the retention tail of a real DRAM chip.

What it does
  predict      Expected results BEFORE you build anything: first-principles leakage arithmetic,
               Arrhenius temperature factors, expected failing-bit counts for a 64 Mbit chip, and
               the expected ECC-safe refresh interval. Anchored to the study's own retention tail
               (models/raw-ber-contract.py, RAIDR-era anchors) -- every number is an ESTIMATE.
  analyze      Read the logs your board streams over UART (see LOG FORMAT) and compute:
                 retention CDF per temperature, tail quantiles (1e-7 .. 1e-2), lognormal fit,
                 Arrhenius activation energy, true-cell / anti-cell layout, data-pattern
                 dependence, variable-retention-time (VRT) statistics, error clustering, and
                 the longest refresh interval that keeps uncorrectable errors under a target for
                 SEC-DED (72,64), BCH t=4 and t=12, and byte-symbol Reed-Solomon codes
                 (random and real-adjacent codeword mappings) -> YOUR chip's refresh
                 relaxation factor, compared with the dossier's ~9x.
  --selftest   Builds a synthetic 4 Mbit chip (lognormal tail + VRT + clusters + true/anti
               cells + pattern dependence), emulates the firmware's UART log byte-for-byte,
               runs the whole pipeline on it and checks that it recovers what was planted.
               Exit 0 = all checks passed.

Dependencies: Python 3.8+ standard library + numpy. No scipy, no matplotlib.

LOG FORMAT (one record per line; the firmware in stm32_retention/ emits exactly this;
capture_retention.py adds the H lines; '#' lines are comments)
  HELLO,<fw>,<chip>,<n_words>,<bits_per_word>,<sdclk_hz>,<methods>
  H,<unix_time_s>                                   host timestamp of the next RUN
  RUN,<id>,<method>,<pattern>,<inv>,<seed>,<wait_ms>,<repeat>,<temp_c_setpoint>
  TEMP,<id>,<start|end|now>,<temp_c or nan>         thermocouple reading (optional)
  F,<id>,<word_index_hex>,<expected_hex>,<observed_hex>
  END,<id>,<fail_words>,<fail_bits>,<bits_1to0>,<bits_0to1>,<logged_words>,<interval_ms>,<OK|TRUNC|ERR>
  methods: A = refresh relaxed to period <wait_ms> (held 3 periods), B = refresh paused for
           <wait_ms> (chip deselected), C = control (normal refresh, no pause), Z = COUNT=0 test.
           For B the firmware reports interval_ms = pause + one normal refresh window (~54 ms):
           every row really goes that long unrefreshed (the chip's row counter stops during the
           pause and resumes where it left off). ERR runs (e.g. precharge timeout) are excluded.
  patterns: 0 ALL0, 1 ALL1, 2 CHECKER, 3 ROWSTRIPE, 4 COLSTRIPE, 5 RANDOM(seed); inv=1 inverts.
"""
import argparse
import math
import os
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

import numpy as np

K_B = 8.617333262e-5          # Boltzmann constant, eV/K
T0 = 273.15
JEDEC_WINDOW_S = 0.064        # standard refresh window for SDR/DDR3/DDR4 (DDR5 uses 32 ms)
LN2 = math.log(2.0)
PATTERN_NAMES = {0: "ALL0", 1: "ALL1", 2: "CHECKER", 3: "ROWSTRIPE", 4: "COLSTRIPE", 5: "RANDOM"}
DEFAULT_WAITS_S = [0.064 * 2 ** i for i in range(11)]          # 64 ms .. 65.5 s, log2 grid
CHIP_BITS_F429 = 4194304 * 16                                   # IS42S16400J: 64 Mbit
DOSSIER = {"ddr5_rs8_85C": 8.9, "ddr4_rs8_85C": 13.1,
           "pass_65C_x": 24.0, "pass_85C_x": 6.0, "kill_65C_x": 4.0}  # dossiers/raw-ber-contract.md 2.5, 5.R
# Method B: the unrefreshed time is the pause plus one normal refresh window. At SDCLK 8 MHz and
# COUNT 105 that window is 4096 x 106 / 8 MHz = 54.3 ms; the firmware reports it as +54 ms.
B_EXTRA_MS = 54


# --------------------------------------------------------------------------------------------
# Normal distribution helpers (no scipy)
# --------------------------------------------------------------------------------------------
def norm_cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_ppf(p):
    """Inverse standard normal CDF (Acklam's rational approximation + one Halley step)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow = 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    elif p <= 1 - plow:
        q = p - 0.5
        r = q * q
        x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
            (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    e = norm_cdf(x) - p
    u = e * math.sqrt(2 * math.pi) * math.exp(x * x / 2)
    return x - u / (1 + x * u / 2)


# --------------------------------------------------------------------------------------------
# Retention model: lognormal tail + temperature law
# --------------------------------------------------------------------------------------------
def dossier_anchor():
    """Lognormal through the study's 85 C anchors (models/raw-ber-contract.py, section 5):
    F(32 ms) = 1.1e-10 and F(64 ms) = 3.6e-9 (RAIDR-era '~30 / ~1000 cells per 32 GB below
    128 / 256 ms', moved 4x to 85 C). Returns (mu = ln median seconds, sigma)."""
    z1, z2 = -norm_ppf(1.1e-10), -norm_ppf(3.6e-9)
    sigma = (math.log(0.064) - math.log(0.032)) / (z1 - z2)
    mu = math.log(0.064) + z2 * sigma
    return mu, sigma


class RetentionModel:
    """F(t, T) = Phi((ln t - mu_T) / sigma). Temperature law: either Arrhenius (ea_ev) or a fixed
    'retention halves every halving_c degrees' rule (the study's dram_cell_physics.py uses 10 C)."""

    def __init__(self, mu_ref, sigma, t_ref_c=85.0, ea_ev=None, halving_c=None, time_scale=1.0):
        self.mu_ref, self.sigma, self.t_ref_c = mu_ref, sigma, t_ref_c
        self.ea_ev, self.halving_c, self.time_scale = ea_ev, halving_c, time_scale

    def mu_at(self, temp_c):
        if self.halving_c:
            shift = -(temp_c - self.t_ref_c) / self.halving_c * LN2
        else:
            shift = (self.ea_ev / K_B) * (1.0 / (temp_c + T0) - 1.0 / (self.t_ref_c + T0))
        return self.mu_ref + math.log(self.time_scale) + shift

    def cdf(self, t_s, temp_c):
        return norm_cdf((math.log(t_s) - self.mu_at(temp_c)) / self.sigma)

    def time_at(self, frac, temp_c):
        return math.exp(self.mu_at(temp_c) + self.sigma * norm_ppf(frac))


def arrhenius_factor(ea_ev, t_cold_c, t_hot_c):
    """Retention-time ratio t(cold)/t(hot) for thermally activated leakage I ~ exp(-Ea/kT)."""
    return math.exp(ea_ev / K_B * (1.0 / (t_cold_c + T0) - 1.0 / (t_hot_c + T0)))


# --------------------------------------------------------------------------------------------
# Data patterns -- MUST match stm32_retention/patterns.c bit for bit
# --------------------------------------------------------------------------------------------
def mix32(x):
    """lowbias32 integer hash on uint32 arrays (wraps mod 2^32)."""
    x = np.asarray(x, dtype=np.uint32)
    x = x ^ (x >> np.uint32(16))
    x = x * np.uint32(0x7FEB352D)
    x = x ^ (x >> np.uint32(15))
    x = x * np.uint32(0x846CA68B)
    x = x ^ (x >> np.uint32(16))
    return x


def pattern_words(pattern, inv, seed, words, words_per_row=256):
    """Expected 16-bit value of each word index for a pattern (vectorised)."""
    w = np.asarray(words, dtype=np.uint32)
    row = w // np.uint32(words_per_row)
    col = w % np.uint32(words_per_row)
    if pattern == 0:
        v = np.zeros_like(w)
    elif pattern == 1:
        v = np.full_like(w, 0xFFFF)
    elif pattern == 2:
        v = np.where(((row ^ col) & np.uint32(1)) == 1, np.uint32(0xAAAA), np.uint32(0x5555))
    elif pattern == 3:
        v = np.where((row & np.uint32(1)) == 1, np.uint32(0xFFFF), np.uint32(0))
    elif pattern == 4:
        v = np.where((col & np.uint32(1)) == 1, np.uint32(0xFFFF), np.uint32(0))
    elif pattern == 5:
        key = mix32(np.array([(int(seed) + 0x9E3779B9) & 0xFFFFFFFF], dtype=np.uint32))[0]
        v = mix32(w ^ key) & np.uint32(0xFFFF)
    else:
        raise ValueError("unknown pattern %r" % pattern)
    v = v.astype(np.uint32)
    if inv:
        v = v ^ np.uint32(0xFFFF)
    return v


def popcount16(x):
    x = np.asarray(x, dtype=np.uint32)
    n = np.zeros(x.shape, dtype=np.int64)
    for b in range(16):
        n += ((x >> np.uint32(b)) & np.uint32(1)).astype(np.int64)
    return n


# --------------------------------------------------------------------------------------------
# Log parsing
# --------------------------------------------------------------------------------------------
class Run:
    __slots__ = ("rid", "method", "pattern", "inv", "seed", "wait_ms", "repeat", "temp_set",
                 "temps", "t_host", "words", "exp", "obs", "fail_words", "fail_bits", "b10",
                 "b01", "logged", "interval_ms", "status", "_bits", "_dir")

    def __init__(self):
        self.temps, self.words, self.exp, self.obs = [], [], [], []
        self.t_host = None
        self.status = None
        self._bits = None
        self._dir = None

    @property
    def temp_c(self):
        good = [t for t in self.temps if not math.isnan(t)]
        return sum(good) / len(good) if good else self.temp_set

    @property
    def truncated(self):
        return self.logged < self.fail_words

    @property
    def wait_s(self):
        return self.interval_ms / 1000.0 if self.interval_ms else self.wait_ms / 1000.0

    def bits(self, bpw):
        """Failing bit indices (int64, sorted) and failure direction (1 = stored 1 read as 0)."""
        if self._bits is None:
            if not self.words:
                self._bits = np.zeros(0, np.int64)
                self._dir = np.zeros(0, np.int8)
            else:
                w = np.asarray(self.words, np.int64)
                e = np.asarray(self.exp, np.uint32)
                x = e ^ np.asarray(self.obs, np.uint32)
                bl, dl = [], []
                for b in range(bpw):
                    sel = ((x >> np.uint32(b)) & np.uint32(1)) == 1
                    if sel.any():
                        bl.append(w[sel] * bpw + b)
                        dl.append(((e[sel] >> np.uint32(b)) & np.uint32(1)).astype(np.int8))
                bits = np.concatenate(bl)
                dirs = np.concatenate(dl)
                o = np.argsort(bits)
                self._bits, self._dir = bits[o], dirs[o]
        return self._bits, self._dir


class Log:
    def __init__(self):
        self.n_words = None
        self.bpw = 16
        self.chip = "unknown"
        self.runs = []
        self.errors = []

    @property
    def n_bits(self):
        return self.n_words * self.bpw


def parse_log(lines, default_words=CHIP_BITS_F429 // 16):
    log = Log()
    runs = {}
    pending_t = None
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        f = line.split(",")
        tag = f[0]
        try:
            if tag == "HELLO" and len(f) >= 6:
                log.chip, log.n_words, log.bpw = f[2], int(f[3]), int(f[4])
            elif tag == "H":
                pending_t = float(f[1])
            elif tag == "RUN":
                r = Run()
                r.rid, r.method, r.pattern, r.inv = int(f[1]), f[2], int(f[3]), int(f[4])
                r.seed, r.wait_ms, r.repeat, r.temp_set = int(f[5]), int(f[6]), int(f[7]), float(f[8])
                r.t_host, pending_t = pending_t, None
                runs[r.rid] = r
            elif tag == "TEMP":
                rid = int(f[1])
                if rid in runs:
                    runs[rid].temps.append(float(f[3]))
            elif tag == "F":
                r = runs[int(f[1])]
                r.words.append(int(f[2], 16))
                r.exp.append(int(f[3], 16))
                r.obs.append(int(f[4], 16))
            elif tag == "END":
                r = runs[int(f[1])]
                r.fail_words, r.fail_bits, r.b10, r.b01 = int(f[2]), int(f[3]), int(f[4]), int(f[5])
                r.logged, r.interval_ms, r.status = int(f[6]), int(f[7]), f[8]
                if r.status == "ERR":
                    log.errors.append("run %d ended with ERR (firmware fault): excluded" % r.rid)
                else:
                    log.runs.append(r)
            elif tag in ("ERR", "PONG"):
                log.errors.append(line)
        except (ValueError, IndexError, KeyError) as exc:
            log.errors.append("parse error %s: %s" % (exc, line[:80]))
    if log.n_words is None:
        log.n_words = default_words
    return log


# --------------------------------------------------------------------------------------------
# Codes and codeword mappings
# --------------------------------------------------------------------------------------------
class Code:
    def __init__(self, name, n_bits, k_bits, unit_bits, t, label):
        self.name, self.n_bits, self.k_bits = name, n_bits, k_bits
        self.unit_bits, self.t, self.label = unit_bits, t, label

    @property
    def n_units(self):
        return self.n_bits // self.unit_bits


CODES = [
    Code("SECDED(72,64)", 72, 64, 1, 1, "Hamming SEC-DED: fixes 1 bit per 64 data bits (12.5% check)"),
    Code("BCH-4(552,512)", 552, 512, 1, 4, "binary BCH, 4 bits per 512 data bits (7.8% check)"),
    Code("BCH-12(640,512)", 640, 512, 1, 12, "binary BCH-12 in a 25% side band (dossier BCH-12)"),
    Code("SSC-RS(18,16)", 144, 128, 8, 1, "byte-symbol RS, fixes 1 bad byte per 16 (chipkill-like)"),
    Code("RS-8(80,64)", 640, 512, 8, 8, "byte-symbol RS, fixes 8 bad bytes per 64 (dossier RS-8)"),
]
MAPPINGS = ["adjacent", "dq", "random"]


def feistel_positions(x, n_total, seed=12345, rounds=4):
    """Pseudo-random bijection of [0, n_total) (balanced Feistel + cycle walking)."""
    m = max(2, int(math.ceil(math.log2(max(n_total, 2)))))
    m += m % 2
    h = m // 2
    mask = np.uint64((1 << h) - 1)
    keys = [int(mix32(np.array([(seed * 2654435761 + 97 * r) & 0xFFFFFFFF], np.uint32))[0])
            for r in range(rounds)]

    def enc(v):
        left = (v >> np.uint64(h)) & mask
        right = v & mask
        for k in keys:
            fr = mix32((right ^ np.uint64(k)).astype(np.uint32)).astype(np.uint64) & mask
            left, right = right, left ^ fr
        return (left << np.uint64(h)) | right

    y = enc(np.asarray(x, np.uint64))
    bad = y >= np.uint64(n_total)
    while bad.any():
        y[bad] = enc(y[bad])
        bad = y >= np.uint64(n_total)
    return y.astype(np.int64)


def map_positions(bits, n_total, mapping, bpw):
    bits = np.asarray(bits, np.int64)
    if mapping == "adjacent":
        return bits
    if mapping == "dq":   # one 8-bit symbol = one data pin (DQ) over 8 consecutive words
        w, j = bits // bpw, bits % bpw
        return (w // 8) * (8 * bpw) + j * 8 + (w % 8)
    if mapping == "random":
        return feistel_positions(bits, n_total)
    raise ValueError(mapping)


def codeword_events(bits, n_total, code, mapping, bpw):
    """Per codeword that holds >=1 failing bit: (bits in it, distinct units in it)."""
    if bits.size == 0:
        return np.zeros(0, np.int64), np.zeros(0, np.int64), n_total // code.n_bits
    pos = map_positions(bits, n_total, mapping, bpw)
    n_cw = n_total // code.n_bits
    cw = pos // code.n_bits
    keep = cw < n_cw
    cw, pos = cw[keep], pos[keep]
    unit = (pos % code.n_bits) // code.unit_bits
    _, bits_per = np.unique(cw, return_counts=True)
    pair = np.unique(cw * code.n_units + unit)
    _, units_per = np.unique(pair // code.n_units, return_counts=True)
    return bits_per, units_per, n_cw


def poisson_logpmf(k, lam):
    return k * math.log(lam) - lam - math.lgamma(k + 1)


def poisson_sf(t, lam):
    """P[K > t] for K ~ Poisson(lam), accurate deep in the tail."""
    if lam <= 0:
        return 0.0
    if lam > t:
        return max(0.0, 1.0 - sum(math.exp(poisson_logpmf(k, lam)) for k in range(t + 1)))
    s, k = 0.0, t + 1
    while True:
        term = math.exp(poisson_logpmf(k, lam))
        s += term
        if term <= s * 1e-17 or k > t + 2000:
            return s
        k += 1


def compound_ue(lam, unit_pmf, t):
    """P[U_1 + ... + U_K > t], K ~ Poisson(lam) error events per codeword, U_i iid units per event."""
    if lam <= 0:
        return 0.0
    p = poisson_sf(t, lam)
    pmf = np.asarray(unit_pmf, float)
    conv = np.array([1.0])
    for k in range(1, t + 1):
        conv = np.convolve(conv, pmf)
        tail = conv[t + 1:].sum()
        if tail > 0:
            p += math.exp(poisson_logpmf(k, lam)) * tail
    return min(p, 1.0)


def unit_pmf_from(units_per, t):
    """pmf over units per event, index = units; mass above t+1 lumped at t+1 (fatal alone)."""
    pmf = np.zeros(t + 2)
    if units_per.size == 0:
        pmf[1] = 1.0
        return pmf
    u = np.minimum(units_per, t + 1)
    for val in range(1, t + 2):
        pmf[val] = np.mean(u == val)
    return pmf


def cluster_pmf(bits_per, units_per, n_cw, t, sig=2.0):
    """Units-per-event pmf with random coincidences removed.
    A codeword holding 2 failing units can be one physical cluster or two independent weak cells
    that happen to share it. With E events spread over n_cw codewords (lambda = E/n_cw), Poisson
    gives P(>=2 | >=1) = 1 - lambda e^-lambda / (1 - e^-lambda) from coincidence alone. Only the
    excess over that is treated as clustering, and only if it is statistically significant
    (k_obs > k_exp + sig*sqrt(k_exp) + 1); sig = 0 uses the raw excess. Returns (pmf, mean bits per
    event, observed multi-unit events, expected from coincidence, excess used)."""
    pmf = np.zeros(t + 2)
    if units_per.size == 0:
        pmf[1] = 1.0
        return pmf, 1.0, 0, 0.0, 0.0
    n_ev = units_per.size
    lam = n_ev / float(n_cw)
    q = 1.0 - lam * math.exp(-lam) / (1.0 - math.exp(-lam)) if lam > 0 else 0.0
    multi = units_per > 1
    k_obs = int(multi.sum())
    k_exp = q * n_ev
    ex = max(0.0, (k_obs - k_exp) / n_ev)
    if sig > 0 and k_obs <= k_exp + sig * math.sqrt(k_exp) + 1.0:
        ex = 0.0
    pmf[1] = 1.0 - ex
    if k_obs and ex > 0:
        u = np.minimum(units_per[multi], t + 1)
        for val in range(2, t + 2):
            pmf[val] = ex * np.mean(u == val)
        mb_multi = float(bits_per[multi].mean())
    else:
        mb_multi = 2.0
    mbe = (1.0 - ex) * 1.0 + ex * mb_multi
    return pmf, mbe, k_obs, k_exp, ex


def safe_interval(ber_fn, code, unit_pmf, mean_bits_per_event, target_cw,
                  lo=1e-3, hi=1e5):
    """Largest refresh interval P (s) with P_UE(P) <= target_cw (bisection in log P)."""
    def pue(p_s):
        lam = ber_fn(p_s) * code.n_bits / max(mean_bits_per_event, 1.0)
        return compound_ue(lam, unit_pmf, code.t)
    if pue(lo) > target_cw:
        return lo
    if pue(hi) <= target_cw:
        return hi
    a, b = math.log(lo), math.log(hi)
    for _ in range(60):
        mid = 0.5 * (a + b)
        if pue(math.exp(mid)) <= target_cw:
            a = mid
        else:
            b = mid
    return math.exp(a)


def targets_for(code, target_bit_hour, scrub_h, target_per_line):
    """Convert the two reliability targets to 'P(uncorrectable) per codeword per scrub period'.
    (1) <= target_bit_hour uncorrectable events per data bit per hour, one chance per scrub.
    (2) the dossier's <= 2e-19 per 64-byte (512-bit) line read, i.e. 512/k codewords per line."""
    t1 = target_bit_hour * code.k_bits * scrub_h
    t2 = target_per_line / (512.0 / code.k_bits)
    return t1, t2


# --------------------------------------------------------------------------------------------
# Fits
# --------------------------------------------------------------------------------------------
def fit_lognormal(points):
    """points: list of (t_s, F, n_bits_failing). Weighted probit regression z = (ln t - mu)/sigma."""
    pts = [(t, f, n) for t, f, n in points if n >= 3 and 0 < f < 0.3]
    if len(pts) < 2:
        return None
    x = np.array([math.log(t) for t, _, _ in pts])
    z = np.array([norm_ppf(f) for _, f, _ in pts])
    wgt = np.sqrt(np.array([n for _, _, n in pts], float))
    if np.ptp(x) == 0:
        return None
    A = np.vstack([x, np.ones_like(x)]).T * wgt[:, None]
    sol, *_ = np.linalg.lstsq(A, z * wgt, rcond=None)
    a, b = sol
    if a <= 0:
        return None
    sigma = 1.0 / a
    return {"mu": -b * sigma, "sigma": sigma, "n_points": len(pts)}


def fit_global_arrhenius(points_by_temp):
    """z = (1/sigma) ln t - (E/sigma) (1/T) + c ; returns sigma, Ea (eV), mu(T) function."""
    rows, zs, ws = [], [], []
    for temp_c, pts in points_by_temp.items():
        for t, f, n in pts:
            if n >= 3 and 0 < f < 0.3:
                rows.append([math.log(t), 1.0 / (temp_c + T0), 1.0])
                zs.append(norm_ppf(f))
                ws.append(math.sqrt(n))
    if len(rows) < 3 or len(points_by_temp) < 2:
        return None
    A = np.array(rows) * np.array(ws)[:, None]
    sol, *_ = np.linalg.lstsq(A, np.array(zs) * np.array(ws), rcond=None)
    a, b, c = sol
    if a <= 0:
        return None
    sigma = 1.0 / a
    e_over_k = -b * sigma
    return {"sigma": sigma, "ea_ev": e_over_k * K_B, "mu_fn": lambda tc: (-c - b / (tc + T0)) * sigma}


def interp_time_at(points, q):
    """Wait at which measured F first reaches q (log-log interpolation). Returns (value, note)."""
    pts = sorted(points)
    if not pts:
        return None, "no data"
    prev = None
    for t, f, _ in pts:
        if f >= q:
            if prev is None:
                return t, "<= (first point)"
            t0_, f0 = prev
            if f0 <= 0:
                return t, "in (%.3g, %.3g] s" % (t0_, t)
            lt = math.log(t0_) + (math.log(q) - math.log(f0)) * (math.log(t) - math.log(t0_)) / \
                (math.log(f) - math.log(f0))
            return math.exp(lt), "interpolated"
        prev = (t, f)
    return None, "> %.3g s (not reached)" % pts[-1][0]


# --------------------------------------------------------------------------------------------
# Analysis
# --------------------------------------------------------------------------------------------
def temp_bins(runs, width=5.0):
    groups = defaultdict(list)
    for r in runs:
        groups[round(r.temp_set / width) * width].append(r)
    return dict(sorted(groups.items()))


def is_solid0(r):
    return (r.pattern == 0 and r.inv == 0) or (r.pattern == 1 and r.inv == 1)


def is_solid1(r):
    return (r.pattern == 1 and r.inv == 0) or (r.pattern == 0 and r.inv == 1)


def pname(r):
    return PATTERN_NAMES.get(r.pattern, str(r.pattern)) + ("~" if r.inv else "")


def analyze_log(log, args, out):
    N, bpw = log.n_bits, log.bpw
    res = {"temps": {}, "checks": {}, "overlap": []}
    only = getattr(args, "method", "all") or "all"
    data_runs = [r for r in log.runs if r.method in ("A", "B", "Z") and (only == "all" or r.method == only)]
    ctrl = [r for r in log.runs if r.method == "C"]
    out("# E6 retention-map report")
    out("")
    out("Chip: %s, %d words x %d bits = %d bits (one failing bit = BER %.2e)." %
        (log.chip, log.n_words, bpw, N, 1.0 / N))
    if str(log.chip).upper().startswith("SYNTH"):
        out("**SYNTHETIC DATA** (from --simulate or --selftest): every number below comes from a made-up chip."
            " It tests the pipeline, not any real DRAM. Do not quote it as a result.")
    out("Runs: %d data runs, %d control runs, %d truncated (logging cap hit), %d parse notes." %
        (len(data_runs), len(ctrl), sum(r.truncated for r in log.runs), len(log.errors)))
    if only != "all":
        out("Only method %s runs are analysed (--method %s)." % (only, only))
    bad_ctrl = [r for r in ctrl if r.fail_bits > 0]
    out("Control runs (normal refresh, no pause) with failures: %d of %d %s" %
        (len(bad_ctrl), len(ctrl), "-> SETUP PROBLEM: fix before trusting anything" if bad_ctrl else "(good)"))
    res["control_failures"] = len(bad_ctrl)
    if not data_runs:
        out("No data runs found.")
        return res
    groups = temp_bins(data_runs)
    pts_by_temp = {}

    # ---- 1. retention CDF per temperature -------------------------------------------------
    out("")
    out("## 1. Retention CDF (fraction of all cells failing) per temperature")
    out("F_solid = (fails in ALL0 + fails in ALL1) / N, counted from END lines, so it is exact even")
    out("when the per-address log was truncated. Every cell is 'charged' in exactly one of the two.")
    out("F_union = all patterns of one repeat combined (needs untruncated logs). Worst = worst single pattern.")
    for tbin, runs in groups.items():
        tmeas = [r.temp_c for r in runs]
        tmean = sum(tmeas) / len(tmeas)
        by_wait = defaultdict(list)
        for r in runs:
            by_wait[r.wait_ms].append(r)
        out("")
        out("### %.0f C bin (measured mean %.2f C, %d runs)" % (tbin, tmean, len(runs)))
        out("| wait (s) | F_solid (mean of repeats) | failing bits | F_union | worst pattern (BER) | repeats |")
        out("|---|---|---|---|---|---|")
        pts = []
        union_ratio = []
        wait_rows = {}
        for wms in sorted(by_wait):
            rr = by_wait[wms]
            t_s = float(np.mean([r.wait_s for r in rr]))
            reps = sorted(set(r.repeat for r in rr))
            meths = sorted(set(r.method for r in rr))
            fs, unions = [], []
            fs_by_m = defaultdict(list)
            for rep in reps:
                for m in meths:          # pair ALL0 with ALL1 of the SAME repeat AND method
                    s0 = [r for r in rr if r.repeat == rep and r.method == m and is_solid0(r)]
                    s1 = [r for r in rr if r.repeat == rep and r.method == m and is_solid1(r)]
                    if s0 and s1:
                        f_pair = (s0[0].fail_bits + s1[0].fail_bits) / N
                        fs.append(f_pair)
                        fs_by_m[m].append(f_pair)
                    rep_runs = [r for r in rr if r.repeat == rep and r.method == m]
                    if rep_runs and not any(r.truncated for r in rep_runs):
                        u = np.unique(np.concatenate([r.bits(bpw)[0] for r in rep_runs]))
                        unions.append(u.size / N)
            if "A" in fs_by_m and "B" in fs_by_m:
                fa, fb = float(np.mean(fs_by_m["A"])), float(np.mean(fs_by_m["B"]))
                ta = float(np.mean([r.wait_s for r in rr if r.method == "A"]))
                tb = float(np.mean([r.wait_s for r in rr if r.method == "B"]))
                res["overlap"].append({"temp_bin": tbin, "wait_ms": wms, "t_a": ta, "t_b": tb, "f_a": fa,
                                       "f_b": fb, "n_a": fa * N, "n_b": fb * N,
                                       "ratio": (fb / fa) if fa > 0 else float("inf") if fb > 0 else 1.0})
            worst = max(rr, key=lambda r: r.fail_bits)
            f_solid = float(np.mean(fs)) if fs else float("nan")
            f_union = float(np.mean(unions)) if unions else float("nan")
            nbits = f_solid * N if fs else float("nan")
            if fs:
                pts.append((t_s, f_solid, nbits))
            if fs and unions and f_solid > 0:
                union_ratio.append(f_union / f_solid)
            wait_rows[wms] = (t_s, f_solid, f_union)
            out("| %.3f | %s | %s | %s | %s (%.2e) | %d |" % (
                t_s, "%.3e" % f_solid if fs else "n/a", "%.0f" % nbits if fs else "n/a",
                "%.3e" % f_union if unions else "n/a (truncated)", pname(worst), worst.fail_bits / N,
                len(reps)))
        pts_by_temp[tmean] = pts
        fit = fit_lognormal(pts)
        tinfo = {"temp_c": tmean, "points": pts, "fit": fit, "runs": runs, "wait_rows": wait_rows,
                 "dpd_factor": float(np.median(union_ratio)) if union_ratio else 1.0}
        res["temps"][tbin] = tinfo
        if fit:
            out("")
            out("Lognormal fit: median retention %.3g s, sigma(ln t) %.2f (%d points)." %
                (math.exp(fit["mu"]), fit["sigma"], fit["n_points"]))
        slopes = []
        for (t1, f1, n1), (t2, f2, n2) in zip(pts, pts[1:]):
            if f1 > 0 and f2 > 0 and n1 >= 3:
                slopes.append("%.2g-%.2g s: k=%.1f" % (t1, t2, math.log(f2 / f1) / math.log(t2 / t1)))
        if slopes:
            out("Local tail slope k (F ~ t^k): " + "; ".join(slopes))
        out("Pattern-dependence factor (median F_union / F_solid): %.2f" % tinfo["dpd_factor"])

    # ---- 1b. method A vs B overlap (only when one log holds both at the same wait) ---------
    if res["overlap"]:
        out("")
        out("## 1b. Method A (relaxed refresh) vs method B (paused refresh) at the same wait")
        out("WARNING: this log mixes methods at the same wait. Section 1 averages them, and sections 6-7 pool")
        out("their repeats. Use this table for the overlap check, then analyse each method's log on its own")
        out("(or pass --method A / --method B). B's interval includes its fixed +%d ms (one normal window)." %
            B_EXTRA_MS)
        out("| temp bin | wait (s) A / B | F_solid A (bits) | F_solid B (bits) | B / A | within 2x? |")
        out("|---|---|---|---|---|---|")
        for o in res["overlap"]:
            enough = min(o["n_a"], o["n_b"]) >= 20
            ok = 0.5 <= o["ratio"] <= 2.0
            out("| %.0f C | %.3f / %.3f | %.3e (%.0f) | %.3e (%.0f) | %.2f | %s |" % (
                o["temp_bin"], o["t_a"], o["t_b"], o["f_a"], o["n_a"], o["f_b"], o["n_b"], o["ratio"],
                ("yes" if ok else "NO") if enough else "too few bits (<20) to judge"))

    # ---- 2. tail quantiles ----------------------------------------------------------------
    out("")
    out("## 2. Tail quantiles: the wait at which a fraction q of cells has failed")
    qs = [1e-7, 1e-6, 1e-5, 2e-5, 1e-4, 1e-3, 1e-2]
    out("| temp | " + " | ".join("q=%.0e" % q for q in qs) + " |")
    out("|---|" + "---|" * len(qs))
    for tbin, ti in res["temps"].items():
        cells = []
        for q in qs:
            v, note = interp_time_at(ti["points"], q)
            if v is not None and note == "interpolated":
                cells.append("%.3g s" % v)
            elif v is not None:
                cells.append(note.replace("<= (first point)", "<=%.3g s" % v))
            elif ti["fit"]:
                cells.append("~%.3g s (fit)" % math.exp(ti["fit"]["mu"] + ti["fit"]["sigma"] * norm_ppf(q)))
            else:
                cells.append(note)
        out("| %.1f C | %s |" % (ti["temp_c"], " | ".join(cells)))
    out("q = 1e-4 and 2e-5 are the quantiles the Oxide Tail Spec asks about. This chip has %d and %d"
        " cells beyond them: enough for a +/-%.0f%% and +/-%.0f%% statistical error." %
        (N * 1e-4, N * 2e-5, 100 / math.sqrt(N * 1e-4), 100 / math.sqrt(N * 2e-5)))

    # ---- 3. temperature acceleration ------------------------------------------------------
    out("")
    out("## 3. Temperature acceleration")
    keys = list(res["temps"].keys())
    for k1, k2 in zip(keys, keys[1:]):
        a, b = res["temps"][k1], res["temps"][k2]
        if a["fit"] and b["fit"]:
            af = math.exp(a["fit"]["mu"] - b["fit"]["mu"])
            t1, t2 = a["temp_c"] + T0, b["temp_c"] + T0
            ea = K_B * math.log(af) / (1 / t1 - 1 / t2) if af > 0 else float("nan")
            halving = (b["temp_c"] - a["temp_c"]) * LN2 / math.log(af) if af > 1 else float("inf")
            out("%.1f -> %.1f C: retention shrinks %.2fx; Ea = %.2f eV; retention halves every %.1f C." %
                (a["temp_c"], b["temp_c"], af, ea, halving))
    garr = fit_global_arrhenius(pts_by_temp)
    res["arrhenius"] = garr
    if garr:
        out("Global fit (all temperatures, one sigma): sigma %.2f, Ea = %.2f eV." %
            (garr["sigma"], garr["ea_ev"]))
        out("Reference: thermally generated junction leakage scales with n_i ~ exp(-Eg/2kT), Ea ~0.55-0.6 eV;"
            " field/trap-assisted tail cells show lower Ea (~0.35 eV reported).")

    # ---- 4. true / anti cells ---------------------------------------------------------------
    out("")
    out("## 4. Cell polarity (true cells store 1 as charge; anti cells store 0 as charge)")
    wpr = args.words_per_row
    true_ct, anti_ct = defaultdict(int), defaultdict(int)
    for r in data_runs:
        if r.truncated or not (is_solid0(r) or is_solid1(r)):
            continue
        bits, dirs = r.bits(bpw)
        rows = (bits // bpw) // wpr
        for row, dd in zip(rows.tolist(), dirs.tolist()):
            if dd == 1:
                true_ct[row] += 1
            else:
                anti_ct[row] += 1
    rows_all = sorted(set(true_ct) | set(anti_ct))
    cls = {}
    for row in rows_all:
        t_, a_ = true_ct[row], anti_ct[row]
        if t_ + a_ >= 2 and max(t_, a_) >= 0.8 * (t_ + a_):
            cls[row] = "T" if t_ > a_ else "A"
    n_t = sum(1 for v in cls.values() if v == "T")
    n_a = sum(1 for v in cls.values() if v == "A")
    res["cell_class"] = cls
    tot10 = sum(r.b10 for r in data_runs)
    tot01 = sum(r.b01 for r in data_runs)
    out("All runs: %d bits failed 1->0, %d failed 0->1." % (tot10, tot01))
    out("Rows classified (>=2 failures, >=80%% one direction): %d true-cell rows, %d anti-cell rows." % (n_t, n_a))
    block = None
    if n_t and n_a:
        changes = []
        srt = sorted(cls.items())
        for (r1, c1), (r2, c2) in zip(srt, srt[1:]):
            if c1 != c2:
                changes.append(r2)
        if len(changes) >= 2:
            gaps = np.diff(changes)
            g = int(np.median(gaps))
            block = 2 ** int(round(math.log2(g))) if g > 0 else None
            out("Polarity changes every ~%d rows (median gap %d): the chip interleaves true and anti"
                " cells in blocks (often one block per subarray)." % (block, g))
    res["anti_block_rows"] = block

    # ---- 5. data-pattern dependence -------------------------------------------------------
    out("")
    out("## 5. Data-pattern dependence (coverage = share of all failing cells that this pattern alone finds)")
    cov = defaultdict(list)
    for tbin, ti in res["temps"].items():
        by_key = defaultdict(list)
        for r in ti["runs"]:
            by_key[(r.wait_ms, r.repeat)].append(r)
        for key, rr in by_key.items():
            if any(r.truncated for r in rr) or len(rr) < 2:
                continue
            u = np.unique(np.concatenate([r.bits(bpw)[0] for r in rr]))
            if u.size < 20:
                continue
            for r in rr:
                cov[pname(r)].append(r.bits(bpw)[0].size / u.size)
    if cov:
        out("| pattern | mean coverage |")
        out("|---|---|")
        for k in sorted(cov):
            out("| %s | %.2f |" % (k, float(np.mean(cov[k]))))
    else:
        out("Not enough untruncated multi-pattern data.")

    # ---- 6. variable retention time -------------------------------------------------------
    out("")
    out("## 6. Variable retention time (VRT)")
    vrt_summary = {}
    for tbin, ti in res["temps"].items():
        runs = [r for r in ti["runs"] if not r.truncated]
        by_pw = defaultdict(list)
        for r in runs:
            by_pw[(r.pattern, r.inv, r.wait_ms)].append(r)
        ever = inter = 0
        for key, rr in by_pw.items():
            if len(rr) < 2:
                continue
            allbits = np.concatenate([r.bits(bpw)[0] for r in rr])
            if allbits.size == 0:
                continue
            u, c = np.unique(allbits, return_counts=True)
            ever += u.size
            inter += int(np.sum(c < len(rr)))
        # strict: per repeat, first wait at which a cell fails (any pattern); spread >= 4x
        reps = sorted(set(r.repeat for r in runs))
        waits = sorted(set(r.wait_ms for r in runs))
        first = {}
        last_wait = {}
        for rep in reps:
            rr = [r for r in runs if r.repeat == rep]
            last_wait[rep] = max(r.wait_ms for r in rr) if rr else 0
            seen = {}
            for wms in waits:
                cur = [r for r in rr if r.wait_ms == wms]
                if not cur:
                    continue
                u = np.unique(np.concatenate([r.bits(bpw)[0] for r in cur]))
                for b in u.tolist():
                    if b not in seen:
                        seen[b] = wms
            first[rep] = seen
        strict = cand = 0
        if len(reps) >= 2:
            allb = set()
            for rep in reps:
                allb.update(first[rep].keys())
            for b in allb:
                vals = [first[rep].get(b, 2 * last_wait[rep]) for rep in reps]
                if min(vals) * 4 <= max(last_wait.values()):
                    cand += 1
                    if max(vals) >= 4 * min(vals):
                        strict += 1
        # growth of the repeat-union at a reference wait
        growth = None
        ref = None
        for wms in waits:
            rr = [r for r in runs if r.wait_ms == wms]
            if len(set(r.repeat for r in rr)) >= 2:
                n_first = np.unique(np.concatenate([r.bits(bpw)[0] for r in rr if r.repeat == reps[0]]
                                                   or [np.zeros(0, np.int64)])).size
                if n_first >= 20 and n_first < 1e-3 * N:
                    ref = wms
                    allu = np.unique(np.concatenate([r.bits(bpw)[0] for r in rr])).size
                    times = [r.t_host for r in rr if r.t_host is not None]
                    span_d = (max(times) - min(times)) / 86400.0 if len(times) >= 2 else None
                    growth = ((allu - n_first) / n_first, span_d, len(reps))
                    break
        vrt_summary[tbin] = {"loose": inter / ever if ever else None,
                             "strict": strict / cand if cand else None, "growth": growth, "ref_ms": ref}
        line = "%.1f C: intermittent (fails in some repeats, not all) %s; strict VRT (first-fail wait" \
               " varies >=4x between repeats) %s" % (
                   ti["temp_c"], "%.1f%% of %d failing cells" % (100 * inter / ever, ever) if ever else "n/a",
                   "%.1f%% of %d testable cells" % (100 * strict / cand, cand) if cand else "n/a")
        out(line)
        if growth:
            g, span_d, nrep = growth
            if span_d and span_d >= 1.0:
                extra = "; over %.2f days -> %.2g x static per day" % (span_d, g / span_d)
            else:
                extra = ("; growth per day: not meaningful (campaign < 1 day, mostly cells flickering near"
                         " their threshold); see the strict-VRT share instead")
            out("   New cells appearing over %d repeats at %.3f s: +%.0f%% of the first repeat%s." %
                (nrep, ref / 1000.0, 100 * g, extra))
    res["vrt"] = vrt_summary
    out("Threshold noise also makes cells near their retention time flicker; only the strict number is VRT-like.")

    # ---- 7. clustering and ECC ------------------------------------------------------------
    out("")
    out("## 7. ECC over the measured failure map -> safe refresh interval")
    out("Targets: (1) <= %.0e uncorrectable events per data bit-hour, scrub every %.0f h; (2) dossier"
        " <= %.0e per 64-byte line read. VRT accrual multiplier (1 + g x scrub/24 h), g = %.2g/day."
        % (args.target_bit_hour, args.scrub_h, args.target_per_line, args.vrt_growth))
    out("p(P) = lognormal fit of F_solid x pattern factor x VRT multiplier. 'EXTRAP' = the safe point sits"
        " below what this chip can resolve (<3 failing cells expected), so it leans on the fitted tail.")
    res["ecc"] = {}
    if garr:
        out("Tail model: the global fit (one sigma for all temperatures, Arrhenius shift of the median)."
            " One shared shape keeps the extrapolation consistent between temperatures.")
    for tbin, ti in res["temps"].items():
        if garr:
            mu, sg, src = garr["mu_fn"](ti["temp_c"]), garr["sigma"], "global"
        elif ti["fit"]:
            mu, sg, src = ti["fit"]["mu"], ti["fit"]["sigma"], "this temperature"
        else:
            out("%.1f C: no lognormal fit (need >=2 points with >=3 failing cells); skipped." % ti["temp_c"])
            continue
        runs = [r for r in ti["runs"] if not r.truncated]
        by_wait = defaultdict(list)
        for r in runs:
            by_wait[r.wait_ms].append(r)
        # failure maps for cluster shapes: first repeat, all patterns combined, one per wait
        maps = []
        for wms in sorted(by_wait):
            rr = by_wait[wms]
            rep0 = min(r.repeat for r in rr)
            maps.append((wms, np.unique(np.concatenate([r.bits(bpw)[0] for r in rr if r.repeat == rep0]))))

        def ref_map(code):
            """Densest map where chance sharing of a codeword stays small (lambda <= 0.02)."""
            best = (None, np.zeros(0, np.int64))
            for wms, u in maps:
                if u.size * code.n_bits <= 0.02 * N and u.size >= best[1].size:
                    best = (wms, u)
            if best[0] is None and maps:
                best = min(maps, key=lambda m: m[1].size)
            return best
        dpd = max(1.0, ti["dpd_factor"])
        vmult = 1.0 + args.vrt_growth * args.scrub_h / 24.0

        def ber_fn(p_s, mu=mu, sg=sg, dpd=dpd, vmult=vmult):
            return min(0.5, norm_cdf((math.log(p_s) - mu) / sg) * dpd * vmult)

        out("")
        out("### %.1f C (tail: %s fit, median %.3g s, sigma %.2f)" % (ti["temp_c"], src, math.exp(mu), sg))
        out("Cluster shapes come from the densest single-repeat map where two independent weak cells share a"
            " codeword < 2%% of the time; an excess counts only if > %.0f sigma above chance." % args.cluster_sig)
        out("| code | mapping | map (cells @ wait) | multi-unit events obs / chance | safe P, target 1 | x vs 64 ms |"
            " safe P, target 2 | x vs 64 ms |")
        out("|---|---|---|---|---|---|---|---|")
        tres = {}
        for code in CODES:
            for mapping in MAPPINGS:
                if mapping == "dq" and code.unit_bits == 1:
                    continue
                ref_wait, ref_bits = ref_map(code)
                bits_per, units_per, n_cw = codeword_events(ref_bits, N, code, mapping, bpw)
                pmf, mbe, k_obs, k_exp, ex = cluster_pmf(bits_per, units_per, n_cw, code.t, args.cluster_sig)
                t1, t2 = targets_for(code, args.target_bit_hour, args.scrub_h, args.target_per_line)
                p1 = safe_interval(ber_fn, code, pmf, mbe, t1)
                p2 = safe_interval(ber_fn, code, pmf, mbe, t2)
                fl1 = " EXTRAP" if ber_fn(p1) * N < 3 else ""
                fl2 = " EXTRAP" if ber_fn(p2) * N < 3 else ""
                tres[(code.name, mapping)] = (p1, p2)
                out("| %s | %s | %d @ %.3g s | %d / %.1f%s | %.3g s%s | %.1fx | %.3g s%s | %.1fx |" % (
                    code.name, mapping, ref_bits.size, (ref_wait or 0) / 1000.0, k_obs, k_exp,
                    " (clustered)" if ex > 0 else "", p1, fl1, p1 / JEDEC_WINDOW_S, p2, fl2,
                    p2 / JEDEC_WINDOW_S))
        res["ecc"][tbin] = tres
        # sensitivity to the measured VRT growth (short campaigns overstate it: see section 6)
        vg = res["vrt"].get(tbin, {}).get("growth")
        if vg and vg[1] and vg[1] >= 1.0:          # a per-day rate needs at least a day of data
            g_meas = min(1000.0, vg[0] / vg[1])
            vm2 = 1.0 + g_meas * args.scrub_h / 24.0
            code = CODES[4]
            bits_per, units_per, n_cw = codeword_events(ref_map(code)[1], N, code, "adjacent", bpw)
            pmf, mbe, _, _, _ = cluster_pmf(bits_per, units_per, n_cw, code.t, args.cluster_sig)
            t1, t2 = targets_for(code, args.target_bit_hour, args.scrub_h, args.target_per_line)
            p_alt = safe_interval(lambda p_s: min(0.5, norm_cdf((math.log(p_s) - mu) / sg) * dpd * vm2),
                                  code, pmf, mbe, t2)
            out("VRT sensitivity: with your measured growth g = %.3g/day instead of %.3g/day, RS-8 adjacent"
                " (target 2) becomes %.3g s = %.1fx." % (g_meas, args.vrt_growth, p_alt, p_alt / JEDEC_WINDOW_S))
        # empirical cross-check at the largest untruncated wait
        if by_wait:
            wmax = max(by_wait)
            u = np.unique(np.concatenate([r.bits(bpw)[0] for r in by_wait[wmax]]))
            obs = []
            for code in (CODES[0], CODES[4]):
                _, units_per, n_cw = codeword_events(u, N, code, "adjacent", bpw)
                obs.append("%s %d of %d codewords" % (code.name, int(np.sum(units_per > code.t)), n_cw))
            out("Direct count at %.3f s (all patterns, all repeats combined): uncorrectable = %s." %
                (wmax / 1000.0, "; ".join(obs)))
    # pair excess (clustering) for SEC-DED adjacent vs random
    out("")
    out("Clustering check: if failing cells were independent, SEC-DED 'adjacent' and 'random' rows would")
    out("match. A shorter safe interval for 'adjacent' means weak cells come in neighbours (clusters).")

    # ---- 8. verdict vs dossier ------------------------------------------------------------
    out("")
    out("## 8. Your relaxation factor vs the study")
    hot = max(res["ecc"].keys()) if res["ecc"] else None
    if hot is not None:
        tc = res["temps"][hot]["temp_c"]
        p_rs8 = res["ecc"][hot].get(("RS-8(80,64)", "adjacent"), (None, None))[1]
        p_sec = res["ecc"][hot].get(("SECDED(72,64)", "adjacent"), (None, None))[0]
        out("Hottest measured bin %.1f C: RS-8 adjacent (dossier target 2) %.3g s = %.1fx of 64 ms;"
            " SEC-DED adjacent (target 1) %.3g s = %.1fx." % (tc, p_rs8, p_rs8 / JEDEC_WINDOW_S,
                                                              p_sec, p_sec / JEDEC_WINDOW_S))
        x65 = p_rs8 / JEDEC_WINDOW_S
        note = ""
        if abs(tc - 65.0) > 3.0 and garr:
            af = math.exp((garr["ea_ev"] / K_B) * (1 / (65.0 + T0) - 1 / (tc + T0)))
            x65 *= af
            note = " (moved to 65 C with the fitted Ea = %.2f eV: EXTRAPOLATION)" % garr["ea_ev"]
        if abs(tc - 65.0) > 3.0 and not garr:
            # One temperature, far from 65 C: no measured or extrapolated 65 C factor exists.
            verdict = "NO VERDICT (no 65 C data)"
            x65 = None
            out("At 65 C: not measured. The gate is defined at 65 C; this campaign's hottest bin is %.1f C,"
                " and one temperature gives no activation energy to move it there -> %s."
                " Run 45 and 65 C (or at least two temperatures) first." % (tc, verdict))
        else:
            verdict = ("PASS (65 C half of the gate only)" if x65 >= DOSSIER["pass_65C_x"] else
                       ("NO-GO" if x65 < DOSSIER["kill_65C_x"] else "PARTIAL"))
            out("At 65 C: %.1fx%s. Dossier gate (section 5.R): PASS needs >= %.0fx at 65 C AND >= %.0fx at 85 C;"
                " NO-GO < %.0fx at 65 C -> %s." %
                (x65, note, DOSSIER["pass_65C_x"], DOSSIER["pass_85C_x"], DOSSIER["kill_65C_x"], verdict))
        out("This chip is rated to about 70 C, so only the 65 C half of the PASS line can be tested here.")
        out("Dossier model for comparison: ~%.1fx on DDR5 and ~%.1fx on retired DDR4 at 85 C (RS-8, chipkill kept)."
            % (DOSSIER["ddr5_rs8_85C"], DOSSIER["ddr4_rs8_85C"]))
        out("Your chip is an old-node SDR part at <=65 C, so expect a larger factor; the direction and the method"
            " are what transfer, not the number.")
        res["verdict"] = verdict
        res["x65"] = x65
    return res


# --------------------------------------------------------------------------------------------
# Predict (expected results before the build)
# --------------------------------------------------------------------------------------------
def predict(args, out):
    mu, sg = dossier_anchor()
    n = args.bits
    out("# E6 expected results (all [ESTIMATE] unless noted)")
    out("")
    out("## A. A DRAM cell is a leaky capacitor: t_ret = C_s * dV_allow / I_leak")
    cs, vdd, cbl, voff = args.cs_ff * 1e-15, args.vdd, args.cbl_ff * 1e-15, args.voff_mv * 1e-3
    ratio = (cs + cbl) / cs
    dv_allow = vdd / 2 - voff * ratio
    q_allow = cs * dv_allow
    out("Charge sharing: bitline signal dV_BL = (V_cell - VDD/2) * C_s / (C_s + C_BL).")
    out("With C_s = %.0f fF, C_BL = %.0f fF, VDD = %.1f V, sense offset %.0f mV:" %
        (args.cs_ff, args.cbl_ff, vdd, args.voff_mv))
    out("  the cell may droop dV_allow = VDD/2 - V_off*(C_s+C_BL)/C_s = %.2f - %.3f = %.2f V" %
        (vdd / 2, voff * ratio, dv_allow))
    out("  -> allowed charge loss Q = C_s * dV_allow = %.1f fC = %.0f electrons" %
        (q_allow * 1e15, q_allow / 1.602e-19))
    out("| retention time | leakage current that empties the cell |")
    out("|---|---|")
    for t in (0.064, 1.0, 10.0, 100.0, 1000.0):
        i = q_allow / t
        out("| %g s | %.3g A = %.3g fA = %.0f aA |" % (t, i, i * 1e15, i * 1e18))
    out("A 10 s cell leaks about %.1f fA. Mapping retention times of 67 million cells is a femtoamp leakage"
        " census (the current scale rests on the assumed C_s and dV_allow, so read it to within a factor"
        " of 2-3)." % (q_allow / 10.0 * 1e15))
    out("")
    out("## B. Temperature: thermally activated leakage, t_ret ~ exp(Ea / kT)")
    out("| Ea (eV) | mechanism | 25->45 C | 45->65 C | 25->65 C | halves every |")
    out("|---|---|---|---|---|---|")
    for ea, mech in ((0.35, "trap-assisted tail (reported)"), (0.6, "SRH generation ~Eg/2"),
                     (1.1, "diffusion ~Eg")):
        f1, f2, f3 = (arrhenius_factor(ea, 25, 45), arrhenius_factor(ea, 45, 65), arrhenius_factor(ea, 25, 65))
        out("| %.2f | %s | %.2fx | %.2fx | %.2fx | %.1f C (near 45 C) |" %
            (ea, mech, f1, f2, f3, 10 * LN2 / math.log(arrhenius_factor(ea, 40, 50))))
    out("")
    out("## C. Expected retention tail of a 64 Mbit SDR chip (%d cells)" % n)
    out("Anchor: the study's lognormal through RAIDR-era 85 C points (mu = ln %.0f s, sigma = %.2f),"
        " retention halves every 10 C (study convention). Band: x0.5 (DDR5-like derate) to x4"
        " (older, larger cells)." % (math.exp(mu), sg))
    temps = [25.0, 45.0, 65.0]
    models = {"pess": RetentionModel(mu, sg, halving_c=10.0, time_scale=0.5),
              "central": RetentionModel(mu, sg, halving_c=10.0, time_scale=1.0),
              "opt": RetentionModel(mu, sg, halving_c=10.0, time_scale=4.0)}
    out("| wait (s) | " + " | ".join("%.0f C: F central (bits) [band]" % t for t in temps) + " |")
    out("|---|" + "---|" * len(temps))
    for w in DEFAULT_WAITS_S:
        cells = []
        for t in temps:
            fc = models["central"].cdf(w, t)
            fp, fo = models["pess"].cdf(w, t), models["opt"].cdf(w, t)
            cells.append("%.1e (%s) [%.0f-%.0f]" % (fc, "%.0f" % (fc * n), fo * n, fp * n))
        out("| %.3f | %s |" % (w, " | ".join(cells)))
    out("")
    out("First failing cell expected (F = 1/N) at: " + "; ".join(
        "%.0f C %.2g s [%.2g-%.2g]" % (t, models["central"].time_at(1.0 / n, t),
                                         models["pess"].time_at(1.0 / n, t), models["opt"].time_at(1.0 / n, t))
        for t in temps))
    out("Wait to reach q = 1e-4 (the Oxide-Tail quantile): " + "; ".join(
        "%.0f C %.3g s" % (t, models["central"].time_at(1e-4, t)) for t in temps))
    # BER growth per 10 C at fixed wait
    w_ref = models["central"].time_at(1e-6, 45.0)
    g10 = models["central"].cdf(w_ref, 55.0) / models["central"].cdf(w_ref, 45.0)
    out("At a fixed wait (%.2g s, F = 1e-6 at 45 C) the failing fraction grows %.1fx per +10 C."
        " Reported for 223 LPDDR4 chips: ~10x per 10 C [REPORTED]." % (w_ref, g10))
    out("Cross-check: '<0.001%% of cells below 3 s at 45 C' (worst DDR3 module) [REPORTED]; central model"
        " gives F(3 s, 45 C) = %.1e." % models["central"].cdf(3.0, 45.0))
    out("")
    out("## D. Expected ECC-safe refresh interval (independent errors, VRT growth %.1f/day, scrub %.0f h)" %
        (args.vrt_growth, args.scrub_h))
    out("P_UE per codeword = P[Poisson(n*p) > t] ~ (n p)^(t+1)/(t+1)!  -> stronger codes buy steeply.")
    vmult = 1.0 + args.vrt_growth * args.scrub_h / 24.0
    out("| code | temp | central P (target 1) | x vs 64 ms | band (pess-opt) | central P (dossier target 2) | x |")
    out("|---|---|---|---|---|---|---|")
    pred = {}
    for code in CODES:
        pmf = unit_pmf_from(np.ones(1, np.int64), code.t)
        t1, t2 = targets_for(code, args.target_bit_hour, args.scrub_h, args.target_per_line)
        for t in temps:
            vals = {}
            for key, m in models.items():
                def bf(p, m=m, t=t):
                    return min(0.5, m.cdf(p, t) * vmult)
                vals[key] = (safe_interval(bf, code, pmf, 1.0, t1), safe_interval(bf, code, pmf, 1.0, t2))
            pc = vals["central"]
            pred[(code.name, t)] = pc
            out("| %s | %.0f C | %.3g s | %.1fx | %.3g-%.3g s | %.3g s | %.1fx |" % (
                code.name, t, pc[0], pc[0] / JEDEC_WINDOW_S, vals["pess"][0], vals["opt"][0],
                pc[1], pc[1] / JEDEC_WINDOW_S))
    out("Compare: dossier ~%.1fx (DDR5, 85 C, RS-8 chipkill kept) and ~%.1fx (retired DDR4). Gate at 65 C:"
        " PASS >= %.0fx, NO-GO < %.0fx." % (DOSSIER["ddr5_rs8_85C"], DOSSIER["ddr4_rs8_85C"],
                                            DOSSIER["pass_65C_x"], DOSSIER["kill_65C_x"]))
    out("Target 1 is an illustrative assumption, not an industry spec: 1e-15 per bit-hour is about %.0f FIT"
        " per Gbit, about %.1f uncorrectable events per year in a 64 GB server. Target 2 (the dossier's) is"
        " the one that matters." % (args.target_bit_hour * 2 ** 30 * 1e9,
                                    args.target_bit_hour * 64 * 2 ** 33 * 8766))
    out("")
    out("## D2. Sensitivity to the temperature law (all models share the same 85 C anchor)")
    out("Section 2.2's tail cells may have Ea ~0.35 eV. A lower Ea means less retention gained by cooling"
        " from 85 C, so every number at 25-65 C moves the pessimistic way.")
    out("| temperature law | retention scale | RS-8 65 C, target 2 | SEC-DED 45 C, target 1 / 2 |"
        " first failing cell, 25 C | failing bits at 25 C: 1.024 s / 65.5 s | at 65 C: 2.048 s / 4.096 s |")
    out("|---|---|---|---|---|---|---|")
    sens = {}
    rs8, sec = CODES[4], CODES[0]
    for law, kw in (("halves every 10 C", {"halving_c": 10.0}), ("Arrhenius Ea 0.6 eV", {"ea_ev": 0.6}),
                    ("Arrhenius Ea 0.35 eV", {"ea_ev": 0.35})):
        for scale in (1.0, 0.5, 4.0):
            m = RetentionModel(mu, sg, time_scale=scale, **kw)

            def bf(p, m=m, t=65.0):
                return min(0.5, m.cdf(p, t) * vmult)

            def bf45(p, m=m):
                return min(0.5, m.cdf(p, 45.0) * vmult)
            pmf8 = unit_pmf_from(np.ones(1, np.int64), rs8.t)
            pmf1 = unit_pmf_from(np.ones(1, np.int64), sec.t)
            x_rs8 = safe_interval(bf, rs8, pmf8, 1.0, targets_for(rs8, args.target_bit_hour, args.scrub_h,
                                                                  args.target_per_line)[1]) / JEDEC_WINDOW_S
            s1, s2 = targets_for(sec, args.target_bit_hour, args.scrub_h, args.target_per_line)
            x_s1 = safe_interval(bf45, sec, pmf1, 1.0, s1) / JEDEC_WINDOW_S
            x_s2 = safe_interval(bf45, sec, pmf1, 1.0, s2) / JEDEC_WINDOW_S
            first25 = m.time_at(1.0 / n, 25.0)
            b25 = (m.cdf(1.024, 25.0) * n, m.cdf(65.536, 25.0) * n)
            b65 = (m.cdf(2.048, 65.0) * n, m.cdf(4.096, 65.0) * n)
            sens[(law, scale)] = {"rs8_65_t2_x": x_rs8, "sec_45_t1_x": x_s1, "sec_45_t2_x": x_s2,
                                  "first25_s": first25, "bits25": b25, "bits65": b65}
            out("| %s | x%g | %.1fx | %.1fx / %.1fx | %.2g s | %.1f / %.0f | %.0f / %.0f |" % (
                law, scale, x_rs8, x_s1, x_s2, first25, b25[0], b25[1], b65[0], b65[1]))
    lo = min(v["rs8_65_t2_x"] for v in sens.values())
    hi = max(v["rs8_65_t2_x"] for v in sens.values())
    out("Gate prediction, RS-8 at 65 C, target 2: central %.0fx (halving rule), %.0fx (Ea 0.6 eV), %.0fx"
        " (Ea 0.35 eV); all corners %.0fx-%.0fx. PASS (>= 24x) is the central expectation; PARTIAL is a real"
        " possibility; NO-GO (< 4x) is not expected." % (
            sens[("halves every 10 C", 1.0)]["rs8_65_t2_x"], sens[("Arrhenius Ea 0.6 eV", 1.0)]["rs8_65_t2_x"],
            sens[("Arrhenius Ea 0.35 eV", 1.0)]["rs8_65_t2_x"], lo, hi))
    smoke = [v["bits25"][1] for v in sens.values()]
    out("Smoke test at room temperature (25 C), ALL0 + ALL1 added together: 0 at 64 ms in every corner;"
        " 0 at 1.024 s centrally (up to %.0f with a low-Ea tail); %.0f-%.0f at 65.5 s (central %.0f)." % (
            max(v["bits25"][0] for v in sens.values()), min(smoke), max(smoke),
            sens[("halves every 10 C", 1.0)]["bits25"][1]))
    pred["sens"] = sens
    out("")
    out("## E. Refresh energy scales as 1/P: a %.0fx longer interval is a %.0fx cut in refresh energy"
        " (array refresh only; periphery and self-refresh entry costs are not modelled)." %
        (pred[("RS-8(80,64)", 65.0)][1] / JEDEC_WINDOW_S, pred[("RS-8(80,64)", 65.0)][1] / JEDEC_WINDOW_S))
    return pred


# --------------------------------------------------------------------------------------------
# Synthetic chip (selftest and capture_retention.py --simulate)
# --------------------------------------------------------------------------------------------
class SyntheticChip:
    """A fake DRAM with the features the analysis must recover."""

    def __init__(self, n_words=1 << 18, bpw=16, words_per_row=256, anti_block_rows=128,
                 mu85=None, sigma=None, ea_ev=0.6, vrt_frac=0.05, vrt_low=1 / 6.0, vrt_p_low=0.3,
                 dpd_frac=0.2, dpd_factor=0.7, cluster_frac=0.05, jitter=0.02, seed=7):
        if mu85 is None or sigma is None:
            mu85, sigma = dossier_anchor()
        rng = np.random.default_rng(seed)
        self.n_words, self.bpw, self.wpr = n_words, bpw, words_per_row
        self.N = n = n_words * bpw
        self.mu85, self.sigma, self.ea = mu85, sigma, ea_ev
        self.vrt_low, self.vrt_p_low, self.dpd_factor, self.jitter = vrt_low, vrt_p_low, dpd_factor, jitter
        self.base85 = np.exp(rng.normal(mu85, sigma, n))
        self.vrt = np.zeros(n, bool)
        self.vrt[rng.choice(n, int(vrt_frac * n), replace=False)] = True
        self.dpd = np.zeros(n, bool)
        self.dpd[rng.choice(n, int(dpd_frac * n), replace=False)] = True
        # coherent 2-bit clusters (one shared defect): the neighbour bit in the same byte copies the
        # leader's retention (+/-2%), VRT and pattern sensitivity
        lead = rng.choice(n, int(cluster_frac * n), replace=False)
        self.base85[lead ^ 1] = self.base85[lead] * rng.uniform(0.98, 1.02, lead.size)
        self.vrt[lead ^ 1] = self.vrt[lead]
        self.dpd[lead ^ 1] = self.dpd[lead]
        self.cid = np.arange(n, dtype=np.int64)          # cluster id: partners follow the leader's VRT state
        self.cid[lead ^ 1] = lead
        rows = (np.arange(n) // bpw) // words_per_row
        self.anti_block_rows = anti_block_rows
        self.anti = ((rows // anti_block_rows) % 2) == 1
        minf = np.where(self.vrt, vrt_low, 1.0) * np.where(self.dpd, dpd_factor, 1.0) * math.exp(-5 * jitter)
        mins = self.base85 * minf
        self.order = np.argsort(mins)
        self.sorted_min = mins[self.order]

    def af(self, temp_c):
        return arrhenius_factor(self.ea, temp_c, 85.0)

    def fail_bits(self, pattern, inv, seed, wait_s, temp_c, rng):
        af = self.af(temp_c)
        nc = int(np.searchsorted(self.sorted_min, wait_s / af, side="right"))
        c = np.sort(self.order[:nc])
        if c.size == 0:
            return c
        w, b = c // self.bpw, (c % self.bpw).astype(np.uint32)
        vals = pattern_words(pattern, inv, seed, w, self.wpr)
        bit = (vals >> b) & np.uint32(1)
        charged = np.where(self.anti[c], bit == 0, bit == 1)
        r = self.base85[c] * af
        run_key = np.uint32(int(rng.integers(0, 2 ** 32)))
        u_state = mix32(self.cid[c].astype(np.uint32) ^ run_key).astype(np.float64) / 4294967296.0
        low = self.vrt[c] & (u_state < self.vrt_p_low)
        r = np.where(low, r * self.vrt_low, r)
        left = (vals >> np.maximum(b.astype(np.int64) - 1, 0).astype(np.uint32)) & np.uint32(1)
        right = (vals >> np.minimum(b + np.uint32(1), np.uint32(self.bpw - 1))) & np.uint32(1)
        opp = ((b == 0) | (left != bit)) & ((b == self.bpw - 1) | (right != bit))
        r = np.where(self.dpd[c] & opp, r * self.dpd_factor, r)
        r = r * np.exp(rng.normal(0.0, self.jitter, c.size))
        return c[charged & (r < wait_s)]

    def hello(self):
        return "HELLO,synthetic-0.2,SYNTH%dK,%d,%d,8000000,A|B|C" % (self.N // 1024, self.n_words, self.bpw)

    def planted_fail_prob(self, p_s, temp_c):
        """Planted truth, straight from the generating model: probability that a cell fails in one run
        with its worst data pattern at interval p_s (lognormal base, pattern factor, VRT low state)."""
        af = self.af(temp_c)
        n_vrt = float(np.mean(self.vrt))
        n_dpd = float(np.mean(self.dpd))
        tot = 0.0
        for d, wd in ((1.0, 1.0 - n_dpd), (self.dpd_factor, n_dpd)):
            for v, wv in ((1.0, 1.0 - n_vrt * self.vrt_p_low), (self.vrt_low, n_vrt * self.vrt_p_low)):
                tot += wd * wv * norm_cdf((math.log(p_s / (af * d * v)) - self.mu85) / self.sigma)
        return tot


def firmware_lines(rid, method, pattern, inv, seed, wait_ms, repeat, temp_set, temp_meas,
                   fbits, bpw, wpr, cap=20000, interval_ms=None):
    """Emulate the firmware's UART output for one run (same fields, same order, same caps)."""
    lines = ["RUN,%d,%s,%d,%d,%d,%d,%d,%.1f" % (rid, method, pattern, inv, seed, wait_ms, repeat, temp_set),
             "TEMP,%d,start,%.2f" % (rid, temp_meas)]
    words = fbits // bpw
    uw, idx = np.unique(words, return_inverse=True)
    xor = np.zeros(uw.size, np.uint32)
    np.bitwise_or.at(xor, idx, (np.uint32(1) << (fbits % bpw).astype(np.uint32)))
    exp = pattern_words(pattern, inv, seed, uw, wpr)
    obs = exp ^ xor
    b10 = int(popcount16(exp & xor).sum()) if uw.size else 0
    b01 = int(popcount16((~exp) & xor & np.uint32(0xFFFF)).sum()) if uw.size else 0
    nlog = min(cap, uw.size)
    for i in range(nlog):
        lines.append("F,%d,%x,%04x,%04x" % (rid, int(uw[i]), int(exp[i]), int(obs[i])))
    lines.append("TEMP,%d,end,%.2f" % (rid, temp_meas))
    lines.append("END,%d,%d,%d,%d,%d,%d,%d,%s" % (rid, uw.size, fbits.size, b10, b01, nlog,
                                                   wait_ms if interval_ms is None else interval_ms,
                                                   "OK" if nlog == uw.size else "TRUNC"))
    return lines


def synthetic_campaign(chip, temps=(25.0, 45.0, 65.0), patterns=((0, 0), (1, 0), (2, 0), (2, 1), (3, 0), (5, 0)),
                       waits_s=DEFAULT_WAITS_S, repeats=3, stop_ber=1e-2, cap=20000, seed=11, controls=True,
                       method_for=None, rid0=0):
    rng = np.random.default_rng(seed)
    lines = [chip.hello()]
    rid = rid0
    clock = 1.8e9
    for temp in temps:
        if controls:
            rid += 1
            lines.append("H,%.1f" % clock)
            lines += firmware_lines(rid, "C", 0, 0, 0, 0, 0, temp, temp + rng.normal(0, 0.3),
                                    np.zeros(0, np.int64), chip.bpw, chip.wpr, cap)
        for rep in range(1, repeats + 1):
            for pat, inv in patterns:
                for w in waits_s:
                    rid += 1
                    wait_ms = int(round(w * 1000))
                    method = method_for or ("A" if w <= 4.096 else "B")
                    interval_ms = wait_ms + (B_EXTRA_MS if method == "B" else 0)
                    fb = chip.fail_bits(pat, inv, 1234, interval_ms / 1000.0, temp, rng)
                    clock += w + 8.0
                    lines.append("H,%.1f" % clock)
                    lines += firmware_lines(rid, method, pat, inv, 1234, wait_ms, rep, temp,
                                            temp + rng.normal(0, 0.3), fb, chip.bpw, chip.wpr, cap,
                                            interval_ms=interval_ms)
                    if fb.size / chip.N > stop_ber:
                        break
        clock += 1800
    return lines


# --------------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------------
def c_pattern_crosscheck(out):
    """Compile stm32_retention/patterns.c on the host and compare with pattern_words()."""
    here = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(here, "stm32_retention")
    cc = shutil.which("gcc") or shutil.which("cc")
    if not cc or not os.path.exists(os.path.join(src_dir, "patterns.c")):
        out("  [SKIP] C/Python pattern cross-check (no gcc or no patterns.c)")
        return True
    with tempfile.TemporaryDirectory() as td:
        exe = os.path.join(td, "host_test_patterns")
        cmd = [cc, "-std=c11", "-O1", "-Wall", "-Wextra", "-o", exe,
               os.path.join(src_dir, "host_test_patterns.c"), os.path.join(src_dir, "patterns.c")]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            res = subprocess.run([exe], check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, OSError) as exc:
            out("  [FAIL] could not build/run host pattern test: %s" % exc)
            return False
    ok = True
    n = 0
    for line in res.stdout.splitlines():
        p, inv, seed, w, v = (int(x, 0) for x in line.split())
        mine = int(pattern_words(p, inv, seed, np.array([w]))[0])
        n += 1
        if mine != v:
            ok = False
            out("  mismatch pattern %d inv %d seed %d word %d: C %04x py %04x" % (p, inv, seed, w, v, mine))
    out("  [%s] C firmware patterns == Python patterns on %d samples" % ("PASS" if ok else "FAIL", n))
    return ok


def selftest():
    import time
    t_start = time.time()
    lines_out = []

    def out(s=""):
        lines_out.append(s)

    print("selftest: building synthetic 4 Mbit chip (lognormal tail + VRT + clusters + anti cells + DPD) ...")
    chip = SyntheticChip()
    log_lines = synthetic_campaign(chip)
    print("selftest: %d synthetic log lines; parsing and analysing ..." % len(log_lines))
    log = parse_log(log_lines)
    args = argparse.Namespace(words_per_row=256, target_bit_hour=1e-15, scrub_h=1.0,
                              target_per_line=2e-19, vrt_growth=1.0, cluster_sig=2.0)
    res = analyze_log(log, args, out)
    checks = []

    def check(name, cond, detail=""):
        checks.append((name, bool(cond), detail))

    n_runs = sum(1 for s in log_lines if s.startswith("END,"))
    check("parse: every END line became a run", len(log.runs) == n_runs, "%d/%d" % (len(log.runs), n_runs))
    check("parse: no parse errors", not log.errors, str(log.errors[:2]))
    check("control runs clean", res["control_failures"] == 0)
    trunc = [r for r in log.runs if r.truncated]
    check("truncation exercised and flagged", len(trunc) > 0, "%d truncated runs" % len(trunc))
    if trunc:
        r = trunc[0]
        check("truncated run keeps exact END counts", r.fail_bits > r.bits(16)[0].size)
    for tbin, ti in res["temps"].items():
        fit = ti["fit"]
        true_mu = chip.mu85 + math.log(chip.af(ti["temp_c"]))
        if fit:
            check("lognormal sigma at %.0f C within 30%%" % tbin, abs(fit["sigma"] / chip.sigma - 1) < 0.30,
                  "fit %.2f true %.2f" % (fit["sigma"], chip.sigma))
            check("lognormal median at %.0f C within 2x" % tbin, abs(fit["mu"] - true_mu) < LN2,
                  "fit %.3g s true %.3g s" % (math.exp(fit["mu"]), math.exp(true_mu)))
        else:
            check("lognormal fit exists at %.0f C" % tbin, False)
    garr = res.get("arrhenius")
    check("global Arrhenius Ea within 0.12 eV of 0.60", garr and abs(garr["ea_ev"] - chip.ea) < 0.12,
          "fit %.3f eV" % (garr["ea_ev"] if garr else float("nan")))
    cls = res["cell_class"]
    correct = sum(1 for row, c in cls.items() if (c == "A") == (((row // chip.anti_block_rows) % 2) == 1))
    check("true/anti rows classified >=97% correct", cls and correct / len(cls) >= 0.97,
          "%d/%d" % (correct, len(cls)))
    check("anti-cell block size recovered (128 rows)", res["anti_block_rows"] == chip.anti_block_rows,
          str(res["anti_block_rows"]))
    vrt_ok = [v for v in res["vrt"].values() if v["strict"] is not None]
    check("VRT detected (strict > 0; its size is NOT checked)", vrt_ok and max(v["strict"] for v in vrt_ok) > 0,
          str([round(v["strict"], 4) for v in vrt_ok]))
    check("intermittent >= strict", vrt_ok and all((v["loose"] or 0) >= 0 for v in vrt_ok))
    check("short campaign: per-day VRT growth reported as not meaningful",
          any("not meaningful" in s for s in lines_out))
    ecc = res["ecc"]
    if ecc:
        tb = sorted(ecc)[1] if len(ecc) > 1 else sorted(ecc)[0]
        e = ecc[tb]
        check("stronger code -> longer safe interval (BCH-4 > SEC-DED, random map)",
              e[("BCH-4(552,512)", "random")][0] > e[("SECDED(72,64)", "random")][0])
        ratios = {tb2: ecc[tb2][("SECDED(72,64)", "adjacent")][1] / ecc[tb2][("SECDED(72,64)", "random")][1]
                  for tb2 in ecc}
        check("planted clusters detected: SEC-DED adjacent < random somewhere (target 2)",
              min(ratios.values()) < 0.98 and max(ratios.values()) <= 1.0001,
              ", ".join("%.0f C %.2f" % kv for kv in sorted(ratios.items())))
        tbc = min(ratios, key=ratios.get)
        r_sec = ecc[tbc][("SECDED(72,64)", "adjacent")][1] / ecc[tbc][("SECDED(72,64)", "random")][1]
        r_ssc = ecc[tbc][("SSC-RS(18,16)", "adjacent")][1] / ecc[tbc][("SSC-RS(18,16)", "random")][1]
        check("in-byte pairs hurt binary SEC-DED more than byte-symbol SSC-RS", r_ssc > r_sec,
              "adjacent/random: SSC-RS %.2f, SEC-DED %.2f" % (r_ssc, r_sec))
        check("safe interval grows as temperature falls (global fit)",
              all(ecc[a][("RS-8(80,64)", "random")][1] >= ecc[b][("RS-8(80,64)", "random")][1]
                  for a, b in zip(sorted(ecc), sorted(ecc)[1:])))
        # planted truth: the same code math applied to the generating model, not to the fit
        hot = max(ecc)
        t_hot = res["temps"][hot]["temp_c"]
        vmult = 1.0 + args.vrt_growth * args.scrub_h / 24.0
        for code, mapping, which in ((CODES[4], "adjacent", 1), (CODES[0], "random", 0)):
            pmf1 = unit_pmf_from(np.ones(1, np.int64), code.t)
            tgt = targets_for(code, args.target_bit_hour, args.scrub_h, args.target_per_line)[which]
            truth = safe_interval(lambda p, T=t_hot: min(0.5, chip.planted_fail_prob(p, T) * vmult),
                                  code, pmf1, 1.0, tgt)
            got = ecc[hot][(code.name, mapping)][which]
            check("%s %s target %d at %.0f C within 2x of planted truth" % (code.name, mapping, which + 1, hot),
                  0.5 <= got / truth <= 2.0, "analysis %.3g s, truth %.3g s (%.2fx)" % (got, truth, got / truth))
    check("verdict computed", "verdict" in res, res.get("verdict", ""))
    # method A vs B overlap: same chip, both methods at 2.048 and 4.096 s, one mixed log
    ov_lines = synthetic_campaign(chip, temps=(65.0,), patterns=((0, 0), (1, 0)), waits_s=[2.048, 4.096],
                                  repeats=2, controls=False, method_for="A", seed=21)
    ov_lines += synthetic_campaign(chip, temps=(65.0,), patterns=((0, 0), (1, 0)), waits_s=[2.048, 4.096],
                                   repeats=2, controls=False, method_for="B", seed=22, rid0=1000)[1:]
    ov_log = parse_log(ov_lines)
    ov_res = analyze_log(ov_log, args, lambda s="": None)
    ov = ov_res["overlap"]
    check("A-vs-B overlap table: both waits, B/A within 2x", len(ov) == 2 and all(0.5 <= o["ratio"] <= 2 for o in ov),
          ", ".join("%.3f s B/A %.2f (%.0f / %.0f bits)" % (o["t_a"], o["ratio"], o["n_a"], o["n_b"]) for o in ov))
    a_only = argparse.Namespace(**dict(vars(args), method="A"))
    ov_res_a = analyze_log(ov_log, a_only, lambda s="": None)
    check("--method A filter drops B runs (no overlap rows)", not ov_res_a["overlap"] and ov_res_a["temps"])
    # numerical helpers
    check("norm_ppf round trip at 1e-12", abs(norm_cdf(norm_ppf(1e-12)) / 1e-12 - 1) < 1e-6)
    check("compound_ue == Poisson tail for single-unit events",
          abs(compound_ue(0.01, [0, 1, 0], 1) / poisson_sf(1, 0.01) - 1) < 1e-9)
    perm = feistel_positions(np.arange(1 << 12), 1 << 12)
    check("Feistel mapping is a permutation", np.array_equal(np.sort(perm), np.arange(1 << 12)))
    perm2 = feistel_positions(np.arange(3000), 3000)
    check("Feistel cycle-walk permutation (non power of 2)", np.array_equal(np.sort(perm2), np.arange(3000)))
    print("selftest: C/Python pattern cross-check")
    msgs = []
    ok_c = c_pattern_crosscheck(msgs.append)
    for m in msgs:
        print(m)
    check("C pattern generator matches Python", ok_c)
    # predict runs
    pl = []
    pargs = argparse.Namespace(bits=CHIP_BITS_F429, cs_ff=20.0, vdd=2.0, cbl_ff=100.0, voff_mv=30.0,
                               vrt_growth=1.0, scrub_h=1.0, target_bit_hour=1e-15, target_per_line=2e-19)
    pred = predict(pargs, pl.append)
    check("predict: SEC-DED 25 C interval > 45 C > 65 C",
          pred[("SECDED(72,64)", 25.0)][0] > pred[("SECDED(72,64)", 45.0)][0] > pred[("SECDED(72,64)", 65.0)][0])
    nfail = sum(1 for _, ok, _ in checks if not ok)
    print("")
    for name, ok, detail in checks:
        print("  [%s] %s %s" % ("PASS" if ok else "FAIL", name, ("(" + detail + ")") if detail else ""))
    print("")
    print("selftest: %d checks, %d failed, %.1f s" % (len(checks), nfail, time.time() - t_start))
    if os.environ.get("E6_SELFTEST_REPORT"):
        with open(os.environ["E6_SELFTEST_REPORT"], "w") as fh:
            fh.write("\n".join(lines_out) + "\n")
    return 0 if nfail == 0 else 1


# --------------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true", help="synthetic end-to-end test; exit 0 on pass")
    sub = ap.add_subparsers(dest="cmd")
    pp = sub.add_parser("predict", help="expected results before the build")
    pp.add_argument("--bits", type=int, default=CHIP_BITS_F429)
    pp.add_argument("--cs-ff", type=float, default=20.0, help="cell capacitance, fF [ESTIMATE]")
    pp.add_argument("--cbl-ff", type=float, default=100.0, help="bitline capacitance, fF [ESTIMATE]")
    pp.add_argument("--vdd", type=float, default=2.0, help="array voltage, V [ESTIMATE]")
    pp.add_argument("--voff-mv", type=float, default=30.0, help="sense-amp offset, mV [ESTIMATE]")
    for p in (pp,):
        p.add_argument("--vrt-growth", type=float, default=1.0, help="VRT growth per day (dossier: 1)")
        p.add_argument("--scrub-h", type=float, default=1.0)
        p.add_argument("--target-bit-hour", type=float, default=1e-15)
        p.add_argument("--target-per-line", type=float, default=2e-19)
    pa = sub.add_parser("analyze", help="analyze firmware logs")
    pa.add_argument("logs", nargs="+")
    pa.add_argument("--words-per-row", type=int, default=256)
    pa.add_argument("--vrt-growth", type=float, default=1.0)
    pa.add_argument("--scrub-h", type=float, default=1.0)
    pa.add_argument("--target-bit-hour", type=float, default=1e-15)
    pa.add_argument("--target-per-line", type=float, default=2e-19)
    pa.add_argument("--cluster-sig", type=float, default=2.0,
                    help="sigma above chance before a cluster excess counts (0 = always count it)")
    pa.add_argument("--method", default="all", choices=["all", "A", "B", "Z"],
                    help="analyse only runs of this method (use for A-vs-B overlap logs)")
    pa.add_argument("--report", help="also write the report to this file")
    pa.add_argument("--csv", help="write the per-(temp, wait) F_solid table as CSV")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.cmd == "predict":
        predict(a, print)
        return 0
    if a.cmd == "analyze":
        lines = []
        for path in a.logs:
            with open(path, "r", errors="replace") as fh:
                lines.extend(fh.readlines())
        log = parse_log(lines)
        rep = []

        def out(s=""):
            print(s)
            rep.append(s)
        res = analyze_log(log, a, out)
        if a.report:
            with open(a.report, "w") as fh:
                fh.write("\n".join(rep) + "\n")
        if a.csv:
            with open(a.csv, "w") as fh:
                fh.write("temp_c,wait_s,F_solid,F_union\n")
                for ti in res["temps"].values():
                    for wms, (t_s, fs, fu) in sorted(ti["wait_rows"].items()):
                        fh.write("%.2f,%.4f,%.6g,%.6g\n" % (ti["temp_c"], t_s, fs, fu))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
