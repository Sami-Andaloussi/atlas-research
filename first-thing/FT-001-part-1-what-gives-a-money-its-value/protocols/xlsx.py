"""A small reader for .xlsx workbooks, from the standard library only (FT-001 M3).

The toolkit's interpreter has no openpyxl, and nothing is installed into it for one mission; an .xlsx file is a
zip of XML parts, and the acts' sources (the Bank of Canada–Bank of England database, Reinhart and Rogoff's
*Varieties* and *This Time Is Different* tables) need only their cells' values. Formulas are read as their
cached values; styles, merged cells and dates' number formats are ignored (the acts' sources hold years as
numbers).
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def _col(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def sheets(path: str | Path) -> list[str]:
    """The workbook's sheet names, in order."""
    with zipfile.ZipFile(path) as z:
        book = ET.fromstring(z.read("xl/workbook.xml"))
    return [s.get("name") for s in book.find("m:sheets", NS)]


def rows(path: str | Path, sheet: str) -> list[list[str | float | None]]:
    """Every row of one sheet as a list of values (strings, floats, or None for an empty cell)."""
    with zipfile.ZipFile(path) as z:
        book = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = {r.get("Id"): r.get("Target") for r in rels}
        rid = next(s.get(REL) for s in book.find("m:sheets", NS) if s.get("name") == sheet)
        part = target[rid].lstrip("/")
        part = part if part.startswith("xl/") else "xl/" + part
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
        data = ET.fromstring(z.read(part))
    out: list[list[str | float | None]] = []
    for row in data.iter(f"{{{NS['m']}}}row"):
        values: list[str | float | None] = []
        for cell in row.findall("m:c", NS):
            index = _col(cell.get("r"))
            while len(values) < index:
                values.append(None)
            kind = cell.get("t")
            v = cell.find("m:v", NS)
            if kind == "s" and v is not None:
                values.append(shared[int(v.text)])
            elif kind == "inlineStr":
                values.append("".join(t.text or "" for t in cell.iter(f"{{{NS['m']}}}t")))
            elif kind in ("str", "e") and v is not None:
                values.append(v.text)
            elif kind == "b" and v is not None:
                values.append(float(v.text))
            elif v is not None and v.text is not None:
                try:
                    values.append(float(v.text))
                except ValueError:
                    values.append(v.text)
            else:
                values.append(None)
        out.append(values)
    return out
