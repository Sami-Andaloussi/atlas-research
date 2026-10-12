"""Card C25 (K9, a base rate): in JST R6's eighteen economies, 1870-2020, how often an inflation crisis began within three
years, by the state's debt against GDP, rows near the world wars and three other wars apart; counts, shares, cluster-bootstrap intervals and the
crisis beginnings no row reaches. Only counts, shares, bounds, intervals, economy names, the years of the missed
beginnings and numpy's and pandas' versions are written (the run is withheld from the public copy, JST's licence).

From the study's folder: ``python code/p1_k9_debt.py``. Writes ``results/runs/C25-k9-crises-by-debt.json``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ft import cards, paths

STUDY = Path(__file__).resolve().parents[1]
CARD = STUDY / "cards" / "C25-k9-crises-by-debt.yaml"
SHA = "b0ebb74a8d1b5b1bc9033fc46a6dcc578736afff8ce1e1086b7840f2649e79b3"
SETTINGS = ("peace", "near_war", "all")


def _war_years(country: str, p: dict) -> set[int]:
    years = {y for a, b in p["war_years_all"] for y in range(a, b + 1)}
    for a, b in p["war_years_extra"].get(country, []):
        years |= set(range(a, b + 1))
    return years


def _band_of(x: float) -> int:
    if x < 0.60:
        return 0
    if x <= 1.00:
        return 1
    return 2


def _merge(counts: list[int], floor: int) -> list[list[int]]:
    groups = [[i] for i in range(len(counts))]
    size = list(counts)
    i = len(groups) - 1
    while i > 0:
        if size[i] < floor:
            groups[i - 1] += groups[i]
            size[i - 1] += size[i]
            del groups[i], size[i]
        i -= 1
    if len(groups) > 1 and size[0] < floor:
        groups[1] = groups[0] + groups[1]
        size[1] += size[0]
        del groups[0], size[0]
    return groups


def _stat(rows: pd.DataFrame, draws: int) -> dict:
    economies = sorted(rows["country"].unique())
    hits = np.array([int(rows.loc[rows.country == c, "followed"].sum()) for c in economies])
    sizes = np.array([int((rows.country == c).sum()) for c in economies])
    n, k, m = int(sizes.sum()), int(hits.sum()), len(economies)
    out = {"rows": n, "economies": m, "economy_names": economies, "followed": k, "share": 100 * k / n if n else None}
    if n == 0:
        return out
    if k == 0:
        out["bound"] = {"kind": "at most", "value": 100 * (1 - 0.05 ** (1 / m))}
    elif k == n:
        out["bound"] = {"kind": "at least", "value": 100 * 0.05 ** (1 / m)}
    else:
        rng = np.random.default_rng(20261012)  # the card's generator, fresh for each band, setting and line
        shares = []
        for _ in range(draws):
            pick = rng.integers(0, m, size=m)
            shares.append(100 * hits[pick].sum() / sizes[pick].sum())
        lo, hi = np.percentile(shares, [2.5, 97.5])
        out["low"], out["high"] = float(lo), float(hi)
    return out


def _one_line(d: pd.DataFrame, line: float, p: dict) -> dict:
    horizon = int(p["horizon_years"])
    rows, missed = [], {s: [] for s in SETTINGS}
    for country, g in d.groupby("country"):
        g = g.set_index("year").sort_index()
        rise = g["cpi"] / g["cpi"].shift(1) - 1
        rise = rise.where(g.index.to_series().diff() == 1)  # consecutive years only
        crisis = rise >= line
        begins = crisis & (rise.shift(1) < line)
        war = _war_years(country, p)
        years = list(g.index)
        reached = set()
        for t in years:
            if pd.isna(g.at[t, "debtgdp"]) or pd.isna(rise.get(t)) or crisis.get(t, False):
                continue
            ahead = [t + h for h in range(1, horizon + 1)]
            if any(y not in rise.index or pd.isna(rise[y]) for y in ahead):
                continue
            near = any(y in war for y in range(t - horizon, t + horizon + 1))
            reached |= {y for y in ahead if begins.get(y, False)}
            rows.append({"country": country, "band": _band_of(float(g.at[t, "debtgdp"])),
                         "setting": "near_war" if near else "peace",
                         "followed": bool(any(begins.get(y, False) for y in ahead))})
        for y in years:
            if not begins.get(y, False) or y in reached:
                continue
            near = any(z in war for z in range(y - 1 - horizon, y + horizon))  # the row t = y-1 would have had: y-4..y+2
            for s in ("near_war" if near else "peace", "all"):
                missed[s].append({"economy": country, "year": int(y)})
    table = pd.DataFrame(rows)
    out: dict = {"settings": {}, "missed_beginnings": {}}
    for s in SETTINGS:
        sub = table if s == "all" else table[table.setting == s]
        counts = [int((sub.band == b).sum()) for b in range(3)]
        groups = _merge(counts, int(p["merge_below_rows"]))
        entries = []
        for grp in groups:
            edges = [list(e) for e in p["bands_debtgdp"]]
            entries.append({"band": {"from": edges[grp[0]][0], "to": edges[grp[-1]][1], "merged": len(grp) > 1},
                            **_stat(sub[sub.band.isin(grp)], 2000)})
        out["settings"][s] = entries
        out["missed_beginnings"][s] = {"count": len(missed[s]),
                                       "each": sorted(missed[s], key=lambda e: (e["economy"], e["year"]))}
    return out


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    p = card["parameters"]
    f = paths.root() / p["data"]
    if hashlib.sha256(f.read_bytes()).hexdigest() != SHA:
        raise SystemExit("C25: the frozen JST file is not the one the card names (sha256)")
    d = pd.read_stata(f)[["country", "year", "debtgdp", "cpi"]]
    d["year"] = d["year"].astype(int)
    if d.country.nunique() != 18 or len(d.dropna(subset=["debtgdp", "cpi"])) != 2489:
        raise SystemExit("C25: the file does not hold 18 economies and 2,489 economy-years with debt and CPI")
    result = {name: _one_line(d, float(v), p) for name, v in p["crisis_line"].items()}
    result["versions"] = {"numpy": np.__version__, "pandas": pd.__version__}
    cards.write_result(STUDY, CARD, result)
    return result


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: {s: [(e["band"], e["rows"], e["followed"]) for e in v["settings"][s]] for s in SETTINGS}
                      for k, v in r.items() if k != "versions"}, indent=1))
