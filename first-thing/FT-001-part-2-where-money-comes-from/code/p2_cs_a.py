"""Card C35 (CS-A): notes and coin held by the public as a share of broad money, every month, in the United States, the
euro area and Britain, with IFS's pair for Britain and every IFS economy with both lines beside.

From the study's folder: ``python code/p2_cs_a.py``. Writes ``results/runs/C35-cs-a-currency-share.json``.

Each share is a ratio of two published stocks matched by month (year and month); a series that stops is read to its last
month, never extended. Nothing is averaged across economies.
"""

from __future__ import annotations

import io
import json
from pathlib import Path
from statistics import median

import pandas as pd

from ft import cards
from ft.data import dbnomics, fred
from ft.data import agency
from ft.data import freeze as F

STUDY = Path(__file__).resolve().parents[1]
CARD = STUDY / "cards" / "C35-cs-a-currency-share.yaml"

# The euro's members and the month each entered (the ECB's list); a member's months from its entry are dropped (method 5).
EURO_ENTRY = {"BE": "1999-01", "DE": "1999-01", "ES": "1999-01", "FR": "1999-01", "IE": "1999-01", "IT": "1999-01",
              "LU": "1999-01", "NL": "1999-01", "AT": "1999-01", "PT": "1999-01", "FI": "1999-01", "GR": "2001-01",
              "SI": "2007-01", "CY": "2008-01", "MT": "2008-01", "SK": "2009-01", "EE": "2011-01", "LV": "2014-01",
              "LT": "2015-01", "HR": "2023-01"}


def monthly(s: pd.Series) -> pd.Series:
    """A series indexed by 'YYYY-MM' strings."""
    s = s.dropna()
    s.index = pd.to_datetime(s.index).strftime("%Y-%m")
    return s[~s.index.duplicated(keep="last")]


def ecb(name: str, key: str, vintage: str) -> pd.Series:
    fz = F.load("ecb/bsi-m3-currency", vintage)
    df = pd.read_csv(io.BytesIO(fz.read_bytes(name)), dtype=str)
    df = df[df["KEY"] == "BSI." + key]
    if df.empty:
        raise SystemExit(f"C35: {key} not in {name}")
    return pd.Series(pd.to_numeric(df["OBS_VALUE"]).values, index=df["TIME_PERIOD"].values).dropna()


def boe(code: str, vintage: str) -> pd.Series:
    fz = F.load("bankofengland/m4-notes", vintage)
    df = pd.read_csv(io.BytesIO(fz.read_bytes(f"{code}.csv")))
    idx = pd.to_datetime(df["DATE"], format="%d %b %Y").dt.strftime("%Y-%m")
    return pd.Series(pd.to_numeric(df[code]).values, index=idx.values).dropna()


def ifs(mask: str, vintage: str) -> pd.DataFrame:
    d = dbnomics.read("IMF", "IFS", mask, vintage)
    mult = d["series_name"].map(dbnomics.multiplier)
    if mult.isna().any() or mult.nunique() != 1:
        raise SystemExit(f"C35: {mask} mixes or lacks unit multipliers")
    return d[["REF_AREA", "period", "value"]].dropna()


def describe(num: pd.Series, den: pd.Series, decimals: int) -> dict:
    common = sorted(set(num.index) & set(den.index))
    if not common:
        raise SystemExit("C35: no common month")
    share = pd.Series([100 * num[m] / den[m] for m in common], index=common)
    lo, hi = share.idxmin(), share.idxmax()
    return {"first": common[0], "last": common[-1], "months": len(common),
            "latest": round(float(share.iloc[-1]), decimals), "lowest": round(float(share[lo]), decimals),
            "lowest_month": lo, "highest": round(float(share[hi]), decimals), "highest_month": hi,
            "series": {m: round(float(v), 3) for m, v in share.items()}}


def wider(cur: pd.DataFrame, bro: pd.DataFrame, line: float, decimals: int) -> dict:
    out, dropped_after_entry = {}, {}
    for area in sorted(set(cur.REF_AREA) & set(bro.REF_AREA)):
        if area[0].isdigit():
            continue
        c = cur[cur.REF_AREA == area].set_index("period")["value"]
        b = bro[bro.REF_AREA == area].set_index("period")["value"]
        months = sorted(set(c.index) & set(b.index))
        if area in EURO_ENTRY:
            kept = [m for m in months if m < EURO_ENTRY[area]]
            dropped_after_entry[area] = len(months) - len(kept)
            months = kept
        months = [m for m in months if b[m] > 0]
        if not months:
            continue
        m = months[-1]
        out[area] = {"latest_month": m, "share": round(100 * float(c[m]) / float(b[m]), decimals)}
    years: dict[str, int] = {}
    for v in out.values():
        years[v["latest_month"][:4]] = years.get(v["latest_month"][:4], 0) + 1
    top = max(years.values())
    modal = max(y for y, n in years.items() if n == top)

    def summary(rows: list[dict]) -> dict:
        shares = [r["share"] for r in rows]
        return {"n": len(rows), "median": round(median(shares), decimals),
                "at_or_above_half": sum(1 for s in shares if s >= 100 * line)}

    return {"economies": out, "latest_month_by_year": dict(sorted(years.items())), "modal_year": modal,
            "modal_year_summary": summary([r for r in out.values() if r["latest_month"][:4] == modal]),
            "all_summary": summary(list(out.values())), "euro_months_dropped": dropped_after_entry}


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    p = card["parameters"]
    dec = int(p["decimals"])
    us = describe(monthly(agency.series("CURRSL", "2026-09-30")), monthly(agency.series("M2SL", "2026-09-30")), dec)
    if us["first"] != p["us"]["from"]:
        raise SystemExit(f"C35: the US series begin at {us['first']}, the card says {p['us']['from']}")
    ea = describe(ecb("bsi-currency.csv", p["euro_area"]["currency"], "2026-10-10"),
                  ecb("bsi-m3.csv", p["euro_area"]["broad"], "2026-10-10"), dec)
    gb = describe(boe("LPMAVAB", "2026-10-10"), boe("LPMAUYN", "2026-10-10"), dec)
    cur, bro = ifs("M..14A___XDC", "2026-09-30"), ifs("M..35L___XDC", "2026-10-01")
    gb_ifs = describe(cur[cur.REF_AREA == "GB"].set_index("period")["value"],
                      bro[bro.REF_AREA == "GB"].set_index("period")["value"], dec)
    payload = {"us": us, "euro_area": ea, "britain": gb, "britain_ifs": gb_ifs,
               "wider": wider(cur, bro, float(p["refutes_most"]), dec),
               "most_refuted_in": [k for k, v in (("us", us), ("euro_area", ea), ("britain", gb))
                                   if v["latest"] >= 100 * float(p["refutes_most"])]}
    cards.write_result(STUDY, CARD, payload)
    return payload


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "series"} if isinstance(v, dict) and "series" in v else v
                      for k, v in r.items() if k != "wider"}, indent=1))
