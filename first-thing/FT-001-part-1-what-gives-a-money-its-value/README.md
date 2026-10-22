# What gives a money its value? — methods and proof

*A First Thing Weekly Study · FT-001, part 1 of "The life of a money" · as of 2026-10-11*

This folder is the proof behind the study published on First Thing's site, for the sceptic and the specialist: what
each claim rests on, what was fixed before each result, what ran, what each result means and what it does not, where
the data come from, and the code. It is not the study: the study, with its argument, its charts and its slider, is on
the site.

Reproduction level: read the code

The code is published here and every number names the script that computed it or the source and page it is cited
from. The code calls a small shared toolkit of ours (the register of numbers, the cards, the charts, the data readers)
that is not in this repository, and the fetched series are not republished: each manifest under `data/` says where a
series was fetched, when, and its hash. So the code can be read and every source traced; it cannot be rerun from this
folder alone.

## What each claim rests on

The study answers its question in ten components, from why a money is accepted to what a reader can ask of any money.
Every claim it makes is in the register (`results/numbers.json`, its `claims`), with its type, the component it
serves, and either the passages it rests on (each with its page, table or section, the copy read, and how deeply the
work was read) or the card of the analysis that measured it. Four types are used: **established** (a documented fact
or mechanism, cited at its passage), **cases** (shown in history, with their sources), **measured** (an analysis of
ours, with its card, or the build protocol it ran) and **judgement** (our reading, said as ours).

The headline is a judgement. It weighs the floor that payments owed by law give a money (established: Woodford,
Cochrane, Grubb; the Fed's and the ECB's pages on legal tender), the monies that circulated with no state behind them
(cases), the cases of backings suspended, kept in law while prices doubled, broken and given up (cases),
and the losses since 1992 of the six monies most readers hold (measured, CS-A). CS-A is a description per money; it
names no regime and credits no restraint with the low losses. No other measurement of ours enters the headline.

What stood behind the destroyed monies is told in the sources' words (Romer's "most, if not all", Cagan, Fischer,
Sahay and Végh within their scope), the cases being told as existence, never counted for or against it. The study
draws no line between the financed monies that held and those destroyed: theory gives a limit, the most a state can raise for long by printing money (Romer, after Cagan), but none of the sources read says where it lay for a money before the fact.

Six analyses of ours are case studies inside the study, each beside the component it supports; none carries the
answer alone, and each component rests on its sources first.

## The readings, and the size that matters

Each measured claim is read against the size that matters, fixed on its card, before or, for the reused cards, as
said here.

- CS-A, CS-B, CS-C and CS-E are descriptions: each figure is printed as it is, read against no size, with no null.
- CS-D: the gap between paper and convertible years, 3.6 points a year (1.9 to
  5.7), against a size that matters of one point a year: an **effect**.
- CS-F: the leavers' consumer-price inflation over the stayers', 1932 to 1934, 3.8 points a year
  (-3.1 to 11), against one point a year: **bounded**. It rules out a gap larger than about
  11 points, and nothing smaller. The size that matters on this card (`C18`) was set after a check of the
  earlier design had printed the 1932–34 consumer-price changes; the card's `seen` field says so.

The cards `C18`, `C19` and `C20` were made for the earlier design of this study and are reused because a rerun would
produce the same: their question, data and code still serve the answer.

## The levels in plain words (today's monies)

The section on today's monies reads past episodes for the levels that mattered (`k9-levels`), in plain words; the
figures behind each word are these. "About half" of Japan's government bonds: the Bank of Japan's share,
47% in June 2026, at a peak of 54% in September 2023. Turkey's rate
"well below inflation": a policy rate of 14% by December 2021 against consumer prices
up 19.6% in the year to September 2021, when the cuts began; "nearly three-quarters": consumer prices 72%
higher in 2022 than in 2021, on yearly averages; "about a third": 35% in 2025. The readings
are associations in the episodes told; none is a threshold we fix or a forecast.

The count in the same reading (`k9-base-rate`; card `C25`, `code/p1_k9_debt.py`) reads the Jordà-Schularick-Taylor database (its sixth release, frozen 2026-09-30; its values, under a CC BY-NC-SA licence, are not republished in bulk: the counts below are ours, and the run is withheld as `C23` and `C24` are, its code regenerating it from the frozen file): public debt against GDP, in the database's own measure, which is wider than the US debt held by the public quoted for today (on it, US debt was above 100% of GDP from 2013 to 2020, the database's last year), and consumer prices for eighteen economies. A crisis year is one in which consumer prices rose by 20% or more, Reinhart and Rogoff's line, as the study defines a crisis; a crisis begins in a year when the year before was below the line, so a crisis that resumes after a year below it begins again. Each year with a debt figure, not itself a crisis year, and with price readings for the next three years, counts once; it is followed when a crisis begins in one of those three years. Years overlap, so one beginning can follow up to three years. The years are set apart when any year from three before to three after is a year of the two world wars (for all eighteen, neutrals included), of Spain's civil war, of Japan's war in China from 1937, or of the war of 1870 to 1871 (France and Germany). Other wars sit among the years away from those wars (among them Portugal's in Africa, France's in Indochina and Algeria, Korea and Vietnam), unless a war of the first list falls within three years. The bands, the wars set apart and the three-year window were fixed before the count. The bands, on the debt figure: below 60%, 60% to 100%, above 100%, none merged. Away from those wars, the shares followed, with ninety-five per cent intervals from a bootstrap that redraws whole economies, since an economy's years are not independent: 1.7% (0.5% to 3.3%), 1.3% (0.0% to 3.2%) and 3.6% (0.0% to 8.7%), in 18, 17 and 11 economies; near the wars, 17.9%, 20.2% and 10.9%; all years together, 56 of 1,537, 25 of 556 and 13 of 268. With few economies in a band, the interval is too narrow, and a shock common to many economies at once (the 1970s) narrows it too. At a 10% line, away from those wars: 122 of 1,237, 16 of 448 and 15 of 214 years followed; near the wars, 74 of 142, 32 of 73 and 19 of 37. The debt figure is missing for years that cluster on wars and crises (Germany from 1914 to 1926 and 1944 to 1949, France from 1914 to 1919 and 1939 to 1948, among others), so those years are never counted. Crisis beginnings that no year reaches: 4 at 20% (France 1918 and 1942, Belgium 1920, Switzerland 1872; 3 near the wars) and 9 at 10%. Germany's inflation of 1919 to 1923 is not a missed beginning: prices rose by the line or more in every year from a beginning during the First World War to 1923, and the years just before the war, which have a debt figure, reach that beginning, so it is counted among the years near the war. The debt figure's denominator is nominal GDP, which rises with prices, so a year of rising inflation sits in a lower band than its debt alone would put it. The eras behind the high-debt years, and the US years above 100%, were read from the debt figure alone, outside the run. The count describes the past of eighteen economies that survived, all rich today; it says nothing of which came first, sets no threshold and forecasts nothing.

## CS-A

**What a unit of money buys, 1914–2025** (`cards/C21-cs-a-what-a-unit-buys.yaml`, `code/p1_cs_a.py`,
`results/runs/C21-cs-a-what-a-unit-buys.json`; the BIS's statistics, republished with the BIS cited as source).

One unit of each of six monies, followed through the BIS's long consumer-price series (`data/bis/WS_LONG_CPI`, frozen
on 2026-09-30), annual averages: the US dollar, the pound sterling, the Swiss franc, the yen, the French franc carried
into the euro's prices in France, and the Deutsche Mark carried into the euro's prices in Germany. Each money starts in
1914 or the first year its series allows: the Swiss franc in 1921, the yen in 1947 (its 1946 rests on a few months),
the French franc in 1951, the Deutsche Mark in 1949. Units are chained across their changes by the official factors:
France's new franc of 1960 at one hundred old francs (the BIS's 30th Annual Report, p. 157), and the euro's fixed
rates of 31 December 1998 (the ECB). Germany's reform of June 1948 converted money at several rates (Mendershausen
1949, p. 658 and its note), so it is not chained: the Reichsmark, 1924 to 1947, is shown as its own money, and the
Deutsche Mark from 1949; the annual 1948, which spans the reform, belongs to neither. The Reichsmark's index reads
official prices under the price stop of 1936 (Mendershausen 1949, p. 649); our reading is that it understates what a
Reichsmark lost.

The four periods and their reasons were fixed on the card before the run: 1914–45 (the wars and the slump), 1946–71
(the postwar fixed rates), 1972–91 (after gold), 1992–2025 (the last third of a century, about a working life). Each
period's loss is measured from the year before it, as a yearly average of the share of what a unit buys that is lost;
a period outside a money's series is not computed. The dollar's 2025 rests on eleven months.

The results (each in the register, with its period and base year):

| Money | 1914–45 | 1946–71 | 1972–91 | 1992–2025 |
|---|---|---|---|---|
| US dollar | 1.9% | 3.1% | 5.9% | 2.5% |
| Pound sterling | 3.1% | 4.3% | 8.3% | 2.4% |
| Swiss franc | 0.2% | 1.9% | 4.0% | 0.8% |
| Yen | | 7.4% | 5.0% | 0.6% |
| French franc, then the euro in France | | 4.2% | 7.3% | 1.6% |
| Deutsche Mark, then the euro in Germany | | 1.9% | 3.6% | 2.0% |
| Reichsmark | 0.5% | | | |

The euro's two carriers are its national indices; the euro area's own index, kept from 1990, lies close to them: from
1992 to 2025 (measured from 1991) the yearly loss on France's index differed from it by -0.5 points and on Germany's by
-0.1; a minus sign means that the national index lost less. The slider on the site reads a grid computed by the same code: for each money and each year, what
one unit of that year buys in 2025 (the Reichsmark in its 1947 value).

## CS-B

**The franc at home and abroad** (`cards/C22-cs-b-the-franc.yaml`, `code/p1_cs_b.py`,
`results/runs/C22-cs-b-the-franc.json`; the BIS's and the World Bank's series, each cited).

The franc's rise against the dollar and against its trading partners is split in logs into two parts that add up:
the inflation gap (Swiss consumer prices against the other side's) and the real rise. The data: the BIS's exchange
rates (`WS_XRU`) and effective rates (`WS_EER`, narrow from 1970, broad from 1994), both frozen on 2026-10-10, and its
long consumer prices; the World Bank's price-level factors and market rates (`PA.NUS.PPP`, `PA.NUS.FCRF`) for
Switzerland's GDP price level against its neighbours'; and exports as a share of GDP (`NE.EXP.GNFS.ZS`). Each stretch is
measured from the year before it, never chained. A stretch's share from the inflation gap is printed only when the
total exceeds one log point and both parts share its sign.

| Stretch | Against the dollar: total | inflation gap | real |
|---|---|---|---|
| 1970–2025 | 165 | 96 | 68 |
| 1970–1980 | 95 | 27 | 68 |
| 1980–1990 | 19 | 13 | 6 |
| 1990–2000 | -20 | 8 | -28 |
| 2000–2010 | 48 | 15 | 33 |
| 2010–2025 | 23 | 33 | -11 |

Against the narrow basket, 1970–2025: 156 log points, 108 from
the gap and 48 real; against the broad basket, 1994–2025: 74,
66 and 8. In 2025, Switzerland's GDP price level was
1.37 times Austria's, 1.40 Germany's, 1.46
France's and 1.62 Italy's. Exports went from 38% of GDP to
78%; they are drawn beside the real rate as a description, never as an effect of it.

## CS-C

**How often a new inflation crisis began, and the years spent in one** (`cards/C28-cs-c-losses-by-era-kazakhstan.yaml`,
`code/p1_cs_c.py`, `results/runs/C28-cs-c-losses-by-era-kazakhstan.json`; `cards/C29-cs-c-years-in-crisis-kazakhstan.yaml`,
`code/p1_cs_c_years.py`, `results/runs/C29-cs-c-years-in-crisis-kazakhstan.json`; both withheld, since they rest on
Reinhart and Rogoff's values, and `C28` on the Jordà–Schularick–Taylor database's too, whose values are not republished
in bulk). `C28` and `C29` are the cards `C23` and `C24` rerun, their rules unchanged, on the price panel with Kazakhstan's correction
alone (22 October 2026, under the research log); `C23`'s and `C24`'s own runs are kept as they were, and so are `C26`'s and
`C27`'s, an earlier rerun on a wider correction that was withdrawn.

Beside the count of crises begun, card C24 (rerun as C29) counts, on C23's own money-years, the years in which prices rose a fifth or
more (Reinhart and Rogoff's own measure, applied to years; for a year read monthly, the mean of its twelve-month
changes is our adaptation, the card's "as they apply it" meaning the line, not this computation; a unit read by several
economies takes their mean). It was added after C23's results, because the count of crises begun was being read as a
count of crisis years; the shares were seen
before the card was written, as its `seen` field says.

Each crisis of prices rising a fifth or more in a year (Reinhart and Rogoff's line for an inflation crisis), counted
once at the date it began (the count is of crises begun, not of years spent in crisis; Reinhart and Rogoff count years,
so the line is theirs and the measure an adaptation of ours), in the
panel built for this series as frame b (`data/reconstructed/ft001-b`, built under the rules in
`protocols/FT-001-M0-rules.md`, its build in `protocols/FT-001-M3-panel.md`). The code rebuilds the panel in memory
from the frozen sources and refuses to count if its digest differs from the manifest's. Consumer prices where they
were kept, a commodity or wholesale index before, as Reinhart and Rogoff's files hold them; a monthly series crosses
the line when three successive twelve-month readings are a fifth or more, our adaptation. Each crossing goes to its era
by the date it began: before 1914, 1914 to July 1971, from August 1971 (an annual 1971 reading to the middle era).

The unit counted is a money, not an economy: the euro from each member's entry; a monetary union (the two CFA francs,
the East Caribbean dollar) counted once, a member's year being the union's when Ilzetzki, Reinhart and Rogoff class it
as having no separate legal tender; crossings of union members within twelve months of the first counted as one, and
the CFA francs' devaluation of January 1994 as one event. An economy using another state's money (in their classes, or
in the IMF's AREAER for four economies their files do not cover: Timor-Leste, Kosovo, Nauru, Tuvalu) is set apart,
its money not having lost at home, and its years leave the count of money-years. Shared colonial monies with no unit
in the panel are counted nowhere. The card lists every exception by name.

| Era | Crossings | Money-years | Monies | Per hundred money-years | With the crossings that cannot be dated | Monies with one | Consumer prices only |
|---|---|---|---|---|---|---|---|
| Before 1914 | 166 | 3,589 | 43 | 4.6 | 4.9 | 77% | 3.7 |
| 1914 to July 1971 | 101 | 3,452 | 100 | 2.9 | 3.3 | 57% | 2.9 |
| From August 1971 | 158 | 7,024 | 168 | 2.2 | 2.6 | 58% | 2.2 |

Before 1900 most readings are annual and many are commodity prices, which swing more than consumer prices; the
consumer-only column is the variant for that. The crossings frame b leaves apart (the post-Soviet hyperinflations among
them) and the five set apart as another state's money are named in the run. Counted in (a variant added after a review
asked for it, with the card's rules on shared monies and on monetary unions applied to them: a crossing in a year classed as another
state's money, and a CFA member's inside the 1994 devaluation's window, left out), they give 4.9,
3.3 and 2.6 crises per hundred money-years, the same order; the frame's unit rule counts Czechia and Slovakia separately in January 1991, Croatia separately in 1986, and
South Sudan's 2008 crossing as its own money's, though it used Sudan's pound until 2011; merged, they would change the last rate
only in its second decimal. No count of recoveries is made: the list
of new units monies took after a collapse could not be made complete from the sources in hand, so recoveries are told
as cases. The dollar's consumer prices have not crossed the line since 1920 on the same panel.

| Era | Money-years | Share of money-years in a crisis (C29) | Consumer prices only |
|---|---|---|---|
| Before 1914 | 3,589 | 6.9% | 5.2% |
| 1914 to July 1971 | 3,452 | 11.0% | 10.8% |
| From August 1971 | 7,024 | 13.8% | 13.8% |

A crisis cannot be dated when a money's record begins during it, or starts again after a gap. After July 1971, 26 crises could not be dated, among them the hyperinflations that followed the end of the Soviet Union. Counted with them or without them, the order of the rates holds, and so does the reading that later crises lasted longer.

That later crises lasted longer is our reading of the two cards together (fewer begun, more years spent in one), not a
third measure. The spans are dates, not monetary systems.

## CS-D

**Prices under a metal standard and under paper, 1870–2020** (`cards/C19-cs-b-inflation-by-convertibility.yaml`,
`cards/C20-cs-b-without-hyperinflation-years.yaml`, `code/cs_b.py`, `code/cs_b_trim.py`, the runs in
`results/runs/`; reused).

Each year of seventeen rich economies is classed convertible or paper by Bordo and Schwartz's `Table 1A` (transcribed
twice and compared cell by cell, `data/reconstructed/ft001-cs-tables`), on the Macrohistory Database's consumer
prices; war years and the fixed-rate years of 1946–71 are classes of their own. `C20` corrects `C19` by setting apart
the 8 economy-years above a hundred per cent a year: the threshold is `C19`'s, fixed before its run;
setting those years apart was chosen after `C19`'s mean was seen, and is said so. The main result:
0.1% a year in 700 convertible years, 3.7% in 1,166
paper years, a gap of 3.6 points (1.9 to 5.7).

Every variant, each with its interval:

| Variant | Gap, points a year | Interval |
|---|---|---|
| Medians, every year kept | 2.3 | 1.3 to 4.1 |
| Log rates | 3.4 | 1.8 to 5.4 |
| Paper years from 1972 only | 4.3 | 2.1 to 7.1 |
| Transition years left out | 3.6 | 1.9 to 5.7 |
| Returns read in their own block only | 3.7 | 2.0 to 5.9 |
| Earlier resumption dates | 3.7 | 2.0 to 5.8 |
| Marked suspensions as paper | 3.6 | 1.9 to 5.7 |

The variants are reported whole and read the same; they are not votes. By era: before 1914, convertible years
0.4% and paper years 0.3%; between the wars,
-1.6% and 2.7%; the fixed-rate years of 1946–71,
5.2%; paper years since 1972, 4.4%. The classes are regime and
era together, and the panel is today's rich economies, which pulls the paper mean down.

## CS-E

**The greenback's and the paper pound's price in gold** (the A3 build, `data/reconstructed/ft001-a3`, its protocol in
`protocols/FT-001-M4-A3-premiums.md`; reused).

The greenback's price in gold month by month, 1862–78, from Mitchell's Table 2 (1908); the paper pound's year by year,
1800–21, from Tooke's tables, read on the page images (the copies are listed under `data/archive-a3/`). A second run of the
model re-read about a tenth of the values blind on the images; all agreed but one, that run's own slip, settled on the
image. Tooke's annual table repeats one year's row in the next and disagrees with itself in 1812: both his tables
are drawn and those years marked. The greenback fell to 39% of its gold value at its low and the
paper pound to 75%; both returned to par (1878 and 1821).

## CS-F

**Consumer prices after leaving gold, 1932–34** (`cards/C18-cs-a-consumer-prices-off-gold.yaml`, `code/cs_a.py`,
`results/runs/C18-cs-a-consumer-prices-off-gold.json`; reused).

The consumer-price inflation of the economies Bernanke and James count as off gold, against those still on it, by
their dates (their Table 2.1, transcribed twice), on the Macrohistory Database: 45 economy-years,
pooled. The difference is 3.8 points a year (-3.1 to 11), bounded. Without the exits by
exchange control: 4.1 (-2.7 to
11.0); without Spain: 3.8
(-2.8 to 10.3). Bernanke and James's own
result, on wholesale prices, is theirs, cited beside it.

## Details from the study

The study's text sends these details here; each keeps its claim.

- Japan, 1945 and 1946. On the Bank of Japan's Tokyo index of retail prices, the first doubling took two months or less: to double in two months, prices must rise by about two-fifths a month on average, and faster if the doubling took less time. The second doubling took three months, about a quarter a month. The yearly figures (van Leeuwen's series, as the Macrohistory Database carries it) and the Tokyo index show the rise in different months; the Tokyo index does not confirm the yearly series' jump in 1945, so the study does not print the yearly figure for that year.
- Britain, 1800. The study quotes Reinhart and Rogoff's data for Britain's consumer prices; the BIS's long series, a different compilation of the same years, gives 34%.
- Britain, 1975. The study quotes the consumer-price index; retail prices, a different index, rose 24%.
- Austria, 1914 to 1918. The government's debts to the central bank are given in crowns at face value; Garber and Spencer's table (1994) names its unit "gold crowns".
- Deficits and inflation. Catão and Terrones (2005) treat inflation as a tax on people who hold money, because it cuts what their money buys. They compare deficits with the amount of money that this inflation tax falls on, and they separate the short run from the long run.
- The dollar's share of reserves. The share at the end of 2024 is measured with exchange rates held fixed, so that it does not change just because the dollar rises or falls against other currencies (the ECB's The international role of the euro, June 2025 and June 2026).
- What central banks weigh in choosing a reserve currency. Eichengreen, Chiţu and Mehl (2016) use the size of the issuer's economy to measure how much a money gains from being used by many others.
- Massachusetts, 1690 and 1691. In Grubb's words (2012), the war issues of 1690 and 1691 were "primarily linked to redemption via future tax payment obligations legislated concurrently".
- Deficits and inflation where inflation is low. In Fischer, Sahay and Végh's words (2002), there is "no obvious long- or short-run relationship" between deficits and inflation.
- Bolivia, 1984 and 1985. The central bank also repaid foreign debts on the Treasury's behalf (Sachs 1986).
- The Fed, 1950. In the autumn of 1950 the Treasury replaced maturing debt with new debt. In Eichengreen and Garber's words (1991), the Fed "was forced to purchase the majority of" this new debt.
- Japan, 1932 to 1949. In Iwata's words (2013), what led to the hyperinflation after the war was "not the Takahashi Economic Policy itself".
- Japan, 1932 to 1949: the two readings. In Iwata's words (2013), after Takahashi died, "the Bank's underwriting of government securities was mismanaged, which led to hyperinflation after World War II". Shirakawa (2011) said that at first the Bank promptly sold most of the bonds it had underwritten, and the money it issued did not grow much.
- Britain, 1914 to 1918. In Moggridge's words (1972, p. 17), Britain "settled down for the duration with the gold standard legally intact".
- The United States, 1917 to 1919. At home, gold "continued to circulate freely", while exports were "permitted under license". The ban on gold exports was made under an act of Congress of June 1917, and announced on the 7th of September 1917 (Silber 2007; the Federal Reserve Bulletin of October 1919; the Federal Reserve Board's Fourth Annual Report, for 1917).
- Hong Kong, since 2005. Since May 2005 the Hong Kong Monetary Authority has stood ready to trade US dollars at two set rates, 7.75 and 7.85 Hong Kong dollars per US dollar, which keeps the exchange rate between them [HKMA](https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/milestones-of-monetary-reform/) ('Milestones of Monetary Reform') [HKMA](https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/how-does-the-lers-work/) ('How does the LERS work?').
- The Fed's rule before and after 1979. In the estimates of Clarida and co-authors, as Woodford (2003) reports them, the Fed's rule for 1960 to 1979 responds too little to inflation, and the rule for 1982 to 1996 meets the Taylor principle.
- The Fed, October 1979. In the Federal Reserve Bulletin's words (October 1979), the Fed began "placing greater emphasis in day-to-day operations on the supply of bank reserves".

## Other cases and sources, by section of the study

The study's text keeps one source at the end of each sentence and sends the others here, under the section they
serve, with the cases it does not keep open; each keeps its claim.

### What is a money's value, and how much has it lost? Other cases and sources

- The Reichsmark in the first case study. In the table, the Reichsmark's figures start in 1924 and the Deutsche Mark's in 1949. Germany's currency reform of June 1948 changed old money into new at several rates. So the Reichsmark cannot be linked to the Deutsche Mark by a single rate [Mendershausen 1949](#sources) (p. 658 and its note: first allotments one to one, later amounts debited nine times over), and it is shown as a money of its own. For the Reichsmark, the slider shows what it would buy in 1947.
- The euro area's own index. The euro area's own price index, kept since 1990, gives about the same loss as Germany's prices, and a larger one than France's.
- The gold bloc in 1935. The passage on the countries that stayed on gold after 1931 also rests on [Eichengreen and Sachs 1985](https://www.nber.org/system/files/working_papers/w1498/w1498.pdf) (p. 9).

### Why do people take a money? Other sources

- Money held by convention. The passage on Samuelson's and Kiyotaki and Wright's models also rests on [Luther and White 2011](https://www.mercatus.org/sites/default/files/d7/positively-valued-fiat-money-after-the-sovereign-disappears.pdf) (pp. 18–19).

### Why were some monies destroyed? Other sources

- The United States, 1946 and 1947. The passage on prices after the end of wartime controls also rests on [Eichengreen and Garber 1991](https://www.nber.org/system/files/chapters/c11485/c11485.pdf) (p. 183).
- Japan, 1932 to 1936. The passage on the Bank of Japan's underwriting and Takahashi also rests on [Hirayama and Noda 2021](https://arxiv.org/pdf/2008.00860) (about p. 10).

### How did a money hold its value, and how did its backing end? Other cases and sources

- Hong Kong, since 1983. A currency board can also hold. Hong Kong has run one since October 1983 [HKMA](https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/milestones-of-monetary-reform/) ('Milestones of Monetary Reform'). All the money issued under the board is fully backed by assets in US dollars, at a fixed rate [HKMA](https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/how-does-the-lers-work/) ('How does the LERS work?'). A backing protects a money only as long as the state keeps it.
- The United States, 1917 to 1919. The passage on the ban on gold exports also rests on [Silber 2007](#sources) (When Washington Shut Down Wall Street, p. 168; a book, listed in the methods' sources).
- The mandat, 1796 and 1797. The passage on the mandat also rests on [White 1995](#sources) (p. 247; listed in the methods' sources).
- Leaving gold after 1931. The passage on prices and output in the countries that left gold also rests on [Bernanke and James 1991](https://www.nber.org/system/files/chapters/c11482/c11482.pdf) (p. 42).
- Italy in the 1970s. The passage on the lira, the yen and the pound in the 1970s also rests on [IMF IFS](https://db.nomics.world/IMF/IFS) (consumer prices, Italy, through DBnomics; the price panel in the methods).
- Turkey's inflation targeting. The passage on its adoption also rests on [Yilmaz 2006](https://www.bis.org/speeches/20061002-economic-outlook-turkey.pdf) (pp. 1–2).

### Do today's monies have the two supports? Other sources

- The Swiss franc. The passage on what the Swiss National Bank may not do also rests on [Hildebrand 2011](https://www.bis.org/speeches/20110623-independence-swiss-national-bank.pdf) (p. 3).
- Dollar stablecoins. The passage on the GENIUS Act and the BIS's tests also rests on [Federal Reserve 2026](https://www.federalreserve.gov/newsevents/pressreleases/files/bcreg20260924a1.pdf) (staff memo on the proposed rule, p. 2).
- A digital euro. The passage on the digital euro also rests on [ECB](https://www.ecb.europa.eu/euro/digital_euro/html/index.en.html) ('Digital euro' page).

## Robustness, chosen by risk

| Risk | Addressed by |
|---|---|
| A case entering by its outcome | the told cases chosen by their support and sources, held and broken alike, and read as existence, never as a rate; the converse cases told beside the destroyed ones |
| A money's loss read off one index's quirks | one source for CS-A (the BIS long series); the euro area's own index beside its two carriers (`C21`) |
| A unit change read as a loss | chaining by official factors; the 1948 reform not chained, the Reichsmark shown apart (`C21`) |
| Price controls hiding a loss | said for the Reichsmark; the levels read official prices, said once in the study |
| Commodity indices inflating early counts | the consumer-only variant beside every rate (`C23`) |
| Crises begun read as years in crisis | the share of money-years in a crisis counted beside, on the same money-years (`C24`) |
| Shared monies counted many times | the euro and each union once, events and years alike; another state's money set apart (`C23`) |
| A few hyperinflation years driving a mean | medians and log rates beside the means; years above a hundred per cent set apart (`C20`) |
| Eras confounding the classes | the gap printed by era (`C20`); said beside the conclusion in the study |
| Dates of convertibility misread | two transcriptions compared cell by cell; earlier resumption dates and marked suspensions as variants (`C19`, `C20`) |
| Exits by exchange control pooled with suspensions | a variant without them (`C18`) |
| A real rise confused with an inflation gap | the split in logs fixed before the data were read (`C22`) |
| Point-in-time (what was knowable when) | n/a because the study draws no investor rule and no scenario |

## Model steps the methods rely on

The convertibility dates of Bordo and Schwartz's `Table 1A` and the exits of Bernanke and James's Table 2.1 were
transcribed on the page images by separate runs of one language model (Claude), which are not independent
coders, and compared cell by cell.
The prices of gold in Mitchell's and Tooke's tables were transcribed on the page images by runs of the same model, and
a sample re-read blind by a second run.
The economies using another state's money that Ilzetzki, Reinhart and Rogoff's files do not cover were read from the
IMF's AREAER by a run of a language model (Claude) and verified by an isolated check (Claude).
The passages cited in the register were read at their pages by runs of a language model (Claude), and the study's notes name which run read each.
The isolated checks this text cites are separate runs of a language model (Claude), none of them
a run that made what it checked.
Each agreement printed measures how far runs of a model agree, not two people; runs of one model share their biases,
so their agreement is weaker evidence than two people's.

## The research log

The order of work, the checks and their answers are kept with the study's working files and are not public: the step record, the
reports of the checks and their answers, and the notes (the harvest, the sources and their passages, the gaps).

This part was rebuilt on 2026-10-10 from its brief under the series design of three parts, every step run again
and each piece of earlier work reused only where a rerun would produce the same. Reused: the frozen data; frame b's
panel and the A3 build; the cards `C18`, `C19` and `C20` with their runs; and the passages already read at their pages.
New: the map and the dossier of this part; the cards `C21`, `C22` and `C23` (fixed in place before any run, the fixes named in their history) and `C24` (added after C23's results, its `seen` field naming what was seen); the register's claims, each sourced passage
read; and the study's text.

One departure from the earlier design is named: what stood behind destroyed monies moved from the headline to the
body, as context told in the sources' words, because the sources' finding is theirs and the study's cases cannot test
it. The runs `C23` to `C29` are withheld from this copy, since they rest on values that are not republished
in bulk (see `WITHHELD.md`); the code regenerates them from the frozen series.

**Correction, 22 October 2026 (the error found on 21 October).** The IMF's consumer price index for Kazakhstan (International Financial Statistics,
`PCPI_IX`, monthly and annual, frozen on 30 September 2026) changes units in January 2020: it doubles in one month, with
no flag or note. The World Bank's index (World Bank, World Development Indicators, `FP.CPI.TOTL`, frozen on 30 September
2026) is the same series through 2019 and runs 1.9427 times below the IMF's from 2020, a ratio that holds
within half a percent through 2024, so it was a change of units, not of prices. Our list of breaks counted it as a
crisis begun in January 2020. The panel now reads the IMF's index for Kazakhstan from January 2020 divided by that
ratio, computed from the two frozen files (the toolkit's `ft.data.splices`, not in this repository), and every count was rerun by its own code
(cards `C28` and `C29`). With the correction, Kazakhstan in 2020 is no longer a crisis, and Kazakhstan's crossing of
December 2022 (20.4% over twelve months) is one; the printed counts do not change
(158 crises begun from August 1971, 2.2 per hundred money-years,
13.8% of money-years in a crisis). Before the IMF's monthly index feeds any count, a check now holds the IMF's monthly index of every money against the World Bank's annual index, for one-month moves of roughly a quarter or more, far larger than the series' usual monthly moves of the previous five years (the toolkit's `ft.quant.jumps`, not in this repository; the BIS's monthly series, which feeds a few counts, and the US and euro-area indices are not screened): a move the World Bank does not confirm stops the run unless it is named with its reason. The other moves it names are left as the IMF reads them: Myanmar's in January 1973 and Congo's (Democratic Republic) in January 2010, both flagged for a separate correction, and Palestine's in 2025 and Zimbabwe's in June 2023, read as price moves (our reading, not checked against a source). Under that reading, Myanmar's crisis of the 1970s stays dated January 1974 in our list of breaks, from the IMF's monthly index; no printed count depends on Myanmar's date, since both of its readings fall after July 1971. Congo's index is read as the IMF prints it, and the rate in the text rests on that reading: read the other way, with Congo's 2009 and 2010 left without a price reading, the money-years from August 1971 would be 7,022 instead of 7,024, and the rate of crises begun from August 1971 would round to 2.3 (2.2501) instead of 2.2 (2.2494), the count of 158 unchanged: a knife-edge. A separate correction of Congo's index is proposed. The check is not exhaustive: smaller moves pass unseen, and so do a move across a gap in a series and any move in a series' first twelve months, and the World Bank's index often derives from the same IMF data, so its agreement is not an independent confirmation. Separately, a fault of rounding,
not of data: the chart's tooltip rounded a rate that was already rounded, and could show a tenth more than the text;
it now rounds once, from the rate kept to four decimals.

## Sources

<!-- numbers:off -->
**Works read at the passage cited** (the page, table or section of each is in the register's `claims`):

- Auer, R., A. Burstein and S. Lein (2021). Exchange Rates and Prices: Evidence from the 2015 Swiss Franc Appreciation. NBER WP 28404.
- Ball, L. and N. Sheridan (2003). Does Inflation Targeting Matter? NBER WP 9577.
- Bank for International Settlements (2018). Annual Economic Report 2018, ch. V, Cryptocurrencies: looking beyond the hype.
- Bank of Japan (2026). Basic Figures, Flow of Funds for the Second Quarter of 2026 (Preliminary); Statement on Monetary Policy of 31 July 2024.
- Beckerman, P. and A. Solimano, eds. (2002). Crisis and Dollarization in Ecuador. World Bank.
- Bernanke, B. and H. James (1991). The Gold Standard, Deflation, and Financial Crisis in the Great Depression. In Hubbard, ed., Financial Markets and Financial Crises. NBER.
- Blanchard, O. (2017). Macroeconomics, 7th ed. Pearson.
- Bordo, M. (1981). The Classical Gold Standard: Some Lessons for Today. Federal Reserve Bank of St. Louis Review, May.
- Bordo, M. (1992). The Bretton Woods International Monetary System: An Historical Overview. NBER WP 4033.
- Bordo, M., O. Bush and R. Thomas (2025). Muddling through or tunnelling through? Bank of England Staff Working Paper.
- Bordo, M. and H. Rockoff (1995). The Gold Standard as a Good Housekeeping Seal of Approval. NBER WP 5340.
- Bordo, M. and A. Schwartz (1994). The Specie Standard as a Contingent Rule. NBER WP 4860.
- Boz, E., C. Casas, G. Georgiadis, G. Gopinath, H. Le Mezo, A. Mehl and T. Nguyen (2020). Patterns in Invoicing Currency in Global Trade. IMF WP/20/126.
- Buiter, W. (2007). Seigniorage. NBER WP 12919. Read for the glossary's two senses of the word.
- Butcher, K. and M. Ponting (2014). The Metallurgy of Roman Silver Coinage: From the Reform of Nero to the Reform of Trajan. Cambridge University Press (Table 19.4).
- Cagan, P. (1956). The Monetary Dynamics of Hyperinflation. In Friedman, ed., Studies in the Quantity Theory of Money. Chicago.
- Calomiris, C. (1988). Price and Exchange Rate Determination during the Greenback Suspension. Oxford Economic Papers 40(4).
- Calomiris, C. and S. Haber (2014). Fragile by Design. Princeton.
- Catão, L. and M. Terrones (2005). Fiscal Deficits and Inflation. Journal of Monetary Economics 52: 529-554. A held copy.
- Cochrane, J. (2000). Money as Stock: Price Level Determination with no Money Demand. NBER WP 7498.
- De Grauwe, P. and M. Polan (2005). Is Inflation Always and Everywhere a Monetary Phenomenon? Scandinavian Journal of Economics 107(2).
- De Santis, R. (2015). A Measure of Redenomination Risk. ECB Working Paper 1785.
- de la Torre, A., E. Levy Yeyati and S. Schmukler (2003). Living and Dying with Hard Pegs. World Bank.
- Eggertsson, G. (2006). Fiscal Multipliers and Policy Coordination. Federal Reserve Bank of New York Staff Report 241.
- Eichengreen, B. and M. Flandreau (2008). The Rise and Fall of the Dollar, or When Did the Dollar Replace Sterling as the Leading International Currency? NBER WP 14154.
- Eichengreen, B. and M. Flandreau (2009). The rise and fall of the dollar (or when did the dollar replace sterling as the leading reserve currency?). European Review of Economic History 13(3): 377-411. A held copy.
- Eichengreen, B., L. Chiţu and A. Mehl (2016). Stability or Upheaval? The Currency Composition of International Reserves in the Long Run. IMF Economic Review 64(2): 354-380. A held copy.
- Eichengreen, B. and P. Garber (1991). Before the Accord: U.S. Monetary-Financial Policy, 1945–51. In Hubbard, ed. NBER.
- Eichengreen, B. and J. Sachs (1985). Exchange Rates and Economic Recovery in the 1930s. NBER WP 1498.
- Erb, C. and C. Harvey (2013). The Golden Dilemma. NBER WP 18706.
- European Central Bank. Press releases of 21 July 2022 (the Transmission Protection Instrument) and 26 February 2026 (the 2025 accounts).
- Federal Reserve (2025). Economic Well-Being of U.S. Households in 2024.
- Feldman, G. (1993). The Great Disorder: Politics, Economics, and Society in the German Inflation, 1914-1924. Oxford University Press. A held copy.
- Fischer, S., R. Sahay and C. Végh (2002). Modern Hyper- and High Inflations. NBER WP 8930.
- Fisher, I. (1933). The Debt-Deflation Theory of Great Depressions. Econometrica 1(4); read in its 1934 reprint.
- Foote, C., W. Block, K. Crane and S. Gray (2004). Economic Policy and Prospects in Iraq. Journal of Economic Perspectives 18(3).
- Garber, P. and M. Spencer (1994). The Dissolution of the Austro-Hungarian Empire: Lessons for Currency Reform. Princeton Essays in International Finance 191.
- Goodfriend, M. and R. King (2005). The Incredible Volcker Disinflation. NBER WP 11562.
- Grubb, F. (2012). Is Paper Money Just Paper Money? NBER WP 17997.
- Hanke, S. and N. Krus (2013). World Hyperinflations. In Parker and Whaples, eds., Routledge Handbook of Major Events in Economic History.
- Harper, K. (2016). People, Plagues, and Prices in the Roman World: The Evidence from Egypt. Journal of Economic History.
- Hirayama, K. and A. Noda (2021). Evaluating the Financial Market Function in Prewar Japan. arXiv 2008.00860.
- Holmström, B. (2015). Understanding the role of debt in the financial system. BIS Working Paper 479.
- Hoshi, T. and A. Kashyap (2001). Corporate Financing and Governance in Japan. MIT Press.
- Kiyotaki, N. and R. Wright (1993). A Search-Theoretic Approach to Monetary Economics. American Economic Review 83(1). A held copy, read at p. 68.
- Liu, J., I. Makarov and A. Schoar (2023). Anatomy of a Run: The Terra Luna Crash. NBER WP 31160.
- Ljungqvist, L. and T. Sargent (2012). Recursive Macroeconomic Theory, 3rd ed. MIT Press.
- Luther, W. and L. White (2011). Positively Valued Fiat Money after the Sovereign Disappears. Mercatus Center.
- McCabe, P. (2010). The Cross Section of Money Market Fund Risks and Financial Crises. FEDS 2010-51.
- Mendershausen, H. (1949). Prices, Money and the Distribution of Goods in Postwar Germany.
- Moggridge, D. (1972). British Monetary Policy 1924–1931: The Norman Conquest of $4.86. Cambridge.
- Obstfeld, M. and K. Rogoff (1983). Speculative Hyperinflations in Maximizing Models: Can We Rule Them Out? Journal of Political Economy 91(4): 675-687. A held copy.
- Reinhart, C., K. Rogoff and M. Savastano (2003). Addicted to Dollars. NBER WP 10015.
- Reinhart, C. and K. Rogoff (2009). This Time Is Different. Princeton.
- Rockoff, H. (1981). Price and Wage Controls in Four Wartime Periods. Journal of Economic History 41(2).
- Rodgers, P. (1998). The Bank of England Act. Bank of England Quarterly Bulletin 1998 Q2.
- Rogoff, K. (1996). The Purchasing Power Parity Puzzle. Journal of Economic Literature 34(2).
- Romer, D. (1996). Advanced Macroeconomics. McGraw-Hill.
- Sachs, J. (1986). The Bolivian Hyperinflation and Stabilization. NBER WP 2073.
- Samuelson, P. (1958). An Exact Consumption-Loan Model of Interest with or without the Social Contrivance of Money. Journal of Political Economy 66(6). A held copy, read at pp. 481-482.
- Sargent, T. (1982). The Ends of Four Big Inflations. In Hall, ed., Inflation: Causes and Effects. NBER.
- Sargent, T. and F. Velde (1995). Macroeconomic Features of the French Revolution. Journal of Political Economy 103(3).
- Shiller, R. (1996). Why Do People Dislike Inflation? NBER WP 5539.
- Silber, W. (2007). When Washington Shut Down Wall Street. Princeton.
- Stantcheva, S. (2024). Why Do We Dislike Inflation? NBER WP 32300.
- Starr, R. M. (1974). The Price of Money in a Pure Exchange Monetary Economy with Taxation. Econometrica 42(1): 45-54. A held copy.
- Tooke, T. (1838). A History of Prices, vols. 1 and 2. London: Longman.
- Velde, F. and D. Weir (1992). The Financial Market and Government Debt Policy in France, 1746–1793. Journal of Economic History.
- von Glahn, R. (1996). Fountain of Fortune: Money and Monetary Policy in China, 1000–1700. California.
- Walsh, C. (2010). Monetary Theory and Policy, 3rd ed. MIT Press.
- White, E. (1995). The French Revolution and the Politics of Government Finance, 1770–1815. Journal of Economic History.
- Willard, K., T. Guinnane and H. Rosen (1995). Turning Points in the Civil War: Views from the Greenback Market. NBER WP 5381.
- Woodford, M. (2003). Interest and Prices. Princeton.
- World Bank (2010). Zimbabwe Public Expenditure Notes (Report No. 72004).
- World Bank (2021). Zimbabwe Economic Update, Issue 3.

**Official documents read**: the Bank of England's explainer on its independence; the Bank of Japan Act (Act No. 89 of 1997, Articles 2, 34 and 46), in the Bank of Japan's Functions and Operations; the Bank of Japan's statements of 21
September 2016 and 19 March 2024 and Governor Shirakawa's speech of 16 June 2011; the BIS's 30th and 44th Annual
Reports, its Quarterly Review of September 2011 and its Annual Economic Report 2025, chapter III; central bankers'
speeches posted by the BIS (Danthine 2015, Hildebrand 2011, Iwata 2013, Jordan 2015 and 2023, Kavcıoğlu 2023, Schlegel
2025, Yilmaz 2006); Draghi's speech of 26 July 2012; the ECB's pages on its inflation target, on cash, on the digital
euro and on the Turkish lira, its strategy statement (2021), The Monetary Policy of the ECB (2011, with the Treaty), the
Statute of the ESCB, The international role of the euro (June 2025 and June 2026) and Virtual Currency Schemes (2012);
the Federal Reserve Act's sections 2A and 14, the Fed's FAQs on cash and on its securities purchases, the FOMC's
Statement on Longer-Run Goals, the Federal Reserve Board's Fourth Annual Report (1917), the Federal Reserve Bulletin of
October 1919 and of October 1979, the Financial Stability Report of May 2023
and a staff memo of September 2026; the GENIUS Act (S. 1582); the HKMA's pages on the Linked Exchange Rate System; the
OECD's Economic Surveys of Switzerland (2015) and Türkiye (2023); the Swiss National Bank's page on its legal
framework.

**Data** (each manifest under `data/`): the BIS's long consumer prices, exchange rates and effective exchange rates;
the World Bank's consumer prices, price-level factors, market rates and exports; the Jordà-Schularick-Taylor
Macrohistory Database (R6); Reinhart and Rogoff's inflation files; the IMF's International Financial Statistics and
World Economic Outlook (through DBnomics); Ilzetzki, Reinhart and Rogoff's classifications; the IMF's AREAER; the Bank
of England's Millennium of Macroeconomic Data; the BLS's CPI-U (CUUR0000SA0, the original of FRED's CPIAUCNS, read over the dates of FRED's copy; the author, 2026-10-21); FRED's FYGFGDQ188S and FYOIGDA188S (FRED's ratios to GDP of the OMB's tables, which were not available to us at their source) and CBBTCUSD (Coinbase's price, which no agency publishes); the BIS's policy rates (WS_CBPOL); and the page images behind the A3 build. The
reconstructed sets ship their manifests only, their rows carrying values from other publishers' datasets.

Named as positions, through the works that report them: Knapp; Goodhart; Menger; Kocherlakota and
Phelan; Kocherlakota; Sargent and Wallace; Leeper and Leith; Clarida, Galí and Gertler; Taylor; Orphanides; Meese and Rogoff.
<!-- numbers:on -->

## How to reproduce every figure and every number

Every number in this folder and in the web study is read from the register (`results/numbers.json`), which names for
each number the script that computed it or the source and page it is cited from. From the study's folder, `code/run.py`
runs the three cards of the rebuild (`p1_cs_a.py`, `p1_cs_b.py`, `p1_cs_c.py`; each refuses a card changed since it was
committed), writes the register (`p1_registry.py`, from the runs, the reused builds, `p1_cited.yaml` for the numbers
cited at their pages and `p1_claims.yaml` for the sourced claims), draws the web study's figures and slider
(`p1_figures.py`) and its preview image (`p1_og.py`). The reused cards ran once at their own step (`cs_a.py`, `cs_b.py`,
`cs_b_trim.py`), each refusing a changed card. Also published: the cards (`cards/`), the results (`results/runs/`, the
three withheld runs apart), the rules and build protocols (`protocols/`) and the manifest of every dataset read
(`data/`).

Not investment advice.
