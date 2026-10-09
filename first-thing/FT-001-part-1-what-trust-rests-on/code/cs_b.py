"""Card C19 (CS-B): average consumer-price inflation by convertibility, 17 rich economies 1870-2020, each year
classed by Bordo & Schwartz's Table 1A.

From the study's folder: ``../../toolkit/bin/ftpy code/cs_b.py``. Writes
``results/runs/C19-cs-b-inflation-by-convertibility.json``.

Readings of the card that its text leaves to the code, fixed here before the run:

- *A printed line*: the transcription's "printed on line k" in coder c2's file locates a footnote mark carried by the
  reason beside a suspension (the US's 1893 and 1907); a mark inside the date cell itself is read from the date.
- *A transition year* (the card's item 3): the calendar year of an unmarked event whose kind differs from the event
  before it (a suspension after a convertibility date, or the reverse, in either block); an economy's first printed
  date changes no status and flags nothing; a footnoted suspension (rule d) changes none either.
- *The bootstrap*: the classes' sums and counts by calendar year are drawn by year weights, so every draw keeps all
  economies of a drawn year together; a moving block starts at any year from 1870 to 2016 (blocks lie inside the
  span).
- *JST's peg*: the economy-year's ``peg`` value, 1 or 0; a missing value is left out of that comparison only.
"""

from __future__ import annotations

import csv
import io
import re
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from ft import cards
from ft.data import freeze

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
CARD = STUDY / "cards" / "C19-cs-b-inflation-by-convertibility.yaml"
T = ROOT / "data" / "reconstructed" / "ft001-cs-tables"
A = ROOT / "data" / "reconstructed" / "ft001-a" / "series.csv"
CONV, SUSP = "convertible", "inconvertible"


def read_csv(p: Path) -> list[dict]:
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def line_of(text: str) -> int | None:
    m = re.search(r"printed on line (\d+)", text or "")
    return int(m.group(1)) if m else None


def reason_marks() -> dict[tuple, str]:
    """(iso3, block, line) -> the footnote mark the reason column carries on that printed line."""
    out = {}
    for r in read_csv(T / "coders" / "c2" / "table-a.csv"):
        if r["table"] != "BS-1A" or "REASONS" not in r["column_as_printed"]:
            continue
        m = re.search(r"\(([abc])\)", r["value_as_printed"])
        if m:
            block = "silver" if r["column_as_printed"].startswith("Silver") else "gold"
            out[(r["iso3"], block, line_of(r["note"]))] = m.group(1)
    return out


def parse(value: str, earlier: bool) -> list[tuple[date, str]]:
    """A printed date cell -> [(date, role)], role 'start' or 'end' for a range, 'at' otherwise."""
    v = re.sub(r"\([abc]\)", "", value).strip()
    m = re.fullmatch(r"(\d{4})/(\d{4})", v)
    if m:
        return [(date(int(m.group(1 if earlier else 2)), 1, 1), "at")]
    m = re.fullmatch(r"(\d{4})-(\d{2,4})", v)
    if m:
        a, b = m.group(1), m.group(2)
        b = a[: 4 - len(b)] + b
        return [(date(int(a), 1, 1), "start"), (date(int(b), 1, 1), "end")]
    m = re.fullmatch(r"(\d{1,2})/(\d{4})", v)
    if m:
        return [(date(int(m.group(2)), int(m.group(1)), 1), "at")]
    m = re.fullmatch(r"(\d{4})", v)
    if m:
        return [(date(int(v), 1, 1), "at")]
    raise ValueError(f"unread date cell {value!r}")


def events(iso: str, rows: list[dict], marks: dict, earlier: bool) -> list[dict]:
    ev = []
    for r in rows:
        if r["iso3"] != iso or r["table"] != "BS-1A":
            continue
        block, what = r["kind"].split("_")
        mark = re.search(r"\(([abc])\)", r["value_as_printed"])
        mark = mark.group(1) if mark else marks.get((iso, block, line_of(r["locator"])))
        for d, role in parse(r["value_as_printed"], earlier):
            if what == "susp" and role == "end":
                ev.append({"date": d, "kind": "conv", "block": block, "mark": None, "from_range": True})
            elif what == "conv" and role == "start":
                continue  # a convertibility range takes its end
            else:
                ev.append({"date": d, "kind": what, "block": block, "mark": mark if what == "susp" else None,
                           "from_range": role != "at"})
    ev.sort(key=lambda e: (e["date"], 0 if e["kind"] == "susp" else 1))
    return ev


def classify(iso: str, ev: list[dict], prm: dict, marked_inconvertible: bool) -> dict[int, dict]:
    """Year -> {status, flags} at 1 July, rules (a)-(g)."""
    y0, y1 = prm["years"]
    live = [e for e in ev if not e["mark"]]
    marked_years = {e["date"].year for e in ev if e["mark"]}
    # (e): a suspension whose return is not printed in its own block
    own_block = []
    for i, e in enumerate(live):
        if e["kind"] != "susp":
            continue
        nxt = next((f for f in live[i + 1:] if f["kind"] == "conv"), None)
        if nxt is not None and nxt["block"] != e["block"] and not nxt["from_range"]:
            own_block.append((e["date"].year, nxt["date"].year))
    last = live[-1] if live else None
    changes = {e["date"].year for p, e in zip(live, live[1:]) if e["kind"] != p["kind"]}
    out = {}
    for y in range(y0, y1 + 1):
        mid = date(y, 7, 1)
        before = [e for e in live if e["date"] <= mid]
        flags = []
        if not before:
            out[y] = {"status": None, "flags": ["before the first printed date"]}
            continue
        st = CONV if before[-1]["kind"] == "conv" else SUSP
        if last is not None and last["kind"] == "conv" and last["date"].year >= 1929 and mid >= last["date"]:
            st = None if y <= 1936 else SUSP
            flags.append("last printed date a convertibility date (rule g)")
        if any(a <= y < b for a, b in own_block):
            flags.append("return printed in another block (rule e)")
        if y in marked_years:
            flags.append("footnoted suspension (rule d)")
            if marked_inconvertible:
                st = SUSP
        if y in changes:
            flags.append("transition year")
        out[y] = {"status": st, "flags": flags}
    return out


def jst() -> pd.DataFrame:
    raw = freeze.load("jst/macrohistory", "2026-09-30").read_bytes("JSTdatasetR6.dta")
    d = pd.read_stata(io.BytesIO(raw))[["iso", "year", "cpi", "peg"]]
    d["year"] = d.year.astype(int)
    d = d.sort_values(["iso", "year"])
    d["pi"] = 100 * (d.cpi / d.groupby("iso").cpi.shift(1) - 1)
    d.loc[d.groupby("iso").year.diff() != 1, "pi"] = np.nan
    return d.set_index(["iso", "year"])


def adoption_years() -> dict[str, int]:
    out = {}
    for r in read_csv(A):
        if r["route"] == "a4" and r["status"] == "counted":
            out[r["money"]] = int(r["period"][:4])
    return out


def panel(prm: dict, earlier: bool = False, marked_inconvertible: bool = False) -> tuple[pd.DataFrame, dict]:
    rows = read_csv(T / "series.csv")
    marks = reason_marks()
    data = jst()
    wars = prm["war_years"]
    bw0, bw1 = prm["bretton_woods"]
    recs, unclassed = [], {}
    for iso in prm["economies"]:
        cls = classify(iso, events(iso, rows, marks, earlier), prm, marked_inconvertible)
        for y, c in cls.items():
            if c["status"] is None:
                unclassed.setdefault(iso, []).append(y)
                continue
            if (iso, y) not in data.index or not np.isfinite(data.at[(iso, y), "pi"]):
                continue
            klass = ("war" if any(a <= y <= b for a, b in wars) else "bretton_woods" if bw0 <= y <= bw1
                     else "convertible" if c["status"] == CONV else "fiat")
            recs.append({"iso": iso, "year": y, "pi": float(data.at[(iso, y), "pi"]), "class": klass,
                         "status": c["status"], "flags": c["flags"], "peg": data.at[(iso, y), "peg"]})
    return pd.DataFrame(recs), {k: [min(v), max(v), len(v)] for k, v in unclassed.items()}


def describe(x: pd.Series) -> dict:
    return {"n": int(len(x)), "mean": float(x.mean()) if len(x) else None,
            "median": float(x.median()) if len(x) else None,
            "share_above_10": float((x > 10).mean()) if len(x) else None, "above_100": int((x > 100).sum())}


def year_matrix(d: pd.DataFrame, years: np.ndarray, classes: list[str]) -> tuple[np.ndarray, np.ndarray]:
    S = np.zeros((len(years), len(classes)))
    N = np.zeros((len(years), len(classes)))
    idx = {y: i for i, y in enumerate(years)}
    for (y, c), g in d.groupby(["year", "class"]):
        if c in classes:
            S[idx[y], classes.index(c)] = g.pi.sum()
            N[idx[y], classes.index(c)] = len(g)
    return S, N


def interval(d: pd.DataFrame, prm: dict, blocks: bool) -> dict:
    y0, y1 = prm["years"]
    years = np.arange(y0, y1 + 1)
    classes = ["convertible", "fiat"]
    S, N = year_matrix(d, years, classes)
    rng = np.random.default_rng(prm["seed"])
    L, n = prm["block_years"], len(years)
    gaps, means = [], []
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
        m = (w @ S) / np.where(w @ N > 0, w @ N, np.nan)
        means.append(m)
        gaps.append(m[1] - m[0])
    gaps, means = np.array(gaps), np.array(means)
    q = lambda v: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]  # noqa: E731
    return {"gap": q(gaps), "convertible_mean": q(means[:, 0]), "fiat_mean": q(means[:, 1])}


def reading(lo: float, hi: float, line: float) -> str:
    if lo > line:
        return "effect"
    if hi < -line:
        return "effect of the other sign"
    if lo >= -line and hi <= line:
        return "too small to matter"
    return "bounded"


def read(d: pd.DataFrame, prm: dict, line: float) -> dict:
    conv, fiat = d[d["class"] == "convertible"].pi, d[d["class"] == "fiat"].pi
    gap = float(fiat.mean() - conv.mean())
    blk, iid = interval(d, prm, True), interval(d, prm, False)
    return {"convertible": describe(conv), "fiat": describe(fiat), "gap": gap, "interval": blk["gap"],
            "means_interval": {k: blk[k] for k in ("convertible_mean", "fiat_mean")}, "iid_years_interval": iid["gap"],
            "reading": reading(*blk["gap"], line), "refuted": False}


def main() -> Path:
    card = yaml.safe_load(CARD.read_text())
    cards.require_locked(CARD)
    prm, mt = card["parameters"], card["matters"]
    d, unclassed = panel(prm)
    out = {"economies": prm["economies"], "unclassed": unclassed, "economy_years": int(len(d)),
           "by_class": {c: describe(d[d["class"] == c].pi) for c in ("convertible", "fiat", "war", "bretton_woods")},
           "main": read(d, prm, mt["cs_b_gap"])}
    from_1972 = d[(d["class"] != "fiat") | (d.year >= 1972)]
    out["fiat_from_1972"] = read(from_1972, prm, mt["cs_b_gap_from_1972"])
    trans = d["flags"].apply(lambda f: "transition year" in f)
    out["no_transition_years"] = read(d[~trans], prm, mt["cs_b_gap_no_transition"])
    own = d["flags"].apply(lambda f: "return printed in another block (rule e)" in f)
    out["own_block_returns_only"] = read(d[~own], prm, mt["cs_b_gap_own_block_returns"])
    d_e, _ = panel(prm, earlier=True)
    out["earlier_resumption"] = read(d_e, prm, mt["cs_b_gap_earlier_resumption"])
    d_m, _ = panel(prm, marked_inconvertible=True)
    out["marked_suspensions_inconvertible"] = read(d_m, prm, mt["cs_b_gap_marked_suspensions"])
    adopt = adoption_years()
    f72 = d[(d["class"] == "fiat") & (d.year >= 1972)]
    out["fiat_from_1972_by_target"] = {
        "before_adoption": describe(f72[f72.apply(lambda r: r.iso in adopt and r.year < adopt[r.iso], axis=1)].pi),
        "from_adoption": describe(f72[f72.apply(lambda r: r.iso in adopt and r.year >= adopt[r.iso], axis=1)].pi),
        "no_counted_adoption": describe(f72[~f72.iso.isin(adopt)].pi), "adoption_years": adopt}
    out["eras"] = {f"{a}-{b}": {c: describe(d[(d.year >= a) & (d.year <= b) & (d["class"] == c)].pi)
                                for c in ("convertible", "fiat", "bretton_woods")} for a, b in prm["eras"]}
    nw = d[d["class"] != "war"].dropna(subset=["peg"])
    out["jst_peg_beside"] = {"peg_1": describe(nw[nw.peg == 1].pi), "peg_0": describe(nw[nw.peg == 0].pi)}
    out["flags_count"] = {f: int(d["flags"].apply(lambda x: f in x).sum()) for f in
                          ("transition year", "footnoted suspension (rule d)", "return printed in another block (rule e)",
                           "last printed date a convertibility date (rule g)")}
    out["beside"] = ("Bordo & Schwartz Table 3 (GNP deflators, log-trend rates, by period) and Rolnick & Weber "
                     "pp. 13, 16 (twelve countries), theirs")
    path = cards.write_result(STUDY, CARD, out)
    print(path)
    return path


if __name__ == "__main__":
    main()
