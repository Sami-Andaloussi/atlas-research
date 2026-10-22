"""Card C28 (C26 rerun, 2026-10-22: the price panel with Kazakhstan's splice alone, ft.data.splices; C23's rules unchanged) (CS-C): how often prices rose a fifth (20%) or more in a year, 1800-2025, per 100 money-years with a price reading, in
three spans named by their dates, from frame b's breaks (M3, M0 v4.2), the euro and each union counted once.

From the study's folder: ``python code/p1_cs_c.py``. Writes ``results/runs/C28-cs-c-losses-by-era-kazakhstan.json``.

The panel is frame b's, rebuilt in memory from the frozen sources by frame b's own code (``panel.py``, read, never
changed), its digest checked against the manifest's before anything is counted. Readings of the card that its text
leaves to the code, fixed here before the run:

- *The class of a year*: IRR's fine class of the calendar year itself (the sheet Fine), an integer 1 to 15, or none
  (no column, a year before 1946 or outside the column's start and end years, an empty or non-integer cell); a year
  after 2016 takes 2016's.
- *A year with a reading*: a year of the timeline (``panel.timeline``, frame b's common ends) holding an annual price
  reading, or a month of the year holding a monthly 12-month reading.
- *A union's window*: months counted between entry months; a crossing joins when the difference is 0 to 12.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from ft import cards

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
CARD = STUDY / "cards" / "C28-cs-c-losses-by-era-kazakhstan.yaml"  # C26 rerun, Kazakhstan alone (2026-10-22)
FRAME_B = ROOT / "data" / "reconstructed" / "ft001-b"
sys.path.insert(0, str(ROOT / "bank" / "maps" / "FT-001" / "missions" / "code"))

import panel as P  # noqa: E402

SPANS = ("before_1914", "1914_to_1971_07", "from_1971_08")


def span_of_entry(entry: str) -> str:
    y = int(entry[:4])
    if y < 1914:
        return SPANS[0]
    if len(entry) == 4:
        return SPANS[1] if y <= 1971 else SPANS[2]
    return SPANS[1] if (y < 1971 or (y == 1971 and int(entry[5:7]) <= 7)) else SPANS[2]


def span_of_year(y: int) -> str:
    return SPANS[0] if y < 1914 else (SPANS[1] if y <= 1971 else SPANS[2])


class Units:
    """The unit of money an economy-year belongs to (the card's method (3)); None for another state's money."""

    def __init__(self, p: dict) -> None:
        self.p = p
        self.irr = P.irr_classes()
        self.union_of = {m: u for u, ms in p["unions"].items() for m in ms}

    def cls(self, money: str, year: int) -> int | None:
        r = self.irr.get(money)
        if r is None or year < 1946:
            return None
        y = min(year, self.p["irr_carry_after"])
        if r["start"] is None or r["end"] is None or not r["start"] <= y <= r["end"]:
            return None
        v = r["classes"].get(y)
        return int(v) if isinstance(v, float) and v == int(v) and 1 <= v <= 15 else None

    def of(self, money: str, year: int) -> str | None:
        p = self.p
        if money == p["euro_unit"]:
            return money
        if money in p["euro_entry"] and year >= p["euro_entry"][money]:
            return p["euro_unit"]
        union = self.union_of.get(money)
        if union is not None and p["union_without_irr"].get(money) == union:
            return union
        if money in p["foreign_without_irr"]:
            return None
        own_from = p["own_despite_class_1"].get(money)
        if self.cls(money, year) == p["irr_class_shared"] and not (own_from is not None and year >= own_from):
            return union  # a union member's year is the union's; any other's is another state's money (None)
        return money


def reading_years(pan, money: str, end_m: int, end_a: int, rr_cpi_only: bool, y0: int, y1: int) -> set[int]:
    tl = P.timeline(money, pan.pi_monthly(money), pan.pi_annual(money, rr_cpi_only=rr_cpi_only), {}, {}, end_m, end_a)
    return {y for y in (int(q.label[:4]) for q in tl if q.pi is not None) if y0 <= y <= y1}


def month_no(entry: str, annual_month: int) -> int:
    y = int(entry[:4])
    return y * 12 + ((int(entry[5:7]) if len(entry) == 7 else annual_month) - 1)


def count(series: Path, pan, units: Units, ends: tuple[int, int], rr_cpi_only: bool) -> dict:
    p = units.p
    y0, y1 = p["years"]
    rows = list(csv.DictReader(series.open(newline="", encoding="utf-8")))
    apart = [{"money": r["money"], "entry": r["entry_date"], "why": r["note"], "span": span_of_entry(r["entry_date"])}
             for r in rows if r["status"] == "apart"]
    set_apart, events, by_union = [], [], {}
    for r in rows:
        if r["status"] != "counted":
            continue
        u = units.of(r["money"], int(r["entry_date"][:4]))
        if u is None:
            set_apart.append({"money": r["money"], "entry": r["entry_date"], "span": span_of_entry(r["entry_date"]),
                              "class": units.cls(r["money"], int(r["entry_date"][:4])),
                              "why": p["set_apart_reason"]})
        elif u in p["unions"]:
            by_union.setdefault(u, []).append(r)
        else:
            events.append({"units": [u], "entry": r["entry_date"], "rows": [r["money"]]})
    lo, hi = (month_no(d, 1) for d in p["cfa_1994_decision"])
    cfa = []
    for u, rs in sorted(by_union.items()):
        rs.sort(key=lambda r: month_no(r["entry_date"], p["annual_entry_month_for_window"]))
        current = None
        for r in rs:
            m = month_no(r["entry_date"], p["annual_entry_month_for_window"])
            if u in ("XOF", "XAF") and lo <= m <= hi:
                cfa.append((u, r["money"], r["entry_date"]))
                continue
            if current is not None and 0 <= m - current["_open"] <= p["union_window_months"]:
                current["rows"].append(r["money"])
                continue
            current = {"units": [u], "entry": r["entry_date"], "rows": [r["money"]], "_open": m}
            events.append(current)
    if cfa:
        events.append({"units": sorted({u for u, _, _ in cfa}), "entry": min(e for _, _, e in cfa),
                       "rows": sorted(m for _, m, _ in cfa), "decision": "CFA francs devalued, 12 January 1994"})
    for e in events:
        e.pop("_open", None)
    # the denominator
    years: dict[str, set[int]] = {}
    other_years: dict[str, list[int]] = {}
    elsewhere: dict[str, set[int]] = {}  # years an economy read that belong to another unit, or to none
    for money in pan.monies:
        for y in sorted(reading_years(pan, money, *ends, rr_cpi_only, y0, y1)):
            u = units.of(money, y)
            if u is None:
                other_years.setdefault(money, []).append(y)
            else:
                years.setdefault(u, set()).add(y)
            if u != money:
                elsewhere.setdefault(money, set()).add(y)
    no_irr = sorted(m for m in pan.monies if m not in units.irr and m != p["euro_unit"]
                    and m not in p["union_without_irr"] and any(reading_years(pan, m, *ends, rr_cpi_only, y0, y1)))
    out = {}
    for s in SPANS:
        ev = [e for e in events if span_of_entry(e["entry"]) == s]
        my = sum(1 for ys in years.values() for y in ys if span_of_year(y) == s)
        gaps = sum(1 for u, ys in years.items() for y in range(min(ys), max(ys) + 1)
                   if y not in ys and y not in elsewhere.get(u, set()) and span_of_year(y) == s)
        with_reading = {u for u, ys in years.items() if any(span_of_year(y) == s for y in ys)}
        hit = {u for e in ev for u in e["units"]} & with_reading
        out[s] = {"events": len(ev), "rows": sum(len(e["rows"]) for e in ev), "money_years": my,
                  "years_without_reading_inside_spans": gaps,
                  "rate_per_100": round(p["per"] * len(ev) / my, p["decimals"]) if my else None,
                  "units_with_reading": len(with_reading),
                  "share_with_event": round(len(hit) / len(with_reading), 2) if with_reading else None,
                  "apart": [a for a in apart if a["span"] == s],
                  "set_apart_another_states_money": [a for a in set_apart if a["span"] == s],
                  "another_states_money_years": sum(1 for ys in other_years.values() for y in ys
                                                    if span_of_year(y) == s)}
    listed = set(p["no_irr_own"]) | set(p["foreign_without_irr"])
    return {"spans": out, "events": sorted(events, key=lambda e: e["entry"]),
            "no_irr_with_readings": no_irr, "no_irr_matches_card": no_irr == sorted(listed),
            "no_irr_own_years": {m: sorted(years.get(m, set())) for m in no_irr if m in p["no_irr_own"]},
            "another_states_money_years_by_economy": {m: [ys[0], ys[-1], len(ys)] for m, ys in other_years.items()}}


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    p = card["parameters"]
    pan = P.Panel()
    digest = P.records(pan)[2]
    expected = p["panel"].split("digest ")[1].rstrip(")")
    if digest != expected:
        raise SystemExit(f"C28: the rebuilt panel's digest {digest} differs from the manifest's {expected}")
    ends = (P.common_end(pan.have_monthly(), 12), P.common_end(pan.have_annual(), 1))
    units = Units(p)
    payload = {"panel_digest": digest, "common_ends": {"monthly": P.month_label(ends[0]), "annual": ends[1]},
               "headline": count(FRAME_B / "series.csv", pan, units, ends, rr_cpi_only=False),
               "rr_cpi_only": count(FRAME_B / "variant-rr-cpi-only.csv", pan, units, ends, rr_cpi_only=True)}
    cards.write_result(STUDY, CARD, payload)
    return payload


if __name__ == "__main__":
    main()
