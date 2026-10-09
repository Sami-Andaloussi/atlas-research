# FT-001 — M4, first part: frame a's four panels, coded before any value or trust

> Mission M4 (frame a; A3's premiums are not in this file) of `bank/dossiers/FT-001-the-life-of-a-money.md`,
> section 14. Written for the E2 session (`plan/e2-ft001.md`), 2026-09-30, **before any list of frame a is
> coded**, to be committed alone first: the coders' protocol M0 section 3 asks for, on the model of
> `FT-001-M3-acts.md`. **The rules are M0's**, version 4.2 (`FT-001-M0-rules.md` and its twin, commit
> 3163162): section 5 a and the twin's `frames.a`; section 1 (*convertible*, the eras, war); section 2
> (*redemption*'s acts R1 and R2, *a limit by institution*); sections 3 and 4 (the case line, the coders,
> censoring); section 7's A2. This file adds no rule; where M0 leaves a reading open it chooses in the open,
> numbered **P1–P29**, for the audit to judge.
> **What was seen before writing** — the four panels' source documents, which are lists of dated support
> changes: Meissner's Table 1 (from the page image); Bernanke and James's Table 2.1 (chapter) and Table 1
> (w3488), their note 7 and the chapter's paragraph on the return to gold; Hammond's Table A with its
> numbers masked, the row labels and row 1.4 of her first four country tables, her printed page 7 and
> footnote 3 of printed page 13; Garriga's variable list and the DDI's summary statistics of her flags
> `creation`, `reform`, `direction`, `increase`, `decrease`, `regional` (their scale and implied counts; no
> index value); M1's Appendix A (Hammond's 27 dates as the map printed them); the acts list's 18 lines whose
> route is R1; M3's two protocols; the frozen manifests; web searches' titles and snippets (among them: a
> gold-standard period table for Italy, Portugal, Chile and Argentina, from a copy on a refused host, not
> opened; a Russian suspension in late July 1914, calendar unstated); the Guard's rulings. **Two slips**:
> (1) printing the text layer of Hammond's printed page 7 put the 27 targeters' names at their heights along
> Chart 1's axis of inflation at adoption, beside a sentence of hers on inflation at adoption — approximate
> values of panel 4's matching variable were on screen; not studied, not written down, and no reading below
> turns on them; (2) her row 1.7 (the current target) printed for four countries — policy parameters, not
> outcomes. No price, inflation, exchange-rate, money, deposit or reserve series of any economy was read.

## 1. What is coded, and where it goes

**The list** — `data/reconstructed/ft001-a/`:

- `series.csv` — one line per change of the four panels, and one per variant line the same sources give,
  set apart (`headline` = `no`, status *apart* with the variant named — the acts list's convention). Its
  columns are the reconstructed dataset's (`period` the change's date, `value`, `unit`, `source`,
  `locator`, `note`, `uncertainty`) beside M0's case line (`case_line.fields`), read for frame a:
  - `money` — below; `frame` = `a`; `route` = `a1` (1914), `a2` (1931–36), `a3-up`, `a3-down`, `a4`;
  - `entry_date` — the change's date (sections 2–5), at the source's precision;
  - `entry_measure`, `entry_measure_date` — **empty here** (P1): frame a's matching measure is π in the
    year before (M0 5 a), which is value — one of frame a's own measures — and is written only by the
    window build (section 7), after this list's commit;
  - `outcome`, `outcome_date`, `onset_date` — empty (P1): frame a counts no outcome; value and trust are
    read over the window and described (M0 section 6, "Where timing is read"; A2);
  - `responses` — the panel's own later dated changes of the same money inside the window, `type:date`
    (panel 2: the table's columns that did not date the exit);
  - `exit` — a competing exit inside the window (M0 section 4), `type, date, source`;
  - `status` — section 6 (*already under way* is not used: frame a has no outcome to be under way);
  - `source`, `locator` (PDF page, printed page, row and column), `coder`, `rules_sha256` (the pair's
    hash at 3163162).
  Added columns: `headline`; `support` (`redemption` for a1 and a2, `limit by institution` for a3 and a4);
  `act` — what dated the change (`suspension`, `exchange control`, `devaluation`, ties joined by `+`;
  `reform`; `target`); `war_year` (`yes` with the COW war, `no`, or *cannot be read*); `flags` (named in each
  section); panel 2's `bj_suspension`, `bj_exchange_control`, `bj_devaluation`; panel 4's `informal_start`
  and `applied_from`.
- `members.csv` — **every candidate of panels 1, 2 and 4**, one row each: the name as printed, its code,
  member or not, the reason and the source, or *cannot be read* where no named source settles it. A member
  with no change in the panel's span has no line in `series.csv` (it is a candidate non-changer, section 7);
  a member whose change cannot be dated at all has none either and is *cannot be read* here — **never "no
  change"** (M0's rule for a source's last year, applied to a source's coverage).
- `coverage.csv` — panel 3: for each economy, the first and last year Garriga codes and the years she
  leaves empty.
- `MANIFEST.md` — section 11.

**`money`** — as the acts list (`FT-001-M3-acts.md` section 1; `missions/code/economies.py`): the issuing
economy's ISO 3166-1 alpha-3 code, the ISO 3166-3 code of a dissolved state; the Russian Empire as `RUS` and
the Ottoman Empire as `TUR` (P2, *reading*: the economy the table names, under the code of the state that
continues it, as `economies.py` already maps "turkey/ottoman empire"); an economy with neither (the Straits
Settlements) takes a code from ISO's user-assigned range (`XAA`–`XZZ`), each printed in the manifest. A
union's money: panel 3 (P15).

**Dates** — `YYYY`, `YYYY-MM` or `YYYY-MM-DD`, at the source's precision, never finer. **Gregorian** (P3,
*reading*): a date a source gives in the Julian calendar (Russia before February 1918, Romania before 1919,
Greece before 1923) or the Ottoman fiscal calendar is converted when the source says which calendar it
uses; when it does not, the date stays as printed, flagged `calendar unstated` (thirteen days can cross a
month's end).

## 2. Panel 1 — the 1914 suspensions (hand)

**Candidates.** Every row of Meissner's Table 1 (`frame-a/meissner-w9233`, PDF page 8, printed page 7; read
from the page image, the text layer being scrambled): 37 economies with a year of adoption of gold
convertibility, and 13 marked "---" (no adoption before 1913). **And the United Kingdom** (P4, *reading*):
the table lists adopters, and the standard's anchor — on gold before every date in it — is not among them;
leaving it out would be a gap of the table's design, not a finding. It is a candidate like the others, its
standing read from the exit source below.

**Members — M0's "convertible on 31 July 1914", read at 30 June 1914** (P5, *reading*). A candidate is a
member if (a) Meissner gives it a year of adoption — the last where he gives several — or it is the United
Kingdom, and (b) the exit source records no suspension or end of gold convertibility between that adoption
and 30 June 1914. *Why 30 June*: M0's 31 July is its metal era's end; read to the letter, it would drop
suspensions of the same war crisis that a source dates in the last days of July, and a source that says
"July 1914" cannot place a suspension before or after the 31st. A suspension dated 1–31 July 1914 is the
member's change, flagged `before 31 July`; the letter (those members out) is a variant. Silver-convertible
monies are not members: Meissner's table is gold's. His "---" rows are not members whatever another source
says; gold members that a source names beyond Meissner are a variant, by source (`headline` = `no`).

**The exit source — M0's named source cannot give it.** Meissner dates adoptions, never exits, and several of
his adopters had left gold before 1914. What can: a table of gold-standard periods, from adoption to exit.
Named candidates, none frozen or opened here, all on `www.nber.org` (Guard: allow; section 9): Obstfeld and
Taylor (2002), NBER WP 9345; Mitchener and Weidenmier (2009), WP 15401; Bordo and Schwartz (1994), WP 4860;
Bordo and Rockoff (1995), WP 5340; Chernyshoff, Jacks and Taylor (2005), WP 11795. **Fixed now, before any
is read** (P6): the headline exit source is the one whose table gives gold-standard periods for the most of
Meissner's 37 dated adopters (counted on its list of economies, before any period is transcribed); ties in
the order listed; a candidate it does not cover is read from the next that covers it, in the same order,
flagged; **a candidate no source covers: membership *cannot be read*, never assumed convertible.** A first
year that differs from Meissner's is printed, never corrected: Meissner's year stands for the adoption (M0
names him), the exit source's years for exits. An exit year of 1914 given without a month leaves the member
in; its change is dated below.

**The change — R1 in 1914–15.** *Suspension* (P7, *reading*) is the dated decision — a law, a decree, a
government's or a central bank's decision — from which a holder can no longer redeem the money on demand, at
its stated rate, into gold or into the money its gold-exchange arrangement redeemed it into (M0 section 1's
*convertible*: on demand, by any holder). **Not R1**: an embargo on exporting gold, or pressure on holders
not to redeem, while redemption at home goes on — *convertible* still holds; its date is noted in `note` and
counted in a variant, by source. The span runs from 1 July 1914 (P5) to 31 December 1915. A member with no
R1 in it has no change (`members.csv`); an R1 after 1915 is noted there, never a panel-1 change; a parity
changed while convertible (R2) in the span is noted, not the change (M0 names the suspension).

**The dating source — again not Meissner.** Named candidates, in this order: Bordo and Schwartz (1994) and
Bordo and Kydland (1990), NBER WP 4860 and 3367, where their tables date the war's suspensions; Brown (1940),
*The International Gold Standard Reinterpreted, 1914–1934*, NBER, Book One ("Breakdown"); the *Federal
Reserve Bulletin*'s 1914 and 1915 issues (FRASER). **Fixed now** (P8): the candidate that dates, at month
precision or finer, the most members' suspensions heads; the others fill, in order, flagged; a member none
dates has its change *cannot be read* (a source that says only "1914" dates it at year precision: annual
window only). The acts list's two R1 lines dated in 1914–15, from the chronologies (India, August 1914;
Australia, July 1915, "suspension of gold shipments" — an export stop, not R1 by P7), are printed beside as
a cross-check, never replacing the headline source.

**Belligerents and neutrals** — section 6: a change in a war year is *apart* and told one by one; the others
are counted (M0 5 a).

## 3. Panel 2 — the exits of 1931–36 (hand)

**Candidates.** The 24 rows of Bernanke and James's Table 2.1, "Dates of Changes in Gold Standard Policies"
(`frame-a/bernanke-james-chapter`, PDF page 6, printed page 37): *return to gold*, *suspension of gold
standard*, *foreign exchange control*, *devaluation*. **The chapter (1991) is the headline** (P9, *reading*:
the published version); the working paper's Table 1 (`frame-a/bernanke-james-w3488`, PDF pages 55–56) is
compared cell by cell and every difference printed in the manifest (it leaves blank some return dates the
chapter gives) — never merged.

**Members — on gold at the end of 1929** (P10, *reading*): a *return to gold* dated on or before December
1929 (a span such as "August 1926–June 1928" read at its later date, the de jure return), and no suspension,
exchange control or devaluation dated on or before December 1929 — a date printed "December 1929" is on or
before the year's end and keeps its country out. A country with no return date is not a member. **The table's
dates stand**: a coder who remembers another month notes it and never uses it (a return the table dates in
1930 keeps its country out).

**Wolf's list where wider — cannot be read.** Wolf (2008), CEPR DP 6685: the PDF answers 403, the other
copies sit on refused hosts, and it is a purchase (GBP 6.00; Sami buys nothing now). M0 section 10: the panel
waits on it, declared, and **stands on Bernanke and James alone**; no other list is swapped in. *Variant, by
source* (P11): economies outside the table whose chronology (Ilzetzki, Reinhart and Rogoff, w23135, frozen)
records a gold standard suspended in 1931–36 while a gold peg stood at 31 December 1929 — the acts list's R1
lines are where the coder starts, the country's table is re-read for its standing at the end of 1929; where
the table does not reach 1929, *cannot be read*. A silver standard's end is not panel 2's.

**The exit — which column** (P12, *reading*). **Headline: Bernanke and James's own definition** (their note
7): the first of the three dates — exchange control, devaluation, suspension. *Why*: (1) it is the named
source's rule, fixed by its authors, who say in the same note that they would not date adherence by
exchange rates, money or prices — the barrier this study wants; (2) M0 section 1's *convertible* is
redemption on demand by any holder, which an exchange control ends for a money redeemable into foreign
exchange; (3) a devaluation that comes first is the parity changed while convertible, M0's R2. **The three
dates are all written on the line** (`bj_*`); `act` names the one that dated the exit (ties joined), and the
later ones go in `responses`. **Variant**: the first of suspension and devaluation only — M0 section 2 read
strictly, where controls imposed are force, "never an act of this list"; a member whose only change in
1931–36 is an exchange control then has no exit (noted in `members.csv`).

**The span — M0's 1931–36** (P13, *reading*): an exit dated before 1 January 1931 (the table has such a row, a
devaluation) is *apart*, "exit before 1931, outside M0's span", shown beside; a member with no exit by 31
December 1936 has no change. **Precision**: the month, as the table prints it; the acts list's R1 lines that
date the same event to the day are printed beside, never replacing the table's month.

**Runs** — section 6 (panels 1 and 2 only).

## 4. Panel 3 — Garriga's legal reforms (script)

**Source.** Garriga (2025), `garriga/cbi` (`Replication_ISQ_2025.tab`, 1970–2023). **Columns read, selected by
name before any row is read** (as `acts.py` does): `cname`, `ISO`, `year`, `reform`, `direction`, `increase`,
`decrease`, `creation`, `regional`, and for the variant `lvau_garriga`. **Never read**: `InflationCP`,
`InflationGDPdeflator`, `linf`, `inf_imp`, `inf_ln`, `GDPpc`, `unemp_imp`, `ka_open`, `wdi_trade`,
`p_polity2`, `ldv` — the file carries inflation beside the flags.

**The change**: a country-year with `reform` = 1 and `direction` = 1 (`a3-up`) or −1 (`a3-down`), dated the
year. **Up and down are two sub-panels, never pooled** (P14, *reading*: opposite changes; pooled, they would
cancel). `direction` disagreeing with `increase` or `decrease` is printed, and `direction` decides (M0 names
it). A reform whose `direction` is 0 is *apart*, "reform, neither up nor down" (the DDI gives the flag from
−1 to 1). `creation` without `reform` is not a change — M0 names her reform flags, and a new central bank is
the institution's start: noted in `coverage.csv`.

**Unions** (P15, *reading*). M0 section 1 makes a union's money one money (the euro from 1999). A reform
Garriga codes for a union's central bank — on its own row if she has one, or on **every** member in the same
year with the same direction — is **one change of the union's money**: one line, coded `EMU` for the euro
area (the World Bank's aggregate code) and otherwise the union's ISO 4217 code (`XOF`, `XAF`, `XCD`), its
members in `note`. A reform coded on some members only is a member's own statute inside a union: *apart*, "a
member's statute; the money is the union's". `regional` = 1 marks the candidates; euro members from 1999 are
read as a union's members whatever `regional` says.

**Coverage.** A country-year Garriga leaves empty is *cannot be read*, never "no reform". **A change in
1970–1972 is *apart***: its window starts before her record (M0 section 4), so a reform in the three years
before it cannot be seen.

**Variant** (M0): every year in which `lvau_garriga` moves by 0.05 or more from the year before, both read, up
or down — `headline` = `no`, *apart*. The index is `lvau_garriga`, as the acts list's L3 variant (P16,
*reading*: one index across the study; her weighted `lvaw_garriga` is not run).

## 5. Panel 4 — inflation-targeting adoptions (hand)

**Hammond's 27.** Her Table A (`frame-a/hammond-ccbs-29`, PDF page 11, printed page 9) names the 27 targeters
at the start of 2012. **Each is dated by its own country table, row 1.4, "Date IT adopted"** (printed pages
18 to about 45): frozen, so nothing is fetched for them; the coder reads the handbook, never M1's Appendix A
(the map's transcription, which the second coder may compare). **Chart 1 is never read**: it plots the
inflation rate at adoption, panel 4's matching variable (and its caption's "start of 2009" is a leftover, M1
row 20).

**Which date** (P17, *reading*): **the formal adoption** — Hammond's note to Chart 1 says the chart shows the
formal date, several countries having targeted informally before. Where row 1.4 gives an informal start and a
formal one (Ghana, Israel, Serbia), the formal one; where it gives an announcement and an application
(Sweden: an announcement in January 1993, applied from 1995), the announcement — M0 dates the adoptions after
2012 by the central bank's announcement, and acts by announcement (L2). The informal starts
(`informal_start`) and the application date (`applied_from`) are carried on the line, each a variant.
Precision as printed: three give the year only (annual window only).

**Adoptions that ended before 2012** (P18, *reading*). Hammond's printed page 7 names the only central banks
that had left targeting: Finland, Spain and Slovakia, each on adopting the euro. **They enter panel 4**,
flagged `exited before 2012`: M0's rule is *every* adoption, and the targeters at the start of 2012 alone
would keep only the adoptions that lasted — a selection on what came after (M0 section 8's third question).
Variant: Hammond's 27 alone (M0's parenthesis to the letter). **Their dates** (P19, fixed now, before either
is read): the adopting central bank's announcement (M0's rule where Hammond gives no date) — the Banco de
España's host is allowed, the Bank of Finland's and the National Bank of Slovakia's are refused (section 9);
where the announcement cannot be read, the first year the classification below gives, at year precision,
flagged; where neither is frozen, *cannot be read*. Their euro entry is a competing exit (section 6).

**Adoptions from 2012 — M0 names the dating document, not the list.** "The adopting central bank's
announcement" dates an adoption; it does not say which central banks adopted. **What can** is a classification
of every money-year, so that no central bank is searched case by case (M0 section 3), in this order, fixed now
(P20): (1) Cobham's classification of monetary policy frameworks (179 countries and currency areas,
1974–2023 in its 2024 update; `monetaryframeworks.org`, **Guard: deny** — a wall, for `policy-demander`); (2)
the IMF's *Annual Report on Exchange Arrangements and Exchange Restrictions*, its yearly classification of
monetary policy frameworks (`www.imf.org`: Guard allow, but the site answers the toolkit 403 — Sami's hand).
**Membership** (P21, *reading*): a money's first year in the list's formal inflation-targeting category from
2012 names a candidate (the category's exact name fixed from the file's legend before any country-year is
read, and written in the manifest; a looser category, if the list has one, is a variant); the candidate is an
adopter if its central bank's announcement states an explicit numerical inflation target adopted as its
policy's anchor — Hammond's "fully fledged". The Federal Reserve's goal of January 2012 is out whatever a list
says: Hammond's footnote, "though it did not formally adopt inflation targeting" (printed page 13); printed as
a disagreement. **Date**: the announcement's own date, from the central bank's document, its host ruled before
any fetch. **Until a list is frozen, adoptions from 2012 *cannot be read*.** *Variant, by source*: the
adopters from 2012 named by the BIS (2025, 26 central banks) and by Kiley and Mishkin (2025) — both on allowed
hosts, both selected samples, said.

## 6. Statuses — the rules common to the four panels

- **War** (M0 section 1): a change whose year is a war year for its state — at least 1,000 battle deaths on
  its territory in the year, or a COW war in which its own forces lost at least 1,000 — is *apart*, "war year
  at entry: told". **Panel 1's belligerents are these** (P22, *reading*): "belligerent" is M0's war year, not
  a declaration of war — a state at war whose own losses in that war stay under 1,000 and on whose soil none
  fell is not in a war year, and its change is counted. Coded now, by script, on every state-year, from the
  frozen COW files (`cow/inter-state-wars`, `cow/intra-state-wars`; from 1989 the World Bank's battle-deaths
  series, UCDP not being frozen): war is a common cause, not one of frame a's measures. War inside the window
  is written on the line (`note`), never apart. **Where the war year cannot be read** (P23, *reading*), the
  line stays counted, flagged, and a variant leaves such lines out.
- **An exit after a run** (M0: reserves down 20% or more [10; 30] in the 12 months before) — **panels 1 and 2
  only** (P24, *reading*: M0 says *exits*; reforms and adoptions are not exits). **Read by the window build,
  never now**: reserves are one of frame a's trust measures. **The measure** (P25, *reading*): M0's reserves
  are IFS's reserves *less gold*, which begin after 1948 and would miss a run on a gold standard — the only
  kind these two panels hold. For them the build reads the central bank's gold reserves (with its foreign
  exchange where the source gives it) from the Federal Reserve Board's *Banking and Monetary Statistics,
  1914–1941* (1943; FRASER, allowed; not frozen); where it has no reading 12 months before the change, the
  test is *cannot be read* and the line stays counted, flagged. The build may move a counted line to *apart*
  ("exit after a run"), never the reverse, each move written.
- **Censoring** (M0 sections 1 and 4): a change whose window ends (the year + 5; the month + 36) past the
  panel's common end is *censored*, reported apart with what happened so far — set by the build from the
  price panel's coverage, a move from counted only.
- **A window before the record** (M0 section 4): before the record of the panel's changes (panel 3's
  1970–72) is *apart* now; before the money's price record (no price in the year − 3) is *apart*, set by the
  build from coverage.
- **A competing exit inside the window** (M0 section 4; the three euro entries of section 5 among them): the
  line carries `exit` and the status *ended unbroken*; the window is read to the exit; the description is
  given with those lines and without them (M0's "twice").
- **Two changes of the same panel in one money within one window** (P26, *reading*): each keeps its line,
  both flagged `overlap`, naming the other; the description is given with and without them.
- A change that cannot be dated has no line (`members.csv`: *cannot be read*). Apart lines are never counted,
  and their reason is written (M0 section 3).

## 7. Non-changers and the window — fixed now, computed after the list's commit

- **The pool** (P27, *reading*): every money with a price index in the year before the change, whose panel
  source covers it over the years ±3 around the change and records no change of the same panel within ±3
  years of the change's date. **Headline: members and non-members alike** — M0 says "monies", and Ball and
  Sheridan's guard against regression to the mean, the dossier's reason for the non-changers, compares
  adopters with non-adopters. **Variant**: only monies on which the support stood as on the changer in the
  year before (convertible, for panels 1 and 2; not targeting, for panel 4; in panel 3 every money is at risk
  of a reform, so the variant is the headline). "The same panel", for panel 3: any reform, up or down.
  Coverage: panel 1, Meissner's candidates and the United Kingdom, with the exit and dating sources; panel 2,
  Bernanke and James's 24 rows; panel 3, Garriga's country-years; panel 4, every money before 2012 (by
  Hammond's text, her 27 and her three exits were all the formal adopters to then), and from 2012 only where
  section 5's list is frozen.
- **The match**: up to five per change, nearest by π in the year before — π(y − 1), the annual change of the
  year before the change's year, from M0 section 1's order of sources, one measure for every money whatever
  its index's frequency (P28, *reading*) — within 3 points [1; 5]; ties by a draw seeded 1797; a non-changer
  may serve several changes, its reuse counted and printed; a change with none within the caliper is shown
  alone, said. **War** (P29, *reading*): a money in a war year in the change's year is no non-changer for a
  counted change — the war that sets a change apart would otherwise ride into the comparison. A non-changer's
  own change of the same panel at +3 to +5 years ends its path there, flagged.
- **The window**: annual, years −3 to +5 around the change's year; monthly, −24 to +36 around its month, only
  where monthly data exist and the change is dated to the month (M0 5 a). Value (π, depreciation, the market
  split) and trust (deposits to GDP, currency to deposits, dollarisation, reserves) apart, from M0's sources.
- **Where the build writes**: its own list, `data/reconstructed/ft001-a-window/`, whose lines name the change
  they complete; it never edits this list. **M0's twin declares no `follows` for frame a**
  (`case_line.follows`), so `m0.py` cannot hold the window build after this list: that order rests on this
  protocol and the commit history — declared (section 10).

## 8. The coders

- **Hand-coded: panels 1, 2 and 4.** The first coder reads every candidate of the panel from the frozen
  documents, in the documents' order, never an economy searched for. Each line carries its locator, the cell
  or text as printed, and, where needed, a quotation of at most twelve words; `uncertainty` is `clear` or
  `judgement` with the reason.
- **A second coder** — an independent agent that has not seen the first coder's files — recodes **a 20% random
  sample of each hand-coded panel's candidates**, drawn with seed 1797 (`random.Random(1797).sample(sorted
  codes, ceil(0.2 n))`, panel by panel; the list from 2012 gets its own draw when it is read), from the same
  frozen pages. Agreement: **Cohen's κ** on each candidate's membership and status (member counted, member
  apart, not a member, *cannot be read*) and the share of identical change dates at the source's precision,
  every disagreement listed. **The samples are small** (about 11, 5 and 6 candidates): κ is printed with its n
  and carries no claim, said. Disagreements are settled by the text of M0 and of this protocol, never by an
  outcome; a reading settled after a pass is written and committed before the next (as the acts' sections
  3a–3c).
- **Scripted: panel 3 and every line's war year**, run identically on every country-year (Garriga) and
  state-year (COW), no second coder; the script (`missions/code/`, beside `acts.py`) prints every unmatched
  name and never drops one.
- **The barrier** (M0 section 3): the coders know the histories; a change is coded only from what the named
  document says, a remembered date noted and never used, and **no price, rate, money, deposit or reserve series
  is opened before this list is committed** — that holds the coders, not code.

## 9. What must be fetched — the Guard's rulings of 2026-09-30

Asked with `ft.data.guard.rule(url, host, record=False)`, one command per host, before any fetch; **nothing
was fetched**. The session freezes through `ft.data.http`, ruling then fetching, never in one command; a
candidate's contents are unverified until it is frozen (its captions first).

| For | Document | URL | Host | Ruling |
|---|---|---|---|---|
| Panel 1, exits (P6) | Obstfeld and Taylor (2002), *Sovereign Risk, Credibility and the Gold Standard: 1870–1913 versus 1925–31*, NBER WP 9345 | https://www.nber.org/system/files/working_papers/w9345/w9345.pdf | www.nber.org | allow |
| Panel 1, exits (P6) | Mitchener and Weidenmier (2009), *Was the Classical Gold Standard Credible on the Periphery?*, NBER WP 15401 | https://www.nber.org/system/files/working_papers/w15401/w15401.pdf | www.nber.org | allow |
| Panel 1, exits and dates (P6, P8) | Bordo and Schwartz (1994), *The Specie Standard as a Contingent Rule*, NBER WP 4860 | https://www.nber.org/system/files/working_papers/w4860/w4860.pdf | www.nber.org | allow |
| Panel 1, exits (P6) | Bordo and Rockoff (1995), *The Gold Standard as a "Good Housekeeping Seal of Approval"*, NBER WP 5340 | https://www.nber.org/system/files/working_papers/w5340/w5340.pdf | www.nber.org | allow |
| Panel 1, exits (P6) | Chernyshoff, Jacks and Taylor (2005), *Stuck on Gold*, NBER WP 11795 | https://www.nber.org/system/files/working_papers/w11795/w11795.pdf | www.nber.org | allow |
| Panel 1, dates (P8) | Bordo and Kydland (1990), *The Gold Standard as a Rule*, NBER WP 3367 | https://www.nber.org/system/files/working_papers/w3367/w3367.pdf | www.nber.org | allow |
| Panel 1, dates (P8) | Brown (1940), *The International Gold Standard Reinterpreted, 1914–1934*, NBER: Book One's chapters (PDFs under `/system/files/chapters/`) | https://www.nber.org/books-and-chapters/international-gold-standard-reinterpreted-1914-1934 | www.nber.org | allow |
| Panel 1, dates (P8) | *Federal Reserve Bulletin*, 1914–1915 issues | https://fraser.stlouisfed.org/title/federal-reserve-bulletin-62 | fraser.stlouisfed.org | allow |
| Panels 1–2, runs (P25, the build) | Board of Governors, *Banking and Monetary Statistics, 1914–1941* (1943), its gold section | https://fraser.stlouisfed.org/files/docs/publications/bms/1914-1941/BMS14-41_complete.pdf | fraser.stlouisfed.org | allow |
| Panel 2, "where wider" | Wolf (2008), CEPR DP 6685 | https://cepr.org/system/files/publication-files/DP6685.pdf | cepr.org | allow; the site answers 403, and a purchase — declared |
| Panel 4, from 2012 (P20) | Cobham, monetary policy frameworks classification (2024 update) | https://monetaryframeworks.org/classifications/ | monetaryframeworks.org | **deny** — `policy-demander` |
| Panel 4, from 2012 (P20) | IMF, *Annual Report on Exchange Arrangements and Exchange Restrictions* (yearly) | https://www.imf.org/en/Publications/Annual-Arrangements-Exchange-Restrictions | www.imf.org | allow; the site answers the toolkit 403 — Sami's hand |
| Panel 4, variant | BIS Quarterly Review, March 2025, *Moving targets? Inflation targeting frameworks, 1990–2025* | https://www.bis.org/publ/qtrpdf/r_qt2503c.pdf | www.bis.org | allow |
| Panel 4, variant | Kiley and Mishkin (2025), *The Evolution of Inflation Targeting from the 1990s to the 2020s*, NBER WP 33585 | https://www.nber.org/system/files/working_papers/w33585/w33585.pdf | www.nber.org | allow |
| Panel 4, three exits (P19) | Banco de España's announcement of its target | a page on the host, to find | www.bde.es | allow |
| Panel 4, three exits (P19) | Bank of Finland's announcement | — | www.suomenpankki.fi; www.bof.fi | **deny**; deny |
| Panel 4, three exits (P19) | National Bank of Slovakia's announcement | — | www.nbs.sk; nbs.sk | **deny**; deny |
| Panel 4, from 2012 | each adopting central bank's announcement | once the list is read | one ruling per host | not asked |

**Refused, never opened** (candidate copies or sources met in the searches): `eh.net` (Officer's
encyclopedia article on the gold standard, with tables of periods), `eml.berkeley.edu` and `escholarship.org`
(copies of Obstfeld and Taylor), `link.springer.com` (Cobham's 2023 article), `www.elibrary.imf.org`,
`digital.library.northwestern.edu`, `digital.nls.uk` and `babel.hathitrust.org` (the League of Nations'
*Memorandum on Currency and Central Banks, 1913–1924*, a primary source for the 1914 suspensions). `archive.org`
answers allow; no copy of the memorandum was found on it, and it is never used for a copy of a refused host's
page. **Already frozen**: Meissner, Bernanke and James (chapter and working paper), Hammond, Garriga, the
chronologies, COW, the World Bank's economies. **For a grouped wall request** (`make -C (private path)
policy-demander`, prepared by the session, decided by Sami's live word): `monetaryframeworks.org`,
`www.suomenpankki.fi`, `www.nbs.sk`.

## 10. What M0 leaves open for frame a, and what this protocol cannot hold

**Open in M0** — each chosen above as a reading, for the audit and M0's next version to judge:

1. Panel 1's membership needs exits Meissner does not give; M0 names no source (P6, P8). The UK is absent from
   his table (P4); M0's 31 July can cut suspensions of the same crisis (P5).
2. Which of Bernanke and James's columns is "the exit" (P12): the headline follows the source's own note 7,
   which counts exchange controls; M0 section 2's "force imposed is not a support giving way" is the variant.
   An exit the table dates before 1931 falls outside M0's span (P13).
3. "The targeters at the start of 2012" select the adoptions that lasted (P18); "the announcement after"
   dates adoptions but lists none (P20, P21).
4. The run rule's measure — IFS's reserves less gold, from 1948 — cannot be read for the only panels whose
   exits it tests (P24, P25).
5. The twin's `case_line.follows` has no line for frame a: M0's next version could add `ft001-a-window:
   [ft001-a]`, so that `m0.py` holds the order this protocol only says.
6. The non-changers' pool, reuse, ties, war and π's frequency (P27–P29); overlapping changes (P26); unions'
   reforms (P15); a reform with no direction, and a creation (P14); the index for the variant (P16).
7. **M0 section 1 reads the regime before 1946 from "the gold-standard lists of frame a"**, and M3's panel
   waits on them for the regime (its R12), for a target standing (c6) and for "convertible at entry" before
   16 August 1971 (c7). These lists give the gold standard at two moments — Meissner's members from adoption
   to 1914, Bernanke and James's from their return to their exit (1919–36) — and the targets from their
   adoption (with the acts list's targets abandoned). **A regime at any other date before 1946, and
   convertibility from 1937 to 1971, cannot be read from them** — declared, for M3's panel and M0's next
   version.

**What this protocol cannot hold**: that no coder looked at a value — the order of commits holds the lists, not
memory (M0 section 3), and this producer's slip on Hammond's chart is told above; Wolf's list; the adoptions
from 2012 until a list is frozen; the contents of the exit and dating candidates, unverified until frozen — if
none dates what P6 and P8 need, the members or changes are *cannot be read*, never filled from memory or a
further search.

## 11. The checks before the commit

- `missions/code/m0.py`'s `list_problems` on `series.csv` (the lock at 3163162, the case line);
  `ft.data.reconstructed.problems("ft001-a")` empty.
- **This list is committed alone and first**, before the window build and before any value or trust measure of
  frame a is computed.
- The manifest says: the sources and their vintages; each step in order; every reading P1–P29 used; the
  members and non-members of each panel with their reasons; the changes by source, panel by panel (M0
  [a-R4]); the coders and κ, with n and every disagreement; the differences between the chapter and the
  working paper; what cannot be read, and where.
- **Audit**: the deep mission audit (`.claude/skills/ft-map/mission-audit-brief.md`), isolated, on a model
  suited to the task and never Fable, which re-codes a sample itself.

## 12. Readings settled after the first coder's pass (2026-09-30, before the second coder)

The first coder (`a1`, Sonnet) read every candidate. These readings settle what sections 2–5 left loose. Each
is settled by M0's text or this protocol's, never by an outcome, and is committed before the second coder
starts. The first coder recodes under them.

- **Q1 — Meissner's table.** The page image holds **35 dated rows and 13 "---"** (48 rows; Argentina's three
  years and Chile's two are one row each), not 37 and 13. With the United Kingdom, panel 1 has **49**
  candidates. Every count in sections 2 and 8 reads 35 and 49.
- **Q2 — P6's "covers"**: a source covers an economy when it gives that economy **a gold-standard period**
  (adoption to exit, or an exit). A list of names with no period covers none. Counting names would let a
  source with no exits head, and make every adopter a member by silence, which P6 forbids. Result: Mitchener
  and Weidenmier (20 of 35) head. Bordo and Schwartz, then Obstfeld and Taylor, fill.
- **Q3 — P8's count** counts only a dated **suspension of redemption** (P7). An export embargo, or notes
  made legal tender, is not one. **Argentina's change** takes its date from the first P8 source, in order,
  that dates a suspension of redemption. If none does, it *cannot be read*. Brown's embargo (2 August 1914)
  and legal-tender date (8 August) are variants. With Argentina not counted for Brown, Brown and Bordo–Schwartz
  tie at 3, and Bordo–Schwartz heads by the order listed.
- **Q4 — P8's fill** (the first coder's reading, kept). P8 chooses its head by **month precision**, so a
  member's date is the first source in P8's order that dates its suspension to the month or finer. If none
  does, it is the first that gives the year (year precision, annual window only, flagged). The plain-order
  reading, in which the first source to date the suspension gives it at its own precision, is a variant.
  It differs only for the United Kingdom.
- **Q5 — Mitchener and Weidenmier's months** end adherence, and their Table 1 is not a P8 candidate. They
  are printed in `reason`, never used as a date.
- **Q6 — P21's category** — Cobham's legend, frozen at `frame-a/cobham-classifications-page`:
  - Full inflation targeting (FIT) and full converging (FCIT) are "typically attained". The loose categories
    (LIT, LCIT) are "not well hit or wider".
  - **Attainment is an outcome** of the targeting whose start panel 4 dates. Choosing candidates from the
    "full" categories would select adoptions by their success (M0 section 8's second question).
  - So **a candidate is a money's first year from 2012 in any of the four inflation-targeting categories
    (FIT, FCIT, LIT, LCIT)**, if it was in none of them before. The "full"-only list is a variant, said to
    select on attainment.
  - P21's announcement still decides membership. P21's own words "the formal inflation-targeting category"
    are read this way.
- **Q7 — Candidates Hammond already holds** (a money reclassified from 2012, Indonesia and Thailand in 2020)
  are not new adoptions. Their date is Hammond's.
- **Q8 — Calendars and codes.** Russia's suspension date is as printed, flagged `calendar unstated` (P3); the
  "before 31 July" test reads the printed date. Salvador, Siam, Santo Domingo, Persia and Rumania take their
  ISO codes. The Straits Settlements take `XSS`, from ISO's user-assigned range (P2).
- **Q9 — Earlier "suspensions".** The United Kingdom's 1847, 1857 and 1866 suspensions (of the Bank Charter
  Act) are not suspensions of convertibility, so the United Kingdom is a member. Uruguay *cannot be read*:
  Obstfeld and Taylor contradict themselves.

**The second coder's sample** (section 8), drawn after the candidate lists and before any second-coder reading:
- panel 1: FIN, GBR, BRA, CRI, AUS, ROU, HTI, TUR, CHN, DEU;
- panel 2: FIN, FRA, BEL, DEU, AUS;
- panel 4: GBR, GHA, BRA, SRB, SWE, COL.

The from-2012 list gets its own draw once its candidates are re-listed under Q6.

## 13. Readings amended after the deep audit (2026-09-30, before the list's second build)

The audit is `bank/checks/FT-001-M4-2026-09-30-opus-audit.md`: not yet, B1. Each amendment below follows M0's
text, never an outcome, and is committed before the code that applies it. The earlier wording stays above,
for the history.

- **P20, P21 and Q6 amended (B1). Cobham's classification is conditioned on behaviour.** Even its loose
  categories include "wider targets attained", and a formal targeter that keeps missing sits in "loosely
  structured discretion" (Ghana: formal in 2007, first in the four categories in 2018). So both Cobham lists,
  the four categories and the full-only list, become **variants "conditioned on behaviour"**.
  - The headline adoptions from 2012 wait on a de jure list: the IMF's AREAER framework classification, by
    Sami's hand.
  - Membership and date still come from each central bank's announcement (P21).
  - Until the AREAER list is frozen, the adoptions from 2012 are *cannot be read*, and the sub-panel is told.
- **P19 amended (B1).** The fallback to "the first year the classification gives" is dropped, since it would
  date by attainment. Finland, Spain and Slovakia are dated by their central banks' announcements only. Their
  hosts are allowed, so this is a fetch and a freeze, not a wall; until those are frozen, they are *cannot be
  read*.
- **P12 amended (O2). The headline exit follows M0's text**: the first of suspension and devaluation. M0
  section 2 says force imposed after strain is never an act of this list, and 8 of the 10 control-first
  exits follow a banking panic in Bernanke and James's own list.
  - Bernanke and James's own definition (their note 7, the first of the three dates) becomes the variant
    `a2-var-bj-note7`.
  - A member whose only change in 1931–36 is an exchange control has no exit in the headline.
  - The window build describes the timing on both readings. Where they disagree, "the order cannot be read".
  - Written as a departure for M0's next version.
  - *For frame c's "convertible"* (M0 section 1: redemption on demand by any holder), an exchange control
    does end convertibility. Frame c keeps reading the first of the three dates. This is not a contradiction:
    the act list and the state of convertibility answer different questions, and both follow M0's text.
- **W11, added to `war.py` (O3). A dependency at war through its metropole** takes the metropole's war year,
  where COW counts the dependency's losses inside the metropole's, the dependency not being a COW state that
  year. The list is fixed and applied identically:
  - the British dominions and India with the United Kingdom, until each enters COW's state system;
  - the Grand Duchy of Finland with Russia, to December 1917.

  Panel 1 is told as **a war-crisis panel**: its counted neutrals' changes are themselves dated by the war's
  outbreak.
- **P27 and P28 amended (O1), for the window build, before it runs.**
  - *The pool* reads information at the change only: a money with no change of the same panel in y−3..y.
    A comparator's own later change, up to y+5, ends its path there, flagged. The as-written ±3 pool becomes
    a variant.
  - *The match* is on π(y−1) and on the change in π from y−3 to y−1, both within M0's caliper.
  - *The null band*: each description prints, beside it, the band a simulation under no effect gives with
    the same pool and match, run before any real window is read.
  - Panel 2's comparators are named for what they are: earlier or later leavers. No panel-2 member stayed on
    gold through 1936.
- **P29 completed (M4).** A non-changer whose war year cannot be read stays in the pool, flagged, and a
  variant drops it.
- **Said in the manifest, no rule changed:**
  - the protocol commit each build was coded under (M1);
  - Cobham's country-years were read under the working reading before the legend was frozen (M2);
  - the size of P23's variant (M3);
  - Mitchener and Weidenmier cover the countries that had short-term interest rates and stayed two years on
    gold, so panel 1's *cannot be read* are the periphery (M6);
  - Obstfeld and Taylor give prewar periods for their four exceptions only (M7);
  - panel 4's headline is, in effect, Hammond's 27 until the AREAER list is frozen (M8);
  - the run test's source, *Banking and Monetary Statistics 1914–1941*, is checked for 1913 by the window
    build (M5).

## 14. Panel 4 from 2012: reading AREAER (2026-10-01, before any country-year is read)

AREAER 2011–2023 is frozen (`frame-a/areaer-2011-2023`, 01c0a38). Sami downloaded it by hand. These readings
complete P20 and P21. The only thing read before writing them was the 2012 edition's legend for Table 1
(PDF pp. 4–5); no country in any framework column was read.

- **R-A1 — the list.** Each edition's Table 1, "De Facto Classification of Exchange Rate Arrangements and
  Monetary Policy Frameworks, April 30, Y". The monetary policy framework column is "as indicated by country
  officials" (the Overview), so it is a de jure list, as section 13 asks. **The category is "Inflation-targeting
  framework"** (the legend: "the public announcement of numerical targets for inflation, with an institutional
  commitment by the monetary authority to achieve these targets"). Table 1 has no looser category, so P21's
  variant has nothing to read.
- **R-A2 — dates.** Edition Y reads the framework at 30 April of Y. The 2011 edition is the base (30 April
  2011).
- **R-A3 — candidates.** A money is a candidate from 2012 when the edition of year Y ≥ 2012 is the first to
  list it in the inflation-targeting column, and the edition before did not list it.
  - A money that leaves the column and later returns is a candidate again at its return, flagged
    `re-entry`.
  - A money listed in 2011 is a targeter already: Hammond's 27 or the targets that ended before 2012, never a
    new candidate.
  - A currency union's line (ECCU, WAEMU, CEMAC, the euro area) is read as one money, as frame a's A1 reads it.
- **R-A4 — membership and date stay P21's.** A candidate is an adopter only where its central bank's
  announcement states an explicit numerical inflation target adopted as its policy's anchor. The date is that
  of the announcement. Until the announcement is frozen, the candidate is *cannot be read*. The edition's year
  is **never** used as a date (section 13, P19's fallback dropped). The Federal Reserve is out, as P21 says.
- **R-A5 — the coders.** Two coders, each over all 13 editions independently, read Table 1's
  inflation-targeting column from the page images. Each country in it is a line: edition, country as printed,
  page. Agreement is reported as κ on country-editions. Disagreements are settled by the page image, read
  by the session and written in the manifest.
- **R-A6 — what is never read here**: the exchange-rate-arrangement rows (de facto, IMF staff's
  classification), the country chapters and any outcome. Only the framework column, and only to list who is
  in it.

## 15. The window build amended after its deep audit (2026-10-01, before the window's second build)

The audit is `bank/checks/FT-001-M4-window-2026-10-01-opus-audit.md`: ready, no B, with O1–O5 to answer
before any description is published. The session follows it on every finding. The first build's windows have
been seen, so every new reading below is said to have been written after them. None changes the list
`ft001-a`.

- **O1 — the null band.**
  - Same-year scenarios are added: a hazard on π(y), and one on π(y) − π(y−1), both signs.
  - Each band is computed at the **described n**: the counted lines with a gap, per description line.
  - A **placebo band on the real panel** is added: pseudo-changes drawn at random years among non-changers,
    through the same pool and match, 200 draws. It needs no chosen price process.
  - The manifest says: "a band from chosen scenarios and a placebo band; a mean inside them is told as no
    effect; outside them it is not a finding".
  - The guards table's frame-a cell is revised.
- **O2 — the run test's grid.**
  - `changes.csv` carries the verdicts at 10% and 30% beside the headline's 20%, and the manifest names the
    lines that move.
  - The strict variant is dropped. The audit checked about 50 of the cells used against the page images and
    found them right, and that check is the record (W9).
- **O3 — gold only.**
  - W9 names the departure from P25: table 160 gives gold, not foreign exchange.
  - A "no" from gold alone is written "no (gold only)" and flagged `gold_only`, so that it is never read as
    "no run".
  - The Bank of England's, the Bank of France's and the Reichsbank's foreign exchange (BMS tables 164, 165
    and 167) are a need, built as a variant when parsed.
- **O4 — units of deposits to GDP.**
  - A level band, deposits to GDP outside 1–300%, flags `units_suspect` on the reading.
  - A units-break flag is carried to every later year of that money's series.
  - Each seam's ratio is printed.
  - The W6 overlap is measured only on years where the old lines and the survey differ. Identical values are
    the survey filling the lines, not a check, and the gap check applies instead.
- **O5 — unions in the pool.**
  - A member of XOF, XCD or the euro area takes its union's changes in the pool's "no change in y−3..y".
  - A euro member after its entry is the euro, never a comparator of its own. The variant
    `euro-members-as-own` keeps the first build's reading.
  - The union lines' reason becomes "no union-level price series".
- **M1–M8.**
  - M1: the manifest names the protocol commit and the code commit apart.
  - M2: censored lines take M0's status *censored*, and a line whose price record has a gap inside it is "a gap
    in the price record", not "before the record".
  - M3: where the headline and note 7 disagree, `describe` says "the order cannot be read", and the "with"
    line of the ended-unbroken lines is printed.
  - M4: `bms160`'s R7 also runs on `extra_group` cells, and a column with a lost leading digit is caught
    through the Total gap.
  - M5: the needs are brought up to date.
  - M6: currency to deposits switches both tables at the later of their first survey readings, and `_seam`
    reports both seams.
  - M7: dropping panel 4's three unread adopters from the pools is said.
  - M8: the band and the described gap cover π only; the other measures are described without a band, said.

## 16. The window amended after its narrow re-check (2026-10-01, before the window's third build)

The re-check (`bank/checks/FT-001-M4-window-second-build-2026-10-01-opus-recheck.md`: ready) reproduced every band,
status and sentence of the second build. Its new findings bear on the placebo's design and on unread units.
The session follows it on each. **These readings are written after the first and second builds' windows were
seen; the manifest says so (N6).**

- **N1 — draws.** The placebo takes 10,000 draws, seeded by (reading, label, n), so identical lines get identical
  bands. Each edge is printed with its Monte Carlo error: the spread of the edge over two independent halves of
  the draws. The scenarios' band takes 300 runs (from 100) and prints its edges' error the same way.
- **N2 — the placebo's design.**
  - **Headline**: a pseudo-change is eligible by the pool's own past-only rule: no change of its panel in y−3..y,
    and its path cut at its own later change, flagged, as a comparator's (W3).
  - **Stratified**, printed beside it: pseudo-changes drawn among eligible money-years within ±3 years of a real
    change and within the caliper (3 points) of that change's π(y−1), one per real change, then matched as in the
    headline.
  - The as-built rule (no change through y+5, uniform over the span) is the variant `placebo-future-clean`.
  - Panel 1's placebo has 7 cells for n = 4: it cannot be read as a band, said.
- **N3 — the record, as it was.** The audit page-checked about 50 cells of table 160 and found two wrong: Italy
  1936-09 (repaired, R7) and Estonia 1930-10. Estonia 1929-10 to 1931-08, where the Total row cannot check the
  column, is **unreadable**; note 7's Estonia line is read again on that rule. W9's text and the manifest say it.
- **N4 — units of deposits to GDP.**
  - GDP's own seam: where IFS NGDP and the World Bank's GDP differ by more than a factor of 2 in their common years,
    every year of the World Bank segment is flagged `units_suspect` (Liberia, Armenia).
  - At a source seam, a units break is a factor of 10 or more (from 100).
  - An overlap where |lines / survey − 1| < 1e-3 in every common year is **identical**: the check is then made
    across the gap.
- **N5 — unions alike.** A member of the West African (XOF), Central African (XAF) or Eastern Caribbean (XCD)
  currency union is, from its entry, that union's money, never a comparator of its own, as a euro member is
  (W15). Under M0 §1 and A1 a union is one money. Variants: `euro-members-as-own` (the euro only) and
  `union-members-as-own` (the three other unions only).
- **N7 — small items.**
  - "Before the price record" reads the money's whole series, not only the panel's table (RUS 1990).
  - The headline and note 7's per-line disagreements are printed line by line (POL 1936; DEU and HUN).
  - Section 15's unions include XAF.
  - A comparator's path ends at its euro entry, flagged, as a change's competing exit ends its own.
  - Wording: a mean inside both bands "is consistent with no effect", never "told as no effect".

## 17. Panel 4 from 2012: the announcements read under R-A4 (2026-10-01, before frame a's list is rebuilt)

A fetcher (Sonnet), every host ruled first, froze what each central bank's own site gave (dc82874; Japan b040b9f).
The session reads each document against R-A4: an adopter is a candidate whose **own announcement** states an
explicit numerical inflation target **adopted as the policy's anchor**, dated by that announcement. Two kinds of
document are not that announcement:
- a later document that recounts an adoption;
- a plan that sets a target for a later year while the regime is still "in transition".

Both are kept for a variant, never the headline.

| Candidate (AREAER) | Document frozen | Reading | Date |
|---|---|---|---|
| Japan (2013) | Bank of Japan, "The Price Stability Target…", 22 Jan 2013 | **adopter**: 2% CPI | 2013-01-22 |
| Russia (2015) | Main Directions 2015–2017, Board 6 Nov 2014: "completes the transition"; 4% medium term | **adopter** | 2014-11-06 |
| Costa Rica (2018) | Junta Directiva 31 Jan 2018, note of 2 Feb 2018: "adoptar un esquema … de meta de inflación", 3% ± 1 | **adopter** | 2018-02-02 |
| Mauritius (2023) | Bank of Mauritius, 11 Jan 2023: flexible inflation targeting, 2–5% | **adopter** | 2023-01-11 |
| Argentina (2017) | Objetivos y planes 2017 (Dec 2016), "ha puesto en marcha", targets 2017–19 | *cannot be read*: a later document; the September 2016 communiqué not reached | variant 2016-12 |
| Ukraine (2017) | Monetary policy strategy, 13 Jul 2018, 5% ± 1 "at the first stage" | *cannot be read*: the 2015–16 announcement not reached | variant 2018-07-13 |
| Kazakhstan (2016) | Monetary policy to 2020 (24 Apr 2015, a plan: 3–4% by 2020); a 2016 text recounting August 2015 | *cannot be read*: a plan and a later account | variant 2015-04-24 |
| Uzbekistan (2021) | Main Directions 2020–2022 (2019): "gradual transition", 5% from 2023 | *cannot be read*: a plan in transition | variant 2019 (year) |
| Seychelles (2020) | Current framework page; framework of 27 Mar 2024: an interest-rate framework, no numerical target | **not an adopter** in what is frozen | — |
| Kenya (2021) | White paper, July 2021: a "forward-looking" framework, no numerical target | **not an adopter** in what is frozen | — |
| Sri Lanka (2020) | current page; two press releases (2018–19) with no target | *cannot be read* (the explicit target dates from Oct 2023's agreement, not frozen) | — |
| Mongolia (2023) | strategy page; a draft for 2023 (6% ± 2) | *cannot be read*: a draft | — |
| Dominican Rep. (2012), Uganda (2014) | — | *cannot be read*: documents on refused hosts (`cdn.bancentral.gov.do`, `bou.or.ug`), declared | — |
| Paraguay (2013) | — | *cannot be read*: the host answered 403 | — |
| India (2015), Uruguay (2016), Jamaica (2018) | nearest pages only (Uruguay, Jamaica) | *cannot be read*: archives load by POST or script | — |

- **Headline**: four adopters from 2012, namely Japan, Russia, Costa Rica and Mauritius. Seychelles and Kenya are not
  adopters in what is frozen. Twelve candidates are *cannot be read*.
- **Variant** `later-or-transition-documents`: it adds Argentina 2016-12, Ukraine 2018-07-13, Kazakhstan
  2015-04-24 and Uzbekistan 2019, at the precision printed.
- The fetcher's quotations and page numbers are in its report, summarised in the plan's Decisions. They are
  short, and their documents are frozen (manifests committed).
- *What no code holds*: the reading of each document. It was made by the session from the fetcher's quotations
  and goes to the small check of frame a's next build.

## 18. The window's bands made stable (2026-10-01, after the third build's re-check)

The re-check (`bank/checks/FT-001-M4-window-third-build-2026-10-01-opus-recheck.md`: ready) found that two
placements printed by the third build rest on noise or on a design chosen after a build was seen. The session
follows it, before any description of the window is used:

- **P1, P2 — the edges' error, and "at the edge".**
  - The scenarios take 1,000 runs (from 300).
  - Every band edge carries a standard error from B = 20 batches: the sd of the batch edges over √20. This
    replaces the half-against-half difference.
  - A mean within 2 standard errors of an edge is printed **"at the edge"**, never inside or outside.
- **P3 — both placebo designs placed.** Each description line places the mean on the past-only (headline)
  placebo, on the stratified one **and on `future-clean`**. It also gives the share of cut cells among the
  pseudo-changes and their mean gap. The variant is named `future-clean` everywhere.
- **P4 — said.** A pseudo-change's path is cut at its own later change; a real change's is not. "Without
  overlapping lines" partly covers this. Said in W19.
- **P5 — units.**
  - The GDP seam reads the median ratio over the common years (Suriname no longer flagged for one year).
  - Where the seam names the World Bank segment, a units break is not carried into the IFS years (Liberia).
  - Armenia is not claimed.
  - The `units_suspect` count is split by reason.
- **P6.** R8 covers Estonia from 1929-01.
- **P7.**
  - Each stratified band prints its smallest stratum.
  - A stratum may hold the changer's own earlier money-years, cut at its change. Said.
- **P8.** The union years cite Garriga's `regional` flag, the frozen source they match. Barbados (the EC dollar
  to 1973) is said, and moves nothing.
- **P9.** 3-up's mean without ESP 1980 (one comparator, gap −48.1) is said beside it, with the median. "Most
  reused" says "within one panel".
- **Two readings settled ahead of documents still to come** (2026-10-01, before either is read):
  - **India.** The Monetary Policy Framework Agreement of 20 February 2015 is signed by the Government of India
    and the Reserve Bank of India. A copy of the agreement's text released by the government (PIB) counts as
    the bank's own announcement, since the bank is a party to the signed text, and is dated by the agreement.
    It is flagged `joint agreement, government's release`. A government statement that only reports the
    agreement does not count.
  - **Uganda.** If the Bank of Uganda's own document dates its adoption ("inflation targeting lite") before
    2012, Uganda is no adoption **from 2012**. It is then an adoption before 2012 that Hammond's 27 do not
    hold, and it is said in the manifest as a gap in panel 4's list, never added to the headline. R-A3 counts
    only AREAER's first listing as a candidate, and R-A4 dates by the announcement, so the two can disagree.
    The disagreement is said either way.
- **Sami's hand downloads, frozen** (2026-10-01):
  - **Paraguay** (`frame-a/bcp-it-recounted-2013`): the bank's July 2013 document recounts the adoption of
    18 May 2011 (Resolución N° 22); it is not the act. Paraguay is **no adoption from 2012**. It is a pre-2012
    adopter that Hammond's 27 do not hold, said as a gap. The act itself is not needed.
  - **Uruguay** (`frame-a/bcu-ipm-2016q2`): the Informe de Política Monetaria for 2016 Q2 is a report giving
    the 3–7% range, not the act. Uruguay is *cannot be read* in the headline. The variant
    `later-or-transition-documents` dates it 2016-Q2 (the report's quarter, at month precision 2016-06),
    flagged `re-entry`.
  - **India** (`frame-a/pib-india-mpfa-reply-2015-08-07`): a minister's reply of 7 August 2015 that reports the
    agreement without its text. Under the India reading above it does not count, and India stays *cannot be
    read*.
  - **Jamaica**: no dated announcement found; *cannot be read*.

## 19. The window reads panel 4 past 2011 (2026-10-01, before the window's fourth build)

W5 stopped every comparator's path in panel 4 at 2011 because nothing after 2011 was read. Sections 14 and 17 have
now read it: AREAER's editions 2012–2023 list every money's framework at 30 April of each year, and the candidates'
announcements are read. So W5 is lifted, under these rules. No outcome has been read for this section: no
comparator's path, π or gap.

- **The end.** Panel 4 covers every money through **2022**, the last full year the 2023 edition closes
  (`PANEL4_LAST_COVERED`).
- **Adopters and non-adopters from 2012** (`4-from-2012`, member *yes* or *no*) are covered through 2022. Their
  change, or its absence, is known.
- **A candidate whose adoption cannot be read** is covered only through **Y − 2**, where Y is the first edition
  that lists it.
  - Edition Y places the adoption between 30 April Y − 1 and 30 April Y. Y − 2 is the last full year known
    untouched.
  - After Y − 2 it is uncovered: never a non-changer there, and never a change.
- **Paraguay.** Section 17's addendum reads a May 2011 adoption, which is not among Hammond's 27. That
  2011 change is listed nowhere, so Paraguay is uncovered from 2011. It is never a non-changer in a window that
  reaches 2011, and this is said as a gap of the pre-2012 list.
- **The variant** `later-or-transition-documents` dates Argentina 2016-12, Ukraine 2018-07-13, Kazakhstan
  2015-04-24, Uzbekistan 2019 and Uruguay 2016-06 (its re-entry). It covers them through 2022, with those dates
  as changes.
- **The at-risk variant** (`standing`, P27):
  - an adopter is "not yet targeting" before its date;
  - a candidate that cannot be read is 2 (*cannot be read*) from Y − 1 on.
- **The four adopters' changes** (frame a's a4 lines from 2012) enter the window like any change. Their pools
  and paths follow sections 7, 15, 16 and 18. A window that runs past the panel's common end is censored as
  before.
- *What no code holds*: that AREAER's column is complete for each edition. The two coders' κ (section 14) is the
  check.

## 20. The third build's small check answered (2026-10-01, before the window's fourth build)

The small check (Sonnet, isolated: `bank/checks/FT-001-M4-frame-a-third-build-2026-10-01-sonnet-small-check.md`)
read all 18 candidates blind against their frozen documents and agreed on every one (18 of 18) and on the four
adopters' dates. It stands in for the from-2012 list's second-coder draw (section 8), as the manifest says. Its
four Bs are answered here, before any window is built on the list.
- **B1, Russia.** The Main Directions approved on 6 November 2014 say the Bank "completes the transition" to
  inflation targeting, with a 4% medium-term target.
  - **Russia stays an adopter.** The document declares the regime adopted from 2015, with its numerical anchor.
  - The line between Russia and Uzbekistan: Uzbekistan's document places the regime **still in transition**,
    with a target only from 2023. A plan for a regime not yet adopted is the variant (section 17); a declaration
    that the transition is complete is the act.
  - If any count turns on Russia, it is said. The headline would then hold three adopters from 2012.
- **B2, India.** The government's reply (PIB, 7 August 2015) is a later document. It recounts the agreement of
  20 February 2015 with its date and numbers.
  - Under section 17's addendum it does not count for the headline.
  - Like Argentina's or Ukraine's later documents, it **joins the variant** `later-or-transition-documents`,
    dated 2015-02-20 and flagged `joint agreement, government's release; a later report`.
  - India's members row names the frozen reply. "No document frozen" was wrong.
- **B3, the variant's dates.** Uruguay 2016-06 and Argentina 2016-12 are the dates of the documents, not of the
  acts. The act's date is unknown, and the variant says so. A variant date marks the latest the regime can have
  started, never its start.
- **B4, Y − 2 contradicted by frozen text.** Section 19's rule covers a candidate that cannot be read through Y − 2.
  Where a frozen document dates the regime's start earlier, coverage ends the year before that start:
  - **Ukraine**: its own page says inflation targeting ran from 2015, so it is covered through 2014;
  - **Mongolia**: its draft dates the 6% ± 2 target from 2021, so it is covered through 2020.
  - The rule holds for every other candidate, and the window reads these two as named exceptions.
- **The Cs.**
  - Section 17's table row for Paraguay ("the host answered 403") is superseded by its addendum: Paraguay is a
    pre-2012 adopter.
  - Russia's line gets its note.
  - The pages not recorded for Russia and Costa Rica stay "page not recorded", said.
  - The `coder` field reads `a1` on the from-2012 lines the session read, said in the manifest.
  - Kenya's "no" rests on one white paper. Uganda's dating risk (an adoption possibly in 2011) waits on request
    7e724f0e2e3a.

## 21. The Dominican Republic and Uganda read (2026-10-01, before frame a's list is rebuilt)

Request 7e724f0e2e3a was applied by Sami on 2026-10-01. A fetcher (Sonnet) ruled every host first, then froze
what each bank's own site gave. It opened no refused host: `archive.bou.or.ug` and
`repositoriocultural.bancentral.gov.do` were seen only in search results. The session reads each document under
R-A4 and section 17's addendum. No window, path, π or gap has been read for this section.

- **Uganda** (`frame-a/bou-it-announcement-2011`):
  - the Bank of Uganda's Monetary Policy Statement for July 2011, signed by the Governor, is **the act**. It
    announces "the transition to an inflation targeting lite monetary policy framework", sets the Central Bank
    Rate, and names "the BOU's policy target of 5 percent" for core inflation over the medium term;
  - the Monetary Policy Report presented on 2 August 2011 recounts the same adoption, "in July 2011".

  Section 18's reading, settled before the document was read, applies: Uganda is **no adoption from 2012**. It is
  a pre-2012 adopter that Hammond's 27 do not hold. That is said as a gap of panel 4's list and never added to
  the headline. AREAER first lists it in 2014, so R-A3 and R-A4 disagree, and this is said. The window treats
  it as it treats Paraguay: uncovered from 2011 (`PANEL4_UNCOVERED_FROM`).
- **The Dominican Republic** (`frame-a/bcrd-it-announcement-2012`): the bank's monthly bulletin *Crónica*,
  January 2012 (No. 082), page 3, prints the bank's communiqué. It says the Junta Monetaria, by its resolution
  of 15 December 2011, authorised the bank to set a monetary policy scheme of explicit inflation targets "a
  partir de enero 2012", with a target of 5.5% ± 1 for 2012 and lower ones after.
  - *Reading*: the bank's own announcement, reproduced in its own bulletin, states the numerical target adopted
    as the policy's anchor. It is not a plan in transition, and not an account written later. The Dominican
    Republic is **an adopter from 2012**.
    - The decision is dated 15 December 2011. The regime runs from January 2012, and the announcement held is
      the January 2012 bulletin.
    - Russia was dated by the day its Board approved the document that announced the regime (section 20, B1). Here
      neither the resolution's text nor the communiqué on its own is frozen. So the line is dated **2012-01**,
      at month precision, by the document held, and flagged `the Junta Monetaria's resolution of 15 December
      2011, reported; the communiqué as printed in the bank's January 2012 bulletin`.
  - Dated by the resolution, the Dominican Republic would be a pre-2012 adopter, like Paraguay and Uganda, and
    the headline would hold four adopters from 2012 instead of five. If any count turns on it, that is said, as
    it is for Russia.
- **The headline from 2012** becomes five adopters: Japan, Russia, the Dominican Republic, Costa Rica and
  Mauritius. Four candidates are not adopters: Seychelles, Kenya, Paraguay and Uganda. Nine remain *cannot be
  read*. The total is 18, as before.
- *What no code holds*: the reading of each document. The fetcher's quotations are the check, and the
  frame's next small check rereads both documents blind.

## 22. War after COW's coverage, read with UCDP (2026-10-01, before frame a's list is rebuilt)

Sami's gap sweep (relayed by the engine session, 2026-10-01) points out that UCDP is now frozen: the UCDP/PRIO Armed
Conflict Dataset v26.1, `ucdp/conflict-dyadic-v26.1`, which Sami downloaded by hand for FT-003. W9 of `war.py` made a
state-year *cannot be read* after COW's coverage: after 2007 for the inter- and extra-state files, after 2014 for
the intra-state file. The reason was that a state's losses abroad, in a war COW has not coded, are not seen. No war
year after 2007 has been read for this section.

- *Reading* (**W12**). UCDP gives no losses by side, so it can never say *yes* to M0's test (b), "its own forces
  lost at least 1,000". It can say **no**. A state that, in a year, is party to no conflict in the dataset whose
  `cumulative_intensity` is 1 (1,000 battle-related deaths or more since the conflict began) cannot have lost
  1,000 in it.
  - A party is any of `gwno_a`, `gwno_a_2nd`, `gwno_b`, `gwno_b_2nd`, each a list, and secondary supporters
    count.
  - So, after COW's coverage, a state-year that W9 left *cannot be read* becomes **no** when the state is party
    to no such conflict that year. Otherwise it stays *cannot be read*.
  - The territory test (a) is unchanged: the World Bank's series, which is UCDP by location, through 2024.
- *Reading* (**W13**). UCDP numbers states by Gleditsch and Ward. COW's codes differ for a few states, among them
  Germany, Yemen, Serbia and the successors of Yugoslavia and the USSR. A table in the code maps them, each line
  with its reason. A UCDP state that maps to no COW state is listed and never dropped silently.
- *What moves*: years after 2007 that were *cannot be read* only because of test (b).
  - Frame k gets its headline count after 2007, where K25 had none. Its variant `war-unreadable-as-no` stays, for
    the years still *cannot be read*.
  - Frame a's cases "apart" in a war year, and the window's war years, are read again on the same rule.
  - **Frame c** reads its war years through `war.py` (`panel.war_at`, M3-panel R14), so it changes too. Frame c
    is rebuilt under its own protocol, which names this section.
  - The variant `after_cow="no"` (W9) stays, as before.
- *Conservative by construction*: the cumulative intensity counts a conflict's deaths from its start up to that year. A state
  party to a long, low-intensity conflict that has passed 1,000 stays *cannot be read*, never *yes*.
- *What no code holds*: that UCDP's list of parties is complete. A state's forces abroad, unlisted as a secondary
  supporter, would read *no*. Said in the manifests.
- *What was seen before this section was committed*: the code's coverage counts only. Of 3,312 state-years after
  2007, 1,788 move from *cannot be read* to *no*, and 1,347 stay *cannot be read* because the state is party to such a
  conflict. No state, year or frame line was looked at.
