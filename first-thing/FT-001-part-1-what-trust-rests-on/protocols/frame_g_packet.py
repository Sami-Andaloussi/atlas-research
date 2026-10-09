"""FT-001 M7, frame g: the coders' packet (FT-001-M7-frame-g.md section 3 and section 5, step 4).

For every coin on the told list (``coins.csv``) except the never-issued, the packet gives:
- its name, ticker and marks (the marks stripped of any word of fate);
- every frozen reading and page that names it (``coins.csv`` and ``coins-draft-occurrences.csv``), the merged ids carried;
- its launch year **only from what the readings print**: BIS Papers 141's Annex 1 (the first date of a price, per coin) and
  Mizrach's Table 1 (first transaction on the Mainnet) and census (the vintage year). Where no reading prints one, the
  packet says "not printed". Nothing is filled from knowledge, and the printed values are never reconciled.

The packet shows **no fate** (no failure, no peg break, no phase date). It quotes no line of any reading: a coin's name as
printed and a locator, and nothing else. The builder refuses (fail-closed) to write a packet in which a word of fate sits.

Output: ``data/reconstructed/ft001-g/coders/packet/packet.csv`` and ``packet/<coin_id>.md``, one sheet per coin with an
empty coding table. The README beside them is the coders' instruction.

Run from the workshop's root:  toolkit/.venv/bin/python bank/maps/FT-001/missions/code/frame_g_packet.py
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import frame_g as G  # noqa: E402  (the frozen readings' reader: pdf_pages, frozen_path, READINGS)

ROOT = HERE.parents[4]
OUT = ROOT / "data" / "reconstructed" / "ft001-g"
PACKET = OUT / "coders" / "packet"
README = PACKET / "README.md"

PACKET_FIELDS = ("coin_id", "name", "ticker", "marks", "merged_ids", "readings_naming", "locators", "launch_year_printed",
                 "bis_group", "bis_peg", "bis_first_price_date", "bis_ccdata_first_date", "mizrach_first_transaction",
                 "mizrach_vintage", "sheet")
LINES = ("redemption", "limit by rule", "limit by institution", "taken back")
NOT_PRINTED = "not printed"

# A reading's id is a file name; the sheets use a neutral label (a folder name may carry a word of fate). The README gives
# the label -> folder table. Every reading of ``frame_g.READINGS`` has one.
LABELS = {
    "bis-papers-141": "BIS-P141",
    "mizrach-arxiv-2201-01392": "Mizrach",
    "bis-wp-1164": "BIS-WP1164",
    "bis-wp-1146": "BIS-WP1146",
    "bis-wp-1219": "BIS-WP1219",
    "bis-wp-1270": "BIS-WP1270",
    "fed-ifdp-1334": "IFDP-1334",
    "feds-notes-stable-in-stablecoins": "FEDS-2022",
    "feds-notes-primary-secondary": "FEDS-2024",
    "feds-notes-shadow-bank-runs": "FEDS-2025",
    "nber-w30796": "NBER-w30796",
    "nber-w27136": "NBER-w27136",
    "nber-w31160": "NBER-w31160",
    "nber-w30256": "NBER-w30256",
    "nyfed-anadu-runs": "NYFed-SR1073",
    "fsb-2020-global-stablecoins": "FSB-2020",
    "fsb-2023-crypto-stablecoins": "FSB-2023",
}
HTML_READINGS = frozenset(r.key for r in G.READINGS if r.kind == "html")

# Words of fate: the packet never prints one (the outcome, the peg, the phases). Matched as whole words, case-insensitive.
FATE = re.compile(
    r"\b(fail\w*|depeg\w*|de-peg\w*|collaps\w*|broke|broken|break|halt\w*|gated|suspend\w*|wound\s+down|shut\s*down|"
    r"defunct|dead|died|die|surviv\w*|delist\w*|discontinu\w*|ceased?|lost\s+its\s+peg|below\s+par|two\s+prices|"
    r"insolven\w*|bankrupt\w*|bank\s+runs?|runs?|crash\w*|vanish\w*|extinct|still\s+active|inactive)\b", re.I)


def fate_words(text: str) -> list[str]:
    """The words of fate in a text (empty when there is none)."""
    return [m.group(0) for m in FATE.finditer(text or "")]


def strip_fate(text: str) -> str:
    """A mark with its fate removed: each ';'-separated piece that holds a word of fate is dropped."""
    return "; ".join(p.strip() for p in (text or "").split(";") if p.strip() and not fate_words(p))


# =============================================================================================================
# 1. The list, and who names each coin where
# =============================================================================================================

def read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def in_the_mapping(coin: dict) -> bool:
    """Every coin on the list but the never-issued (out of the mapping, protocol section 3 / the person's check)."""
    return "never issued" not in (coin.get("marks", "") + " " + coin.get("check", "")).lower()


def plain_id(coin_id: str) -> str:
    return coin_id.removeprefix("G2: ").strip()


SEGMENT = re.compile(r"^(?:(?P<id>(?:G2:\s+)?[^:]+?):\s+)?(?:(?P<reading>[a-z][a-z0-9-]*)\s+)?(?:p\.)?(?P<page>\d+)$")


def parse_pages_field(coin: dict) -> list[tuple[str, str, int]]:
    """``coins.csv``'s ``pages`` as (name it was named as, reading, page). A merged line reads ``id: reading p.N``; a bare
    page belongs to the coin's one reading."""
    readings = [r for r in coin["readings"].split("; ") if r]
    out = []
    for seg in (s.strip() for s in coin["pages"].split(";")):
        if not seg:
            continue
        m = SEGMENT.match(seg)
        if not m:
            raise ValueError(f"{coin['coin_id']}: cannot read the page segment {seg!r}")
        reading = m.group("reading")
        if reading is None:
            if len(readings) != 1:
                raise ValueError(f"{coin['coin_id']}: a bare page {seg!r} with {len(readings)} readings")
            reading = readings[0]
        named = plain_id(m.group("id")) if m.group("id") else ""
        out.append((named, reading, int(m.group("page"))))
    return out


def merged_ids(coin: dict) -> list[str]:
    """The ids merged into this coin by the person's check: the named-as of its merged page segments."""
    return sorted({n for n, _, _ in parse_pages_field(coin) if n and n != coin["coin_id"]})


def locators_of(coin: dict, occurrences: list[dict]) -> list[dict]:
    """Every frozen reading and page that names the coin, under its own id or a merged id: one row per
    (reading, page, name as printed). The name as printed is the only text taken from a reading."""
    ids = {coin["coin_id"], *merged_ids(coin)}
    seen: dict[tuple, dict] = {}
    for named, reading, page in parse_pages_field(coin):
        key = (reading, page, named or coin["name"])
        seen.setdefault(key, {"reading": reading, "page": page, "named_as": named or coin["name"]})
    for o in occurrences:
        if o["coin_id"] in ids:
            key = (o["reading"], int(o["page"]), o["name_as_printed"])
            seen.setdefault(key, {"reading": o["reading"], "page": int(o["page"]), "named_as": o["name_as_printed"]})
    return sorted(seen.values(), key=lambda r: (list(LABELS).index(r["reading"]) if r["reading"] in LABELS else 99,
                                                r["reading"], r["page"], r["named_as"].lower()))


def label_of(reading: str) -> str:
    return LABELS.get(reading, reading)


def locator_text(loc: dict) -> str:
    if loc["reading"] in HTML_READINGS:
        return f"{label_of(loc['reading'])} (whole note)"
    return f"{label_of(loc['reading'])} p.{loc['page']}"


# =============================================================================================================
# 2. The launch year, only from what the readings print
# =============================================================================================================

MONTHS = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
BIS_ROW = re.compile(
    r"^\s{1,10}(?P<name>\S.*?)\s{2,}(?P<peg>[A-Za-z]{2,5})\s+(?P<mcap>[\d,]+\.\d+)\s+"
    r"(?P<date>\d{1,2} [A-Z][a-z]{2} \d{4})\s+(?P<obs>\d+)"
    r"(?:\s+(?P<date2>\d{1,2} [A-Z][a-z]{2} \d{4})\s+(?P<obs2>\d+))?\s*$")
BIS_GROUP = re.compile(r"^\s*\(([A-D])\)\s+(.+?)\s*$")
BIS_START = re.compile(r"^\s*Annex 1: Key features of stablecoins in scope\s*$", re.M)
BIS_END = re.compile(r"^\s*Annex 2: Technical annex", re.M)


def iso(date: str) -> str:
    d, m, y = date.split()
    return f"{int(y):04d}-{MONTHS[m]:02d}-{int(d):02d}"


def parse_bis_annex1(pages: list[str]) -> list[dict]:
    """Annex 1's rows: name, peg, group, the first date of CoinGecko's closing price and of CCData's intraday price, the pdf
    page. The market capitalisation (a state at 30 Sep 2023) is read by the pattern and **dropped**."""
    start = next((i for i, p in enumerate(pages) if BIS_START.search(p)), None)
    if start is None:
        return []
    rows, group = [], ""
    for i in range(start, len(pages)):
        if i > start and BIS_END.search(pages[i]):
            break
        for line in pages[i].splitlines():
            g = BIS_GROUP.match(line)
            if g:
                group = f"{g.group(1)} {g.group(2)}"
                continue
            m = BIS_ROW.match(line)
            if m:
                rows.append({"name": m.group("name").strip(), "peg": m.group("peg"), "group": group,
                             "first_date": iso(m.group("date")), "ccdata_first_date": iso(m.group("date2")) if m.group("date2") else "",
                             "page": i + 1})
    return rows


MZ_T1_TITLE = re.compile(r"^\s*Table 1:")
MZ_T1_ROW = re.compile(r"^\s{1,12}(?P<name>\S.*?)\s{2,}(?P<ticker>[A-Za-z0-9]{2,6})\s{2,}(?P<date>\d{4}-\d\d-\d\d)\s")


def parse_mizrach_table1(pages: list[str]) -> list[dict]:
    """Table 1: name, symbol, the date of the first transaction on the Ethereum Mainnet (the market capitalisation is dropped)."""
    rows = []
    for i, page in enumerate(pages):
        lines = page.splitlines()
        for j, line in enumerate(lines):
            if MZ_T1_TITLE.match(line):
                for row in lines[j + 1:j + 20]:
                    m = MZ_T1_ROW.match(row)
                    if m:
                        rows.append({"name": m.group("name").strip(), "ticker": m.group("ticker"),
                                     "first_transaction": m.group("date"), "page": i + 1})
    return rows


# The census prose gives each token's vintage: "the first year that the token transacts on the Mainnet". The passage runs
# from the first anchor to the last; its year anchors are (year, regex).
MZ_START = "DigixDao (DGD) and Xaurum (XAU)"
MZ_END = "In total, of the 65"
MZ_ANCHORS = (
    (2016, r"the 2016 vintage"), (2017, r"in the 2017 vintage"), (2018, r"in the 2018 vintage"),
    (2019, r"2019 was the peak year"), (2020, r"Issuance slowed in 2020"), (2021, r"The 2021 vintage"),
)
# Names as the census prints them, where they differ from the list's name, ticker or merged ids.
MZ_ALIASES = {"TrueUSD": ["True USD"], "Liquity USD": ["Liquidity USD"]}


def census_segments(pages: list[str]) -> tuple[dict[int, str], int] | None:
    """The census passage cut at its year anchors: {year: text}, and the pdf page it starts on."""
    for i, page in enumerate(pages):
        if MZ_START not in G.dehyphenate(page):
            continue                      # the passage starts on this page; the next page only finishes it
        flat = G.dehyphenate(page + "\n" + (pages[i + 1] if i + 1 < len(pages) else ""))
        s = flat.find(MZ_START)
        e = flat.find(MZ_END, s)
        passage = flat[s:e if e >= 0 else len(flat)]
        marks = []
        for year, rx in MZ_ANCHORS:
            m = re.search(rx, passage)
            if m:
                marks.append((m.start(), year))
        marks.sort()
        out = {}
        for k, (pos, year) in enumerate(marks):
            begin = 0 if k == 0 else pos      # the first sentence names its coins before its year
            out[year] = passage[begin:marks[k + 1][0] if k + 1 < len(marks) else len(passage)]
        return out, i + 1
    return None


def census_vintage(coin: dict, segments: dict[int, str]) -> list[int]:
    """The years of the passage's segments in which the coin is named (whole word, case kept). One year is a reading; two
    or more are an ambiguity and are all returned."""
    names = {coin["name"], coin.get("ticker", ""), *merged_ids(coin), *MZ_ALIASES.get(coin["coin_id"], [])}
    names = {n for n in names if len(n) >= 3}
    years = []
    for year, text in segments.items():
        if any(re.search(rf"(?<![A-Za-z0-9]){re.escape(n)}(?![A-Za-z0-9])", text) for n in names):
            years.append(year)
    return sorted(years)


def bis_row_for(coin: dict, rows: list[dict]) -> dict | None:
    """Annex 1's row of a coin: its name as printed, else its ticker (HUSD, sUSD). Case and spaces are not significant."""
    def n(s: str) -> str:
        return re.sub(r"\s+", "", s).lower()
    for key in (coin["name"], coin.get("ticker", "")):
        if key:
            hit = [r for r in rows if n(r["name"]) == n(key)]
            if hit:
                return hit[0]
    return None


def mizrach_t1_for(coin: dict, rows: list[dict]) -> dict | None:
    """Table 1's row of a coin: its symbol as printed."""
    tick = coin.get("ticker", "")
    hit = [r for r in rows if tick and r["ticker"] == tick]
    return hit[0] if hit else None


def year_of(iso_date: str) -> str:
    return iso_date[:4]


def launch_of(coin: dict, bis: list[dict], mz_t1: list[dict], mz_seg: tuple[dict[int, str], int] | None) -> dict:
    """What the readings print of a coin's start. Every printed value is kept, with its reading and page, and none is chosen
    over another. 'not printed' where no reading prints one."""
    entries, out = [], {"bis_first_price_date": "", "bis_ccdata_first_date": "", "bis_group": "", "bis_peg": "",
                        "mizrach_first_transaction": "", "mizrach_vintage": ""}
    b = bis_row_for(coin, bis)
    if b:
        out.update(bis_first_price_date=b["first_date"], bis_ccdata_first_date=b["ccdata_first_date"],
                   bis_group=b["group"], bis_peg=b["peg"])
        entries.append(f"{year_of(b['first_date'])} ({label_of('bis-papers-141')} p.{b['page']}: the first date of a CoinGecko "
                       f"closing price, {b['first_date']}; a first price, not a launch)")
        if b["ccdata_first_date"]:
            entries.append(f"{year_of(b['ccdata_first_date'])} ({label_of('bis-papers-141')} p.{b['page']}: the first date of a "
                           f"CCData intraday price, {b['ccdata_first_date']})")
    t = mizrach_t1_for(coin, mz_t1)
    if t:
        out["mizrach_first_transaction"] = t["first_transaction"]
        entries.append(f"{year_of(t['first_transaction'])} ({label_of('mizrach-arxiv-2201-01392')} p.{t['page']}: Table 1, the first "
                       f"transaction on the Ethereum Mainnet, {t['first_transaction']})")
    if mz_seg:
        segments, page = mz_seg
        years = census_vintage(coin, segments)
        if years:
            out["mizrach_vintage"] = "|".join(str(y) for y in years)
            note = "the vintage year, the first year the token transacts on the Mainnet" + ("; the passage places it under more than one year" if len(years) > 1 else "")
            for y in years:
                entries.append(f"{y} ({label_of('mizrach-arxiv-2201-01392')} p.{page}: {note})")
    out["launch_year_printed"] = " | ".join(entries) if entries else NOT_PRINTED
    return out


# =============================================================================================================
# 3. The packet
# =============================================================================================================

def safe_name(coin_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", coin_id).strip("-")


def sheet_text(row: dict, locs: list[dict]) -> str:
    """One coin's sheet: its identity, its locators, its launch year as printed, and the empty coding table."""
    by_reading: dict[str, list[dict]] = defaultdict(list)
    for loc in locs:
        by_reading[loc["reading"]].append(loc)
    lines = [f"# {row['name']}" + (f" ({row['ticker']})" if row["ticker"] else ""), "",
             f"- coin_id: `{row['coin_id']}`"]
    if row["marks"]:
        lines.append(f"- marks: {row['marks']}")
    if row["merged_ids"]:
        lines.append(f"- also named, in the readings, as: {row['merged_ids'].replace('; ', ', ')} (merged into this coin)")
    lines += ["", "## Where the frozen readings name it", ""]
    for reading, ls in by_reading.items():
        names = sorted({l["named_as"] for l in ls})
        if reading in HTML_READINGS:
            where = "whole note"
        else:
            where = "p." + ", ".join(str(p) for p in sorted({l["page"] for l in ls}))
        lines.append(f"- {label_of(reading)}: {where}; named as {', '.join(repr(n) for n in names)}")
    lines += ["", "## Launch year, as the readings print it", ""]
    if row["launch_year_printed"] == NOT_PRINTED:
        lines.append(NOT_PRINTED)
    else:
        lines += [f"- {e}" for e in row["launch_year_printed"].split(" | ")]
        if row["bis_group"]:
            lines.append(f"- {label_of('bis-papers-141')} Annex 1 prints the coin under '{row['bis_group']}', peg {row['bis_peg']}")
    lines += ["", "## Coding", "",
              "Code each line **yes / no / cannot be read**, with a source and a locator, from the terms (README). "
              "Redemption: note who may redeem (any holder, or verified customers only). One row per line and phase; "
              "add a row for each later phase the terms change at (`phase` = `after-change:<what, as the source prints it>`).",
              "", "| line | phase | code | source | locator | note |", "|---|---|---|---|---|---|"]
    lines += [f"| {ln} | launch | | | | |" for ln in LINES]
    lines += [f"| {ln} | | | | | |" for ln in LINES]
    lines.append("")
    return "\n".join(lines)


def build_rows(coins: list[dict], occurrences: list[dict], bis: list[dict], mz_t1: list[dict],
               mz_seg: tuple[dict[int, str], int] | None) -> list[tuple[dict, list[dict]]]:
    """One (packet row, locators) per coin on the list but the never-issued."""
    out, seen = [], set()
    for coin in coins:
        if not in_the_mapping(coin):
            continue
        if coin["coin_id"] in seen:
            raise ValueError(f"{coin['coin_id']}: twice on the list")
        seen.add(coin["coin_id"])
        locs = locators_of(coin, occurrences)
        if not locs:
            raise ValueError(f"{coin['coin_id']}: no reading names it")
        launch = launch_of(coin, bis, mz_t1, mz_seg)
        row = {"coin_id": coin["coin_id"], "name": coin["name"], "ticker": coin.get("ticker", ""),
               "marks": strip_fate(coin.get("marks", "")), "merged_ids": "; ".join(merged_ids(coin)),
               "readings_naming": "; ".join(label_of(r) for r in dict.fromkeys(l["reading"] for l in locs)),
               "locators": "; ".join(f"{locator_text(l)} as {l['named_as']!r}" for l in locs),
               "sheet": f"{safe_name(coin['coin_id'])}.md", **launch}
        out.append((row, locs))
    names = [r["sheet"].lower() for r, _ in out]
    if len(set(names)) != len(names):
        raise ValueError("two coins share a sheet's file name")
    return out


def refuse_fate(rows: list[tuple[dict, list[dict]]]) -> None:
    """Fail-closed: no word of fate in any row or sheet."""
    for row, locs in rows:
        for text in (*row.values(), sheet_text(row, locs)):
            bad = fate_words(str(text))
            if bad:
                raise ValueError(f"{row['coin_id']}: a word of fate in the packet: {bad}")


def write_packet(rows: list[tuple[dict, list[dict]]], out: Path) -> None:
    refuse_fate(rows)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "packet.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PACKET_FIELDS)
        w.writeheader()
        w.writerows(r for r, _ in rows)
    for row, locs in rows:
        (out / row["sheet"]).write_text(sheet_text(row, locs), encoding="utf-8")


def frozen_reading(key: str):
    return next(r for r in G.READINGS if r.key == key)


def main() -> int:
    coins = read_csv(OUT / "coins.csv")
    occurrences = read_csv(OUT / "coins-draft-occurrences.csv")
    bis_pages = G.pdf_pages(G.frozen_path(frozen_reading("bis-papers-141")))
    mz_pages = G.pdf_pages(G.frozen_path(frozen_reading("mizrach-arxiv-2201-01392")))
    bis, mz_t1, mz_seg = parse_bis_annex1(bis_pages), parse_mizrach_table1(mz_pages), census_segments(mz_pages)
    rows = build_rows(coins, occurrences, bis, mz_t1, mz_seg)
    write_packet(rows, PACKET)
    printed = sum(1 for r, _ in rows if r["launch_year_printed"] != NOT_PRINTED)
    unmatched_bis = [b["name"] for b in bis if not any(bis_row_for(c, [b]) for c in coins if in_the_mapping(c))]
    print(f"{len(coins)} coins on the list, {len(rows)} in the packet "
          f"({len(coins) - len(rows)} out of the mapping), {printed} with a printed launch year, "
          f"{len(rows) - printed} 'not printed'")
    print(f"Annex 1 rows read: {len(bis)}; Mizrach Table 1 rows: {len(mz_t1)}; census passage found: {mz_seg is not None}")
    print(f"Annex 1 rows matched to no coin of the packet: {unmatched_bis}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
