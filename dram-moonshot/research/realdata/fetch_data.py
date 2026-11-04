#!/usr/bin/env python3
"""
fetch_data.py -- re-download the public data used by REALDATA_RAW_BER.md, and print how to get the rest.

The raw data is NOT kept in this repository: the SAFARI repository has no license file (all rights reserved by
default), and the field datasets are large and/or registration-gated. Only derived summaries are committed.

Usage (stdlib only):
  python3 -I research/realdata/fetch_data.py --dest ~/dram-realdata         # download what can be automated
  python3 -I research/realdata/fetch_data.py --list                         # list every dataset and its status
  python3 -I research/realdata/fetch_data.py --selftest

Each file lands in its own new directory under --dest (treat downloads as untrusted data: read them with
python3 -I scripts kept elsewhere). The SHA-256 of each automated file is checked against the value recorded
on 2026-11-04.
"""

import argparse
import hashlib
import os
import sys
import tempfile
import urllib.request

COMMIT = "b2089c3c7c2aac1d0936b4cfc572a675f5fd73f4"  # CMU-SAFARI/DRAM-Voltage-Study, 2017-06-12
AUTO = [
    dict(name="safari_ddr3l_retention",
         url=f"https://raw.githubusercontent.com/CMU-SAFARI/DRAM-Voltage-Study/{COMMIT}/characterization_results/"
             "retention_time_profile.csv",
         file="retention_time_profile.csv", bytes=1539105,
         sha256="307a36057dc7982cd0708f6a85f3b472c86f4794e38d834c858cfa4ca43e8e2c",
         used_by="retention_fit.py --csv <dest>/safari_ddr3l_retention/retention_time_profile.csv"),
    dict(name="safari_ddr3l_voltage_cachelines",
         url=f"https://raw.githubusercontent.com/CMU-SAFARI/DRAM-Voltage-Study/{COMMIT}/characterization_results/"
             "dimm_faulty_cachelines_out.csv",
         file="dimm_faulty_cachelines_out.csv", bytes=3848,
         sha256="e1acb00351d4030cbec16438dd9ffd76e76950ab34a4bf60c33ba5676f40be67",
         used_by="not used (voltage errors, not retention); kept for completeness"),
]
MANUAL = [
    dict(name="Alibaba SRDS'22 DRAM error logs (mcelog, inventory, trouble tickets)",
         where="https://tianchi.aliyun.com/dataset/132973 (described at "
               "https://github.com/alibaba-edu/dcbrain/tree/master/dramdata)",
         license="CC BY-SA 4.0 [REPORTED: search snippet of the Tianchi page]", size="~410 MB zip [REPORTED]",
         how="Log in to Alibaba Cloud Tianchi, download dramdata.zip, unpack mcelog.csv and trouble_tickets.csv, "
             "then: python3 -I research/realdata/field_logs.py --log mcelog.csv --tickets trouble_tickets.csv. "
             "No chip (device) field, so the multi-chip share cannot be computed from it."),
    dict(name="Huawei SmartMem / M2-MFP memory logs (Intel Purley/Whitley, DQ x beat bitmaps)",
         where="https://www.codabench.org/competitions/3586/ (repo: https://github.com/hwcloud-RAS/M2-MFP)",
         license="CC BY-NC 4.0 under competition rules that forbid redistribution [REPORTED: competition terms]; "
                 "repo CC BY-NC-SA 4.0",
         size="unknown [UNVERIFIED]",
         how="Register on Codabench, accept the rules, download train.zip and failure_ticket.csv, keep them out "
             "of git, then run field_logs.py --log <one DIMM file or a concatenation> --tickets failure_ticket.csv."),
    dict(name="Sandia Astra memory error and system monitoring data sets",
         where="https://doi.org/10.5281/zenodo.6515019 (zenodo.org was blocked in this session)",
         license="unknown [UNVERIFIED]", size="unknown [UNVERIFIED]",
         how="Download from Zenodo; check the README for DIMM/rank/bank/row/column fields before mapping columns."),
    dict(name="CMU SAFARI SIGMETRICS 2014 full retention data (Khan et al., VRT study)",
         where="http://www.ece.cmu.edu/~safari/tools/dram-sigmetrics2014-fulldata.html (host blocked here)",
         license="unknown [UNVERIFIED]", size="unknown [UNVERIFIED]",
         how="The most useful missing set for VRT: if it holds per-cell failure lists over time, it can measure "
             "the VRT growth rate g the dossier kill line #4 needs."),
    dict(name="EINSim / BEER / HARP (on-die ECC)",
         where="https://github.com/CMU-SAFARI/EINSim, https://github.com/CMU-SAFARI/BEER, https://github.com/CMU-SAFARI/HARP",
         license="MIT (tools) [REPORTED: READMEs]", size="small",
         how="Simulators only. EINSim's README says the real-chip experimental data was withheld for "
             "confidentiality, so no public on-die-ECC chip data exists from this source."),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(item, dest, opener=urllib.request.urlopen):
    d = os.path.join(dest, item["name"])
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, item["file"])
    if os.path.exists(out) and sha256(out) == item["sha256"]:
        return out, "already present, hash OK"
    tmp = out + ".part"
    with opener(item["url"], timeout=120) as r, open(tmp, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    got = sha256(tmp)
    if got != item["sha256"]:
        os.remove(tmp)
        raise RuntimeError(f"{item['name']}: SHA-256 mismatch ({got}); the upstream file changed")
    os.replace(tmp, out)
    return out, "downloaded, hash OK"


def selftest():
    import io

    payload = b"dimm_name,vendor\nA1,A\n"
    item = dict(name="t", url="mem://x", file="x.csv", bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())

    class Fake(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    with tempfile.TemporaryDirectory() as td:
        p, msg = fetch(item, td, opener=lambda u, timeout: Fake(payload))
        ok = os.path.exists(p) and msg.startswith("downloaded")
        p2, msg2 = fetch(item, td, opener=lambda u, timeout: Fake(payload))
        ok = ok and msg2.startswith("already")
        bad = dict(item, name="t2", sha256="0" * 64)
        try:
            fetch(bad, td, opener=lambda u, timeout: Fake(payload))
            ok = False
        except RuntimeError:
            pass
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Re-download the public data for REALDATA_RAW_BER.md")
    ap.add_argument("--dest", help="directory to download into (outside the repo is best)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.list or not a.dest:
        for it in AUTO:
            print(f"[auto]   {it['name']}: {it['url']} ({it['bytes']} bytes) -> {it['used_by']}")
        for it in MANUAL:
            print(f"[manual] {it['name']}\n         where: {it['where']}\n         license: {it['license']}; "
                  f"size: {it['size']}\n         how: {it['how']}")
        if not a.dest:
            return 0
    for it in AUTO:
        p, msg = fetch(it, os.path.expanduser(a.dest))
        print(f"{it['name']}: {msg}: {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
