"""Card C22 (CS-B): the Swiss franc at home and abroad since 1971, its rise split in logs into the inflation gap and the
real rise; Switzerland's price level against its neighbours'; exports beside the real rate.

From the study's folder: ``python code/p1_cs_b.py``. Writes ``results/runs/C22-cs-b-the-franc.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *A reading*: a BIS row with a number in OBS_VALUE ("NaN" is none); a World Bank row with a non-null value.
- *The dollar per franc*: 1 / (francs per dollar), from WS_XRU's annual average (FREQ A, collection A).
- *A year of the effective rates*: the mean of its twelve monthly readings; a year with fewer than twelve is left out
  of the split and named.
- *A split*: in log points (100 times the natural log), its two parts and their sum; a share of the total is printed
  only when the total exceeds one log point in size and both parts have its sign (the card), else "no share".
- *The price level*: PA.NUS.PPP over PA.NUS.FCRF for each country and year both exist; Switzerland's over each
  neighbour's; the latest year with all five.
"""

from __future__ import annotations

import csv
import io
import json
import math
import zipfile
from pathlib import Path

from ft import cards
from ft.data import freeze

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
CARD = STUDY / "cards" / "C22-cs-b-the-franc.yaml"


def _bis_rows(dataset: str, vintage: str, zipname: str):
    z = zipfile.ZipFile(io.BytesIO(freeze.load(dataset, vintage).read_bytes(zipname)))
    with z.open(z.namelist()[0]) as fh:
        for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8")):
            r = {k.split(":")[0]: (v.split(":")[0] if k.split(":")[0] not in ("OBS_VALUE", "TIME_PERIOD") else v)
                 for k, v in row.items()}
            try:
                v = float(r["OBS_VALUE"])
            except ValueError:
                continue
            if math.isnan(v):
                continue
            r["v"] = v
            yield r


def xru_usd_per_chf() -> dict[int, float]:
    return {int(r["TIME_PERIOD"]): 1 / r["v"] for r in _bis_rows("bis/WS_XRU", "2026-10-10", "WS_XRU_csv_flat.zip")
            if r["REF_AREA"] == "CH" and r["FREQ"] == "A" and r["COLLECTION"] == "A"}


def cpi(area: str) -> dict[int, float]:
    return {int(r["TIME_PERIOD"]): r["v"] for r in _bis_rows("bis/WS_LONG_CPI", "2026-09-30", "WS_LONG_CPI_csv_flat.zip")
            if r["REF_AREA"] == area and r["FREQ"] == "A" and r["UNIT_MEASURE"] == "628"}


def eer(kind: str, basket: str) -> tuple[dict[int, float], list[int]]:
    months: dict[int, list[float]] = {}
    for r in _bis_rows("bis/WS_EER", "2026-10-10", "WS_EER_csv_flat.zip"):
        if r["REF_AREA"] == "CH" and r["FREQ"] == "M" and r["EER_TYPE"] == kind and r["EER_BASKET"] == basket:
            months.setdefault(int(r["TIME_PERIOD"][:4]), []).append(r["v"])
    full = {y: sum(v) / len(v) for y, v in months.items() if len(v) == 12}
    return full, sorted(y for y, v in months.items() if len(v) != 12)


def wdi(indicator: str) -> dict[tuple[str, int], float]:
    rows = json.loads(freeze.load(f"worldbank/{indicator}", "2026-10-10").read_bytes("page-001.json"))[1]
    return {(r["countryiso3code"], int(r["date"])): r["value"] for r in rows if r["value"] is not None}


def lp(a: float, b: float) -> float:
    return 100 * math.log(a / b)


def split(nominal: dict[int, float], real: dict[int, float], b: int, e: int) -> dict | None:
    if not all(y in d for d in (nominal, real) for y in (b, e)):
        return None
    total, real_rise = lp(nominal[e], nominal[b]), lp(real[e], real[b])
    gap = total - real_rise
    out = {"base": b, "end": e, "total_log_points": round(total, 1), "inflation_gap_log_points": round(gap, 1),
           "real_rise_log_points": round(real_rise, 1)}
    if abs(total) > 1 and gap * total > 0 and real_rise * total > 0:
        out["inflation_gap_share"] = round(gap / total, 2)
        out["real_rise_share"] = round(real_rise / total, 2)
    else:
        out["share"] = "no share"
    return out


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    p = card["parameters"]
    b0, e0 = p["base_year"], p["end_year"]
    spans = [[b0, e0]] + [[s - 1, e] for s, e in p["stretches"]]
    x, pch, pus = xru_usd_per_chf(), cpi("CH"), cpi("US")
    real_bil = {y: x[y] * pch[y] / pus[y] for y in x if y in pch and y in pus}
    bilateral = [split(x, real_bil, b, e) for b, e in spans]
    eff = {}
    for basket in (p["eer"]["main_basket"], p["eer"]["beside_basket"]):
        n, n_short = eer("N", basket)
        r, r_short = eer("R", basket)
        first = max(min(n), min(r))
        eff[basket] = {"first_full_year": first, "short_years": sorted(set(n_short) | set(r_short)),
                       "splits": [split(n, r, max(b, first), e) for b, e in spans if e > max(b, first)],
                       "real_index": {y: round(v, 2) for y, v in sorted(r.items()) if y >= b0}}
    ppp, fcrf = wdi("PA.NUS.PPP"), wdi("PA.NUS.FCRF")
    cs = p["price_level"]["countries"]
    level = {c: {y: ppp[(c, y)] / fcrf[(c, y)] for (cc, y) in ppp if cc == c and (c, y) in fcrf} for c in cs}
    common = sorted(set.intersection(*(set(v) for v in level.values())))
    latest = common[-1] if common else None
    ratios = ({c: round(level["CHE"][latest] / level[c][latest], 2) for c in cs if c != "CHE"} if latest else {})
    exports = {y: round(v, 1) for (c, y), v in wdi("NE.EXP.GNFS.ZS").items() if c == "CHE" and y >= b0 + 1}
    def index(d: dict[int, float], b: int) -> dict[int, float]:
        return {y: round(100 * v / d[b], 2) for y, v in sorted(d.items()) if y >= b} if b in d else {}

    n_main, _ = eer("N", p["eer"]["main_basket"])
    r_main, _ = eer("R", p["eer"]["main_basket"])
    series = {"usd": {"nominal": index(x, b0), "real": index(real_bil, b0)},
              "narrow": {"nominal": index(n_main, b0), "real": index(r_main, b0)}}
    payload = {"bilateral_usd": bilateral, "effective": eff, "series_1970_100": series,
               "price_level": {"latest_common_year": latest, "che_over_neighbour": ratios,
                               "series": {c: {y: round(v, 3) for y, v in sorted(d.items())} for c, d in level.items()}},
               "exports_pct_gdp": exports, "floor": p["floor"]}
    cards.write_result(STUDY, CARD, payload)
    return payload


if __name__ == "__main__":
    main()
