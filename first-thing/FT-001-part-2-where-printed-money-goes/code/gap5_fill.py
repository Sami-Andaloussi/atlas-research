"""Gap 5's fill: card C25 (C02's child: A4 with the annual CPI gaps filled from the World Bank's
Cross-Country Database of Inflation), card C26 (C24's child: the deciders with the monthly CPI gaps filled) and
card C27 (C03's child: A4 on broad money with C25's fill, unchanged).

From the study's folder: ``../../toolkit/bin/ftpy code/gap5_fill.py C25`` or ``... C26`` or ``... C27`` (or ``both``,
which runs the three).
Each refuses to run unless its card is committed and unchanged; each writes ``results/runs/<card>.json``.
The fill's rule is ``fill_cpi.py`` (its docstring is the card's rule (1)); the database is read by ``hko.py``.

Readings of the cards that their text leaves to the code, fixed here before the runs:

- *The panels the fill is read into.* The annual panel keeps its index: a filled year is read only into a row
  the panel already has (a window needs base money and real GDP in the row, so a year without a row cannot
  complete a window). The monthly panel gets a new row for a filled month the panel has no row for; its flags
  (``units_break``, ``inside_euro``: read by year from the annual panel; ``base_break``: by money) are set as
  ``panel.monthly`` sets them. The modules ``common`` and ``frame_e``/``deciders`` read the panels through
  ``common.annual()`` and ``common.monthly()``; the run replaces those two functions by the filled panels
  (the unfilled ones are kept for the reproduction).
- *C25*: the unfilled panel's windows, headline, lines and held-out checks must reproduce C02's stored result
  (and C22's, for the grid beside) to 1e-9; a window of the unfilled list keeps its mu, pi and g under the
  fill. The windows added are listed with the source of each end's CPI. "Differs" is read on: the headline's
  verdict, the held-out windows' verdict, the number of folds that differ, and whether the line separates
  on inflation and on money growth.
- *C27*: C25's reading on C03's windows (``a4_reading`` with ``money="broad"``): the unfilled panel's headline,
  lines, held-out checks and list of windows must reproduce C03's stored result to 1e-9; the filled panel's
  are read beside. C03's failure clause is read on the filled panels (broad money against C25's filled base
  money on the windows both cover). "Differs" is C25's reading plus two items of C27 (5): whether the held-out
  verdict equals the headline's, and whether broad and base money tell different verdicts on the common windows.
- *C26*: C15's lists are re-read, not re-run: each episode's accommodation columns are recomputed by
  ``frame_e.annotate`` on the CPI (the unfilled CPI must give the columns C15 stored, for every episode of every
  list; the filled CPI gives the run's). The measures of an episode (``deciders.measure``) are computed once
  per (economy, m0, c, rule, rise, H, T) whatever the list. The counted runs, the beside runs, the two-thirds
  count and the coincidence follow ``deciders.main`` with C24's coding for "war episodes out"; C05's and C09's
  lists beside are not rerun.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import deciders as D  # noqa: E402
import fill_cpi as FC  # noqa: E402
import frame_e as F  # noqa: E402
import longrun as L  # noqa: E402

from ft import cards  # noqa: E402

C02 = K.CARDS / "C02-a4-base.yaml"
C03 = K.CARDS / "C03-a4-broad.yaml"
C22 = K.CARDS / "C22-a4-base-2019-narrowed.yaml"
C25 = K.CARDS / "C25-a4-base-hko-fill.yaml"
C26 = K.CARDS / "C26-a5-deciders-hko-fill.yaml"
C27 = K.CARDS / "C27-a4-broad-hko-fill.yaml"
C24 = K.CARDS / "C24-a5-deciders-war-coded.yaml"


# --- helpers ------------------------------------------------------------------------------------------

def clean(x):
    """JSON-safe: numpy scalars and arrays to Python, Periods to strings, NaN to None."""
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set)):
        return [clean(v) for v in (sorted(x) if isinstance(x, set) else x)]
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, (np.floating, float)):
        return None if np.isnan(x) else float(x)
    if isinstance(x, (pd.Period, pd.Timestamp)):
        return str(x)
    if isinstance(x, np.ndarray):
        return clean(x.tolist())
    return x


def same(a, b, tol: float = 1e-9) -> bool:
    """Two JSON-shaped values equal, floats to ``tol``."""
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k], tol) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    return a == b


def jsonable(x):
    return json.loads(json.dumps(clean(x), default=str))


# --- the filled panels --------------------------------------------------------------------------------

def filled_annual(a: pd.DataFrame):
    cpi, log, sources = FC.fill_annual(a.cpi)
    out = a.copy()
    out["cpi"] = cpi.reindex(out.index)
    return out, log, sources


def filled_monthly(m: pd.DataFrame, annual: pd.DataFrame):
    cpi, log = FC.fill_monthly(m.cpi)
    new = cpi.index.difference(m.index)
    rows = pd.DataFrame(np.nan, index=new, columns=m.columns)
    rows.index.names = m.index.names
    years = pd.MultiIndex.from_arrays([new.get_level_values(0), new.get_level_values(1).year])
    for flag in ("units_break", "inside_euro"):
        rows[flag] = annual[flag].reindex(years).fillna(False).to_numpy().astype(bool)
    seam = m.groupby(level=0).base_break.max()
    rows["base_break"] = new.get_level_values(0).map(seam).fillna(False).to_numpy().astype(bool)
    out = pd.concat([m, rows]).sort_index()
    out["cpi"] = cpi.reindex(out.index)
    for flag in ("units_break", "inside_euro", "base_break"):
        out[flag] = out[flag].astype(bool)
    # the months filled: those the study's CPI lacked (a month may already have a row, with another series)
    return out, log, cpi.index.difference(m.cpi.dropna().index)


# --- C25: A4 -----------------------------------------------------------------------------------------

def a4_reading(frame: pd.DataFrame, ends: list[int], line: float = 12.0, money: str = "base") -> tuple[pd.DataFrame, dict]:
    df = L.windows(frame, money, ends)
    head = L.headline(df)
    return df, {"sample": {"windows": int(len(df)), "moneys": int(df.area.nunique()),
                           "list": df[["area", "y0", "y1"]].astype(str).agg(" ".join, axis=1).tolist()},
                "headline": head, "prior_line_on_pi": L.prior_line(df, "pi", line),
                "prior_line_on_mu": L.prior_line(df, "mu", line), "held_out": L.held_out(df, head)}


def line_row(p: dict) -> dict:
    keys = ("beta_below", "beta_below_lo", "beta_below_hi", "verdict_below", "beta_above", "beta_above_lo",
            "beta_above_hi", "verdict_above", "theta", "p_theta", "separates", "windows_above", "windows_below")
    return {k: p.get(k) for k in keys}


def summary_of(r: dict) -> dict:
    h, ho = r["headline"], r["held_out"]
    return {"windows": r["sample"]["windows"], "moneys": r["sample"]["moneys"], "beta": h["beta"], "lo": h["beta_lo"],
            "hi": h["beta_hi"], "verdict": h["verdict"], "r2": h["r2"], "gamma": h["coef"]["g"]["b"],
            "gamma_lo": h["coef"]["g"]["lo"], "gamma_hi": h["coef"]["g"]["hi"],
            "gamma_verdict": h.get("gamma_verdict"),
            "line_pi": line_row(r["prior_line_on_pi"]), "line_mu": line_row(r["prior_line_on_mu"]),
            "held_out": {"train_windows": ho["train_windows"], "test_windows": ho["test_windows"],
                         "moneys_in_both": ho["moneys_in_both"], "oos_r2": ho["oos_r2"],
                         "beta": ho["test"]["beta"], "lo": ho["test"]["beta_lo"], "hi": ho["test"]["beta_hi"],
                         "verdict": ho["test"]["verdict"], "same_verdict": ho["same_verdict"],
                         "fit_train_beta": ho["fit_train"]["beta"]},
            "folds": [{k: f[k] for k in ("fold", "windows", "moneys", "oos_r2", "beta", "beta_lo", "beta_hi", "verdict")}
                      for f in ho["folds"]],
            "folds_differing": ho["folds_differing"], "holds": ho["holds"]}


def differs(old: dict, new: dict) -> list[str]:
    """What the card calls a difference (C25 (5))."""
    out = []
    if old["headline"]["verdict"] != new["headline"]["verdict"]:
        out.append(f"headline verdict: {old['headline']['verdict']} -> {new['headline']['verdict']}")
    if old["held_out"]["test"]["verdict"] != new["held_out"]["test"]["verdict"]:
        out.append(f"held-out windows' verdict: {old['held_out']['test']['verdict']} -> {new['held_out']['test']['verdict']}")
    if old["held_out"]["folds_differing"] != new["held_out"]["folds_differing"]:
        out.append(f"folds that differ: {old['held_out']['folds_differing']} -> {new['held_out']['folds_differing']}")
    if (old["held_out"]["folds_differing"] < 2) != (new["held_out"]["folds_differing"] < 2):
        out.append("the folds' statement (fewer than two differ) changes")
    for way in ("pi", "mu"):
        o, n = old[f"prior_line_on_{way}"].get("separates"), new[f"prior_line_on_{way}"].get("separates")
        if o != n:
            out.append(f"the 12% line on {way} separates: {o} -> {n}")
    return out


def c25() -> Path:
    card = yaml.safe_load(C25.read_text())
    cards.require_locked(C25)
    prm = card["parameters"]
    ends, ends22 = prm["window_ends"], prm["window_ends_beside_C22"]
    c02 = json.loads((K.RUNS / "C02-a4-base.json").read_text())["result"]
    c22 = json.loads((K.RUNS / "C22-a4-base-2019-narrowed.json").read_text())["result"]
    a = K.annual()
    a_f, log, sources = filled_annual(a)
    u = a[~a.units_break]
    f = a_f[~a_f.units_break]

    # (3) the reproduction, on the unfilled panel
    df_u, r_u = a4_reading(u, ends)
    df_u22, r_u22 = a4_reading(u, ends22)
    reproduces = {}
    for name, mine, stored in (("C02", r_u, c02), ("C22", r_u22, c22)):
        reproduces[name] = all(same(jsonable(mine[k]), stored[k]) for k in
                               ("headline", "prior_line_on_pi", "prior_line_on_mu", "held_out"))
    void = not all(reproduces.values())

    out: dict = {"void": void, "reproduces_stored": reproduces,
                 "fill": {"economies_filled": int((log.years_added > 0).sum()),
                          "economies_refused_by_the_guard": log[log.years_added == 0][["area", "note"]].to_dict("records"),
                          "years_added": log[log.years_added > 0][["area", "years_added", "sources", "note"]].to_dict("records"),
                          "years_added_total": int(log.years_added.sum())}}
    if void:
        out["note"] = "the unfilled panel did not reproduce the stored result: nothing is read from this run"
        return cards.write_result(K.STUDY, C25, clean(out))
    for tag, grid, df_old, r_old, stored in (("C02_grid", ends, df_u, r_u, c02), ("C22_grid", ends22, df_u22, r_u22, c22)):
        df_f, r_f = a4_reading(f, grid)
        k0 = set(map(tuple, df_old[["area", "y0", "y1"]].values))
        mm = df_old.merge(df_f, on=["area", "y0", "y1"], suffixes=("_0", "_1"))
        unchanged = bool(len(mm) == len(df_old) and ((mm.mu_0 - mm.mu_1).abs().max() < 1e-12)
                         and ((mm.pi_0 - mm.pi_1).abs().max() < 1e-12) and ((mm.g_0 - mm.g_1).abs().max() < 1e-12))
        added = []
        for _, r in df_f.iterrows():
            if (r.area, r.y0, r.y1) in k0:
                continue
            added.append({"area": r.area, "y0": int(r.y0), "y1": int(r.y1), "mu": float(r.mu), "pi": float(r.pi), "g": float(r.g),
                          "cpi_source_y0": sources.get((r.area, int(r.y0)), "panel"),
                          "cpi_source_y1": sources.get((r.area, int(r.y1)), "panel")})
        old_s, new_s = summary_of(r_old), summary_of(r_f)
        diff = differs(r_old, r_f)
        out[tag] = {"filled": new_s, "unfilled": old_s, "windows_added": added, "n_added": len(added),
                    "moneys_added": sorted(set(df_f.area) - set(df_old.area)),
                    "kept_windows_unchanged": unchanged, "differs": diff, "any_verdict_differs": bool(diff),
                    "points": df_f.round(4).to_dict("records")}
    exp = {"C02_grid": (590, 152, 635, 155, 45), "C22_grid": (540, 152, 573, 156, 33)}
    out["expected_check"] = {t: {"before": [out[t]["unfilled"]["windows"], out[t]["unfilled"]["moneys"]],
                                 "after": [out[t]["filled"]["windows"], out[t]["filled"]["moneys"]],
                                 "added": out[t]["n_added"],
                                 "as_the_card_counted": [out[t]["unfilled"]["windows"], out[t]["unfilled"]["moneys"],
                                                         out[t]["filled"]["windows"], out[t]["filled"]["moneys"],
                                                         out[t]["n_added"]] == list(exp[t])} for t in exp}
    out["any_verdict_differs"] = bool(out["C02_grid"]["any_verdict_differs"] or out["C22_grid"]["any_verdict_differs"])
    return cards.write_result(K.STUDY, C25, clean(out))


# --- C27: A4 on broad money -----------------------------------------------------------------------------

def lost_for_cpi(frame: pd.DataFrame, money: str, ends: list[int]) -> list[tuple]:
    """The windows of a grid that have the money and real GDP positive at both ends (neither end inside the euro)
    and no usable CPI at an end: lost only for a missing price (counted, no mu or pi computed)."""
    out = []
    for area, x in frame.groupby(level=0):
        x = x.droplevel(0)
        for y0, y1 in zip(ends[:-1], ends[1:]):
            if y0 not in x.index or y1 not in x.index:
                continue
            r0, r1 = x.loc[y0], x.loc[y1]
            if any(pd.isna(v) or v <= 0 for v in (r0[money], r1[money], r0.rgdp, r1.rgdp)) or bool(r0.inside_euro) or bool(r1.inside_euro):
                continue
            if any(pd.isna(v) or v <= 0 for v in (r0.cpi, r1.cpi)):
                out.append((area, y0, y1))
    return out


def c27() -> Path:
    """C03's model on broad money with C25's fill, unchanged (card C27). The unfilled panel must reproduce C03's
    stored headline, lines and held-out checks to 1e-9 first; the filled run is read beside C03's, and beside
    C25's filled base-money run on the windows both cover (C03's failure clause)."""
    card = yaml.safe_load(C27.read_text())
    cards.require_locked(C27)
    ends = card["parameters"]["window_ends"]
    c03 = json.loads((K.RUNS / "C03-a4-broad.json").read_text())["result"]
    c25 = json.loads((K.RUNS / "C25-a4-base-hko-fill.json").read_text())["result"]
    a = K.annual()
    a_f, log, sources = filled_annual(a)
    u = a[~a.units_break]
    f = a_f[~a_f.units_break]

    # (3) the reproduction, on the unfilled panel
    df_u, r_u = a4_reading(u, ends, money="broad")
    reproduces = all(same(jsonable(r_u[k]), c03[k]) for k in ("headline", "prior_line_on_pi", "prior_line_on_mu", "held_out"))
    reproduces = bool(reproduces and r_u["sample"]["list"] == c03["sample"]["list"])
    out: dict = {"void": not reproduces, "reproduces_stored": {"C03": reproduces},
                 "fill": {"economies_filled": int((log.years_added > 0).sum()),
                          "economies_refused_by_the_guard": log[log.years_added == 0][["area", "note"]].to_dict("records"),
                          "years_added": log[log.years_added > 0][["area", "years_added", "sources", "note"]].to_dict("records"),
                          "years_added_total": int(log.years_added.sum())}}
    if not reproduces:
        out["note"] = "the unfilled panel did not reproduce C03's stored result: nothing is read from this run"
        return cards.write_result(K.STUDY, C27, clean(out))
    df_f, r_f = a4_reading(f, ends, money="broad")
    k0 = set(map(tuple, df_u[["area", "y0", "y1"]].values))
    mm = df_u.merge(df_f, on=["area", "y0", "y1"], suffixes=("_0", "_1"))
    unchanged = bool(len(mm) == len(df_u) and ((mm.mu_0 - mm.mu_1).abs().max() < 1e-12)
                     and ((mm.pi_0 - mm.pi_1).abs().max() < 1e-12) and ((mm.g_0 - mm.g_1).abs().max() < 1e-12))
    added = []
    for _, r in df_f.iterrows():
        if (r.area, r.y0, r.y1) in k0:
            continue
        added.append({"area": r.area, "y0": int(r.y0), "y1": int(r.y1), "mu": float(r.mu), "pi": float(r.pi), "g": float(r.g),
                      "cpi_source_y0": sources.get((r.area, int(r.y0)), "panel"),
                      "cpi_source_y1": sources.get((r.area, int(r.y1)), "panel")})
    old_s, new_s = summary_of(r_u), summary_of(r_f)
    diff = differs(r_u, r_f)
    # (5) whether the held-out verdict equals the headline's, on each side (C03's held-out reading differed already)
    held_agrees = {"unfilled": bool(r_u["held_out"]["same_verdict"]), "filled": bool(r_f["held_out"]["same_verdict"])}
    if held_agrees["unfilled"] != held_agrees["filled"]:
        diff.append(f"the held-out verdict equals the headline's: {held_agrees['unfilled']} -> {held_agrees['filled']}")
    # C03's failure clause on the filled panels: broad money (C27) against base money (C25's filled run), the windows both cover
    base_f = L.windows(f, "base", ends)
    key = ["area", "y0", "y1"]
    common = df_f.merge(base_f[key], on=key)
    base_common = base_f.merge(df_f[key], on=key)
    c_b, c_base = L.headline(common), L.headline(base_common)
    beside = {"common_windows": int(len(common)), "beta_broad_common": c_b["beta"], "lo_broad_common": c_b["beta_lo"],
              "hi_broad_common": c_b["beta_hi"], "verdict_broad_common": c_b["verdict"],
              "beta_base_common": c_base["beta"], "lo_base_common": c_base["beta_lo"], "hi_base_common": c_base["beta_hi"],
              "verdict_base_common": c_base["verdict"], "only_in_C27": int(len(df_f) - len(common)),
              "only_in_C25": int(len(base_f) - len(base_common)),
              "depends_on_the_aggregate": c_b["verdict"] != c_base["verdict"],
              "unfilled_depends_on_the_aggregate": bool(c03["beside_C02"]["depends_on_the_aggregate"]),
              "c25_filled_headline_verdict": c25["C02_grid"]["filled"]["verdict"]}
    if beside["depends_on_the_aggregate"] != beside["unfilled_depends_on_the_aggregate"]:
        diff.append(f"broad and base money tell different verdicts on the windows both cover: "
                    f"{beside['unfilled_depends_on_the_aggregate']} -> {beside['depends_on_the_aggregate']}")
    lost_u, lost_f = lost_for_cpi(u, "broad", ends), lost_for_cpi(f, "broad", ends)
    out["lost_for_missing_cpi"] = {"unfilled": len(lost_u), "filled": len(lost_f),
                                   "filled_starting_before_1970": sum(y0 < 1970 for _, y0, _ in lost_f)}
    out.update({"filled": new_s, "unfilled": old_s, "windows_added": added, "n_added": len(added),
                "moneys_added": sorted(set(df_f.area) - set(df_u.area)), "kept_windows_unchanged": unchanged,
                "held_out_agrees_with_headline": held_agrees, "beside_base_money": beside,
                "differs": diff, "any_verdict_differs": bool(diff), "points": df_f.round(4).to_dict("records")})
    out["expected_check"] = {"before": [old_s["windows"], old_s["moneys"]], "after": [new_s["windows"], new_s["moneys"]],
                             "added": len(added), "added_economies": len({r["area"] for r in added}),
                             "as_the_card_counted": [old_s["windows"], old_s["moneys"], new_s["windows"], new_s["moneys"],
                                                     len(added)] == [580, 152, 625, 155, 45]}
    return cards.write_result(K.STUDY, C27, clean(out))


# --- C26: the deciders --------------------------------------------------------------------------------

class Cache(dict):
    """``deciders.run``'s cache of measures, keyed ``(id(episode), H, T)``, computed lazily and once per episode's
    content (economy, m0, c, rule, rise), whatever the list the episode is in."""

    def __init__(self, data) -> None:
        super().__init__()
        self.data, self.eps, self.memo = data, {}, {}

    def register(self, eps: list[dict]) -> None:
        for e in eps:
            self.eps[id(e)] = e

    def __missing__(self, key):
        i, H, T = key
        e = self.eps[i]
        ck = (e["area"], e["m0"], e["c"], e["rule"], e["rise_pct_gdp"], H, T)
        if ck not in self.memo:
            self.memo[ck] = D.measure(self.data, e, H, T)
        self[key] = self.memo[ck]
        return self[key]


ANNOTATED = ("infl_m0", "infl_max_m0_to_before_c", "acc_T10", "acc_T12", "acc_T20", "acc_m0_T10", "acc_m0_T12",
             "acc_m0_T20", "acc_with_c_T12", "cens_H24", "cens_H36", "cens_H60", "seam_in_window", "flag")


def reannotate(inp, text: str) -> list[dict]:
    """C15's list as stored, with the columns that read the CPI re-read by C15's own ``annotate`` on ``inp``."""
    eps = F.from_csv(text)
    for e in eps:
        e["further"] = e.get("further_crossings_within_H")
        F.annotate(inp, e)
    return eps


def annotation_matches(stored: list[dict], mine: list[dict]) -> bool:
    for s, m in zip(stored, mine):
        if (s["area"], s["m0"], s["c"]) != (m["area"], m["m0"], m["c"]):
            return False
        for k in ANNOTATED:
            a, b = s[k], m[k]
            if isinstance(a, float) or isinstance(b, float):
                if a is None or b is None:
                    if a is not b:
                        return False
                elif abs(a - b) > 1e-5 * max(1.0, abs(a)):
                    return False
            elif a != b:
                return False
    return len(stored) == len(mine)


def battery(data, lists: dict, acd: dict, prm: dict, top_money: str) -> dict:
    """``deciders.main``'s runs on a set of lists, with C24's coding for "war episodes out"."""
    cache = Cache(data)
    for eps in lists.values():
        cache.register(eps)
    R = lambda eps, **kw: D.run(data, eps, cache=cache, prm=prm, **kw)  # noqa: E731
    head = lists["headline"]
    headline = R(head)
    counted: dict = {}
    for name in lists:
        if name.startswith("X"):
            counted[f"list {name}"] = ("list", R(lists[name]))
    counted["T 10"] = ("list", R(head, T=10))
    counted["T 20"] = ("list", R(head, T=20))
    counted["q 0"] = ("list", R(lists["q0"]))
    counted["units factor 3"] = ("list", R(lists["units_factor3"]))
    counted["smoothing"] = ("list", R(lists["smoothing"]))
    counted["set apart not keeping their place"] = ("list", R(lists["not_keeping_place"]))
    counted["seam episodes out"] = ("list", R(head, drop=lambda e, m: bool(e["seam_in_window"])))
    counted["every set-apart jump put back"] = ("list", R(head, share=None))
    counted["H 24"] = ("list", R(lists["H24"], H=24))
    counted["H 60"] = ("list", R(lists["H60"], H=60))
    counted["peg band 1%"] = ("peg", R(head, band=1))
    counted["peg band 5%"] = ("peg", R(head, band=5))
    counted["floor 0.25%"] = ("floor", R(head, floor=0.25))
    counted["floor 1%"] = ("floor", R(head, floor=1))
    counted["deficit -3%"] = ("deficit", R(head, deficit=-3))
    counted["deficit -7%"] = ("deficit", R(head, deficit=-7))
    extended = R(head, drop=lambda e, m: D.war_coded(e, m, acd))
    counted["war episodes out"] = ("list", extended)
    counted["episodes starting in 2020-2021 apart"] = ("list", R(head, drop=lambda e, m: e["m0"][:4] in ("2020", "2021")))
    counted[f"the money giving most episodes out ({top_money})"] = ("list", R(head, drop=lambda e, m: e["area"] == top_money))
    counted["D4's read-past-c episodes out"] = ("past_c", R(head, drop=lambda e, m: bool(m["past_c"])))
    counted["five-year strata"] = ("list", R(head, strata="blocks"))
    assert len(counted) == 29, len(counted)
    beside = {f"jump share {s}": R(head, share=s) for s in (0.5, 0.67, 0.9)}
    two_thirds = D.agreement_of(headline, {k: {"kind": kind, "combined": r["combined"]} for k, (kind, r) in counted.items()})
    coincide = {}
    for reading in ("m0", "design"):
        chosen = D.tested_set(head, reading, 36, 12, 0.8)
        cats = [D.categories(cache[(id(e), 36, 12)]) for e in chosen]
        pairs = {}
        for i, d1 in enumerate(D.DECIDERS):
            for d2 in D.DECIDERS[i + 1:]:
                both = [(c[d1], c[d2]) for c in cats if c[d1] is not None and c[d2] is not None]
                if not both:
                    continue
                same_share = sum(x == y for x, y in both) / len(both)
                pairs[f"{d1}-{d2}"] = {"n": len(both), "same": round(same_share, 3), "opposite": round(1 - same_share, 3),
                                       "cannot_tell_apart": max(same_share, 1 - same_share) > 0.8}
        coincide[reading] = pairs

    def describe(eps, reading):
        rows = [cache[(id(e), 36, 12)] for e in D.tested_set(eps, reading, 36, 12, 0.8)]

        def q(key):
            x = np.array([m[key] for m in rows if m[key] is not None], dtype=float)
            return None if not len(x) else {"n": int(len(x)), "median": float(np.median(x)), "p25": float(np.quantile(x, 0.25)),
                                            "p75": float(np.quantile(x, 0.75)), "share_above_zero": float(np.mean(x > 0))}
        return {"O1": q("O1"), "O1pp": q("O1pp"), "O2_gross": q("O2_gross"), "O2_net": q("O2_net"), "O3": q("O3"),
                "O1_stopped_early": sum(m["O1_stop"] is not None for m in rows)}

    # what C18 stores beside its tests, for the registry: one line per episode of the headline list, the
    # accommodation episodes apart, the censored ones, and C24's count of episodes taken out for war
    lines = []
    for e in head:
        m = cache[(id(e), 36, 12)]
        c = D.categories(m)
        lines.append({"area": e["area"], "m0": e["m0"], "c": e["c"], "rise_pct_gdp": e["rise_pct_gdp"],
                      "apart": e["apart_080"], "flag": e["flag"], "seam_in_window": e["seam_in_window"],
                      "tested_m0": e in D.tested_set([e], "m0", 36, 12, 0.8),
                      "tested_design": e in D.tested_set([e], "design", 36, 12, 0.8),
                      "acc_m0": e["acc_m0_T12"], "acc_design": e["acc_T12"], "censored": e["cens_H36"],
                      **{k: m[k] for k in ("O1", "O1p", "O1pp", "O1_stop", "O2_gross", "O2_net", "O3", "peg_ratio",
                                           "rate_m0", "rate_m3", "D4", "past_c", "deficit", "war_deaths")},
                      **{f"cat_{d}": c[d] for d in D.DECIDERS}})
    acc_apart = [e for e in head if e["acc_T12"] is True and not e["cens_H36"] and not e["apart_080"]]
    acc_o1 = np.array([cache[(id(e), 36, 12)]["O1"] for e in acc_apart if cache[(id(e), 36, 12)]["O1"] is not None])
    war_out = {}
    for reading in ("m0", "design"):
        chosen = D.tested_set(head, reading, 36, 12, 0.8)
        taken = [e for e in chosen if D.war_coded(e, cache[(id(e), 36, 12)], acd)]
        war_out[reading] = {"tested": len(chosen), "out": len(taken),
                            "from_1989": sum(int(e["m0"][:4]) >= 1989 for e in taken),
                            "before_1989": sum(int(e["m0"][:4]) < 1989 for e in taken)}
    pre = [e for e in head if int(e["m0"][:4]) < 1989]
    return {"episodes": lines,
            "accommodation_apart": {"n": len(acc_apart), "O1_n": int(len(acc_o1)),
                                    "O1_median": float(np.median(acc_o1)) if len(acc_o1) else None},
            "episodes_out": war_out, "list_episodes_before_1989": len(pre),
            "list_episodes_before_1989_war_coded": sum(D.war_coded(e, cache[(id(e), 36, 12)], acd) for e in pre),
            "headline": headline, "counted": {k: {"kind": kind, **r} for k, (kind, r) in counted.items()},
            "beside": beside, "two_thirds": two_thirds, "coincidence": coincide, "extended": extended,
            "what_happened": {"m0": describe(head, "m0"), "design": describe(head, "design")},
            "tested": {r: {"n": len(D.tested_set(head, r, 36, 12, 0.8)),
                           "keys": [f"{e['area']} {e['m0']}" for e in D.tested_set(head, r, 36, 12, 0.8)]}
                       for r in ("m0", "design")}}


def frame_stats(lists: dict) -> dict:
    """The numbers the registry reads from C15's lists that depend on the CPI (frame_e.summary on the headline,
    the tested sizes of the lists the text names, and the counts from the list to the tested set), read on
    the lists as annotated."""
    head = lists["headline"]
    kept = [e for e in head if not e["apart_080"]]
    acc = lambda e: str(e["acc_T12"])  # noqa: E731
    rest = [e for e in kept if acc(e) == "False"]
    sizes = {name: F.summary(lists[name], H=int(name[1:]) if name in ("H24", "H60") else 36)["tested_design"]
             for name in ("smoothing", "X2.5_Y2", "X10_Y2", "H24", "H60")}
    return {"summary": F.summary(head), "sizes_tested_design": sizes, "kept": len(kept),
            "acc_kept": sum(acc(e) == "True" for e in kept),
            "acc_apart": sum(acc(e) == "True" for e in head if e["apart_080"]),
            "unread_kept": sum(acc(e) == "cannot be read" for e in kept),
            "censored_rest": sum(bool(e["cens_H36"]) for e in rest)}


def c26() -> Path:
    card = yaml.safe_load(C26.read_text())
    cards.require_locked(C26)
    prm = card["parameters"]
    c18 = json.loads(D.C18_RUN.read_text())
    c24 = json.loads((K.RUNS / "C24-a5-deciders-war-coded.json").read_text())
    c15 = json.loads(D.C15.read_text())
    assert c24["result"]["c18"]["card_hash"] == c18["card_hash"], "C24 did not run on this C18"
    assert not c24["result"]["void"], "C24's run is void"
    assert c18["result"]["c15"]["card_hash"] == c15["card_hash"], "C18 ran on another C15"
    top_money = c15["result"]["summary"]["top_money"]
    common_end = pd.Period(c15["result"]["common_end"], "M")
    texts = c15["result"]["lists"]
    acd, _ = D.acd_war_years()

    # the two sets of panels: the study's (unfilled) and the filled
    a_u, m_u = K.annual(), K.monthly()
    a_f, log_a, _ = filled_annual(a_u)
    m_f, log_m, new_months = filled_monthly(m_u, a_u)
    inp_u = F.Inputs()
    orig = (K.annual, K.monthly)
    K.annual, K.monthly = (lambda: a_f), (lambda: m_f)
    try:
        inp_f = F.Inputs()
        data_f = D.Data()
    finally:
        K.annual, K.monthly = orig
    data_u = D.Data()
    assert inp_u.common_end == common_end and inp_f.common_end == common_end, (inp_u.common_end, inp_f.common_end, common_end)

    # (3) the reproduction on the unfilled CPI
    stored = {name: F.from_csv(t) for name, t in texts.items()}
    lists_u = {name: reannotate(inp_u, t) for name, t in texts.items()}
    annotation_ok = {name: annotation_matches(stored[name], lists_u[name]) for name in texts}
    cache_u = Cache(data_u)
    cache_u.register(lists_u["headline"])
    head_u = D.run(data_u, lists_u["headline"], cache=cache_u, prm=prm)
    ext_u = D.run(data_u, lists_u["headline"], cache=cache_u, prm=prm, drop=lambda e, m: D.war_coded(e, m, acd))
    reproduces = {"annotation_equals_C15": annotation_ok,
                  "headline_equals_C18": same(jsonable(head_u), c18["result"]["headline"]),
                  "extended_equals_C24": same(jsonable(ext_u), c24["result"]["extended"])}
    void = not (all(annotation_ok.values()) and reproduces["headline_equals_C18"] and reproduces["extended_equals_C24"])
    out: dict = {"void": void, "reproduces": reproduces}
    if void:
        out["note"] = "the unfilled CPI did not reproduce C15's columns, C18's headline or C24's run: nothing is read from this run"
        return cards.write_result(K.STUDY, C26, clean(out))

    # (4) the filled run
    lists_f = {name: reannotate(inp_f, t) for name, t in texts.items()}
    res = battery(data_f, lists_f, acd, prm, top_money)
    old = c18["result"]
    cells = []
    for o in D.OUTCOMES:
        for d in D.DECIDERS:
            h, w = res["headline"]["combined"][o][d], res["extended"]["combined"][o][d]
            h18, h24 = old["headline"]["combined"][o][d], c24["result"]["extended"]["combined"][o][d]
            reads = {r: res["headline"]["readings"][r]["tests"][o][d] for r in ("m0", "design")}
            reads18 = {r: old["headline"]["readings"][r]["tests"][o][d] for r in ("m0", "design")}
            cells.append({
                "outcome": o, "decider": d, "filled": h["verdict"], "filled_sign": h["sign"],
                "c18": h18["verdict"], "c18_sign": h18["sign"],
                "filled_war_out": w["verdict"], "filled_war_out_sign": w["sign"], "c24_war_out": h24["verdict"],
                "c24_war_out_sign": h24["sign"],
                "differs_from_c18": (h["verdict"] != h18["verdict"] or h["sign"] != h18["sign"]),
                "war_out_differs_from_filled_headline": (w["verdict"] != h["verdict"] or w["sign"] != h["sign"]),
                "war_out_differs_from_c24": (w["verdict"] != h24["verdict"] or w["sign"] != h24["sign"]),
                "readings": {r: {"tested": reads[r]["tested"], "n_coded": reads[r].get("n_coded"),
                                 "p_holm": reads[r].get("p_holm"), "diff": reads[r].get("diff"),
                                 "verdict": reads[r].get("verdict"),
                                 "c18_n_coded": reads18[r].get("n_coded"), "c18_p_holm": reads18[r].get("p_holm"),
                                 "c18_diff": reads18[r].get("diff"), "c18_verdict": reads18[r].get("verdict")}
                             for r in ("m0", "design")}})
    two = {}
    for o in D.OUTCOMES:
        two[o] = {}
        for d in D.DECIDERS:
            n, c = res["two_thirds"][o][d], old["two_thirds"][o][d]
            c24n = c24["result"]["two_thirds_with_extended"][o][d]
            two[o][d] = {"filled": {k: n[k] for k in ("k", "n", "k_all", "n_all", "holds", "stated")},
                         "c18": {k: c[k] for k in ("k", "n", "k_all", "n_all", "holds", "stated")},
                         "c24": {k: c24n[k] for k in ("k", "n", "k_all", "n_all", "holds", "stated")},
                         "stated_differs_from_c18": n["stated"] != c["stated"], "stated_differs_from_c24": n["stated"] != c24n["stated"]}
    # who enters or leaves the tested set
    moved = {}
    month_set = {(a, m) for a, m in new_months}
    for r in ("m0", "design"):
        tu = D.tested_set(lists_u["headline"], r, 36, 12, 0.8)
        tf = D.tested_set(lists_f["headline"], r, 36, 12, 0.8)
        ku, kf = {(e["area"], e["m0"]): e for e in tu}, {(e["area"], e["m0"]): e for e in tf}
        by_key_u = {(e["area"], e["m0"]): e for e in lists_u["headline"]}
        by_key_f = {(e["area"], e["m0"]): e for e in lists_f["headline"]}

        def line(k, side):
            e0, e1 = by_key_u[k], by_key_f[k]
            m0 = pd.Period(k[1], "M")
            end = min(m0 + 36, common_end)
            filled = sum(1 for t in pd.period_range(m0 - 12, end, freq="M") if (k[0], t) in month_set)
            col = "acc_m0_T12" if r == "m0" else "acc_T12"
            return {"area": k[0], "m0": k[1], "side": side, "acc_before": e0[col], "acc_after": e1[col], "months_filled_in_window": filled}
        moved[r] = {"n_unfilled": len(tu), "n_filled": len(tf),
                    "enter": [line(k, "enters") for k in sorted(set(kf) - set(ku))],
                    "leave": [line(k, "leaves") for k in sorted(set(ku) - set(kf))]}
    fill_by_area = {}
    for a, mth in new_months:
        fill_by_area.setdefault(a, []).append(mth)
    out.update({
        "n_tested": {"c24_headline": c24["result"]["n_tested"]["headline"], "filled_headline": {r: res["headline"]["readings"][r]["n_tested"] for r in ("m0", "design")},
                     "filled_extended": {r: res["extended"]["readings"][r]["n_tested"] for r in ("m0", "design")}},
        "tested_set_movement": moved,
        "fill": {"months_added": int(len(new_months)),
                 "by_economy": {a: {"months": len(v), "first": str(min(v)), "last": str(max(v))} for a, v in sorted(fill_by_area.items())},
                 "refused_by_the_guard": log_m[log_m.months_added == 0][["area", "note"]].to_dict("records"),
                 "annual_panel_years_added": int(log_a.years_added.sum())},
        "cells": cells,
        "cells_differing_from_c18": int(sum(c["differs_from_c18"] for c in cells)),
        "war_out_cells_differing_from_filled_headline": int(sum(c["war_out_differs_from_filled_headline"] for c in cells)),
        "war_out_cells_differing_from_c24": int(sum(c["war_out_differs_from_c24"] for c in cells)),
        "two_thirds": two,
        "two_thirds_stated_differs_from_c18": [f"{o} / {d}" for o in two for d in two[o] if two[o][d]["stated_differs_from_c18"]],
        "two_thirds_stated_differs_from_c24": [f"{o} / {d}" for o in two for d in two[o] if two[o][d]["stated_differs_from_c24"]],
        "coincidence": res["coincidence"], "coincidence_c18": old["coincidence"],
        "what_happened": res["what_happened"], "what_happened_c18": {k: old["what_happened"][k] for k in ("m0", "design")},
        "beside_the_headline": {k: v["combined"] for k, v in res["beside"].items()},
        "beside_the_headline_c18": {k: v["combined"] for k, v in old["beside_the_headline"].items()},
        "headline": res["headline"], "extended": res["extended"],
        "frame": {"filled": frame_stats(lists_f), "unfilled": frame_stats(lists_u)},
        "episodes": res["episodes"], "accommodation_apart": res["accommodation_apart"],
        "episodes_out": res["episodes_out"], "list_episodes_before_1989": res["list_episodes_before_1989"],
        "list_episodes_before_1989_war_coded": res["list_episodes_before_1989_war_coded"],
        "counted": {k: {"kind": v["kind"], "combined": v["combined"]} for k, v in res["counted"].items()},
    })
    out["any_verdict_differs"] = bool(out["cells_differing_from_c18"] or out["two_thirds_stated_differs_from_c18"]
                                      or out["war_out_cells_differing_from_c24"] or out["two_thirds_stated_differs_from_c24"])
    return cards.write_result(K.STUDY, C26, clean(out))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which not in ("C25", "C26", "C27", "both"):
        raise SystemExit(f"unknown card {which!r}: one of C25, C26, C27 (capitals) or both")
    if which in ("C25", "both"):
        print(c25())
    if which in ("C26", "both"):
        print(c26())
    if which in ("C27", "both"):
        print(c27())
