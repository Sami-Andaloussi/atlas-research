"""Cards C28 (C25's child, a correction: C25's and C27's readings with a units guard on the World Bank fills) and
C29 (C28's child, an exploration written after the grid checks of 2026-10-07: where the slope changes with the pace
of money growth, its influential decades, and a null simulation of the line rule).

From the study's folder: ``../../toolkit/bin/ftpy code/units_guard.py C28`` (then ``C29``). Each refuses to run
unless its card is committed and unchanged; each writes ``results/runs/<card>.json``.

Readings of the cards that their text leaves to the code, fixed here before the runs:

- *C28's guard* is applied to the annual panel after C25's fill (``gap5_fill.filled_annual``) and before any window;
  a switched variable keeps the panel's rows (a year the World Bank lacks becomes missing). The reproduction with
  the guard off is C25's filled summaries on both grids and C27's filled summary, compared with ``gap5_fill.same``.
- *C29's slices* read C28's points for C02's grid on base money. A band's model is C02's (pi on mu and g, errors
  clustered by money). "From 2000" is a window whose first year is 2000 or later; "outside 1970-2000", a window
  ending in or before 1970 or starting in or after 2000. The union clusters: one cluster per union for its members,
  one per economy otherwise. The null simulation keeps each draw's design fixed (mu, g, the windows) and draws
  pi* = fitted + w * residual with one Rademacher w per money, the fit and residuals from the pooled model.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import gap5_fill as G  # noqa: E402
import longrun as L  # noqa: E402
import panel as P  # noqa: E402

from ft import cards  # noqa: E402

C28 = K.CARDS / "C28-a4-units-guard.yaml"
C29 = K.CARDS / "C29-a4-exploration-pace.yaml"
WB = {"rgdp": "NY.GDP.MKTP.KN", "cpi": "FP.CPI.TOTL", "gdp": "NY.GDP.MKTP.CN"}
UNIONS = {"WAEMU": ["BJ", "BF", "CI", "GW", "ML", "NE", "SN", "TG"], "CEMAC": ["CM", "CF", "TD", "CG", "GQ", "GA"],
          "ECCU": ["AG", "DM", "GD", "KN", "LC", "VC"]}
DOLLARISED = {"PA": 1950, "EC": 2000, "SV": 2000}  # windows starting in or after this year use another's money


# --- C28 ------------------------------------------------------------------------------------------------

def guard(a: pd.DataFrame, tol: float) -> tuple[pd.DataFrame, dict]:
    out, switched = a.copy(), {}
    for var, code in WB.items():
        wb = P._wb(code)
        switched[var] = []
        for area, x in a[var].groupby(level=0):
            if area in ("US", "U2") or area not in wb.index.get_level_values(0):
                continue
            x = x.droplevel(0).dropna()
            x = x[x > 0]
            w = wb.xs(area)
            w = w[w > 0]
            both = x.index.intersection(w.index)
            if len(both) < 2:
                continue
            r = x[both] / w[both]
            if r.max() / r.min() >= tol:
                rows = out.loc[area].index
                out.loc[(area, slice(None)), var] = w.reindex(rows).to_numpy()
                switched[var].append({"area": area, "spread": float(r.max() / r.min()), "overlap_years": int(len(both))})
    return out, switched


def c28() -> Path:
    card = yaml.safe_load(C28.read_text())
    cards.require_locked(C28)
    prm = card["parameters"]
    ends, ends22 = prm["window_ends"], prm["window_ends_beside_C22"]
    c25 = json.loads((K.RUNS / "C25-a4-base-hko-fill.json").read_text())["result"]
    c27 = json.loads((K.RUNS / "C27-a4-broad-hko-fill.json").read_text())["result"]
    a_f, _, _ = G.filled_annual(K.annual())
    off = a_f[~a_f.units_break]
    g_f, switched = guard(a_f, prm["units_guard_max_over_min"])
    on = g_f[~g_f.units_break]
    readings = {"C02_grid": (ends, "base", c25["C02_grid"]["filled"]), "C22_grid": (ends22, "base", c25["C22_grid"]["filled"]),
                "broad": (ends, "broad", c27["filled"])}
    reproduces = {}
    for tag, (grid, money, stored) in readings.items():
        _, r = G.a4_reading(off, grid, money=money)
        reproduces[tag] = G.same(G.jsonable(G.summary_of(r)), stored)
    expected = {v: sorted(prm["guard_switches_before_the_run"][v]) for v in WB}
    out: dict = {"void": not all(reproduces.values()), "reproduces_stored": reproduces, "switched": switched,
                 "switches_as_counted": {v: sorted(s["area"] for s in switched[v]) == expected[v] for v in WB}}
    if out["void"]:
        out["note"] = "with the guard off, the run did not reproduce C25's and C27's stored results: nothing is read"
        return cards.write_result(K.STUDY, C28, G.clean(out))
    for tag, (grid, money, stored) in readings.items():
        df_off, r_off = G.a4_reading(off, grid, money=money)
        df_on, r_on = G.a4_reading(on, grid, money=money)
        key = ["area", "y0", "y1"]
        mm = df_off.merge(df_on, on=key, how="outer", suffixes=("_off", "_on"), indicator=True)
        changed = mm[(mm._merge != "both") | ((mm.mu_off - mm.mu_on).abs() > 1e-12) | ((mm.pi_off - mm.pi_on).abs() > 1e-12)
                     | ((mm.g_off - mm.g_on).abs() > 1e-12)]
        out[tag] = {"guarded": G.summary_of(r_on), "unguarded": stored, "differs": G.differs(r_off, r_on),
                    "windows_changed": changed.drop(columns="_merge").round(4).to_dict("records"),
                    "points": df_on.round(4).to_dict("records")}
    return cards.write_result(K.STUDY, C28, G.clean(out))


# --- C29 ------------------------------------------------------------------------------------------------

Z = 1.959963984540054


def _slope(d: pd.DataFrame, groups=None) -> dict:
    if len(d) < 3:
        return {"note": "too few windows", "windows": int(len(d))}
    X = sm.add_constant(d[["mu", "g"]].astype(float))
    g = groups if groups is not None else pd.factorize(d.area)[0]
    res = sm.OLS(d.pi.astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": g})
    b, se = float(res.params["mu"]), float(res.bse["mu"])
    gam, gse = float(res.params["g"]), float(res.bse["g"])
    return {"beta": b, "lo": b - Z * se, "hi": b + Z * se, "gamma": gam, "gamma_lo": gam - Z * gse,
            "gamma_hi": gam + Z * gse, "windows": int(len(d)), "moneys": int(d.area.nunique())}


def _line(d: pd.DataFrame, line: float, min_side: int, groups=None) -> dict:
    A = (d.mu > line)
    if A.sum() < min_side or (~A).sum() < min_side:
        return {"note": f"fewer than {min_side} windows on a side", "above": int(A.sum()), "below": int((~A).sum())}
    if groups is None:
        return L.prior_line(d, "mu", line)
    x = d.copy()
    x["A"] = A.astype(float)
    x["muA"] = x.mu * x.A
    res = sm.OLS(x.pi.astype(float), sm.add_constant(x[["mu", "A", "muA", "g"]].astype(float))).fit(
        cov_type="cluster", cov_kwds={"groups": groups})
    V = res.cov_params()
    below, above = float(res.params["mu"]), float(res.params["mu"] + res.params["muA"])
    se_b = float(np.sqrt(V.loc["mu", "mu"]))
    se_a = float(np.sqrt(V.loc["mu", "mu"] + V.loc["muA", "muA"] + 2 * V.loc["mu", "muA"]))
    return {"windows_above": int(A.sum()), "windows_below": int((~A).sum()), "beta_below": below,
            "beta_below_lo": below - Z * se_b, "beta_below_hi": below + Z * se_b, "beta_above": above,
            "beta_above_lo": above - Z * se_a, "beta_above_hi": above + Z * se_a,
            "theta": float(res.params["muA"]), "p_theta": float(res.pvalues["muA"])}


def _union_of(area: str) -> str:
    for u, members in UNIONS.items():
        if area in members:
            return u
    return area


def c29() -> Path:
    card = yaml.safe_load(C29.read_text())
    cards.require_locked(C29)
    prm = card["parameters"]
    line, ms = prm["line"], prm["min_side"]
    c28 = json.loads((K.RUNS / "C28-a4-units-guard.json").read_text())["result"]
    assert not c28["void"], "C28 is void"
    d = pd.DataFrame(c28["C02_grid"]["points"])
    out: dict = {"windows": int(len(d)), "moneys": int(d.area.nunique())}
    bands = {"S1_band_le12": d.mu <= 12, "S2_band_12_20": (d.mu > 12) & (d.mu <= 20),
             "S3_band_20_30": (d.mu > 20) & (d.mu <= 30), "S4_band_30_50": (d.mu > 30) & (d.mu <= 50),
             "S5_band_gt50": d.mu > 50}
    for k, m in bands.items():
        out[k] = _slope(d[m])
    out["S6_above_line_without_gt30"] = _line(d[d.mu <= 30], line, ms)
    out["S7_from_2000"] = _line(d[d.y0 >= 2000], line, ms)
    outside = d[(d.y1 <= 1970) | (d.y0 >= 2000)]
    out["S8_outside_1970_2000"] = {"pooled": _slope(outside), "line": _line(outside, line, ms)}
    c22 = c28["C22_grid"]["guarded"]["held_out"]
    c02 = c28["C02_grid"]["guarded"]["held_out"]
    out["S9_held_out_1999"] = {"C22_grid_held_out": {k: c22[k] for k in ("beta", "lo", "hi", "verdict", "test_windows")},
                               "C02_grid_held_out_1990": {k: c02[k] for k in ("beta", "lo", "hi", "verdict", "test_windows")},
                               "C22_folds_differing": c28["C22_grid"]["guarded"]["folds_differing"]}
    members = {a for m in UNIONS.values() for a in m}
    dollar = d.apply(lambda r: r.area in DOLLARISED and r.y0 >= DOLLARISED[r.area], axis=1)
    keep = d[~d.area.isin(members) & ~dollar]
    out["S10_without_unions"] = {"line": _line(keep, line, ms), "windows_dropped": int(len(d) - len(keep)),
                                 "moneys_left": int(keep.area.nunique())}
    out["S11_cluster_by_union"] = _line(d, line, ms, groups=pd.factorize(d.area.map(_union_of))[0])
    out["S12_without_shrinking_base"] = {"line": _line(d[d.mu >= 0], line, ms),
                                         "windows_dropped": d[d.mu < 0][["area", "y0", "y1", "mu"]].round(2).to_dict("records")}
    wb = P._wb(WB["rgdp"])
    gw, used = [], 0
    for _, r in d.iterrows():
        try:
            v0, v1 = wb.loc[(r.area, int(r.y0))], wb.loc[(r.area, int(r.y1))]
        except KeyError:
            v0 = v1 = np.nan
        if v0 > 0 and v1 > 0:
            gw.append(100 * np.log(v1 / v0) / (r.y1 - r.y0))
            used += 1
        else:
            gw.append(r.g)
    dw = d.assign(g=gw)
    out["S13_g_from_world_bank"] = {"pooled": _slope(dw), "line": _line(dw, line, ms),
                                    "windows_with_world_bank_g": used}
    ab, be = d[d.mu > line], d[d.mu <= line]
    out["S14_levels"] = {"median_pi_over_mu_above": float((ab.pi / ab.mu).median()),
                         "ratio_of_medians_below": float(be.pi.median() / be.mu.median()),
                         "share_above_within_3_or_more": float(((ab.pi >= ab.mu - 3)).mean()),
                         "median_gap_above": float((ab.mu - ab.pi).median())}
    # the null simulation
    obs = L.prior_line(d, "mu", line)
    X = sm.add_constant(d[["mu", "g"]].astype(float))
    fit0 = sm.OLS(d.pi.astype(float), X).fit()
    rng = np.random.default_rng(prm["seed"])
    codes, inv = np.unique(d.area.to_numpy(), return_inverse=True)
    sep, ge = 0, 0
    for _ in range(prm["bootstrap_draws"]):
        w = rng.choice([-1.0, 1.0], size=len(codes))[inv]
        ds = d.assign(pi=fit0.fittedvalues.to_numpy() + w * fit0.resid.to_numpy())
        p = L.prior_line(ds, "mu", line)
        sep += bool(p.get("separates"))
        ge += p.get("theta", -np.inf) >= obs["theta"]
    out["S15_null"] = {"draws": prm["bootstrap_draws"], "share_separates": sep / prm["bootstrap_draws"],
                       "share_theta_at_least_observed": ge / prm["bootstrap_draws"], "observed_theta": obs["theta"],
                       "observed_separates": obs["separates"]}
    return cards.write_result(K.STUDY, C29, G.clean(out))


if __name__ == "__main__":
    {"C28": c28, "C29": c29}[sys.argv[1]]()
