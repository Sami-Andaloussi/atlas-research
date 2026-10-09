"""The long run: cards C02 (base money, every money, 1950-2020), C03 (broad money) and C04 (the
Jorda-Schularick-Taylor database, 18 economies, 1870-1950).

From the study's folder: ``../../toolkit/bin/ftpy code/longrun.py``. Writes ``results/runs/C02-a4-base.json``,
``C03-a4-broad.json``, ``C04-a4-1870.json`` and ``C21-a4-1870-named.json``; C04 and C21 read C02's result
for their out-of-sample fit. ``code/longrun.py C21`` runs C21 alone, reading C02's committed run; ``code/longrun.py C22`` runs C22 (C02's
model on windows ending in December 2019) alone, the same way, without C02's variants or window from 2020.
``code/longrun.py C23`` runs C23 (De Grauwe and Polan's 10% line on C02's model) alone, reading C02's committed run.

Readings of the cards that their text leaves to the code, fixed here before the run:

- *The sample*: the annual panel less the moneys flagged ``units_break`` and the money-years inside the euro
  outside the area; a window needs its money, the CPI and real GDP positive at both ends and neither end
  inside the euro. The euro area is one money from 1999 (its windows 2000-2010, 2010-2020).
- *The interval* is statsmodels' clustered covariance by money, normal quantiles (its default); a verdict
  "partly" is said with the side of one the interval lies on.
- *Above the line*: the window's pi (as drawn) or mu (on the regressor) above 12; "the line separates" if
  theta > 0 with p < 0.05 and beta below the line excludes 1.
- *Out-of-sample R2*: 1 - SSE(test) / sum of (test value - the training mean)^2.
- *Five folds*: the moneys' codes sorted; fold = position modulo 5; each fold's beta estimated on its own
  windows (clustered), its R2 predicted from the fit on the other four.
- *The failure clause*: the held-out windows' verdict, or two folds or more, differing from the headline's.
- *One window per money*: its first to its last year with all three series, at least 20 years apart;
  robust (HC1) errors, one observation per money.
- *The window from 2020*: to the last year in which at least half the moneys with all three series in 2020
  still have them.
- *C04*: the page's labels matched to the file's header through the codes the documentation gives them
  (``notes/data.md``); a label whose code the header lacks stops the run, and the stop is the result. Real
  GDP = the real GDP per capita index times ``pop``. The overlap check reads the
  database's series for 1950-2020 beside C02's panel for the same economies, where the panel has them; the
  two "give different betas" when their verdicts differ. C04's out-of-sample fit uses C02's headline
  coefficients as C02's run wrote them.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

from ft import cards  # noqa: E402
from ft.data import freeze  # noqa: E402

C02 = K.CARDS / "C02-a4-base.yaml"
C03 = K.CARDS / "C03-a4-broad.yaml"
C04 = K.CARDS / "C04-a4-1870.yaml"
C21 = K.CARDS / "C21-a4-1870-named.yaml"
C22 = K.CARDS / "C22-a4-base-2019-narrowed.yaml"
C23 = K.CARDS / "C23-a4-base-de-grauwe-polan.yaml"
JST = ("jst/macrohistory", "2026-09-30")
#: The database page's labels (``data/jst/macrohistory/2026-09-30/database-page.html``, "Variables overview")
#: and the codes its documentation gives them (``data/jst/documentation/2026-09-30/JST_documentationR6.pdf``,
#: "Variable names and descriptive labels in Stata", pp. 5-6): the file's header holds codes only.
JST_CODES = {"Narrow Money (nominal, local currency)": "narrowm", "Broad Money (nominal, local currency)": "money",
             "Consumer Prices (index, 1990=100)": "cpi", "Real GDP per capita (index, 2005=100)": "rgdbarro",
             "Population": "pop"}
JST_ISO2 = {"AUS": "AU", "BEL": "BE", "CAN": "CA", "CHE": "CH", "DEU": "DE", "DNK": "DK", "ESP": "ES", "FIN": "FI",
            "FRA": "FR", "GBR": "GB", "IRL": "IE", "ITA": "IT", "JPN": "JP", "NLD": "NL", "NOR": "NO", "PRT": "PT",
            "SWE": "SE", "USA": "US"}
WAR_YEARS = set(range(1914, 1919)) | set(range(1939, 1946))


def verdict(lo: float, hi: float, one: float = 1.0, zero: float = 0.0) -> str:
    holds_one, holds_zero = lo <= one <= hi, lo <= zero <= hi
    if holds_one and not holds_zero:
        return "one for one"
    if holds_zero and not holds_one:
        return "no relation"
    if not holds_one and not holds_zero:
        side = "above one" if lo > one else ("below zero" if hi < zero else "between zero and one")
        return f"partly ({side})"
    return "cannot tell"


def windows(frame: pd.DataFrame, money: str, ends: list[int], rate: bool = False) -> pd.DataFrame:
    rows = []
    for a, x in frame.groupby(level=0):
        x = x.droplevel(0)
        for y0, y1 in zip(ends[:-1], ends[1:]):
            if y0 not in x.index or y1 not in x.index:
                continue
            r0, r1 = x.loc[y0], x.loc[y1]
            vals = [r0[money], r1[money], r0.cpi, r1.cpi, r0.rgdp, r1.rgdp]
            if any(pd.isna(v) or v <= 0 for v in vals) or bool(r0.inside_euro) or bool(r1.inside_euro):
                continue
            n = y1 - y0
            row = {"area": a, "y0": y0, "y1": y1, "mu": 100 * np.log(r1[money] / r0[money]) / n,
                   "pi": 100 * np.log(r1.cpi / r0.cpi) / n, "g": 100 * np.log(r1.rgdp / r0.rgdp) / n}
            if rate:
                i0, i1 = r0.get("rate_short"), r1.get("rate_short")
                row["i0"], row["i1"] = (None if pd.isna(i0) else float(i0)), (None if pd.isna(i1) else float(i1))
            rows.append(row)
    return pd.DataFrame(rows)


def fit(df: pd.DataFrame, cols: list[str], cluster: bool = True):
    X = sm.add_constant(df[cols].astype(float))
    model = sm.OLS(df.pi.astype(float), X)
    if cluster and df.area.nunique() > 1:
        return model.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(df.area)[0]})
    return model.fit(cov_type="HC1")


def report(res, df: pd.DataFrame) -> dict:
    ci = res.conf_int(0.05)
    out = {"n": int(res.nobs), "moneys": int(df.area.nunique()), "r2": float(res.rsquared),
           "coef": {k: {"b": float(res.params[k]), "lo": float(ci.loc[k, 0]), "hi": float(ci.loc[k, 1]),
                        "p": float(res.pvalues[k])} for k in res.params.index}}
    b = out["coef"]["mu"]
    out["beta"], out["beta_lo"], out["beta_hi"] = b["b"], b["lo"], b["hi"]
    out["verdict"] = verdict(b["lo"], b["hi"])
    if "g" in out["coef"]:
        gg = out["coef"]["g"]
        out["gamma_verdict"] = verdict(gg["lo"], gg["hi"], one=-1.0)
    return out


def headline(df: pd.DataFrame) -> dict:
    return report(fit(df, ["mu", "g"]), df)


def prior_line(df: pd.DataFrame, on: str, line: float = 12.0, cluster: bool = True) -> dict:
    d = df.copy()
    d["A"] = (d[on] > line).astype(float)
    d["muA"] = d.mu * d.A
    if d.A.sum() < 2 or (1 - d.A).sum() < 2:
        return {"note": "too few windows on one side of the line", "above": int(d.A.sum())}
    res = fit(d, ["mu", "A", "muA", "g"], cluster=cluster)
    V = res.cov_params()
    below = float(res.params["mu"])
    se_b = float(np.sqrt(V.loc["mu", "mu"]))
    above = below + float(res.params["muA"])
    se_a = float(np.sqrt(V.loc["mu", "mu"] + V.loc["muA", "muA"] + 2 * V.loc["mu", "muA"]))
    z = 1.959963984540054
    theta, p_theta = float(res.params["muA"]), float(res.pvalues["muA"])
    lo_b, hi_b = below - z * se_b, below + z * se_b
    return {"windows_above": int(d.A.sum()), "windows_below": int((1 - d.A).sum()),
            "beta_below": below, "beta_below_lo": lo_b, "beta_below_hi": hi_b, "verdict_below": verdict(lo_b, hi_b),
            "beta_above": above, "beta_above_lo": above - z * se_a, "beta_above_hi": above + z * se_a,
            "verdict_above": verdict(above - z * se_a, above + z * se_a), "theta": theta, "p_theta": p_theta,
            "separates": theta > 0 and p_theta < 0.05 and not (lo_b <= 1 <= hi_b)}


def oos_r2(y: np.ndarray, pred: np.ndarray, train_mean: float) -> float:
    return float(1 - np.sum((y - pred) ** 2) / np.sum((y - train_mean) ** 2))


def held_out(df: pd.DataFrame, head: dict) -> dict:
    train = df[df.y1 <= 1990]
    test = df[df.y0 >= 1990]
    both = set(train.area) & set(test.area)
    res = fit(train, ["mu", "g"])
    pred = res.params["const"] + res.params["mu"] * test.mu + res.params["g"] * test.g
    out = {"train_windows": len(train), "test_windows": len(test), "moneys_in_both": len(both),
           "can_judge": len(both) >= 30, "oos_r2": oos_r2(test.pi.to_numpy(), pred.to_numpy(), float(train.pi.mean())),
           "fit_train": report(res, train), "test": headline(test)}
    out["same_verdict"] = out["test"]["verdict"] == head["verdict"]
    folds = []
    codes = sorted(df.area.unique())
    fold_of = {a: i % 5 for i, a in enumerate(codes)}
    for k in range(5):
        tr, te = df[df.area.map(fold_of) != k], df[df.area.map(fold_of) == k]
        r = fit(tr, ["mu", "g"])
        p = r.params["const"] + r.params["mu"] * te.mu + r.params["g"] * te.g
        own = headline(te)
        folds.append({"fold": k, "windows": len(te), "moneys": int(te.area.nunique()),
                      "oos_r2": oos_r2(te.pi.to_numpy(), p.to_numpy(), float(tr.pi.mean())),
                      "beta": own["beta"], "beta_lo": own["beta_lo"], "beta_hi": own["beta_hi"],
                      "verdict": own["verdict"]})
    out["folds"] = folds
    out["folds_differing"] = sum(f["verdict"] != head["verdict"] for f in folds)
    out["holds"] = (out["same_verdict"] or not out["can_judge"]) and out["folds_differing"] < 2
    return out


def panel_frame(money: str) -> pd.DataFrame:
    p = K.annual()
    p = p[~p.units_break].copy()
    return p


def last_common_year(frame: pd.DataFrame, money: str) -> int | None:
    ok = frame[[money, "cpi", "rgdp"]].notna().all(axis=1) & ~frame.inside_euro.astype(bool)
    have = ok[ok].index
    y2020 = {a for a, y in have if y == 2020}
    if not y2020:
        return None
    last = None
    for y in range(2021, 2031):
        n = len({a for a, yy in have if yy == y} & y2020)
        if n >= 0.5 * len(y2020):
            last = y
    return last


def variants(frame: pd.DataFrame, money: str, seam_col: str, head_df: pd.DataFrame) -> dict:
    out = {}
    out["five-year windows"] = headline(windows(frame, money, list(range(1950, 2021, 5))))
    out["twenty-year windows"] = headline(windows(frame, money, [1950, 1970, 1990, 2010]))
    rows = []
    for a, x in frame.groupby(level=0):
        x = x.droplevel(0)
        ok = x[[money, "cpi", "rgdp"]].gt(0).all(axis=1) & ~x.inside_euro.astype(bool)
        years = x.index[ok]
        if len(years) and years.max() - years.min() >= 20:
            y0, y1 = int(years.min()), int(years.max())
            n = y1 - y0
            rows.append({"area": a, "y0": y0, "y1": y1, "mu": 100 * np.log(x.loc[y1, money] / x.loc[y0, money]) / n,
                         "pi": 100 * np.log(x.loc[y1, "cpi"] / x.loc[y0, "cpi"]) / n,
                         "g": 100 * np.log(x.loc[y1, "rgdp"] / x.loc[y0, "rgdp"]) / n})
    one = pd.DataFrame(rows)
    out["one window per money"] = report(fit(one, ["mu", "g"], cluster=False), one)
    seams = set(frame[frame[seam_col].astype(bool)].index.get_level_values(0))
    d = head_df[~head_df.area.isin(seams)]
    out["seam-flagged moneys dropped"] = headline(d)
    out["without g"] = report(fit(head_df, ["mu"]), head_df)
    dd = head_df.copy()
    for y in sorted(dd.y1.unique())[1:]:
        dd[f"w{y}"] = (dd.y1 == y).astype(float)
    out["window dummies"] = report(fit(dd, ["mu", "g", *[c for c in dd.columns if c.startswith("w")]]), dd)
    wr = windows(frame, money, list(range(1950, 2021, 10)), rate=True)
    wr = wr[(wr.i0 >= 1) & (wr.i1 >= 1)].copy()
    wr["mu"] = wr.mu + 0.5 * 100 * np.log(wr.i1 / wr.i0) / (wr.y1 - wr.y0)
    out["yield correction (rates at least 1% at both ends)"] = headline(wr)
    return out


def a4(card_path: Path, money: str, seam_col: str, extra=None) -> dict:
    card = yaml.safe_load(card_path.read_text())
    cards.require_locked(card_path)
    frame = panel_frame(money)
    ends = card["parameters"]["window_ends"]
    df = windows(frame, money, ends)
    head = headline(df)
    out = {"sample": {"windows": len(df), "moneys": int(df.area.nunique()),
                      "moneys_dropped_units_break": sorted(K.annual()[K.annual().units_break].index.get_level_values(0).unique()),
                      "list": df[["area", "y0", "y1"]].astype(str).agg(" ".join, axis=1).tolist()},
           "headline": head,
           "prior_line_on_pi": prior_line(df, "pi"), "prior_line_on_mu": prior_line(df, "mu"),
           "held_out": held_out(df, head), "variants": variants(frame, money, seam_col, df)}
    last = last_common_year(frame, money)
    if last:
        recent = windows(frame, money, [2020, last])
        out["from_2020"] = {"to": last, **(headline(recent) if len(recent) > 10 else {"n": len(recent)})}
    out["points"] = df.round(4).to_dict("records")
    if extra:
        out.update(extra(frame, df, head))
    return out, card_path


def broad_extra(frame: pd.DataFrame, df: pd.DataFrame, head: dict) -> dict:
    wbdf = windows(frame, "broad_wb", list(range(1950, 2021, 10)))
    base = windows(K.annual()[~K.annual().units_break], "base", list(range(1950, 2021, 10)))
    key = ["area", "y0", "y1"]
    common = df.merge(base[key], on=key)
    base_common = base.merge(df[key], on=key)
    c_b, c_base = headline(common), headline(base_common)
    return {"world_bank_broad": headline(wbdf),
            "beside_C02": {"common_windows": len(common), "beta_broad_common": c_b["beta"], "verdict_broad_common": c_b["verdict"],
                           "beta_base_common": c_base["beta"], "verdict_base_common": c_base["verdict"],
                           "only_in_C03": int(len(df) - len(common)), "only_in_C02": int(len(base) - len(base_common)),
                           "depends_on_the_aggregate": c_b["verdict"] != c_base["verdict"]}}


GDP_LABEL = "Real GDP per capita (index, 2005=100)"


def card_gdp_column(card: dict) -> str | None:
    """C21's column for the real GDP per capita index, from its card's ``real_gdp_per_capita_column`` (the
    parameter's first word; the rest of it says why); C04 names none and keeps the documentation's code."""
    value = (card.get("parameters") or {}).get("real_gdp_per_capita_column")
    return str(value).split()[0] if value else None


def jst_frame(gdp_column: str | None = None) -> tuple[pd.DataFrame | None, dict]:
    """The database's columns for the page's labels, through the documentation's codes; a label whose code
    the file's header lacks stops the run (C04: never guessed). ``gdp_column`` is the column a card names
    for the real GDP per capita index (C21), in place of the documentation's code for it."""
    codes = dict(JST_CODES)
    if gdp_column:
        codes[GDP_LABEL] = gdp_column
    fz = freeze.load(*JST)
    raw = fz.read_bytes("JSTdatasetR6.dta")
    header = list(pd.io.stata.StataReader(io.BytesIO(raw)).variable_labels())
    missing = {label: code for label, code in codes.items() if code not in header}
    info = {"codes": codes, "header": header, "missing": missing}
    if missing:
        return None, info
    d = pd.read_stata(io.BytesIO(raw))
    d = d.assign(area=d.iso.map(JST_ISO2), year=d.year.astype(int))
    d["rgdp"] = d[codes[GDP_LABEL]] * d["pop"]
    d["inside_euro"] = False
    frame = d.set_index(["area", "year"])[["narrowm", "money", "cpi", "rgdp", "inside_euro"]].sort_index()
    return frame, info


def c04(c02_result: dict, card_path: Path = C04) -> dict:
    """C04, or its child C21 (``card_path``): the same run, C21 naming the real GDP per capita column."""
    card = yaml.safe_load(card_path.read_text())
    cards.require_locked(card_path)
    frame, info = jst_frame(card_gdp_column(card))
    if frame is None:
        return {"stopped": True,
                "reason": "a label on the database's page has no matching column in the file: " + "; ".join(
                    f"{label!r} is {code!r} in the documentation, absent from the file's header"
                    for label, code in info["missing"].items()) + " - the card forbids a guess",
                "dataset": {"name": JST[0], "vintage": JST[1], "file": "JSTdatasetR6.dta"},
                "columns": info}
    ends = card["parameters"]["window_ends"]
    df = windows(frame, "narrowm", ends)
    head = headline(df)
    coef = c02_result["headline"]["coef"]
    pred = coef["const"]["b"] + coef["mu"]["b"] * df.mu + coef["g"]["b"] * df.g
    oos = {"oos_r2_from_C02": oos_r2(df.pi.to_numpy(), pred.to_numpy(), float(df.pi.mean())),
           "note": "C02's headline coefficients (1950-2020, every money) predicting 1870-1950, against the 1870-1950 mean"}
    codes = sorted(df.area.unique())
    fold_of = {a: i % 5 for i, a in enumerate(codes)}
    folds = []
    for k in range(5):
        tr, te = df[df.area.map(fold_of) != k], df[df.area.map(fold_of) == k]
        r = fit(tr, ["mu", "g"])
        p = r.params["const"] + r.params["mu"] * te.mu + r.params["g"] * te.g
        own = headline(te) if te.area.nunique() > 1 else report(fit(te, ["mu", "g"], cluster=False), te)
        folds.append({"fold": k, "economies": sorted(te.area.unique()), "windows": len(te),
                      "oos_r2": oos_r2(te.pi.to_numpy(), p.to_numpy(), float(tr.pi.mean())),
                      "beta": own["beta"], "verdict": own["verdict"]})
    war = df[~df.apply(lambda r: any(r.y0 <= y <= r.y1 for y in WAR_YEARS), axis=1)]
    var = {"broad money": headline(windows(frame, "money", ends)),
           "world-war windows apart": headline(war) if len(war) > 10 else {"n": len(war)},
           "five-year windows": headline(windows(frame, "narrowm", list(range(1870, 1951, 5))))}
    jst_post = windows(frame, "narrowm", list(range(1950, 2021, 10)))
    panel = K.annual()
    panel = panel[~panel.units_break]
    pan = windows(panel, "base", list(range(1950, 2021, 10)))
    pan = pan[pan.area.isin(set(JST_ISO2.values()))]
    overlap = {"jst_1950_2020": headline(jst_post), "panel_same_economies": headline(pan) if len(pan) > 10 else {"n": len(pan)},
               "panel_economies": sorted(pan.area.unique())}
    overlap["different"] = overlap["panel_same_economies"].get("verdict") != overlap["jst_1950_2020"]["verdict"]
    return {"stopped": False,
            "dataset": {"name": f"{JST[0]}", "vintage": JST[1], "file": "JSTdatasetR6.dta", "columns": info},
            "sample": {"windows": len(df), "economies": int(df.area.nunique())},
            "headline": head, "vs_C02": {"C02_verdict": c02_result["headline"]["verdict"],
                                         "same": head["verdict"] == c02_result["headline"]["verdict"]},
            "prior_line_on_pi": prior_line(df, "pi"), "prior_line_on_mu": prior_line(df, "mu"),
            "out_of_sample": oos, "folds": folds, "variants": var, "overlap_1950_2020": overlap,
            "points": df.round(4).to_dict("records")}


def main() -> list[Path]:
    r02, p02 = a4(C02, "base", "base_break")
    out02 = cards.write_result(K.STUDY, p02, r02)
    r03, p03 = a4(C03, "broad", "broad_break", extra=broad_extra)
    out03 = cards.write_result(K.STUDY, p03, r03)
    r04 = c04(json.loads(out02.read_text())["result"])
    out04 = cards.write_result(K.STUDY, C04, r04)
    out21 = c21(json.loads(out02.read_text())["result"])
    out22 = c22(json.loads(out02.read_text())["result"])
    out23 = c23(json.loads(out02.read_text())["result"])
    print(out02, out03, out04, out21, out22, out23)
    return [out02, out03, out04, out21, out22, out23]


def place(mu: float, pi: float, line: float = 12.0) -> str:
    """C22's placement of a named point by C02's line as C02 draws it (above = more than the line)."""
    if mu > line and not pi > line:
        return "above the line on money growth, below it on inflation"
    if mu > line:
        return "above the line on both"
    return "below the line on money growth"


def c22(c02_result: dict | None = None) -> Path:
    """C22: C02's model on the grid its card names (year-ends 1949-2019), its headline, its line both ways
    and C02's held-out checks - never C02's variants nor its window from 2020 (the card check's M5); the
    named points beside C02's 2010-2020 points, placed by C02's line."""
    card = yaml.safe_load(C22.read_text())
    cards.require_locked(C22)
    if c02_result is None:
        c02_result = json.loads((K.RUNS / "C02-a4-base.json").read_text())["result"]
    frame = panel_frame("base")
    ends = card["parameters"]["window_ends"]
    df = windows(frame, "base", ends)
    head = headline(df)
    line = float(card["parameters"]["prior_line_teles_uhlig_pct"])
    c02_pts = {(p["area"], int(p["y0"])): p for p in c02_result["points"]}
    exception = set(card["parameters"]["exception_named"])
    named = []
    for area in card["parameters"]["points_named"]:
        mine = df[(df.area == area) & (df.y1 == ends[-1])]
        old = c02_pts.get((area, 2010))
        row = {"area": area, "in_exception": area in exception,
               "c02_2010_2020": None if old is None else {"mu": old["mu"], "pi": old["pi"],
                                                         "placed": place(old["mu"], old["pi"], line)}}
        if len(mine):
            m = mine.iloc[0]
            row[f"c22_{ends[-2]}_{ends[-1]}"] = {"mu": float(m.mu), "pi": float(m.pi),
                                                 "placed": place(float(m.mu), float(m.pi), line)}
            if area in exception:
                row["shows_the_exception_without_2020"] = place(float(m.mu), float(m.pi), line) == (
                    "above the line on money growth, below it on inflation")
        named.append(row)
    pl_mu = prior_line(df, "mu", line)
    c02_mu = c02_result["prior_line_on_mu"]
    beside = {"C02_verdict": c02_result["headline"]["verdict"], "C22_verdict": head["verdict"],
              "C02_line_on_mu_separates": c02_mu.get("separates"), "C22_line_on_mu_separates": pl_mu.get("separates")}
    beside["differs"] = (beside["C02_verdict"] != beside["C22_verdict"]
                         or beside["C02_line_on_mu_separates"] != beside["C22_line_on_mu_separates"])
    out = {"sample": {"windows": len(df), "moneys": int(df.area.nunique()),
                      "windows_by_start": {int(k): int(v) for k, v in df.groupby("y0").size().items()},
                      "list": df[["area", "y0", "y1"]].astype(str).agg(" ".join, axis=1).tolist()},
           "headline": head, "prior_line_on_pi": prior_line(df, "pi", line), "prior_line_on_mu": pl_mu,
           "held_out": held_out(df, head), "named_points": named, "beside_C02": beside,
           "points": df.round(4).to_dict("records")}
    return cards.write_result(K.STUDY, C22, out)


def _line_reading(d: pd.DataFrame, line: float, *, cluster: bool = True, min_side: int = 20,
                  on_ways: tuple[str, ...] = ("pi", "mu")) -> dict:
    """C23's reading of a line on a set of windows: the model's headline, and the line drawn on inflation
    (as the abstract states it) and on money growth (beside), each said thin where a side holds fewer than
    ``min_side`` observations (C23's failure clause: a thin reading counts neither way)."""
    out = {"n": int(len(d)), "moneys": int(d.area.nunique()),
           "headline": report(fit(d, ["mu", "g"], cluster=cluster), d)}
    for on in on_ways:
        p = prior_line(d, on, line, cluster)
        if "windows_above" in p:
            p["thin"] = bool(p["windows_above"] < min_side or p["windows_below"] < min_side)
            p["moneys_above"] = int(d[d[on] > line].area.nunique())
            p["moneys_below"] = int(d[~(d[on] > line)].area.nunique())
        else:
            p["thin"] = True
        out[f"line_on_{on}"] = p
    return out


def c23(c02_result: dict | None = None) -> Path:
    """C23: C02's model with De Grauwe and Polan's 10% line (their abstract's), on the card's windows - the
    headline reading (the line on the window's inflation, beside it on money growth), variant A (C22's grid),
    variant B (one thirty-year window per money, 1970-2000, robust errors), variant C (the money classified by
    the mean of its windows' inflation), and the windows wholly outside 1970-2000 apart; Teles and Uhlig's 12%
    read from C02's committed run beside. The card's section (8) says in words what the readings together mean;
    this code only computes the quantities that sentence names."""
    card = yaml.safe_load(C23.read_text())
    cards.require_locked(C23)
    if c02_result is None:
        c02_result = json.loads((K.RUNS / "C02-a4-base.json").read_text())["result"]
    prm = card["parameters"]
    line = float(prm["prior_line_de_grauwe_polan_pct"])
    frame = panel_frame("base")
    df = windows(frame, "base", prm["window_ends"])
    head = _line_reading(df, line)
    var_a = _line_reading(windows(frame, "base", prm["window_ends_variant_A"]), line)
    b_ends = prm["window_variant_B"]
    thirty = windows(frame, "base", b_ends)
    var_b = _line_reading(thirty, line, cluster=False, min_side=10)
    var_b["thin_overall"] = bool(len(thirty) < 30)
    # variant C: the money's own mean inflation over its windows (equal weights), above the line = high
    mean_pi = df.groupby("area").pi.mean()
    dc = df.assign(mpi=df.area.map(mean_pi))
    var_c = {"n": int(len(dc)), "moneys": int(dc.area.nunique()),
             "moneys_high": int((mean_pi > line).sum()), "moneys_low": int((mean_pi <= line).sum()),
             "line_on_money": prior_line(dc, "mpi", line)}
    p = var_c["line_on_money"]
    var_c["line_on_money"]["thin"] = bool("windows_above" not in p or min(p["windows_above"], p["windows_below"]) < 20)
    outside = df[(df.y0 >= 2000) | (df.y1 <= 1970)]
    apart = _line_reading(outside, line)
    inside = df[~df.index.isin(outside.index)]
    # Teles and Uhlig's 12% from C02's committed run, and how few windows lie between the two lines
    tu = {on: c02_result[f"prior_line_on_{on}"] for on in ("pi", "mu")}
    between = {on: int(((df[on] > line) & ~(df[on] > 12.0)).sum()) for on in ("pi", "mu")}
    # the card's section (8), as quantities: does each reading separate on the pi split (thin ones count neither way)
    def sep(r: dict, on: str = "pi") -> bool | None:
        p = r[f"line_on_{on}"] if f"line_on_{on}" in r else r["line_on_money"]
        return None if p.get("thin") else bool(p.get("separates"))
    readings = {"headline_pi": sep(head, "pi"), "headline_mu": sep(head, "mu"), "A_pi": sep(var_a, "pi"),
                "A_mu": sep(var_a, "mu"), "B_pi": sep(var_b, "pi") if not var_b["thin_overall"] else None,
                "B_mu": sep(var_b, "mu") if not var_b["thin_overall"] else None, "C": sep(var_c),
                "outside_1970_2000_pi": sep(apart, "pi"), "outside_1970_2000_mu": sep(apart, "mu")}
    pi_variants = [readings[k] for k in ("A_pi", "B_pi", "C") if readings[k] is not None]
    if readings["headline_pi"] is False:
        says = "does not hold"
    elif (readings["headline_pi"] and readings["headline_mu"] and all(pi_variants)):
        says = "holds"
    else:
        says = "holds on one reading and not on another"
    out = {"sample": {"windows": len(df), "moneys": int(df.area.nunique()),
                      "windows_by_start": {int(k): int(v) for k, v in df.groupby("y0").size().items()},
                      "windows_inside_1970_2000": int(len(inside)), "windows_outside_1970_2000": int(len(outside)),
                      "thirty_year_moneys": sorted(thirty.area.unique()),
                      "list": df[["area", "y0", "y1"]].astype(str).agg(" ".join, axis=1).tolist()},
           "headline": head, "variant_A_c22_grid": var_a, "variant_B_thirty_years": var_b,
           "variant_C_money_classified": var_c, "outside_1970_2000": apart,
           "teles_uhlig_12_from_C02": tu, "windows_between_10_and_12": between,
           "separates_by_reading": readings, "read_together": says, "points": df.round(4).to_dict("records")}
    return cards.write_result(K.STUDY, C23, out)


def c21(c02_result: dict | None = None) -> Path:
    """C21 alone: C04 with the column its card names; C02's headline read from C02's committed run."""
    if c02_result is None:
        c02_result = json.loads((K.RUNS / "C02-a4-base.json").read_text())["result"]
    return cards.write_result(K.STUDY, C21, c04(c02_result, C21))


if __name__ == "__main__":
    if sys.argv[1:] == ["C21"]:
        print(c21())
    elif sys.argv[1:] == ["C22"]:
        print(c22())
    elif sys.argv[1:] == ["C23"]:
        print(c23())
    else:
        main()
