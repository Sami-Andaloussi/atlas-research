[Up: Blueprint](README.md) · [L2 →](L2-theory-map.md)

# L1 — Facts

## TL;DR

The floor of the system: public series captured as bytes, each value anchored to the slice it came from, every revision kept as a new vintage.
Any reader asks for an instant and gets exactly what was knowable then, nothing later.
This layer must be right to the last digit: every other layer inherits its errors.

## Purpose

Give the rest of Atlas a store of economic facts that is **exact, dated and replayable**: for any
series and any past instant, the value as it was then known, with the document that said so.

**Success looks like:**
- Every stored value re-reads from its captured document: the document's fingerprint matches, and
  the anchored range gives back the value.
- A read as of an instant never returns anything that became available after it, and replays are
  identical.
- Every absence is typed; no gap is ever filled by a zero, a carry-forward or a guess.

## The series catalogue

L1 owns the catalogue. For each economy and subject it lists the base series, their publisher,
unit, frequency, release calendar, definition versions and, where several sources carry the same
series, which one takes precedence. The theory map and the workshop file requests into it; they
never edit it.

| Subject | United States (first) | Switzerland | Euro area |
|---|---|---|---|
| Growth | Real GDP and its components; potential output (CBO) | Real GDP | Real GDP |
| Prices and expectations | CPI and PCE, headline and core; survey and market-based expectations | CPI, headline and core | HICP, headline and core; the ECB's surveys of expectations |
| Jobs and wages | Payrolls, unemployment, participation, wages | Unemployment, employment, wages | Unemployment, negotiated wages, unit labour costs |
| Central bank and rates | Policy rate, Treasury curve, real yields; neutral-rate and term-premium estimates as published | SNB policy rate, SARON, Confederation bond yields, sight deposits | ECB deposit facility rate, €STR, euro-area yields and sovereign spreads |
| Central-bank documents | FOMC statements and minutes | SNB monetary policy assessments | ECB monetary policy statements and accounts |
| Policy frameworks | The inflation target, its measure and the framework, as dated facts | The SNB's definition of price stability, dated | The ECB's target and strategy, dated |
| Published forecasts | FOMC projections, the Survey of Professional Forecasters | SNB conditional inflation forecast | ECB staff projections |
| Credit | Bank lending, lending standards, credit spreads | Bank lending | Bank lending |
| Budget | Deficit, debt | Confederation finances | Government deficit and debt |
| External and currency | Current account, broad dollar index | Current account, franc exchange rates, SNB foreign-currency reserves | Current account, euro exchange rates |
| Housing | Permits, starts, prices, mortgage rates | Real-estate prices, mortgage rates | House prices |

**Policy frameworks are facts with dates.** A target, its measure, its framework and even the
meaning of "the policy rate" change. The Fed adopted an explicit 2% target in January 2012 and
revised its framework statement in 2020 and again in 2025; the ECB moved to a symmetric 2% target
in 2021 and reviewed its strategy in 2025, and steers through its deposit facility rate; the SNB
equates price stability with CPI inflation below 2%, deflation excluded, and has set an SNB policy
rate only since June 2019, after targeting a range for three-month Libor. A card that compares
inflation with "the target", or reads "the policy rate", reads the definition in force on the run's
date; for the Fed's target range, the card states whether it reads the midpoint or the effective
rate.

**Published forecasts are facts about their forecaster.** A projection is stored under the instant
it was published and the period it targets. It can be read as what the forecaster expected; it is
never read as the value of the period it forecasts.

**Sources: public only.** For the United States, the BLS, the BEA and the Federal Reserve, with FRED
and its vintage archive ALFRED for history; for Switzerland, the SNB, the Federal Statistical Office
and SECO; for the euro area, Eurostat and the ECB. Where a publisher's own release file exists,
values are anchored to it; ALFRED supplies the vintages the publisher does not keep. An economy
enters the catalogue only once a real download from each of its sources has succeeded. Inputs with
no public source (priced policy paths from futures, the cross-currency basis, most emerging-market
spreads) stay declared as not sourced. Where a public proxy exists it is used and named: the New
York Fed's survey of market participants' expected policy path, Treasury bill and two-year yields.
Otherwise a lens that needs the input reads without it, says so, or abstains. Some series that FRED
shows are licensed by their owners; each series records whether it may be redistributed, and the
export carries only those that may.

**Published estimates have no vintages before Atlas.** Neutral-rate and term-premium estimates are
re-estimated over their whole history at each update and mostly not archived. Their real-time
history starts at Atlas's first capture; before it, they are final data only, and flagged.

## Interfaces

| Direction | Artefact | From / to |
|---|---|---|
| in | Requests for series | [L2](L2-theory-map.md), [L3](L3-subject-cards.md) |
| in | Publishers' release calendars | External |
| in | Documents and API responses | Public sources |
| out | Capture archive: bytes, fingerprint, source, capture instant | Audit; [L6](L6-outputs.md) for citations |
| out | Point-in-time fact store ([records](data-contracts.md#records)) | [L4](L4-analysis.md), [L5](L5-scenarios-score.md), [L6](L6-outputs.md) |
| out | The read, with its vintage selector ([contract](data-contracts.md#the-read)) | [L4](L4-analysis.md), [L5](L5-scenarios-score.md), [L6](L6-outputs.md) |

## Gates

**Entry.** Start only when:
- the catalogue names, for the first subject, every series with its publisher, unit, frequency,
  release calendar and definition version;
- each publisher has been reached by a real download, and its terms allow the use.

**Exit.** Pass when all of these hold:
- every value in the store re-reads from its document, checked over the whole store;
- the read is shown unable to return a value available after its instant, by a test that plants a
  later vintage and must not see it, for every vintage selector;
- a revised series holds every vintage it has had since its first capture, or since the start of its
  real-time archive;
- every absence in the first subject's series carries a type;
- capture runs from the release calendar, without a human starting it, and sources with no calendar
  are re-checked on a fixed schedule.

## Steps

1. **Catalogue.** *Design.* Write the catalogue for the first subject; one line of justification
   per series, the date from which each is wanted, and the precedence between sources.
2. **Capture.** *Execution.* Retrieve the response body as bytes, never a parsed copy; store it under
   its fingerprint with the capture instant, and the HTTP headers apart. A document already
   archived is logged as a re-check, not stored twice. A format the system cannot read honestly
   gets a named refusal path, and until it has one, documents in that format are excluded visibly
   rather than half-read.
3. **Anchoring.** *Design and execution.* For every value, record the ranges of the value, the series
   label, the series identifier, the place and the period, through a decode path for spreadsheets
   and PDFs ([anchor](data-contracts.md#records)). A value that cannot be anchored is refused.
4. **Vintages.** *Design.* Capture every vintage where a real-time archive keeps them (ALFRED, the
   Philadelphia Fed's real-time dataset, the euro area's real-time database); elsewhere, start the
   history at the first capture and flag earlier history as final data only. Every release event is
   a vintage with its release stage, flash, advance or later, even when it confirms the previous
   value.
5. **Definitions.** *Design.* Open a new definition version at a method break, a rebasing, a change
   of composition (the euro area gained Croatia in 2023 and Bulgaria in 2026), or a change in what a
   policy rate means, so that a series never silently changes meaning.
6. **Four instants.** *Execution.* Store with each value when it was released, when it counts as
   knowable, when it was captured and when it entered, in UTC.
7. **Absences.** *Design.* Map each publisher's markers to the absence types. A "." that FRED writes
   on a market holiday is not the same absence as a month that was never published: the US CPI for
   October 2025, which the government shutdown left uncollected, is missing for good, and any pace or
   year-on-year rate that needs that month is absent too, with the same reason. A value whose release
   date has not come is "not yet released" only until it does, so that type is computed at read
   time.
8. **The read.** *Execution.* One function reads the store, takes an instant and a vintage selector,
   and caps every answer at that instant. There is no other door; the export materialises the same
   function.
9. **Calendar.** *Execution.* Release calendars trigger capture; a capture that fails is retried and
   reported, never skipped silently.

## Deliverables

- The series catalogue, per economy and subject, with definition versions and source precedence.
- The capture archive and its manifest.
- The point-in-time fact store and its read.
- A one-command check that re-verifies every fingerprint and re-reads every anchor in the store.

## What it refuses

| It refuses | Because |
|---|---|
| A value that does not re-read from its document | It cannot be traced. |
| A read with no instant | Every read in Atlas is a read as of an instant. |
| An update that overwrites a value | A revision is a new vintage. |
| An absence stored as zero, false or empty | Absence is information, and its kind matters. |
| A forecast read as an observation of the period it targets | A projection is a fact about the forecaster, not about the period. |
| A paid or private source | Every number must be re-fetchable by whoever doubts it. |
| A document format with no honest reader | Half-read is worse than excluded. |

## Worked example

US real GDP growth for the second quarter of 2024 was first released by the BEA on 25 July 2024 at
08:30 New York time, at 2.8% annualised; the second estimate on 29 August put it at 3.0%, and the
third on 26 September kept 3.0%. Atlas would store three vintages of the same period, each with its
release stage, its four instants and its anchors into the BEA release file. A read as of 1 August
2024 returns 2.8%; a read as of 1 October returns 3.0%; a read of the *first release* as of
1 October still returns 2.8%. A scenario written in July about that quarter is judged on the
vintage it targeted, not on whichever came last.
