"""Every figure of part 1, drawn by ``ft.charts`` in the house style from the cards' results and the committed builds
the registry reads: the long version's at size ``long`` with a title, the carousel's at ``carousel`` without one.
Called by ``run.py`` after the cards and the registry.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
REC = ROOT / "data" / "reconstructed"
RUNS = STUDY / "results" / "runs"
FIG = STUDY / "results" / "figures"
sys.path.insert(0, str(ROOT / "bank" / "maps" / "FT-001" / "missions" / "code"))

from ft import charts  # noqa: E402
from ft.charts.style import figure, source_line, title  # noqa: E402

T = charts.TOKENS
SIZES = (("long", "", True), ("carousel", "-carousel", False))
MINT = 3.89375


def load(card: str) -> dict:
    return json.loads((RUNS / f"{card}.json").read_text())["result"]


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v: str) -> float | None:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if np.isfinite(x) else None


def _year(period: str) -> float:
    y = int(period[:4])
    return y + (int(period[5:7]) - 0.5) / 12 if len(period) >= 7 else y + 0.5


def door() -> None:
    """The price of gold in paper, 1797-1821: Tooke's annual averages from 1800 and his two dates a year, against the
    mint's price."""
    head = [r for r in read_csv(REC / "ft001-a3" / "series.csv") if r["case"] == "the Bank Restriction"]
    cross = [r for r in read_csv(REC / "ft001-a3" / "variant-cross-source.csv") if r["case"] == "the Bank Restriction"]
    annual = [(int(r["period"][:4]) + 0.5, MINT / num(r["P"])) for r in head if num(r["P"])]
    dates = [(_year(r["period"]), MINT / num(r["P"])) for r in cross if num(r["P"])]
    src = ("Source: Thomas Tooke, A History of Prices, vol. 2 (1838), p. 379 (annual averages, 1800-1821) and pp. "
           "384-385 (standard gold in bars, two dates a year), transcribed from archive.org scans; First Thing.")
    for size, suffix, titled in (*SIZES, ("cover", "-cover", False)):
        fig, ax = figure(size)
        ax.axhline(MINT, color=T["muted"], linewidth=0.9, linestyle="--")
        ax.text(1797.2, MINT - 0.06, "the mint's price", color=T["muted"], va="top",
                fontsize=7 if size == "long" else 9)
        ax.plot(*zip(*annual), color=T["green"], linewidth=1.6, label="annual average")
        ax.scatter(*zip(*dates), s=12, color=T["ink"], zorder=3, label="two dates a year")
        for x, text in ((1819.5, "1819 Act"), (1821.33, "gold again")):
            ax.axvline(x, color=T["grey_light"], linewidth=0.8)
            ax.text(x - 0.15, 5.55, text, rotation=90, ha="right", va="top", color=T["muted"],
                    fontsize=7 if size == "long" else 9)
        ax.set_xlim(1797, 1822)
        ax.set_ylim(3.7, 5.7)
        ax.yaxis.set_major_formatter(lambda v, _: f"£{v:.1f}")
        if size != "cover":
            ax.legend(loc="upper left", frameon=False)
        title(ax, "The price of an ounce of gold in Bank of England notes, 1797-1821" if titled else None,
              "Above the dashed line, gold cost more than the mint's price: the paper's premium" if titled else None)
        source_line(fig, src)
        charts.save(fig, FIG / f"door-premium{suffix}")


def a3_odds() -> None:
    """The expected wait for gold read from the premium (one over the yearly odds), by year, and the stretches where the
    premium cannot separate an expected return from the paper's own value."""
    rows = read_csv(REC / "ft001-a3" / "series.csv")
    spans = read_csv(REC / "ft001-a3" / "spans.csv")
    src = ("Source: Tooke (1838); Mitchell (1908), Table 2; Homer and Sylla (2005), Table 42; the Bank of England's "
           "millennium dataset; First Thing's reading after Calomiris (1988). Shaded, bars in grey: cannot "
           "separate, or at par.")
    for size, suffix, titled in SIZES:
        import matplotlib.pyplot as plt
        fig, ax = figure(size)
        fig.delaxes(ax)
        axes = fig.subplots(1, 2, sharey=True)
        for ax, case, start, law in ((axes[0], "the Bank Restriction", 1797, 1819.5),
                                     (axes[1], "the greenbacks", 1862, 1875.04)):
            by_year: dict[int, list[float]] = {}
            for r in rows:
                if r["case"] == case and r["phase"] == "before the law":
                    lam = num(r["lambda"])
                    if lam:
                        by_year.setdefault(int(r["period"][:4]), []).append(lam)
            years = sorted(by_year)
            wait = [1 / (sum(by_year[y]) / len(by_year[y])) for y in years]
            shaded: set[int] = set(range(1797, 1800)) if case == "the Bank Restriction" else set()  # 1797-99: at par
            for s in spans:
                if s["case"] == case:
                    shaded |= set(range(int(_year(s["first"])), int(_year(s["last"])) + 1))
            shaded |= {int(r["period"][:4]) for r in rows if r["case"] == case and r["phase"] == "before the law"
                       and "at par" in r["flags"]}                                       # a year at par (λ = ∞)
            ax.bar(years, wait, color=[T["grey_light"] if y in shaded else T["green"] for y in years], width=0.7)
            for y in sorted(shaded):
                ax.axvspan(y - 0.5, y + 0.5, color=T["shade"], zorder=0, linewidth=0)
            ax.axvline(law, color=T["grey_light"], linewidth=0.8)
            ax.set_xlabel("Britain, 1797-1821" if case == "the Bank Restriction" else "US greenbacks, 1862-1879")
        axes[0].set_ylabel("wait for gold, years")
        title(axes[0], "What the premium implies about waiting for gold" if titled else None,
              "Before each resumption law; the line marks the law" if titled else None)
        source_line(fig, src)
        charts.save(fig, FIG / f"a3-odds{suffix}")


PANEL_NAMES = {"1": "1914 suspensions", "2": "1931-36 exits from gold", "3-down": "independence cut",
               "3-up": "independence raised", "4": "inflation target adopted"}


def a2_window() -> None:
    import window_a as W
    d = REC / "ft001-a-window"
    changes = read_csv(d / "changes.csv")
    lines = W.describe(changes, read_csv(d / "null-band.csv"), read_csv(d / "placebo-band.csv"))
    pat = re.compile(r"^headline panel (\S+) \(counted\): n = \d+, with a gap (\d+), mean gap ([+-][\d.]+); "
                     r"null band under no effect \[([+-]?[\d.]+), ([+-]?[\d.]+)\]")
    got = []
    for line in lines:
        m = pat.match(line)
        if m and m.group(1) in PANEL_NAMES:
            got.append((PANEL_NAMES[m.group(1)], int(m.group(2)), float(m.group(3)), float(m.group(4)),
                        float(m.group(5))))
    src = ("Source: IMF IFS, World Bank, Reinhart-Rogoff, BIS, JST (prices); Bernanke and James; Garriga (2025); "
           "Hammond and the IMF's AREAER; First Thing. Gap: inflation over the five years after less the year before, "
           "against matched non-changers. Band: scenarios of no effect.")
    for size, suffix, titled in SIZES:
        fig, ax = figure(size)
        for i, (name, n, mean, lo, hi) in enumerate(reversed(got)):
            ax.plot([lo, hi], [i, i], color=T["grey_light"], linewidth=7, solid_capstyle="butt")
            ax.scatter([mean], [i], color=T["green"], s=30, zorder=3)
            ax.text(hi + 0.3, i, f"{name} ({n})", va="center", fontsize=7 if size == "long" else 9, color=T["ink"])
        ax.axvline(0, color=T["muted"], linewidth=0.8)
        ax.set_yticks([])
        ax.set_xlim(min(g[3] for g in got) - 1, max(g[4] for g in got) + 9)
        ax.set_xlabel("gap in inflation, percentage points")
        title(ax, "Inflation after a support changed, against monies that did not change" if titled else None,
              "Dot: the mean gap; bar: the band expected with no effect" if titled else None)
        source_line(fig, src)
        charts.save(fig, FIG / f"a2-window{suffix}")


ACT_STYLE = {"T2": ("o", "red"), "L1": ("s", "ink"), "L2": ("D", "ink"), "L3": ("^", "ink"), "H1": ("v", "ink")}


def c1_lines() -> None:
    r = load("C07-claim1-dated-lines-v2")
    lines = r["lines"]
    src = ("Source: the study's breaks, its spells of strain and its list of acts (Bank of Canada-Bank of England default "
           "database, Garriga, Ilzetzki-Reinhart-Rogoff); First Thing. Red circle: a creditor class newly in arrears; "
           "square: a lending limit lifted; diamond: a peg abandoned; triangle up: independence cut; down: a "
           "second money made legal.")
    fig, ax = figure("long")
    fig.set_size_inches(8.0, 10.5)
    for i, ln in enumerate(lines):
        y = len(lines) - i
        cross = _year(ln["crossing"])
        onset = _year(ln["onset"]) if ln["onset"] != "cannot be read" else None
        if onset is not None:
            ax.plot([onset, cross], [y, y], color=T["grey_light"], linewidth=1)
            ax.scatter([onset], [y], s=8, color=T["green"], zorder=3)
        ax.scatter([cross], [y], s=10, marker="|", color=T["ink"], zorder=3)
        for a in ln["acts"]:
            mk, col = ACT_STYLE[a["act"]]
            ax.scatter([_year(a["date"])], [y], s=9, marker=mk, facecolors="none",
                       edgecolors=T["grey"] if a.get("after_the_crossing") else T[col], linewidths=0.7, zorder=4)
        ax.text(1968.6, y, ln["money"], fontsize=5, va="center", ha="right", color=T["muted"])
    ax.set_yticks([])
    ax.set_xlim(1966, 2027)
    ax.set_ylim(0, len(lines) + 1)
    title(ax, "Every break since 1970: the acts, the onset and the crossing",
          "Green dot: the onset; bar: the crossing; shapes: the acts from three years before the onset to three "
          "after (grey: after the crossing)")
    source_line(fig, src)
    charts.save(fig, FIG / "c1-lines")


def c2_held() -> None:
    r = load("C13-claim2-institution-m0")
    names = {"supports_count": "headline", "supports_count_without_taken_back": "without taken back",
             "supports_count_without_pegs": "without pegs and boards"}
    src = ("Source: spells of fiscal strain from 1970 (debt and deficits: Reinhart-Rogoff, IMF, JST; supports: Garriga, "
           "Chinn-Ito, the Bank of Canada-Bank of England default database, Ilzetzki-Reinhart-Rogoff); First Thing. "
           "Limit by institution: legal independence or an inflation target. Counts: spells with fewer supports, with more. Bars: 90% intervals. Dashed line: the margin of 10 points "
           "fixed in advance, which a yes must pass. Green dot: yes; grey: no verdict.")
    for size, suffix, titled in SIZES:
        fig, ax = figure(size)
        rows = [(names[k], r["readings"][k]) for k in names]
        for i, (name, v) in enumerate(reversed(rows)):
            lo, hi = v["interval_90"]
            if lo is not None:
                ax.plot([lo, hi], [i, i], color=T["grey_light"], linewidth=6, solid_capstyle="butt")
            ax.scatter([v["D_points"]], [i], color=T["green"] if v["outcome"] == "confirmed" else T["grey"], s=30,
                       zorder=3)
            ax.text(52, i, f"{name}: {v['n_one_or_none']} fewer, {v['n_two_or_more']} more", va="center",
                    fontsize=7 if size == "long" else 8, color=T["ink"])
        ax.axvline(0, color=T["muted"], linewidth=0.8)
        ax.axvline(10, color=T["muted"], linewidth=0.8, linestyle="--")
        ax.set_yticks([])
        ax.set_xlim(-60, 120)
        ax.set_xlabel("difference in the share that held, points")
        title(ax, "Did monies with more supports hold more often?" if titled else None,
              "Dashed: the margin fixed in advance; grey dot: no verdict" if titled else None)
        source_line(fig, src)
        charts.save(fig, FIG / f"c2-held{suffix}")


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    door()
    a3_odds()
    a2_window()
    c1_lines()
    c2_held()


if __name__ == "__main__":
    main()
