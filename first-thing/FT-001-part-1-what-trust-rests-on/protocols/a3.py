"""FT-001 M4, A3: the premiums read as expectations (card ``FT-001-M4-A3-premiums.md``; M0 v4.2 section 7, A3).

The rules, on toy series (``test_a3.py``) before any real premium, gold price or yield was read; then the build, run from
the workshop's root with the toolkit's interpreter::

    toolkit/bin/ftpy bank/maps/FT-001/missions/code/a3.py build --go [--overwrite]

It writes ``data/reconstructed/ft001-a3/``: ``series.csv`` (one line per case and month), ``spans.csv`` (the "cannot
separate" spans), ``check-1914.csv``, ``variant-short.csv``, ``variant-cross-source.csv`` and ``cross-source.csv`` (the
months where two premium sources differ by more than 2%). The session writes the manifest. ``build`` without ``--go``
refuses, and an existing folder is refused unless ``--overwrite`` is given.

The premium series come from the transcriptions (``ft001-a3/transcriptions/``, a reader that is not the session, card
section 3). Which file and which column is each case's headline, cross-check and gold-basis yield is said in
``transcriptions/selection.csv`` (columns ``case, role, file, series``), written by the session from the readers'
coverage report, before any value is used. ``series`` is a column name as the transcription's ``series`` field gives it,
or ``hi=<name>;lo=<name>`` for a table printing the month's (or the day's) highest and lowest.

A3 is a **model's reading**: no test, no p-value, no verdict.

Readings made in code, in the open, for the audit (the card's *readings* are its own and bind this module):

Y1. *A printed yield is r as printed*, an annual rate in percent divided by 100, used as the continuous rate of the model
    (P = λ/(λ + r); P = q·e^(−r(T−t))). The difference between an annual and a continuous rate of 3-6% is under 0.2 point,
    said, not corrected.
Y2. *The gold yield of the US 6s computed from a currency price* (card section 4, option 2): the price in gold is
    price × 100 / G, and the yield is the rate y at which semi-annual coupons of 3 per 100 to 1 July 1881 and the principal
    then, discounted continuously, equal that price (bisection to 1e-10).
Y3. *A month's value* is the mean of the source's quotations dated in that month. A month with a highest and a lowest is
    (max of highs + min of lows) / 2. An annual quotation stays annual: it reads the year, flagged ``annual``, and is never
    spread over months.
Y7. *After the first build was checked* (its small check's A1, B2): the greenbacks' after-law reading flips with r, so
    the first build's consol substitute is kept as ``variant-r-consols.csv`` and the case is also read at a flat r of
    3.2-6% (``r-sensitivity.csv``); the cross-check compares only the periods the headline reads (Y6 narrowed), and the
    cross-source variant's spans are written (``variant-cross-source-spans.csv``).
Y4. *The run rule* (card section 5): a calendar year's mean λ is the mean of its read months' λ; an ``at par`` month is
    λ = ∞, so a year with one is ∞. A year with no read month breaks a run.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import m0
import xlsx

ROOT = Path(__file__).resolve().parents[5]
DATA = ROOT / "data"
OUT = DATA / "reconstructed" / "ft001-a3"
TRANS = OUT / "transcriptions"
MILLENNIUM = DATA / "bankofengland" / "millennium" / "2026-09-30" / "a-millennium-of-macroeconomic-data-for-the-uk.xlsx"
JST = DATA / "jst" / "macrohistory" / "2026-09-30" / "JSTdatasetR6.dta"

MINT_PRICE = 3 + 17 / 20 + 10.5 / 240          # £3 17s 10½d per ounce of standard gold (card section 2)
CROSS_SOURCE_GAP = 0.02                         # card section 3: a month where two sources differ by more than 2%
RUN_YEARS = 3                                   # card section 5: three or more consecutive calendar years
WITHIN_A_YEAR = 1.0                             # λ ≥ 1 per year: resumption expected within a year
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


@dataclass(frozen=True)
class Case:
    name: str
    money: str
    first: str              # first month read, YYYY-MM
    last: str               # last month read
    law_passed: date        # the resumption law: months from its month on are "after the law"
    legislated: date        # T
    resumed: date


CASES = (
    Case("the Bank Restriction", "GBR", "1797-03", "1821-05", date(1819, 7, 2), date(1823, 5, 1), date(1821, 5, 1)),
    Case("the greenbacks", "USA", "1862-01", "1879-01", date(1875, 1, 14), date(1879, 1, 1), date(1879, 1, 1)),
)

# The 1914 check (card section 6): parity in local currency per US dollar, the years read, the outcome.
CHECK_1914 = (
    ("GBR", "back at par", 1 / 4.8665, 1915, 1924),
    ("FRA", "devalued", 5.1826, 1915, 1927),
    ("ITA", "devalued", 5.1826, 1915, 1926),
    ("DEU", "replaced", 4.1979, 1915, 1922),
)
CHECK_COMMON = (1915, 1920)
# Y5 (card section 10, written after the first check had been run and seen): JST R6 states some monies in a later unit.
# Its 1913 values, the last gold-standard year, are the statutory parity divided by: France 100 (the new franc of 1960)
# and Germany about 1e12 (the 1923-24 reform: a Reichsmark of a trillion paper marks); the UK and Italy 1. The parity is
# restated in JST's unit by that factor, never fitted: 100 and 1e12 are the reforms' own ratios.
JST_UNITS = {"FRA": 100.0, "DEU": 1e12}


# ---- the model --------------------------------------------------------------------------------------------------------

def paper_value_restriction(market_price: float) -> float:
    """P: the paper pound's value in gold, from the market price of standard gold in paper pounds per ounce."""
    return MINT_PRICE / market_price


def paper_value_greenback(gold_price: float) -> float:
    """P: the greenback dollar's value in gold, from the price of $100 in gold in currency."""
    return 100.0 / gold_price


PAR_TOLERANCE = 1e-9   # a market price printed at the mint price is par: 3.89375 / (3 + 17/20 + 10.5/240) is not 1.0 in floats


def hazard(p: float, r: float) -> float:
    """λ from P = λ/(λ + r), before the law; ∞ at or above par (``at par``)."""
    if p >= 1 - PAR_TOLERANCE:
        return math.inf
    if p <= 0 or r <= 0:
        raise ValueError(f"P {p} and r {r} must be positive")
    return r * p / (1 - p)


def years_between(t: date, later: date) -> float:
    return (later - t).days / 365.25


def mid_month(period: str) -> date:
    """The 15th of a month; 1 July for a year read alone (Y3)."""
    if len(period) == 4:
        return date(int(period), 7, 1)
    y, m = period.split("-")[:2]
    return date(int(y), int(m), 15)


def q_after(p: float, r: float, t: date, legislated: date) -> float:
    """q from P = q·e^(−r(T−t)), after the law."""
    return p * math.exp(r * years_between(t, legislated))


def phase(case: Case, period: str) -> str:
    """A month from the law's month on, or a year read alone whose 1 July is on or after the law, is after the law."""
    if len(period) == 4:
        return "after the law" if mid_month(period) >= case.law_passed else "before the law"
    y, m = (int(x) for x in period.split("-")[:2])
    return "after the law" if (y, m) >= (case.law_passed.year, case.law_passed.month) else "before the law"


def periods(case: Case, p_by_period: dict[str, float]) -> list[str]:
    """The case's months; a year with no monthly premium but an annual one is one line, the year (Y3)."""
    out = []
    for period in month_span(case.first, case.last):
        y = period[:4]
        if y in p_by_period and not any(k[:4] == y and len(k) == 7 for k in p_by_period):
            if y not in out:
                out.append(y)
        else:
            out.append(period)
    return out


def rate_for(r_by_period: dict[str, float], period: str) -> float | None:
    """The month's r; for a year read alone, the mean of its months' r, or the year's own."""
    if period in r_by_period:
        return r_by_period[period]
    if len(period) == 4:
        months = [v for k, v in r_by_period.items() if k[:4] == period and len(k) == 7]
        if months:
            return sum(months) / len(months)
    return r_by_period.get(period[:4])


def cannot_separate_years(lam_by_period: dict[str, float]) -> set[int]:
    """The calendar years of every run of RUN_YEARS or more consecutive years whose mean λ is ≥ 1 (Y4)."""
    by_year: dict[int, list[float]] = defaultdict(list)
    for period, lam in lam_by_period.items():
        by_year[int(period[:4])].append(lam)
    mean = {y: (math.inf if any(math.isinf(v) for v in vs) else sum(vs) / len(vs)) for y, vs in by_year.items()}
    out: set[int] = set()
    run: list[int] = []
    for y in range(min(mean, default=0), max(mean, default=-1) + 2):
        if y in mean and mean[y] >= WITHIN_A_YEAR:
            run.append(y)
            continue
        if len(run) >= RUN_YEARS:
            out.update(run)
        run = []
    return out


def gold_yield_6s(price_currency: float, gold_price: float, t: date, maturity: date = date(1881, 7, 1)) -> float:
    """Y2: the continuous yield of a 6% bond to ``maturity`` (semi-annual coupons of 3) at its price in gold."""
    price = price_currency * 100.0 / gold_price
    flows = []
    y, m = maturity.year, maturity.month
    d = maturity
    while d > t:
        flows.append((years_between(t, d), 3.0 + (100.0 if d == maturity else 0.0)))
        m -= 6
        if m <= 0:
            m += 12
            y -= 1
        d = date(y, m, maturity.day)
    if not flows:
        raise ValueError("no flow after t")

    def value(rate: float) -> float:
        return sum(c * math.exp(-rate * s) for s, c in flows)

    lo, hi = -0.5, 1.0
    if not value(hi) <= price <= value(lo):
        raise ValueError(f"price {price} outside the bracket")
    for _ in range(200):
        mid = (lo + hi) / 2
        if value(mid) > price:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-10:
            break
    return (lo + hi) / 2


def readings(case: Case, p_by_period: dict[str, float], r_by_period: dict[str, float]) -> list[dict]:
    """One reading per month of the case's span: P, r, phase, λ or q, the reading, the status."""
    lam_before = {}
    rows = []
    for period in periods(case, p_by_period):
        p, r = p_by_period.get(period), rate_for(r_by_period, period)
        row = {"period": period, "P": p, "r": r, "phase": phase(case, period), "lambda": None, "q": None,
               "reading": "", "status": "counted", "flags": ["annual"] if len(period) == 4 else []}
        if p is None or r is None:
            row.update(status="cannot be read", reading="cannot be read",
                       flags=["no premium" if p is None else "no yield"])
        elif row["phase"] == "before the law":
            row["lambda"] = hazard(p, r)
            if math.isinf(row["lambda"]):
                row["flags"].append("at par")
            lam_before[period] = row["lambda"]
            row["reading"] = "model"
        else:
            row["q"] = q_after(p, r, mid_month(period), case.legislated)
            row["reading"] = "cannot separate" if row["q"] >= 1 else "model"
        if p is not None and p > 1 + PAR_TOLERANCE:
            row["flags"].append("above par")
        rows.append(row)
    years = cannot_separate_years(lam_before)
    for row in rows:
        if row["phase"] == "before the law" and row["status"] == "counted" and int(row["period"][:4]) in years:
            row["reading"] = "cannot separate"
    return rows


def spans(rows: list[dict]) -> list[tuple[str, str, str]]:
    """The runs of consecutive months read "cannot separate": (first, last, rule)."""
    out, cur = [], None
    for row in rows:
        if row["reading"] == "cannot separate":
            rule = "q >= 1" if row["phase"] == "after the law" else f"mean lambda >= 1 in {RUN_YEARS}+ consecutive years"
            if cur and cur[2] == rule:
                cur = (cur[0], row["period"], rule)
            else:
                if cur:
                    out.append(cur)
                cur = (row["period"], row["period"], rule)
        elif cur:
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def month_span(first: str, last: str) -> list[str]:
    y, m = (int(x) for x in first.split("-"))
    ly, lm = (int(x) for x in last.split("-"))
    out = []
    while (y, m) <= (ly, lm):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


# ---- the transcriptions -----------------------------------------------------------------------------------------------

def monthly(rows: list[dict], series: str) -> dict[str, float]:
    """Y3: a transcription's series by month (or by year where only a year is printed)."""
    if series.startswith("hi="):
        hi_name, lo_name = (part.split("=", 1)[1] for part in series.split(";"))
        hi, lo = _by_period(rows, hi_name, max), _by_period(rows, lo_name, min)
        return {k: (hi[k] + lo[k]) / 2 for k in hi if k in lo}
    return _by_period(rows, series, lambda vs: sum(vs) / len(vs))


def _by_period(rows: list[dict], series: str, agg) -> dict[str, float]:
    got: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        if r["series"].strip() != series or not str(r["value_decimal"]).strip():
            continue
        d = r["date"].strip()
        key = d[:7] if len(d) >= 7 else d[:4]
        got[key].append(float(r["value_decimal"]))
    return {k: agg(v) for k, v in got.items()}


def cross_source(a: dict[str, float], b: dict[str, float]) -> list[tuple[str, float, float]]:
    """The periods both sources read where they differ by more than CROSS_SOURCE_GAP of the first. Y6: where the first
    reads a year alone (an annual headline), the second is read as the mean of its quotations in that year."""
    b = dict(b)
    for k in a:
        if len(k) == 4 and k not in b:
            months = [v for m, v in b.items() if m[:4] == k and len(m) == 7]
            if months:
                b[k] = sum(months) / len(months)
    return [(k, a[k], b[k]) for k in sorted(set(a) & set(b)) if abs(b[k] - a[k]) > CROSS_SOURCE_GAP * a[k]]


def cross_compared(a: dict[str, float], b: dict[str, float]) -> int:
    """How many of the first source's periods the second reads (Y6's rule), so that "none over 2%" has its n."""
    return sum(1 for k in a if k in b or (len(k) == 4 and any(m[:4] == k and len(m) == 7 for m in b)))


def check_1914(xr: dict[tuple[str, int], float], rate: dict[tuple[str, int], float]) -> tuple[list[dict], str]:
    """Card section 6: each case's yearly λ and the common-window mean; the order and whether it is consistent."""
    lines, means = [], {}
    for iso, outcome, parity, first, last in CHECK_1914:
        common = []
        for y in range(first, last + 1):
            x, r = xr.get((iso, y)), rate.get((iso, y))
            line = {"money": iso, "year": y, "outcome": outcome, "parity": parity, "xrusd": x, "r": r,
                    "P": None, "lambda": None, "status": "cannot be read"}
            if x and r and r > 0:
                p = parity / JST_UNITS.get(iso, 1.0) / x
                lam = hazard(p, r)
                line.update(P=p, **{"lambda": lam}, status="counted")
                if CHECK_COMMON[0] <= y <= CHECK_COMMON[1]:
                    common.append(lam)
            lines.append(line)
        n_common = CHECK_COMMON[1] - CHECK_COMMON[0] + 1
        means[iso] = (math.inf if any(math.isinf(v) for v in common) else sum(common) / len(common)) \
            if len(common) == n_common else None
    m = means
    if any(v is None for v in m.values()):
        verdict = "cannot be read: " + ", ".join(k for k, v in m.items() if v is None) + " not read in every common year"
    else:
        ok = m["GBR"] > max(m["FRA"], m["ITA"]) and min(m["FRA"], m["ITA"]) > m["DEU"]
        verdict = ("consistent" if ok else "not consistent") + ": " + ", ".join(
            f"{k} {v:.4g}" for k, v in sorted(m.items(), key=lambda kv: -kv[1]))
    return lines, verdict


# ---- the frozen inputs ------------------------------------------------------------------------------------------------

def millennium_monthly(sheet: str, column_title_start: str) -> dict[str, float]:
    rows = xlsx.rows(MILLENNIUM, sheet)
    head = next(r for r in rows if r and r[0] == "Description")
    col = next(i for i, c in enumerate(head) if isinstance(c, str) and c.startswith(column_title_start))
    out = {}
    for r in rows:
        if not r or not isinstance(r[0], (int, float)) or not isinstance(r[1], str) or r[1][:3] not in MONTHS:
            continue
        v = r[col] if col < len(r) else None
        if isinstance(v, (int, float)):
            out[f"{int(r[0]):04d}-{MONTHS.index(r[1][:3]) + 1:02d}"] = v / 100.0
    return out


def read_transcription(name: str) -> list[dict]:
    with open(TRANS / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def selection() -> list[dict]:
    with open(TRANS / "selection.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def jst() -> tuple[dict, dict, dict]:
    import pandas as pd
    d = pd.read_stata(JST)
    d = d[(d.year >= 1913) & (d.year <= 1928)]
    get = lambda col: {(r.iso, int(r.year)): float(getattr(r, col)) for r in d.itertuples()
                       if getattr(r, col) == getattr(r, col)}
    return get("xrusd"), {k: v / 100 for k, v in get("ltrate").items()}, {k: v / 100 for k, v in get("stir").items()}


# ---- the build --------------------------------------------------------------------------------------------------------

FIELDS = ("period", "value", "unit", "source", "locator", "note", "uncertainty", "money", "frame", "route", "entry_date",
          "entry_measure", "entry_measure_date", "outcome", "outcome_date", "onset_date", "responses", "exit", "status",
          "coder", "rules_sha256", "case", "phase", "P", "r", "r_source", "lambda", "expected_wait_years", "q", "reading",
          "flags")


def _fmt(x) -> str:
    if x is None:
        return ""
    if isinstance(x, float):
        return "inf" if math.isinf(x) else f"{x:.6g}"
    return str(x)


SENSITIVITY_R = (0.032, 0.035, 0.04, 0.045, 0.05, 0.06)


def r_sensitivity(case: Case, p_by_period: dict[str, float], rates=SENSITIVITY_R) -> list[dict]:
    """Y7 (after the first build had been seen: the small check's A1): the case read at a flat r, for each r, counting
    the months after the law with q >= 1 and the years before it inside a "cannot separate" run. Descriptive."""
    out = []
    for rate in rates:
        rows = readings(case, p_by_period, {k: rate for k in p_by_period})
        after = [x for x in rows if x["phase"] == "after the law" and x["status"] == "counted"]
        before = {x["period"][:4] for x in rows if x["phase"] == "before the law" and x["status"] == "counted"}
        sep = {x["period"][:4] for x in rows if x["phase"] == "before the law" and x["reading"] == "cannot separate"}
        out.append({"case": case.name, "r": rate, "months_after_law": len(after),
                    "q_at_least_1": sum(x["reading"] == "cannot separate" for x in after),
                    "years_before_law": len(before), "years_cannot_separate": len(sep)})
    return out


def case_lines(case: Case, rows: list[dict], p_source: str, r_source: str, sha: str) -> list[dict]:
    out = []
    for row in rows:
        lam = row["lambda"]
        out.append({
            "period": row["period"], "value": "nan" if row["P"] is None else _fmt(row["P"]),
            "unit": "paper's value in gold (par = 1)",
            "source": p_source, "locator": "transcriptions/selection.csv", "note": "", "uncertainty": "a model's reading",
            "money": case.money, "frame": "A3", "route": "", "entry_date": row["period"], "entry_measure": "",
            "entry_measure_date": "", "outcome": "", "outcome_date": "", "onset_date": "", "responses": "", "exit": "",
            "status": row["status"], "coder": "a3.py", "rules_sha256": sha, "case": case.name, "phase": row["phase"],
            "P": _fmt(row["P"]), "r": _fmt(row["r"]), "r_source": r_source, "lambda": _fmt(lam),
            "expected_wait_years": _fmt(None if lam is None else (0.0 if math.isinf(lam) else 1 / lam)),
            "q": _fmt(row["q"]), "reading": row["reading"], "flags": "; ".join(row["flags"])})
    return out


def write_csv(path: Path, fields, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fields))
        w.writeheader()
        w.writerows(rows)


def build(sha: str, overwrite: bool = False) -> dict:
    sel = selection()
    pick = lambda case, role: [s for s in sel if s["case"] == case and s["role"] == role]
    uk_long = millennium_monthly("M10. Mthly long-term rates", "Yield on 3% consols 1753-1823")
    uk_short = millennium_monthly("M9. Mthly short-term rates", "Bank Rate")
    world_long = millennium_monthly("M10. Mthly long-term rates", "Yield on 3% consols 1852-1888")
    summary, series_rows, short_rows, cross_rows, cross_variant, span_rows = {}, [], [], [], [], []
    consols_rows, cross_span_rows, sensitivity = [], [], []
    for case in CASES:
        to_p = paper_value_restriction if case.money == "GBR" else paper_value_greenback
        head = pick(case.money, "headline")
        if len(head) != 1:
            raise ValueError(f"{case.money}: selection.csv must name exactly one headline")
        h = head[0]
        price = monthly(read_transcription(h["file"]), h["series"])
        p = {k: to_p(v) for k, v in price.items()}
        if case.money == "GBR":
            r, r_src, r_short = uk_long, "Millennium M10, 3% consols 1753-1823 (Neal 1990)", uk_short
        else:
            r, r_src = {}, ""
            for s in pick("USA", "gold yield"):
                r = {k: v / 100 for k, v in monthly(read_transcription(s["file"]), s["series"]).items()}
                r_src = f"{s['file']}: {s['series']} (gold basis, as printed)"
            for s in pick("USA", "currency price of the 6s") if not r else []:
                cp = monthly(read_transcription(s["file"]), s["series"])
                r = {k: gold_yield_6s(v, price[k], mid_month(k if len(k) == 7 else k + "-07"))
                     for k, v in cp.items() if k in price}
                r_src = f"{s['file']}: {s['series']}, converted to gold at the year's average G (Mitchell 1908 Table 2's yearly row; reading Y2)"
            if not r:
                r, r_src = world_long, "Millennium M10, consols 1852-1888 (NBER): a gold world's long yield, not the US's"
            r_short = {}
        rows = readings(case, p, r)
        series_rows += case_lines(case, rows, f"{h['file']}: {h['series']}", r_src, sha)
        if case.money == "USA":   # Y7: the first build's r, kept as a variant, and the flat-r table (the small check's A1)
            consols_rows += case_lines(case, readings(case, p, world_long), f"{h['file']}: {h['series']}",
                                       "Millennium M10, consols 1852-1888 (NBER): the first build's substitute", sha)
            sensitivity += r_sensitivity(case, p)
        span_rows += [{"case": case.name, "first": a, "last": b, "rule": rule} for a, b, rule in spans(rows)]
        srows = readings(case, p, r_short)
        short_rows += case_lines(case, srows, f"{h['file']}: {h['series']}", "short rate" if r_short else "none", sha)
        read = set(periods(case, price))     # Y6 narrowed (the small check's B2): only the periods the headline reads
        price_read = {k: v for k, v in price.items() if k in read}
        for c in pick(case.money, "cross"):
            other = monthly(read_transcription(c["file"]), c["series"])
            cross_rows += [{"case": case.name, "period": k, "headline": f"{a:.6g}", "cross": f"{b:.6g}",
                            "cross_source": f"{c['file']}: {c['series']}"} for k, a, b in cross_source(price_read, other)]
            summary.setdefault("cross-source periods compared", {})[case.money] = cross_compared(price_read, other)
            crows = readings(case, {k: to_p(v) for k, v in other.items()}, r)
            cross_variant += case_lines(case, crows, f"{c['file']}: {c['series']}", r_src, sha)
            cross_span_rows += [{"case": case.name, "first": a, "last": b, "rule": rule} for a, b, rule in spans(crows)]
        summary[case.money] = {"months": len(rows), "read": sum(x["status"] == "counted" for x in rows),
                               "cannot separate": sum(x["reading"] == "cannot separate" for x in rows),
                               "spans": len(spans(rows))}
    xr, lt, st = jst()
    check_lines, check_verdict = check_1914(xr, lt)
    _, short_verdict = check_1914(xr, st)
    if OUT.exists() and (OUT / "series.csv").exists() and not overwrite:
        raise SystemExit(f"{OUT}/series.csv exists: give --overwrite")
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "series.csv", FIELDS, series_rows)
    write_csv(OUT / "variant-short.csv", FIELDS, short_rows)
    write_csv(OUT / "variant-cross-source.csv", FIELDS, cross_variant)
    write_csv(OUT / "spans.csv", ("case", "first", "last", "rule"), span_rows)
    write_csv(OUT / "variant-cross-source-spans.csv", ("case", "first", "last", "rule"), cross_span_rows)
    write_csv(OUT / "variant-r-consols.csv", FIELDS, consols_rows)
    write_csv(OUT / "r-sensitivity.csv", ("case", "r", "months_after_law", "q_at_least_1", "years_before_law",
                                          "years_cannot_separate"), sensitivity)
    write_csv(OUT / "cross-source.csv", ("case", "period", "headline", "cross", "cross_source"), cross_rows)
    write_csv(OUT / "check-1914.csv", ("money", "year", "outcome", "parity", "xrusd", "r", "P", "lambda", "status"),
              [{k: _fmt(v) for k, v in line.items()} for line in check_lines])
    summary["check 1914"] = check_verdict
    summary["check 1914, short"] = short_verdict
    summary["cross-source months over 2%"] = len(cross_rows)
    return summary


def main(argv: list[str]) -> None:
    if argv[:1] != ["build"] or "--go" not in argv:
        raise SystemExit("usage: a3.py build --go [--overwrite]")
    print(json.dumps(build(m0.require_locked(), overwrite="--overwrite" in argv), indent=1))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
