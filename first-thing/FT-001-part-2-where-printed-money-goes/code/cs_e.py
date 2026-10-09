"""Card C31 (CS-E): across economies whose inflation was calm before the pandemic, did faster 2019-21 growth of broad
money go with more 2021-23 inflation? Huber leads, OLS beside, read on a cluster bootstrap against 0.1 a point.

From the study's folder: ``../../toolkit/bin/ftpy code/cs_e.py``. Writes ``results/runs/C31-cs-e-pandemic-cross-section.json``.
It is long (the leave-one-out and the permutation nulls each re-run a bootstrap); run it in the background.

Readings of the card that its text leaves to the code, fixed here before the run:

- *An economy's code*: IFS's REF_AREA, two letters; anything else (5X, 5Y, 7A, U2 in IFS, ...) never enters. The euro
  area enters once as ``U2`` from the ECB's series.
- *A year-end stock*: IFS's annual value of a stock (end of period). The ECB's M3 at December of the year.
- *Annual-average CPI for the euro area*: the mean of HICP's twelve months (a year needs all twelve).
- *The calm-start mean*: the arithmetic mean of 100 * (CPI_y / CPI_y-1 - 1) over the card's five years (a year
  missing leaves the economy out of the main set, listed as "calm start unknown").
- *The momentum control*: December 2020 to December 2021 where the economy's outcome is monthly and both months
  exist, else the annual averages 2020 to 2021.
- *A Huber fit that fails to converge in a bootstrap draw*: the draw is skipped and counted.
- *Clusters*: a union's members share one cluster; the euro area is its own; every other economy its own.
- *Reported precision*: the half-width of each bootstrap interval, beside the calibration the card restates.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import panel as P  # noqa: E402

from ft import cards  # noqa: E402
from ft.data import worldbank  # noqa: E402

CARD = K.CARDS / "C31-cs-e-pandemic-cross-section.yaml"
EURO = "U2"
C15_FLAGS = {"DK": "C15 flags Denmark's window holding March 2021 as a likely reclassification, unread"}
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------- data

def is_economy(a: str) -> bool:
    return len(a) == 2 and a.isalpha() and a != EURO


def ifs_year(code: str) -> pd.Series:
    return K.ifs(code, "A")


def ifs_month(code: str) -> pd.Series:
    return K.ifs(code, "M")


def at(s: pd.Series, area: str, key) -> float:
    try:
        v = s.loc[(area, key)]
    except KeyError:
        return np.nan
    return float(v) if np.isfinite(v) else np.nan


def first_series(codes: list[str], area: str, years: list[int]) -> tuple[str | None, dict]:
    """The first of ``codes`` that gives the economy every year (the same series at both ends)."""
    for c in codes:
        s = ifs_year(c)
        vals = {y: at(s, area, y) for y in years}
        if all(np.isfinite(v) and v > 0 for v in vals.values()):
            return c, vals
    return None, {}


def ecb_month(dataset: str, mask: str) -> pd.Series:
    x = P._ecb(dataset, mask)
    return pd.Series(x.to_numpy(), index=pd.PeriodIndex(x.index, freq="M"))


def annual_mean_from_months(x: pd.Series, year: int) -> float:
    v = x[(x.index.year == year)]
    return float(v.mean()) if len(v) == 12 else np.nan


def wdi(code: str, vintage: str) -> pd.Series:
    t = worldbank.read(code, vintage).dropna(subset=["value"])
    econ = worldbank.read_economies("2026-09-30").set_index("iso3")
    iso2 = t.iso3.map(econ.iso2)
    iso2 = iso2.where(t.iso3 != "EMU", EURO)
    t = t.assign(area=iso2).dropna(subset=["area"])
    return t.set_index(["area", "year"]).value.sort_index()


def frame(prm: dict, q6: bool) -> tuple[pd.DataFrame, dict]:
    """One row per economy: m, p and every variable a variant needs, with the dropped listed by reason."""
    if q6:
        m0, m1 = (pd.Period(str(x), "M") for x in prm["q6_money"])
        i0, i1 = (pd.Period(str(x), "M") for x in prm["q6_inflation"])
        calm_years = list(range(prm["q6_calm_start_years"][0], prm["q6_calm_start_years"][1] + 1))
        ctrl_year, members = prm["q6_control_year"], set(prm["euro_members_q6"]) | set(prm["euro_joined_inside_q6_money"])
        euro_label = "euro member or joiner inside the money window: the euro area is left out of Q6"
    else:
        m0, m1 = pd.Period(str(prm["money_start"]), "M"), pd.Period(str(prm["money_end"]), "M")
        i0, i1 = pd.Period(str(prm["inflation_start"]), "M"), pd.Period(str(prm["inflation_end"]), "M")
        calm_years = list(range(prm["calm_start_years"][0], prm["calm_start_years"][1] + 1))
        ctrl_year, members = prm["control_year"], set(prm["euro_members_main"])
        euro_label = "euro member, enters as the euro area"
    y0, y1 = m0.year, m1.year
    years = list(range(y0, y1 + 1))
    led_end = y0 + 1
    unions = {a: u for u, ms in prm["unions"].items() for a in ms}
    cpi_m, cpi_a = ifs_month("PCPI_IX"), ifs_year("PCPI_IX")
    energy = wdi("EG.IMP.CONS.ZS", "2026-10-08")
    fx = ifs_year("ENDE_XDC_USD_RATE")
    guard = prm["units_guard_factor"]

    areas = sorted({a for c in ("FMB_XDC", "35L___XDC") for a in ifs_year(c).index.get_level_values(0) if is_economy(a)})
    rows, dropped = [], {euro_label: [], "no broad money at every year-end": [], "units guard": [],
                         "no price at both dates": []}
    for a in areas:
        if a in members:
            dropped[euro_label].append(a)
            continue
        code, M = first_series(["FMB_XDC", "35L___XDC"], a, years)
        if code is None:
            dropped["no broad money at every year-end"].append(a)
            continue
        steps = [M[y + 1] / M[y] for y in years[:-1]]
        if any(r >= guard or r <= 1 / guard for r in steps):
            dropped["units guard"].append(a)
            continue
        pm0, pm1 = at(cpi_m, a, i0), at(cpi_m, a, i1)
        pa0, pa1 = at(cpi_a, a, i0.year), at(cpi_a, a, i1.year)
        if np.isfinite(pm0) and np.isfinite(pm1):
            p, annual = 100 * np.log(pm1 / pm0) / 2, False
        elif np.isfinite(pa0) and np.isfinite(pa1):
            p, annual = 100 * np.log(pa1 / pa0) / 2, True
        else:
            dropped["no price at both dates"].append(a)
            continue
        calm = [at(cpi_a, a, y) / at(cpi_a, a, y - 1) for y in calm_years]
        mom_m0, mom_m1 = at(cpi_m, a, i0 - 12), at(cpi_m, a, i0)
        mom = (100 * np.log(mom_m1 / mom_m0) if not annual and np.isfinite(mom_m0) and np.isfinite(mom_m1)
               else 100 * np.log(at(cpi_a, a, i0.year) / at(cpi_a, a, i0.year - 1)))
        ccode, C = first_series(["FASAG_XDC", "12A___XDC"], a, [y0, y1])
        bcode, B = first_series(["FASMB_XDC", "14____XDC"], a, years)
        net_arg = (M[y1] - (C[y1] - C[y0])) / M[y0] if ccode else np.nan
        rows.append({
            "area": a, "cluster": unions.get(a, a), "broad_series": code, "annual_outcome": annual,
            "m": 100 * np.log(M[y1] / M[y0]) / 2, "m_led": 100 * np.log(M[led_end] / M[y0]),
            "p": p, "p_annual": 100 * np.log(pa1 / pa0) / 2 if np.isfinite(pa0) and np.isfinite(pa1) else np.nan,
            "calm_mean": 100 * (np.mean(calm) - 1) if all(np.isfinite(calm)) else np.nan,
            "energy": at(energy, a, ctrl_year), "mom": mom,
            "fx": 100 * np.log(at(fx, a, y1) / at(fx, a, y0)) / 2,
            "m_net": 100 * np.log(net_arg) / 2 if np.isfinite(net_arg) and net_arg > 0 else np.nan,
            "net_nonpositive": bool(np.isfinite(net_arg) and net_arg <= 0), "claims_series": ccode,
            "m_base": 100 * np.log(B[y1] / B[y0]) / 2 if bcode else np.nan, "base_series": bcode,
        })

    d = pd.DataFrame(rows).set_index("area")
    if q6:  # the euro area is left out of Q6 (its frozen M3 changes composition inside the money window)
        return d, {"dropped": {k: sorted(v) for k, v in dropped.items()},
                   "lacking_the_outcome_price": sorted(dropped["no price at both dates"]), "entering": int(len(d))}
    # the euro area, once
    m3 = ecb_month("BSI", "M.U2.Y.V.M30.X.1.U2.2300.Z01.E")
    hicp = ecb_month("ICP", "M.U2.N.000000.4.INX")
    M = {y: float(m3.get(pd.Period(f"{y}-12", "M"), np.nan)) for y in years}
    ha = {y: annual_mean_from_months(hicp, y) for y in range(min(calm_years) - 1, i1.year + 1)}
    calm = [ha[y] / ha[y - 1] for y in calm_years]
    rows.append({
        "area": EURO, "cluster": EURO, "broad_series": "ECB M3", "annual_outcome": False,
        "m": 100 * np.log(M[y1] / M[y0]) / 2, "m_led": 100 * np.log(M[led_end] / M[y0]),
        "p": 100 * np.log(float(hicp[i1]) / float(hicp[i0])) / 2,
        "p_annual": 100 * np.log(ha[i1.year] / ha[i0.year]) / 2,
        "calm_mean": 100 * (np.mean(calm) - 1), "energy": at(energy, EURO, ctrl_year),
        "mom": 100 * np.log(float(hicp[i0]) / float(hicp[i0 - 12])),
        "fx": 100 * np.log(at(fx, EURO, y1) / at(fx, EURO, y0)) / 2,
        "m_net": np.nan, "net_nonpositive": False, "claims_series": None, "m_base": np.nan, "base_series": None,
    })
    d = pd.DataFrame(rows).set_index("area")
    lacking_outcome = sorted(dropped["no price at both dates"])
    return d, {"dropped": {k: sorted(v) for k, v in dropped.items()}, "lacking_the_outcome_price": lacking_outcome,
               "entering": int(len(d))}


# ---------------------------------------------------------------- estimation

def design(d: pd.DataFrame, x: str, controls: list[str]) -> tuple[np.ndarray, np.ndarray]:
    X = sm.add_constant(d[[x] + controls].astype(float).to_numpy(), has_constant="add")
    return d["p"].astype(float).to_numpy(), X


def huber(d: pd.DataFrame, x: str, controls: list[str]):
    y, X = design(d, x, controls)
    return sm.RLM(y, X, M=sm.robust.norms.HuberT()).fit()


def ols(d: pd.DataFrame, x: str, controls: list[str]):
    y, X = design(d, x, controls)
    return sm.OLS(y, X).fit()


def boot(d: pd.DataFrame, x: str, controls: list[str], draws: int, seed: int, which: str = "huber") -> dict:
    rng = np.random.default_rng(seed)
    cl = d.cluster.unique()
    groups = {c: d[d.cluster == c] for c in cl}
    fit = huber if which == "huber" else ols
    out, skipped = [], 0
    for _ in range(draws):
        x_ = pd.concat([groups[c] for c in rng.choice(cl, size=len(cl), replace=True)])
        try:
            out.append(float(fit(x_, x, controls).params[1]))
        except Exception:
            skipped += 1
    lo, hi = np.percentile(out, [2.5, 97.5])
    return {"lo": float(lo), "hi": float(hi), "half_width": float((hi - lo) / 2), "draws_used": len(out),
            "skipped": skipped}


def reading(lo: float, hi: float, matters: float) -> str:
    if lo > matters:
        return "effect"
    if hi < -matters:
        return "effect of the other sign"
    if lo >= -matters and hi <= matters:
        return "too small to matter"
    return "bounded"


def read(d: pd.DataFrame, x: str, controls: list[str], prm: dict, matters: float, ols_too: bool = True) -> dict:
    d = d.dropna(subset=[x, "p"] + controls)
    h = huber(d, x, controls)
    hb = boot(d, x, controls, prm["bootstrap_draws"], prm["seed"])
    out = {"n": int(len(d)), "clusters": int(d.cluster.nunique()), "huber": float(h.params[1]), "huber_boot": hb,
           "reading": reading(hb["lo"], hb["hi"], matters), "refuted": bool(hb["hi"] < matters)}
    if ols_too:
        o = ols(d, x, controls)
        ob = boot(d, x, controls, prm["bootstrap_draws"], prm["seed"], "ols")
        out.update({"ols": float(o.params[1]), "ols_boot": ob, "ols_reading": reading(ob["lo"], ob["hi"], matters)})
        out["readings_differ"] = out["ols_reading"] != out["reading"]
        w = pd.Series(h.weights, index=d.index)
        resid = pd.Series(h.resid, index=d.index)
        low = w.nsmallest(prm["leave_one_out_downweighted_listed"]).index
        out["downweighted"] = [{"area": a, "weight": float(w[a]), "residual_sign": "+" if resid[a] > 0 else "-",
                                "money_growth_vs_mean": float(d.loc[a, x] - d[x].mean())} for a in low]
    return out


def leave_one_out(d: pd.DataFrame, controls: list[str], prm: dict, matters: float, main: dict) -> list[dict]:
    d = d.dropna(subset=["m", "p"] + controls)
    moves = []
    for c in sorted(d.cluster.unique()):
        x = d[d.cluster != c]
        h = float(huber(x, "m", controls).params[1])
        b = boot(x, "m", controls, prm["bootstrap_draws"], prm["seed"])
        r = reading(b["lo"], b["hi"], matters)
        crosses = (b["lo"] > matters) != (main["huber_boot"]["lo"] > matters) or \
                  (b["hi"] < matters) != (main["huber_boot"]["hi"] < matters)
        moves.append({"dropped": c, "huber": h, "lo": b["lo"], "hi": b["hi"], "reading": r,
                      "moves": bool(r != main["reading"] or crosses), "ols": float(ols(x, "m", controls).params[1])})
    return moves


def permutation(d: pd.DataFrame, controls: list[str], prm: dict, matters: float, observed: float,
                q6_prediction: bool = False) -> dict:
    d = d.dropna(subset=["m", "p"] + controls).copy()
    rng = np.random.default_rng(prm["seed"])
    slopes, confirms = [], 0
    small = dict(prm, bootstrap_draws=prm["permutation_bootstrap_draws"])
    for i in range(prm["permutation_draws"]):
        x = d.copy()
        x["m"] = rng.permutation(d["m"].to_numpy())
        s = float(huber(x, "m", controls).params[1])
        slopes.append(s)
        b = boot(x, "m", controls, small["bootstrap_draws"], prm["seed"] + i + 1)
        if q6_prediction:
            confirms += int(s > 0 and b["lo"] > 0)
        else:
            confirms += int(reading(b["lo"], b["hi"], matters) == "effect")
    slopes = np.array(slopes)
    out = {"draws": len(slopes), "p_value_one_sided": float((slopes >= observed).mean())}
    out["prediction_met_under_null" if q6_prediction else "false_confirmation_rate"] = confirms / len(slopes)
    return out


def concentration(x: pd.Series, k: int = 5) -> dict:
    c = (x - x.mean()) ** 2
    top = c.nlargest(k)
    return {"share_of_variance_top5": float(top.sum() / c.sum()), "top5": list(top.index), "sd": float(x.std())}


# ---------------------------------------------------------------- run

def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm, mt = card["parameters"], card["matters"]
    d_all, cover = frame(prm, q6=False)
    line = prm["calm_start_line_pct"]
    main_set = d_all[d_all.calm_mean < line]
    out = {"coverage": cover, "calm_start_unknown": sorted(d_all.index[d_all.calm_mean.isna()]),
           "main_set": sorted(main_set.index), "control_missing": sorted(main_set.index[main_set.energy.isna()])}
    E = ["energy"]
    main = read(main_set, "m", E, prm, mt["cs_e_broad_huber"])
    out["main"] = main
    out["main_no_control"] = read(main_set, "m", [], prm, mt["cs_e_broad_huber_no_control"])
    out["variants"] = {
        "a_currency": read(main_set, "m", E + ["fx"], prm, mt["cs_e_var_currency"], ols_too=False),
        "b_led": read(main_set, "m_led", E, prm, mt["cs_e_var_led"], ols_too=False),
        "c_momentum": read(main_set, "m", E + ["mom"], prm, mt["cs_e_var_momentum"], ols_too=False),
        "d_net_claims": read(main_set, "m_net", E, prm, mt["cs_e_var_net_claims"], ols_too=False),
        "e_no_hard_pegs": read(main_set[~main_set.index.isin(prm["hard_pegs_areaer_2019"])], "m", E, prm,
                               mt["cs_e_var_no_dollarised"], ols_too=False),
        "f_annual": read(main_set.assign(p=main_set.p_annual), "m", E, prm, mt["cs_e_var_annual"], ols_too=False),
        "g_all": read(d_all, "m", E, prm, mt["cs_e_var_all"], ols_too=False),
    }
    out["variants"]["d_net_claims"]["dropped_nonpositive"] = sorted(main_set.index[main_set.net_nonpositive])
    hb = main_set.dropna(subset=["m_base", "m", "p"] + E)
    out["h_base_described"] = {
        "huber": float(huber(hb, "m_base", E).params[1]), "ols": float(ols(hb, "m_base", E).params[1]),
        "huber_boot": boot(hb, "m_base", E, prm["bootstrap_draws"], prm["seed"]),
        "cor_broad": float(np.corrcoef(hb.p, hb.m)[0, 1]), "cor_base": float(np.corrcoef(hb.p, hb.m_base)[0, 1]),
        "n": int(len(hb)), "base_growth": concentration(hb.m_base.set_axis(hb.index)), "c15_flags": C15_FLAGS,
        "series": hb.base_series.value_counts().to_dict()}
    out["h_base_described"]["dcor_broad_minus_base"] = out["h_base_described"]["cor_broad"] - out["h_base_described"]["cor_base"]
    out["leave_one_out"] = leave_one_out(main_set, E, prm, mt["cs_e_broad_huber"], main)
    out["null"] = permutation(main_set, E, prm, mt["cs_e_broad_huber"], main["huber"])

    q, qcover = frame(prm, q6=True)
    qset = q[q.calm_mean < line]
    qmain = read(qset, "m", E, prm, mt["cs_e_q6_broad_huber"])
    qmain["prediction"] = "a positive Huber slope whose bootstrap interval's lower end is above 0"
    qmain["prediction_holds"] = bool(qmain["huber"] > 0 and qmain["huber_boot"]["lo"] > 0)
    out["q6"] = {"coverage": qcover, "main_set": sorted(qset.index), "read": qmain,
                 "calm_start_unknown": sorted(q.index[q.calm_mean.isna()]),
                 "null": permutation(qset, E, prm, mt["cs_e_q6_broad_huber"], qmain["huber"], q6_prediction=True)}
    out["broad_growth"] = concentration(main_set.m)
    out["calibration"] = "Huber about +-0.075 to 0.15 by cluster bootstrap on past cross-sections; OLS up to +-1.2 with one crisis economy"
    out["beside"] = {"bis67": "0.29: excess broad money Q4 2019 to Q4 2020, 30 economies, inflation to Q3 2022",
                     "cannot_separate": "the money from the fiscal demand that carried it (BIS 67 p. 5)"}
    path = cards.write_result(K.STUDY, CARD, out)
    print(path)
    return path


if __name__ == "__main__":
    main()
