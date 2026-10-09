"""Card C20 (CS-B corrected, C19's child): C19's gap with the economy-years above 100% a year set apart and named;
the gap of medians and of mean log rates beside.

From the study's folder: ``../../toolkit/bin/ftpy code/cs_b_trim.py``. Writes
``results/runs/C20-cs-b-without-hyperinflation-years.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *C19's machinery*: ``cs_b.panel``, ``cs_b.describe``, ``cs_b.interval`` and ``cs_b.reading``, with C19's parameters
  read from C19's card; nothing re-implemented but the medians' bootstrap and the log rates.
- *The medians' bootstrap*: the same year weights as C19's moving blocks (the same seed, so the same draws); each
  draw's class median over its economy-years repeated by their year's weight.
- *The log rate*: ``100 * ln(1 + pi / 100)`` from C19's simple rate, which is ``100 * ln(CPI_t / CPI_t-1)``.
- *Fiat from 1972*: C19's filter (every class but fiat, and fiat from 1972) on the years kept.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cs_b as B  # noqa: E402

from ft import cards  # noqa: E402

CARD = B.STUDY / "cards" / "C20-cs-b-without-hyperinflation-years.yaml"


def weights(prm: dict, blocks: bool = True):
    """C19's year weights, draw by draw (the same generator and order as ``cs_b.interval``)."""
    y0, y1 = prm["years"]
    n, L = y1 - y0 + 1, prm["block_years"]
    rng = np.random.default_rng(prm["seed"])
    for _ in range(prm["draws"]):
        w = np.zeros(n)
        if blocks:
            filled = 0
            while filled < n:
                s = rng.integers(0, n - L + 1)
                take = min(L, n - filled)
                w[s:s + take] += 1
                filled += take
        else:
            np.add.at(w, rng.integers(0, n, size=n), 1)
        yield w


def median_gap(d, prm: dict) -> dict:
    y0 = prm["years"][0]
    conv, fiat = d[d["class"] == "convertible"], d[d["class"] == "fiat"]
    gaps, empty = [], 0
    for w in weights(prm):
        meds = []
        for g in (conv, fiat):
            k = w[(g.year - y0).to_numpy()].astype(int)
            v = np.repeat(g.pi.to_numpy(), k)
            meds.append(np.median(v) if len(v) else np.nan)
        if np.isnan(meds).any():
            empty += 1
            continue
        gaps.append(meds[1] - meds[0])
    lo, hi = (float(x) for x in np.percentile(gaps, [2.5, 97.5]))
    return {"gap": float(fiat.pi.median() - conv.pi.median()), "interval": [lo, hi], "draws_left_out": empty}


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    mt = card["matters"]
    prm = yaml.safe_load(B.CARD.read_text())["parameters"]
    cut = card["parameters"]["set_apart_above"]
    d, unclassed = B.panel(prm)
    apart = d[d.pi > cut]
    named = [{"iso": r.iso, "year": int(r.year), "class": r["class"], "inflation_pct": float(r.pi)}
             for _, r in apart.sort_values(["iso", "year"]).iterrows()]
    cf = apart[apart["class"].isin(["convertible", "fiat"])]["class"].value_counts().to_dict()
    if cf != {"fiat": 3, "convertible": 1}:
        return cards.write_result(B.STUDY, CARD, {"void": True, "why": f"set-apart years {cf}, not C19's four",
                                                  "named": named})
    keep = d[d.pi <= cut]
    out = {"void": False, "set_apart": named, "economy_years": int(len(keep)),
           "by_class": {c: B.describe(keep[keep["class"] == c].pi) for c in ("convertible", "fiat", "war",
                                                                            "bretton_woods")},
           "main": B.read(keep, prm, mt["cs_b_gap_set_apart"])}
    med = median_gap(d, prm)
    out["median_gap"] = {**med, "reading": B.reading(*med["interval"], mt["cs_b_median_gap"])}
    logd = d.assign(pi=100 * np.log1p(d.pi / 100))
    out["log_rates"] = B.read(logd, prm, mt["cs_b_log_gap"])
    out["log_rates_set_apart"] = B.read(logd[d.pi <= cut], prm, mt["cs_b_log_gap_set_apart"])
    out["fiat_from_1972"] = B.read(keep[(keep["class"] != "fiat") | (keep.year >= 1972)], prm,
                                   mt["cs_b_gap_set_apart_from_1972"])
    trans = keep["flags"].apply(lambda f: "transition year" in f)
    out["no_transition_years"] = B.read(keep[~trans], prm, mt["cs_b_gap_set_apart_no_transition"])
    own = keep["flags"].apply(lambda f: "return printed in another block (rule e)" in f)
    out["own_block_returns_only"] = B.read(keep[~own], prm, mt["cs_b_gap_set_apart_own_block_returns"])
    d_e, _ = B.panel(prm, earlier=True)
    out["earlier_resumption"] = B.read(d_e[d_e.pi <= cut], prm, mt["cs_b_gap_set_apart_earlier_resumption"])
    d_m, _ = B.panel(prm, marked_inconvertible=True)
    out["marked_suspensions_inconvertible"] = B.read(d_m[d_m.pi <= cut], prm,
                                                     mt["cs_b_gap_set_apart_marked_suspensions"])
    out["fiat_from_1972_years_above"] = int(((d["class"] == "fiat") & (d.year >= 1972) & (d.pi > cut)).sum())
    out["eras"] = {f"{a}-{b}": {c: B.describe(keep[(keep.year >= a) & (keep.year <= b) & (keep["class"] == c)].pi)
                                for c in ("convertible", "fiat", "bretton_woods")} for a, b in prm["eras"]}
    nw = keep[keep["class"] != "war"].dropna(subset=["peg"])
    out["jst_peg_beside"] = {"peg_1": B.describe(nw[nw.peg == 1].pi), "peg_0": B.describe(nw[nw.peg == 0].pi)}
    out["said"] = ("the threshold is C19's, fixed before its run; setting those years apart was chosen after C19's "
                   "mean was seen (P12); the medians keep every year and need no threshold; the log rates are printed "
                   "with and without the years set apart, and Germany's 1923 still weighs about 2,000 log points")
    path = cards.write_result(B.STUDY, CARD, out)
    print(path)
    return path


if __name__ == "__main__":
    main()
