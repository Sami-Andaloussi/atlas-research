# ft001-acts — reconstructed dataset

FT-001's acts list: every dated act of M0 section 2's headline lists (T2, L1, L2, L3, H1) that the named
sources give, one line each, with the variants the same sources give set apart. Built by mission M3's
second part under the coders' protocol `bank/maps/FT-001/missions/FT-001-M3-acts.md` (committed d7616d1,
its readings settled in 7296e8c, 0600426 and section 3c). **This is the third build**, under section 3d:
the deep audit `bank/checks/FT-001-M3-acts-2026-09-30-opus-audit.md` answered (533d66b), the second build
committed (c4a56ad) before any outcome list, and the small check of its answers
(`bank/checks/FT-001-M3-acts-2026-09-30-sonnet-small-check-v2.md`, not ready, F1) answered here. Frame b
(2ed0741) is committed after the second build; this build changes only T2 from 1960 and wording, still
**before any outcome list** of frames c or f
or the phases (M0's twin, `case_line.follows`). Every line carries the rules' hash of M0 v4.2 (commit
3163162). An act has no outcome: the outcome fields stay empty.

## Sources

- **Bank of Canada–Bank of England Sovereign Default Database**, 2025 edition (`bankofcanada/sovereign-
  defaults`, vintage 2026-09-30): sheet `Debt_2025`, its ten creditor columns (`IMF`, `IBRD`, `IDA`, `IADB`,
  `PARIS_CLUB`, `CHINA`, `OTHER_OFFICIAL_CREDITORS`, `PRIVATE_CREDITORS`, `LC_DEBT`, `FISCAL_ARREARS`, each
  `_2025`) and `TOTAL_2025` (the state's debt in default, US$ million). T2 from 1960; the "World" rows are not
  an economy.
- **Reinhart and Rogoff, *Varieties* of crises**, country sheets (`reinhart-rogoff/varieties-{A-E,F-M,T-Z}`):
  **only** the two columns "Sovereign debt crises — domestic" and "— external", found by their labels; the
  currency, inflation, stock-market and banking columns are never read. T2 to 1959.
- **Reinhart and Rogoff, *This Time Is Different***, external-default dummies (`reinhart-rogoff/ttid-
  default-tables`, the Table 6.2 and 6.4 workbooks' sheet `ExternalDefaultDummys`, checked identical for
  the economies used): T2 to 1959 for the twenty "M–S" economies whose *Varieties* file is not served.
- **Garriga (2025)**, central bank independence data (`garriga/cbi`, `Replication_ISQ_2025.tab`): only
  `cuk_limlen` (L1), `reform` and `decrease` (L3), `lvau_garriga` (L3's index variant), matched to economies
  by her two-letter `ISO` column, else by her country name (`missions/code/economies.py`).
- **Ilzetzki, Reinhart and Rogoff, the country chronologies**, NBER Working Paper 23135, February 2017
  (`irr/country-chronologies-1946-2016`): L2, H1 and their variants, by hand, read to September 2016.
- **Hammond, *State of the art of inflation targeting***, Bank of England CCBS Handbook 29, 2012
  (`frame-a/hammond-ccbs-29`): L3's "target abandoned" — **none found**: the only exits it names (Finland,
  Spain, Slovakia) left targeting on adopting the euro, a competing exit (M0 section 4).

## Steps

1. The protocol committed before any act was coded (d7616d1).
2. **Scripted acts** — `missions/code/acts.py` (`count`, then `build`), identically on every economy each
   source holds: T2 from 1960 = **in each creditor class**, a year whose stock in that class is above zero
   while the year before was read and zero in it (3d, O1); classes starting the same year are one line, the
   classes and their stocks named in `note`, `value` their sum; **an eleventh class, `UNASSIGNED`**, the
   stock the total carries and no class holds (the total less the ten classes, when above the rounding of
   eleven figures printed to US$0.01m; the small check's F1: Argentina 2001, Mexico 1982, Venezuela 1983,
   Greece 2012, Lebanon 2020 were invisible without it); a class left blank in a year whose total is
   read holds no stock; a year whose total is blank cannot be read, and a stock after it is set apart; a
   stock in an economy's first year is dated by the sources before 1960 (noted in `coverage.csv`); the USSR
   and the Russian Federation, one line of the database, read as one series (`SUN` to 1991, `RUS` from 1992).
   Variants, apart: `T2-var-private` (private creditors or local-currency debt only), `T2-var-total` (the
   first build's total stock). T2 to 1959 = the first year of each run of 1s in *Varieties*' domestic or external column
   (a domestic and an external default starting the same year are one line), or in the TTID dummies for
   the M–S economies (a run starting in a series' first year is set apart: it may have begun before);
   L1 = a year in which `cuk_limlen` falls below the year before (the note says whether the cap of 0.5
   stood before and after); L3 = `reform` = 1 and `decrease` = 1, the note saying where her `direction`
   disagrees (Uruguay 2008: `direction` 1; Georgia 1992 has neither flag and no line; the audit's M12);
   the index down by 0.05 or more is `L3-var-index`, set apart.
3. **Hand-coded acts** — the chronologies extracted page by page with their layout (`pdftotext -layout`),
   197 country tables listed from their headings; **four first coders** (Sonnet agents, 50, 50, 50 and 47
   tables, in page order) and **a second coder** on a 20% random sample of the tables (39, drawn with seed
   1797), who saw none of the first coders' work; each wrote `acts.csv` and `countries.csv` (every table
   read, with or without an act). `missions/code/coders.py` checks each coder's files (codes, dates, the
   closed list of acts, quotations of twelve words at most, every table read).
4. **Three passes.** The protocol's loose readings were settled by M0's text, never by an outcome, and
   committed before each new pass: S1–S11 after the first (7296e8c), S12–S16 after the second (0600426),
   S17 at the merge (the protocol's section 3c). Every coder, the second included, recoded under them.
5. **The merge** (`coders.write_hand`): the four first coders' third pass is the list; S17 applied by the
   session to its two lines (Syria 1948 and Turkey 1939: a "parallel market" first-listed after a peg is a
   market split, not an announced end — dropped; S17 was written after the merge showed them, said);
   force's dates (63 lines) written apart, never in `series.csv`. (The first build kept as `L2-var-silent`
   the 32 lines the second pass had coded and S12 dropped; the second build replaced them by the rule, step
   6.)
6. **The second build's hand side** (3d; `coders.write_hand` with the two new coder folders):
   - **headline L2 is a `clear` line** (the comments word the end): 21 lines. A class-only end is
     `L2-var-class` (53); a time-bounded official peg (S13, `judgement` by its own rule: the end dated by
     the bound, no decision worded) is `L2-var-bounded` (12) — the session's reading of 3d's "S13", below;
   - **freely falling read by its next component** (O2): the audit's eleven lines are `L2-var-ff` (10);
     their successors re-read by a fifth coder (c5, `coders/ff-reread-c5/`): Liberia 1998-08-31 re-read as
     S13 (its line replaced), Jamaica 1983-10 already coded, Israel 1952-02-17 a class-only end added; the
     other eight have no end (a de facto successor, the arrangement kept, or freely falling alone — Haiti
     2002, Mozambique 1986, South Sudan 2015 — which has no next component: not an end);
   - **`L2-var-silent` rebuilt by rule** (O4) by c5 in one pass over the 197 tables: 45 lines (the first
     build's 32 came from the second pass; 30 of them are among the 45; Cameroon 1948-01-26 and Ecuador
     1999-02-12 are not — the rule's reading, said);
   - devaluations whose size the text does not state are `L2-var-devaluation-unsized` (26; M8), the sized
     ones `L2-var-devaluation` (20);
   - Argentina's 2001 end dated **2002-01-05**, the text's own date of the formal dual market (M13; a
     class-only line);
   - **force's lifts** (O3) coded by c5, the text's dates: 9, in the force file (below).
7. `acts.py build` joins the scripted and hand lines, writes each line's `rules_sha256` (M0 v4.2's pair,
   after `m0.require_locked()`), and the coverage; `m0.py` checks the list (ok); apart lines carry
   `headline=no` (M3).

## Assumptions

- **`money` is the issuing economy** (ISO 3166-1 alpha-3; former states their ISO 3166-3 code; North
  Yemen `YAR`, the workshop's own; no World Bank aggregate). Which money an act touches is read by the
  frames. The Bank of Canada–Bank of England database's "USSR/Russian Federation" line: `SUN` to 1991,
  `RUS` from 1992, one series.
- **The Bank of Canada–Bank of England classes** are read as printed; they can overlap (their sum exceeds
  the total beyond rounding in 2,435 of the 8,684 economy-years whose total is read), so a line's `value` is an upper bound on the new stock.
  `PRIVATE_CREDITORS` is one class, never foreign-currency loans plus bonds, which do not sum to it.
- **Headline L2 = the `clear` lines** (3d, O2, the reverse of the first build). *Reading, the session's*:
  3d's parenthesis "(S2, S12, S13)" names the rules whose lines can be `clear`; S13 codes its own lines
  `judgement` (a bound dates the end, no decision is worded), so they are a variant of their own,
  `L2-var-bounded`, never mixed with the class-only ends. The small check found it against 3d's literal
  parenthesis (F4), not against M0 ("no announcement is value"); 3d is amended in words. Haiti 1991-09-16,
  touched by S12 and a bound, stays `clear`: the comments word the abandonment itself.
- **A line in two variants**: Finland 1992-09-08 is both `L2-var-bounded` (S13, "this period") and
  `L2-var-silent` (c5's rule). Each variant is read on its own, never summed.
- **H1** (M7): S6's "a money that replaces the old one" is a new unit of the same issuer; official
  dollarisation (Ecuador 2000, Zimbabwe 2009) is H1 by M0's own words, "another money made legal tender",
  both dated after the crossing.
- **T2 for the euro area's members stays on the member**; whether a member's default is an act on the
  euro's *taken back* support is not fixed by M0 — declared for the frames (protocol, section 6).
- **The readings** S1–S17 (protocol, sections 3a–3c), in short: an announced arrangement is shown by the
  class, or stated as official in the comments; L2 is its end when a float, freely falling or dual or
  multiple rates replace it, or when the comments word the end (`clear` if worded, `judgement` if only the
  class shows it); a de facto peg following, a new level or anchor, a peg kept official, a widening, a
  gold suspension (R1, frame a's), anything before 1946 — never a headline L2; a peg known only from the
  comments ends only where they word it; a time-bounded official peg ends at its date unless another
  official anchor follows; an end inside a table's gap cannot be dated; a mixed class is read by its first
  component.
- **Dates** at the precision the text gives; an undated variant at its period's start, at year precision.

## Uncertainty

- **Agreement on the sample** (Cohen's κ on 2,769 country-years, 1946–2016, an act in the year or not;
  `kappa-pass{1,2,3}.json`): L2 **0.50** (first pass, before the readings were settled), **0.89** (second
  pass, S1–S11: five disagreements, all "second coder only" — silence after a comment-stated peg, an end in
  a gap, an anchor change), **1.00** (third pass, S12–S16). **The third pass named to each coder the rows
  the residual rules touched, disagreements included: 0.89 is the independent figure.** H1 and force
  agreed in every pass (one country-year each in the sample).
- **The audit's own re-coding** (M11): 6 of 6 lines out of the sample re-coded identically — but they were
  the first build's headline, of which only Azerbaijan 2015 is still headline (the small check's F2); H1's
  and force's κ rest on one positive country-year each. The sample of 39 tables held **no `clear` L2
  line**, so κ says nothing of the headline L2. **The headline's own agreement**: a sixth coder (c6) re-coded L2 in the 20 tables that carry
  the 21 headline lines and 20 others drawn with seed 1797 (`coders/clear-recode-design.json`,
  `coders/clear-recode-c6/`): **20 of the 21 `clear` lines found at the same date, none found beyond them**
  (in the 40 tables). The one disagreement, Haiti 1991-09-16: c6 reads the freely-falling class by its next
  component, a crawling band, so a widening under S4, where the list keeps the worded "abandonment of the
  peg" (S2, S12) — the headline stands, the disagreement printed. *Slip, said*: c6 saw the design file
  naming which tables carried the headline lines, so the re-code was blind to the list's lines but not to
  where they sat. c6's other cases (the CFA tables' "Currency union/Peg" under S15, Burundi 1999's
  "reclassified", Paraguay 1986's silent gap) are in its `countries.csv`.
- **κ's disagreement lists**: `coders.kappa` prints, beside the counts, disagreements outside the span
  1946–2016 (China 1935; H1 in Andorra 1813, Indonesia 1942, Iraq 1900) that `kappa-pass1.json` leaves out;
  the counts and κ are the same (the small check's F10).
- **L2's headline is small**: 21 lines; the variants beside it (class 53, bounded 12, silent 45, freely
  falling 10) are printed with it, so claim 1 can show its shares on each.
- **S12's cost**: a peg stated only in the comments whose end the comments never word is not an act —
  the 45 `L2-var-silent` lines, now by rule, include Thailand's, Indonesia's and Malaysia's 1997 floats,
  Japan's of 1971, Iceland's of 2001, Madagascar 1994, Malawi 1994, Peru 1975, Rwanda 1994, Paraguay 1985,
  Libya 1981, Iraq 2006, Kenya 1994, Greece 1947 and France 1948. The coder's doubts, kept as coded: seven
  whose next comment describes a band or names an anchor (Colombia 1999, Dominican Republic 1985,
  Seychelles 2008, Suriname 1999, Tonga 2009, Iceland 2001, Brazil 1975), two whose peg is not called
  official (Brazil 1975, Italy 1946), Iran 1977 (the SDR link's end not worded), Congo DR 1962; excluded as
  doubts: South Africa 1979, Russia 2008–14, Sudan 1985 (`coders/rule-c5/countries.csv`, notes).
- **T2 per class is dense** — the price of M0's "first year of a stock" read in each class with no size
  floor (M0 names none): **1,775 lines** from 1960 in 155 economies, **20.4 per 100 economy-years** of
  coverage (the total-stock reading: 385, 4.4). By class: other official creditors 536, the Paris Club 396,
  private creditors 333, China 249, fiscal arrears 247, unassigned 171, local-currency debt 89, the IMF 71,
  IBRD 34, IDA 32, IADB 8 (324 lines name several classes). By size of the new stock: under US$1m 316,
  1–10m 287, 10–100m 433, 100m–1bn 468, US$1bn or more 271. A class that clears and returns starts a new
  line (Argentina has 26 from 1961, Venezuela 17). The major defaults the first build missed are dated:
  Argentina 2001 (unassigned) and 2002 (private creditors), Russia 1998 (local-currency debt), Mexico
  1982, Venezuela 1983, Greece 2012, Lebanon 2020 (unassigned). **For the frames**: claim 1's base rate on the same
  window absorbs the density, and `T2-var-total` and `T2-var-private` are printed beside; a size floor or
  a class list is for M0's next version (the plan's list), never chosen here.
- **The act rate by source, per 100 economy-years of its coverage** (M0 [a-R4]; `acts.py rates`),
  headline lines: T2 — Bank of Canada–Bank of England 1,775 in 8,689 economy-years (20.43), *Varieties* 107
  in 8,000 (1.34), TTID 30 in 3,040 (0.99); L1 — Garriga 62 in 8,547 (0.73); L3 — Garriga 75 in 9,110
  (0.82); L3's target half — Hammond 0 in 328; L2 — the chronologies 21 in 13,814 (0.15); H1 — 3 in 13,814
  (0.02: El Salvador 2001, Ecuador 2000, Zimbabwe 2009). In all 3,146 lines: 2,073 counted, 1,073 apart.
- **No T1 line and no crawl-step line** were coded (M15): T1 (taxes required in metal, another money or
  kind) is M0's hand-coded variant, and no source of this list dates it; `L2-var-crawl-step` was in the
  coders' closed list, and no coder found a step beyond an announced crawl.
- **What cannot be read** (`coverage.csv`): 34 economies whose first year in the Bank of Canada–Bank of
  England database already holds a stock (M4, noted on their rows); past each source's last year (the
  chronologies September 2016, their later version on `www.ilzetzki.com`, opened 2026-09-30, a later build;
  Garriga 2023, the Bank of Canada–Bank of England database 2024); T2 domestic before 1960 for the M–S
  economies; T2 before 1960 for economies outside Reinhart and Rogoff's seventy; a table whose last period
  is open (Turkmenistan, to 2008). The frames read "no act" only inside a source's coverage.
- **Slips, said**: writing the protocol, printing Garriga's header also printed her first two rows (the
  United States, 1970 and 1971, every column, her CPI inflation among them); nothing else of any frame was
  read before this list. The coders' comments read outcomes (the chronologies speak of devaluations and
  premiums): the barrier is S2's condition that an act is coded from a decision recorded, never from what
  followed.

## Files beside `series.csv`

- `coverage.csv` — per economy and act source, the first and last year read.
- `phase4-force-from-chronologies.csv` — force's dates (controls imposed or tightened, S9), 63 lines, the
  first coders' third pass, and **their lifts** (`FORCE-LIFT`, c5, 9 lines: Switzerland 1949, Canada 1951,
  Greece 1965, Argentina 1967 and 2002, the UK 1979, Bangladesh 1992, Botswana 2007, Cyprus 2015 — Greece's
  and Cyprus's the end of a span the text gives, `judgement`): **not acts** (M0 section 2), kept for the
  phases list. **By era** (O3): impositions 50 before 1946, 11 in 1946 to July 1971, 2 from August 1971
  (Argentina 2001, Cyprus 2013); lifts 4 and 5. Phase 4 cannot carry claim 5 (ii) in the fiat era from this
  file — written for M0's next version.
- `second-coder.csv` — the second coder's third pass on the sample, the reliability record, never merged.
- `kappa-pass1.json`, `kappa-pass2.json`, `kappa-pass3.json` — the agreement, act by act, with every
  disagreement.
- `coders/` — every coder's files of the three passes (`round1/`–`round3/`, each coder's `acts.csv` and
  `countries.csv`, and the pass's κ), the rule-built silent variant and force's lifts (`rule-c5/`), the
  freely-falling re-read (`ff-reread-c5/`), the 197 tables (`tables.json`) and the second coder's sample
  (`second-coder-sample.json`, seed 1797): κ reproducible from committed files (M14). Quotations are
  twelve words at most.
