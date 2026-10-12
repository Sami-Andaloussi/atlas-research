"""Card C24 (CS-C, its years): the share of money-years in which prices rose a fifth (20%) or more, in C23's three spans,
beside C23's crises begun.

From the study's folder: ``python code/p1_cs_c_years.py``. Writes ``results/runs/C24-cs-c-years-in-crisis.json``.

The denominator is C23's, read from ``p1_cs_c.py`` (``reading_years``, ``Units``), never changed: each unit-year once. A
year's rise is the timeline's annual reading for the year, else the mean of its monthly 12-month changes; a unit-year
read by several economies takes the mean of their rises. The run stops if a span's money-years differ from C23's.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ft import cards

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p1_cs_c as C  # noqa: E402

STUDY = C.STUDY
CARD = STUDY / "cards" / "C24-cs-c-years-in-crisis.yaml"
C23_RUN = STUDY / "results" / "runs" / "C23-cs-c-losses-by-era.json"


def year_rises(pan, money: str, ends: tuple[int, int], rr_cpi_only: bool, y0: int, y1: int) -> dict[int, float]:
    tl = C.P.timeline(money, pan.pi_monthly(money), pan.pi_annual(money, rr_cpi_only=rr_cpi_only), {}, {}, *ends)
    annual: dict[int, float] = {}
    monthly: dict[int, list[float]] = {}
    for q in tl:
        if q.pi is None:
            continue
        y = int(q.label[:4])
        if not y0 <= y <= y1:
            continue
        if len(q.label) == 4:
            annual[y] = q.pi
        else:
            monthly.setdefault(y, []).append(q.pi)
    out = {y: sum(v) / len(v) for y, v in monthly.items()}
    out.update(annual)
    return out


def count(pan, units, ends, rr_cpi_only: bool, line: float, c23_spans: dict) -> dict:
    y0, y1 = units.p["years"]
    rises: dict[tuple[str, int], list[float]] = {}
    for money in pan.monies:
        yr = year_rises(pan, money, ends, rr_cpi_only, y0, y1)
        for y in C.reading_years(pan, money, *ends, rr_cpi_only, y0, y1):
            u = units.of(money, y)
            if u is None or y not in yr:
                continue
            rises.setdefault((u, y), []).append(yr[y])
    out = {}
    for s in C.SPANS:
        cells = [sum(v) / len(v) for (u, y), v in rises.items() if C.span_of_year(y) == s]
        crisis = sum(1 for r in cells if r >= line)
        out[s] = {"money_years": len(cells), "crisis_years": crisis,
                  "share_pct": round(100 * crisis / len(cells), 1) if cells else None,
                  "c23_money_years": c23_spans[s]["money_years"], "c23_rate_per_100": c23_spans[s]["rate_per_100"],
                  "c23_events": c23_spans[s]["events"]}
        if len(cells) != c23_spans[s]["money_years"]:
            raise SystemExit(f"C24: {s} has {len(cells)} money-years, C23 printed {c23_spans[s]['money_years']}")
    return out


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    c23card = cards.read(C.CARD)
    p = c23card["parameters"]
    line = float(card["parameters"]["line_percent"])
    pan = C.P.Panel()
    digest = C.P.records(pan)[2]
    expected = p["panel"].split("digest ")[1].rstrip(")")
    if digest != expected:
        raise SystemExit(f"C24: the rebuilt panel's digest {digest} differs from C23's {expected}")
    ends = (C.P.common_end(pan.have_monthly(), 12), C.P.common_end(pan.have_annual(), 1))
    units = C.Units(p)
    c23 = json.loads(C23_RUN.read_text())["result"]
    payload = {"panel_digest": digest, "line_percent": line,
               "headline": count(pan, units, ends, False, line, c23["headline"]["spans"]),
               "rr_cpi_only": count(pan, units, ends, True, line, c23["rr_cpi_only"]["spans"])}
    cards.write_result(STUDY, CARD, payload)
    return payload


if __name__ == "__main__":
    print(json.dumps(main(), indent=1)[:1500])
