"""FT-001 M7, frame g: the told list of stablecoins (FT-001-M7-frame-g.md section 5, step 3; M0 v4.2 section 2 and section 5 g).

Frame g is **told**: the coins named in a fixed set of frozen readings (the protocol's section 2), drawn here by
script, each name then checked by a person. This module lists names, counts them and merges the spellings of one
coin. It maps nothing, dates no phase, reads no price, and never drops a candidate by judgement: it **marks**, the
person's ``check`` column decides. ``build()`` prints counts only (and every merge); ``build(go=True)`` writes
``data/reconstructed/ft001-g/coins-draft.csv`` (one line per coin, status *to check*) and
``coins-draft-occurrences.csv`` (every candidate as printed, with its reading and page).

Text reader: the system ``pdftotext -layout`` (poppler; ``which pdftotext``), page by page (a form feed ends a PDF
page), falling back to ``pypdf`` (the toolkit's venv has it) where the binary is missing; the three FEDS Notes are
HTML, read by the standard library's ``html.parser`` as one page. Each frozen file's sha256 is checked against its
``MANIFEST.json`` before it is read: a file that does not match is refused, not read.

Readings made in code, in the open, for the audit (the protocol's *readings* are its own):

G1. *The fixed set.* The readings are the protocol's section 2 (:data:`READINGS`), by dataset and vintage. The frozen
    FSB reports and the NY Fed (Anadu et al.) staff report sit under ``data/frame-g/`` too (allowed by Sami's request
    0e6f6355440d, after the protocol was written) but are **not** in the protocol's set; they are listed in
    :data:`OUTSIDE_THE_SET`, never read here. Section 6 widened the set with the three readings Sami's request
    0e6f6355440d made reachable (the NY Fed's SR 1073, the FSB's 2020 and 2023 reports), before the list is drawn.
G2. *Structured lists* (the layout only was inspected): BIS Papers 141's Annex 1 prints one row per coin (name, peg,
    market capitalisation, first date, observations), four groups (A) to (D), over two pages, no ticker. Mizrach's
    Tables 1, 5 and 6 print names (Table 1 and 6 also a symbol); **his census of dead coins is not a table**: it
    is prose ("Name (TICKER)" in two passages, :data:`MIZRACH_REGIONS`), read by the parenthesis pattern, and some
    coins in it print with no ticker (G6).
G3. *Other readings.* A candidate is (a) a printed name or ticker of the structured lists, or of an alias, found in
    the page text (case-sensitive, whole token, at least 3 characters; the longest match first, so ``PAX Gold`` is
    not read as ``PAX``); (b) a capitalised token in "XXX stablecoin", "XXX algorithmic stablecoin" (up to three
    lower-case words between), "stablecoin XXX" or "stablecoins (X and Y)". A token is kept when, once the
    sentence-starting words (:data:`LEADING_WORDS`) are stripped, it has two capital letters or more and is not a
    bare currency (:data:`CURRENCY_ONLY`); a token made only of an institution's or a method's acronym
    (:data:`NON_COIN_WORDS`: BIS, MMF, SVB, ...) is **set aside and listed by name in the report**, never silently
    dropped; a parenthesis holding a digit (a citation) is not a list of coins. So a single capitalised word that no list names ("stablecoin Neutrino")
    is **not** found: said, and left to the person's check.
G4. *Terra, UST, TerraUSD, USTC and LUNA are out of the mapping* (M0; the dossier; protocol section 2), cited from
    Liu, Makarov and Schoar and Uhlig. They are **kept in the draft, marked** ``excluded`` with that reason, never
    silently absent, so the person sees what the readings name. :data:`TERRA`.
G5. *A governance token is not a stablecoin* (the protocol's *reading*) is **not decided by script**. A candidate
    whose context (120 characters each side) holds "governance token" is marked ``governance?``; nothing is
    dropped. A coin printed in a table carries no such mark: the person reads it.
G6. *What the script cannot find, said.* Coins that print in a reading with no ticker, no parenthesis and no
    "stablecoin" beside them (Mizrach's "Italian Lira", "Ampleforth", "Carbon", "Reserve", "Huobi"; the Examples
    column of IFDP 1334's table of mechanisms) are not found by the patterns; the coverage counts what it found,
    the person's check adds what it misses, by hand, with the reading and page.
G7. *Dedup* by the normalised name or ticker (lower case, letters and digits only), through a union of the strings
    that :data:`ALIASES` joins (each with its reason) and of a name and ticker **printed together** in one
    candidate. Every merge of two differently spelled strings is printed with its reason. Strings that look alike
    but are not merged are in :data:`NOT_MERGED`, printed too.
G8. *Pages* are PDF page numbers (the first page of the file is 1), not the printed folios; an HTML note is page 1.
"""

from __future__ import annotations

import csv
import hashlib
import html.parser
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DATA = ROOT / "data"
FROZEN = DATA / "frame-g"
OUT = DATA / "reconstructed" / "ft001-g"
VINTAGE = "2026-10-01"
EXPECTED_BIS_ROWS = 68          # the protocol's section 2: "68 coins, survivors"
MIN_NAME_LEN = 3                # G3: a printed name or ticker shorter than this is not searched for in prose
CONTEXT = 120                   # G5

FIELDS = ["coin_id", "name", "ticker", "readings", "pages", "how_found", "marks", "excluded", "status", "check"]
OCC_FIELDS = ["coin_id", "name_as_printed", "ticker_as_printed", "reading", "page", "how_found", "marks"]


@dataclass(frozen=True)
class Reading:
    key: str           # the dataset directory under data/frame-g/
    kind: str          # "pdf" or "html"
    label: str
    structured: str = ""    # "bis-annex1" or "mizrach": has a table parsed (G2)


READINGS: tuple[Reading, ...] = (
    Reading("bis-papers-141", "pdf", "Kosse, Glowka, Mattei, Rice, BIS Papers 141 (2023)", "bis-annex1"),
    Reading("mizrach-arxiv-2201-01392", "pdf", "Mizrach, arXiv 2201.01392", "mizrach"),
    Reading("bis-wp-1164", "pdf", "Ahmed, Aldasoro, Duley, BIS WP 1164"),
    Reading("bis-wp-1146", "pdf", "Aldasoro, Mehrling, Neilson, BIS WP 1146"),
    Reading("bis-wp-1219", "pdf", "Aldasoro et al., BIS WP 1219"),
    Reading("bis-wp-1270", "pdf", "Ahmed, Aldasoro, BIS WP 1270"),
    Reading("fed-ifdp-1334", "pdf", "Liao, Caramichael, Fed IFDP 1334"),
    Reading("feds-notes-stable-in-stablecoins", "html", "FEDS Notes, The stable in stablecoins (2022)"),
    Reading("feds-notes-primary-secondary", "html", "FEDS Notes, Primary and secondary markets (2024)"),
    Reading("feds-notes-shadow-bank-runs", "html", "FEDS Notes, In the shadow of bank runs (2025)"),
    Reading("nber-w30796", "pdf", "Gorton, Klee, Ross, Ross, Vardoulakis, NBER w30796"),
    Reading("nber-w27136", "pdf", "Lyons, Viswanath-Natraj, NBER w27136"),
    Reading("nber-w31160", "pdf", "Liu, Makarov, Schoar, NBER w31160"),
    Reading("nber-w30256", "pdf", "Uhlig, NBER w30256"),
    # section 6, G1: the set widened before the list is drawn (request 0e6f6355440d opened the two hosts)
    Reading("nyfed-anadu-runs", "pdf", "Anadu, Azar, Cipriani, Eisenbach, Huang, Landoni, La Spada, Macchiavelli, Malfroy-Camine, Wang, NY Fed SR 1073"),
    Reading("fsb-2020-global-stablecoins", "pdf", "FSB, Global stablecoin arrangements, final report (2020)"),
    Reading("fsb-2023-crypto-stablecoins", "pdf", "FSB, Global stablecoin arrangements, high-level recommendations (2023)"),
)
OUTSIDE_THE_SET: tuple[str, ...] = ()   # G1 as amended in section 6: nothing frozen is left out

# --- G4: Terra out ---------------------------------------------------------------------------------------------
TERRA_REASON = "Terra/UST out of the mapping (M0 section 5 g; protocol section 2); cited from Liu-Makarov-Schoar and Uhlig"
TERRA = ("Terra", "TerraUSD", "Terra USD", "Terra UST", "TerraClassicUSD", "Terra Classic USD", "UST", "USTC", "LUNA", "Luna")

# --- G7: aliases, each with its reason ------------------------------------------------------------------------
ALIASES: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("Tether", ("Tether", "Tether USD", "USD Tether", "USDT"),
     "USDT is Tether's ticker; Mizrach's Table 1 prints 'Tether USD' with USDT, BIS Annex 1 'Tether'; 'USD Tether' is a reading's reversed spelling. "
     "Euro Tether, CNH Tether and Tether Gold are other coins and stay apart"),
    ("USD Coin", ("USD Coin", "USDC"), "USDC is the ticker of USD Coin (Mizrach Table 1 prints both)"),
    ("Binance USD", ("Binance USD", "BUSD"), "BUSD is the ticker of Binance USD (Mizrach Table 1 prints both)"),
    ("Dai", ("Dai", "DAI", "Dai Stablecoin"), "Mizrach's Table 1 prints 'Dai Stablecoin' with symbol DAI; BIS Annex 1 'Dai'"),
    ("TrueUSD", ("TrueUSD", "True USD", "TUSD"), "TUSD is the ticker of TrueUSD (Mizrach Table 1); 'True USD' is Mizrach's prose spelling"),
    ("Pax Dollar", ("Pax Dollar", "Paxos Standard", "USDP", "PAX"),
     "Paxos Standard was rebranded Pax Dollar (USDP) on 24 Aug 2021 (Mizrach); PAX was the old ticker "
     "(Table 1). BIS Annex 1's separate row 'USDP Stablecoin' is NOT merged (NOT_MERGED)"),
    ("Gemini Dollar", ("Gemini Dollar", "GUSD"), "GUSD is the ticker of Gemini Dollar (Mizrach Table 1 prints both)"),
    ("Huobi USD", ("HUSD", "Huobi USD"), "HUSD is the ticker of Huobi USD (Mizrach Tables 1 and 5)"),
    ("Synthetix USD", ("sUSD", "Synth sUSD", "Synthetix USD"), "sUSD is Synthetix's stablecoin; Mizrach Table 1 prints 'Synth sUSD'"),
    ("Liquity USD", ("Liquity USD", "LUSD", "Liquidity USD"),
     "LUSD is the ticker of Liquity USD; Mizrach's prose spells it 'Liquidity USD (LUSD)', same ticker printed with it"),
    ("Fei USD", ("Fei USD", "Fei", "FEI"), "Fei USD (BIS Annex 1; Mizrach 'Fei USD (Fei)'); FEI is its ticker"),
    ("Magic Internet Money", ("Magic Internet Money", "MIM"), "MIM is the ticker of Magic Internet Money"),
    ("Neutrino USD", ("Neutrino USD", "USDN"), "USDN is the ticker of Neutrino USD"),
)
NOT_MERGED: tuple[tuple[str, str, str], ...] = (
    ("USDP Stablecoin", "Pax Dollar",
     "two rows of BIS Annex 1 (a separate coin there); the ticker USDP of Pax Dollar is printed by Mizrach, not by BIS"),
    ("Basis Cash", "Basis",
     "BIS Annex 1 lists Basis Cash (first price Nov 2020); Mizrach and IFDP 1334 name Basis, the earlier failed project; "
     "left apart for the person's check"),
    ("PAX Gold", "PAX", "a commodity-backed coin (BIS Annex 1), not Paxos Standard"),
    ("Tether Gold / Euro Tether / CNH Tether", "Tether", "other BIS Annex 1 rows"),
)

# --- G3: pattern constants -------------------------------------------------------------------------------------
LEADING_WORDS = frozenset({
    "The", "A", "An", "If", "For", "Are", "Is", "Because", "As", "Can", "While", "With", "When", "One", "But", "Then",
    "Only", "In", "Of", "On", "At", "By", "To", "And", "Or", "Such", "These", "This", "That", "Those", "Other",
    "Most", "Some", "Each", "Any", "All", "Many", "Both", "Whether", "Regarding", "Starting", "It", "Its",
    "Panel", "Table", "Figure", "Fig", "Appendix", "Note", "Notes", "See", "Source", "Sources", "Also", "Since",
})
NON_COIN_WORDS = frozenset({       # institutions' and methods' acronyms and words that sit beside "stablecoin"; set aside, listed
    "BIS", "HFT", "MMF", "MMFs", "PSMs", "PSM", "SVB", "HHI", "OLS", "IV", "SC", "TFL", "CCData", "DeFi", "MCt",
    "Ethereum", "Mainnet", "Fed", "FOMC", "SEC", "FSB", "IMF", "ECB", "CFTC", "OCC", "FDIC", "NBER", "DEX", "CEX",
    "AMM", "GDP", "ETF", "ERC", "CBDC", "CBDCs", "II", "III", "IRF",
})
CURRENCY_ONLY = frozenset({"USD", "US", "EUR", "GBP", "JPY", "CNH", "SGD", "TRY", "IDR", "U.S", "UK", "EU", "USA", "ETH", "BTC"})

GOVERNANCE = re.compile(r"governance\s+tokens?", re.I)

# --- G2: Mizrach's prose census (regions of a page where "Name (TICKER)" is the pattern) -----------------------
# start/end are searched in the page text after line breaks and hyphenation are undone; "^" starts at the top of
# the page (the paragraph begins on the page before its first coin); both markers must be on the page.
MIZRACH_REGIONS: tuple[tuple[str, str, str], ...] = (
    (r"^", r"In total, of the 65", "survivorship paragraph (the vintages; from the top of its page)"),
    (r"prominent failures", r"call into question", "algorithmic coins that failed"),
)


@dataclass
class Cand:
    name: str
    ticker: str
    reading: str
    page: int
    how: str
    marks: tuple[str, ...] = ()


# =============================================================================================================
# 1. The text readers
# =============================================================================================================

def frozen_path(reading: Reading) -> Path:
    """The frozen file of a reading, named by its ``MANIFEST.json``; refused if its sha256 does not match."""
    folder = FROZEN / reading.key / VINTAGE
    manifest = json.loads((folder / "MANIFEST.json").read_text())
    files = manifest["files"]
    if len(files) != 1:
        raise ValueError(f"{reading.key}: expected one frozen file, the manifest names {len(files)}")
    path = folder / files[0]["name"]
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != files[0]["sha256"]:
        raise ValueError(f"{reading.key}: {path.name} does not match its manifest's sha256")
    return path


def split_pages(text: str) -> list[str]:
    """pdftotext's form feeds end a page; a trailing empty piece is not a page."""
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def pdf_pages(path: Path) -> list[str]:
    """Page-numbered text of a PDF: ``pdftotext -layout`` where installed, else pypdf (G reader)."""
    exe = shutil.which("pdftotext")
    if exe:
        out = subprocess.run([exe, "-layout", str(path), "-"], capture_output=True, check=True)
        return split_pages(out.stdout.decode("utf-8", "replace"))
    from pypdf import PdfReader       # the toolkit's interpreter has it
    return [(p.extract_text(extraction_mode="layout") or "") for p in PdfReader(str(path)).pages]


class _Text(html.parser.HTMLParser):
    SKIP = {"script", "style", "nav", "header", "footer", "noscript", "svg"}
    BLOCK = {"p", "div", "li", "br", "tr", "h1", "h2", "h3", "h4", "h5", "table", "section", "article", "td", "th"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def html_pages(raw: str) -> list[str]:
    """An HTML note as one page of text."""
    p = _Text()
    p.feed(raw)
    return ["".join(p.parts)]


def read_pages(reading: Reading) -> list[str]:
    path = frozen_path(reading)
    if reading.kind == "pdf":
        return pdf_pages(path)
    return html_pages(path.read_text(encoding="utf-8", errors="replace"))


# =============================================================================================================
# 2. The structured lists
# =============================================================================================================

BIS_CATEGORY = re.compile(r"^\s*\(([A-D])\)\s+(.+?)\s*$")
BIS_ROW = re.compile(r"^\s{1,10}(?P<name>\S.*?)\s{2,}(?P<peg>[A-Za-z]{2,5})\s+(?P<mcap>[\d,]+\.\d+)\s+"
                     r"(?P<date>\d{1,2} [A-Z][a-z]{2} \d{4})\s+(?P<obs>\d+)\b")
BIS_START = re.compile(r"^\s*Annex 1: Key features of stablecoins in scope\s*$", re.M)
BIS_END = re.compile(r"^\s*Annex 2: Technical annex", re.M)


def parse_bis_annex1(pages: list[str], reading: str = "bis-papers-141") -> list[Cand]:
    """Annex 1's table: one candidate per row (name as printed, no ticker), the group (A)-(D) and the peg in the marks."""
    out: list[Cand] = []
    start = next((i for i, p in enumerate(pages) if BIS_START.search(p)), None)
    if start is None:
        return out
    group = ""
    for i in range(start, len(pages)):
        if i > start and BIS_END.search(pages[i]):
            break
        for line in pages[i].splitlines():
            g = BIS_CATEGORY.match(line)
            if g:
                group = f"{g.group(1)} {g.group(2)}"
                continue
            m = BIS_ROW.match(line)
            if m:
                out.append(Cand(m.group("name").strip(), "", reading, i + 1, "table",
                                (f"group {group}", f"peg {m.group('peg')}")))
    return out


MZ_TITLE = re.compile(r"^\s*Table (\d+):")
MZ_ROWS = {
    # Table 1: name, symbol, first transaction (a date), collateral, market cap
    1: re.compile(r"^\s{1,12}(?P<name>\S.*?)\s{2,}(?P<ticker>[A-Za-z0-9]{2,6})\s{2,}\d{4}-\d\d-\d\d\s"),
    # Table 5: name, a dollar volume, a count
    5: re.compile(r"^\s{1,20}(?P<name>[A-Za-z][^$]*?)\s{2,}\$[\d,.]+\s+[\d,.]+\s*$"),
    # Table 6: name, symbol, a count, a volume
    6: re.compile(r"^\s{1,12}(?P<name>\S.*?)\s{2,}(?P<ticker>[A-Z0-9]{2,6})\s+[\d,]+\s+[\d.]+\s*$"),
}
MZ_WINDOW = 22     # lines after a table's title in which its rows are read


def parse_mizrach_tables(pages: list[str], reading: str = "mizrach-arxiv-2201-01392") -> list[Cand]:
    """Tables 1, 5 and 6: the coins as printed, with the symbol where the table prints one."""
    out: list[Cand] = []
    for i, page in enumerate(pages):
        lines = page.splitlines()
        for j, line in enumerate(lines):
            t = MZ_TITLE.match(line)
            if not t or int(t.group(1)) not in MZ_ROWS:
                continue
            rx = MZ_ROWS[int(t.group(1))]
            for row in lines[j + 1:j + 1 + MZ_WINDOW]:
                m = rx.match(row)
                if m:
                    ticker = m.groupdict().get("ticker") or ""
                    out.append(Cand(m.group("name").strip(), ticker, reading, i + 1, "table",
                                    (f"table {t.group(1)}",)))
    return out


PAREN = re.compile(r"((?:[A-Z][A-Za-z0-9]*)(?:\s[A-Z][A-Za-z0-9]*){0,2})\s+\(([A-Za-z0-9]{2,6})\)")


def dehyphenate(text: str) -> str:
    """Line breaks undone (a hyphen at a line's end joins the word), whitespace collapsed."""
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    return re.sub(r"\s+", " ", text)


def line_flat(text: str) -> str:
    """For the patterns: hyphenation undone, a run of spaces (a column gap) kept as one tab and a line break as one
    newline, so that a token (single spaces only) never runs across a column or a line."""
    text = re.sub(r"(\w)-[ \t]*\n[ \t]*(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]{2,}", "\t", text)
    return re.sub(r"[ \t]*\n\s*", "\n", text)


def parse_mizrach_census(pages: list[str], reading: str = "mizrach-arxiv-2201-01392") -> list[Cand]:
    """Mizrach's census of dead coins is prose: 'Name (TICKER)' inside the two regions, G2."""
    out: list[Cand] = []
    for i, page in enumerate(pages):
        flat = dehyphenate(page)
        for start, end, label in MIZRACH_REGIONS:
            s = re.search(start, flat)
            if not s:
                continue
            e = re.search(end, flat[s.start():])
            if end and not e:          # a region is the text between its two markers, both on the page
                continue
            region = flat[s.start():s.start() + e.start()]
            for m in PAREN.finditer(region):
                name = strip_leading(m.group(1))
                if name:
                    out.append(Cand(name, m.group(2), reading, i + 1, "census", (label,)))
    return out


# =============================================================================================================
# 3. Names, aliases, patterns
# =============================================================================================================

def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def strip_leading(tok: str) -> str:
    words = tok.split()
    while words and words[0] in LEADING_WORDS:
        words.pop(0)
    return " ".join(words)


def coin_like(tok: str) -> str:
    """The token's name once the sentence-starting words are stripped, or '' (G3): two capital letters or more,
    and not a bare currency."""
    words = strip_leading(tok).split()
    while words and words[-1] in LEADING_WORDS:       # a sentence's next word ("... Channel The")
        words.pop()
    name = " ".join(words)
    if not name or name in CURRENCY_ONLY:
        return ""
    return name if sum(1 for c in name if c.isupper()) >= 2 else ""


TOK = r"[A-Z][A-Za-z0-9]*(?:[ ][A-Z][A-Za-z0-9]*){0,2}"        # single spaces only: never across a column or a line
P_BEFORE = re.compile(rf"(?<![A-Za-z0-9])({TOK})((?:\s+[a-z][a-z-]*){{0,3}})\s+stable\s?coins?\b")
P_AFTER = re.compile(rf"\bstable\s?coins?[ ]+({TOK})")
P_PAREN = re.compile(r"\bstable\s?coins?\s*\(([^()]{2,80})\)")


def pattern_candidates(page_text: str, reading: str, page: int,
                       set_aside: Counter | None = None) -> list[Cand]:
    """G3 (b): 'XXX stablecoin', 'XXX algorithmic stablecoin', 'stablecoin XXX', 'stablecoins (X and Y)'.

    A token made only of :data:`NON_COIN_WORDS` (an institution's or a method's acronym) is counted in ``set_aside``
    and reported by name, never silently dropped."""
    flat = line_flat(page_text)
    out: list[Cand] = []

    def add(raw: str, how: str, span: tuple[int, int]) -> None:
        name = coin_like(raw)
        if not name:
            return
        if all(w in NON_COIN_WORDS for w in name.split()):
            if set_aside is not None:
                set_aside[name] += 1
            return
        out.append(Cand(name, "", reading, page, how, marks_for(flat, *span)))

    for m in P_BEFORE.finditer(flat):
        add(m.group(1), "pattern: XXX stablecoin", m.span(1))
    for m in P_AFTER.finditer(flat):
        add(m.group(1), "pattern: stablecoin XXX", m.span(1))
    for m in P_PAREN.finditer(flat):
        if re.search(r"\d", m.group(1)):            # a citation ("Author 2020"), not a list of coins
            continue
        inner = re.sub(r"\b(e\.g\.|i\.e\.|such as|including)\b,?", "", m.group(1))
        for part in re.split(r",|;|\band\b|\bor\b", inner):
            part = part.strip()
            if re.fullmatch(r"[A-Z][A-Za-z0-9]*(?: [A-Z][A-Za-z0-9]*){0,2}", part) and part not in CURRENCY_ONLY:
                if part in NON_COIN_WORDS:
                    if set_aside is not None:
                        set_aside[part] += 1
                    continue
                out.append(Cand(part, "", reading, page, "pattern: stablecoins (X and Y)", marks_for(flat, *m.span(1))))
    return out


def marks_for(flat: str, start: int, end: int) -> tuple[str, ...]:
    """G5: marked, never dropped."""
    ctx = flat[max(0, start - CONTEXT):end + CONTEXT]
    return ("governance?",) if GOVERNANCE.search(ctx) else ()


def search_terms(structured: list[Cand]) -> list[str]:
    """The strings looked for in the other pages: every printed name and ticker of the structured lists and of the
    aliases and of Terra (G3 a), at least MIN_NAME_LEN characters."""
    terms = set()
    for c in structured:
        terms.update(s for s in (c.name, c.ticker) if s)
    for _, members, _ in ALIASES:
        terms.update(members)
    terms.update(TERRA)
    return sorted((t for t in terms if len(norm(t)) >= MIN_NAME_LEN), key=lambda t: (-len(t), t))


def name_matches(page_text: str, terms: list[str], reading: str, page: int,
                 skip: frozenset = frozenset()) -> list[Cand]:
    """G3 (a): the terms found as whole case-sensitive tokens in the page, the longest first; a shorter term inside the
    span of a longer one is not counted. ``skip``: (reading, page, term) already read from a table of that page."""
    flat = dehyphenate(page_text)
    taken: list[tuple[int, int]] = []
    out: list[Cand] = []
    for t in terms:
        if (reading, page, t) in skip:
            continue
        rx = re.compile(r"(?<![A-Za-z0-9])" + r"\s+".join(re.escape(w) for w in t.split()) + r"(?![A-Za-z0-9])")
        for m in rx.finditer(flat):
            if any(m.start() < b and a < m.end() for a, b in taken):
                continue
            taken.append(m.span())
            out.append(Cand(t, "", reading, page, "name match", marks_for(flat, *m.span())))
    return out


# =============================================================================================================
# 4. Dedup, the Terra exclusion
# =============================================================================================================

class Union:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def join(self, a: str, b: str) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[max(ra, rb)] = min(ra, rb)
        return True


def terra_keys() -> set[str]:
    return {norm(t) for t in TERRA}


def dedup(cands: list[Cand]) -> tuple[dict[str, list[Cand]], list[str]]:
    """Group the candidates into coins; return {coin_id: candidates} and the printed merges (G7).

    A coin's id is the canonical alias name where an alias group holds it, else the first-seen name (as printed)."""
    uf, merges = Union(), []
    spell: dict[str, set[str]] = defaultdict(set)         # normalised -> spellings as printed
    for canon, members, reason in ALIASES:
        keys = [norm(m) for m in members]
        for m, k in zip(members, keys):
            spell[k].add(m)
        if any([uf.join(keys[0], k) for k in keys[1:]]):
            merges.append(f"alias {canon}: {', '.join(members)} - {reason}")
    terra = terra_keys()
    tk = sorted(terra)
    for k in tk[1:]:
        uf.join(tk[0], k)
    merges.append(f"alias Terra: {', '.join(TERRA)} - {TERRA_REASON}")
    for c in cands:
        nk = norm(c.name)
        spell[nk].add(c.name)
        if c.ticker:
            tkk = norm(c.ticker)
            spell[tkk].add(c.ticker)
            if nk != tkk and uf.join(nk, tkk):
                merges.append(f"printed together: '{c.name}' and '{c.ticker}' ({c.reading} p.{c.page}, {c.how})")
    # a spelling that differs only by case or punctuation from another, printed once
    for k, forms in sorted(spell.items()):
        if len(forms) > 1 and not any(k == norm(m) for _, ms, _ in ALIASES for m in ms) and k not in terra:
            merges.append(f"normalised: {' / '.join(sorted(forms))} -> {k}")
    canon_of = {}
    for canon, members, _ in ALIASES:
        canon_of[uf.find(norm(members[0]))] = canon
    canon_of[uf.find(tk[0])] = "Terra"
    groups: dict[str, list[Cand]] = defaultdict(list)
    first_name: dict[str, str] = {}
    for c in cands:
        root = uf.find(norm(c.name))
        groups[root].append(c)
        first_name.setdefault(root, c.name)
    coins = {canon_of.get(root, first_name[root]): cs for root, cs in groups.items()}
    return coins, merges


def is_excluded(cs: list[Cand]) -> bool:
    terra = terra_keys()
    return any(norm(c.name) in terra or (c.ticker and norm(c.ticker) in terra) for c in cs)


# =============================================================================================================
# 5. The draft, the coverage, the build
# =============================================================================================================

def collect(readings: tuple[Reading, ...] = READINGS, pages_of=None) -> tuple[list[Cand], dict]:
    """Every candidate of every reading, and the per-reading counts. ``pages_of`` is a hook for tests."""
    pages_of = pages_of or read_pages
    texts = {r.key: pages_of(r) for r in readings}
    cands: list[Cand] = []
    structured: list[Cand] = []
    for r in readings:
        if r.structured == "bis-annex1":
            structured += parse_bis_annex1(texts[r.key], r.key)
        elif r.structured == "mizrach":
            structured += parse_mizrach_tables(texts[r.key], r.key) + parse_mizrach_census(texts[r.key], r.key)
    cands += structured
    terms = search_terms(structured)
    skip = frozenset((c.reading, c.page, c.name) for c in structured if c.how == "table")
    set_aside: Counter = Counter()
    for r in readings:
        for i, page in enumerate(texts[r.key]):
            cands += name_matches(page, terms, r.key, i + 1, skip)
            cands += pattern_candidates(page, r.key, i + 1, set_aside)
    counts = {"pages": {r.key: len(texts[r.key]) for r in readings},
              "structured_rows": Counter(f"{c.reading}: {c.how}" for c in structured),
              "set_aside": set_aside}
    return cands, counts


def coverage(cands: list[Cand], coins: dict[str, list[Cand]], counts: dict) -> dict:
    """Counts only (names appear in the merges, which the protocol asks to print)."""
    by = Counter((c.reading, c.how.split(":")[0]) for c in cands)
    table = Counter(c.reading for c in cands if c.how == "table")
    return {
        "pages_read": counts["pages"],
        "structured_rows_parsed": dict(counts["structured_rows"]),
        "bis_annex1_rows": table.get("bis-papers-141", 0),
        "bis_annex1_rows_expected": EXPECTED_BIS_ROWS,
        "bis_annex1_ok": table.get("bis-papers-141", 0) == EXPECTED_BIS_ROWS,
        "pattern_tokens_set_aside": dict(counts.get("set_aside", {})),
        "candidates": len(cands),
        "by_reading_and_how": {f"{r} | {h}": n for (r, h), n in sorted(by.items())},
        "coins_after_dedup": len(coins),
        "coins_excluded_terra": sum(1 for cs in coins.values() if is_excluded(cs)),
        "coins_marked_governance": sum(1 for cs in coins.values()
                                       if any("governance?" in c.marks for c in cs)),
        "coins_named_in_one_reading_only": sum(1 for cs in coins.values() if len({c.reading for c in cs}) == 1),
        "coins_named_in_two_or_more_readings": sum(1 for cs in coins.values() if len({c.reading for c in cs}) > 1),
    }


def coin_rows(coins: dict[str, list[Cand]]) -> list[dict]:
    rows = []
    for coin_id, cs in sorted(coins.items(), key=lambda kv: kv[0].lower()):
        order = {r.key: i for i, r in enumerate(READINGS)}
        cs = sorted(cs, key=lambda c: (c.how != "table", order.get(c.reading, 99), c.page))
        tickers = sorted({c.ticker for c in cs if c.ticker})
        marks = sorted({m for c in cs for m in c.marks if m == "governance?"})
        rows.append({
            "coin_id": coin_id,
            "name": cs[0].name,
            "ticker": "; ".join(tickers),
            "readings": "; ".join(sorted({c.reading for c in cs}, key=lambda k: order.get(k, 99))),
            "pages": "; ".join(sorted({f"{c.reading} p.{c.page}" for c in cs})),
            "how_found": "; ".join(sorted({c.how for c in cs})),
            "marks": "; ".join(marks),
            "excluded": TERRA_REASON if is_excluded(cs) else "",
            "status": "to check",
            "check": "",
        })
    return rows


def occurrence_rows(coins: dict[str, list[Cand]]) -> list[dict]:
    rows = []
    for coin_id, cs in coins.items():
        for c in cs:
            rows.append({"coin_id": coin_id, "name_as_printed": c.name, "ticker_as_printed": c.ticker,
                         "reading": c.reading, "page": c.page, "how_found": c.how, "marks": "; ".join(c.marks)})
    return sorted(rows, key=lambda r: (r["coin_id"].lower(), r["reading"], r["page"], r["how_found"]))


def write(path: Path, rows: list[dict], fields: list[str]) -> None:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def build(go: bool = False) -> dict:
    cands, counts = collect()
    coins, merges = dedup(cands)
    report = {"coverage": coverage(cands, coins, counts), "merges": merges,
              "not_merged": [f"{a} | {b}: {why}" for a, b, why in NOT_MERGED],
              "outside_the_set_not_read": list(OUTSIDE_THE_SET)}
    if not go:
        return report
    OUT.mkdir(parents=True, exist_ok=True)
    write(OUT / "coins-draft.csv", coin_rows(coins), FIELDS)
    write(OUT / "coins-draft-occurrences.csv", occurrence_rows(coins), OCC_FIELDS)
    report["written"] = ["coins-draft.csv", "coins-draft-occurrences.csv"]
    return report


def main(argv: list[str]) -> int:
    if argv[:1] == ["build"]:
        print(json.dumps(build(go="--go" in argv), indent=1, default=str))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
