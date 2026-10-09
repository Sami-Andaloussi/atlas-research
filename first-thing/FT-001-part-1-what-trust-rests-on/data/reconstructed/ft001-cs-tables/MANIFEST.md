# ft001-cs-tables — reconstructed dataset

Two published chronologies transcribed for FT-001 part 1's case studies: Bordo & Schwartz's Table 1A (and Table 1B's
Bretton Woods dates) for CS-B (card C19), and Bernanke & James's Table 2.1 for CS-A (card C18). Dates only, as printed;
no price, inflation or money series was opened to build it.

## Sources

- Bordo, M. D. and A. J. Schwartz (1994), "The Specie Standard as a Contingent Rule: Some Evidence for Core and
  Peripheral Countries, 1880–1990", NBER Working Paper 4860, frozen as `frame-a/bordo-schwartz-w4860`: Table 1A, PDF
  pp. 60–61 (printed pp. 57–58); Table 1B, PDF pp. 62–63 (printed pp. 59–60). Read from the page images (the text layer
  is a broken OCR).
- Bernanke, B. and H. James (1991), "The Gold Standard, Deflation, and Financial Crisis in the Great Depression: An
  International Comparison", in Hubbard (ed.), *Financial Markets and Financial Crises*, NBER, frozen as
  `frame-a/bernanke-james-chapter` (2026-09-30): Table 2.1, PDF p. 6 (printed p. 37).

## Steps

1. The protocol was written and committed before either coder ran
   (`studies/FT-001-part-1-what-trust-rests-on/notes/coding-cs-a-cs-b-tables.md`, 5300e0f0).
2. Two coders, apart, each a fresh Sonnet subagent, transcribed every cell of the seventeen economies' rows (JST R6's
   eighteen but Ireland) in Table 1A and 1B, and the fifteen frame G economies' rows in Table 2.1
   (`coders/c1/`, `coders/c2/`: their CSV files and their notes on what was hard to read).
3. The session compared them by economy, column and the ordered list of printed values (the coders numbered lines
   differently; the values were compared, not the numbering): Table 1A and 1B, 141 of 141 cell lists agree; Table 2.1,
   60 of 60 (`agreement.json`). No disagreement, so no settlement was needed.
4. `series.csv` is drawn from coder c2's file (it carries each cell's printed line): every date of convertibility,
   suspension, par value and gold-standard change, one row each, with its page and line; the reasons and the parity
   column stay in the coders' files (no card uses them). A date printed as `MM/YYYY` is the period `YYYY-MM`; a full
   date `YYYY-MM-DD`; "April 1925" is `1925-04`; a pair ("1875/1879") or a range ("1848-50") is kept as printed; a "—"
   in Table 2.1 is a row with value 0 and period "none printed".

## Assumptions

- The two coders are two runs of one model (Sonnet), not independent coders (W20): their agreement shows the reading
  is stable, not that it is right. The cells either marked unsure that a card uses (France's gold suspension 1936,
  Portugal's 1891 and 09/1931) are read again at the page by the cards' isolated check, another reader.
- Column groups in Table 1A carry no "silver"/"gold" label on the page; the first three columns are the bimetallic or
  silver convertibility block and the next four the gold block, as both coders read the headings.

## Uncertainty

- The scan is degraded on the right half of Table 1A (reasons, parity) and in Table 1B's headings; the dates are legible.
  Eight date cells were marked unsure by one or both coders (the `uncertainty` column names them); both coders read
  the same value in each.
