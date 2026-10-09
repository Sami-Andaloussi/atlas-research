"""Every figure of the study, drawn by ``ft.charts`` in the house style from the cards' results: the long
version's at size ``long`` with a title, the carousel's (and the newsletter's) at ``carousel`` without
one, the cover's at ``cover``. Called by ``run.py`` after the cards have run.
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

from ft import charts  # noqa: E402
from ft.charts import figures as ff  # noqa: E402
from ft.charts.style import figure, source_line, title  # noqa: E402

FIG = K.STUDY / "results" / "figures"
T = charts.TOKENS
FRED = "FRED (Board of Governors: monetary base; BEA: GDP; BLS: CPI-U)"
SIZES = (("long", "", True), ("carousel", "-carousel", False))


def load(card: str) -> dict:
    return json.loads((K.RUNS / f"{card}.json").read_text())["result"]


def door() -> None:
    r = load("C01-door")
    W1, W2 = r["paths"]["W1"], r["paths"]["W2"]
    src = f"Source: {FRED}, First Thing calculations. Months from August 2008 and from February 2020."
    src_prices = "Source: FRED (BLS: CPI-U), First Thing calculations. Months from August 2008 and from February 2020."
    for size, suffix, titled in (*SIZES, ("cover", "-cover", False)):
        series = {"2008–14": pd.Series(W1["added_share"], index=W1["months_since_start"]),
                  "2020–21": pd.Series(W2["added_share"], index=W2["months_since_start"])}
        fig = ff.long_series(series, source=src, size=size, highlight="2020–21", main="2008–14",
                             title_text="Base money added, as a share of the start year's GDP" if titled else None,
                             subtitle="Months since each printing began" if titled else None,
                             yfmt=lambda v: f"{v:.0f}%", label_ends=True)
        fig.axes[0].set_xlabel("months since the start")
        charts.save(fig, FIG / f"door-base{suffix}")
        series = {"2008–14": pd.Series(W1["prices_since_start"], index=W1["months_since_start"]),
                  "2020–21": pd.Series(W2["prices_since_start"], index=W2["months_since_start"])}
        fig = ff.long_series(series, source=src_prices, size=size, highlight="2020–21", main="2008–14",
                             title_text="Consumer prices since the start" if titled else None,
                             subtitle="Change since the first month, in percent" if titled else None,
                             yfmt=lambda v: f"{v:.0f}%", label_ends=True)
        fig.axes[0].axhline(0, color=T["muted"], linewidth=0.8)
        fig.axes[0].set_xlabel("months since the start")
        if size == "cover":
            fig.axes[0].set_ylabel("price rise")
        charts.save(fig, FIG / f"door-prices{suffix}")


def longrun() -> None:
    r = load("C28-a4-units-guard")["C02_grid"]  # C25's windows with the units guard (the regeneration's correction)
    pts = pd.DataFrame(r["points"])
    line = yaml.safe_load((K.CARDS / "C02-a4-base.yaml").read_text())["parameters"]["prior_line_teles_uhlig_pct"]
    src = ("Source: IMF International Financial Statistics (via DBnomics), World Bank (with its inflation database "
           "where prices are missing), FRED, ECB; First Thing calculations. Ten-year averages, 1950 to the end of 2020, every money with data. "
           "The check: a slope fitted on the decades to 1990, tested on those from 1990. Both axes: a "
           "symmetric log scale of the rate in percent.")
    for size, suffix, titled in (*SIZES, ("cover", "-cover", False)):
        fig, ax = figure(size)
        train = pts[pts.y1 <= 1990]
        test = pts[pts.y0 >= 1990]
        if size == "cover":  # the cover shows the two worlds: green above the line, grey below
            train, test = pts[pts.mu <= line], pts[pts.mu > line]
        sym = lambda v: np.sign(v) * np.log10(1 + np.abs(v))  # noqa: E731
        ax.scatter(sym(train.mu), sym(train.pi), s=9 if size == "long" else 12, color=T["grey"], alpha=0.55,
                   linewidths=0, label="to 1990 (the fit)", zorder=2)
        ax.scatter(sym(test.mu), sym(test.pi), s=9 if size == "long" else 12, color=T["green"], alpha=0.75,
                   linewidths=0, label="from 1990 (the check)", zorder=3)
        top = sym(max(pts.mu.max(), pts.pi.max()) * 1.05)
        xlo, ylo = sym(pts.mu.min()) - 0.05, sym(min(pts.pi.min(), 0)) - 0.05
        ax.plot([min(xlo, ylo), top], [min(xlo, ylo), top], color=T["ink"], linewidth=0.9, zorder=4,
                label="one for one")
        ax.axvline(sym(line), color=T["muted"], linewidth=0.9, linestyle="--", zorder=1,
                   label=f"{line}% money growth")
        ticks = (-10, 0, 10, 100, 1000) if size == "cover" else (-10, 0, 3, 10, 30, 100, 300, 1000)
        xt = [t for t in ticks if xlo <= sym(t) <= top]
        yt = [t for t in ticks if t >= 0 and ylo <= sym(t) <= top]
        ax.set_xticks([sym(t) for t in xt], [f"{t}%" for t in xt])
        ax.set_yticks([sym(t) for t in yt], [f"{t}%" for t in yt])
        ax.set_xlim(xlo, top)
        ax.set_ylim(ylo, top)
        ax.grid(axis="x", visible=True)
        ax.set_xlabel("money growth a year" if size == "cover"
                      else "base money growth, a year")
        ax.set_ylabel("inflation, a year")
        if size != "cover":
            ax.legend(loc="upper left", frameon=False)
        else:  # the cover names its two lines on the chart, for a reader who will not read a legend (panel, W11)
            ax.annotate(f"the {line}% line", (sym(line), top), (sym(line) - 0.06, top - 0.08), fontsize=12,
                        color=T["muted"], ha="right", va="top")
            ax.annotate("prices rising as\nfast as money", (top - 0.5, top - 0.5), (top - 0.02, ylo + 0.15),
                        fontsize=12, color=T["ink"], ha="right", va="bottom",
                        arrowprops={"arrowstyle": "-", "color": T["muted"], "linewidth": 0.8})
        # the rich currencies' decade after 2008, named: above the line on money growth, inflation low
        names = {"U2": "euro area", "GB": "Britain", "JP": "Japan", "US": "US"}
        for area, name in (names.items() if size != "cover" else ()):
            p = pts[(pts.area == area) & (pts.y0 == 2010)].iloc[0]
            x, y = sym(p.mu), sym(p.pi)
            ax.scatter([x], [y], s=26 if size == "long" else 34, facecolors="none", edgecolors=T["ink"],
                       linewidths=0.9, zorder=5)
            dy = {"U2": 0.02, "GB": 0.30, "JP": -0.28, "US": -0.36}[area]
            dx = {"U2": 0.30, "GB": 0.08, "JP": 0.10, "US": -0.25}[area]
            ax.annotate(f"{name} 2010–20", (x, y), (x + dx, y + dy), fontsize=7 if size == "long" else 9,
                        color=T["ink"], ha="left" if dx > 0 else "right", va="center",
                        arrowprops={"arrowstyle": "-", "color": T["muted"], "linewidth": 0.6})
        title(ax, "Money growth and inflation, ten-year averages" if titled else None,
              "Each dot one money over one decade; the diagonal is one for one" if titled else None)
        source_line(fig, "Source: IMF, World Bank, ECB, FRED; First Thing calculations. Ten-year averages, "
                    "1950–2020." if size == "cover" else src)
        charts.save(fig, FIG / f"longrun{suffix}")


def years(ax, step: int) -> None:
    import matplotlib.dates as mdates

    ax.xaxis.set_major_locator(mdates.YearLocator(base=step))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def legend(ax, series: dict, highlight: str, main: str, **kw) -> None:
    """A legend for ``ft.charts.figures.long_series``'s lines (drawn highlight last)."""
    order = sorted(series, key=lambda n: (n == highlight, n == main))
    for line, name in zip(ax.lines[:len(order)], order):
        line.set_label(name)
    handles = {line.get_label(): line for line in ax.lines[:len(order)]}
    ax.legend([handles[n] for n in series], list(series), frameon=False, **kw)


def velocity() -> None:
    r = load("C19-velocity-bare")
    sl = r["m2"]["Selden-Latane"]["path"]
    net = r["m2net"]["Selden-Latane"]["path"]
    idx = lambda d: pd.PeriodIndex(list(d), freq="Q").to_timestamp()  # noqa: E731
    actual = pd.Series(list(sl["actual"].values()), index=idx(sl["actual"]))
    pred = pd.Series(list(sl["predicted"].values()), index=idx(sl["predicted"]))
    vnet = pd.Series(list(net["actual"].values()), index=idx(net["actual"]))
    cut = pd.Period(r["cutoff"]["fit_last_quarter"], "Q")
    src = ("Source: FRED (M2V, M2SL, TB3MS, TREAST, WSHOMCB), First Thing calculations. Fitted "
           f"1959 to {cut}; the prediction: velocity as a straight line in the three-month bill rate "
           "(the Selden–Latané form).")
    for size, suffix, titled in SIZES:
        series = {"what the interest rate predicts": pred,
                  "velocity without the Fed's purchases": vnet[vnet.index > cut.end_time],
                  "M2 velocity": actual}
        fig = ff.long_series(series, source=src, size=size, highlight="M2 velocity",
                             main="velocity without the Fed's purchases",
                             title_text="How fast broad money changes hands" if titled else None,
                             subtitle="US M2 velocity (GDP over M2), quarterly; fit before 2008, judged after" if titled else None,
                             label_ends=False)
        ax = fig.axes[0]
        x = cut.end_time
        ax.axvline(x, color=T["muted"], linewidth=0.8, zorder=1)
        ax.text(x, 0.97, "fitted up to here ", transform=ax.get_xaxis_transform(), ha="right", va="top",
                fontsize=7 if size == "long" else 9, color=T["muted"])
        legend(ax, series, "M2 velocity", "velocity without the Fed's purchases", loc="lower left")
        years(fig.axes[0], 10 if size == "long" else 20)
        charts.save(fig, FIG / f"velocity{suffix}")


def tax() -> None:
    r = load("C13-a6-checked")
    by = r["whole_stock"]["by_year"]
    src = ("Source: FRED (CPIAUCSL, CURRSL, FDIC non-interest-bearing deposits, GDP), First Thing calculations. "
           f"{max(by)}: the months to {r['period']['last_month']}, against the quarters published so far.")
    vals = {y: v["share_pct"] for y, v in sorted(by.items())}
    for size, suffix, titled in SIZES:
        fig = ff.before_during_after(vals, source=src, size=size, highlight=max(vals, key=vals.get),
                                     title_text="What inflation took from cash and deposits paying nothing" if titled else None,
                                     subtitle="Each year's loss of purchasing power, as a share of that year's GDP" if titled else None,
                                     fmt=lambda v: f"{v:.1f}%", ylabel="percent of each year's GDP")
        charts.save(fig, FIG / f"tax{suffix}")


def base_now() -> None:
    res = K.fred_series("WRESBAL") / 1e6
    cur = K.fred_series("WCURCIR") / 1e6
    start = pd.Timestamp("2007-01-01")
    src = "Source: FRED (Board of Governors, H.4.1: reserve balances and currency in circulation, weekly)."
    for size, suffix, titled in SIZES:
        fig = ff.long_series({"currency": cur[cur.index >= start], "bank reserves": res[res.index >= start]},
                             source=src, size=size, highlight="bank reserves", main="currency",
                             title_text="Where the base money sits" if titled else None,
                             subtitle="US monetary base by part, trillions of dollars" if titled else None,
                             yfmt=lambda v: f"${v:.0f}tn", label_ends=True)
        years(fig.axes[0], 4 if size == "long" else 6)
        charts.save(fig, FIG / f"base-now{suffix}")


def deciders() -> None:
    r = load("C26-a5-deciders-hko-fill")  # C18's test with the missing prices filled (the pilot's reading)
    t = r["headline"]["readings"]["design"]["tests"]["O1"]
    names = {"D1": "Floating rate\n(vs pegged)", "D2": "Rate above its floor\nnear zero (vs at it)",
             "D4": "Claims on the government\nrose most (vs the rest)", "D5": "Large deficit at the start\n(vs smaller)"}
    vals = {names[d]: t[d]["diff"] for d in names}
    src = ("Source: IMF IFS and WEO (via DBnomics), FRED, ECB, World Bank (and its inflation database); First Thing calculations. "
           f"{r['headline']['readings']['design']['n_tested']} printings tested since 1950; each bar on those its "
           f"candidate could be coded for ({', '.join(str(t[d]['n_coded']) for d in names)}, in the order "
           "exchange rate, floor, purchases, deficit): the median rise in inflation where the label holds, minus "
           "where it does not.")
    for size, suffix, titled in SIZES:
        fig = ff.cross_case(vals, source=src, size=size,
                            title_text="After a printing: four candidates, none beating chance" if titled else None,
                            subtitle="Change in inflation over the next three years: one group's median minus the other's"
                            if titled else None,
                            fmt=lambda v: f"{v:+.1f}", xlabel="extra rise in inflation, points a year")
        charts.save(fig, FIG / f"deciders{suffix}")


def us_euro() -> None:
    """Inflation in the year before each US and euro-area printing and over the three years after it."""
    rows = load("C18-a5-deciders-bare")["described_us_euro"]
    label = {"US": "US", "U2": "Euro area"}
    order = sorted(rows, key=lambda x: (x["area"] != "U2", x["m0"]))
    names = [f"{label[x['area']]}\n{pd.Period(x['m0'], 'M').strftime('%b %Y')}" for x in order]
    before = [x["O1pp"] - x["O1"] for x in order]
    after = [x["O1pp"] for x in order]
    src = ("Source: FRED (CPIAUCSL), ECB (HICP, via DBnomics); First Thing calculations. Each printing "
           "starts in the month its base money began the rise the rule counts; inflation a year, in percent.")
    for size, suffix, titled in SIZES:
        fig, ax = figure(size)
        x = np.arange(len(order))
        w = 0.38
        ax.bar(x - w / 2, before, w, color=T["grey_light"], label="the year before", zorder=2)
        ax.bar(x + w / 2, after, w, color=[T["green"] if o["m0"] >= "2019" else T["ink"] for o in order],
               label="the three years after", zorder=2)
        for xi, v in zip(x + w / 2, after):
            ax.text(xi, v + 0.12, f"{v:.1f}%", ha="center", va="bottom", fontsize=7 if size == "long" else 8.5,
                    color=T["ink"])
        ax.set_xticks(x, names)
        ax.tick_params(axis="x", labelsize=7 if size == "long" else 8.5)
        ax.axhline(0, color=T["muted"], linewidth=0.8)
        ax.set_ylim(min(0, min(before)) - 0.5, max(after) + 2.4)
        ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
        ax.grid(axis="x", visible=False)
        ax.legend(loc="upper left", frameon=False, ncol=2)
        title(ax, "Inflation before and after each printing, US and euro area" if titled else None,
              "The year before the start, and the average of the three years after" if titled else None)
        source_line(fig, src)
        charts.save(fig, FIG / f"us-euro{suffix}")


def history() -> None:
    """The thousand years told in the web study, as a compact timeline for the carousel (register C5)."""
    events = [
        {"year": 1020, "label": "Song China, 1020s: paper with a reserve and a term", "kind": "core"},
        {"year": 1350, "label": "Yuan China, 1350s: paper over-issued as civil war came", "kind": "core"},
        {"year": 1425, "label": "Ming China: unbacked paper far below face", "kind": "core"},
        {"year": 1720, "label": "France: John Law's system collapses", "kind": "core"},
        {"year": 1780, "label": "America: the Continental against coin", "kind": "core"},
        {"year": 1796, "label": "France: the assignats abandoned", "kind": "core"},
        {"year": 1864, "label": "The Confederacy cuts its money stock", "kind": "core"},
        {"year": 1879, "label": "The greenbacks back to par", "kind": "core"},
        {"year": 1923, "label": "Germany: the mark collapses", "kind": "core"},
        {"year": 1946, "label": "Hungary: the fastest inflation on record", "kind": "core"},
        {"year": 2008, "label": "Rich central banks start printing", "kind": "case"},
    ]
    src = ("Source: von Glahn (1996); Guan, Palma and Wu (2024); Velde (2003); Grubb (2008); Sargent and Velde "
           "(1995); Burdekin and Weidenmier (2001); Calomiris (1988); Hanke and Krus (2012).")
    fig = ff.timeline(events, source=src, size="carousel_tall")
    charts.save(fig, FIG / "history-carousel")


def main() -> None:
    history()
    door()
    longrun()
    deciders()
    us_euro()
    velocity()
    tax()
    base_now()


if __name__ == "__main__":
    main()
