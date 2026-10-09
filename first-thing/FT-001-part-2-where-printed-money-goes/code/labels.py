"""What each number a reader sees measures, over what period, for what population (W4; BLUEPRINT P08, §5 d).
Read by ``readings.py``, which writes the three fields into the registry. Written with the regenerated forms
(2026-10-06): the keys they print, by family, each family's words checked against the card that computed it.
"""

from __future__ import annotations

ALL = "every economy with the data"
DEC = "decades, 1950–2020"
DEC19 = "ten-year windows ending in 2019 (1949–2019)"
TESTED = "the large printings tested (since 1950), accommodation dated up to the crossing"
US = "United States"
EA = "euro area"
SLOPE = "inflation per point of base money growth"
BROAD = "inflation per point of broad money growth"
#: Before 1950 the money is JST's narrow money, as each country defines it (base money, notes and coin, or M1): map
#: v15's P2-3 guard (round 2).
SLOPE_JST = "inflation per point of narrow money growth"
#: The site lists each number under a label of under 110 characters (STUDIES-WEB 14.3): the cross-section of
#: 2020-23 (C31) is worded once here, and registry_v15 reads the same words.
P_E = "money 2020–21, inflation 2022–23"
P_E_LED = "money 2020, inflation 2022–23"
P_EC = "2020–23"
CALM = "economies averaging under 10% inflation, 2015-19"
CALM_E = "calm economies with energy data"
#: The decades of C30 (calm: both money growths at or below 12% a year).
P_B = "windows ending 1970–2020"
POP_B = "decades with both money growths at most 12% a year"
BSLOPE = "broad less base slope"

LABELS: dict[str, tuple[str, str, str]] = {
    # the door: two American printings (C01)
    **{f"door_w1_{k}": (m, "August 2008 to October 2014", US) for k, m in (
        ("start", "first month of the window"), ("end", "last month of the window"), ("months", "length of the window"),
        ("added", "base money added"), ("share_pa", "base money added a year, share of the first year's GDP"),
        ("prices_pa", "consumer prices (CPI-U), change a year"), ("prices_total", "consumer prices (CPI-U), change over the window"))},
    **{f"door_w2_{k}": (m, "February 2020 to December 2021", US) for k, m in (
        ("start", "first month of the window"), ("end", "last month of the window"), ("months", "length of the window"),
        ("added", "base money added"), ("share_pa", "base money added a year, share of the first year's GDP"),
        ("share_total", "base money added, share of the first year's GDP"),
        ("prices_pa", "consumer prices (CPI-U), change a year"), ("prices_total", "consumer prices (CPI-U), change over the window"))},
    "door_w1_22_months": ("length of the comparison", "the first 22 months of each window", US),
    "door_w1_22_share_total": ("base money added, share of the first year's GDP", "August 2008 to June 2010", US),
    "door_w1_22_prices_total": ("consumer prices (CPI-U), change", "August 2008 to June 2010", US),
    "door_ratio_share_pa": ("base money added a year as a share of GDP, second window over first",
                            "2020–21 against 2008–14", US),
    "door_ratio_prices_pa": ("consumer price change a year, second window over first", "2020–21 against 2008–14", US),
    # the long run (C25, C27, C22's grid, C21, C23)
    "lr_line": ("money-growth line splitting the decades", DEC, ALL),
    "lr_dgp_line": ("De Grauwe and Polan's inflation line, as their abstract states it", DEC, ALL),
    "lr_ci": ("confidence level of the intervals", DEC, ALL),
    "lr_base_n": ("decade windows with data", DEC, ALL),
    "lr_base_moneys": ("economies with data", DEC, ALL),
    "lr_base_beta": (SLOPE, DEC, ALL), "lr_base_lo": (SLOPE + ", low end", DEC, ALL),
    "lr_base_hi": (SLOPE + ", high end", DEC, ALL),
    "lr_base_mu_below": (SLOPE, DEC, "base money growing under 12% a year"),
    "lr_base_mu_below_lo": (SLOPE + ", low end", DEC, "base money growing under 12% a year"),
    "lr_base_mu_below_hi": (SLOPE + ", high end", DEC, "base money growing under 12% a year"),
    "lr_base_mu_below_n": ("decade windows", DEC, "base money growing under 12% a year"),
    "lr_base_mu_above": (SLOPE, DEC, "base money growing over 12% a year"),
    "lr_base_mu_above_lo": (SLOPE + ", low end", DEC, "base money growing over 12% a year"),
    "lr_base_mu_above_hi": (SLOPE + ", high end", DEC, "base money growing over 12% a year"),
    "lr_base_mu_above_n": ("decade windows", DEC, "base money growing over 12% a year"),
    "lr_mu_below_x10": ("extra inflation a year going with ten points more base money growth a year (ten times the "
                        "slope)", DEC, "base money growing under 12% a year"),
    "lr_base_pi_below": (SLOPE, DEC, "decades with inflation below 12% a year"),
    "lr_base_pi_above": (SLOPE, DEC, "decades with inflation above 12% a year"),
    "lr_base_ho_beta": (SLOPE + ", fitted on decades to 1990, judged on decades from 1990", "ten-year windows from 1990", ALL),
    "lr_base_ho_lo": (SLOPE + ", held out, interval's low end", "ten-year windows from 1990", ALL),
    "lr_base_ho_hi": (SLOPE + ", held out, interval's high end", "ten-year windows from 1990", ALL),
    "lr_base_gamma": ("points of inflation per point of real output growth, money growth held fixed", DEC, ALL),
    "lr_base_gamma_lo": ("the same, interval's low end", DEC, ALL),
    "lr_base_gamma_hi": ("the same, interval's high end", DEC, ALL),
    "lr_broad_mu_below": (BROAD, DEC,
                          "broad money growing under 12% a year"),
    "lr_broad_mu_above": (BROAD, DEC,
                          "broad money growing over 12% a year"),
    "lr_broad_mu_below_lo": (BROAD + ", low end", DEC,
                             "broad money growing under 12% a year"),
    "lr_broad_mu_below_hi": (BROAD + ", high end", DEC,
                             "broad money growing under 12% a year"),
    "lr_broad_mu_below_n": ("decade windows", DEC, "broad money growing under 12% a year"),
    "lr_dgp_head_mu_below": (SLOPE, DEC + " (prices not yet filled)", "decades with base money growing less than 10% a year"),
    "lr_dgp_head_mu_above": (SLOPE, DEC + " (prices not yet filled)", "decades with base money growing more than 10% a year"),
    "lr_1870_economies": ("economies in the Macrohistory Database", "1870–1950", "economies that became rich"),
    "lr_1870_beta": (SLOPE_JST, "ten-year windows, 1870–1950", "18 rich economies (Macrohistory Database)"),
    "lr_1870_nowar_beta": (SLOPE_JST, "ten-year windows, 1870–1950, without those holding a world-war year",
                           "18 rich economies (Macrohistory Database)"),
    "lr_1870_mu_below": (SLOPE_JST, "decades, 1870–1950", "18 rich economies, growth under 12% a year"),
    "lr_1870_mu_above": (SLOPE_JST, "decades, 1870–1950", "18 rich economies, growth over 12% a year"),
    "lr_fill_c02_added": ("decade windows added by filling missing prices from the World Bank's inflation database", DEC, ALL),
    **{f"lr_pt_{c}_2010_{v}": (("base money growth" if v == "mu" else "consumer price inflation") + ", average a year",
                               "end of 2010 to end of 2020", name)
       for c, name in (("u2", EA), ("gb", "United Kingdom"), ("jp", "Japan"), ("us", US)) for v in ("mu", "pi")},
    **{f"lr_c22_pt_{c}_{v}": (("base money growth" if v == "mu" else "consumer price inflation") + ", average a year",
                              "end of 2009 to end of 2019", name)
       for c, name in (("u2", EA), ("jp", "Japan"), ("cz", "Czechia")) for v in ("mu", "pi")},
    # the printings (C15's list read on the filled prices, C26)
    "e_episodes": ("large printings found by the rule", "starts 1950–2026", "every currency with monthly data"),
    "e_moneys": ("currencies with at least one large printing", "1950–2026", "every currency with monthly data"),
    "e_set_apart": ("printings set apart (one-month jumps, changes of definition, yearly data, gaps)", "1950–2026",
                    "the large printings found"),
    "e_tested_design": ("printings tested", "starts 1950–2023", "the large printings found"),
    "e_tested_design_era3": ("printings tested starting in 2000 or later", "starts 2000–2023", "the large printings found"),
    "e_top_money_share": ("largest share of the list held by one currency", "1950–2026", "the large printings found"),
    "e_X": ("base money added, share of a year's GDP, beyond the economy's own growth (the rule's size)", "within the "
            "rule's window", "every currency"),
    "e_Y": ("the rule's window", "any", "every currency"),
    "e_T": ("inflation above which a printing counts as answering inflation", "from the start to the crossing", "every printing"),
    "e_H": ("months after the start over which outcomes are read", "after each start", "every printing"),
    "a5_design_o1pp_med": ("consumer price inflation a year over the 36 months after the start, median", "after each start", TESTED),
    "a5_design_o1_med": ("change in inflation, 36 months after against the year before, median", "after each start", TESTED),
    "a5_design_o1_up": ("share of printings followed by higher inflation", "after each start", TESTED),
    "a5_design_o1_p25": ("change in inflation, lower quartile", "after each start", TESTED),
    "a5_design_o1_p75": ("change in inflation, upper quartile", "after each start", TESTED),
    "a5_design_o2g_med": ("broad money growth a year over the 36 months after the start, median", "after each start", TESTED),
    "a5_floor_after_2000": ("printings at the interest-rate floor, all starting after 2000", "starts 2000–2023", TESTED),
    "a5_perms": ("random reshuffles within eras for each test", "1950–2026", TESTED),
    "a5_counted": ("variant runs fixed before the run", "1950–2026", TESTED),
    "a5_m0_o1_d4_diff": ("gap in the median change in inflation, claims on the government rose most minus the rest",
                         "after each start", "the printings tested, accommodation dated at the start"),
    **{f"a5_design_o1_{d}_{s}": (m + {"diff": ", gap between the two groups", "med1": ", median where it held",
                                      "med0": ", median where it did not", "n1": " — printings where it held",
                                      "n0": " — printings where it did not"}[s],
                                 "after each start", TESTED)
       for d, m in (("d1", "change in inflation by exchange rate (floating against pegged)"),
                    ("d2", "change in inflation by interest rate (above its floor against at it)"),
                    ("d4", "change in inflation by what the central bank's claims grew most on (government against the rest)"),
                    ("d5", "change in inflation by government deficit at the start (5% of GDP or more against less)"))
       for s in ("diff", "med1", "med0", "n1", "n0")},
    # the euro area and the US, described (C18)
    **{f"a5_{a}_{y}_{k}": (m, {"m0": "start month"}.get(k, "around the printing that began then"), n)
       for a, n, ys in (("u2", EA, ("2011", "2014", "2020")), ("us", US, ("2008", "2012", "2019"))) for y in ys
       for k, m in (("m0", "first month of the printing"), ("before", "consumer price inflation, the year before the start"),
                    ("after", "consumer price inflation a year, the 36 months after the start"),
                    ("o2g", "broad money growth a year, the 36 months after the start"))},
    "a5_u2_2011_dfr": ("the ECB's deposit facility rate, average of the start month", "July 2011", EA),
    "a5_us_2008_mich": ("expected inflation over the next year, University of Michigan survey", "September 2008", US),
    "a5_us_2019_mich": ("expected inflation over the next year, University of Michigan survey", "November 2019", US),
    # history (cited)
    "hist_ming_face": ("market value of Ming paper money against its face value", "by 1425", "Ming China"),
    "hist_continental": ("Continental dollars to one dollar of coin, as Congress counted them", "18 March 1780",
                         "the United States under the Continental Congress"),
    "hist_hungary_hours": ("time for prices to double, in hours", "1945–46", "Hungary"),
    # velocity (C19)
    "vel_at_cut": ("M2 velocity (GDP over M2)", "second quarter of 2008", US),
    "vel_low": ("M2 velocity (GDP over M2), lowest", "since 2008", US),
    "vel_low_quarter": ("quarter of the lowest M2 velocity", "since 2008", US),
    "vel_last": ("M2 velocity (GDP over M2)", "latest quarter", US),
    "vel_last_quarter": ("latest quarter with M2 velocity", "2026", US),
    "vel_r2_loglog": ("share of velocity's variation the interest rate explains, best of three forms",
                      "1959 to mid-2008", US),
    "vel_r2_floor": ("least share a form had to explain to judge, fixed before the run", "1959 to mid-2008", US),
    # where the base sits, and the Federal Reserve's income
    "sits_week": ("week of the reading", "September 2026", US),
    "sits_reserves": ("reserve balances", "week to 23 September 2026", US),
    "sits_reserves_share": ("reserve balances, share of base money", "week to 23 September 2026", US),
    "sits_currency": ("currency in circulation", "week to 23 September 2026", US),
    "ior_expense_2021": ("Reserve Banks' interest expense on reserve balances", "2021", "Federal Reserve Banks"),
    "ior_rise_2022": ("rise in the interest expense on reserve balances", "2022 against 2021", "Federal Reserve Banks"),
    "ior_rise_2023": ("rise in the interest expense on reserve balances", "2023 against 2022", "Federal Reserve Banks"),
    "remit_2021": ("transfers to the US Treasury", "2021", "Federal Reserve Banks"),
    "loss_2023": ("expenses beyond earnings", "2023", "Federal Reserve Banks"),
    "deferred_2023": ("deferred asset (earnings owed to the Treasury not yet paid), year-end", "end of 2023",
                      "Federal Reserve Banks"),
    "deferred_lowest": ("deferred asset, peak", "weekly, 2022–2026", "Federal Reserve Banks"),
    "deferred_lowest_date": ("week of the deferred asset's peak", "weekly, 2022–2026", "Federal Reserve Banks"),
    "deferred_latest": ("deferred asset, latest", "week to 23 September 2026", "Federal Reserve Banks"),
    "deferred_latest_date": ("week of the latest reading", "September 2026", "Federal Reserve Banks"),
    # the inflation tax (C13)
    "tax_last_month": ("last month of the measurement", "February 2020 to August 2026", US),
    "tax_hh_lower_current": ("purchasing power lost on households' cash and checking deposits, per household, net of "
                             "checking interest (current dollars)", "February 2020 to August 2026", "US households"),
    "tax_hh_upper_current": ("purchasing power lost on households' cash and checking deposits, per household, as if "
                             "paying nothing (current dollars)", "February 2020 to August 2026", "US households"),
    "tax_households": ("number of households", "February 2020 to August 2026", "US households"),
    "tax_whole_total": ("purchasing power lost on currency and deposits paying no interest", "February 2020 to August 2026",
                        "all holders of US currency and non-interest-bearing deposits"),
    "tax_share_2021": ("purchasing power lost on currency and deposits paying no interest, share of the year's GDP",
                       "2021", "all holders of US currency and non-interest-bearing deposits"),
    "seign_currency_2021": ("rise in currency in circulation", "2021", US),
    "cash_cpi_rise": ("consumer prices (CPI-U), change", "February 2020 to August 2026", US),
    "cash_share_lost": ("purchasing power lost by a balance left unchanged", "February 2020 to August 2026", US),
}

# C29 (exploration, after the grid checks of 2026-10-07) and the held-out reading from 1999 (C28 on C22's grid)
_X = "every economy's decade windows, with the units guard applied"
_BAND = {"lr_x_s2": "12 to 20", "lr_x_s3": "20 to 30", "lr_x_s4": "30 to 50", "lr_x_s5": "above 50"}
for _k, _b in _BAND.items():
    LABELS[_k] = (SLOPE, DEC, f"base money growing {_b}% a year")
LABELS.update({
    "lr_x_edge20": ("edge between money-growth bands", DEC, ALL),
    "lr_x_edge30": ("edge between money-growth bands", DEC, ALL),
    "lr_x_edge50": ("edge between money-growth bands", DEC, ALL),
    "lr_x_s6_above": (SLOPE, DEC, "base money growing 12 to 30% a year"),
    "lr_x_s1_gamma": ("points of inflation per point of real output growth, money growth held fixed, decades at or below the line", DEC, _X),
    "lr_x_s1_gamma_lo": ("points of inflation per point of real output growth, money growth held fixed, decades at or below the line, interval low end", DEC, _X),
    "lr_x_s1_gamma_hi": ("points of inflation per point of real output growth, money growth held fixed, decades at or below the line, interval high end", DEC, _X),
    "lr_x_s7_above": (SLOPE + " above the line, decades from 2000", "ten-year windows from 2000", _X),
    "lr_x_s8": (SLOPE + ", all decades wholly outside 1970–2000", "windows ending by 1970 or starting from 2000", _X),
    "lr_x_s10_below": (SLOPE + " below the line, without currency-union members and economies using another's money",
                       DEC, _X),
    "lr_x_s10_above": (SLOPE + " above the line, without currency-union members and economies using another's money",
                       DEC, _X),
    "lr_x_s12_below": (SLOPE + " below the line, without the decades of shrinking base money", DEC, _X),
    "lr_x_s12_dropped": ("decades in which base money shrank", DEC, _X),
    "lr_x_s13_below": (SLOPE + " below the line, real growth from the World Bank", DEC, _X),
    "lr_x_s13_above": (SLOPE + " above the line, real growth from the World Bank", DEC, _X),
    "lr_x_s15_theta_share": ("share of simulated records with one slope everywhere giving a gap this wide",
                             "one thousand draws", _X),
    "lr_x_s15_draws": ("simulated records drawn", "the null simulation", _X),
    "lr_c22_ho_beta": (SLOPE + ", fitted on decades to 1999, judged on decades from 1999", "ten-year windows from 1999", ALL),
    "lr_c22_ho_lo": (SLOPE + ", held out from 1999, interval's low end", "ten-year windows from 1999", ALL),
    "lr_c22_ho_hi": (SLOPE + ", held out from 1999, interval's high end", "ten-year windows from 1999", ALL),
    "lr_1870_gamma": ("points of inflation per point of real output growth, money growth held fixed", "1870–1950",
                      "economies that became rich (Jordà, Schularick and Taylor)"),
    "lr_1870_gamma_lo": ("points of inflation per point of real output growth, money growth held fixed, interval low end", "1870–1950",
                      "economies that became rich (Jordà, Schularick and Taylor)"),
    "lr_1870_gamma_hi": ("points of inflation per point of real output growth, money growth held fixed, interval high end", "1870–1950",
                      "economies that became rich (Jordà, Schularick and Taylor)"),
})

# map v15's printed keys that carried no labels (round 2, step w, 2026-10-08)
LABELS.update({
    "lr_x_s1": (SLOPE, DEC, "base money growing at most 12% a year"),
    "csb_moneys": ("economies with a decade both moneys grew 12% or less", P_B, ALL),
    "cse_n": ("economies with energy-import data", P_EC, CALM),
    "csc_w1_months": ("length of the first printing's window", "August 2008 to October 2014", US),
    "csc_w2_months": ("length of the second printing's window", "February 2020 to December 2021", US),
    "csc_unrate_line": ("the unemployment line the text reads against", "2008-2014", US),
    "csc_unrate_above8_from": ("first month unemployment stood above the line", "2008-2014", US),
    "csc_unrate_above8_to": ("last month unemployment stood above the line", "2008-2014", US),
})
_CSB = (P_B, POP_B)
_CSE = (P_E, CALM_E)
LABELS.update({
    "csb_gap_lo": (BSLOPE + ", low end", *_CSB),
    "csb_gap_hi": (BSLOPE + ", high end", *_CSB),
    "cse_lo": ("broad slope, low end", *_CSE),
    "cse_hi": ("broad slope, high end", *_CSE),
    "cse_nocontrol_lo": ("broad slope, low end", P_E, CALM),
    "cse_nocontrol_hi": ("broad slope, high end", P_E, CALM),
    "cse_loo_moves": ("economies whose removal alone puts the low end under 0.1", P_EC, CALM_E),
    "cse_loo_lo_min": ("low end of the range, lowest with one economy left out", P_EC, CALM_E),
    "cse_nocontrol_n": ("economies in the run without the energy control", P_EC, CALM),
    "cse_control_missing": ("economies without energy-import data", P_EC, CALM),
    "cs_e_var_momentum": ("broad slope, 2021 inflation fixed", *_CSE),
    "cse_var_momentum_lo": ("slope, 2021 inflation fixed, low end", *_CSE),
    "cse_var_momentum_hi": ("slope, 2021 inflation fixed, high end", *_CSE),
    "cs_e_var_led": ("broad money slope", P_E_LED, CALM_E),
    "cse_var_led_lo": ("broad slope, low end", P_E_LED, CALM_E),
    "cse_var_led_hi": ("broad slope, high end", P_E_LED, CALM_E),
})

# K3 beyond one country (the grid check of 2026-10-08, J)
LABELS.update({
    "boj_base_2012": ("Japan's monetary base at the end of the year", "end of 2012", "Japan"),
    "boj_base_2014": ("Japan's monetary base expected at the end of the year", "end of 2014", "Japan"),
    "snb_assets_gdp": ("the Swiss National Bank's total assets, share of GDP", "December 2014", "Switzerland"),
    "uk_cpi_2011_09": ("consumer-price inflation over twelve months (CPI)", "September 2011", "the United Kingdom"),
})

# CS-B by era and the UK's QE (the confirming check of 2026-10-08)
LABELS.update({
    "csb_to2000_gap_lo": (BSLOPE + ", low end", "windows ending 1970–2000", POP_B),
    "csb_to2000_gap_hi": (BSLOPE + ", high end", "windows ending 1970–2000", POP_B),
    "csb_from2008_gap_lo": (BSLOPE + ", low end", "windows ending 2008–2020", POP_B),
    "csb_from2008_gap_hi": (BSLOPE + ", high end", "windows ending 2008–2020", POP_B),
    "boe_apf_2011": ("the Bank of England's asset purchase programme, total voted", "October 2011", "the United Kingdom"),
    "boe_apf_held_2011": ("the Bank of England's stock of asset purchases financed by reserves", "September 2011",
                          "the United Kingdom"),
})

# The door's scope and the shutdowns (Sami's remarks through the engine, 2026-10-09)
LABELS.update({
    "csc_w1_base_growth": ("growth of central-bank money over the first printing",
                           "August 2008 to October 2014", "the United States"),
    "csc_w2_base_growth": ("growth of central-bank money over the second printing",
                           "February 2020 to December 2021", "the United States"),
    "csc_pre2008_max_growth_74m": ("largest growth of central-bank money in any 74 months",
                                   "windows ending 1965 to August 2008", "the United States"),
    "csc_pre2008_max_growth_22m": ("largest growth of central-bank money in any 22 months",
                                   "windows ending 1960 to August 2008", "the United States"),
    "csc_base_first_month": ("first year of the Fed's monthly series of central-bank money (BOGMBASE)", "1959",
                             "the United States"),
    "fed_bs_ww2_gdp": ("the Fed's balance sheet, share of GDP, peak",
                       "end of each year, 1930s–1940s", "the United States"),
    "fed_bs_2014_gdp": ("the Fed's balance sheet, share of GDP, its peak after 2008", "end of 2014",
                        "the United States"),
})
