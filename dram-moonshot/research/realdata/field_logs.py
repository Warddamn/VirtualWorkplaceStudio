#!/usr/bin/env python3
"""
field_logs.py -- test the raw-ber-contract kill lines that FIELD memory-error logs can speak to.

Field logs come from servers running at the normal refresh rate, so they never show relaxed-refresh behaviour.
They can show: how errors cluster (cell / row / column / bank / rank / chip), how often a fault spans more than
one chip, and whether correctable errors (CEs) come before uncorrectable errors (UEs) or failures.

No public field log with chip-level fields could be downloaded in this session (see REALDATA_RAW_BER.md
section 2). This script is ready for when you get one:
  * Alibaba SRDS'22 "dramdata" (Tianchi; licence reported as CC BY-SA 4.0 [UNVERIFIED]): meclog.tar.gz (sic) with
    sid, memoryid, rankid, bankid, row, col, error_type, error_time; trouble_ticket.tar.gz with sid, failure_type,
    failure_time. Unpack to CSV first. No chip (device) field.
  * Huawei SmartMem / M2-MFP (CC BY-NC 4.0 under competition rules, Codabench registration): per-DIMM logs with
    deviceid, bankgroupid, bankid, rowid, columnid, burst_info (DQ x beat bitmap), error_type, log_time; and
    failure_ticket.csv with serial_number, failure_time. The rules forbid redistribution, so keep it out of git.
    The per-DIMM log files have NO serial_number column (the file name is the serial number), so pass the files
    themselves (--log a.csv b.csv ...): a file with no serial or server column takes its serial from its name.

Run (stdlib + numpy):
  python3 -I research/realdata/field_logs.py --log mcelog.csv [more.csv ...] [--tickets trouble_tickets.csv]
  python3 -I research/realdata/field_logs.py --published     # numbers from published aggregates only
  python3 -I research/realdata/field_logs.py --selftest      # synthetic logs with known answers
Writes research/realdata/field_published_summary.json in --published mode. Exit 0 on success.
"""

import argparse
import csv
import json
import math
import os
import random
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

ALIASES = {
    "serial": ["serial_number", "sn_name"],
    "dimm": ["memoryid", "dimmid"],
    "host": ["sid", "server", "hostname"],
    "socket": ["socketid", "cpuid"],
    "channel": ["channelid"],
    "rank": ["rankid"],
    "device": ["deviceid"],
    "bankgroup": ["bankgroupid"],
    "bank": ["bankid"],
    "row": ["row", "rowid"],
    "col": ["col", "columnid"],
    "burst": ["burst_info"],
    "etype": ["error_type"],
    "time": ["error_time", "log_time", "collect_time"],
}


def pick(header, key):
    for a in ALIASES[key]:
        if a in header:
            return a
    return None


def parse_time(s):
    s = str(s).strip()
    try:
        return float(s)  # unix timestamp
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            d = datetime.strptime(s, fmt)
            # Alibaba anonymised dates start at year 0001: use proleptic ordinal seconds, fine for differences
            return (d.toordinal() * 86400.0) + d.hour * 3600 + d.minute * 60 + d.second
        except ValueError:
            continue
    raise ValueError(f"unparsed time {s!r}")


def load_log(path, default_dimm=None):
    if default_dimm is None:  # SmartMem: one file per DIMM, named by its serial number, with no serial column
        default_dimm = os.path.splitext(os.path.basename(path))[0]
    with open(path, newline="") as f:
        rd = csv.DictReader(f)
        h = rd.fieldnames or []
        cols = {k: pick(h, k) for k in ALIASES}
        if cols["time"] is None or cols["row"] is None or cols["col"] is None or cols["bank"] is None:
            raise ValueError(f"need time, bank, row and column fields; header was {h}")
        recs = []
        for r in rd:
            def g(k, default=None):
                c = cols[k]
                return r[c] if c and r.get(c, "") != "" else default
            serial = g("serial", "" if cols["host"] else default_dimm)  # a multi-server log keys on sid instead
            dimm_parts = [g("host", ""), g("socket", ""), g("channel", ""), g("dimm", ""), serial]
            dev = g("device")
            recs.append(dict(dimm="/".join(str(x) for x in dimm_parts), rank=g("rank", "0"),
                             device=None if dev is None else (g("rank", "0"), dev),  # a chip = (rank, deviceid)
                             bank=(g("bankgroup", "0"), g("bank")), row=g("row"), col=g("col"),
                             burst=int(float(g("burst"))) if g("burst") is not None else None,
                             etype=g("etype"), t=parse_time(g("time")), host=g("host", "")))
    has_device = cols["device"] is not None
    return recs, has_device


def load_tickets(path):
    with open(path, newline="") as f:
        rd = csv.DictReader(f)
        h = rd.fieldnames or []
        key = "sid" if "sid" in h else ("serial_number" if "serial_number" in h else None)
        if key is None or "failure_time" not in h:
            raise ValueError(f"ticket file needs sid/serial_number and failure_time; header was {h}")
        return [dict(key=r[key], ftype=r.get("failure_type", ""), t=parse_time(r["failure_time"])) for r in rd], key


# ------------------------------------------------------------------------------------------------
# Metrics
# ------------------------------------------------------------------------------------------------
def fault_mode(recs):
    """Sridharan-style mode of one DIMM's error set, from distinct addresses."""
    ranks = {r["rank"] for r in recs}
    devs = {r["device"] for r in recs if r["device"] is not None}
    banks = {(r["rank"], r["bank"]) for r in recs}
    if len(devs) > 1:
        return "multi-device"
    if len(ranks) > 1:
        return "multi-rank"
    if len(banks) > 1:
        return "multi-bank"
    rows = {r["row"] for r in recs}
    cols = {r["col"] for r in recs}
    if len(rows) == 1 and len(cols) == 1:
        return "single-cell"
    if len(rows) == 1:
        return "single-row"
    if len(cols) == 1:
        return "single-column"
    return "single-bank"


def burst_counts(b, layout="beat_major"):
    """(DQ count, beat count, bit count) of a 32-bit x4 burst bitmap. layout 'beat_major': bit = beat*4 + dq
    [UNVERIFIED: the SmartMem page says only 'decoded parity error bits in memory DQ and Beat']."""
    bits = [i for i in range(32) if (b >> i) & 1]
    if layout == "beat_major":
        dqs = {i % 4 for i in bits}
        beats = {i // 4 for i in bits}
    else:
        dqs = {i // 8 for i in bits}
        beats = {i % 8 for i in bits}
    return len(dqs), len(beats), len(bits)


def analyse_log(recs, has_device, tickets=None, ticket_key=None, event_window_s=1.0):
    by = defaultdict(list)
    for r in recs:
        by[r["dimm"]].append(r)
    S = dict(n_records=len(recs), n_dimms=len(by), has_device_field=has_device)
    modes = Counter(fault_mode(v) for v in by.values())
    S["fault_modes_per_dimm"] = {k: dict(n=v, share=v / len(by)) for k, v in modes.most_common()}
    # clustering inside each DIMM
    rep, toprow, topcol, topbank = [], [], [], []
    for v in by.values():
        addr = Counter((r["rank"], r["bank"], r["row"], r["col"]) for r in v)
        rep.append(1 - len(addr) / len(v))
        toprow.append(max(Counter((r["rank"], r["bank"], r["row"]) for r in v).values()) / len(v))
        topcol.append(max(Counter((r["rank"], r["bank"], r["col"]) for r in v).values()) / len(v))
        topbank.append(max(Counter((r["rank"], r["bank"]) for r in v).values()) / len(v))
    S["clustering"] = dict(repeat_address_share_median=float(np.median(rep)),
                           top_row_share_median=float(np.median(toprow)), top_col_share_median=float(np.median(topcol)),
                           top_bank_share_median=float(np.median(topbank)),
                           records_in_top_1pct_dimms=float(sum(sorted((len(v) for v in by.values()), reverse=True)
                                                               [:max(1, len(by) // 100)]) / len(recs)))
    # multi-chip events (needs a device field). An event = records on one DIMM chained by gaps <= event_window_s;
    # it is multi-chip if it touches >1 (rank, device). The event CI assumes independent events, but events cluster
    # in a few DIMMs, so the share of DIMMs with any multi-chip event is reported too.
    if has_device:
        ev_total = ev_multi = 0
        dimms_multi = 0
        for v in by.values():
            before = ev_multi
            v = sorted(v, key=lambda r: r["t"])
            cur = [v[0]]
            for r in v[1:]:
                if r["t"] - cur[-1]["t"] <= event_window_s:
                    cur.append(r)
                else:
                    ev_total += 1
                    ev_multi += len({x["device"] for x in cur}) > 1
                    cur = [r]
            ev_total += 1
            ev_multi += len({x["device"] for x in cur}) > 1
            dimms_multi += ev_multi > before
        lo, hi = wilson(ev_multi, ev_total)
        S["multi_chip_events"] = dict(window_s=event_window_s, events=ev_total, multi_chip=ev_multi,
                                      share=ev_multi / ev_total, ci95=[lo, hi], kill_line_share=0.10,
                                      dimms_with_multi_chip_event=dimms_multi,
                                      dimm_share=dimms_multi / len(by), dimm_share_ci95=list(wilson(dimms_multi, len(by))),
                                      verdict="FAIL (>10%)" if lo > 0.10 else ("PASS (<=10%)" if hi <= 0.10 else "UNRESOLVED"))
    # DQ / beat structure and single-bit-before-multi-bit
    bursts = [r for r in recs if r["burst"]]
    if bursts:
        cnt = [burst_counts(r["burst"]) for r in bursts]
        multi = [c[2] > 1 for c in cnt]
        S["burst"] = dict(records=len(bursts), multi_bit_share=float(np.mean(multi)),
                          multi_dq_share=float(np.mean([c[0] > 1 for c in cnt])),
                          multi_beat_share=float(np.mean([c[1] > 1 for c in cnt])))
        prec = n_first_multi = 0
        for v in by.values():
            v = sorted((r for r in v if r["burst"]), key=lambda r: r["t"])
            idx = next((i for i, r in enumerate(v) if burst_counts(r["burst"])[2] > 1), None)
            if idx is None:
                continue
            n_first_multi += 1
            prec += any(burst_counts(r["burst"])[2] == 1 for r in v[:idx])
        if n_first_multi:
            lo, hi = wilson(prec, n_first_multi)
            S["single_before_multi"] = dict(dimms_with_multibit=n_first_multi, preceded_by_single=prec,
                                            share=prec / n_first_multi, ci95=[lo, hi])
    # CE before failure
    if tickets:
        first_ce = defaultdict(list)
        for r in recs:
            first_ce[r["host"] if ticket_key == "sid" else r["dimm"].split("/")[-1]].append(r["t"])  # [-1] = serial
        res = {}
        for lab, win in (("1h", 3600.0), ("24h", 86400.0), ("ever", float("inf"))):
            hit = 0
            for tk in tickets:
                ts = first_ce.get(tk["key"], [])
                hit += any(0 <= tk["t"] - t <= win for t in ts)
            lo, hi = wilson(hit, len(tickets))
            res[lab] = dict(failures=len(tickets), preceded=hit, share=hit / len(tickets), ci95=[lo, hi])
        S["ce_before_failure"] = res
    return S


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ------------------------------------------------------------------------------------------------
# Published-aggregate mode
# ------------------------------------------------------------------------------------------------
M2MFP_MONTHS = [  # Huawei M2-MFP README, Intel Purley columns [REPORTED, CC BY-NC-SA 4.0]
    ("2024-01", 26450, 163, 102423615), ("2024-02", 24682, 133, 97336381), ("2024-03", 26919, 174, 106745981),
    ("2024-04", 29776, 144, 107168332), ("2024-05", 29046, 155, 119407409)]


def iid_multichip_share(p, chips=10, bits_per_chip=64):
    """Share of erroneous 64 B lines whose errors span >1 chip, if raw errors are independent at BER p.
    chips=80, bits_per_chip=8 gives the share spanning >1 byte of RS(80,64) (the dossier's kill #2 wording);
    chips=18, bits_per_chip=32 is a DDR4 x4 RDIMM line (72-bit bus, burst of 8)."""
    q = 1 - (1 - p) ** bits_per_chip
    p1 = 1 - (1 - q) ** chips
    p2 = p1 - chips * q * (1 - q) ** (chips - 1)
    return p2 / p1


def published():
    S = {}
    m = []
    for mon, ce_dimms, fail, ce in M2MFP_MONTHS:
        lo, hi = wilson(fail, ce_dimms)
        m.append(dict(month=mon, ce_dimms=ce_dimms, failed_dimms=fail, monthly_failure_share=fail / ce_dimms,
                      ci95=[lo, hi], ces_per_ce_dimm=ce / ce_dimms))
    tot_d = sum(x[1] for x in M2MFP_MONTHS)
    tot_f = sum(x[2] for x in M2MFP_MONTHS)
    S["m2mfp_purley"] = dict(months=m, pooled_monthly_failure_share=tot_f / tot_d, pooled_ci95=list(wilson(tot_f, tot_d)),
                             note="DIMM counts are DIMMs that logged >=1 CE that month, not the whole fleet [REPORTED]")
    # iid coincidence share at the code limits used by the raw-ber model (models/raw-ber-contract.py section 10.1)
    lims = {"DDR4 RS-8 limit 5.45e-5": 5.446e-5, "DDR4 RS-8 servoed (limit/3)": 5.446e-5 / 3,
            "DDR4 BCH-12 limit 3.3e-4": 3.32e-4}
    S["iid_multichip_share"] = {k: iid_multichip_share(v) for k, v in lims.items()}
    S["iid_multibyte_share_rs80x8"] = {k: iid_multichip_share(v, 80, 8) for k, v in lims.items()}
    S["iid_multichip_share_ddr4_x4_18x32"] = {k: iid_multichip_share(v, 18, 32) for k, v in lims.items()}
    # behind DDR5 on-die SEC only 2+-bit events per 136-bit word escape; their per-chip-slice rate ~ C(136,2) p^2
    p5 = 1.524e-5
    q5 = math.comb(136, 2) * p5 ** 2
    S["iid_multichip_share"]["DDR5 post-SEC events at RS-8 limit 1.52e-5"] = 4.5 * q5  # ~ C(10,2) q^2 / (10 q)
    S["field_published"] = [
        dict(item="Multi-bit share of DDR4 field faults (corrected)", value="~23%", tag="REPORTED",
             url="https://arxiv.org/pdf/2408.15302"),
        dict(item="Multi-bit share of DDR4 field faults (original HPCA 2023 abstract, superseded)", value=">45%",
             tag="REPORTED", url="https://ieeexplore.ieee.org/document/10071066"),
        dict(item="Single-bit share of DRAM faults on Cielo/Hopper by vendor", value="64.6% / 69.5% / 58.4%",
             tag="REPORTED", url="https://sc.osti.gov/-/media/ascr/ascac/pdf/meetings/201512/ResilienceASCAC2015.pdf"),
        dict(item="Single-column share of DRAM faults by vendor", value="8.7% / 8.8% / 11.9%", tag="REPORTED",
             url="https://sc.osti.gov/-/media/ascr/ascac/pdf/meetings/201512/ResilienceASCAC2015.pdf"),
        dict(item="Jaguar: permanent faults share; multi-bit (row/column/bank) share of failures",
             value=">=70%; almost 50%", tag="REPORTED", url="https://math.nist.gov/mcsd/Seminars/2015/2015-07-21-Diniz-presentation.pdf"),
        dict(item="Alibaba: CEs first appear only within 1 h before the failure (short warning)", value=">40% of 2,137",
             tag="REPORTED",
             url="https://shujiehan.github.io/_pages/files/srds22.pdf"),
        dict(item="Astra: faults uniform over socket, column, bank; not over node, rank, slot", value="qualitative",
             tag="REPORTED", url="https://www.osti.gov/servlets/purl/2003151"),
        dict(item="Huawei: predictable UEs (CEs first) are the majority; sudden UEs have no CE first",
             value="qualitative", tag="REPORTED", url="https://arxiv.org/pdf/2406.05354"),
        dict(item="Google fleet: CE rate; DIMMs with errors per year", value="25,000-70,000 FIT/Mbit; >8% of DIMMs",
             tag="REPORTED", url="https://research.google/pubs/dram-errors-in-the-wild-a-large-scale-field-study/"),
    ]
    return S


# ------------------------------------------------------------------------------------------------
# Self-test
# ------------------------------------------------------------------------------------------------
def synth_log(path, tickets_path, seed=3):
    """Synthetic SmartMem-like log: 40 DIMMs with known fault modes; 2 of them get a multi-chip event."""
    rnd = random.Random(seed)
    modes = (["single-cell"] * 16 + ["single-row"] * 8 + ["single-column"] * 8 + ["single-bank"] * 4 +
             ["multi-bank"] * 2 + ["multi-device"] * 2)
    rows, tickets = [], []
    t0 = 1.7e9
    for i, mode in enumerate(modes):
        sn = f"sn_{i}"
        dev, bank, row, col = rnd.randrange(18), rnd.randrange(16), rnd.randrange(1 << 17), rnd.randrange(1 << 10)
        n = rnd.randrange(5, 30)
        for j in range(n):
            d, b, rw, c = dev, bank, row, col
            if mode == "single-row":
                c = rnd.randrange(1 << 10)
            elif mode == "single-column":
                rw = rnd.randrange(1 << 17)
            elif mode == "single-bank":
                rw, c = rnd.randrange(1 << 17), rnd.randrange(1 << 10)
            elif mode == "multi-bank" and j % 2:
                b = (bank + 1) % 16
            t = t0 + i * 1e5 + j * 600.0
            burst = 1 << rnd.randrange(32) if j < n - 1 else (0b11 << 4)  # last record of each DIMM is 2-bit
            rows.append(dict(serial_number=sn, rankid=0, deviceid=d, bankgroupid=0, bankid=b, rowid=rw, columnid=c,
                             burst_info=burst, error_type=1, log_time=t))
            if mode == "multi-device" and j == n - 1:
                rows.append(dict(serial_number=sn, rankid=0, deviceid=(dev + 1) % 18, bankgroupid=0, bankid=b,
                                 rowid=rw, columnid=c, burst_info=1, error_type=1, log_time=t + 0.2))
        if i % 10 == 0:
            tickets.append(dict(serial_number=sn, failure_time=t0 + i * 1e5 + n * 600.0 + 1800.0))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(tickets_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["serial_number", "failure_time"])
        w.writeheader()
        w.writerows(tickets)
    return Counter(modes)


def selftest():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        lp, tp = os.path.join(td, "log.csv"), os.path.join(td, "tickets.csv")
        truth = synth_log(lp, tp)
        recs, hd = load_log(lp)
        tk, key = load_tickets(tp)
        S = analyse_log(recs, hd, tk, key)
        got = {k: v["n"] for k, v in S["fault_modes_per_dimm"].items()}
        if got != dict(truth):
            print(f"FAIL fault modes {got} vs {dict(truth)}")
            ok = False
        mc = S["multi_chip_events"]
        if mc["multi_chip"] != 2:
            print(f"FAIL multi-chip events {mc}")
            ok = False
        if S["single_before_multi"]["share"] != 1.0:
            print(f"FAIL single-before-multi {S['single_before_multi']}")
            ok = False
        if S["ce_before_failure"]["1h"]["share"] != 1.0:
            print(f"FAIL ce_before_failure {S['ce_before_failure']}")
            ok = False
        print(f"selftest: modes {got}; multi-chip {mc['multi_chip']}/{mc['events']} events ({mc['verdict']}); "
              f"single-before-multi {S['single_before_multi']['share']:.2f}")
        if mc["dimms_with_multi_chip_event"] != 2:
            print(f"FAIL DIMM-level multi-chip count {mc['dimms_with_multi_chip_event']}")
            ok = False
        # SmartMem layout: one file per DIMM, named by serial number, no serial column -> serial from the file name
        with open(lp, newline="") as f:
            rd = list(csv.DictReader(f))
        one = [{k: v for k, v in r.items() if k != "serial_number"} for r in rd if r["serial_number"] == "sn_0"]
        sp = os.path.join(td, "sn_0.csv")
        with open(sp, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(one[0]))
            w.writeheader()
            w.writerows(one)
        r1, _ = load_log(sp)
        S1 = analyse_log(r1, True, tk, key)
        if not all(r["dimm"].endswith("/sn_0") for r in r1) or S1["ce_before_failure"]["1h"]["preceded"] != 1:
            print("FAIL serial-from-file-name (SmartMem per-DIMM files)")
            ok = False
    if abs(burst_counts(0b10001)[0] - 1) or burst_counts(0b10001)[1] != 2:
        print("FAIL burst decode")
        ok = False
    # iid coincidence: closed form vs Monte Carlo
    rng = np.random.default_rng(5)
    p = 2e-3
    err = rng.random((40000, 10, 64)) < p
    chips = err.any(axis=2).sum(axis=1)
    mc_share = float(np.mean(chips[chips > 0] > 1))
    if abs(mc_share - iid_multichip_share(p)) > 0.01:
        print(f"FAIL iid share {mc_share:.4f} vs {iid_multichip_share(p):.4f}")
        ok = False
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Field-log tests for the raw-ber-contract kill lines")
    ap.add_argument("--log", nargs="+", help="one or more log CSVs (SmartMem: the per-DIMM files)")
    ap.add_argument("--tickets")
    ap.add_argument("--event-window", type=float, default=1.0)
    ap.add_argument("--published", action="store_true")
    ap.add_argument("--out-dir", default=HERE)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.published:
        S = published()
        os.makedirs(a.out_dir, exist_ok=True)
        p = os.path.join(a.out_dir, "field_published_summary.json")
        with open(p, "w") as f:
            json.dump(S, f, indent=1)
        print(json.dumps({k: S[k] for k in ("iid_multichip_share", "iid_multibyte_share_rs80x8",
                                            "iid_multichip_share_ddr4_x4_18x32")}, indent=1))
        print(f"M2-MFP pooled monthly failure share of CE DIMMs: {S['m2mfp_purley']['pooled_monthly_failure_share']:.4f} "
              f"CI {S['m2mfp_purley']['pooled_ci95']}")
        print(f"[wrote {p}]")
        return 0
    if not a.log:
        ap.error("--log, --published or --selftest is required")
    recs, hd = [], False
    for lp in a.log:
        r_, h_ = load_log(lp)
        recs += r_
        hd = hd or h_
    tk, key = load_tickets(a.tickets) if a.tickets else (None, None)
    print(json.dumps(analyse_log(recs, hd, tk, key, a.event_window), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
