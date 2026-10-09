"""The web study's folder for map v15 (round 2; BLUEPRINT §5 w): ``web/site/<slug>/`` with ``meta.json``,
``glossary.json``, every figure of map v15's web plan (a Vega-Lite spec reading its ``data.csv``), the household
calculator and ``og.png``. ``run.py`` calls :func:`main` in place of round 1's ``web.main``; ``toolkit/bin/ft study
web`` then renders the article and the numbers into the same folder.

Everything is drawn from the cards' stored runs (C28, C29, C30, C31, C32, C33) and the registry; nothing is
recomputed and no explorer shows a variant no card ran. Round 1's helpers (``web.fig``, ``web.names``, ``web.base_now``,
``web.calculator``) are reused where the new engine would draw the same: the reserves-and-currency chart and the
calculator read the same frozen series and the same registered rise.
"""

from __future__ import annotations

import io
import json
import shutil
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402
import web as W  # noqa: E402

from ft import numbers  # noqa: E402

OUT = W.OUT
TITLE = "Does printing money really cause inflation?"
STANDFIRST = ("We read the evidence this way: printing money raises prices when the new money reaches people who spend it rather than hold it, in "
              "an economy that cannot simply produce more, and when it is expected to last.")
W.AS_OF = "2026-10-08"  # the as-of of round 2's series (the grid check of 2026-10-08, I)
tip = W.tip


def load(card: str) -> dict:
    return W.load(card)


def longrun(R: numbers.Registry) -> None:
    """CS-A: C28's guarded windows, base money and broad money, with a toggle between the two (both runs exist)."""
    r = load("C28-a4-units-guard")
    line = R.get("lr_line")["value"]
    nm = W.names()
    rows = []
    for measure, pts in (("central-bank money", r["C02_grid"]["points"]), ("the public's money", r["broad"]["points"])):
        for p in pts:
            rows.append({"money": measure, "economy": nm.get(p["area"], p["area"]), "decade": f"{p['y0']}–{p['y1']}",
                         "money_growth": round(p["mu"], 1), "inflation": round(p["pi"], 1),
                         "pace": f"above {line:g}% a year" if p["mu"] > line else f"at or below {line:g}% a year"})
    sym = {"type": "symlog", "constant": 1}
    spec = {
        "height": 320,
        "params": [{"name": "money", "value": "central-bank money",
                    "bind": {"input": "radio", "options": ["central-bank money", "the public's money"],
                             "name": "Money: "}}],
        "transform": [{"filter": "datum.money == money"}],
        "layer": [
            {"mark": {"type": "point", "filled": True, "opacity": 0.6, "size": 22},
             "encoding": {
                 "x": {"field": "money_growth", "type": "quantitative", "scale": sym,
                       "title": "money growth, % a year (ten-year average)"},
                 "y": {"field": "inflation", "type": "quantitative", "scale": sym, "title": "inflation, % a year"},
                 "color": {"field": "pace", "type": "nominal", "legend": {"orient": "bottom", "title": None}},
                 "tooltip": tip({"field": "economy", "type": "nominal"}, {"field": "decade", "type": "nominal"},
                                {"field": "money_growth", "type": "quantitative", "title": "money growth, % a year"},
                                {"field": "inflation", "type": "quantitative", "title": "inflation, % a year"})}},
            {"mark": {"type": "rule", "strokeDash": [4, 3]},
             "encoding": {"x": {"datum": line, "type": "quantitative", "scale": sym}}},
        ],
    }
    W.fig("fig-longrun", rows, spec, source_note=f"IMF International Financial Statistics, World Bank, ECB, FRED; "
          f"First Thing calculations; {W.DERIVED}",
          title="Money growth and inflation over ten-year windows, every economy with the data",
          measure="average money growth (central-bank money or the public's money) against average consumer-price "
                  "inflation, ten-year windows", unit="% a year", period="ten-year windows, 1950-2020",
          population="every economy with the data at both ends of a window",
          source="IMF International Financial Statistics (via DBnomics), World Bank and its inflation database, ECB, "
                 "FRED; First Thing calculations", source_url=W.IMF_URL, licence=W.DERIVED,
          highlight=f"above {line:g}% a year",
          caption=f"Each dot is one economy over ten years. The dashed line is {line:g}% a year of money growth. Both "
                  "axes stretch the small values so that slow and fast printers both show. Switch between "
                  "central-bank money and the public's money: both were run.",
          alt="A cloud of dots rising from the lower left: flat and low left of the dashed line, climbing more "
              "steeply to its right.",
          description="Each dot is an economy's ten-year average money growth against its average inflation. Left "
                      "of the dashed line the central-bank money cloud is flat: faster money growth went with little more inflation. "
                      "To its right the cloud climbs steeply. The toggle shows the public's money instead, its windows "
                      "and its calm decades counted on its own growth.",
          claims=["p2-1-steeper-with-pace", "k1-money-and-prices"])


def bands(R: numbers.Registry) -> None:
    """CS-A's exploration (C29): the slope in each band of money growth, with its range."""
    r = load("C29-a4-exploration-pace")
    names = {"S1_band_le12": "at or below 12%", "S2_band_12_20": "12% to 20%", "S3_band_20_30": "20% to 30%",
             "S4_band_30_50": "30% to 50%", "S5_band_gt50": "above 50%"}
    rows = [{"band": label, "order": i, "slope": round(r[k]["beta"], 2), "low": round(r[k]["lo"], 2),
             "high": round(r[k]["hi"], 2), "windows": r[k]["windows"]} for i, (k, label) in enumerate(names.items())]
    spec = {"height": 220,
            "layer": [
                {"mark": {"type": "rule", "strokeWidth": 2},
                 "encoding": {"y": {"field": "band", "type": "nominal", "sort": {"field": "order"}, "title": None},
                              "x": {"field": "low", "type": "quantitative",
                                    "title": "points of inflation per point of money growth"},
                              "x2": {"field": "high"}}},
                {"mark": {"type": "point", "filled": True, "size": 60},
                 "encoding": {"y": {"field": "band", "type": "nominal", "sort": {"field": "order"}},
                              "x": {"field": "slope", "type": "quantitative"},
                              "tooltip": tip({"field": "band", "type": "nominal", "title": "money growth"},
                                             {"field": "slope", "type": "quantitative", "format": ".2f"},
                                             {"field": "low", "type": "quantitative", "format": ".2f"},
                                             {"field": "high", "type": "quantitative", "format": ".2f"},
                                             {"field": "windows", "type": "quantitative",
                                              "title": "ten-year windows"})}}]}
    W.fig("fig-bands", rows, spec, source_note=f"IMF IFS, World Bank, ECB, FRED; First Thing calculations; {W.DERIVED}",
          title="How much inflation went with each point of central-bank money growth, by pace",
          measure="slope of inflation on base money growth within each band, output growth held fixed, with its range",
          unit="points of inflation per point of money growth", period="ten-year windows, 1950-2020",
          population="every economy with the data, by band of base money growth",
          source="IMF International Financial Statistics (via DBnomics), World Bank, ECB, FRED; First Thing "
                 "calculations", source_url=W.IMF_URL, licence=W.DERIVED,
          caption="An exploration: the bands were cut after the main split was seen, so they describe, never test.",
          alt="Five dots with their ranges, the slope on central-bank money rising from about a quarter of a point at "
              "slow paces to about one at the fastest.",
          description="For each band of central-bank money growth, the slope of inflation on it and its range: about "
                      "a quarter of a point in calm decades, rising with the pace to about one point above fifty "
                      "per cent a year.",
          claims=["p2-1-bands"])


def calm() -> None:
    """CS-B (C30): the same calm windows read against base and against broad money growth; each fit line drawn
    through the points' means with the card's slope (output growth held fixed)."""
    import cs_b as B  # noqa: PLC0415

    p = yaml.safe_load((K.STUDY / "cards" / "C30-cs-b-base-against-broad.yaml").read_text())["parameters"]
    c28 = load("C28-a4-units-guard")
    d, _ = B.common_windows(c28["C02_grid"]["points"], c28["broad"]["points"])
    line = p["calm_line_pct"]
    calm_w = d[(d.mu_base <= line) & (d.mu_broad <= line)]
    r = load("C30-cs-b-base-against-broad")["calm"]
    nm = W.names()
    rows = []
    for col, label, slope in (("mu_base", "central-bank money", r["slope_base"]["b"]),
                              ("mu_broad", "the public's money", r["slope_broad"]["b"])):
        for _, w in calm_w.iterrows():
            rows.append({"money": label, "kind": "window", "economy": nm.get(w["area"], w["area"]),
                         "decade": f"{int(w['y0'])}–{int(w['y1'])}", "money_growth": round(float(w[col]), 2),
                         "inflation": round(float(w["pi"]), 2)})
        mx, my = float(calm_w[col].mean()), float(calm_w["pi"].mean())
        for x in (float(calm_w[col].min()), float(calm_w[col].max())):
            rows.append({"money": label, "kind": "slope", "economy": "", "decade": "",
                         "money_growth": round(x, 2), "inflation": round(my + slope * (x - mx), 2)})
    spec = {"height": 240,
            "facet": {"column": {"field": "money", "type": "nominal", "title": None,
                                 "sort": ["central-bank money", "the public's money"]}},
            "spec": {"layer": [
                {"transform": [{"filter": "datum.kind == 'window'"}],
                 "mark": {"type": "point", "filled": True, "opacity": 0.6, "size": 18},
                 "encoding": {"x": {"field": "money_growth", "type": "quantitative",
                                    "title": "money growth, % a year"},
                              "y": {"field": "inflation", "type": "quantitative", "title": "inflation, % a year"},
                              "tooltip": tip({"field": "economy", "type": "nominal"},
                                             {"field": "decade", "type": "nominal"},
                                             {"field": "money_growth", "type": "quantitative",
                                              "title": "money growth, % a year"},
                                             {"field": "inflation", "type": "quantitative",
                                              "title": "inflation, % a year"})}},
                {"transform": [{"filter": "datum.kind == 'slope'"}],
                 "mark": {"type": "line", "strokeWidth": 2},
                 "encoding": {"x": {"field": "money_growth", "type": "quantitative"},
                              "y": {"field": "inflation", "type": "quantitative"}}}]}}
    W.fig("fig-calm", rows, spec, source_note=f"IMF IFS, World Bank, ECB, FRED; First Thing calculations; {W.DERIVED}",
          title="The same calm decades, read against two kinds of money",
          measure="average inflation against average money growth, ten-year windows with both growths at or below "
                  f"{line}% a year", unit="% a year", period="ten-year windows ending 1970 to 2020, mostly since 1990",
          population=f"{r['moneys']} economies' calm decades", source="IMF International Financial Statistics (via "
          "DBnomics), World Bank, ECB, FRED; First Thing calculations", source_url=W.IMF_URL, licence=W.DERIVED,
          caption="Each line has the slope our regression found with output growth held fixed, drawn through the "
                  "points' averages; it is not the line through the dots alone.",
          alt="Two scatters of the same decades: against central-bank money the line is nearly flat; against the "
              "public's money it rises more.",
          description="The same calm decades twice: inflation against central-bank money growth on the left, "
                      "against the public's money growth on the right. The line on the right rises more steeply.",
          claims=["p2-2-base-against-broad"])


def door_timeline() -> None:
    """CS-C (C32): the monthly timeline, panels on separate scales, the web version stretched to March 2023."""
    r = load("C32-cs-c-door-timeline")
    m = {**r["timeline"]["monthly"], **r["stretch"]["monthly"]}
    q = {**r["timeline"]["quarterly"], **r["stretch"]["quarterly"]}

    def printing(period: str) -> str:
        for name, label in (("W1", "2008–14 printing"), ("W2", "2020–21 printing")):
            w = r["windows"][name]
            if w["start"] <= period[:7] <= w["end"]:
                return label
        return "between and after"

    def segment(period: str) -> str:
        # "between and after" is two stretches: the line breaks across the 2020-21 printing (the site, 2026-10-08)
        p = printing(period)
        return p if p != "between and after" else ("between" if period[:7] < r["windows"]["W2"]["start"] else "after")

    panels = [("1. Base money, $ trillion", "base_bn", 1 / 1000, m), ("2. Reserves, $ trillion", "reserves_bn",
                                                                       1 / 1000, m),
              ("3. The public's money (M2), growth over 12 months, %", "m2_yoy_pct", 1, m),
              ("5. Consumer prices, inflation over 12 months, %", "cpi_yoy_pct", 1, m),
              ("6. Unemployment, %", "unrate_pct", 1, m)]
    rows = []
    for name, col, k, src in panels:
        for per, v in src.items():
            if v.get(col) is not None:
                rows.append({"panel": name, "month": f"{per}-15", "value": round(float(v[col]) * k, 3),
                             "printing": printing(per), "segment": segment(per)})
    # v/u (Blanchard and Bernanke's files) is not drawn: their data are cited, never redistributed (MANIFEST; the
    # grid check of 2026-10-08, H)
    for name, col in (("4. Velocity of M2 (nominal GDP over M2)", "m2v"),):
        for per, v in q.items():
            if v.get(col) is not None:
                month = pd.Period(per, "Q").start_time + pd.offsets.Day(44)
                end = str(pd.Period(per, "Q").asfreq("M", "end"))
                rows.append({"panel": name, "month": str(month.date()), "value": round(float(v[col]), 3),
                             "printing": printing(end), "segment": segment(end)})
    rows.sort(key=lambda x: (x["panel"], x["month"]))
    acts = r["annotations"]["W2"] + r["annotations"]["stretch"]
    spec = {"height": 90,
            "facet": {"row": {"field": "panel", "type": "nominal", "title": None,
                              "header": {"labelAngle": 0, "labelAlign": "left", "labelAnchor": "start",
                                         "labelOrient": "top"}}},
            "resolve": {"scale": {"y": "independent"}},
            "spec": {"mark": {"type": "line", "strokeWidth": 1.5},
                     "encoding": {"x": {"field": "month", "type": "temporal", "title": None},
                                  "y": {"field": "value", "type": "quantitative", "title": None,
                                        "scale": {"zero": False}},
                                  "color": {"field": "printing", "type": "nominal",
                                            "legend": {"orient": "top", "title": None}},
                                  "detail": {"field": "segment"},
                                  "tooltip": tip({"field": "month", "type": "temporal", "format": "%b %Y"},
                                                 {"field": "panel", "type": "nominal"},
                                                 {"field": "value", "type": "quantitative", "format": ".2f"})}}}
    W.fig("fig-door", rows, spec, source_note="FRED (Board of Governors H.4.1 and H.6; BEA; BLS); First Thing "
          f"calculations; {W.FRED_LICENCE}",
          title="The modern Fed's two largest printings, month by month",
          measure="base money and reserves (H.4.1), M2 growth over 12 months, M2 velocity, CPI inflation over 12 "
                  "months, unemployment", unit="as named in each panel", period="August 2008 to March 2023",
          population="the United States", source="FRED (Board of Governors, BEA, BLS); First Thing calculations",
          source_url=W.FRED_URL, licence=W.FRED_LICENCE,
          highlight="2020–21 printing",
          caption="Each panel has its own scale. Acts named by the sources: " + "; ".join(
              f"{pd.Period(a['month'], 'M').strftime('%B %Y')}, {a['label']}" for a in acts)
          + ". In moderate inflations, monetary policy's peak effect on prices has come more than a year later "
            "(Batini and Nelson 2002).",
          alt="Six stacked panels from 2008 to 2023: base money and reserves jump in both printings; the public's "
              "money and prices rise only after 2020.",
          description="Month by month from August 2008 to March 2023: base money and bank reserves jump in both "
                      "printings; the growth of the public's money spikes in 2020 while its velocity falls; "
                      "velocity falls gradually through the first printing; inflation stays low then and rises "
                      "from 2021; unemployment jumps with the shutdowns of spring 2020 and falls as the economy "
                      "reopens.",
          claims=["p2-4-two-printings", "p2-4-money-held-2020", "p2-10-two-economies", "p2-10-shutdowns"])


def door_decomposition() -> None:
    """CS-C (C32 item 3 g): Blanchard & Bernanke's decomposition whole, as theirs, 2020Q1 to 2023Q1."""
    r = load("C32-cs-c-door-timeline")
    rows = []
    for qtr, v in r["decomposition"]["quarters"].items():
        for part in ("initial conditions", "v/u", "energy", "food", "shortages"):
            rows.append({"quarter": qtr, "part": part, "value": round(float(v[part]), 2), "kind": "bar"})
        rows.append({"quarter": qtr, "part": "actual inflation (theirs)", "value": round(float(v["actual"]), 2),
                     "kind": "line"})
    spec = {"height": 260,
            "layer": [
                {"transform": [{"filter": "datum.kind == 'bar'"}], "mark": {"type": "bar"},
                 "encoding": {"x": {"field": "quarter", "type": "ordinal", "title": None},
                              "y": {"field": "value", "type": "quantitative", "stack": "zero",
                                    "title": "CPI inflation, annualised quarterly log change, %"},
                              "color": {"field": "part", "type": "nominal", "legend": {"orient": "bottom",
                                                                                       "title": None}},
                              "tooltip": tip({"field": "quarter", "type": "ordinal"},
                                             {"field": "part", "type": "nominal"},
                                             {"field": "value", "type": "quantitative", "format": ".1f"})}},
                {"transform": [{"filter": "datum.kind == 'line'"}], "mark": {"type": "line", "point": True},
                 "encoding": {"x": {"field": "quarter", "type": "ordinal"},
                              "y": {"field": "value", "type": "quantitative"},
                              "tooltip": tip({"field": "quarter", "type": "ordinal"},
                                             {"field": "value", "type": "quantitative", "format": ".1f",
                                              "title": "actual inflation (theirs)"})}}]}
    W.fig("fig-decomposition", rows, spec, source_note="Blanchard and Bernanke (2023), NBER Working Paper 31417, "
          "replication output (all_data_decompositions.xls); cited as theirs",
          title="What Blanchard and Bernanke's model attributes US inflation to",
          measure="contributions to CPI inflation (annualised quarterly log change) in their model, and actual "
                  "inflation", unit="percentage points", period="2020Q1 to 2023Q1", population="the United States",
          source="Blanchard and Bernanke (2023), NBER Working Paper 31417, replication files",
          source_url="https://www.nber.org/papers/w31417",
          licence="the authors' public replication output, cited; their residuals omitted",
          caption=r["caption"],
          alt="Stacked bars by quarter from 2020 to 2023: energy and shortages carry most of the rise in 2021-22, "
              "job openings per unemployed person a growing share later.",
          description="Blanchard and Bernanke's model splits each quarter's inflation into initial conditions, "
                      "labour-market tightness, energy, food and shortages. Energy and shortages carry most of the "
                      "2021-22 rise; tightness grows later. Their model has no money variable.",
          claims=["k5-2021-23"])


def cross_section() -> None:
    """CS-E (C31): the main run's economies; the line drawn through the means with the card's Huber slope."""
    import cs_e as E  # noqa: PLC0415

    prm = yaml.safe_load((K.STUDY / "cards" / "C31-cs-e-pandemic-cross-section.yaml").read_text())["parameters"]
    r = load("C31-cs-e-pandemic-cross-section")
    d, _ = E.frame(prm, q6=False)
    main = d[(d.calm_mean < prm["calm_start_line_pct"]) & d.energy.notna()]
    assert len(main) == r["main"]["n"]
    nm = W.names()
    rows = [{"kind": "economy", "economy": nm.get(a, a), "money_growth": round(float(x.m), 2),
             "inflation": round(float(x.p), 2)} for a, x in main.iterrows()]
    mx, my, b = float(main.m.mean()), float(main.p.mean()), r["main"]["huber"]
    for x in (float(main.m.min()), float(main.m.max())):
        rows.append({"kind": "slope", "economy": "", "money_growth": round(x, 2), "inflation": round(my + b * (x - mx),
                                                                                                   2)})
    spec = {"height": 300,
            "layer": [
                {"transform": [{"filter": "datum.kind == 'economy'"}],
                 "mark": {"type": "point", "filled": True, "size": 30, "opacity": 0.7},
                 "encoding": {"x": {"field": "money_growth", "type": "quantitative",
                                    "title": "broad money growth a year, Dec 2019 to Dec 2021 (log %)"},
                              "y": {"field": "inflation", "type": "quantitative",
                                    "title": "inflation a year, Dec 2021 to Dec 2023 (log %)"},
                              "tooltip": tip({"field": "economy", "type": "nominal"},
                                             {"field": "money_growth", "type": "quantitative", "format": ".1f"},
                                             {"field": "inflation", "type": "quantitative", "format": ".1f"})}},
                {"transform": [{"filter": "datum.kind == 'slope'"}], "mark": {"type": "line", "strokeWidth": 2},
                 "encoding": {"x": {"field": "money_growth", "type": "quantitative"},
                              "y": {"field": "inflation", "type": "quantitative"}}}]}
    W.fig("fig-cross-section", rows, spec, source_note="IMF International Financial Statistics (via DBnomics), ECB, "
          f"World Bank (energy imports, 2019); First Thing calculations; {W.DERIVED}",
          title="Money in 2020-21 and prices in 2022-23, economy by economy",
          measure="broad money growth, December 2019 to December 2021, against inflation, December 2021 to December "
                  "2023, both a year, in logs", unit="% a year", period="December 2019 to December 2023",
          population="economies whose 2015-19 inflation averaged below 10% a year, those with 2019 energy-import data",
          source="IMF International Financial Statistics (via DBnomics), ECB, World Bank; First Thing calculations",
          source_url=W.IMF_URL, licence=W.DERIVED,
          caption="The line has our robust slope with the energy-import share held fixed, drawn through the points' "
                  "averages. It cannot separate the money from the fiscal demand that carried it.",
          alt="A cloud of economies rising gently from left to right, with a line through it.",
          description="Each dot is an economy that started calm: its broad money growth over 2020-21 against its "
                      "inflation over 2022-23. Economies whose money grew faster tended to have more inflation "
                      "later; the line shows the robust slope.",
          claims=["p2-5-cross-section"])


GLOSSARY = {
    "printing": {"term": "printing money", "short": "A central bank creating new money of its own, today almost "
                 "always by buying bonds and paying with bank reserves, not by printing notes.",
                 "example": "When the Federal Reserve buys a Treasury bond from a pension fund, it credits the "
                            "fund's bank with new reserves and the bank credits the fund's account.",
                 "first_use_only": True},
    "base-money": W.GLOSSARY["base-money"],
    "reserves": W.GLOSSARY["reserves"],
    "broad-money": {"term": "broad money", "short": "The money the public holds: cash and bank deposits of "
                    "households, firms and financial firms (M2 in the United States).",
                    "long": "Most of it is deposits. Banks create them when they lend, and when a bank or the central "
                            "bank buys an asset from someone outside the banks.",
                    "example": "Your current account balance is broad money; your bank's reserves are not.",
                    "first_use_only": True},
    "velocity": W.GLOSSARY["velocity"],
    "quantity-equation": {"term": "quantity equation", "short": "Money times velocity equals nominal spending: if "
                          "money grows and velocity holds, spending grows; if velocity falls, the money is held.",
                          "example": "In 2020 the public's money jumped while velocity fell: the new money was held.",
                          "first_use_only": True},
    "qe": {"term": "quantitative easing", "short": "Large central-bank purchases of bonds, paid for with new "
           "reserves, to lower long-term interest rates when the short rate is near zero.",
           "example": "The Federal Reserve's purchases from 2008 and from 2020.", "first_use_only": True},
    "interest-on-reserves": {"term": "interest on reserves", "short": "The rate a central bank pays banks on the "
                             "reserves they hold with it; it makes reserves a close substitute for short bills.",
                             "example": "The Federal Reserve has paid it since October 2008.",
                             "first_use_only": True},
    "seigniorage": {"term": "seigniorage", "short": "What the state gains from issuing money that costs it almost "
                    "nothing to create.", "example": "The central bank's profit on the bonds it holds against notes "
                    "that pay no interest goes to the state.", "first_use_only": True},
    "inflation-tax": {"term": "inflation tax", "short": "The loss of purchasing power on central-bank money that "
                      "inflation causes; its gain goes to the state.",
                      "example": "A banknote loses a fifth of its purchasing power when prices rise by a quarter.",
                      "first_use_only": True},
    "size-that-matters": {"term": "size that matters", "short": "The smallest effect a reasonable reader would act "
                          "on, fixed before we ran the test.", "example": "A tenth of a point of inflation per "
                          "point of money growth: at 2020-21's pace of broad money, two points of inflation a year.",
                          "first_use_only": True},
}


def meta_and_glossary() -> None:
    meta = {"id": "FT-001", "slug": W.SLUG, "title": TITLE, "standfirst": STANDFIRST,
            "series": "The life of a money", "part": 2, "as_of": W.AS_OF, "subscriber_at": "2026-12-31",
            "public_at": "2026-12-31", "cut_after": "short-answer", "methods_url": W.METHODS,
            "reading_minutes": 18,
            "og_alt": "US bank reserves and currency since 2007: reserves jump in 2008-14 and again in 2020-21.",
            "updated": W.AS_OF, "changelog": [], "topics": ["money", "inflation", "central banks"],
            "literals": ["M1", "M2", "H.4.1", "COVID-19"], "test": True}
    path = OUT / "meta.json"
    if path.exists():
        old = json.loads(path.read_text())
        for k in ("methods_url",):
            if k in old:
                meta[k] = old[k]
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    (OUT / "glossary.json").write_text(json.dumps(GLOSSARY, indent=2, ensure_ascii=False) + "\n")


def og() -> None:
    """The share picture: the open figure (reserves and currency), nothing from after the cut."""
    import vl_convert as vlc
    from PIL import Image

    spec = json.loads((OUT / "figures" / "fig-base-now" / "spec.vl.json").read_text())
    data = pd.read_csv(OUT / "figures" / "fig-base-now" / "data.csv", comment="#").to_dict("records")
    spec.update(data={"values": data}, width=1080, height=420,
                title={"text": TITLE, "fontSize": 30, "font": "serif", "anchor": "start", "color": "#1c1c1a"},
                background="#f7f5ef", padding=30)
    spec["encoding"]["color"]["scale"] = {"range": ["#2f6b3a", "#9a978c"]}
    im = Image.open(io.BytesIO(vlc.vegalite_to_png(spec, scale=1))).convert("RGB")
    canvas = Image.new("RGB", (1200, 630), (247, 245, 239))
    im.thumbnail((1200, 630))
    canvas.paste(im, ((1200 - im.width) // 2, (630 - im.height) // 2))
    canvas.save(OUT / "og.png", optimize=True)


def tag(fid: str, claims: list[str]) -> None:
    """A figure drawn by round 1's helper takes the claims its alt text states (its ``figure.json``)."""
    f = OUT / "figures" / fid / "figure.json"
    f.write_text(json.dumps(dict(json.loads(f.read_text()), claims=claims), indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    R = W.reg()
    for sub in ("figures", "interactives"):
        if (OUT / sub).exists():
            shutil.rmtree(OUT / sub)  # rebuilt from the runs each time (generated)
    OUT.mkdir(parents=True, exist_ok=True)
    W.base_now()
    longrun(R)
    bands(R)
    calm()
    door_timeline()
    # door_decomposition(): Blanchard and Bernanke's data are cited, never redistributed (the package's MANIFEST;
    # the grid check of 2026-10-08, H)
    cross_section()
    W.calculator(R)
    tag("fig-base-now", ["p2-4-two-printings", "p2-6-reserves"])
    meta_and_glossary()
    og()


if __name__ == "__main__":
    main()
