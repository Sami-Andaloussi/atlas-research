# ft001-a-window — reconstructed dataset

Frame a's window build (FT-001, mission M4, second part): for each change of `data/reconstructed/ft001-a/` (read,
never edited), value and trust from 3 years before to 5 years after (monthly -24 to +36 where the change is dated
to the month and monthly data exist), beside the same measures for its matched non-changers. It describes; it
counts nothing and gives no verdict (A2). Built by `bank/maps/FT-001/missions/code/window_a.py` after frame a's
list was committed. **The null band at the list's n, below, was printed before any window was read**; each line's
band at its own n and the placebo band are computed after, and say so.

**When the readings were written** (N6). The first build's rules (the pool, the match, the first null band) were written
before any window was read. Readings **W10 onward** (section 15: the same-year scenarios, the placebo band, gold only,
units, unions, statuses) were written **after the first build's windows (`eca6369`) had been seen**; readings **W18
onward and section 16's** (the placebo's design, its draws, the units of GDP, unions alike, the small items) were written
**after both the first build's and the second build's (`a2bdaa6`) windows had been seen**; **W24 onward and section
18's** (1,000 runs, each edge's standard error and "at the edge", the three placebos placed, the units' remainder, Estonia
from 1929-01, the unions' source, the descriptive notes) **after the third build's (`04403c6`) windows had been seen as
well**. None changes the list `ft001-a`. The scenarios' hazards came from the deep audit; the placebo's design is the
producer's and was changed after the re-check had shown that its first design moved the bands. **The third build's commit
message summarised panel 4's placement as "outside the stratified placebo only"; it rested on the scenarios' seed (300
runs) and is withdrawn: only the placements printed below stand.**

**This is the fifth build** (2026-10-02). The fourth (committed as is in 25a6f3e, at the pause, on Sami's word) ran
before `war.py`'s W13 learnt Tonga (GW 972 is COW 955 from 1999; e93d2da), and the window reads war years for its
non-changers. The fifth build, on the same code and inputs, differs from the fourth only there:
- `series.csv`, `null-band.csv`, `placebo-band.csv` and `unread.csv` are byte for byte the fourth's;
- in `matches.csv`, 31 rows move. In nine, all outside the variant `war-unreadable-dropped`, Tonga stays the same
  comparator and gains the flag "war year cannot be read" (EST 2011 in the headline and five variants; MMR 2013 in
  `caliper-5`; DOM 2012-01 in `at-risk-only`). The 22 others are all in `war-unreadable-dropped`: in 11, Tonga leaves
  the pool and the next comparator enters (EST 2011, three ranks; DOM 2012-01, four ranks, in two readings); the other
  11 move only `reuse` and `reuse_counted`;
- in `changes.csv`, 22 rows move, all in `war-unreadable-dropped`: the pool falls by one on 22, matchable on 19 and
  in-caliper on 3, and the comparators' delta and the gap move for two changes only (EST 2011, apart: −1.117 to −1.228; DOM
  2012-01, counted, in the headline reading and in `a4-later-or-transition-documents`: 0.345 to 0.320). No status and
  no count of comparators used moves.
- So **every headline figure below is the fourth build's**, and the figures of the variant `war-unreadable-dropped` move
  only as said. The fourth build had no check of its own: the small re-check of this build is the check of both
  (`bank/checks/FT-001-M4-window-fifth-build-2026-10-02-sonnet-small-recheck.md`: ready after C; its B1 and B2 are
  answered in this manifest and in the code).
- **Since the third build** (B1 of that re-check): sections 19–22 (W5 lifted, panel 4 covered through 2022; Ukraine
  and Mongolia as named exceptions; the Dominican Republic an adopter from 2012-01 and Uganda uncovered from 2011; war
  after COW's coverage read with UCDP, W12 and W13) were written **after the third build's windows had been seen**.
  Through them and frame a's rebuilt list, panel 4 moved from the third build's n = 26 and mean −3.12 to n = 30 and
  −2.60 (and the variant `a4-later-or-transition-documents`, n = 35 with a gap, −1.62).

## Sources

- Frame a's list (`series.csv`, `members.csv`, `coverage.csv`), read only: the changes, their statuses, the panels'
  coverage. Protocol: section 13 commit `de3fe65`; section 15 commit `23c93f9`; section 16 commit `b865963`; section 18 commit `0ba2b58`; section 19 commit `c43eb81`; section 20 commit `6007f53`; sections 21-22 commit `2776366`. Code commit: c057af2d, the HEAD at build time (the window's code as last changed before the build, 776174a; `war.py`'s W13, e93d2da); the W29 notes and this line were regenerated from the build's CSVs by the code of the fifth build's small re-check answers (B1, B2). M0 v4.2 rules hash: 1160cab0bd84600d2c65abaf4b86ce7d0aa57f1b9423c8fbb9bbacdad41e58d4.
- Value, through `panel.py`'s readers: π (IFS, World Bank, Reinhart-Rogoff, BIS, Jorda-Schularick-Taylor, in M0's
  order), depreciation (IFS ENDE, against the dollar or the anchor), the market split (Ilzetzki-Reinhart-Rogoff's
  unified-market dummy, 1946-2016; before 1946 it cannot be read).
- Trust: deposits to GDP and currency to deposits (IMF IFS depository corporations survey, FDSBO + FDSBT and FDSBC,
  mostly from 2001; before a money's first survey reading, IFS's old-presentation lines 24 + 25 and 14A, frozen
  2026-10-01, the euro members' legacy money converted at the ECB's fixed rates; GDP from IFS NGDP then the World
  Bank), reserves less gold (IFS RAXG_USD, from 1950); for panels 1 and 2's run test, central banks' gold reserves
  from Banking and Monetary Statistics 1914-1941, table 160 (`frame-a/bms-1914-1941`, `bms160.py`; W9).
- War years: `war.py` (W1-W11), through `panel.war_at`.

## Steps

1. The null band (`window_a.null_band`) was run on synthetic panels and printed; nothing real was read before it.
   Its scenarios include a hazard on the change year's own π and on its rise, both signs (W10); 1,000 runs, each edge
   printed with its standard error, from 20 batches (W24).
2. For each panel and reading (the headline; panel 2 also on Bernanke and James's note 7), the changes of the panel
   (every line of its routes, whatever its status) fix the pool: no change of the same panel in y-3..y -- a currency
   union's change counts as each member's, and a member of the euro area or of XOF, XAF or XCD from its entry is that
   union's money, no comparator of its own (W15, W21) -- and the panel's source covering the money; a war year in y excludes (P29); a war year that cannot be
   read stays, flagged.
3. Up to 5 comparators per change, nearest on pi(y-1) and on the change in pi from y-3 to y-1, both within 3
   points; ties drawn (seed 1797); each comparator's path ends before its own later change or its entry into the euro
   or a union (flagged).
4. The window: annual -3..+5 and monthly -24..+36, each measure for the change and for each comparator, in
   `series.csv` (what was read) and `unread.csv` (what was not, and why).
5. Statuses (`changes.csv`): only a counted line moves, each move written: to *apart* for no pi in y-3 (before the
   price record, or a gap in the price record where the record begins earlier) and for an exit after a run (panels 1
   and 2); to M0's *censored* when censoring is the only reason (y+5 past the annual common end; month+36 past the
   monthly one). A union's line is apart: no union-level price series.
6. The variants (pool as written, at-risk monies only, war-unreadable dropped, caliper 1 and 5, level-only match, empty
   paths skipped, euro members as monies of their own, XOF/XAF/XCD members as monies of their own) write `changes.csv`
   and `matches.csv` lines; only the headline writes window rows.
7. The descriptions (counted; without overlapping lines; ended unbroken; counted with ended unbroken), each with its
   bands at its own n: the scenarios' band and the placebos (10,000 draws, seeded by the design, the reading, the
   label and n, never by a line's name), each edge with its standard error (the sd of the edge over 20 batches of the
   draws, over sqrt(20); W24). **The placebo's headline** draws pseudo-changes among the panel's real money-years by the pool's
   own past-only rule (no change of the panel in y-3..y), through the same pool and match, each pseudo-change's own path
   cut at its own later change, flagged (W19); **beside it a stratified placebo** (one pseudo-change per real change,
   within 3 years of it and within the caliper of its pi(y-1)); **the variant** `future-clean` is the first build's rule
   (no change through y+5). **Each description line places its mean on all three** (inside, outside, or **at the edge**
   where the mean lies within 2 standard errors of an edge), gives beside the headline the share of cut cells among its
   pseudo-changes and their mean gap, and gives the stratified band's smallest stratum (W25). **A real change's own path is
   not cut at its own later change; a pseudo-change's is** (W19, P4), and **a stratum can hold the real changer's own
   earlier money-years, each cut at its change** (P7); both are said here because they bear on how the headline placebo is
   to be read. A placebo of fewer than 30 cells **cannot be read as a band** (panel 1's has 7 cells for n = 4)
   and is not set against the mean. 84 rows in `placebo-band.csv`.

## Assumptions

- The readings P1-P29 and Q1-Q9 of the protocol, sections 13 and 15 applied: the pool reads information at the change
  only; the match is on the level and on the change in pi.
- **How to read the bands**: a band from chosen scenarios and placebo bands (headline, stratified and `future-clean`); a mean
  inside the scenarios' band and the placebo bands is consistent with no effect; outside one it is not a finding; **at the
  edge of one** (within 2 standard errors) it is neither said inside nor outside. The scenarios'
  price process is a choice; the placebo needs none but assumes random timing and takes the real panel's own non-changers;
  neither has both the real spread and the real timing.
- The window build's own readings W1-W29 (module docstring of `window_a.py`): distance is the sum of the two gaps
  (W1); ties drawn from sha256(1797 + the change's key) (W2); a comparator's path stops before its own later change
  and an empty path contributes nothing (W3); the described gap (W4); panel 4 covers every money through 2022, a candidate from 2012 that cannot be read through Y - 2, Paraguay and Uganda to 2010 (section 21), Ukraine and Mongolia as the named exceptions of section 20 (W5); deposits
  from the depository corporations survey, IFS lines 24 + 25 before it, their units checked for deposits to GDP
  (W6); the run test's 12 months (W7); a variant reading's status (W8); the run test's reserves from BMS table
  160 at $20.67 an ounce, panel 1's *cannot be read* (no monthly reading before June 1928) (W9); the band at the
  described n with same-year scenarios (W10); the placebo band (W11); the run threshold's grid (W12); gold only
  (W13); units of deposits to GDP (W14); unions in the pool (W15); statuses (W16); the descriptions (W17); draws, seeds and
  the edges' error (W18); the placebo's design (W19); units of deposits to GDP, again (W20); unions alike (W21); the
  whole price series for "before the record" (W22); the description, again (W23); the edges' standard error and "at the
  edge" (W24); the three placebos placed, the cut cells, the smallest stratum (W25); units, the remainder (W26); Estonia
  from 1929-01 (W27); the unions' years and their source (W28); the descriptive notes (W29).
- **A departure from P25, named**: the run test reads gold, not foreign exchange (BMS table 160), so a "no" is
  "no (gold only)", flagged `gold_only`, never to be read as "no run". There is no strict variant: the window's deep
  audit page-checked about 50 of the cells the verdicts use against the page images and **found two wrong**: Italy
  1936-09, repaired since (R7), and Estonia 1930-10, now **unreadable over 1929-01 to 1931-08** (`bms160` R8, from 1929-01
  since section 18: the image has 1.8 where the text reads .8, and the column reads .7 from 1929-01); that page check, with
  its two errors, is the record. A line whose run test reads an Estonian cell in that run is "cannot be read".
- Every change, whatever its status, is a change of its panel for the pool's exclusion; a panel-2 member whose only
  change is an exchange control is a non-changer on the headline and is labelled so in `matches.csv`.
- **Panel 4's three unread adopters** (Finland, Spain, Slovakia: their adoption cannot be read) are dropped from every
  pool, even for a change years before their adoption: a selection by their later, undated change. It is mild and
  needed, and said.
- **The bands and the described gap cover pi only** (M8): depreciation, the market split and every trust measure have
  rows in `series.csv` and no comparator summary and no band.
- Each seam's ratio is printed in the `note` of the reading it touches (the step across it in a level; the old lines
  over the survey where the readers give it); a seam is a change of definition where the ratio is far from 1, and of
  units where it is a factor of 100 or more, **or of 10 or more at a source seam** (W20). Deposits to GDP outside 1-300%
  is flagged `units_suspect`, and every year after a break is flagged; so is every year of the World Bank's GDP
  segment where the **median** ratio of the World Bank's GDP to IFS NGDP over their common years is beyond a factor of 2
  (W26: not any single year), and **where the seam names the World Bank segment a units break is not carried into the IFS
  years**; an overlap identical to 1e-3 is no check (the check is then made across the gap). Armenia is not claimed as
  caught.
- **The unions' years** as the union's money (Mali 1984, Guinea-Bissau 1997, Equatorial Guinea 1985, Mauritania to 1972) are
  Garriga's `regional` flag's (W28); the XCD members' are not in it (her flag starts in 1983), and Barbados (the EC dollar to
  1973) is not in the list's unions: nothing moves, no headline match uses it before 1975.
- Not built: dollarisation (no open series splits residents' deposits by currency: IFS a...); deposits to GDP monthly (GDP is annual);
  deposits before 1950 (IFS begins then); the market split and every IFS series before their own first year.

## Uncertainty

- a2-bj-note7 / headline / panel 2: apart 8
- a2-bj-note7 / headline / panel 2: counted 13
- a4-later-or-transition-documents / headline / panel 4: apart 1
- a4-later-or-transition-documents / headline / panel 4: censored 1
- a4-later-or-transition-documents / headline / panel 4: counted 36
- headline / headline / panel 1: apart 9
- headline / headline / panel 1: counted 7
- headline / headline / panel 2: apart 6
- headline / headline / panel 2: counted 11
- headline / headline / panel 3: apart 134
- headline / headline / panel 3: censored 13
- headline / headline / panel 3: counted 238
- headline / headline / panel 3: ended unbroken 16
- headline / headline / panel 4: apart 1
- headline / headline / panel 4: censored 1
- headline / headline / panel 4: counted 30
- rows read: 161612; rows unread: 73347 (by reason: market split 15919; not built 15102; path ended 10085; no currency and deposits readings together (depository corporations survey; IFS 14A and 24 + 25 before it) 9925; no reserves reading (IFS RAXG_USD) at both ends 7517; no depreciation reading (IFS ENDE) 7058; no π reading 4442; no deposits reading (depository corporations survey; IFS 24 + 25 before it) 2734)
- deposits-to-GDP rows flagged units_suspect: 170, by reason: outside 1-300%: 130; GDP seam (the World Bank segment): 67; both: 27 (the first is the second plus the third less the fourth); with a units break flagged: 0
- comparators most reused **within one panel** (headline; a comparator's reuse is counted per panel and reading, so the same money serves more lines across panels): USA 22, DNK 18, AUS 17, CHL 17, CAN 16, MEX 15, MYS 14, TUN 14
- what a mean rests on (W29): a2-bj-note7 panel 2 (counted, n = 7): mean gap +3.81, median +4.25; without USA 1933-03 (gap +8.3, 1 comparator) the mean is +3.07; without SWE 1931-09 (gap -0.3, 1 comparator) the mean is +4.50; 3 of the 7 lines rest on a single comparator
- what a mean rests on (W29): a4-later-or-transition-documents panel 4 (counted, n = 35): mean gap -1.62, median -0.82; without ARG 2016-12 (gap +32.2, 1 comparator) the mean is -2.61; without UZB 2019 (gap -26.3, 2 comparators) the mean is -0.89; 3 of the 35 lines rest on a single comparator
- what a mean rests on (W29): headline panel 1 (counted, n = 4): mean gap +1.89, median +1.77; without NOR 1914 (gap +7.2, 1 comparator) the mean is +0.12; without CHE 1914 (gap -3.2, 1 comparator) the mean is +3.58; 4 of the 4 lines rest on a single comparator
- what a mean rests on (W29): headline panel 2 (counted, n = 7): mean gap +3.78, median +3.97; without USA 1933-03 (gap +8.3, 1 comparator) the mean is +3.02; without SWE 1931-09 (gap -0.3, 1 comparator) the mean is +4.45; 4 of the 7 lines rest on a single comparator
- what a mean rests on (W29): headline panel 3-down (counted, n = 41): mean gap +2.16, median +1.38; without BLR 2008 (gap +22.3, 5 comparators) the mean is +1.65; without KOR 1980 (gap -12.6, 1 comparator) the mean is +2.53; 5 of the 41 lines rest on a single comparator
- what a mean rests on (W29): headline panel 3-up (counted, n = 136): mean gap -0.27, median -0.54; without BGR 1991 (gap +70.6, 1 comparator) the mean is -0.80; without ESP 1980 (gap -48.1, 1 comparator) the mean is +0.08; 14 of the 136 lines rest on a single comparator
- what a mean rests on (W29): headline panel 4 (counted, n = 30): mean gap -2.60, median -0.80; without NZL 1989-12 (gap -22.3, 4 comparators) the mean is -1.92; without SRB 2009-01 (gap +1.3, 5 comparators) the mean is -2.73; 2 of the 30 lines rest on a single comparator

- the run test's verdict moves with the threshold on 6 lines (it never moves a status; the status is the headline's 20%):
  - headline a2 CAN 1931-09: at 20% no (gold only), at 10% yes, at 30% no (gold only)
  - headline a2 GBR 1931-09: at 20% no (gold only), at 10% yes, at 30% no (gold only)
  - headline a2 POL 1936-10: at 20% yes, at 10% yes, at 30% no (gold only)
  - a2-bj-note7 a2-var-bj-note7 CAN 1931-09: at 20% no (gold only), at 10% yes, at 30% no (gold only)
  - a2-bj-note7 a2-var-bj-note7 GBR 1931-09: at 20% no (gold only), at 10% yes, at 30% no (gold only)
  - a2-bj-note7 a2-var-bj-note7 POL 1936-04: at 20% no (gold only), at 10% yes, at 30% no (gold only)

- The described gap under no effect is not zero when the timing depends on the price path, and the real panel's spread
  is not the synthetic one: the bands say by how much, and a mean inside them is consistent with no effect (never "told
  as no effect": W23).
- Comparators' reuse is counted in `matches.csv` (`reuse`, `reuse_counted`).

- a2-bj-note7 panel 2 (counted): n = 13, with a gap 7, mean gap +3.81; null band under no effect [-6.81, +6.41] (edge se 0.17, 0.20) over 9 scenarios at n = 7; headline placebo band [-3.30, +3.04] (edge se 0.04, 0.03) over 10000 draws at n = 7 (42 pseudo-changes) [9 of the headline placebo's 42 pseudo-changes are cut cells (21%), mean gap -4.12 (the uncut ones' +1.15)]; stratified placebo band [-4.71, +3.19] (edge se 0.06, 0.04) over 10000 draws at n = 7 (51 pseudo-changes; smallest stratum 4); future-clean placebo band [-1.53, +3.80] (edge se 0.03, 0.03) over 10000 draws at n = 7 (33 pseudo-changes); the mean lies inside the scenarios' band, outside the headline placebo band, outside the stratified placebo band and at the edge of the future-clean placebo band
- a2-bj-note7 panel 2 (counted, without overlapping lines): n = 13, with a gap 7, mean gap +3.81; null band under no effect [-6.81, +6.41] (edge se 0.17, 0.20) over 9 scenarios at n = 7; headline placebo band [-3.30, +3.04] (edge se 0.04, 0.03) over 10000 draws at n = 7 (42 pseudo-changes) [9 of the headline placebo's 42 pseudo-changes are cut cells (21%), mean gap -4.12 (the uncut ones' +1.15)]; stratified placebo band [-4.71, +3.19] (edge se 0.06, 0.04) over 10000 draws at n = 7 (51 pseudo-changes; smallest stratum 4); future-clean placebo band [-1.53, +3.80] (edge se 0.03, 0.03) over 10000 draws at n = 7 (33 pseudo-changes); the mean lies inside the scenarios' band, outside the headline placebo band, outside the stratified placebo band and at the edge of the future-clean placebo band
- a2-bj-note7 panel 2 (ended unbroken): n = 0, with a gap 0, mean gap n/a; null band under no effect [-6.25, +6.08] (edge se 0.28, 0.17) over 9 scenarios at the list's n, not this line's; headline placebo band not drawn for this line; stratified placebo band not drawn for this line; future-clean placebo band not drawn for this line
- a2-bj-note7 panel 2 (counted, with ended unbroken): n = 13, with a gap 7, mean gap +3.81; null band under no effect [-6.81, +6.41] (edge se 0.17, 0.20) over 9 scenarios at n = 7; headline placebo band [-3.30, +3.04] (edge se 0.04, 0.03) over 10000 draws at n = 7 (42 pseudo-changes) [9 of the headline placebo's 42 pseudo-changes are cut cells (21%), mean gap -4.12 (the uncut ones' +1.15)]; stratified placebo band [-4.71, +3.19] (edge se 0.06, 0.04) over 10000 draws at n = 7 (51 pseudo-changes; smallest stratum 4); future-clean placebo band [-1.53, +3.80] (edge se 0.03, 0.03) over 10000 draws at n = 7 (33 pseudo-changes); the mean lies inside the scenarios' band, outside the headline placebo band, outside the stratified placebo band and at the edge of the future-clean placebo band
- a4-later-or-transition-documents panel 4 (counted): n = 36, with a gap 35, mean gap -1.62; null band under no effect [-2.77, +3.69] (edge se 0.05, 0.05) over 9 scenarios at n = 35; headline placebo band [-2.88, +5.94] (edge se 0.04, 0.11) over 10000 draws at n = 35 (3371 pseudo-changes) [536 of the headline placebo's 3371 pseudo-changes are cut cells (16%), mean gap +0.56 (the uncut ones' +0.18)]; stratified placebo band [-2.40, +4.08] (edge se 0.04, 0.05) over 10000 draws at n = 35 (3222 pseudo-changes; smallest stratum 6); future-clean placebo band [-3.07, +5.27] (edge se 0.06, 0.07) over 10000 draws at n = 35 (2915 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- a4-later-or-transition-documents panel 4 (counted, without overlapping lines): n = 36, with a gap 35, mean gap -1.62; null band under no effect [-2.77, +3.69] (edge se 0.05, 0.05) over 9 scenarios at n = 35; headline placebo band [-2.88, +5.94] (edge se 0.04, 0.11) over 10000 draws at n = 35 (3371 pseudo-changes) [536 of the headline placebo's 3371 pseudo-changes are cut cells (16%), mean gap +0.56 (the uncut ones' +0.18)]; stratified placebo band [-2.40, +4.08] (edge se 0.04, 0.05) over 10000 draws at n = 35 (3222 pseudo-changes; smallest stratum 6); future-clean placebo band [-3.07, +5.27] (edge se 0.06, 0.07) over 10000 draws at n = 35 (2915 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- a4-later-or-transition-documents panel 4 (ended unbroken): n = 0, with a gap 0, mean gap n/a; null band under no effect [-2.81, +3.77] (edge se 0.07, 0.06) over 9 scenarios at the list's n, not this line's; headline placebo band not drawn for this line; stratified placebo band not drawn for this line; future-clean placebo band not drawn for this line
- a4-later-or-transition-documents panel 4 (counted, with ended unbroken): n = 36, with a gap 35, mean gap -1.62; null band under no effect [-2.77, +3.69] (edge se 0.05, 0.05) over 9 scenarios at n = 35; headline placebo band [-2.88, +5.94] (edge se 0.04, 0.11) over 10000 draws at n = 35 (3371 pseudo-changes) [536 of the headline placebo's 3371 pseudo-changes are cut cells (16%), mean gap +0.56 (the uncut ones' +0.18)]; stratified placebo band [-2.40, +4.08] (edge se 0.04, 0.05) over 10000 draws at n = 35 (3222 pseudo-changes; smallest stratum 6); future-clean placebo band [-3.07, +5.27] (edge se 0.06, 0.07) over 10000 draws at n = 35 (2915 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- headline panel 1 (counted): n = 7, with a gap 4, mean gap +1.89; null band under no effect [-5.07, +4.86] (edge se 0.13, 0.13) over 9 scenarios at n = 4; headline placebo band: 7 pseudo-changes at n = 4, cannot be read as a band (fewer than 30 cells) [no pseudo-change of the headline placebo has its path cut (0 of 7)]; stratified placebo band [-7.34, +10.49] (edge se 0.10, 0.13) over 10000 draws at n = 4 (46 pseudo-changes; smallest stratum 17); future-clean placebo band: 7 pseudo-changes at n = 4, cannot be read as a band (fewer than 30 cells); the mean lies inside the scenarios' band and inside the stratified placebo band
- headline panel 1 (counted, without overlapping lines): n = 7, with a gap 4, mean gap +1.89; null band under no effect [-5.07, +4.86] (edge se 0.13, 0.13) over 9 scenarios at n = 4; headline placebo band: 7 pseudo-changes at n = 4, cannot be read as a band (fewer than 30 cells) [no pseudo-change of the headline placebo has its path cut (0 of 7)]; stratified placebo band [-7.34, +10.49] (edge se 0.10, 0.13) over 10000 draws at n = 4 (46 pseudo-changes; smallest stratum 17); future-clean placebo band: 7 pseudo-changes at n = 4, cannot be read as a band (fewer than 30 cells); the mean lies inside the scenarios' band and inside the stratified placebo band
- headline panel 1 (ended unbroken): n = 0, with a gap 0, mean gap n/a; null band under no effect [-4.75, +4.64] (edge se 0.22, 0.16) over 9 scenarios at the list's n, not this line's; headline placebo band not drawn for this line; stratified placebo band not drawn for this line; future-clean placebo band not drawn for this line
- headline panel 1 (counted, with ended unbroken): n = 7, with a gap 4, mean gap +1.89; null band under no effect [-5.07, +4.86] (edge se 0.13, 0.13) over 9 scenarios at n = 4; headline placebo band: 7 pseudo-changes at n = 4, cannot be read as a band (fewer than 30 cells) [no pseudo-change of the headline placebo has its path cut (0 of 7)]; stratified placebo band [-7.34, +10.49] (edge se 0.10, 0.13) over 10000 draws at n = 4 (46 pseudo-changes; smallest stratum 17); future-clean placebo band: 7 pseudo-changes at n = 4, cannot be read as a band (fewer than 30 cells); the mean lies inside the scenarios' band and inside the stratified placebo band
- headline panel 2 (counted): n = 11, with a gap 7, mean gap +3.78; null band under no effect [-6.81, +6.41] (edge se 0.17, 0.20) over 9 scenarios at n = 7; headline placebo band [-3.64, +3.67] (edge se 0.04, 0.04) over 10000 draws at n = 7 (51 pseudo-changes) [12 of the headline placebo's 51 pseudo-changes are cut cells (24%), mean gap -3.83 (the uncut ones' +1.16)]; stratified placebo band [-4.38, +3.30] (edge se 0.06, 0.04) over 10000 draws at n = 7 (60 pseudo-changes; smallest stratum 7); future-clean placebo band [-2.23, +4.74] (edge se 0.04, 0.05) over 10000 draws at n = 7 (39 pseudo-changes); the mean lies inside the scenarios' band, outside the headline placebo band, outside the stratified placebo band and inside the future-clean placebo band
- headline panel 2 (counted, without overlapping lines): n = 11, with a gap 7, mean gap +3.78; null band under no effect [-6.81, +6.41] (edge se 0.17, 0.20) over 9 scenarios at n = 7; headline placebo band [-3.64, +3.67] (edge se 0.04, 0.04) over 10000 draws at n = 7 (51 pseudo-changes) [12 of the headline placebo's 51 pseudo-changes are cut cells (24%), mean gap -3.83 (the uncut ones' +1.16)]; stratified placebo band [-4.38, +3.30] (edge se 0.06, 0.04) over 10000 draws at n = 7 (60 pseudo-changes; smallest stratum 7); future-clean placebo band [-2.23, +4.74] (edge se 0.04, 0.05) over 10000 draws at n = 7 (39 pseudo-changes); the mean lies inside the scenarios' band, outside the headline placebo band, outside the stratified placebo band and inside the future-clean placebo band
- headline panel 2 (ended unbroken): n = 0, with a gap 0, mean gap n/a; null band under no effect [-6.25, +6.08] (edge se 0.28, 0.17) over 9 scenarios at the list's n, not this line's; headline placebo band not drawn for this line; stratified placebo band not drawn for this line; future-clean placebo band not drawn for this line
- headline panel 2 (counted, with ended unbroken): n = 11, with a gap 7, mean gap +3.78; null band under no effect [-6.81, +6.41] (edge se 0.17, 0.20) over 9 scenarios at n = 7; headline placebo band [-3.64, +3.67] (edge se 0.04, 0.04) over 10000 draws at n = 7 (51 pseudo-changes) [12 of the headline placebo's 51 pseudo-changes are cut cells (24%), mean gap -3.83 (the uncut ones' +1.16)]; stratified placebo band [-4.38, +3.30] (edge se 0.06, 0.04) over 10000 draws at n = 7 (60 pseudo-changes; smallest stratum 7); future-clean placebo band [-2.23, +4.74] (edge se 0.04, 0.05) over 10000 draws at n = 7 (39 pseudo-changes); the mean lies inside the scenarios' band, outside the headline placebo band, outside the stratified placebo band and inside the future-clean placebo band
- headline panel 3-down (counted): n = 48, with a gap 41, mean gap +2.16; null band under no effect [-3.00, +3.89] (edge se 0.06, 0.08) over 9 scenarios at n = 41; headline placebo band [-3.12, +5.75] (edge se 0.09, 0.12) over 10000 draws at n = 41 (3594 pseudo-changes) [787 of the headline placebo's 3594 pseudo-changes are cut cells (22%), mean gap +0.36 (the uncut ones' +0.25)]; stratified placebo band [-2.26, +5.17] (edge se 0.02, 0.08) over 10000 draws at n = 40 (2861 pseudo-changes; smallest stratum 11); future-clean placebo band [-2.67, +6.03] (edge se 0.04, 0.13) over 10000 draws at n = 41 (2813 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- headline panel 3-down (counted, without overlapping lines): n = 38, with a gap 34, mean gap +2.68; null band under no effect [-3.05, +4.03] (edge se 0.08, 0.08) over 9 scenarios at n = 34; headline placebo band [-3.27, +6.46] (edge se 0.09, 0.11) over 10000 draws at n = 34 (3594 pseudo-changes) [787 of the headline placebo's 3594 pseudo-changes are cut cells (22%), mean gap +0.36 (the uncut ones' +0.25)]; stratified placebo band [-2.39, +5.97] (edge se 0.02, 0.17) over 10000 draws at n = 34 (2772 pseudo-changes; smallest stratum 11); future-clean placebo band [-2.99, +6.91] (edge se 0.07, 0.15) over 10000 draws at n = 34 (2813 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- headline panel 3-down (ended unbroken): n = 1, with a gap 0, mean gap n/a; null band under no effect [-2.87, +3.71] (edge se 0.05, 0.08) over 9 scenarios at the list's n, not this line's; headline placebo band not drawn for this line; stratified placebo band not drawn for this line; future-clean placebo band not drawn for this line
- headline panel 3-down (counted, with ended unbroken): n = 49, with a gap 41, mean gap +2.16; null band under no effect [-3.00, +3.89] (edge se 0.06, 0.08) over 9 scenarios at n = 41; headline placebo band [-3.12, +5.75] (edge se 0.09, 0.12) over 10000 draws at n = 41 (3594 pseudo-changes) [787 of the headline placebo's 3594 pseudo-changes are cut cells (22%), mean gap +0.36 (the uncut ones' +0.25)]; stratified placebo band [-2.26, +5.17] (edge se 0.02, 0.08) over 10000 draws at n = 40 (2861 pseudo-changes; smallest stratum 11); future-clean placebo band [-2.67, +6.03] (edge se 0.04, 0.13) over 10000 draws at n = 41 (2813 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- headline panel 3-up (counted): n = 190, with a gap 136, mean gap -0.27; null band under no effect [-2.29, +3.06] (edge se 0.04, 0.03) over 9 scenarios at n = 136; headline placebo band [-1.92, +2.90] (edge se 0.05, 0.05) over 10000 draws at n = 136 (3594 pseudo-changes) [787 of the headline placebo's 3594 pseudo-changes are cut cells (22%), mean gap +0.36 (the uncut ones' +0.25)]; stratified placebo band [-1.51, +2.20] (edge se 0.02, 0.03) over 10000 draws at n = 136 (3400 pseudo-changes; smallest stratum 2); future-clean placebo band [-1.49, +2.74] (edge se 0.02, 0.03) over 10000 draws at n = 136 (2813 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- headline panel 3-up (counted, without overlapping lines): n = 162, with a gap 119, mean gap +0.11; null band under no effect [-2.37, +3.15] (edge se 0.03, 0.05) over 9 scenarios at n = 119; headline placebo band [-2.25, +3.09] (edge se 0.07, 0.06) over 10000 draws at n = 119 (3594 pseudo-changes) [787 of the headline placebo's 3594 pseudo-changes are cut cells (22%), mean gap +0.36 (the uncut ones' +0.25)]; stratified placebo band [-1.66, +2.40] (edge se 0.03, 0.03) over 10000 draws at n = 119 (3385 pseudo-changes; smallest stratum 2); future-clean placebo band [-1.57, +3.06] (edge se 0.02, 0.05) over 10000 draws at n = 119 (2813 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- headline panel 3-up (ended unbroken): n = 15, with a gap 3, mean gap -2.91; null band under no effect [-8.12, +9.59] (edge se 0.34, 0.34) over 9 scenarios at n = 3; headline placebo band [-10.60, +12.17] (edge se 0.33, 0.48) over 10000 draws at n = 3 (3594 pseudo-changes) [787 of the headline placebo's 3594 pseudo-changes are cut cells (22%), mean gap +0.36 (the uncut ones' +0.25)]; stratified placebo band [-4.81, +7.05] (edge se 0.08, 0.75) over 10000 draws at n = 3 (462 pseudo-changes; smallest stratum 125); future-clean placebo band [-8.26, +12.17] (edge se 0.36, 0.51) over 10000 draws at n = 3 (2813 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- headline panel 3-up (counted, with ended unbroken): n = 205, with a gap 139, mean gap -0.33; null band under no effect [-2.28, +3.00] (edge se 0.04, 0.05) over 9 scenarios at n = 139; headline placebo band [-1.81, +2.83] (edge se 0.04, 0.04) over 10000 draws at n = 139 (3594 pseudo-changes) [787 of the headline placebo's 3594 pseudo-changes are cut cells (22%), mean gap +0.36 (the uncut ones' +0.25)]; stratified placebo band [-1.49, +2.10] (edge se 0.02, 0.04) over 10000 draws at n = 139 (3400 pseudo-changes; smallest stratum 2); future-clean placebo band [-1.43, +2.77] (edge se 0.02, 0.03) over 10000 draws at n = 139 (2813 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, inside the stratified placebo band and inside the future-clean placebo band
- headline panel 4 (counted): n = 30, with a gap 30, mean gap -2.60; null band under no effect [-2.85, +3.74] (edge se 0.07, 0.05) over 9 scenarios at n = 30; headline placebo band [-3.16, +6.30] (edge se 0.05, 0.07) over 10000 draws at n = 30 (3365 pseudo-changes) [533 of the headline placebo's 3365 pseudo-changes are cut cells (16%), mean gap +0.52 (the uncut ones' +0.19)]; stratified placebo band [-2.52, +4.69] (edge se 0.03, 0.12) over 10000 draws at n = 30 (3153 pseudo-changes; smallest stratum 29); future-clean placebo band [-3.23, +6.14] (edge se 0.07, 0.09) over 10000 draws at n = 30 (2912 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, outside the stratified placebo band and inside the future-clean placebo band
- headline panel 4 (counted, without overlapping lines): n = 30, with a gap 30, mean gap -2.60; null band under no effect [-2.85, +3.74] (edge se 0.07, 0.05) over 9 scenarios at n = 30; headline placebo band [-3.16, +6.30] (edge se 0.05, 0.07) over 10000 draws at n = 30 (3365 pseudo-changes) [533 of the headline placebo's 3365 pseudo-changes are cut cells (16%), mean gap +0.52 (the uncut ones' +0.19)]; stratified placebo band [-2.52, +4.69] (edge se 0.03, 0.12) over 10000 draws at n = 30 (3153 pseudo-changes; smallest stratum 29); future-clean placebo band [-3.23, +6.14] (edge se 0.07, 0.09) over 10000 draws at n = 30 (2912 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, outside the stratified placebo band and inside the future-clean placebo band
- headline panel 4 (ended unbroken): n = 0, with a gap 0, mean gap n/a; null band under no effect [-2.81, +3.77] (edge se 0.07, 0.06) over 9 scenarios at the list's n, not this line's; headline placebo band not drawn for this line; stratified placebo band not drawn for this line; future-clean placebo band not drawn for this line
- headline panel 4 (counted, with ended unbroken): n = 30, with a gap 30, mean gap -2.60; null band under no effect [-2.85, +3.74] (edge se 0.07, 0.05) over 9 scenarios at n = 30; headline placebo band [-3.16, +6.30] (edge se 0.05, 0.07) over 10000 draws at n = 30 (3365 pseudo-changes) [533 of the headline placebo's 3365 pseudo-changes are cut cells (16%), mean gap +0.52 (the uncut ones' +0.19)]; stratified placebo band [-2.52, +4.69] (edge se 0.03, 0.12) over 10000 draws at n = 30 (3153 pseudo-changes; smallest stratum 29); future-clean placebo band [-3.23, +6.14] (edge se 0.07, 0.09) over 10000 draws at n = 30 (2912 pseudo-changes); the mean lies inside the scenarios' band, inside the headline placebo band, outside the stratified placebo band and inside the future-clean placebo band
- panel 2, CSK: the readings disagree: headline 1934-02, apart, run test no (gold only); note 7 1931-09, apart, run test no (gold only)
- panel 2, DEU: the readings disagree: headline no line; note 7 1931-07, apart, run test yes
- panel 2, EST: the readings disagree: headline 1933-06, apart, run test no (gold only); note 7 1931-11, apart, run test cannot be read
- panel 2, GRC: the readings disagree: headline 1932-04, counted, run test no (gold only); note 7 1931-09, counted, run test no (gold only)
- panel 2, HUN: the readings disagree: headline no line; note 7 1931-07, apart, run test yes
- panel 2, ITA: the readings disagree: headline 1936-10, apart, run test yes; note 7 1934-05, counted, run test no (gold only)
- panel 2, LVA: the readings disagree: headline no line; note 7 1931-10, apart, run test no (gold only)
- panel 2, POL: the readings disagree: headline 1936-10, apart, run test yes; note 7 1936-04, counted, run test no (gold only)
- panel 2, ROU: the readings disagree: headline no line; note 7 1932-05, apart, run test no (gold only)

## Needs

- Dollarisation: no open series (FT-001-M3-sources.md, 'Not found'); the IMF's Financial Soundness Indicators FSDFCD (foreign-currency liabilities to total liabilities) is named there, not frozen.
- Panel 4's candidates from 2012: the AREAER is frozen and its inflation-targeting column is coded in data/reconstructed/ft001-a-areaer/; the announcements are read (sections 17 and 21: five adopters, four non-adopters, nine candidates that cannot be read); what is still needed is, for each of those nine, its central bank's own announcement, frozen (P21). Until then a candidate that cannot be read is covered only through Y - 2, Y the first edition that lists it, and panel 4 covers every other money through 2022 (W5, section 19). Paraguay's 2011 adoption is listed nowhere (a gap of the pre-2012 list): it is uncovered from 2011.
- The entry and exit years of XOF, XAF and XCD's members as their union's money (W21, W28): the four of Mali 1984, Guinea-Bissau 1997, Equatorial Guinea 1985 and Mauritania to 1972 are Garriga's `regional` flag's (frozen, read by frame_a.py); what is still needed is a frozen source for the XCD members' years (the EC dollar dates from 1965, Grenada 1968; her flag starts in 1983) and for Barbados (the EC dollar to 1973, not in frame_a's unions: nothing moves).
- Foreign exchange for the run test (section 15, O3): the Bank of England's, the Bank of France's and the Reichsbank's balance sheets, BMS 1914-1941 tables 164, 165 and 167, to parse and build as a variant (gold and foreign exchange); until then a "no" of the run test is "no (gold only)" (W13).

## The null band

At the list's counted n; each description line's band at its own n is in `null-band.csv` (rows with a `line`).

```
The null band: the described gap (the change's after-minus-before in π, less its matched comparators')
under NO effect of any change, on synthetic panels shaped like each real one; π in points.
Headline: pool 'past' (no change in y-3..y), match on π(y-1) and on the change in π (caliper 3).
Variants: pool 'written' (none in y-3..y+3); match on the level alone (P28 as first written).
Each band edge is followed by its standard error (se): the sd of the edge over 20 batches of the runs, over sqrt(20).

panel  scenario                   pool     match          n    mean  band lo    se  band hi    se  sd/chg  matched  >|1|
1      after a fall, with drift   past     level+rise     7   -0.00    -4.75  0.22    +4.64  0.16    3.48     0.70  0.65
1      after a rise (pressure)    past     level+rise     7   +0.01    -3.84  0.14    +3.50  0.10    2.99     0.78  0.60
1      after high pi              past     level+rise     7   -0.24    -3.81  0.13    +3.12  0.14    3.05     0.79  0.57
1      after high pi, with drift  past     level+rise     7   -0.04    -4.72  0.20    +4.53  0.14    3.51     0.67  0.67
1      random timing              past     level+rise     7   +0.01    -3.29  0.12    +3.21  0.11    3.10     0.86  0.54
1      same year: a fall          past     level+rise     7   -1.12    -4.22  0.12    +2.10  0.12    3.08     0.87  0.63
1      same year: a rise          past     level+rise     7   +0.98    -2.31  0.12    +4.08  0.13    3.03     0.86  0.60
1      same year: high pi         past     level+rise     7   +0.78    -2.27  0.10    +4.17  0.15    3.10     0.84  0.55
1      same year: low pi          past     level+rise     7   -0.78    -4.00  0.13    +2.37  0.12    3.01     0.84  0.57
1      after a fall, with drift   past     level          7   +0.89    -2.75  0.11    +4.38  0.10    3.63     0.95  0.64
1      after a rise (pressure)    past     level          7   -0.47    -3.41  0.09    +2.41  0.11    2.98     0.96  0.51
1      after high pi              past     level          7   -0.24    -3.51  0.12    +2.96  0.15    2.98     0.92  0.52
1      after high pi, with drift  past     level          7   +0.03    -4.14  0.12    +4.53  0.20    3.57     0.84  0.64
1      random timing              past     level          7   -0.02    -2.90  0.11    +2.93  0.10    3.01     0.97  0.50
1      same year: a fall          past     level          7   -1.18    -4.12  0.12    +1.83  0.09    2.98     0.97  0.62
1      same year: a rise          past     level          7   +1.02    -1.68  0.09    +3.78  0.10    2.93     0.96  0.59
1      same year: high pi         past     level          7   +0.85    -2.01  0.09    +3.85  0.11    2.98     0.96  0.57
1      same year: low pi          past     level          7   -0.78    -3.57  0.13    +2.43  0.14    2.95     0.95  0.55
1      after a fall, with drift   written  level          7   +0.89    -2.82  0.12    +4.36  0.10    3.59     0.95  0.64
1      after a rise (pressure)    written  level          7   -0.48    -3.34  0.09    +2.36  0.10    2.95     0.97  0.50
1      after high pi              written  level          7   -0.27    -3.51  0.12    +2.86  0.14    2.94     0.92  0.51
1      after high pi, with drift  written  level          7   +0.01    -4.11  0.13    +4.35  0.18    3.53     0.84  0.64
1      random timing              written  level          7   -0.00    -2.79  0.11    +2.91  0.12    2.97     0.97  0.48
1      same year: a fall          written  level          7   -1.20    -4.03  0.12    +1.77  0.10    2.94     0.97  0.62
1      same year: a rise          written  level          7   +1.03    -1.69  0.09    +3.74  0.09    2.90     0.97  0.60
1      same year: high pi         written  level          7   +0.82    -2.09  0.10    +3.78  0.10    2.95     0.96  0.57
1      same year: low pi          written  level          7   -0.77    -3.48  0.12    +2.43  0.14    2.91     0.95  0.55
1      after a fall, with drift   written  level+rise     7   -0.00    -4.75  0.22    +4.61  0.16    3.47     0.70  0.64
1      after a rise (pressure)    written  level+rise     7   +0.00    -3.92  0.14    +3.50  0.10    2.98     0.78  0.60
1      after high pi              written  level+rise     7   -0.25    -3.81  0.13    +3.11  0.15    3.03     0.79  0.56
1      after high pi, with drift  written  level+rise     7   -0.05    -4.72  0.19    +4.53  0.15    3.50     0.67  0.67
1      random timing              written  level+rise     7   +0.01    -3.21  0.12    +3.17  0.11    3.08     0.86  0.54
1      same year: a fall          written  level+rise     7   -1.12    -4.22  0.12    +2.13  0.12    3.06     0.87  0.63
1      same year: a rise          written  level+rise     7   +0.98    -2.29  0.11    +4.08  0.13    3.02     0.86  0.61
1      same year: high pi         written  level+rise     7   +0.78    -2.32  0.11    +4.16  0.15    3.09     0.84  0.55
1      same year: low pi          written  level+rise     7   -0.78    -4.00  0.14    +2.45  0.12    2.99     0.84  0.57
2      after a fall, with drift   past     level+rise    15   -0.02    -5.34  0.16    +5.35  0.15    5.30     0.47  0.74
2      after a rise (pressure)    past     level+rise    15   -0.08    -4.92  0.19    +4.23  0.11    4.62     0.54  0.62
2      after high pi              past     level+rise    15   -0.66    -5.22  0.21    +3.35  0.12    4.80     0.59  0.64
2      after high pi, with drift  past     level+rise    15   -0.46    -6.25  0.28    +4.82  0.18    5.40     0.49  0.72
2      random timing              past     level+rise    15   +0.07    -4.07  0.17    +4.07  0.18    4.75     0.67  0.59
2      same year: a fall          past     level+rise    15   -2.19    -6.08  0.16    +1.60  0.13    4.71     0.66  0.77
2      same year: a rise          past     level+rise    15   +2.10    -1.93  0.18    +6.08  0.17    4.73     0.66  0.77
2      same year: high pi         past     level+rise    15   +1.43    -2.20  0.16    +5.45  0.16    4.64     0.66  0.69
2      same year: low pi          past     level+rise    15   -1.48    -5.48  0.16    +2.47  0.09    4.65     0.65  0.72
2      after a fall, with drift   past     level         15   +1.04    -2.65  0.16    +5.05  0.14    5.21     0.88  0.66
2      after a rise (pressure)    past     level         15   -0.64    -4.33  0.14    +2.75  0.09    4.45     0.91  0.57
2      after high pi              past     level         15   -0.66    -4.84  0.17    +2.52  0.12    4.48     0.86  0.60
2      after high pi, with drift  past     level         15   -0.68    -5.24  0.15    +3.41  0.17    5.39     0.79  0.65
2      random timing              past     level         15   +0.06    -3.14  0.09    +3.23  0.09    4.40     0.94  0.51
2      same year: a fall          past     level         15   -2.24    -5.60  0.12    +1.16  0.11    4.37     0.92  0.81
2      same year: a rise          past     level         15   +2.08    -1.23  0.12    +5.50  0.15    4.35     0.92  0.78
2      same year: high pi         past     level         15   +1.30    -1.75  0.13    +4.33  0.14    4.33     0.92  0.63
2      same year: low pi          past     level         15   -1.36    -4.57  0.12    +1.86  0.11    4.35     0.91  0.66
2      after a fall, with drift   written  level         15   +0.30    -3.49  0.14    +4.19  0.17    5.13     0.85  0.63
2      after a rise (pressure)    written  level         15   -0.02    -3.39  0.14    +3.41  0.10    4.33     0.89  0.53
2      after high pi              written  level         15   +0.30    -3.10  0.15    +3.93  0.12    4.28     0.82  0.57
2      after high pi, with drift  written  level         15   +0.63    -3.52  0.16    +4.62  0.14    5.17     0.71  0.65
2      random timing              written  level         15   -0.02    -3.29  0.09    +3.08  0.12    4.33     0.90  0.52
2      same year: a fall          written  level         15   -1.77    -4.97  0.11    +1.66  0.11    4.25     0.88  0.75
2      same year: a rise          written  level         15   +1.62    -1.53  0.11    +4.92  0.14    4.20     0.88  0.72
2      same year: high pi         written  level         15   +1.75    -1.10  0.09    +4.68  0.12    4.22     0.88  0.72
2      same year: low pi          written  level         15   -1.81    -5.08  0.14    +1.41  0.12    4.24     0.87  0.74
2      after a fall, with drift   written  level+rise    15   -0.72    -5.96  0.16    +4.45  0.19    5.03     0.42  0.74
2      after a rise (pressure)    written  level+rise    15   +0.52    -3.86  0.19    +4.82  0.16    4.46     0.50  0.66
2      after high pi              written  level+rise    15   +0.32    -3.62  0.14    +4.50  0.18    4.43     0.52  0.65
2      after high pi, with drift  written  level+rise    15   +0.81    -4.86  0.25    +6.93  0.29    4.93     0.41  0.72
2      random timing              written  level+rise    15   -0.01    -3.92  0.12    +4.01  0.17    4.54     0.60  0.61
2      same year: a fall          written  level+rise    15   -1.71    -5.50  0.17    +2.40  0.15    4.50     0.58  0.73
2      same year: a rise          written  level+rise    15   +1.60    -2.38  0.19    +5.79  0.16    4.45     0.59  0.71
2      same year: high pi         written  level+rise    15   +1.85    -1.74  0.13    +5.75  0.15    4.41     0.58  0.73
2      same year: low pi          written  level+rise    15   -1.89    -5.96  0.21    +2.05  0.12    4.42     0.57  0.74
3-down after a fall, with drift   past     level+rise    58   +0.22    -1.55  0.06    +2.09  0.08    5.90     0.83  0.28
3-down after a rise (pressure)    past     level+rise    58   +0.03    -1.62  0.06    +1.68  0.05    5.46     0.85  0.23
3-down after high pi              past     level+rise    58   -0.08    -2.04  0.06    +1.99  0.07    6.27     0.74  0.32
3-down after high pi, with drift  past     level+rise    58   -0.13    -2.17  0.09    +1.86  0.07    6.58     0.73  0.34
3-down random timing              past     level+rise    58   +0.03    -1.37  0.06    +1.46  0.04    5.24     0.94  0.17
3-down same year: a fall          past     level+rise    58   -1.33    -2.87  0.05    +0.16  0.06    5.37     0.90  0.66
3-down same year: a rise          past     level+rise    58   +2.01    +0.58  0.04    +3.66  0.05    5.85     0.93  0.89
3-down same year: high pi         past     level+rise    58   +1.75    -0.22  0.05    +3.71  0.08    6.47     0.79  0.78
3-down same year: low pi          past     level+rise    58   -0.63    -1.79  0.04    +0.57  0.04    4.58     0.97  0.27
3-down after a fall, with drift   past     level         58   +2.10    +0.32  0.07    +4.12  0.07    6.66     0.99  0.88
3-down after a rise (pressure)    past     level         58   -0.73    -2.32  0.05    +0.86  0.06    5.82     0.97  0.38
3-down after high pi              past     level         58   -0.06    -1.99  0.06    +1.84  0.09    6.69     0.88  0.28
3-down after high pi, with drift  past     level         58   -0.05    -2.15  0.08    +1.92  0.05    7.02     0.87  0.32
3-down random timing              past     level         58   -0.02    -1.48  0.05    +1.45  0.06    5.51     0.99  0.20
3-down same year: a fall          past     level         58   -1.60    -3.11  0.06    -0.17  0.06    5.66     0.97  0.78
3-down same year: a rise          past     level         58   +2.42    +0.83  0.04    +4.29  0.07    6.38     0.99  0.96
3-down same year: high pi         past     level         58   +2.29    +0.21  0.07    +4.40  0.09    7.10     0.93  0.90
3-down same year: low pi          past     level         58   -0.84    -2.05  0.05    +0.39  0.04    4.72     1.00  0.42
3-down after a fall, with drift   written  level         58   +1.87    +0.05  0.07    +3.91  0.07    6.62     0.99  0.83
3-down after a rise (pressure)    written  level         58   -0.38    -1.93  0.05    +1.10  0.07    5.69     0.96  0.24
3-down after high pi              written  level         58   +0.67    -1.15  0.07    +2.71  0.08    6.42     0.87  0.37
3-down after high pi, with drift  written  level         58   +0.72    -1.27  0.08    +2.65  0.06    6.77     0.86  0.44
3-down random timing              written  level         58   -0.02    -1.43  0.05    +1.44  0.05    5.48     0.99  0.19
3-down same year: a fall          written  level         58   -1.41    -2.86  0.06    +0.03  0.05    5.56     0.97  0.71
3-down same year: a rise          written  level         58   +2.33    +0.71  0.04    +4.17  0.07    6.35     0.99  0.94
3-down same year: high pi         written  level         58   +2.67    +0.74  0.07    +4.73  0.06    6.99     0.92  0.95
3-down same year: low pi          written  level         58   -1.01    -2.19  0.04    +0.20  0.04    4.69     1.00  0.52
3-down after a fall, with drift   written  level+rise    58   -0.01    -1.73  0.05    +1.77  0.07    5.84     0.83  0.27
3-down after a rise (pressure)    written  level+rise    58   +0.27    -1.41  0.06    +1.91  0.05    5.37     0.85  0.25
3-down after high pi              written  level+rise    58   +0.43    -1.45  0.06    +2.53  0.09    6.00     0.73  0.33
3-down after high pi, with drift  written  level+rise    58   +0.43    -1.53  0.08    +2.46  0.06    6.34     0.71  0.36
3-down random timing              written  level+rise    58   +0.03    -1.39  0.06    +1.49  0.05    5.22     0.94  0.17
3-down same year: a fall          written  level+rise    58   -1.16    -2.71  0.06    +0.29  0.05    5.28     0.90  0.58
3-down same year: a rise          written  level+rise    58   +1.92    +0.46  0.04    +3.50  0.05    5.80     0.93  0.86
3-down same year: high pi         written  level+rise    58   +2.03    +0.08  0.06    +4.01  0.08    6.34     0.78  0.85
3-down same year: low pi          written  level+rise    58   -0.78    -1.95  0.04    +0.38  0.04    4.56     0.97  0.37
3-up   after a fall, with drift   past     level+rise   272   +0.18    -0.62  0.03    +0.98  0.03    5.98     0.83  0.03
3-up   after a rise (pressure)    past     level+rise   272   +0.08    -0.73  0.03    +0.85  0.03    5.56     0.85  0.01
3-up   after high pi              past     level+rise   272   -0.11    -1.05  0.04    +0.89  0.04    6.37     0.74  0.05
3-up   after high pi, with drift  past     level+rise   272   -0.15    -1.12  0.03    +0.85  0.03    6.69     0.73  0.05
3-up   random timing              past     level+rise   272   +0.05    -0.64  0.03    +0.74  0.03    5.30     0.94  0.01
3-up   same year: a fall          past     level+rise   272   -1.31    -2.08  0.03    -0.56  0.03    5.43     0.90  0.78
3-up   same year: a rise          past     level+rise   272   +1.98    +1.18  0.04    +2.77  0.03    5.92     0.93  0.99
3-up   same year: high pi         past     level+rise   272   +1.73    +0.78  0.03    +2.81  0.04    6.60     0.79  0.93
3-up   same year: low pi          past     level+rise   272   -0.65    -1.21  0.02    -0.09  0.02    4.59     0.97  0.13
3-up   after a fall, with drift   past     level        272   +2.10    +1.22  0.03    +3.03  0.03    6.75     0.99  0.99
3-up   after a rise (pressure)    past     level        272   -0.70    -1.46  0.03    +0.08  0.02    5.89     0.97  0.23
3-up   after high pi              past     level        272   -0.07    -1.04  0.03    +0.92  0.05    6.79     0.88  0.04
3-up   after high pi, with drift  past     level        272   -0.08    -1.04  0.05    +0.91  0.03    7.11     0.88  0.05
3-up   random timing              past     level        272   +0.00    -0.69  0.02    +0.70  0.03    5.60     0.99  0.01
3-up   same year: a fall          past     level        272   -1.57    -2.30  0.02    -0.82  0.03    5.68     0.98  0.93
3-up   same year: a rise          past     level        272   +2.38    +1.49  0.03    +3.30  0.04    6.46     0.99  1.00
3-up   same year: high pi         past     level        272   +2.25    +1.19  0.03    +3.45  0.05    7.18     0.93  0.99
3-up   same year: low pi          past     level        272   -0.86    -1.43  0.02    -0.28  0.02    4.79     1.00  0.33
3-up   after a fall, with drift   written  level        272   +1.86    +0.98  0.03    +2.76  0.03    6.72     0.99  0.97
3-up   after a rise (pressure)    written  level        272   -0.34    -1.07  0.02    +0.41  0.02    5.75     0.96  0.05
3-up   after high pi              written  level        272   +0.65    -0.28  0.03    +1.59  0.04    6.52     0.87  0.24
3-up   after high pi, with drift  written  level        272   +0.68    -0.26  0.04    +1.70  0.04    6.86     0.86  0.27
3-up   random timing              written  level        272   +0.00    -0.69  0.02    +0.70  0.03    5.56     0.99  0.01
3-up   same year: a fall          written  level        272   -1.39    -2.08  0.03    -0.66  0.03    5.58     0.97  0.85
3-up   same year: a rise          written  level        272   +2.29    +1.40  0.03    +3.23  0.04    6.43     0.99  1.00
3-up   same year: high pi         written  level        272   +2.63    +1.54  0.03    +3.85  0.06    7.08     0.92  1.00
3-up   same year: low pi          written  level        272   -1.03    -1.63  0.02    -0.43  0.02    4.75     1.00  0.52
3-up   after a fall, with drift   written  level+rise   272   -0.04    -0.81  0.03    +0.76  0.03    5.92     0.83  0.01
3-up   after a rise (pressure)    written  level+rise   272   +0.32    -0.42  0.02    +1.08  0.03    5.47     0.84  0.04
3-up   after high pi              written  level+rise   272   +0.40    -0.50  0.03    +1.40  0.04    6.09     0.73  0.11
3-up   after high pi, with drift  written  level+rise   272   +0.40    -0.58  0.03    +1.36  0.02    6.44     0.71  0.13
3-up   random timing              written  level+rise   272   +0.05    -0.65  0.03    +0.74  0.03    5.27     0.94  0.00
3-up   same year: a fall          written  level+rise   272   -1.16    -1.92  0.02    -0.39  0.02    5.35     0.90  0.66
3-up   same year: a rise          written  level+rise   272   +1.88    +1.06  0.03    +2.69  0.03    5.88     0.93  0.99
3-up   same year: high pi         written  level+rise   272   +2.00    +1.00  0.03    +3.15  0.05    6.48     0.78  0.97
3-up   same year: low pi          written  level+rise   272   -0.79    -1.36  0.02    -0.24  0.02    4.57     0.97  0.25
4      after a fall, with drift   past     level+rise    31   +0.13    -1.78  0.07    +2.27  0.11    4.98     0.81  0.32
4      after a rise (pressure)    past     level+rise    31   +0.03    -1.78  0.07    +2.02  0.07    4.49     0.83  0.29
4      after high pi              past     level+rise    31   -0.34    -2.56  0.09    +1.79  0.09    5.06     0.79  0.39
4      after high pi, with drift  past     level+rise    31   -0.39    -2.69  0.10    +2.01  0.11    5.39     0.78  0.42
4      random timing              past     level+rise    31   +0.08    -1.56  0.06    +1.77  0.07    4.18     0.96  0.24
4      same year: a fall          past     level+rise    31   -1.02    -2.81  0.07    +0.75  0.05    4.30     0.91  0.53
4      same year: a rise          past     level+rise    31   +1.83    +0.04  0.05    +3.77  0.06    4.93     0.94  0.81
4      same year: high pi         past     level+rise    31   +1.28    -0.79  0.06    +3.44  0.09    5.32     0.84  0.60
4      same year: low pi          past     level+rise    31   -0.41    -1.82  0.04    +1.13  0.06    3.66     0.98  0.25
4      after a fall, with drift   past     level         31   +2.21    +0.14  0.07    +4.41  0.10    5.87     0.99  0.86
4      after a rise (pressure)    past     level         31   -0.51    -2.38  0.07    +1.26  0.07    4.79     0.96  0.36
4      after high pi              past     level         31   -0.49    -2.76  0.06    +1.51  0.08    5.32     0.92  0.40
4      after high pi, with drift  past     level         31   -0.55    -2.84  0.08    +1.80  0.08    5.72     0.91  0.44
4      random timing              past     level         31   +0.05    -1.53  0.07    +1.71  0.06    4.42     0.99  0.25
4      same year: a fall          past     level         31   -1.21    -2.98  0.06    +0.56  0.06    4.50     0.97  0.60
4      same year: a rise          past     level         31   +2.16    +0.33  0.05    +4.32  0.09    5.43     0.99  0.86
4      same year: high pi         past     level         31   +1.42    -0.74  0.07    +3.67  0.09    5.66     0.95  0.66
4      same year: low pi          past     level         31   -0.57    -1.96  0.04    +1.02  0.06    3.79     1.00  0.32
4      after a fall, with drift   written  level         31   +2.17    +0.12  0.07    +4.38  0.10    5.86     0.99  0.85
4      after a rise (pressure)    written  level         31   -0.46    -2.28  0.07    +1.32  0.07    4.76     0.96  0.34
4      after high pi              written  level         31   -0.33    -2.47  0.06    +1.57  0.07    5.26     0.91  0.36
4      after high pi, with drift  written  level         31   -0.38    -2.65  0.08    +1.90  0.09    5.67     0.91  0.40
4      random timing              written  level         31   +0.05    -1.52  0.07    +1.72  0.06    4.41     0.99  0.25
4      same year: a fall          written  level         31   -1.17    -2.97  0.07    +0.58  0.06    4.49     0.97  0.58
4      same year: a rise          written  level         31   +2.15    +0.30  0.05    +4.29  0.09    5.43     0.99  0.86
4      same year: high pi         written  level         31   +1.51    -0.64  0.08    +3.72  0.09    5.64     0.95  0.69
4      same year: low pi          written  level         31   -0.60    -1.98  0.04    +1.00  0.06    3.79     1.00  0.33
4      after a fall, with drift   written  level+rise    31   +0.09    -1.81  0.07    +2.18  0.11    4.97     0.81  0.32
4      after a rise (pressure)    written  level+rise    31   +0.08    -1.75  0.07    +2.04  0.07    4.47     0.83  0.28
4      after high pi              written  level+rise    31   -0.23    -2.38  0.07    +1.86  0.09    5.00     0.78  0.37
4      after high pi, with drift  written  level+rise    31   -0.26    -2.61  0.10    +2.17  0.10    5.35     0.77  0.40
4      random timing              written  level+rise    31   +0.09    -1.57  0.06    +1.72  0.07    4.18     0.96  0.24
4      same year: a fall          written  level+rise    31   -0.99    -2.79  0.07    +0.77  0.05    4.29     0.91  0.51
4      same year: a rise          written  level+rise    31   +1.81    +0.04  0.05    +3.79  0.06    4.93     0.94  0.81
4      same year: high pi         written  level+rise    31   +1.35    -0.79  0.06    +3.55  0.09    5.28     0.84  0.62
4      same year: low pi          written  level+rise    31   -0.43    -1.84  0.04    +1.13  0.06    3.66     0.98  0.26

panel 1: headline band over every scenario [-4.75, +4.64] (edge se 0.22, 0.16) over 9 scenarios; level-only match, written pool [-4.11, +4.36] (edge se 0.13, 0.10) over 9 scenarios
panel 2: headline band over every scenario [-6.25, +6.08] (edge se 0.28, 0.17) over 9 scenarios; level-only match, written pool [-5.08, +4.92] (edge se 0.14, 0.14) over 9 scenarios
panel 3-down: headline band over every scenario [-2.87, +3.71] (edge se 0.05, 0.08) over 9 scenarios; level-only match, written pool [-2.86, +4.73] (edge se 0.06, 0.06) over 9 scenarios
panel 3-up: headline band over every scenario [-2.08, +2.81] (edge se 0.03, 0.04) over 9 scenarios; level-only match, written pool [-2.08, +3.85] (edge se 0.03, 0.06) over 9 scenarios
panel 4: headline band over every scenario [-2.81, +3.77] (edge se 0.07, 0.06) over 9 scenarios; level-only match, written pool [-2.97, +4.38] (edge se 0.07, 0.10) over 9 scenarios
```
