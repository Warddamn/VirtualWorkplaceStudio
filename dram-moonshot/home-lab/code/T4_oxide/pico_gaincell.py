# pico_gaincell.py -- drive and log a home-made 2T0C gain cell (E8): oxide TFT write switch,
# discrete read transistor, storage node SN. Also the 2x2 (4-bit) array stretch goal.
#
# REFERENCE CODE -- UNTESTED ON HARDWARE. Syntax-checked; logic exercised on a PC with --sim.
# Needs t4_hw.py next to it. Track T4, dram-moonshot home lab.
#
# Cell wiring (row r, column c):
#   write switch: oxide TFT on chip r. Back gate (the Si substrate) = WWL r. Drain pad = WBL c.
#                 Source pad (keep it SMALL) = SN.
#   SN: 10 nF C0G or polypropylene capacitor to ground + gate of the read transistor (2N7000).
#   read transistor: drain = RBL c (TIA c virtual node at 2.5 V), source = row-select line r.
#   Silicon comparison (E2): put a 2N7000 in place of the TFT (gate = WWL, max 10 V!).
#   Control cell: put the reed relay (GP14) in place of the TFT. It shows the setup floor.
#
# On the Pico:
#   mpremote cp t4_hw.py pico_gaincell.py :
#   mpremote exec "import pico_gaincell as g; g.run('calibrate')" > cal.csv
#   mpremote exec "import pico_gaincell as g; g.run('retention', temp=45, label='oxide')" > ox45.csv
#   mpremote exec "import pico_gaincell as g; g.run('pattern')" > pattern.csv
# On a PC (simulated cells):
#   python3 pico_gaincell.py --sim --test retention --switch si --temp 65 --out si65.csv

import math

import t4_hw as hw

CONFIG = {
    "switch": "tft",          # "tft" (oxide), "si" (2N7000 write switch), "relay" (control cell)
    "wwl_on": 27.5,           # oxide TFT write level (node volts). <= 28 V hard limit in t4_hw
    "wwl_on_si": 10.0,        # 2N7000 gate: stay well under its +/-20 V gate rating
    "wwl_off": 0.0,
    "write_ms": 200,          # >= 10 x R_on*C_SN (expected_numbers.py: ~2-6 ms)
    "wwl_fall_ms": 400,       # let the RC-filtered WWL fully fall before touching the bit line
    "wbl_hold": 0.0,          # worst case for a stored "1": full Vds across the switch
    "cal_v": [0.1 * k for k in range(0, 37)],     # 0.0 .. 3.6 V
    "i_one_max": 5e-5,        # "1" level: read current stays inside the 10 kohm range
    "i_zero_max": 1e-9,       # "0" level: read transistor essentially off
    "c_sn": 10.18e-9,         # storage-node capacitance (expected_numbers.py)
    "ppd": 20,                # retention samples per decade of time
    "t_first_s": 0.5,
    "heater_kp": 0.05, "heater_ki": 0.0005, "heater_quiet_ms": 300,
}

_STATE = {"cal": {}, "integ": 0.0}


# ------------------------------------------------------------------------------------------
# basic operations
# ------------------------------------------------------------------------------------------
def _wwl_on_level():
    return CONFIG["wwl_on_si"] if CONFIG["switch"] == "si" else CONFIG["wwl_on"]


def write_row(rig, row, col_volts):
    """col_volts: {col: volts}. Bit lines first, word line pulse, bit lines back to hold."""
    for c in col_volts:
        rig.set_wbl(c, col_volts[c])
    hw.sleep_ms(50)
    if CONFIG["switch"] == "relay":
        rig.control_switch(True)
        hw.sleep_ms(CONFIG["write_ms"])
        rig.control_switch(False)
        hw.sleep_ms(50)
    else:
        rig.set_wwl(row, _wwl_on_level())
        hw.sleep_ms(CONFIG["write_ms"])
        rig.set_wwl(row, CONFIG["wwl_off"])
        hw.sleep_ms(CONFIG["wwl_fall_ms"])
    for c in col_volts:
        rig.set_wbl(c, CONFIG["wbl_hold"])


def read_cell(rig, row, col, n_avg=4, keep_selected=False):
    rig.row_select(row)
    hw.sleep_ms(20)
    i, rng = rig.read_current(col, n_avg)
    if not keep_selected:
        rig.row_select(-1)
    return abs(i)


def calibrate(rig, row=0, col=0, quiet=False):
    """Hold the switch ON so SN follows the bit line; record read current vs SN voltage."""
    if not quiet:
        print("# calibration row %d col %d (switch held on: SN = WBL)" % (row, col))
        print("v_sn,i_read")
    rows = []
    if CONFIG["switch"] == "relay":
        rig.control_switch(True)
    else:
        rig.set_wwl(row, _wwl_on_level())
    rig.row_select(row)
    for v in CONFIG["cal_v"]:
        v = rig.set_wbl(col, v)
        hw.sleep_ms(300)
        i, _ = rig.read_current(col, 4)
        rows.append((v, abs(i)))
        if not quiet:
            print("%.4f,%.6e" % (v, abs(i)))
    rig.set_wwl(row, CONFIG["wwl_off"])
    rig.control_switch(False)
    hw.sleep_ms(CONFIG["wwl_fall_ms"])
    rig.set_wbl(col, CONFIG["wbl_hold"])
    rig.row_select(-1)
    _STATE["cal"][(row, col)] = rows
    return rows


def pick_levels(rows):
    v1 = v0 = rows[0][0]
    for v, i in rows:
        if i <= CONFIG["i_one_max"]:
            v1 = v
        if i <= CONFIG["i_zero_max"]:
            v0 = v
    v0 = min(v0, 0.5 * v1)
    return v0, v1


def v_from_i(rows, i):
    """Invert the calibration (log-interpolation of current)."""
    pts = sorted([(math.log10(max(ii, 1e-30)), v) for v, ii in rows])
    x = math.log10(max(i, 1e-30))
    if x <= pts[0][0]:
        return pts[0][1]
    for k in range(len(pts) - 1):
        if pts[k][0] <= x <= pts[k + 1][0]:
            x0, v0 = pts[k]
            x1, v1 = pts[k + 1]
            return v0 if x1 == x0 else v0 + (x - x0) * (v1 - v0) / (x1 - x0)
    return pts[-1][1]


def _i_at(rows, v):
    return min(rows, key=lambda r: abs(r[0] - v))[1]


def threshold_current(rows, v0, v1):
    """Decision level for a 0/1 read: geometric mean of the calibrated '0' and '1' currents."""
    return math.sqrt(max(_i_at(rows, v0), 1e-13) * max(_i_at(rows, v1), 1e-13))


# ------------------------------------------------------------------------------------------
# temperature control (heats ONLY the write-switch block; C_SN and read FET stay at room T)
# ------------------------------------------------------------------------------------------
def control_step(rig, target, dt_s):
    t = rig.temp_c()
    err = target - t
    _STATE["integ"] = max(-200.0, min(_STATE["integ"] + err * dt_s, 2000.0))
    duty = CONFIG["heater_kp"] * err + CONFIG["heater_ki"] * _STATE["integ"]
    rig.heater(max(0.0, min(duty, 1.0)))
    return t


def set_temperature(rig, target, tol=0.5, stable_s=300, timeout_s=7200):
    if target is None:
        return None
    print("# heating switch block to %.1f C" % target)
    t0 = hw.ticks_ms()
    ok_since = None
    while hw.elapsed_s(t0) < timeout_s:
        t = control_step(rig, target, 1.0)
        now = hw.elapsed_s(t0)
        if abs(t - target) < tol:
            ok_since = now if ok_since is None else ok_since
            if now - ok_since >= stable_s:
                print("# stable at %.2f C after %.0f s" % (t, now))
                return t
        else:
            ok_since = None
        hw.sleep_ms(1000)
    print("# WARNING: temperature not stable within timeout")
    return rig.temp_c()


def wait_until(rig, t0_ms, t_target_s, temp_target):
    while True:
        left = t_target_s - hw.elapsed_s(t0_ms)
        if left <= 0:
            return
        step = min(1.0, left)
        if temp_target is not None:
            control_step(rig, temp_target, step)
        hw.sleep_ms(int(step * 1000) + 1)


def _quiet_read(rig, row, col, temp_target, n_avg=4):
    if temp_target is not None and CONFIG["heater_quiet_ms"] > 0:
        rig.heater(0.0)                       # heater PWM off during the read (less noise)
        hw.sleep_ms(CONFIG["heater_quiet_ms"])
    return read_cell(rig, row, col, n_avg, keep_selected=True)


def log_times(t_end, ppd, t_first):
    out = [0.0]
    k = 0
    while True:
        t = t_first * 10 ** (k / float(ppd))
        if t > t_end:
            break
        out.append(t)
        k += 1
    return out


# ------------------------------------------------------------------------------------------
# experiments
# ------------------------------------------------------------------------------------------
def retention(rig, v_write=None, duration_s=3600, row=0, col=0, label="oxide", temp=None):
    if (row, col) not in _STATE["cal"]:
        calibrate(rig, row, col, quiet=True)
    rows = _STATE["cal"][(row, col)]
    v0, v1 = pick_levels(rows)
    v_write = v1 if v_write is None else v_write
    set_temperature(rig, temp)
    print("# retention: write %.3f V to cell (%d,%d), hold WWL %.1f V, WBL %.2f V, switch=%s, label=%s"
          % (v_write, row, col, CONFIG["wwl_off"], CONFIG["wbl_hold"], CONFIG["switch"], label))
    print("# C_SN %.3e F (set CONFIG c_sn to your value)" % CONFIG["c_sn"])
    write_row(rig, row, {col: v_write})
    t0 = hw.ticks_ms()
    print("t_s,i_read_A,v_sn_est,temp_c,label")
    for ts in log_times(duration_s, CONFIG["ppd"], CONFIG["t_first_s"]):
        wait_until(rig, t0, ts, temp)
        i = _quiet_read(rig, row, col, temp)
        print("%.2f,%.6e,%.4f,%.2f,%s" % (hw.elapsed_s(t0), i, v_from_i(rows, i), rig.temp_c(), label))
    rig.row_select(-1)


def read_disturb(rig, n=1000, row=0, col=0):
    if (row, col) not in _STATE["cal"]:
        calibrate(rig, row, col, quiet=True)
    rows = _STATE["cal"][(row, col)]
    v0, v1 = pick_levels(rows)
    write_row(rig, row, {col: v1})
    t0 = hw.ticks_ms()
    i_first = read_cell(rig, row, col, 8)
    t_a = hw.elapsed_s(t0)
    for _ in range(n):
        read_cell(rig, row, col, 1)
    t_b = hw.elapsed_s(t0)
    i_last = read_cell(rig, row, col, 8)
    v_a, v_b = v_from_i(rows, i_first), v_from_i(rows, i_last)
    print("# read disturb: %d reads in %.1f s" % (n, t_b - t_a))
    print("n_reads,i_first_A,i_last_A,v_first,v_last,dv_mV,elapsed_s")
    print("%d,%.4e,%.4e,%.4f,%.4f,%.2f,%.1f" % (n, i_first, i_last, v_a, v_b, 1000 * (v_a - v_b), t_b - t_a))
    print("# compare dv with the droop a quiet hold of the same length shows: equal = reads are harmless")


def hold_bias(rig, levels=(4.0, 2.0, 0.0), hold_s=600, row=0, col=0, temp=None):
    """Leakage vs hold word-line level: subthreshold physics predicts ~10x per SS volts."""
    if (row, col) not in _STATE["cal"]:
        calibrate(rig, row, col, quiet=True)
    rows = _STATE["cal"][(row, col)]
    v0, v1 = pick_levels(rows)
    set_temperature(rig, temp)
    print("wwl_hold_V,v_start,v_end,hold_s,I_leak_A")
    for lvl in levels:
        write_row(rig, row, {col: v1})
        rig.set_wwl(row, lvl)
        hw.sleep_ms(CONFIG["wwl_fall_ms"])
        va = v_from_i(rows, read_cell(rig, row, col, 8))
        t0 = hw.ticks_ms()
        wait_until(rig, t0, hold_s, temp)
        vb = v_from_i(rows, read_cell(rig, row, col, 8))
        dt = hw.elapsed_s(t0)
        print("%.2f,%.4f,%.4f,%.1f,%.3e" % (lvl, va, vb, dt, CONFIG["c_sn"] * (va - vb) / dt))
        rig.set_wwl(row, CONFIG["wwl_off"])


def calibrate_all(rig):
    for r in (0, 1):
        for c in (0, 1):
            calibrate(rig, r, c, quiet=True)


def array_write(rig, bits):
    """bits = [b00, b01, b10, b11] (row-major)."""
    for r in (0, 1):
        cv = {}
        for c in (0, 1):
            v0, v1 = pick_levels(_STATE["cal"][(r, c)])
            cv[c] = v1 if bits[2 * r + c] else v0
        write_row(rig, r, cv)


def array_read(rig):
    got, cur = [], []
    for r in (0, 1):
        for c in (0, 1):
            rows = _STATE["cal"][(r, c)]
            v0, v1 = pick_levels(rows)
            i = read_cell(rig, r, c, 4)
            cur.append(i)
            got.append(1 if i > threshold_current(rows, v0, v1) else 0)
    return got, cur


def pattern_test(rig, wait_s=60):
    calibrate_all(rig)
    print("pattern,expected,got,pass,i00,i01,i10,i11")
    n_pass = 0
    for p in range(16):
        bits = [(p >> (3 - k)) & 1 for k in range(4)]
        array_write(rig, bits)
        t0 = hw.ticks_ms()
        wait_until(rig, t0, wait_s, None)
        got, cur = array_read(rig)
        ok = got == bits
        n_pass += 1 if ok else 0
        print("%d,%s,%s,%d,%.3e,%.3e,%.3e,%.3e" % (p, "".join(str(b) for b in bits),
                                                "".join(str(b) for b in got), 1 if ok else 0,
                                                cur[0], cur[1], cur[2], cur[3]))
    print("# %d of 16 patterns correct after %d s" % (n_pass, wait_s))
    return n_pass


def disturb_test(rig, n=1000):
    """Half-select disturb: hammer row 0 with writes, watch row 1 (which stores 1,1)."""
    calibrate_all(rig)
    array_write(rig, [0, 0, 1, 1])
    v_before = [v_from_i(_STATE["cal"][(1, c)], read_cell(rig, 1, c, 8)) for c in (0, 1)]
    t0 = hw.ticks_ms()
    for k in range(n):
        b = k & 1
        cv = {}
        for c in (0, 1):
            v0, v1 = pick_levels(_STATE["cal"][(0, c)])
            cv[c] = v1 if b else v0
        write_row(rig, 0, cv)
    dt = hw.elapsed_s(t0)
    v_after = [v_from_i(_STATE["cal"][(1, c)], read_cell(rig, 1, c, 8)) for c in (0, 1)]
    print("col,v_before,v_after,dv_mV,elapsed_s,n_writes_row0")
    for c in (0, 1):
        print("%d,%.4f,%.4f,%.2f,%.1f,%d" % (c, v_before[c], v_after[c],
                                             1000 * (v_before[c] - v_after[c]), dt, n))
    print("# compare with a quiet hold of the same length (retention data): the excess is disturb")


def run(test="calibrate", sim=None, switch=None, **kw):
    if switch is not None:
        CONFIG["switch"] = switch
    mode_switch = {"tft": "oxide", "si": "si", "relay": "relay"}[CONFIG["switch"]]
    if sim or (sim is None and hw.SIM):
        rig = hw.make_rig(True, mode="cell", switch=mode_switch)
    else:
        rig = hw.make_rig(False)
    try:
        if test == "calibrate":
            calibrate(rig, kw.get("row", 0), kw.get("col", 0))
        elif test == "retention":
            retention(rig, **kw)
        elif test == "read_disturb":
            read_disturb(rig, **kw)
        elif test == "hold_bias":
            hold_bias(rig, **kw)
        elif test == "pattern":
            pattern_test(rig, **kw)
        elif test == "disturb":
            disturb_test(rig, **kw)
        else:
            print("# unknown test", test)
    finally:
        rig.all_safe()


def _cli():
    import argparse
    import contextlib
    ap = argparse.ArgumentParser(description="E8 gain-cell experiments (simulation on a PC)")
    ap.add_argument("--sim", action="store_true")
    ap.add_argument("--test", default="calibrate",
                    choices=["calibrate", "retention", "read_disturb", "hold_bias", "pattern", "disturb"])
    ap.add_argument("--switch", default="tft", choices=["tft", "si", "relay"])
    ap.add_argument("--temp", type=float, default=None)
    ap.add_argument("--duration", type=float, default=3600.0)
    ap.add_argument("--label", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if not a.sim:
        print("On a PC this script only runs with --sim. On the Pico use mpremote (see header).")
        return 2
    kw = {}
    if a.test == "retention":
        kw = {"duration_s": a.duration, "temp": a.temp, "label": a.label or a.switch}
    elif a.test == "hold_bias":
        kw = {"temp": a.temp}
    elif a.test == "pattern":
        kw = {"wait_s": 60}
    if a.out:
        with open(a.out, "w") as f, contextlib.redirect_stdout(f):
            run(a.test, sim=True, switch=a.switch, **kw)
        print("wrote", a.out)
    else:
        run(a.test, sim=True, switch=a.switch, **kw)
    return 0


if __name__ == "__main__":
    if hw.is_micropython():
        run("calibrate")
    else:
        import sys
        sys.exit(_cli())
