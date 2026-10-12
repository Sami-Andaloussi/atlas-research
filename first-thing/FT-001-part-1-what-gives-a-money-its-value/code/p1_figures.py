"""Part 1's figures and the purchasing-power slider, drawn from the cards' runs and the reused builds into the web
study's folder (``web/site/<slug>/figures`` and ``interactives``); from the study's folder, after the registry:
``python code/p1_figures.py``.

Every value drawn is a run's (C18, C20-C23) or the A3 build's; nothing is typed here. Axis titles stay under 35
characters and the categories sit on y (STUDIES-WEB §16); every chart has a tooltip.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from ft.web import write_figure

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
RUNS = STUDY / "results" / "runs"
SLUG = "ft-001-part-1-what-gives-a-money-its-value"
SITE = STUDY / "web" / "site" / SLUG

BIS = ("BIS, long consumer-price series (WS_LONG_CPI)", "https://data.bis.org/topics/CPI",
       "BIS terms of permitted use: reuse with the BIS cited as source")
SHORT = {"USD": "US dollar", "GBP": "pound sterling", "CHF": "Swiss franc", "JPY": "yen",
         "FRF_then_euro_in_France": "franc, then euro (France)", "DEM_then_euro_in_Germany": "Mark, then euro (Germany)",
         "Reichsmark": "Reichsmark"}
PERIOD = {(1914, 1945): "1914-45", (1946, 1971): "1946-71", (1972, 1991): "1972-91", (1992, 2025): "1992-2025"}


def run(card: str) -> dict:
    return json.loads((RUNS / f"{card}.json").read_text())["result"]


def tooltip(*fields: tuple[str, str, str | None]) -> list[dict]:
    out = []
    for field, title, fmt in fields:
        t = {"field": field, "title": title, "type": "quantitative" if fmt else "nominal"}
        if fmt:
            t["format"] = fmt
        out.append(t)
    return out


def cs_a() -> None:
    r = run("C21-cs-a-what-a-unit-buys")
    rows = []
    for name, label in SHORT.items():
        for row in r["monies"][name]["periods"]:
            if row.get("computable"):
                rows.append({"money": label, "period": PERIOD[tuple(row["period"])], "loss": row["yearly_loss_pct"]})
    spec = {
        "params": [{"name": "period", "value": "1992-2025",
                    "bind": {"input": "radio", "options": list(PERIOD.values()), "name": "Period: "}}],
        "transform": [{"filter": "datum.period == period"}],
        "mark": {"type": "bar"},
        "encoding": {"y": {"field": "money", "type": "nominal", "title": None, "sort": "-x"},
                     "x": {"field": "loss", "type": "quantitative", "title": "yearly loss, % a year"},
                     "tooltip": tooltip(("money", "Money", None), ("period", "Period", None), ("loss", "Yearly loss, %", ".1f"))},
    }
    write_figure(SITE, "fig-cs-a", rows=rows, spec=spec, source_note=f"{BIS[0]}; {BIS[2]}", figure={
        "title": "What each money lost a year, by period", "measure": "yearly loss of what one unit buys",
        "unit": "% a year", "period": "1913-2025", "population": "the reader's monies",
        "source": BIS[0], "source_url": BIS[1], "licence": BIS[2], "as_of": "2026-09-30",
        "alt": "Bars of the yearly loss of what one unit of each money buys, for the chosen period.",
        "description": "For each period (1914-45, 1946-71, 1972-91, 1992-2025), the average yearly "
                       "loss of what one unit of the dollar, the pound, the Swiss franc, the yen, the French franc then "
                       "the euro in France, the Mark then the euro in Germany, and the Reichsmark bought, from the BIS's "
                       "consumer prices. A money appears only in the periods its series covers.",
        "caption": "From the year before each period (or the money's first year) to its last year. The euro's prices in "
                   "France and Germany are the national indices; the Reichsmark and the Deutsche Mark are not chained "
                   "across the reform of 1948.",
        "claims": ["cs-a-1914-45", "cs-a-1946-71", "cs-a-1972-91", "cs-a-1992-2025"]})
    # the slider: what one unit of a year buys in 2025, per money
    grids = {name: {g["year"]: g for g in r["monies"][name]["grid"]} for name in SHORT}
    outs = [("USD", "usd", "One US dollar of that year, in 2025 dollars", {"prefix": "$", "decimals": 2}, "today_units"),
            ("GBP", "gbp", "One pound of that year, in 2025 pounds", {"prefix": "£", "decimals": 2}, "today_units"),
            ("CHF", "chf", "One Swiss franc of that year, in 2025 francs", {"suffix": " francs", "decimals": 2}, "today_units"),
            ("JPY", "jpy", "One yen of that year, in 2025 yen", {"suffix": " yen", "decimals": 2}, "today_units"),
            ("FRF_then_euro_in_France", "fr", "One French franc of that year (from 1999, one euro), in 2025 euros",
             {"prefix": "€", "decimals": 3}, "today_units"),
            ("DEM_then_euro_in_Germany", "de", "One Mark of that year (from 1999, one euro), in 2025 euros",
             {"prefix": "€", "decimals": 2}, "today_units"),
            ("Reichsmark", "rm", "One Reichsmark of that year, in 1947 Reichsmarks", {"suffix": " Reichsmarks", "decimals": 2},
             "units_of_1947")]
    data = []
    for year in range(1914, 2026):
        row = {"year": year}
        for name, col, _, _, field in outs:
            g = grids[name].get(year)
            row[col] = None if g is None else round(g[field], 4)
        data.append(row)
    d = SITE / "interactives" / "slider-cs-a"
    d.mkdir(parents=True, exist_ok=True)
    (d / "data.json").write_text(json.dumps(data, indent=1) + "\n")
    config = {"component": "ft-slider-figure", "version": 1,
              "title": "What one unit of a year buys in 2025",
              "source": "BIS long consumer-price series; the official conversion factors (the BIS, 1960; the ECB, 1998)",
              "settings": {"params": [{"name": "year", "label": "Year", "min": 1914, "max": 2025, "step": 1,
                                       "default": 1971, "format": {"decimals": 0}}],
                           "outputs": [{"name": col, "label": label, "format": fmt} for _, col, label, fmt, _ in outs],
                           "sentence": "What one unit of {year} buys today:",
                           "note": "A dash means the money's series does not cover that year. The franc before 1960 is "
                                   "the old franc (100 to a new franc); the euro took over at 6.55957 francs and 1.95583 "
                                   "Marks. The Reichsmark stops in 1947: the reform of 1948 converted money at several "
                                   "rates, so it is not chained to the Deutsche Mark."}}
    (d / "config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")


def cs_b() -> None:
    r = run("C22-cs-b-the-franc")
    rows = []
    for basis, label in (("usd", "against the dollar"), ("narrow", "against trading partners")):
        for kind in ("nominal", "real"):
            for y, v in r["series_1970_100"][basis][kind].items():
                if int(y) <= 2025:
                    rows.append({"year": int(y), "basis": label, "rate": kind, "index": v})
    spec = {
        "params": [{"name": "basis", "value": "against the dollar",
                    "bind": {"input": "radio", "options": ["against the dollar", "against trading partners"],
                             "name": "The franc: "}},
                   {"name": "zoom", "select": "interval", "bind": "scales", "encodings": ["x"]}],
        "transform": [{"filter": "datum.basis == basis"}],
        "mark": {"type": "line", "point": False},
        "encoding": {"x": {"field": "year", "type": "quantitative", "title": None, "axis": {"format": "d"}},
                     "y": {"field": "index", "type": "quantitative", "title": "index, 1970 = 100"},
                     "color": {"field": "rate", "type": "nominal", "title": None},
                     "tooltip": tooltip(("year", "Year", "d"), ("rate", "Rate", None), ("index", "Index", ".0f"))},
    }
    write_figure(SITE, "fig-cs-b", rows=rows, spec=spec,
                 source_note="BIS WS_XRU, WS_EER (narrow basket) and long consumer prices; BIS terms of permitted use",
                 figure={"title": "The franc, nominal and real, since 1970", "measure": "the franc's exchange rate, nominal and real",
                         "unit": "index, 1970 = 100", "period": "1970-2025", "population": "the Swiss franc",
                         "source": "BIS exchange rates (WS_XRU), effective exchange rates (WS_EER) and consumer prices",
                         "source_url": "https://data.bis.org/topics/EER", "licence": BIS[2], "as_of": "2026-10-10",
                         "highlight": "real",
                         "alt": "Two lines, the franc's nominal and real exchange rate since 1970, against the dollar or against trading partners.",
                         "description": "The franc in dollars, and against its trading partners (the BIS's narrow basket), "
                                        "each nominal and real (adjusted for the gap between Swiss and foreign consumer "
                                        "prices), as an index with 1970 = 100. The space between the nominal and the real "
                                        "line is Switzerland's lower inflation.",
                         "caption": "Annual averages. The real rate is the nominal rate times Swiss over foreign consumer prices.",
                         "claims": ["cs-b-usd", "cs-b-effective"]})
    pl = r["price_level"]
    names = {"DEU": "Germany", "FRA": "France", "ITA": "Italy", "AUT": "Austria"}
    rows = [{"neighbour": names[c], "ratio": v} for c, v in pl["che_over_neighbour"].items()]
    spec = {"mark": {"type": "bar"},
            "encoding": {"y": {"field": "neighbour", "type": "nominal", "title": None, "sort": "-x"},
                         "x": {"field": "ratio", "type": "quantitative", "title": "Swiss price level, times theirs"},
                         "tooltip": tooltip(("neighbour", "Neighbour", None), ("ratio", "Times", ".2f"))}}
    write_figure(SITE, "fig-cs-b-price", rows=rows, spec=spec,
                 source_note="World Bank, PA.NUS.PPP and PA.NUS.FCRF; CC BY 4.0",
                 figure={"title": f"Switzerland's price level against its neighbours', {pl['latest_common_year']}",
                         "measure": "GDP price level, Switzerland over each neighbour", "unit": "times",
                         "period": str(pl["latest_common_year"]), "population": "Switzerland and its neighbours",
                         "source": "World Bank, PPP conversion factor for GDP and official exchange rate",
                         "source_url": "https://data.worldbank.org/indicator/PA.NUS.PPP", "licence": "CC BY 4.0",
                         "as_of": "2026-10-10",
                         "alt": "Bars: Switzerland's GDP price level as a multiple of Germany's, France's, Italy's and Austria's.",
                         "description": "The World Bank's PPP conversion factor for GDP over the market exchange rate gives "
                                        "each country's price level; each bar is Switzerland's divided by a neighbour's.",
                         "caption": "The GDP price level covers everything an economy produces, not only what shoppers buy.",
                         "claims": ["cs-b-price-level"]})
    rows = [{"year": int(y), "series": "exports, % of GDP", "value": v} for y, v in r["exports_pct_gdp"].items() if int(y) <= 2025]
    rows += [{"year": int(y), "series": "real franc vs partners, 1970 = 100", "value": v}
             for y, v in r["series_1970_100"]["narrow"]["real"].items() if 1971 <= int(y) <= 2025]
    # the facet operator, not encoding.row: the site sizes each panel of a column facet and stacks them on a phone
    spec = {"facet": {"column": {"field": "series", "type": "nominal", "title": None}},
            "spec": {"mark": {"type": "line"},
                     "encoding": {"x": {"field": "year", "type": "quantitative", "title": None, "axis": {"format": "d"}},
                                  "y": {"field": "value", "type": "quantitative", "title": None},
                                  "tooltip": tooltip(("year", "Year", "d"), ("series", "Series", None),
                                                     ("value", "Value", ".1f"))}},
            "resolve": {"scale": {"y": "independent"}}}
    write_figure(SITE, "fig-cs-b-exports", rows=rows, spec=spec,
                 source_note="World Bank NE.EXP.GNFS.ZS (CC BY 4.0); BIS WS_EER and long consumer prices",
                 figure={"title": "Swiss exports beside the real franc", "measure": "exports of goods and services; the real effective rate",
                         "unit": "% of GDP; index, 1970 = 100", "period": "1971-2025", "population": "Switzerland",
                         "source": "World Bank, exports of goods and services (% of GDP); BIS effective exchange rates",
                         "source_url": "https://data.worldbank.org/indicator/NE.EXP.GNFS.ZS",
                         "licence": "CC BY 4.0 (World Bank); BIS terms of permitted use", "as_of": "2026-10-10",
                         "alt": "Two panels: Swiss exports as a share of GDP, and the franc's real effective rate, since 1971.",
                         "description": "Top: exports of goods and services as a share of Swiss GDP. Bottom: the franc's real "
                                        "effective exchange rate against its trading partners (narrow basket), 1970 = 100. "
                                        "No line is fitted and no correlation is computed.",
                         "caption": "Two series side by side: many things move exports besides the franc.",
                         "claims": ["cs-b-exports"]})


def cs_c() -> None:
    r = run("C23-cs-c-losses-by-era")
    names = {"before_1914": "before 1914", "1914_to_1971_07": "1914 to July 1971", "from_1971_08": "from August 1971"}
    rows = []
    for variant, label in (("headline", "every price index"), ("rr_cpi_only", "consumer prices only")):
        for span, s in r[variant]["spans"].items():
            rows.append({"span": names[span], "variant": label, "rate": s["rate_per_100"]})
    spec = {"mark": {"type": "bar"},
            "encoding": {"y": {"field": "span", "type": "nominal", "title": None, "sort": list(names.values())},
                         "yOffset": {"field": "variant"},
                         "x": {"field": "rate", "type": "quantitative", "title": "per 100 money-years"},
                         "color": {"field": "variant", "type": "nominal", "title": None},
                         "tooltip": tooltip(("span", "Span", None), ("variant", "Index", None), ("rate", "Per 100 money-years", ".1f"))}}
    write_figure(SITE, "fig-cs-c", rows=rows, spec=spec,
                 source_note="First Thing's panel of price indices (Reinhart and Rogoff; IMF IFS; BIS; World Bank; JST), counts only",
                 figure={"title": "How often a new inflation crisis began", "measure": "crises of 20% or more in a year begun",
                         "unit": "per 100 money-years with a reading", "period": "1800-2025",
                         "population": "every money with a price reading, the euro and each union once",
                         "source": "First Thing's panel of price indices, from Reinhart and Rogoff, the IMF, the BIS, the World Bank and JST",
                         "source_url": "https://www.macrohistory.net/database/", "licence": "counts of ours; the sources' values not republished",
                         "as_of": "2026-09-30", "highlight": "every price index",
                         "alt": "Bars of how often a crisis of prices rising a fifth or more in a year began, per 100 money-years, in three spans of time.",
                         "description": "Crises of prices rising 20% or more in a year, each counted once at its start, per 100 years "
                                        "of readings, before 1914, from 1914 to July 1971 and from August 1971; beside them, "
                                        "the count on consumer prices alone.",
                         "caption": "Each crisis is counted once, at the date it began.",
                         "claims": ["cs-c"]})


def cs_d_f() -> None:
    d = run("C20-cs-b-without-hyperinflation-years")["main"]
    rows = [{"years": "convertible into gold or silver", "mean": d["convertible"]["mean"]},
            {"years": "paper (inconvertible)", "mean": d["fiat"]["mean"]}]
    spec = {"mark": {"type": "bar"},
            "encoding": {"y": {"field": "years", "type": "nominal", "title": None},
                         "x": {"field": "mean", "type": "quantitative", "title": "mean inflation, % a year"},
                         "tooltip": tooltip(("years", "Years", None), ("mean", "Mean, % a year", ".1f"))}}
    write_figure(SITE, "fig-cs-d", rows=rows, spec=spec,
                 source_note="First Thing's two means, computed from the Jorda-Schularick-Taylor Macrohistory Database R6 (CC BY-NC-SA 4.0); no value of the database republished",
                 figure={"title": "Prices under a metal standard and under paper", "measure": "mean consumer-price inflation",
                         "unit": "% a year", "period": "1870-2020", "population": "17 rich economies; war, 1946-71 and over-100% years apart",
                         "source": "Jorda-Schularick-Taylor Macrohistory Database (R6); Bordo and Schwartz's chronology",
                         "source_url": "https://www.macrohistory.net/database/",
                         "licence": "means of ours; the database's values (CC BY-NC-SA 4.0) not republished",
                         "as_of": "2026-09-30", "highlight": "paper (inconvertible)",
                         "alt": "Two bars: average yearly consumer-price inflation in years convertible into gold or silver and in paper years.",
                         "description": "Average yearly consumer-price inflation over economy-years classed by Bordo and "
                                        "Schwartz's chronology, without the years above 100% inflation.",
                         "caption": "No year after 1938 is convertible, so the two classes are also two eras; today's rich "
                                    "economies only.",
                         "claims": ["cs-d"]})
    f = run("C18-cs-a-consumer-prices-off-gold")["main"]
    rows = [{"what": "leavers less stayers", "estimate": f["pooled"], "low": f["lo"], "high": f["hi"]}]
    spec = {"layer": [
        {"mark": {"type": "rule"}, "encoding": {"y": {"field": "what", "type": "nominal", "title": None},
                                                "x": {"field": "low", "type": "quantitative", "title": "points a year"},
                                                "x2": {"field": "high"}}},
        {"mark": {"type": "point", "filled": True, "size": 90},
         "encoding": {"y": {"field": "what", "type": "nominal"}, "x": {"field": "estimate", "type": "quantitative"},
                      "tooltip": tooltip(("estimate", "Estimate", ".1f"), ("low", "Low", ".1f"), ("high", "High", ".1f"))}}]}
    write_figure(SITE, "fig-cs-f", rows=rows, spec=spec,
                 source_note="First Thing's estimate, computed from the Jorda-Schularick-Taylor Macrohistory Database R6 (CC BY-NC-SA 4.0) and Bernanke and James's dates; no value of the database republished",
                 figure={"title": "Consumer prices after leaving gold, 1932-34", "measure": "leavers' inflation less stayers'",
                         "unit": "points a year", "period": "1932-1934", "population": "Bernanke and James's economies in JST",
                         "source": "Jorda-Schularick-Taylor Macrohistory Database (R6); Bernanke and James (1991)",
                         "source_url": "https://www.macrohistory.net/database/",
                         "licence": "an estimate of ours; the database's values (CC BY-NC-SA 4.0) not republished",
                         "as_of": "2026-09-30",
                         "alt": "A point with a long range: the gap in consumer-price inflation between leavers and stayers of gold, 1932-34.",
                         "description": "The difference in yearly consumer-price inflation between the economies off gold and "
                                        "those on it, 1932-34, with its range: wide, from below zero to about eleven points.",
                         "caption": "The range rules out a gap of more than about eleven points a year.",
                         "claims": ["cs-f"]})


def cs_e() -> None:
    rows_all = list(csv.DictReader((ROOT / "data" / "reconstructed" / "ft001-a3" / "series.csv").open(encoding="utf-8")))
    for money, fid, title, period, url, src in (
            ("USA", "fig-cs-e-greenback", "The greenback's value in gold, 1862-1878", "1862-1878",
             "https://archive.org/details/goldpriceswages0000unse", "Mitchell (1908), Gold, Prices, and Wages under the Greenback Standard, Table 2"),
            ("GBR", "fig-cs-e-pound", "The paper pound's value in gold, 1800-1821", "1800-1821",
             "https://archive.org/details/india.history.resource.37818", "Tooke (1838), A History of Prices, vol. 2, p. 379")):
        rows = []
        for r in rows_all:
            if r["money"] != money or r["value"] in ("", "nan") or math.isnan(float(r["value"])):
                continue
            rows.append({"period": r["period"], "value": round(100 * float(r["value"]), 1)})
        temporal = money == "USA"
        spec = {"mark": {"type": "line", "point": not temporal},
                "encoding": {"x": {"field": "period", "type": "temporal" if temporal else "quantitative", "title": None,
                                   **({} if temporal else {"axis": {"format": "d"}})},
                             "y": {"field": "value", "type": "quantitative", "title": "% of its value in gold",
                                   "scale": {"domain": [0, 105]}},
                             "tooltip": tooltip(("period", "Date", None), ("value", "% of par", ".0f"))}}
        if not temporal:
            for row in rows:
                row["period"] = int(row["period"])
        write_figure(SITE, fid, rows=rows, spec=spec, source_note=f"{src}; public domain (transcribed by First Thing)",
                     figure={"title": title, "measure": "paper's value in gold", "unit": "% of par",
                             "period": period, "population": "the greenback" if temporal else "the paper pound",
                             "source": src, "source_url": url, "licence": "public domain (the printed table); our transcription",
                             "as_of": "2026-10-02",
                             "alt": f"A line of {'the greenback' if temporal else 'the paper pound'}'s value in gold, falling and returning to par.",
                             "description": ("The value of a paper dollar in gold, monthly, from Mitchell's table of the gold "
                                             "price in greenbacks." if temporal else
                                             "The value of a paper pound in gold, yearly, from Tooke's table of the average price "
                                             "of gold.") + " Par is 100%.",
                             "caption": "Transcribed from the printed table on its page images.",
                             "claims": ["cs-e"]})


def main() -> None:
    cs_a()
    cs_b()
    cs_c()
    cs_d_f()
    cs_e()


if __name__ == "__main__":
    main()
