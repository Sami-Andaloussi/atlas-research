"""The numbers map v11's components print from others' work and from frozen data (round 2, 2026-10-08): the door, K1-K8
and K5's table (``registry.py`` calls :func:`add`, after ``registry_v11.add``).

Two kinds, each with its labels:
- **cited**: a value printed in a source, at the passage recorded in ``notes/sources.md`` (and the notes it names);
  where our sentence derives a value from cited ones (a median, a count, a share), the derivation is computed here from
  the cited values, never typed;
- **computed from frozen data**: FRED CPIAUCNS (2026-09-30), WDI FP.CPI.TOTL.ZG (2026-09-30), JST R6 (2026-09-30) and
  the IMF WEO's end-of-period consumer prices for Argentina (the October 2013 vintage through DBnomics, frozen
  2026-10-08).
"""

from __future__ import annotations

import io
import statistics
from pathlib import Path

import numpy as np
import pandas as pd

from ft.data import dbnomics, fred, freeze, reconstructed, worldbank

S = "code/sources_v11.py"
PCT0, PCT1, F1, F2 = "{:.0f}%", "{:.1f}%", "{:.1f}", "{:.2f}"

BJ = "Bernanke & James (1991), NBER chapter c11482"
ES = "Eichengreen & Sachs (1985), NBER Working Paper 1498"
SV = "Sargent & Velde (1995), Journal of Political Economy 103(3)"
WHITE = "White (1995), Journal of Economic History 55(2)"
VW = "Velde & Weir (1992), Journal of Economic History 52(1)"
SILBER = "Silber (2007), When Washington Shut Down Wall Street"
CAL = "Calomiris (1988), Oxford Economic Papers 40(4)"
RW = "Rolnick & Weber (1997), Journal of Political Economy 105(6); FRB Minneapolis Quarterly Review 22(2) reprint"
BS = "Bordo & Schwartz (1994), NBER Working Paper 4860"
FSV = "Fischer, Sahay & Vegh (2002), NBER Working Paper 8930"
FOMC12 = "Federal Reserve, FOMC Statement on Longer-Run Goals and Monetary Policy Strategy, 25 January 2012"
FOOTE = "Foote, Block, Crane & Gray (2004), Journal of Economic Perspectives 18(3)"
LW = "Luther & White (2011), 'Positively Valued Fiat Money after the Sovereign Disappears: The Case of Somalia'"
FRB23 = "Federal Reserve Bulletin, December 1923"
FRB24 = "Federal Reserve Bulletin, August 1924"
SARGENT = "Sargent (1982), 'The Ends of Four Big Inflations', NBER chapter c11452"
LMS = "Liu, Makarov & Schoar (2023), NBER Working Paper 31160"
FSR = "Board of Governors of the Federal Reserve System, Financial Stability Report, May 2023"
JUDSON = "Judson (2012), Federal Reserve IFDP 1058"
WILLARD = "Willard, Guinnane & Rosen (1995), NBER Working Paper 5381"

# Bordo & Schwartz, Table 3 (printed p. 62): inflation in GNP deflators, log-trend growth rates, by regime (gold
# standard 1881-1913, Bretton Woods 1946-70, the float 1974-90); None where the table prints "na". Read from the
# transcription data/reconstructed/ft001-bs3 (moved out of this file on 2026-10-09: a table of a printed work ships as
# its manifest only); row j (the G10 and Switzerland, together) is iso3 G10J.
def _bs3() -> tuple[dict, dict]:
    t = reconstructed.load("ft001-bs3")
    rows, row_j = {}, {}
    for r in t.itertuples():
        if r.iso3 == "G10J":
            row_j[r.regime] = float(r.value)
            continue
        cells = rows.setdefault(r.iso3, {"name": r.name})
        cells[r.regime] = float(r.value)
    return ({iso: (c["name"], c.get("gold"), c.get("bw"), c.get("float")) for iso, c in rows.items()}, row_j)


BS3, BS3_J = _bs3()
G10 = ("USA", "GBR", "DEU", "FRA", "CAN", "ITA", "NLD", "BEL", "SWE", "CHE", "JPN")  # Table 3's row j


def door_and_k3(R) -> None:
    R.cite("bj_gap_1932", 12, "percentage points of wholesale-price deflation", BJ,
           "p. 42 ('the twelve percentage point difference in rates of deflation between gold and non-gold countries "
           "in 1932')")
    R.cite("bj_economies", 24, "economies", BJ, "Table 2.1 and fn 6, p. 64")
    for y, gold, off in ((1932, -13, -1), (1933, -7, 0), (1934, -4, 3), (1935, -5, 4)):
        R.cite(f"bj_gold_{y}", gold, "percent a year (wholesale prices, log change x 100)", BJ,
               f"Table 2.2, p. 43, grand average, gold countries, {y}", fmt=PCT0)
        R.cite(f"bj_off_{y}", off, "percent a year (wholesale prices, log change x 100)", BJ,
               f"Table 2.2, p. 43, grand average, non-gold countries, {y}", fmt=PCT0)
    R.cite("bj_min_cover", 40, "percent (statutory minimum gold cover, usually)", BJ, "p. 38", fmt=PCT0)
    raw = freeze.load("jst/macrohistory", "2026-09-30").read_bytes("JSTdatasetR6.dta")
    jst = pd.read_stata(io.BytesIO(raw))[["iso", "year", "cpi"]].set_index(["iso", "year"]).cpi
    uk = 100 * (jst[("GBR", 1932)] / jst[("GBR", 1931)] - 1)
    R.reg.put("uk_cpi_1932", float(uk), unit="percent", origin={"kind": "computed", "script": S}, as_of=R.AS_OF,
              fmt=PCT1, measure="change in consumer prices over the year", period="1932",
              population="the United Kingdom (JST R6)")
    R.reg.put("uk_cpi_1932_fall", -float(uk), unit="percent", origin={"kind": "computed", "script": S},
              as_of=R.AS_OF, fmt=PCT1, measure="fall in consumer prices over the year", period="1932",
              population="the United Kingdom (JST R6)")
    R.cite("mandat_open", 35, "percent of face value in coin", SV, "p. 510 (March 1796)", fmt=PCT0)
    R.cite("mandat_summer", 6, "percent of face value in coin", SV, "p. 510 (early summer 1796)", fmt=PCT0)
    R.cite("mandat_cap", 2400, "livres at face", SV, "p. 510; White (1995) p. 247",
           fmt="{:,.0f} million")
    R.cite("mandat_assignat_rate", 30, "assignats to one mandat", SV, "p. 510 ('to retire the assignats at 30:1')")
    R.cite("mandat_lease_multiple", 22, "times the 1790 lease", WHITE, "p. 247; Sargent & Velde p. 515 (22 times income)")
    R.cite("mandat_deposit", 25, "percent of the price, as a first payment", SV, "p. 515", fmt=PCT0)
    R.cite("assignat_1793", 50, "percent of face value in gold, about", VW, "p. 17, fn 49 (June 1793)", fmt=PCT0)
    # Bordo & Schwartz Table 3, the 1970-73 exits (P1-11) and K4's magnitude
    for iso, (name, gold, bw, flt) in BS3.items():
        for regime, v in (("gold", gold), ("bw", bw), ("float", flt)):
            if v is not None:
                R.reg.put(f"bs3_{iso.lower()}_{regime}", v, unit="percent a year (GNP deflator, log-trend rate)",
                          origin={"kind": "cited", "source": BS, "locator": f"Table 3, p. 62, row {name}"},
                          as_of=R.AS_OF, fmt=PCT1, measure="inflation in the GNP deflator, log-trend growth rate",
                          period={"gold": "1881-1913", "bw": "1946-70", "float": "1974-90"}[regime], population=name)
    for key, v, regime in (("bs3_g10_gold", BS3_J["gold"], "gold standard, 1881-1913"),
                           ("bs3_g10_bw", BS3_J["bw"], "Bretton Woods, 1946-70"),
                           ("bs3_g10_float", BS3_J["float"], "the float, 1974-90")):
        R.reg.put(key, v, unit="percent a year (GNP deflator, log-trend rate)",
                  origin={"kind": "cited", "source": BS, "locator": "Table 3, p. 62, row j (G10 and Switzerland)"},
                  as_of=R.AS_OF, fmt=PCT1, measure="inflation in the GNP deflator",
                  period=regime, population="the G10 economies and Switzerland, together")
    others = [i for i in G10 if i != "USA"]
    us = BS3["USA"][3]
    below = [BS3[i][0] for i in others if BS3[i][3] < us]
    above = [BS3[i][0] for i in others if BS3[i][3] > us]
    flt = [BS3[i][3] for i in others]
    bw = [BS3[i][2] for i in others]
    diffs = {i: BS3[i][3] - BS3[i][1] for i in G10 if BS3[i][1] is not None}
    pop_x = "the G10 economies and Switzerland, the United States aside"
    for key, v, unit, period, measure in (
            ("bs3_exits_n", len(others), "economies", "1974-90", "economies compared with the US"),
            ("bs3_exits_below_us", len(below), "economies", "1974-90", "economies with inflation below the US's"),
            ("bs3_exits_above_us", len(above), "economies", "1974-90", "economies with inflation above the US's"),
            ("bs3_exits_float_min", min(flt), "percent a year", "1974-90", "lowest inflation in the GNP deflator"),
            ("bs3_exits_float_max", max(flt), "percent a year", "1974-90", "highest inflation in the GNP deflator"),
            ("bs3_exits_bw_min", min(bw), "percent a year", "1946-70", "lowest inflation in the GNP deflator"),
            ("bs3_exits_bw_max", max(bw), "percent a year", "1946-70", "highest inflation in the GNP deflator"),
            ("bs3_exits_bw_below_us", sum(v < BS3["USA"][2] for v in bw), "economies", "1946-70",
             "economies with inflation below the US's")):
        R.reg.put(key, v, unit=unit, origin={"kind": "computed", "script": S}, as_of=R.AS_OF,
                  fmt=PCT1 if "percent" in unit else None, period=period, measure=measure, population=pop_x)
    nonus = [i for i in BS3 if i != "USA"]
    R.put("bs3_all_nonus", len(nonus), "economies", S)
    R.put("bs3_all_above_us", sum(BS3[i][3] > us for i in nonus), "economies", S)
    lab_d = dict(period="1974-90 against 1881-1913", population="G10 and Switzerland, both rates")
    for key, v, what in (("bs3_gap_median", statistics.median(diffs.values()), "median"),
                         ("bs3_gap_min", min(diffs.values()), "lowest"),
                         ("bs3_gap_max", max(diffs.values()), "highest"), ("bs3_gap_n", len(diffs), "")):
        R.reg.put(key, v, unit="points a year" if key != "bs3_gap_n" else "economies",
                  origin={"kind": "computed", "script": S}, as_of=R.AS_OF, fmt=F1 if key != "bs3_gap_n" else None,
                  measure=f"{what} inflation gap, float less gold standard" if what else "economies with both rates",
                  **lab_d)
    R.put("bs3_g10_gap", BS3_G10_FLOAT - BS3_G10_GOLD, "points a year", S, fmt=F1)
    R.cite("bs3_arg_float", BS3["ARG"][3], "percent a year (GNP deflator, log-trend rate)", BS, "Table 3, p. 62, row "
           "Argentina")  # kept under its own key for the Latin American contrast
    R.cite("bs3_bra_float", BS3["BRA"][3], "percent a year (GNP deflator, log-trend rate)", BS, "Table 3, p. 62, row "
           "Brazil")
    us_cpi = fred.read("CPIAUCNS", "2026-09-30")
    for key, day in (("us_cpi_1914_06", "1914-06-01"), ("us_cpi_1920_06", "1920-06-01"),
                     ("us_cpi_1965_01", "1965-01-01"), ("us_cpi_1971_01", "1971-01-01")):
        R.reg.put(key, float(us_cpi.loc[day]), unit="index, 1982-84 = 100", origin={"kind": "computed", "script": S},
                  as_of=R.AS_OF, fmt=F1, measure="consumer price index, all urban consumers, not seasonally adjusted", period=day[:7], population="the United States")
    loss = 1 - us_cpi.loc["1914-06-01"] / us_cpi.loc["1920-06-01"]
    R.reg.put("us_pp_loss_1914_20", 100 * float(loss), unit="percent of purchasing power",
              origin={"kind": "computed", "script": S}, as_of=R.AS_OF, fmt=PCT0,
              measure="the dollar's loss of purchasing power over consumer goods",
              period="June 1914 to June 1920", population="the United States")


BS3_G10_GOLD, BS3_G10_FLOAT = BS3_J["gold"], BS3_J["float"]


def k1_k4_k6(R) -> None:
    R.cite("silber_gold_1864", 285, "greenback dollars per 100 gold dollars (the year's highest)", SILBER,
           "p. 27 ('from $285 in 1864 to $107 in 1878')")
    R.put("gb_low_silber", 100 * 100 / 285, "cents in gold per greenback dollar", S, fmt="{:.0f}")
    R.cite("calomiris_max", 2.5, "greenback dollars per gold dollar (the monthly series' highest)", CAL,
           "p. 719 ('ranged from par to 2.5')")
    R.put("gb_low_calomiris", 100 / 2.5, "cents in gold per greenback dollar", S, fmt="{:.0f}")
    R.cite("cal_greenbacks_1863", 58.1, "cents in gold per dollar", CAL, "Table 6, pp. 739-741 (28 February 1863)",
           fmt=F1)
    R.cite("cal_demand_notes_1863", 99.4, "cents in gold per dollar", CAL, "Table 6, pp. 739-741 (28 February 1863)",
           fmt=F1)
    R.cite("willard_1864_shift", 4.8, "percent (the largest one-day move of the war)", WILLARD, "p. 17", fmt=PCT1)
    R.cite("rw_countries", 15, "countries", RW, "p. 13")
    R.cite("rw_both", 12, "countries with both a commodity and a fiat period", RW, "p. 13")
    R.cite("rw_fiat_mean", 9.17, "percent a year (all fiat observations)", RW, "p. 16", fmt="{:.2f}%")
    R.cite("rw_commodity_mean", 1.75, "percent a year (all commodity observations)", RW, "p. 16", fmt="{:.2f}%")
    R.cite("fsv_line", 100, "percent over twelve months (very high inflation)", FSV, "p. 5", fmt=PCT0)
    R.cite("fsv_line25", 25, "percent a year (high inflation, their lower line)", FSV, "p. 7", fmt=PCT0)
    R.cite("fsv_economies", 133, "market economies, 1960-96", FSV, "p. 7")
    for key, v, line in (("fsv_above25", 92, 25), ("fsv_above50", 49, 50), ("fsv_above100", 25, 100)):
        R.cite(key, v, f"economies with inflation above {line}% at some point", FSV, "p. 7")
        R.put(f"{key}_share", 100 * v / 133, "percent of the 133 economies", S, fmt=PCT0)
    R.cite("fomc_target", 2, "percent a year (PCE prices)", FOMC12, "the statement", fmt=PCT0)
    R.cite("judson_abroad_100s", 65, "percent of $100 notes held abroad, end-2011", JUDSON, "p. 12", fmt=PCT0)


def k5_k8(R) -> None:
    R.cite("sd_fixed_years", 13, "years with an essentially fixed stock", FOOTE, "p. 61")
    R.cite("sd_rate", 100, "Saddam dinars to one Swiss dinar, about", FOOTE, "p. 61 (July 1998 to January 2002)")
    R.cite("sd_conversion", 150, "new dinars to one Swiss dinar (the 2003-04 conversion)", FOOTE, "p. 61")
    R.cite("som_notes_bn", 481, "billion unofficial shilling notes printed since 1991, estimated", LW,
           "section 2.2 (citing Symes 2006a, p. 29); library copy, no page")
    for key, v, loc in (("rm_mortgage_bn", 3.2, "p. 1281"), ("rm_gov_cap_bn", 1.2, "p. 1281")):
        R.cite(key, v, "billion gold marks", FRB23, loc, fmt=F1)
    R.cite("rm_current_exp_bn", 1.0, "billion marks (of the loan to the government, to current expenses)", FRB24,
           "p. 636", fmt=F1)
    R.cite("rm_note_limit_bn", 2.4, "billion marks (the present note limit)", FRB24, "p. 636", fmt=F1)
    R.cite("rm_redeem_sum", 500, "marks (the smallest sum redeemable)", FRB23, "p. 1281")
    R.cite("rm_debentures", 196000, "marks of debentures issued on redemption, June 1924", FRB24, "p. 636",
           fmt="{:,.0f}")
    R.cite("rm_notes_bn", 2.05, "billion marks of notes, June 1924", FRB24, "p. 636", fmt=F2)
    R.cite("rm_sargent_cap_bn", 3.2, "billion marks (the issue limit)", SARGENT, "p. 83", fmt=F1)
    R.cite("terra_days", 3, "days", LMS, "abstract ('in three days in May 2022')")
    R.cite("usdc_low", 87, "cents per dollar", FSR, "p. 55")
    wdi = worldbank.read("FP.CPI.TOTL.ZG", "2026-09-30")
    wdi = wdi.dropna(subset=["value"])
    lab = dict(measure="consumer-price inflation, annual average (WDI FP.CPI.TOTL.ZG)")

    def wb(iso: str, year: int) -> float:
        row = wdi[(wdi.iso3 == iso) & (wdi.year == year)]
        assert len(row) == 1, (iso, year)
        return float(row.value.iloc[0])

    hk = wdi[(wdi.iso3 == "HKG") & (wdi.year >= 1983)]
    R.reg.put("hk_cpi_min", float(hk.value.min()), unit="percent a year", origin={"kind": "computed", "script": S},
              as_of=R.AS_OF, fmt=PCT1, period=f"1983-{int(hk.year.max())}", population="Hong Kong", **lab)
    R.reg.put("hk_cpi_max", float(hk.value.max()), unit="percent a year", origin={"kind": "computed", "script": S},
              as_of=R.AS_OF, fmt=PCT1, period=f"1983-{int(hk.year.max())}", population="Hong Kong", **lab)
    for iso, name, years in (("EST", "Estonia", (1993, 1994, 1998)), ("BGR", "Bulgaria", (1996, 1997, 1998, 1999))):
        for y in years:
            R.reg.put(f"{iso.lower()}_cpi_{y}", wb(iso, y), unit="percent a year",
                      origin={"kind": "computed", "script": S}, as_of=R.AS_OF, fmt="{:,.1f}%", period=str(y),
                      population=name, **lab)
    weo = dbnomics.parse(freeze.load("dbnomics/IMF/WEO_2013-10/ARG~PCPIEPCH+PCPIE", "2026-10-08"))
    arg = weo[(weo.series_code == "ARG.PCPIEPCH.pcent_change") & (weo.period == "2002")]
    R.reg.put("arg_cpi_2002", float(arg.value.iloc[0]), unit="percent", origin={"kind": "computed", "script": S},
              as_of="2026-10-08", fmt=PCT0, measure="consumer prices, December to December (IMF WEO, October 2013, "
              "end-of-period)", period="2002", population="Argentina")


def add(R) -> None:
    door_and_k3(R)
    k1_k4_k6(R)
    k5_k8(R)
