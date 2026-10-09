# ft001-a3 — reconstructed dataset

FT-001's A3 (part 1): the premium on gold read as the market's expectation of a return to gold, in two suspensions,
the Bank Restriction (1797–1821) and the greenbacks (1862–79). Paper's value in gold, P, is read as the discounted
chance of resumption at par:
- before each resumption law, with a constant hazard λ: P = λ/(λ + r);
- after it, with the legislated date T: P = q·e^(−r(T−t)).

**q is read only between 0 and 1.** Where q ≥ 1, or where λ implies resumption within a year for three years or more
in a row, the premium **cannot separate** an expected return to gold from the paper's own value as money (M0
section 7). This is **a model's reading, calibrated on nothing**: no test, no p-value, no verdict. It is checked on
the 1914 suspensions, which calibrate nothing.

The rules are A3's card, `bank/maps/FT-001/missions/FT-001-M4-A3-premiums.md`:
- sections 1–8, committed alone before any premium, gold price or yield was read (cb9028d);
- section 9, the readings settled with the transcriptions' coverage before any P was computed (d1a7f12);
- section 10, revised **after the first run had been seen** (b4834d1; FRAMING F72): the 1914 check's units, and the
  annual cross-check;
- section 11, revised **after the first build's small check** (c016271): the greenbacks' r from Homer and Sylla's
  Table 42 (A3-R2 withdrawn), the flat-r table, the cross-check narrowed, the parity check.

**This is the second build** (2026-10-02). The first (b58240e) went to a small check (Sonnet, isolated:
`bank/checks/FT-001-M4-A3-first-build-2026-10-02-sonnet-small-check.md`, not ready: A1, B1–B3, ten C's), answered in
section 11 and below. **What moved**: only the greenbacks' r, so only their λ and q. The first build read r from the
consols (about 3.2%) and found q ≥ 1 in 20 of the 48 months after the 1875 Act (three spans). This build reads the 6s'
own gold yield (3.5–4.7% after the Act, 4.7–12.3% before it), and finds q ≥ 1 in **36 of 48**. The first build's reading
is the variant `variant-r-consols.csv`.

M0 v4.2 applies; its pair hash is on every line (commit 3163162). The code is `missions/code/a3.py`, with 22 tests on
toy series in `test_a3.py`:
- d96f6ea, the model, committed before any value was read;
- b4834d1, section 10's revision;
- c78d4cc, par at the mint price;
- 68639b9, `nan` for an unread line;
- c016271 and ca4e8de, section 11 (the flat-r table, the consols variant, the narrowed cross-check, the label).

## Sources

- **The premiums**: printed tables in public-domain books. Their OCR text is frozen from archive.org
  (`data/archive-a3/`, 35626ca; the manifests are committed, the texts never are). The values were transcribed on the
  page images by an isolated reader (`transcriptions/`, with a page and a leaf for every value):
  - **the Restriction**: Tooke, *A History of Prices*, vol. 2 (1838), p. 379, the annual average price of gold per
    ounce "taken from official documents", 1800–1821 (the headline); and pp. 384–385, the price of standard gold in
    bars at two dates a year (the cross-check; some figures carry an unexplained "F");
  - **the greenbacks**: W. C. Mitchell, *Gold, Prices, and Wages under the Greenback Standard* (1908), Table 2, the
    monthly average price of $100 in gold in currency, 1862–78 (the headline). The cross-check is Mitchell, *A History
    of the Greenbacks* (1903), Table VI, 49 dates in 1862–63.
  - A second reader re-read 39 of the 389 premium values used (10%, seed 1797) on the images: **38 of 39 agree
    blind**; the 39th was the second reader's own misplacement of a line, corrected on the image
    (`transcriptions/second-reader.md`). Homer and Sylla's table was read twice by its reader, not by a second one.
- **Antipa (2016)** draws her agio only in figures. Her source, Castaing's *Course of the Exchange*, is not in hand
  (gap FT001-G16). Calomiris (1988) prints no monthly gold price. Neither is read off a chart.
- **r**:
  - the Restriction: the yield on 3% consols, Bank of England Millennium workbook, sheet M10 (Neal 1990, end of
    month), averaged over the year for an annual line;
  - the greenbacks: the yield in gold of the US 6s of 1861-81 (card section 4, option 2): Homer and Sylla (2005), Table
    42, the annual average price, 1861–1879, transcribed on its images by an isolated reader (`transcriptions/homer-sylla-
    table42-*`; the book was read in `acquisition/inbox/deposited/`, never committed). The table does not state its
    basis; the text beside it speaks of greenback prices (p. 306), so the price is read as currency (A3-R5), converted to
    gold at the year's average G (Mitchell 1908, Table 2's yearly row), and r is the yield to 1 July 1881 at a 6% coupon.
    Mitchell (1903), Table LXI, prints the same bond's January prices beside the currency value of $1,000 in gold and
    the bonds it would buy (1,025 / 0.896 = 1,144 in 1862), so they are currency prices. Read as gold instead, r would
    be 1.4–3.2% after the law and 17 of 48 months would read q ≥ 1 (the narrow re-check's computation).
    Two prices (1862 and 1872) are doubtful fractions against the table's own printed yields, flagged in the
    transcription; both are before the law, and r moves by about 0.1 point.
    A year's r comes from an annual average price. In the years G moved most this differs from a month's reading:
    Table LXI's January realized rates for 1862–65 are 6.9, 9.1, 8.8 and 11.7% (simple, in gold), against the build's
    7.3, 9.4, 12.3 and 9.8%. It moves only λ before the law, which stays below 1 in 1863–69 either way, and above 1 in
    1862 (1.6 at the build's r, about 2.8 at 6.9%). The consols (sheet M10, NBER, 1852–1888) are
    the variant `r-consols`;
  - the variant `short`: Bank Rate (sheet M9) for the Restriction. No US short rate is frozen.
- **The 1914 check**: JST R6, `xrusd` and `ltrate` (`stir` in the variant), 1915–1927.

## Steps

1. The card was committed alone. The code and its tests followed, then the transcriptions, the coverage, the readings
   of section 9, the selection (`transcriptions/selection.csv`) and the second reader's sample, all before the run.
2. **The runs, each after the one before had been seen** (F72):
   - the first (d96f6ea's code): the 1914 check "not consistent", France's and Germany's λ infinite. The cause was units
     (JST states France in new francs and Germany in 10¹² marks), restated by section 10 (b4834d1). Its check is kept
     (`check-1914-first-run.csv`);
   - the second and third changed only flags: 1800 and 1821 read "above par" from a float (c78d4cc), and unread lines
     carried an empty value (68639b9). No reading moved;
   - the fourth was the first build (b58240e), checked;
   - the fifth is this build, after section 11 (c016271, ca4e8de).
3. **This build** (`a3.py build --go --overwrite`, code ca4e8de) wrote:
   - `series.csv`: 261 lines, one per case and month, or per year where only a year is printed;
   - `spans.csv`, the "cannot separate" spans;
   - `check-1914.csv`;
   - `cross-source.csv`: the periods where the two sources differ by more than 2%;
   - `variant-cross-source.csv`: the other source, read alone, with its spans (`variant-cross-source-spans.csv`);
   - `variant-short.csv`, `variant-r-consols.csv`, and `r-sensitivity.csv` (the greenbacks read at a flat r of 3.2–6%).
4. **Checks**: `m0.py list_problems` and `ft.data.reconstructed.problems("ft001-a3")` find no problem.

## Assumptions

- **The parities** are fixed: £3 17s 10½d per ounce of standard gold, and $20.67 per fine ounce.
  - **The dates**: the 1819 Act passed on 2 July 1819, with T = 1 May 1823; the Bank resumed early, on 1 May 1821.
    The Resumption Act passed on 14 January 1875, with T = 1 January 1879.
- **An annual value reads its year as one line**, at 1 July, and is never spread over months. An annual line is after
  the law when its 1 July is (so 1819 is before the law).
- **r is the printed yield as a continuous rate** (Y1). A year's r is the mean of its months.
- **The run rule** is read on calendar years: three or more in a row, each with a mean λ ≥ 1, an "at par" year
  counting as λ = ∞ (Y4).
- **The parities checked** (card section 6): the UK's, 486.65 cents, is printed in the frozen Federal Reserve Bulletin
  (September 1931). Germany's Reichsmark par, 23.82 cents (4.1979 per dollar), is printed in the same table and equals
  the 1914 value used (the Reichsmark kept the mark's gold content). France's and Italy's later parities (3.92 and 5.26
  cents) differ from 1914's, so their statutory 1914 values are used, and JST's 1913 values sit at them.
- **In 1914, the dollar is read as gold**, though the US embargoed gold exports from September 1917 to June 1919.
  The pound was held near $4.76 from 1916 to 1919 by official support, so its P in those years is a pegged rate, not a
  market's odds (said, not corrected).

## Uncertainty

- **The Restriction's headline cannot read 1797–1799.** Tooke prints no annual price before 1800, so 34 months are
  *cannot be read*. Those are the door's years.
  - The cross-check (pp. 384–385) prints standard gold **at the mint price, or at 3 17s 6d to 3 17s 9d, at every
    date from August 1797 to August 1799**. That is the convertible band: the same table prints 3 17s 6d through 1822–28,
    when gold was convertible (in the OCR; the image was read to 1821). So the paper stood at par.
  - Read alone, on those five quotes, each at par, it places 1797–1799 in a "cannot separate" run
    (`variant-cross-source-spans.csv`): the premium cannot say whether holders expected a return to gold or held the
    paper as money.
- **The headline's "cannot separate" span 1803–1809 rests on a flat £4 0s 0d**: every year but 1804 prints exactly
  £4, which is P = 0.973 and λ ≈ 1.6–1.9 a year.
  - Antipa (2016, p. 1069) writes that in 1805–1808 her agio's stability "simply reflects the lack of observations".
    The cross-check prints £4 in 1804–05 and no price at all in 1806–08.
  - So the span is "cannot separate" by the rule, **and its data are thin**: both are said.
- **The headline's other readings**:
  - 1800, its first year, reads par (Tooke's annual average is the mint price), while the cross-check prints £4 5s in
    August 1800, an "F" figure, 9% higher: the two disagree, and the part says the first year's level is in doubt;
  - 1801–1802 and 1810–1816 read λ between 0.13 and 0.55 a year;
  - 1817–1818 read 1.4–1.5, and 1819 reads 0.92: three years that miss a run by 8% in 1819. 1819 is read before the
    law because its line sits at 1 July and the Act passed on 2 July; read after it, its q would be 1.13;
  - 1820–1821, after the law, read q ≥ 1, a span. 1821's line sits at 1 July, after the 1 May resumption: its q ≥ 1 is
    the resumption itself.
- **The greenbacks** (204 of 205 months read; January 1879 has no line in Table 2), on the 6s' gold yield:
  - before the law, the year's mean λ is 1.60 in 1862 (P near par in its first months), 0.14–0.23 in 1863–69, and
    0.41–0.48 in 1870–74. No run of three years reaches 1;
  - after the law, **q ≥ 1 in 36 of 48 months**: all of 1875, December 1876 – April 1877, and June 1877 – December 1878.
    q ranges from 0.975 to 1.072, so the after-law months sit at the edge of the rule;
  - the low is P = 0.387, in July 1864.
- **The greenbacks' reading depends on r** (`r-sensitivity.csv`, the small check's A1). At a flat r of 3.2%, 20 of the 48
  after-law months read q ≥ 1; at 4%, 30; at 4.5%, 42; at 5% and 6%, all 48. On the consols (the first build), 20. So
  "the premium cannot separate after 1875" holds in 36 of 48 months at the 6s' own yield and in all 48 at 5% and above,
  and for fewer months at a lower rate. No sentence may read q below 1 there as holders doubting resumption.
- **The two sources against each other**: 8 of the 27 periods compared differ by more than 2% (`cross-source.csv`), all
  for the Restriction: 8 of 15 years, among them 1800 and 1809. For the greenbacks, none of the 12 months compared.
  Tooke's February 1811 figure reads 4 13s 6d on the image and 4 18s 6d in the OCR; it was not in the second reader's
  sample, and either way 1811 differs by more than 2%.
- **The 1914 check is consistent, narrowly.** The mean λ over 1915–1920 is:
  - the UK (back at par in 1925) 1.42;
  - France (devalued) 0.36;
  - Italy (devalued) 0.143;
  - Germany (replaced) 0.140.

  So the order holds, but Italy and Germany are 0.003 apart. The UK's figure rests on the pegged pound of 1916–18.
  Germany's 1922 is *cannot be read* (no `ltrate`). Austria cannot be read: it is not in JST. On the short rate the check cannot be read: France's and Italy's `stir`
  miss years of 1915–1920.
- **What this shows, and what it cannot.**
  - It shows, month by month (by year for the Restriction), what a constant-hazard or legislated-date reading of
    the premium implies. It also shows where the premium is too small for the reading to separate an expected return
    from the paper's own value.
  - It cannot say that holders expected redemption. The model assumes the premium is only the discounted odds of
    resumption, with r the right rate. For the greenbacks, r is the 6s' gold yield, read from an annual price whose
    basis the table does not state, and the after-law reading moves with r.
  - The door's own years, 1797–1799, are read only by the cross-check. There they cannot separate.
