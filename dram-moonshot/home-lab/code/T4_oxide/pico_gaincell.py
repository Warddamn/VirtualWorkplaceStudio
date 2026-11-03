# pico_gaincell.py -- drive and log a home-made 2T0C gain cell (E8): oxide TFT write switch,
# discrete read transistor, storage node SN. Also the 2x2 (4-bit) array stretch goal.
#
# REFERENCE CODE -- UNTESTED ON HARDWARE. Syntax-checked; logic exercised on a PC with --sim.
# Needs t4_hw.py next to it. Track T4, dram-moonshot home lab.
#
# Cell wiring (row r, column c):
#   write switch: oxide TFT on chip r. Back gate (the Si substrate) = WWL r. Drain pad = WBL c.
#                 Source pad (keep it SMALL) = SN.
#   SN: 10 nF polypropylene (or C0G) capacitor to ground + gate of the read transistor (2N7000).
#   read transistor: drain = RBL c (TIA c virtual node at 2.5 V), source = row-select line r.
#   Silicon comparison (E2): put a 2N7000 in place of the TFT (gate = WWL, max 10 V!). Its adapter
#     carries a 15 V Zener (1N4744A) from its WWL pin to ground as a hardware backstop.
#   Control cell: put the reed relay (GP14, via the ULN2003A) in place of the TFT: the setup floor.
#
# On the Pico. switch= is REQUIRED and must match what is in the socket:
#   mpremote cp t4_hw.py pico_gaincell.py :
#   mpremote exec "import pico_gaincell as g; g.run('calibrate', switch='relay')" > cal.csv
#   mpremote exec "import pico_gaincell as g; g.run('retention', switch='tft', temp=45, label='oxide')" | tee O_45.csv
#   mpremote exec "import pico_gaincell as g; g.run('pattern', switch='tft')" > pattern.csv
# Retention and hold-bias runs also append every line to <label>.csv in the Pico's flash.
# Recover it after a dropped USB link with:  mpremote cp :oxide.csv .
# On a PC (simulated cells; the leakage values are ASSUMPTIONS, see t4_hw.SimCell):
#   python3 pico_gaincell.py --sim --test retention --switch si --temp 65 --out si65.csv

import math

import t4_hw as hw

CONFIG = {
    "switch": None,           # set by run(switch=...): "tft" (oxide), "si" (2N7000), "relay" (control)
    "wwl_on": 27.0,           # oxide TFT write level (node volts): the LM358's guaranteed maximum
    "wwl_on_si": 10.0,        # 2N7000 gate: stay well under its +/-20 V gate rating
    "wwl_off": 0.0,
    "write_ms": 200,          # >= 10 x R_on*C_SN (expected_numbers.py: ~2-6 ms)
    "wwl_fall_ms": 400,       # let the RC-filtered WWL fully fall before touching the bit line
    "wbl_hold": 0.0,          # worst case for a stored "1": full Vds across the switch
    "presoak_s": 600,         # write "1", hold 10 min, re-write, THEN log: dielectric absorption of
                              # C_store settles while the switch stays off (no gate stress)
    "cal_v": [0.1 * k for k in range(0, 37)],     # 0.0 .. 3.6 V
    "i_one_max": 5e-5,        # "1" level: read current stays inside the 10 kohm range
    "i_zero_max": 1e-9,       # "0" level: read transistor essentially off
    "c_sn": 10.23e-9,         # storage-node capacitance (expected_numbers.py, 1.5 mm2 source pad)
    "ppd": 20,                # retention samples per decade of time
    "t_first_s": 0.5,
    "heater_kp": 0.05, "heater_ki": 0.0005, "heater_quiet_ms": 300,
    "setpoint_max_c": 65.0,   # enforced in set_temperature()
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
        hw.emit("# calibration row %d col %d (switch=%s held on: SN = WBL)" % (row, col, CONFIG["switch"]))
        hw.emit("v_sn,i_read")
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
            hw.emit("%.4f,%.6e" % (v, abs(i)))
    rig.set_wwl(row, CONFIG["wwl_off"])
    rig.control_switch(False)
    hw.sleep_ms(CONFIG["wwl_fall_ms"])
    rig.set_wbl(col, CONFIG["wbl_hold"])
    rig.row_select(-1)
    _STATE["cal"][(row, col)] = rows
    return rows


def i_one_limit(rig, col):
    """Largest read current a '1' may draw on this column: TIA1 has a fixed ~1 Mohm feedback
    (full scale ~2 uA), so its '1' must stay below 75% of that, not 50 uA."""
    if col == 1:
        return min(CONFIG["i_one_max"], 0.75 * hw.CFG["ads_fs"] / rig.rf(1))
    return CONFIG["i_one_max"]


def pick_levels(rows, i_max=None):
    i_max = CONFIG["i_one_max"] if i_max is None else i_max
    v1 = v0 = rows[0][0]
    for v, i in rows:
        if i <= i_max:
            v1 = v
        if i <= CONFIG["i_zero_max"]:
            v0 = v
    v0 = min(v0, 0.5 * v1)
    return v0, v1


def levels_for(rig, row, col):
    return pick_levels(_STATE["cal"][(row, col)], i_one_limit(rig, col))


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
    dmax = hw.CFG["heater_duty_max"]
    duty = CONFIG["heater_kp"] * err + CONFIG["heater_ki"] * _STATE["integ"]
    if 0.0 < duty < dmax:                   # anti-windup: integrate only while not saturated
        _STATE["integ"] = max(-200.0, min(_STATE["integ"] + err * dt_s, 2000.0))
    rig.heater(max(0.0, min(duty, dmax)))
    return t


def set_temperature(rig, target, tol=0.5, stable_s=300, timeout_s=7200):
    if target is None:
        return None
    if target > CONFIG["setpoint_max_c"]:
        hw.emit("# setpoint %.1f C clipped to the %.1f C maximum" % (target, CONFIG["setpoint_max_c"]))
        target = CONFIG["setpoint_max_c"]
    hw.enable_watchdog()                    # heated run: a hung program resets the Pico (heater off)
    hw.emit("# heating switch block to %.1f C" % target)
    t0 = hw.ticks_ms()
    ok_since = None
    while hw.elapsed_s(t0) < timeout_s:
        t = control_step(rig, target, 1.0)
        now = hw.elapsed_s(t0)
        if abs(t - target) < tol:
            ok_since = now if ok_since is None else ok_since
            if now - ok_since >= stable_s:
                hw.emit("# stable at %.2f C after %.0f s" % (t, now))
                return target
        else:
            ok_since = None
        hw.sleep_ms(1000)
    hw.emit("# WARNING: temperature not stable within timeout")
    return target


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
def retention(rig, v_write=None, duration_s=3600, row=0, col=0, label="oxide", temp=None,
              wwl_hold=None, presoak_s=None):
    """Write '1', hold, log read current at log-spaced times.
    wwl_hold: word-line level during the hold (default CONFIG wwl_off = 0 V). E8 step 10b uses a
    positive hold (TFT only) to put the oxide's subthreshold leakage 30-100x above the floor.
    presoak_s: write, wait this long (switch off), re-write, then log (dielectric absorption)."""
    hw.set_log(label + ".csv")
    if (row, col) not in _STATE["cal"]:
        calibrate(rig, row, col, quiet=True)
    rows = _STATE["cal"][(row, col)]
    v0, v1 = levels_for(rig, row, col)
    v_write = v1 if v_write is None else v_write
    wwl_hold = CONFIG["wwl_off"] if wwl_hold is None else wwl_hold
    if CONFIG["switch"] == "si" and wwl_hold > 0.5:
        hw.emit("# ERROR: wwl_hold > 0.5 V would turn a 2N7000 on. Use wwl_hold only with switch='tft'.")
        return
    presoak_s = CONFIG["presoak_s"] if presoak_s is None else presoak_s
    temp = set_temperature(rig, temp)
    hw.emit("# retention: write %.3f V to cell (%d,%d), hold WWL %.2f V, WBL %.2f V, switch=%s, label=%s"
            % (v_write, row, col, wwl_hold, CONFIG["wbl_hold"], CONFIG["switch"], label))
    hw.emit("# C_SN %.3e F (set CONFIG c_sn to your value); presoak %d s" % (CONFIG["c_sn"], presoak_s))
    if presoak_s > 0:
        write_row(rig, row, {col: v_write})
        t_ps = hw.ticks_ms()
        wait_until(rig, t_ps, presoak_s, temp)
    write_row(rig, row, {col: v_write})
    if wwl_hold != CONFIG["wwl_off"] and CONFIG["switch"] != "relay":
        rig.set_wwl(row, wwl_hold)
    t0 = hw.ticks_ms()
    hw.emit("t_s,i_read_A,v_sn_est,temp_c,label")
    for ts in log_times(duration_s, CONFIG["ppd"], CONFIG["t_first_s"]):
        wait_until(rig, t0, ts, temp)
        i = _quiet_read(rig, row, col, temp)
        hw.emit("%.2f,%.6e,%.4f,%.2f,%s" % (hw.elapsed_s(t0), i, v_from_i(rows, i), rig.temp_c(), label))
    rig.row_select(-1)
    rig.set_wwl(row, CONFIG["wwl_off"])
    hw.close_log()


def read_disturb(rig, n=1000, row=0, col=0):
    if (row, col) not in _STATE["cal"]:
        calibrate(rig, row, col, quiet=True)
    rows = _STATE["cal"][(row, col)]
    v0, v1 = levels_for(rig, row, col)
    write_row(rig, row, {col: v1})
    t0 = hw.ticks_ms()
    i_first = read_cell(rig, row, col, 8)
    t_a = hw.elapsed_s(t0)
    for _ in range(n):
        read_cell(rig, row, col, 1)
    t_b = hw.elapsed_s(t0)
    i_last = read_cell(rig, row, col, 8)
    v_a, v_b = v_from_i(rows, i_first), v_from_i(rows, i_last)
    hw.emit("# read disturb: %d reads in %.1f s" % (n, t_b - t_a))
    hw.emit("n_reads,i_first_A,i_last_A,v_first,v_last,dv_mV,elapsed_s")
    hw.emit("%d,%.4e,%.4e,%.4f,%.4f,%.2f,%.1f" % (n, i_first, i_last, v_a, v_b, 1000 * (v_a - v_b), t_b - t_a))
    hw.emit("# compare dv with the droop a quiet hold of the same length shows: equal = reads are harmless")


def hold_bias(rig, levels=None, hold_s=600, row=0, col=0, temp=None, label="holdbias"):
    """Leakage vs hold word-line level: subthreshold physics predicts ~10x per SS volts.
    Choose levels from YOUR E7 transfer curve (E8 step 9). Each level stops early once 10% of the
    stored voltage is lost, so a leaky level cannot empty the node before it is measured."""
    if levels is None:
        if CONFIG["switch"] == "si":
            hw.emit("# ERROR: with switch='si' pass levels <= Vth - 1 V of YOUR 2N7000, "
                    "e.g. levels=(0.5, 0.25, 0.0) for a 1.5 V part")
            return
        levels = (6.0, 5.0, 4.0, 0.0)       # about Vth-2, -3, -4 and 0 V for Vth 8 V, SS 1 V/dec
    hw.set_log(label + ".csv")
    if (row, col) not in _STATE["cal"]:
        calibrate(rig, row, col, quiet=True)
    rows = _STATE["cal"][(row, col)]
    v0, v1 = levels_for(rig, row, col)
    temp = set_temperature(rig, temp)
    hw.emit("wwl_hold_V,v_start,v_end,hold_s,I_leak_A")
    for lvl in levels:
        write_row(rig, row, {col: v1})
        rig.set_wwl(row, lvl)
        hw.sleep_ms(CONFIG["wwl_fall_ms"])
        va = v_from_i(rows, read_cell(rig, row, col, 8))
        t0 = hw.ticks_ms()
        vb, dt = va, 0.0
        for ts in log_times(hold_s, 10, 1.0)[1:]:
            wait_until(rig, t0, ts, temp)
            vb = v_from_i(rows, read_cell(rig, row, col, 4))
            dt = hw.elapsed_s(t0)
            if va - vb >= 0.1 * max(va, 0.1):
                break
        dt = max(dt, 1e-3)
        hw.emit("%.2f,%.4f,%.4f,%.1f,%.3e" % (lvl, va, vb, dt, CONFIG["c_sn"] * (va - vb) / dt))
        rig.set_wwl(row, CONFIG["wwl_off"])
    hw.close_log()


def calibrate_all(rig):
    for r in (0, 1):
        for c in (0, 1):
            calibrate(rig, r, c, quiet=True)


def array_write(rig, bits):
    """bits = [b00, b01, b10, b11] (row-major)."""
    for r in (0, 1):
        cv = {}
        for c in (0, 1):
            v0, v1 = levels_for(rig, r, c)
            cv[c] = v1 if bits[2 * r + c] else v0
        write_row(rig, r, cv)


def array_read(rig):
    got, cur = [], []
    for r in (0, 1):
        for c in (0, 1):
            rows = _STATE["cal"][(r, c)]
            v0, v1 = levels_for(rig, r, c)
            i = read_cell(rig, r, c, 4)
            cur.append(i)
            got.append(1 if i > threshold_current(rows, v0, v1) else 0)
    return got, cur


def pattern_test(rig, wait_s=60):
    calibrate_all(rig)
    hw.emit("pattern,expected,got,pass,i00,i01,i10,i11")
    n_pass = 0
    for p in range(16):
        bits = [(p >> (3 - k)) & 1 for k in range(4)]
        array_write(rig, bits)
        t0 = hw.ticks_ms()
        wait_until(rig, t0, wait_s, None)
        got, cur = array_read(rig)
        ok = got == bits
        n_pass += 1 if ok else 0
        hw.emit("%d,%s,%s,%d,%.3e,%.3e,%.3e,%.3e" % (p, "".join(str(b) for b in bits),
                                                  "".join(str(b) for b in got), 1 if ok else 0,
                                                  cur[0], cur[1], cur[2], cur[3]))
    hw.emit("# %d of 16 patterns correct after %d s" % (n_pass, wait_s))
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
            v0, v1 = levels_for(rig, 0, c)
            cv[c] = v1 if b else v0
        write_row(rig, 0, cv)
    dt = hw.elapsed_s(t0)
    v_after = [v_from_i(_STATE["cal"][(1, c)], read_cell(rig, 1, c, 8)) for c in (0, 1)]
    hw.emit("col,v_before,v_after,dv_mV,elapsed_s,n_writes_row0")
    for c in (0, 1):
        hw.emit("%d,%.4f,%.4f,%.2f,%.1f,%d" % (c, v_before[c], v_after[c],
                                               1000 * (v_before[c] - v_after[c]), dt, n))
    hw.emit("# compare with a quiet hold of the same length (retention data): the excess is disturb")


def run(test="calibrate", switch=None, sim=None, **kw):
    """switch is REQUIRED: 'tft', 'si' or 'relay', matching what is in the socket. A forgotten
    switch='si' would otherwise put the 27 V oxide word line on a 2N7000 gate rated 20 V."""
    if switch not in ("tft", "si", "relay"):
        print("# ERROR: pass switch='tft' | 'si' | 'relay' (it must match what is in the socket)")
        return
    CONFIG["switch"] = switch
    mode_switch = {"tft": "oxide", "si": "si", "relay": "relay"}[switch]
    use_sim = sim or (sim is None and hw.SIM)
    if use_sim:
        rig = hw.make_rig(True, mode="cell", switch=mode_switch)
        hw.emit("# SIMULATION: leakage values are assumptions (t4_hw.SimCell.LEAK), the oxide one "
                "deliberately above the relay floor. Real home TFTs are predicted to sit AT the floor.")
    else:
        rig = hw.make_rig(False)
    try:
        two_cols = test in ("pattern", "disturb")
        vos = rig.zero_offset(n=32, set_sources=False, chans=(0, 1) if two_cols else (0,))
        hw.emit("# TIA offset(s) subtracted: %s mV" % ", ".join("%.3f" % (x * 1e3) for x in vos))
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
            hw.emit("# unknown test " + str(test))
    finally:
        rig.all_safe()
        hw.close_log()


def _cli():
    import argparse
    import contextlib
    ap = argparse.ArgumentParser(description="E8 gain-cell experiments (simulation on a PC)")
    ap.add_argument("--sim", action="store_true")
    ap.add_argument("--test", default="calibrate",
                    choices=["calibrate", "retention", "read_disturb", "hold_bias", "pattern", "disturb"])
    ap.add_argument("--switch", default="tft", choices=["tft", "si", "relay"],
                    help="simulated write switch. The simulated leakages are ASSUMED values "
                         "(oxide 1 pA / Ea 0.35 eV, deliberately above the 0.1 pA relay floor; "
                         "si 10 pA / 0.80 eV), not predictions: a real home TFT is predicted to "
                         "leak ~1e-15 A at WWL 0 V, below the rig floor")
    ap.add_argument("--temp", type=float, default=None)
    ap.add_argument("--duration", type=float, default=3600.0)
    ap.add_argument("--wwl-hold", type=float, default=None, help="hold word-line level (TFT only)")
    ap.add_argument("--levels", default=None, help="hold_bias levels, comma-separated volts")
    ap.add_argument("--presoak", type=float, default=None, help="presoak seconds (default 600)")
    ap.add_argument("--label", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if not a.sim:
        print("On a PC this script only runs with --sim. On the Pico use mpremote (see header).")
        return 2
    kw = {}
    if a.test == "retention":
        kw = {"duration_s": a.duration, "temp": a.temp, "label": a.label or a.switch,
              "wwl_hold": a.wwl_hold, "presoak_s": a.presoak}
    elif a.test == "hold_bias":
        kw = {"temp": a.temp}
        if a.levels:
            kw["levels"] = tuple(float(x) for x in a.levels.split(","))
    elif a.test == "pattern":
        kw = {"wait_s": 60}
    if a.out:
        with open(a.out, "w") as f, contextlib.redirect_stdout(f):
            run(a.test, switch=a.switch, sim=True, **kw)
        print("wrote", a.out)
    else:
        run(a.test, switch=a.switch, sim=True, **kw)
    return 0


if __name__ == "__main__":
    if hw.is_micropython():
        print("Use: import pico_gaincell as g; g.run('calibrate', switch='relay')")
    else:
        import sys
        sys.exit(_cli())
