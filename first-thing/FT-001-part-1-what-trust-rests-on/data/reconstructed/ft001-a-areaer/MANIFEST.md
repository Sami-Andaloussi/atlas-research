# ft001-a-areaer — reconstructed dataset

The candidates for frame a's panel 4 from 2012. A candidate is a money listed for the first time in the
IMF AREAER's "Inflation-targeting framework" column in an edition from 2012 on, when the edition before did
not list it. The list follows M4's section 14 (R-A1 to R-A6, committed alone, ae91b27), which completes P20
and P21 under section 13. **A candidate is not an adopter.** Membership and date come from the central
bank's own announcement (P21, R-A4). Until that announcement is frozen, every candidate is *cannot be read*.
This list counts nothing.

## Sources

- The IMF's *Annual Report on Exchange Arrangements and Exchange Restrictions*, editions 2011–2023
  (`frame-a/areaer-2011-2023`, 2026-10-01, 01c0a38). Sami downloaded them by hand. The source is the framework
  grid, "De Facto Classification of Exchange Rate Arrangements and Monetary Policy Frameworks, April 30, Y".
  It is Table 1 in 2011–13, Table 2 in 2014–19 and Table 4 in 2020–23, and only its inflation-targeting
  column was read.

## Steps

1. Section 14 was committed alone (ae91b27), after reading only the 2012 legend.
2. Two coders (Sonnet agents, isolated, neither seeing the other's file) coded the column in all 13 editions
   from the page images. Their files are kept in `coders/`. Both counts equal the bracketed count the
   header prints in every edition (31, 32, 34, 34, 36, 38, 40, 41, 41, 43, 45, 45, 45).
3. **Agreement** (`agreement.json`): after name normalisation, the two lists are identical, κ = 1.00 over
   624 country-editions. The normalisation is "Sarbia" = Serbia (a 2019 misprint), "Czech Rep." = Czech
   Republic, "Dominican Rep." = Dominican Republic, "Korea, Rep. of" = Korea and "Türkiye" = Turkey.
4. `it-column.csv` holds the column per edition with each country's workshop code. `series.csv` holds the
   candidates.

## Assumptions

- R-A1 to R-A6. The framework column is "as indicated by country officials" (the Overview), so it is
  de jure. The exchange-rate rows (IMF staff's de facto classification) were not read for this list.
- Edition Y is read at 30 April of Y, with 2011 as the base.
- A money that leaves the column and returns is a candidate at its return, flagged `re-entry`.
- The edition's year is never a date (section 13).

## Uncertainty

- **18 candidates**:
  - 2012: Dominican Republic
  - 2013: Japan, Paraguay
  - 2014: Uganda
  - 2015: India, Russia
  - 2016: Kazakhstan, Uruguay (`re-entry`)
  - 2017: Argentina, Ukraine
  - 2018: Costa Rica, Jamaica
  - 2020: Seychelles, Sri Lanka
  - 2021: Kenya, Uzbekistan
  - 2023: Mauritius, Mongolia
- **Left the column**: Uruguay 2014 (back in 2016), Argentina 2018, Seychelles 2023 and Ukraine 2023. These are
  frame a facts, said here and used nowhere yet.
- **Footnotes are kept in `note`.** Some mark a framework still in transition: "preliminary steps toward
  inflation targeting" up to 2018, then "in transition toward inflation targeting", and "inflation
  targeting 'lite'" for Jamaica in 2018–20. P21's announcement test decides each such case. A candidate
  whose announcement states no explicit numerical target adopted as the policy's anchor is not an adopter.
- The United States is in no edition's column, so P21's exclusion of the Federal Reserve is not needed here.
- **Next step**: rule each candidate's central-bank host, then freeze its announcement. Hosts that are
  refused or answer 403 go to the engine in one grouped list.
