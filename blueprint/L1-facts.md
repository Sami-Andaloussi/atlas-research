[Up: Blueprint](README.md) · [L2 →](L2-theory-map.md)

# L1 — Facts

## TL;DR

The floor of the system: public series captured as bytes, each value anchored to the slice it came from, every revision kept as a new vintage.
Any reader asks for a date and gets exactly what was known on that date, nothing later.
This layer must be right to the last digit: every other layer inherits its errors.

## Purpose

Give the rest of Atlas a store of economic facts that is **exact, dated and replayable**: for any
series and any past date, the value as it was then known, with the document that said so.

**Success looks like:**
- Every stored value re-reads from its captured bytes: change one byte of the document and the
  anchor breaks.
- A read as of a date never returns anything published after it, and replays are identical.
- Every absence is typed; no gap is ever filled by a zero, a carry-forward or a guess.

## The series catalogue

The catalogue is a data card: for each subject, the base series, their publisher, unit, frequency
and release calendar. Knowledge about a series lives in that file, not in code.

| Subject | United States (first) | Switzerland | Euro area |
|---|---|---|---|
| Growth | Real GDP and its components, potential output | Real GDP | Real GDP |
| Prices | CPI and PCE, headline and core; inflation expectations | CPI | HICP, headline and core |
| Jobs | Payrolls, unemployment, participation, wages | Unemployment, employment | Unemployment |
| Central bank and rates | Policy rate, Treasury curve, real yields | SNB policy rate, Confederation bond yields | ECB policy rates, euro-area yields |
| Credit | Bank lending, lending standards, credit spreads | Bank lending | Bank lending |
| Budget | Deficit, debt | Confederation finances | Government deficit and debt |
| External and currency | Current account, broad dollar index | Current account, franc exchange rates, SNB reserves | Current account, euro exchange rates |
| Housing | Permits, starts, prices, mortgage rates | Real-estate prices, mortgage rates | House prices |

**Sources: public only.** For the United States, FRED and its vintage archive ALFRED, the BLS and
the BEA; for Switzerland, the SNB, the Federal Statistical Office and SECO; for the euro area,
Eurostat and the ECB. An economy enters the catalogue only once a real download from each of its
sources has succeeded. Public-only is a constraint with a purpose: anyone who doubts a number can
fetch it again.

## Interfaces

| Direction | Artefact | From / to |
|---|---|---|
| in | Series catalogue (data card) | The workshop ([L3](L3-subject-cards.md)) |
| in | Publishers' release calendars | External |
| in | Documents and API responses | Public sources |
| out | Capture archive: bytes, fingerprint, source, capture date | Audit; [L6](L6-outputs.md) for citations |
| out | Point-in-time fact store: value, period, vintage, anchors, four dates | [L4](L4-analysis.md), [L5](L5-scenarios-score.md), [L6](L6-outputs.md) |
| out | The as-of read | [L4](L4-analysis.md), [L5](L5-scenarios-score.md) |

## Gates

**Entry.** Start only when:
- the catalogue names, for the first subject, every series with its publisher, unit, frequency and
  release calendar;
- each publisher has been reached by a real download, and its terms allow the use.

**Exit.** Pass when all of these hold:
- every value in the store re-reads from its bytes, checked over the whole store;
- the as-of read is shown unable to return a value known after its date, by a test that plants a
  later vintage and must not see it;
- a revised series holds every vintage it has had since its first capture;
- every absence in the first subject's series carries one of the eleven types;
- capture runs from the release calendar, without a human starting it.

## Steps

1. **Catalogue.** *Design.* Write the data card for the first subject; one line of justification
   per series, and the date from which each is wanted.
2. **Capture.** *Execution.* Retrieve the bytes, never a parsed copy; store them with a fingerprint
   and the capture date. A format the system cannot read honestly gets a named refusal path, and
   until it has one, documents in that format are excluded visibly rather than half-read.
3. **Anchoring.** *Design and execution.* For every value, record the byte ranges of the value, the
   series label, the series identifier, the place and the period; re-reading the ranges must give
   back the value. A value that cannot be anchored is refused.
4. **Vintages.** *Design.* Where the publisher keeps vintages (ALFRED for US series), capture them
   all; elsewhere, start the vintage history at the first capture and never overwrite it.
5. **Four dates.** *Execution.* Store with each value when it was published, captured, known and
   entered.
6. **Absences.** *Design.* Map each publisher's markers to the eleven types: a "." that FRED writes
   on a market holiday is not the same absence as a month that was never published.
7. **As-of read.** *Execution.* One function reads the store, and it takes a date. There is no other
   door.
8. **Calendar.** *Execution.* Release calendars trigger capture; a capture that fails is retried and
   reported, never skipped silently.

## Deliverables

- The series catalogue, per economy and subject.
- The capture archive and its manifest.
- The point-in-time fact store and its as-of read.
- A one-command check that re-reads every anchor in the store.

## What it refuses

| It refuses | Because |
|---|---|
| A value that does not re-read from its bytes | It cannot be traced. |
| A read with no date | Every read in Atlas is a read as of a date. |
| An update that overwrites a value | A revision is a new vintage. |
| An absence stored as zero, false or empty | Absence is information, and its kind matters. |
| A paid or private source | Every number must be re-fetchable by whoever doubts it. |
| A document format with no honest reader | Half-read is worse than excluded. |

## Worked example

The World Bank publishes US GDP for 2024 as 29 298 013 000 000 current dollars, in an API response of
1 567 bytes. Atlas would keep those bytes unchanged, and the stored record would hold five anchors
into them: the value (offset 246, 14 bytes), the series label "GDP (current US$)", the identifier
`NY.GDP.MKTP.CD`, the country and the year; and four dates: published, captured, known, entered.
Change one byte of the document and the anchors no longer re-read. When the World Bank revises the
figure, a second vintage is added, and a read as of a date before the revision still returns the
first.
