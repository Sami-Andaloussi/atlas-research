# FT-001 — M3: the currency boards, coded before frame c reads them

> The hand list that section 7 of the panel protocol (`FT-001-M3-panel.md`, c7) asks for. Written by the E2
> session (`plan/e2-ft001.md`), 2026-10-01, **before any board is coded**, and committed alone first. **The
> rules are M0's**, version 4.2 (commit 3163162), and the panel protocol's: c7 (i) says that from 16 August
> 1971 "only a currency board redeems on demand into another money", and that a lagged class 2 ("pre-announced
> peg or currency board") *cannot be read* until the boards the chronologies name are coded. This file adds no
> rule; where a reading is open it says so (marked *reading*).
> **What was seen before writing**: a count of the phrase "currency board" in the chronologies' text (33
> hits) and the first thirty of those lines — dates, the classification, a few words of comment. Frame c's
> list was read only for its columns and for the count of lines waiting on this list: 120 lines whose lagged
> class is 2 at an entry from 1971 (their money and entry year, and their status as frame c's second build
> wrote it). No outcome, value or break of any line was read for this file.

## 1. What is coded, and where it goes

**The boards list** — `data/reconstructed/ft001-boards/` (`series.csv`, `MANIFEST.md`): one line per
**period during which a money was issued under a currency board**, as the chronology prints it. Columns:
`money` (ISO3 as `economies.py` codes it), `country_as_printed`, `start`, `end` (as printed; `end` empty when
the period runs to the chronology's end, October 2016), `classification` (as printed), `anchor` (as printed),
`label` (`classification` or `comment`, section 2), `locator` ("w23135 p. N, <country>, the period <dates>"),
`quote` (at most twelve words of the comment), `uncertainty` (`clear` or `judgement`, with its reason) and
`coder`.

**Source**: Ilzetzki, Reinhart and Rogoff's country chronologies, NBER Working Paper 23135 (February 2017),
frozen at `data/irr/country-chronologies-1946-2016/2026-09-30/`, read to October 2016. **Every country's table
is read whole, in page order**, never a country searched for.

## 2. The rules

- **B1 — a board**: a period whose **classification** names a currency board — "Peg (Currency board)" in any
  case or spacing, alone or with a second label ("Peg (Currency board)/Freely falling" is a board in a year of
  high inflation: still a board). `label` = `classification`.
- **B2 — a board named only in the comments** (*reading*): a period whose classification does not name a
  board while its comment says the money is issued by a currency board ("West African pound is Currency
  Board"). Listed with `label` = `comment`; **not a board in the headline**, a board in the variant
  `boards-with-comments`.
- **B3 — dates**: as printed. A start or end given by month only is that month; by year only, that year. A
  period whose dates cannot be read is listed with `uncertainty` = `judgement` and is *cannot be read* in
  frame c.
- **B4 — the money**: the chronology's country is coded to the ISO3 of the economy whose money it is, as
  the acts list coded the same tables (`economies.py`); a shared money issued by one board for several
  territories (the West African pound) gives one line per economy the chronology lists it under.
- **B5 — what frame c reads** (*reading*): frame c's lagged class reads the year before the entry (R12). The
  board is read at the same date: **a board in force on 31 December of the year before the entry**. For an
  entry read past 2016, the board of October 2016 is carried, flagged as the class is (`regime_carried`).
  Then, for an entry from 1971 whose lagged class is 2:
  - a board in force → *convertible at entry: yes* (apart, R25);
  - no board in force, and no board period's dates unreadable at that date → *convertible at entry: no*;
  - a board period that cannot be dated around that date → *cannot be read*.
  A class other than 2 is unchanged (not convertible, c7). The variant `boards-with-comments` adds B2's lines.

## 3. The coders

- **Two coders, each over the whole document**, independent agents that have not seen each other's lines
  and never see frame c's lines; each reads every country's table in page order.
- Agreement is reported as Cohen's κ on country-years from 1946 to 2016 (under a board at 31 December or
  not), with every disagreement listed.
- **Disagreements are settled by this file's text**, by the session, each settlement written in the
  manifest; none by looking at frame c.

## 4. Order of commits, and what no code holds

- This protocol alone; then the list (`ft001-boards`) with its κ; then `strain.py`'s reading of it, with
  tests, committed before frame c's third build reads it.
- *The barrier*: the commit order (this file before the list, the list before the code that reads it).
  What no code holds: that the coders choose no board by its outcome. Their prompts carry no frame c line,
  but the chronologies' comments speak of high inflation and parallel premiums; B1 counts a board whatever
  its second label, so a coder has no rule that an outcome could bend. Said.
