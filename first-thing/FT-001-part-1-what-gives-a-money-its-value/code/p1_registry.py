"""Part 1's registry (step d): every printed number into ``results/numbers.json``, and every claim a form states.

From the study's folder: ``python code/p1_registry.py`` (``code/run.py`` calls it after the runs).

- The cards' runs (C21-C23, and the reused C18 and C20) and the reused A3 build give the computed numbers, each naming
  its card or mission in its origin.
- ``code/p1_cited.yaml`` gives the numbers read in a source at its page (``cited``), each with its locator.
- ``code/p1_claims.yaml`` gives the claims resting on sources and cases, each with the passage read and the copy held;
  the measured and judgement claims are written here, beside the numbers they print.
"""

from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

import yaml

from ft.numbers import Registry, cited, computed

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
ROOT = STUDY.parents[1]
RUNS = STUDY / "results" / "runs"

BIS_AS_OF = "2026-09-30"
FRAME_B_AS_OF = "2026-09-30"
CARD_DATA_AS_OF = "2026-10-10"

#: CS-A's monies: the run's name, the key's slug, the reader's name.
MONIES = [("USD", "usd", "the US dollar"), ("GBP", "gbp", "the pound sterling"), ("CHF", "chf", "the Swiss franc"),
          ("JPY", "jpy", "the yen"), ("FRF_then_euro_in_France", "fr", "the French franc, then the euro in France"),
          ("DEM_then_euro_in_Germany", "de", "the Deutsche Mark, then the euro in Germany"),
          ("Reichsmark", "rm", "the Reichsmark")]
PERIODS = {(1914, 1945): "1914-45", (1946, 1971): "1946-71", (1972, 1991): "1972-91", (1992, 2025): "1992-2025"}
SPAN_NAMES = {"before_1914": "before 1914", "1914_to_1971_07": "1914 to July 1971", "from_1971_08": "from August 1971"}


def run(card: str) -> dict:
    return json.loads((RUNS / f"{card}.json").read_text())["result"]


def keys_of(text: str) -> list[str]:
    return sorted(set(re.findall(r"\{\{\s*([A-Za-z0-9_.\-]+)", text)))


# --- the computed numbers -------------------------------------------------------------------------------------

def cs_a(reg: Registry) -> dict:
    r = run("C21-cs-a-what-a-unit-buys")
    origin = computed("code/p1_cs_a.py (card C21)")
    out = {}
    for name, slug, label in MONIES:
        m = r["monies"][name]
        for row in m["periods"]:
            p = PERIODS[tuple(row["period"])]
            if row.get("outside_span") or not row.get("computable"):
                continue
            k = f"cs-a_{slug}_{p}_loss"
            reg.put(k, row["yearly_loss_pct"], unit="% a year", fmt="{:.1f}%", origin=origin, as_of=BIS_AS_OF,
                    measure="average yearly loss of what a unit buys",
                    period=f"{row['base']} to {row['end']}", population=label)
            out[(slug, p)] = row
            if row.get("price_ratio"):
                reg.put(f"cs-a_{slug}_{p}_share-lost", 100 * (1 - 1 / row["price_ratio"]), unit="% of what a unit bought",
                        fmt="{:.0f}%", origin=origin, as_of=BIS_AS_OF,
                        measure="share of what a unit bought lost over the period",
                        period=f"{row['base']} to {row['end']}", population=label)
    for carrier, slug in (("FRF_then_euro_in_France", "fr"), ("DEM_then_euro_in_Germany", "de")):
        if carrier in r["euro_area_gap_points"]:
            reg.put(f"cs-a_euro-gap_{slug}", r["euro_area_gap_points"][carrier], unit="points a year", fmt="{:+.1f}",
                    origin=origin, as_of=BIS_AS_OF, measure="national index's yearly loss less the euro area's",
                    period="1991 to 2025", population="the euro in " + ("France" if slug == "fr" else "Germany"))
    # the euro since its creation: what a euro of 1999 has lost by 2025, from the run's grid (1999 on, no conversion)
    for carrier, slug, where in (("FRF_then_euro_in_France", "fr", "France"), ("DEM_then_euro_in_Germany", "de", "Germany")):
        g = {x["year"]: x["today_units"] for x in r["monies"][carrier]["grid"]}
        if 1999 in g and r["monies"][carrier]["last_reading"] == 2025:
            reg.put(f"cs-a_{slug}_euro-1999-2025_share-lost", 100 * (1 - 1 / g[1999]), unit="% of what a unit bought",
                    fmt="{:.0f}%", origin=origin, as_of=BIS_AS_OF,
                    measure="share of what a euro bought in 1999 lost by 2025", period="1999 to 2025",
                    population=f"the euro in {where}")
    recent = [out[(s, "1992-2025")]["yearly_loss_pct"] for _, s, _ in MONIES if (s, "1992-2025") in out]
    for k, v in (("min", min(recent)), ("max", max(recent))):
        reg.put(f"cs-a_1992-2025_loss-{k}", v, unit="% a year", fmt="{:.1f}%", origin=origin, as_of=BIS_AS_OF,
                measure=f"the {'smallest' if k == 'min' else 'largest'} average yearly loss of the six monies",
                period="1991 to 2025", population="the reader's monies (the first case study)")
    return r


def cs_b(reg: Registry) -> dict:
    r = run("C22-cs-b-the-franc")
    origin = computed("code/p1_cs_b.py (card C22)")
    for i, row in enumerate(r["bilateral_usd"]):
        if not row:
            continue
        span = f"{row['base'] + 1}-{row['end']}"
        for part, field in (("total", "total_log_points"), ("gap", "inflation_gap_log_points"), ("real", "real_rise_log_points")):
            reg.put(f"cs-b_usd_{span}_{part}", row[field], unit="log points", fmt="{:.0f}", origin=origin,
                    as_of=CARD_DATA_AS_OF, measure=f"the franc against the dollar: {part} (BIS rates and consumer prices)",
                    period=f"{row['base']} to {row['end']}", population="the Swiss franc")
        if "inflation_gap_share" in row:
            reg.put(f"cs-b_usd_{span}_gap-share", 100 * row["inflation_gap_share"], unit="% of the rise", fmt="{:.0f}%",
                    origin=origin, as_of=CARD_DATA_AS_OF, measure="share of the franc's rise against the dollar from the inflation gap",
                    period=f"{row['base']} to {row['end']}", population="the Swiss franc")
    for basket, label in (("N", "narrow"), ("B", "broad")):
        e = r["effective"][basket]
        for row in e["splits"]:
            if not row:
                continue
            span = f"{row['base'] + 1}-{row['end']}"
            for part, field in (("total", "total_log_points"), ("gap", "inflation_gap_log_points"), ("real", "real_rise_log_points")):
                reg.put(f"cs-b_{label}_{span}_{part}", row[field], unit="log points", fmt="{:.0f}", origin=origin,
                        as_of=CARD_DATA_AS_OF, measure=f"the franc's {label} effective rate: {part} (BIS)",
                        period=f"{row['base']} to {row['end']}", population="the Swiss franc")
            if "inflation_gap_share" in row:
                reg.put(f"cs-b_{label}_{span}_gap-share", 100 * row["inflation_gap_share"], unit="% of the rise",
                        fmt="{:.0f}%", origin=origin, as_of=CARD_DATA_AS_OF,
                        measure=f"share of the franc's {label} effective rise from the inflation gap",
                        period=f"{row['base']} to {row['end']}", population="the Swiss franc")
    pl = r["price_level"]
    names = {"DEU": "Germany", "FRA": "France", "ITA": "Italy", "AUT": "Austria"}
    for c, v in pl["che_over_neighbour"].items():
        reg.put(f"cs-b_price-level_over-{c.lower()}", v, unit="times", fmt="{:.2f}", origin=origin, as_of=CARD_DATA_AS_OF,
                measure="Swiss GDP price level over the neighbour's",
                period=str(pl["latest_common_year"]), population=f"Switzerland and {names[c]}")
    ex = r["exports_pct_gdp"]
    first, last = min(ex, key=int), max(ex, key=int)
    for k, y in (("first", first), ("last", last)):
        reg.put(f"cs-b_exports_{k}", ex[y], unit="% of GDP", fmt="{:.0f}%", origin=origin, as_of=CARD_DATA_AS_OF,
                measure="Swiss exports of goods and services (World Bank)", period=str(y), population="Switzerland")
    return r


CFA = {"BEN", "BFA", "CIV", "GNB", "MLI", "NER", "SEN", "TGO", "CMR", "CAF", "TCD", "COG", "GNQ", "GAB"}


def _another_states(v: dict, x: dict) -> bool:
    """A crossing left apart in a year card C23 classes as another state's or a shared money (its rule 3)."""
    span = v.get("another_states_money_years_by_economy", {}).get(x["money"])
    return bool(span) and span[0] <= int(x["entry"][:4]) <= span[1]


def _cfa_1994(x: dict) -> bool:
    """A CFA member's crossing inside the window of the January 1994 devaluation, counted once as one event (rule 4)."""
    return x["money"] in CFA and "1993-12" <= x["entry"][:7] <= "1994-12"


def cs_c(reg: Registry) -> dict:
    r = run("C28-cs-c-losses-by-era-kazakhstan")
    origin = computed("code/p1_cs_c.py (card C28, C23 corrected)")
    for variant, prefix in (("headline", "cs-c"), ("rr_cpi_only", "cs-c_cpi-only")):
        for span, s in r[variant]["spans"].items():
            cpi = variant != "headline"
            pop = "monies with consumer prices" if cpi else "every money with a price reading"
            # one rounding, at print: the rate from its counts, never the run's two-decimal rate_per_100 (2.25 printed 2.2
            # here and 2.3 in the figure's tooltip, 2026-10-21)
            rate = 100 * s["events"] / s["money_years"]
            reg.put(f"{prefix}_{span}_rate", rate, unit="per 100 money-years", fmt="{:.1f}", origin=origin,
                    as_of=FRAME_B_AS_OF,
                    measure=("consumer-price crises of a fifth or more begun" if cpi else "crises of a fifth or more in a year begun"),
                    period=SPAN_NAMES[span], population=pop)
            if variant != "headline":
                continue
            apart = [x for x in s["apart"] if not x["why"].startswith("a euro member")
                     and not _another_states(r[variant], x) and not _cfa_1994(x)]
            reg.put(f"{prefix}_{span}_apart", len(apart), unit="crises", fmt="{:.0f}", origin=origin, as_of=FRAME_B_AS_OF,
                    measure="crises left out, their start undatable",
                    period=SPAN_NAMES[span], population=pop)
            reg.put(f"{prefix}_{span}_rate_with-apart", 100 * (s["events"] + len(apart)) / s["money_years"],
                    unit="per 100 money-years", fmt="{:.1f}", origin=origin, as_of=FRAME_B_AS_OF,
                    measure="crises begun at a fifth or more a year, undatable starts included",
                    period=SPAN_NAMES[span], population=pop)
            reg.put(f"{prefix}_{span}_events", s["events"], unit="events", fmt="{:.0f}", origin=origin, as_of=FRAME_B_AS_OF,
                    measure="crises of a fifth or more in a year begun, unions once", period=SPAN_NAMES[span], population=pop)
            reg.put(f"{prefix}_{span}_money-years", s["money_years"], unit="money-years", fmt="{:,.0f}", origin=origin,
                    as_of=FRAME_B_AS_OF, measure="money-years with a price reading", period=SPAN_NAMES[span], population=pop)
            reg.put(f"{prefix}_{span}_units", s["units_with_reading"], unit="monies", fmt="{:.0f}", origin=origin,
                    as_of=FRAME_B_AS_OF, measure="monies counted, the euro and each union once",
                    period=SPAN_NAMES[span], population=pop)
            reg.put(f"{prefix}_{span}_share", 100 * s["share_with_event"], unit="% of monies", fmt="{:.0f}%", origin=origin,
                    as_of=FRAME_B_AS_OF, measure="share of monies with a crisis begun",
                    period=SPAN_NAMES[span], population=pop)
    y = run("C29-cs-c-years-in-crisis-kazakhstan")
    origin_y = computed("code/p1_cs_c_years.py (card C29, C24 corrected)")
    for span, s in y["rr_cpi_only"].items():
        reg.put(f"cs-c_years_cpi-only_{span}_share", s["share_pct"], unit="% of money-years", fmt="{:.1f}%", origin=origin_y,
                as_of=FRAME_B_AS_OF, measure="money-years with consumer prices up a fifth or more",
                period=SPAN_NAMES[span], population="monies with consumer prices")
    for span, s in y["headline"].items():
        reg.put(f"cs-c_years_{span}_share", s["share_pct"], unit="% of money-years", fmt="{:.1f}%", origin=origin_y,
                as_of=FRAME_B_AS_OF, measure="money-years with prices up a fifth or more",
                period=SPAN_NAMES[span], population="every money with a price reading")
    return r


def cs_d_f(reg: Registry) -> None:
    d = run("C20-cs-b-without-hyperinflation-years")["main"]
    o20 = computed("code/cs_b_trim.py (card C20)")
    pop = "17 rich economies"
    reg.put("cs-d_convertible_mean", d["convertible"]["mean"], unit="% a year", fmt="{:.1f}%", origin=o20,
            as_of=BIS_AS_OF, measure="mean consumer-price inflation in convertible years", period="1870-2020", population=pop)
    reg.put("cs-d_paper_mean", d["fiat"]["mean"], unit="% a year", fmt="{:.1f}%", origin=o20,
            as_of=BIS_AS_OF, measure="mean consumer-price inflation in inconvertible years", period="1870-2020", population=pop)
    lo, hi = d["interval"]
    reg.put("cs_b_gap_set_apart", d["gap"], unit="points a year", fmt="{:.1f}", origin=o20, as_of=BIS_AS_OF,
            measure="paper years' mean inflation less convertible years'", period="1870-2020", population=pop,
            low=lo, high=hi, matters=1.0, reading=d["reading"], claim_type="comparative")
    reg.put("cs-d_gap_low", lo, unit="points a year", fmt="{:.1f}", origin=o20, as_of=BIS_AS_OF,
            measure="interval of paper years' mean inflation less convertible years', low end", period="1870-2020", population=pop)
    reg.put("cs-d_gap_high", hi, unit="points a year", fmt="{:.1f}", origin=o20, as_of=BIS_AS_OF,
            measure="interval of paper years' mean inflation less convertible years', high end", period="1870-2020", population=pop)
    r20 = run("C20-cs-b-without-hyperinflation-years")
    for n, side in (("convertible", "convertible"), ("paper", "fiat")):
        reg.put(f"cs-d_{n}_n", d[side]["n"], unit="economy-years", fmt="{:,.0f}", origin=o20, as_of=BIS_AS_OF,
                measure=f"economy-years classed {n}", period="1870-2020", population=pop)
    reg.put("cs-d_set-apart_n", len(r20["set_apart"]), unit="economy-years", fmt="{:.0f}", origin=o20, as_of=BIS_AS_OF,
            measure="economy-years above 100% a year, set apart", period="1870-2020", population="17 rich economies (JST)")
    variants = (("cs_b_median_gap", r20["median_gap"], "the medians' gap (every year kept)"),
                ("cs_b_log_gap_set_apart", r20["log_rates_set_apart"], "the gap in log rates"),
                ("cs_b_gap_set_apart_from_1972", r20["fiat_from_1972"], "paper years from 1972 only"),
                ("cs_b_gap_set_apart_no_transition", r20["no_transition_years"], "transition years left out"),
                ("cs_b_gap_set_apart_own_block_returns", r20["own_block_returns_only"], "returns read in their own block only"),
                ("cs_b_gap_set_apart_earlier_resumption", r20["earlier_resumption"], "the earlier resumption dates"),
                ("cs_b_gap_set_apart_marked_suspensions", r20["marked_suspensions_inconvertible"], "the marked suspensions as paper"))
    for key, v, what in variants:
        lo_v, hi_v = v["interval"]
        reg.put(key, v["gap"], unit="points a year", fmt="{:.1f}", origin=o20, as_of=BIS_AS_OF,
                measure=f"paper years' inflation less convertible years': {what}", period="1870-2020", population=pop,
                low=lo_v, high=hi_v, matters=1.0, reading=v.get("reading") or ("effect" if lo_v > 1.0 else "bounded"),
                claim_type="comparative")
        for end, val in (("low", lo_v), ("high", hi_v)):
            reg.put(f"cs-d_variant_{key}_{end}", val, unit="points a year", fmt="{:.1f}", origin=o20, as_of=BIS_AS_OF,
                    measure=f"the interval of {what}, {end} end", period="1870-2020", population=pop)
    for era, e in r20["eras"].items():
        for cls in ("convertible", "fiat", "bretton_woods"):
            if e[cls]["n"]:
                reg.put(f"cs-d_era_{era}_{cls}", e[cls]["mean"], unit="% a year", fmt="{:.1f}%", origin=o20,
                        as_of=BIS_AS_OF, measure=f"mean consumer-price inflation, {'Bretton Woods' if cls == 'bretton_woods' else cls} years",
                        period=era, population=pop)
    f = run("C18-cs-a-consumer-prices-off-gold")["main"]
    o18 = computed("code/cs_a.py (card C18)")
    pop = "Bernanke and James's economies"
    r18 = run("C18-cs-a-consumer-prices-off-gold")
    for key, v, what in (("cs_a_pooled_no_exchange_control", r18["no_exchange_control"], "exits by exchange control left out"),
                         ("cs_a_pooled_no_spain", r18["no_spain"], "Spain left out")):
        reg.put(key, v["pooled"], unit="points a year", fmt="{:.1f}", origin=o18, as_of=BIS_AS_OF,
                measure=f"leavers' consumer-price inflation less stayers': {what}", period="1932-34", population=pop,
                low=v["lo"], high=v["hi"], matters=1.0, reading=v["reading"], claim_type="comparative")
        for end in ("lo", "hi"):
            reg.put(f"cs-f_variant_{key}_{end}", v[end], unit="points a year", fmt="{:.1f}", origin=o18, as_of=BIS_AS_OF,
                    measure=f"the interval of {what}, {'low' if end == 'lo' else 'high'} end", period="1932-34", population=pop)
    reg.put("cs-f_low", f["lo"], unit="points a year", fmt="{:.1f}", origin=o18, as_of=BIS_AS_OF,
            measure="interval of leavers' inflation less stayers', low end", period="1932-34", population=pop)
    reg.put("cs-f_economy-years", f["economy_years"], unit="economy-years", fmt="{:.0f}", origin=o18, as_of=BIS_AS_OF,
            measure="economy-years compared", period="1932-34", population=pop)
    reg.put("cs_a_pooled", f["pooled"], unit="points a year", fmt="{:.1f}", origin=o18, as_of=BIS_AS_OF,
            measure="leavers' consumer-price inflation less stayers'", period="1932-34", population=pop,
            low=f["lo"], high=f["hi"], matters=1.0, reading=f["reading"], claim_type="comparative")
    reg.put("cs-f_high", f["hi"], unit="points a year", fmt="{:.0f}", origin=o18, as_of=BIS_AS_OF,
            measure="interval of leavers' inflation less stayers', high end", period="1932-34", population=pop)


def cs_e(reg: Registry) -> None:
    rows = list(csv.DictReader((ROOT / "data" / "reconstructed" / "ft001-a3" / "series.csv").open(encoding="utf-8")))
    origin = computed("code/p1_registry.py (the A3 build, mission M4-A3)")
    for money, slug, label in (("USA", "greenback", "the greenback"), ("GBR", "pound", "the paper pound")):
        v = [(r["period"], float(r["value"])) for r in rows if r["money"] == money and r["value"] not in ("", "nan")]
        v = [t for t in v if not math.isnan(t[1])]
        low = min(v, key=lambda t: t[1])
        reg.put(f"a3_{slug}_low", 100 * low[1], unit="% of its value in gold", fmt="{:.0f}%", origin=origin,
                as_of="2026-10-02", measure="paper's value in gold at its low (par = 100%)", period=low[0], population=label)
    return None


# --- the claims -------------------------------------------------------------------------------------------------

JST_AS_OF = "2026-09-30"  # JST R6, frozen 2026-09-30


def k9_base(reg: Registry) -> None:
    r = run("C25-k9-crises-by-debt")
    o = computed("code/p1_k9_debt.py (card C25)")
    per, pop = "1871-2017", "18 economies (JST)"
    card = yaml.safe_load((STUDY / "cards" / "C25-k9-crises-by-debt.yaml").read_text())["parameters"]
    for k, v in card["crisis_line"].items():
        reg.put("k9b_line" + ("" if k == "main" else "10"), 100 * v, unit="% a year", fmt="{:.0f}%", origin=o,
                as_of=JST_AS_OF, measure=f"yearly rise in consumer prices marking a crisis ({k})", period=per,
                population=pop)
    for edge in sorted({e for b in card["bands_debtgdp"] for e in b if e is not None}):
        reg.put(f"k9b_edge_{round(100 * edge)}", 100 * edge, unit="% of GDP", fmt="{:.0f}%", origin=o, as_of=JST_AS_OF,
                measure="band edge on public debt", period=per, population=pop)
    names = {"peace": ("p", "away from the world wars and three others"), "near_war": ("w", "near the world wars and three others"),
             "all": ("a", "all years")}
    for line, suffix in (("main", ""), ("variant", "10")):
        res, lab = r[line], f"{100 * card['crisis_line'][line]:.0f}%"
        for s, (code, what) in names.items():
            for i, e in enumerate(res["settings"][s], start=1):
                lo, hi = e["band"]["from"], e["band"]["to"]
                band = (f"debt below {100 * hi:.0f}%" if lo is None else f"debt above {100 * lo:.0f}%" if hi is None
                        else f"debt {100 * lo:.0f}-{100 * hi:.0f}%")
                key = f"k9b_{code}{i}"
                reg.put(f"{key}_n{suffix}", e["rows"], unit="years", fmt="{:,.0f}", origin=o, as_of=JST_AS_OF,
                        measure=f"economy-years, {band}, {what}, {lab} line", period=per, population=pop)
                if not suffix:
                    reg.put(f"{key}_econ", e["economies"], unit="economies", fmt="{:,.0f}", origin=o, as_of=JST_AS_OF,
                            measure=f"economies, {band}, {what}", period=per, population=pop)
                reg.put(f"{key}_hit{suffix}", e["followed"], unit="years", fmt="{:,.0f}", origin=o, as_of=JST_AS_OF,
                        measure=f"years followed by a crisis start within 3 years ({band}, {what}, {lab} line)",
                        period=per, population=pop)
                if "bound" in e:
                    reg.put(f"{key}_bound{suffix}", e["bound"]["value"], unit="%", fmt="{:.1f}%", origin=o,
                            as_of=JST_AS_OF, measure=f"{e['bound']['kind']}, one-sided 95% bound ({band}, {what})",
                            period=per, population=pop)
                else:
                    reg.put(f"{key}_share{suffix}", e["share"], unit="%", fmt="{:.1f}%", origin=o, as_of=JST_AS_OF,
                            measure=f"share followed by a crisis start ({band}, {what}, {lab} line)", period=per,
                            population=pop, low=e["low"], high=e["high"])
                    for end in ("low", "high"):
                        reg.put(f"{key}_share{suffix}_{end}", e[end], unit="%", fmt="{:.1f}%", origin=o,
                                as_of=JST_AS_OF, measure=f"95% interval of the share, {end} end ({band}, {what})",
                                period=per, population=pop)
            m = res["missed_beginnings"][s]
            reg.put(f"k9b_missed_{code}{suffix}", m["count"], unit="beginnings", fmt="{:,.0f}", origin=o, as_of=JST_AS_OF,
                    measure=f"crisis beginnings no year reaches ({what}, {lab} line)", period=per, population=pop)


def put_sourced(reg: Registry) -> None:
    for e in yaml.safe_load((HERE / "p1_cited.yaml").read_text()):
        reg.put(e["key"], e["value"], unit=e["unit"], fmt=e["fmt"], as_of=e["as_of"],
                origin=cited(e["source"], e["locator"], e.get("url")),
                measure=e["measure"], period=e["period"], population=e["population"])
    for c in yaml.safe_load((HERE / "p1_claims.yaml").read_text()):
        reg.put_claim(c["id"], text=c["text"], type=c["type"], keys=keys_of(c["text"]) or None,
                      sources=c["sources"], component=c["component"])


def put_measured_and_judgement(reg: Registry) -> None:
    def m(cid, text, card, component, measure, period, population, **kw):
        reg.put_claim(cid, text=text, type="measured", card=card, component=component, keys=keys_of(text) or None,
                      scope={"measure": measure, "period": period, "population": population}, **kw)

    def j(cid, text, component, **kw):
        reg.put_claim(cid, text=text, type="judgement", component=component, keys=keys_of(text) or None, **kw)

    m("k9-base-rate", "In JST's eighteen economies, away from the world wars and three other wars, a crisis started or "
      "restarted within three years after {{k9b_p1_hit}} of {{k9b_p1_n}} years with public debt below {{k9b_edge_60}} of "
      "GDP, {{k9b_p2_hit}} of {{k9b_p2_n}} between {{k9b_edge_60}} and {{k9b_edge_100}}, and {{k9b_p3_hit}} of "
      "{{k9b_p3_n}} above {{k9b_edge_100}}, in {{k9b_p3_econ}} economies ({{k9b_p1_share}}, {{k9b_p2_share}} and "
      "{{k9b_p3_share}} of the years), other wars among those years; for the last, a "
      "share above about {{k9b_p3_share_high}} is ruled out by a bound from only {{k9b_p3_econ}} economies; near those "
      "wars, after {{k9b_w1_hit}} of {{k9b_w1_n}}, {{k9b_w2_hit}} of {{k9b_w2_n}} and {{k9b_w3_hit}} of {{k9b_w3_n}}; a "
      "count of the past, not a forecast or a threshold.", "C25", "K9",
      "years followed by a crisis start within three years, by public debt", "1871-2017", "eighteen economies (JST R6)")

    six = "the dollar, the pound, the Swiss franc, the yen, and the euro's prices in France and Germany"
    for p, words in (("1914-45", "From 1913 (or its first year) to 1945"), ("1946-71", "From 1945 (or its first year) to 1971"),
                     ("1972-91", "From 1971 to 1991"), ("1992-2025", "From 1991 to 2025")):
        parts = [f"{label} {{{{cs-a_{slug}_{p}_loss}}}}" for _, slug, label in MONIES
                 if f"cs-a_{slug}_{p}_loss" in reg.entries]
        m(f"cs-a-{p}", f"{words}, one unit lost, a year on average, this share of what it bought: " + "; ".join(parts) + ".",
          "C21", "K5", "yearly loss of what one unit buys (BIS consumer prices)", p, six)
    m("cs-a-1992-2025-cumulative", "From 1991 to 2025 a dollar lost {{cs-a_usd_1992-2025_share-lost}} of what it bought, a "
      "pound {{cs-a_gbp_1992-2025_share-lost}}, a Swiss franc {{cs-a_chf_1992-2025_share-lost}} and a yen "
      "{{cs-a_jpy_1992-2025_share-lost}}.", "C21", "K5", "share of what one unit bought in 1991 lost by 2025 (BIS consumer "
      "prices)", "1992-2025", "the dollar, the pound, the Swiss franc and the yen")
    m("cs-a-euro-1999", "From 1999 to 2025 a euro lost {{cs-a_fr_euro-1999-2025_share-lost}} of what it bought in 1999 "
      "on France's consumer prices and {{cs-a_de_euro-1999-2025_share-lost}} on Germany's.", "C21", "K5",
      "share of what a euro bought in 1999 lost by 2025 (BIS consumer prices)", "1999-2025",
      "the euro's prices in France and Germany")
    m("cs-a-euro-gap", "From 1992 to 2025 (measured from 1991) the yearly loss on France's own index differed from the euro area's index by "
      "{{cs-a_euro-gap_fr}} points, and on Germany's by {{cs-a_euro-gap_de}} (a minus: the national index lost less).",
      "C21", "K1",
      "national index's yearly loss less the euro area's", "1991-2025", "the euro's prices in France and Germany")
    m("cs-b-usd", "From 1970 to 2025 the franc rose {{cs-b_usd_1971-2025_total}} log points against the dollar: "
      "{{cs-b_usd_1971-2025_gap}} from Switzerland's lower inflation and {{cs-b_usd_1971-2025_real}} from a franc that truly "
      "got dearer.", "C22", "K6", "the franc against the dollar, split in logs", "1970-2025", "the Swiss franc")
    m("cs-b-effective", "Against its trading partners (the BIS's narrow basket) the franc rose {{cs-b_narrow_1971-2025_total}} "
      "log points from 1970 to 2025: {{cs-b_narrow_1971-2025_gap}} from the inflation gap and {{cs-b_narrow_1971-2025_real}} "
      "a real rise.", "C22", "K6", "the franc's narrow effective rate, split in logs", "1970-2025", "the Swiss franc")
    pl = [k for k in reg.entries if k.startswith("cs-b_price-level_over-")]
    m("cs-b-price-level", "Switzerland's GDP price level was " + ", ".join(
        "{{" + k + "}} times " + {"over-deu": "Germany's", "over-fra": "France's", "over-ita": "Italy's", "over-aut": "Austria's"}[k.rsplit("_", 1)[1]]
        for k in sorted(pl)) + ".", "C22", "K6", "GDP price level, Switzerland over each neighbour", "latest common year",
      "Switzerland and its neighbours")
    m("cs-b-exports", "Swiss exports went from {{cs-b_exports_first}} of GDP to {{cs-b_exports_last}} while the franc rose.",
      "C22", "K6", "exports of goods and services, % of GDP", "1971-2025", "Switzerland")
    m("cs-c", "A crisis of prices rising a fifth or more in a year began {{cs-c_before_1914_rate}} times per 100 money-years before 1914, "
      "{{cs-c_1914_to_1971_07_rate}} from 1914 to July 1971 and {{cs-c_from_1971_08_rate}} from August 1971; "
      "{{cs-c_before_1914_share}}, {{cs-c_1914_to_1971_07_share}} and {{cs-c_from_1971_08_share}} of the monies with a "
      "reading had at least one such crisis; the count is of crises begun, not of years spent in crisis.", "C28", "K5", "crises of a fifth or more in a year begun, per 100 money-years",
      "1800-2025", "monies with a price reading in frame b's panel, the euro and each union once")
    m("cs-d", "In seventeen rich economies, 1870-2020, consumer prices rose {{cs-d_convertible_mean}} a year on average in "
      "convertible years and {{cs-d_paper_mean}} in paper years (the world-war years, the fixed-rate years of 1946-71 and the economy-years of inflation "
      "above 100% each apart): a gap of {{cs_b_gap_set_apart}} points "
      "({{cs-d_gap_low}} to {{cs-d_gap_high}}).", "C20", "K5", "mean consumer-price inflation by convertibility",
      "1870-2020", "17 rich economies (JST)", reading="effect", claim_type="comparative")
    m("cs-f", "In 1932-34 the leavers' consumer-price inflation was not clearly higher than the stayers': the gap was "
      "{{cs_a_pooled}} points a year ({{cs-f_low}} to {{cs-f_high}}), ruling out only a gap above about {{cs-f_high}} points.", "C18", "K5",
      "leavers' consumer-price inflation less stayers'", "1932-34", "Bernanke and James's economies (JST)",
      reading="bounded", claim_type="comparative")
    m("cs-e", "The greenback fell to {{a3_greenback_low}} of its value in gold in its lowest month and was back at par by the "
      "end of 1878; the paper pound, read by yearly averages, fell to {{a3_pound_low}} and was back at par in 1821.", "M4-A3", "K3",
      "paper's value in gold (par = 100%)", "1800-1821; 1862-1878", "the paper pound; the greenback")
    m("frame-b-dollar", "The dollar's consumer prices have not risen a fifth or more in a year since 1920, by our rule of "
      "three successive twelve-month readings.", "M3-frame-b", "K5", "price rises of a fifth or more in a year (frame b)", "1920-2026",
      "the US dollar")

    j("h1a-floor", "We read the first support this way: payments owed in a money by law, taxes payable in it and debts "
      "settled in it, give it a demand that, in theory, if those payments are heavy enough, rules out its being worth "
      "nothing; that floor rules out a value of zero, not a "
      "collapse under issue without limit, and it is not a necessity, since a money with no state behind it kept "
      "circulating beside a stronger money, for small payments and change.", "K2")
    j("h1d-backing", "We read the cases this way: a backing did not guarantee a money's safety; prices were flat under gold on average, and rose more slowly than under paper in the same economies, mostly in different decades, but it was suspended in war, kept by law "
      "at home while prices doubled, broken when the state's debts pressed on it, and given up "
      "outside a world war.", "K5")
    j("k4-peg-between", "In our reading, buying the state's debt to hold its price or yield (the Fed 1942-51, the "
      "Bank of Japan 2016-24) lies between the four forms and market purchases with no promise: bought in the market, "
      "at a price the central bank had committed to hold.", "K4")
    j("k4-converse", "We read the cases this way: money created for the state stands behind the destroyed monies the "
      "sources studied, but it did not always destroy a money, and, though theory gives a limit on what printing can raise for long, no "
      "source read says where it lay for a money before the fact.", "K4")
    j("k4-linked", "Our reading is that the two supports are linked: the payments owed keep a money wanted, and the "
      "restraint on its issuer keeps that want from being swamped.", "K4")
    j("k5-1971-not-collapse", "In our reading, the dollar did not collapse once its link to gold was cut because what kept "
      "it wanted was still there, taxes and debts owed in dollars and its place in trade and reserves; its inflation, "
      "already rising before 1971, came down after 1979, when the Fed changed its method and let interest rates rise high; so paper is not doomed by being paper: behind the "
      "destroyed monies the sources studied, most if not all, stood a state financing itself with money.", "K5")
    j("cs-c-mix", "The monies changed with the eras: the panel holds {{cs-c_before_1914_units}} monies before 1914 and "
      "{{cs-c_from_1971_08_units}} after July 1971, many of them new states' monies; the rates are per money-year, but the "
      "mix of monies is not the same across eras.", "K5")
    j("k2-two-claims", "In our reading, though, Starr's taxes and the fiscal theory claim different things: taxes payable in a "
      "money keep its price above zero, while the fiscal theory also sets the level of prices from the surpluses the state "
      "is expected to run.", "K2")
    j("trust", "What readers call trust is, in our reading, the expectation that others will take the money tomorrow; the "
      "floor and a restraint on the issuer are what make that expectation reasonable; in the one case found of a money with neither, Somalia's shilling in the years no government supported it, trust kept it in use beside the dollar, mostly for small payments and change; one case cannot show how far trust alone goes; so money is not just trust.", "K2")
    j("k9-table", "We place today's monies on the same supports, each cell from a document read, never from one year's "
      "inflation or one window's real rate.", "K9")
    j("k10-questions", "Our reading gives five questions to ask of any money: are payments owed in it by law; who can make "
      "more of it, and what stops them; is the state paying its way with money created for it, in any form; is a rival "
      "at hand; and are people quietly switching.", "K10")
    m("cs-c-years", "Prices rose a fifth or more in {{cs-c_years_before_1914_share}} of money-years before 1914, "
      "{{cs-c_years_1914_to_1971_07_share}} from 1914 to July 1971 and {{cs-c_years_from_1971_08_share}} from August 1971.",
      "C29", "K5",
      "share of money-years with prices up a fifth or more", "1800-2025",
      "monies with a price reading in frame b's panel, the euro and each union once")
    j("cs-c-not-new", "Inflation crises are not new: in our reading of C28 (C23 corrected), a new one began in each of the three spans, "
      "before 1914 as after 1971, and most monies with a price reading had at least one.", "K5")
    j("cs-c-longer", "In our reading of C28 and C29 together (C23 and C24 corrected), fewer crises began per 100 money-years after 1971 than before "
      "1914 while a larger share of money-years was spent in one, so, on average, later crises lasted longer (an inference "
      "from a share and a rate, across monies that differ by era, not a measure of each crisis), with or without the "
      "crises left out for want of a start date, and on consumer prices alone; the spans are dates, not monetary systems.", "K5")
    m("cs-c-cpi-only", "On consumer prices alone, a crisis of a fifth or more in a year began {{cs-c_cpi-only_before_1914_rate}} "
      "times per 100 money-years before 1914 and {{cs-c_cpi-only_from_1971_08_rate}} from August 1971, and prices rose a "
      "fifth or more in {{cs-c_years_cpi-only_before_1914_share}} and {{cs-c_years_cpi-only_from_1971_08_share}} of "
      "money-years.", "C29", "K5", "crises begun per 100 money-years, and share of money-years in a crisis, consumer prices only",
      "1800-2025", "monies with consumer prices in frame b's panel, the euro and each union once")
    j("cs-f-reading", "In our reading, the central estimate of the leavers' gap in 1932-34 points the same way as "
      "Bernanke and James's wholesale prices, but with so few economies the data cannot pin it down.", "K5")
    j("k2-ftpl-rival", "In our reading, the fiscal theory is the main alternative to our reading of the restraint: in it, prices are "
      "held mainly by the surpluses the state is expected to run, not by a central bank's mandate alone; the study does not test one "
      "against the other.", "K2")
    j("k9-levels", "In our reading, the study's episodes say that a central bank holding about half of its state's "
      "bonds has not by that alone destroyed the yen, one case; that monies a central bank financed had prices rising fast "
      "without being destroyed (the US 1946-47, as wartime price controls ended, Italy 1973-74, and Japan 1944-49, close to the line for a destroyed money late in 1945); that "
      "the destroyed monies went with money created for the state, most plainly a central bank as the state's main or only lender; that "
      "Turkey's rate cut below inflation from 2021 went with inflation near three-quarters in 2022 and its later rises "
      "with inflation near a third by 2025, one case and an association; and that the two studies of deficits and inflation read "
      "measure deficits, not debt, and give no level of debt that matters for low-inflation monies. These are readings of past episodes, not a forecast.", "K9")
    j("k9-today-reading", "In our reading, the restraint on the dollar, the euro, the Swiss franc and the yen is how each "
      "central bank reacts when inflation rises, with public finances that let it do so; a written mandate that includes "
      "stable prices is its legal form, which has not stopped the Bank of Japan from owning nearly half of its state's "
      "bonds; whether it holds against public finances shows only in the outcome.", "K9")
    j("k9-bitcoin-reading", "On this study's supports, bitcoin has neither the floor nor an issuer to restrain: it holds "
      "value by convention alone.", "K9")
    j("headline", "Paper buys a sandwich, in our reading, because people owe taxes and debts in it and expect others to take it; what it "
      "keeps depends on how much more of it is made and what restrains its issuer, and a backing did not guarantee its safety; "
      "from 1991 to 2025 a dollar lost {{cs-a_usd_1992-2025_share-lost}} of what it bought, a pound "
      "{{cs-a_gbp_1992-2025_share-lost}}, a Swiss franc {{cs-a_chf_1992-2025_share-lost}} and a yen "
      "{{cs-a_jpy_1992-2025_share-lost}}, and from 1999 to 2025 a euro lost {{cs-a_de_euro-1999-2025_share-lost}} of what "
      "it bought in Germany.", "K10", headline=True)


def fed_1979(reg: Registry) -> None:
    """US consumer prices before and after the Fed's change of 1979, from the BLS's CPI-U (CUUR0000SA0) over the dates
    of FRED's CPIAUCNS frozen 2026-09-30 (reader panel; the original agency, the author, 2026-10-21)."""
    import pandas as pd
    from ft.data import agency
    cpi = agency.series("CPIAUCNS", "2026-09-30")
    cpi.index = pd.to_datetime(cpi.index).strftime("%Y-%m")
    yoy = 100 * (cpi / cpi.shift(12) - 1)
    o = computed("code/p1_registry.py (the BLS's CPI-U, CUUR0000SA0: the original of FRED's CPIAUCNS)")
    for key, month in (("k5_us_cpi_1980-03", "1980-03"), ("k5_us_cpi_1983-12", "1983-12")):
        reg.put(key, float(yoy[month]), unit="% over twelve months", fmt="{:.1f}%", origin=o, as_of="2026-10-21",
                measure="US consumer prices, change over twelve months", period=month, population="the United States")


def today(reg: Registry) -> None:
    """Today's public finances and bitcoin's swings, from frozen FRED series (2026-10-11)."""
    import pandas as pd
    from ft.data import fred
    debt = fred.read("FYGFGDQ188S", "2026-10-11")
    debt.index = pd.to_datetime(debt.index).strftime("%Y-%m")
    o = computed("code/p1_registry.py (frozen FRED FYGFGDQ188S, FYOIGDA188S, CBBTCUSD)")
    for key, month, period in (("k9_us_debt_2026", "2026-01", "first quarter of 2026"),
                               ("k9_us_debt_2019", "2019-10", "fourth quarter of 2019")):
        reg.put(key, float(debt[month]), unit="% of GDP", fmt="{:.0f}%", origin=o, as_of="2026-10-11",
                measure="US federal debt held by the public, share of GDP", period=period, population="the United States")
    interest = fred.read("FYOIGDA188S", "2026-10-11")
    interest.index = pd.to_datetime(interest.index).strftime("%Y")
    reg.put("k9_us_interest_2025", float(interest["2025"]), unit="% of GDP", fmt="{:.1f}%", origin=o, as_of="2026-10-11",
            measure="US federal interest outlays, share of GDP", period="fiscal year 2025", population="the United States")
    btc = fred.read("CBBTCUSD", "2026-10-11").dropna()
    btc.index = pd.to_datetime(btc.index)
    high = float(btc["2021-11"].max())
    low = float(btc["2022-11"].min())
    reg.put("k9_btc_drawdown", 100 * (1 - low / high), unit="% of its dollar price", fmt="{:.0f}%", origin=o,
            as_of="2026-10-11", measure="fall in bitcoin's dollar price, highest to lowest daily price (Coinbase)",
            period="November 2021 to November 2022", population="bitcoin")


# --- the correction of 2026-10-21 (Kazakhstan's IFS index; the methods' research log) ----------------------------------


def correction(reg: Registry) -> None:
    """The numbers of the correction note: the splice's ratio from the frozen files (``ft.data.splices``),
    Kazakhstan's new crossing from frame b."""
    from ft.data import splices
    kw = dict(as_of=FRAME_B_AS_OF, period="2019-2024", population="Kazakhstan")
    reg.put("corr_kaz_ratio", splices.ratio(splices.SPLICES[0]), unit="ratio", fmt="{:.4f}",
            origin=computed("toolkit/ft/data/splices.py: IFS A.KZ.PCPI_IX 2020 over the World Bank's FP.CPI.TOTL KAZ 2020"),
            measure="IFS's annual price index for Kazakhstan over the World Bank's, 2020", **kw)
    row = next(r for r in csv.DictReader(open(ROOT / "data" / "reconstructed" / "ft001-b" / "series.csv"))
               if r["money"] == "KAZ" and r["entry_date"] == "2022-12")
    reg.put("corr_kaz_2022_entry", float(row["entry_measure"]), unit="%", fmt="{:.1f}%",
            origin=computed("data/reconstructed/ft001-b/series.csv, KAZ 2022-12, entry_measure"), as_of=FRAME_B_AS_OF,
            measure="Kazakhstan's twelve-month price rise at its December 2022 crossing", period="2022-12",
            population="Kazakhstan")
    congo_the_other_way(reg)


def congo_the_other_way(reg: Registry) -> None:
    """Part 1's rate from August 1971 if Congo's (DR) 2009 and 2010 had no price reading (the separate correction
    proposed for Congo's index, 2026-10-22): C28's count over C28's money-years less the years of those two that C28's
    panel reads for Congo, the panel rebuilt by frame b's code and its digest checked against C28's run."""
    import sys
    sys.path.insert(0, str(HERE))
    from ft import cards
    import p1_cs_c as C
    r = run("C28-cs-c-losses-by-era-kazakhstan")
    s = r["headline"]["spans"]["from_1971_08"]
    pan = C.P.Panel()
    if C.P.records(pan)[2] != r["panel_digest"]:
        raise SystemExit("the rebuilt panel differs from C28's")
    ends = (C.P.common_end(pan.have_monthly(), 12), C.P.common_end(pan.have_annual(), 1))
    units = C.Units(cards.read(C.CARD)["parameters"])
    y0, y1 = units.p["years"]
    lost = [y for y in sorted(C.reading_years(pan, "COD", *ends, False, y0, y1))
            if y in (2009, 2010) and units.of("COD", y) is not None]
    my = s["money_years"] - len(lost)
    o = computed("code/p1_registry.py: C28's count and money-years from August 1971, less Congo's 2009 and 2010 "
                 "as C28's panel reads them")
    kw = dict(as_of=FRAME_B_AS_OF, period="August 1971 to 2025", population="every money with a price reading")
    reg.put("corr_cd_money-years_other", my, unit="money-years", fmt="{:,.0f}", origin=o,
            measure="money-years with a price reading, Congo's 2009 and 2010 read as unreadable", **kw)
    reg.put("corr_cd_rate_other", 100 * s["events"] / my, unit="per 100 money-years", fmt="{:.1f}", origin=o,
            measure="crises of a fifth or more in a year begun, Congo's 2009 and 2010 read as unreadable", **kw)
    reg.put("corr_cd_rate_other_exact", 100 * s["events"] / my, unit="per 100 money-years", fmt="{:.4f}", origin=o,
            measure="crises of a fifth or more in a year begun, Congo's 2009 and 2010 read as unreadable", **kw)
    reg.put("corr_rate_exact", 100 * s["events"] / s["money_years"], unit="per 100 money-years", fmt="{:.4f}",
            origin=computed("code/p1_cs_c.py (card C28, C23 corrected)"),
            measure="crises of a fifth or more in a year begun", **kw)

def main() -> Registry:
    reg = Registry(STUDY / "results" / "numbers.json", {})
    cs_a(reg)
    cs_b(reg)
    cs_c(reg)
    cs_d_f(reg)
    cs_e(reg)
    k9_base(reg)
    today(reg)
    fed_1979(reg)
    put_sourced(reg)
    put_measured_and_judgement(reg)
    correction(reg)
    reg.save()
    return reg


if __name__ == "__main__":
    main()
