"""FT-001 M3, first part: frame c, strained monies — the rules (FT-001-M3-panel.md, section 4; M0 v4.2 5 c).

The rules, on plain per-year readings, tested on synthetic series (``test_panel.py``), then the build of
``data/reconstructed/ft001-c/`` (``strain.py build``) from ``panel.py``'s readers (debt, deficits, central-bank
credit and GDP, C15, the state in default per creditor class, Garriga, Chinn-Ito), M4's ``war.py`` (war years)
and ``frame_a.EURO_ENTRY`` (the euro's changeovers), frame b's committed lists and the acts list's H1 lines.

- **Routes** (c1): c1 debt/GDP >= 90; c2 deficit/GDP >= 3; c3 s >= 50 with the deficit >= 3; c4 a C15 episode
  crossing c in the year. Ties c1 > c2 > c3 > c4.
- **Entries and spells** (c2, R20): the first year a route is met; the next entry is the first year at or after
  entry + H with a route met, **whatever the earlier entry's status**.
- **Outcome over H** (c8): broke (frame b's crossing from entry + 1 to entry + H), broke and restored (restored by
  the end of entry + H), held (no crossing, π readable every year), else cannot be read; past the common end,
  censored whatever happened (c10, R27), with what happened so far.
- **Apart** (c7): already inflating (π(y) >= 10 in the entry year or the year before), past frame b's onset (the
  first break crossing in or after the entry year, its onset on or before the entry; its onset unreadable, the
  π-only onset decides when it is on or before the entry, else cannot be read) (R26).
"""

from __future__ import annotations

from dataclasses import dataclass

ROUTES = ("c1", "c2", "c3", "c4")


@dataclass(frozen=True)
class Lines:
    c1: float = 90.0
    c2: float = 3.0
    c3: float = 50.0
    c3_min_deficit: float = 3.0
    lower: float = 10.0


def met(reading: dict[str, float | None], lines: Lines = Lines()) -> list[str]:
    """The routes met in one year, in tie order. ``reading`` holds 'debt', 'deficit', 's' (c3's measure) and
    'c4' (the C15 measure of an episode crossing c that year, else None)."""
    out = []
    if reading.get("debt") is not None and reading["debt"] >= lines.c1:
        out.append("c1")
    if reading.get("deficit") is not None and reading["deficit"] >= lines.c2:
        out.append("c2")
    if reading.get("s") is not None and reading.get("deficit") is not None and reading["s"] >= lines.c3 \
            and reading["deficit"] >= lines.c3_min_deficit:
        out.append("c3")
    if reading.get("c4") is not None:
        out.append("c4")
    return out


def entries(met_by_year: dict[int, list[str]], H: int) -> list[tuple[int, str, list[str]]]:
    """(year, route, every route met) of each entry: one spell per H, whatever each entry's status."""
    out, allowed = [], None
    for year in sorted(met_by_year):
        routes = met_by_year[year]
        if routes and (allowed is None or year >= allowed):
            out.append((year, routes[0], list(routes)))
            allowed = year + H
    return out


def _year(label: str) -> int:
    return int(label[:4])


def already_inflating(pi_annual: dict[int, float], entry: int, lower: float = 10.0) -> str:
    """'yes', 'no' or 'cannot be read'."""
    values = [pi_annual.get(entry), pi_annual.get(entry - 1)]
    if any(v is not None and v >= lower for v in values):
        return "yes"
    if any(v is None for v in values):
        return "cannot be read"
    return "no"


def bound_year(crossing: str, bound_months: int = 36) -> int:
    """The year of a crossing's bound (b5): crossing - ``bound_months`` for a month, - bound_months / 12 years for
    a year."""
    if len(crossing) >= 7:
        t = int(crossing[:4]) * 12 + int(crossing[5:7]) - 1 - bound_months
        return t // 12
    return int(crossing[:4]) - bound_months // 12


def past_onset(breaks: list[dict], entry: int) -> str:
    """'yes', 'no' or 'cannot be read': is the entry on or after the onset of the first break crossing in or after
    the entry year? ``breaks`` hold 'crossing', 'onset' (label or ''), 'pi_only' (label or ''), 'pi_only_bound'
    and 'bound_year' (``bound_year``; computed at 36 months when absent).

    **R26 as amended after frame c's audit (B1; the protocol's section 8)**: b5 dates every onset within its
    bound, so a break whose bound falls after the entry year has its onset after the entry: **no**, whatever the
    onset reading. Inside the bound: a readable onset decides; an unreadable one gives "yes" when the π-only
    onset (not at the bound) is on or before the entry (the true onset is no later), else *cannot be read* —
    the residual (the audit's M5), printed and read both ways. A π-only onset at the bound is never "yes" (O1
    of frame b's audit)."""
    later = [b for b in breaks if _year(b["crossing"]) >= entry]
    if not later:
        return "no"
    b = min(later, key=lambda b: b["crossing"])
    by = b.get("bound_year")
    if by is None:
        by = bound_year(b["crossing"])
    if by > entry:
        return "no"
    if b["onset"]:
        return "yes" if _year(b["onset"]) <= entry else "no"
    if b["pi_only"] and not b.get("pi_only_bound") and _year(b["pi_only"]) <= entry:
        return "yes"
    return "cannot be read"


def during_break(breaks: list[dict], entry: int, undatable=None) -> str:
    """**R26 completed (O1 of frame c's audit)**: 'yes' when the money's latest crossing before the entry year is
    not restored before the entry year begins — a restoration dated inside the entry year leaves it 'yes' (the
    entry year is not wholly outside the break) — else 'no'. Every frame b line counts, apart ones included.
    **N1 of the re-check**: ``undatable(break, entry)`` True (``breaks.restoration_undatable``: a restoration the
    readings show before the entry, which frame b cannot date) makes it *cannot be read* instead of 'yes'."""
    earlier = [b for b in breaks if _year(b["crossing"]) < entry]
    if not earlier:
        return "no"
    b = max(earlier, key=lambda b: b["crossing"])
    restored = b.get("restored") or ""
    if restored and _year(restored) < entry:
        return "no"
    if undatable is not None and undatable(b, entry):
        return "cannot be read"
    return "yes"


def outcome(breaks: list[dict], entry: int, H: int, pi_years: set[int], end: int, exit_year: int | None = None,
            exit_text: str = "") -> dict:
    """The spell's outcome and status over H (c8, c9, c10). ``breaks`` hold 'crossing', 'restored', 'onset' —
    every line of frame b, apart ones included (the audit's M7). ``exit_year``: a competing exit dated on
    1 January of that year (c9: the euro's changeovers), which ends the spell when it falls inside the horizon
    and by the common end: a crossing before it is the outcome; none, with π readable in every year before it,
    is *ended unbroken* (the crossing test of "no crossing in the 12 months before" is met by construction; the
    announcement 12 months before is read as met, as frame a reads it, A3)."""
    stop = entry + H
    if exit_year is not None and exit_year <= stop and exit_year <= end:
        within = sorted((b for b in breaks if entry + 1 <= _year(b["crossing"]) <= exit_year - 1),
                        key=lambda b: b["crossing"])
        if within:
            b = within[0]
            restored = b.get("restored") or ""
            kind = "broke and restored" if restored and _year(restored) <= exit_year - 1 else "broke"
            return {"status": "counted", "outcome": kind, "outcome_date": b["crossing"], "onset_date": b["onset"],
                    "restored": restored if kind == "broke and restored" else "", "so_far": "", "exit": ""}
        if all(y in pi_years for y in range(entry + 1, exit_year)):
            return {"status": "ended unbroken", "outcome": "", "outcome_date": "", "onset_date": "", "restored": "",
                    "so_far": "no crossing before the exit", "exit": exit_text}
        return {"status": "cannot be read", "outcome": "", "outcome_date": "", "onset_date": "", "restored": "",
                "so_far": "π unreadable in a year before the exit, no crossing", "exit": exit_text}
    within = sorted((b for b in breaks if entry + 1 <= _year(b["crossing"]) <= stop), key=lambda b: b["crossing"])
    if stop > end:
        seen = [b for b in within if _year(b["crossing"]) <= end]
        so_far = f"crossing {seen[0]['crossing']}" if seen else "no crossing to the common end"
        return {"status": "censored", "outcome": "", "outcome_date": "", "onset_date": "", "restored": "",
                "so_far": so_far, "exit": ""}
    if within:
        b = within[0]
        restored = b.get("restored") or ""
        kind = "broke and restored" if restored and _year(restored) <= stop else "broke"
        return {"status": "counted", "outcome": kind, "outcome_date": b["crossing"], "onset_date": b["onset"],
                "restored": restored if kind == "broke and restored" else "", "so_far": "", "exit": ""}
    if all(y in pi_years for y in range(entry + 1, stop + 1)):
        return {"status": "counted", "outcome": "held", "outcome_date": "", "onset_date": "", "restored": "",
                "so_far": "", "exit": ""}
    return {"status": "cannot be read", "outcome": "", "outcome_date": "", "onset_date": "", "restored": "",
            "so_far": "π unreadable in a year of the horizon, no crossing", "exit": ""}


def terciles(values: list[float]) -> tuple[float, float]:
    """The two cut-points of a route's entry measures (R21): the 1/3 and 2/3 quantiles, linear interpolation."""
    xs = sorted(values)
    if not xs:
        raise ValueError("no measure")

    def q(p: float) -> float:
        pos = p * (len(xs) - 1)
        lo = int(pos)
        hi = min(lo + 1, len(xs) - 1)
        return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)
    return q(1 / 3), q(2 / 3)


def tercile(value: float, cuts: tuple[float, float]) -> int:
    return 1 if value <= cuts[0] else 2 if value <= cuts[1] else 3


def era(year: int) -> tuple[str, bool]:
    """The era of an annual date: that of its last day (R22); True when the year straddles two eras."""
    if year <= 1913:
        return "metal", False
    if year == 1914:
        return "gold exchange and Bretton Woods", True
    if year <= 1970:
        return "gold exchange and Bretton Woods", False
    return "fiat", year == 1971


# === Frame c's assembly (written, and tested on synthetic readings, before any real series was read for c) ======

APART_REASONS = ("convertible at entry", "already inflating", "during a break", "past frame b's onset",
                 "a war year at entry")


def status_of(apart: dict[str, str], out: dict) -> tuple[str, str]:
    """(status, reason). Order (added in code before any series was read; the exit added with the ECB's dates):
    an apart reason read 'yes' makes the line apart; else a spell past the common end is censored whatever
    happened (R27), and one a competing exit ends is *ended unbroken* (c9); else an apart reason unreadable
    makes it *cannot be read* (the entry may not be an entrant); else the outcome's own status (c8)."""
    yes = [k for k in APART_REASONS if apart.get(k) == "yes"]
    if yes:
        return "apart", "; ".join(yes)
    if out["status"] == "censored":
        return "censored", "entry + H passes the annual common end"
    if out["status"] == "ended unbroken":
        return "ended unbroken", "a competing exit inside the horizon: " + out["exit"]
    unread = [k for k in APART_REASONS if apart.get(k) == "cannot be read"]
    if unread:
        return "cannot be read", "; ".join(f"{k}: cannot be read" for k in unread)
    if out["status"] == "cannot be read":
        return "cannot be read", out["so_far"]
    return out["status"], ""


def war_reading(war: str) -> tuple[str, list[str]]:
    """(the war year's value for the apart test, flags) under the variant ``war-unreadable-as-no`` (M4's P23):
    a war year that *cannot be read* at entry is read as no war, flagged ``war_unreadable_at_entry``. The
    headline reads R14 as M0 section 1 says, "cannot be read, never none" (the protocol's section 8, O3 of
    frame c's audit): an unreadable war year makes the line *cannot be read*."""
    if war == "cannot be read":
        return "no", ["war_unreadable_at_entry"]
    return war, []


def breaks_from_b(rows: list[dict], bound_months: int = 36) -> dict[str, list[dict]]:
    """money -> frame b's lines as the rules here read them: 'crossing' (entry_date), 'restored' (outcome_date
    when restored), 'onset' (break_onset, '' when unreadable), 'pi_only' (onset_pi_only's date, '' when
    unreadable), 'pi_only_bound', 'ifs_break', 'b_status'. Every line of the list, counted or apart, is a
    crossing (the audit's M7)."""
    out: dict[str, list[dict]] = {}
    for r in rows:
        raw = r.get("onset_pi_only", "")
        pi_only = raw.split(" ")[0]
        out.setdefault(r["money"], []).append({
            "crossing": r["entry_date"],
            "restored": r["outcome_date"] if r["outcome"] == "restored" else "",
            "onset": r.get("break_onset", ""),
            "pi_only": "" if pi_only in ("", "cannot") else pi_only,
            "pi_only_bound": raw.endswith("(bound)"),
            "bound_year": bound_year(r["entry_date"], bound_months),
            "ifs_break": r.get("ifs_break", ""),
            "b_status": r["status"]})
    for v in out.values():
        v.sort(key=lambda b: b["crossing"])
    return out


def seam_at(sources: dict[int, str], year: int) -> bool:
    """A reading whose source differs from the year before's (both read)."""
    return year in sources and (year - 1) in sources and sources[year] != sources[year - 1]


def entry_flags(entry: int, routes_met: list[str], readable: dict[int, set[str]], sources: dict[str, dict[int, str]],
                first_year: int | None, lines: Lines = Lines()) -> list[str]:
    """R20 and R30's flags for an entry. ``readable``: year -> the routes c1-c3 readable then (c4's readability is
    not known per year: C15 lists episodes, not the years its panel read — so c4 enters no flag here);
    ``sources``: 'c1'/'c2' -> year -> source. **R30 narrowed (M1 of frame c's audit)**: c3 is tested only where
    its deficit floor lies below c2's line, i.e. only where c3 could enter."""
    flags = []
    if first_year is not None and entry == first_year:
        flags.append("met_at_record_start")
    if any(r in routes_met and seam_at(sources.get(r, {}), entry) for r in ("c1", "c2")):
        flags.append("entry_at_seam")
    c3_can_enter = lines.c3_min_deficit < lines.c2
    wanted = {"c1", "c2"} | ({"c3"} if c3_can_enter and entry - 1 >= 1948 else set())
    if not wanted <= readable.get(entry - 1, set()):
        flags.append("route_unreadable_before")
    return flags


PANEL_SPAN_END = {"1": 1915, "2": 1936}   # the last year each panel's changes are coded (M4)


def convertible_before_1971(year: int, p1: tuple | None, p2: tuple | None) -> str:
    """"Convertible at entry" for an annual entry to 1970, from frame a's panels (the protocol's section 8, O4).
    ``p1`` = (adoption year, change year or None, act) of a panel 1 member; ``p2`` = (return year, exit year or
    None, act) of a panel 2 member. Readings of the boundaries (an annual entry is read at its year's last day,
    as R22 and the 1971 reading): the start year itself is convertible (the adoption or return lies inside it);
    the years before the change year are convertible; a member with no change is convertible to its panel's
    last coded year (1915, 1936); panel 2's end is the first of Bernanke and James's three dates
    (``panel.panel2_end``; M4's section 13: an exchange control ends redemption on demand, M0 section 1);
    **the end year itself is "no" when a suspension or an exchange control is dated in it** (at the year's end
    redemption on demand has stopped) and *cannot be read* when only a devaluation is (convertibility at a new
    parity is not told); 1937-1970 *cannot be read* whatever
    (M4 section 10.7), and every other year and money *cannot be read*."""
    if 1937 <= year <= 1970:
        return "cannot be read"
    verdicts = []
    for panel, rec in (("1", p1), ("2", p2)):
        if rec is None:
            continue
        start, end, act = rec
        last = (end - 1) if end is not None else PANEL_SPAN_END[panel]
        if start <= year <= last:
            verdicts.append("yes")
        elif end is not None and year == end and ("suspension" in act or "exchange control" in act):
            verdicts.append("no")
    if "yes" in verdicts:
        return "yes"
    if "no" in verdicts:
        return "no"
    return "cannot be read"


BOARDS_READ_TO = (2016, 10, 1)        # the chronologies are read to October 2016 (FT-001-M3-boards.md)


def _first_day(text: str) -> tuple[int, int, int] | None:
    """B3: a start is the first day of its precision ('1983' -> 1 January 1983); None when it cannot be read."""
    parts = text.strip().split("-")
    try:
        nums = [int(x) for x in parts]
    except ValueError:
        return None
    if not 1 <= len(nums) <= 3:
        return None
    return (nums[0], nums[1] if len(nums) > 1 else 1, nums[2] if len(nums) > 2 else 1)


def _end_exclusive(text: str) -> tuple[int, int, int] | None:
    """B3: an end given to the day is the switch date (the next period starts on it); to the month or the year,
    the period runs through that month or year (the chronologies' 'April 1994-April 1995', then 'May 1995-'), so
    the first day after it. None when it cannot be read."""
    parts = text.strip().split("-")
    try:
        nums = [int(x) for x in parts]
    except ValueError:
        return None
    if len(nums) == 3:
        return tuple(nums)
    if len(nums) == 2:
        return (nums[0] + 1, 1, 1) if nums[1] == 12 else (nums[0], nums[1] + 1, 1)
    if len(nums) == 1:
        return (nums[0] + 1, 1, 1)
    return None


def board_at(periods: list[dict], entry: int, with_comments: bool = False) -> tuple[str, bool]:
    """(verdict, carried) for an entry whose lagged class is 2 (B5): 'yes' when a board period is in force on 31
    December of the year before the entry, 'no' when none is and every period's dates can be read, else 'cannot
    be read'. Past the chronologies' end, October 2016 is read and ``carried`` is True. ``periods``: the boards
    list's lines of one money (``start``, ``end`` — empty when it runs to the end — and ``label``); comment-only
    lines (B2) count only ``with_comments``."""
    day = (entry - 1, 12, 31)
    carried = day >= BOARDS_READ_TO
    if carried:
        day = BOARDS_READ_TO
    unreadable = False
    for p in periods:
        if p["label"] == "comment" and not with_comments:
            continue
        start = _first_day(p["start"])
        end = _end_exclusive(p["end"]) if p["end"].strip() else (9999, 1, 1)
        if start is None or end is None:
            unreadable = True
            continue
        if start <= day < end:
            return "yes", carried
    return ("cannot be read" if unreadable else "no"), carried


def claim2_mde(rows: list[dict], key: str = "supports_count", base: float = 0.6, from_year: int = 1970) -> dict:
    """The smallest detectable effect of claim 2's headline comparison (80% power, 5% one-sided), **on no
    outcome**: the Mantel-Haenszel difference in share held between "two or more" and "one or none" supports,
    matched on route, tercile, era and the state in default, with a share of ``base`` in every stratum (M0's
    floors take "a share near 0.6"), by the normal approximation; strata with both sides only. Rows: counted
    lines from 1970 whose separator is read. Returns the MDE in points (None when no stratum has both sides)
    and the lines per side. A line whose default at entry cannot be read is in no stratum (N3 of the re-check)."""
    strata: dict[tuple, list[int]] = defaultdict(lambda: [0, 0])
    for r in rows:
        if r["status"] != "counted" or int(r["entry_date"]) < from_year:
            continue
        side = {"two or more": 0, "one or none": 1}.get(r[key])
        if side is None or r["default_at_entry"] not in ("yes", "no"):     # N3: M0's stratum is in default or not
            continue
        strata[(r["route"], str(r["tercile"]), r["era"], r["default_at_entry"])][side] += 1
    n = [sum(v[0] for v in strata.values()), sum(v[1] for v in strata.values())]
    both = [(a, b) for a, b in strata.values() if a and b]
    if not both:
        return {"mde_points": None, "per_side": n, "strata_with_both_sides": 0}
    w = [a * b / (a + b) for a, b in both]
    var = sum(wk ** 2 * base * (1 - base) * (1 / a + 1 / b) for wk, (a, b) in zip(w, both)) / sum(w) ** 2
    return {"mde_points": round(100 * (1.6449 + 0.8416) * var ** 0.5, 1), "per_side": n,
            "strata_with_both_sides": len(both), "matched_per_side": [sum(a for a, _ in both), sum(b for _, b in both)]}


def war_in_h(war: dict[int, str], entry: int, H: int) -> str:
    """Claim 2's variant: the war years inside the horizon, 'n' or 'n (+k unreadable)'."""
    years = range(entry + 1, entry + H + 1)
    yes = sum(war.get(y) == "yes" for y in years)
    unread = sum(war.get(y, "cannot be read") == "cannot be read" for y in years)
    return f"{yes}" + (f" (+{unread} unreadable)" if unread else "")


# === The build: data/reconstructed/ft001-c/ =======================================================================

import csv  # noqa: E402
import sys  # noqa: E402
from collections import Counter, defaultdict  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
OUT = ROOT / "data" / "reconstructed" / "ft001-c"
B_DIR = ROOT / "data" / "reconstructed" / "ft001-b"
ACTS_DIR = ROOT / "data" / "reconstructed" / "ft001-acts"
BOARDS_DIR = ROOT / "data" / "reconstructed" / "ft001-boards"
CODER = "script: missions/code/strain.py"
UNITS = {"c1": "% of GDP (debt)", "c2": "% of GDP (deficit)", "c3": "% of the deficit (central-bank credit)",
         "c4": "% of GDP (base money's rise, C15)"}
DEBT_LOC = {"HPDD": "dbnomics/IMF/HPDD/A~~GGXWDG_GDP", "WEO": "dbnomics/IMF/WEO_2025-04/~GGXWDG_NGDP~pcent_gdp",
            "Reinhart-Rogoff": "reinhart-rogoff/debt-to-gdp", "JST": "jst/macrohistory JSTdatasetR6.dta, debtgdp x 100"}
DEFICIT_LOC = {"WEO": "dbnomics/IMF/WEO_2025-04/~GGXCNL_NGDP~pcent_gdp (minus net lending)",
               "JST": "jst/macrohistory JSTdatasetR6.dta, 100 (expenditure - revenue) / gdp"}
FIELDS = ["period", "value", "unit", "source", "locator", "note", "uncertainty", "money", "frame", "route",
          "entry_date", "entry_measure", "entry_measure_date", "outcome", "outcome_date", "onset_date", "responses",
          "exit", "status", "coder", "rules_sha256", "reason", "H", "routes_met", "debt_pct_gdp_source",
          "deficit_pct_gdp_source", "c3_units_ok", "tercile", "era", "era_boundary_year", "default_at_entry",
          "default_at_entry_total_stock", "taken_back", "limit_by_rule", "limit_by_rule_cap_only",
          "limit_by_institution", "force", "habit", "world_demand", "supports_count", "supports_count_without_pegs",
          "supports_count_without_taken_back", "supports_count_cap_025", "supports_count_cap_075",
          "supports_count_index_04", "supports_count_index_06", "supports_count_ka_01", "supports_count_ka_05",
          "regime_at_entry", "regime_note", "split_at_entry", "convertible_at_entry", "already_inflating",
          "during_a_break", "past_frame_b_onset", "war_at_entry", "war_years_in_H", "restored_date", "so_far", "flags", "c4_c",
          "euro_changeover_year", "shared_or_foreign_money", "new_money_rule", "variant"]


@dataclass(frozen=True)
class Spec:
    H: int = 10
    lines: Lines = Lines()
    entry_year_counted: bool = False     # the already-inflating variant: only the year before sets apart
    drop_flag: str = ""
    regime_carried_out: bool = False
    c4_list: str = "headline"
    b_list: str = "series.csv"
    war_after_cow: str = "cannot be read"
    war_ucdp: bool = True                # FT-001-M3-panel.md section 9: W12 on; off in the variant war-before-w12
    default_total: bool = False
    war_unreadable_as_no: bool = False
    b_bound: int = 36
    boards_with_comments: bool = False   # FT-001-M3-boards.md B2: comment-only boards counted


HEADLINE = Spec()
VARIANTS = {
    "H5": Spec(H=5), "H20": Spec(H=20),
    "c1-60": Spec(lines=Lines(c1=60.0)), "c2-5": Spec(lines=Lines(c2=5.0)),
    "c3-25": Spec(lines=Lines(c3=25.0)), "c3-75": Spec(lines=Lines(c3=75.0)),
    "entry-year-counted": Spec(entry_year_counted=True),
    **{f"drop-{f.replace('_', '-')}": Spec(drop_flag=f) for f in
       ("met_at_record_start", "entry_at_seam", "route_unreadable_before", "c4_flag", "c1_outside_fit",
        "era_boundary_year", "ifs_break")},
    "regime-carried-out": Spec(regime_carried_out=True),
    "c4-smoothing": Spec(c4_list="smoothing"),
    "war-after-cow-no": Spec(war_after_cow="no"),
    "war-before-w12": Spec(war_ucdp=False),
    "war-unreadable-as-no": Spec(war_unreadable_as_no=True),
    "default-total": Spec(default_total=True),
    "boards-with-comments": Spec(boards_with_comments=True),
}


B_LOWER = {"lower-5": 5.0, "lower-15": 15.0}      # M7 of frame c's audit: "already inflating" at b's lower line
B_BOUND = {"bound-24": 24, "bound-60": 60}       # B1: a break's bound as that list dates it


def _b_variant_specs() -> dict[str, Spec]:
    out = {}
    for p in sorted(B_DIR.glob("variant-*.csv")):
        name = p.stem.removeprefix("variant-")
        out[f"b-{name}"] = Spec(b_list=p.name, lines=Lines(lower=B_LOWER.get(name, 10.0)),
                                b_bound=B_BOUND.get(name, 36))
    return out


def b_params(spec: "Spec"):
    """The frame b parameters of the list a spec reads (its ``drop_flagged`` included: the third build's check,
    F1), at the spec's lower line."""
    import breaks as B
    from dataclasses import replace
    name = spec.b_list.removeprefix("variant-").removesuffix(".csv")
    return replace(B.VARIANTS.get(name, B.HEADLINE), lower=spec.lines.lower)


def _read_csv(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


class Readings:
    """Every money's per-year readings for frame c, read once."""

    def __init__(self):
        import panel as P
        self.P = P
        self.pan = P.Panel()
        self.end = P.common_end(self.pan.have_annual(), 1)
        self.c4 = {name: P.c4_by_year(eps) for name, eps in P.c15_lists().items()}
        c4_monies = set().union(*(set(v) for v in self.c4.values()))
        monies = set(self.pan.monies) | set(P.hpdd()) | set(P.weo("GGXWDG_NGDP")) | set(P.weo("GGXCNL_NGDP")) \
            | set(P.rr_debt()) | set(P.jst_fiscal()) | c4_monies
        self.monies = sorted(m for m in monies if m)
        from frame_a import EURO_ENTRY, EURO_EXIT_SOURCE
        # c9: the euro's changeovers, from frame a's EURO_ENTRY (the ECB's page, frozen; 1074f44), imported
        self.euro_entry = {m: int(d[:4]) for m, d in EURO_ENTRY.items()}
        self.euro_text = {m: f"euro changeover:{d}:{EURO_EXIT_SOURCE}" for m, d in EURO_ENTRY.items()}
        self.gold = P.frame_a_gold()
        self.debt, self.deficit, self.s, self.units = {}, {}, {}, {}
        for m in self.monies:
            self.debt[m] = P.debt_readings(m)
            self.deficit[m] = P.deficit_readings(m)
            self.s[m], self.units[m] = P.c3_readings(m, self.deficit[m])
        self.acts_h1 = defaultdict(list)
        for r in _read_csv(ACTS_DIR / "series.csv"):
            if r["route"] == "H1":
                self.acts_h1[r["money"]].append(int(r["entry_date"][:4]))
        self.h1_span = {r["money"]: (int(r["first_year"]), int(r["last_year"]))
                        for r in _read_csv(ACTS_DIR / "coverage.csv") if r["act"] == "H1"}
        # c7 (i): the currency boards (FT-001-M3-boards.md); None until the list is committed, and then a class
        # 2 from 1971 stays "cannot be read" as frame c's second build read it
        self.boards: dict[str, list[dict]] | None = None
        if (BOARDS_DIR / "series.csv").exists():
            self.boards = defaultdict(list)
            for row in _read_csv(BOARDS_DIR / "series.csv"):
                self.boards[row["money"]].append(row)

    def timeline(self, m: str, rr_cpi_only: bool = False) -> list:
        """The money's timeline as frame b read it (``breaks.build``: ``panel.timeline`` at the common ends)."""
        key = (m, rr_cpi_only)
        if not hasattr(self, "_timelines"):
            self._timelines: dict = {}
            self._end_m = self.P.common_end(self.pan.have_monthly(), 12)
        if key not in self._timelines:
            pan = self.pan
            self._timelines[key] = self.P.timeline(m, pan.pi_monthly(m), pan.pi_annual(m, rr_cpi_only=rr_cpi_only),
                                                   pan.d_monthly(m), pan.d_annual(m), self._end_m, self.end)
        return self._timelines[key]

    def restoration_undatable(self, m: str, brk: dict, entry: int, spec: "Spec", rr_cpi_only: bool = False) -> bool:
        """N1: ``breaks.restoration_undatable`` on the money's timeline, before the entry year, at the spec's lower
        line."""
        import breaks as B
        from dataclasses import replace
        if m not in self.pan.monies:
            return False
        return B.restoration_undatable(self.timeline(m, rr_cpi_only), brk["crossing"], entry * 12,
                                       b_params(spec))

    def pi_annual(self, m: str, rr_cpi_only: bool = False) -> dict[int, float]:
        if m not in self.pan.monies:
            return {}
        return {y: v for y, (v, _, _) in self.pan.pi_annual(m, rr_cpi_only=rr_cpi_only).items()}

    def pi_years(self, m: str, rr_cpi_only: bool = False) -> set[int]:
        if m not in self.pan.monies:
            return set()
        return set(self.pi_annual(m, rr_cpi_only)) | {t // 12 for t in self.pan.pi_monthly(m)}


def habit(r: Readings, m: str, entry: int) -> str:
    span = r.h1_span.get(m)
    if any(y < entry for y in r.acts_h1.get(m, [])):
        return "no"
    if span is None or not span[0] <= entry - 1 <= span[1]:
        return "cannot be read"
    return "yes"


def war_readings(P, m: str, entry: int, spec: "Spec") -> tuple[str, dict[int, str]]:
    """(the war year at entry, the war years of entry + 1 ... entry + H), both through ``panel.war_at`` (R14) with the
    spec's ``war_after_cow`` and W12's switch ``war_ucdp`` (panel protocol section 9: the headline reads W12, the variant
    ``war-before-w12`` runs ``ucdp=False``)."""
    war = P.war_at(m, entry, spec.war_after_cow, ucdp=spec.war_ucdp)
    return war, {y: P.war_at(m, y, spec.war_after_cow, ucdp=spec.war_ucdp) for y in range(entry + 1, entry + spec.H + 1)}


def lines_for(r: Readings, spec: Spec, variant: str, sha: str) -> list[dict]:
    P = r.P
    b_rows = _read_csv(B_DIR / spec.b_list)
    breaks_by = breaks_from_b(b_rows, spec.b_bound)
    rr_cpi_only = spec.b_list == "variant-rr-cpi-only.csv"
    c4_all = r.c4[spec.c4_list]
    irr = P.irr_classes()
    garriga, ka = P.garriga(), P.ka_open()
    out = []
    for m in r.monies:
        first_inside = r.euro_entry.get(m)
        last_year = min(r.end, first_inside - 1) if first_inside else r.end
        debt, deficit, s, c4 = r.debt[m], r.deficit[m], r.s[m], c4_all.get(m, {})
        met_by, readable = {}, {}
        for y in range(P.FIRST_YEAR, last_year + 1):
            sv = s.get(y, (None,))[0]
            reading = {"debt": debt.get(y, (None,))[0], "deficit": deficit.get(y, (None,))[0],
                       "s": None if sv is None or sv != sv else sv,
                       "c4": c4[y]["measure"] if y in c4 else None}
            met_by[y] = met(reading, spec.lines)
            readable[y] = {k for k, v in (("c1", y in debt), ("c2", y in deficit), ("c3", y in s)) if v}
        years_read = [y for y, v in readable.items() if v]
        first_year = min(years_read) if years_read else None
        pi = r.pi_annual(m, rr_cpi_only)
        pi_years = r.pi_years(m, rr_cpi_only)
        mb = breaks_by.get(m, [])
        sources = {"c1": {y: v[1] for y, v in debt.items()}, "c2": {y: v[1] for y, v in deficit.items()}}
        for entry, route, routes in entries(met_by, spec.H):
            flags = entry_flags(entry, routes, readable, sources, first_year, spec.lines)
            if "c4" in routes and c4[entry]["flag"]:
                flags.append("c4_flag")
            if route == "c1" and (entry > 2009 or m not in P.rr_debt_monies()):
                flags.append("c1_outside_fit")
            era_name, straddle = era(entry)
            if straddle:
                flags.append("era_boundary_year")
            cls, note = P.class_at(irr.get(m), entry)
            if "regime_carried" in note:
                flags.append("regime_carried")
            # apart (c7)
            if entry <= 1970:
                conv = convertible_before_1971(entry, r.gold["1"].get(m), r.gold["2"].get(m))
            elif cls == 2 and r.boards is not None:
                conv, board_carried = board_at(r.boards.get(m, []), entry, spec.boards_with_comments)
                if board_carried:
                    flags.append("board_carried")
            elif cls is None or cls == 2:
                conv = "cannot be read"
            else:
                conv = "no"
            if spec.entry_year_counted:
                v = pi.get(entry - 1)
                infl = "cannot be read" if v is None else ("yes" if v >= spec.lines.lower else "no")
            else:
                infl = already_inflating(pi, entry, spec.lines.lower)
            past = past_onset(mb, entry)
            if past == "cannot be read":
                flags.append("past_onset_residual")
            during = during_break(mb, entry, lambda b, e: r.restoration_undatable(m, b, e, spec, rr_cpi_only))
            if during == "cannot be read":
                flags.append("restoration_undatable")
            war, war_map = war_readings(P, m, entry, spec)
            if spec.war_unreadable_as_no:
                war_apart, war_flags = war_reading(war)
            else:
                war_apart, war_flags = war, (["war_unreadable_at_entry"] if war == "cannot be read" else [])
            flags += war_flags
            apart = {"convertible at entry": conv, "already inflating": infl, "during a break": during,
                     "past frame b's onset": past, "a war year at entry": war_apart}
            res = outcome(mb, entry, spec.H, pi_years, r.end, first_inside, r.euro_text.get(m, ""))
            within = [b for b in mb if entry + 1 <= int(b["crossing"][:4]) <= entry + spec.H]
            if within and within[0]["ifs_break"] == "yes":
                flags.append("ifs_break")
            status, reason = status_of(apart, res)
            if res["status"] == "cannot be read":
                flags.append("outcome_unreadable")        # M4: read both ways by the claims
            if status == "ended unbroken":
                flags.append("euro_announcement_read_met")  # M6: read both ways by the claims
            if status == "counted":
                outc, outc_date, onset_date, so_far = res["outcome"], res["outcome_date"], res["onset_date"], ""
                restored = res["restored"]
            else:
                outc = outc_date = onset_date = restored = ""
                so_far = res["so_far"] or (f"{res['outcome']} {res['outcome_date']}".strip() if res["outcome"] else "")
            if route == "c4":
                measure, mdate = c4[entry]["measure"], c4[entry]["c"]
                src = "C15-e-episodes-closed (pilot run, fccce91)"
                loc = f"{P.C15_RUN.relative_to(ROOT).as_posix()}, result.lists.{spec.c4_list}, episode c {mdate}"
            elif route == "c3":
                measure, mdate = s[entry][0], str(entry)
                src = s[entry][1]
                loc = f"IFS A~~12A___XDC / A~~FASAG_XDC, A~~NGDP_XDC or WB NY.GDP.MKTP.CN; deficit per its source, {m}, {entry}"
            elif route == "c1":
                measure, mdate, src = debt[entry][0], str(entry), debt[entry][1]
                loc = f"{DEBT_LOC[src]}, {m}, {entry}"
            else:
                measure, mdate, src = deficit[entry][0], str(entry), deficit[entry][1]
                loc = f"{DEFICIT_LOC[src]}, {m}, {entry}"
            year = entry
            gv = garriga.get(m, {}).get(year, {})
            dflt = P.default_at(m, year, total=spec.default_total)
            sup = P.supports(dflt, gv.get("cuk_limlen"), cls, gv.get("lvau_garriga"), ka.get(m, {}).get(year))
            grid = {
                "supports_count_cap_025": P.supports(dflt, gv.get("cuk_limlen"), cls, gv.get("lvau_garriga"),
                                                     ka.get(m, {}).get(year), cap_line=0.25)["supports_count"],
                "supports_count_cap_075": P.supports(dflt, gv.get("cuk_limlen"), cls, gv.get("lvau_garriga"),
                                                     ka.get(m, {}).get(year), cap_line=0.75)["supports_count"],
                "supports_count_index_04": P.supports(dflt, gv.get("cuk_limlen"), cls, gv.get("lvau_garriga"),
                                                      ka.get(m, {}).get(year), index_line=0.4)["supports_count"],
                "supports_count_index_06": P.supports(dflt, gv.get("cuk_limlen"), cls, gv.get("lvau_garriga"),
                                                      ka.get(m, {}).get(year), index_line=0.6)["supports_count"],
                "supports_count_ka_01": P.supports(dflt, gv.get("cuk_limlen"), cls, gv.get("lvau_garriga"),
                                                   ka.get(m, {}).get(year), ka_line=0.1)["supports_count"],
                "supports_count_ka_05": P.supports(dflt, gv.get("cuk_limlen"), cls, gv.get("lvau_garriga"),
                                                   ka.get(m, {}).get(year), ka_line=0.5)["supports_count"]}
            out.append({
                "period": str(entry), "value": round(measure, 6), "unit": UNITS[route], "source": src,
                "locator": loc, "note": "", "uncertainty": "", "money": m, "frame": "c", "route": route,
                "entry_date": str(entry), "entry_measure": round(measure, 6), "entry_measure_date": mdate,
                "outcome": outc, "outcome_date": outc_date, "onset_date": onset_date, "responses": "",
                "exit": res["exit"] if status == "ended unbroken" else "",
                "status": status, "coder": CODER, "rules_sha256": sha, "reason": reason, "H": spec.H,
                "routes_met": " ".join(routes),
                "debt_pct_gdp_source": debt[entry][1] if entry in debt else "cannot be read",
                "deficit_pct_gdp_source": deficit[entry][1] if entry in deficit else "cannot be read",
                "c3_units_ok": r.units[m],
                "tercile": "", "era": era_name, "era_boundary_year": "yes" if straddle else "",
                "default_at_entry": dflt, "default_at_entry_total_stock": P.default_at(m, year, total=True),
                **sup, "habit": habit(r, m, entry), "world_demand": "cannot be read", **grid,
                "regime_at_entry": cls if cls is not None else "cannot be read", "regime_note": note,
                "split_at_entry": P.split_at(m, str(entry)), "convertible_at_entry": conv,
                "already_inflating": infl, "during_a_break": during, "past_frame_b_onset": past, "war_at_entry": war,
                "war_years_in_H": war_in_h(war_map, entry, spec.H), "restored_date": restored, "so_far": so_far,
                "flags": " ".join(flags), "c4_c": c4[entry]["c"] if "c4" in routes else "",
                "euro_changeover_year": first_inside or "",
                "shared_or_foreign_money": "yes" if cls == 1 else "",
                "new_money_rule": "not applied", "variant": variant})
    if spec.drop_flag:
        out = [x for x in out if spec.drop_flag not in x["flags"].split()]
    if spec.regime_carried_out:
        out = [x for x in out if "regime_carried" not in x["flags"].split()]
    cuts = {}
    for route in ROUTES:
        values = [x["entry_measure"] for x in out if x["route"] == route]
        if values:
            cuts[route] = terciles(values)
            for x in out:
                if x["route"] == route:
                    x["tercile"] = tercile(x["entry_measure"], cuts[route])
    return out, cuts


WAR_MOVE_FIELDS = ("war_at_entry", "war_years_in_H")     # what ``war-moves.csv`` compares (panel protocol section 9)


def write(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def summary(rows: list[dict]) -> dict:
    return {"lines": len(rows), "status": Counter(r["status"] for r in rows),
            "by_route": Counter(f"{r['route']} {r['status']}" for r in rows),
            "outcome": Counter(r["outcome"] for r in rows if r["status"] == "counted"),
            "reason": Counter(r["reason"] for r in rows if r["status"] in ("apart", "cannot be read")),
            "flags": Counter(f for r in rows for f in r["flags"].split())}


def build() -> dict:
    sys.path.insert(0, str(HERE))
    import m0
    import panel as P
    sha = m0.require_locked()
    card = m0.rules()["reused_from_pilot"]["c4_card"]["card_hash"]
    problems = P.c15_check(card)
    if problems:
        raise SystemExit("C15: " + "; ".join(problems))
    r = Readings()
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"end": r.end, "euro_entry": dict(r.euro_entry), "units_not_ok": {m: v for m, v in r.units.items() if v != "yes"}}
    report["panel_digest"], report["panel_readings"] = panel_digest(r)
    report["c4_monies"] = len(r.c4["headline"])
    report["monies"] = len(r.monies)
    report["unread_areas"] = {k: sorted(v) for k, v in P.UNREAD_AREAS.items()}
    report["rr_sheets_without_debt_column"] = sorted(set(P.rr_debt_monies()) - {m for m, v in P.rr_debt().items() if v})
    head, cuts = lines_for(r, HEADLINE, "headline", sha)
    # O2: the smallest detectable effect, on no outcome, printed before any count
    report = {"claim2_mde": {k: claim2_mde(head, k) for k in ("supports_count", "supports_count_without_pegs",
                                                                "supports_count_without_taken_back")}, **report}
    write(OUT / "series.csv", head)
    report["headline"] = summary(head)
    report["cuts"] = {"headline": cuts}
    report["variants"] = {}
    for name, spec in {**VARIANTS, **_b_variant_specs()}.items():
        rows, vcuts = lines_for(r, spec, name, sha)
        write(OUT / f"variant-{name}.csv", rows)
        if name == "war-before-w12":              # panel protocol section 9: the move W12 made, line by line
            moves = P.war_moves(head, rows, WAR_MOVE_FIELDS)
            P.write_war_moves(OUT / "war-moves.csv", moves)
            report["war_moves"] = {"lines": len(moves), "by_field": Counter(x["field"] for x in moves),
                                   "status": Counter(f"{x['status_before']} -> {x['status_after']}" for x in moves)}
        report["variants"][name] = summary(rows)
        report["cuts"][name] = vcuts
    return report



def panel_digest(r: "Readings") -> tuple[str, Counter]:
    """The digest of frame c's panel (debt, deficit and c3 readings, sorted) and its readings by item and source."""
    import hashlib
    h, tally = hashlib.sha256(), Counter()
    for m in r.monies:
        for item, table in (("debt", r.debt[m]), ("deficit", r.deficit[m]), ("c3", r.s[m])):
            for y, (v, src) in sorted(table.items()):
                h.update(f"{m}|{item}|{y}|{v:.10g}|{src}\n".encode())
                tally[f"{item} | {src.split(' / ')[0] if item != 'c3' else 'IFS ' + src.split(' ')[1]}"] += 1
    return h.hexdigest(), tally


if __name__ == "__main__":
    if sys.argv[1:2] == ["build"]:
        import json
        rep = build()
        print(json.dumps(rep, default=lambda o: {str(k): v for k, v in o.items()} if isinstance(o, dict) else str(o),
                         indent=1))
    else:
        print(__doc__)
        sys.exit(2)
