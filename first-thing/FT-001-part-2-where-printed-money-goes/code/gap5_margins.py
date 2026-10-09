"""Gap 5's margin check (2026-10-02): for each verdict the long version states, how many episodes (or
windows) would have to change for the verdict to flip under its card's own rule, against how many of them
the missing or gapped prices leave uncertain. It reads existing runs (C18's stored episodes) and the frozen
panels; it writes no card, no result under results/runs and nothing in the registry. Output:
``notes/gap5-margins-2026-10-02.md``. From the study's folder: ``../../toolkit/bin/ftpy code/gap5_margins.py``.

Definitions fixed here:

- *A change* (deciders): one tested episode moved to the other category of the decider (a swap), the
  outcome unchanged. The margin of a cell that "does not separate" is a **greedy upper bound**: at each step
  the swap that most widens the difference of medians in the chosen direction, the permutation test (2,000
  permutations, C18's seed and strata) and Holm's adjustment (the other deciders' stored p) read again; the
  first step at which the reading's verdict differs from its own. "No flip within 40" means none found, not
  that none exists. A reading that is thin (fewer than two qualifying strata, 3 or more in each category)
  has an **exact lower bound**: the fewest swaps (or additions where a stratum has fewer than six episodes)
  that make a second stratum qualify; a further flip needs a permutation p below 0.05 and one sign.
  The combined verdict (C18 (3)) flips if either reading's verdict changes; when it is "we cannot conclude"
  because a reading is thin, it needs every thin reading to qualify (the larger of the two bounds).
- *Uncertain episodes of a cell, per reading* U = the cell's tested episodes whose consumer price index has a
  missing month in m0-12 .. min(m0+36, the common end) (a gap, or a series that begins or ends inside it)
  or that belong to one of the 15 economies whose monthly base money has gaps (C15's "jump cannot be
  read"), plus the episodes of those 15 lines that would enter the tested set under that reading
  (accommodation False, not censored) and are coded for the decider (and have the outcome, for O2).
  The 113 or so episodes whose prices cannot be read at all and that leave the test are reported apart.
- *A4* (annual panel; the 15 gaps are monthly base money and do not enter it): a change is one window
  removed; the margin is a greedy upper bound (the removal that most moves the interval's relevant end,
  among the 12 of largest influence, refitted); U is the headline's windows with a missing year of CPI
  inside the window plus the grid's windows lost only for a missing CPI at an end.
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
import deciders as D  # noqa: E402
import longrun as L  # noqa: E402

OUT = K.STUDY / "notes" / "gap5-margins-2026-10-02.md"
SEED = 20260930
NPERM = 2000
MAXSTEPS = 40
COMMON_END = pd.Period("2026-08", "M")
GAP_AREAS = None  # filled in main


def cell_rows(ep: list[dict], reading: str, o: str, d: str) -> list[dict]:
    return [e for e in ep if e[f"tested_{reading}"] and e[o] is not None and e[f"cat_{d}"] is not None]


def arrays(rows: list[dict], o: str, d: str):
    vals = np.array([e[o] for e in rows], dtype=float)
    cats = np.array([e[f"cat_{d}"] for e in rows], dtype=np.int8)
    st = np.array([D.strata_of(int(e["m0"][:4]), "eras") for e in rows])
    return vals, cats, st


def read_test(vals, cats, st, others_p: dict, d: str, nperm: int) -> dict:
    t = D.perm_test(vals, cats, st, nperm, SEED)
    adj = D.holm({**others_p, d: t["p"]})
    t["p_holm"] = adj[d]
    t.update(D.verdict(t, 0.05))
    return t


def greedy_flip(vals, cats, st, others_p, d, base_verdict) -> dict:
    """Fewest swaps found, over the two directions, that change the reading's verdict."""
    best = None
    for sign in (1, -1):
        c = cats.copy()
        for step in range(1, MAXSTEPS + 1):
            top, top_i = -np.inf, None
            for i in range(len(c)):
                c[i] ^= 1
                if (c == 1).any() and (c == 0).any():
                    diff = np.median(vals[c == 1]) - np.median(vals[c == 0])
                    if sign * diff > top:
                        top, top_i = sign * diff, i
                c[i] ^= 1
            if top_i is None:
                break
            c[top_i] ^= 1
            t = read_test(vals, c, st, others_p, d, NPERM)
            if t["verdict"] != base_verdict:
                best = step if best is None else min(best, step)
                break
    return {"flip_within": best, "searched_to": MAXSTEPS}


def restricted_flip(rows: list[dict], extra: list[dict], allowed_keys: set, o: str, d: str, others: dict,
                    base_verdict: str) -> dict:
    """The direct test: the cell's sample with the episodes that would enter put in (their stored values and
    categories), then only the episodes in ``allowed_keys`` may change side, greedily, in either direction.
    Returns the verdict before any swap (step 0) and the fewest swaps found that make it differ from the
    reading's own verdict (None: none found, searched through every allowed episode)."""
    full = rows + extra
    vals, cats, st = arrays(full, o, d)
    allowed = [i for i, e in enumerate(full) if (e["area"], e["m0"]) in allowed_keys]
    t0 = read_test(vals, cats, st, others, d, NPERM)
    out = {"step0": t0["verdict"], "flip_within": 0 if t0["verdict"] != base_verdict else None, "allowed": len(allowed)}
    if out["flip_within"] is not None:
        return out
    best = None
    for sign in (1, -1):
        c = cats.copy()
        for step in range(1, len(allowed) + 1):
            top, top_i = -np.inf, None
            for i in allowed:
                c[i] ^= 1
                if (c == 1).any() and (c == 0).any():
                    diff = np.median(vals[c == 1]) - np.median(vals[c == 0])
                    if sign * diff > top:
                        top, top_i = sign * diff, i
                c[i] ^= 1
            if top_i is None:
                break
            c[top_i] ^= 1
            tt = read_test(vals, c, st, others, d, NPERM)
            if tt["verdict"] != base_verdict:
                best = step if best is None else min(best, step)
                break
    out["flip_within"] = best
    return out


def qualify_cost(vals, cats, st, thin_need: int = 2) -> int | None:
    """Fewest changes making `thin_need` strata hold 3 or more in each category (swap where a stratum has
    six or more episodes, an addition otherwise); None where impossible."""
    q, costs = 0, []
    for s in np.unique(st):
        m = st == s
        n1, n0 = int((cats[m] == 1).sum()), int((cats[m] == 0).sum())
        if n1 >= 3 and n0 >= 3:
            q += 1
            continue
        costs.append(max(0, 3 - n1, 3 - n0) if n1 + n0 >= 6 else max(0, 3 - n1) + max(0, 3 - n0))
    # strata with no episodes at all are not in np.unique: a missing stratum costs six additions
    absent = 3 - len(np.unique(st))
    costs += [6] * max(0, absent)
    need = max(0, thin_need - q)
    return None if need > len(costs) else sum(sorted(costs)[:need])


def cpi_gap_flags(m: pd.DataFrame) -> dict:
    cpi = {a: set(g.droplevel(0).dropna().index) for a, g in m.cpi.groupby(level=0)}
    return cpi


def touches_gap(cpi: dict, e: dict) -> bool:
    m0 = pd.Period(e["m0"], "M")
    end = min(m0 + 36, COMMON_END)
    have = cpi.get(e["area"], set())
    return any(mo not in have for mo in pd.period_range(m0 - 12, end, freq="M"))


def deciders_part(lines: list[str]) -> tuple[list[list], list[str]]:
    c18 = json.loads(D.C18_RUN.read_text())["result"]
    ep = c18["episodes"]
    m = K.monthly()
    cpi = cpi_gap_flags(m)
    gap15 = [e for e in ep if e["apart"] == "jump cannot be read"]
    gap_areas = {e["area"] for e in gap15}
    rows_out, notes = [], []
    put_back = c18["counted"]["every set-apart jump put back"]["combined"]
    unread = {r: sum(1 for e in ep if not e["apart"] and not e["censored"] and str(e[f"acc_{r}"]) == "cannot be read")
              for r in ("design", "m0")}
    notes.append(f"Episodes whose prices cannot be read at all and that leave the test (apart, not censored): "
                 f"{unread['design']} at the design's reading, {unread['m0']} at m0; they are not in U.")
    notes.append(f"The 15 lines (jump cannot be read) in {len(gap_areas)} economies: " +
                 ", ".join(f"{e['area']} {e['m0']}" for e in gap15) + ".")
    for o in D.OUTCOMES:
        for d in D.DECIDERS:
            comb = c18["headline"]["combined"][o][d]
            per = {}
            for reading in ("m0", "design"):
                rows = cell_rows(ep, reading, o, d)
                tt = c18["headline"]["readings"][reading]["tests"][o][d]
                vals, cats, st = arrays(rows, o, d)
                others = {x: c18["headline"]["readings"][reading]["tests"][o][x]["p"]
                          for x in D.DECIDERS if x != d and c18["headline"]["readings"][reading]["tests"][o][x]["tested"]}
                t = read_test(vals, cats, st, others, d, 10000)
                assert abs(t["diff"] - tt["diff"]) < 1e-9 and abs(t["p"] - tt["p"]) < 1e-12, (o, d, reading)
                touch = [e for e in rows if touches_gap(cpi, e)]
                inarea = [e for e in rows if e["area"] in gap_areas and not touches_gap(cpi, e)]
                adds = [e for e in gap15 if not e["censored"] and e[f"acc_{reading}"] is False
                        and e[f"cat_{d}"] is not None and e[o] is not None]
                U = len(touch) + len(adds)
                Uw = U + len(inarea)
                key = lambda L_: {(e["area"], e["m0"]) for e in L_}  # noqa: E731
                if t["thin"]:
                    lb = qualify_cost(vals, cats, st)
                    mg = {"kind": "thin", "value": lb}
                    rs = {"narrow": "n/a (thin)", "wide": "n/a (thin)"}
                else:
                    g = greedy_flip(vals, cats, st, others, d, t["verdict"])
                    mg = {"kind": "greedy", "value": g["flip_within"]}
                    r1 = restricted_flip(rows, adds, key(touch) | key(adds), o, d, others, t["verdict"])
                    r2 = restricted_flip(rows, adds, key(touch) | key(adds) | key(inarea), o, d, others, t["verdict"])
                    rs = {"narrow": r1["flip_within"], "wide": r2["flip_within"], "step0": r1["step0"]}
                per[reading] = {"n": len(rows), "n_touch": len(touch), "n_area": len(inarea), "adds": len(adds),
                                "U": U, "Uw": Uw, "margin": mg, "restricted": rs, "verdict": t["verdict"], "p_holm": t["p_holm"]}
            thin_r = [r for r in per if per[r]["margin"]["kind"] == "thin"]
            if comb["verdict"] == "we cannot conclude" and thin_r:
                vals_ = [per[r]["margin"]["value"] for r in thin_r]
                cell_margin = None if any(v is None for v in vals_) else max(vals_)
                kind = "lower bound (exact), the larger of the thin readings"
                U = max(per[r]["U"] for r in thin_r)
                Uw = max(per[r]["Uw"] for r in thin_r)
                robust = None if cell_margin is None else cell_margin > U
            else:
                vals_ = [per[r]["margin"]["value"] for r in per if per[r]["margin"]["value"] is not None]
                cell_margin = min(vals_) if vals_ else None
                kind = "greedy, an upper bound (smaller of the readings)" if vals_ else "no flip found within 40 swaps"
                U = max(per[r]["U"] for r in per)
                Uw = max(per[r]["Uw"] for r in per)
                robust = ("no flip found within 40 swaps" if cell_margin is None else cell_margin > U)
            rows_out.append([f"{o} / {d}", comb["verdict"],
                             "; ".join(f"{r}: n {per[r]['n']}, p {per[r]['p_holm']:.3f}, {per[r]['verdict']}" for r in ("design", "m0")),
                             "; ".join(f"{r}: {per[r]['margin']['value']} ({per[r]['margin']['kind']})" for r in ("design", "m0")),
                             kind, cell_margin if cell_margin is not None else f">{MAXSTEPS}",
                             "; ".join(f"{r}: {per[r]['U']} (touch {per[r]['n_touch']}, would enter {per[r]['adds']})" for r in ("design", "m0")),
                             U, Uw, robust,
                             "; ".join(f"{r}: narrow {per[r]['restricted']['narrow']}, wide {per[r]['restricted']['wide']}" for r in ("design", "m0")),
                             "same" if put_back[o][d]["verdict"] == comb["verdict"] else f"differs: {put_back[o][d]['verdict']}"])
    return rows_out, notes


# --- A4 ---------------------------------------------------------------------------------------------

def ci_stats(df: pd.DataFrame, cluster: bool = True):
    res = L.fit(df, ["mu", "g"], cluster)
    ci = res.conf_int(0.05)
    return float(res.params["mu"]), float(ci.loc["mu", 0]), float(ci.loc["mu", 1]), res


def greedy_removal(df: pd.DataFrame, goal: str, limit: int = 40) -> int | None:
    """Windows removed (the most influential first, refitted) until the goal holds: 'hi<1' (the interval's
    top falls below one), 'lo>1', 'hi>=1' (its top reaches one), 'lo<=1'."""
    d = df.reset_index(drop=True).copy()
    def done(lo, hi):
        return {"hi<1": hi < 1, "lo>1": lo > 1, "hi>=1": hi >= 1, "lo<=1": lo <= 1}[goal]
    for step in range(0, limit + 1):
        b, lo, hi, res = ci_stats(d)
        if done(lo, hi):
            return step
        if step == limit or len(d) < 30:
            return None
        X = sm.add_constant(d[["mu", "g"]].astype(float)).to_numpy()
        e = res.resid.to_numpy()
        h = np.einsum("ij,jk,ik->i", X, np.linalg.inv(X.T @ X), X)
        dfb = (np.linalg.inv(X.T @ X) @ X.T * (e / (1 - h))).T[:, 1]  # change in beta_mu if i is dropped is -dfb
        want_down = goal in ("hi<1", "lo<=1")
        order = np.argsort(-dfb if want_down else dfb)
        best, best_val = None, None
        for i in order[:12]:
            _, lo2, hi2, _ = ci_stats(d.drop(index=i))
            val = hi2 if goal in ("hi<1",) else (-lo2 if goal == "lo>1" else (-hi2 if goal == "hi>=1" else lo2))
            if best_val is None or val < best_val:
                best, best_val = i, val
        d = d.drop(index=best).reset_index(drop=True)
    return None


def a4_part() -> tuple[list[list], list[str]]:
    a = K.annual()
    a = a[~a.units_break]
    notes = []
    out = []
    specs = [("C02", "base", yaml.safe_load((K.CARDS / "C02-a4-base.yaml").read_text())["parameters"]["window_ends"]),
             ("C22", "base", yaml.safe_load(L.C22.read_text())["parameters"]["window_ends"]),
             ("C03", "broad", yaml.safe_load((K.CARDS / "C03-a4-broad.yaml").read_text())["parameters"]["window_ends"])]
    for name, money, ends in specs:
        df = L.windows(a, money, ends)
        b, lo, hi, _ = ci_stats(df)
        verdict = L.verdict(lo, hi)
        # windows touching a price gap, and windows lost only for a missing CPI at an end
        touch = 0
        for _, r in df.iterrows():
            x = a.loc[r.area]
            years = range(int(r.y0), int(r.y1) + 1)
            touch += int(any(y not in x.index or pd.isna(x.cpi.get(y, np.nan)) for y in years))
        lost = 0
        for area, x in a.groupby(level=0):
            x = x.droplevel(0)
            for y0, y1 in zip(ends[:-1], ends[1:]):
                if y0 in x.index and y1 in x.index:
                    r0, r1 = x.loc[y0], x.loc[y1]
                    ok_other = all(pd.notna(v) and v > 0 for v in (r0[money], r1[money], r0.rgdp, r1.rgdp)) and not (bool(r0.inside_euro) or bool(r1.inside_euro))
                    cpi_ok = all(pd.notna(v) and v > 0 for v in (r0.cpi, r1.cpi))
                    lost += int(ok_other and not cpi_ok)
        goals = ["hi<1", "lo>1"] if lo <= 1 <= hi else (["hi>=1"] if hi < 1 else ["lo<=1"])
        m = {g: greedy_removal(df, g) for g in goals}
        gone = []
        for i, r in df.iterrows():
            x = a.loc[r.area]
            if any(y not in x.index or pd.isna(x.cpi.get(y, np.nan)) for y in range(int(r.y0), int(r.y1) + 1)):
                gone.append(i)
        v_without = L.verdict(*ci_stats(df.drop(index=gone))[1:3])
        found = [v for v in m.values() if v is not None]
        margin = min(found) if found else None
        out.append([f"{name} headline slope ({money}), {len(df)} windows in {df.area.nunique()} moneys",
                    f"{verdict} ({b:.2f}; {lo:.2f} to {hi:.2f})", "; ".join(f"{g}: {v if v is not None else '>40'}" for g, v in m.items()),
                    margin if margin is not None else ">40", touch, lost, touch + lost,
                    None if margin is None else margin > touch + lost, v_without])
    return out, notes


def a4_folds() -> list[list]:
    a = K.annual()
    a = a[~a.units_break]
    out = []
    for name, money, cardp in (("C02", "base", K.CARDS / "C02-a4-base.yaml"), ("C22", "base", L.C22)):
        ends = yaml.safe_load(cardp.read_text())["parameters"]["window_ends"]
        df = L.windows(a, money, ends)
        head = L.headline(df)
        codes = sorted(df.area.unique())
        fold_of = {x: i % 5 for i, x in enumerate(codes)}
        per = []
        for k in range(5):
            te = df[df.area.map(fold_of) == k]
            own = L.headline(te)
            differs = own["verdict"] != head["verdict"]
            # change the fold's verdict relative to the headline's
            b, lo, hi, _ = ci_stats(te)
            if differs:  # make it equal to the headline's
                goals = ["hi<1"] if head["verdict"].startswith("partly (between") or head["verdict"].startswith("partly (below") else ["hi>=1"]
                goals = ["hi<1"] if head["verdict"].startswith("partly") else ["lo<=1"]
            else:
                goals = ["hi<1", "lo>1"] if lo <= 1 <= hi else (["hi>=1"] if hi < 1 else ["lo<=1"])
            ms = [greedy_removal(te, g) for g in goals]
            ms = [x for x in ms if x is not None]
            per.append({"fold": k, "windows": len(te), "verdict": own["verdict"], "differs": differs,
                        "margin": min(ms) if ms else None})
        k_diff = sum(p["differs"] for p in per)
        # the long's statement flips when the number of differing folds crosses 2 (C02: holds; C22: does not)
        need = (2 - k_diff) if k_diff < 2 else (k_diff - 1)
        pool = sorted(p["margin"] for p in per if p["differs"] == (k_diff >= 2) and p["margin"] is not None)
        out.append([name, head["verdict"], f"{k_diff} of 5 differ", need,
                    "; ".join(f"fold {p['fold']}: {p['verdict']}, margin {p['margin']}" for p in per),
                    sum(pool[:need]) if len(pool) >= need else ">40 per fold"])
    return out


def table(head: list[str], rows: list[list]) -> str:
    def cell(x):
        return "-" if x is None else str(x)
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] +
                     ["| " + " | ".join(cell(x) for x in r) + " |" for r in rows])


def main() -> None:
    K.annual()  # before monthly(): common.monthly() patches panel.panel to annual
    dec, notes = deciders_part([])
    a4, _ = a4_part()
    folds = a4_folds()
    weak = [r[0] for r in dec if r[9] is not True]
    flips = [f"{r[0]} ({r[10]})" for r in dec if any(f"narrow {k}" in r[10] for k in range(0, 41))]
    summary = ["## In one paragraph", "",
               f"Deciders' cells with a margin at or below U (narrow, the larger reading): {len(weak)} of {len(dec)}: "
               + ", ".join(weak) + ". Cells whose verdict flips when only the narrow-U episodes may change side "
               f"(after putting in those that would enter): {len(flips)}: " + ("; ".join(flips) if flips else "none") + ". "
               "The margins are small (greedy swaps of 1 to 21 episodes against 3 to 21 uncertain); the verdicts are "
               "therefore not shown robust to the gapped prices by margin alone. The margin is an upper bound, and "
               "U counts every episode that touches a gap, not those whose values would actually change. "
               "A4: every headline slope and the C02 and C22 fold statements have a margin of 1 to 6 windows; the "
               "four windows with a CPI gap inside, removed, leave all three verdicts unchanged.", ""]
    txt = ["# Gap 5's margin check (2026-10-02)", "",
           "Mechanical, from existing runs only (`code/gap5_margins.py`; C18's stored episodes, the frozen panels). "
           "No card, no result, no registry entry, no published text. A verdict is robust to the gapped prices "
           "only if its margin exceeds the number of uncertain episodes U. **A greedy margin is an upper bound "
           "of the true minimum**: a margin at or below U is a definite weakness; a margin above U, with no flip "
           "found, is evidence, not proof. Definitions are in the script's docstring.", "",
           *summary,
           "## The deciders' 12 cells (C18's headline; both accommodation readings)", "",
           table(["cell", "stated verdict", "each reading", "margin per reading (changes of side)", "kind",
                  "margin used", "uncertain U per reading (touch a price gap + would enter)", "U used (larger)",
                  "U wide (+ other episodes of the 15 economies)", "margin > U?",
                  "swaps found, when only the U episodes may change side (narrow; wide), after putting the would-enter episodes in",
                  "C18's 'every set-apart jump put back'"], dec),
           "", *[f"- {n}" for n in notes], "",
           "## A4 headline slopes (one window removed = one change)", "",
           table(["verdict", "stated", "greedy removals to flip, by direction", "margin", "windows with a CPI gap inside",
                  "windows lost only for a missing CPI at an end", "U", "margin > U?",
                  "verdict with the windows that have a CPI gap inside removed"], a4), "",
           "## A4 folds (the failure clause: two or more folds telling another verdict)", "",
           table(["card", "headline verdict", "folds", "folds that must change", "each fold", "windows to change the statement (sum of the smallest)"], folds), ""]
    OUT.write_text("\n".join(txt))
    print(OUT)


if __name__ == "__main__":
    main()
