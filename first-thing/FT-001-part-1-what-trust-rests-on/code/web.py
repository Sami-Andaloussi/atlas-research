"""The web study's folder (BLUEPRINT §5 w): ``web/site/<slug>/`` — ``meta.json``, ``glossary.json``, every figure
(a Vega-Lite spec reading its ``data.csv``, drawn by the site in its house style), the interactive piece and
``og.png``. Everything is drawn from the committed builds, the cards' stored results and the registry; nothing is
recomputed, and the explorer shows only readings the card ran. ``toolkit/bin/ft study web`` then renders the article
and the numbers into the same folder. Run from the study's folder: ``../../toolkit/bin/ftpy code/web.py``.
"""

from __future__ import annotations

import csv
import io
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
REC = ROOT / "data" / "reconstructed"
sys.path.insert(0, str(HERE))

from ft import numbers  # noqa: E402
from ft.web import write_figure  # noqa: E402

SLUG = "ft-001-part-1-what-trust-rests-on"
OUT = STUDY / "web" / "site" / SLUG
AS_OF = "2026-10-02"
METHODS = ("https://github.com/Sami-Andaloussi/atlas-research/tree/0000000000000000000000000000000000000000/"
           "first-thing/FT-001-part-1-what-trust-rests-on")
TITLE = "Does a money lose its value when its backing goes?"
TOOKE = ("Thomas Tooke, A History of Prices, its second volume (1838), the tables of the price of gold, "
         "transcribed by First Thing from the archive.org scans")
TOOKE_URL = "https://archive.org/details/india.history.resource.37818"
PD = "public domain (published 1838 and 1908); First Thing's transcription, reuse with citation"
DERIVED = ("counts and averages derived by First Thing; each source's own terms apply (listed in the methods and "
           "proof); reuse with citation")


def reg() -> numbers.Registry:
    return numbers.Registry.load(STUDY / "results" / "numbers.json")


def v(R: numbers.Registry, key: str, nd: int = 2) -> float:
    return round(float(R.get(key)["value"]), nd)


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Zoom and pan (Sami's reading on a computer, 2026-10-09; the site's answer, STUDIES-WEB §14.6): the scatters, the
# long timelines and the slope bands carry an interval selection bound to the scales; the site's build gives it its
# behaviour (drag, Ctrl or a pinch to zoom, "Reset view", off on a phone).
ZOOM = {"fig-door", "fig-greenbacks", "fig-cs-a"}
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

def _decimal(period: str) -> float:
    """'1797-08' -> 1797.58; '1800' -> 1800.5 (an annual average sits at mid-year)."""
    if len(period) == 4:
        return int(period) + 0.5
    y, m = period.split("-")
    return round(int(y) + (int(m) - 0.5) / 12, 3)


def door() -> None:
    d = REC / "ft001-a3"
    semi = [r for r in read_csv(d / "variant-cross-source.csv")
            if r["case"] == "the Bank Restriction" and r["P"] and r["period"] <= "1799-12"]
    annual = [r for r in read_csv(d / "series.csv") if r["case"] == "the Bank Restriction" and r["P"] not in ("", "nan")]
    rows = ([{"year": _decimal(r["period"]), "date": r["period"], "value": round(100 * float(r["P"]), 1),
              "read": "two dates a year (gold in bars)"} for r in semi]
            + [{"year": _decimal(r["period"]), "date": r["period"], "value": round(100 * float(r["P"]), 1),
                "read": "the year's average"} for r in annual])
    spec = {"height": 280,
            "layer": [
                {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 100}}},
                {"mark": {"type": "line", "point": True},
                 "encoding": {"x": {"field": "year", "type": "quantitative", "title": None,
                                    "scale": {"domain": [1797, 1822]}, "axis": {"format": "d"}},
                              "y": {"field": "value", "type": "quantitative",
                                    "title": "what a note bought, % of its gold at par",
                                    "scale": {"domain": [70, 102]}},
                              "color": {"field": "read", "type": "nominal",
                                        "legend": {"orient": "bottom", "title": None}},
                              "tooltip": tip({"field": "date", "type": "nominal", "title": "date"},
                                             {"field": "value", "type": "quantitative", "title": "% of par"},
                                             {"field": "read", "type": "nominal", "title": "Tooke's table"})}}]}
    fig("fig-door", rows, spec, source_note=f"{TOOKE}; First Thing calculations; {PD}",
        title="What a Bank of England note bought in gold, 1797–1821",
        measure="the gold a note bought, as a share of the gold it bought at the mint's price", unit="% of par",
        period="August 1797 to 1821", population="Bank of England notes, in London",
        source=TOOKE, source_url=TOOKE_URL, licence=PD, highlight="two dates a year (gold in bars)",
        caption="The dashed line is par: a note buying its full weight of gold at the mint's price. Gold was suspended "
                "in February 1797 and paid again from May 1821.",
        alt="A line at par from 1797 to 1800, then falling below it from 1801 to a low in 1814, and back to par by "
            "1821.",
        description="The gold a Bank of England note bought, as a share of par. At Tooke's five dates from August 1797 "
                    "to August 1799, and in the yearly average for 1800, the line sits at par; from 1801 it falls, to about three quarters of par in 1814, "
                    "and climbs back to par by 1821.")


def greenbacks() -> None:
    rows = [{"month": r["period"], "value": round(100 * float(r["P"]), 1)}
            for r in read_csv(REC / "ft001-a3" / "series.csv")
            if r["case"] == "the greenbacks" and r["P"] not in ("", "nan")]
    spec = {"height": 260,
            "layer": [
                {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"y": {"datum": 100}}},
                {"mark": {"type": "line"},
                 "encoding": {"x": {"field": "month", "type": "temporal", "title": None},
                              "y": {"field": "value", "type": "quantitative",
                                    "title": "what a greenback bought, % of its gold at par",
                                    "scale": {"domain": [30, 102]}},
                              "tooltip": tip({"field": "month", "type": "temporal", "title": "month",
                                              "format": "%B %Y"},
                                             {"field": "value", "type": "quantitative", "title": "% of par"})}}]}
    src = ("Wesley C. Mitchell, Gold, Prices, and Wages under the Greenback Standard (1908), Table 2, transcribed by "
           "First Thing from the archive.org scan")
    fig("fig-greenbacks", rows, spec, source_note=f"{src}; First Thing calculations; {PD}",
        title="What a greenback bought in gold, 1862–1878",
        measure="the gold a greenback dollar bought, as a share of the gold dollar", unit="% of par",
        period="January 1862 to December 1878", population="United States notes (greenbacks), in New York",
        source=src, source_url="https://archive.org/details/goldpriceswages0000unse", licence=PD,
        caption="The dashed line is par. Gold payments were suspended at the end of 1861 and resumed on 1 January 1879.",
        alt="A line falling from par in 1862 to a low in mid-1864, then climbing slowly back toward par by 1878.",
        description="The gold a greenback bought, month by month: a fall to under two fifths of par in July 1864, "
                    "then a slow climb back to par before resumption in 1879.")


GROUPS = (("p1", "1914 suspensions of gold"), ("p2", "1931–36 exits from gold"), ("p3d", "Independence cut"),
          ("p3u", "Independence raised"), ("p4", "Inflation target adopted"))


def window(R: numbers.Registry) -> None:
    rows = [{"group": name, "gap": v(R, f"a2_{k}_mean"), "low": v(R, f"a2_{k}_band_lo"),
             "high": v(R, f"a2_{k}_band_hi"), "changes": int(R.get(f"a2_{k}_n")["value"])} for k, name in GROUPS]
    y = {"field": "group", "type": "nominal", "sort": None, "title": None, "axis": {"labelLimit": 220}}
    spec = {"height": 220,
            "layer": [
                {"mark": {"type": "rule", "strokeWidth": 6, "opacity": 0.35},
                 "encoding": {"y": y, "x": {"field": "low", "type": "quantitative",
                                            "title": "gap in inflation's change, points a year"},
                              "x2": {"field": "high"}}},
                {"mark": {"type": "point", "filled": True, "size": 70},
                 "encoding": {"y": y, "x": {"field": "gap", "type": "quantitative"},
                              "tooltip": tip({"field": "group", "type": "nominal"},
                                             {"field": "gap", "type": "quantitative", "title": "mean gap, points"},
                                             {"field": "low", "type": "quantitative", "title": "chance's range, from"},
                                             {"field": "high", "type": "quantitative", "title": "to"},
                                             {"field": "changes", "type": "quantitative", "title": "changes"})}},
                {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"x": {"datum": 0}}}]}
    fig("fig-window", rows, spec, source_note=f"Bernanke and James; Garriga (2025); Hammond (2012) and the IMF's "
        f"AREAER; IMF IFS, World Bank, Reinhart and Rogoff; First Thing calculations; {DERIVED}",
        title="After a change of backing: inflation's gap against matched monies, with chance's range",
        measure="inflation's change over the five years after a change less the year before, minus the same in "
                "matched monies; the bar is the range scenarios with no effect give", unit="points a year",
        period="changes of 1914, 1931–1936 and since 1970", population="every change in each group, matched to "
        "monies that did not change", source="Bernanke and James; Garriga (2025); Hammond (2012); IMF; World Bank; "
        "Reinhart and Rogoff; First Thing calculations", source_url="https://db.nomics.world/IMF/IFS", licence=DERIVED,
        caption="Dot: the mean gap. Bar: the range a change with no effect gives at that number of changes. Every dot "
                "sits inside its bar: the test could not tell.",
        alt="Five dots, each inside a wide bar that spans zero.",
        description="For each group of changes, the mean gap in inflation against matched monies, inside the range "
                    "that scenarios with no effect give. Every mean lies inside its range; the ranges run several "
                    "points either side of zero.")


DATINGS = ((1, "a class of creditors newly in arrears", ""), (2, "the state's total debt newly in default", "tot_"),
           (3, "its private creditors' debt newly in default", "prv_"))


def defaults(R: numbers.Registry) -> None:
    rows = []
    for _, name, p in DATINGS:
        rows.append({"dating": name, "set": "money crises", "share": v(R, f"c1_{p}after_sr", 1)})
        rows.append({"dating": name, "set": "years of stress that held", "share": v(R, f"c1_{p}base_sr", 1)})
    spec = {"height": 230, "mark": {"type": "bar"},
            "encoding": {"y": {"field": "dating", "type": "nominal", "sort": None, "title": None,
                               "axis": {"labelLimit": 200}},
                         "yOffset": {"field": "set", "type": "nominal"},
                         "x": {"field": "share", "type": "quantitative",
                               "title": "% with a default or another act in the three years before"},
                         "color": {"field": "set", "type": "nominal", "legend": {"orient": "bottom", "title": None}},
                         "tooltip": tip({"field": "dating", "type": "nominal", "title": "a default dated by"},
                                        {"field": "set", "type": "nominal"},
                                        {"field": "share", "type": "quantitative", "title": "% with a default or another act before"})}}
    fig("fig-defaults", rows, spec, source_note=f"the Bank of Canada–Bank of England sovereign default database; IMF "
        f"IFS, World Bank, Reinhart and Rogoff; First Thing calculations; {DERIVED}",
        title="A default or another act in the three years before: money crises against years of stress that held",
        measure="share with a default or another act on the list (a cap on lending lifted, a peg dropped, independence "
                "cut, a second money made legal) in the three years before, under each of three datings of a default",
        unit="% of those that can be read", period="1970 to the sources' last years",
        population="money crises (inflation reaching 20% a year) and years of fiscal stress with no crisis",
        source="Bank of Canada–Bank of England sovereign default database; IMF; World Bank; Reinhart and Rogoff; "
               "First Thing calculations", source_url="https://www.bankofcanada.ca/2025/10/staff-analytical-note-2025-24/", licence=DERIVED,
        highlight="money crises",
        caption="However a default is dated, a default or another act came before a crisis somewhat more often than "
                "before a year of stress that held, and before many years that held. Most crises began from higher "
                "inflation than those years: a description, not a test.",
        alt="Three pairs of bars; in each, the crises' bar is a little longer than the bar of the years that held.",
        description="Under each dating of a default, the share of money crises with a default or another act in the "
                    "three years before, beside the share of years of fiscal stress that did not break. The crises' "
                    "share is higher each time; the years that held have such an act before them often.")


HELD = (("head", "The comparison fixed in advance", "c2_head"), ("tb", "Without the state's credit", "c2_tb"),
        ("np", "Pegs and currency boards set aside", "c2_np"))


def held(R: numbers.Registry) -> None:
    rows = [{"reading": name, "difference": v(R, f"{p}_d", 1), "low": v(R, f"{p}_lo", 1), "high": v(R, f"{p}_hi", 1),
             "thin_side": int(R.get(f"{p}_n_fewer")["value"]), "other_side": int(R.get(f"{p}_n_two")["value"])}
            for _, name, p in HELD]
    margin = R.get("c2_margin")["value"]
    y = {"field": "reading", "type": "nominal", "sort": None, "title": None, "axis": {"labelLimit": 220}}
    spec = {"height": 170,
            "layer": [
                {"mark": {"type": "rule", "strokeWidth": 3},
                 "encoding": {"y": y, "x": {"field": "low", "type": "quantitative",
                                            "title": "held more often, points (two or more backings against fewer)"},
                              "x2": {"field": "high"}}},
                {"mark": {"type": "point", "filled": True, "size": 70},
                 "encoding": {"y": y, "x": {"field": "difference", "type": "quantitative"},
                              "tooltip": tip({"field": "reading", "type": "nominal"},
                                             {"field": "difference", "type": "quantitative", "title": "points"},
                                             {"field": "low", "type": "quantitative", "title": "interval from"},
                                             {"field": "high", "type": "quantitative", "title": "to"},
                                             {"field": "thin_side", "type": "quantitative", "title": "periods, thin side"},
                                             {"field": "other_side", "type": "quantitative", "title": "periods, other side"})}},
                {"mark": {"type": "rule", "strokeDash": [4, 3]}, "encoding": {"x": {"datum": 0}}},
                {"mark": {"type": "rule", "strokeDash": [2, 2], "opacity": 0.6}, "encoding": {"x": {"datum": margin}}}]}
    fig("fig-held", rows, spec, source_note=f"Garriga (2025); Ilzetzki, Reinhart and Rogoff; Chinn and Ito; the "
        f"default database; IMF IFS and WEO; First Thing calculations; {DERIVED}",
        title="Under the same stress, did monies with more backing hold more often?",
        measure="share of periods of stress after which the money held for ten years: two or more backings minus "
                "one or none, with its 90% interval", unit="percentage points",
        period="periods of fiscal stress entered since 1970", population="inconvertible monies under fiscal stress",
        source="Garriga (2025); Ilzetzki, Reinhart and Rogoff; Chinn and Ito; the default database; IMF; First Thing "
               "calculations", source_url="https://db.nomics.world/IMF/IFS", licence=DERIVED,
        caption="Dot: the difference; bar: its 90% interval; dotted line: the ten points fixed in advance as the "
                "smallest that counts. No reading clears it: the record could not tell.",
        alt="Three dots with bars; the first two bars cross zero, the third starts just above zero; all reach below "
            "the dotted line.",
        description="The difference in how often monies held, more backings against fewer, for three readings. The "
                    "first two intervals cross zero; the third, with pegs set aside, starts a few points above zero "
                    "but below the ten points that count.")


def coins(R: numbers.Registry) -> None:
    rows = [{"line": "cannot be read", "coin_lines": int(R.get("c4_unread")["value"])},
            {"line": "yes", "coin_lines": int(R.get("c4_yes")["value"])},
            {"line": "no", "coin_lines": int(R.get("c4_no")["value"])}]
    spec = {"height": 140, "mark": {"type": "bar"},
            "encoding": {"y": {"field": "line", "type": "nominal", "sort": None, "title": None},
                         "x": {"field": "coin_lines", "type": "quantitative",
                               "title": "coin-lines (four lines for each coin)"},
                         "tooltip": tip({"field": "line", "type": "nominal", "title": "the line reads"},
                                        {"field": "coin_lines", "type": "quantitative", "title": "coin-lines"})}}
    fig("fig-coins", rows, spec, source_note=f"BIS, Federal Reserve, New York Fed and NBER papers; the issuers' launch "
        f"documents (Internet Archive, New York DFS); First Thing's coding; {DERIVED}",
        title="What stablecoins rest on: four lines a coin, read at launch",
        measure="each coin's four lines (redemption, reserves or a cap, supervision, the issuer taking the coin) "
                "as coded under a rule fixed in advance", unit="coin-lines",
        period="each coin at its launch", population="every stablecoin named in a fixed set of central-bank and "
        "academic papers", source="BIS, Federal Reserve and NBER papers; the issuers' documents; First Thing's coding",
        source_url="https://www.bis.org/publ/bppdf/bispap141.pdf", licence=DERIVED, highlight="cannot be read",
        caption="Most lines cannot be read from any document found.",
        alt="Three bars: the longest, lines that cannot be read; then yes; then no.",
        description="Of the coins' four lines each, most cannot be read; fewer read yes, and fewest read no.")


# --- the interactive piece -----------------------------------------------------------------------------------

def slider(R: numbers.Registry) -> None:
    """How a default is dated (C15's three readings, all run): the shares for the crises and the years that held."""
    d = OUT / "interactives" / "slider-default-dating"
    d.mkdir(parents=True, exist_ok=True)
    data = [{"dating": i, "name": name, "crises": v(R, f"c1_{p}after_sr", 0), "held": v(R, f"c1_{p}base_sr", 0)}
            for i, name, p in DATINGS]
    config = {"component": "ft-slider-figure", "version": 1,
              "title": "How a default is dated",
              "source": "First Thing calculations on the Bank of Canada–Bank of England default database; the three "
                        "datings were fixed before any crisis was set against them, and all three were run",
              "intro": "One default touches several classes of creditors in turn. Move the setting to date it by "
                       "the first class in arrears, by the state's total debt, or by its private creditors.",
              "settings": {
                  "params": [{"name": "dating", "label": "Dating (1 to 3)", "min": 1, "max": 3, "step": 1,
                              "default": 1, "format": {"decimals": 0}}],
                  "outputs": [
                      {"name": "name", "label": "A default dated by"},
                      {"name": "crises", "label": "Money crises with a default or another act in the three years before, %",
                       "format": {"decimals": 0}},
                      {"name": "held", "label": "Years of stress that held, with one, %", "format": {"decimals": 0}}],
                  "sentence": "Dated by {name}, a default or another act came before {crises}% of the crises and before {held}% of "
                              "the years of stress in which the money held.",
                  "note": "Each setting is a reading the study ran; the page computes nothing."}}
    (d / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    (d / "data.json").write_text(json.dumps(data, indent=2) + "\n")


# --- meta, glossary, og.png ------------------------------------------------------------------------------------

GLOSSARY = {
    "premium": {"term": "premium", "short": "How much more a paper money had to pay for gold than the fixed price at "
                "which it was once convertible.",
                "example": "If an ounce of gold cost a quarter more in notes than the mint's price, the premium was a "
                           "quarter.",
                "first_use_only": True},
    "gap": {"term": "gap", "short": "How much more inflation changed after a change of backing than in the monies "
            "matched to it.",
            "long": "Inflation over the five years after the change, less the year before, minus the same for monies "
                    "that did not change and had the same inflation before.",
            "example": "A gap of two points: inflation rose two points a year more than in the matched monies.",
            "first_use_only": True},
    "crisis": {"term": "money crisis", "short": "Here, a money whose inflation reaches the line Reinhart and Rogoff "
               "use for an inflation crisis; the study gives the line.",
               "long": "It is dated from the month inflation began to stay high, or the money fell sharply against the "
                       "dollar, by lines fixed before any money was read.",
               "example": "A money whose inflation climbs from single digits to past that line has had a money crisis.",
               "first_use_only": True},
    "stress": {"term": "fiscal stress", "short": "A year when the state's debt or deficit passed a fixed line, its "
               "central bank lent to it, or it printed a large sum.",
               "long": "The lines, fixed before any money was read, are given in the study; a year is read only "
                       "while inflation was still low the year before.",
               "example": "A state whose debt has passed the line while its inflation stays low is in a year of "
                          "fiscal stress.",
               "first_use_only": True},
    "stablecoin": {"term": "stablecoin", "short": "A token on a blockchain whose issuer promises a fixed value, most "
                   "often one dollar.",
                   "example": "A dollar stablecoin whose terms let any holder redeem it at one dollar from its issuer.",
                   "first_use_only": True},
}


def meta_and_glossary(R: numbers.Registry) -> None:
    meta = {"id": "FT-001", "slug": SLUG, "title": TITLE,
            "standfirst": ("In 1797 the Bank of England stopped paying gold for its notes until the peace, and for two "
                           "and a half years they still bought their full weight of gold. Since 1970, a default or another act removing "
                           "a backing came before many money crises, and before many years of fiscal stress in which a "
                           "money held."),
            "series": "The life of a money", "part": 1,
            "as_of": AS_OF, "subscriber_at": "2026-12-31", "public_at": "2026-12-31",
            "cut_after": "door", "methods_url": METHODS, "reading_minutes": 18,
            "og_alt": "What a Bank of England note bought in gold from 1797 to 1821: at par for the first years after "
                      "gold was suspended.",
            "updated": AS_OF, "changelog": [], "topics": ["money", "gold", "central banks", "stablecoins"]}
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
    from PIL import Image

    spec = json.loads((OUT / "figures" / "fig-door" / "spec.vl.json").read_text())
    data = pd.read_csv(OUT / "figures" / "fig-door" / "data.csv", comment="#").to_dict("records")
    spec.update(data={"values": data}, width=1080, height=430,
                title={"text": TITLE, "fontSize": 30, "font": "serif", "anchor": "start", "color": "#1c1c1a"},
                background="#f7f5ef", padding=30)
    for layer in spec["layer"]:
        enc = layer["encoding"]
        if "color" in enc:
            enc["color"]["scale"] = {"range": ["#9a978c", "#2f6b3a"]}
    png = vlc.vegalite_to_png(spec, scale=1)
    im = Image.open(io.BytesIO(png)).convert("RGB")
    canvas = Image.new("RGB", (1200, 630), (247, 245, 239))
    im.thumbnail((1200, 630))
    canvas.paste(im, ((1200 - im.width) // 2, (630 - im.height) // 2))
    canvas.save(OUT / "og.png", optimize=True)


def main() -> None:
    R = reg()
    if (OUT / "figures").exists():
        shutil.rmtree(OUT / "figures")  # rebuilt from the builds and runs each time (generated)
    door()
    greenbacks()
    window(R)
    defaults(R)
    held(R)
    coins(R)
    slider(R)
    meta_and_glossary(R)
    og()


if __name__ == "__main__":
    main()
