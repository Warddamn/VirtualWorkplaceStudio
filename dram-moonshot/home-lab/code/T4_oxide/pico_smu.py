# pico_smu.py -- transfer, output and gate-leakage sweeps for a home-made oxide TFT (E7).
#
# REFERENCE CODE -- UNTESTED ON HARDWARE. Syntax-checked; logic exercised on a PC with --sim.
# Needs t4_hw.py next to it. Track T4, dram-moonshot home lab.
#
# On the Pico (MicroPython), from a computer with mpremote installed:
#   mpremote cp t4_hw.py pico_smu.py :
#   mpremote exec "import pico_smu; pico_smu.run('transfer', vd=17.5)" > transfer.csv
#   mpremote exec "import pico_smu; pico_smu.run('output')"          > output.csv
#   mpremote exec "import pico_smu; pico_smu.run('gleak')"           > gate_leak.csv
# then on the computer:
#   python3 iv_analysis.py transfer transfer.csv --W 1000 --L 10 --tox-nm 300 --svg transfer.svg
#
# On a PC without hardware (simulated TFT):
#   python3 pico_smu.py --sim --mode transfer --out sim_transfer.csv
#
# Voltages: the TFT source sits on the TIA virtual node at VREF (2.5 V). So
#   Vgs = V(gate node) - 2.5 V  (range -2.5 .. +25.5 V)   Vds = V(drain node) - 2.5 V
# Lines starting with '#' are comments; iv_analysis.py skips them.

import t4_hw as hw

DEFAULTS = {
    "vd": 17.5,               # Vds for the saturation curve (drain node max 20 V minus 2.5 V VREF)
    "vg_start": -2.5, "vg_stop": 25.5, "vg_step": 0.25,
    "settle_ms": 300,         # per step: RC filter (~2 x 16 ms) + slow traps in the film
    "dual": True,             # forward then reverse sweep (hysteresis)
    "out_vgs": (10.0, 15.0, 20.0, 25.0),
    "out_vd_stop": 17.5, "out_vd_step": 0.25,
    "n_avg": 4,
}


def _frange(a, b, step):
    n = int(round((b - a) / step))
    return [a + k * step for k in range(n + 1)]


def _row(mode, d, vgs, vds, i, rng, t0):
    print("%s,%s,%.4f,%.4f,%.6e,%s,%.2f" % (mode, d, vgs, vds, i, rng, hw.elapsed_s(t0)))


def transfer(rig, vd=None, vg_start=None, vg_stop=None, vg_step=None, settle_ms=None, dual=None):
    p = DEFAULTS
    vd = p["vd"] if vd is None else vd
    vg_start = p["vg_start"] if vg_start is None else vg_start
    vg_stop = p["vg_stop"] if vg_stop is None else vg_stop
    vg_step = p["vg_step"] if vg_step is None else vg_step
    settle_ms = p["settle_ms"] if settle_ms is None else settle_ms
    dual = p["dual"] if dual is None else dual
    vref = hw.CFG["vref"]
    print("# transfer sweep: Vds=%.2f V, Vgs %.2f..%.2f V step %.2f, settle %d ms" %
          (vd, vg_start, vg_stop, vg_step, settle_ms))
    print("mode,dir,vgs,vds,id,range,t_s")
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
    print("# output curves: Vgs in %s, Vds 0..%.2f V" % (str(vgs_list), vd_stop))
    print("mode,dir,vgs,vds,id,range,t_s")
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


def gate_leak(rig, vg_stop=25.5, vg_step=1.0, settle_ms=2000):
    """Wire source AND drain pads together to the TIA input; leave the drain amplifier unplugged.
    Every amp the TIA sees is then gate current through the oxide (plus displacement current
    right after each step -- hence the long settle)."""
    vref = hw.CFG["vref"]
    print("# gate leakage: S and D tied to TIA, drain amplifier disconnected")
    print("mode,dir,vgs,vds,ig,range,t_s")
    t0 = hw.ticks_ms()
    for vgs in _frange(-2.5, vg_stop, vg_step):
        rig.set_gate(vgs + vref)
        hw.sleep_ms(settle_ms)
        i, rng = rig.read_current(0, 8)
        _row("gleak", "f", vgs, 0.0, i, rng, t0)
    rig.set_gate(0.0)


def run(mode="transfer", sim=None, **kw):
    rig = hw.make_rig(sim)
    try:
        if mode == "transfer":
            transfer(rig, **kw)
        elif mode == "output":
            output(rig, **kw)
        elif mode == "gleak":
            gate_leak(rig, **kw)
        else:
            print("# unknown mode", mode)
    finally:
        rig.all_safe()


def _cli():
    import argparse
    import contextlib
    ap = argparse.ArgumentParser(description="T4 mini-SMU sweeps (simulation on a PC)")
    ap.add_argument("--sim", action="store_true", help="simulate a TFT instead of using hardware")
    ap.add_argument("--mode", choices=["transfer", "output", "gleak"], default="transfer")
    ap.add_argument("--vd", type=float, default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if not a.sim:
        print("On a PC this script only runs with --sim. On the Pico use mpremote (see header).")
        return 2
    kw = {"vd": a.vd} if (a.mode == "transfer" and a.vd is not None) else {}
    if a.out:
        with open(a.out, "w") as f, contextlib.redirect_stdout(f):
            run(a.mode, sim=True, **kw)
        print("wrote", a.out)
    else:
        run(a.mode, sim=True, **kw)
    return 0


if __name__ == "__main__":
    if hw.is_micropython():
        run("transfer")
    else:
        import sys
        sys.exit(_cli())
