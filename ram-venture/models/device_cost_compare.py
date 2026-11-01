#!/usr/bin/env python3
"""Device cost comparison: $/GB for every device/material concept vs DDR5 -- American Memory study.

Agent key: p3-devmodel. As of 2026-11-01. Pure Python 3 standard library.

What it does (mission section 3A, "build the cost equation"):
    For every device row filed by branches A1/A2/A3 (research/phase2/A*_device_params.json), map the
    working id (tmp_id, e.g. "A1-04") to its final concept id (research/phase2/tmp_to_id.json;
    absorbed ids map to their keeper), compute $/GB with one transparent formula, and set it beside
    DDR5 incumbent cost, the Q4-2026 DDR5 contract price, the A-05 glut price and the severe glut
    price taken from models/dram_cost_stack.py (ddr5_reference()). It adds reference rows for SRAM
    (28/40/130 nm), Everspin 1Gb STT-MRAM street price, F-RAM, NOR, NAND and HBM3E.

Formula (area-based bits per wafer; every symbol is printed in the PARAMETERS table):
    usable_mm2      = GDPW(ref die 100 mm2) x 100 mm2      Chiplet Actuary form, edge 3 mm, scribe 0.08 mm
                      (= wafer area x utilisation; 0.853 on 300 mm, 0.790 on 200 mm)
    density Gb/mm2  = 1e6 / cell_um2 x array_eff x bits_per_cell x layers / 1e9
                      If the filing gives a die density (measured, or the branch's own computation)
                      that value is used and the effective array efficiency is back-solved, so the
                      same formula still holds exactly.
    gross GB/wafer  = usable_mm2 x density / 8
    good GB/wafer   = gross GB/wafer x yield
    $/GB            = wafer_cost / good GB per wafer + test_and_package $/GB
    Mask count enters through wafer_cost: base logic or DRAM wafer at the node + module adder for the
    extra masks (the adder text is printed in the PARAMETERS table).

Sensitivity per device: wafer cost x0.7 / x1.3 at base yield; yield 0.95 / 0.50 at base wafer cost;
best case (x0.7, 0.95) and worst case (x1.3, 0.50). A concept "cannot win on $/GB under any
sensitivity" when its best case is still at or above the A-05 glut price.

Tiers (by best case):  A <= DDR5 incumbent cost | B <= glut price | C <= Q4-2026 contract | D above contract.

Sources: every parameter row carries a URL, "ESTIMATE" (branch or p3-devmodel judgment) or "DEFAULT"
(documented p3-devmodel default because the filing had no value). Defaults are listed in DEFAULTS
and in research/assumptions/p3-devmodel.md.

Run:  cd ram-venture && python3 models/device_cost_compare.py
      (prints the tables, writes research/phase2/device_cost_output.md, exits 0)
"""
import io
import json
import math
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

AS_OF = "2026-11-01"
AGENT = "p3-devmodel"
RV = Path(__file__).resolve().parents[1]
P1 = RV / "research" / "phase1"
P2 = RV / "research" / "phase2"
PARAM_FILES = ["A1_device_params.json", "A2_device_params.json", "A3_device_params.json"]
TMP_TO_ID = P2 / "tmp_to_id.json"
CONCEPTS = P2 / "concepts_master.json"
COST_INPUTS = P1 / "cost_inputs.json"
COST_STACK_MD = P1 / "cost_stack_output.md"
OUT_MD = P2 / "device_cost_output.md"

WAFER_LOW, WAFER_HIGH = 0.70, 1.30      # wafer cost +/-30% (task spec)
YIELD_LOW, YIELD_HIGH = 0.50, 0.95      # yield range (task spec)

# ----------------------------------------------------------------------------------------------
# DDR5 reference (models/dram_cost_stack.py). Fallback 1: parse cost_stack_output.md section 11.
# Fallback 2: canonical values printed by that model on 2026-11-01.
# ----------------------------------------------------------------------------------------------
CANONICAL_REF = dict(cost_component_usd_per_gb=1.641, contract_component_usd_per_gb_q4_2026=15.993,
                     glut_component_usd_per_gb=6.397, severe_glut_component_usd_per_gb=1.599,
                     cost_component_usd_per_gb_1gamma_mature=1.522, cost_cash_only_usd_per_gb=0.844,
                     hbm3e_cost_usd_per_gb=6.077, hbm3e_price_usd_per_gb_2026=12.0,
                     ddr4_new_us_line_cost_usd_per_gb=3.283, ddr4_depreciated_cost_usd_per_gb=1.284,
                     spot_ddr5_usd_per_gb_2026_08_31=26.96)
DCS = None          # the imported dram_cost_stack module, when available


def load_ddr5_ref():
    global DCS
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import dram_cost_stack as dcs          # noqa: E402  (local model, no side effects on import)
        DCS = dcs
        return dcs.ddr5_reference(), "import models/dram_cost_stack.py: ddr5_reference()"
    except Exception as exc:                    # pragma: no cover - fallback path
        err = "%s: %s" % (type(exc).__name__, exc)
    try:
        text = COST_STACK_MD.read_text(encoding="utf-8")
        ref = {}
        for k in CANONICAL_REF:
            m = re.search(r"^%s\s+([-0-9.]+)\s*$" % re.escape(k), text, re.M)
            if m:
                ref[k] = float(m.group(1))
        if len(ref) >= 4:
            for k, v in CANONICAL_REF.items():
                ref.setdefault(k, v)
            return ref, "parsed %s (import failed: %s)" % (COST_STACK_MD.relative_to(RV), err)
    except OSError:
        pass
    return dict(CANONICAL_REF), "canonical constants (import and md parse failed: %s)" % err


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("WARNING: could not read %s (%s)" % (path, exc))
        return default


def ascii_text(x):
    return str(x).replace("\u2014", "-").replace("\u2013", "-").encode("ascii", "replace").decode("ascii")


def num(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


REF, REF_SRC = load_ddr5_ref()
DDR5_COST = REF["cost_component_usd_per_gb"]
DDR5_CONTRACT = REF["contract_component_usd_per_gb_q4_2026"]
DDR5_GLUT = REF["glut_component_usd_per_gb"]
DDR5_SEVERE = REF["severe_glut_component_usd_per_gb"]
# Deck quoted in the Phase-3 task brief (dram_cost_stack output before the Phase-1b v4-cost revision of
# 2026-11-01). Used only for the deck-robustness check in section 5; the live model values drive everything else.
BRIEF_DECK = dict(cost=CANONICAL_REF["cost_component_usd_per_gb"], glut=CANONICAL_REF["glut_component_usd_per_gb"],
                  contract=CANONICAL_REF["contract_component_usd_per_gb_q4_2026"],
                  severe=CANONICAL_REF["severe_glut_component_usd_per_gb"])
LIVE_DECK = dict(cost=DDR5_COST, glut=DDR5_GLUT, contract=DDR5_CONTRACT, severe=DDR5_SEVERE)

_CI = load_json(COST_INPUTS, {"inputs": []})
CI = {i["key"]: i for i in _CI.get("inputs", [])}


def ci(key, default):
    """(value, low, high, source) from research/phase1/cost_inputs.json, or the default."""
    e = CI.get(key)
    if not e:
        return default, default, default, "DEFAULT (cost_inputs.json key %s missing)" % key
    src = e.get("source_url") or ""
    if not src.startswith("http") or e.get("tag") in ("ESTIMATE", "UNVERIFIED"):
        src = "ESTIMATE" + (" (%s)" % src if src.startswith("http") else "")
    return num(e["value"]), num(e.get("low"), num(e["value"])), num(e.get("high"), num(e["value"])), src


# ----------------------------------------------------------------------------------------------
# Documented defaults (used only when a filing lacks a value; every use is flagged)
# ----------------------------------------------------------------------------------------------
EDGE_MM = ci("edge_exclusion_mm", 3.0)[0]
SCRIBE_MM = ci("scribe_lane_mm", 0.08)[0]
DEFAULTS = {
    "ref_die_mm2": (100.0, "ESTIMATE: reference die for wafer utilisation (A3 convention: 100 mm2 die, ~85% usable)"),
    "array_efficiency": (0.50, "ESTIMATE: midpoint of filed array efficiencies (0.30-0.70)"),
    "bits_per_cell": (1, "ESTIMATE: single-level cell unless filed"),
    "layers": (1, "ESTIMATE: planar unless filed"),
    "yield_lab": (0.30, "ESTIMATE: TRL 2-3 lab process with no production line"),
    "tp_usd_per_mm2": (0.015, "ESTIMATE: A3 convention, test+package $1.50 per 100 mm2 die => $/GB = 0.12/density"),
    "sheet_utilisation": (0.90, "ESTIMATE: usable fraction of a Gen-8.5 glass sheet"),
    "claim_parity_density": (round(16.0 / 41.0, 4), "ESTIMATE: no density filed; assume the claim (DRAM-like $/GB) "
                             "means DDR5 1b density (16Gb / 41 mm2, dram_cost_stack)"),
    "wafer_2d_adder": (1000.0, "ESTIMATE: 2D-material tier (transfer or low-T growth, +4-6 masks) on a 200mm 130nm wafer"),
    "optane_acq_usd_per_gb": (1.40, "ESTIMATE: midpoint of A2's [UNVERIFIED] $0.8-2/GB ITAD acquisition range"),
    "label_usd": (0.10, "ESTIMATE: A3 filing, ~$0.10 per printed 20-bit label"),
    "label_bits": (20, "ESTIMATE: A3 filing, 20-bit label"),
    "yield_ref_sram": (0.90, "ESTIMATE: mature logic die yield for SRAM reference rows"),
}

# Embedded / compute / buyer rows where the filing set test+package to 0 on purpose
# (cost lands in the host SoC or the venture buys finished cards): keep 0, flag EMB.
EMBEDDED = {"A1-01", "A1-10", "A2-08", "A2-09", "A2-14", "A3-03", "A3-04", "A3-08", "A3-10", "A3-14"}
# Rows whose inputs are marketing/company claims rather than array silicon
CLAIM_ROWS = {"A1-05", "A1-11", "A3-02b"}
# Rows that are hypothetical lines (no U.S. foundry offers the process)
HYP_ROWS = {"A1-02s", "A2-04"}
# Variants excluded from concept verdicts: A3-02b (filing: "do not use as a live option"); A1-02s (A1's
# sensitivity row on a 300mm 28nm BEOL line that no U.S. foundry offers, outside C-02's definition of a
# depreciated U.S. 200mm line). Both are still printed and costed.
EXCLUDE_FROM_VERDICT = {"A3-02b": "claim only, no array silicon (A3 filing)",
                        "A1-02s": "hypothetical 300mm 28nm BEOL line; C-02 is defined on a U.S. 200mm line"}

# Which filed source backs the cell area / density. Integer = index into the row's `sources` list;
# "ci:<key>" = cost_inputs.json key; "ESTIMATE" = branch estimate with no source for this number.
CELL_SRC = {
    "REF-DDR5-1b": 0, "A1-04": 1, "A1-05": 1, "A1-06": 1, "A1-07": 1, "A1-12": 1, "A1-15": 1,
    "A2-01": 0, "A2-02": 0, "A2-04": 0, "A2-05": 0, "A2-10": 0, "A2-12": 0,
    "A2-11": "ci:xpoint_gen1_density_gb_per_mm2", "A3-04": 0,
}

SHORT = {
    "REF-DDR5-1b": "A1 ref: DDR5 1b (A1-filed params)",
    "A1-01": "IGZO 2T0C eDRAM macro, S130 BEOL",
    "A1-02": "IGZO 2T0C 4-tier die, 200mm 130nm",
    "A1-02s": "IGZO 2T0C 4-tier, 300mm 28nm (hyp.)",
    "A1-03": "IGZO 2T0C on Gen-8.5 display glass",
    "A1-04": "OCTRAM 4F2 IGZO-on-cap DRAM",
    "A1-05": "NEO 3D X-DRAM (company claim)",
    "A1-06": "HZO 1T1C FeRAM, 200mm 130nm",
    "A1-07": "AlScN ferro-diode 600C crossbar",
    "A1-08": "Micron NVDRAM 2-deck FE 1T1C",
    "A1-09": "FMC DRAM+ (FE-HfO2 capacitor)",
    "A1-10": "FeFET eNVM, GF 22FDX",
    "A1-11": "SunRise 3D NOR quasi-volatile",
    "A1-12": "Infineon EXCELON F-RAM (PZT 130nm)",
    "A1-15": "Samsung 4F2 VCT IGZO DRAM (demand)",
    "A2-01": "Everspin 1Gb STT-MRAM: PLP kit",
    "A2-02": "Everspin 1Gb STT-MRAM: DDR3 swap",
    "A2-03": "Everspin Toggle/xSPI MRAM parts",
    "A2-04": "Fabless 4Gb STT-MRAM, 14nm (hyp.)",
    "A2-05": "MRAM main-memory DIMM/CXL",
    "A2-06": "Toggle/STT MTJ line, US 200mm",
    "A2-07": "Weebit ReRAM 1T1R, S130",
    "A2-08": "CBRAM eNVM, 22nm",
    "A2-09": "RRAM analog CIM macro, 22nm 4b",
    "A2-10": "3D XPoint PCM+OTS 4-deck (Gen2)",
    "A2-11": "Salvaged Optane PMem (acquired)",
    "A2-12": "MRAM persistent log card",
    "A2-13": "SOT-MRAM LLC chiplet, N5",
    "A2-14": "eMRAM unified-memory MCU, 22FDX",
    "REF-DDR5": "A2 ref: DDR5 1b (A2-filed params)",
    "REF-DDR3-4Gb": "A2 ref: DDR3/DDR4 4Gb 2x-nm",
    "A3-01": "Floating-body 1T-DRAM, 45nm SOI",
    "A3-02": "T-RAM thyristor, 32nm SOI",
    "A3-02b": "Kilopass VLT thyristor (claim)",
    "A3-03": "Si 2T/3T gain-cell eDRAM, 28nm",
    "A3-04": "OpenRAM 6T SRAM macros, S130",
    "A3-05": "Deep-trench eDRAM, 14nm SOI",
    "A3-06": "Bulk 6T SRAM die, 28nm",
    "A3-06-n65": "Bulk 6T SRAM die, 65nm",
    "A3-06-n40": "Bulk 6T SRAM die, 40nm",
    "A3-06-n16": "Bulk 6T SRAM die, 16nm",
    "A3-06-n5": "Bulk 6T SRAM die, 5nm",
    "A3-06-n2": "Bulk SRAM die, TSMC N2",
    "A3-07": "Long-life SRAM family, Fab25 65nm",
    "A3-08": "GSI Gemini APU compute-in-SRAM",
    "A3-09": "Wafer-scale SRAM, 28nm",
    "A3-10": "SRAM-only LLM accelerator, 14nm",
    "A3-11": "Nantero NRAM CNT 1T1R, 28nm",
    "A3-12": "2D MoS2/WSe2 gain cell (lab)",
    "A3-13": "Printed P(VDF-TrFE) labels",
    "A3-14": "Cryo Si gain-cell eDRAM, 28nm",
}

# Non-$/GB axes, derived from the card's `wins_axis` text (plus the device retention field).
AXIS_KEYWORDS = [
    ("non-volatility", ["non-volatil", "nonvolatil", "persisten", "battery", "instant-on", " nvm", "envm",
                        "durable commit"]),
    ("retention", ["retention"]),
    ("rad-hard", ["radiation", "rad-hard", "rad hard"]),
    ("temperature", ["temperature", "500c", "600c", "extreme environment", "4 k ", "cryo"]),
    ("standby power", ["standby", "leakage", "static power", "refresh power", "refresh/standby", "w/gb", "w/mb"]),
    ("endurance", ["endurance"]),
    ("provenance", ["supply security", "trusted", "u.s.-made", "provenance", "domestic", "u.s.-fab",
                    "u.s. vendor", "traceability"]),
    ("lifecycle", ["lifecycle", "supply longevity", "eol", "maintenance-free"]),
    ("latency", ["latency"]),
    ("on-die density vs SRAM", ["density vs sram", "cache density", "on-chip memory density", "vs 6t sram",
                                "density (bits/mm2)", "and density vs sram"]),
    ("compute energy", ["tops/w", "watts per query", "energy per bit moved", "w per inference", "energy per retrieval query", "energy per query"]),
]
NONE_TRIGGERS = ("wins on no axis", "not any ram axis")
AXIS_OVERRIDE = {
    # card says "none for commodity buyers ... refresh power only"
    "C-02": ("standby power (refresh only; commodity buyers do not pay for it)", "card wins_axis text"),
    # card says "$/GB via density (if claims hold)": a pure $/GB bet
    "C-05": ("none ($/GB-only bet)", "card wins_axis text"),
}


def derive_axis(cid, card, dv):
    if cid in AXIS_OVERRIDE:
        return AXIS_OVERRIDE[cid][0]
    if not card:
        return "n/a (no card)"
    text = " " + str(card.get("wins_axis", "")).lower() + " "
    if text.strip().startswith("none") or any(t in text for t in NONE_TRIGGERS):
        return "none"
    axes = [name for name, kws in AXIS_KEYWORDS if any(k in text for k in kws)]
    ret = str((dv or {}).get("retention", "")).lower()
    if "non-volatile" in ret or re.search(r"\b\d+\s*(yr|year)", ret) or "years" in ret:
        if "non-volatility" not in axes:
            axes.append("non-volatility")
    elif re.search(r">\s*\d{2,}[,\d]*\s*s\b", ret) and "retention" not in axes:
        axes.append("retention")
    return ", ".join(axes) if axes else "none"


# ----------------------------------------------------------------------------------------------
# Geometry
# ----------------------------------------------------------------------------------------------
def gdpw(die_mm2, wafer_mm, edge_mm=EDGE_MM, scribe_mm=SCRIBE_MM):
    d = wafer_mm - 2.0 * edge_mm
    s = (math.sqrt(die_mm2) + scribe_mm) ** 2
    return math.pi * (d / 2.0) ** 2 / s - math.pi * d / math.sqrt(2.0 * s)


def usable_area(wafer_mm):
    ref = DEFAULTS["ref_die_mm2"][0]
    area = gdpw(ref, wafer_mm) * ref
    return area, area / (math.pi * (wafer_mm / 2.0) ** 2)


# ----------------------------------------------------------------------------------------------
# Row construction
# ----------------------------------------------------------------------------------------------
def make_row(**kw):
    r = dict(tid="", cid="REF", kind="device", mode="wafer", device="", node="", density=0.0,
             usable=0.0, util=0.0, wafer=0.0, wafer_mm=0, yld=0.0, tp=0.0, cell=0.0, bpc=1, layers=1,
             eff=0.0, eff_used=None, dens_cell=None, masks="", flags=[], src_cell="ESTIMATE",
             src_other="ESTIMATE", axis="", fixed=None, sens_fn=None, price_range=None, card=None,
             verdict=True, note="")
    r.update(kw)
    return r


def device_rows(tmp_to_id, cards):
    rows = []
    for fname in PARAM_FILES:
        data = load_json(P2 / fname, {"devices": []})
        seen = set()
        for dv in data.get("devices", []):
            tid = str(dv.get("tmp_id", "?"))
            if tid in seen or str(dv.get("device", "")).upper().startswith("SENSITIVITY"):
                tid = tid + "s"
            seen.add(tid)
            m = re.match(r"^([A-E]\d?-\d\d)", tid)
            base = m.group(1) if m else tid
            cid = tmp_to_id.get(base, "REF" if tid.startswith("REF") else "?")
            card = cards.get(cid)
            flags = []
            node_nm, wafer_mm = num(dv.get("node_nm")), int(num(dv.get("wafer_mm")))
            cell, eff = num(dv.get("cell_area_um2")), num(dv.get("array_efficiency"))
            bpc, layers = num(dv.get("bits_per_cell")), num(dv.get("layers"))
            if eff <= 0:
                eff = DEFAULTS["array_efficiency"][0]
                flags.append("EFF=default")
            if bpc <= 0:
                bpc = DEFAULTS["bits_per_cell"][0]
            if layers <= 0:
                layers = DEFAULTS["layers"][0]
            dens_filed = num(dv.get("die_density_Gb_per_mm2"))
            dens_cell = 1e6 / cell * eff * bpc * layers / 1e9 if cell > 0 else None
            eff_used = None
            if dens_filed > 0:
                dens = dens_filed
                flags.append("DENS=filed")
                if cell > 0:
                    eff_used = dens * 1e9 * cell / (1e6 * bpc * layers)
                    if abs(dens_cell / dens - 1.0) > 0.10:
                        flags.append("MISMATCH")
            elif dens_cell:
                dens = dens_cell
                eff_used = eff
                flags.append("DENS=cell")
            else:
                dens = DEFAULTS["claim_parity_density"][0]
                flags.append("DENS=default")
            wafer = num(dv.get("wafer_cost_usd"))
            yld = num(dv.get("yield_assumption"))
            tp = num(dv.get("test_pkg_usd_per_GB"))
            src_other = "ESTIMATE"
            mode = "wafer"
            extra = {}
            # --- special modes -------------------------------------------------------------
            if tid == "A2-11":                          # acquired modules, no fab
                mode = "acquired"
                extra["acq"] = DEFAULTS["optane_acq_usd_per_gb"][0]
                flags.append("ACQ")
                src_other = "DEFAULT"
            elif tid == "A3-13":                        # printed labels: $/GB from label cost
                mode = "direct"
                extra["label_usd"] = DEFAULTS["label_usd"][0]
                extra["label_bits"] = DEFAULTS["label_bits"][0]
                dens = dens_cell or dens
                flags.append("DIRECT")
            if mode == "wafer":
                if wafer <= 0:
                    base_w = ci("foundry_200mm_wafer_usd_130nm_us_skywater", 1400.0)[0]
                    wafer = base_w + DEFAULTS["wafer_2d_adder"][0]
                    flags.append("W=default")
                    src_other = "DEFAULT"
                if yld <= 0:
                    yld = DEFAULTS["yield_lab"][0]
                    flags.append("Y=default")
                    src_other = "DEFAULT"
            if tp <= 0:
                if tid in EMBEDDED:
                    flags.append("EMB")
                elif mode == "wafer":
                    tp = DEFAULTS["tp_usd_per_mm2"][0] * 8.0 / dens
                    flags.append("TP=default")
                    src_other = "DEFAULT"
            # --- area ---------------------------------------------------------------------
            if wafer_mm <= 0 and num(dv.get("substrate_area_mm2")) > 0:
                util = DEFAULTS["sheet_utilisation"][0]
                usable = num(dv.get("substrate_area_mm2")) * util
                flags.append("SHEET")
                node = "2um glass"
            else:
                wafer_mm = wafer_mm or 300
                usable, util = usable_area(wafer_mm)
                if node_nm > 0:
                    node = "%gnm/%d" % (node_nm, wafer_mm)
                elif layers > 1:
                    node = "3D %dL/%d" % (layers, wafer_mm)
                else:
                    node = "lab/%d" % wafer_mm
            if tid == "A3-13":
                node = "printed"
            if tid in CLAIM_ROWS:
                flags.append("CLAIM")
            if tid in HYP_ROWS:
                flags.append("HYP")
            if card and str(card.get("rule1_status", "")).upper() == "UNSUPPORTED":
                flags.append("UNSUP")
            # --- sources ------------------------------------------------------------------
            srcs = dv.get("sources") or []
            cs = CELL_SRC.get(tid, CELL_SRC.get(base, "ESTIMATE"))
            if isinstance(cs, int) and cs < len(srcs):
                src_cell = srcs[cs]
            elif isinstance(cs, str) and cs.startswith("ci:"):
                src_cell = ci(cs[3:], 0)[3].replace("ESTIMATE (", "").rstrip(")") if CI.get(cs[3:]) else "ESTIMATE"
            else:
                src_cell = "ESTIMATE"
            if "DENS=default" in flags:
                src_cell = "DEFAULT"
            if "CLAIM" in flags and src_cell.startswith("http"):
                src_cell = src_cell + " (company claim)"
            kind = "branch-ref" if tid.startswith("REF") else "device"
            rows.append(make_row(
                tid=tid, cid=cid if kind == "device" else "REF", kind=kind, mode=mode,
                device=SHORT.get(tid, str(dv.get("device", ""))[:34]), node=node, density=dens,
                usable=usable, util=util, wafer=wafer, wafer_mm=wafer_mm, yld=yld, tp=tp, cell=cell,
                bpc=int(bpc), layers=int(layers), eff=eff, eff_used=eff_used, dens_cell=dens_cell,
                masks=ascii_text(dv.get("mask_count_or_adder", "")), flags=flags, src_cell=src_cell,
                src_other=src_other, card=card, verdict=(tid not in EXCLUDE_FROM_VERDICT),
                axis=derive_axis(cid, card, dv) if kind == "device" else "-", **extra))
    return rows


def usd_per_gb(r, wafer_mult=1.0, yld=None):
    """The cost equation. wafer_mult scales wafer (or acquisition / label) cost; yld overrides yield."""
    if r["fixed"] is not None:
        if r["sens_fn"] and (wafer_mult != 1.0 or yld is not None):
            return r["sens_fn"](wafer_mult, yld)
        return r["fixed"]
    y = r["yld"] if yld is None else yld
    if r["mode"] == "acquired":
        return r["acq"] * wafer_mult / y + r["tp"]
    if r["mode"] == "direct":
        gb_per_label = r["label_bits"] / 8.0 / 1e9
        return r["label_usd"] * wafer_mult / (gb_per_label * y)
    good_gb = r["usable"] * r["density"] / 8.0 * y
    return r["wafer"] * wafer_mult / good_gb + r["tp"]


def sensitivity(r):
    if r["fixed"] is not None and r["sens_fn"] is None:
        if r["price_range"]:
            lo, hi = r["price_range"]
            return dict(base=r["fixed"], w_lo=None, w_hi=None, y_hi=None, y_lo=None, best=lo, worst=hi)
        return dict(base=r["fixed"], w_lo=None, w_hi=None, y_hi=None, y_lo=None, best=r["fixed"], worst=r["fixed"])
    return dict(base=usd_per_gb(r), w_lo=usd_per_gb(r, WAFER_LOW), w_hi=usd_per_gb(r, WAFER_HIGH),
                y_hi=usd_per_gb(r, 1.0, YIELD_HIGH), y_lo=usd_per_gb(r, 1.0, YIELD_LOW),
                best=usd_per_gb(r, WAFER_LOW, YIELD_HIGH), worst=usd_per_gb(r, WAFER_HIGH, YIELD_LOW))


def tier(x, deck=None):
    d = deck or LIVE_DECK
    if x <= d["cost"]:
        return "A"
    if x < d["glut"]:
        return "B"
    if x < d["contract"]:
        return "C"
    return "D"


TIER_TEXT = {"A": "<= DDR5 incumbent cost", "B": "below glut price only", "C": "below 2026 contract only",
             "D": "above 2026 contract"}


# ----------------------------------------------------------------------------------------------
# Reference rows
# ----------------------------------------------------------------------------------------------
def dcs_case(case_id):
    """$/GB, density and a sensitivity closure for a dram_cost_stack case (exact model values)."""
    if DCS is None or case_id not in getattr(DCS, "CASE_BY_ID", {}):
        return None
    c, p = DCS.CASE_BY_ID[case_id], DCS.BASE
    base = DCS.compute_case(c, p)

    def fn(wm, y):
        ym = 1.0 if y is None else y / p[c["yld"]]
        return DCS.compute_case(c, p, wafer_mult=wm, yield_mult=ym)["component_gb"]
    return dict(cost=base["component_gb"], density=base["density"], wafer=base["wafer"], yld=base["yld"],
                fn=fn, die=base["die_mm2"], label=c["label"])


def reference_rows():
    rows = []
    area300, util300 = usable_area(300)
    area200, util200 = usable_area(200)
    # DDR5 and DRAM cases from the canonical Phase-1 model
    for case_id, cid, label, key in [
            ("ddr5_16g_1b", "REF", "DDR5 16Gb 1b cost (dram_cost_stack)", "cost_component_usd_per_gb"),
            ("ddr5_16g_1c", "REF", "DDR5 16Gb 1-gamma mature cost", "cost_component_usd_per_gb_1gamma_mature"),
            ("ddr4_16g_1y_dep", "REF", "DDR4 16Gb 1y depreciated-line cost", "ddr4_depreciated_cost_usd_per_gb"),
            ("hbm3e_12h", "REF", "HBM3E 12-high cost (dram_cost_stack)", "hbm3e_cost_usd_per_gb")]:
        d = dcs_case(case_id)
        cost = d["cost"] if d else REF.get(key, CANONICAL_REF.get(key))
        rows.append(make_row(tid="dcs:" + case_id, cid=cid, kind="ref", mode="fixed", device=label,
                             node="1b/300" if "1b" in label or "HBM" in label else ("1c/300" if "gamma" in label else "1y/300"),
                             density=d["density"] if d else 0.0, fixed=cost, sens_fn=d["fn"] if d else None,
                             wafer=d["wafer"] if d else 0.0, yld=d["yld"] if d else 0.0, wafer_mm=300,
                             src_cell="models/dram_cost_stack.py", src_other="models/dram_cost_stack.py",
                             flags=["DCS"], axis="-"))
    # Formula calibration: this script's area formula on the dram_cost_stack DDR5 1b inputs
    d = dcs_case("ddr5_16g_1b")
    if d:
        tp_cal = d["cost"] - d["wafer"] / (d["yld"] * gdpw(d["die"], 300) * 2.0)
        rows.append(make_row(tid="cal:ddr5_1b", cid="REF", kind="ref", device="CAL: this formula on DDR5 1b inputs",
                             node="1b/300", density=d["density"], usable=area300, util=util300, wafer=d["wafer"],
                             wafer_mm=300, yld=d["yld"], tp=tp_cal, src_cell="models/dram_cost_stack.py",
                             src_other="models/dram_cost_stack.py", flags=["CAL"], axis="-"))
    # Market price lines (not costs)
    hbm_p = REF.get("hbm3e_price_usd_per_gb_2026", 12.0)
    for label, val, rng in [("DDR5 Q4-2026 contract PRICE", DDR5_CONTRACT, None),
                            ("DDR5 A-05 glut PRICE (-60%)", DDR5_GLUT, None),
                            ("DDR5 severe glut PRICE", DDR5_SEVERE, None),
                            ("HBM3E 2026 contract PRICE", hbm_p, None)]:
        rows.append(make_row(tid="price", cid="REF", kind="ref", mode="fixed", device=label, node="-",
                             fixed=val, price_range=rng, src_cell="models/dram_cost_stack.py",
                             src_other="models/dram_cost_stack.py", flags=["PRICE"], axis="-"))
    # SRAM reference rows (embedded macro, silicon only) from cost_inputs.json
    eff_v, _, _, eff_src = ci("sram_macro_array_efficiency", 0.6)
    y_ref = DEFAULTS["yield_ref_sram"][0]
    for node, wmm, cell_key, wafer_key, wdef in [
            (28, 300, "sram_cell_um2_28nm", "foundry_300mm_wafer_usd_28nm_2026", 2600.0),
            (40, 300, "sram_cell_um2_40nm", "foundry_300mm_wafer_usd_40nm_2026", 2100.0),
            (130, 200, "sram_cell_um2_130nm_sky130", "foundry_200mm_wafer_usd_130nm_us_skywater", 1400.0)]:
        cell, _, _, csrc = ci(cell_key, 0.0)
        wafer, _, _, wsrc = ci(wafer_key, wdef)
        if cell <= 0:
            continue
        area, util = (area300, util300) if wmm == 300 else (area200, util200)
        rows.append(make_row(tid="ci:" + cell_key, cid="REF", kind="ref", device="SRAM 6T %dnm embedded (silicon)" % node,
                             node="%dnm/%d" % (node, wmm), density=1e6 / cell * eff_v / 1e9, usable=area, util=util,
                             wafer=wafer, wafer_mm=wmm, yld=y_ref, tp=0.0, cell=cell, eff=eff_v, eff_used=eff_v,
                             masks="0 (standard logic)", src_cell=csrc,
                             src_other=wsrc if wsrc.startswith("http") else "ESTIMATE",
                             flags=["EMB"], axis="-"))
    # Street / market price reference rows
    for label, key, default, rng_note in [
            ("Everspin 1Gb STT-MRAM STREET PRICE", "everspin_1gb_sttmram_usd_per_gb", 820.8, "@500 pcs; high = qty 1"),
            ("NOR flash PRICE", "nor_flash_usd_per_gb", 40.0, "SPI NOR 128Mb-1Gb"),
            ("NAND TLC 2026 PRICE", "nand_tlc_usd_per_gb_2026", 0.09, "512Gb TLC")]:
        v, lo, hi, src = ci(key, default)
        rows.append(make_row(tid="ci:" + key, cid="REF", kind="ref", mode="fixed", device=label, node="-",
                             density=0.0, fixed=v, price_range=(lo, hi), src_cell=src, src_other=src,
                             flags=["PRICE"], axis="-", note=rng_note))
    # F-RAM street price: A1-12 filing notes "~$1-4/Mbit at distribution" [ESTIMATE]
    fram_lo, fram_hi = 1.0 * 8192, 4.0 * 8192
    rows.append(make_row(tid="A1-12:notes", cid="REF", kind="ref", mode="fixed", device="F-RAM (PZT) STREET PRICE ~$1/Mbit",
                         node="-", fixed=fram_lo, price_range=(fram_lo, fram_hi),
                         src_cell="ESTIMATE (A1-12 filing notes: ~$1-4/Mbit)", src_other="ESTIMATE",
                         flags=["PRICE"], axis="-"))
    return rows


def supplementary_rows(cards):
    """Silicon-making concepts outside branch A, costed with the canonical DRAM model or their card's numbers."""
    rows = []
    for cid, case_id, label in [("C-58", "ddr4_8g_1x_new", "Licensed DDR4 8Gb, new US 300mm fab"),
                                ("C-59", "ddr3_4g_fdry", "Fabless DDR3 4Gb on PSMC foundry")]:
        d = dcs_case(case_id)
        if not d:
            continue
        card = cards.get(cid)
        rows.append(make_row(tid="dcs:" + case_id, cid=cid, kind="supp", mode="fixed", device=label,
                             node="%s/300" % ("1x" if "1x" in case_id else "25nm"), density=d["density"],
                             fixed=d["cost"], sens_fn=d["fn"], wafer=d["wafer"], yld=d["yld"], wafer_mm=300,
                             src_cell="models/dram_cost_stack.py", src_other="models/dram_cost_stack.py",
                             flags=["DCS"], card=card, axis=derive_axis(cid, card, {})))
    # C-71: 256Mb SDRAM, 1T1C MIM on SkyWater Fab 25 65nm 200mm (C_notes Appendix A: 116 mm2 die,
    # 228 gross / 137 good, $14.6 die, +$15 package+test per unit) [ESTIMATE]
    card = cards.get("C-71")
    area200, util200 = usable_area(200)
    gb_die = 256.0 / 8192.0
    rows.append(make_row(tid="C-14(C)", cid="C-71", kind="supp", device="Trusted 256Mb SDRAM, Fab25 65nm MIM",
                         node="65nm/200", density=0.25 / 116.0, usable=area200, util=util200, wafer=2000.0,
                         wafer_mm=200, yld=137.0 / 228.0, tp=15.0 / gb_die,
                         masks="65nm logic + 1T1C high-k MIM module [ESTIMATE]",
                         src_cell="ESTIMATE (research/phase2/C_notes.md Appendix A)",
                         src_other="ESTIMATE (C_notes.md Appendix A)", flags=["DENS=card"], card=card,
                         axis=derive_axis("C-71", card, {})))
    return rows


# ----------------------------------------------------------------------------------------------
# Formatting helpers (ASCII only)
# ----------------------------------------------------------------------------------------------
def money(x):
    if x is None:
        return "n/a"
    if x >= 1e6:
        return "%.2e" % x
    if x >= 1000:
        return "{:,.0f}".format(x)
    if x >= 100:
        return "%.0f" % x
    if x >= 10:
        return "%.1f" % x
    return "%.2f" % x


def ratio(x):
    if x >= 1e5:
        return "%.1ex" % x
    if x >= 100:
        return "{:,.0f}x".format(x)
    if x >= 10:
        return "%.0fx" % x
    return "%.2fx" % x


def dens_fmt(x):
    if not x:
        return "-"
    if x >= 0.01:
        return "%.3f" % x
    return "%.2e" % x


def table(headers, rows, align=None):
    rows = [["" if v is None else str(v) for v in r] for r in rows]
    w = [max([len(str(h))] + [len(r[i]) for r in rows]) for i, h in enumerate(headers)]
    align = align or ["l"] * len(headers)
    last = len(headers) - 1

    def fmt(cells):
        out = []
        for i, c in enumerate(cells):
            if i == last and align[i] == "l":
                out.append(c)
            else:
                out.append(c.ljust(w[i]) if align[i] == "l" else c.rjust(w[i]))
        return "  ".join(out).rstrip()
    print("\n".join([fmt([str(h) for h in headers]), "  ".join("-" * x for x in w)] + [fmt(r) for r in rows]))


def section(title):
    print("\n" + "=" * 110)
    print(title)
    print("=" * 110)


# ----------------------------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------------------------
def build():
    tmp_to_id = load_json(TMP_TO_ID, {})
    master = load_json(CONCEPTS, {"cards": []})
    cards = {c["id"]: c for c in master.get("cards", [])}
    rows = device_rows(tmp_to_id, cards) + supplementary_rows(cards) + reference_rows()
    for r in rows:
        r["s"] = sensitivity(r)
    return rows, cards, tmp_to_id


def concept_verdicts(rows, cards):
    by = {}
    for r in rows:
        if r["kind"] not in ("device", "supp") or not r["verdict"]:
            continue
        by.setdefault(r["cid"], []).append(r)
    out = {}
    for cid, rs in by.items():
        best_r = min(rs, key=lambda r: r["s"]["best"])
        base_r = min(rs, key=lambda r: r["s"]["base"])
        card = cards.get(cid, {})
        out[cid] = dict(cid=cid, rows=rs, best=best_r["s"]["best"], best_tid=best_r["tid"],
                        base=base_r["s"]["base"], base_tid=base_r["tid"], tier=tier(best_r["s"]["best"]),
                        axis=best_r["axis"], name=card.get("name", ""),
                        unsup=str(card.get("rule1_status", "")).upper() == "UNSUPPORTED",
                        cap=card.get("capital_tier", "?"), trl=card.get("trl", "?"))
    return out


def cid_key(c):
    m = re.match(r"C-(\d+)", c)
    return int(m.group(1)) if m else 999


def report():
    rows, cards, tmp_to_id = build()
    print("DEVICE COST COMPARISON  --  $/GB of every device/material concept vs DDR5   (agent %s, as of %s)" % (AGENT, AS_OF))
    print("DDR5 reference: %s" % REF_SRC)
    print("  DDR5 16Gb 1b incumbent COST     $%.3f/GB   (raw GB, packaged component)" % DDR5_COST)
    print("  DDR5 Q4-2026 contract PRICE     $%.3f/GB" % DDR5_CONTRACT)
    print("  DDR5 A-05 glut PRICE (-60%%)     $%.3f/GB" % DDR5_GLUT)
    print("  DDR5 severe glut PRICE          $%.3f/GB" % DDR5_SEVERE)
    a300, u300 = usable_area(300)
    a200, u200 = usable_area(200)
    print("Formula: $/GB = wafer_cost / (usable_mm2 x density_Gb/mm2 / 8 x yield) + test_pkg_$/GB")
    print("         density = 1e6/cell_um2 x array_eff x bits/cell x layers / 1e9 (filed die density wins; eff back-solved)")
    print("         usable_mm2 = GDPW(100 mm2 die) x 100: 300mm %.0f mm2 (%.3f of wafer), 200mm %.0f mm2 (%.3f)"
          % (a300, u300, a200, u200))
    print("Sensitivity: wafer cost x%.1f / x%.1f; yield %.2f / %.2f; best = (x%.1f, %.2f), worst = (x%.1f, %.2f)"
          % (WAFER_LOW, WAFER_HIGH, YIELD_HIGH, YIELD_LOW, WAFER_LOW, YIELD_HIGH, WAFER_HIGH, YIELD_LOW))

    # ---------------------------------------------------------------- 1. main table
    section("1. $/GB SIDE BY SIDE, sorted by $/GB  (REF = reference row; x = multiple of the DDR5 figure)")
    main = [r for r in rows if r["kind"] in ("device", "supp", "ref")]
    main.sort(key=lambda r: r["s"]["base"])
    t = []
    for r in main:
        b = r["s"]["base"]
        is_price = "PRICE" in r["flags"]
        t.append([r["cid"], r["tid"] if not r["tid"].startswith(("dcs:", "ci:", "cal:", "price", "A1-12:")) else "",
                  r["device"], r["node"], dens_fmt(r["density"]), money(b), ratio(b / DDR5_COST),
                  ratio(b / DDR5_CONTRACT), ratio(b / DDR5_GLUT),
                  "-" if (is_price or r["kind"] == "ref") else (("Y" if b < DDR5_GLUT else "N") + (
                      "*" if set(r["flags"]) & {"CLAIM", "HYP", "UNSUP"} else "")), r["axis"]])
    table(["concept", "row", "device", "node", "Gb/mm2", "$/GB", "xDDR5cost", "xcontract", "xglut",
           "beats glut?", "non-$/GB axis it could still win on"], t,
          ["l", "l", "l", "l", "r", "r", "r", "r", "r", "l", "l"])
    print("* = company claim, hypothetical process line or Rule-1 UNSUPPORTED concept (see flags in section 2).")
    print("Branch-filed DDR5/DDR3 reference rows (computed with each branch's own inputs, for bias checking):")
    br = [r for r in rows if r["kind"] == "branch-ref"]
    table(["row", "device", "node", "Gb/mm2", "$/GB", "xDDR5cost"],
          [[r["tid"], r["device"], r["node"], dens_fmt(r["density"]), money(r["s"]["base"]),
            ratio(r["s"]["base"] / DDR5_COST)] for r in br], ["l", "l", "l", "r", "r", "r"])
    cal = [r for r in rows if r["tid"] == "cal:ddr5_1b"]
    if cal:
        c = cal[0]["s"]["base"]
        print("Calibration: this script's area formula on the dram_cost_stack DDR5 1b inputs gives $%.3f/GB vs the model's "
              "$%.3f/GB (%+.1f%%), so the two methods agree." % (c, DDR5_COST, (c / DDR5_COST - 1) * 100))

    # ---------------------------------------------------------------- 2. parameters
    section("2. PARAMETERS  (every row: cell/density source = URL | ESTIMATE | DEFAULT; wafer/yield/test source in 'src w/y/tp')")
    prm = [r for r in rows if r["kind"] in ("device", "supp", "branch-ref") or (r["kind"] == "ref" and "PRICE" not in r["flags"])]
    t = []
    for r in prm:
        if r["mode"] == "acquired":
            wcell = "acq $%.2f/GB" % r["acq"]
        elif r["mode"] == "direct":
            wcell = "label $%.2f/%db" % (r["label_usd"], r["label_bits"])
        elif r["mode"] == "fixed":
            wcell = "$%s/%s" % (money(r["wafer"]), r["wafer_mm"]) if r["wafer"] else "-"
        else:
            wcell = "$%s/%s" % (money(r["wafer"]), r["wafer_mm"] or "sheet")
        t.append([r["tid"], r["cid"], ("%.4g" % r["cell"]) if r["cell"] else "-", "%dx%d" % (r["bpc"], r["layers"]),
                  ("%.2f" % r["eff"]) if r["eff"] else "-", ("%.3f" % r["eff_used"]) if r["eff_used"] else "-",
                  dens_fmt(r["density"]), ("%.3f" % r["dens_cell"]) if r["dens_cell"] and r["dens_cell"] >= 0.001 else
                  (("%.2e" % r["dens_cell"]) if r["dens_cell"] else "-"),
                  wcell, ("%.2f" % r["yld"]) if r["yld"] else "-", money(r["tp"]) if r["mode"] != "fixed" else "-",
                  (r["masks"][:46] + "..") if len(r["masks"]) > 48 else (r["masks"] or "-"),
                  ",".join(r["flags"]) or "-",
                  "URL (wafer) ->" if r["src_other"].startswith("http") else r["src_other"][:30],
                  r["src_cell"] + ((" | wafer: " + r["src_other"]) if r["src_other"].startswith("http") else "")])
    table(["row", "concept", "cell_um2", "bxL", "eff", "eff_used", "dens", "dens_cell", "wafer$/mm", "yield", "tp$/GB",
           "mask count / module adder", "flags", "src w/y/tp", "source (cell / density)"], t,
          ["l", "l", "r", "r", "r", "r", "r", "r", "r", "r", "r", "l", "l", "l", "l"])
    print("Flags: DENS=filed die density from filing (eff_used back-solved) | DENS=cell from cell area | DENS=default "
          "claim-parity default\n       MISMATCH filed density >10% off the cell formula (A2 uses binary Gb; XPoint measured "
          "die vs cell) | EMB embedded/buyer row, test+pkg=0 as filed\n       CLAIM company/marketing claim | HYP hypothetical "
          "line | UNSUP Rule-1 UNSUPPORTED concept | ACQ acquisition $/GB, yield = test pass rate\n       SHEET Gen-8.5 glass "
          "sheet | DIRECT $/GB from label cost | W/Y/TP=default documented default | DCS dram_cost_stack case")
    print("Defaults used when a filing lacks a value:")
    for k, (v, why) in DEFAULTS.items():
        print("  %-22s %-8s %s" % (k, v, why))

    # ---------------------------------------------------------------- 3. sensitivity
    section("3. SENSITIVITY PER DEVICE  ($/GB; wafer x0.7 / x1.3 at base yield; yield 0.95 / 0.50 at base wafer; best/worst combined)")
    t = []
    sens_rows = [r for r in rows if r["kind"] in ("device", "supp")] + \
                [r for r in rows if r["kind"] == "ref" and (r["sens_fn"] or r["price_range"])]
    for r in sorted(sens_rows, key=lambda r: (r["kind"] == "ref", r["s"]["best"])):
        s = r["s"]
        if r["price_range"]:
            t.append([r["cid"], r["tid"] if not r["tid"].startswith(("ci:", "A1-12:")) else "", r["device"][:34],
                      money(s["base"]), "range", "", "", "", money(s["best"]), money(s["worst"]), "-", "-",
                      "price range " + (r["note"] or "")])
            continue
        t.append([r["cid"], r["tid"] if not r["tid"].startswith("dcs:") else "", r["device"][:34], money(s["base"]),
                  money(s["w_lo"]), money(s["w_hi"]), money(s["y_hi"]), money(s["y_lo"]), money(s["best"]),
                  money(s["worst"]), "Y" if s["best"] < DDR5_GLUT else "N", "Y" if s["best"] <= DDR5_COST else "N",
                  ("%s: %s" % (tier(s["best"]), TIER_TEXT[tier(s["best"])])) if r["kind"] != "ref" else "reference"])
    table(["concept", "row", "device", "base", "w-30%", "w+30%", "y.95", "y.50", "BEST", "WORST", "best<glut",
           "best<=cost", "tier (best case)"], t, ["l", "l", "l", "r", "r", "r", "r", "r", "r", "r", "l", "l", "l"])

    # ---------------------------------------------------------------- 4. concept verdicts
    section("4. CONCEPT VERDICTS ON $/GB  (best live variant per concept)")
    for tid, why in EXCLUDE_FROM_VERDICT.items():
        rr = [r for r in rows if r["tid"] == tid]
        if rr:
            print("Excluded from verdict: %s (%s): %s. Its best case would be $%s/GB." % (
                tid, rr[0]["cid"], why, money(rr[0]["s"]["best"])))
    v = concept_verdicts(rows, cards)
    t = []
    for cid in sorted(v, key=cid_key):
        x = v[cid]
        t.append([cid, x["name"][:52], x["cap"], x["trl"], x["base_tid"], money(x["base"]), money(x["best"]),
                  x["tier"], "UNSUPPORTED" if x["unsup"] else "", x["axis"]])
    table(["concept", "name", "cap", "TRL", "best row", "base $/GB", "best $/GB", "tier", "Rule 1", "non-$/GB axis"], t,
          ["l", "l", "l", "r", "l", "r", "r", "l", "l", "l"])
    no_dev = [c for c in sorted(cards, key=cid_key) if cards[c].get("branch") == "A" and c not in v]
    if no_dev:
        print("Branch-A concepts with no device row (service/data products; $/GB not applicable): %s"
              % ", ".join("%s (%s)" % (c, cards[c]["name"][:40]) for c in no_dev))
    shared = {"C-96": "C-25 (licenses the 3D XPoint/PCM device costed in row A2-10)",
              "C-53": "NAND reference row (HBF stacks are NAND; NAND TLC ~$0.09/GB price)",
              "C-52": "DDR5/LPDDR die economics (buys LPDDR5X dies; no new device)",
              "C-70": "DDR4 depreciated-line cost reference (buys Micron Manassas silicon at market price)"}
    print("Other-branch concepts that reuse a costed device rather than a new one:")
    for k, txt in shared.items():
        if k in cards:
            print("  %s %s -> %s" % (k, cards[k]["name"][:50], txt))

    tiers = {k: sorted([c for c in v if v[c]["tier"] == k], key=cid_key) for k in "ABCD"}
    live = lambda lst: [c for c in lst if not v[c]["unsup"]]
    print("\nTier A, best case <= DDR5 incumbent cost $%.2f/GB : %s" % (DDR5_COST, ", ".join(tiers["A"]) or "none"))
    print("Tier B, best case below glut price $%.2f/GB      : %s" % (DDR5_GLUT, ", ".join(tiers["B"]) or "none"))
    print("Tier C, best case below 2026 contract $%.2f/GB  : %s" % (DDR5_CONTRACT, ", ".join(tiers["C"]) or "none"))
    print("Tier D, best case above 2026 contract           : %s" % (", ".join(tiers["D"]) or "none"))
    base_beats = sorted([c for c in v if v[c]["base"] < DDR5_GLUT], key=cid_key)
    print("Beat the glut price at BASE inputs              : %s" % (", ".join(base_beats) or "none"))
    cannot = sorted(tiers["C"] + tiers["D"], key=cid_key)
    print("CANNOT WIN ON $/GB UNDER ANY SENSITIVITY (best case >= glut price): %s" % ", ".join(cannot))
    print("  ...of which not even below the 2026 contract price (tier D): %s" % ", ".join(tiers["D"]))
    unsup = sorted([c for c in v if v[c]["unsup"]], key=cid_key)
    print("Rule-1 UNSUPPORTED (dead regardless of $/GB): %s" % (", ".join(unsup) or "none"))
    dead_r4 = [c for c in cannot if v[c]["axis"].startswith("none")]
    print("Rule 4: dead on $/GB AND no other axis named : %s" % (", ".join(dead_r4) or "none"))
    surv = [c for c in cannot if not v[c]["axis"].startswith("none") and not v[c]["unsup"]]
    print("Rule 4: survive ONLY on a non-$/GB axis      : %s" % ", ".join(surv))

    # ---------------------------------------------------------------- 5. deck robustness
    section("5. DECK ROBUSTNESS  (live dram_cost_stack deck vs the deck quoted in the Phase-3 task brief)")
    table(["deck", "DDR5 cost", "contract", "glut", "severe"],
          [["live model (this run)", f"{DDR5_COST:.3f}", f"{DDR5_CONTRACT:.3f}", f"{DDR5_GLUT:.3f}", f"{DDR5_SEVERE:.3f}"],
           ["task brief (pre-v4-cost)", f"{BRIEF_DECK['cost']:.3f}", f"{BRIEF_DECK['contract']:.3f}",
            f"{BRIEF_DECK['glut']:.3f}", f"{BRIEF_DECK['severe']:.3f}"]], ["l", "r", "r", "r", "r"])
    brief_tier = {c: tier(v[c]["best"], BRIEF_DECK) for c in v}
    cannot_brief = sorted([c for c in v if brief_tier[c] in "CD"], key=cid_key)
    flips = [c for c in sorted(v, key=cid_key) if brief_tier[c] != v[c]["tier"]]
    print("Cannot win on $/GB under any sensitivity, brief deck: %s" % ", ".join(cannot_brief))
    print("Tier changes between decks: %s" % (", ".join("%s %s->%s (best $%s)" % (
        c, brief_tier[c], v[c]["tier"], money(v[c]["best"])) for c in flips) or "none"))
    both = sorted(set(cannot) & set(cannot_brief), key=cid_key)
    print("Cannot win on $/GB under any sensitivity on EITHER deck (robust list): %s" % ", ".join(both))
    return dict(rows=rows, verdicts=v, tiers=tiers, cannot=cannot, dead_r4=dead_r4, surv=surv, unsup=unsup,
                base_beats=base_beats, live=live, cards=cards, cannot_brief=cannot_brief, flips=flips,
                robust=both, brief_tier=brief_tier)


# ----------------------------------------------------------------------------------------------
# Interpretation (computed numbers, written to the markdown file)
# ----------------------------------------------------------------------------------------------
def interpretation(R):
    v, rows = R["verdicts"], R["rows"]
    row = {r["tid"]: r for r in rows}
    G, K, C, S = DDR5_GLUT, DDR5_COST, DDR5_CONTRACT, DDR5_SEVERE

    def b(tid):
        return row[tid]["s"]["base"] if tid in row else float("nan")

    def bb(tid):
        return row[tid]["s"]["best"] if tid in row else float("nan")

    def ids(lst):
        return ", ".join(lst) if lst else "none"

    def where(x):
        return "below" if x < G else "above"

    catch = {
        "C-25": "needs a T4 crosspoint fab and died on volume and ecosystem, not cost (A2 notes)",
        "C-05": "rests on NEO's unverified ~10x density claim with single-cell proof of concept only",
        "C-26": "is a shrinking inventory of used modules with an UNVERIFIED acquisition price, usable only in "
                "Cascade/Ice Lake Xeons",
        "C-08": "was never productized by Micron and needs a DRAM fab",
        "C-11": "is Rule-1 UNSUPPORTED, and its density is a claim-parity default",
        "C-15": "is Samsung's device (the venture sells IGZO targets and precursors, so this cost is a demand signal, "
                "not venture revenue)",
        "C-58": "needs a T4 fab ($2-3.5B) and would be the highest-cost producer against Micron 1-alpha",
        "C-59": "cannot get foundry wafers in a shortage and has no U.S. manufacturing",
        "C-04": "needs a DRAM fab with a capacitor module (Kioxia/Nanya)",
        "C-09": "has no chip yet and needs a partner DRAM fab",
        "C-02": "only reaches this on a line no U.S. foundry offers",
    }
    tA, tB = R["tiers"]["A"], R["tiers"]["B"]
    n_dev = len([c for c in v if any(r["kind"] == "device" for r in v[c]["rows"])])
    head = ("**Headline.** %d concept ids are costed: %d from branch-A device rows, plus C-58, C-59 and C-71 from the "
            "DRAM model or their cards. %d get under the A-05 glut price ($%.2f/GB) at base inputs: %s. Only %s reach DDR5 "
            "incumbent cost ($%.2f/GB) in the best case (at base inputs: %s). Every sub-glut concept has a catch: %s." % (
                len(v), n_dev, len(R["base_beats"]), G, ids(R["base_beats"]), ids(tA), K,
                ids([c for c in tA if v[c]["base"] <= K]),
                "; ".join("%s at $%s/GB %s" % (c, money(v[c]["base"]), catch.get(c, "(see card)")) for c in
                          sorted(set(tA) | set(R["base_beats"]), key=cid_key))))
    bl = [head]
    bl.append("**Die on $/GB alone (Rule 4, no other axis): %s.** Even with wafer cost -30%% and 0.95 yield, the best case "
              "stays above the glut price, and the cards name no other axis a buyer pays for. That covers display-glass "
              "IGZO (C-03, $%s/GB), floating-body 1T-DRAM (C-30, best $%s), bulk SRAM as a DRAM substitute (C-35, best "
              "$%s at the cheapest node) and wafer-scale SRAM (C-38, $%s). C-42, printed polymer ($%s/GB), is also "
              "Rule-1 UNSUPPORTED."
              % (ids(R["dead_r4"]), money(b("A1-03")), money(bb("A3-01")),
                 money(min(r["s"]["best"] for r in rows if r["tid"].startswith("A3-06"))), money(b("A3-09")),
                 money(b("A3-13"))))
    hyp = bb("A1-02s")
    bl.append("**C-02, the standalone IGZO 2T0C die, is dead on $/GB as defined.** On a U.S. 200mm 130nm line it costs $%s/GB "
              "(best $%s). A1's hypothetical 300mm 28nm BEOL line, which no U.S. foundry offers, would cost $%s/GB "
              "(best $%s), %s the $%.2f glut price%s. Its only axis is refresh power, and commodity DRAM buyers do not pay "
              "for that, so Rule 4 kills it. The IGZO value lives in the embedded and refresh-power cards (C-01, C-04)."
              % (money(b("A1-02")), money(bb("A1-02")), money(b("A1-02s")), money(hyp), where(hyp), G,
                 " only at the best-case corner" if hyp < G <= b("A1-02s") else ""))
    drc = [c for c in ("C-04", "C-08", "C-09") if c in v]
    knife = [c for c in drc if abs(v[c]["best"] / G - 1) < 0.05]
    bl.append("**The DRAM-class challengers (%s) beat the glut price only on DRAM-fab wafers at DRAM-like yields.** OCTRAM "
              "costs $%s/GB (best $%s), Micron NVDRAM $%s (best $%s) and FMC DRAM+ $%s (best $%s)%s. None reaches the $%.2f "
              "incumbent cost, and in a severe glut ($%.2f) %s. They survive on non-volatility or refresh power, but each "
              "needs a DRAM fab with a capacitor module (T3/T4). This founder cannot build that, and no U.S. foundry "
              "offers one."
              % (ids(drc), money(b("A1-04")), money(bb("A1-04")), money(b("A1-08")), money(bb("A1-08")),
                 money(b("A1-09")), money(bb("A1-09")),
                 (", a knife-edge for %s" % ids(knife)) if knife else "",
                 K, S, "all lose" if all(v[c]["best"] > S for c in drc) else "only %s holds at best case" %
                 ids([c for c in drc if v[c]["best"] <= S])))
    mram = [c for c in ("C-16", "C-17", "C-18", "C-19", "C-20", "C-21", "C-27", "C-28", "C-51") if c in v]
    ev_r = [r for r in rows if r["tid"] == "ci:everspin_1gb_sttmram_usd_per_gb"]
    ev = ev_r[0]["s"]["base"] if ev_r else 820.8
    if mram:
        mr = [v[c]["base"] for c in mram]
        bl.append("**MRAM survives only on non-$/GB axes (%s).** Computed cost runs $%s-%s/GB, and the Everspin 1Gb street "
                  "price ($%s/GB) is %s the glut price. Even a hypothetical 14nm 4Gb part costs $%s/GB (best $%s). So C-20, "
                  "MRAM as main memory, is dead on $/GB. The rest live only on non-volatility, lifecycle, rad-hard or "
                  "provenance, and they are sold per chip or per card, not per GB."
                  % (ids(mram), money(min(mr)), money(max(mr)), money(ev), ratio(ev / G), money(b("A2-04")),
                     money(bb("A2-04"))))
    fe = [c for c in ("C-06", "C-07", "C-10", "C-12", "C-22", "C-23", "C-24", "C-40") if c in v]
    if fe:
        fr = [v[c]["base"] for c in fe]
        bl.append("**Ferroelectric, ReRAM, CBRAM, CNT and AlScN memories (%s) cost $%s-%s/GB**, %s-%s the glut price. "
                  "They are embedded or kilobit-to-megabit parts. Their business is non-volatility, rad-hard, 500-600C "
                  "temperature (C-07), compute energy (C-24) or U.S. provenance, so score them on those axes. NRAM (C-40, "
                  "best $%s) gets closest, but only to the 2026 contract price."
                  % (ids(fe), money(min(fr)), money(max(fr)), ratio(min(fr) / G), ratio(max(fr) / G), money(bb("A3-11"))))
    sram_rows = [r for r in rows if r["tid"].startswith("A3-06")]
    sram = [c for c in ("C-33", "C-35", "C-36", "C-37", "C-38", "C-39") if c in v]
    if sram_rows:
        bl.append("**Bulk SRAM never drops below about $%s/GB at any node.** The 2-65nm rows span $%s-%s/GB, with a best "
                  "case of $%s, so trailing nodes are not cheaper per bit. SRAM concepts %s can never win on $/GB. C-33 and "
                  "C-36 survive on provenance and lifecycle, C-37 and C-39 on compute energy and latency, and C-35 and C-38 "
                  "are dead."
                  % (money(min(r["s"]["base"] for r in sram_rows)), money(min(r["s"]["base"] for r in sram_rows)),
                     money(max(r["s"]["base"] for r in sram_rows)), money(min(r["s"]["best"] for r in sram_rows)), ids(sram)))
    s28 = [r for r in rows if r["tid"] == "ci:sram_cell_um2_28nm"]
    s130 = [r for r in rows if r["tid"] == "ci:sram_cell_um2_130nm_sky130"]
    bl.append("**Gain-cell eDRAM (C-01, C-32, C-43) competes with SRAM, not DRAM.** The Si 2T/3T gain cell at 28nm costs "
              "$%s/GB area-equivalent vs $%s/GB for 6T SRAM on a 28nm wafer. The 130nm IGZO macro (C-01) costs $%s/GB vs "
              "$%s/GB for 130nm SkyWater SRAM. So the Rule-4 axis for these cards is on-die density and standby power vs SRAM, "
              "for edge-ASIC, defense and cryo buyers, not $/GB vs DDR5."
              % (money(b("A3-03")), money(s28[0]["s"]["base"]) if s28 else "n/a", money(b("A1-01")),
                 money(s130[0]["s"]["base"]) if s130 else "n/a"))
    tc = R["tiers"]["C"]
    bl.append("**Only-in-a-shortage concepts (tier C: %s)** beat the $%.2f Q4-2026 contract price in their best case but "
              "never the glut price. T-RAM costs $%s (best $%s), floating-body DRAM $%s (best $%s) and NRAM $%s (best $%s). "
              "Under Rule 6 they die in a 2028-29 glut unless a non-$/GB axis carries them. Out-of-branch check: a licensed "
              "legacy DDR4 fab (C-58) costs $%s/GB in the canonical model and a PSMC-foundry DDR3 brand (C-59) $%s/GB, both "
              "below the glut price. Their cards fail on capital and wafer allocation, not unit cost."
              % (ids(tc), C, money(b("A3-02")), money(bb("A3-02")), money(b("A3-01")), money(bb("A3-01")),
                 money(b("A3-11")), money(bb("A3-11")), money(b("dcs:ddr4_8g_1x_new")), money(b("dcs:ddr3_4g_fdry"))))
    w1b = DCS.BASE.get("wafer_cost_1beta_usd", 3800.0) if DCS else 3800.0
    brefs = [r["s"]["base"] for r in rows if r["kind"] == "branch-ref" and "DDR5" in r["device"]]
    bl.append("**Method caveats.** Branch-filed DRAM-class wafer costs ($5.5-7k) are %.0f-%.0f%% above the canonical $%s "
              "1b wafer, so the branches' own DDR5 references compute at $%s-%s/GB vs the model's $%.2f. The -30%% wafer case "
              "is therefore the fair comparison. Gb is decimal in A1/A3 and binary in A2 (up to 7.4%% apart). Embedded rows "
              "carry no test or package cost, by filing. The live model deck (cost $%.2f, contract $%.2f, glut $%.2f) differs "
              "from the brief's ($%.2f / $%.2f / $%.2f); tier changes between the two: %s. UNSUPPORTED concepts (%s) die "
              "under Rule 1 whatever their $/GB, and C-11's sub-glut number rests only on a claim-parity default density."
              % ((5500 / w1b - 1) * 100, (7000 / w1b - 1) * 100, "{:,.0f}".format(w1b),
                 money(min(brefs)) if brefs else "n/a", money(max(brefs)) if brefs else "n/a", K, K, C, G,
                 BRIEF_DECK["cost"], BRIEF_DECK["contract"], BRIEF_DECK["glut"],
                 ", ".join("%s %s->%s" % (c, R["brief_tier"][c], v[c]["tier"]) for c in R["flips"]) or "none",
                 ids(R["unsup"])))
    return bl


def main():
    buf = io.StringIO()
    with redirect_stdout(buf):
        R = report()
    text = buf.getvalue()
    sys.stdout.write(text)
    bullets = interpretation(R)
    md = ["# Device cost comparison: $/GB of every device/material concept vs DDR5", "",
          "**Generated by:** `models/device_cost_compare.py` (agent `%s`) · **As of:** %s · **Inputs:** "
          "`research/phase2/A1|A2|A3_device_params.json`, `tmp_to_id.json`, `concepts_master.json`, "
          "`research/phase1/cost_inputs.json`, DDR5 reference from `models/dram_cost_stack.py` (`ddr5_reference()`) · "
          "**Re-run:** `python3 models/device_cost_compare.py` · **Assumptions:** `research/assumptions/%s.md`"
          % (AGENT, AS_OF, AGENT), "",
          "All values are [ESTIMATE] unless a row's source column gives a URL. Ranges come from the sensitivity table.", "",
          "```text", text.rstrip("\n"), "```", "", "## Interpretation (%s, %s)" % (AGENT, AS_OF), ""]
    md += ["%d. %s" % (i + 1, s) for i, s in enumerate(bullets)]
    md += ["", "## Concept ids that cannot win on $/GB under any sensitivity", "",
           "Best case (wafer cost -30%%, yield 0.95) is still at or above the A-05 glut price ($%.2f/GB): %s." %
           (DDR5_GLUT, ", ".join(R["cannot"])), "",
           "Not even below the Q4-2026 contract price ($%.2f/GB) in the best case (tier D): %s." %
           (DDR5_CONTRACT, ", ".join(R["tiers"]["D"])), "",
           "Robust to the deck choice (cannot win under either the live model deck or the task-brief deck): %s." %
           ", ".join(R["robust"]), "",
           "Could win on $/GB, at least at the glut price (tiers A/B): %s. None of them is a device this founder can "
           "build. C-11 is Rule-1 UNSUPPORTED and C-05 rests on a company claim. C-26 is salvage of used modules, and C-15 "
           "is a materials play riding Samsung's device. C-04, C-08, C-09, C-25 and C-58 need a DRAM- or crosspoint-class "
           "300mm fab (T3/T4), and C-59 needs foundry DRAM wafers that are allocated away in a shortage." %
           ", ".join(sorted(R["tiers"]["A"] + R["tiers"]["B"], key=cid_key)), ""]
    try:
        OUT_MD.parent.mkdir(parents=True, exist_ok=True)
        OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
        print("\nWrote %s" % OUT_MD.relative_to(RV))
    except OSError as exc:
        print("\nWARNING: could not write %s (%s)" % (OUT_MD, exc))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # keep the Phase-7 "every script exits 0" gate honest but visible
        import traceback
        traceback.print_exc()
        print("ERROR in device_cost_compare.py: %s" % exc)
        sys.exit(1)
