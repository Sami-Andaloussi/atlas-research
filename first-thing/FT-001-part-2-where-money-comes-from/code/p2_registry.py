"""Part 2's registry (step d): every printed number into ``results/numbers.json``, and every claim a form states.

From the study's folder: ``python code/p2_registry.py`` (``code/run.py`` calls it after the runs).

- The cards' runs give the computed numbers, each naming its card in its origin: the rebuild's C35 (CS-A), C36 (CS-E),
  C37 (CS-F), C38 (CS-G) and C39 (K11's count), and the reused C28 and C29 (CS-C), C30 (CS-B) and C31 (CS-D).
- Four numbers are read from frozen series here (each from its original agency over its FRED copy's dates), with no choice a result could tune: the US base over the windows
  the Fed's own statements date (K4), M2 and bank loans over 2022 (K4), and output per hour since 1947 (K6).
- ``code/p2_cited.yaml`` gives the numbers read in a source at its page (``cited``), each with its locator.
- ``code/p2_claims.yaml`` gives the claims resting on sources and cases, each with the passage read and the copy held;
  the measured and judgement claims are written here, beside the numbers they print.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import pandas as pd
import yaml

from ft.data import fred
from ft.data import agency
from ft.numbers import Registry, cited, computed

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent
RUNS = STUDY / "results" / "runs"

CARD_DATA_AS_OF = "2026-10-10"
GRID_AS_OF = "2026-10-01"  # a grid of monies: IMF IFS, the World Bank, FRED and the ECB frozen by 2026-10-01

#: CS-A's economies: the run's name, the key's slug, the statistic, the reader's name.
CS_A = [("us", "us", "M2", "the United States"), ("euro_area", "ea", "M3", "the euro area"),
        ("britain", "gb", "M4", "Britain")]
#: CS-E's rows, in the order the text and the figure give them.
CS_E_ROWS = {"real_and_market_priced": "real assets and market-priced claims, real holding gains",
             "fund_and_pension": "fund and pension claims, real holding gains",
             "nominal_claims": "debt securities, currency and deposits, real holding gains",
             "net_investment": "net investment (the Fed's line)",
             "erosion_of_other_nominal_assets": "inflation's erosion of other nominal assets",
             "gain_on_liabilities": "inflation's gain on liabilities",
             "other_volume": "other volume changes"}

SHORT_ROWS = {"real_and_market_priced": "gains on real assets and priced claims", "net_investment": "net investment"}


def run(card: str) -> dict:
    return json.loads((RUNS / f"{card}.json").read_text())["result"]


def keys_of(text: str) -> list[str]:
    return sorted(set(re.findall(r"\{\{\s*([A-Za-z0-9_.\-]+)", text)))


# --- the computed numbers -------------------------------------------------------------------------------------

def cs_a(reg: Registry) -> None:
    r = run("C35-cs-a-currency-share")
    o = computed("code/p2_cs_a.py (card C35)")
    for name, slug, stat, label in CS_A:
        e = r[name]
        reg.put(f"cs-a_{slug}_latest", e["latest"], unit=f"% of {stat}", fmt="{:.1f}%", origin=o, as_of=CARD_DATA_AS_OF,
                measure=(f"notes and coin in circulation, banks' holdings included, share of {stat}" if slug == "gb"
                         else f"notes and coin held by the public, share of {stat}"), period=e["last"], population=label)
        for end in ("lowest", "highest"):
            reg.put(f"cs-a_{slug}_{end[:-3] if end == 'lowest' else 'high'}", e[end], unit=f"% of {stat}", fmt="{:.1f}%",
                    origin=o, as_of=CARD_DATA_AS_OF,
                    measure=f"{'lowest' if end == 'lowest' else 'highest'} monthly share of notes and coin in {stat}",
                    period=f"{e['first']} to {e['last']} ({e[end + '_month']})", population=label)
    b = r["britain_ifs"]
    reg.put("cs-a_gb-ifs_latest", b["latest"], unit="% of money and quasi-money", fmt="{:.1f}%", origin=o,
            as_of=CARD_DATA_AS_OF, measure="currency outside banks, share of money and quasi-money (IMF)",
            period=b["last"], population="Britain")
    w = r["wider"]
    for slug, s, pop in (("all", w["all_summary"], "IMF IFS economies with both lines"),
                         ("modal", w["modal_year_summary"], f"economies with latest month in {w['modal_year']}")):
        reg.put(f"cs-a_{slug}_n", s["n"], unit="economies", fmt="{:.0f}", origin=o, as_of=CARD_DATA_AS_OF,
                measure="economies with both IMF lines", period="each economy's latest month", population=pop)
        reg.put(f"cs-a_{slug}_median", s["median"], unit="% of money and quasi-money", fmt="{:.1f}%", origin=o,
                as_of=CARD_DATA_AS_OF, measure="median share of currency outside banks", period="each economy's latest month",
                population=pop)
        reg.put(f"cs-a_{slug}_half", s["at_or_above_half"], unit="economies", fmt="{:.0f}", origin=o, as_of=CARD_DATA_AS_OF,
                measure="economies where currency is half or more", period="each economy's latest month", population=pop)
    names = {"GW": "Guinea-Bissau", "IQ": "Iraq", "AF": "Afghanistan"}
    for code, label in names.items():
        e = w["economies"][code]
        reg.put(f"cs-a_wider_{code.lower()}", e["share"], unit="% of money and quasi-money", fmt="{:.1f}%", origin=o,
                as_of=CARD_DATA_AS_OF, measure="currency outside banks, share of money and quasi-money (IMF)",
                period=e["latest_month"], population=label)


def cs_e(reg: Registry) -> None:
    r = run("C36-cs-e-household-real-wealth")
    o = computed("code/p2_cs_e.py (card C36)")
    pop = "US households and nonprofits (Z.1)"
    for span, t in r["spans"].items():
        for row, label in CS_E_ROWS.items():
            reg.put(f"cs-e_{span}_{row}", t[row], unit="trillions of Dec-2025 dollars", fmt="${:.1f} trillion", origin=o,
                    as_of=CARD_DATA_AS_OF, measure=label, period=span, population=pop)
        reg.put(f"cs-e_{span}_real-change", t["real_change"], unit="trillions of Dec-2025 dollars", fmt="${:.1f} trillion",
                origin=o, as_of=CARD_DATA_AS_OF, measure="real change in net worth", period=span, population=pop)
        if span == "1952-2025":
            for row in ("real_and_market_priced", "net_investment"):
                reg.put(f"cs-e_{span}_{row}_share", t["shares_pct"][row], unit="% of the real change", fmt="{:.0f}%",
                        origin=o, as_of=CARD_DATA_AS_OF, measure=f"share of the real change: {SHORT_ROWS[row]}",
                        period=span, population=pop)
            fixed = -(t["nominal_claims"] + t["erosion_of_other_nominal_assets"])
            reg.put(f"cs-e_{span}_liabilities_over_fixed", 100 * t["gain_on_liabilities"] / fixed, unit="%",
                    fmt="{:.0f}%", origin=o, as_of=CARD_DATA_AS_OF,
                    measure="inflation's gain on debts over its loss on assets fixed in dollars",
                    period=span, population="US households and nonprofits")
    for line, label in (("F51", "equity"), ("F52", "investment-fund shares")):
        e = r["euro_area_beside"][line]
        for side, pop2 in (("euro_area", "euro-area households (ECB)"), ("us", "US households (Z.1)")):
            reg.put(f"cs-e_{line.lower()}_{side}_2022", e[side]["2022"], unit="% of the start-of-year level", fmt="{:.1f}%",
                    origin=o, as_of=CARD_DATA_AS_OF, measure=f"real holding gains on {label}", period="2022", population=pop2)


def cs_f(reg: Registry) -> None:
    r = run("C37-cs-f-money-output-prices")
    o = computed("code/p2_cs_f.py (card C37)")
    names = {"money": "M2", "real_output": "real GDP", "prices": "the GDP price index", "velocity": "velocity (GDP over M2)"}
    for span, s in r["spans"].items():
        for k, label in names.items():
            reg.put(f"cs-f_{span}_{k}", s[k], unit="% a year", fmt="{:.1f}%", origin=o, as_of=CARD_DATA_AS_OF,
                    measure=f"average yearly growth of {label}", period=f"{s['from']} to {s['to']}",
                    population="the United States")


def cs_g(reg: Registry) -> None:
    r = run("C38-cs-g-money-and-real-growth")
    o = computed("code/p2_cs_g.py (card C38)")
    for k, field, what in (("windows", "windows_drawn", "ten-year windows drawn"), ("monies", "monies_drawn", "economies drawn"),
                           ("calm", "calm", "calm windows drawn (broad money growth at or below the line)"),
                           ("left-out", "windows_left_out", "filled windows left out")):
        reg.put(f"cs-g_{k}", r[field], unit="windows" if k != "monies" else "economies", fmt="{:,.0f}", origin=o,
                as_of=GRID_AS_OF, measure=what, period="1960-2020", population="a grid of economies")
    line = yaml.safe_load((STUDY / "cards" / "C38-cs-g-money-and-real-growth.yaml").read_text())["parameters"]["calm_line_mu_at_or_below"]
    reg.put("cs-g_line", line, unit="% a year", fmt="{:.0f}%", origin=o, as_of=GRID_AS_OF,
            measure="line marking calm windows (Teles and Uhlig's, adapted)",
            period="1960-2020", population="a grid of economies")


def k11_base(reg: Registry) -> None:
    r = run("C41-k11-inflation-by-money-pace-kazakhstan")
    o = computed("code/p2_k11_base.py (card C41, C39 corrected)")
    per, pop = "1950-2020", "a grid of economies"
    names = (("s1", "growth at or below 12"), ("s2", "growth above 12 to 20"), ("s3", "growth above 20 to 30"),
             ("s4", "growth above 30"))
    for (k, what), b in zip(names, r["bands"]):
        m, v = b["main"], b["variant"]
        reg.put(f"k11b_{k}_n", m["windows"], unit="windows", fmt="{:,.0f}", origin=o, as_of=GRID_AS_OF,
                measure=f"decades, base money {what} log pts a year", period=per, population=pop)
        reg.put(f"k11b_{k}_areas", m["areas"], unit="economies", fmt="{:,.0f}", origin=o, as_of=GRID_AS_OF,
                measure=f"economies, base money {what} log pts", period=per, population=pop)
        reg.put(f"k11b_{k}_hit", m["at_or_above"], unit="windows", fmt="{:,.0f}", origin=o, as_of=GRID_AS_OF,
                measure=f"of them ({what}), inflation averaging 20% a year or more", period=per, population=pop)
        reg.put(f"k11b_{k}_hit10", v["at_or_above"], unit="windows", fmt="{:,.0f}", origin=o, as_of=GRID_AS_OF,
                measure=f"of them ({what}), inflation averaging 10% a year or more", period=per, population=pop)
        for line, s in (("", m), ("10", v)):
            if "bound" in s:
                reg.put(f"k11b_{k}_bound{line}", s["bound"]["value"], unit="%", fmt="{:.1f}%", origin=o,
                        as_of=GRID_AS_OF, measure=f"{s['bound']['kind']}, one-sided 95% bound on that share",
                        period=per, population=pop)
            else:
                reg.put(f"k11b_{k}_share{line}", s["share"], unit="%", fmt="{:.1f}%", origin=o, as_of=GRID_AS_OF,
                        measure=f"share of those decades at {'10' if line else '20'}% or more", period=per,
                        population=pop, low=s["low"], high=s["high"])
                for end in ("low", "high"):
                    reg.put(f"k11b_{k}_share{line}_{end}", s[end], unit="%", fmt="{:.1f}%", origin=o,
                            as_of=GRID_AS_OF, measure=f"that share's 95% interval, {end} end", period=per,
                            population=pop)
    a = r["all"]
    reg.put("k11b_n", a["main"]["windows"], unit="windows", fmt="{:,.0f}", origin=o, as_of=GRID_AS_OF,
            measure="decades counted", period=per, population=pop)
    reg.put("k11b_areas", a["main"]["areas"], unit="economies", fmt="{:,.0f}", origin=o, as_of=GRID_AS_OF,
            measure="economies counted", period=per, population=pop)
    for line, s in (("", a["main"]), ("10", a["variant"])):
        reg.put(f"k11b_all_hit{line}", s["at_or_above"], unit="windows", fmt="{:,.0f}", origin=o, as_of=GRID_AS_OF,
                measure=f"decades with inflation averaging {'10' if line else '20'}% a year or more", period=per,
                population=pop)
    reg.put("k11b_filled", run("C25-a4-base-hko-fill")["C02_grid"]["n_added"], unit="windows", fmt="{:,.0f}",
            origin=computed("code/gap5_fill.py (card C25)"), as_of=GRID_AS_OF,
            measure="windows whose consumer prices were filled", period=per, population=pop)
    card = yaml.safe_load((STUDY / "cards" / "C41-k11-inflation-by-money-pace-kazakhstan.yaml").read_text())["parameters"]
    for k, v in card["lines"].items():
        reg.put("k11b_line" + ("" if k == "main" else "10"), 100 * v, unit="% a year", fmt="{:.0f}%", origin=o,
                as_of=GRID_AS_OF, measure=f"inflation line ({k}), averaged over the decade", period=per, population=pop)
    for cut in sorted({c for b in card["bands_mu"] for c in b if c is not None}):
        reg.put(f"k11b_cut_{cut}", cut, unit="log points a year", fmt="{:.0f}", origin=o, as_of=GRID_AS_OF,
                measure="band edge on base money growth", period=per, population=pop)
    reg.put("k11b_floor", card["merge_below_windows"], unit="windows", fmt="{:.0f}", origin=o, as_of=GRID_AS_OF,
            measure="fewest windows a band keeps before it merges", period=per, population=pop)
    for edge in (12, 20, 30):
        reg.put(f"k11b_edge_{edge}", 100 * (math.exp(edge / 100) - 1), unit="% a year", fmt="{:.0f}%", origin=o,
                as_of=GRID_AS_OF, measure=f"{edge} log points a year, as a yearly percentage", period=per,
                population=pop)


def cs_b(reg: Registry) -> None:
    r = run("C30-cs-b-base-against-broad")["calm"]
    o = computed("code/cs_b.py (card C30)")
    pop = "calm ten-year windows, a grid of economies"
    g = r["gap"]
    reg.put("cs_b_gap", g["gap"], unit="points of inflation per point of money growth", fmt="{:.2f}", origin=o,
            as_of=GRID_AS_OF, measure="broad money's slope less base money's", period="1960-2020", population=pop,
            low=g["lo"], high=g["hi"], matters=0.1, reading=r["reading"], claim_type="comparative")
    for k, s in (("base", r["slope_base"]), ("broad", r["slope_broad"])):
        reg.put(f"cs-b_slope_{k}", s["b"], unit="points of inflation per point", fmt="{:.2f}", origin=o, as_of=GRID_AS_OF,
                measure=f"slope of inflation on {k} money growth", period="1960-2020", population=pop)
    for k, field, unit in (("windows", "windows", "windows"), ("monies", "moneys", "economies")):
        reg.put(f"cs-b_{k}", r[field], unit=unit, fmt="{:.0f}", origin=o, as_of=GRID_AS_OF,
                measure=f"calm {unit} compared", period="1960-2020", population=pop)
    for k, v in (("gap-low", g["lo"]), ("gap-high", g["hi"])):
        reg.put(f"cs-b_{k}", v, unit="points per point", fmt="{:.2f}", origin=o, as_of=GRID_AS_OF,
                measure=f"the gap's interval, {'low' if k == 'gap-low' else 'high'} end", period="1960-2020", population=pop)
    reg.put("cs-b_reliability", run("C30-cs-b-base-against-broad")["attenuation"]["reliability_needed"], unit="share",
            fmt="{:.2f}", origin=o, as_of=GRID_AS_OF, measure="base growth's signal share that would close the gap",
            period="1960-2020", population=pop)


def cs_c(reg: Registry) -> None:
    r = run("C28-a4-units-guard")
    o = computed("code/units_guard.py (card C28)")
    pop = "ten-year windows, a grid of economies"
    for grid, prefix, label in (("C02_grid", "lr_base", "base money"), ("broad", "lr_broad", "broad money")):
        g = r[grid]["guarded"]["line_mu"]
        for side in ("above", "below"):
            reg.put(f"{prefix}_mu_{side}", g[f"beta_{side}"], unit="points of inflation per point", fmt="{:.2f}", origin=o,
                    as_of=GRID_AS_OF, measure=f"inflation per point of {label} growth, {side} the line",
                    period="1950-2020", population=pop, low=g[f"beta_{side}_lo"], high=g[f"beta_{side}_hi"], matters=0.1,
                    reading="effect" if g[f"beta_{side}_lo"] > 0.1 else "bounded", claim_type="comparative")
            for end in ("lo", "hi"):
                reg.put(f"cs-c_{prefix}_{side}_{end}", g[f"beta_{side}_{end}"], unit="points per point", fmt="{:.2f}",
                        origin=o, as_of=GRID_AS_OF,
                        measure=f"{label}, windows {side} the line: interval, {'low' if end == 'lo' else 'high'} end",
                        period="1950-2020", population=pop)
            reg.put(f"cs-c_{prefix}_{side}_windows", g[f"windows_{side}"], unit="windows", fmt="{:.0f}", origin=o,
                    as_of=GRID_AS_OF, measure=f"windows {side} the line, {label}", period="1950-2020", population=pop)
    for k, field in (("windows", "windows"), ("monies", "moneys")):
        noun = "economies" if k == "monies" else k
        reg.put(f"cs-c_{k}", r["C02_grid"]["guarded"][field], unit=noun, fmt="{:.0f}", origin=o, as_of=GRID_AS_OF,
                measure=f"{noun} on the base-money grid", period="1950-2020", population=pop)
    line = yaml.safe_load((STUDY / "cards" / "C28-a4-units-guard.yaml").read_text())["parameters"]["prior_line_teles_uhlig_pct"]
    reg.put("cs-c_line", line, unit="% a year", fmt="{:.0f}%", origin=o, as_of=GRID_AS_OF,
            measure="the line on money growth (Teles and Uhlig's, adapted)", period="1950-2020", population=pop)
    x = run("C29-a4-exploration-pace")
    o29 = computed("code/units_guard.py (card C29)")
    for key, block, what in (("lr_x_s7", x["S7_from_2000"], "windows starting from 2000 on"),
                             ("lr_x_s8", x["S8_outside_1970_2000"]["line"], "windows outside 1970-2000")):
        reg.put(key, block["beta_above"], unit="points of inflation per point", fmt="{:.2f}", origin=o29, as_of=GRID_AS_OF,
                measure=f"slope above the line, base money, {what}", period="1950-2020", population=pop,
                low=block["beta_above_lo"], high=block["beta_above_hi"], matters=0.1,
                reading="effect" if block["beta_above_lo"] > 0.1 else "bounded", claim_type="comparative")


def cs_d(reg: Registry) -> None:
    r = run("C31-cs-e-pandemic-cross-section")
    o = computed("code/cs_e.py (card C31)")
    pop = "economies calm in 2015-19"
    per = "money 2019-21, prices 2021-23"
    for key, block, what in (("cs_e_broad_huber", r["main"], "energy-import control"),
                             ("cs_e_var_momentum", r["variants"]["c_momentum"], "with 2021 inflation")):
        b = block["huber_boot"]
        reg.put(key, block["huber"], unit="points of inflation per point of money growth", fmt="{:.2f}", origin=o,
                as_of=CARD_DATA_AS_OF, measure=f"slope on broad money, {what}", period=per,
                population=pop, low=b["lo"], high=b["hi"], matters=0.1, reading=block["reading"], claim_type="association")
        for end in ("lo", "hi"):
            reg.put(f"cs-d_{key}_{end}", b[end], unit="points per point", fmt="{:.2f}", origin=o, as_of=CARD_DATA_AS_OF,
                    measure=f"slope, broad money, {what}: {'low' if end == 'lo' else 'high'} end", period=per, population=pop)
        reg.put(f"cs-d_{key}_n", block["n"], unit="economies", fmt="{:.0f}", origin=o, as_of=CARD_DATA_AS_OF,
                measure=f"economies, broad money slope, {what}", period=per, population=pop)
    nc = r["main_no_control"]  # printed beside, as the card fixes; its reading is the card's, said in the methods
    reg.put("cs-d_no-control", nc["huber"], unit="points per point", fmt="{:.2f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="slope on broad money growth, no control (beside)", period=per, population=pop)
    h = r["h_base_described"]  # variant (h): base money, described in the methods, never a claim (the card)
    reg.put("cs-d_h_base", h["huber"], unit="points per point", fmt="{:.2f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="slope on base money growth, variant h (described)", period=per, population=pop)
    for end in ("lo", "hi"):
        reg.put(f"cs-d_h_base_{end}", h["huber_boot"][end], unit="points per point", fmt="{:.2f}", origin=o,
                as_of=CARD_DATA_AS_OF, measure=f"slope on base money growth, variant h: {'low' if end == 'lo' else 'high'} end",
                period=per, population=pop)
    reg.put("cs-d_h_n", h["n"], unit="economies", fmt="{:.0f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="economies, variant h", period=per, population=pop)
    reg.put("cs-d_h_dcor", h["dcor_broad_minus_base"], unit="correlation", fmt="{:.2f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="correlation with inflation, broad money less base money, variant h", period=per, population=pop)
    reg.put("cs-d_h_sd", h["base_growth"]["sd"], unit="points a year", fmt="{:.1f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="standard deviation of base money growth, variant h", period=per, population=pop)
    reg.put("cs-d_h_top5", 100 * h["base_growth"]["share_of_variance_top5"], unit="percent", fmt="{:.0f}%", origin=o,
            as_of=CARD_DATA_AS_OF, measure="share of base money growth's variance from its five largest contributors",
            period=per, population=pop)
    reg.put("cs-d_no-control_n", nc["n"], unit="economies", fmt="{:.0f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="economies, no control (beside)", period=per, population=pop)
    for end in ("lo", "hi"):
        reg.put(f"cs-d_no-control_{end}", nc["huber_boot"][end], unit="points per point", fmt="{:.2f}", origin=o,
                as_of=CARD_DATA_AS_OF, measure=f"slope, no control: {'low' if end == 'lo' else 'high'} end", period=per,
                population=pop)
    loo = r["leave_one_out"]
    reg.put("cs-d_drops-flip", sum(1 for d in loo if d["moves"]), unit="economies", fmt="{:.0f}", origin=o,
            as_of=CARD_DATA_AS_OF, measure="single drops that turn the main reading to bounded", period=per, population=pop)
    reg.put("cs-d_drops", len(loo), unit="economies", fmt="{:.0f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="single drops tried (economies or monetary unions)", period=per, population=pop)
    reg.put("cs-d_drops-slope-min", min(d["huber"] for d in loo), unit="points per point", fmt="{:.2f}", origin=o,
            as_of=CARD_DATA_AS_OF, measure="lowest slope across the single drops", period=per, population=pop)
    reg.put("cs-d_drops-slope-max", max(d["huber"] for d in loo), unit="points per point", fmt="{:.2f}", origin=o,
            as_of=CARD_DATA_AS_OF, measure="highest slope across the single drops", period=per, population=pop)
    reg.put("cs-d_drops-lo-min", min(d["lo"] for d in loo), unit="points per point", fmt="{:.3f}", origin=o,
            as_of=CARD_DATA_AS_OF, measure="lowest low end across the single drops", period=per,
            population=pop)
    others = {k: v for k, v in r["variants"].items() if k != "c_momentum" and not k.startswith("h")}
    reg.put("cs-d_variants", len(others), unit="variants", fmt="{:.0f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="other variants fixed on the card (a, b, d, e, f, g)", period=per, population=pop)
    reg.put("cs-d_variants-below", sum(1 for v in others.values() if v["huber_boot"]["lo"] < 0.1), unit="variants",
            fmt="{:.0f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="other variants whose interval's lower end is below the size that matters", period=per,
            population=pop)
    reg.put("cs-d_fcr", r["null"]["false_confirmation_rate"], unit="share of null draws", fmt="{:.3f}", origin=o,
            as_of=CARD_DATA_AS_OF, measure="false-confirmation rate of the committed null simulation", period=per,
            population=pop)
    reg.put("cs-d_matters", 0.1, unit="points per point", fmt="{:.1f}", origin=o, as_of=CARD_DATA_AS_OF,
            measure="the size that matters fixed on the card", period=per, population=pop)


def today(reg: Registry) -> None:
    """Where the United States stood in the latest frozen data, for the watch list: twelve-month changes and levels,
    each read as published, no forecast and no threshold."""
    pop = "the United States"

    def put(key, value, fmt, unit, measure, period, series, vintage):
        reg.put(key, value, unit=unit, fmt=fmt, origin=computed(f"code/p2_registry.py ({_src(series)})"),
                as_of=vintage, measure=measure, period=period, population=pop)

    def month(ts) -> str:
        return pd.Timestamp(ts).strftime("%B %Y")

    m2 = agency.series("M2SL", "2026-09-30")
    put("now_m2", 100 * float(m2.iloc[-1] / m2.iloc[-13] - 1), "{:.1f}%", "% over twelve months", "growth of M2",
        f"{month(m2.index[-13])} to {month(m2.index[-1])}", "M2SL", "2026-09-30")
    loans = agency.series("TOTLL", "2026-10-10")
    loans.index = pd.to_datetime(loans.index)
    lm = loans.resample("ME").mean()
    put("now_loans", 100 * float(lm.iloc[-1] / lm.iloc[-13] - 1), "{:.1f}%", "% over twelve months",
        "growth of banks' loans and leases (monthly averages)", f"{month(lm.index[-13])} to {month(lm.index[-1])}", "TOTLL",
        "2026-10-10")
    gdp = agency.series("GDP", "2026-09-30")
    q = pd.Timestamp(gdp.index[-1])
    put("now_gdp", 100 * float(gdp.iloc[-1] / gdp.iloc[-5] - 1), "{:.1f}%", "% over four quarters",
        "growth of nominal GDP (spending in dollars)", f"to {q.year}Q{(q.month - 1) // 3 + 1}", "GDP", "2026-09-30")
    cpi = agency.series("CPIAUCSL", "2026-09-27")
    put("now_cpi", 100 * float(cpi.iloc[-1] / cpi.iloc[-13] - 1), "{:.1f}%", "% over twelve months",
        "consumer-price inflation (CPI-U)", f"{month(cpi.index[-13])} to {month(cpi.index[-1])}", "CPIAUCSL", "2026-09-27")
    ff = agency.series("FEDFUNDS", "2026-09-30")
    put("now_fedfunds", float(ff.iloc[-1]), "{:.2f}%", "% a year", "the effective federal funds rate",
        month(ff.index[-1]), "FEDFUNDS", "2026-09-30")
    deficit = agency.series("FYFSGDA188S", "2026-09-30")
    put("now_deficit", -float(deficit.iloc[-1]), "{:.1f}%", "% of GDP", "the federal deficit",
        f"fiscal year {pd.Timestamp(deficit.index[-1]).year}", "FYFSGDA188S", "2026-09-30")
    tr = agency.series("TREAST", "2026-09-30")
    tr.index = pd.to_datetime(tr.index)
    before = tr[tr.index <= tr.index[-1] - pd.Timedelta(days=364)]
    put("now_fed-treasuries", 100 * float(tr.iloc[-1] / before.iloc[-1] - 1), "{:.1f}%", "% over a year",
        "change in the Fed's holdings of Treasury securities", f"{before.index[-1]:%B %Y} to {tr.index[-1]:%B %Y}",
        "TREAST", "2026-09-30")


def _src(series: str) -> str:
    """Where a number's series comes from (the author, 2026-10-21): the original agency where it has one, FRED otherwise."""
    return f"the original agency's copy of FRED's {series}" if series.upper() in agency.ORIGINALS else f"frozen FRED {series}"


def examples(reg: Registry) -> None:
    """The series brief's example of a share going from $20 to $40: an example amount, not data, said so in its label."""
    o = computed("code/p2_registry.py (an example amount, not data: the series brief's)")
    for key, v, when in (("ex_share_before", 20, "before"), ("ex_share_after", 40, "after")):
        reg.put(key, v, unit="dollars", fmt="${:.0f}", origin=o, as_of="2026-10-11",
                measure=f"an example share price, {when} it doubles", period="any time", population="an example")


def fred_numbers(reg: Registry) -> None:
    """K4's and K6's numbers from the frozen series (their original agencies): windows dated by the Fed's own statements, nothing tuned."""
    base = agency.series("BOGMBASE", "2026-09-30")
    base.index = pd.to_datetime(base.index).strftime("%Y-%m")
    o = computed("code/p2_registry.py (the original agency's copy of FRED's BOGMBASE)")
    for key, a, z, why in (("k4_base_2008-2014", "2008-11", "2014-10", "Fed purchases"),
                           ("k4_base_2020-2022", "2020-02", "2022-03", "net purchases"),
                           ("k4_base_aug-nov-2008", "2008-08", "2008-11", "emergency lending"),
                           ("k4_base_sep-2019-2022", "2019-09", "2022-03", "from bill purchases")):
        reg.put(key, float(base[z] / base[a]), unit="times", fmt="{:.2f}", origin=o, as_of="2026-09-30",
                measure=f"US monetary base, end over start ({why})", period=f"{a} to {z}",
                population="the United States")
    m2 = agency.series("M2SL", "2026-09-30")
    m2.index = pd.to_datetime(m2.index).strftime("%Y-%m")
    om2 = computed("code/p2_registry.py (the original agency's copy of FRED's M2SL)")
    reg.put("k4_m2_2008-2014", float(m2["2014-10"] / m2["2008-11"]), unit="times", fmt="{:.2f}", origin=om2,
            as_of="2026-09-30", measure="US M2, end over start (the Fed's purchases)", period="2008-11 to 2014-10",
            population="the United States")
    reg.put("k4_m2_2020-2022", float(m2["2022-03"] / m2["2020-02"]), unit="times", fmt="{:.2f}", origin=om2,
            as_of="2026-09-30", measure="US M2, end over start (the pandemic purchases)", period="2020-02 to 2022-03",
            population="the United States")
    for key, a, z, months in (("k4_m2_rate_2008-2014", "2008-11", "2014-10", 71),
                              ("k4_m2_rate_2000-2007", "2000-12", "2007-12", 84)):
        reg.put(key, 100 * (float(m2[z] / m2[a]) ** (12 / months) - 1), unit="% a year", fmt="{:.1f}%", origin=om2,
                as_of="2026-09-30", measure="US M2, average growth a year", period=f"{a} to {z}",
                population="the United States")
    yoy = m2 / m2.shift(12) - 1
    first_fall = yoy[yoy < 0].index[0]
    if first_fall != "2022-12":
        raise SystemExit(f"K4: M2's first twelve-month fall is {first_fall}, not December 2022 as the claim says")
    reg.put("k4_m2_2022", 100 * float(m2["2022-12"] / m2["2021-12"] - 1), unit="%", fmt="{:.1f}%",
            origin=computed("code/p2_registry.py (the original agency's copy of FRED's M2SL)"), as_of="2026-09-30",
            measure="change in US M2, seasonally adjusted", period="December 2021 to December 2022",
            population="the United States")
    parts = {}
    for s in ("MDLM", "STDSL", "RMFSL"):
        x = agency.series(s, "2026-10-11")
        x.index = pd.to_datetime(x.index).strftime("%Y-%m")
        parts[s] = float(x["2022-12"] - x["2021-12"]) / 1000
    o3 = computed("code/p2_registry.py (the original agency's copy of FRED's MDLM, STDSL, RMFSL, from the Board's H.6)")
    reg.put("k4_m2_savings_2022", -parts["MDLM"], unit="trillions of dollars", fmt="${:.2f} trillion", origin=o3,
            as_of="2026-10-11", measure="fall in US savings and other liquid deposits counted in M2 (MDLM)",
            period="December 2021 to December 2022", population="the United States")
    reg.put("k4_m2_time-funds_2022", parts["STDSL"] + parts["RMFSL"], unit="trillions of dollars", fmt="${:.2f} trillion",
            origin=o3, as_of="2026-10-11", measure="rise in US small time deposits and retail money-market funds",
            period="December 2021 to December 2022", population="the United States")
    cd = 0.0
    for s in ("CURRSL", "DEMDEPSL"):
        x = agency.series(s, "2026-09-30")
        x.index = pd.to_datetime(x.index).strftime("%Y-%m")
        cd += float(x["2022-12"] - x["2021-12"]) / 1000
    reg.put("k4_m2_cash-demand_2022", cd, unit="trillions of dollars", fmt="${:.2f} trillion",
            origin=computed("code/p2_registry.py (the original agency's copy of FRED's CURRSL, DEMDEPSL)"), as_of="2026-09-30",
            measure="rise in US currency and demand deposits counted in M2", period="December 2021 to December 2022",
            population="the United States")
    loans = agency.series("TOTLL", "2026-10-10")
    loans.index = pd.to_datetime(loans.index)
    monthly = loans.resample("ME").mean()
    monthly.index = monthly.index.strftime("%Y-%m")
    reg.put("k4_loans_2022", 100 * float(monthly["2022-12"] / monthly["2021-12"] - 1), unit="%", fmt="{:.0f}%",
            origin=computed("code/p2_registry.py (the original agency's copy of FRED's TOTLL, weekly levels averaged by month)"),
            as_of="2026-10-10", measure="change in US banks' loans and leases", period="December 2021 to December 2022",
            population="US commercial banks")
    credit = agency.series("TOTBKCR", "2026-10-12")
    credit.index = pd.to_datetime(credit.index)
    cm = credit.resample("ME").mean()
    cm.index = cm.index.strftime("%Y-%m")
    reg.put("k4_credit_2022", 100 * float(cm["2022-12"] / cm["2021-12"] - 1), unit="%", fmt="{:.0f}%",
            origin=computed("code/p2_registry.py (the original agency's copy of FRED's TOTBKCR, weekly levels averaged by month)"),
            as_of="2026-10-12", measure="change in US banks' total credit, loans and securities", period="December 2021 to December 2022",
            population="US commercial banks")
    oph = agency.series("OPHNFB", "2026-10-10")
    first, last = oph.index[0], oph.index[-1]
    reg.put("k6_output-per-hour_multiple", float(oph.iloc[-1] / oph.iloc[0]), unit="times", fmt="{:.1f}",
            origin=computed("code/p2_registry.py (the original agency's copy of FRED's OPHNFB)"), as_of="2026-10-10",
            measure="US nonfarm business output per hour, latest over first",
            period=f"{pd.Timestamp(first):%Y}Q1 to {pd.Timestamp(last).year}Q{(pd.Timestamp(last).month - 1) // 3 + 1}",
            population="the United States")


# --- the claims -------------------------------------------------------------------------------------------------

def put_sourced(reg: Registry) -> None:
    for e in yaml.safe_load((HERE / "p2_cited.yaml").read_text()):
        reg.put(e["key"], e["value"], unit=e["unit"], fmt=e["fmt"], as_of=str(e["as_of"]),
                origin=cited(e["source"], str(e["locator"]), e.get("url")),
                measure=e["measure"], period=str(e["period"]), population=e["population"])
    for c in yaml.safe_load((HERE / "p2_claims.yaml").read_text()):
        reg.put_claim(c["id"], text=c["text"], type=c["type"], keys=keys_of(c["text"]) or None,
                      sources=c["sources"], component=c["component"])


def put_measured_and_judgement(reg: Registry) -> None:
    def m(cid, text, card, component, measure, period, population, **kw):
        reg.put_claim(cid, text=text, type="measured", card=card, component=component, keys=keys_of(text) or None,
                      scope={"measure": measure, "period": period, "population": population}, **kw)

    def j(cid, text, component, **kw):
        reg.put_claim(cid, text=text, type="judgement", component=component, keys=keys_of(text) or None, **kw)

    m("cs-a", "In the latest month, notes and coin held by the public were {{cs-a_us_latest}} of M2 in the United States "
      "and {{cs-a_ea_latest}} of M3 in the euro area, and notes and coin in circulation {{cs-a_gb_latest}} of M4 in "
      "Britain; since each series began the share "
      "has ranged from {{cs-a_us_low}} to {{cs-a_us_high}} in the US, {{cs-a_ea_low}} to {{cs-a_ea_high}} in the euro area "
      "and {{cs-a_gb_low}} to {{cs-a_gb_high}} in Britain.", "C35", "K1",
      "notes and coin held by the public (in Britain, in circulation), share of broad money", "1959-2026",
      "the US, the euro area and Britain")
    m("cs-a-wider", "Across the {{cs-a_all_n}} economies in the IMF's statistics with both lines, at each one's latest month, "
      "currency outside banks was a median {{cs-a_all_median}} of money and quasi-money, and half or more in "
      "{{cs-a_all_half}}: Guinea-Bissau, {{cs-a_wider_gw}}, and Iraq, {{cs-a_wider_iq}}.", "C35", "K1",
      "currency outside banks, share of money and quasi-money", "each economy's latest month", "IMF IFS economies")
    m("cs-e", "From 1952 to 2025 US households' net worth rose {{cs-e_1952-2025_real-change}} in December 2025 dollars: "
      "real holding gains on real assets and market-priced claims added {{cs-e_1952-2025_real_and_market_priced}}, net "
      "investment {{cs-e_1952-2025_net_investment}} and inflation's gain on what households owe "
      "{{cs-e_1952-2025_gain_on_liabilities}}, while fund and pension claims lost {{cs-e_1952-2025_fund_and_pension}} in "
      "real terms, debt securities, currency and deposits {{cs-e_1952-2025_nominal_claims}}, and other nominal assets "
      "{{cs-e_1952-2025_erosion_of_other_nominal_assets}} to inflation; other volume changes added "
      "{{cs-e_1952-2025_other_volume}}; inflation's gain on what households owe was "
      "{{cs-e_1952-2025_liabilities_over_fixed}} of the real loss on debt securities, currency, deposits and "
      "other assets fixed in dollars.", "C36", "K7", "the real change in net worth and its parts (Z.1, S1M.r)",
      "1952-2025", "US households and nonprofits")
    m("cs-e-euro", "In 2022 euro-area households' equity lost {{cs-e_f51_euro_area_2022}} of its value in real terms, "
      "US households' {{cs-e_f51_us_2022}}.", "C36", "K7", "real holding gains on equity, share of the start-of-year level",
      "2022", "euro-area and US households")
    m("cs-f", "From 1959 to 2025 US M2 grew {{cs-f_1959-2025_money}} a year on average, real GDP {{cs-f_1959-2025_real_output}} "
      "and the GDP price index {{cs-f_1959-2025_prices}}; velocity, GDP over M2, changed {{cs-f_1959-2025_velocity}} a year, "
      "the identity's residual.", "C37", "K6", "average yearly growth of M2, real GDP, prices and velocity",
      "1959Q4-2025Q4", "the United States")
    m("cs-g", "Drawn in the manner of Lucas's figure, our {{cs-g_windows}} ten-year windows from {{cs-g_monies}} economies set "
      "real growth against broad money growth; {{cs-g_calm}} are calm, money growing {{cs-g_line}} a year or less.", "C38",
      "K6", "ten-year windows drawn", "1960-2020", "a grid of economies")
    m("cs-b", "In calm decades each point of central-bank money growth went with {{cs-b_slope_base}} of a point of "
      "inflation, each point of the public's money with {{cs-b_slope_broad}}: a gap of {{cs_b_gap}} "
      "({{cs-b_gap-low}} to {{cs-b_gap-high}}), across {{cs-b_windows}} calm windows in {{cs-b_monies}} economies.", "C30", "K8",
      "slopes of inflation on base and on broad money growth, calm windows", "1960-2020", "a grid of economies",
      reading="effect", claim_type="comparative")
    m("cs-c", "Where base money grew faster than {{cs-c_line}} a year, inflation went with it about point for point, "
      "{{lr_base_mu_above}} ({{cs-c_lr_base_above_lo}} to {{cs-c_lr_base_above_hi}}); where it grew slower, by "
      "{{lr_base_mu_below}} of a point ({{cs-c_lr_base_below_lo}} to {{cs-c_lr_base_below_hi}}); in the fast windows "
      "starting from 2000 on, by {{lr_x_s7}}, and outside 1970-2000 by {{lr_x_s8}}.", "C28", "K8",
      "slope of inflation on base money growth, on each side of the line", "1950-2020", "a grid of economies",
      reading="effect", claim_type="comparative")
    m("cs-d", "Across {{cs-d_cs_e_broad_huber_n}} economies that started calm, each point of faster broad money growth in "
      "2020-21 went with {{cs_e_broad_huber}} of a point more inflation in 2022-23 ({{cs-d_cs_e_broad_huber_lo}} to "
      "{{cs-d_cs_e_broad_huber_hi}}); with 2021's inflation as a control the slope falls to {{cs_e_var_momentum}}, and if it "
      "is there it is under {{cs-d_cs_e_var_momentum_hi}}; dropping any one of {{cs-d_drops-flip}} of {{cs-d_drops}} "
      "economies or unions moves the interval's lower end just below the size that matters, and in every drop the slope "
      "stays between {{cs-d_drops-slope-min}} and {{cs-d_drops-slope-max}} and the lower end above zero "
      "({{cs-d_drops-lo-min}} at the lowest); and in {{cs-d_variants-below}} of the "
      "{{cs-d_variants}} other variants the lower end falls below the size that matters.", "C31", "K8",
      "robust slope of 2022-23 inflation on 2020-21 broad money growth", "2019-2023", "economies calm in 2015-19",
      reading="effect", claim_type="association")
    j("k1-cbdc", "A digital currency issued by a central bank would be central-bank money in another form, a promise of "
      "the top of the ladder held directly by the public.", "K1")
    j("k2-edge", "We read the sources' mechanism this way: loans make deposits wherever banks lend against a central bank "
      "that supplies reserves at its rate; it stops holding where a bank keeps all its deposits in coin, where the central "
      "bank buys from the public, and where the state, not a bank, has the money created.", "K2")
    j("k2-state-spending", "The state's spending, paid from its account at the central bank, adds reserves and the "
      "recipients' deposits; taxes, and the bonds the Treasury normally sells to fund itself, move money back into that "
      "account, which absorbs reserves; so over a year, in our reading, spending adds money only where taxes and bonds "
      "sold to the public do not take it back, where the deficit is paid for by the central bank or by banks.", "K2")
    j("k3-twice", "So your money is not handed to the borrower: the bank wrote the borrower a new deposit. Both are money, two "
      "separate promises the bank owes, and yours does not exist twice.", "K3")
    j("k5-lean", "We read the evidence this way: no record shows money growing out of barter, which turns up where money fails; in "
      "the earliest records money is a unit for reckoning debts, long before coin. That money began as credit is one school's "
      "reading, Innes's and Graeber's, not a settled history.", "K5")
    j("k6-oecd", "In our reading, the weak positive relation among the rich economies is what growing economies that borrow "
      "more, and so hold more deposits, would show by the mechanism above, a reading we do not test; it is not evidence that more money makes more output.", "K6")
    j("k6-condition", "Whether more money brings more output depends, in our reading, on what can be produced: credit that "
      "finances new production raises output once the new goods come, with prices rising meanwhile at full use; where "
      "resources lie idle, output can rise first; and over decades, across countries, faster money growth did not go "
      "with faster real growth, or only weakly, though one recent study finds money made scarce can cost output for a decade or more.", "K6")
    j("k7-share", "We read the balance sheets this way: a share that goes from {{ex_share_before}} to {{ex_share_after}} creates no money; its holder's "
      "wealth rises and no deposit or note changes; at a sale between buyers and sellers that are not banks, existing money "
      "changes hands, and if the buyer borrowed, the "
      "loan made the money, not the price; a crash destroys wealth, not money.", "K7")
    j("k7b-shops", "So a boom in valuations reaches the shops only through spending, and whether that spending raises shop "
      "prices depends, in our reading, on what can be produced and on how the central bank answers.", "K7b")
    j("k8-dispute", "How much the money itself added to 2021-23 is disputed; in our reading of these sources, the inflation "
      "in the United States largely reflected strong demand, but most of it came through price shocks from commodities and shortages, and tight labour markets kept it going for longer, and across economies the money went together "
      "with the fiscal spending that carried it, so neither can be credited alone.", "K8")
    j("k8-causes", "Inflation is a broad, lasting fall in what money buys; in our reading of the cases, money growing far "
      "faster than output, demand beyond capacity, supply shocks and states paying their way with money each dominated "
      "somewhere, and none explains every episode; they overlap and are not of the same rank: a state paying with new money "
      "is a deeper cause, working through fast money growth and through demand, but money has grown fast for other reasons (American silver in Spain), and Barro and Bianchi read "
      "the inflation after 2020 through the value of states' debts, with no part for money.", "K8")
    j("cs-e-gross", "In our reading, the rows of the household-wealth split that set holdings against inflation are losses "
      "before interest, since interest earned reaches net worth through saving and investment; they are not net losses to savers.", "K10")
    j("k9-reading", "A hyperinflation is a lot of money and little value at once: the notes multiply, people hold as little "
      "of them as they can, and what all the notes together buy shrinks.", "K9")
    j("k10-who-pays", "In our reading, the transfers that come with creating money move value rather than make it: the state gains through its "
      "central bank, holders of notes, chiefly, pay the inflation tax, borrowers at fixed rates gain from lenders, "
      "banks gain on their deposits, and holders of financial assets gain when purchases raise asset prices.", "K10")
    j("k10-inflation-tax-notes", "Reserves now earn interest close to the policy rate, so we read the inflation tax's net weight as "
      "falling chiefly on whoever holds notes.", "K10")
    j("law-reading", "Law's France shows, in our reading, how the three fared: the real economy grew, in Murphy's account, but "
      "could not keep pace with the notes and shares; prices in Paris rose far less than the money, but the notes lost their value against silver; holding up a share price with new notes "
      "did not protect the money; and carrying the state's debt on shares and notes ended with the notes no longer money "
      "and the debt turned back into bonds.", "K6")
    j("k4-japan-reading", "In our reading, base money growing while prices were falling cannot by itself show what base "
      "money does to prices.", "K4")
    j("k1-floor-bridge", "In our reading, the floor of the first part holds for the unit, the state's money; a deposit, "
      "the bank's promise to pay that money on demand, one for one, keeps its claim to the unit while its bank is sound or "
      "the deposit is insured, and beyond that on what the authorities decide: in Cyprus even insured deposits were held "
      "behind capital controls, and Silicon Valley Bank's uninsured depositors were saved by a decision taken for that bank.", "K1")
    j("k11-watch", "In our reading, what to watch instead of the money printer is: bank credit and the public's money "
      "against spending; how the state's deficits are financed; whether a central bank buys from banks or from the "
      "public; its interest rate against inflation; whether output can still rise; and, for a market's rise, earnings "
      "against the price paid for them and interest rates.", "K11")
    j("k11-levels", "In our reading, the study's episodes say that base money growth over a few years told little on its "
      "own (base money nearly tripled from 2008 to 2014 without shop prices following), while over decades each point of "
      "base money growth went with about one point of inflation where it grew faster than about twelve per cent a year, "
      "and about a quarter below; that after the pandemic faster broad money growth went with more inflation, perhaps none once "
      "2021's inflation is allowed for; that the route of deficit financing, not a size, marks the episodes told (part "
      "1's hyperinflations; Argentina, where the deficit and the central bank's lending ended together); and that the "
      "study holds no level for spare capacity, for prices against earnings or for whom a central bank buys from. These "
      "are readings of past episodes, not a forecast.", "K11")
    m("k11-base-rate", "Of the {{k11b_s1_n}} ten-year windows in which base money grew at or below {{k11b_edge_12}} a year "
      "(twelve log points; every edge here is a yearly percentage), {{k11b_s1_hit}} had inflation averaging 20% a year or more; above it, up to {{k11b_edge_20}} a year, {{k11b_s2_hit}} "
      "of {{k11b_s2_n}}; up to {{k11b_edge_30}}, {{k11b_s3_hit}} of {{k11b_s3_n}}; faster, {{k11b_s4_hit}} of "
      "{{k11b_s4_n}}; money and prices over the same decade, a count of the past, not a forecast or a threshold.",
      "C41", "K11", "decades with inflation averaging 20% a year or more, by base money growth", "1950-2020",
      "a grid of economies")
    j("k4-m2-reading", "In our reading, much of the money that left M2 in 2022 went into Treasury securities; the Fed's "
      "shrinking holdings worked the same way, and the study does not size each flow.", "K4")
    reg.put_claim("now-us", text="Over the twelve months to August 2026 US M2 grew {{now_m2}}, banks' loans and leases "
                  "{{now_loans}} to September 2026 and nominal GDP {{now_gdp}} over four quarters; the federal deficit was "
                  "{{now_deficit}} of GDP in fiscal 2025; the Fed's Treasury holdings changed by {{now_fed-treasuries}} over "
                  "a year, as from December 2025 it bought Treasury bills to keep banks' reserves ample and put the principal "
                  "repaid on its agency securities into bills; its policy rate was {{now_fedfunds}} against consumer-price inflation of {{now_cpi}}.",
                  type="established", component="K11", keys=keys_of("{{now_m2}} {{now_loans}} {{now_gdp}} {{now_deficit}} "
                  "{{now_fed-treasuries}} {{now_fedfunds}} {{now_cpi}}"),
                  sources=[{"source": "the Federal Reserve Board (H.6 M2, H.8 loans and leases, H.4.1 Treasury securities, H.15 the "
                            "federal funds rate), the BEA (nominal GDP) and the BLS (CPI-U), each over the dates of FRED's copy "
                            "frozen 2026-09-27 to 2026-10-10; the deficit as a share of GDP from FRED (FYFSGDA188S)",
                            "locator": "the latest observations and those a year before",
                            "passage": "series values as published; changes computed in code/p2_registry.py",
                            "copy": "data", "read": "full", "url": "https://www.federalreserve.gov/releases/h6/"},
                           {"source": "FOMC, statement of 10 December 2025 and its implementation note", "locator":
                            "statement, the reserves paragraph; implementation note, the directive's purchases and reinvestment",
                            "passage": "The Committee judges that reserve balances have declined to ample levels and will "
                            "initiate purchases of shorter-term Treasury securities as needed to maintain an ample supply of "
                            "reserves on an ongoing basis. ... Reinvest all principal payments from the Federal Reserve's "
                            "holdings of agency securities into Treasury bills.", "copy": "open", "read": "passage",
                            "url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20251210a.htm"}])
    j("headline", "Most money is a bank's promise, created when someone borrows and destroyed when they repay; notes and coin "
      "are a minority of it, {{cs-a_us_latest}} of the money people hold in the United States, {{cs-a_ea_latest}} in the "
      "euro area and {{cs-a_gb_latest}} in Britain. Value is made by producing what people want, and prices are the rate "
      "between the two. Over the long run and across countries, faster money growth has gone with faster inflation, "
      "not, or only weakly, with faster real growth; a share that doubles creates no money, though a bank loan taken against it does; and inflation has several origins: money growing "
      "far faster than output, demand beyond capacity, supply shocks, a state paying its way with money, and, at the "
      "extreme, people fleeing a money.",
      "K1", headline=True)


# --- the correction of 2026-10-21 (Kazakhstan's IFS index; the methods' research log) ----------------------------------

BEFORE = STUDY / "results" / "correction-2026-10-21-before.json"   # written by code/p2_correction_before.py


def correction(reg: Registry) -> None:
    """The numbers of the correction note: the splice's ratio from the frozen files (``ft.data.splices``), Kazakhstan's
    2010-2020 window before and after from C28's runs, and the printed numbers that moved, as printed before (read
    from ``BEFORE``, which ``code/p2_correction_before.py`` extracted from the project's history: never typed)."""
    from ft.data import splices
    reg.put("corr_kaz_ratio", splices.ratio(splices.SPLICES[0]), unit="ratio", fmt="{:.4f}",
            origin=computed("toolkit/ft/data/splices.py: IFS A.KZ.PCPI_IX 2020 over the World Bank's FP.CPI.TOTL KAZ 2020"),
            as_of=GRID_AS_OF, measure="IFS's annual price index for Kazakhstan over the World Bank's, 2020", period="2020",
            population="Kazakhstan")
    before = json.loads(BEFORE.read_text())
    src = f"results/{BEFORE.name} (C28's run and results/numbers.json at {before['commit']})"
    kz_now = next(q for q in run("C28-a4-units-guard")["C02_grid"]["points"] if q["area"] == "KZ" and q["y0"] == 2010)
    for tag, pi, origin in (("before", before["C28_KZ_2010_2020_pi"], f"{src}, C02_grid.points, KZ 2010-2020"),
                            ("after", kz_now["pi"], "C28's run as rerun, C02_grid.points, KZ 2010-2020")):
        reg.put(f"corr_kz_window_pi_{tag}", pi, unit="log points a year", fmt="{:.1f}", origin=computed(origin),
                as_of=GRID_AS_OF, measure=f"Kazakhstan's average inflation over its 2010-2020 window, {tag} the correction",
                period="2010-2020", population="Kazakhstan")
        reg.put(f"corr_kz_window_pct_{tag}", 100 * (math.exp(pi / 100) - 1), unit="% a year", fmt="{:.1f}%",
                origin=computed(f"{origin}: 100 * (exp(pi / 100) - 1), the log-point rate as a compound yearly percentage"),
                as_of=GRID_AS_OF, measure=f"Kazakhstan's average inflation over its 2010-2020 window as a yearly "
                f"percentage, {tag} the correction", period="2010-2020", population="Kazakhstan")
    for key, value in before["numbers"].items():
        entry = reg.get(key)
        reg.put(f"corr_{key}_before", value, unit=entry["unit"], fmt=entry.get("fmt"),
                origin=computed(f"{src}, {key}: the value printed before the correction"),
                as_of=entry.get("as_of"), measure=f"{entry.get('measure') or key}, as printed before the correction",
                period=entry.get("period"), population=entry.get("population"))


def main() -> Registry:
    reg = Registry(STUDY / "results" / "numbers.json", {})
    cs_a(reg)
    cs_e(reg)
    cs_f(reg)
    cs_g(reg)
    k11_base(reg)
    cs_b(reg)
    cs_c(reg)
    cs_d(reg)
    fred_numbers(reg)
    examples(reg)
    today(reg)
    put_sourced(reg)
    put_measured_and_judgement(reg)
    correction(reg)
    reg.save()
    return reg


if __name__ == "__main__":
    main()
