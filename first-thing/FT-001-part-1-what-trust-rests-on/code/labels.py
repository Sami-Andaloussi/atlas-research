"""The labels of every number the reader's forms print (W4, OT03): key -> (measure, period, population). Written with
the forms in the regeneration (2026-10-07); ``readings.py`` writes them into the registry. One family per block."""

from __future__ import annotations

LABELS: dict[str, tuple[str, str, str]] = {}


def _family(keys: dict[str, str], period: str, population: str) -> None:
    for key, measure in keys.items():
        LABELS[key] = (measure, period, population)


# the door, 1797-1821
_family({"door_par_value": "the gold a note bought against par, mean of Tooke's dates (above par +)",
         "door_par_dates": "Tooke's dates with a price of gold, August 1797 to August 1799",
         "door_par_low": "the gold a note bought against par, lowest of Tooke's dates",
         "door_par_high": "the gold a note bought against par, highest of Tooke's dates"},
        "August 1797 to August 1799", "Bank of England notes, in London")
_family({"door_agio_peak": "premium of gold over paper at its peak, as Antipa's text gives it",
         "door_agio_1800": "premium of gold over paper when it first reached this level"},
        "1797 to 1821", "Bank of England notes, in London")
_family({"a3_mint_price": "the mint's price of standard gold, an ounce",
         "a3_flat_price": "the price of gold Tooke prints in every year but one of the near-par years",
         "a3_restriction_p_low": "lowest yearly average value in gold",
         "a3_restriction_premium_low": "the premium of gold over the notes in their lowest year",
         "a3_restriction_wait_low": "the shortest wait for gold the premium implies",
         "a3_restriction_wait_high": "the longest wait for gold the premium implies"},
        "1797-1821 (waits: 1810-16)", "Bank of England notes, in London")
_family({"a3_greenback_p_low": "the greenbacks' lowest monthly value in gold",
         "a3_greenback_wait_low": "the shortest wait for gold the premium implies",
         "a3_greenback_wait_high": "the longest wait for gold the premium implies",
         "a3_greenback_after_law_cannot": "months in which the premium cannot tell an expected return from the "
                                          "paper's own value",
         "a3_greenback_after_law_months": "months between the 1875 Act and the return to gold"},
        "1862-78 (waits: 1863-69)", "United States notes (greenbacks)")
_family({"a3_1914_gbr": "yearly odds of a return to gold implied by the premium, mean",
         "a3_1914_fra": "yearly odds of a return to gold implied by the premium, mean",
         "a3_1914_ita": "yearly odds of a return to gold implied by the premium, mean",
         "a3_1914_deu": "yearly odds of a return to gold implied by the premium, mean"},
        "1915 to 1920", "the pound, the French franc, the Italian lira and the German mark")

# the Bank of England's balance sheet beside the door (Millennium, sheet A23; both grid checks of 2026-10-07)
for y in range(1796, 1802):
    _family({f"door_boe_bullion_{y}": "the Bank of England's coin and bullion, its yearly account",
             f"door_boe_notes_{y}": "the Bank of England's notes in circulation, its yearly account",
             f"door_boe_cover_{y}": "the Bank's coin and bullion as a share of its notes in circulation"},
            str(y), "the Bank of England")
for y in range(1797, 1801):
    _family({f"door_cpi_infl_{y}": "consumer price inflation, the year's change (the workbook's preferred CPI)"},
            str(y), "Great Britain")
_family({"door_cpi_fall_1797": "consumer prices' fall over the year (the workbook's preferred CPI)"}, "1797",
        "Great Britain")

# a backing changed: the five groups (the window build)
_P_END = "1970 to the data's end"
for k, (period, pop) in {"p1": ("1914", "suspensions of gold convertibility"),
                         "p2": ("1931 to 1936", "exits from gold"),
                         "p3d": (_P_END, "cuts in central-bank independence"),
                         "p3u": (_P_END, "rises in central-bank independence"),
                         "p4": (_P_END, "adoptions of an inflation target")}.items():
    _family({f"a2_{k}_mean": "mean change in inflation, less matched monies'",
             f"a2_{k}_band_lo": "no-effect range of the mean gap, low end",
             f"a2_{k}_band_hi": "no-effect range of the mean gap, high end",
             f"a2_{k}_eff_lo": "the effect's range, low end",
             f"a2_{k}_eff_hi": "the effect's range, high end",
             f"a2_{k}_n": "changes with a gap that can be read"},
            period, pop)
_family({"a2_p2_single": "exits whose gap rests on a single matched money"}, "1931 to 1936", "exits from gold")
_family({"a2_p4v_mean": "mean change in inflation, less matched monies', later targets",
         "a2_p4v_n": "adoptions with a gap, with later-dated targets"},
        _P_END, "adoptions of an inflation target")

# money crises and defaults (claim 1)
_P1 = "since 1970"
_family({"c1_breaks": "money crises dated", "c1_after_n": "money crises with a default or listed act in the prior 3 "
         "years", "c1_readable_n": "money crises whose nearby acts can be read",
         "c1_tot_readable_n": "money crises whose nearby acts can be read, the state's total debt",
         "c1_prv_readable_n": "money crises whose nearby acts can be read, private creditors",
         "c1_shared_breaks": "money crises of monies shared between states",
         "c1_once_breaks": "money crises with each shared decision counted once",
         "c1_once_after_n": "of those, crises after a creditor class newly in arrears",
         "c1_not2_after_n": "money crises after an act other than a default",
         "c1_not2_before_n": "money crises before an act other than a default",
         "c1_after_sr": "money crises with a default or listed act in the prior 3 years",
         "c1_tot_after_sr": "crises with a state default or listed act in the prior 3 years",
         "c1_prv_after_sr": "crises with a private-creditor default or listed act in the prior 3 years"},
        _P1, "monies under fiscal stress")
_family({"c1_base_sr": "share with a default or listed act in the prior 3 years",
         "c1_tot_base_sr": "share with a state default or listed act in the prior 3 years",
         "c1_prv_base_sr": "share with a private-creditor default or listed act in the prior 3 years",
         "c1_base_readable_n": "years of stress that held, whose acts can be read",
         "c1_tot_base_readable_n": "years of stress that held, readable, the state's total debt",
         "c1_prv_base_readable_n": "years of stress that held, readable, private creditors",
         "c1_fwd_tot_e_n": "years of stress outside war in which the state newly fell into default or met another "
                           "act on the list"},
        _P1, "strained years the money held")
_family({"c1_t2_lines": "dated lines of the default database", "c1_t2_inside": "of those, lines for states already in "
         "default"}, "1960 to 2024", "Bank of Canada–Bank of England default database")
_family({"c1_break_line": "the inflation line of a money crisis", "c1_onset_pi": "the inflation line above which a "
         "crisis's onset is dated", "c1_at_risk_pi": "inflation below which a stress year is read", "c1_onset_d": "the fall against the dollar that dates a crisis's onset",
         "c1_strain_debt": "the state's debt line of fiscal stress, share of GDP",
         "c1_strain_deficit": "the deficit line of fiscal stress, share of GDP"},
        "fixed in advance", "every money the study reads")

# who held (claim 2)
_P2 = "periods of stress entered since 1970, ten years after"
for p, what in {"c2_head": "the comparison fixed in advance", "c2_tb": "without the state's credit",
                "c2_np": "pegs and currency boards set aside"}.items():
    _family({f"{p}_d": f"held more often, two or more backings against fewer, points: {what}",
             f"{p}_lo": f"its 90% interval, low end: {what}", f"{p}_hi": f"its 90% interval, high end: {what}",
             f"{p}_n_fewer": f"periods of stress on the thin side (one backing or none): {what}",
             f"{p}_n_two": f"periods of stress with two or more backings: {what}"},
            _P2, "inconvertible monies under fiscal stress")
_family({"c2_np_fewer_in_default": "periods on the thin side of states already in default at entry",
         "c2_lines": "periods of fiscal stress compared", "c2_monies": "monies with a period of stress",
         "c2_margin": "the smallest difference that counts, fixed in advance",
         "c2_interval_level": "the interval's level", "c2_np_d_nocfa": "held more often, pegs set aside, without the "
         "CFA unions' members, points"}, _P2, "inconvertible monies under fiscal stress")
_family({"c3_line": "deposits losing to inflation by more than this, two years in a row",
         "c3_open_n": "cases readable on currency where capital is open and a foreign money at hand",
         "c3_closed_n": "cases readable on currency where it is not"},
        "since 1970", "monies whose deposits lost to inflation two years running")

# stablecoins and today
_family({"c4_coins": "stablecoins named in the fixed set of papers", "c4_coins_none": "coins with no line readable",
         "c4_coins_none_pct": "share of coins with no line readable", "c4_coin_lines": "coin-lines (four a coin)",
         "c4_unread": "coin-lines that cannot be read", "c4_yes": "coin-lines read yes", "c4_no": "coin-lines read no",
         "c4_issuer_coins": "coins whose launch documents were found and read",
         "c4_issuer_sought": "coins whose launch documents were sought",
         "c4_kappa": "agreement of two codings made apart, beyond chance (Cohen's kappa)",
         "c4_redeem_yes": "coins whose right to redeem can be read",
         "c4_redeem_any": "coins any holder may redeem", "c4_redeem_account": "coins only verified customers may "
         "redeem"}, "at launch", "stablecoins in central-bank and academic papers")
_family({"now_usd_index": "Garriga's legal index of central-bank independence, 0 to 1",
         "now_index_line": "the index's line fixed in advance", "now_usd_cobham_year": "the year of the Federal "
         "Reserve's inflation goal", "now_usd_cofer": "the dollar's share of allocated official reserves"},
        "the latest year each source reads", "the United States dollar")
_family({"now_eur_cofer": "the euro's share of allocated official reserves", "now_eur_members": "euro area members",
         "now_eur_tb_yes": "members not in default", "now_eur_tb_no": "members in default",
         "now_eur_tb_unread": "members whose default status cannot be read",
         "now_eur_force_no": "members with no capital controls", "now_eur_force_unread": "members whose controls "
         "cannot be read"}, "the latest year each source reads", "the euro and its members")
_family({"now_btc_cap": "the most bitcoins the protocol will ever release"}, "the protocol's schedule", "bitcoin")
_family({"matters_pts": "the size that matters: one point of a note's value or of inflation",
         "matters_ratio": "the size that matters for a ratio of chances"}, "set 2026-10-07", "this study's claims")

# map v11's printed keys (round 2, step w): the cited and frozen-data numbers (sources_v11.py) and map v11's cards
# (registry_v11.py) that carried no labels; each family's words checked against its source's passage or its card
_BJ = "Bernanke and James's 24 economies"
_family({"bj_gap_1932": "gap in wholesale-price deflation, on gold less off gold"}, "1932", _BJ)
_family({"bj_min_cover": "usual legal minimum gold cover of central-bank notes"},
        "between the wars", "central banks on the gold standard")
_family({"mandat_cap": "the legal ceiling on mandats issued, at face", "mandat_open": "the mandat's value in coin "
         "when it was issued", "mandat_summer": "the mandat's value in coin by early summer"},
        "March to summer 1796", "the mandat territorial, France")
_family({"assignat_1793": "the assignats' value against gold, share of face"}, "June 1793", "the assignats, France")
_family({"gb_low_silber": "the greenback dollar's lowest value in gold, per Silber",
         "gb_low_calomiris": "the greenback dollar's lowest value in gold, per Calomiris"}, "1864",
        "United States notes (greenbacks)")
_family({"cal_demand_notes_1863": "the demand notes' price in gold",
         "cal_greenbacks_1863": "the greenbacks' price in gold"}, "February 1863",
        "United States demand notes and greenbacks, in New York")
_family({"rw_countries": "countries Rolnick and Weber observe", "rw_both": "countries with both a commodity and a "
         "fiat period"}, "all years in the data", "Rolnick and Weber's countries")
_family({"rw_fiat_mean": "average inflation in all fiat observations",
         "rw_commodity_mean": "average inflation in all commodity observations"},
        "all years in the data", "Rolnick and Weber's 15 countries")
_family({"bs3_g10_gap": "inflation gap, float less gold standard"}, "1974-90 against 1881-1913",
        "the G10 economies and Switzerland")
_family({"bs3_all_above_us": "economies with inflation above the United States's",
         "bs3_all_nonus": "economies other than the United States in the table"}, "the float, 1974-90",
        "Bordo and Schwartz's 21 countries")
_family({"fsv_economies": "market economies observed", "fsv_above25": "economies whose inflation passed 25% a year "
         "at some point", "fsv_above50": "economies whose inflation passed 50% a year at some point",
         "fsv_above100": "economies whose inflation passed 100% a year at some point"}, "1960-96",
        "133 market economies, pegged or not")
_family({"fsv_line": "the line of very high inflation over 12 months, this study's collapse line",
         "fsv_line25": "the lower line of high inflation (Fischer, Sahay and Vegh)"}, "fixed by the source", "any money")
_family({"fomc_target": "the Federal Reserve's longer-run inflation goal"}, "since January 2012", "the United States")
_family({"sd_fixed_years": "years the stock of Swiss dinars stayed essentially fixed"}, "1991-2003",
        "the Swiss dinar, northern Iraq")
_family({"sd_rate": "Saddam dinars to one Swiss dinar, about"}, "July 1998 to January 2002",
        "the Swiss dinar, northern Iraq")
_family({"som_notes_bn": "unofficial shilling notes printed since 1991, estimated, billions"}, "1991 on",
        "the Somali shilling")
_family({"rm_mortgage_bn": "the Rentenbank's mortgage, its capital",
         "rm_redeem_sum": "the smallest sum of Rentenmarks redeemable into bonds",
         "rm_gov_cap_bn": "the cap on the Rentenbank's lending to the government",
         "rm_notes_bn": "Rentenmark notes outstanding, billion marks",
         "rm_debentures": "gold mortgage bonds issued on redemption, marks"}, "December 1923 to June 1924",
        "the Rentenmark, Germany")
_family({"terra_days": "days from the first break of the peg to the collapse"}, "May 2022", "Terra (UST)")
_family({"usdc_low": "USDC's lowest price, cents per dollar"}, "March 2023", "USDC")
_family({"judson_abroad_100s": "share of US hundred-dollar notes held abroad, estimated"}, "end of 2011",
        "US currency")
_CSA = "15 rich economies"
_family({"csa_economies": "economies compared", "csa_lo": "range of the off-gold less on-gold gap, low end",
         "csa_hi": "range of the off-gold less on-gold gap, high end"}, "1932-34", _CSA)
_CSD = "crises and strained years"
_P_CSD = "1970 to the data's end"
_family({"cs_d_ratio": "crises' share after a default over strained years' share",
         "cs_d_ratio_shared_once": "same ratio, a shared money's crises counted once a month",
         "cs_d_ratio_t2_private": "the same ratio, private creditors' arrears only"}, _P_CSD, _CSD)
_family({"csd_headline_lo": "the ratio's 95% range, low end", "csd_headline_hi": "the ratio's 95% range, high end",
         "csd_headline_after": "crises after a new default",
         "csd_headline_readable": "money crises that can be read"}, _P_CSD,
        "crises and strained years of the same stress spells")
_CSB = "17 rich economies"
_family({"c19_economies": "economies compared", "c20_set_apart": "economy-years above 100% inflation",
         "c20_convertible_mean": "average inflation in convertible years",
         "c20_fiat_mean": "average inflation in inconvertible years",
         "c20_main_lo": "range of the inflation gap, low end", "c20_main_hi": "range of the inflation gap, high end",
         "c20_median_lo": "range of the median gap, low end", "c20_median_hi": "range of the median gap, high end"},
        "1870-2020 minus wars and Bretton Woods", _CSB)
_family({"c20_era_1870_1913_convertible": "average inflation in convertible years",
         "c20_era_1870_1913_fiat": "average inflation in inconvertible years"}, "1870-1913", _CSB)
_family({"c20_era_1919_1938_convertible": "average inflation in convertible years",
         "c20_era_1919_1938_fiat": "average inflation in inconvertible years"}, "1919-38", _CSB)
_family({"c20_era_1972_2020_fiat": "average inflation in inconvertible years"}, "1972-2020", _CSB)
_family({"c4_redeem_unsettled": "coins whose sources disagree on who may redeem"}, "at launch",
        "stablecoins in central-bank and academic papers")

# CS-B's inconvertible years since 1972 by inflation-target adoption (C19 item 4; the grid check of 2026-10-08)
_family({"c19_target_before_mean": "average inflation in inconvertible years before the economy adopted an inflation target",
         "c19_target_from_mean": "average inflation in inconvertible years from the economy's inflation-target adoption",
         "c19_target_none_mean": "average inflation in inconvertible years of economies with no adoption counted",
         "c19_target_before_n": "inconvertible economy-years before adoption",
         "c19_target_from_n": "inconvertible economy-years from adoption",
         "c19_target_none_n": "inconvertible economy-years with no adoption counted"},
        "1972-2020", "the 17 rich economies of the Macrohistory Database, inconvertible years")

# Bernanke & James's yearly averages printed in the open (the grid checks of 2026-10-08)
for _y in (1932, 1933, 1934, 1935):
    _family({f"bj_gold_{_y}": "wholesale-price change, average of economies on gold",
             f"bj_off_{_y}": "wholesale-price change, average of economies off gold"},
            str(_y), "the economies of Bernanke and James's Table 2.2")
_family({"c19_target_none_matched": "average inflation of the economies with no adoption counted, in the adopters' "
                                   "own target years (year for year)"},
        "1991-2020", "the 17 rich economies of the Macrohistory Database, inconvertible years")
# the scope a reader taps (the narrow check of 2026-10-08, class 3): the adopters are six, the matched others eleven
_family({"c19_target_from_mean": "average inflation after adopting an inflation target",
         "c19_target_before_mean": "average inflation before adopting an inflation target",
         "c19_target_from_n": "inconvertible economy-years from adoption",
         "c19_target_before_n": "inconvertible economy-years before adoption"},
        "1972-2020", "Australia, Canada, Japan, Norway, Sweden, UK")
_family({"c19_target_none_matched": "average inflation in the adopters' target years"},
        "1991-2020", "the eleven other economies, inconvertible years")
