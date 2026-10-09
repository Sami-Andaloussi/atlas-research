"""Card C32 (CS-C, C01's correction): the two American printings month by month, on one balance-sheet item, beside
Blanchard & Bernanke's decomposition as theirs.

From the study's folder: ``../../toolkit/bin/ftpy code/cs_c.py``. Writes ``results/runs/C32-cs-c-door-timeline.json``,
whose ``timeline`` and ``decomposition`` blocks are the figure's data (the figure is drawn at step e, never here).

Readings of the card that its text leaves to the code, fixed here before the run:

- *Units*: FRED publishes WRESBAL, WCURCIR, WALCL, TREAST, WSHOMCB, WLRRAL and FYFSD in millions of dollars, BOGMBASE,
  M2SL and GDP in billions (the card's item 0); everything is printed in billions. A units guard refuses the run if WALCL's first month is
  not between $0.5tn and $1.5tn in millions (a check on the scale, read before any window).
- *A weekly series by month*: the mean of the month's weeks (the card's "monthly averages").
- *Added over a window*: the window's last month less its first (C01's convention for the base).
- *The deficits a window covers*: FYFSD is dated at the fiscal year's end (30 September); fiscal year Y runs October
  Y-1 to September Y; a deficit is -FYFSD. The share that must reproduce is on the card's whole fiscal years; beside
  it, the months-weighted share (the window's months are its changes' months, the month after its first to its last,
  C01's n; each fiscal year weighted by the share of its twelve months among them).
- *Nominal GDP growth and velocity*: quarterly, four-quarter growth for GDP; M2V as published (a level).
- *Twelve-month rates*: ``common.yoy`` (percent change over twelve months on a full calendar of months).
- *The decomposition*: the authors' sheets as their figure code reads them (``code/Python/figure_12_13_decomposition.py``):
  each shock's ``contr_gcpi`` from ``wo_residuals_vu``, ``_grpe``, ``_grpf`` and ``_shortage``; initial conditions,
  ``wo_residuals_grpe_grpf_vu_shor``'s ``gcpi_simul``; their actual line, ``wo_residuals_no_shocks_removed``'s ``gcpi``.
  Their periods are Excel day serials (1899-12-30 origin). Only the package's public paths are opened; never
  ``input_data/confidential/``.
- *v/u*: the authors' ``InfoData.xlsx``, sheet ``VOVERU`` (quarterly), over the whole timeline (panel f).
- *Annotations*: the card's, and nothing else: none on 2008-14; the 2022 acts only in the stretch block.
- *Reproduction* (item 7): each target compared to the rounding printed (billions to the nearest billion, shares to
  the percent); a difference is reported, never forced.
"""

from __future__ import annotations

import sys
import tempfile
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import xls_read as XLS  # noqa: E402
import xlsx_read as XLSX  # noqa: E402

from ft import cards  # noqa: E402
from ft.data import freeze  # noqa: E402

CARD = K.CARDS / "C32-cs-c-door-timeline.yaml"
BB = ("brookings/blanchard-bernanke-2023-replication", "2026-10-08")
BB_ROOT = "replication_06.13.2023/data/"
DECOMP = BB_ROOT + "output_data/all_data_decompositions.xls"
INFODATA = BB_ROOT + "input_data/public/InfoData.xlsx"
MILLIONS = {"WRESBAL", "WCURCIR", "WALCL", "TREAST", "WSHOMCB", "WLRRAL", "FYFSD"}
VINTAGE = {"WLRRAL": "2026-10-08", "UNRATE": "2026-10-08", "CPIAUCSL": "2026-09-27"}
TARGETS = {"W1": {"base_added_bn": 3154, "reserves_share_pct": 86, "walcl_added_bn": 3563,
                  "purchases_share_fiscal_years_pct": 32},
           "W2": {"base_added_bn": 2959, "reserves_share_pct": 87, "walcl_added_bn": 4554,
                  "purchases_share_fiscal_years_pct": 54}}
SHOCKS = {"v/u": "wo_residuals_vu", "energy": "wo_residuals_grpe", "food": "wo_residuals_grpf",
          "shortages": "wo_residuals_shortage"}
ANNOTATIONS = {
    "W1": [],
    "W2": [("2020-03", "the lockdown orders and the CARES Act"),
           ("2021-03", "the American Rescue Plan")],
    "stretch": [("2022-02", "Russia's invasion of Ukraine (24 February 2022)"),
                ("2022-03", "the Fed's first rise (FOMC statement, 16 March 2022)")],
}


CAPTION = ("Blanchard & Bernanke's decomposition, as theirs: their model has no money variable; demand from fiscal and "
           "monetary policy enters through v/u and, in their reading, through the price shocks themselves (p. 39). BIS 67 "
           "weighs the money more; Barro & Bianchi find the fiscal surge a key driver of inflation across OECD countries, an "
           "estimated four-fifths of it paid for by inflation eroding the public debt (K5).")


def series(code: str) -> pd.Series:
    """A FRED series in billions, by month (weekly and daily series averaged over the month)."""
    x = K.fred_monthly(code, VINTAGE.get(code, "2026-09-30"))
    return x / 1000 if code in MILLIONS else x


def fiscal_deficits() -> pd.Series:
    x = K.fred_series("FYFSD")
    return pd.Series(-x.to_numpy() / 1000, index=x.index.year)


def deficit_over(s: pd.Period, e: pd.Period, deficits: pd.Series) -> dict:
    months = pd.period_range(s + 1, e, freq="M")
    fy = pd.Series([m.year + (1 if m.month >= 10 else 0) for m in months]).value_counts().sort_index()
    weights = {int(y): n / 12 for y, n in fy.items()}
    missing = [y for y in weights if y not in deficits.index]
    total = float(sum(deficits[y] * w for y, w in weights.items() if y in deficits.index))
    return {"fiscal_year_weights": weights, "weighted_deficits_bn": total, "missing_fiscal_years": missing}


def window(name: str, s: pd.Period, e: pd.Period, S: dict, deficits: pd.Series, fiscal: list[int],
           before: int) -> dict:
    def added(code: str) -> float:
        return float(S[code][e] - S[code][s])

    out = {"start": str(s), "end": str(e), "months": (e - s).n,
           "base_added_bn": added("BOGMBASE"), "reserves_added_bn": added("WRESBAL"),
           "currency_added_bn": added("WCURCIR"), "walcl_added_bn": added("WALCL"),
           "treasuries_and_mbs_added_bn": added("TREAST") + added("WSHOMCB"), "treasuries_added_bn": added("TREAST"),
           "mbs_added_bn": added("WSHOMCB")}
    out["reserves_share_pct"] = 100 * out["reserves_added_bn"] / out["base_added_bn"]
    out["currency_share_pct"] = 100 * out["currency_added_bn"] / out["base_added_bn"]
    if name == "W2":
        out["reverse_repo_added_bn"] = added("WLRRAL")
    years = list(range(fiscal[0], fiscal[1] + 1))
    whole = float(sum(deficits[y] for y in years))
    out["deficits_fiscal_years"] = {"years": years, "sum_bn": whole}
    out["purchases_share_fiscal_years_pct"] = 100 * out["treasuries_added_bn"] / whole
    d = deficit_over(s, e, deficits)
    out["deficits_months_weighted"] = d
    out["purchases_share_months_weighted_pct"] = 100 * out["treasuries_added_bn"] / d["weighted_deficits_bn"]
    m2 = S["M2SL"]
    n = (e - s).n
    out["m2_pace_pa"] = 100 * ((m2[e] / m2[s]) ** (12 / n) - 1)
    out["m2_pace_before_pa"] = 100 * ((m2[s] / m2[s - before]) ** (12 / before) - 1)
    out["m2_before_months"] = before
    return out


def excel_date(serial: float) -> pd.Period:
    return pd.Period(datetime(1899, 12, 30) + timedelta(days=float(serial)), "Q")


def decomposition(zf: zipfile.ZipFile, start: pd.Period) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "all_data_decompositions.xls"
        path.write_bytes(zf.read(DECOMP))

        def column(sheet: str, col: str) -> pd.Series:
            rows = XLS.rows(path, sheet)
            head = rows[0]
            i, p = head.index(col), head.index("period")
            return pd.Series({excel_date(r[p]): float(r[i]) for r in rows[1:] if r[p] is not None and r[i] is not None})

        parts = {k: column(sheet, "contr_gcpi") for k, sheet in SHOCKS.items()}
        parts["initial conditions"] = column("wo_residuals_grpe_grpf_vu_shor", "gcpi_simul")
        actual = column("wo_residuals_no_shocks_removed", "gcpi")
    quarters = [q for q in actual.index if q >= start]
    rows = {str(q): {**{k: float(v[q]) for k, v in parts.items()}, "actual": float(actual[q])} for q in quarters}
    for r in rows.values():
        r["sum_of_bars"] = sum(r[k] for k in parts)
    return {"measure": "CPI inflation, annualised quarterly log change (theirs)", "quarters": rows,
            "first": str(quarters[0]), "last": str(quarters[-1]),
            "max_gap_bars_vs_actual": max(abs(r["sum_of_bars"] - r["actual"]) for r in rows.values())}


def v_over_u(zf: zipfile.ZipFile) -> pd.Series:
    book = XLSX.Book(zf.read(INFODATA))
    rows = book.rows("VOVERU")
    out = {}
    for r in rows.values():
        d, v = r.get(1), r.get(2)
        if isinstance(d, float) and isinstance(v, float):
            out[excel_date(d)] = v
    return pd.Series(out).sort_index()


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm = card["parameters"]
    if " ".join(CAPTION.split()) not in " ".join(card["method"].replace("''", "'").split()):
        raise SystemExit("the caption differs from the card's")
    codes = ["BOGMBASE", "WRESBAL", "WCURCIR", "WALCL", "TREAST", "WSHOMCB", "WLRRAL", "M2SL", "CPIAUCSL", "UNRATE"]
    S = {c: series(c) for c in codes}
    first = S["WALCL"].iloc[0] * 1000
    if not 5e5 <= first <= 1.5e6:
        raise SystemExit(f"units guard: WALCL's first month reads {first:.0f} millions")
    if not 1 <= S["WRESBAL"].iloc[0] <= 100:  # reserves in late 2002, about $10bn: a check on the scale only
        raise SystemExit(f"units guard: WRESBAL's first month reads {S['WRESBAL'].iloc[0]:.1f} billions")
    deficits = fiscal_deficits()

    windows = {}
    for name, (s, e) in prm["windows"].items():
        windows[name] = window(name, pd.Period(str(s), "M"), pd.Period(str(e), "M"), S, deficits,
                               prm["fiscal_years"][name], prm["m2_before_months"])

    repro = {}
    for name, t in TARGETS.items():
        for k, v in t.items():
            got = windows[name][k]
            repro[f"{name} {k}"] = {"audits": v, "run": round(got, 2), "matches": bool(round(got) == v)}

    t0, t1 = (pd.Period(str(x), "M") for x in prm["timeline"])
    x0, x1 = (pd.Period(str(x), "M") for x in prm["stretch"])
    m2_yoy, cpi_yoy = K.yoy(S["M2SL"]), K.yoy(S["CPIAUCSL"])

    def monthly(a: pd.Period, b: pd.Period) -> dict:
        return {str(m): {"base_bn": float(S["BOGMBASE"].get(m, np.nan)), "reserves_bn": float(S["WRESBAL"].get(m, np.nan)),
                         "currency_bn": float(S["WCURCIR"].get(m, np.nan)), "m2_yoy_pct": float(m2_yoy.get(m, np.nan)),
                         "cpi_yoy_pct": float(cpi_yoy.get(m, np.nan)), "unrate_pct": float(S["UNRATE"].get(m, np.nan))}
                for m in pd.period_range(a, b, freq="M")}

    gdp = K.fred_series("GDP")
    gdp = pd.Series(gdp.to_numpy(), index=gdp.index.to_period("Q"))
    m2v = K.fred_series("M2V")
    m2v = pd.Series(m2v.to_numpy(), index=m2v.index.to_period("Q"))
    gdp_g = 100 * (gdp / gdp.shift(4) - 1)
    zf = zipfile.ZipFile(freeze.load(*BB).path("PIIE-replication-package_6.13.zip"))
    vu = v_over_u(zf)

    def quarterly(a: pd.Period, b: pd.Period) -> dict:
        return {str(q): {"m2v": float(m2v.get(q, np.nan)), "ngdp_4q_growth_pct": float(gdp_g.get(q, np.nan)),
                         "v_over_u": float(vu.get(q, np.nan))}
                for q in pd.period_range(a.asfreq("Q"), b.asfreq("Q"), freq="Q")}

    m = lambda s: pd.Period(s, "M")  # noqa: E731
    q = lambda s: pd.Period(s, "Q")  # noqa: E731
    facts = {
        "m2_feb_to_may_2020_pct": 100 * float(S["M2SL"][m("2020-05")] / S["M2SL"][m("2020-02")] - 1),
        "m2_feb_to_may_2020_bn": float(S["M2SL"][m("2020-05")] - S["M2SL"][m("2020-02")]),
        "m2v_2020Q1": float(m2v[q("2020Q1")]), "m2v_2020Q2": float(m2v[q("2020Q2")]),
        "m2_growth_2021_dec_dec_pct": 100 * float(S["M2SL"][m("2021-12")] / S["M2SL"][m("2020-12")] - 1),
        "m2v_2020Q4": float(m2v[q("2020Q4")]), "m2v_2021Q4": float(m2v[q("2021Q4")]),
        "ngdp_growth_2021_q4_q4_pct": float(gdp_g[q("2021Q4")]),
        "unrate": {d: float(S["UNRATE"][m(d)]) for d in ("2009-02", "2009-10", "2012-08", "2012-09", "2020-04",
                                                         "2020-06", "2020-12", "2021-01", "2021-12")},
        "unrate_above_8_from_to": [str(x) for x in (lambda u: [u.index.min(), u.index.max()])(
            S["UNRATE"][(S["UNRATE"] > 8) & (S["UNRATE"].index >= m("2008-08")) & (S["UNRATE"].index <= m("2014-10"))])],
        "unrate_peak_W1": float(S["UNRATE"][m("2008-08"):m("2014-10")].max()),
    }

    payload = {
        "units": "billions of dollars; rates in percent",
        "windows": windows,
        "reproduction": {"targets": repro, "all_match": all(r["matches"] for r in repro.values())},
        "timeline": {"monthly": monthly(t0, t1), "quarterly": quarterly(t0, t1)},
        "stretch": {"monthly": monthly(x0, x1), "quarterly": quarterly(x0, x1),
                    "note": "drawn on the web study's door figure only (the card); the decomposition and v/u end in 2023Q1"},
        "decomposition": decomposition(zf, pd.Period(str(prm["decomposition_from"]), "Q")),
        "authors_figure_starts": "2019Q4 (code/Python/figure_12_13_decomposition.py); this card draws from 2020Q1, said",
        "identity": "M2V is GDP over M2: velocity, nominal GDP and M2 are one fact, never three corroborations",
        "annotations": {k: [{"month": a, "label": b} for a, b in v] for k, v in ANNOTATIONS.items()},
        "facts": facts,
        "lag": "in moderate inflations, monetary policy's peak effect on prices has come more than a year later "
               "(Batini & Nelson 2002, pp. 1-2; p. 7, no stand on money's special role)",
        "caption": CAPTION,
    }
    out = cards.write_result(K.STUDY, CARD, payload)
    print(out)
    return out


if __name__ == "__main__":
    main()
