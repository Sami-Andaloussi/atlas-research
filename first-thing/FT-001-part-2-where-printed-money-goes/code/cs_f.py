"""Card C33 (CS-F, C13's correction): the households' range per household with the savings moved into checkable
deposits measured against other deposits' own path, the baseline fixed on the card before the run.

From the study's folder: ``../../toolkit/bin/ftpy code/cs_f.py``. Writes ``results/runs/C33-cs-f-reclassification.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *C13's method in every part*: the households' range is recomputed with ``tax.py``'s own functions (``losses``,
  ``stock_at_month_start``), its months, prices, households and interest unchanged; only R changes. The parts that
  never touch R (the whole stock as a share of GDP, seigniorage, the base created, the base's place now) are carried
  from C13's stored run, named as carried: the reproduction below is what licenses it.
- *A quarter's change*: the quarter-end stock less the previous quarter-end's, in billions.
- *H.6's month of the move*: the month of M1's largest monthly rise inside the card's timing window.
- *Reproduction* (item 5): with R = 0 the run must give C13's stored upper and lower bounds per household to the
  dollar (C13 found no reclassification, so its lower bound also used R = 0); otherwise the run is void.
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
import tax as T  # noqa: E402

from ft import cards  # noqa: E402

CARD = K.CARDS / "C33-cs-f-reclassification.yaml"
C13 = K.RUNS / "C13-a6-checked.json"


def q_end(label: str) -> pd.Timestamp:
    return pd.Period(label, "Q").end_time.normalize()


def changes(stock: pd.Series) -> pd.Series:
    return stock.sort_index().diff()


def shortfall(other_change: pd.Series, quarters: list[str], at: str, cap: float) -> dict:
    mean = float(np.mean([other_change[q_end(q)] for q in quarters]))
    raw = mean - float(other_change[q_end(at)])
    return {"baseline_quarters": quarters, "baseline_mean_change_bn": mean,
            "change_at_move_bn": float(other_change[q_end(at)]), "raw_bn": raw,
            "R_bn": float(min(max(raw, 0.0), cap)), "floored": raw < 0, "capped": raw > cap}


def household_range(R: float, prm: dict) -> dict:
    """C13's households' range with the lower bound's stock less R from the move's quarter on."""
    start = pd.Period(prm["start"], "M")
    P = T.monthly_prices("CPIAUCSL", "2026-09-27")
    curr = K.fred_monthly("CURRSL")
    end = min(P.index.max(), curr.index.max())
    base = start  # C13's constant dollars are February 2020's
    months = pd.period_range(start + 1, end, freq="M")
    z1 = K.quarter_end_stock("BOGZ1FL193020005Q") / 1000
    hh_stock = T.stock_at_month_start(z1, months)
    move = q_end(prm["reclassification_quarter"])
    upper = T.losses(hh_stock, P, start, end, base)
    lower_stock = hh_stock.copy()
    for m in months:
        if m.start_time > move:
            lower_stock[m] = lower_stock[m] - R
    lower = T.losses(lower_stock, P, start, end, base)
    icndr = K.fred_monthly("ICNDR")
    interest = pd.Series({m: (lower.loc[m, "stock"] * icndr.get(m, np.nan) / 1200) if m in icndr.index else 0.0
                          for m in lower.index})
    interest_const = pd.Series({m: interest[m] * float(P[base]) / float(P[lower.loc[m, "from"]]) for m in lower.index})
    hh = K.fred_series("TTLHH")
    hh = pd.Series(hh.to_numpy(), index=hh.index.year)

    def per_household(frame: pd.DataFrame, col: str, less: pd.Series | None = None) -> float:
        tot = 0.0
        for m, row in frame.iterrows():
            n = hh.get(m.year, hh.iloc[-1]) * 1000
            tot += (row[col] - (0.0 if less is None else float(less.get(m, 0.0)))) * 1e9 / n
        return tot

    ph = {"upper_current": per_household(upper, "loss"), "upper_constant": per_household(upper, "loss_const"),
          "lower_current": per_household(lower, "loss", interest),
          "lower_constant": per_household(lower, "loss_const", interest_const)}
    return {"R_bn": R, "per_household": ph, "upper_total_bn": float(upper.loss.sum()),
            "lower_total_bn": float(lower.loss.sum() - interest.sum()), "interest_deducted_bn": float(interest.sum()),
            "range_ratio": ph["upper_current"] / ph["lower_current"] if ph["lower_current"] else None,
            "period": {"first_loss_month": str(months[0]), "last_month": str(end)}}


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm = card["parameters"]
    c13 = json.loads(C13.read_text())["result"]

    repro = household_range(0.0, prm)
    stored = c13["households"]["per_household"]
    diffs = {k: round(repro["per_household"][k] - stored[k], 6) for k in stored}
    if any(abs(v) >= 0.5 for v in diffs.values()):
        return cards.write_result(K.STUDY, CARD, {"void": True, "why": "C13 not reproduced with R = 0",
                                                  "differences_per_household": diffs})

    z1 = K.quarter_end_stock("BOGZ1FL193020005Q") / 1000
    other = K.quarter_end_stock("BOGZ1FL193030205Q") / 1000
    move = prm["reclassification_quarter"]
    cap = float(changes(z1)[q_end(move)])
    oc = changes(other)
    main_R = shortfall(oc, prm["baseline_quarters"], move, cap)
    beside_R = shortfall(oc, prm["baseline_beside_quarters"], move, cap)
    with_R = household_range(main_R["R_bn"], prm)
    beside = household_range(beside_R["R_bn"], prm)
    spread = {q: shortfall(oc, [q], move, cap)["R_bn"] for q in prm["baseline_quarters"]}

    window = pd.period_range(*[pd.Period(x, "M") for x in prm["monthly_timing_window"]], freq="M")
    timing = {}
    for s, v in (("M1SL", "2026-09-30"), ("M2SL", "2026-09-30"), ("SAVINGSL", "2026-10-08")):
        x = K.fred_monthly(s, v)
        timing[s] = {str(m): float(x[m]) for m in window if m in x.index}
        timing[s + "_last_month"] = str(x.index.max())
    m1 = pd.Series({pd.Period(k, "M"): v for k, v in timing["M1SL"].items()})
    jump = m1.diff().idxmax()
    timing["h6_move_month"] = {"month": str(jump), "m1_change_bn": float(m1.diff()[jump]),
                               "z1_households_quarter": move,
                               "note": "each source's date, never reconciled by us; the range uses Z.1's quarter"}
    quarters = [q for q in pd.period_range("2019Q1", "2021Q4", freq="Q")]
    path = {str(q): {"checkable_and_currency_bn": float(z1.get(q.end_time.normalize(), np.nan)),
                     "other_deposits_bn": float(other.get(q.end_time.normalize(), np.nan)),
                     "other_change_bn": float(oc.get(q.end_time.normalize(), np.nan))} for q in quarters}

    payload = {
        "void": False,
        "reproduction": {"R": 0.0, "differences_per_household_usd": diffs, "holds": True},
        "reclassification": {"main": main_R, "beside_2019": beside_R, "cap_rise_in_move_quarter_bn": cap,
                             "spread_each_surrounding_quarter_alone_bn": spread,
                             "words": "a shortfall read as the reclassification, never '$X moved'",
                             "z1_quarterly_path": path},
        "range": {"lower": with_R["per_household"]["lower_current"], "upper": with_R["per_household"]["upper_current"],
                  "lower_constant": with_R["per_household"]["lower_constant"],
                  "upper_constant": with_R["per_household"]["upper_constant"],
                  "more_than_twice": bool(with_R["per_household"]["upper_current"]
                                          > 2 * with_R["per_household"]["lower_current"]),
                  "detail": with_R},
        "beside_2019_baseline": beside,
        "monthly_timing_h6": timing,
        "carried_from_C13": {k: c13[k] for k in ("whole_stock", "seigniorage", "deferred_asset", "where_the_base_sits")},
        "words": "'tax' only for seigniorage on currency; the rest is what inflation took (card item 4)",
    }
    out = cards.write_result(K.STUDY, CARD, payload)
    print(out)
    return out


if __name__ == "__main__":
    main()
