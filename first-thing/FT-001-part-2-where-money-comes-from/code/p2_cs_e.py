"""Card C36 (CS-E): where the real change in US households' net worth came from, 1952Q1 to 2025Q4, quarter by quarter
(the Fed's Z.1, table S1M.r), with the euro area's households beside (the ECB's quarterly sector accounts).

From the study's folder: ``python code/p2_cs_e.py``. Writes ``results/runs/C36-cs-e-household-real-wealth.json``.

Real terms, each quarter: a series' real holding gain is its revaluation less the quarter's CPI-U inflation times its level
at the end of the previous quarter; other nominal assets (net worth less the partition's levels plus liabilities) lose the
quarter's inflation, liabilities gain it; net investment and other volume changes are the Fed's lines. The parts sum to
the real change in net worth exactly, but for the partition's gap, a row of its own.
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import pandas as pd

from ft import cards
from ft.data import fred
from ft.data import agency
from ft.data import freeze as F

STUDY = Path(__file__).resolve().parents[1]
CARD = STUDY / "cards" / "C36-cs-e-household-real-wealth.yaml"
LINE12 = ["FR155035005", "FR165015205", "FR165013765", "FR155111005"]
LINE17 = ["FR154022005", "FR153064105", "FR152090205", "FR153094305", "FR153064205", "FR153064705", "FR153064505",
          "FR153052005", "FR154000005"]
US_EQUITY = ["FR153064105", "FR152090205", "FR153094305"]  # lines 19-21
US_FUNDS = ["FR153064205", "FR153064705", "FR153064505"]  # lines 22-24
ROWS = ["real_and_market_priced", "fund_and_pension", "nominal_claims", "net_investment",
        "erosion_of_other_nominal_assets", "gain_on_liabilities", "other_volume", "partition_gap"]


def z1_series(vintage: str) -> dict[str, pd.Series]:
    """The card's tables' quarterly series (S1M.r for the flows; S1M.b and S1M.i.q for the levels and the two IMA
    revaluations), each code from the first of them in the release's file list that holds it."""
    fz = F.load("federalreserve/z1-csv", vintage)
    z = zipfile.ZipFile(io.BytesIO(fz.read_bytes("z1_csv_files.zip")))
    out: dict[str, pd.Series] = {}
    for name in z.namelist():
        if name not in ("csv/S1M_r.csv", "csv/S1M_b.csv", "csv/S1M_i_q.csv"):
            continue
        df = pd.read_csv(io.BytesIO(z.read(name)), dtype=str)
        df = df[df["date"].str.contains(":Q")]
        for col in df.columns[1:]:
            code = col.split(".")[0]
            if code not in out:
                out[code] = pd.Series(pd.to_numeric(df[col].str.strip(), errors="coerce").values, index=df["date"].values)
    return out


def level_code(fr: str, series: dict) -> str:
    lm, fl = "LM" + fr[2:], "FL" + fr[2:]
    if lm in series:
        return lm
    if fl in series:
        return fl
    raise SystemExit(f"C36: no level series for {fr}")


def quarter_end_month(q: str) -> str:
    y, n = q.split(":Q")
    return f"{y}-{int(n) * 3:02d}"


def prev_q(q: str) -> str:
    y, n = int(q[:4]), int(q[-1])
    return f"{y - 1}:Q4" if n == 1 else f"{y}:Q{n - 1}"


def decade(y: int) -> str:
    if y < 1960:
        return "1952-59"
    if y >= 2020:
        return "2020-25"
    return f"{y // 10 * 10}-{y % 100 // 10}9"


def main() -> dict:
    card = cards.read(CARD)
    cards.require_locked(CARD)
    p = card["parameters"]
    s = z1_series("2026-10-10")
    groups = p["groups"]
    partition = [c for g in groups.values() for c in g]
    if sorted(partition) != sorted(set(partition)) or sorted(partition) != sorted(LINE12 + LINE17):
        raise SystemExit("C36: the partition does not place lines 13-16 and 18-24 plus the two IMA lines once each")
    levels = {c: level_code(c, s) for c in partition}
    cpi = agency.series("CPIAUCSL", "2026-09-27")
    cpi.index = pd.to_datetime(cpi.index).strftime("%Y-%m")
    base = float(cpi["2025-12"])
    nw, liab = s[p["levels"]["net_worth"]], s[p["levels"]["liabilities"]]
    f = p["flows"]
    quarters = [q for q in s[f["change"]].index if "1952:Q1" <= q <= "2025:Q4"]
    rows: dict[str, dict[str, float]] = {}
    gaps, failures = [], []
    for q in quarters:
        q0 = prev_q(q)
        pi = float(cpi[quarter_end_month(q)]) / float(cpi[quarter_end_month(q0)]) - 1
        k = base / float(cpi[quarter_end_month(q)])
        real = {c: float(s[c][q]) - pi * float(s[levels[c]][q0]) for c in partition}
        part_levels = sum(float(s[levels[c]][q0]) for c in partition)
        ona = float(nw[q0]) - part_levels + float(liab[q0])
        gap12 = float(s["FR152010005"][q]) - sum(float(s[c][q]) for c in LINE12)
        gap17 = float(s["FR154090005"][q]) - sum(float(s[c][q]) for c in LINE17)
        gap = float(s[f["revaluation"]][q]) - sum(float(s[c][q]) for c in partition)
        if abs(gap12) > 0.5 * len(LINE12) or abs(gap17) > 0.5 * len(LINE17):
            gaps.append({"quarter": q, "line12_gap": gap12, "line17_gap": gap17})
            if max(abs(gap12), abs(gap17)) > 0.001 * abs(float(s[f["revaluation"]][q])):
                failures.append(q)
        r = {g: sum(real[c] for c in cs) for g, cs in groups.items()}
        r["net_investment"] = float(s[f["net_investment"]][q])
        r["erosion_of_other_nominal_assets"] = -pi * ona
        r["gain_on_liabilities"] = pi * float(liab[q0])
        r["other_volume"] = float(s[f["other_volume"]][q])
        r["partition_gap"] = gap
        real_change = float(s[f["change"]][q]) - pi * float(nw[q0])
        # line 1 = lines 2 + 11 + 28 holds to the release's integer millions (within 1 million in every quarter): the
        # parts may differ from the real change by the three lines' rounding, 1.5 million, no more
        if abs(sum(r.values()) - real_change) > 1.5:
            raise SystemExit(f"C36: {q}'s parts do not sum to its real change")
        rows[q] = {key: v * k for key, v in r.items()} | {"real_change": real_change * k}
    if failures:
        raise SystemExit(f"C36: the partition's gap passes 0.1% of line 11 in {failures}")

    def total(qs: list[str]) -> dict:
        t = {key: sum(rows[q][key] for q in qs) / 1e6 for key in ROWS + ["real_change"]}  # trillions of Dec-2025 dollars
        t = {key: round(v, 3) for key, v in t.items()}
        if t["real_change"] > 0:
            t["shares_pct"] = {key: round(100 * t[key] / t["real_change"], 1) for key in ROWS}
        return t

    spans = {"1952-2025": total(quarters)}
    for d in sorted({decade(int(q[:4])) for q in quarters}):
        spans[d] = total([q for q in quarters if decade(int(q[:4])) == d])
    payload = {"unit": "trillions of December 2025 dollars", "spans": spans, "quarters": len(quarters),
               "levels": levels, "partition_gap_quarters": gaps, "euro_area_beside": euro_beside(s, levels)}
    cards.write_result(STUDY, CARD, payload)
    return payload


def ecb_series(name: str) -> pd.Series:
    fz = F.load("ecb/qsa-households-revaluations", "2026-10-10")
    df = pd.read_csv(io.BytesIO(fz.read_bytes(name)), dtype=str)
    return pd.Series(pd.to_numeric(df["OBS_VALUE"]).values, index=df["TIME_PERIOD"].values).dropna()


def yearly_real_share(gain: dict[str, float], level: dict[str, float], pi: dict[str, float], years) -> dict:
    """Each year's real holding gains (the sum of its quarters') as a share of the level at the start of the year."""
    out = {}
    for y in years:
        qs = [f"{y}:Q{n}" for n in range(1, 5)]
        start = level[f"{y - 1}:Q4"]
        real = sum(gain[q] - pi[q] * level[prev_q(q)] for q in qs)
        out[str(y)] = round(100 * real / start, 1)
    return out


def euro_beside(s: dict, levels: dict) -> dict:
    hicp = ecb_series("hicp-index.csv")
    cpi = agency.series("CPIAUCSL", "2026-09-27")
    cpi.index = pd.to_datetime(cpi.index).strftime("%Y-%m")
    years = range(2013, 2026)
    qs = [f"{y}:Q{n}" for y in years for n in range(1, 5)]
    pi_ea = {q: float(hicp[quarter_end_month(q)]) / float(hicp[quarter_end_month(prev_q(q))]) - 1 for q in qs}
    pi_us = {q: float(cpi[quarter_end_month(q)]) / float(cpi[quarter_end_month(prev_q(q))]) - 1 for q in qs}
    ecbq = lambda ser: {k.replace("-Q", ":Q"): v for k, v in ser.items()}  # noqa: E731
    out = {}
    for name, codes in (("F51", US_EQUITY), ("F52", US_FUNDS)):
        k7, le = ecbq(ecb_series(f"qsa-K7-{name}.csv")), ecbq(ecb_series(f"qsa-LE-{name}.csv"))
        gain_us = {q: sum(float(s[c][q]) for c in codes) for q in qs}
        lvl_us = {q: sum(float(s[levels[c]][q]) for c in codes) for q in set(qs) | {prev_q(q) for q in qs}}
        out[name] = {"euro_area": yearly_real_share(k7, le, pi_ea, years),
                     "us_lines": "19-21" if name == "F51" else "22-24",
                     "us": yearly_real_share(gain_us, lvl_us, pi_us, years)}
    return out


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: v for k, v in r.items() if k != "partition_gap_quarters"}, indent=1)[:3000])
