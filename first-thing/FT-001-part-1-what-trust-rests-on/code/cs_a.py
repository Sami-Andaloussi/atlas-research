"""Card C18 (CS-A): on consumer prices, did the economies Bernanke & James count as off gold have more inflation in
1932-34 than those still on it, by their dates?

From the study's folder: ``../../toolkit/bin/ftpy code/cs_a.py``. Writes ``results/runs/C18-cs-a-consumer-prices-off-gold.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *A date of Table 2.1*: its month (``series.csv``'s period ``YYYY-MM``); France's return, printed as a range, takes
  the range's end (June 1928), as the transcription's period does.
- *A month off gold*: on or after the first act's month; also any month before the economy's return to gold.
- *The variant without exchange control*: the months from an exchange control to the economy's first suspension or
  devaluation weigh nothing in either group (an economy with neither is dropped from its exchange control on).
- *The calibration*: an economy enters the noise only with inflation for every year 1925-29; an economy without it
  keeps zero noise in the draws (listed).
- *A group with no weight in a year*: that year's difference is not computed (printed as such).
"""

from __future__ import annotations

import csv
import io
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from ft import cards
from ft.data import freeze

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
CARD = STUDY / "cards" / "C18-cs-a-consumer-prices-off-gold.yaml"
TABLES = ROOT / "data" / "reconstructed" / "ft001-cs-tables" / "series.csv"


def month(p: str) -> pd.Period | None:
    return None if p == "none printed" else pd.Period(p, "M")


def dates() -> dict[str, dict[str, pd.Period | None]]:
    out: dict[str, dict] = {}
    with TABLES.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["table"] == "BJ-2.1":
                out.setdefault(r["iso3"], {})[r["kind"]] = month(r["period"])
    return out


def jst_inflation() -> pd.DataFrame:
    raw = freeze.load("jst/macrohistory", "2026-09-30").read_bytes("JSTdatasetR6.dta")
    d = pd.read_stata(io.BytesIO(raw))[["iso", "year", "cpi"]]
    d["year"] = d.year.astype(int)
    d = d.sort_values(["iso", "year"])
    d["pi"] = 100 * (d.cpi / d.groupby("iso").cpi.shift(1) - 1)
    d.loc[d.groupby("iso").year.diff() != 1, "pi"] = np.nan
    return d.set_index(["iso", "year"]).pi


def months_status(dt: dict, year: int, exclude_exchange_control: bool) -> tuple[float, float]:
    """(weight off, weight on) of one economy-year: months off or on gold over 12, excluded months weighing nothing."""
    ret = dt.get("return to gold")
    acts = [dt.get(k) for k in ("suspension of the gold standard", "foreign exchange control", "devaluation")]
    first = min([a for a in acts if a is not None], default=None)
    sd = min([a for a in (dt.get("suspension of the gold standard"), dt.get("devaluation")) if a is not None], default=None)
    ec = dt.get("foreign exchange control")
    off = on = 0
    for m in range(1, 13):
        p = pd.Period(f"{year}-{m:02d}", "M")
        if exclude_exchange_control and ec is not None and (sd is None or ec < sd) and p >= ec and (sd is None or p < sd):
            continue
        if ret is None or p < ret or (first is not None and p >= first):
            off += 1
        else:
            on += 1
    return off / 12, on / 12


def weights(dts: dict, economies: list[str], years: list[int], exclude_ec: bool) -> pd.DataFrame:
    rows = []
    for e in economies:
        for y in years:
            w_off, w_on = months_status(dts[e], y, exclude_ec)
            rows.append({"iso": e, "year": y, "w_off": w_off, "w_on": w_on})
    return pd.DataFrame(rows).set_index(["iso", "year"])


def diff(pi: pd.Series, w: pd.DataFrame) -> float | None:
    x = w.join(pi.rename("pi"), how="left").dropna(subset=["pi"])
    so, sn = x.w_off.sum(), x.w_on.sum()
    if so == 0 or sn == 0:
        return None
    return float((x.w_off * x.pi).sum() / so - (x.w_on * x.pi).sum() / sn)


def read(pi: pd.Series, w: pd.DataFrame, noise: pd.DataFrame, years: list[int], prm: dict, line: float) -> dict:
    obs = diff(pi, w)
    rng = np.random.default_rng(prm["seed"])
    cal = noise.columns.tolist()
    sims, sims2 = [], []
    present = w.join(pi.rename("pi")).dropna(subset=["pi"]).index
    w = w.loc[present]
    for _ in range(prm["draws"]):
        pick = rng.choice(cal, size=len(years), replace=True)
        e = pd.Series({(i, y): noise.at[i, c] for i in noise.index for y, c in zip(years, pick)})
        e = e.reindex(w.index).fillna(0.0)
        sims.append(diff(e, w))
        sims2.append(diff(prm["noise_doubled"] * e, w))
    hw = float(np.percentile(np.abs(sims), 97.5))
    hw2 = float(np.percentile(np.abs(sims2), 97.5))
    lo, hi = obs - hw, obs + hw

    def rd(lo, hi):
        if lo > line:
            return "effect"
        if hi < -line:
            return "effect of the other sign"
        if lo >= -line and hi <= line:
            return "too small to matter"
        return "bounded"
    return {"pooled": obs, "half_width": hw, "lo": lo, "hi": hi, "reading": rd(lo, hi),
            "doubled": {"half_width": hw2, "lo": obs - hw2, "hi": obs + hw2, "reading": rd(obs - hw2, obs + hw2)},
            "economy_years": int(len(w)), "weight_off": float(w.w_off.sum()), "weight_on": float(w.w_on.sum())}


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm, mt = card["parameters"], card["matters"]
    econ = prm["economies"]
    dts = dates()
    missing = [e for e in econ if e not in dts]
    econ = [e for e in econ if e in dts]
    pi = jst_inflation()
    c0, c1 = prm["calibration_years"]
    cal_years = list(range(c0, c1 + 1))
    noise = {}
    for e in econ:
        v = [pi.get((e, y), np.nan) for y in cal_years]
        if all(np.isfinite(v)):
            noise[e] = [x - np.mean(v) for x in v]
    noise = pd.DataFrame(noise, index=cal_years).T
    years = prm["years_read"]
    out = {"economies": econ, "missing_dates": missing, "calibration_without": sorted(set(econ) - set(noise.index))}
    variants = {"main": (econ, False, mt["cs_a_pooled"]),
                "no_exchange_control": (econ, True, mt["cs_a_pooled_no_exchange_control"]),
                "no_spain": ([e for e in econ if e != "ESP"], False, mt["cs_a_pooled_no_spain"])}
    for name, (ec_list, excl, line) in variants.items():
        w = weights(dts, ec_list, years, excl)
        out[name] = read(pi, w, noise.loc[[e for e in noise.index if e in ec_list]], years, prm, line)
        allw = weights(dts, ec_list, list(range(1930, 1937)), excl)
        out[name]["by_year"] = {str(y): diff(pi, allw.xs(y, level="year", drop_level=False)) for y in range(1930, 1937)}
        out[name]["status_1932_34"] = {e: [round(float(allw.loc[(e, y), "w_off"]), 3) for y in years] for e in ec_list}
    out["described_not_read"] = "1930-31 and 1935-36 yearly differences are described, never read"
    out["beside"] = "Bernanke & James, Table 2.2 and p. 42: wholesale prices, theirs"
    path = cards.write_result(STUDY, CARD, out)
    print(path)
    return path


if __name__ == "__main__":
    main()
