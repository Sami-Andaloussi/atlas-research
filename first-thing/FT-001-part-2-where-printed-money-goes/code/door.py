"""The door: card C01 - how much base money the US added in its two printings, per year and in total,
and how much prices rose.

From the study's folder: ``../../toolkit/bin/ftpy code/door.py``. Writes ``results/runs/C01-door.json``.
The monthly paths from each start (base added as a share of the start year's GDP, prices since the start)
are written for the door's figure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

from ft import cards  # noqa: E402

CARD = K.CARDS / "C01-door.yaml"
CHECK = {"base": {"2008-08": 847.6, "2014-10": 4001.5, "2020-02": 3454.5, "2021-12": 6413.1},
         "gdp": {2008: 14769.9, 2020: 21375.3}}
DOSSIER = {  # the dossier's rates (section 4), each checked to 0.1 point (C01's failure clause)
    "W1": {"base_growth_pa": 29, "added_share_pa": 3.5, "added_share_total": 21.4, "prices_pa": 1.3, "prices_total": 8.6},
    "W2": {"base_growth_pa": 40, "added_share_pa": 7.5, "added_share_total": 13.8, "prices_pa": 4.5, "prices_total": 8.3},
    "W1-22": {"prices_pa": -0.4},
}


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    B = K.fred_monthly("BOGMBASE")
    P = K.fred_monthly("CPIAUCSL", "2026-09-27")
    G = K.fred_series("GDP")
    G = G.groupby(G.index.year).mean()
    out = {"windows": {}, "levels": {}, "paths": {}}
    for name, (s, e) in card["parameters"]["windows"].items():
        s, e = pd.Period(str(s), "M"), pd.Period(str(e), "M")
        n = (e - s).n
        g = float(G[s.year])
        added = float(B[e] - B[s])
        w = {"start": str(s), "end": str(e), "months": n, "B_start_bn": float(B[s]), "B_end_bn": float(B[e]),
             "P_start": float(P[s]), "P_end": float(P[e]), "gdp_start_year_bn": g, "gdp_year": s.year,
             "base_growth_pa": 100 * ((B[e] / B[s]) ** (12 / n) - 1), "added_bn": added,
             "added_share_total": 100 * added / g, "added_share_pa": 100 * added / g * 12 / n,
             "prices_total": 100 * (P[e] / P[s] - 1), "prices_pa": 100 * ((P[e] / P[s]) ** (12 / n) - 1),
             "multiple": float(B[e] / B[s])}
        w["price_per_printing"] = w["prices_pa"] / w["added_share_pa"]
        out["windows"][name] = w
        months = pd.period_range(s, e, freq="M")
        out["paths"][name] = {"months_since_start": [(m - s).n for m in months],
                              "added_share": [100 * float(B[m] - B[s]) / g for m in months],
                              "prices_since_start": [100 * float(P[m] / P[s] - 1) for m in months]}
    W1, W2 = out["windows"]["W1"], out["windows"]["W2"]
    out["ratios_W2_over_W1"] = {k: W2[k] / W1[k] for k in ("base_growth_pa", "added_share_pa", "added_share_total",
                                                           "prices_pa", "prices_total", "added_bn",
                                                           "price_per_printing")}
    out["ratios_W2_over_W1_22"] = {k: W2[k] / out["windows"]["W1-22"][k] for k in ("added_share_total",)}
    repro = {"base": {m: {"check": v, "frozen": round(float(B[pd.Period(m, 'M')]), 1)} for m, v in CHECK["base"].items()},
             "gdp": {str(y): {"check": v, "frozen": round(float(G[y]), 1)} for y, v in CHECK["gdp"].items()}}
    ok = all(abs(x["check"] - x["frozen"]) <= 0.1 for part in repro.values() for x in part.values())
    diffs = {}
    for name, rates in DOSSIER.items():
        for k, v in rates.items():
            got = out["windows"][name][k]
            diffs[f"{name} {k}"] = {"dossier": v, "run": round(got, 2), "within": bool(abs(round(got, 1) - v) <= 0.1 + 1e-9)}
    out["reproduction"] = {"levels": repro, "levels_reproduce": ok, "against_the_dossier": diffs,
                           "dossier_holds": all(d["within"] for d in diffs.values())}
    path = cards.write_result(K.STUDY, CARD, out)
    print(path)
    return path


if __name__ == "__main__":
    main()
