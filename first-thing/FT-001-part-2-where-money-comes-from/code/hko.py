"""The World Bank's Cross-Country Database of Inflation (Ha, Kose and Ohnsorge; frozen as
``worldbank-inflation/ha-kose-ohnsorge`` 2026-10-02): the headline CPI sheets the gap-5 fill reads
(``hcpi_m`` and ``hcpi_q``, indices; ``hcpi_a``, annual inflation rates), mapped to the panel's economy codes.

Nothing else of the workbook is read. The fill rule itself is in ``fill_cpi.py`` (cards C25 and C26).
"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import xlsx_read  # noqa: E402

from ft.data import freeze, worldbank  # noqa: E402

DATASET = ("worldbank-inflation/ha-kose-ohnsorge", "2026-10-02")
WDI_VINTAGE = "2026-09-30"   # the panel's own table of economies (iso3 -> iso2), as panel._wb reads it
#: Nothing is added to the World Bank's table of economies (the cards' rule (e)): a territory of the database
#: the table does not carry (Anguilla, Montserrat, ...) is listed in ``frame.attrs['unmapped']`` and not read.
EXTRA_ISO3: dict[str, str] = {}


@lru_cache(maxsize=1)
def _book() -> xlsx_read.Book:
    return xlsx_read.Book(freeze.load(*DATASET).read_bytes("Inflation-data.xlsx"))


def _iso3_to_area() -> dict[str, str]:
    econ = worldbank.read_economies(WDI_VINTAGE).set_index("iso3")
    out = {iso3: iso2 for iso3, iso2 in econ.iso2.items() if isinstance(iso2, str)}
    out["EMU"] = "U2"
    out.update(EXTRA_ISO3)
    return out


@lru_cache(maxsize=None)
def sheet(name: str) -> pd.DataFrame:
    """One headline-CPI sheet as a frame: rows = economy code of the panel (``area``), columns = periods
    (monthly: ``Period('M')``, quarterly: ``Period('Q')``, annual: int years); the economies the table cannot
    map are listed in ``frame.attrs['unmapped']``."""
    rows = _book().rows(name)
    head = rows[1]
    # the first five columns are labels; header cells from the first numeric one on are periods
    first = min(c for c, v in head.items() if isinstance(v, float))
    cols = {c: v for c, v in head.items() if c >= first and isinstance(v, float)}
    if name.endswith("_m"):
        per = {c: pd.Period(f"{int(v) // 100}-{int(v) % 100:02d}", "M") for c, v in cols.items()}
    elif name.endswith("_q"):
        per = {c: pd.Period(f"{int(v) // 10}Q{int(v) % 10}", "Q") for c, v in cols.items()}
    else:
        per = {c: int(v) for c, v in cols.items()}
    iso = _iso3_to_area()
    data, unmapped = {}, []
    for r in sorted(rows):
        if r == 1:
            continue
        row = rows[r]
        code = row.get(1)
        if not isinstance(code, str):
            continue
        area = iso.get(code)
        if area is None:
            unmapped.append((code, row.get(3)))
            continue
        vals = {per[c]: float(v) for c, v in row.items() if c in per and isinstance(v, float)}
        if vals:
            data[area] = pd.Series(vals).sort_index()
    frame = pd.DataFrame(data).T
    frame.index.name = "area"
    frame.attrs["unmapped"] = unmapped
    return frame


if __name__ == "__main__":
    for s in ("hcpi_m", "hcpi_q", "hcpi_a"):
        f = sheet(s)
        print(s, f.shape, "unmapped:", f.attrs["unmapped"])
