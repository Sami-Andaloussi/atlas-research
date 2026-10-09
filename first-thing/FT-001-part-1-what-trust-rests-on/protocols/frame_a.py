"""FT-001 M4, frame a, panel 3: Garriga's legal reforms, up and down, by script (FT-001-M4-frame-a.md, sections 4, 6, 8).

Every country-year of Garriga (2025), ``garriga/cbi`` (``Replication_ISQ_2025.tab``, 1970-2023), with ``reform`` = 1:
``direction`` 1 is route ``a3-up``, -1 ``a3-down``, 0 ``a3-neither`` (set apart: the DDI gives the flag from -1 to 1);
the two sub-panels are never pooled (P14). ``direction`` decides where it disagrees with ``increase`` / ``decrease``
(M0 names it; the clash is printed and flagged). A ``creation`` without a ``reform`` is no change (noted in the
coverage). A country-year she leaves empty is *cannot be read* (the coverage), never "no reform".

**Columns.** Only the ten the protocol names are kept, chosen by name from the header before any row is read
(:data:`READ`); the columns it says never to read (:data:`NEVER`: the inflation, GDP, unemployment, openness,
regime and lagged-inflation columns the file carries beside the flags) are never indexed, stored, printed or
loaded, and a test fails if one ever enters :data:`READ`.

**Status** (section 6, as far as a script can set it now): a change in 1970-72 is *apart* (its window starts before
her record); direction 0 is *apart*; a union member's own statute is *apart*; a **war year at entry** (``war.py``)
is *apart*, told; a war year that *cannot be read* stays counted and is flagged (P23); a national reform of a
future euro member whose window (year to year + 5) holds the member's entry into the euro is *ended unbroken* with
its ``exit``; two changes of one money within one window are each flagged ``overlap`` (P26). The build sets the
rest (censoring; the run rule does not apply to reforms, P24; no price in the year - 3).

**Readings** frame_a makes, in the open, for the audit (the protocol's P14-P16 and P23 are not repeated):

A1. *Union members by year.* The euro area is ``EMU`` and its members are the economies in :data:`EURO_ENTRY` from
    their entry year (whatever ``regional`` says, P15). ``XOF``, ``XAF`` and ``XCD`` (the CFA franc of West and
    Central Africa, the East Caribbean dollar) take as members, in a year, the economies of :data:`UNIONS` whose
    row that year has ``regional`` = 1. ``regional`` = 1 on an economy in no union is printed.
A2. *"Every member".* A union's reform needs at least two members with a readable ``reform`` cell in the year, **all
    of which** have ``reform`` = 1 with the same ``direction``; a member with an empty cell is left out of the
    count and named in the note. Fewer than two readable members, or any member not reforming in that direction,
    makes each reforming member's reform its own statute: *apart*, money = the member's, the union's named in the
    note. Garriga has no row of her own for a union's central bank.
A3. *Euro entry dates.* :data:`EURO_ENTRY` holds each economy's entry year into the euro area as the European
    Central Bank prints it ("Euro since YYYY", frozen at ``frame-a/ecb-euro-area-members``, 2026-09-30), dated
    1 January of that year (the page gives years only): year precision. Whether each entry was "announced at least 12 months before" (M0 section 4) is read as yes for all
    (the Maastricht treaty obliged every member to join), and the test of "no crossing of the break line in the 12
    months before" is frame b's: not read here.
A4. *A competing exit is tested only for national lines of future members*: a line of the money's own code
    dated before its entry year and no more than 5 years before it. A reform in the entry year or after is the
    union's (A1).
A5. *Overlap and responses.* Two changes of one money (up or down, a union's own included; direction 0 excluded)
    overlap when the later is no more than 5 years after the earlier (the earlier's window holds the later); both are
    flagged, each naming the other. ``responses`` lists the later ones inside the window (year + 1 to year + 5),
    ``type:date``, the type the route.
A6. *The index variant* (``a3-var-index``): every year in which ``lvau_garriga`` differs from the year before
    by 0.05 or more (up or down; a rounding of 1e-9 absorbed), both read; one line per economy (never a union's),
    *apart*, ``headline`` no, with its war year. A union's members are each a line.
A8. *A union's war year* is yes if a member's is (the member named), no if every member's is, and otherwise
    *cannot be read* - so a union with a member that is no state (Anguilla, Montserrat) or a member the sources
    cannot read stays *cannot be read* and its line is counted, flagged (P23).
A7. *Headline.* ``headline`` = ``yes`` for every line that is not a variant and not *apart*
    (*counted*, *ended unbroken*, *cannot be read*).

**The hand-coded panels and the list** (:func:`build_all`; FT-001-M4-frame-a.md, sections 1, 6, 8, 12). The first
coder's files (``lines.csv``, ``members.csv``) become ``series.csv`` and ``members.csv`` beside panel 3; the second
coder's recode of the draw becomes ``agreement.json``; both coders' files are archived beside the list.

H1. *A member whose change cannot be dated is "cannot be read", never "no change"* (section 1: "a member whose change
    cannot be dated at all has no line in ``series.csv`` and is *cannot be read* in ``members.csv``"). This is the
    reading that fixes the two coders' labels of Romania in panel 1: the first coder wrote *cannot be read* (a member
    of the exit source whose 1914-15 suspension no dating source dates), the second wrote *yes* and said in the same
    row that the change cannot be dated. Section 1 settles it in the first coder's favour: :func:`settle_member`
    turns such a *yes* into *cannot be read*, and :func:`agreement` counts the pair as a disagreement of label
    (``kind`` = ``labelling``, ``settled_in_favour_of`` = ``a1``), with kappa printed both as coded and after the
    settlement. A member that *has* a line is never turned; a member with no line whose row says nothing of the
    kind stays a member with no change (the United States and Japan in panel 1).
H2. *Statuses set now* (section 6, :func:`hand_status`): a variant line is *apart* (route ``<route>-var-<variant>``,
    ``headline`` no); a war year at entry is *apart*, told; a panel 2 exit before 1 January 1931 is *apart* (P13); a
    war year that cannot be read leaves the line counted and flagged (P23); a line carrying an ``exit`` is *ended
    unbroken*. Everything else is *counted*. ``headline`` = ``yes`` for a line that is not a variant and not *apart*
    (A7's rule, as panel 3's). The run, censoring and price-record statuses are the window build's (P24, P25), never
    set here. Two changes of one panel in one money (P26) cannot occur in the hand panels (one change per money).
H3. *The archive* copies each coder's top-level ``.csv``, ``.md`` and ``.json`` files (no script: BLUEPRINT §7); the page images and
    text extracts of the frozen documents they worked from (``img/``, ``txt/``, ``*.txt``, ``*.png``) are not
    copied: the workshop never commits a document's text.
H5. *P11's variant by source* (:func:`irr_lines`, :func:`irr_members`): the first coder's ``panel2-irr-variant.csv``
    (economies outside Bernanke and James's table whose chronology, Ilzetzki, Reinhart and Rogoff, w23135, records a
    gold standard suspended in 1931-36 while a gold peg stood at 31 December 1929) gives one line per row whose
    ``gold_peg_stood_end_1929`` is *yes* and which has an exit date: route ``a2-var-irr``, ``headline`` no, status
    *apart*, the date and the quotation as the coder gave them, the war year and P13 applied as to every hand line.
    Every row is a candidate of the variant in ``members.csv``, panel label ``2-irr`` (*yes*, *no* or *cannot be
    read* as the coder wrote it; a *cannot be read* such as Egypt, whose table begins after 1929, has no line).
H6. *P12 amended* (section 13, the audit's O2; :func:`p12_amended`): panel 2's headline exit is the first of suspension
    and devaluation (M0 section 2: force imposed is never an act of this list); Bernanke and James's note 7, the first
    of the three dates, is the variant ``a2-var-bj-note7`` (apart). The first coder coded both: its headline rows are
    note 7's, its ``susp-dev-only`` variant rows are the amended headline. They are swapped **by rule in the build**,
    never in the coder's files. A member whose only change in 1931-36 is an exchange control has no headline exit: it
    stays a member with no change in the span (its dates are read: not *cannot be read*), and its note-7 line is the
    variant's. The three ``bj_*`` columns are kept on every panel-2 line. ``responses`` are recomputed from them (the
    dates later than the exit); a date earlier than the headline exit is not a response (the line check refuses one)
    and is told in ``flags``. The agreement keeps comparing the coders' own headline lines, panel 2's being note 7's
    (what both coded): the amendment is a rule of the build, not a recode.
H7. *B1 and P19* (section 13; :func:`from2012_members`, :func:`hand_problems`): Cobham's four-category list and its
    full-only list are variants "conditioned on behaviour" in ``members.csv`` (panels ``4-from-2012-var-cobham-four`` and
    ``-full``), each candidate *cannot be read*. Finland, Spain and Slovakia stay *cannot be read* by "announcement not frozen"
    alone: ``hand_problems`` refuses a line or a label for them that would be a fallback (no Cobham date).
H9. *Panel 4 from 2012 is AREAER's list* (sections 14 and 17; :func:`from2012_members`, :func:`areaer_problems`,
    :func:`hand_problems`): the headline panel ``4-from-2012`` of ``members.csv`` is the 18 candidates of the frozen
    ``ft001-a-areaer`` list (R-A3), each *yes* (an adopter: its central bank's own announcement states an explicit numerical
    inflation target as the anchor, R-A4), *no* (not an adopter in what is frozen) or *cannot be read*; ``areaer_problems``
    refuses a first coder's file whose ``4-from-2012`` panel is not exactly those 18. An adopter has one headline line
    (panel ``4``, route ``a4``, the announcement's own date, never the edition's year, R-A4), dated from 2012; a *yes* with
    no line, a line for a candidate that is not *yes*, a candidate of both panels ``4`` and ``4-from-2012`` (a money listed
    in 2011 is a targeter already, R-A3) are refused. The later or transition documents (section 17) are variant lines of
    panel ``4`` (variant ``later-or-transition-documents``, headline *no*, status *apart*) beside their *cannot be read*
    headline members. Cobham's four-category candidates (the first coder's ``4-from-2012-var-cobham-four`` rows, checked by
    :func:`cobham_problems` against ``panel4-from2012-cobham.csv``) and its full-only list stay the variants of H7.
H8. *M1*: ``agreement.json`` and the build's summary name the protocol commit they were coded under
    (:func:`protocol_commit`, ``git log -1 --format=%h`` of the protocol; refused when the protocol is uncommitted).
H4. *Agreement* compares the **headline** lines of a sampled candidate (a coder's ``headline`` = ``yes``; variant
    lines are not compared), at the source's own precision (``1914`` and ``1914-08`` differ).

Run from the workshop's root with the toolkit's interpreter::

    toolkit/.venv/bin/python bank/maps/FT-001/missions/code/frame_a.py count
    toolkit/.venv/bin/python bank/maps/FT-001/missions/code/frame_a.py build <first coder's folder>   # writes the list

``panel3()`` returns ``(rows, coverage)`` and writes nothing: the list is built later with the hand-coded panels
(``data/reconstructed/ft001-a/``), ``rules_sha256`` set by :func:`m0.require_locked`.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import economies  # noqa: E402
import m0  # noqa: E402
import war  # noqa: E402

ROOT = HERE.parents[4]
VINTAGE = "2026-09-30"
GARRIGA = ROOT / "data" / "garriga" / "cbi" / VINTAGE / "Replication_ISQ_2025.tab"
SOURCE = f"Garriga (2025), central bank independence data (garriga/cbi {VINTAGE}, Replication_ISQ_2025.tab)"
CODER = "script: missions/code/frame_a.py"
FIRST_RECORD_YEAR = 1970
LAST_RECORD_YEAR = 2023
WINDOW_AFTER = 5

#: The columns the protocol names (section 4), selected by name before any row is read.
READ = ("cname", "ISO", "year", "reform", "direction", "increase", "decrease", "creation", "regional",
        "lvau_garriga")
#: The columns it says never to read: the file carries inflation and its controls beside the flags.
NEVER = ("InflationCP", "InflationGDPdeflator", "linf", "inf_imp", "inf_ln", "GDPpc", "unemp_imp", "ka_open",
         "wdi_trade", "p_polity2", "ldv")
assert not set(READ) & set(NEVER), "a column the protocol forbids is among those read"

FIELDS = ["period", "value", "unit", "source", "locator", "note", "uncertainty", "money", "frame", "route", "support",
          "headline", "act", "entry_date", "entry_measure", "entry_measure_date", "outcome", "outcome_date",
          "onset_date", "responses", "exit", "status", "war_year", "flags", "bj_suspension", "bj_exchange_control",
          "bj_devaluation", "informal_start", "applied_from", "coder", "rules_sha256"]
COVERAGE_FIELDS = ["money", "act", "source", "first_year", "last_year", "years_empty", "creation_without_reform",
                   "names", "note"]
SUPPORT = "limit by institution"

#: The economies' entry into the euro area (A3); the euro is one money from 1999-01-01 (M0 section 1).
EURO_ENTRY = {"AUT": "1999-01-01", "BEL": "1999-01-01", "FIN": "1999-01-01", "FRA": "1999-01-01",
              "DEU": "1999-01-01", "IRL": "1999-01-01", "ITA": "1999-01-01", "LUX": "1999-01-01",
              "NLD": "1999-01-01", "PRT": "1999-01-01", "ESP": "1999-01-01", "GRC": "2001-01-01",
              "SVN": "2007-01-01", "CYP": "2008-01-01", "MLT": "2008-01-01", "SVK": "2009-01-01",
              "EST": "2011-01-01", "LVA": "2014-01-01", "LTU": "2015-01-01", "HRV": "2023-01-01",
              "BGR": "2026-01-01"}
EURO_EXIT_SOURCE = ("the European Central Bank, 'Our money', each member's 'Euro since' year "
                    "(frame-a/ecb-euro-area-members 2026-09-30)")
#: Unions other than the euro (ISO 4217 codes); members in a year are the rows with ``regional`` = 1 (A1).
UNIONS = {
    "XOF": ("West African Economic and Monetary Union (BCEAO)",
            ("BEN", "BFA", "CIV", "GNB", "MLI", "MRT", "NER", "SEN", "TGO")),
    "XAF": ("Central African Economic and Monetary Community (BEAC)", ("CMR", "CAF", "TCD", "COG", "GNQ", "GAB")),
    "XCD": ("Eastern Caribbean Currency Union (ECCB)", ("AIA", "ATG", "DMA", "GRD", "KNA", "LCA", "MSR", "VCT")),
}
UNION_OF = {m: u for u, (_, members) in UNIONS.items() for m in members}

R_NEITHER = "reform, neither up nor down"
R_STATUTE = "a member's statute; the money is the union's"
R_BEFORE = "window starts before Garriga's record (1970): a change in 1970-72"
R_WAR = "war year at entry: told"
R_VARIANT = "variant: the index moved by 0.05 or more"


# --- reading Garriga ---------------------------------------------------------------------------------------

def read_rows(path: Path = GARRIGA):
    """The file's rows, each reduced to the columns of :data:`READ`; the others are never indexed."""
    with open(path, newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        at = {name: header.index(name) for name in READ}     # by name, before any row is read
        for raw in reader:
            yield {name: raw[i].strip().strip('"') for name, i in at.items()}


def _num(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None


def _flag(row: dict, name: str) -> int | None:
    value = _num(row[name])
    return None if value is None else int(round(value))


def _moneys(rows) -> tuple[dict[str, dict[int, dict]], list[dict]]:
    """Garriga's rows by money and year; a name with no code is listed and printed, never dropped."""
    iso2 = {e["iso2Code"]: e["id"] for e in json.loads(economies.WB.read_text())[1]
            if e["region"]["value"] not in ("", "Aggregates")}
    by: dict[str, dict[int, dict]] = defaultdict(dict)
    unmatched: dict[tuple[str, str], list[int]] = defaultdict(list)
    for row in rows:
        year = int(float(row["year"]))
        money = iso2.get(row["ISO"])
        if money is None:
            try:
                money = economies.code(row["cname"])
            except KeyError:
                unmatched[(row["cname"], row["ISO"])].append(year)
                continue
        if year in by[money]:
            raise ValueError(f"Garriga: {money} {year} held twice ({by[money][year]['cname']}, {row['cname']})")
        by[money][year] = row
    lost = [{"cname": c, "ISO": i, "years": sorted(y)} for (c, i), y in sorted(unmatched.items())]
    for u in lost:
        print(f"Garriga name with no economy code: {u['cname']!r} (ISO {u['ISO'] or 'none'}), years "
              f"{u['years'][0]}-{u['years'][-1]}: kept out of the lines, listed in the coverage", file=sys.stderr)
    return dict(by), lost


# --- lines -------------------------------------------------------------------------------------------------

def line(money: str, route: str, year: int, *, value, unit: str, locator: str, act: str, note: str, status: str,
         war_year: str, flags: list[str], headline: bool, uncertainty: str = "clear", responses: str = "",
         exit: str = "") -> dict:
    """One change of panel 3 as a line of the reconstructed dataset (columns of FT-001-M4 section 1)."""
    return {"period": str(year), "value": value, "unit": unit, "source": SOURCE, "locator": locator, "note": note,
            "uncertainty": uncertainty, "money": money, "frame": "a", "route": route, "support": SUPPORT,
            "headline": "yes" if headline else "no", "act": act, "entry_date": str(year), "entry_measure": "",
            "entry_measure_date": "", "outcome": "", "outcome_date": "", "onset_date": "", "responses": responses,
            "exit": exit, "status": status, "war_year": war_year, "flags": "; ".join(flags), "bj_suspension": "",
            "bj_exchange_control": "", "bj_devaluation": "", "informal_start": "", "applied_from": "",
            "coder": CODER, "rules_sha256": ""}


def _route(direction: int | None) -> str:
    return {1: "a3-up", -1: "a3-down", 0: "a3-neither"}.get(direction, "a3-unread")


def _member_year(money: str, year: int, row: dict) -> str | None:
    """The union a money belongs to in the year (A1), or None."""
    if money in EURO_ENTRY:
        return "EMU" if year >= int(EURO_ENTRY[money][:4]) else None
    if money in UNION_OF and _flag(row, "regional") == 1:
        return UNION_OF[money]
    return None


def _union_war(members: list[str], year: int, war_year_fn: Callable[[str, int], str]) -> str:
    """A union's money has no state: its war year is yes if a member's is, no if every member's is, else unread."""
    results = {m: war_year_fn(m, year) for m in members}
    yes = [f"{m}: {r[5:]}" for m, r in results.items() if r.startswith("yes")]
    if yes:
        return "yes: " + "; ".join(yes)
    return "no" if all(r == "no" for r in results.values()) else "cannot be read"


def _collapse(years: list[int]) -> str:
    runs, start, prev = [], None, None
    for y in sorted(years):
        if start is None:
            start = prev = y
        elif y == prev + 1:
            prev = y
        else:
            runs.append((start, prev))
            start = prev = y
    if start is not None:
        runs.append((start, prev))
    return ";".join(str(a) if a == b else f"{a}-{b}" for a, b in runs)


def build(rows, *, war_year_fn: Callable[[str, int], str] = war.war_year, sha: str = "") -> tuple[list[dict], list[dict], dict]:
    """Panel 3 from Garriga's rows (each a dict of :data:`READ`): its lines, its coverage rows and the notes
    (``unmatched``, ``clashes``, ``unions``, ``regional`` outside a union)."""
    by, unmatched = _moneys(rows)
    notes: dict = {"unmatched": unmatched, "clashes": [], "unions": [], "regional_outside": [],
                   "apart_reasons": Counter()}
    events: dict[tuple[str, int], dict] = {}     # (money, year) -> a national change (kind: national | member)
    union_events: list[dict] = []

    def cname(m: str, y: int) -> str:
        return by[m][y]["cname"]

    # 1. each reform, and its direction
    reforms: dict[tuple[str, int], dict] = {}
    for money, years in by.items():
        for year, r in years.items():
            if _flag(r, "regional") == 1 and money not in UNION_OF and money not in EURO_ENTRY:
                notes["regional_outside"].append((money, year))
            if _flag(r, "reform") != 1:
                continue
            direction = _flag(r, "direction")
            inc, dec = _flag(r, "increase"), _flag(r, "decrease")
            clash = None
            if None not in (direction, inc, dec):
                expected = {1: (1, 0), -1: (0, 1)}.get(direction)
                if expected is not None and (inc, dec) != expected:
                    clash = f"direction {direction} but increase {inc}, decrease {dec}"
                if direction == 0 and inc != dec:
                    clash = f"direction 0 but increase {inc}, decrease {dec}"
            if clash:
                notes["clashes"].append((money, year, clash))
            reforms[(money, year)] = {"direction": direction, "clash": clash}

    # 2. unions: a reform on every readable member, same direction, is one change of the union's money (P15, A2)
    in_union: dict[tuple[str, int], str] = {}
    for money, years in by.items():
        for year, r in years.items():
            u = _member_year(money, year, r)
            if u:
                in_union[(money, year)] = u
    union_years = {(u, y) for (m, y), u in in_union.items()}
    absorbed: set[tuple[str, int]] = set()
    for u, year in sorted(union_years, key=lambda t: (t[1], t[0])):
        members = [m for (m, y), uu in in_union.items() if y == year and uu == u]
        readable = [m for m in members if _flag(by[m][year], "reform") is not None]
        unread = sorted(set(members) - set(readable))
        for d in (1, -1):
            reforming = [m for m in readable if _flag(by[m][year], "reform") == 1
                         and reforms[(m, year)]["direction"] == d]
            if len(readable) >= 2 and reforming and len(reforming) == len(readable):
                absorbed |= {(m, year) for m in reforming}
                union_events.append({"union": u, "year": year, "direction": d, "members": sorted(readable),
                                     "unread": unread})
    notes["unions"] = [(e["union"], e["year"], e["direction"], e["members"]) for e in union_events]

    # 3. the changes
    changes: list[dict] = []
    for e in union_events:
        names = ", ".join(f"{cname(m, e['year'])} ({m})" for m in e["members"])
        label = "the euro area" if e["union"] == "EMU" else UNIONS[e["union"]][0]
        clash = [reforms[(m, e["year"])]["clash"] for m in e["members"] if reforms[(m, e["year"])]["clash"]]
        changes.append({
            "money": e["union"], "year": e["year"], "direction": e["direction"], "kind": "union",
            "members": e["members"], "war": _union_war(e["members"], e["year"], war_year_fn),
            "locator": f"Replication_ISQ_2025.tab, {names}, {e['year']}, reform and direction on every member",
            "note": f"a reform Garriga codes on every readable member of {label} in the same year with the same "
                    f"direction: one change of the union's money (P15); members: {', '.join(e['members'])}"
                    + (f"; members with no readable reform cell, left out: {', '.join(e['unread'])}"
                       if e["unread"] else ""),
            "clash": "; ".join(clash) or None})
    for (money, year), rf in sorted(reforms.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        if (money, year) in absorbed:
            continue
        u = in_union.get((money, year))
        changes.append({
            "money": money, "year": year, "direction": rf["direction"], "kind": "member" if u else "national",
            "members": [money], "war": war_year_fn(money, year),
            "locator": f"Replication_ISQ_2025.tab, {cname(money, year)}, {year}, reform and direction",
            "note": ("a reform Garriga codes for this economy's central bank"
                     + (f"; it is a member of {u} this year and the reform is not on every readable member with "
                        f"the same direction (A2)" if u else "")),
            "clash": rf["clash"], "union": u})

    # 4. overlaps and responses (A5), per money, over the up and down changes
    by_money: dict[str, list[dict]] = defaultdict(list)
    for c in changes:
        if c["direction"] in (1, -1):
            by_money[c["money"]].append(c)
    for c in changes:
        c["overlap"] = [f"{_route(o['direction'])}:{o['year']}" for o in by_money.get(c["money"], [])
                        if o is not c and c["direction"] in (1, -1)
                        and (0 < o["year"] - c["year"] <= WINDOW_AFTER or 0 < c["year"] - o["year"] <= WINDOW_AFTER)]
        c["responses"] = "; ".join(f"{_route(o['direction'])}:{o['year']}" for o in sorted(
            by_money.get(c["money"], []), key=lambda o: o["year"])
            if c["direction"] in (1, -1) and 0 < o["year"] - c["year"] <= WINDOW_AFTER)

    # 5. status (section 6) and the lines
    lines: list[dict] = []
    for c in sorted(changes, key=lambda c: (c["money"], c["year"], c["direction"] if c["direction"] is not None else 9)):
        money, year, direction = c["money"], c["year"], c["direction"]
        route = _route(direction)
        reasons, flags, exit_ = [], [], ""
        status = "counted"
        if direction is None:
            status = "cannot be read"
            flags.append("reform flagged, direction not read")
        if direction == 0:
            reasons.append(R_NEITHER)
        if c["kind"] == "member":
            reasons.append(R_STATUTE)
        if year <= FIRST_RECORD_YEAR + 2:
            reasons.append(R_BEFORE)
        if c["war"].startswith("yes"):
            reasons.append(f"{R_WAR} ({c['war'][5:]})")
        elif c["war"] == "cannot be read":
            flags.append("war year cannot be read")
        if c["clash"]:
            flags.append(f"direction clash: {c['clash']}")
        if c["overlap"]:
            flags.append("overlap: " + ", ".join(c["overlap"]))
        if reasons:
            status = "apart"
            notes["apart_reasons"].update(r.split(" (")[0] if r.startswith(R_WAR) else r for r in reasons)
        elif c["kind"] == "national" and money in EURO_ENTRY and status == "counted":
            entry = EURO_ENTRY[money]
            if year < int(entry[:4]) <= year + WINDOW_AFTER:
                status = "ended unbroken"
                exit_ = f"euro adoption, {entry}, {EURO_EXIT_SOURCE}"
                flags.append("competing exit: euro adoption inside the window")
        note = (f"apart: {'; '.join(reasons)}. " if reasons else "") + c["note"]
        if c["kind"] == "union":
            note += f"; war year read through the members (yes if one is, no if all are)"
        lines.append(line(money, route, year, value=1, unit="flag", locator=c["locator"], act="reform", note=note,
                          status=status, war_year=c["war"], flags=flags, headline=status != "apart",
                          uncertainty="judgement: the union's reading (P15, A2)" if c["kind"] == "union"
                          else "judgement: Garriga's direction disagrees with increase/decrease" if c["clash"]
                          else "clear", responses=c["responses"], exit=exit_))

    # 6. the index variant (A6)
    variants = 0
    for money, years in sorted(by.items()):
        for year in sorted(years):
            prev = years.get(year - 1)
            now, before = _num(years[year]["lvau_garriga"]), _num(prev["lvau_garriga"]) if prev else None
            if now is None or before is None or abs(round(now - before, 6)) < 0.05 - 1e-9:
                continue
            delta = round(now - before, 6)
            wy = war_year_fn(money, year)
            reasons = [R_VARIANT] + ([R_BEFORE] if year <= FIRST_RECORD_YEAR + 2 else []) \
                + ([f"{R_WAR} ({wy[5:]})"] if wy.startswith("yes") else [])
            lines.append(line(money, "a3-var-index", year, value=delta, unit="index points",
                              locator=f"Replication_ISQ_2025.tab, {cname(money, year)}, {year}, lvau_garriga",
                              act="index change", status="apart", war_year=wy, headline=False,
                              flags=["up" if delta > 0 else "down"]
                              + (["war year cannot be read"] if wy == "cannot be read" else []),
                              note=f"apart: {'; '.join(reasons)}. lvau_garriga moved {delta:+.3f} from {year - 1}"))
            variants += 1
    notes["variant_lines"] = variants
    for ln in lines:
        ln["rules_sha256"] = sha

    # 7. coverage
    cover: list[dict] = []
    for money, years in sorted(by.items()):
        coded = [y for y, r in years.items() if _flag(r, "reform") is not None]
        empty = [y for y, r in years.items() if _flag(r, "reform") is None]
        creation = [y for y, r in years.items() if _flag(r, "creation") == 1 and _flag(r, "reform") != 1]
        names = sorted({r["cname"] for r in years.values()})
        unions = sorted({u for (m, y), u in in_union.items() if m == money})
        cover.append({"money": money, "act": "A3 reform", "source": SOURCE,
                      "first_year": min(coded) if coded else "", "last_year": max(coded) if coded else "",
                      "years_empty": _collapse(empty), "creation_without_reform": _collapse(creation),
                      "names": " | ".join(names),
                      "note": "years with a row and an empty `reform` cell cannot be read, never 'no reform'; "
                              "a `creation` without a `reform` is no change (the institution's start)"
                              + (f"; a member of {', '.join(unions)} in some years (A1)" if unions else "")})
    for u in unmatched:
        cover.append({"money": f"unmatched:{u['cname']}", "act": "A3 reform", "source": SOURCE, "first_year": "",
                      "last_year": "", "years_empty": _collapse(u["years"]), "creation_without_reform": "",
                      "names": f"{u['cname']} (ISO {u['ISO'] or 'none'})",
                      "note": "no economy code: left out of the lines, never dropped silently"})
    return lines, cover, notes


def panel3_full(sha: str | None = None, *, rows=None, war_year_fn: Callable[[str, int], str] = war.war_year):
    """``(lines, coverage, notes)``: ``sha`` is the rules' hash (None: :func:`m0.require_locked`, which refuses
    uncommitted rules; ``""`` for a count that writes nothing)."""
    sha = m0.require_locked() if sha is None else sha
    return build(read_rows() if rows is None else rows, war_year_fn=war_year_fn, sha=sha)


def panel3(sha: str | None = None, *, rows=None, war_year_fn: Callable[[str, int], str] = war.war_year):
    """Panel 3's lines and coverage rows; nothing is written (the list is built later with the hand-coded panels)."""
    lines, cover, _ = panel3_full(sha, rows=rows, war_year_fn=war_year_fn)
    return lines, cover


# --- the hand-coded panels 1, 2 and 4, and the list ------------------------------------------------------------

CODER_FIRST = "a1: first coder (hand), coders/a1/lines.csv"
HAND_PANELS = ("1", "2", "4")
FROM2012 = "4-from-2012"                  # the headline: AREAER's candidates (sections 14, 17)
COBHAM_FOUR = "4-from-2012-var-cobham-four"
COBHAM_FULL = "4-from-2012-var-cobham-full"
MEMBER_PANELS = ("1", "2", "4", FROM2012, "2-irr", COBHAM_FOUR, COBHAM_FULL)
#: The frozen candidate list the headline membership of panel 4 from 2012 is (R-A3; built from the frozen AREAER editions).
AREAER_SERIES = ROOT / "data" / "reconstructed" / "ft001-a-areaer" / "series.csv"
#: A money's adoption from 2012 is dated from this date on (R-A3: the first listing is in an edition of 2012 or later).
FROM2012_START = "2012"
PROTOCOL = HERE.parent / "FT-001-M4-frame-a.md"
#: P19 (amended): the three targets that ended before 2012 are dated by their announcements only, not frozen.
P19_CODES = ("FIN", "ESP", "SVK")
COBHAM_FILE = "panel4-from2012-cobham.csv"
AREAER_DATASET = "frame-a/areaer-2011-2023"
P12_NOTE7 = "bj-note7"
P12_SUSP_DEV = "susp-dev-only"
BJ_COLUMNS = (("suspension", "bj_suspension"), ("exchange control", "bj_exchange_control"),
              ("devaluation", "bj_devaluation"))
HAND_ROUTES = {"1": "a1", "2": "a2", "4": "a4"}
HAND_SUPPORT = {"1": "redemption", "2": "redemption", "4": SUPPORT}
MEMBER_FIELDS = ["panel", "name_as_printed", "code", "member", "reason", "source", "locator", "settled"]
R_SPAN = "exit before 1931, outside M0's span (P13)"
#: Panel 1's span (P5, P7: 1 July 1914 to 31 December 1915) and panel 2's end (M0's 1931-36).
SPANS = {"1": ("1914-07", "1915-12"), "2": (None, "1936-12")}

#: Section 1's reading (H1): a member row that says its change cannot be dated (or read) while the coder wrote no line.
CANNOT_DATE = re.compile(r"\bchange\b[^.;]{0,80}?\bcannot be (?:read|dated)\b|\bcannot be dated\b", re.I)
SECTION_1 = ("section 1: a member whose change cannot be dated has no line and is 'cannot be read' in members.csv, "
             "never 'no change'")


def _csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as handle:
        return [dict(r) for r in csv.DictReader(handle)]


def settle_member(row: dict, *, has_line: bool) -> tuple[str, str]:
    """``(label, why)`` of a candidate of ``members.csv`` under section 1 (H1). A *yes* whose reason says its change
    cannot be dated, and for which its coder wrote no line, is *cannot be read*; anything else keeps its label."""
    label = row["member"].strip()
    if label == "yes" and not has_line and CANNOT_DATE.search(row["reason"]):
        return "cannot be read", SECTION_1
    return label, ""


def hand_status(row: dict, war: str) -> tuple[str, list[str], list[str]]:
    """``(status, reasons, flags)`` of a hand line, as far as section 6 can be read now (H2). ``war`` is the war year
    of the money in the change's year (:func:`war.war_year`'s answer)."""
    reasons, flags = [], []
    if row["headline"].strip() != "yes":
        reasons.append(f"variant: {row['variant'].strip() or 'unnamed'}")
    if war.startswith("yes"):
        reasons.append(f"{R_WAR} ({war[5:]})")
    elif war == "cannot be read":
        flags.append("war year cannot be read")                                 # P23: counted, flagged
    if row["panel"].strip() == "2" and m0._before(row["date"].strip(), "1931"):
        reasons.append(R_SPAN)                                                   # P13
    if reasons:
        return "apart", reasons, flags
    return ("ended unbroken" if row.get("exit", "").strip() else "counted"), reasons, flags


def hand_line(row: dict, *, sha: str, war_year_fn: Callable[[str, int], str] = war.war_year) -> dict:
    """One line of ``series.csv`` from one line of the first coder's ``lines.csv`` (columns of section 1)."""
    panel, code, date = row["panel"].strip(), row["code"].strip(), row["date"].strip()
    war_year = war_year_fn(code, int(date[:4]))
    status, reasons, flags = hand_status(row, war_year)
    variant = row["variant"].strip()
    route = HAND_ROUTES[panel] + (f"-var-{variant}" if row["headline"].strip() != "yes" else "")
    judged = row["uncertainty"].strip().startswith("judgement")
    quote, reason = row["quote"].strip(), row["reason"].strip()
    note = (f"apart: {'; '.join(reasons)}. " if reasons else "") + (f'quote: "{quote}"' if quote else "")
    if reason and not judged:
        note += f"; {reason}"
    given = [f.strip() for f in row["flags"].split(";") if f.strip() and not f.strip().startswith("apart:")]
    return {"period": date, "value": 1, "unit": "flag", "source": row["source"].strip(),
            "locator": row["locator"].strip(), "note": note.strip("; "),
            "uncertainty": f"judgement: {reason}" if judged else "clear", "money": code, "frame": "a", "route": route,
            "support": HAND_SUPPORT[panel], "headline": "yes" if row["headline"].strip() == "yes" and status != "apart"
            else "no", "act": row["act"].strip(), "entry_date": date, "entry_measure": "", "entry_measure_date": "",
            "outcome": "", "outcome_date": "", "onset_date": "", "responses": row.get("responses", "").strip(),
            "exit": row.get("exit", "").strip(), "status": status, "war_year": war_year,
            "flags": "; ".join(dict.fromkeys(given + flags)), "bj_suspension": row.get("bj_suspension", "").strip(),
            "bj_exchange_control": row.get("bj_exchange_control", "").strip(),
            "bj_devaluation": row.get("bj_devaluation", "").strip(), "informal_start": row.get("informal_start", "").strip(),
            "applied_from": row.get("applied_from", "").strip(), "coder": CODER_FIRST, "rules_sha256": sha}


IRR_SOURCE = ("Ilzetzki, Reinhart and Rogoff, 'The Country Chronologies to Exchange Rate Arrangements into the 21st "
              "Century', NBER Working Paper 23135 (February 2017) (irr/country-chronologies-1946-2016 2026-09-30)")
IRR_VARIANT = "irr"
IRR_FILE = "panel2-irr-variant.csv"
IRR_PEG = ("yes", "no", "cannot be read")


def _col(row: dict, prefix: str) -> str:
    """The value of the column whose name starts with ``prefix`` (the coder's headers carry a gloss after the name)."""
    [key] = [k for k in row if k.startswith(prefix)]
    return row[key].strip()


def irr_problems(rows: list[dict]) -> list[str]:
    """What is wrong with ``panel2-irr-variant.csv`` (H5): a code ``economies.py`` lacks, a standing that is not
    yes / no / cannot be read, a *yes* with no readable exit date (or an exit date on any other row), a candidate twice."""
    known = economies.known_codes()
    found = [f"irr: {c} listed {n} times" for c, n in Counter(r["code"] for r in rows).items() if n > 1]
    for r in rows:
        where, peg, date = f"irr {r['code']}", _col(r, "gold_peg"), _col(r, "exit_date")
        if r["code"] not in known:
            found.append(f"{where}: code is not in economies.py")
        if peg not in IRR_PEG:
            found.append(f"{where}: standing {peg!r} is not one of {IRR_PEG}")
        if (peg == "yes") != bool(date):
            found.append(f"{where}: a gold peg that stood has an exit date, any other standing has none")
        if date:
            try:
                m0._interval(date)
            except ValueError:
                found.append(f"{where}: exit date {date!r} cannot be read")
    return found


def irr_lines(rows: list[dict], *, sha: str, war_year_fn: Callable[[str, int], str] = war.war_year) -> list[dict]:
    """P11's variant by source as lines of ``series.csv``: route ``a2-var-irr``, ``headline`` no, *apart*, the exit
    date and the quotation as given, the war year and P13 applied by :func:`hand_line` (H5)."""
    out = []
    for r in rows:
        if _col(r, "gold_peg") != "yes":
            continue
        line = hand_line({"panel": "2", "code": r["code"].strip(), "date": _col(r, "exit_date"), "act": r["act"].strip(),
                          "headline": "no", "variant": IRR_VARIANT, "responses": "", "exit": "",
                          "flags": "P11 variant by source: a gold peg stood at 31 December 1929 (chronology)",
                          "source": IRR_SOURCE, "locator": r["locator"].strip(), "quote": _col(r, "quote"),
                          "uncertainty": "clear", "reason": r["reason"].strip()}, sha=sha, war_year_fn=war_year_fn)
        out.append(line)
    return out


def irr_members(rows: list[dict]) -> list[dict]:
    """Every row of the variant as a candidate in ``members.csv`` (panel ``2-irr``): the coder's standing, as written."""
    return [{"panel": "2-irr", "name_as_printed": r["name_as_printed"].strip(), "code": r["code"].strip(),
             "member": _col(r, "gold_peg"), "reason": r["reason"].strip(), "source": IRR_SOURCE,
             "locator": r["locator"].strip(), "settled": ""} for r in rows]


def hand_lines(rows: list[dict], *, sha: str, war_year_fn: Callable[[str, int], str] = war.war_year) -> list[dict]:
    return [hand_line(r, sha=sha, war_year_fn=war_year_fn) for r in rows]


def hand_problems(lines: list[dict], members: list[dict]) -> list[str]:
    """What is wrong with the first coder's files before any line is built (empty when they pass): a code that
    ``economies.py`` lacks, a route that is not the panel's, a variant that is not set apart (or the reverse), a date
    that cannot be read or lies outside the panel's span, a line for a candidate that is not a member, a candidate
    twice; for panel 4 from 2012 (H9): a money of both panel ``4`` and ``4-from-2012``, a line dated before 2012, an
    adopter (*yes*) with no headline line, a headline line for a candidate that is not *yes*."""
    known = economies.known_codes()
    found: list[str] = []
    seen = Counter((m["panel"], m["code"]) for m in members)
    found += [f"members: {p} {c} listed {n} times" for (p, c), n in seen.items() if n > 1]
    found += [f"members: panel {m['panel']!r} is not one of {MEMBER_PANELS}" for m in members
              if m["panel"] not in MEMBER_PANELS]
    found += [f"members: {m['panel']} {m['code']}: member {m['member']!r} is not yes, no or cannot be read"
              for m in members if m["member"] not in ("yes", "no", "cannot be read")]
    found += [f"members: code {m['code']!r} ({m['name_as_printed']}) is not in economies.py" for m in members
              if m["code"] not in known]
    label = {(m["panel"], m["code"]): m["member"] for m in members}
    from2012 = {m["code"]: m["member"] for m in members if m["panel"] == FROM2012}
    found += [f"members: {c} is in panel 4 and in {FROM2012}: a money listed in 2011 is a targeter already (R-A3)"
              for c in sorted(from2012) if ("4", c) in label]
    for code in P19_CODES:                                        # P19 amended: no fallback to Cobham's years
        if label.get(("4", code), "cannot be read") != "cannot be read" or any(
                r["panel"] == "4" and r["code"] == code for r in lines):
            found.append(f"P19 amended: {code} is dated by its central bank's announcement only (not frozen): "
                         "cannot be read, no line")
    for r in lines:
        where = f"line {r['panel']} {r['code']} {r['date']}"
        if r["panel"] not in HAND_PANELS:
            found.append(f"{where}: panel {r['panel']!r} is not one of {HAND_PANELS}")
            continue
        if r["route"] != HAND_ROUTES[r["panel"]]:
            found.append(f"{where}: route {r['route']!r} is not {HAND_ROUTES[r['panel']]!r}")
        if r["code"] not in known:
            found.append(f"{where}: code is not in economies.py")
        if r["headline"] not in ("yes", "no"):
            found.append(f"{where}: headline {r['headline']!r} is not yes or no")
        if (r["headline"] == "no") != bool(r["variant"].strip()):
            found.append(f"{where}: a variant line has headline no and a named variant, a headline line neither")
        try:
            m0._interval(r["date"])
        except ValueError:
            found.append(f"{where}: date cannot be read")
            continue
        late = r["panel"] == "4" and r["code"] in from2012                   # H9: a candidate of the AREAER list
        if late and m0._before(r["date"], FROM2012_START):
            found.append(f"{where}: an adoption from 2012 dated before {FROM2012_START}")
        if r["headline"] == "yes":
            lo, hi = SPANS.get(r["panel"], (None, None))
            if lo and m0._before(r["date"], lo) or hi and m0._before(hi, r["date"]):
                found.append(f"{where}: a headline change outside the panel's span {lo or '...'} to {hi}")
            held = label.get((r["panel"], r["code"])) or (from2012.get(r["code"]) if r["panel"] == "4" else None)
            if held != "yes":
                found.append(f"{where}: a headline change of a candidate that is not a member "
                             f"({held or 'not listed'})")
    headed = Counter(r["code"] for r in lines if r["panel"] == "4" and r["headline"] == "yes")
    found += [f"members: {FROM2012} {c} is an adopter (yes) and has {headed[c]} headline lines, not one: it is dated by "
              "its central bank's announcement (R-A4)" for c, v in sorted(from2012.items()) if v == "yes" and headed[c] != 1]
    return found


def _p12_responses(row: dict) -> tuple[str, list[str]]:
    """``(responses, earlier)`` of a panel-2 line from its three ``bj_*`` dates: the changes dated after the line's
    exit as ``type:date``, and those dated before it (told in ``flags``, never responses: a response before the entry
    is refused by the line check). A date equal to the exit's is the exit's own (``act``)."""
    entry = row["date"].strip()
    later, earlier = [], []
    for name, column in BJ_COLUMNS:
        when = row.get(column, "").strip()
        if not when or when == entry:
            continue
        (earlier if m0._before(when, entry) else later).append(f"{name}:{when}")
    return ";".join(later), earlier


def p12_amended(lines: list[dict]) -> tuple[list[dict], list[str]]:
    """Panel 2 under P12 as amended (H6): ``(rows, control_only)``.

    ``rows`` are the first coder's lines with panel 2 swapped by rule: its ``susp-dev-only`` rows become the headline
    (first of suspension and devaluation), its headline rows (note 7's first of the three dates) become the variant
    ``bj-note7``; the other panels' rows pass through. ``control_only`` are the panel-2 members whose only change in
    1931-36 is an exchange control: they have a note-7 row and no suspension-or-devaluation row, hence no headline."""
    other = [r for r in lines if r["panel"] != "2"]
    by: dict[str, list[dict]] = defaultdict(list)
    for r in lines:
        if r["panel"] == "2":
            by[r["code"]].append(r)
    out, control_only, faults = [], [], []
    for code, rows in by.items():
        note7 = [r for r in rows if r["headline"] == "yes" and not r["variant"].strip()]
        both = [r for r in rows if r["variant"].strip() == P12_SUSP_DEV]
        if len(note7) != 1 or len(both) > 1 or len(note7) + len(both) != len(rows):
            faults.append(f"panel 2 {code}: needs one note-7 (headline) row and at most one '{P12_SUSP_DEV}' row, "
                          f"has {[(r['headline'], r['variant']) for r in rows]}")
            continue
        n7 = note7[0]
        kept = lambda r: [f.strip() for f in r["flags"].split(";")  # noqa: E731
                          if f.strip() and not f.strip().startswith(("variant:", "apart:"))]
        if both:
            sd = both[0]
            later, earlier = _p12_responses(sd)
            told = [f"{n7['act']} dated {n7['date']}, earlier than the headline exit: Bernanke and James's note 7 "
                    "reads it as the exit (variant a2-var-bj-note7)"] if n7["date"] != sd["date"] else []
            out.append({**sd, "headline": "yes", "variant": "", "responses": later,
                        "flags": "; ".join(dict.fromkeys(kept(sd) + kept(n7) + told)),
                        "reason": "first of suspension and devaluation (M0 section 2: force imposed is never an act of "
                                  "this list; P12 amended, section 13)"})
            gap = f"the headline exit (suspension or devaluation) is {sd['act']} {sd['date']}" \
                if n7["date"] != sd["date"] else "the headline exit is the same event and date"
        else:
            control_only.append(code)
            gap = "no headline exit: its only change in 1931-36 is an exchange control"
        later, _ = _p12_responses(n7)
        out.append({**n7, "headline": "no", "variant": P12_NOTE7, "responses": later,
                    "flags": "; ".join(dict.fromkeys(kept(n7) + [f"variant: Bernanke and James's note 7, the first of "
                                                                  f"the three dates; {gap}"]))})
    if faults:
        raise ValueError("panel 2 cannot be split under P12 as amended:\n  " + "\n  ".join(faults))
    return other + out, sorted(control_only)


def settled_members(members: list[dict], lines: list[dict]) -> list[dict]:
    """``members.csv``'s rows: the first coder's, each settled under section 1 (H1); ``settled`` says why a label
    moved, or which amended reading applies (empty otherwise). The Cobham full-only list's rows are
    :func:`from2012_members`'; the headline from 2012 is the first coder's ``4-from-2012`` rows (AREAER's, H9)."""
    has_line = {(r["panel"], r["code"]) for r in lines}
    control_only = set(p12_amended(lines)[1]) if any(r["panel"] == "2" for r in lines) else set()
    out = []
    for m in members:
        label, why = settle_member(m, has_line=(m["panel"], m["code"]) in has_line)
        if m["panel"] == "2" and m["code"] in control_only:
            why = ("P12 amended (section 13): its only change in 1931-36 is an exchange control, which is no act of "
                   "this list (M0 section 2): a member with no change in the span, its dates read; its note-7 line is "
                   "the variant a2-var-bj-note7")
        elif m["panel"] == "4" and m["code"] in P19_CODES:
            why = ("P19 amended (section 13): dated by the central bank's announcement only, not frozen; no fallback "
                   "to Cobham's classification")
        elif m["panel"] == FROM2012:
            why = FROM2012_WHY
        elif m["panel"] == COBHAM_FOUR:
            why = COBHAM_WHY
        out.append({**{k: m[k].strip() for k in MEMBER_FIELDS[:-1]}, "member": label, "settled": why})
    return out


COBHAM_WHY = ("variant conditioned on behaviour (section 13, B1): Cobham's categories include targets attained, and a "
              "formal targeter that keeps missing sits in loosely structured discretion")
FROM2012_WHY = ("the list is AREAER's (sections 13 and 14: R-A1 to R-A3); an adopter is a candidate whose own central "
                "bank's announcement states an explicit numerical inflation target as the anchor, dated by it (R-A4, "
                "P21); a candidate whose announcement is not frozen, or is no announcement, is cannot be read "
                "(section 17)")


def _cobham_rows(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """``(four-category, full-only)`` candidates of ``panel4-from2012-cobham.csv``, Hammond's holdings left out (Q7)."""
    free = [r for r in rows if _col(r, "in_Hammond").startswith("no")]
    return ([r for r in free if r["list"].startswith("Q6 headline")],
            [r for r in free if r["list"].startswith("variant: full")])


def cobham_problems(members: list[dict], rows: list[dict]) -> list[str]:
    """The first coder's Cobham four-category candidates (panel ``4-from-2012-var-cobham-four``) and Cobham's file must
    name the same candidates."""
    known = economies.known_codes()
    four, _ = _cobham_rows(rows)
    mine = {m["code"] for m in members if m["panel"] == COBHAM_FOUR}
    found = [f"cobham file: {r['code']} is not in economies.py" for r in rows if r["code"] not in known]
    if mine != {r["code"] for r in four}:
        found.append(f"{COBHAM_FOUR}: members.csv has {sorted(mine)}, the Cobham file's four-category list "
                     f"{sorted(r['code'] for r in four)}")
    return found


def areaer_problems(members: list[dict], rows: list[dict]) -> list[str]:
    """The first coder's headline panel ``4-from-2012`` must name exactly the candidates of the frozen AREAER list
    (``ft001-a-areaer``'s ``series.csv``, ``rows``), each once (H9), with the AREAER dataset among its sources."""
    mine = Counter(m["code"] for m in members if m["panel"] == FROM2012)
    theirs = {r["money"].strip() for r in rows}
    found = [f"{FROM2012}: {c} listed {n} times" for c, n in sorted(mine.items()) if n > 1]
    if set(mine) != theirs:
        found.append(f"{FROM2012}: members.csv has {sorted(set(mine) - theirs)} that the AREAER list lacks and lacks "
                     f"{sorted(theirs - set(mine))} that it has")
    found += [f"{FROM2012} {m['code']}: its source does not name frame-a/areaer-2011-2023" for m in members
              if m["panel"] == FROM2012 and AREAER_DATASET not in m["source"]]
    return found


def from2012_members(rows: list[dict]) -> list[dict]:
    """The Cobham full-only list's rows of ``members.csv`` (H7, B1): a variant "conditioned on behaviour", each candidate
    *cannot be read*. The headline from 2012 (AREAER's candidates) and Cobham's four-category candidates are the first
    coder's own rows (H9), passed through :func:`settled_members`."""
    def row(panel, name, code, reason, source, locator, settled=""):
        return {"panel": panel, "name_as_printed": name, "code": code, "member": "cannot be read", "reason": reason,
                "source": source, "locator": locator, "settled": settled}

    _, full = _cobham_rows(rows)
    return [row(COBHAM_FULL, r["name_as_printed"].strip(), r["code"].strip(),
                f"Cobham's full categories only (FIT, FCIT): first year from 2012 is "
                f"{_col(r, 'first_year')} (code {_col(r, 'category_code')}; the year before: "
                f"{_col(r, 'previous_year')}); this list selects on attainment; cannot be read: announcement "
                "not frozen", "frame-a/cobham-monetary-frameworks-2024", f"{COBHAM_FILE}, {r['name_as_printed']}",
                COBHAM_WHY) for r in full]


# --- the second coder's agreement --------------------------------------------------------------------------

def cohen_kappa(pairs: list[tuple[str, str]]) -> dict:
    """Cohen's kappa on ``(first coder's category, second coder's category)`` pairs, with n. Undefined (``None``, said)
    where chance agreement is 1, i.e. every candidate is in one category for both coders."""
    n = len(pairs)
    if n == 0:
        return {"n": 0, "kappa": None, "observed": None, "expected": None, "note": "no candidate"}
    po = Fraction(sum(a == b for a, b in pairs), n)
    pe = sum(Fraction(sum(a == c for a, _ in pairs), n) * Fraction(sum(b == c for _, b in pairs), n)
             for c in {x for pair in pairs for x in pair})
    out = {"n": n, "observed": round(float(po), 3), "expected": round(float(pe), 3)}
    if pe == 1:
        return {**out, "kappa": None, "note": "undefined: every candidate is in one category for both coders"}
    return {**out, "kappa": round(float((po - pe) / (1 - pe)), 3)}


def _headline(lines: list[dict], panel: str, code: str) -> list[dict]:
    return [r for r in lines if r["panel"].strip() == panel and r["code"].strip() == code
            and r["headline"].strip() == "yes"]


def _category(label: str, lines: list[dict], war_year_fn) -> str:
    """A candidate's category for the status kappa: cannot be read, not a member, or a member counted, apart,
    ended unbroken or with no change (the lines are the coder's headline lines)."""
    if label == "cannot be read":
        return "cannot be read"
    if label == "no":
        return "not a member"
    if not lines:
        return "member, no change"
    return "member, " + "+".join(sorted({hand_status(r, war_year_fn(r["code"].strip(), int(r["date"].strip()[:4])))[0]
                                         for r in lines}))


def agreement_rows(first_members: list[dict], first_lines: list[dict], second_members: list[dict],
                   second_lines: list[dict], sample: dict[str, list[str]], *,
                   war_year_fn: Callable[[str, int], str] = war.war_year) -> dict:
    """The first and second coders compared on the sample (``{"1": [codes], "2": [...], "4": [...]}``, section 12).

    Per panel and pooled: Cohen's kappa on membership (yes / no / cannot be read) as the coders coded it
    (``kappa_membership``) and after section 1's settlement (``kappa_membership_settled``), kappa on membership and
    status (``kappa_status``: not a member, cannot be read, member counted / apart / ended unbroken / with no
    change, from the settled labels and the lines' statuses), and the share of identical dates of the headline
    changes both coders dated. Every disagreement is listed with its ``kind``: ``membership``, ``labelling`` (the
    labels differ as coded, and section 1 settles them), ``status``, ``date``, or ``dated by one only``."""
    by1 = {(m["panel"].strip(), m["code"].strip()): m for m in first_members}
    by2 = {(m["panel"].strip(), m["code"].strip()): m for m in second_members}
    results: dict = {"panels": {}}
    pooled = {"raw": [], "settled": [], "status": []}
    dates_pooled = [0, 0]
    disagreements: list[dict] = []
    for panel, codes in sample.items():
        raw, settled, status, both_dated, identical = [], [], [], 0, 0
        for code in codes:
            for who, table in (("a1", by1), ("a2", by2)):
                if (panel, code) not in table:
                    raise ValueError(f"coder {who} has no row for sampled candidate {panel} {code}")
            l1, l2 = _headline(first_lines, panel, code), _headline(second_lines, panel, code)
            any1 = any(r["panel"].strip() == panel and r["code"].strip() == code for r in first_lines)
            any2 = any(r["panel"].strip() == panel and r["code"].strip() == code for r in second_lines)
            r1, r2 = by1[(panel, code)]["member"].strip(), by2[(panel, code)]["member"].strip()
            s1, _ = settle_member(by1[(panel, code)], has_line=any1)
            s2, _ = settle_member(by2[(panel, code)], has_line=any2)
            c1, c2 = _category(s1, l1, war_year_fn), _category(s2, l2, war_year_fn)
            raw.append((r1, r2))
            settled.append((s1, s2))
            status.append((c1, c2))
            where = {"panel": panel, "code": code, "name": by1[(panel, code)]["name_as_printed"].strip()}
            if r1 != r2 and s1 == s2:
                disagreements.append({**where, "kind": "labelling", "a1": r1, "a2": r2,
                                      "settled_by": SECTION_1, "settled_in_favour_of": "a1" if r1 == s1 else "a2",
                                      "a1_reason": by1[(panel, code)]["reason"].strip(),
                                      "a2_reason": by2[(panel, code)]["reason"].strip()})
            elif s1 != s2:
                disagreements.append({**where, "kind": "membership", "a1": r1, "a2": r2,
                                      "settled_by": "not settled: by the text of M0 and of the protocol (section 8)",
                                      "a1_reason": by1[(panel, code)]["reason"].strip(),
                                      "a2_reason": by2[(panel, code)]["reason"].strip()})
            d1, d2 = sorted(r["date"].strip() for r in l1), sorted(r["date"].strip() for r in l2)
            one_sided = bool(d1) != bool(d2)
            if s1 == s2 and c1 != c2 and not one_sided:     # a one-sided date already says why the statuses differ
                disagreements.append({**where, "kind": "status", "a1": c1, "a2": c2,
                                      "settled_by": "not settled: by the text of M0 and of the protocol (section 8)"})
            if d1 and d2:
                both_dated += 1
                identical += d1 == d2
                if d1 != d2:
                    disagreements.append({**where, "kind": "date", "a1": d1, "a2": d2,
                                          "settled_by": "not settled: by the text of M0 and of the protocol (section 8)"})
            elif one_sided and s1 == s2:     # under a membership disagreement the missing line is its consequence
                disagreements.append({**where, "kind": "dated by one only", "a1": d1, "a2": d2,
                                      "settled_by": "not settled: by the text of M0 and of the protocol (section 8)"})
        results["panels"][panel] = {
            "n": len(codes), "candidates": list(codes), "kappa_membership": cohen_kappa(raw),
            "kappa_membership_settled": cohen_kappa(settled), "kappa_status": cohen_kappa(status),
            "dates": {"both_dated": both_dated, "identical": identical,
                      "share_identical": round(identical / both_dated, 3) if both_dated else None}}
        pooled["raw"] += raw
        pooled["settled"] += settled
        pooled["status"] += status
        dates_pooled[0] += both_dated
        dates_pooled[1] += identical
    results["pooled"] = {
        "n": len(pooled["raw"]), "kappa_membership": cohen_kappa(pooled["raw"]),
        "kappa_membership_settled": cohen_kappa(pooled["settled"]), "kappa_status": cohen_kappa(pooled["status"]),
        "dates": {"both_dated": dates_pooled[0], "identical": dates_pooled[1],
                  "share_identical": round(dates_pooled[1] / dates_pooled[0], 3) if dates_pooled[0] else None}}
    results["disagreements"] = sorted(disagreements, key=lambda d: (d["panel"], d["code"], d["kind"]))
    results["reading"] = {
        "section_1": SECTION_1, "compared": "each coder's headline lines, dates at the source's own precision "
        "(H4); variant lines are not compared",
        "samples_are_small": "kappa is printed with its n and carries no claim (M4 section 8)"}
    return results


def agreement(first_dir: Path, second_dir: Path, sample_file: Path, *,
              war_year_fn: Callable[[str, int], str] = war.war_year, protocol: str | None = None) -> dict:
    """:func:`agreement_rows` on the two coders' folders and the draw's file (``second-coder-sample.json``)."""
    drawn = json.loads(Path(sample_file).read_text())
    sample = {k.removeprefix("panel_"): v for k, v in drawn["sample"].items()}
    out = agreement_rows(_csv(first_dir / "members.csv"), _csv(first_dir / "lines.csv"),
                         _csv(second_dir / "members.csv"), _csv(second_dir / "lines.csv"), sample,
                         war_year_fn=war_year_fn)
    out["reading"]["panel_2"] = ("the coders' own headline lines: Bernanke and James's note 7, what both coded; the "
                                 "amended P12 (section 13) swaps them by rule in the build, it is not recoded")
    return {"protocol_commit": protocol or protocol_commit(), "seed": drawn.get("seed"), "rule": drawn.get("rule"),
            **out}


def protocol_commit(path: Path = PROTOCOL) -> str:
    """The commit of the protocol the lists are coded under (M1): ``git log -1 --format=%h`` of the file; refused when
    the file is not committed or changed since its commit (a changed protocol is committed before any build)."""
    cwd = path.parent
    run = lambda *a: subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)  # noqa: E731
    head = run("log", "-1", "--format=%h", "--", path.name).stdout.strip()
    if not head:
        raise RuntimeError(f"{path.name} is not committed: commit the protocol before any build")
    if run("diff", "--quiet", "HEAD", "--", path.name).returncode != 0:
        raise RuntimeError(f"{path.name} changed since its commit {head}: commit it before any build")
    return head


# --- the archive and the build -----------------------------------------------------------------------------

ARCHIVED_SUFFIXES = (".csv", ".md", ".json")  # a reconstructed dataset holds no script (BLUEPRINT §7)


def archive_coders(first_dir: Path, second_dir: Path, sample_file: Path, out: Path) -> list[str]:
    """Copy each coder's top-level files (H3) to ``out/coders/a1`` and ``out/coders/a2``, and the draw beside them."""
    dest = out / "coders"
    written = []
    for name, src in (("a1", first_dir), ("a2", second_dir)):
        (dest / name).mkdir(parents=True, exist_ok=True)
        for f in sorted(src.iterdir()):
            if f.is_file() and f.suffix in ARCHIVED_SUFFIXES:
                shutil.copyfile(f, dest / name / f.name)
                written.append(f"coders/{name}/{f.name}")
    shutil.copyfile(sample_file, dest / "second-coder-sample.json")
    written.append("coders/second-coder-sample.json")
    return written


def _write(path: Path, fields: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def build_all(hand_dir: str | Path, out: str | Path = Path("data/reconstructed/ft001-a"), *,
              second_dir: str | Path | None = None, sample_file: str | Path | None = None, sha: str | None = None,
              war_year_fn: Callable[[str, int], str] = war.war_year, panel3_rows=None,
              protocol: str | None = None, areaer_series: str | Path = AREAER_SERIES) -> dict:
    """Write frame a's list in the protocol's format (section 1) and return a summary.

    ``hand_dir`` is the first coder's folder (``lines.csv``, ``members.csv``, ``panel2-irr-variant.csv``,
    ``panel4-from2012-cobham.csv``); ``protocol`` is the protocol's commit (default: :func:`protocol_commit`);
    ``areaer_series`` is the frozen AREAER candidate list (``ft001-a-areaer``) the headline ``4-from-2012`` panel must
    equal (H9); ``second_dir`` and ``sample_file`` default to ``<hand_dir>/../a2`` and ``<hand_dir>/../second-coder-sample.json``. Writes ``series.csv`` (the hand
    panels 1, 2 and 4 and P11's variant lines, then panel 3), ``members.csv`` (panels 1, 2, 4, AREAER's from-2012
    candidates, Cobham's two variant lists and P11's variant's candidates, settled under section 1), ``coverage.csv`` (panel 3's), ``agreement.json`` and ``coders/``. ``out`` is relative to the
    workshop's root. Refuses, before writing anything, a hand file :func:`hand_problems` faults or a line
    :func:`m0.line_problems` refuses. The rules must be committed (:func:`m0.require_locked`) unless ``sha`` is given
    (tests)."""
    hand_dir = Path(hand_dir)
    second_dir = Path(second_dir) if second_dir else hand_dir.parent / "a2"
    sample_file = Path(sample_file) if sample_file else hand_dir.parent / "second-coder-sample.json"
    out = Path(out) if Path(out).is_absolute() else ROOT / out
    sha = m0.require_locked() if sha is None else sha
    first_lines, first_members = _csv(hand_dir / "lines.csv"), _csv(hand_dir / "members.csv")
    irr, cobham = _csv(hand_dir / IRR_FILE), _csv(hand_dir / COBHAM_FILE)
    areaer = _csv(areaer_series)
    protocol = protocol or protocol_commit()
    faults = (hand_problems(first_lines, first_members) + irr_problems(irr) + cobham_problems(first_members, cobham)
              + areaer_problems(first_members, areaer))
    if faults:
        raise ValueError("the first coder's files are refused:\n  " + "\n  ".join(faults))
    swapped, control_only = p12_amended(first_lines)
    hand = hand_lines(swapped, sha=sha, war_year_fn=war_year_fn) + irr_lines(irr, sha=sha, war_year_fn=war_year_fn)
    reform, cover = panel3(sha, rows=panel3_rows, war_year_fn=war_year_fn)
    series = sorted(hand + reform, key=lambda r: (r["route"][:2], r["money"], r["period"], r["route"]))
    statuses = tuple(m0.rules()["case_line"]["statuses"])
    refused = [f"{r['route']} {r['money']} {r['period']}: {p}" for r in series
               for p in m0.line_problems(r, sha, statuses)]
    if refused:
        raise ValueError("lines refused by m0.line_problems:\n  " + "\n  ".join(refused))
    members = settled_members(first_members, first_lines) + from2012_members(cobham) + irr_members(irr)
    agreed = agreement(hand_dir, second_dir, sample_file, war_year_fn=war_year_fn, protocol=protocol)
    out.mkdir(parents=True, exist_ok=True)
    _write(out / "series.csv", FIELDS, series)
    _write(out / "members.csv", MEMBER_FIELDS, members)
    _write(out / "coverage.csv", COVERAGE_FIELDS, cover)
    (out / "agreement.json").write_text(json.dumps(agreed, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    archived = archive_coders(hand_dir, second_dir, sample_file, out)
    tally = Counter(m["member"] for m in first_members if m["panel"] == FROM2012)
    from_2012 = (f"the headline is the IMF AREAER's {sum(tally.values())} candidates (ft001-a-areaer), each read by its "
                 f"central bank's own announcement (R-A4): {tally['yes']} adopters, {tally['no']} not adopters, "
                 f"{tally['cannot be read']} cannot be read; Cobham's four-category and full-only lists are variants "
                 "conditioned on behaviour, every candidate cannot be read (announcement not frozen)")
    return {"protocol_commit": protocol, "rules_sha256": sha, "panel_2_control_only_members": control_only,
            "from_2012": from_2012,
            "out": str(out), "series_lines": len(series), "hand_lines": len(hand), "panel3_lines": len(reform),
            "members": len(members), "coverage_rows": len(cover), "archived": archived,
            "by_route_status": dict(Counter((r["route"].split("-var")[0], r["status"]) for r in series))}


def count() -> None:
    lines, cover, notes = panel3_full("")
    print(f"{len(lines)} lines, {len(cover)} coverage rows")
    tally = Counter((r["route"], r["status"]) for r in lines)
    print("\nroute / status")
    for key, n in sorted(tally.items()):
        print(f"{n:6d}  {key[0]:14s}{key[1]}")
    print("\napart, by reason (up, down and neither lines; a line can carry several)")
    for k, n in notes["apart_reasons"].most_common():
        print(f"{n:6d}  {k}")
    panel = [r for r in lines if r["route"] in ("a3-up", "a3-down")]
    print("\nup and down, by status:", dict(Counter(r["status"] for r in panel)))
    print("war year, on lines not apart:", dict(Counter(r["war_year"].split(":")[0] for r in panel
                                                      if r["status"] != "apart")))
    print("war year, all up/down/neither lines:", dict(Counter(r["war_year"].split(":")[0] for r in lines
                                                                if r["route"] != "a3-var-index")))
    print("\nunions (one line of the union's money each):")
    for u, y, d, members in notes["unions"]:
        print(f"  {u} {y} {'up' if d == 1 else 'down'}: {', '.join(members)}")
    print("\ndirection clashes:", len(notes["clashes"]))
    for c in notes["clashes"]:
        print("  ", *c)
    print("regional = 1 on an economy in no union:", notes["regional_outside"] or "none")
    print("variant lines (a3-var-index):", notes["variant_lines"], dict(Counter(
        r["flags"].split(";")[0] for r in lines if r["route"] == "a3-var-index")))
    print("ended unbroken (euro entry inside the window):", sum(r["status"] == "ended unbroken" for r in lines))
    print("lines with an overlap flag:", sum("overlap" in r["flags"] for r in lines))
    print("unmatched Garriga names:", [(u["cname"], u["ISO"], f"{u['years'][0]}-{u['years'][-1]}")
                                       for u in notes["unmatched"]] or "none")
    print("coverage rows with empty years:", sum(1 for c in cover if c["years_empty"]))


if __name__ == "__main__":
    if sys.argv[1:2] == ["count"]:
        count()
    elif sys.argv[1:2] == ["build"] and len(sys.argv) == 3:
        def _keys(o):  # the summary's counts are keyed by tuples: printed as "a|b"
            if isinstance(o, dict):
                return {("|".join(map(str, k)) if isinstance(k, tuple) else k): _keys(v) for k, v in o.items()}
            return [_keys(v) for v in o] if isinstance(o, list) else o
        print(json.dumps(_keys(build_all(sys.argv[2])), indent=1))
    else:
        print(__doc__)
        sys.exit(2)
