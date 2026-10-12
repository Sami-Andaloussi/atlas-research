"""Card C21 (CS-A): what one unit of the dollar, the pound, the franc, the yen and the euro's monies bought each year
since 1914, and its yearly loss in four periods fixed on the card (the BIS long consumer-price series).

From the study's folder: ``python code/p1_cs_a.py``. Writes ``results/runs/C21-cs-a-what-a-unit-buys.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *A reading*: a row of the BIS file with FREQ A, unit 628 and a number in OBS_VALUE; a row holding "NaN" is no reading.
- *A period's base*: the year before the period, or the money's own first year on the card when later; a period whose
  base or end has no reading is "not computable" and printed so, never filled.
- *A period outside a money's span* (ending before the money's first year, or after its last): printed as outside
  the span, never computed (the Reichsmark, 1924-1947, has 1914-1945 only).
- *A loss or a gain*: the yearly loss is kept with its sign; ``direction`` says "gain" where it is negative.
- *The euro area beside*: its loss is computed for 1992-2025 only (base 1991), the one period it covers whole, and the
  gap to each euro carrier is the carrier's yearly loss less the euro area's, in points.
- *The grid*: one row per money and year t of its span, the value in 2025 of one unit of year t, in today's unit; the
  Reichsmark's, not chained across 1948, gives what one Reichsmark of year t bought in 1947, in 1947 Reichsmarks.
"""

from __future__ import annotations

import csv
import io
import math
import zipfile
from pathlib import Path

from ft import cards
from ft.data import freeze

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
CARD = STUDY / "cards" / "C21-cs-a-what-a-unit-buys.yaml"


def bis_annual(card: dict) -> dict[str, dict[int, float]]:
    """{area: {year: index}} for the card's areas, FREQ A, unit 628, readings only."""
    p = card["parameters"]
    ds, vintage = p["dataset"].split()
    raw = freeze.load(ds, vintage).read_bytes("WS_LONG_CPI_csv_flat.zip")
    z = zipfile.ZipFile(io.BytesIO(raw))
    areas = {m["area"] for m in p["monies"].values()}
    out: dict[str, dict[int, float]] = {a: {} for a in areas}
    with z.open(z.namelist()[0]) as fh:
        for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8")):
            area = row["REF_AREA:Reference area"].split(":")[0]
            if area not in areas or not row["FREQ:Frequency"].startswith(p["freq"] + ":"):
                continue
            if not row["UNIT_MEASURE:Unit of measure"].startswith(p["unit_measure"] + ":"):
                continue
            try:
                v = float(row["OBS_VALUE:Observation Value"])
            except ValueError:
                continue
            if math.isnan(v):
                continue
            out[area][int(row["TIME_PERIOD:Time period or range"])] = v
    return out


def yearly_loss(index: dict[int, float], base: int, end: int) -> float | None:
    if base not in index or end not in index or end <= base:
        return None
    return 100 * (1 - (index[base] / index[end]) ** (1 / (end - base)))


def to_2025_factor(money: str, year: int, factors: dict) -> float:
    """Units of today's money one unit of `year`'s money converts into, by the official factors (index ratio apart)."""
    f = 1.0
    if money.startswith("FRF"):
        if year < 1960:
            f /= factors["FRF_old_to_new_1960"]
        if year < 1999:
            f /= factors["FRF_per_euro_1999"]
    if money.startswith("DEM") and year < 1999:
        f /= factors["DEM_per_euro_1999"]
    return f


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    p = card["parameters"]
    bis = bis_annual(card)
    excluded = {(e.split()[0], int(e.split()[1])) for e in p["excluded"]}
    monies = {}
    for name, m in p["monies"].items():
        idx = {y: v for y, v in bis[m["area"]].items()
               if m["from"] <= y <= m["to"] and (m["area"], y) not in excluded}
        first = min(idx) if idx else None
        periods = []
        for start, end in p["periods"]:
            base = max(start - 1, m["from"])
            last = min(end, m["to"])
            if name == "euro_area_beside" and (start, end) != (1992, 2025):
                continue
            if last <= base or m["to"] < end:
                periods.append({"period": [start, end], "outside_span": True})
                continue
            loss = yearly_loss(idx, base, last)
            row = {"period": [start, end], "base": base, "end": last,
                   "yearly_loss_pct": None if loss is None else round(loss, 1),
                   "direction": None if loss is None else ("gain" if loss < 0 else "loss"),
                   "computable": loss is not None,
                   "price_ratio": None if loss is None else idx[last] / idx[base]}
            if loss is not None and name not in ("euro_area_beside", "Reichsmark") and 2025 in idx:
                row["value_2025_of_one_base_unit"] = (idx[2025] / idx[base]
                                                      * to_2025_factor(name, base, p["conversion_factors"]))
            periods.append(row)
        grid = []
        if name == "Reichsmark":
            # not chained across the 1948 reform: what one Reichsmark of year t bought in 1947, in 1947 Reichsmarks
            grid = [{"year": y, "units_of_1947": idx[1947] / idx[y]} for y in sorted(idx)] if 1947 in idx else []
        elif name != "euro_area_beside" and 2025 in idx:
            grid = [{"year": y, "today_units": idx[2025] / idx[y] * to_2025_factor(name, y, p["conversion_factors"])}
                    for y in sorted(idx)]
        monies[name] = {"area": m["area"], "first_reading": first, "last_reading": max(idx) if idx else None,
                        "periods": periods, "grid": grid}
    # the euro area beside each carrier, 1992-2025
    xm = next(r for r in monies["euro_area_beside"]["periods"] if r["period"] == [1992, 2025])
    gaps = {}
    for carrier in ("FRF_then_euro_in_France", "DEM_then_euro_in_Germany"):
        c = next(r for r in monies[carrier]["periods"] if r["period"] == [1992, 2025])
        if c.get("computable") and xm.get("computable"):
            gaps[carrier] = round(c["yearly_loss_pct"] - xm["yearly_loss_pct"], 1)
    payload = {"monies": monies, "euro_area_gap_points": gaps}
    cards.write_result(STUDY, CARD, payload)
    return payload


if __name__ == "__main__":
    main()
