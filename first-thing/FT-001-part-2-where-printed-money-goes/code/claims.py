"""The claims registry (BLUEPRINT §5 d, P10; W14, F81): every claim map v15 makes (its claims table, P2-1 to P2-10,
and the components K1-K7 they serve), each typed, scoped, and resting on its sources' passages or its card.

Run after ``registry.py`` and ``readings.py`` (``run.py`` calls :func:`apply`): it reads ``results/numbers.json``,
puts each claim (validated by ``ft.numbers``: a key a claim rests on must be registered, a source must be a legal copy
read at its passage) and saves. The passages are the ones recorded at step a (``notes/sources.md`` and the notes it
names), quoted short or closely paraphrased, with the page; the isolated check reads them against the sources.
The forms (step w onward) tag the units that make each claim; a claim no form makes is dropped there, never kept.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

from ft import numbers  # noqa: E402


def src(source: str, locator: str, passage: str, copy: str = "open", read: str = "passage") -> dict:
    return {"source": source, "locator": locator, "passage": passage, "copy": copy, "read": read}


LUCAS = "Lucas, R. E. (1996), 'Nobel Lecture: Monetary Neutrality', Journal of Political Economy 104(4)"
TELES = "Teles, P. & Uhlig, H. (2010, rev. 2013), 'Is Quantity Theory Still Alive?', NBER Working Paper 16393"
BIS67 = ("Borio, C., Hofmann, B. & Zakrajsek, E. (2023), 'Does money growth help explain the recent inflation "
         "surge?', BIS Bulletin 67")
RW = ("Rolnick, A. J. & Weber, W. E. (1997), 'Money, Inflation, and Output under Fiat and Commodity Standards', "
      "Journal of Political Economy 105(6); FRB Minneapolis Quarterly Review 22(2) reprint")
BENATI = ("Benati, L., Lucas, R. E., Nicolini, J. P. & Weber, W. (2016), 'International Evidence on Long Run Money "
          "Demand', NBER Working Paper 22475")
MCLEAY = ("McLeay, M., Radia, A. & Thomas, R. (2014), 'Money creation in the modern economy', Bank of England "
          "Quarterly Bulletin 2014 Q1")
BN = ("Batini, N. & Nelson, E. (2002), 'The lag from monetary policy actions to inflation: Friedman revisited', "
      "Bank of England External MPC Unit Discussion Paper 6")
KRUGMAN = ("Krugman, P. (1998), 'It's Baaack: Japan's Slump and the Return of the Liquidity Trap', Brookings Papers "
           "on Economic Activity 1998(2)")
BB = "Blanchard, O. & Bernanke, B. (2023), 'What Caused the US Pandemic-Era Inflation?', NBER Working Paper 31417"
BARRO = ("Barro, R. J. & Bianchi, F. (2023, rev. 2025), 'Fiscal Influences on Inflation in OECD Countries, "
         "2020-2023', NBER Working Paper 31838")
SARGENT = ("Sargent, T. J. (1982), 'The Ends of Four Big Inflations', in R. E. Hall (ed.), Inflation: Causes and "
           "Effects, University of Chicago Press")
LEEPER = ("Leeper, E. M. & Leith, C. (2016), 'Understanding Inflation as a Joint Monetary-Fiscal Phenomenon', "
          "NBER Working Paper 21867")
BUITER = "Buiter, W. H. (2007), 'Seigniorage', NBER Working Paper 12919"
FED08 = "Board of Governors of the Federal Reserve System, press release of 6 October 2008"
FOMC79 = "Federal Reserve, FOMC Record of Policy Actions, meeting of 6 October 1979"
FOMC82 = "Federal Reserve, FOMC Record of Policy Actions, meeting of 5 October 1982"
GREENSPAN = ("Greenspan, A., testimony before the Subcommittee on Economic Growth and Credit Formation, House "
             "Committee on Banking, 20 July 1993")
BOJ01 = "Bank of Japan, 'New Procedures for Money Market Operations and Monetary Easing', 19 March 2001"
BOJ06 = "Bank of Japan, monetary policy decision of 9 March 2006"
BOJ13 = "Bank of Japan, 'Introduction of the Quantitative and Qualitative Monetary Easing', 4 April 2013"
BISQ15 = "BIS Quarterly Review, March 2015, overview 'A wave of further easing'"
BISQ11 = "BIS Quarterly Review, September 2011, 'Global growth and sovereign debt concerns drive markets'"
WGR = "Willard, Guinnane and Rosen (1995), 'Turning Points in the Civil War: Views from the Greenback Market', NBER WP 5381"
JW26 = "Judson and Weiss (2026), 'A Brief Illustrated History of the Federal Reserve's Balance Sheet', FEDS Notes, 13 February"
FOMC0315 = "Federal Reserve, FOMC statement of 15 March 2020"
FOMC0429 = "Federal Reserve, FOMC statement of 29 April 2020"
BOE11 = "Bank of England, Inflation Report, November 2011"
REGD = "Board of Governors of the Federal Reserve System, press release of 24 April 2020 (Regulation D)"

LONG_RUN = {"measure": "average inflation against average money growth, ten-year windows (slopes)",
            "period": "ten-year windows, 1950-2020", "population": "every money with the data at both ends of a "
            "window (IMF, World Bank, ECB, FRED), by coverage only"}


def claims() -> dict[str, dict]:
    C: dict[str, dict] = {}
    C["k1-money-and-prices"] = dict(
        text="Across countries and decades, faster money growth went with faster inflation: loosely in calm decades, "
             "steeply among fast printers.",
        type="established", component="K1", claim_type="descriptive",
        sources=[src(LUCAS, "p. 249 (Figure 1, p. 250)", "Thirty-year averages for 110 countries (McCandless & "
                     "Weber): the points lie roughly on the 45-degree line; the simple correlation between inflation "
                     "and money growth is .95 (M2), .96 (M1), .92 (M0).", read="full"),
                 src(BIS67, "p. 1, key takeaways; p. 3, Graph 2 and footnote 5", "The link between money growth and "
                     "inflation 'is one-to-one when inflation is high and virtually non-existent when it is low'; "
                     "the same result holds with the thresholds set on excess money growth rather than inflation.",
                     read="full"),
                 src(TELES, "abstract; p. 3", "For countries with low inflation, the raw relationship between average "
                     "inflation and money growth 'is tenuous at best'; below 12 percent inflation the points 'no "
                     "longer assemble nicely around a line'.", read="chapter"),
                 src(RW, "p. 14; p. 17", "Under fiat standards (14 countries, 15 periods) the slope through the grand "
                     "means of long averages is close to unity; the authors caution that the facts do not show "
                     "causality.", copy="held")])
    C["p2-1-steeper-with-pace"] = dict(
        text="Over 1950-2020, each point of base money growth went with about {{lr_base_mu_below}} of a point of "
             "inflation in decades below {{lr_line}} a year, and about {{lr_base_mu_above}} in decades above it; counted on "
             "broad money, the public's cash and deposits, with the line on its own growth, about "
             "{{lr_broad_mu_below}} below the line and {{lr_broad_mu_above}} above it.",
        type="measured", card="C28", component="K1", claim_type="comparative",
        keys=["lr_base_mu_below", "lr_base_mu_above", "lr_x_s6_above", "lr_x_edge30", "lr_base_mu_below_lo",
              "lr_base_mu_below_hi", "lr_broad_mu_below", "lr_broad_mu_below_lo", "lr_broad_mu_below_hi",
              "lr_broad_mu_above", "lr_broad_mu_below_n", "csb_base", "csb_broad", "lr_x_s1"], scope=LONG_RUN)
    C["p2-1-bands"] = dict(
        text="By band of money growth, the slope rose with the pace: {{lr_x_s1}} at or below {{lr_line}} a year, "
             "{{lr_x_s3}} between {{lr_x_edge20}} and {{lr_x_edge30}}, {{lr_x_s5}} above {{lr_x_edge50}} (an "
             "exploration).",
        type="measured", card="C29", component="K1", claim_type="exploration",
        keys=["lr_x_s1", "lr_x_s2", "lr_x_s3", "lr_x_s4", "lr_x_s5"], scope=LONG_RUN)
    C["p2-3-before-1950"] = dict(
        text="Before 1950, in {{lr_1870_economies}} rich economies, inflation went with the Macrohistory Database's narrow money about "
             "{{lr_1870_mu_below}} of a point per point below the line; the fast-money decades were the world "
             "wars'.",
        type="measured", card="C21", component="K1", claim_type="descriptive", keys=["lr_1870_mu_below"],
        scope={"measure": "average inflation against narrow money growth (base money, notes or M1 by country), "
                          "ten-year windows", "period": "ten-year windows, 1870-1950",
               "population": "18 rich economies of the Macrohistory Database"})
    C["k2-loose-in-calm-times"] = dict(
        text="In calm times the link is loose, because the demand for money moves: people hold more money when "
             "holding it costs little, and central banks supply what is demanded at their interest rate.",
        type="established", component="K2", claim_type="causal",
        sources=[src(BENATI, "section 2, pp. 7-9", "Long-run money demand: for low-inflation countries the data "
                     "often prefer velocity linear in the short rate (Selden-Latane); the demand for M1 moves with "
                     "the cost of holding it.", read="chapter"),
                 src(MCLEAY, "p. 25", "The Bank of England 'does not directly control the quantity of either base "
                     "or broad money'."),
                 src(GREENSPAN, "p. 10", "M2 'has been downgraded as a reliable indicator of financial conditions'; "
                     "the relationships between money and income, and money and prices, 'have largely broken down'.",
                     read="full")])
    C["k2-cases-us-targets"] = dict(
        text="The Federal Reserve targeted the money stock from October 1979, de-emphasised M1 in October 1982, and "
             "downgraded M2 in July 1993.",
        type="cases", component="K2", claim_type="descriptive",
        sources=[src(FOMC79, "PDF p. 5", "A shift in open market operations to 'supplying the volume of bank reserves "
                     "estimated to be consistent with the desired rates of growth in monetary aggregates'."),
                 src(FOMC82, "p. 12", "'much less than usual weight be placed on movements in' M1 during the "
                     "quarter."),
                 src(GREENSPAN, "p. 10", "'At least for the time being, M2 has been downgraded as a reliable "
                     "indicator'.", read="full")])
    C["p2-2-base-against-broad"] = dict(
        text="In {{csb_moneys}} economies' decades with both money growths at or below {{lr_line}} a year, mostly since "
             "1990, each point of central-bank money growth went with {{csb_base}} of a point of inflation, each "
             "point of the public's money with {{csb_broad}}.",
        type="measured", card="C30", component="K2", claim_type="comparative",
        keys=["cs_b_gap", "csb_base", "csb_broad", "csb_moneys", "csb_windows", "cs_b_gap_era_to_2000",
              "cs_b_gap_era_from_2008", "csb_to2000_gap_lo", "csb_to2000_gap_hi", "csb_from2008_gap_lo",
              "csb_from2008_gap_hi"],
        scope={"measure": "inflation per point of money growth, broad slope less base slope (OLS, clustered by "
                          "money and currency union)", "period": "ten-year windows ending 1970 to 2020",
               "population": "decade windows with base and broad money growth both at or below 12% a year"})
    C["p2-6-reserves"] = dict(
        text="Banks cannot lend reserves to households and firms; since October 2008 reserves in the United States "
             "earn interest, which makes them close to bills.",
        type="established", component="K3", claim_type="causal",
        sources=[src(MCLEAY, "pp. 14, 16, 24-25", "QE buys mainly from non-bank financial companies, creating "
                     "deposits for them; reserves are lent only between banks; newly created reserves 'do not, by "
                     "themselves, meaningfully change the incentives for the banks to create new broad money'."),
                 src(FED08, "the release", "The Board 'will begin to pay interest on depository institutions' "
                     "required and excess reserve balances', effective 9 October 2008.", read="full")])
    # the grid check of 2026-10-08 (J): K3 shown beyond one country, from the harvest of 2026-10-07 (sections 6-15)
    C["k3-other-printings"] = dict(
        text="The Bank of Japan targeted banks' reserves with it from March 2001 to March 2006, until consumer "
             "prices excluding fresh food stopped falling, which it judged done in March 2006, and in April 2013 set out to double the monetary base, from {{boj_base_2012}} "
             "to an expected {{boj_base_2014}}; defending its floor against the euro, the Swiss National Bank took "
             "its assets to {{snb_assets_gdp}} of GDP; British inflation reached {{uk_cpi_2011_09}} in September "
             "2011, put down by the Bank of England to VAT, energy and import prices, after it had bought "
             "{{boe_apf_held_2011}} of assets with new reserves; in October it raised the total to {{boe_apf_2011}}.",
        type="established", component="K3", claim_type="descriptive",
        keys=["boj_base_2012", "boj_base_2014", "snb_assets_gdp", "uk_cpi_2011_09", "boe_apf_held_2011",
              "boe_apf_2011"],
        sources=[src(BOJ01, "the release, a and b", "The operating target changed to 'the outstanding balance of the "
                     "current accounts at the Bank of Japan', in place 'until the consumer price index ... registers "
                     "stably a zero percent or an increase year on year'.", read="full"),
                 src(BOJ06, "the release", "The operating target changed back 'to the uncollateralized overnight "
                     "call rate'.", read="full"),
                 src(BOJ13, "p. 1 and footnote 1", "'It will double the monetary base ... in two years'; the base "
                     "'was 138 trillion yen at end-2012' and 'is expected to reach ... 270 trillion yen at "
                     "end-2014'.", read="full"),
                 src(BISQ15, "the paragraph on Swiss tensions", "The defence of the floor 'had caused the SNB's total "
                     "assets to surge to 87% of GDP in December'; 'on 15 January ... the SNB discontinued the cap'.",
                     read="chapter"),
                 src(BISQ11, "p. 13", "Quoting the SNB on 6 September 2011: 'With immediate effect, it will no longer "
                     "tolerate a EUR/CHF exchange rate below the minimum rate of CHF 1.20.'", read="chapter"),
                 src(BOE11, "p. 33, section 4.1", "'CPI inflation rose to 5.2% in September ... the elevated rate of "
                     "inflation reflects the temporary impact of increases in VAT, energy prices and import "
                     "prices.'; p. 5: 'the MPC increased the size of its asset purchase programme by £75 billion, to a "
                     "total of £275 billion'; p. 10: in September 'Eight members voted to keep the stock of asset "
                     "purchases at £200 billion'; in October, a further £75 billion 'by the issuance of central bank "
                     "reserves'.", read="chapter"),
                 src(BOJ06 + " (read 2026-10-08)", "the release", "'Concerning prices, year-on-year changes in the "
                     "consumer price index turned positive.'", read="full")])
    C["p2-4-two-printings"] = dict(
        text="The United States added about {{csc_w1_base_tn}} of base money over {{csc_w1_months}} months from 2008 "
             "and {{csc_w2_base_tn}} over {{csc_w2_months}} months from 2020; about {{csc_w1_reserves_share}} and "
             "{{csc_w2_reserves_share}} of it ended as bank reserves.",
        type="measured", card="C32", component="K3", claim_type="descriptive",
        keys=["csc_w1_base_tn", "csc_w2_base_tn", "csc_w1_months", "csc_w2_months", "csc_w1_reserves_share",
              "csc_w2_reserves_share"],
        scope={"measure": "change in base money and in reserves (H.4.1, monthly averages)",
               "period": "August 2008 to October 2014; February 2020 to December 2021",
               "population": "the United States, the Federal Reserve's balance sheet"})
    C["p2-4-purchases-and-deficits"] = dict(
        text="The Fed's Treasury purchases equalled about {{csc_w1_purchases_share}} of the federal deficits of "
             "fiscal years 2009-14 and {{csc_w2_purchases_share}} of those of 2020-21.",
        type="measured", card="C32", component="K5", claim_type="descriptive",
        keys=["csc_w1_purchases_share", "csc_w2_purchases_share"],
        scope={"measure": "the Fed's Treasury holdings added over the whole fiscal years' federal deficits",
               "period": "FY2009-14; FY2020-21", "population": "the United States"})
    C["k4-capacity-and-lag"] = dict(
        text="The same money meets different prices when output can rise than when it cannot, and an expansion "
             "read as temporary is held, not spent; in moderate inflations, monetary policy's peak effect on prices "
             "has come more than a year later.",
        type="established", component="K4", claim_type="causal",
        sources=[src(BN, "p. 1; p. 2; p. 7", "It takes over a year before monetary policy actions have their peak "
                     "effect on inflation (UK and US, 1953-2001), a rule of thumb for countries that have had "
                     "moderate inflation; the authors take no stand on whether money has a special role.",
                     read="full"),
                 src(KRUGMAN, "pp. 139, 160-161", "'only temporary monetary expansions are ineffectual'; a monetary "
                     "expansion perceived to be permanent will raise prices or output.")])
    C["p2-10-two-economies"] = dict(
        text="2008-14 and 2021 met different economies: unemployment stood above {{csc_unrate_line}} from "
             "{{csc_unrate_above8_from}} "
             "to {{csc_unrate_above8_to}}, peaking at {{csc_unrate_2009_10}}, while in 2021 it fell from "
             "{{csc_unrate_2021_01}} to {{csc_unrate_2021_12}}.",
        type="measured", card="C32", component="K4", claim_type="descriptive",
        keys=["csc_unrate_above8_from", "csc_unrate_above8_to", "csc_unrate_2009_10", "csc_unrate_2021_01",
              "csc_unrate_2021_12"],
        scope={"measure": "unemployment rate (FRED UNRATE, frozen 2026-10-08)", "period": "2008-2014 and 2021",
               "population": "the United States"})
    C["p2-4-largest-modern"] = dict(
        text="In the Fed's monthly series of central-bank money, which starts in {{csc_base_first_month}}, the stock "
             "had grown at most about {{csc_pre2008_max_growth_74m}} over any {{csc_w1_months}} months, or "
             "{{csc_pre2008_max_growth_22m}} over any {{csc_w2_months}}, before 2008; it grew "
             "{{csc_w1_base_growth}} over the first printing and {{csc_w2_base_growth}} over the second.",
        type="measured", card="C32", component="K4", claim_type="descriptive",
        keys=["csc_base_first_month", "csc_pre2008_max_growth_74m", "csc_pre2008_max_growth_22m",
              "csc_w1_base_growth", "csc_w2_base_growth", "csc_w1_months", "csc_w2_months"],
        scope={"measure": "growth of the monetary base (FRED BOGMBASE, vintage 2026-09-30)",
               "period": "1959 to 2021", "population": "the United States"})
    C["p2-4-earlier-printings"] = dict(
        text="Earlier American printings: the Union's greenbacks from 1862, legal tender not convertible into gold; "
             "the Fed's purchases of Treasury securities in the Second World War, its balance sheet peaking at about "
             "{{fed_bs_ww2_gdp}} of GDP, gold its largest asset, against just over {{fed_bs_2014_gdp}} in 2014.",
        type="established", component="K4", claim_type="descriptive",
        keys=["fed_bs_ww2_gdp", "fed_bs_2014_gdp"],
        sources=[src(WGR, "abstract", "'In early 1862, the United States government began issuing Greenbacks, a "
                     "legal tender currency that was not convertible into gold'; the chance of redemption depended "
                     "on the war's expected cost.", read="passage"),
                 src(JW26, "section 4", "The balance sheet 'expanded dramatically during the Great Depression and "
                     "through World War II ... peaking at about 22 percent of GDP'; at the onset of the war 'Treasury "
                     "purchases expanded as a means to support wartime investment', though 'gold certificates remained the "
                     "dominant asset component'."),
                 src(JW26, "section 7", "'The balance sheet size peaked at just over 25 percent of GDP in 2014'.")])
    C["p2-10-shutdowns"] = dict(
        text="In April 2020 unemployment reached {{csc_unrate_2020_04}}, the job losses of the virus and the measures "
             "taken against it; the Fed's purchases, announced in March 2020, answered that shock.",
        type="established", component="K4", claim_type="descriptive",
        keys=["csc_unrate_2020_04"],
        sources=[src(FOMC0429, "the statement, first paragraph", "'The virus and the measures taken to protect public "
                     "health are inducing sharp declines in economic activity and a surge in job losses.'",
                     read="full"),
                 src(FOMC0315, "the statement", "Citing the coronavirus outbreak's disruption, 'the Committee will "
                     "increase its holdings of Treasury securities by at least $500 billion and its holdings of agency "
                     "mortgage-backed securities by at least $200 billion'.", read="full")])
    C["p2-4-money-held-2020"] = dict(
        text="From February to May 2020 the public's money rose by about {{csc_m2_feb_may_2020_tn}} while its "
             "velocity fell from {{csc_m2v_2020q1}} to {{csc_m2v_2020q2}}; in 2021 it grew {{csc_m2_growth_2021}} "
             "with velocity flat and nominal spending up {{csc_ngdp_growth_2021}}.",
        type="measured", card="C32", component="K2", claim_type="descriptive",
        keys=["csc_m2_feb_may_2020_tn", "csc_m2v_2020q1", "csc_m2v_2020q2", "csc_m2_growth_2021",
              "csc_ngdp_growth_2021"],
        scope={"measure": "M2, its velocity (FRED M2V) and nominal GDP", "period": "2020-2021",
               "population": "the United States"})
    C["p2-5-cross-section"] = dict(
        text="Across {{cse_n}} economies that started calm, faster broad-money growth in 2020-21 went "
             "with more inflation in 2022-23: about {{cs_e_broad_huber}} of a point per point (robust slope).",
        type="measured", card="C31", component="K5", claim_type="comparative",
        keys=["cs_e_broad_huber", "cse_n", "cs_e_broad_huber_no_control", "cse_loo_moves", "cse_loo_lo_min",
              "cse_nocontrol_n", "cse_control_missing", "cs_e_var_momentum", "cse_var_momentum_lo",
              "cse_var_momentum_hi", "cs_e_var_led", "cse_var_led_lo", "cse_var_led_hi"],
        scope={"measure": "inflation per point of broad money growth (Huber robust slope, energy-import share "
                          "controlled)", "period": "broad money December 2019 to December 2021; inflation "
                          "December 2021 to December 2023",
               "population": "economies whose 2015-19 inflation averaged below 10% a year"})
    C["k5-2021-23"] = dict(
        text="In 2021-23, strong demand, fed by transfers the central banks' purchases helped finance, met supply "
             "and energy shocks; how much the money itself added, scholars weigh differently.",
        type="established", component="K5", claim_type="descriptive",
        sources=[src(BB, "p. 39; abstract", "The inflation 'largely reflected strong aggregate demand, the product "
                     "of easy fiscal and monetary policies, excess savings accumulated during the pandemic, and the "
                     "reopening'; most of the surge came as shocks to prices given wages.", read="full"),
                 src(BIS67, "p. 1; p. 4, Graph 3; p. 5", "Countries with stronger money growth saw markedly higher "
                     "inflation (beta 0.29 on 30 economies); the findings 'say little about causality', and money "
                     "may capture the income effect of the fiscal transfer.", read="full"),
                 src(BARRO, "abstract; p. 21", "About 80% of effective government financing came from the effect "
                     "of unexpected inflation on the real value of public debt.", read="chapter")])
    C["k5-our-weighing"] = dict(
        text="That the money added to the 2021-23 inflation, beyond the fiscal demand that carried it, is our "
             "judgement: our cross-section cannot separate the two.",
        type="judgement", component="K5", claim_type="judgement")
    C["p2-7-big-inflations"] = dict(
        text="In the four big inflations Sargent read, prices stopped when the deficit financing stopped, while the "
             "note circulation kept growing.",
        type="established", component="K6", claim_type="causal",
        sources=[src(SARGENT, "pp. 42, 89-90", "Persistently large deficits financed by creating money impart the "
                     "momentum; in each case 'the note circulation continued to grow rapidly after the exchange "
                     "rate and price level had been stabilized'.", read="full"),
                 src(LEEPER, "p. 87", "'Economists generally agree that historical episodes of high and volatile "
                     "inflation rates inevitably have fiscal roots.'")])
    C["p2-8-what-inflation-took"] = dict(
        text="From March 2020, inflation took about {{csf_hh_lower}} to {{csf_hh_upper}} from the average US "
             "household's cash and checking deposits.",
        type="measured", card="C33", component="K7", claim_type="descriptive",
        keys=["csf_hh_lower", "csf_hh_upper", "csf_R_bn"],
        scope={"measure": "the loss of purchasing power on cash and on deposits that paid nothing, the "
                          "reclassified savings read against other deposits' own path",
               "period": "March 2020 to August 2026", "population": "US households (the average household)"})
    C["k7-who-gains"] = dict(
        text="On cash the gain is the state's (the inflation tax on base money); on deposits that paid nothing the "
             "loss went to those owing at fixed rates below inflation, the state among them, and to banks "
             "through their spread.",
        type="established", component="K7", claim_type="causal",
        sources=[src(BUITER, "p. 4", "'The inflation tax is the reduction in the real value of the stock of base "
                     "money caused by inflation.'", read="chapter"),
                 src(REGD, "the release", "The six-per-month limit on convenient transfers from savings deposits "
                     "deleted, so savings could be classed with checkable deposits.", read="full")])
    C["what-to-watch"] = dict(
        text="What to watch is not the size of the central bank's balance sheet but the money the public holds "
             "against its spending, whether the purchases pay for transfers or only swap bonds for reserves, and "
             "whether the economy can produce more.",
        type="judgement", component="answer", claim_type="judgement")
    C["headline"] = dict(
        text="Printing money raises prices when the new money reaches people who spend it rather than hold it, in "
             "an economy that cannot simply produce more, and when it is expected to last.",
        type="judgement", component="answer", claim_type="judgement", headline=True)
    return C


def apply(path: Path | None = None) -> None:
    reg = numbers.Registry.load(path or K.STUDY / "results" / "numbers.json")
    reg.claims.clear()
    for cid, c in claims().items():
        reg.put_claim(cid, **c)
    reg.save()


if __name__ == "__main__":
    apply()
