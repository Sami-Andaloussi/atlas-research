"""FT-001 M3, first part: the panel, built in memory from the frozen sources (FT-001-M3-panel.md, sections 1-2, 5).

The panel is **not committed** (R28): it is rebuilt from the frozen files at every run; what is committed of it is
its coverage (``panel-coverage.csv``), its seams (``panel-seams.csv``) and its digest, written by ``breaks.py
build`` beside frame b's list. This module reads each source in M0's order (the twin's
``common.source_order``) and gives, per money:

- **π** — monthly π12 from IFS ``M..PCPI_IX`` then the BIS's long series (index, unit 628); annual π(y) from IFS
  ``A..PCPI_IX``, the World Bank's published rate ``FP.CPI.TOTL.ZG``, Reinhart and Rogoff's compiled column (R7),
  the BIS (annual index) and Jordà-Schularick-Taylor's ``cpi``. A change is read from the first source that reads
  **both ends** (R4); an IFS observation flagged ``B`` inside a change's span flags it (R5).
- **d** — 100(E_t/E_{t-12} - 1), E the money's units per unit of its anchor (R11), from IFS ``ENDE`` (monthly and
  end of year): the anchor of IRR's ``Master`` sheet for the class year (the date's year less one; 2015's
  carried after 2015; the dollar before 1946, for no code, for ``USD``/``SDR``/``Freely_falling``/``n.a.``, where
  the anchor's rate cannot be read at both ends, or where the anchor is the money's own currency). The United
  States: no d (R11). The euro: against the dollar.
- **the regime** (R12) and **the market split** (R13), at a date; **the common ends** (R6); **the timeline**
  frame b reads (R3); the seams, the coverage and the digest.

The default reader of R23 (``in_default``) serves frame c and the strata; frame b does not read it.

Run from the workshop's root: ``toolkit/bin/ftpy bank/maps/FT-001/missions/code/panel.py count`` prints the
coverage (counts and first and last periods), never a value.
"""

from __future__ import annotations

import csv
import glob
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import defaultdict
from functools import cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import economies  # noqa: E402
import xls  # noqa: E402
import xlsx  # noqa: E402
from breaks import Period, month_label  # noqa: E402

ROOT = HERE.parents[4]
DATA = ROOT / "data"
VINTAGE = "2026-09-30"
FIRST_YEAR = 1800
EURO_FIRST_MONTH = 1999 * 12

IFS_SPECIAL = {"SUH": "SUN", "CSH": "CSK", "YUC": "YUG", "DE2": "DDR", "1C_473": "YAR", "1C_459": "YMD",
               "AN": "ANT", "TW": "TWN", "AI": "AIA", "MS": "MSR", "U2": "EMU", "XM": "EMU"}
GROUPS = {"W0", "W00", "A10", "F6", "R1", "4F", "5I", "5O", "5W", "5X", "5Y", "7A"}
ANCHOR_AREA = {"GBP": "GB", "EUR": "U2", "DEM": "DE", "FRF": "FR", "JPY": "JP", "CHF": "CH", "AUD": "AU",
               "NZD": "NZ", "BEF": "BE", "NLG": "NL", "ITL": "IT", "ESP": "ES", "PTE": "PT", "INR": "IN",
               "EGP": "EG", "RUB": "RU", "ZAR": "ZA"}
PARITY = set(range(1, 11)) | {15}
FLOATING = {11, 12, 13}

LOCATOR = {
    "IFS-M": "dbnomics/IMF/IFS/M~~PCPI_IX (PCPI_IX, area {area})",
    "BIS-M": "bis/WS_LONG_CPI (FREQ M, UNIT_MEASURE 628, REF_AREA {area})",
    "IFS-A": "dbnomics/IMF/IFS/A~~PCPI_IX (PCPI_IX, area {area})",
    "World Bank": "worldbank/FP.CPI.TOTL.ZG ({area})",
    "Reinhart-Rogoff": "reinhart-rogoff/inflation ({area})",
    "BIS-A": "bis/WS_LONG_CPI (FREQ A, UNIT_MEASURE 628, REF_AREA {area})",
    "JST": "jst/macrohistory JSTdatasetR6.dta, cpi ({area})",
}

UNREAD_AREAS: dict[str, set[str]] = defaultdict(set)  # source -> areas left unread (groups or no code), for the manifest


# Frozen after the panel's vintage, for frame a's window (window_a.py W6): read at their own date, never re-dated.
LATER_VINTAGES = {f"{freq}~~{line}____XDC": "2026-10-01" for freq in "AM" for line in ("24", "25")}
#: Frame f's banks' lines (its F6), frozen on 2026-10-01: claims on central government and assets.
LATER_VINTAGES.update({f"A~~{code}": "2026-10-01" for code in ("FOSAG_XDC", "FOSAA_XDC", "FOSAF_XDC", "FOSAO_XDC",
                                                                  "22A___XDC", "20RA__XDC")})


def _v(path: Path) -> Path:
    return path / LATER_VINTAGES.get(path.name, VINTAGE)


# --- codes ---------------------------------------------------------------------------------------------------

@cache
def _iso2() -> dict[str, str]:
    entries = json.loads(economies.WB.read_text())[1]
    return {e["iso2Code"]: e["id"] for e in entries if e["region"]["id"] and e["region"]["value"].strip() != "Aggregates"}


def area_money(area: str, source: str = "") -> str | None:
    """A two-letter (or IFS special) area's money; None for a group or an area with no economy code."""
    if area in IFS_SPECIAL:
        return IFS_SPECIAL[area]
    if area == "1C_355":
        UNREAD_AREAS[source].add("1C_355 (Curacao and St Maarten: one series for two economies, not read)")
        return None
    if area in GROUPS or area.startswith(("XR", "XS", "1C_")):
        UNREAD_AREAS[source].add(f"{area} (a group)")
        return None
    money = _iso2().get(area)
    if money is None:
        UNREAD_AREAS[source].add(f"{area} (no economy code)")
    return money


# --- readers (each returns data keyed by money or area; nothing printed) ----------------------------------------

def _dbnomics(folder: str) -> dict[str, dict[str, tuple[float, bool]]]:
    """area -> period label -> (value, flagged B), from the frozen DBnomics pages of one IFS or WEO query."""
    out: dict[str, dict[str, tuple[float, bool]]] = {}
    for page in sorted(_v(DATA / "dbnomics" / "IMF" / folder).glob("page-*.json")):
        for doc in json.loads(page.read_text())["series"]["docs"]:
            dims = doc["dimensions"]
            area = dims.get("REF_AREA") or dims.get("weo-country")
            codes: list = []
            for item in doc.get("observations_attributes") or []:
                if item and item[0] == "OBS_STATUS":
                    codes = item[1] if len(item) == 2 and isinstance(item[1], list) else list(item[1:])
            if len(codes) != len(doc["period"]):
                codes = [""] * len(doc["period"])
            series = out.setdefault(area, {})
            for period, value, code in zip(doc["period"], doc["value"], codes):
                if value in ("NA", None):
                    continue
                series[period] = (float(value), code == "B")
    return out


def _by_month(series: dict[str, tuple[float, bool]]) -> dict[int, tuple[float, bool]]:
    out = {}
    for label, v in series.items():
        y, m = label.split("-")
        out[int(y) * 12 + int(m) - 1] = v
    return out


@cache
def ifs(code: str, freq: str) -> dict[str, dict[int, tuple[float, bool]]]:
    """IFS area -> period (month index, or year) -> (value, flagged B)."""
    raw = _dbnomics(f"IFS/{freq}~~{code}")
    if freq == "M":
        return {a: _by_month(s) for a, s in raw.items()}
    return {a: {int(p): v for p, v in s.items()} for a, s in raw.items()}


@cache
def bis() -> dict[str, dict[str, dict[int, float]]]:
    """BIS area -> 'M' (month index) or 'A' (year) -> index level (unit 628 only)."""
    out: dict[str, dict[str, dict[int, float]]] = {}
    zpath = _v(DATA / "bis" / "WS_LONG_CPI") / "WS_LONG_CPI_csv_flat.zip"
    with zipfile.ZipFile(zpath) as z:
        with z.open(z.namelist()[0]) as handle:
            reader = csv.reader(io.TextIOWrapper(handle, encoding="utf-8-sig"))
            head = next(reader)
            col = {h.split(":")[0]: i for i, h in enumerate(head)}
            for row in reader:
                if not row[col["UNIT_MEASURE"]].startswith("628"):
                    continue
                if row[col["OBS_STATUS"]].startswith("M") or not row[col["OBS_VALUE"]].strip():
                    continue
                area = row[col["REF_AREA"]].split(":")[0].strip()
                freq = row[col["FREQ"]].split(":")[0].strip()
                period = row[col["TIME_PERIOD"]].strip()
                key = int(period[:4]) * 12 + int(period[5:7]) - 1 if freq == "M" else int(period)
                out.setdefault(area, {}).setdefault(freq, {})[key] = float(row[col["OBS_VALUE"]])
    return out


@cache
def worldbank(indicator: str) -> dict[str, dict[int, float]]:
    """ISO3 (economies, and the euro area's EMU) -> year -> value."""
    body = json.loads((_v(DATA / "worldbank" / indicator) / "page-001.json").read_text())
    keep = set(_iso2().values()) | {"EMU"}
    out: dict[str, dict[int, float]] = {}
    for r in body[1]:
        code = r.get("countryiso3code")
        if code in keep and r.get("value") is not None:
            out.setdefault(code, {})[int(r["date"])] = float(r["value"])
    return out


@cache
def rr_inflation() -> dict[str, dict[int, tuple[float, str]]]:
    """ISO3 -> year -> (inflation, locator), Reinhart and Rogoff's compiled column (R7)."""
    out: dict[str, dict[int, tuple[float, str]]] = {}
    for path in sorted(glob.glob(str(DATA / "reinhart-rogoff" / "inflation-*" / VINTAGE / "*.xls"))):
        for sheet in xls.sheets(path):
            if sheet in ("Contents", "Sheet1", "Sheet2", "Sheet3"):
                continue
            money = economies.code(sheet)
            cells = xls.cells(path, sheet)
            years = {r: int(v) for (r, c), v in cells.items()
                     if c == 0 and isinstance(v, float) and 1000 <= v <= 2100 and v == int(v)}
            first = min(years)
            head = max(r for (r, c), v in cells.items() if isinstance(v, str) and c > 0 and r < first)
            labels = {c: v.strip() for (r, c), v in cells.items() if r == head and isinstance(v, str) and v.strip()}
            rr = [c for c, lab in labels.items() if "reinhart" in lab.lower()]
            columns = rr[:1] if rr else sorted(labels, reverse=True)
            name = Path(path).name
            series = out.setdefault(money, {})
            for r, year in years.items():
                for c in columns:
                    v = cells.get((r, c))
                    if isinstance(v, float):
                        tag = "" if rr else "; rr_no_compiled_column"
                        series[year] = (v, f"{name}, sheet {sheet}, column '{labels[c]}', {year}{tag}")
                        break
    return out


@cache
def rr_basis() -> dict[str, list[tuple[int, int, str]]]:
    """ISO3 -> (first year, last year, series) of each line of a sheet's "Based on" block: the prices Reinhart and
    Rogoff's compiled column rests on (a description written on frame b's lines, never a rule)."""
    out: dict[str, list[tuple[int, int, str]]] = {}
    for path in sorted(glob.glob(str(DATA / "reinhart-rogoff" / "inflation-*" / VINTAGE / "*.xls"))):
        for sheet in xls.sheets(path):
            if sheet in ("Contents", "Sheet1", "Sheet2", "Sheet3"):
                continue
            cells = xls.cells(path, sheet)
            spans = []
            for (r, c), v in cells.items():
                if c == 0 and isinstance(v, str) and re.fullmatch(r"\s*\d{4}\s*-\s*\d{4}\s*", v):
                    a, b = (int(x) for x in re.findall(r"\d{4}", v))
                    label = cells.get((r, 2))
                    spans.append((a, b, str(label).strip() if label else ""))
            out[economies.code(sheet)] = sorted(spans)
    return out


def rr_names_cpi(money: str, year: int) -> bool:
    """True when a line of the sheet's "Based on" block covering the year names a consumer price index."""
    labels = [lab.lower() for lo, hi, lab in rr_basis().get(money, []) if lo <= year <= hi]
    return any("cpi" in lab or "consumer" in lab for lab in labels)


def _is_cpi(label: str) -> bool:
    return "cpi" in label.lower() or "consumer" in label.lower()


def rr_basis_kind(spans: list[tuple[int, int, str]], year: int) -> str:
    """The audit's M4 (second build), a flag from the "Based on" block, never a rule: '' when every line covering
    the year names a consumer price index; "non-CPI basis" when none does; "mixed basis (CPI and non-CPI lines
    cover the year)" when both do — which one the compiled value follows is not said; "basis not stated for the
    year" when no line covers it."""
    labels = [lab for lo, hi, lab in spans if lo <= year <= hi]
    if not labels:
        return "basis not stated for the year"
    cpi = [_is_cpi(lab) for lab in labels]
    return "" if all(cpi) else "non-CPI basis" if not any(cpi) else "mixed basis (CPI and non-CPI lines cover the year)"


def rr_basis_seam(spans: list[tuple[int, int, str]], year: int) -> str:
    """A seam inside Reinhart and Rogoff's compiled column: the lines covering the year differ from those
    covering the year before (the year's rate may compare two bases); '' otherwise."""
    now = sorted({lab for lo, hi, lab in spans if lo <= year <= hi})
    before = sorted({lab for lo, hi, lab in spans if lo <= year - 1 <= hi})
    if now == before:
        return ""
    return f"{year - 1}: {' / '.join(before) or 'not stated'} -> {year}: {' / '.join(now) or 'not stated'}"


@cache
def jst() -> dict[str, dict[int, float]]:
    import pandas as pd
    frame = pd.read_stata(_v(DATA / "jst" / "macrohistory") / "JSTdatasetR6.dta", columns=["iso", "year", "cpi"])
    out: dict[str, dict[int, float]] = {}
    for iso, year, cpi in frame.itertuples(index=False):
        if cpi == cpi and cpi is not None:
            out.setdefault(str(iso), {})[int(year)] = float(cpi)
    return out


# --- IRR: the regime (R12), the anchor (R11), the market split (R13) ---------------------------------------------

IRR = DATA / "irr"


@cache
def irr_classes() -> dict[str, dict]:
    """ISO3 -> {'start', 'end', 'classes': {year: value}} from the sheet Fine."""
    path = _v(IRR / "classification-annual-1946-2016") / "IRR_Classification_Annual_1946-2016.xlsx"
    rows = xlsx.rows(path, "Fine")
    label_row = {str(r[1]).strip(): i for i, r in enumerate(rows[:8]) if len(r) > 1 and isinstance(r[1], str)}
    start_row, end_row, name_row = rows[label_row["Start"]], rows[label_row["End"]], label_row["Country"]
    year_rows = {i: int(r[1]) for i, r in enumerate(rows) if len(r) > 1 and isinstance(r[1], float)
                 and 1900 <= r[1] <= 2100}
    out: dict[str, dict] = {}
    width = max(len(r) for r in rows[name_row:name_row + 2])
    for j in range(2, width):
        parts = [rows[i][j] for i in (name_row, name_row + 1) if j < len(rows[i]) and isinstance(rows[i][j], str)]
        name = " ".join(p.strip() for p in parts if p.strip())
        if not name:
            continue
        money = economies.code(name)
        if money is None:
            continue
        if money in out:
            raise ValueError(f"IRR Fine: {money} held twice")

        def num(row, j=j):
            v = row[j] if j < len(row) else None
            return int(v) if isinstance(v, float) else None
        out[money] = {"start": num(start_row), "end": num(end_row),
                      "classes": {y: rows[i][j] if j < len(rows[i]) else None for i, y in year_rows.items()}}
    return out


def class_at(record: dict | None, date_year: int) -> tuple[int | None, str]:
    """The fine class 12 months before a date in ``date_year`` (R12): (class, note)."""
    if record is None:
        return None, "no IRR column"
    cy = date_year - 1
    if cy < 1946:
        return None, "class year before 1946: frame a's lists (M4), not coded"
    carried = cy > 2016
    y = min(cy, 2016)
    while y >= 1946:
        if record["start"] is None or record["end"] is None or not record["start"] <= y <= record["end"]:
            return None, "outside the country's start and end years"
        v = record["classes"].get(y)
        if not isinstance(v, float) or v != int(v) or not 1 <= v <= 15:
            return None, "the class cannot be read"
        if int(v) == 14:
            y -= 1
            continue
        return int(v), ("regime_carried (2016's class)" if carried else "")
    return None, "class 14 with no class before it"


def regime_group(cls: int | None) -> str:
    if cls is None:
        return "cannot be read"
    return "parity" if cls in PARITY else "floating"


def _iso3_columns(rows: list, label: str) -> tuple[int, dict[int, str]]:
    for i, r in enumerate(rows[:10]):
        for j, v in enumerate(r):
            if isinstance(v, str) and v.strip() == label:
                return i, {k: str(x).strip() for k, x in enumerate(r) if k > j and isinstance(x, str) and
                           re.fullmatch(r"[A-Z]{3}", str(x).strip())}
    raise ValueError(f"no row labelled {label!r}")


@cache
def irr_anchors() -> dict[str, dict[int, str]]:
    path = _v(IRR / "anchor-currency-annual-1946-2016") / "IRR_Anchor_Currency_Annual_1946-2016.xlsx"
    rows = xlsx.rows(path, "Master")
    head, cols = _iso3_columns(rows, "ISO3 Code")
    out: dict[str, dict[int, str]] = {}
    for r in rows[head + 1:]:
        if r and isinstance(r[0], float) and 1900 <= r[0] <= 2100:
            for j, code in cols.items():
                v = r[j] if j < len(r) else None
                if isinstance(v, str) and v.strip():
                    out.setdefault(code, {})[int(r[0])] = v.strip()
    return out


@cache
def irr_split() -> tuple[dict[str, dict[int, float | None]], dict[str, dict[int, float | None]]]:
    """(annual, monthly): ISO3 -> year or month index -> 1.0, 0.0, or None ("n.a.")."""
    path = _v(IRR / "unified-market-annual-1946-2016") / "IRR_Unified_Market_Annual_1946-2016.xlsx"
    rows = xlsx.rows(path, "Unified")
    head, cols = _iso3_columns(rows, "ISO3 Code")
    annual: dict[str, dict[int, float | None]] = {}
    for r in rows[head + 1:]:
        if r and isinstance(r[0], float) and 1900 <= r[0] <= 2100:
            for j, code in cols.items():
                v = r[j] if j < len(r) else None
                annual.setdefault(code, {})[int(r[0])] = v if isinstance(v, float) else None
    rows = xlsx.rows(path, "Master")
    head, cols = _iso3_columns(rows, "ISO3 Code")
    monthly: dict[str, dict[int, float | None]] = {}
    for r in rows[head + 1:]:
        label = r[2] if len(r) > 2 else None
        m = re.fullmatch(r"(\d{4})M(\d{1,2})", str(label).strip()) if isinstance(label, str) else None
        if not m:
            continue
        t = int(m.group(1)) * 12 + int(m.group(2)) - 1
        for j, code in cols.items():
            v = r[j] if j < len(r) else None
            monthly.setdefault(code, {})[t] = v if isinstance(v, float) else None
    return annual, monthly


def split_at(money: str, label: str) -> str:
    """'recorded', 'not recorded', 'no parity' or 'cannot be read' at a date (R13)."""
    year = int(label[:4])
    cls, _ = class_at(irr_classes().get(money), year)
    if cls is None:
        return "cannot be read"
    if cls not in PARITY:
        return "no parity"
    if cls == 15:
        return "recorded"
    annual, monthly = irr_split()
    v = monthly.get(money, {}).get(int(label[:4]) * 12 + int(label[5:7]) - 1) if "-" in label \
        else annual.get(money, {}).get(year)
    if v is None:
        return "cannot be read"
    return "recorded" if v == 1 else "not recorded"


# --- the monies and their readings -------------------------------------------------------------------------------

class Panel:
    """Every reading frame b needs, per money, built once from the frozen files."""

    def __init__(self) -> None:
        self.ifs_pi_m, self.ifs_pi_a = ifs("PCPI_IX", "M"), ifs("PCPI_IX", "A")
        self.ende_m, self.ende_a = ifs("ENDE_XDC_USD_RATE", "M"), ifs("ENDE_XDC_USD_RATE", "A")
        self.bis, self.wb, self.rr, self.jst = bis(), worldbank("FP.CPI.TOTL.ZG"), rr_inflation(), jst()
        self.ifs_area: dict[str, str] = {}
        self.bis_area: dict[str, str] = {}
        for source, areas, target in (("IFS", set(self.ifs_pi_m) | set(self.ifs_pi_a) | set(self.ende_m) |
                                       set(self.ende_a), self.ifs_area), ("BIS", set(self.bis), self.bis_area)):
            for area in sorted(areas):
                money = area_money(area, source)
                if money is None:
                    continue
                if money in target and target[money] != area:
                    raise ValueError(f"{source}: {money} held by {target[money]} and {area}")
                target[money] = area
        self.monies = sorted(m for m in set(self.ifs_area) | set(self.bis_area) | set(self.wb) | set(self.rr) |
                             set(self.jst) if m in economies.known_codes())
        self.self_anchored: set[str] = set()

    # π ------------------------------------------------------------------------------------------------------
    def pi_monthly(self, money: str) -> dict[int, tuple[float, str, bool]]:
        ifs_l = self.ifs_pi_m.get(self.ifs_area.get(money, ""), {})
        bis_l = self.bis.get(self.bis_area.get(money, ""), {}).get("M", {})
        first = EURO_FIRST_MONTH if money == "EMU" else FIRST_YEAR * 12
        out = {}
        for t in sorted(set(ifs_l) | set(bis_l)):
            if t < first:
                continue
            if t in ifs_l and t - 12 in ifs_l and ifs_l[t][0] > 0 and ifs_l[t - 12][0] > 0:
                flag = any(ifs_l.get(k, (0, False))[1] for k in range(t - 11, t + 1))
                out[t] = (100 * (ifs_l[t][0] / ifs_l[t - 12][0] - 1), "IFS-M", flag)
            elif t in bis_l and t - 12 in bis_l and bis_l[t] > 0 and bis_l[t - 12] > 0:
                out[t] = (100 * (bis_l[t] / bis_l[t - 12] - 1), "BIS-M", False)
        return out

    def pi_annual(self, money: str, rr_cpi_only: bool = False) -> dict[int, tuple[float, str, bool]]:
        """π(y) in M0's order. ``rr_cpi_only`` (the variant ``rr-cpi-only``, added by the session after the
        headline's counts were seen): a Reinhart-Rogoff year whose "Based on" block names no consumer price
        index is not read."""
        ifs_l = self.ifs_pi_a.get(self.ifs_area.get(money, ""), {})
        wb = self.wb.get(money, {})
        rr = self.rr.get(money, {})
        if rr_cpi_only:
            rr = {y: v for y, v in rr.items() if rr_names_cpi(money, y)}
        bis_l = self.bis.get(self.bis_area.get(money, ""), {}).get("A", {})
        jst_l = self.jst.get(money, {})
        first = 1999 if money == "EMU" else FIRST_YEAR
        out = {}
        for y in sorted(set(ifs_l) | set(wb) | set(rr) | set(bis_l) | set(jst_l)):
            if y < first:
                continue
            if y in ifs_l and y - 1 in ifs_l and ifs_l[y][0] > 0 and ifs_l[y - 1][0] > 0:
                out[y] = (100 * (ifs_l[y][0] / ifs_l[y - 1][0] - 1), "IFS-A", ifs_l[y][1])
            elif y in wb:
                out[y] = (wb[y], "World Bank", False)
            elif y in rr:
                out[y] = (rr[y][0], "Reinhart-Rogoff", False)
            elif y in bis_l and y - 1 in bis_l and bis_l[y] > 0 and bis_l[y - 1] > 0:
                out[y] = (100 * (bis_l[y] / bis_l[y - 1] - 1), "BIS-A", False)
            elif y in jst_l and y - 1 in jst_l and jst_l[y] > 0 and jst_l[y - 1] > 0:
                out[y] = (100 * (jst_l[y] / jst_l[y - 1] - 1), "JST", False)
        return out

    def locator(self, money: str, source: str) -> str:
        area = {"IFS-M": self.ifs_area, "IFS-A": self.ifs_area, "BIS-M": self.bis_area,
                "BIS-A": self.bis_area}.get(source, {}).get(money, money)
        return LOCATOR[source].format(area=area)

    # d ------------------------------------------------------------------------------------------------------
    def _anchor(self, money: str, date_year: int) -> tuple[str, str | None]:
        cy = date_year - 1
        if cy < 1946 or money == "EMU":
            return "USD", None
        code = irr_anchors().get(money, {}).get(min(cy, 2015), "")
        area = ANCHOR_AREA.get(code)
        if area is not None and area == self.ifs_area.get(money):
            self.self_anchored.add(money)
            return "USD", None
        return (code, area) if area else ("USD", None)

    def _d(self, money: str, table: dict, step: int, year_of) -> dict[int, tuple[float, bool, str]]:
        if money == "USA":
            return {}
        own = table.get(self.ifs_area.get(money, ""), {})
        first = EURO_FIRST_MONTH if money == "EMU" and step == 12 else (1999 if money == "EMU" else -1)
        out = {}
        for t in sorted(own):
            if t < first or t - step not in own or own[t][0] <= 0 or own[t - step][0] <= 0:
                continue
            code, area = self._anchor(money, year_of(t))
            a_now = a_then = 1.0
            flag = own[t][1] if step == 1 else any(own.get(k, (0, False))[1] for k in range(t - 11, t + 1))
            if area is not None:
                anchor = table.get(area, {})
                if t in anchor and t - step in anchor and anchor[t][0] > 0 and anchor[t - step][0] > 0:
                    a_now, a_then = anchor[t][0], anchor[t - step][0]
                    flag = flag or (anchor[t][1] if step == 1 else
                                    any(anchor.get(k, (0, False))[1] for k in range(t - 11, t + 1)))
                else:
                    code = "USD (anchor's rate unreadable)"
            out[t] = (100 * ((own[t][0] / a_now) / (own[t - step][0] / a_then) - 1), flag, code)
        return out

    def d_monthly(self, money: str) -> dict[int, tuple[float, bool, str]]:
        return self._d(money, self.ende_m, 12, lambda t: t // 12)

    def d_annual(self, money: str) -> dict[int, tuple[float, bool, str]]:
        return self._d(money, self.ende_a, 1, lambda y: y)

    # the common ends (R6) -----------------------------------------------------------------------------------
    def have_monthly(self) -> dict[int, set[str]]:
        have: dict[int, set[str]] = defaultdict(set)
        for money in self.monies:
            first = EURO_FIRST_MONTH if money == "EMU" else 0
            for table in (self.ifs_pi_m.get(self.ifs_area.get(money, ""), {}),
                          self.bis.get(self.bis_area.get(money, ""), {}).get("M", {})):
                for t in table:
                    if t >= first:
                        have[t].add(money)
        return have

    def have_annual(self) -> dict[int, set[str]]:
        have: dict[int, set[str]] = defaultdict(set)
        for money in self.monies:
            first = 1999 if money == "EMU" else 0
            for table in (self.ifs_pi_a.get(self.ifs_area.get(money, ""), {}), self.wb.get(money, {}),
                          self.rr.get(money, {}), self.bis.get(self.bis_area.get(money, ""), {}).get("A", {}),
                          self.jst.get(money, {})):
                for y in table:
                    if y >= first:
                        have[y].add(money)
        return have


def common_end(have: dict[int, set[str]], step: int, share: float = 0.5) -> int | None:
    """The last period in which at least ``share`` of the monies that had a reading ``step`` periods earlier
    still have one (M0 section 1; R6)."""
    last = None
    if not have:
        return None
    for t in range(min(have), max(have) + 1):
        before = have.get(t - step, set())
        if before and len(before & have.get(t, set())) >= share * len(before):
            last = t
    return last


def seams(readings: dict[int, str]) -> list[tuple[int, str, str]]:
    """(period, old source, new source) wherever a reading's source differs from the reading before it."""
    out, previous = [], None
    for t in sorted(readings):
        if previous is not None and readings[t] != previous:
            out.append((t, previous, readings[t]))
        previous = readings[t]
    return out


def timeline(money: str, pm: dict, pa: dict, dm: dict, da: dict, end_m: int, end_a: int) -> list[Period]:
    """The periods frame b reads (R3): years before the monthly span, months inside it (a calendar year with no
    readable month read as a year), years after it; nothing past the common ends. Before and after the span the
    months of the edge years outside it are not read: the year before the span's first month, then its months."""
    first_year = 1999 if money == "EMU" else FIRST_YEAR
    months = sorted(t for t in pm if t <= end_m)

    def year(y: int) -> Period:
        pi = pa.get(y)
        d = da.get(y)
        rise = d[0] - da[y - 1][0] if d and (y - 1) in da else None
        return Period(str(y), "A", y * 12, 12, pi[0] if pi else None, pi[1] if pi else "", pi[2] if pi else False,
                      d[0] if d else None, rise, d[1] if d else False, d[2] if d else "")

    def month(t: int) -> Period:
        pi = pm.get(t)
        d = dm.get(t)
        rise = d[0] - dm[t - 12][0] if d and (t - 12) in dm else None
        return Period(month_label(t), "M", t, 1, pi[0] if pi else None, pi[1] if pi else "", pi[2] if pi else False,
                      d[0] if d else None, rise, d[1] if d else False, d[2] if d else "")

    if not months:
        return [year(y) for y in range(first_year, end_a + 1)]
    s, e = months[0], months[-1]
    out = [year(y) for y in range(first_year, s // 12)]
    readable = set(months)
    for y in range(s // 12, e // 12 + 1):
        inside = range(max(s, y * 12), min(e, y * 12 + 11) + 1)
        if not any(t in readable for t in inside):
            out.append(year(y))
        else:
            out.extend(month(t) for t in inside)
    out.extend(year(y) for y in range(e // 12 + 1, end_a + 1))
    return out


# --- R23: the state in default at a date (frame c and the strata; not read by frame b) ------------------------

@cache
def default_stocks() -> dict[str, dict[int, float | None]]:
    """ISO3 -> year -> the stock of the state's debt in default (BoC-BoE 2025, DEBT_TOTAL_2025), None if empty."""
    path = _v(DATA / "bankofcanada" / "sovereign-defaults") / "BoC-BoE-Database-2025.xlsx"
    table = xlsx.rows(path, "Debt_2025")
    head = next(i for i, r in enumerate(table) if r and "DEBT_COUNTRY" in r and "DEBT_YEAR" in r)
    labels = table[head]
    ci, yi, ti = labels.index("DEBT_COUNTRY"), labels.index("DEBT_YEAR"), labels.index("DEBT_TOTAL_2025")
    out: dict[str, dict[int, float | None]] = {}
    for r in table[head + 1:]:
        if len(r) <= yi or not isinstance(r[ci], str) or not isinstance(r[yi], float):
            continue
        money = economies.code(r[ci])
        if money is None:
            continue
        v = r[ti] if len(r) > ti and isinstance(r[ti], float) else None
        out.setdefault(money, {})[int(r[yi])] = v
    return out


def in_default(stocks: dict[int, float | None] | None, before_1960: dict[int, tuple] | None, year: int,
               m_to_s: bool = False) -> str:
    """'yes', 'no' or 'cannot be read' (R23). ``before_1960`` maps a year to (domestic, external) dummies (either
    None if unread); for the M-S economies only the external dummy exists and a 0 cannot be read."""
    if year >= 1960:
        if stocks is None or year not in stocks or stocks[year] is None:
            return "cannot be read"
        return "yes" if stocks[year] > 0 else "no"
    if before_1960 is None or year not in before_1960:
        return "cannot be read"
    domestic, external = before_1960[year]
    if domestic == 1 or external == 1:
        return "yes"
    if m_to_s:
        return "cannot be read"
    if domestic == 0 and external == 0:
        return "no"
    return "cannot be read"


# --- coverage, seams, digest ------------------------------------------------------------------------------------

def records(panel: Panel) -> tuple[list[dict], list[dict], str]:
    """(coverage rows, seam rows, digest) over every money's π and d readings."""
    coverage, seam_rows = [], []
    digest = hashlib.sha256()
    for money in panel.monies:
        items = {"pi monthly": panel.pi_monthly(money), "pi annual": panel.pi_annual(money),
                 "d monthly": {t: (v, "IFS ENDE", f) for t, (v, f, _) in panel.d_monthly(money).items()},
                 "d annual": {t: (v, "IFS ENDE", f) for t, (v, f, _) in panel.d_annual(money).items()}}
        for item, readings in items.items():
            fmt = month_label if "monthly" in item else str
            by_source: dict[str, list[int]] = defaultdict(list)
            for t, (v, source, _) in sorted(readings.items()):
                by_source[source].append(t)
                digest.update(f"{money}|{item}|{t}|{v:.10g}|{source}\n".encode())
            for source, ts in by_source.items():
                coverage.append({"money": money, "item": item, "source": source, "first": fmt(ts[0]),
                                 "last": fmt(ts[-1]), "readings": len(ts)})
            for t, old, new in seams({t: r[1] for t, r in readings.items()}):
                seam_rows.append({"money": money, "item": item, "period": fmt(t), "from": old, "to": new})
    return coverage, seam_rows, digest.hexdigest()


def count() -> None:
    panel = Panel()
    ends = common_end(panel.have_monthly(), 12), common_end(panel.have_annual(), 1)
    print("monies:", len(panel.monies), "| common end, monthly:", month_label(ends[0]), "| annual:", ends[1])
    coverage, seam_rows, digest = records(panel)
    tally: dict[tuple[str, str], int] = defaultdict(int)
    for row in coverage:
        tally[(row["item"], row["source"])] += 1
    for (item, source), n in sorted(tally.items()):
        print(f"{item}\t{source}\t{n} monies")
    print("seams:", len(seam_rows), "| digest:", digest)
    print("areas not read:", {k: sorted(v) for k, v in UNREAD_AREAS.items()})


if __name__ == "__main__":
    if sys.argv[1:2] == ["count"]:
        count()
    else:
        print(__doc__)
        sys.exit(2)


# === Frame c's readers (FT-001-M3-panel.md, section 4; written, and tested on synthetic series, before any real
# series was read for frame c). Each returns money -> year -> reading; nothing printed. =========================

WEO_ISO = {"UVK": "XKX", "WBG": "PSE"}
WEO_LAST_YEAR = 2024          # R8: 2025-2030 are the April 2025 vintage's projections
HPDD_LAST_YEAR = 2015
C3_FIRST_YEAR = 1948
UNITS_FACTOR, UNITS_CEILING = 100.0, 3.0   # R10: the pilot's panel rule 6, its 0.1% floor not used


def _dbnomics_mult(folder: str) -> dict[str, float]:
    """area -> the multiplier its series name ends with (IFS: "Millions")."""
    from ft.data import dbnomics
    out = {}
    for page in sorted(_v(DATA / "dbnomics" / "IMF" / folder).glob("page-*.json")):
        for doc in json.loads(page.read_text())["series"]["docs"]:
            out[doc["dimensions"]["REF_AREA"]] = dbnomics.multiplier(doc.get("series_name", "")) or 1.0
    return out


@cache
def ifs_levels(code: str) -> dict[str, dict[int, float]]:
    """IFS annual series by money, times its multiplier (end-of-year stocks, or the year's flow)."""
    raw, mult = ifs(code, "A"), _dbnomics_mult(f"IFS/A~~{code}")
    out: dict[str, dict[int, float]] = {}
    for area, series in raw.items():
        money = area_money(area, f"IFS {code}")
        if money:
            out[money] = {y: v * mult.get(area, 1.0) for y, (v, _) in series.items()}
    return out


@cache
def hpdd() -> dict[str, dict[int, float]]:
    out: dict[str, dict[int, float]] = {}
    for area, series in _dbnomics("HPDD/A~~GGXWDG_GDP").items():
        money = area_money(area, "HPDD")
        if money:
            out[money] = {int(p): v for p, (v, _) in series.items() if int(p) <= HPDD_LAST_YEAR}
    return out


@cache
def weo(subject: str) -> dict[str, dict[int, float]]:
    """The WEO's April 2025 vintage (``GGXWDG_NGDP`` or ``GGXCNL_NGDP``, % of GDP), years to 2024 only (R8)."""
    known = economies.known_codes()
    out: dict[str, dict[int, float]] = {}
    for iso, series in _dbnomics(f"WEO_2025-04/~{subject}~pcent_gdp").items():
        money = WEO_ISO.get(iso, iso)
        if money in known:
            out[money] = {int(p): v for p, (v, _) in series.items() if int(p) <= WEO_LAST_YEAR}
        else:
            UNREAD_AREAS["WEO"].add(f"{iso} (no economy code)")
    return out


def rr_debt_columns(labels: dict[int, str]) -> list[int]:
    """R8: the columns of a sheet's debt ratio, preferred kind first — "Total (domestic plus external)", "gross
    central government", "debt/GDP"; else the same with general government ("gross government", "gross central
    (federal) government"); never debt/exports or gross external debt. ``labels``: column -> its header labels
    joined, lower-case."""
    def ok(text: str, kinds: tuple[str, ...]) -> bool:
        return ("total (domestic plus external)" in text and "debt/gdp" in text and "debt/exports" not in text
                and "gross external" not in text and any(k in text for k in kinds))
    central = [c for c, t in sorted(labels.items()) if ok(t, ("gross central government",))]
    if central:
        return central
    return [c for c, t in sorted(labels.items())
            if ok(t, ("gross general government", "gross government", "gross central (federal) government"))]


@cache
def rr_debt() -> dict[str, dict[int, tuple[float, str]]]:
    """ISO3 -> year -> (debt/GDP, locator): per year the leftmost preferred column that reads it (R8)."""
    out: dict[str, dict[int, tuple[float, str]]] = {}
    for path in sorted(glob.glob(str(DATA / "reinhart-rogoff" / "debt-to-gdp-*" / VINTAGE / "*.xls"))):
        for sheet in xls.sheets(path):
            if sheet in ("Contents", "Sheet1", "Sheet2", "Sheet3"):
                continue
            cells = xls.cells(path, sheet)
            years = {r: int(v) for (r, c), v in cells.items()
                     if c == 0 and isinstance(v, float) and 1000 <= v <= 2100 and v == int(v)}
            if not years:
                continue
            first = min(years)
            numeric_cols = sorted({c for (r, c), v in cells.items() if c > 0 and r >= first and isinstance(v, float)})
            labels = {c: " / ".join(cells[(r, c)].strip() for r in range(first - 4, first)
                                    if isinstance(cells.get((r, c)), str) and cells[(r, c)].strip()).lower()
                      for c in numeric_cols}
            cols = rr_debt_columns(labels)
            money = economies.code(sheet)
            series = out.setdefault(money, {})
            for r, year in years.items():
                for c in cols:
                    v = cells.get((r, c))
                    if isinstance(v, float):
                        series[year] = (v, f"{Path(path).name}, sheet {sheet}, column '{labels[c]}', {year}")
                        break
    return out


@cache
def rr_debt_monies() -> frozenset[str]:
    """Reinhart and Rogoff's seventy (the frozen debt files' sheets): R29's fitting sample."""
    out = set()
    for path in sorted(glob.glob(str(DATA / "reinhart-rogoff" / "debt-to-gdp-*" / VINTAGE / "*.xls"))):
        out |= {economies.code(s) for s in xls.sheets(path) if s not in ("Contents", "Sheet1", "Sheet2", "Sheet3")}
    return frozenset(out)


@cache
def jst_fiscal() -> dict[str, dict[int, dict[str, float]]]:
    import pandas as pd
    frame = pd.read_stata(_v(DATA / "jst" / "macrohistory") / "JSTdatasetR6.dta",
                          columns=["iso", "year", "debtgdp", "revenue", "expenditure", "gdp"])
    out: dict[str, dict[int, dict[str, float]]] = {}
    for row in frame.itertuples(index=False):
        values = {k: float(getattr(row, k)) for k in ("debtgdp", "revenue", "expenditure", "gdp")
                  if getattr(row, k) == getattr(row, k)}
        out.setdefault(str(row.iso), {})[int(row.year)] = values
    return out


def first_in_order(year: int, sources: list[tuple[str, dict]]) -> tuple[float, str] | None:
    """The first source in order that reads the year: (value, source name)."""
    for name, table in sources:
        v = table.get(year)
        if v is not None:
            return (v[0] if isinstance(v, tuple) else v), name
    return None


def debt_readings(money: str) -> dict[int, tuple[float, str]]:
    """Debt/GDP per year, M0's order: the HPDD mirror (to 2015), the WEO (1980-2024), R-R, JST."""
    # JST's debtgdp is a ratio, read x 100 (its aggregate median over every economy-year, 0.45, seen before
    # this line was written: a reading after data, said in the manifest)
    jst_d = {y: 100 * v["debtgdp"] for y, v in jst_fiscal().get(money, {}).items() if "debtgdp" in v}
    sources = [("HPDD", hpdd().get(money, {})), ("WEO", weo("GGXWDG_NGDP").get(money, {})),
               ("Reinhart-Rogoff", rr_debt().get(money, {})), ("JST", jst_d)]
    years = set().union(*(t for _, t in sources))
    return {y: r for y in sorted(years) if y >= FIRST_YEAR and (r := first_in_order(y, sources))}


def deficit_readings(money: str) -> dict[int, tuple[float, str]]:
    """Deficit/GDP per year (the negative of net lending): the WEO (1980-2024), then JST (central government)."""
    weo_d = {y: -v for y, v in weo("GGXCNL_NGDP").get(money, {}).items()}
    jst_d = {y: 100 * (v["expenditure"] - v["revenue"]) / v["gdp"] for y, v in jst_fiscal().get(money, {}).items()
             if {"expenditure", "revenue", "gdp"} <= set(v) and v["gdp"] > 0}
    sources = [("WEO", weo_d), ("JST", jst_d)]
    years = set().union(*(t for _, t in sources))
    return {y: r for y in sorted(years) if y >= FIRST_YEAR and (r := first_in_order(y, sources))}


def credit_change(l12a: dict[int, float], fasag: dict[int, float], year: int) -> tuple[float, str] | None:
    """R9: the year's change in central-bank claims on the state, within one line: 12A to 2000, FASAG from 2002;
    2001 on 12A where it reads 2000 and 2001 (flagged), else unreadable."""
    if year <= 2000 or year == 2001:
        if year in l12a and year - 1 in l12a:
            return l12a[year] - l12a[year - 1], ("12A (2001: seam_12A_FASAG)" if year == 2001 else "12A")
        return None
    if year in fasag and year - 1 in fasag:
        return fasag[year] - fasag[year - 1], "FASAG"
    return None


def credit_level(l12a: dict[int, float], fasag: dict[int, float], year: int) -> float | None:
    return l12a.get(year) if year <= 2000 else fasag.get(year)


def units_ok(ratios: dict[int, float]) -> bool:
    """R10: False when credit over GDP moves by a factor of 100 or more between consecutive years, or its median
    exceeds 300%."""
    xs = [ratios[y] for y in sorted(ratios)]
    if not xs:
        return True
    ordered = sorted(xs)
    median = ordered[len(ordered) // 2] if len(ordered) % 2 else (ordered[len(ordered) // 2 - 1] + ordered[len(ordered) // 2]) / 2
    if median > UNITS_CEILING:
        return False
    years = sorted(ratios)
    for a, b in zip(years, years[1:]):
        if b != a + 1:
            continue
        lo, hi = sorted((abs(ratios[a]), abs(ratios[b])))
        if lo > 0 and hi / lo >= UNITS_FACTOR:
            return False
    return True


def c3_measure(dcredit: float, gdp: float, deficit_pct: float) -> float | None:
    """s = 100 x [change in credit / GDP, in %] / [deficit / GDP, in %]; None where the deficit is not positive."""
    if gdp <= 0 or deficit_pct <= 0:
        return None
    return 100 * (100 * dcredit / gdp) / deficit_pct


def c3_readings(money: str, deficits: dict[int, tuple[float, str]]) -> tuple[dict[int, tuple[float, str]], str]:
    """(year -> (s, source), the units check's verdict) for route c3, from 1948. The units check (R10) runs on
    each credit line alone — 12A over the years it serves (to 2001), FASAG over its own (from 2001) — since two
    lines are never compared (R4); a line that fails leaves c3 unreadable over its years. *Added after the first
    build was seen*: that build ran the check across the 2000-2001 seam and on the two lines together."""
    l12a, fasag = ifs_levels("12A___XDC").get(money, {}), ifs_levels("FASAG_XDC").get(money, {})
    ngdp = ifs_levels("NGDP_XDC").get(money, {})
    wbgdp = worldbank("NY.GDP.MKTP.CN").get(money, {})

    def gdp(y: int) -> tuple[float, str] | None:
        return (ngdp[y], "IFS NGDP") if y in ngdp else ((wbgdp[y], "WB GDP") if y in wbgdp else None)

    def ratios(line: dict[int, float], years) -> dict[int, float]:
        out = {}
        for y in years:
            g = gdp(y)
            if y in line and g and g[0] > 0:
                out[y] = line[y] / g[0]
        return out
    ok = {"12A": units_ok(ratios(l12a, [y for y in l12a if y <= 2001])),
          "FASAG": units_ok(ratios(fasag, [y for y in fasag if y >= 2001]))}
    verdict = "yes" if all(ok.values()) else "no: " + " and ".join(k for k, v in ok.items() if not v) + \
        " fails the units check (R10), c3 cannot be read over its years"
    out = {}
    for y, (deficit, dsource) in deficits.items():
        if y < C3_FIRST_YEAR or not ok["12A" if y <= 2001 else "FASAG"]:
            continue
        ch, g = credit_change(l12a, fasag, y), gdp(y)
        if ch is None or g is None:
            continue
        s_ = c3_measure(ch[0], g[0], deficit)
        if s_ is not None:
            out[y] = (s_, f"IFS {ch[1]} / {g[1]} / {dsource} deficit")
        else:
            out[y] = (float("nan"), f"deficit not positive ({dsource})")
    return out, verdict


# --- route c4: the pilot's C15 (read, never edited) --------------------------------------------------------------

C15_RUN = ROOT / "studies" / "FT-001-part-2-where-printed-money-goes" / "results" / "runs" / "C15-e-episodes-closed.json"
C15_COMMIT = "fccce91"


def c15_check(expected_hash: str) -> list[str]:
    """What is wrong with the run file M0 names: its card hash, and any change since its commit."""
    import subprocess
    body = json.loads(C15_RUN.read_text())
    found = []
    if body.get("card_hash") != expected_hash:
        found.append("C15's card_hash is not M0's")
    rel = C15_RUN.relative_to(ROOT).as_posix()
    if subprocess.run(["git", "diff", "--quiet", C15_COMMIT, "--", rel], cwd=ROOT).returncode != 0:
        found.append(f"C15's run file changed since {C15_COMMIT}")
    return found


def c4_by_year(episodes: list[dict], first_year: int = 1950) -> dict[str, dict[int, dict]]:
    """money -> year -> the year's first episode crossing c (R19: its measure is rise_pct_gdp), from 1950; only
    episodes not set apart (``apart_080`` empty)."""
    out: dict[str, dict[int, dict]] = {}
    for e in sorted(episodes, key=lambda e: e["c"]):
        if e.get("apart_080", "").strip():
            continue
        year = int(e["c"][:4])
        if year < first_year:
            continue
        money = area_money(e["area"], "C15")
        if money is None:
            continue
        flagged = e.get("flag", "").strip() == "likely reclassification, unread" or (
            e["area"] == "CI" and e.get("seam_in_window") == "True" and "2001-10" <= e["c"] <= "2002-12")
        out.setdefault(money, {}).setdefault(year, {
            "c": e["c"], "measure": float(e["rise_pct_gdp"]), "flag": flagged,
            "seam_in_window": e.get("seam_in_window") == "True"})
    return out


@cache
def c15_lists() -> dict[str, list[dict]]:
    body = json.loads(C15_RUN.read_text())
    return {name: list(csv.DictReader(io.StringIO(body["result"]["lists"][name]))) for name in ("headline", "smoothing")}


# --- R23 before 1960, and the default per creditor class (the acts list's second build, c4a56ad) --------------

@cache
def default_classes() -> dict[str, dict[int, dict[str, str]]]:
    """ISO3 -> year -> {'class': 'yes'/'no'/'cannot be read', 'total': the same by DEBT_TOTAL_2025 > 0}, from 1960,
    as the acts list's builds read the Bank of Canada-Bank of England database: a class left blank in a year whose
    total is read holds no stock; a year whose total is blank cannot be read; the stock the total carries and no
    class holds (TOTAL less the ten classes, above the rounding of the eleven figures) is an eleventh class,
    ``UNASSIGNED`` (acts.py's third build); the USSR to 1991 on SUN, the Russian Federation from 1992 on RUS; in
    default when any class holds a stock."""
    import acts
    table = xlsx.rows(acts.BOC, "Debt_2025")
    head = next(i for i, r in enumerate(table) if r and "DEBT_COUNTRY" in r and "DEBT_YEAR" in r)
    labels = table[head]
    ci, yi = labels.index("DEBT_COUNTRY"), labels.index("DEBT_YEAR")
    cols = {c: labels.index(f"DEBT_{c}_2025") for c in (*acts.BOC_CLASSES, "TOTAL")}
    out: dict[str, dict[int, dict[str, str]]] = {}
    for r in table[head + 1:]:
        if len(r) <= yi or not isinstance(r[ci], str) or not isinstance(r[yi], float):
            continue
        money = economies.code(r[ci])
        if money is None:
            continue
        year = int(r[yi])
        if money == "RUS" and year <= 1991:
            money = "SUN"
        cells = {c: (r[i] if len(r) > i and isinstance(r[i], float) else None) for c, i in cols.items()}
        out.setdefault(money, {})[year] = in_default_by_class(cells, acts.BOC_CLASSES, acts.ROUNDING)
    return out


def in_default_by_class(cells: dict[str, float | None], classes: tuple[str, ...], rounding: float) -> dict[str, str]:
    total = cells.get("TOTAL")
    if total is None:
        return {"class": "cannot be read", "total": "cannot be read"}
    filled = {c: (cells.get(c) or 0.0) for c in classes}
    unassigned = round(total - sum(filled.values()), 3)
    held = any(v > 0 for v in filled.values()) or unassigned > rounding
    return {"class": "yes" if held else "no", "total": "yes" if total > 0 else "no"}


@cache
def default_before_1960() -> tuple[dict[str, dict[int, tuple]], frozenset[str]]:
    """(ISO3 -> year -> (domestic, external) dummies, the M-S economies), read as the acts list reads them: the
    two columns of *Varieties*; TTID's external dummies for the M-S economies (their domestic cannot be read)."""
    import acts
    out: dict[str, dict[int, tuple]] = {}
    for path in acts.VARIETIES:
        for sheet in xlsx.sheets(path):
            if sheet in ("Contents", "CrisisDefinitions", "CrisisDefinition", "Sheet1", "Sheet2", "Sheet3"):
                continue
            money = economies.code(sheet)
            table = xlsx.rows(path, sheet)
            head = next(i for i, r in enumerate(table[:25]) if "domestic" in [str(c).strip().lower() for c in r]
                        and "external" in [str(c).strip().lower() for c in r])
            lab = [str(c).strip().lower() for c in table[head]]
            di, ei = lab.index("domestic"), lab.index("external")
            for r in table[head + 1:]:
                if r and isinstance(r[0], float):
                    d = r[di] if len(r) > di and isinstance(r[di], float) else None
                    e = r[ei] if len(r) > ei and isinstance(r[ei], float) else None
                    out.setdefault(money, {})[int(r[0])] = (d, e)
    table = xlsx.rows(acts.TTID[0], "ExternalDefaultDummys")
    years = {i: int(v) for i, v in enumerate(table[1]) if isinstance(v, float)}
    for r in table[4:]:
        if len(r) < 2 or not isinstance(r[1], str) or not r[1].strip():
            continue
        money = economies.code(r[1])
        if money in acts.M_TO_S:
            out[money] = {y: (None, r[i] if i < len(r) and isinstance(r[i], float) else None) for i, y in years.items()}
    return out, frozenset(acts.M_TO_S)


def default_at(money: str, year: int, ms_variant: bool = False, total: bool = False) -> str:
    """R23 at an annual date; ``total``: the first build's reading (DEBT_TOTAL_2025 > 0), for the manifest's count."""
    if money == "EMU":
        return "cannot be read"
    if year >= 1960:
        return default_classes().get(money, {}).get(year, {}).get("total" if total else "class", "cannot be read")
    early, m_to_s = default_before_1960()
    return in_default(None, early.get(money), year, m_to_s=(money in m_to_s and not ms_variant))


# --- war (R14): M4's war.py, the one reader of M0's war year (committed 7871641) ------------------------------
# The first build of frame c read war years with a reader of its own here (R14); M4's war.py, committed the same
# day, is the workshop's one foyer for M0 section 1's war year, so frame c reads it (its readings W1-W10). Said in
# the manifest: a change made after the first build was seen.

def war_at(money: str, year: int, after_cow: str = "cannot be read", ucdp: bool = True) -> str:
    """'yes', 'no' or 'cannot be read' (M0 section 1, through war.war_year). ``ucdp`` is W12's switch (FT-001-M3-panel.md
    section 9; frame k's protocol section 15): True, the default, reads test (b) after COW's coverage through UCDP/PRIO
    v26.1; False runs W9 alone, the reading before W12 (the variant ``war-before-w12`` of frames c and k)."""
    import war
    v = war.war_year(money, year, after_cow=after_cow, ucdp=ucdp)
    return "yes" if v.startswith("yes") else v


#: ``war-moves.csv`` (frames c and k, the variant ``war-before-w12``): the lines whose war reading W12 moved.
WAR_MOVES_FIELDS = ["money", "year", "field", "before", "after", "status_before", "status_after"]


def war_moves(headline: list[dict], before: list[dict], fields: tuple[str, ...]) -> list[dict]:
    """The moves of W12 (panel protocol section 9; frame k's section 15): one row per line and per war field in
    ``fields`` whose reading differs between the headline's lines (``after``, W12 applied) and the variant
    ``war-before-w12``'s (``before``, W9 alone), in the headline's order, with the line's status on each side. A line is
    keyed by (money, entry_date). The two lists must hold the same lines (W12 never dates an entry): a line in one only is
    a slip of the build, and it raises."""
    key = lambda r: (r["money"], r["entry_date"])
    old = {key(r): r for r in before}
    if len(old) != len(before) or set(old) != {key(r) for r in headline}:
        raise ValueError("war_moves: the headline and the war-before-w12 variant do not hold the same lines")
    out = []
    for h in headline:
        b = old[key(h)]
        for f in fields:
            if b[f] != h[f]:
                out.append({"money": h["money"], "year": h["entry_date"], "field": f, "before": b[f], "after": h[f],
                            "status_before": b["status"], "status_after": h["status"]})
    return out


def write_war_moves(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=WAR_MOVES_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


# --- the supports' "stands" (R24) --------------------------------------------------------------------------------

@cache
def garriga() -> dict[str, dict[int, dict[str, float]]]:
    out: dict[str, dict[int, dict[str, float]]] = {}
    with open(_v(DATA / "garriga" / "cbi") / "Replication_ISQ_2025.tab", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            r = {k: (r.get(k) or "").strip().strip('"') for k in ("year", "cname", "ISO", "lvau_garriga", "cuk_limlen")}
            money = _iso2().get(r["ISO"])
            if money is None:
                try:
                    money = economies.code(r["cname"])
                except KeyError:
                    UNREAD_AREAS["Garriga"].add(r["cname"])
                    continue
            if money is None:
                continue
            vals = {}
            for k in ("lvau_garriga", "cuk_limlen"):
                try:
                    vals[k] = float(r[k])
                except ValueError:
                    pass
            out.setdefault(money, {})[int(float(r["year"]))] = vals
    return out


CHINN_ITO_ISO = {"ZAR": "COD", "TMP": "TLS"}  # the old ISO3 codes of Zaire and East Timor


@cache
def ka_open() -> dict[str, dict[int, float]]:
    import pandas as pd
    frame = pd.read_stata(_v(DATA / "chinn-ito" / "kaopen") / "kaopen_2023.dta", columns=["ccode", "year", "ka_open"])
    known = economies.known_codes()
    out: dict[str, dict[int, float]] = {}
    for code, year, v in frame.itertuples(index=False):
        code = CHINN_ITO_ISO.get(str(code), code)
        if v == v and str(code) in known:
            out.setdefault(str(code), {})[int(year)] = float(v)
        elif str(code) not in known:
            UNREAD_AREAS["Chinn-Ito"].add(str(code))
    return out


def supports(default: str, cap: float | None, cls: int | None, index: float | None, kaopen: float | None,
             cap_line: float = 0.5, index_line: float = 0.5, ka_line: float = 0.25) -> dict[str, str]:
    """The four counted supports' readings at entry and the counts (R24)."""
    def yn(cond):
        return "yes" if cond else "no"
    taken_back = {"no": "yes", "yes": "no"}.get(default, "cannot be read")
    peg = None if cls is None else cls in PARITY
    if cap is not None and cap >= cap_line:
        by_rule = "yes"
    elif peg:
        by_rule = "yes"
    elif cap is not None and peg is False:
        by_rule = "no"
    else:
        by_rule = "cannot be read"
    cap_only = "cannot be read" if cap is None else yn(cap >= cap_line)
    if index is not None and index >= index_line:
        institution = "yes"
    else:
        institution = "cannot be read"   # below 0.5, or unread: "a target announced" is frame a's list (M4)
    force = "cannot be read" if kaopen is None else yn(kaopen <= ka_line)

    def count(items):
        yes = sum(v == "yes" for v in items)
        unknown = sum(v == "cannot be read" for v in items)
        if yes >= 2:
            return "two or more"
        if yes + unknown <= 1:
            return "one or none"
        return "cannot be read"
    return {"taken_back": taken_back, "limit_by_rule": by_rule, "limit_by_rule_cap_only": cap_only,
            "limit_by_institution": institution, "force": force,
            "supports_count": count([taken_back, by_rule, institution, force]),
            "supports_count_without_pegs": count([taken_back, cap_only, institution, force]),
            "supports_count_without_taken_back": count([by_rule, institution, force])}


# --- M3's source anomalies (the audit; frame b's second build): listed, never swapped -------------------------

def year_anomalies(pi_a: float, months: dict[int, float], months_before: dict[int, float]) -> list[str]:
    """Screens chosen after the audit named AZE 1992, MMR 1973 and DEU 1924 (so after data), for one money-year:
    ``pi_a`` the year's annual π(y) from IFS-A; ``months`` / ``months_before`` IFS-M's index levels by month
    number (1-12) in the year and the year before. (ii) IFS-M's year-average change differs from IFS-A's by
    more than 20 points and by more than half the larger in size (both years complete); (iii) IFS-A falls while
    IFS-M's index rises by more than 20% from the year's first to its last month read."""
    out = []
    if len(months) == 12 and len(months_before) == 12:
        avg = 100 * (sum(months.values()) / sum(months_before.values()) - 1)
        if abs(avg - pi_a) > 20 and abs(avg - pi_a) > 0.5 * max(abs(avg), abs(pi_a)):
            out.append(f"IFS-A {pi_a:.1f} against IFS-M's year average {avg:.1f}")
    if len(months) >= 2 and pi_a < 0:
        first, last = months[min(months)], months[max(months)]
        if first > 0 and 100 * (last / first - 1) > 20:
            out.append(f"IFS-A {pi_a:.1f} while IFS-M's index rises {100 * (last / first - 1):.0f}% inside the year")
    return out


def source_anomalies(pan: "Panel") -> list[dict]:
    """(i) every π(y) at or below -50% in any annual source as read; (ii)-(iii) ``year_anomalies`` on IFS."""
    rows = []
    for money in pan.monies:
        for y, (v, src, _) in sorted(pan.pi_annual(money).items()):
            if v <= -50:
                rows.append({"money": money, "period": str(y), "source": src,
                             "anomaly": f"pi(y) {v:.1f}: at or below -50%"})
        area = pan.ifs_area.get(money, "")
        ann, mon = pan.ifs_pi_a.get(area, {}), pan.ifs_pi_m.get(area, {})
        for y in sorted(ann):
            if y - 1 not in ann or ann[y][0] <= 0 or ann[y - 1][0] <= 0:
                continue
            pi_a = 100 * (ann[y][0] / ann[y - 1][0] - 1)
            months = {t % 12 + 1: v for t, (v, _) in mon.items() if t // 12 == y and v > 0}
            before = {t % 12 + 1: v for t, (v, _) in mon.items() if t // 12 == y - 1 and v > 0}
            for text in year_anomalies(pi_a, months, before):
                rows.append({"money": money, "period": str(y), "source": "IFS-A / IFS-M", "anomaly": text})
    return rows


# --- "Convertible at entry" before 1971 from frame a's panels 1 and 2 (the protocol's section 8, O4) ------------

FRAME_A = DATA / "reconstructed" / "ft001-a"


def gold_adoption_year(reason: str) -> int | None:
    """Panel 1: the adoption year in ``members.csv``'s reason — the last year of Meissner's (a later year
    "stands for the adoption", as frame a reads Argentina's 1863, 1883, 1903); else a span "from YYYY to" (the
    United Kingdom's 1821, from Bordo and Kydland, quoted there); else None."""
    m = re.search(r"Meissner (\d{4}(?:(?:, | & )\d{4})*)", reason)
    if m:
        return int(re.findall(r"\d{4}", m.group(1))[-1])
    m = re.search(r"from (\d{4}) to \d{4}", reason)
    return int(m.group(1)) if m else None


def gold_return_year(reason: str) -> int | None:
    """Panel 2: the return to gold in ``members.csv``'s reason ("return 1925-04 on or before ...", or a span
    "return August 1926-June 1928 ..." read at its later date, as frame a reads it)."""
    m = re.search(r"return (.+?) on or before", reason)
    if not m:
        return None
    years = re.findall(r"\d{4}", m.group(1))
    return int(years[-1]) if years else None


BJ_KINDS = (("bj_suspension", "suspension"), ("bj_exchange_control", "exchange control"),
            ("bj_devaluation", "devaluation"))


def panel2_end(lines: list[dict]) -> tuple[int | None, str]:
    """A panel 2 member's end of convertibility (the M4 protocol's section 13, "for frame c's convertible"):
    the **first of Bernanke and James's three dates** (suspension, exchange control, devaluation), read from
    the ``bj_*`` columns of the member's ``a2`` and ``a2-var-bj-note7`` lines — never from the headline exit
    alone, which since frame a's second build is the first of suspension and devaluation only. Returns (the
    year, the kinds dated in that year joined by '+'), or (None, '') when no date is given."""
    dates: dict[str, str] = {}
    for r in lines:
        for col, kind in BJ_KINDS:
            d = (r.get(col) or "").strip()
            if d and (kind not in dates or d < dates[kind]):
                dates[kind] = d
    if not dates:
        return None, ""
    year = int(min(dates.values())[:4])
    return year, "+".join(kind for _, kind in BJ_KINDS if kind in dates and int(dates[kind][:4]) == year)


@cache
def frame_a_gold() -> dict[str, dict[str, tuple]]:
    """{'1': money -> (adoption year, change year or None, act), '2': money -> (return year, end year or None,
    kinds ended that year)} for the members frame a codes "yes" in panels 1 and 2 (``members.csv``): panel 1's
    change from its ``a1`` line (any status); panel 2's end from ``panel2_end`` over its ``a2`` and
    ``a2-var-bj-note7`` lines. Only these two files of ``ft001-a`` are read."""
    with open(FRAME_A / "members.csv", newline="") as f:
        members = [r for r in csv.DictReader(f) if r["panel"] in ("1", "2") and r["member"] == "yes"]
    a1: dict[str, tuple] = {}
    a2: dict[str, list[dict]] = defaultdict(list)
    with open(FRAME_A / "series.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["route"] == "a1":
                a1.setdefault(r["money"], (int(r["entry_date"][:4]), r["act"]))
            elif r["route"] in ("a2", "a2-var-bj-note7"):
                a2[r["money"]].append(r)
    out: dict[str, dict[str, tuple]] = {"1": {}, "2": {}}
    for r in members:
        if r["panel"] == "1":
            start = gold_adoption_year(r["reason"])
            end, act = a1.get(r["code"], (None, ""))
        else:
            start = gold_return_year(r["reason"])
            end, act = panel2_end(a2.get(r["code"], []))
        if start is not None:
            out[r["panel"]][r["code"]] = (start, end, act)
    return out
