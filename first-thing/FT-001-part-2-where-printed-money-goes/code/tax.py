"""What inflation took from US cash and from deposits that paid nothing since February 2020, and what the
base's growth created and the Federal Reserve earned or lost: card C13 (C08 checked).

From the study's folder: ``../../toolkit/bin/ftpy code/tax.py``. Writes
``results/runs/C13-a6-checked.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *Months*: the loss in month t runs from March 2020 (the stock held at the start of March, February's
  prices) to the last month with both the CPI and currency; the monthly stock of currency S(t-1) is the
  previous month's value (CURRSL, a monthly average); a quarterly stock is the last quarter-end at or before
  the first day of month t.
- *The CPI's missing month* (October 2025 in this vintage): the loss over the gap is taken once, in the
  month after it, on the stock at the gap's start, priced from the last month before the gap.
- *Constant dollars*: each month's loss times P(February 2020) / P(t-1).
- *Households*: TTLHH (thousands) in the month's calendar year; the last year's value for later months.
- *The reclassification test* reads Z.1's households' checkable deposits and currency and their other
  deposits at 2020Q3 and 2020Q4 (quarter-ends); R, when found, is subtracted from the lower bound's stock for
  the months whose stock is 2020Q4's or later.
- *Interest deducted* (the lower bound, from April 2021): the stock times ICNDR / 1200 in each month where
  ICNDR exists, in the same dollars as the loss.
- *Share of GDP*: a calendar year's loss over the mean of that year's quarters of GDP (the last year's
  quarters so far); the period's total over the sum, month by month, of the quarter's GDP over 12 (a month
  past the last published quarter takes that quarter's value).
- *The rule's start* (a variant): m0 of C15's headline US episode holding February 2020, else the nearest.
- *Remittances* (5c): the Board's January releases for 2020 to 2023, read and cited in
  `notes/fed-statements.md` before this part was written, enter the registry as cited numbers (never
  computed here); 2024 and 2025 were not found and are not reported; the deferred asset carries them.
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
import frame_e as F  # noqa: E402

from ft import cards  # noqa: E402

CARD = K.CARDS / "C13-a6-checked.yaml"
C15 = K.RUNS / "C15-e-episodes-closed.json"


def monthly_prices(series: str, vintage: str) -> pd.Series:
    return K.fred_monthly(series, vintage)


def stock_at_month_start(q: pd.Series, months: pd.PeriodIndex) -> pd.Series:
    """A quarter-end stock read at each month's first day: the last quarter-end at or before it."""
    out = []
    for m in months:
        s = q[q.index <= m.start_time]
        out.append(np.nan if not len(s) else float(s.iloc[-1]))
    return pd.Series(out, index=months)


def losses(stock_prev: pd.Series, P: pd.Series, start: pd.Period, end: pd.Period, base: pd.Period) -> pd.DataFrame:
    """Month by month from start + 1 to end: the loss on the stock held at the month's start
    (``stock_prev[t]``), in dollars of the month's start and in dollars of ``base``; a missing CPI month is
    bridged (the loss over the gap taken once, on the stock at its start)."""
    rows, prev = [], start
    for t in pd.period_range(start + 1, end, freq="M"):
        if t not in P.index or pd.isna(P.get(t)):
            continue  # a gap: its loss is taken in the next month with a price
        p0, p1 = float(P[prev]), float(P[t])
        s = stock_prev.get(prev + 1, np.nan) if prev + 1 != t else stock_prev.get(t, np.nan)
        loss = s * (1 - p0 / p1)
        rows.append({"month": t, "from": prev, "stock": s, "loss": loss, "loss_const": loss * float(P[base]) / p0})
        prev = t
    return pd.DataFrame(rows).set_index("month")


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm = card["parameters"]
    start = pd.Period(prm["start"], "M")
    base = pd.Period(prm["constant_dollars_of"], "M")
    P = monthly_prices("CPIAUCSL", "2026-09-27")
    P_nsa = monthly_prices("CPIAUCNS", "2026-09-30")
    curr = K.fred_monthly("CURRSL")
    currcir = K.fred_monthly("CURRCIR")
    end = min(P.index.max(), curr.index.max())
    missing = [str(m) for m in pd.period_range(start, end, freq="M") if m not in P.index]
    months = pd.period_range(start + 1, end, freq="M")

    # the stock held at each month's start: currency, last month's value; deposits, the last quarter-end
    cur_prev = pd.Series({m: curr.get(m - 1, np.nan) for m in months})
    cir_prev = pd.Series({m: currcir.get(m - 1, np.nan) for m in months})
    fdic = K.quarter_end_stock("QBPBSTLKDPDOFFDPNIDP") / 1000  # millions -> billions
    dep = stock_at_month_start(fdic, months)
    z1 = K.quarter_end_stock("BOGZ1FL193020005Q") / 1000
    other = K.quarter_end_stock("BOGZ1FL193030205Q") / 1000
    hh_stock = stock_at_month_start(z1, months)

    def run_whole(cur_series, prices, st):
        cash = losses(cur_series, prices, st, end, base)
        deposits = losses(dep, prices, st, end, base)
        return cash, deposits

    cash, deposits = run_whole(cur_prev, P, start)

    # reclassification test on Z.1 (2020Q3 -> 2020Q4)
    q3, q4 = pd.Timestamp("2020-09-30"), pd.Timestamp("2020-12-31")
    rise = float(z1[q4] - z1[q3])
    fall = float(other[q3] - other[q4])
    reclass = fall >= 0.5 * rise and rise > 0
    R = min(rise, fall) if reclass else 0.0
    upper = losses(hh_stock, P, start, end, base)
    lower_stock = hh_stock.copy()
    for m in months:
        if m.start_time > q4:  # the month's stock is 2020Q4's or later
            lower_stock[m] = lower_stock[m] - R
    lower = losses(lower_stock, P, start, end, base)
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
            val = row[col] - (0.0 if less is None else float(less.get(m, 0.0)))
            tot += val * 1e9 / n
        return tot

    ph = {"upper_current": per_household(upper, "loss"),
          "upper_constant": per_household(upper, "loss_const"),
          "lower_current": per_household(lower, "loss", interest),
          "lower_constant": per_household(lower, "loss_const", interest_const)}

    gdp_q = K.fred_series("GDP")
    gdp_q = pd.Series(gdp_q.to_numpy(), index=gdp_q.index.to_period("Q"))
    by_year = {}
    for y in sorted({m.year for m in cash.index}):
        g = gdp_q[gdp_q.index.year == y]
        tot = float(cash.loss[cash.index.year == y].sum() + deposits.loss[deposits.index.year == y].sum())
        by_year[str(y)] = {"loss_bn": tot, "gdp_bn": float(g.mean()), "share_pct": 100 * tot / float(g.mean()),
                           "quarters": int(len(g))}
    quarters = pd.period_range(gdp_q.index.min(), max(gdp_q.index.max(), cash.index.max().asfreq("Q")), freq="Q")
    gdp_filled = gdp_q.reindex(quarters).ffill()  # months past the last published quarter: its value
    period_gdp = float(sum(gdp_filled[m.asfreq("Q")] / 12 for m in cash.index))
    whole_total = float(cash.loss.sum() + deposits.loss.sum())
    whole_const = float(cash.loss_const.sum() + deposits.loss_const.sum())

    def whole_variant(cur_series, prices, st):
        c, d = run_whole(cur_series, prices, st)
        return {"total_bn": float(c.loss.sum() + d.loss.sum()), "cash_bn": float(c.loss.sum()),
                "deposits_bn": float(d.loss.sum()), "total_const_bn": float(c.loss_const.sum() + d.loss_const.sum())}

    c15 = json.loads(C15.read_text())["result"]
    us = [e for e in F.from_csv(c15["us_episodes"])]
    holding = [e for e in us if pd.Period(e["m0"], "M") <= start <= pd.Period(e["c"], "M")]
    near = holding[0] if holding else min(us, key=lambda e: abs((pd.Period(e["m0"], "M") - start).n))
    rule_start = pd.Period(near["m0"], "M")
    cur_prev_rule = pd.Series({m: curr.get(m - 1, np.nan) for m in pd.period_range(rule_start + 1, end, freq="M")})
    variants = {
        "CPI not seasonally adjusted": whole_variant(cur_prev, P_nsa, start),
        "currency in circulation (CURRCIR)": whole_variant(cir_prev, P, start),
    }
    c_rule = losses(cur_prev_rule, P, rule_start, end, base)
    dep_rule = stock_at_month_start(fdic, pd.period_range(rule_start + 1, end, freq="M"))
    d_rule = losses(dep_rule, P, rule_start, end, base)
    variants[f"start at the rule's m0 ({rule_start})"] = {"total_bn": float(c_rule.loss.sum() + d_rule.loss.sum())}

    # seigniorage and what the Fed earned or lost
    mbc = K.fred_monthly("MBCURRCIR")
    bog = K.fred_monthly("BOGMBASE")
    seign = {}
    for y in range(2020, 2026):
        d0, d1 = pd.Period(f"{y - 1}-12", "M"), pd.Period(f"{y}-12", "M")
        g = float(gdp_q[gdp_q.index.year == y].mean())
        seign[str(y)] = {"currency_rise_bn": float(mbc[d1] - mbc[d0]), "currency_share_pct": 100 * float(mbc[d1] - mbc[d0]) / g,
                         "base_rise_bn": float(bog[d1] - bog[d0]), "base_share_pct": 100 * float(bog[d1] - bog[d0]) / g}
    bog_last = bog.index.max()
    base_created = {"from": str(start), "to": str(bog_last), "bn": float(bog[bog_last] - bog[start]),
                    "level_start_bn": float(bog[start]), "level_last_bn": float(bog[bog_last])}
    rem = K.fred_series("RESPPLLOPNWW")
    deferred = {"lowest_mn": float(rem.min()), "lowest_date": str(rem.idxmin().date()),
                "latest_mn": float(rem.iloc[-1]), "latest_date": str(rem.index[-1].date()),
                "first_negative": str(rem[rem < 0].index.min().date()) if (rem < 0).any() else None}
    res_bal = K.fred_series("WRESBAL")
    cur_cir = K.fred_series("WCURCIR")
    last_week = min(res_bal.index.max(), cur_cir.index.max())
    rb, cc = float(res_bal[last_week]), float(cur_cir[last_week])
    where = {"week": str(last_week.date()), "reserves_bn": rb, "currency_bn": cc,
             "reserves_share_pct": 100 * rb / (rb + cc), "currency_share_pct": 100 * cc / (rb + cc)}

    payload = {
        "period": {"first_loss_month": str(months[0]), "last_month": str(end), "cpi_missing": missing},
        "whole_stock": {"total_bn": whole_total, "total_const_bn": whole_const,
                        "cash_bn": float(cash.loss.sum()), "deposits_bn": float(deposits.loss.sum()),
                        "cash_const_bn": float(cash.loss_const.sum()), "deposits_const_bn": float(deposits.loss_const.sum()),
                        "period_gdp_bn": period_gdp, "share_of_period_gdp_pct": 100 * whole_total / period_gdp,
                        "by_year": by_year,
                        "stock_start_bn": {"cash": float(curr[start]), "deposits": float(dep.iloc[0])},
                        "stock_last_bn": {"cash": float(curr[end]), "deposits": float(dep.iloc[-1])}},
        "households": {"reclassification": {"rise_bn": rise, "other_fall_bn": fall, "found": reclass, "R_bn": R},
                       "per_household": ph,
                       "upper_total_bn": float(upper.loss.sum()), "lower_total_bn": float(lower.loss.sum() - interest.sum()),
                       "interest_deducted_bn": float(interest.sum()),
                       "households_first_year": float(hh.get(2020)), "households_last": float(hh.iloc[-1]),
                       "households_last_year": int(hh.index[-1]),
                       "range_ratio": ph["upper_current"] / ph["lower_current"] if ph["lower_current"] else None,
                       "stock_2020Q3_bn": float(z1[q3]), "stock_2020Q4_bn": float(z1[q4])},
        "variants": variants,
        "seigniorage": {"by_year": seign, "base_created": base_created,
                        "remittances": "cited from the Board's releases for 2020-2023 (notes/fed-statements.md); 2024-2025 not found"},
        "deferred_asset": deferred,
        "where_the_base_sits": where,
    }
    out = cards.write_result(K.STUDY, CARD, payload)
    print(out)
    return out


if __name__ == "__main__":
    main()
