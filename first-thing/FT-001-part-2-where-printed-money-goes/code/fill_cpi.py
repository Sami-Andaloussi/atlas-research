"""The gap-5 fill (cards C25 for A4 and C26 for the deciders; written 2026-10-02): where the CPI the study reads
(IFS, then the World Bank, as ``panel.py`` builds it; the United States and the euro area from FRED and the
ECB) is missing, fill it from the World Bank's Cross-Country Database of Inflation's headline CPI
(``hko.py``), at the frequency the study's rule needs, preferring monthly, then quarterly, then annual.

**The rule, as the cards fix it** (nothing here reads an outcome):

1. *Never replace a value the study already reads.* A fill touches only a year (annual panel) or a month
   (monthly panel) where the study's CPI is missing.
2. *Annual panel* (A4: a year's average, as ``panel.py`` rule 1): the database's value for a year is, in
   this order, the mean of its twelve monthly values (``hcpi_m``), else the mean of its four quarterly
   values (``hcpi_q``), else the level chained from annual inflation rates (``hcpi_a``: a run of
   consecutive years with a rate gives levels from the year before its first year, base 100). Each lower
   source is scaled to the sources above it (median ratio over the years both exist), so one database
   level series ``H`` is built; a source with no year in common with a non-empty ``H`` is not used, and
   where ``H`` is empty the annual run is the longest run (the later on a tie), unscaled.
3. *Monthly panel* (the deciders: the twelve-month change at monthly dates): ``hcpi_m`` only; the
   quarterly and annual series are not read, since they cannot give a value at a month without a
   rule of interpolation that nothing fixes.
4. *Scaling to the study's series* (``panel.py`` rule 3, as the World Bank's CPI is scaled): ``H`` times the
   median ratio (study / database) over the periods both exist; where the study has no CPI at all for the
   economy, ``H`` as it is (unscaled); where both exist but never at the same period, no fill. *Guard* (as
   rule 2's ``BREAK_TOL``): if on the periods both exist the ratio's maximum over its minimum exceeds
   1.10, the two are not one series and the economy is not filled (listed, counted).
5. Economies with no code in the panel (database territories the panel does not carry) are not read.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hko  # noqa: E402

TOL = 1.10


def _scale(study: pd.Series, db: pd.Series) -> tuple[float | None, int, float | None]:
    """(factor, overlap, max/min of the ratio): study / database over the periods both exist."""
    both = study.index.intersection(db.index)
    both = [p for p in both if db[p] > 0 and study[p] > 0]
    if not both:
        return None, 0, None
    r = np.array([study[p] / db[p] for p in both])
    return float(np.median(r)), len(both), float(r.max() / r.min())


def annual_levels(area: str) -> tuple[pd.Series, dict[int, str]]:
    """The database's merged annual level series ``H`` for an economy (rule 2) and the source of each year."""
    hm, hq, ha = hko.sheet("hcpi_m"), hko.sheet("hcpi_q"), hko.sheet("hcpi_a")
    parts: list[tuple[str, pd.Series]] = []
    if area in hm.index:
        s = hm.loc[area].dropna()
        g = s.groupby([p.year for p in s.index])
        parts.append(("monthly", g.mean()[g.size() == 12]))
    if area in hq.index:
        s = hq.loc[area].dropna()
        g = s.groupby([p.year for p in s.index])
        parts.append(("quarterly", g.mean()[g.size() == 4]))
    if area in ha.index:
        s = ha.loc[area].dropna()
        years = sorted(int(y) for y in s.index)
        runs, cur = [], []
        for y in years:
            if cur and y != cur[-1] + 1:
                runs.append(cur)
                cur = []
            cur.append(y)
        if cur:
            runs.append(cur)
        levels = []
        for run in runs:
            lv = {run[0] - 1: 100.0}
            for y in run:
                lv[y] = lv[y - 1] * (1 + float(s[y]) / 100)
            levels.append(pd.Series(lv).sort_index())
        parts.append(("annual", levels))
    H = pd.Series(dtype=float)
    src: dict[int, str] = {}
    for kind, s in parts:
        runs = s if isinstance(s, list) else [s]
        if kind == "annual" and len(H) == 0 and len(runs) > 1:
            runs = [max(runs, key=lambda r: (len(r), r.index.max()))]
        for r in runs:
            r = r[r > 0]
            if not len(r):
                continue
            if len(H) == 0:
                H = pd.concat([H, r]).sort_index()
                src.update({int(y): kind for y in r.index})
                continue
            f, n, spread = _scale(H, r)
            if f is None or spread > TOL:
                continue
            new = r[~r.index.isin(H.index)] * f
            H = pd.concat([H, new]).sort_index()
            src.update({int(y): kind for y in new.index})
    return H, src


def fill_annual(cpi: pd.Series) -> tuple[pd.Series, pd.DataFrame, dict[tuple[str, int], str]]:
    """``cpi``: the study's annual CPI, index (area, year). Returns the filled series, a log of the economies
    touched (area, years added, sources, a note; the refused ones with the reason) and the source of each filled
    year, ``{(area, year): 'monthly' | 'quarterly' | 'annual'}``."""
    cpi = cpi.dropna()
    out = [cpi]
    log, sources = [], {}
    have = {a: g.droplevel(0) for a, g in cpi.groupby(level=0)}
    areas_db = set(hko.sheet("hcpi_m").index) | set(hko.sheet("hcpi_q").index) | set(hko.sheet("hcpi_a").index)
    for area in sorted(areas_db):
        H, src = annual_levels(area)
        if not len(H):
            continue
        s = have.get(area, pd.Series(dtype=float))
        missing = [y for y in H.index if y not in s.index and 1970 <= y <= 2024]
        if not missing:
            continue
        if len(s):
            f, n, spread = _scale(s, H)
            if f is None:
                log.append((area, 0, "", "no year in common"))
                continue
            if spread > TOL:
                log.append((area, 0, "", f"ratio spread {spread:.3f} over {n} years"))
                continue
        else:
            f = 1.0
        add = pd.Series({y: float(H[y] * f) for y in missing}, dtype=float)
        add.index = pd.MultiIndex.from_product([[area], add.index], names=["area", "year"])
        out.append(add)
        sources.update({(area, int(y)): src[int(y)] for y in missing})
        kinds = sorted({src[int(y)] for y in missing})
        log.append((area, len(missing), "+".join(kinds), "" if len(s) else "no study CPI: database as it is"))
    res = pd.concat(out)
    res = res[~res.index.duplicated(keep="first")].sort_index()
    return res, pd.DataFrame(log, columns=["area", "years_added", "sources", "note"]), sources


def fill_monthly(cpi: pd.Series) -> tuple[pd.Series, pd.DataFrame]:
    """``cpi``: the study's monthly CPI, index (area, month). Rules 1, 3 and 4."""
    hm = hko.sheet("hcpi_m")
    cpi = cpi.dropna()
    out = [cpi]
    log = []
    have = {a: g.droplevel(0) for a, g in cpi.groupby(level=0)}
    for area in sorted(hm.index):
        H = hm.loc[area].dropna()
        H = H[H > 0]
        s = have.get(area, pd.Series(dtype=float))
        missing = [p for p in H.index if p not in s.index]
        if not missing:
            continue
        if len(s):
            f, n, spread = _scale(s, H)
            if f is None:
                log.append((area, 0, "no month in common"))
                continue
            if spread > TOL:
                log.append((area, 0, f"ratio spread {spread:.3f} over {n} months"))
                continue
        else:
            f = 1.0
        add = pd.Series({p: float(H[p] * f) for p in missing}, dtype=float)
        add.index = pd.MultiIndex.from_product([[area], pd.PeriodIndex(list(add.index), freq="M")], names=["area", "month"])
        out.append(add)
        log.append((area, len(missing), "" if len(s) else "no study CPI: database as it is"))
    res = pd.concat(out)
    res = res[~res.index.duplicated(keep="first")].sort_index()
    return res, pd.DataFrame(log, columns=["area", "months_added", "note"])
