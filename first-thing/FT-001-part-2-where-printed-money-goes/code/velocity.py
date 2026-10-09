""""No one spends"? - card C19 (C17 with its additions removed): US broad money's velocity against the
interest rate, fitted before the first printing and tested after, on M2 and on M2 net of the Federal
Reserve's purchases; the counted variants; across moneys from C15's list.

From the study's folder, after ``frame_e.py``: ``../../toolkit/bin/ftpy code/velocity.py``. Writes
``results/runs/C19-velocity-bare.json``.

Readings of the cards (C07, C14, C17, C19) that their text leaves to the code, fixed here before the run:

- *Quarters*: M2V as FRED gives it; the bill rate (TB3MS), M2 (M2SL) and the Fed's holdings (TREAST,
  WSHOMCB, weekly) as the quarter's mean; a quarter needs its three months.
- *The in-sample residuals' standard deviation* uses one degree of freedom (numpy ``ddof=1``).
- *z's verdict* per form: "fit cannot tell" if the in-sample R2 < 0.3; else |z| <= 1 "moved as the rate
  predicts"; z <= -2 "fell below"; z >= 2 "stayed above"; otherwise "between". A series' verdict is the one
  two forms of three or more give; where none has two, "the forms disagree".
- *Mortgage-backed securities before WSHOMCB's first week* are read as zero (the Federal Reserve bought
  none before January 2009, `notes/fed-statements.md`), so S(f) at the fit's last quarter is the Treasuries
  alone.
- *The X-Y variant's cutoffs* come from C15's other eight lists (the list that dates the headline cutoff),
  each list's first US episode not set apart that leaves 40 quarters of fit.
- *The splits* of the test period stay C07's (C05's later US starts): descriptive pieces only.
- *Across moneys*: V = nominal GDP over the mean of broad money at the year's two ends; the rate is the
  panel's annual short rate; a year counts when V and the rate exist; 20 such years before m0's year are
  needed; moneys and years the panel flags (units, euro use outside the area) are out; the log-log form
  drops years with a rate at or below -1.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import frame_e as F  # noqa: E402

from ft import cards  # noqa: E402

CARD = K.CARDS / "C19-velocity-bare.yaml"
C15 = K.RUNS / "C15-e-episodes-closed.json"
C05 = K.RUNS / "C05-e-episodes.json"
FORMS = ("log-log", "semi-log", "Selden-Latane")
SENTENCES = {
    ("fell below", "fell below"): "velocity fell beyond what the rate predicts, even net of all the Fed's "
                                  "purchases - money held rather than spent",
    ("fell below", "moved as the rate predicts"): "the fall was no larger than the Fed's purchases; how much "
                                                  "was deposits created and how much money held cannot be told "
                                                  "from these series",
    ("fell below", "stayed above"): "the Fed's purchases exceed the fall; since subtracting them all overstates "
                                    "the deposits created, velocity net of created deposits lies between the two "
                                    "readings, and these series cannot place it",
    ("fell below", "between"): "velocity fell beyond what the rate predicts on M2; net of the Fed's purchases, we "
                               "cannot conclude",
}


def xy(form: str, v: pd.Series, r: pd.Series) -> tuple[pd.Series, pd.Series]:
    if form == "log-log":
        ok = r > -1
        return np.log(v[ok]), np.log(r[ok] + 1)
    if form == "semi-log":
        return np.log(v), r
    return v, r


def fit_and_test(v: pd.Series, r: pd.Series, fit_end, test_end=None, periods: dict | None = None) -> dict:
    """Each form fitted on the quarters (or years) to ``fit_end``, judged after it."""
    data = pd.concat([v.rename("v"), r.rename("r")], axis=1).dropna()
    if test_end is not None:
        data = data[data.index <= test_end]
    out = {}
    for form in FORMS:
        y, x = xy(form, data.v, data.r)
        fit = y.index <= fit_end
        test = y.index > fit_end
        if fit.sum() < 3 or test.sum() < 1:
            out[form] = {"verdict": "fit cannot tell", "note": "too few points"}
            continue
        X = np.column_stack([np.ones(fit.sum()), x[fit]])
        b, *_ = np.linalg.lstsq(X, y[fit].to_numpy(), rcond=None)
        resid = y[fit].to_numpy() - X @ b
        r2 = 1 - np.sum(resid ** 2) / np.sum((y[fit] - y[fit].mean()) ** 2)
        sd = float(np.std(resid, ddof=1))
        pred = b[0] + b[1] * x[test]
        err = y[test] - pred
        z = float(err.mean() / sd)
        res = {"a": float(b[0]), "b": float(b[1]), "r2": float(r2), "sd": sd, "z": z,
               "n_fit": int(fit.sum()), "n_test": int(test.sum()), "verdict": verdict_of(z, r2)}
        if periods:
            res["pieces"] = {}
            for name, (lo, hi) in periods.items():
                sel = (err.index >= lo) & (err.index <= hi)
                if sel.sum():
                    zz = float(err[sel].mean() / sd)
                    res["pieces"][name] = {"z": zz, "n": int(sel.sum()), "verdict": verdict_of(zz, r2)}
        res["path"] = {"actual": {str(k): float(val) for k, val in y.items()},
                       "predicted": {str(k): float(b[0] + b[1] * x[k]) for k in y.index}}
        out[form] = res
    return out


def verdict_of(z: float, r2: float) -> str:
    if r2 < 0.3:
        return "fit cannot tell"
    if abs(z) <= 1:
        return "moved as the rate predicts"
    if z <= -2:
        return "fell below"
    if z >= 2:
        return "stayed above"
    return "between"


def majority(res: dict) -> tuple[str, dict]:
    counts = Counter(r["verdict"] for r in res.values())
    top, n = counts.most_common(1)[0]
    return (top if n >= 2 else "the forms disagree"), dict(counts)


def sentence(m2: str, net: str) -> str:
    if m2 == "the forms disagree" or net == "the forms disagree":
        return "the forms disagree"
    if m2 != "fell below":
        return f"on M2: {m2} (C07's verdict; M2 net adds nothing to it)"
    return SENTENCES.get((m2, net), f"on M2: {m2}; net of the Fed's purchases: {net}")


def us_cutoff(eps: list[dict], first_quarter: pd.Period, min_fit: int) -> tuple[pd.Period | None, str | None]:
    for e in sorted(eps, key=lambda e: e["m0"]):
        if e["area"] != "US" or e["apart_080"]:
            continue
        q = pd.Period(e["m0"], "M").asfreq("Q")
        f = q - 1
        if (f - first_quarter).n + 1 >= min_fit:
            return f, e["m0"]
    return None, None


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm = card["parameters"]
    c15 = json.loads(C15.read_text())
    lists = {k: F.from_csv(v) for k, v in c15["result"]["lists"].items()}
    c05 = json.loads(C05.read_text())["result"]
    c05_us = [e for e in F.from_csv(c05["us_episodes"])]

    v = K.fred_series("M2V")
    v = pd.Series(v.to_numpy(), index=v.index.to_period("Q"))
    r = K.fred_quarterly_mean("TB3MS")
    first = v.index.min()
    cutoff, cutoff_m0 = us_cutoff(lists["headline"], first, 40)
    last = min(v.index.max(), r.index.max())
    later = sorted(pd.Period(e["m0"], "M").asfreq("Q") for e in c05_us if pd.Period(e["m0"], "M").asfreq("Q") > cutoff)
    bounds = [cutoff + 1, *[q for q in later], last + 1]
    periods = {}
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1] - 1
        if hi >= lo:
            periods[f"{lo}-{hi}"] = (lo, hi)
    m2_res = fit_and_test(v, r, cutoff, periods=periods)

    # M2 net of the Fed's purchases since the cutoff (C14)
    m2 = K.fred_quarterly_mean("M2SL")
    tre = K.fred_quarterly_mean("TREAST") / 1000
    mbs_raw = K.fred_quarterly_mean("WSHOMCB") / 1000
    mbs_first = K.fred_series("WSHOMCB").index.min()
    mbs = mbs_raw.reindex(tre.index)
    mbs[mbs.index < mbs_first.to_period("Q")] = 0.0
    S = (tre + mbs).dropna()
    s_f = float(S.get(cutoff, np.nan))
    net = m2 - (S - s_f)
    vnet = (v * m2 / net).dropna()
    vnet = pd.concat([v[v.index <= cutoff], vnet[vnet.index > cutoff]]).sort_index()
    net_res = fit_and_test(vnet, r, cutoff, periods=periods)
    m2_major, m2_counts = majority(m2_res)
    net_major, net_counts = majority(net_res)

    # counted variants
    variants = {}
    m1v = K.fred_series("M1V")
    m1v = pd.Series(m1v.to_numpy(), index=m1v.index.to_period("Q"))
    variants["M1 (test to 2020Q1)"] = fit_and_test(m1v, r, cutoff, test_end=pd.Period("2020Q1", "Q"))
    own = K.fred_quarterly_mean("M2OWN")
    spread = (r - own).dropna()
    variants["opportunity cost r - M2OWN (fit and test to 2019Q2)"] = fit_and_test(
        v, spread, cutoff, test_end=pd.Period("2019Q2", "Q"))
    for name, eps in lists.items():
        if not name.startswith("X"):
            continue
        cq, cm = us_cutoff(eps, first, 40)
        if cq is None:
            variants[f"cutoff from C15's list {name}"] = {"note": "no US episode not set apart leaves 40 quarters"}
            continue
        variants[f"cutoff from C15's list {name} ({cm})"] = fit_and_test(v, r, cq)
    variant_verdicts = {k: (majority(x)[0] if isinstance(x, dict) and all(isinstance(y, dict) and "verdict" in y for y in x.values()) else None)
                        for k, x in variants.items()}

    # across moneys: cutoffs dated at m0 of each money's first C15 headline episode not set apart
    annual = K.annual()
    annual = annual[~annual.units_break & ~annual.inside_euro]
    firsts = {}
    for e in sorted(lists["headline"], key=lambda e: e["m0"]):
        if e["apart_080"] or e["area"] in firsts:
            continue
        firsts[e["area"]] = e["m0"]
    cross = {"moneys": {}, "counts": {f: Counter() for f in FORMS}}
    for a, m0 in sorted(firsts.items()):
        if a not in annual.index.get_level_values(0):
            continue
        x = annual.xs(a)
        mean_broad = (x.broad + x.broad.shift(1)) / 2
        vel = (x.gdp / mean_broad).where((x.gdp > 0) & (mean_broad > 0))
        rr = x.rate_short.astype(float)
        both = pd.concat([vel.rename("v"), rr.rename("r")], axis=1).dropna()
        y0 = int(m0[:4])
        if (both.index < y0).sum() < 20 or (both.index >= y0).sum() < 1:
            continue
        res = fit_and_test(both.v, both.r, y0 - 1)
        for f in FORMS:
            cross["counts"][f][res[f]["verdict"]] += 1
            res[f].pop("path", None)
        cross["moneys"][a] = {"m0": m0, "forms": res, "verdict": majority(res)[0]}
    cross["counts"] = {f: dict(c) for f, c in cross["counts"].items()}
    cross["by_money_verdict"] = dict(Counter(x["verdict"] for x in cross["moneys"].values()))

    payload = {
        "cutoff": {"fit_last_quarter": str(cutoff), "first_us_episode_m0": cutoff_m0,
                   "as_c07": str(cutoff) == "2008Q2"},
        "test_last_quarter": str(last),
        "pieces": list(periods),
        "m2": m2_res, "m2_verdict": m2_major, "m2_counts": m2_counts,
        "m2net": net_res, "m2net_verdict": net_major, "m2net_counts": net_counts,
        "S_at_cutoff_bn": s_f,
        "purchases_since_cutoff_bn_last": float(S.iloc[-1] - s_f),
        "sentence": sentence(m2_major, net_major),
        "variants": variants, "variant_verdicts": variant_verdicts,
        "cross_money": cross,
    }
    out = cards.write_result(K.STUDY, CARD, payload)
    print(out)
    return out


if __name__ == "__main__":
    main()
