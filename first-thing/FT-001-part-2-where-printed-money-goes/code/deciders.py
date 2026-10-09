"""A5's test on the closed list: card C18 (C16 with its additions removed; C12's rule for the two
readings of accommodation).

From the study's folder, after ``frame_e.py``: ``../../toolkit/bin/ftpy code/deciders.py``. Refuses to
run unless the card is committed and unchanged; reads C15's result (naming its hash), C05's and C09's
(the lists reported beside, never counted); writes ``results/runs/C18-a5-deciders-bare.json``.

Readings of the cards (C06, C10, C12, C16, C18) that their text leaves to the code, fixed here before the
run:

- *Direction.* Each decider's first category is the one the question names: D1 floating (not pegged), D2
  above its floor, D4 government, D5 a large deficit. A difference is the first category's median minus
  the other's: positive means prices (or broad money) rose more where the question expects.
- *The p-value* is two-sided: (1 + the permutations whose |difference| reaches the observed one) over
  (1 + 10,000); each test draws its permutations from a generator seeded with 20260930, so a result does
  not depend on the order of the tests.
- *"Separates"*: Holm-adjusted p < 0.05, at least two qualifying strata (3 or more episodes in each
  category), and the difference of medians of one sign in every qualifying stratum; that sign is the
  verdict's. "Does not separate": adjusted p >= 0.05 with at least two qualifying strata. Otherwise "we
  cannot conclude" — with "(thin)" when fewer than two strata qualify.
- *The two readings* (C18 (3)): the verdict stands when both readings qualify and give the same verdict
  (and, for "separates", the same sign); both qualify and differ: "depends on how accommodation is dated";
  one thin: "we cannot conclude", the thin reading and its strata's n said.
- *Tested and coded.* A decider is tested for an outcome when at least 10 tested episodes have both the
  decider coded and the outcome readable (C06: fewer is described, never tested); Holm runs over the
  deciders tested for that outcome and reading. The two-thirds rule (C18 (4)) counts a run when the
  decider is tested under both readings; it is read only when the headline's verdict is "separates" or
  "does not separate" (k of n is reported either way).
- *O1 when the CPI stops early* (a money whose series ends before m0 + H, not at the panel's common end):
  read over the months that exist if at least 12 follow m0, the stop's month said; otherwise "cannot be
  read". O2 needs broad money at both year-ends (the last before m0's year; the first at or after m0 + H);
  "annualised as a share of broad money at the start" is the change over the years between them, over the
  start's stock, per year, in percent. O2 net subtracts the increases of the central bank's claims on
  the government, on others and (revalued at the start's exchange rate) on the rest of the world; where
  one of those lines is missing, the net bound cannot be read. The United States: Treasuries and
  mortgage-backed securities (H.4.1 year-ends), no foreign line. The euro area: no claims lines in the
  panel, so no net bound.
- *D1*: the money's end-of-month rate against the dollar and, by cross rates, against the pound, the
  French franc and the Deutsche Mark (months to December 1998) and the euro (from January 1999), over the
  twelve months m0 - 11 to m0, all twelve present for an anchor to be read; pegged if, for some anchor,
  the highest over the lowest is at most (1 + b)/(1 - b); not pegged if every readable anchor fails; not
  coded if none is readable. Annual episodes: the last two year-ends before m0. A currency board counts
  as pegged by the band, never as a cap (STATE, "C06's currency-board rule": inert).
- *D2*: the monthly short rate at m0 at or below the floor; or, where the twelve-month inflation stayed
  below T at every month from m0 to m0 + 3, the rate at m0 + 3 (C06); not coded when neither exists.
- *D4* (C12 (4)): the four lines' increases from the last year-end at or before m0 to the last at or
  before c (read to the first year-end after c where none lies between, flagged "read past c"), foreign
  assets converted at the start year's end-of-year rate; the line that rose most; all four needed. The
  United States by C06's own rule, the H.4.1 week-ends: the last week of m0's month and of c's month
  (which never reads past c), Treasuries, mortgage-backed securities, and the rest of total assets.
- *D5*: WEO's general government net lending in the year before m0's year (from 1980); the United States
  before 1980 from FYFSGDA188S; the euro area has no WEO line here: not coded.
- *War*: battle-related deaths of 1,000 or more in m0's year (World Bank, 1989-2024; an economy-year
  absent from the counts read as none); before 1989, not coded, and a war-out run keeps those episodes.
- *The money giving most episodes* is C15's (its headline list's top money).
- *The five-year strata*: 1950-54, ..., 2020-24, 2025-26.
- *Coincidence* (C12's failure clause): for two deciders, the share of the tested episodes coded for both
  whose first categories coincide, or whose first categories are exact opposites, whichever is larger.
- *Accommodation episodes* are reported apart with their outcomes; censored episodes with what happened
  so far (O1 over the months that exist, at least 12).
"""

from __future__ import annotations

import io
import json
import math
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
from ft.data import dbnomics, freeze, worldbank  # noqa: E402
from ft.quant import regression  # noqa: E402

CARD = K.CARDS / "C18-a5-deciders-bare.yaml"
CARD24 = K.CARDS / "C24-a5-deciders-war-coded.yaml"
C18_RUN = K.RUNS / "C18-a5-deciders-bare.json"
UCDP = ("ucdp/conflict-dyadic-v26.1", "2026-10-01")
C15 = K.RUNS / "C15-e-episodes-closed.json"
C05 = K.RUNS / "C05-e-episodes.json"
C09 = K.RUNS / "C09-e-episodes-excess.json"
DECIDERS = ("D1", "D2", "D4", "D5")
OUTCOMES = ("O1", "O2_net", "O2_gross")
NAMES = {"D1": ("floating", "pegged"), "D2": ("above the floor", "at the floor"),
         "D4": ("government", "banks, others or foreign"), "D5": ("large deficit", "smaller deficit")}
BLOCKS = [(y, min(y + 4, 2026)) for y in range(1950, 2026, 5)]
MIN_TESTED = 10
EXCLUDED_FOR = {"D1": {"floor", "deficit", "past_c"}, "D2": {"peg", "deficit", "past_c"},
                "D4": {"peg", "floor", "deficit"}, "D5": {"peg", "floor", "past_c"}}


# --- the data, loaded once --------------------------------------------------------------------------

class Data:
    def __init__(self) -> None:
        self.annual = K.annual()
        self.monthly = K.monthly()
        m = self.monthly
        self.cpi = {a: g.droplevel(0).dropna() for a, g in m.cpi.groupby(level=0)}
        self.base = {a: g.droplevel(0).dropna() for a, g in m.base.groupby(level=0)}
        self.rate = {a: g.droplevel(0).dropna() for a, g in m.rate_short.astype(float).groupby(level=0)}
        fx = K.ifs("ENDE_XDC_USD_RATE", "M")
        self.fx = {a: g.droplevel(0).dropna() for a, g in fx.groupby(level=0)}
        self.fx_year = {a: g.droplevel(0).dropna() for a, g in self.annual.fx_end.groupby(level=0)}
        self.infl = {a: K.yoy(c) for a, c in self.cpi.items()}
        weo = dbnomics.read("IMF", "WEO:2025-04", ".GGXCNL_NGDP.pcent_gdp", "2026-09-30").dropna(subset=["value"])
        econ = worldbank.read_economies("2026-09-30").set_index("iso3")
        weo = weo.assign(area=weo["weo-country"].map(econ.iso2), year=weo.period.astype(int)).dropna(subset=["area"])
        weo = weo[weo.year <= 2025]
        self.deficit = {(a, y): v for a, y, v in zip(weo.area, weo.year, weo.value)}
        us = K.fred_series("FYFSGDA188S")
        for d, v in us.items():
            if d.year < 1980:
                self.deficit[("US", d.year)] = float(v)
        war = K.wb("VC.BTL.DETH")
        self.war = {k: float(v) for k, v in war.items()}
        self.h41 = {s: K.fred_series(s) for s in ("WALCL", "TREAST", "WSHOMCB")}
        self.nasdaq = K.fred_series("NASDAQCOM")
        self.houses = K.fred_series("CSUSHPISA")
        self.ioer = pd.concat([K.fred_series("IOER"), K.fred_series("IORB")]).sort_index()
        dfr = K.dbnomics.read("ECB", "FM", "D.U2.EUR.4F.KR.DFR.LEV", "2026-09-30").dropna(subset=["value"])
        self.dfr = pd.Series(dfr.value.to_numpy(), index=pd.to_datetime(dfr.period)).sort_index()
        self.mich = K.fred_monthly("MICH")
        self.dgs10 = K.fred_series("DGS10")

    def cb(self, a: str, line: str, year: int) -> float | None:
        try:
            v = self.annual.at[(a, year), line]
        except KeyError:
            return None
        return None if pd.isna(v) else float(v)


# --- outcomes and deciders, per episode -------------------------------------------------------------

def _get(s: pd.Series | None, key):
    if s is None or not len(s):
        return None
    v = s.get(key, np.nan)
    return None if pd.isna(v) else float(v)


def outcomes(D: Data, e: dict, H: int) -> dict:
    a = e["area"]
    m0, c = pd.Period(e["m0"], "M"), pd.Period(e["c"], "M")
    cpi = D.cpi.get(a)
    out = {"O1": None, "O1p": None, "O1pp": None, "O1_stop": None, "O2_gross": None, "O2_net": None,
           "O3": None}
    p0, pm12 = _get(cpi, m0), _get(cpi, m0 - 12)
    end = m0 + H
    pe = _get(cpi, end)
    months = H
    if pe is None and cpi is not None and len(cpi):
        seen = cpi[(cpi.index > m0) & (cpi.index <= end)]
        if len(seen) and (seen.index[-1] - m0).n >= 12:
            months = (seen.index[-1] - m0).n
            pe = float(seen.iloc[-1])
            out["O1_stop"] = str(seen.index[-1])
    if p0 is not None and pe is not None:
        level = 100 * math.log(pe / p0) * 12 / months
        out["O1pp"] = level
        if pm12 is not None:
            out["O1"] = level - 100 * math.log(p0 / pm12)
            if e.get("rise_pct_gdp"):
                out["O1p"] = out["O1"] / float(e["rise_pct_gdp"])
    ys, ye = m0.year - 1, end.year
    ms, me = D.cb(a, "broad", ys), D.cb(a, "broad", ye)
    if ms and me is not None and ms > 0:
        years = ye - ys
        out["O2_gross"] = 100 * (me - ms) / ms / years
        dc = 0.0
        lines = ("cb_gov", "cb_others") if a == "US" else ("cb_gov", "cb_others", "cb_foreign")
        ok = a != "U2"
        for line in lines:
            s0, s1 = D.cb(a, line, ys), D.cb(a, line, ye)
            if s0 is None or s1 is None:
                ok = False
                break
            if line == "cb_foreign":
                f0, f1 = _get(D.fx_year.get(a), ys), _get(D.fx_year.get(a), ye)
                if not f0 or not f1:
                    ok = False
                    break
                s1 = s1 * f0 / f1
            dc += s1 - s0
        if ok:
            out["O2_net"] = 100 * (me - ms - dc) / ms / years
    b = D.base.get(a)
    if b is not None and e["rule"] == "monthly":
        b0, bc, be = _get(b, m0), _get(b, c), _get(b, end)
        path = b[(b.index >= c) & (b.index <= end)]
        if b0 is not None and be is not None and len(path):
            top = float(path.max())
            if top > b0:
                out["O3"] = (top - be) / (top - b0)
    return out


def peg_ratio(D: Data, e: dict) -> float | None:
    """The smallest, over the anchors readable, of the highest rate over the lowest in the 12 months to m0."""
    a = e["area"]
    if a in ("US", "U2"):
        return math.inf  # not pegged by rule
    m0 = pd.Period(e["m0"], "M")
    own = D.fx.get(a)
    if own is None:
        return None
    if e["rule"] == "annual":
        fy = D.fx_year.get(a)
        vals = [_get(fy, m0.year - 1), _get(fy, m0.year - 2)]
        if None in vals or min(vals) <= 0:
            return None
        return max(vals) / min(vals)
    months = pd.period_range(m0 - 11, m0, freq="M")
    x = own.reindex(months)
    if x.isna().any() or (x <= 0).any():
        return None
    ratios = [float(x.max() / x.min())]
    for anchor, last, first in (("GB", None, None), ("FR", "1998-12", None), ("DE", "1998-12", None),
                                ("U2", None, "1999-01")):
        if anchor == a or anchor not in D.fx:
            continue
        if last and months[-1] > pd.Period(last, "M"):
            continue
        if first and months[0] < pd.Period(first, "M"):
            continue
        y = D.fx[anchor].reindex(months)
        if y.isna().any() or (y <= 0).any():
            continue
        cross = x / y
        ratios.append(float(cross.max() / cross.min()))
    return min(ratios)


def rates(D: Data, e: dict, T: float) -> dict:
    a = e["area"]
    m0 = pd.Period(e["m0"], "M")
    r = D.rate.get(a)
    inf = D.infl.get(a)
    r0, r3 = _get(r, m0), _get(r, m0 + 3)
    calm = inf is not None and all(_get(inf, m0 + k) is not None and _get(inf, m0 + k) < T for k in range(4))
    return {"rate_m0": r0, "rate_m3": r3, "calm_m0_m3": calm}


def at_floor(rt: dict, f: float) -> bool | None:
    if rt["rate_m0"] is not None and rt["rate_m0"] <= f:
        return True
    if rt["calm_m0_m3"] and rt["rate_m3"] is not None:
        return rt["rate_m3"] <= f
    if rt["rate_m0"] is not None:
        return False
    return None


def _week_end(s: pd.Series, month: pd.Period) -> float | None:
    x = s[(s.index >= month.start_time) & (s.index <= month.end_time)]
    return None if not len(x) else float(x.iloc[-1])


def channel(D: Data, e: dict) -> dict:
    a = e["area"]
    m0, c = pd.Period(e["m0"], "M"), pd.Period(e["c"], "M")
    if a == "US":
        vals = {}
        for when, month in (("s", m0), ("e", c)):
            w, t, m = (_week_end(D.h41[k], month) for k in ("WALCL", "TREAST", "WSHOMCB"))
            if None in (w, t, m):
                return {"D4": None, "past_c": False}
            vals[when] = {"government": t, "others": m, "banks": w - t - m}
        inc = {k: vals["e"][k] - vals["s"][k] for k in vals["s"]}
        return {"D4": max(inc, key=inc.get), "past_c": False, "increases": inc}
    ys = m0.year if m0.month == 12 else m0.year - 1
    ye = c.year if c.month == 12 else c.year - 1
    past = False
    if ye <= ys:
        ye = c.year if c.month < 12 else c.year + 1
        past = True
    inc = {}
    for name, line in (("government", "cb_gov"), ("banks", "cb_banks"), ("others", "cb_others"),
                       ("foreign", "cb_foreign")):
        s0, s1 = D.cb(a, line, ys), D.cb(a, line, ye)
        if s0 is None or s1 is None:
            return {"D4": None, "past_c": past}
        if line == "cb_foreign":
            f0, f1 = _get(D.fx_year.get(a), ys), _get(D.fx_year.get(a), ye)
            if not f0 or not f1:
                return {"D4": None, "past_c": past}
            s1 = s1 * f0 / f1
        inc[name] = s1 - s0
    return {"D4": max(inc, key=inc.get), "past_c": past, "increases": inc}


def measure(D: Data, e: dict, H: int, T: float) -> dict:
    a = e["area"]
    m0 = pd.Period(e["m0"], "M")
    out = {**outcomes(D, e, H), "peg_ratio": peg_ratio(D, e), **rates(D, e, T), **channel(D, e),
           "deficit": D.deficit.get((a, m0.year - 1)),
           "war_deaths": (D.war.get((a, m0.year), 0.0) if 1989 <= m0.year <= 2024 else None)}
    return out


def categories(m: dict, band: float = 2, floor: float = 0.5, deficit: float = -5) -> dict:
    """Each decider's first category (1), the other (0), or None where it is not coded."""
    lim = (1 + band / 100) / (1 - band / 100)
    pr = m["peg_ratio"]
    d1 = None if pr is None else int(not pr <= lim)
    af = at_floor(m, floor)
    d2 = None if af is None else int(not af)
    d4 = None if m["D4"] is None else int(m["D4"] == "government")
    d5 = None if m["deficit"] is None else int(m["deficit"] <= deficit)
    return {"D1": d1, "D2": d2, "D4": d4, "D5": d5}


# --- the test ---------------------------------------------------------------------------------------

def strata_of(year: int, kind: str) -> int:
    spans = K.ERAS if kind == "eras" else BLOCKS
    for i, (lo, hi) in enumerate(spans):
        if lo <= year <= hi:
            return i
    raise ValueError(year)


def perm_test(values: np.ndarray, cats: np.ndarray, strata: np.ndarray, n_perm: int, seed: int) -> dict:
    """Difference of medians (first category minus the other), two-sided permutation p within strata,
    and each stratum's difference and n."""
    obs = float(np.median(values[cats == 1]) - np.median(values[cats == 0]))
    rng = np.random.default_rng(seed)
    perm = np.empty((n_perm, len(values)), dtype=cats.dtype)
    for s in np.unique(strata):
        idx = np.flatnonzero(strata == s)
        keys = rng.random((n_perm, len(idx)))
        order = np.argsort(keys, axis=1)
        perm[:, idx] = cats[idx][order]
    v = np.broadcast_to(values, perm.shape)
    one = np.where(perm == 1, v, np.nan)
    zero = np.where(perm == 0, v, np.nan)
    diffs = np.nanmedian(one, axis=1) - np.nanmedian(zero, axis=1)
    p = (1 + int(np.sum(np.abs(diffs) >= abs(obs) - 1e-12))) / (1 + n_perm)
    by = []
    for s in np.unique(strata):
        m = strata == s
        n1, n0 = int(np.sum(cats[m] == 1)), int(np.sum(cats[m] == 0))
        d = (float(np.median(values[m & (cats == 1)]) - np.median(values[m & (cats == 0)]))
             if n1 and n0 else None)
        by.append({"stratum": int(s), "n1": n1, "n0": n0, "diff": d, "qualifies": n1 >= 3 and n0 >= 3})
    return {"diff": obs, "p": p, "strata": by, "n1": int(np.sum(cats == 1)), "n0": int(np.sum(cats == 0)),
            "median1": float(np.median(values[cats == 1])), "median0": float(np.median(values[cats == 0]))}


def holm(ps: dict[str, float]) -> dict[str, float]:
    order = sorted(ps, key=ps.get)
    m, adj, running = len(order), {}, 0.0
    for i, k in enumerate(order):
        running = max(running, min(1.0, (m - i) * ps[k]))
        adj[k] = running
    return adj


def verdict(t: dict, alpha: float) -> dict:
    q = [s for s in t["strata"] if s["qualifies"]]
    signs = {int(np.sign(s["diff"])) for s in q if s["diff"] is not None}
    thin = len(q) < 2
    if thin:
        v, sign = "we cannot conclude", None
    elif t["p_holm"] < alpha and len(signs) == 1 and 0 not in signs:
        v, sign = "separates", signs.pop()
    elif t["p_holm"] >= alpha:
        v, sign = "does not separate", None
    else:
        v, sign = "we cannot conclude", None
    return {"verdict": v, "sign": sign, "thin": thin, "qualifying_strata": len(q),
            "pooled_sign_agrees": None if sign is None else int(np.sign(t["diff"])) == sign}


def combine(a: dict | None, b: dict | None) -> dict:
    """C18 (3): the two readings' verdicts into one."""
    if a is None or b is None:
        return {"verdict": "not tested", "sign": None}
    if a["thin"] or b["thin"]:
        thin = [r for r, x in (("at m0", a), ("the design's way", b)) if x["thin"]]
        return {"verdict": "we cannot conclude", "sign": None, "thin_readings": thin}
    if a["verdict"] == b["verdict"] and (a["verdict"] != "separates" or a["sign"] == b["sign"]):
        return {"verdict": a["verdict"], "sign": a["sign"]}
    return {"verdict": "depends on how accommodation is dated", "sign": None}


# --- a run: one list, one set of thresholds, both readings -------------------------------------------

def tested_set(eps: list[dict], reading: str, H: int, T: int, share: float | None) -> list[dict]:
    out = []
    for e in eps:
        apart = "" if share is None else e.get(f"apart_{int(round(share * 100)):03d}", "")
        acc = e[f"acc_m0_T{T}"] if reading == "m0" else e[f"acc_T{T}"]
        if not apart and not e[f"cens_H{H}"] and acc is False:
            out.append(e)
    return out


def run(D: Data, eps: list[dict], *, H: int = 36, T: int = 12, share: float | None = 0.8, band: float = 2,
        floor: float = 0.5, deficit: float = -5, strata: str = "eras", drop=None, cache: dict,
        prm: dict) -> dict:
    """Both readings, every decider and outcome; the combined verdicts."""
    res: dict = {"readings": {}, "combined": {}}
    per_reading = {}
    for reading in ("m0", "design"):
        chosen = tested_set(eps, reading, H, T, share)
        if drop is not None:
            chosen = [e for e in chosen if not drop(e, cache[(id(e), H, T)])]
        rows = []
        for e in chosen:
            m = cache[(id(e), H, T)]
            rows.append((e, m, categories(m, band, floor, deficit)))
        tests: dict = {}
        for o in OUTCOMES:
            raw = {}
            for d in DECIDERS:
                sel = [(m[o], cat[d], int(e["m0"][:4])) for e, m, cat in rows if m[o] is not None and cat[d] is not None]
                if len(sel) < MIN_TESTED or len({c for _, c, _ in sel}) < 2:
                    raw[d] = {"tested": False, "n_coded": len(sel)}
                    continue
                vals = np.array([x for x, _, _ in sel], dtype=float)
                cats = np.array([c for _, c, _ in sel], dtype=np.int8)
                st = np.array([strata_of(y, strata) for _, _, y in sel])
                t = perm_test(vals, cats, st, prm["permutations"], prm["seed"])
                raw[d] = {"tested": True, "n_coded": len(sel), **t}
            adj = holm({d: r["p"] for d, r in raw.items() if r["tested"]})
            for d, r in raw.items():
                if r["tested"]:
                    r["p_holm"] = adj[d]
                    r.update(verdict(r, prm["alpha_after_holm"]))
            tests[o] = raw
        per_reading[reading] = tests
        res["readings"][reading] = {"n_tested": len(chosen), "tests": tests}
    for o in OUTCOMES:
        res["combined"][o] = {}
        for d in DECIDERS:
            a, b = per_reading["m0"][o][d], per_reading["design"][o][d]
            comb = combine(a if a["tested"] else None, b if b["tested"] else None)
            comb["tested_both"] = a["tested"] and b["tested"]
            res["combined"][o][d] = comb
    return res


def load_list(text: str) -> list[dict]:
    return F.from_csv(text)


def old_list(path: Path) -> list[dict]:
    """C05's or C09's list read for C12's method, beside: no jump rule; accommodation at m0 from the
    inflation at m0 (the list's own column), the design's from its T columns."""
    body = json.loads(path.read_text())["result"]
    eps = F.from_csv(body["episodes"])
    for e in eps:
        for T in (10, 12, 20):
            v = e.get("infl_m0")
            e[f"acc_m0_T{T}"] = "cannot be read" if v is None else bool(v >= T)
        for s in F.SHARES:
            e[f"apart_{int(round(s * 100)):03d}"] = ""
        e.setdefault("seam_in_window", False)
    return eps


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm = card["parameters"]
    c15 = json.loads(C15.read_text())
    c15_hash = c15["card_hash"]
    lists = {k: load_list(v) for k, v in c15["result"]["lists"].items()}
    top_money = c15["result"]["summary"]["top_money"]
    D = Data()
    cache: dict = {}

    def prepare(eps, H, Ts=(10, 12, 20)):
        for e in eps:
            for T in Ts:
                key = (id(e), H, T)
                if key not in cache:
                    cache[key] = measure(D, e, H, T)

    head = lists["headline"]
    for name, eps in lists.items():
        H = int(name[1:]) if name in ("H24", "H60") else 36
        prepare(eps, H, (12,) if name != "headline" else (10, 12, 20))
    c05, c09 = old_list(C05), old_list(C09)
    prepare(c05, 36, (12,))
    prepare(c09, 36, (12,))

    R = lambda eps, **kw: run(D, eps, cache=cache, prm=prm, **kw)  # noqa: E731
    headline = R(head)
    counted = {}
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
    counted["war episodes out"] = ("list", R(head, drop=lambda e, m: bool(m["war_deaths"] and m["war_deaths"] >= 1000)))
    counted["episodes starting in 2020-2021 apart"] = ("list", R(head, drop=lambda e, m: e["m0"][:4] in ("2020", "2021")))
    counted[f"the money giving most episodes out ({top_money})"] = ("list", R(head, drop=lambda e, m: e["area"] == top_money))
    counted["D4's read-past-c episodes out"] = ("past_c", R(head, drop=lambda e, m: bool(m["past_c"])))
    counted["five-year strata"] = ("list", R(head, strata="blocks"))
    # C18 (5) names 29 counted runs: C15's eight other X-Y lists and the 21 runs after them. (The first
    # run of this script asserted 30, a miscount, and stopped here before writing or printing anything.)
    assert len(counted) == 29, len(counted)
    beside = {f"jump share {s}": R(head, share=s) for s in (0.5, 0.67, 0.9)}
    beside_not_counted = {"C12's method on C05's list": R(c05, share=None),
                          "C12's method on C09's list": R(c09, share=None)}

    agreement = {}
    for o in OUTCOMES:
        agreement[o] = {}
        for d in DECIDERS:
            h = headline["combined"][o][d]
            rows = []
            for name, (kind, r) in counted.items():
                c = r["combined"][o][d]
                if not c["tested_both"]:
                    continue
                agrees = c["verdict"] == h["verdict"] and (h["verdict"] != "separates" or c["sign"] == h["sign"])
                rows.append((name, kind, agrees))
            n_all, k_all = len(rows), sum(a for _, _, a in rows)
            kept = [r for r in rows if r[1] not in EXCLUDED_FOR[d]]
            n2, k2 = len(kept), sum(a for _, _, a in kept)
            holds = None
            if h["verdict"] in ("separates", "does not separate"):
                holds = n2 > 0 and k2 / n2 >= 2 / 3
            agreement[o][d] = {"headline": h, "k_all": k_all, "n_all": n_all, "k": k2, "n": n2,
                               "holds": holds,
                               "stated": (h["verdict"] if holds or holds is None else f"fragile: {k2} of {n2}")}

    # coincidence of the deciders' categories, the headline's tested episodes, each reading
    coincide = {}
    for reading in ("m0", "design"):
        chosen = tested_set(head, reading, 36, 12, 0.8)
        cats = [categories(cache[(id(e), 36, 12)]) for e in chosen]
        pairs = {}
        for i, d1 in enumerate(DECIDERS):
            for d2 in DECIDERS[i + 1:]:
                both = [(c[d1], c[d2]) for c in cats if c[d1] is not None and c[d2] is not None]
                if not both:
                    continue
                same = sum(x == y for x, y in both) / len(both)
                pairs[f"{d1}-{d2}"] = {"n": len(both), "same": round(same, 3), "opposite": round(1 - same, 3),
                                       "cannot_tell_apart": max(same, 1 - same) > 0.8}
        coincide[reading] = pairs

    # descriptive: O1 on the four deciders, era dummies and the rise (OLS, robust errors)
    descriptive = {}
    for reading in ("m0", "design"):
        chosen = tested_set(head, reading, 36, 12, 0.8)
        recs = []
        for e in chosen:
            m = cache[(id(e), 36, 12)]
            c = categories(m)
            if m["O1"] is None or None in c.values():
                continue
            y = int(e["m0"][:4])
            recs.append({"O1": m["O1"], **{d: c[d] for d in DECIDERS}, "rise": float(e["rise_pct_gdp"]),
                         "era2": int(1972 <= y <= 1999), "era3": int(y >= 2000)})
        if len(recs) >= 20:
            df = pd.DataFrame(recs)
            X = df[[*DECIDERS, "rise", "era2", "era3"]]
            X = X.loc[:, X.std() > 0]
            descriptive[reading] = regression.ols(df["O1"], X).as_dict()
        else:
            descriptive[reading] = {"nobs": len(recs), "note": "too few episodes coded for all four"}

    # what happened: the tested episodes' outcomes, accommodation and censored apart
    def describe(eps, reading, H=36):
        rows = [cache[(id(e), H, 12)] for e in tested_set(eps, reading, H, 12, 0.8)]
        o1 = np.array([m["O1"] for m in rows if m["O1"] is not None], dtype=float)
        o1pp = np.array([m["O1pp"] for m in rows if m["O1pp"] is not None], dtype=float)
        o2g = np.array([m["O2_gross"] for m in rows if m["O2_gross"] is not None], dtype=float)
        o2n = np.array([m["O2_net"] for m in rows if m["O2_net"] is not None], dtype=float)
        o3 = np.array([m["O3"] for m in rows if m["O3"] is not None], dtype=float)

        def q(x):
            return None if not len(x) else {"n": int(len(x)), "median": float(np.median(x)),
                                             "p25": float(np.quantile(x, 0.25)), "p75": float(np.quantile(x, 0.75)),
                                             "share_above_zero": float(np.mean(x > 0))}
        return {"O1": q(o1), "O1pp": q(o1pp), "O2_gross": q(o2g), "O2_net": q(o2n), "O3": q(o3),
                "O1_stopped_early": sum(m["O1_stop"] is not None for m in rows)}

    acc_apart = [e for e in head if e["acc_T12"] is True and not e["cens_H36"] and not e["apart_080"]]
    acc_o1 = np.array([cache[(id(e), 36, 12)]["O1"] for e in acc_apart if cache[(id(e), 36, 12)]["O1"] is not None])
    cens = [e for e in head if e["cens_H36"] and not e["apart_080"]]
    cens_rows = [{"area": e["area"], "m0": e["m0"], "c": e["c"], "O1_so_far": cache[(id(e), 36, 12)]["O1"],
                  "O1_stop": cache[(id(e), 36, 12)]["O1_stop"]} for e in cens]

    # the headline tested list, one line per episode, with its deciders and outcomes
    lines = []
    for e in head:
        m = cache[(id(e), 36, 12)]
        c = categories(m)
        lines.append({"area": e["area"], "m0": e["m0"], "c": e["c"], "rise_pct_gdp": e["rise_pct_gdp"],
                      "apart": e["apart_080"], "flag": e["flag"], "seam_in_window": e["seam_in_window"],
                      "tested_m0": e in tested_set([e], "m0", 36, 12, 0.8),
                      "tested_design": e in tested_set([e], "design", 36, 12, 0.8),
                      "acc_m0": e["acc_m0_T12"], "acc_design": e["acc_T12"], "censored": e["cens_H36"],
                      **{k: m[k] for k in ("O1", "O1p", "O1pp", "O1_stop", "O2_gross", "O2_net", "O3", "peg_ratio",
                                           "rate_m0", "rate_m3", "D4", "past_c", "deficit", "war_deaths")},
                      **{f"cat_{d}": c[d] for d in DECIDERS}})

    # the United States and the euro area, described (D3, D6, O4)
    described = []
    for e in head:
        if e["area"] not in ("US", "U2"):
            continue
        m0, c = pd.Period(e["m0"], "M"), pd.Period(e["c"], "M")
        end = m0 + 36
        row = {"area": e["area"], "m0": e["m0"], "c": e["c"], **{k: cache[(id(e), 36, 12)][k] for k in ("O1", "O1pp", "O2_gross", "O2_net", "O3", "D4")}}
        if e["area"] == "US":
            io = D.ioer[(D.ioer.index >= m0.start_time) & (D.ioer.index <= (m0 + 3).end_time)]
            row["D3_paid_by_m0_plus_3"] = bool(len(io))
            row["D3_rate_first"] = None if not len(io) else float(io.iloc[0])
            row["D3_first_day"] = None if not len(io) else str(io.index[0].date())
            row["D6_michigan_m0"] = _get(D.mich, m0)
            ten = D.dgs10[(D.dgs10.index >= m0.start_time) & (D.dgs10.index <= m0.end_time)]
            row["D6_ten_year_m0"] = None if not len(ten) else float(ten.mean())
            for name, s in (("O4_nasdaq_pct", D.nasdaq), ("O4_houses_pct", D.houses)):
                x0 = s[(s.index >= m0.start_time) & (s.index <= m0.end_time)]
                x1 = s[(s.index >= end.start_time) & (s.index <= end.end_time)]
                row[name] = None if not len(x0) or not len(x1) else float(100 * (x1.mean() / x0.mean() - 1))
        else:
            dd = D.dfr[(D.dfr.index >= m0.start_time) & (D.dfr.index <= m0.end_time)]
            row["D3_deposit_rate_m0"] = None if not len(dd) else float(dd.mean())
        described.append(row)

    payload = {
        "c15": {"card_hash": c15_hash, "run_at": c15["run_at"]},
        "headline": headline,
        "counted": {k: {"kind": kind, **r} for k, (kind, r) in counted.items()},
        "beside_the_headline": beside,
        "beside_not_counted": beside_not_counted,
        "two_thirds": agreement,
        "coincidence": coincide,
        "descriptive_regression": descriptive,
        "what_happened": {"m0": describe(head, "m0"), "design": describe(head, "design"),
                          "H24_design": describe(lists["H24"], "design", 24),
                          "H60_design": describe(lists["H60"], "design", 60)},
        "accommodation_apart": {"n": len(acc_apart), "O1_n": int(len(acc_o1)),
                                "O1_median": float(np.median(acc_o1)) if len(acc_o1) else None},
        "censored_apart": cens_rows,
        "described_us_euro": described,
        "episodes": lines,
    }
    out = cards.write_result(K.STUDY, CARD, payload)
    print(out, f"{out.stat().st_size / 1e6:.2f} MB")
    return out


# --- C24: C18's war-out run with the wars of 1946-1988 coded -----------------------------------------
#
# Readings of card C24 that its text leaves to the code, fixed here before the run:
#
# - *The table GW_ISO2* matches each Gleditsch-Ward number the dataset gives in a 1946-1988 intensity-2 row
#   to the study's economy code (the same country's modern code; None where the place had no money of its
#   own). It is made from the dataset's own names and numbers; a number with no entry stops the run.
# - *Several countries in a row's gwno_loc* (an inter-state war) each count as the location.
# - *The year* is the year of m0, as C18's; 1989-2024 is C18's World Bank rule untouched, 1946-1988 the
#   dataset's rows with year = Y and intensity_level = 2, and before 1946 the Correlates of War lists, which
#   code no episode (the list's first start is 1963): the run asserts that no episode starts before 1946.
# - *Headline rerun* must equal C18's stored headline in every p, difference and verdict (floats to 1e-9);
#   if not, the result says ``void`` and nothing is read from it.
# - *Two thirds* (C18 (4)) is computed by ``agreement_of``, a copy of main()'s loop; it is first run on
#   C18's own stored counted runs and must reproduce C18's stored ``two_thirds`` before it is trusted.

#: Gleditsch-Ward number -> the study's economy code, for every number in a 1946-1988 intensity-2 row.
GW_ISO2 = {
    40: "CU", 91: "HN", 92: "SV", 93: "NI", 94: "CR", 100: "CO", 135: "PE", 145: "BO", 150: "PY",
    200: "GB", 220: "FR", 310: "HU", 350: "GR", 352: "CY", 365: "RU",  # 365: Russia, the Soviet Union
    471: "CM", 475: "NG", 483: "TD", 490: "CD", 500: "UG", 501: "KE", 520: "SO", 530: "ET", 540: "AO",
    541: "MZ", 552: "ZW", 560: "ZA", 580: "MG", 600: "MA", 615: "DZ", 616: "TN", 620: "LY", 625: "SD",
    630: "IR", 640: "TR", 645: "IQ", 651: "EG", 652: "SY", 660: "LB", 663: "JO", 666: "IL",
    678: "YE", 680: "YE",  # North Yemen, South Yemen
    700: "AF", 710: "CN", 713: "TW", 731: "KP", 732: "KR", 750: "IN",
    751: None,  # Hyderabad: no money of its own
    770: "PK", 775: "MM", 780: "LK", 811: "KH", 812: "LA",
    816: "VN", 817: "VN",  # North Vietnam, South Vietnam
    820: "MY", 840: "PH", 850: "ID",
}


def acd_war_years() -> tuple[dict[str, set[int]], list[dict]]:
    """Economy code -> the years 1946-1988 in which UCDP/PRIO's armed conflict dataset has an intensity-2
    row (at least 1,000 battle deaths in the year) with the economy among the conflict's locations; and the
    rows used, for the record."""
    fz = freeze.load(*UCDP)
    d = pd.read_csv(io.BytesIO(fz.read_bytes("UcdpPrioConflict_v26_1.csv")))
    w = d[(d.intensity_level == 2) & d.year.between(1946, 1988)]
    out: dict[str, set[int]] = {}
    rows = []
    for _, r in w.iterrows():
        for g in str(r.gwno_loc).split(","):
            g = int(g.strip())
            if g not in GW_ISO2:
                raise KeyError(f"Gleditsch-Ward number {g} ({r.location}, {int(r.year)}) has no entry in GW_ISO2")
            iso = GW_ISO2[g]
            rows.append({"conflict_id": int(r.conflict_id), "location": r.location, "gwno": g, "year": int(r.year),
                         "economy": iso})
            if iso:
                out.setdefault(iso, set()).add(int(r.year))
    return out, rows


def war_coded(e: dict, m: dict, acd: dict[str, set[int]]) -> bool:
    """C24 (1): is the episode's m0 year a war year for its economy?"""
    y = int(e["m0"][:4])
    if y >= 1989:
        return bool(m["war_deaths"] and m["war_deaths"] >= 1000)  # C18's rule (the World Bank, to 2024)
    if y >= 1946:
        return y in acd.get(e["area"], set())
    raise AssertionError(f"an episode starts before 1946 ({e['area']} {e['m0']}): the COW rule was never coded")


def agreement_of(headline: dict, counted: dict) -> dict:
    """C18 (4)'s two-thirds count, a copy of main()'s loop, on a headline and a dict of counted runs
    (``{name: {"kind": ..., "combined": ...}}``)."""
    agreement: dict = {}
    for o in OUTCOMES:
        agreement[o] = {}
        for d in DECIDERS:
            h = headline["combined"][o][d]
            rows = []
            for name, r in counted.items():
                c = r["combined"][o][d]
                if not c["tested_both"]:
                    continue
                agrees = c["verdict"] == h["verdict"] and (h["verdict"] != "separates" or c["sign"] == h["sign"])
                rows.append((name, r["kind"], agrees))
            n_all, k_all = len(rows), sum(a for _, _, a in rows)
            kept = [x for x in rows if x[1] not in EXCLUDED_FOR[d]]
            n2, k2 = len(kept), sum(a for _, _, a in kept)
            holds = None
            if h["verdict"] in ("separates", "does not separate"):
                holds = n2 > 0 and k2 / n2 >= 2 / 3
            agreement[o][d] = {"headline": h, "k_all": k_all, "n_all": n_all, "k": k2, "n": n2, "holds": holds,
                               "stated": (h["verdict"] if holds or holds is None else f"fragile: {k2} of {n2}")}
    return agreement


def _same(a, b, tol: float = 1e-9) -> bool:
    """Two JSON-shaped values equal, floats to ``tol`` (the stored result went through json)."""
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k], tol) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    return a == b


def _roundtrip(x):
    return json.loads(json.dumps(x, default=str))


def war() -> Path:
    """C24: the headline rerun, and the headline with the episodes whose m0 year is a war year out (C24 (1)-(3))."""
    card = yaml.safe_load(CARD24.read_text())
    cards.require_locked(CARD24)
    prm = card["parameters"]
    c18 = json.loads(C18_RUN.read_text())
    assert c18["card_hash"] == card["parent"]["hash"], "C18's run is not the card's parent"
    c15 = json.loads(C15.read_text())
    assert c15["card_hash"] == c18["result"]["c15"]["card_hash"], "C18 ran on another C15"
    lists = {k: load_list(v) for k, v in c15["result"]["lists"].items()}
    head = lists["headline"]
    assert min(int(e["m0"][:4]) for e in head) >= 1946
    acd, acd_rows = acd_war_years()
    D = Data()
    cache: dict = {}
    for e in head:
        cache[(id(e), 36, 12)] = measure(D, e, 36, 12)
    R = lambda eps, **kw: run(D, eps, cache=cache, prm=prm, **kw)  # noqa: E731
    headline = R(head)
    extended = R(head, drop=lambda e, m: war_coded(e, m, acd))

    reproduces = _same(_roundtrip(headline), c18["result"]["headline"])
    old = c18["result"]["counted"]
    two_thirds_check = _same(_roundtrip(agreement_of(c18["result"]["headline"], old)), c18["result"]["two_thirds"])
    counted2 = {k: v for k, v in old.items()}
    counted2["war episodes out"] = {"kind": "list", **_roundtrip(extended)}
    two_thirds_new = agreement_of(c18["result"]["headline"], counted2)

    old_war = old["war episodes out"]
    cells = []
    for o in OUTCOMES:
        for d in DECIDERS:
            h, w_old, w_new = (headline["combined"][o][d], old_war["combined"][o][d], extended["combined"][o][d])
            cells.append({"outcome": o, "decider": d, "headline": h["verdict"], "headline_sign": h["sign"],
                          "c18_war_out": w_old["verdict"], "c18_war_out_sign": w_old["sign"],
                          "extended": w_new["verdict"], "extended_sign": w_new["sign"],
                          "extended_tested_both": w_new["tested_both"],
                          "differs_from_headline": (w_new["verdict"] != h["verdict"] or w_new["sign"] != h["sign"]),
                          "differs_from_c18_war_out": (w_new["verdict"] != w_old["verdict"] or w_new["sign"] != w_old["sign"])})
    out_lines: dict = {}
    for reading in ("m0", "design"):
        chosen = tested_set(head, reading, 36, 12, 0.8)
        taken = [(e, cache[(id(e), 36, 12)]) for e in chosen if war_coded(e, cache[(id(e), 36, 12)], acd)]
        out_lines[reading] = {
            "tested": len(chosen), "out": len(taken),
            "from_1989": sum(int(e["m0"][:4]) >= 1989 for e, _ in taken),
            "before_1989": sum(int(e["m0"][:4]) < 1989 for e, _ in taken),
            "before_1989_list": [{"area": e["area"], "m0": e["m0"], "war_year": int(e["m0"][:4])}
                                 for e, _ in taken if int(e["m0"][:4]) < 1989]}
    pre_all = [{"area": e["area"], "m0": e["m0"]} for e in head
               if int(e["m0"][:4]) < 1989 and war_coded(e, cache[(id(e), 36, 12)], acd)]
    payload = {
        "c18": {"card_hash": c18["card_hash"], "run_at": c18["run_at"]},
        "headline_reproduces_c18": reproduces, "two_thirds_function_reproduces_c18": two_thirds_check,
        "void": not (reproduces and two_thirds_check),
        "n_tested": {"headline": {r: headline["readings"][r]["n_tested"] for r in ("m0", "design")},
                     "c18_war_out": {r: old_war["readings"][r]["n_tested"] for r in ("m0", "design")},
                     "extended": {r: extended["readings"][r]["n_tested"] for r in ("m0", "design")}},
        "episodes_out": out_lines,
        "list_episodes_before_1989": sum(int(e["m0"][:4]) < 1989 for e in head),
        "list_episodes_before_1989_war_coded": pre_all,
        "cells": cells,
        "cells_differing_from_headline": sum(c["differs_from_headline"] for c in cells),
        "cells_differing_from_c18_war_out": sum(c["differs_from_c18_war_out"] for c in cells),
        "extended": extended,
        "two_thirds_with_extended": two_thirds_new, "two_thirds_c18": c18["result"]["two_thirds"],
        "acd_war_years": {k: sorted(v) for k, v in sorted(acd.items())},
        "acd_rows_used": acd_rows,
    }
    out = cards.write_result(K.STUDY, CARD24, payload)
    print(out, f"{out.stat().st_size / 1e6:.2f} MB")
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["C24"]:
        war()
    else:
        main()
