"""The figures of map v11's new cards (round 2), drawn by ``ft.charts`` in the house style from the committed runs and
the registry: CS-A (C18) on consumer prices with Bernanke & James's wholesale gap beside as theirs; CS-B (C20, C19's
medians beside) by class and era; CS-D (C16) the ratio by variant against the band of what matters. ``run.py`` calls
:func:`main` after ``figures.py``. Nothing is computed here that a card or the registry did not compute.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ft import charts
from ft.charts.style import figure, source_line, title

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
RUNS = STUDY / "results" / "runs"
FIG = STUDY / "results" / "figures"
T = charts.TOKENS
SIZES = (("long", "", True), ("carousel", "-carousel", False))


def load(card: str) -> dict:
    return json.loads((RUNS / f"{card}.json").read_text())["result"]


def reg() -> dict:
    return json.loads((STUDY / "results" / "numbers.json").read_text())["numbers"]


def cs_a() -> None:
    r = load("C18-cs-a-consumer-prices-off-gold")
    # 1931-34 only, and no Bernanke-James line: a group of two or three economies in 1930 and 1935-36 comes close to
    # one economy's JST value, and the figure is ours alone (the engine's decision, 2026-10-09)
    by = {int(y): v for y, v in r["main"]["by_year"].items() if 1931 <= int(y) <= 1934}
    years = sorted(by)
    src = ("Source: Jorda-Schularick-Taylor Macrohistory Database R6 (consumer prices); Bernanke and James (1991), "
           "Table 2.1 (the dates each economy left gold); First Thing. 1931 described only; from 1935 too few "
           "economies stayed on gold.")
    for size, suffix, titled in SIZES:
        fig, ax = figure(size)
        lo, hi, pooled = r["main"]["lo"], r["main"]["hi"], r["main"]["pooled"]
        ax.fill_between([1931.6, 1934.4], lo, hi, color=T["grey_light"], alpha=0.6, linewidth=0)
        ax.plot([1931.6, 1934.4], [pooled, pooled], color=T["green"], linewidth=1.2, linestyle="--")
        ax.plot(years, [by[y] for y in years], color=T["green"], marker="o", linewidth=1.8)
        ax.axhline(0, color=T["muted"], linewidth=0.8)
        fs = 7 if size == "long" else 9
        ax.text(years[-1] + 0.12, by[years[-1]], "consumer\nprices (ours)", fontsize=fs, color=T["ink"],
                va="center")
        ax.text(1933, lo - 0.4, "1932-34 pooled, with its range", fontsize=fs, color=T["muted"], ha="center",
                va="top")
        ax.set_xlim(1930.6, 1935.6)
        ax.set_xticks(years)
        ax.set_ylim(min(lo, min(by.values())) - 3, max(hi, max(by.values())) + 3)
        ax.set_ylabel("off less on gold, points")
        title(ax, "After leaving gold: prices off gold against those still on it" if titled else None,
              "Inflation off gold less inflation on gold, by year" if titled else None)
        source_line(fig, src)
        charts.save(fig, FIG / f"cs-a{suffix}")


def cs_b() -> None:
    r20, r19 = load("C20-cs-b-without-hyperinflation-years"), load("C19-cs-b-inflation-by-convertibility")
    groups = [("all years", r20["by_class"]["convertible"]["mean"], r20["by_class"]["fiat"]["mean"],
               r19["by_class"]["convertible"]["median"], r19["by_class"]["fiat"]["median"])]
    for era, name in (("1870-1913", "1870-1913"), ("1919-1938", "1919-38")):
        e = r20["eras"][era]
        groups.append((name, e["convertible"]["mean"], e["fiat"]["mean"], None, None))
    groups.append(("1972-2020", None, r20["eras"]["1972-2020"]["fiat"]["mean"], None, None))
    bw = r20["by_class"]["bretton_woods"]["mean"]
    src = ("Source: Jorda-Schularick-Taylor Macrohistory Database R6 (consumer prices); Bordo and Schwartz (1994), "
           "Table 1A (dates); First Thing. Means leave out the years above 100%, "
           "which would swamp them; medians keep every year. War years and Bretton Woods set apart.")
    for size, suffix, titled in SIZES:
        fig, ax = figure(size)
        x = np.arange(len(groups))
        w = 0.36
        for i, (name, conv, fiat, conv_md, fiat_md) in enumerate(groups):
            if conv is not None:
                ax.bar(i - w / 2, conv, w, color=T["grey_light"])
            ax.bar(i + w / 2, fiat, w, color=T["green"])
            if conv_md is not None:
                ax.scatter([i - w / 2, i + w / 2], [conv_md, fiat_md], color=T["ink"], marker="_", s=180, zorder=3)
        ax.axhline(bw, color=T["muted"], linewidth=0.8, linestyle="--")
        ax.axhline(0, color=T["muted"], linewidth=0.8)
        ax.set_xticks(x, [g[0] for g in groups])
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch
        # the panel of 2026-10-08: readers could not decode the dashes and the dashed line, so the key names them
        ax.legend(handles=[Patch(color=T["grey_light"], label="convertible into gold"),
                           Patch(color=T["green"], label="inconvertible"),
                           Line2D([], [], color=T["ink"], marker="_", markersize=12, linestyle="none",
                                  label="median, all years"),
                           Line2D([], [], color=T["muted"], linewidth=0.8, linestyle="--",
                                  label="Bretton Woods, our mean")],
                  loc="upper right", ncol=2, frameon=False, handlelength=1.4, columnspacing=1.0)
        ax.set_ylim(top=bw + 3.4)
        ax.set_ylabel("average inflation, % a year")
        title(ax, "Inflation in years a money was convertible into gold, and years it was not" if titled else None,
              "Means by class and era; short bars: medians over all years" if titled else None)
        source_line(fig, src)
        charts.save(fig, FIG / f"cs-b{suffix}")


def cs_d() -> None:
    r, n = load("C16-cs-d-default-ratio"), reg()
    m = n["cs_d_ratio"]["matters"]
    rows = [("headline", "every crisis counted"), ("shared_once", "shared monies counted once"),
            ("T2-var-private", "private creditors only")]
    src = ("Source: the Bank of Canada-Bank of England sovereign default database (2025), the panel of money crises "
           "and strained years (IMF, World Bank, JST, Reinhart-Rogoff); First Thing. Ratio of the share of money "
           "crises after a default to the share of strained years that held with one; 95% range by money.")
    for size, suffix, titled in SIZES:
        fig, ax = figure(size)
        ax.axvspan(1 / m, m, color=T["grey_light"], alpha=0.6, linewidth=0)
        ax.axvline(1, color=T["muted"], linewidth=0.8)
        for i, (key, name) in enumerate(reversed(rows)):
            x = r["readings"][key]
            lo, hi = max(x["interval"]["lo"], 0.25), x["interval"]["hi"]
            ax.plot([lo, hi], [i, i], color=T["ink"], linewidth=1.5)
            ax.scatter([x["ratio"]], [i], color=T["green"], s=30, zorder=3)
            ax.text(hi * 1.05, i, f"{name} ({x['after']} of {x['readable']})", va="center",
                    fontsize=7 if size == "long" else 9, color=T["ink"])
        ax.set_xscale("log")
        from matplotlib.ticker import NullFormatter, NullLocator
        ax.xaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_xticks([0.25, 0.5, 1, 1.5, 2], ["0.25", "0.5", "1", "1.5", "2"])
        ax.set_xlim(0.25, 8)
        ax.set_yticks([])
        ax.set_xlabel("times as often (log scale)")
        title(ax, "Defaults before money crises, against strained years that held" if titled else None,
              "Dot: the ratio; bar: its range; shaded: smaller than what matters" if titled else None)
        source_line(fig, src)
        charts.save(fig, FIG / f"cs-d{suffix}")


def cover() -> None:
    """The carousel's cover (step f): Bordo & Schwartz's Table 3, row j, as theirs: inflation in the G10 economies and
    Switzerland under the gold standard, Bretton Woods and the float (GNP deflators, log-trend rates)."""
    n = reg()
    bars = [("gold standard\n1881–1913", n["bs3_g10_gold"]["value"], T["grey_light"]),
            ("Bretton Woods\n1946–70", n["bs3_g10_bw"]["value"], T["grey"]),
            ("the float\n1974–90", n["bs3_g10_float"]["value"], T["green"])]
    fig, ax = figure("cover")
    for i, (name, val, col) in enumerate(bars):
        ax.bar(i, val, 0.6, color=col)
        ax.text(i, val + 0.15, f"{val:.1f}%", ha="center", va="bottom", fontsize=13, color=T["ink"])
    ax.set_xticks(range(len(bars)), [b[0] for b in bars])
    ax.set_ylim(0, max(b[1] for b in bars) * 1.25)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylabel("")
    source_line(fig, "Inflation a year, G10 and Switzerland. The float: none of their monies convertible into gold. Source: Bordo and "
                     "Schwartz (1994), Table 3.")
    charts.save(fig, FIG / "bs3-cover")


def main() -> None:
    cover()
    cs_a()
    cs_b()
    cs_d()


if __name__ == "__main__":
    main()
