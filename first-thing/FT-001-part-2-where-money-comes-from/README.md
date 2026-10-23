# Where money comes from — methods and proof

*A First Thing Weekly Study · FT-001, part 2 of "The life of a money" · as of 2026-10-11*

This folder is the proof behind the study published on First Thing's site, for the sceptic and the specialist: what
each claim rests on, what was fixed before each result, what ran, what each result means and what it does not, where
the data come from, and the code. It is not the study: the study, with its argument, its charts and its balance-sheet
explorer, is on the site.

Reproduction level: read the code

The code is published here and every number names the script that computed it or the source and page it is cited
from. The code calls a small shared toolkit of ours (the register of numbers, the cards, the charts, the data readers)
that is not in this repository, and the fetched series are not republished: each manifest under `data/` says where a
series was fetched, when, and its hash. So the code can be read and every source traced; it cannot be rerun from this
folder alone.

## What each claim rests on

The study answers its question, where money and value come from and how they differ, in eleven components: what money
is today, who creates it, money in a bank account, what central banks do, where money first came from, real value,
valuations and whether they reach the shops, what inflation is, hyperinflation, who gains and who pays, and what to
watch. Every claim it makes is in the register (`results/numbers.json`, its `claims`), with its type, the component it
serves, and either the passages it rests on (each with its page, table or section, the copy read, and how deeply the
work was read) or the card of the analysis that measured it. Four types are used: **established** (a documented fact
or mechanism, cited at its passage), **cases** (shown in history, with their sources), **measured** (an analysis of
ours, with its card) and **judgement** (our reading, said as ours).

The headline is a judgement whose parts are each established or measured. "Most money is a bank's promise, created
when someone borrows and destroyed when they repay" rests on the central banks' own account (McLeay, Radia and Thomas
2014, pp. 14–18, pp. 24–25); "notes and coin are a minority of it" is measured (CS-A); "value is made by producing what
people want" rests on Smith and the national accounts' definition; "over the long run and across
countries, faster money growth has gone with faster inflation, and with faster real growth only weakly or not at all" rests on the cross-country
findings of Lucas (1996) and McCandless and Weber (1995), the OECD exception printed with it; "a share that doubles creates no money" is our application of the balance sheets above, never a
result of CS-E; "inflation has several origins" is a judgement on
the established sources and cases of the inflation section, CS-C supporting only "went with".

Seven analyses of ours are case studies inside the study, each beside the component it supports; none carries the
answer alone.

## The readings, and the size that matters

Each measured claim is read against the size that matters, fixed on its card.

- CS-A, CS-E and CS-F are descriptions, and CS-G an illustration: each figure is printed as it is, read against no
  size, with no null. CS-A's card fixed what would refute "most money is a bank's promise" before any value: currency
  at half or more of broad money in an economy's latest month.
- CS-B: the gap between the slope of inflation on broad money growth and the slope on base money growth, in calm
  decades, 0.27 (0.14 to 0.40), against a size that matters of a tenth of a point: an
  **effect**.
- CS-C: the slope of inflation on base money growth in windows above the line, 1.07
  (1.01 to 1.12), and below it, 0.25
  (0.14 to 0.36), each against a tenth of a point: both **effects**, the first about
  one for one. The explorations `S7` and `S8` of `C29`: 0.66 and 0.70 above the line, both effects.
- CS-D: the robust slope of 2022–2023 inflation on 2020–2021 broad money growth, 0.27
  (0.10 to 0.48), against a tenth of a point: an **effect**, its lower end just
  above the size that matters. With 2021's inflation as a control (`C31`'s variant c), 0.10
  (-0.05 to 0.33): **bounded**, ruling out a slope above
  0.33. Without the energy-import control, beside as the card fixes, 0.22
  (0.08 to 0.38) across 112 economies, which the card's own rule
  reads as bounded since its lower end is below the size that matters. Dropping any one of 10 of the
  71 economies or unions alone turns the main reading to bounded. Of the other variants fixed on the card
  (a, b, d, e, f, g), 5 of 6 have their interval's lower end below the size that
  matters, so the card's rule reads them bounded; f (annual-average inflation) reads an effect. Each variant's slope and
  interval is in the run file. The main reading is therefore fragile, and the text says so beside it.
- K11's count (`C41`, `C39` rerun on C28's corrected run): a description, each count printed with its denominator, read against no size, with no null; an
  exploration on `C29`'s cuts.

The cards `C28`, `C29`, `C30` and `C31` were made for the earlier design of this study and are reused because a rerun
would produce the same: their question, data and code still serve the answer. Their results were known when this
study's plan chose them: each card's `seen` field lists what had been
seen when it was written (`C30`'s design was motivated by `C28`'s slopes; `C31`'s by checks on earlier
cross-sections), and the reading of each is ours on results already known.

## The levels in plain words (what to watch)

The section on what to watch reads past episodes for the levels that mattered (`k11-levels`), in plain words; the
figures behind each word are these. "Nearly tripled": US base money multiplied by 2.77 from November
2008 to October 2014 (frozen BOGMBASE). "Faster than about twelve per cent a year": CS-C's line, 12%;
"about one point" and "about a quarter of a point": CS-C's slopes above and below it, 1.07 and
0.25. "About a quarter of a point" after the pandemic: CS-D's robust slope, 0.27;
"perhaps none": with 2021's inflation as a control, 0.10, with an upper limit of 0.33.
Argentina's "about thirteen per cent" and "about four per cent": monthly inflation of 12.8% in November
2023 and 4.2% in May 2024 (INDEC); December 2023 and January 2024 were higher still, at
25.5% in December. "About three per cent of GDP a year": Mian and Sufi's
2.8%, 2002–2006. The readings are associations in the episodes told; none is a threshold we fix or a
forecast.

The count in the same reading (`k11-base-rate`; card `C41`, `C39` rerun after the correction below, `code/p2_k11_base.py`) takes CS-C's ten-year windows on base money as stored, 635 windows in 155 economies (C28's grid, with its units guard; the 45 windows whose consumer prices were filled from Ha, Kose and Ohnsorge's database are in the count), and sorts them by base money growth in log points a year, on C29's cuts: at or below 12, above 12 to 20, above 20 to 30, and above 30 (the bands above 30 and above 50 merged, since the band above 50 held fewer than 20 windows, by a rule fixed before any window was counted). As yearly percentages the edges are 13%, 22% and 35%: the table's first edge, about 13% a year, is 12 log points, the line that CS-C's text calls about twelve per cent. A window counts when its inflation averaged 20% a year or more over the decade as a compound yearly rate (inflation is in log points, like money growth, and compared with the log of its line): Reinhart and Rogoff's (2009) yearly crisis line applied to a decade's average, an adaptation of ours. A decade under it can hold years above it, and one or two very high years can lift a decade over it. The shares, with ninety-five per cent intervals from a bootstrap that redraws whole economies, since an economy's decades are not independent: 3.4% (1.1% to 6.0%), 21.8% (13.5% to 31.0%) and 84.4% (71.4% to 93.8%); for the slowest band, with no such window, a one-sided ninety-five per cent bound across its 131 economies: at most 2.3%. At a 10% line the counts are 16 of 309, 70 of 203, 59 of 78 and 42 of 45; across all windows, 62 of 635 at 20% and 187 at 10%. The empty slowest band is close to what arithmetic implies: with money growing no faster than the line, inflation averaging 20% a year would need the speed at which money changes hands, less real growth, to add at least about six log points a year for a decade. The bands are cuts seen in C29 before this count, so the card is an exploration. Money and prices are of the same decade, so the count describes: it predicts nothing and says nothing of which came first. Left out by C02's rules, never by outcome: the six moneys whose units break, Venezuela and Zimbabwe among them; money-years using the euro outside the euro area; a euro member's windows once it uses the euro, the euro area counting as one money from 1999; and windows without real GDP at both ends. A hole in the data, not a rule: of the twenty-one euro members of 2026, only Estonia (2000 to 2010) and Bulgaria (2000 to 2020) have windows of their own before the euro; Slovakia's units break, and the others have no base money here before the euro, or too few years of it for a window. The moneys whose units break include some of the fastest inflations, so the shares in the fastest bands may be understated.

## CS-A

**Notes and coin as a share of the money people hold** (card `C35`, `code/p2_cs_a.py`). For each economy, the notes and
coin held by the public divided by its broad money, every month since each series begins: the United States, the Federal Reserve Board's
currency over M2 (H.6; FRED's `CURRSL` over `M2SL`, from 1959); the euro area, the ECB's currency in circulation over M3 (BSI series, from 1980);
Britain, the Bank of England's notes and coin in circulation (`LPMAVAB`) over M4 (`LPMAUYN`, from 1982).
In the US and the euro area the held side only: currency in banks' vaults is not the public's (a departure from the
map's first wording, said on the card). Britain's numerator includes the notes and coin banks hold, which raises its
share, and M4 includes intermediate financial companies' deposits, which lowers it; the series that would remove
either (M4ex and M4's own notes-and-coin component) were not identified on the Bank's database. US currency includes notes held abroad, which only makes the domestic share smaller than it looks.

| Economy | Latest | Lowest | Highest |
|---|---|---|---|
| United States (M2) | 10.2% | 6.6% | 11.3% |
| Euro area (M3) | 9.2% | 4.3% | 9.6% |
| Britain (M4) | 3.2% | 2.5% | 8.1% |

Outside check: the IMF's currency outside banking institutions over money plus quasi-money, for every economy in its
statistics with both lines, each at its own latest month: 163 economies, a median of 11.1%,
half or more in 2 (Guinea-Bissau, 65.6%; Iraq, 50.9%). The same at the year
most economies' series end (89 economies): a median of 10.1%, half or more in
1. Britain on the IMF's lines reads 2.0%, the IMF's aggregates not being the Bank of
England's. Euro members are read as the euro area, never twice.

## CS-B

**Base against broad money in calm decades** (card `C30`, reused, `code/cs_b.py`). On C28's ten-year windows where
money grew calmly (its rule on money growth only, never on inflation), the slope of inflation on base money growth,
0.12, against the slope on broad money growth, 0.39, across 243 calm windows
in 113 economies, clustered by monetary union. Attenuation: noise in base money growth would close the gap only
if 0.31 or less of its variance were signal. The study cites it for its gap only; it is never read as
an illustration of interest on reserves nor of the US after 2008.

In plain words: the gap was 0.27, across 243 calm decades in 113 economies. Could errors in measuring base money explain the whole gap? Only if they were very large: at most 0.31 of the ups and downs in measured base money growth could then be real changes, and the rest would be error. The case study on money growth and inflation by pace (CS-C) calls a decade slow when base money alone grew at the line or less, so calm decades are fewer than slow ones. The comparison here also allows for real growth. For both reasons, the figure for base money here differs from the slow decades' figure in CS-C.

## CS-C

**Money growth and inflation by pace** (cards `C28` and `C29`, reused, `code/units_guard.py`). Every economy's ten-year
windows of average money growth and average inflation, 1950–2020, from the IMF's, the World Bank's, FRED's and the
ECB's series, with C28's guard against changes of unit; split at Teles and Uhlig's line of 12%, theirs drawn
on average inflation, adapted here to money growth and named so. Base money is the lead (635 windows in
155 economies; 326 above the line, 309 below); broad
money is beside, its slope above the line 1.04 and below 0.61. The line C28 also
reports on inflation, a split on the outcome, is never read. The public figures are drawn without the windows whose
consumer prices were filled from Ha, Kose and Ohnsorge's database. Measurement error in money growth flattens the slow
side: in our reading, part of the gap, not all of it. The fast side's figure rests mostly on the fastest decades, most
of them between 1970 and 2000. In the fast decades outside 1970–2000, each point of base money growth went with
0.70 of a point of inflation.

In plain words: for every economy, we take its average money growth and its average inflation over each decade, from the IMF's, the World Bank's, FRED's and the ECB's series. We sort the decades into fast and slow at 12% a year of base money growth. Where base money grew faster than that, each extra point of money growth went with 1.07 of a point of inflation. Where base money grew slower, each point went with 0.25 of a point. On the slow side, though, each point of broad money growth went with more inflation than each point of base money growth.

## CS-D

**The pandemic cross-section** (card `C31`, reused, `code/cs_e.py`). Every economy in the IMF's statistics whose
inflation was calm in 2015–2019 (a line adapted from De Grauwe and Polan), its broad money growth from December 2019 to
December 2021 against its inflation from December 2021 to December 2023; euro members enter as the euro area, the
other monetary unions' members one by one, clustered by union and dropped together; energy imports in 2019 as the control; a Huber slope with a cluster bootstrap fixed before the
run (in plain words: the comparison allows for how much energy each economy imports, and uses a method that a few
extreme economies cannot distort); variants a to g and every single drop, as the card fixes. Variant h, base money in place of broad money, is described and never a claim: its slope is 0.02 (-0.02 to 0.10, 75 economies, the euro area left out), which rules out a slope on base money above about 0.10; broad money's correlation with inflation exceeds base money's by 0.26. Base money growth has a standard deviation of 13.3 points a year, and 64% of its variance comes from five economies (Sweden, New Zealand, Norway, Denmark and Mongolia); C15, the base-money episodes card, flags a one-month jump in Denmark's base money in March 2021 as a likely reclassification, unread. The main slope's committed null simulation gives a false-confirmation
rate of 0.001. The cross-section does not separate the money from the fiscal demand that carried it, as the BIS says of
its own estimate.

In plain words: we ran the comparison 71 times, each time leaving out one economy, or one monetary union as a whole. In every run the link stayed between 0.24 and 0.32, and the low end of its margin of error stayed above zero (0.087 at the lowest). But in 10 of these runs, that low end fell just below a tenth of a point, the smallest link we count as large enough to matter. Most other versions of the comparison, all chosen before we saw the results, also put that low end below a tenth of a point.

## CS-E

**Where US households' real wealth came from** (card `C36`, `code/p2_cs_e.py`). The Fed's table of the change in
households' and nonprofits' net worth (Z.1, `S1M.r`), read quarter by quarter, from the first quarter of 1952 to the
last of 2025. Each holding-gains
series is placed in one of three groups fixed on the card before any value (real assets and market-priced claims; fund
and pension claims; debt securities, currency and deposits); each series' real holding gain is its revaluation less the
quarter's consumer-price inflation times its level at the start of the quarter. Other nominal assets (net worth less
the partition's levels plus liabilities) lose the quarter's inflation; liabilities gain it; net investment and other
volume changes are the Fed's lines as published, never called saving. The parts sum to the real change in net worth,
to the release's rounding (the tolerance, a quarter's rounding of three lines published in whole millions, is said in
the code). Everything is put in December 2025 dollars. Inflation's gain on what households owe, set against the real loss on debt securities, currency, deposits and other assets fixed in dollars together, is 82% (`cs-e_1952-2025_liabilities_over_fixed`); fund and pension claims are left out of that comparison, since their values move partly with markets (their real holding gains were positive in 1990–99 and 2010–19).

| Part, 1952–2025 | Trillions of December 2025 dollars |
|---|---|
| Real holding gains, real assets and market-priced claims | $79.9 trillion |
| Real holding gains, fund and pension claims | $-15.8 trillion |
| Real holding gains, debt securities, currency and deposits | $-23.2 trillion |
| Net investment | $98.2 trillion |
| Inflation's erosion of other nominal assets | $-5.2 trillion |
| Inflation's gain on liabilities | $23.4 trillion |
| Other volume changes | $9.3 trillion |
| Real change in net worth | $166.5 trillion |

The decades are in `results/runs/C36-cs-e-household-real-wealth.json`. Outside check: the euro area's households in the
ECB's quarterly sector accounts, equity and investment-fund shares in real terms, 2013 to 2025, against the
corresponding US lines; for instance equity in 2022, -9.3% in the euro area and
-18.4% in the US. No line is drawn and no part is called the main one.

## CS-F

**Money, real output and prices in the US since 1959** (card `C37`, `code/p2_cs_f.py`). The identity of the Board's M2 (FRED's `M2SL`),
`GDPC1` and `GDPDEF`, fourth quarter to fourth quarter, velocity the residual, checked against nominal GDP (`GDP`) in
every quarter, as average growth in logs: from 1959 to 2025 money 6.5% a year, real output 3.0%,
prices 3.2%, velocity -0.3%. The decades are in the run. An identity
attributes nothing. Britain's long series was dropped on the card, its columns not identified within the run.

## CS-G

**Money growth and real growth across decades** (card `C38`, `code/p2_cs_g.py`). Lucas's second figure redrawn on C28's
stored ten-year windows of broad money growth and real GDP growth: 580 windows from 152
economies, 274 of them calm (money growing 12% a year or less), 45 filled windows left
out. This calm set is wider than the calm decades of the case studies on inflation, where base money and broad money
must both grow at that rate or less. No regression line, no slope, no correlation is computed or printed: an
illustration; the finding is Lucas's and McCandless and Weber's.

In plain words: in 274 of these decades, broad money grew 12% a year or less, and we do not draw a trend through the points.

## The numbers read from frozen series

The study prints numbers computed in `code/p2_registry.py` from frozen series, each US one (except M2V and the deficit as a share of GDP, still FRED's) from its original agency over the dates of the FRED copy the study first read (FRED's copy kept beside it; the author, 2026-10-21), with no choice a result could
tune. The US base (`BOGMBASE`) over windows dated by the Fed's own statements: from November 2008, the month before the
purchases announced late that month began, to October 2014, when the FOMC ended them, 2.77 times;
from February 2020 to March 2022, the end of net purchases the FOMC set in January 2022, 1.78 times;
from August to November 2008, through emergency lending, 1.70 times; and, said because both windows
were seen, from September 2019, before the bill purchases the Fed said were not quantitative easing,
1.92 times to March 2022. US M2 (`M2SL`) from December 2021 to December 2022, -1.0%, its
first fall over twelve months since the series began (the code refuses to run if that is no longer so). Banks' loans
and leases (`TOTLL`, weekly, averaged by month) over the same months, 12%; banks' total credit (`TOTBKCR`, weekly, averaged by month), 7%, their securities (`INVEST`, monthly) having fallen. The study reads no split of the flows that drained deposits that year, and sizes none. Output per hour in nonfarm
business (`OPHNFB`), latest quarter over the first of 1947, 5.4 times.

For the watch list, where the United States stood in the latest frozen data, each read as published, no forecast and
no threshold: M2 (`M2SL`) and consumer prices (`CPIAUCSL`, CPI-U) over the twelve months to their latest month,
5.7% and 3.4%; banks' loans and leases (`TOTLL`, weekly averaged by month) over the twelve months to
their latest month, 7.7%; nominal GDP (`GDP`) over the four quarters to the latest, 6.3%; the effective
federal funds rate (`FEDFUNDS`) in its latest month, 3.63%; the federal deficit (`FYFSGDA188S`, the surplus's
sign reversed) in the latest fiscal year, 5.8% of GDP; the Fed's Treasury holdings (`TREAST`, weekly) over
the latest year, 8.5%. The latest months differ by series (the register gives each period), which
the text says.

## The balance-sheet explorer

The explorer draws the study's balance sheets on round example amounts (a loan, a share whose price doubles): the
accounting of McLeay, Radia and Thomas (2014), pp. 14–18, pp. 24–25, for the loan, its repayment, the cash withdrawal
and the central bank's purchases; the state's spending and the share's two steps apply the same accounting. It shows no
data. Its steps are in `code/p2_figures.py`.

## Details behind the text

The study's text keeps what carries each section's point. These details, which it once held, are kept here, each with
its claims and sources.

**The floor under the market rate.** After the Fed began paying interest on reserves in October 2008, the market rate
traded below the rate paid on reserves. Part of the reason is that some lenders are not banks, and by law cannot earn
the rate on reserves. Fannie Mae and Freddie Mac, enterprises sponsored by the US government, are two of them. From
September 2013 the Fed began testing overnight reverse repos. A reverse repo is a loan to the Fed that is repaid the
next day, and these lenders could make such loans too. Reverse repos set a soft floor under market rates: a lower
limit, but not a strict one (Ihrig, Meade and Weinbach 2015, a FEDS working paper, p. 10 and pp. 13–15) [FOMC 2013](https://www.federalreserve.gov/monetarypolicy/fomcminutes20130918.htm) (minutes of September 2013, the reverse repo authorization).

**The Fed's purchases, the other windows.** Even before the purchases began, emergency lending had multiplied US base
money by 1.70 from August to November 2008; the factor of 2.77 from November 2008
to October 2014 came on top of that first rise. Over the same years, November 2008 to October 2014, M2 was multiplied by
1.44. In the pandemic, from February 2020 to the end of net purchases in March 2022, base money was
multiplied by 1.78, and M2 by 1.41 [FOMC 2022](https://www.federalreserve.gov/newsevents/pressreleases/monetary20220126a.htm) (statement, January 2022).

**Japan's targets.** In March 2001 the Bank of Japan began targeting the balances that banks hold with it, at about
5 trillion yen. It set the target higher in steps, to between 30 and
35 trillion yen by January 2004, and kept it in that range until consumer prices stopped falling. In
March 2006 the Bank of Japan returned to targeting an interest rate. In April 2013 it planned to double base money, from
138 trillion yen at the end of 2012 to 270 trillion yen at the end of 2014. At the end of 2014, base money
stood at about 276 trillion yen [Bank of Japan 2001](https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2001/k010319a.htm) (decision of March 2001) [Bank of Japan 2004](https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2004/k040120.htm) (decision of January 2004) [Bank of Japan 2006](https://www.boj.or.jp/en/mopo/mpmdeci/mpr_2006/k060309.htm) (decision of March 2006) (Bank of Japan 2013, its statement of April 2013, p. 1 and its note) [Bank of Japan](https://www.boj.or.jp/en/statistics/boj/other/mb/mblong.xlsx) (Monetary Base, long series, end of December 2014).

**2022: the ECB's rate, and the parts of M2.** The ECB raised the rate it pays banks on money they leave with it, from
below zero before July 2022 to 4.00% by September 2023 [ECB](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html) (key ECB interest rates, deposit facility).
In July 2022 it raised this deposit rate from -0.50% to zero. That starting rate was below zero, so banks were paying to leave money with the ECB (the ECB's key
interest rates, deposit facility). Within M2, savings and other liquid deposits fell by $1.13 trillion over 2022.
Small time deposits and retail money-market funds, which M2 also counts, rose by $0.52 trillion, and notes,
coin and demand deposits rose by $0.44 trillion. These figures for time deposits and funds also include
money in retirement accounts, which M2 itself does not count, so they are not exactly the parts of M2 [Federal Reserve Board, H.6](https://www.federalreserve.gov/releases/h6/) (other liquid deposits, small time deposits and retail money funds (FRED's MDLM, STDSL and RMFSL), December 2021 and December 2022) [Federal Reserve H.6](https://www.federalreserve.gov/releases/h6/current/default.htm) (Money Stock Measures, notes on M1 and M2).

**Silicon Valley Bank's uninsured deposits.** The share of uninsured deposits quoted in the text is the whole Silicon
Valley Bank group's. At the bank itself, one part of the group, the share was 88%, as the bank
reported it [FDIC 2023](https://www.fdic.gov/news/speeches/2023/spmar2723.html) (Chairman Gruenberg's testimony, March 2023, the section on Silicon Valley Bank). On the day of the run, more than $100 billion was expected to leave Silicon Valley Bank the following day (Federal Reserve Board 2023, its review of the supervision of Silicon Valley Bank).

**Northern Rock.** Runs on banks show what happens when people doubt the promise. In September 2007, once Northern Rock's difficulties became known, its depositors rushed to take their money out. The government then guaranteed all of Northern Rock's existing deposits (Bank of England 2007, its Financial Stability Report of October 2007, Box A, p. 11).

**Money as memory.** Monetary theory reaches a view related to the credit theory of money by another route. Kocherlakota showed that a full record of who gave what to whom could do everything that money does for a society. In that sense, money works as "a primitive form of memory" (Kocherlakota 1998, 'Money Is Memory', pp. 232–233).

**Very high inflation and growth.** Very high inflation goes with lost growth while it lasts. Fischer found that high inflation and lasting growth do not go together. Bruno and Easterly found that growth fell sharply while inflation ran above 40% a year, and recovered strongly once inflation fell back below that level. On average, the fall and the recovery roughly cancel each other out (Fischer 1993, 'The Role of Macroeconomic Factors in Growth', an NBER working paper, its abstract) (Bruno and Easterly 1995, 'Inflation Crises and Long-Run Growth', an NBER working paper, its abstract).

**Where the rise in US share values came from.** One study split the rise in the value of US shares per person, after inflation, from 1989 to 2017. It attributes 25% of that rise to economic growth. Profits shifted to shareholders, mostly from wages, account for 40%. Investors asking less extra return for the risk of holding shares account for 21%, and lower interest rates for 14% (Greenwald, Lettau and Ludvigson, 'How the Wealth Was Won', the abstract and Table 2, Panel B, p. 37).

**National wealth: saving and prices.** Most of the growth of US national wealth from 1970 to 2010 came from saving, not from rising prices. Piketty and Zucman put 72% of that growth down to saving, and the rest to rises in asset prices. National wealth is a different measure from the households' wealth in the study's case study on where US households' real wealth came from (CS-E) (Piketty and Zucman 2014, 'Capital is Back', p. 1257 and pp. 1285–1286, Table V).

**Where the share gain came from before 1989.** From 1952 to 1988 the rise in the value of US shares per person was
slower than from 1989 to 2017. Growth alone added more than the whole rise, more than 100% of it,
because the other forces taken together pulled the value down (Greenwald, Lettau and Ludvigson, Table 2, Panel B).

**Energy in Germany and France, 2022.** In the first three quarters of 2022, energy added about twice as much to
Germany's inflation as to France's. Blanchard and Bernanke write that this gap appears to reflect in large part
differences in subsidies meant to cap energy prices (Blanchard and Bernanke 2024, p. 29 and p. 31).

**The BIS's split on excess money growth.** The BIS also divided the cases by excess money growth instead of by
inflation, and found the same split (Borio, Hofmann and Zakrajšek 2023, p. 3 and a note to it). Excess money growth is broad
money growth minus the growth of real output (Borio, Hofmann and Zakrajšek 2023, a BIS Bulletin, p. 3, its second graph and the note to it).

**The Fed's "deferred asset".** The Fed records the shortfall it must make good before it pays the state again as a
"deferred asset". Despite its name, it is not money the Fed holds (Federal Reserve Banks, Combined Financial
Statements 2023, the notes on the deferred asset).

**The Fed's agency securities.** In the latest year the Fed also put the money repaid on its agency securities into
Treasury bills [FOMC 2025](https://www.federalreserve.gov/newsevents/pressreleases/monetary20251210a1.htm) (implementation note of 10 December 2025).

## Other cases and sources, section by section

The study's text keeps open one or two cases for each point, and one source at the end of each sentence. The other
cases, and the further sources for its sentences, are kept here under the section of the study they belong to, each
with its claims and sources.

### Banks create money when they lend: other cases and sources

**Further sources.** That a bank which lends does not hand over other savers' deposits is also stated by Jakab and
Kumhof (2015, the abstract of their Bank of England staff working paper).

That adding
reserves did not, by itself, make it easier for banks to lend is also the reading of Borio and Disyatat (2009, a BIS
working paper, pp. 1–2) and of Carpenter and Demiralp (2010, a FEDS working paper, its abstract).

How money moving into the Treasury's account at the Fed removes reserves
from the banks is also set out in the Fed's own account of itself (Federal Reserve 2021, The Fed Explained, p. 87
and p. 103).

**The Bank of Amsterdam's story.** The Bank of Amsterdam was founded in 1609. At first it took deposits of coin and
did not expand credit. Later the same bank lent on a large scale to the Dutch East India Company and to the city, and
its promise failed. It suspended payments in 1791. By 1795 the precious metal the bank held covered only
21% of what it owed, and the bank no longer played a part in the city's commerce [de Vries and van der Woude](#sources) (The First Modern Economy, the passage on the Bank of Amsterdam; a book, listed in the methods' sources) [Kindleberger and Aliber](#sources) (Manias, Panics and Crashes, the chapter on the Bank of Amsterdam; a book, listed in the methods' sources) (Quinn and Roberds, their paper on the lessons of the shadow banking crisis of 1763, p. 1158).

### A deposit is a bank's debt to you: other sources

**Further source.** The limit of deposit insurance per depositor, for each ownership category, at each insured bank,
is set in the United States Code, in its section on the FDIC's insurance of deposits (the 2023 edition).

### What do central banks control: other sources

**Further sources.** The window of the Fed's purchases, from November 2008 to October 2014, is dated by the Federal
Reserve Board's press release of November 2008, which announced them, and by the FOMC's statement of October 2014,
which ended them.

### Did money grow out of barter: other cases and sources

**Further sources.** Desan also tells the familiar story, as the conventional story of how money was created (Desan
2014, Making Money, its first chapter).

Graeber also finds barter between strangers,
or where money has failed [Graeber 2011](#sources) (Debt, p. 29; a book, listed in the methods' sources).

**Menger's account.** The economist Menger explained how money could have grown out of barter. His account shows that
this was possible in theory, not that it happened [Graeber 2011](#sources) (Debt, pp. 28–29; a book, listed in the methods' sources).

**What the first coins were made of.** The first coins were made of a natural mix of gold and silver. The Greek
historian Herodotus wrote that the Lydians were the first people to make coins of gold and silver (Head 1911,
Historia Numorum, the entry on Lydia, pp. 643–645).

**A state's paper money in Song China.** Paper came late too. The Song state issued its own paper money in Sichuan
from the 1020s. Its notes could be exchanged for the region's iron coin. They were a state's promise on paper, long
before Europe had one [von Glahn 1996](#sources) (Fountain of Fortune, p. 51; a book, listed in the methods' sources).

**How banks' money began in England.** In England, the money that banks issued had two origins: deposits of coin, and
a loan to the state. London's goldsmiths had stored coin and given receipts for it, and the receipts came to circulate
as money [McLeay, Radia and Thomas 2014a](https://www.bankofengland.co.uk/-/media/boe/files/quarterly-bulletin/2014/money-in-the-modern-economy-an-introduction.pdf) (p. 8). The Bank of England was founded in 1694 to lend £1.2 million to the Crown, at
8% a year. The Bank made the loan by issuing its own notes. The state paid for its spending with
these notes and took them back in taxes. By 1696 more than £2 million of notes were in circulation
(Desan 2014, Making Money, the chapter on the mode of payment) [Graeber 2011](#sources) (Debt, p. 49; a book, listed in the methods' sources) (Bank of England, 'Our history', the entries for the year of its founding).

### John Law's France: other sources

**Further source.** Murphy (1997, pp. 228–229 and p. 266) is the second source for the fixing of the share price in March 1720
and for the end of the notes as money.

### Where does inflation come from: other cases and sources

**Argentina since then.** Monthly inflation in Argentina has stayed far lower since: 1.7% in August 2026. Over the twelve months to August 2026, prices still rose 33.5% in total [INDEC](https://www.indec.gob.ar/ftp/cuadros/economia/serie_ipc_divisiones.csv) (consumer prices by division, national level, monthly and twelve-month changes).

**Further sources.** TePaske (2010, A New World of Gold and Silver, p. 5 and p. 306) is the second source for the large
amounts of American silver that reached Spain.

Teles and Uhlig (2013, p. 3) are
the second source for the split by inflation: a link between money growth and inflation about one for one when
inflation is high, and nearly absent when it is low.

### What happens in a hyperinflation: other sources

**Further source.** Romer's textbook gives the same account of Cagan's model [Romer](#sources) (Advanced Macroeconomics, the chapter on inflation and money growth; a book, listed in the methods' sources).

## Robustness, chosen by risk

| Risk | Addressed by |
|---|---|
| A definition of money tuned to the result | each central bank's own aggregate, fixed on the card before any value; the IMF's lines for every economy beside (`C35`) |
| Currency in banks' vaults counted as the public's | the held side only in the US and the euro area; in Britain counted, said beside its share (`C35`) |
| US notes held abroad inflating the share | said; it only strengthens "a minority" |
| A minority in three economies only | the IMF's lines for every economy with both, each at its latest month (`C35`) |
| A household wealth split with a hidden residual | the quarterly table has none; the parts sum to the real change, to the release's rounding (`C36`) |
| A group chosen after the values | the partition fixed on the card, every line placed once (`C36`) |
| An identity read as a cause | said in the text and the caption; velocity printed (`C37`) |
| A picture read as a test | no line, no slope, no correlation (`C38`) |
| A split drawn on the outcome | the line on money growth only; the line on inflation never read (`C28`) |
| Changes of unit in long series | C28's units guard |
| Filled prices from a restricted database | the public figures drawn without the filled windows |
| Fiscal demand confounding the cross-section | said beside every reading (`C31`) |
| One economy driving the cross-section | every single drop, the count that flips printed (`C31`) |
| The US base after 2008 read as a test of money and prices | its confounder said beside it: purchases answered collapsed demand at rates near zero, and reserves earned interest |
| Point-in-time (what was knowable when) | n/a because the study draws no investor rule and no scenario |

## Model steps the methods rely on

The passages cited in the register were read at their pages by runs of a language model (Claude),
the study's writer and its delegated readers, and the project's notes name who read each.
The isolated checks this text cites are separate runs of a language model (Claude), none of them
a run that made what it checked.

## The research log

The order of work, the checks and their answers are kept in the project and are not public: the step record, the
reports of the checks and their answers, and the notes (the harvest, the sources and their passages, the gaps).

This part was rebuilt on 2026-10-10 and 2026-10-11 from its brief under the series design of three parts, every step
run again and each piece of earlier work reused only where a rerun would produce the same. Reused: the frozen data; the
cards `C28`, `C29`, `C30` and `C31` with their runs; and the passages already read at their pages. New: the map and the
dossier of this part; the cards `C35`, `C36`, `C37` and `C38`, each checked three times by an isolated check before any
run and fixed in place, the fixes named in their history; the register's claims, each sourced passage read; and the
study's text.

**Correction, 21 October 2026.** The IMF's consumer price index for Kazakhstan (International Financial Statistics,
`PCPI_IX`, frozen on 30 September 2026) changes units in January 2020: it doubles in one month, with no flag or note.
The World Bank's index (World Bank, World Development Indicators, `FP.CPI.TOTL`, frozen on 30 September 2026) is the
same series through 2019 and runs 1.9427 times below the IMF's from 2020, a ratio that holds within half a
percent through 2024, so it was a change of units, not of prices. In CS-C it put a false doubling into Kazakhstan's
window from 2010 to 2020: an average of 13.7 log points a year (about 14.7%) where 7.0 (about 7.3%) is right.
The panel now reads the IMF's index for Kazakhstan from January 2020 divided by that ratio, computed from the two
frozen files (`toolkit/ft/data/splices.py`). Before the IMF's monthly index feeds any count, a check now holds the IMF's monthly index of every money against the World Bank's annual index, for one-month moves of roughly a quarter or more, far larger than the series' usual monthly moves of the previous five years (`toolkit/ft/quant/jumps.py`; the BIS's monthly series, which feeds a few counts, and the US and euro-area indices are not screened): a move the World Bank does not confirm stops the run unless it is named with its reason. The other moves it names are left as the IMF reads them: Myanmar's in January 1973 and Congo's (Democratic Republic) in January 2010, both flagged for a separate correction, and Palestine's in 2025 and Zimbabwe's in June 2023, read as price moves. Under that reading Myanmar's index and Congo's are read as the IMF prints them; no number printed here depends on Myanmar's. The check is not exhaustive: smaller moves pass unseen, and the World Bank's index often derives from the same IMF data, so its agreement is not an independent confirmation. The cards were rerun by their own code (`C02`,
`C03`, `C21`, `C23`, `C25`, `C27`, `C28`, `C29`, and `C41` for `C39`); `C40`, an earlier rerun on a wider correction
that was withdrawn, is kept as it was. Four were kept as run, unchanged: `C15`, the episodes the FT-001 map's frame c
(`data/reconstructed/ft001-c`) reads at a pinned version, which a rerun would break, and `C18`, `C24` and `C26`, the
deciders read on those episodes; none feeds a number printed here. What moved in print: in CS-C's figure, broad
money's slope below the line, 0.62 to 0.61 (its range
0.48 to 0.75, now 0.48 to
0.74); in these methods, `S7`'s slope above the line, 0.65 to 0.66,
and at the line of a tenth, 71 to 70 of 203 windows in the second
band and 188 to 187 of all windows. No reading changes. Separately, a fault
of rounding: the CS-C figure's values were stored rounded to three decimals and rounded again when shown; they are now
stored to four and rounded once.

## Sources

<!-- numbers:off -->
**Works read at the passage cited** (the page, table or section of each is in the register's `claims`):

- Bank of England (2007). Financial Stability Report, October 2007.
- Bank of England. Explainer, "How is money created?"; "Further details about M4 data"; "Our history".
- Bank of Japan. Monetary policy decisions of March 2001, January 2004, March 2006 and April 2013; Monetary Base, long series (end of 2014).
- Barro, R. and F. Bianchi (2023). Fiscal Influences on Inflation in OECD Countries, 2020–2023. NBER WP 31838.
- Barsky, R. and L. Kilian (2001). Do We Really Know that Oil Caused the Great Stagflation? NBER WP 8389.
- BCRA (2026). Informe de Política Monetaria, June 2026.
- BEA. Glossary, "Value added".
- Blanchard, O. and B. Bernanke (2023). What Caused the US Pandemic-Era Inflation? NBER WP 31417.
- Blanchard, O. and B. Bernanke (2024). An Analysis of Pandemic-Era Inflation in 11 Economies. NBER WP 32532.
- Blanchard, O. and J. Galí (2007). The Macroeconomic Effects of Oil Shocks. NBER WP 13368.
- BLS. Measuring Price Change in the CPI: Rent and Rental Equivalence.
- Borio, C. and P. Disyatat (2009). Unconventional Monetary Policies: An Appraisal. BIS WP 292.
- Borio, C., B. Hofmann and E. Zakrajšek (2023). Does Money Growth Help Explain the Recent Inflation Surge? BIS Bulletin 67.
- Braun, R., A. Flaaen and S. Hacıoğlu Hoke (2024). Supply vs Demand Factors Influencing Prices of Manufactured Goods. FEDS Notes.
- Bruno, M. and W. Easterly (1995). Inflation Crises and Long-Run Growth. NBER WP 5209.
- Buiter, W. (2007). Seigniorage. NBER WP 12919.
- Carpenter, S. and S. Demiralp (2010). Money, Reserves, and the Transmission of Monetary Policy. FEDS 2010-41.
- Chodorow-Reich, G., P. Nenov and A. Simsek (2021). Stock Market Wealth and the Real Economy. NBER WP 25959.
- de Vries, J. and A. van der Woude (1997). The First Modern Economy. Cambridge University Press.
- Desan, C. (2014). Making Money: Coin, Currency, and the Coming of Capitalism. Oxford University Press.
- Diamond, D. and P. Dybvig (1983). Bank Runs, Deposit Insurance, and Liquidity. Journal of Political Economy 91(3).
- Doepke, M. and M. Schneider (2006). Inflation as a Redistribution Shock: Effects on Aggregates and Welfare. NBER WP 12319.
- Doepke, M. and M. Schneider (2006). Inflation and the Redistribution of Nominal Wealth. Journal of Political Economy 114(6): 1069-1097. A held copy, read at pp. 1069 and 1071.
- Drechsler, I., A. Savov and P. Schnabl (2017). The Deposits Channel of Monetary Policy. NBER WP 22152.
- European Commission (2019). Ex-Post Evaluation of the Economic Adjustment Programme, Cyprus, 2013–2016. Institutional Paper 114.
- European Central Bank. Monetary aggregates; key ECB interest rates.
- FDIC (2023). Testimony of Chairman Martin Gruenberg to the Senate Committee on Banking, 27 March 2023.
- Federal Reserve. Money Stock Measures (H.6), notes, release of 22 September 2026; Financial Accounts of the United States (Z.1), table L.210, release of 9 March 2023.
- Federal Reserve. Factors Affecting Reserve Balances (H.4.1), release of 8 October 2026; The Fed Explained, 11th ed. (2021).
- Federal Reserve Bank of New York (2023). Open Market Operations during 2022.
- Federal Reserve Banks. Combined Financial Statements, 2019, 2023 and 2025.
- Board of Governors of the Federal Reserve System, Treasury and FDIC. Joint statement of March 2023.
- Bank of Japan (2016). Comprehensive Assessment of the monetary easing since the introduction of QQE.
- Federal Reserve Board. Press releases of October and November 2008; FAQ "What is the money supply?"; Review of the Federal Reserve's Supervision and Regulation of Silicon Valley Bank (2023).
- Fischer, S. (1993). The Role of Macroeconomic Factors in Growth. NBER WP 4565.
- FOMC. Minutes of September 2013; Records of Policy Actions, October 1979 and October 1982; statements of October 2014, January 2022, March 2022 and May 2022.
- Gold Reserve Act of 1934, 48 Stat. 337.
- Graeber, D. (2011). Debt: The First 5,000 Years. Melville House.
- Greenspan, A. (1993). Testimony of July 1993.
- Greenwald, D., M. Lettau and S. Ludvigson (2024). How the Wealth Was Won: Factor Shares as Market Fundamentals. NBER WP 25769.
- Hanke, S. and N. Krus (2013). World Hyperinflations. In Parker and Whaples, eds., Routledge Handbook of Major Events in Economic History.
- Hamilton, E. J. (1934). American Treasure and the Price Revolution in Spain, 1501–1650. Harvard University Press. A held copy, read at p. 301.
- Head, B. (1911). Historia Numorum, 2nd ed. Oxford.
- Humphrey, C. (1985). Barter and Economic Disintegration. Man 20(1).
- Ihrig, J., E. Meade and G. Weinbach (2015). Monetary Policy 101. FEDS 2015-047.
- INDEC. Consumer prices by division.
- Innes, A. M. (1913). What Is Money? Banking Law Journal 30(5).
- Jakab, Z. and M. Kumhof (2015). Banks are not intermediaries of loanable funds — and why this matters. Bank of England Staff WP 529.
- Jevons, W. S. (1879). The Theory of Political Economy, 2nd ed.
- Jordà, Ò., S. Singh and A. Taylor (2024). The Long-Run Effects of Monetary Policy. NBER WP 26666.
- Kindleberger, C. and R. Aliber. Manias, Panics and Crashes.
- Kocherlakota, N. R. (1998). Money Is Memory. Journal of Economic Theory 81: 232-251. A held copy, read at pp. 232-233.
- Krugman, P. (1998). It's Baaack: Japan's Slump and the Return of the Liquidity Trap. Brookings Papers on Economic Activity 1998(2).
- Law, J. (1705). Money and Trade Considered, as quoted in Murphy (1997), pp. 88–89.
- Lucas, R. (1996). Nobel Lecture: Monetary Neutrality. Journal of Political Economy 104(4); cited at the pages of the Nobel Foundation's PDF of the lecture (1995), the copy read.
- Magyar Nemzeti Bank. History.
- McCandless, G. and W. Weber (1995). Some Monetary Facts. Federal Reserve Bank of Minneapolis Quarterly Review 19(3).
- McLeay, M., A. Radia and R. Thomas (2014). Money creation in the modern economy. Bank of England Quarterly Bulletin 2014 Q1.
- McLeay, M., A. Radia and R. Thomas (2014a). Money in the modern economy: an introduction. Bank of England Quarterly Bulletin 2014 Q1.
- Mehrling, P. (2012). The Inherent Hierarchy of Money. Paper of 25 January 2012.
- Mian, A. and A. Sufi (2009). House Prices, Home Equity-Based Borrowing, and the U.S. Household Leverage Crisis. NBER WP 15283.
- Murphy, A. (1978). Money in an Economy Without Banks: The Case of Ireland. Manchester School 46.
- Murphy, A. (1997). John Law: Economic Theorist and Policy-Maker. Oxford University Press.
- Piketty, T. and G. Zucman (2014). Capital is Back: Wealth-Income Ratios in Rich Countries 1700–2010. Quarterly Journal of Economics 129(3).
- Quinn, S. and W. Roberds. Responding to a Shadow Banking Crisis: The Lessons of 1763.
- Radford, R. A. (1945). The Economic Organisation of a P.O.W. Camp. Economica 12(48).
- Reinhart, C. and K. Rogoff (2009). This Time Is Different: Eight Centuries of Financial Folly. Princeton University Press.
- Ricks, M. (2016). The Money Problem. University of Chicago Press.
- Romer, D. Advanced Macroeconomics. McGraw-Hill.
- Schumpeter, J. (1934). The Theory of Economic Development, tr. R. Opie. Harvard University Press.
- Shapiro, A. H. (2024). Decomposing Supply and Demand Driven Inflation. Federal Reserve Bank of San Francisco WP 2022-18, revised February 2024. A held copy.
- Smith, A. (1776). The Wealth of Nations, Book I, chapters 1 and 4 (Bohn's edition, 1921).
- Teles, P. and H. Uhlig (2013). Is Quantity Theory Still Alive? NBER WP 16393.
- TePaske, J. (2010). A New World of Gold and Silver. Brill. Read at pp. 5 and 306.
- Tobin, J. (1963). Commercial Banks as Creators of "Money". Cowles Foundation Discussion Paper 159. A held copy, read at typescript pp. 7–9.
- United States Code, 12 U.S.C. §1821.
- Velde, F. (2003). Government Equity and Money: John Law's System in 1720 France. Federal Reserve Bank of Chicago WP 2003-31.
- von Glahn, R. (1996). Fountain of Fortune: Money and Monetary Policy in China, 1000–1700. University of California Press.
- Walsh, C. (2010). Monetary Theory and Policy, 3rd ed. MIT Press.
- Werner, R. (2014). Can banks individually create money out of nothing? International Review of Financial Analysis 36.

**Data** (each manifest under `data/` gives where and when a series was fetched, and its hash): the US series from their original agencies, read over the dates of the FRED copies the study first used (the author,
2026-10-21; FRED's id in brackets): the Federal Reserve Board's H.6 (currency, M2, other liquid deposits, small time
deposits, retail money funds, the monetary base: `CURRSL`, `M2SL`, `MDLM`, `STDSL`, `RMFSL`, `BOGMBASE`), H.8
(loans and leases, bank credit, securities: `TOTLL`, `TOTBKCR`, `INVEST`; the Board's revisions from July 2026 on move
the printed loans figure from FRED's older copy), H.15 (`FEDFUNDS`) and H.4.1 (`TREAST`); the
BEA's NIPA tables 1.1.5, 1.1.6 and 1.1.9 (`GDP`, `GDPC1`, `GDPDEF`; its annual update of September 2026 revises the
quarters since 2021, so the printed nominal GDP figure differs from FRED's older copy); the BLS's CPI-U (`CPIAUCSL`) and output per
hour (`OPHNFB`); and from FRED itself `M2V` (FRED's own calculation, which no agency publishes) and the deficit as a
share of GDP, `FYFSGDA188S`, which the OMB publishes on a host the project cannot reach; the reused runs of cards C28 to C31 were computed on
FRED's copies of the same series before the switch and are read as they stand; the ECB's monetary statistics (BSI), its
quarterly sector accounts for households and the HICP; the Bank of Japan's monetary base, long series; the Bank of England's `LPMAVAB` and `LPMAUYN`; the IMF's
International Financial Statistics; the Federal Reserve Board's Financial Accounts (Z.1); and, for C28's grid, the
IMF's, the World Bank's, FRED's and the ECB's series.
<!-- numbers:on -->

## How to reproduce every figure and every number

Every number in this folder and in the web study is read from the register (`results/numbers.json`), which names for
each number the script that computed it or the source and page it is cited from. From the study's folder, `code/run.py`
runs the four cards of the rebuild (`p2_cs_a.py`, `p2_cs_e.py`, `p2_cs_f.py`, `p2_cs_g.py`; each refuses a card changed
since it was committed), writes the register (`p2_registry.py`, from the runs, the reused runs, the frozen series,
`p2_cited.yaml` for the numbers cited at their pages and `p2_claims.yaml` for the sourced claims), draws the web study's
figures and the balance-sheet explorer (`p2_figures.py`) and its preview image (`p2_og.py`). The reused cards ran once
at their own step (`units_guard.py`, `cs_b.py`, `cs_e.py`), each refusing a changed card. Also published: the cards
(`cards/`), the results (`results/runs/`, with the redactions listed in `REDACTIONS.md`) and the manifest of every
dataset read (`data/`).

Not investment advice.
