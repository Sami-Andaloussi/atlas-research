"""The web study's folder for map v11 (round 2; BLUEPRINT §5 w): ``web/site/<slug>/`` with ``meta.json``,
``glossary.json``, every figure of map v11's web plan (§12; a Vega-Lite spec reading its ``data.csv``), the
purchasing-power calculator by regime and ``og.png``. ``run.py`` calls :func:`main` in place of round 1's ``web.main``;
``toolkit/bin/ft study web`` then renders the article and the numbers into the same folder.

Everything is drawn from the cards' stored runs (C16, C18, C20; reused: A3's build, frame a's window build, C14) and
the registry; nothing is recomputed and no explorer shows a variant no card ran. Round 1's helpers (``web.fig``,
``web.door``, ``web.greenbacks``) are reused where the new engine would draw the same: CS-C's two series read the same
A3 build. K5's table is written in the article as a list (the site's markdown has no tables; map v11 §12 allows a
plain table), so it reads without JavaScript.
"""

from __future__ import annotations

import io
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import web as W  # noqa: E402

from ft import numbers  # noqa: E402

AS_OF = "2026-10-08"
W.AS_OF = AS_OF  # the figures carry the date the study's facts were read (round 1's helper reads this global)
OUT = W.OUT
STUDY = W.STUDY
RUNS = STUDY / "results" / "runs"
TITLE = "Does a money lose its value when its backing goes?"
STANDFIRST = ("Monies with nothing behind them have had more inflation, but a backing is neither necessary nor a "
              "guarantee: unbacked monies have run for decades without collapsing, a dollar convertible into gold at "
              "home lost half its purchasing power in six years, and land stood behind both a money that collapsed and one that held.")
BJ = ("Bernanke and James (1991), 'The Gold Standard, Deflation, and Financial Crisis in the Great Depression', NBER "
      "chapter, Table 2.2")
BJ_21 = BJ.replace("Table 2.2", "Table 2.1")
BJ_URL = "https://www.nber.org/system/files/chapters/c11482/c11482.pdf"
JST = "Jorda, Schularick and Taylor, Macrohistory Database, release 6"
JST_URL = "https://www.macrohistory.net/database/"
DERIVED = W.DERIVED
tip = W.tip


def load(card: str) -> dict:
    return json.loads((RUNS / f"{card}.json").read_text())["result"]


def tag(fid: str, claims: list[str]) -> None:
    """A figure drawn by round 1's helper takes the claims its alt text states (its ``figure.json``)."""
    f = OUT / "figures" / fid / "figure.json"
    f.write_text(json.dumps(dict(json.loads(f.read_text()), claims=claims), indent=2, ensure_ascii=False) + "\n")


# --- the open figure: the 1930s, as Bernanke and James give it -------------------------------------------------

def wholesale_1930s(R: numbers.Registry) -> None:
    rows = []
    for y in (1932, 1933, 1934, 1935):
        rows.append({"year": y, "group": "had left gold", "change": W.v(R, f"bj_off_{y}", 1)})
        rows.append({"year": y, "group": "still on gold", "change": W.v(R, f"bj_gold_{y}", 1)})
    spec = {"height": 260,
            "layer": [
                {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 0}}},
                {"mark": {"type": "line", "point": True},
                 "encoding": {"x": {"field": "year", "type": "ordinal", "title": None, "axis": {"labelAngle": 0}},
                              "y": {"field": "change", "type": "quantitative",
                                    "title": "wholesale prices, change over the year, %"},
                              "color": {"field": "group", "type": "nominal",
                                        "legend": {"orient": "bottom", "title": None}},
                              "tooltip": tip({"field": "year", "type": "ordinal"},
                                             {"field": "group", "type": "nominal"},
                                             {"field": "change", "type": "quantitative",
                                              "title": "change in wholesale prices, %"})}}]}
    W.fig("fig-1930s", rows, spec, source_note=f"quoted from {BJ}, p. 43",
          title="Wholesale prices in the 1930s: countries that had left gold against those still on it",
          measure="average change in wholesale prices over the year (log change, in percent), as Bernanke and "
                  "James give it", unit="% a year", period="1932 to 1935",
          population="Bernanke and James's 24 economies, each year off or on gold by their dates (exchange controls "
                     "count as leaving)",
          source=BJ, source_url=BJ_URL,
          licence="quoted from Bernanke and James (1991), Table 2.2, p. 43",
          highlight="had left gold",
          caption="Wholesale prices, as the source measures them; the dashed line is no change. Consumer prices, "
                  "which tell what a money buys in the shops, are in the case study on leaving gold.",
          alt="Two lines from 1932 to 1935: prices in the countries off gold stop falling by 1933 and rise after, "
              "while those still on gold keep falling.",
          description="The average yearly change in wholesale prices, as Bernanke and James publish it, for the "
                      "economies that had left gold and those still on it. In 1932 the stayers' prices fell much "
                      "faster; from 1933 the leavers' prices stopped falling and then rose, while the stayers' kept "
                      "falling.",
          claims=["door-1931", "p1-1-1930s"])


# --- the case studies ------------------------------------------------------------------------------------------

def cs_a(R: numbers.Registry) -> None:
    """CS-A (C18): consumer prices off less on gold by year, 1931-34, and the pooled 1932-34 range. 1930 and
    1935-36 are left out (a group of two or three economies comes close to one economy's JST value), and Bernanke and
    James's wholesale gap with them, so the figure is ours alone (the engine's decision, 2026-10-09)."""
    r = load("C18-cs-a-consumer-prices-off-gold")["main"]
    rows = [{"year": int(y), "series": "consumer prices (ours)", "gap": round(float(g), 1), "low": None,
             "high": None} for y, g in sorted(r["by_year"].items()) if 1931 <= int(y) <= 1934]
    rows += [{"year": y, "series": "1932 to 1934 pooled, with its range", "gap": round(r["pooled"], 1),
              "low": round(r["lo"], 1), "high": round(r["hi"], 1)} for y in (1932, 1934)]
    pts = {"filter": "datum.series != '1932 to 1934 pooled, with its range'"}
    band = {"filter": "datum.series == '1932 to 1934 pooled, with its range'"}
    x = {"field": "year", "type": "quantitative", "title": None, "axis": {"format": "d", "tickMinStep": 1},
         "scale": {"domain": [1931, 1934]}}
    spec = {"height": 280,
            "layer": [
                {"transform": [band], "mark": {"type": "area", "opacity": 0.25},
                 "encoding": {"x": x, "y": {"field": "low", "type": "quantitative"}, "y2": {"field": "high"}}},
                {"transform": [band], "mark": {"type": "line", "strokeDash": [4, 3]},
                 "encoding": {"x": x, "y": {"field": "gap", "type": "quantitative"}}},
                {"mark": {"type": "rule", "strokeDash": [2, 2]}, "encoding": {"y": {"datum": 0}}},
                {"transform": [pts], "mark": {"type": "line", "point": True},
                 "encoding": {"x": x,
                              "y": {"field": "gap", "type": "quantitative",
                                    "title": "inflation off gold less on gold, points a year"},
                              "color": {"field": "series", "type": "nominal",
                                        "legend": {"orient": "bottom", "title": None}},
                              "tooltip": tip({"field": "year", "type": "quantitative", "format": "d"},
                                             {"field": "series", "type": "nominal"},
                                             {"field": "gap", "type": "quantitative", "title": "points a year"})}}]}
    W.fig("fig-cs-a", rows, spec, source_note=f"{JST} (consumer prices); {BJ_21} (the dates each economy left "
          f"gold); First Thing calculations; {DERIVED}",
          title="Leaving gold in the 1930s: consumer prices off gold against those still on it",
          measure="average consumer-price inflation in the economies off gold less the economies on gold, by year",
          unit="points of inflation a year", period="1931 to 1934; read pooled over 1932 to 1934",
          population="the 15 economies of Bernanke and James's list that the Macrohistory Database covers, off or "
                     "on gold by their dates",
          source=f"{JST}; {BJ_21}; First Thing calculations", source_url=JST_URL, licence=DERIVED,
          highlight="consumer prices (ours)",
          caption="The shaded band is the range of the pooled 1932 to 1934 gap: it holds zero. 1931 is shown, never "
                  "read; from 1935 too few economies were still on gold to show a gap.",
          alt="By year from 1931 to 1934, the consumer-price gap sits above zero, inside a wide shaded band.",
          description="For each year from 1931 to 1934, consumer-price inflation in the economies off gold less those on "
                      "gold. The gap is a few points, and the pooled 1932 to 1934 range runs from below zero to about "
                      "ten points; Bernanke and James's wholesale prices are in the figure on the 1930s above.",
          claims=["p1-2-cs-a"])


def all_monies(R: numbers.Registry) -> None:
    """Fischer, Sahay & Vegh's distribution, titled as all monies, pegged or not (map v11 §12, [k-C2])."""
    n = int(R.get("fsv_economies")["value"])
    rows = [{"line": f"above {k}% a year", "order": i, "economies": int(R.get(key)["value"]),
             "share": round(100 * R.get(key)["value"] / n)}
            for i, (k, key) in enumerate(((25, "fsv_above25"), (50, "fsv_above50"), (100, "fsv_above100")))]
    spec = {"height": 150, "mark": {"type": "bar"},
            "encoding": {"y": {"field": "line", "type": "nominal", "sort": {"field": "order"}, "title": None},
                         "x": {"field": "economies", "type": "quantitative",
                               "title": f"market economies, of {n}, whose inflation passed the line at some point"},
                         "tooltip": tip({"field": "line", "type": "nominal", "title": "inflation"},
                                        {"field": "economies", "type": "quantitative"},
                                        {"field": "share", "type": "quantitative", "title": "% of the economies"})}}
    W.fig("fig-all-monies", rows, spec,
          source_note="quoted from Fischer, Sahay and Vegh (2002), NBER Working Paper 8930, p. 7",
          title="Every money, pegged or not: how many economies passed each inflation line, 1960 to 1996",
          measure="market economies whose inflation passed each line at some point", unit="economies",
          period="1960 to 1996", population="133 market economies, all monies, pegged or not",
          source="Fischer, Sahay and Vegh (2002), 'Modern Hyper- and High Inflations', NBER Working Paper 8930",
          source_url="https://www.nber.org/papers/w8930",
          licence="quoted from Fischer, Sahay and Vegh (2002), NBER Working Paper 8930, p. 7",
          caption="All monies, pegged or not: the source classes no regime. Most countries, most of the time, stayed "
                  "below the first line.",
          alt="Three bars: most economies passed 25% a year at some point, fewer passed 50%, and about one in five "
              "passed 100%.",
          description="Of 133 market economies in 1960 to 1996, the number whose inflation passed 25%, 50% and 100% a "
                      "year at some point. The source does not class them by backing or peg.",
          claims=["p1-4-all-monies"])


def cs_b() -> None:
    """CS-B (C20): average inflation by convertibility and era; the Bretton Woods years beside."""
    r = load("C20-cs-b-without-hyperinflation-years")
    rows = [{"era": "all years, 1870-2020", "order": 0, "class": c, "mean": round(r["main"][k]["mean"], 2),
             "years": r["main"][k]["n"]}
            for c, k in (("convertible into gold", "convertible"), ("inconvertible", "fiat"))]
    for i, era in enumerate(("1870-1913", "1919-1938", "1972-2020"), start=1):
        for c, k in (("convertible into gold", "convertible"), ("inconvertible", "fiat")):
            e = r["eras"][era][k]
            if e.get("n") and e.get("mean") is not None:
                rows.append({"era": era, "order": i, "class": c, "mean": round(e["mean"], 2), "years": e["n"]})
    bw = round(r["by_class"]["bretton_woods"]["mean"], 2)
    rows.append({"era": "Bretton Woods years, 1946 to 1971", "order": 4, "class": "Bretton Woods", "mean": bw,
                 "years": r["by_class"]["bretton_woods"]["n"]})
    spec = {"height": 260, "mark": {"type": "bar"},
            "encoding": {"x": {"field": "era", "type": "nominal", "title": None,
                               "sort": ["all years, 1870-2020", "1870-1913", "1919-1938", "1972-2020",
                                        "Bretton Woods years, 1946 to 1971"],
                               "axis": {"labelAngle": 0, "labelLimit": 120}},
                         "xOffset": {"field": "class", "type": "nominal"},
                         "y": {"field": "mean", "type": "quantitative", "title": "average inflation, % a year"},
                         "color": {"field": "class", "type": "nominal", "legend": {"orient": "bottom", "title": None}},
                         "tooltip": tip({"field": "era", "type": "nominal"}, {"field": "class", "type": "nominal"},
                                        {"field": "mean", "type": "quantitative", "format": ".1f",
                                         "title": "average inflation, % a year"},
                                        {"field": "years", "type": "quantitative", "title": "economy-years"})}}
    W.fig("fig-cs-b", rows, spec, source_note=f"{JST} (consumer prices); Bordo and Schwartz (1994), NBER Working Paper "
          f"4860, Table 1A (convertibility dates); First Thing calculations; {DERIVED}",
          title="Inflation in years a money was convertible into gold, and years it was not",
          measure="average consumer-price inflation by class (convertible into gold or inconvertible, by Bordo and "
                  "Schwartz's dates) and calendar era, war years apart, the economy-years above 100% set apart",
          unit="% a year", period="1870 to 2020", population="17 rich economies of the Macrohistory Database",
          source=f"{JST}; Bordo and Schwartz (1994); First Thing calculations", source_url=JST_URL, licence=DERIVED,
          highlight="inconvertible",
          caption="No economy was convertible after 1972, so that era has one bar. The Bretton Woods years, tied to "
                  "a dollar convertible for central banks only, are shown apart.",
          alt="Bars by era: before 1914 both classes near zero; between the wars inconvertible years above, "
              "convertible below zero; since 1972 inconvertible years at a few points.",
          description="Average inflation in years each money was convertible into gold and years it was not, over "
                      "all years and by era. Before 1914 the two are about the same; the gap comes from the interwar "
                      "years and the float since 1972.",
          claims=["p1-7-cs-b", "p1-7-cs-b-eras"])


def calculator(R: numbers.Registry) -> None:
    """What a sum buys after some years at each class's average inflation (C20's means; no new number)."""
    d = OUT / "interactives" / "calc-regime"
    d.mkdir(parents=True, exist_ok=True)
    conv = round(R.get("c20_convertible_mean")["value"] / 100, 5)
    fiat = round(R.get("c20_fiat_mean")["value"] / 100, 5)
    flt = round(R.get("c20_era_1972_2020_fiat")["value"] / 100, 5)
    config = {"component": "ft-calc", "version": 1,
              "title": "What a sum buys after some years, at each regime's average inflation",
              "source": "First Thing calculations on the Macrohistory Database (17 rich economies, 1870-2020), each "
                        "year classed by Bordo and Schwartz's convertibility dates; war years and Bretton Woods apart",
              "intro": "Type a sum and a number of years. The calculator applies, year after year, the average "
                       "inflation of the convertible years, of the inconvertible years, and of the float since 1972.",
              "settings": {
                  "inputs": [
                      {"name": "amount", "label": "Sum held, in any money", "min": 0, "max": 100000000,
                       "default": 100, "format": {"decimals": 0}},
                      {"name": "years", "label": "Years held", "min": 0, "max": 100, "default": 30,
                       "format": {"decimals": 0}}],
                  "constants": {"conv": conv, "fiat": fiat, "flt": flt},
                  "outputs": [
                      {"label": "What it buys at the convertible years' average", "expr":
                       "amount / pow(1 + conv, years)", "format": {"decimals": 0}},
                      {"label": "At the inconvertible years' average", "expr": "amount / pow(1 + fiat, years)",
                       "format": {"decimals": 0}},
                      {"label": "At the float's average since 1972", "expr": "amount / pow(1 + flt, years)",
                       "format": {"decimals": 0},
                       "note": "In today's prices of the start. An average across 17 economies and many years: no "
                               "money followed it exactly, and it is no forecast."}]}}
    (d / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    buys = lambda a, r, y: a / (1 + r) ** y  # noqa: E731
    tests = [{"inputs": {"amount": 100, "years": 30}, "outputs": [buys(100, conv, 30), buys(100, fiat, 30),
                                                                  buys(100, flt, 30)]},
             {"inputs": {"amount": 0, "years": 30}, "outputs": [0, 0, 0]},
             {"inputs": {"amount": 250, "years": 0}, "outputs": [250, 250, 250]}]
    (d / "tests.json").write_text(json.dumps(tests, indent=2) + "\n")


def cs_d(R: numbers.Registry) -> None:
    """CS-D (C16): the like-for-like ratio by reading, against the band of what matters (log scale)."""
    r = load("C16-cs-d-default-ratio")["readings"]
    m = R.get("cs_d_ratio")["matters"]
    names = (("headline", "every crisis counted", 0), ("shared_once", "a shared money counted once", 1),
             ("T2-var-private", "private creditors' arrears only", 2))
    rows = [{"reading": name, "order": i, "ratio": round(r[k]["ratio"], 2),
             "low": round(r[k]["interval"]["lo"], 2), "high": round(r[k]["interval"]["hi"], 2),
             # the log axis starts at 0.2: a range reaching lower is drawn from the axis, its true end kept in the
             # data and the tooltip (the grid checks of 2026-10-08)
             "low_drawn": round(max(r[k]["interval"]["lo"], 0.2), 2),
             "crises_after": r[k]["after"], "crises_read": r[k]["readable"]} for k, name, i in names]
    y = {"field": "reading", "type": "nominal", "sort": {"field": "order"}, "title": None,
         "axis": {"labelLimit": 220}}
    xs = {"type": "log", "domain": [0.2, 3]}
    spec = {"height": 170,
            "layer": [
                {"mark": {"type": "rect", "opacity": 0.15},
                 "encoding": {"x": {"datum": round(1 / m, 3), "type": "quantitative", "scale": xs},
                              "x2": {"datum": m}}},
                {"mark": {"type": "rule", "strokeDash": [4, 3]},
                 "encoding": {"x": {"datum": 1, "type": "quantitative", "scale": xs}}},
                {"mark": {"type": "rule", "strokeWidth": 3},
                 "encoding": {"y": y, "x": {"field": "low_drawn", "type": "quantitative", "scale": xs,
                                            "title": "times as often (log scale)"},
                              "x2": {"field": "high"}}},
                {"mark": {"type": "point", "filled": True, "size": 70},
                 "encoding": {"y": y, "x": {"field": "ratio", "type": "quantitative", "scale": xs},
                              "tooltip": tip({"field": "reading", "type": "nominal"},
                                             {"field": "ratio", "type": "quantitative", "title": "times as often"},
                                             {"field": "low", "type": "quantitative", "title": "range from"},
                                             {"field": "high", "type": "quantitative", "title": "to"},
                                             {"field": "crises_after", "type": "quantitative",
                                              "title": "crises after a default"},
                                             {"field": "crises_read", "type": "quantitative",
                                              "title": "crises that can be read"})}}]}
    W.fig("fig-cs-d", rows, spec, source_note="the Bank of Canada-Bank of England sovereign default database; IMF IFS, "
          f"World Bank, Macrohistory Database, Reinhart and Rogoff; First Thing calculations; {DERIVED}",
          title="A default before a money crisis, against strained years in which the money held",
          measure="share of money crises with a creditor class newly in arrears in the three years before, over the same "
                  "share among strained years that held, with its 95% range", unit="times as often",
          period="1970 to the sources' common end",
          population="money crises and strained years drawn from the same spells of fiscal stress",
          source="Bank of Canada-Bank of England sovereign default database; IMF; World Bank; Macrohistory Database; "
                 "Reinhart and Rogoff; First Thing calculations",
          source_url="https://www.bankofcanada.ca/2025/10/staff-analytical-note-2025-24/", licence=DERIVED,
          caption="Dot: the ratio; bar: its range; dashed line: as often; shaded: closer to as often than the size "
                  "that matters, half as often again either way. Every range holds the dashed line and reaches past "
                  "the shaded band.",
          alt="Three dots with long bars on a log scale, each bar crossing the dashed line at one and reaching past "
              "the shaded band.",
          description="For three ways of counting, how many times as often a newly missed payment came before a money "
                      "crisis as before a strained year in which the money held. Each ratio is near one and each "
                      "range runs from below one to past the band of what matters.",
          claims=["p1-6-cs-d"])


def cs_f(R: numbers.Registry) -> None:
    """CS-F (frame a's window build, A2 panels 3-4, the two claim P1-9 states): each gap inside its band."""
    groups = (("p3u", "central bank made independent"), ("p4", "inflation target adopted"))
    rows = [{"change": name, "gap": W.v(R, f"a2_{k}_mean"), "low": W.v(R, f"a2_{k}_band_lo"),
             "high": W.v(R, f"a2_{k}_band_hi"), "changes": int(R.get(f"a2_{k}_n")["value"])} for k, name in groups]
    y = {"field": "change", "type": "nominal", "sort": None, "title": None, "axis": {"labelLimit": 220}}
    spec = {"height": 130,
            "layer": [
                {"mark": {"type": "rule", "strokeWidth": 6, "opacity": 0.35},
                 "encoding": {"y": y, "x": {"field": "low", "type": "quantitative",
                                            "title": "change in inflation against matched monies, points a year"},
                              "x2": {"field": "high"}}},
                {"mark": {"type": "point", "filled": True, "size": 70},
                 "encoding": {"y": y, "x": {"field": "gap", "type": "quantitative"},
                              "tooltip": tip({"field": "change", "type": "nominal"},
                                             {"field": "gap", "type": "quantitative", "title": "mean gap, points"},
                                             {"field": "low", "type": "quantitative", "title": "chance's band, from"},
                                             {"field": "high", "type": "quantitative", "title": "to"},
                                             {"field": "changes", "type": "quantitative", "title": "changes"})}},
                {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"x": {"datum": 0}}}]}
    W.fig("fig-reforms", rows, spec, source_note=f"Garriga (2025); Hammond (2012) and the IMF's AREAER; IMF IFS, World "
          f"Bank, Reinhart and Rogoff; First Thing calculations; {DERIVED}",
          title="After independence or an inflation target: inflation's change against matched monies",
          measure="inflation's change over the five years after the reform less the year before, minus the same in "
                  "matched monies; the bar is the band that scenarios with no effect give", unit="points a year",
          period="reforms since 1970, five years either side", population="every reform in each group with a "
          "matched money that did not change", source="Garriga (2025); Hammond (2012); IMF; World Bank; Reinhart and "
          "Rogoff; First Thing calculations", source_url="https://db.nomics.world/IMF/IFS", licence=DERIVED,
          caption="Dot: the mean gap; bar: the band a reform with no effect gives at that number of reforms. Both dots "
                  "sit inside their bands, which run two to four points either side of zero.",
          alt="Two dots, each inside a wide bar that spans zero.",
          description="For central banks made independent and for inflation targets adopted, the mean change in "
                      "inflation against matched monies, inside the band that scenarios with no effect give. Both "
                      "lie inside; the bands run several points either side of zero.",
          claims=["p1-9-cs-f"])


def cs_e(R: numbers.Registry) -> None:
    """CS-E (C14, reused): who may redeem each stablecoin, as its issuer's documents say."""
    coins = int(R.get("c4_coins")["value"])
    rows = [{"who": "only verified customers", "order": 0, "coins": int(R.get("c4_redeem_account")["value"])},
            {"who": "any holder", "order": 1, "coins": int(R.get("c4_redeem_any")["value"])},
            {"who": "not settled by the documents", "order": 2, "coins": int(R.get("c4_redeem_unsettled")["value"])},
            {"who": "no right to redeem that can be read", "order": 3,
             "coins": coins - int(R.get("c4_redeem_yes")["value"])}]
    spec = {"height": 170, "mark": {"type": "bar"},
            "encoding": {"y": {"field": "who", "type": "nominal", "sort": {"field": "order"}, "title": None,
                               "axis": {"labelLimit": 220}},
                         "x": {"field": "coins", "type": "quantitative", "title": f"stablecoins, of {coins}"},
                         "tooltip": tip({"field": "who", "type": "nominal", "title": "who may redeem"},
                                        {"field": "coins", "type": "quantitative"})}}
    W.fig("fig-coins", rows, spec, source_note=f"BIS, Federal Reserve, New York Fed and NBER papers (the coins); the "
          f"issuers' documents (Internet Archive, New York DFS); First Thing's coding; {DERIVED}",
          title="Who may redeem a stablecoin, as its issuer's documents say",
          measure="who may redeem each coin for its reference asset, read in its issuer's documents under a rule "
                  "fixed in advance", unit="stablecoins", period="the documents as frozen in 2026",
          population="every stablecoin named in a fixed set of central-bank and academic papers",
          source="BIS, Federal Reserve and NBER papers; the issuers' documents; First Thing's coding",
          source_url="https://www.bis.org/publ/bppdf/bispap141.pdf", licence=DERIVED,
          highlight="only verified customers",
          caption="Of the coins whose documents state who may redeem, most allow only verified customers; for most "
                  "coins no right to redeem can be read.",
          alt="Four bars: the longest, coins with no readable right to redeem; then verified customers only; then any "
              "holder; one not settled.",
          description="For each stablecoin in a fixed set, who may redeem it as its issuer's documents say: verified "
                      "customers only, any holder, not settled, or no right that can be read.",
          claims=["p1-10-cs-e"])


# --- glossary, meta, og.png -------------------------------------------------------------------------------------

GLOSSARY = {
    "backing": {"term": "backing", "short": "A claim on a stated asset at a fixed rate that the issuer promises to "
                "honour: gold, land, another money, or a token.",
                "long": "A backing says who may redeem the money, into what, and at what rate. It is not the same as "
                        "the asset the issuer happens to hold.",
                "example": "Before 1914 a pound note could be taken to the Bank of England and exchanged for a fixed "
                           "weight of gold.", "first_use_only": True},
    "convertible": {"term": "convertible", "short": "Said of a money its issuer exchanges for its backing at the "
                    "fixed rate, on demand.", "example": "The dollar was convertible into gold for anyone at home "
                    "until 1933, and for foreign central banks until 1971.", "first_use_only": True},
    "redeem": {"term": "redeem", "short": "To hand a money back to its issuer and receive the backing it promises.",
               "example": "Redeeming a stablecoin means its issuer pays you dollars for it.",
               "first_use_only": True},
    "suspension": {"term": "suspension", "short": "A pause in convertibility: the issuer stops paying out its "
                   "backing, often with a promise to resume.",
                   "example": "In 1797 the Bank of England stopped paying gold for its notes; it paid again from "
                              "1821.", "first_use_only": True},
    "fiat": {"term": "fiat money", "short": "Money its issuer does not promise to exchange for anything: it is "
             "worth what it buys.", "example": "The dollar, the euro and the pound today.", "first_use_only": True},
    "legal-tender": {"term": "legal tender", "short": "Money a creditor must accept in payment of a debt, by law.",
                     "example": "Euro banknotes are legal tender in the euro area.", "first_use_only": True},
    "currency-board": {"term": "currency board", "short": "An issuer bound by law to exchange its money for a "
                       "foreign one at a fixed rate, holding that foreign money against what it issues.",
                       "example": "Hong Kong's dollar has been tied to the US dollar this way since 1983.",
                       "first_use_only": True},
    "stablecoin": {"term": "stablecoin", "short": "A token on a blockchain whose issuer promises a fixed value, most "
                   "often one dollar.", "example": "A dollar stablecoin whose terms let verified customers redeem "
                   "it at one dollar.", "first_use_only": True},
    "default": {"term": "default", "short": "Here, a class of the state's creditors newly left unpaid, as the Bank "
                "of Canada and Bank of England's database dates it.",
                "long": "A state may already be in default with some creditors when another class goes unpaid; we "
                        "count each newly unpaid class.",
                "example": "A state that stops paying its bondholders while it keeps paying the IMF.",
                "first_use_only": True},
    "collapse": {"term": "collapse", "short": "Here, prices in a money more than doubling within twelve months, the "
                 "line Fischer, Sahay and Vegh call very high inflation.",
                 "long": "For a token priced in dollars, its price falling below half within twelve months; where a "
                         "source gives only the value in coin, that measure is named.",
                 "example": "A money whose prices more than double within a year has collapsed.",
                 "first_use_only": True},
    "wholesale-prices": {"term": "wholesale prices", "short": "Prices of goods traded in bulk between firms, "
                         "heavy in raw materials, which move with world prices faster than shop prices.",
                         "example": "The price of a ton of wheat or copper, rather than of a loaf of bread.",
                         "first_use_only": True},
    "size-that-matters": {"term": "size that matters", "short": "The smallest effect a reasonable reader would act "
                          "on, fixed before we read the result, or said where it was set after.",
                          "example": "One point of inflation a year.", "first_use_only": True},
}


def meta_and_glossary() -> None:
    meta = {"id": "FT-001", "slug": W.SLUG, "title": TITLE, "standfirst": STANDFIRST,
            "series": "The life of a money", "part": 1, "as_of": AS_OF, "subscriber_at": "2026-12-31",
            "public_at": "2026-12-31", "cut_after": "short-answer", "methods_url": W.METHODS,
            "reading_minutes": 20,
            "og_alt": "Wholesale prices in the 1930s: in the countries that had left gold they stopped falling by "
                      "1933, while those still on gold kept falling.",
            "updated": AS_OF, "changelog": [], "topics": ["money", "gold", "inflation", "stablecoins"],
            "literals": ["G10"], "test": True}
    path = OUT / "meta.json"
    if path.exists():
        old = json.loads(path.read_text())
        for k in ("methods_url",):
            if k in old:
                meta[k] = old[k]
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    (OUT / "glossary.json").write_text(json.dumps(GLOSSARY, indent=2, ensure_ascii=False) + "\n")


def og() -> None:
    """The share picture: the open figure (the 1930s, wholesale), nothing from after the cut."""
    import vl_convert as vlc
    from PIL import Image

    spec = json.loads((OUT / "figures" / "fig-1930s" / "spec.vl.json").read_text())
    data = pd.read_csv(OUT / "figures" / "fig-1930s" / "data.csv", comment="#").to_dict("records")
    spec.update(data={"values": data}, width=1080, height=420,
                title={"text": TITLE, "fontSize": 30, "font": "serif", "anchor": "start", "color": "#1c1c1a"},
                background="#f7f5ef", padding=30)
    spec["layer"][1]["encoding"]["color"]["scale"] = {"range": ["#2f6b3a", "#9a978c"]}
    im = Image.open(io.BytesIO(vlc.vegalite_to_png(spec, scale=1))).convert("RGB")
    canvas = Image.new("RGB", (1200, 630), (247, 245, 239))
    im.thumbnail((1200, 630))
    canvas.paste(im, ((1200 - im.width) // 2, (630 - im.height) // 2))
    canvas.save(OUT / "og.png", optimize=True)


def main() -> None:
    R = W.reg()
    for sub in ("figures", "interactives"):
        if (OUT / sub).exists():
            shutil.rmtree(OUT / sub)  # rebuilt from the runs each time (generated)
    OUT.mkdir(parents=True, exist_ok=True)
    wholesale_1930s(R)
    W.door()
    tag("fig-door", ["p1-8-cs-c"])
    W.greenbacks()
    tag("fig-greenbacks", ["p1-8-cs-c", "k1-greenbacks"])
    cs_a(R)
    all_monies(R)
    cs_b()
    calculator(R)
    cs_d(R)
    cs_f(R)
    cs_e(R)
    meta_and_glossary()
    og()


if __name__ == "__main__":
    main()
