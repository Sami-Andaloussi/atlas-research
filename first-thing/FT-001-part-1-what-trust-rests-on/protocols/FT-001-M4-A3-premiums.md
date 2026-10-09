# FT-001 — M4: A3, the premiums read as expectations (card)

> Analysis A3 of `bank/dossiers/FT-001-the-life-of-a-money.md` (part 1, "what trust rests on"), the premiums half of
> mission M4 (frame a's protocol, `FT-001-M4-frame-a.md`, says A3 is not in it). The E2 session wrote this card on
> 2026-10-02, **before any gold premium, gold price or bond yield of the two cases or of the 1914 check was read**.
> It is committed alone first; the transcriptions, the code and its tests follow, and the build comes last
> (BLUEPRINT section 5 c: the card's commit precedes its results).
>
> **The rules are M0's**, version 4.2 (`FT-001-M0-rules.md`, section 7, A3; commit 3163162): the parities fixed
> before reading; P = λ/(λ + r) before each resumption law, P = q·e^(−r(T−t)) after it; r the long government yield,
> the short rate a variant; **q read only between 0 and 1**; "cannot separate" where q ≥ 1 or where λ implies
> resumption within a year for three years or more in a row; checked on the 1914 suspensions, with no calibration
> from them. This card adds no rule. Where M0 leaves a reading open, it chooses in the open, marked *reading*.
>
> **What was seen before writing** (structure only, no value):
> - Antipa (2016, *JEH*; in `acquisition/inbox/deposited/`, read only, never committed): her agio is drawn in figures
>   1 and 5–6 and summarised in Table 1, **never printed as numbers**; her source is Castaing's and Wettenhall's
>   *Course of the Exchange*, not in hand.
> - Calomiris (1988, *OEP*; deposited, read only): its tables are annual depreciation rates, a model's estimates,
>   bond-yield differentials and an 1862–63 note table from Mitchell (1903); no monthly gold price.
> - On archive.org (the Guard allows it, 2026-10-02): W. C. Mitchell, *Gold, Prices, and Wages under the Greenback
>   Standard* (1908); Mitchell, *A History of the Greenbacks* (1903); Tooke, *A History of Prices* (1838), volumes
>   1–6; the Bullion Committee's *Report, together with minutes of evidence, and accounts* (1810); Silberling,
>   "British Financial Experience 1790–1830" (1919, JSTOR's early content). Titles only were read.
> - The Bank of England's Millennium workbook (frozen 2026-09-30): sheet M10, monthly 3% consol yields 1753–1823
>   (Neal 1990, end of month) and 1852–1888 (NBER); sheet M9, Bank Rate monthly; sheet M15, the dollar–sterling rate
>   monthly from 1791. Headers only.
> - Homer and Sylla (2005, deposited, read only): Table 42 (US long-term high-grade bonds, 1860–1879) has no text
>   layer; its title only.
> - JST R6 (frozen): `xrusd`, `ltrate` and `stir` are present for GBR, FRA, ITA, DEU in 1913–28 (counts only); Austria
>   is not in JST.
> - MeasuringWorth is refused by the Guard (2026-10-02) and is not opened.

## 1. The cases and their dates (fixed now)

| Case | Suspension | Resumption law (passed) | Legislated date T | Actual resumption |
|---|---|---|---|---|
| The Bank Restriction | 27 February 1797 (Order in Council, 26 February) | the 1819 Act ("Peel's Act"), 2 July 1819 | 1 May 1823 | 1 May 1821 (early: said) |
| The greenbacks | 30 December 1861 (the banks' suspension; the first legal-tender notes, 25 February 1862) | the Resumption Act, 14 January 1875 | 1 January 1879 | 1 January 1879 |

- *Reading*: the span read runs from the suspension's month to the resumption's, both included. Months before the
  law's passage are "before the law"; the month of passage and after are "after the law".
- The greenbacks' span starts in January 1862, the first month a gold price in currency is quoted after the
  suspension; the notes' own legal-tender date is told.

## 2. The parities (fixed now, before reading)

- **The Restriction**: the mint price, **£3 17s 10½d per ounce of standard gold** (£3.89375). The paper pound's value
  in gold is P = 3.89375 / (the market price of standard gold in bars, in paper £ per ounce).
- **The greenbacks**: **$20.67 per fine ounce**, so a gold dollar is the parity. The quotation is the price of $100
  in gold in currency, G; P = 100 / G.
- P = 1 is par. A market price below the mint price (P > 1) is read as printed and flagged `above par`.

## 3. The premiums: which series, from which source (fixed now)

- **The Restriction**: the market price of **standard gold in bars**, London, in paper pounds per ounce.
  - Source order, chosen by coverage before any value is used: among Tooke (1838), Silberling (1919) and the Bullion
    Report's accounts (1810), the series that covers **the most months of March 1797 – May 1821** is the headline;
    the others are cross-checks where they overlap. A month where two sources differ by more than 2% is listed.
  - *Reading*: where a source prints only "Portugal gold in coin", it is used as printed and flagged `coin`.
  - *Reading*: where a source states that gold stood at the mint price, P = 1 for those months, flagged `stated`.
- **The greenbacks**: Mitchell (1908)'s gold price in currency.
  - *Reading*: the month's value is the monthly mean the table prints; if it prints only daily highs and lows, the
    mean of the month's highest and lowest.
  - Mitchell (1903) is the cross-check for 1862–63, where it overlaps.
- **Frequency**: monthly where a source prints at least one quotation in the month (the month's mean of
  quotations). Otherwise the source's own frequency, flagged. Nothing is interpolated or carried.
- **The transcription** is done by a reader that is not this session, on the page images, with a page locator per
  value. A second reader re-reads a sample of at least 10% of the values, drawn by a fixed seed, before the build.
  A disagreement is settled on the image, and listed.

## 4. The yield r (fixed now)

- **The Restriction**: the yield on 3% consols, Millennium sheet M10 (Neal 1990, end of month), as an annual
  decimal. Variant `short`: Bank Rate (sheet M9).
- **The greenbacks**: the yield of the US 6% bonds **in gold**, from the first of:
  1. a gold-basis yield of the 6s of 1881 printed in a source in hand or on an allowed host (Homer and Sylla's Table
     42, read on its image; Mitchell 1908);
  2. else the yield to 1881 at a 6% coupon of the 6s of 1881's **currency** price, converted to gold at the same
     month's G (price in gold = price × 100 / G), from the same sources;
  3. else the consol yield of sheet M10 (NBER, 1852–1888), labelled *a gold world's long yield, not the United
     States'*, a declared substitute.
  - Variant `short`: the New York commercial paper rate, if a frozen source holds it; else *cannot be read*.
- The yield is that of the same month as P where monthly; else of P's year.

## 5. The model, and what it says

- **Before the law**: a constant hazard λ (per year): P = λ/(λ + r), so **λ = r·P/(1 − P)**. The expected wait to
  resumption is 1/λ.
  - P ≥ 1 gives no finite λ: the month reads `at par`, counted as λ ≥ 1 below.
- **After the law**: the legislated date T. P = q·e^(−r(T−t)), so **q = P·e^(r(T−t))**, with T − t in years
  (days / 365.25, t the 15th of the month).
- **"Cannot separate"** (M0), for a span:
  - after the law: every month with q ≥ 1;
  - before the law: every calendar year of a run of **three or more consecutive calendar years** in which the
    year's mean λ (the mean of its months' λ, `at par` months as λ = ∞) is **≥ 1**, that is, resumption expected
    within a year. *Reading*: the run is read on calendar years, the span on their months.
  - There, A3 says the premium cannot separate an expected return to gold from the paper's own value as money, and
    the part's outcome "redemption was expected" **cannot be read**.
- **Elsewhere**, A3 reports λ (and 1/λ in years) or q, month by month, with r and its source. This is a model's
  reading, labelled *a model, calibrated on nothing*; no test, no p-value, no verdict.

## 6. The 1914 check (fixed now; no calibration)

The same model, before-law form only (no case had a legislated date before its outcome), annually, from the
suspension's year to the year before the outcome:

| Case | Outcome | Years read | Gold parity (per US dollar unless said) |
|---|---|---|---|
| United Kingdom | back at par, 1925 | 1915–1924 | $4.8665 per £ |
| France | devalued, 1928 | 1915–1927 | FRF 5.1826 |
| Italy | devalued, 1927 | 1915–1926 | ITL 5.1826 |
| Germany | replaced, 1923–24 | 1915–1922 | DEM 4.1979 |
| Austria | renamed (the schilling, 1925; M1 row 9) | — | *cannot be read*: not in JST, told |

- P = (the parity in local currency per dollar) / JST `xrusd` (local currency per dollar, the year's value as JST
  gives it). For the UK the parity is 1 / 4.8665 = £0.205487 per dollar. *Reading*: the dollar is read as gold,
  though the US embargoed gold exports from September 1917 to June 1919: said.
- r: JST `ltrate`; variant `short`: `stir`.
- The parities are checked against a frozen printing (the Federal Reserve Bulletin's par of exchange, FRASER) before
  the build; if none prints them, the session says so and uses the values above, which are the statutory ones.
- **What the check reads**: each case's mean λ over 1915–1920, the years common to all four before hyperinflation.
  The model's reading is **consistent** if the order is: the case back at par above both devalued cases, and both
  above the replaced case. The order is reported as found. If it fails, A3 says so beside its result, and the part
  says the model's reading is not supported by its check. The cases calibrate nothing: no parameter is set from them.

## 7. What is written

- `data/reconstructed/ft001-a3/`:
  - `series.csv`, one line per case and month (or year), in M0's case-line format: P, r and its source, the phase
    (before / after the law), λ or q, the reading (`model` / `cannot separate` / `cannot be read`) and the flags;
  - `spans.csv`, the "cannot separate" spans per case, with their rule;
  - `check-1914.csv`, the check's lines and its order;
  - variants `short` and `cross-source` (the other premium source where it overlaps);
  - `MANIFEST.md`.
- Code: `missions/code/a3.py`, with tests on toy series in `test_a3.py`, committed before the build.
- The transcriptions: `data/reconstructed/ft001-a3/transcriptions/`, one CSV per source with page locators (numbers
  and locators only, no text of the books).

## 8. Checks

- A small check (Sonnet, isolated) of the transcription sample and of `series.csv` against the rules above.
- Part 1 is published: before it, a deep check (Opus, isolated) of A3's build with the part's others (BLUEPRINT
  section 8).

## 9. Readings settled with the transcriptions' coverage (2026-10-02, before any P, λ or q is computed)

The transcription reader (Sonnet, isolated) read every value on the page images and wrote its coverage report
(`data/reconstructed/ft001-a3/transcriptions/coverage.md`). The session read the coverage, the series names and the
units. It computed nothing from the values. What the coverage showed, and what this section settles:

- **No monthly London gold price exists for 1797–1821 in the frozen sources.** The candidates, counted in months of
  March 1797 – May 1821:
  - Tooke, vol. 2, p. 379: annual averages of the price of gold per ounce, 1800–1821, one per year. That is 22 years,
    or 257 months read by year.
  - Tooke, vol. 2, pp. 384–385: the price of standard gold in bars, at two dates a year, of which 28 carry a price.
  - Tooke, vol. 1, pp. 242 and 249: seven in-text values, for 1799–1802.
  - The Bullion Report's accounts price gold at Hamburg, not in London. Silberling's Table 6 is silver.

  **Reading A3-R1**: an annual value covers its year's months, so **the headline is Tooke's p. 379**. Its years read
  as single lines, flagged `annual` (`a3.py`, Y3). The cross-check is pp. 384–385, the only other source that prices
  standard gold in bars. 1797–1799 has no annual value, so **the headline cannot read the Restriction's first three
  years**; the cross-source variant reads them where p. 384 prints a price. This is said with the result.
  - The letter "F" printed after some figures on pp. 384–385 is unexplained on the page. Those values are read as
    printed, and the transcription keeps the letter in `value_as_printed`.
- **The greenbacks**: Mitchell (1908) Table 2 prints a monthly average, January 1862 – December 1878 (204 of 205
  months). **The headline is its "gold price in greenbacks, average"**, the card's first choice. The cross-check for
  1862–63 is Mitchell (1903) Table VI, "price of gold in currency", in the same unit (49 dates; the card's section 3).
  Mitchell (1903) Appendix A and Table 18 of Mitchell (1908) are transcribed but not used. They price the greenback in
  gold, or by quarter.
- **r for the greenbacks** (card section 4). Options 1 and 2 are thin:
  - Mitchell (1903) Table LXI prints a realized gold-basis rate on the 6s of 1881 for four Januaries (1862–65);
  - Table VII prints the 5-20s' currency prices for 1864–65, which are not the 6s of 1881.

  **Reading A3-R2**: an option counts when it gives a yield for at least half the case's months. Options 1 and 2 give 4
  and 24 of 205, so **the headline takes option 3**, the consol yield (Millennium M10, 1852–1888), labelled *a gold
  world's long yield, not the United States'*. Table LXI's four realized rates are printed beside, for comparison
  only.
- `transcriptions/selection.csv` writes these choices, in the columns `a3.py` reads.

## 10. Revised after the first run had been seen (2026-10-02; FRAMING F72, BLUEPRINT §11.15)

The first build (`a3.py`, d96f6ea, with section 9's selection) ran once. Its 1914 check read "not consistent", with
France's and Germany's λ infinite. The cause is units, not the model. JST R6 states France in new francs (1 = 100 old
francs) and Germany in units of 10¹² marks (the 1923–24 reform). Against the statutory parities, JST's 1913 values
(the last gold-standard year) are off by factors of 99.97 and 9.97 × 10¹¹; for the UK and Italy the factor is 1.00
and 0.98.
- **A3-R3 (Y5 in `a3.py`)**: the parity is restated in JST's unit by the reform's own ratio, 100 for France and 10¹²
  for Germany. These ratios are not fitted. This revision was made **after the first check's result had been seen**,
  and that result is kept beside the new one (`check-1914-first-run.csv`), as F72 requires.
- **A3-R4 (Y6)**: the first run compared the Restriction's annual headline with nothing, since the cross-check's
  periods are months. Where the headline reads a year alone, the cross-check is now read as the mean of its quotations
  in that year, and the count of periods compared is printed.
- Nothing else changes. The card's rules, the selection and the transcriptions stand.

## 11. Revised after the build's small check (2026-10-02; FRAMING F72)

The small check (Sonnet, isolated: `bank/checks/FT-001-M4-A3-first-build-2026-10-02-sonnet-small-check.md`) recomputed
every line and found no arithmetic error. Its verdict was **not ready**, for one A and three B's. It judged section 10's
units revision legitimate.
- **B1 and A1, the greenbacks' r.** Section 4 names Homer and Sylla's Table 42 first, read on its image, and section 9
  passed over it with a threshold ("at least half the months") the card does not contain. The greenbacks' after-law
  reading flips with r: at a flat 3.2% (the consols), 20 of 48 months read q ≥ 1, and at 5% all 48 do. So:
  - **A3-R2 is withdrawn.** Table 42 was transcribed on its images by an isolated reader
    (`transcriptions/homer-sylla-table42-*`). It prints the 6s of 1861-81's annual average price, 1861–1879. It does not
    state the basis; the text beside it speaks of greenback prices (p. 306).
  - **A3-R5**: the price is read as in currency. Section 4's option 2 applies: the price is converted to gold at the
    year's average G (Mitchell 1908, Table 2's yearly row), and the yield to 1 July 1881 at a 6% coupon is r for every
    month of that year (Y2; "else of P's year").
  - The first build's consol reading is kept as `variant-r-consols.csv`. The case is also read at a flat r of 3.2–6%
    (`r-sensitivity.csv`, Y7), so that the reading's dependence on r is printed beside it.
- **B2**: the cross-check compares only the periods the headline reads (Y6 narrowed). The greenbacks' yearly rows of
  Table 2 are no longer set against part-year means.
- **B3**: the UK's parity is printed in the frozen Federal Reserve Bulletin (September 1931, foreign exchange: 486.65
  cents). France's, Italy's and Germany's 1914 parities are not printed in the frozen FRASER texts, whose 1931 tables
  give their later parities. The statutory values are used, and JST's 1913 values sit at them (Italy 0.985).
- The C items are answered in the manifest.
- This revision was made **after the first build's results had been seen**. The first build's figures stay beside the
  new ones in the manifest.

## 12. After the second build's narrow re-check (2026-10-02)

The re-check (`bank/checks/FT-001-M4-A3-second-build-2026-10-02-sonnet-narrow-recheck.md`, Sonnet, isolated) reads
**ready after C**: no A, no B; every earlier finding answered, B3 partly. Its six Cs are wording, and none moves a
number. They are answered in the manifest. One corrects this card: section 11 says Germany's 1914 parity is not
printed in the frozen FRASER texts. It is: the September 1931 Bulletin prints the Reichsmark's par, 23.82 cents
(4.1979 per dollar), the value section 2 fixed. Only France's and Italy's later parities differ from 1914's. Section 11
stays as written; this section corrects it. No rule, parity or reading changes, and nothing is rebuilt.
