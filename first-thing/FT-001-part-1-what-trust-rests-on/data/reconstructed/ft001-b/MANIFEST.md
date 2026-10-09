# ft001-b — reconstructed dataset

FT-001's frame b: every break of a money's price level — π crossing 20%, M0 v4.2 section 5 b — one line each
in M0's case-line format, built by rule from the frozen sources under the coders' protocol
`bank/maps/FT-001/missions/FT-001-M3-panel.md` (committed alone, 77a730a, before any series was read). Every
line carries M0 v4.2's pair hash (`1160cab0bd84…e58d4`, commit 3163162). The list follows the acts list
(`ft001-acts`, as the twin's `case_line.follows` declares). **This is the second build** (2026-09-30): the
first (2ed0741) was audited deep and isolated (`bank/checks/FT-001-M3-panel-2026-09-30-opus-audit.md`: ready,
no B); the session's answers (`plan/e2-ft001.md`, Decisions, "Frame b's deep audit answered") were coded and
tested, the code committed alone (58bb80d), then this list rebuilt. What moved is under "The second build".
Frame c (`ft001-c`) reads this build.

## Sources

All at vintage 2026-09-30, read in M0's order (the twin's `common.source_order`), the first source that reads
a period giving its reading, never filled, scaled or spliced:

- **π, monthly**: IMF IFS through DBnomics, `dbnomics/IMF/IFS/M~~PCPI_IX`; the BIS's long consumer price
  series, `bis/WS_LONG_CPI` (FREQ M, unit 628, index).
- **π, annual**: IFS `A~~PCPI_IX`; the World Bank's `FP.CPI.TOTL.ZG` (its published rate; the euro area's
  `EMU` from 1999); Reinhart and Rogoff's inflation files (`reinhart-rogoff/inflation-{A-E,F-M,M-S,T-Z}`,
  the column headed "Reinhart and Rogoff", read by `missions/code/xls.py`); the BIS (FREQ A, 628);
  Jordà–Schularick–Taylor R6's `cpi`.
- **d, the onset's depreciation route**: IFS `ENDE_XDC_USD_RATE`, monthly and end of year, against the anchor
  of Ilzetzki–Reinhart–Rogoff's anchor file (`irr/anchor-currency-annual-1946-2016`, sheet Master) through the
  anchor's own IFS rate, else the dollar (protocol R11).
- **The regime and the market split, described on each line**: Ilzetzki–Reinhart–Rogoff's fine classes
  (`irr/classification-annual-1946-2016`, sheet Fine) and unified-market dummies
  (`irr/unified-market-annual-1946-2016`, sheets Unified and Master).
- Codes: `missions/code/economies.py` (additions only, marked "the panel").

## Steps

1. The protocol committed (77a730a); the code (`xls.py`, `panel.py`, `breaks.py`, `strain.py`,
   `economies.py`'s additions) and its tests (`test_panel.py`, 32 tests on synthetic series at the first
   build — the first manifest said 31: corrected, the audit's M10 — and `test_m0.py`) written and green
   **before any real series was read**. **O5, said**: at the first build the code, its tests and every list
   were committed together (2ed0741; `economies.py`'s panel additions went in c4a56ad), so git cannot date
   the readings (a)–(f) below, nor the post-count `rr_cpi_only` code, before the lists: only this manifest's
   word holds them. From the second build on, code and tests are committed before any build (58bb80d).
2. `panel.py` builds the panel in memory (not committed, R28): 215 monies with a code, 197 with a π reading;
   π12 per month and π(y) per year, each change from the first source reading both ends (R4); d per month and
   per year (R11); an IFS observation flagged `B` inside a change's span flags it (R5).
3. The common ends (R6), read literally: **monthly 2026-08, annual 2025**. See Uncertainty for the monthly one.
4. Each money's timeline (R3): years before its monthly span, months inside it (a year with no readable month
   read as a year), years after it, nothing past the common ends; from 1800 (the euro from 1999-01).
5. `breaks.py build`: the crossing (3 months at or above 20%, or a year read annually), restoration (24 months
   below 10%, dated at the last), the onset (π at 10% and d at 15%, runs through the crossing's period, begun
   within 36 months; the bound; *cannot be read*), the π-only onset beside, the statuses; the same for each
   grid variant (`variant-*.csv`).
   **Added afterwards**, on the session's decision after the headline's counts were seen: the variant
   `variant-rr-cpi-only.csv`, built alone (`breaks.py build --only rr-cpi-only`) with the same machinery; the
   headline and the other variants were not rebuilt.
6. `panel-coverage.csv` (per money, item and source: first and last period, number of readings) and
   `panel-seams.csv` (every change of source between consecutive readings: 513) written; the panel's digest,
   SHA-256 of its sorted readings: `d5debead680cb9d113ef0e3d8da10bf7c66e871e4136a350b896d76915b35d75`.
7. `m0.py list_problems` on `series.csv` and every variant (`rr-cpi-only` included): no problem; `ft.data.reconstructed.problems
   ("ft001-b")`: empty.
8. **The second build** (the audit's answers, code at 58bb80d; `breaks.py build`, which rebuilds the headline,
   every variant and `rr-cpi-only`): b10 as written (O4), the euro's changeovers (O3), the dollar's absent d
   route (M9), Reinhart–Rogoff's basis flags (M4) — each under Assumptions, with the moment it was chosen;
   `panel-coverage.csv` and `panel-seams.csv` rebuilt byte-identical, the digest unchanged. The source
   anomalies (M3) screened and listed under Uncertainty. `test_panel.py` 56 passed (with `test_m0.py` and
   frame a's `test_frame_a.py`, 106), `m0.py` and `reconstructed.problems` as in step 7.

## Assumptions

- **The readings of the protocol** used here: R1–R7, R11–R13, R15–R18 (R8–R10, R14, R19–R30 are frame c's).
- **`onset_date` is empty on frame b's lines; the onset is in `break_onset`** (R18). `route` = the onset's route.
- **Readings made in the code before any real series was read, not written in the protocol** (for the audit):
  (a) a crossing whose first reading follows an unreadable period is *apart*, "the crossing follows a gap" — it
  may have happened inside the gap (the protocol's b10 names only the record's start); (b) an unreadable period
  lying wholly before the bound leaves a run read as beginning after it — its date is then the bound's month
  or later; (c) an anchor whose issuer is the money itself is read as the dollar (Australia, Germany, the
  United Kingdom and Japan in some years); (d) on a tie between routes' starts, π before d; (e) at the monthly
  span's edges, the months of the edge year outside the span are not read (a run steps from the year before to
  the span's first month); (f) the change from annual to monthly readings is listed as a seam
  (`IFS-A -> IFS-M`).
- **Readings of the second build**, each chosen after the first build's lists and the audit were seen:
  (g) **b10 as written** (O4): a *stretch* is a run of consecutive readable periods; one that begins at or
  above the line — the record's first, or one after a gap — begins inside a break that cannot be dated, so the
  money's next crossing is *apart* with the reason of (a) or of the record's start; a stretch that begins
  between the lower line and the line flags the next crossing `stretch_begins` ("between the lower line and the
  line": it may continue an unrecorded break), the line counted. *The producer's reading*, tested: readings
  below the lower line adding up to 24 months before that next crossing (a restoration of the undated break)
  clear both. (h) **The euro's changeovers** (O3): a crossing of a member on or after its entry into the euro
  is *apart*, "a euro member after its changeover"; the entry years are frame a's `EURO_ENTRY` (the ECB's
  "Our money" page, frozen, 1074f44), imported by `breaks.py`, never copied. (i) **The dollar has no d route**
  (M9, R11): the United States' onset reads the π route alone; its d is absent, never "unreadable".
  (j) **Reinhart–Rogoff's basis, flagged from the "Based on" block** (M4), never a rule: `rr_basis_kind` —
  empty when every line covering the year names a CPI, "non-CPI basis" when none does, "mixed basis (CPI and
  non-CPI lines cover the year)" when both do (which one the compiled value follows is not said), "basis not
  stated for the year"; `rr_basis_seam` — the lines covering the crossing's year differ from the year
  before's (conservative: the end of an overlapping line raises it too). (k) **The source anomalies' screens**
  (M3), chosen after the audit named three: listed below, never swapped.
- **Not coded, said**: frame b's controls rule (b6) acts only on a market split or a premium as onset routes,
  neither of which is a headline route; the premium route and its variant have no series. The new-money rule is
  not applied (`new_money_rule: not applied`): no dated list of new units exists. Monies using another's
  money (the euro's unilateral users among them) are read economy by economy (R1), flagged
  `shared_or_foreign_money` from their lagged class 1. IFS's and the BIS's monthly readings alternate at series
  edges and for Ireland; where both read they differ by a median of 0.01 points (the audit's M5): said, kept.
- **Not read**: IFS areas that are groups, and `1C_355` (Curaçao and St Maarten: one series for two economies),
  `GF`, `GG`, `GP`, `JE`, `MQ`, `PM`, `RE` (no economy code); the BIS's own year-on-year series.

## Uncertainty

- **The list (second build)**: 501 headline lines in 156 monies — **445 counted**, 56 apart (40 "the record
  begins at or above the line", 13 "the crossing follows a gap", 3 "a euro member after its changeover");
  216 monthly, 285 annual; 472 restored, 29 not restored by the common end. **Not seen restored: the series
  stops** — 5 of the 29 are monies whose π record ends before 2025, the annual common end, with no restoration
  seen: Sudan (crossing 1972-11, record to 2023-02), Syria (2012-02; to 2019-12), Venezuela (1987; to 2016-12),
  Yemen (2008-03; to 2015-12), Zimbabwe (2018-10; to 2023-08). They keep the coding (M0 section 4: coded by
  what happened); "not restored" there means not seen restored. The other 24 run to 2025 or later.
- **The second build — what moved from the first** (headline): 4 statuses, 2 onsets, nothing else in any
  column the first build had. Serbia 1995-03 counted → apart ("the record begins at or above the line": its
  record opens in 1994-12 far above the line; O4); Estonia 2022-06, Lithuania 2022-06 and Latvia 2022-07
  counted → apart ("a euro member after its changeover"; O3); the United States' onsets, *cannot be read*
  before, now read on the π route alone (M9): 1863 → 1862 (π), 1920-02 → the bound, 1917-02. Seven counted
  lines flagged `stretch_begins`: Afghanistan 2008-04, Grenada 1979-03, St Kitts and Nevis 1980-05, Laos
  1989-02, Liberia 2008-06, Malawi 1984-04, Poland 1947. Counted by era: metal 167, gold exchange and Bretton
  Woods 100, fiat 182 → 178. Every variant moves the same way (1 to 5 statuses; the United States' onsets
  where the variant reads d); no line enters or leaves any file.
- **The onset**: π 160, d 26, the bound 2, **cannot be read 313** (257 of them counted). Of the 257 counted,
  242 cross before 1950: no exchange rate is frozen before IFS's (the d route cannot be read). Since 1950, 201
  counted breaks: π 159, d 26, bound 1, cannot be read 15 (12 for d, 3 for π). The π-only onset: π 437, bound
  7, cannot be read 57. Reading (b) above dates no headline onset (0 lines; the audit's M10).
- **The sources of the crossings**: Reinhart and Rogoff 265 (all annual), IFS 215, the BIS 19, JST 2. Of the
  265 Reinhart–Rogoff crossings (`rr_basis_kind`, reading j): 177 in years whose covering lines are all CPIs,
  **64 "non-CPI basis"** (single commodities — wheat, rice, rye flour, bread, meat —, wholesale prices, GDP
  deflators), **21 "mixed basis"** (the first build's count of 85 non-CPI took these with the 64), 3 "basis not
  stated"; 3 carry `rr_basis_seam` (Austria 1915, Sweden 1800, Turkey 1915). `price_basis` gives the sheet's
  words. M0 reads Reinhart and Rogoff's compiled column as given, and so does the headline (R7; the session's
  decision; whether R7 honours M0's "consumer price index" goes to M0's next version, the audit's O2).
- **M3's source anomalies — listed, never swapped** (screens of reading k: (i) a π(y) at or below −50% in any
  annual source as read; (ii) IFS-A's π(y) against IFS-M's year-average change, both years complete, apart by
  more than 20 points and by more than half the larger; (iii) IFS-A falling while IFS-M's index rises by more
  than 20% inside the year). 14 readings:
  - Azerbaijan 1992, IFS-A −10.6% while IFS-M's index rises 669% inside the year (iii) — the year before the
    counted crossing 1993-01, which rests on it.
  - Myanmar 1973, IFS-A +25.2% against IFS-M's year average −5.9% (ii); Nigeria 1984, IFS-A +17.8% against
    +39.6% (ii).
  - Reinhart and Rogoff's compiled column at or below −50% (i): Germany 1924 (−200.0, impossible for a price
    change), 1818 (−55.2), 1824 (−50.0), 1848 (−67.6); China 1912 (−51.1); Korea 1811 (−60.0), 1816 (−66.7);
    Norway 1813 (−67.6); Romania 1815 (−74.7), 1819 (−52.5); Thailand 1920 (−62.5).
  None is a crossing's own reading; a fall read as given can end a restoration count or open a stretch.
- **The variant `rr-cpi-only`** — **added after the first build's headline counts were seen, on the
  session's decision; a variant, never the headline.** A Reinhart–Rogoff year whose sheet's "Based on" block
  names no consumer price index is read as *cannot be read* for π; a year where any line of the block covering
  it names a CPI is read (the audit's M4: this keeps "mixed" years, e.g. France 1808 and 1820, whose compiled
  value may follow wholesale prices, and drops years no line covers — reading j flags both). Second build: 439
  lines (387 counted, 52 apart) against the headline's 501 (445 / 56). **Lines it moves**: 64 headline lines
  leave (60 counted, 4 apart; all Reinhart–Rogoff crossings) — 59 in the metal era, 5 in the gold-exchange and
  Bretton Woods era, 0 in the fiat era; 2 enter (both counted, from JST: Switzerland 1872, Finland 1915); 2
  change (both apart): Austria 1800's restoration 1803 → 1881, and Russia 1993-01's reason. Counted by era:
  metal 167 → 111, gold exchange and Bretton Woods 100 → 98, fiat 178 → 178.
- **The monthly common end**: read literally (M0 section 1, R6, as the pilot's C05 reads it) it is 2026-08,
  because after IFS's last month (2025-07) the sixty-odd monies of the BIS series go on alone and pass the
  "half of those that had one twelve months before" test again from 2026-06; the test fails from 2025-07 to
  2026-05. The variant `common-end-before-the-last-failing-run` ends in 2025-06: the same 501 lines, one
  restoration fewer (Hungary 2022-09's). Horizons counted in months (A12, frame h) use 2025-06 (the audit's M1).
- **Flags**: 21 lines `ifs_break`; 27 lines with a change of source inside the onset's window or the crossing
  (`seams`); 7 `stretch_begins`; 26 lines whose regime is `regime_carried` (2016's class); the regime at the
  crossing cannot be read on 263 lines (255 with a class year before 1946: frame a's lists, M4, not coded), the
  split on 298.
- **The United Kingdom around 1975**: one line, crossing 1975-03 (IFS, monthly), onset 1973-11 by the π route,
  restored 1984-03; no line under the 40% grid.
- **The grid** (lines; counted / apart): line 40, 205 (169 / 36); line 100, 72 (54 / 18); crossing of 1 month,
  525 (469 / 56); lower line 5, 425 (369 / 56); lower line 15, 572 (513 / 59); bound 24 and 60, 501 each (445 /
  56; onsets at the bound 6 and 1); d at 10, 501 (d onsets 29); d at 25 with a 10-point rise, 501 (d onsets
  20); π-only onsets, 501 (bound 7); bound breaks apart, 501 (443 / 58); IFS-break readings unreadable, 493
  (427 / 66); common end 2025-06, 501 (445 / 56); Reinhart–Rogoff CPI years only, 439 (387 / 52), above.
- **What was seen**: the protocol's producer read the structure of every source before writing it; building
  the first build, the coverage counts around the common end, the United Kingdom's 1975 line (the protocol's
  b8) and the counts above were printed; then the not-restored lines with each money's last reading, and the
  comparison of `rr-cpi-only` with the headline. Before the second build: the audit's report (with its named
  lines and values) and a pre-audit build of frame c (counts and structure, superseded, never committed).
  Building the second: the moves listed above, the anomaly screens' 14 readings, and the counts.
- **The acts list**: frame b reads no act. It was first built after the acts list's second build (c4a56ad);
  the acts list's third build (a8780e1) and its check (40f2c78) came after frame b's first build — `m0.py`
  checks first commits only, so the order of rebuilds rests on the commit messages (the audit's M8).
