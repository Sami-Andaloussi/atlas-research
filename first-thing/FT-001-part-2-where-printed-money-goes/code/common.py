"""What every card's code of step d shares: the panels built once, the frozen series, the eras.

The annual and monthly panels (``panel.py``, its rules unchanged) are slow to build (they verify every
frozen file's hash); a run builds each once and every card reads the same objects. Nothing here reads
an outcome: it loads.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402

from ft.data import dbnomics, fred, worldbank  # noqa: E402

STUDY = Path(__file__).resolve().parents[1]
CARDS = STUDY / "cards"
RUNS = STUDY / "results" / "runs"
ERAS = ((1950, 1971), (1972, 1999), (2000, 2026))


@lru_cache(maxsize=1)
def annual() -> pd.DataFrame:
    return P.panel()


@lru_cache(maxsize=1)
def monthly() -> pd.DataFrame:
    """``panel.monthly()`` on the annual panel built once (it calls ``panel()`` itself otherwise)."""
    original = P.panel
    P.panel = annual
    try:
        return P.monthly()
    finally:
        P.panel = original


@lru_cache(maxsize=None)
def ifs(code: str, freq: str = "A") -> pd.Series:
    return P._ifs(code, freq)


@lru_cache(maxsize=None)
def fred_series(series: str, vintage: str = "2026-09-30") -> pd.Series:
    return fred.read(series, vintage).dropna()


def fred_monthly(series: str, vintage: str = "2026-09-30") -> pd.Series:
    x = fred_series(series, vintage)
    x = pd.Series(x.to_numpy(), index=x.index.to_period("M"))
    return x.groupby(level=0).mean()


def fred_quarterly_mean(series: str, vintage: str = "2026-09-30") -> pd.Series:
    """The quarter's mean of a monthly or weekly FRED series; a quarter needs its three months (or, for a
    weekly series, at least ten weeks)."""
    x = fred_series(series, vintage)
    q = x.index.to_period("Q")
    g = pd.Series(x.to_numpy(), index=q).groupby(level=0)
    months = pd.Series(x.index.to_period("M"), index=q).groupby(level=0).nunique()
    return g.mean()[months == 3]


def quarter_end_stock(series: str, vintage: str = "2026-09-30") -> pd.Series:
    """A quarterly stock that FRED dates at the quarter's first day, mapped to the quarter's last day
    (the value is the stock at the quarter's end: C13 (2))."""
    x = fred_series(series, vintage)
    idx = x.index.to_period("Q").end_time.normalize()
    return pd.Series(x.to_numpy(), index=idx)


@lru_cache(maxsize=None)
def wb(code: str) -> pd.Series:
    return P._wb(code)


def seam_months() -> dict[str, set[pd.Period]]:
    """Each IFS money's definition-change months (C11 (2), (3)): December 2001, IFS's switch to the
    central bank survey back-filled into line 14, and the money's own seam month, the first month its old
    (line 14) and new (monetary base) monthly series overlap. The United States and the euro area are
    read from FRED and the ECB: no IFS seam."""
    old, new = ifs("14____XDC", "M"), ifs("FASMB_XDC", "M")
    out: dict[str, set[pd.Period]] = {}
    areas = set(old.index.get_level_values(0)) | set(new.index.get_level_values(0))
    for a in areas:
        months = {pd.Period("2001-12", "M")}
        if a in old.index.get_level_values(0) and a in new.index.get_level_values(0):
            o, n = old.xs(a), new.xs(a)
            both = o[o > 0].index.intersection(n[n > 0].index)
            if len(both):
                months.add(both.min())
        out[a] = months
    out.pop("US", None)
    out.pop("U2", None)
    return out


def era_of(year: int) -> int | None:
    for i, (a, b) in enumerate(ERAS):
        if a <= year <= b:
            return i
    return None


def yoy(cpi: pd.Series) -> pd.Series:
    """The twelve-month change in percent on a full calendar of months."""
    if not len(cpi):
        return pd.Series(dtype=float)
    full = pd.period_range(cpi.index.min(), cpi.index.max(), freq="M")
    c = cpi.reindex(full)
    return 100 * (c / c.shift(12) - 1)


__all__ = ["P", "dbnomics", "fred", "worldbank", "np", "pd"]
