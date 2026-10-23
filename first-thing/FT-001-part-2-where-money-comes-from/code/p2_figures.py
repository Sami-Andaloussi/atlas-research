"""Part 2's figures, drawn from the cards' runs into the web study's folder (``web/site/<slug>/figures``); from the
study's folder, after the registry: ``python code/p2_figures.py``.

Every value drawn is a run's (C28, C30, C31, C35-C38), except the balance-sheet explorer's, which shows the
mechanisms of the study's balance sheets on an example amount (a loan of 100, a share from 20 to 40), named so in its
caption: it draws the sources' accounting, not a measurement. Axis titles stay under 35 characters and the categories
sit on y (STUDIES-WEB §16); every chart has a tooltip.
"""

from __future__ import annotations

import json
from pathlib import Path

from ft.web import write_figure

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
RUNS = STUDY / "results" / "runs"
SLUG = "ft-001-part-2-where-money-comes-from"
SITE = STUDY / "web" / "site" / SLUG

FRED = ("the Federal Reserve Board (H.6, M2) and the BEA (NIPA tables 1.1.5, 1.1.6 and 1.1.9)", "https://www.bea.gov/data/gdp/gross-domestic-product",
        "public domain (US government works), each agency credited")
CS_A_SOURCES = ("the Federal Reserve Board, H.6 (currency, M2); the ECB's monetary statistics (BSI); the Bank of England's database (LPMAVAB, "
                "LPMAUYN)", "https://data.ecb.europa.eu", "public domain (the Board); reuse with attribution (the ECB, the Bank of England)")
Z1 = ("Federal Reserve Board, Financial Accounts of the United States (Z.1), table S1M.r; the BLS's CPI-U",
      "https://www.federalreserve.gov/releases/z1/", "public domain")
GRID = ("IMF International Financial Statistics, the World Bank, FRED and the ECB (a grid of economies)",
        "https://data.imf.org", "free with attribution (IMF, World Bank); public domain (FRED)")


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
    r = run("C35-cs-a-currency-share")
    names = {"us": "United States (M2)", "euro_area": "euro area (M3)", "britain": "Britain (M4)"}
    rows = []
    for k, label in names.items():
        for month, share in r[k]["series"].items():
            if share is not None and month.endswith(("-03", "-06", "-09", "-12")):  # quarter-end months: lighter data
                rows.append({"month": month, "economy": label, "share": share})
    spec = {
        "params": [{"name": "zoom", "select": "interval", "bind": "scales"}],
        "mark": {"type": "line"},
        "encoding": {"x": {"field": "month", "type": "temporal", "title": None},
                     "y": {"field": "share", "type": "quantitative", "title": "notes and coin, % of money"},
                     "color": {"field": "economy", "type": "nominal", "title": None},
                     "tooltip": tooltip(("economy", "Economy", None), ("month", "Month", None),
                                        ("share", "Notes and coin, % of broad money", ".1f"))},
    }
    write_figure(SITE, "fig-cs-a", rows=rows, spec=spec, source_note=f"{CS_A_SOURCES[0]}; {CS_A_SOURCES[2]}", figure={
        "title": "Notes and coin as a share of the money people hold",
        "measure": "notes and coin held by the public (in Britain, in circulation), share of broad money",
        "unit": "% of broad money",
        "period": "1959-2026", "population": "the US, the euro area and Britain",
        "source": CS_A_SOURCES[0], "source_url": CS_A_SOURCES[1], "licence": CS_A_SOURCES[2], "as_of": "2026-10-10",
        "alt": "Lines of notes and coin as a share of broad money in the US, the euro area and Britain, each since its "
               "series began.",
        "description": "Notes and coin held by the public (in Britain, all in circulation, banks' holdings included), as "
                       "a share of each economy's broad money (M2 in the US, M3 in the euro area, M4 in Britain), at the "
                       "end of each quarter since each series begins.",
        "caption": "Each statistic counts different promises as money (M2, M3, M4), so the levels compare forms, not "
                   "economies. US currency includes notes held abroad.",
        "claims": ["cs-a"]})


def cs_e() -> None:
    r = run("C36-cs-e-household-real-wealth")
    labels = {"real_and_market_priced": "real assets, priced claims", "fund_and_pension": "funds and pensions",
              "nominal_claims": "bonds, notes and coin, deposits", "net_investment": "net investment",
              "erosion_of_other_nominal_assets": "other nominal assets",
              "gain_on_liabilities": "gain on what is owed", "other_volume": "other volume changes"}
    rows = []
    for span, t in r["spans"].items():
        if span == "1952-2025":
            continue
        for k, label in labels.items():
            rows.append({"decade": span, "part": label, "trillions": t[k]})
    spec = {
        "mark": {"type": "bar"},
        "encoding": {"y": {"field": "decade", "type": "nominal", "title": None, "sort": None},
                     "x": {"field": "trillions", "type": "quantitative", "title": "trillions of 2025 dollars"},
                     "color": {"field": "part", "type": "nominal", "title": None, "sort": list(labels.values())},
                     "tooltip": tooltip(("decade", "Years", None), ("part", "Part", None),
                                        ("trillions", "Trillions of Dec-2025 dollars", ".1f"))},
    }
    write_figure(SITE, "fig-cs-e", rows=rows, spec=spec, source_note=f"{Z1[0]}; {Z1[2]}", figure={
        "title": "Where US households' real wealth came from, by decade",
        "measure": "the real change in net worth and its parts", "unit": "trillions of December 2025 dollars",
        "period": "1952-2025", "population": "US households and nonprofits",
        "source": Z1[0], "source_url": Z1[1], "licence": Z1[2], "as_of": "2026-10-10",
        "alt": "Bars by decade of the parts of the real change in US households' net worth: holding gains by group, "
               "net investment, inflation's erosion and gain, and other volume changes.",
        "description": "For each decade from 1952, the real change in US households' net worth split into real "
                       "holding gains on three groups of assets, the Fed's net investment, inflation's erosion of other "
                       "nominal assets, inflation's gain on what households owe, and other volume changes, in December "
                       "2025 dollars. The parts add up to the real change.",
        "caption": "A description, not a test: no line is drawn. Real holding gains are revaluations less the "
                   "quarter's inflation on the start-of-quarter holding.",
        "claims": ["cs-e"]})


def cs_f() -> None:
    r = run("C37-cs-f-money-output-prices")
    names = {"money": "money (M2)", "real_output": "real output", "prices": "prices", "velocity": "velocity"}
    spans = list(r["spans"])
    rows = [{"span": span, "series": label, "growth": r["spans"][span][k]} for span in spans for k, label in names.items()]
    spec = {
        "params": [{"name": "span", "value": spans[0], "bind": {"input": "select", "options": spans, "name": "Years: "}}],
        "transform": [{"filter": "datum.span == span"}],
        "mark": {"type": "bar"},
        "encoding": {"y": {"field": "series", "type": "nominal", "title": None, "sort": list(names.values())},
                     "x": {"field": "growth", "type": "quantitative", "title": "average growth, % a year"},
                     "tooltip": tooltip(("span", "Years", None), ("series", "Series", None),
                                        ("growth", "Average growth, % a year", ".2f"))},
    }
    write_figure(SITE, "fig-cs-f", rows=rows, spec=spec, source_note=f"{FRED[0]}; {FRED[2]}", figure={
        "title": "Money, real output and prices in the US",
        "measure": "average yearly growth of M2, real GDP, the GDP price index and velocity", "unit": "% a year",
        "period": "1959-2025", "population": "the United States",
        "source": "the Board's M2 (H.6); the BEA's real GDP, GDP price deflator and nominal GDP", "source_url": FRED[1], "licence": FRED[2], "as_of": "2026-10-10",
        "alt": "Bars of the average yearly growth of money, real output, prices and velocity in the US, for the chosen years.",
        "description": "Average yearly growth, fourth quarter to fourth quarter, of US M2, real output (real GDP), the GDP price index "
                       "and velocity (GDP over M2), for 1959 to 2025 and each decade.",
        "caption": "An identity: money growth equals real growth plus price growth less velocity growth. It says how "
                   "the four moved side by side, and attributes nothing.",
        "claims": ["cs-f"]})


def cs_g() -> None:
    r = run("C38-cs-g-money-and-real-growth")
    rows = [{"economy": p["area"], "window": p["window"], "money": round(p["mu"], 2), "real": round(p["g"], 2),
             "kind": "calm" if p["calm"] else "faster money"} for p in r["points"]]
    spec = {
        "params": [{"name": "zoom", "select": "interval", "bind": "scales"}],
        "mark": {"type": "point", "filled": True, "opacity": 0.6},
        "encoding": {"x": {"field": "money", "type": "quantitative", "title": "money growth, % a year",
                           "scale": {"type": "symlog"}},
                     "y": {"field": "real", "type": "quantitative", "title": "real growth, % a year"},
                     "color": {"field": "kind", "type": "nominal", "title": None},
                     "tooltip": tooltip(("economy", "Economy", None), ("window", "Decade", None),
                                        ("money", "Broad money growth, % a year", ".1f"),
                                        ("real", "Real GDP growth, % a year", ".1f"))},
    }
    write_figure(SITE, "fig-cs-g", rows=rows, spec=spec, source_note=f"{GRID[0]}; {GRID[2]}", figure={
        "title": "Money growth and real growth, decade by decade",
        "measure": "average yearly growth of broad money and of real GDP over ten years", "unit": "% a year",
        "period": "1960-2020", "population": "a grid of economies",
        "source": GRID[0], "source_url": GRID[1], "licence": GRID[2], "as_of": "2026-10-01",
        "alt": "A scatter of real growth against broad money growth, one point per economy and decade, calm decades "
               "marked.",
        "description": "Each point is one economy's decade: its broad money growth (a log-like scale) against its real "
                       "output growth, both averages over ten years; calm decades are those in which money grew no "
                       "faster than the line the text describes, adapted from Teles and Uhlig.",
        "caption": "An illustration in the manner of Lucas's figure, not a test: no line is fitted. Lucas found no "
                   "relation across countries over 1960-90; McCandless and Weber found a weak positive one in the OECD.",
        "claims": ["cs-g", "k6-neutrality"]})


def cs_c() -> None:
    r = run("C28-a4-units-guard")
    rows = []
    for grid, label in (("C02_grid", "base money"), ("broad", "broad money")):
        g = r[grid]["guarded"]["line_mu"]
        for side, words in (("above", "faster than the line"), ("below", "slower")):
            # four places, so the tooltip's .2f is the one rounding and agrees with the text (1.1248 stored as 1.125
            # read 1.13 in the tooltip where the methods print 1.12, 2026-10-21)
            rows.append({"row": f"{label}, {words}", "slope": round(g[f"beta_{side}"], 4),
                         "low": round(g[f"beta_{side}_lo"], 4), "high": round(g[f"beta_{side}_hi"], 4)})
    enc_y = {"field": "row", "type": "nominal", "title": None, "sort": None}
    spec = {
        "layer": [
            {"mark": {"type": "rule"}, "encoding": {"y": enc_y, "x": {"field": "low", "type": "quantitative",
                                                                     "title": "inflation per point of money"},
                                                    "x2": {"field": "high"}}},
            {"mark": {"type": "point", "filled": True, "size": 80},
             "encoding": {"y": enc_y, "x": {"field": "slope", "type": "quantitative"},
                          "tooltip": tooltip(("row", "Windows", None), ("slope", "Slope", ".2f"),
                                             ("low", "Low end", ".2f"), ("high", "High end", ".2f"))}}],
    }
    write_figure(SITE, "fig-cs-c", rows=rows, spec=spec, source_note=f"{GRID[0]}; {GRID[2]}", figure={
        "title": "How much inflation went with each point of money growth",
        "measure": "slope of ten-year inflation on ten-year money growth, each side of the line",
        "unit": "points of inflation per point of money growth", "period": "1950-2020", "population": "a grid of economies",
        "source": GRID[0], "source_url": GRID[1], "licence": GRID[2], "as_of": "2026-10-01",
        "alt": "How much inflation went with each point of money growth, for base and broad money, in decades faster and "
               "slower than the line, each with its 95% margin of error.",
        "description": "How much average inflation went with each point of average money growth across decades, for "
                       "decades in which money grew faster than the line (adapted from Teles and Uhlig) and for those in "
                       "which it grew slower, for base money and for broad money, each with its 95% margin of error.",
        "caption": "An association across decades. Measurement error in money growth flattens the slow side somewhat.",
        "claims": ["cs-c"]})


def cs_d() -> None:
    r = run("C31-cs-e-pandemic-cross-section")
    rows = []
    for label, block in (("energy-import control (main)", r["main"]), ("no control", r["main_no_control"]),
                         ("2021 inflation as a control", r["variants"]["c_momentum"])):
        b = block["huber_boot"]
        rows.append({"row": label, "slope": round(block["huber"], 3), "low": round(b["lo"], 3), "high": round(b["hi"], 3),
                     "economies": block["n"]})
    enc_y = {"field": "row", "type": "nominal", "title": None, "sort": None}
    spec = {
        "layer": [
            {"mark": {"type": "rule"}, "encoding": {"y": enc_y, "x": {"field": "low", "type": "quantitative",
                                                                     "title": "inflation per point of money"},
                                                    "x2": {"field": "high"}}},
            {"mark": {"type": "point", "filled": True, "size": 80},
             "encoding": {"y": enc_y, "x": {"field": "slope", "type": "quantitative"},
                          "tooltip": tooltip(("row", "Version", None), ("slope", "Slope", ".2f"), ("low", "Low end", ".2f"),
                                             ("high", "High end", ".2f"), ("economies", "Economies", ".0f"))}}],
    }
    write_figure(SITE, "fig-cs-d", rows=rows, spec=spec, source_note="IMF International Financial Statistics; free with attribution",
                 figure={
        "title": "Money growth in 2020-21 and inflation in 2022-23",
        "measure": "robust slope of 2022-23 inflation on 2020-21 broad money growth",
        "unit": "points of inflation per point of money growth", "period": "2019-2023",
        "population": "economies that started calm", "source": "IMF International Financial Statistics",
        "source_url": "https://data.imf.org", "licence": "free with attribution", "as_of": "2026-10-10",
        "alt": "How much inflation went with each point of money growth in three versions: the main one, one without "
               "the energy-import control, one allowing for 2021's inflation, each with its 95% margin of error.",
        "description": "Across economies whose inflation was calm in 2015-19, how much their inflation over 2022-23 went "
                       "with each point of their broad money growth over 2020-21, by a method that a few extreme "
                       "economies cannot distort, in three versions set before we saw the results, each with its 95% "
                       "margin of error from resampling the economies.",
        "caption": "The money and the fiscal spending that carried it went together; the cross-section does not separate them.",
        "claims": ["cs-d"]})


#: The explorer's steps: the study's balance sheets (map §7, after McLeay, Radia and Thomas 2014) on an example amount.
STEPS = {
    "A bank lends": [("Bank", "loan to the borrower", "asset", 100), ("Bank", "the borrower's deposit", "owes", 100),
                     ("Borrower", "deposit", "asset", 100), ("Borrower", "debt to the bank", "owes", 100)],
    "The loan is repaid": [("Bank", "loan to the borrower", "asset", -100), ("Bank", "the borrower's deposit", "owes", -100),
                           ("Borrower", "deposit", "asset", -100), ("Borrower", "debt to the bank", "owes", -100)],
    "Cash is withdrawn": [("You", "deposit", "asset", -100), ("You", "notes", "asset", 100),
                          ("Bank", "your deposit", "owes", -100), ("Bank", "reserves", "asset", -100),
                          ("Central bank", "reserves", "owes", -100), ("Central bank", "notes", "owes", 100)],
    "Central bank buys from a bank": [("Central bank", "bond", "asset", 100), ("Central bank", "reserves", "owes", 100),
                                      ("Bank", "bond", "asset", -100), ("Bank", "reserves", "asset", 100)],
    "Central bank buys from a fund": [("Central bank", "bond", "asset", 100), ("Central bank", "reserves", "owes", 100),
                                      ("Bank", "reserves", "asset", 100), ("Bank", "the fund's deposit", "owes", 100),
                                      ("Pension fund", "bond", "asset", -100), ("Pension fund", "deposit", "asset", 100)],
    "The state spends": [("State", "account at the central bank", "asset", -100),
                         ("Central bank", "the state's account", "owes", -100), ("Central bank", "reserves", "owes", 100),
                         ("Bank", "reserves", "asset", 100), ("Bank", "the recipient's deposit", "owes", 100),
                         ("Recipient", "deposit", "asset", 100)],
    "A share doubles": [("Holder", "share (from 20 to 40)", "asset", 20), ("Company", "equity at market value", "owes", 20)],
    "A share is pledged": [("Bank", "loan to the holder", "asset", 20), ("Bank", "the holder's deposit", "owes", 20),
                           ("Holder", "deposit", "asset", 20), ("Holder", "debt to the bank", "owes", 20)],
}
#: What each step does to the two money stocks: broad (the public's notes and deposits) and base (notes and reserves).
MONEY = {"A bank lends": (100, 0), "The loan is repaid": (-100, 0), "Cash is withdrawn": (0, 0),
         "Central bank buys from a bank": (0, 100), "Central bank buys from a fund": (100, 100),
         "The state spends": (100, 100), "A share doubles": (0, 0), "A share is pledged": (20, 0)}


def explorer() -> None:
    rows = []
    for step, entries in STEPS.items():
        for holder, item, side, change in entries:
            rows.append({"step": step, "line": f"{holder}: {item}", "side": "holds" if side == "asset" else "owes",
                         "change": change})
        broad, base = MONEY[step]
        rows.append({"step": step, "line": "Broad money: the public's notes and deposits", "side": "money stock", "change": broad})
        rows.append({"step": step, "line": "Base money: notes and reserves", "side": "money stock", "change": base})
    steps = list(STEPS)
    spec = {
        "params": [{"name": "step", "value": steps[0], "bind": {"input": "select", "options": steps, "name": "What happens: "}}],
        "transform": [{"filter": "datum.step == step"}],
        "layer": [
            {"mark": {"type": "bar"},
             "encoding": {"y": {"field": "line", "type": "nominal", "title": None, "sort": None},
                          "x": {"field": "change", "type": "quantitative", "title": "change, example amount",
                                "scale": {"domain": [-100, 100]}},
                          "color": {"field": "side", "type": "nominal", "title": None,
                                    "sort": ["holds", "owes", "money stock"]},
                          "tooltip": tooltip(("line", "Line", None), ("side", "Kind", None), ("change", "Change", "+.0f"))}},
            {"mark": {"type": "text", "align": "left", "dx": 4},
             "encoding": {"y": {"field": "line", "type": "nominal", "sort": None},
                          "x": {"datum": 0}, "text": {"field": "change", "type": "quantitative", "format": "+.0f"}}}],
    }
    write_figure(SITE, "fig-explorer", rows=rows, spec=spec,
                 source_note="First Thing; the balance sheets of McLeay, Radia and Thomas (2014), on an example amount",
                 figure={
        "title": "Move the balance sheets: what each step does to money",
        "measure": "change on each balance sheet and in the money stock", "unit": "an example amount",
        "period": "any time", "population": "an economy with a central bank and commercial banks",
        "source": "McLeay, Radia and Thomas (2014), Bank of England Quarterly Bulletin 2014 Q1",
        "source_url": "https://www.bankofengland.co.uk/-/media/boe/files/quarterly-bulletin/2014/money-creation-in-the-modern-economy.pdf",
        "licence": "the mechanism as the source states it; the figure is First Thing's", "as_of": "2026-10-11",
        "alt": "For the chosen step, bars of what changes on each balance sheet, what is held and what is owed, and "
               "in the two money stocks.",
        "description": "Choose a step: a bank lends, the loan is repaid, cash is withdrawn, the central bank buys a bond "
                       "from a bank or from a pension fund, the state spends, a share doubles, a share is pledged for a "
                       "loan. The bars show each change on the balance sheets involved and in broad money and base "
                       "money.",
        "caption": "An example amount, not data: a loan of 100, a share going from 20 to 40. The accounting is the Bank "
                   "of England's; the state's and the share's steps apply it.",
        "claims": ["k2-loans-create", "k2-repay-destroys", "k4-qe-deposits", "k7-share"]})


def main() -> None:
    cs_a()
    cs_e()
    cs_f()
    cs_g()
    cs_c()
    cs_d()
    explorer()


if __name__ == "__main__":
    main()
