"""Freeze every dataset part 2 reads, through the toolkit's fetchers (each asks Mnemosyne's Guard).

From the study's folder: ``../../toolkit/bin/ftpy code/fetch_data.py [--only fred|worldbank|ifs|ecb|livingston]``

Each dataset is frozen under today's date as its vintage (``data/<dataset>/<vintage>/``); the files stay
out of git, the manifests go in. The cards name the vintages they read, so a later run of this script
adds new vintages and changes no result. The door reads CPIAUCSL's 2026-09-27 vintage, the one the
dossier's check used (`bank/checks/doors-facts-2026-09-30.md`); this script does not refetch it.

A host the Guard refuses raises ``ft.data.guard.Wall``: it is declared, never fetched another way.
``www.macrohistory.net`` (Jorda-Schularick-Taylor) and ``www.globalmacrodata.com`` are such walls on
2026-09-30 (request a644c018d47b waits for Sami's live "OUI"); card C04 runs only once they lift.
"""

from __future__ import annotations

import sys

from ft.data import dbnomics, fred, freeze, guard, http, worldbank

#: FRED series (fred.stlouisfed.org, keyless CSV). What each is for: notes/data.md.
FRED = [
    # the door and A5 (the US)
    "BOGMBASE", "GDP", "GDPC1", "GDPDEF", "CPIAUCNS", "M2SL", "M2V", "M1SL", "M1V", "M2OWN", "TB3MS", "FEDFUNDS",
    "DGS10", "IOER", "IORR", "IORB", "TOTRESNS", "EXCSRESNS", "WRESBAL", "WALCL", "TREAST", "WSHOMCB",
    "FYFSGDA188S", "FYFSD",
    # surveyed and market expectations of inflation (the Livingston Survey waits: see LIVINGSTON below)
    "MICH", "T5YIE", "T10YIE",
    # A6 (the inflation tax and seigniorage)
    "CURRSL", "CURRCIR", "MBCURRCIR", "WCURCIR", "DEMDEPSL", "QBPBSTLKDPDOFFDPNIDP", "QBPBSTLKDPDOFFDPIDP",
    "QBPBSTLKDPDOFFDP", "ICNDR", "SNDR", "BOGZ1FL193020005Q", "TTLHH", "RESPPLLOPNWW",
    # C13: households' other deposits, to test Z.1's 2020Q4 rise for a reclassification
    "BOGZ1FL193030205Q",
    # A5's O4, "moved alongside" (the United States only; never tested): equity and house prices
    "NASDAQCOM", "CSUSHPISA",
]

#: World Bank WDI indicators (api.worldbank.org), every economy, 1960 on.
WDI = [
    "FM.LBL.BMNY.CN", "FM.LBL.BMNY.ZG", "FM.LBL.BMNY.GD.ZS", "FP.CPI.TOTL", "FP.CPI.TOTL.ZG",
    "NY.GDP.MKTP.CN", "NY.GDP.MKTP.KN", "NY.GDP.MKTP.KD.ZG", "NY.GDP.DEFL.KD.ZG", "FR.INR.DPST",
    "VC.BTL.DETH",  # battle-related deaths (UCDP, through the World Bank; from 1989): war at the start, A5
]

#: IMF International Financial Statistics, through DBnomics (api.db.nomics.world), every country.
IFS_ANNUAL = [
    # base money: the old presentation (line 14, to about 2008) and the central bank survey (from 2001)
    "14____XDC", "FASMB_XDC", "FMA_XDC", "FASMBEA_EUR", "14____USD",
    # what the base bought (A5's channel): claims on government, on banks, on others; foreign assets
    "12A___XDC", "FASAG_XDC", "12E___XDC", "FASAD_XDC", "12D___XDC", "FASAO_XDC", "11____XDC", "FASAF_XDC",
    # broad money, output, prices
    "35L___XDC", "FMB_XDC", "NGDP_XDC", "NGDP_R_XDC", "PCPI_IX",
    # rates (the floor; money demand) and the exchange rate (the regime)
    "FIMM_PA", "FITB_PA", "FPOLM_PA", "FIDR_PA", "FIGB_PA", "ENDE_XDC_USD_RATE",
]
IFS_MONTHLY = ["14____XDC", "FASMB_XDC", "FIMM_PA", "FITB_PA", "FPOLM_PA", "ENDE_XDC_USD_RATE", "PCPI_IX"]

#: The euro area as one money, from 1999 (the ECB's own data, through DBnomics: ``data-api.ecb.europa.eu``
#: is open but its certificate chain fails Python's check on this Mac, 2026-09-30): base money (average
#: over the maintenance period; ILM's end-of-month series could not be loaded by DBnomics that day), HICP,
#: nominal and real GDP (changing composition), M3, the deposit facility rate.
ECB = [("ECB", "ILM", "M.U2.C.LT00001MP.Z5.EUR"), ("ECB", "ICP", "M.U2.N.000000.4.INX"),
       ("ECB", "MNA", "Q.Y.I9.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.V.N"),
       ("ECB", "MNA", "Q.Y.I9.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.LR.N"),   # real GDP, chain-linked volumes
       ("ECB", "BSI", "M.U2.Y.V.M30.X.1.U2.2300.Z01.E"),             # M3, stocks
       ("ECB", "FM", "D.U2.EUR.4F.KR.DFR.LEV")]                      # the deposit facility rate, daily

#: IMF World Economic Outlook (April 2025), general government net lending, % of GDP (from 1980).
WEO = [("IMF", "WEO:2025-04", ".GGXCNL_NGDP.pcent_gdp")]

#: The Livingston Survey (Federal Reserve Bank of Philadelphia): the files as the survey publishes them.
#: **Escalated on 2026-09-30**: the Guard's content check reads the links' ``hash=`` parameter (a 32-digit
#: hexadecimal cache key the site puts in its own links) as non-public; reported to Mnemosyne
#: (``docs/signalements/2026-09-30-garde-faux-positif-…``). The URL is never altered to pass: the survey
#: waits, and the study reads surveyed expectations from the University of Michigan (FRED ``MICH``).
LIVINGSTON_BASE = "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/livingston-survey/"
LIVINGSTON = {
    "medians.xlsx": LIVINGSTON_BASE + "historical-data/medians.xlsx?sc_lang=en&hash=CD0870EE8D175A251D5321627B6040C7",
    "means.xlsx": LIVINGSTON_BASE + "historical-data/means.xlsx?sc_lang=en&hash=F23FEB7733AD966703D6014D2C440BEC",
    "MedianGrowthRate.xlsx": LIVINGSTON_BASE
    + "historical-data/MedianGrowthRate.xlsx?sc_lang=en&hash=B2EA848F3A660081D8F427DE535C3C97",
    "livingston-release-dates.xlsx": LIVINGSTON_BASE
    + "livingston-release-dates.xlsx?la=en&sc_lang=en&hash=F1B872596626611C6F8C973747D3DA37",
}


def run(only: str | None = None) -> None:
    if only in (None, "fred"):
        for s in FRED:
            f = fred.fetch(s)
            print(f"fred/{s}: {f.vintage}")
    if only in (None, "worldbank"):
        f = worldbank.fetch_economies()
        print(f"worldbank/_economies: {f.vintage}")
        for code in WDI:
            f = worldbank.fetch(code)
            print(f"worldbank/{code}: {f.vintage}")
    if only in (None, "ifs"):
        for code in IFS_ANNUAL:
            f = dbnomics.fetch("IMF", "IFS", f"A..{code}")
            print(f"{f.dataset}: {f.vintage} ({f.manifest['notes']})")
        for code in IFS_MONTHLY:
            f = dbnomics.fetch("IMF", "IFS", f"M..{code}")
            print(f"{f.dataset}: {f.vintage} ({f.manifest['notes']})")
        for provider, code, mask in WEO:
            f = dbnomics.fetch(provider, code, mask)
            print(f"{f.dataset}: {f.vintage} ({f.manifest['notes']})")
    if only in (None, "ifs", "ecb"):
        for provider, code, mask in ECB:
            f = dbnomics.fetch(provider, code, mask)
            print(f"{f.dataset}: {f.vintage} ({f.manifest['notes']})")
    if only in (None, "livingston"):
        try:
            files = [freeze.FileSpec(name, url, http.fetch(url)) for name, url in LIVINGSTON.items()]
        except guard.Escalation as exc:
            print(f"philadelphiafed/livingston: escalated, waits ({str(exc)[:120]}...)")
            return
        f = freeze.freeze("philadelphiafed/livingston", files,
                          source="Federal Reserve Bank of Philadelphia, Livingston Survey (historical data)",
                          licence="Federal Reserve Bank of Philadelphia: public data, cited; see its terms of use",
                          notes="medians and means of the forecasts for levels, growth of the median forecast, "
                                "release dates; documentation: livingston-documentation.pdf on the same site")
        print(f"philadelphiafed/livingston: {f.vintage}")


if __name__ == "__main__":
    run(sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--only" else None)
