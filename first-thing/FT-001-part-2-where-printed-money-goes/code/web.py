"""The web study's folder (BLUEPRINT §5 w): ``web/site/<slug>/`` — ``meta.json``, ``glossary.json``, every figure
(a Vega-Lite spec reading its ``data.csv``, drawn by the site in its house style), the interactive pieces and
``og.png``. Everything is drawn from the cards' stored results and the registry; nothing is recomputed, and no
explorer shows a variant no card ran. ``toolkit/bin/ft study web`` then renders the article and the numbers into
the same folder. Run from the study's folder: ``../../toolkit/bin/ftpy code/web.py``.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

from ft import numbers  # noqa: E402
from ft.web import write_figure  # noqa: E402

SLUG = "ft-001-part-2-where-printed-money-goes"
OUT = K.STUDY / "web" / "site" / SLUG
AS_OF = "2026-09-30"
METHODS = ("https://github.com/Sami-Andaloussi/atlas-research/tree/0000000000000000000000000000000000000000/"
           "first-thing/FT-001-part-2-where-printed-money-goes")
FRED_URL = "https://fred.stlouisfed.org"
IMF_URL = "https://db.nomics.world/IMF/IFS"
FRED_LICENCE = "public-domain series, reused with citation (FRED terms of use)"
DERIVED = ("derived averages computed by First Thing from IMF data (free to use with attribution), World Bank data "
           "(CC BY 4.0) and the World Bank's inflation database (Ha, Kose and Ohnsorge, cited as asked), ECB and "
           "FRED series (reuse with citation)")

TITLE = "Does inflation really follow printed money?"


def load(card: str) -> dict:
    return json.loads((K.RUNS / f"{card}.json").read_text())["result"]


def reg() -> numbers.Registry:
    return numbers.Registry.load(K.STUDY / "results" / "numbers.json")


def names() -> dict[str, str]:
    """ISO2 code -> name, from the World Bank's list of economies (frozen), with the euro area's code."""
    page = json.loads((K.STUDY.parents[1] / "data" / "worldbank" / "_economies" / "2026-09-30" / "page-001.json").read_text())
    out = {e["iso2Code"]: e["name"] for e in page[1]}
    out.update({"U2": "Euro area"})
    return out


# Zoom and pan (Sami's reading on a computer, 2026-10-09; the site's answer, STUDIES-WEB §14.6): the scatters, the
# long timelines and the slope bands carry an interval selection bound to the scales; the site's build gives it its
# behaviour (drag, Ctrl or a pinch to zoom, "Reset view", off on a phone). Not fig-door: its six panels have six y
# units, so one interval set them all to one y range, and the zoom along x alone answers only inside a panel, which
# the site's test (Ctrl + wheel at the chart's centre, between two panels) refuses; it shows its whole window.
ZOOM = {"fig-bands", "fig-longrun", "fig-cross-section", "fig-calm", "fig-base-now"}
DATA_MARKS = ("point", "line", "area", "circle")


def _mark(layer: dict) -> str | None:
    m = layer.get("mark")
    return m if isinstance(m, str) else (m or {}).get("type")


def zoomable(spec: dict) -> dict:
    """The spec with the zoom param in the layer that holds the data marks (the top for a single view, the inner spec
    for a facet). Zoom along x only where y cannot take one shared interval: panels with independent y scales (one
    drag would set every panel's y to the same range) or a nominal y (scale binding needs a continuous domain)."""
    host = spec["spec"] if "facet" in spec and "spec" in spec else spec
    if "layer" in host:
        host = next(l for l in host["layer"] if _mark(l) in DATA_MARKS)
    y_type = (host.get("encoding", {}).get("y") or {}).get("type")
    x_only = spec.get("resolve", {}).get("scale", {}).get("y") == "independent" or y_type in ("nominal", "ordinal")
    select = {"type": "interval", "encodings": ["x"]} if x_only else "interval"
    host.setdefault("params", []).append({"name": "zoom", "select": select, "bind": "scales"})
    return spec


def fig(fid: str, rows: list[dict], spec: dict, **meta) -> None:
    if fid in ZOOM:
        spec = zoomable(spec)
    source_note = meta.pop("source_note")
    figure = {"as_of": AS_OF, **meta}
    write_figure(OUT, fid, rows=rows, spec={"$schema": "https://vega.github.io/schema/vega-lite/v6.json", **spec},
                 figure=figure, source_note=source_note)


def tip(*fields) -> list[dict]:
    return [dict(f) for f in fields]


# --- the figures ---------------------------------------------------------------------------------------------

def longrun(R: numbers.Registry) -> None:
    r = load("C28-a4-units-guard")["C02_grid"]
    line = R.get("lr_line")["value"]
    nm = names()
    rows = [{"economy": nm.get(p["area"], p["area"]), "decade": f"{p['y0']}–{p['y1']}",
             "money_growth": round(p["mu"], 1), "inflation": round(p["pi"], 1),
             "side": "above the line" if p["mu"] > line else "below the line"}
            for p in r["points"]]
    sym = {"type": "symlog", "constant": 1}
    spec = {
        "height": 320,
        "layer": [
            {"mark": {"type": "point", "filled": True, "opacity": 0.6, "size": 22, "aria": False},
             "encoding": {
                 "x": {"field": "money_growth", "type": "quantitative", "scale": sym,
                       "title": "base money growth, % a year (ten-year average)",
                       },
                 "y": {"field": "inflation", "type": "quantitative", "scale": sym,
                       "title": "inflation, % a year"},
                 "color": {"field": "side", "type": "nominal", "legend": {"orient": "bottom", "title": None}},
                 "tooltip": tip({"field": "economy", "type": "nominal"}, {"field": "decade", "type": "nominal"},
                                {"field": "money_growth", "type": "quantitative", "title": "money growth, % a year"},
                                {"field": "inflation", "type": "quantitative", "title": "inflation, % a year"})}},
            {"mark": {"type": "line", "strokeWidth": 1}, "transform": [{"filter": "datum.money_growth >= 0"}],
             "encoding": {"x": {"field": "money_growth", "type": "quantitative", "scale": sym},
                          "y": {"field": "money_growth", "type": "quantitative", "scale": sym}}},
            {"mark": {"type": "rule", "strokeDash": [4, 3]},
             "encoding": {"x": {"datum": line, "type": "quantitative", "scale": sym}}},
        ],
    }
    fig("fig-longrun", rows, spec, source_note=f"IMF International Financial Statistics, World Bank, ECB, FRED; "
        f"First Thing calculations; {DERIVED}",
        title="Money growth and inflation over decades, every economy with the data",
        measure="average growth of base money and average consumer price inflation over ten-year windows",
        unit="% a year", period="ten-year windows since 1950", population="every economy with the data",
        source="IMF International Financial Statistics (via DBnomics), World Bank and its inflation database, ECB, FRED; "
               "First Thing calculations", source_url=IMF_URL, licence=DERIVED,
        highlight="above the line",
        caption="Each dot is one economy over one decade. The diagonal is point for point; the dashed line is the "
                "line described in the text. Both axes stretch the small values so that both worlds show.",
        alt="A cloud of dots rising from the lower left; to the left of the dashed line they lie flat and low, to "
            "its right they climb more steeply, nearing the diagonal only at the fastest paces.",
        description="Each dot is one economy's ten-year average of base money growth against its average "
                    "inflation. Left of the dashed line the cloud is flat and low: faster money growth went with "
                    "little more inflation. To its right the cloud climbs more steeply, and only at the fastest paces "
                    "does it run along the diagonal, prices rising point for point with money.")


def door(R: numbers.Registry) -> None:
    r = load("C01-door")
    rows = []
    for label, w in (("2008–14", "W1"), ("2020–21", "W2")):
        p = r["paths"][w]
        for m, v in zip(p["months_since_start"], p["prices_since_start"]):
            rows.append({"printing": label, "months": m, "prices": round(v, 2)})
    spec = {"height": 260, "mark": {"type": "line", "point": False},
            "encoding": {"x": {"field": "months", "type": "quantitative", "title": "months since the printing began"},
                         "y": {"field": "prices", "type": "quantitative", "title": "% change since the first month"},
                         "color": {"field": "printing", "type": "nominal", "legend": {"orient": "bottom", "title": None}},
                         "tooltip": tip({"field": "printing", "type": "nominal"},
                                        {"field": "months", "type": "quantitative", "title": "months"},
                                        {"field": "prices", "type": "quantitative", "title": "prices, % change"})}}
    fig("fig-door-prices", rows, spec, source_note=f"FRED (BLS: CPIAUCSL); First Thing calculations; {FRED_LICENCE}",
        title="US consumer prices since the start of each printing",
        measure="consumer price index, all urban consumers, change since the first month", unit="%",
        period="August 2008 to October 2014; February 2020 to December 2021", population="United States",
        source="FRED (U.S. Bureau of Labor Statistics, CPIAUCSL); First Thing calculations", source_url=FRED_URL,
        licence=FRED_LICENCE, highlight="2020–21",
        alt="Two lines of prices since each printing began: the 2008 line flat for two years then rising slowly, "
            "the 2020 line rising fast to about the same height.",
        description="Prices since the first month of each American printing. The first line stays near zero for "
                    "about two years and ends 74 months later; the second climbs steadily and ends after 22 months "
                    "at about the same rise.")


def history() -> None:
    rows = [
        {"year": 1020, "event": "Song China, 1020s: the jiaozi, paper with a reserve and a term"},
        {"year": 1350, "event": "Yuan China, 1350s: paper over-issued as civil war came"},
        {"year": 1425, "event": "Ming China: unbacked paper far below its face value"},
        {"year": 1720, "event": "France: John Law's system collapses"},
        {"year": 1780, "event": "America: the Continental counted against coin"},
        {"year": 1796, "event": "France: the assignats abandoned"},
        {"year": 1864, "event": "The Confederacy cuts its money stock by law"},
        {"year": 1879, "event": "The Union's greenbacks back to par"},
        {"year": 1923, "event": "Germany: the mark collapses"},
        {"year": 1946, "event": "Hungary: the fastest inflation on record"},
        {"year": 2008, "event": "Zimbabwe's hyperinflation peaks; rich central banks start printing"},
    ]
    spec = {"height": 340, "mark": {"type": "point", "filled": True, "size": 70},
            "encoding": {"x": {"field": "year", "type": "quantitative", "scale": {"domain": [1000, 2030]},
                               "axis": {"format": "d", "values": [1000, 1250, 1500, 1750, 2000]}, "title": None},
                         "y": {"field": "event", "type": "nominal", "sort": {"field": "year"},
                               "title": None, "axis": {"labelLimit": 260}},
                         "tooltip": tip({"field": "year", "type": "quantitative", "format": "d"},
                                        {"field": "event", "type": "nominal"})}}
    fig("fig-history", rows, spec, source_note="First Thing, from the works cited in the text (von Glahn 1996; Guan, "
        "Palma and Wu 2024; Velde 2003; Grubb 2008; Sargent and Velde 1995; Burdekin and Weidenmier 2001; Calomiris "
        "1988; Hanke and Krus 2012); CC BY 4.0",
        title="A thousand years of adding money: the episodes told here", measure="dated episodes", unit="year",
        period="1020s–2008", population="the episodes told in this section",
        source="First Thing, from the works cited in the text", source_url=METHODS, licence="CC BY 4.0",
        alt="A timeline of eleven episodes from Song China in the 1020s to Zimbabwe and the rich central banks in 2008.",
        description="Each dot is one episode told in this section, placed on its year, from the jiaozi of the 1020s "
                    "to 2008.")


def deciders(R: numbers.Registry) -> None:
    t = load("C26-a5-deciders-hko-fill")["headline"]["readings"]["design"]["tests"]["O1"]
    label = {"D1": "Floating rather than pegged", "D2": "Rate above its floor near zero",
             "D4": "Claims on the government rose most", "D5": "Large deficit at the start"}
    rows = [{"candidate": label[d], "gap": round(t[d]["diff"], 2), "where_it_held": t[d]["n1"],
             "where_it_did_not": t[d]["n0"]} for d in label]
    spec = {"height": 200, "mark": {"type": "bar"},
            "encoding": {"y": {"field": "candidate", "type": "nominal", "sort": None, "title": None,
                               "axis": {"labelLimit": 220}},
                         "x": {"field": "gap", "type": "quantitative",
                               "title": "gap in inflation's change, points a year (none beats chance)"},
                         "tooltip": tip({"field": "candidate", "type": "nominal"},
                                        {"field": "gap", "type": "quantitative", "title": "gap, points a year"},
                                        {"field": "where_it_held", "type": "quantitative", "title": "printings where it held"},
                                        {"field": "where_it_did_not", "type": "quantitative",
                                         "title": "printings where it did not"})}}
    n = R.get("e_tested_design")["value"]
    fig("fig-deciders", rows, spec, source_note=f"IMF IFS and WEO (via DBnomics), FRED, ECB, World Bank and its "
        f"inflation database; First Thing calculations; {DERIVED}",
        title="Four candidates tested after a printing: none tells the printings apart",
        measure="median change in inflation over the 36 months after a printing, against the year before: where the "
                "candidate held minus where it did not", unit="points a year",
        period="printings starting 1950–2023", population=f"the {n} printings tested, each candidate on those it could "
        "be coded for",
        source="IMF International Financial Statistics and World Economic Outlook (via DBnomics), FRED, ECB, World "
               "Bank; First Thing calculations", source_url=IMF_URL, licence=DERIVED,
        caption="None of these gaps beats chance; the test gives no range, so it cannot show they are small either.",
        alt="Four short bars, two pointing left and two right, none large.",
        description="The gap in the median change in inflation after a printing, between the printings where each "
                    "candidate held and those where it did not. Two gaps are negative and two positive; none is "
                    "significant.")


def us_euro() -> None:
    rows = []
    for x in sorted(load("C18-a5-deciders-bare")["described_us_euro"], key=lambda x: (x["area"] != "U2", x["m0"])):
        name = f"{'Euro area' if x['area'] == 'U2' else 'United States'}, {pd.Period(x['m0'], 'M').strftime('%b %Y')}"
        rows.append({"printing": name, "when": "the year before", "inflation": round(x["O1pp"] - x["O1"], 2)})
        rows.append({"printing": name, "when": "the three years after", "inflation": round(x["O1pp"], 2)})
    spec = {"height": 280, "mark": {"type": "bar"},
            "encoding": {"y": {"field": "printing", "type": "nominal", "sort": None, "title": None},
                         "yOffset": {"field": "when", "type": "nominal", "sort": ["the year before", "the three years after"]},
                         "x": {"field": "inflation", "type": "quantitative", "title": "inflation, % a year"},
                         "color": {"field": "when", "type": "nominal", "sort": ["the year before", "the three years after"],
                                   "legend": {"orient": "bottom", "title": None}},
                         "tooltip": tip({"field": "printing", "type": "nominal"}, {"field": "when", "type": "nominal"},
                                        {"field": "inflation", "type": "quantitative", "title": "inflation, % a year"})}}
    fig("fig-us-euro", rows, spec, source_note=f"FRED (BLS: CPIAUCSL); ECB HICP (via DBnomics); First Thing "
        f"calculations; {FRED_LICENCE}; ECB data reused with citation",
        title="Inflation before and after each printing, United States and euro area",
        measure="consumer price inflation, the year before each printing began and the average of the three years after",
        unit="% a year", period="printings starting 2008–2020", population="the United States and the euro area",
        source="FRED (CPIAUCSL), ECB (HICP, via DBnomics); First Thing calculations", source_url=FRED_URL,
        licence="FRED public-domain series and ECB data, reused with citation", highlight="the three years after",
        alt="Paired bars for three euro-area and three US printings; only the two that began in 2019 and 2020 are "
            "followed by high inflation.",
        description="For each printing, inflation in the year before it began and over the three years after. The "
                    "first two in each economy were followed by low inflation; the third, by inflation near five "
                    "per cent a year.")


def velocity() -> None:
    r = load("C19-velocity-bare")
    sl = r["m2"]["Selden-Latane"]["path"]
    rows = []
    for q, v in sl["actual"].items():
        rows.append({"quarter": str(pd.Period(q, "Q").start_time.date()), "series": "M2 velocity", "value": round(v, 3)})
    for q, v in sl["predicted"].items():
        rows.append({"quarter": str(pd.Period(q, "Q").start_time.date()), "series": "what the interest rate predicts",
                     "value": round(v, 3)})
    spec = {"height": 260, "mark": {"type": "line"},
            "encoding": {"x": {"field": "quarter", "type": "temporal", "title": None},
                         "y": {"field": "value", "type": "quantitative", "title": "dollars of GDP per dollar of M2",
                               "scale": {"zero": False}},
                         "color": {"field": "series", "type": "nominal", "legend": {"orient": "bottom", "title": None}},
                         "tooltip": tip({"field": "quarter", "type": "temporal", "format": "%Y Q%q"},
                                        {"field": "series", "type": "nominal"},
                                        {"field": "value", "type": "quantitative", "format": ".2f"})}}
    fig("fig-velocity", rows, spec, source_note=f"FRED (M2V, TB3MS); First Thing calculations; {FRED_LICENCE}",
        title="How fast US broad money changes hands, against the interest rate's prediction",
        measure="M2 velocity (GDP divided by M2), and its prediction from the three-month bill rate (fitted to mid-2008)",
        unit="dollars of GDP per dollar of M2", period="1959–2026, quarterly", population="United States",
        source="FRED (Federal Reserve Bank of St. Louis: M2V; Board of Governors: TB3MS); First Thing calculations",
        source_url=FRED_URL, licence=FRED_LICENCE, highlight="M2 velocity",
        caption="The prediction explains less than one per cent of velocity's past, so the gap after 2008 cannot be read.",
        alt="Velocity rising to the late 1990s, falling after 2008 to a low in 2020, against a nearly flat prediction.",
        description="US M2 velocity each quarter since 1959 and the level predicted from the three-month bill rate. "
                    "After 2008 velocity runs below the prediction, but the prediction barely fits the years before, so "
                    "the gap cannot be read.")


def base_now() -> None:
    res = K.fred_series("WRESBAL") / 1e6
    cur = K.fred_series("WCURCIR") / 1e6
    start = pd.Timestamp("2007-01-01")
    rows = []
    for name, s in (("bank reserves", res), ("notes and coins", cur)):
        m = s[s.index >= start].resample("MS").mean()
        rows += [{"month": str(d.date()), "part": name, "trillions": round(float(v), 3)} for d, v in m.items()]
    spec = {"height": 240, "mark": {"type": "line"},
            "encoding": {"x": {"field": "month", "type": "temporal", "title": None},
                         "y": {"field": "trillions", "type": "quantitative", "title": "trillions of dollars"},
                         "color": {"field": "part", "type": "nominal", "legend": {"orient": "bottom", "title": None}},
                         "tooltip": tip({"field": "month", "type": "temporal", "format": "%b %Y"},
                                        {"field": "part", "type": "nominal"},
                                        {"field": "trillions", "type": "quantitative", "format": ".2f"})}}
    fig("fig-base-now", rows, spec, source_note=f"FRED (Board of Governors, H.4.1: WRESBAL, WCURCIR), monthly means "
        f"of weekly data; {FRED_LICENCE}",
        title="Where US base money sits: bank reserves and notes and coins",
        measure="reserve balances and currency in circulation, monthly means of weekly data", unit="trillions of dollars",
        period="January 2007 to September 2026", population="United States",
        source="FRED (Board of Governors, H.4.1)", source_url=FRED_URL, licence=FRED_LICENCE, highlight="bank reserves",
        alt="Bank reserves jumping far above notes and coins after 2008 and again in 2020; notes and coins rising slowly.",
        description="US bank reserves and currency in circulation each month since 2007. Reserves rise from almost "
                    "nothing to several trillion dollars after 2008 and again in 2020; currency rises steadily.")


def tax() -> None:
    by = load("C13-a6-checked")["whole_stock"]["by_year"]
    rows = [{"year": int(y), "loss": round(v["share_pct"], 3)} for y, v in sorted(by.items())]
    spec = {"height": 220, "mark": {"type": "bar"},
            "encoding": {"x": {"field": "year", "type": "ordinal", "title": None},
                         "y": {"field": "loss", "type": "quantitative", "title": "% of the year's GDP"},
                         "tooltip": tip({"field": "year", "type": "ordinal"},
                                        {"field": "loss", "type": "quantitative", "format": ".1f",
                                         "title": "% of the year's GDP"})}}
    fig("fig-tax", rows, spec, source_note=f"FRED (CPIAUCSL, CURRSL, FDIC non-interest-bearing deposits, GDP); First "
        f"Thing calculations; {FRED_LICENCE}",
        title="What inflation took each year from cash and from deposits paying nothing, United States",
        measure="purchasing power lost on currency and on deposits paying no interest, all holders",
        unit="% of each year's GDP", period="February 2020 to August 2026 (2026: to August)",
        population="all holders of US currency and non-interest-bearing deposits: households, firms, foreigners",
        source="FRED (BLS, Board of Governors, FDIC, BEA); First Thing calculations", source_url=FRED_URL,
        licence=FRED_LICENCE,
        caption="All holders, as a share of each year's GDP; the per-household figure in the text covers households "
                "only, over the whole period.",
        alt="Bars for each year from 2020 to 2026, tallest in 2021 and 2022, small before and after.",
        description="The purchasing power that inflation took each year from all US currency and deposits paying "
                    "no interest, as a share of that year's GDP: highest in 2021, then falling.")


# --- the interactive pieces ----------------------------------------------------------------------------------

def slider(R: numbers.Registry) -> None:
    """Where the decades end (C25 on its two grids: decades to 2020, and decades to 2019, C22's): a variant run."""
    d = OUT / "interactives" / "slider-decade-end"
    d.mkdir(parents=True, exist_ok=True)
    row = lambda end, p: {"end": end, "below": round(R.get(f"{p}_mu_below")["value"], 2),  # noqa: E731
                          "above": round(R.get(f"{p}_mu_above")["value"], 2), "all": round(R.get(f"{p}_beta")["value"], 2)}
    data = [row(2019, "lr_c22"), row(2020, "lr_base")]
    line = R.get("lr_line")["value"]
    config = {"component": "ft-slider-figure", "version": 1,
              "title": "Where the decades end",
              "source": "First Thing calculations on IMF, World Bank, ECB and FRED data; both grids run with the same "
                        "model and the same filled prices",
              "intro": "Every decade is read from its first and last year-ends. Move the last year: the decades ending "
                       "in 2020 count that year's pandemic printing and none of the inflation after it.",
              "settings": {
                  "params": [{"name": "end", "label": "The decades end in", "min": 2019, "max": 2020, "step": 1,
                              "default": 2019, "format": {"decimals": 0}}],
                  "outputs": [
                      {"name": "below", "label": f"Below the {line:g}% line: points of inflation per point of money",
                       "format": {"decimals": 2}},
                      {"name": "above", "label": f"Above the {line:g}% line", "format": {"decimals": 2}},
                      {"name": "all", "label": "All decades together", "format": {"decimals": 2}}],
                  "sentence": "On decades ending in {end}, a point more money growth went with {below} of a point "
                              "more inflation below the line, and {above} above it.",
                  "note": "Both settings are runs the study made; the page computes nothing."}}
    (d / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    (d / "data.json").write_text(json.dumps(data, indent=2) + "\n")


def calculator(R: numbers.Registry) -> None:
    d = OUT / "interactives" / "calc-cash"
    d.mkdir(parents=True, exist_ok=True)
    rise = round(R.get("cash_cpi_rise")["value"], 1)
    config = {"component": "ft-calc", "version": 1,
              "title": "What the price rise took from a balance you left untouched",
              "source": "US consumer prices, February 2020 to August 2026 (FRED, CPIAUCSL); First Thing calculation",
              "settings": {
                  "inputs": [
                      {"name": "balance", "label": "Cash or current-account balance", "min": 0, "max": 100000000,
                       "default": 10000, "format": {"prefix": "$", "decimals": 0}},
                      {"name": "rise", "label": "Rise in prices while you held it, %", "min": 0, "max": 1000,
                       "default": rise, "format": {"decimals": 1},
                       "help": "The default is the US rise from February 2020 to August 2026; type your own."}],
                  "outputs": [
                      {"label": "Purchasing power lost", "expr": "balance * (1 - 1 / (1 + rise / 100))",
                       "format": {"prefix": "$", "decimals": 0},
                       "note": "In the prices of the month you started holding it. A balance that earned interest lost less; one that grew or "
                               "shrank, a different sum."}]}}
    (d / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    lost = lambda b, r: b * (1 - 1 / (1 + r / 100))  # noqa: E731
    tests = [{"inputs": {"balance": 10000, "rise": rise}, "outputs": [lost(10000, rise)]},
             {"inputs": {"balance": 0, "rise": rise}, "expected": 0},
             {"inputs": {"balance": 2500, "rise": 0}, "expected": 0},
             {"inputs": {"balance": 1000, "rise": 25}, "expected": 200, "tolerance": 0.01}]
    (d / "tests.json").write_text(json.dumps(tests, indent=2) + "\n")


# --- meta, glossary, og.png ------------------------------------------------------------------------------------

GLOSSARY = {
    "base-money": {"term": "base money", "short": "The central bank's own money: notes and coins, and the reserves "
                   "banks hold at the central bank.",
                   "long": "Base money is what the central bank owes. Households hold only its notes and coins; the "
                           "reserves are held by banks alone.",
                   "example": "When a central bank buys a bond from a bank, the bank's reserves rise by the price paid.",
                   "first_use_only": True},
    "broad-money": {"term": "broad money", "short": "The money people and firms spend: cash and bank deposits.",
                    "long": "Most of it is deposits. Commercial banks create them when they lend, and when a bank or the "
                            "central bank buys an asset from someone outside the banks.",
                    "example": "Your current account balance is broad money; your bank's reserves are not.",
                    "first_use_only": True},
    "reserves": {"term": "reserves", "short": "The accounts commercial banks keep at the central bank.",
                 "long": "Banks use reserves to settle payments with one another. They do not lend them to customers: "
                         "a bank lends by creating a deposit.",
                 "example": "When the Federal Reserve buys Treasury bonds, it pays by adding to banks' reserves.",
                 "first_use_only": True},
    "quantity-theory": {"term": "quantity theory of money", "short": "The rule that prices rise when money grows "
                        "faster than what the economy produces, unless people hold more money for each dollar they spend.",
                        "example": "If money grows ten points faster than output for a decade, the rule expects prices "
                                   "to rise about ten points a year faster.",
                        "first_use_only": True},
    "interval": {"term": "interval", "short": "The range of values the data support, at the stated confidence: a range "
                 "drawn this way from repeated samples would hold the true value that often.",
                 "example": "A slope of one with an interval from a little under one to a little over one means the data fit anything in that range.",
                 "first_use_only": True},
    "velocity": {"term": "velocity", "short": "How many times a year, on average, a unit of money pays for the economy's "
                 "output: GDP divided by the money stock.",
                 "example": "A velocity of two means each dollar of broad money paid for two dollars of GDP in a year.",
                 "first_use_only": True},
}


def meta_and_glossary(R: numbers.Registry) -> None:
    meta = {"id": "FT-001", "slug": SLUG, "title": TITLE,
            "standfirst": ("Across 155 economies since 1950, the faster central banks created money, the more of it "
                           "showed up in prices. Below 12% a year — the dollar's pace over the decade to 2020 — a point "
                           "more money growth went with a quarter of a point more inflation; only the fastest printers "
                           "saw prices follow money point for point."),
            "series": "The life of a money", "part": 2,
            "as_of": AS_OF, "subscriber_at": "2026-12-31", "public_at": "2026-12-31",
            "cut_after": "the-line", "methods_url": METHODS, "reading_minutes": 22,
            "og_alt": "Ten-year averages of money growth against inflation for every economy since 1950: flat and low "
                      "at slow paces, steeper at fast ones.",
            "updated": AS_OF, "changelog": [], "topics": ["money", "inflation", "central banks"]}
    path = OUT / "meta.json"
    if path.exists():  # the engine's fields (literals, test, a pinned methods_url) are kept
        old = json.loads(path.read_text())
        for k in ("literals", "test", "methods_url"):
            if k in old:
                meta[k] = old[k]
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    (OUT / "glossary.json").write_text(json.dumps(GLOSSARY, indent=2, ensure_ascii=False) + "\n")


def og() -> None:
    import vl_convert as vlc

    spec = json.loads((OUT / "figures" / "fig-longrun" / "spec.vl.json").read_text())
    data = pd.read_csv(OUT / "figures" / "fig-longrun" / "data.csv", comment="#").to_dict("records")
    spec.update(data={"values": data}, width=1080, height=470,
                title={"text": TITLE, "fontSize": 30, "font": "serif", "anchor": "start", "color": "#1c1c1a"},
                background="#f7f5ef", padding=30)
    for layer in spec["layer"]:
        enc = layer["encoding"]
        if "color" in enc:
            enc["color"]["scale"] = {"range": ["#2f6b3a", "#9a978c"]}  # "above" sorts first
    png = vlc.vegalite_to_png(spec, scale=1)
    from PIL import Image  # noqa: PLC0415
    import io  # noqa: PLC0415
    im = Image.open(io.BytesIO(png)).convert("RGB")
    canvas = Image.new("RGB", (1200, 630), (247, 245, 239))
    im.thumbnail((1200, 630))
    canvas.paste(im, ((1200 - im.width) // 2, (630 - im.height) // 2))
    canvas.save(OUT / "og.png", optimize=True)


def main() -> None:
    R = reg()
    if (OUT / "figures").exists():
        shutil.rmtree(OUT / "figures")  # rebuilt from the runs each time (generated)
    longrun(R)
    door(R)
    history()
    deciders(R)
    us_euro()
    velocity()
    base_now()
    tax()
    slider(R)
    calculator(R)
    meta_and_glossary(R)
    og()


if __name__ == "__main__":
    main()
