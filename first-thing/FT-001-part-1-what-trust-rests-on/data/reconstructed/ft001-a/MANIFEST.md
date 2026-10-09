# ft001-a — reconstructed dataset

FT-001's frame a: the dated changes of a support in four panels — the 1914 suspensions (a1), the exits from
gold of 1931–36 (a2), central-bank independence reforms up and down (a3), inflation-targeting adoptions (a4) —
one line each in M0's case-line format, with the variants the same sources give set apart. Built under the
coders' protocol `bank/maps/FT-001/missions/FT-001-M4-frame-a.md` (committed alone, 731d10b; its readings
settled after the first coder's pass, section 12, c93ef42), by `missions/code/frame_a.py` (`build_all`,
committed before this list, 4d251bd; panel 3 and `war.py`, 7871641).

**This is the fourth build** (2026-10-02). It carries panel 4 **from 2012**: AREAER's candidates (section 14),
each read by its central bank's own announcement (sections 17, 20 and 21). The protocol through section 22 (2776366)
and the code with the first coder's files (776174a) were committed before it, and `agreement.json` and the build
name the protocol's commit.
- **What moved from the third build** (d310f2a):
  - **Two lines were added**: the Dominican Republic's adoption (2012-01, section 21) and India's variant line
    (2015-02-20, section 20, B2).
  - **No line changed status.**
  - **90 lines' war year moved from *cannot be read* to *no*** (W12, section 22: UCDP v26.1 reads test (b) after
    COW's coverage). That is 36 `a3` variant lines, 34 `a3-up`, 12 `a3-down` and 8 `a4`. Under P23 a line whose war
    year cannot be read was already counted and flagged, so only its flag and P23's variant move.
  - The third build's small check (`bank/checks/FT-001-M4-frame-a-third-build-2026-10-01-sonnet-small-check.md`)
    was answered in section 20.
- **The build reads the first coder's working folder** `data/hand/ft001-a/a1`, which is outside git. Its
  committed copy is the archive in `coders/`. The pre-commit refuses data files under `bank/`.
- **The second build** was 4510971. The deep audit before it (`bank/checks/FT-001-M4-2026-09-30-opus-audit.md`,
  not yet, B1) was answered in section 13 (de3fe65) and in code (e861121). Every line carries M0 v4.2's pair hash
(commit 3163162). **Frame a counts no outcome**: `entry_measure` and the outcome fields stay empty (P1); the
window build, `ft001-a-window`, reads value and trust after this list is committed.

## Sources

All frozen at vintage 2026-09-30.

- **Panel 1**:
  - Meissner, NBER WP 9233, Table 1 (`frame-a/meissner-w9233`, read from the page image): the candidates.
  - Exit sources (P6, Q2): Mitchener and Weidenmier, WP 15401, Table 1 (the head, 20 of Meissner's 35
    dated adopters), then Bordo and Schwartz, WP 4860, Table 1A, then Obstfeld and Taylor, WP 9345;
    Bordo and Rockoff and Chernyshoff–Jacks–Taylor give no period that fills.
  - Dating sources (P8, Q3, Q4): Bordo and Schwartz (the head by order, tied with Brown at 3), Bordo
    and Kydland, WP 3367, Brown (1940), Book One (`frame-a/brown-1940-book-one`), and the *Federal
    Reserve Bulletin*, May–December 1915 (none dated).
- **Panel 2**: Bernanke and James, the chapter's Table 2.1 and its note 7 (`frame-a/bernanke-james-chapter`);
  the working paper's Table 1 (`frame-a/bernanke-james-w3488`) compared cell by cell. The variant P11 comes
  from Ilzetzki, Reinhart and Rogoff's chronologies (`irr/country-chronologies-1946-2016`).
- **Panel 3**: Garriga (2025), `garriga/cbi`, only `cname`, `ISO`, `year`, `reform`, `direction`, `increase`,
  `decrease`, `creation`, `regional`, `lvau_garriga` (selected by name; her inflation columns never read).
- **Panel 4**:
  - Hammond, CCBS Handbook 29 (`frame-a/hammond-ccbs-29`): Table A and each country table's row 1.4;
    Chart 1 never read.
  - **Adoptions from 2012, the headline**:
    - the IMF's AREAER, editions 2011–2023 (`frame-a/areaer-2011-2023`, Sami's hand), its framework column
      coded by two coders (`ft001-a-areaer`);
    - each candidate's central-bank announcement, frozen from its own host after the Guard's ruling
      (`frame-a/*-it-announcement-*`, `*-it-nearest-*`, `boj-price-stability-target-2013`);
    - Sami's hand downloads (`frame-a/bcp-it-recounted-2013`, `frame-a/bcu-ipm-2016q2`,
      `frame-a/pib-india-mpfa-reply-2015-08-07`).
  - **Adoptions from 2012, the variants**: Cobham's classification, 2024 update
    (`frame-a/cobham-monetary-frameworks-2024`), and its legend (`frame-a/cobham-classifications-page`).
- **War years**: `war.py` on the Correlates of War's inter-, intra- and extra-state war files (`cow/*`), and
  the World Bank's battle-related deaths from 1989 (`worldbank/VC.BTL.DETH`).
- **The euro's entry years**: the ECB's "Our money" page (`frame-a/ecb-euro-area-members`).

## Steps

1. The protocol was committed alone, before any list of frame a was coded (731d10b).
2. The candidate sources were frozen after the Guard's rulings (03f9e55, e1324d7, 1074f44). Cobham's host
   and the Finnish and Slovak central banks' hosts were opened by Sami (741cfb10eb31).
3. **Panel 3 and the war years by script** (`frame_a.panel3`, `war.py`, 7871641): identically on every
   Garriga country-year and every COW state-year; its tests were green on synthetic rows first.
4. **Panels 1, 2 and 4 by hand**:
   - a first coder (`a1`, Sonnet) read every candidate;
   - the loose readings were settled by the protocol's and M0's text (section 12, Q1–Q9), committed before
     the second coder (c93ef42); the first coder recoded under them;
   - a second coder (`a2`, Sonnet, who saw none of `a1`'s files) coded the 20% sample drawn with seed 1797
     (panel 1: 10, panel 2: 5, panel 4: 6).
5. `frame_a.build_all` (4d251bd; section 13 in e861121) joins the lines:
   - it runs `hand_problems` and `irr_problems` before any write, sets section 6's statuses (a war year at
     entry apart; P13; P23 flagged; a competing exit ends a line unbroken), and applies section 1's
     settlement;
   - it writes `series.csv`, `members.csv`, `coverage.csv` and `agreement.json`, and archives the coders'
     files in `coders/`.
   - `m0.py` checks the list: ok.
6. **Section 13, applied by rule in the build** (the coders' files are never edited):
   - panel 2's headline exit is the first of suspension and devaluation (M0 section 2);
   - Bernanke and James's note-7 exit becomes the variant `a2-var-bj-note7`;
   - Germany, Hungary, Latvia and Romania, whose only change is an exchange control, are members with no
     headline exit;
   - W11: Australia 1915, Canada 1914 and Finland 1914 take their metropole's World War I year, so they are
     apart;
   - Cobham's lists from 2012 are variants conditioned on behaviour, and the headline from 2012 waits on
     AREAER;
   - P19 has no fallback.
7. **Panel 4 from 2012** (sections 14, 17 and 19; this build):
   - AREAER's 18 candidates make the headline membership `4-from-2012`, checked against `ft001-a-areaer`
     (`areaer_problems`).
   - The session read each candidate's announcement under R-A4. The adopters' dated lines are `a4` lines, and
     the later or transition documents are the variant `a4-var-later-or-transition-documents`.
   - `m0.py` checks the list: ok. `ft.data.reconstructed.problems("ft001-a")` is empty.

## Assumptions

- **The readings P1–P29 and Q1–Q9** of the protocol, as written there. In short:
  - Panel 1:
    - membership is read at 30 June 1914 (P5);
    - the exit source is the one giving gold-standard periods for the most of Meissner's 35 dated
      adopters (Q1, Q2);
    - R1 is a dated suspension of redemption, never an export embargo or a legal-tender decree (P7, Q3);
    - a member's date is the first P8 source to date it to the month, else to the year (Q4).
  - Panel 2:
    - members are on gold at the end of 1929 (P10);
    - the exit is the first of suspension and devaluation (P12 as amended in section 13); Bernanke and
      James's first of three (their note 7) is the variant;
    - an exit before 1931 is apart (P13).
  - Panel 3: up and down are never pooled (P14); a union's reform counts once (P15).
  - Panel 4: the formal adoption date (P17); the three exits before 2012 enter (P18).
  - **From 2012** (R-A1–R-A6, section 17):
    - The headline is AREAER's de jure list. A candidate is an adopter only where its own announcement states
      an explicit numerical target adopted as the policy's anchor, dated by that announcement.
    - The edition's year is never a date.
    - A later document that recounts the adoption, or a plan for a regime "in transition", is the variant.
    - Cobham's four-category and full-only lists are variants **conditioned on behaviour**: even its loose
      categories include targets attained (section 13, B1).
- **`money`** is the issuing economy (`economies.py`). Austria-Hungary is `XAH` and the Straits Settlements
  `XSS`, from ISO's user-assigned range (P2). A union's money is `EMU`, `XOF`, `XAF` or `XCD`.
- **War years** (`war.py`, W1–W13): after COW's 2007 end, a state's own losses abroad are read with UCDP v26.1
  (W12): *no* where the state is party to no conflict of cumulative intensity 1, else *cannot be read*. W12 never
  makes a *yes*, and `ucdp=False` keeps the third build's reading. Such a line stays counted and flagged (P23), and a variant
  drops it. W11: a dependency that is not a COW state takes its metropole's World War I or II year (the
dominions and India with the United Kingdom, Finland with Russia).
- **Section 1's settlement**: a member whose change cannot be dated at all is *cannot be read* in
  `members.csv`, never "no change" (Romania, India in panel 1).

## Uncertainty

- **Lines**: 711 in all, 106 by hand and 605 by script. By route and status:

  | Route | Counted | Apart | Ended unbroken |
  |---|---|---|---|
  | a1 | 7 | 15 | |
  | a2 | 15 | 27 | |
  | a3-up | 272 | 40 | 15 |
  | a3-down | 58 | 15 | 1 |
  | a4 | 31 | 1 | |

  Variants and the rest, all apart:
  - `a3-var-index`: 197;
  - `a3-neither` (direction 0): 6;
  - `a3-unread`: 1;
  - panel 4's variants: `a4-var-later-or-transition-documents` 6, `a4-var-informal-start` 3, and
    `a4-var-applied-from` 1.
  - **Panel 4 from 2012** adds five counted adoptions: the Dominican Republic 2012-01, Japan 2013-01-22, Russia
    2014-11-06, Costa Rica 2018-02-02 and Mauritius 2023-01-11.
    - The Dominican Republic is dated by the bank's January 2012 bulletin. The Junta Monetaria's resolution of 15
      December 2011 is reported, not frozen. Dated by the resolution, it would be a pre-2012 adopter, and four
      would remain.
    - The bulletin also carries earlier traces: a date of 26 November 2011, and a monetary programme "recently
      published". So the announcement may predate January 2012. That is the same risk, said.
    - If any count turns on it, or on Russia (section 20, B1), that is said.
    - Russia's line keeps its date. Only its flag gains section 20's note (B1: the act, not a plan in
      transition).
  - The variant dates Argentina 2016-12, Ukraine 2018-07-13, Kazakhstan 2015-04-24, Uzbekistan 2019 and
    Uruguay 2016-06 (a re-entry); India 2015-02-20 (a later report of the joint agreement).
  - Panel 1's apart headline lines are the belligerents in a war year at entry, told one by one (Belgium,
    Germany, France, the United Kingdom, Russia, and through W11 Australia, Canada and Finland; Brazil's
    Contestado rebellion).
  - **Panel 1 is a war-crisis panel.** Its seven counted neutrals (Argentina, Denmark, Greece, Norway,
    Sweden, Switzerland, the Netherlands) changed at the war's outbreak.
  - Panel 2 has 17 headline exits, 15 counted:
    - New Zealand (April 1930) is apart under P13, and Italy (October 1936) for a war year.
    - The swap moved five dates: Czechoslovakia 1931-09 → 1934-02, Estonia 1931-11 → 1933-06, Greece
      1931-09 → 1932-04, Italy 1934-05 → 1936-10, Poland 1936-04 → 1936-10.
    - Nine of the first-of-three exits were exchange controls, eight of them after a banking panic in
      Bernanke and James's own list (the audit's O2).
  - P23's variant, which drops the lines whose war year cannot be read, removes 16 of 59 a3-down lines and 61
    of 287 a3-up lines. Before W12 it removed 28 and 94, most of them after COW's 2007 end (the audit's M3).
- **Members** (`members.csv`, 146 rows):
  - panel 1: 18 members, 17 not, 14 *cannot be read*. Twelve of those 14 are adopters no exit source covers
    (Colombia, Turkey, Egypt, Salvador, Costa Rica, Ecuador, the Philippines, the Straits Settlements, Siam,
    Bolivia, Nicaragua, and Uruguay, whose source contradicts itself); the other two are India and Romania,
    members whose suspension no P8 source dates;
  - panel 2: 21 members, 3 not (Australia, Japan, Spain);
  - panel 4 before 2012: Hammond's 27 (no adoption after 2009; the audit's M8). Finland, Spain and Slovakia
    *cannot be read*: their announcements are not frozen, and there is no fallback.
  - **panel 4 from 2012** (`4-from-2012`, AREAER's 18 candidates):
    - **5 adopters**: the Dominican Republic, Japan, Russia, Costa Rica and Mauritius.
    - **4 not adopters**:
      - Seychelles and Kenya, whose frozen documents give no numerical target;
      - Paraguay and Uganda, **pre-2012 adopters**: the BCP's July 2013 document recounts 18 May 2011, and the
        Bank of Uganda's Monetary Policy Statement of July 2011 announces "inflation targeting lite" with a 5%
        target.

      Uganda's statement names "the BOU's policy target of 5 percent" as a target already set, so its adoption
      may be earlier than July 2011. Either way it falls before 2012.

      Hammond's 27 hold neither, so each is a gap in the pre-2012 list, said and never added. R-A3 (AREAER's
      first listing) and R-A4 (the announcement) disagree there, and this is said.
    - **9 *cannot be read***:
      - India: the agreement's own text cannot be had, and the government's reply only reports it;
      - Uruguay, Jamaica, Sri Lanka and Mongolia;
      - Argentina, Ukraine, Kazakhstan and Uzbekistan, whose frozen documents are later or transition
        documents (the variant).
    - Cobham's 12 four-category candidates and 5 full-only ones are variants conditioned on behaviour, each
      *cannot be read*.
  - P11's variant: Bolivia, Chile, India and Lebanon dated; Egypt *cannot be read*; Uruguay, China and Lao
    not candidates.
- **Agreement** (`agreement.json`, n = 21, the second coder's sample; panel 2 is compared on note 7, which
  both coders coded as their headline):
  - change dates identical in 15 of 15;
  - κ on status 1.0 per panel;
  - κ on membership: 0.887 as coded (panel 1 0.833), 1.0 after section 1's settlement;
  - the one disagreement is Romania's label (a member whose change cannot be dated), settled by section 1;
  - panel 4's κ on membership is undefined (every candidate a member for both coders);
  - the samples are small (10, 5, 6): κ carries no claim, as section 8 says.
  - **The from-2012 readings had no second coder.** AREAER's column was coded by two coders (`ft001-a-areaer`),
    but the announcements were read by the session alone (section 17). Section 8 gives that list its own draw.
    The third build's small check read all 18 candidates blind against their frozen documents and agreed on 18
    of 18. It stands in for that draw, which is said. This build's small check
    (`bank/checks/FT-001-M4-frame-a-fourth-build-2026-10-02-sonnet-small-check.md`, ready after C, no B) read
    the two new documents blind and agreed with section 21.
- **Chapter against working paper** (panel 2, `coders/a1/bj-chapter-vs-wp.csv`): four cells differ, all in
  "Return to gold", left blank in the working paper for Australia, Estonia, Finland and Greece. Under the
  working paper Estonia, Finland and Greece would not be members (21 → 18).
- **Cases the rules settle only by a reading, printed on their lines**:
  - suspension against practice for the United Kingdom (Bordo and Kydland: conversion prevented; Brown: no
    suspension), Australia in July 1915 (a suspension in Bordo and Schwartz; an export stop in the
    chronology and in Brown), Canada and the Netherlands;
  - Japan (Mitchener and Weidenmier end adherence in 1914; Bordo and Schwartz date a suspension in 1917,
    after the span: no change);
  - Sweden (Bordo and Schwartz: suspended in 1914; Bordo and Kydland: the prewar parity kept);
  - Russia's calendar, unstated, which decides "before 31 July" (flagged).
- **Coverage of panel 1's exit source** (the audit's M6): Mitchener and Weidenmier cover the countries that
  had short-term interest rates and stayed two years on gold, so panel 1's *cannot be read* are the
  periphery. Obstfeld and Taylor give prewar periods for their four exceptions only (M7).
- **Cobham's country-years were read under the working reading** "FIT" before the legend was frozen (the
  audit's M2; the first coder's `choices.md` §5.1).
- **What cannot be read**:
  - a regime at any date before 1946 other than frame a's two moments, and convertibility from 1937 to
    1971 (the protocol's §10.7). M3's panel reads the regime before 1946 from these lists; frame c's
    "convertible" before 1971 waits on this commit;
  - the 11 candidates from 2012 whose announcements are not frozen or not the act;
  - Wolf's list (a purchase).
- **Slips, said**: both coders met values they did not use while locating tables — sterling's dollar rate
  in 1914–16, gold holdings and wholesale prices in Brown and Bernanke and James, bond yields in a figure of
  Bordo and Rockoff — and Hammond's current targets (policy, not outcomes). The protocol's producer saw the
  labels of Hammond's Chart 1 axis (its header). No reading depends on them.
