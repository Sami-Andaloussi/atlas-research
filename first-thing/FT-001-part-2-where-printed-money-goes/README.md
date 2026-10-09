# Does printing money really cause inflation? — methods and proof

*A First Thing Weekly Study · FT-001, part 2 of "The life of a money" · as of 2026-10-08*

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

The study answers its question in seven components. Every claim it makes is in the register of numbers
(`results/numbers.json`, its `claims`), with its evidence type, the component it serves, and either the passages it
rests on (each with its page, table or section, and how deeply the work was read) or the card of the analysis that
measured it. Four types are used: **established** (a documented fact or mechanism, cited at its passage), **cases**
(shown in history, with sources), **measured** (an analysis of ours, with its card) and **judgement** (our reading,
said as ours). The headline is a judgement weighing the components: the long-run link between money and prices, its
looseness in calm times, where the new money goes, whether the economy can produce more, and the fiscal roots of the
great inflations, each resting on its sources first.

Five analyses of ours are case studies inside the study, each beside the component it supports.

| Case study | Component | Card | Its parent | New in this run? |
|---|---|---|---|---|
| CS-A, the money growth line | K1 | `C28-a4-units-guard` (with `C29-a4-exploration-pace`, an exploration, and `C21-a4-1870-named` before 1950) | `C28`'s is `C25` (a correction) | reused |
| CS-B, central-bank money against the public's money | K2 | `C30-cs-b-base-against-broad` | `C28` (an extension) | yes |
| CS-C, the modern Fed's two largest printings, month by month | K3, K4, K5 | `C32-cs-c-door-timeline` (with `C34-cs-c-vu-bls`, its correction for v/u) | `C01-door` (a correction) | yes |
| CS-E, money in the pandemic, prices after it | K5 | `C31-cs-e-pandemic-cross-section` | — | yes |
| CS-F, what inflation took from cash and current accounts | K7 | `C33-cs-f-reclassification` | `C13-a6-checked` (a correction) | yes |

Every card in `cards/` was committed before any result on its data existed; the code refuses to run a card changed
since its commit, and each result in `results/runs/` names its card's hash. A card first committed after a result on
the same data names what it saw (`seen`) and whether it is a correction, an extension or an exploration (`kind`).
`C28`, `C29` and `C21` were reused from the study's earlier runs: the components they serve are the same, their cards
hold every rule the design asks, and their audits recomputed them. The earlier cards (`C01` to `C27`) stay in
`cards/` and `results/runs/`; those the text does not use are not reported here.

## The readings, and the size that matters

Each measured result is read against the size that matters fixed on its card: an **effect** (its range excludes no
difference and is not wholly inside the size that matters), **too small to matter** (its range lies wholly inside
it), or **bounded** (its range holds no difference and reaches past the size that matters), reported as what it
excludes. The size that matters for a slope is 0.1 of a point of inflation per point of money growth:
at the pace of 2020 and 2021's broad money, about two points of inflation a year.

**One rule, two wordings.** The new cards of this run (`C30`, `C31`) wrote the rule more strictly: an effect only if
the range's near end lies beyond the size that matters. The register keeps the workshop's rule. Where the two read
differently, the range excludes zero but its near end lies short of 0.1, and the text says so, never
"shown to matter": the long-run panel's version of CS-B (0.15, range 0.03 to
0.27), CS-E without its energy control (0.22, 0.08 to
0.38), and five of CS-E's variants, listed below.

**Sizes that matter set after the results.** `C28`'s, the same 0.1, was set on 2026-10-06 from the
reader's question after the earlier cards' results had been seen, and `C28`'s card restates it before its own run.
`C30` and `C31` fixed theirs before their runs; `C32` and `C33` measure and read against no size.

## CS-A

*The money growth line.* `C28` takes every economy with central-bank money, consumer prices and real output at both
ends of a ten-year window ending 1950 to 2020 (IMF, World Bank, ECB, FRED), and regresses average inflation on average
money growth with real output growth held fixed, below and above a line of 12% a year adapted from Teles and Uhlig (who cut on
average inflation, using M1; ours cuts on money growth), fixed before the run. It corrects `C25` (and `C27` for broad money) with a units guard: a World Bank series filling years the IMF
lacks is refused where its level differs from the IMF's by a factor the card fixes, after an isolated check found
Burkina Faso's real GDP spliced across units.

- Base money, 635 windows of 155 economies: below the line 0.25
  (0.14 to 0.36, 309 windows); above it 1.07
  (1.01 to 1.12); all windows 1.00. Held out from 1990, fitted on
  the earlier windows: 0.94 (0.83 to 1.04).
- Broad money, the line drawn on its own growth: below the line 0.62 (0.48 to
  0.75, 285 windows); above it 1.04. Each slope comes from one
  regression whose slope changes at the line, output growth held fixed by one coefficient on both sides. The study
  prints both where the calm slope appears: central-bank money's is the one its question bears on, and noise in that
  money flattens it by itself. The two rest on different decades, so their like-for-like comparison is CS-B. Fitted
  on the calm decades alone, each with its own output coefficient, central-bank money's slope is about the same
  (0.23, `C29`'s first band) and broad money's lower by more than the size that matters, still below one (an
  isolated check's recomputation, 2026-10-08, not a card's run, so not printed as a number).
- `C29`, an exploration written after two isolated checks and committed before `C28` ran, every slice named before
  its run: the slope by band, 0.23 at or below the line, 0.43 from 12% to 20%,
  0.68 from 20% to 30%, 1.26 from 30% to 50%, 1.01
  above; without the windows above 30%, above the line 0.62; from 2000, 0.65. A
  null simulation with one slope everywhere calls the line "separating" in 4.6% of draws. The bands
  were cut after the main split was seen, so they describe and never test.
- `C21`, before 1950: in 18 rich economies of the Macrohistory Database, on its narrow money
  (base money, notes or M1 by country), 0.58 below the line and 1.30 above; without
  the war decades, 0.58 over all.

These are associations across economies, never a measure of what printing does in one. Noise in base money at the
ends of a decade (spikes, reserve requirements, a union's national slice) flattens a slope; the decades just above the
line are less spread out than those below and yet steeper, so noise of one size does not explain the difference.

## CS-B

*Central-bank money against the public's money.* `C30` keeps `C28`'s windows where both base money and broad money
grew at or below 12% a year (our adaptation of Teles and Uhlig's line, which cuts on inflation using M1),
runs the same regression on each money, and reads the gap between the two slopes, with errors clustered by money (a
currency union counted once) and a paired cluster bootstrap beside.

- 113 economies' calm windows, 74% of them from 1990: base 0.12
  (0.03 to 0.21), broad 0.39 (0.23 to 0.56); the gap
  0.27, range 0.14 to 0.40 (bootstrap 0.15 to 0.41), an
  effect.
- The checks fixed before the run: windows from 1990, 0.27 (0.14 to
  0.41); to 1990, 0.13 (-0.11 to 0.36), named weak
  beforehand, bounded; windows ending by 2000, 0.12 (-0.02 to
  0.26), bounded; windows holding 2008 or later, 0.32
  (0.15 to 0.49); the Macrohistory Database's own windows before 1950,
  0.15 (0.03 to 0.27), and without the war decades 0.05
  (-0.04 to 0.13).
- Beside the slopes, the correlations: 0.18 with base money, 0.41 with broad money.

Base money growth is noisier, which flattens its slope by itself: part of the gap is that. About half the windows end
by 2000; there the gap is at most 0.26 and may be
zero (0.12, from -0.02), and it is clear in windows ending 2008 or later,
0.32 (0.15 to 0.49). So in recent calm decades the public's
money tracked inflation better; this does not measure what paid reserves do. The card was designed after
`C28`'s slopes on both monies had been seen, said on the card.

## CS-C

*The modern Fed's two largest printings, month by month.* `C32` corrects `C01`, which printed price totals over each window
across a change in the economy's state. It reads the two printings on one balance-sheet item, base money (H.4.1 and
FRED), August 2008 to October 2014 and February 2020 to December 2021: base money added
($3.15 trillion over 74 months; $2.96 trillion over 22), the share ending as
reserves (86%; 87%), the Fed's total assets beside
($3.56 trillion; $4.55 trillion), and the Fed's Treasury purchases as a share of the federal deficits of
the whole fiscal years (32%; 54%; months-weighted beside,
31% and 65%), said as "equal to", never "financed". Then a monthly
timeline to March 2023, each series in its own panel (base money, with reserves and currency; the public's money as growth
over twelve months; its velocity; nominal GDP as growth over four quarters; consumer-price inflation; job openings
per unemployed person; and unemployment), in the figure of these methods (`door-timeline-web`; `door-timeline` stops in December 2021); the web study's timeline has six panels,
base money and reserves apart, without nominal GDP and job openings. The job-openings panel is
built from BLS's own series, JOLTS job openings over unemployed persons, by `C34`, a correction of `C32` made for
the public copy: `C32` had read Blanchard and Bernanke's v/u from their replication files, which are cited and never
redistributed; `C34`'s series follows theirs closely, quarter by quarter, and its run gives the largest difference.
Blanchard and Bernanke's decomposition of 2020 to 2023 is read from their files the same way: the web study links
their paper rather than redrawing it (their parts, without the authors' residuals, sum to within
2.5% of actual inflation in every quarter).

*The door's scope* (a revision of 2026-10-09, on the reader's remark that the two printings read as the only ones):
the growth of base money over each printing's window as `C32` stored it (372%; 86%),
against the largest growth over any window of the same length ending by August 2008 in FRED's monthly series,
which starts in 1959 (62% over 74 months; 25%
over 22), computed in `code/registry_v15.py` from the same frozen series; descriptive, testing nothing. The series
does not reach the Second World War, whose balance sheet is cited from Judson and Weiss (2026) as a share of GDP,
a different measure, said as theirs.

M2 velocity is nominal GDP over M2, so velocity, nominal spending and the public's money are one fact, never three
confirmations. The dates of the acts annotated on the timeline were chosen after the window's price splits had been
seen, said on the card. A timeline shows what happened together, never what caused what.

## CS-E

*Money in the pandemic, prices after it.* `C31` takes every economy with the IMF's broad money at the ends of 2019,
2020 and 2021 and consumer prices for December 2021 and December 2023 (the euro area once, through the ECB), keeps
those whose 2015 to 2019 inflation averaged below ten per cent a year, and regresses inflation from December 2021 to
December 2023 on broad money growth from December 2019 to December 2021, both a year in logs, with each economy's 2019
energy imports held fixed, by a robust (Huber) regression with a bootstrap by cluster (a currency union counted once).
A test against chance, a leave-one-out check and a prediction on 2007 to 2011 (Q6) were fixed before the run.

- The main run, 76 economies: 0.27 of a point per point, range 0.10 to 0.48, an
  effect; by ordinary least squares 0.31 (0.14 to 0.50). Leaving one economy out at a time,
  the range's near end runs from 0.09 to 0.18: dropping any one of 10
  economies (Brunei, Hong Kong, Hungary, Jordan, Japan, Kyrgyzstan, Kazakhstan, Mongolia, Malaysia, Rwanda) brings it
  just below the size that matters, so on the card's own wording the reading would move to bounded; on the workshop's,
  the range still excludes zero, and the study prints the main reading with this beside it. Against
  2,000 permutations of money growth, the one-sided p-value is 0.000, and the reading rule
  confirms an effect under the null in 0.1% of them.
- Without the energy control, all 112 calm-start economies, 36 of them small
  economies with no energy data: 0.22, range
  0.08 to 0.38: it excludes zero but reaches below the size that matters.
- The variants, each read by the same rule: in each economy's currency, 0.25 (0.07
  to 0.46); money led a year, 0.14 (0.04 to 0.29); with
  2021's inflation momentum held fixed, 0.10 (-0.05 to 0.33),
  bounded; with the central bank's claims on the state, 0.23 (0.08 to
  0.50); without dollarised economies, 0.24; on annual averages,
  0.32 (0.14 to 0.53); every economy, calm start or not,
  0.40 (0.08 to 0.80). Five of them (in each currency, money led, the claims
  on the state, without dollarised economies, every economy) exclude zero but reach below the size that matters.
- On base money, the slope is 0.02 (-0.02 to 0.10): most of base money's spread in
  2019 to 2021 came from five economies, 64% of its variance.
- Q6, 2007 to 2011, the same design: 0.22 (0.12 to 0.41).

The same transfers swelled both money and demand, so the slope measures the two together; the cross-section cannot
separate the money from the fiscal demand that carried it, and the study says how much was the money's alone as its
judgement, beside the scholars who weigh it differently.

## CS-F

*What inflation took from cash and current accounts.* `C33` corrects `C13`. From February 2020 it applies each
month's price rise to US households' currency and checkable deposits (the Federal Reserve's Financial Accounts), less from April 2021 the interest a national interest-checking rate would pay. In 2020 a
change to Regulation D let banks class savings deposits as checkable (Federal Reserve, 24 April 2020); `C13` measured
that move against zero, and `C33` measures it as the shortfall of households' other deposits in the quarter the move landed
against those deposits' own path in the four surrounding quarters, fixed before the run: $720 billion (against
2019's quarters, beside, $627 billion; against each surrounding quarter alone, from $290 billion to
$1,009 billion).

- Per household, from February 2020: $6,170 to $7,581 (in constant dollars,
  $5,404 to $6,645); the whole stock, $813 billion to
  $998 billion. The upper bound treats the stock as published and paying nothing; the lower sets the
  measured move aside and deducts the interest. With 2019's baseline, the lower bound is $6,340.
- The timing beside, all holders: H.6 moved savings into M1 in May 2020; the households' accounts in a
  later quarter. Each date is its source's, never reconciled by us; the range uses the households' accounts.

"Tax" is said only of what the state collected on currency (seigniorage); the rest is what inflation took, with who
gained told from the balance sheets, never measured here.

## Robustness, chosen by risk

| Risk | Addressed by |
|---|---|
| A line chosen to fit | the line fixed before the run, adapted from Teles and Uhlig's (`C28`); another author's line beside (`C23`, earlier, reported in the register) |
| Overfitting the decades | held out by years from 1990 (`C28`) |
| Influential decades (the fast tail) | the slope by band, without the decades above the third band's edge, from 2000 (`C29`) |
| The line's rule firing by chance | a null simulation with one slope everywhere (`C29`) |
| Units breaks in the filled series | the units guard (`C28`) |
| Currency unions read as economies | errors clustered by union (`C29`, `C30`, `C31`) |
| Wars driving the long run | the war decades out before 1950 (`C21`, `C30`) |
| Noise in base money flattening its slope | said beside CS-B's gap; the correlations beside the slopes (`C30`) |
| An era or period carrying CS-B's gap | by period and by era, fixed before the run (`C30`) |
| Outliers driving the cross-section | a robust slope, leave-one-out, the least-squares slope beside (`C31`) |
| Energy shocks in the cross-section | the energy-import control, and the slope without it (`C31`) |
| Inflation already rising before the money | money led a year; 2021's momentum held fixed (`C31`) |
| Money standing in for fiscal transfers | the central bank's claims on the state as a variant; the limit said beside every reading (`C31`) |
| A pattern of one episode | the same design on 2007 to 2011 (`C31`, Q6) |
| A cause read off a timeline | each series in its own panel, no window total of prices across a change of state; the decomposition left as its authors', read in their paper (`C32`) |
| A reclassification passing as lost money | the move measured against deposits' own path, a range never a midpoint (`C33`) |
| Point-in-time (what was knowable when) | n/a because the study draws no investor rule and no scenario |

## Model steps the methods rely on

No coding, transcription or classification by a language model enters this part's evidence: its data are read by
script from their published files.
The passages cited in the register were read at their pages by runs of a language model (the study's writer, Claude Opus; the isolated audits of its design, Claude Opus), and the workshop's notes name who read each.
The isolated checks this text cites are independent runs of a language model (Claude Opus or Claude Sonnet), none of them a run that made what it checked.

## The research log

The order of work, the checks and their answers are kept in the workshop and are not public: the step record (each step and its commit),
`check/` (the reports of the checks and their answers) and `notes/` (the harvest, the sources and their passages, the
gaps). This part was first produced on 2026-09-30, regenerated on 2026-10-06 and restated on 2026-10-07 from `C28`
and `C29`; on 2026-10-08 it was rebuilt from the design step under the revised production rules, answer-led. Reused from the
earlier runs, each because a rerun would produce the same: the frozen data, `C28`, `C29`, `C21` and `C13`'s method
(through `C33`). New in this run: `C30` to `C33`, the series of 2026-10-08 (energy imports, unemployment, the Fed's
reverse repurchase agreements, Blanchard and Bernanke's files, savings deposits), and the cited passages of the seven
components. On 2026-10-09, `C34` (`cs_c_vu.py`) was added: the timeline's v/u from BLS's own series, a correction of
`C32` for the public copy. `C30`'s code first kept only the windows straddling 2008 in its era split; it was corrected to the windows
holding 2008 or later, the card's own count, before the result was kept; the card did not change.

## Sources

<!-- numbers:off -->
**Data** (each file frozen on the day named, its manifest — source, address, date read, fingerprint — published
with this study in `data/`; vintages in the cards)

- Board of Governors of the Federal Reserve System, via FRED: monetary base (BOGMBASE), reserve balances (WRESBAL),
  currency (WCURCIR), the H.4.1 balance sheet (WALCL, TREAST, WSHOMCB, WLRRAL), M2 and its velocity (M2SL, M2V), M1
  (M1SL), savings deposits (SAVINGSL), households' checkable deposits and currency and other deposits (Z.1), the
  national rate on interest checking (ICNDR); the federal deficit (FYFSD); BLS consumer prices (CPIAUCSL) and the
  unemployment rate (UNRATE); BLS job openings (JOLTS, JTSJOL) and unemployed persons (UNEMPLOY); BEA GDP; Census
  households (TTLHH); read 2026-09-27 to 2026-10-09.
- Olivier Blanchard and Ben Bernanke, replication files of NBER Working Paper 31417 (the decomposition; their v/u read only beside `C34`'s), frozen
  2026-10-08.
- International Monetary Fund, *International Financial Statistics* and *World Economic Outlook*, via DBnomics, read
  2026-09-30.
- European Central Bank, euro-area monetary aggregates and prices, via DBnomics.
- World Bank, World Development Indicators (GDP, consumer prices, broad money; energy imports EG.IMP.CONS.ZS, read
  2026-10-08); the World Bank's cross-country database of inflation (Ha, Kose and Ohnsorge), frozen 2026-10-02.
- Òscar Jordà, Moritz Schularick and Alan M. Taylor, Macrohistory Database, release 6 (CC BY-NC-SA 4.0).

**Works cited at their passages** (the passage and page of each are in the register's claims)

- Barro, R. J. & Bianchi, F. (2023, rev. 2025), "Fiscal Influences on Inflation in OECD Countries, 2020–2023", NBER
  WP 31838.
- Batini, N. & Nelson, E. (2002), "The lag from monetary policy actions to inflation: Friedman revisited", Bank of
  England External MPC Unit Discussion Paper 6.
- Benati, L., Lucas, R. E., Nicolini, J. P. & Weber, W. (2016), "International Evidence on Long Run Money Demand",
  NBER WP 22475.
- Blanchard, O. & Bernanke, B. (2023), "What Caused the US Pandemic-Era Inflation?", NBER WP 31417.
- Borio, C., Hofmann, B. & Zakrajšek, E. (2023), "Does money growth help explain the recent inflation surge?", BIS
  Bulletin no. 67.
- Buiter, W. H. (2007), "Seigniorage", NBER WP 12919.
- Board of Governors of the Federal Reserve System, press releases of 6 October 2008 (interest on reserves) and 24
  April 2020 (Regulation D).
- Federal Reserve, FOMC Records of Policy Actions, meetings of 6 October 1979 and 5 October 1982.
- Greenspan, A., testimony before the House Committee on Banking, 20 July 1993.
- Bank of England, *Inflation Report*, November 2011 (pp. 5, 10, 33).
- Federal Reserve, FOMC statements of 15 March 2020 and 29 April 2020.
- Judson, R. & Weiss, C. (2026), "A Brief Illustrated History of the Federal Reserve's Balance Sheet", *FEDS Notes*,
  13 February 2026 (sections 4 and 7).
- Bank of Japan, releases of 19 March 2001, 9 March 2006 and 4 April 2013.
- BIS, *Quarterly Review*, September 2011 and March 2015.
- Krugman, P. (1998), "It's Baaack: Japan's Slump and the Return of the Liquidity Trap", *Brookings Papers on Economic
  Activity* 1998(2).
- Leeper, E. M. & Leith, C. (2016), "Understanding Inflation as a Joint Monetary-Fiscal Phenomenon", NBER WP 21867.
- Lucas, R. E. (1996), "Nobel Lecture: Monetary Neutrality", *Journal of Political Economy* 104(4).
- McLeay, M., Radia, A. & Thomas, R. (2014), "Money creation in the modern economy", *Bank of England Quarterly
  Bulletin* 2014 Q1.
- Rolnick, A. J. & Weber, W. E. (1997), "Money, Inflation, and Output under Fiat and Commodity Standards", *Journal of
  Political Economy* 105(6); the Federal Reserve Bank of Minneapolis *Quarterly Review* reprint, whose pages are cited.
- Sargent, T. J. (1982), "The Ends of Four Big Inflations", in Hall (ed.), *Inflation: Causes and Effects*,
  University of Chicago Press.
- Teles, P. & Uhlig, H. (2010, rev. 2013), "Is Quantity Theory Still Alive?", NBER WP 16393.
- Willard, K. L., Guinnane, T. W. & Rosen, H. S. (1995), "Turning Points in the Civil War: Views from the Greenback
  Market", NBER WP 5381 (the abstract).
<!-- numbers:on -->

## How to reproduce every figure and every number

Every number in this folder and in the web study is read from the register (`results/numbers.json`), which names for
each number the script that computed it or the source and page it is cited from, with its measure, period and
population. `code/run.py` reruns the earlier cards in the order the study fixed (`C15`, `C18`, `C24`, `C13`, `C19`,
`C01`, `C02` to `C04`, `C21`, `C22`, `C25` to `C27`, `C28`, `C29`), reads `C30` to `C34`, which ran once at their own
step (`cs_b.py`, `cs_e.py`, `cs_c.py`, `cs_f.py`, `cs_c_vu.py`), each refusing a changed card, then writes the register
(`registry.py`, with `registry_v15.py` for `C30` to `C33`), the readings and labels (`readings.py`, `labels.py`), the
claims (`claims.py`), the figures (`figures.py`, `figures_v15.py`) and the web study's figures and calculator
(`web_v15.py`). The cards are in `cards/`, the results in `results/runs/`, the manifests in `data/`. Part 2
reconstructs no series, so only manifests ship. The public copy of `C32`'s result leaves out Blanchard and Bernanke's
decomposition and v/u (`decomposition`, `v_over_u`), and the figures that redrew it for our checks (`door-decomposition`) are not published: their
replication files are cited and never redistributed. The public copies also leave out each economy's windows and
episodes where they were computed from the Macrohistory Database (CC BY-NC-SA, `points` in `C21`) or, in part,
from Ha, Kose and Ohnsorge's inflation database (`points`, `windows_added`, `windows_changed`, `windows_dropped` and
`episodes` in `C25` to `C29`), whose licence is not established (its page could not be read); their readings,
slopes and counts stay, and the figures that draw those windows (`longrun`, its email image, `cs-b-slopes`) and the carousel, whose
cover is one of them, are not published here. They
leave out too the changes of the NASDAQ and Case-Shiller indexes and the University of Michigan's expected inflation, copyrighted, in `C18`
and the register.

Not investment advice.
