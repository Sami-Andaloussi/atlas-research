"""FT-001 M4, frame a: M0 section 1's *war year* for every state-year, by script (FT-001-M4-frame-a.md, sections 6, 8).

M0 (section 1, "War, the common cause"): a war year for a state is one in which (a) at least 1,000 battle deaths
fell on its territory (UCDP by location from 1989 where open, else the World Bank's battle-deaths series; the
Correlates of War's intra-state wars and the inter-state wars fought on its soil before), or (b) it took part in a
Correlates of War war in which its own forces lost at least 1,000. A case entering in a war year is *apart*.

Sources, frozen in ``data/`` (vintage 2026-09-30): ``cow/inter-state-wars`` v4.0 (1816-2007, one record per
participant, its battle deaths), ``cow/intra-state-wars`` v5.1 (zip; 1816-2014; a war file with the state in whose
territory it was fought, and a state-participants file with each state's deaths), ``cow/extra-state-wars`` v4.0
(1816-2007, a state against a non-state entity outside its borders), ``cow/state-system`` v2024 (which states
exist, which year, and their codes), ``worldbank/VC.BTL.DETH`` (battle-related deaths by location, 1989-2024) and,
frozen on 2026-10-01, ``ucdp/conflict-dyadic-v26.1`` (the UCDP/PRIO Armed Conflict Dataset v26.1, 1946-2025, one row
per conflict-year, downloaded by hand; only W12 reads it, through ``UcdpPrioConflict_v26_1.csv``). UCDP's other files
are not frozen. COW's non-state wars are not frozen either.

:func:`war_year` answers ``"yes: <war name(s)>"``, ``"no"`` or ``"cannot be read"`` for a money and a year;
:func:`detail` says why; :func:`table` is the builder, one row per state-year of the COW state system.

**Readings.** M0's words do not fix the rule in the places below; each is chosen here, in the open, for the
audit to judge (the protocol's P22-P23 are the frame's own; these are this script's).

W1. *Year precision.* A war is in a year if its fighting (COW's "sustained combat", each of its periods, up to
    four) touches any day of it: month and day are not used. A year a war ended on its first day is counted.

W2. *Deaths "in the year" when COW gives a war's total.* COW gives battle deaths once per war, never per year.
    COW defines a war as sustained combat with at least 1,000 battle-related combatant deaths within a twelve-month
    period, and dates its end as the month after which fatalities fell below that threshold (its codebooks, the
    variables EndMonth1 / EndMo1). So the fighting years of a COW war are read as years at war level: **every year
    a COW war's fighting touches is a year with at least 1,000 deaths on the territory of the state where it was
    fought** (W4) and, for a state that took part, **a year of the war in which its own forces lost at least
    1,000** if their total in the war is 1,000 or more (W5). The alternative - the total divided over the war's
    days - would call a year "no" in the heart of a long war; it is not built. The span reading can overcount a
    long war's quiet years; :func:`count` prints, for 1989-2014, how often COW's span says "war" where the World
    Bank's annual series says "under 1,000" (on 2026-09-30: 152 of 335 state-years with a COW-located war and a
    World Bank value, 45%; a calibration by war-years (338) of the total divided over the war's months gave
    the other error too: 17 years the World Bank puts at 1,000 or more called "no", 100 called "yes" that it
    puts under, against 152 "yes" and no "no" for the span). So **a *yes* before 1989 on
    COW's territory test is an upper bound**; from 1989 the World Bank's annual value decides.

W3. *War years from the World Bank's series.* For 1989-2024 the territory's deaths are the World Bank's
    ``VC.BTL.DETH`` (UCDP by location), 1,000 or more = yes. The series holds a value only for an economy with a
    UCDP conflict in the year; a missing value in a year the economy has a row is read as **no battle deaths
    recorded (UCDP codes conflicts from 25 deaths)**, i.e. under 1,000. For a state the World Bank does not list
    (a dissolved state; Taiwan) the series cannot be read: the state's successors' rows are summed where the
    state's territory became theirs (W8); otherwise COW's intra-state wars are the fallback for a *yes*, and no
    *no* is given. From 1989 the COW territory test is not applied where the World Bank's series can be read
    (M0 names COW's territory for "before").

W4. *Territory, before 1989.* A state's territory is in a war year if COW's intra-state war file locates a war in
    it (``CcodeA``, the state on Side A: the government of a civil war) in a year of the fighting. **41 of the 420
    intra-state wars have no state in that field** (regional internal wars and intercommunal wars whose host COW
    does not code): they are attributed to no state, so a state-year "no" before 1989 means "no war COW locates
    on its soil". :func:`table` carries, for each year, how many such wars were open (``open_unlocated``).
    Inter-state wars are located only by region ("WhereFought"), never by state: see W6.

W5. *Own forces' losses.* "Its own forces lost at least 1,000" is read at the level of the war: the sum of the
    state's records in the war (a state that changed sides has two; COW gives the deaths of each) of COW's battle
    deaths "suffered by the state" (inter-state ``BatDeath``; extra-state ``BatDeath``; intra-state ``Deaths A``
    for a state on Side A and ``Deaths B`` for one on Side B, in the state-participants file). The deaths are the
    war's total for the state, never a year's (W2); the years counted are those of the state's own records
    (each participant has its own dates). A total of -9 (unknown) in any record, with the known part under 1,000,
    makes the state-year *cannot be read*, never "no". Extra-state wars count for (b): M0 says "a Correlates of
    War war", not a type; they never count for (a) (they are fought outside the state system).

W6. *An inter-state war's participant whose own losses stay under 1,000, before 1989.* Its territory was
    possibly a battlefield: COW says only "region(s) where combat involving the state occurred". Soil cannot be
    attributed to a state, so the state-year in the war's years is **cannot be read**, never "no" (the protocol's
    P22 calls this state "not in a war year" if none fell on its soil; no source frozen here says so).
    A state that is not a participant is read as having no war on its soil from inter-state wars (a neutral
    territory used as a battlefield is not seen). An intervening state in an intra-state or extra-state war is
    read as fighting outside its territory.

W7. *A state outside the record.* Before 1816, after 2024, or in a year the state is not in COW's state system
    (occupation, dependence, a place that is not a state): **cannot be read**. A union's money (``EMU``,
    ``XOF``) and a colony are not states here; :mod:`frame_a` reads a union through its members. COW's state
    codes are mapped to the workshop's codes through ``economies.code``; a name it does not know keeps its state
    in the table under ``COW<ccode>`` and is listed by :func:`unmatched` and ``count`` - none is dropped.
    Lineage: COW's Russia (365) is ``RUS``, and also ``SUN`` for 1922-1991 (the acts list's convention);
    COW's Austria-Hungary (300, to 1918) answers ``XAH`` and also ``AUT`` and ``HUN`` (a panel may code the
    Dual Monarchy under either successor, as P2 does the Ottoman and Russian empires);
    COW's Yugoslavia/Serbia (345) answers ``YUG``, ``SCG`` and ``SRB`` all along; West Germany (260) is ``DEU``
    and East Germany (265) ``DDR``; the Republic of the Congo (484) is ``COG`` (an override held here, since a
    global alias for the bare name "Congo" would catch another source's DRC).

W8. *Territory of a dissolved state, 1989 on* (the World Bank has no row for it): the sum of its successors'
    rows in the year - the USSR 1989-91: the fifteen republics; Czechoslovakia: the Czech Republic and Slovakia;
    Yugoslavia: Serbia, with the other five republics to 1991 and Montenegro to 2005 (the World Bank codes the
    1991 war in Croatia under Serbia: a series line it gives for Yugoslavia); East Germany: Germany; the two
    Yemens: Yemen. This is the workshop's reading of "territory" for a state whose borders the successors took.

W9. *After COW's coverage.* The own-forces test (b) needs COW's three war files: they end in 2007 (inter- and
    extra-state) and 2014 (intra-state). After 2007 a state-year not shown at war by what remains (intra-state
    wars to 2014; the World Bank's territory to 2024) is **cannot be read**: a state's losses abroad in a war COW
    has not coded are not seen. ``after_cow="no"`` is the variant that reads test (b) as "no" after 2007 (the
    territory test alone); it is never the default. W12 narrows what stays *cannot be read*.

W12. *After COW's coverage, read with UCDP* (FT-001-M4 protocol section 22). UCDP gives no losses by side, so it can
    never say *yes* to test (b), "its own forces lost at least 1,000". It can say **no**: a state that, in a year, is
    party to no conflict of the UCDP/PRIO dataset whose ``cumulative_intensity`` is 1 (1,000 battle-related deaths or
    more since the conflict began) cannot have lost 1,000 in it. A party is any Gleditsch-Ward number listed in
    ``gwno_a``, ``gwno_a_2nd``, ``gwno_b`` or ``gwno_b_2nd`` (each a comma-separated list or empty; secondary
    supporters count). W12 replaces **only** W9's outcome "*cannot be read* because test (b) is unseen": in a year
    after :data:`COW_FULL_END` (W9's own condition, unchanged), when the state is not shown at war by what remains
    and nothing else cannot be read, the state-year is **no** if the state is party to no such conflict that year;
    otherwise it stays *cannot be read*, the conflict ids named in ``detail``'s ``unread``. When W12 gives *no*,
    ``detail`` names UCDP in ``basis``. W12 never makes a *yes*: a *yes* from the territory test (a) or from COW
    stands as before, and a state party to a long, low-intensity conflict that has passed 1,000 stays *cannot be
    read*. UCDP covers 1946-2025; outside those years (none is asked: COW's state system ends in 2024) W12 is not
    applied. The ``after_cow="no"`` variant is unchanged (it never reaches W12). ``ucdp=False`` (``decide``'s
    ``ucdp_parties=None``) is the switch: it runs W9 alone. *What no code holds*: that UCDP's list of parties is
    complete; a state's forces abroad, unlisted as a secondary supporter, would read *no*.

W13. *Gleditsch-Ward numbers to COW's* (the key W12 needs). UCDP numbers states by Gleditsch and Ward (GW), COW by its
    own codes. They agree for every state UCDP names, bar the few lines of :data:`W13` (each with its reason, checked
    against the frozen ``cow/state-system`` file and UCDP's own side names): the united Germany (GW 260, COW 255
    from 1990; COW's 260 is West Germany to 1990), Tonga (GW 972, COW 955 from 1999) and Yemen (GW 678 goes on after 1990, COW's 678 is the Yemen Arab
    Republic to 1990 and 679 the united Yemen). :data:`W13_SAME` lists the numbers a reader would suspect and that
    are the same state in both (Russia / the USSR, Serbia / Yugoslavia, both Vietnams, both Germanies, the South
    Yemen, the successors of Yugoslavia). A GW state-year of the UCDP file that no COW state holds (Hyderabad
    1947-48, Oman before COW holds it in 1971, Tonga before COW holds it in 1999) is never dropped silently:
    :func:`ucdp_unmatched` lists it, and :func:`ucdp_parties` cannot name it for any COW state.

W10. *"At least 1,000" is >= 1,000.* COW's extra-state and intra-state wars whose end is ``-7`` (ongoing at the file's
    end) run to 2007 / 2014; an intra-state participant whose end year is ``-9`` (unknown; thirteen rows) or
    ``-8`` (not applicable; one row, Boko Haram's war of 2013) is read as ongoing to 2014 as well: all are wars
    of 2007-2014 named "to present" or "ongoing". A record with no start
    year raises an error (none exists).

W11. *A dependency at war through its metropole, in the two World Wars* (FT-001-M4-frame-a.md section 13, the audit's
    O3). COW's world wars list no dominion: the United Kingdom's losses are the whole Empire's, so Australia in 1915
    or Canada in 1914, belligerents from August 1914, would be *cannot be read* (W7) and, under P23, counted as
    neutrals. A fixed table, :data:`W11`, applied identically: Australia, Canada, New Zealand and South Africa with
    the United Kingdom, until each enters COW's state system (the entry year is read from the frozen
    ``cow/state-system`` file); India with the United Kingdom until 1947; Finland with Russia to December 1917.
    **Only in a year when the dependency is not a COW state** (COW holds Finland from 1917, so its own reading applies
    to 1917 on; India from 1947), **and only for World War I and World War II**: the wars whose COW totals include the
    dependencies' forces (:data:`WORLD_WARS`, COW war numbers 106 and 139, their names read from the frozen
    inter-state file, which is refused if it does not hold them). When the metropole's war year in that year is *yes*
    through one of them, the dependency's is that *yes*, the world war(s) named and suffixed ``(W11: <money> at war
    through <metropole>)`` (``detail`` names the basis). **In any other case the dependency answers as before, *cannot
    be read* (W7)**, whatever its metropole's war year: a metropole's other wars (the Boer War, a Caucasian war) are no
    evidence that the dependency's forces fought, and COW's totals for them do not count the dependency's losses.
    The table covers the cases the audit found, and no other colony, protectorate or dominion.

Run from the workshop's root with the toolkit's interpreter::

    toolkit/.venv/bin/python bank/maps/FT-001/missions/code/war.py count
    toolkit/.venv/bin/python bank/maps/FT-001/missions/code/war.py lookup FRA 1916
    toolkit/.venv/bin/python bank/maps/FT-001/missions/code/war.py table <path.csv>   # only where you name the path
"""

from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from collections import Counter, defaultdict
from functools import cache
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import economies  # noqa: E402

ROOT = HERE.parents[4]
DATA = ROOT / "data"
VINTAGE = "2026-09-30"
INTER = DATA / "cow" / "inter-state-wars" / VINTAGE / "Inter-StateWarData_v4.0.csv"
EXTRA = DATA / "cow" / "extra-state-wars" / VINTAGE / "Extra-StateWarData_v4.0.csv"
INTRA_ZIP = DATA / "cow" / "intra-state-wars" / VINTAGE / "Intra-State-Wars-v5.1.zip"
INTRA_WARS = "INTRA-STATE WARS v5.1 CSV.csv"
INTRA_STATES = "INTRA-STATE_State_participants v5.1 CSV.csv"
SYSTEM_ZIP = DATA / "cow" / "state-system" / VINTAGE / "System2024.zip"
SYSTEM_CSV = "System2024/system2024.csv"
WB_DEATHS = DATA / "worldbank" / "VC.BTL.DETH" / VINTAGE / "page-001.json"
UCDP_VINTAGE = "2026-10-01"
UCDP_FILE = DATA / "ucdp" / "conflict-dyadic-v26.1" / UCDP_VINTAGE / "UcdpPrioConflict_v26_1.csv"
UCDP_MANIFEST = UCDP_FILE.parent / "MANIFEST.md"
UCDP_PARTY_FIELDS = ("gwno_a", "gwno_a_2nd", "gwno_b", "gwno_b_2nd")   # W12: each a comma-separated list, or empty

THRESHOLD = 1000
WB_FROM = 1989                      # M0: UCDP / the World Bank's series "from 1989"
COW_END = {"inter": 2007, "extra": 2007, "intra": 2014}
COW_FULL_END = min(COW_END.values())    # the year to which all three war files speak
FIRST_YEAR = 1816                   # COW's state system and wars begin here
#: Territory of a dissolved state in the World Bank's series (W8).
SOVIET = ("RUS", "UKR", "BLR", "EST", "LVA", "LTU", "MDA", "GEO", "ARM", "AZE", "KAZ", "KGZ", "TJK", "TKM", "UZB")
YUGOSLAV_REPUBLICS = ("SRB", "HRV", "SVN", "MKD", "BIH", "MNE")
OVERRIDE = {484: "COG"}             # W7: the Republic of the Congo
UNMATCHED: list[tuple[int, str]] = []


class GW(NamedTuple):
    """W13: a Gleditsch-Ward number that is a different COW code in some years."""
    gw: int
    first: int          # the years in which the GW number stands for ``cow`` (inclusive)
    last: int
    cow: int
    reason: str


#: W13: Gleditsch-Ward number -> COW code where they differ. Each line was checked against the frozen COW state-system
#: file (which ccode is held in which years) and against UCDP's own side names ("Government of Germany" for 260 in 2003,
#: "Government of Yemen (North Yemen)" for 678 in 2008). The GW number also keeps standing for the COW code of the
#: same number in the years COW holds it (:func:`gw_numbers_for_cow`).
W13 = (
    GW(260, 1990, 2024, 255,
       "Germany: GW keeps 260 for the united Germany after 1990 (UCDP: 'Government of Germany', 1999-2023); COW's 260 is "
       "the German Federal Republic, 1955-1990, and the united Germany returns under 255, from 1990"),
    GW(678, 1990, 2024, 679,
       "Yemen: GW keeps 678 for the united Yemen after 1990 (UCDP: 'Government of Yemen (North Yemen)' to 2025); COW's 678 "
       "is the Yemen Arab Republic, to 1990, and the united Yemen is 679, from 1990"),
    GW(972, 1999, 2024, 955,
       "Tonga: GW 972, COW 955 (System2024 holds TON 955 from 1999; UCDP: 'Government of Tonga'), added after frames c and "
       "k's fourth-build check (A1, 2026-10-02), which found Tonga's UCDP years read as no"),
)
#: W13: the numbers a reader would suspect and that name the same state in both systems (identity read from the frozen
#: COW state-system file and UCDP's side names; no table line is needed).
W13_SAME = {
    265: "East Germany: GW 265 and COW 265 (German Democratic Republic, 1954-1990)",
    680: "South Yemen: GW 680 and COW 680 (Yemen People's Republic, 1967-1990)",
    345: "Serbia / Yugoslavia: GW 345 and COW 345 are one code all along; COW's System2024 file holds no 340 (Serbia "
         "before 1918 is 345 there too), and UCDP never uses 340",
    365: "Russia / the USSR: GW 365 and COW 365 are one code for the Soviet Union and Russia alike (UCDP: "
         "'Russia (Soviet Union)')",
    816: "Vietnam: GW 816 and COW 816 (the north to 1975, the united Vietnam after; COW's 'Vietnam', 1954-2024)",
    817: "South Vietnam: GW 817 and COW 817 (Republic of Vietnam, 1954-1975)",
    315: "Czechoslovakia: GW 315 and COW 315 (to 1992); the Czech Republic 316 and Slovakia 317 are the same in both",
    341: "Montenegro: GW 341 and COW 341 (from 2006); the other successors of Yugoslavia are the same in both: "
         "Macedonia 343, Croatia 344, Bosnia and Herzegovina 346, Slovenia 349",
}
#: Names for the GW numbers :func:`ucdp_unmatched` lists, as UCDP's own files give them (972 by elimination: in UCDP's
#: row of 2004 for the Iraq war, the 32 numbers of ``gwno_a_2nd`` and the 32 names of ``side_a_2nd`` match one to one,
#: and 972 is the one left for 'Government of Tonga'). A number listed without a name here fails the tests.
UNMATCHED_NAMES = {751: "Hyderabad", 972: "Tonga (before COW holds it, 1999)", 698: "Oman (before COW holds it, 1971)"}


class Own(NamedTuple):
    """One state's losses in one COW war, at the level of the war (W5)."""
    war: str
    kind: str            # inter | intra | extra
    deaths: int | None   # the known total; None = unknown (-9) and the known part under 1,000


# --- reading the files -------------------------------------------------------------------------------------

def _csv(text: str) -> list[dict]:
    """COW's files end their lines with a lone carriage return; keys are stripped (one has a trailing space)."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    rows = []
    for raw in csv.DictReader(io.StringIO(text)):
        row = {(k or "").strip(): (v or "").strip() for k, v in raw.items()}
        if row.get("WarNum"):
            rows.append(row)
    return rows


def _file(path: Path) -> list[dict]:
    return _csv(path.read_bytes().decode("latin-1"))


def _zipped(name: str) -> list[dict]:
    with zipfile.ZipFile(INTRA_ZIP) as z:
        return _csv(z.read(name).decode("latin-1"))


def _int(text: str) -> int:
    return int(float(text))


def spans(row: dict, start: str, end: str, last: int, n: int = 4) -> set[int]:
    """The calendar years a record's fighting touches (W1): its periods 1..n, ``-8`` = no such period,
    ``-7``, and in the intra-state files ``-9`` and ``-8``, as the end of a period that has a start = ongoing at
    the file's end (W10)."""
    years: set[int] = set()
    for i in range(1, n + 1):
        s, e = row.get(f"{start}{i}", "-8"), row.get(f"{end}{i}", "-8")
        s, e = (_int(s) if s else -8), (_int(e) if e else -8)
        if s == -8 and e == -8:
            continue
        if s < 0:
            raise ValueError(f"war {row.get('WarNum')} ({row.get('WarName')}): no start year in period {i}: settle by hand")
        if e in (-7, -8, -9):
            e = last
        if e < s:
            raise ValueError(f"war {row.get('WarNum')} ({row.get('WarName')}): ends ({e}) before it starts ({s})")
        years.update(range(s, min(e, last) + 1))
    return years


def _deaths(values: list[str]) -> int | None:
    """W5: the sum of the known records; None if any is unknown and the known part is under the threshold."""
    known = [_int(v) for v in values if v and _int(v) >= 0]
    unknown = any((not v) or _int(v) < 0 for v in values)
    total = sum(known)
    return None if unknown and total < THRESHOLD else total


@cache
def _own() -> dict[tuple[int, int], list[Own]]:
    """(ccode, year) -> the state's COW wars in that year, with its own losses in each (W5)."""
    groups: dict[tuple[str, str, int], dict] = {}

    def add(kind: str, war: str, name: str, ccode: int, years: set[int], deaths: str) -> None:
        g = groups.setdefault((kind, war, ccode), {"name": name, "years": set(), "deaths": []})
        g["years"] |= years
        g["deaths"].append(deaths)

    for r in _file(INTER):
        add("inter", r["WarNum"], r["WarName"], _int(r["ccode"]), spans(r, "StartYear", "EndYear", COW_END["inter"], 2),
            r["BatDeath"])
    for r in _file(EXTRA):
        state = _int(r["ccode1"]) if _int(r["ccode1"]) > 0 else _int(r["ccode2"])
        if state > 0:
            add("extra", r["WarNum"], r["WarName"], state, spans(r, "StartYear", "EndYear", COW_END["extra"], 2),
                r["BatDeath"])
    for r in _zipped(INTRA_STATES):
        years = spans(r, "StartYr", "EndYr", COW_END["intra"], 4)
        for side, ccode, name, deaths in (("A", r["CcodeA"], r["SideA"], r["Deaths A"]),
                                          ("B", r["CcodeB"], r["SideB"], r["Deaths B"])):
            if _int(ccode) > 0 and name != "-8":
                add("intra", r["WarNum"], r["WarName"], _int(ccode), years, deaths)
    out: dict[tuple[int, int], list[Own]] = defaultdict(list)
    for (kind, war, ccode), g in groups.items():
        own = Own(g["name"], kind, _deaths(g["deaths"]))
        for year in g["years"]:
            out[(ccode, year)].append(own)
    return out


@cache
def _soil() -> tuple[dict[tuple[int, int], list[str]], Counter]:
    """(ccode, year) -> intra-state wars located in the state (W4), and per year the wars with no state located."""
    located: dict[tuple[int, int], list[str]] = defaultdict(list)
    unlocated: Counter = Counter()
    for r in _zipped(INTRA_WARS):
        years = spans(r, "StartYr", "EndYr", COW_END["intra"], 4)
        ccode = _int(r["CcodeA"])
        for year in years:
            if ccode > 0:
                located[(ccode, year)].append(r["WarName"])
            else:
                unlocated[year] += 1
    return located, unlocated


@cache
def _wb() -> tuple[dict[tuple[str, int], float | None], int]:
    """(iso3, year) -> the World Bank's battle-related deaths (None = no value) for every economy row, and the last
    year the series holds any value (W3). Regions and income groups are not economies."""
    economy = {e["id"] for e in json.loads(economies.WB.read_text())[1] if e["region"]["value"] not in ("", "Aggregates")}
    rows: dict[tuple[str, int], float | None] = {}
    last = 0
    for r in json.loads(WB_DEATHS.read_text())[1]:
        iso = r["countryiso3code"]
        if iso not in economy:
            continue
        year = int(r["date"])
        rows[(iso, year)] = r["value"]
        if r["value"] is not None:
            last = max(last, year)
    return rows, last


# --- states: COW codes to the workshop's -------------------------------------------------------------------

@cache
def _states() -> tuple[dict[tuple[int, int], str], dict[tuple[str, int], list[int]], dict[int, str]]:
    """Per (ccode, year) the state's money, per (money, year) its ccodes (with W7's lineage), and each ccode's name."""
    with zipfile.ZipFile(SYSTEM_ZIP) as z:
        rows = list(csv.DictReader(io.StringIO(z.read(SYSTEM_CSV).decode("latin-1").replace("\r", "\n"))))
    primary: dict[tuple[int, int], str] = {}
    by_money: dict[tuple[str, int], list[int]] = defaultdict(list)
    names: dict[int, str] = {}
    bad: dict[tuple[int, str], None] = {}
    for r in rows:
        ccode, year, name = _int(r["ccode"]), _int(r["year"]), r["statenme"].strip()
        names[ccode] = name
        money = OVERRIDE.get(ccode)
        if money is None:
            try:
                money = economies.code(name)
            except KeyError:
                bad[(ccode, name)] = None
                money = f"COW{ccode}"
        primary[(ccode, year)] = money
        monies = {money}
        if ccode == 345:
            monies |= {"YUG", "SCG", "SRB"}
        if ccode == 365:
            monies |= {"RUS"} | ({"SUN"} if 1922 <= year <= 1991 else set())
        if ccode == 300:
            monies |= {"AUT", "HUN"}
        for m in monies:
            by_money[(m, year)].append(ccode)
    UNMATCHED[:] = sorted(bad)
    if bad:
        print("COW state names with no workshop code (kept as COW<ccode>):",
              ", ".join(f"{c} {n}" for c, n in sorted(bad)), file=sys.stderr)
    return primary, dict(by_money), names


def unmatched() -> list[tuple[int, str]]:
    """The COW states (ccode, name) that ``economies.code`` does not know; they keep a ``COW<ccode>`` money."""
    _states()
    return list(UNMATCHED)


def _wb_codes(ccode: int, year: int, money: str) -> tuple[str, ...]:
    """W8: the World Bank rows that make up a state's territory."""
    if ccode == 365 and year <= 1991:
        return SOVIET
    if ccode == 315:
        return ("CZE", "SVK")
    if ccode == 345:
        return YUGOSLAV_REPUBLICS if year <= 1991 else ("SRB", "MNE") if year <= 2005 else ("SRB",)
    if ccode == 265:
        return ("DEU",)
    if ccode in (678, 680):
        return ("YEM",)
    return (money,)


def _wb_territory(ccode: int, year: int, money: str) -> float | None:
    """The battle-related deaths on the state's territory (W3, W8); None when the series cannot be read."""
    rows, last = _wb()
    if not WB_FROM <= year <= last:
        return None
    codes = _wb_codes(ccode, year, money)
    if any((c, year) not in rows for c in codes):
        return None
    return sum(rows[(c, year)] or 0.0 for c in codes)


# --- UCDP: parties of the conflicts, GW numbers to COW codes (W12, W13) ------------------------------------

def _gw_list(text: str) -> list[int]:
    """One ``gwno_*`` cell: a comma-separated list of Gleditsch-Ward numbers, or empty."""
    out = []
    for token in text.split(","):
        token = token.strip()
        if token:
            if not token.isdigit():
                raise ValueError(f"UCDP: a Gleditsch-Ward number that is not a number: {token!r}")
            out.append(int(token))
    return out


@cache
def _ucdp() -> tuple[dict[tuple[int, int], tuple[str, ...]], dict[int, set[int]], int, int]:
    """(gw, year) -> the ids of the conflicts of that year with ``cumulative_intensity`` 1 in which the state is a party
    (any of the four party fields); gw -> every year it is a party to any conflict-year of the file (for
    :func:`ucdp_unmatched`); and the first and last year of the file."""
    serious: dict[tuple[int, int], set[str]] = defaultdict(set)
    seen: dict[int, set[int]] = defaultdict(set)
    years: set[int] = set()
    with open(UCDP_FILE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            year, cum = int(r["year"]), r["cumulative_intensity"].strip()
            if cum not in ("0", "1"):
                raise ValueError(f"UCDP conflict {r['conflict_id']} {year}: cumulative_intensity {cum!r}, expected 0 or 1")
            years.add(year)
            for field in UCDP_PARTY_FIELDS:
                for gw in _gw_list(r[field]):
                    seen[gw].add(year)
                    if cum == "1":
                        serious[(gw, year)].add(r["conflict_id"].strip())
    return ({k: tuple(sorted(v, key=int)) for k, v in serious.items()}, dict(seen), min(years), max(years))


def gw_numbers_for_cow(ccode: int, year: int) -> tuple[int, ...]:
    """The Gleditsch-Ward numbers that stand for a COW state in a year (W13): its own number (the same state in both
    systems unless :data:`W13` says otherwise) and the GW numbers :data:`W13` maps to it."""
    return tuple(sorted({ccode} | {e.gw for e in W13 if e.cow == ccode and e.first <= year <= e.last}))


def cow_codes_for_gw(gw: int, year: int) -> tuple[int, ...]:
    """The COW states a Gleditsch-Ward number stands for in a year (W13), empty if COW holds none (listed by
    :func:`ucdp_unmatched`)."""
    primary, _, _ = _states()
    codes = {e.cow for e in W13 if e.gw == gw and e.first <= year <= e.last} | {gw}
    return tuple(sorted(c for c in codes if (c, year) in primary))


def ucdp_unmatched() -> list[tuple[int, str, tuple[int, ...]]]:
    """W13: the UCDP states (gw, name, years) that map to no COW state in some year in which UCDP lists them as a party,
    1946 to the last year of COW's state system. Never dropped silently: W12 cannot name a conflict for them, which is
    right (no COW state is asked about) and said here. The years after COW's state system (UCDP's 2025) are not asked
    of any COW state and are not listed."""
    primary, _, _ = _states()
    last = max(y for _, y in primary)
    _, seen, _, _ = _ucdp()
    out = []
    for gw in sorted(seen):
        years = tuple(y for y in sorted(seen[gw]) if y <= last and not cow_codes_for_gw(gw, y))
        if years:
            out.append((gw, UNMATCHED_NAMES.get(gw, "?"), years))
    return out


def ucdp_parties(ccode: int, year: int) -> list[str] | None:
    """W12: the ids of the UCDP conflicts of the year, with cumulative intensity 1, to which the COW state is a party
    (empty: none); None when the file does not cover the year (W12 is not applied)."""
    serious, _, first, last = _ucdp()
    if not first <= year <= last:
        return None
    ids = {cid for gw in gw_numbers_for_cow(ccode, year) for cid in serious.get((gw, year), ())}
    return sorted(ids, key=int)


# --- the decision ----------------------------------------------------------------------------------------

def decide(year: int, *, own: list[Own], soil_wars: list[str], wb: float | None, after_cow: str = "cannot be read",
           ucdp_parties: list[str] | None = None) -> dict:
    """M0's war year for one state-year inside the COW state system, from its evidence (pure; the tests call it).

    ``own``: the state's COW wars this year with its own losses (W5); ``soil_wars``: intra-state wars COW locates
    in it (W4); ``wb``: the World Bank's deaths on its territory, None when the series cannot be read (W3);
    ``ucdp_parties`` (W12): the ids of the UCDP conflicts of the year with cumulative intensity 1 to which the state is a
    party, an empty list for none, None when W12 is not applied (the switch off, or a year UCDP does not cover)."""
    if after_cow not in ("cannot be read", "no"):
        raise ValueError("after_cow is 'cannot be read' (default) or 'no' (the variant, W9)")
    yes: list[str] = []
    unread: list[str] = []
    basis: list[str] = []
    ucdp_note: list[str] = []       # W12's no, a ground for a no and a note beside a yes
    for o in own:
        if o.deaths is not None and o.deaths >= THRESHOLD:
            yes.append(o.war)
            basis.append(f"own forces: {o.war} ({o.kind}-state), {o.deaths:,} battle deaths in the war")
        elif o.deaths is None:
            unread.append(f"own losses in {o.war} ({o.kind}-state) are unknown in COW")
        elif o.kind == "inter" and year < WB_FROM:
            unread.append(f"{o.war}: inter-state war, COW places combat by region only: soil cannot be attributed (W6)")
    if year >= WB_FROM:
        if wb is not None:
            if wb >= THRESHOLD:
                yes.append(f"battle-related deaths on its territory: {wb:,.0f}")
                basis.append(f"territory: World Bank VC.BTL.DETH, {wb:,.0f}")
        elif soil_wars:
            yes += soil_wars
            basis += [f"territory: COW intra-state, {w} (the World Bank's series cannot be read here)" for w in soil_wars]
        else:
            unread.append("the World Bank's battle-deaths series has no row for this state-year (W3)")
    else:
        yes += soil_wars
        basis += [f"territory: COW intra-state, {w}" for w in soil_wars]
    if year > COW_FULL_END and after_cow == "cannot be read" and not any(b.startswith("own forces") for b in basis):
        w9 = (f"own forces' losses after COW's coverage (inter- and extra-state to {COW_END['inter']}, "
              f"intra-state to {COW_END['intra']}) (W9)")
        if ucdp_parties is None:                    # W12 not applied: W9 alone
            unread.append(w9)
        elif ucdp_parties:                          # W12: a party to a conflict whose deaths had passed 1,000 by that year: still unread
            unread.append(f"{w9}; UCDP/PRIO v26.1 (W12): party to conflict(s) {', '.join(ucdp_parties)} with cumulative "
                          f"intensity 1 in {year}, so the losses stay unseen")
        else:                                       # W12: party to none: its own forces cannot have lost 1,000 in one
            ucdp_note.append(f"UCDP/PRIO v26.1 (W12): party to no conflict with cumulative intensity 1 in {year}, so its "
                             f"own forces cannot have lost {THRESHOLD:,} in one (test (b) is no)")
    yes = list(dict.fromkeys(yes))
    unread = list(dict.fromkeys(unread))
    if yes:     # a yes stands whatever else cannot be read; what was not read is kept as a note
        return {"status": "yes", "wars": yes, "basis": basis, "unread": [], "notes": unread + ucdp_note}
    return {"status": "cannot be read" if unread else "no", "wars": [], "basis": basis + ucdp_note, "unread": unread,
            "notes": []}


def _evaluate(ccode: int, year: int, after_cow: str, ucdp: bool = True) -> dict:
    """:func:`decide` on one COW state-year's evidence (W12 read through UCDP unless ``ucdp`` is False)."""
    primary, _, _ = _states()
    soil, _unlocated = _soil()
    return decide(year, own=_own().get((ccode, year), []), soil_wars=soil.get((ccode, year), []),
                  wb=_wb_territory(ccode, year, primary[(ccode, year)]), after_cow=after_cow,
                  ucdp_parties=ucdp_parties(ccode, year) if ucdp and year > COW_FULL_END else None)


#: W11: money -> (metropole, last year of the dependency, None: until it enters COW's state system).
W11 = {"AUS": ("GBR", None), "CAN": ("GBR", None), "NZL": ("GBR", None), "ZAF": ("GBR", None),
       "IND": ("GBR", 1946), "FIN": ("RUS", 1917)}
#: W11's wars: COW's war numbers of the two World Wars in the inter-state file, and the names they must carry there.
WORLD_WARS = {"106": "World War I", "139": "World War II"}


@cache
def _world_wars() -> frozenset[str]:
    """The war names of :data:`WORLD_WARS`, read from the frozen inter-state file by war number; refuses a file in which
    a number is missing or carries another name."""
    found = {r["WarNum"]: r["WarName"] for r in _file(INTER) if r["WarNum"] in WORLD_WARS}
    if found != WORLD_WARS:
        raise ValueError(f"COW's inter-state file holds {found} for the war numbers {sorted(WORLD_WARS)}, not {WORLD_WARS}")
    return frozenset(found.values())


def _w11(money: str, year: int, by_money: dict[tuple[str, int], list[int]]) -> str | None:
    """The metropole whose war year a dependency may take in ``year`` (W11), or None."""
    if money not in W11 or (money, year) in by_money:          # a COW state answers for itself
        return None
    metropole, last = W11[money]
    entry = min((y for (m, y) in by_money if m == money), default=None)
    if last is not None and year > last or last is None and entry is not None and year >= entry:
        return None
    return metropole


def detail(money: str, year: int | str, *, after_cow: str = "cannot be read", ucdp: bool = True) -> dict:
    """The war year of a money in a year, with its evidence: ``status`` (yes / no / cannot be read), ``wars``,
    ``basis``, ``unread`` (why it cannot be read), ``notes`` (what a *yes* did not need to read), ``ccodes`` and
    ``open_unlocated`` (W4). ``ucdp=False`` runs W9 without W12."""
    year = int(str(year)[:4])
    primary, by_money, names = _states()
    base = {"money": money, "year": year, "wars": [], "basis": [], "ccodes": [], "open_unlocated": 0, "notes": []}
    ccodes = by_money.get((money, year), [])
    metropole = _w11(money, year, by_money)
    if metropole:
        d = detail(metropole, year, after_cow=after_cow, ucdp=ucdp)
        worlds = [w for w in d["wars"] if w in _world_wars()]
        if d["status"] == "yes" and worlds:                      # W11: a World War only; else W7's answer below
            tag = f"(W11: {money} at war through {metropole})"
            return {**d, "money": money, "wars": [f"{w} {tag}" for w in worlds],
                    "basis": [*d["basis"], f"W11: {money} is no COW state in {year}; {metropole}'s war year in "
                                           f"{', '.join(worlds)}"], "ccodes": []}
    if not ccodes:
        why = (f"before COW's coverage ({FIRST_YEAR})" if year < FIRST_YEAR
               else f"after the COW state system's coverage ({max(y for _, y in primary)})" if year > max(y for _, y in primary)
               else f"{money} is not a member of the COW state system in {year}")
        return {**base, "status": "cannot be read", "unread": [why + " (W7)"]}
    results = [_evaluate(c, year, after_cow, ucdp) for c in ccodes]
    # a money that stands for two COW states in one year (none in the system) would be yes if either is
    best = next((r for r in results if r["status"] == "yes"), None) or next(
        (r for r in results if r["status"] == "cannot be read"), results[0])
    return {**base, **best, "ccodes": ccodes, "open_unlocated": _soil()[1].get(year, 0)}


def war_year(money: str, year: int | str, *, after_cow: str = "cannot be read", ucdp: bool = True) -> str:
    """``"yes: <war name; ...>"``, ``"no"`` or ``"cannot be read"`` (M0 section 1; readings W1-W13 above)."""
    d = detail(money, year, after_cow=after_cow, ucdp=ucdp)
    return f"yes: {'; '.join(d['wars'])}" if d["status"] == "yes" else d["status"]


# --- the table and the counts ------------------------------------------------------------------------------

TABLE_FIELDS = ["money", "also", "year", "ccode", "state", "war_year", "status", "wars", "basis", "unread",
                "wb_deaths", "open_unlocated"]


def table(*, after_cow: str = "cannot be read", ucdp: bool = True) -> list[dict]:
    """One row per state-year of COW's state system (1816-2024): its war year and what it rests on."""
    primary, by_money, names = _states()
    also: dict[tuple[int, int], list[str]] = defaultdict(list)
    for (money, year), ccodes in by_money.items():
        for c in ccodes:
            if money != primary[(c, year)]:
                also[(c, year)].append(money)
    rows = []
    for (ccode, year), money in sorted(primary.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        d = {**_evaluate(ccode, year, after_cow, ucdp), "open_unlocated": _soil()[1].get(year, 0)}
        wb = _wb_territory(ccode, year, money)
        rows.append({"money": money, "also": ";".join(sorted(also[(ccode, year)])), "year": year, "ccode": ccode,
                     "state": names[ccode], "war_year": f"yes: {'; '.join(d['wars'])}" if d["status"] == "yes" else d["status"],
                     "status": d["status"], "wars": " | ".join(d["wars"]), "basis": " | ".join(d["basis"]),
                     "unread": " | ".join(d["unread"]), "wb_deaths": "" if wb is None else f"{wb:.0f}",
                     "open_unlocated": d["open_unlocated"]})
    return rows


ERAS = (("metal, to 1913", 0, 1913), ("gold exchange and Bretton Woods, 1914-1971", 1914, 1971),
        ("fiat, 1972 on", 1972, 9999))
COVERAGE = (("1816-1988: COW", 1816, 1988), ("1989-2007: COW + World Bank", 1989, 2007),
            ("2008-2014: intra-state COW + World Bank", 2008, 2014), ("2015-2024: World Bank only", 2015, 2024))


def tally(rows: list[dict], bands) -> list[tuple[str, int, int, int]]:
    out = []
    for label, a, b in bands:
        c = Counter(r["status"] for r in rows if a <= r["year"] <= b)
        out.append((label, c["yes"], c["no"], c["cannot be read"]))
    return out


def span_overcount() -> tuple[int, int]:
    """W2's check: state-years 1989-2014 in which COW locates a war on the state's soil (span reading) and the
    World Bank's series can be read; how many of them have under 1,000 deaths there."""
    soil, _ = _soil()
    primary, _, _ = _states()
    both = under = 0
    for (ccode, year), wars in soil.items():
        if WB_FROM <= year <= COW_END["intra"] and (ccode, year) in primary:
            wb = _wb_territory(ccode, year, primary[(ccode, year)])
            if wb is not None:
                both += 1
                under += wb < THRESHOLD
    return both, under


def count() -> None:
    rows = table()
    variant = table(after_cow="no")
    no_ucdp = table(ucdp=False)
    print(f"{len(rows)} state-years of the COW state system ({rows[0]['year']}-{rows[-1]['year']}), "
          f"{len({r['ccode'] for r in rows})} COW states")
    for title, data in (("default reading (after COW's coverage: cannot be read)", rows),
                        ("variant ucdp=False (W9 alone, without W12)", no_ucdp),
                        ("variant after_cow='no'", variant)):
        print(f"\n{title}\n{'band':52s}{'yes':>8s}{'no':>8s}{'cannot':>8s}")
        for bands in (ERAS, COVERAGE):
            for label, y, n, c in tally(data, bands):
                print(f"{label:52s}{y:8d}{n:8d}{c:8d}")
            print()
        total = Counter(r["status"] for r in data)
        print(f"{'all':52s}{total['yes']:8d}{total['no']:8d}{total['cannot be read']:8d}")
    why = Counter()
    for r in rows:
        if r["status"] == "cannot be read":
            for u in r["unread"].split(" | "):
                why[u.split(":")[0][:70] if "soil" not in u else "an inter-state participant's soil (W6)"] += 1
    print("\nwhy 'cannot be read' (a state-year may have several reasons):")
    for k, v in why.most_common():
        print(f"{v:7d}  {k}")
    by_basis = Counter()
    for r in rows:
        if r["status"] == "yes":
            for b in r["basis"].split(" | "):
                by_basis[b.split(":")[0]] += 1
    print("\nyes by basis:", dict(by_basis))
    both, under = span_overcount()
    print(f"\nW2 check, 1989-2014: {both} state-years with a COW intra-state war on the soil and a World Bank value; "
          f"{under} of them under {THRESHOLD} deaths there")
    print("unlocated intra-state war-years (W4), state-years before 1989 answered 'no' while one was open:",
          sum(1 for r in rows if r["year"] < WB_FROM and r["status"] == "no" and r["open_unlocated"]))
    print("unmatched COW names:", unmatched() or "none")
    print("UCDP states that map to no COW state (W13), GW number, name, state-years:",
          [(g, n, len(ys)) for g, n, ys in ucdp_unmatched()] or "none")


if __name__ == "__main__":
    if sys.argv[1:2] == ["count"]:
        count()
    elif sys.argv[1:2] == ["lookup"] and len(sys.argv) == 4:
        d = detail(sys.argv[2], sys.argv[3])
        print(war_year(sys.argv[2], sys.argv[3]))
        print(json.dumps({k: v for k, v in d.items() if k != "wars"}, indent=1))
    elif sys.argv[1:2] == ["table"] and len(sys.argv) == 3:
        out = table()
        with open(sys.argv[2], "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=TABLE_FIELDS)
            w.writeheader()
            w.writerows(out)
        print(f"{len(out)} rows -> {sys.argv[2]}")
    else:
        print(__doc__)
        sys.exit(2)
