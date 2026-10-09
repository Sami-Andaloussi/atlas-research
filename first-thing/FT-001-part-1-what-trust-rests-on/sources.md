# Sources

**Data**

- Òscar Jordà, Moritz Schularick and Alan M. Taylor, Macrohistory Database, release 6 (consumer prices, 1870–2020; CC BY-NC-SA 4.0).
- Federal Reserve Bank of St. Louis, FRED, CPIAUCNS (US consumer prices, monthly, from 1913), frozen 2026-09-30.
- World Bank, World Development Indicators, FP.CPI.TOTL.ZG (consumer-price inflation), frozen 2026-09-30.
- IMF, World Economic Outlook, October 2013, Argentina's end-of-period consumer prices, through DBnomics, frozen
  2026-10-08.
- The Bank of Canada–Bank of England sovereign default database (2025); IMF International Financial Statistics; the
  World Bank; Carmen Reinhart and Kenneth Rogoff's inflation and debt files (`C15`'s panel).
- Thomas Tooke, *A History of Prices*, vol. 2 (1838); Wesley C. Mitchell, *Gold, Prices, and Wages under the Greenback
  Standard* (1908), Table 2, and *A History of the Greenbacks* (1903); archive.org scans (A3).
- Frame a's sources: Bernanke and James's Table 2.1; Ana Carolina Garriga's central bank independence data (2025); Gill
  Hammond, *State of the art of inflation targeting*, Bank of England CCBS Handbook No. 29 (2012); the IMF's AREAER;
  David Cobham's classification of monetary policy frameworks (2024 update).
- The stablecoins' fixed set of papers: BIS Papers 141; BIS working papers 1146, 1164, 1219 and 1270; the Federal
  Reserve's IFDP 1334 and FEDS Notes; the New York Fed's Staff Report 1073; NBER working papers w27136, w30256,
  w30796 and w31160; and the issuers' launch documents as frozen.

Each dataset's URL, date retrieved and hash are in its manifest, published under `data/`; `results/datasets.yaml`
lists them all.

Of the series the study reconstructed (`data/reconstructed/`), one ships with its values: `ft001-g`, our own coding of
the issuers' launch documents. The others ship as their manifests only, which name their sources and how each series
was built. Their rows carry values from other publishers' datasets, which we republish only where a licence allows it:
Reinhart and Rogoff; Ilzetzki, Reinhart and Rogoff; the Macrohistory Database (CC BY-NC-SA 4.0); the Bank of England's
Millennium dataset; Chinn and Ito; the IMF, the AREAER among them. Or they transcribe tables of printed works (Bordo and
Schwartz's Tables 1A and 3, Bernanke and James's Table 2.1, Homer and Sylla's Table 42), which are not republished: their
values are verifiable at the table or page each row names. The public copies of the results leave out, likewise, Chinn
and Ito's index values and Ilzetzki, Reinhart and Rogoff's 2016 classes (the keys `ka_open` and `irr_class_2016`, in
`C06`, `C08`, `C09`, `C10`, `C12` and `C14`, with Cobham's first years in `C14`); each economy's line, its crossing and onset
dates, entry tercile and dated acts with each act's year before (the key `lines`, in `C04`, `C07` and `C15`), computed
or compiled in part from Reinhart and Rogoff's and JST's files; each economy's gold status in 1932–34, from Bernanke
and James's table (`status_1932_34`, in `C18`); each economy's inflation-target adoption year and the years Bordo and
Schwartz leave unclassed (`adoption_years`, `unclassed`, in `C19`); and the economy-years set apart with their JST rates
(`set_apart`, in `C20`).

**Works cited at their passages** (the passage and page of each are in the register's claims)

- Barsky, R. & Kilian, L. (2001), "Do We Really Know That Oil Caused the Great Stagflation?", NBER WP 8389.
- Bernanke, B. & James, H. (1991), "The Gold Standard, Deflation, and Financial Crisis in the Great Depression: An
  International Comparison", in Hubbard (ed.), *Financial Markets and Financial Crises*, NBER.
- Board of Governors of the Federal Reserve System, *Financial Stability Report*, May 2023.
- Bordo, M. D. (1992), "The Bretton Woods International Monetary System: An Historical Overview", NBER WP 4033.
- Bordo, M. D., Humpage, O. & Schwartz, A. J. (2006), "The Historical Origins of U.S. Exchange Market Intervention
  Policy", NBER WP 12662.
- Bordo, M. D. & Kydland, F. E. (1990), "The Gold Standard as a Rule", NBER WP 3367.
- Bordo, M. D., Landon-Lane, J. & Redish, A. (2004), "Good versus Bad Deflation", NBER WP 10329.
- Bordo, M. D. & Schwartz, A. J. (1994), "The Specie Standard as a Contingent Rule", NBER WP 4860.
- Calomiris, C. W. (1988), "Price and Exchange Rate Determination during the Greenback Suspension", *Oxford Economic
  Papers* 40(4), pp. 719–750.
- de la Torre, A., Levy Yeyati, E. & Schmukler, S. (2003), "Living and Dying with Hard Pegs", World Bank PRWP 2980.
- DeLong, J. B. (1997), "America's Peacetime Inflation: The 1970s", in Romer & Romer (eds.), *Reducing Inflation*.
- Eichengreen, B. & Sachs, J. (1985), "Exchange Rates and Economic Recovery in the 1930s", NBER WP 1498.
- Federal Reserve, FOMC, Statement on Longer-Run Goals and Monetary Policy Strategy, January 2012.
- Federal Reserve Bulletin, October 1919, December 1923 and August 1924 (FRASER).
- FEDS Notes, "Primary and Secondary Markets for Stablecoins", February 2024.
- Fischer, S., Sahay, R. & Végh, C. (2002), "Modern Hyper- and High Inflations", NBER WP 8930.
- Foote, C., Block, W., Crane, K. & Gray, S. (2004), "Economic Policy and Prospects in Iraq", *Journal of Economic
  Perspectives* 18(3).
- Grubb, F. (2012), "Is Paper Money Just Paper Money?", NBER WP 17997.
- Hong Kong Monetary Authority, its description of the Convertibility Undertakings.
- Judson, R. (2012), "Crisis and Calm: Demand for U.S. Currency at Home and Abroad", Federal Reserve IFDP 1058.
- Leeper, E. M. & Leith, C. (2016), "Understanding Inflation as a Joint Monetary-Fiscal Phenomenon", NBER WP 21867.
- Liu, J., Makarov, I. & Schoar, A. (2023), "Anatomy of a Run: The Terra Luna Crash", NBER WP 31160.
- Luther, W. J. & White, L. H. (2011), "Positively Valued Fiat Money after the Sovereign Disappears: The Case of
  Somalia".
- Posen, A. S. (1995), "Declarations Are Not Enough", *NBER Macroeconomics Annual* 10.
- Rolnick, A. J. & Weber, W. E. (1997), "Money, Inflation, and Output under Fiat and Commodity Standards", *Journal of
  Political Economy* 105(6); the Federal Reserve Bank of Minneapolis *Quarterly Review* reprint, whose pages are cited.
- Sargent, T. J. (1982), "The Ends of Four Big Inflations", in Hall (ed.), *Inflation: Causes and Effects*, NBER.
- Sargent, T. J. & Velde, F. R. (1995), "Macroeconomic Features of the French Revolution", *Journal of Political
  Economy* 103(3).
- Silber, W. L. (2007), *When Washington Shut Down Wall Street*, Princeton University Press.
- Velde, F. R. & Weir, D. R. (1992), "The Financial Market and Government Debt Policy in France, 1746–1793", *Journal
  of Economic History* 52(1).
- White, E. N. (1995), "The French Revolution and the Politics of Government Finance, 1770–1815", *Journal of Economic
  History* 55(2).
- Willard, K., Guinnane, T. & Rosen, H. (1995), "Turning Points in the Civil War: Views from the Greenback Market",
  NBER WP 5381.

Named as positions, through the works that report them: Mitchell (1903), Friedman and Schwartz (1963), Blinder
(1979), Bruno and Sachs (1985), Darby et al. (1983), Alesina and Summers (1993), Ball and Sheridan (2003).
