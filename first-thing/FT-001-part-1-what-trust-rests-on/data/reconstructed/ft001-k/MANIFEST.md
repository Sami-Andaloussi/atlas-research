# ft001-k — reconstructed dataset

FT-001's frame k, "flee or stay", for claim 3, which is **told, not counted**. There is one case line per entry: the
last year of a run of real deposit returns below −5%. The entry is placed in a cell, open or closed, as it stood at
entry and in the year before. What holders did over the next W years sits beside it, in three measures: m1, m1c and
m2, each with its blind spot. **There is no margin, no test and no verdict** (M0, claim 3).

The rules are the protocol `bank/maps/FT-001/missions/FT-001-M3-frame-k.md`:
- **sections 1–8**: committed alone before any entry was computed (18a252e);
- **section 9**: the readings settled with the code (76173c3);
- **section 10**: currency unions, after a first build that was not committed (8188c98);
- **section 11**: the deep audit's findings followed (`bank/checks/FT-001-M3-frame-k-2026-10-01-opus-audit.md`);
- **section 12**: settled with section 11's code (4eeec75);
- **section 13**: a World Bank GDP with no common year is not used (ee9dca5);
- **section 14**: the narrow re-check answered (4b87a2a). It adds a units screen on dollar GDP and the variant
  `war-unreadable-as-no`.

M0 v4.2 applies, and its pair hash is on every line (commit 3163162). The code is `missions/code/frame_k.py`, with
105 tests in `test_frame_k.py` at the fourth build (93 at the third). A Sonnet producer wrote it, and the session applied sections 9–14 (697e113,
68374c6, a1c3209, 8397c2c and 6226207).

**This is the fourth committed build** (2026-10-02). It differs from the third by two readings, each written
before it ran (sections 15 and 16) and coded and tested before it (5479e73, K26–K27):
- **W12** (section 15): after COW's coverage, a war year reads *no* where UCDP/PRIO v26.1 lists the state as party
  to no conflict of cumulative intensity 1. The third build's reading is the variant `war-before-w12`. Its file
  equals the third build's `series.csv` line for line, except for the `variant` column, which was checked.
  `war-moves.csv` lists the 45 lines whose war reading at entry moved.
- **AREAER** (section 16): the variant `areaer`, which reads residents' foreign exchange accounts at home from
  the IMF's country chapters (`areaer/`, 98df7a2).
The fourth build's figures come first in "Uncertainty". The third build's description follows as it was written.
**The rest of this manifest describes the third build**: in Sources, Steps and Assumptions, "this build" is the
third. Where the fourth differs: it writes 18 variant files, not 16; 21 lines have their war year at entry unread
(17 of them a war year read *yes*), not 27; the counted list runs to 2021, not 2007; and of the 17 lines with
`censored` "yes", 5 are now *censored* (their so-far values are in the headline), 10 *cannot be read* and 2 apart.
`m0.py list_problems` and `ft.data.reconstructed.problems("ft001-k")` find no problem in the fourth build.

**This is the third committed build** (2026-10-01). The first was a1aa13b. The second, 81e6544, went to a narrow
re-check (Opus, isolated: `bank/checks/FT-001-M3-frame-k-2026-10-01-opus-recheck.md`). Its verdict was **not
yet**, with two Bs:
- a units break inside IFS's own rate (Belarus 2000);
- no entry counted after 2007, for want of a war reading.

Both are answered in section 14, together with its eight Cs.
- A run of this build **before section 13** was not committed. Its all-strata m2 means for the closed cells were
  about 5 × 10¹⁰ % of GDP. The cause was Venezuela: IFS has no GDP for it, the World Bank's is in today's bolívar,
  and the rate is in each year's units. Section 13 was written **after those values were seen**, and is said as
  such, as section 10 was.
- Its effect is that Venezuela's six entries read m2 as *cannot be read* (section 13 named the five whose m2 had been read; C8). Venezuela 1995 goes from counted to
  *cannot be read*, since it is left with neither measure.

## Sources

- **Real deposit return**: IFS `FIDR_PA` (annual) less π. π is the panel's annual reader in M0's order
  (`panel.Panel.pi_annual`).
- **Deposit freezes**: Laeven and Valencia (2026), the "Resolution Details" sheet: each Deposit Freeze with its date
  and duration (`laeven-valencia/systemic-banking-crises-2026`).
- **Forced**: Chinn and Ito's `ka_open` (`panel.ka_open`, 1970–2023).
- **A substitute at hand**:
  - **Land borders**: COW Direct Contiguity v3.2, type 1, 1816–2016 (`cow/direct-contiguity-v3.2`).
  - **The dollar and euro economies**: built by rule (section 11) and written to `dollar-euro.csv` (82 rows). They
    are the United States, the euro members from their entry (the ECB's list), and the economies with no separate
    legal tender anchored to the dollar or the euro in Ilzetzki, Reinhart and Rogoff's classes (1946–2016).
    - **Named exclusions**: Eritrea to 1997, Serbia 2001–02, Vietnam 1950–55, and Greece 1999–2000 (the drachma).
    - **Named additions**: Montenegro, Kosovo, Andorra and Timor-Leste.
    - **Kept against the audit**: the Dominican Republic 1946–47, whose legal tender was the dollar until 1947
      (section 12).
    - **Never included**: a currency union's members (section 10).
- **m1c**: IFS `FDSBC`, then `14A` before a money's first survey reading, deflated by IFS `PCPI_IX`. These are the
  phases list's readers, with its units-glitch screen.
- **m2**: IFS BOP, BPM6, in US dollars. It is the net acquisition of direct, portfolio and other investment assets
  (`BFDA`, `BFPA`, `BFOA`) plus net errors and omissions (`BOP`), over GDP in dollars.
  - **GDP in local currency** comes from IFS `NGDP_XDC`, then the World Bank's `NY.GDP.MKTP.CN` where IFS has none.
    The World Bank's figure is used only where it agrees with IFS within a factor of 2 in **every** common year,
    and never with no common year (section 13).
  - **The rate** is the year average of IFS's monthly `ENDE_XDC_USD_RATE`, all twelve months read.
  - **The units screen** (section 14, K24) treats a year whose dollar GDP differs from the year before's by more
    than a factor of 20 as a break. The segment after the last break is kept, and earlier years are not read.
    Breaks found:

    | Money | Break |
    |---|---|
    | Belarus | 2000 |
    | Ecuador | 2000 |
    | Laos | 1984 |
    | Myanmar | 2012, the official rate's unification |
    | Nicaragua | 1988 |
    | San Marino | 1999 |
    | Suriname | 2014 and 2015: one bad IFS year (SRD 503m against 17.3bn), not a redenomination. It drops 2006–2013, where no entry falls. |

    Nine entries are flagged `gdp_units_break`: Belarus 1994 and 1998, and seven Myanmar entries before 2012.
    - Three counted lines (Myanmar 1994, 2002 and 2007) lack m2 because of the screen. Belarus 1998, the only
      counted line lost, goes to *cannot be read* (56 → 55).
    - **What the screen does not catch** (the narrow check, C2): errors without a one-year step of 20. These are
      Iraq 1960–87, Guinea-Bissau 1970–86, Equatorial Guinea 2006–23 (IFS a thousand times too small) and
      Burkina Faso's zero GDP before 1999. Section 14 was wrong to say it covers Iraq and Guinea-Bissau.
    - No entry reads any of those years, so nothing moves. Iran 1992–93 moves 14 times in a year, below the
      line, and is kept.

## Steps

1. The protocol was committed alone. The producer inspected structures only. The first build (a1aa13b) was followed
   by a deep audit (Opus, isolated), answered in sections 11 and 12, then coded (a1c3209).
2. A run of the second build showed Venezuela's m2. Section 13 was written and coded (8397c2c), and the build was
   run again and committed (81e6544).
3. Its narrow re-check was answered in section 14 (4b87a2a) and coded (6226207).
4. **This build** (`frame_k.py build --go`) wrote:
   - `series.csv` (177 lines);
   - `shown.csv`, the told table;
   - `shown-variants.csv`;
   - `dollar-euro.csv`;
   - 16 variants.
5. **Coverage**, counted in money-years:

   | Measure | Money-years |
   |---|---|
   | Deposit rate | 4,787 |
   | π | 11,115 |
   | Real return | 4,447 |
   | ka_open | 6,503 |
   | Real currency (m1c) | 6,624 |
   | Outflows (m2) | 5,459 |
   | GDP in dollars | 7,625 (3,395 from the World Bank), after the units screen |
   | Freeze years | 27 |

   - **The World Bank's GDP was refused for 14 monies.** Thirteen fail the seam: BEN, BLR, BLZ, COD, GAB, GNQ, HTI,
     LBR, NIC, SLE, SOM, SUR and ZWE. Venezuela has no common year.
   - **The regimes end** in 2016 (borders and classes) and 2015 (anchors). Each is carried from its own last year,
     and flagged.
6. `m0.py list_problems` found no problem on `series.csv` and the 16 variants. `ft.data.reconstructed.problems("ft001-k")`
   is empty.

## Assumptions

- **Sections 2–4 and 9–13.**
  - The entry is the last year of N = 2 years below −5%, from 1970, one per W = 3 years. A year that is unread or
    under a freeze breaks a run.
  - **Forced** means ka_open ≤ 0.25 alone. No source dates bans on holding foreign money.
  - **Open** means not forced, and a land border with a dollar or euro economy in the entry year.
  - Not forced with no such border is ***cannot be read***, never "closed".
  - **m1 is readable nowhere.**
  - m2 leaves out derivatives; the variant `with-derivatives` keeps them. Errors and omissions enter with their sign
    reversed.
  - **m2's blind spots** (C1): it sees only what crosses the border. Where dollar GDP is taken at an official rate
    far from the market, m2 is biased down, on the closed side above all (Ghana 1983, Nigeria 1984,
    Egypt 1988).
- **The statuses, in order** (sections 11–12):
  1. **Not a money of its own** (apart, 10 lines): CAF 1995, FSM 2009, GNQ 1995, KNA 1981, MNE 2023, TCD 2009,
     TLS 2008, 2012 and 2023, and ZWE 2019.
  2. **A war year at entry** (apart, 9 lines): LBY 1984, MMR 1976 and 1986, NGA 1993, PAK 2005, PER 1989, PHL 1980,
     RUS 2003 and ZWE 2000.
     - An entry year whose war status cannot be read is *cannot be read*: 27 lines.
       - **`war.py` cannot read war after 2007** (its W9). COW's war files end there, and a state's losses
         abroad after 2007 are not seen.
       - So **the headline's counted list runs 1970–2007**, and no line reaches *censored*.
       - The variant **`war-unreadable-as-no`** reads an unreadable entry year as no war, as frames c and d
         do. It counts 70 (69 closed, 1 open), 13 of them after 2007, and holds 8 censored lines with their
         so-far values.
       - Of those 8, three are open: Botswana 2022, Mexico 2022 and North Macedonia 2023.
       - Eight more war-at-entry lines show as *cannot be read* here and would be apart if war were read (C4).
       - **The variant reads every unreadable war year at entry as no war**, not only those after 2007. Three of
         the 27 are not W9's: Angola 2000, Ethiopia 2006 and Myanmar 1990. These are war years whose own
         losses cannot be read, and they count as closed in the variant. Myanmar 1990 is also flagged
         `war_in_window`. Read without them, the variant would count 68 (67 closed).
     - War inside the window is flagged `war_in_window` (26 lines). The variant `war-in-window-apart` sets those
       lines apart.
  3. **A cell that changed in the year before** (apart): MEX 1987.
  4. **Cannot be read**:
     - 69 lines for the cell, most of them not forced with no dollar or euro border;
     - 6 lines with neither m1c nor m2 read, among them Venezuela 1995 (section 13) and Belarus 1998 (section 14).
  5. **Counted.**
- **The producer's readings K1–K23** (`frame_k.py`'s docstring) are kept, including:
  - censoring at each measure's panel end (2024). The `censored` column is "yes" on 17 lines, but in the
    headline every one of them is set apart or *cannot be read* first. The so-far values exist in the variant
    `war-unreadable-as-no` only (C4).
  - the United States as the dollar's issuer, with its money its own;
  - `no-carry` dropping 2016 for IRR's spans;
  - Andorra read as using the euro from 2002.
- **What section 11 promised to say** (C4):
  - Zimbabwe 2019 is apart as "not a money of its own" through a carried regime that is wrong in fact: Zimbabwe
    had its own currency again from 2019.
  - ka_open has a cluster at 0.2557, just above the 0.25 line, so `kaopen-050` and the headline differ by those
    monies.
  - The dollar-euro list moves no headline line.
- **Freezes**:
  - Two Ukrainian money-years below the line are removed by their freeze (2015 at −35.69% and 2017 at −5.31%), and
    said (C5).
  - Argentina's freeze of 28 December 1989 "lasting 120 months" is read as written: 1989–1999.
    - The 120 months may be the Bonex bonds' maturity, a conjecture the sheet does not state.
    - Argentina has no deposit rate before 2010, so the reading moves no entry.
- **Flags** on the lines:
  - `gdp_worldbank`: 51;
  - `gdp_units_break`: 9;
  - `war_in_window`: 26;
  - `regime_carried`: 19;
  - `m1c:seam` / `m1c_net:seam`: 10 and 16.

## Uncertainty

**The fourth build (2026-10-02)**:
- **The headline, by status**: the same 177 entries. **65 counted** (64 closed, **1 open**: Mexico 1977), **87
  *cannot be read***, **20 apart**, **5 censored**.
- **What W12 moved**: 15 statuses, all from *cannot be read*, all entries from 2008. Nothing else moved.
  - 10 became counted, all closed (forced): Angola 2008, 2012, 2016 and 2020; Belarus 2012; Solomon Islands
    2012; Suriname 2017 and 2021; Tanzania 2012; Venezuela 2008.
  - 5 became censored: Algeria 2022, Moldova 2023, Solomon Islands 2023 and Samoa 2023, all closed; and North
    Macedonia 2023, open across its border.
- **The other open cells**: Botswana 2022 and Mexico 2022 stay *cannot be read*. UCDP lists each as a party (a
  secondary supporter) to a conflict whose deaths had passed 1,000 by that year, and its own losses are unseen. Russia 2003 stays apart (a war year).
- **The told table still cannot compare.** One open line stands against 64 closed.

  | Measure, all strata | n open | n closed | closed: median |
  |---|---|---|---|
  | m1c gross | 1 | 58 | 0.12 |
  | m1c net | 1 | 48 | 0.07 |
  | m2 gross (% of GDP) | 0 | 48 | 2.50 |
  | m2 net (% of GDP) | 0 | 45 | 0.20 |

- **The variant `areaer`** makes Argentina 2021 and Haiti 2021 counted and open. Both are not forced, and AREAER
  prints that residents may hold foreign exchange accounts at home. Their lines also carry `regime_carried`.
  - KGZ 2022, NIC 2023 and VUT 2023 become censored. Nigeria 2021 becomes apart (a war year in its window).
  - So the variant has **3** open counted lines (Mexico 1977, Argentina 2021, Haiti 2021) against 64 closed.
  - m1c is read on two of them, Haiti 2021 and Mexico 1977 (Argentina 2021 has none). Their median is −0.16,
    against the closed cells' 0.12. On two lines nothing carries, and nothing is read.
  - AREAER's "not permitted" reaches no entry (only Venezuela 2010 prints it). The variant moves no cell to
    closed.
  - G11 said AREAER cannot move a conclusion. With 3 open lines against 64, it does not: the told claim 3
    stays "cannot compare".
- **The variant `war-before-w12`** is the third build: 55 counted.
- **Other variants moved with W12** (counted lines, open / closed):
  - `N1`: 6 / 97 (m1c read on 6 / 86);
  - **`line-0`** (every year with a negative real return): 24 / 128 (m1c read on 23 / 117). **This is the first
    reading whose open side passes the twin's floor of 20.** Its m1c gross median is 0.164 open against 0.126
    closed: a variant, told, not the headline. The open lines are mostly Mexico, Costa Rica, Canada and
    Guatemala.
  - The rest have 0 to 3 open lines.
  - The third build's sentences below ("too thin in every variant", "only `line-0` gives … 14 open") describe the
    third build. Under W12, `line-0` is no longer too thin.
- **What was seen for the fourth build**: the counts, the moved lines' names, and the told table's rows for the
  headline and the two new variants.


**The third build (2026-10-01), as written then:**

- **The headline, by status.** There are 177 entries: 1970s 17, 1980s 30, 1990s 40, 2000s 41, 2010s 24 and 2020s 25.
  - **55 counted**: 54 closed and **1 open**, Mexico 1977, across its border with the United States.
  - **102 *cannot be read***.
  - **20 apart**.
- **The other open cells are not counted.**
  - Russia 2003 (border with Finland) is apart: 2003 is a war year for Russia.
  - Botswana 2022, Mexico 2022 and North Macedonia 2023 are *cannot be read*, because `war.py` cannot read war after 2007
    (W9). The variant `war-unreadable-as-no` reads them as censored, with their so-far
    values.
- **The told table cannot compare.** One open line stands against 54 closed. No open-minus-closed difference carries
  anything, and none is read.

  | Measure, all strata | n open | n closed | closed: median |
  |---|---|---|---|
  | m1c gross | 1 | 48 | 0.13 |
  | m1c net | 1 | 40 | 0.07 |
  | m2 gross (% of GDP) | 0 | 40 | 2.27 |
  | m2 net (% of GDP) | 0 | 37 | 0.68 |

  - m1c is read for 49 of the 55 counted lines and m2 for 40. Where m2 is missing, the cause is a gap in the
    balance of payments or a missing dollar GDP (C6).
  - `shown.csv` prints every cell with its n, as the protocol says.
  - The closed m2 means are pulled up by single lines.
    - Zambia 1986 reads 121% of GDP over the window, mostly one year's errors and omissions (1989, −$1.71bn)
      (C7).
    - Angola 2004 reads 70%.
    - Their dollar GDP was checked and reads in the right range. The medians are the safer description.
- **What the closed side is.** Every closed cell is forced on ka_open. The closed side means the capital account
  was closed on ka_open. It says nothing about deposits.
- **The variants** (counted lines, open and closed):

  | Variant | Open | Closed |
  |---|---|---|
  | N1 | 3 | 78 |
  | N3 | 2 | 26 |
  | W2 | 2 | 61 |
  | W5 | 2 | 40 |
  | line-0 | 14 | 92 |
  | line-10 | 1 | 28 |
  | kaopen-010 | 3 | 16 |
  | kaopen-050 | 1 | 68 |
  | fisher | 2 | 45 |
  | net | 1 | 52 |
  | class1-only | 0 | 54 |
  | with-derivatives | 1 | 48 |
  | neo-negative-only | 1 | 54 |
  | no-carry | 1 | 54 |
  | war-in-window-apart | 1 | 51 |
  | war-unreadable-as-no | 1 | 69 |

  - Only `line-0` (every year with a negative real return) gives an open side of more than three lines: 14 open,
    from Canada, Costa Rica, Guatemala, Indonesia, Mexico and Russia.
  - Even there, the open cells are those of the few monies with such a border.
- **Too thin.** With 20 per side as the twin's floor, the open side is too thin in the headline and in every
  variant. Claim 3 stays told.
- **What part 1 can say.** The sources date neither the legality of foreign-currency deposits nor bans on them.
  The open/closed split therefore rests on capital controls and a handful of land borders. This list shows where
  the capital account was closed on ka_open (C2), not where holders could leave. The question stays open, and that is the record.
- **What was seen**:
  - the coverage-only runs;
  - the first build's cells and open lines;
  - the uncommitted run before section 13 (statuses, open lines, the all-strata table and the m2 values above 30%
    of GDP that led to section 13);
  - the second build's re-check, which recomputed every figure;
  - this build's statuses, cells, open lines, flags, units breaks, all-strata rows and the variants' counts.
