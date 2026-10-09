# ft001-bs3 — reconstructed dataset

Bordo and Schwartz's Table 3 (NBER Working Paper 4860, printed p. 62), transcribed for FT-001 part 1: inflation in GNP deflators, log-trend growth rates, by regime, for the twenty-one economies and the G10-and-Switzerland row j. Moved out of `code/sources_v11.py` (where it sat as a literal) on 2026-10-09, so that the public copy ships its manifest only (Sami's rule of 2026-10-09: tables of printed works are not republished); the values are unchanged.

## Sources

- Bordo, M. D. and A. J. Schwartz (1994), "The Specie Standard as a Contingent Rule: Some Evidence for Core and
  Peripheral Countries, 1880–1990", NBER Working Paper 4860, frozen as `frame-a/bordo-schwartz-w4860`: Table 3,
  printed p. 62, "Inflation (GNP deflators), log-trend growth rates", columns gold standard (1881–1913), Bretton Woods
  (1946–70) and the float (1974–90); the twenty-one economies' rows and row j (the G10 and Switzerland, together).
  Licence of the source: "(c) the authors, all rights reserved (NBER working paper): cited, never republished".

## Steps

1. The table's cells were read for FT-001 part 1 (step d, registry v11) and typed into `code/sources_v11.py` as the
   literal `BS3` (and row j as constants), each cell as printed; "na" left out.
2. On 2026-10-09 (the workshop's pre-publication check, Sami's rule that tables of printed works are not
   republished), the literal was moved here, one row per printed cell, with its row and page in `locator`; columns
   `iso3`, `name` and `regime` (gold, bw, float) say which cell. Row j is `iso3` G10J. The code now reads this set
   (`sources_v11._bs3()`, which builds `BS3`); the register's numbers are unchanged (checked key by key).

## Assumptions

- None beyond the transcription: no value is computed here.

## Uncertainty

- A transcription of a printed table: one reader, the cells read off the page; the values feed only the comparisons
  the study prints (the G10 row's three rates, the exits' range, the gap's median and range).
