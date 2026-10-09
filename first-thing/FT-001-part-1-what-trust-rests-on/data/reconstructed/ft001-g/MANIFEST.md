# ft001-g — reconstructed dataset

FT-001's frame g, **told**: the coins named in sourced reading (M0 section 2, "named in sourced reading"), and each
coin's supports at launch, mapped onto M0's four private-issuer lines by two coders working apart. It serves claim 4
in part 1 ("the new containers"): **no verdict, n given** (the dossier, claim 4). Frame g follows no other list, and it
is never pooled into claim 5's odds or into test (ii).

The rules are the protocol `bank/maps/FT-001/missions/FT-001-M7-frame-g.md`:
- sections 1–5, committed alone with the source scout's report, before any coin was listed (61374d7);
- section 6, the told list's code (aa2ccc3), and section 8, the person's check (008240a);
- sections 9 and 10, the coders' packet (825e7d2, 7267d0a), the two coders, κ and the settlements (e30de86).

M0 v4.2 applies (commit 3163162).

**This manifest covers the told list and the mapping, which part 1 reads.** The phases (A9, M7 sections 4, 7, 11
and 12) are part 3's. Their stated rows and code are committed (`coders/phases-stated.csv`, `frame_g_phases.py`), but
`phases.csv` is not built. Whether to build or replace it is part 3's first decision (`plan/e2-ft001.md`).

**After G25 (M7 sections 14 to 16, 2026-10-02).** The issuers' own documents were opened by Sami's policy request 11
and frozen by the engine for 17 coins (83af35af). Two more coders coded them apart (`coders/i1`, `coders/i2`), with
κ 0.74 on 68 coin-lines. Their nine disagreements were settled in `coders/issuer-settlements.csv` (rules S1, S3, S7,
S11 and S12). The layer was merged with the fixed readings by S11 and S13 (`frame_g_mapping.py`, b5772ad and 0b9fe03);
no line is read differently by the two layers.

Section 16 answers the layer's small check
(`bank/checks/FT-001-M7-frame-g-issuer-layer-2026-10-02-sonnet-small-check.md`, nothing blocking). GYEN's and ZUSD's
*limit by institution* become *cannot be read*: no file prints either coin's launch date against the charter of
2020-12-29. Frax's *limit by rule* is settled by M0's text. Who may redeem takes the issuer's own words, and XSGD's
late prints are flagged.

`mapping.csv` and `series.csv` are the merged build. The fixed readings alone are `variant-fixed-readings-only.csv`
and `variant-series-fixed-readings-only.csv` (identical to the build at 97f10368). Steps 1 to 3 describe how that
first layer was built.

**After G25b (M7 sections 17 to 19, 2026-10-02).** Step h's second check (B4) found that the issuers' documents had
been read for 17 coins only. The engine froze launch-time copies for 30 more coins the expert map placed (policy
request 12; ed19676c, 8d323293, 14ed918b; Reserve has no capture). Two more coders read them apart (`coders/i3`,
`coders/i4`), with κ 0.84 on 120 coin-lines. The thirteen disagreements, and six agreed lines read from absence that
the round's small check found, are settled in `coders/issuer-settlements-2.csv` (S1, S7, S11, S12 and S14; S14 written
after the rows were read). The round met the build after section 16 by S11 and S13, with no conflicting line; that
build is kept as `variant-after-section-16.csv`. Who may redeem, on every *redemption yes* line, was put in M0's two
classes by two readers apart, who agreed on 30 of 30 (`coders/who-classes.csv`).

**The build today:**
- launch coin-lines, *cannot be read* / *yes* / *no*: **199 / 91 / 46**. By line:
  - redemption 41 / 30 / 13;
  - a limit by rule 44 / 38 / 2;
  - a limit by institution 46 / 7 / 31;
  - taken back 68 / 16 / 0.
- **37 of 84 coins have no line read** (58 after the first round, 66 on the fixed readings alone). 35 of them are
  coins for which no place of their launch terms was known when the study looked; the two others are CNH Tether, which its files do not name, and Reserve.
- Who may redeem, on the 30 *redemption yes* lines: any holder 13, verified customers only 16, and Tether not
  settled.
- Late prints are flagged by the coders on XSGD, BitUSD, Neutrino USD, Synthetix USD and sEUR.

Not in hand:
- Reserve: no capture.
- Documents on refused hosts:
  - PayPal's own terms (www.paypal.com);
  - mStable's white paper (github.com) and Liquity's (docsend.com);
  - Ampleforth's white paper (drive.google.com);
  - Alchemix's docs (alchemix-finance.gitbook.io);
  - Celo Euro's launch post (blog.celo.org);
  - Neutrino's white paper (wp.neutrino.at);
  - Havven's site (www.havven.io).
- agEUR's white paper, behind a token URL.

The first round's own figures (273 / 53 / 10, then 275 / 51 / 10 after section 16) are in git (daf87773, 8ace613e).

## Sources

- **The fixed readings** (M7 section 2), frozen before the list was drawn. The manifests are committed; the texts
  never are:
  - BIS Papers 141 (Kosse, Glowka, Mattei and Rice 2023), Annex 1;
  - BIS working papers 1146, 1164, 1219 and 1270;
  - the Federal Reserve's IFDP 1334 and three FEDS Notes;
  - the New York Fed's Staff Report 1073;
  - NBER w27136, w30256, w30796 and w31160;
  - Mizrach, arXiv 2201.01392, the census of dead coins.
- **Readings that cannot be had**, said and not replaced (M7 section 2):
  - Anadu et al. and the FSB's reports, on denied hosts;
  - Gorton and Zhang, on SSRN, also denied (gap FT001-G10).
- **The issuers' own documents**: at the first build every issuer host was denied by the Guard, and none was opened
  (M7 section 3; gap **FT001-G25**). After Sami's policy request 11, the engine froze launch-time versions for 17 coins
  through web.archive.org and the NYDFS (`data/frame-g/issuer-<slug>/2026-10-02/`, manifests committed in 83af35af; the
  texts never are). M7 section 14 reads them. After policy request 12, the engine froze 30 more coins' documents
  (ed19676c, 8d323293, 14ed918b); M7 section 17 reads them.

## Steps

1. **The told list.** `frame_g_list.py` drew 95 draft names from the frozen texts. A person's check (a Sonnet
   reader, read by the session, rechecked by a second isolated reader, which agreed on 102 of 103 rows) read 104
   rows (the 95, and 9 names added at the check), merged 4 into other coins, and left:
   - **85 coins** (`coins.csv`), 9 of them commodity-pegged and one never issued (Libra/Diem);
   - **15 names off the list** (`coins-off.csv`): 14 that are not a coin, and Terra;
   - Terra and UST are cited, not mapped (M0).
2. **The coders' packet** (`coders/packet/`, 84 sheets): one per coin to map (the 85 less Libra/Diem). Each sheet
   gives the coin and the frozen readings' pages that name it, and nothing else.
3. **Two coders** (Sonnet, apart: `coders/g1`, `coders/g2`) coded each coin's four lines at launch: *yes*, *no* or
   *cannot be read*, with a source and a locator.
   - **κ = 0.743** on 336 launch coin-lines; they agreed on 317.
   - The 19 disagreements were settled by M0's text, never by the coin's fate (`coders/settlements.csv`, rules
     S1–S5; S6 records who may redeem on three agreed lines).
   - **After frame g's small check** (`bank/checks/FT-001-M7-frame-g-mapping-2026-10-02-sonnet-small-check.md`, not
     ready: A1, B1), the session added rule **S9** (M7 section 13), applying the settled readings to every line they
     govern, agreed or not:
     - who may redeem is recorded for all nine launch *redemption yes* lines (A1); Tether's two prints are kept, not
       settled;
     - S1 is applied to three *no* codes that print fractional backing but nothing on a cap: IRON's and Frax's limit by
       rule at launch, and Frax's Version 2. All three become *cannot be read* (B1);
     - S2's reading is applied to Magic Internet Money's *taken back* (*yes*), whose cauldron prints Dai's mechanism.
     These revise agreed lines after a check, in the open (FRAMING F72). The first mapping is in git (e4ee50f).
   - The printed changes after launch are rows of their own (S7, S8).
4. **`frame_g_mapping.py`** (13 tests; f1ac65b) draws two files from the coders and the settlements, adding nothing:
   - `mapping.csv`: 343 rows, the 336 launch coin-lines and 7 after-change rows;
   - `series.csv`: one line per coin, with its four launch codes and the number of lines **read** (*yes* or *no*) as
     the value.

   It refuses a disagreement without a settlement. Re-run after S9, it rewrote `mapping.csv` and `series.csv`.
   After G25 (sections 14 to 16; 17 tests), it also draws the issuer layer (`issuer_layer`) and merges it (`merge`, S11
   and S13). Today `mapping.csv` has 344 rows: the 336 launch coin-lines and 8 after-change rows. The first layer's
   files are kept as the two variants.
5. **Checks**: `ft.data.reconstructed.problems("ft001-g")` finds no problem. A small check (Sonnet, isolated) of
   the list and the mapping follows (M7 section 5, step 6).

## Assumptions

- **"Named in sourced reading"** is a fixed set of readings, frozen before the list. It is not a search, so a coin
  named only elsewhere is not on the list. *What no code holds*: that no coin was kept or dropped for its known fate.
  Every decision cites its page, and the recheck read them all.
- **The coders are outcome-aware** (M7 section 3), since the coins' histories are known, and so is the session that
  settled them.
  - **The barrier**: each settlement quotes M0's line and a printed page, and an isolated check reads them.
- **A line is read at the coin's launch.** A later print of the terms is not a change (M7 section 10). A printed
  change touches only the lines it names (S7), and an undated change dates nothing (S8).
- **A bare category label does not read a line** (S1, S3). A statement that names the coin and prints the mechanism
  does; for Liquity USD that statement is a category sentence that names the coin (FEDS-2022). A *no* needs both arms
  of "a limit by rule" excluded (S1), on every line (S9). g2's reading of S1's 14 lines (*no*) is a variant, `g2-no`.
  It is told, not written as a file.
- **"At launch" is read from later prints** where no launch document is in hand: several *yes* lines rest on
  statements of 2020–2023 read as the standing terms (USD Coin's *limit by institution* on its licences as of 2022, for
  one). The date of each print is in its locator.
- **Who may redeem** is recorded as the page prints it, and in the issuer's own words where the issuer layer reads it
  (S13). NYFed-SR1073 p.8 prints "a restricted set of participants". The issuers of the same four coins print
  verified customers, and both are kept.
- **A yield is not a support** (the dossier, claim 4). It is decided from monies before 1900, before any coin is
  read.

## Uncertainty

- *This section describes the fixed readings alone (the variant). The merged build's counts are at the top.*
- **Most lines cannot be read.** Of the 336 launch coin-lines, **302 are *cannot be read***; 27 read *yes* and 7 read
  *no*. By line, the three counts are *cannot be read* / *yes* / *no*:
  - redemption: 74 / 9 / 1;
  - a limit by rule: 73 / 11 / 0;
  - a limit by institution: 73 / 5 / 6;
  - taken back: 82 / 2 / 0 (Dai and Magic Internet Money, both by S2's reading of a borrower's repayment).

  Who may redeem, for the nine *redemption yes* lines:
  - a restricted set of participants for 4 (Binance USD, Gemini Dollar, Pax Dollar, TrueUSD);
  - any user or any holder, by smart contract or on demand, for 3 (Frax, Liquity USD, USDD);
  - USD Coin's direct customers, in two prints of 2022 and 2023;
  - Tether's two prints, not settled: any investor in its 2014 white paper, and verified customers with a USD 100,000
    minimum in 2023.
- **Per coin**:
  - 66 of the 84 mapped coins have no line read;
  - 10 have one, 1 has two, 6 have three, and 1 has all four.

  So claim 4's figure can describe only the few coins whose terms the frozen readings print. The rest are
  *cannot be read*, said coin by coin, never filled.
- **Why**: the frozen readings give most coins only a category label (BIS Papers 141's Annex 1), and every issuer
  host was denied until G25. The gap is worked as FT001-G25 (`bank/maps/FT-001/gaps.csv`): looked in hand, an expert map of
  where each coin's launch terms are printed, then the documents asked of Sami's hand through the engine.
- **After launch** (7 rows), one changes a code: Dai's peg stability module (redemption *no* becomes *yes*; undated, so
  it dates nothing). Frax's Version 2 and its 2023 vote read *cannot be read* after a *cannot be read* launch (S9). Tether's
  2019 restatement ("100 percent backed by reserves" that may include loans to affiliates) loosens the one-for-one
  wording and is still read *yes* by both coders; it and USD Coin's two restatements confirm a launch code.
- **What this shows, and what it cannot.** It shows which of the private issuer's supports the sources in hand print
  for each coin at launch, and how often two coders apart agree on them (κ 0.74, where most agreement is on *cannot
  be read*). It cannot say what share of stablecoins rest on each support, since the sources print the terms for
  only a few coins, and the list is what sourced reading names, not a census.
