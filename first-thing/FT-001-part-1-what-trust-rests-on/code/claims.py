"""The claims registry (BLUEPRINT §5 d, P10; W14, F81): every claim map v11 makes (its claims table, P1-1 to P1-11,
the door and the components K1-K8 they serve), each typed, scoped, and resting on its sources' passages or its card.

Run after ``registry.py`` and ``readings.py`` (``run.py`` calls :func:`apply`): it reads ``results/numbers.json``,
puts each claim (validated by ``ft.numbers``: a key a claim rests on must be registered, a source must be a legal copy
read at its passage) and saves. The passages are the ones recorded at step a (``notes/sources.md`` and the notes it
names: the two harvests of 2026-10-08, the dossier's re-reads, the map's audits), closely paraphrased or quoted short,
with the page; the isolated check reads them against the sources. Held works (F86) are cited, never quoted at length.
The forms (step w onward) tag the units that make each claim; a claim no form makes is dropped there, never kept.

Two measured claims rest on reused builds whose committed protocols are their cards (CS-C on M4's A3 protocol, CS-F on
M4's frame a): they name the mission card (``M4-A3``, ``M4-frame-a``), accepted by the registry since the engine's
change of 2026-10-08.
"""

from __future__ import annotations

from pathlib import Path

from ft import numbers

STUDY = Path(__file__).resolve().parent.parent


def src(source: str, locator: str, passage: str, copy: str = "open", read: str = "passage") -> dict:
    return {"source": source, "locator": locator, "passage": passage, "copy": copy, "read": read}


BJ = ("Bernanke, B. & James, H. (1991), 'The Gold Standard, Deflation, and Financial Crisis in the Great Depression: An "
      "International Comparison', in Hubbard (ed.), Financial Markets and Financial Crises, NBER (chapter c11482)")
ES = "Eichengreen, B. & Sachs, J. (1985), 'Exchange Rates and Economic Recovery in the 1930s', NBER Working Paper 1498"
SV = "Sargent, T. J. & Velde, F. R. (1995), 'Macroeconomic Features of the French Revolution', JPE 103(3)"
WHITE = "White, E. N. (1995), 'The French Revolution and the Politics of Government Finance, 1770-1815', JEH 55(2)"
VW = ("Velde, F. R. & Weir, D. R. (1992), 'The Financial Market and Government Debt Policy in France, 1746-1793', "
      "JEH 52(1)")
BK = "Bordo, M. D. & Kydland, F. E. (1990), 'The Gold Standard as a Rule', NBER Working Paper 3367"
CAL = ("Calomiris, C. W. (1988), 'Price and Exchange Rate Determination during the Greenback Suspension', Oxford "
       "Economic Papers 40(4)")
WGR = ("Willard, K., Guinnane, T. & Rosen, H. (1995), 'Turning Points in the Civil War: Views from the Greenback "
       "Market', NBER Working Paper 5381")
SILBER = "Silber, W. L. (2007), When Washington Shut Down Wall Street, Princeton University Press"
BLR = ("Bordo, M. D., Landon-Lane, J. & Redish, A. (2004), 'Good versus Bad Deflation: Lessons from the Gold Standard "
       "Era', NBER Working Paper 10329")
DELONG = "DeLong, J. B. (1997), 'America's Peacetime Inflation: The 1970s', in Romer & Romer (eds.), Reducing Inflation"
BK01 = ("Barsky, R. & Kilian, L. (2001), 'Do We Really Know That Oil Caused the Great Stagflation? A Monetary "
        "Alternative', NBER Working Paper 8389")
BS = ("Bordo, M. D. & Schwartz, A. J. (1994), 'The Specie Standard as a Contingent Rule: Some Evidence for Core and "
      "Peripheral Countries, 1880-1990', NBER Working Paper 4860")
BORDO92 = ("Bordo, M. D. (1992), 'The Bretton Woods International Monetary System: An Historical Overview', NBER "
           "Working Paper 4033")
BHS = ("Bordo, M. D., Humpage, O. & Schwartz, A. J. (2006), 'The Historical Origins of U.S. Exchange Market "
       "Intervention Policy', NBER Working Paper 12662")
FRB19 = "Federal Reserve Bulletin, 1 October 1919"
FRB23 = "Federal Reserve Bulletin, December 1923"
FRB24 = "Federal Reserve Bulletin, August 1924"
FRED = "FRED CPIAUCNS, US consumer price index (frozen 2026-09-30)"
JST = "Jorda, Schularick & Taylor, Macrohistory Database, release 6 (frozen 2026-09-30)"
WDI = "World Bank, WDI FP.CPI.TOTL.ZG, consumer-price inflation (frozen 2026-09-30)"
WEO = "IMF World Economic Outlook, October 2013, Argentina end-of-period consumer prices, via DBnomics (frozen 2026-10-08)"
RW = ("Rolnick, A. J. & Weber, W. E. (1997), 'Money, Inflation, and Output under Fiat and Commodity Standards', "
      "JPE 105(6); FRB Minneapolis Quarterly Review 22(2) reprint")
FSV = "Fischer, S., Sahay, R. & Vegh, C. (2002), 'Modern Hyper- and High Inflations', NBER Working Paper 8930"
FOMC12 = "Federal Reserve, FOMC, Statement on Longer-Run Goals and Monetary Policy Strategy, 25 January 2012"
FOOTE = "Foote, C., Block, W., Crane, K. & Gray, S. (2004), 'Economic Policy and Prospects in Iraq', JEP 18(3)"
LW = ("Luther, W. J. & White, L. H. (2011), 'Positively Valued Fiat Money after the Sovereign Disappears: The Case of "
      "Somalia'")
DLT = ("de la Torre, A., Levy Yeyati, E. & Schmukler, S. (2003), 'Living and Dying with Hard Pegs', World Bank Policy "
       "Research Working Paper 2980")
LMS = "Liu, J., Makarov, I. & Schoar, A. (2023), 'Anatomy of a Run: The Terra Luna Crash', NBER Working Paper 31160"
SARGENT = "Sargent, T. J. (1982), 'The Ends of Four Big Inflations', in Hall (ed.), Inflation: Causes and Effects"
GRUBB = "Grubb, F. (2012), 'Is Paper Money Just Paper Money?', NBER Working Paper 17997"
JUDSON = ("Judson, R. (2012), 'Crisis and Calm: Demand for U.S. Currency at Home and Abroad from the Fall of the Berlin "
          "Wall to 2011', Federal Reserve IFDP 1058")
POSEN = ("Posen, A. S. (1995), 'Declarations Are Not Enough: Financial Sector Sources of Central Bank Independence', "
         "NBER Macroeconomics Annual 10")
LL = "Leeper, E. M. & Leith, C. (2016), 'Understanding Inflation as a Joint Monetary-Fiscal Phenomenon', NBER WP 21867"
FSR = "Board of Governors of the Federal Reserve System, Financial Stability Report, May 2023"
FEDS = "FEDS Notes, 'Primary and Secondary Markets for Stablecoins', 23 February 2024"
HKMA = "Hong Kong Monetary Authority, the Convertibility Undertakings (its description of the Linked Exchange Rate System)"

B3 = "bank/maps/FT-001/missions"


def claims() -> dict[str, dict]:
    C: dict[str, dict] = {}
    # --- the door
    C["door-1931"] = dict(
        text="In September 1931 Britain cut the pound from gold; in 1932, wholesale prices in the countries that had "
             "left gold fell about {{bj_gap_1932}} points less than in those still on it.",
        type="cases", component="K3", claim_type="comparative", keys=["bj_gap_1932", "bj_gold_1932", "bj_off_1932"],
        sources=[src(BJ, "Table 2.1, p. 37; p. 42; Table 2.2, p. 43", "Britain's first act, September 1931; 'the "
                     "twelve percentage point difference in rates of deflation between gold and non-gold countries in "
                     "1932' (wholesale prices, log changes; their 24 economies, exchange controls counted as leaving).",
                     read="chapter")])
    C["door-uk-1932"] = dict(
        text="Britain's consumer prices fell by {{uk_cpi_1932_fall}} over 1932: the pound gained purchasing power; what "
             "fell was its value against staying on gold.",
        type="cases", component="K3", claim_type="descriptive", keys=["uk_cpi_1932", "uk_cpi_1932_fall"],
        sources=[src(JST, "cpi, GBR, 1931-1932", "The United Kingdom's consumer price index, 1932 against 1931.",
                     copy="data", read="full")])
    C["door-mandat"] = dict(
        text="In March 1796 France issued the mandat, paper any holder could use to buy national land at a fixed "
             "price; it opened at about {{mandat_open}} of its face value in coin and was worth about "
             "{{mandat_summer}} by early summer, with no note issued beyond its legal ceiling.",
        type="cases", component="K5", claim_type="descriptive", keys=["mandat_open", "mandat_summer", "mandat_cap"],
        sources=[src(SV, "pp. 510, 515", "Estates earmarked; 2,400 millions of mandats to retire the assignats at 30 "
                     "to 1 and finance 1796's spending, land sold at fixed prices; 35% of face in March, 6% by early "
                     "summer, failing although no note went beyond the ceiling; sales at 22 times income, a 25% "
                     "deposit.", copy="held", read="chapter"),
                 src(WHITE, "p. 247", "The mandat was legal tender, received at par with specie, limited in quantity; "
                     "the underpriced land was rapidly claimed and the paper became fiat money.", copy="held")])
    # --- K1, what backing does
    C["k1-what-backing-does"] = dict(
        text="A backing limits how much money can be issued and gives holders a way out; a suspension with a return "
             "to gold expected is a promise deferred, priced on the news about that return.",
        type="established", component="K1", claim_type="causal",
        sources=[src(BK, "pp. 2-3", "The gold standard was intended as a contingent rule: convertibility could be "
                     "suspended in a wartime emergency on the understanding that it would be restored at the original "
                     "price when the emergency passed; outside the core, more a desirable goal than an operational "
                     "constraint (paraphrase)."),
                 src(CAL, "pp. 719-720, 747", "Resumption expectations play a central role in the exchange rate and the "
                     "price level; fiscal shocks and battle news moved the expected timing of resumption; the paper "
                     "favours Mitchell's approach over Friedman and Schwartz's quantity explanation.", copy="library",
                     read="full"),
                 src(WGR, "abstract; p. 17", "Speculators understood that the probability of redemption depended on "
                     "the Union army's fortunes and political news; the end of Early's raid in July 1864 was the "
                     "war's largest one-day shift.", read="full")])
    C["k1-greenbacks"] = dict(
        text="At their 1864 low the greenbacks were worth about {{gb_low_silber}} to {{gb_low_calomiris}} cents in "
             "gold, depending on the series, and they returned to par in 1879.",
        type="cases", component="K1", claim_type="descriptive", keys=["gb_low_silber", "gb_low_calomiris"],
        sources=[src(SILBER, "p. 27", "The year's highest gold price fell 'from $285 in 1864 to $107 in 1878' (the "
                     "greenback's gold value at its low computed from it).", copy="held"),
                 src(CAL, "p. 719", "The greenback price of the gold dollar 'ranged from par to 2.5' over the "
                     "suspension (monthly series).", copy="library", read="full")])
    C["p1-8-cs-c"] = dict(
        text="Read as the market's odds of a return to gold, the premiums priced Britain's suspended notes at "
             "{{a3_restriction_p_low}} of their gold value in their lowest year and the greenbacks at "
             "{{a3_greenback_p_low}} in their lowest month, implying waits for gold of {{a3_restriction_wait_low}} "
             "to {{a3_restriction_wait_high}} years and {{a3_greenback_wait_low}} to {{a3_greenback_wait_high}}.",
        type="measured", card="M4-A3", component="K1", claim_type="descriptive",
        keys=["a3_restriction_p_low", "a3_greenback_p_low", "a3_restriction_wait_low", "a3_restriction_wait_high",
              "a3_greenback_wait_low", "a3_greenback_wait_high"],
        scope={"measure": "the paper's value in gold and the wait for gold its premium implies at the interest rates "
                          "the protocol fixes", "period": "1797-1821 and 1862-79",
               "population": "the Bank of England's notes under the Restriction; the US greenbacks"})
    # --- K2, a backed money is worth what its backing is worth
    C["p1-3-worth-its-backing"] = dict(
        text="Under the gold standard the quantity of money was tied to the stock of gold: prices fell while gold was "
             "scarce, to 1896, and rose once new gold was found, with the backing standing.",
        type="established", component="K2", claim_type="causal",
        sources=[src(BLR, "pp. 1, 4", "Mild deflation from 1870 to 1896 and inflation after; 'the gold standard tied "
                     "the quantity of money to the stock of gold'; world gold output low to 1890 and rising after the "
                     "South African, Australian and North American discoveries."),
                 src(DELONG, "p. 248", "'Since 1896, there has been a steady upward drift in the price level' (the US "
                     "GDP deflator).", read="chapter")])
    C["p1-3-dollar-1914-20"] = dict(
        text="The dollar stayed convertible into gold at home through 1914-20, with gold exports embargoed from 1917 "
             "to June 1919 and exchange controls from 1918, and it lost about {{us_pp_loss_1914_20}} of its "
             "purchasing power between June 1914 and June 1920.",
        type="cases", component="K2", claim_type="descriptive", keys=["us_pp_loss_1914_20", "us_cpi_1914_06",
                                                                      "us_cpi_1920_06"],
        sources=[src(BS, "Table 1A, printed pp. 57-58, row United States", "Gold convertibility 1879-1933 with no "
                     "suspension in 1914-20 (restrictions of payment by banks in 1893 and 1907 aside).",
                     read="chapter"),
                 src(BHS, "pp. 7-8", "The gold drain 'led to the imposition of an embargo on gold exports in June "
                     "1917, and the institution of strict exchange controls beginning in February 1918'."),
                 src(FRB19, "p. 918", "Gold exported 'since the removal of the gold embargo on June 7' (1919)."),
                 src(FRED, "June 1914 and June 1920", "The index at 9.9 in June 1914 and 20.9 in June 1920.",
                     copy="data", read="full")])
    C["k2-cover"] = dict(
        text="Between the wars the statutory minimum gold cover of a note issue was usually {{bj_min_cover}}: a "
             "floor, not the cover held.",
        type="established", component="K2", claim_type="descriptive", keys=["bj_min_cover"],
        sources=[src(BJ, "p. 38", "Central banks were usually required by statute to hold gold cover of at least "
                     "40% of their note issue (paraphrase).", read="chapter")])
    # --- K3, leaving gold in the 1930s
    C["p1-1-1930s"] = dict(
        text="In the 1930s, wholesale prices in the countries that left gold stabilised by 1933 and rose mildly after, "
             "while those still on gold kept falling until the gold standard's end in 1936.",
        type="established", component="K3", claim_type="comparative",
        keys=["bj_gold_1932", "bj_off_1932", "bj_gold_1933", "bj_off_1933", "bj_gold_1934", "bj_off_1934",
              "bj_gold_1935", "bj_off_1935"],
        sources=[src(BJ, "p. 42; Table 2.2, p. 43", "'Price levels in countries off the gold standard have "
                     "stabilized by 1933 (with one or two exceptions), and these countries experience mild inflations "
                     "in 1934-36'; 'the gold standard countries continue to deflate … until the gold standard's "
                     "dissolution in 1936' (wholesale prices).", read="chapter")])
    C["k3-how"] = dict(
        text="In 1932 money growth differed little between leavers and stayers; Bernanke and James suggest the gap "
             "came through expectations, and Eichengreen and Sachs find that depreciation put upward pressure on "
             "prices; from 1933, leaving freed central banks to expand money.",
        type="established", component="K3", claim_type="causal",
        sources=[src(BJ, "p. 42", "Despite the 1932 difference in deflation, 'the differences in average money growth "
                     "in that year … are minor'; leaving gold 'afforded countries more latitude to expand their money "
                     "supplies and thus to escape deflation'.", read="chapter"),
                 src(ES, "p. 13", "Depreciation, 'by putting upward pressure on prices', reduced the real wage.",
                     read="full")])
    C["k3-chosen"] = dict(
        text="Countries chose when to leave, largely by their experience of the 1920s, and the depreciations helped "
             "each leaver at its neighbours' expense.",
        type="established", component="K3", claim_type="descriptive",
        sources=[src(ES, "pp. 9-10, 20", "The timing of devaluation was heavily influenced by considerations exogenous "
                     "to their model, the historical experience of the 1920s; depreciation conferred macroeconomic "
                     "benefits on the initiating country, but as made it was beggar-thy-neighbour.", read="full")])
    C["p1-2-cs-a"] = dict(
        text="On consumer prices, across {{csa_economies}} economies, inflation in 1932-34 ran {{cs_a_pooled}} points "
             "a year higher off gold than on it; the range, {{csa_lo}} to {{csa_hi}}, includes no difference: if "
             "leaving gold raised consumer-price inflation in those years, it raised it by less than {{csa_hi}} "
             "points a year.",
        type="measured", card="C18", component="K3", claim_type="comparative",
        keys=["cs_a_pooled", "csa_lo", "csa_hi", "csa_economies", "cs_a_pooled_no_exchange_control",
              "cs_a_pooled_no_spain"],
        scope={"measure": "consumer-price inflation off gold less on gold, pooled by year weights",
               "period": "1932-34", "population": "the economies of Bernanke & James's Table 2.1 in the Macrohistory "
                                                   "Database, classed by their dates"})
    C["k3-1971"] = dict(
        text="US prices had been rising under the Bretton Woods tie since 1965 (the index from {{us_cpi_1965_01}} to "
             "{{us_cpi_1971_01}} by January 1971); the 1970s' inflation is disputed between oil supply shocks and "
             "monetary and policy explanations that link it to Bretton Woods' breakdown.",
        type="established", component="K3", claim_type="descriptive", keys=["us_cpi_1965_01", "us_cpi_1971_01"],
        sources=[src(DELONG, "pp. 249-251, 259", "No one with the mandate stopped inflation before Volcker; Bretton "
                     "Woods broke down at the beginning of the 1970s, and thereafter domestic political economy "
                     "predominated.", read="chapter"),
                 src(BK01, "abstract; p. 3", "Oil price increases were not nearly as essential to the stagflation as "
                     "believed; monetary expansion can generate it; they link the shift to the breakdown of Bretton "
                     "Woods (Blinder and Bruno & Sachs the oil-shock reading).", read="abstract"),
                 src(FRED, "January 1965 and January 1971", "The index at 31.2 and 39.8.", copy="data",
                     read="full")])
    C["p1-11-exits"] = dict(
        text="After the 1970-73 exits from the dollar, rich economies' inflation spread: under Bretton Woods all "
             "{{bs3_exits_n}} ran at or above the United States, at {{bs3_exits_bw_min}} to {{bs3_exits_bw_max}} a "
             "year; in the float of 1974-90 they ran from {{bs3_exits_float_min}} to {{bs3_exits_float_max}}, "
             "{{bs3_exits_below_us}} below the US's {{bs3_usa_float}} and {{bs3_exits_above_us}} above.",
        type="established", component="K3", claim_type="descriptive",
        keys=["bs3_exits_n", "bs3_exits_bw_min", "bs3_exits_bw_max", "bs3_exits_float_min", "bs3_exits_float_max",
              "bs3_exits_below_us", "bs3_exits_above_us", "bs3_usa_float", "bs3_all_above_us", "bs3_all_nonus"],
        sources=[src(BS, "Table 3, printed p. 62, row j and its rows", "Inflation in GNP deflators, log-trend rates, "
                     "by regime (Bretton Woods 1946-70, the float 1974-90), for the G10 economies and Switzerland "
                     "and 21 countries in all.", read="chapter"),
                 src(BORDO92, "pp. 51-53", "With US inflation spreading through dollar reserves, 'the only alternative "
                     "to importing U.S. inflation was to float — the route taken by all countries in 1973' (Darby et "
                     "al.'s reading, through Bordo).")])
    # --- K4, the long run
    C["p1-4-rolnick-weber"] = dict(
        text="In each of the {{rw_both}} countries Rolnick and Weber observe under both standards, inflation was "
             "higher under fiat money; over all their observations it averaged {{rw_fiat_mean}} a year under fiat "
             "standards against {{rw_commodity_mean}} under commodity standards.",
        type="established", component="K4", claim_type="comparative",
        keys=["rw_both", "rw_countries", "rw_fiat_mean", "rw_commodity_mean"],
        sources=[src(RW, "pp. 12, 13, 16", "Of their fifteen countries, twelve had both a commodity and a fiat period; "
                     "inflation was higher under fiat in every one; 9.17% a year over all fiat observations against "
                     "1.75% over all commodity ones; temporary suspensions with a return counted as commodity "
                     "standards; the facts are not read as causal.", copy="held")])
    C["p1-4-bordo-schwartz"] = dict(
        text="In the G10 economies and Switzerland, inflation in the float of 1974-90 ran about {{bs3_g10_gap}} "
             "points a year above the gold standard of 1881-1913 (by country, a median of {{bs3_gap_median}}, from "
             "{{bs3_gap_min}} in Japan to {{bs3_gap_max}} in Italy), the Bretton Woods years at {{bs3_g10_bw}} "
             "between.",
        type="established", component="K4", claim_type="comparative",
        keys=["bs3_g10_gap", "bs3_g10_gold", "bs3_g10_float", "bs3_g10_bw", "bs3_gap_median", "bs3_gap_min",
              "bs3_gap_max", "bs3_gap_n"],
        sources=[src(BS, "Table 3, printed p. 62; pp. 1, 38", "Row j: 0.8% under gold, 3.5% under Bretton Woods, "
                     "6.4% under the float (GNP deflators, log-trend rates; the gold era holding some inconvertible "
                     "monies); the gold era's stability 'may also reflect the absence of major shocks'.",
                     read="chapter")])
    C["p1-4-all-monies"] = dict(
        text="Among {{fsv_economies}} market economies in 1960-96, pegged or not, {{fsv_above25}} passed "
             "{{fsv_line25}} a year at some point and {{fsv_above100}} passed {{fsv_line}}, while most stayed below "
             "{{fsv_line25}} most of the time.",
        type="established", component="K4", claim_type="descriptive",
        keys=["fsv_economies", "fsv_above25", "fsv_above50", "fsv_above100", "fsv_line25", "fsv_line"],
        sources=[src(FSV, "printed p. 7", "Of 133 market economies in 1960-96, 92 had inflation above 25% at some "
                     "point, 49 above 50%, 25 above 100%; 'most countries, most of the time' below 25%; no regime "
                     "classification.", read="chapter")])
    C["k4-by-choice"] = dict(
        text="Today's central banks aim for a little inflation by choice: the Federal Reserve's goal is "
             "{{fomc_target}} a year on consumer spending prices.",
        type="established", component="K4", claim_type="descriptive", keys=["fomc_target"],
        sources=[src(FOMC12, "the statement", "'inflation at the rate of 2 percent, as measured by the annual change "
                     "in the price index for personal consumption expenditures, is most consistent over the longer "
                     "run' with the mandate.", read="full")])
    C["p1-7-cs-b"] = dict(
        text="Across {{c19_economies}} rich economies in 1870-2020, war and Bretton Woods years apart, inflation "
             "averaged {{c20_fiat_mean}} a year in inconvertible years against {{c20_convertible_mean}} in "
             "convertible ones: a gap of {{cs_b_gap_set_apart}} points, {{c20_main_lo}} to {{c20_main_hi}}, with the "
             "{{c20_set_apart}} economy-years above {{fsv_line}} set apart.",
        type="measured", card="C20", component="K4", claim_type="comparative",
        keys=["cs_b_gap_set_apart", "c20_main_lo", "c20_main_hi", "c20_fiat_mean", "c20_convertible_mean",
              "c20_set_apart", "c19_economies", "cs_b_median_gap", "c20_median_lo", "c20_median_hi"],
        scope={"measure": "average consumer-price inflation, inconvertible years less convertible years",
               "period": "1870-2020", "population": "17 rich economies of the Macrohistory Database, each year classed "
                                                   "by Bordo & Schwartz's Table 1A"})
    C["p1-7-cs-b-eras"] = dict(
        text="Before 1914 inconvertible years ran at about the same inflation as convertible ones "
             "({{c20_era_1870_1913_fiat}} against {{c20_era_1870_1913_convertible}}); the gap comes from the "
             "interwar years and the float since 1972, which averaged {{c20_era_1972_2020_fiat}}: "
             "{{c19_target_from_mean}} from adoption of an inflation target in the six economies that adopted one, "
             "{{c19_target_before_mean}} before it, {{c19_target_none_mean}} with no adoption counted (C19); every "
             "dated adoption came in 1991 or later, and in the same years the economies with no adoption counted "
             "averaged {{c19_target_none_matched}}: inflation was low with or without a formal adoption.",
        type="measured", card="C20", component="K4", claim_type="descriptive",
        keys=["c20_era_1870_1913_fiat", "c20_era_1870_1913_convertible", "c20_era_1919_1938_fiat",
              "c20_era_1919_1938_convertible", "c20_era_1972_2020_fiat", "c19_target_from_mean",
              "c19_target_before_mean", "c19_target_none_mean", "c19_target_from_n", "c19_target_before_n",
              "c19_target_none_n", "c19_target_none_matched"],
        scope={"measure": "average consumer-price inflation by class and calendar era",
               "period": "1870-1913, 1919-38, 1972-2020", "population": "17 rich economies of the Macrohistory "
                                                                       "Database"})
    # --- K5, neither necessary nor a guarantee
    C["p1-5-unbacked-held"] = dict(
        text="Monies with nothing behind them have run for decades without collapsing: no year of the rich economies' floats since "
             "1972 crossed {{fsv_line}} inflation, and northern Iraq's "
             "Swiss dinar, a stock fixed for about {{sd_fixed_years}} years and redeemable into nothing, kept its "
             "value against the Saddam dinar.",
        type="cases", component="K5", claim_type="descriptive",
        keys=["c20_float_years_above_line", "sd_fixed_years", "sd_rate"],
        sources=[src(JST, "cpi, the 17 economies, 1972-2020", "Annual consumer-price inflation in the inconvertible "
                     "years since 1972 (C20's count of years above 100%).", copy="data", read="full"),
                 src(FOOTE, "p. 61", "The supply of Swiss dinars 'had remained essentially fixed for 13 years', "
                     "letting the north escape Iraq's ruinous inflation; about 100 Saddam dinars to one from July 1998 "
                     "to January 2002.", copy="held")])
    C["k5-pair"] = dict(
        text="Land stood behind both a money that collapsed and one that held, each capped by law and each "
             "financing its state: France's mandat in 1796 and Germany's Rentenmark from 1923.",
        type="cases", component="K5", claim_type="descriptive",
        sources=[src(SV, "pp. 510-512", "The mandat, against national estates, capped at 2,400 millions, issued "
                     "partly to finance 1796's spending, fell to 6% of face by early summer; revenues were not raised "
                     "and two-thirds of the debt was defaulted in 1797.", copy="held", read="chapter"),
                 src(FRB23, "p. 1281", "The Rentenbank's capital a mortgage of 3.2 billion gold marks, half on "
                     "agricultural land, half on industrial, commercial and banking property; notes redeemable in sums "
                     "of 500 into 5% gold mortgage bonds; not legal tender, taken in all payments to the government; "
                     "1.2 billion lent to the Reich to cover the budget deficit."),
                 src(SARGENT, "p. 83", "Binding limits on total Rentenmarks (3.2 billion) and on issue to the "
                     "government (1.2 billion); then government borrowing stopped, the budget balanced and 'inflation "
                     "stopped'.", read="chapter")])
    C["k5-rentenmark"] = dict(
        text="The Rentenmark was redeemable, in sums of {{rm_redeem_sum}} marks, into the bank's gold mortgage bonds, "
             "and almost no one redeemed: {{rm_debentures}} marks of bonds against {{rm_notes_bn}} billion of notes "
             "in June 1924; its lending to the Reich was capped at {{rm_gov_cap_bn}} billion, lent at that maximum.",
        type="cases", component="K5", claim_type="descriptive",
        keys=["rm_redeem_sum", "rm_debentures", "rm_notes_bn", "rm_gov_cap_bn", "rm_current_exp_bn",
              "rm_mortgage_bn"],
        sources=[src(FRB23, "p. 1281", "Redemption in sums of 500 into the Rentenbank's 5% gold mortgage bonds; "
                     "lending to the government 1.2 billion, the legal maximum, to cover the budget deficit."),
                 src(FRB24, "p. 636", "About 1.2 billion lent to the government, 1.0 billion to current expenses; "
                     "2.4 billion the present note limit; 196,000 marks of debentures against 2.05 billion of "
                     "notes.")])
    C["k5-other-collapses"] = dict(
        text="The assignats, sold against land at auction, had lost about half their gold value by June 1793, before "
             "the hyperinflation; Terra, exchangeable for a dollar's worth of its issuer's own token, collapsed in "
             "{{terra_days}} days in May 2022.",
        type="cases", component="K5", claim_type="descriptive", keys=["assignat_1793", "terra_days"],
        sources=[src(VW, "p. 17, fn 49", "Assignats 'backed by the national wealth'; by June 1793 'their value "
                     "against gold had fallen to about 50 percent of face value'.", copy="held"),
                 src(LMS, "abstract; pp. 2-3", "UST was backed not by off-chain collateral but by a contract exchanging "
                     "one UST for $1 worth of LUNA; it collapsed in three days in May 2022.")])
    C["k5-boards"] = dict(
        text="Currency boards came at or after very high inflations that then fell: Estonia's at "
             "{{est_cpi_1993}} in 1993 and {{est_cpi_1998}} by 1998; Bulgaria's after {{bgr_cpi_1997}} in 1997, at "
             "{{bgr_cpi_1999}} by 1999; Hong Kong's, redeemable by banks only, between {{hk_cpi_min}} and "
             "{{hk_cpi_max}} a year since 1983; Argentina's broke in January 2002, and prices rose {{arg_cpi_2002}} "
             "that year.",
        type="cases", component="K5", claim_type="descriptive",
        keys=["est_cpi_1993", "est_cpi_1994", "est_cpi_1998", "bgr_cpi_1996", "bgr_cpi_1997", "bgr_cpi_1998",
              "bgr_cpi_1999", "hk_cpi_min", "hk_cpi_max", "arg_cpi_2002"],
        sources=[src(WDI, "EST, BGR, HKG", "Annual consumer-price inflation, 1983 on.", copy="data", read="full"),
                 src(WEO, "ARG, PCPIEPCH, 2002", "Consumer prices up 40.95% December to December 2002.", copy="data",
                     read="full"),
                 src(DLT, "pp. 3-4, 10-11", "The rule precluded pesos not backed by hard dollars, up to a third of "
                     "reserves in Argentine dollar bonds; the April 2001 amendments effectively eliminated the issue "
                     "rule; convertibility collapsed in January 2002.", read="full"),
                 src(HKMA, "the Convertibility Undertakings", "The HKMA converts US dollars and Hong Kong dollars upon "
                     "request by banks.")])
    C["k5-somalia"] = dict(
        text="The Somali shilling kept circulating at a positive value with no state behind it after 1991, while an "
             "estimated {{som_notes_bn}} billion unofficial notes were printed.",
        type="cases", component="K5", claim_type="descriptive", keys=["som_notes_bn"],
        sources=[src(LW, "sections 2.2-2.3 (library passages, no page)", "Somalis kept accepting shillings without "
                     "sovereign support; an estimated 481 billion unofficial notes printed since 1991 (Symes); "
                     "Somaliland's taking them for taxes in 1991-95 they doubt was real support.", copy="held")])
    C["k5-existence"] = dict(
        text="We read these cases as existence only: they show that each outcome happened, never how often, and no "
             "trait in them is read as what decides whether a money collapses.",
        type="judgement", component="K5", claim_type="judgement")
    # --- K6, what can do backing's job instead
    C["k6-other-limits"] = dict(
        text="Other things can do backing's job: a cap on issue with a balanced budget, the state taking the money in "
             "taxes, a fixed stock, and demand from abroad.",
        type="established", component="K6", claim_type="causal",
        keys=["cal_demand_notes_1863", "cal_greenbacks_1863", "judson_abroad_100s"],
        sources=[src(SARGENT, "pp. 45, 83", "In effect the notes 'were backed by the government's pursuit of an "
                     "appropriate budget policy'; the Rentenmark's change of unit was cosmetic, the caps and the "
                     "balanced budget the substance.", read="chapter"),
                 src(GRUBB, "pp. 3, 19, 53", "Colonial paper was redeemed by accepting it for future taxes; trading "
                     "below face 'is not depreciation, but simply time-discounting'.", read="full"),
                 src(CAL, "Table 6, pp. 739-741", "The 1861 demand notes, taken for customs duties at par with gold, "
                     "stood at 99.4 in gold when greenbacks stood at 58.1 (28 February 1863): 'it was expected "
                     "backing that distinguished demand notes from greenbacks'.", copy="library", read="full"),
                 src(JUDSON, "p. 12", "About half of all US currency, and about 65 percent of $100s, were held abroad "
                     "at the end of 2011.")])
    C["k6-independence"] = dict(
        text="Whether central-bank independence itself lowers inflation is disputed: the correlation is not "
             "evidence of cause.",
        type="established", component="K6", claim_type="descriptive",
        sources=[src(POSEN, "p. 253", "He rejects reading 'the negative correlation between average inflation rates "
                     "and indices of central bank independence as prima facie evidence of a causal relationship' "
                     "(Alesina & Summers named).", read="chapter")])
    C["p1-9-cs-f"] = dict(
        text="Within five years of a central bank's legal independence, inflation's change differed from matched "
             "monies' by {{a2_p3u_mean}} points on average over {{a2_p3u_n}} changes, inside the {{a2_p3u_band_lo}} "
             "to {{a2_p3u_band_hi}} that scenarios with no effect give; after an inflation target's adoption, by "
             "{{a2_p4_mean}} over {{a2_p4_n}}, inside {{a2_p4_band_lo}} to {{a2_p4_band_hi}}. Read as ranges on the "
             "effect: {{a2_p3u_eff_lo}} to {{a2_p3u_eff_hi}}, and {{a2_p4_eff_lo}} to {{a2_p4_eff_hi}}.",
        type="measured", card="M4-frame-a", component="K6", claim_type="comparative",
        keys=["a2_p3u_mean", "a2_p3u_n", "a2_p3u_band_lo", "a2_p3u_band_hi", "a2_p4_mean", "a2_p4_n",
              "a2_p4_band_lo", "a2_p4_band_hi", "a2_p3u_eff_lo", "a2_p3u_eff_hi", "a2_p4_eff_lo", "a2_p4_eff_hi"],
        scope={"measure": "inflation's change after the change less matched monies', mean gap, against the band "
                          "scenarios with no effect give", "period": "five years either side of each change",
               "population": "central-bank reforms raising independence and inflation-target adoptions in frame a's "
                             "window build, with matched non-changers"})
    # --- K7, what came before money crises; the fiscal root
    C["k7-fiscal-roots"] = dict(
        text="Economists generally agree that great inflations have fiscal roots: deficits explain high inflation, "
             "though across countries no long-run link shows, and year by year the link holds only where inflation "
             "is high.",
        type="established", component="K7", claim_type="causal",
        sources=[src(LL, "p. 87", "'Economists generally agree that historical episodes of high and volatile "
                     "inflation rates inevitably have fiscal roots.'"),
                 src(FSV, "pp. 10, 34", "'By and large, we find that fiscal deficits indeed explain high inflation'; "
                     "no significant long-run cross-section relationship between deficits and inflation, the link "
                     "holding in high-inflation countries.", read="chapter")])
    C["k7-acts-before-crises"] = dict(
        text="Of the {{c1_readable_n}} money crises since 1970 whose acts we could read, {{c1_after_n}} came after a "
             "default (a creditor class newly in arrears) or another act on our list; so did {{c1_base_sr}} of the "
             "strained years in which the money held; an act other than a default came first in only "
             "{{c1_not2_after_n}} crises. Counting only a default newly begun on the state's total debt, "
             "{{c1_tot_after_sr}} of crises and {{c1_tot_base_sr}} of strained years.",
        type="measured", card="C15", component="K7", claim_type="descriptive",
        keys=["c1_readable_n", "c1_after_n", "c1_after_sr", "c1_base_sr", "c1_not2_after_n", "c1_t2_lines",
              "c1_t2_inside", "c1_tot_after_sr", "c1_tot_base_sr", "c1_tot_after_n", "c1_tot_readable_n",
              "c1_break_line", "c1_at_risk_pi"],
        scope={"measure": "shares of money crises and of strained years that held with an act on the list in the "
                          "year before", "period": "1970 to the panel's common end",
               "population": "the panel's money crises and years of fiscal stress whose acts can be read"})
    C["p1-6-cs-d"] = dict(
        text="On like-for-like populations, money crises followed a newly missed payment about {{cs_d_ratio}} times "
             "as often as strained years that held; the range, {{csd_headline_lo}} to {{csd_headline_hi}}, includes no "
             "difference: if a missed payment made a crisis more likely, it did so by a factor below "
             "{{csd_headline_hi}}.",
        type="measured", card="C16", component="K7", claim_type="comparative",
        keys=["cs_d_ratio", "csd_headline_lo", "csd_headline_hi", "csd_headline_after", "csd_headline_readable",
              "cs_d_ratio_shared_once", "cs_d_ratio_t2_private"],
        scope={"measure": "share of readable money crises after a default over share of readable strained years "
                          "with one", "period": "1970 to the panel's common end",
               "population": "C07's R10 population: breaks and strained years from the same spells"})
    # --- K8, where today's monies stand
    C["p1-10-today"] = dict(
        text="We read today's monies on each job: the dollar and the euro rest on institutions and taxes, redeemable "
             "into nothing; reserve-backed stablecoins bring backing back, redeemable by verified customers only and "
             "worth what their reserves are worth; gold has no issuer; bitcoin has a fixed limit and no one who "
             "takes it back.",
        type="judgement", component="K8", claim_type="judgement")
    C["p1-10-cs-e"] = dict(
        text="Of the {{c4_coins}} stablecoins named in a fixed set of papers, {{c4_redeem_yes}} state who may redeem "
             "them: {{c4_redeem_account}} only verified customers, {{c4_redeem_any}} any holder.",
        type="measured", card="C14", component="K8", claim_type="descriptive",
        keys=["c4_coins", "c4_redeem_yes", "c4_redeem_account", "c4_redeem_any", "c4_coins_none"],
        scope={"measure": "who may redeem each coin, read in its issuer's documents", "period": "the documents as "
                          "frozen in 2026", "population": "the stablecoins named in frame g's fixed set of papers"})
    C["k8-usdc"] = dict(
        text="In March 2023 USDC, redeemable by verified customers in banking hours, fell to {{usdc_low}} cents and "
             "came back near a dollar after the deposit guarantees.",
        type="cases", component="K8", claim_type="descriptive", keys=["usdc_low"],
        sources=[src(FSR, "p. 55", "With $3.3 billion of its reserves at Silicon Valley Bank, USDC fell 'temporarily "
                     "below its target $1 value to as low as 87 cents', stabilising near $1 after the guarantees."),
                 src(FEDS, "the note", "Circle said redemption was 'constrained by the working hours of the U.S. "
                     "banking system'.")])
    # --- the answer
    C["headline"] = dict(
        text="Unbacked monies have had more inflation, about {{bs3_g10_gap}} points a year more in the rich "
             "economies' float of 1974-90 than in their gold era, but a backing is neither necessary nor a "
             "guarantee: monies with nothing behind them have run for decades without collapsing, the dollar, convertible into gold at "
             "home, lost half its purchasing power in 1914-20, and land stood behind both a money that collapsed and "
             "one that held.",
        type="judgement", component="answer", claim_type="judgement", headline=True,
        keys=["bs3_g10_gap"])
    # the payoff (step w, map v11 §5): what the reader can ask of any money, readable at the time
    C["what-to-ask"] = dict(
        text="We would ask four questions of any money, each readable in public documents at the time: who can "
             "create more of it and what stops them; who may redeem it, and into what; what the asset behind it is "
             "worth and whose it is; and what else its holders could use.",
        type="judgement", component="answer", claim_type="judgement")
    return C


def apply(path: Path | None = None) -> None:
    reg = numbers.Registry.load(path or STUDY / "results" / "numbers.json")
    reg.claims.clear()
    for cid, c in claims().items():
        reg.put_claim(cid, **c)
    reg.save()


if __name__ == "__main__":
    apply()
