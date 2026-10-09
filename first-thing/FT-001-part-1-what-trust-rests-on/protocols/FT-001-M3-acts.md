# FT-001 — M3, second part: the acts, coded before any outcome

> Mission M3 (second part) of `bank/dossiers/FT-001-the-life-of-a-money.md`, section 14. Written by the E2
> session (`plan/e2-ft001.md`), 2026-09-30, **before any act is coded**, and committed alone first: this file
> is the coders' protocol M0 section 3 asks for. **The rules are M0's**, version 4.2
> (`FT-001-M0-rules.md` and its twin, commit 3163162; this protocol was first written under v4.1, 5b95936, which v4.2 changed in no decision rule): section 2's closed lists of acts, their headline
> sources, and section 3's case line and coders. This file adds no rule; where M0 leaves a reading open, it
> says so and chooses in the open (marked *reading*), for the audit to judge.
> **What was seen before writing**: the frozen sources' structure — sheet names, column labels, the layout of
> the Bank of Canada–Bank of England workbook, Reinhart and Rogoff's *Varieties* and *This Time Is Different*
> workbooks, Garriga's variable list, and the chronologies' first pages (how a country's table is laid out:
> Afghanistan, Albania, Angola, Zimbabwe's first lines). One slip: printing Garriga's header also printed its
> first two rows (the United States, 1970 and 1971, every column, the file's own CPI inflation among them).
> No other value of any source was read, and no price, rate or money stock of any frame.

## 1. What is coded, and where it goes

**The acts list** — `data/reconstructed/ft001-acts/` (`series.csv` and `MANIFEST.md`): one line per act of
M0 section 2's headline lists, **T2, L1, L2, L3 and H1**, and one per variant act the same sources give
(L3's index variant), set apart. Its columns are the reconstructed dataset's (`period` the act's date, `value`,
`unit`, `source`, `locator`, `note`, `uncertainty`) beside M0's case line: `money` (below), `frame` = `acts`,
`route` = the act's code, `entry_date` = the act's date, `status`, `source`, `locator`, `coder`,
`rules_sha256` (the pair's hash at 3163162, v4.2); the outcome fields stay empty — an act has none. Two more
columns: `headline` (`yes` for the headline acts; `no` for a variant, whose `status` is *apart* with the
variant named, never counted in a headline) and `support` (the support the act makes give way).

**Coverage** — `coverage.csv` in the same folder: for each economy and each act's source, the first and last
year the source reads. **Past a source's last year an act *cannot be read*, never "none"** (M0, `common.
source_last_year`): the frames read "no act" only inside a source's coverage.

**`money`** — the issuing economy's ISO 3166-1 alpha-3 code, from the World Bank's list frozen at
`data/worldbank/_economies/2026-09-30/` (e.g. `ARG`). Economies that no longer exist take their former
ISO 3166-3 code (`YUG` Yugoslavia, `SUN` the Soviet Union, `CSK` Czechoslovakia, `DDR` East Germany) —
*reading*. **Acts are coded by economy**, as the sources give them: which money an act touches (a new money
chained to the old, M0 section 1) is read by the frames, not here. **For the euro area** (M0 section 1: one
money from 1999), T2 stays on the member state; whether a member's default is an act on the euro's
*taken back* support is not fixed by M0 — **declared** for the frames (section 6).

**Dates** — `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, at the precision the source gives, never finer.

## 2. The acts coded by script — `missions/code/acts.py`

Run identically on every economy the source holds; nothing searched case by case.

- **T2 — a default or restructuring of the state's debt, external or domestic (its year).** *Taken back*
  gives way.
  - **From 1960**: the Bank of Canada–Bank of England database, 2025 edition (`bankofcanada/sovereign-
    defaults`, sheet `Debt_2025`, column `TOTAL_2025`: the stock of the state's debt in default, all
    creditors, US$ million). M0: "the year of a default is the first year of a stock". *Reading*: a year t
    whose stock is above zero while year t−1's was read and zero. A stock already above zero in an
    economy's first year in the database began before it: dated by the sources before 1960, never a 1960
    act. A year that cannot be read (empty) between two years with a stock breaks the reading: the next
    stock after it is coded *apart*, "the year before cannot be read". `value` = the stock that year,
    `unit` = US$ million.
    **Since the second build (3d, O1), read in each creditor class**; this total-stock reading is the
    variant `T2-var-total`.
  - **To 1959**: Reinhart and Rogoff's *Varieties* (`reinhart-rogoff/varieties-{A-E,F-M,T-Z}`), **only the
    two columns "Sovereign debt crises — domestic" and "— external"**, found by their labels. **The
    currency, inflation, stock-market and banking columns are never read** (outcomes). An act in the first
    year of each run of 1s in either column. `value` 1, `unit` "dummy".
  - **The M–S countries** (their *Varieties* file is not served): the external-default dummy panel of *This
    Time Is Different* (`reinhart-rogoff/ttid-default-tables`, the Table 6.2 and 6.4 workbooks' sheet
    `ExternalDefaultDummys`), the first year of each run of 1s; **domestic defaults cannot be read** there,
    said in `coverage.csv`.
  - The 1959/1960 seam: a run that crosses it is one default, dated by the earlier source.
- **L1 — a statutory cap on issue or on central-bank credit to the state lifted or raised.** *A limit by
  rule* gives way. Garriga (2025) (`garriga/cbi`, `cuk_limlen`, 1970–2023): a year in which the component
  falls below its value the year before, both read. `value` = the fall, `unit` "index points"; `note` says
  whether the component stays at or above M0's 0.5 after the fall — **an L1 act can leave the cap standing**
  (M0 v4.1, declared).
- **L3 — a legal reform Garriga codes as decreasing independence.** *A limit by institution* gives way.
  Garriga's `reform` = 1 and `decrease` = 1 in the year (her own flags, M0 [c-M3]). **Variant**, *apart*:
  her index (`lvau_garriga`) down by 0.05 or more in a year. The other half of L3, **a target abandoned**,
  is coded by hand (section 3).
- Economies are matched to `money` by Garriga's two-letter `ISO` column; the other sources' names by the
  table in `missions/code/economies.py` (the World Bank's names, then each source's spelling beside it),
  every unmatched name printed and never dropped silently.

## 3. The acts coded by hand — from the chronologies

**Source**: Ilzetzki, Reinhart and Rogoff's country chronologies, NBER Working Paper 23135 (February 2017),
frozen at `data/irr/country-chronologies-1946-2016/` — for each country, a table of periods (dates;
classification, primary/secondary/tertiary; comments). **Read to September 2016**: after it, L2 and H1
*cannot be read*. **Every country's table is read whole, in page order**, never a country searched for.

- **L2 — a peg, band or board abandoned by an announced decision** (M0 section 2). A line when:
  1. a period whose classification is an **announced** arrangement — a peg, a pre-announced crawling peg,
     a pre-announced band or crawling band, or a currency board; not one the classification calls
     *de facto* (the chronologies' mark of an arrangement that was not announced);
  2. **ends by a decision the chronology records** — the classification or the comments say it was
     abandoned, suspended, broken, floated, or replaced by a float, a de facto regime, freely falling, a
     wider band, or multiple rates **in place of** the peg;
  3. **not** a change of level (a devaluation or revaluation) or of anchor **within a kept announced
     arrangement**, and not the start of a new money with the same arrangement (those are value, or a new
     money, M0) — M0's two variants, **a devaluation of 10% or more within a kept peg** and **a step beyond
     an announced crawl**, are coded *apart* where the chronology states the change and its size, and
     noted without a size where it does not (never sized from an exchange-rate series here);
  4. dated at the date the chronology gives for the change (the day or month where given; the year
     otherwise); where the comments give the announcement's own date, that date.
  A change of classification with no end of the announced arrangement recorded is **value, never an act**.
- **H1 — another money made legal tender, or legal for domestic contracts, by an announced decision**: the
  comments record that a foreign money (or several) became legal tender, or was allowed for domestic
  contracts or payments, by a decision — official dollarisation or euroisation, a multi-currency system.
  A foreign money merely circulating, or foreign-currency deposits allowed, is **not** H1.
- **L3's other half, a target abandoned**: an inflation target the chronology records as abandoned, and
  Hammond's handbook (`frame-a/hammond-ccbs-29`, *State of the art of inflation targeting*, 2012) where it
  names a country that stopped targeting. Joining the euro is a competing exit (M0 section 4), not an
  abandonment.

**Each hand-coded line** carries the page (`locator`: "w23135 p. N, <country>, the period <dates>"), the
classification before and after as the chronology prints them, and a comment of at most twelve words
quoted — never more (the chronologies' copyright notice allows short sections with credit). `uncertainty`:
`clear` or `judgement` (a decision the text implies but does not state), with the reason.

**The coders.** The first coder reads every country in page order; **a second coder**, an independent agent
that has not seen the first's lines, recodes **a 20% random sample of the countries, drawn with seed 1797**
(M0 section 3) from the same pages; agreement is reported as Cohen's κ on country-years (an act in the year
or not), for L2 and H1 apart, with every disagreement listed. **Disagreements are settled by the text of M0
and of this protocol, never by an outcome**; each settlement is written in the manifest. Coders are outcome-
aware (the histories are known, and the chronologies' comments speak of devaluations and parallel
premiums): the protocol's barrier is that an act is coded only from what the chronology says was decided,
never from what followed.

### 3a. Readings settled after the first pass (2026-09-30, before the second)

The five coders' first pass (kept in the manifest: files and counts) read the protocol's L2 differently
where it was loose — condition 1 said a "de facto" class marks an arrangement not announced, while the
chronologies' comments sometimes state an official peg under a de facto class; condition 2 let the
classification alone record an end, and named "a wider band" as one. On the sample, L2's first-pass κ was
**0.50**; H1's and force's disagreements were none. **Settled by M0's text** (section 2: *a peg, band or
board abandoned by an announced decision; a change of de facto class with no announcement is value*),
never by an outcome, and committed before the second pass; every coder recodes under them, the second
coder included, and κ is measured again:

- **S1 — an announced arrangement stands** when the classification names a peg, a pre-announced band or
  crawl, a moving band or a currency board, not marked *de facto*; **or** when the comments state an
  official (announced) peg, band or board — a statement of announcement, which the class's *de facto*
  mark does not override.
- **S2 — L2 (headline)**: that arrangement ends, and what follows is a float (managed or free), freely
  falling, or dual or multiple rates in place of the peg, with no comment saying an official peg or link
  continues; or the comments word the end (abandoned, ended, floated, band eliminated, peg broken).
  `clear` when the comments word it; `judgement` when only the classification shows it. Both are
  headline; **the `clear`-only list is a variant**, reported beside.
- **S3 — not L2**: a successor that is a *de facto* peg, crawl or band (the same rate may be held de facto:
  value), a new level or anchor within a kept announced arrangement, or a peg the comments still call
  official — unless the comments word the official arrangement's end (S2).
- **S4 — a widening** — a peg to a band, a band to a wider band — keeps a limit: **`L2-var-widened`**, a
  variant set apart. A band **eliminated** is L2.
- **S5 — before 1946**: the chronologies classify from 1946, and M0 reads L2 and H1 over 1946–2016; an L2
  or H1 dated before 1946 is set apart ("before the classification's span"). A gold or silver standard
  suspended is **R1** (*redemption* gives way), frame a's list (M4), never L2: set apart, "R1: frame a's".
- **S6 — H1** needs a dated decision making another money legal tender, or legal for domestic contracts
  (official dollarisation or euroisation, a multi-currency system by decree). **Not H1**: a foreign money
  already legal tender at the table's start (the baseline, no decision); a money that replaces the old one
  (a new money, M0 section 1); joining a currency union (a competing exit, M0 section 4); "also legal
  tender" with no decision recorded.
- **S7 — the euro, or any currency union joined**: a competing exit, neither L2 nor H1.
- **S8 — the devaluation variant**: stated in the text, within a kept announced arrangement (S1), with its
  size where given ("size not stated" otherwise); undated in the text, it is dated at its period's start,
  at year precision, `judgement`, "undated in the text". A devaluation under a class that is not an
  announced arrangement is not coded.
- **S9 — force (phase 4, kept apart)**: controls imposed, introduced, reimposed or tightened as the
  comments word them, or a period whose class names capital or exchange controls, dated at its start
  (`judgement`). Controls "already in place" with no date are not coded. Force before 1946 is kept: M0's
  check before 1946 reads phase 4 where the chronologies reach.
- **S10 — a table covering two economies** (Curaçao and St. Maarten) is coded on both codes, one row each.
- **S11 — the date**: the start of the period that follows, as printed; where the comments give the
  announcement's own date, that date.

### 3b. The residual cases, settled after the second pass (before the third)

Under S1–S11, L2's κ on the sample rose to **0.89**; H1 and force agreed. The five disagreements, and the
cases the coders named as unsettled, fall into five kinds, settled by the same text:

- **S12 — a peg known only from the comments** (S1's second clause, under a class that is not an
  announced arrangement) **ends only where the comments word its end**: abandoned, ended, terminated,
  "until" or "through" a date, or another official regime named ("officially it is a managed float").
  Silence — a later period whose comments no longer mention the peg — records no end: not coded. A peg
  the class itself shows (S1's first clause) still ends by the class (S2).
- **S13 — a time-bounded official peg** ("until", "through", "from … to" a date) is L2 at the end's date
  (the start of the next period), `judgement`, whatever follows — a de facto peg included (the official
  arrangement's end is worded, S3's exception) — **unless an official peg to another anchor follows**:
  an anchor change (S3), not coded. The same for "the peg … was ended" when an official peg to another
  anchor follows.
- **S14 — an end inside a gap** of the printed periods (the table has no row for the months between)
  cannot be dated: not coded, said in the country's note.
- **S15 — a mixed class** ("Managed floating/De facto crawling band"): its **first-listed component**
  decides, for the class before and the class after alike.
- **S16 — a peg the comments keep official while the class moves to a band** ("officially pegged to a
  basket" under a moving band): a kept official peg (S3), neither L2 nor a widening.

### 3c. The third pass, the last reading, and the merge

Under S12–S16 the sample's L2 κ was **1.00** — but the third pass named to each coder the rows the
residual rules touched, disagreements included, so it overstates independent agreement: **the second
pass's κ, 0.89, is the independent measure**, reported with it.

- **S17 — a "parallel market" first-listed after a peg** is two prices recorded (claim 5's phase 3, M0's
  market split), not an announced end: not L2 unless the comments word the end. A **dual** market — two
  official rates — stays in S2's list. Applied by the session to the two lines it touches (Syria 1948,
  Turkey 1939), written in the manifest. *Said* (the audit's M2): S17 was written after the merge showed
  its two lines, a rule fixed on the cases it judges.
- **The list** is the four first coders' third pass; the second coder's file is kept beside it as the
  reliability record, never merged. **`L2-var-silent`**, a variant set apart: the lines the second pass
  coded and S12 dropped (a peg known only from the comments whose end is not worded — Thailand's and
  Indonesia's 1997 floats among them), so that S12's weight can be read; the silent cases no pass ever
  coded as lines are named in the manifest, not rebuilt.
- **Force's dates** (phase 4) are kept in the dataset's folder as their own file, never in `series.csv`
  (M0 section 2: force is not an act of this list), for the phases list to read.

### 3d. The deep audit answered (before the list's second build)

`bank/checks/FT-001-M3-acts-2026-09-30-opus-audit.md` — ready, no B; O1–O4, M1–M15. Answered here, then
the list rebuilt, still before any outcome list:

- **O1 — T2 from 1960 per creditor class.** "The first year of a stock" (M0) is read **in each of the
  database's creditor columns** (the IMF, IBRD, IDA, IADB, the Paris Club, China, other official
  creditors, private creditors — foreign-currency bank loans and bonds —, local-currency debt, fiscal
  arrears): a year whose stock in that class is above zero while the year before was read and zero — as
  *Varieties* is read per type before 1960. Several classes starting the same year are one line, the
  classes named. The total-stock reading of the first build, and the private-and-local-currency-only
  reading, are variants; each line carries the new stock's size, and the manifest prints the act count
  by class and by size (no size floor: M0 names none, and the count is shown).
- **O2 — L2's headline follows M0's text**: *abandoned by an announced decision*. **Headline L2 is a
  `clear` line** (the comments word the end, S2, S12, S13 — *amended at the second build*: S13's own
  lines are `judgement` by its rule, a bound dating the end with no decision worded, so they form the
  variant `L2-var-bounded`; a line that S12 and a time bound both touch stays `clear` where the comments
  word the abandonment itself, Haiti 1991-09-16); **a class-only end is the variant
  `L2-var-class`**, printed beside — this reverses the first build's choice, since a class change is IRR's
  reading of the rate beginning to move (M0: "value"), and the audit's null simulation puts claim 1's
  "after an act" 2–14 points above its base rate with it. **A freely-falling class is read by its next
  component** (M0 §1: class 14 is defined by inflation and never used; the chronologies' own note, p. 3):
  the eleven lines it created are re-read.
- **O3 — force**: its file is counted by era in the manifest (50 before 1946, 13 in 1946–2016, 2 from
  August 1971); the lifts the text dates are coded as end dates in the same file; that phase 4 cannot
  carry claim 5 (ii) in the fiat era is written for M0's next version (plan, "For M0's next version").
- **O4 — `L2-var-silent` rebuilt by rule** in one pass over all 197 tables: every peg the comments state
  as official, followed by a float or freely-falling class, its end not worded.
- **M-items**: the header names v4.2 (M1); S17 said to be fixed after its lines (M2, in 3c); apart lines
  carry `headline=no` (M3); an economy whose first year holds a stock is noted in `coverage.csv` (M4); no
  World Bank aggregate is an economy (M5); the Soviet Union's years to 1991 on `SUN` (M6); **H1**: S6's
  "a money that replaces the old one" means a new unit of the same issuer — official dollarisation
  (Ecuador 2000, Zimbabwe 2009) is H1, the case M0 names, said with its date after the crossing (M7);
  devaluations with no stated size are `L2-var-devaluation-unsized` (M8); L2 and H1 coverage ends
  2016-09 (M9); act rates per economy-year of coverage (M10); the audit's out-of-sample re-coding (6 of 6
  headline lines) reported beside κ (M11); Garriga's contradictory flags noted (M12); Argentina 2001
  dated by the text's own date of the dual market (M13); the three passes' files and the sample archived
  in the dataset (M14); no T1 or crawl-step line, said (M15).
- **Readings settled in writing the second build** (before it ran; no act count read before they were
  written except O1's own class columns' blank, zero and positive cells):
  - *Reading*: in `Debt_2025`, **a class left blank in a year whose `TOTAL` is read holds no stock** (the
    database leaves blank what it does not hold: of the 8,684 economy-years whose total is read, World rows
    out, 868 to 8,245 leave a class blank); a year whose `TOTAL` is blank cannot be read, in every class.
  - The classes are read as the database prints them; **they can overlap** (their sum exceeds `TOTAL` beyond
    rounding in 2,435 of 8,684 economy-years), so a line's `value`, the sum of its new classes, is an upper bound on the
    new stock, and each class's stock is printed in its note. `PRIVATE_CREDITORS` is read as one class (the
    audit's ten), never as foreign-currency loans plus bonds, which do not sum to it.
  - The private-and-local-currency variant is `T2-var-private`: the first year of a stock in
    `PRIVATE_CREDITORS` or `LC_DEBT`; the first build's reading is `T2-var-total`.
  - The database's one line for the USSR and the Russian Federation is **one series**: its years to 1991
    on `SUN`, from 1992 on `RUS`, and 1992 is compared with 1991 (so no first year is lost at the seam).
    The database's "World" rows are not an economy (M5).
  - L3's target half has coverage rows: Hammond's 27 from their formal adoption year (M1's Appendix A),
    Finland, Spain and Slovakia with no adoption year, all readable to the start of 2012.
- **The third build** (the small check `bank/checks/FT-001-M3-acts-2026-09-30-sonnet-small-check-v2.md`,
  not ready, F1 blocking), still before any outcome list is read by this list:
  - **An eleventh class, `UNASSIGNED`**: the stock `TOTAL` carries and no class holds (`TOTAL` less the
    ten classes' sum, when positive), read in the same way as a class. Without it a default the database
    leaves unassigned is invisible (Argentina 2001: `TOTAL` US$84,830m, every class blank; Mexico 1982,
    Venezuela 1983, Greece 2012, Lebanon 2020). A remainder within the rounding of the eleven printed
    figures (each to US$0.01m: 11 × 0.005) is none — 108 remainders of exactly 0.01 are rounding.
  - The headline L2's reliability: the 20% sample held no `clear` line, so a sixth coder re-codes, blind,
    the 20 tables that carry the 21 headline lines and 20 others drawn with seed 1797; the agreement on
    `clear` ends is printed beside κ.

**Phase 4 — force** is **not** an act (M0 section 2: controls imposed after strain are claim 5's phase 4, a
response). The same reading can date *exchange controls imposed or tightened* for the phases list; those
lines are kept apart from this list, in `ft001-phases` when it is built, which follows this list (M0's twin,
`case_line.follows`).

## 4. The checks before the commit

- `missions/code/m0.py`'s `list_problems` on `series.csv` (the lock at 3163162, the case line, the order);
  `ft.data.reconstructed.problems("ft001-acts")` empty.
- **This list is committed alone and first**, before any list of frames b, c or f or the phases (the twin's
  `case_line.follows`, checked by `m0.py`). Nothing of frames b, c, f or the phases is computed before that
  commit.
- The manifest says: the sources and their vintages; each step in order; the act rate **by source** (M0
  [a-R4]); the coders and κ; every *reading* this file chose; what cannot be read and where.
- **Audit**: the deep mission audit (`.claude/skills/ft-map/mission-audit-brief.md`), which re-codes a sample
  itself.

## 5. What this protocol cannot hold

- That nobody looked at an outcome before coding the acts: the order of commits holds the lists, not the
  coders' memory (M0 section 3) — the chronologies' comments themselves speak of outcomes, so the barrier
  is the protocol's condition 2 above: an L2 needs a recorded decision.
- The chronologies stop in September 2016. The authors' later version sits on `www.ilzetzki.com`, a wall
  when this protocol was written, opened by Sami on 2026-09-30 (request 1d8eeccdef2b): reading it is a
  later build under this protocol, never a patch of this one.
- Garriga ends in 2023, the Bank of Canada–Bank of England database with its 2025 edition, *Varieties* in
  2010 (used to 1959 only).

## 6. Declared for the frames

- **The euro's acts**: T2 is coded on member states; M0 does not say whether a member's default is an act
  on the euro's *taken back* support. The frames must say, before counting a euro spell.
- **Economies and monies**: an act is coded on the economy the source names; a territory or union the
  sources code apart (a currency union's members, the CFA franc zone) is coded as the source codes it, and
  the frames map economies to monies.
