"""FT-001 M3, frame k: flee or stay (claim 3, told) (FT-001-M3-frame-k.md; M0 v4.2 section 5 k and section 6, claim 3).

The rules, on plain per-year readings, tested on synthetic series (``test_frame_k.py``) before any real series was read;
then the build of ``data/reconstructed/ft001-k/`` (``frame_k.py build [--go]``). ``build()`` prints the coverage only
(the entries by year and status, the cells and their reasons, the sources' coverage per measure): no measure is
computed or printed. ``build(go=True)`` writes ``series.csv`` (one case line per entry), ``shown.csv`` (the told table),
``shown-variants.csv`` and ``variant-<name>.csv``. The session writes the manifest.

Claim 3 is **told**: this module shows, it never concludes. No margin, no test, no verdict.

**The barrier**: the entry and the cell are functions of the deposit rate, pi, the freezes, ka_open and the borders only
(``entries``, ``cell_at``); no holding (currency, balance-of-payments flow) is an argument of either. A test draws
holdings independently of cells and checks that no entry and no cell moves.

Readings made in code, in the open, for the audit (the protocol's *readings* are its own):

K1. *A cell that changed.* The cell is read at the entry year t and at t - 1 (annual sources), each as open, closed, or
    *cannot be read*. Both read and different: **changed** (status *apart*, the reason written). Both read and equal:
    that cell. A cell unread at either end is *cannot be read* (the reason names the end): "as they stood at entry and
    for at least 12 months before it" cannot be said of a cell read at one end only.
K2. *Censored.* An entry is censored when t + W is past the last year of every measure's data (``ends``, the panel-level
    last year each measure is read: ``panel.common_end`` of its own years). A measure whose own end falls inside the
    window while the other's does not is unread for that entry (not censored). A money whose series stops early is
    *cannot be read*, never censored (M0 section 4).
K3. *The spacing.* The scan is by year; a year is an entry if the N years ending in it are below the line and no entry of
    the money lies in the W years before it. The run need not be fresh: a money below the line for ten years has an entry
    every W + 1 years.
K4. *The freezes.* Laeven and Valencia's deposit freezes are on the sheet ``Resolution Details`` (Table A2, "Deposit
    Freeze", a date and a duration in months), **not** on "Crisis Resolution and Outcomes", where the protocol names it
    (that sheet has no freeze column). A freeze covers the years from its start year to the year of start + duration,
    inclusive. Its date is an Excel serial or a bare year; Lebanon's is text ("17-Oct-") with the year on the next row.
    A freeze year is an unread year for the return (it breaks a run). *The window* held for an entry is t + 1 ... t + W.
    An entry whose window holds a freeze year is dated all the same (it takes its place in the spacing) and its line is
    *cannot be read*: the freeze is a later event, not a holding, and it does not decide the entry.
K5. *Before 1970.* A run may begin before 1970; no entry is dated before it, and a run before 1970 occupies no window.
K6. *Cells.* ``Forced`` is ka_open at or below the line (a float tolerance of 1e-9), in the year read. A forced money is
    *closed*, whatever its neighbours. Not forced: a land border (Direct Contiguity type 1, either direction) with an
    economy whose legal tender is the dollar or the euro in the year is *open*; else *cannot be read* (the protocol's
    reading). A year without ka_open is *cannot be read*, whatever the border.
K7. *The foreign legal tender of a neighbour*: the economy is in the ``DOLLAR_EURO`` table (K17) in the year itself (not the
    class twelve months before: that is the regime at a date; this is a cell). **The United States, the dollar's own
    issuer, is read as a dollar economy** (section 9: M0's "an economy whose legal tender is the dollar" includes it, as the
    euro's members are included); the variant ``class1-only`` (``Spec.us_issuer`` off) reads class 1 and the euro's members
    only.
K8. *After a source's end* (section 11, B1). The regime has three sources, each read to **its own last year**, found in the
    data: contiguity (2016), the classification's classes (2016) and the classification's anchors (**2015**: the anchor file
    has no 2016 row). After its last year each is carried **from that year** (the anchors from 2015, never from 2016), and
    a cell read through a carried year is flagged ``regime_carried``: the border read after the contiguity's end, or a
    neighbour read (as dollar or euro, or as not) after the earlier of the classes' and the anchors' ends. A forced cell
    reads ka_open alone and carries nothing. After 2023 ka_open cannot be read. Variant ``no-carry`` (``Spec.carry`` off):
    no year after a source's end is read (the border, or a neighbour's class and anchor, is unread there). Zimbabwe's own
    money returns in 2019, which the carry cannot see: said.
K9. *m1c.* Delta log of the real currency from t to t + W (FDSBC, then 14A before a money's first survey reading, as the
    phases list; deflated by IFS PCPI_IX; the phases list's units-glitch screen drops its glitch years). Every year of the
    span read must come from one source (``seam`` otherwise). *Net*: that change less the change from t - W to t, on the
    same terms (a seam in either span leaves the net unread, flagged ``seam``).
K10. *m2.* The year's outflow is BFDA + BFPA + BFOA less net errors and omissions (section 9: derivatives, BFFA, only in
    the variant ``with-derivatives``) (the sign reversed: a negative balance is an unrecorded outflow and adds; the variant
    ``neo-negative-only``, section 11 M4, adds only a negative balance). All parts must be read in the year. The sum over
    t + 1 ... t + W, over the **entry year's** dollar GDP (K19, K20), times 100. *Net*: that sum less the same sum over
    t - W + 1 ... t, on the same denominator.
K11. *Statuses, in this order* (section 11): a money that is not its own (K18) is *apart*; a freeze in the window, an
    unread cell, or a war year at entry that cannot be read is *cannot be read*; a war year at entry (K15) or a changed cell
    is *apart*; the variant ``war-in-window-apart`` sets apart a war year in t ... t + W; censored (K2) is *censored* (M0's
    status; the protocol's "apart"); neither measure read (the net ones, in the variant ``net``) is *cannot be read*; else
    *counted*. Where two apply, the first in this order is the status and the reason writes it; ``censored`` and
    ``freeze_in_window`` stay in their own columns.
K12. *The strata.* The depth at the entry year is ``(-10,-5]``, ``(-20,-10]``, ``<=-20``; a return above -5 (the variants
    ``line-0``) is ``above -5``, a stratum of its own. pi at the entry year: below 20, 20-40 (20 inclusive), 40 or more.
    ``shown.csv`` adds a row set ``all`` (every counted entry), the same cells and the same n.
K13. *War in the window.* ``war_in_window`` is flagged when a war year (``panel.war_at``) falls in t ... t + W (information
    only in the headline; the variant ``war-in-window-apart`` sets it apart). The war year *at entry* is K15.
K14. *The net variant.* ``variant-net.csv`` is the headline lines whose counted status reads the net measures; ``shown.csv``
    carries gross and net side by side for the headline.
K15. *War at entry* (section 11, B2; M0 section 1, the twin's ``entry_in_war_year: apart``). The war year at the entry year
    is read as ``strain.py`` reads it (``panel.war_at``, the workshop's ``war.py``): ``yes`` is *apart*, ``cannot be read``
    is *cannot be read* (frame c's R14). The column ``war_at_entry`` carries the reading.
K16. *Regime carried per source*: K8.
K17. *The DOLLAR_EURO table* (section 11, O4): economy -> spans (first year, last year, currency, reason, source), built at
    load by :func:`dollar_euro`, never typed. It holds (a) every IRR fine class 1 money with a USD or EUR anchor, year by
    year (the class read from its own last year on, the anchor likewise: K8), **minus** the currency unions' members
    (``frame_a.UNION_OF``: section 10) and the named exclusions :data:`DE_EXCLUDED`; (b) the euro's members from their entry
    (``frame_a.EURO_ENTRY``); (c) the United States as the dollar's issuer (off in ``class1-only``); (d) the hand additions
    :data:`DE_ADDED`, where IRR has no class or no anchor. Each span carries its reason.
K18. *Not a money of its own* (section 11, O5; M0 section 1). An entry of an economy whose legal tender is another's money in
    the entry year is *apart*, "not a money of its own (M0 section 1)": a ``DOLLAR_EURO`` economy in that year (the United
    States, the dollar's issuer, is not one: its money is its own) or a member of ``XOF``, ``XAF`` or ``XCD``
    (``frame_a.UNION_OF``) in the years of ``window_a.UNION_SPAN``. The column ``own_money`` carries the reading.
K19. *GDP in local currency* (section 11, O1): IFS ``NGDP_XDC``; where IFS has none, the World Bank's ``NY.GDP.MKTP.CN``
    ("GDP (current LCU)"), used only where it agrees with IFS within a factor of 2 in every common year
    (its own check, every common year; window_a's W20 reads the median since section 18). With no common year it is not
    used (section 13: nothing checks its unit against the rate's; Venezuela's bolivar was 1e11-1e13 off). The year read
    from the World Bank is flagged ``gdp_worldbank``.
K20. *The rate* (section 11, O2): the year average of IFS's monthly ``ENDE_XDC_USD_RATE``, all twelve months read; else the
    GDP in dollars of that year is unread.
K24. *GDP in dollars is screened for units* (section 14, B1): a year whose dollar GDP differs from the year before's by
    more than a factor of ``UNITS_BREAK_FACTOR`` either way is a units break (Belarus's rate, about 11,200 times, at
    January 2000). The segment after the last break is kept; earlier years are not read, and an entry among them is
    flagged ``gdp_units_break``. The report lists every break.
K25. *The variant* ``war-unreadable-as-no`` (section 14, B2): an entry year whose war status cannot be read (``war.py``
    W9: COW's war files end in 2007) is read as no war, as frames c and d read it.
K26. *W12 and the variant* ``war-before-w12`` (section 15). The headline reads war through ``panel.war_at`` with W12 on
    (``ucdp=True``, ``war.py``'s default): after COW's coverage a state-year that was *cannot be read* only for lack of the
    state's own losses abroad is *no* where UCDP/PRIO v26.1 lists the state as party to no conflict of cumulative
    intensity 1. The variant ``war-before-w12`` (``Spec.war_ucdp`` off) reads the third build's war, W9 alone
    (``World.war_before_w12``, ``panel.war_at(..., ucdp=False)``). ``war-moves.csv`` lists each line whose ``war_at_entry``
    differs, with its status on each side (``panel.war_moves``). W12 never makes a *yes*, so ``war_in_window`` never moves.
K27. *The variant* ``areaer`` (section 16, gap G11), read **only in that variant**. The table
    ``data/reconstructed/ft001-k/areaer/resident-fx-accounts.csv`` (``money, year, status, edition, page, as_of, note``)
    states, for a money-year, whether residents may hold foreign exchange accounts at home: *permitted*, *not permitted*,
    *permitted with conditions* (read as *permitted*, said) or *not printed*. In a cell year (``cell_at`` is read at the
    entry year and the year before, K1, so both years are read this way):
    *not permitted* makes **forced** *yes* (the cell is *closed*, whatever ka_open reads, even none); *permitted* makes a
    substitute at hand *yes* (the cell is *open* when ka_open is read and above the line, with or without a border; a
    year without ka_open stays *cannot be read*, since forced cannot be told); *not printed*, or a year not in the table,
    leaves the headline's reading. ka_open at or below the line stays *closed* whatever the table says (forced comes
    first). A cell made by the table carries the flag ``areaer_forced`` or ``areaer_substitute`` (a border that already
    made it open carries none). A malformed table (a status that is not one of the four, a money-year given two
    different readings) raises: it never silently reads as the headline. A missing table writes no variant; the build
    says so in one line (stderr) and in its report.
K21. *The neo variant* (section 11, M4): ``neo-negative-only``: only a negative balance adds.
K22. *Censored lines carry what was read so far* (M0 section 4; section 11): ``m1c_so_far`` (the change from t to the last
    year read up to the measure's data end) and ``m2_so_far`` (the sum over t + 1 to that year, % of the entry year's GDP),
    with ``so_far_note`` naming the years. Only the status *censored*; no net.
K23. *The report* (section 11, M3): the build's report lists the money-years below the line that the deposit freezes removed
    (money, year, real return) and how Argentina 1989's freeze was read.
"""

from __future__ import annotations

import csv
import math
import re
import statistics
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DATA = ROOT / "data"
OUT = DATA / "reconstructed" / "ft001-k"

FIRST_ENTRY_YEAR = 1970
KA_EPS = 1e-9
FREEZE_FILE = (DATA / "laeven-valencia" / "systemic-banking-crises-2026" / "2026-09-30" /
               "SYSTEMIC_BANKING_CRISES_DATABASE_2026.xlsx")
FREEZE_SHEET = "Resolution Details"
CONTIGUITY_ZIP = DATA / "cow" / "direct-contiguity-v3.2" / "2026-10-01" / "DirectContiguity320.zip"
CONTIGUITY_CSV = "DirectContiguity320/contdird.csv"
FOREIGN_ANCHORS = ("USD", "EUR")
from frame_a import UNION_OF     # section 10: XOF, XAF and XCD members (class 1 in IRR, never the dollar or the euro)
from window_a import UNION_SPAN                          # K18: the union spans
UNITS_BREAK_FACTOR = 20.0                               # K24: a units break in dollar GDP (section 14, B1)
GDP_SEAM_FACTOR = 2.0                                   # K19: the World Bank segment within a factor of 2 (section 11)
WB_GDP = "NY.GDP.MKTP.CN"        # K19: the World Bank's GDP (current LCU), frozen under data/worldbank/
NOT_OWN = "not a money of its own (M0 section 1)"
AREAER_FILE = DATA / "reconstructed" / "ft001-k" / "areaer" / "resident-fx-accounts.csv"     # K27, section 16
AREAER_STATUSES = ("permitted", "not permitted", "permitted with conditions", "not printed")
ASSETS = ("BFDA", "BFPA", "BFOA")
DERIVATIVES = "BFFA"             # section 9: the variant with-derivatives only
M1_REASON = ("IFS splits residents' deposits by currency for one area only (35B/35X) and the bans that would make "
             "deposits all local are not dated")
BLIND_SPOT = {"m1": "readable nowhere: " + M1_REASON,
              "m1c": "misses the main road out in open cells, from local deposits into home foreign-currency deposits",
              "m2": "sees only what crosses the border"}
DEPTHS = ("(-10,-5]", "(-20,-10]", "<=-20")
PI_BANDS = ("below 20", "20-40", "40 or more")


@dataclass(frozen=True)
class Spec:
    n: int = 2                    # N: the run's length [1; 3]
    line: float = -5.0            # the line, % [0; -10]
    w: int = 3                    # W: the window, and the spacing [2; 5]
    ka_line: float = 0.25         # forced at or below [0.1; 0.5]
    fisher: bool = False          # the Fisher real return (variant)
    net: bool = False             # the counted status reads the measures net of their own change (variant)
    neo: str = "reversed"         # K10, K21; "negative-only" is the variant neo-negative-only (section 11, M4)
    us_issuer: bool = True        # K7, section 9: the dollar's issuer counts; off in class1-only
    derivatives: bool = False     # section 9: BFFA in m2, the variant with-derivatives
    carry: bool = True            # K8, section 11 B1: carry each regime source from its own last year; off in no-carry
    war_window_apart: bool = False   # K11, section 11 B2: a war year in t ... t + W is apart, the variant war-in-window-apart
    war_unreadable_as_no: bool = False   # K25, section 14 B2: the variant war-unreadable-as-no
    war_ucdp: bool = True                # K26, section 15: W12 on; off in the variant war-before-w12
    areaer: bool = False                 # K27, section 16: the cells also read AREAER's table; on in the variant areaer


HEADLINE = Spec()
VARIANTS = {"N1": Spec(n=1), "N3": Spec(n=3), "line-0": Spec(line=0.0), "line-10": Spec(line=-10.0),
            "W2": Spec(w=2), "W5": Spec(w=5), "kaopen-010": Spec(ka_line=0.1), "kaopen-050": Spec(ka_line=0.5),
            "fisher": Spec(fisher=True), "net": Spec(net=True), "class1-only": Spec(us_issuer=False),
            "with-derivatives": Spec(derivatives=True), "war-in-window-apart": Spec(war_window_apart=True),
            "no-carry": Spec(carry=False), "neo-negative-only": Spec(neo="negative-only"),
            "war-unreadable-as-no": Spec(war_unreadable_as_no=True), "war-before-w12": Spec(war_ucdp=False),
            "areaer": Spec(areaer=True)}


# --- the entry (section 2) ------------------------------------------------------------------------------------------

def real_return(rate: float, pi: float, fisher: bool = False) -> float:
    """The real deposit return, % a year: the deposit rate less pi (M0's reading), or (1 + i) / (1 + pi) - 1."""
    if fisher:
        return 100 * ((1 + rate / 100) / (1 + pi / 100) - 1)
    return rate - pi


def real_returns(rate: dict[int, float], pi: dict[int, float], freeze: set[int] = frozenset(),
                 fisher: bool = False) -> dict[int, float]:
    """{year: real return} where the rate and pi both read and the year is not under a deposit freeze. A year absent
    here breaks a run (neither below nor above the line)."""
    out = {}
    for y, i in rate.items():
        if y in freeze or y not in pi or (fisher and pi[y] <= -100):
            continue
        out[y] = real_return(i, pi[y], fisher)
    return out


def entries(returns: dict[int, float], spec: Spec = HEADLINE) -> list[int]:
    """The entry years (K3, K5): the last year of N consecutive years below the line, from 1970, none within W years after
    an entry. Reads no holding."""
    out: list[int] = []
    if not returns:
        return out
    last = None
    for y in range(min(returns), max(returns) + 1):
        if y < FIRST_ENTRY_YEAR:
            continue
        if not all(returns.get(y - k, math.inf) < spec.line for k in range(spec.n)):
            continue
        if last is not None and y <= last + spec.w:
            continue
        out.append(y)
        last = y
    return out


def freeze_in_window(entry: int, freeze: set[int], w: int) -> list[int]:
    """K4: the freeze years in t + 1 ... t + W."""
    return [y for y in range(entry + 1, entry + w + 1) if y in freeze]


# --- the cells (section 3) ------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Span:
    """One span of the DOLLAR_EURO table (K17): the economy's legal tender is ``currency`` from ``first`` to ``last``
    (None: unbounded)."""
    first: int | None
    last: int | None
    currency: str                 # USD | EUR
    reason: str
    source: str                   # IRR | ECB | issuer | session

    def holds(self, year: int) -> bool:
        return (self.first is None or self.first <= year) and (self.last is None or year <= self.last)


#: Named exclusions from the IRR-built part of the table (section 11, O4; the audit's pass over IRR's class 1 with a USD or
#: EUR anchor): economy -> ((first year, last year, reason), ...). IRR's anchor there is a regime's coding, not the legal
#: tender. The currency unions' members are excluded whole, by ``frame_a.UNION_OF`` (section 10).
DE_EXCLUDED = {
    "ERI": ((None, 1997, "Eritrea's money was the Ethiopian birr until the nakfa in 1997: IRR's USD anchor is not its "
                         "legal tender (audit O4)"),),
    "SRB": ((2001, 2002, "Serbia's legal tender was the dinar: IRR's EUR anchor is not its legal tender (audit O4)"),),
    "VNM": ((1950, 1955, "audit O4: not a dollar economy; before 1970, it moves no entry and no cell"),),
    "GRC": ((1999, 2000, "the drachma stayed Greece's legal tender until its euro entry in 2001 (the ECB's list): IRR's "
                         "class 1 with a EUR anchor from 1999 is not its legal tender (the session, section 12)"),),
}
#: Hand additions (section 11, O4), where IRR has no class (Fine sheet) or no anchor (Master sheet), **the session's
#: reading of each economy's legal tender, not a frozen source** (a need). Each is an unbounded span: a legal fact, not a
#: carried source.
DE_ADDED = {
    "MNE": (Span(2002, None, "EUR", "Montenegro: the euro from 2002 (IRR has the class, no anchor column)", "session"),),
    "XKX": (Span(2002, None, "EUR", "Kosovo: the euro from 2002 (not in IRR's Fine sheet nor its anchors)", "session"),),
    "AND": (Span(2002, None, "EUR", "Andorra: the euro from 2002, the year of its notes and coins; before it the French "
                                    "franc and the peseta circulated without a monetary agreement. IRR's anchor sheet "
                                    "reads EUR from 1999, but has no class for Andorra", "session"),),
    "TLS": (Span(2000, None, "USD", "Timor-Leste: the US dollar from 2000 (not in IRR's Fine sheet nor its anchors)",
                 "session"),),
}
UNION_REASON = "a member of a currency union with a money of its own (section 10): excluded whole"


def _runs(years: list[int]) -> list[tuple[int, int]]:
    out: list[list[int]] = []
    for y in sorted(years):
        if out and out[-1][1] == y - 1:
            out[-1][1] = y
        else:
            out.append([y, y])
    return [(a, b) for a, b in out]


def dollar_euro(classes: dict[str, dict[int, int]], anchors: dict[str, dict[int, str]], euro_entry: dict[str, int],
                class_end: int | None, anchor_end: int | None) -> dict[str, tuple[Span, ...]]:
    """K17: the DOLLAR_EURO table, economy -> spans, built by the rule over ``classes`` (money -> year -> IRR fine class)
    and ``anchors`` (money -> year -> anchor): every money with class 1 and a USD or EUR anchor in a year, from the first
    year read to the later of the two sources' last years (each source read at its own last year after that: K8), minus
    the unions' members and :data:`DE_EXCLUDED`; plus the euro's members from ``euro_entry``, the United States (the
    issuer), and :data:`DE_ADDED`."""
    table: dict[str, list[Span]] = defaultdict(list)
    if class_end is not None and anchor_end is not None:
        top = max(class_end, anchor_end)
        for m, by_year in classes.items():
            if m in UNION_OF or not by_year:
                continue
            skip = DE_EXCLUDED.get(m, ())
            per_cur: dict[str, list[int]] = defaultdict(list)
            for y in range(min(by_year), top + 1):
                cls, anc = by_year.get(min(y, class_end)), anchors.get(m, {}).get(min(y, anchor_end))
                if cls == 1 and anc in FOREIGN_ANCHORS and not any(
                        (lo is None or lo <= y) and (hi is None or y <= hi) for lo, hi, _ in skip):
                    per_cur[anc].append(y)
            for cur, ys in per_cur.items():
                for a, b in _runs(ys):
                    table[m].append(Span(a, b, cur, f"IRR fine class 1 (no separate legal tender) with a {cur} anchor",
                                         "IRR"))
    for m, entry in euro_entry.items():
        table[m].append(Span(entry, None, "EUR", "a euro member from its entry (the ECB's member list)", "ECB"))
    table["USA"].append(Span(None, None, "USD", "the dollar's own issuer (section 9)", "issuer"))
    for m, spans in DE_ADDED.items():
        table[m].extend(spans)
    return {m: tuple(spans) for m, spans in sorted(table.items())}


DE_FIELDS = ["economy", "first", "last", "currency", "source", "reason"]


def dollar_euro_rows(world: "World") -> list[dict]:
    """The table as rows (the report, ``dollar-euro.csv``), with the exclusions listed, so that nothing is hidden."""
    rows = [{"economy": m, "first": "" if sp.first is None else sp.first, "last": "" if sp.last is None else sp.last,
             "currency": sp.currency, "source": sp.source, "reason": sp.reason}
            for m, spans in world.dollar_euro.items() for sp in spans]
    for m, items in DE_EXCLUDED.items():
        rows += [{"economy": m, "first": "" if lo is None else lo, "last": "" if hi is None else hi, "currency": "",
                  "source": "excluded", "reason": why} for lo, hi, why in items]
    rows += [{"economy": m, "first": "", "last": "", "currency": "", "source": "excluded", "reason": UNION_REASON}
             for m in sorted(UNION_OF) if m in world.classes]
    return rows


@dataclass(frozen=True)
class World:
    """What the cells and the flags read beyond a money's own series (never a holding). The three regime sources' last years
    are found in the data (K8)."""
    contiguity: dict[tuple[str, int], set[str]] = field(default_factory=dict)   # (money, year) -> land neighbours
    classes: dict[str, dict[int, int]] = field(default_factory=dict)            # money -> year -> IRR fine class
    anchors: dict[str, dict[int, str]] = field(default_factory=dict)            # money -> year -> IRR anchor
    euro_entry: dict[str, int] = field(default_factory=dict)                    # money -> first year in the euro
    war: Callable[[str, int], str] = lambda m, y: "no"
    dollar_euro: dict[str, tuple[Span, ...]] | None = None                      # K17; built from the above when None
    war_before_w12: Callable[[str, int], str] | None = None                     # K26: W9 alone (the variant war-before-w12)
    areaer: dict[tuple[str, int], str] = field(default_factory=dict)            # K27: (money, year) -> permitted | not permitted
    contiguity_end: int | None = field(init=False, default=None)
    class_end: int | None = field(init=False, default=None)
    anchor_end: int | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        put = object.__setattr__
        put(self, "contiguity_end", max((y for _, y in self.contiguity), default=None))
        put(self, "class_end", max((y for by in self.classes.values() for y in by), default=None))
        put(self, "anchor_end", max((y for by in self.anchors.values() for y in by), default=None))
        if self.dollar_euro is None:
            put(self, "dollar_euro", dollar_euro(self.classes, self.anchors, self.euro_entry, self.class_end,
                                                 self.anchor_end))

    @property
    def min_end(self) -> int | None:
        """The earlier of the classes' and the anchors' last years: a neighbour read after it reads a carried year."""
        ends = [e for e in (self.class_end, self.anchor_end) if e is not None]
        return min(ends) if ends else None

    @property
    def table_end(self) -> int | None:
        ends = [e for e in (self.class_end, self.anchor_end) if e is not None]
        return max(ends) if ends else None


def dollar_euro_span(m: str, year: int, world: World, us_issuer: bool = False,
                     carry: bool = True) -> tuple[Span | None, bool]:
    """K7, K8, K17: (the span that makes the economy's legal tender the dollar or the euro in ``year``, or None; whether
    it was read through a carried year). The IRR-built spans are read at ``min(year, table end)`` (each source from its
    own last year) and are carried after the earlier of the two sources' ends; with ``carry`` off they are unread there."""
    low = world.min_end
    for sp in world.dollar_euro.get(m, ()):
        if sp.source == "issuer":
            if us_issuer:
                return sp, False
        elif sp.source == "IRR":
            if low is None or (year > low and not carry):
                continue
            if sp.holds(min(year, world.table_end)):
                return sp, year > low
        elif sp.holds(year):
            return sp, False
    return None, False


def foreign_legal(m: str, year: int, world: World, us_issuer: bool = False, carry: bool = True) -> bool:
    """K7: the economy's legal tender is the dollar or the euro in ``year`` (its place in the DOLLAR_EURO table)."""
    return dollar_euro_span(m, year, world, us_issuer, carry)[0] is not None


def own_money(m: str, year: int, world: World, spec: "Spec" = None) -> tuple[bool, str, tuple[str, ...]]:
    """K18: (the economy's money is its own in ``year``, the reason it is not, the flags). Not its own: a member of XOF,
    XAF or XCD in the years of ``UNION_SPAN``, or a DOLLAR_EURO economy (the dollar's issuer excepted: its money is its own)."""
    spec = spec or HEADLINE
    if m in UNION_OF:
        lo, hi = UNION_SPAN.get(m, (None, None))
        if (lo is None or lo <= year) and (hi is None or year <= hi):
            return False, f"the {UNION_OF[m]} union's money", ()
    sp, carried = dollar_euro_span(m, year, world, False, spec.carry)
    if sp is not None:
        return False, f"a {sp.currency} economy: {sp.reason}", ("regime_carried",) if carried else ()
    return True, "", ()


@dataclass(frozen=True)
class Cell:
    state: str                    # open | closed | cannot be read
    forced: bool | None
    border: bool | None
    flags: tuple[str, ...] = ()
    why: str = ""


def cell_at(m: str, year: int, ka: dict[int, float], world: World, spec: Spec = HEADLINE) -> Cell:
    """K6, K8: the money's cell in one year. In the variant ``areaer`` (K27), the year's AREAER status also reads:
    *not permitted* is a forced cell (closed), *permitted* a substitute at hand."""
    k = ka.get(year)
    status = world.areaer.get((m, year)) if spec.areaer else None
    if status == "not permitted":
        return Cell("closed", True, None, ("areaer_forced",),
                    f"AREAER: residents may not hold foreign exchange accounts at home in {year} (variant areaer)")
    if k is None:
        return Cell("cannot be read", None, None, (), f"ka_open not read in {year}")
    if k <= spec.ka_line + KA_EPS:
        return Cell("closed", True, None, (), "")
    ce, low = world.contiguity_end, world.min_end
    if ce is not None and year > ce:
        neighbours = world.contiguity.get((m, ce), set()) if spec.carry else set()
    else:
        neighbours = world.contiguity.get((m, year), set())
    carried = spec.carry and ((ce is not None and year > ce) or (bool(neighbours) and low is not None and year > low))
    flags = ("regime_carried",) if carried else ()
    hit = sorted(n for n in neighbours if foreign_legal(n, year, world, spec.us_issuer, spec.carry))
    if hit:
        return Cell("open", False, True, flags, "border with " + " ".join(hit))
    if status == "permitted":
        return Cell("open", False, False, (*flags, "areaer_substitute"),
                    f"AREAER: residents may hold foreign exchange accounts at home in {year} (variant areaer)")
    ends = [e for e in (ce, world.class_end, world.anchor_end) if e is not None]
    cut = (f" (variant no-carry: the regime sources are read to {min(ends)} at most, not carried)"
           if not spec.carry and ends and year > min(ends) else "")
    return Cell("cannot be read", False, False, flags,
                f"not forced in {year} and no land border with a dollar or euro economy: deposits and cash are not dated" + cut)


def cell_summary(now: Cell, before: Cell, year: int) -> tuple[str, str]:
    """K1: (open | closed | changed | cannot be read, reason)."""
    if now.state == "cannot be read":
        return "cannot be read", now.why
    if before.state == "cannot be read":
        return "cannot be read", f"year before ({year - 1}): {before.why}"
    if now.state != before.state:
        return "changed", f"{before.state} in {year - 1}, {now.state} in {year}"
    return now.state, ""


# --- the measures (section 4) ---------------------------------------------------------------------------------------

@dataclass
class Reading:
    value: float | None
    flags: list[str] = field(default_factory=list)
    why: str = ""
    ok: bool = True


def unread(why: str, flags: list[str] | None = None) -> Reading:
    return Reading(None, list(flags or []), why, False)


def m1() -> Reading:
    """Local-currency money: cannot be read, for every entry."""
    return unread(M1_REASON)


def m1c(lm: dict[int, tuple[float, str]], t: int, w: int, net: bool = False, values: bool = True) -> Reading:
    """K9: the change in log real currency from t to t + w; ``net``, less its change from t - w to t. ``lm``:
    {year: (log real currency, source)}. A source seam in the span read leaves it unread (``seam``)."""
    lo = t - w if net else t
    for y in {lo, t, t + w}:
        if y not in lm:
            return unread(f"real currency not read in {y}")
    if len({lm[y][1] for y in range(lo, t + w + 1) if y in lm}) > 1:
        return unread("a source seam inside the span", ["seam"])
    if not values:
        return Reading(None)
    v = lm[t + w][0] - lm[t][0]
    return Reading(v - (lm[t][0] - lm[t - w][0]) if net else v)


def outflow(bop: dict[str, dict[int, float]], y: int, neo: str = "reversed", derivatives: bool = False) -> float | None:
    """K10: the year's recorded acquisitions of foreign assets (reserves excluded) and the unrecorded outflow; None when a
    part is unread. ``derivatives`` adds BFFA (section 9's variant)."""
    parts = [bop.get(k, {}).get(y) for k in (*ASSETS, *((DERIVATIVES,) if derivatives else ()))]
    e = bop.get("NEO", {}).get(y)
    if e is None or any(p is None for p in parts):
        return None
    return sum(parts) + (-e if neo == "reversed" else max(0.0, -e))


def m2(bop: dict[str, dict[int, float]], gdp_usd: dict[int, float], t: int, w: int, neo: str = "reversed",
       net: bool = False, values: bool = True, derivatives: bool = False) -> Reading:
    """K10: the sum of the year outflows over t + 1 ... t + w, % of the entry year's dollar GDP; ``net``, less the same
    sum over t - w + 1 ... t."""
    g = gdp_usd.get(t)
    if g is None or not g > 0:
        return unread(f"GDP in dollars not read in {t}")
    spans = [range(t + 1, t + w + 1)] + ([range(t - w + 1, t + 1)] if net else [])
    for span in spans:
        for y in span:
            if outflow(bop, y, neo, derivatives) is None:
                return unread(f"balance of payments not read in {y}")
    if not values:
        return Reading(None)
    after = sum(outflow(bop, y, neo, derivatives) for y in spans[0])
    before = sum(outflow(bop, y, neo, derivatives) for y in spans[1]) if net else 0.0
    return Reading(100 * (after - before) / g)


def m1c_so_far(lm: dict[int, tuple[float, str]], t: int, last: int) -> Reading:
    """K22: the change in log real currency from t to ``last`` (the last year read up to the data end), for a censored
    entry; unread where ``last`` is not after t, an end is missing, or a source seam falls inside."""
    if last <= t:
        return unread(f"no year after the entry ({t}) is inside the data")
    for y in {t, last}:
        if y not in lm:
            return unread(f"real currency not read in {y}")
    if len({lm[y][1] for y in range(t, last + 1) if y in lm}) > 1:
        return unread("a source seam inside the span", ["seam"])
    return Reading(lm[last][0] - lm[t][0])


def m2_so_far(bop: dict[str, dict[int, float]], gdp_usd: dict[int, float], t: int, last: int, neo: str = "reversed",
              derivatives: bool = False) -> Reading:
    """K22: the sum of the year outflows over t + 1 ... ``last``, % of the entry year's dollar GDP, for a censored entry."""
    if last <= t:
        return unread(f"no year after the entry ({t}) is inside the data")
    g = gdp_usd.get(t)
    if g is None or not g > 0:
        return unread(f"GDP in dollars not read in {t}")
    parts = [outflow(bop, y, neo, derivatives) for y in range(t + 1, last + 1)]
    if any(p is None for p in parts):
        return unread("balance of payments not read in a year of the span")
    return Reading(100 * sum(parts) / g)


def gdp_lcu(ifs: dict[int, float], wb: dict[int, float],
            factor: float = GDP_SEAM_FACTOR) -> tuple[dict[int, float], dict[int, tuple[str, ...]], str]:
    """K19: (GDP in local currency by year, the flags by year, why the World Bank's was not used). IFS ``NGDP_XDC`` first;
    the World Bank's GDP (current LCU) only for the years IFS lacks, and only where it agrees with IFS within ``factor`` in
    every common year; with no common year it is not used (section 13). A year read from the World Bank is flagged
    ``gdp_worldbank``."""
    out, flags = dict(ifs), {}
    if not wb:
        return out, flags, ""
    common = [t for t in set(ifs) & set(wb) if ifs[t] > 0 and wb[t] > 0]
    if not common:                                                                      # section 13
        return out, flags, "no common year with IFS: the World Bank's GDP unit cannot be checked against the rate: not used"
    off = [t for t in sorted(common) if not 1 / factor <= wb[t] / ifs[t] <= factor]    # every common year (section 11)
    if off:
        return out, flags, (f"GDP seam: the World Bank's GDP differs from IFS's by more than a factor of {factor:g} in "
                            f"{', '.join(map(str, off))}: not used")
    tag = ("gdp_worldbank",)
    for t, v in wb.items():
        if t not in out:
            out[t], flags[t] = v, tag
    return out, flags, ""


def year_average(monthly: dict[int, float]) -> dict[int, float]:
    """K20: {year: the mean of the twelve months} where all twelve months of the year are read and positive; ``monthly``
    is keyed by the month index ``year * 12 + month - 1`` (``panel.ifs``'s monthly layout)."""
    out = {}
    for y in {i // 12 for i in monthly}:
        months = [monthly.get(y * 12 + k) for k in range(12)]
        if all(v is not None and v > 0 for v in months):
            out[y] = sum(months) / 12
    return out


def units_screen(gdp_usd: dict[int, float],
                 factor: float = UNITS_BREAK_FACTOR) -> tuple[dict[int, float], set[int], list[int]]:
    """K24: (the dollar GDP kept, the years dropped, the break years). A break is a year whose value differs from the
    previous year read by more than ``factor`` either way; the segment from the last break on is kept."""
    years = sorted(y for y, v in gdp_usd.items() if v > 0)
    breaks = [b for a, b in zip(years, years[1:]) if not 1 / factor <= gdp_usd[b] / gdp_usd[a] <= factor]
    if not breaks:
        return dict(gdp_usd), set(), []
    last = breaks[-1]
    return {y: v for y, v in gdp_usd.items() if y >= last}, {y for y in gdp_usd if y < last}, breaks


def gdp_usd_of(gdp: dict[int, float], rate: dict[int, float]) -> dict[int, float]:
    """K20: the GDP in dollars where the year's average rate (local units per dollar) is read."""
    return {y: gdp[y] / rate[y] for y in gdp if y in rate and rate[y] > 0}


# --- the strata -----------------------------------------------------------------------------------------------------

def depth_stratum(r: float) -> str:
    if r <= -20:
        return "<=-20"
    if r <= -10:
        return "(-20,-10]"
    return "(-10,-5]" if r <= -5 else "above -5"


def pi_stratum(p: float) -> str:
    return "below 20" if p < 20 else ("20-40" if p < 40 else "40 or more")


# --- the lines ------------------------------------------------------------------------------------------------------

@dataclass
class MoneyData:
    """One money's readings. The first four are the entry's and the cell's; the rest are the measures'."""
    money: str
    rate: dict[int, float] = field(default_factory=dict)
    pi: dict[int, float] = field(default_factory=dict)
    freeze: set[int] = field(default_factory=set)
    ka: dict[int, float] = field(default_factory=dict)
    lm: dict[int, tuple[float, str]] = field(default_factory=dict)
    bop: dict[str, dict[int, float]] = field(default_factory=dict)
    gdp_usd: dict[int, float] = field(default_factory=dict)
    gdp_flags: dict[int, tuple[str, ...]] = field(default_factory=dict)     # K19: gdp_worldbank by year
    gdp_dropped: set[int] = field(default_factory=set)                      # K24: years dropped by the units screen


FIELDS = ["period", "value", "unit", "source", "locator", "note", "uncertainty", "money", "frame", "route", "entry_date",
          "entry_measure", "entry_measure_date", "outcome", "outcome_date", "onset_date", "responses", "exit", "status",
          "coder", "rules_sha256", "reason", "real_return", "pi", "depth_stratum", "pi_stratum", "ka_open",
          "ka_open_before", "forced", "border", "cell", "cell_before", "m1", "m1_reason", "m1c", "m1c_net", "m1c_why",
          "m2", "m2_net", "m2_why", "m1c_so_far", "m2_so_far", "so_far_note", "own_money", "war_at_entry", "censored",
          "freeze_in_window", "flags", "variant"]
SHOWN_FIELDS = ["variant", "stratum_kind", "stratum", "measure", "basis", "n_open", "n_closed", "mean_open", "median_open",
                "mean_closed", "median_closed", "open_minus_closed", "blind_spot"]


def num(v: float | None, digits: int = 6) -> str:
    return "" if v is None else f"{v:.{digits}g}"


def war_reader(world: World, spec: Spec) -> Callable[[str, int], str]:
    """K26: the war reader a spec uses: W12's (``world.war``) in the headline, ``world.war_before_w12`` (W9 alone) in the
    variant ``war-before-w12``. A world without the second reader raises: the variant must never read the headline's war."""
    if spec.war_ucdp:
        return world.war
    if world.war_before_w12 is None:
        raise ValueError("the variant war-before-w12 needs World.war_before_w12 (panel.war_at with ucdp=False)")
    return world.war_before_w12


def line_for(md: MoneyData, t: int, world: World, spec: Spec, variant: str, sha: str, ends: dict[str, int],
             returns: dict[int, float], values: bool = True) -> dict:
    """The case line of the entry of ``md.money`` in year ``t``."""
    m, w = md.money, spec.w
    r, pi = returns[t], md.pi[t]
    now, before = cell_at(m, t, md.ka, world, spec), cell_at(m, t - 1, md.ka, world, spec)
    cell, cell_why = cell_summary(now, before, t)
    own, own_why, own_flags = own_money(m, t, world, spec)
    war = war_reader(world, spec)
    war_entry = war(m, t)
    if spec.war_unreadable_as_no and war_entry == "cannot be read":     # K25
        war_entry = "no"
    war_years = [y for y in range(t, t + w + 1) if war(m, y) == "yes"]
    frozen = freeze_in_window(t, md.freeze, w)
    data_end = max(ends.values(), default=0)
    censored = t + w > data_end
    g1 = m1c(md.lm, t, w, False, values)
    n1 = m1c(md.lm, t, w, True, values)
    g2 = m2(md.bop, md.gdp_usd, t, w, spec.neo, False, values, spec.derivatives)
    n2 = m2(md.bop, md.gdp_usd, t, w, spec.neo, True, values, spec.derivatives)
    read = (n1, n2) if spec.net else (g1, g2)
    if not own:
        status, reason = "apart", NOT_OWN
    elif frozen:
        status, reason = "cannot be read", f"a deposit freeze in the window ({' '.join(map(str, frozen))})"
    elif cell == "cannot be read":
        status, reason = "cannot be read", cell_why
    elif war_entry == "cannot be read":
        status, reason = "cannot be read", f"whether {t} is a war year cannot be read (frame c's R14)"
    elif war_entry == "yes":
        status, reason = "apart", f"a war year at entry ({t}; M0 section 1)"
    elif cell == "changed":
        status, reason = "apart", "cell changed in the year before: " + cell_why
    elif spec.war_window_apart and war_years:
        status, reason = "apart", f"a war year inside the window ({' '.join(map(str, war_years))}; variant war-in-window-apart)"
    elif censored:
        status, reason = "censored", f"the window to {t + w} runs past the measures' data ({data_end})"
    elif not any(x.ok for x in read):
        status, reason = "cannot be read", "neither m1c nor m2 read over the window" + (" (net)" if spec.net else "")
    else:
        status, reason = "counted", ""
    so1 = so2 = None
    note = ""
    if status == "censored" and values:           # K22: what was read so far, up to each measure's data end
        last1, last2 = min(t + w, ends.get("m1c", 0)), min(t + w, ends.get("m2", 0))
        so1 = m1c_so_far(md.lm, t, last1)
        so2 = m2_so_far(md.bop, md.gdp_usd, t, last2, spec.neo, spec.derivatives)
        note = "; ".join(p for p in ((f"m1c to {last1}" if so1.ok else ""), (f"m2 to {last2}" if so2.ok else "")) if p)
    flags = list(dict.fromkeys([*now.flags, *before.flags, *own_flags]))
    for name, x in (("m1c", g1), ("m1c_net", n1), ("m2", g2), ("m2_net", n2), ("m1c_so_far", so1), ("m2_so_far", so2)):
        flags += [f"{name}:{f}" for f in (x.flags if x else [])]
    if g2.ok or n2.ok or (so2 is not None and so2.ok):     # K19: the entry year's GDP came from the World Bank
        flags += [f for f in md.gdp_flags.get(t, ()) if f not in flags]
    if t in md.gdp_dropped:                                  # K24
        flags.append("gdp_units_break")
    if war_years:
        flags.append("war_in_window")
    fisher = " (Fisher)" if spec.fisher else ""
    return {
        "period": str(t), "value": num(r), "unit": f"% a year (real deposit return{fisher})",
        "source": "IFS FIDR_PA less pi (panel.Panel.pi_annual, M0's order); Laeven-Valencia freezes; Chinn-Ito; COW contiguity; IRR",
        "locator": f"{m} {t}: run of {spec.n} year(s) {t - spec.n + 1}-{t} below {spec.line:g}%",
        "note": "", "uncertainty": "", "money": m, "frame": "k", "route": "k", "entry_date": str(t),
        "entry_measure": num(r), "entry_measure_date": str(t), "outcome": "", "outcome_date": "", "onset_date": "",
        "responses": "", "exit": "", "status": status, "coder": "script: missions/code/frame_k.py", "rules_sha256": sha,
        "reason": reason, "real_return": num(r), "pi": num(pi), "depth_stratum": depth_stratum(r),
        "pi_stratum": pi_stratum(pi), "ka_open": num(md.ka.get(t)), "ka_open_before": num(md.ka.get(t - 1)),
        "forced": {True: "yes", False: "no", None: "cannot be read"}[now.forced],
        "border": {True: "yes", False: "no", None: ""}[now.border], "cell": cell, "cell_before": before.state,
        "m1": "cannot be read", "m1_reason": M1_REASON, "m1c": num(g1.value), "m1c_net": num(n1.value),
        "m1c_why": g1.why or n1.why, "m2": num(g2.value), "m2_net": num(n2.value), "m2_why": g2.why or n2.why,
        "m1c_so_far": num(so1.value if so1 else None), "m2_so_far": num(so2.value if so2 else None),
        "so_far_note": note, "own_money": "yes" if own else "no", "war_at_entry": war_entry,
        "censored": "yes" if censored else "no", "freeze_in_window": " ".join(map(str, frozen)),
        "flags": " ".join(flags), "variant": variant}


def lines_for(datas: list[MoneyData], world: World, spec: Spec, variant: str, sha: str, ends: dict[str, int],
              values: bool = True) -> list[dict]:
    rows = []
    for md in datas:
        returns = real_returns(md.rate, md.pi, md.freeze, spec.fisher)
        for t in entries(returns, spec):
            rows.append(line_for(md, t, world, spec, variant, sha, ends, returns, values))
    return rows


# --- the told table (section 4) -------------------------------------------------------------------------------------

def shown_rows(lines: list[dict], variant: str = "headline") -> list[dict]:
    """For each stratum (all, depth, pi) and measure (m1, m1c, m2; gross and net), over the counted lines whose cell is open
    or closed: n open, n closed, the mean and median of each, the open-minus-closed difference of means. n in every row; no
    margin. m1 has no reading: its n are 0 and its blind spot says why."""
    counted = [r for r in lines if r["status"] == "counted" and r["cell"] in ("open", "closed")]
    strata = [("all", "all", lambda r: True)]
    strata += [("depth", s, lambda r, s=s: r["depth_stratum"] == s) for s in (*DEPTHS, "above -5")]
    strata += [("pi", s, lambda r, s=s: r["pi_stratum"] == s) for s in PI_BANDS]
    out = []
    for kind, name, keep in strata:
        part = [r for r in counted if keep(r)]
        if kind != "all" and name == "above -5" and not part:
            continue
        for measure, basis, col in (("m1", "gross", None), ("m1", "net", None), ("m1c", "gross", "m1c"),
                                    ("m1c", "net", "m1c_net"), ("m2", "gross", "m2"), ("m2", "net", "m2_net")):
            vals = {side: [float(r[col]) for r in part if r["cell"] == side and col and r[col] != ""]
                    for side in ("open", "closed")}
            o, c = vals["open"], vals["closed"]
            out.append({
                "variant": variant, "stratum_kind": kind, "stratum": name, "measure": measure, "basis": basis,
                "n_open": len(o), "n_closed": len(c),
                "mean_open": num(statistics.fmean(o)) if o else "", "median_open": num(statistics.median(o)) if o else "",
                "mean_closed": num(statistics.fmean(c)) if c else "",
                "median_closed": num(statistics.median(c)) if c else "",
                "open_minus_closed": num(statistics.fmean(o) - statistics.fmean(c)) if o and c else "",
                "blind_spot": BLIND_SPOT[measure]})
    return out


# --- the readers of the frozen files --------------------------------------------------------------------------------

def excel_date(serial: float) -> date:
    return date(1899, 12, 30) + timedelta(days=int(serial))


MONTHS = {m: i for i, m in enumerate(("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), 1)}


def freeze_years(start: float | str | None, months: float | None, next_year: float | None = None) -> set[int]:
    """K4: the years a freeze covers, from the start year to the year of start + duration; empty when the date cannot be
    read. ``start`` is an Excel serial, a bare year, or text 'D-Mon-' whose year is ``next_year`` (Lebanon)."""
    if isinstance(start, float) and start >= 3000:
        d = excel_date(start)
        y, mo = d.year, d.month
    elif isinstance(start, float) and 1800 <= start <= 2100:
        y, mo = int(start), 1
    elif isinstance(start, str) and next_year is not None and (mm := re.search(r"([A-Za-z]{3})", start)) and \
            mm.group(1).lower() in MONTHS:
        y, mo = int(next_year), MONTHS[mm.group(1).lower()]
    else:
        return set()
    end_y = y + (mo - 1 + int(months or 0)) // 12
    return set(range(y, end_y + 1))


def parse_freezes(rows: list[list]) -> tuple[dict[str, set[int]], list[str]]:
    """({country name: freeze years}, rows whose date cannot be read) from the sheet ``Resolution Details``."""
    head = next(i for i, r in enumerate(rows) if r and r[0] == "Country")
    col = next(j for j, v in enumerate(rows[head]) if isinstance(v, str) and v.strip() == "Deposit Freeze")
    out: dict[str, set[int]] = defaultdict(set)
    bad: list[str] = []
    for i in range(head + 1, len(rows)):
        r = rows[i]
        if not r or not r[0] or len(r) <= col or r[col] is None or str(r[0]).startswith(("Source", "1/", "2/")):
            continue
        nxt = rows[i + 1] if i + 1 < len(rows) else []
        next_year = nxt[col] if len(nxt) > col and not nxt[0] and isinstance(nxt[col], float) else None
        months = r[col + 1] if len(r) > col + 1 and isinstance(r[col + 1], float) else None
        years = freeze_years(r[col], months, next_year)
        if years:
            out[str(r[0]).strip()] |= years
        else:
            bad.append(str(r[0]).strip())
    return dict(out), bad


def read_freezes() -> tuple[dict[str, set[int]], list[str]]:
    """{money: freeze years}; the names economies.py does not know and the rows whose date cannot be read."""
    import economies
    import xlsx
    by_name, bad = parse_freezes(xlsx.rows(FREEZE_FILE, FREEZE_SHEET))
    out: dict[str, set[int]] = defaultdict(set)
    for name, years in by_name.items():
        try:
            out[economies.code(name)] |= years
        except KeyError:
            bad.append(f"unmapped: {name}")
    return dict(out), bad


def read_contiguity(primary: dict[tuple[int, int], str]) -> tuple[dict[tuple[str, int], set[str]], list[tuple[int, int]]]:
    """{(money, year): land neighbours} from the directed dyad-year file (conttype 1), both directions; the
    (ccode, year) pairs the state system does not map."""
    import io
    with zipfile.ZipFile(CONTIGUITY_ZIP) as z:
        text = z.read(CONTIGUITY_CSV).decode("latin-1")
    out: dict[tuple[str, int], set[str]] = defaultdict(set)
    missing: set[tuple[int, int]] = set()
    for r in csv.DictReader(io.StringIO(text)):
        if r["conttype"].strip() != "1":
            continue
        year = int(r["year"])
        a, b = int(r["state1no"]), int(r["state2no"])
        ma, mb = primary.get((a, year)), primary.get((b, year))
        for ccode, mm in ((a, ma), (b, mb)):
            if mm is None:
                missing.add((ccode, year))
        if ma and mb:
            out[(ma, year)].add(mb)
            out[(mb, year)].add(ma)
    return dict(out), sorted(missing)


def irr_by_year(records: dict[str, dict]) -> dict[str, dict[int, int]]:
    """money -> year -> the fine class, within the country's start and end years and a valid value (as panel.class_at)."""
    out: dict[str, dict[int, int]] = {}
    for m, rec in records.items():
        s, e = rec.get("start"), rec.get("end")
        years = {}
        for y, v in rec["classes"].items():
            if s is None or e is None or not s <= y <= e:
                continue
            if isinstance(v, float) and v == int(v) and 1 <= v <= 15:
                years[y] = int(v)
        out[m] = years
    return out


def bop_levels(code: str) -> dict[str, dict[int, float]]:
    """A BOP annual series by money, times its multiplier (the same DBnomics layout as ``panel.ifs_levels``)."""
    import panel as P
    folder = f"BOP/A~~{code}"
    raw, mult = P._dbnomics(folder), P._dbnomics_mult(folder)
    out: dict[str, dict[int, float]] = {}
    for area, series in raw.items():
        money = P.area_money(area, f"BOP {code}")
        if money:
            for p, (v, _) in series.items():
                out.setdefault(money, {}).setdefault(int(p), v * mult.get(area, 1.0))
    return out


def read_areaer(path: Path | None = None) -> dict[tuple[str, int], str] | None:
    """K27: {(money, year): 'permitted' | 'not permitted'} from the AREAER transcription table (section 16), or None when
    the file does not exist (the variant is then not written). *permitted with conditions* is read as *permitted*; *not
    printed* rows are left out (the headline's reading stands there, as for a year not in the table). A status that is not
    one of the four, or a money-year with two different readings, raises."""
    path = path or AREAER_FILE
    if not path.exists():
        return None
    out: dict[tuple[str, int], str] = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            status = (r.get("status") or "").strip().lower()
            if status not in AREAER_STATUSES:
                raise ValueError(f"{path.name}: {r.get('money')} {r.get('year')}: status {r.get('status')!r} is not one of "
                                 f"{', '.join(AREAER_STATUSES)}")
            if status == "not printed":
                continue
            key = (r["money"].strip(), int(r["year"]))
            read = "not permitted" if status == "not permitted" else "permitted"
            if out.setdefault(key, read) != read:
                raise ValueError(f"{path.name}: {key[0]} {key[1]} is given two different readings")
    return out


def sources() -> dict:
    """Every input, from the frozen series; nothing is computed from them here but the real log currency (as the
    phases list) and the dollar GDP (K19: IFS NGDP_XDC, then the World Bank's NY.GDP.MKTP.CN where it agrees; K20: over the
    year average of the monthly ENDE, all twelve months read)."""
    sys.path.insert(0, str(HERE))
    import panel as P
    import phases
    import war
    import window_a as W
    from frame_a import EURO_ENTRY
    pan = P.Panel()
    rate = W.ifs_level_by_money("FIDR_PA", "A")
    ngdp, ende_m = W.ifs_level_by_money("NGDP_XDC", "A"), W.ifs_level_by_money("ENDE_XDC_USD_RATE", "M")
    wbgdp = P.worldbank(WB_GDP)
    fdsbc, l14a, cpi_all = (W.ifs_level_by_money(c, "A") for c in ("FDSBC_XDC", "14A___XDC", "PCPI_IX"))
    bop = {c: bop_levels(f"{c}_BP6_USD") for c in (*ASSETS, DERIVATIVES, "BOP")}
    freezes, freeze_bad = read_freezes()
    primary, _, _ = war._states()
    contiguity, contiguity_missing = read_contiguity(primary)
    ka = P.ka_open()
    datas, gdp_rejected, units_breaks = [], {}, {}
    for m in sorted(rate):
        survey = {t: (v, "FDSBC") for t, v in fdsbc.get(m, {}).items()}
        cur = W.merge_sources(survey, W.before(l14a.get(m, {}), min(survey) if survey else None, "14A"))
        real = phases.log_money(cur, cpi_all.get(m, {}), True)
        bad = phases.glitches(real)
        parts = {k: bop[k].get(m, {}) for k in (*ASSETS, DERIVATIVES)}
        parts["NEO"] = bop["BOP"].get(m, {})
        gdp, gdp_flags, why = gdp_lcu(ngdp.get(m, {}), wbgdp.get(m, {}))
        if why:
            gdp_rejected[m] = why
        gdp_usd, dropped, breaks = units_screen(gdp_usd_of(gdp, year_average(ende_m.get(m, {}))))
        if breaks:
            units_breaks[m] = breaks
        datas.append(MoneyData(
            money=m, rate=rate[m],
            pi={y: v for y, (v, _, _) in pan.pi_annual(m).items()} if m in pan.monies else {},
            freeze=freezes.get(m, set()), ka=ka.get(m, {}),
            lm={y: v for y, v in real.items() if y not in bad}, bop=parts,
            gdp_usd=gdp_usd, gdp_flags={y: f for y, f in gdp_flags.items() if y in gdp_usd}, gdp_dropped=dropped))
    world = World(contiguity=contiguity, classes=irr_by_year(P.irr_classes()), anchors=P.irr_anchors(),
                  euro_entry={m: int(d[:4]) for m, d in EURO_ENTRY.items()}, war=lambda m, y: P.war_at(m, y),
                  war_before_w12=lambda m, y: P.war_at(m, y, ucdp=False))
    have_lm: dict[int, set[str]] = defaultdict(set)
    have_m2: dict[int, set[str]] = defaultdict(set)
    for md in datas:
        for y in md.lm:
            have_lm[y].add(md.money)
        for y in set(md.bop.get("NEO", {})):
            if outflow(md.bop, y) is not None:
                have_m2[y].add(md.money)
    ends = {"m1c": P.common_end(have_lm, 1) or 0, "m2": P.common_end(have_m2, 1) or 0}
    return {"datas": datas, "world": world, "ends": ends, "freeze_bad": freeze_bad,
            "contiguity_missing": contiguity_missing, "gdp_rejected": gdp_rejected,
            "units_breaks": units_breaks}


def freeze_removed(datas: list[MoneyData], spec: Spec = HEADLINE) -> list[tuple[str, int, float]]:
    """K23: the money-years below the line that a deposit freeze removed (money, year, real return): the years whose
    deposit rate and pi are both read, whose return is below the line, and that a freeze made unreadable."""
    out = []
    for md in datas:
        free = real_returns(md.rate, md.pi, set(), spec.fisher)
        out += [(md.money, y, round(free[y], 2)) for y in sorted(md.freeze) if y in free and free[y] < spec.line]
    return out


#: K23: how Argentina 1989's freeze was read (the audit's M3).
ARGENTINA_1989 = ("Laeven and Valencia's sheet gives a deposit freeze from 28 December 1989 lasting 120 months; K4 reads "
                  "it as written, the years 1989 to 1999 inclusive. The 120 months are the audit's likely reading of the "
                  "Bonex bonds' maturity, a conjecture the sheet does not state.")


def argentina_reading(datas: list[MoneyData]) -> dict:
    """K23: Argentina's 1989 freeze years, and how many of them hold a deposit rate (those years leave no run)."""
    arg = next((d for d in datas if d.money == "ARG"), None)
    if arg is None:
        return {"reading": ARGENTINA_1989, "freeze_years": [], "years_with_a_deposit_rate": 0}
    years = sorted(y for y in arg.freeze if 1989 <= y <= 1999)
    return {"reading": ARGENTINA_1989, "freeze_years": years, "years_with_a_deposit_rate": sum(y in arg.rate for y in years),
            "first_deposit_rate_year": min(arg.rate, default=None)}


def coverage(src: dict, sha: str) -> dict:
    """Section 7: the entries by year and status, the cells and their reasons, the sources' coverage per measure. No measure
    is computed or printed."""
    rows = lines_for(src["datas"], src["world"], HEADLINE, "headline", sha, src["ends"], values=False)
    by_year: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        by_year[r["entry_date"]][r["status"]] += 1
    datas = src["datas"]
    return {
        "entries": len(rows), "entries_by_year": {y: dict(c) for y, c in sorted(by_year.items())},
        "by_status": dict(Counter(r["status"] for r in rows)),
        "cells": dict(Counter(r["cell"] for r in rows)),
        "cell_reasons": dict(Counter(r["reason"] for r in rows if r["status"] != "counted")),
        "forced": dict(Counter(r["forced"] for r in rows)), "border": dict(Counter(r["border"] for r in rows)),
        "money_years": {
            "deposit rate": sum(len(d.rate) for d in datas), "pi": sum(len(d.pi) for d in datas),
            "real return": sum(len(real_returns(d.rate, d.pi, d.freeze)) for d in datas),
            "freeze years": sum(len(d.freeze) for d in datas), "ka_open": sum(len(d.ka) for d in datas),
            "real currency (m1c)": sum(len(d.lm) for d in datas),
            "outflow read (m2)": sum(1 for d in datas for y in d.bop.get("NEO", {}) if outflow(d.bop, y) is not None),
            "GDP in dollars": sum(len(d.gdp_usd) for d in datas),
            "GDP in dollars from the World Bank": sum(1 for d in datas for y in d.gdp_usd if "gdp_worldbank" in d.gdp_flags.get(y, ()))},
        "gdp_worldbank_rejected": src.get("gdp_rejected", {}),
        "gdp_units_breaks": src.get("units_breaks", {}),
        "ends": src["ends"], "freeze_unread": src["freeze_bad"], "contiguity_unmapped": len(src["contiguity_missing"]),
        "own_money": dict(Counter(r["own_money"] for r in rows)), "war_at_entry": dict(Counter(r["war_at_entry"] for r in rows)),
        "freeze_removed": freeze_removed(datas), "argentina_1989": argentina_reading(datas),
        "regime_ends": {"contiguity": src["world"].contiguity_end, "classes": src["world"].class_end,
                        "anchors": src["world"].anchor_end},
        "dollar_euro": dollar_euro_rows(src["world"])}


WAR_MOVE_FIELDS = ("war_at_entry",)         # what ``war-moves.csv`` compares (K26)


def write(path: Path, rows: list[dict], fields: list[str]) -> None:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def build(go: bool = False) -> dict:
    sys.path.insert(0, str(HERE))
    import m0
    sha = m0.require_locked()
    src = sources()
    report = {"coverage": coverage(src, sha)}
    if not go:
        return report
    OUT.mkdir(parents=True, exist_ok=True)
    head = lines_for(src["datas"], src["world"], HEADLINE, "headline", sha, src["ends"])
    write(OUT / "dollar-euro.csv", dollar_euro_rows(src["world"]), DE_FIELDS)
    write(OUT / "series.csv", head, FIELDS)
    write(OUT / "shown.csv", shown_rows(head), SHOWN_FIELDS)
    report["headline"] = dict(Counter(r["status"] for r in head))
    report["variants"], shown = {}, []
    areaer = read_areaer()                                   # K27: read for the variant areaer only
    for name, spec in VARIANTS.items():
        world = src["world"]
        if spec.areaer:
            if areaer is None:
                where = AREAER_FILE.relative_to(ROOT).as_posix() if AREAER_FILE.is_relative_to(ROOT) else str(AREAER_FILE)
                report["areaer"] = f"not written: {where} does not exist"
                print(f"variant areaer not written: {where} does not exist", file=sys.stderr)
                continue
            world = replace(world, areaer=areaer)
            report["areaer"] = dict(Counter(areaer.values()))
        rows = lines_for(src["datas"], world, spec, name, sha, src["ends"])
        write(OUT / f"variant-{name}.csv", rows, FIELDS)
        shown += shown_rows(rows, name)
        report["variants"][name] = dict(Counter(r["status"] for r in rows))
        if name == "war-before-w12":                         # section 15: the move W12 made, line by line
            import panel as P
            moves = P.war_moves(head, rows, WAR_MOVE_FIELDS)
            P.write_war_moves(OUT / "war-moves.csv", moves)
            report["war_moves"] = {"lines": len(moves), "status": dict(Counter(f"{x['status_before']} -> {x['status_after']}"
                                                                                for x in moves))}
    write(OUT / "shown-variants.csv", shown, SHOWN_FIELDS)
    return report


if __name__ == "__main__":
    if sys.argv[1:2] == ["build"]:
        import json
        print(json.dumps(build(go="--go" in sys.argv), indent=1, default=str))
    else:
        print(__doc__)
        sys.exit(2)
