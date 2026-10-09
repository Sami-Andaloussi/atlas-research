"""FT-001 M4, second part: frame a's window build, ``ft001-a-window`` (FT-001-M4-frame-a.md, sections 6, 7, 13, 15, 16, 18 and 19).

Frame a's list (``data/reconstructed/ft001-a/``) dates the changes of a support; this module reads, **after that
list is committed**, what value and trust did around each change, and sets it beside what the same measures did
around its non-changers. It describes; it counts nothing and gives no verdict (A2). **It never edits frame a's
list.** Code only: nothing here has been run on a real series; the null band (:func:`null_band`) is run first,
on synthetic panels, and :func:`build_window` refuses to touch a reading before it has printed the band.

**The pool (section 13, P27 amended).** The non-changers of a change in year y are monies with **no change of the
same panel in y-3..y** (information at the change only). A comparator's own later change, up to y+5, or its entry
into the euro (W21), ends its path there (the change's year and after are not read), flagged. The as-written pool (none in y-3..y+3) is a
variant, ``pool="written"``. "The same panel" is every line of the panel's headline routes, whatever its status
(an apart line is a change all the same); panel 3: any reform, up or down. A panel's *coverage* decides who can
be in the pool at all: panels 1 and 2, the candidates whose membership the list reads (*cannot be read* is not
"no change"); panel 3, Garriga's country-years; panel 4, every money through 2022 (W5, section 19), less the three whose
adoption cannot be read (Finland, Spain, Slovakia: **a selection by their later, undated change**, dropped from every
pool even for a change years before their adoption; mild and needed, said: M7), less each candidate from 2012 whose
adoption cannot be read from two years before the first AREAER edition that lists it, and Paraguay and Uganda from 2011. **Unions** (W15, W21; sections 15 and
16): a member of ``XOF``, ``XAF``, ``XCD`` or the euro area takes its union's changes in "no change in y-3..y", and a
member **from its entry** is that union's money, never a comparator of its own, the three other unions as the euro (the
variants ``euro-members-as-own`` and ``union-members-as-own`` each keep the first build's reading for one of the two).

**The match (section 13, P28 amended; M0's caliper).** Up to 5 comparators, nearest on π(y-1) and on the change
in π from y-3 to y-1, **both within the caliper** (3 points [1; 5]). *Distance* (reading W1, below): the sum of
the two absolute gaps; the caliper holds on each. Ties are drawn, seed 1797 (W2). A comparator's reuse is
counted and written. A change with no comparator in the caliper is shown alone, said. P29: a money in a war year
in the change's year is no comparator; a comparator whose war year **cannot be read** stays, flagged, and the
variant ``war_unreadable="drop"`` drops it. Panel 2's comparators are named for what they are: earlier or later
leavers (members), not members, or members whose only change is an exchange control.

**The window.** Annual, -3..+5 around the change's year; monthly, -24..+36 around its month, where the change is
dated to the month and monthly data exist. *Value* (π, depreciation, the market split) and *trust* (deposits to
GDP, currency to deposits, reserves; dollarisation *not built*) are kept apart and come from M0's sources
through ``panel.py``'s readers (:class:`Readers`, :func:`panel_readers`); a measure with no reader is *not built*,
never guessed.

**The run rule (P24, P25), panels 1 and 2 only** (:func:`run_test`): reserves down 20% [10; 30] in the 12 months
before. Its source is *Banking and Monetary Statistics 1914-1941*'s table 160, frozen and parsed (W9,
:func:`bms_reserves_at`); without a reader the test is *cannot be read*.

**The null band (sections 13, 15 and 16)** (:func:`null_band`): the gap the described comparison gives under **no effect**,
on synthetic panels shaped like each real one, with the same :func:`pool` and :func:`match`; its scenarios now include a
hazard on the change year's own π and on its rise (W10); 1,000 runs (:data:`SCENARIO_RUNS`, W18, W24). Callable alone:
``python window_a.py null-band``. The **placebo band** (:func:`placebo_band`, W11, W19) is the second band: pseudo-changes
among the real non-changers, through the same pool and match, which needs no chosen price process; 10,000 draws, a headline
design and a stratified one printed beside it, and the variant ``future-clean``. Every band edge is printed with its
**standard error** from 20 batches (W24), and a mean within 2 of it is "at the edge", never inside or outside (W24).
Neither band is a verdict (M8: they cover π only).

**Readings chosen here, in the open, for the audit to judge** (W-numbers; the protocol's are P1-P29):

W1. *Distance* for ranking is the sum of |gap in π(y-1)| and |gap in the change in π|; a comparator must be
    within the caliper on each. (The max of the two would rank by the worse gap only.) The level-only match, P28
    as first written, is a variant (``on="level"``).
W2. *Ties* are drawn by a random key per candidate, from ``numpy``'s generator seeded by sha256 of ``"1797|" +
    the change's key`` (the reading's name and the line's key): a change's draw depends on its own key and on the
    order of its pool (money codes, sorted), never on another change.
W3. *A comparator's path* runs over y+1 .. the year before its own later change (the change's year is partly
    after the support gave way, so it is not read), or to the last year its panel's source covers. A comparator
    whose path is empty (a change in y+1) **stays matched and contributes nothing**: dropping it would choose
    comparators by their own future, which is what the audit's O1 objected to. ``skip_empty_paths=True`` is the
    audit simulation's behaviour, a variant.
W4. *The described gap* is [mean π over y+1..y+5 less π(y-1)] for the change, less the same for its matched
    comparators' mean (each over its own path); the change's own path stops before a competing exit's year.
W5. *Panel 4 covers every money through 2022* (section 19; the fourth build; the first three stopped it in 2011, when nothing
    after 2011 was read). AREAER's editions 2012-2023 list every money's framework at 30 April of each year and the
    candidates' announcements are read (sections 14 and 17), so :data:`PANEL4_LAST_COVERED` = 2022, the last full year the
    2023 edition closes. The members file's panel ``4-from-2012`` rows say who: **member yes or no** is covered through 2022 (its
    change, or its absence, is known); **a candidate whose adoption cannot be read** is covered only through **Y - 2**, Y the
    first edition that lists it (edition Y places the adoption between 30 April Y - 1 and 30 April Y, so Y - 2 is the last full
    year known untouched), and is uncovered after: never a non-changer there, never a change. Y is parsed from the row's reason
    ("first listed in the AREAER <Y>"; :func:`first_listing_year`) and a candidate whose Y cannot be read is refused, loudly.
    **Paraguay and Uganda** (:data:`PANEL4_UNCOVERED_FROM`) are uncovered from 2011: Paraguay's bank recounts an adoption of
    18 May 2011, and Uganda's announced one in July 2011 (section 21); Hammond's 27 hold neither and no line dates them: a gap of
    the pre-2012 list, said. The older panel ``4`` rows that cannot
    be read (Finland, Spain, Slovakia) stay uncovered throughout. **The reading** ``a4-later-or-transition-documents``
    (:data:`READINGS`) adds frame a's lines of route :data:`LATER_OR_TRANSITION_ROUTE` (Argentina 2016-12, Ukraine 2018-07-13,
    Kazakhstan 2015-04-24, Uzbekistan 2019, Uruguay 2016-06) to the headline's panel 4 lines: those five are covered through
    2022 there, with their dates as changes, and are "not yet targeting" before them in the at-risk variant. A window that runs
    past the panel's common end is censored as before. The at-risk variant (P27): an adopter from 2012 is "not yet targeting"
    before its date; a candidate that cannot be read is 2 (*cannot be read*) from Y - 1 on. *What no code holds*: that
    AREAER's column is complete for each edition (the two coders' kappa, section 14, is the check). A 2023 change (Mauritius)
    has its own year uncovered, so its pool is empty: it is shown alone, said.
W6. *Deposits* for the trust measures are the depository corporations survey's other and transferable deposits
    (IFS ``FDSBO`` + ``FDSBT``), mostly from 2001 (monthly from 1997-12); the same survey's ``FDSBC`` is currency.
    **Before a money's first survey reading**, IFS's old presentation gives them as published lines: the deposit
    money banks' demand deposits (line ``24``) plus their time, savings and foreign-currency deposits (``25``),
    with currency outside them (``14A``) — frozen 2026-10-01, read by default (``deposits_before="lines"``), and
    the seam to the survey flagged, never smoothed. *Deposits to GDP* switches at the deposits' own first survey
    reading; *currency to deposits* switches **both** tables at the **later** of their first survey readings (M6: the
    survey's currency begins before its deposits in 85 rows, and a ratio is within one presentation), and a seam in
    either table is reported, both (``_seam``). Where the two overlap (138 monies), the lines' sum is the survey's at a
    median ratio of 1.00, measured once before this rule was written. *Deposits to GDP* reads the old lines only
    where their units are checked (:func:`old_lines_units`): a euro member with no survey reading of its own (IFS
    moved it to the euro area's) has its lines in its legacy money, converted at the fixed rate (:data:`EURO_RATE`);
    where both read, the lines over the survey at their first common period lie within ``UNITS_BAND`` -- **measured
    only on the years where the two differ** (W14: identical values are the survey filling the lines, not a check, and
    the gap check applies instead); where the survey only starts after the lines end, deposits to GDP across the gap
    does; where no survey reads at all, the lines are read and their tag says the units are unchecked. A failed
    check (a redenomination at the seam) is *cannot be read*. *Currency to deposits* is a ratio within one
    presentation, so its units cancel. The identity broad money (``35L``) less currency (``14A``) is a variant
    (``deposits_before="identity"``, annual only, flagged *derived*); ``"none"`` reads the survey alone. Deposits to GDP is annual only (GDP is annual).
W7. *The 12 months before a run* are: for a change dated to the month, the level at the end of the month before
    against the level 12 months earlier; for a year-dated change, the end of y-1 against the end of y-2.
W9. *The run test's reserves* (P24, P25) are the Federal Reserve Board's table 160 (*Banking and Monetary
    Statistics 1914-1941*, frozen 2026-10-01, parsed by ``bms160.py``): central banks' and governments' gold
    reserves, read **at one footing, $20.67 an ounce** (the book's own to January 1934, restated after it), so
    that the dollar's revaluation of January 1934 is not read as a rise. The table is yearly (December) to 1927,
    monthly from June 1928: a 1914 change dated to the month has no reading 12 months before, so panel 1's run
    test is *cannot be read* (its lines stay counted, P25). A cell the parser flags (a repair, a failed Total
    row, a continuity spike) is read. **There is no strict variant** (section 15, O2): the window's deep audit
    page-checked about 50 of the cells the verdicts use against the page images (PDF pp. 543, 544, 546, 549-552;
    2026-10-01, ``bank/checks/FT-001-M4-window-2026-10-01-opus-audit.md``) and **found two wrong**: Italy 1936-09,
    repaired since by R7, and Estonia 1930-10, now **unreadable over 1929-01 to 1931-08** (``bms160`` R8, section 16, N3,
    from 1929-01 by section 18, P6: the image has 1.8 where the text reads .8, in a run no check sees; the column reads
    ``.7`` from 1929-01); **that page check, with its two errors, is the
    record**: not "found them right". The threshold's grid [10; 30] is built as the columns ``run_10`` and ``run_30`` of ``changes.csv``, beside
    the headline's 20%, and the manifest names the lines that move. **A departure from P25, named** (O3): P25 reads
    "the central bank's gold reserves (with its foreign exchange where the source gives it)"; table 160 gives gold, not
    foreign exchange. So a "no" is written ``no (gold only)`` and flagged ``gold_only`` (``run_flag``), never read as "no
    run"; the Bank of England's, the Bank of France's and the Reichsbank's foreign exchange (BMS tables 164, 165 and 167)
    are a need, built as a variant once parsed.
W8. *A variant reading's status* (panel 2 on Bernanke and James's note 7) is derived: apart for a war year or an
    exit before 1931, counted otherwise; the list marks all of its lines *apart* because they are variants.

Readings added after the first build's windows had been seen (section 15 of the protocol; each is said to have been
written after them, and none changes the list ``ft001-a``). **W18-W23 (section 16) were written after the first build's
(eca6369) and the second build's (a2bdaa6) windows had both been seen**; the manifest says so (N6):

W10. *The band at the described n, with same-year scenarios* (O1). The scenarios gain a hazard on π(y) and one on
    π(y) - π(y-1), each of both signs (:data:`SCENARIOS`): the match reads π(y-1) and the rise to y-1 and never π(y), so
    a timing tied to the change year's own π moves the null gap. :func:`null_band` keeps each run's gaps
    (``keep_gaps``) and :func:`band_at_n` draws, from the changes that found a gap, as many as a **description line**
    has (counted lines with a gap, the line's own n), so each line's band is at its n and not the list's. The first
    band (the list's counted n) is printed before any reader is made, as before; the described-n rows are computed
    after the counts are known (a count enters, no real value), carry the line's name, and are written beside it.
W11. *The placebo band* (O1, :func:`placebo_band`). Pseudo-changes are drawn at random among the money-years of the
    panel's real non-changers (no change of the panel, own or its union's, in y-3..y+5; the source covering them; π
    readable in y-3 and y-1; no war year in y; y within the span of the panel's real changes and y+5 inside the common
    end), through the same :func:`pool` and :func:`match` and the same :func:`described_gap`. A draw takes as many
    pseudo-changes as the description line has with a gap; 200 draws, seeded; written as its own rows
    (``placebo-band.csv``). It runs inside the build after the readers are made. It needs no chosen price process:
    **a mean inside the scenarios' band and the placebo bands is consistent with no effect; outside one it is not a
    finding**. *Eligibility, draws and seeds are amended by W18 and W19; the paragraph above is the first build's.*
W12. *The run threshold's grid* (O2): ``run_10`` and ``run_30`` beside ``run_test`` (20%) in ``changes.csv``; the
    status moves on the headline's 20% only, and the manifest names the lines whose verdict moves at 10% or 30%.
W13. *Gold only* (O3): a "no" from table 160 is ``no (gold only)``, flagged ``gold_only``; a "yes" stays "yes" (a gold
    outflow is a run, whatever else the bank held).
W14. *Units of deposits to GDP* (O4): a ratio outside 1-300% (:data:`GDP_RATIO_BAND`) is flagged ``units_suspect``;
    once a break is seen in a money's deposits to GDP (a factor of 100 or more, **or of 10 or more at a source seam**,
    W20), **every later year** is flagged; each seam's ratio is printed in the reading's ``note`` (the step across the
    seam in a level, and, where the readers give it, the old lines over the survey at their first differing year); the
    overlap's units check ignores years where the old lines and the survey are identical **to 1e-3** (W20: the survey
    filling the lines is no check) and falls to the gap check.
W15. *Unions in the pool* (O5): a member of ``XOF``, ``XAF``, ``XCD`` or the euro area takes its union's changes (the
    members named on the union's line in the list, as ``frame_a.py`` names them; for the euro area, ``EURO_ENTRY``'s
    members from their entry year) in the pool's "no change in y-3..y" and in the path's end; a euro member from its
    entry year is the euro and **never a comparator of its own**. *The first build read a comparator that would enter
    the euro within its window to the window's end; W21 ends its path at the entry. W21 also treats XOF, XAF and XCD
    members as the euro's, and splits the variant ``euro-members-as-own``.* The union lines are moved apart as "no
    union-level price series".
W16. *Statuses* (M2): a counted line whose only move is censoring takes M0's status ``censored``; any other move is
    ``apart`` with every reason written; no π in y-3 is "a gap in the price record" where the money has a reading in
    an earlier year (the record begins before y-3), and "before the price record" otherwise. *Amended by W22: "the
    money has a reading in an earlier year" is read over its whole price series, not the panel's table.*
W17. *The description* (M3, M8): the ended-unbroken lines are described "with and without" (the "counted, with ended
    unbroken" line); where the headline and note 7 disagree in sign, ``describe`` says "the order cannot be read" (W23
    adds their disagreements line by line). The
    bands and the described gap cover π only: depreciation, the market split and every trust measure have rows and no
    comparator summary and no band, said.

Readings added after the re-check of the second build (section 16 of the protocol; N1-N7 of
``bank/checks/FT-001-M4-window-second-build-2026-10-01-opus-recheck.md``), written after the first and second builds'
windows had been seen:

W18. *Draws, seeds and the edges' error* (N1). The placebo takes :data:`PLACEBO_DRAWS` = 10,000 draws, each description
    line's seeded by sha256 of (the seed, the design, the reading, the label and **n**) and never by the line's display name:
    two lines with the same changes get the same band. The scenarios' band took 300 runs (from 100): **1,000 since W24**.
    *The third build printed each edge with the absolute difference of that edge between the first and the second half of
    the draws (columns* ``lo_err`` *and* ``hi_err``*): one random draw, not a standard error (section 18, P2). W24 replaces
    it:* :func:`edge_se`, columns ``lo_se`` and ``hi_se``.
W19. *The placebo's design* (N2, :func:`placebo_cells`). **Headline**: a pseudo-change (money j, year y) is eligible by
    the pool's own past-only rule: no change of its panel, its union's included, in y-3..y, the source covering it over
    those years, π readable in y-3 and y-1, no war year in y, not in the euro or a union as that union's money (W21), y
    inside the span of the panel's real changes and y+5 inside the common end; its **path is cut** at its own later change
    (or its union's, or its entry into a union, or where its source stops covering it) and flagged, as a comparator's is
    (W3): the cell's gap is read over that shorter path, as a real change's is to its competing exit. **Stratified**,
    printed beside it: per draw, **one pseudo-change per real change** of the description line, drawn among the headline's
    eligible money-years within +-3 years of that real change (:data:`PLACEBO_STRATUM_YEARS`; the years may lie outside
    the span) and with π(y-1) within the caliper (3 points) of the real change's π(y-1), then matched as in the headline;
    the draws of different changes are independent (one cell may serve two changes); a real change with no cell in its
    stratum is left out and counted (``note``). **A stratum can hold the real changer's own earlier money-years** (years
    in which its money had no change in y-3..y), each cut at its change (the third build's re-check: 4 of the 7 cells of
    panel 2's smallest stratum, 106 cells in 3-up's) (section 18, P7). **Variant**
    ``future-clean`` (the name is the same in the protocol, the code and the files): the first build's rule (no change in
    y-3..y+5, covered through y+5, uniform over the span, the path to y+5 uncut). ``placebo-band.csv`` carries the
    ``design`` (headline, stratified, future-clean). **A difference of design, said** (section 18, P4): **a pseudo-change's
    path is cut at its own later change of the same panel; a real change's is not** (it is cut only at a competing exit), so
    a real line with a later reform of its own keeps its full path where a headline pseudo-change in the same position would
    not (in the third build's panel 3, 787 of 3,594 cells are cut, and a real counted line with a later reform keeps its
    path). The description line "counted, without overlapping lines" partly covers this, and :func:`describe` prints, beside
    the headline placebo, the share of cut cells and their mean gap (W25). **A placebo with fewer than** :data:`PLACEBO_MIN_CELLS` = 30 **cells cannot be
    read as a band** (the session's reading: below it the draws repeat the same few subsets; panel 1 has 7 cells for
    n = 4, 35 subsets): ``describe`` says so and does not place the mean against it.
W20. *Units of deposits to GDP, again* (N4). GDP's own seam: where IFS NGDP and the World Bank's GDP differ by more than
    a factor of :data:`GDP_SEAM_FACTOR` = 2 in **any** of their common years (*W26 reads the median ratio instead*;
    :func:`gdp_seam_message`), every year of the World Bank segment is flagged ``units_suspect`` (Liberia; **not Armenia**,
    which the third build's re-check showed this rule does not catch: IFS and the World Bank agree in their common years,
    and its x12.6 step in 1993 is a level step: W26). At a source seam, a units break is a factor of
    :data:`UNITS_BREAK_AT_SEAM` = 10 or more, a factor of :data:`UNITS_BREAK` = 100 or more elsewhere. An overlap where
    |lines / survey - 1| < :data:`IDENTICAL_TOL` = 1e-3 in every common year is **identical** (:func:`_differ`): the survey
    filling the lines, and the check is then made across the gap.
W21. *Unions alike* (N5, N7). A member of ``XOF``, ``XAF`` or ``XCD`` is, **from its entry** (:data:`UNION_SPAN`), that
    union's money and never a comparator of its own, as a euro member is from ``EURO_ENTRY`` (M0 section 1, A1: a union is
    one money); before its entry, or after its exit, it is its own money. The entry and exit years of the three unions'
    members were **the session's reading from the unions' histories** (Mali 1984, Guinea-Bissau 1997, Equatorial Guinea 1985;
    Mauritania until 1972; the other members throughout the record). **W28 (section 18, P8) cites the frozen source the
    four years match: Garriga's ``regional`` flag**; what stays a need is the XCD members' years (:data:`NEEDS`).
    A comparator's path ends, flagged, at its entry into the euro or a union within its window (``euro entry YYYY``,
    ``union entry YYYY``) as a change's competing exit ends its own; the monthly path the same. Variants:
    ``euro-members-as-own`` (the euro only reverted: its members are comparators of their own again, their later euro
    entry no end to their path) and ``union-members-as-own`` (the three other unions only reverted).
W22. *"Before the price record" reads the money's whole price series* (N7): :attr:`PanelData.pi_first` is the first year
    the money has a π anywhere (all its source's years, not the panel's table), so a money that has π before y-3 and none
    in y-3 is "a gap in the price record" (RUS 1990: π to 1910 and from 1993).
W23. *The description, again* (N7). The headline's and note 7's per-line disagreements (a money whose entry date or
    status differs between the two readings, or that has a line in one only: POL 1936; DEU and HUN) are printed line by
    line by ``describe``, with each reading's run verdict. A mean inside the scenarios' band and the placebo bands
    "is consistent with no effect" and never "told as no effect": the placebo assumes random timing and the scenarios a
    synthetic spread, and neither has both.

Readings added after the third build's re-check (section 18 of the protocol; P1-P9 of
``bank/checks/FT-001-M4-window-third-build-2026-10-01-opus-recheck.md``), written after the first, second **and third**
builds' windows had been seen:

W24. *Each edge's standard error, "at the edge", 1,000 runs* (P1, P2). The scenarios take :data:`SCENARIO_RUNS` = 1,000 runs
    (from 300). **Every band edge** (the scenarios', and the placebo's headline, stratified and ``future-clean``) **carries a
    standard error from** :data:`EDGE_BATCHES` = 20 **batches** (:func:`edge_se`): the 20 consecutive batches of the
    independent draws or runs each give the edge (2.5 and 97.5 per cent), and the error is the sd of those 20 edges over
    sqrt(20). It estimates the sd of the edge computed from all the draws; it replaces W18's half-against-half difference,
    which was one random draw (0.001 against a true 0.060 in one edge, 0.389 against 0.103 in another). The columns are
    ``lo_se`` and ``hi_se``; with fewer than 40 draws (two per batch) there is none. The scenarios' envelope takes the
    standard error of the scenario that gives the edge (:func:`envelope_se`); an envelope is the minimum of its scenarios'
    edges and, with few runs, biased outward: the 1,000 runs are what makes it stable (the re-check: panel 4's lower edge
    moved with the seed at 300 runs). :func:`describe` says **"at the edge of"** a band, never inside or outside it, where
    the mean lies within :data:`AT_EDGE_SE` = 2 standard errors of either of its edges (:func:`_place`); a band with no
    standard error is placed inside or outside as before.
W25. *Each description line places the mean on all three placebo designs* (P3, P7). The headline (past-only) placebo, the
    stratified one **and** ``future-clean`` (the name is the same in the protocol, the code and the files): the headline's
    sentence rests on a design chosen after the second build's window was seen, and the variant's placement may differ
    (panel 2 on the third build: outside the headline's band, inside the variant's, by the 12 cut cells, whose gaps average
    -3.84 against +1.16 for the 39 uncut). Beside the headline placebo the line gives **the share of cut cells among its
    pseudo-changes, their mean gap and the uncut ones'** (``cut``, ``cut_mean``, ``uncut_mean``). Each stratified band prints
    **its smallest stratum** (``min_stratum``: the fewest cells any real change's stratum holds), which can hold the real
    changer's own earlier money-years, each cut at its change (W19). The placebos' difference of design, a pseudo-change's path
    cut at its own later change and a real change's not, is said in W19 (P4).
W26. *Units of deposits to GDP, the remainder* (P5). **GDP's seam reads the median ratio** of the World Bank's GDP to IFS NGDP
    over their common years (:func:`gdp_seam_message`), not any single year: a money whose ratio is far from 1 in one year
    only (Suriname's 2014) is no longer flagged, and one far from 1 in most (Liberia's 0.0055 to 0.012) is. **Where the GDP
    seam names the World Bank segment, a units break at the seam is not carried into the IFS years** (Liberia's 2010-2022,
    about 15% of GDP, are IFS's, the right units: :meth:`Readers.read` drops the break when the break year or the year before
    it is in the flagged segment; the segment's own years keep ``units_suspect``, and the seam's ratio is still printed).
    **Armenia is not claimed**: IFS and the World Bank agree in their common years, its x12.6 step in 1993 is a level step,
    and its 1992 reading is read as clear. The manifest **splits the ``units_suspect`` count by reason** (outside 1-300%; GDP
    seam; both), as :func:`units_suspect_split` counts them.
W27. *Estonia's lost digit from 1929-01* (P6). ``bms160``'s R8 empties Estonia's $20.67 cells from **1929-01**, not 1929-10 to
    1931-08 only: the column reads ``.7`` from 1929-01 where the image has 1.7 (the step from 1.7 in 1928-12 is flagged), and
    the third build read 1929-01 to 1929-09 although the Total row fails there. No run test reads them either way.
W28. *The unions' years, their source* (P8). The four years of :data:`UNION_SPAN` (Mali 1984, Guinea-Bissau 1997, Equatorial
    Guinea 1985, Mauritania to 1972) are exactly what **Garriga's ``regional`` flag** gives (MLI 0 to 1983 then 1; GNB 1 from
    1997; GNQ 1 from 1985; MRT 1 to 1972, 0 from 1973), the frozen source ``frame_a`` already reads (a test reads it). It is
    **not** the source for the rest: the XCD members are the EC dollar's from 1965 (Grenada 1968) and her flag starts in 1983.
    **Barbados** (the EC dollar until 1973) is not in ``frame_a.UNIONS``; no headline match uses it before 1975, so nothing
    moves; said.
W29. *The manifest's descriptive notes* (P9). For each description line of the headline reading, the manifest says the median,
    the line that moves the mean most and the extreme line on the other side, how many comparators each rests on and the mean
    without each (3-up's -0.27 is +0.08 without ESP 1980, one comparator, gap -48.1, and -0.80 without BGR 1991, +70.6; its
    median is -0.54), and how many lines rest on a single comparator
    (:func:`robustness_notes`). "Comparators most reused" is the maximum **within one panel** (a comparator's reuse is counted
    per panel and variant), never across panels.

Run from the workshop's root with the toolkit's interpreter::

    PYTHONDONTWRITEBYTECODE=1 toolkit/bin/ftpy bank/maps/FT-001/missions/code/window_a.py null-band
"""

from __future__ import annotations

import csv
import hashlib
import math
import re
import subprocess
import sys
import zlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, NamedTuple

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from frame_a import EURO_ENTRY, UNION_OF, UNIONS  # noqa: E402  (the euro's entries and the unions' members, as the list reads them)

ROOT = HERE.parents[4]
FRAME_A = ROOT / "data" / "reconstructed" / "ft001-a"
OUT = ROOT / "data" / "reconstructed" / "ft001-a-window"

SEED = 1797
CALIPER = 3.0                      # M0 5 a: 3 points [1; 5]
CALIPER_GRID = (1.0, 5.0)
MAX_MATCHES = 5
RUN_FALL_PCT = 20.0                # M0 5 a: reserves down 20% [10; 30]
RUN_GRID = (10.0, 30.0)
PLACEBO_DRAWS = 10_000             # section 16, N1 (200 in the first two builds)
SCENARIO_RUNS = 1000               # section 18, P1: the scenarios' band's runs (300 in the third build, 100 in the first two)
EDGE_BATCHES = 20                  # section 18, P2: the batches of a band edge's standard error (W24)
AT_EDGE_SE = 2.0                   # section 18, P1: a mean within this many standard errors of an edge is "at the edge"
PLACEBO_MIN_CELLS = 30             # W19, the session's reading: a placebo with fewer cells cannot be read as a band
PLACEBO_STRATUM_YEARS = 3          # W19: the stratified placebo draws within +-3 years of the real change
GDP_RATIO_BAND = (1.0, 300.0)      # section 15, O4: deposits to GDP in per cent; outside it is flagged units_suspect
GDP_SEAM_FACTOR = 2.0              # section 16, N4: IFS NGDP and the World Bank's GDP may differ by this factor, no more
UNITS_BREAK = 100.0                # W14: a change of units, in deposits to GDP year on year
UNITS_BREAK_AT_SEAM = 10.0         # section 16, N4: ... where a source seam falls
IDENTICAL_TOL = 1e-3               # section 16, N4: |lines / survey - 1| below this is identical (W14)
#: The protocol's commits the manifest names beside the code's (section 15, M1): section 13 amended the rules after
#: the first audit; section 15 amended the window build after its own.
#: Section 18 is commit 0ba2b58.
PROTOCOL_COMMITS = (("section 13", "de3fe65"), ("section 15", "23c93f9"), ("section 16", "b865963"),
                    ("section 18", "0ba2b58"), ("section 19", "c43eb81"), ("section 20", "6007f53"),
                    ("sections 21-22", "2776366"))
#: The builds whose windows had been seen when the readings after them were written (section 16, N6): W10 onward were
#: written after the first, W18 onward after both.
#: The third build's windows (section 18) had been seen when W24 onward were written.
WINDOWS_SEEN = (("first build", "eca6369"), ("second build", "a2bdaa6"), ("third build", "04403c6"))
#: A member's years as its union's money (W21, N5): member -> (first year, last year), None unbounded; a member not listed
#: is the union's throughout the record. **The four years match Garriga's ``regional`` flag exactly** (the frozen source
#: ``frame_a`` reads: MLI 1 from 1984, GNB from 1997, GNQ from 1985, MRT to 1972: W28, section 18, P8); that flag is no source
#: for the XCD members (the EC dollar dates from 1965, Grenada 1968, her flag from 1983). Barbados (the EC dollar until 1973)
#: is not in ``frame_a.UNIONS`` and moves nothing: no headline match uses it before 1975.
UNION_SPAN = {"MLI": (1984, None), "GNB": (1997, None), "GNQ": (1985, None), "MRT": (None, 1972)}
ANNUAL_OFFSETS = tuple(range(-3, 6))
MONTHLY_OFFSETS = tuple(range(-24, 37))
PANEL4_LAST_COVERED = 2022         # W5, section 19: the last full year AREAER's 2023 edition closes
#: Panel 4's money whose coverage stops before the others (W5, section 19): the first uncovered year. Paraguay adopted on 18 May
#: 2011 (Resolucion N 22; Sami's hand download, section 18), which Hammond's 27 do not hold and no line of the list dates;
#: Uganda in July 2011 (the Bank of Uganda's Monetary Policy Statement, section 21), likewise.
PANEL4_UNCOVERED_FROM = {"PRY": 2011, "UGA": 2011}
#: Section 20, B4: a candidate that cannot be read whose frozen document dates the regime's start before Y - 1 is covered
#: only through the year before that start (Ukraine: inflation targeting from 2015; Mongolia: the target from 2021).
PANEL4_COVERED_THROUGH = {"UKR": 2014, "MNG": 2020}
FROM2012 = "4-from-2012"           # the members file's panel of AREAER's candidates (frame_a.FROM2012; sections 14 and 17)
#: Frame a's lines of the variant that adds the later and the transition documents (section 17, 19), and the reading that reads them.
LATER_OR_TRANSITION_ROUTE = "a4-var-later-or-transition-documents"
LATER_OR_TRANSITION_READING = "a4-later-or-transition-documents"

#: The panels' headline routes (the list's ``route`` column); a line of these routes is a change of the panel,
#: whatever its status. Variant readings replace a panel's routes.
HEADLINE_ROUTES = {"1": ("a1",), "2": ("a2",), "3": ("a3-up", "a3-down"), "4": ("a4",)}
READINGS = {"headline": HEADLINE_ROUTES, "a2-bj-note7": {"2": ("a2-var-bj-note7",)},
            LATER_OR_TRANSITION_READING: {"4": ("a4", LATER_OR_TRANSITION_ROUTE)}}     # W5, section 19

UNIVERSAL_STATUSES = ("counted", "apart", "ended unbroken")
#: The window may add M0's own status *censored* to a counted line (W16); the list's statuses are the three above.
UNION_NO_PI = ("no union-level price series: the money is a currency union's; its members have π and the union has "
               "none (W15)")
NOT_BUILT = {
    "dollarisation": ("no open series splits residents' deposits by currency: IFS and MFS publish the split for one "
                      "economy (35B, 35X); the IMF's Financial Soundness Indicators proxy (FSDFCD) is not frozen "
                      "(FT-001-M3-sources.md, 'Not found')"),
}

# --- dates ----------------------------------------------------------------------------------------------------

DATE = re.compile(r"^\s*(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?\s*$")


def parse_date(text: str) -> tuple[int, int | None, int | None]:
    """(year, month or None, day or None) of ``YYYY``, ``YYYY-MM`` or ``YYYY-MM-DD``; ValueError otherwise."""
    m = DATE.match(text or "")
    if not m:
        raise ValueError(f"not a date: {text!r}")
    return int(m.group(1)), int(m.group(2)) if m.group(2) else None, int(m.group(3)) if m.group(3) else None


def month_index(year: int, month: int) -> int:
    return year * 12 + month - 1


def month_label(t: int) -> str:
    return f"{t // 12:04d}-{t % 12 + 1:02d}"


def earliest_month(text: str) -> int:
    """The first month the date could be in (a year-only date: its January)."""
    y, m, _ = parse_date(text)
    return month_index(y, m or 1)


# --- the lists: frame a's ``series.csv``, ``members.csv`` and ``coverage.csv`` (read, never edited) ---------------

def read_csv(path: Path) -> list[dict]:
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


@dataclass(frozen=True)
class Change:
    """One line of frame a's list that the window completes."""
    key: str               # route|money|entry_date: names the line
    row: int               # its row in series.csv (the header is row 1)
    panel: str
    route: str
    money: str
    entry_date: str
    year: int
    month: int | None
    status: str            # the list's (headline reading) or derived (a variant reading, W8)
    status_reason: str
    war_year: str
    flags: str
    exit_date: str         # a competing exit's date, '' if none
    exit_year: int | None
    members: tuple[str, ...] = ()   # a union's line: the members the list names in its note (W15)

    @property
    def t0(self) -> int | None:
        """Its month index when it is dated to the month."""
        return month_index(self.year, self.month) if self.month else None

    @property
    def t_first(self) -> int:
        return month_index(self.year, self.month or 1)

    @property
    def exit_t(self) -> int | None:
        return earliest_month(self.exit_date) if self.exit_date else None


def derived_status(row: dict) -> tuple[str, str]:
    """W8: the status of a variant reading's line. The list marks a variant line *apart*; its other reasons
    (a war year, an exit before 1931) are read from the line itself."""
    if row["war_year"].startswith("yes"):
        return "apart", "war year at entry: told"
    if "exit before 1931" in row["note"]:
        return "apart", "exit before 1931, outside M0's span (P13)"
    return "counted", "variant reading: counted by the same rules as the headline"


#: The currency unions whose changes their members take (W15): ``frame_a.UNIONS`` (XOF, XAF, XCD) and the euro area.
UNION_CODES = frozenset(UNIONS) | {"EMU"}
_MEMBERS = re.compile(r"members:\s*([A-Z]{3}(?:\s*,\s*[A-Z]{3})*)")


def parse_members(note: str) -> tuple[str, ...]:
    """The members a union's line names in its note (``members: BEN, BFA, ...``), as the list wrote them."""
    found = _MEMBERS.search(note or "")
    return tuple(re.findall(r"[A-Z]{3}", found.group(1))) if found else ()


def union_members(change: "Change") -> tuple[str, ...]:
    """The monies whose changes include this line (W15): for a union's line, its members that year -- the ones the
    list names, else the union's economies (the euro area: ``EURO_ENTRY``'s from their entry year); () for any other."""
    if change.money not in UNION_CODES:
        return ()
    if change.members:
        return change.members
    if change.money == "EMU":
        return tuple(sorted(m for m, e in EURO_ENTRY.items() if int(e[:4]) <= change.year))
    return tuple(UNIONS[change.money][1])


def load_changes(series_rows: list[dict], reading: str = "headline") -> list[Change]:
    """Every line of the reading's routes, any status, in the list's order; the list's row numbers kept."""
    route_panel = {r: p for p, routes in READINGS[reading].items() for r in routes}
    out = []
    for i, row in enumerate(series_rows, start=2):
        panel = route_panel.get(row["route"])
        if panel is None:
            continue
        year, month, _ = parse_date(row["entry_date"])
        status, why = (row["status"], "") if reading == "headline" else derived_status(row)
        if status not in UNIVERSAL_STATUSES:
            raise ValueError(f"row {i}: status {status!r}")
        exit_date, exit_year = "", None
        if row.get("exit", "").strip():
            found = re.search(r"\b(\d{4}(?:-\d{2}(?:-\d{2})?)?)\b", row["exit"])
            if found:
                exit_date, exit_year = found.group(1), int(found.group(1)[:4])
        out.append(Change(f"{row['route']}|{row['money']}|{row['entry_date']}", i, panel, row["route"], row["money"],
                          row["entry_date"], year, month, status, why, row.get("war_year", ""), row.get("flags", ""),
                          exit_date, exit_year, parse_members(row.get("note", ""))))
    keys = Counter(c.key for c in out)
    dup = [k for k, n in keys.items() if n > 1]
    if dup:
        raise ValueError(f"two lines of the list share a key: {dup[:3]}")
    return out


def empty_years(text: str) -> frozenset[int]:
    """Coverage.csv's ``years_empty``: years and ranges such as ``1985`` or ``1973-1975``, separated by ; or ,."""
    years: set[int] = set()
    for token in re.findall(r"\d{4}(?:\s*-\s*\d{4})?", text or ""):
        parts = [int(p) for p in re.findall(r"\d{4}", token)]
        years.update(range(parts[0], parts[-1] + 1))
    return frozenset(years)


_FIRST_LISTED = re.compile(r"first listed in the AREAER (\d{4})")


def first_listing_year(row: dict) -> int:
    """Y, the first AREAER edition that lists a ``4-from-2012`` candidate, read from its reason ("first listed in the AREAER
    <Y> inflation-targeting column"); refused (ValueError) where it cannot be read or is no edition from 2012 to 2023."""
    found = _FIRST_LISTED.search(row.get("reason") or "")
    if found is None or not 2012 <= int(found.group(1)) <= PANEL4_LAST_COVERED + 1:
        raise ValueError(f"{FROM2012} {row.get('code')!r}: the first AREAER edition that lists it cannot be read from its "
                         f"reason ({(row.get('reason') or '')[:80]!r})")
    return int(found.group(1))


def panel4_unread_from2012(members_rows: list[dict]) -> dict[str, int]:
    """The ``4-from-2012`` candidates whose adoption cannot be read, each with Y (:func:`first_listing_year`); refused where
    the file holds the list's placeholder (a row with no code: the list was not rebuilt, section 17) or a Y cannot be read."""
    out: dict[str, int] = {}
    for r in members_rows:
        if r["panel"] != FROM2012:
            continue
        if not r["code"].strip():
            raise ValueError(f"{FROM2012}: a row with no code (the list's placeholder): frame a's list has not been rebuilt "
                             "with AREAER's candidates (sections 14 and 17)")
        if r["member"] == "cannot be read":
            out[r["code"]] = first_listing_year(r)
    return out


def panel4_last_covered(members_rows: list[dict], later_or_transition: frozenset[str] | set[str] = frozenset()) -> dict[str, int]:
    """Panel 4's last covered year, for each money covered through less than :data:`PANEL4_LAST_COVERED` (W5, section 19):
    a candidate from 2012 whose adoption cannot be read, through Y - 2 (:func:`panel4_unread_from2012`) unless
    ``later_or_transition`` (the variant's monies: their lines date them, covered through 2022); Paraguay, through the year
    before :data:`PANEL4_UNCOVERED_FROM`; a candidate named in :data:`PANEL4_COVERED_THROUGH` (section 20, B4), through the
    earlier of Y - 2 and that year. Any other money is covered through 2022."""
    out = {m: min(y - 2, PANEL4_COVERED_THROUGH.get(m, y - 2))
           for m, y in panel4_unread_from2012(members_rows).items() if m not in later_or_transition}
    out.update({m: y - 1 for m, y in PANEL4_UNCOVERED_FROM.items()})
    return out


def later_or_transition_money(changes: list["Change"]) -> frozenset[str]:
    """The monies the variant ``a4-later-or-transition-documents`` dates: those with a line of its route in ``changes``."""
    return frozenset(c.money for c in changes if c.route == LATER_OR_TRANSITION_ROUTE)


def coverage_table(panel: str, monies: list[str], first: int, last: int, members_rows: list[dict],
                   coverage_rows: list[dict], later_or_transition: frozenset[str] | set[str] = frozenset()) -> np.ndarray:
    """Who the panel's source covers, money by year: True where the list can tell "no change" there.

    Panels 1 and 2: a candidate whose membership the list reads (yes or no); *cannot be read* is uncovered.
    Panel 3: Garriga's years between her first and last, less the years she leaves empty. Panel 4: every money
    through 2022 (W5, section 19), less the older candidates (panel ``4``) whose date *cannot be read*, the candidates from
    2012 whose adoption cannot be read after Y - 2 (not ``later_or_transition``: the variant's monies, which are covered
    through 2022) and Paraguay from 2011 (:func:`panel4_last_covered`)."""
    T = last - first + 1
    out = np.zeros((len(monies), T), bool)
    years = np.arange(first, last + 1)
    if panel in ("1", "2"):
        known = {r["code"] for r in members_rows if r["panel"] == panel and r["member"] in ("yes", "no")}
        for j, m in enumerate(monies):
            out[j, :] = m in known
    elif panel == "3":
        table = {r["money"]: (int(r["first_year"]), int(r["last_year"]), empty_years(r["years_empty"]))
                 for r in coverage_rows if r["first_year"].strip() and r["last_year"].strip()}   # SUN: no year coded
        for j, m in enumerate(monies):
            if m in table:
                a, b, empty = table[m]
                out[j, :] = (years >= a) & (years <= b) & ~np.isin(years, list(empty))
    elif panel == "4":
        unread = {r["code"] for r in members_rows if r["panel"] == "4" and r["member"] == "cannot be read"}
        ends = panel4_last_covered(members_rows, later_or_transition)
        for j, m in enumerate(monies):
            out[j, :] = (years <= min(PANEL4_LAST_COVERED, ends.get(m, PANEL4_LAST_COVERED))) & (m not in unread)
    else:
        raise ValueError(f"panel {panel!r}")
    return out


def coverage_monies(panel: str, members_rows: list[dict], coverage_rows: list[dict],
                    universe: list[str]) -> set[str]:
    """The monies that can be in a panel's pool (before the year test): panel 4's are every money read."""
    if panel in ("1", "2"):
        return {r["code"] for r in members_rows if r["panel"] == panel and r["member"] in ("yes", "no")}
    if panel == "3":
        return {r["money"] for r in coverage_rows}
    return set(universe)


def standing(panel: str, monies: list[str], first: int, last: int, members_rows: list[dict],
             changes: list[Change]) -> np.ndarray:
    """The at-risk variant's table (P27): 1 where the support stood on the money in the year, 0 where it did not,
    2 where that cannot be read. Panels 1 and 2: convertible (a member from its adoption or return year to its
    change); panel 3: every money is at risk; panel 4: not yet targeting, from 1 before the money's first change to 0 from it
    (an adopter from 2012 likewise: its line is a change), and **2 (cannot be read)** for a candidate from 2012 whose adoption
    cannot be read from Y - 1 on, unless the variant dates it (a line of :data:`LATER_OR_TRANSITION_ROUTE` in ``changes``), and
    for Paraguay from 2011 (W5, section 19)."""
    import panel as panel_readers_module  # the workshop's readers of the lists' own reasons
    T = last - first + 1
    out = np.ones((len(monies), T), np.int8)
    years = np.arange(first, last + 1)
    first_change: dict[str, int] = {}
    for c in changes:
        first_change[c.money] = min(first_change.get(c.money, 9999), c.year)
    if panel in ("1", "2"):
        read = (panel_readers_module.gold_adoption_year if panel == "1" else panel_readers_module.gold_return_year)
        rows = {r["code"]: r for r in members_rows if r["panel"] == panel}
        for j, m in enumerate(monies):
            r = rows.get(m)
            if r is None or r["member"] == "cannot be read":
                out[j, :] = 2
            elif r["member"] == "no":
                out[j, :] = 0
            else:
                start = read(r["reason"])
                if start is None:
                    out[j, :] = 2
                else:
                    end = first_change.get(m, 9999)
                    out[j, :] = np.where((years >= start) & (years < end), 1, 0)
    elif panel == "4":
        unread = {r["code"] for r in members_rows if r["panel"] == "4" and r["member"] == "cannot be read"}
        unread_2012 = panel4_unread_from2012(members_rows)
        dated = later_or_transition_money(changes)
        for j, m in enumerate(monies):
            if m in unread:
                out[j, :] = 2
            elif m in unread_2012 and m not in dated:
                out[j, :] = np.where(years >= unread_2012[m] - 1, 2, 1)
            elif m in first_change:
                out[j, :] = np.where(years >= first_change[m], 0, 1)
            if m in PANEL4_UNCOVERED_FROM:
                out[j, years >= PANEL4_UNCOVERED_FROM[m]] = 2
    return out


# --- the panel's data, as arrays ------------------------------------------------------------------------------------

@dataclass
class PanelData:
    """Everything the pool and the match read, money by year. Built from the real readers
    (:func:`panel_data`) or from a synthetic panel (:func:`null_band`): the same pool and match run on both."""
    monies: list[str]
    first: int
    last: int
    pi: np.ndarray                      # n x T, annual π(y), NaN where unread
    covered: np.ndarray                 # n x T, bool
    war: np.ndarray                     # n x T, 0 no, 1 yes, 2 cannot be read
    at_risk: np.ndarray                 # n x T, 1 at risk, 0 not, 2 cannot be read
    change_years: list[list[int]]       # per money, the panel's changes (any status), sorted
    change_months: list[list[int]]      # the same, as the earliest month index
    union_years: list[list[int]] | None = None    # per money, the changes of its XOF / XAF / XCD union (W15), sorted
    union_months: list[list[int]] | None = None
    euro_from: list[int | None] | None = None     # per money, the year it entered the euro area, if it did
    euro_years: list[list[int]] | None = None     # per money, the changes of the euro area's line (``EMU``), sorted
    euro_months: list[list[int]] | None = None
    union_span: list[tuple[int | None, int | None] | None] | None = None   # per money, its years in XOF / XAF / XCD (W21)
    pi_first: list[int | None] | None = None      # per money, the first year it has a π in any year (W22)
    cum: np.ndarray = field(init=False)
    cum_union: np.ndarray = field(init=False)     # own changes and its XOF / XAF / XCD union's
    cum_euro: np.ndarray = field(init=False)      # own changes and the euro area's
    cum_all: np.ndarray = field(init=False)       # own changes and both
    index: dict[str, int] = field(init=False)

    def _cumulate(self, table: list[list[int]]) -> np.ndarray:
        n, T = self.pi.shape
        out = np.zeros((n, T + 1), np.int32)
        for j, years in enumerate(table):
            mark = np.zeros(T, np.int32)
            for y in years:
                if self.first <= y <= self.last:
                    mark[y - self.first] += 1
            out[j, 1:] = np.cumsum(mark)
        return out

    def _join(self, *tables: list[list[int]] | None) -> list[list[int]]:
        out = [list(ys) for ys in self.change_years]
        for table in tables:
            if table is not None:
                out = [sorted(a + b) for a, b in zip(out, table)]
        return out

    def __post_init__(self) -> None:
        self.index = {m: j for j, m in enumerate(self.monies)}
        self.cum = self._cumulate(self.change_years)
        self.cum_union = self.cum if self.union_years is None else self._cumulate(self._join(self.union_years))
        self.cum_euro = self.cum if self.euro_years is None else self._cumulate(self._join(self.euro_years))
        self.cum_all = (self.cum if self.union_years is None and self.euro_years is None
                        else self._cumulate(self._join(self.union_years, self.euro_years)))

    def years_of(self, j: int, unions: bool = True, euro: bool = True) -> list[int]:
        """Money ``j``'s changes of the panel: its own, and (``unions``) its XOF / XAF / XCD union's and (``euro``) the euro
        area's, sorted (W15)."""
        out = list(self.change_years[j])
        if unions and self.union_years is not None:
            out += self.union_years[j]
        if euro and self.euro_years is not None:
            out += self.euro_years[j]
        return sorted(out)

    def months_of(self, j: int, unions: bool = True, euro: bool = True) -> list[int]:
        out = list(self.change_months[j])
        if unions and self.union_months is not None:
            out += self.union_months[j]
        if euro and self.euro_months is not None:
            out += self.euro_months[j]
        return sorted(out)

    def entries(self, j: int, unions: bool = True, euro: bool = True) -> list[tuple[int, str]]:
        """The years money ``j`` enters a union's money (W21): the euro area (``euro_from``) and XOF / XAF / XCD
        (``union_span``'s first year), each with its label; none where it was always the union's."""
        out: list[tuple[int, str]] = []
        if euro and self.euro_from is not None and self.euro_from[j] is not None:
            out.append((int(self.euro_from[j]), "euro entry"))
        span = self.union_span[j] if unions and self.union_span is not None else None
        if span is not None and span[0] is not None:
            out.append((int(span[0]), "union entry"))
        return out

    def in_euro(self, year: int) -> np.ndarray:
        """True for each money that is a euro member in ``year`` (the euro is one money from its entry, M0 section 1)."""
        out = np.zeros(len(self.monies), bool)
        if self.euro_from is not None:
            for j, e in enumerate(self.euro_from):
                out[j] = e is not None and e <= year
        return out

    def in_union(self, year: int) -> np.ndarray:
        """True for each money that is, in ``year``, the money of XOF, XAF or XCD (W21): its union's from its entry to its
        exit (:data:`UNION_SPAN`), never a comparator of its own."""
        out = np.zeros(len(self.monies), bool)
        if self.union_span is not None:
            for j, span in enumerate(self.union_span):
                out[j] = span is not None and (span[0] is None or span[0] <= year) and (span[1] is None or year <= span[1])
        return out

    def first_pi_year(self, j: int) -> int | None:
        """The first year money ``j`` has a π in its whole series (W22), else the panel table's first, else None."""
        if self.pi_first is not None and self.pi_first[j] is not None:
            return int(self.pi_first[j])
        read = np.nonzero(~np.isnan(self.pi[j]))[0]
        return int(self.first + read[0]) if len(read) else None

    @property
    def T(self) -> int:
        return self.last - self.first + 1

    def col(self, year: int) -> int | None:
        c = year - self.first
        return c if 0 <= c < self.T else None

    def pi_at(self, j: int, year: int) -> float:
        c = self.col(year)
        return float("nan") if c is None else float(self.pi[j, c])

    def free_of_changes(self, lo: int, hi: int, unions: bool = True, euro: bool = True) -> np.ndarray:
        """True for each money with no change of the panel in the years lo..hi (inclusive); ``unions`` and ``euro``: a
        union's change is its members' (W15), the first build's reading when False."""
        a, b = max(lo - self.first, 0), min(hi - self.first + 1, self.T)
        if a >= b:
            return np.ones(len(self.monies), bool)
        cum = self.cum_all if unions and euro else self.cum_union if unions else self.cum_euro if euro else self.cum
        return (cum[:, b] - cum[:, a]) == 0

    def covered_over(self, lo: int, hi: int) -> np.ndarray:
        if lo < self.first or hi > self.last:
            return np.zeros(len(self.monies), bool)
        return self.covered[:, lo - self.first:hi - self.first + 1].all(axis=1)


def panel_data(panel: str, changes: list[Change], readers: "Readers", members_rows: list[dict],
               coverage_rows: list[dict], *, other_changes: list[Change] | None = None) -> PanelData:
    """The pool's data for one panel and reading, from the readers. ``changes``: every line of the panel's routes.
    The years run from 4 before the earliest change to 6 after the latest, **and 3 more each way** (W19: the stratified
    placebo draws within +-3 years of a real change, and a pseudo-change in the 3 years outside the span reads y-3 and y+5
    too); the pool and the match of a real change read nothing the extra years add."""
    if not changes:
        raise ValueError(f"panel {panel}: no change")
    first = min(c.year for c in changes) - 4 - PLACEBO_STRATUM_YEARS
    last = max(c.year for c in changes) + 6 + PLACEBO_STRATUM_YEARS
    universe = sorted(readers.monies())
    allowed = coverage_monies(panel, members_rows, coverage_rows, universe)
    monies = sorted((allowed & set(universe)) | {c.money for c in changes if c.money in set(universe)})
    T = last - first + 1
    pi = np.full((len(monies), T), np.nan)
    war = np.zeros((len(monies), T), np.int8)
    pi_first: list[int | None] = []
    for j, m in enumerate(monies):
        series = readers.series("pi", m, "A")
        ever = [y for y, v in series.items() if isinstance(v[0], (int, float)) and not math.isnan(v[0])]
        pi_first.append(min(ever) if ever else None)                          # W22: the whole series, not the table
        for y in range(first, last + 1):
            if y in series and isinstance(series[y][0], (int, float)):
                pi[j, y - first] = series[y][0]
            w = readers.war(m, y)
            war[j, y - first] = 1 if str(w).startswith("yes") else 2 if w == "cannot be read" else 0
    by_money: dict[str, list[Change]] = defaultdict(list)
    for c in changes:
        by_money[c.money].append(c)
    position = {m: j for j, m in enumerate(monies)}
    union_years: list[list[int]] = [[] for _ in monies]
    union_months: list[list[int]] = [[] for _ in monies]
    euro_years: list[list[int]] = [[] for _ in monies]
    euro_months: list[list[int]] = [[] for _ in monies]
    for c in changes:                                        # W15: a union's change is each of its members'
        euro = c.money == "EMU"
        for member in union_members(c):
            j = position.get(member)
            if j is not None and member != c.money:
                (euro_years if euro else union_years)[j].append(c.year)
                (euro_months if euro else union_months)[j].append(c.t_first)
    euro_from = [int(EURO_ENTRY[m][:4]) if m in EURO_ENTRY else None for m in monies]
    union_span = [UNION_SPAN.get(m, (None, None)) if m in UNION_OF else None for m in monies]     # W21
    return PanelData(monies, first, last, pi,
                     coverage_table(panel, monies, first, last, members_rows, coverage_rows, later_or_transition_money(changes)),
                     war, standing(panel, monies, first, last, members_rows, changes),
                     [sorted(c.year for c in by_money.get(m, [])) for m in monies],
                     [sorted(c.t_first for c in by_money.get(m, [])) for m in monies],
                     [sorted(y) for y in union_years], [sorted(t) for t in union_months], euro_from,
                     [sorted(y) for y in euro_years], [sorted(t) for t in euro_months], union_span, pi_first)


# --- the pool -----------------------------------------------------------------------------------------------------

def pool(pd: PanelData, i: int, y: int, *, rule: str = "past", war_unreadable: str = "keep",
         at_risk_only: bool = False, euro_as_own: bool = False,
         unions_as_own: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """The non-changers of a change of money ``i`` in year ``y``: (indices, war-unreadable flags of those).

    ``rule="past"`` (the headline, section 13): no change of the panel in y-3..y and the source covering the
    money over those years; ``rule="written"`` (the variant): no change in y-3..y+3, covered over y-3..y+3.
    Always: a price reading in y-1; no war year in y (P29); a war year that cannot be read stays, flagged
    (``war_unreadable="drop"``: dropped). ``at_risk_only``: only monies the support stood on in y-1.

    **Unions** (W15, W21; sections 15 and 16): a union's change is each member's (``pd.union_years``, ``pd.euro_years``) in
    "no change in y-3..y", and a member from its entry year is the union's money, no comparator of its own
    (:meth:`PanelData.in_euro`, :meth:`PanelData.in_union`): the euro area, and XOF, XAF and XCD alike. ``euro_as_own``
    and ``unions_as_own`` are the first build's reading of each (the variants ``euro-members-as-own`` and
    ``union-members-as-own``)."""
    hi = y if rule == "past" else y + 3
    if rule not in ("past", "written"):
        raise ValueError(rule)
    ok = pd.free_of_changes(y - 3, hi, unions=not unions_as_own, euro=not euro_as_own) & pd.covered_over(y - 3, hi)
    if not euro_as_own:
        ok &= ~pd.in_euro(y)
    if not unions_as_own:
        ok &= ~pd.in_union(y)
    ok[i] = False
    c1 = pd.col(y - 1)
    ok &= ~np.isnan(pd.pi[:, c1]) if c1 is not None else False
    cy = pd.col(y)
    w = pd.war[:, cy] if cy is not None else np.full(len(pd.monies), 2, np.int8)
    ok &= w != 1
    if war_unreadable == "drop":
        ok &= w != 2
    if at_risk_only:
        cb = pd.col(y - 1)
        ok &= (pd.at_risk[:, cb] == 1) if cb is not None else False
    idx = np.nonzero(ok)[0]
    return idx, w[idx] == 2


# --- the match ----------------------------------------------------------------------------------------------------

class Match(NamedTuple):
    j: int
    money: str
    distance: float
    gap_level: float           # comparator's π(y-1) less the change's
    gap_rise: float            # comparator's change in π (y-3 to y-1) less the change's (nan on the level match)
    path_end: int              # the first year NOT read of its path (y+6: the whole window)
    end_reason: str            # '', 'own later change YYYY', or 'panel coverage ends YYYY'
    flags: tuple[str, ...]


def tie_rng(key: str) -> np.random.Generator:
    """W2: the draw's generator, seeded by 1797 and the change's key alone."""
    digest = hashlib.sha256(f"{SEED}|{key}".encode()).digest()
    return np.random.default_rng(int.from_bytes(digest[:8], "big"))


def path_end(pd: PanelData, j: int, y: int, unions: bool = True, euro: bool = True) -> tuple[int, str]:
    """W3: the first year not read of comparator ``j``'s path after a change in ``y``: its own later change, its union's
    (W15) or **its entry into the euro or a union** (W21, N7), whichever comes first within y+1..y+5, or the first year its
    panel's source stops covering it. ``unions`` and ``euro`` False are the first build's reading (the later change of the
    union is no end, and neither is an entry)."""
    end, why = y + 6, ""
    own = pd.change_years[j]
    stops = [(c, 0 if c in own else 1, f"own later change {c}" if c in own else f"its union's later change {c}")
             for c in pd.years_of(j, unions, euro) if y < c <= y + 5]
    stops += [(e, 2, f"{label} {e}") for e, label in pd.entries(j, unions, euro) if y < e <= y + 5]
    if stops:
        end, _, why = min(stops)
    for t in range(y + 1, end):
        c = pd.col(t)
        if c is None or not pd.covered[j, c]:
            return t, f"panel coverage ends {t}"
    return end, why


def match(pd: PanelData, i: int, y: int, cand: np.ndarray, war_flag: np.ndarray, *, key: str,
          caliper: float = CALIPER, k: int = MAX_MATCHES, on: str = "level+rise",
          skip_empty_paths: bool = False, stats: dict | None = None, unions: bool = True,
          euro: bool = True) -> list[Match]:
    """Up to ``k`` comparators from the pool, nearest first (W1), each within ``caliper`` on π(y-1) and, unless
    ``on="level"``, on the change in π from y-3 to y-1; ties drawn (W2). Empty if the change's own π(y-1) (or,
    on "level+rise", π(y-3)) cannot be read. ``stats``, if given, is filled with ``matchable`` (comparators with
    every reading the match needs) and ``in_caliper``."""
    if on not in ("level+rise", "level"):
        raise ValueError(on)
    if stats is not None:
        stats.update(matchable=0, in_caliper=0)
    own1, own3 = pd.pi_at(i, y - 1), pd.pi_at(i, y - 3)
    if math.isnan(own1) or (on == "level+rise" and math.isnan(own3)) or len(cand) == 0:
        return []
    c1, c3 = pd.col(y - 1), pd.col(y - 3)
    lvl = pd.pi[cand, c1]
    g1 = np.abs(lvl - own1)
    keep = g1 <= caliper
    if on == "level+rise":
        if c3 is None:
            return []
        rise = lvl - pd.pi[cand, c3]
        g2 = np.abs(rise - (own1 - own3))
        readable = ~np.isnan(g2)
        keep &= readable & (g2 <= caliper)
        dist = g1 + np.where(readable, g2, 0.0)
    else:
        readable = np.ones(len(cand), bool)
        rise = np.full(len(cand), np.nan)
        dist = g1
    sel = np.nonzero(keep)[0]
    if stats is not None:
        stats.update(matchable=int(readable.sum()), in_caliper=len(sel))
    if skip_empty_paths:
        sel = np.array([s for s in sel if path_end(pd, int(cand[s]), y, unions, euro)[0] > y + 1], dtype=int)
    if len(sel) == 0:
        return []
    draw = tie_rng(key).random(len(cand))
    order = sorted(sel, key=lambda s: (round(float(dist[s]), 9), float(draw[s])))[:k]
    out = []
    for s in order:
        j = int(cand[s])
        end, why = path_end(pd, j, y, unions, euro)
        flags = ("war year cannot be read",) if war_flag[s] else ()
        out.append(Match(j, pd.monies[j], float(dist[s]), float(lvl[s] - own1),
                         float(rise[s] - (own1 - own3)) if on == "level+rise" else float("nan"), end, why, flags))
    return out


def _nanmean(a: np.ndarray) -> float:
    a = a[~np.isnan(a)]
    return float(a.mean()) if len(a) else float("nan")


def path_delta(pd: PanelData, j: int, y: int, end: int) -> float:
    """Mean π over y+1 .. end-1 less π(y-1); NaN when no year of the path is read."""
    a, b = y + 1 - pd.first, min(end, pd.last + 1) - pd.first
    if a < 0 or b <= a:
        return float("nan")
    return _nanmean(pd.pi[j, a:b]) - pd.pi_at(j, y - 1)


def described_gap(pd: PanelData, i: int, y: int, own_end: int, matches: list[Match]) -> dict:
    """W4: the change's after-minus-before in π, less its comparators' mean. ``n_used``: comparators whose path
    holds at least one read year."""
    own = path_delta(pd, i, y, own_end)
    deltas = [d for d in (path_delta(pd, m.j, y, m.path_end) for m in matches) if not math.isnan(d)]
    comp = float(np.mean(deltas)) if deltas else float("nan")
    gap = own - comp if deltas and not math.isnan(own) else float("nan")
    return {"own": own, "comparators": comp, "gap": gap, "n_used": len(deltas)}


def comparator_kind(panel: str, y: int, years: list[int], member: str | None, alt_years: list[int]) -> str:
    """What a comparator is, for the description: panel 2's are earlier or later leavers (section 13); the
    others' changers. ``years``: the comparator's own changes of the panel (any status); ``alt_years``: changes
    of another reading (panel 2: Bernanke and James's note 7 exits, whose exchange controls the headline does not
    count)."""
    noun = "leaver" if panel == "2" else "changer"
    earlier = [c for c in years if c < y - 3]
    later = [c for c in years if c > y]
    if earlier:
        return f"earlier {noun} ({max(earlier)})"
    if later:
        return f"later {noun} (first {min(later)}, path ends there if by y+5)"
    if panel == "2":
        if alt_years:
            return f"no headline exit by 1936; a leaver on note 7 ({min(alt_years)}): exchange control only"
        return "not a leaver by 1936" + ("" if member == "yes" else " (not a member: not on gold at the end of 1929)")
    return f"no change of the panel in the record ({member or 'not listed'})" if member else "no change of the panel"


# --- the run rule (P24, P25) ----------------------------------------------------------------------------------------

RUN_SOURCE_NEED = ("Board of Governors, Banking and Monetary Statistics 1914-1941 (1943), table 160 "
                   "(frame-a/bms-1914-1941, frozen 2026-10-01; bms160.py): with no reader given, every panel 1 "
                   "and 2 line's run test is 'cannot be read' and the line stays counted (P25)")


GOLD_ONLY = "no (gold only)"


def run_test(change: Change, reserves_at: Callable[[str, str], float | None] | None,
             threshold: float = RUN_FALL_PCT, *, gold_only: bool = True) -> tuple[str, str]:
    """(verdict, reason): 'n/a' (panels 3 and 4), 'cannot be read', 'yes' (reserves down by the threshold or more
    in the 12 months before) or 'no'. ``reserves_at(money, label)``: the reserves at the end of ``YYYY`` or
    ``YYYY-MM``, None where unread. W7 fixes the two dates. **W13: ``gold_only``** (the reader of BMS table 160,
    which gives gold and not foreign exchange): a "no" is written ``no (gold only)``, so that it is never read as "no
    run"; a "yes" stays "yes"."""
    if change.panel not in ("1", "2"):
        return "n/a", "panels 1 and 2 only (P24)"
    if reserves_at is None:
        return "cannot be read", "no reserves reader given: Banking and Monetary Statistics 1914-1941, table 160 (P25)"
    if change.t0 is not None:
        end, start = month_label(change.t0 - 1), month_label(change.t0 - 13)
    else:
        end, start = str(change.year - 1), str(change.year - 2)
    a, b = reserves_at(change.money, start), reserves_at(change.money, end)
    if a is None or b is None or a <= 0 or b <= 0:
        return "cannot be read", f"no reserves reading at {start} or {end}"
    fall = 100 * (b / a - 1)
    if fall <= -threshold:
        return "yes", f"reserves {start} to {end}: {fall:.1f}%"
    if gold_only:
        return GOLD_ONLY, f"reserves {start} to {end}: {fall:.1f}% (gold only: foreign exchange is not in the source)"
    return "no", f"reserves {start} to {end}: {fall:.1f}%"


def run_flag(verdict: str) -> str:
    """``gold_only`` on a "no" read from gold alone (O3), '' otherwise."""
    return "gold_only" if verdict == GOLD_ONLY else ""


def bms_reserves_at(basis: str = "20.67") -> Callable[[str, str], float | None]:
    """W9: ``reserves_at(money, label)`` from BMS table 160 (``bms160.reserves``), parsed once, at one footing. Gold
    only (W13). There is no strict variant: the audit's page check is the record (W9, O2)."""
    import bms160
    cells = bms160.table()[0]

    def read(money: str, label: str) -> float | None:
        return bms160.reserves(money, label, basis=basis, cells=cells)
    return read


def gap_in_record(pd: PanelData, j: int, year: int) -> bool:
    """True where money ``j`` has no π in ``year`` but has one in an earlier year **anywhere in its price series** (W22):
    the record begins before it, so ``year`` is a hole in it (or past its end), not a window before the record (M2: DJI
    1992, LSO 2000, RWA 1997 in the first build; RUS 1990, whose π runs to 1910 and from 1993, in the second). A panel
    built without the whole series reads the panel's table only."""
    first = pd.first_pi_year(j)
    return first is not None and first < year


def window_status(change: Change, pd: PanelData, annual_end: int | None, run: tuple[str, str]) -> tuple[str, str]:
    """(status, reason). Only *counted* moves, each move written (section 6): to *apart* for no π in y-3 (a window
    before the price record, or **a gap in the price record** where the record begins before y-3: M2) and for an
    exit after a run; to M0's own status *censored* (y+5 past the panel's common end) when censoring is the only
    reason (W16). With both, the line is *apart* and every reason is written."""
    if change.status != "counted":
        return change.status, change.status_reason
    reasons, censored = [], False
    if math.isnan(pd.pi_at(pd.index[change.money], change.year - 3)):
        if gap_in_record(pd, pd.index[change.money], change.year - 3):
            reasons.append(f"a gap in the price record: no π reading in the year y-3 = {change.year - 3}, "
                           "though the record begins earlier")
        else:
            reasons.append("window before the price record: no π reading in the year y-3")
    if annual_end is not None and change.year + 5 > annual_end:
        reasons.append(f"censored: y+5 = {change.year + 5} is past the panel's common end {annual_end}")
        censored = True
    if run[0] == "yes":
        reasons.append(f"exit after a run: {run[1]}")
    if not reasons:
        return "counted", ""
    only_censored = censored and len(reasons) == 1
    return ("censored" if only_censored else "apart"), "; ".join(reasons)


def monthly_status(change: Change, readers: "Readers", monthly_end: int | None) -> str:
    if change.t0 is None:
        return "not built: the change is dated to the year only"
    if not readers.has_monthly(change.money):
        return "not built: no monthly reading of this money"
    if monthly_end is not None and change.t0 + 36 > monthly_end:
        return f"censored: month+36 is past the monthly common end {month_label(monthly_end)}; read to it"
    return "read"


# --- the readers of the window's measures -----------------------------------------------------------------------------

class Reading(NamedTuple):
    value: float | None
    source: str = ""
    flag: str = ""
    reason: str = ""            # why it is unread, when value is None
    note: str = ""              # what is told beside a read value: each seam's ratio (W14)


#: name -> (family, unit, frequencies)
MEASURES = {
    "pi": ("value", "%", "AM"),
    "depreciation": ("value", "%", "AM"),
    "market_split": ("value", "1 recorded, 0 not recorded", "AM"),
    "deposits_to_gdp": ("trust", "% of GDP", "A"),
    "currency_to_deposits": ("trust", "ratio", "AM"),
    "dollarisation": ("trust", "not built", "A"),
    "reserves_change": ("trust", "%, 12 months", "AM"),
}
SPLIT_VALUE = {"recorded": 1.0, "not recorded": 0.0}


class Readers:
    """Every reading the window needs, by money. Each table is a function money -> {period: reading}, so the real
    readers (:func:`panel_readers`) load lazily and a test passes dicts. Periods are years (annual) or month
    indices, ``year * 12 + month - 1`` (monthly).

    - ``pi_a``, ``pi_m``: {period: (π, source, flagged B)}; ``d_a``, ``d_m``: {period: (d, flagged, anchor)};
    - ``split(money, label)``: 'recorded', 'not recorded', 'no parity' or 'cannot be read' (``panel.split_at``);
    - ``reserves_a``, ``reserves_m``: {period: level}; ``deposits_a``, ``deposits_m``, ``gdp_a``: {period: (level,
      source tag)}; ``currency_a``, ``currency_m``: the same; ``deposits_gdp_a``: the deposits deposits to GDP may
      read (W6; ``deposits_a`` when not given); ``war(money, year)``: 'yes...', 'no', 'cannot be read';
      ``seam_text(money)``: what the readers tell of the deposits' seam beyond the step across it (W14);
      ``gdp_suspect(money)``: {year: why} the years of GDP whose units are suspect (the World Bank segment where it
      differs from IFS NGDP by more than a factor of 2, W20).
    """

    def __init__(self, *, monies, pi_a, pi_m=None, d_a=None, d_m=None, split=None, reserves_a=None, reserves_m=None,
                 deposits_a=None, deposits_m=None, currency_a=None, currency_m=None, gdp_a=None, war=None,
                 deposits_gdp_a=None, annual_end: int | None = None, monthly_end: int | None = None, locator=None,
                 seam_text=None, gdp_suspect=None):
        empty = lambda money: {}  # noqa: E731
        self._monies = monies
        self.pi_a, self.pi_m = pi_a, pi_m or empty
        self.d_a, self.d_m = d_a or empty, d_m or empty
        self.split = split or (lambda money, label: "cannot be read")
        self.reserves_a, self.reserves_m = reserves_a or empty, reserves_m or empty
        self.deposits_a, self.deposits_m = deposits_a or empty, deposits_m or empty
        self.deposits_gdp_a = deposits_gdp_a or self.deposits_a      # W6: the old lines only where units are checked
        self.currency_a, self.currency_m = currency_a or empty, currency_m or empty
        self.gdp_a = gdp_a or empty
        self._war = war or (lambda money, year: "cannot be read")
        self.annual_end, self.monthly_end = annual_end, monthly_end
        self._locator = locator
        self._seam_text = seam_text
        self._gdp_suspect = gdp_suspect
        self._cache: dict[tuple, dict] = {}

    def monies(self) -> list[str]:
        return list(self._monies() if callable(self._monies) else self._monies)

    def war(self, money: str, year: int) -> str:
        return self._war(money, year)

    def gdp_suspect(self, money: str) -> dict:
        """{year: why} the years of ``money``'s GDP whose units are suspect (W20); empty where no check is given."""
        return self._gdp_suspect(money) if self._gdp_suspect else {}

    def has_monthly(self, money: str) -> bool:
        return bool(self.pi_m(money))

    def locator(self, measure: str, money: str, freq: str, source: str) -> str:
        if self._locator:
            return self._locator(measure, money, freq, source)
        return f"window_a.Readers: {measure} ({freq}), {source}, money {money}"

    # -- one period ---------------------------------------------------------------------------------------------------
    def series(self, measure: str, money: str, freq: str) -> dict:
        """{period: (value, source, flag)} of π, the one plain series the pool and the match read; every measure is
        read, with its reason when unread, through :meth:`read`."""
        table = {("pi", "A"): self.pi_a, ("pi", "M"): self.pi_m}.get((measure, freq))
        if table is None:
            raise KeyError(f"{measure}/{freq} is not a plain series: use read()")
        out = {}
        for t, (v, src, flag) in table(money).items():
            out[t] = (v, src, flag)
        return out

    def read(self, measure: str, money: str, freq: str, t: int) -> Reading:
        """One money's reading of one measure at one period: a value, or the reason it is unread."""
        if measure not in MEASURES or freq not in MEASURES[measure][2]:
            raise KeyError(f"{measure}/{freq}")
        if measure in NOT_BUILT:
            return Reading(None, reason=f"not built: {NOT_BUILT[measure]}")
        if measure == "pi":
            v = (self.pi_a if freq == "A" else self.pi_m)(money).get(t)
            return Reading(None, reason="no π reading") if v is None else Reading(float(v[0]), v[1], "B" if v[2] else "")
        if measure == "depreciation":
            v = (self.d_a if freq == "A" else self.d_m)(money).get(t)
            if v is None:
                return Reading(None, reason="no depreciation reading (IFS ENDE)")
            return Reading(float(v[0]), f"IFS ENDE, anchor {v[2]}", "B" if v[1] else "")
        if measure == "market_split":
            label = str(t) if freq == "A" else month_label(t)
            verdict = self.split(money, label)
            return (Reading(SPLIT_VALUE[verdict], "IRR unified-market dummy", verdict) if verdict in SPLIT_VALUE
                    else Reading(None, reason=f"market split: {verdict}"))
        if measure == "reserves_change":
            table = (self.reserves_a if freq == "A" else self.reserves_m)(money)
            lag = 1 if freq == "A" else 12
            a, b = table.get(t - lag), table.get(t)
            if a is None or b is None or a <= 0 or b <= 0:
                return Reading(None, reason="no reserves reading (IFS RAXG_USD) at both ends")
            return Reading(100 * (b / a - 1), "IFS RAXG_USD")
        if measure == "deposits_to_gdp":
            dep_tab, gdp_tab = self.deposits_gdp_a(money), self.gdp_a(money)
            dep, gdp = dep_tab.get(t), gdp_tab.get(t)
            if dep is None and t in self.deposits_a(money):
                return Reading(None, reason="cannot be read: the old lines' units are not checked against the survey's (W6)")
            if dep is None:
                return Reading(None, reason="no deposits reading (depository corporations survey; IFS 24 + 25 before it)")
            if gdp is None or gdp[0] <= 0:
                return Reading(None, reason="no GDP reading (IFS NGDP, then the World Bank)")
            flags = [self._seam(dep_tab, t), self._seam(gdp_tab, t)]           # both seams, never the first alone (M6)
            notes = [self._seam_ratio(dep_tab, t, "deposits"), self._seam_ratio(gdp_tab, t, "GDP")]
            if flags[0] and self._seam_text:
                notes.append(self._seam_text(money))
            pct = 100 * dep[0] / gdp[0]
            lo, hi = GDP_RATIO_BAND
            if not lo <= pct <= hi:                                              # W14: the level band
                flags.append(f"units_suspect: deposits to GDP {pct:.3g}% is outside {lo:g}-{hi:g}%")
            segment = self.gdp_suspect(money)
            suspect = segment.get(t)
            if suspect:                                                          # W20: GDP's own seam
                flags.append(f"units_suspect: {suspect}")
            jump_year, at_seam = self._units_break(dep_tab, gdp_tab)
            if jump_year is not None and (jump_year in segment or jump_year - 1 in segment):
                jump_year = None          # W26: the break is the World Bank segment's, flagged; the IFS years are not carried
            if jump_year is not None and t == jump_year:
                flags.append(f"units break: the ratio moves by a factor of {UNITS_BREAK_AT_SEAM:g} or more at a source seam"
                             if at_seam else f"units break: the ratio moves by a factor of {UNITS_BREAK:g} or more")
            elif jump_year is not None and t > jump_year:
                flags.append(f"units break at {jump_year}: the units are not the earlier ones, every later year is flagged")
            return Reading(pct, f"{dep[1]} / {gdp[1]}", "; ".join(f for f in flags if f), note="; ".join(n for n in notes if n))
        if measure == "currency_to_deposits":
            cur_t, dep_t = (self.currency_a, self.deposits_a) if freq == "A" else (self.currency_m, self.deposits_m)
            cur, dep = cur_t(money).get(t), dep_t(money).get(t)
            if cur is None or dep is None or dep[0] <= 0:
                return Reading(None, reason="no currency and deposits readings together (depository corporations survey; "
                                            "IFS 14A and 24 + 25 before it)")
            flags = [self._seam(dep_t(money), t), self._seam(cur_t(money), t)]   # both tables' seams (M6)
            notes = [self._seam_ratio(dep_t(money), t, "deposits"), self._seam_ratio(cur_t(money), t, "currency")]
            return Reading(cur[0] / dep[0], f"{cur[1]} / {dep[1]}", "; ".join(f for f in flags if f),
                           note="; ".join(n for n in notes if n))
        raise KeyError(measure)

    @staticmethod
    def _seam(table: dict, t: int) -> str:
        """A seam between sources is flagged, never smoothed (M0 section 1)."""
        now, before = table.get(t), table.get(t - 1)
        if now and before and now[1] != before[1]:
            return f"seam: {before[1]} -> {now[1]}"
        return ""

    @staticmethod
    def _seam_ratio(table: dict, t: int, what: str) -> str:
        """The step across a seam, level at t over level at t-1, printed beside the reading (W14, O4): it is growth
        and a change of definition together, and a factor of 100 or more is a change of units."""
        now, before = table.get(t), table.get(t - 1)
        if now and before and now[1] != before[1] and before[0]:
            return f"{what} seam: level {now[0] / before[0]:.3g} times the year before's"
        return ""

    @staticmethod
    def _units_break(dep_tab: dict, gdp_tab: dict) -> tuple[int | None, bool]:
        """W14, W20: (the first year in which deposits to GDP moves from the year before's by a factor of
        :data:`UNITS_BREAK` or more, **or of** :data:`UNITS_BREAK_AT_SEAM` **or more where a source seam falls in that year**
        (the deposits' or GDP's source differs from the year before's), whether it was a seam); (None, False) if it never does."""
        ratio = {y: dep_tab[y][0] / gdp_tab[y][0] for y in dep_tab
                 if y in gdp_tab and dep_tab[y][0] > 0 and gdp_tab[y][0] > 0}
        for y in sorted(ratio):
            if y - 1 not in ratio:
                continue
            jump = max(ratio[y], ratio[y - 1]) / min(ratio[y], ratio[y - 1])
            seam = dep_tab[y][1] != dep_tab[y - 1][1] or gdp_tab[y][1] != gdp_tab[y - 1][1]
            if jump >= UNITS_BREAK:
                return y, False
            if seam and jump >= UNITS_BREAK_AT_SEAM:
                return y, True
        return None, False

    @staticmethod
    def _units_break_year(dep_tab: dict, gdp_tab: dict) -> int | None:
        """The year of :meth:`_units_break`, alone."""
        return Readers._units_break(dep_tab, gdp_tab)[0]


def ifs_level_by_money(code: str, freq: str) -> dict[str, dict[int, float]]:
    """An IFS series' levels by money (× its multiplier), keyed by year (A) or month index (M). The annual case is
    ``panel.ifs_levels``; the monthly one is written the same way. A group or an area with no economy is left
    out (``panel.area_money``); two areas for one money is an error."""
    import panel
    if freq == "A":
        return panel.ifs_levels(code)
    raw = panel.ifs(code, freq)
    mult = panel._dbnomics_mult(f"IFS/{freq}~~{code}")
    out: dict[str, dict[int, float]] = {}
    for area, series in raw.items():
        money = panel.area_money(area, f"IFS {code}")
        if money is None:
            continue
        if money in out:
            raise ValueError(f"IFS {code}: {money} held by two areas")
        out[money] = {t: v * mult.get(area, 1.0) for t, (v, _) in series.items()}
    return out


def add_levels(a: dict[int, float], b: dict[int, float], tag: str) -> dict[int, tuple[float, str]]:
    """{period: (a + b, tag)} where both are read."""
    return {t: (a[t] + b[t], tag) for t in a if t in b}


def old_presentation_deposits(l35: dict[int, float], l14: dict[int, float], last: int = 2000,
                              tag: str = "derived: IFS 35L less 14A") -> dict[int, tuple[float, str]]:
    """W6's variant: deposits as broad money less currency outside banks, in IFS's old presentation, to ``last``.
    An identity, read only with ``deposits_before="identity"``."""
    return {t: (l35[t] - l14[t], tag) for t in l35 if t in l14 and t <= last}


OLD_LINES = "IFS 24 + 25 (old presentation)"
OLD_CURRENCY = "IFS 14A (old presentation)"
UNITS_BAND = (0.5, 2.0)


def before(table: dict[int, float], first: int | None, tag: str) -> dict[int, tuple[float, str]]:
    """{period: (level, tag)} for the periods before ``first`` (every period when ``first`` is None)."""
    return {t: (v, tag) for t, v in table.items() if first is None or t < first}


def old_lines_deposits(l24: dict[int, float], l25: dict[int, float], first: int | None,
                       tag: str = OLD_LINES) -> dict[int, tuple[float, str]]:
    """W6: demand (24) plus time, savings and foreign-currency deposits (25) of the deposit money banks, before the
    money's first survey reading ``first``."""
    return before({t: l24[t] + l25[t] for t in l24 if t in l25}, first, tag)


#: The euro's fixed conversion rates, legacy units per euro, by economy: the European Central Bank's "Our money"
#: page, frozen at ``frame-a/ecb-euro-area-members`` (2026-09-30); a test reads each rate there.
EURO_RATE = {"BEL": 40.3399, "BGR": 1.95583, "DEU": 1.95583, "EST": 15.6466, "IRL": 0.787564, "GRC": 340.750,
             "ESP": 166.386, "CYP": 0.585274, "FRA": 6.55957, "HRV": 7.53450, "ITA": 1936.27, "LVA": 0.702804,
             "LTU": 3.45280, "LUX": 40.3399, "MLT": 0.429300, "NLD": 2.20371, "AUT": 13.7603, "PRT": 200.482,
             "SVN": 239.640, "SVK": 30.1260, "FIN": 5.94573}
EURO_CODE = {"BEL": "BEF", "BGR": "BGN", "DEU": "DEM", "EST": "EEK", "IRL": "IEP", "GRC": "GRD", "ESP": "ESP",
             "CYP": "CYP", "FRA": "FRF", "HRV": "HRK", "ITA": "ITL", "LVA": "LVL", "LTU": "LTL", "LUX": "LUF",
             "MLT": "MTL", "NLD": "NLG", "AUT": "ATS", "PRT": "PTE", "SVN": "SIT", "SVK": "SKK", "FIN": "FIM"}


def _differ(lines: float, survey: float) -> bool:
    """Two readings differ (W14, W20): **not** |lines / survey - 1| < :data:`IDENTICAL_TOL`. A ratio of 1 to within a
    thousandth is the survey filling the lines (rounding included), not two sources."""
    if survey == 0:
        return lines != 0
    return not abs(lines / survey - 1) < IDENTICAL_TOL


def old_lines_units(money: str, lines: dict[int, float], survey: dict[int, float],
                    gdp: dict[int, float]) -> tuple[float, str] | None:
    """W6: (factor, tag) that put the old lines in the units of deposits to GDP, or None when the check fails.
    **W14**: where the two overlap, the check is made only on the years where they differ (W20: by a thousandth or more);
    if they never do (IFS fills
    lines 24 + 25 with the survey's numbers from 2001, so the overlap says nothing), the lines before the overlap are
    checked against the survey across the gap, by deposits to GDP."""
    factor, tag = 1.0, OLD_LINES
    if not survey:                     # a member with a survey of its own (Bulgaria) is checked against it instead
        if money in EURO_RATE:
            return 1 / EURO_RATE[money], f"{OLD_LINES}, in euros at the fixed rate"
        return factor, f"{OLD_LINES}, units unchecked (no survey reading)"
    conv = lines
    common = set(conv) & set(survey)
    if common:
        if any(_differ(conv[t], survey[t]) for t in common):
            return (factor, tag) if units_agree(conv, survey) else None
        conv = {t: v for t, v in conv.items() if t < min(common)}       # the survey filling the lines is no check
        if not conv:
            return None
    last, first = max(conv), min(survey)
    if last < first and gdp.get(last) and gdp.get(first):
        gap = {0: conv[last] / gdp[last]}, {0: survey[first] / gdp[first]}
        return (factor, f"{tag}, units checked across the gap") if units_agree(*gap, differing_only=False) else None
    return None


def units_agree(old: dict[int, float], survey: dict[int, float], band: tuple[float, float] = UNITS_BAND, *,
                differing_only: bool = True) -> bool:
    """W6: the old lines and the survey are in the same units where both first read **and differ** (their ratio within
    ``band``). No common period, or none where they differ, is no check: False (W14). ``differing_only=False`` is the
    gap check's, whose two readings are two years' deposits to GDP and are not an overlap."""
    common = sorted(t for t in set(old) & set(survey) if not differing_only or _differ(old[t], survey[t]))
    if not common or not survey[common[0]]:
        return False
    return band[0] <= old[common[0]] / survey[common[0]] <= band[1]


def seam_ratio_text(lines: dict[int, float], survey: dict[int, float], gdp: dict[int, float]) -> str:
    """W14: what to print beside a deposits seam: the old lines over the survey at their first differing common year;
    or, with no differing overlap, deposits to GDP across the gap between them; or that nothing can be said."""
    common = sorted(set(lines) & set(survey))
    differing = [t for t in common if _differ(lines[t], survey[t])]
    if differing and survey[differing[0]]:
        t = differing[0]
        return f"old lines over survey {lines[t] / survey[t]:.3g} at {t} (the first year they differ)"
    if common:
        before = [t for t in lines if t < common[0]]
        if before and gdp.get(max(before)) and gdp.get(min(survey)) and survey[min(survey)]:
            a, b = max(before), min(survey)
            r = (lines[a] / gdp[a]) / (survey[b] / gdp[b])
            return (f"old lines identical to the survey over {common[0]}-{common[-1]} (no check); deposits to GDP "
                    f"{lines[a] / gdp[a]:.3g} at {a} against {survey[b] / gdp[b]:.3g} at {b}: ratio {r:.3g}")
        return f"old lines identical to the survey over {common[0]}-{common[-1]} (no check)"
    if lines and survey:
        a, b = max(lines), min(survey)
        if a < b and gdp.get(a) and gdp.get(b) and survey[b]:
            r = (lines[a] / gdp[a]) / (survey[b] / gdp[b])
            return f"no overlap; deposits to GDP across the gap {r:.3g} times ({a} against {b})"
    return "no overlap and no GDP at the gap: the seam's ratio cannot be read"


def gdp_seam_message(ifs: dict[int, float], wb: dict[int, float], factor: float = GDP_SEAM_FACTOR) -> str:
    """W20, W26 (section 18, P5): ``''`` unless the **median** ratio of the World Bank's GDP to IFS NGDP over their common years
    is beyond ``factor`` (either way), in which case the text says what it is: their units are not the same, and the World Bank
    segment of the merged GDP is not in IFS's. The third build read **any** common year (Suriname flagged for 2014 alone); one
    year's disagreement is no seam."""
    common = sorted(t for t in set(ifs) & set(wb) if ifs[t] > 0 and wb[t] > 0)
    if not common:
        return ""
    median = float(np.median([wb[t] / ifs[t] for t in common]))
    if max(median, 1 / median) <= factor:
        return ""
    return (f"GDP seam: the World Bank's GDP is {median:.3g} times IFS NGDP at the median of the {len(common)} common years "
            f"{common[0]}-{common[-1]} (beyond a factor of {factor:g}): the World Bank segment is not in IFS's units")


def merge_sources(*tables: dict[int, tuple[float, str]]) -> dict[int, tuple[float, str]]:
    """The first table that reads a period wins (M0's order); the seam is flagged by :meth:`Readers.read`."""
    out: dict[int, tuple[float, str]] = {}
    for table in tables:
        for t, v in table.items():
            out.setdefault(t, v)
    return out


DEPOSITS_BEFORE = ("lines", "identity", "none")


def panel_readers(deposits_before: str = "lines") -> Readers:
    """The real readers, all through ``panel.py``. **Never called in a test, and not run by this session**: it
    loads the frozen series. π and d are ``Panel.pi_annual``, ``pi_monthly``, ``d_annual``, ``d_monthly``; the
    market split ``panel.split_at``; war ``panel.war_at`` (war.py); the common ends ``panel.common_end``. Deposits
    before the survey: ``deposits_before`` (W6)."""
    if deposits_before not in DEPOSITS_BEFORE:
        raise ValueError(f"deposits_before: one of {DEPOSITS_BEFORE}")
    import panel
    pan = panel.Panel()
    annual_end = panel.common_end(pan.have_annual(), 1)
    monthly_end = panel.common_end(pan.have_monthly(), 12)
    cache: dict = {}

    def memo(name, fn):
        def read(money):
            key = (name, money)
            if key not in cache:
                cache[key] = fn(money)
            return cache[key]
        return read

    def level(code, freq):
        def read(money):
            key = ("level", code, freq)
            if key not in cache:
                cache[key] = ifs_level_by_money(code, freq)
            return cache[key].get(money, {})
        return read

    joint = deposits_before == "lines"

    def survey_deposits(freq, money, tag="IFS DCS (FDSBO + FDSBT)"):
        return add_levels(level("FDSBO_XDC", freq)(money), level("FDSBT_XDC", freq)(money), tag)

    def survey_currency(freq, money):
        return {t: (v, "IFS DCS FDSBC") for t, v in level("FDSBC_XDC", freq)(money).items()}

    def switch(freq, money):
        """M6: the period from which both trust tables of a ratio read the survey: the **later** of their first survey
        readings; infinity (the old lines only) where one of the two has no survey reading at all."""
        d, c = survey_deposits(freq, money), survey_currency(freq, money)
        return max(min(d), min(c)) if d and c else math.inf

    def dcs(freq, tag="IFS DCS (FDSBO + FDSBT)", *, together=False):
        """Deposits: the survey from its first reading (``together``: from the ratio's switch, M6), the old lines
        (W6) before it."""
        def read(money):
            key = ("dcs", freq, money, together)
            if key not in cache:
                table = survey_deposits(freq, money, tag)
                first = min(table) if table else None
                if together and joint:
                    first = switch(freq, money)
                    table = {t: v for t, v in table.items() if t >= first}
                old: dict = {}
                if deposits_before == "lines":
                    old = old_lines_deposits(level("24____XDC", freq)(money), level("25____XDC", freq)(money), first)
                elif deposits_before == "identity" and freq == "A":
                    old = old_presentation_deposits(level("35L___XDC", "A")(money), level("14A___XDC", "A")(money),
                                                    last=2000 if first is None else min(2000, first - 1))
                cache[key] = merge_sources(table, old)
            return cache[key]
        return read

    def dcs_for_gdp(money):
        """W6: the old lines enter deposits to GDP only where their units are checked (:func:`old_lines_units`)."""
        key = ("dcs_gdp", money)
        if key not in cache:
            table = dcs("A")(money)
            if deposits_before != "lines":
                cache[key] = table
                return table
            survey = {t: v for t, (v, src) in table.items() if src != OLD_LINES}
            l24, l25 = level("24____XDC", "A")(money), level("25____XDC", "A")(money)
            lines = {t: l24[t] + l25[t] for t in l24 if t in l25}
            gdp_levels = {t: v for t, (v, _) in gdp(money).items()}
            units = old_lines_units(money, lines, survey, gdp_levels) if lines else None
            out = {t: v for t, v in table.items() if v[1] != OLD_LINES}
            if units:
                factor, tag = units
                out.update({t: (v * factor, tag) for t, (v, src) in table.items() if src == OLD_LINES})
            cache[key] = out
            cache[("seam", money)] = seam_ratio_text(lines, survey, gdp_levels) if lines and survey else ""
        return cache[key]

    def seam_text(money):
        dcs_for_gdp(money)
        return cache.get(("seam", money), "")

    def currency(freq):
        def read(money):
            key = ("cur", freq, money)
            if key not in cache:
                table = survey_currency(freq, money)
                first = min(table) if table else None
                if joint:
                    first = switch(freq, money)                                    # M6: both tables at the later first reading
                    table = {t: v for t, v in table.items() if t >= first}
                    table = merge_sources(table, before(level("14A___XDC", freq)(money), first, OLD_CURRENCY))
                elif deposits_before == "identity" and freq == "A":
                    cut = 2001 if first is None else min(2001, first)
                    table = merge_sources(table, before(level("14A___XDC", freq)(money), cut, OLD_CURRENCY))
                cache[key] = table
            return cache[key]
        return read

    def gdp(money):
        key = ("gdp", money)
        if key not in cache:
            ifs = {t: (v, "IFS NGDP") for t, v in level("NGDP_XDC", "A")(money).items()}
            wb = {t: (v, "WB GDP") for t, v in panel.worldbank("NY.GDP.MKTP.CN").get(money, {}).items()}
            cache[key] = merge_sources(ifs, wb)
            why = gdp_seam_message({t: v for t, (v, _) in ifs.items()}, {t: v for t, (v, _) in wb.items()})
            cache[("gdp_suspect", money)] = {t: why for t in wb if t not in ifs} if why else {}      # W20: the WB segment
        return cache[key]

    def gdp_suspect(money):
        gdp(money)
        return cache.get(("gdp_suspect", money), {})

    def locator(measure, money, freq, source):
        codes = {"pi": None, "depreciation": "ENDE_XDC_USD_RATE", "reserves_change": "RAXG_USD",
                 "deposits_to_gdp": "FDSBO_XDC + FDSBT_XDC (before it 24 + 25) / NGDP_XDC",
                 "currency_to_deposits": "FDSBC_XDC / (FDSBO_XDC + FDSBT_XDC) (before it 14A / (24 + 25))",
                 "market_split": "irr/unified-market-annual-1946-2016"}
        if measure == "pi":
            return pan.locator(money, source) if source in panel.LOCATOR else f"{source}, money {money}"
        return f"dbnomics/IMF/IFS/{freq}~~{codes[measure]} (money {money})"

    return Readers(
        monies=pan.monies, pi_a=memo("pi_a", pan.pi_annual), pi_m=memo("pi_m", pan.pi_monthly),
        d_a=memo("d_a", pan.d_annual), d_m=memo("d_m", pan.d_monthly), split=panel.split_at,
        reserves_a=level("RAXG_USD", "A"), reserves_m=level("RAXG_USD", "M"),
        deposits_a=dcs("A", together=True), deposits_m=dcs("M", together=True), currency_a=currency("A"),
        currency_m=currency("M"), gdp_a=gdp, deposits_gdp_a=dcs_for_gdp, seam_text=seam_text, gdp_suspect=gdp_suspect,
        war=panel.war_at, annual_end=annual_end, monthly_end=monthly_end, locator=locator)


# --- the window's rows --------------------------------------------------------------------------------------------------

SERIES_FIELDS = ["period", "value", "unit", "source", "locator", "note", "uncertainty", "reading", "variant", "change",
                 "series_row", "panel", "route", "change_money", "entry_date", "status", "role", "money", "rank", "freq",
                 "measure", "family", "offset"]
UNREAD_FIELDS = ["reading", "variant", "change", "series_row", "panel", "route", "change_money", "entry_date", "status",
                 "role", "money", "rank", "freq", "measure", "family", "offset", "period", "reason"]
CHANGE_FIELDS = ["reading", "variant", "change", "series_row", "panel", "route", "money", "entry_date", "list_status",
                 "status", "status_reason", "monthly_status", "war_year", "flags", "exit", "pi_before", "pi_rise", "pool",
                 "matchable", "in_caliper", "matched", "used", "own_delta", "comparators_delta", "gap", "run_test",
                 "run_reason", "run_flag", "run_10", "run_30", "rules_sha256"]
MATCH_FIELDS = ["reading", "variant", "change", "series_row", "panel", "route", "change_money", "entry_date", "rank", "comparator",
                "comparator_kind", "distance", "gap_level", "gap_rise", "caliper", "path_end_year", "path_end_reason",
                "flags", "reuse", "reuse_counted", "monthly_data", "note"]
#: ``lo_se`` and ``hi_se``: each edge's standard error from 20 batches (W24; the third build's ``lo_err`` and ``hi_err`` were
#: the difference between two halves, W18).
BAND_FIELDS = ["panel", "label", "scenario", "pool", "match", "runs", "n_changes", "n_described", "share_matched", "mean",
               "sd_runs", "lo", "lo_se", "hi", "hi_se", "sd_single", "share_beyond_1", "reading", "line"]
#: The placebo band's rows (W11, W19): one per reading, label, design and description line, at that line's n with a gap.
#: ``lo_se`` and ``hi_se``: each edge's standard error (W24); ``cut``: the cells whose own path was cut (W19), ``cut_mean`` and
#: ``uncut_mean`` their mean gap and the others' (W25); ``min_stratum``: the stratified design's smallest stratum (W25, P7).
PLACEBO_FIELDS = ["reading", "panel", "label", "design", "line", "n", "draws", "cells", "cut", "cut_mean", "uncut_mean",
                  "min_stratum", "mean", "sd_draws", "lo", "lo_se", "hi", "hi_se", "sd_single", "share_beyond_1", "note"]
PLACEBO_DESIGNS = ("headline", "stratified", "future-clean")

#: The variants of the pool and the match (section 13; P29 as completed). Only the headline writes the window's rows.
VARIANTS: dict[str, dict] = {
    "headline": {},
    "pool-written": {"rule": "written"},
    "at-risk-only": {"at_risk_only": True},
    "war-unreadable-dropped": {"war_unreadable": "drop"},
    "caliper-1": {"caliper": CALIPER_GRID[0]},
    "caliper-5": {"caliper": CALIPER_GRID[1]},
    "level-only-match": {"on": "level"},
    "skip-empty-paths": {"skip_empty_paths": True},
    # W21: the first build's reading of each, one at a time (section 16, N5): the euro's members as monies of their own ...
    "euro-members-as-own": {"euro_as_own": True},
    # ... and XOF, XAF and XCD's members as monies of their own
    "union-members-as-own": {"unions_as_own": True},
}


def _row_id(change: Change, reading: str, variant: str) -> dict:
    return {"reading": reading, "variant": variant, "change": change.key, "series_row": change.row,
            "panel": change.panel, "route": change.route, "change_money": change.money,
            "entry_date": change.entry_date}


def comparator_end_t(pd: PanelData, m: Match, t0: int, unions: bool = True, euro: bool = True) -> tuple[int | None, str]:
    """A comparator's monthly path end: the earliest month of its own later change after ``t0`` within the window
    (+36), **or of its entry into the euro or a union** (W21, the January of the entry year), or the first month of the
    year its panel's coverage ends; None if none falls in the window."""
    ends = []
    later = [t for t in pd.months_of(m.j, unions, euro) if t0 < t <= t0 + 36]
    if later:
        ends.append((min(later), f"own later change {month_label(min(later))}"))
    for e, label in pd.entries(m.j, unions, euro):
        if t0 < e * 12 <= t0 + 36:
            ends.append((e * 12, f"{label} {month_label(e * 12)}"))
    if m.end_reason.startswith("panel coverage"):
        ends.append((m.path_end * 12, m.end_reason))
    return min(ends) if ends else (None, "")


def window_rows(change: Change, status: str, matches: list[Match], pd: PanelData, readers: Readers, *, reading: str,
                variant: str, kinds: dict[int, str], monthly: str, annual_end: int | None,
                monthly_end: int | None) -> tuple[list[dict], list[dict]]:
    """One row per change, measure and offset, for the change and for each matched comparator: the readings in
    ``series`` (period, value, unit, source, locator), what cannot be read in ``unread`` with its reason."""
    series, unread = [], []
    ident = _row_id(change, reading, variant)
    y, t0 = change.year, change.t0
    own_year_end = min(y + 6, change.exit_year) if change.exit_year else y + 6
    owners = [(change.money, "change", 0, own_year_end, f"competing exit {change.exit_year}" if change.exit_year else "",
               change.exit_t if t0 is not None else None, f"competing exit {change.exit_date}" if change.exit_date else "")]
    for rank, m in enumerate(matches, start=1):
        end_t, why_t = comparator_end_t(pd, m, t0) if t0 is not None else (None, "")
        owners.append((m.money, "comparator", rank, m.path_end, m.end_reason, end_t, why_t))

    def emit(role, money, rank, freq, measure, off, period, t, end, why):
        family, unit, _ = MEASURES[measure]
        base = {**ident, "status": status, "role": role, "money": money, "rank": rank, "freq": freq, "measure": measure,
                "family": family, "offset": off}
        if off > 0 and end is not None and t >= end:
            unread.append({**base, "period": period, "reason": f"path ended: {why}"})
            return
        cutoff = annual_end if freq == "A" else monthly_end
        if cutoff is not None and t > cutoff:
            unread.append({**base, "period": period, "reason": "past the panel's common end (censored)"})
            return
        r = readers.read(measure, money, freq, t)
        if r.value is None:
            unread.append({**base, "period": period, "reason": r.reason})
            return
        note = "; ".join(x for x in (kinds.get(rank, "") if role == "comparator" else "", r.flag and f"flag: {r.flag}",
                                     r.note) if x)
        series.append({**base, "period": period, "value": r.value, "unit": unit, "source": r.source,
                       "locator": readers.locator(measure, money, freq, r.source), "note": note,
                       "uncertainty": "flagged" if r.flag else "clear"})

    for money, role, rank, end_y, why_y, end_t, why_t in owners:
        for measure, (_family, _unit, freqs) in MEASURES.items():
            if "A" in freqs:
                for off in ANNUAL_OFFSETS:
                    emit(role, money, rank, "A", measure, off, str(y + off), y + off, end_y, why_y)
            if "M" in freqs and t0 is not None and not monthly.startswith("not built") and readers.has_monthly(money):
                for off in MONTHLY_OFFSETS:
                    emit(role, money, rank, "M", measure, off, month_label(t0 + off), t0 + off,
                         end_t if end_t is not None else None, why_t)
    return series, unread


def unread_all(change: Change, status: str, reason: str, *, reading: str, variant: str) -> list[dict]:
    """A change whose money has no reading at all: every measure and annual offset, unread, with the reason."""
    ident = _row_id(change, reading, variant)
    return [{**ident, "status": status, "role": "change", "money": change.money, "rank": 0, "freq": "A",
             "measure": measure, "family": MEASURES[measure][0], "offset": off, "period": str(change.year + off),
             "reason": reason} for measure in MEASURES for off in ANNUAL_OFFSETS]


# --- building one reading ---------------------------------------------------------------------------------------------------

@dataclass
class Result:
    changes: list[dict] = field(default_factory=list)
    matches: list[dict] = field(default_factory=list)
    series: list[dict] = field(default_factory=list)
    unread: list[dict] = field(default_factory=list)


def label_of(change: Change) -> str:
    return "3-up" if change.route == "a3-up" else "3-down" if change.route == "a3-down" else change.panel


def build_reading(reading: str, series_rows: list[dict], members_rows: list[dict], coverage_rows: list[dict],
                  readers: Readers, *, sha: str = "", variants: dict[str, dict] | None = None,
                  reserves_at: Callable[[str, str], float | None] | None = None,
                  run_threshold: float = RUN_FALL_PCT, gold_only: bool = True) -> Result:
    """Every change of a reading, every variant of the pool and the match; the window's rows for the headline only.
    ``gold_only``: the reserves reader gives gold and not foreign exchange (W13), so a "no" is ``no (gold only)``."""
    variants = VARIANTS if variants is None else variants
    result = Result()
    changes = load_changes(series_rows, reading)
    member_of: dict[str, dict[str, str]] = defaultdict(dict)
    for r in members_rows:
        member_of[r["panel"]][r["code"]] = r["member"]
    alt_years: dict[str, list[int]] = defaultdict(list)
    if reading == "headline":
        for c in load_changes(series_rows, "a2-bj-note7"):
            alt_years[c.money].append(c.year)
    annual_end, monthly_end = readers.annual_end, readers.monthly_end
    for panel in sorted({c.panel for c in changes}):
        of_panel = [c for c in changes if c.panel == panel]
        pd = panel_data(panel, of_panel, readers, members_rows, coverage_rows)
        for variant, options in variants.items():
            if variant == "at-risk-only" and panel == "3":
                continue                                    # every money is at risk of a reform: the headline is it
            served: Counter = Counter()
            served_counted: Counter = Counter()
            staged = []
            for c in of_panel:
                run = run_test(c, reserves_at, run_threshold, gold_only=gold_only)
                if c.money not in pd.index:
                    if c.status != "counted":
                        status, why = c.status, c.status_reason
                    elif c.money in UNION_CODES:                    # W15: the union's members have π, the union has none
                        status, why = "apart", UNION_NO_PI
                    else:
                        status, why = "apart", "window before the price record: the money has no π reading in any source"
                    staged.append((c, status, why, run, [], {}, None, "not built: no reading of this money"))
                    continue
                i = pd.index[c.money]
                status, why = window_status(c, pd, annual_end, run)
                as_own, euro_own = options.get("unions_as_own", False), options.get("euro_as_own", False)
                cand, war_flag = pool(pd, i, c.year, rule=options.get("rule", "past"),
                                      war_unreadable=options.get("war_unreadable", "keep"),
                                      at_risk_only=options.get("at_risk_only", False),
                                      euro_as_own=euro_own, unions_as_own=as_own)
                stats: dict = {}
                matches = match(pd, i, c.year, cand, war_flag, key=f"{reading}|{c.key}",
                                caliper=options.get("caliper", CALIPER), on=options.get("on", "level+rise"),
                                skip_empty_paths=options.get("skip_empty_paths", False), stats=stats,
                                unions=not as_own, euro=not euro_own)
                own_end = min(c.year + 6, c.exit_year) if c.exit_year else c.year + 6
                gap = described_gap(pd, i, c.year, own_end, matches)
                staged.append((c, status, why, run, matches, {**stats, "pool": len(cand), **gap}, i,
                               monthly_status(c, readers, monthly_end)))
                for m in matches:
                    served[m.money] += 1
                    if status in ("counted", "ended unbroken"):
                        served_counted[m.money] += 1
            for c, status, why, run, matches, info, i, monthly in staged:
                result.changes.append({
                    "reading": reading, "variant": variant, "change": c.key, "series_row": c.row, "panel": c.panel,
                    "route": c.route, "money": c.money, "entry_date": c.entry_date, "list_status": c.status,
                    "status": status, "status_reason": why, "monthly_status": monthly, "war_year": c.war_year,
                    "flags": c.flags, "exit": c.exit_date, "run_test": run[0], "run_reason": run[1],
                    "run_flag": run_flag(run[0]),
                    "run_10": run_test(c, reserves_at, RUN_GRID[0], gold_only=gold_only)[0],
                    "run_30": run_test(c, reserves_at, RUN_GRID[1], gold_only=gold_only)[0], "rules_sha256": sha,
                    "pi_before": "" if i is None or math.isnan(pd.pi_at(i, c.year - 1)) else pd.pi_at(i, c.year - 1),
                    "pi_rise": "" if i is None or math.isnan(pd.pi_at(i, c.year - 1) - pd.pi_at(i, c.year - 3))
                    else pd.pi_at(i, c.year - 1) - pd.pi_at(i, c.year - 3),
                    "pool": info.get("pool", ""), "matchable": info.get("matchable", ""),
                    "in_caliper": info.get("in_caliper", ""), "matched": len(matches), "used": info.get("n_used", ""),
                    "own_delta": _num(info.get("own")), "comparators_delta": _num(info.get("comparators")),
                    "gap": _num(info.get("gap"))})
                if i is None:
                    if variant == "headline":
                        result.unread += unread_all(c, status, monthly, reading=reading, variant=variant)
                    continue
                kinds = {}
                for rank, m in enumerate(matches, start=1):
                    kinds[rank] = comparator_kind(panel, c.year, pd.years_of(m.j), member_of[panel].get(m.money),
                                                  alt_years.get(m.money, []) if panel == "2" else [])
                    result.matches.append({
                        **_row_id(c, reading, variant), "rank": rank, "comparator": m.money,
                        "comparator_kind": kinds[rank], "distance": round(m.distance, 6), "gap_level": round(m.gap_level, 6),
                        "gap_rise": _num(m.gap_rise), "caliper": options.get("caliper", CALIPER),
                        "path_end_year": m.path_end, "path_end_reason": m.end_reason, "flags": "; ".join(m.flags),
                        "reuse": served[m.money], "reuse_counted": served_counted[m.money],
                        "monthly_data": "yes" if readers.has_monthly(m.money) else "no", "note": ""})
                if not matches:
                    result.matches.append({
                        **_row_id(c, reading, variant), "rank": 0, "comparator": "", "comparator_kind": "",
                        "distance": "", "gap_level": "", "gap_rise": "", "caliper": options.get("caliper", CALIPER),
                        "path_end_year": "", "path_end_reason": "", "flags": "", "reuse": "", "reuse_counted": "",
                        "monthly_data": "", "note": "shown alone: no comparator within the caliper" if info.get("pool")
                        else "shown alone: no comparator in the pool, or the change's own π cannot be read"})
                if variant == "headline":
                    s, u = window_rows(c, status, matches, pd, readers, reading=reading, variant=variant, kinds=kinds,
                                       monthly=monthly, annual_end=annual_end, monthly_end=monthly_end)
                    result.series += s
                    result.unread += u
    return result


def _num(x) -> float | str:
    return "" if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), 6)


# --- describing, beside the bands (sections 13 and 15) ------------------------------------------------------------------------

#: The description lines of the protocol (section 6): the counted lines; without those that overlap another of the
#: same money; the ended-unbroken lines; and the counted and ended-unbroken together (M3: "with and without").
DESCRIPTIONS = (
    ("counted", lambda r: r["status"] == "counted"),
    ("counted, without overlapping lines", lambda r: r["status"] == "counted" and "overlap" not in r["flags"]),
    ("ended unbroken", lambda r: r["status"] == "ended unbroken"),
    ("counted, with ended unbroken", lambda r: r["status"] in ("counted", "ended unbroken")),
)


def _label(r: dict) -> str:
    return "3-up" if r["route"] == "a3-up" else "3-down" if r["route"] == "a3-down" else r["panel"]


def description_members(change_rows: list[dict]) -> dict[tuple[str, str, str], list[dict]]:
    """Each description line's changes **with a gap**, by (reading, label, name), over the headline variant: the n of
    :func:`description_lines` and, for the stratified placebo (W19), which real changes they are."""
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in change_rows:
        if r["variant"] == "headline":
            groups[(r["reading"], _label(r))].append(r)
    return {(reading, label, name): [r for r in rows if keep(r) and r["gap"] != ""]
            for (reading, label), rows in sorted(groups.items()) for name, keep in DESCRIPTIONS}


def description_lines(change_rows: list[dict]) -> list[dict]:
    """Each description line's numbers, per reading and panel (panel 3 up and down apart), over the headline variant:
    ``reading``, ``label``, ``name``, ``n`` (the lines), ``n_gap`` (those with a gap: the n a band is computed at, W10)
    and ``mean`` (the mean described gap, None if no line has one). A line with no gap (no comparator, or no path) is
    in ``n`` and not in the mean."""
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in change_rows:
        if r["variant"] == "headline":
            groups[(r["reading"], _label(r))].append(r)
    out = []
    for (reading, label), rows in sorted(groups.items()):
        for name, keep in DESCRIPTIONS:
            chosen = [r for r in rows if keep(r)]
            gaps = [float(r["gap"]) for r in chosen if r["gap"] != ""]
            out.append({"reading": reading, "label": label, "name": name, "n": len(chosen), "n_gap": len(gaps),
                        "mean": float(np.mean(gaps)) if gaps else None})
    return out


def placebo_real_changes(change_rows: list[dict]) -> dict[tuple[str, str, str], list[tuple[int, float]]]:
    """The (year, π(y-1)) of each real change of each description line that has a gap: the stratified placebo's input (W19)."""
    out = {}
    for key, rows in description_members(change_rows).items():
        out[key] = [(int(r["entry_date"][:4]), float(r["pi_before"])) for r in rows if r.get("pi_before", "") != ""]
    return out


def _edge_pair(se: tuple | None) -> str:
    """`` (edge se lo, hi)``: each edge's standard error (W24); nothing where the rows carry none."""
    return f" (edge se {se[0]:.2f}, {se[1]:.2f})" if se is not None else ""


def _se_pair(row: dict) -> tuple[float, float] | None:
    """A row's ``(lo_se, hi_se)``, None where it carries none (or NaN)."""
    lo, hi = row.get("lo_se", ""), row.get("hi_se", "")
    if lo == "" or hi == "" or lo is None or hi is None:
        return None
    return float(lo), float(hi)


def envelope_bounds(band_rows: list[dict], label: str, pool_rule: str = "past", on: str = "level+rise",
                    reading: str = "", line: str = "") -> tuple[float, float, int] | None:
    """The headline combination's band over every synthetic scenario: (lo, hi, number of scenarios), None if the
    panel was not simulated. ``line`` '' is the first band (the list's counted n); a line's name, with its reading, is
    the band at that line's own n (:func:`band_at_n`)."""
    rows = _envelope_rows(band_rows, label, pool_rule, on, reading, line)
    if not rows:
        return None
    return min(float(r["lo"]) for r in rows), max(float(r["hi"]) for r in rows), len(rows)


def _envelope_rows(band_rows: list[dict], label: str, pool_rule: str, on: str, reading: str, line: str) -> list[dict]:
    return [r for r in band_rows if r["label"] == label and r["pool"] == pool_rule and r["match"] == on
            and r.get("line", "") == line and r.get("reading", "") == reading and r["lo"] != ""]


def envelope_se(band_rows: list[dict], label: str, pool_rule: str = "past", on: str = "level+rise",
                reading: str = "", line: str = "") -> tuple[float, float] | None:
    """The standard error (W24) of the envelope's two edges: the ``lo_se`` of the scenario whose ``lo`` is the lowest and the
    ``hi_se`` of the one whose ``hi`` is the highest; None where the rows carry none."""
    rows = _envelope_rows(band_rows, label, pool_rule, on, reading, line)
    if not rows or any(r.get("lo_se", "") == "" or r.get("hi_se", "") == "" for r in rows):
        return None
    return (float(min(rows, key=lambda r: float(r["lo"]))["lo_se"]), float(max(rows, key=lambda r: float(r["hi"]))["hi_se"]))


def envelope(band_rows: list[dict], label: str, pool_rule: str = "past", on: str = "level+rise",
             reading: str = "", line: str = "") -> str:
    """:func:`envelope_bounds`, as text, with each edge's standard error where the rows carry it (W24)."""
    found = envelope_bounds(band_rows, label, pool_rule, on, reading, line)
    if found is None:
        return "not simulated for this panel"
    se = envelope_se(band_rows, label, pool_rule, on, reading, line)
    return f"[{found[0]:+.2f}, {found[1]:+.2f}]{_edge_pair(se)} over {found[2]} scenarios"


def _placebo_row(placebo_rows: list[dict] | None, reading: str, label: str, name: str,
                 design: str = "headline") -> dict | None:
    for r in placebo_rows or []:
        if (r["reading"] == reading and r["label"] == label and r["line"] == name and r.get("design", "headline") == design
                and r["lo"] != ""):
            return r
    return None


def _readable(row: dict) -> bool:
    """A placebo of fewer than :data:`PLACEBO_MIN_CELLS` cells cannot be read as a band (W19)."""
    return int(row["cells"]) >= PLACEBO_MIN_CELLS


def _placebo_text(row: dict | None, design: str) -> str:
    name = f"{design} placebo band"
    if row is None:
        return f"{name} not drawn for this line"
    if not _readable(row):
        return (f"{name}: {row['cells']} pseudo-changes at n = {row['n']}, cannot be read as a band (fewer than "
                f"{PLACEBO_MIN_CELLS} cells)")
    text = (f"{name} [{float(row['lo']):+.2f}, {float(row['hi']):+.2f}]{_edge_pair(_se_pair(row))} over {row['draws']} draws at "
            f"n = {row['n']} ({row['cells']} pseudo-changes")
    if design == "stratified" and row.get("min_stratum", "") != "":
        text += f"; smallest stratum {row['min_stratum']}"
    return text + ")"


def _cut_text(row: dict | None) -> str:
    """W25 (P3): the share of cut cells among the headline placebo's pseudo-changes and their mean gap (and the uncut ones'),
    which is the whole difference between the headline's band and ``future-clean``'s. '' where the row carries no count."""
    if row is None or row.get("cut", "") == "" or not int(row.get("cells") or 0):
        return ""
    cells, cut = int(row["cells"]), int(row["cut"])
    if cut == 0:
        return f"no pseudo-change of the headline placebo has its path cut (0 of {cells})"
    text = f"{cut} of the headline placebo's {cells} pseudo-changes are cut cells ({100 * cut / cells:.0f}%)"
    if row.get("cut_mean", "") != "":
        text += f", mean gap {float(row['cut_mean']):+.2f}"
        if row.get("uncut_mean", "") != "":
            text += f" (the uncut ones' {float(row['uncut_mean']):+.2f})"
    return text


def _inside(mean: float, lo: float, hi: float) -> str:
    return "inside" if lo <= mean <= hi else "outside"


def _place(mean: float, lo: float, hi: float, se: tuple[float, float] | None = None) -> str:
    """Where a mean lies against a band (W24, section 18, P1): ``at the edge of`` when it is within :data:`AT_EDGE_SE` = 2
    standard errors of either edge (``se``: that edge's), else ``inside`` or ``outside``. With no standard error (None, or NaN)
    an edge is exact, and the mean is inside or outside."""
    if se is not None:
        if abs(mean - lo) < AT_EDGE_SE * se[0] or abs(mean - hi) < AT_EDGE_SE * se[1]:
            return "at the edge of"
    return _inside(mean, lo, hi)


def _disagreements(change_rows: list[dict]) -> list[str]:
    """W23: where the headline's and note 7's lines of one money differ (an entry date or a status, or a line in one reading
    only), one line per money and panel, each reading's line with its run verdict. Rows with no ``money`` are skipped."""
    by: dict[tuple[str, str], dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    readings_of: dict[str, set[str]] = defaultdict(set)
    for r in change_rows:
        if r["variant"] == "headline" and r.get("money"):
            by[(_label(r), r["money"])][r["reading"]].append(r)
            readings_of[_label(r)].add(r["reading"])
    sig = lambda rows: sorted((r["entry_date"], r["status"]) for r in rows)  # noqa: E731
    say = lambda rows: ("no line" if not rows else "; ".join(  # noqa: E731
        f"{r['entry_date']}, {r['status']}, run test {r.get('run_test', '?')}" for r in sorted(rows, key=lambda r: r["entry_date"])))
    out = []
    for (label, money), found in sorted(by.items()):
        if not {"headline", "a2-bj-note7"} <= readings_of[label]:
            continue                                          # a panel with one reading has nothing to disagree with
        head, note = found.get("headline", []), found.get("a2-bj-note7", [])
        if sig(head) != sig(note):
            out.append(f"panel {label}, {money}: the readings disagree: headline {say(head)}; note 7 {say(note)}")
    return out


def describe(change_rows: list[dict], band_rows: list[dict], placebo_rows: list[dict] | None = None) -> list[str]:
    """Each description's mean described gap with its bands beside it (sections 13, 15, 16 and 18): per reading and panel
    (panel 3 up and down apart), the headline variant's counted lines, those without overlapping lines, the ended-unbroken
    lines, and the two together (M3). **The bands are at the line's own n** (lines with a gap, W10): the scenarios' band
    (``band_rows``, :func:`band_at_n`'s rows; the first band at the list's n is the fallback, said) and the **three placebos**
    (``placebo_rows``, :func:`placebo_band`'s): the headline (past-only) one, the stratified one and ``future-clean`` (W25), **each
    edge with its standard error** (W24); a placebo of fewer than 30 cells says it "cannot be read as a band" and is not set
    against the mean. Beside the headline placebo: the share of its pseudo-changes whose path is cut and their mean gap (W25,
    P3); beside the stratified one: its smallest stratum (P7). **The mean is placed on each band**: ``inside``, ``outside``, or
    ``at the edge of`` it where it lies within 2 standard errors of an edge (W24, :func:`_place`). Where the headline and note 7
    disagree in sign, it says "the order cannot be read" (M3), and it prints their disagreements line by line (W23). **π only**
    (M8): the other measures have rows and no summary here and no band.

    A mean inside the scenarios' band and the placebo bands "is consistent with no effect"; outside one it is not a
    finding (section 16): this counts nothing and gives no verdict, it says where the mean lies."""
    lines, means = [], {}
    drawn = {design: any(r.get("design") == design for r in placebo_rows or []) for design in ("stratified", "future-clean")}
    for d in description_lines(change_rows):
        reading, label, name, n_gap, mean = d["reading"], d["label"], d["name"], d["n_gap"], d["mean"]
        text = f"{mean:+.2f}" if mean is not None else "n/a"
        scenarios = envelope_bounds(band_rows, label, reading=reading, line=name)
        if scenarios is not None:
            band = f"{envelope(band_rows, label, reading=reading, line=name)} at n = {n_gap}"
            scen_se = envelope_se(band_rows, label, reading=reading, line=name)
        else:                                         # no band at this line's n: the list's, said
            scenarios = envelope_bounds(band_rows, label)
            band = (envelope(band_rows, label) + (" at the list's n, not this line's" if scenarios is not None else ""))
            scen_se = envelope_se(band_rows, label)
        rows = {design: _placebo_row(placebo_rows, reading, label, name, design) for design in PLACEBO_DESIGNS}
        where = []
        if mean is not None and scenarios is not None:
            where.append(f"{_place(mean, scenarios[0], scenarios[1], scen_se)} the scenarios' band")
        for design in PLACEBO_DESIGNS:                                          # W25: all three designs
            row = rows[design]
            if mean is not None and row is not None and _readable(row):
                where.append(f"{_place(mean, float(row['lo']), float(row['hi']), _se_pair(row))} the {design} placebo band")
        line = (f"{reading} panel {label} ({name}): n = {d['n']}, with a gap {n_gap}, mean gap {text}; "
                f"null band under no effect {band}; {_placebo_text(rows['headline'], 'headline')}")
        cut = _cut_text(rows["headline"])
        if cut:
            line += f" [{cut}]"
        for design in ("stratified", "future-clean"):
            if drawn[design]:
                line += f"; {_placebo_text(rows[design], design)}"
        if where:
            line += "; the mean lies " + ", ".join(where[:-1]) + (" and " if len(where) > 1 else "") + where[-1]
        lines.append(line)
        if name == "counted" and mean is not None:
            means[(reading, label)] = mean
    for label in sorted({lab for (_, lab) in means}):
        a, b = means.get(("headline", label)), means.get(("a2-bj-note7", label))
        if a is not None and b is not None and a * b < 0:
            lines.append(f"panel {label}: the headline mean gap {a:+.2f} and note 7's {b:+.2f} disagree in sign: "
                         "the order cannot be read")
    lines += _disagreements(change_rows)
    return lines


# --- the null band (section 13) --------------------------------------------------------------------------------------------------

def edge_se(values, batches: int = EDGE_BATCHES) -> tuple[float, float]:
    """W24 (section 18, P2): each edge's **standard error**, ``(lo_se, hi_se)``. ``values`` (the independent draws or runs, in
    the order drawn, NaN left out) are cut into ``batches`` consecutive batches of equal size (the last ones one shorter
    where they do not divide); each batch gives the edge (2.5 and 97.5 per cent) and the error is the sd of the batches' edges
    over sqrt(``batches``): the sd of the edge computed from all the values, which is what it estimates. NaN with fewer than
    two values per batch. It replaces W18's half-against-half difference, which was a single random draw."""
    v = np.asarray(values, float)
    v = v[~np.isnan(v)]
    if len(v) < 2 * batches:
        return float("nan"), float("nan")
    parts = np.array_split(v, batches)
    return tuple(float(np.std([float(np.percentile(p, q)) for p in parts], ddof=1)) / math.sqrt(batches)
                 for q in (2.5, 97.5))  # type: ignore[return-value]


def _se(x: float) -> float | str:
    return "" if math.isnan(x) else round(float(x), 3)


@dataclass
class Shape:
    """A synthetic panel shaped like a real one: how many monies and changes, in which years, how changes recur.
    The sizes come from the committed list (:func:`shapes_from_list` refreshes them); the price process's scale is
    **a choice** (general knowledge of the era, no frozen series read): ``mu_mean`` the typical inflation, ``noise``
    the typical shock, ``common_sd`` a factor every money shares (war, depression, oil), ``ref`` scales the
    hazard's covariates. ``described``: label -> how many of the changes the description counts."""
    panel: str
    n_monies: int
    first: int
    last: int
    change_first: int
    change_last: int
    n_changes: int
    described: dict[str, int]
    once: bool = True
    min_gap: int = 3
    mu_mean: float = 8.0
    mu_sd: float = 3.0
    gamma_mu: bool = True
    noise: float = 4.0
    proportional: bool = False
    common_sd: float = 2.0
    ref: float = 8.0


SHAPES: dict[str, Shape] = {
    # 1914: 35 candidates the list reads, 16 lines, 7 counted; prewar prices; a common war shock
    "1": Shape("1", 35, 1903, 1922, 1914, 1915, 16, {"1": 7}, once=True, mu_mean=1.5, mu_sd=2.0, gamma_mu=False,
               noise=3.0, common_sd=4.0, ref=4.0),
    # 1931-36: 24 rows, 17 lines, 15 counted; deflation and a depression shock
    "2": Shape("2", 24, 1920, 1946, 1931, 1936, 17, {"2": 15}, once=True, mu_mean=0.0, mu_sd=2.0, gamma_mu=False,
               noise=4.0, common_sd=4.0, ref=5.0),
    # Garriga: 195 monies, 1970-2023, 401 lines (up 272 and down 58 counted), several per money
    "3": Shape("3", 195, 1970, 2023, 1973, 2018, 401, {"3-up": 272, "3-down": 58}, once=False, min_gap=3, mu_mean=8.0,
               noise=4.2, proportional=True, common_sd=2.0, ref=8.0),
    # targeting: about 150 monies with a price index, 27 lines, 26 counted, adoptions 1989-2009
    "4": Shape("4", 150, 1980, 2020, 1989, 2009, 27, {"4": 26}, once=True, mu_mean=6.0, noise=3.5, proportional=True,
               common_sd=1.5, ref=6.0),
}

#: name -> (b_level, b_rise, b_fall, drift_sd[, b_same_level, b_same_rise]): how the timing of a change depends on the
#: price path, with no effect of the change. The first five are the first audit's own scenarios (sim_nonchangers.py),
#: kept; the last four are the window audit's O1 (section 15, W10): a hazard on the change year's own π(y) and on its
#: rise π(y) - π(y-1), each of both signs, which the match (it reads π(y-1) and the rise to y-1) does not control. The
#: same-year coefficients use the same scale as the others (0.12 and 0.15 per 8 points). A 4-tuple has none.
SCENARIOS: dict[str, tuple[float, ...]] = {
    "random timing": (0.0, 0.0, 0.0, 0.0),
    "after high pi": (0.12 * 8, 0.0, 0.0, 0.0),
    "after a rise (pressure)": (0.0, 0.15 * 8, 0.0, 0.0),
    "after a fall, with drift": (0.0, 0.0, 0.15 * 8, 0.6),
    "after high pi, with drift": (0.12 * 8, 0.0, 0.0, 0.6),
    "same year: high pi": (0.0, 0.0, 0.0, 0.0, 0.12 * 8, 0.0),
    "same year: low pi": (0.0, 0.0, 0.0, 0.0, -0.12 * 8, 0.0),
    "same year: a rise": (0.0, 0.0, 0.0, 0.0, 0.0, 0.15 * 8),
    "same year: a fall": (0.0, 0.0, 0.0, 0.0, 0.0, -0.15 * 8),
}
COMBOS = (("past", "level+rise"), ("written", "level+rise"), ("past", "level"), ("written", "level"))


def shapes_from_list(series_rows: list[dict]) -> dict[str, Shape]:
    """:data:`SHAPES` with the change counts and years of the committed list (dates and statuses only, no value)."""
    out = {p: Shape(**{**s.__dict__, "described": dict(s.described)}) for p, s in SHAPES.items()}
    for reading_panel, routes in HEADLINE_ROUTES.items():
        rows = [r for r in series_rows if r["route"] in routes]
        if not rows:
            continue
        years = [int(r["entry_date"][:4]) for r in rows]
        shape = out[reading_panel]
        shape.n_changes = len(rows)
        shape.change_first, shape.change_last = min(years), max(years)
        shape.first = min(shape.first, shape.change_first - 6)
        shape.last = max(shape.last, shape.change_last + 6)
        if reading_panel == "3":
            shape.described = {"3-up": sum(r["route"] == "a3-up" and r["status"] == "counted" for r in rows),
                               "3-down": sum(r["route"] == "a3-down" and r["status"] == "counted" for r in rows)}
        else:
            shape.described = {reading_panel: sum(r["status"] == "counted" for r in rows)}
    return out


def _expected(alpha: float, z: np.ndarray, eligible: np.ndarray, once: bool) -> float:
    p = np.where(eligible, 1 / (1 + np.exp(-(alpha + z))), 0.0)
    return float((1 - np.prod(1 - p, axis=1)).sum()) if once else float(p.sum())


def simulate(rng: np.random.Generator, shape: Shape, scenario: tuple[float, ...]):
    """One synthetic panel under **no effect** of any change: π(y) by money and year, and each money's change years.
    The changes' timing depends on the price path as the scenario says (on π(y-1) and π(y-3), and, W10, on the change
    year's own π(y)) and is calibrated to the shape's count."""
    b_level, b_rise, b_fall, drift_sd, *same = scenario
    b_same_level, b_same_rise = (list(same) + [0.0, 0.0])[:2]
    n, T, burn = shape.n_monies, shape.last - shape.first + 1, 30
    mu = rng.gamma(2.0, shape.mu_mean / 2, n) if shape.gamma_mu else rng.normal(shape.mu_mean, shape.mu_sd, n)
    sig = (shape.noise * (0.5 + 0.5 * np.abs(mu) / max(shape.mu_mean, 1.0)) if shape.proportional
           else np.full(n, shape.noise))
    a, d, c = np.zeros(n), np.zeros(n), 0.0
    pi = np.empty((n, burn + T))
    for t in range(burn + T):
        a = 0.6 * a + sig * rng.standard_normal(n)
        d = d + drift_sd * rng.standard_normal(n)
        c = 0.5 * c + shape.common_sd * rng.standard_normal()
        pi[:, t] = mu + d + a + c
    pi = pi[:, burn:]
    z = np.zeros((n, T))
    eligible = np.zeros((n, T), bool)
    for t in range(max(3, shape.change_first - shape.first), min(T, shape.change_last - shape.first + 1)):
        z[:, t] = (b_level * (pi[:, t - 1] - shape.mu_mean) + b_rise * (pi[:, t - 1] - pi[:, t - 3])
                   + b_fall * (pi[:, t - 3] - pi[:, t - 1])
                   + b_same_level * (pi[:, t] - shape.mu_mean) + b_same_rise * (pi[:, t] - pi[:, t - 1])) / shape.ref
        eligible[:, t] = True
    lo, hi = -15.0, 6.0
    for _ in range(45):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _expected(mid, z, eligible, shape.once) < shape.n_changes else (lo, mid)
    p = np.where(eligible, 1 / (1 + np.exp(-((lo + hi) / 2 + z))), 0.0)
    hit = rng.random((n, T)) < p
    years: list[list[int]] = [[] for _ in range(n)]
    if shape.once:
        for j in np.nonzero(hit.any(axis=1))[0]:
            years[j].append(shape.first + int(hit[j].argmax()))
    else:
        last = np.full(n, -99)
        for t in range(T):
            h = hit[:, t] & (t - last >= shape.min_gap)
            for j in np.nonzero(h)[0]:
                years[j].append(shape.first + t)
            last[h] = t
    return pi, years


def synthetic_panel_data(shape: Shape, pi: np.ndarray, years: list[list[int]]) -> PanelData:
    n, T = pi.shape
    return PanelData([f"S{j:03d}" for j in range(n)], shape.first, shape.last, pi, np.ones((n, T), bool),
                     np.zeros((n, T), np.int8), np.ones((n, T), np.int8), years,
                     [[y * 12 for y in ys] for ys in years])


def null_band(seed: int = SEED, runs: int = SCENARIO_RUNS, shapes: dict[str, Shape] | None = None,
              scenarios: dict[str, tuple] | None = None, combos=COMBOS, progress: Callable[[str], None] | None = None,
              panels: tuple[str, ...] | None = None, keep_gaps: dict | None = None) -> list[dict]:
    """The band the described gap takes **under no effect**, with the same :func:`pool` and :func:`match` as the real
    build, on synthetic panels shaped like each real one. No file and no real series is read: callable alone.

    Per panel label, scenario and (pool, match) combination, over ``runs`` synthetic panels: the gap's mean over
    the described changes of each run, then the mean, the spread and the 2.5 to 97.5 percentile band of that mean
    over the runs (``lo``, ``hi``), ``sd_single`` (the spread of one change's gap), the share of described changes
    that found a gap, and the share of runs whose mean lies beyond +-1 point. The headline is (past, level+rise);
    the others are the variants the audit's O1 names. These rows are at the list's counted n; ``keep_gaps``, if a dict
    is given, is filled with every run's gaps by (panel, scenario, pool, match), so that :func:`band_at_n` can give the
    band at any description line's own n (W10) without simulating again."""
    shapes = SHAPES if shapes is None else shapes
    scenarios = SCENARIOS if scenarios is None else scenarios
    keys = [k for k in shapes if panels is None or k in panels]
    rows: list[dict] = []
    for si, key in enumerate(keys):
        shape = shapes[key]
        for ci, (scenario, params) in enumerate(scenarios.items()):
            means: dict[tuple, list[float]] = defaultdict(list)
            singles: dict[tuple, list[float]] = defaultdict(list)
            found: dict[tuple, list[float]] = defaultdict(list)
            counts: list[int] = []
            for run in range(runs):
                rng = np.random.default_rng([seed, si, ci, run])
                pi, years = simulate(rng, shape, params)
                pd = synthetic_panel_data(shape, pi, years)
                changes = sorted((y, j) for j, ys in enumerate(years) for y in ys
                                 if y - 3 >= shape.first and y + 5 <= shape.last)
                counts.append(len(changes))
                subsets = {label: (rng.choice(len(changes), size=min(n, len(changes)), replace=False)
                                   if changes else np.array([], int)) for label, n in shape.described.items()}
                for pool_rule, on in combos:
                    gaps = []
                    for y, j in changes:
                        cand, flags = pool(pd, j, y, rule=pool_rule)
                        found_m = match(pd, j, y, cand, flags, key=f"{seed}|{si}|{ci}|{run}|{j}|{y}", on=on)
                        gaps.append(described_gap(pd, j, y, y + 6, found_m)["gap"])
                    gaps = np.array(gaps)
                    if keep_gaps is not None:
                        keep_gaps.setdefault((key, scenario, pool_rule, on), []).append(gaps)
                    for label, pick in subsets.items():
                        g = gaps[pick] if len(pick) else np.array([])
                        ok = g[~np.isnan(g)]
                        means[(label, pool_rule, on)].append(float(ok.mean()) if len(ok) else float("nan"))
                        singles[(label, pool_rule, on)].append(float(ok.std()) if len(ok) > 1 else float("nan"))
                        found[(label, pool_rule, on)].append(len(ok) / len(g) if len(g) else float("nan"))
            for (label, pool_rule, on), v in means.items():
                v = np.array(v)
                v = v[~np.isnan(v)]
                lo_se, hi_se = edge_se(v)
                rows.append({
                    "panel": key, "label": label, "scenario": scenario, "pool": pool_rule, "match": on, "runs": len(v),
                    "n_changes": round(float(np.mean(counts)), 1), "n_described": shape.described[label],
                    "share_matched": round(float(np.nanmean(found[(label, pool_rule, on)])), 3),
                    "mean": round(float(v.mean()), 3) if len(v) else "",
                    "sd_runs": round(float(v.std()), 3) if len(v) else "",
                    "lo": round(float(np.percentile(v, 2.5)), 3) if len(v) else "", "lo_se": _se(lo_se),
                    "hi": round(float(np.percentile(v, 97.5)), 3) if len(v) else "", "hi_se": _se(hi_se),
                    "sd_single": round(float(np.nanmean(singles[(label, pool_rule, on)])), 3),
                    "share_beyond_1": round(float(np.mean(np.abs(v) > 1)), 3) if len(v) else "", "reading": "", "line": ""})
            if progress:
                progress(f"panel {key}, {scenario}: {runs} runs")
    return rows


def band_at_n(keep_gaps: dict, label: str, n: int, *, reading: str = "", line: str = "", seed: int = SEED,
              combos=(("past", "level+rise"),)) -> list[dict]:
    """The scenarios' band at **n changes with a gap** (W10): per scenario, for each simulated run, ``n`` of the changes
    that found a gap are drawn (seeded by the label, the scenario and n), their mean taken, and the 2.5 to 97.5
    percentile band of those means over the runs given. ``keep_gaps`` is what :func:`null_band` filled. A run with fewer
    than ``n`` gaps gives the mean of those it has. Rows have the band's fields, ``reading`` and ``line`` set; their
    ``n_described`` is ``n``. Nothing real is read: the n is a count taken from the build."""
    panel = label.split("-")[0]
    rows = []
    for (key, scenario, pool_rule, on), runs in keep_gaps.items():
        if key != panel or (pool_rule, on) not in combos:
            continue
        rng = np.random.default_rng([seed, 5, zlib.crc32(f"{label}|{scenario}|{n}".encode())])
        means, singles, share = [], [], []
        for gaps in runs:
            ok = gaps[~np.isnan(gaps)]
            share.append(len(ok) / len(gaps) if len(gaps) else float("nan"))
            if len(ok) == 0 or n < 1:
                continue
            g = ok[rng.choice(len(ok), size=min(n, len(ok)), replace=False)]
            means.append(float(g.mean()))
            singles.append(float(g.std()) if len(g) > 1 else float("nan"))
        v = np.array(means)
        lo_se, hi_se = edge_se(v)
        rows.append({"panel": key, "label": label, "scenario": scenario, "pool": pool_rule, "match": on, "runs": len(v),
                     "n_changes": round(float(np.mean([len(g) for g in runs])), 1), "n_described": n,
                     "share_matched": round(float(np.nanmean(share)), 3),
                     "mean": round(float(v.mean()), 3) if len(v) else "",
                     "sd_runs": round(float(v.std()), 3) if len(v) else "",
                     "lo": round(float(np.percentile(v, 2.5)), 3) if len(v) else "", "lo_se": _se(lo_se),
                     "hi": round(float(np.percentile(v, 97.5)), 3) if len(v) else "", "hi_se": _se(hi_se),
                     "sd_single": round(float(np.nanmean(singles)), 3) if len(v) and not np.isnan(singles).all() else "",
                     "share_beyond_1": round(float(np.mean(np.abs(v) > 1)), 3) if len(v) else "",
                     "reading": reading, "line": line})
    return rows


# --- the placebo band (sections 15 and 16; W11, W18, W19) ---------------------------------------------------------------------

class PlaceboCell(NamedTuple):
    """One pseudo-change that found a gap: money index, year, the described gap, π(y-1), and whether its own path was cut
    (at its own or its union's later change, an entry into a union, or where its source stops covering it)."""
    j: int
    y: int
    gap: float
    pi_before: float
    cut: bool


def placebo_cells(pd: PanelData, y_lo: int, y_hi: int, *, design: str = "headline", annual_end: int | None = None,
                  key: str = "placebo", **pool_options) -> list[PlaceboCell]:
    """Every pseudo-change the panel allows, with its described gap (W19). Each money-year (money j, year y in ``y_lo``..
    ``y_hi``) runs through the same :func:`pool`, :func:`match` and :func:`described_gap` as a real change; the cells with
    no gap (no comparator, no path) are left out. Cells come in (year, money) order.

    ``design="headline"``: j is eligible by the pool's own past-only rule: no change of the panel (its union's included) in
    y-3..y, the source covering it over those years; its **own path is cut** at its own later change (or its union's, or its
    entry into a union) or where its source stops covering it, as a comparator's is (:func:`path_end`, W3), and the cell is
    flagged ``cut``. ``design="future-clean"`` (the variant): the first build's rule, no change in y-3..y+5 and the source
    covering it through y+5, the path uncut to y+5. Always: π readable in y-3 and y-1, no war year in y, a money in the euro
    or in XOF, XAF or XCD in y is that union's, never a pseudo-change of its own (W21), y+5 inside the panel and the common end."""
    if design not in ("headline", "future-clean"):
        raise ValueError(design)
    out = []
    for y in range(y_lo, y_hi + 1):
        if y - 3 < pd.first or y + 5 > pd.last or (annual_end is not None and y + 5 > annual_end):
            continue
        c1, c3, cy = pd.col(y - 1), pd.col(y - 3), pd.col(y)
        hi = y if design == "headline" else y + 5
        ok = pd.free_of_changes(y - 3, hi) & pd.covered_over(y - 3, hi) & (pd.war[:, cy] != 1)
        ok &= ~np.isnan(pd.pi[:, c1]) & ~np.isnan(pd.pi[:, c3]) & ~pd.in_euro(y) & ~pd.in_union(y)    # a union's money (W21)
        for j in np.nonzero(ok)[0]:
            cand, flags = pool(pd, int(j), y, **pool_options)
            found = match(pd, int(j), y, cand, flags, key=f"{key}|{pd.monies[j]}|{y}")
            end, why = path_end(pd, int(j), y) if design == "headline" else (y + 6, "")
            gap = described_gap(pd, int(j), y, end, found)["gap"]
            if not math.isnan(gap):
                out.append(PlaceboCell(int(j), y, gap, pd.pi_at(int(j), y - 1), bool(why)))
    return out


def placebo_gaps(pd: PanelData, y_lo: int, y_hi: int, *, design: str = "headline", annual_end: int | None = None,
                 key: str = "placebo", **pool_options) -> np.ndarray:
    """The gaps of :func:`placebo_cells`, in (year, money) order."""
    return np.array([c.gap for c in placebo_cells(pd, y_lo, y_hi, design=design, annual_end=annual_end, key=key,
                                                   **pool_options)])


def _digest_seed(*parts) -> int:
    """W18: a generator's seed from sha256 of its parts, never from a display name."""
    return int.from_bytes(hashlib.sha256("|".join(str(p) for p in parts).encode()).digest()[:8], "big")


def subset_means(gaps: np.ndarray, k: int, draws: int, rng: np.random.Generator) -> np.ndarray:
    """The mean of ``k`` gaps drawn without replacement, ``draws`` times (W11)."""
    return np.array([float(gaps[rng.choice(len(gaps), size=k, replace=False)].mean()) for _ in range(draws)])


def stratum(cells: list[PlaceboCell], year: int, pi_before: float, *, years: int = PLACEBO_STRATUM_YEARS,
            caliper: float = CALIPER) -> list[PlaceboCell]:
    """W19: the eligible money-years within ``years`` of a real change's year and with π(y-1) within the ``caliper`` of the
    change's own π(y-1)."""
    return [c for c in cells if abs(c.y - year) <= years and abs(c.pi_before - pi_before) <= caliper]


def stratified_means(cells: list[PlaceboCell], real: list[tuple[int, float]], draws: int, rng: np.random.Generator
                     ) -> tuple[np.ndarray, int, int, dict]:
    """W19: per draw, **one pseudo-change per real change** (``real``: year and π(y-1) of each), drawn uniformly in its
    stratum; the mean of those gaps. Returns the means, the real changes used, those with an empty stratum (left out), and
    the distinct cells the strata hold, by (money, year). The draws of different changes are independent."""
    columns, distinct = [], {}
    empty = 0
    ys = np.array([c.y for c in cells])
    pis = np.array([c.pi_before for c in cells])
    gaps_all = np.array([c.gap for c in cells])
    for year, pi_before in real:                       # the same test as :func:`stratum`, on arrays
        idx = np.nonzero((np.abs(ys - year) <= PLACEBO_STRATUM_YEARS) & (np.abs(pis - pi_before) <= CALIPER))[0]
        if len(idx) == 0:
            empty += 1
            continue
        columns.append(gaps_all[idx][rng.integers(0, len(idx), size=draws)])
        distinct.update({int(i): cells[int(i)] for i in idx})
    if not columns:
        return np.array([]), 0, empty, {}
    return np.mean(np.array(columns), axis=0), len(columns), empty, distinct


def stratum_sizes(cells: list[PlaceboCell], real: list[tuple[int, float]]) -> list[int]:
    """W25 (section 18, P7): the number of eligible cells in the stratum of each real change that has one (the empty strata,
    which :func:`stratified_means` leaves out, are not listed). A stratum can hold the real changer's own earlier
    money-years, cut at its change (W19)."""
    ys = np.array([c.y for c in cells])
    pis = np.array([c.pi_before for c in cells])
    sizes = [int(((np.abs(ys - year) <= PLACEBO_STRATUM_YEARS) & (np.abs(pis - pi_before) <= CALIPER)).sum())
             for year, pi_before in real]
    return [n for n in sizes if n]


def _cut_stats(cells: list[PlaceboCell]) -> dict:
    """``cut`` (how many of the cells have their own path cut), ``cut_mean`` and ``uncut_mean`` (the mean gap of those and of
    the others, '' where there are none): the whole difference between the headline placebo and ``future-clean`` (W25, P3)."""
    cut = [c.gap for c in cells if c.cut]
    uncut = [c.gap for c in cells if not c.cut]
    return {"cut": len(cut), "cut_mean": round(float(np.mean(cut)), 3) if cut else "",
            "uncut_mean": round(float(np.mean(uncut)), 3) if uncut else ""}


def placebo_band(readers: "Readers", series_rows: list[dict], members_rows: list[dict], coverage_rows: list[dict],
                 ns: dict[tuple[str, str, str], int], *, draws: int = PLACEBO_DRAWS, seed: int = SEED,
                 lines: dict[tuple[str, str, str], list[tuple[int, float]]] | None = None,
                 designs: tuple[str, ...] = PLACEBO_DESIGNS) -> list[dict]:
    """The placebo band (W11, W18, W19): the mean described gap of ``n`` pseudo-changes drawn at random among the real
    non-changers of the panel, over ``draws`` draws (:data:`PLACEBO_DRAWS`), **seeded by sha256 of (seed, design, reading,
    label, n) and never by the line's name**, so two lines with the same n get the same band. ``ns``: (reading, label,
    line) -> n, the lines with a gap of each description (:func:`description_lines`). Three designs, one row each per line
    (``design`` column): ``headline`` (past-only eligibility, own path cut: W19), ``stratified`` (one pseudo-change per
    real change, among the eligible money-years within +-3 years and the caliper of its π(y-1); needs ``lines``:
    (reading, label, line) -> the (year, π(y-1)) of each real change with a gap) and the variant ``future-clean``. Each row
    has its edges' standard error (:func:`edge_se`, W24), the cut cells' count and mean gap and the uncut ones' (W25) and, for the
    stratified design, its smallest stratum (W25, P7). **A placebo of fewer than** :data:`PLACEBO_MIN_CELLS`
    **cells cannot be read as a band**, and its ``note`` says so. **It needs the readers** (the real panel's π), so the build
    runs it after they are made; it needs no chosen price process. Rows: ``PLACEBO_FIELDS``."""
    rows: list[dict] = []
    by_reading: dict[str, list[tuple[str, str, int]]] = defaultdict(list)
    for (reading, label, line), n in ns.items():
        by_reading[reading].append((label, line, n))
    for reading, wanted in sorted(by_reading.items()):
        changes = load_changes(series_rows, reading)
        for panel in sorted({label.split("-")[0] for label, _, _ in wanted}):
            of_panel = [c for c in changes if c.panel == panel]
            if not of_panel:
                continue
            pd = panel_data(panel, of_panel, readers, members_rows, coverage_rows)
            span = (min(c.year for c in of_panel), max(c.year for c in of_panel))
            wide = placebo_cells(pd, span[0] - PLACEBO_STRATUM_YEARS, span[1] + PLACEBO_STRATUM_YEARS, design="headline",
                                 annual_end=readers.annual_end, key=f"placebo|{reading}") if (
                "headline" in designs or "stratified" in designs) else []
            cells = {"headline": [c for c in wide if span[0] <= c.y <= span[1]], "stratified": wide}
            if "future-clean" in designs:
                cells["future-clean"] = placebo_cells(pd, span[0], span[1], design="future-clean",
                                                      annual_end=readers.annual_end, key=f"placebo|{reading}")
            memo: dict[tuple, tuple] = {}
            for label, line, n in sorted(wanted):
                if label.split("-")[0] != panel:
                    continue
                for design in designs:
                    if design == "stratified" and lines is None:
                        continue
                    real = sorted(lines.get((reading, label, line), [])) if design == "stratified" else []
                    key = (design, label, n, tuple(real))
                    if key not in memo:
                        memo[key] = _placebo_numbers(design, cells[design], reading, label, n, real, draws, seed)
                    rows.append({"reading": reading, "panel": panel, "label": label, "design": design, "line": line,
                                 **memo[key]})
    return rows


def _placebo_numbers(design: str, cells: list[PlaceboCell], reading: str, label: str, n: int,
                 real: list[tuple[int, float]], draws: int, seed: int) -> dict:
    """One placebo row's numbers (:func:`placebo_band`)."""
    blank = {"n": 0, "draws": draws, "cells": len(cells), **_cut_stats(cells), "min_stratum": "", "mean": "", "sd_draws": "",
             "lo": "", "lo_se": "", "hi": "", "hi_se": "", "sd_single": "", "share_beyond_1": "", "note": ""}
    gaps = np.array([c.gap for c in cells])
    if len(gaps) == 0 or n < 1:
        return {**blank, "note": "no pseudo-change has a gap" if n else "the line has no gap"}
    rng = np.random.default_rng(_digest_seed(seed, design, reading, label, n, *(f"{y}:{p:.6g}" for y, p in real)))
    notes = []
    if design == "stratified":
        means, used, empty, distinct = stratified_means(cells, real, draws, rng)
        if used == 0:
            return {**blank, "note": "no real change has a pseudo-change in its stratum"}
        shown = {"n": used, "cells": len(distinct), **_cut_stats(list(distinct.values())),
                 "min_stratum": min(stratum_sizes(cells, real))}
        if empty:
            notes.append(f"{empty} of {len(real)} real changes have no eligible money-year in their stratum and are left out")
        sd_single = float(np.std(np.array([c.gap for c in distinct.values()])))
    else:
        k = min(n, len(gaps))
        means = subset_means(gaps, k, draws, rng)
        shown = {"n": k, "cells": len(cells), **_cut_stats(cells)}
        sd_single = float(gaps.std())
        if k != n:
            notes.append(f"fewer pseudo-changes with a gap ({len(gaps)}) than the line's n ({n})")
    if shown["cells"] < PLACEBO_MIN_CELLS:
        notes.insert(0, f"cannot be read as a band: {shown['cells']} cells, fewer than {PLACEBO_MIN_CELLS}")
    lo_se, hi_se = edge_se(means)
    return {**blank, **shown, "mean": round(float(means.mean()), 3), "sd_draws": round(float(means.std()), 3),
            "lo": round(float(np.percentile(means, 2.5)), 3), "lo_se": _se(lo_se),
            "hi": round(float(np.percentile(means, 97.5)), 3), "hi_se": _se(hi_se), "sd_single": round(sd_single, 3),
            "share_beyond_1": round(float(np.mean(np.abs(means) > 1)), 3), "note": "; ".join(notes)}


def format_band(rows: list[dict]) -> str:
    """The band as a table, headline combination first, for printing before any real window is read. It is the band at
    the list's counted n; a line's own band (``line`` set) is :func:`band_at_n`'s and is not printed here."""
    rows = [r for r in rows if not r.get("line")]
    out = ["The null band: the described gap (the change's after-minus-before in π, less its matched comparators')",
           "under NO effect of any change, on synthetic panels shaped like each real one; π in points.",
           "Headline: pool 'past' (no change in y-3..y), match on π(y-1) and on the change in π (caliper 3).",
           "Variants: pool 'written' (none in y-3..y+3); match on the level alone (P28 as first written).", ""]
    out[4:4] = ["Each band edge is followed by its standard error (se): the sd of the edge over 20 batches of the runs, over sqrt(20)."]
    head = f"{'panel':6s} {'scenario':26s} {'pool':8s} {'match':11s} {'n':>4s} {'mean':>7s} {'band lo':>8s} {'se':>5s} " \
           f"{'band hi':>8s} {'se':>5s} {'sd/chg':>7s} {'matched':>8s} {'>|1|':>5s}"
    out.append(head)
    for r in sorted(rows, key=lambda r: (r["label"], (r["pool"], r["match"]) != ("past", "level+rise"),
                                         r["pool"], r["match"], r["scenario"])):
        err = lambda k: f"{float(r[k]):>5.2f}" if r.get(k, "") != "" else f"{'n/a':>5s}"  # noqa: E731
        out.append(f"{r['label']:6s} {r['scenario']:26s} {r['pool']:8s} {r['match']:11s} {r['n_described']:>4d} "
                   f"{float(r['mean']):>+7.2f} {float(r['lo']):>+8.2f} {err('lo_se')} {float(r['hi']):>+8.2f} {err('hi_se')} "
                   f"{float(r['sd_single']):>7.2f} {float(r['share_matched']):>8.2f} {float(r['share_beyond_1']):>5.2f}")
    out.append("")
    for label in sorted({r["label"] for r in rows}):
        out.append(f"panel {label}: headline band over every scenario {envelope(rows, label)}; "
                   f"level-only match, written pool {envelope(rows, label, 'written', 'level')}")
    return "\n".join(out)


# --- the output: data/reconstructed/ft001-a-window/ --------------------------------------------------------------------------

NEEDS = [
    "Dollarisation: no open series (FT-001-M3-sources.md, 'Not found'); the IMF's Financial Soundness Indicators "
    "FSDFCD (foreign-currency liabilities to total liabilities) is named there, not frozen.",
    "Panel 4's candidates from 2012: the AREAER is frozen and its inflation-targeting column is coded in "
    "data/reconstructed/ft001-a-areaer/; the announcements are read (section 17: four adopters, twelve candidates that cannot be "
    "read); what is still needed is, for each of those twelve, its central bank's own announcement, frozen (P21). Until then a "
    "candidate that cannot be read is covered only through Y - 2, Y the first edition that lists it, and panel 4 covers every "
    "other money through 2022 (W5, section 19). Paraguay's 2011 adoption is listed nowhere (a gap of the pre-2012 list): it is "
    "uncovered from 2011.",
    "The entry and exit years of XOF, XAF and XCD's members as their union's money (W21, W28): the four of Mali 1984, "
    "Guinea-Bissau 1997, Equatorial Guinea 1985 and Mauritania to 1972 are Garriga's `regional` flag's (frozen, read by "
    "frame_a.py); what is still needed is a frozen source for the XCD members' years (the EC dollar dates from 1965, "
    "Grenada 1968; her flag starts in 1983) and for Barbados (the EC dollar to 1973, not in frame_a's unions: nothing moves).",
    "Foreign exchange for the run test (section 15, O3): the Bank of England's, the Bank of France's and the "
    "Reichsbank's balance sheets, BMS 1914-1941 tables 164, 165 and 167, to parse and build as a variant (gold and "
    "foreign exchange); until then a \"no\" of the run test is \"no (gold only)\" (W13).",
]


def run_grid_moves(change_rows: list[dict]) -> list[str]:
    """The headline lines whose run verdict is not the same at 10%, 20% and 30% (W12), as text."""
    out = []
    for r in change_rows:
        if r["variant"] != "headline" or r["run_test"] == "n/a":
            continue
        if r["run_10"] != r["run_test"] or r["run_30"] != r["run_test"]:
            out.append(f"{r['reading']} {r['route']} {r['money']} {r['entry_date']}: at 20% {r['run_test']}, at 10% "
                       f"{r['run_10']}, at 30% {r['run_30']}")
    return out


def units_suspect_split(series_rows: list[dict]) -> dict[str, int]:
    """W26 (section 18, P5): the deposits-to-GDP rows flagged ``units_suspect``, **by reason**: ``any``; ``band`` (deposits to GDP
    outside 1-300%); ``seam`` (the World Bank segment of a GDP whose seam is beyond a factor of 2); ``both`` (in each); and the
    rows carrying a ``units break`` flag. ``any`` is ``band + seam - both``; the third build printed ``any`` as "outside 1-300%"."""
    rows = [r["note"] for r in series_rows if r["measure"] == "deposits_to_gdp"]
    band = [("units_suspect: deposits to GDP" in n) for n in rows]
    seam = [("units_suspect: GDP seam" in n) for n in rows]
    return {"any": sum("units_suspect" in n for n in rows), "band": sum(band), "seam": sum(seam),
            "both": sum(a and b for a, b in zip(band, seam)), "units_break": sum("units break" in n for n in rows)}


def robustness_notes(change_rows: list[dict]) -> list[str]:
    """W29 (section 18, P9): for each reading's and panel's counted line with a gap: its mean, its **median**, the line that moves
    the mean most (the largest |gap - mean|) and the extreme line on the other side (the lowest gap if the first is the highest,
    else the highest), each with the comparators it rests on and **the mean without it**, and how many of the lines rest on a
    single comparator. (3-up on the third build: -0.27, +0.08 without ESP 1980, whose one comparator gives -48.1; median -0.54.
    From the fourth build BGR 1991, +70.6, moves it most, so both are named: the fifth build's small re-check, B2.) Descriptive:
    it says what the mean rests on and gives no verdict."""
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in change_rows:
        if r["variant"] == "headline" and r["status"] == "counted" and r["gap"] != "":
            groups[(r["reading"], _label(r))].append(r)
    out = []
    for (reading, label), rows in sorted(groups.items()):
        gaps = np.array([float(r["gap"]) for r in rows])
        mean = float(gaps.mean())
        text = f"{reading} panel {label} (counted, n = {len(rows)}): mean gap {mean:+.2f}, median {float(np.median(gaps)):+.2f}"
        if len(rows) > 1:
            first = int(np.argmax(np.abs(gaps - mean)))
            other = int(np.argmin(gaps)) if first == int(np.argmax(gaps)) else int(np.argmax(gaps))
            for k in (first, other) if other != first else (first,):
                r = rows[k]
                used = str(r.get("used", ""))
                rests = f", {used} comparator{'' if used == '1' else 's'}" if used else ""
                text += (f"; without {r.get('money', '?')} {r.get('entry_date', '?')} (gap {gaps[k]:+.1f}{rests}) the mean is "
                         f"{float(np.delete(gaps, k).mean()):+.2f}")
        single = sum(1 for r in rows if str(r.get("used", "")) == "1")
        out.append(text + f"; {single} of the {len(rows)} lines rest on a single comparator")
    return out


def manifest_text(*, sha: str = "", code_commit: str = "", band_rows: list[dict] | None = None,
                  result: Result | None = None, described: list[str] | None = None,
                  placebo_rows: list[dict] | None = None) -> str:
    """``MANIFEST.md``: the skeleton, with the counts and the band filled where the build has them. ``code_commit``:
    the commit of the code that built it; the protocol's two commits are :data:`PROTOCOL_COMMITS` (M1)."""
    counts = ["The build fills the counts when it runs; none yet."]
    moves = ["The build names the lines whose run verdict moves at 10% or 30% when it runs; none yet."]
    if result is not None:
        by = Counter((r["reading"], r["variant"], r["panel"], r["status"]) for r in result.changes)
        counts = [f"- {reading} / {variant} / panel {panel}: {status} {n}"
                  for (reading, variant, panel, status), n in sorted(by.items()) if variant == "headline"]
        unread = Counter(u["reason"].split(":")[0] for u in result.unread)
        counts += ["- rows read: %d; rows unread: %d (by reason: %s)" % (
            len(result.series), len(result.unread), "; ".join(f"{k} {v}" for k, v in unread.most_common(8)) or "none")]
        split = units_suspect_split(result.series)
        counts.append("- deposits-to-GDP rows flagged units_suspect: %d, by reason: outside 1-300%%: %d; GDP seam (the World Bank "
                      "segment): %d; both: %d (the first is the second plus the third less the fourth); with a units break "
                      "flagged: %d" % (split["any"], split["band"], split["seam"], split["both"], split["units_break"]))
        reuse = Counter()
        for r in result.matches:
            if r["variant"] == "headline" and r["comparator"]:
                reuse[r["comparator"]] = max(reuse[r["comparator"]], int(r["reuse"]))
        if reuse:
            counts.append("- comparators most reused **within one panel** (headline; a comparator's reuse is counted per panel and "
                          "reading, so the same money serves more lines across panels): "
                          + ", ".join(f"{m} {n}" for m, n in reuse.most_common(8)))
        counts += [f"- what a mean rests on (W29): {note}" for note in robustness_notes(result.changes)]
        grid = run_grid_moves(result.changes)
        moves = ([f"- the run test's verdict moves with the threshold on {len(grid)} lines (it never moves a status; the "
                  "status is the headline's 20%):"] + [f"  - {g}" for g in grid]) if grid else [
            "- the run test's verdict does not move at 10% or 30% on any line."]
    band = format_band(band_rows) if band_rows else "The null band is written by the build before any window is read."
    protocol = "; ".join(f"{name} commit `{commit}`" for name, commit in PROTOCOL_COMMITS)
    placebo = ("The placebo band is written by the build after the readers are made (`placebo-band.csv`)." if placebo_rows is None
               else f"{len(placebo_rows)} rows in `placebo-band.csv`.")
    first_seen, second_seen, third_seen = WINDOWS_SEEN[0][1], WINDOWS_SEEN[1][1], WINDOWS_SEEN[2][1]
    return f"""# ft001-a-window — reconstructed dataset

Frame a's window build (FT-001, mission M4, second part): for each change of `data/reconstructed/ft001-a/` (read,
never edited), value and trust from 3 years before to 5 years after (monthly -24 to +36 where the change is dated
to the month and monthly data exist), beside the same measures for its matched non-changers. It describes; it
counts nothing and gives no verdict (A2). Built by `bank/maps/FT-001/missions/code/window_a.py` after frame a's
list was committed. **The null band at the list's n, below, was printed before any window was read**; each line's
band at its own n and the placebo band are computed after, and say so.

**When the readings were written** (N6). The first build's rules (the pool, the match, the first null band) were written
before any window was read. Readings **W10 onward** (section 15: the same-year scenarios, the placebo band, gold only,
units, unions, statuses) were written **after the first build's windows (`{first_seen}`) had been seen**; readings **W18
onward and section 16's** (the placebo's design, its draws, the units of GDP, unions alike, the small items) were written
**after both the first build's and the second build's (`{second_seen}`) windows had been seen**; **W24 onward and section
18's** (1,000 runs, each edge's standard error and "at the edge", the three placebos placed, the units' remainder, Estonia
from 1929-01, the unions' source, the descriptive notes) **after the third build's (`{third_seen}`) windows had been seen as
well**. None changes the list `ft001-a`. The scenarios' hazards came from the deep audit; the placebo's design is the
producer's and was changed after the re-check had shown that its first design moved the bands. **The third build's commit
message summarised panel 4's placement as "outside the stratified placebo only"; it rested on the scenarios' seed (300
runs) and is withdrawn: only the placements printed below stand.**

## Sources

- Frame a's list (`series.csv`, `members.csv`, `coverage.csv`), read only: the changes, their statuses, the panels'
  coverage. Protocol: {protocol}. Code commit: {code_commit or "(written by the build)"}. M0 v4.2 rules hash: {sha or "(written by the build)"}.
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
   and is not set against the mean. {placebo}

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
  and an empty path contributes nothing (W3); the described gap (W4); panel 4 covers every money through 2022, a candidate from 2012 that cannot be read through Y - 2, Paraguay to 2010 (W5); deposits
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
- Not built: {"; ".join(f"{k} ({v[:60]}...)" for k, v in NOT_BUILT.items())}; deposits to GDP monthly (GDP is annual);
  deposits before 1950 (IFS begins then); the market split and every IFS series before their own first year.

## Uncertainty

{chr(10).join(counts)}

{chr(10).join(moves)}

- The described gap under no effect is not zero when the timing depends on the price path, and the real panel's spread
  is not the synthetic one: the bands say by how much, and a mean inside them is consistent with no effect (never "told
  as no effect": W23).
- Comparators' reuse is counted in `matches.csv` (`reuse`, `reuse_counted`).

{chr(10).join(f"- {d}" for d in (described or []))}

## Needs

{chr(10).join(f"- {n}" for n in NEEDS)}

## The null band

At the list's counted n; each description line's band at its own n is in `null-band.csv` (rows with a `line`).

```
{band}
```
"""


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(out_dir: Path, result: Result | None, band_rows: list[dict], manifest: str, *,
                  overwrite: bool = False, placebo_rows: list[dict] | None = None) -> None:
    """``series.csv`` (what was read, in the reconstructed datasets' required columns), ``unread.csv``,
    ``changes.csv``, ``matches.csv``, ``null-band.csv``, ``placebo-band.csv`` (when ``placebo_rows`` is given),
    ``MANIFEST.md``. The null band and, before the readings, nothing else, are written when ``result`` is None."""
    out_dir = Path(out_dir)
    if not overwrite and (out_dir / "series.csv").exists():
        raise FileExistsError(f"{out_dir / 'series.csv'} exists: the window build is not run twice over one list")
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "null-band.csv", BAND_FIELDS, band_rows)
    if result is not None:
        write_csv(out_dir / "series.csv", SERIES_FIELDS, result.series)
        write_csv(out_dir / "unread.csv", UNREAD_FIELDS, result.unread)
        write_csv(out_dir / "changes.csv", CHANGE_FIELDS, result.changes)
        write_csv(out_dir / "matches.csv", MATCH_FIELDS, result.matches)
    if placebo_rows is not None:
        write_csv(out_dir / "placebo-band.csv", PLACEBO_FIELDS, placebo_rows)
    (out_dir / "MANIFEST.md").write_text(manifest)


def build_window(out_dir: Path, series_rows: list[dict], members_rows: list[dict], coverage_rows: list[dict],
                 readers: "Readers | Callable[[], Readers]", *, sha: str = "", code_commit: str = "",
                 band_rows: list[dict] | None = None, runs: int = SCENARIO_RUNS, print_fn: Callable[[str], None] = print,
                 reserves_at: Callable[[str, str], float | None] | None = None, overwrite: bool = False,
                 readings: tuple[str, ...] = ("headline", "a2-bj-note7", LATER_OR_TRANSITION_READING),
                 placebo_draws: int = PLACEBO_DRAWS) -> Result:
    """The whole build. **The null band (at the list's n) is run, printed and written first**; only then are the readers
    made (a factory is called after the band) and any real series read. The lists are read, never edited. After the
    readings: each description line's scenarios' band at its own n (:func:`band_at_n`, from the first run's gaps when the
    build ran it, W10) and the placebo band (:func:`placebo_band`, W11, W19: headline, stratified and future-clean, which
    needs the readers), both written."""
    out_dir = Path(out_dir)
    if not overwrite and (out_dir / "series.csv").exists():
        raise FileExistsError(f"{out_dir / 'series.csv'} exists")
    keep: dict | None = None
    if band_rows is None:
        keep = {}
        band_rows = null_band(runs=runs, shapes=shapes_from_list(series_rows), keep_gaps=keep)
    print_fn(format_band(band_rows))
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "null-band.csv", BAND_FIELDS, band_rows)
    rd = readers() if callable(readers) and not isinstance(readers, Readers) else readers
    result = Result()
    for reading in readings:
        part = build_reading(reading, series_rows, members_rows, coverage_rows, rd, sha=sha, reserves_at=reserves_at)
        result.changes += part.changes
        result.matches += part.matches
        result.series += part.series
        result.unread += part.unread
    lines = description_lines(result.changes)
    all_band = list(band_rows)
    if keep:
        for d in lines:
            if d["n_gap"]:
                all_band += band_at_n(keep, d["label"], d["n_gap"], reading=d["reading"], line=d["name"])
    placebo_rows = placebo_band(rd, series_rows, members_rows, coverage_rows,
                                {(d["reading"], d["label"], d["name"]): d["n_gap"] for d in lines},
                                draws=placebo_draws, lines=placebo_real_changes(result.changes))
    described = describe(result.changes, all_band, placebo_rows)
    for line in described:
        print_fn(line)
    write_outputs(out_dir, result, all_band, manifest_text(sha=sha, code_commit=code_commit, band_rows=band_rows,
                                                           result=result, described=described, placebo_rows=placebo_rows),
                  overwrite=True, placebo_rows=placebo_rows)
    return result


def frame_a_problems(folder: Path = FRAME_A) -> list[str]:
    """The window build reads frame a's list only once it is committed and unchanged (section 11)."""
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=folder, capture_output=True, text=True).stdout.strip()
    found = []
    for name in ("series.csv", "members.csv", "coverage.csv"):
        rel = (folder / name).resolve().relative_to(Path(top).resolve()).as_posix()
        if subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=top, capture_output=True).returncode != 0:
            found.append(f"{rel} is not committed")
        elif subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=top).returncode != 0:
            found.append(f"{rel} changed since its commit")
    return found


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("null-band", "build"):
        print(__doc__.split("**The pool")[0] + "\nUsage: window_a.py null-band [--runs N] [--list] | build --go [--overwrite]", file=sys.stderr)
        return 2
    runs = int(argv[argv.index("--runs") + 1]) if "--runs" in argv else SCENARIO_RUNS
    if argv[0] == "null-band":
        shapes = shapes_from_list(read_csv(FRAME_A / "series.csv")) if "--list" in argv else None
        rows = null_band(runs=runs, shapes=shapes, progress=lambda s: print(s, file=sys.stderr))
        print(format_band(rows))
        return 0
    if "--go" not in argv:
        print("build reads every real series: pass --go only when the session has committed this module first",
              file=sys.stderr)
        return 2
    import m0
    problems = frame_a_problems()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    sha = m0.require_locked()
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    build_window(OUT, read_csv(FRAME_A / "series.csv"), read_csv(FRAME_A / "members.csv"),
                 read_csv(FRAME_A / "coverage.csv"), panel_readers, sha=sha, code_commit=commit, runs=runs,
                 reserves_at=bms_reserves_at(), overwrite="--overwrite" in argv)   # a rebuild names it
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
