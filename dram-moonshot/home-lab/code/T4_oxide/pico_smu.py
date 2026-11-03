# pico_smu.py -- transfer, output and gate-leakage sweeps for a home-made oxide TFT (E7).
#
# REFERENCE CODE -- UNTESTED ON HARDWARE. Syntax-checked; logic exercised on a PC with --sim.
# Needs t4_hw.py next to it. Track T4, dram-moonshot home lab.
#
# On the Pico (MicroPython), from a computer with mpremote installed:
#   mpremote cp t4_hw.py pico_smu.py :
#   mpremote exec "import t4_hw as h; h.calibrate_dacs()"                 (once, NO device connected)
#   mpremote exec "import pico_smu; pico_smu.run('floor')"           > floor.csv   (nothing connected)
#   mpremote exec "import pico_smu; pico_smu.run('gleak')"           > gleak.csv
#   mpremote exec "import pico_smu; pico_smu.run('transfer', vd=17.5)" > transfer_sat.csv
#   mpremote exec "import pico_smu; pico_smu.run('output')"          > output.csv
# then on the computer:
#   python3 iv_analysis.py transfer transfer_sat.csv --gleak gleak.csv --W 3000 --L 100 --tox-nm 300
#
# On a PC without hardware (simulated TFT):
#   python3 pico_smu.py --sim --mode transfer --out sim_transfer.csv
#
# Voltages: the TFT source sits on the TIA virtual node at VREF (2.5 V). So
#   Vgs = V(gate node) - 2.5 V  (range -2.5 .. +24.5 V; the LM358 tops out at 27 V)
#   Vds = V(drain node) - 2.5 V (up to 17.5 V)
# Every sweep first zeroes the TIA offset (t4_hw.zero_offset) with the gate node at 0 V and the
# drain at VREF, so no current can flow. Lines starting with '#' are comments; iv_analysis.py
# skips them.

import t4_hw as hw

DEFAULTS = {
    "vd": 17.5,               # Vds for the saturation curve (drain node max 20 V minus 2.5 V VREF)
    "vg_start": -2.5, "vg_stop": 24.5, "vg_step": 0.25,
    "settle_ms": 300,         # per step: RC filter (~2 x 16 ms) + slow traps in the film
    "dual": True,             # forward then reverse sweep (hysteresis)
    "out_vgs": (10.0, 15.0, 20.0, 24.0),
    "out_vd_stop": 17.5, "out_vd_step": 0.25,
    "n_avg": 4,
}


def _frange(a, b, step):
    n = int(round((b - a) / step))
    return [a + k * step for k in range(n + 1)]


def _row(mode, d, vgs, vds, i, rng, t0):
    hw.emit("%s,%s,%.4f,%.4f,%.6e,%s,%.2f" % (mode, d, vgs, vds, i, rng, hw.elapsed_s(t0)))


def _zero(rig, set_sources=True):
    vos = rig.zero_offset(n=32, set_sources=set_sources)
    hw.emit("# TIA0 offset %.4f mV = %.2f pA on the 100 Mohm range (subtracted from every reading)"
            % (vos[0] * 1e3, vos[0] / hw.CFG["r_hi"] * 1e12))
    if abs(vos[0]) > 2e-3:
        hw.emit("# WARNING: offset > 2 mV. Is the op-amp an LMC6482AIN (A grade)? Is the input clean?")


def floor_test(rig, n=60, n_avg=8):
    """Nothing connected to the TIA input. Measures the offset, then n offset-corrected readings
    on the 100 Mohm range. Their standard deviation is your current floor."""
    hw.emit("# floor test: NOTHING connected to the TIA input; 100 Mohm range")
    if getattr(rig, "sim_connect", None):
        rig.sim_connect("open")
    _zero(rig, set_sources=False)
    hw.emit("mode,dir,vgs,vds,id,range,t_s")
    t0 = hw.ticks_ms()
    xs = []
    for _ in range(n):
        i, rng = rig.read_current(0, n_avg, autorange=False)
        xs.append(i)
        _row("floor", "f", 0.0, 0.0, i, rng, t0)
    mean = sum(xs) / len(xs)
    sd = (sum((x - mean) ** 2 for x in xs) / max(1, len(xs) - 1)) ** 0.5
    hw.emit("# floor: mean %.3e A (should be ~0 after offset removal), std %.3e A = your floor"
            % (mean, sd))
    return mean, sd


def transfer(rig, vd=None, vg_start=None, vg_stop=None, vg_step=None, settle_ms=None, dual=None):
    p = DEFAULTS
    vd = p["vd"] if vd is None else vd
    vg_start = p["vg_start"] if vg_start is None else vg_start
    vg_stop = p["vg_stop"] if vg_stop is None else vg_stop
    vg_step = p["vg_step"] if vg_step is None else vg_step
    settle_ms = p["settle_ms"] if settle_ms is None else settle_ms
    dual = p["dual"] if dual is None else dual
    vref = hw.CFG["vref"]
    vg_stop = min(vg_stop, hw.CFG["gate_max"] - vref)
    hw.emit("# transfer sweep: Vds=%.2f V, Vgs %.2f..%.2f V step %.2f, settle %d ms" %
            (vd, vg_start, vg_stop, vg_step, settle_ms))
    hw.emit("mode,dir,vgs,vds,id,range,t_s")
    t0 = hw.ticks_ms()
    up = _frange(vg_start, vg_stop, vg_step)
    sweeps = [("f", up)]
    if dual:
        sweeps.append(("r", list(reversed(up))[1:]))
    rig.set_gate(vg_start + vref)
    rig.set_drain(vd + vref)
    hw.sleep_ms(2000)
    for d, seq in sweeps:
        for vgs in seq:
            rig.set_gate(vgs + vref)
            hw.sleep_ms(settle_ms)
            i, rng = rig.read_current(0, p["n_avg"])
            g, dn = rig.monitor()
            _row("transfer", d, g - vref, dn - vref, i, rng, t0)
    rig.set_gate(0.0)
    rig.set_drain(vref)          # Vds = 0


def output(rig, vgs_list=None, vd_stop=None, vd_step=None, settle_ms=None):
    p = DEFAULTS
    vgs_list = p["out_vgs"] if vgs_list is None else vgs_list
    vd_stop = p["out_vd_stop"] if vd_stop is None else vd_stop
    vd_step = p["out_vd_step"] if vd_step is None else vd_step
    settle_ms = p["settle_ms"] if settle_ms is None else settle_ms
    vref = hw.CFG["vref"]
    hw.emit("# output curves: Vgs in %s, Vds 0..%.2f V" % (str(vgs_list), vd_stop))
    hw.emit("mode,dir,vgs,vds,id,range,t_s")
    t0 = hw.ticks_ms()
    for vgs in vgs_list:
        rig.set_gate(vgs + vref)
        for vds in _frange(0.0, vd_stop, vd_step):
            rig.set_drain(vds + vref)
            hw.sleep_ms(settle_ms)
            i, rng = rig.read_current(0, p["n_avg"])
            g, dn = rig.monitor()
            _row("output", "f", g - vref, dn - vref, i, rng, t0)
        rig.set_drain(vref)
    rig.set_gate(0.0)


def gate_leak(rig, vg_stop=24.5, vg_step=1.0, settle_ms=2000):
    """Wire source AND drain pads together to the TIA input; leave the drain amplifier unplugged.
    Every amp the TIA sees is then gate current through the oxide (plus displacement current
    right after each step -- hence the long settle). Pass the file to iv_analysis.py --gleak."""
    vref = hw.CFG["vref"]
    hw.emit("# gate leakage: S and D tied to TIA, drain amplifier disconnected")
    if getattr(rig, "sim_connect", None):
        rig.sim_connect("gleak")
    hw.emit("mode,dir,vgs,vds,ig,range,t_s")
    t0 = hw.ticks_ms()
    for vgs in _frange(-2.5, min(vg_stop, hw.CFG["gate_max"] - vref), vg_step):
        rig.set_gate(vgs + vref)
        hw.sleep_ms(settle_ms)
        i, rng = rig.read_current(0, 8)
        _row("gleak", "f", vgs, 0.0, i, rng, t0)
    rig.set_gate(0.0)


def run(mode="transfer", sim=None, zero=True, **kw):
    rig = hw.make_rig(sim)
    try:
        if mode == "floor":
            floor_test(rig, **kw)
            return
        if zero:
            if mode == "gleak" and getattr(rig, "sim_connect", None):
                rig.sim_connect("gleak")
            _zero(rig, set_sources=(mode != "gleak"))
        if mode == "transfer":
            transfer(rig, **kw)
        elif mode == "output":
            output(rig, **kw)
        elif mode == "gleak":
            gate_leak(rig, **kw)
        else:
            hw.emit("# unknown mode " + str(mode))
    finally:
        rig.all_safe()


def _cli():
    import argparse
    import contextlib
    ap = argparse.ArgumentParser(description="T4 mini-SMU sweeps (simulation on a PC)")
    ap.add_argument("--sim", action="store_true", help="simulate a TFT instead of using hardware")
    ap.add_argument("--mode", choices=["transfer", "output", "gleak", "floor"], default="transfer")
    ap.add_argument("--vd", type=float, default=None)
    ap.add_argument("--no-zero", action="store_true", help="skip the TIA offset zeroing (to see its effect)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if not a.sim:
        print("On a PC this script only runs with --sim. On the Pico use mpremote (see header).")
        return 2
    kw = {"vd": a.vd} if (a.mode == "transfer" and a.vd is not None) else {}
    if a.mode != "floor":
        kw["zero"] = not a.no_zero
    if a.out:
        with open(a.out, "w") as f, contextlib.redirect_stdout(f):
            run(a.mode, sim=True, **kw)
        print("wrote", a.out)
    else:
        run(a.mode, sim=True, **kw)
    return 0


if __name__ == "__main__":
    if hw.is_micropython():
        print("Use: import pico_smu; pico_smu.run('floor' | 'gleak' | 'transfer' | 'output')")
    else:
        import sys
        sys.exit(_cli())
