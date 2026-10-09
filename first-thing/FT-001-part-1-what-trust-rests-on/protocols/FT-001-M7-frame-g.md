# FT-001 — M7: frame g, the stablecoins (claim 4 and A9, told)

> Mission M7 of `bank/dossiers/FT-001-the-life-of-a-money.md`, section 14. The E2 session (`plan/e2-ft001.md`)
> wrote it on 2026-10-01, **before any coin is listed or mapped**, and committed it alone first.
>
> **The rules are M0's**, version 4.2 (`FT-001-M0-rules.md` and its twin, commit 3163162):
> - section 2's **private issuer's supports**: redemption, a limit by rule, a limit by institution, taken back;
> - section 5 g;
> - A9;
> - section 3's coders.
>
> **Frame g is told** (M0; D1). DefiLlama's terms bar commercial copying, and no open census of coins includes the
> dead ones, so no coin can be entered by rule. **Nothing is counted and no verdict is given.** This protocol adds
> no rule. Where M0 leaves a reading open, it chooses in the open, marked *reading*.
>
> **What was seen before writing**: the source scout's report (`M7-sources-scout-2026-10-01.md`, a Sonnet
> subagent). It gives each source's host and Guard ruling, which coins each reading names, and two sample prices it
> read to test a file (Tether's low of 0.925 on 2018-10-15). The scout's flag on M0's rule is section 5's. No coin
> was mapped and no phase was dated for this file.

## 1. What is listed, and where it goes

`data/reconstructed/ft001-g/`:
- `coins.csv`: one line per coin on the told list, with where it was named;
- `mapping.csv`: each coin's supports, by line of M0 section 2, with its source and locator, as the two coders
  settled them;
- `phases.csv`: the told phases with their dates and sources;
- `MANIFEST.md`.

The coders' files go in `coders/` beside them.

Frame g follows no other list. It is never pooled into claim 5's odds or into test (ii).

## 2. The told list (by the fixed readings; M0 "named in sourced reading")

*Reading*: "sourced reading" is a **fixed set of readings, frozen before the list is drawn**. It is not a search.
A coin is on the list when one of these names it as a stablecoin. The set:

| Reading | Host (ruling) | What it brings |
|---|---|---|
| Kosse, Glowka, Mattei and Rice, BIS Papers 141 (2023), Annex 1 | www.bis.org (allow) | 68 coins, survivors |
| Ahmed, Aldasoro and Duley, BIS WP 1164 | www.bis.org (allow) | the 2023 runs |
| Aldasoro, Mehrling and Neilson, BIS WP 1146 | www.bis.org (allow) | NuBits and BitUSD, the first coins |
| BIS WP 1219 and BIS WP 1270 | www.bis.org (allow) | the large coins |
| Federal Reserve IFDP 1334 (10.17016/IFDP.2022.1334) and the three FEDS Notes the scout read | www.federalreserve.gov (allow) | failed coins (IRON, Fei, Basis); USDC and BUSD in 2023 |
| NBER w30796, w27136, w31160 (Liu, Makarov and Schoar) and w30256 (Uhlig) | www.nber.org (allow) | Terra and UST, cited, out of the mapping |
| Mizrach, arXiv 2201.01392 | arxiv.org (ruled before freezing) | **the census of dead coins** |

- **Terra and UST are out of the mapping** (M0; the dossier). Their model is LL-332's, cited from Liu, Makarov and
  Schoar and from Uhlig.
- **Readings that cannot be had** are said and not replaced: Anadu et al. and the FSB's reports sit on denied
  hosts, and Gorton and Zhang on SSRN, also denied. A coin named only there is not on the list.
- *Reading*: a name that is a token of a protocol, never redeemable for a fiat unit (a governance token), is not
  a stablecoin, even where a reading lists it beside them.

## 3. The mapping (two coders apart; M0 section 2's private-issuer lines)

For each coin, each line of M0 section 2 is coded as it stood at the coin's launch and at each phase. The four
lines are:
- **redemption**: the terms give holders a right to redeem at par on demand. Who may redeem is recorded: any
  holder, or verified customers only.
- **a limit by rule**: issue is tied by contract or code to reserves held one for one, or to a stated cap. A
  target alone does not count.
- **a limit by institution**: the issuer is supervised under a law that limits its issue.
- **taken back**: the issuer accepts the coin for its own fees or claims.

Each line is coded *yes*, *no* or *cannot be read*, with a source and a locator. A mechanism that meets none of
the lines is outside the list, and is said.

- Two coders work apart, each from the same packet: the coin, its launch year, and the frozen readings' locators
  that name it.
- κ is reported on coin-lines. Disagreements are settled by M0's text, never by the coin's fate.
- The coders are outcome-aware, since the coins' histories are known. This is said.
- **Sources for the terms**, in order:
  1. the issuer's own documents, where frozen from an allowed host;
  2. regulators' filings (SEC prospectuses, state licences) and central-bank notes;
  3. the readings of section 2.

  *Reading*: every issuer host the scout ruled is denied. They are declared, never opened, and an archive's copy
  of a denied host is never used. A line that only such a host could settle is *cannot be read*.

## 4. The phases (A9; used only to date, never to count)

- **"Two prices"**: redemption halted, gated or limited by the issuer's notice.
  - *Reading*: with the issuers' hosts denied, a notice is dated from a filing or a central-bank note that reports
    it. Examples are Circle's SEC 424B4 on the March 2023 backlog, and the Federal Reserve's notes on USDC (March
    2023) and BUSD (February 2023). The line says so (`notice_reported_by`).
- **"Broke"**: below par by **3%** [1; 10] for **7 consecutive days** [1; 30], on a daily price.
  - **The price source**: Gandal, Hamrick, Moore and Vasek's replication data (Harvard Dataverse,
    doi:10.7910/DVN/H98LCZ and JPEF8T, CC0 1.0). It holds daily OHLC to October 2019, NuBits to February 2018, and
    dead coins, read through the tabular API.
    - *Reading*: the deposit does not name its price vendor, so upstream rights are unverified. This is said.
  - After October 2019, **no allowed daily source exists**. Every price vendor's host is denied, and the
    Dataverse deposits that cover 2020–2025 are synthetic ("pseudo data"). "Broke" *cannot be read* after
    2019 and is said.
  - The session declares the wall: one keyless daily source, its terms read first, via `policy-demander`. The
    choice is Sami's.
- **What M0's line misses, said**: 3% for 7 days would register neither USDC in March 2023 (back near par within
  about 3 days) nor Tether in October 2018 (its close never below about 0.97). The grid's corners (1%, 1 day)
  show them. M0 is fixed, and the told phases print the grid beside the headline.
- Each phase carries its date, source and locator. The order of the phases is kept (A9). No rate, share or odds
  is computed.

## 5. Order of commits, checks and audit

1. This protocol, alone, with the scout's report.
2. The readings of section 2, frozen (manifests committed; texts never), each host ruled first.
3. The told list (`coins.csv`) drawn by script from the frozen texts' names, with a person's check of each
   name, and committed before any mapping.
4. The coders' packet and README, committed. Then the two coders, κ, the settlements, and `mapping.csv`.
5. The Gandal data frozen; then the phases (`phases.csv`) and the manifest.
6. A small check (Sonnet, isolated): frame g is told, so a deep audit is not needed unless the small check finds a
   B.

*The barrier*: the fixed readings, the commit order, and the second coder. *What no code holds*: that no coin was
added because its story is known. The list is drawn from the frozen texts alone, and the manifest gives each
coin's reading.

## 6. Readings settled with the told list's code (2026-10-01, before the list is drawn)

A Sonnet producer wrote `frame_g.py` and `test_frame_g.py` (26 tests). It inspected the readings' layout only, and
ran the coverage mode, which prints counts. It named its readings G1–G8, and the session keeps them, with one
change to G1.
- **G1, the fixed set, widened before the list is drawn.** Section 2 said Anadu et al. and the FSB's reports
  cannot be had. Sami's request 0e6f6355440d then opened `www.newyorkfed.org` and `www.fsb.org`, and the three
  were frozen (`frame-g/nyfed-anadu-runs`, `frame-g/fsb-2020-global-stablecoins`,
  `frame-g/fsb-2023-crypto-stablecoins`). The set is fixed when the list is drawn, not when this protocol was
  written. So **the three join the set**, and the order of section 5 holds: the set is frozen, then the list is
  drawn. Gorton and Zhang (SSRN) stay out.
- **G2**: BIS Papers 141's Annex 1 is a table (68 rows). Mizrach's census of dead coins is prose. It is read by a
  "Name (TICKER)" pattern inside its two passages.
  - The coins that passage prints with no ticker (the Italian Lira coin, Ampleforth, Carbon, Reserve, Huobi as a
    bare word) are added at the person's check, each with its page. They come from the fixed reading, not from
    a search.
- **G3**: in the other readings, a candidate is a name from the structured lists or their aliases, or a token in
  four fixed patterns. Acronyms that are not coins are set aside and listed.
- **G4**: Terra and its tickers stay in the draft, marked excluded with the reason.
- **G5**: a "governance token" within 120 characters marks a candidate `governance?`. Nothing is dropped by
  script. The person decides, under section 2's reading.
- **G6–G8**: what the script cannot find is said (single words outside the lists, the examples column of IFDP
  1334's table of mechanisms); the deduplication runs on an alias table, each alias with its reason; pages are
  PDF pages.
- **The person's check** reads every line of the draft against its occurrences (`coins-draft-occurrences.csv`)
  and writes `check`:
  - keep;
  - not a coin (noise such as "Biden Administration");
  - merge with another line;
  - governance token;
  - excluded (Terra).

  Each decision cites a page. It is the session's check, and a second reader (Sonnet, isolated) rechecks it
  before `coins.csv` is committed.

## 7. "Broke" after 2019 read from a stated path (2026-10-01, before any phase is dated)

Section 4 left "broke" *cannot be read* after October 2019, because no allowed daily price source exists. Sami
asked (through the engine session, 2026-10-01) that this not stop at "no price vendor". FRAMING F59 allows a
specialist agent consulted as an expert: it is a resource, never a source. The session takes that route, under
these readings:

- *Reading* of M0's "on a daily price": the line needs the price on each of the days, not a vendor's file. A
  **source that states the daily path** meets it. Three kinds of statement count:
  - a text that gives the price below a level over dated days, for example "below $0.97 from 11 to 13 March";
  - a table of daily prices;
  - a figure's own data, for example a Federal Reserve note's "Accessible Data", which lists the plotted values.

  A figure read by eye does not count, and neither does a single low ("fell to 0.87") with no duration. M0 is
  unchanged and no rules version is needed: frame g is told, nothing is counted, and M0 names no price source.
- **The map.** An isolated expert agent (Opus, from its own knowledge, with no tool that reads the web) lists,
  for each depeg episode after October 2019 that it knows, how far below par the coin went, for how long, and
  **which documents state it**. Its answer is a map, never cited, and is kept in `coders/` beside the lists.
- **The check.** Each claim is read in the document the map names, on an allowed host, ruled first and frozen
  (manifest committed, text never). Phase dating follows section 3's order of sources. A document outside
  section 2's fixed set may date a phase. It never adds a coin to the list: the list is closed by section 2.
- **What is written.** "Broke" is *yes* only where the stated path holds the price at least 3% below par for 7
  consecutive days. It is *no* where the stated path shows the coin back within 3% sooner, a dated statement
  of its return to par included ("recovery took three days" from a dated trough). It stays *cannot be
  read* where no document states the path, and it is declared as such. The grid's corners print beside it
  wherever the stated path allows.
- **What the locator found** (`coders/path-locations-2026-10-01.md`, a Sonnet subagent that reported places, not
  values). Before any value was read:
  - the frozen documents give daily or hourly **charts** for March 2020, May 2021, May 2022 and March 2023;
  - the FEDS Notes' "Accessible Data" is prose, not lists of values;
  - the only daily table is Uhlig's, for UST, which is out;
  - stated durations are few.

  So most coins stay *cannot be read* after 2019. The route is kept for what it does reach, and that is said.
- **The barrier, and what no code holds.** The barrier is the source column: every phase line names its
  document and locator, and `phases.csv` refuses a line without them. No code holds that the expert's
  knowledge did not choose which episodes were looked for. The map's list of episodes is kept, and the manifest
  says that episodes the expert did not name were not looked for.

## 8. The person's check, and the told list drawn (2026-10-02)

- **Who checked.**
  - Section 6 calls the person's check the session's. A Sonnet reader drafted it, reading every one of the 95
    draft lines at its page; every quotation was checked by script against the frozen page
    (`coders/person-check-draft-2026-10-02.csv` and `.md`).
  - The session read it and changed one decision: Havven, which the census names as a project "now rebranded as
    Synthetix", is merged with Synthetix USD. HAV is its collateral token, which section 2 keeps off.
  - A second Sonnet reader, isolated, rechecked every row against its page
    (`bank/checks/FT-001-M7-frame-g-person-check-2026-10-02-sonnet-recheck.md`). It agreed on 102 of 103 rows.
- **The recheck's answers.**
  - JPM Coin is **kept**, marked `deposit token; the issuer denies it is a stablecoin`. IFDP 1334 names it an
    institutional stablecoin, and an issuer's denial is not one of section 2's exclusions.
  - Libra/Diem, a miss, is added `keep, never issued`. It is on the list and out of the mapping, since it has no
    terms at launch.
  - Reserve gains its second citation.
- **G9, a reading made at the check**: a coin pegged to gold or another commodity is kept, marked
  `commodity-pegged` (nine coins), and the mapping reads its lines like any other.
- **The list**: 85 coins (`coins.csv`) and 15 names off it, with why (`coins-off.csv`: 14 names that are not a coin,
  and Terra). `frame_g_list.py` applies the check and adds nothing of its own.
- *What no code holds*: that a coin was not kept or dropped for its known fate. Every decision cites its page, and the
  recheck read them all.

## 9. The coders' packet (2026-10-02, before either coder starts)

A Sonnet producer wrote `frame_g_packet.py` (37 tests). It built the packet: 84 coins, Libra/Diem being out of the
mapping, each with its name, ticker, marks and the frozen readings and pages that name it
(`coders/packet/packet.csv`, one sheet per coin, and the coders' `README.md`). The builder refuses any packet that
holds a word of fate.

- *Reading*, **the launch** is what a reading prints:
  - BIS Annex 1's first price date, labelled as such: it is a first price in the data, not a launch;
  - or Mizrach's printed years.

  These are not reconciled, and 7 coins say "not printed". The coders code the terms **at launch, and at each
  change of terms a source prints** (`after-change:<what>`).
- *Reading*: **the told phases are dated apart**, by the session (section 4, section 7), never in the packet. A
  phase's terms are read from the coders' line in force at its date. This keeps fate out of the packet.
- Readings appear under neutral labels, because some folder names carry "runs". The README maps each label to its
  folder.

## 10. The two coders, κ and the settlements (2026-10-02, before `mapping.csv` is drawn)

Two Sonnet coders worked apart from the packet. Each saw only the packet, the frozen readings and its own folder.
- **κ on the launch coin-lines** (84 coins × 4 lines = 336): the coders agree on 317. Cohen's κ is **0.74**. Most
  lines are *cannot be read*, since the frozen readings give many coins only a category label.
- **19 disagreements**, settled by M0's text, never by the coin's fate. Each settlement is a row of
  `coders/settlements.csv`, with its rule:
  - **S1** (14 lines, *limit by rule* of unbacked or algorithmic coins: g2 *no*, g1 *cannot be read*). The line has
    two arms, reserves one for one **or** a stated cap. BIS's group D and Mizrach's "non-collateralised" exclude
    reserves but print nothing on a cap. A *no* needs both arms excluded, so they are **cannot be read**. g2's
    reading is told as a variant (`g2-no`).
  - **S2** (Dai, *taken back*): **yes**. The vault owner repays the Dai with the stability fee to recover the
    collateral (NBER-w27136 p.62). The protocol accepts its coin for its own claim, as M0's line words it.
    Disclosed: MIM's cauldron prints the same mechanism (NYFed-SR1073 p.48). Both coders agreed *cannot be read*
    there, and agreements are not reopened.
  - **S3** (Gemini Dollar and Liquity USD, *redemption*): **yes**. A statement that names the coin and prints the
    mechanism counts; a bare category label does not (S1). Gemini: verified customers only (NYFed-SR1073 p.8).
    LUSD: any holder (FEDS-2022).
  - **S4** (Magic Internet Money, *redemption*): **cannot be read**. p.48 prints the minter's repayment route. It
    neither grants nor excludes a right of other holders.
  - **S5** (Tether, *limit by institution*): **no**. BIS-WP1164 p.36 prints that the coin operated outside the
    purview of regulators. That is a printed absence, not silence.
  - **S6** (who may redeem: Binance USD, Pax Dollar and TrueUSD, agreed *yes*): **verified customers only**, by
    S3's rule (NYFed-SR1073 p.8). g2 had read "not printed".
- **The phases.** g1 found nine changes, g2 seven. A printed change touches the lines it names, and the other lines
  stay in force from before (**S7**). This settles the coders' two styles: g1 wrote *cannot be read* on untouched
  lines, while g2 carried the launch codes. Kept as after-change rows:
  - Dai's multi-collateral switch (2019-11, *limit by rule* yes);
  - Dai's peg stability module (undated, *redemption* yes, any holder);
  - Tether's restated backing (2019-03, *limit by rule* yes);
  - USDC's two restatements (2021-07 and 2021-08, *limit by rule* yes);
  - Frax's Version 2 (undated, *limit by rule* no, g1's reading; g2 had merged it with the vote);
  - Frax's 2023-02 vote (*limit by rule* cannot be read).
  - **S8**: an undated change dates nothing. For any dated phase, the line before it stays in force.
- **Not phases**, since no line's code changes:
  - Tether's redemption policy printed in 2023 (a later print of terms, not a dated change);
  - TrueUSD's sale (2020);
  - Paxos halting BUSD's issue (2023-02), which g1 called a fate and g2 coded with the launch codes.
- Only two after-change rows **change a code**: Dai's module (redemption no → yes) and Frax's vote (limit by rule
  no → cannot be read).
- `frame_g_mapping.py` (11 tests) draws `mapping.csv` from the two coders and the settlements, and adds nothing of
  its own. It refuses a disagreement without a settlement.

*What no code holds*: the coders are outcome-aware (section 3), and so is the session that settled them. The
barrier is that each settlement quotes M0's line and a printed page, and an isolated check reads them.

## 11. The phases' code (2026-10-02, before any phase is computed)

A Sonnet producer wrote `frame_g_phases.py` (G-P1–G-P12; 70 tests on toy data). It read the Gandal files' format
only: columns, keys, sentinels and date ranges, and computed no price statistic. The session keeps its readings:
- **G-P1, the barrier**: a stated row with an empty or placeholder source or locator is refused, as section 7
  says.
- **G-P2–G-P5, runs**: consecutive calendar days at or below par × (1 − d). A missing day breaks a run, which can
  hide a break but never invent one. A close at or below 1e-50 is a filler (about 58,000 rows carry 9.9e-99) and
  is a day not read.
- **G-P6, spans**: a coin's series is read from its first to its last read day. After that, to October 2019, it is
  *cannot be read*, and after October 2019 only stated rows speak (G-P9).
  - The coins file ends on 2018-02-06, the tokens file on 2019-10-21.
- **G-P7, par**: 1 only for a peg printed as exactly "USD", or a par the session sets in `gandal-names.csv`. A coin
  pegged to the euro, gold or another coin is *cannot be read*: the frozen files hold no price for its peg, and a
  par for it would be invented.
- **Gandal's key** is the exact `market` string, since the `id` column is empty. The session writes
  `coders/gandal-names.csv` after reading the coverage, and the build refuses to guess.
- **The names table** (`coders/gandal-names.csv`, the session, after the coverage run, which prints names and
  days only). 19 of the 85 coins have a Gandal series by exact name or ticker.
  - The coverage's name-prefix candidates are not taken, since each is another asset: Bean Cash, Carboncoin,
    Magi, ParallelCoin, Reserve Rights, and Tether for Tether Gold. Stronghold's ticker SHX is the Stronghold
    token, so its series is left out as ambiguous.
  - The first coverage runs also found Gandal's markers for a missing date, `-` (46 rows) and `NA` (25). They are
    read as no date (G-P2's refusal had stopped the run).

## 12. The stated phases, drafted and read (2026-10-02, before the phases' build)

A Sonnet reader drafted `coders/phases-stated.csv` from the frozen documents and a few more, each on an allowed
host, ruled first and frozen. It also wrote `phases-stated-README.md`, which lists the hosts, the freezes and the
expert map's episodes, found or not. A script checked that every quote is verbatim in its document. The session
read every row.
- **53 rows**:
  - two prices: 5 yes (USDC, March 2023), 3 no (BUSD, issuance halted but redemption stated open; Tether, March
    2023), 2 *cannot be read*;
  - broke: 29 no, 14 *cannot be read*.
- **S-G1, a stated minimum is a path's bound.** A minimum printed for a dated window (a table's "Min" column, or an
  end-of-day extreme) bounds every day of that window. A minimum within 3% of par therefore reads *no* for the window.
  A minimum below the line, with no duration, is *cannot be read* (Fei, Neutrino USD). Section 7's three kinds
  name texts, tables and figures' data; a minimum is the narrowest text of the first kind. This was decided before
  the build, from the rows' notes.
- **"Barely above and below one dollar"** (a FEDS Note's figure description) gives no level. Its two rows (Tether,
  USDC, 2021–22) are *cannot be read*.
- **USDC, March 2023**: the Fed's notes report Circle's notice pausing redemptions over the weekend of 10–13 March
  (two prices, yes). Circle's own 424B4 (2025) says it honoured one-for-one redemption for Circle Mint customers
  at all times. Both rows are kept, and the conflict is told.
- **Dated returns**: USDC and Dai fell under 90 cents on 11 March 2023 and were back at the dollar by 14 March:
  *no* at 3% for 7 days. The grid's corners (1 day) would read *yes*, as section 4 foresaw.
- **Not found**: FDUSD, MIM, TrueUSD in 2023–24, HUSD after May 2022 and Frax have no stated path. Three of the
  expert map's episodes name coins outside the list (aUSD, USDR, USDe), and they are not added (section 7).

## 13. The mapping's small check answered (2026-10-02, after `mapping.csv` had been drawn and checked)

The small check (Sonnet, isolated: `bank/checks/FT-001-M7-frame-g-mapping-2026-10-02-sonnet-small-check.md`) recomputed
κ (0.7426, 317 of 336) and found every count right. Its verdict was **not ready**, for one A and one B:
- **A1**: who may redeem was recorded for 5 of the 9 *redemption yes* lines, and S6's "verified" was a reading, since
  NYFed-SR1073 p.8 prints "a restricted set of participants";
- **B1**: S1 (a *no* needs both arms of the limit by rule excluded) governed only the disputed lines. Three *no* codes
  rest on fractional backing with the cap arm open.

**S9** (written after the check, in the open: FRAMING F72): a settled reading governs every line it covers, agreed or
not. So:
- who may redeem is recorded for the four missing lines, as each source prints it. Tether's two prints (2014 and
  2023) are kept, not settled. S6's and S3's "verified customers only" becomes the page's own words;
- IRON's and Frax's limit by rule at launch, and Frax's Version 2, become *cannot be read*;
- Magic Internet Money's *taken back* becomes *yes* by S2's reading (NYFed-SR1073 p.48: the borrower repays MIM to
  recover the collateral, as for Dai). The check's C1 had set it beside Dai's.

The check's C items are answered in `settlements.csv` (S2's locator, Liquity's category sentence, Ampleforth's S1 note)
and in the manifest (the list's arithmetic, S1–S5, later prints read as launch terms, Tether's 2019 restatement).
`frame_g_mapping.py` has 13 tests since f1ac65b (section 10 said 11, before its `series.csv`).

## 14. The issuers' own documents (G25; 2026-10-02, written before any coder reads them)

Section 3 left the issuers' own documents unread because every issuer host was denied. Sami opened them (policy
request 11, 7341cfee6974), and the engine froze launch-time versions for 17 of the 18 coins the G25 expert map ranked,
through web.archive.org and the NYDFS releases (83af35af; `data/frame-g/issuer-<slug>/2026-10-02/`, each manifest
naming every file's version date). This section revises section 3 openly (FRAMING F72): the told list is unchanged
(section 2: a document read here adds no coin), and only the four launch lines of those coins are read again.
- **Who codes.** Two Sonnet coders, apart, as in section 10: each sees only `coders/issuer-packet/` (one sheet per coin,
  naming its frozen files and their version dates, and the README with M0's four lines and the rules below) and its own
  folder (`coders/i1`, `coders/i2`). Neither sees the first coders' codes, the settlements or this mapping.
- **What a line reads** (M0 section 2's private-issuer lines, unchanged; S1, S3, S7, S8 hold):
  - a document is read for the coin's terms **at launch**. A version dated after launch reads the standing terms at
    launch unless it says the terms changed (then it is an after-change row, S7); its version date is in the locator,
    as for the readings already in hand. **S10**: a version dated more than 12 months after the launch is read and
    flagged `late print` in the note, and the page says how many lines rest on one;
  - who may redeem is recorded in the issuer's own words (S9);
  - a coder never reads a fact from memory: a line no frozen document prints stays *cannot be read*.
- **How the two layers meet (S11).** Each coin-line's final code comes from:
  1. the issuer coders' agreed code, or their disagreement settled by M0's text (a settlement row, rule S11, quoting
     M0's line and the document's words);
  2. set against the first layer (`mapping.csv`, sections 10 and 13): where the first layer read *cannot be read*, the
     issuer layer's code stands; where both read *yes* or *no* and agree, it stands; where they disagree, the issuer's
     own document prevails **only if** its version is dated at or before the launch, and otherwise the line is settled
     by M0's text, said line by line. The first layer stays in git and is told as a variant (`fixed-readings-only`).
- **Not in hand, said**: Reserve (no launch document found); Liquity's whitepaper (docsend.com) and technical papers and
  mStable's whitepaper (github.com), and PayPal USD's own terms (www.paypal.com), on refused hosts. Their lines read only
  what the frozen files print.
- **κ** is reported on the issuer layer's coin-lines (17 coins × 4), beside section 10's.
- **Checks**: a small check (Sonnet, isolated) of the issuer layer's settlements and the merged mapping, before the
  mapping is redrawn into the study.

## 15. The issuer layer coded and merged (2026-10-02, after the two issuer coders, before the small check)

- **κ on the issuer layer**: 68 coin-lines (17 coins × 4), 59 agreed, κ **0.74**, as section 10's.
- **Nine disagreements**, settled in `coders/issuer-settlements.csv`:
  - **S12** (six *taken back* lines: Binance USD, Gemini Dollar, Pax Dollar, PayPal USD, Tether Gold, ZUSD; i1 *no*, i2
    *cannot be read*): M0's line has two arms, the issuer's own fees **or** its claims. "No fees", or fees charged in
    dollars, exclude the fees arm at most; no file excludes the issuer accepting the coin for a claim, so the line
    **cannot be read** (S1's reading carried to this line, written here after the coders' rows were read).
  - First Digital USD *taken back*: **yes** (S3: the terms define FDUSD as an FDD and print that the issuer deducts FDD
    for its own conversion fees).
  - Frax *limit by rule*: **cannot be read** (S1, S9: one for one "at genesis" only, by design).
  - GYEN *limit by institution*: **yes** (S10: no frozen file prints the launch date; the whitepaper's standing terms
    name NYDFS regulation, as both coders read ZUSD's identical line; i2's after-change row rested on the manifest's
    launch month, which is not a print, and is not kept).
  - One after-change row, found by both coders: XSGD *taken back* **yes** from 2021-04-12 (a fee charged in XSGD).
- **S11's merge** found no line where the two layers read different codes; the issuer layer filled 29 first-layer
  *cannot be read* lines. Launch coin-lines, *cannot be read* / *yes* / *no*: **273 / 53 / 10** (the fixed readings
  alone, `variant-fixed-readings-only.csv`: 302 / 27 / 7). Coins with no line read: **58 of 84** (66 before). Eleven
  coins gained lines.
- **Late prints (S10)**: XSGD's four lines rest on versions captured from 2021-10, about a year after its launch read
  from its own post; the page says so.
- **Not in hand**: Reserve; Liquity's and mStable's whitepapers and PayPal's own terms (refused hosts). Liquity's four
  lines and PayPal USD's three read lines are read without them; mStable's three read lines come from its docs.

## 16. The issuer layer's small check answered (2026-10-02, after the check, before the rebuild; FRAMING F72)

The check (Sonnet, isolated: `bank/checks/FT-001-M7-frame-g-issuer-layer-2026-10-02-sonnet-small-check.md`, on
daf87773) found nothing blocking: κ, the nine settlements' accounts of the coders, S12, the merge and the counts
hold. Its four "should fix" items and its notes are answered here. Every answer is written after the build was seen.

- **S1, GYEN *limit by institution***: the check is right. S10 governs late prints, not whether a charter came
  before the launch. The whitepaper dates the NYDFS charter 2020-12-29, a 2020-11-01 page says approval was being
  sought, and no frozen file prints GYEN's launch date. So the order of launch and charter cannot be read, and the
  line is **cannot be read** (section 14: a line no frozen document prints stays *cannot be read*). ZUSD's line is in
  the same case, and both coders read it yes on the manifest's launch year, which is not a print. The 2020-11-01 page
  shows approval still being sought for both coins. So ZUSD's line is settled **cannot be read** by the same rule.
  (Corrected before the rebuild: this section's first version said ZUSD's launch was printed, and it is not.)
- **S2, who may redeem**: section 14 records who in the issuer's own words, but merge kept the readings' words where
  both layers read *redemption yes*. **S13** (code, `merge`): where both layers read a line alike, the who column is
  the issuer layer's words when it has them, the readings' words go into the note, and both layers' notes are kept.
  The MANIFEST then says how many *redemption yes* lines carry the issuer's own words.
- **S3, Frax *limit by rule***: the settlement now rests on M0's text, not on S1 and S9. M0's line is issue tied by
  code to reserves held one for one, or to a stated cap. The documents print one for one at genesis only, then a
  ratio the protocol moves by design, and they state no cap and no absence of one. So the line is **cannot be read**,
  as the first layer read it. Rule: S11 (settled by M0's text).
- **S4, the late-print flag**: **S13** (code, `issuer_layer`) carries "late print (S10)" into a line's note when
  either coder's note flags it. XSGD's launch rows get the flag.
- **Notes, kept as they are, with reasons**:
  - FDUSD *taken back yes*: the terms let the issuer deduct FDD from a holder for a conversion. Whoever's cost that
    covers, the issuer takes its own coin for a sum the holder owes it, which is M0's claims arm.
  - Kinesis's fees go to a fee pool that Kinesis holds and shares out. The issuer still charges the fee and takes it
    in its coin. Where the proceeds go afterwards does not change what is accepted.
  - S11 has no clause for a first-layer *yes* against an issuer-layer *cannot be read* (Frax's redemption). S13 says
    the reading stands.
  - XSGD's "will take effect" page: the after-change row reads the fee from its dated start. No earlier fee is
    printed, so the launch row stays *cannot be read*.
  - The coders' caveats live in `coders/i1` and `coders/i2` and move no code:
    - Liquity's first fourteen days: redemption opens on a schedule set at launch, which is a start date, not a
      standing term;
    - TrueUSD's clause that guarantees no redemption;
    - Tether Gold's whitepaper, which calls itself non-binding.
- **The MANIFEST's stale first-layer text** (step 4, uncertainty, assumptions) is redrawn with the rebuild.

## 17. G25b: the issuers' documents for the coins the map placed but nobody sought (2026-10-02, before any coder reads)

Step h's second check (B4) found that section 14 read the issuers' documents for 17 coins only. The G25 expert map
places 31 more coins with high or medium confidence, and their documents were never sought. Sami's policy request 12
(the engine, 22298e7a) opened their hosts, and the engine is freezing launch-time versions (Tether, Euro Tether and CNH
Tether in 14ed918b; the other 27 coming). This section revises section 14's scope openly (FRAMING F72). The told list is
unchanged. Only the four launch lines of these coins are read again, and the coins the map placed with low confidence
stay read from the fixed readings alone.

- **What is read, how and by whom**: as section 14, with no rule changed. S1, S3 and S7-S13 hold as written.
  - Two Sonnet coders work apart, in `coders/i3` and `coders/i4`. Each sees only `coders/issuer-packet-2/`: its README
    is section 14's packet README with M0's four lines and the rules, and it has one sheet per coin naming its frozen
    files and their version dates.
  - Neither coder sees the first layers, the settlements or the mapping.
  - A coin with no frozen launch document is listed as such and is not coded.
- **Meeting the layers**: S11 and S13, as written. The new layer meets the build after section 16 (8ace613e) line by
  line. `frame_g_mapping.py` reads the second issuer layer as it reads the first, with its own settlements file
  (`coders/issuer-settlements-2.csv`) and merge settlements (`coders/merge-settlements-2.csv`). The build after section
  16 stays in git and is told as a variant.
- **κ** is reported on the new layer's coin-lines, beside sections 10 and 15. Its disagreements are settled by M0's
  text, one row per line, rule named.
- **Checks**: a small check (Sonnet, isolated) of the new layer and the merge, before the mapping is redrawn into the
  study. Then a card on the new build (C12, parent C10), committed before its run.
- **Not in hand, said**: each host that stays refused, and each coin with no launch document found (Reserve: no
  capture past 2018 stubs, the engine).

## 18. G25b coded and merged (2026-10-02, after the two coders, before the small check)

- **κ on the second layer**: 120 coin-lines (30 coins × 4), 108 agreed, κ **0.84**.
- **Twelve disagreements**, settled in `coders/issuer-settlements-2.csv`:
  - **S12**, eight *taken back* lines (Basis, Basis Cash, Bean, Celo Euro, Neutrino USD, NuBits, Origin Dollar, agEUR):
    **cannot be read**. A sale of the protocol's own bonds or tokens for the coin, a loan or deposit of the coin to
    it, or a fee paid in another asset or not said to be paid in the coin, excludes the fees arm at most.
  - **S14** (written here after the coders' rows were read; FRAMING F72): for an issuer that is a company, *limit by
    institution* reads *no* only where a file prints the regime the issuer is under and that regime does not limit
    issue (Tether's FinCEN registration for anti-money-laundering duties, which both coders read), or says the issuer
    is unregulated. A bare statement of compliance, a law named without what it requires of issue, or oversight said
    of other entities, reads *cannot be read*. Under it:
    - DigixDao: oversight is said of its custodians, not of the issuer;
    - Euro Tether: only a compliance assertion and KYC/AML duties;
    - STASIS EURO: Malta's Virtual Financial Assets Act is named without what it requires.
    All three read **cannot be read**. Applied to the agreed lines (as S9 was), S14 also makes R's line **cannot be
    read**: its disclaimer names Tempus Labs Inc., a BVI company, as the issuer and prints no regime. It keeps Tether
    (a printed registration that does not limit issue), BiLira (an e-commerce company whose terms say crypto assets
    are not guaranteed by official bodies) and EOSDT ("not ... a regulated instrument") at *no*. A protocol or DAO that
    its files call decentralized, with no company named as issuer, reads *no*: 22 lines, which both coders read and S14
    leaves as they are.
  - STASIS EURO *redemption*: **cannot be read**, by M0's text. The FAQ names third parties and "direct emission"
    for large buyers, and no terms of 2017-18 are in hand.
- **After-change rows**: none kept.
  - IRON's end of Phase 1: the date is the coder's own sum, not a print, so S8 gives no row.
  - Synthetix's transfer fee set to 0 in February 2019: the line stays *yes* on the exchange fee and on debt repaid
    in the coin, so no code changes.
- **The merge (S11, S13)**: no line is read differently by this layer and the build after section 16. Launch
  coin-lines *cannot be read* / *yes* / *no* are **194 / 91 / 51** (after section 16: 275 / 51 / 10). Coins with no
  line read: **37 of 84** (58 after section 16, 66 on the fixed readings alone).
- **Late prints (S10)** are flagged on BitUSD, Neutrino USD, Synthetix USD and sEUR, beside XSGD.
- **Who may redeem, in M0's two classes.** M0 records who may redeem as "any holder, or verified customers only".
  C10's word rule leaves 9 of the 30 *redemption yes* lines unclassified ("users", "anyone") and puts Neutrino's
  "Waves account" (a wallet, not an account at the issuer) with the issuer's account holders. So, before the card on
  this build, two Sonnet readers apart each put every *redemption yes* line's own words (the who column and the line's
  note) in one of M0's classes: *any holder*, *verified customers only* (an account, a check or a membership with
  the issuer or its platform), or *not settled* (two sources disagree, S9). Their κ and settlements are written in
  `coders/who-classes.csv`, and the card reads that file. The word rule of C08-C10 stays in their runs.
- **Not in hand**, said:
  - Reserve, which has no capture.
  - On refused hosts: Ampleforth's white paper (drive.google.com), Alchemix's docs (alchemix-finance.gitbook.io),
    Celo Euro's launch post (blog.celo.org), Neutrino's white paper (wp.neutrino.at) and Havven's site
    (www.havven.io).
  - agEUR's white paper (a token URL, not fetched).

## 19. G25b's small check answered (2026-10-02, after the check, before the card's run; FRAMING F72)

The check (Sonnet, isolated: `bank/checks/FT-001-M7-frame-g-issuer-layer-2-2026-10-02-sonnet-small-check.md`, on
c97ed714) recomputed κ, every count and the build (0 differences). It found two blocking findings: six agreed *no*
lines read from absence. Every answer below is written after the build was seen.

- **B1**: S1 is carried to the agreed *limit by rule* lines of Ampleforth, Basis, Basis Cash and Bean, as S9 carried
  it in section 13. They now read **cannot be read**. Fei and NuBits print the exclusion in words, so they stand.
- **B2**: S12 is carried to the agreed *taken back* lines of Ampleforth and Djed. They now read **cannot be read**;
  Djed is Origin Dollar's case.
- **S1, R: the check is right.** Tempus Labs is the issuer *of the disclaimer* and the protocol's developer, not
  named as issuer of R. R reads *no* as a protocol, like Basis, Celo or Origin. Section 18's correction (0b3d6467)
  rested on a misreading, and its settlement row is removed.
- **S2, late prints**: the flag is the coders' own (S13 carries it). A flag on a line whose source predates launch
  (BitUSD *limit by rule*) over-flags. A line on the same litepaper without one (Synthetix USD's two limits)
  under-flags. The page names late prints as "flagged by the coders where a print may be late", never as a count of
  lines dated past twelve months.
- **S3, IRON's limit by rule**: kept *yes* at launch, with its note: three days at 100% collateral, then a ratio that
  floats, a change printed without a date (S8).
- **S4, Synthetix's 2019 rows**: kept, as the first layer kept its confirming rows (Dai, Tether, USD Coin). There are
  two after-change rows (Synthetix USD and sEUR *taken back*, February 2019, still *yes*).
- **S5, the Tether family**:
  - Tether's own files name a FinCEN registration for anti-money-laundering duties: a printed regime that does not
    limit issue, so *no* (S14).
  - Euro Tether's 2017 files name no registration, only a compliance assertion: *cannot be read* (S14).
  - CNH Tether's files do not name the coin: all four lines *cannot be read* (S3).
  One issuer, three readings, each from its own files.
- **Notes**:
  - DigixDao is the told list's name (the fixed readings name DigixDao); the documents read are DGX's, the gold token.
    Said on the coin's line, not changed: the list is the readings' list (section 2).
  - Eight *redemption yes* lines are redemption in another asset at the coin's value (collateral, reserve), not at
    par in the coin's unit. M0's line reads "a right to redeem at par on demand", and the coders read the value
    redeemed, not the asset. This is said beside the who classes.
  - The other notes (Fei's burned fee, Synthetix's work-in-progress proposal, Celo's fees to the network, and merge
    keeping a first-layer code) change no line.
- **The build**: 199 / 91 / 46, with 37 of 84 coins having no line read, and 8 after-change rows from the second
  round. Of the five refused documents, the check names Celo Euro's launch post as the likeliest to move lines (its
  three *cannot be read*). This goes to the engine.
