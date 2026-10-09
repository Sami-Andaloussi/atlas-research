# FT-001 — M3: frame k, flee or stay (claim 3, told)

> Part of mission M3 ("the acts and phases", then "frame k, and the told timeline") of
> `bank/dossiers/FT-001-the-life-of-a-money.md`, section 14. The E2 session (`plan/e2-ft001.md`) wrote it on
> 2026-10-01, **before any frame k entry is computed**, and committed it alone first.
>
> **The rules are M0's**, version 4.2 (`FT-001-M0-rules.md` and its twin, commit 3163162):
> - section 5 k (the entry);
> - section 6, claim 3 (told: the cells, the measures, the strata);
> - section 2 (force's reader, ka_open);
> - section 1 (the regime carried after 2016; censoring);
> - the dossier's claim 3 paragraph.
>
> It adds no rule. Where M0 leaves a reading open, it says so and chooses in the open (marked *reading*),
> for the audit to judge. **Claim 3 is told**: this list shows, it never concludes. No margin, no verdict.
>
> **What was seen before writing**:
> - the frozen series' names and coverage, as `FT-001-M3-sources.md` prints them (IFS `FIDR_PA`, `PCPI_IX`,
>   `FDSBC`, `14A`, NGDP, ENDE; BOP net errors and omissions and the financial account's assets);
> - Chinn–Ito's `ka_open` (1970–2023);
> - Ilzetzki, Reinhart and Rogoff's classification and anchors (1946–2016);
> - Laeven and Valencia's workbook's sheet names;
> - the Direct Contiguity zip's file list (frozen today, `cow/direct-contiguity-v3.2`).
>
> No deposit return, cell or measure was read for this file.

## 1. What is listed, and where it goes

`data/reconstructed/ft001-k/`:
- `series.csv`: one case line per entry, in M0's case-line format, with its cell, its measures and its strata;
- `shown.csv`: the told table, open against closed within each stratum, with n in every cell;
- `MANIFEST.md`;
- the variants as `variant-<name>.csv` (section 6).

The twin's `case_line.follows` names no predecessor for frame k. *Reading*: the list reads no other
reconstructed list, so it follows none.

## 2. The entry (by script; M0 section 5 k)

- **The real deposit return** of a money-year is the deposit rate less π: IFS `FIDR_PA` (annual, % a year)
  less π (annual, %). π is read by the panel's annual reader in M0's source order, as frame b reads it.
  - *Reading*: M0 writes "the deposit rate less π", so the difference is arithmetic. The Fisher form
    (1 + i)/(1 + π) − 1 is the variant `fisher`.
- **A run**: N = 2 consecutive years [1; 3] whose real return is below −5% [0; −10]. **The entry is the last
  year of the run**, so it is known when it is dated.
- **From 1970**: the entry year is 1970 or later; a run may begin before it.
- **One entry per window W** (W = 3 [2; 5]): after an entry at t, no entry of the same money is dated in
  t + 1 … t + W.
- A year whose deposit rate or π cannot be read **breaks a run**. It is neither below nor above the line, and
  no run spans it.
- **A money-year under a deposit freeze cannot be read** (M0). The freezes are Laeven and Valencia's
  (`laeven-valencia/systemic-banking-crises-2026`, the "Crisis Resolution and Outcomes" sheet's
  deposit-freeze column, with its years). A run that touches a freeze year is broken as an unread year. An
  entry whose W window holds a freeze year is *cannot be read*.
  - *Reading*: the freezes are those of systemic banking crises only; a freeze outside one is not seen.

## 3. The cells (by script; M0 claim 3)

Cells are read **at entry and in the year before** ("as they stood at entry and for at least 12 months
before it", read on annual sources).

- **Forced**: `ka_open` at or below 0.25 [0.1; 0.5] (Chinn–Ito, 1970–2023), or a ban on residents holding
  foreign money.
  - No frozen source dates the bans year by year (AREAER's text is behind a sign-in). So **forced is read on
    ka_open alone**, said.
  - After 2023, ka_open cannot be read, and neither can the cell.
- **A substitute at hand**: foreign-currency deposits legal for residents, foreign cash legal to hold, or a
  land border with an economy whose legal tender is the dollar or the euro. Never a parallel market, which is
  flight itself.
  - **The land border** is a Direct Contiguity type 1 pair (land or river) in the year. "Whose legal tender is
    the dollar or the euro" means Ilzetzki, Reinhart and Rogoff's fine class 1 ("no separate legal tender"),
    with an anchor of the US dollar or the euro (the Deutsche mark before 1999 is not the euro), in the year.
    - The euro area's members from their entry also count, since the euro is their legal tender (the ECB's
      member list, `frame-a/ecb-euro-area-members`).
    - Contiguity runs to 2016, and the classification to 2016: later years read the 2016 state carried
      (M0 section 1), flagged `regime_carried`.
  - **Deposits and cash legal**: no frozen source dates them year by year. So "a substitute at hand" is read
    **yes** only through a border; otherwise it is **not read**.
- **Open** = not forced and a substitute at hand. **Closed** = forced, *or* not forced with no substitute.
  - *Reading*: a not-forced money with no such border cannot be called closed, since its deposits may be
    legal. Its cell is *cannot be read*, said. In practice, then, closed means forced, and open means not
    forced and bordering a dollar or euro economy. The manifest says how thin this leaves each side.
- **A money whose cell changed** between the year before and the entry is *apart* (M0).

## 4. What is shown (by script; M0 claim 3)

Over **W = 3 years** [2; 5] from the entry (t → t + W), side by side, each with its blind spot said:

- **m1** — local-currency money: *cannot be read* for every entry. IFS splits residents' deposits by currency
  for one area only (35B/35X), and the bans that would make deposits all local are not dated. The column is
  carried, empty, with its reason.
- **m1c** — currency: Δ log real currency from t to t + W. Currency is IFS `FDSBC`, with `14A` before a
  money's first survey reading. It is deflated by IFS `PCPI_IX` (one CPI, as in the phases list). A source
  seam inside the window makes it unread, flagged `seam`.
  - Blind spot: it misses the main road out in open cells, from local deposits into home foreign-currency
    deposits.
- **m2** — what crosses the border: the sum over t + 1 … t + W of residents' net acquisition of foreign
  financial assets **excluding reserve assets** (BOP `BFOA` + `BFPA` + `BFDA` + `BFFA`, BPM6, US dollars),
  plus net errors and omissions taken as outflow when negative (`BOP_BP6_USD`). The sum is taken as a share
  of GDP in dollars (IFS `NGDP_XDC` over ENDE, the year average of the rate).
  - *Reading*: errors and omissions enter with their sign reversed, so that unrecorded outflows add to m2.
  - Blind spot: it sees only what crosses the border.
- **Each net of its own change** over the W years before entry (t − W → t), as the variants named `net`
  (M0: "each also net of its own change over the W years before entry"). They are shown beside the gross
  figures, not instead of them.
- **Strata**:
  - the real return's depth at the entry year: (−10, −5], (−20, −10], −20 or worse;
  - π at the entry year: below 20%, 20–40%, 40% or more.
- **The table** (`shown.csv`): for each stratum and each measure (m1c, m2, gross and net), n open, n closed,
  the mean and median of each, and the open-minus-closed difference of means. **n is printed in every
  cell.** No margin, no test, no verdict.
- **Censored**: an entry whose window t + W runs past the measure's data end is *censored*, apart (M0;
  [conf-N3]). The annual common end is 2025; IFS ends in 2024.

## 5. Statuses

- **Counted** (shown): a cell read open or closed, unchanged over the year before, and a window fully read
  for at least one of m1c and m2.
- **Apart**: a cell changed in the year before (reason written), or censored (M0's *censored*).
- **Cannot be read**: the cell cannot be read, a freeze inside the window, or neither measure read.
- War is not a condition of frame k in M0. The war years inside the window are flagged `war_in_window`, as
  information only, said.

## 6. Variants (M0's brackets, and the readings)

- `N1`, `N3`: the run's length;
- `line-0`, `line-10`: the line at 0% and at −10%;
- `W2`, `W5`: the window, which also sets the one-entry spacing and the measures' span;
- `kaopen-010`, `kaopen-050`: forced at 0.1 and at 0.5;
- `fisher`: the Fisher real return;
- `net`: the measures net of their own change before entry (shown in `shown.csv` beside the gross ones).

## 7. What the build prints before any measure is read

- the entries by year and status;
- the cells: open, closed, apart, *cannot be read*, and the reasons;
- the sources' coverage per measure.

It prints no measure.

## 8. Order of commits, checks and audit

1. This protocol alone.
2. `frame_k.py` and `test_frame_k.py`, on synthetic series, green before any real series is read.
3. The coverage-only run; then the build, with `m0.py list_problems` (the lock) and
   `ft.data.reconstructed.problems` empty before the commit.
4. A deep audit (Opus, isolated). No rule here may read a money's later holdings to place an entry or a
   cell; the audit checks it with a null simulation in which holdings are drawn independently of cells.

*The barrier*: the commit order, the synthetic tests, the null. *What no code holds*: that the cells' thinness,
which is said, is not read as an answer. Claim 3 is told, and its page in part 1 says what the table cannot
show.

## 9. Readings settled with the code (2026-10-01, before any entry, cell or measure was computed)

The producer (a Sonnet agent) inspected the frozen files' structures only and named its readings K1–K14 in
`frame_k.py`'s docstring. The session settles these, before the coverage run:

- **The freeze sheet** is Laeven and Valencia's "Resolution Details" (Deposit Freeze: date and duration in
  months), not "Crisis Resolution and Outcomes", which has no freeze column. This is a fact of the file;
  section 2's rule is unchanged.
- **The dollar's issuer counts.** M0's "an economy whose legal tender is the dollar or the euro" includes the
  United States, as the euro's members are included. The **headline** reads a land border with the United States
  as a substitute at hand. Variant `class1-only`: only economies with no separate legal tender (fine class 1,
  anchor USD or EUR) and the euro's members.
- **m2 without derivatives.** Financial derivatives (BFFA) are read for 169 monies against about 200 for the other
  parts, and a derivatives position is not a holding of foreign money. The **headline** m2 is BFDA + BFPA + BFOA
  less net errors and omissions (sign reversed, K10). Variant `with-derivatives`: BFFA added, all parts required.
- **The exchange rate** for GDP in dollars is IFS's end-of-period rate (`ENDE`, as the file gives it), not the
  year average section 4 named. No year-average rate is frozen. Said.
- **K1–K14 as written** in the docstring, said in the manifest: an unread end makes a cell *cannot be read*;
  censoring uses each measure's panel end; runs need not be fresh; a frozen entry keeps its place in the spacing;
  the neighbour's class is read in the year itself; the units-glitch screen is reused for m1c; a money that is
  itself dollarised or a euro member is not excluded; `shown-variants.csv` holds each variant's table.

## 10. A currency union is not the dollar or the euro (2026-10-01, after a first build that was not committed)

The first build's seven open cells showed Liberia and Nigeria "open" through CFA-franc neighbours: Ilzetzki,
Reinhart and Rogoff's fine class 1 is "no separate legal tender **or currency union**", and the CFA zones are
anchored to the euro. Their legal tender is the CFA franc, not the euro. Section 3 read M0's "an economy whose
legal tender is the dollar or the euro" too widely. **Back to M0's text**: a member of a currency union with a
money of its own (the West African and Central African CFA francs and the Eastern Caribbean dollar,
`frame_a.UNIONS`) is never a dollar or euro economy. The euro's members and the United States are, as section 9
says. This was found after a build whose outcomes were seen. It is a correction to M0's wording, not a choice
among readings; the manifest says so. The first build was not committed.

## 11. Readings amended after the deep audit (2026-10-01, before the second build)

The deep audit (`bank/checks/FT-001-M3-frame-k-2026-10-01-opus-audit.md`: not yet, B1 and B2) reproduced the
build row for row and confirmed the null over 440 runs. The session follows it on every finding.

- **B2 — war at entry** (M0 section 1, its twin's `entry_in_war_year: apart`, and section 8). Section 5's
  "war is not a condition of frame k" misread M0, and is struck.
  - An entry in a war year is *apart*. An entry whose war year cannot be read is *cannot be read*, as in frame
    c's R14.
  - Variant `war-in-window-apart`: also sets apart an entry with a war year inside its window, as the twin's
    variant does.
- **B1 — the carried regime.** After its last year read (the anchors to 2015, the classes and contiguity to
  2016), each is carried from its own last year, flagged `regime_carried`.
  - Variant `no-carry`: no year after the sources' end is read (O3).
  - Zimbabwe's own money returns in 2019, which the carry cannot see. Said.
- **O4 — the dollar and euro economies, by a full list.** Section 3's rule is applied economy by economy over
  every class-1 money with a USD or EUR anchor. The list is written in `frame_k.py` (`DOLLAR_EURO`), with a
  reason for each economy, and covers:
  - the United States and the euro's members;
  - the class-1 economies whose legal tender is the dollar or the euro;
  - excluded: currency union members (section 10), Eritrea to 1997 (the Ethiopian birr), Serbia 2001–02
    (the dinar), Vietnam 1950–55 and the Dominican Republic 1946–47;
  - added, where IRR has no anchor: Montenegro (euro from 2002), Kosovo (euro from 2002), Andorra and
    Timor-Leste (US dollar from 2000).

  The whole list was checked after the first committed build; it moves no headline line. Said.
- **O5 — not a money of its own.** An entry of an economy whose legal tender is another's money (the dollar or
  euro users above, and the CFA and Eastern Caribbean members, whose money is their union's, as frame a's
  R_STATUTE reads them) is *apart*, "not a money of its own" (M0 section 1).
- **O1 — GDP in dollars.** IFS `NGDP_XDC`, then the World Bank's GDP in local currency (frozen) where IFS has
  none. The World Bank segment is used only where it agrees with IFS within a factor of 2 in their common
  years, or where they have no common year (said, and flagged).
- **O2 — the rate.** The year average of IFS's monthly `ENDE`, all twelve months read, as section 4 named.
  Otherwise the GDP in dollars cannot be read.
- **Minor.**
  - M4: variant `neo-negative-only`, in which only a negative balance adds, as section 4's sentence read.
  - M3: the manifest lists the money-years below the line that the freezes removed, and how Argentina 1989's
    duration was read.
  - M5: the twin's too-thin line (20 per side) is said beside n.
  - Censored lines carry the measures read so far (`m1c_so_far`, `m2_so_far`).
  - M1 and M2: the manifest's counts and the closed cell's wording ("the capital account closed on
    ka_open").
  - ka_open's cluster at 0.2557, just above the line, is said; the variants 0.1 and 0.5 bracket it.

## 12. Settled with section 11's code (2026-10-01, before the second build)

- **Greece 1999–2000** is excluded from the dollar and euro economies: the drachma stayed its legal tender until
  its euro entry in 2001 (the ECB's list), whatever IRR's class 1 says.
- **The Dominican Republic 1946–47 stays** a dollar economy. The US dollar was its legal tender until the peso oro
  of 1947, so the audit's exclusion is not followed. Before 1970, it moves no entry and no cell.
- **The World Bank's GDP** is checked against IFS's in **every** common year (section 11), with frame k's own check,
  not the window's median rule (M4 section 18).
- The producer's readings K15–K23 are kept and said in the manifest:
  - the United States is the dollar's issuer, its money its own;
  - "not a money of its own" comes first in the statuses;
  - `no-carry` drops 2016 for IRR's spans;
  - the `regime_carried` flag is broad;
  - an unreadable war year inside the window does not set an entry apart in `war-in-window-apart`;
  - Andorra is read as using the euro from 2002.

## 13. A World Bank GDP with no common year is not used (2026-10-01, after the second build was run, not committed)

The second build was run and not committed. Its all-strata m2 means for closed cells were about 5 × 10¹⁰ % of
GDP, which no outflow can be. The lines behind them were Venezuela 1988, 1995, 2004, 2008 and 2012, the only
entries flagged `gdp_no_overlap`.
- IFS has no `NGDP_XDC` for Venezuela. The World Bank's GDP in local currency is in today's bolívar, after the
  redenominations of 2008, 2018 and 2021, about 10¹⁴ older units in all. IFS's rate is in the units of each
  year. So the dollar GDP was wrong by a factor of about 10¹¹ to 10¹³.
- **Section 11's O1 allowed a World Bank segment with no common year** ("said, and flagged"). Without a common
  year, nothing checks that its unit is the rate's unit, so the rule is changed: **a World Bank segment with no
  common year with IFS is not used.** GDP in dollars is then not read in those years, and m2 cannot be read
  there. The `gdp_no_overlap` flag goes; the reason names the missing check.
- This moves Venezuela's m2 alone among the entries. The monies with World Bank GDP, a rate and no IFS GDP are
  CUB, CUW, FRO, PYF, GRL, IMN, NCL, SXM and VEN.
- **This was found after the second build's values were seen**, and is said as such in the manifest, as section
  10 was. The other large m2 values seen (Timor-Leste, Macao, Zambia 1986, Eswatini 1986, Angola 2004, Papua
  New Guinea 2003, Seychelles 2009) were checked against their GDP in dollars, which reads in the right range,
  and are kept.

## 14. The narrow re-check answered (2026-10-01, before the third build)

The narrow re-check (Opus, isolated: `bank/checks/FT-001-M3-frame-k-2026-10-01-opus-recheck.md`) found the second
build's files and manifest consistent with the code. Its verdict was **not yet**, with two Bs and eight Cs. Each is
followed.
- **B1: a unit break inside IFS's rate.** Belarus's monthly rate jumps about 11,200 times between December 1999
  and January 2000 (the redenomination). Its dollar GDP for 1992–1999 is about 10¹⁴, and m2 for BLR 1998 reads
  near 0 instead of about −2%. Section 13 checked GDP against GDP and never the rate's unit.
  - **The rule**: GDP in dollars is screened for units. A year whose dollar GDP differs from the year before's
    by more than a factor of **20** either way is a units break.
  - The segment **after the last break** is kept. Earlier years are not read, and their m2 *cannot be read*,
    flagged `gdp_units_break`. The latest segment is the reference because IFS's current units are.
  - *Reading*: a factor of 20 in one year is beyond any dollar GDP's real move, collapse or boom. The report
    lists every break, so one that is real would be seen.
  - The same screen covers Ecuador to 1999 and the World Bank segments in another unit before their common years
    (Iraq, Guinea-Bissau, San Marino), which carry no m2 today.
  - A test reproduces Belarus's shape.
- **B2: the headline counts nothing after 2007.** `war.py` cannot read war after 2007 (its W9: COW's war files
  end there). Every entry after 2007 is *cannot be read* at its entry year, so no line reaches *censored*.
  - **The variant** `war-unreadable-as-no` reads an unreadable war year at entry as no war, as frames c and d
    do. The deep audit asked for it; it was not built.
  - The manifest says that **the headline's counted list runs 1970–2007**. The variant carries the later
    entries and the censored lines' so-far values.
- **The Cs**, all in the manifest:
  - C1: m2's blind spot also includes dollar GDP at official rates far from the market, which bias m2 down on
    the closed side.
  - C2: "where holders could not leave easily" becomes "where the capital account was closed on ka_open".
  - C3: the war reading is described by `war.py`'s W9.
  - C4: the four items section 11 promised are said: Zimbabwe 2019, ka_open's cluster at 0.2557, that the
    dollar-euro list moves no headline line, and the war-at-entry lines that show as *cannot be read*.
  - C5: the Ukrainian freeze years are money-years, not entry years.
  - C6: m2's coverage is limited by the cause actually found (BOP gaps and missing GDP).
  - C7: Zambia 1986's level is one year's errors and omissions.
  - C8: Venezuela's entries are counted from the build.

## 15. War years after COW's coverage (2026-10-01, before the fourth build)

Frame k reads war years through `war.py` (via `strain.py` and `panel.war_at`). W12 and W13 of frame a's protocol,
section 22, now read test (b) after 2007 from UCDP v26.1. A state-year becomes **no** where the state is party to no
conflict of cumulative intensity 1; otherwise it stays *cannot be read*. K25's lack of a headline count after 2007
is lifted wherever W12 reads *no*.
- The variant `war-unreadable-as-no` stays, for the years still *cannot be read*.
- The third build's reading (`ucdp=False`) is kept as a variant, so the move is seen.
- No frame k line has been read for this section.

## 16. AREAER as a second yardstick, 2011–2023 (2026-10-02, before the fourth build; gap G11)

The IMF's AREAER editions 2011–2023 are frozen (`frame-a/areaer-2011-2023`, Sami's hand). Each edition has a
summary table of features by member, which says whether residents may hold foreign exchange accounts at home. The
headline is unchanged: it keeps one rule over the whole span (sections 3 and 14), and AREAER covers only its end.
AREAER enters as **a variant, `areaer`**, as G11 says:
- **Forced** is also *yes* where the table prints that residents may **not** hold foreign exchange accounts at
  home. That is the "ban on residents holding foreign money" of section 3.
- **A substitute at hand** is also *yes* where it prints that they **may**. Those are the "foreign-currency
  deposits legal for residents" of section 3, until now not dated.
- **The year.** A cell is read at entry and in the year before (section 3). Each year is read from the edition
  whose table states the position at that year's end, by the table's own "as of" date. A year no edition states
  stays as the headline reads it.
- **Who reads.** A Sonnet reader transcribes the row for frame k's 33 economies with an entry from 2011 to 2023,
  and for the years 2010–2023 only. It gets the economies and the years, and nothing of frame k's lines. For each
  economy-year it writes:
  - *permitted*, *not permitted*, *permitted with conditions* (kept as *permitted*, said) or *not printed*;
  - the edition, page and "as of" date.
- **Sampling.** An isolated Sonnet re-reads a sample of 20% (seed 1797), drawn from all the reader's
  economy-years.
- The code reads that table (`data/reconstructed/ft001-k/areaer/resident-fx-accounts.csv`), and only in the
  variant.
- No frame k line has been read for this section. G11's row says it cannot move a conclusion; the variant shows
  whether it does.
- *Readings settled with the code* (K26–K27, 2026-10-02):
  - a *permitted* year with no ka_open stays *cannot be read*, since forced cannot be told;
  - a *not permitted* year is *closed* even with no ka_open, since AREAER alone makes forced *yes*;
  - ka_open at or below the line stays *closed*, whatever the table says;
  - a malformed table raises, and a missing table writes no variant.
  - `war-moves.csv` compares the entry year's war reading only. W12 turns *cannot be read* into *no*, never into *yes*,
    so it makes no window year a war year in any variant: `war-in-window-apart` moves only through the entry year's
    reading, which `war-moves.csv` lists (reworded 2026-10-02 after the fifth-build narrow re-check, N7).
- *What the reading found* (2026-10-02; `data/reconstructed/ft001-k/areaer/README.md`):
  - **The summary table has no resident-accounts row** in any edition. The feature is printed in each country's
    chapter ("Resident Accounts": "Held domestically", with "Approval required"), and only the full editions
    have chapters: 2011, and 2019–2023. The 2012–2018 Overviews have none.
  - So the years read are 2010 (the 2011 edition, as of 31 December 2010), 2018, and 2020–2023. The 2020–2023
    editions state the position at 30 June, and each is read as its year's, said. 2011–2017 and 2019 are *not
    printed*.
  - Status follows the printed marks alone: *permitted with conditions* is Yes with approval required. Narratives
    that limit who may hold the accounts are kept in `note`.
  - Over 462 economy-years, after the session's Venezuela change below: 150 *permitted*, 40 *with conditions*, 1
    *not permitted* (Venezuela, 2010), and 271 *not printed*.
  - With a cell read at entry and in the year before (section 3), the variant reaches only the entries whose
    two years both fall in 2020–2023 (or 2010 and 2011, of which 2011 is not printed). That is said, and G11's
    "cannot move a conclusion" stands unless the variant shows otherwise.
  - **The re-read** (Sonnet, isolated, blind, 93 economy-years, seed 1797) agrees on all 93 statuses. The 2022 and
    2023 editions state Venezuela as of end-June 2021, so VEN 2022 and 2023 are set to *not printed* by the
    session.
