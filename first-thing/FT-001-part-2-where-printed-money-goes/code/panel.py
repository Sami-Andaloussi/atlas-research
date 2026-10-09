"""The annual panel part 2 reads: one row per money (a country, or the euro area) and year.

Built only from frozen vintages (``VINTAGES``); every card that reads it names this file and the commit
that holds it. From the study's folder, ``../../toolkit/bin/ftpy code/panel.py`` prints the coverage
(counts of moneys and years per variable) — conditions, never an outcome.

**The rules** (fixed here, before any card runs; `notes/data.md` says why each):

1. *Units.* IFS values are multiplied by the multiplier their series name ends with (all "Millions" on
   the 2026-09-30 vintage). Stocks are end-of-year; GDP is the year's flow; the CPI is the year's
   average.
2. *Two IFS presentations, one series.* Base money = IFS line 14 "Reserve Money" (the old
   presentation, 1950 to about 2008) chained to "Central Bank Survey, Monetary Base" (from 2001): the
   old series is scaled by the ratio of the two in the **first year both exist** and used before that
   year, the new one from it — no jump at the seam. The same chaining for broad money (lines 35L and
   FMB) and for the central bank's asset lines (12A→FASAG claims on central government, 12E→FASAD claims
   on banks, 12D→FASAO claims on others, 11→FASAF foreign assets; the old "others" line is claims on the
   private sector only, flagged). A money whose two series disagree by more than 10% across their
   overlap years (max/min of the ratio above 1.10) is flagged ``*_break``: a change of definition, not
   of money; cards report it apart where it matters.
3. *Fallbacks.* Where IFS lacks nominal GDP, real GDP or the CPI for a money-year, the World Bank's
   series is used, scaled by the median IFS/World-Bank ratio over the years both exist (``*_source`` =
   ``wb``); a money IFS lacks altogether takes the World Bank's series as it is (``wb_unscaled``); where
   the two never overlap, IFS is kept alone (no scale, no filling).
4. *The United States* from FRED (the door's own series): base money = BOGMBASE in December (billions)
   chained before 1959 to IFS line 14 in dollars; GDP = the year's average of GDP (SAAR, billions); the
   CPI = CPIAUCSL's average (the 2026-09-27 vintage, the door's); real GDP = GDPC1's average; broad money =
   M2SL in December; the Fed's assets from H.4.1 on the last Wednesday of December — Treasuries
   (TREAST), mortgage-backed securities (WSHOMCB, as "others"), and everything else on WALCL (loans,
   facilities, swaps: as "banks and facilities").
5. *The euro area* as one money from 1999 (area ``U2``): base money = the ECB's Eurosystem base money in
   December (average over the maintenance period, ILM); nominal and real GDP = the sums of the ECB's four
   quarters (changing composition; current prices and chain-linked volumes); the CPI = the HICP's
   average; broad money = M3 in December (BSI); the short rate = the deposit facility rate (FM, daily).
   A money-year that uses the euro outside the area itself is dropped: its end-of-year rate against the
   dollar equals the euro area's within 0.1% in that year and the year before or after (two years in a
   row, so a peg that crosses the euro's rate once is not caught). Members' base money before they joined
   is kept where IFS has it (the founding members' is absent from this mirror: said in `notes/data.md`).
6. *Not moneys, and broken units.* IFS areas whose code starts with a digit are IMF groups, dropped. The
   historical areas (the USSR ``SUH``, Czechoslovakia ``CSH``, Yugoslavia ``YUC``, ``DE2``) are kept as
   moneys. A money whose ratio of base money to GDP moves by a factor of 100 or more from one year to the
   next, or whose median ratio lies outside 0.1%–300%, is flagged ``units_break`` (a redenomination or a
   unit the two sources do not share, not an economic event — the highest medians of the panel otherwise
   stay below that ceiling);
   cards drop flagged moneys and list them. Years with fewer than twelve months (or four quarters) are
   not averaged: a year's mean needs the whole year.
7. *Rates.* The short rate is the policy rate where IFS has it, else the money-market rate, else the
   Treasury-bill rate (``rate_short`` and ``rate_source``); annual averages, and the December value from
   the monthly series (``rate_short_dec``). The United States: FEDFUNDS.
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from ft.data import dbnomics, fred, worldbank

VINTAGES = {"ifs": "2026-09-30", "ecb": "2026-09-30", "wdi": "2026-09-30", "fred": "2026-09-30",
            "fred_cpi": "2026-09-27"}
BREAK_TOL = 1.10     # max/min of the old/new ratio over the overlap years above which a seam is a definition change
UNION_TOL = 0.001    # an end-of-year dollar rate within 0.1% of the euro area's: the year is inside the euro
LEVEL_MAX, LEVEL_MIN = 3.0, 0.001   # a median base-to-GDP ratio outside 0.1%-300%: the two series do not share a unit


def _ifs(code: str, freq: str = "A") -> pd.Series:
    t = dbnomics.read("IMF", "IFS", f"{freq}..{code}", VINTAGES["ifs"]).dropna(subset=["value"])
    if t.empty:
        return pd.Series(dtype=float)
    mult = t.series_name.map(dbnomics.multiplier).fillna(1.0)
    t = t.assign(value=t.value * mult)
    if freq == "A":
        t = t.assign(year=t.period.astype(int))
        return t.set_index(["REF_AREA", "year"]).value.sort_index()
    t = t.assign(month=pd.PeriodIndex(t.period, freq="M"))
    return t.set_index(["REF_AREA", "month"]).value.sort_index()


def chain(old: pd.Series, new: pd.Series) -> tuple[pd.Series, set[str]]:
    """Chain ``old`` onto ``new`` money by money (rule 2); the moneys whose seam is a definition change."""
    out, breaks = [], set()
    areas = set(old.index.get_level_values(0)) | set(new.index.get_level_values(0))
    for a in sorted(areas):
        o = old.xs(a) if a in old.index.get_level_values(0) else pd.Series(dtype=float)
        n = new.xs(a) if a in new.index.get_level_values(0) else pd.Series(dtype=float)
        o, n = o[o > 0], n[n > 0]
        both = o.index.intersection(n.index)
        if len(both):
            ratio = n[both] / o[both]
            if ratio.max() / ratio.min() > BREAK_TOL:
                breaks.add(a)
            first = both.min()
            s = pd.concat([o[o.index < first] * ratio[first], n])
        else:
            s = pd.concat([o, n[~n.index.isin(o.index)]])
        out.append(s.sort_index().rename(a))
    frame = pd.concat({s.name: s for s in out if len(s)}, names=["area", "year"])
    return frame.sort_index(), breaks


def _wb(code: str) -> pd.Series:
    t = worldbank.read(code, VINTAGES["wdi"]).dropna(subset=["value"])
    econ = worldbank.read_economies(VINTAGES["wdi"]).set_index("iso3")
    t = t[t.iso3.isin(econ.index)]
    iso2 = t.iso3.map(econ.iso2)
    iso2 = iso2.where(t.iso3 != "EMU", "U2")
    return t.assign(area=iso2).set_index(["area", "year"]).value.sort_index()


def fill(ifs: pd.Series, wb: pd.Series) -> tuple[pd.Series, dict[str, str]]:
    """IFS, and the World Bank where IFS lacks a year, scaled by their median ratio (rule 3)."""
    out, how = [], {}
    for a in sorted(set(ifs.index.get_level_values(0)) | set(wb.index.get_level_values(0))):
        i = ifs.xs(a) if a in ifs.index.get_level_values(0) else pd.Series(dtype=float)
        w = wb.xs(a) if a in wb.index.get_level_values(0) else pd.Series(dtype=float)
        missing = w.index.difference(i.index)
        if len(missing) and len(w):
            both = i.index.intersection(w.index)
            if len(both):
                i = pd.concat([i, w[missing] * float(np.median(i[both] / w[both]))])
                how[a] = "wb"
            elif not len(i):
                i = w
                how[a] = "wb_unscaled"
            # IFS and the World Bank on disjoint years, never overlapping: no scale, so no filling
        if len(i):
            out.append(i.sort_index().rename(a))
    return pd.concat({s.name: s for s in out}, names=["area", "year"]).sort_index(), how


def _full_mean(x: pd.Series, per_year: int) -> pd.Series:
    g = x.groupby(x.index.year)
    return g.mean()[g.size() >= per_year]


def _fred_year(series: str, how: str, vintage: str | None = None, scale: float = 1.0,
               per_year: int = 12) -> pd.Series:
    """A FRED series by year: the mean of a full year (``per_year`` observations: 12 monthly, 4 quarterly),
    the December value, or the year's last observation (weekly H.4.1)."""
    x = fred.read(series, vintage or VINTAGES["fred"]).dropna()
    if how == "mean":
        y = _full_mean(x, per_year)
    elif how == "december":
        y = x[x.index.month == 12].groupby(x[x.index.month == 12].index.year).last()
    else:  # the last observation of each year (weekly H.4.1), only when it falls in December
        dec = x[x.index.month == 12]
        y = dec.groupby(dec.index.year).last()
    y.index.name = "year"
    return (y * scale).rename("US")


def _ecb(dataset: str, mask: str) -> pd.Series:
    t = dbnomics.read("ECB", dataset, mask, VINTAGES["ecb"]).dropna(subset=["value"])
    return t.set_index("period").value


def _us_and_euro() -> dict[str, dict[str, pd.Series]]:
    us = {
        "base": _fred_year("BOGMBASE", "december", scale=1e9),
        "gdp": _fred_year("GDP", "mean", scale=1e9, per_year=4),
        "cpi": _fred_year("CPIAUCSL", "mean", vintage=VINTAGES["fred_cpi"]),
        "rgdp": _fred_year("GDPC1", "mean", scale=1e9, per_year=4),
        "broad": _fred_year("M2SL", "december", scale=1e9),
        "cb_gov": _fred_year("TREAST", "last", scale=1e6),
        "cb_others": _fred_year("WSHOMCB", "last", scale=1e6),
        "rate_short": _fred_year("FEDFUNDS", "mean"),
        "rate_short_dec": _fred_year("FEDFUNDS", "december"),
    }
    us["cb_banks"] = (_fred_year("WALCL", "last", scale=1e6) - us["cb_gov"] - us["cb_others"]).dropna().rename("US")
    base = _ecb("ILM", "M.U2.C.LT00001MP.Z5.EUR")
    base.index = pd.PeriodIndex(base.index, freq="M")
    base = base[base.index.month == 12]
    base.index = base.index.year
    hicp = _ecb("ICP", "M.U2.N.000000.4.INX")
    hicp.index = pd.PeriodIndex(hicp.index, freq="M").year
    hicp = hicp.groupby(level=0).mean()[hicp.groupby(level=0).size() == 12]

    def quarters(mask: str) -> pd.Series:
        q = _ecb("MNA", mask)
        q.index = pd.PeriodIndex(q.index.str.replace("-", ""), freq="Q").year
        return q.groupby(level=0).sum()[q.groupby(level=0).size() == 4] * 1e6

    m3 = _ecb("BSI", "M.U2.Y.V.M30.X.1.U2.2300.Z01.E")
    m3.index = pd.PeriodIndex(m3.index, freq="M")
    m3 = m3[m3.index.month == 12]
    m3.index = m3.index.year
    dfr = _ecb("FM", "D.U2.EUR.4F.KR.DFR.LEV")
    dfr.index = pd.to_datetime(dfr.index)
    euro = {"base": (base * 1e6).rename("U2"), "cpi": hicp.rename("U2"),
            "gdp": quarters("Q.Y.I9.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.V.N").rename("U2"),
            "rgdp": quarters("Q.Y.I9.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.LR.N").rename("U2"),
            "broad": (m3 * 1e6).rename("U2"),
            "rate_short": dfr.groupby(dfr.index.year).mean()[
                dfr.groupby(dfr.index.year).apply(lambda d: d.index.month.nunique()) == 12].rename("U2"),
            "rate_short_dec": dfr[dfr.index.month == 12].groupby(dfr[dfr.index.month == 12].index.year).last().rename("U2")}
    for s in euro.values():
        s.index.name = "year"
    return {"US": us, "U2": euro}


def panel() -> pd.DataFrame:
    base, base_breaks = chain(_ifs("14____XDC"), _ifs("FASMB_XDC"))
    us_old = _ifs("14____USD")
    us_old = us_old.xs("US") if "US" in us_old.index.get_level_values(0) else pd.Series(dtype=float)
    broad, broad_breaks = chain(_ifs("35L___XDC"), _ifs("FMB_XDC"))
    cols = {"base": base, "broad": broad}
    breaks = {"base": base_breaks, "broad": broad_breaks}
    for name, (old, new) in {"cb_gov": ("12A___XDC", "FASAG_XDC"), "cb_banks": ("12E___XDC", "FASAD_XDC"),
                             "cb_others": ("12D___XDC", "FASAO_XDC"), "cb_foreign": ("11____XDC", "FASAF_XDC")}.items():
        cols[name], breaks[name] = chain(_ifs(old), _ifs(new))
    how = {}
    cols["gdp"], how["gdp"] = fill(_ifs("NGDP_XDC"), _wb("NY.GDP.MKTP.CN"))
    cols["rgdp"], how["rgdp"] = fill(_ifs("NGDP_R_XDC"), _wb("NY.GDP.MKTP.KN"))
    cols["cpi"], how["cpi"] = fill(_ifs("PCPI_IX"), _wb("FP.CPI.TOTL"))
    wb_broad = _wb("FM.LBL.BMNY.CN")
    rates = {"policy": _ifs("FPOLM_PA"), "money market": _ifs("FIMM_PA"), "treasury bill": _ifs("FITB_PA")}
    rates_m = {"policy": _ifs("FPOLM_PA", "M"), "money market": _ifs("FIMM_PA", "M"),
               "treasury bill": _ifs("FITB_PA", "M")}
    fx = _ifs("ENDE_XDC_USD_RATE")

    frame = pd.DataFrame(cols)
    frame.index.names = ["area", "year"]
    # the United States and the euro area from their own series (rules 4 and 5)
    special = _us_and_euro()
    frame = frame.drop(index=[a for a in ("US", "U2") if a in frame.index.get_level_values(0)], level=0)
    rows = []
    for area, series in special.items():
        f = pd.DataFrame({k: v for k, v in series.items() if k in cols or k in ("rate_short", "rate_short_dec")})
        if area == "US" and len(us_old):
            f["base"] = chain(pd.concat({"US": us_old}, names=["area", "year"]),
                              pd.concat({"US": series["base"]}, names=["area", "year"]))[0].xs("US")
        f.index.name = "year"
        rows.append(pd.concat({area: f}, names=["area", "year"]))
    frame = pd.concat([frame, *rows]).sort_index()
    frame["broad_wb"] = wb_broad.reindex(frame.index)

    # the short rate (rule 7), for the moneys other than the United States
    short = pd.Series(np.nan, index=frame.index)
    source = pd.Series(pd.NA, index=frame.index, dtype="object")
    short_dec = pd.Series(np.nan, index=frame.index)
    for name in ("treasury bill", "money market", "policy"):  # later names win: policy first
        r = rates[name].reindex(frame.index)
        short = r.where(r.notna(), short)
        source = source.where(r.isna(), name)
        m = rates_m[name]
        if len(m):
            dec = m[m.index.get_level_values(1).month == 12]
            dec.index = pd.MultiIndex.from_arrays([dec.index.get_level_values(0), dec.index.get_level_values(1).year],
                                                  names=["area", "year"])
            d = dec.reindex(frame.index)
            short_dec = d.where(d.notna(), short_dec)
    own = frame.index.get_level_values(0).isin(["US", "U2"])
    frame["rate_short"] = np.where(own, frame["rate_short"], short)
    frame["rate_short_dec"] = np.where(own, frame["rate_short_dec"], short_dec)
    frame["rate_source"] = np.where(frame.index.get_level_values(0) == "US", "federal funds",
                                    np.where(frame.index.get_level_values(0) == "U2", "ECB deposit facility", source))
    frame["gdp"] = frame.gdp.where(frame.gdp > 0)
    frame["fx_end"] = fx.reindex(frame.index)

    # not moneys (rule 6) and member-years inside the euro (rule 5)
    areas = frame.index.get_level_values(0)
    frame = frame[~areas.str.match(r"^\d")]
    euro_fx = fx.xs("U2") if "U2" in fx.index.get_level_values(0) else pd.Series(dtype=float)
    ey = frame.index.get_level_values(1)
    ref = pd.Series(ey, index=frame.index).map(euro_fx)
    match = pd.Series((frame.index.get_level_values(0) != "U2") & (ey >= 1999)
                      & ((frame.fx_end / ref - 1).abs() <= UNION_TOL).to_numpy(), index=frame.index)
    prev = match.groupby(level=0).shift(1, fill_value=False)
    nxt = match.groupby(level=0).shift(-1, fill_value=False)
    frame["inside_euro"] = match & (prev | nxt)
    ratio = np.log(frame.base / frame.gdp)
    jump = ratio.groupby(level=0).diff().abs() > np.log(100)
    level = ratio.groupby(level=0).median()
    odd = set(jump[jump].index.get_level_values(0)) | set(level[(level > np.log(LEVEL_MAX)) | (level < np.log(LEVEL_MIN))].index)
    frame["units_break"] = frame.index.get_level_values(0).isin(sorted(odd))
    for name, b in breaks.items():
        frame[f"{name}_break"] = frame.index.get_level_values(0).isin(sorted(b))
    for name, h in how.items():
        frame[f"{name}_source"] = pd.Series(frame.index.get_level_values(0), index=frame.index).map(h).fillna("ifs")
    return frame


def _chain_monthly(old: pd.Series, new: pd.Series) -> tuple[pd.Series, set[str]]:
    """Rule 2 on monthly series: the old presentation chained to the new at the first common month."""
    return chain(old, new)


def _fred_monthly(series: str, vintage: str | None = None, scale: float = 1.0) -> pd.Series:
    x = fred.read(series, vintage or VINTAGES["fred"]).dropna()
    x.index = x.index.to_period("M")
    return (x.groupby(level=0).mean() * scale)


def monthly() -> pd.DataFrame:
    """One row per money and month: base money (end of month), the CPI, the short rate, the dollar rate.

    Rules as for the annual panel (1, 2, 4, 5, 6, 7), on the monthly series: IFS monthly lines 14 and
    FASMB chained at their first common month; the United States from BOGMBASE, CPIAUCSL (the
    2026-09-27 vintage) and FEDFUNDS; the euro area from the ECB's base money (average over the
    maintenance period), the HICP and the deposit facility rate (the month's mean). The moneys the annual
    panel flags ``units_break`` and the money-months using the euro outside the area are flagged the same
    way (``units_break``, ``inside_euro``, read from the annual panel by year).
    """
    base, breaks = _chain_monthly(_ifs("14____XDC", "M"), _ifs("FASMB_XDC", "M"))
    cpi = _ifs("PCPI_IX", "M")
    fx = _ifs("ENDE_XDC_USD_RATE", "M")
    short = pd.Series(dtype=float)
    source = pd.Series(dtype=object)
    for name in ("treasury bill", "money market", "policy"):  # later names win: policy first
        r = _ifs({"treasury bill": "FITB_PA", "money market": "FIMM_PA", "policy": "FPOLM_PA"}[name], "M")
        short = r.combine_first(short) if len(short) else r
        source = pd.Series(name, index=r.index).combine_first(source) if len(source) else pd.Series(name, index=r.index)
    frame = pd.DataFrame({"base": base, "cpi": cpi, "rate_short": short, "fx_end": fx})
    frame.index.names = ["area", "month"]
    frame["rate_source"] = source.reindex(frame.index)
    frame = frame.drop(index=[a for a in ("US", "U2") if a in frame.index.get_level_values(0)], level=0)
    us = pd.DataFrame({"base": _fred_monthly("BOGMBASE", scale=1e9),
                       "cpi": _fred_monthly("CPIAUCSL", VINTAGES["fred_cpi"]),
                       "rate_short": _fred_monthly("FEDFUNDS")})
    us["rate_source"] = "federal funds"
    eb = _ecb("ILM", "M.U2.C.LT00001MP.Z5.EUR")
    eb.index = pd.PeriodIndex(eb.index, freq="M")
    eh = _ecb("ICP", "M.U2.N.000000.4.INX")
    eh.index = pd.PeriodIndex(eh.index, freq="M")
    dfr = _ecb("FM", "D.U2.EUR.4F.KR.DFR.LEV")
    dfr.index = pd.to_datetime(dfr.index).to_period("M")
    eu = pd.DataFrame({"base": eb * 1e6, "cpi": eh, "rate_short": dfr.groupby(level=0).mean()})
    eu["rate_source"] = "ECB deposit facility"
    parts = [frame]
    for area, f in (("US", us), ("U2", eu)):
        f.index.name = "month"
        parts.append(pd.concat({area: f}, names=["area", "month"]))
    frame = pd.concat(parts).sort_index()
    frame = frame[~frame.index.get_level_values(0).str.match(r"^\d")]
    annual = panel()
    years = pd.MultiIndex.from_arrays([frame.index.get_level_values(0), frame.index.get_level_values(1).year])
    for flag in ("units_break", "inside_euro"):
        frame[flag] = annual[flag].reindex(years).fillna(False).to_numpy()
    frame["base_break"] = frame.index.get_level_values(0).isin(sorted(breaks))
    return frame


def coverage(frame: pd.DataFrame) -> pd.DataFrame:
    """Moneys and years per variable, the members' euro years out: conditions only."""
    f = frame[~frame.inside_euro]
    rows = {}
    for c in ("base", "gdp", "cpi", "rgdp", "broad", "broad_wb", "cb_gov", "cb_banks", "cb_foreign", "rate_short"):
        x = f[c].dropna()
        years = x.index.get_level_values(1)
        rows[c] = {"moneys": x.index.get_level_values(0).nunique(), "first": int(years.min()),
                   "last": int(years.max()), "money-years": len(x)}
    return pd.DataFrame(rows).T


if __name__ == "__main__":
    m = monthly()
    mm = m[~m.inside_euro & ~m.units_break]
    print("monthly: base money for", mm.base.dropna().index.get_level_values(0).nunique(), "moneys;",
          "CPI for", mm.cpi.dropna().index.get_level_values(0).nunique(), "; both from",
          str(mm.dropna(subset=["base", "cpi"]).index.get_level_values(1).min()))
    p = panel()
    print(coverage(p).to_string())
    print("base money seams flagged as definition changes:", sorted(p[p.base_break].index.get_level_values(0).unique()))
    print("money-years using the euro outside the area, dropped:",
          p[p.inside_euro].groupby(level=0).size().to_dict())
    print("moneys with broken units (dropped by the cards):", sorted(p[p.units_break].index.get_level_values(0).unique()))
    if len(sys.argv) > 1:
        p.to_csv(sys.argv[1])
