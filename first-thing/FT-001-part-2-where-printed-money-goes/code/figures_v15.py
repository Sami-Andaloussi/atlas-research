"""The figures of map v15's new cards (round 2), drawn by ``ft.charts`` in the house style from the committed runs:
the door's monthly timeline and Blanchard & Bernanke's decomposition (C32, CS-C), the slopes of base and broad
money on the same calm decades (C30, CS-B), and the pandemic cross-section (C31, CS-E). ``run.py`` calls
:func:`main` after ``figures.py``. Nothing is computed here that a card did not compute, but the points the cards
read (C28's windows for CS-B, C31's frame for CS-E), re-read through the cards' own code.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

from ft import charts  # noqa: E402
from ft.charts import style  # noqa: E402

FIG = K.STUDY / "results" / "figures"
T = charts.TOKENS


def load(card: str) -> dict:
    return json.loads((K.RUNS / f"{card}.json").read_text())["result"]


def panels(n: int, height: float, size: str = "long"):
    """A figure of ``n`` stacked panels sharing the time axis, in the house style."""
    style.apply()
    plt.rcParams.update({k: v * style.TEXT_SCALE[size] for k, v in style._BASE_SIZES.items()})
    fig, axes = plt.subplots(n, 1, figsize=(style.SIZES[size][0], height), dpi=style.DPI, sharex=True,
                             layout="constrained")
    return fig, axes


def label(ax, text: str) -> None:
    """A panel's name, top left inside the axes, in ink (text never wears a series colour)."""
    ax.text(0.005, 0.97, text, transform=ax.transAxes, ha="left", va="top", fontsize=plt.rcParams["axes.labelsize"],
            color=T["ink"], fontweight=600)


def months(index) -> pd.DatetimeIndex:
    return pd.PeriodIndex(list(index), freq="M").to_timestamp(how="end") - pd.offsets.Day(14)


def quarters(index) -> pd.DatetimeIndex:
    return pd.PeriodIndex(list(index), freq="Q").to_timestamp(how="end") - pd.offsets.Day(45)


#: The acts' labels on the chart, short so they stay inside the prices' panel; the card's full names go to the source
#: line (C32 item 4).
SHORT = {"2020-03": "lockdowns, CARES Act", "2021-03": "Rescue Plan", "2022-02": "Ukraine invaded",
         "2022-03": "Fed's first rise"}


def door_timeline(stretch: bool) -> None:
    """C32 item 3: the monthly timeline, panels on separate axes, the acts K5's sources name; the stretch to 2023-03
    on the web study's figure only (item 4)."""
    r = load("C32-cs-c-door-timeline")
    m = pd.DataFrame(r["timeline"]["monthly"]).T
    q = pd.DataFrame(r["timeline"]["quarterly"]).T
    if stretch:
        m = pd.concat([m, pd.DataFrame(r["stretch"]["monthly"]).T])
        q = pd.concat([q, pd.DataFrame(r["stretch"]["quarterly"]).T])
    # v/u from BLS's own series (C34, C32's correction): Blanchard & Bernanke's are cited, never redistributed
    q["v_over_u"] = pd.Series(load("C34-cs-c-vu-bls")["quarterly"])
    mt, qt = months(m.index), quarters(q.index)
    fig, ax = panels(7, 12.5)
    base = ax[0]
    base.stackplot(mt, m.reserves_bn.astype(float) / 1000, m.currency_bn.astype(float) / 1000,
                   colors=[T["green"], T["grey_light"]], linewidth=0)
    base.annotate("reserves", (mt[-1], float(m.reserves_bn.iloc[-1]) / 2000), xytext=(4, 0),
                  textcoords="offset points", va="center", fontsize=plt.rcParams["legend.fontsize"], color=T["ink"])
    base.annotate("currency", (mt[-1], (float(m.reserves_bn.iloc[-1]) + float(m.currency_bn.iloc[-1]) / 2) / 1000),
                  xytext=(4, 0), textcoords="offset points", va="center", fontsize=plt.rcParams["legend.fontsize"],
                  color=T["ink"])
    label(base, "Base money, $ trillion")
    rows = [(ax[1], mt, m.m2_yoy_pct, "The public's money (M2), growth over 12 months, %", T["ink"]),
            (ax[2], qt, q.m2v, "Velocity of M2 (nominal GDP over M2), quarterly", T["ink"]),
            (ax[3], qt, q.ngdp_4q_growth_pct, "Nominal GDP, growth over 4 quarters, %", T["ink"]),
            (ax[4], mt, m.cpi_yoy_pct, "Consumer prices, inflation over 12 months, %", T["ink"]),
            (ax[5], qt, q.v_over_u, "Job openings per unemployed person (v/u, BLS JOLTS)", T["ink"]),
            (ax[6], mt, m.unrate_pct, "Unemployment rate, %", T["grey"])]
    for a, x, y, name, colour in rows:
        a.plot(x, y.astype(float), color=colour, linewidth=1.4)
        label(a, name)
        a.margins(y=0.25)
    for a in (ax[1], ax[3], ax[4]):
        a.axhline(0, color=T["muted"], linewidth=0.6)
    acts = r["annotations"]["W2"] + (r["annotations"]["stretch"] if stretch else [])
    for i, act in enumerate(acts):
        x = months([act["month"]])[0]
        for a in ax:
            a.axvline(x, color=T["muted"], linewidth=0.7, linestyle=":")
        right = i % 2 == 1  # acts a month apart: their labels on either side of their lines
        ax[4].annotate(SHORT[act["month"]], (x, 1.0), xycoords=("data", "axes fraction"), xytext=(3 if right else -3, -14),
                       textcoords="offset points", rotation=90, ha="left" if right else "right", va="top",
                       fontsize=plt.rcParams["legend.fontsize"] * 0.9, color=T["muted"])
    for name in ("W1", "W2"):
        w = r["windows"][name]
        s, e = months([w["start"], w["end"]])
        for a in ax:
            a.axvspan(s, e, color=T["shade"], zorder=0, linewidth=0)
    style.title(ax[0], "The modern Fed's two largest printings, month by month",
                "Shaded: August 2008 to October 2014, and February 2020 to December 2021. Velocity, nominal GDP "
                "and M2 are one fact (velocity is GDP over M2)")
    end = "March 2023" if stretch else "December 2021"
    named = "; ".join(f"{a['month']}: {a['label']}" for a in acts)
    style.source_line(fig, f"Source: FRED (Board of Governors H.4.1 and H.6; BEA; BLS, with JOLTS openings over unemployed "
                      f"persons for v/u); First Thing calculations. August 2008 to {end}. Dotted lines: "
                      f"{named}. In moderate "
                      "inflations, monetary policy's peak effect on prices has come more than a year later (Batini "
                      "& Nelson 2002).")
    charts.save(fig, FIG / ("door-timeline-web" if stretch else "door-timeline"))


def door_decomposition(stretch: bool) -> None:
    """C32 item 3 (g): Blanchard & Bernanke's Figure 12 decomposition whole, as theirs, from 2020Q1, in its own
    panel, under the card's fixed caption."""
    r = load("C32-cs-c-door-timeline")
    d = pd.DataFrame(r["decomposition"]["quarters"]).T
    if not stretch:
        d = d.loc[: "2021Q4"]
    parts = [("initial conditions", T["grey_light"]), ("v/u", T["green"]), ("energy", T["grey"]),
             ("food", T["shade_emphasis"]), ("shortages", T["muted"])]
    fig, ax = style.figure("long")
    x = np.arange(len(d))
    pos, neg = np.zeros(len(d)), np.zeros(len(d))
    for name, colour in parts:
        v = d[name].astype(float).to_numpy()
        bottom = np.where(v >= 0, pos, neg)
        ax.bar(x, v, 0.7, bottom=bottom, color=colour, label=name, linewidth=0)
        pos, neg = pos + np.clip(v, 0, None), neg + np.clip(v, None, 0)
    ax.plot(x, d["actual"].astype(float), color=T["ink"], linewidth=1.6, marker="o", markersize=3,
            label="actual inflation (theirs)")
    ax.axhline(0, color=T["muted"], linewidth=0.6)
    ax.set_xticks(x, list(d.index), rotation=0)
    for t in ax.get_xticklabels()[1::2]:
        t.set_visible(False)
    ax.set_ylabel("CPI inflation, annualised quarterly log change, %")
    ax.legend(loc="upper left", ncols=3, frameon=False)
    style.title(ax, "What Blanchard & Bernanke's model attributes the inflation to",
                "Their decomposition, drawn as theirs; the bars omit their residuals")
    style.source_line(fig, "Source: Blanchard & Bernanke (2023), NBER WP 31417, replication output "
                      "(all_data_decompositions.xls), from 2020Q1 (their figure starts at 2019Q4). "
                      + r["caption"])
    charts.save(fig, FIG / ("door-decomposition-web" if stretch else "door-decomposition"))


def _scatter(ax, x, y, slope: float, label_text: str, highlight: bool) -> None:
    ax.scatter(x, y, s=12, color=T["green"] if highlight else T["grey"], alpha=0.7, linewidths=0, zorder=2)
    xs = np.linspace(float(x.min()), float(x.max()), 50)
    ax.plot(xs, float(y.mean()) + slope * (xs - float(x.mean())), color=T["ink"], linewidth=1.4, zorder=3)
    ax.text(0.03, 0.96, label_text, transform=ax.transAxes, ha="left", va="top", color=T["ink"],
            fontsize=plt.rcParams["legend.fontsize"])


def cs_b() -> None:
    """C30: the same calm decades read against base money growth and against broad money growth; each line drawn
    through the points' means with the card's slope (output growth held fixed, so not the raw scatter's fit)."""
    import cs_b as B  # noqa: PLC0415  (the card's own frame)
    import yaml  # noqa: PLC0415
    p = yaml.safe_load((K.STUDY / "cards" / "C30-cs-b-base-against-broad.yaml").read_text())["parameters"]
    c28 = load("C28-a4-units-guard")
    d, _ = B.common_windows(c28["C02_grid"]["points"], c28["broad"]["points"])
    line = p["calm_line_pct"]
    calm = d[(d.mu_base <= line) & (d.mu_broad <= line)]
    r = load("C30-cs-b-base-against-broad")["calm"]
    assert len(calm) == load("C30-cs-b-base-against-broad")["calm"]["windows"]
    style.apply()
    plt.rcParams.update({k: v * style.TEXT_SCALE["long"] for k, v in style._BASE_SIZES.items()})
    fig, ax = plt.subplots(1, 2, figsize=style.SIZES["long"], dpi=style.DPI, sharey=True, layout="constrained")
    _scatter(ax[0], calm.mu_base, calm.pi, r["slope_base"]["b"],
             f"central-bank money: {r['slope_base']['b']:.2f} a point", False)
    _scatter(ax[1], calm.mu_broad, calm.pi, r["slope_broad"]["b"],
             f"the public's money: {r['slope_broad']['b']:.2f} a point", True)
    ax[0].set_xlabel("base money growth, % a year")
    ax[1].set_xlabel("broad money growth, % a year")
    ax[0].set_ylabel("inflation, % a year")
    style.title(ax[0], "The same calm decades, two kinds of money",
                f"{r['windows']} ten-year windows of {r['moneys']} economies, both growths at or below {line}% a year")
    style.source_line(fig, "Source: IMF International Financial Statistics (via DBnomics), World Bank, ECB, FRED; "
                      "First Thing calculations. Windows ending 1970 to 2020, mostly from 1990. Lines: each slope "
                      "with output growth held fixed, drawn through the points' means.")
    charts.save(fig, FIG / "cs-b-slopes")


def cs_e() -> None:
    """C31: the main run's economies, broad money growth 2019-21 against inflation 2021-23; the line drawn through
    the points' means with the card's Huber slope (the energy-import share held fixed)."""
    import cs_e as E  # noqa: PLC0415  (the card's own frame)
    import yaml  # noqa: PLC0415
    prm = yaml.safe_load((K.STUDY / "cards" / "C31-cs-e-pandemic-cross-section.yaml").read_text())["parameters"]
    r = load("C31-cs-e-pandemic-cross-section")
    d, _ = E.frame(prm, q6=False)
    main = d[(d.calm_mean < prm["calm_start_line_pct"]) & d.energy.notna()]
    assert len(main) == r["main"]["n"]
    fig, ax = style.figure("long")
    _scatter(ax, main.m, main.p, r["main"]["huber"], f"robust slope {r['main']['huber']:.2f} a point "
             f"(range {r['main']['huber_boot']['lo']:.2f} to {r['main']['huber_boot']['hi']:.2f})", True)
    ax.set_xlabel("broad money growth a year, December 2019 to December 2021 (log %)")
    ax.set_ylabel("inflation a year, Dec 2021 to Dec 2023 (log %)")
    style.title(ax, "Money in 2020-21 and prices in 2022-23, economy by economy",
                f"{r['main']['n']} economies that started calm (2015-19 inflation below "
                f"{prm['calm_start_line_pct']}% a year)")
    style.source_line(fig, "Source: IMF International Financial Statistics (via DBnomics), ECB, World Bank (energy "
                      "imports, 2019); First Thing calculations. Line: the Huber slope with the energy-import share "
                      "held fixed, drawn through the points' means. It cannot separate the money from the fiscal "
                      "demand that carried it.")
    charts.save(fig, FIG / "cs-e-cross-section")


def main() -> None:
    door_timeline(False)
    door_timeline(True)
    door_decomposition(False)
    door_decomposition(True)
    cs_b()
    cs_e()


if __name__ == "__main__":
    main()
