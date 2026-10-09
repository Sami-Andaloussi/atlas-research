"""A minimal reader for ``.xlsx`` workbooks (Office Open XML), the pilot's own copy (gap 5, 2026-10-02): the
toolkit has no ``openpyxl`` and nothing is installed. Written after reading E3's reader
(``bank/maps/FT-002/missions/code/m0b/xlsx.py``); nothing is imported from it.

``Book(data)`` reads the sheet names and shared strings; ``Book.rows(sheet)`` streams one sheet as
``{row number: {column number: value}}`` (a value is a ``str`` or a ``float``; empty cells are absent,
empty strings are dropped).
"""

from __future__ import annotations

import io
import re
import xml.etree.ElementTree as ET
import zipfile

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def _col(letters: str) -> int:
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


class Book:
    def __init__(self, data: bytes) -> None:
        self.z = zipfile.ZipFile(io.BytesIO(data))
        book = ET.fromstring(self.z.read("xl/workbook.xml"))
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(self.z.read("xl/_rels/workbook.xml.rels"))}
        self.paths: dict[str, str] = {}
        for sheet in book.find(NS + "sheets"):
            target = rels[sheet.get(RNS + "id")]
            self.paths[sheet.get("name")] = "xl/" + target.lstrip("/").removeprefix("xl/")
        self.strings: list[str] = []
        if "xl/sharedStrings.xml" in self.z.namelist():
            self.strings = ["".join(t.text or "" for t in si.iter(NS + "t"))
                            for si in ET.fromstring(self.z.read("xl/sharedStrings.xml"))]

    @property
    def sheet_names(self) -> list[str]:
        return list(self.paths)

    def rows(self, sheet: str) -> dict[int, dict[int, str | float]]:
        out: dict[int, dict[int, str | float]] = {}
        with self.z.open(self.paths[sheet]) as handle:
            for _, el in ET.iterparse(handle):
                if el.tag != NS + "row":
                    continue
                for c in el.findall(NS + "c"):
                    m = re.fullmatch(r"([A-Z]+)(\d+)", c.get("r"))
                    letters, row = m.group(1), int(m.group(2))
                    t, v = c.get("t"), c.find(NS + "v")
                    if t == "inlineStr":
                        value: str | float = "".join(x.text or "" for x in c.iter(NS + "t"))
                    elif v is None or v.text is None:
                        continue
                    elif t == "s":
                        value = self.strings[int(v.text)]
                    elif t in ("str", "e"):
                        value = v.text
                    else:
                        value = float(v.text)
                    if value == "":
                        continue
                    out.setdefault(row, {})[_col(letters)] = value
                el.clear()
        return out
