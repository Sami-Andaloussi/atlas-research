"""A small reader for .xls (BIFF8, and BIFF5) workbooks, from the standard library only (FT-001 M3, panel).

The toolkit's interpreter has no xlrd, and nothing is installed into it for one mission (FT-001-M3-panel.md,
section 6); Reinhart and Rogoff's inflation and debt workbooks are .xls. An .xls file is an OLE2 compound file
whose ``Workbook`` (or ``Book``) stream is a sequence of BIFF records; this module reads the sheet list
(``BOUNDSHEET``), the shared strings (``SST`` with its ``CONTINUE`` records) and the cells: ``LABELSST``,
``LABEL``, ``NUMBER``, ``RK``, ``MULRK`` and ``FORMULA``'s cached numbers. Styles, dates' formats and merged
cells are ignored. The twin of ``xlsx.py``: :func:`sheets` and :func:`rows` have the same shapes.
"""

from __future__ import annotations

import struct
from functools import cache
from pathlib import Path

_END = 0xFFFFFFFA


def _stream(data: bytes, want: tuple[str, ...] = ("Workbook", "Book")) -> bytes:
    if data[:8] != b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        raise ValueError("not an OLE2 compound file")
    sec = 1 << struct.unpack_from("<H", data, 0x1E)[0]
    mini = 1 << struct.unpack_from("<H", data, 0x20)[0]
    dir0, = struct.unpack_from("<I", data, 0x30)
    cutoff, = struct.unpack_from("<I", data, 0x38)
    mf0, = struct.unpack_from("<I", data, 0x3C)
    nmf, = struct.unpack_from("<I", data, 0x40)
    dif0, = struct.unpack_from("<I", data, 0x44)
    ndif, = struct.unpack_from("<I", data, 0x48)
    difat = list(struct.unpack_from("<109I", data, 0x4C))

    def sector(i: int) -> bytes:
        return data[(i + 1) * sec:(i + 2) * sec]

    s = dif0
    for _ in range(ndif):
        vals = struct.unpack("<%dI" % (sec // 4), sector(s))
        difat += list(vals[:-1])
        s = vals[-1]
    fat: list[int] = []
    for fs in difat:
        if fs < _END:
            fat += list(struct.unpack("<%dI" % (sec // 4), sector(fs)))

    def chain(start: int) -> bytes:
        out, s, seen = [], start, 0
        while s < _END and seen <= len(fat):
            out.append(sector(s))
            s = fat[s]
            seen += 1
        return b"".join(out)

    directory = chain(dir0)
    entries = []
    for i in range(0, len(directory), 128):
        e = directory[i:i + 128]
        nl, = struct.unpack_from("<H", e, 0x40)
        name = e[:max(nl - 2, 0)].decode("utf-16le", "replace")
        start, = struct.unpack_from("<I", e, 0x74)
        size, = struct.unpack_from("<I", e, 0x78)
        entries.append((name, e[0x42], start, size))
    root = entries[0]
    ministream = chain(root[2]) if root[2] < _END else b""
    minifat: list[int] = []
    if nmf:
        mfd = chain(mf0)
        minifat = list(struct.unpack("<%dI" % (len(mfd) // 4), mfd))
    for name, kind, start, size in entries:
        if name in want and kind == 2:
            if size < cutoff:
                out, s = [], start
                while s < _END:
                    out.append(ministream[s * mini:(s + 1) * mini])
                    s = minifat[s]
                return b"".join(out)[:size]
            return chain(start)[:size]
    raise ValueError("no Workbook stream: " + str([e[0] for e in entries]))


def _records(buf: bytes, pos: int = 0):
    while pos + 4 <= len(buf):
        rid, ln = struct.unpack_from("<HH", buf, pos)
        yield pos, rid, buf[pos + 4:pos + 4 + ln]
        pos += 4 + ln


def _rk(v: int) -> float:
    if v & 2:
        x = v >> 2
        if x & 0x20000000:
            x -= 0x40000000
        x = float(x)
    else:
        x = struct.unpack("<d", struct.pack("<Q", (v & 0xFFFFFFFC) << 32))[0]
    return x / 100 if v & 1 else x


def _sst(chunks: list[bytes]) -> list[str]:
    _, unique = struct.unpack_from("<II", chunks[0], 0)
    out: list[str] = []
    ci, buf, pos = 0, chunks[0], 8
    while len(out) < unique:
        if pos >= len(buf):
            ci += 1
            if ci >= len(chunks):
                break
            buf, pos = chunks[ci], 0
        ln, = struct.unpack_from("<H", buf, pos)
        flags = buf[pos + 2]
        pos += 3
        rich = ext = 0
        if flags & 8:
            rich, = struct.unpack_from("<H", buf, pos)
            pos += 2
        if flags & 4:
            ext, = struct.unpack_from("<I", buf, pos)
            pos += 4
        parts, remaining, wide = [], ln, flags & 1
        while remaining > 0:
            if pos >= len(buf):
                ci += 1
                buf = chunks[ci]
                wide, pos = buf[0] & 1, 1
            width = 2 if wide else 1
            take = min((len(buf) - pos) // width, remaining)
            seg = buf[pos:pos + take * width]
            parts.append(seg.decode("utf-16le", "replace") if wide else seg.decode("latin-1"))
            pos += take * width
            remaining -= take
        skip = rich * 4 + ext
        while skip > 0:
            if pos >= len(buf):
                ci += 1
                buf, pos = chunks[ci], 0
            t = min(skip, len(buf) - pos)
            pos += t
            skip -= t
        out.append("".join(parts))
    return out


@cache
def _book(path: str) -> tuple[bytes, int, tuple[tuple[str, int], ...], tuple[str, ...]]:
    wb = _stream(Path(path).read_bytes())
    biff, sheets, sst, last = 8, [], None, None
    for pos, rid, body in _records(wb):
        if rid == 0x0809 and pos == 0:
            biff = 8 if struct.unpack_from("<H", body, 0)[0] >= 0x0600 else 5
        if rid == 0x00FC:
            sst, last = [body], "sst"
        elif rid == 0x003C and last == "sst":
            sst.append(body)
        elif rid != 0x003C:
            last = None
        if rid == 0x0085:
            offset, = struct.unpack_from("<I", body, 0)
            kind, nl = body[5], body[6]
            if biff == 5:
                name = body[7:7 + nl].decode("latin-1", "replace")
            else:
                wide = body[7] & 1
                name = body[8:8 + nl * (2 if wide else 1)].decode("utf-16le" if wide else "latin-1", "replace")
            if kind == 0:
                sheets.append((name, offset))
    return wb, biff, tuple(sheets), tuple(_sst(sst) if sst else ())


def sheets(path: str | Path) -> list[str]:
    """The workbook's worksheet names, in order."""
    return [name for name, _ in _book(str(path))[2]]


def cells(path: str | Path, sheet: str) -> dict[tuple[int, int], str | float]:
    """Every non-empty cell of one sheet, keyed by (row, column), 0-based."""
    wb, biff, sheet_list, sst = _book(str(path))
    offset = dict(sheet_list)[sheet]
    out: dict[tuple[int, int], str | float] = {}
    for pos, rid, body in _records(wb, offset):
        if rid == 0x000A and pos > offset:  # EOF of the sheet
            break
        if rid == 0x00FD:
            r, c, _, i = struct.unpack_from("<HHHI", body, 0)
            out[(r, c)] = sst[i]
        elif rid == 0x0203:
            r, c, _, v = struct.unpack_from("<HHHd", body, 0)
            out[(r, c)] = v
        elif rid == 0x027E:
            r, c, _, v = struct.unpack_from("<HHHI", body, 0)
            out[(r, c)] = _rk(v)
        elif rid == 0x00BD:
            r, c0 = struct.unpack_from("<HH", body, 0)
            for k in range((len(body) - 6) // 6):
                _, v = struct.unpack_from("<HI", body, 4 + 6 * k)
                out[(r, c0 + k)] = _rk(v)
        elif rid == 0x0006:
            r, c, _ = struct.unpack_from("<HHH", body, 0)
            res = body[6:14]
            if res[6:8] != b"\xff\xff":  # a cached number (not a string, boolean or error)
                out[(r, c)] = struct.unpack("<d", res)[0]
        elif rid == 0x0204:
            r, c, _, ln = struct.unpack_from("<HHHH", body, 0)
            out[(r, c)] = body[8:8 + ln].decode("latin-1") if biff == 5 else body[9:9 + ln].decode("latin-1")
    return out


def rows(path: str | Path, sheet: str) -> list[list[str | float | None]]:
    """Every row of one sheet as a list of values (strings, floats, or None), like ``xlsx.rows``."""
    found = cells(path, sheet)
    if not found:
        return []
    nrows = max(r for r, _ in found) + 1
    out: list[list[str | float | None]] = [[] for _ in range(nrows)]
    for (r, c), v in sorted(found.items()):
        row = out[r]
        while len(row) < c:
            row.append(None)
        row.append(v)
    return out
