"""FT-001 M3, second part: the acts list, ``data/reconstructed/ft001-acts/`` (FT-001-M3-acts.md).

The scripted acts — T2 from the Bank of Canada–Bank of England database (from 1960) and Reinhart and
Rogoff (to 1959), L1 and L3 from Garriga — are coded here, identically for every economy each source holds;
the hand-coded acts (L2, H1, a target abandoned) come from the coders' settled file and are merged as given.
Only the columns the protocol names are read: *Varieties*' two sovereign-default columns, never its
currency, inflation, stock-market or banking columns; Garriga's ``cuk_limlen``, ``reform``, ``decrease`` and
``lvau_garriga``, never her inflation or other controls.

Run from the workshop's root with the toolkit's interpreter::

    toolkit/.venv/bin/python bank/maps/FT-001/missions/code/acts.py count
    toolkit/.venv/bin/python bank/maps/FT-001/missions/code/acts.py build --hand <settled.csv>

``count`` prints how many acts each source gives (no value); ``build`` writes ``series.csv`` and
``coverage.csv`` after :func:`m0.require_locked`.
"""

from __future__ import annotations

import csv
import glob
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import economies  # noqa: E402
import m0  # noqa: E402
import xlsx  # noqa: E402

ROOT = HERE.parents[4]
DATA = ROOT / "data"
OUT = DATA / "reconstructed" / "ft001-acts"
CODER = "script: missions/code/acts.py"
VINTAGE = "2026-09-30"

BOC = DATA / "bankofcanada" / "sovereign-defaults" / VINTAGE / "BoC-BoE-Database-2025.xlsx"
BOC_SOURCE = ("Bank of Canada-Bank of England Sovereign Default Database, 2025 edition "
              f"(bankofcanada/sovereign-defaults {VINTAGE})")
VARIETIES = sorted(glob.glob(str(DATA / "reinhart-rogoff" / "varieties-*" / VINTAGE / "*.xlsx")))
VAR_SOURCE = "Reinhart and Rogoff, Varieties of crises, country sheets (reinhart-rogoff/varieties-{A-E,F-M,T-Z} " \
             f"{VINTAGE})"
TTID = sorted(glob.glob(str(DATA / "reinhart-rogoff" / "ttid-default-tables" / VINTAGE / "Table_6.[24]*.xlsx")))
TTID_SOURCE = ("Reinhart and Rogoff, This Time Is Different, external default dummies "
               f"(reinhart-rogoff/ttid-default-tables {VINTAGE}, sheet ExternalDefaultDummys)")
GARRIGA = DATA / "garriga" / "cbi" / VINTAGE / "Replication_ISQ_2025.tab"
GARRIGA_SOURCE = f"Garriga (2025), central bank independence data (garriga/cbi {VINTAGE}, Replication_ISQ_2025.tab)"

#: The twenty economies whose Varieties file ("M-S") is not served (FT-001-M3-sources.md, "Not found").
M_TO_S = {"MMR", "NLD", "NZL", "NIC", "NGA", "NOR", "PAN", "PRY", "PER", "PHL", "POL", "PRT", "ROU", "RUS", "SGP",
          "ZAF", "ESP", "LKA", "SWE", "CHE"}
LAST_RR_YEAR = 1959
FIRST_BOC_YEAR = 1960

SERIES_FIELDS = ["period", "value", "unit", "source", "locator", "note", "uncertainty", "money", "frame", "route",
                 "support", "headline", "entry_date", "entry_measure", "entry_measure_date", "outcome",
                 "outcome_date", "onset_date", "responses", "exit", "status", "coder", "rules_sha256"]
COVERAGE_FIELDS = ["money", "act", "source", "first_year", "last_year", "note"]
SUPPORT = {"T2": "taken back", "L1": "a limit by rule", "L2": "a limit by rule", "L3": "a limit by institution",
           "H1": "habit", "R1": "redemption"}


def line(money: str, route: str, date: str, value, unit: str, source: str, locator: str, *, note: str = "",
         uncertainty: str = "", headline: bool = True, status: str = "counted", coder: str = CODER) -> dict:
    headline = headline and status == "counted"
    return {"period": date, "value": value, "unit": unit, "source": source, "locator": locator, "note": note,
            "uncertainty": uncertainty, "money": money, "frame": "acts", "route": route,
            "support": SUPPORT[route.split("-")[0]], "headline": "yes" if headline else "no", "entry_date": date,
            "entry_measure": "", "entry_measure_date": "", "outcome": "", "outcome_date": "", "onset_date": "",
            "responses": "", "exit": "", "status": status, "coder": coder}


def _runs(years: dict[int, float | None]) -> list[tuple[int, bool]]:
    """The first year of each run of 1s, and whether the year before it was read (not empty)."""
    starts = []
    for year in sorted(years):
        if years[year] == 1 and years.get(year - 1) != 1:
            starts.append((year, (year - 1) in years and years[year - 1] is not None))
    return starts


# --- T2 to 1959: Reinhart and Rogoff ------------------------------------------------------------------

def _varieties() -> tuple[list[dict], list[dict]]:
    rows, cover = [], []
    for path in VARIETIES:
        for sheet in xlsx.sheets(path):
            if sheet in ("Contents", "CrisisDefinitions", "CrisisDefinition", "Sheet1", "Sheet2", "Sheet3"):
                continue
            money = economies.code(sheet)
            table = xlsx.rows(path, sheet)
            head = next((i for i, r in enumerate(table[:25])
                         if "domestic" in [str(c).strip().lower() for c in r]
                         and "external" in [str(c).strip().lower() for c in r]), None)
            if head is None:
                raise ValueError(f"{sheet}: no 'domestic' and 'external' columns found")
            labels = [str(c).strip().lower() for c in table[head]]
            cols = {"domestic": labels.index("domestic"), "external": labels.index("external")}
            series = {k: {} for k in cols}
            for r in table[head + 1:]:
                if not r or not isinstance(r[0], float):
                    continue
                year = int(r[0])
                for k, c in cols.items():
                    series[k][year] = r[c] if len(r) > c else None
            for kind, years in series.items():
                read = [y for y, v in years.items() if v is not None]
                if read:
                    cover.append({"money": money, "act": f"T2 {kind}", "source": VAR_SOURCE,
                                  "first_year": min(read), "last_year": min(max(read), LAST_RR_YEAR),
                                  "note": f"used to {LAST_RR_YEAR}; the Bank of Canada-Bank of England database from "
                                          f"{FIRST_BOC_YEAR}"})
                for year, before_read in _runs(years):
                    if year > LAST_RR_YEAR:
                        continue
                    first = year == min(read)
                    rows.append(line(money, "T2", str(year), 1, "dummy", VAR_SOURCE,
                                     f"{Path(path).name}, sheet {sheet}, sovereign debt crises - {kind}, {year}",
                                     note=f"{kind} default; first year of a run of 1s"
                                          + ("; the series' first year: the default may have begun before it"
                                             if first else ""),
                                     status="apart" if first else "counted"))
    return _dedupe(rows), cover


def _ttid() -> tuple[list[dict], list[dict]]:
    panels = []
    for path in TTID:
        table = xlsx.rows(path, "ExternalDefaultDummys")
        years = {i: int(v) for i, v in enumerate(table[1]) if isinstance(v, float)}
        panel = {}
        for r in table[4:]:
            if len(r) < 2 or not isinstance(r[1], str) or not r[1].strip():
                continue
            money = economies.code(r[1])
            if money is None or money not in M_TO_S:
                continue
            panel[money] = (r[1].strip(), {y: (r[i] if i < len(r) else None) for i, y in years.items()})
        panels.append((Path(path).name, panel))
    (name_a, a), (name_b, b) = panels
    if {k: v[1] for k, v in a.items()} != {k: v[1] for k, v in b.items()}:
        raise ValueError(f"{name_a} and {name_b} disagree on the M-S economies' dummies: settle by hand")
    rows, cover = [], []
    for money, (printed, years) in sorted(a.items()):
        read = [y for y, v in years.items() if v is not None]
        if read:
            cover.append({"money": money, "act": "T2 external", "source": TTID_SOURCE, "first_year": min(read),
                          "last_year": min(max(read), LAST_RR_YEAR),
                          "note": "the M-S economies only (their Varieties file is not served); domestic defaults "
                                  "cannot be read before 1960"})
        for year, _ in _runs(years):
            if year > LAST_RR_YEAR:
                continue
            first = year == min(read)
            rows.append(line(money, "T2", str(year), 1, "dummy", TTID_SOURCE,
                             f"{name_a}, sheet ExternalDefaultDummys, {printed}, {year}",
                             note="external default; first year of a run of 1s"
                                  + ("; the series' first year: the default may have begun before it" if first else ""),
                             status="apart" if first else "counted"))
    return rows, cover


def _dedupe(rows: list[dict]) -> list[dict]:
    """A domestic and an external default beginning the same year are one act, both named."""
    seen: dict[tuple, dict] = {}
    for r in rows:
        key = (r["money"], r["route"], r["period"])
        if key in seen:
            seen[key]["note"] += " | also " + r["note"]
            seen[key]["locator"] += " | " + r["locator"]
            if r["status"] == "counted":
                seen[key]["status"] = "counted"
        else:
            seen[key] = dict(r)
    return list(seen.values())


# --- T2 from 1960: the Bank of Canada-Bank of England database ------------------------------------------

#: The database's creditor classes (FT-001-M3-acts.md, 3d, O1): "the first year of a stock" is read in each.
BOC_CLASSES = ("IMF", "IBRD", "IDA", "IADB", "PARIS_CLUB", "CHINA", "OTHER_OFFICIAL_CREDITORS", "PRIVATE_CREDITORS",
               "LC_DEBT", "FISCAL_ARREARS")
PRIVATE = ("PRIVATE_CREDITORS", "LC_DEBT")
#: The stock the total carries and no class holds (the small check's F1): TOTAL less the classes' sum, when
#: positive. Read as an eleventh class, so a default the database leaves unassigned (Argentina 2001) is dated.
#: A remainder within the rounding of the eleven figures, each printed to US$0.01m (11 x 0.005), is none.
UNASSIGNED = "UNASSIGNED"
ROUNDING = 11 * 0.005
CLASSES = (*BOC_CLASSES, UNASSIGNED)


def _boc() -> tuple[list[dict], list[dict]]:
    """T2 from 1960, per creditor class; the first build's total-stock reading kept as the variant T2-var-total.

    *Reading*: a class left blank in a year whose total is read holds no stock (the database leaves blank
    what it does not hold); a year whose total is blank cannot be read. The Soviet Union's years to 1991
    are coded on ``SUN``, the Russian Federation's from 1992 on ``RUS``: one line of the database, read as one
    series (1992 is compared with 1991)."""
    table = xlsx.rows(BOC, "Debt_2025")
    head = next(i for i, r in enumerate(table) if r and "DEBT_COUNTRY" in r and "DEBT_YEAR" in r)
    labels = table[head]
    ci, yi = labels.index("DEBT_COUNTRY"), labels.index("DEBT_YEAR")
    cols = {c: labels.index(f"DEBT_{c}_2025") for c in (*BOC_CLASSES, "TOTAL")}
    data: dict[str, dict[int, dict[str, float | None]]] = {}
    for r in table[head + 1:]:
        if len(r) <= yi or not isinstance(r[ci], str) or not isinstance(r[yi], float):
            continue
        year = int(r[yi])
        if economies.code(r[ci]) is None:
            continue
        cells = {c: (r[i] if len(r) > i and isinstance(r[i], float) else None) for c, i in cols.items()}
        if cells["TOTAL"] is not None:
            cells = {c: (0.0 if v is None else v) for c, v in cells.items()}
            rest = round(cells["TOTAL"] - sum(cells[c] for c in BOC_CLASSES), 3)
            cells[UNASSIGNED] = rest if rest > ROUNDING else 0.0
        else:
            cells[UNASSIGNED] = None
        data.setdefault(" ".join(r[ci].split()), {})[year] = cells

    def money_of(name: str, year: int) -> str:
        money = economies.code(name)
        return "SUN" if money == "RUS" and year <= 1991 else money

    rows, cover = [], []
    for name, years in sorted(data.items()):
        read = [y for y, c in years.items() if c["TOTAL"] is not None]
        if not read:
            continue
        first_year = min(read)
        opening = [c for c in CLASSES if (years[first_year][c] or 0) > 0]
        spans = {}
        for y in read:
            m = money_of(name, y)
            spans[m] = (min(spans.get(m, (y, y))[0], y), max(spans.get(m, (y, y))[1], y))
        for m, (a, b) in sorted(spans.items(), key=lambda kv: kv[1]):
            cover.append({"money": m, "act": "T2", "source": BOC_SOURCE, "first_year": a, "last_year": b,
                          "note": "a stock of the state's debt in default, per creditor class"
                                  + (f"; its first year already holds a stock ({', '.join(opening)}): a default "
                                     "begun before it is dated by the sources before 1960, or cannot be read"
                                     if opening and a == first_year else "")
                                  + ("; the database's one line for the USSR and the Russian Federation, read as "
                                     "one series" if m in ("SUN", "RUS") else "")})
        for year in sorted(years):
            if year == first_year:
                continue
            money = money_of(name, year)
            now, before = years[year], years.get(year - 1)
            if now["TOTAL"] is None:
                continue
            loc = f"Debt_2025, {name}, {year}"
            readable = before is not None and before["TOTAL"] is not None
            # the headline: the first year of a stock in each creditor class (3d, O1)
            new = [c for c in CLASSES if (now[c] or 0) > 0 and (not readable or before[c] == 0)]
            if new:
                size = round(sum(now[c] for c in new), 3)
                sizes = "; ".join(f"{c} {now[c]:,.3f}" for c in new)
                private = [c for c in new if c in PRIVATE]
                if readable:
                    rows.append(line(money, "T2", str(year), size, "US$ million", BOC_SOURCE,
                                     loc + ", " + " ".join(new),
                                     note=f"the first year of a stock in default in: {sizes} (US$ million; the "
                                          f"database's classes may overlap, so the sum is an upper bound)"
                                          f"; private or local-currency: {'yes' if private else 'no'}"))
                else:
                    rows.append(line(money, "T2", str(year), size, "US$ million", BOC_SOURCE,
                                     loc + ", " + " ".join(new),
                                     note=f"a stock in default ({sizes}); the year before cannot be read",
                                     status="apart"))
            # the variants: private creditors and local-currency debt only; the total stock (the first build)
            if readable:
                prv = [c for c in PRIVATE if (now[c] or 0) > 0 and before[c] == 0]
                if prv:
                    rows.append(line(money, "T2-var-private", str(year), round(sum(now[c] for c in prv), 3),
                                     "US$ million", BOC_SOURCE, loc + ", " + " ".join(prv),
                                     note="variant: the first year of a stock owed to private creditors or in "
                                          "local currency", status="apart"))
                if now["TOTAL"] > 0 and before["TOTAL"] == 0:
                    rows.append(line(money, "T2-var-total", str(year), now["TOTAL"], "US$ million", BOC_SOURCE,
                                     loc + ", TOTAL", note="variant: the first year of a total stock (the first build)",
                                     status="apart"))
    return rows, cover


# --- L1 and L3: Garriga ------------------------------------------------------------------------------------

def _garriga() -> tuple[list[dict], list[dict]]:
    iso2 = {e["iso2Code"]: e["id"] for e in __import__("json").loads(economies.WB.read_text())[1]
            if e["region"]["value"] not in ("", "Aggregates")}
    wanted = ("year", "cname", "ISO", "reform", "decrease", "direction", "lvau_garriga", "cuk_limlen")
    by: dict[str, dict[int, dict]] = {}
    names: dict[str, str] = {}
    unknown: set[str] = set()
    with open(GARRIGA, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            r = {k: (r.get(k) or "").strip().strip('"') for k in wanted}
            money = iso2.get(r["ISO"])
            if money is None:
                try:
                    money = economies.code(r["cname"])
                except KeyError:
                    unknown.add(f"{r['cname']} ({r['ISO'] or 'no ISO'})")
                    continue
            year = int(float(r["year"]))
            if year in by.get(money, {}) and by[money][year]["cname"] != r["cname"]:
                raise ValueError(f"Garriga: {money} {year} held twice ({by[money][year]['cname']}, {r['cname']})")
            names[money] = r["cname"]
            by.setdefault(money, {})[year] = r
    if unknown:
        print("Garriga rows with no economy code, left out:", sorted(unknown))

    def num(x: str) -> float | None:
        try:
            return float(x)
        except ValueError:
            return None

    rows, cover = [], []
    for money, years in sorted(by.items()):
        for field, act in (("cuk_limlen", "L1"), ("reform", "L3")):
            read = [y for y, r in years.items() if num(r[field]) is not None]
            if read:
                cover.append({"money": money, "act": act, "source": GARRIGA_SOURCE, "first_year": min(read),
                              "last_year": max(read), "note": f"`{field}`"})
        for year in sorted(years):
            r, prev = years[year], years.get(year - 1)
            loc = f"Replication_ISQ_2025.tab, {names[money]}, {year}"
            now, before = num(r["cuk_limlen"]), num(prev["cuk_limlen"]) if prev else None
            if now is not None and before is not None and now < before:
                rows.append(line(money, "L1", str(year), round(now - before, 6), "index points", GARRIGA_SOURCE,
                                 loc + ", cuk_limlen",
                                 note=f"the component falls; the cap {'stood' if before >= 0.5 else 'did not stand'} "
                                      f"before (>= 0.5) and {'still stands' if now >= 0.5 else 'no longer stands'} after"))
            if num(r["reform"]) == 1 and num(r["decrease"]) == 1:
                clash = num(r["direction"]) is not None and num(r["direction"]) >= 0
                rows.append(line(money, "L3", str(year), 1, "flag", GARRIGA_SOURCE, loc + ", reform and decrease",
                                 note="a legal reform Garriga codes as decreasing independence"
                                      + (f"; her `direction` reads {r['direction']}: her flags disagree (the audit's "
                                         "M12; frame a reads `direction`)" if clash else "")))
            idx, idx_before = num(r["lvau_garriga"]), num(prev["lvau_garriga"]) if prev else None
            if idx is not None and idx_before is not None and idx - idx_before <= -0.05 + 1e-12:
                rows.append(line(money, "L3-var-index", str(year), round(idx - idx_before, 6), "index points",
                                 GARRIGA_SOURCE, loc + ", lvau_garriga",
                                 note="variant: the index down by 0.05 or more", headline=False,
                                 status="apart"))
    return rows, cover


def scripted() -> tuple[list[dict], list[dict]]:
    rows, cover = [], []
    for part in (_varieties(), _ttid(), _boc(), _garriga()):
        rows += part[0]
        cover += part[1]
    return rows, cover


def hand(path: str | Path) -> list[dict]:
    """The coders' settled lines, as given (FT-001-M3-acts.md, section 3)."""
    with open(path, newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def build(hand_path: str | Path, hand_coverage: str | Path) -> None:
    sha = m0.require_locked()
    rows, cover = scripted()
    rows += hand(hand_path)
    cover += hand(hand_coverage)
    for r in rows:
        r["rules_sha256"] = sha
    rows.sort(key=lambda r: (r["money"], r["period"], r["route"]))
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "series.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SERIES_FIELDS, extrasaction="raise")
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "coverage.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COVERAGE_FIELDS)
        w.writeheader()
        w.writerows(sorted(cover, key=lambda c: (c["money"], c["act"], c["source"])))
    print(f"{len(rows)} lines, {len(cover)} coverage rows -> {OUT}")


def rates(folder: Path = OUT) -> list[tuple[str, str, int, int, float]]:
    """M0 [a-R4]: each headline act's rate per economy-year of its source's coverage (the audit's M10):
    (act, source, counted lines inside the coverage, economy-years, lines per 100 economy-years)."""
    with open(folder / "series.csv", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["status"] == "counted"]
    with open(folder / "coverage.csv", newline="") as f:
        cover = list(csv.DictReader(f))
    spans: dict[tuple[str, str], dict[str, set[int]]] = {}
    for c in cover:
        if c["first_year"] and c["last_year"]:
            key = (c["act"].split()[0], c["source"].split(" (")[0])  # "T2 domestic" and "T2 external": one T2
            spans.setdefault(key, {}).setdefault(c["money"], set()).update(
                range(int(c["first_year"]), int(c["last_year"]) + 1))
    out = []
    for (act, source), by in sorted(spans.items()):
        years = sum(len(s) for s in by.values())
        n = sum(1 for r in rows if r["route"] == act and r["source"].split(" (")[0] == source
                and int(r["period"][:4]) in by.get(r["money"], ()))
        out.append((act, source, n, years, round(100 * n / years, 2) if years else 0.0))
    return out


def count() -> None:
    rows, cover = scripted()
    tally = Counter((r["route"], r["status"], r["source"].split(" (")[0][:40]) for r in rows)
    for key, n in sorted(tally.items()):
        print(n, *key, sep="\t")
    print(len({r["money"] for r in rows}), "economies with an act;", len(cover), "coverage rows")


if __name__ == "__main__":
    if sys.argv[1:2] == ["count"]:
        count()
    elif sys.argv[1:2] == ["rates"]:
        for r in rates():
            print(*r, sep="\t")
    elif sys.argv[1:2] == ["build"] and "--hand" in sys.argv and "--hand-coverage" in sys.argv:
        build(sys.argv[sys.argv.index("--hand") + 1], sys.argv[sys.argv.index("--hand-coverage") + 1])
    else:
        print(__doc__)
        sys.exit(2)
