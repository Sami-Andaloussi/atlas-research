"""Frame e's list, the rule closed: card C15 (C11's rule without its document exception).

From the study's folder: ``../../toolkit/bin/ftpy code/frame_e.py`` (``code/run.py`` calls it first).
Refuses to run unless the card is committed and unchanged (``ft.cards``); writes
``results/runs/C15-e-episodes-closed.json``.

**Entry side only.** Reads base money, GDP, and the CPI up to the crossing month (the two accommodation
readings), and which months the CPI reaches (censoring, a condition of the data). No price after a
crossing, no broad money after the start, no outcome: those are C18's.

The rule is C05's scan with C09's changes (the base read net of nominal GDP's prior pace, one episode per
horizon, units checked), C11's (the pace floored at zero; jumps and seams per episode; a smoothing
variant) and C15's (every jump share of 0.8 or more set apart, documented or not; guards read on the raw
base in every variant; nine lines flagged "likely reclassification, unread").

Readings of the card that its text leaves to the code, fixed here before the run (entry side only):

- *The jump share* is the largest one-month rise of the raw base in (low, c] over B(c) - B(low); a rise
  whose month or the month before is missing is not a one-month rise and is skipped. Where no one-month
  rise can be read at all, the episode is set apart as "jump cannot be read" (as C11 sets annual episodes
  apart: the guard cannot run).
- *The smoothing variant* scans the three-month trailing mean (the month and the two before, all three
  present); the guards read the raw base at the smoothed scan's low and crossing. Where the raw base did
  not rise from that low to that crossing, the episode is set apart as "no rise in the raw base" (the
  guard's purpose, a real addition of reported base money, cannot hold).
- *Seams*: December 2001 for every money whose base comes from IFS, and the money's own seam month, the
  first month its monthly line 14 and monetary base both hold a positive value; the United States and the
  euro area (FRED's and the ECB's series) have none. ``seam_in_window``: a seam month in [w, c].
- *A definition change* is a set-apart episode whose jump month is a seam month; any other is "a one-month
  jump"; annual episodes are "annual" (C11: cannot be checked).
- *Accommodation* (C12 (2)): the design's reading, inflation at or above T at any month from m0 to the
  month before c where the CPI exists ("cannot be read" where it exists at none); the reading at m0, the
  twelve-month inflation at m0 at or above T ("cannot be read" where it is missing). Annual episodes: the
  year-average inflation of m0's year to the year before c's, and of m0's year.
- *Set-apart episodes not keeping their place* (a variant): the search resumes at c + 1 after an episode
  set apart at the headline share (0.8), at m0 + H after any other.
- *The money giving most episodes* (C18's variant) is the one with most episodes on the headline list,
  ties broken by its code; written here, used there.
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
import common as K  # noqa: E402

from ft import cards  # noqa: E402

CARD = K.CARDS / "C15-e-episodes-closed.yaml"
SHARES = (0.5, 0.67, 0.8, 0.9)
FLAGGED = {("BJ", "2003-12"), ("NE", "2003-12"), ("SN", "2003-12"), ("DM", "1984-03"), ("KN", "1984-03"),
           ("VC", "1984-03"), ("DK", "2012-07"), ("DK", "2021-03"), ("GT", "2001-12")}
DOOR_STARTS = {"W1": pd.Period("2008-08", "M"), "W2": pd.Period("2020-02", "M")}
COLUMNS = ["area", "rule", "w", "low", "m0", "c", "B_low", "B_m0", "B_c", "rise_pct_gdp", "gdp_year",
           "gdp_year_before", "gamma", "further_crossings_within_H", "jump_share", "jump_month",
           "apart_050", "apart_067", "apart_080", "apart_090", "seam_in_window", "flag", "infl_m0",
           "infl_max_m0_to_before_c", "acc_m0_T10", "acc_m0_T12", "acc_m0_T20", "acc_T10", "acc_T12",
           "acc_T20", "acc_with_c_T12", "cens_H24", "cens_H36", "cens_H60", "cpi_source", "gdp_source",
           "door_windows"]


def scan(b: np.ndarray, years: np.ndarray, per_year: int, X: float, Y: int, q: float, gdp_of, gamma_of, *,
         floor_gamma: bool, H_periods: int, floor0: int = 0, stop: int | None = None,
         apart_of=None) -> tuple[list[dict], int]:
    """The rule on one series ``b`` (NaN where missing). ``gamma_of(year) -> growth or None``; the pace is
    floored at zero when ``floor_gamma``. ``apart_of(episode) -> bool``, when given, makes a set-apart
    episode resume the search at c + 1 (the variant); otherwise every episode resumes it at m0 + H."""
    out, untestable, floor = [], 0, floor0
    n = len(b) if stop is None else min(len(b), stop)
    Yp = Y * per_year
    for t in range(floor0, n):
        if t < floor or np.isnan(b[t]):
            continue
        w = max(t - Yp, floor)
        if np.all(np.isnan(b[w:t])):
            continue
        gamma = gamma_of(int(years[w]))
        if gamma is None:
            untestable += 1
            continue
        if floor_gamma:
            gamma = max(0.0, gamma)
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
            e = {"w": w, "low": low_at, "m0": s0, "c": t, "rise_pct_gdp": float(100 * rise / g), "gdp_year": gy,
                 "gdp_year_before": gy != int(years[s0]), "gamma": round(gamma, 5)}
            out.append(e)
            if apart_of is not None and apart_of(e):
                floor = t + 1
            else:
                floor = max(t + 1, s0 + H_periods)
    return out, untestable


def jump_of(raw: np.ndarray, low: int, c: int) -> tuple[float | None, int | None, str]:
    """(share, position of the jump, status) on the raw base over (low, c]."""
    denom = raw[c] - raw[low]
    if np.isnan(denom) or not denom > 0:
        return None, None, "no rise in the raw base"
    best, at = None, None
    for s in range(low + 1, c + 1):
        if np.isnan(raw[s]) or np.isnan(raw[s - 1]):
            continue
        r = raw[s] - raw[s - 1]
        if best is None or r > best:
            best, at = r, s
    if best is None:
        return None, None, "jump cannot be read"
    return float(best / denom), at, ""


class Inputs:
    """The panels, cut as the card says, and each money's series, prepared once."""

    def __init__(self) -> None:
        annual, monthly = K.annual(), K.monthly()
        self.broken = sorted(annual[annual.units_break].index.get_level_values(0).unique())
        self.annual = annual[~annual.units_break & ~annual.inside_euro]
        self.monthly = monthly[~monthly.units_break & ~monthly.inside_euro]
        self.seams = K.seam_months()
        cpi_m = self.monthly.cpi.dropna()
        have = cpi_m.groupby(level=1).apply(lambda s: set(s.index.get_level_values(0)))
        self.common_end = None
        for t in pd.period_range(have.index.min(), have.index.max(), freq="M"):
            prev = have.get(t - 12, set())
            if len(prev) and len(prev & have.get(t, set())) >= 0.5 * len(prev):
                self.common_end = t
        self.areas = sorted(set(self.annual.index.get_level_values(0)) | set(self.monthly.index.get_level_values(0)))
        wbr = K.worldbank.read("FM.LBL.BMNY.GD.ZS", K.P.VINTAGES["wdi"]).dropna(subset=["value"])
        econ = K.worldbank.read_economies(K.P.VINTAGES["wdi"]).set_index("iso3")
        wbr = wbr[wbr.iso3.isin(econ.index)]
        wbr = wbr.assign(area=wbr.iso3.map(econ.iso2).where(wbr.iso3 != "EMU", "U2")).set_index(["area", "year"]).value / 100
        pb = (self.annual.broad / self.annual.gdp).dropna()
        ratio = (pb / wbr.reindex(pb.index)).dropna()
        med = ratio.groupby(level=0).median()
        self.units_factor = {a: (None if a not in med.index else float(max(med[a], 1 / med[a]))) for a in self.areas}
        self.series: dict[str, dict] = {}
        for a in self.areas:
            g = self.annual.gdp.xs(a).dropna() if a in self.annual.index.get_level_values(0) else pd.Series(dtype=float)
            mb = self.monthly.base.xs(a).dropna() if a in self.monthly.index.get_level_values(0) else pd.Series(dtype=float)
            ab = self.annual.base.xs(a).dropna() if a in self.annual.index.get_level_values(0) else pd.Series(dtype=float)
            first_m = mb.index.min() if len(mb) else None
            if first_m is not None:
                ab = ab[[pd.Period(f"{y}-12", "M") < first_m for y in ab.index]]
            entry = {"gdp": g, "annual_base": ab}
            if len(mb) >= 2:
                idx = pd.period_range(mb.index.min(), mb.index.max(), freq="M")
                raw = mb.reindex(idx)
                entry.update(idx=idx, raw=raw.to_numpy(dtype=float),
                             smooth=raw.rolling(3, min_periods=3).mean().to_numpy(dtype=float),
                             years=np.array([p.year for p in idx]))
            cpi = self.monthly.cpi.xs(a).dropna() if a in self.monthly.index.get_level_values(0) else pd.Series(dtype=float)
            entry["infl_m"] = K.yoy(cpi)
            ca = self.annual.cpi.xs(a).dropna() if a in self.annual.index.get_level_values(0) else pd.Series(dtype=float)
            entry["infl_a"] = 100 * (ca / ca.shift(1) - 1) if len(ca) else pd.Series(dtype=float)
            row = self.annual.loc[a].iloc[-1] if a in self.annual.index.get_level_values(0) else None
            own = {"US": "fred", "U2": "ecb"}.get(a)
            entry["cpi_source"] = own or (None if row is None else row.get("cpi_source"))
            entry["gdp_source"] = own or (None if row is None else row.get("gdp_source"))
            self.series[a] = entry

    def admitted(self, a: str, factor: float) -> bool:
        if a == "U2":
            return True
        f = self.units_factor.get(a)
        return f is not None and f <= factor


def classify(share: float | None, status: str, jump_month: pd.Period | None, seams: set, threshold: float) -> str:
    if status:
        return status
    if share is None or share < threshold:
        return ""
    return "definition change" if jump_month is not None and jump_month in seams else "one-month jump"


def run_list(inp: Inputs, *, X: float, Y: int, q: float, H: int, factor: float, floor_gamma: bool = True,
             smoothing: bool = False, keep_place: bool = True, T0: float = 12) -> tuple[list[dict], Counter, list[str]]:
    """One list by the rule, each episode with its guards (entry side)."""
    eps, untestable, out_units = [], Counter(), []
    for a in inp.areas:
        if not inp.admitted(a, factor):
            out_units.append(a)
            continue
        S = inp.series[a]
        g = S["gdp"]
        seams = inp.seams.get(a, set())

        def get(y, g=g):
            for yy in (y, y - 1):
                if yy in g.index and g[yy] > 0:
                    return float(g[yy]), yy
            return None, None

        def gamma(y_window, g=g):
            y1, y0 = y_window - 1, y_window - 1 - Y
            if y1 in g.index and y0 in g.index and g[y1] > 0 and g[y0] > 0:
                return math.log(g[y1] / g[y0]) / Y
            return None

        resume_after = None
        ab = S["annual_base"]
        if len(ab) >= 2:
            yrs = np.arange(ab.index.min(), ab.index.max() + 1)
            b = ab.reindex(yrs).to_numpy(dtype=float)
            apart_of = None if keep_place else (lambda e: True)  # an annual episode is always set apart
            found, u = scan(b, yrs, 1, X, Y, q, get, gamma, floor_gamma=floor_gamma, H_periods=math.ceil(H / 12),
                            apart_of=apart_of)
            untestable[a] += u
            for e in found:
                e["further"] = len(scan(b, yrs, 1, X, Y, q, get, gamma, floor_gamma=floor_gamma, H_periods=0,
                                        floor0=e["c"] + 1, stop=e["m0"] + math.ceil(H / 12))[0])
                m0_year = int(yrs[e["m0"]])
                e.update({"area": a, "rule": "annual", "B_low": float(b[e["low"]]), "B_m0": float(b[e["m0"]]),
                          "B_c": float(b[e["c"]]), "jump_share": None, "jump_month": None,
                          **{k: str(pd.Period(f"{yrs[e[k]]}-12", "M")) for k in ("w", "low", "m0", "c")}})
                for s in SHARES:
                    e[f"apart_{int(round(s * 100)):03d}"] = "annual"
                eps.append(e)
                nxt = pd.Period(e["c"], "M") + 1 if not keep_place else max(
                    pd.Period(e["c"], "M") + 1, pd.Period(f"{m0_year + math.ceil(H / 12)}-12", "M"))
                resume_after = nxt
        if "raw" in S:
            idx, raw = S["idx"], S["raw"]
            b = S["smooth"] if smoothing else raw
            floor0 = 0 if resume_after is None else max(0, (resume_after - idx[0]).n)

            def apart_of(e, raw=raw, idx=idx, seams=seams):
                share, at, status = jump_of(raw, e["low"], e["c"])
                return bool(classify(share, status, None if at is None else idx[at], seams, 0.8))

            found, u = scan(b, S["years"], 12, X, Y, q, get, gamma, floor_gamma=floor_gamma, H_periods=H,
                            floor0=floor0, apart_of=None if keep_place else apart_of)
            untestable[a] += u
            for e in found:
                e["further"] = len(scan(b, S["years"], 12, X, Y, q, get, gamma, floor_gamma=floor_gamma,
                                        H_periods=0, floor0=e["c"] + 1, stop=e["m0"] + H)[0])
                share, at, status = jump_of(raw, e["low"], e["c"])
                jm = None if at is None else idx[at]
                e.update({"area": a, "rule": "monthly", "B_low": float(raw[e["low"]]), "B_m0": float(raw[e["m0"]]),
                          "B_c": float(raw[e["c"]]), "jump_share": None if share is None else round(share, 4),
                          "jump_month": None if jm is None else str(jm),
                          **{k: str(idx[e[k]]) for k in ("w", "low", "m0", "c")}})
                for s in SHARES:
                    e[f"apart_{int(round(s * 100)):03d}"] = classify(share, status, jm, seams, s)
                eps.append(e)
    for e in eps:
        annotate(inp, e)
    return eps, untestable, out_units


def annotate(inp: Inputs, e: dict) -> dict:
    a = e["area"]
    S = inp.series[a]
    w, low, m0, c = (pd.Period(e[k], "M") for k in ("w", "low", "m0", "c"))
    seams = inp.seams.get(a, set())
    e["seam_in_window"] = any(w <= s <= c for s in seams)
    e["flag"] = "likely reclassification, unread" if any(
        a == fa and low <= pd.Period(fm, "M") <= c for fa, fm in FLAGGED) else ""
    if e["rule"] == "monthly":
        inf = S["infl_m"]
        before = np.array([inf.get(t, np.nan) for t in pd.period_range(m0, c - 1, freq="M")], dtype=float)
        at_c, at_m0 = inf.get(c, np.nan), inf.get(m0, np.nan)
    else:
        inf = S["infl_a"]
        before = np.array([inf.get(y, np.nan) for y in range(m0.year, c.year)], dtype=float)
        at_c, at_m0 = inf.get(c.year, np.nan), inf.get(m0.year, np.nan)
    seen = before[~np.isnan(before)]
    e["infl_m0"] = None if pd.isna(at_m0) else round(float(at_m0), 2)
    e["infl_max_m0_to_before_c"] = None if not len(seen) else round(float(seen.max()), 2)
    for T in (10, 12, 20):
        e[f"acc_T{T}"] = "cannot be read" if not len(seen) else bool(seen.max() >= T)
        e[f"acc_m0_T{T}"] = "cannot be read" if pd.isna(at_m0) else bool(at_m0 >= T)
    with_c = np.append(seen, [] if pd.isna(at_c) else [float(at_c)])
    e["acc_with_c_T12"] = "cannot be read" if not len(with_c) else bool(with_c.max() >= 12)
    for H in (24, 36, 60):
        e[f"cens_H{H}"] = bool(inp.common_end is None or m0 + H > inp.common_end)
    e["cpi_source"], e["gdp_source"] = S["cpi_source"], S["gdp_source"]
    e["door_windows"] = " ".join(k for k, d in DOOR_STARTS.items() if a == "US" and m0 <= d <= c)
    e["further_crossings_within_H"] = e.pop("further", None)
    return e


def tested(e: dict, reading: str, H: int = 36, T: int = 12, share: float = 0.8) -> bool:
    """Neither set apart (at ``share``), nor censored at H, nor accommodation under ``reading``."""
    apart = e[f"apart_{int(round(share * 100)):03d}"]
    acc = e[f"acc_m0_T{T}"] if reading == "m0" else e[f"acc_T{T}"]
    return not apart and not e[f"cens_H{H}"] and acc is False


def summary(eps: list[dict], H: int = 36, T: int = 12, share: float = 0.8) -> dict:
    key = f"apart_{int(round(share * 100)):03d}"
    by = Counter(e["area"] for e in eps)
    top = sorted(by.items(), key=lambda kv: (-kv[1], kv[0]))[0] if by else (None, 0)
    apart = Counter(e[key] for e in eps if e[key])
    out = {"episodes": len(eps), "moneys": len(by), "monthly": sum(e["rule"] == "monthly" for e in eps),
           "annual": sum(e["rule"] == "annual" for e in eps), "set_apart": sum(apart.values()),
           "set_apart_by_kind": dict(sorted(apart.items())),
           "censored_at_H": sum(e[f"cens_H{H}"] for e in eps),
           "accommodation_design": sum(e[f"acc_T{T}"] is True for e in eps),
           "accommodation_design_cannot_be_read": sum(e[f"acc_T{T}"] == "cannot be read" for e in eps),
           "accommodation_m0": sum(e[f"acc_m0_T{T}"] is True for e in eps),
           "accommodation_m0_cannot_be_read": sum(e[f"acc_m0_T{T}"] == "cannot be read" for e in eps),
           "tested_design": sum(tested(e, "design", H, T, share) for e in eps),
           "tested_m0": sum(tested(e, "m0", H, T, share) for e in eps),
           "tested_both": sum(tested(e, "design", H, T, share) and tested(e, "m0", H, T, share) for e in eps),
           "top_money": top[0], "top_money_episodes": top[1],
           "top_money_share": round(top[1] / len(eps), 3) if eps else None}
    for reading in ("design", "m0"):
        by_era = Counter(K.era_of(int(e["m0"][:4])) for e in eps if tested(e, reading, H, T, share))
        out[f"tested_{reading}_by_era"] = [by_era.get(i, 0) for i in range(len(K.ERAS))]
        out[f"tested_{reading}_2020_2021"] = sum(tested(e, reading, H, T, share) and e["m0"][:4] in ("2020", "2021")
                                                 for e in eps)
    pool = [e for e in eps if e[f"acc_T{T}"] is False and not e[f"cens_H{H}"]]
    out["neither_acc_nor_censored"] = len(pool)
    out["set_apart_in_that_pool"] = sum(bool(e[key]) for e in pool)
    out["one_month_jumps_in_that_pool"] = sum(e[key] == "one-month jump" for e in pool)
    out["seam_in_window_tested_design"] = sum(e["seam_in_window"] and tested(e, "design", H, T, share) for e in eps)
    out["flagged_tested_design"] = sum(bool(e["flag"]) and tested(e, "design", H, T, share) for e in eps)
    return out


def to_csv(eps: list[dict]) -> str:
    df = pd.DataFrame(sorted(eps, key=lambda e: (e["m0"], e["area"])))
    for col in COLUMNS:
        if col not in df:
            df[col] = None
    return df[COLUMNS].to_csv(index=False, float_format="%.6g")


def from_csv(text: str) -> list[dict]:
    """A list written by :func:`to_csv`, back to dicts with the flags' types restored."""
    import io

    df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False)
    out = []
    for row in df.to_dict("records"):
        e = {}
        for k, v in row.items():
            if k.startswith(("acc_", "seam_in_window", "cens_", "gdp_year_before")):
                e[k] = {"True": True, "False": False}.get(v, v)
            elif k in ("rise_pct_gdp", "jump_share", "infl_m0", "infl_max_m0_to_before_c", "gamma", "B_low",
                       "B_m0", "B_c"):
                e[k] = float(v) if v not in ("", "None") else None
            else:
                e[k] = v
        out.append(e)
    return out


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)  # refuse before reading any data
    p = card["parameters"]
    X0, Y0, q0, T0, H0, U0 = (p["X_pct_of_gdp"], p["Y_years"], p["q_takeoff"], p["T_inflation_pct"],
                              p["H_months"], p["units_factor"])
    inp = Inputs()
    base = dict(X=X0, Y=Y0, q=q0, H=H0, factor=U0)
    head, untestable, out_units = run_list(inp, **base)
    s = summary(head)
    lists = {"headline": head}
    for X in p["grid"]["X_pct_of_gdp"]:
        for Y in p["grid"]["Y_years"]:
            if (X, Y) != (X0, Y0):
                lists[f"X{X}_Y{Y}"] = run_list(inp, **{**base, "X": X, "Y": Y})[0]
    lists["q0"] = run_list(inp, **{**base, "q": 0})[0]
    for H in p["grid"]["H_months"]:
        lists[f"H{H}"] = run_list(inp, **{**base, "H": H})[0]
    lists["units_factor3"], _, out3 = run_list(inp, **{**base, "factor": 3})
    lists["smoothing"] = run_list(inp, **base, smoothing=True)[0]
    lists["not_keeping_place"] = run_list(inp, **base, keep_place=False)[0]
    lists["gamma_not_floored"] = run_list(inp, **base, floor_gamma=False)[0]
    sizes = {}
    for name, eps in lists.items():
        H = int(name[1:]) if name in ("H24", "H60") else H0
        sizes[name] = summary(eps, H=H)
    sizes_by_T = {str(T): summary(head, T=T) for T in (10, 12, 20)}
    sizes_by_share = {str(sh): summary(head, share=sh) for sh in SHARES}
    beside = {
        "seam_variant": {"tested_design": sum(tested(e, "design") and not e["seam_in_window"] for e in head),
                         "tested_m0": sum(tested(e, "m0") and not e["seam_in_window"] for e in head)},
        "every_set_apart_jump_put_back": {
            "tested_design": sum((not e["cens_H36"]) and e["acc_T12"] is False for e in head),
            "tested_m0": sum((not e["cens_H36"]) and e["acc_m0_T12"] is False for e in head)},
    }
    narrow = {"episodes": 667, "set_apart": 64, "one_month_jumps": 56, "definition_changes": 5, "annual": 3,
              "tested_design": 289, "tested_m0": 356}
    ours = {"episodes": s["episodes"], "set_apart": s["set_apart"],
            "one_month_jumps": s["set_apart_by_kind"].get("one-month jump", 0),
            "definition_changes": s["set_apart_by_kind"].get("definition change", 0),
            "annual": s["set_apart_by_kind"].get("annual", 0),
            "tested_design": s["tested_design"], "tested_m0": s["tested_m0"]}
    payload = {
        "headline": {"X_pct_of_gdp": X0, "Y_years": Y0, "q_takeoff": q0, "T_inflation_pct": T0, "H_months": H0,
                     "units_factor": U0, "jump_share": p["jump_share"]},
        "common_end": str(inp.common_end),
        "moneys_in_panel": len(inp.areas),
        "moneys_dropped_units_break": inp.broken,
        "moneys_set_aside_by_units_check": out_units,
        "moneys_set_aside_by_units_check_factor3": out3,
        "periods_untestable": int(sum(untestable.values())),
        "summary": s,
        "summary_by_T": sizes_by_T,
        "summary_by_jump_share": sizes_by_share,
        "sizes": sizes,
        "beside_the_headline": beside,
        "against_the_narrow_check": {"narrow_check": narrow, "this_run": ours,
                                     "same": all(narrow[k] == ours[k] for k in narrow)},
        "without_top_money": summary([e for e in head if e["area"] != s["top_money"]])
        if s["top_money_share"] and s["top_money_share"] > 0.25 else None,
        "failure_clause_jumps_over_a_third": s["one_month_jumps_in_that_pool"] > s["neither_acc_nor_censored"] / 3,
        "us_episodes": to_csv([e for e in head if e["area"] == "US"]),
        "lists": {name: to_csv(eps) for name, eps in lists.items()},
    }
    out = cards.write_result(K.STUDY, CARD, payload)
    print(out, f"{out.stat().st_size / 1e6:.2f} MB")
    print("common end:", inp.common_end, "| moneys:", len(inp.areas), "| set aside by units:", out_units)
    print("headline:", s)
    print("against the narrow check:", payload["against_the_narrow_check"])
    for k, v in sizes.items():
        print(k, {kk: v[kk] for kk in ("episodes", "set_apart", "tested_design", "tested_m0")})
    print(payload["us_episodes"])
    return out


if __name__ == "__main__":
    main()
