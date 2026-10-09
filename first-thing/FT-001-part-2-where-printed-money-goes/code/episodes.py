"""Frame e's episodes, by rule, before any outcome is read: cards C05 (the rule as first written) and C09
(its correction: excess over the prior pace of nominal GDP, one episode per horizon, units checked).

From the study's folder: ``../../toolkit/bin/ftpy code/episodes.py C05-e-episodes`` (or
``C09-e-episodes-excess``). Refuses to run unless the card is committed and unchanged (``ft.cards``);
writes ``results/runs/<card>.json``.

Reads only what is known at each crossing: base money, GDP, and the CPI up to the crossing month (the
accommodation guard and its variant) - plus, for the censoring flags, which months the CPI reaches (a
condition of the data, not an outcome), and for C09's units check, broad money and the World Bank's
broad money as a share of GDP. The one reading after a crossing is C09's count of further crossings
within the horizon: base money only, a description, never an entry. Outcomes are C06's and C10's.

Readings of the cards that their text leaves to the code, fixed here before the runs:
- inflation is the twelve-month (or, annual, year-average on year-average) change of the CPI, in percent;
- accommodation: at or above T at any month from m0 to the month before c where the CPI exists; "cannot
  be read" only if it exists at none of them; months without it are counted (``cpi_gap_months``);
- the annual rule's accommodation reads the year-average inflation of m0's year to the year before c's
  (the variant adds c's year), m0 and c being Decembers;
- the panel's common end is computed on the monthly CPI of the moneys scanned (units_break moneys out);
- C09's resume point for an annual episode is m0 plus H rounded up to whole years.

The list is written as CSV text inside the result (one line per episode), so the result stays small.
"""

from __future__ import annotations

import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402

from ft import cards  # noqa: E402
from ft.data import worldbank  # noqa: E402

STUDY = Path(__file__).resolve().parents[1]
DOOR_STARTS = {"W1": pd.Period("2008-08", "M"), "W2": pd.Period("2020-02", "M")}
RULES = {  # what each card changes; C05 is the rule as first written
    "C05-e-episodes": {"excess": False, "resume": "crossing", "units": False},
    "C09-e-episodes-excess": {"excess": True, "resume": "horizon", "units": True},
}
COLUMNS = ["area", "rule", "w", "low", "m0", "c", "L", "B_m0", "B_c", "rise_pct_gdp", "gdp_year",
           "gdp_year_before", "gamma", "further_crossings_within_H", "infl_m0", "infl_max_m0_to_before_c",
           "infl_c", "cpi_gap_months", "acc_T10", "acc_T12", "acc_T20", "acc_with_c_T12", "cens_H24",
           "cens_H36", "cens_H60", "base_break", "cpi_source", "gdp_source", "door_windows"]


def scan(b: np.ndarray, years: np.ndarray, per_year: int, X: float, Y: int, q: float, gdp_of, *,
         excess: bool = False, gamma_of=None, resume: str = "crossing", H_periods: int = 0,
         floor0: int = 0, stop: int | None = None) -> tuple[list[dict], int]:
    """The rule on one series of ``b`` (NaN where missing), ``per_year`` periods a year, a window of
    ``Y * per_year`` periods. ``gdp_of(year) -> (value, year_used)``; ``gamma_of(year) -> growth or
    None`` (C09). Returns episodes (index positions) and the count of periods not testable for want of
    GDP. ``stop``: scan no further than this index (exclusive)."""
    out, untestable, floor = [], 0, floor0
    n = len(b) if stop is None else min(len(b), stop)
    Yp = Y * per_year
    for t in range(floor0, n):
        if t < floor or np.isnan(b[t]):
            continue
        w = max(t - Yp, floor)
        if np.all(np.isnan(b[w:t])):
            continue
        gamma = 0.0
        if excess:
            gamma = gamma_of(int(years[w]))
            if gamma is None:
                untestable += 1
                continue
        k = np.arange(w, t + 1)
        d = b[w:t + 1] * np.exp(-gamma * (k - w) / per_year)
        low = np.nanmin(d)
        lift = d[-1] - low
        if not lift > 0:
            continue
        thr = low + q * lift
        cand = [s for s in range(w, t) if not np.isnan(d[s - w]) and d[s - w] <= thr]
        if not cand:
            continue
        s0 = cand[-1]
        g, gy = gdp_of(int(years[s0]))
        if g is None:
            untestable += 1
            continue
        rise = lift * math.exp(gamma * (t - w) / per_year)
        if rise >= X / 100 * g:
            low_at = max(s for s in range(w, t + 1) if not np.isnan(d[s - w]) and d[s - w] == low)
            out.append({"w": w, "low": low_at, "m0": s0, "c": t, "L": float(b[low_at]), "B_m0": float(b[s0]),
                        "B_c": float(b[t]), "rise_pct_gdp": float(100 * rise / g), "gdp_year": gy,
                        "gdp_year_before": gy != int(years[s0]), "gamma": round(gamma, 5)})
            floor = t + 1 if resume == "crossing" else max(t + 1, s0 + H_periods)
    return out, untestable


def main(card_id: str) -> None:
    card_path = STUDY / "cards" / f"{card_id}.yaml"
    card = yaml.safe_load(card_path.read_text())
    cards.require_locked(card_path)  # refuse before reading any data
    rule = RULES[card_id]
    prm, grid = card["parameters"], card["parameters"]["grid"]
    X0, Y0, q0, T0, H0 = (prm["X_pct_of_gdp"], prm["Y_years"], prm["q_takeoff"], prm["T_inflation_pct"],
                          prm["H_months"])
    U0 = prm.get("units_factor")
    Ts = sorted({T0, *grid["T_inflation_pct"]})
    Hs = sorted({H0, *grid["H_months"]})

    annual = P.panel()
    monthly = P.monthly()
    broken = sorted(annual[annual.units_break].index.get_level_values(0).unique())
    annual = annual[~annual.units_break & ~annual.inside_euro]
    monthly = monthly[~monthly.units_break & ~monthly.inside_euro]
    seam = set(annual[annual.base_break].index.get_level_values(0)) | set(
        monthly[monthly.base_break].index.get_level_values(0))

    # the panel's common end, on the monthly CPI (half the moneys with a value 12 months earlier)
    cpi_m = monthly.cpi.dropna()
    have = cpi_m.groupby(level=1).apply(lambda s: set(s.index.get_level_values(0)))
    common_end = None
    for t in pd.period_range(have.index.min(), have.index.max(), freq="M"):
        prev = have.get(t - 12, set())
        if len(prev) and len(prev & have.get(t, set())) >= 0.5 * len(prev):
            common_end = t

    areas_all = sorted(set(annual.index.get_level_values(0)) | set(monthly.index.get_level_values(0)))

    # C09's units check: the panel's broad money to GDP against the World Bank's (a ratio, free of units)
    units_factor_of: dict[str, float | None] = {}
    if rule["units"]:
        wb = worldbank.read("FM.LBL.BMNY.GD.ZS", P.VINTAGES["wdi"]).dropna(subset=["value"])
        econ = worldbank.read_economies(P.VINTAGES["wdi"]).set_index("iso3")
        wb = wb[wb.iso3.isin(econ.index)]
        wb = wb.assign(area=wb.iso3.map(econ.iso2).where(wb.iso3 != "EMU", "U2")).set_index(["area", "year"]).value / 100
        pb = (annual.broad / annual.gdp).dropna()
        ratio = (pb / wb.reindex(pb.index)).dropna()
        med = ratio.groupby(level=0).median()
        for a in areas_all:
            units_factor_of[a] = None if a not in med.index else float(max(med[a], 1 / med[a]))

    def admitted(a: str, factor: float | None) -> bool:
        if not rule["units"] or a == "U2":
            return True
        f = units_factor_of.get(a)
        return f is not None and f <= factor

    def gdp_getter(area):
        g = annual.gdp.xs(area).dropna() if area in annual.index.get_level_values(0) else pd.Series(dtype=float)

        def get(y):
            for yy in (y, y - 1):
                if yy in g.index and g[yy] > 0:
                    return float(g[yy]), yy
            return None, None

        def gamma(y_window):
            y1, y0 = y_window - 1, y_window - 1 - Y_current[0]
            if y1 in g.index and y0 in g.index and g[y1] > 0 and g[y0] > 0:
                return math.log(g[y1] / g[y0]) / Y_current[0]
            return None
        return get, gamma

    Y_current = [Y0]

    def run(X, Y, q, H, factor):
        Y_current[0] = Y
        eps, untestable, out_units = [], Counter(), []
        for a in areas_all:
            if not admitted(a, factor):
                out_units.append(a)
                continue
            get, gamma = gdp_getter(a)
            mb = monthly.base.xs(a).dropna() if a in monthly.index.get_level_values(0) else pd.Series(dtype=float)
            first_m = mb.index.min() if len(mb) else None
            ab = annual.base.xs(a).dropna() if a in annual.index.get_level_values(0) else pd.Series(dtype=float)
            if first_m is not None:
                ab = ab[[pd.Period(f"{y}-12", "M") < first_m for y in ab.index]]
            resume_after = None  # the month from which the monthly scan may start
            if len(ab) >= 2:
                yrs = np.arange(ab.index.min(), ab.index.max() + 1)
                b = ab.reindex(yrs).to_numpy(dtype=float)
                kw = dict(excess=rule["excess"], gamma_of=gamma, resume=rule["resume"], H_periods=math.ceil(H / 12))
                found, u = scan(b, yrs, 1, X, Y, q, get, **kw)
                untestable[a] += u
                for e in found:
                    e["further"] = None
                    if rule["resume"] == "horizon":
                        e["further"] = len(scan(b, yrs, 1, X, Y, q, get, excess=rule["excess"], gamma_of=gamma,
                                                floor0=e["c"] + 1, stop=e["m0"] + math.ceil(H / 12))[0])
                    m0_year = int(yrs[e["m0"]])
                    e.update({"area": a, "rule": "annual",
                              **{k: str(pd.Period(f"{yrs[e[k]]}-12", "M")) for k in ("w", "low", "m0", "c")}})
                    eps.append(e)
                    nxt = pd.Period(e["c"], "M") + 1 if rule["resume"] == "crossing" else max(
                        pd.Period(e["c"], "M") + 1, pd.Period(f"{m0_year + math.ceil(H / 12)}-12", "M"))
                    resume_after = nxt
            if len(mb) >= 2:
                idx = pd.period_range(mb.index.min(), mb.index.max(), freq="M")
                b = mb.reindex(idx).to_numpy(dtype=float)
                floor0 = 0 if resume_after is None else max(0, (resume_after - idx[0]).n)
                yrs = np.array([p.year for p in idx])
                found, u = scan(b, yrs, 12, X, Y, q, get, excess=rule["excess"], gamma_of=gamma,
                                resume=rule["resume"], H_periods=H, floor0=floor0)
                untestable[a] += u
                for e in found:
                    e["further"] = None
                    if rule["resume"] == "horizon":
                        e["further"] = len(scan(b, yrs, 12, X, Y, q, get, excess=rule["excess"], gamma_of=gamma,
                                                floor0=e["c"] + 1, stop=e["m0"] + H)[0])
                    e.update({"area": a, "rule": "monthly", **{k: str(idx[e[k]]) for k in ("w", "low", "m0", "c")}})
                    eps.append(e)
        return eps, untestable, out_units

    cpi_cache: dict[str, pd.Series] = {}

    def annotate(e, H_list=Hs):
        a = e["area"]
        m0, c = pd.Period(e["m0"], "M"), pd.Period(e["c"], "M")
        if e["rule"] == "monthly":
            if a not in cpi_cache:
                cpi = monthly.cpi.xs(a).dropna() if a in monthly.index.get_level_values(0) else pd.Series(dtype=float)
                if len(cpi):
                    cpi = cpi.reindex(pd.period_range(cpi.index.min(), cpi.index.max(), freq="M"))
                    cpi_cache[a] = 100 * (cpi / cpi.shift(12) - 1)
                else:
                    cpi_cache[a] = pd.Series(dtype=float)
            inf = cpi_cache[a]
            before = np.array([inf.get(t, np.nan) for t in pd.period_range(m0, c - 1, freq="M")], dtype=float)
            at_c, at_m0 = inf.get(c, np.nan), inf.get(m0, np.nan)
        else:
            cpi = annual.cpi.xs(a).dropna() if a in annual.index.get_level_values(0) else pd.Series(dtype=float)
            inf = 100 * (cpi / cpi.shift(1) - 1) if len(cpi) else pd.Series(dtype=float)
            before = np.array([inf.get(y, np.nan) for y in range(m0.year, c.year)], dtype=float)
            at_c, at_m0 = inf.get(c.year, np.nan), inf.get(m0.year, np.nan)
        seen = before[~np.isnan(before)]
        e["infl_m0"] = None if pd.isna(at_m0) else round(float(at_m0), 2)
        e["infl_max_m0_to_before_c"] = None if not len(seen) else round(float(seen.max()), 2)
        e["infl_c"] = None if pd.isna(at_c) else round(float(at_c), 2)
        e["cpi_gap_months"] = int(np.isnan(before).sum()) if e["rule"] == "monthly" else None
        for T in Ts:
            e[f"acc_T{T}"] = "cannot be read" if not len(seen) else bool(seen.max() >= T)
        with_c = np.append(seen, [] if pd.isna(at_c) else [float(at_c)])
        e[f"acc_with_c_T{T0}"] = "cannot be read" if not len(with_c) else bool(with_c.max() >= T0)
        for H in H_list:
            e[f"cens_H{H}"] = bool(common_end is None or m0 + H > common_end)
        e["base_break"] = a in seam
        row = annual.loc[a].iloc[-1] if a in annual.index.get_level_values(0) else None
        own = {"US": "fred", "U2": "ecb"}.get(a)  # the panel's *_source columns describe IFS/World Bank filling only
        e["cpi_source"] = own or (None if row is None else row.get("cpi_source"))
        e["gdp_source"] = own or (None if row is None else row.get("gdp_source"))
        e["door_windows"] = " ".join(k for k, d in DOOR_STARTS.items() if a == "US" and m0 <= d <= c)
        e["further_crossings_within_H"] = e.pop("further", None)
        return e

    def summary(eps, H=H0):
        by = Counter(e["area"] for e in eps)
        top = by.most_common(1)[0] if by else (None, 0)
        return {"episodes": len(eps),
                "accommodation": sum(e[f"acc_T{T0}"] is True for e in eps),
                "accommodation_cannot_be_read": sum(e[f"acc_T{T0}"] == "cannot be read" for e in eps),
                "censored_at_H": sum(e[f"cens_H{H}"] for e in eps),
                "eligible": sum(e[f"acc_T{T0}"] is False and not e[f"cens_H{H}"] for e in eps),
                "moneys": len(by), "monthly": sum(e["rule"] == "monthly" for e in eps),
                "annual": sum(e["rule"] == "annual" for e in eps),
                "top_money": top[0], "top_money_episodes": top[1],
                "top_money_share": round(top[1] / len(eps), 3) if eps else None}

    def compact(eps):
        rows = sorted(eps, key=lambda e: (e["m0"], e["area"]))
        return "area,m0,c,rise_pct_gdp,accommodation\n" + "".join(
            f"{e['area']},{e['m0']},{e['c']},{e['rise_pct_gdp']:.2f},{e[f'acc_T{T0}']}\n" for e in rows)

    def full_csv(eps):
        df = pd.DataFrame(sorted(eps, key=lambda e: (e["m0"], e["area"])))
        for col in COLUMNS:
            if col not in df:
                df[col] = None
        return df[COLUMNS].to_csv(index=False, float_format="%.6g")

    head, untestable, out_units = run(X0, Y0, q0, H0, U0)
    head = [annotate(e) for e in head]
    s = summary(head)
    grid_out = {}
    for X in grid["X_pct_of_gdp"]:
        for Y in grid["Y_years"]:
            eps = head if (X, Y) == (X0, Y0) else [annotate(e) for e in run(X, Y, q0, H0, U0)[0]]
            grid_out[f"X{X}_Y{Y}"] = {**summary(eps), "list": compact(eps)}
    variants = {}
    for q in grid["q_takeoff"]:
        eps = [annotate(e) for e in run(X0, Y0, q, H0, U0)[0]]
        variants[f"q{q}"] = {**summary(eps), "list": compact(eps)}
    if rule["resume"] == "horizon":  # the list itself depends on H
        for H in grid["H_months"]:
            eps = [annotate(e) for e in run(X0, Y0, q0, H, U0)[0]]
            variants[f"H{H}"] = {**summary(eps, H), "list": compact(eps)}
    if rule["units"]:
        for f in grid.get("units_factor", []):
            eps, _, out_f = run(X0, Y0, q0, H0, f)
            eps = [annotate(e) for e in eps]
            variants[f"units_factor{f}"] = {**summary(eps), "set_aside": out_f, "list": compact(eps)}
    payload = {
        "card_rule": rule,
        "headline": {"X_pct_of_gdp": X0, "Y_years": Y0, "q_takeoff": q0, "T_inflation_pct": T0, "H_months": H0,
                     "units_factor": U0},
        "common_end": str(common_end),
        "moneys_in_panel": len(areas_all),
        "moneys_dropped_units_break": broken,
        "moneys_set_aside_by_units_check": out_units,
        "units_check_factor_by_money": {a: (None if v is None else round(v, 3)) for a, v in units_factor_of.items()
                                        if a in out_units},
        "periods_untestable": int(sum(untestable.values())),
        "summary": s,
        "summary_by_T": {str(T): {"accommodation": sum(e[f"acc_T{T}"] is True for e in head),
                                  "eligible": sum(e[f"acc_T{T}"] is False and not e[f"cens_H{H0}"] for e in head)}
                         for T in Ts},
        "summary_by_H_on_headline_list": {str(H): {"censored": sum(e[f"cens_H{H}"] for e in head),
                                                   "eligible": sum(e[f"acc_T{T0}"] is False and not e[f"cens_H{H}"]
                                                                   for e in head)} for H in Hs},
        "accommodation_with_crossing_month": sum(e[f"acc_with_c_T{T0}"] is True for e in head),
        "without_top_money": summary([e for e in head if e["area"] != s["top_money"]])
        if s["top_money_share"] and s["top_money_share"] > 0.25 else None,
        "us_episodes": full_csv([e for e in head if e["area"] == "US"]),
        "episodes": full_csv(head),
        "grid": grid_out,
        "variants": variants,
    }
    out = cards.write_result(STUDY, card_path, payload)
    print(out, f"{out.stat().st_size / 1e6:.2f} MB")
    print("common end:", common_end, "| moneys in panel:", len(areas_all), "| set aside by units:", out_units)
    print("headline:", s)
    for k, v in {**grid_out, **variants}.items():
        print(k, {kk: v[kk] for kk in ("episodes", "accommodation", "censored_at_H", "eligible")})
    print(payload["us_episodes"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "C09-e-episodes-excess")
