"""FT-001 M3, first part: frame b, breaks, by rule (FT-001-M3-panel.md, section 3; M0 v4.2 section 5 b).

A money's **timeline** is a list of periods in order (``panel.timeline``): months inside its monthly span, years
outside it (R3), each carrying π (π12 for a month, π(y) for a year), its source, and d, the depreciation read
on the same period (R11). This module holds the rules only, on any timeline; ``panel.py`` builds the timelines
from the frozen sources and ``build_b`` writes ``data/reconstructed/ft001-b/``.

- **Crossing** (b2): the first of ``cross_months`` consecutive calendar months, each readable and at or above
  the line; a year read annually crosses when π(y) is at or above it. A money crosses only while unbroken.
- **Restoration** (b3, R15): readable periods below the lower line adding up to 24 months (a year counts
  twelve), dated at the period that completes them; an unreadable period or a reading at or above the lower
  line starts the count again.
- **Onset** (b4-b5, R16): for each route, the run of readable periods at or above the route's line **through the
  crossing's period**; a run begun at or after crossing - bound is a candidate; the onset is the earliest
  candidate (π before d on a tie); none, the bound (flagged); a route unreadable at the crossing, or whose run
  reaches an unreadable period that lies at or after the bound, makes the onset *cannot be read*. An
  unreadable period lying wholly before the bound leaves the run read as beginning after it (its date is then
  the bound's month or later).
- **Status** (b10): *counted*; *apart* when the crossing is the money's first readable period ("the record
  begins at or above the line") or follows an unreadable period ("the crossing follows a gap": it may have
  happened inside the gap — a reading the protocol did not state for gaps inside the record, said in the
  manifest); **second build** (the audit's O4): also the next crossing after a stretch of readings that
  begins at or above the line, unless 24 months below the lower line come first (see ``find``); and (O3) a
  crossing of a euro member on or after its changeover, "a euro member after its changeover".
"""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass
class Period:
    label: str            # "YYYY-MM" for a month, "YYYY" for a year
    freq: str             # "M" or "A"
    start: int            # month index: year * 12 + month - 1 (a year starts in its January)
    months: int           # 1 or 12
    pi: float | None = None
    pi_source: str = ""
    pi_flag: bool = False  # the reading's span holds an IFS observation flagged B (R5)
    d: float | None = None
    d_rise: float | None = None  # d less d twelve months (one year) before, for the Frankel-Rose grid
    d_flag: bool = False
    d_anchor: str = ""


@dataclass(frozen=True)
class Params:
    line: float = 20.0
    cross_months: int = 3
    lower: float = 10.0
    restore_months: int = 24
    bound: int = 36
    d_line: float = 15.0
    d_rise: float | None = None
    routes: tuple[str, ...] = ("pi", "d")
    drop_flagged: bool = False
    bound_apart: bool = False


HEADLINE = Params()


def month_label(index: int) -> str:
    return f"{index // 12:04d}-{index % 12 + 1:02d}"


def month_index(label: str) -> int:
    y, m = label.split("-")
    return int(y) * 12 + int(m) - 1


def _crossing_at(tl: list[Period], i: int, p: Params) -> list[int] | None:
    first = tl[i]
    if first.pi is None or first.pi < p.line:
        return None
    if first.freq == "A":
        return [i]
    found = [i]
    for k in range(1, p.cross_months):
        j = i + k
        if j >= len(tl) or tl[j].freq != "M" or tl[j].start != first.start + k or tl[j].pi is None \
                or tl[j].pi < p.line:
            return None
        found.append(j)
    return found


def _route(tl: list[Period], c: int, route: str, p: Params) -> tuple[str, int | None]:
    """('start', j), ('none', None) or ('unknown', None) for one route's run ending at the crossing."""
    bound = tl[c].start - p.bound

    def value(q: Period) -> float | None:
        if route == "pi":
            return q.pi
        if p.d_rise is not None and q.d_rise is None:
            return None
        return q.d

    def holds(q: Period) -> bool:
        if route == "pi":
            return q.pi >= p.lower
        return q.d >= p.d_line and (p.d_rise is None or q.d_rise >= p.d_rise)

    if value(tl[c]) is None:
        return "unknown", None
    if not holds(tl[c]):
        return "none", None
    j = c
    while True:
        prev = j - 1
        if prev < 0:
            return ("unknown", None) if tl[j].start - 1 >= bound else ("start", j)
        q = tl[prev]
        if value(q) is None:
            return ("unknown", None) if q.start + q.months - 1 >= bound else ("start", j)
        if not holds(q):
            return "start", j
        if q.start < bound:
            return "none", None
        j = prev


def _bound_label(tl: list[Period], c: int, p: Params) -> str:
    if tl[c].freq == "A":
        return str(tl[c].start // 12 - p.bound // 12)
    return month_label(tl[c].start - p.bound)


def onset(tl: list[Period], c: int, p: Params, routes: tuple[str, ...] | None = None) -> dict:
    """The onset of the break crossing at index c: label, route, flag ('' | 'bound' | 'cannot be read'), index."""
    routes = routes or p.routes
    found, unknown = [], []
    for order, route in enumerate(routes):
        kind, j = _route(tl, c, route, p)
        if kind == "unknown":
            unknown.append(route)
        elif kind == "start":
            found.append((tl[j].start, order, route, j))
    if unknown:
        return {"label": "", "route": "cannot be read", "flag": "cannot be read", "index": None,
                "unknown": unknown}
    if found:
        _, _, route, j = min(found)
        return {"label": tl[j].label, "route": route, "flag": "", "index": j, "unknown": []}
    return {"label": _bound_label(tl, c, p), "route": "bound", "flag": "bound", "index": None, "unknown": []}


def _clean(tl: list[Period], p: Params) -> list[Period]:
    if not p.drop_flagged:
        return tl
    return [replace(q, pi=None if q.pi_flag else q.pi, d=None if q.d_flag else q.d,
                    d_rise=None if q.d_flag else q.d_rise) for q in tl]


def find(timeline: list[Period], p: Params = HEADLINE, absent: tuple[str, ...] = ()) -> list[dict]:
    """Every break of one money's timeline, in order, with its crossing, status, restoration and onset.

    ``absent``: onset routes the money has not at all (the United States' d, R11: the dollar has no d against
    itself; the audit's M9) — left out of the onset, never read as unreadable.

    **b10 as written** (the audit's O4, second build): a *stretch* is a run of consecutive readable periods; one
    that begins at or above the line — the record's first, or one after a gap — begins inside a break that
    cannot be dated, so the money's next crossing is *apart* ("the record begins at or above the line", or "the
    crossing follows a gap"), unless readings below the lower line adding up to 24 months (a restoration of that
    undated break) come first. A stretch that begins between the lower line and the line flags the next crossing
    ``stretch_begins`` "between the lower line and the line" under the same condition (it may continue an
    unrecorded break); the line stays counted."""
    tl = _clean(timeline, p)
    routes = tuple(r for r in p.routes if r not in absent)
    readable = [i for i, q in enumerate(tl) if q.pi is not None]
    if not readable:
        return []
    first = readable[0]
    out: list[dict] = []
    broken, count = False, 0
    pending, pending_flag, calm = "", "", 0
    for i in range(first, len(tl)):
        q = tl[i]
        starts = q.pi is not None and (i == first or tl[i - 1].pi is None)
        if not broken:
            if starts:
                where = "the record begins at or above the line" if i == first else "the crossing follows a gap"
                if q.pi >= p.line:
                    pending, pending_flag, calm = where, "", 0
                elif q.pi >= p.lower and not pending:
                    pending_flag, calm = "between the lower line and the line", 0
            idx = _crossing_at(tl, i, p)
            if idx is None:
                if q.pi is None or q.pi >= p.lower:
                    calm = 0
                else:
                    calm += q.months
                    if calm >= p.restore_months:
                        pending, pending_flag, calm = "", "", 0
                continue
            reason = ("the record begins at or above the line" if i == first
                      else "the crossing follows a gap" if tl[i - 1].pi is None else pending)
            on = onset(tl, i, p, routes)
            pi_only = onset(tl, i, p, ("pi",))
            status = "apart" if reason else "counted"
            if status == "counted" and p.bound_apart and on["flag"] == "bound":
                status, reason = "apart", "variant: onset at the bound"
            flag = any(tl[j].pi_flag for j in idx)
            if on["index"] is not None:
                k = on["index"]
                flag = flag or (tl[k].pi_flag if on["route"] == "pi" else tl[k].d_flag)
            out.append({"index": i, "crossing": q.label, "freq": q.freq, "pi": q.pi, "source": q.pi_source,
                        "crossing_periods": [tl[j].label for j in idx], "status": status, "reason": reason,
                        "restored": "", "onset": on, "pi_only": pi_only, "ifs_break": flag,
                        "stretch_begins": "" if reason else pending_flag})
            broken, count = True, 0
            pending, pending_flag, calm = "", "", 0
            continue
        if q.pi is None or q.pi >= p.lower:
            count = 0
            continue
        count += q.months
        if count >= p.restore_months:
            out[-1]["restored"] = q.label
            broken, count = False, 0
    return out


def restoration_undatable(timeline: list[Period], crossing: str, before: int, p: Params = HEADLINE) -> bool:
    """N1 of frame c's re-check (2026-09-30): True when, after the break crossing at ``crossing`` and before the
    month index ``before``, readings below the lower line add up to the restoration's months **once unreadable
    periods are passed over** (a reading at or above the lower line still resets). Frame b's restoration (R15)
    resets at an unreadable period, so where the months are quarterly (Sweden 1919-54, Tanzania) it cannot date
    a restoration the readings show: frame c then reads "during a break" as *cannot be read*, never "yes"."""
    tl = _clean(timeline, p)
    idx = next((i for i, q in enumerate(tl) if q.label == crossing), None)
    if idx is None:
        return False
    count = 0
    for q in tl[idx + 1:]:
        if q.start >= before:
            break
        if q.pi is None:
            continue
        if q.pi >= p.lower:
            count = 0
            continue
        count += q.months
        if count >= p.restore_months:
            return True
    return False


def public_by_convention(label: str) -> str:
    """Frame h's release lags (M0 5 h): a month's reading one month later; a year's nine months after its end."""
    if "-" in label:
        return month_label(month_index(label) + 1)
    return f"{int(label) + 1}-09"


#: The grid (b11): each variant's parameters; every other parameter stays the headline's.
VARIANTS: dict[str, Params] = {
    "line-40": replace(HEADLINE, line=40.0),
    "line-100": replace(HEADLINE, line=100.0),
    "crossing-1-month": replace(HEADLINE, cross_months=1),
    "lower-5": replace(HEADLINE, lower=5.0),
    "lower-15": replace(HEADLINE, lower=15.0),
    "bound-24": replace(HEADLINE, bound=24),
    "bound-60": replace(HEADLINE, bound=60),
    "depreciation-10": replace(HEADLINE, d_line=10.0),
    "depreciation-25-rise-10": replace(HEADLINE, d_line=25.0, d_rise=10.0),
    "pi-only-onset": replace(HEADLINE, routes=("pi",)),
    "bound-breaks-apart": replace(HEADLINE, bound_apart=True),
    "ifs-break-unreadable": replace(HEADLINE, drop_flagged=True),
}

__all__ = ["Period", "Params", "HEADLINE", "VARIANTS", "find", "onset", "month_label", "month_index",
           "public_by_convention"]


# --- the build: data/reconstructed/ft001-b/ (FT-001-M3-panel.md, sections 3 and 6) --------------------------------

CODER = "script: missions/code/breaks.py"
SOURCE_NAME = {
    "IFS-M": "IMF IFS through DBnomics, M..PCPI_IX (vintage 2026-09-30)",
    "BIS-M": "BIS long consumer price series, monthly index (vintage 2026-09-30)",
    "IFS-A": "IMF IFS through DBnomics, A..PCPI_IX (vintage 2026-09-30)",
    "World Bank": "World Bank WDI, FP.CPI.TOTL.ZG, as published (vintage 2026-09-30)",
    "Reinhart-Rogoff": "Reinhart and Rogoff, inflation files (October 2010), as published (vintage 2026-09-30)",
    "BIS-A": "BIS long consumer price series, annual index (vintage 2026-09-30)",
    "JST": "Jorda-Schularick-Taylor Macrohistory Database R6, cpi (vintage 2026-09-30)",
}
FIELDS = ["period", "value", "unit", "source", "locator", "note", "uncertainty", "money", "frame", "route",
          "entry_date", "entry_measure", "entry_measure_date", "outcome", "outcome_date", "onset_date", "responses",
          "exit", "status", "coder", "rules_sha256", "break_onset", "onset_route", "onset_flag",
          "onset_unknown_routes", "onset_d_anchor", "onset_pi_only", "frequency", "line_pct", "crossing_periods", "price_basis",
          "rr_basis_kind", "rr_basis_seam", "stretch_begins",
          "first_reading_at_line", "first_public_crossing", "public_by_convention", "regime_at_crossing",
          "regime_note", "split_at_crossing", "seams", "ifs_break", "shared_or_foreign_money", "new_money_rule",
          "variant"]


def _pi_only_label(o: dict) -> str:
    if o["flag"] == "cannot be read":
        return "cannot be read"
    return o["label"] + (" (bound)" if o["flag"] == "bound" else "")


def _seams_in(tl: list[Period], b: dict, p: Params) -> str:
    c = b["index"]
    lo = tl[c].start - p.bound
    last = c + len(b["crossing_periods"]) - 1
    out, prev = [], None
    for q in tl[:last + 1]:
        if q.pi is None:
            continue
        if prev is not None and q.pi_source != prev.pi_source and q.start >= lo:
            out.append(f"{q.label}: {prev.pi_source} -> {q.pi_source}")
        prev = q
    return "; ".join(out)


#: R11: the dollar has no d against itself; its onset reads the π route alone (the audit's M9).
ABSENT_ROUTES = {"USA": ("d",)}
EURO_APART = "a euro member after its changeover"


def euro_member_after_changeover(money: str, date: str) -> bool:
    """O3 (the audit; second build): a crossing on or after the member's entry into the euro, whose dates are
    frame a's ``EURO_ENTRY`` (the ECB's 'Our money' page, frozen; 1074f44), imported, never copied."""
    from frame_a import EURO_ENTRY
    entry = EURO_ENTRY.get(money)
    return entry is not None and date[:7] >= entry[:7 if "-" in date else 4]


def rows_for(pan, money: str, tl: list[Period], p: Params, variant: str, sha: str) -> list[dict]:
    import panel as P
    out = []
    for b in find(tl, p, ABSENT_ROUTES.get(money, ())):
        if euro_member_after_changeover(money, b["crossing"]):
            b["status"], b["reason"] = "apart", EURO_APART
        on, crossing = b["onset"], b["crossing"]
        cls, note = P.class_at(P.irr_classes().get(money), int(crossing[:4]))
        locator = pan.locator(money, b["source"])
        if b["source"] == "Reinhart-Rogoff":
            locator = pan.rr[money][int(crossing)][1]
        basis = kind = seam = ""
        if b["source"] == "Reinhart-Rogoff":
            year = int(crossing)
            spans = P.rr_basis().get(money, [])
            basis = " / ".join(sorted({lab for lo, hi, lab in spans if lo <= year <= hi})) \
                or "not stated for the year"
            kind, seam = P.rr_basis_kind(spans, year), P.rr_basis_seam(spans, year)
        anchor = ""
        if on["route"] == "d" and on["index"] is not None:
            anchor = tl[on["index"]].d_anchor
        out.append({
            "period": crossing, "value": f"{b['pi']:.4f}",
            "unit": ("percent, 12-month change of the consumer price index" if b["freq"] == "M"
                     else "percent, change of the year's average consumer price index"),
            "source": SOURCE_NAME[b["source"]], "locator": f"{locator}; {', '.join(b['crossing_periods'])}",
            "note": b["reason"], "uncertainty": on["flag"] or "clear", "money": money, "frame": "b",
            "route": on["route"], "entry_date": crossing, "entry_measure": f"{b['pi']:.4f}",
            "entry_measure_date": crossing, "outcome": "restored" if b["restored"] else "not restored by the common end",
            "outcome_date": b["restored"], "onset_date": "", "responses": "", "exit": "", "status": b["status"],
            "coder": CODER, "rules_sha256": sha, "break_onset": on["label"], "onset_route": on["route"],
            "onset_flag": on["flag"], "onset_unknown_routes": ";".join(on["unknown"]), "onset_d_anchor": anchor,
            "onset_pi_only": _pi_only_label(b["pi_only"]), "frequency": "monthly" if b["freq"] == "M" else "annual",
            "line_pct": f"{p.line:g}", "crossing_periods": " ".join(b["crossing_periods"]), "price_basis": basis,
            "rr_basis_kind": kind, "rr_basis_seam": seam, "stretch_begins": b.get("stretch_begins", ""),
            "first_reading_at_line": crossing, "first_public_crossing": "cannot be read",
            "public_by_convention": public_by_convention(crossing),
            "regime_at_crossing": f"{cls} ({P.regime_group(cls)})" if cls else "cannot be read", "regime_note": note,
            "split_at_crossing": P.split_at(money, crossing), "seams": _seams_in(tl, b, p),
            "ifs_break": "yes" if b["ifs_break"] else "no",
            "shared_or_foreign_money": "cannot be read" if cls is None else ("yes" if cls == 1 else "no"),
            "new_money_rule": "not applied", "variant": variant,
        })
    return out


def _last_run_start(have: dict, step: int) -> int | None:
    """The first failing period of the latest run of failing periods (for the end-at-first-failure variant)."""
    def fails(t):
        before = have.get(t - step, set())
        return bool(before) and len(before & have.get(t, set())) < 0.5 * len(before)
    t = max(have)
    while t >= min(have) and not fails(t):
        t -= 1
    while t - 1 >= min(have) and fails(t - 1):
        t -= 1
    return t


def build() -> dict:
    import m0
    import panel as P
    sha = m0.require_locked()
    pan = P.Panel()
    have_m, have_a = pan.have_monthly(), pan.have_annual()
    end_m, end_a = P.common_end(have_m, 12), P.common_end(have_a, 1)
    end_m_alt = _last_run_start(have_m, 12) - 1
    lists: dict[str, list[dict]] = {"headline": []}
    for name in VARIANTS:
        lists[name] = []
    lists["common-end-before-the-last-failing-run"] = []
    for money in pan.monies:
        pm, pa, dm, da = pan.pi_monthly(money), pan.pi_annual(money), pan.d_monthly(money), pan.d_annual(money)
        tl = P.timeline(money, pm, pa, dm, da, end_m, end_a)
        lists["headline"] += rows_for(pan, money, tl, HEADLINE, "headline", sha)
        for name, params in VARIANTS.items():
            lists[name] += rows_for(pan, money, tl, params, name, sha)
        tl_alt = P.timeline(money, pm, pa, dm, da, end_m_alt, end_a)
        lists["common-end-before-the-last-failing-run"] += rows_for(
            pan, money, tl_alt, HEADLINE, "common-end-before-the-last-failing-run", sha)
    out = P.DATA / "reconstructed" / "ft001-b"
    out.mkdir(parents=True, exist_ok=True)
    import csv
    for name, rows in lists.items():
        target = out / ("series.csv" if name == "headline" else f"variant-{name}.csv")
        with open(target, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="raise")
            w.writeheader()
            w.writerows(sorted(rows, key=lambda r: (r["money"], r["period"])))
    coverage, seam_rows, digest = P.records(pan)
    for name, rows, fields in (("panel-coverage.csv", coverage, ["money", "item", "source", "first", "last", "readings"]),
                               ("panel-seams.csv", seam_rows, ["money", "item", "period", "from", "to"])):
        with open(out / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
    return {"lists": lists, "end_m": month_label(end_m), "end_a": end_a, "end_m_alt": month_label(end_m_alt),
            "digest": digest, "monies": len(pan.monies), "seams": len(seam_rows), "coverage": coverage,
            "unread": {k: sorted(v) for k, v in P.UNREAD_AREAS.items()}, "self_anchored": sorted(pan.self_anchored),
            "sha": sha}


def build_rr_cpi_only() -> list[dict]:
    """The variant ``rr-cpi-only`` alone (the session's decision, after the headline's counts were seen): the
    headline's machinery, with a Reinhart-Rogoff year whose "Based on" block names no consumer price index read
    as *cannot be read* for π. Written to ``variant-rr-cpi-only.csv``; the headline and other variants untouched."""
    import csv
    import m0
    import panel as P
    sha = m0.require_locked()
    pan = P.Panel()
    end_m, end_a = P.common_end(pan.have_monthly(), 12), P.common_end(pan.have_annual(), 1)
    rows: list[dict] = []
    for money in pan.monies:
        tl = P.timeline(money, pan.pi_monthly(money), pan.pi_annual(money, rr_cpi_only=True), pan.d_monthly(money),
                        pan.d_annual(money), end_m, end_a)
        rows += rows_for(pan, money, tl, HEADLINE, "rr-cpi-only", sha)
    target = P.DATA / "reconstructed" / "ft001-b" / "variant-rr-cpi-only.csv"
    with open(target, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="raise")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["money"], r["period"])))
    return rows


if __name__ == "__main__":
    import sys
    if sys.argv[1:2] == ["build"] and sys.argv[2:4] == ["--only", "rr-cpi-only"]:
        print(len(build_rr_cpi_only()), "lines")
    elif sys.argv[1:2] == ["build"]:
        result = build()
        build_rr_cpi_only()
        print({k: len(v) for k, v in result["lists"].items()})
    else:
        print(__doc__)
        sys.exit(2)
