"""Card C37 (CS-F): money (M2), real output (real GDP) and prices (the GDP deflator) in the United States since 1959, as an
identity in logs, velocity the residual.

From the study's folder: ``python code/p2_cs_f.py``. Writes ``results/runs/C37-cs-f-money-output-prices.json``.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

from ft import cards
from ft.data import fred
from ft.data import agency

STUDY = Path(__file__).resolve().parents[1]
CARD = STUDY / "cards" / "C37-cs-f-money-output-prices.yaml"


def quarterly(s: pd.Series) -> pd.Series:
    s = s.dropna()
    s.index = pd.PeriodIndex(pd.to_datetime(s.index), freq="Q")
    return s.groupby(level=0).mean()


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    v = card["parameters"]["vintage"]
    m2 = agency.series("M2SL", v).dropna()
    m2.index = pd.to_datetime(m2.index)
    m2 = m2.groupby(pd.PeriodIndex(m2.index, freq="Q")).agg(["mean", "count"])
    m2 = m2[m2["count"] == 3]["mean"]  # a quarter with its three months only
    y, p, gdp = (quarterly(agency.series(c, v)) for c in ("GDPC1", "GDPDEF", "GDP"))
    common = m2.index.intersection(y.index).intersection(p.index).intersection(gdp.index)
    bad = 0
    for q in common:
        tol = y[q] * 0.0005 / 100 + p[q] * 0.0005 / 100 + 0.0005
        if abs(y[q] * p[q] / 100 - gdp[q]) > tol:
            bad += 1
    if bad:
        raise SystemExit(f"C37: nominal GDP computed here differs from FRED's GDP beyond the inputs' rounding in {bad} quarters")
    q4 = sorted(q for q in common if q.quarter == 4)
    first, last = q4[0].year, q4[-1].year
    if first != 1959:
        raise SystemExit(f"C37: the first fourth quarter with all series is {first}, not 1959")

    def growth(a: int, b: int) -> dict:
        qa, qb = pd.Period(f"{a}Q4"), pd.Period(f"{b}Q4")
        g = lambda s: 100 * (math.log(s[qb]) - math.log(s[qa])) / (b - a)  # noqa: E731
        nom = lambda q: y[q] * p[q] / 100  # noqa: E731
        money, real, prices = g(m2), g(y), g(p)
        velocity = 100 * ((math.log(nom(qb)) - math.log(m2[qb])) - (math.log(nom(qa)) - math.log(m2[qa]))) / (b - a)
        if abs(money - (real + prices - velocity)) > 1e-9:
            raise SystemExit("C37: the identity does not close")
        return {"from": f"{a}Q4", "to": f"{b}Q4", "money": round(money, 2), "real_output": round(real, 2),
                "prices": round(prices, 2), "velocity": round(velocity, 2)}

    spans = {f"1959-{last}": growth(1959, last)}
    a = 1959
    while a < last:
        b = min(a + 10, last)
        spans[f"{a}-{b}"] = growth(a, b)
        a = b
    payload = {"spans": spans, "quarters_checked_against_gdp": len(common), "latest_full_year": last}
    cards.write_result(STUDY, CARD, payload)
    return payload


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
