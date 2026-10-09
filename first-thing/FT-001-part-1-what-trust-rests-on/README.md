# Does a money lose its value when its backing goes? — methods and proof

*A First Thing Weekly Study · FT-001, part 1 of "The life of a money" · as of 2026-10-08*

This folder is the proof behind the study published on First Thing's site, for the sceptic and the specialist: what
each claim rests on, what was fixed before each result, what ran, what each result means and what it does not, where
the data come from, and the code. It is not the study: the study, with its argument, its charts and its calculator,
is on the site.

Reproduction level: read the code

The code is published here and every number names the script that computed it or the source it is cited from, but
the code calls a small shared toolkit of ours (the register of numbers, the charts, the data readers) that is not in
this repository, and the fetched series are not republished (each manifest says where to fetch them, when they were
fetched and their hash). So the code can be read and every source traced; it cannot be rerun from this folder alone.

## What each claim rests on

The study answers its question in eight components. Every claim it makes is in the register of numbers
(`results/numbers.json`, its `claims`), with its evidence type, the component it serves, and either the passages it
rests on (each with its page, table or section, and how deeply the work was read) or the card of the analysis that
measured it. Four types are used: **established** (a documented fact or mechanism, cited at its passage), **cases**
(shown in history, with sources), **measured** (an analysis of ours, with its card or the protocol its build ran)
and **judgement** (our reading, said as ours). The headline is a judgement weighing three components: the long-run
record of inflation with and without a backing (established), the backed money that lost half its purchasing power
(cases, frozen data), and the monies that held or collapsed whatever stood behind them (cases). No measurement of ours
enters it.

Six analyses of ours are case studies inside the study, each beside the component it supports; none carries the
answer alone, and each component rests on its sources first.

| Case study | Component | What ran | Card or protocol | Its parent | New in this run? |
|---|---|---|---|---|---|
| CS-A, leaving gold on consumer prices | K3 (context) | `C18-cs-a-consumer-prices-off-gold` | `cards/C18…` | — | yes |
| CS-B, convertible and inconvertible years | K4 (context) | `C19-cs-b-inflation-by-convertibility`, then `C20-cs-b-without-hyperinflation-years` | `cards/C19…`, `cards/C20…` | `C20`'s is `C19` (a correction) | yes |
| CS-C, two suspensions priced on the return to gold | K1 (context) | A3's second build | `protocols/FT-001-M4-A3-premiums.md` | — | reused |
| CS-D, a missed payment before a money crisis | K7 (context) | `C16-cs-d-default-ratio` | `cards/C16…` | `C15-claim1-institution-m0` (an extension) | yes |
| CS-E, who may redeem a stablecoin | K8 (context) | `C14-now-institution-m0`; `C17-cs-e-second-model`, void | `cards/C14…`, `cards/C17…` | `C14`'s chain from `C06`; `C17`'s is `C14` | `C14` reused, `C17` run |
| CS-F, independence and inflation targets | K6 (context) | frame a's fifth build, its independence and inflation-target panels | `protocols/FT-001-M4-frame-a.md` | — | reused |

Every card in `cards/` was committed before any result on its data existed; the code refuses to run a card changed
since its commit, and each result in `results/runs/` names its card's hash. A card first committed after a result on
the same data names what it saw (`seen`) and whether it is a correction, an extension or an exploration (`kind`).

**The reused builds and the version of their protocol.** CS-C is A3's second build (`139c8e56`), which ran the A3
protocol as of `c0162713`; that protocol's last three sections were written after the first build was seen, said there,
and its text changed once more at `dabda6bd` with the answers to the build's narrow recheck. CS-F is frame a's fifth
build (`a78fbf95`), which ran frame a's protocol as of `5dcbcaab`, unchanged since; its last three sections were written
after earlier builds were seen. Between the fourth and fifth builds the inflation-target panel changed, said in the build's manifest. CS-E's `C14` and CS-D's parent `C15` were reused from the study's first
run; their children test them (`C16` refuses to run unless it rebuilds `C15`'s counts to the unit).

## The readings, and the size that matters

Each measured result is read against the size that matters fixed on its card: an **effect** (its range excludes no
difference and is not wholly inside the size that matters), **too small to matter** (its range lies wholly inside
it), or **bounded** (its range holds no difference and reaches past the size that matters), reported as what it
excludes. The new cards of this run (`C16` to `C20`) wrote the rule more strictly, as "an effect only if the range's
near end lies beyond the size that matters"; the register keeps the workshop's rule, and no result of this part reads
differently under the two.

**Sizes that matter set after the results.** For `C14` and `C15`, written before cards held a size that matters, it
was set on 2026-10-07 from the reader's question, after their results had been seen. For `C16`, the ratio's size that
matters (half as often again, either way: 1.5) was set after the map's audits had recomputed the ratio,
and the card says so. `C18`, `C19` and `C20` fixed theirs, one point of inflation a year, before their runs. CS-A was
designed after an earlier analysis (A2's second panel) had read these economies' consumer prices around their exits,
and an auditor had printed their changes for 1932 to 1934; it is therefore context, never the headline.

## CS-A

*Leaving gold, on consumer prices.*

`C18` takes Bernanke and James's list and dates of exits from gold (their Table 2.1, transcribed for this study; the
transcription's manifest is in `data/reconstructed/ft001-cs-tables`, its values at the table's page) for the 15 economies the Macrohistory Database covers, classes each year off or on gold (a mid-year exit weighted by its months, as their notes do), and takes the mean consumer-price
inflation off gold less the mean on gold, pooled over 1932 to 1934 by year weights. The range is built from the noise
of the calm years 1925 to 1929, with a variant that doubles it.

- Pooled 1932 to 1934: 3.8 points a year, range -3.1 to 10.7 (half-width 6.9;
  doubled noise, 13.8). Bounded: it excludes a gap above 10.7 points a year.
- Without the leavers by exchange control alone: 4.1, range -2.7 to
  11.0. Without Spain, never on gold: 3.8, range -2.8 to 10.3.
- By year, described and never read: 2.9 in 1931, and 4.6, 1.4 and
  4.1 in the pooled years. The years before 1931 and after 1934 are not shown: one side then rests on
  two or three economies, which comes close to printing a single economy's Macrohistory value.

Bernanke and James's own result is on wholesale prices; CS-A shows that consumer prices do not contradict it. The
leavers chose when to leave, largely by their experience of the 1920s (Eichengreen and Sachs, p. 10); that a worse
deflation hastened some exits is a possible selection, our reading. The comparison is not checked outside the
economies that built it: League of Nations consumer prices for other economies were not in hand.

## CS-B

*Convertible and inconvertible years.*

`C19` classes every year of 17 rich economies of the Macrohistory Database (its eighteen but Ireland,
which Bordo and Schwartz's dated chronology does not class), 1870 to 2020, as convertible into gold or inconvertible by Bordo
and Schwartz's dated chronology, with war years and the Bretton Woods years apart, and compares average consumer-price
inflation, with ranges drawn by blocks of years. Its mean gap was carried by Germany's hyperinflation years (three
years above 100% a year in the inconvertible class); the medians, 0.0 against
2.3, were not. `C20`, a correction committed after `C19`'s result and checked before its own run,
sets apart the 8 economy-years above 100% a year from the means and keeps them in the medians.

- Means: 3.7% in inconvertible years (1,166 economy-years) against 0.1% in
  convertible ones (700): a gap of 3.6, range 1.9 to
  5.7, an effect. Medians: 2.3, range 1.3 to 4.1.
- Shares of years above ten per cent: 11% inconvertible, 2% convertible. Bretton Woods
  years, apart: mean 5.2%.
- By era: 1870 to 1913, 0.3% against 0.4%; 1919 to 1938,
  2.7% against -1.6%; 1972 to 2020, inconvertible only,
  4.4%, with 0 economy-years above 100%. Within it, by each
  economy's adoption of an inflation target (`C19`'s split by adoption): from adoption 1.9%
  (143 economy-years), before it 6.4% (151), no adoption
  counted 4.5% (539; the United States and the euro members among them). The six
  adoptions dated among these economies (Canada 1991, the United Kingdom 1992, Australia and Sweden 1993, Norway 2001,
  Japan 2013) came in 1991 or later, the adoption year counted as from; over the adopters'
  own target years, year for year, the economies with no adoption counted averaged 1.7%. So the
  split describes the calendar, not what a formal target did: most of the others are euro members, whose central bank
  defines price stability by a number of its own, and the United States set a goal of its own in 2012. Finland and
  Spain targeted inflation before they adopted the euro (Hammond 2012, p. 7), but frame a could not read their dates
  (its manifest), so they sit among the economies with no adoption counted.
- The variants the card fixed, each an effect: in log rates, 3.4; without transition years,
  3.6; with earlier resumption dates, 3.7;
  with the marked suspensions counted inconvertible, 3.6; returns to gold read
  from each economy's own block only, 3.7; inconvertible years from 1972 only,
  4.3.

CS-B describes; it does not test what convertibility did. The component it sits beside (K4) rests on Rolnick and
Weber and on Bordo and Schwartz's Table 3; CS-B gives the same order of size on a panel of our own. The calculator in
the web study applies its three averages (convertible years, inconvertible years, the float since 1972) to a sum the
reader types; it computes nothing else.

## CS-C

*Two suspensions priced on the return to gold.*

A3 reads a suspended paper money's value in gold as the market's expectation of a return to par, at fixed parities
and with the long government yield as the rate (the short rate a variant), its rules fixed before any premium was
read (`protocols/FT-001-M4-A3-premiums.md`). The prices of gold in paper were transcribed from Tooke's *History of
Prices* for London and Mitchell's tables for New York.

- Britain's notes, 1797 to 1821: at their lowest year, 75% of their gold value (a premium of
  34%); the yearly odds of a return implied, 0.13 to
  0.55, a wait of 2 to 7 years.
- The greenbacks, 1862 to 1878: at their lowest month, 39%; odds in 1863 to 1869 of
  0.14 to 0.23, a wait of 4 to
  7 years. In 36 of the 48
  months between the 1875 Act and the return to gold, the premium cannot separate an expected return from the paper's
  own value, and those months are not read.

These are values in gold, never purchasing power. The dispute over what moved the greenback's gold price is named in
the study with its sides (Mitchell and Calomiris on expectations; Friedman and Schwartz on the quantity of notes).

## CS-D

*A missed payment before a money crisis.*

`C16` is a child of `C15`, which dates, for each money crisis since 1970 and each strained year in which the money
held, the acts on the study's list in the three years before (a creditor class newly in arrears in the Bank of Canada
and Bank of England's sovereign default database, a cap on central-bank lending to the state lifted, a peg dropped,
independence cut, a second money made legal). `C16` takes the population on which crises and strained years come
from the same spells of fiscal stress, and computes how many times as often a creditor class newly in arrears came
before a crisis as before a strained year that held, with a range from a bootstrap that draws whole monies (a shared
money's members drawn together), and a second by onset year beside it.

- Every crisis counted: 14 of 20 readable crises after an act, against
  513 of 923 readable strained years: a ratio of 1.26,
  range 0.70 to 1.61 (by onset year, 0.62 to
  1.67). Bounded: it excludes a factor above 1.61.
- A shared money's crises of one onset month counted once: 1.12, range
  0.67 to 1.55. Private creditors' arrears only: 0.86, range
  0.00 to 2.09. Without creditors in arrears, the other acts alone:
  0 crises after an act, no reading made. A default newly begun on the state's total debt
  only: 1 of 19 readable crises, against
  156 of 884 strained years; on all of `C15`'s crises,
  18 of 65 (28%) against 18% of strained years. Under
  this narrow count a default came before a minority of crises: "before most" holds only under the broad one.

A creditor class newly in arrears is often inside a default already running: 1,424 of the database's
1,775 dated lines fall in a year the state was already in default. Crises are events and strained years
country-years; the ratio sets each crisis against the years drawn from the same spells. The shares on all of `C15`'s
readable crises, printed in the study beside the ratio, are its earlier result, not this card's.

## CS-E

*Who may redeem a stablecoin.*

`C14` codes every stablecoin named in a fixed set of central-bank and academic papers on four lines (redemption,
reserves or a cap, supervision, the issuer taking the coin back), first from those papers and then from each issuer's
launch documents, sought for 48 coins and found and read for 47; who may redeem is
coded in two classes (any holder; verified customers only), with "not settled" where the documents leave it open.
`C17` was to have a second model code a quarter of the coins, every disagreement read at its document. Its isolation
rule, fixed on the card, voids a run whose coder reached outside its stage; both runs were void by that rule, and the
card allows no third (`results/runs/C17-cs-e-second-model.json`). CS-E therefore rests on `C14`'s codes alone.

**Which claims rest on these codes, and whether each is weight-bearing.** Two runs of one model coded `C14`'s terms
(agreement beyond chance, as a kappa: 0.74 on the papers' readings, 0.84 on the issuers'
documents), so the codes are one model's, not two coders'. Two claims rest on them. *The count of who may redeem*
(the case study's finding) is context: no headline, hook or payoff rests on it, and it supports K8 beside its other
evidence. *Our reading of today's monies* (K8) is a component: its clause that reserve-backed stablecoins are
redeemable by verified customers rests on its other evidence for the coin it names (USDC's terms, through the Federal
Reserve's Financial Stability Report of May 2023 and the FEDS Note of February 2024), not on the count.

## CS-F

*Independence and inflation targets.*

Frame a's window build matches each change to monies that did not change and had the same inflation before it, takes
inflation's change over the five years after less the year before, and sets the mean gap against bands that scenarios
with no effect give at the same number of changes, with placebo bands beside. The study uses two panels: central banks
made more independent (136 changes: -0.27, band -2.29 to +3.06) and
inflation targets adopted (30: -2.60, band -2.85 to +3.74; with the later
candidates read as adopters, 35: -1.62). Each gap lies inside its band. Read as a range on
the effect, the band moved to the observed gap: -3.3 to +2.0 after independence, which
excludes neither no change nor one of the size that matters; -6.3 to +0.3 after a target, which
excludes a rise beyond its high end and reaches a fall of several points. Monies that adopted a target often did so after high
inflation, which tends to fall back by itself (Ball and Sheridan name this regression to the mean).

## Robustness, chosen by risk

| Risk | Addressed by |
|---|---|
| A case entering by its outcome | the case studies' populations by published lists and rules (Bernanke and James's exits, Bordo and Schwartz's chronology, the default database, the papers' coins); K5's cases said to show existence only, never a rate or a condition |
| An outcome measured by the backing's own yardstick | value read as consumer prices (CS-A, CS-B); CS-C's value in gold said to be that, never purchasing power |
| Wholesale and consumer prices conflated | Bernanke and James's result printed on wholesale prices, CS-A on consumer prices, each named (`C18`) |
| Exits by exchange control pooled with suspensions | a variant without them (`C18`) |
| A few hyperinflation years driving a mean | medians and shares above ten per cent beside the means (`C19`); the years above 100% set apart (`C20`) |
| Eras confounding the classes | calendar eras beside the classes; war years and Bretton Woods apart (`C19`, `C20`) |
| Dates of convertibility misread | two transcriptions compared cell by cell; earlier resumption dates and the marked suspensions as variants (`C19`, `C20`) |
| Shared monies counted many times | the shared-once reading; bootstraps drawing a shared money's members together (`C16`) |
| A default dated inside a default already running | the breadth said wherever the share is printed; private creditors' arrears alone as a reading (`C16`) |
| A mean gap read off chance | null and placebo bands at the same number of changes (frame a) |
| Regression to the mean after high inflation | named beside the inflation-target panel (frame a) |
| A single model's coding read as two coders | said above for CS-E; a second model's run fixed on a card (`C17`), void by its own rule |
| Point-in-time (what was knowable when) | n/a because the study draws no investor rule and no scenario |

## Model steps the methods rely on

Each coding below followed rules fixed before it ran, and was checked as its record says.
The dates of Bordo and Schwartz's convertibility tables and of Bernanke and James's table of exits were transcribed on the page images by two separate runs of the same model (Claude Sonnet), which are not independent coders, compared cell by cell.
The prices of gold in Tooke's and Mitchell's tables, read on the page images, were transcribed by separate runs of the same model (Claude Sonnet), which are not independent coders, and a sample re-read by a second run whose model the record does not name.
The pegs abandoned, the second monies made legal and the currency boards, read from Ilzetzki, Reinhart and Rogoff's country chronologies for `C15`, were coded by separate runs of the same model (Claude Sonnet), which are not independent coders, some samples by runs whose model the record does not name.
The 1914 suspensions, the 1930s exits and the inflation targets adopted, for frame a, were read from their sources by separate runs of the same model (Claude Sonnet), which are not independent coders; the later adopters' membership and dates were read once by runs of Claude Opus and re-read blind by runs of Claude Sonnet.
The stablecoins' terms (`C14`) were coded by two runs of one language model (Claude Sonnet) working apart, which are not independent coders, and the issuers' documents sought and frozen by runs of the same model.
The passages cited in the register were read at their pages by runs of a language model (the study's writer, Claude Opus; delegated readers; the isolated audits of its design, Claude Opus), and the workshop's notes name who read each.
The interest rates of the greenback years (Homer and Sylla's Table 42) were transcribed on the page images and read twice by one run of a language model whose model the record does not name.
The isolated checks this text cites are separate runs of a language model (Claude Opus or Claude Sonnet), none of them a run that made what it checked.
Each agreement printed measures how far runs of a model agree, not two people; runs of one model share their biases, so their agreement is weaker evidence than two people's.

## The research log

The order of work, the checks and their answers are kept in the workshop and are not public: the step record (each step and its commit),
`check/` (the reports of the checks and their answers) and `notes/` (the harvest, the sources and their passages, the
gaps). This part was first produced on 2026-10-03 and regenerated on 2026-10-07; on 2026-10-08 it was rebuilt from the
design step under the revised production rules, answer-led. Reused from the earlier runs, each because a rerun would produce the
same: the frozen data, A3's and frame a's builds, `C14` and `C15`. New in this run: `C16` to `C20`, the transcription
of the three tables, and the cited numbers and passages of the eight components. The cards and results of the earlier
runs (`C04` to `C13`) stay in `cards/` and `results/runs/`, unused by this study's text.

## Sources

<!-- numbers:off -->
**Data**

- Òscar Jordà, Moritz Schularick and Alan M. Taylor, Macrohistory Database, release 6 (consumer prices, 1870–2020; CC BY-NC-SA 4.0).
- Federal Reserve Bank of St. Louis, FRED, CPIAUCNS (US consumer prices, monthly, from 1913), frozen 2026-09-30.
- World Bank, World Development Indicators, FP.CPI.TOTL.ZG (consumer-price inflation), frozen 2026-09-30.
- IMF, World Economic Outlook, October 2013, Argentina's end-of-period consumer prices, through DBnomics, frozen
  2026-10-08.
- The Bank of Canada–Bank of England sovereign default database (2025); IMF International Financial Statistics; the
  World Bank; Carmen Reinhart and Kenneth Rogoff's inflation and debt files (`C15`'s panel).
- Thomas Tooke, *A History of Prices*, vol. 2 (1838); Wesley C. Mitchell, *Gold, Prices, and Wages under the Greenback
  Standard* (1908), Table 2, and *A History of the Greenbacks* (1903); archive.org scans (A3).
- Frame a's sources: Bernanke and James's Table 2.1; Ana Carolina Garriga's central bank independence data (2025); Gill
  Hammond, *State of the art of inflation targeting*, Bank of England CCBS Handbook No. 29 (2012); the IMF's AREAER;
  David Cobham's classification of monetary policy frameworks (2024 update).
- The stablecoins' fixed set of papers: BIS Papers 141; BIS working papers 1146, 1164, 1219 and 1270; the Federal
  Reserve's IFDP 1334 and FEDS Notes; the New York Fed's Staff Report 1073; NBER working papers w27136, w30256,
  w30796 and w31160; and the issuers' launch documents as frozen.

Each dataset's URL, date retrieved and hash are in its manifest, published under `data/`; `results/datasets.yaml`
lists them all.

Of the series the study reconstructed (`data/reconstructed/`), one ships with its values: `ft001-g`, our own coding of
the issuers' launch documents. The others ship as their manifests only, which name their sources and how each series
was built. Their rows carry values from other publishers' datasets, which we republish only where a licence allows it:
Reinhart and Rogoff; Ilzetzki, Reinhart and Rogoff; the Macrohistory Database (CC BY-NC-SA 4.0); the Bank of England's
Millennium dataset; Chinn and Ito; the IMF, the AREAER among them. Or they transcribe tables of printed works (Bordo and
Schwartz's Tables 1A and 3, Bernanke and James's Table 2.1, Homer and Sylla's Table 42), which are not republished: their
values are verifiable at the table or page each row names. The public copies of the results leave out, likewise, Chinn
and Ito's index values and Ilzetzki, Reinhart and Rogoff's 2016 classes (the keys `ka_open` and `irr_class_2016`, in
`C06`, `C08`, `C09`, `C10`, `C12` and `C14`, with Cobham's first years in `C14`); each economy's line, its crossing and onset
dates, entry tercile and dated acts with each act's year before (the key `lines`, in `C04`, `C07` and `C15`), computed
or compiled in part from Reinhart and Rogoff's and JST's files; each economy's gold status in 1932–34, from Bernanke
and James's table (`status_1932_34`, in `C18`); each economy's inflation-target adoption year and the years Bordo and
Schwartz leave unclassed (`adoption_years`, `unclassed`, in `C19`); and the economy-years set apart with their JST rates
(`set_apart`, in `C20`).

**Works cited at their passages** (the passage and page of each are in the register's claims)

- Barsky, R. & Kilian, L. (2001), "Do We Really Know That Oil Caused the Great Stagflation?", NBER WP 8389.
- Bernanke, B. & James, H. (1991), "The Gold Standard, Deflation, and Financial Crisis in the Great Depression: An
  International Comparison", in Hubbard (ed.), *Financial Markets and Financial Crises*, NBER.
- Board of Governors of the Federal Reserve System, *Financial Stability Report*, May 2023.
- Bordo, M. D. (1992), "The Bretton Woods International Monetary System: An Historical Overview", NBER WP 4033.
- Bordo, M. D., Humpage, O. & Schwartz, A. J. (2006), "The Historical Origins of U.S. Exchange Market Intervention
  Policy", NBER WP 12662.
- Bordo, M. D. & Kydland, F. E. (1990), "The Gold Standard as a Rule", NBER WP 3367.
- Bordo, M. D., Landon-Lane, J. & Redish, A. (2004), "Good versus Bad Deflation", NBER WP 10329.
- Bordo, M. D. & Schwartz, A. J. (1994), "The Specie Standard as a Contingent Rule", NBER WP 4860.
- Calomiris, C. W. (1988), "Price and Exchange Rate Determination during the Greenback Suspension", *Oxford Economic
  Papers* 40(4), pp. 719–750.
- de la Torre, A., Levy Yeyati, E. & Schmukler, S. (2003), "Living and Dying with Hard Pegs", World Bank PRWP 2980.
- DeLong, J. B. (1997), "America's Peacetime Inflation: The 1970s", in Romer & Romer (eds.), *Reducing Inflation*.
- Eichengreen, B. & Sachs, J. (1985), "Exchange Rates and Economic Recovery in the 1930s", NBER WP 1498.
- Federal Reserve, FOMC, Statement on Longer-Run Goals and Monetary Policy Strategy, January 2012.
- Federal Reserve Bulletin, October 1919, December 1923 and August 1924 (FRASER).
- FEDS Notes, "Primary and Secondary Markets for Stablecoins", February 2024.
- Fischer, S., Sahay, R. & Végh, C. (2002), "Modern Hyper- and High Inflations", NBER WP 8930.
- Foote, C., Block, W., Crane, K. & Gray, S. (2004), "Economic Policy and Prospects in Iraq", *Journal of Economic
  Perspectives* 18(3).
- Grubb, F. (2012), "Is Paper Money Just Paper Money?", NBER WP 17997.
- Hong Kong Monetary Authority, its description of the Convertibility Undertakings.
- Judson, R. (2012), "Crisis and Calm: Demand for U.S. Currency at Home and Abroad", Federal Reserve IFDP 1058.
- Leeper, E. M. & Leith, C. (2016), "Understanding Inflation as a Joint Monetary-Fiscal Phenomenon", NBER WP 21867.
- Liu, J., Makarov, I. & Schoar, A. (2023), "Anatomy of a Run: The Terra Luna Crash", NBER WP 31160.
- Luther, W. J. & White, L. H. (2011), "Positively Valued Fiat Money after the Sovereign Disappears: The Case of
  Somalia".
- Posen, A. S. (1995), "Declarations Are Not Enough", *NBER Macroeconomics Annual* 10.
- Rolnick, A. J. & Weber, W. E. (1997), "Money, Inflation, and Output under Fiat and Commodity Standards", *Journal of
  Political Economy* 105(6); the Federal Reserve Bank of Minneapolis *Quarterly Review* reprint, whose pages are cited.
- Sargent, T. J. (1982), "The Ends of Four Big Inflations", in Hall (ed.), *Inflation: Causes and Effects*, NBER.
- Sargent, T. J. & Velde, F. R. (1995), "Macroeconomic Features of the French Revolution", *Journal of Political
  Economy* 103(3).
- Silber, W. L. (2007), *When Washington Shut Down Wall Street*, Princeton University Press.
- Velde, F. R. & Weir, D. R. (1992), "The Financial Market and Government Debt Policy in France, 1746–1793", *Journal
  of Economic History* 52(1).
- White, E. N. (1995), "The French Revolution and the Politics of Government Finance, 1770–1815", *Journal of Economic
  History* 55(2).
- Willard, K., Guinnane, T. & Rosen, H. (1995), "Turning Points in the Civil War: Views from the Greenback Market",
  NBER WP 5381.

Named as positions, through the works that report them: Mitchell (1903), Friedman and Schwartz (1963), Blinder
(1979), Bruno and Sachs (1985), Darby et al. (1983), Alesina and Summers (1993), Ball and Sheridan (2003).
<!-- numbers:on -->

## How to reproduce every figure and every number

Every number in this folder and in the web study is read from the register (`results/numbers.json`), which names for
each number the script that computed it or the source and page it is cited from. Published with this study: the code
(`code/`), whose `run.py` reruns the earlier cards (`C15`, `C05`, `C11`, `C13`, `C14`), writes the register
(`registry.py`, with `registry_v11.py` for `C16` to `C20` and `sources_v11.py` for the cited numbers and those read off
frozen data), adds the readings and the labels (`readings.py`, `labels.py`) and the claims (`claims.py`), draws every
figure (`figures.py`, `figures_v11.py`) and builds the web study's figures and calculator (`web_v11.py`); `C16` to
`C20` ran once at their own step (`cs_d.py`, `cs_e_second.py`, `cs_a.py`, `cs_b.py`, `cs_b_trim.py`), each refusing
a changed card. Also published: the cards (`cards/`), the results (`results/runs/`), the rules and the build protocols
(`protocols/`), and the manifest of every dataset read (`data/`); which of the series the study reconstructed ship
with their values is said under Sources.

Not investment advice.
