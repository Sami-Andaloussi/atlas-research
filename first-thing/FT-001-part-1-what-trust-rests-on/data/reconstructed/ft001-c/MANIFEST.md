# ft001-c — reconstructed dataset

FT-001's frame c: every entry of a money into fiscal strain — a year when its debt, its deficit, its central
bank's financing of the deficit, or a base-money episode reaches its line (M0 v4.2 section 5 c) — one spell per
horizon, followed over H years for a break of frame b, one line each in M0's case-line format. Built by rule
from the frozen sources under the coders' protocol `bank/maps/FT-001/missions/FT-001-M3-panel.md` (77a730a;
**section 8, the readings amended after frame c's deep audit, d164fa9**), section 4 (c1–c12) and readings
R8–R10, R14, R19–R30. Every line carries M0 v4.2's pair hash (`1160cab0bd84…e58d4`, commit 3163162).

**This is frame c's fifth build** (2026-10-02). The fourth (fbbef5c) went to a small check (Sonnet, isolated:
`bank/checks/FT-001-M3-frames-c-k-fourth-build-2026-10-02-sonnet-small-check.md`). The check found that `war.py`'s
W13 did not map Tonga (GW 972, COW 955 from 1999), so Tonga's UCDP years read *no*. W13 was fixed (e93d2da), and
the fifth build differs from the fourth in **one status**: Tonga 2011 (c2, held) goes from counted to *cannot be
read*; and Tonga 2001's war years in H (c4, counted, held) gain 2 unreadable ("0" becomes "0 (+2 unreadable)"). The figures below are the fifth build's. The fourth differed from the third by one reading, W12, coded and tested
before it ran (protocol section 9; `war.py` W12–W13, 776174a; the switch and the variant, 5479e73):
- after COW's coverage, a state-year whose war status was *cannot be read* only because the state's own losses
  are unseen reads **no** where UCDP/PRIO's Armed Conflict Dataset v26.1 lists the state as party to no conflict
  of cumulative intensity 1 that year. W12 never makes a *yes*.
- The third build's reading is the variant **`war-before-w12`**. Its file equals the third build's `series.csv`
  line for line, except for the `variant` column, which was checked. `war-moves.csv` lists every line and war
  field that moved: in the fifth build 420 rows, 144 at entry and 276 in the H years (the fourth's 421 and 145 held
  Tonga 2011's entry row, which no longer moves).
- Nothing else changed: the same 832 entries, routes, measures and spells.
The fifth build's figures come first in "Uncertainty". The third build's description follows as it was written.

**This is frame c's third build** (2026-10-01). It differs from the second (dcdea0c) by three readings, each
coded and tested before it ran, and by nothing else:
- the **currency boards** (c7 (i)): a lagged class 2 from 1971 now reads the boards list `ft001-boards`
  (16e0a57, under its own coders' protocol `FT-001-M3-boards.md`, 6b709f4) through `strain.board_at` (code
  cf380fc, committed before the list);
- **N1** of the narrow re-check (`bank/checks/FT-001-M3-panel-frame-c-2026-09-30-opus-recheck.md`): "during a
  break" reads *cannot be read* where frame b cannot date a restoration the readings show
  (`breaks.restoration_undatable`, 7c1e5d1);
- **N3**: claim 2's smallest detectable effect leaves out the lines whose default cannot be read (7c1e5d1).
The rest of this manifest describes the third build; where a sentence speaks of "this build" it is the third,
and the second build's description follows as it was written.

**The second build** (2026-09-30). The first (committed in b2a34a8) was audited deep and
isolated (`bank/checks/FT-001-M3-panel-frame-c-2026-09-30-opus-audit.md`: not yet, B1); the answers were
written into the protocol first (section 8, d164fa9), then coded and tested, the code committed before this
build. **Code commits**: 58bb80d (the readers and rules, before frame b's second build), 8997785 (P23 and
the anomaly screens; committed after the first build had run), **dba97b1** (section 8: R26 amended and
completed, R14 restored, R30 narrowed, M7, "convertible" from frame a, the smallest detectable effect) and
**78ab4b3** (panel 2's end at the first of Bernanke and James's three dates, M4 section 13), both committed
before this build. **Builds read**: the acts list's third build **a8780e1** (its H1 lines and coverage, for
*habit*); frame b's second build **b2a34a8** (`ft001-b`, unchanged since); frame a's second build **4510971**
(`ft001-a`, its manifest fixed in 9173abf; only `members.csv` and `series.csv` read). The list follows the
acts list, as the twin's `case_line.follows` declares; that it follows frame b (whose lines it reads) and
frame a is the build's order, not the twin's (the audit's M8), said.

## Claim 2's smallest detectable effect, printed before any count (O2; M0 v4.1's duty)

*Fifth build* (W12 and W13):
- the headline count gives 101 / 2 lines a side, in 2 strata with both sides (16 / 2 matched), and **91.7 points**;
- without pegs and boards: 66 / 24, 8 strata (40 / 24), **32.4 points**;
- without "taken back": 95 / 2, 2 strata (16 / 2), **91.7 points**.

**The reading without pegs and boards now has 24 lines on its fewer side, above M0's floor of 20.** Its smallest
detectable effect, 32.4 points, is still above M0's margin of 10. The other two readings stay below the floor. The
third build's figures follow.

Claim 2's headline comparison — the Mantel–Haenszel difference in share held between "two or more" and
"one or none" supports, matched on route, tercile, era and the state in default, over counted spells from
1970 — at 80% power and 5% one-sided, with a share of 0.6 in every stratum (M0's floor figure) and no
outcome read (`strain.claim2_mde`, the normal approximation over the strata where both sides are present):

| Reading of the count | Lines per side (two or more / one or none) | Strata with both sides (lines matched) | Smallest detectable effect |
|---|---|---|---|
| The headline count | 70 / 1 | 1 (3 / 1) | **140.7 points** — no effect can be detected: too thin by construction |
| Without pegs and boards (the cap alone) | 43 / 16 | 7 (22 / 16) | **43.1 points** |
| Without "taken back" | 65 / 1 | 1 (3 / 1) | **140.7 points** |

*Third build* (N3): lines whose default cannot be read are in no stratum. The second build counted them as a
stratum of their own: 69 / 1 at 140.7, 45 / 14 at 44.6, 64 / 8 at 73.5. Without "taken back", the fall from
73.5 to 140.7 is N3's doing: the stratum the second build matched was the unreadable default's.

M0's margin is 10 points and its floor 20 lines a side; every reading is below the floor on its fewer side.
Why (the audit's O2): "a limit by institution" reads only "yes" or *cannot be read* until frame a's targets
exist, and "taken back" is exactly "not in default", so in the stratum not in default nobody can be on the
fewer side; the comparison can live only among states in default. Whether it should is for M0's next
version.

## Sources

All at vintage 2026-09-30, each item read in M0's order (the twin's `common.source_order`), the first source
that reads a year giving its reading, never filled, scaled or spliced:

- **Debt / GDP** (route c1): the IMF's HPDD through DBnomics (`dbnomics/IMF/HPDD/A~~GGXWDG_GDP`, to 2015); the
  WEO of April 2025 (`dbnomics/IMF/WEO_2025-04/~GGXWDG_NGDP~pcent_gdp`, 1980–2024 read, never its
  projections); Reinhart and Rogoff's debt files (`reinhart-rogoff/debt-to-gdp-{A-E,F-M,M-S,T-Z}`, by R8's
  column rule, read by `missions/code/xls.py`); Jordà–Schularick–Taylor R6's `debtgdp` (× 100, see
  Assumptions).
- **Deficit / GDP** (c2, c3): the WEO's `~GGXCNL_NGDP~pcent_gdp` (the deficit is minus net lending; general
  government); JST's 100 (`expenditure` − `revenue`) / `gdp` (central government).
- **Central-bank credit to the state** (c3): IFS `A~~12A___XDC` to 2000 (and 2001, flagged), IFS `A~~FASAG_XDC`
  from 2002 (R9); GDP in national currency, IFS `A~~NGDP_XDC` then the World Bank's `NY.GDP.MKTP.CN` (R10).
- **Route c4**: the pilot's run `studies/FT-001-part-2-where-printed-money-goes/results/runs/C15-e-episodes-closed.json`
  (read, never edited; its only commit fccce91; its `card_hash` checked equal to M0's
  `reused_from_pilot.c4_card.card_hash`, and the file unchanged since fccce91, before the build):
  `result.lists.headline`, and `result.lists.smoothing` for its variant.
- **π and frame b's breaks**: `ft001-b`'s second build (b2a34a8; `series.csv` and each `variant-*.csv`), and the panel's π
  readings (`panel.py`, as frame b reads them) for "already inflating" and "π readable".
- **The regime and the split**: Ilzetzki–Reinhart–Rogoff's fine classes and unified-market dummies, as frame b.
- **The state in default** (R23): the Bank of Canada–Bank of England Sovereign Default Database 2025
  (`Debt_2025`) from 1960, per creditor class, as the acts list's builds read it; before 1960, Reinhart and
  Rogoff's *Varieties* (domestic and external columns) and, for the M–S economies, TTID's external dummies.
- **War years**: M4's `war.py` (7871641; W11, a dependency at war through its metropole, e861121), the
  workshop's one reader of M0's war year (COW's inter-, intra- and extra-state files; the World Bank's
  `VC.BTL.DETH` from 1989), readings W1–W11 in its docstring.
- **"Convertible" before 1971**: frame a's second build (`data/reconstructed/ft001-a/`, 4510971):
  `members.csv` (panels 1 and 2, members coded "yes"; the adoption year of panel 1 from its reason — the last
  of Meissner's years, or the United Kingdom's "from 1821 to 1914" —, panel 2's return from its reason, a span
  read at its later date) and `series.csv` (panel 1's `a1` change; panel 2's `bj_suspension`,
  `bj_exchange_control` and `bj_devaluation` on its `a2` and `a2-var-bj-note7` lines). Nothing else there is
  read.
- **The euro's changeovers** (c9): frame a's `EURO_ENTRY` (the European Central Bank's "Our money" page,
  frozen; 1074f44), imported by `strain.py`, never copied.
- **Supports**: Garriga (2025) `lvau_garriga` and `cuk_limlen` (`garriga/cbi`); Chinn–Ito's `ka_open`
  (`chinn-ito/kaopen`, `kaopen_2023.dta`); the acts list's H1 lines (a8780e1).
- **The currency boards** (c7 (i), third build): `data/reconstructed/ft001-boards/` (16e0a57), its
  `series.csv` only, read by `strain.board_at` at 31 December of the year before entry (B5).
- Codes: `missions/code/economies.py`.

## Steps

1. Frame c's readers and rules written in `panel.py` and `strain.py`, with synthetic tests in `test_panel.py`,
   **green before any real series was read for frame c**; then the readers' coverage printed (counts only).
2. A pre-audit build (never committed) was run and seen; the session's decisions on it were coded (8997785).
3. Frame c's first build (b2a34a8) on frame b's second build; its deep audit (not yet, B1).
4. The answers written as the protocol's section 8 (d164fa9); coded with one synthetic test per fix (dba97b1);
   panel 2's end amended after frame a's second build (M4 section 13, de3fe65; code 78ab4b3). Tests at this
   build: 152 passed over the code folder (`test_panel.py` 65, `test_m0.py`, `test_frame_a.py`).
5. `strain.py build`: per money and year from 1800 to the annual common end, **2025**, the routes' readings
   (c1–c4), the entries and spells (H = 10 headline), the flags, the entry measure and terciles, the era, the
   state in default, the supports, the regime and split, the five apart tests, the outcome over H, the
   competing exit (c9), censoring (c10); then each variant (`variant-*.csv`, 33) with the same machinery; the
   smallest detectable effect (above) computed and printed first in the build's report.
6. The panel of frame c (debt, deficit and c3 readings) is not committed (R28); its digest, SHA-256 of its
   sorted readings, unchanged from the first build: `ebbdfe912b30091b27a971f28476cac990280334c41765177cca21339bd26cc9`.
   Readings by item and source: debt HPDD 9,602, WEO 1,924, Reinhart–Rogoff 1,769, JST 36; deficit WEO 6,403,
   JST 1,852; c3 measures on 12A 1,302, on FASAG 2,042, and 1,076 years whose deficit is not positive.
7. `m0.py list_problems` on `series.csv` and all 33 variants: no problem; `ft.data.reconstructed.problems
   ("ft001-c")`: empty.
8. **The third build** (2026-10-01): the boards list coded and committed (6b709f4, 16e0a57); `board_at` and N1/N3
   coded with synthetic tests (cf380fc, 7c1e5d1; 215 passed over the code folder); `strain.py build` rerun on
   the same frozen inputs and the same lists (frame b b2a34a8, frame a 4510971, the acts a8780e1), plus
   `ft001-boards`. The panel's digest is unchanged. `m0.py list_problems` on `series.csv` and the 34 variants
   (`boards-with-comments` added): no problem. Its order check reads first commits only, so that this build
   follows `ft001-boards` rests on the commit order: said. `ft.data.reconstructed.problems("ft001-c")`:
   empty.

## Assumptions

- **The protocol's readings used here**: R1, R2, R4, R8–R10, R12–R14 (R14 through `war.py`), R19–R27, R29, R30,
  and section 8's amendments.
- **Readings made in code before any real series was read for frame c** (tested on synthetic readings):
  - *The status order*: an apart reason read "yes" makes the line *apart*; else a spell past the common end is
    *censored* whatever happened (R27), and one a competing exit ends is *ended unbroken*; else an apart
    reason that cannot be read makes the line *cannot be read* (the entry may not be an entrant); else the
    outcome's own status (c8).
  - *Every frame b line is a crossing* for the outcome and R26, counted or apart (frame b's audit's M7).
  - *c4's readability* is not known per year, so c4 enters neither `met_at_record_start` nor
    `route_unreadable_before`.
  - *c3 with a deficit not positive*: the measure is not defined; the route is read as not met that year.
  - *Convertible at entry from 1971* (R25): an annual entry in 1971 is read at its last day, so after 16 August
    1971 (as R22); an unreadable class *cannot be read*, any class but 2 "no". **Third build**: a lagged class
    2 is "yes" when a board of `ft001-boards` (B1) is in force on 31 December of the year before entry, "no"
    otherwise, and *cannot be read* only where a board's dates cannot be read (none). Past the chronologies'
    end, October 2016's board is carried, flagged `board_carried`. Month- and year-precision ends run through
    their month or year (B3, read in code). `boards-with-comments` adds B2's one line (Trinidad and Tobago,
    1935–64), which touches no entry from 1971: the variant equals the headline.
  - *During a break, N1* (third build): where the money's latest crossing is unrestored by frame b, and the
    readings below the lower line add up to 24 months before the entry year once unreadable periods are passed
    over (`breaks.restoration_undatable`: the months are quarterly), "during a break" is *cannot be read*,
    flagged `restoration_undatable`.
  - *Supports* at the entry year's own value (Garriga, Chinn–Ito); *a limit by institution* below 0.5 or unread
    *cannot be read* (targets are frame a's list); the count's grid (the cap at 0.25 / 0.75, the index at 0.4 /
    0.6, `ka_open` at 0.1 / 0.5) written as columns. *Habit* (a variant): "yes" when no H1 act before the entry
    and the year before it lies in the chronologies' span, "no" with one, else *cannot be read*. *World
    demand*: *cannot be read* (COFER is not frozen).
  - *π readable in a year* (for "held"): an annual reading or any monthly one.
  - *Terciles*: the 1/3 and 2/3 quantiles by linear interpolation; a measure equal to a cut-point goes below.
  - *A line not counted* keeps its outcome, dates and onset empty; what happened is in `so_far`.
  - *Reinhart–Rogoff's debt*: per year, the leftmost column R8 prefers that reads the year; the sheets of
    Guatemala, the Netherlands, Tunisia and Taiwan have no column R8 reads.
  - *C15's O1 lines* (the nine "likely reclassification, unread", and Côte d'Ivoire's episodes with a seam in
    their window crossing from 2001-10 to 2002-12) enter flagged `c4_flag`.
  - *`war_years_in_H`*: the war years from entry + 1 to entry + H, the unreadable ones counted beside.
  - *Chinn–Ito's* old codes ZAR and TMP read as COD and TLS (seen in its structure, before any value).
- **Readings chosen after the pre-audit build was seen** (said as such, each approved by the session):
  JST's `debtgdp` read × 100 (after its aggregate median, 0.45, was printed); the units check (R10) on each
  credit line alone (the pre-audit build ran it across the 2000–2001 seam); `ifs_break` read where frame b
  writes "yes" (a code error corrected); war years through `war.py`; the euro's changeovers from `EURO_ENTRY`
  (c9: a member's years from its entry are no entries; a spell reaching the changeover before the common end
  ends there — a crossing before it is the outcome, none with π readable every year before it is *ended
  unbroken*, otherwise *cannot be read*; the euro's unilateral users read as their own economies, flagged by
  R1); the state in default **per creditor class, `UNASSIGNED` and `FISCAL_ARREARS` included** (section 8,
  c5 kept), `DEBT_TOTAL_2025` > 0 beside and the variant `default-total` — **they disagree on 25 headline
  entries** (per class "yes", total "no", 0 of them counted in this build): the database's `FISCAL_ARREARS`
  is not part of its `DEBT_TOTAL`; a claim 2 verdict that turns on either is "we cannot conclude".
- **Section 8's readings (d164fa9), each coded and tested before this build (dba97b1, 78ab4b3)**:
  - **R26 amended (B1)**: a later break whose bound (crossing − 36 months; − 3 years annually; the bound of
    the frame b list read: 24 and 60 under `b-bound-24` and `b-bound-60`) falls in a year after the entry
    reads "no", whatever its onset reading; inside the bound a readable onset decides, an unreadable one gives
    "yes" when the π-only onset (not at the bound) is on or before the entry, else *cannot be read*, flagged
    `past_onset_residual`. **The producer's refinement of frame b's O1**, kept: a π-only onset at the bound
    never gives "yes".
  - **R26 completed (O1)**: an entry whose money's latest crossing before the entry year is not restored
    before that year begins is *apart*, "during a break" — a restoration dated inside the entry year leaves it
    apart; every frame b line counts, apart ones included.
  - **R14 restored (O3)**: a war year that *cannot be read* at entry makes the line *cannot be read*, flagged
    `war_unreadable_at_entry`; M4's P23 (read as no war) is the variant `war-unreadable-as-no`. The first
    build's variant `drop-war-unreadable-at-entry` is gone (it could no longer move a counted line).
  - **R30 narrowed (M1)**: `route_unreadable_before` tests c3 only where c3's deficit floor lies below c2's
    line — never in the headline, from 1949 in `c2-5`.
  - **M7**: under frame b's `lower-5` and `lower-15`, "already inflating" reads that variant's lower line.
  - **"Convertible" before 1971 (O4; M4 section 13)**, `strain.convertible_before_1971`: "yes" for a panel 1
    member from its adoption year to the year before its 1914–15 change, and for a panel 2 member from its
    return year to the year before its end; a member with no change, to its panel's last coded year (1915,
    1936). **Panel 2's end is the first of Bernanke and James's three dates** (suspension, exchange control,
    devaluation), from its `a2` and `a2-var-bj-note7` lines whichever carries it (an exchange control ends
    redemption on demand, M0 section 1; frame a's own headline exit, the first of suspension and devaluation,
    answers another question). **Boundaries** (an annual entry is read at its year's last day, as R22): the
    start year itself is "yes"; the change or end year itself is "no" when a suspension or an exchange control
    is dated in it, *cannot be read* when only a devaluation is; a year-precision date is read as its year.
    **1937–1970 is *cannot be read* whatever** (M4 section 10.7), and so is every other year and money. USA
    and Japan have no panel 1 change and read "yes" to 1915.
- **Said, no rule changed** (section 8):
  - **M2** — c3 cannot enter the headline: its deficit floor (3%) is c2's line and c2 wins ties, so a year
    that meets c3 meets c2. c3 is met in 44 entries' `routes_met`; `c3-25` and `c3-75` equal the headline line
    for line; **c3 enters only in `c2-5`** (c2 at 5%), where it has its own terciles. Claim 5 has no c3
    entrant in the headline. For M0's next version.
  - **M3** — c4's entry measure is the overshoot of C15's own threshold (entry measures: minimum 5.01, median
    5.47, third quartile 6.30% of GDP), so its tercile carries little strain information; claim 2's c4 strata
    are weak on it.
  - **M9** — claim 2 is "from 1970", but every 1970 entry reads "convertible: cannot be read" (7 entries): in
    practice it starts in 1971.
  - **M10** — the euro area (EMU) can never be counted: it has no IRR class and its state in default cannot
    be read (its one entry is *cannot be read*). Frame i should know.
  - **M6** — the euro's "announced 12 months before" is read as met (the ECB page gives years only; the
    Council's decisions are not frozen): the 10 *ended unbroken* lines carry `euro_announcement_read_met`, to
    be read both ways by the claims.
- **Not coded, said**: the new-money rule (`new_money_rule: not applied`); other competing exits than the
  euro's; the premium; COFER. (IRR's class-2 hard pegs are read through the boards list since the third build.)
- **N2 of the narrow re-check, said** (the frame a / frame c tension over the 1930s controls): frame c's
  "convertible" ends at the first of Bernanke and James's three dates, an exchange control included, because
  an exchange control ends redemption on demand (M0 section 1). Frame a's headline exit is the first of
  suspension and devaluation (M4 section 13, P12). The two frames answer different questions: a state (can a
  holder redeem?) and an act (did the state leave gold?). Claim 5's pre-1946 check is told with this.

## Uncertainty

**The fifth build (2026-10-02, W12 and W13)**:
- **The headline (H = 10)**: **832 lines** in 194 monies. **168 counted** (146 held, 13 broke, 9 broke and
  restored) in 105 monies; **371 apart**; **184 cannot be read**; **99 censored**; **10 ended unbroken**.
- **By route** (counted / apart / cannot be read / censored / ended unbroken):
  - c1: 35 / 107 / 89 / 16 / 2;
  - c2: 99 / 174 / 73 / 79 / 8;
  - c4: 34 / 90 / 22 / 4 / 0.
- **What moved against the third build, and why**: 45 statuses, all *cannot be read → counted*, all entries from
  2008 to 2015 whose war year at entry W12 reads *no*.
  - Their outcomes: held 42; broke 3 (Haiti 2013, Lebanon 2012, Syria 2010).
  - No status moved in any other direction.
  - Tonga 2011 moved in the fourth build and moved back in the fifth (W13).
  - `war_unreadable_at_entry` falls from 315 to 171.
- **Cannot be read, by reason** (184; a line can carry several): convertible at entry 92 (alone 52), already
  inflating 72 (alone 41), a war year at entry 67 (alone 38).
  - Of the 171 lines whose war year at entry is still *cannot be read*, 108 are from 2008 (Tonga 2011 is the 108th). There UCDP lists
    the state as a party to a conflict whose deaths had passed 1,000 by that year, and **most of them as a secondary
    supporter**: a contributor to a UN or regional mission, or an ally.
  - The rest: 41 have no COW state (31 before 2008, and ABW, EMU, HKG, MAC, PRI and PSE after); 19, before 2008,
    have COW's own losses unknown (inter-state wars with combat by region only, intra-state wars with unknown own
    losses); and 3 have a World Bank gap (Taiwan 1989, 2000 and 2010). 108 + 41 + 19 + 3 = 171.
- **Counted outcomes by route**: c1 held 26, broke 5, broke and restored 4; c2 91, 3, 5; c4 29, 5, 0.
- **The variants** (counted lines; on the headline's 832 lines unless a line count is given):
  - `war-before-w12` 123 (the third build);
  - `war-after-cow-no` 195; `war-unreadable-as-no` 204 (its statuses are the fourth build's; only its war text
    columns changed);
  - H5 347 (1,365 lines); H20 64 (521); c1 at 60: 189 (935); c2 at 5: 147 (737); `entry-year-counted` 184;
  - the flag drops: `met_at_record_start` 167 (795 lines), `entry_at_seam` 166 (822), `route_unreadable_before` 141
    (535), `c4_flag` 165 (828), `c1_outside_fit` 144 (719), `era_boundary_year` 167 (824), `ifs_break` 163 (821);
  - `regime-carried-out` 168 (719 lines, 16 censored); `c4-smoothing` 167 (816);
  - frame b's variants: `b-crossing-1-month` 166, `b-ifs-break-unreadable` 164, `b-line-40` 180, `b-line-100` 183,
    `b-lower-15` 220, `b-lower-5` 90, `b-rr-cpi-only` 167, the other eight 168;
  - `boards-with-comments`, `default-total`, `c3-25` and `c3-75` 168.
- **What was seen for the fifth build**: the counts and the moved lines' names. No measure was read line by line.
- **Downstream**: `ft001-phases` reads this list (`phases.py`), and is rebuilt on it.
- The third build's text below is kept as written then, and its figures are the third build's ("the counted list
  runs 1970–2007" and the like are no longer true).


**The third build (2026-10-01)**:
- **The headline (H = 10)**: **832 lines** in 194 monies, entries 1800–2024. **123 counted** (104 held, 10
  broke, 9 broke and restored) in 92 monies; **371 apart**; **229 cannot be read**; **99 censored**; **10 ended
  unbroken** (the same ten as below). Counted by era: fiat 122, gold exchange and Bretton Woods 1 (Greece 1931).
- **By route** (counted / apart / cannot be read / censored / ended unbroken):
  - c1 249: 29 / 107 / 95 / 16 / 2;
  - c2 433: 66 / 174 / 106 / 79 / 8;
  - c4 150: 28 / 90 / 28 / 4 / 0;
  - c3 0.
  Counted outcomes: c1 held 21, broke 4, broke and restored 4; c2 held 60, broke 1, broke and restored 5; c4
  held 23, broke 5.
- **What moved against the second build (dcdea0c), and why**: the same 832 entries; 26 statuses moved.

  | Second build → third | Lines | Why |
  |---|---|---|
  | cannot be read → counted | 12 | a class 2 with no board in force: "convertible" reads "no" (ARE 2001, BHR 1990 and 2002, BHS 1978, BLZ 1999, BRB 2002, BTN 2002, CPV 2001, JOR 1985, MDV 2005, NZL 1973, QAT 1993) |
  | cannot be read → apart | 8 | a board in force: "convertible" reads "yes" (ARG 1999, BGR 2003 and 2014, BIH 1999 and 2009, HKG 2001 and 2012, MAC 2012) |
  | censored → apart | 4 | a board in force (BGR 2024, BIH 2020, HKG 2022, MAC 2022; an apart "yes" comes before censoring) |
  | apart → cannot be read | 2 | N1: Sweden 1933 and 1943, "during a break" now *cannot be read* (frame b leaves Sweden unrestored 1917–1957-05 for want of consecutive months) |

  All 120 class-2 entries from 1971 are now read (24 "yes" or "no" moved a status above; 96 changed their
  "convertible" reading without a status change, another apart reason or censoring deciding). Suriname 2023 is
  among them, and its "during a break" also became *cannot be read* (N1); it stays apart for another reason.
  Counted: 111 → 123; apart 361 → 371; cannot be read 247 → 229; censored 103 → 99.
- **Apart, by reason** (371; a line can carry several): already inflating 268 (alone 71); during a break 192
  (alone 32; 156 with already inflating); a war year at entry 69 (alone 32); convertible at entry 39 (alone
  32); past frame b's onset 34 (alone 1).
- **Cannot be read, by reason** (229; each turns on an apart test): a war year at entry 116 (alone 84);
  convertible at entry 92 (alone 51); already inflating 72 (alone 41); past frame b's onset 10; during a
  break 2.
- **"Convertible" from 1971** (669 entries): no 633, yes 16, cannot be read 20 (no IRR class). The 16 "yes":
  Argentina 1999, Bulgaria 2003, 2014 and 2024, Bosnia 1999, 2009 and 2020, Estonia 1999 and 2009, Gambia
  1977, Hong Kong 2001, 2012 and 2022, Lithuania 1995, Macao 2012 and 2022. Before 1971, unchanged: 23 yes,
  3 no, 137 *cannot be read*.
- **Flags** (headline): `war_unreadable_at_entry` 315; `route_unreadable_before` 297; `c1_outside_fit` 113;
  `regime_carried` 113; `outcome_unreadable` 67 (53 *cannot be read*, 14 apart); `met_at_record_start` 37;
  `past_onset_residual` 22; **`board_carried` 19**; `ifs_break` 11; `entry_at_seam` 10;
  `euro_announcement_read_met` 10; `era_boundary_year` 8; `c4_flag` 4; **`restoration_undatable` 3**.
- **The state in default at entry**: yes 424, no 213, cannot be read 195 (counted: yes 62, no 21, cannot be
  read 40). Supports' count on counted lines: two or more 75, one or none 1, cannot be read 47 (without pegs
  47 / 16 / 60; without "taken back" 70 / 8 / 45). 68 counted lines have a war year inside H that cannot be
  read.
- **The variants** (lines; counted / apart / cannot be read / censored / ended unbroken):
  - H5 1,365 (211 / 625 / 466 / 54 / 9); H20 521 (64 / 228 / 104 / 114 / 11).
  - c1 at 60: 935 (139 / 407 / 281 / 96 / 12); c2 at 5: 737 (111 / 325 / 197 / 92 / 12); c3 at 25 and 75: the
    headline.
  - `entry-year-counted` 832 (135 / 341 / 241 / 104 / 11).
  - Flags dropped (lines, counted): `met_at_record_start` 795, 122; `entry_at_seam` 822, 121;
    `route_unreadable_before` 535, 96; `c4_flag` 828, 120; `c1_outside_fit` 719, 105; `era_boundary_year`
    824, 122; `ifs_break` 821, 118.
  - `regime-carried-out` 719 (123 / 341 / 229 / 16 / 10); `c4-smoothing` 816 (121 counted).
  - **War**: `war-unreadable-as-no` 832 (204 / 371 / 148 / 99 / 10); `war-after-cow-no` 832 (195 / 371 / 157 /
    99 / 10).
  - `default-total` and `boards-with-comments`: the headline's statuses.
  - Frame b's variants carried through (`b-*`, 15): counted 123 in most; `b-crossing-1-month` 122,
    `b-ifs-break-unreadable` 119, `b-line-40` 131, `b-line-100` 134, `b-lower-15` 155, `b-lower-5` 67,
    `b-rr-cpi-only` 122.
- **What was seen for the third build**: the boards coders' reports and lists (dates and labels), this build's
  counts, the moved lines named above, and the flagged lines' names. No measure or outcome was read line by
  line.

**The second build's figures (dcdea0c), as written then:**

- **The headline (H = 10)**: **832 lines** in 194 monies, entries 1800–2024 — **111 counted** (93 held, 10
  broke, 8 broke and restored) in 83 monies, **361 apart**, **247 cannot be read**, **103 censored**, **10
  ended unbroken** (the euro: Belgium 1993, Germany 1991, Spain 1992, Finland 1992, France 1996, Italy 1998,
  the Netherlands 1990, Portugal 1995 — changeover 1999 —; Malta 2000 — 2008 —; Slovakia 2006 — 2009).
  Counted by era: fiat 110, gold exchange and Bretton Woods 1 (Greece 1931).
- **By route** (lines; counted / apart / cannot be read / censored / ended unbroken): c1 249 (29 / 107 / 95 /
  16 / 2); c2 433 (57 / 168 / 117 / 83 / 8); c4 150 (25 / 86 / 35 / 4 / 0); **c3 0** (M2). Counted outcomes:
  c1 held 21, broke 4, broke and restored 4; c2 held 52, broke 1, broke and restored 4; c4 held 20, broke 5.
- **What moved against the first build (b2a34a8), and why** — the same 832 entries (routes, measures and
  spells unchanged); 125 statuses moved:

  | First build → rebuild | Lines | Why |
  |---|---|---|
  | counted → cannot be read | 67 | R14 restored: the war year at entry cannot be read (the first build read it as no war, P23) |
  | counted → apart | 20 | R26 completed: "during a break" (11 alone, 9 also with the war year unreadable) — among them NGA 1986, DZA 1984 and SDN 2005, which read "held" while π was far above the line |
  | cannot be read → apart | 32 | "convertible" read "yes" from frame a (17 with R26 amended, 3 alone), "during a break" (8, and 2 with R26 amended), and two war years now read "yes" through `war.py`'s W11 (e861121: a dependency at war through its metropole): Canada 1915, South Africa 1914 |
  | censored → apart | 5 | "during a break" |
  | cannot be read → counted | 1 | Greece 1931: R26 amended (its later break's bound is after the entry) and "convertible" read "no" (panel 2's end at its 1931 exchange control) |

  Counted: 197 → 111 (c1 43 → 29, c2 118 → 57, c4 36 → 25); apart 304 → 361; cannot be read 213 → 247;
  censored 108 → 103; ended unbroken 10 → 10. The audit's two B1 lines: Latvia 1999 is now *apart* ("during a
  break"), Palestine 2009 *cannot be read* (its war year; under `war-unreadable-as-no` it is counted).
- **Apart, by reason** (361; a line can carry several): already inflating 268 (alone 71); during a break 195
  (alone 35; 136 with already inflating); a war year at entry 69 (alone 32); past frame b's onset 34 (alone
  1); convertible at entry 23 (alone 20).
- **Cannot be read, by reason** (247; every one turns on an apart test): convertible at entry 146 (alone 65);
  a war year at entry 121 (alone 68); already inflating 73 (alone 25); past frame b's onset 10.
- **"Convertible" before 1971**: of the 163 entries to 1970, 23 read "yes" (Australia, Belgium, Canada,
  Denmark, Finland, France, the United Kingdom, the Netherlands, Norway, the United States, as the panels
  date them), 3 "no" (France 1914, the United Kingdom 1914, Greece 1931) and 137 *cannot be read* — 44 in
  1937–1970 (M4 section 10.7) and 93 outside the two panels' members and spans. From 1971, 140 *cannot be
  read* (a class 2, or no class).
- **Lines read both ways** (the audit's M4–M6; the claims read each both ways and say whether a verdict turns
  on them):
  - `outcome_unreadable` (M4): **67** lines whose outcome cannot be read (π unreadable in a year of the
    horizon with no crossing): 54 *cannot be read*, 13 apart — none counted; "held" needs π every year,
    "broke" does not.
  - `past_onset_residual` (M5): **22** lines where R26 stays *cannot be read* inside a bound: 11 apart on
    another reason, 10 *cannot be read*, 1 censored — Belgium 1920, Canada 1915, Finland 1918, France 1924 and
    1934, the United Kingdom 1800, Georgia 1995, Guinea-Bissau 1986, Greece 1858, 1868 and 1888, Italy 1914,
    Japan 1941, Kyrgyzstan 1995, St Kitts and Nevis 1980, Laos 1989, Mongolia 1991, Russia 1992, São Tomé
    1995, Tajikistan 1998, Yemen 1990, Zimbabwe 2016.
  - `euro_announcement_read_met` (M6): the 10 *ended unbroken* lines.
  - Also carried: `war_unreadable_at_entry` on 315 lines (the variant `war-unreadable-as-no`: 179 counted);
    61 counted lines have a war year inside H that cannot be read (`war_years_in_H`).
- **Flags** (headline): `war_unreadable_at_entry` 315; `route_unreadable_before` 297 (c1 and c2 only, M1);
  `c1_outside_fit` 113; `regime_carried` 113; `outcome_unreadable` 67; `met_at_record_start` 37;
  `past_onset_residual` 22; `ifs_break` 11; `entry_at_seam` 10; `euro_announcement_read_met` 10;
  `era_boundary_year` 8; `c4_flag` 4.
- **The state in default at entry**: yes 424, no 213, cannot be read 195 (counted: yes 58, no 19, cannot be
  read 34). Supports' count on counted lines: two or more 69, one or none 1, cannot be read 41 (without pegs
  45 / 14 / 52; without "taken back" 64 / 8 / 39).
- **The units check (R10)** leaves c3 unreadable over the failing line's years for 40 monies (listed in the
  first build's manifest, unchanged: legacy-currency 12A series, redenominations, claims near zero).
- **Tercile cut-points** (over every entry line with a readable measure, whatever its status; unchanged from
  the first build, the entries being the same): c1 101.33 and 141.16 (% of GDP); c2 3.95 and 5.72; c4 5.30 and
  5.88. H5: c1 102.87 / 139.96, c2 3.98 / 5.93, c4 5.27 / 5.83. H20: c1 99.78 / 125.64, c2 3.98 / 5.89, c4 5.23
  / 5.88. c2-5: c1 101.14 / 137.91, c2 5.97 / 7.78, c3 63.16 / 80.12, c4 5.27 / 5.88. c1-60: c1 72.98 / 99.86,
  c2 3.79 / 5.52, c4 5.29 / 5.92.
- **The variants** (lines; counted / apart / cannot be read / censored / ended unbroken):
  - H5 1,365 (187 / 611 / 502 / 56 / 9); H20 521 (54 / 221 / 117 / 118 / 11).
  - c1 at 60: 935 (125 / 399 / 299 / 100 / 12); c2 at 5: 737 (98 / 314 / 218 / 95 / 12); c3 at 25 and 75: the
    headline.
  - `entry-year-counted`: 832 (121 / 331 / 261 / 108 / 11).
  - Flags dropped: `met_at_record_start` 795 (110 counted); `entry_at_seam` 822 (109);
    `route_unreadable_before` 535 (88); `c4_flag` 828 (108); `c1_outside_fit` 719 (93);
    `era_boundary_year` 824 (110); `ifs_break` 821 (107).
  - `regime-carried-out` 719 (111 / 335 / 247 / 16 / 10); `c4-smoothing` 816 (108 counted).
  - **War**: `war-unreadable-as-no` (P23) 832 (179 / 361 / 179 / 103 / 10); `war-after-cow-no` 832 (173 /
    361 / 185 / 103 / 10).
  - `default-total`: the headline's statuses (the state in default is no apart test; its columns differ on 25
    lines).
  - Frame b's variants carried through (`b-*`, 15): counted 111 in most; `b-crossing-1-month` 110,
    `b-ifs-break-unreadable` 107, `b-line-40` 119, `b-line-100` 121, `b-lower-15` 139, `b-lower-5` 57 ("already
    inflating" at 5%, M7), `b-rr-cpi-only` 110 (the audit's O2 carried through: claim 5 and every pre-1946
    verdict say whether they turn on it).
- **What was seen**: for the first build and before, as that build's manifest said (the readers' coverage
  counts, the Reinhart–Rogoff debt labels, the COW headers, C15's labels, the pre-audit build's counts and
  named monies, JST's aggregate median); since: the audit's report with its named lines and values, frame a's
  members and dates (its `members.csv` and `series.csv`, structure and dates), and this build's counts, moves
  and flagged lines as listed above. No line's measure or outcome was read one by one beyond those named.
