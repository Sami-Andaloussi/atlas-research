# FT-001 — M3, first part: the panel, and frames b and c by rule

> Mission M3 (first part) of `bank/dossiers/FT-001-the-life-of-a-money.md`, section 14. Written for the E2
> session (`plan/e2-ft001.md`), 2026-09-30, **before any value of any series is read**, and committed alone
> first: the coders' protocol M0 section 3 asks for, on the model of `FT-001-M3-acts.md`. **The rules are
> M0's**, version 4.2 (`FT-001-M0-rules.md` and its twin, commit 3163162, pair hash `1160cab0bd84…e58d4`):
> sections 1, 4, 5 b, 5 c and 6's pressure strata; the twin's `common`, `frames.b`, `frames.c`,
> `claims.pressure_strata`. This file adds no rule; where M0 leaves a reading open it chooses in the open,
> numbered **R1–R30**, for the audit to judge. It follows the acts list, `data/reconstructed/ft001-acts/`
> (c816d52), committed before any outcome list.
> **What was seen before writing** — structure only: file, sheet and column names; DBnomics and World Bank
> page keys, dimension codes and series names; coverage (first and last periods, numbers of areas, counts of
> readings); IFS's observation-status codes, counted; Reinhart and Rogoff's sheet header labels; the IRR
> files' legends and the list of anchor codes (no country-year); the C15 run's keys, its list's header, the
> counts of its categorical labels (`rule`, `apart_080`, `flag`, `seam_in_window`, `cpi_source`) and the eight
> commonest values of its entry-side `w` column; the acts list's columns, route and status counts, and its
> T2 notes with digits masked. **Two slips**: printing the header of COW's inter-state file (its lines end
> with carriage returns) printed its first rows — wars of 1823 to the 1850s, participants and battle deaths:
> war data, no price, rate, money, debt, deficit, reserve or class value; and reading the pilot's `STATE.md`
> for C15 showed part 2's own results (C01, C02), which bear on no frame here. No price, rate, money, debt,
> deficit, reserve, class or default value of any economy was read.

## 1. The unit, the span, the dates

- **The money (R1).** The key is the issuing economy's ISO 3166-1 alpha-3 code, as in the acts list
  (`missions/code/economies.py`; former states SUN, CSK, YUG, DDR, YAR; Yemen PDR `YMD`). Codes map through
  that table: IFS, HPDD and BIS two-letter areas by the World Bank's `iso2Code` (IFS `SUH`, `CSH`, `YUC`,
  `DE2`, `1C_473`, `1C_459`, `AN`, `TW`, `1C_355` by name); the WEO's, the IRR unified-market and anchor
  files' and JST's ISO3 as given; Reinhart–Rogoff's sheet names and the IRR classification's two-row names
  by alias; COW state codes through Garriga's own `cowcode`–`ISO1AL3` pairs, then by name. An unmatched
  name is printed, never dropped silently. **The euro area is one money from 1999-01** (M0 section 1), coded
  `EMU`; IFS `U2` is read only from then; a member's own money ends at its changeover (c9). Groups and
  institutions are no money (`W0`, `W00`, `XR*`, `XS*`, `A10`, `F6`, `R1`, `4F`, `5I`, `5O`, `5W`, `5X`,
  `5Y`, `7A`, the `1C_` groups). *Reading*: the CFA francs, the Eastern Caribbean dollar and economies using
  another's money are read **economy by economy**, as their sources and the acts list give them, flagged
  `shared_or_foreign_money` in every year whose lagged fine class is 1 — M0 names only the euro as one money,
  and each has its own price index; the claims decide whether to cluster them. *Declared*: M0's **new-money
  rule** needs dated new units, which no frozen source gives as data (the chronologies name reforms in prose):
  until such a list is coded, each economy's chain, as its sources chain it, is one money, and every line
  says `new_money_rule: not applied`.
- **Span.** Frames b and c enter from 1800 (before, frame d only); the panel reads from 1800 and ends at the
  common end (2a). **Dates** at the source's precision: `YYYY` or `YYYY-MM`, compared as `m0.py` compares them.
- **π at a date (R2).** At a month, π12; at a year, π(y), the change of the year's average — every annual
  reading (frame c, the annual strata) uses π(y), since a year holds twelve π12.
- **The monthly span (R3).** From a money's first to its last month with a readable π12 (either monthly
  source). Inside it frame b reads months; a calendar year inside it with no readable month is read as a
  year. Outside it, years. A run that crosses the span's edge counts a year as twelve months and is dated at
  the precision of the period where it starts.

## 2. The series, and M0's source order

### 2a. How the order is applied

- For each item, money and period, **the first source in M0's order that reads the period** gives the
  reading; a source that does not is skipped — never filled, interpolated or scaled. **Levels are never
  spliced.**
- **Changes within one source (R4).** A change (π12, π(y) from an index, d, the reserves' change, Δπ, Δd,
  the change in credit) is read from the first source in the order that reads **both ends**; where none
  does, it cannot be read. A ratio is one source's ratio; c3's measure is a ratio of two ratios, each within
  its own source (4, c1).
- **A seam** — a reading whose source differs from the same item's reading before it — is flagged on the
  reading (`seam: old -> new`) and listed in `panel-seams.csv`; never smoothed.
- **IFS's break flag (R5).** IFS marks observations `OBS_STATUS = B` (557 in the monthly CPI, 407 in the
  annual, 475 in the monthly rate). A change whose span holds one is kept (IFS publishes one series) and
  flagged `ifs_break`, on every b and c line it reaches; a variant reads those changes as *cannot be read*.
- IFS values are multiplied by the multiplier their series name ends with (`ft.data.dbnomics.multiplier`).
- **The common end (R6).** A money "has a price index" in a month (year) when a source of the monthly
  (annual) price order reads a level or a published rate for it then. Monthly: the last month in which at
  least half of the monies that had one twelve months earlier still have one; annual: the same against the
  year before (M0 section 1). Computed once, printed in the manifest; frames b and c read nothing past it.

### 2b. The series (the frozen datasets are under `data/`, vintage 2026-09-30)

| Item (M0) | Sources, in M0's order | How read |
|---|---|---|
| **π** (§1; frame b; strata) | *Monthly*: IFS `dbnomics/IMF/IFS/M~~PCPI_IX` (CPI, index; 190 areas, 1920-01 to 2025-07); the BIS `bis/WS_LONG_CPI` (`FREQ` M, `UNIT_MEASURE` 628, index; 63 areas, 1913-01 to 2026-08). *Annual*: IFS `A~~PCPI_IX` (201 areas, 1920–2024); the World Bank `worldbank/FP.CPI.TOTL.ZG` (193 economies, 1960–2025); Reinhart–Rogoff `reinhart-rogoff/inflation-{A-E,F-M,M-S,T-Z}` (`.xls`, 70 country sheets, to 2010); the BIS (`FREQ` A, 628; 1661–2025); JST `jst/macrohistory`, `cpi` (18 economies, 1870–2020) | π12 = 100(P_t/P_{t−12} − 1); π(y) = 100(P_y/P_{y−1} − 1) on an annual index (IFS's and the BIS's are year averages). The World Bank and R-R give published rates, read as given (R7). The World Bank, R-R and JST have no months. The BIS's own year-on-year series (771) is not read. The euro reads the World Bank's `EMU` (annual) and the BIS's `XM` (monthly). |
| **Debt / GDP** (§1; c1) | The HPDD mirror `dbnomics/IMF/HPDD/A~~GGXWDG_GDP` (191 areas, 1800–2015); the WEO `dbnomics/IMF/WEO_2025-04/~GGXWDG_NGDP~pcent_gdp` (general government gross debt; ISO3; 1980–2024 read); R-R `reinhart-rogoff/debt-to-gdp-{A-E,F-M,M-S,T-Z}` (`.xls`, to 2008–10); JST `debtgdp` | The year's ratio from the first source that reads it (R8). |
| **Deficit / GDP** (§1; c2, c3) | The WEO `~GGXCNL_NGDP~pcent_gdp` (net lending/borrowing; 1980–2024 read); JST 100(`expenditure` − `revenue`)/`gdp` | The deficit is minus net lending. JST's is central government, the WEO's general: the seam says which. |
| **Central-bank credit to the state** (c3) | IFS `A~~12A___XDC` (monetary authorities' claims on central government; 178 areas, 1950–2024) **to 2000**; IFS `A~~FASAG_XDC` (central bank survey, claims on central government; 148 areas, 2001–2024) **from 2001**, the seam flagged | End-of-year stocks; the year's change within one line (R9). From 1948 (M0). |
| **GDP, national currency** (c3 only) | *Reading* (R10): IFS `A~~NGDP_XDC` (198 areas), then the World Bank `worldbank/NY.GDP.MKTP.CN` (1960–2025), never scaled | M0 names no GDP source. |
| **Exchange rate** (d; the onset's route; strata) | IFS `M~~ENDE_XDC_USD_RATE` (national currency per dollar, end of period; 225 areas, 1940-01 to 2025-07) and `A~~ENDE_XDC_USD_RATE` (end of year); R-R's *Exchange Rates (Official and Parallel)*: **not served** | R11. Anchors: IRR `irr/anchor-currency-annual-1946-2016`, sheet `Master` (ISO3 columns, 1946–2015). |
| **Reserves** (§1; strata) | IFS `M~~RAXG_USD` (excluding gold, dollars; 209 areas, 1950-12 to 2025-07); `A~~RAXG_USD` | 100(R_t/R_{t−12} − 1); annual: end of year on end of year. |
| **Regime** (§1) | IRR `irr/classification-annual-1946-2016`, sheet `Fine` (countries in columns, each named over the two rows beside the label "Country"; years in column B, 1940–2016; each country's first and last years in the rows labelled "Start" and "End"; classes 1–15 in the order the sheet `Classification` lists them) | R12. |
| **Market split** (§1, "two prices") | IRR `irr/unified-market-annual-1946-2016`: sheet `Unified` (annual 1946–2016), sheet `Master` (monthly 1946M1–2016M12); 1 dual, multiple or parallel, 0 unified, "n.a." no data; or class 15 of the lagged regime | R13. |
| **State in default** (§2; c5; strata) | As T2: `bankofcanada/sovereign-defaults` (`Debt_2025`, `DEBT_TOTAL_2025`, 1960–2024); *Varieties*' two sovereign-debt columns (to 1959); TTID's `ExternalDefaultDummys` (the M–S economies) | R23. |
| **War** (§1) | World Bank `worldbank/VC.BTL.DETH` (1989–2024); COW `cow/inter-state-wars` v4.0, `cow/extra-state-wars` v4.0, `cow/intra-state-wars` v5.1 (wars and state participants) | R14. UCDP is not open. |
| **Supports' "stands"** (§2; c6; strata) | Garriga `garriga/cbi` (`lvau_garriga`, `cuk_limlen`, 1970–2023); Chinn–Ito `chinn-ito/kaopen` (`ka_open`, `kaopen_2023.dta`, 1970–2023); the regime; the state in default; the acts list's H1 lines | R24. |
| **Route c4** | The pilot's run `studies/FT-001-part-2-where-printed-money-goes/results/runs/C15-e-episodes-closed.json` (its only commit fccce91; `card_hash` `3bf06edb…8d8dc`, the card committed at d58f06f, as M0 names them): `result.lists.headline` (a CSV text, 667 episodes) and `result.lists.smoothing` | R19. |

- **R7.** The World Bank: its published rate `FP.CPI.TOTL.ZG` (the index `FP.CPI.TOTL` is not read: one series
  per source). R-R: the column headed "Reinhart and Rogoff" (their compiled series, 68 sheets); India and
  Indonesia have none ("VanLeeuven", "IMF"): read right to left, the first column that reads the year,
  flagged `rr_no_compiled_column`. No other column is read.
- **R8.** R-R's debt: the column labelled "Total (domestic plus external)", "gross central government",
  "debt/GDP"; where a sheet has none, the same with "gross general government" (or "gross government",
  "gross central (federal) government"); never "debt/exports" nor "Total (public plus private) / gross
  external"; a sheet whose labels fit none cannot be read. The WEO: 2025–2030 are the April 2025 vintage's
  projections, never read; which of its last years are IMF estimates is not in the frozen pages (declared).
- **R9.** The change in credit: to 2000 on 12A; from 2002 on FASAG; **2001's** on 12A where 12A reads 2000
  and 2001 (flagged `seam_12A_FASAG`), else it cannot be read (FASAG's annual pages begin in 2001). 12A is not
  read for any other year after 2000, nor FASAG before 2001: M0 dates the two lines, and a date-bound source
  is not a fallback.
- **R10.** c3's GDP: IFS first (the credit line's own source), the World Bank where IFS has none. The pilot's
  units check (its panel rule 6, fixed before any of its runs) on credit over GDP: a money whose ratio moves
  by a factor of 100 or more between consecutive years, or whose median exceeds 300%, has c3 *cannot be
  read*, listed. The pilot's 0.1% floor is not used (a central bank may hold almost no claims on the state):
  a unit error downward can hide a c3 entry, never make one — declared.
- **R11. Depreciation.** d = 100(E_t/E_{t−12} − 1), E the money's units per unit of the anchor: the anchor is
  IRR's code for the regime's class year (R12; 2015's carried after 2015, flagged), read through its issuer's
  IFS rate (a cross rate of two IFS `ENDE` series), the same anchor at both ends of the window (the later
  end's); `USD`, `SDR`, `Freely_falling`, `n.a.`, no code, an anchor whose rate cannot be read at both ends,
  and every date before 1946: the dollar. **Market and official are one series here**: IFS's `ENDE` is the
  rate IFS reports, and no parallel or second rate is frozen; the lagged regime only labels d "market"
  (floating) or "official" (parity). Annual d: end of year on end of year. **The US dollar** has no d against
  itself: *cannot be read*, declared (the route dates no US onset; the US strata's d cannot be read). The
  euro: against the dollar.
- **R12. The regime.** Classes are annual, so the class 12 months before a date in year y is year y − 1's.
  Class years are read **1946–2016 only** (M0's span; the file's 1940–45 are not read); a class year before
  1946 — so every date in 1946 — takes frame a's gold-standard lists (M4, not yet coded: *cannot be read*
  until then); a class year after 2016 takes 2016's class, flagged `regime_carried` (dates from 2018; a 2017
  date reads 2016's own class). Class 14: the last class before it; none, *cannot be read*. An empty cell, a
  value not an integer 1–15, or a year outside the country's start and end: *cannot be read*. Parity 1–10
  (class 9 a parity; variant floating), floating 11–13, class 15 a parity whose premium cannot be read.
- **R13. The market split** is read at the date itself (M0 lags the class, not the dummy): `Master` for a
  month, `Unified` for a year; "n.a." or after 2016: *cannot be read* (only the class is carried). "A split
  recorded" = the dummy at 1 or the lagged class 15, **while a parity stands** (lagged class 1–10 or 15). The
  other sheets (`IUnified`, `WUnified`, `Advanced`, `WAdvanced`, `Figures`, `Independence`, `GDPSH`) are
  never read.
- **R14. War years.** (a) *Territory*: from 1989, `VC.BTL.DETH` ≥ 1,000 in the year — an empty cell for an
  economy the Bank lists is "none recorded" (the series records conflict-years, not a survey), and after 2024
  cannot be read; before 1989, each calendar year a COW intra-state war (v5.1) with the state as `CcodeA`
  touches (COW's definition carries the 1,000; no yearly deaths are published). **Inter-state wars "fought on
  its soil" cannot be read**: v4.0's `WhereFought` is a region, not a state — declared; (b) catches the
  belligerents. (b) *Own losses*: each calendar year of the state's participation (`StartYear1`–`EndYear1`,
  `StartYear2`–`EndYear2`) in a COW inter-state war (`BatDeath` of its row), extra-state war (`BatDeath`) or
  intra-state war it joined (its side's deaths, only where it is the side's only state) with own deaths
  ≥ 1,000; codes −8 and −9 cannot be read. Past a file's last war year (b) cannot be read: the year is a war
  year if (a) says so, else *cannot be read* (M0 section 1, a source's last year).

### 2c. Missing, and what M0 says then (*cannot be read*, never swapped)

Mauro et al.'s FPP (the IMF's site refuses the toolkit: not in the order); R-R's *Exchange Rates (Official
and Parallel)* — the second exchange-rate source and every parallel premium (M0 1 and 5 b: the premium route
is a hand variant, and none is found); IRR's monthly classification and 2017–2019 (`www.ilzetzki.com`); UCDP
(not open); release dates of index readings (b7). Not in M0's order and never read here: the Millennium
workbook, FRED, the ECB, the Global Macro Database.

## 3. Frame b, step by step (M0 5 b, `frames.b`)

- **b1 — the series**: π12 inside the monthly span, π(y) outside (R3), each from its order (2b).
- **b2 — the crossing**: the first month t with π12 ≥ **20** at t, t + 1 and t + 2, all readable (a gap
  breaks the run); dated t. A year read annually: the first year with π(y) ≥ 20. A money crosses only while
  unbroken: after a crossing, the next counts only after restoration.
- **b3 — restoration (R15)**: 24 consecutive readable months with π12 < **10** (2 years with π(y) < 10 where
  read annually), dated at the run's **last** month (year), the first date it is known; a crossing after it
  is a new break. `outcome` = `restored` with that date, else `not restored by the common end`.
- **b4 — the onset's routes**: π at **10**; d at **15** (R11; market under a float, official under a parity,
  the regime lagged 12 months); the premium at 10 only where a parallel series is found by hand — none is, so
  the route is empty and its variant cannot run.
- **b5 — the onset (R16)**: a route's run = its consecutive readable periods at or above its line **through
  the crossing's period** ("stayed … up to the crossing", read inclusive; the π route always holds there); a
  route below its line at the crossing dates nothing. A run begun within **36 months** of the crossing (start
  ≥ crossing − 36) is a candidate; **the onset is the earliest candidate's start**, `onset_route` its route.
  None: the onset at **the bound**, crossing − 36 months, `onset_route` = `bound`, flagged (variant: those
  breaks apart). The onset **cannot be read** where a route cannot be read at the crossing, or its run reaches
  back to an unreadable period (a gap, the record's start) at or after the bound: the earliest start is then
  unknown. **The π-only onset** (M0's variant) is written on every line. Annual crossings: routes in years,
  the bound 3 years.
- **b6 — controls**: a split first recorded, or a premium first passing its line, in a month (year) of
  controls imposed or tightened dates no onset (force's dates: `ft001-acts/phase4-force-from-chronologies.csv`).
  Neither is a headline route (b4): the rule has nothing to act on there, and is coded for the premium
  variant.
- **b7 — the first public crossing (R17)**: the release date of the reading at t (the crossing's first
  reading; an isolated earlier reading at the line is not a crossing) **cannot be read**: no frozen source
  carries release dates (DBnomics holds one vintage, indexed 2025-08-26; ALFRED and IFS's archived editions
  are not frozen). Written beside, flagged `convention`: t + 1 month, or the year's end + 9 months — frame h's
  release lags (M0 5 h) — for A12 to use only as flagged.
- **b8 — the line and the pound**: 20% for every money; no line of code names a money. The manifest reports,
  as the rule makes them, the United Kingdom's lines around 1975 (IFS read first) under the headline and the
  40% grid.
- **b9 — the case line**, one per break (`case_line.fields`): `money`; `frame` b; `route` = `onset_route`;
  `entry_date` = the crossing; `entry_measure` = π at it, `entry_measure_date` = the crossing; `outcome`,
  `outcome_date` (b3); **`onset_date` empty, the onset in `break_onset` (R18)** — `m0.py` refuses a counted
  line whose `onset_date` is not after its entry, a check written for entries that precede a break, while a
  break's own onset is at or before its crossing by definition; `responses` empty; `exit` empty until the
  new-money list exists (R1); `status`; `source` and `locator` (dataset, code, months of the crossing's
  readings); `coder` the script; `rules_sha256`. Beside, as the acts list adds columns: `break_onset`,
  `onset_route`, `onset_flag` (bound, cannot be read, ifs_break), `onset_pi_only`, `frequency`, `line_pct`,
  `first_reading_at_line`, `public_by_convention`, `regime_at_crossing`, `split_at_crossing`, `seams`, and
  R1's flags.
- **b10 — statuses**: `counted` — a crossing dated inside the record; `apart`, "the record begins at or above
  the line" — the money's first readable π is ≥ 20, so the crossing cannot be dated (M0 4). A crossing past the
  common end is no line. Censoring sits in the outcome (`not restored by the common end`); *cannot be read*
  sits in `onset_flag`, never on the break.
- **b11 — the grid**, each list beside the headline in the same format (`variant-<name>.csv`): the line 40 and
  100; a crossing of 1 month; the lower line 5 and 15 (onset and restoration); the bound 24 and 60; d at 10,
  and at 25 with a 10-point rise over 12 months (Frankel–Rose); π-only onsets; bound breaks apart;
  `ifs_break` readings unreadable.

## 4. Frame c, step by step (M0 5 c, `frames.c`)

- **c1 — the routes, per money and year** (from 1800; c3 from 1948, c4 from 1950), "met" when the year's
  reading is at or above the line: **c1** debt/GDP ≥ 90 [60]; **c2** deficit/GDP ≥ 3 [5]; **c3** the measure
  s = 100 · [Δcredit / GDP]_IFS ÷ [deficit / GDP]_WEO or JST ≥ 50 [25; 75], with the deficit ≥ 3% of GDP (R4,
  R9, R10); **c4** each episode of C15's headline list not set apart (`apart_080` empty: every one-month jump,
  change of definition, annual episode and "jump cannot be read" out), entering in the year of its `c`;
  `area` (IFS two-letter; `U2` → `EMU`) to the money. **R19**: c4's measure is the episode's own
  `rise_pct_gdp` (base money's rise over (low, c], % of GDP), dated `c` — M0 names none. The nine O1 lines
  (`flag` "likely reclassification, unread") and CI's episode through its December-2001 seam
  (`seam_in_window`) enter flagged `c4_flag`; a variant drops them; O2's smoothing list gives its variant. The
  build first checks the run's `card_hash` against M0's and that the file is unchanged since fccce91.
- **c2 — entry and spells (R20)**: the entry is the first year any route is met, ties **c1 > c2 > c3 > c4**
  (`route` the first, `routes_met` all); the spell runs entry to entry + H − 1; **the next entry is the first
  year at or after entry + H with a route met, whatever the earlier entry's status** — else "already
  inflating" would choose the next entry by π. H = 10; H = 5 and 20 are their own lists. Flags, each with a
  variant that drops them: `met_at_record_start` (an entry in the first year the money's routes can be read:
  it may have been met before); `entry_at_seam` (c1 or c2 met in a year whose source differs from the year
  before's); **R30** `route_unreadable_before` (a route could not be read in the year before the entry, so the
  entry may be late: kept, since "the first year any route is met" reads the routes that can be read).
- **c3 — entry measure and tercile (R21)**: the route's measure in the entry year (c4: at `c`); terciles **per
  route and per H list, over every entry line with a readable measure, whatever its status** (M0: "terciles of
  all entrants"), the cut-points in the manifest and fixed for every claim. **R29**: `c1_outside_fit` on c1
  lines after 2009 or of an economy outside R-R's seventy (the frozen debt files' sheets; the paper's own
  sample is not frozen).
- **c4 — era (R22)**: of the entry date; the annual years 1914 and 1971 straddle two eras and take the era of
  the year's last day (annual readings are known at its end), flagged `era_boundary_year`.
- **c5 — the state in default at entry (R23)**: **a stock in default at a date is not in the acts list** (its
  T2 lines are the first years of stocks, its `coverage.csv` the sources' spans), so it is read from the same
  files by `acts.py`'s own readers, factored out with `acts.scripted()`'s output checked unchanged. In the
  entry year: from 1960, `DEBT_TOTAL_2025` > 0 in default, = 0 not, empty *cannot be read*; to 1959, a 1 in
  *Varieties*' domestic or external column in default, 0 in both not; the M–S economies' TTID external dummy,
  1 in default, 0 *cannot be read* (their domestic defaults cannot be read; variant: not); outside the
  sources' economies or years (2024 the last): *cannot be read*. **The euro**: M0 names no rule for a union's
  state — *cannot be read*, declared (the acts protocol's section 6 left it to the frames).
- **c6 — supports standing at entry (R24)**, each read from its "stands" condition at the entry, never from
  the acts: *taken back* — not in default (c5), "legal for taxes" read as holding (T1 is hand, a variant);
  *a limit by rule* — `cuk_limlen` ≥ 0.5 [0.25; 0.75], or the lagged class a parity (1–10, 15); without pegs
  and boards, the cap alone; *a limit by institution* — `lvau_garriga` ≥ 0.5 [0.4; 0.6] or a target announced
  (frame a's list, M4, not coded: with the index below 0.5, *cannot be read* until M4); *force* — `ka_open`
  ≤ 0.25 [0.1; 0.5] (the ban half has no headline source: variant); *habit* (variant) — no H1 act before
  entry, within the chronologies' span; *world demand* (variant) — COFER is not frozen: *cannot be read*.
  Garriga and Chinn–Ito start in 1970: before, those supports cannot be read. Each reading and the count (one,
  or two or more; *cannot be read* when the count turns on an unreadable support) are columns of the line.
- **c7 — apart**, a status with its reason: (i) **convertible at entry (R25)** — before 16 August 1971,
  frame a's gold-standard lists (M4: *cannot be read* until coded); from it, only a currency board redeems on
  demand into another money: a lagged class 2 ("pre-announced peg or currency board") *cannot be read* until
  the boards the chronologies name are coded; any other class, not convertible; (ii) **already inflating** —
  π(y) ≥ 10 in the entry year or the year before (R2), either unreadable *cannot be read*; variant: entry-year
  cases counted as entrants whose outcome is read; (iii) **past frame b's onset (R26)** — the money's first
  headline break whose crossing is not before the entry: apart if its onset is on or before the entry (an
  onset inside the entry year is "on", as `m0.py` compares); its onset unreadable: apart if the π-only onset
  is on or before the entry (the true one is no later), else *cannot be read*; (iv) **a war year** at entry
  (R14), unreadable *cannot be read*.
- **c8 — the outcome over H**: *broke* — frame b's headline crossing in a year from entry + 1 to entry + H
  (`outcome_date` the crossing, `onset_date` its onset); *broke and restored* — restored (b3's date) on or
  before the end of entry + H; *held* — no crossing, π readable in every year to entry + H; a year unreadable
  before any crossing makes the line *cannot be read* ("coded from the record by what happened, or cannot be
  read", M0 4).
- **c9 — competing exits and early ends** (M0 4): a union, merger or replacement unrelated to breaking,
  announced 12 months or more before, with no crossing in the 12 months before it, ends the spell `ended
  unbroken` (`exit`: type, date, source), apart, counted both ways by the claims. The euro's changeovers are
  the ones in reach; **no frozen source dates them**: until that table exists (section 6), a member's spell
  reaching 1999 is *cannot be read*, and so is any spell whose π stops before entry + H and the common end
  with no crossing before the stop.
- **c10 — censoring (R27)**: only the annual common end censors: a spell whose entry + H passes it is
  `censored` **whatever happened before it** (M0: counted neither way), what happened so far in `so_far`.
- **c11 — the case line**: `money`, `frame` c, `route`, `entry_date` (YYYY), `entry_measure`,
  `entry_measure_date`, `outcome`, `outcome_date`, `onset_date`, `responses` (empty), `exit`, `status`,
  `source`, `locator`, `coder`, `rules_sha256`; beside: `H`, `routes_met`, `tercile`, `era`,
  `default_at_entry`, the supports and their count, `regime_at_entry`, `split_at_entry`,
  `convertible_at_entry`, `already_inflating`, `war_at_entry`, `war_years_in_H` (claim 2's variant),
  `restored_date`, `so_far`, and every flag above.
- **c12 — variants**, each its own file: H 5 and 20; c1 at 60, c2 at 5, c3 at 25 and 75; the entry-year
  variant; each flag's drop; `regime_carried` entries out; frame b's variant lists carried through.

## 5. The pressure strata's series (M0 6, `claims.pressure_strata`)

The panel carries, per money and year (and month where monthly), the items the claims' strata read — reading
A takes the year before's value, reading B the year's own; the choice is the claims': π(y) (R2) and Δπ over 1
and 3 years (within one source, R4); d and Δd (R11), labelled by regime; the split (parities only, R13); the
reserves' 12-month change and its fall of 20% [10; 30]; the year's route measures c1–c4 (strain's terciles
over strained at-risk years are the claims', once at-risk years exist); the state in default (c5); the
supports standing and their count (c6); the regime group (R12, carried flagged); the decade.

## 6. What the build runs, its checks, its manifest

- **Code**, under `missions/code/`, committed with its tests **before any run**: `xls.py` (a standard-library
  BIFF8 reader for R-R's `.xls` — the OLE2 `Workbook` stream, `BOUNDSHEET`, `SST`, `LABELSST`, `LABEL`,
  `NUMBER`, `RK`, `MULRK` and `FORMULA`'s cached values; `xlsx.py`'s twin, nothing installed); `panel.py`
  (every reader, the order, seams, the common end, war years, default through `acts.py`'s readers; `panel.py
  count` prints coverage, never a value); `breaks.py` (frame b); `strain.py` (frame c); `economies.py`
  extended (IFS, BIS, IRR, R-R's inflation and debt sheets, COW); `test_panel.py`, every rule of sections 3
  and 4 on synthetic series (a crossing, a gap, restoration, the onset's three cases and the bound, a seam,
  2001's credit seam, the spell grid), green before a real series is read.
- **The panel itself is not committed (R28)**: it is rebuilt in memory from the frozen files at every run, as
  the pilot's panel is, since its rows would be the sources' own values (R-R and IRR are cited, never
  republished; JST is CC BY-NC-SA; the workshop commits manifests and original work). Committed of it:
  `panel-coverage.csv` (per money, item and source: first and last period, number of readings),
  `panel-seams.csv`, and the panel's digest (SHA-256 of its sorted rows) in each manifest, so a rebuild is
  checked identical.
- **Datasets**: `data/reconstructed/ft001-b/` (`series.csv` the headline breaks, `variant-*.csv`, the panel's
  two files, `MANIFEST.md`); `data/reconstructed/ft001-c/` (`series.csv` the H = 10 spells, `variant-*.csv`,
  `MANIFEST.md`).
- **Checks before each commit**: `m0.py`'s `list_problems` on every `series.csv` and `variant-*.csv` (the lock
  at 3163162, the case line, the order: both lists follow `ft001-acts`, as the twin declares);
  `ft.data.reconstructed.problems` on `ft001-b` and `ft001-c`, empty; `test_panel.py` green.
- **Order of commits**: this protocol alone; the code and tests; the hand lists frame c needs (section 7),
  each under its own coders' protocol, before frame c is computed; `ft001-b`; then `ft001-c` (it reads b's
  onsets and crossings — the twin does not declare it, so the order is the build's, said).
- **The manifests say**: sources and vintages; each step; every reading R1–R30 used; the common ends;
  readings by source, and the seams; counts by status, reason and flag; the tercile cut-points; the UK's 1975
  lines; what cannot be read, item by item, and why; the panel's digest; what was seen, and any slip.
- **Audit**: the deep mission audit (`.claude/skills/ft-map/mission-audit-brief.md`), isolated.

## 7. What the build needs that is not frozen, and what this protocol cannot hold

- **Hand lists, none frozen as data**, each coded before frame c is computed or left *cannot be read*: the
  euro's members and changeover dates with their legal acts (c9); new currency units (R1); other money ends
  and competing exits with their announcement dates (c9); currency boards from the chronologies (c7);
  frame a's gold-standard lists and inflation targets (M4; R12, c6, c7).
- **Walls and gaps** (2c): FPP; R-R's official and parallel rates; IRR monthly and after 2016; UCDP; release
  vintages; COFER; an SDR or basket rate for the dollar's own d (R11); the WEO's estimate years (R8).
- **Declared, not closed**: inter-state wars on a state's soil (R14); c3's downward unit errors (R10); the
  euro's state in default (c5); shared and foreign monies read one by one (R1); IFS breaks kept in the
  headline (R5); an entry's route unreadable the year before (c2).
- **The barrier**: frames b and c are scripted, run identically on every money, never searched by name; the
  commit order holds the lists (`m0.py`). What no code holds: that nobody read an outcome between this
  protocol's commit and the lists' — the build's producer prints coverage and counts, never a case's value,
  until the lists are written.

## 8. Readings amended after frame c's deep audit (2026-09-30, before frame c's rebuild)

The audit is `bank/checks/FT-001-M3-panel-frame-c-2026-09-30-opus-audit.md`: not yet, B1. Each reading below
is amended by M0's text, never by an outcome, and is committed before the code that applies it. The earlier
wording stays above, for the history.

- **R26, amended (B1).** "Past frame b's onset" reads each later break's crossing:
  - b5 dates every onset within its bound (36 months before the crossing; 3 years annually). A later break
    whose **bound** falls after the entry therefore has its onset after the entry, whatever the onset
    reading: **no**.
  - *Cannot be read* is kept only when the entry lies inside a crossing's bound and that break's onset
    cannot be read.
  - The earlier branch let only monies that later break be set aside, which is a choice by outcome. The
    residual lines are printed and read both ways (the audit's M5).
- **R26, completed (O1).** M0 5 c sets apart "an entry on or after frame b's onset". An entry **inside an
  unrestored break**, whose latest earlier crossing is not restored before the entry year begins, is *apart*,
  "during a break". A restoration dated inside the entry year leaves the entry apart as well: the entry year
  is not wholly outside the break. Frame b's apart lines count here too (M7 of frame b's audit).
- **R14 in frame c, restored (O3).** M0 section 1 says "cannot be read, never none". A war year that cannot be
  read at entry makes the line *cannot be read* in the headline. Reading it as no war (M4's P23, a frame a
  reading) is a variant, `war-unreadable-as-no`. The code of 8997785 had applied P23 to frame c against
  R14: said.
- **c5, kept, with its variant (O3).** "In default at entry" is a stock in any creditor class of the
  database, `UNASSIGNED` and `FISCAL_ARREARS` included. M0 says "a stock in default in the Bank of
  Canada–Bank of England database", and fiscal arrears are one of its stocks. The TOTAL reading is the
  variant `default-total`. A claim 2 verdict that turns on either variant is "we cannot conclude".
- **R30, narrowed (M1).** `route_unreadable_before` tests c3 only where c3's deficit floor lies below c2's
  line, that is, only where c3 could enter.
- **"Already inflating" under frame b's lower-line variants (M7)**: read at that variant's lower line, as
  M0 ties it to "the lower line".
- **Said in the manifest, no rule changed**:
  - claim 2's headline is thin by construction (O2): "taken back" is the default stratum's opposite, and the
    smallest detectable effect is printed before any count (M0 v4.1's duty);
  - c3 cannot enter the headline (M2), and c4's measure is nearly nominal (M3);
  - lines whose outcome is unreadable are counted and read both ways (M4);
  - "announced 12 months before" at the euro changeovers is read as met, and both ways (M6);
  - claim 2 starts in practice in 1971 (M9);
  - the euro area is never counted (M10).
- **What M4's lists can and cannot give (O4)**:
  - "convertible" before 1971 is read from frame a's panels (`data/reconstructed/ft001-a/`, 0c4b737);
  - the 21 entries of 1937–1970 stay *cannot be read* (M4 §10.7);
  - IRR's class-2 hard pegs wait on the currency-boards list of section 7, a task added to the plan.

## 9. War years after COW's coverage (2026-10-01, before frame c's next build)

Frame c reads every war year through `war.py` (`panel.war_at`, R14). `war.py` gains W12 and W13 (frame a's protocol,
`FT-001-M4-frame-a.md` section 22, written in Sami's gap sweep): after COW's coverage, a state-year that was *cannot be
read* only because a state's own losses abroad are unseen becomes **no** when UCDP/PRIO's Armed Conflict Dataset v26.1
lists the state as party to no conflict of cumulative intensity 1 that year. W12 never makes a *yes*.

- Frame c is rebuilt under this protocol unchanged. The rebuild's manifest says which entries moved, and counts them.
- The old reading stays runnable (`ucdp=False`) and is reported beside the rebuild as a variant, so that the move is
  seen.
- No frame c line has been read for this section.
